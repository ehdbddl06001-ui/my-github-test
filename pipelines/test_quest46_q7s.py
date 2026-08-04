"""퀘스트46 Q7-S(개인 내 vs 교차환자) 픽스처.

Q7-R(`ailab-2026-0067`)의 R1(교차환자 ΔAUPRC −0.0115)과 R5(개체 내 P−ST +0.0974)는
모순이 아니라 **추정 대상이 다르다**. Q7-S 는 그걸 주 가설로 승격하고, 동시에 Q7-R 의
교정 결함 넷을 코드로 고친다.

픽스처의 핵심은 셋이다:

    **`detect()` 가 Q7-R 의 오판을 재현하지 않는가** — 회수 +0.0016 · MDE 0.0300 인데
    기저가 유의하다는 이유로 ✅ 가 찍혔었다. 이제 **회수로만** 판정한다
    **`snr_select()` 가 실측 효과 근방에서 고르는가** — Q7-R 실측 표를 넣으면 `raw` 가
    아니라 `strat` 이 나와야 한다(순위가 진폭에 따라 뒤집힌다)
    **개인화 대조가 공정한가** — (i)LORO 와 (ii)개인화를 **같은 평가 비트**에서 비교하고,
    개인화에 쓴 비트는 **양쪽 다** 평가에서 빠져야 한다

정적 검사:
  ① `run.*` API(finish dict) · fallback 부재(R16)
  ② ★★ `DETECT_RULE` 이 **문자열로 출력**되는가(R34 ①) — Q7-R 은 규칙이 어디에도 없었다
  ③ ★★ `detect()` 가 **회수로만** 판정하는가 — 기저 유의성이 안 들어가는가
  ④ ★★ `snr_select()` 가 **회수/MDE** 를 **실측 효과 근방**에서 평균하는가(R34 ②)
  ⑤ ★★ 주입 격자가 0.001 까지 내려가는가(R33 ②) · 감쌈 판정·출력
  ⑥ ★★ 구성 보장 음성 대조 — **같은 레코드의 무작위 다른 비트**(R34 ③)
  ⑦ ★★ Δ 의 **영점 대조 팔**(`noise5`·`shuf5`)이 있고 `shuf5` 가 **레코드 안에서** 치환되는가
  ⑧ ★★ 개인화가 **같은 평가 비트**에서 비교되고 쓴 비트를 뺐는가(R22)
  ⑨ ★ `f2_k` **전 계열**이 기저에 들어가고 프로브가 계열 **밖**인가(무한회귀 종결)
  ⑩ ★ 누출 바닥이 **부트스트랩 max + 팔 개수 민감도**인가
  ⑪ ★ **필요 표본을 출력**하는가(R30 ① — Q7-R 이 안 셌다) · DB 풀링 전제 명시
  ⑫ ★ **하드코딩 분기 문턱이 없는가**(R34 ④)
  ⑬ ★ 종결 조건이 코드에 있는가(R34 ⑤) · `dr` 이 버그가 아니라는 근거
  ⑭ 「측정 불가」가 어떤 결론 분기도 안 타는가(R29 ②) · 그림 ASCII

동적 검사 — 노트북 함수를 **그대로 꺼내** 돌린다:
  ⑮ ★★ `detect()` — Q7-R 의 `raw` a=0.005(회수 +0.0016 · MDE 0.0300)를 **❌** 로 찍는가
  ⑯ ★★ `snr_select()` — Q7-R 실측 표에서 `raw` 가 아니라 **`strat`** 을 고르는가
  ⑰ ★ `judge()` — MDE 아래를 측정 한계로 · 필요 표본을 계산
  ⑱ ★ `partial_auc()` 건전성
"""
import os, sys, json, re
import unicodedata
import numpy as np
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
NB = json.load(open(os.path.join(ROOT, "notebooks", "quest46_q7s_personalize.ipynb")))
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
SRC_A, SRC_B = cell("【S-A】"), cell("【S-B】")
SRC_C, SRC_D = cell("【S-C】"), cell("【S-D】")
SRC_E, SRC_F, SRC_FIG = cell("【S-E】"), cell("【S-F】"), cell("【S-G】")
ALL_SRC = "".join("".join(c["source"]) for c in CODE)

print("### 정적 검사")

# ── ①
for m in ("run.log(", "run.save_json(", "run.save_fig(", "run.finish("):
    assert m in ALL_SRC, f"❌ {m} 가 없다"
assert re.search(r"run\.finish\(\s*\{", ALL_SRC), "❌ finish 에 dict 를 안 넘긴다"
assert "fallback 없음" in cell("【S-0a】"), "❌ R16 표기가 없다"
print("  ✅ ① run.* API(finish dict) · fallback 부재(R16)")

# ── ② ★★ 검출 규칙을 문자열로 출력 (R34 ①)
assert "DETECT_RULE" in SRC_0, "❌ 검출 규칙 상수가 없다"
assert "DETECT_RULE" in SRC_D and "DETECT_RULE" in SRC_FIG, \
    "❌ 검출 규칙을 **출력**하지 않는다 — Q7-R 은 규칙이 어디에도 없어 오판을 못 잡았다"
assert "기저의 유의성은 판정에 **들어가지 않는다**" in SRC_0, "❌ 규칙 문장이 불완전하다"
print("  ✅ ② `DETECT_RULE` 을 상수로 두고 관문·요약에서 **출력**한다(R34 ①)")

# ── ③ ★★ detect() 가 회수로만 판정
assert "def detect(" in SRC_0, "❌ detect() 가 없다"
dt = SRC_0[SRC_0.index("def detect("):SRC_0.index("def snr_select(")]
assert "rec_lo > 0" in dt and "rec_mean > m_" in dt, \
    "❌ 검출이 (회수 CI 하한 > 0) AND (회수 > MDE) 가 아니다(R34 ①)"
assert "base" not in dt.replace("기저", ""), "❌ detect() 가 기저를 본다 — 들어가면 안 된다"
assert "rc = rm - bm" in SRC_D and "rc_lo = rlo - bm" in SRC_D, \
    "❌ 관문에서 회수를 (주입 − 기저)로 안 만든다"
assert "detect(rc, rc_lo, m_)" in SRC_D, "❌ 관문이 detect() 를 안 쓴다"
print("  ✅ ③ `detect()` 가 **회수로만** 판정 — 기저 유의성이 안 들어간다(R34 ①)")

# ── ④ ★★ SNR 선택 (R34 ②)
assert "def snr_select(" in SRC_0, "❌ snr_select() 가 없다"
ss = SRC_0[SRC_0.index("def snr_select("):SRC_0.index("class AssetError")]
assert 'd["rec"][a] / d["mde"]' in ss, "❌ SNR = 회수/MDE 가 아니다"
assert "target_a" in ss, "❌ 실측 효과 근방에서 평균하지 않는다"
tgt = eval(re.search(r"^TARGET_A\s*=\s*(\([^)]*\))", SRC_SET, re.M).group(1))
assert max(tgt) <= 0.02, f"❌ SNR 평가 구간 {tgt} 가 실측 효과(a≈0.008)에서 멀다"
assert "snr_select(ROWS, TARGET_A)" in SRC_D, "❌ 관문에서 SNR 선택을 안 쓴다"
assert "MDE 단독" in ss or "MDE 단독" in SRC_D, "❌ MDE 단독이 왜 안 되는지 근거가 없다"
print(f"  ✅ ④ 선택 = **SNR(회수/MDE)** · 평가 구간 {tgt}(실측 효과 근방)(R34 ②)")

# ── ⑤ ★★ 격자 (R33 ②)
amps = eval(re.search(r"^AMPS\s*=\s*(\([^)]*\))", SRC_SET, re.M).group(1))
assert min(amps) <= 0.001, f"❌ 격자 최소 {min(amps)} — Q7-R 은 0.005 에서 이미 전부 검출됐다"
assert len(amps) >= 5, f"❌ 격자가 얇다 {amps}"
assert "BRACKET" in SRC_D and "미확정" in SRC_D, "❌ 감쌈 판정·출력이 없다"
print(f"  ✅ ⑤ 주입 격자 {amps} · 감쌈 판정 출력(R33 ②)")

# ── ⑥ ★★ 구성 보장 음성 대조 (R34 ③)
assert "NEG_SHUF" in SRC_B, "❌ 구성 보장 음성 대조가 없다"
wa = SRC_B[SRC_B.index("def win_arr("):SRC_B.index("NEG_SHUF =")]
assert "shuffle_neg" in wa and "rng.permutation(len(Bw))" in wa, \
    "❌ 음성 대조가 **같은 레코드의 무작위 다른 비트**가 아니다(R34 ③)"
assert "구성으로 보장" in wa, "❌ R34 ③ 근거가 안 적혀 있다"
assert "NEG_SHUF" in SRC_D and "NEG_SHUF" in SRC_F, "❌ 관문이 구성 보장 음성 대조를 안 쓴다"
print("  ✅ ⑥ 구성 보장 음성 대조 = 같은 레코드 무작위 다른 비트(R34 ③)")

# ── ⑦ ★★ Δ 의 영점
ctrl = eval(re.search(r"^CTRL_ARMS\s*=\s*(\([^)]*\))", SRC_SET, re.M).group(1))
assert set(ctrl) == {"noise5", "shuf5"}, f"❌ 영점 대조 팔이 {ctrl}"
ff = SRC_E[SRC_E.index("def feats_for("):SRC_E.index("def fit_eval(")]
assert "NOISE5" in ff, "❌ 순수 잡음 5차원 팔이 없다"
assert "RID[m_] == u" in ff and "rr.permutation" in ff, \
    "❌ `shuf5` 가 **레코드 안에서** 치환되지 않는다 — 주변분포가 안 보존된다"
assert '"S2"' in SRC_E and "영점" in SRC_E, "❌ S2 관문이 없다"
print("  ✅ ⑦ Δ 영점 대조 `noise5`·`shuf5`(레코드 안 치환) — −0.0115 의 해석 근거")

# ── ⑧ ★★ 개인화 공정성
assert "ev = np.setdiff1d(te0, used)" in SRC_E, \
    "❌ 개인화에 쓴 비트를 평가에서 안 뺀다(R22 누수)"
assert "같은 평가 비트" in SRC_E, "❌ (i)/(ii) 공정 비교 근거가 없다"
assert "base_i = fit_eval" in SRC_E and "base_p[k] = fit_eval" in SRC_E, \
    "❌ LORO 와 개인화의 리듬 기저를 따로 안 낸다"
kp = eval(re.search(r"^K_PERS\s*=\s*(\([^)]*\))", SRC_SET, re.M).group(1))
assert len(kp) >= 3 and min(kp) <= 5, f"❌ 개인화 라벨 격자가 얇다 {kp}"
print(f"  ✅ ⑧ 개인화 k={kp} · **같은 평가 비트** · 쓴 비트 제외(R22)")

# ── ⑨ ★ f2 전 계열 + 계열 밖 프로브
fk = eval(re.search(r"^FULL_K\s*=\s*(tuple\(range\([^)]*\)\))", SRC_SET, re.M).group(1))
pk = eval(re.search(r"^PROBE_K\s*=\s*(\([^)]*\))", SRC_SET, re.M).group(1))
assert len(fk) >= 20 and min(fk) <= 4 and max(fk) >= 32, f"❌ 계열이 얇다 {fk}"
assert not (set(pk) & set(fk)), f"❌ 프로브가 계열 안이다 {pk}"
assert min(pk) > max(fk), f"❌ 프로브가 계열 밖이 아니다 {pk} vs max {max(fk)}"
bm = SRC_A[SRC_A.index("def basis_mat("):SRC_A.index("def prep(")]
assert "FULL_K" in bm, "❌ 확장 기저가 f2 전 계열을 안 담는다 — 무한회귀가 안 끝난다"
assert "무한회귀" in bm, "❌ 무한회귀 종결 근거가 안 적혀 있다"
print(f"  ✅ ⑨ 기저에 `f2_k` 전 계열 k={min(fk)}..{max(fk)}({len(fk)}개) · 계열 밖 프로브 {pk}")

# ── ⑩ ★ 누출 바닥 부트스트랩 + 팔 개수 민감도
assert "def leak_boot(" in SRC_D, "❌ 누출 바닥 부트스트랩이 없다"
lb = SRC_D[SRC_D.index("def leak_boot("):SRC_D.index("CONFIG[\"leak\"]")]
assert "LEAK_SUBSET_SIZES" in SRC_D, "❌ 팔 개수 민감도가 없다 — 선택 편의를 못 본다"
assert "선택 편의" in SRC_D, "❌ 선택 편의 진단 문구가 없다"
print("  ✅ ⑩ 누출 바닥 = 부트스트랩 max + 팔 개수 민감도(선택 편의 진단)")

# ── ⑪ ★ 필요 표본 · DB 풀링
assert "need_n(" in SRC_F and "필요 표본" in SRC_F, "❌ 필요 표본을 안 낸다(R30 ①)"
assert "POOL" in SRC_F and "SVDB" in SRC_F and "INCART" in SRC_F, "❌ DB 풀링 도달 판정이 없다"
for w in ("샘플레이트", "고정효과", "이질성"):
    assert w in SRC_F, f"❌ DB 풀링 전제 '{w}' 가 안 적혀 있다"
assert "124" in SRC_F, "❌ Q7-R 이 안 센 124 레코드를 참조하지 않는다"
print("  ✅ ⑪ 필요 표본 출력 + DB 풀링 도달 판정 + 전제(리샘플·고정효과·이질성) 명시")

# ── ⑫ ★ 하드코딩 문턱 부재 (R34 ④)
bad = re.findall(r"if abs\([^)]*\) < 0\.0[0-9]+", ALL_SRC)
assert not bad, f"❌ 하드코딩 분기 문턱이 남아 있다: {bad} (R34 ④)"
assert "abs(mean) < m_" in SRC_0, "❌ 측정 한계 판정이 MDE 에서 유도되지 않는다"
print("  ✅ ⑫ 하드코딩 분기 문턱 없음 — 전부 CI/MDE 에서 유도(R34 ④)")

# ── ⑬ ★ 종결 조건 · dr 근거
assert "종결 조건" in SRC_FIG and "300" in SRC_FIG, "❌ 사전등록 종결 조건이 코드에 없다(R34 ⑤)"
assert "더 돌지 않는다" in SRC_FIG, "❌ 종결 문구가 없다"
assert "버그가 아니었다" in SRC_SET and "확장 기저 안" in SRC_SET, \
    "❌ `dr` 의 0.5000 이 항등식이라는 근거가 없다"
print("  ✅ ⑬ 종결 조건(필요표본 >300 → 갈래 종료) · `dr` 항등식 근거")

# ── ⑭ 측정 불가 · ASCII
assert 'un_ = lambda k: VERD.get(k, "").startswith("⛔")' in SRC_FIG, "❌ 측정 불가 검사가 없다"
assert re.search(r"un_\(g\).*for g in", SRC_FIG), "❌ 결론 분기가 측정 불가를 안 거른다"
assert re.search(r'elif\s+"[A-Z0-9]+"\s+in\s+VERD', ALL_SRC) is None, "❌ Q7-M 분기 버그 패턴"
bad = [t for t in re.findall(r'set_[xy]label\("([^"]*)"\)|label="([^"]*)"', SRC_FIG)
       for t in t if t and any(unicodedata.name(ch, "").startswith("HANGUL") for ch in t)]
assert not bad, f"❌ 그림 라벨에 한글: {bad}"
assert "한글이 없어" in SRC_FIG, "❌ 폰트 한계가 명시돼 있지 않다"
print("  ✅ ⑭ 「측정 불가」가 어떤 분기도 안 탄다(R29 ②) · 그림 ASCII")


# ═══════════════════════════════════════════════════════════════════════
print("\n### 동적 검사 — 노트북 함수를 그대로 꺼내 돌린다")

NS = dict(np=np, stats=stats)
exec("import numpy as np\nfrom scipy import stats\nfrom sklearn.metrics import roc_curve\n"
     "class AssetError(RuntimeError): pass\n", NS)
exec(SRC_0[SRC_0.index("def decide("):SRC_0.index("class AssetError")], NS)
exec(SRC_E[SRC_E.index("def partial_auc("):SRC_E.index("run.log(")], NS)
detect, snr_select, judge = NS["detect"], NS["snr_select"], NS["judge"]
mde_f, partial_auc = NS["mde"], NS["partial_auc"]

# ── ⑮ ★★ detect() — Q7-R 오판 회귀 테스트
# Q7-R raw a=0.005: 회수 +0.0016 · MDE 0.0300. 기저 [+0.0630,+0.1230] 이 유의하다는
# 이유로 ✅ 가 찍혔었다. 회수만 보면 명백히 ❌ 여야 한다.
assert not detect(0.0016, -0.0100, 0.0300), \
    "❌ Q7-R 의 raw a=0.005(회수 +0.0016 · MDE 0.0300)를 여전히 검출로 찍는다"
assert not detect(0.0400, -0.0050, 0.0300), "❌ 회수 CI 가 0 을 걸치는데 검출로 찍는다"
assert not detect(0.0200, 0.0050, 0.0300), "❌ 회수가 MDE 아래인데 검출로 찍는다"
assert detect(0.0400, 0.0120, 0.0300), "❌ 회수>MDE 이고 CI 하한>0 인데 검출이 아니다"
print("  ✅ ⑮ `detect()` — Q7-R 의 raw a=0.005 를 **❌** 로 · MDE 위 + CI 하한>0 만 ✅")

# ── ⑯ ★★ snr_select() — Q7-R 실측에서 raw 가 아니라 strat 이 나와야 한다
Q7R = {
    "raw":   dict(mde=0.0300, rec={0.005: 0.0016, 0.010: 0.0033, 0.020: 0.0140,
                                   0.030: 0.0299, 0.050: 0.0534}),
    "lin":   dict(mde=0.0372, rec={0.005: 0.0031, 0.010: 0.0007, 0.020: 0.0153,
                                   0.030: 0.0314, 0.050: 0.0613}),
    "rank":  dict(mde=0.0343, rec={0.005: 0.0020, 0.010: 0.0022, 0.020: 0.0123,
                                   0.030: 0.0277, 0.050: 0.0451}),
    "strat": dict(mde=0.1131, rec={0.005: 0.0040, 0.010: 0.0147, 0.020: 0.0733,
                                   0.030: 0.1027, 0.050: 0.1748}),
    "dr":    dict(mde=0.1211, rec={0.005: 0.0025, 0.010: 0.0049, 0.020: 0.0432,
                                   0.030: 0.0931, 0.050: 0.1627}),
}
snr_near, best_near = snr_select(Q7R, (0.005, 0.010, 0.020))
assert best_near == "strat", \
    f"❌ 실측 효과 근방에서 `{best_near}` 를 골랐다 — Q7-R 실측으로는 strat 이어야 한다"
snr_far, best_far = snr_select(Q7R, (0.030, 0.050))
assert best_far == "raw", f"❌ 큰 진폭에서는 raw 가 이겨야 하는데 {best_far}"
assert best_near != best_far, "❌ 순위가 진폭에 안 뒤집힌다 — 그러면 R34 ② 의 근거가 없다"
print(f"  ✅ ⑯ `snr_select()` — 근방(a≤0.02) **{best_near}**(SNR {snr_near[best_near]:.3f}) vs "
      f"큰 진폭 **{best_far}**({snr_far[best_far]:.3f}) — **순위가 뒤집힌다**")

# ── ⑰ ★ judge()
eq, sup, nn, m_, frame = judge(0.0293, -0.0873, 0.1466, 55, 0.05)
assert "측정 한계" in frame, "❌ MDE 아래를 측정 한계로 안 찍는다"
eq2, sup2, nn2, m2, fr2 = judge(-0.0115, -0.0271, 0.0018, 59, 0.01)
assert np.isfinite(m2) and abs(m2 - 0.01445) < 1e-4, f"❌ MDE {m2}"
assert nn2 is None, "❌ 점추정 −0.0115 가 여유 ±0.01 밖인데 등가 필요표본을 낸다"
eqA, supA, nnA, mA, frA = judge(0.005, -0.0095, 0.0195, 59, 0.01)
assert nnA is not None and abs(nnA - 59 * (0.01450 / 0.005) ** 2) < 1.0, \
    f"❌ 필요 표본 계산이 틀렸다 {nnA}"
print(f"  ✅ ⑰ `judge()` — Q7-R R1(MDE {m2:.4f})을 등가 불가로 · 필요표본 {nnA:.0f} 계산")

# ── ⑱ ★ partial_auc
rng = np.random.RandomState(5)
n = 4000
y = (rng.uniform(size=n) < 0.08).astype(int)
p_sep = partial_auc(y, y + rng.normal(0, 0.01, n), 0.95)
p_rnd = partial_auc(y, rng.normal(size=n), 0.95)
p_wk = partial_auc(y, y * 0.35 + rng.normal(0, 1.0, n), 0.95)
assert p_sep > 0.95 and p_rnd < 0.15 and p_rnd < p_wk < p_sep, \
    f"❌ partial_auc {p_rnd:.3f}/{p_wk:.3f}/{p_sep:.3f}"
print(f"  ✅ ⑱ `partial_auc` — 무작위 {p_rnd:.3f} < 약함 {p_wk:.3f} < 완전분리 {p_sep:.3f}")

print("\n✅ Q7-S 픽스처 18/18 통과")
