"""퀘스트46 Q7-F(P 창 심박수 교란) 픽스처.

이 실험은 **정오 확인**이다 — Q7-D·E·H 의 「형태 축」이 P 파인지, 심박수 때문에 창
안 내용물이 바뀐 인공물인지. 그래서 픽스처의 핵심은 하나다:

    **교란을 심어 넣으면 관문이 실제로 그걸 잡아내는가.**

못 잡으면 이 노트북은 「형태가 진짜다」를 찍어주는 도장기다.

정적 검사:
  ① `run.*` API 정합 + fallback 부재(R16)
  ② 구간 정의 — `P_early`·`P_late` 가 **폭이 같고** 겹치지 않는가 (폭이 다르면
     차원 수 차이가 곧 결론이 된다)
  ③ 두 템플릿이 Q7-H 와 같이 **교차적합 × 되풀이** 되는가 (R22)
  ④ **F1 은 평가만 제한**하는가 — 정합 부분집합에서 템플릿을 다시 적합하면
     한 번에 두 개를 바꾸는 것이다
  ⑤ 정합의 대가(남은 S·쌍·개체 수)를 **관문보다 먼저** 출력하고, 개체가 모자라면
     **미결**로 빠지는가 (R17 — 조용히 적은 n 으로 판정하지 않는다)
  ⑥ ★ **F4 의 방향이 반대라는 것**이 코드·출력에 박혀 있는가 (지지 = 교란 있음)
  ⑦ 직전 T 위치가 **모형 어림**임을 밝히는가 (실측 T 주석이 없다)
  ⑧ 문턱이 CELL 1 상수이고 관문 셀에서 다시 안 고르는가
  ⑨ 결론 문장이 **관문 조합으로만** 만들어지는가 · 갈리면 갈렸다고 쓰는가(R18)
  ⑩ 그림 라벨이 ASCII 인가

동적 검사 — 관문 셀을 **합성 코호트로 실제 실행**한다:
  ⑪ **null** (P 차이 없음 · RR 차이 없음) — 아무것도 안 나와야 한다
  ⑫ ★★ **T 침입** (P 파는 S·N 이 **완전히 같고** RR 만 다르다) —
     F2 가 기각되고 F4 가 지지돼야 한다. **이게 이 픽스처의 존재 이유다**
  ⑬ ★ **진짜 P** (P 파가 다르고 **RR 은 같다**) — F1·F2 지지 · F4 비지지
  ⑭ **둘 다** (P 도 다르고 RR 도 다르다) — 정합해도 살아남아야 한다(F1 지지)
"""
import os, sys, json, re
import unicodedata
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
NB = json.load(open(os.path.join(ROOT, "notebooks", "quest46_q7f_window_confound.ipynb")))
CODE = [c for c in NB["cells"] if c["cell_type"] == "code"]


def cell(tag):
    hit = [c for c in CODE if "".join(c["source"]).split("\n", 1)[0].startswith("# CELL")
           and tag in "".join(c["source"]).split("\n", 1)[0]]
    assert len(hit) == 1, f"헤더가 '{tag}' 인 셀을 {len(hit)}개 찾았다"
    return "".join(hit[0]["source"])


SRC_SET = [c for c in CODE if "".join(c["source"]).startswith("# CELL 1 ")]
assert len(SRC_SET) == 1
SRC_SET = "".join(SRC_SET[0]["source"])
SRC_A, SRC_B = cell("【F-A】"), cell("【F-B】")
SRC_C, SRC_D = cell("【F-C】"), cell("【F-D】")
SRC_FIG = [c for c in CODE if "".join(c["source"]).startswith("# CELL 7")]
assert len(SRC_FIG) == 1
SRC_FIG = "".join(SRC_FIG[0]["source"])
ALL_SRC = "".join("".join(c["source"]) for c in CODE)

print("### 정적 검사")

# ── ①
lib = os.path.join(ROOT, "lib", "medkos_run.py")
if os.path.exists(lib):
    have = set(re.findall(r"^\s{4}def (\w+)\(", open(lib).read(), re.M))
    miss = sorted(set(re.findall(r"\brun\.(\w+)\(", ALL_SRC)) - have)
    assert not miss, f"MedKOSRun 에 없는 메서드: {miss}"
    call = re.search(r"MedKOSRun\(([^)]*)\)", ALL_SRC)
    assert call and "project" in call.group(1), "MedKOSRun 호출에 project 없음"
assert "range(800, 895)" not in ALL_SRC and "range(800,895)" not in ALL_SRC, \
    "❌ 연속번호 fallback (R16)"
print("  ✅ ① run.* API 정합 · fallback 부재")

# ── ② 구간 정의
SEGS = {m[0]: (int(m[1]), int(m[2]))
        for m in re.findall(r'"(\w+)":\s*\((\d+),\s*(\d+)\)', SRC_SET)}
for k in ("P_full", "P_early", "P_late", "STT"):
    assert k in SEGS, f"❌ 구간 {k} 가 없다"
we = SEGS["P_early"][1] - SEGS["P_early"][0]
wl = SEGS["P_late"][1] - SEGS["P_late"][0]
assert we == wl, f"❌ P_early({we})·P_late({wl}) 폭이 다르다 — 차원 수 차이가 곧 결론이 된다"
assert SEGS["P_early"][1] <= SEGS["P_late"][0], "❌ P_early 와 P_late 이 겹친다"
assert (SEGS["STT"][1] - SEGS["STT"][0]) == (SEGS["P_full"][1] - SEGS["P_full"][0]), \
    "❌ 음성 대조(STT)가 P_full 과 폭이 다르다 — 공정한 대조가 아니다"
assert SEGS["STT"][0] > 100, "❌ STT 가 R(=100) 이후가 아니다"
print(f"  ✅ ② P_early{SEGS['P_early']}·P_late{SEGS['P_late']} 폭 동일({we}) · 비중첩 · "
      f"STT{SEGS['STT']} 는 P_full 과 동폭")

# ── ③ 교차적합 (R22)
assert "def two_template_cv(" in SRC_B, "❌ 두 템플릿 교차적합 함수가 없다"
assert "fold = rng.permutation(len(tt)) % K" in SRC_B, "❌ K겹 교차적합이 아니다"
assert "medN = np.median(B[tr & ~tt], axis=0); medS = np.median(B[tr & tt], axis=0)" in SRC_B, \
    "❌ 템플릿이 훈련 겹에서 만들어지지 않는다 (R22 — 인-샘플이면 신호 0에서도 0.89)"
assert "sc[te] = dist(B[te], medN) - dist(B[te], medS)" in SRC_B, "❌ 채점이 시험 겹이 아니다"
assert "for rep in range(max(n_rep, 1))" in SRC_B, "❌ 되풀이 교차적합이 아니다"
assert "np.sqrt(se_ ** 2 + rsd ** 2)" in SRC_B, "❌ SE 에 겹 배정 잡음이 안 더해진다 (R22 ②)"
print("  ✅ ③ 두 템플릿은 Q7-H 와 같은 교차적합 × 되풀이 (R22)")

# ── ④ F1 은 평가만 제한
i0 = SRC_B.index("def matched_auc(")
body = SRC_B[i0:]
end = re.search(r"\n(?=\S)", body[body.index("\n"):])
FN = body[:body.index("\n") + end.start() + 1] if end else body
assert "다시 적합하지 않는다" in FN, "❌ '평가만 제한' 규약이 코드에 없다"
for banned in ("median(B", "two_template_cv", "medS", "medN"):
    assert banned not in FN, f"❌ matched_auc 안에서 템플릿을 다시 만든다: {banned}"
assert "np.floor(pre_v / max(band_w" in FN, "❌ pre_rr 대역으로 나누지 않는다"
print("  ✅ ④ F1 은 **평가만** 제한한다 — 정합 부분집합에서 템플릿을 다시 적합하지 않는다")

# ── ⑤ 정합의 대가를 먼저 · 부족하면 미결
assert "정합의 대가" in SRC_B, "❌ 정합의 대가를 출력하지 않는다"
assert SRC_B.index("정합의 대가") < SRC_B.index("{'구간':<24}"), \
    "❌ 정합의 대가가 매크로 표보다 뒤에 나온다 — 대가를 먼저 봐야 한다"
assert "match_ok" in SRC_B and "MIN_MATCH_S" in SRC_B and "MIN_MATCH_PAIR" in SRC_B, \
    "❌ 정합 가능 판정 기준이 없다"
assert "정합 불가 개체" in SRC_B, "❌ 정합 불가 개체를 이름으로 안 남긴다"
j = SRC_C.index('if int(MOK.sum()) < MIN_MATCH_REC:')
seg = SRC_C[j:j + 500]
assert '"⚠️ 미결"' in seg and "이것 자체가 결과다" in seg, \
    "❌ 정합 가능 개체가 모자랄 때 미결로 빠지지 않는다 (R17)"
print("  ✅ ⑤ 정합의 대가를 관문보다 먼저 내고, 개체가 모자라면 미결로 빠진다")

# ── ⑥ F4 의 방향
assert "지지 = 교란" in SRC_D, "❌ F4 의 방향(지지=교란 있음)이 코드에 없다"
# ★ F3 이 말할 수 있는 것의 한계 — 픽스처가 잡았다: T 침입 시나리오(P 파가 완전히 같음)
#   에서도 F3 이 +0.36 으로 지지된다. F3 은 「P 창 안」까지만 말한다
assert "P 파라는 뜻은 아니다" in SRC_C, \
    "❌ F3 지지가 'P 파' 를 뜻하지 않는다는 단서가 없다 — T 침입만으로도 F3 은 통과한다"
assert "방향이 반대" in SRC_D, "❌ F4 가 다른 관문과 방향이 반대임을 밝히지 않는다"
assert "방향이 반대" in SRC_FIG or "지지 = 교란" in SRC_FIG, \
    "❌ 관문 요약 출력에 F4 방향 경고가 없다"
assert 'DIFF["F4"]' in SRC_D and 'boot_rho(A["ov_gap_early"], A["P_early"]' in SRC_D, \
    "❌ F4 가 (T중첩격차 × P_early) 상관이 아니다"
assert 'boot_rho(A["ov_gap_early"], A["P_late"]' in SRC_D, \
    "❌ P_late 대조(같은 상관이 여기선 약해야 한다)가 없다"
print("  ✅ ⑥ F4 는 **지지 = 교란 있음** 으로 표시되고 P_late 대조를 병기한다")

# ── ⑦ T 위치가 모형 어림
assert "모형 어림" in SRC_A, "❌ 직전 T 위치가 모형 어림임을 밝히지 않는다"
assert "T 주석" in SRC_A or "T 주석" in SRC_SET, "❌ 실측 T 주석이 없다는 사실을 안 남긴다"
assert "T_LO, T_HI" in SRC_SET, "❌ T 구간 모형 상수가 CELL 1 에 없다"
print("  ✅ ⑦ 직전 T 위치는 모형 어림으로 표기된다")

# ── ⑧ 문턱은 CELL 1 상수
for nm_ in ("MIN_S_TPL", "K_FOLD", "N_REPEAT", "BAND_FRAC", "MIN_MATCH_S",
            "MIN_MATCH_PAIR", "MIN_MATCH_REC", "NI_MATCH", "F3_MARGIN"):
    assert re.search(rf"^{nm_}\s*=", SRC_SET, re.M), f"❌ {nm_} 가 CELL 1 상수가 아니다"
    for tag, src in (("F-B", SRC_B), ("F-C", SRC_C), ("F-D", SRC_D)):
        assert not re.search(rf"^\s*{nm_}\s*=", src, re.M), f"❌ {nm_} 를 {tag} 에서 다시 고른다"
assert "Q7-H 승계" in SRC_SET, "❌ 승계 상수 표시가 없다"
print("  ✅ ⑧ 사전등록 문턱은 CELL 1 상수 (MIN_S_TPL·K_FOLD·N_REPEAT 은 Q7-H 승계)")

# ── ⑨ 결론은 관문 조합으로만
assert "ok = lambda k:" in SRC_D and "no = lambda k:" in SRC_D, "❌ 결론이 관문 조합이 아니다"
assert "소급 정정" in SRC_D, "❌ '리듬 대리' 판정 시 소급 정정한다는 결론 분기가 없다"
assert "갈렸다" in SRC_D and "R18" in SRC_D, "❌ 갈렸을 때의 처리(R18)가 없다"
print("  ✅ ⑨ 결론 문장은 관문 조합으로만 만들어지고, 갈리면 갈렸다고 쓴다")

# ── ⑩ 그림 ASCII
bad = [t for t in re.findall(r'set_title\(f?"([^"]*)"', SRC_FIG)
       + re.findall(r'set_xlabel\(f?"([^"]*)"', SRC_FIG)
       + re.findall(r'set_ylabel\(f?"([^"]*)"', SRC_FIG)
       if any(unicodedata.name(ch, "").startswith("HANGUL") for ch in t)]
assert not bad, f"❌ 그림 라벨에 한글이 있다: {bad}"
assert "한글이 없어" in SRC_FIG, "❌ 폰트 한계가 코드에 명시돼 있지 않다"
print("  ✅ ⑩ 그림 라벨이 ASCII 다")


# ═══════════════════════════════════════════════════════════════════════
print("\n### 동적 검사 — 교란을 심어 넣고 관문이 잡는지 본다")

import scipy.stats as _st

RPRE = 100
T_LO, T_HI = 0.85, 0.45


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


# 노트북이 정의한 t_overlap 을 **그대로** 쓴다 (픽스처가 따로 구현하면 검사가 무의미하다)
_i = SRC_A.index("def t_overlap(")
_b = SRC_A[_i:]
_e = re.search(r"\n(?=\S)", _b[_b.index("\n"):])
T_OVERLAP_SRC = _b[:_b.index("\n") + _e.start() + 1] if _e else _b


def make_record(rng, n_s, n_n, rr_s, rr_n, rr_sd=35, p_amp=0.0, t_amp=0.0, noise=0.9):
    """비트 (n,2,300) · R = index 100.

    p_amp  : S 와 N 의 **P 파 극성 차이**(index 55 근처)  → '진짜 형태' 신호
    t_amp  : **직전 T** 봉우리 진폭. 위치는 `100 − 0.65·pre_rr` 로 **RR 에 따라 움직인다**
             → p_amp=0 이고 t_amp>0 이면 클래스 차이는 **오직 창이 밀린 것**뿐이다
    """
    n = n_s + n_n
    t = np.r_[np.ones(n_s, bool), np.zeros(n_n, bool)]
    x = np.arange(300)
    qrs = np.exp(-((x - 100) ** 2) / (2 * 6 ** 2)) * 5.0
    cur_t = np.exp(-((x - 172) ** 2) / (2 * 16 ** 2)) * 1.5      # 현재 비트의 T (양 클래스 동일)
    pre = np.where(t, rng.normal(rr_s, rr_sd, n), rng.normal(rr_n, rr_sd, n))
    pre = np.clip(pre, 60, 500)
    B = np.zeros((n, 2, 300), "float32")
    for i in range(n):
        base = qrs + cur_t
        if p_amp:
            base = base + (-p_amp if t[i] else p_amp) * np.exp(-((x - 55) ** 2) / (2 * 8 ** 2))
        if t_amp:
            c = 100 - 0.65 * pre[i]
            base = base + t_amp * np.exp(-((x - c) ** 2) / (2 * 14 ** 2))
        for ch in range(2):
            B[i, ch] = base + rng.normal(0, noise, 300)
    return B, t, pre.astype(float)


def cohort(specs, seed):
    rng = np.random.RandomState(seed)
    Bs, Ys, Rs, Ps = [], [], [], []
    for rec, kw in specs:
        B, t, pre = make_record(rng, **kw)
        Bs.append(B); Ys.append(np.where(t, 1, 0)); Ps.append(pre)
        Rs.append(np.full(len(t), rec, np.int64))
    return (np.concatenate(Bs), np.concatenate(Ys),
            np.concatenate(Rs), np.concatenate(Ps))


def run_cohort(tag, specs, seed=0, cells=("B", "C", "D")):
    print("\n" + "=" * 78); print(f"### {tag}"); print("=" * 78)
    BEAT, Y, REC, PRE = cohort(specs, seed)
    g = {"np": np, "stats": _st, "run": Run(), "AssetError": AssetError, "decide": decide,
         "BEAT": BEAT, "Y": Y, "REC": REC, "PRE": PRE,
         "ALLR": [int(r) for r in np.unique(REC)],
         "SEGS": SEGS, "RPRE": RPRE, "T_LO": T_LO, "T_HI": T_HI,
         "MIN_S_TPL": 20, "K_FOLD": 5, "N_REPEAT": 2,
         "BAND_FRAC": 0.05, "BAND_MIN": 8, "MIN_BAND_S": 3, "MIN_BAND_N": 3,
         "MIN_MATCH_S": 20, "MIN_MATCH_PAIR": 200, "MIN_MATCH_REC": 6,
         "NI_MATCH": 0.05, "F3_MARGIN": 0.05,
         "SEED0": 7, "NB_BOOT": 1200, "NB_REC": 200, "IDX_S": 1, "CONFIG": {}}
    exec(compile(T_OVERLAP_SRC, "q7f_tov", "exec"), g)
    src = {"B": SRC_B, "C": SRC_C, "D": SRC_D}
    for c in cells:
        exec(compile(src[c], f"q7f_{c}", "exec"), g)
    return g


def mac(g, k):
    return float(np.nanmean(g["A"][k]))


# ── ⑪ null
NULL = [(900 + i, dict(n_s=120, n_n=500, rr_s=220, rr_n=220)) for i in range(12)]
g0 = run_cohort("(A) null — P 차이 없음 · RR 차이 없음", NULL, seed=1)
V0 = g0["VERD"]
print(f"    매크로 P_early {mac(g0,'P_early'):.3f} · P_late {mac(g0,'P_late'):.3f}"
      f" · STT {mac(g0,'STT'):.3f}")
for k_ in ("P_early", "P_late", "P_full", "STT"):
    assert abs(mac(g0, k_) - 0.5) < 0.08, \
        f"A: 신호가 0인데 {k_} 가 {mac(g0,k_):.4f} 다 — 지표가 샌다(교차적합 확인)"
assert not V0["F2"].startswith("✅"), f"A: 차이가 없는데 F2 가 지지다 — {V0['F2']}"
assert not V0["F3"].startswith("✅"), f"A: 차이가 없는데 F3 가 지지다 — {V0['F3']}"
assert not V0["F4"].startswith("✅"), f"A: 교란이 없는데 F4 가 지지다 — {V0['F4']}"
print(f"  ✅ ⑪ null — F2 {V0['F2']} · F3 {V0['F3']} · F4 {V0['F4']} (아무것도 안 지어낸다)")

# ── ⑫ ★★ T 침입 — P 파는 완전히 같고 RR 만 다르다
# ★ 레코드마다 rr_s 를 바꿔 **T 침입 정도에 기울기**를 준다 — F4 는 개체 간 상관이라
#   전부 같은 조건이면 상관을 낼 게 없다(첫 시도에서 미결로 빠졌다)
TCONF = [(910 + i, dict(n_s=250, n_n=800, rr_s=115 + 8 * i, rr_n=265, rr_sd=38,
                        p_amp=0.0, t_amp=4.0)) for i in range(16)]
g1 = run_cohort("(B) ★★T 침입 — P 파는 S·N 이 완전히 같다 · RR 만 다르다", TCONF, seed=2)
V1, D1 = g1["VERD"], g1["DIFF"]
print(f"    매크로 P_early {mac(g1,'P_early'):.3f} · P_late {mac(g1,'P_late'):.3f}"
      f" · P_full {mac(g1,'P_full'):.3f} · T중첩격차 {np.nanmean(g1['A']['ov_gap_early']):+.3f}")
assert mac(g1, "P_early") > 0.65, \
    f"B: 시나리오가 교란을 못 만들었다 — P_early 가 {mac(g1,'P_early'):.3f}"
assert not V1["F2"].startswith("✅"), \
    (f"B: **P 파가 완전히 같은데 F2 가 지지다** — 관문이 교란을 못 잡는다. {V1['F2']} ({D1['F2']})")
assert V1["F4"].startswith("✅"), \
    f"B: 교란을 심었는데 F4 가 안 잡는다 — {V1['F4']} ({D1['F4']})"
print(f"  ✅ ⑫ T 침입 — F2 {V1['F2']}(신호가 early 에 있다) · F4 {V1['F4']}(교란 확인)")
print(f"     F1 {V1['F1']}  ← 정합 가능 개체 {int(g1['MOK'].sum())}/{len(g1['RS'])}")
print("     → **P 파가 한 톨도 안 다른데 P_full 이 잘 맞힌다.** 이게 우리가 두려워한 그림이다")

# ── ⑬ ★ 진짜 P — P 파가 다르고 RR 은 같다
REALP = [(920 + i, dict(n_s=150, n_n=600, rr_s=220, rr_n=220, p_amp=0.85, t_amp=0.0))
         for i in range(12)]
g2 = run_cohort("(C) ★진짜 P — P 파가 다르고 **RR 은 같다**", REALP, seed=3)
V2, D2 = g2["VERD"], g2["DIFF"]
print(f"    매크로 P_early {mac(g2,'P_early'):.3f} · P_late {mac(g2,'P_late'):.3f}"
      f" · P_full {mac(g2,'P_full'):.3f} · STT {mac(g2,'STT'):.3f}")
assert V2["F1"].startswith("✅"), f"C: RR 이 같은데 정합에서 무너졌다 — {V2['F1']} ({D2.get('F1')})"
assert V2["F2"].startswith("✅"), f"C: P 신호가 late 에 있는데 F2 가 안 잡는다 — {V2['F2']}"
assert V2["F3"].startswith("✅"), f"C: P 특이 신호인데 F3 가 안 잡는다 — {V2['F3']}"
assert not V2["F4"].startswith("✅"), f"C: 교란이 없는데 F4 가 지지다 — {V2['F4']}"
print(f"  ✅ ⑬ 진짜 P — F1 {V2['F1']} · F2 {V2['F2']} · F3 {V2['F3']} · F4 {V2['F4']}")
print("     → 관문 넷이 **진짜 신호를 죽이지 않는다**. 기각기 전용이 아니다")

# ── ⑭ 둘 다 — 정합해도 살아남아야
BOTH = [(930 + i, dict(n_s=250, n_n=800, rr_s=150, rr_n=210, rr_sd=40,
                       p_amp=0.85, t_amp=3.0)) for i in range(12)]
g3 = run_cohort("(D) 둘 다 — P 도 다르고 RR 도 다르다", BOTH, seed=4)
V3, D3 = g3["VERD"], g3["DIFF"]
print(f"    매크로 P_early {mac(g3,'P_early'):.3f} · P_late {mac(g3,'P_late'):.3f}"
      f" · 정합 가능 {int(g3['MOK'].sum())}/{len(g3['RS'])}")
assert V3["F2"].startswith("✅"), f"D: P 신호가 있는데 F2 가 안 잡는다 — {V3['F2']}"
if int(g3["MOK"].sum()) >= 6:
    assert V3["F1"].startswith("✅"), \
        f"D: 정합해도 P 신호는 남아야 한다 — {V3['F1']} ({D3.get('F1')})"
    print(f"  ✅ ⑭ 둘 다 — F1 {V3['F1']}(정합해도 살아남음) · F2 {V3['F2']}")
else:
    assert V3["F1"].startswith("⚠️"), f"D: 정합 불가인데 미결이 아니다 — {V3['F1']}"
    print(f"  ✅ ⑭ 둘 다 — 정합 가능 개체 부족 → F1 {V3['F1']} (조용히 판정하지 않는다) · F2 {V3['F2']}")

print("\n전부 통과 ✅ — Q7-F 는 심어 넣은 교란을 잡고, 진짜 신호는 죽이지 않는다")
sys.exit(0)
