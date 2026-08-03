# -*- coding: utf-8 -*-
# =============================================================================
#  colab_crossdb_svdb.py  —  [퀘스트46 Q7-B] colab_crossdb.py 의 **부록**
#
#  ★ 단독으로 못 돈다. colab_crossdb.py 를 **먼저** exec 해야 한다:
#      exec(open(f"{_BASE}/colab_crossdb.py").read(), globals())
#      exec(open(f"{_BASE}/colab_crossdb_svdb.py").read(), globals())
#    아래가 쓰는 것들이 전부 거기 module-level 로 정의돼 있다:
#      _BASE · _FEATDIR · _DS1 · _DS2 · _determinism · _znorm · _medref
#      · _net · _crossdb_rhythm · auto_weights
#
#  무엇이 다른가 (colab_crossdb_split.py 대비):
#    ① 교차 대상이 INCART → **SVDB**(78레코드 · 레코드=환자 1:1)
#    ② WST SelectKBest 를 **DS1 에서만** fit 한다(`wst_fit="ds1"`, 기본값).
#       ★ 실험22-A 는 MIT-BIH **전체**로 fit 했다 — DS2 가 테스트였는데도. §6.5 와
#         이어붙이려는 타협이었고 한계로 명시돼 있었다. 여기서는 그럴 이유가 없다:
#         Q7-B 의 판정 대상은 SVDB 이고 DS2 는 참고용이라, DS1-only fit 이 **더
#         엄격하면서 비용이 0** 이다. 대신 이 값들은 §6.5·실험22-A 와 **직접 비교
#         불가**다(선택 규격이 다르다).
#    ③ 오염 감사(`svdb_leak_audit`)를 학습 전에 **강제**한다. 실패하면 예외.
#
#  ⚠️ 대역 교란: SVDB 원본은 128Hz 이고 여기 들어오는 배열은 360Hz 로 **업샘플된**
#     것이다(svdb_labels.build_labeled). 파형은 360 이지만 대역폭은 64Hz 로 잘려
#     있다 — MIT-BIH(180Hz 대역)와 다르다. 그래서 **SVDB 전이 낙폭을 인용하면
#     안 된다.** 그건 별도 실험(Q7-C, 동일 대역 MIT-BIH 대조군)이 있어야 한다.
#     Q7-B 가 묻는 것은 낙폭이 아니라 **'이 코호트가 판정을 지탱할 만큼 정밀한가'**
#     뿐이므로 이 교란과 무관하게 답이 나온다.
#
#  실행(Colab):
#    OUT = run_crossdb_svdb(seeds=range(2000, 2005))
# =============================================================================


def _svdb_load(path=None):
    """svdb_data5.npz 를 3-class 로 정리해 로드. (beat, y, pid_rec, pre, post)

    ★ svdb_labels.build_labeled() 가 만든 파일을 쓴다. svdb_prep.build_svdb() 의
      `svdb_data.npz` 를 **쓰지 않는다** — 거기 pre_rr/post_rr 은 `'+'`(리듬변경)
      주석까지 diff 해서 만든 값이라 **RR 이 오염**돼 있다(svdb_labels 서두 참조).
      S 는 RR 로 정의되는 클래스다. 오염된 RR 로 S 를 재면 실험 자체가 무의미하다.
    """
    import os
    path = path or f"{_BASE}/svdb_data5.npz"
    if not os.path.exists(path):
        raise RuntimeError(
            f"{path} 가 없다.\n"
            "  → svdb_labels.build_labeled() 를 먼저 돌릴 것(신호까지 받으므로 오래 걸린다).\n"
            "  ⚠️ svdb_data.npz(svdb_prep) 로 대체하지 말 것 — RR 이 오염돼 있다."
        )
    d = np.load(path, allow_pickle=True)
    y3 = d["y3"]
    keep = y3 >= 0                                   # F/Q 제외 → 기존 3-class 재현
    beat = d["beat"][keep]
    y = y3[keep].astype(np.int64)
    ridx = d["pid"][keep].astype(int)                # ★ 레코드 **인덱스**(0..n-1)
    pre = d["pre_rr"][keep].astype("float32")
    post = d["post_rr"][keep].astype("float32")
    edge = d["rr_edge"][keep] if "rr_edge" in d.files else np.zeros(len(y), bool)

    # 레코드 인덱스 → 실제 레코드 번호. Q7 카운트와 같은 키를 쓴다.
    #  ⛔ **fallback 금지.** 예전엔 여기서 실패 시 `[str(i) for i in range(800,895)]` 로
    #     조용히 넘어갔다. 그러면 `recs[i] = 800+i` 가 되어 **그럴듯하지만 틀린 레코드
    #     번호**가 나온다 — SVDB 는 813~819·830~839 이 비어 있어서 인덱스 13 부터 어긋난다.
    #     실제로 그 사고가 났고(ailab-2026-0052), 라벨 800~877 중 17개가 존재하지 않는
    #     번호였다. 터지는 게 낫다 — 조용히 틀린 번호를 내면 그걸로 쓴 모든 문장이 틀린다.
    import wfdb
    recs = wfdb.get_record_list("svdb")
    if not recs:
        raise RuntimeError("wfdb.get_record_list('svdb') 가 비었다 — 네트워크 확인. "
                           "연속 번호로 대체하지 않는다(그러면 번호가 조용히 어긋난다)")
    if ridx.max() >= len(recs):
        raise RuntimeError(f"pid 인덱스 {ridx.max()} 가 레코드 목록 {len(recs)}개를 넘는다 — "
                           "build_labeled 가 다른 목록으로 돌았다")
    num = np.array([int(recs[i]) for i in ridx], np.int64)
    # 매핑 자가검증: 라벨이 목록의 부분집합이어야 한다(연속 가정이 섞이면 깨진다)
    bad = sorted(set(num.tolist()) - {int(r) for r in recs})
    if bad:
        raise RuntimeError(f"매핑된 레코드 번호가 목록에 없다: {bad[:8]} — 인덱스 기준이 어긋났다")
    print(f"  SVDB {len(y):,}비트 · 레코드 {len(np.unique(num))}개 "
          f"(N/S/V={int((y==0).sum()):,}/{int((y==1).sum()):,}/{int((y==2).sum()):,})")
    print(f"    RR 은 비트 주석만으로 계산됨(오염 없음) · 레코드 양끝 비트 {int(edge.sum())}개는 RR 이 이웃 복제")
    return beat, y, num, pre, post, edge


def _svdb_feats(beat, pid, cache=None):
    """SVDB 비트에서 v1 자립특징 계산. `_incart_feats` 와 **같은 추출기·같은 순서**.

    ★ 라벨을 쓰지 않는다. `extract_koopman_features`·`extract_gnn_features` 는
      시그니처에 `y=None` 이 있지만 본문에서 y 를 **참조하지 않는다**(확인함).
      그래서 여기서는 아예 넘기지 않는다 — '안 쓴다' 를 코드로 보이게.
    """
    import os
    # ★ Drive 에 이미 `svdb_feats/` **폴더**(07-27 SVDB 작업물)가 있다. 이름이 겹치면
    #   헷갈리므로 이 실험 전용 이름을 쓴다. 그쪽 산출물은 `svdb_data.npz`(RR 오염)
    #   기준이라 여기 비트 배열과 정렬이 다를 수 있다 — 재사용하지 않는다.
    cache = cache or f"{_BASE}/svdb_feats_q7b.npz"
    if os.path.exists(cache):
        d = np.load(cache); print(f"  SVDB 특징 캐시 로드 ({os.path.basename(cache)})")
        F = {k: d[k] for k in d.files}
        if len(F["MORPHO"]) != len(beat):
            raise RuntimeError(f"특징 캐시 길이 {len(F['MORPHO'])} != 비트 {len(beat)} — "
                               "캐시가 다른 빌드의 것이다. 지우고 다시 계산할 것")
        return F
    g = globals()
    for src in ("colab_step15_morpho.py", "colab_step18_repol.py", "colab_step52_newfeats.py"):
        exec(open(f"{_BASE}/{src}").read(), g)
    ref = _medref(beat, pid)
    print("  SVDB 특징 계산: MORPHO·REPOL·KOOPMAN·GNN·WST... (라벨 미사용)")
    F = {"MORPHO": g["extract_morpho_features"](beat, ref, pid),
         "REPOL": g["extract_repol_features"](beat, ref, pid)[:, [0, 1, 4, 5]].astype("float32"),
         "KOOPMAN": g["extract_koopman_features"](beat, pid),
         "GNN": g["extract_gnn_features"](beat, pid)}
    exec(open(f"{_BASE}/colab_step12_wst.py").read(), g)
    F["WST_raw"] = g["compute_wst_features"](beat)
    np.savez(cache, **F); print(f"  → {os.path.basename(cache)} 저장")
    return F


def svdb_leak_audit(mpid, tr_mask, spid, strict=True):
    """학습 전에 도는 **오염 감사**. 실패하면 예외를 던지고 학습을 시작하지 않는다.

    반환: 감사 항목 dict(사람이 읽는 근거). 통과해도 '한계' 항목은 남는다.
    """
    rep = {}
    mtr = np.unique(np.asarray(mpid)[np.asarray(tr_mask, bool)])
    srec = np.unique(np.asarray(spid))

    # ① 학습 환자 ∩ 평가 환자 = ∅
    inter = np.intersect1d(mtr, srec)
    rep["train_test_disjoint"] = (len(inter) == 0, f"학습 {len(mtr)}환자 ∩ SVDB {len(srec)}레코드 = {inter.tolist()}")

    # ② 학습셋이 DS1 그대로인가(DS2 가 섞이지 않았나)
    ds2_in = np.intersect1d(mtr, _DS2)
    rep["no_ds2_in_train"] = (len(ds2_in) == 0, f"학습에 섞인 DS2 = {ds2_in.tolist()}")

    # ③ SVDB 레코드 번호가 MIT-BIH 대역(100~234)과 겹치지 않는가(pid 충돌 방지)
    clash = srec[(srec >= 100) & (srec <= 234)]
    rep["pid_namespace"] = (len(clash) == 0, f"MIT-BIH 번호대와 겹치는 SVDB 레코드 = {clash.tolist()}")

    fails = [k for k, (ok, _) in rep.items() if not ok]
    print("\n  ── 오염 감사 ──")
    for k, (ok, msg) in rep.items():
        print(f"    {'✅' if ok else '❌'} {k}: {msg}")
    print("    ⚠️ 공개 한계(누수 아님, 그러나 반드시 병기): "
          "`_medref`(환자별 중앙 파형)와 BN 적응은 **평가 데이터의 입력**을 쓴다. "
          "라벨은 안 쓰므로 누수는 아니지만 **transductive** 다. "
          "관문은 raw(=BN 미적응)로 매기고 BN 은 참고로만 낸다.")
    if fails and strict:
        raise RuntimeError(f"오염 감사 실패: {fails} — 학습을 시작하지 않는다")
    return rep


def run_crossdb_svdb(seeds=None, Kwst=40, wst_fit="ds1", use_rhythm=True,
                     train_mask=None, svdb_path=None):
    """DS1 학습 → SVDB(cross) + DS2(within, 참고) 예측. 학습셋에 SVDB 를 쓰지 않는다.

    wst_fit: "ds1"(기본 · 더 엄격) | "all"(실험22-A 규격 재현용)
    반환: {"y_cross","rec_cross","v1_cross_raw","v2_cross_raw","v2_cross_bn",
           "y_within","rec_within","v2_within_raw", ...}
    """
    import torch, torch.nn as nn, torch.nn.functional as Fn
    from sklearn.preprocessing import RobustScaler
    from sklearn.feature_selection import SelectKBest, f_classif
    _determinism()
    seeds = list(seeds) if seeds is not None else list(range(2000, 2005))
    dev = "cuda" if torch.cuda.is_available() else "cpu"

    # ── MIT-BIH ──
    d = np.load(f"{_BASE}/mamba_data.npz")
    mb = _znorm(d["beat"]); my = d["y"]; mpid = d["pid"]; mref = _medref(mb, mpid); mfeats0 = d["feats"]
    tr = np.isin(mpid, _DS1) if train_mask is None else np.asarray(train_mask, bool)
    te = np.isin(mpid, _DS2)
    if (tr & te).any():
        raise RuntimeError("train 과 within-test 가 겹친다 — 누수")

    # ── SVDB ──
    sb_raw, sy, srec, spre, spost, sedge = _svdb_load(svdb_path)
    sb = _znorm(sb_raw); sref = _medref(sb, srec)

    svdb_leak_audit(mpid, tr, srec, strict=True)

    # ── WST 선택 ──
    exec(open(f"{_BASE}/colab_step12_wst.py").read(), globals())
    mWSTraw = globals()["compute_wst_features"](d["beat"])
    if wst_fit == "ds1":
        sel = SelectKBest(f_classif, k=Kwst).fit(np.nan_to_num(mWSTraw[tr]), my[tr])
        print(f"\n  WST SelectKBest: **DS1 에서만** fit (k={Kwst}) — 실험22-A(전체 fit)와 규격이 다르다")
    elif wst_fit == "all":
        sel = SelectKBest(f_classif, k=Kwst).fit(np.nan_to_num(mWSTraw), my)
        print(f"\n  WST SelectKBest: MIT-BIH 전체 fit (k={Kwst}) — 실험22-A 규격 재현")
    else:
        raise ValueError("wst_fit 은 'ds1' 또는 'all'")
    def wsel(raw): return np.nan_to_num(sel.transform(np.nan_to_num(raw))).astype("float32")

    Fm1 = np.concatenate([wsel(mWSTraw), np.load(f"{_FEATDIR}/MORPHO.npy"), np.load(f"{_FEATDIR}/REPOL.npy"),
                          np.load(f"{_FEATDIR}/KOOPMAN.npy"), np.load(f"{_FEATDIR}/GNN.npy")], 1).astype("float32")
    SF = _svdb_feats(sb_raw, srec)
    Fs1 = np.concatenate([wsel(SF["WST_raw"]), SF["MORPHO"], SF["REPOL"],
                          SF["KOOPMAN"], SF["GNN"]], 1).astype("float32")
    if Fm1.shape[1] != Fs1.shape[1]:
        raise RuntimeError(f"특징 차원 불일치 MIT {Fm1.shape[1]} vs SVDB {Fs1.shape[1]}")

    CFG = [("v1", Fm1, Fs1)]
    if use_rhythm:
        # SVDB 는 INCART 와 같은 방식 — 저장된 pre/post_rr 를 **명시 컬럼**으로 준다.
        # 라벨 자동식별을 건너뛰므로 평가 라벨이 특징에 안 들어간다.
        mRHY, sRHY = _crossdb_rhythm(mb, mfeats0, mpid, sb, spre, spost, srec)
        CFG.append(("v2", np.concatenate([Fm1, mRHY], 1).astype("float32"),
                          np.concatenate([Fs1, sRHY], 1).astype("float32")))

    Sw = auto_weights(my[tr])
    nc = np.array([(my[tr] == k).sum() for k in range(3)], np.float32)
    mc = (1.0 / np.power(np.maximum(nc, 1), 0.25)); mc = (mc / mc.max() * 0.5).astype("float32")
    print(f"\nDS1 학습 {int(tr.sum()):,}비트(N/S/V={int((my[tr]==0).sum())}/{int((my[tr]==1).sum())}/{int((my[tr]==2).sum())})"
          f" → SVDB {len(sy):,} · DS2(참고) {int(te.sum()):,}")

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

    OUT = {"y_cross": sy, "rec_cross": srec, "rr_edge_cross": sedge,
           "y_within": my[te], "rec_within": mpid[te], "wst_fit": wst_fit,
           "seeds": np.array(list(seeds))}
    for cname, Fm, Fs in CFG:
        acc = {k: [] for k in ("cross_raw", "cross_bn", "within_raw")}
        for seed in seeds:
            torch.manual_seed(seed); np.random.seed(seed)
            sc = RobustScaler().fit(Fm[tr])                      # DS1 에만 fit
            f_tr = np.nan_to_num(sc.transform(Fm[tr]), posinf=0, neginf=0).astype("float32")
            f_te = np.nan_to_num(sc.transform(Fm[te]), posinf=0, neginf=0).astype("float32")
            f_sv = np.nan_to_num(sc.transform(Fs),     posinf=0, neginf=0).astype("float32")
            M = _net(Fm.shape[1]).to(dev)
            opt = torch.optim.AdamW(M.parameters(), lr=1e-3, weight_decay=1e-4)
            cw = torch.tensor([1., Sw, 1.5], device=dev); mcv = torch.from_numpy(mc).to(dev)
            ds = torch.utils.data.TensorDataset(*[torch.from_numpy(x) for x in
                                                  (mb[tr], mref[tr], f_tr, my[tr])])
            dl = torch.utils.data.DataLoader(ds, batch_size=512, shuffle=True)
            for ep in range(15):
                M.train()
                for bb, rr, ff, yy in dl:
                    bb, rr, ff, yy = (t.to(dev) for t in (bb, rr, ff, yy)); opt.zero_grad()
                    lo = M(bb, rr, ff); lg = lo - torch.zeros_like(lo).scatter_(1, yy[:, None], mcv[yy][:, None])
                    ce = Fn.cross_entropy(lg, yy, reduction="none"); loss = (ce * cw[yy]).sum() / cw[yy].sum()
                    loss.backward(); torch.nn.utils.clip_grad_norm_(M.parameters(), 1.0); opt.step()
            acc["cross_raw"].append(pred(M, sb, sref, f_sv, bn=False))
            acc["within_raw"].append(pred(M, mb[te], mref[te], f_te, bn=False))
            Mb = _net(Fm.shape[1]).to(dev); Mb.load_state_dict(M.state_dict())
            acc["cross_bn"].append(pred(Mb, sb, sref, f_sv, bn=True))
            print(f"  [{cname}] seed {seed} 완료")
        for k, v in acc.items():
            OUT[f"{cname}_{k}"] = np.stack(v, 0)
    return OUT
