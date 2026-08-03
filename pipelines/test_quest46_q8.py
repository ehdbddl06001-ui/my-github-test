"""퀘스트46 Q8(가중 매크로) 노트북을 합성 데이터로 검정하는 픽스처.

노트북의 CELL 3(【Q8】)·CELL 4(【Q8 채점】)를 직접 읽어 돌린다.

검정하는 것:
  ① `kish_ess` 가 정의대로인가 — 균등이면 n, 한 명에 몰리면 → 1
  ② 역분산 가중이 **정밀한 개체 쪽으로** 추정치를 끈다(작동 확인)
  ③④ (A) 균질 코호트에서 역분산이 오히려 손해라는 것을 실측으로 드러내는가
  ⑤ 기준선(GMIN 10)이 안 서는 코호트를 **조용히 통과시키지 않는가**
  ⑥ **가중이 소수에 몰리는 코호트에서 Q8-4 가 기각되는가** — 이게 이 실험의
     안전장치다. ESS 를 안 보면 '27명을 받았다' 고 말하면서 실질은 1.8명일 수 있다
     (R11-b 의 #213 과 같은 구조)
  ⑦ 관문이 무조건 기각기가 아닌가 — 완만한 이질성에서는 통과해야 한다
  ⑧ **관문의 판독 순서** — ESS 가 무너졌을 때 좁아진 CI 를 성과로 못 읽게 막는가
  ⑨ **완벽 분리 개체**(AUROC=1 · 부트 SE=0)를 어떻게 다루는가 — R14-b

시나리오:
  (A) SE 가 **균질** → 역분산 가중이 **오히려 나쁘다**(추정 잡음). 이게 이 방법의
      핵심 한계이고, 픽스처가 실측으로 잡았다: 25개체 동일 조건에서 가중 CI 폭
      0.0425 vs 단순 0.0254 — 1.7배 나쁘다. ESS 도 25 → 18.
  (B) 기준선 붕괴 — GMIN 10 을 넘는 개체가 1개뿐 → Q8-1~3 미결, Q8-4 는 그래도 잰다
  (C) 가중 쏠림 — 기준선은 서는데 ESS 가 1.8 로 붕괴 → Q8-4 기각
  (D) SE 가 **완만하게 이질적** → ESS 23.5 로 살아남고 전 관문 통과
  (E) **완벽 분리 개체**가 섞임 → 1/SE² 발산. 단순 arm 은 21개 전부 유지하는데
      역분산은 **그 한 개체가 가중의 100.0%** 를 가져간다(ESS 1.00 · 점추정 1.0000)

★ 이 픽스처가 잡은 것 세 가지:
  1. 처음엔 (A)에서 '지지' 를 기대했다. 틀렸다 — 역분산 가중은 SE 가 **참값**일
     때만 최적이다. 부트 추정치로 가중하면 균질한 코호트에서는 잡음만 증폭한다.
     그래서 노트북에 **양성수 가중**(w = n_pos · 추정 잡음 없음) arm 을 나란히 넣었다.
  2. (B) 는 `base['width'] = 0` 나눗셈으로 죽었다. 죽는 것보다 큰 문제는 개체
     1개짜리를 '폭 0.0000 의 최정밀 기준선' 으로 쓰고 있었다는 것이다.
  3. (C) 에서 Q8-1 은 **'지지'(폭 −46.6%)** 였다. 그런데 ESS 는 1.8 이었다.
     좁아진 CI 는 정밀해진 게 아니라 개체가 무너진 결과였다 — 폭만 보면 성과로
     썼을 것이다. 그래서 관문에 **판독 순서**를 박았다(Q8-4 기각 → Q8-1·3 보류).

★ 실데이터(ailab-2026-0050)가 이 픽스처보다 나쁜 것을 하나 더 찾았다: INCART 에서
  역분산 점추정이 **정확히 1.0000** 이 나왔다. AUROC 는 천장이 1 이라 완벽 분리
  개체의 부트 SE 가 0 으로 가고, `w = 1/SE²` 가 **발산**한다. 합성 데이터를 전부
  분리도 0.85 근처로 깔았기 때문에 픽스처가 못 봤다 → 시나리오 (E)를 추가했더니
  실데이터보다 더 선명하게 재현됐다(실측 ESS 2.0/27 · 최대 55.8% → 합성 ESS 1.00/21 ·
  최대 **100.0%**). 교훈: **경계값 지표를 검정할 때는 경계에 붙은 개체를 넣는다.**

★ 반례도 남긴다: (D)에서는 양성수 가중 ESS 24.0 > 역분산 23.5 인데, (C)에서는
  양성수 1.2 < 역분산 1.8 이다. '양성수 가중이 항상 낫다' 는 성립하지 않는다.
"""
import os, sys, json
import numpy as np

NB = json.load(open(os.path.join(os.path.dirname(__file__), "..", "notebooks",
                                 "quest46_q8_weighted_macro.ipynb")))
CODE = [c for c in NB["cells"] if c["cell_type"] == "code"]
def cell(tag):
    hit = [c for c in CODE if tag in "".join(c["source"])]
    assert len(hit) == 1, f"셀 '{tag}' 를 {len(hit)}개 찾았다"
    return "".join(hit[0]["source"])

SRC_DEF = cell("【Q8】")          # per_record · kish_ess · wmean 정의 + arm 구성
SRC_GATE = cell("【Q8 채점】")


def check_run_api():
    import re
    lib = os.path.join(os.path.dirname(__file__), "..", "lib", "medkos_run.py")
    if not os.path.exists(lib):
        print("  (lib 없음 — 생략)"); return
    have = set(re.findall(r"^\s{4}def (\w+)\(", open(lib).read(), re.M))
    nb_src = "".join("".join(c["source"]) for c in CODE)
    miss = sorted(set(re.findall(r"\brun\.(\w+)\(", nb_src)) - have)
    assert not miss, f"MedKOSRun 에 없는 메서드: {miss}"
    call = re.search(r"MedKOSRun\(([^)]*)\)", nb_src)
    assert call and "project" in call.group(1), "MedKOSRun 호출에 project 없음"
    print("  ✅ run.* API 정합")

print("### run.* API 정합성")
check_run_api()


class Run:
    def __init__(self): self.lines = []; self.dir = "/tmp"
    def log(self, s): self.lines.append(str(s)); print(s)
    def save_json(self, n, o): pass
    def save_fig(self, n, f=None): pass


def build(rng, spec):
    """spec: [(레코드, 양성 수, 진짜 AUROC)] → INCART 흉내 배열."""
    ys, gs, ps = [], [], []
    for r, npos, auc in spec:
        nneg = 1500
        y = np.r_[np.ones(npos, int), np.zeros(nneg, int)] * 1
        g = np.full(npos + nneg, r)
        # AUROC 가 대략 auc 가 되도록 분리도를 준다. auc >= 1 이면 **완벽 분리**
        # (R14-b ④ — 경계값 지표는 경계에 붙은 개체가 시나리오에 있어야 한다)
        if auc >= 1.0:
            d = 30.0
        elif 0.5 < auc < 1:
            d = np.sqrt(2) * np.abs(np.percentile(rng.normal(size=100000), 100 * auc))
        else:
            d = 0.0
        s = np.r_[rng.normal(d, 1, npos), rng.normal(0, 1, nneg)]
        ys.append(y); gs.append(g); ps.append(s)
    y = np.concatenate(ys); g = np.concatenate(gs); s = np.concatenate(ps)
    prob = np.zeros((5, len(y), 3))
    for k in range(5):
        prob[k, :, 1] = s + rng.normal(0, .01, len(s))
    return y, g, prob


def scenario(tag, spec, seed=0):
    print("\n" + "=" * 78); print(f"### {tag}"); print("=" * 78)
    rng = np.random.RandomState(seed)
    y, g, prob = build(rng, spec)
    ctx = {"np": np, "run": Run(), "CONFIG": {}, "SEED0": 1, "N_MIN": 20,
           "P": {"y_cross": y, "v2_cross_raw": prob}, "ipid": g}
    exec(compile(SRC_DEF, "q8_def", "exec"), ctx)
    exec(compile(SRC_GATE, "q8_gate", "exec"), ctx)
    return ctx


# ── ① kish_ess 정의 확인
probe = scenario("(준비) kish_ess 정의 확인",
                 [(300 + i, 30, 0.85) for i in range(25)])
ke = probe["kish_ess"]
assert abs(ke(np.ones(10)) - 10) < 1e-9, "균등 가중이면 ESS = n"
assert abs(ke(np.array([1e9] + [1.0] * 99)) - 1.0) < 1e-3, "한 명에 몰리면 ESS → 1"
assert abs(ke(np.array([1, 1, 2, 2.0])) - 3.6) < 1e-9, f"손계산 3.6 ≠ {ke(np.array([1,1,2,2.0]))}"
print("\n✅ ① kish_ess — 균등 n · 집중 1 · 손계산 3.6 전부 일치")

# ── ② 가중이 정밀한 쪽으로 끈다
wm = probe["wmean"]
assert abs(wm([0.9, 0.5], [9.0, 1.0]) - 0.86) < 1e-9, "역분산 가중이 정밀한 쪽으로 끌어야 한다"
print("✅ ② wmean — 가중 9:1 이면 0.86 (정밀한 0.9 쪽)")

# ── (A) SE 가 균질 → 역분산 가중이 오히려 나빠야 한다(이 방법의 한계)
a = scenario("(A) SE 가 균질 — 25레코드가 양성 30개씩", [(300 + i, 30, 0.85) for i in range(25)])
va = a["CONFIG"]["result"]["verdicts"]
ar = a["CONFIG"]["result"]["arms"]
iv, pl = ar["**역분산 가중 (GMIN 2)**"], ar["단순 매크로 (GMIN 10)"]
print(f">>> {va}")
print(f"    역분산 CI {iv['width']:.4f} (ESS {iv['ess']:.1f}) vs 단순 {pl['width']:.4f}")
assert iv["width"] > pl["width"], \
    "A: SE 가 균질하면 역분산 가중은 이득이 없어야 한다(추정 잡음)"
assert iv["ess"] < iv["n"], "A: 역분산 가중은 ESS 를 깎는다"
assert va["Q8-1"] == "❌ 기각", f"A: Q8-1 은 기각이어야 한다 — {va}"
print("✅ ③ SE 균질 코호트에서 역분산 가중의 손해를 실측으로 드러낸다")
npg = ar.get("양성수 가중 (GMIN 2)")
assert npg and npg["ess"] > iv["ess"], \
    f"A: 양성수 가중이 역분산보다 ESS 가 커야 한다 {npg} vs {iv}"
print(f"✅ ④ 양성수 가중 ESS {npg['ess']:.1f} > 역분산 {iv['ess']:.1f} — 잡음 없는 대안이 낫다")

IV = "**역분산 가중 (GMIN 2)**"
BASE = "단순 매크로 (GMIN 10)"

# ── (B) 기준선 자체가 안 서는 코호트 → 조용히 비우지 말고 '미결' 로 남겨야 한다
#     GMIN 10 을 넘는 개체가 1개뿐이면 매크로가 성립하지 않는다(부트 CI 폭 0 = 가짜 정밀도).
#     ★ 이 시나리오가 잡은 것: 예전 코드는 여기서 base['width']=0 으로 나눠
#       ZeroDivisionError 로 죽었다. 죽는 것도 문제지만, 더 큰 문제는 개체 1개짜리를
#       '폭 0.0000 의 최정밀 기준선' 으로 취급하고 있었다는 것이다.
b = scenario("(B) 기준선 붕괴 — 양성 3,000개 1개 + 3개짜리 26개",
             [(300, 3000, 0.85)] + [(301 + i, 3, 0.85) for i in range(26)], seed=1)
rb, vb = b["CONFIG"]["result"], b["CONFIG"]["result"]["verdicts"]
print(f">>> {vb}")
assert BASE not in rb["arms"], "B: 개체 1개짜리 arm 은 성립하면 안 된다"
assert vb["Q8-1"] == "⚠️ 미결", f"B: 기준선이 없으면 미결이어야 한다 — {vb}"
assert vb["Q8-4"] == "❌ 기각", f"B: ESS 관문은 기준선 없이도 서야 한다 — {vb}"
print(f"✅ ⑤ 기준선이 없으면 조용히 통과시키지 않고 미결 — ESS 는 그래도 잰다"
      f" (ESS {rb['arms'][IV]['ess']:.2f})")

# ── (C) 기준선은 서지만 가중이 한 개체로 쏠린다 → '27명 받았다' 는 착시
c = scenario("(C) 가중 쏠림 — 양성 3,000개 1개 + 12개짜리 26개",
             [(300, 3000, 0.85)] + [(301 + i, 12, 0.85) for i in range(26)], seed=2)
rc, vc = c["CONFIG"]["result"], c["CONFIG"]["result"]["verdicts"]
ivc = rc["arms"][IV]
print(f">>> {vc}")
print(f"    역분산 n={ivc['n']} · ESS={ivc['ess']:.2f} · 최대가중={ivc['top_w']:.1%}")
assert rc["arms"][BASE]["n"] >= 20, f"C: 기준선은 서야 한다 — {rc['arms'][BASE]['n']}"
assert vc["Q8-4"] == "❌ 기각", f"C: 쏠림을 ESS 관문이 잡아야 한다 — ESS={ivc['ess']}"
assert ivc["ess"] < 5 < ivc["n"], \
    f"C: 개체는 {ivc['n']}개인데 실질은 한 줌이어야 한다 — ESS {ivc['ess']}"
print("✅ ⑥ 가중 쏠림을 ESS 가 잡는다 — R11-b 의 #213 과 같은 구조를 사전에 차단")
# ★ (C) 가 잡은 진짜 함정: **CI 폭만 보면 이겼다.** Q8-1 은 '지지'(폭 −46.6%)인데
#   그 좁아짐은 정밀해져서가 아니라 유효 개체가 1.8 로 무너져서 생긴 것이다.
#   관문에 읽는 순서가 없으면 이걸 성과로 쓴다.
assert "판독 보류" in vc["Q8-1"], \
    f"C: ESS 가 무너졌으면 Q8-1 의 '지지' 는 보류로 표시돼야 한다 — {vc['Q8-1']}"
assert any("Q8-4 가 기각이면" in l for l in c["run"].lines), \
    "C: 판독 순서 경고가 로그에 남아야 한다"
print("✅ ⑧ 좁아진 CI 를 성과로 못 읽게 막는다 — 관문에 판독 순서가 있다")

# ── (D) SE 가 **이질적**이되 쏠리지는 않는다 → 가중이 이득일 수 있는 유일한 지형
d = scenario("(D) 이질 SE — 양성 30개 15개체 + 90개 15개체",
             [(300 + i, 30, 0.85) for i in range(15)]
             + [(400 + i, 90, 0.85) for i in range(15)], seed=3)
rd, vd = d["CONFIG"]["result"], d["CONFIG"]["result"]["verdicts"]
ivd, npd, bsd = rd["arms"][IV], rd["arms"]["양성수 가중 (GMIN 2)"], rd["arms"][BASE]
print(f">>> {vd}")
print(f"    폭 — 단순 {bsd['width']:.4f} · 양성수 {npd['width']:.4f} · 역분산 {ivd['width']:.4f}")
print(f"    ESS — 양성수 {npd['ess']:.1f} · 역분산 {ivd['ess']:.1f} (개체 {ivd['n']})")
assert vd["Q8-4"] == "✅ 지지", f"D: 완만한 이질성이면 ESS 는 살아야 한다 — {vd}"
assert npd["ess"] > ivd["ess"], "D: 추정 잡음이 없는 양성수 가중이 ESS 를 더 지켜야 한다"
print("✅ ⑦ 완만한 이질성에서는 ESS 관문이 통과 — 관문이 무조건 기각기가 아니다")

# ── (E) **완벽 분리 개체**가 섞인다 → 1/SE² 발산 (R14-b · 실데이터가 가르쳐준 것)
#     실측(ailab-2026-0050): 역분산 점추정이 정확히 1.0000, ESS 2.0. 합성 픽스처는
#     분리도를 0.85 근처로만 깔아서 이걸 못 봤다. 이제 경계에 붙은 개체를 넣는다.
e = scenario("(E) 완벽 분리 개체 1개 + 보통 개체 20개", 
             [(300, 30, 1.0)] + [(301 + i, 30, 0.85) for i in range(20)], seed=4)
re_, ve = e["CONFIG"]["result"], e["CONFIG"]["result"]["verdicts"]
ive, bse = re_["arms"][IV], re_["arms"][BASE]
logs = "\n".join(e["run"].lines)
print(f">>> {ve}")
print(f"    단순 n={bse['n']} · 역분산 n={ive['n']} ESS={ive['ess']:.2f}"
      f" 최대가중={ive['top_w']:.1%} 점추정={ive['est']:.4f}")
# 단순 arm 은 완벽 분리 개체를 **떨구면 안 된다** — se>0 필터는 역분산 전용이다
assert bse["n"] == 21, f"E: 단순 매크로는 21개체 전부 채점해야 한다 — {bse['n']}"
# 역분산은 그 개체를 배제했거나(로그) 가중이 발산해 ESS 가 무너졌거나 둘 중 하나다
excluded = "SE=0(완벽 분리)" in logs
assert excluded or ive["ess"] < 20, \
    f"E: 완벽 분리 개체를 배제하거나 ESS 가 무너져야 한다 — ESS {ive['ess']}"
how = "역분산 arm 에서 배제" if excluded else f"ESS {ive['ess']:.2f} 로 붕괴"
print(f"✅ ⑨ 완벽 분리 개체 — 단순 arm 은 {bse['n']}개 전부 유지, {how}")

print("\n전부 통과 ✅ — Q8 은 가중의 이득과 그 대가(ESS)를 함께 잰다")
sys.exit(0)
