"""퀘스트46 Q7-S′(P 정렬 특징) 픽스처.

**퀘스트 46 의 실제 질문에 답하는 런.** Q7-T~Q7-P0 는 전부 자를 세우는 일이었다.

픽스처가 지킬 것은 셋이다:

    **Q7-P0 의 두 제약을 지키는가** — `p_score` 를 연속으로(존재 플래그 아님) ·
    P 위치를 **7.8125ms 격자**로(SVDB 원본 128Hz · 그보다 미세하면 보간 인공물)
    **주 관문 S3 이 조기성을 진짜로 통제하는가** — `f1` **정확 매칭 쌍** 안에서 재는가
    **영점이 구성으로 보장되는가** — 전 팔 같은 차원 · `noise5`/`shuf5`

정적 검사:
  ① `run.*` API(finish dict) · fallback 부재(R16)
  ② ★★ 소비 측 **정합 재확인** — `pid`·`sym` 이 어긋나면 **중단**(R35 ⑦)
  ③ ★★★ **Q7-P0 제약 ①** — `p_score` 를 연속으로 쓰는가 · 존재 플래그만 쓰지 않는가
  ④ ★★★ **Q7-P0 제약 ②** — 위치를 `1000/128` ms 격자로 양자화하는가(유도값 · R34 ④)
  ⑤ ★★★ **S3 이 정확 매칭 쌍인가** — 층화가 아니라 매칭인 근거 · `f1` 상수 안에서
  ⑥ ★★ **차원 정합** — 전 팔이 `N_DIM` 로 같은가(차원 추가 비용 상쇄)
  ⑦ ★★ 누수 없음(R22) — PCA·표준화·개인 기준이 **학습/그 레코드 N 비트**에서만
  ⑧ ★ 리듬 기저가 **강한가** · `RHY_K ⊆ FULL_K` 를 강제하는가
  ⑨ ★ 영점 팔(`noise5`·`shuf5`)이 구성 보장인가 · `shuf5` 가 **레코드 안** 치환인가
  ⑩ ★ 선택이 전부 LORO 인가(개인화 k · S3 프로브) — 성적표 최대 금지
  ⑪ ★ 종결 조건(R34 ⑤) · **딥러닝은 S3 ✅ 일 때만** 이 코드에 있는가
  ⑫ 「측정 불가」·영점 붕괴가 결론 분기를 안 타는가(R29 ②) · 그림 ASCII

동적 검사 — 노트북 함수를 **그대로 꺼내** 돌린다:
  ⑬ ★★★ `matched_auc()` — 심은 신호를 잡고 · null 이 0.5 이며 · 조기성만으로는 안 속는가
  ⑭ ★★ 양자화 — `1000/128` 격자로 떨어지는가 · 그보다 미세한 차이가 지워지는가
  ⑮ ★ `decide`·`mde`·`need_n`·`boot_mean` 건전성
"""
import os, sys, json, re
import unicodedata
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
NB = json.load(open(os.path.join(ROOT, "notebooks", "quest46_q7s2_p_aligned.ipynb")))
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
SRC_A, SRC_B = cell("【S2-0a】"), cell("【S2-A】")
SRC_C, SRC_D = cell("【S2-B】"), cell("【S2-C】")
SRC_E, SRC_FIG = cell("【S2-D】"), cell("【S2-E】")
ALL_SRC = "".join("".join(c["source"]) for c in CODE)
MD_SRC = "".join("".join(c["source"]) for c in NB["cells"] if c["cell_type"] == "markdown")

print("### 정적 검사")

# ── ①
for m in ("run.log(", "run.save_json(", "run.save_fig(", "run.finish("):
    assert m in ALL_SRC, f"❌ {m} 가 없다"
assert re.search(r"run\.finish\(\s*\{", ALL_SRC), "❌ finish 에 dict 를 안 넘긴다"
assert re.search(r"if not os\.path\.exists\(p_\):\s*\n\s*raise AssetError", SRC_A), \
    "❌ 자산이 없어도 안 멈춘다(R16)"
assert "Q7-P0 를 먼저 돌린다" in SRC_A, "❌ 선행 런 안내가 없다"
assert not re.search(r"except[^\n]*:\s*\n[^\n]*(synth|합성|randn)", ALL_SRC), \
    "❌ 실패를 합성으로 대체하는 경로가 있다(R16)"
print("  ✅ ① run.* API(finish dict) · fallback 부재(R16)")

# ── ② ★★ 소비 측 정합 재확인 (R35 ⑦)
assert "정합 재확인" in SRC_A, "❌ 정합 재확인이 없다"
assert re.search(r"if len\(PD\[.p_idx.\]\) != len\(PID\):\s*\n\s*raise AssetError", SRC_A), \
    "❌ 길이가 달라도 안 멈춘다"
assert re.search(r"if _bp or _bs:", SRC_A), "❌ pid·sym 불일치를 안 잡는다"
assert "raise AssetError(f\"정합 깨짐" in SRC_A, "❌ 정합이 깨져도 안 멈춘다"
assert "첫 어긋남 idx" in SRC_A, "❌ 어디서 어긋났는지 안 알려준다"
print("  ✅ ② 소비 측 정합 재확인 — pid·sym 어긋나면 첫 위치를 찍고 **중단**(R35 ⑦)")

# ── ③ ★★★ Q7-P0 제약 ① — p_score 를 연속으로
assert "psc," in SRC_B and "PAL = np.c_[psc," in SRC_B, \
    "❌ `p_score` 가 특징 첫 열에 없다 — 연속값으로 안 쓴다"
for w in ("후보를 놓았다", "0.7145"):
    assert w in ALL_SRC or w in MD_SRC, f"❌ 제약 ①('{w}')의 근거가 없다"
assert "p_miss" in SRC_B, "❌ 결측을 표현하는 열이 없다 — 버리면 정보가 준다"
assert "버리지 않고" in SRC_B, "❌ 결측 처리 근거가 없다"
print("  ✅ ③ `p_score` **연속** · 결측은 `p_miss` 로 표현(Q7-P0 제약 ①)")

# ── ④ ★★★ Q7-P0 제약 ② — 7.8125ms 양자화 (유도값)
q = re.search(r"^QUANT_MS = ([\d./ ]+)", SRC_SET, re.M).group(1).strip()
assert q == "1000.0 / 128.0", f"❌ 양자화가 유도식이 아니다 — `{q}`(1000/128 이어야 · R34 ④)"
assert "pr_q8 = np.round(pr_ms / QUANT_MS) * QUANT_MS" in SRC_B, "❌ 위치를 양자화 안 한다"
assert "128Hz" in SRC_SET or "128Hz" in MD_SRC, "❌ 128Hz 근거가 없다"
assert "보간 인공물" in MD_SRC, "❌ 왜 양자화하는지 근거가 없다"
print(f"  ✅ ④ 위치 양자화 `{q}` = 7.8125ms — **유도값**(SVDB 원본 128Hz · R34 ④)")

# ── ⑤ ★★★ S3 이 정확 매칭 쌍인가
assert "def matched_auc(" in SRC_D, "❌ 매칭 AUROC 가 없다"
ma = SRC_D[SRC_D.index("def matched_auc("):SRC_D.index("# 층화 AUROC 를 **레코드별**")] \
    if "# 층화 AUROC 를 **레코드별**" in SRC_D else \
    SRC_D[SRC_D.index("def matched_auc("):SRC_D.index("PROBES = {")]
assert "key = np.round(f1[idx]).astype(int)" in ma, "❌ `f1` 정확 매칭이 아니다"
assert "a[:, None] - b[None, :]" in ma, "❌ S×N 쌍을 안 만든다(Mann-Whitney 가 아니다)"
assert "0.5 * tie" in ma, "❌ 동점 처리가 없다 — AUROC 가 아니다"
assert "층화는 거의 안 선다" in ma or "안 선다" in ma, \
    "❌ 층화 대신 매칭을 쓰는 근거가 없다"
assert "def strat_auc(" not in ALL_SRC, "❌ 옛 층화 함수가 남아 있다"
assert "resid(v, idx)" in SRC_D and "basis_ext" in SRC_D, "❌ f2_k 전 계열 잔차화가 없다"
assert "vsub[m[tt[m]]]" in ma and "vsub[m[~tt[m]]]" in ma, \
    "❌ 이미 잘린 배열을 전역 인덱스로 다시 인덱싱한다(스모크런이 IndexError 로 잡은 버그)"
assert "vsub[idx]" not in ma and "v[idx][" not in ma, "❌ 이중 인덱싱이 남아 있다"
print("  ✅ ⑤ S3 = **`f1` 정확 매칭 쌍** Mann-Whitney · f2_k 전 계열 잔차화 · 동점 0.5")

# ── ⑥ ★★ 차원 정합
nd = int(re.search(r"^N_DIM = (\d+)", SRC_SET, re.M).group(1))
assert re.search(r"if PAL\.shape\[1\] != N_DIM:\s*\n\s*raise AssetError", SRC_B), \
    "❌ P 정렬 특징 차원을 강제하지 않는다 — 영점과 차원이 어긋나면 비교가 불공정하다"
assert f"NOISE = _rng.normal(size=(len(K), N_DIM))" in SRC_B, "❌ 영점이 같은 차원이 아니다"
assert "n_components=N_DIM" in SRC_C, "❌ 옛 창 PCA 가 같은 차원이 아니다"
assert "차원 추가 비용" in SRC_SET or "차원 비용" in SRC_SET, "❌ 차원 정합의 근거가 없다"
print(f"  ✅ ⑥ 전 팔 **{nd}차원** 정합 — 차원 추가 비용을 상쇄(강제 assert 포함)")

# ── ⑦ ★★ 누수 없음 (R22)
fe = SRC_C[SRC_C.index("def feats_for("):SRC_C.index("D_LORO = {")]
assert "PCA(n_components=N_DIM, random_state=SEED0).fit(PM_RAW[tr])" in fe, \
    "❌ PCA 를 **학습 비트에서만** 적합하지 않는다"
assert "mu, sd = Xtr.mean(0)" in SRC_C, "❌ 표준화를 학습에서만 적합하지 않는다"
assert "ev = np.setdiff1d(te0, used)" in SRC_C, \
    "❌ 개인화에 쓴 비트를 평가에서 안 뺀다 — S1/S2 비교가 불공정해진다"
assert "양쪽 다" in SRC_C or "양쪽 팔" in SRC_SET, "❌ 공정 비교 근거가 없다"
# 개인 기준을 그 레코드의 **N 비트**에서만 — S 로 기준을 잡으면 라벨이 샌다
assert "mn = m & nmask" in SRC_B, "❌ 개인 기준을 N 비트로 한정하지 않는다"
assert "S 비트로" in SRC_B and "라벨이 샌다" in SRC_B, "❌ 그 근거가 없다"
print("  ✅ ⑦ PCA·표준화는 학습에서만 · 개인 기준은 **그 레코드 N 비트**에서만(R22)")

# ── ⑧ ★ 리듬 기저 · RHY_K ⊆ FULL_K
fk = eval(re.search(r"^FULL_K = (tuple\(range\([^)]*\)\))", SRC_SET, re.M).group(1))
rk = eval(re.search(r"^RHY_K  = (\([^)]*\))", SRC_SET, re.M).group(1))
assert set(rk) <= set(fk), f"❌ RHY_K {rk} ⊄ FULL_K"
assert "assert set(RHY_K) <= set(FULL_K)" in SRC_SET, \
    "❌ 부분집합을 **코드가 강제**하지 않는다(스모크런이 KeyError 로 잡았다)"
assert len(fk) >= 25 and min(fk) <= 4 and max(fk) >= 32, f"❌ f2 계열이 얇다 {fk}"
assert "RHY = np.c_[f1," in SRC_B and "np.log1p(pre)" in SRC_B, "❌ 리듬 기저가 얇다"
assert "바를 높인다" in SRC_SET or "바를 높인다" in SRC_B, "❌ 강한 기저의 근거가 없다"
print(f"  ✅ ⑧ 리듬 기저 강함(f2_{min(fk)}..{max(fk)} · f1·f3·f4·log RR) · RHY_K ⊆ FULL_K 강제")

# ── ⑨ ★ 영점이 구성 보장
assert '"noise5"' in SRC_SET and '"shuf5"' in SRC_SET, "❌ 영점 팔이 없다"
assert "rr.permutation(len(sel))" in fe and "RID[m_] == u" in fe, \
    "❌ `shuf5` 가 **레코드 안에서** 치환되지 않는다 — 주변분포가 안 보존된다"
assert "레코드 안에서" in fe, "❌ 근거가 없다"
assert "S4ok" in SRC_E and "영점이 깨" in SRC_E, "❌ 영점 붕괴를 판정하지 않는다"
print("  ✅ ⑨ 영점 `noise5`(순수 잡음)·`shuf5`(레코드 안 치환) — 구성 보장(R34 ③)")

# ── ⑩ ★ 선택이 전부 LORO
assert "np.nanmean(np.delete(D_PERS[k][GATE_ARM], i))" in SRC_C, \
    "❌ 개인화 k 선택이 LORO 가 아니다 — 성적표 최대를 고르면 선택 편의(R34 ②)"
assert "성적표에서 최대를 고르면 선택 편의" in SRC_C, "❌ 근거가 없다"
print("  ✅ ⑩ 개인화 k 를 **LORO 로** 선택 — 성적표 최대 금지(R34 ②)")

# ── ⑪ ★ 종결 조건 · 딥러닝 진입 조건
assert "종결 조건" in SRC_FIG and "R34 ⑤" in SRC_FIG, "❌ 종결 조건이 코드에 없다"
assert "더 돌지 않는다" in SRC_FIG, "❌ 종결 문구가 없다"
assert "딥러닝은 **S3 이 ✅ 일 때만**" in SRC_FIG, \
    "❌ **딥러닝 진입 조건**이 코드에 없다 — 값싼 모형으로 먼저 가르는 이유가 사라진다"
assert "null 을 숨긴다" in SRC_FIG or "숨긴다" in SRC_FIG, "❌ 그 이유가 없다"
assert "딥러닝이 아니다" in SRC_FIG, "❌ 이 런이 딥러닝이 아니라는 표기가 없다"
print("  ✅ ⑪ 종결 조건 3개 · **딥러닝은 S3 ✅ 일 때만** 이 코드에 박혀 있다(R34 ⑤)")

# ── ⑫ 측정 불가 · 영점 붕괴 · ASCII
assert 'un_ = lambda k: VERD.get(k, "").startswith("⛔")' in SRC_FIG, "❌ 측정 불가 검사가 없다"
assert re.search(r'if not ok_\("S4"\):', SRC_FIG), \
    "❌ **영점이 깨졌을 때** 결론 분기를 안 막는다 — 가장 먼저 걸러야 한다"
assert SRC_FIG.index('if not ok_("S4")') < SRC_FIG.index("elif any(un_(g)"), \
    "❌ 영점 검사가 측정 불가 검사보다 뒤에 온다"
for g in ("S1", "S2", "S3"):
    assert f'"{g}"' in SRC_FIG, f"❌ {g} 가 요약에 없다"
bad = [t for t in re.findall(r'set_[xy]label\("([^"]*)"\)|label="([^"]*)"', SRC_FIG)
       for t in t if t and any(unicodedata.name(ch, "").startswith("HANGUL") for ch in t)]
assert not bad, f"❌ 그림 라벨에 한글: {bad}"
assert "한글이 없어" in SRC_FIG, "❌ 폰트 한계가 명시돼 있지 않다"
print("  ✅ ⑫ **영점 붕괴를 가장 먼저** 거른다 · 측정 불가 분기 없음(R29 ②) · 그림 ASCII")


# ═══════════════════════════════════════════════════════════════════════
print("\n### 동적 검사 — 노트북 함수를 그대로 꺼내 돌린다")

NS = dict(np=np)
exec("import numpy as np\nclass AssetError(RuntimeError): pass\n", NS)
exec(SRC_0[SRC_0.index("def decide("):SRC_0.index("class AssetError")], NS)
decide, mde, need_n, boot_mean = (NS["decide"], NS["mde"], NS["need_n"], NS["boot_mean"])

# ── ⑬ ★★★ matched_auc — 심은 신호를 잡고, 조기성만으로는 안 속는가
rng = np.random.RandomState(3)
NR, NB = 6, 900
RID = np.repeat(np.arange(NR), NB)
n = len(RID)
TT = np.zeros(n, bool)
for u in range(NR):
    m = np.where(RID == u)[0]
    TT[rng.choice(m, int(NB * 0.15), replace=False)] = True
pre = np.where(TT, rng.normal(230, 30, n), rng.normal(330, 35, n))
f1 = np.zeros(n)
for u in range(NR):
    m = RID == u
    f1[m] = np.median(pre[m]) - pre[m]
NS.update(TT=TT, RID=RID, f1=f1, MIN_PAIR=50)
exec(SRC_D[SRC_D.index("def matched_auc("):SRC_D.index("PROBES = {")], NS)
matched_auc = NS["matched_auc"]

idx = np.arange(n)
# (a) 조기성 **그 자체** — 매칭 안에서는 상수여야 하므로 0.5 근처
a_f1, np_f1 = matched_auc(f1[idx], idx)
assert abs(a_f1 - 0.5) < 0.02, \
    f"❌ `f1` 자신이 매칭 안에서 {a_f1:.4f} — 매칭이 조기성을 상수로 안 만든다"
# (b) 조기성의 **단조 함수**(pre) — 역시 속으면 안 된다
a_pre, _ = matched_auc(-pre[idx], idx)
assert abs(a_pre - 0.5) < 0.10, f"❌ 조기성 대리변수에 속는다 {a_pre:.4f}"
# (c) 심은 **진짜** 신호 — S 에서만 값이 높다
sig = rng.normal(0, 1, n) + 0.8 * TT
a_sig, np_sig = matched_auc(sig[idx], idx)
assert a_sig > 0.65, f"❌ 심은 신호를 못 잡는다 {a_sig:.4f}"
# (d) null — 레코드 안 셔플이면 0.5
a_nul = np.mean([matched_auc(sig[idx], idx, 100 + s)[0] for s in range(5)])
assert abs(a_nul - 0.5) < 0.05, f"❌ 라벨셔플 null 이 0.5 가 아니다 {a_nul:.4f}"
# (e) 쌍이 부족하면 nan
a_few, _ = matched_auc(sig[:60], np.arange(60))
assert np.isnan(a_few), "❌ 쌍이 부족해도 값을 낸다(R17)"
print(f"  ✅ ⑬ `matched_auc()` — f1 자신 {a_f1:.4f}·조기성대리 {a_pre:.4f}(속지 않음) · "
      f"심은 신호 **{a_sig:.4f}** · null {a_nul:.4f} · 쌍 부족 시 nan")

# ── ⑭ ★★ 양자화
Q = 1000.0 / 128.0
assert abs(Q - 7.8125) < 1e-9, f"❌ 격자 {Q}"
rv = np.random.RandomState(9).uniform(100, 260, 5000)
qv = np.round(rv / Q) * Q
# ① 결과가 **격자 위**에 있다  ② 이동량이 반칸을 안 넘는다(정보 손실 상한)
assert np.allclose(qv / Q, np.round(qv / Q)), "❌ 격자에 안 떨어진다"
assert np.max(np.abs(qv - rv)) <= Q / 2 + 1e-9, "❌ 반칸보다 크게 움직인다"
# ③ 같은 칸 안 차이는 **지워지고**, 한 칸 이상 차이는 **보존**된다
c = 20 * Q                                       # 격자 중심
assert np.round((c - 1) / Q) * Q == np.round((c + 1) / Q) * Q, "❌ 칸 안 차이가 안 지워진다"
assert np.round((c - Q) / Q) * Q != np.round((c + Q) / Q) * Q, "❌ 칸 밖 차이까지 지운다"
# ④ 서로 다른 값의 개수가 실제로 준다(= 해상도가 낮아진다)
assert len(np.unique(qv)) < len(np.unique(np.round(rv, 6))) / 5,     f"❌ 해상도가 안 낮아졌다 — 고유값 {len(np.unique(qv))}"
print(f"  ✅ ⑭ 양자화 {Q:.4f}ms — 격자 위 · 이동 ≤ 반칸 · 칸 안 차이 소거 · "
      f"고유값 {len(np.unique(rv)):,} → {len(np.unique(qv))}")

# ── ⑮ ★ 판정 유틸
assert decide(0.52, 0.60, 0.5, ">") == "✅ 지지"
assert decide(0.40, 0.49, 0.5, ">") == "❌ 기각"
assert decide(0.48, 0.56, 0.5, ">") == "⚠️ 미결"
assert abs(mde(0.45, 0.55) - 0.05) < 1e-12, "❌ MDE 가 CI 반폭이 아니다"
m_, lo_, hi_, n_ = boot_mean([0.5, 0.6, 0.7, 0.55, 0.65], 1)
assert n_ == 5 and lo_ < m_ < hi_, f"❌ boot_mean {m_},{lo_},{hi_}"
assert boot_mean([1.0, 2.0], 1)[3] == 2 and np.isnan(boot_mean([1.0, 2.0], 1)[0]), \
    "❌ 표본 3 미만인데 값을 낸다"
nn = need_n(78, 0.48, 0.56, 0.02, 0.01)
assert nn is None or np.isfinite(nn), "❌ 필요 표본 계산이 이상하다"
print(f"  ✅ ⑮ `decide`·`mde`·`need_n`·`boot_mean` 건전성 (표본 3 미만은 nan)")

print("\n✅ Q7-S′ 픽스처 15/15 통과")
