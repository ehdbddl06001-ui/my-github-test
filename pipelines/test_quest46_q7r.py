"""퀘스트46 Q7-R(calibrate) 픽스처.

Q7-Q(`ailab-2026-0066`)가 병목을 **창의 위치가 아니라 관문의 분해능**으로 특정했다.
Q7-R 은 창 질문을 보류하고 **자를 고치고 결정 가능한 추정 대상으로 갈아탄다.**

픽스처의 핵심은 셋이다:

    **양성 대조가 관문을 통과하는가**(R33 ①) — Q7-Q 는 수준 추정기만 검정하고 관문의
    검출력을 주장했다. 이제 주입 → 짝의 차이 → 부트스트랩 → Bonferroni 전부를 탄다
    **격자가 바닥을 감싸는가**(R33 ②) — 최소 진폭에서 미검출이 나와야 유효하다
    **`ladder_read()` 가 단조성을 실제로 검사하는가**(R33 ④) — Q7-Q 는 끝값 비만 봤다

정적 검사:
  ① `run.*` API(finish dict) · fallback 부재(R16)
  ② ★★ `ladder_read()` 가 **단조성을 실제로 검사**하는가(R33 ④)
  ③ ★★ `judge()` 가 **MDE** 를 내고 「MDE 아래 = 측정 한계」를 찍는가(R33 ①)
  ④ ★★ 양성 대조가 **관문에 통과**하는가 — 주입 배열이 `boot_pair` 로 들어가고
     Bonferroni 분위수를 쓰는가(R33 ①)
  ⑤ ★★ 격자 최소가 0.01 이하이고 **바닥 감쌈 여부를 판정·출력**하는가(R33 ②)
  ⑥ ★★ 주입 파형이 **개체별로 다른가**(동일 파형 금지 — 상한만 재게 된다)
  ⑦ ★★ 주 관문이 **ΔAUPRC/부분 AUC** 이고 등가 임계가 사전등록 상수인가(R33 ⑤)
  ⑧ ★ 교차환자가 **LORO(개체 단위)** 이고 PCA 가 **학습 레코드에서만** 적합되는가
  ⑨ ★ 클러스터 부트스트랩이 **레코드 단위**인가
  ⑩ ★ `dr` 를 **AIPW 라 부르지 않고** 확장 기저가 누출 채널을 포함하는가
  ⑪ ★ 프로브가 **기저·누출 채널 밖**인가
  ⑫ ★ 지터 대조가 있는가(Q7-Q 의 −0.0666 을 (A)/(B) 로 가른다)
  ⑬ 누출 바닥 양수(R32 ④) · 짝의 차이에서 안 뺀다(R32 ⑤) · 폭 정합 코드 강제
  ⑭ 「측정 불가」가 어떤 결론 분기도 안 타는가(R29 ②) · 그림 ASCII

동적 검사 — 노트북 함수를 **그대로 꺼내** 합성 코호트로 실행한다:
  ⑮ ★★ `ladder_read()` — Q7-Q 실측(비단조)을 「단조 감쇠」로 **안** 부르는가(R33 ④ 회귀)
  ⑯ ★★ `judge()` — Q7-Q 실측(+0.0293, 반폭 0.117)을 **측정 한계**로 찍는가(R33 ① 회귀)
  ⑰ ★★ `partial_auc()` — 완전 분리에서 1, 무작위에서 ≈(1−spec) 규모, 단조인가
  ⑱ ★ 주입 파형이 개체(시드)마다 실제로 다른가 · 진폭에 단조인가
"""
import os, sys, json, re
import unicodedata
import numpy as np
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
NB = json.load(open(os.path.join(ROOT, "notebooks", "quest46_q7r_calibrate.ipynb")))
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


SRC_0, SRC_SET = starts("# CELL 0 "), starts("# CELL 1 ")
SRC_A, SRC_B = cell("【R-A】"), cell("【R-B】")
SRC_C, SRC_D = cell("【R-C】"), cell("【R-D】")
SRC_E, SRC_F, SRC_FIG = cell("【R-E】"), cell("【R-F】"), cell("【R-G】")
ALL_SRC = "".join("".join(c["source"]) for c in CODE)

print("### 정적 검사")

# ── ① API
for m in ("run.log(", "run.save_json(", "run.save_fig(", "run.finish("):
    assert m in ALL_SRC, f"❌ {m} 가 없다"
assert re.search(r"run\.finish\(\s*\{", ALL_SRC), "❌ finish 에 dict 를 안 넘긴다"
assert "fallback 없음" in cell("【R-0a】"), "❌ R16 표기가 없다"
print("  ✅ ① run.* API(finish dict) · fallback 부재(R16)")

# ── ② ★★ 단조성 검사 (R33 ④)
lr = SRC_0[SRC_0.index("def ladder_read("):SRC_0.index("class AssetError")]
assert "mono" in lr and "abs(vals[i]) >= abs(vals[i + 1])" in lr, \
    "❌ `ladder_read()` 가 **단조성을 실제로 검사하지 않는다**(R33 ④) — Q7-Q 는 끝값 비만 봤다"
assert "단조가 아니다" in lr, "❌ 비단조일 때 그렇게 적지 않는다"
assert 'amax != "raw"' in lr, "❌ raw 앵커 검사가 없다(R32 ②)"
print("  ✅ ② `ladder_read()` 가 단조성을 실제로 검사(R33 ④) + raw 앵커(R32 ②)")

# ── ③ ★★ MDE (R33 ①)
assert "def mde(" in SRC_0, "❌ MDE 함수가 없다(R33 ①)"
js = SRC_0[SRC_0.index("def judge("):SRC_0.index("def ladder_read(")]
for m in ("equiv(", "decide(", "need_n(", "mde("):
    assert m in js, f"❌ judge() 가 {m} 를 안 쓴다"
assert "측정 한계" in js, "❌ judge() 가 MDE 아래를 **측정 한계**로 안 찍는다(R33 ①)"
print("  ✅ ③ judge() 가 등가·우월성·필요표본·**MDE**·측정한계를 전부(R33 ①)")

# ── ④ ★★ 양성 대조가 관문을 통과한다 (R33 ①)
assert "arr=INJ[m][a_]" in SRC_D, "❌ 주입 배열이 관문 부트스트랩으로 안 들어간다(R33 ①)"
assert re.search(r"boot_pair\(GATE_WIN, NEG22, m, [^)]*arr=INJ", SRC_D), \
    "❌ 주입을 **짝의 차이 관문**에 통과시키지 않는다"
assert SRC_D.count("q=BONF2 * 100") >= 2, "❌ 주입 회수에 Bonferroni 를 안 쓴다(관문과 같은 조건이어야)"
assert "관문 통과형" in SRC_D and "수준 추정기" in SRC_D, "❌ R33 ① 의 근거가 안 적혀 있다"
print("  ✅ ④ 양성 대조가 **관문에 그대로 통과**한다 — 같은 부트스트랩·같은 Bonferroni(R33 ①)")

# ── ⑤ ★★ 격자가 바닥을 감싸는가 (R33 ②)
amps = eval(re.search(r"^AMPS = (\([^)]*\))", SRC_SET, re.M).group(1))
assert min(amps) <= 0.01, f"❌ 격자 최소 {min(amps)} — 바닥을 감싸려면 0.01 이하가 필요하다"
assert len(amps) >= 4, f"❌ 격자가 얇다 {amps}"
assert "BRACKET" in SRC_D and "바닥을 못 감쌌다" in SRC_D, \
    "❌ 바닥 감쌈 여부를 **판정·출력**하지 않는다(R33 ②)"
assert "미확정" in SRC_D, "❌ 미감쌈일 때 「미확정」이라 안 적는다"
print(f"  ✅ ⑤ 주입 격자 {amps} · 바닥 감쌈 여부를 판정·출력(R33 ②)")

# ── ⑥ ★★ 개체별 이질 파형
wa = SRC_B[SRC_B.index("def win_arr("):SRC_B.index("def build_scores(")]
assert "HETERO" in wa and "rng.uniform" in wa, "❌ 주입 파형이 개체별로 안 다르다"
assert "sgn" in wa, "❌ 부호도 안 흔든다 — 동일 파형은 상한만 잰다"
assert re.search(r"^HETERO\s*=", SRC_SET, re.M), "❌ 이질성이 사전등록 상수가 아니다"
assert "동일 파형" in SRC_B or "동일 파형" in SRC_SET, "❌ 동일 파형 금지 근거가 없다"
print("  ✅ ⑥ 주입 파형이 **개체별로 다르다**(중심·폭·부호) — 상한만 재는 걸 피한다")

# ── ⑦ ★★ 주 관문이 ΔAUPRC / 부분 AUC (R33 ⑤)
assert "average_precision_score" in SRC_A, "❌ AUPRC 를 안 쓴다"
assert "def partial_auc(" in SRC_E, "❌ 동작점 부분 AUC 가 없다"
assert re.search(r"^EQ_DELTA = ([\d.]+)", SRC_SET, re.M), "❌ 등가 임계가 사전등록 상수가 아니다"
eqd = float(re.search(r"^EQ_DELTA = ([\d.]+)", SRC_SET, re.M).group(1))
assert eqd <= 0.01, f"❌ 등가 임계 {eqd} 가 너무 느슨하다"
assert "천장효과" in SRC_E and "0.9600" in SRC_E, "❌ AUROC 를 안 쓰는 이유(천장효과)가 없다"
assert '"R1"' in SRC_E and '"R1b"' in SRC_E, "❌ 주 관문 둘이 없다"
print(f"  ✅ ⑦ 주 관문 = ΔAUPRC · Δ부분AUC · 등가 임계 ±{eqd} 사전등록(R33 ⑤)")

# ── ⑧ ★ LORO + PCA 누수 없음
assert "te = RID == r" in SRC_E and "tr = ~te" in SRC_E, "❌ LORO(개체 단위 분리)가 아니다"
assert "PCA(n_components=N_PCA" in SRC_E, "❌ 창 특징이 PCA 가 아니다"
pca_line = [l for l in SRC_E.split("\n") if "PCA(" in l and ".fit(" in l]
assert pca_line and "[tr]" in pca_line[0], \
    f"❌ PCA 가 **학습 레코드에서만** 적합되지 않는다(누수): {pca_line}"
assert "학습 레코드에서만" in SRC_E, "❌ 누수 없음 근거가 안 적혀 있다"
print("  ✅ ⑧ 교차환자 = LORO · PCA 는 학습 레코드에서만 적합(누수 없음)")

# ── ⑨ ★ 레코드 단위 클러스터 부트스트랩
assert "rng.choice(recs_" in SRC_E and "클러스터 부트스트랩" in SRC_E, \
    "❌ 레코드 단위 클러스터 부트스트랩이 아니다"
print("  ✅ ⑨ 레코드 단위 클러스터 부트스트랩")

# ── ⑩ ★ dr 를 AIPW 라 부르지 않는다
assert "AIPW 가 아니다" in SRC_SET, "❌ `dr` 와 AIPW 의 구분이 안 적혀 있다"
assert re.search(r'"dr"\s*:|dr.*AIPW|AIPW.*dr', SRC_SET), "❌ dr 설명이 없다"
bm = SRC_A[SRC_A.index("def basis_mat("):SRC_A.index("def prep(")]
assert 'kind == "ext"' in bm and "LEAK_K" in bm, \
    "❌ 확장 기저가 **누출 채널**을 포함하지 않는다 — 그러면 dr 이 층화와 같아진다"
assert 'MET["dr"]' in SRC_B, "❌ dr 를 채점하지 않는다"
print("  ✅ ⑩ `dr` = 확장기저(누출채널 포함) 잔차화 → 층화 · **AIPW 라 부르지 않는다**")

# ── ⑪ ★ 프로브가 기저·누출 밖
bk = eval(re.search(r"^BASIS_K = (\([^)]*\))", SRC_SET, re.M).group(1))
lk = eval(re.search(r"^LEAK_K  = (\([^)]*\))", SRC_SET, re.M).group(1))
pk = eval(re.search(r"^PROBE_K = (\([^)]*\))", SRC_SET, re.M).group(1))
assert not (set(pk) & (set(bk) | set(lk))), f"❌ 프로브가 기저/누출과 겹친다 {pk}"
assert len(pk) >= 3, "❌ 프로브가 3개 미만"
print(f"  ✅ ⑪ 기저 {bk} · 누출채널 {lk} · **기저 밖** 프로브 {pk}")

# ── ⑫ ★ 지터 대조
assert "sh_jit" in SRC_F and "rng.permutation(sh_align)" in SRC_F, \
    "❌ 지터 대조가 없다 — Q7-Q 의 −0.0666 을 (A)/(B) 로 못 가른다"
assert "(B) 검출기 잡음" in SRC_F and "(A) 타이밍" in SRC_F, "❌ 두 해석 분기가 없다"
assert "pr_scalar" in SRC_B and "PR 잔차화" in SRC_F, "❌ 타이밍/형태 분해 (c)(d) 가 없다"
print("  ✅ ⑫ 지터 대조 + 스칼라 PR 단독 + PR 잔차화 — (A)/(B) 를 가른다")

# ── ⑬ 누출 바닥 · 폭 정합
assert "max(pos.values()" in SRC_D, "❌ 누출 바닥이 양의 초과 최댓값이 아니다(R32 ④)"
assert "수준 주장에만" in SRC_D, "❌ R32 ⑤ 명시가 없다"
assert not re.search(r"DIFF\[[^\]]*\]\[.mean.\]\s*-\s*LEAK_MAX", ALL_SRC), \
    "❌ 짝의 차이에서 누출 바닥을 뺀다(R32 ⑤)"
assert "R27 ③ 위반" in cell("【R-0a】") and "겹친다" in cell("【R-0a】"), \
    "❌ 폭 정합·겹침이 코드로 강제되지 않는다"
segs = eval(re.search(r"SEGS22 = (\{.*?\})", SRC_SET, re.S).group(1))
assert len({b - a for a, b in segs.values()}) == 1, "❌ 폭이 다르다"
print("  ✅ ⑬ 누출 바닥 양수(R32 ④) · 수준에만(R32 ⑤) · 폭 정합 코드 강제")

# ── ⑭ 측정 불가 · ASCII
assert 'un_ = lambda k: VERD.get(k, "").startswith("⛔")' in SRC_FIG, "❌ 측정 불가 검사가 없다"
assert re.search(r"un_\(g\).*for g in", SRC_FIG), "❌ 결론 분기가 측정 불가를 안 거른다"
# ★ 판정표가 **완결**인가 — 우월성·MDE미달 분기가 빠지면 진짜 결과가 「미결」로 찍힌다
assert "sup_(" in SRC_FIG and "below_mde" in SRC_FIG, \
    "❌ 판정 분기가 불완전하다 — 우월성/MDE미달 경우가 else 로 흘러 「미결」이 된다"
assert "실제로 기여한다" in SRC_FIG, "❌ 양의 결과 분기가 없다"
assert re.search(r'elif\s+"[A-Z0-9]+"\s+in\s+VERD', ALL_SRC) is None, "❌ Q7-M 의 분기 버그 패턴"
bad = [t for t in re.findall(r'set_[xy]label\("([^"]*)"\)|label="([^"]*)"', SRC_FIG)
       for t in t if t and any(unicodedata.name(ch, "").startswith("HANGUL") for ch in t)]
assert not bad, f"❌ 그림 라벨에 한글: {bad}"
assert "한글이 없어" in SRC_FIG, "❌ 폰트 한계가 명시돼 있지 않다"
print("  ✅ ⑭ 「측정 불가」가 어떤 분기도 안 탄다(R29 ②) · 그림 ASCII")


# ═══════════════════════════════════════════════════════════════════════
print("\n### 동적 검사 — 노트북 함수를 그대로 꺼내 돌린다")


def grab(src, first, stop="run.log("):
    i = src.index(first)
    return src[i:src.index(stop, i)]


NS = dict(np=np, stats=stats)
exec("import numpy as np\nfrom scipy import stats\n"
     "from sklearn.metrics import roc_curve\n"
     f"HETERO={float(re.search(r'^HETERO = ([0-9.]+)', SRC_SET, re.M).group(1))}\n"
     f"SPEC_LO={float(re.search(r'^SPEC_LO = ([0-9.]+)', SRC_SET, re.M).group(1))}\n"
     "class AssetError(RuntimeError): pass\n", NS)
exec(grab(SRC_0, "def decide(", "class AssetError"), NS)
exec(grab(SRC_E, "def partial_auc(", "run.log("), NS)
judge, ladder_read, partial_auc = NS["judge"], NS["ladder_read"], NS["partial_auc"]
mde_f = NS["mde"]

# ── ⑮ ★★ ladder_read — Q7-Q 실측(비단조)을 단조라 부르지 않는가 (R33 ④ 회귀)
q7q_q1 = {"raw": 0.0477, "lin": 0.0214, "hist": 0.0261, "quad": 0.0096,
          "rank": 0.0326, "strat": 0.0293}
v = ladder_read(q7q_q1)
# ⚠️ 「단조 감쇠」라는 **문자열**은 부정문("…라고 쓰지 않는다")에도 나온다.
#    판정을 가르는 건 **잔여 교란 평결**이 붙었는지다.
assert "잔여 교란" not in v, f"❌ Q7-Q 의 **비단조** 사다리를 잔여 교란으로 평결한다: {v}"
assert "단조가 아니다" in v, f"❌ 비단조라고 명시하지 않는다: {v}"
mono = {"raw": 0.20, "lin": 0.15, "rank": 0.10, "strat": 0.06}
assert "잔여 교란" in ladder_read(mono), "❌ 진짜 단조 감쇠를 못 잡는다"
q7p = {"raw": 0.0469, "lin": 0.0745, "rank": 0.0466, "strat": 0.0314}
assert "교란으로 읽지 않는다" in ladder_read(q7p), "❌ raw 앵커 판정이 깨졌다"
print("  ✅ ⑮ ladder_read — Q7-Q(비단조)를 「단조 감쇠」라 안 부르고, 진짜 단조는 잡는다")

# ── ⑯ ★★ judge — Q7-Q 실측을 측정 한계로 찍는가 (R33 ① 회귀)
eq, sup, nn, m_, frame = judge(0.0293, -0.0873, 0.1466, 55, 0.05)
assert abs(m_ - 0.11695) < 1e-4, f"❌ MDE {m_}"
assert "측정 한계" in frame, f"❌ Q7-Q Q1 을 **측정 한계**로 안 찍는다: {frame}"
eq2, sup2, nn2, m2, frame2 = judge(0.30, 0.25, 0.35, 55, 0.05)
assert "측정 한계" not in frame2, "❌ MDE 위인데 측정 한계로 찍는다"
assert sup2.startswith("✅"), "❌ 명백한 우월성을 못 잡는다"
print(f"  ✅ ⑯ judge — Q7-Q Q1(+0.0293, MDE {m_:.4f})을 **측정 한계**로 정확히 찍는다")

# ── ⑰ ★★ partial_auc 건전성
rng = np.random.RandomState(3)
n = 4000
y = (rng.uniform(size=n) < 0.08).astype(int)
sep = y + rng.normal(0, 0.01, n)                       # 완전 분리
rnd = rng.normal(size=n)                               # 무작위
weak = y * 0.35 + rng.normal(0, 1.0, n)                # 약한 신호
p_sep, p_rnd, p_weak = (partial_auc(y, sep, 0.95), partial_auc(y, rnd, 0.95),
                        partial_auc(y, weak, 0.95))
assert p_sep > 0.95, f"❌ 완전 분리인데 부분 AUC {p_sep:.4f}"
assert p_rnd < 0.15, f"❌ 무작위인데 부분 AUC {p_rnd:.4f} (특이도≥0.95 구간이면 작아야)"
assert p_rnd < p_weak < p_sep, f"❌ 단조가 아니다 {p_rnd:.3f} / {p_weak:.3f} / {p_sep:.3f}"
print(f"  ✅ ⑰ partial_auc — 무작위 {p_rnd:.3f} < 약함 {p_weak:.3f} < 완전분리 {p_sep:.3f}")

# ── ⑱ ★ 주입 파형이 개체마다 다르고 진폭에 단조인가
L = 22
def bump(seed, amp):
    rng = np.random.RandomState(seed)
    x = np.arange(L, dtype=float)
    c = (L - 1) / 2.0 * (1.0 + NS["HETERO"] * rng.uniform(-1, 1))
    w = max(L / 6.0 * (1.0 + NS["HETERO"] * rng.uniform(-1, 1)), 1.0)
    sgn = 1.0 if rng.uniform() > 0.25 else -1.0
    return sgn * amp * np.exp(-((x - c) ** 2) / (2 * w ** 2))
# 부호 반전은 25% 확률이라 시드 5개로는 흔들린다 — 20개로 결정적으로 본다
shapes = [bump(s, 1.0) for s in range(11, 31)]
pair = [float(np.abs(shapes[i] - shapes[j]).max())
        for i in range(len(shapes)) for j in range(i + 1, len(shapes))]
assert min(pair) > 1e-6, "❌ 어떤 두 개체의 주입 파형이 동일하다"
assert max(pair) > 0.3, f"❌ 파형 이질성이 너무 작다 (최대 차이 {max(pair):.3f})"
assert any(s.sum() < 0 for s in shapes), "❌ 부호가 안 흔들린다 — 전부 같은 방향이면 상한만 잰다"
norms = [float(np.abs(bump(11, a)).max()) for a in (0.005, 0.01, 0.02, 0.05)]
assert all(norms[i] < norms[i + 1] for i in range(len(norms) - 1)), \
    f"❌ 진폭에 단조가 아니다 {norms}"
print(f"  ✅ ⑱ 주입 파형이 개체마다 다르고(최대 차이 {max(pair):.3f}) 부호도 흔들리며 "
      f"진폭에 단조")

print("\n✅ Q7-R 픽스처 18/18 통과")
