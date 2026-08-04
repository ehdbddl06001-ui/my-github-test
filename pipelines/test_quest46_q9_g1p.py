#!/usr/bin/env python3
"""Q9-G1′(`quest46_q9_g1p_pmorph_v2`) 픽스처 — G1 재설계.

1차(`20260804T1340`)는 판정이 아니라 **측정 실패**였다. 이 런이 고치는 넷을 지킨다:
  ① **층 폭** — 1샘플(2.78ms)이라 S 와 N 이 안 겹쳐 쌍이 죽었다(20만 중 68). 폭을 사전등록하고
     격자는 **보고용**으로만 쓴다(문턱 훑기 금지)
  ② **코호트를 매칭 쌍으로 센다** — 1차는 S/N 개수를 세서 35명 중 11명만 통계량이 섰다
  ③ **리듬-only 팔**(사전등록 G3 흡수) — 없으면 P 의 몫을 리듬 대리변수와 못 가른다
  ④ **대비의 영점을 측정한다** — `rhythm` 팔은 잔차화로 0.5 **아래**에 앉으므로 `raw−rhythm` 의
     영점은 0 이 아니다. 스모크 음성 조건에서 신호가 0 인데 **+0.0907** 이 나왔다

그리고 **위치 대조 `offwin`** 을 둔다 — P 창이 창 밖과 구별되지 않으면 P 의 증거가 아니다.
"""
import json
import os
import re
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NB = os.path.join(ROOT, "notebooks", "quest46_q9_g1p_pmorph_v2.ipynb")

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

    # ① 층 폭
    ok("STRATUM_W = 10" in s,
       "① 층 폭이 사전등록 상수다(10샘플 = 27.8ms)")
    ok("float(w)).astype(int)" in s and "def matched_auc" in s,
       "① ★★ 매칭이 **층 폭으로 나눈 뒤** 반올림한다 — 1차는 `np.round(f1)` = 1샘플이었다")
    ok("W_GRID" in s and "격자는 **보고용**" in s and "문턱 훑기 금지" in s,
       "① ★★★ 폭 격자는 **보고용**이고 판정은 사전등록 폭 하나다(R34 ②)")
    ok("판정 폭(사전등록)" in s,
       "① 격자 표에서 판정 폭이 표시된다")

    # ② 코호트를 매칭 쌍으로
    ok("def pair_count" in s,
       "② 매칭 쌍을 세는 함수가 있다")
    ok('d["pairs"] >= MIN_PAIR' in s,
       "② ★★★ 코호트 조건이 **매칭 쌍 수**다 — 1차는 S/N 개수였다")
    ok("n_old_rule" in s and "세기와 요구가 달랐다" in s,
       "② ★★ 1차 기준과 이번 기준을 **나란히 찍는다** — 무엇이 달라졌는지 보이게")
    ok("len(COH) < MIN_REC" in s and "raise AssetError" in s,
       "② 코호트가 얕으면 **중단**한다")

    # ③ 런 내 천장 · 옛 앵커 무효
    ok("런 내 천장" in s and "ANCHOR_OLD" in s,
       "③ 런 내 천장을 다시 내고 옛 앵커를 상수로 들고 있다")
    ok("비교 불가" in s,
       "③ ★★★ 옛 앵커 0.6097 이 **비교 불가**라고 못 박혀 있다(층 폭이 다르다)")
    ok("CEIL_HI" in s and 'H2["raw"]["lo"] > CEIL_HI' in s,
       "③ H2 조건 ⓑ 가 **런 내 천장의 CI 상단**을 쓴다")

    # ④ ★★★ 리듬-only 팔 · 대비의 영점
    ok('ARMS = ("rhythm", "raw", "cancel", "pmask", "offwin")' in s,
       "④ 5팔이 사전등록돼 있고 **`rhythm` 이 들어 있다**")
    ok("class TinyMLP" in s and 'arm == "rhythm"' in s,
       "④ ★★ `rhythm` 팔이 리듬 특징을 입력으로 받는 별도 모델이다")
    ok("`rhythm` 팔도 **같은 잔차화·매칭**을 거친다" in s,
       "④ ★★ `rhythm` 팔도 같은 통제를 거친다 — 남는 건 **비선형 리듬**이다")
    ok("NUL_PER" in s and "NUL_DIFF" in s,
       "④ ★★★ 영점을 **(rep, 환자)별로 보관**해 **대비의 영점**을 만든다")
    ok('decide(d_raw["lo"], d_raw["hi"], NR["hi"], ">")' in s,
       "④ ★★★ H2 판정이 **0 이 아니라 측정된 영점 상단** 기준이다")
    ok("이 대비의 영점은 **0 이 아니다**" in s or "이 대비의 영점은 0 이 아니다" in s,
       "④ ★★ 왜 0 으로 판정하면 안 되는지가 소스에 적혀 있다")
    ok("+0.0907" in s,
       "④ ★ 스모크 음성 조건의 실측(+0.0907)이 근거로 박혀 있다")
    # 판정이 영점 계산 **뒤** 셀에 있어야 한다
    i_null = next((i for i, c in enumerate(cs) if "NUL_DIFF[arm] = dict" in c), -1)
    i_verd = next((i for i, c in enumerate(cs) if 'g_("H2"' in c), -1)
    ok(0 <= i_null <= i_verd,
       f"④ ★★★ H2 판정이 대비의 영점을 **잰 뒤**에 온다(영점 셀 {i_null} ≤ 판정 셀 {i_verd})")

    # ⑤ 위치 대조 · P 전폭 마스크
    ok("OFFWIN_C = 160" in s and 'arm == "offwin"' in s,
       "⑤ ★★ **위치 대조 `offwin`** 이 P 창 밖에 있다")
    ok("raw_minus_offwin" in s and "OFF_SAME" in s,
       "⑤ ★★★ `raw − offwin` 을 재고 그 결과로 갈래를 닫을 수 있다")
    ok("PMASK_MS = 55.0" in s,
       "⑤ ★★ P 마스크가 **전폭(55ms)** 이다 — 1차는 25ms 라 잔여 P 가 남았다")
    ok("P 창이 창 밖과 구별되지 않는다" in s,
       "⑤ `offwin` ≈ `raw` 일 때 쓸 문장이 코드에 있다")

    # ⑥ 누출 차단
    ok("tmpl = np.median(XB[tr], axis=0)" in s,
       "⑥ ★★ 소거 템플릿이 **학습 구간에서만** 만들어진다")
    ok("mu, sd = Xtr.mean(0), Xtr.std(0)" in s,
       "⑥ 표준화도 학습 구간 통계로만 한다(R22)")
    ok("t < cut - GUARD_S / 2.0" in s and "t > cut + GUARD_S / 2.0" in s,
       "⑥ 시간 분할 + 가드밴드")
    ok("EPOCHS = 200" in s,
       "⑥ EPOCHS 가 설계 상수다(풀배치 = 스텝 수)")
    knobs = set(re.findall(r'^\s*(\w+)\s*=.*\bif SMOKE\b', s, re.M))
    ok(knobs <= {"NB_BOOT", "N_PERM_H3", "N_SHUF_H4"},
       f"⑥ ★★ SMOKE 가 만지는 건 **비용 손잡이뿐**이다({sorted(knobs)})")

    # ⑦ 위생
    ok(s.count("np.load") == 2,
       "⑦ 자산 두 개(svdb_data5 · svdb_pdelin)만 읽는다 — 새 데이터 0")
    ok("첫 불일치 idx" in s and "PR 중앙" in s,
       "⑦ 정합 증명 + 생리학적 자기검증")
    ok("_rank_avg" in s and "평균 순위" in s,
       "⑦ `spearman` 이 동점 평균순위 판본이다")
    ok("1차의 수" in s and "인용하지 않는다" in s,
       "⑦ ★★ 1차의 수를 인용하지 않는다고 못 박혀 있다(자가 달랐다)")
    ok("CHECK = [" in s and "가정" in s and "틀리면" in s,
       "⑦ 결론 검산표가 코드에 있다")
    ok("해석 불가" in s and "uninterpretable" in s,
       "⑦ 효과가 0 근처면 필요표본 해석 불가로 찍는다(R41 ②)")
    ok("등가가 아니다" in s,
       "⑦ 미결을 등가로 읽지 말라고 못 박는다")
    for bad in ("아무도 안 했다", "최초로 증명", "확실히 입증"):
        ok(bad not in s, f"⑦ 금지 문구 없음 — 「{bad}」")
    axis = re.findall(r'set_(?:x|y)label\(([^\n]*)\)', s) + \
        re.findall(r'set_(?:x|y)ticklabels\(([^\n]*)\)', s) + \
        re.findall(r'set_title\(([^\n]*)\)', s)
    han = [a for a in axis if re.search(r'["\'][^"\']*[가-힣]', a)]
    ok(not han, f"⑦ 그림 축·제목에 한글이 없다(발견 {len(han)}건)")


# ══════════════════════════════════════════════════════════════════ 동적
def dynamic():
    print("\n[동적] 절차가 옳게 움직이는가")
    rng = np.random.RandomState(91)

    # ── ⓐ ★★★ 층 폭이 쌍을 살린다 (1차가 죽은 이유)
    nN, nS, med = 1000, 200, 250.0
    f1 = np.r_[med - rng.normal(med, 15, nN), med - rng.normal(med * 0.72, 20, nS)]
    tt = np.r_[np.zeros(nN, bool), np.ones(nS, bool)]
    def pairs(w):
        key = np.round(f1 / w).astype(int)
        return sum(int(tt[key == k].sum()) * int((~tt[key == k]).sum()) for k in np.unique(key))
    p1, p10, p20 = pairs(1), pairs(10), pairs(20)
    ok(p1 < 200 <= p10 < p20,
       f"ⓐ ★★★ 층 폭 1샘플이면 쌍이 **{p1}개**(MIN_PAIR=200 미달)인데 10샘플이면 {p10:,}, "
       f"20샘플이면 {p20:,} — S 는 정의상 f1 이 커서 촘촘한 층에서는 N 과 **안 겹친다**")
    ok(np.median(f1[tt]) > np.median(f1[~tt]) + 30,
       f"ⓐ 그 기전 — S 의 f1 중앙 {np.median(f1[tt]):.0f} vs N {np.median(f1[~tt]):.0f} "
       "(매칭 축이 곧 클래스 정의 축이다)")

    # ── ⓑ ★★★ 잔차화된 리듬 팔은 0.5 **아래**에 앉을 수 있다 → 대비의 영점 ≠ 0
    n = 4000
    y = (rng.rand(n) < 0.2).astype(int)
    r_feat = rng.normal(np.where(y, 1.0, 0.0), 1.0)          # 리듬 특징(라벨과 상관)
    def resid_lin(v, X):
        X = np.c_[np.ones(len(X)), X]
        b = np.linalg.lstsq(X, v, rcond=None)[0]
        return v - X @ b
    def auc(v, yy):
        a, b = v[yy == 1], v[yy == 0]
        d = a[:, None] - b[None, :]
        return float(((d > 0).sum() + 0.5 * (d == 0).sum()) / d.size)
    rhythm_score = r_feat + rng.normal(0, .05, n)             # 리듬만 쓰는 모델
    wave_score = rng.normal(0, 1, n)                          # 신호 없는 파형 모델
    a_r = auc(resid_lin(rhythm_score, r_feat), y)
    a_w = auc(resid_lin(wave_score, r_feat), y)
    ok(a_r < 0.5 - 0.01 and abs(a_w - 0.5) < 0.03,
       f"ⓑ ★★★ 리듬 모델을 **자기 특징에 잔차화**하면 {a_r:.4f} 로 **0.5 아래**에 앉는데 "
       f"신호 없는 파형 모델은 {a_w:.4f} 다 → `wave − rhythm` = **{a_w-a_r:+.4f}** 가 "
       "**신호 0 에서도** 나온다. 0 으로 판정하면 거짓 통과다")

    # ── ⓒ 같은 모델 클래스끼리의 대비(offwin)는 영점이 구성으로 0 근처다
    w2 = rng.normal(0, 1, n)
    d_off = auc(resid_lin(wave_score, r_feat), y) - auc(resid_lin(w2, r_feat), y)
    ok(abs(d_off) < 0.05,
       f"ⓒ ★★ 같은 종류의 두 파형 팔 대비는 영점이 **0 근처**다({d_off:+.4f}) — "
       "그래서 `raw − offwin` 이 해석하기 쉬운 대비다")

    # ── ⓓ 가드밴드
    t = np.sort(rng.uniform(0, 1800, 3000))
    cut = t.min() + 0.5 * (t.max() - t.min())
    tr, ev = t[t < cut - 30], t[t > cut + 30]
    ok(len(tr) and len(ev) and (ev.min() - tr.max()) >= 60.0 - 1e-9,
       f"ⓓ 학습 끝과 평가 시작 사이가 가드밴드 이상이다({ev.min()-tr.max():.1f}초)")

    # ── ⓔ P 전폭 마스크가 P 를 실제로 덮는다
    FS, HW_P = 360, 32
    pm25, pm55 = int(round(25 * FS / 1000)), int(round(55 * FS / 1000))
    p_half = int(round(45 * FS / 1000))          # P 반폭 ≈ 45ms (전폭 90ms)
    ok(pm25 < p_half <= pm55,
       f"ⓔ ★★ ±25ms({pm25}샘플)는 P 반폭({p_half}샘플)을 **못 덮고** "
       f"±55ms({pm55}샘플)는 덮는다 — 1차 마스크가 헐거웠던 이유")

    # ── ⓕ 매칭 AUROC 는 방향이 있다
    key = rng.randint(0, 10, 2000); tt2 = rng.rand(2000) < 0.2
    v = rng.normal(0, 1, 2000) + np.where(tt2, 0.6, 0)
    def matched(vv, kk, t_):
        win = tie = tot = 0.0
        for k in np.unique(kk):
            m = np.where(kk == k)[0]
            a, b = vv[m[t_[m]]], vv[m[~t_[m]]]
            if not len(a) or not len(b):
                continue
            d = a[:, None] - b[None, :]
            win += (d > 0).sum(); tie += (d == 0).sum(); tot += d.size
        return (win + 0.5 * tie) / tot
    ok(matched(v, key, tt2) > 0.6 and matched(-v, key, tt2) < 0.4,
       f"ⓕ 매칭 AUROC 는 방향이 있다(정 {matched(v,key,tt2):.3f} · 역 {matched(-v,key,tt2):.3f})")

    # ── ⓖ spearman 동점 회귀 검사
    def _ravg(vv):
        vv = np.asarray(vv, float); o = vv.argsort()
        r = np.empty(len(vv), float); r[o] = np.arange(len(vv), dtype=float)
        for u in np.unique(vv):
            m = vv == u
            if m.sum() > 1:
                r[m] = r[m].mean()
        return r
    A = np.r_[np.linspace(0, 1, 14), [0.5] * 6]
    B = np.r_[np.linspace(0, 1, 14) + rng.normal(0, .1, 14), [0.01] * 6]
    vals = {round(float(np.corrcoef(_ravg(A[p]), _ravg(B[p]))[0, 1]), 9)
            for p in (rng.permutation(len(A)) for _ in range(200))}
    ok(len(vals) == 1, f"ⓖ 평균순위 spearman 은 순서에 무관하다(고유값 {len(vals)}개)")


if __name__ == "__main__":
    if not os.path.exists(NB):
        print(f"❌ 노트북이 없다 — {NB}")
        sys.exit(1)
    print("=" * 78)
    print("Q9-G1′ 픽스처 — 층 폭 · 쌍 기준 코호트 · 리듬 팔 · **대비의 영점** · 위치 대조")
    print("=" * 78)
    static()
    dynamic()
    print("\n" + "=" * 78)
    print(f"통과 {len(PASS)} · 실패 {len(FAIL)}")
    for f in FAIL:
        print("  ✗ " + f)
    sys.exit(1 if FAIL else 0)
