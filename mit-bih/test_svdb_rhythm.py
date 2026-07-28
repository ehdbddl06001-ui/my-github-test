# =============================================================================
#  test_svdb_rhythm.py — svdb_rhythm.py + svdb_bench.py arm 레지스트리 통합 검증
#
#  Colab/Drive/GPU 없이 로컬에서 도는 검증. 두 가지를 확인한다:
#   (1) svdb_rhythm.selftest()          — RR 문맥·모델·판정 로직의 불변식
#   (2) 하니스 통합                      — attach_arms() 후 bench_models() 가
#       B0~B4C 와 '동일 폴드'에서 R0/R1/R2 를 함께 평가하고, fper 가 대응 비교
#       가능한 형태(같은 환자 순서·같은 길이)로 나오는지
#
#  ★B0~B4C 의 수치적 동작은 이 테스트의 대상이 아니다(내가 건드리지 않은 코드).
#    B 계열이 의존하는 colab_step67~70 헬퍼는 '테스트 더블'로 대체한다 —
#    검증 대상은 레지스트리 배선과 RSN arm 이다.
#
#  실행:  python test_svdb_rhythm.py
# =============================================================================
import os
import sys
import tempfile
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))


# ─── 테스트 더블: B 계열이 기대하는 헬퍼(colab_step67~70 유래) ───
def _doubles():
    def _determinism():
        pass

    def _median_ref(beats, pid):
        r = np.empty_like(beats)
        for p in np.unique(pid):
            m = pid == p
            r[m] = np.median(beats[m], 0, keepdims=True)
        return r.astype("float32")

    def robust_template(beats, pid, frac=0.6, n_iter=6, conf_cut=0.85, verbose=True):
        return _median_ref(beats, pid), []

    def auto_weights(y1, beta=0.9999):
        nN = (y1 == 0).sum(); nS = max((y1 == 1).sum(), 1)
        eff = lambda n: (1 - beta) / (1 - beta ** n + 1e-12)
        return float(eff(nS) / eff(nN))

    def _binmet(s, y, t):
        pos = s >= t; yp = (y == 1)
        tp = float((pos & yp).sum()); fp = float((pos & ~yp).sum()); fn = float((~pos & yp).sum())
        pr = tp / (tp + fp + 1e-9); se = tp / (tp + fn + 1e-9)
        return pr, se, 2 * pr * se / (pr + se + 1e-9)

    def _best_t_f1(s, y, n=300):
        ts = np.unique(np.quantile(s, np.linspace(0.50, 0.9995, n)))
        best = (-1.0, ts[0])
        for t in ts:
            f1 = _binmet(s, y, t)[2]
            if f1 > best[0]: best = (f1, t)
        return float(best[1])

    def _pp_center2(s, pid, sep=1.0):
        out = s.copy().astype(np.float64)
        for p in np.unique(pid):
            m = pid == p
            out[m] = s[m] - np.median(s[m])
        return out

    def _net(fdim):
        import torch, torch.nn as nn
        class Net(nn.Module):
            def __init__(s):
                super().__init__()
                s.c = nn.Sequential(nn.Conv1d(2, 16, 7, padding=3), nn.ReLU(),
                                    nn.AdaptiveAvgPool1d(1))
                s.fm = nn.Sequential(nn.Linear(max(fdim, 1), 32), nn.ReLU())
                s.cls = nn.Linear(16 + 32, 3)
            def forward(s, b, rr, ft):
                return s.cls(torch.cat([s.c(b).squeeze(-1), s.fm(ft)], -1))
        return Net()

    return dict(_determinism=_determinism, _median_ref=_median_ref,
                robust_template=robust_template, auto_weights=auto_weights,
                _best_t_f1=_best_t_f1, _binmet=_binmet, _pp_center2=_pp_center2,
                _net=_net)


def main():
    ok = lambda c, m: (_ for _ in ()).throw(AssertionError(m)) if not c else print(f"  ✔ {m}")

    # ── (1) 단위 자기검증 ────────────────────────────────────────────────
    g = dict(__name__="svdb_rhythm_test")
    exec(open(f"{HERE}/svdb_rhythm.py").read(), g)
    g["selftest"]()

    # ── (2) 하니스 통합 ─────────────────────────────────────────────────
    print("\n=== 하니스 통합 검증 (svdb_bench arm 레지스트리) ===")
    beat, y, pid, pre, post = g["_synth"](n_rec=9, n_beat=260, seed=1)
    tmp = tempfile.mkdtemp()
    feat = os.path.join(tmp, "svdb_feats"); os.makedirs(feat, exist_ok=True)
    np.savez(os.path.join(tmp, "svdb_data.npz"),
             beat=beat, y=y, pid=pid, pre_rr=pre, post_rr=post)
    rng = np.random.RandomState(0)
    dims = dict(WST=8, MORPHO=6, REPOL=4, RHYTHM=10, KOOPMAN=5, GNN=5, AE=5)
    for nm, d in dims.items():
        np.save(f"{feat}/{nm}.npy", rng.randn(len(y), d).astype("float32"))
    np.save(f"{feat}/RR.npy", np.stack([pre, post], 1).astype("float32"))

    H = dict(__name__="svdb_bench_test")
    H.update(_doubles())                       # → step70 체인 exec 를 건너뛴다
    exec(open(f"{HERE}/svdb_bench.py").read(), H)
    H["_BASE"] = tmp; H["_SFEAT"] = feat       # Drive 대신 임시 디렉터리

    ok(callable(H.get("register_arm")), "register_arm 노출됨")
    ok(H["EXTRA_ARMS"] == {}, "초기 EXTRA_ARMS 비어 있음")

    # svdb_rhythm 을 하니스와 '같은 globals'에 얹는다 (Colab exec 순서와 동일)
    exec(open(f"{HERE}/svdb_rhythm.py").read(), H)
    n = H["attach_arms"](which=("R0","R1","R2","R3","R4"), n_seed=1, epochs=3)
    ok(n == 5 and len(H["EXTRA_ARMS"]) == 5, f"arm {n}개 등록 (EXTRA_ARMS={list(H['EXTRA_ARMS'])})")

    OUT = H["bench_models"](n_rep=1, k=3, use_ae=True)
    R = OUT["res"]
    ok(not OUT["dead"], f"실패한 arm 없음 (dead={OUT['dead']})")
    for a in ("R0.RSN(리듬만)", "R1.RSN(리듬+형태)", "R2.RSN(+Poincaré)",
              "R3.RSN(+환자템플릿)", "R4.RSN(+P파)"):
        ok(a in R, f"{a} 결과 존재 (매크로F1={R[a]['macro']:.3f})")

    # 대응 비교의 전제: 모든 arm 의 환자별 F1 벡터가 같은 길이·같은 환자 순서
    ls = {a: len(R[a]["fper"]) for a in R}
    ok(len(set(ls.values())) == 1, f"모든 arm 의 fper 길이 동일 ({set(ls.values())})")

    # ★합성 데이터에는 이제 이소성 P파가 들어 있으므로 '형태만으로는 S 를 못 잡는다'는
    #   전제가 성립하지 않는다(B2 도 P 를 보고 잘 맞힌다). 실데이터의 결론1과 달리
    #   합성은 P 대비가 과장돼 있기 때문이며, 이는 배선 검증용 데이터의 성질일 뿐이다.
    #   따라서 B2 와 비교하지 않고, RSN 이 자명한 하한을 확실히 넘는지만 확인한다.
    ok(R["R1.RSN(리듬+형태)"]["macro"] > max(R["B0.다수결"]["macro"], 0.4),
       f"R1 {R['R1.RSN(리듬+형태)']['macro']:.3f} > 자명한 하한(B0=0, 0.4)")
    ok(R["R4.RSN(+P파)"]["macro"] >= R["R1.RSN(리듬+형태)"]["macro"] - 0.15,
       f"R4 {R['R4.RSN(+P파)']['macro']:.3f} 가 R1 {R['R1.RSN(리듬+형태)']['macro']:.3f} 대비 붕괴하지 않음")

    rep = H["report"](OUT, base="B2.CNN(raw)")
    ok("R1.RSN(리듬+형태)" in rep and "ci" in rep["R1.RSN(리듬+형태)"], "report() 대응 비교 산출")

    # 오류 분해에 필요한 것들이 OUT 에 실렸는지 (없으면 '왜 낮은가'를 못 묻는다)
    ok("pred" in R["R1.RSN(리듬+형태)"], "RES 에 비트별 pred 저장됨")
    ok("order" in OUT and len(OUT["order"]) == len(OUT["y"]), "OUT 에 원본 색인 order 저장됨")
    ep = H["error_profile"](OUT, "R1.RSN(리듬+형태)", topn=5)
    ok(ep["rows"] and {"tp", "fp", "fn", "contam", "hrv"} <= set(ep["rows"][0]),
       "error_profile: 환자별 FP/FN + 공변량 산출")
    r0 = ep["rows"][0]
    ok(r0["tp"] + r0["fn"] == r0["n_S"], "오류 분해 정합(TP+FN = 실제 S 수)")
    ok(H["error_profile"]({"res": {"X": dict(fper=[1])}, "y": [], "pid": []}, "X") == {},
       "pred 없는 옛 OUT 은 안내 후 안전 종료")

    # 점수 저장 + 천장 분석 (순위 문제 vs 임계 문제 판정)
    ok(R["R1.RSN(리듬+형태)"].get("score") is not None, "RES 에 연속 점수 score 저장됨")
    ca = H["ceiling_analysis"](OUT, "R1.RSN(리듬+형태)")
    ok("oracle" in ca and len(ca["oracle"]) == len(ca["cur"]), "천장 분석: 오라클 임계 F1 산출")
    ok((ca["oracle"] >= ca["cur"] - 1e-9).all(),
       "오라클 임계 F1 은 항상 현재 이상(상한의 정의)")
    ok(H["ceiling_analysis"]({"res": {"X": dict(fper=[1], score=None)}}, "X") == {},
       "score 없는 옛 OUT 은 안내 후 안전 종료")

    # only= 로 일부만 학습 → merge_out 으로 합치기 (재실행 시간 절약의 핵심)
    O_only = H["bench_models"](n_rep=1, k=3, use_ae=True, only=["R4.RSN(+P파)"])
    ok(set(O_only["res"]) == {"R4.RSN(+P파)"}, f"only= 로 1개만 학습됨 {list(O_only['res'])}")
    M = H["merge_out"](O_only, OUT)
    ok(set(M["res"]) == set(OUT["res"]) | {"R4.RSN(+P파)"}, "병합 후 arm 집합이 합집합")
    ok(len(set(len(M["res"][a]["fper"]) for a in M["res"])) == 1,
       "병합 후에도 모든 arm 의 fper 길이 동일(대응비교 성립)")
    ok(np.array_equal(M["res"]["B4.본연구"]["fper"], OUT["res"]["B4.본연구"]["fper"]),
       "재사용된 arm 의 값이 그대로 보존됨")
    # 정렬이 다르면 반드시 거부해야 한다 (조용한 오비교 방지)
    bad = dict(O_only); bad["pid"] = np.asarray(O_only["pid"])[:-1]
    try:
        H["merge_out"](bad, OUT); ok(False, "정렬 불일치 거부")
    except ValueError:
        ok(True, "정렬 불일치 시 병합 거부(조용한 오비교 방지)")

    # arm 이 예외를 던져도 전체 실행이 죽지 않아야 한다
    H["clear_arms"]()
    H["register_arm"]("Z.고장난arm", lambda ctx: (_ for _ in ()).throw(RuntimeError("의도된 실패")))
    O2 = H["bench_models"](n_rep=1, k=3, use_ae=True)
    ok(O2["dead"] == ["Z.고장난arm"] and "Z.고장난arm" not in O2["res"],
       "실패 arm 은 격리되고 나머지 결과는 보존됨")

    # 잘못된 길이를 반환하는 arm 도 거부되어야 한다
    H["clear_arms"]()
    H["register_arm"]("Z.길이틀림", lambda ctx: np.zeros(3, bool))
    O3 = H["bench_models"](n_rep=1, k=3, use_ae=True)
    ok(O3["dead"] == ["Z.길이틀림"], "길이 계약 위반 arm 거부")

    print("\n=== 통합 검증 전 항목 통과 ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
