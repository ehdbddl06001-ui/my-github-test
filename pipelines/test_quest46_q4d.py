#!/usr/bin/env python3
"""Q4-D(`quest46_q4d_calibrator_shift_equivariance`) 픽스처 — 원인 제거 + 대가 측정.

Q4-C(`20260805T0212`)가 원인을 특정했다. `add` 모드에서 burden 은 레코드 내 상수·선형
이므로 **보정 전** 테스트시 burden 은 레코드 내 판별에 **원리적으로 기여하지 않는다** —
실측으로 `TT`≡`TS` 매크로 **0.577231 동일 · 순위 56/56 일치**였다. 그런데 보정 후엔
갈라졌고(TT −0.0074 · TE −0.0109 · TS −0.0419) **손실이 b̂ 오차 크기를 그대로 따라간다**.

    범인은 **등장성 보정의 계단 구조**다. 그리고 이건 **구성으로 고칠 수 있다**:
    Platt 은 logit(σ(a·s+b)) = a·s+b 라 상수 시프트를 **상수 시프트인 채 보존**하므로
    매크로가 **정확히 불변**이 된다. 근사가 아니라 항등이다.

이 런에서 빠뜨리면 결과가 무효인 것 다섯:
  ① **보정기가 「보정된 로짓」을 직접 반환해야** 한다. 확률로 왕복하면
     `logit(clip(σ(as+b), 1e-6, 1−1e-6))` 이 포화 구간에서 clip 에 걸려 항등이 깨진다
     (실측: 시프트 후 차이의 SD 5.86e-14, 포화가 심하면 훨씬 커진다). 편법이 아니라
     **더 정확한 구현**이고, G1 을 항등으로 만드는 자리다
  ② **G1 이 이 런의 자다**(R35 ①) — Platt 하 `TT`≡`TE`≡`TS` 는 **수식에서 따라오므로**
     안 서면 코드가 틀린 것이다. 실패 시 **중단**. 보정 전 항등은 **네 칸 전부** 확인
     (Q4-C 는 `TT`·`TS` 만 쟀다)
  ③ **「없앨 수 있나」가 아니라 「바꾸는 게 이득인가」** 를 묻는다(R40 ①) — Platt 이 π̂
     의존을 0 으로 만들어도 보정이 거칠어 교차레코드가 나빠지면 **순손해**다.
     G2(관문)와 G3(대가)를 **함께** 읽는다
  ④ **주 관문은 배포 가능판끼리**(`TE − A_em`) — 오라클은 상한이지 방법이 아니다
     (Q4-C 실측 `A_em` 전역 0.1254 < raw 0.2097)
  ⑤ **분해의 식별 판정** — 합계가 0 을 떼는가 + 상호작용이 **합계 대비** 작은가.
     「가장 작은 몫」기준을 쓰면 Platt 에서 테스트 몫이 구성으로 0 이라 **항상 실패**한다.
     정작 그때가 분해가 가장 잘 되는 경우다(스모크가 잡았다)
"""
import json
import os
import re
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NB = os.path.join(ROOT, "notebooks", "quest46_q4d_calibrator_shift_equivariance.ipynb")

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

    # ── ① 보정기가 보정 로짓을 직접 낸다
    ok('CALS = ("iso", "platt")' in s and 'PRIMARY_CAL = "platt"' in s,
       "① 보정기 두 종이 사전등록돼 있고 처방 후보가 `platt` 이다")
    ok("def make_cal(kind, s, y)" in s,
       "① 보정기가 한 함수로 매개변수화돼 있다 — 팔마다 같은 코드가 돈다")
    ok("lambda v: a * np.asarray(v, float) + b" in s,
       "① ★★★ Platt 의 보정 로짓을 **해석적으로** `a·s+b` 로 낸다 — 확률 왕복이 아니다")
    ok("확률로 왕복하면" in s and "clip" in s and "5.86e-14" in s,
       "① ★★★ 확률 왕복이 왜 안 되는지(포화 구간 clip · 실측 SD 5.86e-14)가 박혀 있다")
    ok("보정 로짓을 직접" in s or "보정된 로짓을 직접" in s,
       "① 「보정 로짓을 직접 반환한다」가 명시돼 있다")
    ok("(lambda v: logit(p_(v)))" in s,
       "① 등장성은 `logit(clip(·))` 로 — 계단 구조가 그대로 남는다")

    # ── ② G1 이 자다
    ok('TRIO = ("TT", "TE", "TS")' in s,
       "② G1 이 **테스트시 burden 만 다른 세 팔**을 비교한다")
    ok("raise AssetError(f\"G1 실패" in s and "수식에서 따라오는 항등" in s,
       "② ★★★ Platt 하 항등이 깨지면 **중단**한다 — 가설이 아니라 구현 검사다")
    ok('pre_ident_T' in s and 'pre_ident_S' in s,
       "② ★★★ 보정 전 항등을 **네 칸 전부** 확인한다(학습 true 행 + 학습 shuf 행) — "
       "Q4-C 는 `TT`·`TS` 만 쟀다")
    ok('raise AssetError(f"보정 전 항등 실패' in s,
       "② 보정 전 항등이 깨져도 **중단**한다")
    ok("ISO_LEAK" in s and 'G1["iso"]["spread"]' in s,
       "② ★★ 등장성의 폭을 **누출의 실측치**로 남긴다")
    ok("q4c_pre_macro=0.577231" in s and 'q4c_pre_rank="56/56"' in s,
       "② Q4-C 의 보정 전 항등 실측이 앵커로 박혀 있다")

    # ── ③ 「바꾸는 게 이득인가」 — G2 와 G3 를 함께
    ok("ece_of" in s and "ece_iso" in s and "ece_platt" in s,
       "③ ★★ 보정 품질(ECE)을 **교체의 대가**로 잰다")
    ok("R40 ①" in s and ("보정이 좋다고 판별이 좋은 게 아니" in s
                          or "λ 는 신뢰도" in s or "λ ≠ 타당성" in s),
       "③ ★★★ R40 ① — 보정 품질과 판별력은 **다른 것**이라고 못박았다")
    ok("바꾸는 게 이득인가" in s,
       "③ ★★ 묻는 것이 「없앨 수 있나」가 아니라 「바꾸는 게 이득인가」임이 명시돼 있다")
    ok('G3[a] = dict(' in s and 'for a in ("TE", "TT", "A_em", "raw")' in s,
       "③ 대가를 **같은 팔·보정기만 바꿔** 짝지은 차로 잰다")
    ok("prob = 1.0 / (1.0 + np.exp(-np.clip(out, -60, 60)))" in s,
       "③ ★★ ECE 를 **최종(사전확률 시프트까지 끝난) 로짓**의 확률에서 잰다 — "
       "시프트 전 확률을 쓰면 A 팔 ECE 가 raw 와 같게 나온다(스모크가 잡았다)")

    # ── ④ 주 관문은 배포 가능판끼리
    ok('MAIN = ("A_em", "TE")' in s,
       "④ ★★★ 주 관문이 **`TE − A_em`**(둘 다 배포 가능판)이다")
    ok("오라클은 **상한이지 방법이 아니다**" in s,
       "④ ★★ 「오라클은 상한이지 방법이 아니다」가 소스에 있다")
    ok("q4c_pool=dict(raw=0.2097" in s and "A_em=0.1254" in s,
       "④ `A_em`(0.1254) < raw(0.2097) 앵커가 박혀 있다")
    ok('THR[c] = dict(' in s and "max(0.0, NUL[c][" in s,
       "④ ★★ 문턱이 **보정기별** max(0, 영점 상단) 이다")
    ok("for c in CALS:" in s and "NUL[c] = dict(macro=NMc, xrec=NXc)" in s,
       "④ ★★★ 영점을 **보정기별로 따로** 측정한다 — 보정기가 영점을 바꿀 수 있다")
    ok('NUL_OK = all(' in s and 'if NUL_OK else "⚠️ 미결"' in s,
       "④ 영점을 못 쟀으면 G2 를 **읽지 않는다**(R26)")

    # ── ⑤ 분해의 식별 판정 (스모크가 잡은 함정)
    ok("TOTAL_READABLE" in s and "SMALL_INTER" in s,
       "⑤ ★★★ 식별을 **두 조건**(합계가 읽히는가 + 상호작용이 작은가)으로 판정한다")
    ok("abs(inter) < 0.25 * abs(tot)" in s,
       "⑤ ★★★ 상호작용을 **합계 대비**로 잰다 — 「가장 작은 몫」 기준이 아니다")
    ok("항상" in s and "Platt" in s and "구성으로" in s,
       "⑤ ★★★ 왜 「가장 작은 몫」기준이 안 되는지(Platt 에서 테스트 몫이 구성으로 0 이라 "
       "항상 실패)가 소스에 있다 — 스모크가 잡았다")
    ok("test_deploy" in s and "test_adversarial" in s,
       "⑤ ★★ 테스트 반사실을 **배포판**과 **적대적 상한**으로 나눠 저장한다")
    ok("적대적인 쪽을 판정에 쓴 게 F4 의 오류였다" in s,
       "⑤ ★★★ Q4-C 의 F4 오류(적대적 반사실을 판정에 씀)가 명시돼 있다")
    ok("q4c_test_deploy=0.0035" in s and "q4c_test_adv=0.0346" in s,
       "⑤ 두 반사실의 Q4-C 실측(5% vs 54%)이 앵커로 박혀 있다")

    # ── G5 — 전역의 정체
    ok("pooled_bal_of" in s and "WBAL" in s and "sample_weight=WBAL" in s,
       "★★ **레코드 크기 균등 가중** 전역을 따로 잰다(G5)")
    ok("유병률 가중" in s and "판별력" in s,
       "★★★ 전역 이득을 「유병률 가중」과 「판별력」으로 가르는 게 G5 다")
    ok("소급 재해석" in s and "0.2151" in s,
       "★★ Q3 의 +0.2151 소급 재해석이 걸려 있다고 명시됐다")

    # ── 판정 위생
    ok("N_PERM  = 2   if SMOKE else 10" in s,
       "★★ N_PERM 을 Q4-C 의 5 → **10** 으로 올렸다(영점 정밀도가 병목이었다)")
    ok("영점의 정밀도" in s or "영점 정밀도" in s,
       "★ 왜 올렸는지가 소스에 있다")
    ok("def need_super" in s and "관문 문턱과의 거리" in s,
       "★★ 필요표본이 **관문 문턱 기준**이다(R40 ②)")
    ok("d, thr = G2[c][k], THR[c][k]" in s and 'eff = d["mean"] - thr' in s,
       "★★ 실제 호출도 관문 문턱을 쓴다")
    ok("해석 불가" in s and "R41 ②" in s,
       "★ 효과가 0 근처면 필요표본을 **해석 불가**로 표시한다")
    ok('elif no_("G2")' in s and 'no_ = lambda k' in s,
       "★★★ 요약이 **네 갈래**다 — 미결을 기각으로 쓰지 않는다")
    ok("if not NUL_OK:" in cs[-1],
       "★★★ 요약의 첫 갈래가 **영점 미측정**이다(R38 ⑦)")
    ok("def decide(lo, hi, thr, direction)" in s and "np.isfinite(thr)" in s,
       "★★ `decide` 가 문턱이 nan 이면 미결을 낸다")
    ok("접힌 채" in s and "356" in s,
       "★★ 전역은 **접힌 채**로 둔다(상한 · 필요 356 · 가용 56)")
    ok("r != held" in s and "def split_rest(held)" in s,
       "★★ LORO — held-out 이 TRAIN·DEV 어디에도 안 들어간다(R22)")
    ok("def derangement" in s and "np.any(p == np.arange(n))" in s,
       "★ 셔플은 derangement 다")
    ok('raise AssetError(f"{SV5} 없음' in s,
       "★ 자산 없으면 fallback 없이 중단(R16)")
    ok("새 데이터 0" in md() or "새 데이터 0" in s,
       "★ 새 데이터를 안 쓴다는 게 명시돼 있다")
    knob_names = re.findall(r"^\s*(\w+)\s*=\s*[^=].*\bif SMOKE\b", s, flags=re.M)
    ok(set(knob_names) <= {"NB_BOOT", "N_PERM", "N_SHUF"},
       f"★★★ SMOKE 로 값이 바뀌는 이름이 **비용 손잡이뿐**이다({sorted(set(knob_names))})")


# ══════════════════════════════════════════════════════════════════ 동적
def dynamic():
    print("\n[동적] 합성 데이터로 설계 불변식을 **실제로** 검증")
    from sklearn.isotonic import IsotonicRegression
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import average_precision_score

    rng = np.random.RandomState(23)
    n = 1200
    s0 = rng.normal(0.0, 2.0, n)
    y = (rng.rand(n) < 1.0 / (1.0 + np.exp(-s0))).astype(int)

    # ── ⓐ Platt 의 보정 로짓은 원점수의 **아핀 변환**이다
    lr = LogisticRegression(max_iter=3000, C=1e6).fit(s0.reshape(-1, 1), y)
    a, b = float(lr.coef_[0, 0]), float(lr.intercept_[0])
    lg = lambda v: a * np.asarray(v, float) + b
    p_ = lambda v: 1.0 / (1.0 + np.exp(-lg(v)))
    ok(abs(a) > 1e-9,
       f"ⓐ Platt 이 실제로 적합됐다(a={a:.4f}, b={b:.4f})")
    for c in (0.5, 3.0, 12.0, -8.0):
        d = lg(s0 + c) - lg(s0)
        if abs(float(d.std())) > 1e-12:
            break
    ok(all(float((lg(s0 + c) - lg(s0)).std()) < 1e-12 for c in (0.5, 3.0, 12.0, -8.0)),
       "ⓐ ★★★ 상수 시프트가 **상수 시프트인 채 보존**된다 — 큰 시프트(±12)에서도 "
       "차이의 SD < 1e-12")

    def macro1(sc):
        return float(average_precision_score(y, sc))
    ok(all(macro1(lg(s0 + c)) == macro1(lg(s0)) for c in (0.5, 3.0, 12.0, -8.0)),
       "ⓐ ★★★ 따라서 레코드 내 PR-AUC 가 **정확히** 불변이다(부동소수점까지) — G1 이 "
       "검사하는 그것")

    # ── ⓑ 그런데 **확률로 왕복하면 깨진다** — 이 런이 보정 로짓을 직접 내는 이유
    def round_trip(v, eps=1e-6):
        pc = np.clip(p_(v), eps, 1 - eps)
        return np.log(pc) - np.log1p(-pc)
    worst = max(float((round_trip(s0 + c) - round_trip(s0)).std()) for c in (3.0, 12.0, 20.0))
    ok(worst > 1e-14,
       f"ⓑ ★★★ 확률→clip→logit 왕복이면 시프트 후 차이의 SD 가 {worst:.2e} 로 **0 이 "
       f"아니다** — 포화 구간이 clip 에 걸리기 때문. 그래서 보정 로짓을 **직접** 낸다")
    ok(macro1(round_trip(s0 + 20.0)) != macro1(round_trip(s0)),
       "ⓑ ★★ 그리고 큰 시프트에서는 PR-AUC 까지 달라진다 — 항등이 실제로 무너진다")

    # ── ⓒ 등장성은 **계단함수**라 시프트가 동점 구조를 바꾼다
    ir = IsotonicRegression(out_of_bounds="clip", y_min=1e-6, y_max=1 - 1e-6).fit(s0, y.astype(float))
    iso = lambda v: np.clip(ir.predict(np.asarray(v, float)), 1e-6, 1 - 1e-6)
    steps = len(np.unique(ir.predict(s0)))
    leaks = [abs(macro1(iso(s0 + c)) - macro1(iso(s0))) for c in (0.5, 3.0, 12.0)]
    ok(steps < n // 4,
       f"ⓒ 등장성은 계단이다 — 고유 예측값 {steps}개(표본 {n}개)")
    ok(max(leaks) > 1e-6,
       f"ⓒ ★★★ 등장성에서는 상수 시프트가 PR-AUC 를 바꾼다(최대 {max(leaks):.4f}) — "
       f"**이게 Q4-C 가 본 누출**이고 Platt 에는 없다")
    ok(leaks[2] >= leaks[0],
       f"ⓒ ★★ 누출이 시프트 크기를 따라간다({leaks[0]:.4f} → {leaks[2]:.4f}) — Q4-C 실측 "
       f"TT −0.0074 < TE −0.0109 < TS −0.0419 와 같은 구조")

    # ── ⓓ A 팔의 매크로 불변은 **보정기와 무관**하다(G0)
    recs = np.repeat(np.arange(6), 200)
    pis = np.array([0.05, 0.10, 0.18, 0.28, 0.40, 0.55])
    def macro_r(sc):
        return float(np.mean([average_precision_score(y[recs == r], sc[recs == r])
                              for r in range(6)]))
    for nm, cal in (("platt", lg), ("iso", lambda v: np.log(iso(v)) - np.log1p(-iso(v)))):
        base = cal(s0); shifted = base.copy()
        for r in range(6):
            shifted[recs == r] += np.log(pis[r] / (1 - pis[r]))
        ok(macro_r(shifted) == macro_r(base),
           f"ⓓ ★★ G0 — `{nm}` 에서도 A 팔(레코드별 상수 시프트)의 매크로가 **정확히** "
           f"불변이다(Δ {macro_r(shifted)-macro_r(base):.1e})")

    # ── ⓔ 식별 판정 — 「가장 작은 몫」기준의 함정 (스모크가 잡았다)
    def ident_bad(tot, p1t, p1e, p2t, p2e):
        return abs(p1e - p2e) < min(abs(p1t), abs(p1e), abs(p2t), abs(p2e)) and abs(tot) > 1e-9
    def ident_good(tot, tot_lo, tot_mde, inter):
        return (tot_lo > 0.0 and abs(tot) > tot_mde and abs(tot) > 1e-12
                and abs(inter) < 0.25 * abs(tot))
    ok(not ident_bad(0.0638, 0.0292, 0.0000, 0.0638, 0.0000),
       "ⓔ ★★★ 「가장 작은 몫」기준은 **테스트 몫이 정확히 0 일 때 항상 실패**한다 — "
       "정작 그때가 분해가 완벽한 경우다(Platt)")
    ok(ident_good(0.0638, 0.0332, 0.0302, 0.0000),
       "ⓔ ★★★ 합계 대비 기준이면 같은 경우를 **식별됨**으로 읽는다")
    ok(not ident_good(0.0638, 0.0332, 0.0302, 0.0236),
       "ⓔ ★★★ 그리고 Q4-C 의 실제 상호작용(+0.0236 = 합계의 37%)은 **분해 거부**된다 — "
       "F4 가 그걸 안 보고 판정한 게 오류였다")
    ok(not ident_good(0.0017, -0.0040, 0.0058, 0.0000),
       "ⓔ ★★ 합계가 0 을 못 떼면(Q4-C 스모크의 +0.0017) 상호작용이 0 이어도 거부한다")

    # ── ⓕ 배포 반사실 vs 적대적 반사실 (Q4-C 정정)
    m = dict(TT=0.5698, TE=0.5663, TS=0.5353, SS=0.5061)
    dep, adv, tot = m["TT"] - m["TE"], m["TT"] - m["TS"], m["TT"] - m["SS"]
    ok(abs(dep / tot - 0.055) < 0.01 and abs(adv / tot - 0.54) < 0.02,
       f"ⓕ ★★★ 같은 데이터인데 반사실을 바꾸면 테스트 몫이 {dep/tot:.0%}(배포) vs "
       f"{adv/tot:.0%}(적대적) 다 — Q4-C 는 적대적인 쪽을 판정에 썼다")
    ok((m["TE"] - 0.5117) / (m["TT"] - 0.5117) > 0.9,
       f"ⓕ ★★ 배포판 `TE` 가 `TT` 의 raw 대비 이득 중 "
       f"{(m['TE']-0.5117)/(m['TT']-0.5117):.1%} 를 지킨다")

    # ── ⓖ 세 가중은 **다른 것을 잰다** (G5)
    #    ★ 레코드 **크기까지 다르게** 만들어야 전역 ≠ 전역(균등) 이 된다.
    #      크기가 같으면 두 지표가 같은 수를 내서 분해를 시험하지 못한다(스모크가 잡았다).
    g_pis = [0.03, 0.06, 0.12, 0.22, 0.38, 0.55]
    g_sz = [900, 700, 500, 350, 250, 150]
    g_rec = np.concatenate([np.full(g_sz[r], r) for r in range(6)])
    g_y = np.zeros(len(g_rec), int)
    for r in range(6):
        m = np.where(g_rec == r)[0]
        g_y[m[:int(g_pis[r] * len(m))]] = 1
    g0 = np.random.RandomState(5).normal(0, 1, len(g_rec))
    g0[g_y == 1] += 0.7                                  # 레코드 내 판별력(공통)
    g1 = g0.copy()
    for r in range(6):                                   # ★ 사전확률 주입(방법 A)
        g1[g_rec == r] += np.log(g_pis[r] / (1 - g_pis[r]))
    gw = np.zeros(len(g_rec))
    for r in range(6):
        gw[g_rec == r] = 1.0 / g_sz[r]
    pooled = lambda sc: float(average_precision_score(g_y, sc))
    pbal = lambda sc: float(average_precision_score(g_y, sc, sample_weight=gw))
    def xrec(sc):
        v = []
        for i in range(6):
            p = np.sort(sc[(g_rec == i) & (g_y == 1)])
            for j in range(6):
                if i == j:
                    continue
                q = np.sort(sc[(g_rec == j) & (g_y == 0)])
                if not len(p) or not len(q):
                    continue
                lo = np.searchsorted(q, p, "left"); hi = np.searchsorted(q, p, "right")
                v.append((lo + 0.5 * (hi - lo)).sum() / (len(p) * len(q)))
        return float(np.mean(v))
    dp = pooled(g1) - pooled(g0); db = pbal(g1) - pbal(g0); dx = xrec(g1) - xrec(g0)
    ok(dp > 0.05 and dx < 0.0,
       f"ⓖ ★★★ 사전확률 주입이 전역은 **{dp:+.4f}** 올리는데 교차레코드는 **{dx:+.4f}** 로 "
       f"오히려 **내려간다** — 레코드 내 판별력은 하나도 안 건드렸는데도. "
       f"**전역 이득은 「유병률 가중」이지 레코드 간 판별력이 아니다**. "
       f"Q4-C 실측(전역 +0.2398 · 교차 −0.0150)과 같은 구조")
    ok(abs(db - dp) > 1e-6,
       f"ⓖ ★★ 레코드 **크기** 균등 가중도 또 다른 답을 낸다({db:+.4f} vs 전역 {dp:+.4f}) — "
       f"세 지표가 **다른 것을 잰다**는 게 G5 의 요점이다")
    ok(db > 0.05,
       f"ⓖ ★★★ 그런데 크기만 균등하게 해서는 **안 없어진다**({db:+.4f}) — 유병률이 높은 "
       f"레코드는 같은 가중에서도 양성을 더 많이 낸다. **쌍마다 동일 가중(교차레코드)만이** "
       f"유병률 가중을 완전히 뺀다")

    # ── ⓗ LORO 누출 없음
    REC = list(range(6))
    def split_rest(held, every=4):
        rest = sorted([r for r in REC if r != held], key=lambda r: (pis[r], r))
        dv = [r for i, r in enumerate(rest) if i % every == 0]
        return [r for r in rest if r not in set(dv)], dv
    ok(not [h for h in REC if h in split_rest(h)[0] or h in split_rest(h)[1]],
       "ⓗ ★★★ held-out 레코드가 TRAIN·DEV 어디에도 안 들어간다(R22)")


if __name__ == "__main__":
    if not os.path.exists(NB):
        print(f"❌ 노트북이 없다 — {NB}")
        sys.exit(1)
    print("=" * 78)
    print("Q4-D 픽스처 — Platt 시프트 등변성 · 보정 로짓 직접 · 배포 가능판 관문 · "
          "식별 판정 · 전역의 정체")
    print("=" * 78)
    static()
    dynamic()
    print("\n" + "=" * 78)
    print(f"통과 {len(PASS)} · 실패 {len(FAIL)}")
    for f in FAIL:
        print("  ✗ " + f)
    sys.exit(1 if FAIL else 0)
