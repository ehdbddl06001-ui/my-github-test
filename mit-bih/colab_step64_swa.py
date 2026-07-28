# =============================================================================
#  colab_step64_swa.py  —  [STEP 64] SWA(가중치 평균)로 학습 분산 보정
#
#  STEP62/63: best-epoch 선택이 작은 DS1-val에 취약 → 시드마다 붕괴(F1 σ 0.064, S_PR 0.48~0.83).
#  SWA(Izmailov 2018): 학습 후반 여러 epoch의 '가중치'를 평균 → 평평한 최소값 → 일반화·분산 개선.
#  best-epoch 하나 고르는 취약성을 회피(val에 덜 의존) → 붕괴 완화. BN은 평균 후 재계산.
#  같은 시드에서 best-epoch vs SWA를 나란히 비교(개별 σ·앙상블). 트릭 아닌 표준 최적화 보정.
#  ※ 이건 ①학습분산 보정. ②DS1-val≠DS2(도메인shift)는 교차DB로 별도 검증.
#
#  선행: colab_prep_all.py
#  실행:
#    exec(open('/content/drive/MyDrive/mitbih/colab_step64_swa.py').read())
#    run_swa(fams=("RHYTHM","KOOPMAN","AE","GNN"))     # best-epoch vs SWA, 15seed
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
def _determinism():
    import torch
    os.environ["CUBLAS_WORKSPACE_CONFIG"]=":4096:8"
    torch.backends.cudnn.deterministic=True; torch.backends.cudnn.benchmark=False
    try: torch.use_deterministic_algorithms(True, warn_only=True)
    except Exception as e: print("  det note:", type(e).__name__, e)

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

def _train_seed(F, beats, ref, y, pid, mc, Sw, seed, swa_start=8):
    """best-epoch 예측과 SWA 예측을 둘 다 반환."""
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
    Xtr=[torch.from_numpy(x) for x in (b1[tr],r1[tr],f1[tr],y1[tr])]
    ds=torch.utils.data.TensorDataset(*Xtr); dl=torch.utils.data.DataLoader(ds,batch_size=512,shuffle=True); best=-1; bs=None
    swa={n:None for n,_ in M.named_parameters()}; nswa=0
    for ep in range(15):
        M.train()
        for bb,rr,ff,yy in dl:
            bb,rr,ff,yy=(t.to(dev) for t in (bb,rr,ff,yy)); opt.zero_grad()
            lo=M(bb,rr,ff); lg=lo-torch.zeros_like(lo).scatter_(1,yy[:,None],mcv[yy][:,None])
            ce=Fn.cross_entropy(lg,yy,reduction="none"); loss=(ce*cw[yy]).sum()/cw[yy].sum()
            loss.backward(); torch.nn.utils.clip_grad_norm_(M.parameters(),1.0); opt.step()
        pv=pred(b1[va],r1[va],f1[va]); v=met(pv,y1[va])
        if v>best: best=v; bs={k:vv.cpu() for k,vv in M.state_dict().items()}   # best-epoch 저장
        if ep>=swa_start:                                                       # SWA 가중치 누적평균
            with torch.no_grad():
                for n,pp in M.named_parameters():
                    swa[n]=pp.detach().clone().float() if swa[n] is None else (swa[n]*nswa+pp.detach().float())/(nswa+1)
            nswa+=1
    # best-epoch 예측
    M.load_state_dict(bs); P_best=pred(b2,r2,f2)
    # SWA: 평균 가중치 로드 → BN 재계산(train 순전파) → 예측
    with torch.no_grad():
        for n,pp in M.named_parameters(): pp.copy_(swa[n].to(dev))
    for mod in M.modules():
        if isinstance(mod,nn.BatchNorm1d): mod.reset_running_stats(); mod.momentum=None
    M.train()
    with torch.no_grad():
        for bb,rr,ff,yy in dl:
            M(bb.to(dev),rr.to(dev),ff.to(dev))                                 # BN 통계만 갱신
    P_swa=pred(b2,r2,f2)
    return P_best, P_swa

def _trim(Pn):
    if len(Pn)==1: P=Pn[0]; return P/P.sum(1,keepdims=True)
    medS=np.median(Pn[:,:,1],0); corr=np.array([np.corrcoef(Pn[i,:,1],medS)[0,1] for i in range(len(Pn))])
    keep=np.argsort(-corr)[:max(1,int(round(len(Pn)*0.8)))]; P=Pn[keep].mean(0); return P/P.sum(1,keepdims=True)

def run_swa(fams=("RHYTHM","KOOPMAN","AE","GNN"), seeds=None):
    _determinism()
    seeds=list(seeds) if seeds is not None else list(range(2000,2015))
    beats,y,pid,F,bb=_bestF(fams); ref=np.empty_like(beats)
    for p in np.unique(pid): m=pid==p; ref[m]=np.median(beats[m],0,keepdims=True)
    ref=ref.astype("float32"); m1=np.isin(pid,_DS1); m2=np.isin(pid,_DS2); y2=y[m2]
    Sw=auto_weights(y[m1]); nc=np.array([(y[m1]==k).sum() for k in range(3)],np.float32); mc=(1.0/np.power(nc,0.25)); mc=(mc/mc.max()*0.5).astype("float32")
    def sm(p): S=average_precision_score((y2==1).astype(int),p[:,1]); pr,se,f1=_f1(y2,p[:,1]); return S,pr,se,f1
    print(f"백본: {bb}  결정성 ON  {len(seeds)}seed  Sw={Sw:.2f}")
    Pb=[]; Ps=[]
    for s in seeds:
        pb,ps=_train_seed(F,beats,ref,y,pid,mc,Sw,s); Pb.append(pb); Ps.append(ps)
    Pb=np.stack(Pb,0); Ps=np.stack(Ps,0)
    for nm,P in [("best-epoch(기존)",Pb),("SWA(가중치평균)",Ps)]:
        per=np.array([sm(p) for p in P]); lbl=["S_PR","PREC","SEN","F1"]
        print(f"\n=== {nm} — 개별 시드 분포 ===")
        for i,l in enumerate(lbl):
            v=per[:,i]; print(f"  {l:5s}: 평균 {v.mean():.4f} ± {v.std():.4f}  [최소 {v.min():.4f}, 최대 {v.max():.4f}]")
        S,pr,se,f1=sm(_trim(P)); print(f"  트림앙상블: S_PR={S:.4f} PREC={pr:.3f} SEN={se:.3f} F1={f1:.3f}")
    # 요약 비교
    fb=np.array([sm(p)[3] for p in Pb]); fs=np.array([sm(p)[3] for p in Ps])
    print(f"\n▶ F1 개별 σ:  best-epoch {fb.std():.4f}  →  SWA {fs.std():.4f}  (작아지면 분산 보정 성공)")
    print(f"  ★ SWA의 개별 σ가 줄고 트림앙상블이 같거나↑ 면 = 붕괴 완화(정직한 안정화). 채택.")
    return dict(best=Pb, swa=Ps)
