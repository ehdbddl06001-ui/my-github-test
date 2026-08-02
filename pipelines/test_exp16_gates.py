"""실험16 채점 로직 픽스처 — 기전을 심어놓고 관문이 제대로 켜지는지 본다."""
import sys, numpy as np
sys.path.insert(0, "/home/user/my-github-test/pipelines")
from ecg_preflight import decide, collapse_report, assert_lead_order
from scipy import stats

ok = True
def check(name, cond):
    global ok
    print(("  ✅ " if cond else "  ❌ ") + name)
    ok = ok and bool(cond)

def t_ci(vals, conf=0.95):
    v = np.asarray(vals, float); n = len(v); m = float(v.mean())
    if n < 2: return m, np.nan, np.nan, 0.0
    sd = float(v.std(ddof=1)); h = float(stats.t.ppf(0.975, n - 1) * sd / np.sqrt(n))
    return m, m - h, m + h, sd

SEEDS = [0, 1, 2]
SITES = ["IMI", "ILMI", "IPLMI", "ASMI", "AMI", "ALMI", "LMI"]
PLANE = {"IMI": "전두면", "ILMI": "혼합", "IPLMI": "혼합", "ASMI": "횡단면",
         "AMI": "횡단면", "ALMI": "혼합", "LMI": "혼합"}
FRONT = [s for s in SITES if PLANE[s] == "전두면"]
TRANS = [s for s in SITES if PLANE[s] == "횡단면"]

print("t_ci")
m, lo, hi, sd = t_ci([1.0, 1.0, 1.0])
check("분산 0 이면 CI 폭 0", abs(hi - lo) < 1e-12 and abs(m - 1.0) < 1e-12)
m, lo, hi, sd = t_ci([-0.0303, -0.0114, +0.0336])
check("실험15d IMI Δ 를 재현한다 (−0.0027 [−0.0842,+0.0788])",
      abs(m + 0.0027) < 5e-4 and abs(lo + 0.0842) < 5e-4 and abs(hi - 0.0788) < 5e-4)
check("df=2 t 값 4.303", abs(stats.t.ppf(0.975, 2) - 4.302652) < 1e-5)

print("\nP-3 · P-4 — 기전을 심으면 켜지는가")
# 심는 기전: 전두면은 사지 2개로 포화(D≈0), 횡단면은 V1 이 크게 메운다.
def make(planted=True, noise=0.004, seed=1):
    rs = np.random.RandomState(seed)
    D = {c: {} for c in ("II", "I+II", "II+V1", "12")}
    A = {c: {} for c in D}
    for s in SITES:
        if PLANE[s] == "전두면":
            base = dict(II=0.045, **{"I+II": 0.001, "II+V1": 0.040})
        elif PLANE[s] == "횡단면" and planted:
            base = dict(II=0.150, **{"I+II": 0.140, "II+V1": 0.030})   # V1 이 메운다
        else:
            base = dict(II=0.090, **{"I+II": 0.060, "II+V1": 0.055})
        for c in ("II", "I+II", "II+V1"):
            D[c][s] = [base[c] + rs.randn() * noise for _ in SEEDS]
        D["12"][s] = [0.0] * len(SEEDS)
        for c in D:
            A[c][s] = [0.95 - d for d in D[c][s]]      # AUROC = 0.95 − D
    return D, A

D, A = make(planted=True)

# P-1 단조성
mono = sum((np.mean(D["II"][s]) >= np.mean(D["I+II"][s])) and
           (np.mean(D["II"][s]) >= np.mean(D["II+V1"][s])) for s in SITES)
check("P-1 단조성이 성립한다", mono >= len(SITES) - 1)

# P-2 전두면 포화
m, lo, hi, _ = t_ci(D["I+II"]["IMI"])
check("P-2 IMI 포화 지지 (상한 < 0.02)", decide(lo, hi, 0.02, "<") is True)

# P-3 V1 선택성
G = {s: [D["II"][s][i] - D["II+V1"][s][i] for i in range(3)] for s in SITES}
gt = [np.mean([G[s][i] for s in TRANS]) for i in range(3)]
gf = [np.mean([G[s][i] for s in FRONT]) for i in range(3)]
m3, lo3, hi3, sd3 = t_ci([gt[i] - gf[i] for i in range(3)])
check("P-3 지지 (심은 기전을 잡는다)", decide(lo3, hi3, 0.0, ">") is True)
print(f"      P-3 = {m3:+.4f} [{lo3:+.4f}, {hi3:+.4f}]")

# P-4 교차
W = {s: [A["II+V1"][s][i] - A["I+II"][s][i] for i in range(3)] for s in SITES}
wt = [np.mean([W[s][i] for s in TRANS]) for i in range(3)]
wf = [np.mean([W[s][i] for s in FRONT]) for i in range(3)]
m4, lo4, hi4, sd4 = t_ci([wt[i] - wf[i] for i in range(3)])
check("P-4 지지", decide(lo4, hi4, 0.0, ">") is True)
check("부호 교차 성립 (전두면<0<횡단면)", np.mean(wf) < 0 < np.mean(wt))
print(f"      P-4 = {m4:+.4f} [{lo4:+.4f}, {hi4:+.4f}] · 전두면 {np.mean(wf):+.4f} 횡단면 {np.mean(wt):+.4f}")

print("\n귀무(기전 없음)에서는 켜지지 않아야 한다")
D0, A0 = make(planted=False, seed=7)
G0 = {s: [D0["II"][s][i] - D0["II+V1"][s][i] for i in range(3)] for s in SITES}
gt0 = [np.mean([G0[s][i] for s in TRANS]) for i in range(3)]
gf0 = [np.mean([G0[s][i] for s in FRONT]) for i in range(3)]
m30, lo30, hi30, _ = t_ci([gt0[i] - gf0[i] for i in range(3)])
check("P-3 가 귀무에서 '지지'로 켜지지 않는다", decide(lo30, hi30, 0.0, ">") is not True)
print(f"      귀무 P-3 = {m30:+.4f} [{lo30:+.4f}, {hi30:+.4f}]")

print("\n실측 시드잡음(15d)을 넣어도 살아남는가 — 검정력 확인")
# 15d 실측: 공유 헤드 부위별 시드 SD 0.0035~0.0506 (AUPRC). AUROC 는 더 안정하지만
# 보수적으로 AUPRC 급 잡음을 그대로 얹어 본다.
for nz, label in ((0.004, "낙관 0.004"), (0.015, "실측중앙 0.015"), (0.030, "비관 0.030")):
    Dn, An = make(planted=True, noise=nz, seed=3)
    Gn = {s: [Dn["II"][s][i] - Dn["II+V1"][s][i] for i in range(3)] for s in SITES}
    gtn = [np.mean([Gn[s][i] for s in TRANS]) for i in range(3)]
    gfn = [np.mean([Gn[s][i] for s in FRONT]) for i in range(3)]
    mn, lon, hin, sdn = t_ci([gtn[i] - gfn[i] for i in range(3)])
    v = decide(lon, hin, 0.0, ">")
    print(f"      시드SD {label:<14} P-3 = {mn:+.4f} [{lon:+.4f}, {hin:+.4f}] "
          f"→ {'지지' if v else '미결' if v is None else '기각'}  (|효과|/SD = {abs(mn)/sdn:.1f})")

print("\n붕괴 감시 계약")
prev = {"IMI": .123, "ILMI": .022, "IPLMI": .0023, "ASMI": .108,
        "AMI": .016, "ALMI": .013, "LMI": .009}
r = collapse_report({s: prev[s] * 5 for s in SITES}, prev, SITES)
check("전부 살아 있으면 사망 0", r["dead"] == [] and r["fatal_majority"] is False)
sc = {s: prev[s] * 5 for s in SITES}; sc["IPLMI"] = prev["IPLMI"] * 1.0
r = collapse_report(sc, prev, SITES)
check("희소 하나만 사망 → 치명 아님", r["dead"] == ["IPLMI"] and not r["fatal_majority"])

print("\n유도 순서 — 실제 마스크 인덱스가 의도한 유도인가")
rs = np.random.RandomState(0)
I, II = rs.randn(30, 100), rs.randn(30, 100)
V = [rs.randn(30, 100) for _ in range(6)]
Xf = np.stack([I, II, II - I, -(I + II) / 2, I - II / 2, II - I / 2] + V, axis=2)
check("표준 순서 통과", assert_lead_order(Xf)["ok"])
CONFIGS = {"II": [1], "I+II": [0, 1], "II+V1": [1, 6], "12": list(range(12))}
mk = np.zeros(12); mk[CONFIGS["II+V1"]] = 1
check("{II,V1} 마스크가 II 와 V1 만 켠다",
      mk.sum() == 2 and mk[1] == 1 and mk[6] == 1 and mk[0] == 0)
mk2 = np.zeros(12); mk2[CONFIGS["I+II"]] = 1
check("{I,II} 마스크가 사지 2개만 켠다",
      mk2.sum() == 2 and mk2[0] == 1 and mk2[1] == 1 and mk2[6] == 0)
check("두 구성의 유도 수가 같다(교차 검정의 전제)", mk.sum() == mk2.sum())

print("\n" + ("전부 통과 ✅" if ok else "실패 있음 ❌"))
sys.exit(0 if ok else 1)
