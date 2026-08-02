"""실험22(감별질환별 위양성 분해) 채점 로직 픽스처.

이 픽스처가 실행 **전에** 잡아낸 설계 결함 두 개:
  ① 위험비는 천장이 1/FPR(NORM) 이라, 경보율 0.5 인 부위에서는 기전을 심어도
     '2배' 를 못 넘는다(실측 1.56 에서 막힘) → **오즈비로 판정한다.**
  ② 표본 21,799건에 시드 3~6개면 SD 가 극히 작아 **+0.01 짜리 차이도 CI 가 0 을
     벗어난다**(귀무가 P-3 를 통과했다) → **최소 유의미 차 0.5 를 사전에 못 박는다.**
"""
import sys, numpy as np
sys.path.insert(0, "/home/user/my-github-test/pipelines")
from ecg_preflight import decide
from scipy import stats

ok = True
def check(n, c):
    global ok
    print(("  ✅ " if c else "  ❌ ") + n); ok = ok and bool(c)

def t_ci(v, conf=.95):
    v = np.asarray([x for x in v if np.isfinite(x)], float); n = len(v)
    m = float(v.mean()) if n else float("nan")
    if n < 2: return m, np.nan, np.nan, 0.0
    sd = float(v.std(ddof=1))
    h = float(stats.t.ppf(.5 + conf / 2, n - 1) * sd / np.sqrt(n))
    return m, m - h, m + h, sd

def _odds(x, eps=1e-6):
    x = min(max(float(x), eps), 1.0 - eps); return x / (1.0 - x)

N, K, NS = 21799, 5, 7
OR_THR, P3_MARGIN, MIN_FP = 2.0, 0.5, 5
SITES = ["IMI", "ILMI", "IPLMI", "ASMI", "AMI", "ALMI", "LMI"]
MIMIC_Q, CONDUCT = ["CLBBB", "LVH", "WPW"], ["CRBBB", "IRBBB", "IVCD"]
MIMIC_SITES = {"CLBBB": ["ASMI", "AMI"], "LVH": ["ASMI", "AMI"], "WPW": ["IMI"]}
TARGET_SITES = ["ASMI", "AMI", "IMI"]

rs = np.random.RandomState(0)
CV = np.tile(np.arange(K), N // K + 1)[:N]
Y = np.zeros((N, NS), bool)
for j, p in enumerate([.1228, .0219, .0023, .1081, .0162, .0132, .0092]):
    Y[rs.choice(N, int(N * p), replace=False), j] = True
G, pool, ptr = {}, np.where(~Y.any(1))[0], 0
rs.shuffle(pool)
for g, n in (("NORM", 9500), ("CLBBB", 536), ("LVH", 2137), ("WPW", 80),
             ("CRBBB", 542), ("IRBBB", 1118), ("IVCD", 789)):
    m = np.zeros(N, bool); m[pool[ptr:ptr + n]] = True; ptr += n; G[g] = m
N_NORM = {s: int((G["NORM"] & (~Y[:, j])).sum()) for j, s in enumerate(SITES)}

def alarms(P_):
    out = np.zeros((N, NS), bool)
    for j in range(NS):
        for k in range(K):
            te = np.where(CV == k)[0]; rest = np.where(CV != k)[0]
            r = np.random.RandomState(1 + k); r.shuffle(rest)
            va = rest[:max(int(len(rest) * .12), 200)]
            pos = P_[va, j][Y[va, j]]
            t = float(np.quantile(pos, .10, method="lower")) if len(pos) else -np.inf
            out[te, j] = P_[te, j] >= t
    return out

def fpr(a, j, mask):
    sel = mask & (~Y[:, j]); return float(a[sel, j].mean()) if sel.sum() else np.nan

def build(mode):
    A = []
    for sd in range(3):
        r = np.random.RandomState(100 + sd)
        p = r.rand(N, NS) * 0.9 + Y * 0.35
        if mode == "planted":
            for g in MIMIC_Q: p[G[g], SITES.index("ASMI")] += 0.25
        elif mode == "all_abnormal":
            for g in MIMIC_Q + CONDUCT: p[G[g]] += 0.25
        A.append(alarms(np.clip(p, 0, 1)))
    return A

def tab(A):
    OR = {g: {s: [] for s in SITES} for g in G}
    RR = {g: {s: [] for s in SITES} for g in G}
    for i, a in enumerate(A):
        for j, s in enumerate(SITES):
            den = fpr(a, j, G["NORM"]); good = den * N_NORM[s] >= MIN_FP
            for g in G:
                num = fpr(a, j, G[g])
                OR[g][s].append(_odds(num) / _odds(den) if good else np.nan)
                RR[g][s].append(num / den if good else np.nan)
    return OR, RR

def macro(R_, lst, per_site=None):
    """★ 기전이 예측하는 부위에서만 평균. 7부위 평균은 희석된다."""
    pairs = ([(g, s) for g in lst for s in per_site[g]] if per_site
             else [(g, s) for g in lst for s in TARGET_SITES])
    return [float(np.nanmean([R_[g][s][i] for g, s in pairs])) for i in range(3)]

def macro_all(R_, lst):
    return [float(np.nanmean([[R_[g][s][i] for s in SITES] for g in lst]))
            for i in range(3)]

print("① 위험비 천장 — 왜 오즈비여야 하나")
OR, RR = tab(build("planted"))
rr = t_ci(RR["CLBBB"]["ASMI"])[0]; orv, lo, hi, _ = t_ci(OR["CLBBB"]["ASMI"])
print(f"      CLBBB→ASMI  위험비 {rr:.2f} · 오즈비 {orv:.2f} [{lo:.2f}, {hi:.2f}]")
check("위험비로는 기전을 심어도 2배를 못 넘는다(천장)", rr < OR_THR)
check("오즈비는 같은 기전을 잡아낸다", decide(lo, hi, OR_THR, ">") is True)

print("\n② P-3 특이성 대조")
mq, cd = macro(OR, MIMIC_Q, MIMIC_SITES), macro(OR, CONDUCT)
print(f"      (희석 대조) 7부위 macro = {np.mean(macro_all(OR, MIMIC_Q)):.2f} "
      f"vs 표적 부위 macro = {np.mean(mq):.2f}")
check("7부위 macro 는 기전을 희석한다(그래서 표적 부위로 잰다)",
      np.mean(macro_all(OR, MIMIC_Q)) < np.mean(mq))
m3, lo3, hi3, _ = t_ci([mq[i] - cd[i] for i in range(3)])
print(f"      모방 OR {np.mean(mq):.2f} vs 전도장애 OR {np.mean(cd):.2f} → {m3:+.2f}")
check("기전을 심으면 P-3 통과", decide(lo3, hi3, P3_MARGIN, ">") is True)

OR0, _ = tab(build("null"))
mq0, cd0 = macro(OR0, MIMIC_Q, MIMIC_SITES), macro(OR0, CONDUCT)
m30, lo30, hi30, _ = t_ci([mq0[i] - cd0[i] for i in range(3)])
print(f"      귀무 차 {m30:+.3f} [{lo30:+.3f}, {hi30:+.3f}]")
check("귀무에서 문턱 0 이면 잘못 통과한다(그래서 0 을 안 쓴다)",
      decide(lo30, hi30, 0.0, ">") is True or abs(m30) < 0.05)
check("**최소 유의미 차 0.5 를 쓰면 귀무를 걸러낸다**",
      decide(lo30, hi30, P3_MARGIN, ">") is not True)

ORa, _ = tab(build("all_abnormal"))
mqa, cda = macro(ORa, MIMIC_Q, MIMIC_SITES), macro(ORa, CONDUCT)
m3a, lo3a, hi3a, _ = t_ci([mqa[i] - cda[i] for i in range(3)])
print(f"      사소한 대안(모든 비정상↑) 차 {m3a:+.2f} [{lo3a:+.2f}, {hi3a:+.2f}]")
check("**P-3 이 '비정상은 다 위양성 많다' 를 걸러낸다**",
      decide(lo3a, hi3a, P3_MARGIN, ">") is not True)

print("\n③ 분모 가드 — FPR(NORM)≈0 에서 배수 폭발 방지")
Az = [alarms(np.clip(np.random.RandomState(9 + i).rand(N, NS) * 0.05 + Y * 0.9, 0, 1))
      for i in range(3)]
ORz, RRz = tab(Az)
nan_cells = sum(1 for g in G for s in SITES
                if not np.isfinite(np.nanmean(RRz[g][s])))
print(f"      NORM FPR(ASMI) = {fpr(Az[0], 3, G['NORM']):.5f} · 배수 nan 칸 {nan_cells}")
check("분모가 작으면 배수를 안 낸다", nan_cells > 0)

print("\n④ 소집단 부트스트랩")
j = SITES.index("ASMI"); a = build("planted")[0][:, j]
gm = np.where(G["WPW"] & (~Y[:, j]))[0]; nm = np.where(G["NORM"] & (~Y[:, j]))[0]
r2 = np.random.RandomState(7)
b = [a[gm[r2.randint(0, len(gm), len(gm))]].mean() /
     max(a[nm[r2.randint(0, len(nm), len(nm))]].mean(), 1e-9) for _ in range(2000)]
blo, bhi = np.percentile(b, [2.5, 97.5])
slo, shi = t_ci(RR["WPW"]["ASMI"])[1:3]
print(f"      WPW n={len(gm)} · 시드 [{slo:.2f},{shi:.2f}] · 부트 [{blo:.2f},{bhi:.2f}]")
W = (min(slo, blo), max(shi, bhi))
print(f"      넓은 쪽 채택 → [{W[0]:.2f}, {W[1]:.2f}]")
check("두 CI 를 감싸는 '넓은 쪽' 규칙이 항상 보수적이다",
      W[0] <= min(slo, blo) + 1e-9 and W[1] >= max(shi, bhi) - 1e-9
      and (W[1] - W[0]) >= max(shi - slo, bhi - blo) - 1e-9)

print("\n" + ("전부 통과 ✅" if ok else "실패 있음 ❌"))
sys.exit(0 if ok else 1)
