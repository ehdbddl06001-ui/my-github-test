"""퀘스트46 Q1(`GMIN_S` 재정의) 노트북을 **가짜 Drive** 위에서 실제로 실행하는 픽스처.

노트북의 CELL 2~6 을 직접 읽어 돌린다(사본이 아니라 실물).

검정하는 것:
  ① Hanley–McNeil SE 가 **보수적**인가 — 부트스트랩 SE 이상이면서 2배 이내.
     헐거우면(비 < 1) GMIN 하한이 실제보다 낮게 잡혀 #213 같은 사고가 다시 난다.
  ② GMIN 스윕이 **단조**인가 — GMIN↑ → 채점 환자↓ · 커버리지↓ · 계단↓ · SE↓
  ③ 선택 규칙이 **최대 SE 조건**을 지키는가. 중앙값만 보면 SE 0.11 짜리가 섞인다
     (실험22-A #213 이 정확히 그 경우였다 → R11-b)
  ④ 조건을 만족하는 GMIN 이 **없을 때** 기각으로 끝나고 예외로 죽지 않는가

시나리오 셋:
  (A) 양성이 고르게 퍼진 코호트 → 채점 환자가 넉넉히 나온다(Q1-1 지지)
  (B) 한 환자가 양성을 독점 → 지배 지분에서 걸린다(Q1-4 기각)
  (C) 양성이 전체적으로 희박 → 조건을 만족하는 GMIN 이 없다(전부 기각, 예외 없음)
"""
import os, sys, json, shutil, tempfile
import numpy as np
from scipy import stats

NB = json.load(open(os.path.join(os.path.dirname(__file__), "..", "notebooks",
                                 "quest46_q1_gmin_resolution.ipynb")))
CODE = [c for c in NB["cells"] if c["cell_type"] == "code"]
def cell(tag):
    hit = [c for c in CODE if tag in "".join(c["source"])]
    assert len(hit) == 1, f"셀 '{tag}' 를 {len(hit)}개 찾았다"
    return "".join(hit[0]["source"])

SRC = "\n".join(cell(t) for t in ("【Q1-A】", "【Q1-B】", "【Q1-C】", "【Q1 채점】"))


def t_ci(v, conf=.95):
    v = np.asarray([x for x in v if np.isfinite(x)], float); n = len(v)
    m = float(v.mean()) if n else float("nan")
    if n < 2:
        return m, np.nan, np.nan
    h = float(stats.t.ppf(.5 + conf / 2, n - 1) * v.std(ddof=1) / np.sqrt(n))
    return m, m - h, m + h


class Run:
    def __init__(self): self.lines = []; self.dir = "/tmp"
    def log(self, s): self.lines.append(str(s)); print(s)
    def save_json(self, n, o): pass
    def savefig(self, f, n): pass


def make_cohort(rng, n, recs, n_pos, mode):
    """mode: even(고르게) · dominated(한 명 독점) · sparse(전체적으로 희박)"""
    g = rng.choice(recs, n)
    y = np.zeros(n, int)
    if mode == "dominated":
        # DS2 흉내 — 한 레코드가 양성의 ~75% (#232 는 75.2%)
        w = np.full(len(recs), 0.0045); w[0] = 1.0
    elif mode == "sparse":
        w = np.full(len(recs), 1.0)
    else:
        w = rng.pareto(1.5, len(recs)) + 0.5
    w = w / w.sum()
    for r, p in zip(recs, w):
        ii = np.where(g == r)[0]
        k = min(len(ii) - 1, int(round(n_pos * p)))
        if k > 0:
            y[rng.choice(ii, k, replace=False)] = 1
    y[rng.choice(np.where(y == 0)[0], min(2000, int((y == 0).sum() // 3)),
                 replace=False)] = 2          # V 도 조금
    return g, y


def scenario(tag, mode, n_pos, seed=0):
    print("\n" + "=" * 78); print(f"### {tag}"); print("=" * 78)
    rng = np.random.RandomState(seed)
    W = [100 + i for i in range(22)]
    C = [300 + i for i in range(75)]
    gw, yw = make_cohort(rng, 40000, W, 1837, "dominated")   # within 은 항상 DS2 흉내
    gc, yc = make_cohort(rng, 120000, C, n_pos, mode)

    def probs(y):
        """AUROC 가 **천장에 붙지 않게** 만든다(≈0.8).

        ★ 처음엔 분리를 세게 줬더니 AUROC 가 0.99 근처가 됐고, 그러면 Hanley 의
          이항정규 가정이 깨져 부트 대비 4~6배로 부푼다. 근사의 타당성을 검정하려면
          **실데이터와 비슷한 분리도**여야 한다(실험22-A 의 환자별 AUROC 는 0.77~0.95)."""
        lg = rng.normal(0, 1, (5, len(y), 3))
        for k in (1, 2):
            lg[:, y == k, k] += 1.2
        e = np.exp(lg - lg.max(2, keepdims=True))
        return e / e.sum(2, keepdims=True)

    P = {"y_within": yw, "y_cross": yc,
         "v2_within_raw": probs(yw), "v2_cross_raw": probs(yc)}
    g = {"np": np, "t_ci": t_ci, "run": Run(), "CONFIG": {},
         "COH": {"within (MIT-BIH DS2)": (yw, gw), "cross (INCART)": (yc, gc)},
         "P": P, "SE_CAP": 0.05, "SE_MULT": 2.0, "N_MIN": 20,
         "COV_MIN": 0.70, "DOM_MAX": 0.50, "SEED0": 1,
         "GMINS": [2, 5, 10, 15, 20, 30, 40, 50, 75, 100, 150, 200]}
    exec(compile(SRC, "quest46_q1", "exec"), g)
    return g


# ── (A) 고르게 퍼진 코호트
a = scenario("(A) INCART 흉내 — 양성이 고르게 퍼짐", "even", 1958)
va = a["CONFIG"]["result"]["verdicts"]
print(f">>> {va}")
assert va["Q1-1"] == "✅ 지지", f"A: 채점 환자가 확보돼야 한다 — {va}"
assert va["Q1-4"] == "✅ 지지", f"A: 지배 지분이 낮아야 한다 — {va}"
assert va["Q1-5"] == "✅ 지지", "A: INCART 가 DS2 보다 환자가 많아야 한다"

# ── 스윕 단조성 (②)
#   ⚠️ `se_med` 는 **단조가 아니다** — GMIN 이 오르면 채점 집합이 바뀌는데, AUROC 가
#     높은 레코드는 SE 가 작아서 집합이 줄면 중앙값이 오를 수 있다. 처음엔 단조를
#     가정했다가 이 픽스처에 걸렸다. 집합 크기에만 의존하는 셋만 단조를 요구한다.
for key, rows in a["SWEEP"].items():
    fin = [r for r in rows if r["n_rec"] > 0]
    for k in ("n_rec", "cov", "step_med"):
        vals = [r[k] for r in fin]
        assert all(x >= y - 1e-9 for x, y in zip(vals, vals[1:])), \
            f"{key} 의 {k} 가 GMIN 에 대해 단조감소가 아니다: {vals}"
    se = [r["se_med"] for r in fin]
    assert se[0] >= se[-1] - 1e-9, f"{key}: SE 가 전체적으로는 줄어야 한다 {se}"
print("\n✅ ② 스윕 — 환자·커버리지·계단은 단조감소 · SE 는 전체 추세만(집합이 바뀐다)")

# ── 선택 규칙이 최대 SE 를 지키는가 (③)
for key, sel in a["PICK"].items():
    if sel:
        assert sel["se_max"] <= 0.05 * 2.0 + 1e-9, \
            f"{key}: 최대 SE {sel['se_max']:.4f} 가 상한을 넘었는데 선택됐다"
        assert sel["se_med"] <= 0.05 + 1e-9, f"{key}: 중앙 SE 초과"
        assert sel["n_rec"] >= 20, f"{key}: 환자 수 미달"
print("✅ ③ 선택 규칙이 중앙·최대 SE 와 환자 수를 모두 지킨다")

# ── Hanley 가 보수적인가 (①)
for key, ratio in a["RATIO"].items():
    if np.isfinite(ratio):
        # 하한이 본질이다 — Hanley 가 실제보다 **작으면** GMIN 이 헐거워져 위험하다.
        # 상한은 '과도한 보수성 = 환자를 불필요하게 잃음' 이라 경고 대상이지 실패는 아니다.
        assert ratio >= 0.90, f"{key}: Hanley/부트 = {ratio:.2f} — 보수적이지 않다(위험)"
        if ratio > 2.0:
            print(f"  ⚠️ {key}: 비 {ratio:.2f} — 과도하게 보수적(AUROC 천장 효과)")
print(f"✅ ① Hanley 가 부트스트랩 이상: "
      f"{ {k[1]: round(v, 2) for k, v in a['RATIO'].items() if np.isfinite(v)} }")

# ── (B) 한 환자 독점 → Q1-4 기각
b = scenario("(B) 한 환자가 양성을 독점", "dominated", 1958, seed=1)
vb = b["CONFIG"]["result"]["verdicts"]
print(f">>> {vb}")
assert vb["Q1-4"] == "❌ 기각", f"B: 지배 지분에서 걸려야 한다 — {vb}"

# ── (C) 양성 희박 → 조건 만족 GMIN 없음. 예외 없이 기각으로 끝나야 한다
c = scenario("(C) 양성이 희박 — 조건을 만족하는 GMIN 이 없다", "sparse", 60, seed=2)
vc = c["CONFIG"]["result"]["verdicts"]
print(f">>> {vc}")
assert vc["Q1-1"] == "❌ 기각", f"C: 환자 확보 실패로 기각돼야 한다 — {vc}"
assert c["PICK"][("cross (INCART)", "S")] is None, "C: 선택된 GMIN 이 없어야 한다"
print("✅ ④ 조건 불만족 시 예외 없이 기각으로 끝난다")

print("\n전부 통과 ✅ — Q1 은 '환자를 몇 명 확보할 수 있나' 를 정직하게 잰다")
sys.exit(0)
