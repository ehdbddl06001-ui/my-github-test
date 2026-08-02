"""실험22-A CELL 3c(【G1-c】)를 합성 데이터로 검정하는 픽스처.

묻는 것: S 상위 순위 붕괴가 **코호트 성질인가, 환자 한 명의 성질인가**.

MIT-BIH DS2 는 **#232 한 명이 S 의 76% 를 갖는다**(`PAPER.md` 관찰3). 그래서
"S 가 무너졌다" 는 결론이 실제로는 "#232 에서 무너졌다" 일 수 있다. 그걸 가르지
않으면 일반화할 수 없다.

두 시나리오(정답을 알고 있다):
  (A) 손상을 **#232 에만** 심는다 → "한 명의 성질" 이라고 말해야 한다
  (B) 손상을 **전 레코드에** 심는다 → "한 환자짜리 아님" 이라고 말해야 한다

둘은 전체 코호트에서 보면 비슷하게 나쁘다. #232 를 뺀 코호트에서만 갈린다.
"""
import os, sys, json, pickle, shutil, tempfile
import numpy as np
from scipy import stats

NB = json.load(open(os.path.join(os.path.dirname(__file__), "..",
                                 "notebooks", "exp22a_axis_transfer.ipynb")))
_c = [c for c in NB["cells"]
      if c["cell_type"] == "code" and "【G1-c】" in "".join(c["source"])]
assert len(_c) == 1, f"G1-c 셀을 {len(_c)}개 찾았다"
SRC = "".join(_c[0]["source"])

N = 20000
DOM = 232
SHARE = 0.76        # #232 가 갖는 S 비율 — 실데이터와 같은 성질
OTHERS = [100, 103, 105, 111, 113, 117, 121, 123, 200, 202, 210,
          212, 213, 214, 219, 221, 222, 228, 231, 233, 234]


def t_ci(v, conf=.95):
    v = np.asarray([x for x in v if np.isfinite(x)], float); n = len(v)
    m = float(v.mean()) if n else float("nan")
    if n < 2:
        return m, np.nan, np.nan
    h = float(stats.t.ppf(.5 + conf / 2, n - 1) * v.std(ddof=1) / np.sqrt(n))
    return m, m - h, m + h


class Run:
    def __init__(self): self.lines = []
    def log(self, s): self.lines.append(str(s)); print(s)
    def save_json(self, n, o): pass


def scenario(tag, where):
    print("\n" + "=" * 78); print(f"### {tag}"); print("=" * 78)
    rng = np.random.RandomState(0)
    rec = rng.choice([DOM] + OTHERS, N, p=[.10] + [.90 / len(OTHERS)] * len(OTHERS))
    yv = rng.choice([0, 1, 2, 3], N, p=[.90, .038, .055, .007])
    # S 를 재배치해 #232 가 76% 를 갖게 한다
    s_idx = np.where(yv == 1)[0]
    yv[s_idx] = 0
    n_dom = int(len(s_idx) * SHARE)
    yv[rng.choice(np.where(rec == DOM)[0], n_dom, replace=False)] = 1
    yv[rng.choice(np.where(rec != DOM)[0], len(s_idx) - n_dom, replace=False)] = 1

    root = tempfile.mkdtemp()
    try:
        found = {}
        for arm in ("mit_only", "mit_svdb"):
            for i in range(5):
                r = np.random.RandomState(50 + i)
                lg = r.normal(0, 1, (N, 4))
                lg[np.arange(N), yv] += 2.2
                if arm == "mit_svdb":
                    hit = (rec == DOM) if where == "only_dom" else np.ones(N, bool)
                    lg[hit & (yv == 1), 1] -= 1.6      # 해당 구간의 S 판별력만 훼손
                e = np.exp(lg - lg.max(1, keepdims=True))
                p = (e / e.sum(1, keepdims=True)).astype("float16")
                fn = f"{arm}_{1000+i}.pkl"
                found[fn] = os.path.join(root, fn)
                pickle.dump({"proba": p}, open(found[fn], "wb"))
        g = {"np": np, "pickle": pickle, "yv": yv, "zp": rec, "G1": {},
             "found": found, "t_ci": t_ci, "run": Run(), "CONFIG": {}, "G1_NOTE": []}
        exec(compile(SRC, "exp22a_cell3c", "exec"), g)
        return g
    finally:
        shutil.rmtree(root)


def note(g, s):
    return any(s in x for x in g["G1_NOTE"])


a = scenario("(A) 손상을 #232 에만 심음", "only_dom")
assert note(a, "한 명의 성질") or note(a, "한 명에서만"), \
    f"A: '#{DOM} 한 명의 성질' 이라고 말해야 한다 — {a['G1_NOTE']}"
assert not note(a, "한 환자짜리 아님"), "A 를 코호트 성질이라고 말하면 안 된다"

b = scenario("(B) 손상을 전 레코드에 심음", "all")
assert note(b, "한 환자짜리 아님"), \
    f"B: 코호트 성질이라고 말해야 한다 — {b['G1_NOTE']}"

# 상위 목록 구성 분석이 실제로 '무엇이 채웠나' 를 잡는지
for g, t in ((a, "A"), (b, "B")):
    assert any("상위" in x and "진짜 S" in x for x in g["G1_NOTE"]), \
        f"{t}: 상위 목록 구성 변화를 기록해야 한다"
    assert g["CONFIG"]["g1c"]["dominant_record"] == DOM, f"{t}: 지배 레코드 오인"
    assert abs(g["CONFIG"]["g1c"]["dominant_share"] - SHARE) < 0.02, \
        f"{t}: 지배 비율 오인"

print("\n전부 통과 ✅ — 한 명짜리 효과와 코호트 효과를 가른다")
sys.exit(0)
