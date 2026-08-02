"""실험22-A CELL 3d(【G1-d】)를 합성 데이터로 검정하는 픽스처.

묻는 것: 전역 PR-AUC 붕괴가 **환자 안 판별력** 손상인가 **환자 간 점수 눈금** 붕괴인가.

두 시나리오(정답을 알고 있다):
  (A) 특정 레코드(#210·#219·#221)의 S 로짓에 **전반적 가산** → 눈금만 어긋난다.
      환자 안 순위는 100% 보존되므로 레코드내 정규화로 완전히 복구돼야 한다.
  (B) S 양성의 S 로짓을 전역으로 −1.4 → 환자 안 판별력이 실제로 훼손된다.

★ 이 픽스처가 판정 규칙을 고치게 했다. 처음엔 '레코드내 정규화 회복비율' 로만
  판정했는데, (B)에서 회복비율이 65.6% 나와 '혼합' 으로 흐려졌다 — 환자 안 판별력이
  명백히 망가졌는데도(매크로 R-prec Δ −0.3328). 전역 하락이 워낙 커서 분모가
  부풀었기 때문이다. 그래서 **주 판정을 레코드 매크로**로 옮겼다: 각 레코드 안에서만
  채점하므로 환자 간 비교가 정의상 0 이고, 환자 안 판별력을 단독으로 잰다.
"""
import os, sys, json, pickle, shutil, tempfile
import numpy as np
from scipy import stats

NB = json.load(open(os.path.join(os.path.dirname(__file__), "..",
                                 "notebooks", "exp22a_axis_transfer.ipynb")))
_c = [c for c in NB["cells"]
      if c["cell_type"] == "code" and "【G1-d】" in "".join(c["source"])]
assert len(_c) == 1, f"G1-d 셀을 {len(_c)}개 찾았다"
SRC = "".join(_c[0]["source"])

N = 20000
RECS = [232, 222, 234, 202, 200, 213, 210, 219, 221, 231]
DOM, SHARE, S_ALL = 232, 0.76, 700


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


def scenario(tag, mode):
    print("\n" + "=" * 78); print(f"### {tag}"); print("=" * 78)
    rng = np.random.RandomState(0)
    rec = rng.choice(RECS, N, p=[.10] + [.90 / (len(RECS) - 1)] * (len(RECS) - 1))
    yv = np.zeros(N, int)
    nd = int(S_ALL * SHARE)
    yv[rng.choice(np.where(rec == DOM)[0], nd, replace=False)] = 1
    yv[rng.choice(np.where(rec != DOM)[0], S_ALL - nd, replace=False)] = 1
    yv[rng.choice(np.where(yv == 0)[0], 1200, replace=False)] = 2

    root = tempfile.mkdtemp()
    try:
        found = {}
        for arm in ("mit_only", "mit_svdb"):
            for i in range(5):
                r = np.random.RandomState(50 + i)
                lg = r.normal(0, 1, (N, 4))
                lg[np.arange(N), yv] += 2.2
                if arm == "mit_svdb":
                    if mode == "scale":            # 레코드별 전반 가산 = 눈금만
                        for rr, b in ((210, 2.2), (219, 2.0), (221, 1.8)):
                            lg[rec == rr, 1] += b
                    else:                          # 환자 안 판별력 훼손
                        lg[yv == 1, 1] -= 1.4
                e = np.exp(lg - lg.max(1, keepdims=True))
                p = (e / e.sum(1, keepdims=True)).astype("float16")
                fn = f"{arm}_{1000+i}.pkl"
                found[fn] = os.path.join(root, fn)
                pickle.dump({"proba": p}, open(found[fn], "wb"))
        g = {"np": np, "pickle": pickle, "yv": yv, "zp": rec, "G1": {},
             "found": found, "t_ci": t_ci, "run": Run(), "CONFIG": {}, "G1_NOTE": []}
        exec(compile(SRC, "exp22a_cell3d", "exec"), g)
        return g
    finally:
        shutil.rmtree(root)


a = scenario("(A) 특정 레코드에 점수 가산 = 환자 간 눈금만 어긋남", "scale")
va = a["CONFIG"]["g1d"]
assert va["verdict"] == "환자 간 눈금", f"A 오판: {va['verdict']}"
assert va["recovered_frac"] > 0.9, f"A: 정규화로 거의 전부 복구돼야 한다 ({va['recovered_frac']:.1%})"
assert abs(va["macro_rp"][0]) < 0.02, f"A: 매크로는 안 움직여야 한다 ({va['macro_rp'][0]:+.4f})"

b = scenario("(B) 환자 안 S 판별력 훼손", "discrim")
vb = b["CONFIG"]["g1d"]
assert vb["verdict"].startswith("환자 안 판별력"), f"B 오판: {vb['verdict']}"
assert vb["macro_rp"][0] < -0.05, f"B: 매크로가 떨어져야 한다 ({vb['macro_rp'][0]:+.4f})"

# 레코드내 순위정규화가 **환자 안 순위를 보존**하는지 — 이 전제가 깨지면 논증이 무너진다
print("\n" + "=" * 78)
print("### (C) 레코드내 순위정규화가 환자 안 순위를 보존하는가")
print("=" * 78)
rng = np.random.RandomState(3)
rec_c = rng.choice([100, 200, 300], 500)
s_c = rng.rand(500)
out = np.empty(500)
for r in np.unique(rec_c):
    ii = np.where(rec_c == r)[0]
    out[ii] = (s_c[ii].argsort().argsort() + 0.5) / len(ii)
for r in np.unique(rec_c):
    ii = np.where(rec_c == r)[0]
    assert (s_c[ii].argsort() == out[ii].argsort()).all(), f"#{r} 안에서 순위가 바뀌었다"
print("  ✅ 세 레코드 모두 내부 순위가 정확히 보존된다")

print("\n전부 통과 ✅ — 환자 간 눈금과 환자 안 판별력을 가른다")
sys.exit(0)
