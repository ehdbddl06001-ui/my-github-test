# =============================================================================
#  colab_step59_asl.py  —  [STEP 59] ASL(비대칭 초점 손실) — SEN 병목 정통 해법
#
#  SEN이 낮은 건 놓친 subtle S 때문. ASL(Asymmetric Loss, Ridnik 2021)의 다중클래스 적응:
#  '쉬운 다수(N/V) 음성은 초점을 낮추고(γ_neg 큼), 소수 S 양성은 항상 기여(γ_pos 작음)'
#  → 모델 용량을 놓친 S에 집중 → 민감도 회복 기대. LDAM 대체/병용 비교.
#  손실만 교체(백본·특징 동일) → Mamba 전에 손쉬운 개선.
#
#  손실 = -w_c · (1-p_c)^γ · log p_c  (γ = c==S? γ_pos : γ_neg)  (+옵션 LDAM margin)
#  선행: colab_prep_all.py
#  실행:
#    exec(open('/content/drive/MyDrive/mitbih/colab_step59_asl.py').read())
#    run_asl(fams=("RHYTHM","KOOPMAN","GNN"))        # 균형형
#    run_asl(fams=("RHYTHM","KOOPMAN","AE","GNN"))   # 4가지(정밀형) — SEN 여지 최대
# =============================================================================
import os
import numpy as np
from sklearn.metrics import average_precision_score, precision_recall_curve

_BASE="/content/drive/MyDrive/mitbih"; _FEATDIR=f"{_BASE}/synergy_feats"
_DS1=[101,106,108,109,112,114,115,116,118,119,122,124,201,203,205,207,208,209,215,220,223,230]
_DS2=[100,103,105,111,113,117,121,123,200,202,210,212,213,214,219,221,222,228,231,232,233,234]
# 손실 구성: (이름, γ_pos(S), γ_neg(N/V), LDAM margin 병용)
_CFGS=[("LDAM(base)",None,None,True),
       ("AFL(0,2)",0.0,2.0,False),
       ("AFL(1,3)",1.0,3.0,False),
       ("LDAM+AFL(0,2)",0.0,2.0,True)]

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

def run_asl(fams=("RHYTHM","KOOPMAN","GNN"), seeds=None):
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
    @torch.no_grad()
    def pred(M,b,r,ft):
        M.eval(); o=[]
        for i in range(0,len(b),4096):
            o.append(torch.softmax(M(torch.from_numpy(b[i:i+4096]).to(dev),torch.from_numpy(r[i:i+4096]).to(dev),torch.from_numpy(ft[i:i+4096]).to(dev)),-1).cpu().numpy())
        return np.concatenate(o)
    def train_one(cfg,seed):
        _,gpos,gneg,ldam=cfg
        b1,r1,f1a,y1,p1=beats[m1],ref[m1],F[m1],y[m1],pid[m1]; b2,r2,f2a=beats[m2],ref[m2],F[m2]
        torch.manual_seed(seed); np.random.seed(seed)
        tr,va=next(GroupShuffleSplit(1,test_size=0.2,random_state=seed).split(f1a,y1,groups=p1))
        sc=RobustScaler().fit(f1a[tr]); f1=np.nan_to_num(sc.transform(f1a),posinf=0,neginf=0).astype("float32"); f2=np.nan_to_num(sc.transform(f2a),posinf=0,neginf=0).astype("float32")
        M=_net(F.shape[1]).to(dev); opt=torch.optim.AdamW(M.parameters(),lr=1e-3,weight_decay=1e-4)
        cw=torch.tensor([1.,Sw,1.5],device=dev); mcv=torch.from_numpy(mc).to(dev)
        ds=torch.utils.data.TensorDataset(*[torch.from_numpy(x) for x in (b1[tr],r1[tr],f1[tr],y1[tr])]); dl=torch.utils.data.DataLoader(ds,batch_size=512,shuffle=True); best=-1; bs=None
        for ep in range(15):
            M.train()
            for bb2,rr,ff,yy in dl:
                bb2,rr,ff,yy=(t.to(dev) for t in (bb2,rr,ff,yy)); opt.zero_grad()
                lo=M(bb2,rr,ff)
                if ldam: lo=lo-torch.zeros_like(lo).scatter_(1,yy[:,None],mcv[yy][:,None])
                logp=Fn.log_softmax(lo,-1); logpt=logp.gather(1,yy[:,None]).squeeze(1); pt=logpt.exp()
                if gpos is None:                                     # 순수 가중 CE(LDAM base)
                    focal=1.0
                else:                                                # 비대칭 초점: S=γpos, N/V=γneg
                    g=torch.where(yy==1, torch.tensor(gpos,device=dev), torch.tensor(gneg,device=dev))
                    focal=(1-pt).clamp(min=1e-6)**g
                w=cw[yy]; loss=-(w*focal*logpt).sum()/w.sum()
                loss.backward(); torch.nn.utils.clip_grad_norm_(M.parameters(),1.0); opt.step()
            pv=pred(M,b1[va],r1[va],f1[va]); s,v=met(pv,y1[va])
            if 0.5*(s+v)>best: best=0.5*(s+v); bs={k:vv.cpu() for k,vv in M.state_dict().items()}
        M.load_state_dict(bs); return pred(M,b2,r2,f2)
    def trim(Pn):
        medS=np.median(Pn[:,:,1],0); corr=np.array([np.corrcoef(Pn[i,:,1],medS)[0,1] for i in range(len(Pn))])
        keep=np.argsort(-corr)[:max(1,int(round(len(Pn)*0.8)))]; P=Pn[keep].mean(0); return P/P.sum(1,keepdims=True)
    res={}
    print(f"margin CNN 15seed, Sw={Sw:.1f}")
    for cfg in _CFGS:
        Pt=trim(np.stack([train_one(cfg,s) for s in seeds],0)); S,V=met(Pt,y2); pr,se,f1=_f1(y2,Pt[:,1]); res[cfg[0]]=(S,pr,se,f1)
        print(f"  {cfg[0]:16s} S={S:.4f} PREC={pr:.3f} SEN={se:.3f} F1={f1:.3f}")
    b=res["LDAM(base)"]
    print(f"\n▶ LDAM(base) 대비:")
    for nm,(S,pr,se,f1) in res.items():
        if nm=="LDAM(base)": continue
        print(f"  {nm:16s}: ΔS={S-b[0]:+.4f} ΔPREC={pr-b[1]:+.3f} ΔSEN={se-b[2]:+.3f} ΔF1={f1-b[3]:+.3f}")
    print(f"\n  ★ ΔSEN>0 & ΔF1>0 = 비대칭 초점이 놓친 S를 잡아 민감도·F1 동시 개선(ASL 성립).")
    return res
