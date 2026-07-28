# =============================================================================
#  rhythm_bench.py  —  리듬(질환) 분류 벤치마크.  RSN 백본을 질환 축에 적용한다.
#
#  ── 왜 별도 하니스인가 ─────────────────────────────────────────────────────
#  svdb_bench 는 처음부터 끝까지 **S vs 나머지 이진**으로 짜여 있다(`_prf` 의
#  `yp=(yy==1)`). 리듬은 다중 클래스이고 평가 단위도 다르므로 재사용할 수 없다.
#  다만 **규율은 그대로 가져온다**: 환자 GroupKFold, calib 에서만 임계 결정,
#  환자단위 매크로 + 대응 부트스트랩, arm 레지스트리.
#
#  ── 비트 클래스와 리듬은 직교한다 (핵심) ────────────────────────────────────
#   비트 클래스(AAMI N/S/V/F/Q) = 이 박이 **어디서 기원**했나
#   리듬 라벨(AFIB/VT/B/T)      = 이 구간이 **무슨 부정맥**인가
#  AFIB 구간의 박은 대부분 AAMI class N 이다(심방이 세동해도 심실로는 정상 전도).
#  → **질환 진단은 리듬 축에 있지 비트 클래스 축에 있지 않다.**
#
#  ── 실측 규모 (db_audit 결과, 레코드 8개 이상만) ────────────────────────────
#     N    80,865비트 / 43레코드      B(이단맥)  3,288 / 12
#     AFIB 16,631     / 10           T(삼단맥)  1,360 / 12
#                                    VT           399 / 13   ← 레코드당 30비트뿐
#  ⚠ 리듬 주석은 사실상 MIT-BIH 에만 있다(svdb 는 99.25%, incart 는 92.4% 가 미상).
#    → 이 과제의 환자 수는 약 54명. SVDB(73명)보다 적어 **검정력이 낮다**.
#    → MDE 를 SVDB 기준(0.07)으로 잡으면 안 된다. 아래 mde 인자로 데이터에서 계산한다.
#
#  ── 왜 RSN 이 여기에 맞는가 ─────────────────────────────────────────────────
#  AF 는 **정의상 RR 불규칙**이다. SVEB 에서 아무 이득이 없던 Poincaré 채널
#  (PAPER §7-N1 이 'AF 는 확산 구름, 이소성은 이산 군집'이라 적어둔 그것)이
#  여기서는 **주 신호**가 된다. 리듬 채널이 무차원이라 DB 를 섞어도 축이 안 흔들린다.
#
#  ⚠ 다만 창 길이를 바꿔야 한다: K=8(17슬롯)은 비트 이소성용이다. AF·VT 는
#    수십 박 지속 상태이므로 K=32(65슬롯)를 기본으로 한다. TCN 수용야는
#    svdb_rhythm._rsn 이 L 에 맞춰 자동으로 층을 늘린다(65 → conv 5층).
#
#  선행: build_multi() 로 ecg_multi.npz 생성, svdb_rhythm.py 로드
#  실행:
#    OUT = bench_rhythm(n_rep=1)      # A0/A1/A2 + 등록된 확장 arm
#    report_rhythm(OUT)               # 클래스별 대응 부트스트랩
#
#  자기검증: python rhythm_bench.py --selftest
# =============================================================================
import numpy as np

_BASE = globals().get("_BASE", "/content/drive/MyDrive/mitbih")

RHY_ARMS = {}


def register_rhythm_arm(name, fn):
    if not callable(fn):
        raise TypeError("fn 은 호출 가능해야 합니다")
    RHY_ARMS[name] = fn
    return name


def clear_rhythm_arms():
    RHY_ARMS.clear()


# ─────────────────────────────────────────────────────────────────────────────
#  1. 데이터 준비
# ─────────────────────────────────────────────────────────────────────────────
def load_task(path=None, task="rhythm", min_records=8, exclude=("(미상)",), verbose=True):
    """ecg_multi.npz → 과제용 부분집합.

    task="rhythm" : 리듬(질환) 라벨 — AFIB/B/T/VT ...
    task="beat5"  : AAMI 5-class 비트 라벨 — N/S/V/F/Q
    ★두 축은 직교한다(AFIB 구간의 박은 대부분 AAMI N). 같은 하니스로 둘 다 돈다.

    ★'(미상)' 은 **클래스가 아니라 '주석이 없음'** 이다. 클래스로 넣으면
      "리듬 주석이 안 달린 구간"을 학습·평가하게 되어 무의미하다. 반드시 제외한다.
    ★레코드 수가 min_records 미만인 리듬도 제외한다 — 환자분리 평가가 성립하지
      않는 클래스를 넣으면 매크로 지표가 몇 명의 우연에 좌우된다(HANDOFF §2).
      제외된 비트는 학습에서도 뺀다(다른 클래스로 오염시키지 않기 위해).
    """
    d = np.load(path or f"{_BASE}/ecg_multi.npz", allow_pickle=True)
    beat, pid, pre, post = d["beat"], d["pid"], d["pre_rr"], d["post_rr"]
    if task == "beat5":
        rhy = d["y5"]; names = ["N", "S", "V", "F", "Q"]; exclude = ()
    else:
        rhy = d["rhythm"]; names = [str(x) for x in d["rhythm_names"]]
    y5 = d["y5"] if "y5" in d else None
    keep_ids, kept = [], []
    for i, nm in enumerate(names):
        if nm in exclude:
            continue
        m = rhy == i
        nrec = len(np.unique(pid[m]))
        if nrec >= min_records:
            keep_ids.append(i); kept.append((nm, int(m.sum()), nrec))
    if not keep_ids:
        raise RuntimeError("남는 리듬 클래스가 없습니다 — min_records 를 낮추거나 "
                           "build_multi 에 mitdb 를 포함했는지 확인하세요.")
    sel = np.isin(rhy, keep_ids)
    remap = {old: new for new, old in enumerate(keep_ids)}
    y = np.array([remap[v] for v in rhy[sel]], np.int64)
    cls = [names[i] for i in keep_ids]
    out = dict(beat=beat[sel], y=y, pid=pid[sel], pre=pre[sel], post=post[sel],
               classes=cls, y5=(y5[sel] if y5 is not None else None),
               db=(d["db"][sel] if "db" in d else None))
    if verbose:
        print(f"[{task}] 데이터: {len(y):,}비트  환자 {len(np.unique(out['pid']))}명  "
              f"클래스 {len(cls)}종")
        print(f"  {'클래스':<8}{'비트':>10}{'레코드':>8}{'비율':>8}")
        for nm, nb, nr in kept:
            print(f"  {nm:<8}{nb:>10,}{nr:>8}{100*nb/len(y):>7.2f}%")
        drop = int((~sel).sum())
        print(f"  제외 {drop:,}비트 (미상 + 레코드<{min_records} 클래스)")
        if task == "rhythm":
            print(f"  ⚠ 리듬 주석은 사실상 MIT-BIH 에만 있다 → 환자 수가 SVDB(73)보다 적다")
    return out


def load_rhythm(path=None, min_records=8, exclude=("(미상)",), verbose=True):
    """하위호환 별칭."""
    return load_task(path, "rhythm", min_records, exclude, verbose)


def mde_estimate(pid, y, cls, sigma=0.32, verbose=True):
    """이 데이터에서 검출 가능한 최소 효과(MDE)를 **클래스별로** 계산한다.

    ★SVDB 의 0.07 을 그대로 쓰면 안 된다. MDE 는 '그 클래스를 가진 환자 수'로
      정해지고, 리듬 클래스마다 그 수가 10~43 으로 크게 다르다.
    """
    out = {}
    for c, nm in enumerate(cls):
        n = len(np.unique(pid[y == c]))
        out[nm] = (float(1.96 * sigma / max(np.sqrt(n), 1)), n)
    if verbose:
        print(f"\n  [검정력] 환자별 F1 의 σ≈{sigma} 가정")
        print(f"  {'클래스':<8}{'환자':>6}{'95%CI 반폭':>12}  판정 가능 최소 효과")
        for nm, (h, n) in out.items():
            print(f"  {nm:<8}{n:>6}{h:>11.3f}   {h:.2f}")
        print(f"  ※ SVDB 의 MDE 0.07 을 그대로 쓰면 안 된다 — 클래스마다 다르다.")
    return out


# ─────────────────────────────────────────────────────────────────────────────
#  2. 지표 — 클래스별 '환자단위 매크로 F1' (SVEB 때와 같은 구조)
# ─────────────────────────────────────────────────────────────────────────────
def _f1(v, yp):
    tp = float((v & yp).sum()); fp = float((v & ~yp).sum()); fn = float((~v & yp).sum())
    pr = tp / (tp + fp + 1e-9); se = tp / (tp + fn + 1e-9)
    return 2 * pr * se / (pr + se + 1e-9), pr, se


def per_class_macro(pred, y, pid, cls, B=2000, seed=0):
    """클래스 c 마다: c 를 가진 환자들의 'c vs 나머지' F1 을 평균.

    ★SVEB 때의 '환자단위 매크로 F1' 과 정확히 같은 구조다. 그래야 두 과제의
      수치를 같은 잣대로 읽을 수 있다.
    """
    res = {}
    rng = np.random.RandomState(seed)
    for c, nm in enumerate(cls):
        ps = np.array([p for p in np.unique(pid) if (y[pid == p] == c).any()])
        if len(ps) == 0:
            continue
        f = np.array([_f1(pred[pid == p] == c, y[pid == p] == c)[0] for p in ps])
        bs = np.array([f[rng.randint(0, len(f), len(f))].mean() for _ in range(B)])
        gp, gr, gs = _f1(pred == c, y == c)
        res[nm] = dict(macro=float(f.mean()), ci=(float(np.percentile(bs, 2.5)),
                                                  float(np.percentile(bs, 97.5))),
                       n=len(ps), fper=f, pids=ps, micro=gp, prec=gr, sen=gs)
    return res


# ─────────────────────────────────────────────────────────────────────────────
#  3. 기준선 모델
# ─────────────────────────────────────────────────────────────────────────────
def _mlp(din, ncls):
    import torch.nn as nn
    return nn.Sequential(nn.Linear(din, 64), nn.ReLU(), nn.Dropout(0.1),
                         nn.Linear(64, 64), nn.ReLU(), nn.Linear(64, ncls))


def _rr_scalars(pre, post, pid, W=64):
    """A1 기준선용 RR 스칼라 — '시퀀스 없이 요약만' 준 경우를 재현한다.
       RSN(A2) 과의 차이가 곧 '시퀀스화의 효과'가 되도록 정보량을 맞춘다."""
    FS = 360.0
    a = np.asarray(pre, float) / FS; b = np.asarray(post, float) / FS
    F = np.zeros((len(a), 8), "float32")
    for p in np.unique(pid):
        m = np.flatnonzero(pid == p)
        x = a[m]
        pad = np.concatenate([np.full(W - 1, x[0]), x])
        sw = np.lib.stride_tricks.sliding_window_view(pad, W)
        med = np.median(sw, 1); sd = np.std(sw, 1)
        dif = np.abs(np.diff(sw, axis=1))
        F[m, 0] = x; F[m, 1] = b[m]; F[m, 2] = med
        F[m, 3] = np.clip(x / np.maximum(med, 1e-3), 0, 4)
        F[m, 4] = sd / np.maximum(med, 1e-3)                      # 변동계수
        F[m, 5] = dif.mean(1) / np.maximum(med, 1e-3)             # RMSSD 유사
        F[m, 6] = (dif > 0.05).mean(1)                            # pNN50 유사
        F[m, 7] = np.median(dif, 1) / np.maximum(med, 1e-3)
    return np.nan_to_num(F)


def _fit_mlp(F, y, tr, te, ncls, seed, epochs=20, bs=512):
    import torch
    import torch.nn.functional as Fn
    from sklearn.preprocessing import RobustScaler
    dev = "cuda" if torch.cuda.is_available() else "cpu"
    torch.manual_seed(seed); np.random.seed(seed)
    sc = RobustScaler().fit(F[tr])
    T = lambda X: np.nan_to_num(sc.transform(X), posinf=0, neginf=0).astype("float32")
    M = _mlp(F.shape[1], ncls).to(dev)
    opt = torch.optim.AdamW(M.parameters(), lr=1e-3, weight_decay=1e-4)
    cnt = np.array([(y[tr] == c).sum() for c in range(ncls)], np.float64)
    cw = torch.tensor((cnt.sum() / np.maximum(cnt, 1)) ** 0.5, dtype=torch.float32, device=dev)
    ds = torch.utils.data.TensorDataset(torch.from_numpy(T(F[tr])), torch.from_numpy(y[tr]))
    dl = torch.utils.data.DataLoader(ds, batch_size=bs, shuffle=True)
    for _ in range(epochs):
        M.train()
        for xb, yb in dl:
            xb, yb = xb.to(dev), yb.to(dev)
            opt.zero_grad()
            Fn.cross_entropy(M(xb), yb, weight=cw).backward()
            torch.nn.utils.clip_grad_norm_(M.parameters(), 1.0); opt.step()
    M.eval()
    with torch.no_grad():
        Xt = torch.from_numpy(T(F[te])).to(dev)
        return M(Xt).argmax(1).cpu().numpy()


# ─────────────────────────────────────────────────────────────────────────────
#  4. 하니스
# ─────────────────────────────────────────────────────────────────────────────
def bench_rhythm(n_rep=1, k=5, K=32, min_records=8, path=None, only=None,
                 epochs=20, split="patient", verbose=True):
    """리듬 분류 벤치. 규율은 SVEB 하니스와 동일(환자 GroupKFold, 결정론적 분할).

    split="patient" : 환자 GroupKFold (기본)
    split="db"      : ★leave-one-DB-out — 한 DB 를 통째로 빼고 학습, 그 DB 로 평가.
                      **DB 조건부 가중치의 진위를 가르는 유일한 검정**이다.
                      같은 DB 안에서만 오르고 여기서 무너지면 사전확률 암기다.
                      (테스트 DB 의 도메인 임베딩은 학습에서 본 적이 없으므로
                       평균 도메인으로 폴백된다 — 그게 정직한 배포 조건이다.)
    """
    from sklearn.model_selection import GroupKFold
    D = load_rhythm(path=path, min_records=min_records, verbose=verbose)
    beat, y, pid, pre, post, cls = (D["beat"], D["y"], D["pid"], D["pre"],
                                    D["post"], D["classes"])
    ncls = len(cls)
    mde = mde_estimate(pid, y, cls, verbose=verbose)
    g = globals()
    _want = lambda nm: (only is None) or (nm in only)

    ARMS = ["A0.다수결", "A1.RR스칼라", "A2.RSN-리듬"]
    ARMS += [a for a in RHY_ARMS if a not in ARMS]
    if only is not None:
        ARMS = [a for a in ARMS if a in only]
    acc = {a: [] for a in ARMS}; order = []; dead = set()

    # RSN 문맥 — 리듬용 긴 창
    ctxc = None
    if any(_want(a) for a in ("A2.RSN-리듬",)) or RHY_ARMS:
        rc = g.get("rr_context")
        if rc is None:
            raise RuntimeError("svdb_rhythm.py 를 먼저 로드하세요(rr_context 없음).")
        if verbose:
            print(f"\nRSN 문맥 계산: K=±{K} (창 {2*K+1}슬롯) — AF·VT 는 지속 상태라 긴 문맥이 필요")
        ctxc = rc(pre, post, pid, K=K, poincare=True, verbose=verbose)

    FRR = _rr_scalars(pre, post, pid) if _want("A1.RR스칼라") else None

    # 분할 생성
    if split == "db":
        dbv = D.get("db")
        if dbv is None:
            raise RuntimeError("npz 에 db 열이 없습니다 — build_multi 로 만든 파일이 필요합니다.")
        uds = [d for d in np.unique(dbv) if (dbv == d).sum() > 0]
        folds = []
        for d in uds:
            te = np.flatnonzero(dbv == d); tr = np.flatnonzero(dbv != d)
            # 그 DB 에만 있는 클래스는 학습에서 못 보므로 평가에서 뺀다(불가능한 문제 방지)
            seen = set(np.unique(y[tr]).tolist())
            keep = np.isin(y[te], list(seen))
            if keep.sum() < len(te) and verbose:
                print(f"  [LODO {d}] 학습에 없는 클래스의 비트 {int((~keep).sum()):,}개 평가 제외")
            folds.append((tr, te[keep], str(d)))
        if verbose:
            print(f"\n★leave-one-DB-out: {len(folds)}폴드 {[f[2] for f in folds]}")
            print(f"  DB 조건부 가중치가 여기서도 이기면 진짜, 여기서만 무너지면 사전확률 암기다.")
    else:
        gkf = GroupKFold(n_splits=k)
        folds = [(a, b, None) for a, b in gkf.split(np.arange(len(y)), y, groups=pid)]

    for rep in range(n_rep):
        for fi, (tr, te, tag) in enumerate(folds):
            seed = 100 * rep + fi
            order.append(te)
            if _want("A0.다수결"):
                maj = np.bincount(y[tr], minlength=ncls).argmax()
                acc["A0.다수결"].append(np.full(len(te), maj, np.int64))
            if _want("A1.RR스칼라"):
                acc["A1.RR스칼라"].append(_fit_mlp(FRR, y, tr, te, ncls, seed, epochs))
            if _want("A2.RSN-리듬"):
                acc["A2.RSN-리듬"].append(
                    _fit_rsn_rhythm(ctxc, beat, y, tr, te, ncls, seed, epochs))
            for nm, fn in RHY_ARMS.items():
                if nm in dead or not _want(nm):
                    continue
                try:
                    v = np.asarray(fn(dict(beat=beat, y=y, pid=pid, pre=pre, post=post,
                                           tr=tr, te=te, ncls=ncls, seed=seed,
                                           ctx=ctxc, classes=cls))).astype(np.int64).reshape(-1)
                    if v.shape != (len(te),):
                        raise ValueError(f"길이 {v.shape} != {len(te)}")
                    acc[nm].append(v)
                except Exception as e:
                    print(f"  ⚠ arm '{nm}' 실패 → 제외: {type(e).__name__}: {e}")
                    dead.add(nm)
            if verbose:
                print(f"  rep{rep} fold{fi}{'('+tag+')' if tag else ''} 완료 "
                      f"(train {len(tr):,} / test {len(te):,})")
    if dead:
        ARMS = [a for a in ARMS if a not in dead]
    idx = np.concatenate(order); yA = y[idx]; pA = pid[idx]
    RES = {}
    print(f"\n=== 리듬 분류 결과 (클래스별 환자단위 매크로 F1) ===")
    print(f"  {'arm':<14}" + "".join(f"{c:>12}" for c in cls) + f"{'평균':>10}")
    for a in ARMS:
        v = np.concatenate(acc[a])
        pc = per_class_macro(v, yA, pA, cls)
        RES[a] = dict(per_class=pc, pred=v,
                      mean=float(np.mean([pc[c]["macro"] for c in pc])))
        print(f"  {a:<14}" + "".join(f"{pc[c]['macro']:>12.3f}" if c in pc else f"{'—':>12}"
                                     for c in cls) + f"{RES[a]['mean']:>10.3f}")
    print(f"\n  ※ 클래스마다 환자 수가 달라 MDE 가 다르다(위 검정력 표). 평균은 참고용.")
    if split == "db":
        print(f"\n  ★이 수치는 leave-one-DB-out 이다 — 학습에서 본 적 없는 DB 로 평가했다.")
        print(f"    환자 GroupKFold 수치보다 낮은 것이 정상이며, 그 격차가 'DB 특화로")
        print(f"    얻은 것 중 전이되지 않는 몫'이다.")
    return dict(res=RES, y=yA, pid=pA, order=idx, classes=cls, mde=mde,
                arms=ARMS, dead=sorted(dead), split=split)


def _fit_rsn_rhythm(c, beat, y, tr, te, ncls, seed, epochs=20, bs=512):
    """RSN 을 리듬 다중분류로. 모델은 svdb_rhythm._rsn 을 n_class 로 재사용."""
    import torch
    import torch.nn.functional as Fn
    from sklearn.preprocessing import RobustScaler
    g = globals()
    _rsn = g.get("_rsn")
    if _rsn is None:
        raise RuntimeError("svdb_rhythm.py 를 먼저 로드하세요(_rsn 없음).")
    SEQ, AUX = c["seq"], c["aux"]
    dev = "cuda" if torch.cuda.is_available() else "cpu"
    torch.manual_seed(seed); np.random.seed(seed)
    sc = RobustScaler().fit(AUX[tr])
    T = lambda X: np.nan_to_num(sc.transform(X), posinf=0, neginf=0).astype("float32")
    M = _rsn(SEQ.shape[1], SEQ.shape[2], AUX.shape[1], n_class=ncls).to(dev)
    opt = torch.optim.AdamW(M.parameters(), lr=1e-3, weight_decay=1e-4)
    cnt = np.array([(y[tr] == cc).sum() for cc in range(ncls)], np.float64)
    cw = torch.tensor((cnt.sum() / np.maximum(cnt, 1)) ** 0.5, dtype=torch.float32, device=dev)
    ds = torch.utils.data.TensorDataset(torch.from_numpy(SEQ[tr]), torch.from_numpy(beat[tr]),
                                        torch.from_numpy(T(AUX[tr])), torch.from_numpy(y[tr]))
    dl = torch.utils.data.DataLoader(ds, batch_size=bs, shuffle=True)
    for _ in range(epochs):
        M.train()
        for sq, bt, ax, yb in dl:
            sq, bt, ax, yb = (t.to(dev) for t in (sq, bt, ax, yb))
            opt.zero_grad()
            Fn.cross_entropy(M(sq, bt, ax), yb, weight=cw).backward()
            torch.nn.utils.clip_grad_norm_(M.parameters(), 1.0); opt.step()
    M.eval(); Ate = T(AUX[te]); o = []
    with torch.no_grad():
        for i in range(0, len(te), 4096):
            sl = te[i:i + 4096]
            o.append(M(torch.from_numpy(SEQ[sl]).to(dev),
                       torch.from_numpy(beat[sl]).to(dev),
                       torch.from_numpy(Ate[i:i + 4096]).to(dev)).argmax(1).cpu().numpy())
    return np.concatenate(o)


# ─────────────────────────────────────────────────────────────────────────────
#  5. 전이 실험 — "통합 학습 → 해당 DB 로 미세조정" 이 정말 이득인가
# ─────────────────────────────────────────────────────────────────────────────
def _fit_rsn_generic(c, beat, y, tr, te, ncls, seed, epochs, lr=1e-3,
                     init=None, ft_scope="all", bs=512, ret_model=False):
    """RSN 학습. init 이 주어지면 그 가중치에서 시작(= 미세조정)."""
    import copy
    import torch
    import torch.nn.functional as Fn
    from sklearn.preprocessing import RobustScaler
    g = globals(); _rsn = g["_rsn"]
    SEQ, AUX = c["seq"], c["aux"]
    dev = "cuda" if torch.cuda.is_available() else "cpu"
    torch.manual_seed(seed); np.random.seed(seed)
    sc = RobustScaler().fit(AUX[tr])
    T = lambda X: np.nan_to_num(sc.transform(X), posinf=0, neginf=0).astype("float32")
    M = _rsn(SEQ.shape[1], SEQ.shape[2], AUX.shape[1], n_class=ncls).to(dev)
    if init is not None:
        M.load_state_dict(copy.deepcopy(init))
        if ft_scope == "head":
            # ★인코더를 얼리면 '파국적 망각'을 막는다. 통합 학습으로 얻은 표현
            #   (특히 희소 클래스 F/Q 는 mitdb 에만 있다)을 미세조정이 지워버리는
            #   것을 방지하려는 것. 대신 적응력은 떨어진다 — 둘 다 재볼 것.
            for n_, p_ in M.named_parameters():
                p_.requires_grad = n_.startswith("cls") or n_.startswith("dg") or n_.startswith("dbi")
    opt = torch.optim.AdamW([p_ for p_ in M.parameters() if p_.requires_grad],
                            lr=lr, weight_decay=1e-4)
    cnt = np.array([(y[tr] == cc).sum() for cc in range(ncls)], np.float64)
    cw = torch.tensor((cnt.sum() / np.maximum(cnt, 1)) ** 0.5, dtype=torch.float32, device=dev)
    ds = torch.utils.data.TensorDataset(torch.from_numpy(SEQ[tr]), torch.from_numpy(beat[tr]),
                                        torch.from_numpy(T(AUX[tr])), torch.from_numpy(y[tr]))
    dl = torch.utils.data.DataLoader(ds, batch_size=bs, shuffle=True)
    for _ in range(epochs):
        M.train()
        for sq, bt, ax, yb in dl:
            sq, bt, ax, yb = (t.to(dev) for t in (sq, bt, ax, yb))
            opt.zero_grad()
            Fn.cross_entropy(M(sq, bt, ax), yb, weight=cw).backward()
            torch.nn.utils.clip_grad_norm_(M.parameters(), 1.0); opt.step()
    M.eval(); Ate = T(AUX[te]); o = []
    with torch.no_grad():
        for i in range(0, len(te), 4096):
            sl = te[i:i + 4096]
            o.append(M(torch.from_numpy(SEQ[sl]).to(dev), torch.from_numpy(beat[sl]).to(dev),
                       torch.from_numpy(Ate[i:i + 4096]).to(dev)).argmax(1).cpu().numpy())
    pred = np.concatenate(o)
    return (pred, {k2: v.detach().cpu().clone() for k2, v in M.state_dict().items()}) \
        if ret_model else pred


def bench_transfer(task="beat5", path=None, K=8, k=5, epochs=20, ft_epochs=5,
                   ft_lr=2e-4, ft_scope="all", min_records=8, verbose=True):
    """★"통합 학습 → 해당 DB 미세조정" 이 정말 이득인가 — 3자 비교.

    같은 홀드아웃 환자로 세 가지를 비교한다(대응 비교가 성립한다):
      P0.단독      그 DB 의 학습 환자만으로 학습        ← 지금까지의 방식
      P1.통합      전 DB 의 학습 환자로 학습            ← 표본은 늘지만 도메인이 섞임
      P2.통합→미세 P1 에서 시작해 그 DB 로 미세조정      ← ★제안하신 방식

    ★이 설계가 답하는 것:
      P1 > P0 이면 → 다른 DB 를 합치는 것 자체가 이득이다(희소 클래스에 특히).
      P2 > P1 이면 → 도메인 특화가 추가 이득을 준다.
      P2 ≈ P1 이면 → 미세조정은 불필요하다(통합만으로 충분).
      P2 < P1 이면 → **파국적 망각**. ft_scope="head" 로 다시 볼 것.

    ★무결성: 미세조정은 **그 DB 의 학습 환자만** 쓴다. 홀드아웃 환자는 어느
      단계에서도 보지 않는다. 이건 '이 병원의 라벨 일부를 갖고 있다'는 현실적
      배포 시나리오이며, zero-shot 전이(=LODO)와는 다른 질문이다.
    """
    from sklearn.model_selection import GroupKFold
    D = load_task(path=path, task=task, min_records=min_records, verbose=verbose)
    beat, y, pid, pre, post, cls = (D["beat"], D["y"], D["pid"], D["pre"],
                                    D["post"], D["classes"])
    dbv = D.get("db")
    if dbv is None:
        raise RuntimeError("npz 에 db 열이 없습니다 — build_multi 로 만든 파일이 필요합니다.")
    ncls = len(cls)
    g = globals()
    if verbose:
        print(f"\nRSN 문맥 계산: K=±{K}")
    c = g["rr_context"](pre, post, pid, K=K, poincare=True, verbose=verbose)

    uds = sorted(set(map(str, dbv)))
    # ★비용 경고 — 폴드마다 3회 학습이고 P1 은 매번 전체 데이터를 본다.
    nfit = 3 * k * len(uds)
    print(f"\n  ⚠ 학습 {nfit}회 예정 (DB {len(uds)} × {k}폴드 × 3모델)."
          f"  P1 은 매번 {len(y):,}비트 전체를 본다.")
    print(f"    SVDB 벤치(184k비트 15회)가 수십 분이었으니 여기는 **수 시간**일 수 있다.")
    print(f"    먼저 k=3, epochs=10 으로 감을 잡고 늘리는 것을 권한다.")
    acc = {a: [] for a in ("P0.단독", "P1.통합", "P2.통합→미세")}
    order = []
    for db in uds:
        inn = np.flatnonzero(np.array(list(map(str, dbv))) == db)
        pin = pid[inn]
        if len(np.unique(pin)) < k:
            print(f"  ⚠ {db}: 환자 {len(np.unique(pin))}명 < {k}폴드 → 건너뜀"); continue
        out_idx = np.flatnonzero(np.array(list(map(str, dbv))) != db)
        gkf = GroupKFold(n_splits=k)
        for fi, (a_, b_) in enumerate(gkf.split(inn, y[inn], groups=pin)):
            tr_d, te = inn[a_], inn[b_]
            tr_all = np.concatenate([tr_d, out_idx])
            seed = 1000 * uds.index(db) + fi
            order.append(te)
            acc["P0.단독"].append(_fit_rsn_generic(c, beat, y, tr_d, te, ncls, seed, epochs))
            p1, w = _fit_rsn_generic(c, beat, y, tr_all, te, ncls, seed, epochs,
                                     ret_model=True)
            acc["P1.통합"].append(p1)
            acc["P2.통합→미세"].append(
                _fit_rsn_generic(c, beat, y, tr_d, te, ncls, seed, ft_epochs,
                                 lr=ft_lr, init=w, ft_scope=ft_scope))
            if verbose:
                print(f"  {db} fold{fi}: 단독 {len(tr_d):,} / 통합 {len(tr_all):,} "
                      f"/ 테스트 {len(te):,}")
    idx = np.concatenate(order); yA = y[idx]; pA = pid[idx]
    dbA = np.array(list(map(str, dbv)))[idx]
    RES = {}
    print(f"\n=== 전이 실험 [{task}] (클래스별 환자단위 매크로 F1) ===")
    print(f"  {'arm':<14}" + "".join(f"{cc:>10}" for cc in cls) + f"{'평균':>9}")
    for a in acc:
        v = np.concatenate(acc[a])
        pc = per_class_macro(v, yA, pA, cls)
        RES[a] = dict(per_class=pc, pred=v,
                      mean=float(np.mean([pc[cc]["macro"] for cc in pc])))
        print(f"  {a:<14}" + "".join(f"{pc[cc]['macro']:>10.3f}" if cc in pc else f"{'—':>10}"
                                     for cc in cls) + f"{RES[a]['mean']:>9.3f}")
    print(f"\n  [DB별]")
    for db in uds:
        m = dbA == db
        if not m.any():
            continue
        print(f"    {db:<10}" + "  ".join(
            f"{a.split('.')[0]} {np.mean([q['macro'] for q in per_class_macro(RES[a]['pred'][m], yA[m], pA[m], cls).values()]):.3f}"
            for a in acc))
    d10 = RES["P1.통합"]["mean"] - RES["P0.단독"]["mean"]
    d21 = RES["P2.통합→미세"]["mean"] - RES["P1.통합"]["mean"]
    print(f"\n  통합의 효과   P1−P0 = {d10:+.3f}")
    print(f"  미세조정 효과 P2−P1 = {d21:+.3f}")
    if d21 < -0.01:
        print(f"    ⚠ 미세조정이 오히려 나쁘다 — 파국적 망각 의심."
              f" ft_scope='head' 로 인코더를 얼리고 다시 볼 것.")
    elif abs(d21) <= 0.01:
        print(f"    → 미세조정이 사실상 무효. 통합 학습만으로 충분하다는 뜻.")
    return dict(res=RES, y=yA, pid=pA, db=dbA, order=idx, classes=cls, task=task)


def report_rhythm(OUT, base="A1.RR스칼라", B=5000, show=True):
    """클래스별 대응 부트스트랩. MDE 는 **클래스마다 다른 값**을 쓴다."""
    R = OUT["res"]; cls = OUT["classes"]; mde = OUT["mde"]
    arms = [a for a in R if a != base and a != "A0.다수결"]
    k = max(1, len(arms) * len(cls))
    out = {}
    if show:
        print(f"\n=== 리듬 판정 (기준 {base}, Bonferroni k={k} = arm{len(arms)}×클래스{len(cls)}) ===")
    for a in arms:
        for c in cls:
            pa = R[a]["per_class"].get(c); pb = R[base]["per_class"].get(c)
            if pa is None or pb is None:
                continue
            d = np.asarray(pa["fper"]) - np.asarray(pb["fper"])
            rng = np.random.RandomState(0); n = len(d)
            bs = np.array([d[rng.randint(0, n, n)].mean() for _ in range(B)])
            al = 0.05 / k
            lo, hi = np.percentile(bs, [2.5, 97.5])
            blo, bhi = np.percentile(bs, [100 * al / 2, 100 * (1 - al / 2)])
            m = mde[c][0]
            ok = (d.mean() >= m) and (blo > 0)
            out[f"{a}|{c}"] = dict(delta=float(d.mean()), ci=(lo, hi), bonf=(blo, bhi),
                                   mde=m, meets=bool(ok), n=n)
            if show:
                v = "★확증" if blo > 0 or bhi < 0 else "유의하지 않음"
                print(f"  {a} − {base} [{c}]: Δ={d.mean():+.3f} "
                      f"[{lo:+.3f},{hi:+.3f}] Bonf[{blo:+.3f},{bhi:+.3f}] {v}"
                      + (f"  ★Δ≥MDE({m:.2f})" if ok else f"  (MDE {m:.2f} 미달)"))
    if show:
        print(f"\n  ※ MDE 가 클래스마다 다르다 — 환자 수가 다르기 때문이다.")
        print(f"     VT 처럼 환자당 비트가 30개뿐인 클래스는 F1 자체가 불안정하다.")
    return out


# ─────────────────────────────────────────────────────────────────────────────
#  5. 자기검증
# ─────────────────────────────────────────────────────────────────────────────
def selftest():
    import os
    import tempfile
    ok = lambda c, m: (_ for _ in ()).throw(AssertionError(m)) if not c else print(f"  ✔ {m}")
    print("=== rhythm_bench 자기검증 ===")
    g = globals()
    if "_rsn" not in g:
        here = os.path.dirname(os.path.abspath(__file__))
        exec(open(f"{here}/svdb_rhythm.py").read(), g)

    # 합성: 4 리듬 × 여러 환자. AF 는 '불규칙하게 불규칙', 이단맥은 짧-긴 교대.
    rng = np.random.RandomState(0)
    BE = []; RH = []; PI = []; PR = []; PO = []
    names = ["N", "AFIB", "B", "RARE"]
    plan = [(0, 12), (1, 10), (2, 10), (3, 2)]          # (리듬, 환자수) — RARE 는 2명뿐
    p = 0
    for r, npat in plan:
        for _ in range(npat):
            n = 400; base = rng.uniform(0.7, 1.0)
            if r == 0:
                rr = base * rng.uniform(0.95, 1.05, n)
            elif r == 1:
                rr = base * rng.uniform(0.6, 1.5, n)              # AF: 확산
            elif r == 2:
                rr = base * np.where(np.arange(n) % 2 == 0, 0.65, 1.3)  # 이단맥: 교대
            else:
                rr = base * rng.uniform(0.9, 1.1, n)
            BE.append(rng.randn(n, 2, 300).astype("float32") * 0.1)
            RH.append(np.full(n, r)); PI.append(np.full(n, p))
            PR.append(rr * 360); PO.append(np.roll(rr, -1) * 360)
            p += 1
    beat = np.concatenate(BE); rhy = np.concatenate(RH).astype(np.int64)
    pid = np.concatenate(PI).astype(np.int64)
    pre = np.concatenate(PR).astype("float32"); post = np.concatenate(PO).astype("float32")
    td = tempfile.mkdtemp()
    np.savez(f"{td}/ecg_multi.npz", beat=beat, y5=np.zeros(len(rhy), np.int64),
             y3=np.zeros(len(rhy), np.int64), pid=pid, pre_rr=pre, post_rr=post,
             rhythm=rhy, rhythm_names=np.array(names + ["(미상)"]),
             sym=np.array(["N"] * len(rhy)), db=np.array(["t"] * len(rhy)),
             rr_edge=np.zeros(len(rhy), bool))

    D = load_rhythm(path=f"{td}/ecg_multi.npz", min_records=8, verbose=False)
    ok(D["classes"] == ["N", "AFIB", "B"], f"레코드<8 클래스 제외됨 → {D['classes']}")
    ok("(미상)" not in D["classes"], "'(미상)' 은 클래스가 아니라 제외 대상")
    ok(len(D["y"]) == 400 * 32, f"RARE 2명 비트가 빠짐 ({len(D['y']):,})")

    m = mde_estimate(D["pid"], D["y"], D["classes"], verbose=False)
    ok(m["N"][1] == 12 and m["AFIB"][1] == 10, "클래스별 환자 수 집계")
    ok(m["AFIB"][0] > m["N"][0], "환자 적은 클래스의 MDE 가 더 크다")

    pm = per_class_macro(D["y"], D["y"], D["pid"], D["classes"])
    ok(all(abs(pm[c]["macro"] - 1.0) < 1e-6 for c in pm), "완벽 예측 → 클래스별 F1 = 1")
    pm0 = per_class_macro(np.zeros_like(D["y"]), D["y"], D["pid"], D["classes"])
    ok(pm0["AFIB"]["macro"] == 0.0, "전부 N 이라 하면 AFIB F1 = 0")

    F = _rr_scalars(pre, post, pid)
    ok(F.shape == (len(pre), 8) and np.isfinite(F).all(), "RR 스칼라 산출")
    af = F[rhy == 1, 4].mean(); nn_ = F[rhy == 0, 4].mean()
    ok(af > nn_ * 2, f"AF 의 변동계수가 정상보다 큼 ({af:.3f} vs {nn_:.3f})")

    OUT = bench_rhythm(n_rep=1, k=3, K=16, path=f"{td}/ecg_multi.npz",
                       epochs=3, verbose=False)
    ok(OUT["split"] == "patient", "기본 분할은 환자 GroupKFold")
    ok(set(OUT["res"]) == {"A0.다수결", "A1.RR스칼라", "A2.RSN-리듬"}, "3개 arm 실행")
    ok(OUT["res"]["A2.RSN-리듬"]["mean"] > OUT["res"]["A0.다수결"]["mean"],
       f"RSN {OUT['res']['A2.RSN-리듬']['mean']:.3f} > 다수결 "
       f"{OUT['res']['A0.다수결']['mean']:.3f}")
    rp = report_rhythm(OUT, show=False)
    ok(any("AFIB" in k2 for k2 in rp), "클래스별 대응 비교 산출")

    # ★leave-one-DB-out — DB 조건부 가중치의 진위를 가르는 검정
    np.savez(f"{td}/multi2.npz", beat=beat, y5=np.zeros(len(rhy), np.int64),
             y3=np.zeros(len(rhy), np.int64), pid=pid, pre_rr=pre, post_rr=post,
             rhythm=rhy, rhythm_names=np.array(names + ["(미상)"]),
             sym=np.array(["N"] * len(rhy)),
             db=np.where(pid % 2 == 0, "dbA", "dbB"),        # 두 DB 로 가르기
             rr_edge=np.zeros(len(rhy), bool))
    O2 = bench_rhythm(n_rep=1, K=16, path=f"{td}/multi2.npz", split="db",
                      only=["A0.다수결", "A1.RR스칼라"], epochs=3, verbose=False)
    ok(O2["split"] == "db", "split='db' 로 LODO 실행")
    ok(len(np.unique(O2["pid"])) == len(np.unique(D["pid"])),
       f"LODO 도 (제외 클래스 뺀) 전체 환자를 한 번씩 평가 "
       f"({len(np.unique(O2['pid']))}명)")
    ok(O2["res"]["A1.RR스칼라"]["mean"] > O2["res"]["A0.다수결"]["mean"],
       "LODO 에서도 RR 기준선이 다수결을 이김")

    # n_domain FiLM 이 항등으로 시작하는지 (도메인 정보가 없을 때 기존 동작 보존)
    import torch
    M = g["_rsn"](4, 33, 10, n_class=3, n_domain=2); M.eval()
    a1 = (torch.randn(4, 4, 33), torch.randn(4, 2, 300), torch.randn(4, 10))
    with torch.no_grad():
        z0 = M(*a1, None, None); z1 = M(*a1, None, torch.tensor([0, 1, 0, 1]))
    ok(torch.allclose(z0, z1, atol=1e-6), "도메인 FiLM 은 항등 초기화(켜도 처음엔 무변화)")

    # ★전이 실험 — 통합/미세조정 3자 비교
    OT = bench_transfer(task="rhythm", path=f"{td}/multi2.npz", K=16, k=3,
                        epochs=3, ft_epochs=2, verbose=False)
    ok(set(OT["res"]) == {"P0.단독", "P1.통합", "P2.통합→미세"}, "3자 비교 실행")
    ls = {a: len(OT["res"][a]["pred"]) for a in OT["res"]}
    ok(len(set(ls.values())) == 1, f"세 arm 이 같은 홀드아웃을 본다(대응비교 성립) {ls}")
    ok(len(OT["y"]) == len(np.unique(OT["order"])), "홀드아웃이 중복 없이 한 번씩")
    # beat5 태스크도 도는지
    D5 = load_task(path=f"{td}/multi2.npz", task="beat5", min_records=1, verbose=False)
    ok(D5["classes"] and all(cc in ["N","S","V","F","Q"] for cc in D5["classes"]),
       f"beat5 태스크 로드 {D5['classes']}")
    print("=== 전 항목 통과 ===")
    return True


if __name__ == "__main__":
    import sys
    if "--selftest" in sys.argv:
        selftest()
