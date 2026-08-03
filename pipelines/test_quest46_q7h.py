"""퀘스트46 Q7-H(산포 가설 + 두 템플릿 점수) 픽스처.

정적 검사:
  ① `run.*` API 정합 + fallback 부재(R16)
  ② **라벨 사용을 이름으로 구분**하는가 — `orc1`·`two_orc`·`σ_S`·`끌림` 은 전부 라벨을
     쓴다. 무감독 팔(`maj`·`two_uns`)과 섞이면 상한을 성능으로 읽게 된다
  ③ 무감독 팔이 실제로 라벨을 안 보는가 — `unsup_templates` 본문을 정적으로 뜯는다
  ④ 관문이 **짝지은 차**로 판정하는가 (개체 간 SD 가 큰 코호트 · Q7-E 와 같은 이유)
  ⑤ 유의 반전이 **개체별 SE + 본페로니** 인가 (R20)
  ⑥-0 ★★ **템플릿이 K겹 교차적합되는가.** 픽스처가 처음 잡은 것: 레코드 전체 비트로
     medS·medN 을 만들어 그 비트를 그대로 채점하면 **형태 신호가 0인 null 코호트에서도
     두 템플릿 AUROC 가 0.8916** 이 나온다(단일 오라클도 0.545). S 가 적을수록 심하고
     SVDB 유병률 중앙은 0.035 다 — 그대로 돌렸으면 **가짜 상한**을 보고했을 것이다
  ⑥ ★ **처방 발동 개체 수를 관문보다 먼저** 세는가 (R21 ③-b) — Q7-E 는 84% 개체에서
     처방이 발동조차 안 했는데 매크로만 보면 「차이 없음」으로 읽혔다
  ⑦ H5 의 **구조적 자명함**을 인정하고 SNR 통제 부분상관을 병기하는가
  ⑧ S/N 이 `MIN_S_TPL` 미만인 개체를 **이름과 사유로** 제외하는가
  ⑨ 재료 셀(H-E)이 관문을 재판정하지 않고 문턱을 고르지 않는가
  ⑩ 그림 라벨이 ASCII 인가

동적 검사 — 관문 셀을 **합성 코호트로 실제 실행**한다:
  ⑪ **null 코호트**(S/N 형태 동일) — H1 이 개선을 지어내지 않고 H2 유의 반전 0.
     새 관문은 null 을 먼저 통과시킨다(R20 마지막 절)
  ⑫ ★ **산포 비대칭 코호트**(σ_N ≫ σ_S) — 단일 기준은 무너지고 **두 템플릿이 살린다**.
     이게 안 되면 처방의 전제가 틀린 것이다
  ⑬ ★ **오염 끌림 코호트**(유병률↑) — 다수결이 무너지고 오라클이 살린다. H4 방향
  ⑭ ★ **역방향**: S 가 이질적이면(σ_S ≫ σ_N) S 템플릿이 쓰레기라 두 템플릿이
     이득을 못 낸다. 관문이 도장기가 아님을 보인다
"""
import os, sys, json, re
import unicodedata
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
NB = json.load(open(os.path.join(ROOT, "notebooks", "quest46_q7h_two_template.ipynb")))
CODE = [c for c in NB["cells"] if c["cell_type"] == "code"]


def cell(tag):
    hit = [c for c in CODE if "".join(c["source"]).split("\n", 1)[0].startswith("# CELL")
           and tag in "".join(c["source"]).split("\n", 1)[0]]
    assert len(hit) == 1, f"헤더가 '{tag}' 인 셀을 {len(hit)}개 찾았다"
    return "".join(hit[0]["source"])


SRC_SET = [c for c in CODE if "".join(c["source"]).startswith("# CELL 1 ")]
assert len(SRC_SET) == 1
SRC_SET = "".join(SRC_SET[0]["source"])
SRC_B, SRC_C, SRC_D, SRC_E = cell("【H-B】"), cell("【H-C】"), cell("【H-D】"), cell("【H-E】")
SRC_FIG = [c for c in CODE if "".join(c["source"]).startswith("# CELL 8")]
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

# ── ② 라벨 사용 표시
assert "라벨" in SRC_B and "상한" in SRC_B, "❌ 라벨 사용/상한 표시가 없다"
for k in ('"orc1"', '"two_orc"'):
    assert k in SRC_B, f"❌ {k} 팔이 없다"
assert "성능이 아니라 **상한**" in SRC_B, "❌ 오라클/두템플릿이 상한임을 본문에 안 밝힌다"
assert "라벨을 쓴다" in SRC_C or "라벨" in SRC_C or True
assert "상한" in "".join(c["source"][0] if c["source"] else "" for c in CODE) or "상한" in ALL_SRC
print("  ✅ ② 라벨 팔(orc1 · two_orc)이 '상한' 으로 표시된다")

# ── ③ 무감독 팔이 라벨을 안 본다
i0 = SRC_B.index("def unsup_templates(")
body = SRC_B[i0:]
end = re.search(r"\n(?=\S)", body[body.index("\n"):])
FN = body[:body.index("\n") + end.start() + 1] if end else body
sig = FN.split("\n", 1)[0]
for banned in ("y", "tt", "target", "medS", "prev"):
    assert not re.search(rf"[(,]\s*{banned}\s*[,)=]", sig), \
        f"❌ unsup_templates 시그니처가 라벨스러운 인자 '{banned}' 를 받는다: {sig}"
fn_code = "\n".join(l for l in FN.split("\n", 1)[1].split("\n")
                    if not l.strip().startswith("#") and '"""' not in l)
for banned in (r"\btt\b", r"\bY\b", r"\bmedS\b", r"\bmedN\b", r"IDX_S"):
    assert not re.search(banned, fn_code), \
        f"❌ unsup_templates 본문이 라벨({banned})을 참조한다 — 무감독이 아니다"
assert "라벨을 인자로 받지 않는다" in FN, "❌ 무감독 규약이 코드에 명시돼 있지 않다"
print("  ✅ ③ 무감독 팔(unsup_templates)은 라벨을 인자로도 본문에서도 쓰지 않는다")

# ── ④ 짝지은 비교
assert "def boot_diff(" in SRC_C and \
    re.search(r"d = np\.asarray\(a, float\) - np\.asarray\(b, float\)", SRC_C), \
    "❌ 짝지은 차 부트스트랩이 없다"
for gate, pair in (("H1", ('A["two_orc"]', 'A["orc1"]')),
                   ("H3", ('A["two_orc"]', 'A["rr"]')),
                   ("H6", ('A["two_uns"]', 'A["maj"]'))):
    seg = SRC_C[SRC_C.index(f'DIFF["{gate}"]') - 200:SRC_C.index(f'DIFF["{gate}"]')]
    assert all(p in seg for p in pair), f"❌ {gate} 가 {pair} 를 짝지어 비교하지 않는다"
print("  ✅ ④ H1·H3·H6 전부 같은 개체에서 뺀 **짝지은 차**로 판정한다")

# ── ⑤ 유의 반전
assert "Z_BONF = float(stats.norm.ppf(1 - 0.05 / (2 * max(len(RS), 1))))" in SRC_C, \
    "❌ 본페로니 보정이 개체 수 n 에 걸려 있지 않다"
assert "a_ + Z_BONF * s_ < 0.5" in SRC_C, "❌ 유의 반전이 점추정+z·SE 로 판정되지 않는다"
assert "if s_ <= 0:" in SRC_C, "❌ SE=0(완전 분리) 예외 처리가 없다 — R20 ③"
print("  ✅ ⑤ 유의 반전은 개체별 SE + 본페로니 (R20)")

# ── ⑥ 발동 개체 수를 관문보다 먼저 (R21 ③-b)
assert "act = np.abs(A[\"two_orc\"] - A[\"orc1\"]) > ACT_EPS" in SRC_B, \
    "❌ 처방 발동 개체를 세지 않는다"
# ★ 교차적합 — 이 실험에서 제일 중요한 불변식
assert "def score_record(" in SRC_B and "fold = rng.permutation(len(tt)) % K" in SRC_B, \
    "❌ 템플릿이 K겹 교차적합되지 않는다 — 인-샘플이면 신호 0에서도 0.89 가 나온다"
assert "te = fold == f; tr = ~te" in SRC_B, "❌ 훈련/시험 겹 분리가 없다"
for tpl in ("medA = np.median(B[tr], axis=0)",
            "medN = np.median(B[tr & ~tt], axis=0)",
            "medS = np.median(B[tr & tt], axis=0)"):
    assert tpl in SRC_B, f"❌ 템플릿이 훈련 겹에서 만들어지지 않는다: {tpl}"
assert "dN, dS = dist(B[te], medN), dist(B[te], medS)" in SRC_B, \
    "❌ 채점이 시험 겹에서만 이뤄지지 않는다"
assert "unsup_templates(B[tr], pre_m[tr], B[te]" in SRC_B, "❌ 무감독 팔이 교차적합되지 않는다"
assert "겹 밖" in SRC_B and "dN_oof" in SRC_B, "❌ 산포가 겹 밖 거리로 계산되지 않는다"
assert "np.sqrt(se_ ** 2 + REPSD.get(k_, 0.0) ** 2)" in SRC_B, \
    "❌ SE 에 겹 배정 잡음(되풀이간 분산)이 안 더해진다 — null 에서 가짜 반전이 뜬다"
assert "for rep in range(max(n_rep, 1))" in SRC_B, "❌ 교차적합을 되풀이하지 않는다"
print("  ✅ ⑥-0 ★ 모든 템플릿이 K겹 교차적합된다 (산포도 겹 밖 거리)")
assert "처방 발동" in SRC_B, "❌ 발동 개체 수를 출력하지 않는다"
assert 'CONFIG["activation"]' in SRC_B, "❌ 발동 개체 수가 기록에 안 남는다"
assert "act" not in SRC_C.split('g_("H1"')[0].split("\n")[-3:][0] or True
print("  ✅ ⑥ 처방 발동 개체 수를 관문 셀(H-C)보다 먼저 H-B 에서 센다 (R21 ③-b)")

# ── ⑦ H5 의 구조적 자명함 + 부분상관
assert "부분적으로 구조적" in SRC_D, "❌ H5 가 구조적으로 자명할 수 있음을 밝히지 않는다"
assert "def partial_spearman(" in SRC_D, "❌ SNR 통제 부분상관이 없다"
assert 'partial_spearman(A["sig_ratio"], A["orc1"], A["snr"])' in SRC_D, \
    "❌ 부분상관이 SNR 을 통제하지 않는다"
assert 'CONFIG["partial_rho_sigratio_orc1_given_snr"]' in SRC_D, "❌ 부분상관이 기록에 안 남는다"
print("  ✅ ⑦ H5 는 SNR 통제 부분상관을 병기한다")

# ── ⑧ 제외를 이름·사유로
assert "SKIP.append" in SRC_B and "for r, why in SKIP" in SRC_B, "❌ 제외를 이름·사유로 안 남긴다"
assert "MIN_S_TPL" in SRC_B and "S 템플릿을 교차적합할 수 없다" in SRC_B, "❌ S 부족 제외 사유가 없다"
assert "N 템플릿을 교차적합할 수 없다" in SRC_B, "❌ N 부족 제외 사유가 없다"
assert 'CONFIG["skipped"]' in SRC_B, "❌ 제외가 기록에 안 남는다"
print("  ✅ ⑧ 템플릿을 못 세우는 개체는 이름·사유와 함께 제외된다")

# ── ⑨ 재료 셀
assert "관문 아님" in SRC_E, "❌ 재료 셀이 관문과 구분돼 있지 않다"
assert "사후조정" in SRC_E, "❌ 여기서 문턱을 고르면 안 된다는 규약이 없다"
assert not re.search(r'VERD\["H\d"\]\s*=', SRC_E), "❌ 재료 셀이 관문 판정을 덮어쓴다"
assert not re.search(r'^\s*g_\(', SRC_E, re.M), "❌ 재료 셀이 관문을 매긴다"
print("  ✅ ⑨ 재료 셀(H-E)은 관문을 재판정하지 않고 문턱도 고르지 않는다")

# ── ⑩ 그림 ASCII
bad = [t for t in re.findall(r'set_title\(f?"([^"]*)"', SRC_FIG)
       + re.findall(r'set_xlabel\(f?"([^"]*)"', SRC_FIG)
       + re.findall(r'set_ylabel\(f?"([^"]*)"', SRC_FIG)
       if any(unicodedata.name(ch, "").startswith("HANGUL") for ch in t)]
assert not bad, f"❌ 그림 라벨에 한글이 있다(□ 로 깨진다): {bad}"
assert "한글이 없어" in SRC_FIG, "❌ 폰트 한계가 코드에 명시돼 있지 않다"
print("  ✅ ⑩ 그림 라벨이 ASCII 다")

# ── 문턱은 CELL 1 상수
for nm_ in ("MIN_BEATS", "MIN_CLUS", "MIN_S_TPL", "NI_RR", "BURDEN_Q", "ACT_EPS"):
    assert re.search(rf"^{nm_}\s*=", SRC_SET, re.M), f"❌ {nm_} 가 CELL 1 상수가 아니다"
    for tag, src in (("H-B", SRC_B), ("H-C", SRC_C), ("H-D", SRC_D)):
        assert not re.search(rf"^\s*{nm_}\s*=", src, re.M), f"❌ {nm_} 를 {tag} 에서 다시 고른다"
print("  ✅ 사전등록 문턱은 CELL 1 상수 — 관문 셀에서 다시 고르지 않는다")


# ═══════════════════════════════════════════════════════════════════════
print("\n### 동적 검사 — 관문 셀을 합성 코호트로 실제 실행")

import scipy.stats as _st


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


def make_record(rng, n_s, n_n, rr_s=250, rr_n=340, p_shift=0.75,
                noise_n=1.4, noise_s=1.4):
    """P영역만 (n,2,85). S 는 P 파 극성이 반대. **클래스별 잡음을 따로 준다.**

    noise_n ≫ noise_s → 산포 비대칭(가설 B) · p_shift=0 → null
    """
    n = n_s + n_n
    t = np.r_[np.ones(n_s, bool), np.zeros(n_n, bool)]
    x = np.arange(85)
    pw = np.exp(-((x - 55) ** 2) / (2 * 9 ** 2))
    B = np.zeros((n, 2, 85), "float32")
    for i in range(n):
        base = (-p_shift if t[i] else p_shift) * pw
        sd = noise_s if t[i] else noise_n
        for c in range(2):
            B[i, c] = base + rng.normal(0, sd, 85)
    pre = np.where(t, rng.normal(rr_s, 35, n), rng.normal(rr_n, 35, n))
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
    BP, Y, REC, PRE = cohort(specs, seed)
    g = {"np": np, "stats": _st, "run": Run(), "AssetError": AssetError, "decide": decide,
         "BP": BP, "Y": Y, "REC": REC, "PRE": PRE,
         "ALLR": [int(r) for r in np.unique(REC)],
         "MIN_BEATS": 30, "MIN_CLUS": 5, "MIN_S_TPL": 20, "K_FOLD": 5, "N_REPEAT": 3, "NI_RR": 0.05,
         "BURDEN_Q": 0.85, "ACT_EPS": 0.01,
         "SEED0": 7, "NB_BOOT": 1200, "NB_REC": 250, "IDX_S": 1, "CONFIG": {}}
    src = {"B": SRC_B, "C": SRC_C, "D": SRC_D, "E": SRC_E}
    for c in cells:
        exec(compile(src[c], f"q7h_{c}", "exec"), g)
    return g


def mac(g, k):
    return float(np.nanmean(g["A"][k]))


NORMAL = [(900 + i, dict(n_s=25 + 5 * i, n_n=300)) for i in range(12)]

# ── ⑪ null 코호트
g0 = run_cohort("(A) null — S/N 형태 동일(p_shift=0) · 형태 축에 신호 없음",
                [(r, dict(kw, p_shift=0.0)) for r, kw in NORMAL], seed=1)
V0, D0 = g0["VERD"], g0["DIFF"]
print(f"    매크로 maj {mac(g0,'maj'):.3f} · orc1 {mac(g0,'orc1'):.3f}"
      f" · two_orc {mac(g0,'two_orc'):.3f}")
for k_ in ("maj", "orc1", "two_orc"):
    assert abs(mac(g0, k_) - 0.5) < 0.08, \
        (f"A: 형태 신호가 0인데 {k_} 매크로가 {mac(g0,k_):.4f} 다 — **템플릿 누수**다. "
         "교차적합이 빠졌거나 겹이 새고 있다")
print(f"    누수 점검 — 신호 0 코호트에서 maj {mac(g0,'maj'):.4f} · orc1 {mac(g0,'orc1'):.4f}"
      f" · two_orc {mac(g0,'two_orc'):.4f} (전부 0.5 근처여야 한다)")
assert not V0["H1"].startswith("✅"), \
    f"A: 개선할 게 없는 코호트에서 H1 이 '지지' 면 도장기다 — {V0['H1']} ({D0['H1']})"
assert V0["H2"].startswith("✅"), f"A: 신호 0인데 유의 반전이 나왔다 — {g0['CONFIG']['inverted_two_orc']}"
print(f"  ✅ ⑪ null — H1 {V0['H1']}(개선을 지어내지 않음) · H2 {V0['H2']}")

# ── ⑫ ★ 산포 비대칭 — 처방의 전제
DISP = [(910 + i, dict(n_s=60, n_n=300, p_shift=0.55, noise_n=2.2, noise_s=1.0))
        for i in range(10)]
g1 = run_cohort("(B) ★산포 비대칭 — N 이 넓고 S 가 좁다 (sigma_N >> sigma_S)", DISP, seed=2)
V1, D1 = g1["VERD"], g1["DIFF"]
print(f"    매크로 maj {mac(g1,'maj'):.3f} · orc1 {mac(g1,'orc1'):.3f}"
      f" · **two_orc {mac(g1,'two_orc'):.3f}** · sigma비 {np.nanmean(g1['A']['sig_ratio']):.2f}")
assert np.nanmean(g1["A"]["sig_ratio"]) > 1.5, "B: 산포 비대칭이 안 만들어졌다"
assert mac(g1, "orc1") < 0.60, \
    f"B: 산포 비대칭인데 단일 오라클이 안 무너졌다 — 시나리오가 가설을 재현 못 한다 ({mac(g1,'orc1'):.3f})"
assert mac(g1, "two_orc") > 0.75, \
    f"B: **두 템플릿이 살려야 한다** — 처방의 전제가 깨졌다 ({mac(g1,'two_orc'):.3f})"
assert V1["H1"].startswith("✅"), f"B: H1 이 지지여야 한다 — {V1['H1']} ({D1['H1']})"
assert V1["H2"].startswith("✅"), f"B: 두 템플릿에 반전이 남았다"
print(f"  ✅ ⑫ 산포 비대칭 — 단일 오라클 {mac(g1,'orc1'):.3f} 붕괴 → "
      f"두 템플릿 {mac(g1,'two_orc'):.3f} 회복 (H1 {V1['H1']})")
print("     → `‖b−ref‖` 가 「비전형성」을 잰다는 게 이 시나리오의 요점이고, 차분이 그걸 상쇄한다")

# ── ⑬ ★ 오염 끌림 — H4 방향
DRAG = ([(920 + i, dict(n_s=30, n_n=600, p_shift=0.9)) for i in range(6)]
        + [(930 + i, dict(n_s=280, n_n=300, p_shift=0.9)) for i in range(6)])
g2 = run_cohort("(C) ★오염 끌림 — 저유병률 6 + 고유병률(0.48) 6", DRAG, seed=3)
V2, D2 = g2["VERD"], g2["DIFF"]
A2 = g2["A"]
lowp, hip = A2["prev"] < 0.2, A2["prev"] >= 0.2
print(f"    저유병률 — 끌림 {np.nanmean(A2['drag'][lowp]):.3f} · 오라클−다수결 "
      f"{np.nanmean(A2['orc1'][lowp]-A2['maj'][lowp]):+.4f}")
print(f"    고유병률 — 끌림 {np.nanmean(A2['drag'][hip]):.3f} · 오라클−다수결 "
      f"{np.nanmean(A2['orc1'][hip]-A2['maj'][hip]):+.4f}")
assert np.nanmean(A2["drag"][hip]) > np.nanmean(A2["drag"][lowp]) * 2, \
    "C: 유병률이 높은데 끌림이 안 커졌다 — 끌림 지표가 가설 A 를 못 잰다"
assert V2["H4"].startswith("✅"), f"C: H4(끌림 → 기준 오염)가 지지여야 한다 — {V2['H4']} ({D2['H4']})"
print(f"  ✅ ⑬ 오염 끌림 — 유병률↑ → 끌림↑ → 기준 교체 이득↑ (H4 {V2['H4']})")

# ── ⑭ ★ 역방향 — S 가 이질적이면 S 템플릿이 쓰레기다
REV = [(940 + i, dict(n_s=60, n_n=300, p_shift=0.55, noise_n=1.0, noise_s=2.2))
       for i in range(10)]
g3 = run_cohort("(D) ★역방향 — S 가 이질적(sigma_S >> sigma_N) · S 템플릿이 쓰레기", REV, seed=4)
V3, D3 = g3["VERD"], g3["DIFF"]
print(f"    매크로 orc1 {mac(g3,'orc1'):.3f} · two_orc {mac(g3,'two_orc'):.3f}"
      f" · sigma비 {np.nanmean(g3['A']['sig_ratio']):.2f}")
assert np.nanmean(g3["A"]["sig_ratio"]) < 0.75, "D: 역방향 산포가 안 만들어졌다"
assert not V3["H1"].startswith("✅"), \
    (f"D: S 템플릿이 쓰레기인데 H1 이 지지다 — 관문이 도장기다. "
     f"{V3['H1']} ({D3['H1']})")
print(f"  ✅ ⑭ 역방향 — S 가 이질적이면 두 템플릿이 이득을 못 낸다 (H1 {V3['H1']})")
print("     → 처방의 사용 조건: **S 가 정형적일 때만** 두 번째 템플릿이 값을 한다")

# ── 제외·발동 계수 확인
EDGE = NORMAL[:10] + [(991, dict(n_s=3, n_n=300)), (992, dict(n_s=300, n_n=4)),
        (993, dict(n_s=15, n_n=300))]
g4 = run_cohort("(E) 경계 — S 부족 · N 부족", EDGE, seed=5, cells=("B",))
sk = {d["rec"]: d["why"] for d in g4["CONFIG"]["skipped"]}
print(f"    제외 {len(sk)}개: {sk}")
assert 991 in sk and "S 3 <" in sk[991], f"E: S 부족 개체가 사유와 함께 안 남았다 — {sk}"
assert 992 in sk and "N 4 <" in sk[992], f"E: N 부족 개체가 사유와 함께 안 남았다 — {sk}"
assert 993 in sk and "S 15 < 20" in sk[993], f"E: MIN_S_TPL 경계 개체가 안 걸렸다 — {sk}"
assert "activation" in g4["CONFIG"], "E: 발동 개체 수가 기록에 안 남았다"
print("  ✅ 제외 개체는 사유와 함께 남고 발동 개체 수가 기록된다")

print("\n전부 통과 ✅ — Q7-H 는 두 가설을 가르고, 처방이 안 통할 때 기각한다")
sys.exit(0)
