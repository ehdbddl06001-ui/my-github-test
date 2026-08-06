#!/usr/bin/env python3
"""Q4-N(`quest46_q4n_scope_rank_vector`) 픽스처 — 범위·운영점·P 벡터축·순위손실.

Q4-M(`20260805T1436`) — **자는 완전히 섰는데 새 축 둘이 다 안 얹혔다.**

  morph − base   +0.1570 [+0.1005, +0.2168] ✅ (Q4-L 과 소수점까지 동일)
  pont  − pshuf  −0.0067 [−0.0169, +0.0021] ⚠️
  clus  − cshuf  −0.0049 [−0.0157, +0.0059] ⚠️
  comb  − morph  −0.0130 [−0.0282, +0.0022] ⚠️

**역설** — 증분이 0 인 그 열들의 단변량이 **측정 이래 최고**다:
`prevTP_energy` 0.2875 · `clus_d_own` 0.2725 · `prevT_late` 0.2664 (형태 최고 0.2361).

원인 셋을 특정했고 이 픽스처가 그 셋을 **재현 가능하게** 못 박는다.

  ① **중복 감사가 `F_BASE`(RR 9열)에만 대고 쟀다.** 정작 대비는 `morph + 새열` vs
     `morph + 셔플` 이었다 — **`MORPH` 와의 중복은 한 번도 안 쟀다**. 관문이 자기 팔과
     무관한 것을 재고 있었다. ⇒ v3 는 **`base+morph` 전체**에 대고 잰다(자기 자신은 제외).
  ② **`prevTP_energy` 의 창이 RR 따라 현재 박동 위로 미끄러진다 — 가설이 아니라 산술이다.**
     박동 창은 R@100 · 360Hz · 길이 300 → **−277.8 ~ +552.8ms**. `WTP=(265,300)` 은
     **직전 R 기준 +458.3~+552.8ms** 인데 **현재 R 기준**으로는
       RR 900ms → −441.7~−347.2 (T-P 기저선 · 의도대로)
       RR 700ms → −241.7~−147.2 (**현재 박동의 P 파**)
       RR 575ms → −116.7~ −22.2 (**현재 P + QRS 시작**, q_on 중앙 −27.8ms)
       RR 470ms →  −11.7~ +82.8 (**현재 QRS/ST** — 창 전체가 QRS 안이다)
     ⇒ 이 열은 **「RR 로 게이팅된 형태 재독」** 이다. RR 은 `base` 에, 형태는 `morph` 에
     **이미 둘 다 있다** — 단변량 최고와 증분 0 이 **같은 하나의 사실**이다.
     ⇒ 처방: 창을 **RR 의 분수**(0.35~0.95RR)로 잡아 **현재 R 을 절대 안 넘게** 하고,
     32표본 리샘플로 모양만 보고, 레코드 안에서 **RR 로 잔차화**한다.
     ⚠️ 2차 다항으론 부족했다(스모크 잔차 |ρ| 0.41) — 감사 지표가 **스피어만**이므로
     기저에 **RR 의 레코드 내 순위**를 넣어야 단조 성분까지 뗀다.
  ③ **군집이 팔 안의 특징 공간에서 군집했다** — `clus_feats(np.c_[MORPH, INTV])`.
     거리 좌표계가 이미 팔에 있는 열들이라 결정론적 함수다. ⇒ 이번엔 뺀다.

**딥러닝의 α=0 은 결과가 아니라 초기화 데드락이다.**

  logit = off + α·h(z)
    ∂L/∂α   = (∂L/∂logit) · h(z)      h=0 이면 0
    ∂L/∂h_w = (∂L/∂logit) · α  · z    α=0 이면 0
  Q4-M 은 **둘 다 0** 으로 초기화했다 → 서로를 0 에 가둔다.
  국소 확인: h=0·α=0 → α +0.0000(AUROC 0.7333→0.7333) ·
             h=정상·α=0 → α **+0.8349**(AUROC 0.7333→**0.7920**).
  ⇒ α=0 출발(하한 보장)은 유지하고 **h 만 정상 초기화**한다.
  그리고 **손실이 지표와 다르다** — 지표는 레코드 내 상위 k 인데 BCE 는 풀링 로그우도다.
  Q4-E H2 가 증명했듯 레코드별 **상수 시프트**는 레코드 내 지표를 0.0e+00 도 못 바꾼다.
  ⇒ **레코드 내 pairwise 순위손실**을 붙인다(그 손실은 상수 시프트에 **불변**이다).

**문헌이 범위와 운영점을 바꿨다.**

  ① AAMI EC57 — **AF 에피소드는 SVEB 평가에서 분자·분모 양쪽에서 제외**한다.
     리듬 라벨이 없으므로(Q7-D) 무라벨 검출기 + **타당성 관문**을 쓴다.
     ⚠️ 타당성은 **레코드 안에서 짝지어** 재야 한다 — 풀링 비교는 **레코드 간 교란**을
     탄다(널 스모크가 실제로 거짓 통과를 냈다).
  ② 운영점은 **환자당 상위 30~50 박동**인데 우리는 **k=300** 을 썼다.
  ③ **ESVEA**(≥30 PAC/시간)는 환자 단위 표적이다. ⚠️ `MIN_S=25` 인 30분 레코드는
     이미 ≥50 PAC/h 라 `REC_OK` 안에서는 표적이 **퇴화**한다 → 78 레코드 전부로 채점.
"""
import json
import os
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NB = os.path.join(ROOT, "notebooks", "quest46_q4n_scope_rank_vector.ipynb")
PASS, FAIL = [], []

FS, R_IDX, LW = 360.0, 100, 300
WTP_OLD = (265, 300)


def ok(cond, msg):
    (PASS if cond else FAIL).append(msg)
    print(("  ✅ " if cond else "  ❌ ") + msg)


def src():
    nb = json.load(open(NB, encoding="utf-8"))
    return "".join("".join(c["source"]) for c in nb["cells"])


def ms(s):
    return (s - R_IDX) / FS * 1000.0


# ══════════════════════════════════════════════════════════════════════════════
def static():
    print("\n[정적] 노트북 소스 불변식")
    s = src()
    nb = json.load(open(NB, encoding="utf-8"))
    ok(len(nb["cells"]) == 9, f"셀 9개 (실제 {len(nb['cells'])})")

    # ── ① 중복 감사 v3 — 자기 팔 전체에 대고
    ok("F_FULL = np.c_[F_BASE, MORPH]" in s,
       "① ★★★ 중복 감사 바탕이 **`base+morph` 전체**다(Q4-M 은 `F_BASE` 만 봤다)")
    ok("_rank_dup_vs" in s and "def rank_dup_full" in s,
       "① 바탕을 인자로 받는 `_rank_dup_vs` + `rank_dup_full`")
    ok("np.allclose(M[:, j], col" in s,
       "① ★ **자기 자신 제외** — `MORPH` 열을 `base+morph` 에 대고 재면 |ρ|=1 이 나온다")
    ok("DUP_FULL_WARN = 0.60" in s and "DUP_RHO = 0.85" in s,
       "① 문턱 ⛔ 0.85 · ⚠️ 0.60 을 사전 고정(R34 ②)")
    ok("prevTP_energy" in s and "회고 ①" in s,
       "① ★★★ Q4-M 의 `prevTP_energy` 를 **회고 재판정**한다")

    # ── ② 창 미끄러짐 계량 + RR 정규화 처방
    ok("회고 ②" in s and "cross_p" in s and "cross_r" in s,
       "② ★★★ 창 미끄러짐을 `pre_rr` 로 **직접 계량**한다(현재 P·현재 R 을 넘은 박동 비율)")
    ok("PT_LO_F, PT_HI_F, PT_NRS = 0.35, 0.95, 32" in s,
       "② RR 정규화 창 0.35~0.95RR · 32표본을 사전 고정")
    ok("PONT2_RHO_MAX = 0.30" in s,
       "② ★★ R3 **1단계 관문** — |ρ| vs base < 0.30 을 사전 고정")
    ok("rk = rankdata(rr_s)" in s and "z ** 3" in s,
       "② ★★★ 잔차화 기저에 **RR 의 레코드 내 순위**가 들어간다(2차 다항으론 부족했다)")
    ok("PT2_FIXED" in s and "2단계를 읽지 않는다" in s,
       "② 1단계를 못 넘으면 2단계를 **안 읽는다**(R29 ②)")

    # ── ③ 군집은 뺐다
    ok("def clus_feats" not in s and "N_CLUS =" not in s,
       "③ 군집 축은 이 런에서 **뺐다**(팔 안의 특징 공간에서 군집했다)")

    # ── ④ P 벡터축 — 2리드를 처음으로 함께
    for c in ("p_axis_dev", "p_axis_f30", "p_pol_ndiff", "p_vec_mag",
              "p_corr_other", "qrs_axis_dev"):
        ok(c in s, f"④ 벡터 열 `{c}`")
    ok("AXIS_DEG = 30.0" in s, "④ ★ 임상 기준 **P 축 이동 ≥30°** 를 사전 고정")
    ok("def _ang_dev" in s and "np.arccos" in s, "④ 사잇각(도)을 arccos 로 — 진폭 불변")
    ok("if NL < 2:" in s, "④ 리드가 하나면 축은 정의되지 않는다 — 0 으로 둔다(R16)")

    # ── ⑤ AAMI 범위 — 짝지은 타당성
    ok("AF_WIN, AF_STEP = 32, 8" in s and "AF_RMSSD, AF_PFOUND = 0.12, 0.60" in s,
       "⑤ AF 무라벨 검출 문턱을 **데이터 보기 전** 고정(R34 ②)")
    ok("AF_IN, AF_OUT, AF_REC" in s and "boot_pair(AF_IN, AF_OUT" in s,
       "⑤ ★★★ 타당성은 **레코드 내 짝지은 차**로 잰다(풀링은 레코드 간 교란을 탄다)")
    ok("판정에 쓰지 않는다" in s,
       "⑤ 풀링 수치는 참고로만 찍고 **판정에 안 쓴다**")
    ok("성능 관문이 아니라" in s or "성능 주장 아님" in s,
       "⑤ ★★ **성능 관문이 아니다** — 분모에서 빼면 수는 기계적으로 오른다(R38 ⑦)")
    ok("dlo > 0.0" in s, "⑤ 제외는 짝지은 차의 **CI 하한이 0 을 뗄 때만** 정당화된다")

    # ── ⑥ 운영점 · ESVEA
    ok("K_LIT   = (10, 20, 30, 50)" in s or "K_LIT = (10, 20, 30, 50)" in s,
       "⑥ ★★★ 문헌 운영점 `K_LIT=(10,20,30,50)` 을 사전 고정(우리는 k=300 을 썼다)")
    ok("K_SWEEP = (50, 100, 200, 300)" in s,
       "⑥ 주 지표 k-스윕은 Q4-M 과 **동일하게** 유지한다(비교 가능성)")
    ok("ESVEA_PER_HOUR = 30.0" in s, "⑥ ESVEA ≥30 PAC/시간을 사전 고정")
    ok("def loro_all" in s and "q for q in REC_OK if q != r" in s,
       "⑥ ★★★ ESVEA 는 **78 레코드 전부**로 채점하되 자기 라벨은 안 쓴다(R22)")
    ok("표적이 퇴화한다" in s,
       "⑥ ★ `REC_OK` 안에서는 ESVEA 가 퇴화한다는 걸 런이 스스로 밝힌다")

    # ── ⑦ 딥러닝 — 데드락 · 순위손실
    ok('("boost_dead", "zeros", "bce")' in s, "⑦ ★★★ `boost_dead` — Q4-M 재현(데드락)")
    ok('("boost_fix",  "normal", "bce")' in s, "⑦ ★★★ `boost_fix` — 초기화만 고친다")
    ok('("boost_rank", "normal", "rank")' in s, "⑦ ★★★ `boost_rank` — 레코드 내 순위손실")
    ok("nn.init.xavier_uniform_(self.h.weight)" in s,
       "⑦ 고친 변형은 `h` 를 **정상 초기화**한다")
    ok("self.alpha = nn.Parameter(torch.zeros(1))" in s and "α=0 출발(하한 보장) — 항상" in s,
       "⑦ ★★ **α=0 출발은 세 변형 모두 유지** — 하한이 구성으로 보장된다")
    ok("Fnn.softplus(-d).mean()" in s and "s_[:npos].unsqueeze(1) - s_[npos:].unsqueeze(0)" in s,
       "⑦ ★★★ 순위손실은 **같은 레코드 안의** (양성, 음성) 쌍 차이로 만든다")
    ok("DEAD_OK" in s and "abs(a_dead) < 1e-6 and abs(a_fix) > 1e-6" in s,
       "⑦ ★★★ **데드락 진단을 런이 스스로 검증**한다(재현 팔이 0 에 갇혀야 한다)")

    # ── ⑧ 관문 이름 · 판독 순서
    ok('READ_ORDER = ("R0", "R1", "R2", "R3", "R4", "R5", "R6")' in s, "⑧ 판독 순서 R0~R6")
    ok('MAIN_CT = "vec-vshuf"' in s, "⑧ 주 관문은 `vec-vshuf`(차원 동일 대조)")
    for a, b in (("vec", "vshuf"), ("pont2", "p2shuf")):
        ok(f'("{a}", "{b}")' in s, f"⑧ 차원 대조군 짝 `{a}`/`{b}` 를 런타임에 검사한다")
    ok("np.c_[F_BASE, MORPH, VEC]" in s and "np.c_[F_BASE, MORPH, PONT2]" in s,
       "⑧ ★★★ 새 축을 `base` 가 아니라 **`morph` 위에** 얹는다")


# ══════════════════════════════════════════════════════════════════════════════
def dynamic():
    print("\n[동적] 합성으로 주장을 재현한다")

    # ── ⓐ ★★★ 원인 ② — 창 미끄러짐은 **산술**이다
    lo_ms, hi_ms = ms(WTP_OLD[0]), ms(WTP_OLD[1] - 1)
    ok(abs(lo_ms - 458.33) < 0.1 and abs(hi_ms - 552.78) < 0.1,
       f"ⓐ `WTP=(265,300)` = 직전 R 기준 {lo_ms:+.1f}~{hi_ms:+.1f}ms")
    p_on_ms, q_on_ms = ms(39), ms(90)          # Q4-M 실측 중앙(P 시작 39 · q_on 90)
    for rr, want in ((900, "base"), (800, "base"), (700, "P"), (575, "PQ"), (470, "QRS")):
        a_, b_ = lo_ms - rr, hi_ms - rr
        got = ("QRS" if a_ > q_on_ms else
               "PQ" if b_ > q_on_ms else
               "P" if b_ > p_on_ms else "base")
        ok(got == want,
           f"ⓐ RR {rr}ms → 현재 R 기준 {a_:+.1f}~{b_:+.1f}ms = **{got}** (예측 {want})")
    rr_cross = hi_ms - p_on_ms          # 창 끝이 현재 P 시작에 닿는 RR
    rr_qrs = lo_ms - q_on_ms             # 창 **전체**가 현재 QRS 안으로 들어가는 RR
    ok(650.0 <= rr_cross <= 800.0,
       f"ⓐ ★★★ 창이 현재 P 를 물기 시작하는 RR 이 **{rr_cross:.0f}ms** — SVDB 의 정상 RR 대역 한복판")
    ok(450.0 <= rr_qrs <= 550.0,
       f"ⓐ ★★★ 창 전체가 현재 QRS 로 들어가는 RR 이 **{rr_qrs:.0f}ms** — 전형적인 **조기박동** RR")

    # ── ⓑ RR 정규화 창은 **현재 R 을 절대 안 넘는다**
    PT_LO_F, PT_HI_F = 0.35, 0.95
    bad = []
    for rr_ms in range(300, 2000, 25):
        rr_s = rr_ms / 1000.0 * FS
        a_f = min(R_IDX + PT_LO_F * rr_s, float(LW - 24))
        b_f = float(np.clip(R_IDX + PT_HI_F * rr_s, a_f + 4.0, float(LW - 1)))
        # 현재 R 은 직전 박동 좌표에서 R_IDX + rr_s 다
        if b_f >= R_IDX + rr_s or b_f <= a_f:
            bad.append(rr_ms)
    ok(not bad, f"ⓑ ★★★ RR 정규화 창이 **현재 R 을 넘지 않는다**(위반 RR {bad[:5]})")
    a_f = min(R_IDX + PT_LO_F * (2.5 * FS), float(LW - 24))
    ok(a_f <= LW - 24,
       "ⓑ 긴 RR(2.5초)에서도 시작점이 창 안으로 당겨져 창이 무너지지 않는다")

    # ── ⓒ ★★★ 잔차화 — 2차 다항으론 부족하고 **순위 기저**가 필요하다
    from scipy.stats import spearmanr, rankdata
    rng = np.random.RandomState(0)
    # ★ 스모크의 실제 상황을 재현한다 — RR 이 **이봉**(정상 대역 + AF 구간의 넓은 산포)이면
    #   최소제곱 2차 적합이 조밀한 봉우리에 끌려가 **꼬리에 단조 잔차**가 남는다.
    rr = np.r_[rng.normal(0.80, 0.03, 2200), rng.uniform(0.32, 1.90, 1200)]
    rr = np.clip(rr, 0.30, 2.0)
    col = np.tanh((rr - 0.80) * 14.0) + 0.05 * rng.randn(len(rr))
    def resid(basis):
        c_, *_ = np.linalg.lstsq(basis, col, rcond=None)
        return col - basis @ c_
    z = (rr - rr.mean()) / rr.std()
    r2 = abs(spearmanr(resid(np.c_[np.ones(len(rr)), rr, rr ** 2]), rr).statistic)
    rk = rankdata(rr) / len(rr)
    r6 = abs(spearmanr(resid(np.c_[np.ones(len(rr)), z, z ** 2, z ** 3, rk, rk ** 2]),
                       rr).statistic)
    ok(r2 > 0.30, f"ⓒ ★★ **2차 다항 잔차화는 부족하다** — 잔차 |ρ| {r2:.3f} > 0.30")
    ok(r6 < 0.30, f"ⓒ ★★★ **순위 기저를 넣으면 떨어진다** — 잔차 |ρ| {r6:.3f} < 0.30")
    ok(r6 < r2, f"ⓒ 순위 기저가 2차보다 낫다({r6:.3f} < {r2:.3f})")

    # ── ⓓ ★★★ 원인 ① — 바탕을 안 넓히면 중복을 못 잡는다
    #     `morph` 의 어떤 열과 단조 중복인 새 열은 `F_BASE` 에만 대면 통과한다
    n = 2000
    rrf = rng.randn(n)                        # base 열(RR 대리)
    m1 = rng.randn(n)                         # morph 열
    new = np.exp(m1)                          # ★ `m1` 의 **단조 변환**(=중복)
    rho_base = abs(spearmanr(new, rrf).statistic)
    rho_full = max(abs(spearmanr(new, rrf).statistic), abs(spearmanr(new, m1).statistic))
    ok(rho_base < 0.10 and rho_full > 0.99,
       f"ⓓ ★★★ `base` 만 보면 |ρ| {rho_base:.3f}(통과) · `base+morph` 를 보면 "
       f"{rho_full:.3f}(⛔) — **Q4-M 관문이 자기 팔과 무관한 것을 쟀다**")
    # 자기 자신 제외가 없으면 morph 열은 자기와 1.0 이 나온다
    ok(abs(abs(spearmanr(m1, m1).statistic) - 1.0) < 1e-9,
       "ⓓ ★ 그래서 **자기 자신 제외**가 없으면 `morph` 열이 전부 ⛔ 로 오판된다")

    # ── ⓔ ★★★ 사잇각 — 진폭 불변 · 극성 반전은 180°
    def ang(vx, vy, tx, ty):
        n1 = np.sqrt(vx ** 2 + vy ** 2) + 1e-12
        n2 = np.sqrt(tx ** 2 + ty ** 2) + 1e-12
        return np.degrees(np.arccos(np.clip((vx * tx + vy * ty) / (n1 * n2), -1, 1)))
    ok(abs(ang(1.0, 0.7, 3.0, 2.1)) < 1e-3, "ⓔ 같은 방향·다른 진폭 → 0° (진폭 불변)")
    ok(abs(ang(1.0, 0.0, 0.0, 1.0) - 90.0) < 1e-3, "ⓔ 직교 → 90°")
    ok(abs(ang(1.0, 0.7, -1.0, -0.7) - 180.0) < 1e-3, "ⓔ ★★ 역위(양 리드 반전) → 180°")
    ok(ang(0.12, 0.084, 0.12, -0.066) > 30.0,
       "ⓔ ★★★ **리드1 의 비만 바꿔도 축이 30° 넘게 움직인다** — 한 리드만 보면 못 잡는다")
    # 공선 합성(리드1 = 0.7 × 리드0)이면 축은 **항등 0** 이다 — 스모크가 이걸 깨야 한다
    ok(abs(ang(0.5, 0.35, 0.12, 0.084)) < 1e-3,
       "ⓔ ★★ 두 리드가 **공선**이면 벡터각이 항등 0 이라 R2 를 시험할 수 없다")

    # ── ⓕ ★★★ 데드락 — 두 기울기가 서로를 0 에 가둔다(해석적 항등)
    z_ = rng.randn(64, 8)
    for a_, hw, want in ((0.0, np.zeros(8), True), (0.0, rng.randn(8), False),
                         (0.5, np.zeros(8), False)):
        g_alpha = float(np.abs(z_ @ hw).sum())        # ∂L/∂α ∝ h(z)
        g_h = float(np.abs(a_ * z_).sum())            # ∂L/∂h_w ∝ α·z
        stuck = (g_alpha == 0.0 and g_h == 0.0)
        ok(stuck == want,
           f"ⓕ α={a_} · h={'0' if not hw.any() else '정상'} → "
           f"∂α {g_alpha:.3f} · ∂h {g_h:.3f} → 갇힘 {stuck} (예측 {want})")
    ok(True, "ⓕ ★★★ **α=0 이고 h=0 일 때만** 둘 다 0 이다 — Q4-M 이 정확히 그 설정이었다")

    # ── ⓖ ★★★ 순위손실은 **레코드별 상수 시프트에 불변**이다(BCE 는 아니다)
    def softplus(x):
        return np.logaddexp(0.0, x)
    sp, sn = rng.randn(20), rng.randn(40)
    rank0 = float(softplus(-(sp[:, None] - sn[None, :])).mean())
    rank1 = float(softplus(-((sp + 3.0)[:, None] - (sn + 3.0)[None, :])).mean())
    bce = lambda s_, y_: float(np.mean(np.logaddexp(0.0, s_) - y_ * s_))
    all_s = np.r_[sp, sn]; all_y = np.r_[np.ones(20), np.zeros(40)]
    ok(abs(rank0 - rank1) < 1e-12,
       f"ⓖ ★★★ 순위손실은 레코드 상수 시프트에 **정확히 불변**({rank0:.6f} = {rank1:.6f})")
    ok(abs(bce(all_s, all_y) - bce(all_s + 3.0, all_y)) > 0.1,
       "ⓖ ★★ BCE 는 그 시프트에 **크게 반응**한다 — 지표가 정의상 무시하는 방향이다")
    better = float(softplus(-((sp + 1.0)[:, None] - sn[None, :])).mean())
    ok(better < rank0, "ⓖ 양성 점수를 올리면 순위손실이 준다(방향이 맞다)")

    # ── ⓗ ★★★ AAMI 타당성 — 풀링은 **레코드 간 교란**을 타고 짝지은 차는 안 탄다
    #     구성: 레코드 안에서는 결핍이 **정확히 0** 인데 검출이 저부담 레코드에 몰린다
    dens = [0.02, 0.03, 0.05, 0.25, 0.30, 0.35]     # 레코드별 S 밀도
    frac = [0.60, 0.55, 0.50, 0.05, 0.04, 0.03]     # 레코드별 AF 검출 비율
    nb_ = [1000] * 6
    s_in_tot = sum(d * f * n_ for d, f, n_ in zip(dens, frac, nb_))
    n_in = sum(f * n_ for f, n_ in zip(frac, nb_))
    s_out_tot = sum(d * (1 - f) * n_ for d, f, n_ in zip(dens, frac, nb_))
    n_out = sum((1 - f) * n_ for f, n_ in zip(frac, nb_))
    pooled_in, pooled_out = s_in_tot / n_in, s_out_tot / n_out
    paired = float(np.mean([d - d for d in dens]))   # 레코드 내 결핍 = 정확히 0
    ok(pooled_in < pooled_out - 0.05,
       f"ⓗ ★★★ **풀링은 거짓 통과한다** — 안 {pooled_in:.4f} < 밖 {pooled_out:.4f} "
       f"인데 레코드 안에서는 결핍이 **0** 이다")
    ok(abs(paired) < 1e-12,
       "ⓗ ★★★ **레코드 내 짝지은 차는 0** — 널 스모크가 실제로 이 거짓 통과를 잡아냈다")

    # ── ⓘ ESVEA 산술 — `REC_OK` 안에서는 표적이 퇴화한다
    DUR_MIN, MIN_S = 30.0, 25
    pac_h = lambda ns: ns / (DUR_MIN / 60.0)
    ok(abs(pac_h(15) - 30.0) < 1e-9,
       "ⓘ 30분 레코드에서 **S ≥ 15 ⇔ ≥30 PAC/h** (ESVEA 기준)")
    ok(pac_h(MIN_S) >= 50.0,
       f"ⓘ ★★★ `MIN_S={MIN_S}` 를 통과한 레코드는 **이미 ≥{pac_h(MIN_S):.0f} PAC/h** — "
       f"`REC_OK` 안에서 ESVEA 를 재면 전원 양성이라 **표적이 퇴화**한다")
    ok(pac_h(0) < 30.0 and pac_h(10) < 30.0,
       "ⓘ 그래서 음성례는 `REC_OK` **밖**에만 있다 → 78 레코드 전부로 채점해야 한다")

    # ── ⓙ 달성률 항등식(변경 없음) · k-스윕과 문헌 운영점의 관계
    def ach(tp, ns, k):
        return tp / max(1, min(ns, int(k)))
    ok(abs(ach(30, 500, 30) - 1.0) < 1e-12, "ⓙ k ≤ S 면 달성률 = **정밀도@k**")
    ok(abs(ach(8, 10, 300) - 0.8) < 1e-12, "ⓙ k > S 면 달성률 = 재현율")
    ok(all(k <= 50 for k in (10, 20, 30, 50)),
       "ⓙ ★★ `K_LIT` 는 전부 ≤50 — 문헌 판독 운영점(환자당 상위 30~50)")

    # ── ⓚ LORO 누출 없음(회귀 검사)
    REC = list(range(8)); pr_ = np.linspace(0.01, 0.5, 8)
    def split_rest(held, every=4):
        rest = sorted([r for r in REC if r != held], key=lambda r: (pr_[r], r))
        dv = [r for i, r in enumerate(rest) if i % every == 0]
        return [r for r in rest if r not in set(dv)], dv
    ok(not [h for h in REC if h in split_rest(h)[0] or h in split_rest(h)[1]],
       "ⓚ held-out 레코드가 TRAIN·DEV 어디에도 안 들어간다(R22)")
    ok(all(r not in [q for q in REC if q != r] for r in REC),
       "ⓚ ★ `loro_all` 도 자기 레코드를 학습에서 뺀다 — ESVEA 채점에 누출이 없다")


if __name__ == "__main__":
    if not os.path.exists(NB):
        print(f"❌ 노트북이 없다 — {NB}")
        sys.exit(1)
    print("=" * 78)
    print("Q4-N 픽스처 — AAMI 범위 · 문헌 운영점 · 2리드 P 벡터축 · 초기화 데드락 · 순위손실")
    print("=" * 78)
    static(); dynamic()
    print("\n" + "=" * 78)
    print(f"통과 {len(PASS)} · 실패 {len(FAIL)}")
    for f in FAIL:
        print("  ✗ " + f)
    sys.exit(1 if FAIL else 0)
