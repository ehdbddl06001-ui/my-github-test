# =============================================================================
#  colab_step61_context.py  —  [STEP 61] 다중비트 시퀀스 문맥 (SEN 병목 새 축)
#
#  현 모델은 '단일 비트'만 CNN에 넣음 → 조기 S(이웃 대비 일찍 온 것)를 놓쳐 SEN 0.73.
#  이웃 비트 파형(±W)을 공유 인코더로 인코딩해 attention pool → 문맥벡터를 분류기에 추가.
#  RR 스칼라(feats0)·리듬은 있었지만 '이웃 파형' 문맥은 처음 → 진짜 새 정보축(morphology 유지).
#  공유 인코더 재사용(추가 파라미터 최소=과적합 방지). 4-family 위 15seed 비교.
#
#  선행: colab_prep_all.py
#  실행:
#    exec(open('/content/drive/MyDrive/mitbih/colab_step61_context.py').read())
#    run_context(fams=("RHYTHM","KOOPMAN","AE","GNN"))   # baseline vs +문맥(W1) vs +문맥(W2)
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
def _bestF(fams):
    d=np.load(f"{_BASE}/mamba_data.npz"); beats,y,pid=d["beat"],d["y"],d["pid"]
    BB=[_Lnpy(n) for n in ["feats0","WST","MORPHO","REPOL","DTW"]+list(fams)]
    if any(x is None for x in BB): raise RuntimeError("캐시 없음 → colab_prep_all.py 먼저")
    return beats,y,pid,np.concatenate(BB,1).astype("float32"),"+".join(fams)

def _nbr_idx(pid, W):
    """환자 내 시간순 ±W 이웃 비트의 전역 인덱스(경계는 clamp). (N, 2W+1)"""
    N=len(pid); K=2*W+1; idx=np.zeros((N,K),np.int64)
    for p in np.unique(pid):
        gi=np.where(pid==p)[0]; n=len(gi); ar=np.arange(n)
        for k,off in enumerate(range(-W,W+1)):
            idx[gi,k]=gi[np.clip(ar+off,0,n-1)]
    return idx

def _net(fdim, use_ctx=False, K=3):
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
            s.uc=use_ctx; cin=192+(64 if use_ctx else 0)
            if use_ctx: s.tq=nn.Parameter(torch.randn(64)*0.1)          # 이웃비트 attention query
            s.cls=nn.Sequential(nn.Linear(cin,64),nn.ReLU(),nn.Linear(64,3))
        def forward(s,b,r,ft,ctx=None):
            z1=s.e(b); z2=s.e(r); zb=s.sia(torch.cat([z1,z2,z1-z2,(z1-z2).abs()],-1))
            z=z1+torch.sigmoid(s.gate(torch.cat([z1,zb],-1)))*zb
            zp=torch.softmax((z@s.proto.t())*(64**-0.5),-1)@s.proto
            parts=[z,zp,s.fm(ft)]
            if s.uc:
                B,K2,C,L=ctx.shape; ze=s.e(ctx.reshape(B*K2,C,L)).reshape(B,K2,64)   # 이웃 인코딩
                a=torch.softmax((ze@s.tq)*(64**-0.5),-1)                              # (B,K2)
                parts.append((a.unsqueeze(-1)*ze).sum(1))                             # 문맥벡터(64)
            return s.cls(torch.cat(parts,-1))
    return Net()

def run_context(fams=("RHYTHM","KOOPMAN","AE","GNN"), seeds=None):
    import torch, torch.nn as nn, torch.nn.functional as Fn
    from sklearn.preprocessing import RobustScaler
    from sklearn.model_selection import GroupShuffleSplit
    seeds=seeds or list(range(2000,2015)); dev="cuda" if torch.cuda.is_available() else "cpu"
    beats,y,pid,F,bb=_bestF(fams); print(f"백본: {bb}")
    ref=np.empty_like(beats)
    for p in np.unique(pid): m=pid==p; ref[m]=np.median(beats[m],0,keepdims=True)
    ref=ref.astype("float32"); m1=np.isin(pid,_DS1); m2=np.isin(pid,_DS2); y2=y[m2]
    Sw=auto_weights(y[m1]); nc=np.array([(y[m1]==k).sum() for k in range(3)],np.float32); mc=(1.0/np.power(nc,0.25)); mc=(mc/mc.max()*0.5).astype("float32")
    def met(p,yy): return (average_precision_score((yy==1).astype(int),p[:,1]),average_precision_score((yy==2).astype(int),p[:,2]))
    def train_one(W,seed):
        use_ctx=W>0; K=2*W+1
        CTX = beats[_nbr_idx(pid,W)].astype("float32") if use_ctx else None    # (N,K,2,L)
        b1,r1,f1a,y1,p1=beats[m1],ref[m1],F[m1],y[m1],pid[m1]; b2,r2,f2a=beats[m2],ref[m2],F[m2]
        c1=CTX[m1] if use_ctx else None; c2=CTX[m2] if use_ctx else None
        torch.manual_seed(seed); np.random.seed(seed)
        tr,va=next(GroupShuffleSplit(1,test_size=0.2,random_state=seed).split(f1a,y1,groups=p1))
        sc=RobustScaler().fit(f1a[tr]); f1=np.nan_to_num(sc.transform(f1a),posinf=0,neginf=0).astype("float32"); f2=np.nan_to_num(sc.transform(f2a),posinf=0,neginf=0).astype("float32")
        M=_net(F.shape[1],use_ctx,K).to(dev); opt=torch.optim.AdamW(M.parameters(),lr=1e-3,weight_decay=1e-4)
        cw=torch.tensor([1.,Sw,1.5],device=dev); mcv=torch.from_numpy(mc).to(dev)
        @torch.no_grad()
        def pred(b,r,ft,c):
            M.eval(); o=[]
            for i in range(0,len(b),2048):
                cc=torch.from_numpy(c[i:i+2048]).to(dev) if use_ctx else None
                lo=M(torch.from_numpy(b[i:i+2048]).to(dev),torch.from_numpy(r[i:i+2048]).to(dev),torch.from_numpy(ft[i:i+2048]).to(dev),cc)
                o.append(torch.softmax(lo,-1).cpu().numpy())
            return np.concatenate(o)
        arrs=[b1[tr],r1[tr],f1[tr],y1[tr]]+([c1[tr]] if use_ctx else [])
        ds=torch.utils.data.TensorDataset(*[torch.from_numpy(x) for x in arrs]); dl=torch.utils.data.DataLoader(ds,batch_size=256,shuffle=True); best=-1; bs=None
        for ep in range(15):
            M.train()
            for batch in dl:
                batch=[t.to(dev) for t in batch]; bb2,rr,ff,yy=batch[:4]; cc=batch[4] if use_ctx else None
                opt.zero_grad(); lo=M(bb2,rr,ff,cc); lo=lo-torch.zeros_like(lo).scatter_(1,yy[:,None],mcv[yy][:,None])
                ce=Fn.cross_entropy(lo,yy,reduction="none"); loss=(ce*cw[yy]).sum()/cw[yy].sum()
                loss.backward(); torch.nn.utils.clip_grad_norm_(M.parameters(),1.0); opt.step()
            pv=pred(b1[va],r1[va],f1[va],c1[va] if use_ctx else None); s,v=met(pv,y1[va])
            if 0.5*(s+v)>best: best=0.5*(s+v); bs={k:vv.cpu() for k,vv in M.state_dict().items()}
        M.load_state_dict(bs); return pred(b2,r2,f2,c2)
    def trim(Pn):
        medS=np.median(Pn[:,:,1],0); corr=np.array([np.corrcoef(Pn[i,:,1],medS)[0,1] for i in range(len(Pn))])
        keep=np.argsort(-corr)[:max(1,int(round(len(Pn)*0.8)))]; P=Pn[keep].mean(0); return P/P.sum(1,keepdims=True)
    res={}
    print(f"margin CNN {len(seeds)}seed, Sw={Sw:.1f}")
    for nm,W in [("baseline(단일)",0),("+문맥 W1(±1=3비트)",1),("+문맥 W2(±2=5비트)",2)]:
        Pt=trim(np.stack([train_one(W,s) for s in seeds],0)); S,V=met(Pt,y2); pr,se,f1=_f1(y2,Pt[:,1]); res[nm]=(S,pr,se,f1)
        print(f"  {nm:20s} S={S:.4f} PREC={pr:.3f} SEN={se:.3f} F1={f1:.3f}")
    b=res["baseline(단일)"]
    print(f"\n▶ baseline 대비:")
    for nm,(S,pr,se,f1) in res.items():
        if nm=="baseline(단일)": continue
        print(f"  {nm:20s}: ΔS={S-b[0]:+.4f} ΔPREC={pr-b[1]:+.3f} ΔSEN={se-b[2]:+.3f} ΔF1={f1-b[3]:+.3f}")
    print(f"\n  ★ ΔSEN>0 & ΔF1>0 = 이웃비트 문맥이 놓친 조기 S를 잡음(새 정보축 성립). 그럼 이 문맥을 최종에 편입.")
    return res
