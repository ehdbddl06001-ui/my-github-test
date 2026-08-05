#!/usr/bin/env python3
"""Q4-F(`quest46_q4f_deployment_mode`) 픽스처 — 배포 방식 + 부담 정량.

Q4-E(`20260805T0413`)가 두 가지를 동시에 보였다.

**(좋은 쪽)** 매크로 **AUROC 0.9418**, 유병률 사분위별 AUROC 0.9513/0.9461/0.9358/0.9340 로
**거의 평평**하다. 「고유병률에서 무의미」는 **PR-AUC 의 무작위 기저선이 유병률**이라 lift 가
떨어지는 것이지 모델 열화가 아니다(레코드 48 도 AUROC 0.8491).

**(나쁜 쪽)** 그런데 **전역 단일 문턱**에서 레코드 48 이 FN **1816**, 상위 6개만으로 FN 3342.
순위는 좋은데 **절대 수준이 어긋나** 문턱을 아무도 못 넘는다.

그리고 해법이 이미 로그 안에 있었다 — **환자별 예산**이 민감도를 0.2743 → 0.5030(**1.83배**).
게다가 예산 방식에서는 네 팔이 같다(raw 0.5054 = A_em 0.5054 ≈ TE 0.5030).

이 런에서 빠뜨리면 결과가 무효인 것 여섯:
  ① **J2 가 자다** — 예산은 레코드 **내 순위만** 쓰고 `A_em` 은 레코드별 **상수 시프트**이므로
     둘이 **정확히** 같아야 한다. 서면 **처방에서 층② 를 통째로 뺄 수 있다**
  ② **J1 은 총 경보 수를 맞춰** 비교한다 — 안 맞추면 **많이 울리는 쪽이 민감도로 이긴다**
     (Q4-E 스모크에서 `A_em` 이 경보율 0.2505 로 그랬다)
  ③ **환자 평균 민감도와 총 FN 은 반대로 갈 수 있다** — 전자는 레코드 동등 가중(R11),
     후자는 양성 수 가중이다. 숨기지 말고 **명시**해야 한다(R38 ⑦)
  ④ **절대 예산**(기록당 100·300개)도 잰다 — 24시간 홀터에서 5% 는 5000개로 판독 불가능하다
  ⑤ **부담 정량(π̂ 오차)** — 고유병률 환자의 임상 과제는 탐지가 아니라 **정량**이다.
     이 퀘스트가 **한 번도 안 잰 지표**다(Q3 은 π̂ 가 순위에 주는 영향만 봤다)
  ⑥ **문턱·TPR/FPR 을 그 fold 의 DEV 에서만** 추정한다(R22 · R34 ②)
"""
import json
import os
import re
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NB = os.path.join(ROOT, "notebooks", "quest46_q4f_deployment_mode.ipynb")

PASS, FAIL = [], []


def ok(cond, msg):
    (PASS if cond else FAIL).append(msg)
    print(("  ✅ " if cond else "  ❌ ") + msg)


def cells():
    with open(NB, encoding="utf-8") as f:
        nb = json.load(f)
    return ["".join(c["source"]) for c in nb["cells"] if c["cell_type"] == "code"]


def md():
    with open(NB, encoding="utf-8") as f:
        nb = json.load(f)
    return "\n".join("".join(c["source"]) for c in nb["cells"]
                     if c["cell_type"] == "markdown")


def src():
    return "\n".join(cells())


# ══════════════════════════════════════════════════════════════════ 정적
def static():
    print("\n[정적] 노트북 소스 불변식")
    s = src()
    cs = cells()

    # ── ① J2 가 자
    ok("def alloc_budget" in s and "np.partition(sc, -k)" in s,
       "① 환자별 예산이 **문턱 없이** 레코드별 상위 k개로 정의돼 있다")
    ok('raise AssetError(f"J2 실패' in s,
       "① ★★★ J2 가 깨지면 **중단**한다(R29 ②)")
    ok("레코드 **내 순위만**" in s and "상수 시프트" in s,
       "① ★★★ 왜 정확히 같아야 하는지(예산=레코드 내 순위 · A_em=상수 시프트)가 소스에 있다")
    ok("처방에서 층② 를 통째로 뺄 수 있다" in s or "층② 를 통째로 뺄 수 있다" in s,
       "① ★★★ J2 가 서면 **층② 를 처방에서 뺀다**는 결론이 박혀 있다")
    ok("d2p = max(abs(B[q][\"raw\"][r][\"ppv\"]" in s,
       "① 민감도뿐 아니라 **PPV 도** 같은지 본다")
    ok("MAIN_ARM" in s and 'MAIN_ARM = "raw"' in s,
       "① 처방 후보 팔이 `raw` 로 사전등록돼 있다")

    # ── ② J1 은 총 경보 수를 맞춘다
    ok("def matched_budget" in s and 'gstat[r]["flagged"]' in s,
       "② ★★★ 전역 문턱이 쓴 **총 경보 수**를 세서 그만큼만 배분한다")
    ok("많이 울리는 쪽이 민감도로 이긴다" in s and "R36 ②" in s,
       "② ★★★ 왜 맞춰야 하는지가 소스에 있다")
    ok("tot_global" in s and "tot_budget" in s,
       "② 두 방식의 총 경보 수를 **결과에 저장**한다(맞았는지 확인 가능)")
    ok("0.2505" in s,
       "② Q4-E 스모크의 반례(경보율 0.2505)가 앵커로 박혀 있다")

    # ── ③ 두 수가 반대로 갈 수 있다
    ok("반대로 갈 수 있다" in s or "반대 방향이다" in s,
       "③ ★★★ 환자 평균 민감도와 총 FN 이 **반대로 갈 수 있다**는 게 소스에 있다")
    ok('if (m_ > 0) != (fn_g - fn_b > 0):' in s,
       "③ ★★★ 실제로 반대로 가면 **런타임에 경고**한다(R38 ⑦)")
    ok("양성 수로 가중" in s and "동등 가중" in s,
       "③ ★★ 두 가중이 다르다는 설명이 있다")
    ok("R11 이 주 지표로 요구한 건 환자 단위" in s,
       "③ ★★ 어느 쪽이 주 지표인지(R11 = 환자 단위) 못박았다")

    # ── ④ 절대 예산
    ok("FLAG_K = (100, 300)" in s,
       "④ ★★ **절대 예산**(기록당 100·300개)이 사전등록돼 있다")
    ok("판독 불가능" in s and "24시간" in s,
       "④ ★★★ 왜 분율이 아니라 절대 개수인지(24시간 홀터에서 5%=5000개)가 소스에 있다")
    ok("BK = {k: alloc_budget" in s,
       "④ 절대 예산으로도 실제 계산한다")

    # ── ⑤ 부담 정량
    ok('PI_EST = ("em", "mean_p", "bbse", "count")' in s,
       "⑤ ★★★ 부담 추정기 **네 개**가 사전등록돼 있다")
    ok("(rate - fpr) / (tpr - fpr)" in s,
       "⑤ ★★ BBSE / Rogan-Gladen 보정식이 구현돼 있다")
    ok('tpr = float((dl[dy] >= thr).mean())' in s and 'd["logit"]' in s,
       "⑤ ★★★ TPR·FPR 을 **그 fold 의 DEV 에서만** 추정한다(R22)")
    ok("탐지가 아니라" in s and "정량" in s,
       "⑤ ★★★ 고유병률 환자의 과제가 **탐지가 아니라 정량**이라는 게 소스에 있다")
    ok("한 번도 안 잰" in s,
       "⑤ ★★ 이 퀘스트가 π̂ 오차를 지표로 잰 적이 없다는 게 기록돼 있다")
    ok("rel_med" in s and "np.median(rel)" in s,
       "⑤ 절대 오차뿐 아니라 **상대 오차**도 낸다(유병률이 82배 벌어져 있다)")
    ok("hi_r = [r for r in REC_OK if BURD[r] >= qs[3]]" in s,
       "⑤ ★★ **고유병률 사분위에서 따로** 오차를 낸다 — 거기가 정량 트랙의 표적이다")

    # ── ⑥ DEV 에서만
    ok('thr = float(np.quantile(dev[r]["logit"], 1.0 - q))' in s,
       "⑥ ★★★ 전역 문턱을 **DEV 분위수**로 잡는다")
    ok('dev[held] = dict(logit=cl(s_dv)' in s,
       "⑥ fold 마다 DEV 로짓·라벨을 따로 남긴다")
    ok("r != held" in s and "def split_rest(held)" in s,
       "⑥ ★★ LORO — held-out 이 TRAIN·DEV 어디에도 안 들어간다(R22)")
    ok("TEST 에서 쓸어보지 않는다" in s,
       "⑥ 예산을 사전 고정했다는 게 명시돼 있다(R34 ②)")

    # ── 판정 위생
    ok("모델 열화가 아니" in s and "qband_auc" in s,
       "★★★ 「고유병률에서 낮은 lift 는 모델 열화가 아니다」가 Q4-E 앵커와 함께 박혀 있다")
    ok("탐지의 임상적 가치가 낮은 것은 사실" in s,
       "★★ 그렇다고 **탐지의 임상적 가치가 낮은 것은 사실**이라고 인정한다(과잉 방어 없음)")
    ok('j1v = decide(J1[q]["lo"], J1[q]["hi"], J1_THR, ">")' in s
       and "J1_THR = max(0.0, NS[2])" in s,
       "★★ 주 관문이 **측정된 영점 상단**을 문턱으로 쓴다(R26)")
    ok("def decide(lo, hi, thr, direction)" in s and "np.isfinite(thr)" in s,
       "★ `decide` 가 문턱이 nan 이면 미결을 낸다")
    ok("해석 불가" in s and "R41 ②" in s,
       "★ 효과가 0 근처면 필요표본을 해석 불가로 표시한다")
    ok("미결 ≠ 등가" in s or "R33 ①" in s,
       "★ 「미결 ≠ 등가」가 소스에 있다")
    ok('raise AssetError(f"{SV5} 없음' in s,
       "★ 자산 없으면 fallback 없이 중단(R16)")
    ok("새 데이터 0" in md() or "새 데이터 0" in s,
       "★ 새 데이터를 안 쓴다는 게 명시돼 있다")
    knob = re.findall(r"^\s*(\w+)\s*=\s*[^=].*\bif SMOKE\b", s, flags=re.M)
    ok(set(knob) <= {"NB_BOOT", "N_PERM"},
       f"★★★ SMOKE 로 값이 바뀌는 이름이 **비용 손잡이뿐**이다({sorted(set(knob))})")
    ok(not re.search(r"^\s*(FLAG_Q|FLAG_K|MAIN_Q|TOL_IDENT)\s*=.*SMOKE", s, flags=re.M),
       "★★★ 예산·허용오차는 SMOKE 와 무관하게 고정이다")


# ══════════════════════════════════════════════════════════════════ 동적
def dynamic():
    print("\n[동적] 합성 데이터로 설계 불변식을 **실제로** 검증")
    from sklearn.metrics import roc_auc_score

    rng = np.random.RandomState(41)
    pis = [0.01, 0.03, 0.08, 0.15, 0.28, 0.45, 0.58]
    sz = [900, 800, 700, 600, 500, 400, 300]
    recs = np.concatenate([np.full(sz[r], r) for r in range(7)])
    y = np.zeros(len(recs), int)
    for r in range(7):
        m = np.where(recs == r)[0]
        y[m[:int(pis[r] * len(m))]] = 1
    sc = rng.normal(0, 1, len(recs)); sc[y == 1] += 1.1
    REC = list(range(7))

    def budget(s_, k_of):
        out = {}
        for r in REC:
            m = recs == r; ss = s_[m]; yy = y[m] == 1
            k = int(min(max(1, k_of(r)), m.sum()))
            fl = ss >= np.partition(ss, -k)[-k]
            tp = int((fl & yy).sum())
            out[r] = dict(sens=tp / max(1, int(yy.sum())), tp=tp,
                          fn=int(yy.sum()) - tp, flagged=int(fl.sum()))
        return out

    def glob(s_, thr):
        out = {}
        for r in REC:
            m = recs == r; ss = s_[m]; yy = y[m] == 1
            fl = ss >= thr
            tp = int((fl & yy).sum())
            out[r] = dict(sens=tp / max(1, int(yy.sum())), tp=tp,
                          fn=int(yy.sum()) - tp, flagged=int(fl.sum()))
        return out

    # ── ⓐ J2 의 근거: 예산은 **레코드별 상수 시프트에 완전히 불변**이다
    shifted = sc.copy()
    for r in REC:
        shifted[recs == r] += np.log(pis[r] / (1 - pis[r]))       # 방법 A 시프트
    b0 = budget(sc, lambda r: int(0.05 * sz[r]))
    b1 = budget(shifted, lambda r: int(0.05 * sz[r]))
    ok(all(b0[r]["sens"] == b1[r]["sens"] and b0[r]["tp"] == b1[r]["tp"] for r in REC),
       "ⓐ ★★★ **환자별 예산은 레코드별 상수 시프트에 정확히 불변**이다 — 예산은 레코드 "
       "내 순위만 쓰기 때문. 이것이 J2 이고 **층② 를 처방에서 빼는 근거**다")
    thr = float(np.quantile(sc, 0.95))
    g0, g1 = glob(sc, thr), glob(shifted, thr)
    ok(any(g0[r]["sens"] != g1[r]["sens"] for r in REC),
       "ⓐ ★★★ 반면 **전역 문턱은 같은 시프트로 바뀐다** — 층② 가 의미를 갖는 건 오직 "
       "이 배포 방식에서다")

    # ── ⓑ 총 경보 수를 안 맞추면 「많이 울리는 쪽」이 이긴다
    lo_thr = float(np.quantile(sc, 0.75))                          # 25% 를 울린다
    g_loose = glob(sc, lo_thr)
    s_tight = float(np.mean([g0[r]["sens"] for r in REC]))
    s_loose = float(np.mean([g_loose[r]["sens"] for r in REC]))
    ok(s_loose > s_tight,
       f"ⓑ ★★★ 문턱을 낮춰 많이 울리면 민감도가 {s_tight:.4f} → {s_loose:.4f} 로 오른다 — "
       f"**총 경보 수를 안 맞추면 비교가 성립하지 않는다**")
    tot_g = sum(g0[r]["flagged"] for r in REC)
    bm = budget(sc, lambda r: int(round(tot_g / len(recs) * sz[r])))
    tot_b = sum(bm[r]["flagged"] for r in REC)
    ok(abs(tot_g - tot_b) <= max(5, 0.05 * tot_g),
       f"ⓑ ★★ 총 경보 수를 맞추면 {tot_g} vs {tot_b} 로 같아진다 — **그때만 공정하다**")

    # ── ⓒ 환자 평균 민감도와 총 FN 은 **반대로 갈 수 있다**
    ms_g = float(np.mean([g0[r]["sens"] for r in REC]))
    ms_b = float(np.mean([bm[r]["sens"] for r in REC]))
    fn_g = sum(g0[r]["fn"] for r in REC); fn_b = sum(bm[r]["fn"] for r in REC)
    ok(True,
       f"ⓒ 실측 — 환자 평균 민감도 전역 {ms_g:.4f} vs 배분 {ms_b:.4f} · 총 FN "
       f"{fn_g} vs {fn_b}")
    # 구성으로 반대 방향을 만들어 보인다
    fake_sens = dict(A=dict(s=[0.0, 0.0, 0.9], n=[10, 10, 1000]),
                     B=dict(s=[0.5, 0.5, 0.5], n=[10, 10, 1000]))
    mA = np.mean(fake_sens["A"]["s"]); mB = np.mean(fake_sens["B"]["s"])
    fnA = sum(n * (1 - s) for s, n in zip(fake_sens["A"]["s"], fake_sens["A"]["n"]))
    fnB = sum(n * (1 - s) for s, n in zip(fake_sens["B"]["s"], fake_sens["B"]["n"]))
    ok(mB > mA and fnB > fnA,
       f"ⓒ ★★★ 구성 예시 — 환자 평균 민감도는 B 가 높은데({mB:.3f} > {mA:.3f}) 총 FN 도 "
       f"B 가 많다({fnB:.0f} > {fnA:.0f}). **동등 가중과 양성 수 가중이 다르기 때문**이고, "
       f"R11 이 주 지표로 요구한 건 **환자 단위**다")

    # ── ⓓ 부담 추정 — BBSE / Rogan-Gladen 이 옳게 구현됐는가
    for tpr, fpr, pi in ((0.80, 0.10, 0.30), (0.80, 0.20, 0.10), (0.60, 0.05, 0.55)):
        rate = pi * tpr + (1 - pi) * fpr
        ok(abs((rate - fpr) / (tpr - fpr) - pi) < 1e-12,
           f"ⓓ ★★★ Rogan-Gladen 이 참 유병률을 **정확히** 복원한다"
           f"(π={pi} · TPR {tpr} · FPR {fpr} · 관측율 {rate:.4f} → "
           f"{(rate-fpr)/(tpr-fpr):.4f})")
    tpr, fpr, pi = 0.80, 0.20, 0.10
    rate = pi * tpr + (1 - pi) * fpr
    ok(abs(rate - pi) > 0.10,
       f"ⓓ ★★ 보정 안 한 **문턱초과율** {rate:.4f} 는 참값 {pi} 와 "
       f"{abs(rate-pi):.4f} 어긋난다(FPR 이 클수록 커진다) — `count` 팔이 필요한 이유")

    # ── ⓔ 유병률이 82배 벌어지면 **절대 오차만으로는 못 읽는다**
    err_lo = abs(0.05 - 0.01); err_hi = abs(0.60 - 0.56)
    ok(abs(err_lo - err_hi) < 1e-9 and (err_lo / 0.01) > 10 * (err_hi / 0.56),
       f"ⓔ ★★★ 절대 오차가 같아도(둘 다 {err_lo:.2f}) 상대 오차는 "
       f"{err_lo/0.01:.0%} vs {err_hi/0.56:.0%} 다 — **상대 오차를 함께 내야** 한다")

    # ── ⓕ 고유병률에서 낮은 lift 는 모델 열화가 아니다 (Q4-E 재확인)
    aucs = [roc_auc_score(y[recs == r], sc[recs == r]) for r in REC]
    lifts = []
    from sklearn.metrics import average_precision_score
    for r in REC:
        ap = average_precision_score(y[recs == r], sc[recs == r])
        lifts.append(ap / pis[r])
    ok(max(aucs) - min(aucs) < 0.15 and lifts[0] > 2.0 * lifts[-1],
       f"ⓕ ★★★ AUROC 는 {min(aucs):.3f}~{max(aucs):.3f} 로 **범위 "
       f"{max(aucs)-min(aucs):.3f}** 인데 lift 는 {lifts[0]:.1f}배 → {lifts[-1]:.1f}배로 "
       f"**{lifts[0]/lifts[-1]:.1f}배** 떨어진다 — 모델이 아니라 **기저선이 움직이는 것**"
       f"이다(Q4-E 실측 AUROC 0.9340~0.9513 · lift 31.8→3.3배 와 같은 구조)")
    ok(lifts[-1] < 2.0 and aucs[-1] > 0.7,
       f"ⓕ ★★ 그리고 최고유병률 레코드는 lift {lifts[-1]:.2f}배(거의 무작위처럼 보인다)인데 "
       f"AUROC 는 {aucs[-1]:.3f} 다 — **두 지표가 정반대 인상을 준다**")

    # ── ⓖ LORO 누출 없음
    def split_rest(held, every=4):
        rest = sorted([r for r in REC if r != held], key=lambda r: (pis[r], r))
        dv = [r for i, r in enumerate(rest) if i % every == 0]
        return [r for r in rest if r not in set(dv)], dv
    ok(not [h for h in REC if h in split_rest(h)[0] or h in split_rest(h)[1]],
       "ⓖ ★★★ held-out 레코드가 TRAIN·DEV 어디에도 안 들어간다(R22)")


if __name__ == "__main__":
    if not os.path.exists(NB):
        print(f"❌ 노트북이 없다 — {NB}")
        sys.exit(1)
    print("=" * 78)
    print("Q4-F 픽스처 — 예산은 시프트 불변(J2) · 총 경보 수 맞춤(J1) · 절대 예산 · "
          "부담 정량(J4)")
    print("=" * 78)
    static()
    dynamic()
    print("\n" + "=" * 78)
    print(f"통과 {len(PASS)} · 실패 {len(FAIL)}")
    for f in FAIL:
        print("  ✗ " + f)
    sys.exit(1 if FAIL else 0)
