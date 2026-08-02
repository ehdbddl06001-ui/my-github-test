"""실험20b(환자 단위 집계 + AMI 라벨 정합) 사전 검증 픽스처.

실행 전에 확인하는 것:
  ① 환자 단위 집계 — 예측=평균 · 라벨=any (다중라벨 7부위)
  ② 내부 동결 임계값이 목표 민감도를 실제로 낸다
  ③ OR 합성 — 독립 가정 상한 vs 상관이 있을 때의 실측
  ④ P-2 — 절대 ΔSp 는 천장에 막힌다 → 위양성 **오즈비**로 재야 한다
  ⑤ ★ 시드 CI vs 환자 부트스트랩 CI — 소집단에서 어느 쪽이 넓은가(실험20 의 교훈)
  ⑥ P-4/P-5 — 라벨 정의 불일치를 심어놓고 잡히는지, 그리고 **헤드 세기 교란**에
     이중차분이 안 속는지
"""
import sys, numpy as np
sys.path.insert(0, "/home/user/my-github-test/pipelines")
from ecg_preflight import decide, boot_indices
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

SITES = ["IMI", "ILMI", "IPLMI", "ASMI", "AMI", "ALMI", "LMI"]

print("① 환자 단위 집계 (다중라벨)")
PT = np.array(["p1", "p1", "p2", "p3", "p3"])
sc = np.array([[.9, .1], [.7, .3], [.2, .2], [.4, .8], [.6, .9]])
y = np.array([[1, 0], [1, 0], [0, 0], [0, 1], [1, 1]], bool)
PTS = sorted(set(PT)); PIDX = {p: np.where(PT == p)[0] for p in PTS}
S = np.stack([np.array([sc[PIDX[p], j].mean() for p in PTS]) for j in range(2)], 1)
Y = np.stack([np.array([y[PIDX[p], j].any() for p in PTS]) for j in range(2)], 1)
check("환자 3명 × 부위 2", S.shape == (3, 2) and Y.shape == (3, 2))
check("예측은 평균 (p1 부위0 = 0.8)", abs(S[0, 0] - 0.8) < 1e-9)
check("라벨은 any (p3 부위0 = True)", bool(Y[2, 0]))
check("MI 환자 = 어느 부위든 양성", list(Y.any(1)) == [True, False, True])

print("\n② 내부 동결 임계값이 목표 민감도를 낸다")
def thr_sens(score, pos, t=0.90):
    p = score[pos]
    return float(np.quantile(p, 1.0 - t, method="lower")) if len(p) else -np.inf
r = np.random.RandomState(0)
pos = np.zeros(2000, bool); pos[:400] = True
s_ = np.where(pos, r.normal(1.0, 1, 2000), r.normal(0, 1, 2000))
th = thr_sens(s_, pos, 0.90)
se = (s_[pos] >= th).mean()
print(f"      임계 {th:+.3f} → 내부 민감도 {se:.3f}")
check("목표 0.90 을 만족(>=)", se >= 0.90 - 1e-9)
check("특이도는 1 미만(실제로 자른다)", (s_[~pos] < th).mean() < 1.0)

print("\n③ OR 합성 — 독립 가정 상한은 상관이 있으면 과장된다")
n = 400
def or_spec(F):
    """F: (n, k) 위양성 여부 → OR 특이도."""
    return float((~F.any(1)).mean())
r = np.random.RandomState(1)
p_fp = np.array([.28, .24, .28, .57, .36, .60, .60])
indep_F = np.stack([r.rand(n) < q for q in p_fp], 1)          # 완전 독립
bound = 1 - np.prod(1 - p_fp)
print(f"      독립 상한 {bound:.3f} · 독립 모의 {1-or_spec(indep_F):.3f}")
check("독립일 때 상한 ≈ 실측", abs(bound - (1 - or_spec(indep_F))) < 0.05)
u = r.rand(n)                                                  # 완전 상관(공통 잠재)
corr_F = np.stack([u < q for q in p_fp], 1)
print(f"      완전 상관 실측 {1-or_spec(corr_F):.3f}  (상한 {bound:.3f})")
check("상관이 있으면 실측 << 상한", (1 - or_spec(corr_F)) < bound - 0.20)
check("완전 상관이면 최댓값 부위 하나로 수렴", abs((1 - or_spec(corr_F)) - p_fp.max()) < 0.06)

print("\n④ P-2 — 절대 ΔSp 는 천장에 막힌다. 오즈비로 재야 한다")
# ★ 이 픽스처가 설계 결함을 잡았다: 특이도가 0 근처면 아무리 큰 효과도 ΔSp 로는
#   작게 나온다(P-1 이 강하게 지지될수록 P-2 가 구조적으로 불가능해진다).
#   실험22 에서 위험비 → 오즈비로 바꾼 것과 **같은 종류의 버그**다.
KEEP = [j for j in range(7) if j != 5]        # ALMI(0.60) 제외
def fp_or(F, cols):
    a_all = float(F.any(1).mean()); a_sub = float(F[:, cols].any(1).mean())
    return (a_all / max(1 - a_all, 1e-9)) / max(a_sub / max(1 - a_sub, 1e-9), 1e-9)
for tag, F in (("독립", indep_F), ("상관", corr_F)):
    d = or_spec(F[:, KEEP]) - or_spec(F)
    o = fp_or(F, KEEP)
    print(f"      {tag}: ΔSp {d:+.3f} · 위양성 오즈비 {o:.2f}")
    check(f"{tag} — 부위를 빼면 특이도가 안 내려간다", d >= -1e-9)
check("천장 문제 재현 — 독립인데도 ΔSp 는 0.05 미만",
      or_spec(indep_F[:, KEEP]) - or_spec(indep_F) < 0.05)
check("오즈비는 천장에 안 막힌다(독립 케이스를 잡아낸다)", fp_or(indep_F, KEEP) >= 1.5)
check("완전 상관이면 오즈비도 1 근처(효과 없음을 옳게 말한다)",
      abs(fp_or(corr_F, KEEP) - 1.0) < 0.1)

print("\n⑤ ★ 시드 CI vs 환자 부트스트랩 CI — 실험20 이 속은 자리")
# 시드 3개는 거의 같은 값을 내지만(재학습 잡음 작음) 환자가 적으면 표집 잡음은 크다
def auc_sub(n_pos, seed):
    rr = np.random.RandomState(seed)
    neg = rr.normal(0, 1, 200)
    pos = rr.normal(1.2, 1, n_pos)
    yy = np.r_[np.ones(n_pos, bool), np.zeros(200, bool)]
    return float(roc_auc_score(yy, np.r_[pos, neg])), np.r_[pos, neg], yy
widths = {}
for n_pos in (2, 40):
    seeds = [auc_sub(n_pos, 100)[0] + d for d in (-0.004, 0.0, 0.004)]  # 미미한 시드 잡음
    _, sc2, yy = auc_sub(n_pos, 100)
    m, lo, hi = t_ci(seeds)
    bs = []
    for ix in boot_indices(len(yy), 400, 0):
        yb, sb = yy[ix], sc2[ix]
        if yb.any() and (~yb).any():
            bs.append(roc_auc_score(yb, sb))
    blo, bhi = np.percentile(bs, [2.5, 97.5])
    print(f"      양성 {n_pos:>2}명 — 시드폭 {hi-lo:.3f} · 환자부트폭 {bhi-blo:.3f}")
    check(f"양성 {n_pos}명: 환자 표집 쪽이 더 넓다", (bhi - blo) > (hi - lo))
    widths[n_pos] = bhi - blo
check(f"양성이 적을수록 부트폭이 커진다 ({widths[2]:.3f} > {widths[40]:.3f})",
      widths[2] > widths[40])

print("\n⑥ P-4/P-5 — 라벨 정의 불일치를 심어놓고 잡히는가")
def make(n_grp, n_neg, gap_asmi, gap_ami, head_bonus, seed):
    """gap_* = 그 헤드가 그룹을 대조군보다 얼마나 높게 주나. head_bonus 는 ASMI 헤드가
    **전반적으로** 잘하는 정도(교란). 이중차분은 여기 안 속아야 한다."""
    rr = np.random.RandomState(seed)
    out = {}
    for head, g in (("ASMI", gap_asmi + head_bonus), ("AMI", gap_ami)):
        pos = rr.normal(g, 1, n_grp); neg = rr.normal(0, 1, n_neg)
        yy = np.r_[np.ones(n_grp, bool), np.zeros(n_neg, bool)]
        out[head] = float(roc_auc_score(yy, np.r_[pos, neg]))
    return out

def gaps(gap_a_ant, gap_m_ant, gap_a_inf, gap_m_inf, bonus):
    ant = [make(30, 100, gap_a_ant, gap_m_ant, bonus, s) for s in (1, 2, 3)]
    inf = [make(44, 100, gap_a_inf, gap_m_inf, bonus, s) for s in (4, 5, 6)]
    ga = [a["ASMI"] - a["AMI"] for a in ant]
    gi = [i["ASMI"] - i["AMI"] for i in inf]
    return ga, gi

# (a) 진짜 라벨 불일치: 'anterior' 를 ASMI 헤드가 훨씬 잘 잡는다. 헤드 보너스 없음
ga, gi = gaps(1.4, 0.3, 0.2, 1.4, 0.0)
m4, lo4, hi4 = t_ci(ga)
did = [ga[i] - gi[i] for i in range(3)]
m5, lo5, hi5 = t_ci(did)
print(f"      (a) 불일치 심음 — P-4 {m4:+.3f} [{lo4:+.3f},{hi4:+.3f}] · "
      f"DiD {m5:+.3f} [{lo5:+.3f},{hi5:+.3f}]")
check("(a) P-4 지지", decide(lo4, hi4, 0.05, ">") is True)
check("(a) P-5(이중차분) 지지", decide(lo5, hi5, 0.05, ">") is True)

# (b) 교란만: ASMI 헤드가 전반적으로 세다. 라벨 불일치는 **없다**
ga, gi = gaps(0.5, 0.5, 0.5, 0.5, 1.2)
m4, lo4, hi4 = t_ci(ga)
did = [ga[i] - gi[i] for i in range(3)]
m5, lo5, hi5 = t_ci(did)
print(f"      (b) 헤드 보너스만 — P-4 {m4:+.3f} · DiD {m5:+.3f} [{lo5:+.3f},{hi5:+.3f}]")
check("(b) P-4 는 속는다(그래서 단독으로 못 쓴다)", m4 > 0.05)
check("(b) P-5 이중차분은 안 속는다", decide(lo5, hi5, 0.05, ">") is not True)

print("\n⑥-b 그룹 순수화 — 다른 전벽 변종이 섞인 환자는 뺀다")
SITESET = {"p1": {"AMI"}, "p2": {"AMI", "ASMI"}, "p3": {"AMI", "IMI"}, "p4": {"IMI"}}
raw = {"p1": "anterior", "p2": "anterior", "p3": "anterior", "p4": "inferior"}
pure_ant = [p for p in SITESET if raw[p] == "anterior" and SITESET[p] == {"AMI"}]
check("ASMI 가 함께 적힌 p2 는 빠진다", "p2" not in pure_ant)
check("IMI 가 함께 적힌 p3 도 빠진다", "p3" not in pure_ant)
check("순수 p1 만 남는다", pure_ant == ["p1"])

print("\n⑦ GMIN_SUB — 부분군 최소 n (실험20 이 빠뜨린 관문)")
GMIN_SUB = 20
for n_, want in ((2, False), (19, False), (20, True), (44, True)):
    check(f"부분군 {n_}명 → {'채점' if want else '제외'}", (n_ >= GMIN_SUB) == want)

print("\n" + ("전부 통과 ✅" if ok else "실패 있음 ❌"))
sys.exit(0 if ok else 1)
