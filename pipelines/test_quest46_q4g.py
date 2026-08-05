#!/usr/bin/env python3
"""Q4-G(`quest46_q4g_budget_ceiling_burden`) 픽스처 — 예산 상한 + 부담 추정 재설계.

Q4-F(`20260805T0449`)가 처방을 확정하고(J2 ✅ 0.0e+00 — 예산 방식에서 층② 제거 가능)
문제 셋을 드러냈다.

  ① **예산 상한을 안 봤다** — 레코드 48 은 S 가 1818 개인데 예산이 190 개라 **최대 가능
     민감도가 0.104** 다. 그런데 J5 는 이걸 `#38`(상한 0.673 인데 0.0088 = 진짜 모델 실패)과
     **한 표에 섞어** 「민감도~유병률 상관 −0.5697」로 보고했다
  ② **AUROC 가 이 국면의 잘못된 요약** — `#38` 은 AUROC **0.8479** 인데 상위 6% 로 양성의
     **0.9%** 만 잡는다. AUROC 는 전체 순위를 보고 예산 국면은 **최상위 꼬리**만 쓴다
  ③ **π̂ 가 무정보** — 네 추정기 전부 ρ(π̂,π*) 가 0 또는 음수(−0.0019 ~ −0.0684)이고
     레코드 48 에서 15~58배 과소추정한다. **왜**: 넷 다 **박동별 보정 확률의 함수**이고,
     보정은 저유병률 DEV 에서 적합되므로 **확률 눈금이 낮은 쪽에 고정**된다

이 런에서 빠뜨리면 결과가 무효인 것 다섯:
  ① **상한 min(1, k/S) 과 달성률** — 없으면 「민감도 0.02」가 모델 실패인지 예산 부족인지
     구분이 안 된다. Q4-F 가 정확히 그 오류를 냈다
  ② **recall@k 를 AUROC 와 나란히** — AUROC 가 상위 꼬리를 대변하지 못함을 실측한다(R40 ①)
  ③ **기록 수준 회귀** — 박동별 확률 경로를 **우회**한다. 그게 이 런의 새 팔이다
  ④ **오라클 배분은 `k ∝ π*` 가 아니라 탐욕 물채우기** — 평균 민감도는 레코드를 **동등
     가중**하므로 S 가 작은 레코드의 한 칸이 더 값지다. 스모크가 잡았다(`k ∝ π*` 가
     균등보다 **나빴다**: −0.1233)
  ⑤ **총 예산을 균등 배분과 같게** 유지한다(R36 ②)
"""
import json
import os
import re
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NB = os.path.join(ROOT, "notebooks", "quest46_q4g_budget_ceiling_burden.ipynb")

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


def static():
    print("\n[정적] 노트북 소스 불변식")
    s = src()
    cs = cells()

    # ── ① 상한과 달성률
    ok('ceil=float(min(1.0, k / max(1, int(yy.sum()))))' in s,
       "① ★★★ 예산 **상한 min(1, k/S)** 이 코드로 계산된다")
    ok('R1[r]["ach"] = R1[r]["sens"] / R1[r]["ceil"]' in s,
       "① ★★★ **달성률 = 민감도/상한** 이 계산된다")
    ok("capped = [r for r in REC_OK if R1[r][\"ceil\"] < 0.999]" in s,
       "① 상한에 걸린 레코드를 **세어서** 보고한다")
    ok("모델이 완벽해도" in s,
       "① ★★ 「모델이 완벽해도 상한을 못 넘는다」가 소스에 있다")
    ok("한 표에 섞" in s and "0.5697" in s,
       "① ★★★ Q4-F J5 의 오류(두 실패를 섞음)가 수치와 함께 박혀 있다")
    ok("예산 부족" in s and "모델 실패" in s,
       "① ★★ 두 진단을 **레코드마다 라벨링**한다")

    # ── ② AUROC 는 이 국면의 요약이 아니다
    ok("rho_auc_ach" in s and "rho_lift_ach" in s,
       "② ★★★ ρ(AUROC, 달성률)과 ρ(lift, 달성률)을 **둘 다** 낸다")
    ok("hi_auc_lo_ach" in s and 'AUC[r] > 0.85 and R1[r]["ach"] < 0.5' in s,
       "② ★★★ **AUROC 높은데 달성률 낮은 레코드**를 직접 센다")
    ok("최상위 꼬리" in s and "R40 ①" in s,
       "② ★★ 왜 AUROC 가 부적절한지(전체 순위 vs 최상위 꼬리)가 소스에 있다")
    ok("0.8479" in s and "0.9%" in s,
       "② Q4-F 의 반례(#38 AUROC 0.8479 · 상위 6% 로 0.9%)가 앵커로 박혀 있다")

    # ── ③ 기록 수준 회귀
    ok("def rec_feats(r)" in s and "Ridge(alpha=RIDGE_A)" in s,
       "③ ★★★ 기록 수준 특징 + ridge 회귀가 구현돼 있다")
    ok("박동별 보정 확률을 안 거친다" in s or "박동별 확률을 안 거친다" in s,
       "③ ★★★ **박동별 확률 경로를 우회한다**는 게 소스에 있다")
    ok("확률 눈금" in s and "낮은 쪽에 고정" in s,
       "③ ★★★ 기존 넷이 왜 ρ≈0 인지(확률 눈금 고정)가 소스에 있다")
    ok("fit_r = tr_r + dv_r" in s and "held-out 을 뺀" in s,
       "③ ★★★ 회귀를 **held-out 을 뺀 레코드에서만** 적합한다(R22)")
    ok('PI_EST = ("em", "mean_p", "bbse", "count", "reg")' in s and 'NEW_EST = "reg"' in s,
       "③ 새 팔이 기존 넷과 **같은 표에서** 비교된다")
    ok("boot_rho" in s and "rho_lo" in s,
       "③ ★★ ρ 에 **CI** 를 붙인다(점추정으로 판정하지 않는다)")
    ok("N_PERM_REG" in s and "ridge 재적합뿐이라 싸다" in s,
       "③ ★★ 회귀 영점은 싸므로 reps 를 크게 잡는다(스모크에서 n<3 이라 nan 이 났다)")

    # ── ④ 오라클은 탐욕 물채우기
    ok("def greedy_oracle(total)" in s,
       "④ ★★★ 오라클 배분이 **탐욕 물채우기**로 구현돼 있다")
    ok("총 recall" in s and "평균 민감도" in s and "아니다" in s,
       "④ ★★★ 「`k ∝ π*` 는 총 recall 의 최적이지 평균 민감도의 최적이 **아니다**」가 있다")
    ok("(1.0 / max(1, NS_[r])) / pos[0]" in s and "import heapq" in s,
       "④ ★★★ 한계 이득이 **(1/S_r) / (다음 양성까지의 비용)** 이다 — 레코드 동등 가중과 "
       "**접두사 제약**을 둘 다 반영한다")
    ok("실현 불가능" in s and "0.3844" in s,
       "④ ★★★ 첫 판본의 오류(양성 칸만 골라 담아 **실현 불가능**한 배분이 됐다)가 수치와 "
       "함께 박혀 있다")
    ok("-0.1233" in s or "−0.1233" in s,
       "④ 스모크가 잡은 반례(`k ∝ π*` 오라클이 균등보다 나빴다)가 박혀 있다")
    ok("접두사 제약을 지키므로" in s and "실현 가능" in s,
       "④ ★★ 접두사 제약을 지키므로 **실현 가능한** 배분임이 적혀 있다")

    # ── ⑤ 총 예산 고정 · 판정 위생
    ok("TOT = MAIN_K * NRE" in s and "총 예산은 균등 배분과 **같게**" in s,
       "⑤ ★★★ 총 예산을 균등 배분과 같게 유지한다(R36 ②)")
    ok('REC_RATE = (m3 / m4) if (m4 > 1e-9 and m3 > 0)' in s,
       "⑤ ★★★ 회수율을 **둘 다 양수일 때만** 읽는다(널 조건에서 −78% 가 나왔다)")
    ok("FLAG_K = (100, 300)" in s and "RIDGE_A = 1.0" in s,
       "⑤ 예산·정규화가 **사전 고정**돼 있다(R34 ②)")
    ok("K2_THR = max(0.0, NR[2])" in s and "K3_THR = max(0.0, N3[2])" in s,
       "★★ 두 관문 모두 **max(0, 측정된 영점 상단)** 을 문턱으로 쓴다")
    ok("무작위 재배치" in s,
       "★★ K3 의 영점은 **같은 π̂ 값 집합을 레코드에 재배치**한 것이다(구성 대조)")
    ok("def decide(lo, hi, thr, direction)" in s and "np.isfinite(thr)" in s,
       "★ `decide` 가 문턱이 nan 이면 미결을 낸다")
    ok("해석 불가" in s and "R41 ②" in s,
       "★ 효과가 0 근처면 필요표본을 해석 불가로 표시한다")
    ok("미결 ≠ 등가" in s or "R33 ①" in s,
       "★ 「미결 ≠ 등가」가 소스에 있다")
    ok("r != held" in s and "def split_rest(held)" in s,
       "★★ LORO — held-out 이 TRAIN·DEV 어디에도 안 들어간다(R22)")
    ok('raise AssetError(f"{SV5} 없음' in s,
       "★ 자산 없으면 fallback 없이 중단(R16)")
    ok("새 데이터 0" in md() or "새 데이터 0" in s,
       "★ 새 데이터를 안 쓴다는 게 명시돼 있다")
    knob = re.findall(r"^\s*(\w+)\s*=\s*[^=].*\bif SMOKE\b", s, flags=re.M)
    ok(set(knob) <= {"NB_BOOT", "N_PERM", "N_PERM_REG"},
       f"★★★ SMOKE 로 값이 바뀌는 이름이 **비용 손잡이뿐**이다({sorted(set(knob))})")
    ok(not re.search(r"^\s*(FLAG_K|MAIN_K|RIDGE_A)\s*=.*SMOKE", s, flags=re.M),
       "★★★ 예산·정규화는 SMOKE 와 무관하게 고정이다")


def dynamic():
    print("\n[동적] 합성 데이터로 설계 불변식을 **실제로** 검증")
    from sklearn.metrics import average_precision_score, roc_auc_score

    rng = np.random.RandomState(53)
    pis = [0.01, 0.03, 0.09, 0.18, 0.30, 0.58]
    sz = [2500, 2400, 2600, 2300, 2200, 3150]
    recs = np.concatenate([np.full(sz[r], r) for r in range(6)])
    y = np.zeros(len(recs), int)
    for r in range(6):
        m = np.where(recs == r)[0]
        y[m[:int(pis[r] * len(m))]] = 1
    sc = rng.normal(0, 1, len(recs)); sc[y == 1] += 1.3
    REC = list(range(6))
    NS = {r: int((y[recs == r] == 1).sum()) for r in REC}

    def at_k(r, k):
        m = recs == r; ss = sc[m]; yy = y[m] == 1
        k = int(min(max(1, k), m.sum()))
        fl = ss >= np.partition(ss, -k)[-k]
        tp = int((fl & yy).sum())
        return dict(sens=tp / max(1, NS[r]), tp=tp, ceil=min(1.0, k / max(1, NS[r])),
                    flagged=int(fl.sum()))

    # ── ⓐ 상한은 예산과 S 만으로 정해진다 — 모델과 무관하다
    K = 300
    ceil = {r: min(1.0, K / NS[r]) for r in REC}
    ok(ceil[5] < 0.20 and ceil[0] >= 1.0,
       f"ⓐ ★★★ 같은 예산 {K}개인데 상한이 레코드마다 {ceil[5]:.3f} ~ {ceil[0]:.3f} 다 — "
       f"**모델과 무관하게** S 가 크면 민감도가 막힌다(Q4-F 레코드 48 상한 0.104)")
    perfect = {r: min(1.0, K / NS[r]) for r in REC}
    ok(all(at_k(r, K)["sens"] <= perfect[r] + 1e-12 for r in REC),
       "ⓐ ★★ 실측 민감도가 **어떤 레코드에서도 상한을 못 넘는다** — 상한 계산이 옳다")

    # ── ⓑ 달성률이 두 실패를 가른다
    ach = {r: at_k(r, K)["sens"] / ceil[r] for r in REC}
    ok(min(ach.values()) >= 0.0 and max(ach.values()) <= 1.0 + 1e-9,
       f"ⓑ 달성률이 [0,1] 안이다({min(ach.values()):.3f}~{max(ach.values()):.3f})")
    lo_sens_hi_ach = [r for r in REC if at_k(r, K)["sens"] < 0.3 and ach[r] > 0.8]
    desc = " · ".join("#%d(민감도 %.3f·달성 %.0f%%)"
                      % (r, at_k(r, K)["sens"], 100 * ach[r]) for r in lo_sens_hi_ach)
    ok(len(lo_sens_hi_ach) > 0,
       "ⓑ ★★★ **민감도는 낮은데 달성률이 높은** 레코드가 있다(" + desc +
       ") — **예산 부족이지 모델 실패가 아니다**. Q4-F 는 이 둘을 못 갈랐다")

    # ── ⓒ AUROC 는 상위 꼬리를 대변하지 못한다
    aucs = {r: roc_auc_score(y[recs == r], sc[recs == r]) for r in REC}
    lifts = {r: average_precision_score(y[recs == r], sc[recs == r]) / pis[r] for r in REC}
    a = np.array([aucs[r] for r in REC]); c = np.array([ach[r] for r in REC])
    l = np.array([lifts[r] for r in REC])
    ok(max(a) - min(a) < 0.2,
       f"ⓒ AUROC 는 {min(a):.3f}~{max(a):.3f} 로 좁다")
    ok(np.std(c) > 2 * np.std(a),
       f"ⓒ ★★★ 그런데 달성률은 SD {np.std(c):.4f} 로 AUROC 의 SD {np.std(a):.4f} 보다 "
       f"{np.std(c)/np.std(a):.1f}배 흩어진다 — **AUROC 가 배포 성능을 대변하지 못한다**")
    ok(abs(np.corrcoef(l, c)[0, 1]) >= 0 and np.isfinite(np.corrcoef(a, c)[0, 1]),
       f"ⓒ ρ(AUROC,달성률) {np.corrcoef(a,c)[0,1]:+.3f} · ρ(lift,달성률) "
       f"{np.corrcoef(l,c)[0,1]:+.3f} — 둘을 함께 봐야 한다")

    # ── ⓓ ★★★ 오라클 배분: `k ∝ π*` 는 평균 민감도의 최적이 **아니다**
    TOT = K * len(REC)
    def alloc_prop(w):
        ww = np.array([w[r] for r in REC], float); ww = ww / ww.sum()
        return {r: max(10, int(round(TOT * ww[i]))) for i, r in enumerate(REC)}
    def greedy(total):
        """★ 접두사 제약을 지키는 탐욕 — 「다음 양성까지의 비용」 대비 이득."""
        import heapq
        nxt, hp = {}, []
        for r in REC:
            m = recs == r; order = np.argsort(-sc[m])
            yy = (y[m] == 1)[order]
            pos = np.where(yy)[0] + 1
            nxt[r] = pos
            if len(pos):
                heapq.heappush(hp, (-(1.0 / max(1, NS[r])) / pos[0], r, 0, int(pos[0])))
        k = {r: 0 for r in REC}; spent = 0
        while hp and spent < total:
            _, r, pi_, j = heapq.heappop(hp)
            cost = j - k[r]
            if cost > 0 and spent + cost <= total:
                k[r] = j; spent += cost
            elif cost > 0:
                continue
            if pi_ + 1 < len(nxt[r]):
                jj = int(nxt[r][pi_ + 1])
                heapq.heappush(hp, (-(1.0 / max(1, NS[r])) / max(1, jj - k[r]),
                                    r, pi_ + 1, jj))
        for r in REC:
            k[r] = max(1, k[r])
        left = total - sum(k.values())
        if left > 0:
            for i, r in enumerate(sorted(REC, key=lambda x: NS[x])):
                k[r] += left // len(REC) + (1 if i < left % len(REC) else 0)
        return k
    mean_sens = lambda km: float(np.mean([at_k(r, km[r])["sens"] for r in REC]))
    uni = {r: K for r in REC}
    prop = alloc_prop({r: pis[r] * sz[r] for r in REC})
    gre = greedy(TOT)
    ok(mean_sens(gre) >= mean_sens(prop) - 1e-12,
       f"ⓓ ★★★ **탐욕 물채우기 {mean_sens(gre):.4f} ≥ `k ∝ π*` {mean_sens(prop):.4f}** — "
       f"평균 민감도는 레코드를 **동등 가중**하므로 `k ∝ π*`(총 recall 최적)가 최적이 아니다")
    ok(mean_sens(gre) >= mean_sens(uni) - 1e-12,
       f"ⓓ ★★★ 그리고 탐욕이 균등({mean_sens(uni):.4f})도 넘는다 — **진짜 상한**이다")
    ok(mean_sens(prop) < mean_sens(uni),
       f"ⓓ ★★ 실제로 `k ∝ π*` 가 균등보다 **나쁘다**({mean_sens(prop):.4f} < "
       f"{mean_sens(uni):.4f}) — 스모크가 잡은 그 현상")
    ok(sum(gre.values()) <= TOT + len(REC),
       f"ⓓ 탐욕 배분이 총 예산을 안 넘는다({sum(gre.values())} ≤ {TOT})")
    ok(all(gre[r] >= 1 for r in REC),
       "ⓓ ★★ 모든 레코드가 최소 1개는 받는다 — **접두사 제약**을 지키는 실현 가능 배분이다")

    # ── ⓔ 회수율은 둘 다 양수일 때만
    def rec_rate(m3, m4):
        return (m3 / m4) if (m4 > 1e-9 and m3 > 0) else float("nan")
    ok(not np.isfinite(rec_rate(-0.0271, 0.0349)) and
       not np.isfinite(rec_rate(-0.4714, -0.1233)) and
       abs(rec_rate(0.05, 0.10) - 0.5) < 1e-12,
       "ⓔ ★★★ 회수율이 **둘 다 양수일 때만** 계산된다 — 널 조건의 −78% 와 신호 조건의 "
       "382% 가 둘 다 막힌다")

    # ── ⓕ 고정 예산은 82배 유병률 범위를 못 덮는다
    lo_r = [r for r in REC if pis[r] <= 0.03]; hi_r = [r for r in REC if pis[r] >= 0.30]
    ppv = lambda r: at_k(r, K)["tp"] / max(1, at_k(r, K)["flagged"])
    ok(np.mean([ppv(r) for r in lo_r]) < np.mean([ppv(r) for r in hi_r]) and
       np.mean([at_k(r, K)["sens"] for r in lo_r]) >
       np.mean([at_k(r, K)["sens"] for r in hi_r]),
       f"ⓕ ★★★ 같은 예산에서 저유병률은 민감도 "
       f"{np.mean([at_k(r,K)['sens'] for r in lo_r]):.3f}/PPV "
       f"{np.mean([ppv(r) for r in lo_r]):.3f}, 고유병률은 "
       f"{np.mean([at_k(r,K)['sens'] for r in hi_r]):.3f}/"
       f"{np.mean([ppv(r) for r in hi_r]):.3f} — **하나의 예산으로 둘 다 못 만족한다**")

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
    print("Q4-G 픽스처 — 상한·달성률(K1) · 기록 수준 회귀(K2) · 탐욕 오라클(K4)")
    print("=" * 78)
    static()
    dynamic()
    print("\n" + "=" * 78)
    print(f"통과 {len(PASS)} · 실패 {len(FAIL)}")
    for f in FAIL:
        print("  ✗ " + f)
    sys.exit(1 if FAIL else 0)
