"""퀘스트46 Q7-T(P delineation + QRST 소거) 픽스처.

Q7-D~Q7-S 는 「리듬 너머로 P 형태가 정보를 주는가」를 물었는데, **형태 측정기**가
R 기준 고정창 + 두 템플릿 거리였다 — R24 가 「심박수 대리변수」라고 못 박은 그 도구다.
Q7-T 는 질문을 바꾸지 않고 **좌표계를 바꾼다**(P delineation + QRST 소거 잔차), 그리고
이 퀘스트에서 **처음으로 외부 정답**(BUT PDB 전문가 P 주석)에 자를 맞춘다.

이 런은 SVEB 질문에 답하지 않는다 — 「P 를 볼 수 있기는 한가」만 답한다.

픽스처의 핵심은 넷이다:

    **매칭이 탐욕적 1:1 인가** — 안 걸면 검출 하나가 정답 여럿을 먹어 Se 가 부푼다
    **적합 구간이 심실에만 있는가** — P 구간이 적합에 끼면 소거가 P 를 지운다
    **전문가 주석이 평가에만 쓰이는가** — 검출기가 정답을 보면 T1 이 무의미해진다
    **부재 문턱이 BUT PDB 에서 오는가** — SVDB 라벨을 보고 고르면 순환이다

정적 검사:
  ① `run.*` API(finish dict) · fallback 부재(R16)
  ② ★★ 외부 정답 — BUT PDB 를 **실제로** 받고 실패 시 **중단**(합성 대체 없음)
  ③ ★★ 매칭이 **탐욕적 1:1** 인가 · 규칙이 코드·출력에 박혀 있는가(R34 ①)
  ④ ★★ 적합 구간이 **심실에만** — `P_HI ≤ FIT_LO` · 차감 전 구간의 대가를 명시
  ⑤ ★★ 전문가 주석이 **평가에만** — `p_detect()` 가 정답을 안 본다(R22)
  ⑥ ★ 좌표 정합 — BUT PDB 를 **360Hz 로 리샘플**하고 **주석도 같은 배율**(R27 ③)
  ⑦ ★ 부재 문턱이 **BUT PDB 에서** — SVDB 라벨을 안 본다(순환 방지 · R22) · 전이 진단
  ⑦c ★★ 소거 방식 선택도 **LORO** 인가 — 세 방식의 T1 점수 최대를 고르면 그건 평가
       지표로 고른 것이라 보고값이 낙관 편향된다(선택 편의)
  ⑦b ★★ 검출기가 **기권하는가** — 기권이 없으면 PPV 상한이 P 유병률(~0.71)로 구조적으로
       고정돼 PPV 문턱이 검출기가 아니라 **유병률**을 잰다(스모크런이 잡았다)
  ⑧ ★ 벤치마크 병기(Saclova 2022) · **종결 조건**이 코드에 있는가(R34 ⑤)
  ⑨ ★ 하드코딩 분기 문턱 부재 · 문턱 근거 명시(R34 ④)
  ⑩ ★ 관문마다 **MDE** 출력(R33 ①) · 미결이면 **필요 표본**(R30 ①)
  ⑪ ★ `st` 가 **완전한 판본이 아니다**라고 명시 · 이 런이 **SVEB 질문에 답하지 않는다**
  ⑫ 「측정 불가」가 어떤 결론 분기도 안 타는가(R29 ②) · 그림 ASCII

동적 검사 — 노트북 함수를 **그대로 꺼내** 돌린다:
  ⑬ ★★ `match_1d()` — 검출 하나가 정답 여럿을 **못 먹는가**(Se 부풀림 차단)
  ⑭ ★★ `qrst_cancel()` — 심실 잔차가 **none > abs > st** 로 줄고, **P 는 살아남는가**
  ⑮ ★★ `qrst_cancel("st")` — 진폭·전기축·시프트 변동을 `abs` 보다 잘 흡수하는가
  ⑯ ★★ `p_detect()`/`p_prom()` — 합성 P 를 ±TOL 안에서 찾는가 · P 유무가 갈리는가 ·
       ★ **절대 대비는 소거로 떨어지고 순위는 오른다**(T2 통계량 선택의 실측 근거)
  ⑰ ★ `cut_beats()` — 리샘플 후 R 위치·주석 좌표가 맞는가(R27 ③)
  ⑱ ★ `decide` · `mde` · `need_n` 건전성
"""
import os, sys, json, re
import unicodedata
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
NB = json.load(open(os.path.join(ROOT, "notebooks", "quest46_q7t_p_anchored.ipynb")))
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
SRC_LOAD = cell("【T-0a】")
SRC_A = cell("【T-A】")
SRC_B = cell("【T-B】")
SRC_C = cell("【T-C】")
SRC_D = cell("【T-D】")
SRC_FIG = cell("【T-E】")
ALL_SRC = "".join("".join(c["source"]) for c in CODE)
MD_SRC = "".join("".join(c["source"]) for c in NB["cells"] if c["cell_type"] == "markdown")

print("### 정적 검사")

# ── ①
for m in ("run.log(", "run.save_json(", "run.save_fig(", "run.finish("):
    assert m in ALL_SRC, f"❌ {m} 가 없다"
assert re.search(r"run\.finish\(\s*\{", ALL_SRC), "❌ finish 에 dict 를 안 넘긴다"
assert "fallback 없음" in SRC_LOAD, "❌ R16 표기가 없다"
print("  ✅ ① run.* API(finish dict) · fallback 부재(R16)")

# ── ② ★★ 외부 정답 — 실패 시 중단, 합성 대체 없음
assert 'wfdb.get_record_list("but-pdb")' in SRC_LOAD, "❌ BUT PDB 목록을 안 받는다"
assert "pn_dir=BUT_DIR" in SRC_LOAD, "❌ PhysioNet 에서 직접 안 읽는다"
assert re.search(r"if len\(BUT_RECS\) < 10:\s*\n\s*raise AssetError", SRC_LOAD), \
    "❌ 다운로드 실패 시 **중단**하지 않는다(R16)"
assert not re.search(r"except[^\n]*:\s*\n[^\n]*(synth|합성|randn|normal\()", SRC_LOAD), \
    "❌ 다운로드 실패를 합성으로 대체하는 경로가 있다(R16)"
# 주석 확장자 탐색은 '이름 확인'이지 대체가 아니다 — 다 못 찾으면 중단해야 한다
fe = SRC_LOAD[SRC_LOAD.index("def find_ext("):SRC_LOAD.index("EXT_Q =")]
assert "raise AssetError" in fe, "❌ 주석 확장자를 못 찾아도 안 멈춘다"
assert "합성 대체가 아니라" in fe, "❌ 확장자 탐색이 R16 예외가 아니라는 근거가 없다"
print("  ✅ ② 외부 정답 = BUT PDB 실물 · 실패 시 중단 · 합성 대체 없음(R16)")

# ── ③ ★★ 탐욕적 1:1 매칭 (R34 ①)
assert "def match_1d(" in SRC_0, "❌ match_1d() 가 없다"
m1 = SRC_0[SRC_0.index("def match_1d("):SRC_0.index("class AssetError")]
assert "used" in m1 and "(~used)" in m1, "❌ 매칭이 1:1 이 아니다 — 중복 매칭을 안 막는다"
assert "탐욕적 1:1" in m1 and "Se 가 부푼다" in m1, "❌ 1:1 근거가 안 적혀 있다"
assert "match_1d(det, ref, TOL)" in SRC_B, "❌ 관문 T1 이 match_1d() 를 안 쓴다"
assert "탐욕적 1:1" in SRC_B and "탐욕적 1:1" in SRC_SET, \
    "❌ 매칭 규칙을 **출력**하지 않는다(R34 ①)"
assert "R34 ①" in SRC_SET, "❌ 규칙 체크리스트에 R34 ① 이 없다"
print("  ✅ ③ 매칭 = **탐욕적 1:1** · 규칙을 코드·출력·체크리스트에 박았다(R34 ①)")

# ── ④ ★★ 적합 구간이 심실에만
fl, fh = (int(x) for x in re.search(r"^FIT_LO, FIT_HI = (\d+), (\d+)", SRC_SET, re.M).groups())
pl, ph = (int(x) for x in re.search(r"^P_LO, P_HI = (\d+), (\d+)", SRC_SET, re.M).groups())
assert ph <= fl, f"❌ P 탐색 [{pl},{ph}) 이 적합 [{fl},{fh}) 과 겹친다 — 소거가 P 를 지운다"
assert "assert P_HI <= FIT_LO" in SRC_SET, "❌ 겹침 금지를 코드가 강제하지 않는다"
qc = SRC_A[SRC_A.index("def qrst_cancel("):SRC_A.index("def smooth(")]
assert "fit = slice(FIT_LO, FIT_HI)" in qc, "❌ 적합이 심실 구간으로 제한되지 않는다"
assert "B[:, l, fit]" in qc, "❌ 최소제곱이 심실 구간 밖까지 본다"
assert "심실 구간에서만" in qc, "❌ 적합 제한 근거가 안 적혀 있다"
# 차감이 전 구간이라는 대가를 명시했는가
assert "중앙값 P" in SRC_A and "순차익" in SRC_A, \
    "❌ 차감 전 구간이 템플릿 P 도 지운다는 대가가 명시돼 있지 않다"
print(f"  ✅ ④ 적합 [{fl},{fh}) 심실 전용 · P 탐색 [{pl},{ph}) 비겹침 · 차감 대가 명시")

# ── ⑤ ★★ 정답은 평가에만 (R22)
pd_ = SRC_A[SRC_A.index("def p_detect("):SRC_A.index("run.log(")]
for w in ("p_true", "has_p", "ref", "정답"):
    if w == "정답":
        assert "정답 주석을 쓰지 않는다" in pd_, "❌ R22 근거가 안 적혀 있다"
    else:
        assert w not in pd_.replace("정답 주석을 쓰지 않는다", ""), \
            f"❌ p_detect() 가 정답(`{w}`)을 본다 — T1 이 무의미해진다(R22)"
det_i = SRC_A.index("DET = {c: {} for c in CANCEL}")
assert det_i < SRC_A.index("run.log(f\"  ({time.time()-T1"), "❌ 검출 순서가 이상하다"
assert "평가에만" in SRC_SET, "❌ 규칙 체크리스트에 '평가에만' 이 없다"
print("  ✅ ⑤ `p_detect()` 가 정답을 안 본다 — 주석은 **평가에만**(R22)")

# ── ⑥ ★ 좌표 정합 (R27 ③)
cb = SRC_LOAD[SRC_LOAD.index("def cut_beats("):SRC_LOAD.index("BUT = {}")]
assert "resample_poly" in cb and "gcd" in cb, "❌ 정수비 리샘플이 아니다"
assert "scale = FS / float(fs_in)" in cb, "❌ 배율을 안 낸다"
assert "np.round(np.asarray(rpos, float) * scale)" in cb, "❌ R 주석에 배율을 안 먹인다"
assert "p_res = np.round(np.asarray(ap.sample, float) * sc)" in SRC_LOAD, \
    "❌ **P 주석에 같은 배율**을 안 먹인다 — 좌표가 어긋난다(R27 ③)"
assert "nan_to_num" in cb, "❌ NaN 방어가 없다 — 리샘플이 전부 NaN 이 된다"
print("  ✅ ⑥ 360Hz 정수비 리샘플 · **R·P 주석에 같은 배율** · NaN 방어(R27 ③)")

# ── ⑦ ★ 부재 문턱이 BUT PDB 에서 (순환 방지)
thr = SRC_D[SRC_D.index("con_all, y_all = [], []"):SRC_D.index("T2_ = time.time()")]
assert "for rid, d in BUT.items()" in thr, "❌ 문턱을 BUT PDB 에서 안 정한다"
assert "Y[" not in thr and "IDX_S" not in thr, "❌ 문턱 계산이 SVDB 라벨을 본다 — 순환이다"
assert "순환 방지" in SRC_D, "❌ 순환 방지 근거가 안 적혀 있다"
assert SRC_D.index("ABS_THR =") < SRC_D.index("con[tt] < ABS_THR"), "❌ 문턱을 나중에 정한다"
assert "관문이 아니다" in SRC_D, "❌ T4 가 관문이 아니라는 표기가 없다"
assert "SV_CON" in SRC_D and "분위" in SRC_D, "❌ 두 DB 의 대비 분포를 나란히 안 찍는다"
assert "전이 OK" in SRC_D and "그대로 믿지 말 것" in SRC_D, \
    "❌ 문턱이 전이 안 됐을 때의 경고가 없다 — 부재율이 0/1 로 쏠려도 모른다"
print("  ✅ ⑦ 부재 문턱 = **BUT PDB 의 P 없는 QRS 분위수** — SVDB 라벨을 안 본다(R22)")

# ── ⑦b ★★ 기권 — PPV 가 유병률을 재지 않는가 (스모크런이 잡은 구조적 결함)
assert "def loro_thr(" in SRC_B, "❌ 기권 문턱이 없다 — PPV 상한이 P 유병률로 고정된다"
lt = SRC_B[SRC_B.index("def loro_thr("):SRC_B.index("T1TAB = {}")]
assert "if rid == rid_out:" in lt and "continue" in lt,     "❌ 기권 문턱이 **자기 레코드**를 본다 — T1 이 순환이다(R22)"
assert "roc_curve" in lt and "np.argmax(tpr - fpr)" in lt, "❌ Youden 최적점이 아니다"
assert "thr = loro_thr(c, rid)" in SRC_B, "❌ 레코드마다 LORO 문턱을 안 쓴다"
assert 'if fire[i] else []' in SRC_B, "❌ 검출기가 기권하지 않는다"
assert "n_det += len(det)" in SRC_B, "❌ PPV 분모가 **발화 수**가 아니다"
assert "유병률" in SRC_B and "발화율" in SRC_B,     "❌ 「기권이 없으면 PPV 가 유병률을 잰다」는 근거·발화율 출력이 없다"
assert "frac_with_p" in SRC_B, "❌ PPV 구조적 상한(P 유병률)을 출력하지 않는다"
print("  ✅ ⑦b 검출기가 **기권한다**(LORO Youden · 자기 레코드 제외) — "
      "PPV 가 유병률이 아니라 검출기를 잰다")

# ── ⑦c ★★ 소거 방식 선택도 LORO 인가 (선택 편의)
assert "def loro_pick(" in SRC_B, "❌ 소거 방식을 LORO 로 안 고른다 — 지표로 고르면 선택 편의다"
lp = SRC_B[SRC_B.index("def loro_pick("):SRC_B.index("T1TAB = {}")]
assert "for o in RIDS if o != rid" in lp, "❌ 방식 선택이 **평가 대상 레코드**를 본다"
assert 'PICK = {r: loro_pick(' in SRC_B, "❌ 레코드마다 LORO 선택을 안 한다"
assert 'DIFF["T1"] = dict(cancel="loro"' in SRC_B, "❌ T1 판정이 LORO 선택 팔이 아니다"
assert "선택 편의" in SRC_B, "❌ 선택 편의를 정량해 출력하지 않는다"
assert "_omax" in SRC_B, "❌ 「최대를 고르면 얼마인지」 대조를 안 낸다"
for tag, src in (("T2", SRC_C), ("T3", SRC_C)):
    assert f'DIFF["{tag}"] = dict(cancel="loro"' in src, f"❌ {tag} 도 LORO 선택이어야 한다"
assert 'if o != r] or [-np.inf]' in SRC_C, "❌ T2/T3 방식 선택이 평가 대상을 본다"
assert re.search(r"^(?!.*def ).*= max\(T1TAB, key", SRC_B, re.M) is None,     "❌ 지표 최대로 방식을 고르는 코드가 남아 있다"
print("  ✅ ⑦c 소거 방식 선택도 **LORO** — T1·T2·T3 판정 팔이 평가 대상 레코드를 안 본다")

# ── ⑧ ★ 벤치마크 · 종결 조건 (R34 ⑤)
bse = float(re.search(r"^BENCH_SE, BENCH_PP = ([\d.]+), ([\d.]+)", SRC_SET, re.M).group(1))
assert abs(bse - 0.9307) < 1e-6, f"❌ 벤치마크 Se {bse} — Saclova 2022 는 0.9307"
assert "Saclova" in SRC_SET and "Sci Rep 12:6589" in SRC_SET, "❌ 벤치마크 출처가 없다"
assert "BENCH_SE" in SRC_B and "격차" in SRC_B, "❌ T1 이 벤치마크를 나란히 안 낸다"
assert "종결 조건" in SRC_FIG and "R34 ⑤" in SRC_FIG, "❌ 종결 조건이 코드에 없다"
assert "더 돌지 않는다" in SRC_FIG, "❌ 종결 문구가 없다"
assert "자체 검출기를" in SRC_FIG and "공개 방법" in SRC_FIG, \
    "❌ 「검출기를 버린다」 갈래가 없다 — 무한 튜닝을 막는 게 종결 조건이다"
print(f"  ✅ ⑧ 벤치마크 Se {bse:.4f}(Saclova 2022) 병기 · 종결 조건 3개 코드에(R34 ⑤)")

# ── ⑨ ★ 하드코딩 문턱 부재 · 근거 (R34 ④)
bad = re.findall(r"if abs\([^)]*\) < 0\.0[0-9]+", ALL_SRC)
assert not bad, f"❌ 하드코딩 분기 문턱이 남아 있다: {bad}(R34 ④)"
assert "R34 ④" in SRC_SET and "문헌 관행" in SRC_SET, "❌ 문턱 근거가 안 적혀 있다"
tol_ms = int(re.search(r"^TOL_MS\s*=\s*(\d+)", SRC_SET, re.M).group(1))
assert tol_ms == 50, f"❌ 허용 오차 {tol_ms}ms — 문헌 관행은 ±50ms"
smin = float(re.search(r"^SE_MIN, PPV_MIN = ([\d.]+)", SRC_SET, re.M).group(1))
assert smin < bse, f"❌ 자체 문턱 {smin} 이 벤치마크 {bse} 보다 낮지 않다 — 보수적이지 않다"
print(f"  ✅ ⑨ 하드코딩 문턱 없음 · ±{tol_ms}ms(문헌) · 자체 문턱 {smin} < 벤치마크(R34 ④)")

# ── ⑩ ★ MDE · 필요 표본
assert SRC_B.count("mde(") >= 2, "❌ T1 이 MDE 를 안 낸다(R33 ①)"
assert "mde(lo_, hi_)" in SRC_C, "❌ T2 가 MDE 를 안 낸다"
assert 'mde=float(mde(d2["lo"], d2["hi"]))' in SRC_C, "❌ T2 가 MDE 를 안 남긴다"
assert 'mde=float(mde(d3["lo"], d3["hi"]))' in SRC_C, "❌ T3 가 MDE 를 안 남긴다"
assert "need_n(" in SRC_FIG and "필요 레코드" in SRC_FIG, "❌ 필요 표본을 안 낸다(R30 ①)"
print("  ✅ ⑩ 관문마다 MDE 출력(R33 ①) · 미결이면 필요 레코드 계산(R30 ①)")

# ── ⑪ ★ 축소판 명시 · SVEB 질문에 답하지 않음
assert "완전한 판본이 아니" in SRC_SET and "완전한 판본이 아니" in SRC_FIG, \
    "❌ `st` 가 Stridh–Sornmo 의 완전한 판본이 아니라는 표기가 없다"
assert "Stridh" in SRC_SET and "48:105-111" in SRC_SET, "❌ 방법 출처가 없다"
assert "SVEB 질문에 답하지 않는다" in SRC_SET, "❌ 설정에 범위 한정이 없다"
assert "SVEB 질문에 답하지 않는다" in SRC_FIG, "❌ 요약에 범위 한정이 없다"
assert "SVEB 질문에 답하지 않는다" in MD_SRC, "❌ 서두에 범위 한정이 없다"
print("  ✅ ⑪ `st` = 2유도 축소판 명시 · 「SVEB 질문에 답하지 않는다」 3곳(서두·설정·요약)")

# ── ⑫ 측정 불가 · ASCII
assert 'un_ = lambda k: VERD.get(k, "").startswith("⛔")' in SRC_FIG, "❌ 측정 불가 검사가 없다"
assert re.search(r"if any\(un_\(g\) for g in", SRC_FIG), "❌ 결론 분기가 측정 불가를 안 거른다"
assert re.search(r'elif\s+"[A-Z0-9]+"\s+in\s+VERD', ALL_SRC) is None, "❌ Q7-M 분기 버그 패턴"
for g in ("T1", "T2", "T3"):
    assert f'g_("{g}", "⛔ 측정 불가"' in ALL_SRC, f"❌ {g} 에 측정 불가 갈래가 없다"
bad = [t for t in re.findall(r'set_[xy]label\("([^"]*)"\)|label="([^"]*)"', SRC_FIG)
       for t in t if t and any(unicodedata.name(ch, "").startswith("HANGUL") for ch in t)]
assert not bad, f"❌ 그림 라벨에 한글: {bad}"
assert "한글이 없어" in SRC_FIG, "❌ 폰트 한계가 명시돼 있지 않다"
print("  ✅ ⑫ 「측정 불가」가 어떤 분기도 안 탄다(R29 ②) · 그림 ASCII")


# ═══════════════════════════════════════════════════════════════════════
print("\n### 동적 검사 — 노트북 함수를 그대로 꺼내 돌린다")

FS = int(re.search(r"^FS, RPRE, BEAT_LEN = (\d+), (\d+), (\d+)", SRC_SET, re.M).group(1))
RPRE = int(re.search(r"^FS, RPRE, BEAT_LEN = (\d+), (\d+), (\d+)", SRC_SET, re.M).group(2))
BEAT_LEN = int(re.search(r"^FS, RPRE, BEAT_LEN = (\d+), (\d+), (\d+)", SRC_SET, re.M).group(3))
SHIFTS = eval(re.search(r"^SHIFTS = (tuple\(range\([^)]*\)\))", SRC_SET, re.M).group(1))
P_SMOOTH = int(re.search(r"^P_SMOOTH\s*=\s*(\d+)", SRC_SET, re.M).group(1))
REF_LO, REF_HI = (int(x) for x in
                  re.search(r"^REF_LO, REF_HI = (\d+), (\d+)", SRC_SET, re.M).groups())
TOL = int(round(tol_ms * FS / 1000))

NS = dict(np=np)
exec("import numpy as np\nfrom scipy.signal import resample_poly\nfrom math import gcd\n"
     "class AssetError(RuntimeError): pass\n", NS)
CANCEL = eval(re.search(r"^CANCEL = (\([^)]*\))", SRC_SET, re.M).group(1))
NS.update(CANCEL=CANCEL, FS=FS, RPRE=RPRE, BEAT_LEN=BEAT_LEN, FIT_LO=fl, FIT_HI=fh,
          SHIFTS=SHIFTS, P_LO=pl, P_HI=ph, P_SMOOTH=P_SMOOTH,
          REF_LO=REF_LO, REF_HI=REF_HI)
exec(SRC_0[SRC_0.index("def decide("):SRC_0.index("class AssetError")], NS)
exec(SRC_A[SRC_A.index("def qrst_cancel("):SRC_A.index("run.log(")], NS)
exec(SRC_LOAD[SRC_LOAD.index("def cut_beats("):SRC_LOAD.index("BUT = {}")], NS)
match_1d, qrst_cancel, p_detect = NS["match_1d"], NS["qrst_cancel"], NS["p_detect"]
cut_beats, decide, mde, need_n = NS["cut_beats"], NS["decide"], NS["mde"], NS["need_n"]

# ── ⑬ ★★ match_1d 가 1:1 인가
m, e = match_1d([50], [48, 52], 5)
assert m == 1, f"❌ 검출 1개가 정답 2개를 먹었다 (매칭 {m}) — Se 가 부푼다"
m, e = match_1d([48, 52], [48, 52], 5)
assert m == 2 and np.allclose(np.sort(np.abs(e)), [0, 0]), f"❌ 정상 1:1 이 안 된다 {m}, {e}"
m, e = match_1d([50], [200], 5)
assert m == 0 and len(e) == 0, "❌ 허용 오차 밖을 매칭했다"
m, e = match_1d([10, 11], [10], 5)
assert m == 1 and abs(e[0]) == 0, f"❌ 가장 가까운 검출을 안 골랐다 {e}"
m, e = match_1d([], [10, 20], 5)
assert m == 0, "❌ 빈 검출이 매칭됐다"
# 부풀림 정량 — 1:1 없이 세면 Se 가 몇 배가 되는가
naive = sum(1 for r in [48, 50, 52] if abs(50 - r) <= 5)
m3, _ = match_1d([50], [48, 50, 52], 5)
assert naive == 3 and m3 == 1, f"❌ 부풀림 대조가 안 선다 {naive}/{m3}"
print(f"  ✅ ⑬ `match_1d()` — 탐욕적 1:1 · 순진하게 세면 Se 가 {naive}배 부푼다")

# ── ⑭ ★★ qrst_cancel — 심실은 지우고 P 는 남기는가
rng = np.random.RandomState(7)
n, L = 300, BEAT_LEN
t = np.arange(L)


def bump(c, w, a):
    return a * np.exp(-0.5 * ((t - c) / w) ** 2)


# 심실 템플릿: **앞 비트의 T 꼬리**(idx 18 — P 창 안!) + QRS(idx 100) + T(idx 175).
# ★ 앞 T 를 넣는 게 핵심이다 — P 창의 배경은 진짜로 앞 비트의 T 다(R24 가 짚은 그 교란).
#   진폭이 심실과 함께 흔들리므로 **진폭 맞춘 템플릿 차감**만이 이걸 걷어낼 수 있다.
VENT = np.stack([bump(18, 18.0, 0.34) + bump(100, 4.0, 1.00) - bump(112, 5.0, 0.22)
                 + bump(175, 16.0, 0.30),
                 bump(18, 18.0, 0.23) + bump(100, 4.0, 0.55) - bump(112, 5.0, 0.14)
                 + bump(175, 16.0, 0.20)])
P_AMP, P_CEN = 0.045, 55.0


def synth(n_, jitter=True, p_on=None, seed=0):
    """앞 T + 심실 + P + 잡음. PR 은 비트마다 흔들린다(중앙값 P 가 뭉개지도록 — 실제와 같게)."""
    r = np.random.RandomState(seed)
    p_on = np.ones(n_, bool) if p_on is None else p_on
    amp = np.ones(n_) + (0.18 * r.randn(n_) if jitter else 0.0)
    axis = np.ones(n_) + (0.25 * r.randn(n_) if jitter else 0.0)
    sh = (r.randint(-3, 4, n_) if jitter else np.zeros(n_, int))
    pc = P_CEN + r.randint(-8, 9, n_)           # PR 흔들림 ±22ms
    B = np.zeros((n_, 2, L))
    for i in range(n_):
        B[i, 0] = np.roll(VENT[0], sh[i]) * amp[i]
        B[i, 1] = np.roll(VENT[1], sh[i]) * amp[i] * axis[i]
        if p_on[i]:
            B[i, 0] += P_AMP * np.exp(-0.5 * ((t - pc[i]) / 5.0) ** 2)
            B[i, 1] += 0.6 * P_AMP * np.exp(-0.5 * ((t - pc[i]) / 5.0) ** 2)
    B += 0.004 * r.randn(n_, 2, L)
    return B, pc


B, PC = synth(n, seed=11)
rms = {}
for c in ("none", "abs", "st"):
    R_ = qrst_cancel(B, c)
    rms[c] = float(np.sqrt((R_[:, :, fl:fh] ** 2).mean()))
assert rms["abs"] < rms["none"], f"❌ ABS 가 심실을 못 지운다 {rms}"
assert rms["st"] < rms["abs"], f"❌ 시공간-lite 가 ABS 보다 못하다 {rms}"
# P 가 살아남는가 — 정답 위치의 잔차 진폭 vs 노이즈 수준
R_st = qrst_cancel(B, "st")
p_amp = np.array([abs(R_st[i, 0, int(PC[i])]) for i in range(n)])
assert np.median(p_amp) > 0.4 * P_AMP, \
    f"❌ 소거가 P 를 지웠다 — 잔여 {np.median(p_amp):.4f} vs 원 {P_AMP}"
print(f"  ✅ ⑭ 심실 RMS none {rms['none']:.4f} > abs {rms['abs']:.4f} > st {rms['st']:.4f} · "
      f"P 잔존 {np.median(p_amp)/P_AMP:.2f}배")

# ── ⑮ ★★ st 가 변동을 흡수하는가 (변동 없으면 abs 와 비슷해야 한다)
B0, _ = synth(n, jitter=False, seed=12)
r0 = {c: float(np.sqrt((qrst_cancel(B0, c)[:, :, fl:fh] ** 2).mean())) for c in ("abs", "st")}
gain_j = rms["abs"] / rms["st"]
gain_0 = r0["abs"] / r0["st"]
assert gain_j > gain_0, \
    f"❌ 변동이 있을 때 `st` 의 이득이 더 커야 한다 — 변동 {gain_j:.2f}배 vs 무변동 {gain_0:.2f}배"
assert gain_j > 1.5, f"❌ 시공간 보정 이득이 {gain_j:.2f}배뿐 — 흡수가 안 된다"
print(f"  ✅ ⑮ `st` 이득 — 변동 있음 **{gain_j:.2f}배** > 변동 없음 {gain_0:.2f}배 "
      "(진폭·전기축·시프트를 흡수한다)")

# ── ⑯ ★★ p_detect — 위치를 찾고, P 유무가 대비로 갈리는가
has_p = rng.uniform(size=n) > 0.35
Bm, PCm = synth(n, p_on=has_p, seed=13)
Rm = qrst_cancel(Bm, "st")
pk, con = p_detect(Rm)
err = np.abs(pk[has_p] - PCm[has_p])
hit = float((err <= TOL).mean())
assert hit > 0.80, f"❌ 합성 P 조차 ±{tol_ms}ms 안에서 못 찾는다 (적중 {hit:.3f})"
from sklearn.metrics import roc_auc_score
au = roc_auc_score(has_p.astype(int), con)
assert au > 0.75, f"❌ P 유무가 대비로 안 갈린다 (AUROC {au:.3f}) — T3 자체가 안 선다"
# 소거 없이 하면 더 나빠야 한다(소거가 배경을 걷어낸다는 근거)
au_none = roc_auc_score(has_p.astype(int), p_detect(qrst_cancel(Bm, "none"))[1])
assert au_none < 0.60, \
    f"❌ 소거 없이도 {au_none:.3f} 이면 앞 T 배경이 안 깔린 합성이다 — 관문이 헐거워진다"
assert au - au_none > 0.20, f"❌ 소거 이득이 얇다 {au:.3f} vs {au_none:.3f}"
# ★★ T2 가 실제로 쓰는 통계량 — **절대 대비를 쓰면 안 된다**는 걸 실측으로 못 박는다.
# 소거 전에는 앞 T 꼬리가 P 창을 덮어 |진폭|/잡음 이 **더 크게** 나온다(배경을 재는 것).
exec(SRC_C[SRC_C.index("def p_prom("):SRC_C.index('run.log("  T2')], NS)
p_prom = NS["p_prom"]
rel = [np.array([int(PCm[i])]) if has_p[i] else np.array([], int) for i in range(n)]
Rn = qrst_cancel(Bm, "none")


def abs_contrast(RES):
    E = np.abs(NS["smooth"](RES, P_SMOOTH)).sum(axis=1)
    bg = E[:, REF_LO:REF_HI]
    mad = np.median(np.abs(bg - np.median(bg, axis=1, keepdims=True)), axis=1) + 1e-9
    return float(np.mean([E[i, int(PCm[i])] / mad[i] for i in range(n) if has_p[i]]))


a0, a1 = abs_contrast(Rn), abs_contrast(Rm)
assert a1 < a0, ("❌ 합성에서 절대 대비가 소거로 **떨어지지 않는다** — 그러면 이 함정을 "
                 f"재현하지 못한 것이라 통계량 선택의 근거가 없다 {a0:.1f}→{a1:.1f}")
r0 = float(np.mean(p_prom(Rn, rel)))
r1 = float(np.mean(p_prom(Rm, rel)))
assert r1 > r0, f"❌ 순위 개선분이 음수다 — 소거가 P 를 지운 것이다 {r0:.3f}→{r1:.3f}"
assert r1 > 0.9, f"❌ 소거 후 P 가 창 안에서 두드러지지 않는다 (순위 {r1:.3f})"
print(f"  ✅ ⑯ `p_detect()` 적중 {hit:.3f}(±{tol_ms}ms) · P 부재 AUROC **{au:.3f}** vs "
      f"소거 없음 {au_none:.3f}")
print(f"       ★ T2 통계량 — 절대 대비 {a0:.1f}→{a1:.1f}(**떨어진다**: 배경을 잰다) vs "
      f"순위 {r0:.3f}→**{r1:.3f}**(오른다: P 를 잰다)")

# ── ⑰ ★ cut_beats — 리샘플 좌표 정합 (R27 ③)
FS_IN, DUR = 250, 40
x = np.zeros((FS_IN * DUR, 2))
r_in = np.arange(2 * FS_IN, FS_IN * (DUR - 2), FS_IN)      # 1Hz 심박
for p_ in r_in:
    x[p_, :] = 1.0
Bc, rp, sc = cut_beats(x, r_in, FS_IN)
assert abs(sc - FS / FS_IN) < 1e-9, f"❌ 배율 {sc}"
assert Bc.shape[1:] == (2, BEAT_LEN), f"❌ 비트 모양 {Bc.shape}"
assert len(rp) == len(r_in), f"❌ 비트를 {len(rp)}/{len(r_in)} 개만 잘랐다"
assert np.allclose(rp, np.round(r_in * sc)), "❌ R 주석에 배율이 안 먹었다"
# 스파이크가 R=index RPRE 근처(리샘플 번짐 ±2)에 오는가
peak = np.argmax(np.abs(Bc[:, 0, :]), axis=1)
assert np.all(np.abs(peak - RPRE) <= 2), f"❌ R 정렬이 어긋났다 {np.unique(peak)}"
# 잘린 비트가 신호 밖으로 안 나가는가
assert np.isfinite(Bc).all(), "❌ 비트에 NaN/inf 가 있다"
xn = x.copy(); xn[5, 0] = np.nan
Bn, _, _ = cut_beats(xn, r_in, FS_IN)
assert np.isfinite(Bn).all(), "❌ NaN 방어가 작동하지 않는다"
print(f"  ✅ ⑰ `cut_beats()` — {FS_IN}→{FS}Hz 배율 {sc:.2f} · R 정렬 idx {RPRE} · NaN 방어")

# ── ⑱ ★ decide · mde · need_n
assert decide(0.72, 0.81, 0.70, ">") == "✅ 지지"
assert decide(0.51, 0.64, 0.70, ">") == "❌ 기각"
assert decide(0.66, 0.78, 0.70, ">") == "⚠️ 미결"
assert decide(-0.02, 0.09, 0.0, ">") == "⚠️ 미결"
assert abs(mde(0.60, 0.80) - 0.10) < 1e-12, "❌ MDE 가 CI 반폭이 아니다"
assert not np.isfinite(mde(float("nan"), 0.8)), "❌ MDE 가 NaN 을 안 흘린다"
nn = need_n(50, 0.60, 0.80, 0.02, 0.05)
assert nn is not None and abs(nn - 50 * (0.10 / 0.03) ** 2) < 1e-6, f"❌ 필요 표본 {nn}"
assert need_n(50, 0.60, 0.80, 0.09, 0.05) is None, "❌ 여유 밖인데 필요 표본을 낸다"
try:
    decide(0, 1, 0.5, "!=")
    raise AssertionError("❌ 잘못된 방향을 안 막는다")
except ValueError:
    pass
print(f"  ✅ ⑱ `decide`·`mde`·`need_n` 건전성 (필요 표본 {nn:.0f})")

print("\n✅ Q7-T 픽스처 20/20 통과")
