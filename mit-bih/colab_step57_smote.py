# =============================================================================
#  colab_step57_smote.py  —  [STEP 57] SMOTE/Borderline/ADASYN — subtle S 경계 증강
#
#  소수 S(특히 경계의 subtle S)를 특징+파형 공간에서 합성해 학습에 추가 → 모델이 애매한
#  S 경계를 더 배움 → 민감도↑ 기대. DS1 학습셋에서만 합성(라벨 O이지만 train만 = 오염X).
#   · SMOTE      : S의 kNN(같은 S) 사이 선형보간
#   · Borderline : 이웃 다수가 非S인 '경계 S'만 증강(정확히 subtle S 겨냥)
#   · ADASYN     : 배우기 어려운 S(非S 이웃 많음)에 더 많이 합성
#  파형·기준비트·특징을 같은 λ로 보간(멀티모달 SMOTE). best(RKG) 위 15seed 비교.
#  ★ 합성은 매 fold의 DS1-train 안에서만. DS2는 절대 안 씀.
#
#  선행: colab_prep_all.py
#  실행:
#    exec(open('/content/drive/MyDrive/mitbih/colab_step57_smote.py').read())
#    run_smote()              # none vs SMOTE vs Borderline vs ADASYN (margin CNN 15seed)
# =============================================================================
import os
import numpy as np
from sklearn.metrics import average_precision_score, precision_recall_curve

_BASE="/content/drive/MyDrive/mitbih"; _FEATDIR=f"{_BASE}/synergy_feats"
_DS1=[101,106,108,109,112,114,115,116,118,119,122,124,201,203,205,207,208,209,215,220,223,230]
_DS2=[100,103,105,111,113,117,121,123,200,202,210,212,213,214,219,221,222,228,231,232,233,234]

def _f1(y2,s):
    p,r,_=precision_recall_curve((y2==1).astype(int),s); f=2*p*r/(p+r+1e-9); i=int(np.nanargmax(f)); return p[i],r[i],f[i]
def auto_weights(y1,beta=0.9999):
    nN=(y1==0).sum(); nS=max((y1==1).sum(),1); eff=lambda n:(1-beta)/(1-beta**n+1e-12); return float(eff(nS)/eff(nN))
def _Lnpy(n):
    p=f"{_FEATDIR}/{n}.npy"; return np.load(p) if os.path.exists(p) else None
def _bestF(fams=("RHYTHM","KOOPMAN","GNN")):
    d=np.load(f"{_BASE}/mamba_data.npz"); beats,y,pid=d["beat"],d["y"],d["pid"]
    BB=[_Lnpy(n) for n in ["feats0","WST","MORPHO","REPOL","DTW"]+list(fams)]
    if any(x is None for x in BB): raise RuntimeError("캐시 없음 → colab_prep_all.py 먼저")
    return beats,y,pid,np.concatenate(BB,1).astype("float32"),"+".join(fams)

def _smote(kind, Xs, b, r, fr, ysub, k=5, mult=2, rng=None):
    """DS1-train 안에서 S 합성. Xs=이웃탐색용(스케일특징), b/r/fr=파형/기준/원특징, ysub=라벨."""
    from sklearn.neighbors import NearestNeighbors
    Si=np.where(ysub==1)[0]
    if len(Si)<k+2: return b,r,fr,ysub
    nnS=NearestNeighbors(n_neighbors=k+1).fit(Xs[Si]); _,nbr=nnS.kneighbors(Xs[Si])   # S 내부 이웃
    base=np.arange(len(Si)); w=None
    if kind in ("borderline","adasyn"):
        nnA=NearestNeighbors(n_neighbors=k+1).fit(Xs); _,nbrA=nnA.kneighbors(Xs[Si])
        nonS=np.array([(ysub[nbrA[i,1:]]!=1).mean() for i in range(len(Si))])
        if kind=="borderline":
            base=np.where((nonS>0.3)&(nonS<1.0))[0]                       # 경계(노이즈 제외)
            if len(base)<1: base=np.arange(len(Si))
        else:
            w=(nonS+1e-3); w=w/w.sum()                                    # 어려운 S 가중
    nsyn=int(mult*len(Si)); sb=[];sr=[];sf=[]
    picks=rng.choice(base if w is None else np.arange(len(Si)), size=nsyn, p=w)
    for pi in picks:
        j=Si[nbr[pi, rng.randint(1,k+1)]]; a=Si[pi]; lam=rng.rand()
        sb.append(b[a]*(1-lam)+b[j]*lam); sr.append(r[a]*(1-lam)+r[j]*lam); sf.append(fr[a]*(1-lam)+fr[j]*lam)
    b2=np.concatenate([b,np.array(sb,b.dtype)]); r2=np.concatenate([r,np.array(sr,r.dtype)])
    fr2=np.concatenate([fr,np.array(sf,fr.dtype)]); y2=np.concatenate([ysub,np.ones(nsyn,ysub.dtype)])
    return b2,r2,fr2,y2

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

def run_smote(fams=("RHYTHM","KOOPMAN","GNN"), seeds=None, mult=2):
    import torch, torch.nn as nn, torch.nn.functional as Fn
    from sklearn.preprocessing import RobustScaler
    from sklearn.model_selection import GroupShuffleSplit
    seeds=seeds or list(range(2000,2015)); dev="cuda" if torch.cuda.is_available() else "cpu"
    beats,y,pid,BEST,bb=_bestF(fams); print(f"백본: {bb}"); ref=np.empty_like(beats)
    for p in np.unique(pid): m=pid==p; ref[m]=np.median(beats[m],0,keepdims=True)
    ref=ref.astype("float32"); m1=np.isin(pid,_DS1); m2=np.isin(pid,_DS2); y2=y[m2]
    Sw=auto_weights(y[m1]); nc=np.array([(y[m1]==k).sum() for k in range(3)],np.float32); mc=(1.0/np.power(nc,0.25)); mc=(mc/mc.max()*0.5).astype("float32")
    def met(p,yy): return (average_precision_score((yy==1).astype(int),p[:,1]),average_precision_score((yy==2).astype(int),p[:,2]))
    @torch.no_grad()
    def pred(M,b,r,ft):
        M.eval(); o=[]
        for i in range(0,len(b),4096):
            o.append(torch.softmax(M(torch.from_numpy(b[i:i+4096]).to(dev),torch.from_numpy(r[i:i+4096]).to(dev),torch.from_numpy(ft[i:i+4096]).to(dev)),-1).cpu().numpy())
        return np.concatenate(o)
    def train_one(kind,seed):
        rng=np.random.RandomState(seed)
        b1,r1,fr1,y1,p1=beats[m1],ref[m1],BEST[m1],y[m1],pid[m1]; b2,r2,fr2=beats[m2],ref[m2],BEST[m2]
        torch.manual_seed(seed); np.random.seed(seed)
        tr,va=next(GroupShuffleSplit(1,test_size=0.2,random_state=seed).split(fr1,y1,groups=p1))
        sc=RobustScaler().fit(fr1[tr])
        bt,rt,frt,yt=b1[tr],r1[tr],fr1[tr],y1[tr]
        if kind!="none":                                                 # DS1-train 안에서만 합성
            Xs=np.nan_to_num(sc.transform(frt),posinf=0,neginf=0)
            bt,rt,frt,yt=_smote(kind,Xs,bt,rt,frt,yt,mult=mult,rng=rng)
        ftr=np.nan_to_num(sc.transform(frt),posinf=0,neginf=0).astype("float32")
        fva=np.nan_to_num(sc.transform(fr1[va]),posinf=0,neginf=0).astype("float32")
        f2=np.nan_to_num(sc.transform(fr2),posinf=0,neginf=0).astype("float32")
        M=_net(BEST.shape[1]).to(dev); opt=torch.optim.AdamW(M.parameters(),lr=1e-3,weight_decay=1e-4)
        cw=torch.tensor([1.,Sw,1.5],device=dev); mcv=torch.from_numpy(mc).to(dev)
        ds=torch.utils.data.TensorDataset(*[torch.from_numpy(x) for x in (bt,rt,ftr,yt)]); dl=torch.utils.data.DataLoader(ds,batch_size=512,shuffle=True); best=-1; bs=None
        for ep in range(15):
            M.train()
            for bb,rr,ff,yy in dl:
                bb,rr,ff,yy=(t.to(dev) for t in (bb,rr,ff,yy)); opt.zero_grad()
                lo=M(bb,rr,ff); lg=lo-torch.zeros_like(lo).scatter_(1,yy[:,None],mcv[yy][:,None])
                ce=Fn.cross_entropy(lg,yy,reduction="none"); wv=cw[yy]; loss=(ce*wv).sum()/wv.sum()
                loss.backward(); torch.nn.utils.clip_grad_norm_(M.parameters(),1.0); opt.step()
            pv=pred(M,b1[va],r1[va],fva); s,v=met(pv,y1[va])
            if 0.5*(s+v)>best: best=0.5*(s+v); bs={k:vv.cpu() for k,vv in M.state_dict().items()}
        M.load_state_dict(bs); return pred(M,b2,r2,f2)
    def trim(Pn):
        medS=np.median(Pn[:,:,1],0); corr=np.array([np.corrcoef(Pn[i,:,1],medS)[0,1] for i in range(len(Pn))])
        keep=np.argsort(-corr)[:max(1,int(round(len(Pn)*0.8)))]; P=Pn[keep].mean(0); return P/P.sum(1,keepdims=True)
    res={}
    print(f"margin CNN {len(seeds)}seed, Sw={Sw:.1f}, mult={mult} (합성은 DS1-train 안에서만)")
    for kind in ["none","SMOTE","borderline","adasyn"]:
        Pt=trim(np.stack([train_one(kind,s) for s in seeds],0)); S,V=met(Pt,y2); pr,se,f1=_f1(y2,Pt[:,1]); res[kind]=(S,pr,se,f1)
        print(f"  {kind:12s} S={S:.4f} PREC={pr:.3f} SEN={se:.3f} F1={f1:.3f}")
    b=res["none"]
    print(f"\n▶ none 대비:")
    for kind,(S,pr,se,f1) in res.items():
        if kind=="none": continue
        print(f"  {kind:12s}: ΔS={S-b[0]:+.4f} ΔPREC={pr-b[1]:+.3f} ΔSEN={se-b[2]:+.3f} ΔF1={f1-b[3]:+.3f}")
    print(f"\n  ★ ΔSEN>0 & F1↑ = subtle S 합성이 경계학습에 도움. borderline이 특히 subtle 겨냥.")
    return res

# 여러 백본 한 번에 (균형형 / 정밀형 / 4가지)
def run_smote_backbones(seeds=None, mult=2):
    R={}
    for fams in [("RHYTHM","KOOPMAN","GNN"),("KOOPMAN","AE","GNN"),("RHYTHM","KOOPMAN","AE","GNN")]:
        print("\n"+"="*58); R["+".join(fams)]=run_smote(fams,seeds,mult)
    return R
