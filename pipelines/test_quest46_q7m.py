"""퀘스트46 Q7-M(표본 회복 · 정확 pre × 기저선 대역) 픽스처.

Q7-K 는 두 축을 **같은 폭 대역**으로 갈라 정합했고 **어느 쪽도 못 죽였다**
(`f1ₘ` 0.5526 · `f2ₘ` 0.5445). 원인이 둘로 갈렸다.

**① 정확 pre 를 팔았다.** `f1` 은 `pre` 의 결정론적 단조함수라 짝 잔여 1.7 샘플에도
순위가 산다(R27 ①). `pre` 는 정수 격자가 있어 **정확 정합이 가능한데** 그걸 버렸다.

**② 표본을 버렸다.** 19/59 개체 · S 의 25%. 그 원인은 `MIN_CELL_S = MIN_CELL_N = 3`
이라는 **레거시 상수**다 — Q7-F 의 `matched_auc` 에서 물려받았고 정당화된 적이 없다.
조건부 일치도는 **칸마다 추정치를 만들지 않는다.** 이긴 쌍/전체 쌍을 누적할 뿐이라
**S 1 · N 1 칸도 유효한 쌍 1개**를 기여한다. 편의가 아니라 분산만 늘고, 그건 개체
부트스트랩이 이미 잡는다.

그래서 이 실험은 **`pre` 를 항상 정확 정합으로 고정**하고 **국소 기저선만 대역**으로
묶으며(`pre` 고정 시 `f2 = 1 − pre/b` 는 **`b` 의 순증가 함수**라 둘은 정확히 같다),
**`MIN_CELL` 을 1** 로 내려 버리던 칸을 되찾는다.

픽스처의 핵심은 셋이다:

    **`MIN_CELL` 3 → 1 이 실제로 표본을 되찾는가**
    **정확 pre × 기저선 대역이 `f1` 을 0.5 로 유지한 채 `f2` 를 떨어뜨리는가**(Q7-K 의 실패 수정)
    **`f3_glob` 이 기저선 대역에 `f3` 보다 덜 반응하는가**(M5 의 반증 시험이 성립하는가)

정적 검사:
  ① `run.*` API 정합(finish 인자 포함) + fallback 부재(R16)
  ② ★ `pre` 는 **항상 정확**이고 기저선만 대역인가 — Q7-K 의 두-축-대역이 남아 있지 않은가
  ③ ★ **`MIN_CELL` = 1** 이고 【M-0】 이 3→2→1 회복량을 실측하는가
  ④ ★ **주지표가 「차이」**(M3a·M3b)이고 봉인이 **수준에만** 걸리는가(R27 ②)
  ⑤ null 의 셔플 SE 를 CI 에 전파하는가 · 셔플 20회 이상인가(R26 ②)
  ⑥ **`f3_glob`** 이 있고 M5 가 **반증 시험**으로 서술돼 있는가
  ⑦ **실험 간 세로 비교 금지**가 명시돼 있는가 (Q7-I‴ 22 vs Q7-K 25 는 문턱 차이)
  ⑧ **상쇄 검증 · leave-one-out · 선택 편향 · 층화 간극**이 다 있는가
  ⑨ 1차 가족 {M3a·M3b·M4} 만 Bonferroni · 교차적합(R22)
  ⑩ `max` 바닥 부재(R25) · 그림 라벨 ASCII

동적 검사 — 노트북 함수를 **그대로 꺼내** 합성 코호트로 실행한다:
  ⑪ ★★ `MIN_CELL` 3 → 1 이 **남은 S 비율과 쌍 수를 늘린다**
  ⑫ ★★ 정확 pre × 기저선 대역 — **`f1` = 0.5 정확 유지 + `f2` 붕괴**(Q7-K 는 둘 다 실패)
  ⑬ ★ 결정적 짝 — 형태를 심은 코호트에서 `STT` 초과가 살고 안 심은 코호트에서 죽는다
  ⑭ ★ `f3_glob` 이 기저선 대역에 **`f3` 보다 덜 반응**한다 (M5 가 반증력을 갖는가)
"""
import os, sys, json, re
import unicodedata
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
NB = json.load(open(os.path.join(ROOT, "notebooks", "quest46_q7m_recover_power.ipynb")))
CODE = [c for c in NB["cells"] if c["cell_type"] == "code"]


def cell(tag):
    hit = [c for c in CODE if "".join(c["source"]).split("\n", 1)[0].startswith("# CELL")
           and tag in "".join(c["source"]).split("\n", 1)[0]]
    assert len(hit) == 1, f"헤더가 '{tag}' 인 셀을 {len(hit)}개 찾았다"
    return "".join(hit[0]["source"])


def starts(pfx):
    hit = [c for c in CODE if "".join(c["source"]).startswith(pfx)]
    assert len(hit) == 1, f"'{pfx}' 로 시작하는 셀을 {len(hit)}개 찾았다"
    return "".join(hit[0]["source"])


SRC_SET = starts("# CELL 1 ")
SRC_A, SRC_0 = cell("【M-A】"), cell("【M-0】")
SRC_B, SRC_C = cell("【M-B】"), cell("【M-C】")
SRC_D, SRC_E = cell("【M-D】"), cell("【M-E】")
SRC_F, SRC_FIG = cell("【M-F】"), cell("【M-G】")
ALL_SRC = "".join("".join(c["source"]) for c in CODE)

print("### 정적 검사")

# ── ① API · fallback
for m in ("run.log(", "run.save_json(", "run.save_fig(", "run.finish("):
    assert m in ALL_SRC, f"❌ {m} 가 없다"
assert re.search(r"run\.finish\(\s*\{", ALL_SRC), "❌ run.finish 에 result dict 를 안 넘긴다"
assert "MedKOSRun(" in SRC_SET, "❌ MedKOSRun 을 안 쓴다"
assert "fallback 없음" in cell("【M-0a】"), "❌ R16 표기가 없다"
print("  ✅ ① run.* API 정합(finish 인자) · fallback 부재(R16)")

# ── ② ★ pre 는 항상 정확
assert "def exact_key(" in SRC_0 and "k = exact_key(pre_v)" in SRC_0, "❌ pre 가 정확 정합이 아니다"
assert "np.floor(pre_v /" not in ALL_SRC, "❌ Q7-K 의 **pre 대역**이 남아 있다(R27 ①)"
assert "np.floor(lb_v /" in SRC_0, "❌ 기저선 축이 없다"
assert "순증가 함수" in SRC_0, "❌ 기저선 대역 = f2 대역이라는 근거가 안 적혀 있다"
print("  ✅ ② `pre` 는 **항상 정확**, 국소 기저선만 대역")

# ── ③ ★ MIN_CELL = 1 + 감사
mc = re.search(r"^MIN_CELL_S, MIN_CELL_N\s*=\s*(\d+),\s*(\d+)", SRC_SET, re.M)
assert mc and mc.group(1) == "1" and mc.group(2) == "1", "❌ MIN_CELL 이 1 이 아니다"
assert "AUDIT_CELL" in SRC_SET and "AUDIT_CELL" in SRC_0, "❌ 레거시 상수 감사가 없다"
assert "레거시" in SRC_SET and "정당화된 적이 없다" in SRC_SET, "❌ 상수 변경 근거가 없다"
assert "유효한 쌍 1개" in SRC_SET or "유효한 쌍 1개" in SRC_0, "❌ 1·1 칸이 유효하다는 근거가 없다"
print("  ✅ ③ MIN_CELL = 1 · 【M-0】 이 3→2→1 회복량을 실측한다")

# ── ④ ★ 주지표가 차이 · 봉인은 수준에만
assert "def boot_excess_diff(" in SRC_D, "❌ 초과분 차이 함수가 없다"
assert 'boot_excess_diff("p_late", "stt"' in SRC_D, "❌ M3a 가 차이가 아니다"
assert 'boot_excess_diff("stt", "f3"' in SRC_D, "❌ M3b 가 차이가 아니다"
assert "「수준」을 인용하지 않는다" in SRC_D, "❌ 봉인이 수준을 겨냥하지 않는다"
assert "봉인 아래에서도 읽는다" in SRC_D and "R27" in SRC_D, "❌ 차이는 읽는다는 규약이 없다"
assert "1차 지표로" in SRC_SET, "❌ 사전등록에 차이-1차가 없다"
print("  ✅ ④ 주지표가 **차이**(M3a·M3b) · 봉인은 **수준에만**(R27 ②)")

# ── ⑤ null SE 전파
assert "NSE" in SRC_C and "std(ddof=1)" in SRC_C, "❌ null 의 셔플 SE 를 안 낸다"
assert "rng.normal(0.0, 1.0, len(idx)) * se[idx]" in SRC_D, "❌ null 오차를 CI 에 안 흔든다"
n_shuf = int(re.search(r"^N_SHUF\s*=\s*(\d+)", SRC_SET, re.M).group(1))
assert n_shuf >= 20, f"❌ 셔플 {n_shuf}회 — 20 이상이어야"
print(f"  ✅ ⑤ 셔플 {n_shuf}회 · null SE 를 CI 에 전파(R26 ②)")

# ── ⑥ f3_glob 반증 시험
assert '"f3_glob"' in SRC_A, "❌ f3_glob 이 없다"
assert "2.0 * max(med, 1e-9)" in SRC_A, "❌ f3_glob 의 분모가 전역 중앙이 아니다"
assert "반증" in SRC_A and "반증 시험" in SRC_D, "❌ M5 가 반증 시험으로 서술되지 않았다"
assert "그 해석은 틀렸다" in SRC_D or "해석이 틀린" in SRC_A, "❌ 틀릴 조건이 안 적혀 있다"
print("  ✅ ⑥ f3_glob 이 있고 M5 가 **반증 시험**이다")

# ── ⑦ 실험 간 세로 비교 금지
assert "세로 비교" in SRC_SET, "❌ 실험 간 세로 비교 금지가 없다"
assert "20/200" in SRC_SET or "(20 S, 200 쌍)" in SRC_0, "❌ 문턱 차이 설명이 없다"
assert "같은 실행" in SRC_SET or "이 실행 안에서만" in SRC_0, "❌ 비교 범위 규약이 없다"
print("  ✅ ⑦ 실험 간 세로 비교 금지 · 문턱 차이(20/200 vs 15/100) 명시")

# ── ⑧ 강건성 넷
assert "상쇄 검증" in SRC_F, "❌ 상쇄 검증이 없다"
assert "leave-one-out" in SRC_F and "부호가 바뀐다" in SRC_F, "❌ LOO 가 없다"
assert "선택 편향" in SRC_F and "한 개도 안 남았다" in SRC_F, "❌ 선택 편향 진단이 없다"
assert "층화" in SRC_F and "매크로가 주지표" in SRC_F, "❌ 층화-매크로 간극이 없다"
print("  ✅ ⑧ 상쇄 검증 · LOO · 선택 편향 · 층화 간극")

# ── ⑨ 다중검정 · 교차적합
assert "BONF3" in SRC_SET and SRC_D.count("BONF3 * 100") >= 2, "❌ 1차 가족 보정이 없다"
assert "BONF3" in SRC_E, "❌ M4 에 보정이 없다"
assert "미보정" in SRC_D, "❌ 참고값을 미보정이라고 안 적는다"
assert "fold = rng.permutation(len(tt)) % K" in SRC_A, "❌ 교차적합(R22)이 아니다"
print("  ✅ ⑨ 1차 가족 {M3a·M3b·M4} 만 Bonferroni · 교차적합(R22)")

# ── ⑩ max 바닥 부재 · ASCII
# R25 는 **개체별 max 로 만든 바닥**을 금지한다. LOO 범위 같은 1-D `np.nanmax(vals)` 는
# 바닥이 아니라 요약 통계라 허용된다 — 패턴을 정확히 겨냥한다.
for pat in ("np.nanmax(np.stack", "np.maximum(np.stack", "nanmax(np.stack"):
    assert pat not in ALL_SRC, f"❌ max 바닥이 되살아났다(R25): {pat}"
assert "FLOOR" not in ALL_SRC, "❌ Q7-I″ 의 FLOOR 변수가 되살아났다(R25)"
bad = [t for t in re.findall(r'set_[xy]label\("([^"]*)"\)|label="([^"]*)"', SRC_FIG)
       for t in t if t and any(unicodedata.name(ch, "").startswith("HANGUL") for ch in t)]
assert not bad, f"❌ 그림 라벨에 한글: {bad}"
assert "한글이 없어" in SRC_FIG, "❌ 폰트 한계가 명시돼 있지 않다"
print("  ✅ ⑩ max 바닥 부재(R25) · 그림 라벨 ASCII")


# ═══════════════════════════════════════════════════════════════════════
print("\n### 동적 검사 — 노트북 함수를 그대로 꺼내 돌린다")


def grab(src, first, stop="run.log("):
    i = src.index(first)
    return src[i:src.index(stop, i)]


NS = dict(np=np)
exec("import numpy as np\nfrom sklearn.linear_model import LogisticRegression\n"
     "from sklearn.metrics import roc_auc_score\n"
     "K_FOLD, N_REPEAT, SEED0, NB_BOOT = 3, 1, 20260803, 600\n"
     "KS = (8, 16)\nLB_K = 16\n"
     "class AssetError(RuntimeError): pass\n", NS)
exec(grab(SRC_A, "def local_base("), NS)
exec(grab(SRC_0, "def exact_key("), NS)
rhythm_feats, build_scores = NS["rhythm_feats"], NS["build_scores"]
joint_key, cell_auc = NS["joint_key"], NS["cell_auc"]


def make_record(rng, n=3000, prev=0.20, base=280.0, sd=38.0, early=0.62,
                drift=0.22, morph=0.0, noise=0.8, w=85):
    """`pre_rr` 은 **정수 격자**(SVDB 실측 Δ = 1.0 샘플) 위에 만든다."""
    n_s = max(int(n * prev), 40)
    t = np.zeros(n, bool)
    t[rng.choice(np.arange(3, n - 3), size=n_s, replace=False)] = True
    loc = base * (1.0 + drift * np.sin(2 * np.pi * np.arange(n) / 240.0))
    pre = np.where(t, loc * early, loc) + rng.normal(0, sd, n)
    pre = np.round(np.clip(pre, 90.0, 600.0))
    post = np.r_[pre[1:], base]
    B = rng.normal(0, noise, (n, 2, w)).astype("float32")
    if morph:
        B[t] += (morph * np.exp(-((np.arange(w) - w / 2) ** 2) / (2 * (w / 6) ** 2))
                 ).astype("float32")[None, None, :]
    return B, t, pre.astype(float), post.astype(float)


def cohort(seed, nrec=5, **kw):
    rng = np.random.RandomState(seed)
    out = []
    for _ in range(nrec):
        B, t, pre, post = make_record(rng, **kw)
        X, NAMES, lb = rhythm_feats(pre, post, (8, 16))
        S = build_scores(X, NAMES, t, {"stt": B}, 20260803)
        assert S is not None, "합성 코호트에서 교차적합이 실패했다"
        out.append(dict(B=B, tt=t, pre=pre, lb=lb, X=X, NAMES=NAMES, S=S))
    return out


def measure(recs, arm, bw_f, min_cell=1, allow_empty=False):
    """`allow_empty=True` 면 칸이 하나도 안 생겨도 예외 대신 0 을 돌려준다 —
    **`MIN_CELL=3` 에서 칸이 사라지는 것 자체가 이 실험의 논거**이기 때문이다."""
    v, g1, g2, sf, pr = [], [], [], [], []
    for r in recs:
        med = float(np.median(r["pre"]))
        key = joint_key(r["pre"], r["lb"], None if bw_f is None else bw_f * med)
        a, ks_, pr_, nc_, r1, r2 = cell_auc(r["S"][arm], r["tt"], key, min_cell, min_cell,
                                            pre_v=r["pre"], f2_v=r["S"]["f2_16"])
        if pr_ >= 1:
            v.append(a); g1.append(r1); g2.append(r2)
            sf.append(ks_ / max(int(r["tt"].sum()), 1)); pr.append(pr_)
    if not v:
        if allow_empty:
            return (float("nan"), float("nan"), float("nan"), 0.0, 0.0, 0)
        raise AssertionError(f"{arm}: 칸이 하나도 안 생겼다")
    return (float(np.mean(v)), float(np.nanmedian(g1)), float(np.nanmedian(g2)),
            float(np.median(sf)), float(np.median(pr)), len(v))


def shuffle_null(recs, arm, bw_f, n_shuf=3):
    m_ = []
    for k, r in enumerate(recs):
        med = float(np.median(r["pre"]))
        key = joint_key(r["pre"], r["lb"], None if bw_f is None else bw_f * med)
        acc = []
        for s_ in range(n_shuf):
            rng = np.random.RandomState(4242 + 97 * s_ + k)
            ts = rng.permutation(r["tt"])
            Ss = build_scores(r["X"], r["NAMES"], ts, {"stt": r["B"]}, 20260803 + 31 * (s_ + 1))
            if Ss is None:
                continue
            a, _, pr_, _, _, _ = cell_auc(Ss[arm], ts, key, 1, 1)
            if pr_ >= 1:
                acc.append(a)
        if acc:
            m_.append(float(np.mean(acc)))
    return float(np.mean(m_)) if m_ else float("nan")


BW = 0.04
SIG = cohort(11, morph=1.1)

# ── ⑪ ★★ MIN_CELL 3 → 1 이 표본을 되찾는다
r3 = measure(SIG, "f1", BW, min_cell=3, allow_empty=True)
r2 = measure(SIG, "f1", BW, min_cell=2, allow_empty=True)
r1 = measure(SIG, "f1", BW, min_cell=1, allow_empty=True)
assert r1[5] > 0, "❌ MIN_CELL=1 에서도 칸이 없다 — 픽스처 설계 실패"
assert r1[3] > max(r3[3], r2[3]) * 1.3, \
    f"❌ MIN_CELL 1 이 남은 S 를 못 늘렸다 ({r3[3]:.3f}/{r2[3]:.3f} → {r1[3]:.3f})"
assert r1[4] > max(r3[4], r2[4]), f"❌ 쌍 수가 안 늘었다 ({r3[4]:.0f} → {r1[4]:.0f})"
assert r1[5] >= r3[5], "❌ 개체 수가 줄었다"
print(f"  ✅ ⑪ MIN_CELL 3→2→1 — 남은 S {r3[3]:.3f} / {r2[3]:.3f} → **{r1[3]:.3f}** · "
      f"쌍 {r3[4]:.0f} / {r2[4]:.0f} → **{r1[4]:.0f}** · 개체 {r3[5]} / {r2[5]} → **{r1[5]}**"
      + ("   ← MIN_CELL=3 은 칸이 아예 안 생긴다" if r3[5] == 0 else ""))

# ── ⑫ ★★ 정확 pre 유지 + f2 붕괴 (Q7-K 의 실패 수정)
f1_ex, g1_ex, g2_ex, _, _, _ = measure(SIG, "f1", None)
f2_ex = measure(SIG, "f2_16", None)[0]
f1_jt, g1_jt, g2_jt, _, _, njt = measure(SIG, "f1", BW)
f2_jt = measure(SIG, "f2_16", BW)[0]
assert abs(f1_ex - 0.5) < 1e-9, f"❌ 정확 pre 에서 f1 이 {f1_ex:.9f}"
assert abs(f1_jt - 0.5) < 1e-9, \
    f"❌ **기저선 대역을 얹었더니 f1 이 {f1_jt:.9f}** — pre 정확 정합이 깨졌다"
assert g1_jt == 0.0, f"❌ f1 짝 잔여가 {g1_jt} — 정확 정합이면 0 이어야"
assert f2_ex > 0.75, f"❌ 정확 pre 만으로 f2 가 {f2_ex:.4f} — Q7-I‴ K3 를 재현 못 한다"
assert f2_jt < f2_ex - 0.15, f"❌ f2 가 충분히 안 떨어졌다 ({f2_ex:.4f} → {f2_jt:.4f})"
assert g2_jt < g2_ex * 0.6, f"❌ f2 짝 잔여가 안 줄었다 ({g2_ex:.4f} → {g2_jt:.4f})"
print(f"  ✅ ⑫ f1 **{f1_ex:.4f} → {f1_jt:.4f}(유지)** · f2 {f2_ex:.4f} → **{f2_jt:.4f}** · "
      f"f2 짝잔여 {g2_ex:.4f} → **{g2_jt:.4f}**")

# ── ⑬ ★ 결정적 짝 — 형태 있음 / 없음
FLAT = cohort(12, morph=0.0)
e_sig = measure(SIG, "stt", BW)[0] - shuffle_null(SIG, "stt", BW)
e_flt = measure(FLAT, "stt", BW)[0] - shuffle_null(FLAT, "stt", BW)
assert e_sig > 0.10, f"❌ 형태를 심었는데 STT 초과가 {e_sig:+.4f}"
assert abs(e_flt) < 0.06, f"❌ 형태가 없는데 STT 초과가 {e_flt:+.4f}"
print(f"  ✅ ⑬ STT 초과 — 형태 심음 {e_sig:+.4f} vs 없음 {e_flt:+.4f}")

# ── ⑭ ★ f3_glob 이 f3 보다 기저선 대역에 덜 반응한다 (M5 의 반증력)
d_f3 = abs(measure(SIG, "f3", 0.10)[0] - measure(SIG, "f3", 0.02)[0])
d_gl = abs(measure(SIG, "f3_glob", 0.10)[0] - measure(SIG, "f3_glob", 0.02)[0])
assert d_gl < d_f3, (f"❌ f3_glob 이 f3 보다 더/같이 반응한다 ({d_gl:.4f} vs {d_f3:.4f}) — "
                     "M5 가 반증력을 못 갖는다")
print(f"  ✅ ⑭ 기저선 대역 0.10→0.02 변화폭 — f3 **{d_f3:.4f}** vs f3_glob **{d_gl:.4f}**")

print("\n✅ Q7-M 픽스처 14/14 통과")
