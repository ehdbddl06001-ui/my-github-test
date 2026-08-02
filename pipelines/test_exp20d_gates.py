"""실험20d(결합 점수 재채점 + Top-1 기준선) 사전 검증 픽스처.

실행 전에 확인하는 것:
  ① 결합 점수 max()는 두 헤드가 **다른 환자를 잡을 때만** 개별 최선을 넘는다
  ② 산술평균 집계는 약한 헤드에 끌려간다 — 실험20c 의 0.7178 이 그 구조인지
  ③ Top-1 다수결 기준선은 라벨 불균형을 그대로 이용하므로 순열보다 **엄격**하다
  ④ 순열 기준선은 점수 행을 셔플해도 라벨 분포를 보존한다
  ⑤ SCORE_MASK 를 한 곳에서 정의하면 모든 집계가 같은 부위를 쓴다(3중 오염 재발 방지)
"""
import sys, numpy as np
sys.path.insert(0, "/home/user/my-github-test/pipelines")
from ecg_preflight import decide
from scipy import stats
from sklearn.metrics import roc_auc_score

ok = True
def check(n, c):
    global ok
    print(("  ✅ " if c else "  ❌ ") + n); ok = ok and bool(c)

def t_ci(v, conf=.95):
    v = np.asarray([x for x in v if np.isfinite(x)], float); n = len(v)
    m = float(v.mean()) if n else float("nan")
    if n < 2:
        return m, np.nan, np.nan
    h = float(stats.t.ppf(.5 + conf / 2, n - 1) * v.std(ddof=1) / np.sqrt(n))
    return m, m - h, m + h

def auc_(y, s):
    return float(roc_auc_score(y, s)) if y.any() and (~y).any() else np.nan

print("① 결합 max() 는 두 헤드가 다른 환자를 잡을 때만 이긴다")
n, npos = 600, 200
r = np.random.RandomState(0)
y = np.zeros(n, bool); y[:npos] = True

# (a) 상보적: 양성의 앞 절반은 헤드A 가, 뒤 절반은 헤드B 가 잡는다
a = r.normal(0, 1, n).copy(); b = r.normal(0, 1, n).copy()
a[:npos // 2] += 2.5
b[npos // 2:npos] += 2.5
comb = np.maximum(a, b)
print(f"      상보적 — A {auc_(y,a):.3f} · B {auc_(y,b):.3f} · 결합 {auc_(y,comb):.3f}")
check("(a) 결합이 개별 최선을 넘는다", auc_(y, comb) > max(auc_(y, a), auc_(y, b)) + 0.05)

# (b) 중복: 헤드B 가 헤드A 의 열화판. 결합해도 A 를 크게 못 넘는다
a2 = r.normal(0, 1, n); a2[y] += 2.0
b2 = a2 * 0.5 + r.normal(0, 1, n) * 0.5
c2 = np.maximum(a2, b2)
print(f"      중복적 — A {auc_(y,a2):.3f} · B {auc_(y,b2):.3f} · 결합 {auc_(y,c2):.3f}")
check("(b) 중복이면 결합이 개별 최선을 크게 못 넘는다",
      auc_(y, c2) - max(auc_(y, a2), auc_(y, b2)) < 0.05)
check("(b) 결합이 약한 헤드보다는 낫다", auc_(y, c2) > auc_(y, b2))

print("\n② 산술평균 집계는 약한 헤드에 끌려간다 (실험20c 0.7178 의 구조)")
strong, weak = 0.8660, 0.5684
print(f"      강 {strong} · 약 {weak} → 산술평균 {(strong+weak)/2:.4f} "
      f"(실험20c 가 보고한 0.7178)")
check("산술평균은 두 값의 정확히 중간", abs((strong + weak) / 2 - 0.7172) < 0.001)
check("산술평균은 강한 헤드보다 항상 낮다", (strong + weak) / 2 < strong)
check("문턱 0.05 를 자동으로 넘긴다 — 약한 헤드가 있으면 P-2 는 구조적으로 기각된다",
      strong - (strong + weak) / 2 > 0.05)

print("\n③ Top-1 기준선 두 개 — 다수결이 더 엄격하다")
K = 3
rr = np.random.RandomState(1)
NP_ = 300
Y = np.zeros((NP_, K), bool)
# 불균형 라벨: 부위0 을 절반이 갖는다
grp = rr.choice(K, NP_, p=[0.5, 0.2, 0.3])
Y[np.arange(NP_), grp] = True
mi = np.ones(NP_, bool)

def top1(S, Y_, m_):
    pick = np.argmax(S, axis=1)
    return float(np.array([Y_[i, pick[i]] for i in range(len(pick))])[m_].mean())

S_rand = rr.rand(NP_, K)                      # 정보 없는 점수
maj_j = int(np.argmax(Y[mi].sum(0)))
maj = float(Y[mi][:, maj_j].mean())
perm = float(np.mean([top1(S_rand[rr.permutation(NP_)], Y, mi) for _ in range(300)]))
print(f"      다수결 {maj:.3f} · 순열 {perm:.3f} · 무정보 점수 실측 {top1(S_rand,Y,mi):.3f}")
check("다수결 기준선이 순열보다 높다(더 엄격)", maj > perm)
check("순열 ≈ 1/K (라벨 불균형을 못 쓴다)", abs(perm - 1 / K) < 0.06)
check("무정보 점수는 순열과 같은 수준", abs(top1(S_rand, Y, mi) - perm) < 0.08)

S_good = Y.astype(float) + rr.rand(NP_, K) * 0.3    # 진짜 실력
print(f"      실력 있는 점수 {top1(S_good,Y,mi):.3f}")
check("실력이 있으면 다수결도 넘는다", top1(S_good, Y, mi) > maj + 0.2)

print("\n④ 순열은 점수 행을 셔플해도 라벨 분포를 보존한다")
before = Y[mi].sum(0)
_ = top1(S_rand[rr.permutation(NP_)], Y, mi)
check("라벨 행렬은 안 건드린다", (Y[mi].sum(0) == before).all())

print("\n⑤ SCORE_MASK 를 한 곳에서 정의 — 3중 오염 재발 방지")
SITES = ["IMI", "ILMI", "IPLMI", "ASMI", "AMI", "ALMI", "LMI"]
npat = {"IMI": 44, "ILMI": 25, "IPLMI": 9, "ASMI": 58, "AMI": 1, "ALMI": 19, "LMI": 1}
GMIN = 20
MASK = np.array([npat[s] >= GMIN for s in SITES])
sel = [s for s, m in zip(SITES, MASK) if m]
check("v2-narrow 채점 대상은 IMI·ILMI·ASMI", sel == ["IMI", "ILMI", "ASMI"])
# 세 집계가 전부 같은 마스크를 받아야 한다
def agg_site(mask): return [s for s, m in zip(SITES, mask) if m]
def agg_or(mask):   return [s for s, m in zip(SITES, mask) if m]
def agg_cv(mask):   return [s for s, m in zip(SITES, mask) if m]
check("부위 채점·OR·CV 세 집계가 같은 부위를 본다",
      agg_site(MASK) == agg_or(MASK) == agg_cv(MASK))
# 실험20c 에서 실제로 벌어진 일: OR·CV 가 마스크를 안 받았다
check("마스크를 안 주면 7부위가 들어간다(실험20c 의 버그 재현)",
      len(agg_or(np.ones(7, bool))) == 7)

print("\n" + ("전부 통과 ✅" if ok else "실패 있음 ❌"))
sys.exit(0 if ok else 1)
