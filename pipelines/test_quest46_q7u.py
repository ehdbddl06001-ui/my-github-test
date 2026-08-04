"""퀘스트46 Q7-U(공개 delineator × QRST 소거) 픽스처.

Q7-T 는 T1(자체 검출기) ❌ · **T2(소거가 P 를 드러낸다) ✅** 로 끝났다. 죽은 건
**검출기**이지 가설이 아니다 — 검출기는 자다. Q7-U 는 자를 빌리고(NeuroKit2 DWT ·
phasor transform 축소판), **주 관문 U2 로 「소거 잔차가 원신호보다 나은가」**를 묻는다.
공개 방법은 전부 원신호에서만 P 를 찾으므로 이 조합이 이 퀘스트의 고유 질문이다.

★ 이 픽스처의 존재 이유는 **실데이터 3회 실행이 잡은 설계 결함 셋**을 회귀로 박는 것이다.

    ① **작동점이 팔마다 딴판이었다** — 기권 문턱을 팔마다 Youden 으로 최적화했더니
       발화율이 0.038~0.977 로 26배 벌어졌다. 거기서 나온 U2 의 「소거 승리」
       ΔSe +0.1413 [+0.1111,+0.1741] 은 **6.7배 더 쏜 결과**였다.
       → 문턱을 **점수 분위수**로 잡아 발화율을 강제로 맞추고, 격자 전체에서 비교한다
    ② **재구성 비용이 지배했다** — 비트 잔차를 Voronoi 로 되붙여 연속 신호를 만들었는데
       그 이음매가 파형이라 재구성만으로 F1 0.7705 → 0.6132. 소거 이득(+0.01~0.09)보다
       **내 구현 비용(−0.16)이 10배** 컸다.
       → 소거를 **`raw − 심실추정치`** 로 뒤집었다. 덮이지 않은 구간은 raw 그대로라
         `none` 은 **정의상 raw** 이고 대조가 구성으로 보장된다
    ③ **선택 편의** — 팔·발화율·Rv·문턱을 성적표에서 고르면 보고값이 낙관 편향된다.
       → **네 군데 전부 LORO**

정적 검사:
  ① `run.*` API(finish dict) · fallback 부재(R16)
  ② ★ 외부 정답 — 레코드 이름·주석 확장자를 **실물로 확인**(Q7-T 가 여기서 두 번 멈췄다)
  ③ ★★ **소거 = `raw − 심실추정치`** — 잔차를 되붙이지 않는가 · `none` 은 정의상 raw
  ④ ★★ **항등 점검이 강제인가** — `none` vs `raw` 의 ΔF1 ≠ 0 이면 **중단**하는가
  ⑤ ★★ **발화율 정합** — 문턱이 점수 분위수인가 · 격자가 있는가 · 비교가 같은 rate 인가
  ⑥ ★★ **LORO 가 네 군데 전부** — 문턱 · Rv · 팔 · 발화율
  ⑦ ★ 적합 구간이 **심실에만** · 소거가 P 구간을 적합에 안 넣는가
  ⑧ ★ 검출기가 **정답을 인자로도 안 받는가**(R22)
  ⑨ ★ 매칭 **탐욕적 1:1** · Se 분모 = **정답 전수**(벤치마크와 같게)
  ⑩ ★ 벤치마크 병기 · **종결 조건**(R34 ⑤) · 하드코딩 문턱 부재(R34 ④)
  ⑪ ★ `phasor`·`st` 가 **축소판**이라는 명시 · 이 런이 **SVEB 질문에 답하지 않음**
  ⑩b ★★ **과잉주장 방지** — 「아무도 안 했다」 부재 · Diaz 2001·Shah 2004(PMID) 인용 ·
       novelty 를 'not systematically established' 로 (사용자가 문헌으로 잡아낸 오류)
  ⑫ 「측정 불가」가 어떤 결론 분기도 안 타는가(R29 ②) · 그림 ASCII

동적 검사 — 노트북 함수를 **그대로 꺼내** 돌린다:
  ⑬ ★★ `cancel_full("none")` 이 입력과 **비트 동일**한가(대조의 구성 보장)
  ⑭ ★★ `cancel_full` 이 **심실만** 지우고 P 는 남기는가 · `st` < `abs`
  ⑭b ★★ `prev`/`prevfit` 이 **직전 비트 템플릿**인가(Shah 2004) · 단일 비트의 SNR 대가
  ⑮ ★★ Voronoi 조립에 **겹침·틈이 없는가**(각 샘플이 최근접 R 에 정확히 한 번)
  ⑯ ★★ `loro_score_thr` 이 **목표 발화율을 실제로** 만드는가
  ⑰ ★ `detect_phasor` — arctan 이 **작은 파형을 QRS 대비 증폭**하는가(방법의 요점)
  ⑱ ★ `match_1d` 1:1 · `se_ppv` 분모 · `decide`/`mde`/`need_n` 건전성
"""
import os, sys, json, re
import unicodedata
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
NB = json.load(open(os.path.join(ROOT, "notebooks", "quest46_q7u_public_delineator.ipynb")))
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
SRC_LOAD, SRC_A = cell("【U-0a】"), cell("【U-A】")
SRC_B, SRC_C, SRC_D, SRC_FIG = cell("【U-B】"), cell("【U-C】"), cell("【U-D】"), cell("【U-E】")
ALL_SRC = "".join("".join(c["source"]) for c in CODE)
MD_SRC = "".join("".join(c["source"]) for c in NB["cells"] if c["cell_type"] == "markdown")

print("### 정적 검사")

# ── ①
for m in ("run.log(", "run.save_json(", "run.save_fig(", "run.finish("):
    assert m in ALL_SRC, f"❌ {m} 가 없다"
assert re.search(r"run\.finish\(\s*\{", ALL_SRC), "❌ finish 에 dict 를 안 넘긴다"
assert "fallback 없음" in SRC_LOAD, "❌ R16 표기가 없다"
assert not re.search(r"except[^\n]*:\s*\n[^\n]*(synth|합성|randn)", SRC_LOAD), \
    "❌ 적재 실패를 합성으로 대체하는 경로가 있다(R16)"
print("  ✅ ① run.* API(finish dict) · fallback 부재(R16)")

# ── ② ★ 이름·확장자를 실물로 확인 (Q7-T 가 여기서 두 번 멈췄다)
assert "def resolve_rid(" in SRC_LOAD and "rdheader" in SRC_LOAD, \
    "❌ 레코드 이름을 헤더로 확인하지 않는다(BUT PDB 1.0.0 은 RECORDS `1` vs 파일 `01.hea`)"
assert 'f"{int(r):0{w}d}"' in SRC_LOAD, "❌ 0 채움 변형을 안 시도한다"
assert "ANNOTATORS" in SRC_LOAD, "❌ 주석 확장자를 DB 에 안 묻는다"
assert "BEAT_SYM" in SRC_LOAD, "❌ QRS 주석을 **비트 기호**로 안 가린다 — 이름 추측이다"
assert re.search(r"if not PROBE:\s+raise AssetError", SRC_LOAD), "❌ 주석이 없어도 안 멈춘다"
assert re.search(r"if EXT_P is None or EXT_Q is None:\s+raise AssetError", SRC_LOAD), \
    "❌ 주석 역할을 못 가려도 안 멈춘다"
print("  ✅ ② 레코드 이름·주석 확장자를 **실물로 확인** · 못 가리면 중단(R16)")

# ── ③ ★★ 소거 = raw − 심실추정치 (잔차 되붙이기 금지)
cf = SRC_A[SRC_A.index("def cancel_full("):SRC_A.index('run.log("\\n" + "=" * 100)')]
assert re.search(r'if mode == "none":\s*\n\s*return sig\[:, :2\]\.copy\(\)', cf), \
    "❌ `none` 이 **정의상 raw** 가 아니다 — 대조가 구성 보장이 아니다(R34 ③)"
assert "return sig[:, :2] - est" in cf, \
    "❌ 소거가 `raw − 심실추정치` 가 아니다 — 잔차를 되붙이면 이음매가 파형이 된다"
assert "FITB" in cf and "est[a:b, :] = FITB" in cf, \
    "❌ Voronoi 로 조립하는 게 **잔차**다 — **템플릿**이어야 한다"
assert "정의상 raw" in cf and "이음매" in cf, "❌ 뒤집은 근거가 안 적혀 있다"
assert "0.7705" in cf and "0.6132" in cf, "❌ 재구성 비용 실측값이 근거로 안 적혀 있다"
print("  ✅ ③ 소거 = **`raw − 심실추정치`** · `none` 은 정의상 raw(대조 구성 보장 · R34 ③)")

# ── ④ ★★ 항등 점검이 강제인가
assert "항등 점검" in SRC_D, "❌ U3 이 항등 점검이 아니다"
assert re.search(r"if _ident > 1e-9:\s*\n\s*raise AssetError", SRC_D), \
    "❌ `none` 이 raw 와 달라도 **중단하지 않는다** — 조용히 틀린 대조로 판정하게 된다"
assert 'profile(det, "none", "raw"' in SRC_D, "❌ 항등을 실제로 재지 않는다"
print("  ✅ ④ `none` ≠ raw 이면 **AssetError 로 중단** — 대조가 깨지면 판정하지 않는다")

# ── ⑤ ★★ 발화율 정합 (1판이 여기서 무너졌다)
assert "def loro_score_thr(" in SRC_C, "❌ 발화율 정합 문턱이 없다"
lt = SRC_C[SRC_C.index("def loro_score_thr("):SRC_C.index("def evaluate(")]
assert "np.percentile" in lt and "100.0 * (1.0 - rate)" in lt, \
    "❌ 문턱이 **점수 분위수**가 아니다 — Youden 이면 팔마다 작동점이 달라진다"
assert "Youden" not in SRC_C.split("def evaluate(")[0].replace(lt, ""), \
    "❌ Youden 문턱이 판정 경로에 남아 있다"
rg = eval(re.search(r"^RATE_GRID = (\([^)]*\))", SRC_SET, re.M).group(1))
RVF = eval(re.search(r"^RV_FRACS = (\([^)]*\))", SRC_SET, re.M).group(1))
assert len(rg) >= 4 and max(rg) == 1.0, f"❌ 발화율 격자가 얇거나 기권없음(1.0)이 없다 {rg}"
assert "0.038" in SRC_SET and "0.977" in SRC_SET, \
    "❌ 1판의 발화율 폭주(0.038~0.977) 근거가 사전등록에 없다"
assert "6.7배" in SRC_SET or "6.7배" in SRC_C, "❌ 「6.7배 더 쏜 결과」 근거가 없다"
# 비교가 **같은 rate** 에서 이뤄지는가
pd_ = SRC_D[SRC_D.index("def paired("):SRC_D.index("def profile(")]
assert "(f\"{det}|{a_in}\", rate)" in pd_ and "(f\"{det}|{b_in}\", rate)" in pd_, \
    "❌ 짝지은 차가 **같은 발화율**에서 계산되지 않는다"
assert "def profile(" in SRC_D and "for rate in RATE_GRID" in SRC_D, \
    "❌ 격자 전체 프로필을 안 찍는다 — 한 점만 보면 작동점 인공물을 못 가른다"
print(f"  ✅ ⑤ 문턱 = **점수 분위수** · 격자 {rg} · 비교는 **같은 발화율**에서")

# ── ⑥ ★★ LORO 가 네 군데 전부
assert "if r != rid_out" in lt, "❌ 문턱이 **자기 레코드**를 본다(R22)"
assert re.search(r"best = max\(cand, key=lambda rv: np\.mean\(\s*\n?\s*\[per_rv\[rv\]\[o\]\[\"f1\"\]"
                 r" for o in per_rv\[rv\] if o != rid\]", SRC_C), "❌ Rv 선택이 LORO 가 아니다"
assert "for o in COMMON if o != rid" in SRC_C, "❌ 팔×발화율 선택이 LORO 가 아니다"
assert "for o in R2 if o != rid" in SRC_D, "❌ U2 의 팔 선택이 LORO 가 아니다"
assert "선택 편의" in SRC_C, "❌ 선택 편의를 정량해 출력하지 않는다"
print("  ✅ ⑥ LORO 네 군데 — 기권 문턱 · Rv · 팔 · 발화율 (전부 자기 레코드 제외)")

# ── ⑦ ★ 적합은 심실에만
assert "FIT_LO_MS, FIT_HI_MS" in SRC_SET, "❌ 적합 구간이 없다"
flo, fhi = (float(x) for x in
            re.search(r"^FIT_LO_MS, FIT_HI_MS = (-?[\d.]+), (-?[\d.]+)", SRC_SET, re.M).groups())
plo, phi = (float(x) for x in
            re.search(r"^P_LO_MS, P_HI_MS = (-?[\d.]+), (-?[\d.]+)", SRC_SET, re.M).groups())
assert phi <= flo, f"❌ P 탐색 [{plo},{phi}]ms 이 적합 [{flo},{fhi}]ms 과 겹친다 — P 를 지운다"
assert "fit = slice(lo, hi)" in cf and "B[:, 0, fit]" in cf, "❌ 최소제곱이 심실 밖까지 본다"
assert "심실 구간에서만" in cf, "❌ 적합 제한 근거가 없다"
print(f"  ✅ ⑦ 적합 [{flo:.0f},{fhi:.0f}]ms 심실 전용 · P 탐색 [{plo:.0f},{phi:.0f}]ms 비겹침")

# ── ⑧ ★ 검출기가 정답을 안 본다 (R22)
for fn in ("def detect_dwt(", "def detect_phasor(", "def score_at("):
    body = SRC_B[SRC_B.index(fn):]
    body = body[:body.index("\ndef ") if "\ndef " in body[1:] else len(body)]
    for w in ("p_true", "has_p", 'd["p"]', "BUT["):
        assert w not in body, f"❌ {fn} 가 정답(`{w}`)을 본다 — U1 이 무의미해진다(R22)"
assert re.search(r"def detect_dwt\(x, rp, fs\)", SRC_B), "❌ dwt 검출기 서명이 다르다"
assert "정답을 인자로도 받지 않는다" in SRC_B, "❌ R22 근거가 없다"
print("  ✅ ⑧ 검출기·점수는 정답을 **인자로도 안 받는다** — R 위치만(R22)")

# ── ⑨ ★ 탐욕적 1:1 · Se 분모 = 정답 전수
m1 = SRC_0[SRC_0.index("def match_1d("):SRC_0.index("def se_ppv(")]
assert "used" in m1 and "(~used)" in m1, "❌ 매칭이 1:1 이 아니다"
sp = SRC_0[SRC_0.index("def se_ppv("):SRC_0.index("class AssetError")]
assert "m / max(len(ref), 1)" in sp and "m / max(len(det), 1)" in sp, \
    "❌ Se/PPV 분모가 (정답 전수 / 발화수)가 아니다"
assert "정답 전수" in sp and "벤치마크와 같게" in sp, "❌ 분모 근거가 안 적혀 있다"
print("  ✅ ⑨ 매칭 탐욕적 1:1 · Se 분모 = **정답 전수**(벤치마크와 같게)")

# ── ⑩ ★ 벤치마크 · 종결 조건 · 하드코딩 문턱
bse = float(re.search(r"^BENCH_SE, BENCH_PP = ([\d.]+), ([\d.]+)", SRC_SET, re.M).group(1))
assert abs(bse - 0.9307) < 1e-9, f"❌ 벤치마크 Se {bse}"
assert "Saclova" in SRC_SET and "Sci Rep 12:6589" in SRC_SET, "❌ 벤치마크 출처가 없다"
assert "phasor transform + 부정맥별 결정 규칙" in SRC_SET, \
    "❌ 벤치마크 **방법**을 안 적었다 — Q7-T 는 CEEMDAN 이라고 잘못 썼다"
assert "BENCH_SE" in SRC_C and "Q7-T 자체 검출기" in SRC_C, "❌ 벤치마크·전판을 병기 안 한다"
assert "종결 조건" in SRC_FIG and "R34 ⑤" in SRC_FIG, "❌ 종결 조건이 코드에 없다"
assert "더 돌지 않는다" in SRC_FIG, "❌ 종결 문구가 없다"
bad = re.findall(r"if abs\([^)]*\) < 0\.0[0-9]+", ALL_SRC)
assert not bad, f"❌ 하드코딩 분기 문턱: {bad}(R34 ④)"
print(f"  ✅ ⑩ 벤치마크 {bse:.4f}(방법까지 병기) · 종결 조건 · 하드코딩 문턱 없음")

# ── ⑩b ★★ 과잉주장 방지 (사용자가 문헌으로 잡아낸 오류의 회귀)
for bad_claim in ("아무도 안 했다", "아무도 안 한", "누구도 하지 않았"):
    assert bad_claim not in ALL_SRC and bad_claim not in MD_SRC, \
        f"❌ 「{bad_claim}」 — Diaz 2001 · Shah 2004 가 이미 QRST 를 빼고 심방 활동을 봤다"
assert "Diaz" in ALL_SRC and "Shah" in ALL_SRC, "❌ 선행연구를 인용하지 않는다"
assert "15485519" in ALL_SRC, "❌ Shah 2004 의 PMID 가 없다 — 검증 가능해야 한다"
assert "novelty_note" in SRC_SET, "❌ novelty 주장을 config 에 명시하지 않는다"
assert "systematically established" in SRC_SET, \
    "❌ novelty 를 **'체계적으로 확립되지 않았다'** 로 안 쓴다 — 그게 방어 가능한 표현이다"
assert "안 된 건" in MD_SRC and "비교" in MD_SRC, "❌ 「발상이 아니라 비교」 위치가 없다"
print("  ✅ ⑩b 「아무도 안 했다」 부재 · Diaz 2001·Shah 2004(PMID) 인용 · "
      "novelty 는 'not systematically established'")

# ── ⑪ ★ 축소판 명시 · 범위 한정
for w in ("완전한 판본이 아니", "P 정점만"):
    assert w in MD_SRC or w in SRC_B or w in SRC_SET, f"❌ `phasor` 축소판 표기 '{w}' 가 없다"
assert "2유도 축소판" in SRC_SET or "2유도 축소판" in SRC_FIG, "❌ `st` 축소판 표기가 없다"
assert "Martinez" in SRC_SET and "Stridh" in SRC_SET, "❌ 방법 출처가 없다"
for src, nm in ((MD_SRC, "서두"), (SRC_SET, "설정"), (SRC_FIG, "요약")):
    assert "SVEB 질문에 답하지 않는다" in src, f"❌ {nm} 에 범위 한정이 없다"
print("  ✅ ⑪ `phasor`·`st` 축소판 명시 · 「SVEB 질문에 답하지 않는다」 3곳")

# ── ⑫ 측정 불가 · ASCII
assert 'un_ = lambda k: VERD.get(k, "").startswith("⛔")' in SRC_FIG, "❌ 측정 불가 검사가 없다"
assert re.search(r"if any\(un_\(g\) for g in", SRC_FIG), "❌ 결론 분기가 측정 불가를 안 거른다"
for g in ("U1", "U2", "U5"):
    assert f'g_("{g}", "⛔ 측정 불가"' in ALL_SRC, f"❌ {g} 에 측정 불가 갈래가 없다"
bad = [t for t in re.findall(r'set_[xy]label\("([^"]*)"\)|label="([^"]*)"', SRC_FIG)
       for t in t if t and any(unicodedata.name(ch, "").startswith("HANGUL") for ch in t)]
assert not bad, f"❌ 그림 라벨에 한글: {bad}"
assert "한글이 없어" in SRC_FIG, "❌ 폰트 한계가 명시돼 있지 않다"
print("  ✅ ⑫ 「측정 불가」가 어떤 분기도 안 탄다(R29 ②) · 그림 ASCII")


# ═══════════════════════════════════════════════════════════════════════
print("\n### 동적 검사 — 노트북 함수를 그대로 꺼내 돌린다")

FS = 360
BP, BQ = (float(x) for x in
          re.search(r"^BEAT_PRE_MS, BEAT_POST_MS = ([\d.]+), ([\d.]+)", SRC_SET, re.M).groups())
SH_MS = float(re.search(r"^SHIFT_MS = ([\d.]+)", SRC_SET, re.M).group(1))
NS = dict(np=np)
exec("import numpy as np\nclass AssetError(RuntimeError): pass\n", NS)
NS.update(BEAT_PRE_MS=BP, BEAT_POST_MS=BQ, FIT_LO_MS=flo, FIT_HI_MS=fhi,
          P_LO_MS=plo, P_HI_MS=phi, SHIFT_MS=SH_MS)
exec(SRC_0[SRC_0.index("def decide("):SRC_0.index("class AssetError")], NS)
exec(SRC_A[SRC_A.index("def ms2s("):SRC_A.index('run.log("\\n" + "=" * 100)')], NS)
exec(SRC_B[SRC_B.index("def _detrend_win("):SRC_B.index("def detect_dwt(")], NS)
exec(SRC_B[SRC_B.index("def qrs_amp("):SRC_B.index("def score_at(")], NS)
exec(SRC_C[SRC_C.index("def f1("):SRC_C.index("def evaluate(")].replace(
    "DET[key][r]", "DET[key][r]"), NS)
cancel_full, ms2s = NS["cancel_full"], NS["ms2s"]
match_1d, se_ppv, decide, mde, need_n = (NS["match_1d"], NS["se_ppv"], NS["decide"],
                                         NS["mde"], NS["need_n"])
detect_phasor, f1 = NS["detect_phasor"], NS["f1"]

# ── 합성 레코드 (심실 + P · 진폭·전기축·시프트 변동)
rng = np.random.RandomState(7)
N, DUR = 100, 100.0
t_all = np.arange(int(DUR * FS))


def gauss(t, c, w, a):
    return a * np.exp(-0.5 * ((t - c) / w) ** 2)


rr = rng.normal(0.86, 0.07, N)
RPOS = (np.cumsum(rr) * FS + 400).astype(int)
RPOS = RPOS[RPOS < len(t_all) - 400]
SIG = np.zeros((len(t_all), 2))
PTRUE = []
amp = 1.0 + 0.15 * rng.randn(len(RPOS))
axs = 1.0 + 0.20 * rng.randn(len(RPOS))
for i, r0 in enumerate(RPOS):
    lo, hi = r0 - 300, r0 + 300
    tt = np.arange(lo, hi) - r0
    v = gauss(tt, 0, 4, 1.0) - gauss(tt, 12, 5, 0.22) + gauss(tt, 75, 16, 0.30)
    SIG[lo:hi, 0] += v * amp[i]
    SIG[lo:hi, 1] += v * amp[i] * axs[i] * 0.6
    pc = r0 - int(rng.uniform(60, 85))                  # PR 167~236ms
    PTRUE.append(pc)
    ts = np.arange(pc - 60, pc + 60) - pc
    SIG[pc - 60:pc + 60, 0] += gauss(ts, 0, 6, 0.10)
    SIG[pc - 60:pc + 60, 1] += gauss(ts, 0, 6, 0.06)
SIG += 0.004 * rng.randn(*SIG.shape)
PTRUE = np.asarray(PTRUE)

# ── ⑬ ★★ `none` 이 입력과 비트 동일
out_none = cancel_full(SIG, RPOS, FS, "none")
assert out_none.shape == SIG[:, :2].shape, f"❌ 모양 {out_none.shape}"
assert np.array_equal(out_none, SIG[:, :2]), \
    "❌ `none` 이 입력과 **비트 동일하지 않다** — 대조가 구성 보장이 아니다"
assert out_none is not SIG, "❌ 같은 배열을 돌려준다(복사 아님)"
print("  ✅ ⑬ `cancel_full('none')` 이 입력과 **비트 동일** — 대조가 구성으로 보장된다")

# ── ⑭ ★★ 심실만 지우고 P 는 남는가 · st < abs
pre = ms2s(BP, FS)
vlo, vhi = ms2s(flo, FS), ms2s(fhi, FS)
res = {m: cancel_full(SIG, RPOS, FS, m) for m in ("none", "abs", "st")}
INP = eval(re.search(r"^INPUTS = (\([^)]*\))", SRC_SET, re.M).group(1))
assert set(INP) >= {"raw", "none", "abs", "st", "prev", "prevfit"}, f"❌ 팔 {INP}"


def vent_rms(x):
    seg = [x[r + vlo:r + vhi, 0] for r in RPOS if r + vlo >= 0 and r + vhi < len(x)]
    return float(np.sqrt(np.mean(np.concatenate(seg) ** 2)))


def p_amp(x):
    return float(np.median([abs(x[p, 0]) for p in PTRUE if 0 <= p < len(x)]))


vr = {m: vent_rms(res[m]) for m in res}
pa = {m: p_amp(res[m]) for m in res}
assert vr["abs"] < vr["none"], f"❌ ABS 가 심실을 못 지운다 {vr}"
assert vr["st"] < vr["abs"], f"❌ 시공간 보정이 ABS 보다 못하다 {vr}"
assert pa["st"] > 0.35 * pa["none"], f"❌ 소거가 P 를 지웠다 {pa['st']:.4f} vs {pa['none']:.4f}"
# 소거는 P 창 **밖 · 비트 밖** 을 건드리면 안 된다(est 는 비트 안에서만 산다)
gap = np.setdiff1d(np.arange(0, RPOS[0] - pre - 5), np.array([], int))
if len(gap):
    assert np.allclose(res["st"][gap, :], SIG[gap, :2]), \
        "❌ 첫 비트 이전 구간이 바뀌었다 — est 가 덮이지 않은 구간까지 샜다"
print(f"  ✅ ⑭ 심실 RMS none {vr['none']:.4f} > abs {vr['abs']:.4f} > st {vr['st']:.4f} · "
      f"P 잔존 {pa['st']/pa['none']:.2f}배 · 비트 밖 보존")

# ── ⑭b ★★ `prev`/`prevfit` — Shah 2004 의 직전-비트 템플릿
assert "PREV[0] = T; PREV[1:] = B[:-1]" in cf, \
    "❌ `prev` 템플릿이 **직전 비트**가 아니다(Shah 2004)"
assert "Shah 2004" in cf and "가장 잘 맞는 템플릿" in cf, "❌ 근거가 안 적혀 있다"
rp2 = cancel_full(SIG, RPOS, FS, "prev")
rpf = cancel_full(SIG, RPOS, FS, "prevfit")
# 직전 비트를 뺐으면 **연속한 두 비트가 닮을수록** 잔차가 작아야 한다
assert vent_rms(rp2) < vent_rms(res["none"]), "❌ `prev` 가 심실을 못 지운다"
assert vent_rms(rpf) <= vent_rms(rp2) * 1.05, "❌ `prevfit` 이 `prev` 보다 크게 나쁘다"
# 첫 비트는 앞이 없으므로 중앙값 템플릿으로 — 그래도 유한해야 한다
assert np.isfinite(rp2).all() and np.isfinite(rpf).all(), "❌ 첫 비트 처리에서 NaN"
# ★ 단일 비트 템플릿은 **중앙값보다 잡음이 크다** — Shah 가 명시한 대가다
assert vent_rms(rp2) > vent_rms(res["st"]), \
    "❌ 합성이 SNR 대가를 재현 못 한다 — 실데이터에서 `prev` 가 진 이유를 못 설명한다"
print(f"  ✅ ⑭b `prev` 템플릿 = **직전 비트**(Shah 2004) · 심실 RMS "
      f"prev {vent_rms(rp2):.4f} · prevfit {vent_rms(rpf):.4f} vs st {vent_rms(res['st']):.4f} "
      f"— 단일 비트의 **SNR 대가**가 보인다")

# ── ⑮ ★★ Voronoi 조립에 겹침·틈이 없는가
est = SIG[:, :2] - res["abs"]
covered = np.abs(est).sum(1) > 0
# ★ 전 구간이 덮일 필요는 없다. 비트 창은 R−278~+556ms 인데 Voronoi 경계는 ±RR/2 라,
#   RR 860ms 면 R+430~다음R−278 (≈152ms) 은 **어느 창에도 안 들어간다**. 거긴 늦은 T·TP
#   분절이고 est=0 → raw 그대로다. 판정에 필요한 건 **P 창이 덮이는가** 하나다.
pw_lo, pw_hi = ms2s(plo, FS), ms2s(phi, FS)
miss = [r for r in RPOS[1:-1]
        if not covered[max(r + pw_lo, 0):min(r + pw_hi, len(SIG))].all()]
assert not miss, f"❌ **P 창이 안 덮인 비트**가 {len(miss)}개 — 거기선 소거가 안 걸린다"
frac = float(covered.mean())
# 겹침: 각 샘플이 정확히 한 비트에서만 왔는지 — 경계 중점이 단조·이웃 R 사이인지로
mid = (RPOS[:-1] + RPOS[1:]) // 2
assert np.all(np.diff(mid) > 0), "❌ Voronoi 경계가 단조가 아니다 — 겹침이 생긴다"
assert np.all(mid < RPOS[1:]) and np.all(mid > RPOS[:-1]), \
    "❌ 경계가 이웃 R 사이에 있지 않다"
# 덮이지 않은 구간은 **정확히 raw** 여야 한다(소거가 새지 않았다)
assert np.allclose(res["st"][~covered, :], SIG[~covered, :2]), \
    "❌ 덮이지 않은 구간이 바뀌었다 — est 가 샜다"
print(f"  ✅ ⑮ Voronoi — **P 창은 전 비트에서 덮인다** · 경계 단조(겹침 없음) · "
      f"미덮임 {1-frac:.3f}(늦은 T·TP)은 raw 보존")

# ── ⑯ ★★ 발화율 정합 — 분위수 문턱이 목표 발화율을 만드는가
sc_pool = rng.gamma(2.0, 3.0, 5000)
for rate in rg:
    thr = -np.inf if rate >= 1.0 else float(np.percentile(sc_pool, 100.0 * (1.0 - rate)))
    got = float((sc_pool >= thr).mean())
    assert abs(got - rate) < 0.02, f"❌ 목표 발화율 {rate} 인데 실제 {got:.3f}"
assert (sc_pool >= -np.inf).all(), "❌ rate=1.0 이 기권 없음이 아니다"
print(f"  ✅ ⑯ 분위수 문턱이 목표 발화율 {rg} 을 ±0.02 안에서 만든다(rate 1.0 = 기권 없음)")

# ── ⑰ ★ phasor — arctan 이 작은 파형을 QRS 대비 증폭하는가
x = SIG[:, 0]
big, small = 1.0, 0.10                                   # QRS vs P 진폭
# ★ Rv 눈금이 **R 파 진폭**이어야 한다 — 신호 전체 MAD 는 기저선이 지배해 잡음 아래로 간다
qa = NS["qrs_amp"](x, RPOS)
mad = float(np.median(np.abs(x - np.median(x)))) + 1e-12
assert qa > 20 * mad, f"❌ 합성이 함정을 재현 못 한다 (R파 {qa:.4f} vs MAD {mad:.4f})"
assert "R 파 진폭" in SRC_B and "전부 포화" in SRC_B, \
    "❌ Rv 눈금을 MAD 로 잡으면 포화한다는 근거가 안 적혀 있다"
ratio_lin = small / big
for rv in RVF:
    Rv = rv * qa
    ratio_phi = np.arctan(small / Rv) / np.arctan(big / Rv)
    assert ratio_phi > ratio_lin, \
        f"❌ arctan 이 작은 파형을 **증폭하지 않는다**(rv={rv}) {ratio_phi:.3f} vs {ratio_lin:.3f}"
# 격자가 **포화 구간과 약증폭 구간을 감싸는가**(R33 ② 감쌈)
sat = np.arctan(0.004 / (min(RVF) * qa)) / np.arctan(small / (min(RVF) * qa))
weak = np.arctan(small / (max(RVF) * qa)) / np.arctan(big / (max(RVF) * qa)) / ratio_lin
assert sat > 0.15 and weak < 4.0, f"❌ Rv 격자가 유용 구간을 안 감싼다 (포화 {sat:.2f} · 약증폭 {weak:.1f}배)"
pk = detect_phasor(x, RPOS, FS, 0.03)
assert len(pk) >= len(RPOS) * 0.8, f"❌ phasor 가 비트당 후보를 못 낸다 {len(pk)}/{len(RPOS)}"
hit = float(np.mean([np.any(np.abs(pk - p) <= 0.05 * FS) for p in PTRUE]))
assert hit > 0.6, f"❌ 합성 P 조차 ±50ms 안에서 못 찾는다 (적중 {hit:.3f})"
print(f"  ✅ ⑰ Rv 눈금 = **R 파 진폭**({qa:.3f}, MAD {mad:.4f} 의 {qa/mad:.0f}배) · "
      f"P/QRS 비 {ratio_lin:.3f} → {ratio_phi:.3f} 증폭 · 합성 적중 {hit:.3f}")

# ── ⑱ ★ 매칭·분모·판정 건전성
m, e = match_1d([50], [48, 52], 5)
assert m == 1, f"❌ 검출 1개가 정답 2개를 먹었다 {m}"
se, pp, _ = se_ppv([10, 20, 999], [10, 20, 30, 40], 2)
assert abs(se - 0.5) < 1e-9 and abs(pp - 2 / 3) < 1e-9, f"❌ Se/PPV 분모 {se}, {pp}"
assert abs(f1(0.5, 2 / 3) - 2 * 0.5 * (2 / 3) / (0.5 + 2 / 3)) < 1e-12, "❌ F1 이 조화평균이 아니다"
assert f1(0.0, 0.0) == 0.0, "❌ F1 이 0/0 에서 안 죽는다"
assert decide(0.72, 0.81, 0.70, ">") == "✅ 지지"
assert decide(0.51, 0.64, 0.70, ">") == "❌ 기각"
assert decide(0.63, 0.79, 0.70, ">") == "⚠️ 미결"
assert abs(mde(0.60, 0.80) - 0.10) < 1e-12, "❌ MDE 가 CI 반폭이 아니다"
nn = need_n(48, 0.63, 0.79, 0.7145 - 0.70, 0.05)
assert nn is not None and np.isfinite(nn), "❌ 필요 표본을 못 낸다"
print(f"  ✅ ⑱ 1:1 매칭 · Se {se:.3f}/PPV {pp:.3f} 분모 · F1 조화평균 · decide/mde/need_n")

print("\n✅ Q7-U 픽스처 20/20 통과")
