# =============================================================================
#  colab_step62_stable.py  —  [STEP 62] 비결정성 통제 + 분산 정식보고 (신뢰 천장 확정)
#
#  문제: 같은 설정·같은 시드인데 실행마다 PREC 0.85↔0.92, F1 0.80↔0.81 흔들림(GPU cudnn
#  비결정성). 우리가 쫓던 트릭 효과(±0.01~0.03)가 이 노이즈(±0.03~0.07)보다 작아 측정 불가.
#  → (a) 결정성 플래그로 재현성 확보 (b) 앙상블 + 다시드로 '평균±표준편차' 정식 보고.
#  이걸로 '4-family의 진짜 성적 = X ± σ'를 못박고, 이후 metric learning 등의 효과를
#  이 오차막대 위에서만 판정한다(노이즈 쫓기 방지).
#
#  선행: colab_prep_all.py
#  실행:
#    exec(open('/content/drive/MyDrive/mitbih/colab_step62_stable.py').read())
#    run_stable(fams=("RHYTHM","KOOPMAN","AE","GNN"))     # 20seed 결정성 + 분산
# =============================================================================
import os
import numpy as np
from sklearn.metrics import average_precision_score, precision_recall_curve

_BASE="/content/drive/MyDrive/mitbih"; _FEATDIR=f"{_BASE}/synergy_feats"; _OUT=f"{_BASE}/stable_out"
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
    """GPU 비결정성 최대한 제거 → 같은 시드=같은 결과(재현성)."""
    import torch
    os.environ["CUBLAS_WORKSPACE_CONFIG"]=":4096:8"
    torch.backends.cudnn.deterministic=True; torch.backends.cudnn.benchmark=False
    try: torch.use_deterministic_algorithms(True, warn_only=True)      # 일부 op은 경고만(크래시 방지)
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
            ce=Fn.cross_entropy(lg,yy,reduction="none"); loss=(ce*cw[yy]).sum()/cw[yy].sum()
            loss.backward(); torch.nn.utils.clip_grad_norm_(M.parameters(),1.0); opt.step()
        v=met(pred(b1[va],r1[va],f1[va]),y1[va])
        if v>best: best=v; bs={k:vv.cpu() for k,vv in M.state_dict().items()}
    M.load_state_dict(bs); return pred(b2,r2,f2)

def _trim(Pn):
    if len(Pn)==1: P=Pn[0]; return P/P.sum(1,keepdims=True)
    medS=np.median(Pn[:,:,1],0); corr=np.array([np.corrcoef(Pn[i,:,1],medS)[0,1] for i in range(len(Pn))])
    keep=np.argsort(-corr)[:max(1,int(round(len(Pn)*0.8)))]; P=Pn[keep].mean(0); return P/P.sum(1,keepdims=True)

def run_stable(fams=("RHYTHM","KOOPMAN","AE","GNN"), seeds=None):
    _determinism(); os.makedirs(_OUT,exist_ok=True)
    seeds=list(seeds) if seeds is not None else list(range(2000,2020))
    beats,y,pid,F,bb=_bestF(fams); ref=np.empty_like(beats)
    for p in np.unique(pid): m=pid==p; ref[m]=np.median(beats[m],0,keepdims=True)
    ref=ref.astype("float32"); m1=np.isin(pid,_DS1); m2=np.isin(pid,_DS2); y2=y[m2]
    Sw=auto_weights(y[m1]); nc=np.array([(y[m1]==k).sum() for k in range(3)],np.float32); mc=(1.0/np.power(nc,0.25)); mc=(mc/mc.max()*0.5).astype("float32")
    tag=bb.replace("+","_")
    def sm(p): S=average_precision_score((y2==1).astype(int),p[:,1]); pr,se,f1=_f1(y2,p[:,1]); return S,pr,se,f1
    print(f"백본: {bb}  결정성 ON  {len(seeds)}seed  Sw={Sw:.2f}")
    Ps=[]
    for s in seeds:
        sp=f"{_OUT}/{tag}_s{s}.npy"
        if os.path.exists(sp): P=np.load(sp)
        else: P=_train_seed(F,beats,ref,y,pid,mc,Sw,s); np.save(sp,P.astype("float32"))
        Ps.append(P)
    Ps=np.stack(Ps,0)
    # 1) 개별 시드 분포(단일모델 변동)
    per=np.array([sm(P) for P in Ps])   # (K,4) S,PREC,SEN,F1
    lbl=["S_PR","PREC","SEN","F1"]
    print(f"\n=== 개별 시드 분포 ({len(seeds)}개) ===")
    for i,l in enumerate(lbl):
        v=per[:,i]; print(f"  {l:5s}: 평균 {v.mean():.4f} ± {v.std():.4f}  [최소 {v.min():.4f}, 최대 {v.max():.4f}]")
    # 2) 트림 앙상블 점추정(전체)
    S,pr,se,f1=sm(_trim(Ps))
    print(f"\n=== 트림 앙상블(전체 {len(seeds)}) 점추정 ===")
    print(f"  S_PR={S:.4f}  PREC={pr:.3f}  SEN={se:.3f}  F1={f1:.3f}")
    # 3) 앙상블 수준 안정성: 시드 반반 나눠 각각 앙상블
    h=len(seeds)//2
    for nm,sub in [("전반부",Ps[:h]),("후반부",Ps[h:])]:
        Sa,pa,sa,fa=sm(_trim(sub)); print(f"  [{nm} {h}seed 앙상블] S_PR={Sa:.4f} PREC={pa:.3f} SEN={sa:.3f} F1={fa:.3f}")
    print(f"\n  ★ '개별 σ'가 트릭 효과(±0.01~0.03)보다 크면 = 그 트릭은 노이즈. 앙상블 반반이 가까우면 앙상블은 안정.")
    print(f"     논문 보고: '{lbl[3]} = {per[:,3].mean():.3f} ± {per[:,3].std():.3f} (n={len(seeds)}), 트림앙상블 {f1:.3f}'.")
    return dict(per=per, ensemble=(S,pr,se,f1))
