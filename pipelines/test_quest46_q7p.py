"""퀘스트46 Q7-P(`p_safe` · 직전 T 침입을 표본으로 친다) 픽스처.

Q7-N 에서 두 결론이 **동시에** 나왔다 — 「폭을 맞추니 P 가 이긴다」(`p_full − stt`
+0.0745)와 「P 창 안에서 이른 쪽이 더 세다」(`p_early` 0.2426 > `p_late` 0.2116).
둘을 동시에 참으로 만드는 유일한 설명은 **앞쪽 창이 담는 게 P 파가 아니라 직전 T** 다.

침입은 **창의 내용물**이라 RR 특징 잔차화로는 안 지워진다(점수의 선형 성분이 아니다).
그래서 Q7-P 는 특징이 아니라 **표본**으로 친다 — 직전 T 가 P 창에 **기하학적으로 못
드는 비트만** 남기고 헤드라인을 다시 잰다.

픽스처의 핵심은 셋이다:

    **마스크가 기하적으로 맞는가** — SAFE 로 남은 비트는 `t_overlap` 이 **정확히 0**
    **★★ 결정적 짝** — 침입만 심은 코호트는 마스크 후 **무너지고**, 진짜 P 파를 심은
    코호트는 마스크 후에도 **산다**. 마스크가 「무엇을 지우는지」를 실측으로 고정한다
    **`judge()` 가 Q7-N 의 실패를 재현하지 않는가**(R31 ①) — 등가 미결 + 우월성 지지 +
    등가 불가를 **한 번에** 내는가

정적 검사:
  ① `run.*` API(finish dict 포함) · fallback 부재(R16)
  ② ★ `post_rr` 이 **기저**에 없는가(R28 ②) — 마스크에만 쓴다는 근거가 적혀 있는가
  ③ ★ 프로브가 기저 밖인가 · 순위 기저 병기
  ④ ★★ `judge()` 가 **등가와 우월성을 둘 다** 내고 `need_n` 이 붙는가(R31 ① · R30 ①)
  ⑤ ★ 폭 정합이 **코드로 강제**되는가(`gate_pair` 가 폭 불일치에 raise) · 짝의 폭 실측
  ⑥ null SE 전파 · 셔플 20회 이상 · ★ **프로브·순수특징도 실측**(P7)
  ⑦ ★ 사전등록 규칙 체크리스트에 R30 · R31 이 들어 있는가(R29 ③)
  ⑧ ★ 「측정 불가」가 어떤 결론 분기도 안 타는가(R29 ②) · `elif "X" in VERD` 부재
  ⑨ ★ 누출 바닥이 **기저 밖 모든 팔**(f4·f5 포함)인가(R31 ②) · R25 와의 구분 · 교차적합
  ⑩ ★ **주 분석이 층화**인가(P8) · 잔차 팔 간 비교 금지 명시(R31 ⑤)
  ⑪ ★ 코호트 보고(P0)가 **관문보다 먼저**인가 · 선택 편향 명시(R17)
  ⑫ ★ `T_HI` × 여유 **민감도 격자**(물려받은 어림 감사 · R28 ① ③)
  ⑬ ★ 감쇠 사다리를 **기울기로** 읽는가(R31 ③) · 사다리가 약함→강함 순인가
  ⑭ 그림 라벨 ASCII · 폰트 한계 명시

동적 검사 — 노트북 함수를 **그대로 꺼내** 합성 코호트로 실행한다:
  ⑮ ★★ 마스크 기하 — SAFE 비트는 모든 창에서 `t_overlap == 0` · 컷이 이론값과 일치
  ⑯ ★★ **결정적 짝** — 침입만 심으면 마스크 후 **붕괴**, 진짜 P 를 심으면 **생존**
  ⑰ ★ `strat_auc` 항등식 — 층 키에 들어간 `f1` 은 칸 안에서 상수라 **정확히 0.5**
  ⑱ ★★ `judge()` · `need_n()` · `slope_read()` 단위 검증 — **Q7-N 실패의 회귀 테스트**
"""
import os, sys, json, re
import unicodedata
import numpy as np
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
NB = json.load(open(os.path.join(ROOT, "notebooks", "quest46_q7p_p_safe.ipynb")))
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


SRC_0 = starts("# CELL 0 ")
SRC_SET = starts("# CELL 1 ")
SRC_A, SRC_B = cell("【P-A】"), cell("【P-B】")
SRC_C, SRC_D = cell("【P-C】"), cell("【P-D】")
SRC_E, SRC_FIG = cell("【P-E】"), cell("【P-F】")
ALL_SRC = "".join("".join(c["source"]) for c in CODE)

print("### 정적 검사")

# ── ① API
for m in ("run.log(", "run.save_json(", "run.save_fig(", "run.finish("):
    assert m in ALL_SRC, f"❌ {m} 가 없다"
assert re.search(r"run\.finish\(\s*\{", ALL_SRC), "❌ run.finish 에 result dict 를 안 넘긴다"
assert "fallback 없음" in cell("【P-0a】"), "❌ R16 표기가 없다"
print("  ✅ ① run.* API(finish dict) · fallback 부재(R16)")

# ── ② ★ post_rr 은 기저에 없다 — 마스크에만 쓴다
bm = SRC_A[SRC_A.index("def basis_mat("):SRC_A.index("def prep(")]
for bad in ("post", "f3"):
    assert bad not in bm, f"❌ 기저에 `{bad}` 가 들어갔다 — 하류 변수 통제 금지(R28 ②)"
assert "마스크는 통제가 아니라 **표본 정의**" in SRC_A, \
    "❌ 마스크가 왜 R28 ② 에 안 걸리는지 근거가 없다"
assert "R28 ②" in SRC_SET, "❌ 사전등록에 하류 변수 금지가 없다"
print("  ✅ ② `post_rr` 이 기저에 없다 · 마스크는 표본 정의라는 근거 명시(R28 ②)")

# ── ③ ★ 프로브가 기저 밖
bk = eval(re.search(r"^BASIS_K\s*=\s*(\([^)]*\))", SRC_SET, re.M).group(1))
pk = eval(re.search(r"^PROBE_K\s*=\s*(\([^)]*\))", SRC_SET, re.M).group(1))
assert not (set(bk) & set(pk)), f"❌ 프로브가 기저와 겹친다 {set(bk) & set(pk)}"
assert len(pk) >= 3, "❌ 프로브가 3개 미만"
assert "f1_rank" in SRC_A, "❌ 비선형(단조 변환) 프로브가 없다"
assert '"rank"' in SRC_A and "def prep(" in SRC_A, "❌ 순위 기저(함수형 민감도)가 없다"
print(f"  ✅ ③ 기저 k={bk} · **기저 밖** 프로브 k={pk} + f1_rank")

# ── ④ ★★ 등가와 우월성을 둘 다 · 필요표본은 모든 관문에서
assert "def equiv(" in SRC_0 and "CI **전체**가" in SRC_0, "❌ 등가 판정 함수/정의가 없다"
assert "def need_n(" in SRC_0, "❌ 필요 표본 계산 함수가 없다(R30 ①)"
assert "def judge(" in SRC_0, "❌ 등가/우월성 동시 판정 함수가 없다(R31 ①)"
jsrc = SRC_0[SRC_0.index("def judge("):SRC_0.index("def slope_read(")]
assert "equiv(" in jsrc and "decide(" in jsrc and "need_n(" in jsrc, \
    "❌ judge() 가 등가·우월성·필요표본을 다 안 낸다 — Q7-N 이 놓친 지점이다(R31 ①)"
assert "어떤 표본으로도 불가능" in jsrc, "❌ 등가 불가 판정 문구가 없다"
assert re.search(r"^EQUIV_MARGIN\s*=", SRC_SET, re.M), "❌ 등가 여유가 사전등록 상수가 아니다"
assert re.search(r"^PROBE_MARGIN\s*=", SRC_SET, re.M), "❌ 프로브 여유가 상수가 아니다"
assert "judge(" in SRC_D, "❌ 관문이 judge() 를 안 쓴다"
assert "need_n" in SRC_D or "need_n" in jsrc, "❌ 관문에 필요표본이 안 붙는다"
print("  ✅ ④ judge() 가 등가·우월성·필요표본을 **한 관문에서 전부**(R31 ① · R30 ①)")

# ── ⑤ ★ 폭 정합이 코드로 강제된다
segs = eval(re.search(r"SEGS = (\{[^}]*\})", SRC_SET, re.S).group(1))
wp = eval(re.search(r"WIDTH_PAIRS = (\([^\n]*\))", SRC_SET).group(1))
iw = eval(re.search(r"INWIN_PAIR\s*= (\([^\n]*\))", SRC_SET).group(1))
for a, b in tuple(wp) + (tuple(iw),):
    wa = segs[a][1] - segs[a][0]; wb = segs[b][1] - segs[b][0]
    assert wa == wb, f"❌ 폭이 다르다 {a}({wa}) vs {b}({wb}) — R27 ③ 위반"
gp = SRC_D[SRC_D.index("def gate_pair("):SRC_D.index("# ── P1")]
assert "raise AssetError" in gp and "폭 불일치" in gp, \
    "❌ 폭 정합이 **코드로 강제**되지 않는다 — 주석은 Q7-M 에서 이미 실패했다"
print("  ✅ ⑤ 폭 정합 코드 강제 · 짝 " + " · ".join(
    f"{a}/{b}({segs[a][1]-segs[a][0]})" for a, b in tuple(wp) + (tuple(iw),)))

# ── ⑥ null SE 전파 · 셔플 · ★ 프로브도 실측(P7)
assert "NSE" in SRC_C and "std(ddof=1)" in SRC_C, "❌ null 의 셔플 SE 를 안 낸다"
assert "rng.normal(0.0, 1.0, len(ix)) * se[ix]" in SRC_D, "❌ null 오차를 CI 에 안 흔든다"
n_shuf = int(re.search(r"^N_SHUF\s*=\s*(\d+)", SRC_SET, re.M).group(1))
assert n_shuf >= 20, f"❌ 셔플 {n_shuf}회"
assert "for a in ARMS:" in SRC_C, "❌ null 을 일부 팔만 잰다 — P7 은 **전 팔 실측**이다"
assert re.search(r"NULL\[[a-z]\]\[m\]\[a\]\[:\]\s*=\s*0\.5", SRC_C) is None, \
    "❌ 순수 특징의 null 을 0.5 로 **가정**하고 있다 — P7 은 재라고 했다"
assert "가정이 아니라 실측" in SRC_E, "❌ P7 결과를 읽는 자리가 없다"
print(f"  ✅ ⑥ 셔플 {n_shuf}회 · null SE 전파(R26 ②) · **프로브·순수특징도 실측**(P7)")

# ── ⑦ ★ 규칙 체크리스트
assert "RULE_CHECK" in SRC_SET, "❌ 사전등록 규칙 체크리스트가 없다"
for r_ in ("R17", "R25", "R26 ②", "R27 ③", "R28 ①", "R28 ②", "R28 ③",
           "R29 ①", "R29 ②", "R30 ③", "R31 ①", "R31 ②", "R31 ③", "R31 ④", "R31 ⑤"):
    assert r_ in SRC_SET, f"❌ 체크리스트에 {r_} 가 없다"
print("  ✅ ⑦ 사전등록 규칙 체크리스트에 R17·R25~R31 전부(R29 ③)")

# ── ⑧ ★ 측정 불가 분기 금지
assert 'un_ = lambda k: VERD.get(k, "").startswith("⛔")' in SRC_FIG, "❌ 측정 불가 검사가 없다"
for g_ in ("P1", "P2", "P3"):
    assert f'un_("{g_}")' in SRC_FIG, f"❌ {g_} 결론 분기가 측정 불가를 먼저 안 거른다"
assert 'for k in ("P1", "P2", "P3")' in SRC_FIG, "❌ 요약이 관문을 다 안 낸다"
assert re.search(r'elif\s+"[A-Z0-9]+"\s+in\s+VERD', ALL_SRC) is None, \
    "❌ `elif \"X\" in VERD` 패턴이 남아 있다 — Q7-M 의 버그(R29 ②)"
assert "측정 불가" in gp and "n_ < 3" in gp, \
    "❌ 관문이 개체 부족을 ⛔ 로 안 찍는다 — 조용히 적은 n 으로 판정하면 안 된다(R17)"
assert "not un_(k)" in SRC_FIG, \
    "❌ ⛔ 관문에 등가·필요표본 주석이 그대로 붙는다 — 측정 못 한 값을 프레임 논의에 얹는 것도 R29 ② 위반이다"
print("  ✅ ⑧ 「측정 불가」가 어떤 결론 분기도 안 탄다(R29 ②)")

# ── ⑨ ★ 누출 바닥 = 기저 밖 모든 팔 · R25 구분 · 교차적합
for pat in ("np.nanmax(np.stack", "np.maximum(np.stack", "nanmax(np.stack"):
    assert pat not in ALL_SRC, f"❌ 개체별 max 바닥(R25): {pat}"
la = re.search(r"^LEAK_ARMS = (.+)$", SRC_D, re.M).group(1)
for must in ("f4", "f5", "PROBES"):
    assert must in la, f"❌ 누출 바닥에 {must} 가 없다 — f2 프로브만 보면 3배 과소평가(R31 ②)"
assert "R25 와 헷갈리지 말 것" in SRC_D, "❌ 보수적 차감과 R25 의 구분이 안 적혀 있다"
assert "fold = rng.permutation(len(tt)) % K" in SRC_A, "❌ 교차적합(R22)이 아니다"
assert "BONF3" in SRC_SET and "BONF3 * 100" in SRC_D, "❌ 1차 가족 보정이 없다"
assert "미보정" in SRC_D, "❌ 참고값을 미보정이라 안 적는다"
print("  ✅ ⑨ 누출 바닥 = 기저 밖 **모든 팔**(R31 ②) · R25 구분 · 교차적합(R22)")

# ── ⑩ ★ 주 분석 = 층화 · 잔차 팔 간 비교 금지
assert re.search(r'^PRIMARY_METHOD\s*=\s*"strat"', SRC_SET, re.M), \
    "❌ 주 분석이 층화가 아니다 — P8 / R31 ③ ⑤"
lad = eval(re.search(r"^LADDER\s*=\s*(\([^)]*\))", SRC_SET, re.M).group(1))
assert lad[0] == "raw" and lad[-1] == "strat", f"❌ 사다리가 약함→강함 순이 아니다 {lad}"
assert "R31 ⑤" in SRC_SET and "팔 간 수준 비교" in SRC_B, \
    "❌ 잔차 AUROC 의 팔 간 비교 금지가 명시돼 있지 않다(R31 ⑤)"
assert "def strat_auc(" in SRC_A and "def strat_key(" in SRC_A, "❌ 층화 함수가 없다"
print(f"  ✅ ⑩ 주 분석 = **층화**(P8) · 사다리 {' → '.join(lad)} · 잔차 팔 간 비교 금지")

# ── ⑪ ★ 코호트 보고가 관문보다 먼저 · 선택 편향 명시
assert "【P0】" in SRC_A, "❌ 코호트 보고(P0)가 없다"
assert SRC_A.index("【P0】") < len(SRC_A), "❌ P0 위치 확인 실패"
assert "선택 편향" in SRC_A and "R17" in SRC_A, "❌ 선택 편향을 명시하지 않는다"
assert "관문보다 **먼저**" in SRC_A, "❌ P0 가 관문보다 먼저라는 선언이 없다"
assert CODE.index([c for c in CODE if "【P-A】" in "".join(c["source"])][0]) < \
       CODE.index([c for c in CODE if "【P-D】" in "".join(c["source"])][0]), \
    "❌ 코호트 셀이 관문 셀보다 뒤에 있다"
print("  ✅ ⑪ 코호트(P0) 보고가 관문보다 먼저 · 선택 편향 명시(R17)")

# ── ⑫ ★ 민감도 격자 — 물려받은 어림 감사
ths = eval(re.search(r"^T_HI_SENS\s*=\s*(\([^)]*\))", SRC_SET, re.M).group(1))
gds = eval(re.search(r"^GUARD_SENS\s*=\s*(\([^)]*\))", SRC_SET, re.M).group(1))
assert len(ths) >= 3 and len(gds) >= 2, f"❌ 민감도 격자가 얇다 {ths} × {gds}"
assert "for th in T_HI_SENS:" in SRC_D and "for gd in GUARD_SENS:" in SRC_D, \
    "❌ 격자를 실제로 돌지 않는다"
assert "모형 어림" in SRC_A and "R28 ③" in SRC_SET, "❌ 물려받은 상수 감사 근거가 없다"
print(f"  ✅ ⑫ 민감도 격자 T_HI={ths} × 여유={gds} (R28 ① ③)")

# ── ⑬ ★ 감쇠를 기울기로 읽는다
assert "def slope_read(" in SRC_0, "❌ 사다리 판정 함수가 없다(R31 ③)"
assert "slope_read(" in SRC_D, "❌ 관문에서 사다리를 기울기로 안 읽는다"
assert "잔여 교란" in SRC_0, "❌ 단조 감쇠의 해석이 안 적혀 있다"
assert "부호가 아니라 기울기" in SRC_0 or "부호가 아니라 기울기" in SRC_D, \
    "❌ Q7-N 의 오독(부호 일치 = 강건)을 막는 문구가 없다"
print("  ✅ ⑬ 감쇠 사다리를 **기울기로** 읽는다(R31 ③)")

# ── ⑭ 그림 ASCII
bad = [t for t in re.findall(r'set_[xy]label\("([^"]*)"\)|label="([^"]*)"', SRC_FIG)
       for t in t if t and any(unicodedata.name(ch, "").startswith("HANGUL") for ch in t)]
assert not bad, f"❌ 그림 라벨에 한글: {bad}"
assert "한글이 없어" in SRC_FIG, "❌ 폰트 한계가 명시돼 있지 않다"
print("  ✅ ⑭ 그림 라벨 ASCII · 폰트 한계 명시")


# ═══════════════════════════════════════════════════════════════════════
print("\n### 동적 검사 — 노트북 함수를 그대로 꺼내 돌린다")


def grab(src, first, stop="run.log("):
    i = src.index(first)
    return src[i:src.index(stop, i)]


T_LO = float(re.search(r"^T_LO, T_HI = ([\d.]+), ([\d.]+)", SRC_SET, re.M).group(1))
T_HI = float(re.search(r"^T_LO, T_HI = ([\d.]+), ([\d.]+)", SRC_SET, re.M).group(2))
T_GUARD = int(re.search(r"^T_GUARD\s*=\s*(\d+)", SRC_SET, re.M).group(1))
LB_K = int(re.search(r"^LB_K\s*=\s*(\d+)", SRC_SET, re.M).group(1))
F2_BIN = float(re.search(r"^F2_BIN\s*=\s*([\d.]+)", SRC_SET, re.M).group(1))
RPRE = int(re.search(r"^RPRE\s*=\s*(\d+)", SRC_SET, re.M).group(1))

NS = dict(np=np, stats=stats)
exec("import numpy as np\nfrom scipy import stats\n"
     "from sklearn.linear_model import LogisticRegression\n"
     "from sklearn.metrics import roc_auc_score\n"
     f"BASIS_K = {bk}\nPROBE_K = {pk}\nHIST_K = 64\nLB_K = {LB_K}\nTREND_W = 8\n"
     f"F2_BIN = {F2_BIN}\nRPRE = {RPRE}\nSEGS = {segs}\n"
     f"T_LO, T_HI, T_GUARD = {T_LO}, {T_HI}, {T_GUARD}\n"
     "N_REPEAT, SEED0 = 1, 20260803\n"
     "class AssetError(RuntimeError): pass\n", NS)
exec(grab(SRC_0, "def decide(", "class AssetError"), NS)
exec(grab(SRC_A, "def t_overlap("), NS)
t_overlap, safe_mask = NS["t_overlap"], NS["safe_mask"]
safe_threshold, all_feats = NS["safe_threshold"], NS["all_feats"]
strat_key, strat_auc = NS["strat_key"], NS["strat_auc"]
build_scores = NS["build_scores"]
judge, need_n, slope_read, equiv = NS["judge"], NS["need_n"], NS["slope_read"], NS["equiv"]
from sklearn.metrics import roc_auc_score

# ── ⑮ ★★ 마스크 기하 — SAFE 비트는 모든 창에서 중첩이 정확히 0
rng = np.random.RandomState(7)
pre_t = np.round(rng.uniform(120.0, 520.0, 6000))
post_t = np.round(rng.uniform(120.0, 520.0, 6000))
sm = safe_mask(pre_t, post_t)
for k_, sg in segs.items():
    ov = t_overlap(pre_t, sg)
    assert float(ov[sm].max()) == 0.0, \
        f"❌ SAFE 인데 {k_} 에 직전 T 가 든다 (max 중첩 {ov[sm].max():.4f})"
pre_min, post_min = safe_threshold()
theory = max((RPRE - s[0] + T_GUARD) / T_HI for s in segs.values())
assert abs(pre_min - theory) < 1e-9, f"❌ 컷 {pre_min} ≠ 이론값 {theory}"
assert sm.any() and not sm.all(), "❌ 마스크가 전부/전무다 — 검사가 무의미하다"
assert float(pre_t[sm].min()) >= pre_min - 1e-9, "❌ 컷 아래 비트가 SAFE 에 남았다"
assert float(post_t[sm].min()) >= post_min - 1e-9, "❌ post 컷 아래 비트가 SAFE 에 남았다"
print(f"  ✅ ⑮ 마스크 기하 — SAFE 비트는 전 창에서 중첩 0 · 컷 pre ≥ {pre_min:.1f}"
      f"({pre_min/360*1000:.0f}ms) · post ≥ {post_min:.0f} · 남은 비율 {sm.mean():.3f}")


# ── ⑯ ★★ **결정적 짝** — 침입만 심으면 마스크 후 붕괴, 진짜 P 면 생존
def make_record(seed, n=2600, prev=0.20, base=400.0, sd=45.0,
                early_lo=0.35, early_hi=0.95, t_gain=0.0, p_gain=0.0, noise=0.6, L=300):
    """합성 레코드. **직전 T 를 `pre` 에 따라 실제로 그린다** — 그게 이 실험의 대상이다.

    `t_gain` : 직전 T 진폭. 위치가 `RPRE − 0.65·pre` 라 **이른 비트에서만 P 창에 든다**
    `p_gain` : 진짜 P 파 진폭(S 에서만 · index 68 = `p_late` 자리 · **`pre` 와 무관**)
    """
    rng = np.random.RandomState(seed)
    t = np.zeros(n, bool)
    t[rng.choice(np.arange(3, n - 3), size=max(int(n * prev), 60), replace=False)] = True
    pre = rng.normal(base, sd, n)
    pre[t] *= rng.uniform(early_lo, early_hi, int(t.sum()))
    pre = np.round(np.clip(pre, 110.0, 700.0))
    post = np.round(np.clip(np.r_[pre[1:], base], 110.0, 900.0))
    post[t] = np.round(np.clip(2.0 * base - pre[t], 110.0, 900.0))   # 보상성 휴지
    x = np.arange(L, dtype=float)
    B = rng.normal(0, noise, (n, 2, L))
    B += (0.9 * np.exp(-((x - 170.0) ** 2) / (2 * 22.0 ** 2)))[None, None, :]  # 자기 T
    if t_gain:                                    # 직전 T — 위치가 pre 에 따라 움직인다
        c = RPRE - 0.65 * pre
        B += (t_gain * np.exp(-((x[None, :] - c[:, None]) ** 2) / (2 * 20.0 ** 2))
              )[:, None, :]
    if p_gain:                                    # 진짜 P 파 — S 에서만 · 위치 고정
        B[t] += (p_gain * np.exp(-((x - 68.0) ** 2) / (2 * 9.0 ** 2)))[None, None, :]
    return B.astype("float32"), t, pre.astype(float), post.astype(float)


def pair_diff(seed_list, pa="p_full", pb="stt", **kw):
    """(pa AUROC − pb AUROC) 를 전체 / SAFE 코호트에서. 두 팔 모두 **같은 비트 집합**."""
    out = {"all": [], "safe": []}
    for sd_ in seed_list:
        B, t, pre, post = make_record(sd_, **kw)
        F = all_feats(pre, post)
        MORPH = {k: np.ascontiguousarray(B[:, :, a:b]) for k, (a, b) in segs.items()}
        for coh, sub in (("all", None), ("safe", safe_mask(pre, post))):
            tt = t if sub is None else t[sub]
            if int(tt.sum()) < 15 or int((~tt).sum()) < 15:
                continue
            S = build_scores(F, tt, MORPH, 20260803, 3, sub=sub)
            assert S is not None, f"합성 코호트[{coh}]에서 교차적합이 실패했다"
            out[coh].append(roc_auc_score(tt.astype(int), S[pa])
                            - roc_auc_score(tt.astype(int), S[pb]))
    return {k: float(np.mean(v)) if v else float("nan") for k, v in out.items()}


SEEDS = [101, 102, 103, 104]
INTRUDE = pair_diff(SEEDS, t_gain=3.0, p_gain=0.0)     # 침입만 — 진짜 P 없음
GENUINE = pair_diff(SEEDS, t_gain=0.0, p_gain=1.6)     # 진짜 P 만 — 침입 없음
assert INTRUDE["all"] > 0.10, \
    f"❌ 침입을 심었는데 전체 코호트에서 P 우위가 {INTRUDE['all']:+.4f} — 시나리오가 안 섰다"
assert abs(INTRUDE["safe"]) < 0.05, \
    (f"❌ **마스크가 침입을 안 지운다** — SAFE 에서 {INTRUDE['safe']:+.4f} 가 남았다. "
     "마스크가 이걸 못 지우면 P1 은 아무것도 못 묻는다")
assert GENUINE["all"] > 0.10 and GENUINE["safe"] > 0.08, \
    (f"❌ **마스크가 진짜 P 까지 지운다** — SAFE 에서 {GENUINE['safe']:+.4f}. "
     "그러면 P1 붕괴를 「침입이었다」로 못 읽는다(마스크가 다 지우니까)")
print(f"  ✅ ⑯ 결정적 짝 — 침입만: all {INTRUDE['all']:+.4f} → safe **{INTRUDE['safe']:+.4f}"
      f"(붕괴)** | 진짜 P: all {GENUINE['all']:+.4f} → safe **{GENUINE['safe']:+.4f}(생존)**")

# ── ⑰ ★ strat_auc 항등식 — 층 키에 들어간 f1 은 칸 안에서 상수 → 정확히 0.5
B, t, pre, post = make_record(201, t_gain=2.0, p_gain=1.0)
F = all_feats(pre, post)
key = strat_key(F, None)
v_f1, ks, den = strat_auc(F["f1"], t, key)
assert den >= 1, "❌ 층화 칸이 하나도 안 생겼다 — 합성 코호트가 너무 흩어져 있다"
assert abs(v_f1 - 0.5) < 1e-9, f"❌ 층 키에 든 f1 의 층화 AUROC 가 {v_f1:.9f} (0.5 여야)"
v_raw = roc_auc_score(t.astype(int), F["f1"])
assert abs(v_raw - 0.5) > 0.05, f"❌ f1 이 무층화에서도 {v_raw:.4f} — 통제 검증이 무의미하다"
print(f"  ✅ ⑰ strat_auc 항등식 — f1 무층화 {v_raw:.4f} → 층화 **{v_f1:.6f}** "
      f"(칸 {int(den)}쌍 · S {ks}비트)")

# ── ⑱ ★★ judge()/need_n()/slope_read() — **Q7-N 실패의 회귀 테스트**
# Q7-N 실측: p_full − stt = +0.0745 [+0.0387, +0.1112] · 여유 ±0.05.
# 관문은 「⚠️ 미결」만 찍었고 요약은 「등가도 우월도 아니다」라고 적었다 — 틀렸다(R31 ①).
eq, sup, nn, frame = judge(+0.0745, +0.0387, +0.1112, 59, 0.05)
assert eq.startswith("⚠️"), f"❌ 등가 판정이 {eq} — 미결이어야 한다"
assert sup.startswith("✅"), f"❌ **우월성을 놓쳤다** ({sup}) — CI 하한 +0.0387 이 0 을 뗀다"
assert nn is None, "❌ 점추정이 여유 밖인데 **등가 불가**로 안 찍는다(R31 ①)"
assert "우월성" in frame, "❌ 프레임 전환 안내가 없다"
# 폭 32 판본: 점추정이 여유 안 → 필요 개체가 **유한하게** 나와야 한다(Q7-N 실측 276)
eq2, sup2, nn2, _ = judge(+0.0310, -0.0088, +0.0708, 59, 0.05)
assert nn2 is not None and np.isfinite(nn2) and nn2 > 59, \
    f"❌ 필요 개체가 {nn2} — 현재 표본보다 커야 한다(R30 ①)"
assert sup2.startswith("⚠️"), f"❌ 우월성이 {sup2} — CI 가 0 을 걸치므로 미결이어야 한다"
for lo, hi, mg, want in ((-0.02, +0.03, 0.05, "✅"), (-0.09, +0.05, 0.05, "⚠️"),
                         (+0.06, +0.12, 0.05, "❌"), (-0.05, +0.05, 0.05, "⚠️")):
    assert equiv(lo, hi, mg).startswith(want), f"❌ equiv([{lo},{hi}],{mg})"
# 사다리: Q7-N 의 단조 감쇠는 「강건」이 아니라 「잔여 교란」으로 읽혀야 한다
assert "잔여 교란" in slope_read([0.0745, 0.0621, 0.0564, 0.0466, 0.0359]), \
    "❌ Q7-N 의 단조 감쇠를 잔여 교란으로 안 읽는다(R31 ③)"
assert "잔여 교란" not in slope_read([0.070, 0.069, 0.071, 0.068, 0.070]), \
    "❌ 평평한 사다리를 잔여 교란으로 오독한다"
print(f"  ✅ ⑱ judge() — Q7-N 의 +0.0745 를 등가 {eq} · 우월성 **{sup}** · "
      f"등가 **불가** 로 정확히 가른다 | 폭 32 필요 개체 ≈ {nn2:.0f}")

print("\n✅ Q7-P 픽스처 18/18 통과")
