"""퀘스트46 Q7-E(긴RR 앵커 전수 적용) 픽스처.

정적 검사:
  ① `run.*` API 정합 + fallback 부재(R16)
  ② **앵커가 라벨을 안 본다** — `anchor_split` 은 정답을 인자로도 안 받고 본문에서도
     안 쓴다. 이게 깨지면 '무감독 앵커' 주장 전체가 무너진다. 함수 본문을 정적으로 뜯는다
  ③ 관문이 **짝지은 차**로 판정하는가 — 개체 간 SD 0.157 짜리 코호트에서 비짝지은
     비교는 검정력을 버린다. 매크로 두 개를 따로 내서 눈으로 비교하면 안 된다
  ④ 오라클은 **상한**으로만 쓰이는가 — E1·E2·E3 이 oracle 로 판정하면 안 된다
  ⑤ 제외 개체를 **이름과 사유로** 남기는가 (조용히 빼면 매크로가 좋아 보인다 — R16·R17)
  ⑥ ★ E2 반전 판정이 **개체별 SE + 본페로니** 인가. — 픽스처가 두 번 잡았다:
     (1) 「점추정 < 0.5 & 정보량 ≥ INFO_MIN」 → **null 코호트**(S/N 형태 동일)에서
         S 16비트짜리 개체가 우연히 0.344 로 찍혀 '반전' 에 잡혔다. 신호가 0인데도.
     (2) 개별 95% CI 상한 < 0.5 로 바꿔도 **같은 개체가 또 걸렸다**(상한 0.491).
         개체마다 검정하니 14개면 ~0.35개가 우연히 걸리는 게 정상이다.
     → 최종은 **본페로니 보정 z·SE**. 점추정 문턱은 표본수도 검정 횟수도 모른다
  ⑦ 문턱이 CELL 1 상수이고 관문 셀에서 숫자를 다시 안 고르는가
  ⑧ 사후 탐색이 **관문과 분리·표기**돼 있고 관문을 재판정하지 않는가
  ⑨ 그림 라벨이 ASCII 인가 (Colab 기본 폰트에 한글 없음)

동적 검사 — 관문 셀을 **합성 코호트로 실제 실행**한다:
  ⑩ 정상 코호트 — 앵커가 **개선을 지어내지 않는다**(E1 미결/기각) · 정상 비열등(E3 지지)
  ⑪ 반전 섞인 코호트 — E1 지지 · E2 반전 0 · E3 비열등
  ⑫ ★ **역방향 검정: 늦은 이소성(이탈박동) 코호트**. 앵커의 유일한 가정
     「이소성은 이르다」가 깨지면 앵커는 **S 군을 기저로 고른다**. 관문이 이걸 잡는가.
     못 잡으면 E2 는 도장기지 관문이 아니다
  ⑬ 제외 사유가 실제로 이름과 함께 남는가 (비트 부족 · S 부족)
"""
import os, sys, json, re
import unicodedata
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
NB = json.load(open(os.path.join(ROOT, "notebooks", "quest46_q7e_anchor_sweep.ipynb")))
CODE = [c for c in NB["cells"] if c["cell_type"] == "code"]


def cell(tag):
    hit = [c for c in CODE if "".join(c["source"]).split("\n", 1)[0].startswith("# CELL")
           and tag in "".join(c["source"]).split("\n", 1)[0]]
    assert len(hit) == 1, f"헤더가 '{tag}' 인 셀을 {len(hit)}개 찾았다"
    return "".join(hit[0]["source"])


SRC_SET = [c for c in CODE if "".join(c["source"]).startswith("# CELL 1 ")]
assert len(SRC_SET) == 1
SRC_SET = "".join(SRC_SET[0]["source"])
SRC_G0, SRC_A = cell("【G0】"), cell("【E-A】")
SRC_B, SRC_C, SRC_D = cell("【E-B】"), cell("【E-C】"), cell("【E-D】")
SRC_FIG = [c for c in CODE if "".join(c["source"]).startswith("# CELL 7")]
assert len(SRC_FIG) == 1
SRC_FIG = "".join(SRC_FIG[0]["source"])
ALL_SRC = "".join("".join(c["source"]) for c in CODE)

print("### 정적 검사")

# ── ① API · fallback
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

# ── ② 앵커가 라벨을 안 본다 (이 실험의 핵심 불변식)
i0 = SRC_B.index("def anchor_split(")
body = SRC_B[i0:]
end = re.search(r"\n(?=\S)", body[body.index("\n"):])
FN = body[:body.index("\n") + end.start() + 1] if end else body
sig = FN.split("\n", 1)[0]
for banned in ("y", "tt", "t", "lab_true", "target", "oracle", "prev"):
    assert not re.search(rf"[(,]\s*{banned}\s*[,)=]", sig), \
        f"❌ anchor_split 시그니처가 라벨스러운 인자 '{banned}' 를 받는다: {sig}"
fn_body = FN.split("\n", 1)[1]
fn_code = "\n".join(l for l in fn_body.split("\n")
                    if not l.strip().startswith("#") and '"""' not in l)
for banned in (r"\btt\b", r"\bY\b", r"\boracle\b", r"IDX_S", r"\bPER\b"):
    assert not re.search(banned, fn_code), \
        f"❌ anchor_split 본문이 라벨({banned})을 참조한다 — 무감독이 아니다"
assert "라벨을 인자로 받지 않는다" in FN, "❌ 무감독 규약이 코드에 명시돼 있지 않다"
assert "리듬 지식" in FN, "❌ 앵커가 쓰는 사전지식의 성격(리듬)이 명시돼 있지 않다"
print("  ✅ ② 앵커(anchor_split)는 라벨을 인자로도 본문에서도 쓰지 않는다")

# 앵커 선택은 **개수가 아니라 RR** 로 한다
assert re.search(r"longrr = 0 if m0 > m1 else 1", SRC_B), "❌ 긴RR 앵커 선택 규칙이 없다"
assert re.search(r"big = 0 if n0 >= n1 else 1", SRC_B), "❌ 다수 앵커(대조)가 없다"
print("  ✅ ② 앵커는 개수(big)가 아니라 중앙 RR(longrr)로 고른다 — 대조군도 함께 잰다")

# ── ③ 짝지은 비교
assert "def boot_diff(" in SRC_C, "❌ 짝지은 차 부트스트랩이 없다"
assert re.search(r"d = np\.asarray\(a, float\) - np\.asarray\(b, float\)", SRC_C), \
    "❌ boot_diff 가 짝지은 차를 만들지 않는다"
for gate, pair in (("E1", ('A["anchor"]', 'A["maj"]')),
                   ("E4", ('A["oracle"][om]', 'A["anchor"][om]')),
                   ("E5", ('A["anchor"]', 'A["rr"]'))):
    seg = SRC_C[SRC_C.index(f'DIFF["{gate}"]') - 260:SRC_C.index(f'DIFF["{gate}"]')]
    assert all(p in seg for p in pair), f"❌ {gate} 가 {pair} 를 짝지어 비교하지 않는다"
assert 'boot_diff(A["anchor"][nm], A["maj"][nm]' in SRC_C, "❌ E3 이 정상 개체 부분집합에서 짝지어지지 않는다"
print("  ✅ ③ E1·E3·E4·E5 전부 같은 개체에서 뺀 **짝지은 차**로 판정한다")

# ── ④ 오라클은 상한으로만
for gate in ("E1", "E2", "E3"):
    j = SRC_C.index(f'g_("{gate}"')
    seg = SRC_C[j:j + 420]
    assert "oracle" not in seg, f"❌ {gate} 판정에 oracle(라벨) 이 끼어 있다 — 상한을 성능으로 쓴다"
assert "라벨 사용" in SRC_B or "라벨=상한" in SRC_B, "❌ 오라클이 라벨 사용임을 표시하지 않는다"
print("  ✅ ④ 오라클은 E4(상한 거리)에만 쓰이고 성립 조건 관문에는 안 들어간다")

# ── ⑤ 제외 개체를 이름과 사유로
assert "SKIP.append" in SRC_B and "for r, why in SKIP" in SRC_B, \
    "❌ 제외 개체를 이름·사유로 출력하지 않는다"
assert 'CONFIG["skipped"]' in SRC_B, "❌ 제외가 기록에 안 남는다"
assert "조용히 빼지 않는다" in SRC_B, "❌ 제외 규약이 코드에 명시돼 있지 않다"
print("  ✅ ⑤ 제외 개체는 이름·사유와 함께 출력·기록된다")

# ── ⑥ E2 는 개체별 CI 로 판정한다 (점추정 고정 문턱 금지)
assert "def sig_inv(" in SRC_C, "❌ 유의 반전 판정 함수가 없다"
j = SRC_C.index("def sig_inv(")
seg = SRC_C[j:j + 260]
assert "a_ + Z_BONF * s_ < 0.5" in seg, \
    "❌ 유의 반전이 (점추정 + 본페로니 z·SE < 0.5) 로 판정되지 않는다"
assert "Z_BONF = float(stats.norm.ppf(1 - 0.05 / (2 * max(len(RS), 1))))" in SRC_C, \
    "❌ 본페로니 보정이 개체 수 n 에 걸려 있지 않다"
assert "inv_anc = [r for r in RS if sig_inv(r, \"anchor\")]" in SRC_C,     "❌ E2 가 유의 반전 목록을 쓰지 않는다"
k = SRC_C.index('g_("E2"')
assert "inv_anc" in SRC_C[k:k + 400] and "pt_anc" not in SRC_C[k:k + 400],     "❌ E2 관문이 점추정 반전(pt_anc)으로 판정한다"
assert "pt_anc" in SRC_C and "관문에 쓰지 않는다" in SRC_C,     "❌ 점추정 반전을 병기·구분하지 않는다"
assert "_lo" in SRC_B and "boot_auroc" in SRC_B, "❌ E-B 가 개체별 CI 를 안 낸다"
assert "inv_maj" in SRC_C, "❌ 다수결 기준 반전 개체 수를 병기하지 않는다(개선폭을 못 읽는다)"
print("  ✅ ⑥ E2 는 **개체별 SE + 본페로니 보정**으로 반전을 센다 (점추정은 병기만)")

# ── ⑦ 문턱은 CELL 1 상수
for nm_ in ("MIN_BEATS", "MIN_CLUS", "INFO_MIN", "NI_NORMAL", "ORACLE_MAX", "NI_RR", "GMIN"):
    assert re.search(rf"^{nm_}\s*=", SRC_SET, re.M), f"❌ {nm_} 가 CELL 1 상수가 아니다"
    assert not re.search(rf"^\s*{nm_}\s*=", SRC_B, re.M), f"❌ {nm_} 를 E-B 에서 다시 고른다"
    assert not re.search(rf"^\s*{nm_}\s*=", SRC_C, re.M), f"❌ {nm_} 를 E-C 에서 다시 고른다"
assert "GMIN    = 2" in SRC_SET and "Q7-B 승계" in SRC_SET, "❌ GMIN 승계 표시가 없다"
print("  ✅ ⑦ 사전등록 문턱은 CELL 1 상수 — 관문 셀에서 다시 고르지 않는다")

# ── ⑧ 사후 탐색 분리
assert "관문 아님" in SRC_D, "❌ 사후 탐색이 관문과 구분돼 있지 않다"
assert "관문을 다시 매기지 않는다" in SRC_D or "관문 재판정 금지" in SRC_D, \
    "❌ 사후 조건으로 관문을 다시 매기지 않는다는 규약이 없다"
assert not re.search(r'VERD\["E\d[b]?"\]\s*=', SRC_D), "❌ 사후 셀이 관문 판정을 덮어쓴다"
print("  ✅ ⑧ 사후 탐색(E-D)은 관문을 재판정하지 않는다")

# ── ⑨ 그림 ASCII
bad = [t for t in re.findall(r'set_title\(f?"([^"]*)"', SRC_FIG)
       + re.findall(r'set_xlabel\(f?"([^"]*)"', SRC_FIG)
       + re.findall(r'set_ylabel\(f?"([^"]*)"', SRC_FIG)
       if any(unicodedata.name(ch, "").startswith("HANGUL") for ch in t)]
assert not bad, f"❌ 그림 라벨에 한글이 있다(□ 로 깨진다): {bad}"
assert "한글이 없어" in SRC_FIG, "❌ 폰트 한계가 코드에 명시돼 있지 않다"
print("  ✅ ⑨ 그림 라벨이 ASCII 다")


# ═══════════════════════════════════════════════════════════════════════
print("\n### 동적 검사 — 관문 셀을 합성 코호트로 실제 실행")


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


def make_record(rng, n_s, n_n, rr_s, rr_n, p_shift=0.75, noise=1.4):
    """비트 (n,2,300). S 는 **P 영역 극성이 반대**. RR 은 인자로 준다.

    rr_s < rr_n → 이른 이소성(정상 가정) · rr_s > rr_n → **늦은 이소성(이탈박동)**
    ★ 기본 잡음은 **AUROC 가 0.85~0.93 에 앉도록** 맞췄다. 완전 분리(1.0000)면
      관문·CI 가 전부 퇴화해서 무엇을 검사했는지 알 수 없다(R14-b: 경계에 붙은 단위 포함).
    p_shift=0 → **S 와 N 의 형태가 같다 = null 코호트**
    """
    n = n_s + n_n
    t = np.r_[np.ones(n_s, bool), np.zeros(n_n, bool)]
    x = np.arange(300)
    qrs = np.exp(-((x - 100) ** 2) / (2 * 6 ** 2)) * 5.0
    pw = np.exp(-((x - 55) ** 2) / (2 * 9 ** 2))
    B = np.zeros((n, 2, 300), "float32")
    for i in range(n):
        base = qrs + (-p_shift if t[i] else p_shift) * pw
        for c in range(2):
            B[i, c] = base + rng.normal(0, noise, 300)
    pre = np.where(t, rng.normal(rr_s, 35, n), rng.normal(rr_n, 35, n))
    return B, t, pre.astype(float)


def cohort(specs, seed, p_shift=0.75):
    """specs: [(rec, n_s, n_n, rr_s, rr_n)] → BEAT, Y, REC, PRE"""
    rng = np.random.RandomState(seed)
    Bs, Ys, Rs, Ps = [], [], [], []
    for rec, n_s, n_n, rr_s, rr_n in specs:
        B, t, pre = make_record(rng, n_s, n_n, rr_s, rr_n, p_shift=p_shift)
        Bs.append(B); Ys.append(np.where(t, 1, 0)); Ps.append(pre)
        Rs.append(np.full(len(t), rec, np.int64))
    return (np.concatenate(Bs), np.concatenate(Ys),
            np.concatenate(Rs), np.concatenate(Ps))


def run_cohort(tag, specs, seed=0, p_shift=0.75):
    print("\n" + "=" * 78); print(f"### {tag}"); print("=" * 78)
    BEAT, Y, REC, PRE = cohort(specs, seed, p_shift=p_shift)
    g = {"np": np, "stats": __import__("scipy.stats", fromlist=["stats"]),
         "run": Run(), "AssetError": AssetError, "decide": decide,
         "BEAT": BEAT, "Y": Y, "REC": REC, "PRE": PRE,
         "ALLR": [int(r) for r in np.unique(REC)],
         "MIN_BEATS": 30, "MIN_CLUS": 5, "GMIN": 2, "INFO_MIN": 0.60,
         "NI_NORMAL": 0.02, "ORACLE_MAX": 0.05, "NI_RR": 0.05,
         "SEED0": 7, "NB_BOOT": 1500, "NB_REC": 300, "IDX_S": 1,
         "P_SEG": (0, 85), "QRS_SEG": (85, 130), "FULL_SEG": (0, 300),
         "CONFIG": {}}
    exec(compile(SRC_B, "q7e_b", "exec"), g)
    exec(compile(SRC_C, "q7e_c", "exec"), g)
    exec(compile(SRC_D, "q7e_d", "exec"), g)
    return g


NORMAL = [(900 + i, 12 + 4 * i, 300, 250, 340) for i in range(14)]


def macros(g):
    A = g["A"]
    return {k: float(np.nanmean(A[k])) for k in ("rr", "maj", "big", "anchor", "oracle")}


# ── ⑩ null 코호트 — S 와 N 의 형태가 **같다**. 개선할 게 없다
g0 = run_cohort("(A) null 코호트 — S/N 형태 동일(p_shift=0) · 형태 축에 신호가 없다",
                NORMAL, seed=1, p_shift=0.0)
V0, D0, M0 = g0["VERD"], g0["DIFF"], macros(g0)
print(f"    매크로 {(', '.join(f'{k} {v:.3f}' for k, v in M0.items()))}")
assert abs(M0["maj"] - 0.5) < 0.06 and abs(M0["anchor"] - 0.5) < 0.06, \
    f"A: 형태 신호가 없는데 형태 축이 0.5 가 아니다 — 지표가 샌다: {M0}"
assert not V0["E1"].startswith("✅"), \
    f"A: 개선할 게 없는 코호트에서 E1 이 '지지' 면 도장기다 — {V0['E1']} ({D0['E1']})"
I0 = g0["CONFIG"]["inverted"]
print(f"    유의 반전 {I0['anchor']} · 점추정만 반전 {I0['point_anchor']}")
assert V0["E2"].startswith("✅"), \
    f"A: 신호 0인 코호트에서 유의 반전이 나오면 안 된다 — {I0}"
assert I0["point_anchor"], \
    ("A: 점추정 반전이 하나도 안 나오면 이 시나리오가 문제를 재현 못 한 것이다 — "
     "CI 판정의 필요성을 보여주는 게 이 검사의 목적이다")
print(f"  ✅ ⑩ null 코호트 — E1 {V0['E1']}(개선을 지어내지 않음) · E2 {V0['E2']}"
      f" (점추정이었으면 {len(I0['point_anchor'])}개 오발 → **CI 판정이 걸러냈다**)")

# ── ⑩-b 정상 코호트 — 신호는 있고 유병률은 낮다. 앵커가 정상을 깎으면 안 된다
g1 = run_cohort("(B) 정상 코호트 14개체 (유병률 0.04~0.18 · 이른 S · 부분 분리)",
                NORMAL, seed=1)
V1, D1, M1 = g1["VERD"], g1["DIFF"], macros(g1)
print(f"    매크로 {(', '.join(f'{k} {v:.3f}' for k, v in M1.items()))}")
assert 0.6 < M1["maj"] < 0.999, f"B: 다수결 축이 퇴화했다(완전 분리/무신호) — {M1}"
assert V1["E2"].startswith("✅"), f"B: 정상 코호트에서 앵커 반전이 나오면 안 된다 — {V1['E2']}"
assert V1["E3"].startswith("✅"), f"B: 정상 개체 비열등이 깨졌다 — {V1['E3']} ({D1['E3']})"
print(f"  ✅ ⑩-b 정상 코호트 — E2 반전 0 · E3 비열등({D1['E3']['mean']:+.4f})")

# ── ⑪ 반전 섞인 코호트
MIX = NORMAL[:8] + [(950 + i, 320, 200, 250, 340) for i in range(6)]   # 유병률 0.615 × 6
g2 = run_cohort("(C) 반전 6개체 섞인 코호트 (유병률 0.615 · S 가 다수)", MIX, seed=2)
V2, D2, M2 = g2["VERD"], g2["DIFF"], macros(g2)
inv = g2["CONFIG"]["inverted"]
print(f"    매크로 {(', '.join(f'{k} {v:.3f}' for k, v in M2.items()))}")
print(f"    다수결 반전 {len(inv['maj'])}개 → 앵커 반전 {len(inv['anchor'])}개")
assert len(inv["maj"]) >= 5, f"C: 다수가 S 인데 다수결 기준이 안 뒤집혔다 — {inv['maj']}"
assert V2["E1"].startswith("✅"), f"C: 개선이 검출돼야 한다 — {V2['E1']} ({D2['E1']})"
assert V2["E2"].startswith("✅"), f"C: 앵커가 반전을 남겼다 — {inv['anchor']}"
assert V2["E3"].startswith("✅"), f"C: 정상 개체를 깎았다 — {V2['E3']} ({D2['E3']})"
print(f"  ✅ ⑪ 반전 코호트 — E1 지지({D2['E1']['mean']:+.4f}) · E2 반전 0 · E3 비열등")

# ── ⑫ ★ 역방향 검정 — 늦은 이소성(이탈박동). 앵커의 가정이 깨진다
LATE = NORMAL[:8] + [(970 + i, 60, 340, 430, 330) for i in range(6)]   # S 가 **늦다**
g3 = run_cohort("(D) ★역방향 — 늦은 이소성(이탈박동) 6개체 · rr_S > rr_N", LATE, seed=3)
V3, D3 = g3["VERD"], g3["DIFF"]
inv3 = g3["CONFIG"]["inverted"]
ph3 = g3["CONFIG"]["posthoc"]["anchor_picked_s_cluster"]
print(f"    다수결 반전 {len(inv3['maj'])}개 · **앵커 반전 {len(inv3['anchor'])}개** {inv3['anchor']}")
print(f"    앵커가 S 우세 군을 기저로 고른 개체: {ph3}")
assert len(inv3["anchor"]) >= 5, (
    "D: 늦은 이소성인데 앵커가 안 뒤집혔다 — 관문이 못 잡으면 E2 는 도장기다. "
    f"{inv3['anchor']}")
assert V3["E2"].startswith("❌"), f"D: E2 가 기각해야 한다 — {V3['E2']}"
assert not V3["E1"].startswith("✅"), f"D: 앵커가 해로운데 개선으로 읽혔다 — {V3['E1']} ({D3['E1']})"
assert len(ph3) >= 5, f"D: 사후 셀이 '앵커가 S 군을 골랐다' 를 못 짚었다 — {ph3}"
print(f"  ✅ ⑫ 역방향 검정 — 「이소성은 이르다」가 깨지면 E2 가 기각하고 사후 셀이 원인을 짚는다 "
      f"(E1 {V3['E1']} · E2 {V3['E2']})")
print("     → 앵커는 **리듬 사전지식**이다. 형태 지식이 아니다. 이 가정이 처방의 사용 조건이다")

# ── ⑬ 제외 사유가 이름과 함께
EDGE = NORMAL[:6] + [(991, 3, 17, 250, 340),      # 비트 20 < 30
                     (992, 1, 300, 250, 340)]     # S 1 < GMIN 2
g4 = run_cohort("(E) 경계 개체 — 비트 부족 · S 부족", EDGE, seed=4)
sk = {d["rec"]: d["why"] for d in g4["CONFIG"]["skipped"]}
print(f"    제외 {len(sk)}개: {sk}")
assert 991 in sk and "비트" in sk[991], f"E: 비트 부족 개체가 사유와 함께 안 남았다 — {sk}"
assert 992 in sk and "S 1" in sk[992], f"E: S 부족 개체가 사유와 함께 안 남았다 — {sk}"
assert 992 not in g4["PER"] and 991 not in g4["PER"], "E: 제외 개체가 채점에 들어갔다"
print("  ✅ ⑬ 제외 개체는 사유와 함께 남고 채점에 안 들어간다")

print("\n전부 통과 ✅ — Q7-E 는 앵커를 라벨 없이 세우고, 해로울 때 기각한다")
sys.exit(0)
