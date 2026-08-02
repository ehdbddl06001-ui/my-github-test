"""실험20(PTBDB 외부검증) 사전 검증 픽스처.

실행 전에 확인하는 것:
  ① PTBDB 국소화 문자열 정규화·매핑 (표기 흔들림 흡수 · 미매핑은 예외)
  ② 1000Hz → 100Hz 리샘플 후에도 아인트호벤 항등식이 서는가
  ③ 진폭 스케일 가드
  ④ 환자 단위 집계(1인 다레코드)
  ⑤ 베이즈 PPV — 특이도가 유지되면 예측=관측, 무너지면 관측<예측
  ⑥ P-3 방향(진구성 − 급성)
"""
import sys, re, numpy as np
sys.path.insert(0, "/home/user/my-github-test/pipelines")
from ecg_preflight import decide, assert_lead_order
from scipy.signal import resample_poly
from scipy import stats

ok = True
def check(n, c):
    global ok
    print(("  ✅ " if c else "  ❌ ") + n); ok = ok and bool(c)

def norm_loc(s):
    return re.sub(r"[^a-z]", "", str(s).strip().lower())

def split_locs(s):
    """통짜 정규화 — 구분자로 쪼개지 않는다('n/a' 가 'n'+'a' 로 갈라지는 것 방지)."""
    return [norm_loc(s)]

LOC_MAP = {"anterior": ["AMI"], "anteroseptal": ["ASMI"], "anteriorseptal": ["ASMI"],
           "anterolateral": ["ALMI"], "anteriorlateral": ["ALMI"],
           "anteroapicallateral": ["ALMI"], "anteroseptallateral": ["ASMI"],
           "anteroseptolateral": ["ASMI"], "inferior": ["IMI"],
           "inferolateral": ["ILMI"], "inferiorlateral": ["ILMI"],
           "inferoposterolateral": ["IPLMI"], "inferoposterlateral": ["IPLMI"],
           "inferiorposteriorlateral": ["IPLMI"], "lateral": ["LMI"],
           # 2026-08-02 실제 PTBDB 헤더에서 게이트가 잡아낸 것들
           "inferolatera": ["ILMI"], "anteriorinferior": ["AMI", "IMI"],
           "anterioranterior": ["AMI"], "inferoposteriorinferior": ["IMI"]}
LOC_DROP = {"no", "nein", "unknown", "", "none", "na", "inferoposterior",
            "inferiorposterior", "posterior", "posterolateral", "posteriorlateral"}

def sites_of(v):
    out = []
    for k in split_locs(v):
        out += LOC_MAP.get(k, [])
    return sorted(set(out))

print("① 국소화 문자열 매핑")
for raw, want in [("infero-lateral", ["ILMI"]), ("Infero-Lateral ", ["ILMI"]),
                  ("antero-septal", ["ASMI"]), ("infero-poster-lateral", ["IPLMI"]),
                  ("anterior", ["AMI"]), ("inferior", ["IMI"]), ("lateral", ["LMI"])]:
    check(f"'{raw}' → {want}", sites_of(raw) == want)

print("\n①-b 실제 헤더에서 나온 것들 (게이트가 잡아 명시한 5개)")
check("'infero-latera'(원본 표기 누락) → ILMI", sites_of("infero-latera") == ["ILMI"])
check("'anterior-inferior' → AMI+IMI (다중 부위)",
      sites_of("anterior-inferior") == ["AMI", "IMI"])
check("'anterior-anterior'(중복 기재) → AMI", sites_of("anterior-anterior") == ["AMI"])
check("'infero-posterior-inferior' → IMI (후벽은 PTB-XL 제외 부위)",
      sites_of("infero-posterior-inferior") == ["IMI"])
check("'n/a' → 버림", norm_loc("n/a") in LOC_DROP and sites_of("n/a") == [])

print("\n①-c 통짜 정규화 — 구분자로 쪼개지 않는다")
check("'n/a' 가 'n'+'a' 로 갈라지지 않는다", split_locs("n/a") == ["na"])
check("'infero-lateral' 이 갈라지지 않는다", split_locs("infero-lateral") == ["inferolateral"])
# 'inferior, lateral' 은 통짜로 'inferiorlateral' 이 되어 이미 ILMI 로 매핑된다(의도된 동작)
check("'inferior, lateral' → 통짜 정규화로 ILMI", sites_of("inferior, lateral") == ["ILMI"])
check("정말 모르는 복합 형태는 미매핑으로 잡혀 게이트가 선다",
      sites_of("septal, apical") == [] and norm_loc("septal, apical") not in LOC_DROP)

for raw in ("no", "unknown", "", "posterior", "infero-posterior", "n/a"):
    check(f"'{raw or '(빈칸)'}' 명시적 제외", all(k in LOC_DROP for k in split_locs(raw)))
newk = [k for k in ("antero-basal", "septal")
        if norm_loc(k) not in LOC_MAP and norm_loc(k) not in LOC_DROP]
check("모르는 문자열은 미매핑으로 잡힌다(추측 금지)", set(newk) == {"antero-basal", "septal"})

print("\n② 리샘플 후 유도 순서")
rs = np.random.RandomState(0); n, T = 20, 11000
t = np.linspace(0, 11, T)
I = np.stack([np.sin(2 * np.pi * 1.2 * t + rs.rand()) for _ in range(n)])
II = np.stack([np.sin(2 * np.pi * 1.2 * t + rs.rand()) * 1.4 for _ in range(n)])
V = [rs.randn(n, T) * .1 for _ in range(6)]
X1k = np.stack([I, II, II - I, -(I + II) / 2, I - II / 2, II - I / 2] + V, axis=2)
seg = resample_poly(X1k[:, 1000:11000, :], 1, 10, axis=1)
check("리샘플 후 (n, 1000, 12)", seg.shape == (n, 1000, 12))
check("리샘플 후 항등식 통과", assert_lead_order(seg.astype("float32"))["ok"])
bad = resample_poly(X1k[:, 1000:11000, [1, 0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]], 1, 10, axis=1)
try:
    assert_lead_order(bad.astype("float32")); check("I·II 뒤바뀜 탐지", False)
except ValueError:
    check("I·II 뒤바뀜 탐지", True)

print("\n③ 진폭 스케일 가드")
for r, want in ((1.0, True), (1.8, True), (2.5, False), (0.3, False)):
    check(f"배수 {r} → {'통과' if want else '중단'}", (0.5 <= r <= 2.0) == want)

print("\n④ 환자 단위 집계")
PT = np.array(["p1", "p1", "p2", "p3", "p3", "p3"])
score = np.array([.9, .7, .1, .4, .6, .8]); y = np.array([1, 1, 0, 0, 1, 0], bool)
PTS = sorted(set(PT)); PIDX = {p: np.where(PT == p)[0] for p in PTS}
s = np.array([score[PIDX[p]].mean() for p in PTS])
lab = np.array([y[PIDX[p]].any() for p in PTS])
check("환자 3명으로 접힌다", len(s) == 3)
check("예측은 평균(p1 = 0.8)", abs(s[0] - 0.8) < 1e-9)
check("라벨은 any(p3 = True)", bool(lab[2]))

print("\n⑤ 베이즈 PPV")
se, sp = 0.90, 0.85
for prev in (0.12, 0.51):
    pred = se * prev / (se * prev + (1 - sp) * (1 - prev))
    N = 200000; r2 = np.random.RandomState(1)
    yy = r2.rand(N) < prev
    al = np.where(yy, r2.rand(N) < se, r2.rand(N) < (1 - sp))
    obs = (al & yy).sum() / max(al.sum(), 1)
    print(f"      유병률 {prev:.2f} → 예측 {pred:.3f} · 모의 {obs:.3f}")
    check(f"유병률 {prev:.2f} 에서 예측 = 관측", abs(pred - obs) < 0.01)
pred = se * .51 / (se * .51 + .15 * .49)
obs = se * .51 / (se * .51 + .30 * .49)
print(f"      특이도 0.85→0.70 → 관측 {obs:.3f} vs 예측 {pred:.3f} ({obs-pred:+.3f})")
check("특이도 붕괴는 관측<예측 으로 잡힌다", obs < pred - 0.05)

print("\n⑥ P-3 방향 (진구성 − 급성 < 0.10 이면 지지)")
def t_ci(v):
    v = np.asarray(v, float); m = float(v.mean()); sd = float(v.std(ddof=1))
    h = float(stats.t.ppf(.975, len(v) - 1) * sd / np.sqrt(len(v)))
    return m - h, m + h
check("급성이 조금만 나쁘면 지지", decide(*t_ci([.02, .03, .01]), 0.10, "<") is True)
check("급성이 크게 나쁘면 기각", decide(*t_ci([.25, .28, .22]), 0.10, "<") is False)

print("\n" + ("전부 통과 ✅" if ok else "실패 있음 ❌"))
sys.exit(0 if ok else 1)
