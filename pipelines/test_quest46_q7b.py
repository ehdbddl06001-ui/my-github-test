"""퀘스트46 Q7-B(SVDB SE 실측) 노트북·하니스를 합성 데이터로 검정하는 픽스처.

이 실험은 **테스트가 오염되면 전부 무의미**하다. 그래서 이 픽스처의 절반은
성능 검정이 아니라 **오염 차단 장치가 실제로 작동하는지**를 본다.

정적 검사 (코드를 읽어서 확인 — 돌려보는 것으로는 못 잡는다):
  ① `run.*` API 정합 + `MedKOSRun(..., project=)`
  ② **CELL 5(GMIN 선택)가 TEST 를 참조하지 않는다** — 이게 이 실험의 핵심 불변식이다.
     GMIN 을 훑어 SE 가 통과하는 값을 고르면 그건 테스트로 고른 것이다(R12).
  ③ CELL 4 가 `wst_fit="ds1"` 로 부른다 — 특징선택이 DS2 를 안 본다
  ④ 학습 텐서(`TensorDataset`)에 SVDB 배열이 안 들어간다
  ⑤ 노트북이 오염된 `svdb_data.npz`(svdb_prep) 대신 `svdb_data5.npz` 를 쓴다
     — S 는 RR 로 정의되는 클래스라 `'+'` 주석 오염이 치명적이다

동적 검사 (합성 데이터로 셀을 직접 돌린다):
  ⑥ DEV/TEST 분할이 겹치지 않고 · 전수를 덮고 · **결정론적**인가
  ⑦ 분할이 S 부담을 실제로 맞추는가 (한쪽에 쏠리면 GMIN 선택이 왜곡된다)
  ⑧ `svdb_leak_audit` 가 학습∩평가 겹침을 **예외로** 막는가
  ⑨ DEV 에서 통과 GMIN 이 없으면 **TEST 를 열지 않고** 종료하는가
  ⑩ 정상 코호트에서 관문이 서고, 개체가 모자라면 기각되는가
     — 관문이 무조건 통과기도, 무조건 기각기도 아님을 양쪽으로 보인다
  ⑮ **탐색적 부지표** — PR-AUC 를 유병률과 함께 내는가(R4), 관문을 안 바꾸는가,
     '최대기여' 두 정의가 서로 다른 개체를 가리킬 수 있는가(R11-c)
  ⑬ **빌드 손실 감사** — Q7-A 주석 대비 레코드가 통째로 빠졌는지, 특히 **최상위
     S 레코드**가 빠졌는지 잡는가(실제로 일어났다)
  ⑭ **CI 폭 분해(R15)** — 매크로 CI 폭이 측정오차가 아니라 **개체 간 이질성**으로
     설명된다는 것을 수치로 보이는가
  ⑫ **Drive 자산이 자리표시자면 잡는가** — Drive 는 갱신 도구가 없어 빈 파일·자리
     표시자가 올라갈 수 있다(실제로 그랬다). 존재만 보면 CELL 4 에서 NameError 로 죽는다
  ⑪ **대조군 V 가 실제로 채점되는가** — 조용히 비면 "V 도 떨어졌다" 를 못 읽는다
     (첫 판에서 합성 데이터에 V 비트를 안 넣어 V arm 이 늘 '개체 0개' 였다)

★ 픽스처는 **정밀도가 아니라 논리**를 검정한다. 부트 횟수를 실제(400/4000)보다
  줄여 돌린다(120/800). SE 의 절대값은 여기서 의미 없다.
"""
import os, sys, json, re, shutil, tempfile
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
NB_PATH = os.path.join(ROOT, "notebooks", "quest46_q7b_svdb_se.ipynb")
NB = json.load(open(NB_PATH))
CODE = [c for c in NB["cells"] if c["cell_type"] == "code"]


def cell(tag):
    hit = [c for c in CODE if tag in "".join(c["source"])]
    assert len(hit) == 1, f"셀 '{tag}' 를 {len(hit)}개 찾았다"
    return "".join(hit[0]["source"])


SRC_SPLIT = cell("【G0】")
SRC_DEV = cell("【Q7B-A】")
SRC_TEST = cell("【Q7B-B】")
SRC_LOSS = cell("【Q7B-L】")
SRC_X = cell("【Q7B-X】")
SRC_M = [c for c in CODE if "".join(c["source"]).startswith("# CELL 4c — 【Q7B-M】")]
assert len(SRC_M) == 1; SRC_M = "".join(SRC_M[0]["source"])
HARNESS = open(os.path.join(ROOT, "mit-bih", "colab_crossdb_svdb.py")).read()

# ═══════════════════════════════════════════════════════════════════════════
#  정적 검사 — 오염 차단 불변식
# ═══════════════════════════════════════════════════════════════════════════
print("### 정적 검사 — 오염 차단 불변식")


def check_run_api():
    lib = os.path.join(ROOT, "lib", "medkos_run.py")
    if not os.path.exists(lib):
        print("  (lib 없음 — 생략)"); return
    have = set(re.findall(r"^\s{4}def (\w+)\(", open(lib).read(), re.M))
    nb_src = "".join("".join(c["source"]) for c in CODE)
    miss = sorted(set(re.findall(r"\brun\.(\w+)\(", nb_src)) - have)
    assert not miss, f"MedKOSRun 에 없는 메서드: {miss}"
    call = re.search(r"MedKOSRun\(([^)]*)\)", nb_src)
    assert call and "project" in call.group(1), "MedKOSRun 호출에 project 없음"
    print("  ✅ ① run.* API 정합")


check_run_api()

# ② GMIN 선택 셀이 TEST 를 만지면 안 된다 — 이 실험의 핵심 불변식
BANNED = ["test_have", "TEST_RECS", "S_TEST", "score_cohort"]
touched = [b for b in BANNED if b in SRC_DEV]
assert not touched, (
    f"❌ CELL 5(GMIN 선택)가 TEST 를 참조한다: {touched}\n"
    "   GMIN 을 TEST 를 보고 고르면 '검증이 선택에 의존' 하게 된다(R12).")
assert "dev_have" in SRC_DEV, "CELL 5 가 DEV 를 안 쓴다 — 분할이 무의미하다"
print(f"  ✅ ② GMIN 선택 셀이 TEST 를 참조하지 않는다 (금지어 {BANNED} 전부 부재)")

# ②-b 손실 감사 셀은 GMIN 선택 **앞**에 오지만 예측을 만지면 안 된다.
#     주석 카운트(SCOUNT)와 '어떤 레코드가 빌드됐나'(REC) 만 본다.
for bad in ("v2_cross_raw", "SC_S", "SC_V", "per_record", "roc_auc_score", "auroc"):
    assert bad not in SRC_LOSS, f"❌ 손실 감사 셀이 예측을 만진다: {bad}"
assert "✅ 지지" not in SRC_LOSS, "❌ 손실 감사 셀이 '지지' 를 낼 수 있다"
assert "SCOUNT" in SRC_LOSS and "REC" in SRC_LOSS, "손실 감사가 주석/빌드 대조를 안 한다"
print("  ✅ ②-b 손실 감사 셀은 주석·레코드 존재만 본다 (예측 미사용)")

# ②-c 부지표 셀은 **관문을 바꾸면 안 된다**(사후등록 금지)
assert "✅ 지지" not in SRC_X and "VERD" not in SRC_X, "❌ 부지표 셀이 판정을 낸다"
assert 'CONFIG["result"]["verdicts"] == _V0' in SRC_X, "❌ 관문 불변 확인이 없다"
assert "average_precision_score" in SRC_X, "PR-AUC 를 안 잰다"
assert "prev" in SRC_X and "lift" in SRC_X, "PR-AUC 를 유병률 없이 낸다 — R4 위반"
print("  ✅ ②-c 부지표 셀은 관문을 바꾸지 않고, PR-AUC 를 유병률과 함께 낸다")

# ②-d **조용한 fallback 금지** — 실제로 이 사고가 났다(ailab-2026-0052)
#     `_svdb_load` 가 wfdb 목록을 못 받으면 [800..894] 연속 목록으로 넘어가고 있었다.
#     SVDB 는 813~819·830~839 가 비어 있어 인덱스 13 부터 번호가 조용히 어긋난다.
assert "range(800, 895)" not in HARNESS, \
    "❌ 하니스에 연속번호 fallback 이 남아 있다 — 조용히 틀린 레코드 번호를 낸다"
assert "매핑된 레코드 번호가 목록에 없다" in HARNESS, "매핑 자가검증이 없다"
assert "wfdb.get_record_list" in SRC_M and "except" not in SRC_M.split("recs = [int(r)")[0][-200:], \
    "❌ 매핑 검증 셀도 fallback 을 쓰면 안 된다"
assert "recs[l - CONT[0]]" in SRC_M, "결정론적 복원식이 없다"
assert "재라벨에서 레코드가 합쳐졌다" in SRC_M, "재라벨 단사성 검사가 없다"
assert "재라벨 후 DEV/TEST 가 겹친다" in SRC_M, "재라벨 후 서로소 검사가 없다"
print("  ✅ ②-d 연속번호 fallback 부재 — 목록을 못 받으면 터진다")

# ③ 특징선택이 DS1 에서만 fit
SRC_TRAIN = cell("【Q7B-T】")
assert re.search(r'wst_fit\s*=\s*"ds1"', SRC_TRAIN), \
    "CELL 4 가 wst_fit='ds1' 로 부르지 않는다 — WST 선택이 DS2 를 본다"
assert 'RobustScaler().fit(Fm[tr])' in HARNESS, "스케일러가 DS1 에만 fit 되지 않는다"
print("  ✅ ③ WST SelectKBest·RobustScaler 모두 DS1 에만 fit")

# ④ 학습 텐서에 SVDB 가 안 들어간다
i = HARNESS.find("TensorDataset(")
assert i > 0, "TensorDataset 호출을 못 찾았다"
body = HARNESS[i:HARNESS.index("\n", HARNESS.index("\n", i) + 1)]   # 호출이 걸친 두 줄
for bad in ("sb", "sref", "sy", "f_sv", "Fs"):
    assert not re.search(rf"\b{bad}\b", body), f"학습 텐서에 SVDB 배열 `{bad}` 가 들어간다 — 누수"
assert "mb[tr]" in body and "my[tr]" in body, "학습 텐서가 DS1 만 쓰지 않는다"
print("  ✅ ④ 학습 텐서는 DS1(mb[tr]·my[tr])만 — SVDB 배열 부재")

# ⑤ 오염된 RR 파일을 안 쓴다
assert "svdb_data5.npz" in SRC_TRAIN + cell("【Q7B-P】") + HARNESS
assert not re.search(r'["\']svdb_data\.npz["\']', cell("【Q7B-P】")), \
    "오염된 svdb_data.npz(svdb_prep) 를 쓰고 있다 — RR 이 '+' 주석으로 오염돼 있다"
assert "build_labeled" in cell("【Q7B-P】"), "svdb_labels.build_labeled 로 빌드하지 않는다"
print("  ✅ ⑤ 오염 없는 svdb_data5.npz(build_labeled)를 쓴다")

# 관문 판정은 CELL 6 에만 있다.
#  ★ DEV 셀에도 "Q7B-*" 문자열은 나온다 — DEV 에서 못 고르면 **전부 기각**으로 닫는
#    분기다. 그건 정당하다. 금지해야 하는 건 DEV 셀이 **'지지'를 낼 수 있는 것**이다.
assert "✅ 지지" not in SRC_DEV, \
    "❌ DEV 셀이 '지지' 판정을 낼 수 있다 — 통과는 TEST 에서만 나와야 한다"
assert "def g_" not in SRC_DEV and "VERD" not in SRC_DEV, \
    "❌ 관문 채점기가 DEV 셀에 있다"
assert '"stopped_at": "dev"' in SRC_DEV, "DEV 중단 경로가 기록되지 않는다"
assert all(f"Q7B-{i}" in SRC_TEST for i in range(1, 6)), "관문 5개가 TEST 셀에 다 없다"
print("  ✅ DEV 셀은 '기각'만 낼 수 있다 — '지지'는 TEST 셀에서만 나온다")


# ═══════════════════════════════════════════════════════════════════════════
#  동적 검사
# ═══════════════════════════════════════════════════════════════════════════
class Run:
    def __init__(self): self.lines = []; self.dir = "/tmp"
    def log(self, s=""): self.lines.append(str(s)); print(s)
    def save_json(self, n, o): pass
    def save_fig(self, n, f=None): pass
    def save_npy(self, n, a): pass
    def finish(self, r): pass
    def data(self, n): return os.path.join(self._d, n) if hasattr(self, "_d") else "/tmp/" + n


STUB = {"mamba_data.npz": "", "colab_crossdb.py": "def run_crossdb(): pass",
        "colab_crossdb_svdb.py": "def run_crossdb_svdb(): pass",
        "svdb_labels.py": "def build_labeled(): pass"}


def run_split(scount, stub=None):
    """CELL 2 를 합성 주석 카운트로 돌린다 — 자산 검사를 위해 임시 트리를 만든다."""
    tmp = tempfile.mkdtemp()
    mit = os.path.join(tmp, "mitbih"); proj = os.path.join(tmp, "proj", "data")
    os.makedirs(mit); os.makedirs(proj)
    for f, body in (stub or STUB).items():
        open(os.path.join(mit, f), "w").write(body)
    json.dump({str(r): {"0": 2000, "1": n, "2": 100} for r, n in scount.items()},
              open(os.path.join(proj, "svdb_ann_counts.json"), "w"))
    g = {"np": np, "os": os, "json": json, "run": Run(), "CONFIG": {},
         "MITBIH": mit, "PROJECT": os.path.dirname(proj), "AssetError": RuntimeError}
    exec(compile(SRC_SPLIT, "q7b_split", "exec"), g)
    shutil.rmtree(tmp, ignore_errors=True)
    return g


# ── ⑥⑦ 분할
print("\n### ⑥⑦ DEV/TEST 사전 분할")
SC = {800 + i: v for i, v in enumerate(
    [1500, 900, 700, 640, 300, 280, 250, 240, 120, 110, 100, 95,
     60, 55, 40, 38, 20, 18, 12, 11, 9, 8, 4, 3, 2, 1, 0, 0])}
g1 = run_split(SC)
dev, test = g1["DEV_RECS"], g1["TEST_RECS"]
assert not (set(dev) & set(test)), "DEV/TEST 가 겹친다"
assert sorted(dev + test) == sorted(SC), "분할이 전수를 덮지 않는다"
g2 = run_split(SC)
assert (g2["DEV_RECS"], g2["TEST_RECS"]) == (dev, test), "분할이 결정론적이지 않다"
print(f"  ✅ ⑥ 겹침 없음 · 전수 덮음 · 재실행 동일 (DEV {len(dev)} · TEST {len(test)})")

sdev = sum(SC[r] for r in dev); stest = sum(SC[r] for r in test)
ratio = max(sdev, stest) / max(min(sdev, stest), 1)
assert ratio < 1.35, f"S 부담이 한쪽으로 쏠렸다 — DEV {sdev} vs TEST {stest} (비 {ratio:.2f})"
n10d = sum(SC[r] >= 10 for r in dev); n10t = sum(SC[r] >= 10 for r in test)
assert abs(n10d - n10t) <= 1, f"S≥10 레코드 수가 안 맞는다 — DEV {n10d} vs TEST {n10t}"
print(f"  ✅ ⑦ 부담 균형 — S {sdev:,} vs {stest:,} (비 {ratio:.2f}) · S≥10 {n10d} vs {n10t}")

# 지배 개체가 한쪽을 삼키지 않는지: 최대 개체는 한쪽에만 갈 수밖에 없다 → 그 쪽의 지배지분 보고
print(f"     (최대 개체 {max(SC, key=SC.get)}({max(SC.values()):,})는 "
      f"{'TEST' if max(SC, key=SC.get) in test else 'DEV'} 로 갔다 — 사실만 기록)")

# ── ⑫ 자리표시자 방어 — Drive 는 갱신 도구가 없어 빈 파일이 올라갈 수 있다
print("\n### ⑫ Drive 자산 내용 검사 — 존재만으로 통과시키지 않는다")
for victim in ("colab_crossdb_svdb.py", "colab_crossdb.py", "svdb_labels.py"):
    bad = dict(STUB); bad[victim] = "＿PLACEHOLDER＿"       # 실제로 이렇게 올라간 적 있다
    try:
        run_split(SC, stub=bad)
    except RuntimeError as e:
        assert victim in str(e), str(e)[:120]
        print(f"  ✅ {victim} 자리표시자를 잡는다")
    else:
        raise AssertionError(f"❌ {victim} 가 자리표시자인데 통과시켰다 — CELL 4 에서 NameError 로 죽는다")

# ── ⑧ 누수 감사
print("\n### ⑧ svdb_leak_audit — 학습∩평가 겹침을 예외로 막는가")
hg = {"np": np, "_DS1": [101, 106, 108], "_DS2": [100, 103, 105], "_BASE": "/tmp"}
exec(compile(HARNESS, "crossdb_svdb", "exec"), hg)
audit = hg["svdb_leak_audit"]
mpid = np.array([101] * 5 + [106] * 5 + [100] * 5)
tr = np.isin(mpid, [101, 106])
rep = audit(mpid, tr, np.array([800, 801, 802]), strict=True)
assert all(ok for ok, _ in rep.values()), rep
print("  ✅ 정상 구성은 통과")

for tag, bad_tr, bad_rec in (
        ("학습에 DS2 가 섞임", np.isin(mpid, [101, 106, 100]), np.array([800, 801])),
        ("평가 레코드가 학습 환자와 겹침", tr, np.array([101, 800]))):
    try:
        audit(mpid, bad_tr, bad_rec, strict=True)
    except RuntimeError as e:
        print(f"  ✅ 막았다 — {tag}: {str(e)[:70]}")
    else:
        raise AssertionError(f"❌ 통과시켰다 — {tag}")


# ── ⑨⑩ DEV 선택 → TEST 채점
def build(rng, spec, nneg=400, nv=40):
    """spec: [(레코드, S 양성 수, 진짜 AUROC)]. V 는 대조군 경로를 **실제로 태우려고**
    레코드마다 nv 개씩 넣는다(넣지 않으면 V arm 이 '개체 0개' 로 조용히 비어버린다)."""
    ys, rs, sS, sV = [], [], [], []
    for r, npos, auc in spec:
        d = (np.sqrt(2) * abs(np.percentile(rng.normal(size=60000), 100 * auc))
             if 0.5 < auc < 1 else 0.0)
        ys.append(np.r_[np.ones(npos, int), np.full(nv, 2), np.zeros(nneg, int)])
        rs.append(np.full(npos + nv + nneg, r))
        # S 점수: S 만 높다.  V 점수: V 만 높다(독립 축)
        sS.append(np.r_[rng.normal(d, 1, npos), rng.normal(0, 1, nv), rng.normal(0, 1, nneg)])
        sV.append(np.r_[rng.normal(0, 1, npos), rng.normal(d, 1, nv), rng.normal(0, 1, nneg)])
    y = np.concatenate(ys); rec = np.concatenate(rs)
    a, b = np.concatenate(sS), np.concatenate(sV)
    prob = np.zeros((5, len(y), 3))
    for k in range(5):
        prob[k, :, 1] = a + rng.normal(0, .01, len(a))
        prob[k, :, 2] = b + rng.normal(0, .01, len(b))
    return y, rec, prob


def run_pipeline(tag, dev_spec, test_spec, seed=0):
    print("\n" + "=" * 78); print(f"### {tag}"); print("=" * 78)
    rng = np.random.RandomState(seed)
    y, rec, prob = build(rng, list(dev_spec) + list(test_spec))
    g = {"np": np, "run": Run(), "P": {"v2_cross_raw": prob},
         "Y": y, "REC": rec,
         "dev_have": [r for r, *_ in dev_spec], "test_have": [r for r, *_ in test_spec],
         "DEV_RECS": [r for r, *_ in dev_spec], "TEST_RECS": [r for r, *_ in test_spec],
         "CONFIG": {}, "GMINS": [2, 5, 10, 20, 50], "SE_CAP": .05, "SE_MAX": .10,
         "N_MIN": 8, "DOM_MAX": .50, "CIW_MAX": .10, "NB_BOOT": 120, "NB_MACRO": 800,
         "IDX_S": 1, "IDX_V": 2, "SEED0": 1, "LeakError": RuntimeError}
    exec(compile(SRC_DEV, "q7b_dev", "exec"), g)
    exec(compile(SRC_TEST, "q7b_test", "exec"), g)
    return g


# ⑨ DEV 가 못 고르면 TEST 를 안 연다
bad_dev = [(300 + i, 3, 0.80) for i in range(12)]           # 양성 3개 → SE 폭발
good_test = [(400 + i, 60, 0.85) for i in range(12)]        # TEST 는 멀쩡하다
gA = run_pipeline("(A) DEV 에서 통과 GMIN 이 없다 — TEST 는 멀쩡해도 열지 않는다",
                  bad_dev, good_test)
RA = gA["CONFIG"]["result"]
assert RA["stopped_at"] == "dev", f"A: DEV 에서 멈춰야 한다 — {RA['stopped_at']}"
assert RA["gmin"] is None and all(v == "❌ 기각" for v in RA["verdicts"].values()), RA
assert "test_S" not in RA, "A: TEST 결과가 계산됐다 — 봉인이 깨졌다"
assert not any("TEST 채점" in l for l in gA["run"].lines), "A: TEST 채점 로그가 남았다"
print("  ✅ ⑨ DEV 에서 종료 — TEST 는 계산조차 하지 않았다(멀쩡한 TEST 를 두고도)")

# ⑩-a 정상 코호트 → 관문이 선다
ok_dev = [(300 + i, 60, 0.85) for i in range(12)]
ok_test = [(400 + i, 60, 0.85) for i in range(12)]
gB = run_pipeline("(B) 양쪽 다 넉넉하다 — 관문이 통과해야 한다", ok_dev, ok_test, seed=1)
RB = gB["CONFIG"]["result"]; VB = RB["verdicts"]
print(f">>> {VB}")
assert RB["stopped_at"] == "test" and RB["gmin"] is not None, RB
assert VB["Q7B-1"] == "✅ 지지" and VB["Q7B-2"] == "✅ 지지", f"B: 넉넉하면 통과해야 한다 — {VB}"
assert VB["Q7B-3"] == "✅ 지지", f"B: 균등 코호트인데 지배 지분에 걸렸다 — {VB}"
assert RB["test_S"]["n"] == 12, RB["test_S"]["n"]
# 대조군 V 가 **실제로 채점됐는지** 확인한다. 조용히 비면 "V 도 떨어졌다" 를 못 읽는다.
assert RB["test_V"] is not None and RB["test_V"]["n"] >= 8, \
    f"B: 대조군 V 가 채점되지 않았다 — {RB['test_V']}"
print(f"  ✅ ⑩-a 관문이 통과 — GMIN={RB['gmin']} · 개체 {RB['test_S']['n']}"
      f" · 최대SE {RB['test_S']['se_max']:.4f} · 매크로 CI 폭 {RB['test_S']['width']:.4f}")
print(f"     대조군 V 도 채점됨 — 개체 {RB['test_V']['n']} · 매크로 {RB['test_V']['macro']:.4f}")

# ⑩-b DEV 는 통과하는데 TEST 개체가 모자라다 → Q7B-1 기각 (관문이 통과기가 아님)
few_test = [(400 + i, 60, 0.85) for i in range(4)]
gC = run_pipeline("(C) DEV 는 통과 · TEST 개체 4개 — 하한에서 잡혀야 한다",
                  ok_dev, few_test, seed=2)
RC = gC["CONFIG"]["result"]; VC = RC["verdicts"]
print(f">>> {VC}")
assert RC["stopped_at"] == "test", RC
assert VC["Q7B-1"] == "❌ 기각", f"C: 개체 4개는 N_MIN 8 미만이라 기각이어야 한다 — {VC}"
print("  ✅ ⑩-b 개체 하한에서 기각 — 관문이 무조건 통과기가 아니다")

# ⑩-c 지배 개체가 있으면 R11-3 이 잡는다
dom_test = [(400, 3000, 0.85)] + [(401 + i, 20, 0.85) for i in range(11)]
gD = run_pipeline("(D) TEST 에 지배 개체 — R11-3 이 잡아야 한다", ok_dev, dom_test, seed=3)
RD = gD["CONFIG"]["result"]; VD = RD["verdicts"]
print(f">>> {VD}")
assert VD["Q7B-3"] == "❌ 기각", f"D: 지배 지분 관문이 잡아야 한다 — {RD['test_S']['dom']:.1%}"
assert "drop_rec" in RD["test_S"], "D: R11-b 최대기여 개체가 보고되지 않았다"
print(f"  ✅ ⑩-c 지배 지분 {RD['test_S']['dom']:.1%} 를 R11-3 이 잡는다"
      f" · 최대기여 #{RD['test_S']['drop_rec']} 제외값 {RD['test_S']['drop_macro']:.4f}")

# ── ⑬ 손실 감사가 '최상위 레코드 소실' 을 잡는가 (실제로 일어난 일)
print("\n### ⑬ 빌드 손실 감사")
def run_loss(scount, built):
    g = {"np": np, "run": Run(), "CONFIG": {}, "SCOUNT": dict(scount),
         "REC": np.array(sorted(built)),
         "DEV_RECS": sorted(list(scount)[1::2]), "TEST_RECS": sorted(list(scount)[0::2])}
    exec(compile(SRC_LOSS, "q7b_loss", "exec"), g)
    return g

full = run_loss(SC, list(SC))
assert full["CONFIG"]["build_loss"]["lost"] == [], "손실 0 인데 손실을 보고했다"
assert not any("최상위 레코드가 빠졌다" in l for l in full["run"].lines)
print("  ✅ 손실 0 이면 조용하다")

top = max(SC, key=SC.get)
part = run_loss(SC, [r for r in SC if r != top])
bl = part["CONFIG"]["build_loss"]
assert bl["top_record_lost"] is True, f"최상위 소실을 못 잡았다 — {bl}"
assert bl["lost"] == [top] and bl["lost_s"] == SC[top], bl
assert any("최상위 레코드가 빠졌다" in l for l in part["run"].lines), "경고가 안 남았다"
assert any("낙관적으로 보인다" in l for l in part["run"].lines), \
    "지배 지분이 낙관적이라는 경고가 없다"
print(f"  ✅ ⑬ 최상위 #{top}({SC[top]:,}) 소실을 잡고 '지배 지분이 낙관적' 을 경고한다")

# ── ⑭ CI 폭 분해가 이질성 지배를 드러내는가 (실측 재현)
print("\n### ⑭ CI 폭 분해 (R15)")
gE = run_pipeline("(E) 개체 간 이질성이 큰 코호트 — CI 폭 분해",
                  [(300 + i, 60, 0.85) for i in range(12)],
                  [(400 + i, 60, auc) for i, auc in enumerate(
                      [0.72, 0.99, 0.83, 0.97, 0.75, 0.995, 0.88, 0.93, 0.71, 0.99, 0.86, 0.96])],
                  seed=5)
dec = gE["CONFIG"].get("ciw_decomp")
assert dec, "CI 폭 분해가 CONFIG 에 없다"
print(f"    관측 {dec['observed']:.4f} · 이질성만 {dec['het_only']:.4f}"
      f" · 측정오차만 {dec['err_only']:.4f} · 분산비 {dec['var_ratio']:.1f}배")
assert dec["het_only"] > dec["err_only"], "이질성 큰 코호트인데 측정오차가 더 크게 나왔다"
assert abs(dec["het_only"] - dec["observed"]) < 0.4 * dec["observed"], \
    "이질성 근사가 관측 폭을 못 설명한다 — 분해가 잘못됐다"
print("  ✅ ⑭ 매크로 CI 폭이 개체 간 이질성으로 설명된다는 것을 수치로 보인다")

# ── ⑮ 부지표 셀이 관문을 안 바꾸고 PR-AUC 를 유병률과 함께 내는가
print("\n### ⑮ 탐색적 부지표 (PR-AUC · 부담 층화)")
#     ★ 두 '최대기여' 정의가 **다른 개체**를 가리키도록 만든다 — 실측 SVDB 가 그랬다
#       (#843: AUROC 0.7167 · S 17 → 제거영향 최대 / #853: 0.7251 · S 454 → 부담 최대)
gF = run_pipeline("(F) 부지표 — 부담 큰 실패군 + 부담 작은 극단 개체",
                  [(300 + i, 60, 0.85) for i in range(12)],
                  [(400, 400, 0.78), (401, 300, 0.82), (402, 200, 0.86),
                   (403, 10, 0.55)] + [(410 + i, 25, 0.97) for i in range(8)], seed=6)
V_before = dict(gF["CONFIG"]["result"]["verdicts"])
exec(compile(SRC_X, "q7b_x", "exec"), gF)
E = gF["CONFIG"]["exploratory"]
assert gF["CONFIG"]["result"]["verdicts"] == V_before, "부지표가 관문을 바꿨다"
print(f"    PR-AUC 매크로 {E['pr_auc_macro']:.4f} · 유병률 중앙 {E['prev_median']:.4f}"
      f" · lift {E['lift_macro']:.1f}배")
print(f"    단순 매크로 vs 양성수 가중 = {gF['CONFIG']['result']['test_S']['macro']:.4f}"
      f" vs {E['auroc_weighted_by_pos']:.4f}")
print(f"    스피어만 rho={E['spearman_pos_auroc'][0]:+.3f}")
assert E["auroc_weighted_by_pos"] < gF["CONFIG"]["result"]["test_S"]["macro"], \
    "부담 큰 쪽이 나쁜 코호트인데 가중값이 더 높게 나왔다"
assert E["spearman_pos_auroc"][0] < 0, "양성수-성능 음의 상관을 못 잡았다"
assert E["max_removal_rec"] != E["max_burden_rec"], \
    "두 '최대기여' 정의가 같은 개체를 가리켰다 — 시나리오가 구분을 못 만든다"
assert any("가중값으로 갈아타지 않는다" in l for l in gF["run"].lines), \
    "집계 갈아타기 금지 경고가 없다"
print(f"  ✅ ⑮ 제거영향 #{E['max_removal_rec']} ≠ 부담가중 #{E['max_burden_rec']} — 둘 다 보고한다")

print("\n전부 통과 ✅ — Q7-B 는 TEST 를 열기 전에 스스로를 잠근다")
sys.exit(0)
