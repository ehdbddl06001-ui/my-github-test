# =============================================================================
#  colab_step66_patemb.py  —  [STEP 66] Patient Embedding (환자 분포 표현) — 개인화 축
#
#  static 중앙값 기준(_REF)을 넘어, 각 환자의 '비트 분포'를 학습된 벡터로 표현해 분류기에 추가.
#  각 환자 비트를 k-means(8)로 군집 → 8 대표형태(프로토타입) → 공유 인코더 → attention pool
#  → 환자 임베딩(64). 비지도(라벨 X, DS2도 자기 비트로) → inter-patient 깨끗(Setting A).
#  ※ 노이즈(±0.06) 때문에 DS2 단독 판정은 어려움 → 진짜 가치는 교차DB(INCART) 전이에서.
#  ※ 분산(평균±σ)·앙상블을 함께 보고 — 효과가 노이즈 위인지 확인.
#
#  선행: colab_prep_all.py
#  실행:
#    exec(open('/content/drive/MyDrive/mitbih/colab_step66_patemb.py').read())
#    run_patemb(fams=("RHYTHM","KOOPMAN","AE","GNN"))   # baseline vs +환자임베딩
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

def _patient_protos(beats, pid, k=8):
    """환자별 비트를 k-means → 군집평균 파형 8개(대표형태). 비지도. (P,k,2,L), 환자→행맵, 비트→행맵."""
    from sklearn.cluster import KMeans
    ups=np.unique(pid); L=beats.shape[2]; protos=np.zeros((len(ups),k,2,L),np.float32); row={}
    for i,p in enumerate(ups):
        idx=np.where(pid==p)[0]; b=beats[idx]; row[p]=i
        VM=np.sqrt(b[:,0]**2+b[:,1]**2); feat=VM[:,::10]                       # 군집용 다운샘플
        if len(idx)<k:
            for c in range(k): protos[i,c]=b[min(c,len(idx)-1)]
            continue
        km=KMeans(k,n_init=3,random_state=0).fit(np.nan_to_num(feat))
        for c in range(k):
            m=km.labels_==c; protos[i,c]=b[m].mean(0) if m.sum()>0 else b[0]
    prow=np.array([row[p] for p in pid],np.int64)                             # 각 비트→환자행
    return protos.astype("float32"), prow

def _net(fdim, use_pe=False, K=8):
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
            s.pe=use_pe; cin=192+(64 if use_pe else 0)
            if use_pe: s.pq=nn.Parameter(torch.randn(64)*0.1)                  # 환자 프로토 attention
            s.cls=nn.Sequential(nn.Linear(cin,64),nn.ReLU(),nn.Linear(64,3))
        def forward(s,b,r,ft,pe=None):
            z1=s.e(b); z2=s.e(r); zb=s.sia(torch.cat([z1,z2,z1-z2,(z1-z2).abs()],-1))
            z=z1+torch.sigmoid(s.gate(torch.cat([z1,zb],-1)))*zb
            zp=torch.softmax((z@s.proto.t())*(64**-0.5),-1)@s.proto
            parts=[z,zp,s.fm(ft)]
            if s.pe:
                B,K2,C,L=pe.shape; ze=s.e(pe.reshape(B*K2,C,L)).reshape(B,K2,64)   # 환자 프로토 인코딩
                a=torch.softmax((ze@s.pq)*(64**-0.5),-1); parts.append((a.unsqueeze(-1)*ze).sum(1))
            return s.cls(torch.cat(parts,-1))
    return Net()

def run_patemb(fams=("RHYTHM","KOOPMAN","AE","GNN"), seeds=None, k=8):
    import torch, torch.nn as nn, torch.nn.functional as Fn
    from sklearn.preprocessing import RobustScaler
    from sklearn.model_selection import GroupShuffleSplit
    _determinism(); seeds=list(seeds) if seeds is not None else list(range(2000,2012)); dev="cuda" if torch.cuda.is_available() else "cpu"
    beats,y,pid,F,bb=_bestF(fams); print(f"백본: {bb}  환자프로토 k={k}")
    ref=np.empty_like(beats)
    for p in np.unique(pid): m=pid==p; ref[m]=np.median(beats[m],0,keepdims=True)
    ref=ref.astype("float32"); m1=np.isin(pid,_DS1); m2=np.isin(pid,_DS2); y2=y[m2]
    print("환자 프로토타입(k-means) 계산..."); PROTO,prow=_patient_protos(beats,pid,k)
    Sw=auto_weights(y[m1]); nc=np.array([(y[m1]==k2).sum() for k2 in range(3)],np.float32); mc=(1.0/np.power(nc,0.25)); mc=(mc/mc.max()*0.5).astype("float32")
    def met(p,yy): return (average_precision_score((yy==1).astype(int),p[:,1]),average_precision_score((yy==2).astype(int),p[:,2]))
    def train_one(use_pe,seed):
        b1,r1,f1a,y1,p1,pr1=beats[m1],ref[m1],F[m1],y[m1],pid[m1],prow[m1]; b2,r2,f2a,pr2=beats[m2],ref[m2],F[m2],prow[m2]
        torch.manual_seed(seed); np.random.seed(seed)
        tr,va=next(GroupShuffleSplit(1,test_size=0.2,random_state=seed).split(f1a,y1,groups=p1))
        sc=RobustScaler().fit(f1a[tr]); f1=np.nan_to_num(sc.transform(f1a),posinf=0,neginf=0).astype("float32"); f2=np.nan_to_num(sc.transform(f2a),posinf=0,neginf=0).astype("float32")
        M=_net(F.shape[1],use_pe,k).to(dev); opt=torch.optim.AdamW(M.parameters(),lr=1e-3,weight_decay=1e-4)
        cw=torch.tensor([1.,Sw,1.5],device=dev); mcv=torch.from_numpy(mc).to(dev); PT=torch.from_numpy(PROTO).to(dev)
        @torch.no_grad()
        def pred(b,r,ft,prw):
            M.eval(); o=[]
            for i in range(0,len(b),2048):
                pe=PT[torch.from_numpy(prw[i:i+2048]).to(dev)] if use_pe else None
                lo=M(torch.from_numpy(b[i:i+2048]).to(dev),torch.from_numpy(r[i:i+2048]).to(dev),torch.from_numpy(ft[i:i+2048]).to(dev),pe)
                o.append(torch.softmax(lo,-1).cpu().numpy())
            return np.concatenate(o)
        ds=torch.utils.data.TensorDataset(*[torch.from_numpy(x) for x in (b1[tr],r1[tr],f1[tr],y1[tr],pr1[tr])])
        dl=torch.utils.data.DataLoader(ds,batch_size=512,shuffle=True); best=-1; bs=None
        for ep in range(15):
            M.train()
            for bb2,rr,ff,yy,pw in dl:
                bb2,rr,ff,yy=(t.to(dev) for t in (bb2,rr,ff,yy)); pe=PT[pw.to(dev)] if use_pe else None
                opt.zero_grad(); lo=M(bb2,rr,ff,pe); lo=lo-torch.zeros_like(lo).scatter_(1,yy[:,None],mcv[yy][:,None])
                ce=Fn.cross_entropy(lo,yy,reduction="none"); loss=(ce*cw[yy]).sum()/cw[yy].sum()
                loss.backward(); torch.nn.utils.clip_grad_norm_(M.parameters(),1.0); opt.step()
            pv=pred(b1[va],r1[va],f1[va],pr1[va]); s,v=met(pv,y1[va])
            if 0.5*(s+v)>best: best=0.5*(s+v); bs={kk:vv.cpu() for kk,vv in M.state_dict().items()}
        M.load_state_dict(bs); return pred(b2,r2,f2,pr2)
    def trim(Pn):
        medS=np.median(Pn[:,:,1],0); corr=np.array([np.corrcoef(Pn[i,:,1],medS)[0,1] for i in range(len(Pn))])
        keep=np.argsort(-corr)[:max(1,int(round(len(Pn)*0.8)))]; P=Pn[keep].mean(0); return P/P.sum(1,keepdims=True)
    def sm(p): S=average_precision_score((y2==1).astype(int),p[:,1]); pr,se,f1=_f1(y2,p[:,1]); return S,pr,se,f1
    print(f"결정성 ON  {len(seeds)}seed  Sw={Sw:.2f}")
    res={}
    for nm,upe in [("baseline",False),("+환자임베딩",True)]:
        P=np.stack([train_one(upe,s) for s in seeds],0); per=np.array([sm(p) for p in P])
        S,pr,se,f1=sm(trim(P)); res[nm]=(per,(S,pr,se,f1))
        print(f"\n=== {nm} ===")
        for i,l in enumerate(["S_PR","PREC","SEN","F1"]):
            v=per[:,i]; print(f"  {l:5s}: 평균 {v.mean():.4f} ± {v.std():.4f}")
        print(f"  트림앙상블: S_PR={S:.4f} PREC={pr:.3f} SEN={se:.3f} F1={f1:.3f}")
    pb=res["baseline"][0][:,3]; pe=res["+환자임베딩"][0][:,3]
    print(f"\n▶ F1 개별평균: baseline {pb.mean():.4f} → +환자 {pe.mean():.4f} (Δ{pe.mean()-pb.mean():+.4f}, σ~{pb.std():.3f})")
    print(f"  트림앙상블 F1: {res['baseline'][1][3]:.4f} → {res['+환자임베딩'][1][3]:.4f}")
    print(f"  ★ Δ가 σ보다 크면 진짜 효과. 노이즈 안이면 = DS2로는 판정불가 → 교차DB에서 확인해야.")
    return res
