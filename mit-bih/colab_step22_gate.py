# =============================================================================
#  colab_step22_gate.py  —  [STEP 22] 비트별 T파 게이트 F (DS1 학습 → DS2 눈감고 적용)
#
#  사장님 아이디어: seed가 아니라 '개별 ECG마다' T파(재분극) 정보를 쓸지/얼마나 쓸지
#  판단하는 함수 F. DS1의 각 ECG로 F를 학습(F 모델), DS2의 각 ECG 특징을 F에 넣어
#  비트별로 base(T파X) ↔ repol(T파O) 전문가를 섞는 α를 정한다.  inductive(ECG 1개로 추론).
#
#  전문가 2: E_base=26+WST+morpho , E_repol=+repolK(RT중심·T비대칭).  둘 다 DS1 학습.
#  게이트 F: 입력=그 비트의 형태특징(morpho16+repol12, 표준화), 출력=α∈[0,1](repol 비중).
#    최종확률 = α·repol + (1-α)·base.  F는 DS1에서 α를 움직여 DS1 라벨을 맞추게 학습.
#  ★ 누출 차단: 전문가가 '안 본' DS1 비트로 게이트를 학습해야 함 → 환자별 2-fold OOF.
#    가중치(F)는 DS1만, DS2는 최종 평가만.
#
#  선행(캐시): _WST, extract_morpho_features, extract_repol_features/_REPOL
#  실행:
#    exec(open('/content/drive/MyDrive/mitbih/colab_step22_gate.py').read())
#    run_gate(Kwst=40)               # nseed_oof=2, nseed_full=3 (원하면 조절)
# =============================================================================
import os
import numpy as np
from sklearn.metrics import average_precision_score

_DS1=[101,106,108,109,112,114,115,116,118,119,122,124,201,203,205,207,208,209,215,220,223,230]
_DS2=[100,103,105,111,113,117,121,123,200,202,210,212,213,214,219,221,222,228,231,232,233,234]
_SAVE="/content/drive/MyDrive/mitbih/ablation_step22"; _C={}
_REPOLK_IDX=[0,1,4,5]

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

def run_gate(Kwst=40, nseed_oof=2, nseed_full=3, seed0=1000):
    import torch, torch.nn as nn, torch.nn.functional as Fn
    from sklearn.preprocessing import RobustScaler
    from sklearn.model_selection import GroupShuffleSplit, GroupKFold
    from sklearn.feature_selection import SelectKBest, f_classif
    dev="cuda" if torch.cuda.is_available() else "cpu"
    d=np.load("/content/drive/MyDrive/mitbih/mamba_data.npz")
    beats,feats0,y,pid=d["beat"],d["feats"],d["y"],d["pid"]
    if "ref" not in _C:
        r=np.empty_like(beats)
        for p in np.unique(pid):
            m=pid==p; r[m]=np.median(beats[m],axis=0,keepdims=True)
        _C["ref"]=r.astype("float32")
    ref=_C["ref"]
    Xw=globals().get("_WST",None); Xw=Xw if Xw is not None else compute_wst_features(beats)
    Xm=globals().get("_MORPHO",None); Xm=Xm if Xm is not None else extract_morpho_features(beats,ref,pid)
    Xr=globals().get("_REPOL",None); Xr=Xr if Xr is not None else extract_repol_features(beats,ref,pid)
    m1=np.isin(pid,_DS1); m2=np.isin(pid,_DS2)
    Xwk=np.nan_to_num(SelectKBest(f_classif,k=min(Kwst,Xw.shape[1])).fit(np.nan_to_num(Xw[m1]),y[m1]).transform(np.nan_to_num(Xw))).astype("float32")
    Fwm =np.concatenate([feats0,Xwk,Xm],1).astype("float32")               # 전문가1 특징
    Fwmr=np.concatenate([feats0,Xwk,Xm,Xr[:,_REPOLK_IDX]],1).astype("float32")  # 전문가2 특징
    G   =np.concatenate([Xm,Xr],1).astype("float32")                       # 게이트 입력=형태특징(morpho16+repol12)
    # DS1/DS2 슬라이스
    y1,p1=y[m1],pid[m1]; y2=y[m2]
    b1,r1,b2,r2=beats[m1],ref[m1],beats[m2],ref[m2]
    N1=int(m1.sum())
    def met(p,yy): return (average_precision_score((yy==1).astype(int),p[:,1]),average_precision_score((yy==2).astype(int),p[:,2]))
    @torch.no_grad()
    def _pred(M,sc,b,r,Fraw):
        f=np.nan_to_num(sc.transform(Fraw),posinf=0,neginf=0).astype("float32"); M.eval(); o=[]
        for i in range(0,len(b),4096):
            o.append(torch.softmax(M(torch.from_numpy(b[i:i+4096]).to(dev),torch.from_numpy(r[i:i+4096]).to(dev),torch.from_numpy(f[i:i+4096]).to(dev)),-1).cpu().numpy())
        return np.concatenate(o)
    def fit_expert(Fds1, bA,rA, tr_local, seed):
        """DS1 인덱스 tr_local 로 학습(내부 조기종료 split). 반환 (M, scaler)."""
        torch.manual_seed(seed); np.random.seed(seed)
        a,vb=next(GroupShuffleSplit(1,test_size=0.2,random_state=seed).split(Fds1[tr_local],y1[tr_local],groups=p1[tr_local]))
        tr=tr_local[a]; va=tr_local[vb]
        sc=RobustScaler().fit(Fds1[tr]); f=np.nan_to_num(sc.transform(Fds1),posinf=0,neginf=0).astype("float32")
        M=_net(Fds1.shape[1]).to(dev); opt=torch.optim.AdamW(M.parameters(),lr=1e-3,weight_decay=1e-4)
        lf=nn.CrossEntropyLoss(weight=torch.tensor([1.,3.,1.5],device=dev))
        ds=torch.utils.data.TensorDataset(*[torch.from_numpy(x) for x in (bA[tr],rA[tr],f[tr],y1[tr])])
        dl=torch.utils.data.DataLoader(ds,batch_size=512,shuffle=True); best=-1; bs=None
        for ep in range(15):
            M.train()
            for bb,rr,ff,yy in dl:
                bb,rr,ff,yy=(t.to(dev) for t in (bb,rr,ff,yy)); opt.zero_grad()
                loss=lf(M(bb,rr,ff),yy); loss.backward(); torch.nn.utils.clip_grad_norm_(M.parameters(),1.0); opt.step()
            pv=_pred(M,sc,bA[va],rA[va],Fds1[va]); s,v=met(pv,y1[va])
            if 0.5*(s+v)>best: best=0.5*(s+v); bs={k:v.cpu() for k,v in M.state_dict().items()}
        M.load_state_dict(bs); return M,sc
    FwmD1,FwmrD1=Fwm[m1],Fwmr[m1]; FwmD2,FwmrD2=Fwm[m2],Fwmr[m2]
    # ── 1) OOF 전문가 예측(환자별 2-fold) : 게이트 학습용 (전문가가 안 본 DS1 비트) ──
    base_oof=np.zeros((N1,3),np.float32); repol_oof=np.zeros((N1,3),np.float32)
    gkf=GroupKFold(n_splits=2)
    print("OOF 전문가(게이트 학습용) ...")
    for fa,fb in gkf.split(FwmD1,y1,p1):
        aB=np.zeros((len(fb),3),np.float32); aR=np.zeros((len(fb),3),np.float32)
        for s in range(nseed_oof):
            Mb,sb=fit_expert(FwmD1,b1,r1,fa,seed0+s);      aB+=_pred(Mb,sb,b1[fb],r1[fb],FwmD1[fb])
            Mr,sr=fit_expert(FwmrD1,b1,r1,fa,seed0+50+s);  aR+=_pred(Mr,sr,b1[fb],r1[fb],FwmrD1[fb])
        base_oof[fb]=aB/nseed_oof; repol_oof[fb]=aR/nseed_oof
    print(f"  OOF base S={met(base_oof,y1)[0]:.3f}  repol S={met(repol_oof,y1)[0]:.3f}")
    # ── 2) 최종 전문가(전체 DS1 학습) → DS2 예측 ──
    print("최종 전문가(전체 DS1) → DS2 ...")
    alltr=np.arange(N1); PB2=np.zeros((int(m2.sum()),3),np.float32); PR2=np.zeros((int(m2.sum()),3),np.float32)
    for s in range(nseed_full):
        Mb,sb=fit_expert(FwmD1,b1,r1,alltr,seed0+s);     PB2+=_pred(Mb,sb,b2,r2,FwmD2)
        Mr,sr=fit_expert(FwmrD1,b1,r1,alltr,seed0+50+s); PR2+=_pred(Mr,sr,b2,r2,FwmrD2)
    PB2/=nseed_full; PR2/=nseed_full
    # ── 3) 게이트 F: 입력=형태특징(표준화), α로 base↔repol 혼합, DS1 OOF로 학습 ──
    G1,G2=G[m1],G[m2]; scg=RobustScaler().fit(np.nan_to_num(G1))
    g1=torch.from_numpy(np.nan_to_num(scg.transform(np.nan_to_num(G1)),posinf=0,neginf=0).astype("float32")).to(dev)
    g2=torch.from_numpy(np.nan_to_num(scg.transform(np.nan_to_num(G2)),posinf=0,neginf=0).astype("float32")).to(dev)
    gate=nn.Sequential(nn.Linear(G1.shape[1],32),nn.ReLU(),nn.Linear(32,1)).to(dev)
    gopt=torch.optim.Adam(gate.parameters(),lr=3e-3,weight_decay=1e-3)
    Bp=torch.from_numpy(base_oof).to(dev); Rp=torch.from_numpy(repol_oof).to(dev)
    yt=torch.from_numpy(y1.astype("int64")).to(dev); wcls=torch.tensor([1.,3.,1.5],device=dev)
    torch.manual_seed(0)
    for it in range(400):
        a=torch.sigmoid(gate(g1))                       # (N1,1) 비트별 repol 비중
        final=a*Rp+(1-a)*Bp                             # 확률 볼록결합(단순plex 유지)
        loss=Fn.nll_loss(torch.log(final.clamp_min(1e-6)),yt,weight=wcls)
        gopt.zero_grad(); loss.backward(); gopt.step()
    with torch.no_grad():
        a1=torch.sigmoid(gate(g1)).cpu().numpy().ravel()
        a2=torch.sigmoid(gate(g2)).cpu().numpy().ravel()
    os.makedirs(_SAVE,exist_ok=True)
    np.savez(os.path.join(_SAVE,"gate.npz"),base_oof=base_oof,repol_oof=repol_oof,PB2=PB2,PR2=PR2,a1=a1,a2=a2,y1=y1,y2=y2,pid2=pid[m2])
    # ── 4) 비교 (DS2) ──
    def norm(P): return P/P.sum(-1,keepdims=True)
    gated2=norm(a2[:,None]*PR2+(1-a2[:,None])*PB2)
    print(f"\n{'='*58}\nα(repol 비중) 분포:  DS1 mean={a1.mean():.2f} std={a1.std():.2f} | DS2 mean={a2.mean():.2f} std={a2.std():.2f}")
    print(f"  DS2 S비트 α평균={a2[y2==1].mean():.2f}  N비트 α평균={a2[y2==0].mean():.2f}  (S에서 α↑면 게이트가 T파를 옳게 켬)")
    print(f"\n[DS2 결과]  (게이트 F는 DS1만으로 학습, DS2는 평가만)")
    rB=met(PB2,y2); rR=met(PR2,y2); r5=met(norm(0.5*PB2+0.5*PR2),y2); rG=met(gated2,y2)
    print(f"  base(T파X)          S={rB[0]:.4f}  V={rB[1]:.4f}")
    print(f"  repol(T파O)         S={rR[0]:.4f}  V={rR[1]:.4f}")
    print(f"  0.5 고정혼합         S={r5[0]:.4f}  V={r5[1]:.4f}")
    print(f"  ★ 게이트 F(비트별α)  S={rG[0]:.4f}  V={rG[1]:.4f}")
    best=max(rB[0],rR[0],r5[0])
    print(f"\n▶ 게이트 − max(base,repol,0.5) = {rG[0]-best:+.4f}")
    print("  >0: 비트별 T파 판단이 고정혼합보다 이득(사장님 구조 성립).  ≤0: 형태특징으로 언제 T파 쓸지 예측 불가.")
    return dict(a2=a2,PB2=PB2,PR2=PR2,gated=gated2)
