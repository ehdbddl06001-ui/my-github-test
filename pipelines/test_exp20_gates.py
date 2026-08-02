"""실험20(PTBDB 외부검증) 사전 검증 픽스처.

실행 전에 확인하는 것:
  ① PTBDB 국소화 문자열 정규화·매핑 (표기 흔들림 흡수 · 미매핑은 예외)
  ② 1000Hz → 100Hz 리샘플 후에도 아인트호벤 항등식이 서는가
  ③ 진폭 스케일 가드
  ④ 환자 단위 집계(1인 다레코드)
  ⑤ 베이즈 PPV — 특이도가 유지되면 예측=관측, 무너지면 관측<예측
  ⑥ P-3 방향(진구성 − 급성)
  ⑦ 신호 파일을 **헤더에서** 정한다 (확장자 추측 금지 — .xyz 누락 사고)
  ⑧ wfdb 반환 열 순서를 가정하지 않고 이름으로 다시 세운다
  ⑨ 전처리 0건이면 사유를 요약해 죽는다 (np.stack([]) 로 끝나지 않는다)
  ⑩ 대역 정합 사다리 — DC 오프셋 / 저주파 흔들림 / 진짜 이득차 를 구분해 대처한다
  ⑪ 보정이 선형이라 아인트호벤 항등식이 보존된다
  ⑫ 잘린 다운로드를 예상 바이트로 잡는다
"""
import sys, os, re, numpy as np
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

print("\n⑦ 신호 파일 결정 — 확장자를 추측하지 않는다")
# 2026-08-02 사고 재발 방지. PTBDB 한 레코드는 12유도와 Frank 3유도(vx·vy·vz)가
# **다른 파일**에 있고 헤더가 둘 다 가리킨다. `.dat` 만 받으면 rdsamp 가 전 레코드
# 실패 → X 가 비어 np.stack([]) 이 터졌다.
ORDER = ["i", "ii", "iii", "avr", "avl", "avf", "v1", "v2", "v3", "v4", "v5", "v6"]

class FakeHdr:
    def __init__(self, sig_name, file_name):
        self.sig_name, self.file_name = sig_name, file_name

PTBDB_HDR = FakeHdr(
    ORDER + ["vx", "vy", "vz"],
    ["s0010_re.dat"] * 12 + ["s0010_re.xyz"] * 3)

def rec_files(rec, hdr, all_files=False):
    names = [s.lower() for s in hdr.sig_name]
    miss = [nm for nm in ORDER if nm not in names]
    if miss:
        raise RuntimeError(f"{rec}: 12유도 중 {miss} 가 헤더에 없다")
    want = sorted(set(hdr.file_name) if all_files
                  else {hdr.file_name[names.index(nm)] for nm in ORDER})
    d = os.path.dirname(rec)
    return [(os.path.join(d, f) if d else f) for f in want]

r12 = rec_files("patient001/s0010_re", PTBDB_HDR)
rall = rec_files("patient001/s0010_re", PTBDB_HDR, all_files=True)
print(f"      12유도분 {r12}")
print(f"      헤더 전체 {rall}")
check("12유도분은 .dat 하나", r12 == ["patient001/s0010_re.dat"])
check("헤더 전체는 .xyz 도 포함(카나리아 2차 시도용)",
      rall == ["patient001/s0010_re.dat", "patient001/s0010_re.xyz"])
check("디렉터리가 붙는다(중첩 경로)", all(x.startswith("patient001/") for x in rall))
# 12유도가 두 파일에 흩어진 가정 — 그래도 헤더가 시키는 대로 둘 다 받아야 한다
SPLIT = FakeHdr(ORDER + ["vx"], ["a.dat"] * 6 + ["b.dat"] * 6 + ["c.xyz"])
check("12유도가 두 파일에 나뉘면 둘 다 집는다",
      rec_files("p/s", SPLIT) == ["p/a.dat", "p/b.dat"])
try:
    rec_files("p/s", FakeHdr(["i", "ii"], ["a.dat"] * 2)); check("유도 누락은 예외", False)
except RuntimeError:
    check("12유도가 헤더에 없으면 예외", True)

print("\n⑧ 반환 열 순서를 가정하지 않는다")
# wfdb 가 channels 를 어떤 순서로 돌려주든 **이름으로** 다시 세운다
got = ["v1", "i", "avf", "ii", "iii", "avr", "avl", "v2", "v3", "v4", "v5", "v6"]
sig = np.tile(np.arange(len(got), dtype="float32"), (5, 1))   # 열 j = 값 j
out = sig[:, [got.index(nm) for nm in ORDER]]
check("셔플된 반환을 ORDER 로 되돌린다",
      [got[int(v)] for v in out[0]] == ORDER)

print("\n⑨ 0건이면 사유를 요약해 죽는다")
from collections import Counter
def summarize(bad, n_rec):
    cnt = Counter(w for _, w in bad)
    return (f"전처리 결과가 0건이다 (실패 {len(bad)}/{n_rec}건). 사유 상위:\n"
            + "\n".join(f"    {n:>5}건  {w}" for w, n in cnt.most_common(8)))
msg = summarize([(f"r{i}", "FileNotFoundError: s0010_re.xyz") for i in range(549)], 549)
print("      " + msg.replace("\n", "\n      "))
check("실패 건수가 드러난다", "549/549" in msg)
check("사유가 드러난다(np.stack 만 뜨지 않는다)", "FileNotFoundError" in msg)
mix = [("a", "짧음")] * 3 + [("b", "NaN")] * 7
check("여러 사유는 많은 순으로", summarize(mix, 10).index("NaN") < summarize(mix, 10).index("짧음"))

print("\n⑩ 대역 정합 사다리 — 진단 → 최소 보정 → 검증")
# 2026-08-02: PTBDB 는 DC 결합(0~1kHz), PTB-XL 은 아니다. pooled std 비가 4.67 로
# 게이트가 섰다. 초과분 √(b²−a²) 가 12유도에서 0.80~1.32 로 평평했고 흉부/사지
# 진폭비가 1.94 → 0.82 로 뒤집혔다 = 생리 신호가 아닌 공통 가산 성분.
from scipy.signal import butter, filtfilt
FS_OUT = 100

def decomp(S):
    return dict(within=np.median(S.std(axis=1), axis=0),
                offset=S.mean(axis=1).std(axis=0))

def demean(X):
    return (X - X.mean(axis=1, keepdims=True)).astype("float32")

def hp(X, fc, order=3):
    b, a = butter(order, fc / (FS_OUT / 2), btype="high")
    return filtfilt(b, a, X, axis=1).astype("float32")

LADDER = [("원본", lambda X: X), ("레코드별 평균 제거", demean),
          ("0.5Hz 0위상 고역통과", lambda X: hp(demean(X), 0.5))]

OFF_THR = 0.25
def climb(XL, DB):
    """진폭비 [0.5,2.0] **이고** DC 오프셋 <= OFF_THR **이고** 학습쪽 무영향(<10%).

    ★ 오프셋 조건이 없으면 사다리가 '원본' 에서 멈춘다 — 표준편차는 평균을 빼고
      재므로 레코드별 DC 오프셋에 눈이 멀기 때문이다. 모델은 안 그렇다.
    """
    d0 = decomp(XL)
    for name, fn in LADDER:
        d = decomp(fn(DB))
        r = float(np.nanmedian(d["within"] / d0["within"]))
        r_off = float(np.median(d["offset"]) / np.median(d0["within"]))
        noop = float(np.nanmax(np.abs(decomp(fn(XL))["within"] - d0["within"]) / d0["within"]))
        if 0.5 <= r <= 2.0 and r_off <= OFF_THR and noop < 0.10:
            return name, r
    return None, None

r3 = np.random.RandomState(7)
T = 1000
tt = np.arange(T) / FS_OUT
def synth(n, amp):                      # 사지 작고 흉부 큰 '생리적' 모의 신호
    base = np.stack([r3.randn(n, T) * a for a in amp], axis=2)
    return base.astype("float32")
AMP = [.15] * 6 + [.30] * 6
XL = synth(120, AMP)

check("보정 불필요하면 '원본' 에서 멈춘다", climb(XL, synth(120, AMP))[0] == "원본")
check("표준편차만 보면 DC 오프셋에 눈이 먼다(그래서 오프셋 조건이 필요)",
      abs(float(np.median(decomp(XL + 0.9)["within"] - decomp(XL)["within"]))) < 1e-6)

# (a) 레코드별 DC 오프셋만 얹은 경우 → 평균 제거로 끝나야 한다
off = XL.copy() + r3.randn(120, 1, 12).astype("float32") * 0.9
nm, r = climb(XL, off)
print(f"      DC 오프셋만 → {nm} (비 {r:.2f})")
check("DC 오프셋은 평균 제거 단계에서 잡힌다", nm == "레코드별 평균 제거")

# (b) 레코드 안 저주파 흔들림 → 평균 제거로는 안 되고 고역통과까지 가야 한다
wob = XL + (0.9 * np.sin(2 * np.pi * 0.15 * tt + r3.rand(120, 1))
            )[:, :, None].astype("float32")
nm, r = climb(XL, wob)
print(f"      0.15Hz 흔들림 → {nm} (비 {r:.2f})")
check("저주파 흔들림은 고역통과까지 올라간다", nm == "0.5Hz 0위상 고역통과")
check("보정 후 비가 1 근처", abs(r - 1) < 0.35)

# (c) 진짜 이득 차이(×5)는 어떤 단계로도 못 고친다 → 반드시 멈춰야 한다
nm, _ = climb(XL, XL * 5.0)
check("진짜 이득 차이는 사다리로 고쳐지지 않고 멈춘다", nm is None)

print("\n⑪ 보정은 선형이라 아인트호벤 항등식이 보존된다")
# 중앙값 필터 같은 비선형 기저선 제거를 쓰면 III = II − I 이 깨진다 → 선형만 쓴다
tt2 = np.linspace(0, 10, T)
I_ = np.stack([np.sin(2 * np.pi * 1.2 * tt2 + r3.rand()) for _ in range(20)])
II_ = np.stack([np.sin(2 * np.pi * 1.2 * tt2 + r3.rand()) * 1.4 for _ in range(20)])
V_ = [r3.randn(20, T) * .1 for _ in range(6)]
X12 = np.stack([I_, II_, II_ - I_, -(I_ + II_) / 2, I_ - II_ / 2, II_ - I_ / 2] + V_,
               axis=2).astype("float32")
X12 = X12 + r3.randn(20, 1, 12).astype("float32") * 0.9      # 오프셋을 얹는다
check("평균 제거 후 항등식 유지", assert_lead_order(demean(X12))["ok"])
check("고역통과 후 항등식 유지", assert_lead_order(hp(demean(X12), 0.5))["ok"])

print("\n⑫ 잘린 다운로드 탐지 (예상 바이트)")
FMT_BYTES = {"16": 2, "61": 2, "160": 2, "80": 1}
def expect(sig_len, n_sig_in_file, fmt):
    nb_ = FMT_BYTES.get(str(fmt))
    return sig_len * n_sig_in_file * nb_ if nb_ else None
e = expect(38400, 12, 16)
check("fmt16 · 38400표본 · 12유도 = 921600 B", e == 921600)
check("851785 B 는 모자라서 다시 받는다", 851785 < e)
check("정상 크기는 통과", e >= e)
check("모르는 형식은 None(크기 검사 생략)", expect(1000, 12, 212) is None)

print("\n" + ("전부 통과 ✅" if ok else "실패 있음 ❌"))
sys.exit(0 if ok else 1)
