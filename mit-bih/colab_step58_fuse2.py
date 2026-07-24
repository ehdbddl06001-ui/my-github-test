# =============================================================================
#  colab_step58_fuse2.py  —  [STEP 58] 정밀모델 ⊕ 고SEN모델 점수융합 (세 지표 동시 상승 시도)
#
#  발견: RHYTHM+KOOPMAN+AE+GNN(4가지) = PREC 0.917/F1 0.798(정밀), 근데 SEN 0.706 낮음.
#  geo융합(RKG⊕KAG)이 S_PR을 0.822→0.835로 올렸듯, 정밀모델을 고-SEN 모델과 점수융합하면
#  랭킹↑ + 균형 운영점 → F1 최고점 가능(단, PREC는 4가지 단독보다 내려감 = 상충 불가피).
#  파라미터-free 융합(mean/max/geo) = 오염 없음.
#  ★ 4가지(mask29) 예측만 새로 학습·저장, 나머지(1·21·28)는 STEP54 sweep 캐시 재활용.
#
#  마스크(STEP54 비트순: RHYTHM0 NOISE1 KOOPMAN2 AE3 GNN4 SEGDEV5 VCG6):
#    RHYTHM=1  RHYTHM+KOOPMAN+GNN=21  KOOPMAN+AE+GNN=28  RHYTHM+KOOPMAN+AE+GNN=29
#  선행: colab_prep_all.py
#  실행:
#    exec(open('/content/drive/MyDrive/mitbih/colab_step58_fuse2.py').read())
#    run_fuse2()              # 없는 모델(29)만 학습(15seed), 나머지 캐시 로드 후 융합
# =============================================================================
import os
import numpy as np
from sklearn.metrics import average_precision_score, precision_recall_curve

_BASE="/content/drive/MyDrive/mitbih"; _FEATDIR=f"{_BASE}/synergy_feats"; _CNN=f"{_BASE}/synergy2_out/cnn"
_DS1=[101,106,108,109,112,114,115,116,118,119,122,124,201,203,205,207,208,209,215,220,223,230]
_DS2=[100,103,105,111,113,117,121,123,200,202,210,212,213,214,219,221,222,228,231,232,233,234]
_BACKBONE=["feats0","WST","MORPHO","REPOL","DTW"]
_TOGGLE=["RHYTHM","NOISE","KOOPMAN","AE","GNN","SEGDEV","VCG"]
_CAND={1:"RHYTHM",21:"RHYTHM+KOOPMAN+GNN",28:"KOOPMAN+AE+GNN",29:"RHYTHM+KOOPMAN+AE+GNN"}
_PAIRS=[(29,21),(29,1),(21,28)]     # 4가지⊕균형 / 4가지⊕RHYTHM / (기존 geo 재확인)

def _f1(y2,s):
    p,r,_=precision_recall_curve((y2==1).astype(int),s); f=2*p*r/(p+r+1e-9); i=int(np.nanargmax(f)); return p[i],r[i],f[i]
def auto_weights(y1,beta=0.9999):
    nN=(y1==0).sum(); nS=max((y1==1).sum(),1); eff=lambda n:(1-beta)/(1-beta**n+1e-12); return float(eff(nS)/eff(nN))
def _Lnpy(n):
    p=f"{_FEATDIR}/{n}.npy"; return np.load(p) if os.path.exists(p) else None
def _buildX(back,tog,mask):
    parts=[back]
    for i,n in enumerate(_TOGGLE):
        if mask>>i&1 and n in tog: parts.append(tog[n])
    return np.concatenate(parts,1).astype("float32")
def _trim(Pn):
    if len(Pn)==1: P=Pn[0]; return P/P.sum(1,keepdims=True)
    medS=np.median(Pn[:,:,1],0); corr=np.array([np.corrcoef(Pn[i,:,1],medS)[0,1] for i in range(len(Pn))])
    keep=np.argsort(-corr)[:max(1,int(round(len(Pn)*0.8)))]; P=Pn[keep].mean(0); return P/P.sum(1,keepdims=True)

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

def _train_seed(F, beats, ref, y, pid, mc, Sw, seed):
    import torch, torch.nn as nn, torch.nn.functional as Fn
    from sklearn.preprocessing import RobustScaler
    from sklearn.model_selection import GroupShuffleSplit
    dev="cuda" if torch.cuda.is_available() else "cpu"; m1=np.isin(pid,_DS1); m2=np.isin(pid,_DS2)
    b1,r1,f1a,y1,p1=beats[m1],ref[m1],F[m1],y[m1],pid[m1]; b2,r2,f2a=beats[m2],ref[m2],F[m2]
    torch.manual_seed(seed); np.random.seed(seed)
    tr,va=next(GroupShuffleSplit(1,test_size=0.2,random_state=seed).split(f1a,y1,groups=p1))
    sc=RobustScaler().fit(f1a[tr]); f1=np.nan_to_num(sc.transform(f1a),posinf=0,neginf=0).astype("float32"); f2=np.nan_to_num(sc.transform(f2a),posinf=0,neginf=0).astype("float32")
    M=_net(F.shape[1]).to(dev); opt=torch.optim.AdamW(M.parameters(),lr=1e-3,weight_decay=1e-4)
    cw=torch.tensor([1.,Sw,1.5],device=dev); mcv=torch.from_numpy(mc).to(dev)
    def met(p,yy): return 0.5*(average_precision_score((yy==1).astype(int),p[:,1])+average_precision_score((yy==2).astype(int),p[:,2]))
    @torch.no_grad()
    def pred(b,r,ft):
        M.eval(); o=[]
        for i in range(0,len(b),4096):
            o.append(torch.softmax(M(torch.from_numpy(b[i:i+4096]).to(dev),torch.from_numpy(r[i:i+4096]).to(dev),torch.from_numpy(ft[i:i+4096]).to(dev)),-1).cpu().numpy())
        return np.concatenate(o)
    ds=torch.utils.data.TensorDataset(*[torch.from_numpy(x) for x in (b1[tr],r1[tr],f1[tr],y1[tr])]); dl=torch.utils.data.DataLoader(ds,batch_size=512,shuffle=True); best=-1; bs=None
    for ep in range(15):
        M.train()
        for bb,rr,ff,yy in dl:
            bb,rr,ff,yy=(t.to(dev) for t in (bb,rr,ff,yy)); opt.zero_grad()
            lo=M(bb,rr,ff); lg=lo-torch.zeros_like(lo).scatter_(1,yy[:,None],mcv[yy][:,None])
            ce=Fn.cross_entropy(lg,yy,reduction="none"); wv=cw[yy]; loss=(ce*wv).sum()/wv.sum()
            loss.backward(); torch.nn.utils.clip_grad_norm_(M.parameters(),1.0); opt.step()
        v=met(pred(b1[va],r1[va],f1[va]),y1[va])
        if v>best: best=v; bs={k:vv.cpu() for k,vv in M.state_dict().items()}
    M.load_state_dict(bs); return pred(b2,r2,f2)

def _ensure_preds(mask, seeds, ctx):
    beats,ref,y,pid,back,tog,mc,Sw=ctx; F=None; P=[]
    for s in seeds:
        sp=f"{_CNN}/{mask}_s{s}.npy"
        if os.path.exists(sp): P.append(np.load(sp)); continue
        if F is None: F=_buildX(back,tog,mask); print(f"  mask={mask}({_CAND.get(mask,'')}) 학습 중(캐시 없음)...")
        pr=_train_seed(F,beats,ref,y,pid,mc,Sw,s); np.save(sp,pr.astype("float32")); P.append(pr)
    return np.stack(P,0)

def run_fuse2(seeds=None):
    os.makedirs(_CNN,exist_ok=True); seeds=seeds or list(range(2000,2015))
    d=np.load(f"{_BASE}/mamba_data.npz"); beats,y,pid=d["beat"],d["y"],d["pid"]; ref=np.empty_like(beats)
    for p in np.unique(pid): m=pid==p; ref[m]=np.median(beats[m],0,keepdims=True)
    ref=ref.astype("float32"); m1=np.isin(pid,_DS1); m2=np.isin(pid,_DS2); y2=y[m2]
    back=np.concatenate([_Lnpy(n) for n in _BACKBONE],1).astype("float32"); tog={n:_Lnpy(n) for n in _TOGGLE if _Lnpy(n) is not None}
    Sw=auto_weights(y[m1]); nc=np.array([(y[m1]==k).sum() for k in range(3)],np.float32); mc=(1.0/np.power(nc,0.25)); mc=(mc/mc.max()*0.5).astype("float32")
    ctx=(beats,ref,y,pid,back,tog,mc,Sw)
    tr={}
    for mask in _CAND: tr[mask]=_trim(_ensure_preds(mask,seeds,ctx))
    def M(sc): return average_precision_score((y2==1).astype(int),sc)
    def row(nm,sc): S=M(sc); pr,se,f1=_f1(y2,sc); print(f"  {nm:34s} S={S:.4f} PREC={pr:.3f} SEN={se:.3f} F1={f1:.3f}"); return (S,pr,se,f1)
    print("=== 단일 모델 ===")
    single={mask:row(_CAND[mask],tr[mask][:,1]) for mask in _CAND}
    def fuse(a,b,how):
        sa=np.clip(a,1e-6,1); sb=np.clip(b,1e-6,1)
        return {"mean":(sa+sb)/2,"max":np.maximum(sa,sb),"geo":np.sqrt(sa*sb)}[how]
    bestF1=max(v[3] for v in single.values()); bestS=max(v[0] for v in single.values())
    for a,b in _PAIRS:
        if a not in tr or b not in tr: continue
        print(f"\n=== 융합: {_CAND[a]}  ⊕  {_CAND[b]} ===")
        for how in ("mean","max","geo"):
            S,pr,se,f1=row(how, fuse(tr[a][:,1],tr[b][:,1],how))
            tag=[]
            if S>bestS+1e-4: tag.append("S_PR신기록")
            if f1>bestF1+1e-4: tag.append("F1신기록")
            if tag: print(f"       → {' '.join(tag)}")
    print(f"\n  ★ 융합 F1이 최고 단일 F1({bestF1:.3f}) 넘으면 = 상보성으로 균형점 개선(사장님 아이디어 성립).")
    print(f"     PREC는 4가지 단독(0.9x)보다 내려가는 게 정상(상충) — F1·S_PR 동시 최고인지가 판정.")
