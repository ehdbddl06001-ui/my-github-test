# =============================================================================
#  colab_step42_autoweight.py  —  [STEP 42] 클래스 가중치 자동탐색 (DB 전이 가능)
#
#  고정 S가중치(4)는 MIT-BIH의 S비율에 맞춘 것 → 다른 DB(S 많을 수도)엔 안 맞음.
#  '규칙'으로 데이터에서 가중치를 계산/탐색하면 어떤 DB에도 자동 적응:
#   ① 역빈도(balanced): w_S=n/(K·n_S)   ② 유효표본수: w∝(1-β)/(1-β^n)  ③ DS1-val peak 탐색
#  base=best+DTW_full 위에서 S가중치 스윕 → DS1-val S와 DS2 S 둘 다 기록 →
#  DS1-val 최고 가중치가 DS2 peak와 맞나(=val로 자동선택이 전이되나) 검증.
#
#  선행 캐시: _WST, _MORPHO, _REPOL, _DTW(15특징 v2)
#  실행:
#    exec(open('/content/drive/MyDrive/mitbih/colab_step42_autoweight.py').read())
#    run_autoweight()          # weights·seeds 조절 가능
# =============================================================================
import os
import numpy as np
from sklearn.metrics import average_precision_score, precision_recall_curve

_DS1=[101,106,108,109,112,114,115,116,118,119,122,124,201,203,205,207,208,209,215,220,223,230]
_DS2=[100,103,105,111,113,117,121,123,200,202,210,212,213,214,219,221,222,228,231,232,233,234]
_C={}; _REPOLK_IDX=[0,1,4,5]

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

def auto_weights(y1, beta=0.9999):
    """데이터에서 S가중치 자동계산: 역빈도(balanced) + 유효표본수(β). N=1 기준 S배수 반환."""
    nN=(y1==0).sum(); nS=(y1==1).sum(); nV=(y1==2).sum()
    bal_S=nN/max(nS,1)                                        # 역빈도(N대비 S배수)
    eff=lambda n:(1-beta)/(1-beta**n+1e-12)
    en_S=eff(nS)/eff(nN)                                      # 유효표본수(N대비 S배수)
    return dict(nN=int(nN),nS=int(nS),nV=int(nV),balanced_S=float(bal_S),effnum_S=float(en_S))

def run_autoweight(Kwst=40, weights=(2.,4.,6.,8.,12.,16.), seeds=None):
    import torch, torch.nn as nn
    from sklearn.preprocessing import RobustScaler
    from sklearn.model_selection import GroupShuffleSplit
    from sklearn.feature_selection import SelectKBest, f_classif
    seeds=seeds or list(range(1000,1006)); dev="cuda" if torch.cuda.is_available() else "cpu"
    d=np.load("/content/drive/MyDrive/mitbih/mamba_data.npz"); beats,feats0,y,pid=d["beat"],d["feats"],d["y"],d["pid"]
    if "ref" not in _C:
        r=np.empty_like(beats)
        for p in np.unique(pid): m=pid==p; r[m]=np.median(beats[m],axis=0,keepdims=True)
        _C["ref"]=r.astype("float32")
    ref=_C["ref"]
    Xw=globals().get("_WST"); Xm=globals().get("_MORPHO"); Xr=globals().get("_REPOL"); Xd=globals().get("_DTW")
    m1=np.isin(pid,_DS1); m2=np.isin(pid,_DS2); y2=y[m2]
    Xwk=np.nan_to_num(SelectKBest(f_classif,k=min(Kwst,Xw.shape[1])).fit(np.nan_to_num(Xw[m1]),y[m1]).transform(np.nan_to_num(Xw))).astype("float32")
    F=np.concatenate([feats0,Xwk,Xm,Xr[:,_REPOLK_IDX],Xd],1).astype("float32")
    aw=auto_weights(y[m1]); print(f"DS1 클래스수 N={aw['nN']} S={aw['nS']} V={aw['nV']}")
    print(f"자동 제안 S가중치:  역빈도(balanced)={aw['balanced_S']:.1f}   유효표본수(β=.9999)={aw['effnum_S']:.1f}")
    def met(p,yy): return (average_precision_score((yy==1).astype(int),p[:,1]),average_precision_score((yy==2).astype(int),p[:,2]))
    @torch.no_grad()
    def pred(M,b,r,ft):
        M.eval(); o=[]
        for i in range(0,len(b),4096):
            o.append(torch.softmax(M(torch.from_numpy(b[i:i+4096]).to(dev),torch.from_numpy(r[i:i+4096]).to(dev),torch.from_numpy(ft[i:i+4096]).to(dev)),-1).cpu().numpy())
        return np.concatenate(o)
    def train_one(seed,Sw):
        b1,r1,f1a,y1,p1=beats[m1],ref[m1],F[m1],y[m1],pid[m1]; b2,r2,f2a=beats[m2],ref[m2],F[m2]
        torch.manual_seed(seed); np.random.seed(seed)
        tr,va=next(GroupShuffleSplit(1,test_size=0.2,random_state=seed).split(f1a,y1,groups=p1))
        sc=RobustScaler().fit(f1a[tr]); f1=np.nan_to_num(sc.transform(f1a),posinf=0,neginf=0).astype("float32"); f2=np.nan_to_num(sc.transform(f2a),posinf=0,neginf=0).astype("float32")
        M=_net(F.shape[1]).to(dev); opt=torch.optim.AdamW(M.parameters(),lr=1e-3,weight_decay=1e-4)
        lf=nn.CrossEntropyLoss(weight=torch.tensor([1.,Sw,1.5],device=dev))
        ds=torch.utils.data.TensorDataset(*[torch.from_numpy(x) for x in (b1[tr],r1[tr],f1[tr],y1[tr])]); dl=torch.utils.data.DataLoader(ds,batch_size=512,shuffle=True); best=-1; bs=None; bvalS=0
        for ep in range(15):
            M.train()
            for bb,rr,ff,yy in dl:
                bb,rr,ff,yy=(t.to(dev) for t in (bb,rr,ff,yy)); opt.zero_grad()
                loss=lf(M(bb,rr,ff),yy); loss.backward(); torch.nn.utils.clip_grad_norm_(M.parameters(),1.0); opt.step()
            pv=pred(M,b1[va],r1[va],f1[va]); s,v=met(pv,y1[va])
            if 0.5*(s+v)>best: best=0.5*(s+v); bvalS=s; bs={k:v.cpu() for k,v in M.state_dict().items()}
        M.load_state_dict(bs); return pred(M,b2,r2,f2), bvalS                 # DS2예측, DS1-val S
    def trim(Pn):
        medS=np.median(Pn[:,:,1],0); corr=np.array([np.corrcoef(Pn[i,:,1],medS)[0,1] for i in range(len(Pn))])
        keep=np.argsort(-corr)[:max(1,int(round(len(Pn)*0.8)))]; P=Pn[keep].mean(0); return P/P.sum(1,keepdims=True)
    print(f"\n{'가중치':>6} {'DS1-val S':>10} {'DS2 S':>8} {'PREC':>6} {'F1':>6}")
    res={}
    for Sw in weights:
        preds=[]; vals=[]
        for s in seeds: p,vs=train_one(s,Sw); preds.append(p); vals.append(vs)
        Pt=trim(np.stack(preds,0)); S,V=met(Pt,y2); pr,se,f1=_f1(y2,Pt[:,1]); vm=float(np.mean(vals))
        res[Sw]=(vm,S,pr,f1); print(f"{Sw:6.1f} {vm:10.4f} {S:8.4f} {pr:6.3f} {f1:6.3f}")
    wpk_val=max(res,key=lambda k:res[k][0]); wpk_ds2=max(res,key=lambda k:res[k][1])
    print(f"\n▶ DS1-val 최고 가중치={wpk_val} (→그때 DS2 S={res[wpk_val][1]:.4f})   |   실제 DS2 최고={wpk_ds2} (S={res[wpk_ds2][1]:.4f})")
    print(f"  둘이 같/가까우면 = 'DS1-val로 자동선택'이 전이됨 → 다른 DB도 이 함수로 peak 자동탐색 가능.")
    print(f"  참고 자동값: 역빈도={aw['balanced_S']:.0f}, 유효표본수={aw['effnum_S']:.1f} (스윕 범위 밖이면 확장 고려)")
    return res
