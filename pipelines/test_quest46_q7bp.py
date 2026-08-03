"""퀘스트46 Q7-B′(전수 재채점) 노트북을 합성 데이터로 검정하는 픽스처.

Q7-B 노트북은 **얼려 둔다**(관문이 이미 발화했다). 이건 별도 실험이고 자기 사전등록을
갖는다. 그래서 픽스처도 따로다.

정적 검사:
  ① `run.*` API 정합 + `MedKOSRun(..., project=)`
  ② **GMIN 을 여기서 다시 고르지 않는다** — Q7-B 에서 승계한 상수만 쓴다.
     스윕이 있으면 '전수를 보고 GMIN 을 고른' 것이 되어 R12 위반이다.
  ③ 연속번호 fallback 부재 (R16) + 재라벨 단사성·목록 부분집합 검사
  ④ 부지표 셀이 관문을 안 바꾼다(사후등록 금지)

동적 검사:
  ⑤ 매핑이 어긋난 캐시를 주면 **복원해서** 채점하는가 (Q7-B 와 같은 지문)
  ⑥ 관문이 통과기가 아닌가 — 개체 부족·지배 개체에서 각각 기각되는가
  ⑦ **P5 순열검정이 작동하는가** — ★ 처음에 방향을 거꾸로 걸었다가 픽스처가 잡았다.
     P5 는 '관측 격차가 **이 코호트의 개체 간 산포**로 설명되나' 를 묻는다. 균질하면
     무작위 분할 격차가 작아 0.0874 가 **희귀**해지고(p 작음 → 기각), 이질적이면
     흔해진다(p 큼 → 지지). 양쪽을 다 낼 수 있어야 한다
  ⑧ 전수 CI 폭이 반쪽보다 좁아지는가 (R15 — 개체를 늘리면 좁아진다)

★ 픽스처는 정밀도가 아니라 논리를 검정한다. 부트·순열 횟수를 줄여 돌린다.
"""
import os, sys, json, re
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
NB = json.load(open(os.path.join(ROOT, "notebooks", "quest46_q7bp_svdb_full.ipynb")))
CODE = [c for c in NB["cells"] if c["cell_type"] == "code"]


def cell(tag):
    hit = [c for c in CODE if tag in "".join(c["source"])]
    assert len(hit) == 1, f"셀 '{tag}' 를 {len(hit)}개 찾았다"
    return "".join(hit[0]["source"])


SRC_G0 = cell("【G0】")
SRC_A = cell("【Q7B′-A】")
SRC_B = cell("【Q7B′-B】")

print("### 정적 검사")


def check_run_api():
    lib = os.path.join(ROOT, "lib", "medkos_run.py")
    if not os.path.exists(lib):
        print("  (lib 없음 — 생략)"); return
    have = set(re.findall(r"^\s{4}def (\w+)\(", open(lib).read(), re.M))
    src = "".join("".join(c["source"]) for c in CODE)
    miss = sorted(set(re.findall(r"\brun\.(\w+)\(", src)) - have)
    assert not miss, f"MedKOSRun 에 없는 메서드: {miss}"
    call = re.search(r"MedKOSRun\(([^)]*)\)", src)
    assert call and "project" in call.group(1), "MedKOSRun 호출에 project 없음"
    print("  ✅ ① run.* API 정합")


check_run_api()

# ② GMIN 을 여기서 고르면 안 된다 — 전수를 보고 고르는 게 되어 R12 위반
ALL_SRC = "".join("".join(c["source"]) for c in CODE)
assert "GMINS" not in ALL_SRC, "❌ GMIN 스윕이 있다 — 전수를 보고 GMIN 을 고르면 R12 위반"
assert re.search(r"^GMIN\s*=\s*2\b", ALL_SRC, re.M), "GMIN 이 상수로 고정돼 있지 않다"
assert "gmin_provenance" in ALL_SRC, "GMIN 의 출처(Q7-B DEV)를 기록하지 않았다"
for bad in ("se_cap", "SE_CAP", "후보 GMIN"):
    assert bad not in ALL_SRC, f"❌ GMIN 재선택 흔적: {bad}"
print("  ✅ ② GMIN 은 Q7-B 에서 승계한 상수 — 여기서 다시 고르지 않는다")

# ③ fallback 금지 + 재라벨 안전장치 (R16)
assert "range(800, 895)" not in ALL_SRC and "range(800,895)" not in ALL_SRC, \
    "❌ 연속번호 fallback 이 있다"
assert "재라벨에서 레코드가 합쳐졌다" in SRC_G0, "재라벨 단사성 검사 없음"
assert "재라벨 후에도 목록 밖 번호가 남았다" in SRC_G0, "목록 부분집합 검사 없음"
assert "매핑 재검증 실패" in SRC_G0, "(N,S,V) 재검증이 없다"
print("  ✅ ③ fallback 부재 + 재라벨 단사성·부분집합·(N,S,V) 재검증")

# ④ 부지표는 관문을 못 바꾼다
assert 'CONFIG["result"]["verdicts"] == _V0' in SRC_B, "❌ 관문 불변 확인이 없다"
assert "✅ 지지" not in SRC_B, "❌ 부지표 셀이 판정을 낸다"
assert all(f"P{i}" in SRC_A for i in range(1, 6)), "관문 5개가 A 셀에 다 없다"
print("  ✅ ④ 부지표 셀은 관문을 바꾸지 않는다")


# ═══════════════════════════════════════════════════════════════════════
class Run:
    def __init__(self): self.lines = []; self.dir = "/tmp"
    def log(self, s=""): self.lines.append(str(s)); print(s)
    def save_json(self, n, o): pass
    def save_fig(self, n, f=None): pass
    def finish(self, r): pass


def build(rng, spec, nneg=400, nv=40):
    ys, rs, sS, sV = [], [], [], []
    for r, npos, auc in spec:
        d = (np.sqrt(2) * abs(np.percentile(rng.normal(size=60000), 100 * auc))
             if 0.5 < auc < 1 else 0.0)
        ys.append(np.r_[np.ones(npos, int), np.full(nv, 2), np.zeros(nneg, int)])
        rs.append(np.full(npos + nv + nneg, r))
        sS.append(np.r_[rng.normal(d, 1, npos), rng.normal(0, 1, nv), rng.normal(0, 1, nneg)])
        sV.append(np.r_[rng.normal(0, 1, npos), rng.normal(d, 1, nv), rng.normal(0, 1, nneg)])
    y = np.concatenate(ys); rec = np.concatenate(rs)
    a, b = np.concatenate(sS), np.concatenate(sV)
    prob = np.zeros((5, len(y), 3))
    for k in range(5):
        prob[k, :, 1] = a + rng.normal(0, .01, len(a))
        prob[k, :, 2] = b + rng.normal(0, .01, len(b))
    return y, rec, prob


def run_full(tag, spec, seed=0, nperm=3000):
    print("\n" + "=" * 78); print(f"### {tag}"); print("=" * 78)
    rng = np.random.RandomState(seed)
    y, rec, prob = build(rng, spec)
    g = {"np": np, "run": Run(), "P": {"v2_cross_raw": prob}, "Y": y, "REC": rec,
         "CONFIG": {}, "GMIN": 2, "SE_MAX": .10, "N_MIN": 8, "DOM_MAX": .50,
         "CIW_MAX": .10, "NB_BOOT": 120, "NB_MACRO": 800, "NB_PERM": nperm,
         "IDX_S": 1, "IDX_V": 2, "SEED0": 1, "AssetError": RuntimeError}
    exec(compile(SRC_A, "q7bp_a", "exec"), g)
    return g


# ── ⑤ 매핑 복원 (G0) — Q7-B 와 같은 지문을 주고 복원되는지
print("\n### ⑤ 매핑 복원")
import tempfile, shutil
tmp = tempfile.mkdtemp(); os.makedirs(os.path.join(tmp, "data"))
REAL = [n for n in range(800, 895) if n not in
        list(range(813, 820)) + list(range(830, 840))]        # 78개 (실제 SVDB 구조)
rng = np.random.RandomState(0)
spec = [(800 + i, 20 + i, 0.9) for i in range(len(REAL))]      # 라벨 = 800+인덱스 (사고 재현)
y, rec, prob = build(rng, spec, nneg=200, nv=10)
np.savez(os.path.join(tmp, "data", "q7b_svdb_probs_s5.npz"),
         y_cross=y, rec_cross=rec, v2_cross_raw=prob)
CNT = {}
for i, t in enumerate(REAL):
    m = rec == 800 + i
    CNT[str(t)] = {"0": int((y[m] == 0).sum()), "1": int((y[m] == 1).sum()),
                   "2": int((y[m] == 2).sum())}
json.dump(CNT, open(os.path.join(tmp, "data", "svdb_ann_counts.json"), "w"))

g0 = {"np": np, "os": os, "json": json, "sys": sys, "importlib": __import__("importlib"),
      "run": Run(), "CONFIG": {}, "PROJECT": tmp, "AssetError": RuntimeError,
      "wfdb": type("W", (), {"get_record_list": staticmethod(lambda db: [str(r) for r in REAL])})()}
exec(compile(SRC_G0.replace("try:\n    import wfdb", "if False:\n    import wfdb")
             .replace("except ModuleNotFoundError:", "elif False:"), "q7bp_g0", "exec"), g0)
got = sorted(int(x) for x in np.unique(g0["REC"]))
assert got == sorted(REAL), f"복원 실패 — {got[:6]} vs {sorted(REAL)[:6]}"
assert g0["CONFIG"]["id_map_recheck"]["agree"] == len(REAL), g0["CONFIG"]["id_map_recheck"]
shutil.rmtree(tmp, ignore_errors=True)
print(f"  ✅ ⑤ 라벨 800~877 → 참 번호 {len(REAL)}개 전부 복원 · (N,S,V) 전수 일치")

# ── ⑥ 관문이 통과기가 아니다
print("\n### ⑥ 관문이 무조건 통과기가 아닌가")
gA = run_full("(A) 개체 6개 — 하한(8)에서 기각 · P5 는 미결이어야 한다",
              [(400 + i, 40, 0.9) for i in range(6)], seed=1)
vA = gA["CONFIG"]["result"]["verdicts"]
assert vA["P1"] == "❌ 기각", vA
# ★ 픽스처가 잡은 버그: n1=28 을 개체 수 확인 없이 쓰면 av[pm[28:]] 가 빈 배열이 되어
#   평균이 nan → 비교가 전부 False → p=0 → **조용히 기각**이 나왔다. 나눌 수 없으면 미결이다.
assert vA["P5"] == "⚠️ 미결", f"A: 6개체로는 28/x 분할이 불가능하니 미결이어야 한다 — {vA}"
assert gA["CONFIG"]["result"]["perm"] is None, "A: 순열 결과가 있으면 안 된다"
print("  ✅ 개체 하한에서 기각 · 분할 불가한 P5 는 미결(조용한 기각 아님)")
gB = run_full("(B) 지배 개체 — R11-3 이 잡아야 한다",
              [(400, 4000, 0.9)] + [(401 + i, 20, 0.9) for i in range(11)], seed=2)
vB = gB["CONFIG"]["result"]["verdicts"]
assert vB["P3"] == "❌ 기각", f"지배 지분 관문 — {gB['CONFIG']['result']['full_S']['dom']:.1%}"
print(f"  ✅ 지배 지분 {gB['CONFIG']['result']['full_S']['dom']:.1%} 기각")

# ── ⑦ P5 순열검정이 양쪽으로 작동하는가
#
#  ★★ 처음에 방향을 **거꾸로** 걸었다가 픽스처가 잡았다. 바로잡은 의미론:
#     P5 는 "관측 격차 0.0874 가 **이 코호트의 개체 간 산포**로 설명되나" 를 묻는다.
#       · 코호트가 **균질**하면(개체 간 SD 작음) 무작위 분할 격차도 작다 →
#         0.0874 는 **희귀** → p 작음 → **기각**("우연이 아니다, 뭔가 구조적이다")
#       · 코호트가 **이질**적이면(SD 큼) 무작위 분할로도 그 정도 격차가 흔하다 →
#         p 큼 → **지지**("우연으로 설명된다")
#     즉 균질 코호트에서 p 가 작게 나오는 게 **정상**이다. 내가 반대로 기대했다.
print("\n### ⑦ P5 순열검정 — 균질이면 p 작고, 이질이면 p 커야 한다")
gH = run_full("(C) 균질(전부 AUROC 0.90) — 0.0874 는 희귀해야 한다(p 작음 → 기각)",
              [(400 + i, 40, 0.90) for i in range(55)], seed=3)
pH = gH["CONFIG"]["result"]["perm"]["p"]
gS = run_full("(D) 강한 이질(0.99 층 28 + 0.60 층 27) — 0.0874 는 흔해야 한다(p 큼 → 지지)",
              [(400 + i, 40, 0.99) for i in range(28)]
              + [(500 + i, 40, 0.60) for i in range(27)], seed=4)
pS = gS["CONFIG"]["result"]["perm"]["p"]
sdH = np.std(gH["CONFIG"]["result"]["full_S"]["auroc"], ddof=1)
sdS = np.std(gS["CONFIG"]["result"]["full_S"]["auroc"], ddof=1)
print(f"    균질  개체간 SD {sdH:.4f} → p={pH:.4f} · {gH['CONFIG']['result']['verdicts']['P5']}")
print(f"    이질  개체간 SD {sdS:.4f} → p={pS:.4f} · {gS['CONFIG']['result']['verdicts']['P5']}")
assert sdS > sdH, "시나리오 구성 오류 — 이질 코호트의 SD 가 더 커야 한다"
assert pH < 0.05, f"균질 코호트에서는 0.0874 가 희귀해 기각이어야 한다 — p={pH:.4f}"
assert pS > pH, f"이질일수록 p 가 커야 한다 — 균질 {pH:.4f} vs 이질 {pS:.4f}"
assert gH["CONFIG"]["result"]["verdicts"]["P5"] == "❌ 기각"
assert gS["CONFIG"]["result"]["verdicts"]["P5"] == "✅ 지지", \
    f"강한 이질에서는 지지가 나와야 한다 — p={pS:.4f} (관문이 기각기 전용이면 안 된다)"
print("  ✅ ⑦ 순열검정이 양쪽으로 작동한다 — 기각·지지 둘 다 낼 수 있다")

# ── ⑧ 개체를 늘리면 CI 폭이 좁아진다 (R15)
print("\n### ⑧ 개체 수와 CI 폭 (R15)")
half = run_full("(E-half) 개체 28", [(400 + i, 40, 0.90) for i in range(28)], seed=5, nperm=500)
full = run_full("(E-full) 개체 56 — 같은 분포", [(400 + i, 40, 0.90) for i in range(56)],
                seed=5, nperm=500)
wh = half["CONFIG"]["result"]["full_S"]["width"]; wf = full["CONFIG"]["result"]["full_S"]["width"]
print(f"    CI 폭 — 28개체 {wh:.4f} → 56개체 {wf:.4f} (비 {wf/wh:.2f} · √2 예측 0.71)")
assert wf < wh, "개체를 늘렸는데 CI 가 안 좁아졌다 — R15 와 어긋난다"
print("  ✅ ⑧ 개체를 늘리면 CI 폭이 좁아진다")

print("\n전부 통과 ✅ — Q7-B′ 는 GMIN 을 다시 고르지 않고 전수를 잰다")
sys.exit(0)
