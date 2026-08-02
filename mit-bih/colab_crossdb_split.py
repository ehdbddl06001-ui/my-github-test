# -*- coding: utf-8 -*-
# =============================================================================
#  colab_crossdb_split.py  —  [실험22-A] colab_crossdb.py 의 **부록**
#
#  ★ 단독으로 못 돈다. colab_crossdb.py 를 **먼저** exec 해야 한다:
#      exec(open(f"{_BASE}/colab_crossdb.py").read(), globals())
#      exec(open(f"{_BASE}/colab_crossdb_split.py").read(), globals())
#    아래 함수가 쓰는 것들이 전부 거기 module-level 로 정의돼 있다:
#      _BASE · _FEATDIR · _DS1 · _DS2 · _determinism · _znorm · _medref
#      · _net · _incart_feats · _crossdb_rhythm · auto_weights
#
#  왜 원본을 안 고치고 파일을 나눴나: Drive 사본을 덮어쓰면 되돌릴 수 없고,
#  같은 이름으로 새로 올리면 중복 파일이 생겨 exec 가 어느 쪽을 읽을지 불확실해진다.
# =============================================================================
# =============================================================================
#  run_crossdb_split  —  [실험22-A] DS1 학습 → DS2(within) + INCART(cross) 동시 예측
#
#  왜 필요한가: run_crossdb 는 MIT-BIH **전체**로 학습해 INCART 만 예측한다.
#  그러면 낙폭(= within − cross)을 계산할 within 기준선이 **같은 모델에서** 안 나온다.
#  PAPER §6.5 의 수치가 cross 만 있는 이유가 이것이고, 그래서 축 간 비교가 막혀 있었다.
#
#  바꾼 것은 **네 가지뿐**이다. 백본·특징·에폭·손실·앙상블은 run_crossdb 와 동일:
#    ① RobustScaler 를 DS1 에만 fit      ② 학습 텐서를 DS1 로 제한
#    ③ auto_weights 를 DS1 라벨로 계산   ④ 예측을 DS2 와 INCART 양쪽에
#  ★ WST SelectKBest 는 원본과 동일하게 MIT-BIH **전체**로 fit 한다(원본 규격 유지).
#    엄밀히는 DS1 에서만 fit 해야 하나, 그러면 §6.5 와 이어붙지 않는다. 한계로 명시한다.
#
#  반환: {"v1_within_raw": (seed, n_ds2, 3), "v1_cross_raw": (seed, n_incart, 3),
#         "v1_within_bn": ..., "v1_cross_bn": ..., "v2_*": ..., "y_within", "y_cross"}
# =============================================================================
def run_crossdb_split(seeds=None, Kwst=40, train_mask=None, test_mask=None, use_rhythm=True):
    import torch, torch.nn as nn, torch.nn.functional as Fn
    from sklearn.preprocessing import RobustScaler
    from sklearn.feature_selection import SelectKBest, f_classif
    _determinism()
    seeds = list(seeds) if seeds is not None else list(range(2000, 2005))
    dev = "cuda" if torch.cuda.is_available() else "cpu"

    d = np.load(f"{_BASE}/mamba_data.npz")
    mb = _znorm(d["beat"]); my = d["y"]; mpid = d["pid"]; mref = _medref(mb, mpid); mfeats0 = d["feats"]
    if train_mask is None: train_mask = np.isin(mpid, _DS1)
    if test_mask is None:  test_mask  = np.isin(mpid, _DS2)
    tr = np.asarray(train_mask, bool); te = np.asarray(test_mask, bool)
    if (tr & te).any():
        raise RuntimeError("train_mask 와 test_mask 가 겹친다 — 누수")
    if not tr.any() or not te.any():
        raise RuntimeError(f"분할이 비었다 (train {tr.sum()} · test {te.sum()})")

    exec(open(f"{_BASE}/colab_step12_wst.py").read(), globals())
    mWSTraw = globals()["compute_wst_features"](d["beat"])
    sel = SelectKBest(f_classif, k=Kwst).fit(np.nan_to_num(mWSTraw), my)   # ★ 원본과 동일(전체 fit)
    def wsel(raw): return np.nan_to_num(sel.transform(np.nan_to_num(raw))).astype("float32")
    Fm1 = np.concatenate([wsel(mWSTraw), np.load(f"{_FEATDIR}/MORPHO.npy"), np.load(f"{_FEATDIR}/REPOL.npy"),
                          np.load(f"{_FEATDIR}/KOOPMAN.npy"), np.load(f"{_FEATDIR}/GNN.npy")], 1).astype("float32")

    di = np.load(f"{_BASE}/incart_data.npz")
    ib = _znorm(di["beat"]); iy = di["y"]; ipid = di["pid"]; iref = _medref(ib, ipid)
    IF = _incart_feats()
    Fi1 = np.concatenate([wsel(IF["WST_raw"]), IF["MORPHO"], IF["REPOL"], IF["KOOPMAN"], IF["GNN"]], 1).astype("float32")

    CFG = [("v1", Fm1, Fi1)]
    if use_rhythm:
        mRHY, iRHY = _crossdb_rhythm(mb, mfeats0, mpid, ib, di["pre_rr"], di["post_rr"], ipid)
        CFG.append(("v2", np.concatenate([Fm1, mRHY], 1).astype("float32"),
                          np.concatenate([Fi1, iRHY], 1).astype("float32")))

    Sw = auto_weights(my[tr])                                    # ② DS1 라벨로
    nc = np.array([(my[tr] == k).sum() for k in range(3)], np.float32)
    mc = (1.0 / np.power(np.maximum(nc, 1), 0.25)); mc = (mc / mc.max() * 0.5).astype("float32")
    print(f"DS1 학습 {int(tr.sum()):,}비트(N/S/V={int((my[tr]==0).sum())}/{int((my[tr]==1).sum())}/{int((my[tr]==2).sum())})"
          f" → DS2 {int(te.sum()):,} · INCART {len(iy):,}")

    @torch.no_grad()
    def pred(M, b, r, ft, bn=False):
        if bn:
            for mod in M.modules():
                if isinstance(mod, nn.BatchNorm1d): mod.reset_running_stats(); mod.momentum = None
            M.train()
            for i in range(0, len(b), 512):
                M(torch.from_numpy(b[i:i+512]).to(dev), torch.from_numpy(r[i:i+512]).to(dev),
                  torch.from_numpy(ft[i:i+512]).to(dev))
        M.eval(); o = []
        for i in range(0, len(b), 4096):
            o.append(torch.softmax(M(torch.from_numpy(b[i:i+4096]).to(dev), torch.from_numpy(r[i:i+4096]).to(dev),
                                     torch.from_numpy(ft[i:i+4096]).to(dev)), -1).cpu().numpy())
        return np.concatenate(o)

    OUT = {"y_within": my[te], "y_cross": iy}
    for cname, Fm, Fi in CFG:
        acc = {k: [] for k in ("within_raw", "within_bn", "cross_raw", "cross_bn")}
        for seed in seeds:
            torch.manual_seed(seed); np.random.seed(seed)
            sc = RobustScaler().fit(Fm[tr])                      # ① DS1 에만 fit
            f_tr = np.nan_to_num(sc.transform(Fm[tr]), posinf=0, neginf=0).astype("float32")
            f_te = np.nan_to_num(sc.transform(Fm[te]), posinf=0, neginf=0).astype("float32")
            f_in = np.nan_to_num(sc.transform(Fi),     posinf=0, neginf=0).astype("float32")
            M = _net(Fm.shape[1]).to(dev)
            opt = torch.optim.AdamW(M.parameters(), lr=1e-3, weight_decay=1e-4)
            cw = torch.tensor([1., Sw, 1.5], device=dev); mcv = torch.from_numpy(mc).to(dev)
            ds = torch.utils.data.TensorDataset(*[torch.from_numpy(x) for x in
                                                  (mb[tr], mref[tr], f_tr, my[tr])])   # ② DS1 만
            dl = torch.utils.data.DataLoader(ds, batch_size=512, shuffle=True)
            for ep in range(15):
                M.train()
                for bb, rr, ff, yy in dl:
                    bb, rr, ff, yy = (t.to(dev) for t in (bb, rr, ff, yy)); opt.zero_grad()
                    lo = M(bb, rr, ff); lg = lo - torch.zeros_like(lo).scatter_(1, yy[:, None], mcv[yy][:, None])
                    ce = Fn.cross_entropy(lg, yy, reduction="none"); loss = (ce * cw[yy]).sum() / cw[yy].sum()
                    loss.backward(); torch.nn.utils.clip_grad_norm_(M.parameters(), 1.0); opt.step()
            acc["within_raw"].append(pred(M, mb[te], mref[te], f_te, bn=False))   # ④ 양쪽
            acc["cross_raw"].append(pred(M, ib, iref, f_in, bn=False))
            Mb = _net(Fm.shape[1]).to(dev); Mb.load_state_dict(M.state_dict())
            acc["within_bn"].append(pred(Mb, mb[te], mref[te], f_te, bn=True))
            Mb2 = _net(Fm.shape[1]).to(dev); Mb2.load_state_dict(M.state_dict())
            acc["cross_bn"].append(pred(Mb2, ib, iref, f_in, bn=True))
            print(f"  [{cname}] seed {seed} 완료")
        for k, v in acc.items():
            OUT[f"{cname}_{k}"] = np.stack(v, 0)
    return OUT
