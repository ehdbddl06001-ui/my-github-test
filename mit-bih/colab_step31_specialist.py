# =============================================================================
#  colab_step31_specialist.py  —  [STEP 31] 자기전문화 MoE — 라우팅 성패 진단
#
#  사장님 아이디어: 조건을 더/뺀 모델들을 전문가로, DS1 ECG를 '가장 잘 맞춘 전문가'에
#  배정(군집), (다음 단계) 군집으로 전문가 파인튜닝, DS2는 가장 가까운 군집 전문가가 판독.
#  → 파인튜닝 전에 '라우팅이 되나'부터 싸게 검증(그게 성패). OOF 배정으로 순환오류 차단.
#
#  전문가 5 (공통기반 26+WST+morpho, 차별자 더/빼기):
#    A=26+WST  B=+morpho  C=+repolK(best)  D=+segT  E=+xlead
#  진단: ① 오라클 라우팅(천장, DS2라벨=누출) ② 정직 라우팅(특징→승자 예측) ③ 최고단일/균일
#        + 라우터 DS1-CV 정확도(승자가 특징으로 예측되나) + S/F1.
#
#  선행 캐시: _WST, extract_morpho/_MORPHO, extract_repol/_REPOL, extract_segdev/_SEGDEV,
#            extract_xlead/_XLEAD (step12·15·18·28·25)
#  실행:
#    exec(open('/content/drive/MyDrive/mitbih/colab_step31_specialist.py').read())
#    run_specialist(Kwst=40)
# =============================================================================
import os
import numpy as np
from sklearn.metrics import average_precision_score, precision_recall_curve

_DS1=[101,106,108,109,112,114,115,116,118,119,122,124,201,203,205,207,208,209,215,220,223,230]
_DS2=[100,103,105,111,113,117,121,123,200,202,210,212,213,214,219,221,222,228,231,232,233,234]
_SAVE="/content/drive/MyDrive/mitbih/ablation_step31"; _C={}
_REPOLK_IDX=[0,1,4,5]; _SEG_IDX=[9,10,8,4]

def _net(fdim):
    import torch, torch.nn as nn
    class Enc(nn.Module):
        def __init__(s):
            super().__init__(); s.net=nn.Sequential(
                nn.Conv1d(2,32,7,padding=3),nn.BatchNorm1d(32),nn.ReLU(),nn.MaxPool1d(2),
                nn.Conv1d(32,64,5,padding=2),nn.BatchNorm1d(64),nn.ReLU(),nn.MaxPool1d(2),
                nn.Conv1d(64,128,3,padding=1),nn.BatchNorm1d(128),nn.ReLU(),nn.AdaptiveAvgPool1d(1))
            s.proj=nn.Linear(128,64)
        def forward(s,w): return s.proj(s.net(w).squeeze(-1))
    class Net(nn.Module):
        def __init__(s):
            super().__init__(); s.e=Enc(); s.sia=nn.Sequential(nn.Linear(256,64),nn.ReLU())
            s.gate=nn.Linear(128,64); s.proto=nn.Parameter(torch.randn(32,64)*0.1)
            s.fm=nn.Sequential(nn.Linear(fdim,64),nn.ReLU(),nn.Linear(64,64),nn.ReLU())
            s.cls=nn.Sequential(nn.Linear(192,64),nn.ReLU(),nn.Linear(64,3))
        def forward(s,b,r,ft):
            z1=s.e(b); z2=s.e(r); zb=s.sia(torch.cat([z1,z2,z1-z2,(z1-z2).abs()],-1))
            z=z1+torch.sigmoid(s.gate(torch.cat([z1,zb],-1)))*zb
            zp=torch.softmax((z@s.proto.t())*(64**-0.5),-1)@s.proto
            return s.cls(torch.cat([z,zp,s.fm(ft)],-1))
    return Net()

def _f1(y2,s):
    p,r,_=precision_recall_curve((y2==1).astype(int),s); f=2*p*r/(p+r+1e-9); i=int(np.nanargmax(f)); return p[i],r[i],f[i]

def run_specialist(Kwst=40, nseed_oof=1, nseed_full=2, seed0=1000):
    import torch, torch.nn as nn
    from sklearn.preprocessing import RobustScaler, StandardScaler
    from sklearn.model_selection import GroupShuffleSplit, GroupKFold, cross_val_score
    from sklearn.feature_selection import SelectKBest, f_classif
    from sklearn.ensemble import RandomForestClassifier
    dev="cuda" if torch.cuda.is_available() else "cpu"
    d=np.load("/content/drive/MyDrive/mitbih/mamba_data.npz")
    beats,feats0,y,pid=d["beat"],d["feats"],d["y"],d["pid"]
    if "ref" not in _C:
        r=np.empty_like(beats)
        for p in np.unique(pid): m=pid==p; r[m]=np.median(beats[m],axis=0,keepdims=True)
        _C["ref"]=r.astype("float32")
    ref=_C["ref"]
    Xw=globals().get("_WST",None); Xw=Xw if Xw is not None else compute_wst_features(beats)
    Xm=globals().get("_MORPHO",None); Xm=Xm if Xm is not None else extract_morpho_features(beats,ref,pid)
    Xr=globals().get("_REPOL",None); Xr=Xr if Xr is not None else extract_repol_features(beats,ref,pid)
    Xs=globals().get("_SEGDEV",None); Xs=Xs if Xs is not None else extract_segdev_features(beats,ref,pid)
    Xx=globals().get("_XLEAD",None); Xx=Xx if Xx is not None else extract_xlead_features(beats,ref,pid)
    m1=np.isin(pid,_DS1); m2=np.isin(pid,_DS2); y1,p1=y[m1],pid[m1]; y2=y[m2]; N1=int(m1.sum())
    Xwk=np.nan_to_num(SelectKBest(f_classif,k=min(Kwst,Xw.shape[1])).fit(np.nan_to_num(Xw[m1]),y[m1]).transform(np.nan_to_num(Xw))).astype("float32")
    F={"A_wst":np.concatenate([feats0,Xwk],1),
       "B_wstm":np.concatenate([feats0,Xwk,Xm],1),
       "C_repol":np.concatenate([feats0,Xwk,Xm,Xr[:,_REPOLK_IDX]],1),
       "D_segT":np.concatenate([feats0,Xwk,Xm,Xs[:,_SEG_IDX]],1),
       "E_xlead":np.concatenate([feats0,Xwk,Xm,Xx],1)}
    names=list(F); F={k:v.astype("float32") for k,v in F.items()}
    b1,r1,b2,r2=beats[m1],ref[m1],beats[m2],ref[m2]
    def met(p,yy): return average_precision_score((yy==1).astype(int),p[:,1])
    @torch.no_grad()
    def pred(M,sc,b,r,Fraw):
        f=np.nan_to_num(sc.transform(Fraw),posinf=0,neginf=0).astype("float32"); M.eval(); o=[]
        for i in range(0,len(b),4096):
            o.append(torch.softmax(M(torch.from_numpy(b[i:i+4096]).to(dev),torch.from_numpy(r[i:i+4096]).to(dev),torch.from_numpy(f[i:i+4096]).to(dev)),-1).cpu().numpy())
        return np.concatenate(o)
    def fit_expert(Fd1,tr_local,seed):
        torch.manual_seed(seed); np.random.seed(seed)
        a,vb=next(GroupShuffleSplit(1,test_size=0.2,random_state=seed).split(Fd1[tr_local],y1[tr_local],groups=p1[tr_local]))
        tr=tr_local[a]; va=tr_local[vb]
        sc=RobustScaler().fit(Fd1[tr]); f=np.nan_to_num(sc.transform(Fd1),posinf=0,neginf=0).astype("float32")
        M=_net(Fd1.shape[1]).to(dev); opt=torch.optim.AdamW(M.parameters(),lr=1e-3,weight_decay=1e-4)
        lf=nn.CrossEntropyLoss(weight=torch.tensor([1.,3.,1.5],device=dev))
        ds=torch.utils.data.TensorDataset(*[torch.from_numpy(x) for x in (b1[tr],r1[tr],f[tr],y1[tr])]); dl=torch.utils.data.DataLoader(ds,batch_size=512,shuffle=True); best=-1; bs=None
        for ep in range(15):
            M.train()
            for bb,rr,ff,yy in dl:
                bb,rr,ff,yy=(t.to(dev) for t in (bb,rr,ff,yy)); opt.zero_grad()
                loss=lf(M(bb,rr,ff),yy); loss.backward(); torch.nn.utils.clip_grad_norm_(M.parameters(),1.0); opt.step()
            pv=pred(M,sc,b1[va],r1[va],Fd1[va]); s=met(pv,y1[va])
            if s>best: best=s; bs={k:v.cpu() for k,v in M.state_dict().items()}
        M.load_state_dict(bs); return M,sc
    OOF={}; DS2={}; gkf=GroupKFold(2)
    for nm in names:
        Fd1=F[nm][m1]; Fd2=F[nm][m2]; oo=np.zeros((N1,3),np.float32)
        for fa,fb in gkf.split(Fd1,y1,p1):
            acc=np.zeros((len(fb),3),np.float32)
            for s in range(nseed_oof): M,sc=fit_expert(Fd1,fa,seed0+s); acc+=pred(M,sc,b1[fb],r1[fb],Fd1[fb])
            oo[fb]=acc/nseed_oof
        acc=np.zeros((int(m2.sum()),3),np.float32)
        for s in range(nseed_full): M,sc=fit_expert(Fd1,np.arange(N1),seed0+100+s); acc+=pred(M,sc,b2,r2,Fd2)
        OOF[nm]=oo; DS2[nm]=acc/nseed_full
        print(f"  expert {nm:8s}: OOF S={met(oo,y1):.3f}  DS2 S={met(DS2[nm],y2):.3f}")
    os.makedirs(_SAVE,exist_ok=True)
    np.savez(os.path.join(_SAVE,"experts.npz"),**{f"oof_{n}":OOF[n] for n in names},**{f"ds2_{n}":DS2[n] for n in names},y1=y1,y2=y2)
    # ── 승자 배정(OOF, 참클래스 확률 최대) ──
    OA=np.stack([OOF[n] for n in names],0); DA=np.stack([DS2[n] for n in names],0)     # (E,N,3)
    win1=OA[:,np.arange(N1),y1].argmax(0)                                              # DS1 승자
    print("\nDS1 군집 크기:", {names[k]:int((win1==k).sum()) for k in range(len(names))})
    print("DS1 S비트 군집:", {names[k]:int(((win1==k)&(y1==1)).sum()) for k in range(len(names))})
    # ── 라우터: 특징→승자 (승자가 특징으로 예측되나) ──
    G=np.concatenate([feats0,Xwk,Xm,Xr[:,_REPOLK_IDX],Xs[:,_SEG_IDX],Xx],1)
    scg=StandardScaler().fit(np.nan_to_num(G[m1])); G1=np.nan_to_num(scg.transform(np.nan_to_num(G[m1]))); G2=np.nan_to_num(scg.transform(np.nan_to_num(G[m2])))
    rf=RandomForestClassifier(n_estimators=200,max_depth=12,n_jobs=-1,random_state=0,class_weight="balanced")
    cv=cross_val_score(rf,G1,win1,cv=3).mean(); rf.fit(G1,win1)
    print(f"\n라우터 DS1-CV 승자예측 정확도={cv:.3f}  (무작위={1/len(names):.3f})  ← 특징으로 전문성 예측되나")
    # ── DS2 라우팅 ──
    def routed(sel): return DA[sel,np.arange(len(y2))]
    honest=routed(rf.predict(G2))                                                      # 정직(특징→승자)
    oracle=routed(DA[:,np.arange(len(y2)),y2].argmax(0))                               # 오라클(참, 누출 천장)
    uni=DA.mean(0); uni=uni/uni.sum(-1,keepdims=True)
    best_single=max(names,key=lambda n:met(DS2[n],y2))
    print(f"\n{'='*54}\n[DS2] (라우팅은 특징만, 오라클은 라벨=누출 천장)")
    for nm,P in [(f"최고단일({best_single})",DS2[best_single]),("균일평균",uni),("정직 라우팅",honest),("오라클 라우팅",oracle)]:
        pr,se,f1=_f1(y2,P[:,1]); print(f"  {nm:16s} S={met(P,y2):.4f}  |  PREC={pr:.3f} SEN={se:.3f} F1={f1:.3f}")
    print(f"\n▶ 정직 라우팅 > 최고단일 이면 = 사장님 전문화 구조 성립(→STEP32 파인튜닝).")
    print(f"  오라클만 높고 정직 낮으면 = 라우팅이 병목(특징이 전문성 예측 못함). 오라클도 낮으면 = 상보성 부족.")
    return dict(OOF=OOF,DS2=DS2,win1=win1,router=rf,names=names)
