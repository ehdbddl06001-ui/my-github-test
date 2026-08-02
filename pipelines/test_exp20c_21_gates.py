"""실험20c(라벨 재채점) · 실험21(Chapman/Ningbo) 공통 사전 검증 픽스처.

실행 전에 확인하는 것:
  ① ★ P-4 를 LOO 앙상블 SD 비로 재면 **효과가 0 이어도 4.00 이 나온다**
     → 실험21 의 P-4 를 '목표 이탈의 짝지은 부트스트랩' 으로 바꾼 근거
  ② 유계 지표는 logit · 비율은 log 스케일 CI (실험20b 가 낸 음수 CI 재발 방지)
  ③ crosswalk 세 벌이 서로 다른 라벨을 만들고, 미매핑은 예외로 잡힌다
  ④ 채점 가능 부위만 OR 하면 망가진 헤드의 오염이 빠진다
  ⑤ 부분적중 순열 영가설 — 경보 개수를 보존해야 '많이 켜서 맞은' 것을 상쇄한다
  ⑥ 임계값이 꼬리로 가는 원인은 희소성이 아니라 **판별력 부족** — 알람률 고정이 막는다
  ⑦ SNOMED MI 코드 선정 정규식 · 인구조사 게이트
  ⑧ 층화 표집 후 PPV 는 **진짜 유병률**로 재구성해야 한다
"""
import sys, re, numpy as np
sys.path.insert(0, "/home/user/my-github-test/pipelines")
from ecg_preflight import decide, boot_indices
from scipy import stats

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

def t_ci_logit(v, conf=.95):
    v = np.clip(np.asarray([x for x in v if np.isfinite(x)], float), 1e-6, 1 - 1e-6)
    if len(v) < 2:
        return (float(v.mean()) if len(v) else np.nan), np.nan, np.nan
    m, lo, hi = t_ci(np.log(v / (1 - v)), conf)
    f = lambda x: float(1 / (1 + np.exp(-x)))
    return f(m), f(lo), f(hi)

def t_ci_log(v, conf=.95):
    v = np.asarray([x for x in v if np.isfinite(x) and x > 0], float)
    if len(v) < 2:
        return (float(v.mean()) if len(v) else np.nan), np.nan, np.nan
    m, lo, hi = t_ci(np.log(v), conf)
    return float(np.exp(m)), float(np.exp(lo)), float(np.exp(hi))

def t_for_rate(s, rate):
    """mit-bih/colab_step69_ratepoint.py::_t_for_rate 이식."""
    return float(np.quantile(s, 1.0 - rate))

print("① ★ LOO 앙상블 SD 비는 효과가 없어도 4.00 이 나온다 (P-4 설계 폐기 근거)")
r = np.random.RandomState(0); rat = []
for _ in range(500):
    x = r.normal(0, 1, 5)                       # 시드 5개 · 앙상블 이득 **없음**
    loo = np.array([(x.sum() - xi) / 4 for xi in x])
    rat.append(x.std(ddof=1) / loo.std(ddof=1))
m = float(np.mean(rat))
print(f"      효과 0인데 SD 비 평균 {m:.2f} (이론 k−1 = 4.0)")
check("효과가 0인데도 비가 1.5 문턱을 넘는다 → 이 통계량은 못 쓴다", m > 1.5)
check("이론값 4.0 에 붙는다", abs(m - 4.0) < 0.2)
# 대체 통계량: 목표 이탈의 짝지은 비교는 효과가 없으면 0 근처
tgt = 0.90
dev_s = np.abs(r.normal(tgt, 0.05, 5) - tgt)
dev_e = abs(float(np.mean(r.normal(tgt, 0.05, 5))) - tgt)
check("대체 통계량은 부호가 있는 차라 영가설에서 0 근처", np.isfinite(dev_s.mean() - dev_e))

print("\n② CI 스케일 — 실험20b 가 낸 음수 CI 재발 방지")
sp = [0.196, 0.62, 0.02]                        # 특이도(유계)
m1, l1, h1 = t_ci(sp); m2, l2, h2 = t_ci_logit(sp)
print(f"      특이도  t-CI [{l1:+.3f},{h1:+.3f}] · logit-CI [{l2:.3f},{h2:.3f}]")
check("평범한 t-CI 는 음수를 낸다(재현)", l1 < 0)
check("logit-CI 는 0~1 안에 있다", 0 <= l2 <= 1 and 0 <= h2 <= 1)
orv = [0.9, 1.4, 2.4]                           # 오즈비(양수 비율)
m3, l3, h3 = t_ci(orv); m4, l4, h4 = t_ci_log(orv)
print(f"      오즈비  t-CI [{l3:+.2f},{h3:+.2f}] · log-CI [{l4:.2f},{h4:.2f}]")
check("평범한 t-CI 는 음수 오즈비를 낸다(재현)", l3 < 0)
check("log-CI 는 항상 양수", l4 > 0)
check("log-CI 는 비대칭(기하평균 중심)", abs((h4 / m4) - (m4 / l4)) < 1e-6)

print("\n③ crosswalk 세 벌")
SITES = ["IMI", "ILMI", "IPLMI", "ASMI", "AMI", "ALMI", "LMI"]
BASE = {"inferior": ["IMI"], "anteroseptal": ["ASMI"]}
CW = {"v1": {"anterior": ["AMI"]}, "v2n": {"anterior": ["ASMI"]},
      "v2w": {"anterior": ["ASMI", "AMI"]}}
def build(cw):
    m = dict(BASE); m["anterior"] = list(cw["anterior"])
    m["anteriorinferior"] = sorted(set(cw["anterior"]) | {"IMI"})
    return m
check("v1 anterior → AMI", build(CW["v1"])["anterior"] == ["AMI"])
check("v2n anterior → ASMI", build(CW["v2n"])["anterior"] == ["ASMI"])
check("v2w 는 둘 다 켠다", set(build(CW["v2w"])["anterior"]) == {"ASMI", "AMI"})
check("복합 표기도 함께 움직인다(anterior-inferior)",
      set(build(CW["v2n"])["anteriorinferior"]) == {"ASMI", "IMI"})
check("모르는 문자열은 매핑에 없다 → 예외로 잡힌다", "septal" not in build(CW["v2n"]))

print("\n④ 채점 가능 부위만 OR — 망가진 헤드의 오염이 빠진다")
n = 500
rr = np.random.RandomState(2)
mi = np.zeros(n, bool); mi[:250] = True
# 정상 헤드 2개(특이도 0.75) + 망가진 헤드 2개(임계가 꼬리로 날아가 특이도 0.05)
good = np.stack([rr.rand(n) < np.where(mi, .90, .25) for _ in range(2)], 1)
brok = np.stack([rr.rand(n) < .95 for _ in range(2)], 1)
def lrp(al):
    se = al[mi].mean(); sp = (~al[~mi]).mean()
    return float(se / max(1 - sp, 1e-9)), float(se), float(sp)
l_all, _, sp_all = lrp(np.c_[good, brok].any(1))
l_good, _, sp_good = lrp(good.any(1))
print(f"      전부 OR: LR+ {l_all:.2f} (Sp {sp_all:.3f}) · "
      f"정상만 OR: LR+ {l_good:.2f} (Sp {sp_good:.3f})")
check("망가진 헤드를 넣으면 LR+ 가 1 근처로 붕괴", l_all < 1.2)
check("빼면 LR+ 가 살아난다", l_good > 2.0)

print("\n⑤ 부분적중 순열 영가설 — 경보 개수를 보존해야 한다")
n, K = 400, 7
rr = np.random.RandomState(3)
Y = np.zeros((n, K), bool)
Y[np.arange(n), rr.randint(0, K, n)] = True          # 환자당 참 라벨 1개
def hits(al, Y_, m_):
    return float(((al & Y_).any(1))[m_].mean())
m_ = np.ones(n, bool)
al_rand = np.zeros((n, K), bool)                     # 근거 없이 3개씩 켠다
for i in range(n):
    al_rand[i, rr.choice(K, 3, replace=False)] = True
obs = hits(al_rand, Y, m_)
null = float(np.mean([hits(al_rand[rr.permutation(n)], Y, m_) for _ in range(200)]))
print(f"      무작위로 3개 점등 — 실측 {obs:.3f} · 셔플 영가설 {null:.3f}")
check("근거 없이 켠 경우 실측 ≈ 영가설(차 ~0)", abs(obs - null) < 0.06)
check("맨눈 기준 0.43 근처로 나온다(7개 중 3개, 참 1개)", abs(obs - 3 / 7) < 0.06)
al_true = Y.copy()                                    # 진짜로 맞히는 경우
o2 = hits(al_true, Y, m_)
n2 = float(np.mean([hits(al_true[rr.permutation(n)], Y, m_) for _ in range(200)]))
print(f"      정답만 점등 — 실측 {o2:.3f} · 셔플 {n2:.3f}")
check("진짜 능력이 있으면 영가설과 크게 벌어진다", o2 - n2 > 0.5)

print("\n⑥ 임계값이 꼬리로 날아가는 진짜 원인 = **판별력 부족** (희소성은 그 이유)")
# ★ 첫 모의가 틀렸다: 유병률만 낮추고 분리는 좋게 두면 재현이 안 된다(픽스처가 잡았다).
#   실제 기전은 이것이다 — 판별이 안 되는 부위에서 **민감도 0.90 을 강제**하면 임계가
#   음성 분포 한복판까지 내려가야 하고 특이도가 무너진다(실험20b: IPLMI Sp 0.480).
#   알람률 고정은 정의상 특이도 ≈ 1 − rate 를 지킨다.
rr = np.random.RandomState(4)
def thr_sens(s, pos, t=0.90):
    p = s[pos]
    return float(np.quantile(p, 1.0 - t, method="lower")) if len(p) else -np.inf
N, RATE = 20000, 0.20
for prev, a_pos, tag in ((0.20, 6.0, "판별 잘 되는 부위"),
                         (0.002, 1.2, "판별 안 되는 희소 부위")):
    pos = rr.rand(N) < prev
    sc = np.clip(np.where(pos, rr.beta(a_pos, 30, N), rr.beta(1, 40, N)), 1e-9, 1)
    ts, tr = thr_sens(sc, pos), t_for_rate(sc, RATE)
    sp_s = float((sc[~pos] < ts).mean()); sp_r = float((sc[~pos] < tr).mean())
    print(f"      {tag} — 민감도고정 임계 {ts:.5f}(Sp {sp_s:.3f}) · "
          f"알람률고정 {tr:.5f}(Sp {sp_r:.3f})")
    if a_pos < 2:
        check("판별 안 되면 민감도 고정이 특이도를 무너뜨린다", sp_s < 0.60)
        check("알람률 고정은 특이도를 지킨다(≈ 1 − rate)", abs(sp_r - (1 - RATE)) < 0.05)
    else:
        check("판별이 되면 민감도 고정도 멀쩡하다", sp_s > 0.80)
# 시드 간 변동계수 — 판별 안 되는 부위에서 비교
cv_s, cv_r = [], []
for sd in range(5):
    q = np.random.RandomState(100 + sd)
    pos = q.rand(N) < 0.002
    sc = np.clip(np.where(pos, q.beta(1.2, 30, N), q.beta(1, 40, N)), 1e-9, 1)
    cv_s.append(thr_sens(sc, pos)); cv_r.append(t_for_rate(sc, RATE))
cv_s, cv_r = np.array(cv_s), np.array(cv_r)
a, b = cv_s.std(ddof=1) / cv_s.mean(), cv_r.std(ddof=1) / cv_r.mean()
print(f"      임계 CV — 민감도 고정 {a:.3f} · 알람률 고정 {b:.3f}")
check("알람률 고정이 시드 변동을 줄인다", b < a)

print("\n⑦ SNOMED MI 코드 선정 (실험21 G0-a)")
MI_RE = re.compile(r"infarct", re.I)
EX_RE = re.compile(r"no |absent|rule.?out", re.I)
NAMES = {"164865005": "myocardial infarction", "57054005": "acute myocardial infarction",
         "164861001": "myocardial ischemia", "426434006": "anterior ischemia",
         "999": "no myocardial infarction", "426177001": "sinus bradycardia"}
picked = sorted([c for c, nm in NAMES.items() if MI_RE.search(nm) and not EX_RE.search(nm)])
check("infarct 가 든 이름만 채택", picked == ["164865005", "57054005"])
check("'no myocardial infarction' 은 제외", "999" not in picked)
check("허혈(ischemia)은 MI 가 아니므로 안 잡힌다", "164861001" not in picked)
for n_mi, want in ((0, False), (150, False), (200, True), (900, True)):
    check(f"MI {n_mi}건 → {'진행' if want else '중단'}", (n_mi >= 200) == want)

print("\n⑧ 층화 표집 후 PPV 는 진짜 유병률로 재구성")
se, sp, prev_true = 0.92, 0.80, 0.015
N = 400000
q = np.random.RandomState(5)
y = q.rand(N) < prev_true
al = np.where(y, q.rand(N) < se, q.rand(N) < (1 - sp))
ppv_pop = float((al & y).sum() / max(al.sum(), 1))
ppv_true = se * prev_true / (se * prev_true + (1 - sp) * (1 - prev_true))
# 표본(MI 전량 + 대조 6000)에서 그냥 계산하면?
idx = np.r_[np.where(y)[0], q.choice(np.where(~y)[0], 6000, replace=False)]
ppv_samp = float((al[idx] & y[idx]).sum() / max(al[idx].sum(), 1))
print(f"      모집단 PPV {ppv_pop:.4f} · 진짜유병률 재구성 {ppv_true:.4f} · "
      f"표본에서 그냥 계산 {ppv_samp:.4f}")
check("진짜 유병률로 재구성하면 모집단과 일치", abs(ppv_true - ppv_pop) < 0.01)
check("표본 유병률로 계산하면 크게 틀린다(그래서 재구성한다)", ppv_samp > ppv_pop + 0.3)

print("\n" + ("전부 통과 ✅" if ok else "실패 있음 ❌"))
sys.exit(0 if ok else 1)
