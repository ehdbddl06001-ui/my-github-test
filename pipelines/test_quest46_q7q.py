"""퀘스트46 Q7-Q(`p_late_strict` + 양성 대조) 픽스처.

Q7-P(`ailab-2026-0065`)가 남긴 두 미결은 **선행 관계**다:
    ⓐ `p_late` 우위의 정체 — P/PR 축인가 **QRS 개시 형태**인가
    ⓑ **측정기의 검출 바닥을 모른다** — +0.03 이 바닥 위인지 아래인지

ⓑ 없이 ⓐ 를 물으면 음성 결과가 「QRS 개시였다」인지 「폭을 줄여 바닥 아래로 갔다」인지
구분되지 않는다. 그래서 **같은 노트북·같은 추정량·같은 폭**에서 둘을 함께 잰다.

픽스처의 핵심은 셋이다:

    **양성 대조가 실제로 교정기 노릇을 하는가** — 주입 진폭이 커지면 회수가 **단조 증가**
    하고, 주입 0 이면 회수도 0 이어야 한다. 이게 깨지면 검출 바닥이 의미가 없다
    **폭 22 계열이 진짜 같은 폭이고 겹치지 않는가** — 코드가 raise 하는지까지
    **Q7-P 의 오독을 규칙으로 막았는가**(R32) — `raw` 앵커 · 양수 누출 바닥 · 컷 코호트 부재

정적 검사:
  ① `run.*` API(finish dict 포함) · fallback 부재(R16)
  ② ★★ `ladder_read()` 가 **`raw` 앵커**로 판정하는가(R32 ②) — Q7-P 가 여기서 틀렸다
  ③ ★★ 누출 바닥이 **양의 초과분 최댓값**이고 음의 초과는 **분리 보고**되는가(R32 ④)
  ④ ★ 누출 바닥을 **짝의 차이에서 빼지 않는가**(R32 ⑤)
  ⑤ ★★ **컷 기반 코호트를 안 만드는가**(R32 ③) — Q7-P 의 SAFE 실패
  ⑥ ★★ 폭 22 계열이 **코드로 강제**되는가(폭 동일 + 겹침 없음 · R27 ③ · R30 ③)
  ⑦ ★ `p_late_strict` 가 **QRS 개시(≈R−45ms) 앞에서 끝나는가**
  ⑧ ★ 버린 띠(`p_mid_22`)가 실제로 Q7-F 가 버린 index 33–52 를 덮는가
  ⑨ ★★ 양성 대조가 **주입 후 null 을 다시 재지 않는 근거**를 적었는가 · 상한임을 명시했는가
  ⑩ ★ `judge()` 가 등가·우월성·필요표본을 한 관문에서 전부(R31 ① · R30 ①)
  ⑪ ★ 공동 1차(`strat`/`rank`) **효율 표**가 있는가(R32 ⑥)
  ⑫ ★ Q3 이 **개체 내**임을 명시하고, Q7-P 의 `lr_all`−`lr_norr` 오용을 막았는가
  ⑬ null SE 전파 · 셔플 20회 이상 · 교차적합(R22) · Bonferroni
  ⑭ 「측정 불가」가 어떤 결론 분기도 안 타는가(R29 ②) · 그림 라벨 ASCII

동적 검사 — 노트북 함수를 **그대로 꺼내** 합성 코호트로 실행한다:
  ⑮ ★★ **양성 대조 단조성** — 주입 0 → 회수 ≈0, 진폭 ↑ → 회수 **단조 증가**
  ⑯ ★★ **`p_late_strict` 가 QRS 개시를 안 문다** — QRS 개시에만 심은 신호가 고정 창에서
     안 잡히고 `p_late`(구 창)에서는 잡힌다. **이게 Q1 의 판별력 그 자체다**
  ⑰ ★ `qrs_onset()` 이 심어둔 개시를 **되찾고**, 잡음에서는 **포화를 자백**하는가
  ⑱ ★ `ladder_read()` — Q7-P 실측 사다리를 「교란」으로 오독하지 않는가(R32 ② 회귀 테스트)
"""
import os, sys, json, re
import unicodedata
import numpy as np
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
NB = json.load(open(os.path.join(ROOT, "notebooks", "quest46_q7q_late_strict.ipynb")))
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
SRC_A, SRC_B = cell("【Q-A】"), cell("【Q-B】")
SRC_C, SRC_D = cell("【Q-C】"), cell("【Q-D】")
SRC_E, SRC_F, SRC_FIG = cell("【Q-E】"), cell("【Q-F】"), cell("【Q-G】")
ALL_SRC = "".join("".join(c["source"]) for c in CODE)
RPRE = 100

print("### 정적 검사")

# ── ① API
for m in ("run.log(", "run.save_json(", "run.save_fig(", "run.finish("):
    assert m in ALL_SRC, f"❌ {m} 가 없다"
assert re.search(r"run\.finish\(\s*\{", ALL_SRC), "❌ run.finish 에 result dict 를 안 넘긴다"
assert "fallback 없음" in cell("【Q-0a】"), "❌ R16 표기가 없다"
print("  ✅ ① run.* API(finish dict) · fallback 부재(R16)")

# ── ② ★★ raw 앵커 (R32 ② — Q7-P 가 틀린 지점)
assert "def ladder_read(" in SRC_0, "❌ 사다리 판정 함수가 없다"
lr = SRC_0[SRC_0.index("def ladder_read("):SRC_0.index("class AssetError")]
assert '"raw" not in lad' in lr, "❌ `raw` 앵커 부재를 검사하지 않는다(R32 ②)"
assert 'amax != "raw"' in lr, "❌ **`raw` 가 최댓값인지**를 안 본다 — 교란 판정의 핵심이다"
assert "교란으로 읽지 않는다" in lr, "❌ raw 가 최댓값이 아닐 때의 처리가 없다"
lad = eval(re.search(r"^LADDER\s*=\s*(\([^)]*\))", SRC_SET, re.M).group(1))
assert lad[0] == "raw", f"❌ 사다리가 `raw` 로 시작하지 않는다 {lad}"
assert "ladder_read(" in SRC_E, "❌ 관문에서 사다리를 안 읽는다"
print(f"  ✅ ② `raw` 앵커로 교란 판정 · 사다리 {' → '.join(lad)} (R32 ②)")

# ── ③ ★★ 누출 바닥 = 양의 초과 max · 음의 초과 분리
_li = SRC_E.index("LEAK_ARMS")          # ⚠️ "효율 표" 는 셀 헤더에도 있다 — 뒤에서 찾는다
leak = SRC_E[_li:SRC_E.index("효율 표", _li)]
assert "pos, neg" in leak or ("pos" in leak and "neg" in leak), "❌ 양/음 초과를 안 가른다"
assert "max((v[0] for v in pos.values())" in leak, \
    "❌ 누출 바닥이 **양의 초과분 최댓값**이 아니다(R32 ④) — abs() 를 쓰면 Q7-P 처럼 0.3167 이 잡힌다"
assert "과잉보정" in leak, "❌ 음의 초과분을 **과잉보정 진단**으로 분리 보고하지 않는다"
assert "abs(mm_)" not in leak, "❌ 절댓값 바닥이 남아 있다(R32 ④ 위반)"
print("  ✅ ③ 누출 바닥 = **양의 초과 최댓값** · 음의 초과는 분리 진단(R32 ④)")

# ── ④ ★ 바닥을 짝의 차이에서 빼지 않는다
assert "짝의 차이" in leak and "빼지 않는다" in leak, "❌ R32 ⑤ 명시가 없다"
assert not re.search(r"DIFF\[[^\]]*\]\[.mean.\]\s*-\s*LEAK_MAX", ALL_SRC), \
    "❌ 짝의 차이에서 누출 바닥을 빼고 있다 — 공통 누출은 상쇄된다(R32 ⑤)"
print("  ✅ ④ 누출 바닥을 **수준에만** 적용 · 짝의 차이에서 안 뺀다(R32 ⑤)")

# ── ⑤ ★★ 컷 기반 코호트 부재 (R32 ③)
for bad in ("safe_mask", "p_safe_seg", "q_safe_seg", "SAFE 코호트를 만든다"):
    assert bad not in ALL_SRC, f"❌ 컷 기반 코호트가 남아 있다: {bad} (R32 ③)"
assert "마스크를 만들지 않는다" in SRC_A, "❌ 마스크를 안 만든다는 근거가 없다"
assert "R32 ③ 컷 코호트 금지" in SRC_SET, "❌ 체크리스트에 R32 ③ 이 없다"
print("  ✅ ⑤ **컷 기반 코호트 없음** — 전 개체를 쓴다(R32 ③)")

# ── ⑥ ★★ 폭 22 계열이 코드로 강제된다
segs22 = eval(re.search(r"SEGS22 = (\{.*?\})", SRC_SET, re.S).group(1))
w = {k: v[1] - v[0] for k, v in segs22.items()}
assert len(set(w.values())) == 1, f"❌ 폭이 다르다 {w} — R27 ③"
order = sorted(segs22.values())
for (a1, b1), (a2, b2) in zip(order, order[1:]):
    assert b1 <= a2, f"❌ 창이 겹친다 {(a1,b1)} vs {(a2,b2)}"
assert "R27 ③ 위반" in cell("【Q-0a】") and "겹친다" in cell("【Q-0a】"), \
    "❌ 폭 정합·겹침이 **코드로 강제**되지 않는다(주석은 Q7-M 에서 이미 실패했다)"
print(f"  ✅ ⑥ 폭 22 계열 코드 강제 — " + " · ".join(
    f"{k}{v}" for k, v in segs22.items()) + " (겹침 없음)")

# ── ⑦ ★ p_late_strict 가 QRS 개시 앞에서 끝난다
end_ms = (segs22["p_late_strict"][1] - RPRE) / 360 * 1000
assert end_ms <= -60, f"❌ p_late_strict 가 R{end_ms:+.0f}ms 에서 끝난다 — QRS 개시(≈−45ms)에 너무 가깝다"
old_end_ms = (85 - RPRE) / 360 * 1000
assert end_ms < old_end_ms, "❌ 구 `p_late`(끝 −42ms)보다 앞에서 안 끝난다 — 자른 게 없다"
print(f"  ✅ ⑦ `p_late_strict` 끝 R{end_ms:+.0f}ms < 구 `p_late` 끝 R{old_end_ms:+.0f}ms "
      f"(QRS 개시 ≈−45ms 에서 {abs(end_ms)-45:.0f}ms 여유)")

# ── ⑧ ★ 버린 띠를 덮는가 (Q7-F 가 버린 index 33–52)
mid = segs22["p_mid_22"]
assert mid[0] <= 33 + 2 and mid[1] >= 52 - 2, \
    f"❌ `p_mid_22`{mid} 가 Q7-F 가 버린 띠(33–52)를 안 덮는다"
print(f"  ✅ ⑧ `p_mid_22`{mid} 가 버린 띠(33–52 · P 종말부)를 덮는다")

# ── ⑨ ★★ 양성 대조의 전제가 적혀 있는가
assert "상한" in SRC_D and "동일 파형" in SRC_D, \
    "❌ 양성 대조가 **검출력의 상한**이라는 근거가 없다"
assert "null 을 다시 안 잰다" in SRC_D or "null 을 다시 안 재는" in SRC_D, \
    "❌ 주입 후 null 을 재사용하는 근거가 없다"
amps = eval(re.search(r"^AMPS\s*=\s*(\([^)]*\))", SRC_SET, re.M).group(1))
assert len(amps) >= 3 and min(amps) <= 0.05, f"❌ 주입 진폭 격자가 얇다 {amps}"
assert "검출 바닥" in SRC_E, "❌ 검출 바닥을 관문 셀에서 안 낸다"
print(f"  ✅ ⑨ 양성 대조 진폭 {amps} · 상한임을 명시 · null 재사용 근거 있음")

# ── ⑩ ★ judge()
assert "def judge(" in SRC_0 and "def need_n(" in SRC_0 and "def equiv(" in SRC_0
js = SRC_0[SRC_0.index("def judge("):SRC_0.index("def ladder_read(")]
for m in ("equiv(", "decide(", "need_n("):
    assert m in js, f"❌ judge() 가 {m} 를 안 쓴다(R31 ① · R30 ①)"
assert "judge(" in SRC_E, "❌ 관문이 judge() 를 안 쓴다"
print("  ✅ ⑩ judge() 가 등가·우월성·필요표본을 한 관문에서 전부(R31 ① · R30 ①)")

# ── ⑪ ★ 효율 표 (R32 ⑥)
assert re.search(r"^PRIMARY, CO_PRIMARY\s*=", SRC_SET, re.M), "❌ 공동 1차 선언이 없다"
assert "효율 표" in SRC_E and "배**" in SRC_E, "❌ CI 폭 비 표가 없다(R32 ⑥)"
assert "AIPW" in SRC_SET, "❌ AIPW 로 가는 다음 단계가 적혀 있지 않다"
print("  ✅ ⑪ `strat`/`rank` 공동 1차 + 효율(CI 폭 비) 표(R32 ⑥)")

# ── ⑫ ★ Q3 의 범위와 Q7-P 오용 차단
assert "개체 내" in SRC_F and "교차환자가 아니다" in SRC_F, \
    "❌ Q3 이 개체 내라는 한계가 명시돼 있지 않다"
assert "창 특징이 0개" in SRC_F, \
    "❌ Q7-P 의 `lr_all`−`lr_norr` 오용(둘 다 창 특징 0개)을 막는 문구가 없다"
rhy = eval(re.search(r"RHY_COLS = (\[[^\]]*\])", SRC_A).group(1))
assert all(c.startswith(("f1", "f2", "f3", "f4", "f5", "f6")) for c in rhy), \
    f"❌ 리듬 전용 팔에 창 특징이 섞였다 {rhy}"
print(f"  ✅ ⑫ Q3 은 **개체 내** 명시 · 리듬 전용 팔 {len(rhy)}개 전부 RR 파생")

# ── ⑬ null SE · 셔플 · 교차적합 · Bonferroni
assert "NSE" in SRC_C and "std(ddof=1)" in SRC_C, "❌ null 의 셔플 SE 를 안 낸다"
assert "rng.normal(0.0, 1.0, len(ix)) * se[ix]" in SRC_E, "❌ null 오차를 CI 에 안 흔든다"
n_shuf = int(re.search(r"^N_SHUF\s*=\s*(\d+)", SRC_SET, re.M).group(1))
assert n_shuf >= 20, f"❌ 셔플 {n_shuf}회"
assert "fold = rng.permutation(len(tt)) % K" in SRC_A, "❌ 교차적합(R22)이 아니다"
assert "BONF3" in SRC_SET and "BONF3 * 100" in SRC_E, "❌ 1차 가족 보정이 없다"
print(f"  ✅ ⑬ 셔플 {n_shuf}회 · null SE 전파(R26 ②) · 교차적합(R22) · Bonferroni")

# ── ⑭ 측정 불가 분기 · ASCII
assert 'un_ = lambda k: VERD.get(k, "").startswith("⛔")' in SRC_FIG, "❌ 측정 불가 검사가 없다"
assert 'if un_("Q1")' in SRC_FIG, "❌ Q1 결론 분기가 측정 불가를 먼저 안 거른다"
assert "not un_(g)" in SRC_FIG, "❌ ⛔ 관문에 등가 주석이 그대로 붙는다(R29 ②)"
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
     "from sklearn.linear_model import LogisticRegression\n"
     "from sklearn.metrics import roc_auc_score\n"
     "BASIS_K=(4,6,8,12,16,24,32)\nPROBE_K=(5,10,20)\nHIST_K=64\nLB_K=16\nTREND_W=8\n"
     f"F2_BIN=0.02\nRPRE={RPRE}\nSEGS22={segs22}\n"
     "SEGS=dict(SEGS22, **{'p_late':(53,85)})\n"
     "ONSET_SEARCH=(70,96)\nONSET_FRAC=0.15\nONSET_RUN=3\nQRS_LO,QRS_HI=85,115\n"
     "K_FOLD,N_REPEAT,SEED0=3,1,20260803\n"
     "class AssetError(RuntimeError): pass\n", NS)
exec(grab(SRC_0, "def decide(", "class AssetError"), NS)
exec(grab(SRC_A, "def local_base("), NS)
qrs_onset, two_template_cv = NS["qrs_onset"], NS["two_template_cv"]
strat_key, strat_auc, all_feats = NS["strat_key"], NS["strat_auc"], NS["all_feats"]
ladder_read = NS["ladder_read"]
from sklearn.metrics import roc_auc_score

W22 = list(w.values())[0]


def make_record(seed, n=2200, prev=0.16, base=330.0, sd=42.0, L=300,
                onset=84, p_amp=0.0, p_at=None, onset_amp=0.0, noise=0.5,
                qrs_w=5.0):
    """합성 레코드. `p_at` 창 중앙에 S 전용 P 섭동, `onset_amp` 는 **QRS 개시에만** 심는다."""
    rng = np.random.RandomState(seed)
    t = np.zeros(n, bool)
    t[rng.choice(np.arange(3, n - 3), size=max(int(n * prev), 60), replace=False)] = True
    pre = rng.normal(base, sd, n)
    pre[t] *= rng.uniform(0.55, 0.92, int(t.sum()))
    pre = np.round(np.clip(pre, 120.0, 620.0))
    post = np.round(np.clip(np.r_[pre[1:], base], 120.0, 900.0))
    x = np.arange(L, dtype=float)
    B = rng.normal(0, noise, (n, 2, L))
    B += (3.5 * np.exp(-((x - RPRE) ** 2) / (2 * qrs_w ** 2)))[None, None, :]  # QRS
    B += (0.9 * np.exp(-((x - 170.0) ** 2) / (2 * 22.0 ** 2)))[None, None, :]  # T
    if p_amp and p_at is not None:
        a_, b_ = p_at; c = (a_ + b_ - 1) / 2.0
        B[t] += (p_amp * np.exp(-((x - c) ** 2) / (2 * ((b_ - a_) / 6.0) ** 2))
                 )[None, None, :]
    if onset_amp:                       # ★ QRS 개시 **직전 10샘플**에만
        B[t] += (onset_amp * np.exp(-((x - (onset + 3)) ** 2) / (2 * 3.0 ** 2))
                 )[None, None, :]
    return B.astype("float32"), t, pre.astype(float), post.astype(float)


def excess(B, t, pre, post, win, n_shuf=3):
    """창 `win` 의 층화 초과분(실측 − 셔플 null). 노트북과 같은 추정량."""
    F = all_feats(pre, post); key = strat_key(F)
    a_, b_ = NS["SEGS"][win]
    Bw = np.ascontiguousarray(B[:, :, a_:b_]).astype("float64")
    st = two_template_cv(Bw, t, 3, 20260803, 1)
    if st is None:
        return float("nan")
    obs = strat_auc(st, t, key)
    nulls = []
    for s_ in range(n_shuf):
        rng = np.random.RandomState(555 + 97 * s_)
        ts = rng.permutation(t)
        stn = two_template_cv(Bw, ts, 3, 20260803, 1)
        if stn is not None:
            nulls.append(strat_auc(stn, ts, key))
    return obs - float(np.mean(nulls))


# ── ⑮ ★★ 양성 대조 단조성 — 교정기로 쓸 수 있는가
SEED = 31
rec0 = make_record(SEED)
curve = []
for a_ in (0.0, 0.05, 0.10, 0.20):
    B, t, pre, post = make_record(SEED, p_amp=a_ * 3.5, p_at=segs22["p_late_strict"])
    curve.append(excess(B, t, pre, post, "p_late_strict"))
assert abs(curve[0]) < 0.06, f"❌ 주입 0 인데 회수가 {curve[0]:+.4f} — 교정기가 0점이 안 맞는다"
assert all(curve[i] <= curve[i + 1] + 1e-9 for i in range(len(curve) - 1)), \
    f"❌ 주입 진폭에 대해 회수가 **단조 증가**하지 않는다 {curve} — 검출 바닥이 무의미해진다"
assert curve[-1] - curve[0] > 0.15, \
    f"❌ 진폭 20% 를 심었는데 회수가 {curve[-1]-curve[0]:+.4f} — 교정기 감도가 없다"
print("  ✅ ⑮ 양성 대조 단조 — " +
      " → ".join(f"a={a_:.2f} {v:+.4f}" for a_, v in zip((0, .05, .10, .20), curve)))

# ── ⑯ ★★ Q1 의 판별력 — QRS 개시 신호를 고정 창이 안 문다
B, t, pre, post = make_record(SEED, onset_amp=1.6)      # **QRS 개시에만** 신호
e_strict = excess(B, t, pre, post, "p_late_strict")
e_old = excess(B, t, pre, post, "p_late")
assert e_old > 0.10, f"❌ QRS 개시에 심었는데 구 `p_late` 가 {e_old:+.4f} — 시나리오가 안 섰다"
assert e_strict < 0.5 * e_old, \
    (f"❌ **`p_late_strict` 가 QRS 개시를 여전히 문다** (strict {e_strict:+.4f} vs "
     f"old {e_old:+.4f}) — 그러면 Q1 은 P/PR 축과 QRS 개시를 못 가른다")
Bp, tp, prep_, postp = make_record(SEED, p_amp=1.6, p_at=segs22["p_late_strict"])
e_pr = excess(Bp, tp, prep_, postp, "p_late_strict")
assert e_pr > 0.10, f"❌ PR 분절에 심었는데 `p_late_strict` 가 {e_pr:+.4f} — 감도가 없다"
print(f"  ✅ ⑯ 판별력 — QRS 개시 신호: 구 p_late **{e_old:+.4f}** vs strict **{e_strict:+.4f}**"
      f"(안 문다) | PR 분절 신호: strict **{e_pr:+.4f}**(잡는다)")

# ── ⑰ ★ QRS 개시 검출기 — **심어둔 개시를 되찾는가 · 포화를 자백하는가**
# ⚠️ 초판은 「탐색 범위 안인가」만 봐서 **경계 포화를 통과시켰다**(중앙 96 = R−11ms).
#    이제 ⓐ 깨끗한 신호에서 심어둔 개시를 되찾고 ⓑ 잡음에서 포화를 **보고**하는지 본다.
for true_on in (80, 84, 88):
    B2, t2, _, _ = make_record(SEED + 1, onset=true_on, qrs_w=(RPRE - true_on) / 2.6,
                               noise=0.05)
    est, sat = qrs_onset(B2[:, 0, :])
    med = float(np.median(est))
    assert sat.mean() < 0.5, f"❌ 깨끗한 신호인데 포화율 {sat.mean():.2f}"
    assert abs(med - true_on) <= 8, \
        f"❌ 개시 {true_on} 을 심었는데 {med:.0f} 로 추정 (오차 {med-true_on:+.0f})"
_, sat_noisy = qrs_onset(make_record(SEED + 2, noise=1.2)[0][:, 0, :])
assert sat_noisy.mean() > 0.0, "❌ 잡음이 심한데 포화를 하나도 보고하지 않는다"
assert "포화" in SRC_A and "ONSET_OK" in SRC_A, "❌ 노트북이 포화를 진단하지 않는다"
assert "if ONSET_OK else []" in SRC_F or "ONSET_OK" in SRC_F, \
    "❌ 포화 시 적응형 팔(Q4)을 건너뛰지 않는다 — 못 믿을 창으로 민감도를 쓴다"
print(f"  ✅ ⑰ `qrs_onset()` 이 심어둔 개시 80/84/88 을 ±8 안에서 되찾고, "
      f"잡음에서는 **포화를 자백**한다(포화율 {sat_noisy.mean():.2f} → Q4 미실행)")

# ── ⑱ ★★ ladder_read() — Q7-P 실측의 회귀 테스트 (R32 ②)
q7p = {"raw": 0.0469, "lin": 0.0745, "hist": 0.0621, "quad": 0.0564,
       "rank": 0.0466, "strat": 0.0314}
v = ladder_read(q7p)
assert "교란으로 읽지 않는다" in v, \
    f"❌ Q7-P 사다리를 여전히 「잔여 교란」으로 읽는다: {v}"
real = {"raw": 0.20, "lin": 0.15, "hist": 0.12, "quad": 0.10, "rank": 0.08, "strat": 0.06}
assert "잔여 교란" in ladder_read(real), "❌ raw 가 최댓값인 진짜 감쇠를 못 잡는다"
assert "앵커가 없다" in ladder_read({"lin": .07, "quad": .05, "strat": .03}), \
    "❌ raw 없는 사다리를 그냥 판정한다(R32 ②)"
print("  ✅ ⑱ ladder_read() — Q7-P 사다리를 **잔차화 인공물**로, raw 최대 감쇠를 "
      "**잔여 교란**으로 정확히 가른다")

print("\n✅ Q7-Q 픽스처 18/18 통과")
