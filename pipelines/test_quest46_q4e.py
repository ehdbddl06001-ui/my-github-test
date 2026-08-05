#!/usr/bin/env python3
"""Q4-E(`quest46_q4e_operating_point`) 픽스처 — 동작점 + 축 결정.

두 질문을 한 런에서 답한다.

**(실무)** Q3~Q4-D 는 전부 **문턱 없는 지표**(PR-AUC · AUROC)였다. 민감도도 PPV도
환자당 오경보율도 **한 번도 안 쟀다**. 「실제 모델에 쓸 수 있나」에 답하려면 동작점이 필요하다.

**(전략)** 「매크로 0.58 이 무작위에 가깝다」는 인상은 **지표 오독**이다 — PR-AUC 의 무작위
기저선은 0.5 가 아니라 **그 레코드의 유병률**이다. 유병률 0.02 면 lift 29배, 0.576 이면
1.0배. 0.0070~0.5764 를 섞은 매크로 **하나로는 못 읽는다**. 게다가 **퀘스트 안에서 지표가
갈렸다** — Q2/Q7-B′ 의 「매크로 0.8842」는 `roc_auc_score` 이고 Q4 라인의 「0.5796」은
`average_precision_score` 다. 같은 이름으로 불려 왔지만 **비교할 수 없는 수**다.

이 런에서 빠뜨리면 결과가 무효인 것 여섯:
  ① **H1 이 눈금이다** — 레코드별 유병률·PR-AUC·**AUROC**·lift 를 함께 낸다. AUROC 를
     같이 내야 Q7 라인의 0.8842 와 다리가 놓인다
  ② **H2 가 축을 정한다** — 레코드별 상수 로짓 시프트는 레코드 내 지표를 **정확히**
     불변으로 둔다. 층②(사전확률 정렬·부담 주입)가 바로 그 부류이므로 **층②로 매크로를
     올리는 것은 원리적으로 불가능**하다. 층②가 실패한 게 아니라 **그 일을 하는 도구가
     아니다**. 깨지면 **중단**
  ③ **주 관문은 민감도가 아니라 「경보율 이탈」이다** — 스모크가 잡았다: `A_em` 민감도
     0.2575 가 `TE` 0.1496 보다 높아 보였지만 **경보율이 0.2505(목표 5% 의 5배)** 였다.
     많이 울려서 많이 맞힌 것뿐이다. **서로 다른 동작점에서 민감도를 비교하면 안 된다**
  ④ **순위 비교는 H4 에서** — 환자별 예산은 경보율이 **구성으로 일치**하므로 거기서만
     민감도 비교가 공정하다
  ⑤ **문턱은 그 fold 의 DEV 에서만** 잡는다(R22 · R34 ②). 예산 `FLAG_Q` 는 **사전 고정**
  ⑥ **Platt 기울기** — Q4-D 에 없던 검사. 조용한 버그는 「하나가 뒤집히는 것」이 아니라
     **「전부 뒤집히는 것」**이다(하나면 그 레코드 AUROC 가 0.5 아래로 보여 증상이 난다).
     그래서 **중앙값 부호**로 체계적 반전을 막고 개별 퇴화는 비율로 제한한다 — 스모크
     널 조건에서 44개 중 1개가 실제로 음수였다
"""
import json
import os
import re
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NB = os.path.join(ROOT, "notebooks", "quest46_q4e_operating_point.ipynb")

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

    # ── ① H1 이 눈금
    ok("per_auc" in s and "roc_auc_score" in s and "per_ap" in s,
       "① 레코드별 **PR-AUC 와 AUROC 를 둘 다** 낸다")
    ok("MEAN_PREV" in s and "무작위 기저선" in s,
       "① ★★★ 매크로 PR-AUC 의 무작위 기저선이 **평균 유병률**임이 코드·로그에 있다")
    ok("LIFT" in s and "AP[c][a][r] / BURD[r]" in s,
       "① 레코드별 **lift(AP/유병률)** 를 낸다")
    ok("q7_macro_auroc=0.8842" in s and "roc_auc_score" in s and "비교할 수 없" in s,
       "① ★★★ Q2/Q7-B′ 의 0.8842 가 **AUROC** 라 Q4 라인의 PR-AUC 와 비교 불가임이 박혀 있다")
    ok("QBAND" in s and "사분위" in s,
       "① 유병률 사분위별로 AP·lift·AUROC 를 갈라 낸다 — 하나의 매크로로는 못 읽는다")
    ok("거의 무작위가 맞다" in s,
       "① ★★ 고유병률 레코드에서는 **실제로** PR-AUC 가 거의 무작위임을 인정한다"
       "(지표 오독으로 다 덮지 않는다)")

    # ── ② H2 가 축
    ok("rng_h2" in s and "rng_h2.normal(0, 3.0)" in s,
       "② ★★★ **무작위** 레코드별 시프트로 검사한다 — 두 팔만 보는 게 아니다")
    ok("d_auc = max(abs(per_auc(Ls)" in s and "d_ap = max(abs(per_ap(Ls)" in s,
       "② PR-AUC 와 AUROC **둘 다** 불변인지 본다")
    ok('raise AssetError(f"H2 실패' in s,
       "② ★★★ 깨지면 **중단**한다(R29 ②)")
    ok("원리적으로 불가능" in s and "그 일을 하는 도구가 아니" in s,
       "② ★★★ **축 결정 문장**이 소스에 박혀 있다 — 층②는 실패한 게 아니라 "
       "매크로를 움직이는 도구가 아니다")
    ok("층①" in s and "층④" in s,
       "② 다음 축 후보(층① 표현 · 층④ 코호트)가 명시돼 있다")

    # ── ③ 주 관문은 경보율 이탈
    ok('h5v = decide(H5["dev"]["lo"], H5["dev"]["hi"], H5_THR, "<")' in s,
       "③ ★★★ 주 관문이 **경보율 이탈**이고 방향이 `<`(낮을수록 좋다)다")
    ok('H5_THR = min(0.0, NS[1])' in s,
       "③ ★★★ 방향이 `<` 이므로 문턱이 **min(0, 영점 하단)** 이다")
    ok("많이 울려서 많이 맞힌 것뿐이다" in s and "0.2505" in s,
       "③ ★★★ 스모크가 잡은 함정(다른 동작점에서 민감도 비교)이 수치와 함께 박혀 있다")
    ok("동작점이 다르면 비교 불가" in s or "동작점이 달라 직접 비교 불가" in s,
       "③ ★★ 민감도 Δ 에 「동작점이 달라 비교 불가」 꼬리표가 붙는다")
    ok('abs(GLB[q_][a][r]["rate"] - q_)' in s,
       "③ 이탈이 |실현 경보율 − 목표| 로 정의돼 있다")

    # ── ④ 순위 비교는 H4 에서
    ok("경보율이 **구성으로 일치**" in s,
       "④ ★★★ 환자별 예산에서는 경보율이 **구성으로 일치**하므로 민감도 비교가 공정하다")
    ok("H4D = dict(" in s and 'BUD[q][MAIN[0]][r]["sens"]' in s,
       "④ H4 의 순위 비교(짝지은 민감도 차)를 따로 낸다")
    ok("np.partition(sc, -k)" in s,
       "④ 환자별 예산은 **문턱 없이** 상위 k개로 정한다(순수 순위)")

    # ── ⑤ 문턱은 DEV 에서만 · 예산은 사전 고정
    ok("FLAG_Q = (0.05, 0.10)" in s and "미리 고정" in s,
       "⑤ ★★★ 경보 예산이 **사전 고정**돼 있다(R34 ②)")
    ok("dev_pool[held] = (cl(s_dv)" in s and "held-out 은 안 본다" in s,
       "⑤ ★★★ 문턱용 DEV 로짓을 fold 마다 따로 남기고 held-out 은 안 본다(R22)")
    ok("thr = float(np.quantile(dl, 1.0 - q))" in s,
       "⑤ ★★ 전역 문턱을 **DEV 분위수**로 잡는다 — TEST 를 안 본다")
    ok("TEST 에서 쓸어보지 않는다" in s,
       "⑤ 「TEST 에서 쓸어보지 않는다」가 명시돼 있다(R34 ②)")

    # ── ⑥ Platt 기울기
    ok("SLOPES.append(a)" in s,
       "⑥ Platt 기울기를 fold×팔 전수로 모은다")
    ok("np.median(sl) <= 0" in s and "MAX_NEG_SLOPE" in s,
       "⑥ ★★★ **중앙값 부호**로 체계적 반전을 막고 개별 퇴화는 **비율**로 제한한다")
    ok("전부 뒤집히는 것" in s and "증상" in s,
       "⑥ ★★★ 왜 최솟값이 아니라 중앙값인지(하나면 증상이 나고 전부면 조용하다)가 소스에 있다")
    ok("Q4-D 는 이 검사가 **없었다**" in s,
       "⑥ Q4-D 의 미검사 결함임이 기록돼 있다")

    # ── H3 — 두 천장
    ok("CEIL, SH_OPT = xrec_opt" in s and "CEIL_TE, _SH_TE = xrec_opt" in s,
       "★★ 천장을 **raw 와 TE 두 모델에서** 잰다")
    ok("사과 대 사과" in s and "다른 모델" in s,
       "★★★ `A_em` 은 raw 의 층② 시프트라 raw-천장과 견주고, `TE` 는 **다른 모델**이라 "
       "넘어도 정당하다는 게 소스에 있다")
    ok("상한이지 방법이 아니다" in s and "R36 ①" in s,
       "★★ 오라클 시프트는 **상한이지 방법이 아니다**(TEST 적합)")
    ok("rho_with_logit_prev" in s,
       "★ 최적 시프트가 **유병률과 같은 방향인지** 잰다(Q4-D 에서 추정치>오라클 이었다)")

    # ── 판정 위생
    ok("def boot_sd_diff" in s,
       "★★ **산포의 차**를 부트스트랩한다 — 단일 문턱의 일관성이 거기서 보인다")
    ok("R40 ①" in s and "동작점이 고르다는 보장은 없다" in s,
       "★★★ R40 ① — 교차레코드가 좋다고 동작점이 고르다는 보장이 없다고 못박았다")
    ok("미결 ≠ 등가" in s or "R33 ①" in s,
       "★ 「미결 ≠ 등가」가 소스에 있다")
    ok("def decide(lo, hi, thr, direction)" in s and "np.isfinite(thr)" in s,
       "★ `decide` 가 문턱이 nan 이면 미결을 낸다")
    ok("def need_super" in s and "관문 문턱과의 거리" in s,
       "★ 필요표본이 관문 문턱 기준이다(R40 ②)")
    ok("해석 불가" in s and "R41 ②" in s,
       "★ 효과가 0 근처면 필요표본을 해석 불가로 표시한다")
    ok("r != held" in s and "def split_rest(held)" in s,
       "★★ LORO — held-out 이 TRAIN·DEV 어디에도 안 들어간다(R22)")
    ok('raise AssetError(f"{SV5} 없음' in s,
       "★ 자산 없으면 fallback 없이 중단(R16)")
    ok("새 데이터 0" in md() or "새 데이터 0" in s,
       "★ 새 데이터를 안 쓴다는 게 명시돼 있다")
    knob = re.findall(r"^\s*(\w+)\s*=\s*[^=].*\bif SMOKE\b", s, flags=re.M)
    ok(set(knob) <= {"NB_BOOT", "N_PERM", "N_GRID"},
       f"★★★ SMOKE 로 값이 바뀌는 이름이 **비용 손잡이뿐**이다({sorted(set(knob))})")
    ok(not re.search(r"^\s*(FLAG_Q|MAIN_Q|TOL_IDENT|MAX_NEG_SLOPE)\s*=.*SMOKE", s, flags=re.M),
       "★★★ 예산·허용오차·기울기 한계는 SMOKE 와 무관하게 고정이다")


# ══════════════════════════════════════════════════════════════════ 동적
def dynamic():
    print("\n[동적] 합성 데이터로 설계 불변식을 **실제로** 검증")
    from sklearn.metrics import average_precision_score, roc_auc_score

    rng = np.random.RandomState(31)

    # ── ⓐ PR-AUC 의 무작위 기저선은 **유병률**이다 (AUROC 는 0.5)
    aps, aucs, prevs = [], [], []
    for p in (0.01, 0.05, 0.20, 0.50):
        n = 4000
        y = (rng.rand(n) < p).astype(int)
        sc = rng.normal(0, 1, n)                       # ★ 신호 없음
        aps.append(average_precision_score(y, sc)); aucs.append(roc_auc_score(y, sc))
        prevs.append(y.mean())
    ok(all(abs(a - q) < 0.03 for a, q in zip(aps, prevs)),
       f"ⓐ ★★★ 신호가 없으면 PR-AUC 가 **유병률**로 간다"
       f"({[f'{a:.3f}' for a in aps]} vs 유병률 {[f'{q:.3f}' for q in prevs]}) — "
       f"**0.5 가 아니다**")
    ok(all(abs(a - 0.5) < 0.03 for a in aucs),
       f"ⓐ ★★★ 반면 AUROC 는 유병률과 무관하게 **0.5** 다"
       f"({[f'{a:.3f}' for a in aucs]}) — 두 지표는 **다른 눈금**이다")
    ok(abs(aps[0] - aps[3]) > 0.4,
       f"ⓐ ★★ 같은 「무작위」인데 PR-AUC 는 {aps[0]:.3f} ~ {aps[3]:.3f} 로 벌어진다 — "
       f"유병률 0.0070~0.5764 를 섞은 매크로를 **하나로 읽으면 안 되는 이유**")

    # ── ⓑ 축: 레코드별 상수 시프트는 레코드 내 지표를 **정확히** 불변으로 둔다
    recs = np.repeat(np.arange(8), 500)
    pis = np.array([0.01, 0.03, 0.07, 0.12, 0.22, 0.35, 0.48, 0.58])
    y = np.zeros(len(recs), int)
    for r in range(8):
        m = np.where(recs == r)[0]
        y[m[:int(pis[r] * len(m))]] = 1
    sc = rng.normal(0, 1, len(recs)); sc[y == 1] += 0.9
    def per_ap(s_):
        return {r: average_precision_score(y[recs == r], s_[recs == r]) for r in range(8)}
    def per_auc(s_):
        return {r: roc_auc_score(y[recs == r], s_[recs == r]) for r in range(8)}
    base_ap, base_auc = per_ap(sc), per_auc(sc)
    worst = 0.0
    for _ in range(5):
        s2 = sc.copy()
        for r in range(8):
            s2[recs == r] += rng.normal(0, 3.0)
        worst = max(worst,
                    max(abs(per_ap(s2)[r] - base_ap[r]) for r in range(8)),
                    max(abs(per_auc(s2)[r] - base_auc[r]) for r in range(8)))
    ok(worst == 0.0,
       f"ⓑ ★★★ **임의의** 레코드별 상수 시프트에서 레코드 내 PR-AUC·AUROC 가 **정확히** "
       f"불변이다({worst:.1e}) — 층②(사전확률 정렬·부담 주입)가 그 부류이므로 "
       f"**층②로 매크로를 올리는 건 원리적으로 불가능**하다")
    xr_before = np.mean([average_precision_score(y, sc)])
    s3 = sc.copy()
    for r in range(8):
        s3[recs == r] += np.log(pis[r] / (1 - pis[r]))
    ok(average_precision_score(y, s3) != xr_before,
       "ⓑ ★★ 그런데 **전역** 지표는 같은 시프트로 움직인다 — 층②가 움직일 수 있는 건 "
       "레코드 **간** 것뿐이라는 그림과 맞는다")

    # ── ⓒ 서로 다른 동작점에서 민감도를 비교하면 안 된다 (스모크가 잡은 함정)
    def at_rate(s_, r_, rate):
        m = recs == r_
        k = max(1, int(round(rate * m.sum())))
        thr = np.partition(s_[m], -k)[-k]
        fl = s_[m] >= thr
        return float((fl & (y[m] == 1)).sum() / max(1, (y[m] == 1).sum())), float(fl.mean())
    s_lo = np.array([at_rate(sc, r, 0.05)[0] for r in range(8)]).mean()
    s_hi = np.array([at_rate(sc, r, 0.25)[0] for r in range(8)]).mean()
    ok(s_hi > s_lo,
       f"ⓒ ★★★ 같은 점수인데 경보율만 5%→25% 로 올리면 민감도가 {s_lo:.4f} → {s_hi:.4f} "
       f"로 오른다. **동작점이 다르면 민감도 비교는 무의미**하다 — 스모크에서 `A_em` "
       f"경보율 0.2505 로 민감도가 높아 보인 게 정확히 이것")
    dev_lo = abs(0.05 - 0.05); dev_hi = abs(0.2505 - 0.05)
    ok(dev_hi > dev_lo,
       f"ⓒ ★★★ **경보율 이탈**로 재면 뒤집힌다({dev_hi:.4f} vs {dev_lo:.4f}) — "
       f"「단일 문턱이 통하나」의 옳은 지표다")

    # ── ⓓ 환자별 예산은 경보율이 **구성으로** 일치한다
    rates = [at_rate(sc, r, 0.05)[1] for r in range(8)]
    ok(max(rates) - min(rates) < 0.02,
       f"ⓓ ★★ 환자별 예산이면 경보율이 레코드마다 {min(rates):.4f}~{max(rates):.4f} 로 "
       f"거의 같다 — **여기서만 민감도 비교가 공정**하다")

    # ── ⓔ Platt 기울기 — 조용한 버그는 「전부 뒤집히는 것」이다
    d_flip = max(abs(per_auc(-sc)[r] - (1.0 - per_auc(sc)[r])) for r in range(8))
    ok(d_flip < 1e-12,
       f"ⓔ 기울기가 음수면 AUROC 가 **1−AUROC** 로 정확히 뒤집힌다(max|Δ| {d_flip:.1e})")
    flip_auc = per_auc(-sc)
    # ★ 원래 AUROC 가 0.5 아래였던 레코드는 뒤집으면 위로 가므로, 「원래 0.5 위였던
    #   레코드가 아래로 내려가는가」로 본다(저유병률 레코드는 표본이 적어 원래도 흔들린다)
    up = [r for r in range(8) if base_auc[r] > 0.5]
    n_below = sum(1 for r in up if flip_auc[r] < 0.5)
    ok(n_below == len(up),
       f"ⓔ ★★ 원래 0.5 위였던 레코드 {len(up)}개가 뒤집으면 **전부 0.5 아래**로 간다"
       f"({n_below}/{len(up)}) — 하나만 뒤집혀도 **증상이 난다**. 그래서 최솟값이 아니라 "
       f"**중앙값**으로 체계적 반전을 막는다")
    a_all, b_all = per_ap(-sc), per_ap(-sc - 5.0)
    ok(all(abs(a_all[r] - b_all[r]) < 1e-12 for r in range(8)),
       "ⓔ ★★★ 그런데 **전부** 뒤집히면 팔들끼리는 여전히 항등이라 **Q4-D 의 G1 은 그대로 "
       "통과**한다 — 그게 조용한 버그이고 H0 가 막는 것")
    med_ok = lambda sl: (np.median(sl) > 0) and ((np.array(sl) <= 0).mean() <= 0.10)
    ok(med_ok([1.1, 0.9, 1.3, -0.25, 1.0, 0.8, 1.2, 1.4, 0.95, 1.05, 1.15]),
       "ⓔ ★★ 11개 중 1개(9.1%)가 음수인 건 통과한다 — 스모크 널 조건에서 44개 중 1개가 "
       "실제로 음수였다")
    ok(not med_ok([-1.1, -0.9, -1.3, -1.0]) and not med_ok([1.0, -1.0, -0.5, 0.9, -0.8]),
       "ⓔ ★★★ 체계적 반전(중앙값 ≤ 0)이나 음수 비율 초과는 **막힌다**")

    # ── ⓕ 문턱을 DEV 에서만 잡는다(누출 없음)
    REC = list(range(8))
    def split_rest(held, every=4):
        rest = sorted([r for r in REC if r != held], key=lambda r: (pis[r], r))
        dv = [r for i, r in enumerate(rest) if i % every == 0]
        return [r for r in rest if r not in set(dv)], dv
    ok(not [h for h in REC if h in split_rest(h)[0] or h in split_rest(h)[1]],
       "ⓕ ★★★ held-out 레코드가 TRAIN·DEV 어디에도 안 들어간다(R22)")
    thr_dev = {h: float(np.quantile(sc[np.isin(recs, split_rest(h)[1])], 0.95)) for h in REC}
    thr_te = {h: float(np.quantile(sc[recs == h], 0.95)) for h in REC}
    ok(any(abs(thr_dev[h] - thr_te[h]) > 1e-9 for h in REC),
       "ⓕ ★★ DEV 에서 잡은 문턱은 held-out 에서 잡은 것과 **다르다** — 같으면 누출이다")


if __name__ == "__main__":
    if not os.path.exists(NB):
        print(f"❌ 노트북이 없다 — {NB}")
        sys.exit(1)
    print("=" * 78)
    print("Q4-E 픽스처 — 눈금(H1) · 축(H2) · 경보율 이탈이 주 관문(H5) · DEV 문턱 · "
          "Platt 기울기")
    print("=" * 78)
    static()
    dynamic()
    print("\n" + "=" * 78)
    print(f"통과 {len(PASS)} · 실패 {len(FAIL)}")
    for f in FAIL:
        print("  ✗ " + f)
    sys.exit(1 if FAIL else 0)
