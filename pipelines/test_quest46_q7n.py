"""퀘스트46 Q7-N(잔차화 · 정합에서 전환) 픽스처.

Q7-M 은 `f1`·`f2_16` 을 동시에 통제했지만(M1·M2 ✅) 남은 미결 셋이 전부 **정합이
표본을 버린다**에서 왔다 — ① 3축 = 6/59(Q7-K·Q7-M 둘 다) ② `k` 는 무한 계열이라
`f2_8` 이 **8.1σ** 로 생존 ③ 등가성엔 개체 **34** 가 필요한데 18.

**잔차화는 축을 몇 개든 한꺼번에 넣으면서 개체 59 · S 100% 를 쓴다.**

픽스처의 핵심은 셋이다:

    **기저에서 빼둔 프로브가 죽는가** — 기저 **안** 변수의 잔차는 정의상 0 이라
    검증이 안 된다. `f2_6·f2_12·f2_24·f1_rank` 로 검증해야 「`k` 계열을 덮었다」다
    **폭을 맞춘 음성 대조가 실제로 같은 폭인가**(R27 ③ — Q7-M 이 어긴 그 규칙)
    **`equiv()` 가 미결과 등가를 구분하는가**(R29 ① — Q7-M 이 넘어간 그 지점)

정적 검사:
  ① `run.*` API(finish dict 포함) · fallback 부재(R16)
  ② ★ **`post_rr` 이 기저에 없는가**(R28 ②) — 잔차화도 통제다
  ③ ★ **프로브가 기저 밖인가** — `PROBE_K ∩ BASIS_K = ∅`
  ④ ★ **등가 판정이 별도 함수**이고 여유가 사전등록 상수인가(R29 ①)
  ⑤ ★ **폭 정합 쌍의 폭이 실제로 같은가**(R27 ③)
  ⑥ null 의 셔플 SE 를 CI 에 전파 · 셔플 20회 이상(R26 ②)
  ⑦ ★ **사전등록 규칙 체크리스트**가 있는가(R29 ③)
  ⑧ ★ **「측정 불가」가 어떤 결론 분기도 안 타는가**(R29 ②)
  ⑨ `max` 바닥 부재(R25) · 교차적합(R22) · 1차 가족만 Bonferroni
  ⑩ 층화가 **「비트 100%」가 아님**을 명시 · 그림 라벨 ASCII

동적 검사 — 노트북 함수를 **그대로 꺼내** 합성 코호트로 실행한다:
  ⑪ ★★ 기저 **안** 변수의 잔차 AUROC 는 **정확히 0.5**(항등식 · 검증이 안 된다는 증거)
  ⑫ ★★ **프로브가 누수를 실제로 잡는다** — `k` 프로브는 ±0.02 안(기저 밀도 충분),
     `f1_rank` 는 lin 에서 **새고**(함수형 포착) rank 기저에서 0.5(기저 안)
  ⑬ ★ 결정적 짝 — 형태를 심으면 `STT` 잔차가 살고, 안 심으면 죽는다. 그리고
     `post` 기반 `f3` 는 잔차화로 죽는다
  ⑭ ★ `equiv()` 단위 검증 — 미결 / 등가 / 차이 있음을 정확히 가르는가
"""
import os, sys, json, re
import unicodedata
import numpy as np
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
NB = json.load(open(os.path.join(ROOT, "notebooks", "quest46_q7n_residualize.ipynb")))
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
SRC_A, SRC_B = cell("【N-A】"), cell("【N-B】")
SRC_C, SRC_D = cell("【N-C】"), cell("【N-D】")
SRC_E, SRC_FIG = cell("【N-E】"), cell("【N-F】")
ALL_SRC = "".join("".join(c["source"]) for c in CODE)

print("### 정적 검사")

# ── ① API
for m in ("run.log(", "run.save_json(", "run.save_fig(", "run.finish("):
    assert m in ALL_SRC, f"❌ {m} 가 없다"
assert re.search(r"run\.finish\(\s*\{", ALL_SRC), "❌ run.finish 에 result dict 를 안 넘긴다"
assert "fallback 없음" in cell("【N-0a】"), "❌ R16 표기가 없다"
print("  ✅ ① run.* API(finish dict) · fallback 부재(R16)")

# ── ② ★ post_rr 이 기저에 없다
bm = SRC_A[SRC_A.index("def basis_mat("):SRC_A.index("def residualize(")]
for bad in ("post", "f3"):
    assert bad not in bm, f"❌ 기저에 `{bad}` 가 들어갔다 — 하류 변수 통제 금지(R28 ②)"
assert "post_rr` 은 기저에 안 들어간다" in SRC_A, "❌ 하류 변수 금지 근거가 안 적혀 있다"
assert "R28 ②" in SRC_SET, "❌ 사전등록에 하류 변수 금지가 없다"
print("  ✅ ② `post_rr`(하류 변수)이 기저에 없다(R28 ②)")

# ── ③ ★ 프로브가 기저 밖
bk = eval(re.search(r"^BASIS_K\s*=\s*(\([^)]*\))", SRC_SET, re.M).group(1))
pk = eval(re.search(r"^PROBE_K\s*=\s*(\([^)]*\))", SRC_SET, re.M).group(1))
assert not (set(bk) & set(pk)), f"❌ 프로브가 기저와 겹친다 {set(bk) & set(pk)}"
assert len(pk) >= 3, "❌ 프로브가 3개 미만"
assert "f1_rank" in SRC_A, "❌ 비선형(단조 변환) 프로브가 없다"
assert "기저 **안**" in SRC_B or "기저 안" in SRC_B, "❌ 기저 안 변수는 검증이 안 된다는 설명이 없다"
assert "픽스처 실측" in SRC_SET, "❌ 기저 밀도를 실측으로 정했다는 근거가 없다"
assert '"rank"' in SRC_A and "def prep(" in SRC_A, "❌ 순위 기저(함수형 민감도)가 없다"
print(f"  ✅ ③ 기저 k={bk} · **기저 밖** 프로브 k={pk} + f1_rank")

# ── ④ ★ 등가 판정
assert "def equiv(" in SRC_0, "❌ 등가 판정 함수가 없다"
assert "CI **전체**가" in SRC_0, "❌ 등가 정의가 안 적혀 있다"
assert re.search(r"^EQUIV_MARGIN\s*=", SRC_SET, re.M), "❌ 등가 여유가 사전등록 상수가 아니다"
assert re.search(r"^PROBE_MARGIN\s*=", SRC_SET, re.M), "❌ 프로브 여유가 상수가 아니다"
assert "도달 가능" in SRC_SET, "❌ 필요 표본을 미리 계산하지 않았다(R29 ①)"
assert SRC_D.count("equiv(") >= 2, "❌ 등가 판정을 관문에 안 쓴다"
assert "equiv(lo_, hi_, PROBE_MARGIN)" in SRC_D, "❌ N2 프로브가 등가 판정이 아니다"
assert "N2a" in SRC_D and "N2b" in SRC_D, "❌ k 커버리지와 함수형을 분리하지 않았다"
assert "봉인 사유가 아니라 캐비앳" in SRC_D, "❌ N2b 실패의 처리가 안 적혀 있다"
assert "equiv(lo_, hi_, EQUIV_MARGIN)" in SRC_D, "❌ N3 이 등가 판정이 아니다"
print("  ✅ ④ 등가 판정이 별도 함수 · 여유·필요표본 사전등록(R29 ①)")

# ── ⑤ ★ 폭 정합 — 실제로 계산해서 확인한다
segs = eval(re.search(r"SEGS = (\{[^}]*\})", SRC_SET, re.S).group(1))
wp = eval(re.search(r"WIDTH_PAIRS = (\([^\n]*\))", SRC_SET).group(1))
for a, b in wp:
    wa = segs[a][1] - segs[a][0]; wb = segs[b][1] - segs[b][0]
    assert wa == wb, f"❌ 폭이 다르다 {a}({wa}) vs {b}({wb}) — R27 ③ 위반"
assert "stt_32" in segs, "❌ 폭 32 음성 대조가 신설되지 않았다"
print("  ✅ ⑤ 폭 정합 쌍 " + " · ".join(
    f"{a}/{b} (폭 {segs[a][1]-segs[a][0]})" for a, b in wp))

# ── ⑥ null SE 전파
assert "NSE" in SRC_C and "std(ddof=1)" in SRC_C, "❌ null 의 셔플 SE 를 안 낸다"
assert "rng.normal(0.0, 1.0, len(ix)) * se[ix]" in SRC_D, "❌ null 오차를 CI 에 안 흔든다"
n_shuf = int(re.search(r"^N_SHUF\s*=\s*(\d+)", SRC_SET, re.M).group(1))
assert n_shuf >= 20, f"❌ 셔플 {n_shuf}회"
assert "라벨을 안 쓰므로" in SRC_C or "라벨을 안 쓰므로" in SRC_A, "❌ 잔차화 누수 없음 근거가 없다"
print(f"  ✅ ⑥ 셔플 {n_shuf}회 · null SE 전파(R26 ②)")

# ── ⑦ ★ 규칙 체크리스트
assert "RULE_CHECK" in SRC_SET, "❌ 사전등록 규칙 체크리스트가 없다"
for r_ in ("R25", "R26", "R27 ③", "R28 ①", "R28 ②", "R29 ①", "R29 ②"):
    assert r_ in SRC_SET, f"❌ 체크리스트에 {r_} 가 없다"
print("  ✅ ⑦ 사전등록 규칙 체크리스트(R29 ③)")

# ── ⑧ ★ 측정 불가 분기 금지
assert 'un_ = lambda k: VERD.get(k, "").startswith("⛔")' in SRC_FIG, "❌ 측정 불가 검사가 없다"
assert 'if un_("N4")' in SRC_FIG, "❌ N4 결론 분기가 측정 불가를 먼저 안 거른다"
assert 'for k in ("N2a", "N2b", "N3a", "N3b", "N4")' in SRC_FIG, "❌ 요약이 관문을 다 안 낸다"
assert 'decide(d_["lo"], d_["hi"], 0.0, ">")' in SRC_FIG, \
    "❌ 등가 미결을 **우월성 미결**로 읽고 있다 — 두 검정을 따로 판정해야 한다(R31 ①)"
assert "어떤 표본으로도 등가 판정은 불가능" in SRC_FIG, "❌ 등가 프레임 오용 경고가 없다"
assert re.search(r'elif\s+"[A-Z0-9]+"\s+in\s+VERD', ALL_SRC) is None, \
    "❌ `elif \"X\" in VERD` 패턴이 남아 있다 — Q7-M 의 버그(R29 ②)"
print("  ✅ ⑧ 「측정 불가」가 어떤 결론 분기도 안 탄다(R29 ②)")

# ── ⑨ max 바닥 · 교차적합 · Bonferroni
# R25 가 금하는 건 **개체별 max 로 부풀린 바닥을 문턱 0 과 비교**하는 것이다.
# 팔별 매크로의 max 를 주장 값에서 **빼는** 것(보수적 차감)은 방향이 반대라 허용된다.
for pat in ("np.nanmax(np.stack", "np.maximum(np.stack", "nanmax(np.stack"):
    assert pat not in ALL_SRC, f"❌ max 바닥(R25): {pat}"
assert "LEAK_MAX" in SRC_D and "R25(개체별 max 바닥 금지)와 헷갈리지" in SRC_D, \
    "❌ 보수적 누출 차감이 없거나 R25 와의 구분이 안 적혀 있다"
assert "fold = rng.permutation(len(tt)) % K" in SRC_A, "❌ 교차적합(R22)이 아니다"
assert "BONF3" in SRC_SET and SRC_D.count("BONF3 * 100") >= 2, "❌ 1차 가족 보정이 없다"
assert "미보정" in SRC_D, "❌ 참고값을 미보정이라 안 적는다"
print("  ✅ ⑨ max 바닥 부재(R25) · 교차적합(R22) · 1차 가족만 Bonferroni")

# ── ⑩ 층화 주의 · ASCII
assert "비트 100%" in SRC_E and "개체 수준 문턱" in SRC_E, "❌ 층화의 한계를 잘못 적었다"
assert "층별도 **폭 정합**" in SRC_E and "WIDTH_PAIRS" in SRC_E, \
    "❌ 층별이 폭 불일치 팔을 쓴다 — 헤드라인의 층 분해가 안 된다(R27 ③)"
bad = [t for t in re.findall(r'set_[xy]label\("([^"]*)"\)|label="([^"]*)"', SRC_FIG)
       for t in t if t and any(unicodedata.name(ch, "").startswith("HANGUL") for ch in t)]
assert not bad, f"❌ 그림 라벨에 한글: {bad}"
assert "한글이 없어" in SRC_FIG, "❌ 폰트 한계가 명시돼 있지 않다"
print("  ✅ ⑩ 층화 한계 명시 · 그림 라벨 ASCII")


# ═══════════════════════════════════════════════════════════════════════
print("\n### 동적 검사 — 노트북 함수를 그대로 꺼내 돌린다")


def grab(src, first, stop="run.log("):
    i = src.index(first)
    return src[i:src.index(stop, i)]


NS = dict(np=np, stats=stats)
exec("import numpy as np\nfrom scipy import stats\n"
     "from sklearn.linear_model import LogisticRegression\n"
     "from sklearn.metrics import roc_auc_score\n"
     f"BASIS_K = {bk}\nPROBE_K = {pk}\nHIST_K = 64\nLB_K = 16\nTREND_W = 8\n"
     "K_FOLD, N_REPEAT, SEED0 = 3, 1, 20260803\n"
     "class AssetError(RuntimeError): pass\n", NS)
exec(grab(SRC_0, "def equiv(", "class AssetError"), NS)
exec(grab(SRC_A, "def local_base("), NS)
all_feats, basis_mat = NS["all_feats"], NS["basis_mat"]
residualize, build_scores, equiv = NS["residualize"], NS["build_scores"], NS["equiv"]
from sklearn.metrics import roc_auc_score


def make_record(rng, n=2500, prev=0.18, base=280.0, sd=38.0, early=0.62,
                drift=0.22, morph=0.0, noise=0.8, w=85):
    n_s = max(int(n * prev), 40)
    t = np.zeros(n, bool)
    t[rng.choice(np.arange(3, n - 3), size=n_s, replace=False)] = True
    loc = base * (1.0 + drift * np.sin(2 * np.pi * np.arange(n) / 240.0))
    pre = np.where(t, loc * early, loc) + rng.normal(0, sd, n)
    pre = np.round(np.clip(pre, 90.0, 600.0))
    post = np.r_[pre[1:], base]
    idx = np.where(t)[0]
    post[idx] = np.round(np.clip(2.0 * loc[idx] * 0.88 - pre[idx], 90.0, 900.0))
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
        F = all_feats(pre, post)
        S = build_scores(F, t, {"stt": B}, 20260803)
        assert S is not None, "합성 코호트에서 교차적합이 실패했다"
        out.append(dict(F=F, tt=t, B=B, S=S))
    return out


def resid_auc(recs, name, kind="lin"):
    v = []
    for r in recs:
        s = r["S"][name] if name in r["S"] else r["F"][name]
        e = residualize(s, basis_mat(r["F"], kind))
        if e is not None:
            v.append(roc_auc_score(r["tt"].astype(int), e))
    return float(np.mean(v))


def shuffle_null(recs, name, kind="lin", n_shuf=3):
    v = []
    for k, r in enumerate(recs):
        acc = []
        for s_ in range(n_shuf):
            rng = np.random.RandomState(4242 + 97 * s_ + k)
            ts = rng.permutation(r["tt"])
            Ss = build_scores(r["F"], ts, {"stt": r["B"]}, 20260803 + 31 * (s_ + 1))
            if Ss is None:
                continue
            e = residualize(Ss[name], basis_mat(r["F"], kind))
            if e is not None:
                acc.append(roc_auc_score(ts.astype(int), e))
        if acc:
            v.append(float(np.mean(acc)))
    return float(np.mean(v)) if v else float("nan")


SIG = cohort(11, morph=1.1)

# ── ⑪ ★★ 기저 안 변수는 정의상 0.5 — 검증이 안 된다
inside = ["f1", f"f2_{bk[0]}", f"f2_{bk[-1]}", "f6"]
for a in inside:
    v = resid_auc(SIG, a)
    assert abs(v - 0.5) < 1e-6, f"❌ 기저 안 변수 {a} 의 잔차 AUROC 가 {v:.6f}"
print(f"  ✅ ⑪ 기저 안 변수 {inside} 잔차 AUROC = 0.500000 (항등식 — 검증 불가)")

# ── ⑫ ★★ 프로브가 **누수를 실제로 잡아낸다** — k 커버리지는 통과, 함수형은 잡힌다
prep = NS["prep"]

def resid_auc2(recs, name, kind):
    v = []
    for r in recs:
        s_ = r["S"][name] if name in r["S"] else r["F"][name]
        e = residualize(prep(s_, kind), basis_mat(r["F"], kind))
        if e is not None:
            v.append(roc_auc_score(r["tt"].astype(int), e))
    return float(np.mean(v))

kprobe = [f"f2_{k}" for k in pk]
kv = {a: resid_auc2(SIG, a, "lin") for a in kprobe}
for a, v in kv.items():
    assert abs(v - 0.5) < 0.02, (f"❌ k 프로브 {a} 잔차 {v:.4f} — 기저 밀도가 부족하다. "
                                 "BASIS_K 를 촘촘히 해야 한다")
fr_lin = resid_auc2(SIG, "f1_rank", "lin")
fr_rank = resid_auc2(SIG, "f1_rank", "rank")
assert abs(fr_lin - 0.5) > 0.02, (f"❌ f1_rank 가 lin 기저에서 {fr_lin:.4f} 로 죽었다 — "
                                  "프로브가 **함수형 누수를 못 잡는다**(무의미한 프로브)")
assert abs(fr_rank - 0.5) < 1e-6, f"❌ rank 기저에서 f1_rank 가 {fr_rank:.6f} (기저 안이라 0.5여야)"
print(f"  ✅ ⑫ k 프로브 " + " · ".join(f"{a} {v:.4f}" for a, v in kv.items()) +
      f" (전부 ±0.02) | 함수형 f1_rank — lin **{fr_lin:.4f}(누수 포착)** vs rank {fr_rank:.4f}")

# ── ⑬ ★ 결정적 짝 + f3(post 기반) 사망
FLAT = cohort(12, morph=0.0)
e_sig = resid_auc(SIG, "stt") - shuffle_null(SIG, "stt")
e_flt = resid_auc(FLAT, "stt") - shuffle_null(FLAT, "stt")
assert e_sig > 0.10, f"❌ 형태를 심었는데 STT 잔차 초과가 {e_sig:+.4f}"
assert abs(e_flt) < 0.06, f"❌ 형태가 없는데 STT 잔차 초과가 {e_flt:+.4f}"
f3_raw = float(np.mean([roc_auc_score(r["tt"].astype(int), r["F"]["f3"]) for r in SIG]))
f3_res = resid_auc(SIG, "f3")
assert abs(f3_res - 0.5) < abs(f3_raw - 0.5), \
    f"❌ post 기반 f3 가 잔차화로 안 죽었다 (raw {f3_raw:.4f} → resid {f3_res:.4f})"
print(f"  ✅ ⑬ STT 잔차 초과 — 형태 심음 {e_sig:+.4f} vs 없음 {e_flt:+.4f} | "
      f"f3 {f3_raw:.4f} → {f3_res:.4f} (0.5 로 이동)")

# ── ⑭ ★ equiv() 단위 검증 — 미결을 등가로 읽지 않는가 (R29 ①)
cases = [((-0.02, +0.03), 0.05, "✅"),   # CI 전체가 여유 안 → 등가
         ((-0.09, +0.05), 0.05, "⚠️"),   # 여유를 넘음 → 미결 (Q7-M 이 등가로 읽은 형태)
         ((+0.06, +0.12), 0.05, "❌"),   # 여유 밖 한쪽 → 차이 있음
         ((-0.05, +0.05), 0.05, "⚠️")]   # 경계 포함 → 등가 아님(엄격)
for (lo, hi), mg, want in cases:
    got = equiv(lo, hi, mg)
    assert got.startswith(want), f"❌ equiv([{lo},{hi}], {mg}) = {got} · 기대 {want}"
print("  ✅ ⑭ equiv() — 등가/미결/차이있음을 정확히 가른다 (경계는 등가 아님)")

print("\n✅ Q7-N 픽스처 14/14 통과")
