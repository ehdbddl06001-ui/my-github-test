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
def load_rhythm(path=None, min_records=8, exclude=("(미상)",), verbose=True):
    """ecg_multi.npz → 리듬 과제용 부분집합.

    ★'(미상)' 은 **클래스가 아니라 '주석이 없음'** 이다. 클래스로 넣으면
      "리듬 주석이 안 달린 구간"을 학습·평가하게 되어 무의미하다. 반드시 제외한다.
    ★레코드 수가 min_records 미만인 리듬도 제외한다 — 환자분리 평가가 성립하지
      않는 클래스를 넣으면 매크로 지표가 몇 명의 우연에 좌우된다(HANDOFF §2).
      제외된 비트는 학습에서도 뺀다(다른 클래스로 오염시키지 않기 위해).
    """
    d = np.load(path or f"{_BASE}/ecg_multi.npz", allow_pickle=True)
    beat, pid, pre, post = d["beat"], d["pid"], d["pre_rr"], d["post_rr"]
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
               classes=cls, y5=(y5[sel] if y5 is not None else None))
    if verbose:
        print(f"리듬 과제 데이터: {len(y):,}비트  환자 {len(np.unique(out['pid']))}명  "
              f"클래스 {len(cls)}종")
        print(f"  {'클래스':<8}{'비트':>10}{'레코드':>8}{'비율':>8}")
        for nm, nb, nr in kept:
            print(f"  {nm:<8}{nb:>10,}{nr:>8}{100*nb/len(y):>7.2f}%")
        drop = int((~sel).sum())
        print(f"  제외 {drop:,}비트 (미상 + 레코드<{min_records} 클래스)")
        print(f"  ⚠ 리듬 주석은 사실상 MIT-BIH 에만 있다 → 환자 수가 SVDB(73)보다 적다")
    return out


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
                 epochs=20, verbose=True):
    """리듬 분류 벤치. 규율은 SVEB 하니스와 동일(환자 GroupKFold, 결정론적 분할)."""
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
    gkf = GroupKFold(n_splits=k)
    for rep in range(n_rep):
        for fi, (tr, te) in enumerate(gkf.split(np.arange(len(y)), y, groups=pid)):
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
                print(f"  rep{rep} fold{fi} 완료 (train {len(tr):,} / test {len(te):,})")
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
    return dict(res=RES, y=yA, pid=pA, order=idx, classes=cls, mde=mde,
                arms=ARMS, dead=sorted(dead))


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
    ok(set(OUT["res"]) == {"A0.다수결", "A1.RR스칼라", "A2.RSN-리듬"}, "3개 arm 실행")
    ok(OUT["res"]["A2.RSN-리듬"]["mean"] > OUT["res"]["A0.다수결"]["mean"],
       f"RSN {OUT['res']['A2.RSN-리듬']['mean']:.3f} > 다수결 "
       f"{OUT['res']['A0.다수결']['mean']:.3f}")
    rp = report_rhythm(OUT, show=False)
    ok(any("AFIB" in k2 for k2 in rp), "클래스별 대응 비교 산출")
    print("=== 전 항목 통과 ===")
    return True


if __name__ == "__main__":
    import sys
    if "--selftest" in sys.argv:
        selftest()
