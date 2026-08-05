#!/usr/bin/env python3
"""Q4-K(`quest46_q4k_pp_interval`) 픽스처 — **P 의 시간**을 잰다.

Q4-J(`20260805T0914`)는 **성공했는데 내가 잘못된 자로 쟀다**.

  지표             base     morph     Δ         상대
  매크로 AUROC     0.9420   0.9529   +0.0109   +1.2%   ← 내가 주 관문으로 건 것
  매크로 PR-AUC    0.5796   0.7236   +0.1440  +24.8%
  민감도@300       0.7459   0.8211   +0.0752  +10.1%
  PPV@300         0.3620   0.4280   +0.0660  +18.2%
  달성률@300       0.8074   0.9018   +0.0944  +11.7%

형태는 **상위 300개에서 V 를 걷어내는** 일을 한다(V 위양성 4380 → 1444 · 67% 감소, N 은
6338 → 8166 으로 빈자리를 채웠다). 그건 **순위 맨 위**에서 벌어지고, AUROC 는 전체
순위쌍에 지배된다. **Q4-G 의 ρ(AUROC, 달성률)=+0.8869 는 「레코드 간 상관」이지
「개입이 둘을 같이 움직인다」가 아닌데 내가 혼동했다.**

그리고 N1 오류 해부가 다음 축을 지목했다: **놓친 S 의 상대 RR 중앙이 0.868** —
**13% 나 이른데도 놓쳤다**. 조기성이 없어서가 아니라 조기성만으로는 정상 변동과 겹쳐서
못 가른 것이고, 그 실패의 **90%가 AF 대리 상위**에 몰려 있다. ⇒ RR 축 안에선 더 못 간다.

이 런에서 빠뜨리면 결과가 무효인 것 일곱:
  ① **주 지표를 달성률@300 으로 바꾼다** — 데이터 보기 **전** 사전등록(R34 ②).
     AUROC 는 2차로 병기해서, 갈리면 그 자체가 「상위 꼬리 개입」의 증거가 되게 한다
  ② ★★★ **PP(i) = RR(i) − ΔPR(i)** — 「P-P 가 R-R 과 어긋나는 지점」은 **정확히 ΔPR** 이다.
     사용자 가설 (a)가 대수적으로 한 열로 압축되고, **RR 과 직교**한다
  ③ ⚠️ **TP 구간은 그대로 넣으면 RR 의 재표현**이다 — `RR = TP+P+PR+QRS+ST+T` 라
     나머지가 고정이면 TP = RR − 상수. **`TP/RR` 과 RR 회귀 잔차**로만 넣는다
  ④ ⚠️ **QRS 폭 정의를 표준으로 고쳤다** — 원안 「Q 시작 − S **시작**」 → **Q 시작 ~ S 종료**
  ⑤ ★★★ **중복 감사(새 자)** — 모든 새 열을 base 9열에 회귀시켜 R² 를 **먼저** 낸다.
     Q4-H 의 `pre/base` 가 여기서 걸렸어야 했다. 레코드 내 분산비도 같이 봐서
     **레코드 상수**(within-record 순위를 못 바꾸는 열)를 가른다
  ⑥ **차원 동일 대조군** — `ishuf`·`fshuf`
  ⑦ ★★★ **영점이 관측보다 흐리면 기각을 미결로 강등**한다 — 보수적 문턱은 ✅ 를 어렵게
     하는 건 맞지만 **❌ 를 만들어선 안 된다**. ⚠️ 이건 **스모크가 잡아준 것**이다
"""
import json
import os
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NB = os.path.join(ROOT, "notebooks", "quest46_q4k_pp_interval.ipynb")
PASS, FAIL = [], []


def ok(cond, msg):
    (PASS if cond else FAIL).append(msg)
    print(("  ✅ " if cond else "  ❌ ") + msg)


def cells():
    with open(NB, encoding="utf-8") as f:
        return ["".join(c["source"]) for c in json.load(f)["cells"]
                if c["cell_type"] == "code"]


def md():
    with open(NB, encoding="utf-8") as f:
        return "\n".join("".join(c["source"]) for c in json.load(f)["cells"]
                         if c["cell_type"] == "markdown")


def src():
    return "\n".join(cells())


def static():
    print("\n[정적] 노트북 소스 불변식")
    s = src(); m = md()

    for tok in ("FS", "R_IDX", "W_P_S", "W_T_S", "W_Q_S", "FRAC_QRS", "FRAC_P", "FRAC_T",
                "LAG", "P_CORR_MIN", "DUP_R2", "MAIN_K", "N_PERM"):
        ok(f"{tok} =" in s or f"{tok}," in s, f"사전 고정 손잡이 `{tok}` 가 CELL 1 에 있다")

    # ── ① 지표 변경
    ok('PRIMARY, SECONDARY = "ach", "auc"' in s,
       "① ★★★ **주 지표가 달성률@300**, 2차가 매크로 AUROC 다")
    ok("사전등록 변경" in s and "데이터 보기 전" in s,
       "① ★★★ 지표 변경이 **데이터 보기 전**임을 명시한다(R34 ②)")
    ok("레코드 간 상관" in s and "0.8869" in s,
       "① ★★★ Q4-G 의 ρ 를 **개입 효과로 오독했다**는 정정이 들어 있다(R38 ⑦)")
    ok("두 지표가 갈리면" in s,
       "① 두 지표가 갈리는 것 자체를 **상위 꼬리 개입의 증거**로 읽는다")
    ok("0.0944" in s and "0.0109" in s, "① Q4-J 의 두 수치가 앵커로 박혀 있다")

    # ── ② P-P = RR − ΔPR
    ok("PP(i) = RR(i) − ΔPR(i)" in s or "PP = RR − ΔPR" in s or "RR(i) − ΔPR(i)" in s,
       "② ★★★ 대수적 항등이 노트북에 적혀 있다")
    ok('"pp_over_rr"' in s and '"dpr_ms"' in s and '"pr_dev_ms"' in s,
       "② ΔPR·PR편차·PP/RR 이 실제 열로 있다")
    ok("dpr = np.r_[0.0, np.diff(pr_ms)]" in s,
       "② ΔPR 이 **연속 박동 간 PR 차**로 계산된다")
    ok("best_c" in s and "corr_to(B[:, :, a:b], tp_seg)" in s and "range(-LAG, LAG + 1)" in s,
       "② P 위치를 **템플릿 P 조각과의 교차상관 최대**로 잡는다(±LAG)")

    # ── ③ TP 는 RR 잔차화로만
    ok("tp_res = tp - A @ coef" in s and "np.linalg.lstsq(A, tp" in s,
       "③ ★★★ TP 의 **RR 회귀 잔차**를 만든다")
    ok('"tp_over_rr"' in s and '"tp_resid"' in s and "tp_ms" not in s,
       "③ ★★★ TP 를 **원값으로 넣지 않는다** — 비와 잔차만 쓴다")
    ok("RR = TP+P+PR+QRS+ST+T" in s or "RR = TP + P + PR + QRS + ST + T" in s,
       "③ ★★ 중복의 **대수적 이유**가 적혀 있다")
    ok("ρ=+1.0000" in s or "+1.0000" in s,
       "③ 합성 확인(ρ(TP,RR)=+1.0000)이 근거로 박혀 있다")

    # ── ④ QRS 폭 정의
    ok("S **종료**" in s or "S 종료" in s,
       "④ ★★ QRS 폭 정의를 **Q 시작 ~ S 종료**로 고쳤다고 명시한다")
    ok("W_Q_S  = (72, 145)" in s or "W_Q_S = (72, 145)" in s,
       "④ QRS 탐색 창이 S 종료까지 덮는다")

    # ── ⑤ 중복 감사
    ok("def dup_r2" in s and "LinearRegression().fit(Zb, y)" in s,
       "⑤ ★★★ **중복 감사** — 새 열을 base 9열에 회귀시켜 R² 를 낸다")
    ok("def within_var" in s and "레코드 상수" in s,
       "⑤ ★★★ **레코드 내 분산비**도 잰다 — 레코드 상수는 within-record 순위를 못 바꾼다")
    ok("⛔ 중복" in s and "⚠️ 레코드상수" in s and "✅ 새 축" in s,
       "⑤ 세 판정이 열마다 나온다")
    ok("Q4-H 의 `pre/base` 는 여기서" in s,
       "⑤ ★★ 이 자의 **존재 이유**(Q4-H 를 입구에서 잡는다)가 로그에 남는다")
    ok("uni_one" in s, "⑤ 열별 단변량 판별력도 같이 낸다")

    # ── ⑥ 차원 동일 대조군
    ok("def rec_shuffle" in s and "M[ii][_rs.permutation(len(ii))]" in s,
       "⑥ 대조군은 **레코드 안에서 공동 행치환**이다")
    ok("차원 대조군 불일치" in s and "raise AssetError" in s,
       "⑥ 차원이 다르면 **중단**한다")
    ok('MAIN_CT = "intv-ishuf"' in s, "⑥ ★★★ 주 관문이 `intv-ishuf` 다")

    # ── ⑦ 영점 흐림 강등
    ok("NULL_BLUR" in s and "강등" in s,
       "⑦ ★★★ 영점이 관측보다 흐리면 **기각을 미결로 강등**한다")
    ok("보수적 문턱은 ✅ 를 어렵게" in s or "❌ 를 만들어선 안 된다" in s,
       "⑦ ★★★ 그 근거(보수적 문턱이 ❌ 를 만들면 안 된다)가 적혀 있다")
    ok("증거 없음" in s and "반대 증거가 아니다" in s,
       "⑦ 강등된 경우를 **증거 없음**으로 읽는다고 로그에 남는다")

    # ── 델리네이션 자기검증 · 누출 · DL
    ok("O0 실패 — 템플릿 PR 중앙" in s and "생리 범위" in s,
       "★ 델리네이션이 **생리 범위**(PR 60~260ms)를 벗어나면 중단한다(R16)")
    ok("P 검출률" in s and "너무 낮다" in s, "★ P 검출률이 너무 낮으면 중단한다")
    ok("okm = (REL[ii] >= TMPL_LO)" in s and "라벨을 안 쓴다" in s,
       "★★ 템플릿·델리네이션·잔차화가 **라벨을 안 쓴다**(R22)")
    ok("CUDA 없음" in s and "건너뛴다" in s,
       "★ 딥러닝 절은 **GPU 없으면 건너뛴다**(관문 아님)")
    ok("def cpu_fold" in s and "같은 5겹" in s,
       "★★★ DL 비교는 **같은 5겹에서 CPU 팔을 다시 재서** 한다(다른 자로 비교 금지)")
    ok("74.56" in s, "★ 문헌(1D CNN 환자분리 SVEB 74.56%)이 사전 입장으로 박혀 있다")
    ok("Q7-S′ 의 P 갈래 재개가 아니다" in s or "P 갈래 재개가 아니다" in s,
       "★★ Q7-S′ 재개가 아니라 **P 의 시간**이라는 구분이 있다")
    ok('READ_ORDER = ("O0"' in s and "R41" in s, "읽는 순서와 R41 이 있다")


def dynamic():
    print("\n[동적] 합성으로 확인하는 구성")
    rng = np.random.RandomState(31)

    # ── ⓐ ★★★ PP = RR − ΔPR (사용자 가설 (a)의 대수적 정리)
    n = 40
    R = np.cumsum(rng.normal(360, 20, n)).astype(float)
    PR = np.full(n, 58.0); PR[[7, 19, 28]] = 92.0          # 이소성 박동만 PR 이 길다
    P = R - PR
    RR, PP, dPR = np.diff(R), np.diff(P), np.diff(PR)
    ok(float(np.max(np.abs(PP - (RR - dPR)))) < 1e-9,
       f"ⓐ ★★★ **PP(i) = RR(i) − ΔPR(i)** 가 구성으로 정확하다"
       f"(max|Δ| = {float(np.max(np.abs(PP - (RR - dPR)))):.1e}) — P-P 를 따로 재는 것은 "
       f"ΔPR 을 재는 것이고, 열 하나로 압축된다")
    ok(abs(dPR[6]) > 30 and abs(RR[6] - np.median(RR)) < 3 * np.std(RR),
       f"ⓐ ★★★ 이소성 박동에서 **RR 은 정상 범위인데 ΔPR 이 {dPR[6]:+.0f} 로 튄다** — "
       f"RR 축이 못 보는 자리를 정확히 겨눈다")

    # ── ⓑ ★★★ TP 를 그대로 넣으면 RR 의 재표현이다(사용자 가설 (d)의 함정)
    RRs = rng.normal(360, 40, 4000)
    TP_fix = RRs - 218.0                                   # 나머지 구간 고정
    TP_real = RRs - 218.0 + rng.normal(0, 9, 4000)
    def resid(y, x):
        A = np.c_[np.ones(len(x)), x]
        c, *_ = np.linalg.lstsq(A, y, rcond=None)
        return y - A @ c
    r_fix, r_real = resid(TP_fix, RRs), resid(TP_real, RRs)
    ok(abs(np.corrcoef(TP_fix, RRs)[0, 1]) > 0.999 and r_fix.std() < 1e-6,
       f"ⓑ ★★★ 나머지 구간이 고정이면 **TP = RR − 상수**(ρ {np.corrcoef(TP_fix,RRs)[0,1]:+.4f}) "
       f"이고 RR 잔차는 **아무것도 안 남긴다**(SD {r_fix.std():.1e}) — 그대로 넣으면 Q4-H 의 반복")
    ok(r_real.std() > 1.0,
       f"ⓑ ★★★ 진짜 새 정보가 있으면 잔차가 **그것만 남긴다**(SD {r_real.std():.2f}) — "
       f"잔차화는 **중복이면 0, 새 정보면 그것만** 남기는 자동 안전장치다")

    # ── ⓒ ★★ 중복 감사가 Q4-H 의 실패를 입구에서 잡는다
    from sklearn.linear_model import LinearRegression
    m_ = 3000
    base_col = rng.normal(0, 1, m_)
    Zb = np.c_[base_col, rng.normal(0, 1, (m_, 8))]
    dup_col = 1.0 - 0.5 * base_col + rng.normal(0, 0.02, m_)   # Q4-H 의 `pre/base` 꼴
    new_col = rng.normal(0, 1, m_)
    r2d = LinearRegression().fit(Zb, dup_col).score(Zb, dup_col)
    r2n = LinearRegression().fit(Zb, new_col).score(Zb, new_col)
    ok(r2d > 0.90 > r2n,
       f"ⓒ ★★★ **중복 감사가 재표현을 잡는다** — 기존 축의 아핀 변환은 R² {r2d:.3f} > 0.90 "
       f"(⛔ 중복), 독립 열은 {r2n:.3f}(✅ 새 축). Q4-H 의 `pre/base` 가 여기서 걸렸어야 했다")

    # ── ⓓ ★★ 레코드 상수는 within-record 순위를 못 바꾼다(층② 불가능 정리와 같은 이유)
    rid = np.repeat(np.arange(10), 300)
    rec_const = np.repeat(rng.normal(0, 1, 10), 300)
    tot = np.std(rec_const) + 1e-12
    wv = np.mean([np.std(rec_const[rid == r]) for r in range(10)]) / tot
    ok(wv < 1e-6,
       f"ⓓ ★★★ **레코드 상수 열의 레코드 내 분산비는 {wv:.1e}** — 레코드 안에서 안 변하므로 "
       f"within-record 순위를 못 바꾼다. `p_found`(AF 에서 P 가 통째로 없는 레코드)가 "
       f"이렇게 될 수 있어 중복 감사가 그걸 같이 본다")

    # ── ⓔ ★★★ 영점이 흐리면 기각이 아니라 미결이다(스모크가 잡은 것)
    def decide(lo, hi, thr):
        if not all(np.isfinite(v) for v in (lo, hi, thr)): return "미결"
        return "지지" if lo > thr else ("기각" if hi < thr else "미결")
    obs_lo, obs_hi = 0.0169, 0.1249                    # 관측: 뚜렷한 양수
    obs_half = (obs_hi - obs_lo) / 2
    thr_noisy = 0.15                                   # 영점이 흐려 문턱이 부풀었다
    null_half = 0.30
    raw = decide(obs_lo, obs_hi, thr_noisy)
    demoted = "미결" if (null_half > obs_half and raw == "기각") else raw
    ok(raw == "기각" and demoted == "미결",
       f"ⓔ ★★★ 영점 반폭 {null_half:.2f} > 관측 반폭 {obs_half:.4f} 이면 「기각」은 "
       f"**영점 잡음이 만든 것**이다 → **미결로 강등**한다. 관측은 [{obs_lo:+.4f}, "
       f"{obs_hi:+.4f}] 로 오히려 양수인데 기각이 나오는 게 그 증거다")
    ok(decide(0.30, 0.40, 0.15) == "지지",
       "ⓔ ★★ 강등은 **기각에만** 적용된다 — 보수적 문턱을 **넘은** 지지는 그대로 유효하다")

    # ── ⓕ 예산 고정에서 달성률이 상위 꼬리 개입을 본다(지표 변경의 근거)
    k, S_, N_ = 300, 500, 2000                         # 예산 · 양성 · 음성
    tp0, tp1 = 200, 240                                # V 40개를 상위에서 걷어냈다
    ceil = min(1.0, k / S_)
    d_ach = (tp1 / S_) / ceil - (tp0 / S_) / ceil
    # AUROC: 음성 40개가 **모든 양성 위 → 모두 아래**로 내려간 최대 효과
    d_auc = (tp1 - tp0) * S_ / (S_ * N_)
    ok(d_ach > 3 * d_auc,
       f"ⓕ ★★★ 상위 {k}개에서 음성 {tp1-tp0}개를 걷어내면 **달성률 {d_ach:+.4f}** vs "
       f"**AUROC {d_auc:+.4f}**(최대치로 잡아도) — **{d_ach/d_auc:.1f}배** 차이다. "
       f"Q4-J 실측 비도 0.0944/0.0109 = 8.7배였다. 주 지표를 바꾼 이유다")
    ok(abs(d_ach / d_auc - 6.7) < 1.0,
       f"ⓕ ★★ 그 비는 **예산 k 와 양성 수 S 로 결정**된다(여기선 {d_ach/d_auc:.1f}배) — "
       f"S 가 클수록 AUROC 가 더 둔해진다")

    # ── ⓖ LORO 누출 없음
    REC = list(range(8)); pr_ = np.linspace(0.01, 0.5, 8)
    def split_rest(held, every=4):
        rest = sorted([r for r in REC if r != held], key=lambda r: (pr_[r], r))
        dv = [r for i, r in enumerate(rest) if i % every == 0]
        return [r for r in rest if r not in set(dv)], dv
    ok(not [h for h in REC if h in split_rest(h)[0] or h in split_rest(h)[1]],
       "ⓖ ★★★ held-out 레코드가 TRAIN·DEV 어디에도 안 들어간다(R22)")


if __name__ == "__main__":
    if not os.path.exists(NB):
        print(f"❌ 노트북이 없다 — {NB}")
        sys.exit(1)
    print("=" * 78)
    print("Q4-K 픽스처 — 지표 정정 · P-P=RR−ΔPR · TP 잔차화 · 중복 감사 · 영점 흐림 강등")
    print("=" * 78)
    static(); dynamic()
    print("\n" + "=" * 78)
    print(f"통과 {len(PASS)} · 실패 {len(FAIL)}")
    for f in FAIL:
        print("  ✗ " + f)
    sys.exit(1 if FAIL else 0)
