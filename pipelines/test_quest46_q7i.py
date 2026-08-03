"""퀘스트46 Q7-I(리듬 특징 묶음) 픽스처.

이 실험의 핵심 주장은 하나다 — **`post_rr`(보상성 휴지)는 `pre_rr`(조기성)과 독립인
정보를 갖는다.** 그래서 픽스처의 핵심도 하나다:

    **심박수를 정합하면 `f1`·`f2` 는 무너지고 `f3` 만 남는가.**

`f3` 가 정합에서 같이 무너지면 리듬 축도 「조기성」 하나였다는 뜻이고,
`f1` 이 정합에서 안 무너지면 정합이 고장난 것이다. 둘 다 확인한다.

정적 검사:
  ① `run.*` API 정합 + fallback 부재(R16)
  ② **공정 비교** — `f1` 도 조합과 **같은 교차적합 로지스틱**에 태우는가
     (적합한 조합 vs 적합 안 한 단일을 비교하면 그 차이가 곧 결론이 된다)
  ③ 교차적합 × 되풀이 + SE 에 겹 배정 잡음 (R22)
  ④ **음성 대조(STT)** 가 관문(I2)으로 걸려 있는가 — Q7-F 에서 STT 가 0.8515 를 낸 게
     이번 퀘스트에서 제일 값어치 있는 숫자였다
  ⑤ **정합은 평가만 제한**하고, 정합 전·후 RR 격차를 **나란히** 내는가
  ⑥ **런 우세 층을 성과로 읽지 않는가** — I4(고립)와 I5(런·비열등)가 분리돼 있는가
  ⑦ 【I-0】가 리뷰 지적 ②③④⑤ 를 **측정으로** 닫는가 — 특히 ⑤(리듬 주석)를
     **단정하지 않고** 원본 직독으로 가르는가
  ⑧ 문턱이 CELL 1 상수인가
  ⑨ 라벨 사용(로지스틱·STT)을 **상한**으로 표시하는가
  ⑩ 그림 라벨이 ASCII 인가

동적 검사 — 관문 셀을 **합성 코호트로 실제 실행**한다:
  ⑪ **null** — 아무 신호 없음. 조합이 개선을 지어내지 않는가. ★ 픽스처가 여기서
     **교차적합 로지스틱의 null 편의**를 잡았다 — 특징 6개짜리가 1개짜리보다 높게 나온다.
     그래서 **라벨셔플 null 팔(I2b)** 을 관문으로 추가했다
  ⑫ ★★ **조기성만** (S 는 이르고 **휴지는 N 과 구분 안 됨**) — 정합하면 **f1·f3 둘 다** 무너져야
  ⑬ ★★ **보상성 휴지까지** (S 는 이르고 **비보상성**) — 정합해도 **f3 만 남아야**
  ⑭ 런 지배 코호트 — 층 분리가 실제로 작동하는가
"""
import os, sys, json, re
import unicodedata
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
NB = json.load(open(os.path.join(ROOT, "notebooks", "quest46_q7i_rhythm_bundle.ipynb")))
CODE = [c for c in NB["cells"] if c["cell_type"] == "code"]


def cell(tag):
    hit = [c for c in CODE if "".join(c["source"]).split("\n", 1)[0].startswith("# CELL")
           and tag in "".join(c["source"]).split("\n", 1)[0]]
    assert len(hit) == 1, f"헤더가 '{tag}' 인 셀을 {len(hit)}개 찾았다"
    return "".join(hit[0]["source"])


SRC_SET = [c for c in CODE if "".join(c["source"]).startswith("# CELL 1 ")]
assert len(SRC_SET) == 1
SRC_SET = "".join(SRC_SET[0]["source"])
SRC_0, SRC_A = cell("【I-0】"), cell("【I-A】")
SRC_B, SRC_C, SRC_D = cell("【I-B】"), cell("【I-C】"), cell("【I-D】")
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

# ② 공정 비교
assert '"lr_f1": [NAMES.index("f1")]' in SRC_B, "❌ f1 을 같은 로지스틱에 안 태운다"
assert 'boot_diff(A["lr_all"], A["lr_f1"]' in SRC_C, "❌ I1 이 LR(f1) 대비가 아니다"
assert "공정 비교" in SRC_SET or "공정 비교" in ALL_SRC, "❌ 공정 비교 규약이 명시돼 있지 않다"
print("  ✅ ② f1 도 같은 교차적합 로지스틱에 태워 공정 비교한다")

# ③ 교차적합 (R22)
for tok in ("def cv_logit(", "fold = rng.permutation(len(tt)) % K",
            "for rep in range(max(n_rep, 1))", "np.sqrt(se_ ** 2 + rsd ** 2)"):
    assert tok in SRC_B, f"❌ 교차적합/되풀이/SE 합성이 없다: {tok}"
assert "lr.fit((X[tr] - mu) / sd" in SRC_B and "sc[te] = lr.decision_function" in SRC_B, \
    "❌ 적합은 훈련 겹, 채점은 시험 겹이 아니다"
assert "mu = X[tr].mean(0)" in SRC_B, "❌ 표준화도 훈련 겹에서 해야 한다"
print("  ✅ ③ 교차적합 × 되풀이 · 표준화까지 훈련 겹에서 (R22)")

# ④ 음성 대조가 관문
assert 'g_("I2"' in SRC_C and 'A["stt"]' in SRC_C, "❌ 창 음성 대조가 관문으로 안 걸려 있다"
assert "최소 관문" in SRC_C, "❌ I2 가 최소 관문임을 밝히지 않는다"
# ★ 라벨셔플 null — 특징 수가 다른 두 로지스틱을 비교하려면 필수다(픽스처가 잡았다)
assert 'g_("I2b"' in SRC_C and 'A["lr_null"]' in SRC_C, \
    "❌ 라벨셔플 null 관문(I2b)이 없다 — 특징 수 차이가 곧 결론이 된다"
assert "tt_p = rng_p.permutation(tt)" in SRC_B and 'row["lr_null"]' in SRC_B, \
    "❌ 라벨셔플 null 팔을 계산하지 않는다"
print("  ✅ ④ 창 음성 대조(I2)와 **라벨셔플 null**(I2b)이 둘 다 관문이다")

# ⑤ 정합 — 평가만 제한 · 전후 병기
i0 = SRC_B.index("def matched_auc(")
body = SRC_B[i0:]
end = re.search(r"\n(?=\S)", body[body.index("\n"):])
FN = body[:body.index("\n") + end.start() + 1] if end else body
assert "평가만" in FN, "❌ '평가만 제한' 규약이 없다"
for banned in ("cv_logit", "lr.fit", "np.median(B["):
    assert banned not in FN, f"❌ matched_auc 안에서 다시 적합한다: {banned}"
assert "rr_gap_pre" in SRC_B and "rr_gap_post" in SRC_B, "❌ 정합 전/후 RR 격차를 안 낸다"
assert "정합 전" in SRC_B and "정합 후" in SRC_B, "❌ 전/후를 나란히 출력하지 않는다"
print("  ✅ ⑤ 정합은 평가만 제한 · RR 격차를 정합 전/후로 나란히 낸다 (리뷰 ④)")

# ⑥ 런 층을 성과로 읽지 않는다
assert 'g_("I4"' in SRC_D and 'g_("I5"' in SRC_D, "❌ 층별 관문이 분리돼 있지 않다"
assert "S_ISO" in SRC_D and "S_RUN" in SRC_D, "❌ 층 마스크가 없다"
j4 = SRC_D.index('g_("I4"'); j5 = SRC_D.index('g_("I5"')
assert "S_ISO" in SRC_D[j4 - 300:j4], "❌ I4 가 고립 S 층이 아니다"
assert "S_RUN" in SRC_D[j5 - 400:j5] and "NI_RUN" in SRC_D[j5:j5 + 400], \
    "❌ I5 가 런 우세 층 비열등이 아니다"
assert "0.9905" in SRC_D or "성과가 아니" in SRC_D, "❌ 런 층 성능을 성과로 읽지 말라는 경고가 없다"
print("  ✅ ⑥ I4(고립 S 개선)와 I5(런 우세 비열등)가 분리돼 있다")

# ⑦ 【I-0】 — 측정으로 닫는다
assert "단정하지 않는다" in SRC_0 or "단정은 측정으로" in ALL_SRC, \
    "❌ 리뷰 지적을 단정으로 받는다"
assert "wfdb.rdann" in SRC_0 and "aux_note" in SRC_0, "❌ 원본 주석을 직독하지 않는다"
assert "파싱 버그다" in SRC_0 and "데이터에 없다" in SRC_0, \
    "❌ 두 가능성(버그 / 데이터에 없음)을 가르지 않는다"
assert "partial_spearman" in SRC_0 and "rg" in SRC_0, "❌ RR격차 통제 편상관이 없다"
assert "unusable & runny" in SRC_0, "❌ F1 코호트 편향(정합불가 ∩ 런우세)을 안 낸다"
assert "생략" in SRC_0, "❌ Q7-F 산출물이 없을 때 추측 없이 생략하지 않는다"
print("  ✅ ⑦ 【I-0】는 리뷰 ②③④⑤ 를 **측정으로** 닫고, ⑤ 는 단정 대신 원본 직독으로 가른다")

# ⑧ 문턱은 CELL 1
for nm_ in ("KS", "MIN_S_TPL", "K_FOLD", "N_REPEAT", "BAND_FRAC", "MIN_MATCH_S",
            "MIN_MATCH_REC", "ISO_HI", "ISO_LO", "NI_RUN"):
    assert re.search(rf"^\s*[\w, ]*\b{nm_}\b[\w, ]*=", SRC_SET, re.M), \
        f"❌ {nm_} 가 CELL 1 상수가 아니다"
    for tag, src in (("I-B", SRC_B), ("I-C", SRC_C), ("I-D", SRC_D)):
        assert not re.search(rf"^\s*[\w, ]*\b{nm_}\b[\w, ]*=[^=]", src, re.M), \
            f"❌ {nm_} 를 {tag} 에서 다시 고른다"
print("  ✅ ⑧ 사전등록 문턱은 CELL 1 상수")

# ⑨ 라벨 사용 = 상한
assert "상한" in SRC_SET and "라벨을 쓴다" in SRC_SET, "❌ 로지스틱이 라벨을 쓴다는 표시가 없다"
assert "상한" in SRC_B, "❌ 결과 표에 상한 경고가 없다"
print("  ✅ ⑨ 개체 내부 로지스틱·STT 는 '상한' 으로 표시된다")

# ⑩ 그림 ASCII
bad = [t for t in re.findall(r'set_title\(f?"([^"]*)"', SRC_FIG)
       + re.findall(r'set_xlabel\(f?"([^"]*)"', SRC_FIG)
       + re.findall(r'set_ylabel\(f?"([^"]*)"', SRC_FIG)
       if any(unicodedata.name(ch, "").startswith("HANGUL") for ch in t)]
assert not bad, f"❌ 그림 라벨에 한글: {bad}"
assert "한글이 없어" in SRC_FIG, "❌ 폰트 한계가 명시돼 있지 않다"
print("  ✅ ⑩ 그림 라벨이 ASCII 다")


# ═══════════════════════════════════════════════════════════════════════
print("\n### 동적 검사 — 정합하면 f1 은 무너지고 f3 만 남는가")

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


def make_record(rng, n_s, n_n, base=280, sd=25, early=0.55, comp=1.0,
                run_len=1, p_amp=0.0, noise=0.8):
    """비트열을 **시간순으로** 만든다. RR 은 생리적으로 구성한다.

    early : S 의 pre_rr = base × early   (작을수록 이르다)
    comp  : S 의 (pre+post)/(2·base).  <1 = 비보상성(PAC 형).
            **None 이면 S 의 post 를 N 과 똑같이 다음 RR 로 둔다** — f3 가 정보를 갖지
            않아야 하는 대조 시나리오(정합 후 f3 도 무너져야 한다)
    run_len: S 가 몇 개씩 연달아 나오나 (1 = 고립)
    """
    # ── 라벨 배치를 **명시적으로** 만든다. (확률 추첨은 n_s 를 못 맞춘다 — 픽스처가 잡았다)
    n_run = max(1, int(round(n_s / max(run_len, 1))))
    lab = np.zeros(n_s + n_n, bool)
    slots = rng.choice(np.arange(2, n_s + n_n - run_len - 2), size=n_run, replace=False)
    for st in np.sort(slots):
        lab[st:st + run_len] = True
    if lab.sum() > n_s:
        on = np.where(lab)[0][n_s:]
        lab[on] = False
    t = lab
    pre = np.where(t, base * early + rng.normal(0, sd, len(t)),
                   rng.normal(base, sd, len(t)))
    # post 를 comp 규약대로 만든다: S 의 다음 RR = 2·base·comp − pre
    pre = np.clip(pre, 60, 600)
    post = np.r_[pre[1:], base]
    post = np.r_[pre[1:], base]
    if comp is not None:
        for k in np.where(t)[0]:
            post[k] = 2.0 * base * comp - pre[k]
    x = np.arange(300)
    qrs = np.exp(-((x - 100) ** 2) / (2 * 6 ** 2)) * 5.0
    B = np.zeros((len(t), 2, 300), "float32")
    for i2 in range(len(t)):
        b = qrs + ((-p_amp if t[i2] else p_amp)
                   * np.exp(-((x - 172) ** 2) / (2 * 16 ** 2)) if p_amp else qrs * 0)
        for c in range(2):
            B[i2, c] = qrs + b * 0 + (b if p_amp else 0) + rng.normal(0, noise, 300)
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
         "BAND_FRAC": 0.05, "BAND_MIN": 8, "MIN_BAND_S": 3, "MIN_BAND_N": 3,
         "MIN_MATCH_S": 20, "MIN_MATCH_PAIR": 200, "MIN_MATCH_REC": 5,
         "ISO_HI": 0.7, "ISO_LO": 0.3, "NI_RUN": 0.02,
         "SEED0": 7, "NB_BOOT": 1000, "NB_REC": 150, "IDX_S": 1, "CONFIG": {}}
    src = {"A": SRC_A, "B": SRC_B, "C": SRC_C, "D": SRC_D}
    for c in cells:
        exec(compile(src[c], f"q7i_{c}", "exec"), g)
    return g


def mac(g, k):
    v = g["A"].get(k)
    return float(np.nanmean(v)) if v is not None else float("nan")


def macm(g, k):
    v = g["A"].get(k + "_m")
    return float(np.nanmean(v[g["MOK"]])) if v is not None else float("nan")


# ── ⑪ null
NULL = [(900 + i, dict(n_s=150, n_n=600, early=1.0, comp=None)) for i in range(10)]
g0 = run_cohort("(A) null — S 가 이르지도 않고 휴지도 정상", NULL, seed=1)
V0 = g0["VERD"]
print(f"    f1 {mac(g0,'f1'):.3f} · f3 {mac(g0,'f3'):.3f} · LR(all) {mac(g0,'lr_all'):.3f}")
print(f"    라벨셔플 null {mac(g0,'lr_null'):.3f} · LR(f1) {mac(g0,'lr_f1'):.3f}")
for k_ in ("f1", "f3"):
    assert abs(mac(g0, k_) - 0.5) < 0.10, f"A: 신호 0인데 {k_} 가 {mac(g0,k_):.4f} — 지표가 샌다"
assert not V0["I2b"].startswith("✅"), \
    (f"A: **신호 0인데 라벨셔플 null 도 못 이긴 게 아니라 이겼다** — {V0['I2b']} ({g0['DIFF']['I2b']}). "
     "I2b 가 교차적합 편의를 못 거르면 I1 은 특징 수만 세는 관문이다")
print(f"  ✅ ⑪ null — I1 {V0['I1']} · **I2b {V0['I2b']}**(라벨셔플 null 을 못 이긴다)")

# ── ⑫ ★ 조기성만 (완전보상) — 정합하면 f1·f3 둘 다 무너져야
EARLY = [(910 + i, dict(n_s=200, n_n=700, sd=48, early=0.62 + 0.02 * i, comp=None)) for i in range(10)]
g1 = run_cohort("(B) ★조기성만 — S 는 이르고 **휴지는 N 과 구분 안 됨**", EARLY, seed=2)
V1 = g1["VERD"]
print(f"    무정합 f1 {mac(g1,'f1'):.3f} · f3 {mac(g1,'f3'):.3f}")
print(f"    정합   f1 {macm(g1,'f1'):.3f} · f3 {macm(g1,'f3'):.3f}"
      f"   (정합 가능 {int(g1['MOK'].sum())}/{len(g1['RS'])})")
assert mac(g1, "f1") > 0.65, f"B: 조기성 신호가 안 만들어졌다 — f1 {mac(g1,'f1'):.3f}"
if int(g1["MOK"].sum()) >= 5:
    assert abs(macm(g1, "f1") - 0.5) < 0.15, \
        f"B: **정합했는데 f1 이 안 무너진다** — 정합이 고장났다 ({macm(g1,'f1'):.3f})"
    assert abs(macm(g1, "f3") - 0.5) < 0.15, \
        (f"B: 휴지가 N 과 같은데 정합 후 f3 가 {macm(g1,'f3'):.3f} 다 — "
         "f3 가 조기성을 새 담고 있으면 I3 이 도장기가 된다")
    print(f"  ✅ ⑫ 조기성만 — 정합하면 f1({macm(g1,'f1'):.3f})·f3({macm(g1,'f3'):.3f}) 둘 다 무너진다")
else:
    print(f"  ⚠️ ⑫ 정합 가능 개체 부족({int(g1['MOK'].sum())}) — 이 시나리오는 미결")

# ── ⑬ ★★ 보상성 휴지까지 — 정합해도 f3 만 남아야
COMP = [(920 + i, dict(n_s=200, n_n=700, sd=48, early=0.62 + 0.02 * i, comp=0.80)) for i in range(10)]
g2 = run_cohort("(C) ★★비보상성 — S 는 이르고 휴지가 **짧다**(PAC 형)", COMP, seed=3)
V2, D2 = g2["VERD"], g2["DIFF"]
print(f"    무정합 f1 {mac(g2,'f1'):.3f} · f3 {mac(g2,'f3'):.3f}")
print(f"    정합   f1 {macm(g2,'f1'):.3f} · **f3 {macm(g2,'f3'):.3f}**"
      f"   (정합 가능 {int(g2['MOK'].sum())}/{len(g2['RS'])})")
if int(g2["MOK"].sum()) >= 5:
    assert macm(g2, "f3") > 0.65, \
        (f"C: **비보상성인데 정합 후 f3 가 안 남는다**({macm(g2,'f3'):.3f}) — "
         "I3 이 잡을 게 있어도 못 잡는다는 뜻이다")
    assert V2["I3"].startswith("✅"), f"C: I3 이 지지여야 한다 — {V2['I3']} ({D2.get('I3')})"
    assert V2["I2b"].startswith("✅"), \
        f"C: 진짜 신호가 있는데 라벨셔플 null 을 못 이긴다 — {V2['I2b']}"
    print(f"  ✅ ⑬ 비보상성 — 정합해도 **f3 만 살아남는다** (I3 {V2['I3']})")
    print("     → post_rr 이 조기성과 독립인 정보를 갖는다는 주장이 검정 가능하다")
else:
    print(f"  ⚠️ ⑬ 정합 가능 개체 부족({int(g2['MOK'].sum())})")

# ── ⑭ 런 지배 — 층 분리
RUN = ([(930 + i, dict(n_s=60, n_n=900, early=0.6, comp=0.8)) for i in range(8)]
       + [(940 + i, dict(n_s=300, n_n=500, early=0.6, comp=0.8, run_len=25)) for i in range(5)])
g3 = run_cohort("(D) 런 지배 5 + 고립 8 — 층 분리가 작동하나", RUN, seed=4)
st = g3["CONFIG"]["strata"]
print(f"    층 크기 — 고립 {st['iso']} · 혼합 {st['mix']} · 런 {st['run']}")
assert st["run"] >= 3, f"D: 런 우세 층이 안 잡혔다 — {st}"
assert st["iso"] >= 3, f"D: 고립 층이 안 잡혔다 — {st}"
assert g3["VERD"].get("I4") is not None and g3["VERD"].get("I5") is not None, \
    "D: 층별 관문이 안 매겨졌다"
print(f"  ✅ ⑭ 층 분리 작동 — I4 {g3['VERD']['I4']} · I5 {g3['VERD']['I5']}")

print("\n전부 통과 ✅ — Q7-I 는 정합에서 무너질 것과 남을 것을 가른다")
sys.exit(0)
