"""실험22-A CELL 3(【G1】)을 **가짜 Drive** 위에서 실제로 실행하는 픽스처.

노트북에서 셀 소스를 직접 읽으므로 노트북이 바뀌면 이 테스트도 같이 따라간다.

세 시나리오:
  A) data_mit.npz 있고 DS2 마스크가 pkl 길이와 일치 → AUROC 재계산까지 간다
  B) data_mit.npz 없음 → 저장 지표만 회수, AUROC 생략, 죽지 않는다
  C) pkl 일부 없음 → 조기 skip, NameError 없이 끝난다
"""
import os, sys, json, pickle, shutil, tempfile
import numpy as np
from scipy import stats

NB = json.load(open(os.path.join(os.path.dirname(__file__), "..",
                                 "notebooks", "exp22a_axis_transfer.ipynb")))
_c = [c for c in NB["cells"]
      if c["cell_type"] == "code" and "\u3010G1\u3011" in "".join(c["source"])]
assert len(_c) == 1, f"G1 \uc140\uc744 {len(_c)}\uac1c \ucc3e\uc558\ub2e4"
SRC = "".join(_c[0]["source"])   # \u2605 \uc0ac\ubcf8\uc774 \uc544\ub2c8\ub77c **\ub178\ud2b8\ubd81 \uc790\uccb4**\ub97c \uc2e4\ud589\ud55c\ub2e4

_DS2 = [100,103,105,111,113,117,121,123,200,202,210,212,213,214,219,221,222,228,231,232,233,234]
PKL_NAMES = [f"{a}_{1000+i}.pkl" for a in ("mit_only","mit_svdb") for i in range(5)]

def t_ci(v, conf=.95):
    v = np.asarray([x for x in v if np.isfinite(x)], float); n = len(v)
    m = float(v.mean()) if n else float("nan")
    if n < 2: return m, np.nan, np.nan
    h = float(stats.t.ppf(.5+conf/2, n-1) * v.std(ddof=1) / np.sqrt(n))
    return m, m-h, m+h

class Run:
    def __init__(self): self.lines = []
    def log(self, s): self.lines.append(str(s)); print(s)
    def save_json(self, n, o): json.dump(o, open(os.devnull, "w"))

def build(root, with_labels=True, drop_pkl=False, per_record_gap=True):
    """가짜 Drive. 07-17 캐시는 레코드 232 를 통째로 빼서 길이 차이를 만든다."""
    runs = os.path.join(root, "ecg_out", "runs_s1p"); os.makedirs(runs)
    cache = os.path.join(root, "cache"); os.makedirs(cache)
    rng = np.random.RandomState(0)
    per = 300
    recs = [r for r in _DS2 if not (per_record_gap and r == 232)]
    zp = np.repeat(recs, per)
    zy = rng.choice([0,1,2], size=len(zp), p=[.94,.03,.03])
    if with_labels:
        np.savez(os.path.join(cache, "data_mit.npz"), y=zy, pid=zp,
                 beat=np.zeros((len(zy),1), "float32"))
    n_test = len(zy)
    names = PKL_NAMES[:-1] if drop_pkl else PKL_NAMES
    for n in names:
        arm = "mit_only" if n.startswith("mit_only") else "mit_svdb"
        seed = int(n.split("_")[-1].split(".")[0])
        p = rng.rand(n_test, 3).astype("float16")
        boost = 0.30 if arm == "mit_svdb" else 0.0
        p[zy == 2, 2] += boost                 # V 는 개선
        p[zy == 1, 1] -= boost * 0.7           # S 는 악화
        pickle.dump({"arm": arm, "seed": seed, "proba": p,
                     "train_prior": np.array([.94,.03,.03]),
                     "pred": p.argmax(1).astype("int8"),
                     "f1": {"N": .95+.001*seed%1, "S": .40-boost, "V": .88+boost},
                     "macro4": float(.70 + rng.rand()*.01),
                     "nsv": np.array([(zy==0).sum(), (zy==1).sum(), (zy==2).sum()]),
                     "n_train": 50576 + (8000 if arm=="mit_svdb" else 0),
                     "n_S_train": 944 + (7452 if arm=="mit_svdb" else 0),
                     "n_pat_train": 22 + (14 if arm=="mit_svdb" else 0),
                     "mins": 12.3},
                    open(os.path.join(runs, n), "wb"))
    return n_test

def scenario(tag, **kw):
    print("\n" + "=" * 78); print(f"### {tag}"); print("=" * 78)
    root = tempfile.mkdtemp()
    try:
        n_test = build(root, **kw)
        rng = np.random.RandomState(1)
        mpid = np.repeat(_DS2 + [101, 106], 300)          # 이 실험은 232 를 포함한다
        my = rng.choice([0,1,2], size=len(mpid), p=[.94,.03,.03])
        TE = np.isin(mpid, _DS2)
        g = {"os": os, "np": np, "pickle": pickle, "sys": sys,
             "DRIVE_ROOT": root, "PKL_NAMES": PKL_NAMES, "_DS2": _DS2,
             "mpid": mpid, "my": my, "TE": TE, "t_ci": t_ci,
             "run": Run(), "CONFIG": {}}
        exec(compile(SRC, "cell3_new.py", "exec"), g)
        print(f"\n>>> 결과: AUROC 재계산 {'✅' if g.get('G1') else '건너뜀'} "
              f"· 진단 {g.get('G1_NOTE')}")
        print(f">>> DS2 실제 {int(TE.sum()):,} · 가짜 07-17 테스트 {n_test:,}")
        return g
    finally:
        shutil.rmtree(root)

a = scenario("A) 라벨 있음 · 레코드 232 누락", with_labels=True)
assert a.get("G1"), "A 는 AUROC 까지 가야 한다"
assert any("232" in s for s in a["G1_NOTE"]), "누락 레코드를 진단해야 한다"

b = scenario("B) data_mit.npz 없음", with_labels=False)
assert b.get("G1") is None, "B 는 AUROC 를 생략해야 한다"
assert b.get("META"), "B 도 저장 지표는 회수해야 한다"

c = scenario("C) pkl 9/10 개", with_labels=True, drop_pkl=True)
assert c.get("G1") is None and c.get("META") is None, "C 는 조기 skip"

print("\n전부 통과 ✅ — 세 경로 모두 예외 없이 끝나고 진단을 남긴다")

sys.exit(0)
