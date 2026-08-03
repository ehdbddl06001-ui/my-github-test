"""퀘스트46 Q7(SVDB 코호트 스크리닝) 노트북을 합성 데이터로 검정하는 픽스처.

노트북의 CELL 3(【Q7-A】)·CELL 4(【Q7 채점】)를 직접 읽어 돌린다.
CELL 2(주석 다운로드)는 네트워크가 필요하므로 `CNT` 를 합성으로 주입한다.

검정하는 것:
  ① `dist_stats` 가 **실측 DS2 값을 그대로 재현**하는가
     (지배 75.2% · 양성>0 16/22 · 중앙값 4.5 · k50=1 · k90=4)
     → 이게 안 맞으면 R13 통계 자체를 못 믿는다
  ② `gmin_table` 이 단조인가
  ③ SVDB 가 넉넉하면 지지, 편중되면 기각으로 갈리는가
  ④ 관문이 예외 없이 끝나는가

★ 이 픽스처가 잡은 것: 노트북 Q1-A 가 중앙값을 `int(np.median(...))` 으로 잘라
  4.5 를 4 로 보고하고 있었다. 카드에도 그대로 들어갔다 — 고쳤다.
"""
import os, sys, json
import numpy as np

NB = json.load(open(os.path.join(os.path.dirname(__file__), "..", "notebooks",
                                 "quest46_q7_svdb_cohort.ipynb")))
CODE = [c for c in NB["cells"] if c["cell_type"] == "code"]
def cell(tag):
    hit = [c for c in CODE if tag in "".join(c["source"])]
    assert len(hit) == 1, f"셀 '{tag}' 를 {len(hit)}개 찾았다"
    return "".join(hit[0]["source"])

SRC = cell("【Q7-A】") + "\n" + cell("【Q7 채점】")

# ── run.* API 정합성 (Q1 에서 배운 것 — exec 안 하는 셀도 정적으로 본다)
def check_run_api():
    import re
    lib = os.path.join(os.path.dirname(__file__), "..", "lib", "medkos_run.py")
    if not os.path.exists(lib):
        print("  (lib/medkos_run.py 없음 — 생략)"); return
    have = set(re.findall(r"^\s{4}def (\w+)\(", open(lib).read(), re.M))
    nb_src = "".join("".join(c["source"]) for c in CODE)
    miss = sorted(set(re.findall(r"\brun\.(\w+)\(", nb_src)) - have)
    assert not miss, f"MedKOSRun 에 없는 메서드 호출: {miss}"
    call = re.search(r"MedKOSRun\(([^)]*)\)", nb_src)
    assert call and "project" in call.group(1), \
        f"MedKOSRun 호출에 project 가 없다: {call.group(1) if call else None}"
    print("  ✅ run.* API 정합")

print("### run.* API 정합성")
check_run_api()


class Run:
    def __init__(self): self.lines = []; self.dir = "/tmp"
    def log(self, s): self.lines.append(str(s)); print(s)
    def save_json(self, n, o): pass
    def save_fig(self, n, f=None): pass


# forensics/Q1 실측 — 지어낸 값이 아니다
DS2_REAL = {100:33,103:2,105:0,111:0,113:6,117:1,121:1,123:0,200:30,202:55,210:22,
            212:0,213:28,214:0,219:7,221:0,222:209,228:3,231:1,232:1382,233:7,234:50}


def run_cells(svdb_s):
    g = {"np": np, "run": Run(), "CONFIG": {},
         "CNT": {r: {0: 2000, 1: n, 2: 100} for r, n in svdb_s.items()},
         "STAT": {}, "GMINS": [2, 5, 10, 15, 20, 30, 50, 75, 100, 200, 500],
         "GMIN_SCREEN": 10, "N_MIN": 20}
    exec(compile(SRC, "quest46_q7", "exec"), g)
    return g


def scenario(tag, svdb_s):
    print("\n" + "=" * 78); print(f"### {tag}"); print("=" * 78)
    return run_cells(svdb_s)


# ── ① dist_stats 가 실측 DS2 를 재현하는가
probe = run_cells({800 + i: 50 for i in range(30)})
ds = probe["dist_stats"](DS2_REAL)
print(f"\n### ① dist_stats(DS2 실측) = {ds}")
assert ds["total"] == 1837, ds["total"]
assert abs(ds["dom"] - 0.7523) < 0.001, f"지배지분 {ds['dom']:.4f} ≠ 75.2%"
assert ds["n_pos"] == 16, f"양성>0 {ds['n_pos']} ≠ 16"
assert abs(ds["med"] - 4.5) < 1e-9, f"중앙값 {ds['med']} ≠ 4.5  ← int() 절삭 회귀"
assert (ds["k50"], ds["k90"]) == (1, 4), f"k50/k90 {ds['k50']}/{ds['k90']} ≠ 1/4"
print("✅ ① 실험22-A·Q1 실측을 그대로 재현한다")

# ── ② gmin_table 단조
tbl = probe["gmin_table"](DS2_REAL, [2, 5, 10, 20, 50, 200])
ns = [r["n"] for r in tbl]
assert all(a >= b for a, b in zip(ns, ns[1:])), f"단조감소 위반 {ns}"
print(f"✅ ② gmin_table 단조 — {ns}")

# ── ③ 넉넉한 SVDB → 지지
a = scenario("(A) SVDB 가 넉넉하다 — 40레코드가 S 를 30개씩", {800 + i: 30 for i in range(40)})
va = a["CONFIG"]["result"]["verdicts"]
print(f">>> {va}")
assert all(v.startswith("✅") for v in va.values()), f"A 는 전부 지지여야 한다 — {va}"

# ── 편중된 SVDB → 기각
b = scenario("(B) SVDB 도 한 레코드가 독점", {800: 1500, **{801 + i: 2 for i in range(30)}})
vb = b["CONFIG"]["result"]["verdicts"]
print(f">>> {vb}")
assert vb["Q7-1"] == "❌ 기각", f"B: 채점 개체 부족으로 기각 — {vb}"
assert vb["Q7-2"] == "❌ 기각", f"B: 지배 지분에서도 걸려야 한다 — {vb}"

# ── 경계: 정확히 20개
c = scenario("(C) 경계 — S≥10 인 레코드가 정확히 20개",
             {**{800 + i: 12 for i in range(20)}, **{900 + i: 3 for i in range(20)}})
vc = c["CONFIG"]["result"]["verdicts"]
print(f">>> {vc}")
assert vc["Q7-1"] == "✅ 지지", f"C: 20개는 하한 이상이므로 지지 — {vc}"

print("\n전부 통과 ✅ — Q7 은 SVDB 를 필요조건으로 거른다")
sys.exit(0)
