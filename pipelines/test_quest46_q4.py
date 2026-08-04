#!/usr/bin/env python3
"""Q4(`quest46_q4_burden_feature`) 픽스처 — 방법 B: burden 을 특징으로.

이 런에서 빠뜨리면 결과가 무효인 것 넷:
  ① **A 와 B 를 가르는 것이 무엇인지** — 선형 모델에서 burden **상수 특징**은 레코드별 상수
     로짓 시프트라 방법 A 와 구조적으로 같다. **상호작용**이라야 레코드 내 순위가 바뀐다.
     둘 다 팔로 두고 D1 이 구분한다. 안 하면 Q4 는 Q3 를 계수만 바꿔 다시 재는 런이다
  ② **주 관문 문턱 = max(0, 측정된 영점 상단)** — 사전등록이 「> 0」이므로 0 은 반드시 넘어야
     하고, 영점이 0 보다 높으면 그쪽이 더 엄하다. 영점만 쓰면 영점이 **음수**일 때 효과가
     사실상 0 이어도 통과한다(스모크 실측: D2 +0.0002 인데 ✅ 로 찍혔다)
  ③ **매크로가 진짜 판정 대상** — Q3 와 달리 `B_int` 는 레코드 내 순위를 바꾼다
  ④ **셔플 대조** — 같은 기저·같은 burden 값 집합, 대응만 깨진다(Q3-B 이식)
"""
import json
import os
import re
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NB = os.path.join(ROOT, "notebooks", "quest46_q4_burden_feature.ipynb")

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

    # ① 구조 — A 와 B 를 가르는 것
    ok('ARMS = ("raw", "A_oracle", "A_em", "B_add_oracle", "B_int_oracle", '
       '"B_int_em", "B_int_shuf")' in s,
       "① 7팔이 사전등록돼 있다 — `B_add` 와 `B_int` 가 **둘 다** 있다")
    ok("def build_B" in s and 'mode == "add"' in s and "RHY[TR_I] * btr[:, None]" in s,
       "① ★★ 상수 특징 판본과 **상호작용** 판본이 코드로 구분돼 있다")
    ok("구조적으로 같다" in s and "상수 로짓 시프트" in s,
       "① ★★★ 「상수 특징 = 레코드별 상수 시프트 = 방법 A」가 소스에 박혀 있다")
    ok("B_CONTRIB" in s and 'B_CONTRIB["B_add_oracle"]["ratio"] < 0.01' in s
       and 'B_CONTRIB["B_int_oracle"]["ratio"] > 0.01' in s,
       "① ★★★ D1 판정이 **burden 기여분의 레코드 내 산포**로 이뤄진다 — 구성으로 정확하다")
    ok("는 **틀린 말**이다" in s and "모든 계수를 다시 적합" in s,
       "① ★★ 「`B_add` 가 raw 의 순위를 정확히 보존한다」가 **틀린 말**임이 적혀 있다 — "
       "특징을 더하면 로지스틱이 모든 계수를 다시 적합한다")
    ok("Q3 를 계수만 바꿔 다시 재는 런" in s,
       "① ★★ 구조가 안 갈리면 무엇을 뜻하는지가 소스에 적혀 있다")

    # ② 주 관문 문턱
    ok("D2_THR = max(0.0, nhi)" in s,
       "② ★★★ D2 문턱이 **max(0, 영점 상단)** 이다")
    ok("영점만 문턱으로 쓰면" in s and "음수" in s,
       "② ★★ 영점만 쓰면 왜 안 되는지가 소스에 적혀 있다(영점이 음수면 0 효과도 통과)")
    ok("+0.0002" in s,
       "② ★ 스모크에서 잡힌 실측(+0.0002 인데 ✅)이 근거로 박혀 있다")
    ok('decide(D2["lo"], D2["hi"], D2_THR, ">")' in s,
       "② 판정이 그 문턱을 실제로 쓴다")
    ok("nd = []" in s and "yperm" in s,
       "② ★★ **대비의 영점**을 라벨 치환으로 측정한다(Q3-B 교훈)")

    # ③ 매크로가 진짜 판정 대상
    ok("매크로가 진짜 판정 대상" in s,
       "③ ★★★ Q3 와 달리 매크로가 **진짜 판정 대상**임이 박혀 있다")
    ok("NONINF_MARGIN = 0.01" in s,
       "③ ★★ 비열등 여유가 **상수로 사전 고정**돼 있다 — 사전등록 문구가 안 밝혔다(R39 ①)")
    ok('decide(d5["lo"], d5["hi"], -NONINF_MARGIN, ">")' in s,
       "③ D5 판정이 그 여유를 쓴다")
    ok("사전등록이 안 밝혀" in s,
       "③ 여유를 왜 여기서 못 박는지가 적혀 있다")

    # ④ 셔플 대조
    ok("def derangement" in s and "SHUF_MAPS" in s,
       "④ ★★ 셔플이 **derangement** 다(자기 값을 받는 레코드가 없다)")
    ok("대응만" in s,
       "④ 셔플 대조가 「대응만 깨진다」는 게 적혀 있다")
    ok('paired("A_oracle", "B_add_oracle"' in s,
       "④ 구조 대조 `B_add − A` 도 함께 찍는다")

    # ⑤ 재현·코호트 게이팅
    ok("COHORT_MATCH = (" in s and "len(RS) == 78" in s,
       "⑤ 재현 앵커가 **코호트 동일성**으로 게이팅된다")
    anchor_cell = next((c for c in cs if "D0 재현 실패" in c), "")
    ok(bool(anchor_cell) and "SMOKE" not in anchor_cell,
       "⑤ ★★ 재현 앵커가 든 셀에 **SMOKE 가 없다** — 스위치로 관문을 끄지 않는다")
    ok("리허설" in s and "수치 인용 금지" in s,
       "⑤ 코호트가 다르면 스스로 리허설이라 선언한다")

    # ⑥ 누출·위생
    ok("def fit_feats" in s and "Ftr.mean(0)" in s and "팔마다 다시 적합" in s,
       "⑥ ★ 팔마다 특징이 다르므로 **팔마다 다시 적합**하고 표준화도 TRAIN 에서만 한다")
    ok("DEV 반쪽 홀드아웃" in s,
       "⑥ 보정기 선택이 DEV 반쪽 홀드아웃이다(R22 · R36 ②)")
    ok("def cluster_boot" in s and "재표집 단위는 **레코드**" in s,
       "⑥ 부트스트랩이 레코드 군집이다(R11)")
    ok(s.count("np.load") == 1,
       "⑥ 자산 하나만 읽는다 — 새 데이터 0")
    ok("_rank_avg" in s and "평균 순위" in s,
       "⑥ `spearman` 이 동점 평균순위 판본이다")
    ok("전역 단독 인용 금지" in s and "지배 지분" in s,
       "⑥ 전역 단독 인용을 금하고 지배 지분을 병기한다(R11)")
    ok("CHECK = [" in s and "가정" in s and "틀리면" in s,
       "⑥ 결론 검산표가 코드에 있다")
    ok("등가가 아니다" in s,
       "⑥ 미결을 등가로 읽지 말라고 못 박는다")
    for bad in ("아무도 안 했다", "최초로 증명", "확실히 입증"):
        ok(bad not in s, f"⑥ 금지 문구 없음 — 「{bad}」")
    axis = re.findall(r'set_(?:x|y)label\(([^\n]*)\)', s) + \
        re.findall(r'set_(?:x|y)ticklabels\(([^\n]*)\)', s) + \
        re.findall(r'set_title\(([^\n]*)\)', s)
    han = [a for a in axis if re.search(r'["\'][^"\']*[가-힣]', a)]
    ok(not han, f"⑥ 그림 축·제목에 한글이 없다(발견 {len(han)}건)")
    knobs = set(re.findall(r'^\s*(\w+)\s*=.*\bif SMOKE\b', s, re.M))
    ok(knobs <= {"NB_BOOT", "N_SHUF", "N_PERM"},
       f"⑥ ★★ SMOKE 가 만지는 건 **비용 손잡이뿐**이다({sorted(knobs)})")

    # ⑦ 순서 — D1(구조)이 D2(주 관문)보다 앞
    i1 = next((i for i, c in enumerate(cs) if c.lstrip().startswith("# CELL") and "【D-B】" in c), -1)
    i2 = next((i for i, c in enumerate(cs) if c.lstrip().startswith("# CELL") and "【D-C】" in c), -1)
    ok(0 <= i1 < i2, f"⑦ ★★ D1(구조 대조)이 D2(주 관문) **앞 셀**이다({i1} < {i2}) — "
                     "구조가 안 갈리면 D2 를 읽을 이유가 없다")


# ══════════════════════════════════════════════════════════════════ 동적
def dynamic():
    print("\n[동적] 절차가 옳게 움직이는가")
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import average_precision_score
    rng = np.random.RandomState(4)

    # 합성 코호트 — 레코드마다 유병률이 다르다
    recs, X, y, b = [], [], [], []
    for r, pi in enumerate((0.02, 0.05, 0.12, 0.25, 0.40, 0.58)):
        n = 3000
        yy = (rng.rand(n) < pi).astype(int)
        X.append(rng.normal(np.c_[yy, yy, yy] * 0.7, 1.0))
        recs += [r] * n; y.append(yy); b += [pi] * n
    recs = np.array(recs); X = np.vstack(X); y = np.concatenate(y); b = np.array(b)

    def fit(Z):
        m = LogisticRegression(max_iter=2000).fit(Z, y)
        return m.decision_function(Z)

    def within_rho(a, c):
        out = []
        for r in np.unique(recs):
            m = recs == r
            ra = a[m].argsort().argsort().astype(float)
            rc = c[m].argsort().argsort().astype(float)
            out.append(np.corrcoef(ra, rc)[0, 1])
        return float(np.mean(out))

    s_raw = fit(X)
    s_add = fit(np.c_[X, b])
    s_int = fit(np.c_[X, b, X * b[:, None]])

    # ── ⓐ ★★★ burden **기여분**이 레코드 안에서 상수인가 (구성으로 정확한 검사)
    #    ⚠️ 「상수 특징이 raw 의 순위를 정확히 보존한다」는 **틀린 말**이다 — 특징을 더하면
    #    로지스틱이 모든 계수를 다시 적합하므로 리듬 가중치도 바뀐다. 정확한 명제는
    #    **burden 에서 나오는 기여분이 레코드별 상수**라는 것이고, 그건 직접 잴 수 있다.
    def contrib_ratio(mode):
        Z = np.c_[X, b] if mode == "add" else np.c_[X, b, X * b[:, None]]
        m = LogisticRegression(max_iter=2000).fit(Z, y)
        flat = np.full(len(b), b.mean())
        Zf = np.c_[X, flat] if mode == "add" else np.c_[X, flat, X * flat[:, None]]
        d = m.decision_function(Z) - m.decision_function(Zf)
        within = float(np.mean([d[recs == r].std() for r in np.unique(recs)]))
        return within / (float(d.std()) + 1e-12)
    c_add, c_int = contrib_ratio("add"), contrib_ratio("int")
    ok(c_add < 0.01 < c_int,
       f"ⓐ ★★★ burden **기여분**의 레코드 내 산포 비 — 상수 특징 **{c_add:.2e}**(레코드별 "
       f"상수 = A 와 같은 구조) vs 상호작용 **{c_int:.4f}**(레코드 안에서 변한다). "
       "이게 A 와 B 를 가르는 것이고 **구성으로 정확하다**")
    r_add = within_rho(s_raw, s_add); r_int = within_rho(s_raw, s_int)
    ok(r_add > r_int,
       f"ⓐ (참고) raw 대비 레코드 내 ρ — 상수 특징 {r_add:.6f} > 상호작용 {r_int:.6f}. "
       "★ 다만 상수 특징도 **정확히 1.0 은 아니다** — 재적합으로 리듬 계수가 바뀌기 때문이고, "
       "그래서 판정을 ρ 가 아니라 위 기여분으로 한다")

    # ── ⓑ 상수 특징 팔은 실제로 **레코드별 상수 시프트**와 같다(차가 레코드 안에서 상수)
    spread = []
    for r in np.unique(recs):
        m = recs == r
        d = s_add[m] - s_raw[m]
        spread.append(float(d.std()))
    ok(max(spread) < 0.5 * float(np.std(s_add - s_raw)),
       f"ⓑ ★★ `B_add − raw` 의 **레코드 안 산포**(최대 {max(spread):.4f})가 전체 산포"
       f"({np.std(s_add-s_raw):.4f})보다 훨씬 작다 — 레코드별 **상수 시프트**에 가깝다")

    # ── ⓒ ★★★ 문턱을 「영점 상단」만으로 두면 효과 0 도 통과한다
    def gate(lo, hi, null_hi, use_max0):
        thr = max(0.0, null_hi) if use_max0 else null_hi
        return "PASS" if lo > thr else "not"
    ok(gate(-0.0037, 0.0056, -0.0856, False) == "PASS"
       and gate(-0.0037, 0.0056, -0.0856, True) == "not",
       "ⓒ ★★★ 영점 상단(−0.0856)만 쓰면 효과 +0.0002 [−0.0037,+0.0056] 도 **통과**하지만 "
       "**max(0, 영점)** 이면 통과하지 않는다 — 스모크가 잡은 그 버그")

    # ── ⓓ 셔플 대조 — burden 값 집합은 같고 대응만 깨진다
    def derange(n, r_):
        for _ in range(500):
            p = r_.permutation(n)
            if not np.any(p == np.arange(n)):
                return p
        return np.roll(np.arange(n), 1)
    pis = np.array([0.02, 0.05, 0.12, 0.25, 0.40, 0.58])
    perm = derange(len(pis), np.random.RandomState(3))
    b_sh = np.array([pis[perm][r] for r in recs], float)
    ok(sorted(np.unique(b_sh)) == sorted(np.unique(b)) and not np.array_equal(b_sh, b),
       "ⓓ ★★ 셔플 팔은 **같은 burden 값 집합**을 쓰고 대응만 깨진다(구성 대조)")
    ap_or = average_precision_score(y, fit(np.c_[X, b, X * b[:, None]]))
    ap_sh = average_precision_score(y, fit(np.c_[X, b_sh, X * b_sh[:, None]]))
    ok(ap_or > ap_sh,
       f"ⓓ 그리고 대응이 맞을 때가 더 낫다(전역 {ap_or:.4f} > 셔플 {ap_sh:.4f})")

    # ── ⓔ 매크로는 여기서 **움직인다** (Q3 와 다른 점)
    def macro(sc):
        return float(np.mean([average_precision_score(y[recs == r], sc[recs == r])
                              for r in np.unique(recs)]))
    ok(abs(macro(s_add) - macro(s_raw)) < abs(macro(s_int) - macro(s_raw)) + 1e-9,
       f"ⓔ 매크로 Δ — 상수 특징 {macro(s_add)-macro(s_raw):+.6f} · "
       f"상호작용 {macro(s_int)-macro(s_raw):+.6f} (상호작용이라야 움직일 여지가 있다)")


if __name__ == "__main__":
    if not os.path.exists(NB):
        print(f"❌ 노트북이 없다 — {NB}")
        sys.exit(1)
    print("=" * 78)
    print("Q4 픽스처 — A/B 구조 구분 · 문턱 max(0,영점) · 매크로는 진짜 관문 · 셔플 대조")
    print("=" * 78)
    static()
    dynamic()
    print("\n" + "=" * 78)
    print(f"통과 {len(PASS)} · 실패 {len(FAIL)}")
    for f in FAIL:
        print("  ✗ " + f)
    sys.exit(1 if FAIL else 0)
