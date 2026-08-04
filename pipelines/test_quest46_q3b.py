#!/usr/bin/env python3
"""Q3-B(`quest46_q3b_prior_shuffle`) 픽스처 — 사전확률 셔플 대조.

이 런은 새 가설이 아니라 **자(대조)를 고친다**. Q3 의 C4 는 라벨치환 영점을 썼는데,
그러면 기저가 무력해져 **raw 가 관측보다 낮은 데서 출발**하므로 이득끼리 비교할 수 없었다
(천장 효과 · R40 ②). 그래서 지킬 것이 셋이다:

  ① 대조가 **구성으로 공정**할 것 — 같은 기저 점수 · derangement · **raw 가 정확히 동일**
  ② 재현 앵커를 **SMOKE 가 아니라 코호트 조건**으로 걸 것 — 스위치를 두면 공식 실행에서도 꺼진다
  ③ 영점을 **Δ 가 아니라 절대 수준**으로 비교하고, Q3 이 안 남긴 **영점 raw 를 실측**할 것
"""
import json
import os
import re
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NB = os.path.join(ROOT, "notebooks", "quest46_q3b_prior_shuffle.ipynb")

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

    # ① ★★★ 대조가 구성으로 공정한가
    ok("def derangement" in s and "자기 자리를 받는 원소가" in s,
       "① ★★ 셔플이 **derangement** 다 — 자기 값을 받는 레코드가 있으면 대조가 희석된다")
    ok("n_self != 0" in s and "raise AssetError" in s,
       "① ★★★ 자기 값을 받은 레코드가 하나라도 있으면 **중단**한다")
    ok("모든 팔이 **같은 기저 점수**에서 출발한다" in s and "raw 가 구성으로 동일" in s,
       "① ★★★ 모든 팔이 **같은 raw** 에서 출발한다는 게 소스에 박혀 있다")
    ok("이것이 C4 가 못 한 것이다" in s,
       "① ★ Q3 의 C4 가 무엇을 못 했는지가 소스에 적혀 있다")
    ok("def shift_logit" in s and "if pi == pi_tr:" in s and "return 0.0" in s,
       "① 보정이 **상수 로짓 시프트**이고 π=π_tr 에서 정확히 0.0 이다")
    ok("d_ident != 0.0" in s,
       "① 항등 팔이 정확히 0 이 아니면 **중단**한다(R34 ③ · R35 ④)")
    ok("TOL_IDENT = 1e-12" in s and "worst >= TOL_IDENT" in s,
       "① 매크로 항등이 깨지면 **중단** — 여기서도 매크로는 검산이다")

    # ② ★★★ 재현 앵커는 **코호트 조건**에 걸린다 (SMOKE 스위치가 아니다)
    ok("COHORT_MATCH = (" in s and "len(RS) == 78" in s and "len(REC_OK) == 56" in s,
       "② ★★★ 재현 앵커가 **코호트 동일성**으로 게이팅돼 있다")
    # ★ 구조로 검사한다 — 재현 앵커가 든 **셀에 SMOKE 가 아예 없어야** 하고,
    #   raise 는 `if COHORT_MATCH:` 블록 **안**에 있어야 한다.
    anchor_cell = next((c for c in cs if "if d_rep > TOL_REPRO:" in c), "")
    ok(bool(anchor_cell) and "SMOKE" not in anchor_cell,
       "② ★★★ 재현 앵커가 든 셀에 **SMOKE 가 없다** — 스위치를 두면 공식 실행에서도 꺼진다")
    ok(0 <= anchor_cell.find("if COHORT_MATCH:") < anchor_cell.find("if d_rep > TOL_REPRO:"),
       "② ★★ 재현 raise 가 `if COHORT_MATCH:` **블록 안**에 있다")
    ok("스모크 플래그로 관문을 끄지 않는다" in s,
       "② ★★ 왜 SMOKE 로 관문을 끄지 않는지가 소스에 적혀 있다")
    ok("공식 재현이 아니라 리허설" in s and "수치를 인용하지 마라" in s,
       "② ★★ 코호트가 다르면 스스로 **리허설**이라고 선언하고 인용을 막는다")
    ok('COHORT_MATCH and ok_("B0")' in s,
       "② ★ `passed` 가 **코호트 일치일 때만** True 가 될 수 있다")
    ok("TOL_REPRO = 0.005" in s,
       "② 재현 허용오차가 상수로 박혀 있다(로그가 4자리라 이보다 못 좁힌다)")

    # ③ ★★★ 주 통계량 — 짝지은 차 · 같은 재표집
    ok('PRIMARY = "oracle_minus_shuffled"' in s,
       "③ ★★★ 주 통계량이 **`oracle − shuffled` 짝지은 차**로 사전등록돼 있다")
    ok("모든 팔을 **같은 재표집**에 태워" in s,
       "③ ★★ 모든 팔이 **같은 부트스트랩 재표집**을 탄다(짝지은 차의 전제)")
    ok("재표집 단위는 **레코드**" in s,
       "③ 부트스트랩이 레코드 군집이다(R11)")
    ok('d_b1 = B["oracle"] - SH' in s,
       "③ B1 이 실제로 두 팔의 차다")
    ok("주 통계량은 **짝지은 차**다(비가 아니다" in s,
       "③ ★ 비가 아니라 차로 판정한다(R40 ②)")

    # ④ ★★★ 영점은 절대 수준으로 · 영점 raw 를 남긴다
    ok("Δ 가 아니라 **절대 수준**" in s or "Δ 가 아니라 절대 수준" in s,
       "④ ★★★ 영점을 **Δ 가 아니라 절대 수준**으로 비교한다")
    ok('NUL = {"raw": []' in s and "영점 raw" in s and "Q3 이 안 남긴 수" in s,
       "④ ★★★ **영점 raw 를 실측해 로그에 남긴다** — Q3 은 이득만 찍어 비교가 불가능했다")
    ok("출발점이" in s and "다르므로 이 둘을 직접 비교하지 않는다" in s,
       "④ ★★ 두 이득을 직접 비교하지 않는다고 소스에 못 박혀 있다")
    ok('decide(no_lo, no_hi, AP_ORACLE, "<")' in s,
       "④ B2 판정이 **수준 대 수준**이다")
    ok("천장 효과" in s,
       "④ ★ 천장 효과가 왜 이득 비교를 깨는지가 적혀 있다")

    # ⑤ 성분 병기 · 미결 ≠ 등가
    ok("차의 부호를 성분 없이 인용하지 않는다" in s and "shuf −raw" in s,
       "⑤ ★ 차와 함께 **성분**(oracle−raw · shuf−raw)을 병기한다(R36 ⑤)")
    ok("등가가 아니다" in s,
       "⑤ 미결을 등가로 읽지 말라고 못 박는다(R33 ① · R36 ①)")
    ok("상한은 CI 상단" in s,
       "⑤ 미결일 때 **상한**을 말한다(R36 ①)")

    # ⑥ MLLS 는 별도 팔이 아니다
    ok("MLLS 는 Saerens EM 과 **같은 것**" in s or "MLLS 는 Saerens EM 과 같은 것" in s,
       "⑥ ★★ **MLLS = Saerens EM** 임을 명시한다 — 인수인계의 「BBSE·MLLS」를 그대로 베끼지 않았다")
    ok("em (=MLLS)" in s,
       "⑥ 추정기 표에서도 EM 이 MLLS 임을 표기한다")
    ok("Rogan" in s or "((p > TH).mean() - FPR) / (TPR - FPR)" in s,
       "⑥ BBSE 가 혼동행렬 기반 닫힌 해다")
    ok("문턱도 **DEV 에서** 고정" in s,
       "⑥ ★ BBSE 문턱도 **DEV 에서** 고정한다(R22 · R36 ②)")

    # ⑦ B4·B5 는 관문이 아니다
    ok("B4 — 관문 아님" in s or "관문 아님. Q3 의 실패 기전" in s,
       "⑦ B4(π̂ 진단)가 **관문이 아님**을 명시한다")
    ok("후보 지목" in s and "채택은 다음 런에서 사전등록" in s,
       "⑦ ★ B5(추정기 비교)가 **후보 지목**이지 채택이 아니라고 못 박는다")
    ok("진단**이지 주 팔 교체가 아니다" in s or "진단이지 주 팔 교체가 아니다" in s,
       "⑦ ★★ `em@대안보정기` 가 **진단**이지 주 팔 교체가 아니라고 못 박는다")
    ok("입자도" in s and "고유값" in s and "계단이 거칠면 EM 이" in s,
       "⑦ ★★ 사후확률 **입자도**(고유값 수)를 진단으로 찍는다 — EM 붕괴의 실제 기전")
    ok("추정 지표** 위에 있어 전역 PR-AUC 의 오염과 무관" in s
       or "추정 지표" in s and "오염과 무관" in s,
       "⑦ ★★ B5 가 **추정 지표** 위에 있어 pooled 오염과 무관하다고 적혀 있다")

    # ⑧ 순서 · 위생
    i1 = next((i for i, c in enumerate(cs) if "★★★ B1 —" in c), -1)
    i2 = next((i for i, c in enumerate(cs) if "영점(라벨치환) **절대 수준**" in c), -1)
    ok(0 <= i1 < i2,
       f"⑧ B1(주 관문)이 B2 **앞 셀**에서 계산된다(B1 셀 {i1} < B2 셀 {i2})")
    ok(s.count("np.load") == 1 and "np.load(SV5" in s,
       "⑧ ★ **새 데이터 0** — 자산을 하나만 읽는다")
    ok("svdb_pdelin" not in s and "p_idx" not in s and "p_score" not in s,
       "⑧ P 위치 자산을 쓰지 않는다")
    for bad in ("아무도 안 했다", "최초로 증명", "확실히 입증"):
        ok(bad not in s, f"⑧ 금지 문구 없음 — 「{bad}」")
    axis = re.findall(r'set_(?:x|y)label\(([^\n]*)\)', s) + \
        re.findall(r'set_(?:x|y)ticklabels\(([^\n]*)\)', s) + \
        re.findall(r'set_title\(([^\n]*)\)', s)
    han = [a for a in axis if re.search(r'["\'][^"\']*[가-힣]', a)]
    ok(not han, f"⑧ 그림 축·제목에 한글이 없다(발견 {len(han)}건)")
    knobs = set(re.findall(r'^\s*(\w+)\s*=.*\bif SMOKE\b', s, re.M))
    ok(knobs <= {"NB_BOOT", "N_PERM", "N_SHUF"},
       f"⑧ ★★ SMOKE 가 만지는 건 **비용 손잡이뿐**이다({sorted(knobs)})")
    ok("CHECK = [" in s and "가정" in s and "틀리면" in s,
       "⑧ **결론 검산표**가 코드에 고정돼 있다(R38 ⑦ · R39 ⑤)")
    ok("해석 불가" in s and "uninterpretable" in s,
       "⑧ 효과가 0 근처면 필요표본을 **해석 불가**로 찍는다(R41 ②)")
    ok("지배 지분" in s and "전역 단독 인용 금지" in s,
       "⑧ 지배 지분을 병기하고 전역 단독 인용을 금한다(R11)")


# ══════════════════════════════════════════════════════════════════ 동적
def dynamic():
    print("\n[동적] 절차가 옳게 움직이는가")
    from sklearn.metrics import average_precision_score

    def logit(p):
        p = np.clip(np.asarray(p, float), 1e-12, 1 - 1e-12)
        return np.log(p) - np.log1p(-p)

    def derangement(n, rng):
        for _ in range(1000):
            p = rng.permutation(n)
            if not np.any(p == np.arange(n)):
                return p
        return np.roll(np.arange(n), 1)

    rng = np.random.RandomState(63)

    # ── ⓐ derangement 는 자기 자리를 **하나도** 안 남긴다
    bad = 0
    for s_ in range(200):
        p = derangement(12, np.random.RandomState(s_))
        bad += int(np.any(p == np.arange(12)))
    ok(bad == 0, f"ⓐ ★ derangement 200회 전부 **고정점이 없다**(위반 {bad}회)")

    # ── 합성 코호트: 레코드마다 유병률이 다르고, 기저는 약하게 판별한다
    def cohort(n_rec=14, n=1200, sep=0.55, seed=1):
        r_ = np.random.RandomState(seed)
        pis = np.linspace(0.02, 0.45, n_rec)
        ys, ls, rc = [], [], []
        for i, pi in enumerate(pis):
            yy = (r_.rand(n) < pi).astype(int)
            x = r_.normal(np.where(yy, sep, 0.0), 1.0)
            o = np.exp(sep * x - sep * sep / 2) * (0.1 / 0.9)
            ls.append(logit(np.clip(o / (1 + o), 1e-6, 1 - 1e-6)))
            ys.append(yy); rc += [i] * n
        return np.array(rc), np.concatenate(ys), np.concatenate(ls), pis

    rc, ys, ls, pis = cohort()
    pi_tr = ys.mean()
    def shift(pi_by):
        out = ls.copy()
        for i in range(len(pis)):
            out[rc == i] += logit(pi_by[i]) - logit(pi_tr)
        return out
    ap = lambda L: average_precision_score(ys, L)
    ap_raw, ap_or = ap(ls), ap(shift(pis))
    perm = derangement(len(pis), np.random.RandomState(5))
    ap_sh = ap(shift(pis[perm]))

    # ── ⓑ ★★★ 셔플 팔은 raw 를 건드리지 않는다 — 같은 기저 점수를 쓰므로 **구성으로** 동일
    ok(ap(ls) == ap_raw,
       "ⓑ ★★★ 오라클 팔이든 셔플 팔이든 **기저 점수는 그대로**다 → raw 가 구성으로 동일하다 "
       "(라벨치환 영점은 이 성질이 **없다**)")

    # ── ⓒ ★★★ 대응이 맞으면 이득, 깨지면 무너진다 (B1 이 재는 것)
    ok(ap_or > ap_raw and ap_sh < ap_or,
       f"ⓒ ★★★ oracle {ap_or:.4f} > raw {ap_raw:.4f} 이고 shuffled {ap_sh:.4f} 는 "
       f"**무너진다**(oracle−shuffled {ap_or - ap_sh:+.4f}) — B1 이 재는 게 **대응**이다")

    # ── ⓓ ★★ 음성 대조: 유병률이 **다 같으면** 셔플이 아무것도 안 바꾼다 → B1 ≈ 0
    rc2, ys2, ls2, _ = cohort(seed=2)
    flat = np.full(14, ys2.mean())
    def shift2(pi_by):
        out = ls2.copy()
        for i in range(14):
            out[rc2 == i] += logit(pi_by[i]) - logit(ys2.mean())
        return out
    d_flat = abs(average_precision_score(ys2, shift2(flat))
                 - average_precision_score(ys2, shift2(flat[derangement(14, np.random.RandomState(9))])))
    ok(d_flat < 1e-12,
       f"ⓓ ★★ **음성 대조** — 유병률이 다 같으면 셔플이 아무것도 안 바꾼다(|Δ| {d_flat:.1e}). "
       "즉 B1 은 **유병률이 벌어져 있을 때만** 힘이 있다(검산표의 가정 항목이 그것이다)")

    # ── ⓔ ★★★ C4 의 결함 재현 — 라벨치환 영점은 **raw 자체를 바꾼다**
    ls_null = logit(np.full(len(ys), pi_tr)) + rng.normal(0, 1e-3, len(ys))
    ap_null_raw = average_precision_score(ys, ls_null)
    out = ls_null.copy()
    for i in range(len(pis)):
        out[rc == i] += logit(pis[i]) - logit(pi_tr)
    ap_null_or = average_precision_score(ys, out)
    ok(ap_null_raw < ap_raw - 0.05,
       f"ⓔ ★★★ 라벨치환 영점은 raw 를 {ap_raw:.4f} → {ap_null_raw:.4f} 로 **떨어뜨린다** — "
       "출발점이 달라지므로 **이득끼리 비교하면 안 된다**(Q3 의 C4 가 그렇게 죽었다)")
    ok((ap_null_or - ap_null_raw) > (ap_or - ap_raw),
       f"ⓔ ★★★ 그리고 낮은 데서 출발한 영점의 **이득이 더 크다**"
       f"({ap_null_or - ap_null_raw:+.4f} > {ap_or - ap_raw:+.4f}) — **천장 효과**다. "
       "그래서 Q3 의 C4 가 「관측이 영점 안」이라는 잘못된 경고를 냈다")
    ok(ap_or > ap_null_or,
       f"ⓔ ★★ **수준으로 비교하면** 관측 oracle {ap_or:.4f} > 영점 oracle {ap_null_or:.4f} 로 "
       "제대로 갈린다 — 그래서 B2 는 Δ 가 아니라 **수준**을 본다")

    # ── ⓕ BBSE(Rogan–Gladen) 정합성 — 알려진 TPR/FPR 에서 진짜 유병률을 되찾는가
    errs = []
    for pi_true in (0.03, 0.12, 0.30, 0.55):
        n = 40000
        yy = rng.rand(n) < pi_true
        pred = np.where(yy, rng.rand(n) < 0.80, rng.rand(n) < 0.10)   # TPR .80 · FPR .10
        errs.append(abs((pred.mean() - 0.10) / (0.80 - 0.10) - pi_true))
    ok(max(errs) < 0.02,
       f"ⓕ ★ BBSE 닫힌 해가 진짜 유병률을 되찾는다(최대 오차 {max(errs):.4f}) — "
       "**추정 지표**라 pooled 오염과 무관하다")

    # ── ⓖ ★★★ EM 을 clip 경계로 모는 건 **사후확률의 거친 입자도**다
    #    (Q3 은 isotonic 을 골랐고 그 TEST 사후확률은 고유값이 61개뿐이었다)
    def em_prior(p, pi_tr_, iters=500, tol=1e-9, clip=1e-2):
        pi = float(pi_tr_)
        for _ in range(iters):
            w = pi / pi_tr_; v = (1.0 - pi) / (1.0 - pi_tr_)
            num = w * p
            pp = num / (num + v * (1.0 - p))
            new = float(np.clip(pp.mean(), clip, 1.0 - clip))
            if abs(new - pi) < tol:
                pi = new; break
            pi = new
        return pi

    n = 20000
    yy = rng.rand(n) < 0.576                       # ★ Q3 의 지배 레코드와 같은 유병률
    x = rng.normal(np.where(yy, 0.9, 0.0), 1.0)
    o = np.exp(0.9 * x - 0.405) * (0.08 / 0.92)    # π_tr = 0.08 기준 사후확률
    p_cont = np.clip(o / (1 + o), 1e-6, 1 - 1e-6)

    def quantize(p, nlev):
        q = np.quantile(p, np.linspace(0, 1, nlev + 1))
        idx = np.clip(np.searchsorted(q[1:-1], p), 0, nlev - 1)
        return np.clip(q[idx], 1e-6, 1 - 1e-6)

    hat_cont = em_prior(p_cont, 0.08)
    hat_c3 = em_prior(quantize(p_cont, 3), 0.08)
    hat_c30 = em_prior(quantize(p_cont, 30), 0.08)
    ok(abs(hat_cont - 0.576) < 0.05,
       f"ⓖ ★★ **연속** 사후확률이면 EM 이 π* 를 거의 되찾는다(π̂ {hat_cont:.4f} vs 0.576)")
    ok(abs(hat_c3 - 0.01) < 1e-9,
       f"ⓖ ★★★ **같은 자료인데 계단 3개로 뭉개면 EM 이 clip 바닥으로 달아난다**"
       f"(π̂ {hat_c3:.4f} = clip). Q3 의 지배 레코드에서 일어난 일이고, 원인은 과신이 아니라 "
       "**입자도**다 — isotonic 은 계단 함수라 고유값이 적다")
    ok(hat_c3 < hat_c30 < hat_cont,
       f"ⓖ ★ 입자도가 거칠수록 단조로 나빠진다(계단3 {hat_c3:.4f} < 계단30 {hat_c30:.4f} "
       f"< 연속 {hat_cont:.4f}) — B5 의 `em@대안보정기` 가 재는 게 이 축이다")

if __name__ == "__main__":
    if not os.path.exists(NB):
        print(f"❌ 노트북이 없다 — {NB}")
        sys.exit(1)
    print("=" * 78)
    print("Q3-B 픽스처 — 셔플 대조의 구성적 공정성 · 코호트 게이팅 · 수준 비교")
    print("=" * 78)
    static()
    dynamic()
    print("\n" + "=" * 78)
    print(f"통과 {len(PASS)} · 실패 {len(FAIL)}")
    for f in FAIL:
        print("  ✗ " + f)
    sys.exit(1 if FAIL else 0)
