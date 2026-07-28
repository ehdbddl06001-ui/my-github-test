# =============================================================================
#  svdb_bench.py  —  [대규모 Phase A] SVDB 특징계산 + B0~B4 동일 프로토콜 벤치마크
#
#  SVDB 실측: 184,397비트 / S 12,196(6.61%) / 78레코드 중 73개가 S 보유
#   → 매크로F1 95%CI ±0.073 (MIT-BIH DS2 16명 ±0.157의 2.2배 정밀). 비로소 검정 가능.
#   → 단일 레코드 지배 불가 구조 → H5(#232 지배가 일반현상인가) 검정 가능.
#
#  ★규율(LARGESCALE_PLAN §4): 모델 구성을 SVDB에서 재탐색하지 않는다.
#    MIT-BIH에서 확정한 구성을 '얼려서' 그대로 적용 → 캠페인 편향 없는 out-of-sample 검정.
#    특징군 스윕 금지, conf_cut·frac 재조정 금지. 나온 대로 보고.
#
#  ★정직한 차이 (반드시 논문에 명시): SVDB에는 MIT-BIH의 feats0(26, 외부제공)가 없다.
#    대신 저장된 pre_rr/post_rr을 직접 사용한다. 따라서 B4의 특징벡터는 MIT-BIH판과
#    동일하지 않다(RR 정보는 보존되나 feats0의 나머지는 부재). 절대 비교 시 유의.
#
#  비교 모델(모두 동일 분할·동일 지표):
#    B0 다수결(항상 N)          — 자명한 하한
#    B1 de Chazal형 LDA         — 형태(MORPHO+REPOL)+RR
#    B2 1D-CNN (raw beat만)     — 딥러닝 최소 기준선
#    B3 1D-CNN + RR             — 흔한 실무 구성
#    B4 본 연구(전체특징+강건템플릿) — 제안
#    B4C B4 + 2성분 센터링       — 라벨프리 개인화 추가분
#
#  주지표: 환자단위 매크로 F1 + 부트스트랩 95%CI.  micro는 최다레코드 기여율과 함께 참고 표기.
#
#  선행: svdb_prep.py 실행(svdb_data.npz) + colab_step67~70 + 추출기 소스들 Drive에
#  실행:
#    exec(open('/content/drive/MyDrive/mitbih/svdb_bench.py').read())
#    svdb_prep_feats()            # ① 특징 계산·캐시 (GPU 권장, 15~30분, 재개가능)
#    OUT=bench_models(n_rep=1)    # ② B0~B4C 벤치 (5fold, NN 3종 → 15학습)
#
#  신규 모델을 같은 폴드에 붙이려면 (arm 레지스트리):
#    exec(open('/content/drive/MyDrive/mitbih/svdb_rhythm.py').read())
#    attach_arms()                # R0/R1/R2 등록 → bench_models()가 함께 평가
#    OUT=bench_models(n_rep=1);  report(OUT)
# =============================================================================
import os
import numpy as np
from sklearn.metrics import average_precision_score

_BASE="/content/drive/MyDrive/mitbih"; _SFEAT=f"{_BASE}/svdb_feats"
if "robust_template" not in globals():
    exec(open(f"{_BASE}/colab_step70_evalintegrity.py").read(), globals())  # 70→69→68→67 체인

def _sv():
    d=np.load(f"{_BASE}/svdb_data.npz")
    return d["beat"],d["y"],d["pid"],d["pre_rr"],d["post_rr"]

# ─────────────── 확장 arm 레지스트리 (신규 모델을 같은 폴드에 붙이는 통로) ───────────────
#  왜: 새 모델을 별도 스크립트에서 따로 돌리면 폴드·calib·임계규약이 달라져 대응
#      부트스트랩(같은 환자의 F1 차이)이 성립하지 않는다. 여기에 arm 으로 붙이면
#      B0~B4C 와 '완전히 동일한 분할·동일 임계법'에서 평가되어 비교가 유효해진다.
#  계약: fn(ctx) -> bool 배열, 길이 len(ctx["te"]).  ctx 키는 아래 _arm_ctx 참조.
#      ctx["te"] 라벨은 절대 보지 않는다(임계는 ctx["cal"] 에서만 — 무결성 §7-1).
EXTRA_ARMS={}

def register_arm(name, fn):
    """새 모델 arm 등록. 예: register_arm("R1.RSN", my_fn)  (svdb_rhythm.attach_arms 사용)"""
    if not callable(fn): raise TypeError("fn 은 호출 가능해야 합니다")
    EXTRA_ARMS[name]=fn; return name

def clear_arms():
    EXTRA_ARMS.clear()

def list_arms():
    print(f"등록된 확장 arm {len(EXTRA_ARMS)}개: {list(EXTRA_ARMS)}")
    return list(EXTRA_ARMS)

# ─────────────── ① 특징 계산 (캐시·재개) ───────────────
def svdb_prep_feats(force=False, use_ae=True, Kwst=40):
    """SVDB 특징 계산 → svdb_feats/*.npy. MIT-BIH와 동일 추출기·동일 파라미터."""
    os.makedirs(_SFEAT,exist_ok=True); g=globals()
    beats,y,pid,pre,post=_sv()
    need=lambda n: force or not os.path.exists(f"{_SFEAT}/{n}.npy")
    print(f"SVDB 특징 계산: {len(y)}비트 / {len(np.unique(pid))}레코드")
    ref=_median_ref(beats,pid)                       # 특징계산용 레퍼런스(중앙값; B4의 ref는 별도로 강건템플릿)
    if need("WST"):
        exec(open(f"{_BASE}/colab_step12_wst.py").read(), g)
        from sklearn.feature_selection import SelectKBest, f_classif
        raw=g["compute_wst_features"](beats)
        sel=SelectKBest(f_classif,k=min(Kwst,raw.shape[1])).fit(np.nan_to_num(raw),y)   # 선택은 SVDB 내에서 fit
        np.save(f"{_SFEAT}/WST.npy",np.nan_to_num(sel.transform(np.nan_to_num(raw))).astype("float32"))
        print("  WST 저장"); del raw
    else: print("  WST 캐시")
    if need("MORPHO"):
        exec(open(f"{_BASE}/colab_step15_morpho.py").read(), g)
        np.save(f"{_SFEAT}/MORPHO.npy",np.nan_to_num(g["extract_morpho_features"](beats,ref,pid)).astype("float32")); print("  MORPHO 저장")
    else: print("  MORPHO 캐시")
    if need("REPOL"):
        exec(open(f"{_BASE}/colab_step18_repol.py").read(), g)
        np.save(f"{_SFEAT}/REPOL.npy",np.nan_to_num(g["extract_repol_features"](beats,ref,pid)[:,[0,1,4,5]]).astype("float32")); print("  REPOL 저장")
    else: print("  REPOL 캐시")
    if need("RHYTHM"):
        exec(open(f"{_BASE}/colab_step49_rhythm2.py").read(), g)
        f0=np.stack([pre.astype("float64"),post.astype("float64")],1)      # feats0 대용 = [pre_rr, post_rr]
        R=g["extract_rhythm_v2"](beats,f0,pid,pre_col=0,post_col=1,verbose=True)   # 라벨 미사용(명시컬럼)
        np.save(f"{_SFEAT}/RHYTHM.npy",np.nan_to_num(R).astype("float32")); print(f"  RHYTHM 저장 dim={R.shape[1]}")
    else: print("  RHYTHM 캐시")
    if any(need(k) for k in ("KOOPMAN","GNN")) or (use_ae and need("AE")):
        exec(open(f"{_BASE}/colab_step52_newfeats.py").read(), g)
        if need("KOOPMAN"):
            np.save(f"{_SFEAT}/KOOPMAN.npy",np.nan_to_num(g["extract_koopman_features"](beats,pid,y)).astype("float32")); print("  KOOPMAN 저장")
        if need("GNN"):
            np.save(f"{_SFEAT}/GNN.npy",np.nan_to_num(g["extract_gnn_features"](beats,pid,y)).astype("float32")); print("  GNN 저장")
        if use_ae and need("AE"):
            # ★SVDB pid(0~77)는 MIT-BIH _DS1과 교집합이 없다 → train_mask 명시 필수(전체 환자의 정상비트로 학습)
            print("  AE 학습(GPU, 수분)...")
            A=g["extract_ae_features"](beats,y,pid,train_mask=np.ones(len(y),bool))
            np.save(f"{_SFEAT}/AE.npy",np.nan_to_num(A).astype("float32")); print("  AE 저장")
    else: print("  KOOPMAN/GNN/AE 캐시")
    # RR 원값도 특징으로(정규화는 학습시 RobustScaler)
    if need("RR"): np.save(f"{_SFEAT}/RR.npy",np.stack([pre,post],1).astype("float32")); print("  RR 저장")
    print("✔ 특징 준비 완료")

def _load_feats(names):
    out=[]
    for n in names:
        p=f"{_SFEAT}/{n}.npy"
        if not os.path.exists(p): raise RuntimeError(f"{n} 캐시 없음 → svdb_prep_feats() 먼저")
        out.append(np.load(p))
    return np.concatenate(out,1).astype("float32")

# ─────────────── 지표 ───────────────
def _prf(v,yy):
    yp=(yy==1); tp=float((v&yp).sum()); fp=float((v&~yp).sum()); fn=float((~v&yp).sum())
    pr=tp/(tp+fp+1e-9); se=tp/(tp+fn+1e-9); return pr,se,2*pr*se/(pr+se+1e-9)

def _macro(v,y,pid,B=2000,seed=0):
    """환자단위 매크로 F1 + 환자 부트스트랩 95%CI."""
    ps=[p for p in np.unique(pid) if (y[pid==p]==1).sum()>0]
    f=np.array([_prf(v[pid==p],y[pid==p])[2] for p in ps])
    rng=np.random.RandomState(seed); n=len(f)
    bs=np.array([f[rng.randint(0,n,n)].mean() for _ in range(B)])
    return float(f.mean()), float(np.percentile(bs,2.5)), float(np.percentile(bs,97.5)), n, f

# ─────────────── 모델 ───────────────
def _cnn(fdim):
    """B2/B3용 표준 1D-CNN(+선택적 특징). 우리 구조의 게이트·프로토타입 없음."""
    import torch, torch.nn as nn
    class Net(nn.Module):
        def __init__(s):
            super().__init__(); s.c=nn.Sequential(
                nn.Conv1d(2,32,7,padding=3),nn.BatchNorm1d(32),nn.ReLU(),nn.MaxPool1d(2),
                nn.Conv1d(32,64,5,padding=2),nn.BatchNorm1d(64),nn.ReLU(),nn.MaxPool1d(2),
                nn.Conv1d(64,128,3,padding=1),nn.BatchNorm1d(128),nn.ReLU(),nn.AdaptiveAvgPool1d(1))
            s.fm=nn.Sequential(nn.Linear(max(fdim,1),64),nn.ReLU()) if fdim>0 else None
            s.cls=nn.Sequential(nn.Linear(128+(64 if fdim>0 else 0),64),nn.ReLU(),nn.Linear(64,3))
        def forward(s,b,ft):
            z=s.c(b).squeeze(-1)
            if s.fm is not None: z=torch.cat([z,s.fm(ft)],-1)
            return s.cls(z)
    return Net()

def _fit_predict(kind, beats, ref, F, y, pid, tr, cal, te, Sw, mc, seed):
    """kind: 'cnn'(B2/B3) | 'ours'(B4). (calib예측, test예측) 반환."""
    import torch, torch.nn.functional as Fn
    from sklearn.preprocessing import RobustScaler
    dev="cuda" if torch.cuda.is_available() else "cpu"
    torch.manual_seed(seed); np.random.seed(seed)
    sc=RobustScaler().fit(F[tr]); T=lambda X: np.nan_to_num(sc.transform(X),posinf=0,neginf=0).astype("float32")
    Ftr,Fca,Fte=T(F[tr]),T(F[cal]),T(F[te])
    M=(_net(F.shape[1]) if kind=="ours" else _cnn(F.shape[1])).to(dev)
    opt=torch.optim.AdamW(M.parameters(),lr=1e-3,weight_decay=1e-4)
    cw=torch.tensor([1.,Sw,1.5],device=dev); mcv=torch.from_numpy(mc).to(dev)
    def fwd(bb,rr,ff): return M(bb,rr,ff) if kind=="ours" else M(bb,ff)
    @torch.no_grad()
    def pred(idx,Fx):
        M.eval(); o=[]
        for i in range(0,len(idx),4096):
            sl=idx[i:i+4096]
            bb=torch.from_numpy(beats[sl]).to(dev); rr=torch.from_numpy(ref[sl]).to(dev); ff=torch.from_numpy(Fx[i:i+4096]).to(dev)
            o.append(torch.softmax(fwd(bb,rr,ff),-1).cpu().numpy())
        return np.concatenate(o)
    ds=torch.utils.data.TensorDataset(torch.from_numpy(beats[tr]),torch.from_numpy(ref[tr]),
                                      torch.from_numpy(Ftr),torch.from_numpy(y[tr]))
    dl=torch.utils.data.DataLoader(ds,batch_size=512,shuffle=True)
    for ep in range(15):
        M.train()
        for bb,rr,ff,yy in dl:
            bb,rr,ff,yy=(t.to(dev) for t in (bb,rr,ff,yy)); opt.zero_grad()
            lo=fwd(bb,rr,ff); lg=lo-torch.zeros_like(lo).scatter_(1,yy[:,None],mcv[yy][:,None])
            ce=Fn.cross_entropy(lg,yy,reduction="none"); loss=(ce*cw[yy]).sum()/cw[yy].sum()
            loss.backward(); torch.nn.utils.clip_grad_norm_(M.parameters(),1.0); opt.step()
    return pred(cal,Fca), pred(te,Fte)

def bench_models(n_rep=1, k=5, use_ae=True, seed0=0):
    from sklearn.model_selection import GroupKFold, GroupShuffleSplit
    from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
    from sklearn.preprocessing import StandardScaler
    _determinism()
    beats,y,pid,pre,post=_sv()
    FAM=["WST","MORPHO","REPOL","RHYTHM","KOOPMAN","GNN"]+(["AE"] if use_ae else [])
    Fall=_load_feats(FAM+["RR"]); FRR=_load_feats(["RR"]); Fmor=_load_feats(["MORPHO","REPOL","RR"])
    print(f"SVDB {len(y)}비트  S={int((y==1).sum())}({100*(y==1).mean():.2f}%)  레코드 {len(np.unique(pid))}")
    print(f"특징: 전체 {Fall.shape[1]}차원 [{'+'.join(FAM)}+RR]  ※feats0 없음(MIT-BIH판과 상이)")
    print(f"★구성 동결: MIT-BIH 확정 구성 그대로. SVDB에서 재탐색 없음.\n")
    refM=_median_ref(beats,pid)
    refR=robust_template(beats,pid,frac=0.6,conf_cut=0.879,verbose=True)[0]   # DS1서 정한 값 그대로
    ARMS=["B0.다수결","B1.LDA(형태+RR)","B2.CNN(raw)","B3.CNN+RR","B4.본연구","B4C.본연구+센터링"]
    ARMS+= [a for a in EXTRA_ARMS if a not in ARMS]           # 확장 arm(신규 모델)
    if EXTRA_ARMS: print(f"확장 arm {len(EXTRA_ARMS)}개 동반 평가: {list(EXTRA_ARMS)}\n")
    else: print("※ 확장 arm 없음 — B0~B4C 기준선만 돕니다. 신규 모델(R0/R1/R2)도 함께\n"
                "   평가하려면 이 실행을 멈추고 attach_arms() 를 먼저 부르세요.\n"
                "   (런타임이 끊기면 등록이 초기화되므로 재실행 때마다 다시 불러야 합니다.)\n")
    acc={a:[] for a in ARMS}                                  # 각 arm의 test 결정벡터(전 폴드 합침)
    dead=set()                                                # 실패한 확장 arm(전체 실행은 계속)
    order_idx=[]                                              # 대응하는 원본 인덱스
    gkf=GroupKFold(n_splits=k)
    for rep in range(n_rep):
        for fi,(tr_all,te) in enumerate(gkf.split(np.arange(len(y)),y,groups=pid)):
            # 학습셋에서 calib 환자 분리(임계 결정용, test 미사용)
            f_o,c_o=next(GroupShuffleSplit(1,test_size=0.25,random_state=rep).split(tr_all,y[tr_all],groups=pid[tr_all]))
            tr=tr_all[f_o]; cal=tr_all[c_o]
            Sw=auto_weights(y[tr]); nc=np.array([(y[tr]==c).sum() for c in range(3)],np.float32)
            mc=(1.0/np.power(nc,0.25)); mc=(mc/mc.max()*0.5).astype("float32")
            seed=100*rep+fi
            order_idx.append(te)
            # B0
            acc["B0.다수결"].append(np.zeros(len(te),bool))
            # B1 LDA
            ss=StandardScaler().fit(Fmor[tr]); L=LinearDiscriminantAnalysis().fit(ss.transform(Fmor[tr]),y[tr])
            pc=L.predict_proba(ss.transform(Fmor[cal]))[:,1]; pt=L.predict_proba(ss.transform(Fmor[te]))[:,1]
            t=_best_t_f1(pc,y[cal]); acc["B1.LDA(형태+RR)"].append(pt>=t)
            # B2 CNN(raw) / B3 CNN+RR
            for nm,Fx in [("B2.CNN(raw)",np.zeros((len(y),1),"float32")),("B3.CNN+RR",FRR)]:
                pc,pt=_fit_predict("cnn",beats,refM,Fx,y,pid,tr,cal,te,Sw,mc,seed)
                t=_best_t_f1(pc[:,1],y[cal]); acc[nm].append(pt[:,1]>=t)
            # B4 / B4C (같은 모델, 임계법만 다름)
            pc,pt=_fit_predict("ours",beats,refR,Fall,y,pid,tr,cal,te,Sw,mc,seed)
            t=_best_t_f1(pc[:,1],y[cal]); acc["B4.본연구"].append(pt[:,1]>=t)
            cc=_pp_center2(pc[:,1],pid[cal]); ct=_pp_center2(pt[:,1],pid[te]); tc=_best_t_f1(cc,y[cal])
            acc["B4C.본연구+센터링"].append(ct>=tc)
            # ─── 확장 arm (동일 폴드·동일 calib·동일 임계규약) ───
            if EXTRA_ARMS:
                ctx=dict(beats=beats,y=y,pid=pid,pre=pre,post=post,refM=refM,refR=refR,
                         tr=tr,cal=cal,te=te,Sw=Sw,mc=mc,seed=seed,rep=rep,fold=fi,
                         best_t=_best_t_f1)
                for nm,fn in EXTRA_ARMS.items():
                    if nm in dead: continue
                    try:
                        v=np.asarray(fn(ctx)).astype(bool).reshape(-1)
                        if v.shape!=(len(te),): raise ValueError(f"길이 {v.shape} != test {len(te)}")
                        acc[nm].append(v)
                    except Exception as e:
                        # 한 arm의 실패로 15회 학습을 버리지 않는다. 해당 arm만 결과에서 제외.
                        print(f"  ⚠ arm '{nm}' 실패 → 결과에서 제외: {type(e).__name__}: {e}")
                        dead.add(nm)
            print(f"  rep{rep} fold{fi} 완료 (train {len(tr)} / calib {len(cal)} / test {len(te)})")
    if dead: ARMS=[a for a in ARMS if a not in dead]
    idx=np.concatenate(order_idx); yA=y[idx]; pA=pid[idx]
    print(f"\n=== 결과 (환자단위 매크로 F1 = 주지표, 환자 부트스트랩 95%CI) ===")
    RES={}
    for a in ARMS:
        v=np.concatenate(acc[a])
        m,lo,hi,n,fper=_macro(v,yA,pA)
        pr,se,f1=_prf(v,yA)
        # pred: 비트별 판정 벡터(yA/pA 와 같은 순서). 환자별 오류 분해(FP/FN)에 필수 —
        # 이걸 안 남기면 "이 환자가 왜 낮은가"를 사후에 물을 수 없다.
        RES[a]=dict(macro=m,ci=(lo,hi),micro=f1,prec=pr,sen=se,fper=fper,pred=v)
        print(f"  {a:20s} 매크로F1={m:.3f} [{lo:.3f}–{hi:.3f}] (n={n})   micro={f1:.3f} (SEN {se:.3f}/PREC {pr:.3f})")
    # H5 검정: 최다 S 레코드의 micro 기여
    cnt={int(p):int((yA[pA==p]==1).sum()) for p in np.unique(pA)}
    top=max(cnt,key=cnt.get); share=100*cnt[top]/max(sum(cnt.values()),1)
    print(f"\n=== H5 검정: 단일 레코드 지배 여부 ===")
    print(f"  최다 S 레코드 = {top} (S {cnt[top]}, 전체의 {share:.1f}%)   [MIT-BIH #232는 75.2%]")
    print(f"  → {'지배 있음(MIT-BIH와 유사)' if share>40 else '★지배 없음 → #232 지배는 MIT-BIH 고유 현상'}")
    b4=RES["B4.본연구"]; b4c=RES["B4C.본연구+센터링"]; b3=RES["B3.CNN+RR"]
    print(f"\n=== 사전등록 가설 검정 ===")
    print(f"  H3(센터링이 매크로F1 개선): Δ={b4c['macro']-b4['macro']:+.3f}  "
          f"{'★지지' if b4c['ci'][0]>b4['macro'] else '기각/불확정(CI 겹침)'}   [MIT-BIH에선 −0.004로 기각됨]")
    print(f"  제안 vs 최선기준선(B3): Δ매크로={b4['macro']-b3['macro']:+.3f}  "
          f"{'★유의' if b4['ci'][0]>b3['ci'][1] else 'CI 겹침(유의하지 않음)'}")
    print(f"\n  ★해석 규율: CI가 겹치면 '개선'이라 쓰지 않는다. micro는 위 지배율과 함께만 인용한다.")
    if any(a in RES for a in EXTRA_ARMS):
        print(f"\n  ※ 확장 arm 은 주변 CI 비교로 판정하지 말 것. 대응 부트스트랩을 쓰세요:")
        print(f"     report(OUT)   # svdb_rhythm.py — 환자별 F1 차이 + Bonferroni + ±0.07 판정")
    # order: yA/pA/pred 를 원본 배열(beat, pre_rr ...)로 되돌리는 색인. 오류 분석용.
    return dict(res=RES, y=yA, pid=pA, order=idx, top=top, share=share,
                arms=ARMS, dead=sorted(dead))
