"""퀘스트46 Q7-I″(정합 잔여 · I3 재판정) 픽스처.

이 실험의 존재 이유는 하나다 — **영가설이 틀렸다.**
Q7-I 의 I3 은 「정합 조건에서 `f3` 가 **우연 0.5** 를 넘는가」였는데, 같은 조건에서
`f1`(0.5779)·`STT`(0.5833)가 `f3`(0.5745)보다 높았다. **바닥이 0.5 가 아니었다.**

그래서 픽스처의 핵심도 하나다:

    **영가설을 실측 바닥으로 바꾸면, 잔여만 있는 코호트에서 J1 이 기각되는가.**

기각 못 하면 이 노트북은 Q7-I 의 실수를 되풀이하는 것이다.

정적 검사:
  ① `run.*` API 정합 + fallback 부재(R16)
  ② ★ **J1 의 영가설이 `max(정합 f1, 정합 STT)`** 인가 — 우연 0.5 가 아니라
  ③ ★ **유효 대역을 규칙이 고르는가** — `min(정합가능 ≥ MIN_MATCH_REC 인 대역)`.
     데이터를 보고 고르면 사후조정이다
  ④ **J3 이 지지가 아니면 J1·J2 를 인용하지 말라**는 경고가 코드에 있는가 —
     정합이 f1 을 못 죽였으면 그 대역의 f3 는 잔여 조기성을 담는다(R24-b)
  ⑤ 정합은 **평가만** 제한하고 **잔여 RR 격차를 대역폭별로** 내는가
  ⑥ `f2` 를 **설계 대상 층**(혼합+런)에서 재평가하는가 · 고립 층 대조를 병기하는가
  ⑦ `f5` 를 **상호작용항**으로 넣고 `rho(f5, 고립비율)` 을 병기하는가
  ⑧ 편상관을 **CI 와 함께** 내는가 (Q7-I 는 점추정만 냈다)
  ⑨ 문턱이 CELL 1 상수인가 · 교차적합(R22)인가
  ⑩ 그림 라벨이 ASCII 인가

동적 검사 — 관문 셀을 **합성 코호트로 실제 실행**한다:
  ⑪ ★★ **잔여만 있는 코호트** — `f3` 에 진짜 신호가 **없고** 정합이 불완전해 `f1` 이
     0.5 를 넘는다. **J1 이 기각돼야 한다.** Q7-I 의 실수를 재현하는 시나리오다
  ⑫ ★ **진짜 `f3` 신호 코호트** — 비보상성이 뚜렷하면 J1 이 지지여야 한다
  ⑬ **대역을 좁히면 `f1` 이 내려가는가** — 곡선이 단조로워야 J3 이 의미가 있다
"""
import os, sys, json, re
import unicodedata
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
NB = json.load(open(os.path.join(ROOT, "notebooks", "quest46_q7i2_match_residual.ipynb")))
CODE = [c for c in NB["cells"] if c["cell_type"] == "code"]


def cell(tag):
    hit = [c for c in CODE if "".join(c["source"]).split("\n", 1)[0].startswith("# CELL")
           and tag in "".join(c["source"]).split("\n", 1)[0]]
    assert len(hit) == 1, f"헤더가 '{tag}' 인 셀을 {len(hit)}개 찾았다"
    return "".join(hit[0]["source"])


SRC_SET = [c for c in CODE if "".join(c["source"]).startswith("# CELL 1 ")]
assert len(SRC_SET) == 1
SRC_SET = "".join(SRC_SET[0]["source"])
SRC_A, SRC_B = cell("【J-A】"), cell("【J-B】")
SRC_C, SRC_D, SRC_E = cell("【J-C】"), cell("【J-D】"), cell("【J-E】")
SRC_FIG = [c for c in CODE if "".join(c["source"]).startswith("# CELL 8")]
assert len(SRC_FIG) == 1
SRC_FIG = "".join(SRC_FIG[0]["source"])
ALL_SRC = "".join("".join(c["source"]) for c in CODE)

print("### 정적 검사")

lib = os.path.join(ROOT, "lib", "medkos_run.py")
if os.path.exists(lib):
    have = set(re.findall(r"^\s{4}def (\w+)\(", open(lib).read(), re.M))
    miss = sorted(set(re.findall(r"\brun\.(\w+)\(", ALL_SRC)) - have)
    assert not miss, f"MedKOSRun 에 없는 메서드: {miss}"
assert "range(800, 895)" not in ALL_SRC and "range(800,895)" not in ALL_SRC, "❌ fallback (R16)"
print("  ✅ ① run.* API 정합 · fallback 부재")

# ② ★ 영가설이 실측 바닥
assert 'FLOOR = np.nanmax(np.stack([MM["f1"], MM["stt"]]), axis=0)' in SRC_C, \
    "❌ 영가설이 max(정합 f1, 정합 STT) 가 아니다"
j = SRC_C.index('g_("J1"')
seg = SRC_C[j - 400:j + 400]
assert "FLOOR" in seg, "❌ J1 이 실측 바닥과 비교하지 않는다"
assert "우연 0.5 가 아니라" in SRC_C, "❌ 영가설을 바꾼 이유가 코드에 없다"
assert 'boot_diff(MM["f3"], FLOOR' in SRC_C, "❌ J1 이 짝지은 차가 아니다"
print("  ✅ ② J1 의 영가설은 **max(정합 f1, 정합 STT)** — 우연 0.5 가 아니다")

# ③ ★ 유효 대역을 규칙이 고른다
assert "elig = [bf for bf in BANDS if int(CURVE[bf][\"ok\"].sum()) >= MIN_MATCH_REC]" in SRC_B, \
    "❌ 유효 대역 조건이 없다"
assert "BF = min(elig)" in SRC_B, "❌ 가장 좁은 유효 대역을 규칙으로 고르지 않는다"
assert "규칙이 고른다" in SRC_B or "규칙 선택" in SRC_B, "❌ 규칙 선택임을 밝히지 않는다"
assert "raise AssetError" in SRC_B, "❌ 유효 대역이 없을 때 멈추지 않는다"
print("  ✅ ③ 유효 대역은 **규칙이 고른다**(정합가능 ≥ 문턱 중 가장 좁은 것)")

# ④ J3 이 지지가 아니면 인용 금지
k = SRC_C.index('g_("J3"')
seg3 = SRC_C[k:k + 700]
assert 'if not VERD["J3"].startswith("✅")' in seg3, "❌ J3 실패 시 경고가 없다"
assert "인용하지 않는다" in seg3, "❌ J3 실패 시 J1·J2 인용 금지 경고가 없다"
assert "잔여 조기성" in SRC_C, "❌ 잔여 조기성 개념이 코드에 없다 (R24-b)"
print("  ✅ ④ J3 이 지지가 아니면 J1·J2 를 인용하지 말라는 경고가 박혀 있다")

# ⑤ 정합 — 평가만 · 대역폭별 잔여
i0 = SRC_B.index("def matched_auc(")
body = SRC_B[i0:]
end = re.search(r"\n(?=\S)", body[body.index("\n"):])
FN = body[:body.index("\n") + end.start() + 1] if end else body
assert "평가만" in FN, "❌ '평가만 제한' 규약이 없다"
for banned in ("cv_logit", "lr.fit", "np.median(B["):
    assert banned not in FN, f"❌ matched_auc 안에서 다시 적합한다: {banned}"
assert "resid" in FN, "❌ 잔여 RR 격차를 안 낸다"
assert "for bf in BANDS" in SRC_B and "잔여 RR 격차" in SRC_B, "❌ 대역폭별 잔여를 안 낸다"
print("  ✅ ⑤ 정합은 평가만 제한 · 대역폭별 잔여 RR 격차를 낸다")

# ⑥ f2 를 설계 대상 층에서
assert "TARGET = S_MIX | S_RUN" in SRC_D, "❌ f2 재평가 층이 혼합+런이 아니다"
assert 'boot_diff(RAW["f2_16"], RAW["f1"], SEED0 + 11, mask=TARGET)' in SRC_D, \
    "❌ J4 가 대상 층에서 짝지은 비교가 아니다"
assert "mask=S_ISO" in SRC_D and "설계 대상이 아닌 층" in SRC_D, "❌ 고립 층 대조가 없다"
assert "오염된 환자" in SRC_D, "❌ f2 의 설계 의도가 코드에 없다"
print("  ✅ ⑥ f2 를 설계 대상 층(혼합+런)에서 재평가하고 고립 층 대조를 병기한다")

# ⑦ f5 상호작용
assert "(X[:, i1] - X[:, i1].mean()) * (X[:, i5] - X[:, i5].mean())" in SRC_A, \
    "❌ f1×f5 상호작용항이 없다"
assert '"lr_inter": XI' in SRC_A, "❌ 상호작용 팔이 없다"
assert 'boot_diff(RAW["lr_inter"], RAW["lr_all"]' in SRC_D, "❌ J5 가 상호작용 vs 기본이 아니다"
assert "런 검출자" in SRC_D, "❌ f5 가 런 검출자라는 가설이 코드에 없다"
assert 'stats.spearmanr(RAW["f5"], ISO)' in SRC_D, "❌ rho(f5, 고립비율) 보조 지표가 없다"
print("  ✅ ⑦ f5 는 f1×f5 상호작용으로 들어가고 rho(f5, 고립비율)을 병기한다")

# ⑧ 편상관 CI
assert "def boot_partial(" in SRC_E, "❌ 편상관 부트스트랩이 없다"
assert "점추정만" in SRC_E or "CI 와 함께" in ALL_SRC or "구간으로 말한다" in SRC_E, \
    "❌ Q7-I 가 점추정만 냈다는 사실이 안 남아 있다"
assert "미결" in SRC_E and "독립 통로" in SRC_E, "❌ CI 가 0 을 포함/배제할 때의 해석이 없다"
assert "생략" in SRC_E, "❌ Q7-F 산출물이 없을 때 추측 없이 생략하지 않는다"
print("  ✅ ⑧ 편상관을 **CI 와 함께** 내고 0 포함/배제의 해석을 미리 적어둔다")

# ⑨ 상수 · 교차적합
for nm_ in ("KS", "MIN_S_TPL", "K_FOLD", "N_REPEAT", "BANDS", "MIN_MATCH_REC",
            "F1_COLLAPSE", "ISO_HI", "ISO_LO"):
    assert re.search(rf"^\s*[\w, ]*\b{nm_}\b[\w, ]*=", SRC_SET, re.M), \
        f"❌ {nm_} 가 CELL 1 상수가 아니다"
    for tag, src in (("J-A", SRC_A), ("J-B", SRC_B), ("J-C", SRC_C), ("J-D", SRC_D)):
        assert not re.search(rf"^\s*[\w, ]*\b{nm_}\b[\w, ]*=[^=]", src, re.M), \
            f"❌ {nm_} 를 {tag} 에서 다시 고른다"
assert "fold = rng.permutation(len(tt)) % K" in SRC_A and "lr.fit((X[tr] - mu) / sd" in SRC_A, \
    "❌ 교차적합이 아니다 (R22)"
print("  ✅ ⑨ 문턱은 CELL 1 상수 · 교차적합 (R22)")

# ⑩ 그림 ASCII
bad = [t for t in re.findall(r'set_title\(f?"([^"]*)"', SRC_FIG)
       + re.findall(r'set_xlabel\(f?"([^"]*)"', SRC_FIG)
       + re.findall(r'set_ylabel\(f?"([^"]*)"', SRC_FIG)
       if any(unicodedata.name(ch, "").startswith("HANGUL") for ch in t)]
assert not bad, f"❌ 그림 라벨에 한글: {bad}"
assert "한글이 없어" in SRC_FIG, "❌ 폰트 한계가 명시돼 있지 않다"
print("  ✅ ⑩ 그림 라벨이 ASCII 다")


# ═══════════════════════════════════════════════════════════════════════
print("\n### 동적 검사 — 잔여만 있으면 J1 이 기각되는가")

import scipy.stats as _st


class Run:
    def __init__(self): self.lines = []; self.dir = "/tmp"
    def log(self, s=""): self.lines.append(str(s)); print(s)
    def save_json(self, n, o): pass
    def save_fig(self, n, f=None): pass
    def finish(self, r): pass


class AssetError(RuntimeError):
    pass


def decide(lo, hi, thr, direction):
    if direction not in (">", "<"):
        raise ValueError("direction 은 '>' 또는 '<'")
    if direction == ">":
        if lo > thr: return "✅ 지지"
        if hi < thr: return "❌ 기각"
    else:
        if hi < thr: return "✅ 지지"
        if lo > thr: return "❌ 기각"
    return "⚠️ 미결"


def make_record(rng, n_s, n_n, base=280, sd=45, early=0.62, comp=None,
                run_len=1, noise=0.8):
    """`comp=None` 이면 S 의 post 를 N 과 똑같이 다음 RR 로 둔다 —
    **`f3` 에 진짜 신호가 없는 코호트**(잔여만 남는 시나리오)."""
    n_run = max(1, int(round(n_s / max(run_len, 1))))
    lab = np.zeros(n_s + n_n, bool)
    slots = rng.choice(np.arange(2, n_s + n_n - run_len - 2), size=n_run, replace=False)
    for st in np.sort(slots):
        lab[st:st + run_len] = True
    if lab.sum() > n_s:
        lab[np.where(lab)[0][n_s:]] = False
    t = lab
    pre = np.where(t, base * early + rng.normal(0, sd, len(t)),
                   rng.normal(base, sd, len(t)))
    pre = np.clip(pre, 60, 600)
    post = np.r_[pre[1:], base]
    if comp is not None:
        for k in np.where(t)[0]:
            post[k] = 2.0 * base * comp - pre[k]
    x = np.arange(300)
    qrs = np.exp(-((x - 100) ** 2) / (2 * 6 ** 2)) * 5.0
    B = np.zeros((len(t), 2, 300), "float32")
    for i2 in range(len(t)):
        for c in range(2):
            B[i2, c] = qrs + rng.normal(0, noise, 300)
    return B, t, pre, post


def cohort(specs, seed):
    rng = np.random.RandomState(seed)
    Bs, Ys, Rs, Ps, Qs = [], [], [], [], []
    for rec, kw in specs:
        B, t, pre, post = make_record(rng, **kw)
        Bs.append(B); Ys.append(np.where(t, 1, 0)); Ps.append(pre); Qs.append(post)
        Rs.append(np.full(len(t), rec, np.int64))
    return (np.concatenate(Bs), np.concatenate(Ys), np.concatenate(Rs),
            np.concatenate(Ps), np.concatenate(Qs))


def run_cohort(tag, specs, seed=0, cells=("A", "B", "C", "D")):
    print("\n" + "=" * 78); print(f"### {tag}"); print("=" * 78)
    BSTT, Y, REC, PRE, POST = cohort(specs, seed)
    g = {"np": np, "stats": _st, "run": Run(), "AssetError": AssetError, "decide": decide,
         "BSTT": BSTT[:, :, 130:215], "Y": Y, "REC": REC, "PRE": PRE, "POST": POST,
         "ALLR": [int(r) for r in np.unique(REC)],
         "KS": (8, 16), "MIN_S_TPL": 20, "K_FOLD": 5, "N_REPEAT": 2,
         "BANDS": (0.05, 0.03, 0.02, 0.01), "BAND_MIN": 4,
         "MIN_BAND_S": 3, "MIN_BAND_N": 3, "MIN_MATCH_S": 20, "MIN_MATCH_PAIR": 200,
         "MIN_MATCH_REC": 5, "F1_COLLAPSE": 0.52, "ISO_HI": 0.7, "ISO_LO": 0.3,
         "SEED0": 7, "NB_BOOT": 1000, "NB_REC": 150, "IDX_S": 1, "CONFIG": {}}
    src = {"A": SRC_A, "B": SRC_B, "C": SRC_C, "D": SRC_D}
    for c in cells:
        exec(compile(src[c], f"q7i2_{c}", "exec"), g)
    return g


def mm_(g, a):
    return float(np.nanmean(g["MM"][a][g["MOK"]]))


# ── ⑪ ★★ 잔여만 — f3 에 진짜 신호가 없다
RESID = [(900 + i, dict(n_s=200, n_n=700, early=0.62 + 0.02 * i, comp=None)) for i in range(12)]
g0 = run_cohort("(A) ★★잔여만 — f3 에 신호 없음 · 정합이 불완전해 f1 이 0.5 를 넘는다",
                RESID, seed=1)
V0, D0 = g0["VERD"], g0["DIFF"]
print(f"    선택 대역 {g0['BF']} · f1ₘ {mm_(g0,'f1'):.4f} · f3ₘ {mm_(g0,'f3'):.4f}"
      f" · STTₘ {mm_(g0,'stt'):.4f}")
assert not V0["J1"].startswith("✅"), \
    (f"A: **f3 에 신호가 없는데 J1 이 지지다** — 영가설이 또 틀린 것이다. "
     f"{V0['J1']} ({D0.get('J1')})")
print(f"  ✅ ⑪ 잔여만 — J1 {V0['J1']} (실측 바닥을 못 넘는다). Q7-I 의 실수를 되풀이하지 않는다")

# ── ⑫ ★ 진짜 f3 신호
REAL = [(910 + i, dict(n_s=200, n_n=700, early=0.62 + 0.02 * i, comp=0.80)) for i in range(12)]
g1 = run_cohort("(B) ★진짜 f3 신호 — 비보상성(PAC 형)", REAL, seed=2)
V1, D1 = g1["VERD"], g1["DIFF"]
print(f"    선택 대역 {g1['BF']} · f1ₘ {mm_(g1,'f1'):.4f} · **f3ₘ {mm_(g1,'f3'):.4f}**"
      f" · STTₘ {mm_(g1,'stt'):.4f}")
assert V1["J1"].startswith("✅"), \
    (f"B: **진짜 f3 신호가 있는데 J1 이 못 잡는다** — 관문이 기각기 전용이다. "
     f"{V1['J1']} ({D1.get('J1')})")
print(f"  ✅ ⑫ 진짜 신호 — J1 {V1['J1']} (실측 바닥을 넘는다). 기각기 전용이 아니다")

# ── ⑬ 대역을 좁히면 f1 이 내려가는가
c0 = g1["CURVE"]
f1s = [float(np.nanmean(c0[b]["M"]["f1"][c0[b]["ok"]])) for b in (0.05, 0.03, 0.02, 0.01)
       if c0[b]["ok"].any()]
rs = [float(np.nanmedian(c0[b]["resid"][c0[b]["ok"]])) for b in (0.05, 0.03, 0.02, 0.01)
      if c0[b]["ok"].any()]
print(f"    f1ₘ 곡선 {['%.3f' % v for v in f1s]}")
print(f"    잔여 격차 {['%.3f' % v for v in rs]}")
assert len(f1s) >= 2 and f1s[-1] <= f1s[0] + 1e-6, \
    f"C: 대역을 좁혔는데 f1 이 안 내려간다 — 정합이 작동하지 않는다: {f1s}"
assert rs[-1] <= rs[0] + 1e-6, f"C: 대역을 좁혔는데 잔여 격차가 안 준다: {rs}"
print("  ✅ ⑬ 대역을 좁히면 f1 과 잔여 격차가 함께 내려간다 — J3 의 전제가 성립한다")

print("\n전부 통과 ✅ — Q7-I″ 는 영가설을 실측 바닥으로 두고 잔여와 신호를 가른다")
sys.exit(0)
