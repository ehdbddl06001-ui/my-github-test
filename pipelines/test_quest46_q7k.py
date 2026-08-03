"""퀘스트46 Q7-K(합동 정합 · 상대 조기성까지 통제) 픽스처.

Q7-I‴ K3 이 문을 열었다 — `pre_rr` 을 **값 단위로** 맞춰도 `f2`(국소 기저선 대비
조기성)가 **0.6688** 로 살아남는다(+0.1688 [+0.0760, +0.2535]). 같은 절대 RR 이라도
**S 는 국소 기저선이 긴 자리에서** 나오기 때문이다. 그러니 이 퀘스트가 지금껏
「정합 후」라고 부른 값(Q7-F 0.6890 · Q7-I 0.5745)은 **조기성을 다 뺀 값이 아니다.**

그래서 이 실험은 **`pre_rr` 값 × 국소 기저선 대역**으로 **합동 정합**해 `f1` 과 `f2` 를
**둘 다** 무너뜨리고, 그 조건에서 형태(`STT`·P 창)와 `post_rr`(`f3`)가 남는지 묻는다.

픽스처의 핵심은 셋이다:

    **합동 정합이 `f1` 과 `f2` 를 둘 다 죽이는가**(하나만 죽으면 이 실험은 무의미하다)
    **그 조건에서 진짜 형태 신호는 살고, 없는 코호트에서는 안 사는가**
    **null 의 셔플 오차를 CI 에 전파하는가**(5회 셔플로 ±0.02 를 판정하면 안 된다)

정적 검사:
  ① `run.*` API 정합 + fallback 부재(R16)
  ② ★ 정합 키가 **두 축**(`pre_rr` 값 × 국소 기저선 대역)인가
  ③ ★ **L2(`f2` 붕괴)가 전제**이고, 미지지면 L3~L6 인용을 봉인하는가(R24-b)
  ④ ★ **null 의 셔플 간 SE 를 CI 에 전파**하는가 · 셔플 횟수가 20 이상인가(R26 ②)
  ⑤ ★ **선택 편향**(누가 정합 가능한가)을 층 구성·RR 분리도로 보고하는가
  ⑥ **P 창 3종을 정확 정합 조건에서 다시 재는가** — Q7-F 의 0.6890 은 무효다
  ⑦ 짝 단위 잔여를 **`f1`·`f2` 둘 다** 내는가
  ⑧ **억제 변수 경고** — 폴드 간 계수 부호 안정성을 내는가
  ⑨ 1차 가족만 Bonferroni 이고 **민감도 관문은 미보정이라고 적는가** · 교차적합(R22)
  ⑩ `max` 바닥 부재(R25) · 그림 라벨 ASCII

동적 검사 — 노트북 함수를 **그대로 꺼내** 합성 코호트로 실행한다:
  ⑪ ★★ **합동 정합은 `f1`·`f2` 를 둘 다 무너뜨린다**(정확 `pre` 만 맞추면 `f2` 는 산다)
  ⑫ ★★ 결정적 짝 — **형태 신호를 심은 코호트**에서 `STT` 가 살고,
     **안 심은 코호트**에서는 안 산다
  ⑬ 셔플 null 이 교차적합 바닥을 잡는가 (라벨 무작위 코호트에서 초과분 ≈ 0)
  ⑭ ★ `boot_excess` 가 **null 오차를 전파**하는가 — SE 를 키우면 CI 가 넓어져야 한다
"""
import os, sys, json, re
import unicodedata
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
NB = json.load(open(os.path.join(ROOT, "notebooks", "quest46_q7k_relative_match.ipynb")))
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
SRC_A, SRC_B = cell("【L-A】"), cell("【L-B】")
SRC_C, SRC_D = cell("【L-C】"), cell("【L-D】")
SRC_E, SRC_FIG = cell("【L-E】"), cell("【L-F】")
ALL_SRC = "".join("".join(c["source"]) for c in CODE)

print("### 정적 검사")

# ── ① API · fallback
for m in ("run.log(", "run.save_json(", "run.save_fig(", "run.finish("):
    assert m in ALL_SRC, f"❌ {m} 가 없다"
assert re.search(r"run\.finish\(\s*\{", ALL_SRC), "❌ run.finish 에 result dict 를 안 넘긴다"
assert "MedKOSRun(" in SRC_SET, "❌ MedKOSRun 을 안 쓴다"
assert "fallback 없음" in cell("【L-0a】"), "❌ R16 표기가 없다"
assert "except Exception" not in SRC_B, "❌ 정합 셀에 예외 삼킴"
print("  ✅ ① run.* API 정합(finish 인자 포함) · fallback 부재(R16)")

# ── ② ★ 두 축 정합
assert "def joint_key(" in SRC_B, "❌ joint_key 가 없다"
assert "np.unique(np.round(pre_v, 6), return_inverse=True)" in SRC_B, "❌ 정확 pre 참조점이 없다"
assert "np.floor(pre_v /" in SRC_B and "np.floor(lb_v /" in SRC_B, "❌ 두 축 대역이 아니다"
assert "칸이 잘게 쪼개져" in SRC_B, "❌ 두 축 모두 대역으로 간 이유가 안 적혀 있다"
assert "LB_K" in SRC_SET and 'f"f2_{LB_K}"' in SRC_B, "❌ 정합 축과 f2 의 k 가 안 묶였다"
print("  ✅ ② 정합 키가 **pre_rr 값 × 국소 기저선 대역** 두 축이다")

# ── ③ ★ L2 전제 · 봉인
assert "F2_COLLAPSE" in SRC_SET and "F2_COLLAPSE" in SRC_D, "❌ f2 붕괴 문턱이 상수가 아니다"
assert "F1_COLLAPSE" in SRC_SET and "F1_COLLAPSE" in SRC_D, "❌ f1 붕괴 문턱이 상수가 아니다"
assert re.search(r'decide\(lo2, hi2, F2_COLLAPSE, "<"\)', SRC_D), "❌ L2 가 상한 검정이 아니다"
assert "SEALED" in SRC_D and "인용하지 않는다" in SRC_D, "❌ 봉인 규약이 없다"
assert "SEALED" in SRC_FIG, "❌ 요약이 봉인 상태를 안 본다"
print("  ✅ ③ L2(f2 붕괴)가 전제이고 미지지면 아래를 봉인한다")

# ── ④ ★ null 오차 전파
assert "NSE" in SRC_C and "std(ddof=1)" in SRC_C, "❌ null 의 셔플 간 SE 를 안 낸다"
assert "def boot_excess(" in SRC_D, "❌ boot_excess 가 없다"
assert "rng.normal(0.0, 1.0, len(idx)) * se[idx]" in SRC_D, "❌ null 오차를 CI 에 안 흔든다"
n_shuf = int(re.search(r"^N_SHUF\s*=\s*(\d+)", SRC_SET, re.M).group(1))
assert n_shuf >= 20, f"❌ 셔플 {n_shuf}회 — 작은 초과분을 판정하려면 20 이상"
print(f"  ✅ ④ 셔플 {n_shuf}회 · null 의 SE 를 CI 에 전파한다(R26 ②)")

# ── ⑤ ★ 선택 편향
assert "선택 편향" in SRC_E, "❌ 선택 편향 진단이 없다"
assert "RRSEP" in SRC_E and "rr_sep_matched" in SRC_E, "❌ RR 분리도를 정합/제외로 안 비교한다"
assert "한 개도 안 남았다" in SRC_E, "❌ 층이 통째로 빠진 경우를 표시하지 않는다"
assert "적용 범위" in SRC_E and "적용 범위" in SRC_SET, "❌ 적용 범위 한정 규약이 없다"
print("  ✅ ⑤ 정합 코호트의 **선택 편향**을 층 구성·RR 분리도로 보고한다")

# ── ⑥ P 창 재측정
for w in ("p_full", "p_early", "p_late"):
    assert f'"{w}"' in SRC_SET, f"❌ {w} 창이 사전등록에 없다"
assert "0.6890" in SRC_SET and "무효" in SRC_SET, "❌ Q7-F 상한이 무효라는 근거가 없다"
assert 'JM["p_late"]' in SRC_D, "❌ L7 이 P_late 를 안 잰다"
print("  ✅ ⑥ P 창 3종을 오염되지 않은 조건에서 다시 잰다")

# ── ⑦ 짝 단위 잔여 f1·f2 둘 다
assert "np.abs(a_[:, None] - b_[None, :])" in SRC_B, "❌ f1 짝 잔여가 없다"
assert "np.abs(a2[:, None] - b2[None, :])" in SRC_B, "❌ **f2** 짝 잔여가 없다"
assert "짝잔여 f1" in SRC_B and "f2 {" in SRC_B, "❌ 곡선이 두 잔여를 같이 안 낸다"
print("  ✅ ⑦ 짝 단위 잔여를 f1·f2 **둘 다** 낸다")

# ── ⑧ 억제 변수 경고
assert "부호 일치율" in SRC_E and "억제 변수" in SRC_E, "❌ 계수 부호 안정성 진단이 없다"
assert "lr.coef_[0]" in SRC_E, "❌ 계수를 실제로 안 본다"
print("  ✅ ⑧ 폴드 간 계수 부호 안정성(억제 변수 경고)을 낸다")

# ── ⑨ 다중검정 · 교차적합
assert "BONF3" in SRC_SET and SRC_D.count("BONF3 * 100") >= 3, "❌ 1차 가족에 보정을 안 쓴다"
assert "민감도·미보정" in SRC_D, "❌ 민감도 관문을 미보정이라고 안 적는다"
assert "fold = rng.permutation(len(tt)) % K" in SRC_A, "❌ 교차적합(R22)이 아니다"
assert "sc[te] = lr.decision_function" in SRC_A, "❌ 겹 밖 점수가 아니다"
print("  ✅ ⑨ 1차 가족만 Bonferroni · 민감도는 미보정 명시 · 교차적합(R22)")

# ── ⑩ max 바닥 부재 · ASCII
assert "nanmax" not in ALL_SRC and "np.maximum(np.stack" not in ALL_SRC, \
    "❌ Q7-I″ 의 max 바닥이 되살아났다(R25)"
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
     "K_FOLD, N_REPEAT, SEED0, NB_BOOT = 3, 1, 20260803, 800\n"
     "MIN_CELL_S, MIN_CELL_N = 3, 3\nKS = (8, 16)\nLB_K = 16\n"
     "class AssetError(RuntimeError): pass\n", NS)
exec(grab(SRC_A, "def local_base("), NS)
exec(grab(SRC_B, "def joint_key("), NS)
exec(grab(SRC_D, "def boot_diff("), NS)
rhythm_feats, build_scores = NS["rhythm_feats"], NS["build_scores"]
joint_key, cell_auc, boot_excess = NS["joint_key"], NS["cell_auc"], NS["boot_excess"]


def make_record(rng, n=3200, prev=0.26, base=280.0, sd=40.0, early=0.62,
                drift=0.22, morph=0.0, noise=0.8, w=85):
    """`pre_rr` 은 **정수 격자**(SVDB 실측 Δ = 1.0 샘플) 위에 만든다.

    drift : 국소 기저선이 천천히 흔들리는 정도. >0 이면 **같은 절대 RR 인데 국소
            기저선이 다른** 비트가 생긴다 → `pre` 만 맞추면 `f2` 가 산다(Q7-I‴ K3).
    morph : S 비트의 형태 창에 심는 **진짜 형태 차이**. 0 이면 형태 신호가 없다.
    """
    n_s = max(int(n * prev), 40)
    t = np.zeros(n, bool)
    t[rng.choice(np.arange(3, n - 3), size=n_s, replace=False)] = True
    loc = base * (1.0 + drift * np.sin(2 * np.pi * np.arange(n) / 240.0))
    pre = np.where(t, loc * early, loc) + rng.normal(0, sd, n)
    pre = np.round(np.clip(pre, 90.0, 600.0))                 # ★ 정수 격자
    post = np.r_[pre[1:], base]
    B = rng.normal(0, noise, (n, 2, w)).astype("float32")
    if morph:
        B[t] += (morph * np.exp(-((np.arange(w) - w / 2) ** 2) / (2 * (w / 6) ** 2))
                 ).astype("float32")[None, None, :]
    return B, t, pre.astype(float), post.astype(float)


def cohort(seed, nrec=6, scramble=False, **kw):
    rng = np.random.RandomState(seed)
    out = []
    for _ in range(nrec):
        B, t, pre, post = make_record(rng, **kw)
        if scramble:
            t = rng.permutation(t)
        X, NAMES, lb = rhythm_feats(pre, post, (8, 16))
        S = build_scores(X, NAMES, t, {"stt": B}, 20260803)
        assert S is not None, "합성 코호트에서 교차적합이 실패했다"
        out.append(dict(B=B, tt=t, pre=pre, lb=lb, X=X, NAMES=NAMES, S=S))
    return out


def macro(recs, arm, bw_f):
    """bw_f=None → pre 만 정합(Q7-I‴ 재현). 아니면 합동 정합."""
    v, g2 = [], []
    for r in recs:
        med = float(np.median(r["pre"]))
        key = joint_key(r["pre"], r["lb"], None if bw_f is None else bw_f * med)
        a, ks_, pr_, nc_, r1, r2 = cell_auc(r["S"][arm], r["tt"], key, 3, 3,
                                            pre_v=r["pre"], f2_v=r["S"]["f2_16"])
        if pr_ >= 1:
            v.append(a); g2.append(r2)
    assert v, f"{arm}: 칸이 하나도 안 생겼다"
    return float(np.mean(v)), float(np.nanmedian(g2)), len(v)


def shuffle_null(recs, arm, bw_f, n_shuf=3):
    m_, se_ = [], []
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
            a, _, pr_, _, _, _ = cell_auc(Ss[arm], ts, key, 3, 3)
            if pr_ >= 1:
                acc.append(a)
        if len(acc) >= 2:
            m_.append(float(np.mean(acc)))
            se_.append(float(np.std(acc, ddof=1) / np.sqrt(len(acc))))
    return np.array(m_), np.array(se_)


BW = 0.03

# ── ⑪ ★★ 합동 정합은 f1·f2 를 둘 다 죽인다 (pre 만 맞추면 f2 는 산다)
SIG = cohort(11, nrec=5, n=9000, prev=0.25, sd=35, morph=1.1)
f1_pre, _, _ = macro(SIG, "f1", None)
f2_pre, _, _ = macro(SIG, "f2_16", None)
f1_jt, g2_jt, njt = macro(SIG, "f1", BW)
f2_jt, _, _ = macro(SIG, "f2_16", BW)
assert njt >= 4, f"❌ 합동 정합 가능 개체 {njt} — 픽스처 설계 실패"
assert abs(f1_pre - 0.5) < 1e-9, f"❌ 정확 pre 정합에서 f1 이 {f1_pre:.9f} (동점뿐이어야)"
assert f2_pre > 0.80, f"❌ 정확 pre 만 맞췄는데 f2 가 {f2_pre:.4f} — Q7-I‴ K3 를 재현 못 한다"
assert f1_jt < 0.60, f"❌ 합동 정합에서 f1 이 {f1_jt:.4f}"
assert f2_jt < 0.62, f"❌ 합동 정합인데 f2 가 {f2_jt:.4f} — 상대 조기성이 안 죽었다"
assert f2_pre - f2_jt > 0.25, f"❌ f2 가 충분히 안 떨어졌다 ({f2_pre:.4f} → {f2_jt:.4f})"
assert g2_jt < 0.03, f"❌ 합동 정합 후 f2 짝 잔여가 {g2_jt:.4f}"
print(f"  ✅ ⑪ 정확pre: f1 {f1_pre:.4f} · f2 **{f2_pre:.4f}(생존)** → "
      f"합동: f1 {f1_jt:.4f} · f2 **{f2_jt:.4f}** (f2 짝잔여 {g2_jt:.4f}) — 두 축이 같이 죽는다")

# ── ⑫ ★★ 결정적 짝 — 형태 신호 있음 / 없음
FLAT = cohort(12, nrec=5, n=9000, prev=0.25, sd=35, morph=0.0)
s_sig, _, _ = macro(SIG, "stt", BW)
s_flt, _, _ = macro(FLAT, "stt", BW)
n_sig, e_sig = shuffle_null(SIG, "stt", BW)
n_flt, e_flt = shuffle_null(FLAT, "stt", BW)
exc_sig = s_sig - float(np.mean(n_sig))
exc_flt = s_flt - float(np.mean(n_flt))
assert exc_sig > 0.10, f"❌ 형태를 심었는데 합동 정합 STT 초과가 {exc_sig:+.4f}"
assert abs(exc_flt) < 0.06, f"❌ 형태가 없는 코호트인데 STT 초과가 {exc_flt:+.4f}"
assert exc_sig - exc_flt > 0.08, "❌ 두 코호트가 안 갈린다"
print(f"  ✅ ⑫ 합동 정합 STT 초과 — 형태 심음 {exc_sig:+.4f} vs 없음 {exc_flt:+.4f}")

# ── ⑬ 셔플 null 이 교차적합 바닥을 잡는가
RND = cohort(13, nrec=5, n=9000, prev=0.25, sd=35, scramble=True, morph=1.1)
r_obs, _, _ = macro(RND, "lr_norr", BW)
r_nul, _ = shuffle_null(RND, "lr_norr", BW)
exc_rnd = r_obs - float(np.mean(r_nul))
assert abs(exc_rnd) < 0.07, f"❌ 라벨 무작위인데 LR(f3,f4) 초과가 {exc_rnd:+.4f}"
print(f"  ✅ ⑬ 라벨 무작위 코호트에서 초과분 {exc_rnd:+.4f} ≈ 0")

# ── ⑭ ★ boot_excess 가 null 오차를 전파하는가
obs = np.array([s_sig] * len(n_sig)) if len(n_sig) else np.array([])
obs = np.array([macro([r], "stt", BW)[0] for r in SIG])[:len(n_sig)]
msk = np.ones(len(obs), bool)
_, lo_a, hi_a, _ = boot_excess(obs, n_sig, np.zeros_like(e_sig), 7, msk)
_, lo_b, hi_b, _ = boot_excess(obs, n_sig, e_sig + 0.05, 7, msk)
assert (hi_b - lo_b) > (hi_a - lo_a), \
    f"❌ null SE 를 키웠는데 CI 가 안 넓어졌다 ({hi_a-lo_a:.4f} → {hi_b-lo_b:.4f})"
print(f"  ✅ ⑭ null 오차 전파 — CI 폭 {hi_a-lo_a:.4f} → **{hi_b-lo_b:.4f}** (SE +0.05)")

print("\n✅ Q7-K 픽스처 14/14 통과")
