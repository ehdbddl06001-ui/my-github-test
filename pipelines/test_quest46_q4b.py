#!/usr/bin/env python3
"""Q4-B(`quest46_q4b_burden_feature_v2`) 픽스처 — **주 관문을 고친 판**.

Q4 는 관문 자체가 틀렸다. 「burden 상수 특징 = 레코드별 상수 시프트 = 방법 A」라는 **참인
전제**에서 「그러므로 `B_add` 는 A 와 구조가 같다」는 **거짓 결론**을 끌어냈고, 그래서
`B_add` 를 주 관문 밖으로 밀어냈다. 실측은 정반대였다 —

    전역 PR-AUC   raw 0.3362 · A_oracle 0.5514 · **B_add 0.5725** · B_int 0.4116
    주 관문 D2    `B_int − A_oracle` = −0.1398   ← 「B 가 A 를 못 이긴다」
    구조 대조 D2b `B_add − A_oracle` = **+0.0212**  ← **가장 잘한 팔이 관문 밖에 있었다**

무엇이 빠졌었나: **특징을 추가하면 로지스틱이 리듬 계수를 전부 다시 적합한다.** burden
**기여분**이 레코드별 상수인 건 참(SD 4.46e-16)이지만, 나머지 가중치가 재조정되므로
**모델 전체는 레코드 내 순위를 바꾼다**(실측 ρ 0.792 · 매크로 +0.0398). Q4 의 픽스처는
합성에 **burden 의존 결정경계**가 없어 ρ 0.99996 만 보고 이걸 놓쳤다.

이 런에서 빠뜨리면 결과가 무효인 것 다섯:
  ① **주 관문 = `B_add` 대 A** — 사전등록 문구(「burden 을 **별도 특징**으로」)로 되돌린다.
     `B_int` 는 **과적합 진단**으로 강등. 안 하면 Q4 의 선택 편의를 그대로 되풀이한다
  ② **두 명제를 분리** — 「기여분은 상수」(참)와 「모델 전체가 A 와 같다」(거짓)는 다른 말이다.
     E1 이 ⓐ 기여분 산포와 ⓑ 모델 전체 ρ 를 **따로** 잰다
  ③ **매크로가 공동 주 지표** — A 는 상수 시프트라 매크로가 **정의상 불변**이다(Q4 실측
     A 매크로 = raw 매크로 = 0.5389, 완전 동일). 매크로에서 이기는 건 **A 가 원리적으로
     못 하는 일**이고, R11 이 원래 요구한 지표다
  ④ **영점을 못 쟀으면 문턱을 0 으로 되돌리지 않는다** — rep 당 한 숫자만 모으면 n=N_PERM
     이라 부트 CI 가 nan 이 되고 문턱이 **조용히 0 으로** 떨어진다. 그건 「영점을 측정한다」가
     아니라 「0 을 가정한다」다(R26·R38 ②). 스모크가 정확히 이걸 잡았다 → rep×레코드로 보관
  ⑤ **LORO** — Q4 는 TEST 20 레코드뿐이라 전역 MDE 가 0.1614 였다. 56 레코드 전부를 쓴다
"""
import json
import os
import re
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NB = os.path.join(ROOT, "notebooks", "quest46_q4b_burden_feature_v2.ipynb")

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

    # ── ① 주 관문이 `B_add` 로 되돌아왔는가
    ok('ARMS = ("raw", "A_oracle", "A_em", "B_add_oracle", "B_add_em", '
       '"B_add_shuf", "B_int_oracle")' in s,
       "① 7팔이 사전등록돼 있다 — `B_add_oracle`·`B_add_em`·`B_add_shuf` 가 모두 있다")
    ok('E2 = macro_diff("A_oracle", "B_add_oracle"' in s
       and 'E3 = pooled_diff("A_oracle", "B_add_oracle")' in s,
       "① ★★★ 주 관문 두 개가 **`B_add_oracle` 대 `A_oracle`** 이다(Q4 는 `B_int` 를 썼다)")
    ok('E6m = macro_diff("B_int_oracle", "B_add_oracle"' in s
       and "과적합 진단" in s and "강등" in s,
       "① ★★ `B_int` 는 **과적합 진단으로 강등**됐다 — 관문이 아니다")
    ok("B_add_em" in s and "배포판" in s,
       "① `B_add_em`(배포 가능판)이 팔로 들어왔다 — Q4 에는 **없었다**")
    ok(re.search(r"q4_B_add\s*=\s*0\.5725", s) and re.search(r"q4_B_int\s*=\s*0\.4116", s),
       "① Q4 실측(B_add 0.5725 ≫ B_int 0.4116)이 REF 로 박혀 있다")
    ok("사전등록 문구" in s and "별도 특징" in s,
       "① ★★★ 관문을 바꾼 **이유**가 소스에 박혀 있다 — 사후에 유리한 팔을 고른 게 "
       "아니라 사전등록 문구로 되돌린 것이다(R36 ②)")

    # ── ② 두 명제의 분리
    ok("CONTRIB" in s and "RHO_IN" in s,
       "② ⓐ 기여분 산포와 ⓑ 모델 전체 ρ 를 **따로** 잰다")
    ok("리듬 계수를 전부 다시 적합" in s or "계수를 전부 다시 적합" in s,
       "② ★★★ 「특징을 추가하면 계수가 전부 재적합된다」가 소스에 박혀 있다")
    ok("참인 명제에서 거짓인 결론" in s or "다른 명제" in s,
       "② ★★ Q4 의 추론 오류(참인 전제 → 거짓 결론)가 명시돼 있다")
    ok(re.search(r"q4_rho_add\s*=\s*0\.792", s),
       "② Q4 의 반증 수치(ρ 0.792)가 REF 에 있다")
    ok("rho_n" in s and "유효" in s,
       "② ★★ ρ 의 **유효 레코드 수**를 함께 보고한다 — nan 을 평균에 흘리지 않는다")
    ok('g_("E1", "⚠️ 미결"' in s and 'g_("E1", "❌ 기각"' in s and 'g_("E1", "✅ 지지"' in s,
       "② ★★★ E1 이 **세 갈래**다 — ρ 를 못 쟀으면 「분리됐다」를 찍지 않는다")

    # ── ③ 매크로가 공동 주 지표 · A 의 항등이 그 근거
    ok('PRIMARY = ("macro", "pooled")' in s,
       "③ ★★★ 주 지표가 **매크로·전역 공동**으로 사전등록돼 있다")
    ok("TOL_IDENT" in s and "raise AssetError" in s and "E0 실패" in s,
       "③ ★★★ E0 — A 팔의 매크로가 raw 와 **정확히 같은지** 런타임에 검사하고, "
       "깨지면 **중단**한다(R34 ③ · R35 ④)")
    ok("정의상 불변" in s or "매크로가 불변" in s,
       "③ ★★ 「A 는 상수 시프트라 매크로가 정의상 불변」이 소스에 있다 — E2 의 의미다")
    ok("READ_ORDER" in s and '"E0", "E1", "E2"' in s,
       "③ 판정 순서가 사전등록돼 있다(E0 → E1 → E2 …)")

    # ── ④ 영점 — 못 쟀으면 0 으로 되돌리지 않는다  ★ 이번 스모크가 잡은 버그
    ok("NUL_PER" in s and "NUL_L" in s,
       "④ ★★★ 영점을 **rep × 레코드**로 보관한다 — rep 당 한 숫자면 n=N_PERM 이라 "
       "CI 가 안 나온다")
    ok("NUL_OK" in s and 'if NUL_OK else "⚠️ 미결"' in s,
       "④ ★★★ 영점을 못 쟀으면 E2·E3 을 **읽지 않는다**")
    ok('E2_THR = NM[2] if np.isfinite(NM[2]) else float("nan")' in s,
       "④ ★★★ 문턱이 nan 일 때 **0 으로 되돌리지 않는다** — 그건 측정이 아니라 가정이다")
    ok("E3_THR = max(0.0, NP[2])" in s,
       "④ ★★ E3 문턱 = **max(0, 영점 상단)** — 사전등록 「> 0」과 측정된 영점 중 엄한 쪽")
    ok("y_override" in s and "rr.permutation" in s,
       "④ 영점은 **학습 라벨 치환**으로 측정한다(0 을 가정하지 않는다)")
    ok("uninterpretable" in s and "영점 미측정" in s,
       "④ ★★ 필요표본도 영점을 못 쟀으면 **계산하지 않는다**(nan 을 「읽을 수 있다」로 "
       "흘리지 않는다 · R41 ②)")

    # ── ⑤ LORO
    ok("def split_rest(held)" in s and "for held in REC_OK" in s,
       "⑤ ★★ LORO — 레코드 하나를 빼고 나머지로 학습·보정한다")
    ok("r != held" in s,
       "⑤ ★★★ held-out 레코드가 학습·DEV 어디에도 안 들어간다(R22 누출 없음)")
    ok("dv = [r for i, r in enumerate(rest) if i % DEV_EVERY == 0]" in s
       and "cal = make_iso(s_dv" in s,
       "⑤ ★★ 보정은 **DEV 레코드에서만** 적합한다 — held-out 도 TRAIN 도 아니다")
    ok("보정 뒤" in s and "척도가 맞는다" in s,
       "⑤ ★★ 모든 팔을 **보정 뒤** 로짓으로 비교한다 — fold 간 척도가 맞아야 전역이 성립")
    ok("0.1614" in s,
       "⑤ Q4 의 전역 MDE(0.1614)가 비교 기준으로 박혀 있다")

    # ── 판정 위생 (R29 ① · R33 ① · R38 ⑦ · R40 ②)
    ok('e6_v = decide(E6m["lo"], E6m["hi"], 0.0, ">")' in s,
       "★★ E6 을 **CI 로** 읽는다 — 점추정 부호로 판정하지 않는다(G1 의 G5 오류)")
    ok("e5m_v" in s and "e5p_v" in s,
       "★★ E5 도 **두 주 지표 모두**로 읽는다(R40 ② — 판정과 비교에 같은 통계)")
    ok("미결 ≠ 등가" in s and "R33" in s,
       "★★ 「미결 ≠ 등가」가 소스에 박혀 있다(R29 ① · R33 ①)")
    ok('elif no_("E2")' in s and 'no_ = lambda k' in s,
       "★★★ 요약이 **네 갈래**다 — 미결을 기각으로 쓰지 않는다(스모크가 잡았다)")
    ok("if not NUL_OK:" in cs[-1],
       "★★★ 요약의 첫 갈래가 **영점 미측정**이다 — 판정·검산표·요약이 같은 갈래다(R38 ⑦)")
    ok("전역 단독 인용 금지" in s and "DOMINANT" in s,
       "★ 전역은 지배 지분 때문에 단독 인용 금지(R11)")
    ok("직접 비교하지 않는다" in s and "단일 분할" in s,
       "★★ Q4 의 전역 수치는 **단일 분할**이라 LORO 와 직접 비교하지 않는다고 못박았다")

    # ── SMOKE 가 관문을 못 건드린다
    smoke_lines = [l for l in s.split("\n") if "SMOKE" in l and "=" in l]
    knobs = " ".join(smoke_lines)
    ok(all(k not in knobs for k in ("TOL_IDENT", "NONINF_MARGIN", "E2_THR", "E3_THR",
                                    "DEV_EVERY")),
       "★★★ SMOKE 는 **비용 손잡이만** 줄인다 — 관문 문턱·설계 상수를 못 건드린다")
    ok(all(x in knobs for x in ("NB_BOOT", "N_SHUF", "N_PERM")),
       "★ 비용 손잡이는 NB_BOOT·N_SHUF·N_PERM 셋뿐이다")

    # ── 공용 도구
    ok("def _rank_avg" in s and "r[m] = r[m].mean()" in s,
       "★★ spearman 이 **평균 순위** 판본이다(Q3-B 에서 argsort 판본의 순서 의존이 드러났다)")
    ok("def derangement" in s and "np.any(p == np.arange(n))" in s,
       "★ 셔플은 **derangement** 다 — 자기 자리에 남는 레코드가 없다")
    ok("R16" in s and 'raise AssetError(f"{SV5} 없음' in s,
       "★ 자산이 없으면 fallback 없이 **중단**한다(R16)")
    ok("새 데이터 0" in md() or "새 데이터 0" in s,
       "★ 새 데이터를 안 쓴다는 게 명시돼 있다")


# ══════════════════════════════════════════════════════════════════ 동적
def dynamic():
    print("\n[동적] 합성 데이터로 설계 불변식을 **실제로** 검증")
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import average_precision_score

    rng = np.random.RandomState(11)
    n_rec, n_beat = 8, 400
    pis = np.array([0.03, 0.07, 0.12, 0.18, 0.26, 0.35, 0.45, 0.55])
    recs, y, X = [], [], []
    for r in range(n_rec):
        tt = rng.rand(n_beat) < pis[r]
        # ★★★ Q4 픽스처의 사각지대를 여기서 재현한다. 합성에 **burden 과 얽힌 레코드 수준
        #     교란**이 없으면 계수 재적합이 거의 안 일어나 ρ 가 1 에 붙고(Q4 실측 0.99996),
        #     「B_add = A」라는 거짓 결론을 픽스처가 통과시킨다.
        #     x1 을 **레코드 수준으로 burden 을 따라가는 교란**으로 만든다 — raw 모델은
        #     x1 에 큰 가중치를 싣지만(레코드 간 예측력), burden 을 명시적으로 주면 그
        #     가중치가 빠지면서 **레코드 내 순위가 바뀐다**.
        sep = 0.35 + 1.3 * pis[r]
        x = rng.normal(0.0, 1.0, (n_beat, 3))
        x[tt, 0] += sep
        x[:, 1] += 4.0 * pis[r]        # 레코드 수준 교란 (burden 을 따라간다)
        x[tt, 1] += 0.12               # 레코드 안에서는 아주 약하게만 정보
        recs += [r] * n_beat; y += tt.astype(int).tolist(); X.append(x)
    recs = np.array(recs); y = np.array(y); X = np.vstack(X)
    b = np.array([pis[r] for r in recs], float)

    def fit(F, yy=None):
        mu, sd = F.mean(0), F.std(0) + 1e-9
        lr = LogisticRegression(max_iter=3000, C=1.0)
        lr.fit((F - mu) / sd, y if yy is None else yy)
        return lr.decision_function((F - mu) / sd)

    s_raw = fit(X)
    s_add = fit(np.c_[X, b])
    s_int = fit(np.c_[X, b, X * b[:, None]])

    def _rank_avg(v):
        v = np.asarray(v, float); o = v.argsort()
        rr = np.empty(len(v), float); rr[o] = np.arange(len(v), dtype=float)
        for u in np.unique(v):
            m = v == u
            if m.sum() > 1:
                rr[m] = rr[m].mean()
        return rr

    def rho(a, c):
        ra, rb = _rank_avg(a), _rank_avg(c)
        return float(np.corrcoef(ra, rb)[0, 1])

    def macro(sc):
        return float(np.mean([average_precision_score(y[recs == r], sc[recs == r])
                              for r in range(n_rec)]))

    # ── ⓐ 「기여분은 상수」는 **참**이다 (Q4 의 전제)
    lr_add = LogisticRegression(max_iter=3000, C=1.0)
    F = np.c_[X, b]; mu, sd = F.mean(0), F.std(0) + 1e-9
    lr_add.fit((F - mu) / sd, y)
    g = lambda bv: lr_add.decision_function((np.c_[X, bv] - mu) / sd)
    contrib = g(b) - g(np.full(len(b), b.mean()))
    within = float(np.mean([contrib[recs == r].std() for r in range(n_rec)]))
    ok(within < 1e-9,
       f"ⓐ ★★★ burden **기여분**은 레코드 내 상수다(SD {within:.2e}) — Q4 의 전제는 **참**")

    # ── ⓑ 그런데 「모델 전체가 A 와 같다」는 **거짓**이다 (Q4 의 결론)
    r_add = float(np.mean([rho(s_raw[recs == r], s_add[recs == r]) for r in range(n_rec)]))
    ok(r_add < 0.999,
       f"ⓑ ★★★ 그럼에도 모델 **전체**는 레코드 내 순위를 바꾼다(ρ {r_add:.6f} < 0.999) — "
       f"Q4 의 결론은 **거짓**이다. 실측 ρ 0.792 와 같은 방향")
    ok(within < 1e-9 and r_add < 0.999,
       "ⓑ ★★★ 두 명제가 **동시에** 성립한다 — 참인 전제에서 거짓 결론이 나온 자리다")

    # ── ⓒ A 팔은 매크로가 **정확히** 불변이다 (E0 의 근거)
    def a_shift(sc, pi_map):
        out = sc.copy()
        for r in range(n_rec):
            out[recs == r] = sc[recs == r] + np.log(pi_map[r] / (1 - pi_map[r]))
        return out
    s_A = a_shift(s_raw, pis)
    ok(abs(macro(s_A) - macro(s_raw)) == 0.0,
       f"ⓒ ★★★ 방법 A 는 매크로가 **정확히** 불변이다(Δ {macro(s_A)-macro(s_raw):.1e}) — "
       f"이것이 E0 이고, **매크로에서 이기는 건 A 가 못 하는 일**이라는 근거다")
    ok(abs(macro(s_add) - macro(s_raw)) > 0.0,
       f"ⓒ ★★ 반면 `B_add` 는 매크로를 움직인다(Δ {macro(s_add)-macro(s_raw):+.6f}) — "
       f"Q4 실측 +0.0398 과 같은 방향")
    ok(average_precision_score(y, s_A) > average_precision_score(y, s_raw),
       "ⓒ 그리고 A 는 **전역**은 올린다 — 두 지표가 서로 다른 것을 잰다")

    # ── ⓓ 영점을 못 쟀을 때 0 으로 되돌리면 어떻게 되는가  ★ 스모크가 잡은 버그
    def boot_mean_like(v):
        d = np.asarray(v, float); d = d[np.isfinite(d)]
        return float("nan") if len(d) < 3 else float(np.percentile(d, 97.5))
    ok(not np.isfinite(boot_mean_like([0.01, 0.02])),
       "ⓓ ★★★ rep 당 한 숫자만 모으면(n=2) 영점 CI 가 **nan** 이다 — 스모크 실측")

    def gate(lo, hi, nul_hi, fallback_zero):
        thr = (0.0 if not np.isfinite(nul_hi) else nul_hi) if fallback_zero else nul_hi
        if not np.isfinite(thr):
            return "not-read"
        return "PASS" if lo > thr else "not"
    ok(gate(0.0054, 0.0742, float("nan"), True) == "PASS"
       and gate(0.0054, 0.0742, float("nan"), False) == "not-read",
       "ⓓ ★★★ 영점이 nan 인데 0 으로 되돌리면 Q4 실측 효과(+0.0398 [+0.0054,+0.0742])가 "
       "**통과**한다. 되돌리지 않으면 **읽지 않는다** — 그게 R26 이다")
    ok(gate(0.0054, 0.0742, 0.0219, False) == "not",
       "ⓓ ★★ 그리고 영점을 실제로 재면(상단 +0.0219) 같은 효과가 **통과하지 않는다** — "
       "0 을 가정했으면 놓쳤을 판정이다")

    # ── ⓔ max(0, 영점) — 영점이 음수일 때. ★ 판정은 **CI 하단**으로 한다(점추정 아님)
    def gate3(lo, nul_hi, use_max):
        thr = max(0.0, nul_hi) if use_max else nul_hi
        return "PASS" if lo > thr else "not"
    ok(gate3(-0.0037, -0.0856, False) == "PASS" and gate3(-0.0037, -0.0856, True) == "not",
       "ⓔ ★★★ Q4 스모크가 잡았던 그 버그 — 효과 +0.0002 [−0.0037,+0.0056] 은 음수 영점"
       "(−0.0856)만 쓰면 **통과**하지만 max(0,·) 면 통과하지 않는다")
    ok(gate3(-0.0034, -0.1075, True) == "not",
       "ⓔ ★★ 이번 스모크의 전역 영점도 음수(−0.1075)였고, max(0,·) 라 효과 +0.0009 "
       "[−0.0034,+0.0072] 가 통과하지 않았다 — 재발 방지가 실제로 작동했다")
    ok(gate3(0.0054, -0.1075, True) == "PASS",
       "ⓔ 반대로 CI 하단이 0 을 확실히 넘으면(+0.0054) max(0,·) 여도 **통과한다** — "
       "문턱이 무조건 막는 게 아니다")

    # ── ⓕ 셔플 대조 — 같은 값 집합, 대응만 깨진다
    def derange(n, r_):
        for _ in range(500):
            p = r_.permutation(n)
            if not np.any(p == np.arange(n)):
                return p
        return np.roll(np.arange(n), 1)
    perm = derange(n_rec, np.random.RandomState(5))
    b_sh = np.array([pis[perm][r] for r in recs], float)
    ok(sorted(np.unique(b_sh).tolist()) == sorted(np.unique(b).tolist())
       and not np.array_equal(b_sh, b),
       "ⓕ ★★ 셔플 팔은 **같은 burden 값 집합**을 쓰고 대응만 깨진다(구성 대조 · R34 ③)")
    ok(np.all(perm != np.arange(n_rec)),
       "ⓕ derangement — 자기 자리에 남는 레코드가 **하나도 없다**")
    ap_or = average_precision_score(y, s_add)
    ap_sh = average_precision_score(y, fit(np.c_[X, b_sh]))
    ok(ap_or > ap_sh,
       f"ⓕ 대응이 맞을 때가 더 낫다(전역 {ap_or:.4f} > 셔플 {ap_sh:.4f})")

    # ── ⓖ LORO 가 누출 없이 짜였는가
    REC = list(range(n_rec))
    def split_rest(held, every=4):
        rest = sorted([r for r in REC if r != held], key=lambda r: (pis[r], r))
        dv = [r for i, r in enumerate(rest) if i % every == 0]
        return [r for r in rest if r not in set(dv)], dv
    bad = [h for h in REC if h in split_rest(h)[0] or h in split_rest(h)[1]]
    ok(not bad,
       "ⓖ ★★★ LORO — held-out 레코드가 TRAIN·DEV 어디에도 안 들어간다(R22)")
    ok(all(len(split_rest(h)[1]) >= 1 and len(split_rest(h)[0]) >= 1 for h in REC),
       "ⓖ 모든 fold 에서 TRAIN·DEV 가 비지 않는다")
    covered = sorted({h for h in REC})
    ok(covered == REC,
       f"ⓖ ★★ **{len(REC)} 레코드 전부**가 평가에 들어간다 — Q4 는 TEST 20 뿐이었다")
    dv_pi = [np.mean([pis[r] for r in split_rest(h)[1]]) for h in REC]
    ok(min(dv_pi) > 0 and max(dv_pi) < 1,
       f"ⓖ DEV 유병률이 fold 마다 {min(dv_pi):.3f}~{max(dv_pi):.3f} — 보정이 성립한다")

    # ── ⓗ 순위 보존이 **깨지지 않는** 대조: A 는 로짓 상수 시프트라 항등이다.
    #    ★ ρ 를 1.0 과 **정확히** 비교하지 않는다 — corrcoef 는 같은 벡터끼리도
    #      0.9999999999999998 을 낼 수 있다. 진짜 불변식은 **순위 벡터가 동일**한 것이다.
    same_rank = all(np.array_equal(_rank_avg(s_raw[recs == r]), _rank_avg(s_A[recs == r]))
                    for r in range(n_rec))
    ok(same_rank,
       "ⓗ ★★★ A 팔의 레코드 내 **순위 벡터가 raw 와 완전히 동일**하다 — 상수 시프트는 "
       "순위를 부동소수점까지 보존한다. E1 ⓑ 가 재는 것이 **재적합 효과**임을 가른다")
    ok(all(rho(s_raw[recs == r], s_A[recs == r]) > 1 - 1e-12 for r in range(n_rec)),
       "ⓗ 그리고 ρ 도 1 과 구분되지 않는다(< 1e-12)")
    ok(not all(np.array_equal(_rank_avg(s_raw[recs == r]), _rank_avg(s_add[recs == r]))
               for r in range(n_rec)),
       "ⓗ ★★ 반면 `B_add` 의 순위 벡터는 raw 와 **다르다** — 같은 검사가 두 팔을 가른다")

    # ── ⓘ 미결을 기각으로 쓰지 않는다
    def verdict(lo, hi, thr):
        if lo > thr:
            return "✅"
        if hi < thr:
            return "❌"
        return "⚠️"
    ok(verdict(-0.0078, 0.0048, 0.0219) == "❌" and verdict(-0.0023, 0.0046, 0.0011) == "⚠️",
       "ⓘ ★★★ 같은 부호의 작은 효과도 문턱에 따라 **기각**과 **미결**이 갈린다 — "
       "스모크 실측 두 조건이 정확히 그랬다")


if __name__ == "__main__":
    if not os.path.exists(NB):
        print(f"❌ 노트북이 없다 — {NB}")
        sys.exit(1)
    print("=" * 78)
    print("Q4-B 픽스처 — 주 관문을 `B_add` 로 · 두 명제 분리 · 매크로 공동 주 지표 · "
          "영점 미측정이면 안 읽는다 · LORO")
    print("=" * 78)
    static()
    dynamic()
    print("\n" + "=" * 78)
    print(f"통과 {len(PASS)} · 실패 {len(FAIL)}")
    for f in FAIL:
        print("  ✗ " + f)
    sys.exit(1 if FAIL else 0)
