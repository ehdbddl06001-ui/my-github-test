"""실험22-A CELL 3b(【G1-b】)를 합성 데이터로 검정하는 픽스처.

묻는 것: F1 은 크게 떨어졌는데 AUROC 는 미결일 때, **임계값 이동인가 판별력 변화인가**.

두 시나리오를 심는다(정답을 알고 있다):
  (1) **순수 임계값 이동** — S 로짓에 상수 +1.6. softmax 에서 이건
      `p_S = sigmoid(l_S − logsumexp(나머지))` 의 인자에 상수를 더하는 것이라
      **S 확률의 순위를 정확히 보존**한다. 따라서 순위 지표는 안 움직여야 한다.
  (2) **진짜 판별력 훼손** — S 양성인 비트의 S 로짓만 −1.1. 순위가 실제로 섞인다.

★ 이 픽스처가 설계 결함을 하나 잡았다. 처음엔 판정을 **유의성**으로 했는데,
  시나리오(1)에서 PR-AUC Δ 가 −0.0003 인데 CI 가 [−0.0004, −0.0003] 으로 0 을
  제외해 '유의' 가 떴다. 시드 5개가 거의 결정론적이라 CI 가 비현실적으로 좁았던
  것이다 — **유의하지만 무의미한 값**(R5 계열). 그래서 판정을 효과크기 비
  `REL = max|Δ순위| / |ΔF1|` 로 바꿨다. (1)은 0.1%, (2)는 239% 로 즉시 갈린다.

참고: 시나리오(1)에서 **V 는 '판별력 변화'로 나오는 게 옳다.** S 로짓만 올려도
softmax 분모가 바뀌어 V 확률의 순위는 보존되지 않는다. 버그가 아니라 성질이다.
"""
import os, sys, json, pickle, shutil, tempfile
import numpy as np
from scipy import stats
from sklearn.metrics import f1_score

NB = json.load(open(os.path.join(os.path.dirname(__file__), "..",
                                 "notebooks", "exp22a_axis_transfer.ipynb")))
_c = [c for c in NB["cells"]
      if c["cell_type"] == "code" and "【G1-b】" in "".join(c["source"])]
assert len(_c) == 1, f"G1-b 셀을 {len(_c)}개 찾았다"
SRC = "".join(_c[0]["source"])          # ★ 노트북 자체를 실행한다

N = 20000
PRI = [.90, .038, .055, .007]           # N/S/V/F — 실제 DS2 와 비슷한 비율


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


def scenario(tag, mode, shuffle_labels=False):
    print("\n" + "=" * 78); print(f"### {tag}"); print("=" * 78)
    root = tempfile.mkdtemp()
    try:
        yv = np.random.RandomState(0).choice([0, 1, 2, 3], N, p=PRI)
        found, META = {}, {}
        for arm in ("mit_only", "mit_svdb"):
            for i in range(5):
                r = np.random.RandomState(100 + i)
                lg = r.normal(0, 1, (N, 4))
                lg[np.arange(N), yv] += 2.2                  # 기본 판별력
                if arm == "mit_svdb":
                    if mode == "threshold":
                        lg[:, 1] += 1.6                      # 순위 보존 이동
                    else:
                        lg[yv == 1, 1] -= 1.1                # 진짜 훼손
                e = np.exp(lg - lg.max(1, keepdims=True))
                p = (e / e.sum(1, keepdims=True)).astype("float16")
                pred = p.argmax(1)
                fn = f"{arm}_{1000+i}.pkl"
                found[fn] = os.path.join(root, fn)
                META[fn] = {"n_train": 38283 if arm == "mit_only" else 74788,
                            "n_S_train": 422 if arm == "mit_only" else 8396,
                            **{f"f1[{k}]": float(f1_score((yv == k).astype(int),
                                                          (pred == k).astype(int),
                                                          zero_division=0))
                               for k in range(4)}}
                pickle.dump({"proba": p}, open(found[fn], "wb"))
        if shuffle_labels:      # ★ 확률은 그대로, 라벨만 섞는다 → 정렬이 깨진 상태
            yv = np.random.RandomState(7).permutation(yv)
        g = {"np": np, "pickle": pickle, "yv": yv, "G1": {}, "found": found,
             "META": META, "t_ci": t_ci, "run": Run(), "CONFIG": {}, "G1_NOTE": []}
        exec(compile(SRC, "exp22a_cell3b", "exec"), g)
        return g
    finally:
        shutil.rmtree(root)


a = scenario("(1) 순수 임계값 이동 — S 로짓에 상수 +1.6 (순위 보존)", "threshold")
va = a["CONFIG"]["g1b"]
assert va["verdict"]["S"] == "임계값 이동", f"시나리오1 오판: {va['verdict']}"
assert va["f1_recheck_ok"], "무결성 검증(재계산 F1 vs 저장 f1)이 실패했다"

b = scenario("(2) 진짜 판별력 훼손 — S 양성의 S 로짓만 −1.1", "discrim")
vb = b["CONFIG"]["g1b"]
assert vb["verdict"]["S"] == "판별력 변화", f"시나리오2 오판: {vb['verdict']}"
assert vb["f1_recheck_ok"], "무결성 검증이 실패했다"

# 무결성 검증이 **실제로 감시하고 있는지** — 라벨을 망가뜨리면 잡아야 한다.
#   이게 없으면 "재계산 F1 == 저장 f1" 은 항상 참인 무의미한 도장일 수 있다.
c = scenario("(3) 확률은 그대로, **라벨만 셔플** → 무결성 검증이 걸려야 한다",
             "threshold", shuffle_labels=True)
assert not c["CONFIG"]["g1b"]["f1_recheck_ok"], \
    "라벨을 셔플했는데 무결성 검증이 통과했다 — 검증이 아무것도 안 지키고 있다"
print("  ✅ 셔플된 라벨을 무결성 검증이 잡아냈다")

print("\n전부 통과 ✅ — 임계값 이동과 판별력 변화를 효과크기 비로 가른다")
sys.exit(0)
