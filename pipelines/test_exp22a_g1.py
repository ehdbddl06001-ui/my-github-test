"""실험22-A CELL 3(【G1】)을 **가짜 Drive** 위에서 실제로 실행하는 픽스처.

노트북에서 셀 소스를 직접 읽으므로, 노트북이 바뀌면 이 테스트도 같이 따라간다.

다섯 시나리오:
  A) 07-17 캐시에서 **레코드 232 가 통째로** 빠짐 → 레코드 소실이라고 말해야 한다
  B) data_mit.npz 없음 → 저장 지표만 회수, AUROC 생략, 죽지 않는다
  C) pkl 일부 없음 → 조기 skip, NameError 없이 끝난다
  D) 【R10-b】 **길이는 정확히 맞는데 클래스 구성이 다르다** → 정렬을 거부해야 한다
  E) 전 레코드에서 4% 씩 **분산 손실** → 레코드 통째 누락을 배제한다고 말해야 한다

**A 와 E 가 이 픽스처의 핵심 대비다.** 겉보기 비트 수 차이는 비슷한데 A 는 레코드
소실, E 는 검출기 손실이다. 둘을 가르는 건 오직 **클래스 프로파일**이다 — MIT-BIH
DS2 는 한 레코드(#232)가 S 의 약 3/4 를 갖고 있어서, 그게 빠지면 S 손실이 폭발한다
(`mit-bih/PAPER.md` 관찰3). 그래서 가짜 07-17 배열은 **현재 배열에서 파생**시킨다.
독립 난수로 만들면 이 구조가 사라져 A 와 E 가 구분 불가능해진다(실제로 그렇게
짰다가 이 픽스처에 걸렸다).

07-17 배열은 4클래스(N/S/V/**F**)이고 `nsv` 는 N/S/V **셋만** 센다 — 실제 pkl 구조.
그래서 '부족(N/S/V) + 초과(F)' 가 상쇄돼 겉보기 길이 차이가 줄어든다.
"""
import os, sys, json, pickle, shutil, tempfile
import numpy as np
from scipy import stats

NB = json.load(open(os.path.join(os.path.dirname(__file__), "..",
                                 "notebooks", "exp22a_axis_transfer.ipynb")))
_c = [c for c in NB["cells"]
      if c["cell_type"] == "code" and "【G1】" in "".join(c["source"])]
assert len(_c) == 1, f"G1 셀을 {len(_c)}개 찾았다"
SRC = "".join(_c[0]["source"])   # ★ 사본이 아니라 **노트북 자체**를 실행한다

_DS2 = [100,103,105,111,113,117,121,123,200,202,210,212,213,214,219,221,222,228,231,232,233,234]
PKL_NAMES = [f"{a}_{1000+i}.pkl" for a in ("mit_only", "mit_svdb") for i in range(5)]
PER = 300          # 레코드당 비트(가짜)
S_TOT = 200        # DS2 전체 S(가짜)
S_232 = 0.75       # #232 가 갖는 S 비율 — 실데이터와 같은 성질
N_F = 180          # 07-17 에만 있는 제4클래스(F) 개수


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
    def save_json(self, n, o): json.dump(o, open(os.devnull, "w"))


def cur_arrays(rng):
    """현재 파이프라인 배열(3클래스). **#232 가 DS2 S 의 3/4 를 갖는다**."""
    mpid = np.repeat(_DS2 + [101, 106], PER)          # 101·106 은 DS1(마스크 밖)
    my = rng.choice([0, 2], size=len(mpid), p=[.96, .04])
    n232 = int(S_TOT * S_232)
    my[rng.choice(np.where(mpid == 232)[0], n232, replace=False)] = 1
    rest = np.where((mpid != 232) & np.isin(mpid, _DS2))[0]
    my[rng.choice(rest, S_TOT - n232, replace=False)] = 1
    return mpid, my


def make_old(mpid, my, mode, rng):
    """07-17 배열을 **현재 배열에서 파생**시킨다.

    현재 DS2 에서 (모드에 따라) 비트를 잃고, 그 위에 제4클래스 F 를 얹는다.
    F 는 현재 파이프라인에 아예 없는 클래스라 '초과분' 으로 작동한다.
    """
    te = np.isin(mpid, _DS2)
    p, y = mpid[te], my[te]
    if mode == "record":                       # 232 가 통째로 빠진다
        keep = p != 232
    elif mode == "detector":                   # 전 레코드에서 4% 씩
        keep = rng.rand(len(p)) > 0.04
    elif mode == "trap":                       # 길이가 정확히 맞도록 F 개수만큼만 뺀다
        keep = np.ones(len(p), bool)
        keep[rng.choice(len(p), N_F, replace=False)] = False
    else:
        raise ValueError(mode)
    zp, zy = p[keep], y[keep].astype(int)
    # F 는 **살아남은 레코드에만** 흩뿌린다. 통째로 빠진 레코드에 F 를 넣으면
    # 그 레코드가 0 이 아니게 돼 '레코드 소실' 이 진단에서 지워진다.
    fp = rng.choice(np.unique(zp), N_F)
    return np.concatenate([zp, fp]), np.concatenate([zy, np.full(N_F, 3)])


def build(root, mpid, my, mode, rng, with_labels=True, drop_pkl=False, trap_nsv=False):
    runs = os.path.join(root, "ecg_out", "runs_s1p"); os.makedirs(runs)
    cache = os.path.join(root, "cache"); os.makedirs(cache)
    zp, zy = make_old(mpid, my, mode, rng)
    if with_labels:
        np.savez(os.path.join(cache, "data_mit.npz"), y=zy, pid=zp,
                 beat=np.zeros((len(zy), 1), "float32"))
    n_test = len(zy)
    nsv = [int((zy == k).sum()) for k in range(3)]     # ★ N/S/V 만. 합 < n_test
    if trap_nsv:
        nsv[0] += 1; nsv[1] -= 1                       # 합·길이 유지, **구성만** 어긋남
    for n in (PKL_NAMES[:-1] if drop_pkl else PKL_NAMES):
        arm = "mit_only" if n.startswith("mit_only") else "mit_svdb"
        seed = int(n.split("_")[-1].split(".")[0])
        p = rng.rand(n_test, 4).astype("float16")      # ★ 4열 = 4클래스
        boost = 0.30 if arm == "mit_svdb" else 0.0
        p[zy == 2, 2] += boost                         # V 는 개선
        p[zy == 1, 1] -= boost * 0.7                   # S 는 악화
        pickle.dump({"arm": arm, "seed": seed, "proba": p,
                     "train_prior": np.array([.90, .03, .04, .03]),
                     "pred": p.argmax(1).astype("int8"),
                     "f1": {"N": .95, "S": .40 - boost, "V": .88 + boost, "F": .20},
                     "macro4": float(.70 + rng.rand() * .01),
                     "nsv": np.array(nsv),
                     "n_train": 50576 + (8000 if arm == "mit_svdb" else 0),
                     "n_S_train": 944 + (7452 if arm == "mit_svdb" else 0),
                     "n_pat_train": 22 + (14 if arm == "mit_svdb" else 0),
                     "mins": 12.3},
                    open(os.path.join(runs, n), "wb"))
    return n_test


def scenario(tag, mode="record", **kw):
    print("\n" + "=" * 78); print(f"### {tag}"); print("=" * 78)
    root = tempfile.mkdtemp()
    try:
        rng = np.random.RandomState(1)
        mpid, my = cur_arrays(rng)
        n_test = build(root, mpid, my, mode, rng, **kw)
        TE = np.isin(mpid, _DS2)
        g = {"os": os, "np": np, "pickle": pickle, "sys": sys,
             "DRIVE_ROOT": root, "PKL_NAMES": PKL_NAMES, "_DS2": _DS2,
             "mpid": mpid, "my": my, "TE": TE, "t_ci": t_ci,
             "run": Run(), "CONFIG": {}}
        exec(compile(SRC, "exp22a_cell3", "exec"), g)
        print(f"\n>>> AUROC 재계산 {'✅' if g.get('G1') else '건너뜀'}"
              f" · DS2 {int(TE.sum()):,} vs 07-17 {n_test:,}")
        return g
    finally:
        shutil.rmtree(root)


def note(g, s):
    return any(s in x for x in g["G1_NOTE"])


a = scenario("A) 레코드 232 가 통째로 빠짐", mode="record")
assert a.get("G1"), "A 는 길이·클래스가 맞으므로 AUROC 까지 가야 한다"
assert note(a, "누락 레코드 [232]"), "232 소실을 지목해야 한다"
assert not note(a, "분산 손실"), \
    "A 는 S 가 대량 소실되므로 '분산 손실' 이라고 말하면 안 된다"

b = scenario("B) data_mit.npz 없음", mode="record", with_labels=False)
assert b.get("G1") is None, "B 는 AUROC 를 생략해야 한다"
assert b.get("META"), "B 도 저장 지표는 회수해야 한다"

c = scenario("C) pkl 9/10 개", mode="record", drop_pkl=True)
assert c.get("G1") is None and c.get("META") is None, "C 는 조기 skip"

d = scenario("D)【R10-b】길이 정확히 일치 · 클래스 구성만 다름", mode="trap", trap_nsv=True)
assert d.get("G1") is None, "D 는 길이가 맞아도 정렬을 **거부**해야 한다"
assert note(d, "길이 일치·클래스 불일치"), "R10-b 가 잡았다고 기록해야 한다"

e = scenario("E) 전 레코드 4% 분산 손실 (검출기 가설)", mode="detector")
assert e.get("G1"), "E 도 길이·클래스가 맞으면 AUROC 까지 가야 한다"
assert note(e, "분산 손실"), "E 는 레코드 통째 누락을 배제해야 한다"
assert note(e, "누락 레코드 []"), "E 에는 통째로 빠진 레코드가 없어야 한다"

for _g, _t in ((a, "A"), (d, "D"), (e, "E")):
    assert note(_g, "4클래스"), f"{_t}: nsv 합 < n_test 에서 제4클래스를 검출해야 한다"

print("\n전부 통과 ✅ — 다섯 경로 모두 예외 없이 끝나고, A/E 를 클래스 프로파일로 가른다")
sys.exit(0)
