"""퀘스트46 Q7-D(#865 반전 감사 + 기준 선택 실험) 픽스처.

정적 검사:
  ① `run.*` API 정합 + `MedKOSRun(..., project=)` + fallback 부재(R16)
  ② 불일치 레코드를 **이름으로** 출력하는가 (개수만 세면 어느 게 틀렸는지 안 남는다)
  ③ D-A 가 D1 기각 시 **중단**하는가 (정렬 사고면 하류 값이 전부 무효다)
  ④-0 RR 위치형이 **기준 불변 대조군**으로만 쓰이는가 — ★ 픽스처가 잡은 개념 오류.
     `base − pre` 는 base 가 바뀌어도 상수 이동이라 AUROC 가 안 변한다. 기준 셋을
     돌려봐야 같은 값 셋이 나올 뿐이다. **반전은 거리형(‖b−ref‖)에서만** 생긴다
  ④ 기준 격자가 **방향 있는 AUROC** 를 쓰는가
     — ★ 처음엔 `max(AUROC, 1−AUROC)` 로 '분리도' 만 봤다. 그러면 **완벽히 뒤집힌
       기준도 만점**을 받아 D4 가 통과해 버린다. 방향을 모르면 못 쓴다는 게 요점인데
       그 요점이 지워진다.
  ⑤ 음성 대조(무작위 반쪽 기준)가 있는가 — 없으면 '기준에서 먼 거리' 지표가 새는지 모른다

동적 검사:
  ⑥ **반전 레코드를 합성**해서 기준 격자가 진단하는가
     — 다수가 S 인 레코드를 만들면: 다수결 기준은 뒤집히고(D4 기각) 오라클은 회복(D3 지지)
  ⑦ **정상 레코드**에서는 다수결도 멀쩡한가 (격자가 무조건 기각기가 아님)
  ⑥-b **다수 비의존 앵커**(긴 RR 군)가 반전을 되돌리는가 — 처방 후보
  ⑧ 음성 대조가 실제로 0.5 근처인가 — ★ null 은 **라벨 셔플**이다. '무작위 부분집합의
     중앙을 기준으로' 는 null 이 아니다(그 중앙도 다수 모드에 앉는다 — 실측 0.0000)
  ⑨ P5 재구성이 **같은 코호트**에서 통계량과 귀무분포를 만드는가
     — Q7-B′ 는 통계량 55개체 / 귀무분포 72개체로 어긋나 있었다(내 오류)
"""
import os, sys, json, re
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
NB = json.load(open(os.path.join(ROOT, "notebooks", "quest46_q7d_inversion.ipynb")))
CODE = [c for c in NB["cells"] if c["cell_type"] == "code"]


def cell(tag):
    """헤더 줄(`# CELL n — 【TAG】 …`)로 고른다.
    본문 언급(예: CONFIG 주석의 '【D-D】에서 재구성')과 헷갈리면 안 된다."""
    hit = [c for c in CODE if "".join(c["source"]).split("\n", 1)[0].startswith("# CELL")
           and tag in "".join(c["source"]).split("\n", 1)[0]]
    assert len(hit) == 1, f"헤더가 '{tag}' 인 셀을 {len(hit)}개 찾았다"
    return "".join(hit[0]["source"])


SRC_G0, SRC_A = cell("【G0】"), cell("【D-A】")
SRC_B, SRC_C = cell("【D-B】"), cell("【D-C】")
SRC_D, SRC_E = cell("【D-D】"), cell("【D-E】")
ALL_SRC = "".join("".join(c["source"]) for c in CODE)

print("### 정적 검사")


def check_run_api():
    lib = os.path.join(ROOT, "lib", "medkos_run.py")
    if not os.path.exists(lib):
        print("  (lib 없음 — 생략)"); return
    have = set(re.findall(r"^\s{4}def (\w+)\(", open(lib).read(), re.M))
    miss = sorted(set(re.findall(r"\brun\.(\w+)\(", ALL_SRC)) - have)
    assert not miss, f"MedKOSRun 에 없는 메서드: {miss}"
    call = re.search(r"MedKOSRun\(([^)]*)\)", ALL_SRC)
    assert call and "project" in call.group(1), "MedKOSRun 호출에 project 없음"
    print("  ✅ ① run.* API 정합")


check_run_api()
assert "range(800, 895)" not in ALL_SRC and "range(800,895)" not in ALL_SRC, \
    "❌ 연속번호 fallback (R16)"
print("  ✅ ① fallback 부재 (R16)")

# ② 불일치를 이름으로
assert "for r, o, a in mism" in SRC_G0, "❌ 불일치를 이름으로 출력하지 않는다"
assert "mism.append" in SRC_G0, "불일치 목록을 모으지 않는다"
assert 'CONFIG["mismatch"]' in SRC_G0, "불일치가 기록에 안 남는다"
print("  ✅ ② 불일치 레코드를 이름·수치와 함께 출력하고 기록한다")

# ③ D1 기각 → 중단
assert "raise AssetError" in SRC_A and "D1 기각" in SRC_A, \
    "❌ D1 기각 시 중단하지 않는다 — 정렬 사고면 하류가 전부 무효다"
assert SRC_A.index("D1") < SRC_A.index("D2"), "D1 이 D2 보다 먼저 와야 한다"
print("  ✅ ③ D1 기각이면 예외로 중단한다")

# ④ 방향 있는 AUROC — 이게 이 실험의 핵심 불변식
assert "★ 방향 있는 AUROC" in SRC_C, "❌ 방향 규약이 코드에 명시돼 있지 않다"
assert re.search(r"a_ = float\(roc_auc_score\(tm\.astype\(int\), sig\)\)", SRC_C), \
    "❌ 기준 격자가 방향 있는 AUROC 를 안 쓴다"
i0 = SRC_C.index("ROWS.append(")
row = SRC_C[i0:i0 + 320]
assert "auroc=a_" in row and "info=info" in row, \
    "❌ auroc(방향 있음)와 info(방향 무시)가 분리돼 있지 않다"
assert "info = float(max(a_, 1 - a_))" in SRC_C, "❌ info 정의가 max(a, 1−a) 가 아니다"
assert "inverted=bool(a_ < 0.5 and info >= INFO_MIN)" in row, \
    "❌ 뒤집힘이 '신호 있는 축' 조건 없이 판정된다 — 0.5 근처 잡음도 반전으로 센다"
assert "INFO_MIN = 0.60" in SRC_C, "❌ 신호 문턱(INFO_MIN)이 없다"
for gate in ("D3", "D4"):
    seg = SRC_C[SRC_C.index(f'g_("{gate}"'):][:400]
    assert '["auroc"]' in seg and '["info"]' not in seg, \
        f"❌ {gate} 가 방향 무시 값(info)으로 판정한다 — 뒤집힌 기준이 통과한다"
print("  ✅ ④ 기준 격자는 방향 있는 AUROC 로 판정한다 (info 는 병기만)")

# ⑤ 음성 대조
assert "음성 대조" in SRC_C, "❌ 음성 대조가 없다"
print("  ✅ ⑤ 음성 대조가 있다")
assert "라벨을 섞는다" in SRC_C, "❌ null 이 라벨 셔플이 아니다"
assert "기준 불변" in SRC_C and "순위를 안 바꾼다" in SRC_C, \
    "❌ RR 위치형의 기준 불변성이 코드에 명시돼 있지 않다"
assert '"kind": "anchor"' in SRC_C or 'kind="anchor"' in SRC_C or '"anchor"' in SRC_C, \
    "❌ 다수 비의존 앵커가 없다"
assert 'g_("D4b"' in SRC_C, "❌ D4b(다수 비의존 앵커) 관문이 없다"
print("  ✅ ④-0 RR 위치형은 기준 불변 대조군 · 다수 비의존 앵커(D4b) 존재")

# ⑨ P5 재구성이 같은 코호트인가
assert "aO[pm[:n1]]" in SRC_D and "aO[pm[n1:]]" in SRC_D, \
    "❌ 순열이 aO(기존 55개체) 안에서 돌지 않는다"
assert "n1 = len(TEST55)" in SRC_D, "분할 크기가 TEST55 에서 오지 않는다"
assert "obs = abs(aT.mean() - aD.mean())" in SRC_D, "관측 통계량이 TEST/DEV 격차가 아니다"
assert "72개체 28/44" in SRC_D, "무효였던 이전 구성을 기록하지 않았다"
print("  ✅ ⑨ P5 재구성 — 통계량과 귀무분포가 **같은 55개체**에서 나온다")


# ═══════════════════════════════════════════════════════════════════════
class Run:
    def __init__(self): self.lines = []; self.dir = "/tmp"
    def log(self, s=""): self.lines.append(str(s)); print(s)
    def save_json(self, n, o): pass
    def save_fig(self, n, f=None): pass
    def finish(self, r): pass


def make_record(rng, n_s, n_n, p_shift=1.1, rr_s=250, rr_n=340, noise=0.9):
    """비트 (n,2,300) 합성. S 는 **P 영역이 다르고 RR 이 짧다**.

    R 은 index 100. P 영역 0:85 에 가우시안 P 파를 놓되 S 는 진폭을 바꾼다.
    """
    n = n_s + n_n
    t = np.r_[np.ones(n_s, bool), np.zeros(n_n, bool)]
    x = np.arange(300)
    qrs = np.exp(-((x - 100) ** 2) / (2 * 6 ** 2)) * 5.0
    pw = np.exp(-((x - 55) ** 2) / (2 * 9 ** 2))
    B = np.zeros((n, 2, 300), "float32")
    for i in range(n):
        amp = (-p_shift if t[i] else p_shift)          # S 는 P 파가 반대 극성
        base = qrs + amp * pw
        for c in range(2):
            B[i, c] = base + rng.normal(0, noise, 300)
    pre = np.where(t, rng.normal(rr_s, 35, n), rng.normal(rr_n, 35, n))  # 겹치게
    return B, t, pre.astype(float)


def run_grid(tag, n_s, n_n, seed=0):
    print("\n" + "=" * 78); print(f"### {tag}  (S {n_s} · N {n_n} · 유병률 {n_s/(n_s+n_n):.3f})")
    print("=" * 78)
    rng = np.random.RandomState(seed)
    B, t, pre = make_record(rng, n_s, n_n)
    n = len(t)
    VERD = {}
    def g_(k, ok, d):
        VERD[k] = "✅ 지지" if ok else "❌ 기각"; print(f"  {k:<4}{VERD[k]}  {d}")
    from sklearn.metrics import roc_auc_score
    g = {"np": np, "run": Run(), "d5": {"beat": B, "post_rr": pre},
         "keep": np.ones(n, bool), "m": np.arange(n), "t": t, "PRE": pre,
         "prev": float(t.mean()), "FOCUS": 999, "P_SEG": (0, 85), "QRS_SEG": (85, 130),
         "SEED0": 1, "ORACLE_THR": .80, "UNSUP_THR": .80, "POST": None,
         "roc_auc_score": roc_auc_score, "g_": g_, "VERD": VERD, "CONFIG": {},
         "Y": np.where(t, 1, 0), "REC": np.full(n, 999), "IDX_V": 2}
    exec(compile(SRC_C, "q7d_c", "exec"), g)
    return g, VERD


# ── ⑥ 반전 레코드 — 다수가 S
print("\n### ⑥ 반전 레코드 — 다수가 S")
g1, v1 = run_grid("(A) S 가 다수 (57.6%) — #865 재현", 1818, 1336, seed=1)
R1 = g1["CONFIG"]["reference_grid"]
gm = lambda R, k: max((r["auroc"] for r in R if r["kind"] == k), default=None)
print(f"    RR 위치형(기준 불변) {g1['CONFIG']['rr_positional_auroc']:.4f}"
      f" · 다수 의존 최고 {gm(R1,'maj'):.4f} · 오라클 최고 {gm(R1,'oracle'):.4f}"
      f" · 긴RR 앵커 최고 {gm(R1,'anchor'):.4f}")
print(f"    다수 의존에서 뒤집힌 축: {g1['CONFIG']['inverted_axes_majority']}")
# 다수결 기준은 뒤집혀야 한다 (거리형에서만)
inv1 = [r for r in R1 if r["kind"] == "maj" and r["inverted"]]
assert inv1, "A: 다수가 S 인데 다수 의존 기준이 안 뒤집혔다"
assert all(r["info"] >= 0.60 for r in inv1), "A: 신호 없는 축이 반전으로 잘못 세어졌다"
assert not any(r["inverted"] for r in R1 if r["kind"] == "invariant"), \
    "A: RR 위치형은 구조적으로 반전 불가인데 뒤집혔다"
assert v1["D3"] == "✅ 지지", f"A: 오라클로는 회복돼야 한다 — {v1}"
assert v1["D4"] == "❌ 기각", f"A: 다수 의존 기준은 실패해야 한다 — {v1}"
assert g1["CONFIG"]["unsup_cluster"]["big_s_frac"] > 0.5, "A: 큰 군이 S 여야 한다"
print("  ✅ ⑥ 반전을 진단한다 — 오라클 회복 · 다수 의존 실패 · RR 위치형은 불변")

# ── ⑥-b 다수 비의존 앵커(긴 RR)가 회복시키는가 — 처방 후보
print("\n### ⑥-b 긴RR 앵커")
uc = g1["CONFIG"]["unsup_cluster"]
print(f"    큰 군 S비율 {uc['big_s_frac']:.3f} · 긴RR 군 S비율 {uc['longrr_s_frac']:.3f}"
      f" · 둘이 같은 군인가 {uc['big_is_longrr']}")
assert not uc["big_is_longrr"], "A: 큰 군과 긴RR 군이 같으면 앵커를 구분 못 한다"
assert uc["longrr_s_frac"] < 0.5, "A: 긴RR 군이 N 쪽이어야 한다(이소성은 이르다)"
assert v1["D4b"] == "✅ 지지", f"A: 긴RR 앵커로는 회복돼야 한다 — {v1}"
print("  ✅ ⑥-b 개수를 안 보는 앵커가 기저를 되찾는다 — 처방 후보로 성립")

# ── ⑦ 정상 레코드 (격자가 무조건 기각기가 아님)
print("\n### ⑦ 정상 레코드 — S 가 소수")
g2, v2 = run_grid("(B) S 가 소수 (10%)", 300, 2700, seed=2)
R2 = g2["CONFIG"]["reference_grid"]
print(f"    다수 의존 최고 {gm(R2,'maj'):.4f} · 긴RR 앵커 최고 {gm(R2,'anchor'):.4f}")
assert v2["D4"] == "✅ 지지", f"B: S 가 소수면 다수 의존 기준으로도 돼야 한다 — {v2}"
# ★ '뒤집힘' 은 신호가 있는 축에서만 센다. 신호 없는 축(합성에서 QRS 는 S/N 이 같다)은
#   0.48 처럼 0.5 근처를 오가는데 그걸 반전으로 세면 정상 레코드도 늘 걸린다 — 픽스처가 잡았다.
inv2 = [r for r in R2 if r["kind"] == "maj" and r["inverted"]]
assert not inv2, f"B: 신호 있는 축이 뒤집히면 안 된다 — {[(r['axis'], round(r['auroc'],3)) for r in inv2]}"
assert any(not r["signal"] for r in R2), "B: 신호 없는 축이 '신호없음' 으로 표시돼야 한다"
assert v2["D4b"] == "✅ 지지", f"B: 정상 레코드에서 앵커가 망가지면 안 된다 — {v2}"
print("  ✅ ⑦ 정상에서는 다수 의존도 앵커도 둘 다 멀쩡 — 격자가 기각기 전용이 아니다")

# ── ⑧ 음성 대조
for tag, g in (("반전", g1), ("정상", g2)):
    nc = g["CONFIG"]["neg_control"]
    print(f"  {tag} 음성 대조(라벨 셔플) 중앙 {nc['median']:.4f} [{nc['lo']:.4f}, {nc['hi']:.4f}]")
    assert nc["ok"], f"{tag}: 라벨을 섞었는데 0.5 가 아니다 — 지표가 샌다"
print("  ✅ ⑧ 라벨 셔플 null 이 0.5 — 지표가 새지 않는다")
# ★ 처음엔 '무작위 부분집합의 중앙' 을 음성 대조로 썼다가 0.0000 이 나왔다.
#   무작위 부분집합의 중앙도 여전히 **다수 모드**에 앉으므로 null 이 아니다.
#   null 은 **라벨을 섞는 것**이다.

print("\n전부 통과 ✅ — Q7-D 는 방향을 접지 않고 기준 문제를 가른다")
sys.exit(0)
