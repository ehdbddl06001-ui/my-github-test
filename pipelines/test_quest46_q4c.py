#!/usr/bin/env python3
"""Q4-C(`quest46_q4c_burden_train_vs_test`) 픽스처 — 분해 + 지표 교체.

Q4-B(`20260805T0114`)가 주 관문을 통과시켰다(`B_add − A` 매크로 **+0.0582**
[+0.0318, +0.0867]). 남은 게 셋이고 이 런이 그걸 푼다.

**① 두 몫이 안 갈렸다.** Q4-B 의 `B_add_shuf` 는 학습과 테스트 burden 을 **동시에**
뒤섞는다. 그래서 매크로 차 +0.0538 이 「학습 때 올바른 burden 을 쓴 몫」인지 「테스트 때
올바른 burden 을 쓴 몫」인지 갈리지 않는다. **빠진 칸이 `학습 true / 테스트 shuf`** 다.

    이게 왜 중요한가 — Q4-B 실측이 `B_add_em − B_add_oracle` 을 매크로 **−0.0035**,
    전역 **−0.1588** 로 냈다(45배). `add` 모드에서 burden 은 **레코드 내 상수**이고
    선형으로 들어가므로 테스트시 burden 은 그 레코드의 로짓을 **통째로 평행이동**시킬
    뿐 **레코드 내 순위를 못 바꾼다**. 그렇다면 매크로 이득은 **π̂ 를 필요로 하지
    않는다** — Q3 이 막혔던 병목의 우회다. 그런데 Q4-B 는 이걸 증명하지 못했다.

**② 전역 PR-AUC 는 SVDB 에서 구조적으로 검정력이 없다.** Q4-B 의 E3 은 미결이었는데
표본을 늘려서 될 일이 아니다 — 관문 문턱(0) 기준 필요표본이 **80% 에서 356 레코드**인데
채점 가능 상한은 **56** 이다. 유병률이 0.0070~0.5764 로 82배 벌어져 레코드 하나(48)가
양성의 **15.2%** 를 갖는 탓에 √n 이 안 먹는다(MDE 0.1614 → 0.1365, 1.18배뿐).

**③ 배포 가능판끼리가 관문 밖에 있었다.** Q4-B 실측 `A_em` 전역 **0.1254** 는
raw(0.2097)**보다도 나쁘다** — 방법 A 는 배포 불가고 오라클은 상한이지 방법이 아니다.

이 런에서 빠뜨리면 결과가 무효인 것 다섯:
  ① **2×2 가 다 차 있어야** 한다 — TT/TE/TS/ST/SS. `TS`·`ST` 가 없으면 분해가 불가능하다
  ② **F1 이 이 런의 자다**(R35 ①) — **보정 전** `TT` ≡ `TS` 가 정확히 서야 F4 의
     「테스트 몫」을 **등장성 몫**으로 읽을 수 있다. 런타임 검사 + 실패 시 중단
  ③ **전역을 관문에서 내린다** — 대신 **교차레코드 AUROC**(쌍마다 동일 가중). 전역은
     **접되 닫지 않는다**(상한 + 조건부 재개 · R36 ①)
  ④ **필요표본을 관문 문턱 기준으로** — Q4-B 는 영점 평균 기준으로 재서 E3 을
     「n(80%)=32」로 적었다. 관문 기준으론 **356** 이다(R40 ②)
  ⑤ **0 을 쪼개지 않는다** — 합계가 0 과 안 갈리면 배분을 계산하지 않는다. 스모크가
     잡았다: 합계 +0.0017 인데 「학습 몫이다 ✅」가 찍히고 배분이 259%/−159% 였다(R41 ②)
"""
import json
import os
import re
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NB = os.path.join(ROOT, "notebooks", "quest46_q4c_burden_train_vs_test.ipynb")

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

    # ── ① 2×2 가 다 차 있는가
    for nm, tr, te in (("TT", "true", "true"), ("TE", "true", "em"),
                       ("TS", "true", "shuf"), ("ST", "shuf", "true"),
                       ("SS", "shuf", "shuf")):
        ok(f'"{nm}": ("{tr}", "{te}")' in s,
           f"① 2×2 칸 `{nm}` = (학습 {tr} / 테스트 {te})")
    ok("def loro_B(train_src, test_src, shuf_map" in s,
       "① ★★★ 학습 burden 과 테스트 burden 을 **따로** 받는다 — Q4-B 는 하나로 묶여 있었다")
    ok('bmap = BURD if train_src == "true" else shuf_map' in s
       and 'if test_src == "true":' in s,
       "① ★★ 학습용 burden 맵과 테스트용 burden 이 코드에서 **독립적으로** 갈린다")
    ok("동시에" in s and "안 갈렸다" in s,
       "① Q4-B 의 `B_add_shuf` 가 두 몫을 동시에 뒤섞었다는 게 소스에 박혀 있다")
    ok("TRAIN_M = d_macro(\"SS\", \"TS\"" in s and "TEST_M  = d_macro(\"TS\", \"TT\"" in s,
       "① ★★★ 학습 몫 = `TS − SS` · 테스트 몫 = `TT − TS` 로 사전등록돼 있다")
    ok('ALT_TR_M = d_macro("ST", "TT"' in s and 'ALT_TE_M = d_macro("SS", "ST"' in s,
       "① ★★ **대체 경로**(다른 쪽 변수를 고정한 분해)도 잰다 — 가법성 검산")
    ok("additivity_macro" in s and "add_m = " in s,
       "① 가법성 잔차를 명시적으로 계산·저장한다")

    # ── ② F1 이 자다
    ok("want_precal" in s and "pre_[te] = s_te" in s and "보정 전" in s,
       "② ★★★ **보정 전** 점수를 따로 남긴다 — F1 의 항등이 여기서 정확히 선다")
    ok('PRECAL["TT"]' in s and 'PRECAL["TS"]' in s,
       "② F1 은 `TT` 와 `TS` 를 비교한다(테스트시 burden 만 다르다)")
    ok("n_rank_identical" in s and "_rank_avg(PRECAL" in s,
       "② ★★ PR-AUC 뿐 아니라 **순위 벡터 동일성**까지 검사한다")
    ok('raise AssetError(f"F1 실패' in s and "F4 를 읽지 않는다" in s,
       "② ★★★ F1 이 깨지면 **중단**한다 — 안 서면 「테스트 몫 ≈ 0」을 등장성 탓으로 "
       "돌릴 수 없다(R29 ② · R35 ①)")
    ok("d1 >= TOL_IDENT or n_same != NRE" in s,
       "② ★★ 두 조건(허용오차 · 순위 전수 일치)을 **둘 다** 요구한다")
    ok("통째로 평행이동" in s and "레코드 내 상수" in s,
       "② ★★ 왜 항등이 성립하는지(레코드 내 상수 × 선형 = 상수 시프트)가 소스에 있다")

    # ── ③ 전역을 내리고 교차레코드로
    ok('PRIMARY = ("macro", "xrec")' in s and 'REPORT_ONLY = ("pooled",)' in s,
       "③ ★★★ 주 지표가 **매크로 · 교차레코드**다 — **전역은 관문에서 내려갔다**")
    ok("def xrec_matrix(L)" in s and "np.searchsorted(q, p" in s,
       "③ 교차레코드 AUROC 를 레코드 쌍마다 계산한다")
    ok("쌍마다 동일 가중" in s,
       "③ ★★★ **쌍마다 동일 가중** — 전역과 달리 양성 많은 레코드에 안 눌린다")
    ok("if ri == rj:" in s and "continue" in s,
       "③ ★★ 같은 레코드 쌍(대각)은 **교차가 아니므로 제외**한다")
    ok("same = idx[:, None] == idx[None, :]" in s and "(~same)" in s,
       "③ ★★★ 부트스트랩에서 **같은 원본 레코드끼리의 쌍**도 제외한다 — 복원추출로 "
       "같은 레코드가 두 번 뽑히면 그 쌍은 교차가 아니다")
    ok("접는다" in s and "닫는 게 아니" in s and "R36 ①" in s,
       "③ ★★ 전역은 **접는다**(상한 + 조건부 재개), 닫지 않는다")
    ok('CONFIG["F6"] = dict(' in s and "folded=True" in s and "upper=" in s,
       "③ 접힌 상한과 재개 조건을 결과에 저장한다")

    # ── ④ 필요표본을 관문 문턱 기준으로 (Q4-B 오류 정정)
    ok("관문 문턱과의 거리" in s and "영점 평균이 아니라" in s,
       "④ ★★★ `need_super` 의 `eff` 가 **관문 문턱과의 거리**임이 문서화돼 있다")
    ok('("F2 매크로", F2, F2_THR)' in s and '("F3 교차", F3, F3_THR)' in s,
       "④ ★★★ 필요표본 호출이 **관문 문턱**(`*_THR`)을 넘긴다 — Q4-B 는 영점 평균을 넘겼다")
    ok('eff = d["mean"] - thr' in s,
       "④ 효과를 문턱과의 거리로 정의한다")
    ok("q4b_need_E3_gate=356" in s and "「32」" in s,
       "④ ★★ Q4-B 가 잘못 적은 수(32)와 관문 기준 참값(356)이 **둘 다** 박혀 있다")
    ok("R40 ②" in s and "관문이 묻는 질문과 필요표본이 답하는 질문이 달랐다" in s,
       "④ ★★ 오류의 성격(같은 통계로 판정·비교 · R40 ②)이 명시돼 있다")

    # ── ⑤ 0 을 쪼개지 않는다 (스모크가 잡은 함정)
    ok("TOTAL_READABLE" in s,
       "⑤ ★★★ 분해 전에 **쪼갤 합계가 읽히는지** 먼저 본다")
    ok('decide(BOTH_M["lo"], BOTH_M["hi"], 0.0, ">").startswith("✅")' in s
       and 'abs(BOTH_M["mean"]) > BOTH_M["mde"]' in s,
       "⑤ ★★★ 합계가 **0 을 떼고** MDE 보다 커야 배분을 계산한다")
    ok("0 을 쪼개면" in s and "아무 비율이나 나온다" in s,
       "⑤ ★★ 왜 그런지(0 을 쪼개면 아무 비율이나 나온다 · R41 ②)가 소스에 있다")
    ok("tr_share = iso_share = float(\"nan\")" in s,
       "⑤ 못 읽으면 배분을 **nan 으로 두고 찍지 않는다**")
    ok('if not TOTAL_READABLE:\n    f4 = ("⚠️ 미결"' in s,
       "⑤ ★★★ 그 경우 F4 판정이 **미결**이다 — 「학습 몫이다 ✅」를 못 찍는다")
    ok("배분으로 읽지 않는다" in s,
       "⑤ 성분은 보고하되 배분으로 읽지 않는다고 못박았다")

    # ── 문턱 규칙 통일 (Q4-B 오류 정정)
    ok('F2_THR = max(0.0, NM[2])' in s and 'F3_THR = max(0.0, NX[2])' in s,
       "★★★ 문턱 규칙이 **양 관문 모두 max(0, 영점 상단)** 으로 통일됐다 — Q4-B 는 갈렸다")
    ok("양 관문 같은 규칙" in s and "Q4-B 는 갈렸다" in s,
       "★★ 통일했다는 사실과 Q4-B 가 갈렸다는 사실이 로그에 남는다")

    # ── F5 승격
    ok('g_("F5"' in s and "배포 가능판끼리" in s,
       "★★ `TE − A_em` 이 **관문**이다 — Q4-B 는 「참고」로 뒀다")
    ok("오라클은 **상한이지 방법이 아니다**" in s,
       "★★★ 「오라클은 상한이지 방법이 아니다」가 소스에 박혀 있다")
    ok("q4b_pool_Aem=0.1254" in s and "q4b_pool_raw=0.2097" in s,
       "★★ `A_em`(0.1254) < raw(0.2097) 이 앵커로 박혀 있다 — 방법 A 는 배포 불가")
    ok('f5_v = "✅ 지지" if (f5m_v.startswith("✅") and f5x_v.startswith("✅"))' in s,
       "★ F5 는 **두 주 지표 모두** 통과해야 ✅ 다(R40 ②)")

    # ── 판정 위생
    ok("NUL_PER" in s or ("NUL_MAC" in s and "NUL_XM" in s),
       "★★ 영점을 **rep × 레코드**로 보관한다(Q4-B 스모크가 잡은 함정)")
    ok("NUL_OK" in s and 'if NUL_OK else "⚠️ 미결"' in s,
       "★★★ 영점을 못 쟀으면 관문을 **읽지 않는다**")
    ok("미결 ≠ 등가" in s or ("R33 ①" in s and "등가가 아니다" in s),
       "★★ 「미결 ≠ 등가」가 소스에 있다(R29 ① · R33 ①)")
    ok('elif no_("F2")' in s and 'no_ = lambda k' in s,
       "★★★ 요약이 **네 갈래**다 — 미결을 기각으로 쓰지 않는다")
    ok("if not NUL_OK:" in cs[-1],
       "★★★ 요약의 첫 갈래가 **영점 미측정**이다(R38 ⑦)")
    ok("def decide(lo, hi, thr, direction)" in s and "np.isfinite(thr)" in s,
       "★★ `decide` 가 문턱이 nan 이면 **미결**을 낸다 — 0 으로 안 흐른다")
    ok("def _rank_avg" in s and "r[m] = r[m].mean()" in s,
       "★ spearman 이 평균 순위 판본이다")
    ok("def derangement" in s and "np.any(p == np.arange(n))" in s,
       "★ 셔플은 derangement 다")
    ok("r != held" in s and "def split_rest(held)" in s,
       "★★ LORO — held-out 이 TRAIN·DEV 어디에도 안 들어간다(R22)")
    ok('raise AssetError(f"{SV5} 없음' in s,
       "★ 자산 없으면 fallback 없이 중단(R16)")
    ok("새 데이터 0" in md() or "새 데이터 0" in s,
       "★ 새 데이터를 안 쓴다는 게 명시돼 있다")

    # ★ SMOKE 로 **값이 바뀌는** 줄만 본다(`x = a if SMOKE else b`).
    #   CONFIG 에 상수를 기록하는 줄(`dev_every=DEV_EVERY, ..., smoke=SMOKE`)은 손잡이가
    #   아니므로 제외한다 — 안 그러면 거짓양성이 난다.
    knob_names = re.findall(r"^\s*(\w+)\s*=\s*[^=].*\bif SMOKE\b", s, flags=re.M)
    ok(set(knob_names) <= {"NB_BOOT", "N_PERM", "N_SHUF"},
       f"★★★ SMOKE 로 값이 바뀌는 이름이 **비용 손잡이뿐**이다({sorted(set(knob_names))}) — "
       "관문 문턱·설계 상수를 못 건드린다")
    ok({"NB_BOOT", "N_PERM"} <= set(knob_names),
       "★ 비용 손잡이 NB_BOOT·N_PERM 은 실제로 SMOKE 로 줄어든다")
    ok(not re.search(r"^\s*(TOL_IDENT|DEV_EVERY)\s*=.*SMOKE", s, flags=re.M),
       "★★ 설계 상수 TOL_IDENT·DEV_EVERY 는 SMOKE 와 무관하게 고정이다")


# ══════════════════════════════════════════════════════════════════ 동적
def dynamic():
    print("\n[동적] 합성 데이터로 설계 불변식을 **실제로** 검증")
    from sklearn.linear_model import LogisticRegression
    from sklearn.isotonic import IsotonicRegression
    from sklearn.metrics import average_precision_score

    rng = np.random.RandomState(17)
    n_rec, n_beat = 8, 400
    pis = np.array([0.03, 0.07, 0.12, 0.18, 0.26, 0.35, 0.45, 0.55])
    recs, y, X = [], [], []
    for r in range(n_rec):
        tt = rng.rand(n_beat) < pis[r]
        sep = 0.35 + 1.3 * pis[r]
        x = rng.normal(0.0, 1.0, (n_beat, 3))
        x[tt, 0] += sep
        x[:, 1] += 4.0 * pis[r]
        x[tt, 1] += 0.12
        recs += [r] * n_beat; y += tt.astype(int).tolist(); X.append(x)
    recs = np.array(recs); y = np.array(y); X = np.vstack(X)
    b = np.array([pis[r] for r in recs], float)

    F = np.c_[X, b]; mu, sd = F.mean(0), F.std(0) + 1e-9
    lr = LogisticRegression(max_iter=3000, C=1.0).fit((F - mu) / sd, y)
    sc = lambda bv: lr.decision_function((np.c_[X, bv] - mu) / sd)

    def _rank_avg(v):
        v = np.asarray(v, float); o = v.argsort()
        rr = np.empty(len(v), float); rr[o] = np.arange(len(v), dtype=float)
        for u in np.unique(v):
            m = v == u
            if m.sum() > 1:
                rr[m] = rr[m].mean()
        return rr

    def macro(s_):
        return float(np.mean([average_precision_score(y[recs == r], s_[recs == r])
                              for r in range(n_rec)]))

    # ── ⓐ F1 의 근거: 테스트시 burden 은 **레코드 내 상수 시프트**다 (보정 전 · 정확)
    b_shuf = np.array([pis[(r + 3) % n_rec] for r in recs], float)   # derangement 흉내
    s_true, s_shuf = sc(b), sc(b_shuf)
    within = float(np.mean([(s_true - s_shuf)[recs == r].std() for r in range(n_rec)]))
    same_rank = all(np.array_equal(_rank_avg(s_true[recs == r]), _rank_avg(s_shuf[recs == r]))
                    for r in range(n_rec))
    ok(within < 1e-9,
       f"ⓐ ★★★ 보정 **전** — 테스트시 burden 을 바꿔도 차이의 레코드 내 SD 가 "
       f"{within:.2e} 다. **순전한 상수 시프트**")
    ok(same_rank,
       "ⓐ ★★★ 그리고 레코드 내 **순위 벡터가 완전히 동일**하다 — F1 이 검사하는 그것")
    ok(abs(macro(s_true) - macro(s_shuf)) == 0.0,
       f"ⓐ ★★★ 따라서 보정 전 매크로가 **정확히 같다**"
       f"(Δ {macro(s_true)-macro(s_shuf):.1e}) — **테스트시 burden 은 레코드 내 판별에 "
       f"원리적으로 기여하지 않는다**")

    # ── ⓑ 그런데 **보정 후**엔 깨질 수 있다 — 등장성은 계단함수다
    ir = IsotonicRegression(out_of_bounds="clip", y_min=1e-6, y_max=1 - 1e-6)
    ir.fit(s_true, y.astype(float))
    p_true = np.clip(ir.predict(s_true), 1e-6, 1 - 1e-6)
    p_shuf = np.clip(ir.predict(s_shuf), 1e-6, 1 - 1e-6)
    ok(macro(p_true) != macro(p_shuf),
       f"ⓑ ★★★ 보정 **후**엔 달라진다(Δ {macro(p_true)-macro(p_shuf):+.6f}) — 등장성은 "
       f"계단함수라 상수 시프트가 **동점 구조**를 바꾼다. F4 의 「테스트 몫」이 바로 이것")
    # ★ 등장성 몫은 π̂ 오차 크기에 따라 **얼마든지 커질 수 있다** — 작다고 보장된 게 아니다.
    #   (방향에 따라 고유값이 늘 수도 줄 수도 있으므로, 판정은 **매크로 변화폭**으로 한다)
    scan = {}
    for bh in (0.001, 0.01, 0.1, 0.5, 0.9, 0.999):
        p_ = np.clip(ir.predict(sc(np.full(len(b), bh))), 1e-6, 1 - 1e-6)
        scan[bh] = (abs(macro(p_) - macro(p_true)), len(np.unique(p_)))
    worst = max(scan, key=lambda k: scan[k][0])
    best = min(scan, key=lambda k: scan[k][0])
    light = abs(macro(p_true) - macro(p_shuf))
    ok(scan[worst][0] > 5 * light,
       f"ⓑ ★★★ π̂ 오차가 커지면 등장성 몫도 커진다 — b̂={worst} 에서 매크로가 "
       f"**{scan[worst][0]:.4f}** 움직여, 가벼운 셔플의 {light:.4f} 보다 "
       f"{scan[worst][0]/light:.1f}배다. **작다고 보장된 게 아니다**")
    ok(scan[worst][0] > 10 * max(scan[best][0], 1e-6),
       f"ⓑ ★★★ 그리고 **얼마나 어긋났느냐가 크기를 정한다** — 같은 모델·같은 보정인데 "
       f"b̂ 에 따라 {scan[best][0]:.4f}(b̂={best}) ~ {scan[worst][0]:.4f}(b̂={worst}) 로 "
       f"벌어진다. 사전에 상한이 없으므로 **`TS` 로 실측해야** 한다 — 그게 F4 다")
    ok(len({v[1] for v in scan.values()}) > 1,
       f"ⓑ ★★ 예측의 **동점 구조 자체가 바뀐다**(고유값 "
       f"{len(np.unique(p_true))} → {sorted({v[1] for v in scan.values()})}) — "
       f"보정 전엔 정확히 항등인데 보정 후에 새는 통로가 이것이다")

    # ── ⓒ 교차레코드 AUROC — 정의와 전역과의 차이
    def xrec_matrix(sc_):
        P = {r: np.sort(sc_[(recs == r) & (y == 1)]) for r in range(n_rec)}
        N = {r: np.sort(sc_[(recs == r) & (y == 0)]) for r in range(n_rec)}
        M = np.full((n_rec, n_rec), np.nan)
        for a in range(n_rec):
            p = P[a]
            if not len(p):
                continue
            for c in range(n_rec):
                if a == c or not len(N[c]):
                    continue
                q = N[c]
                lo = np.searchsorted(q, p, "left"); hi = np.searchsorted(q, p, "right")
                M[a, c] = float((lo + 0.5 * (hi - lo)).sum() / (len(p) * len(q)))
        return M

    def xrec(M):
        off = ~np.eye(n_rec, dtype=bool)
        return float(M[off & np.isfinite(M)].mean())

    M_t = xrec_matrix(s_true)
    ok(np.all(np.isnan(np.diag(M_t))),
       "ⓒ ★★ 대각(같은 레코드)은 **교차가 아니므로** 계산에서 빠진다")
    ok(0.0 <= xrec(M_t) <= 1.0,
       f"ⓒ 교차레코드 AUROC 가 [0,1] 안이다({xrec(M_t):.4f})")
    # ★ 신호가 전혀 없으면 **0.5** 여야 한다. 레코드 8개짜리 한 번은 표집 오차가 커서
    #   (레코드 하나가 자기 쌍 전부를 끌고 간다) **여러 시드의 평균**으로 편향을 본다.
    nn = [xrec(xrec_matrix(np.random.RandomState(900 + i).normal(0, 1, len(y))))
          for i in range(40)]
    ok(abs(float(np.mean(nn)) - 0.5) < 0.01,
       f"ⓒ ★★★ 신호가 없으면 **0.5** 다(40시드 평균 {np.mean(nn):.4f}) — 눈금에 "
       f"**고정 기준**이 있다. 전역 PR-AUC 는 기저선이 유병률이라 이런 기준이 없고, "
       f"그래서 레코드 구성이 바뀌면 기저선까지 흔들린다")
    ok(float(np.std(nn)) > 0.005,
       f"ⓒ ★★ 다만 한 번의 표집 오차는 작지 않다(시드 SD {np.std(nn):.4f}) — 그래서 "
       f"**영점을 라벨 치환으로 측정**하고 레코드 군집 부트스트랩을 태운다(R26)")
    # 가중이 다르다 — 양성이 많은 레코드가 지분을 독점하지 못한다
    npos = np.array([int(((recs == r) & (y == 1)).sum()) for r in range(n_rec)], float)
    ok(npos.max() / npos.sum() > 1.5 / n_rec,
       f"ⓒ ★★ 전역은 양성 수로 가중된다 — 최대 지분 {npos.max()/npos.sum():.3f} vs "
       f"교차레코드의 균등 지분 {1.0/n_rec:.3f}")

    # ── ⓓ 2×2 분해의 가법성은 **구성으로** 성립한다
    m = {"TT": 0.5698, "TS": 0.5710, "ST": 0.5170, "SS": 0.5160}
    tr_, te_, both_ = m["TS"] - m["SS"], m["TT"] - m["TS"], m["TT"] - m["SS"]
    ok(abs(tr_ + te_ - both_) < 1e-12,
       f"ⓓ ★★★ 학습 몫 + 테스트 몫 = 합계 (잔차 {tr_+te_-both_:.1e}) — **망원 합**이라 "
       f"구성으로 성립한다. 잔차가 0 이 아니면 구현이 틀린 것이다")
    alt_tr, alt_te = m["TT"] - m["ST"], m["ST"] - m["SS"]
    ok(abs(alt_tr + alt_te - both_) < 1e-12,
       "ⓓ ★★ **대체 경로**(ST 를 거치는 분해)도 같은 합계에 도착한다 — 두 경로의 "
       "차이가 곧 **학습×테스트 상호작용**이다")

    # ── ⓔ Q4-B 의 필요표본 오류를 정확히 재현한다
    def need(n, half, eff, p80=True):
        return n * (half / abs(eff)) ** 2 * (2.04 if p80 else 1.0)
    mean_, mde_, nul_ = 0.0773, 0.1365, -0.1807      # Q4-B E3 실측
    n_gate = need(56, mde_, mean_ - 0.0)
    n_null = need(56, mde_, mean_ - nul_)
    ok(round(n_null) == 32,
       f"ⓔ ★★★ **영점 평균** 기준으로 재면 {n_null:.0f} — Q4-B 가 「32」로 적은 그 수다")
    ok(round(n_gate) == 356,
       f"ⓔ ★★★ **관문 문턱(0)** 기준으로 재면 {n_gate:.0f} — 이게 참값이다. "
       f"11배 차이이고, 관문이 미결인데 「표본은 충분하다」가 찍힌 이유다(R40 ②)")
    ok(n_gate > 56 and n_null < 56,
       "ⓔ ★★ 두 기준이 **결론을 반대로** 만든다 — 하나는 「부족」, 하나는 「충분」")

    # ── ⓕ 0 을 쪼개면 아무 비율이나 나온다  ★ 스모크가 잡은 함정
    tot, tr2, te2 = 0.0017, 0.0044, -0.0027          # 스모크 실측
    ok(abs(tr2 / tot) > 2.0 and te2 / tot < -1.0,
       f"ⓕ ★★★ 합계 {tot:+.4f}(≈0)를 쪼개면 배분이 {tr2/tot:.0%} / {te2/tot:.0%} 가 "
       f"된다 — **의미 없는 수**다. 스모크 실측 그대로")

    def f4_verdict(tot_mean, tot_lo, tot_hi, tot_mde):
        readable = (tot_lo > 0.0) and (abs(tot_mean) > tot_mde)
        return "분해함" if readable else "미결"
    ok(f4_verdict(0.0017, -0.0040, 0.0075, 0.0058) == "미결",
       "ⓕ ★★★ 그래서 합계가 0 을 못 떼면 F4 는 **미결**이다 — 배분을 계산하지 않는다")
    ok(f4_verdict(0.0538, 0.0273, 0.0823, 0.0275) == "분해함",
       "ⓕ 반대로 Q4-B 의 실제 이득(+0.0538 [+0.0273,+0.0823])은 **쪼갤 수 있다**")

    # ── ⓖ LORO 누출 없음
    REC = list(range(n_rec))
    def split_rest(held, every=4):
        rest = sorted([r for r in REC if r != held], key=lambda r: (pis[r], r))
        dv = [r for i, r in enumerate(rest) if i % every == 0]
        return [r for r in rest if r not in set(dv)], dv
    ok(not [h for h in REC if h in split_rest(h)[0] or h in split_rest(h)[1]],
       "ⓖ ★★★ held-out 레코드가 TRAIN·DEV 어디에도 안 들어간다(R22)")
    ok(all(len(split_rest(h)[0]) >= 1 and len(split_rest(h)[1]) >= 1 for h in REC),
       "ⓖ 모든 fold 에서 TRAIN·DEV 가 비지 않는다")

    # ── ⓗ 복원추출 부트스트랩에서 같은 원본 레코드 쌍을 빼는가
    r_ = np.random.RandomState(1)
    idx = r_.randint(0, n_rec, n_rec)
    same = idx[:, None] == idx[None, :]
    ok(same.sum() >= n_rec,
       f"ⓗ ★★ 복원추출이라 같은 원본 레코드 쌍이 {same.sum()}개 생긴다"
       f"(대각 {n_rec}개보다 많다) — **전부 빼야** 교차 지표가 오염되지 않는다")
    sub = M_t[np.ix_(idx, idx)]
    keep = (~same) & np.isfinite(sub)
    ok(keep.sum() < sub.size and keep.any(),
       f"ⓗ 제외 후 남는 쌍 {keep.sum()}/{sub.size} — 계산이 성립한다")


if __name__ == "__main__":
    if not os.path.exists(NB):
        print(f"❌ 노트북이 없다 — {NB}")
        sys.exit(1)
    print("=" * 78)
    print("Q4-C 픽스처 — 2×2 분해 · F1 이 자 · 전역을 교차레코드로 · "
          "필요표본은 관문 기준 · 0 을 쪼개지 않는다")
    print("=" * 78)
    static()
    dynamic()
    print("\n" + "=" * 78)
    print(f"통과 {len(PASS)} · 실패 {len(FAIL)}")
    for f in FAIL:
        print("  ✗ " + f)
    sys.exit(1 if FAIL else 0)
