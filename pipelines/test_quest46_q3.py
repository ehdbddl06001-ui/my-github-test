#!/usr/bin/env python3
"""Q3(`quest46_q3_prior_em`) 픽스처 — 무라벨 EM 사전확률 보정(층② 눈금).

사전등록 관문 C0~C7 은 이미 확정돼 있다. 이 픽스처가 지키는 건 **빠뜨리면 런이 무효인 셋**이다:
  ① **C2(오라클 사전확률 팔)를 C3 보다 먼저 읽는** 판정 순서 — C2 ❌ 면 회복률(비)을 안 읽는다
  ② 기저 모델 보정을 **DEV 에서만** 적합 — EM 은 보정된 사후확률을 전제한다
  ③ 매크로는 판정 지표가 아니라 **항등 대조** — 보정이 레코드 내 순위를 보존하므로

동적 검사는 합성 데이터로 **절차가 옳게 움직이는지**를 본다. 특히:
  · 상수 로짓 시프트가 레코드 내 순위를 **부동소수점에서도 정확히** 보존하는가(확률공간 구현과 대조)
  · 보정 안 된 사후확률에서 EM 이 무너지는가(→ DEV 보정이 전제인 이유)
  · **오라클 팔이 정보 없는 기저에서도 이득을 내는가**(→ 영점이 필수인 이유)
  · 부담순 배분에 **덩어리 패턴**을 쓰면 유병률이 블록으로 갈리는가(스모크가 잡은 버그의 회귀)
"""
import json
import os
import re
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NB = os.path.join(ROOT, "notebooks", "quest46_q3_prior_em.ipynb")

PASS, FAIL = [], []


def ok(cond, msg):
    (PASS if cond else FAIL).append(msg)
    print(("  ✅ " if cond else "  ❌ ") + msg)


def cells():
    with open(NB, encoding="utf-8") as f:
        nb = json.load(f)
    return ["".join(c["source"]) for c in nb["cells"] if c["cell_type"] == "code"]


def src():
    return "\n".join(cells())


# ══════════════════════════════════════════════════════════════════ 정적
def static():
    print("\n[정적] 노트북 소스 불변식")
    s = src()
    cs = cells()

    # ① ★★★ 판정 순서 — C2 를 C3 보다 먼저 읽는다
    ok("C3 보다 먼저 읽는다" in s,
       "① ★★★ **C2 를 C3 보다 먼저 읽는다**가 소스에 박혀 있다")
    ok("READ_ORDER" in s and '"C2", "C3"' in s,
       "① 판정을 **읽는 순서**가 `READ_ORDER` 로 사전등록돼 있다")
    ok("GATE_DEP" in s and '"C3": ["C0", "C1", "C2"]' in s,
       "① ★ 관문 **의존 그래프**가 있다 — C3 은 C2 에 의존한다(R35 ①)")
    ok("RATIO_READ" in s and 'VERD.get("C2", "").startswith("✅")' in s,
       "① ★★★ 회복률을 읽을지가 **C2 의 판정에 게이팅**돼 있다")
    ok("회복률 미판독" in s and "비를 읽지 않는다" in s,
       "① ★★ C2 가 통과 못 하면 회복률을 **미판독**으로 남긴다")
    ok("C3_OK = c3_abs.startswith(\"✅\") and c3_ratio and RATIO_READ" in s,
       "① ★ C3 통과 조건에 `RATIO_READ` 가 **곱해져** 있다 — 순서가 판정의 일부다")
    # C2 가 C3 보다 **먼저 실행**되는 셀에 있어야 한다
    i2 = next((i for i, c in enumerate(cs) if "C2 — 오라클 이득" in c), -1)
    i3 = next((i for i, c in enumerate(cs) if "절대 ΔPR-AUC(EM − raw)" in c), -1)
    ok(0 <= i2 < i3,
       f"① ★★ C2 가 C3 **앞 셀**에서 계산된다(C2 셀 {i2} < C3 셀 {i3}) — 순서가 코드 구조로 강제된다")

    # ② ★★★ 기저 보정은 DEV 에서만
    ok("DEV 에서만" in s,
       "② ★★★ 「보정은 **DEV 에서만**」이 소스에 박혀 있다")
    ok("EM 은 보정된 사후확률을 전제" in s,
       "② ★ **왜** DEV 보정이 필요한지가 적혀 있다 — EM 은 보정된 사후확률을 전제한다")
    ok("(SC_dev, TT[DV_I])" in s,
       "② 최종 보정기가 **DEV 에서** 적합된다")
    ok("fit(SC_te" not in s and "SC_te, TT[TE_I]" not in s and "(SC_te, Y_te)" not in s,
       "② ★★ **TEST 로 보정기를 적합하지 않는다** — 소스에 그런 호출이 없다")
    ok("DV_FIT_R, DV_SEL_R" in s and "DEV 반쪽" in s,
       "② ★ 보정기 **선택**도 DEV 반쪽에서 한다(R22 · R36 ②)")
    ok("PI_TR = float(TT[DV_I].mean())" in s,
       "② ★★ `π_tr` 이 **DEV 유병률**이다 — 보정기를 DEV 에서 적합했으므로 기준이 거기다")
    ok("EM 하이퍼" in s and "PI_STAR_DEV" in s and "TEST 를 안 봤다" in s,
       "② ★ EM 하이퍼도 **DEV 에서 고정**한다 — 보고할 지표로 고르면 누출")
    ok("구성상 0 에 가깝다" in s and "증거로 쓰지 않는다" in s,
       "② ★ DEV **자기적합** ECE 를 보정도의 증거로 쓰지 않는다고 못 박는다(R38 ⑦)")

    # ③ ★★★ 매크로는 항등 대조
    ok("매크로는 판정 지표가 아니라" in s and "항등 대조" in s,
       "③ ★★★ **매크로 = 항등 대조**가 소스에 박혀 있다(판정 지표가 아니다)")
    ok('MACRO_ROLE = "identity_control"' in s,
       "③ 매크로의 역할이 **사전등록 상수**로 선언돼 있다")
    ok("ARM_MONOTONE" in s and "비단조 팔만" in s or "비단조 팔" in s,
       "③ ★ **팔별 단조성**이 사전등록돼 있다 — 비단조 팔만 진짜 판정 대상")
    ok("정보량 0 인 항등 관문" in s,
       "③ ★ 「매크로가 안 떨어질 것」이 **정보량 0** 이라는 진단이 적혀 있다")
    ok("def shift_logit" in s and "상수 로짓 시프트" in s,
       "③ ★★ 보정이 **로짓 공간의 상수 시프트**로 구현돼 있다(순위 보존이 구성으로 선다)")
    ok("if pi == pi_tr:" in s and "return 0.0" in s,
       "③ ★★★ π=π_tr 이면 시프트가 **정확히 0.0** — C0 이 가정이 아니라 **항등식**이다(R34 ③)")
    ok("if d0 != 0.0:" in s and "raise AssetError" in s,
       "③ ★★ C0 이 정확히 0 이 아니면 **중단**한다(런타임 검사 · R35 ④)")
    ok("TOL_IDENT = 1e-12" in s and "if worst >= TOL_IDENT:" in s,
       "③ ★ C1 항등이 깨지면 **중단** — 원인 규명 전엔 C2·C3 을 안 읽는다(R29 ②)")
    ok("C6 실패" in s,
       "③ 단조 팔인데 매크로가 움직이면 C6 에서도 중단한다")

    # ④ 회복률 분모 고정 · 절대 Δ 병기
    ok('RECOVERY_DEN = "oracle_gain"' in s and "분모 = 오라클" in s,
       "④ ★ 회복률 **분모가 사전 고정**돼 있다(오라클 팔의 이득 · R39 ①)")
    ok("(B2[\"em\"] - B2[\"raw\"]) / np.where" in s and "B2[\"oracle\"] - B2[\"raw\"]" in s,
       "④ 회복률이 사전등록된 그 식이다")
    ok("절대 Δ 를 **항상 병기**" in s,
       "④ ★★ **절대 Δ 를 항상 병기**한다 — 비만 보면 분모가 0 근처일 때 CI 가 폭발(R40 ② · R41 ②)")
    ok("RECOVERY_THR = 0.50" in s,
       "④ 합격선 50% 가 상수로 박혀 있다")

    # ⑤ 영점은 측정한다
    ok("가정하지 않는다" in s or "가정하지 마라" in s,
       "⑤ ★ 영점을 **가정하지 않는다**고 적혀 있다(R26 · R38 ②)")
    ok("N_PERM  = 3   if SMOKE else 50" in s,
       "⑤ ★ 영점 reps 기본값이 **50** 이다(R39 ①)")
    ok("rr.permutation(len(TR_I))" in s and "fit_base(TR_I, y_perm)" in s,
       "⑤ 영점이 **학습 라벨 치환** 뒤 기저를 다시 적합한다")
    ok("같은 파이프라인" in s,
       "⑤ ★ 영점이 **같은 절차**(DEV 보정 → 레코드별 EM)를 밟는다(R34 ③)")
    ok("진짜 유병률을 주입" in s,
       "⑤ ★★ 오라클 팔이 **영점에서도 이득을 낼 수 있다**는 게 소스에 경고돼 있다 — "
       "그게 이 관문이 필요한 이유다")
    ok("C2 ✅ 를 그렇게 읽지 마라" in s,
       "⑤ ★★ C2 ✅ 가 **자기 영점 안**이면 처방의 증거가 아니라고 요약이 못 박는다")

    # ⑥ 코호트·통계 위생
    ok("def cluster_boot" in s and "재표집 단위는 **레코드**" in s,
       "⑥ ★ 부트스트랩이 **레코드 군집**이다(비트가 아니다 · R11)")
    ok("지배 지분" in s and "전역 수치를 단독 인용하지 않는다" in s,
       "⑥ ★★ 전역이 주 지표인 **예외 런**이라 지배 지분·제외를 병기하고 단독 인용을 금한다(R11)")
    ok("GMIN_S" in s and "MIN_S, MIN_N = 25, 25" in s,
       "⑥ `GMIN_S` 조건이 명시돼 있다(R11-b)")
    ok("우월 프레임" in s and "sup50" in s and "sup80" in s,
       "⑥ ★ 필요표본이 **프레임(우월)**과 검정력 50/80% 를 밝힌다(R37 ①)")
    ok("해석 불가" in s and "uninterpretable" in s,
       "⑥ ★★ 효과가 0 근처면 필요표본을 **해석 불가**로 찍는다(R41 ②)")
    ok("판정은 필요표본이 아니라 **MDE 로**" in s,
       "⑥ ★ 판정은 MDE 로 한다고 적혀 있다(R41 ②)")
    ok("CHECK = [" in s and "가정" in s and "틀리면" in s,
       "⑥ **결론 검산표**가 코드에 고정돼 있다(R38 ⑦ · R39 ⑤)")
    ok("미결은 **등가가 아니다**" in s,
       "⑥ 미결을 등가로 읽지 말라고 못 박는다(R29 · R33 ①)")
    ok("SPLIT_PATTERN 이 섞여 있어야 한다" in s and "cover < 0.5" in s,
       "⑥ ★★ 분할이 유병률을 **블록으로 가르면 중단**한다(스모크가 잡은 버그의 회귀 방지)")

    # ⑦ 위생 — 새 데이터 0 · 금지 문구 · 한글 축
    # ★ 「안 쓴다」는 **선언**은 있어야 하고, **실제 사용**은 없어야 한다.
    #   (문자열 부재로 검사하면 「안 쓴다」고 적어 둔 선언까지 걸린다 — 1판이 그랬다)
    ok(s.count("np.load") == 1 and 'np.load(SV5' in s,
       "⑦ ★★ **자산을 하나만 읽는다** — `np.load` 호출이 `svdb_data5.npz` 하나뿐이다")
    ok("svdb_pdelin" not in s and "PDEL" not in s and "p_idx" not in s and "p_score" not in s,
       "⑦ ★ P 위치 자산(Q7-P0)을 **실제로 안 쓴다** — 변수도 경로도 없다")
    ok('D5["beat"]' not in s and "XB" not in s,
       "⑦ 비트 파형 배열도 안 읽는다 — 리듬 특징만 쓴다")
    ok("BUT PDB 도 쓰지 않는다" in s,
       "⑦ ★ **새 데이터 0** 이 소스에 선언돼 있다(λ 는 이 런의 질문이 아니다)")
    for bad in ("아무도 안 했다", "최초로 증명", "확실히 입증", "최초로 규명"):
        ok(bad not in s, f"⑦ 금지 문구 없음 — 「{bad}」")
    axis = re.findall(r'set_(?:x|y)label\(([^\n]*)\)', s) + \
        re.findall(r'set_(?:x|y)ticklabels\(([^\n]*)\)', s) + \
        re.findall(r'set_title\(([^\n]*)\)', s)
    han = [a for a in axis if re.search(r'["\'][^"\']*[가-힣]', a)]
    ok(not han, f"⑦ 그림 축·제목에 한글이 없다(발견 {len(han)}건)")

    # ⑧ ★ 스모크 손잡이는 **비용만** 만진다 — 관문 문턱을 건드리면 안 된다
    knobs = set(re.findall(r'^\s*(\w+)\s*=.*\bif SMOKE\b', s, re.M))
    ok(knobs <= {"NB_BOOT", "N_PERM"},
       f"⑧ ★★ SMOKE 가 만지는 건 **비용 손잡이뿐**이다({sorted(knobs)}) — 관문 문턱은 불변")
    ok("관문 문턱은 그대로다" in s,
       "⑧ 스모크가 문턱을 안 건드린다고 소스에 적혀 있다")
    for thr in ("RECOVERY_THR = 0.50", "TOL_IDENT = 1e-12", "MIN_S, MIN_N = 25, 25"):
        ok("SMOKE" not in thr and thr in s, f"⑧ 문턱이 SMOKE 와 무관하게 고정 — `{thr}`")


# ══════════════════════════════════════════════════════════════════ 동적
def dynamic():
    print("\n[동적] 절차가 옳게 움직이는가")
    from sklearn.metrics import average_precision_score, roc_auc_score

    def logit(p):
        p = np.clip(np.asarray(p, float), 1e-12, 1 - 1e-12)
        return np.log(p) - np.log1p(-p)

    def em_prior(p, pi_tr, iters=500, tol=1e-9, clip=1e-4):
        pi = float(pi_tr)
        for _ in range(iters):
            w = pi / pi_tr; v = (1.0 - pi) / (1.0 - pi_tr)
            num = w * p
            pp = num / (num + v * (1.0 - p))
            new = float(np.clip(pp.mean(), clip, 1.0 - clip))
            if abs(new - pi) < tol:
                pi = new; break
            pi = new
        return pi

    rng = np.random.RandomState(46)

    # ── ⓐ ★★★ 상수 로짓 시프트는 레코드 내 순위를 **정확히** 보존한다
    y = (rng.rand(4000) < 0.2).astype(int)
    p = np.clip(rng.beta(2, 6, 4000) + 0.25 * y, 1e-6, 1 - 1e-6)
    L = logit(p)
    ap0, au0 = average_precision_score(y, L), roc_auc_score(y, L)
    dmax_l = dmax_p = 0.0
    for pi in (0.01, 0.05, 0.35, 0.80):
        d = float(logit(pi) - logit(0.2))
        dmax_l = max(dmax_l, abs(average_precision_score(y, L + d) - ap0),
                     abs(roc_auc_score(y, L + d) - au0))
        # 대조 — **확률 공간**에서 같은 보정을 하면?
        w = pi / 0.2; v = (1 - pi) / (1 - 0.2)
        pp = (w * p) / (w * p + v * (1 - p))
        dmax_p = max(dmax_p, abs(average_precision_score(y, pp) - ap0),
                     abs(roc_auc_score(y, pp) - au0))
    ok(dmax_l == 0.0,
       f"ⓐ ★★★ **로짓 공간 덧셈**이면 레코드 내 AP·AUROC 가 **정확히 불변**이다(max|Δ| {dmax_l:.1e}) "
       "— C0·C1 이 가정이 아니라 **구성**으로 선다")
    ok(dmax_p <= 1e-9,
       f"ⓐ (참고) 확률 공간 구현도 이 조건에선 순위를 보존한다(max|Δ| {dmax_p:.1e}) — "
       "다만 극단 포화에서 동순위가 생길 수 있어 **로짓 덧셈이 더 안전**하다")

    # ── ⓑ 그런데 **pooled** 지표는 움직인다 → 그래서 주 지표가 전역이다
    recs, ys, ls = [], [], []
    for r, pi_r in enumerate((0.03, 0.10, 0.30)):
        n = 3000
        yy = (rng.rand(n) < pi_r).astype(int)
        pp = np.clip(rng.beta(2, 6, n) + 0.25 * yy, 1e-6, 1 - 1e-6)
        recs += [r] * n; ys.append(yy); ls.append(logit(pp))
    recs = np.array(recs); ys = np.concatenate(ys); ls = np.concatenate(ls)
    ap_raw = average_precision_score(ys, ls)
    adj = ls.copy()
    for r, pi_r in enumerate((0.03, 0.10, 0.30)):
        m = recs == r
        adj[m] = adj[m] + (logit(pi_r) - logit(ys.mean()))
    ap_or = average_precision_score(ys, adj)
    per_raw = [average_precision_score(ys[recs == r], ls[recs == r]) for r in range(3)]
    per_or = [average_precision_score(ys[recs == r], adj[recs == r]) for r in range(3)]
    ok(ap_or > ap_raw and max(abs(a - b) for a, b in zip(per_raw, per_or)) == 0.0,
       f"ⓑ ★★★ **전역은 움직이고**(PR-AUC {ap_raw:.4f} → {ap_or:.4f}) "
       "**매크로는 정확히 불변**이다 — 주 지표가 전역이어야 하는 이유이자, "
       "「매크로 비열등」이 정보량 0 인 이유")

    # ── ⓒ EM 구현 정합성 — **보정된** 사후확률에서 진짜 사전확률을 되찾는가
    errs = []
    for pi_true in (0.03, 0.10, 0.20, 0.35):
        n = 20000
        yy = rng.rand(n) < pi_true
        x = rng.normal(np.where(yy, 1.2, 0.0), 1.0)
        o = np.exp(1.2 * x - 0.72) * (0.20 / 0.80)      # π_tr = 0.20 기준 베이즈 사후확률
        errs.append(abs(em_prior(o / (1 + o), 0.20) - pi_true))
    ok(max(errs) < 0.02,
       f"ⓒ ★★ 사후확률이 **보정돼 있으면** EM 이 진짜 사전확률을 되찾는다(최대 오차 {max(errs):.4f})")

    # ── ⓓ ★★ 그런데 **보정 안 된** 사후확률에서는 무너진다 → DEV 보정이 전제인 이유
    bad = []
    for pi_true in (0.03, 0.10, 0.20, 0.35):
        n = 20000
        yy = rng.rand(n) < pi_true
        x = rng.normal(np.where(yy, 1.2, 0.0), 1.0)
        o = np.exp(3.0 * x - 0.72) * (0.20 / 0.80)      # ★ 과신(기울기 1.2 → 3.0)
        bad.append(abs(em_prior(np.clip(o / (1 + o), 1e-6, 1 - 1e-6), 0.20) - pi_true))
    ok(max(bad) > max(errs) * 3,
       f"ⓓ ★★★ **과신(미보정) 사후확률에서는 EM 이 무너진다**(최대 오차 {max(bad):.4f} ≫ "
       f"보정된 경우 {max(errs):.4f}) — 그래서 기저 보정을 **DEV 에서 먼저** 적합한다")

    # ── ⓔ ★★ 오라클 팔은 **정보 없는 기저**에서도 이득을 낸다 → 영점이 필수
    n_ = 3000
    ys2, ls2, rc2 = [], [], []
    for r, pi_r in enumerate((0.03, 0.10, 0.30)):
        yy = (rng.rand(n_) < pi_r).astype(int)
        ys2.append(yy); ls2.append(logit(np.full(n_, 0.143)) + rng.normal(0, 1e-3, n_))
        rc2 += [r] * n_
    ys2 = np.concatenate(ys2); ls2 = np.concatenate(ls2); rc2 = np.array(rc2)
    a_raw = average_precision_score(ys2, ls2)
    a2 = ls2.copy()
    for r, pi_r in enumerate((0.03, 0.10, 0.30)):
        a2[rc2 == r] += logit(pi_r) - logit(0.143)
    a_or = average_precision_score(ys2, a2)
    ok(a_or - a_raw > 0.05,
       f"ⓔ ★★★ **신호가 0 인 기저**에서도 오라클 보정만으로 전역 PR-AUC 가 "
       f"{a_raw:.4f} → {a_or:.4f} 로 오른다 — 진짜 유병률이 **정보 그 자체**이기 때문이다. "
       "그래서 C2 의 이득은 **반드시 자기 영점 대비**로 읽어야 한다(C4)")

    # ── ⓕ ★★★ 판정 순서 — C2 ❌ 면 회복률을 **읽지 않는다**
    def judge(c2_pass, abs_ci_lo, ratio):
        ratio_read = bool(c2_pass)
        c3 = (abs_ci_lo > 0) and (ratio >= 0.50) and ratio_read
        return ratio_read, c3
    r1, c1_ = judge(False, 0.01, 9.9)      # 회복률이 아무리 커도
    r2, c2_ = judge(True, 0.01, 0.80)
    ok(r1 is False and c1_ is False,
       "ⓕ ★★★ C2 ❌ 면 회복률이 **9.9 여도** C3 이 서지 않는다 — 순서가 판정의 일부다")
    ok(r2 is True and c2_ is True,
       "ⓕ C2 ✅ 일 때만 회복률을 읽고 C3 이 설 수 있다")

    # ── ⓖ 분모가 0 근처면 **비**의 CI 가 폭발한다 → 절대 Δ 를 병기하는 이유
    num = rng.normal(0.002, 0.004, 4000)
    den_small = rng.normal(0.003, 0.004, 4000)
    den_big = rng.normal(0.050, 0.004, 4000)
    w_small = np.percentile(num / den_small, 97.5) - np.percentile(num / den_small, 2.5)
    w_big = np.percentile(num / den_big, 97.5) - np.percentile(num / den_big, 2.5)
    ok(w_small > 20 * w_big,
       f"ⓖ ★★ 분모가 0 근처면 비의 CI 폭이 {w_small:.1f} 로 폭발한다(분모가 크면 {w_big:.3f}) — "
       "**절대 Δ 를 항상 병기**하는 이유(R40 ② · R41 ②)")

    # ── ⓗ ★★ 부담순 배분에 **덩어리 패턴**을 쓰면 유병률이 블록으로 갈린다 (회귀 검사)
    burd = np.linspace(0.03, 0.35, 24)
    blocked = ("TRAIN",) * 8 + ("DEV",) * 5 + ("TEST",) * 7
    mixed = ("TRAIN", "TEST", "DEV", "TRAIN", "TEST", "TRAIN", "DEV", "TEST",
             "TRAIN", "TEST", "DEV", "TRAIN", "TEST", "TRAIN", "DEV", "TEST",
             "TRAIN", "TEST", "DEV", "TRAIN")
    def cover(pat):
        te = [burd[i] for i in range(len(burd)) if pat[i % len(pat)] == "TEST"]
        return (max(te) - min(te)) / (burd.max() - burd.min())
    ok(cover(blocked) < 0.5 < cover(mixed),
       f"ⓗ ★★★ 덩어리 패턴은 TEST 커버리지 {cover(blocked):.2f} 로 **유병률을 블록으로 가르고**, "
       f"섞인 패턴은 {cover(mixed):.2f} 다 — Q3 의 질문이 유병률 차이에 걸려 있으므로 "
       "블록 분할은 **관문을 무의미하게** 만든다(스모크런이 잡은 결함)")

    # ── ⓘ 필요표본은 효과² 반비례이고, 효과가 0 근처면 수가 아니다
    need = lambda n, half, eff: n * (half / abs(eff)) ** 2 if abs(eff) > 1e-9 else np.inf
    ok(need(24, 0.03, 0.0007) > 100 * need(24, 0.03, 0.06),
       "ⓘ ★ 효과가 0 근처면 필요표본이 임의로 커진다 — **해석 불가**로 찍어야 한다(R41 ②)")


if __name__ == "__main__":
    if not os.path.exists(NB):
        print(f"❌ 노트북이 없다 — {NB}")
        sys.exit(1)
    print("=" * 78)
    print("Q3 픽스처 — 판정 순서(C2→C3) · DEV 전용 보정 · 매크로는 항등 대조")
    print("=" * 78)
    static()
    dynamic()
    print("\n" + "=" * 78)
    print(f"통과 {len(PASS)} · 실패 {len(FAIL)}")
    for f in FAIL:
        print("  ✗ " + f)
    sys.exit(1 if FAIL else 0)
