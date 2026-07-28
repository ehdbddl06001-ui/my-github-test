# =============================================================================
#  colab_step56_atrial.py  —  [STEP 56] QRST 소거 → 심방(P) 잔차 (subtle S 직공)
#
#  SVEB 정의 = 이소성 심방활동(이상 P'). QRS는 N과 공유 → QRS를 소거하면 심방활동만 남음.
#  고전 기법(AF의 QRST cancellation)의 개인화판: 환자 평균비트(=평균 QRST+P)를 QRS에 맞춰
#  스케일 후 각 비트에서 빼면 → 잔차 = 이 비트 심방활동의 '정상 대비 편차'. 타이밍이 정상인
#  subtle S도 이상 P'가 잔차에 드러남 → 민감도 회복 후보(정밀도 유지).
#  전부 환자별 비지도(라벨X) → inter-patient 깨끗.
#
#  선행: colab_prep_all.py (백본+RHYTHM+KOOPMAN+GNN 캐시)
#  실행:
#    exec(open('/content/drive/MyDrive/mitbih/colab_step56_atrial.py').read())
#    diag_atrial()            # 단일AUC(DS1/DS2) — 빠름
#    run_atrial_cnn()         # best(RHYTHM+KOOPMAN+GNN) vs +심방잔차 (margin CNN 15seed)
# =============================================================================
import os
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score, precision_recall_curve, roc_auc_score

_BASE="/content/drive/MyDrive/mitbih"; _FEATDIR=f"{_BASE}/synergy_feats"
_DS1=[101,106,108,109,112,114,115,116,118,119,122,124,201,203,205,207,208,209,215,220,223,230]
_DS2=[100,103,105,111,113,117,121,123,200,202,210,212,213,214,219,221,222,228,231,232,233,234]
ATR_NAMES=["P잔차E","PR잔차E","P잔차최대","P축편차","비QRS잔차","P잔차집중"]

def _f1(y2,s):
    p,r,_=precision_recall_curve((y2==1).astype(int),s); f=2*p*r/(p+r+1e-9); i=int(np.nanargmax(f)); return p[i],r[i],f[i]
def auto_weights(y1,beta=0.9999):
    nN=(y1==0).sum(); nS=max((y1==1).sum(),1); eff=lambda n:(1-beta)/(1-beta**n+1e-12); return float(eff(nS)/eff(nN))
def _Lnpy(n):
    p=f"{_FEATDIR}/{n}.npy"; return np.load(p) if os.path.exists(p) else None

def extract_atrial_features(beats, pid, y=None):
    N=len(beats); L=beats.shape[2]; F=np.zeros((N,6),np.float32); eps=1e-6
    for p in np.unique(pid):
        idx=np.where(pid==p)[0]; b=beats[idx].astype(np.float64)      # (n,2,L)
        T=np.median(b,0)                                              # (2,L) 평균 QRST+P 템플릿
        VMt=np.sqrt(T[0]**2+T[1]**2); R=int(np.argmax(VMt))
        q0,q1=max(0,R-18),min(L,R+18); Ps,Pe=max(0,R-90),max(3,R-25); Rs,Re=max(0,R-25),max(5,R-5)
        # 리드별 QRS에 템플릿 스케일 맞춤 후 소거 → 심방 잔차
        res=np.empty_like(b)
        for l in range(2):
            s=(b[:,l,q0:q1]*T[l,q0:q1]).sum(1)/((T[l,q0:q1]**2).sum()+eps)   # (n,) QRS 매칭 스케일
            res[:,l]=b[:,l]-s[:,None]*T[l]
        rVM=np.sqrt(res[:,0]**2+res[:,1]**2)                         # (n,L) 잔차 벡터크기
        qE=np.sqrt(b[:,0,q0:q1]**2+b[:,1,q0:q1]**2).sum(1)+eps       # QRS 에너지(정규화)
        F[idx,0]=rVM[:,Ps:Pe].sum(1)/qE                             # P구간 잔차E (이상 P')
        F[idx,1]=rVM[:,Rs:Re].sum(1)/qE                             # PR구간 잔차E
        F[idx,2]=rVM[:,Ps:Pe].max(1)/qE                             # P 잔차 최대
        # P축(심방벡터) 편차: 잔차의 리드간 방향
        aP=np.arctan2(res[:,1,Ps:Pe].sum(1),res[:,0,Ps:Pe].sum(1))
        aT=np.arctan2(T[1,Ps:Pe].sum(),T[0,Ps:Pe].sum())
        F[idx,3]=np.abs(np.arctan2(np.sin(aP-aT),np.cos(aP-aT)))
        nonq=np.r_[0:q0,q1:L]
        F[idx,4]=rVM[:,nonq].sum(1)/qE                              # 비-QRS 총잔차(전반 이상)
        F[idx,5]=rVM[:,Ps:Pe].max(1)/(rVM[:,Ps:Pe].mean(1)+eps)     # P잔차 집중도(구조=피크성)
    return np.nan_to_num(F,posinf=0,neginf=0).astype("float32")

def _bestF(fams=("RHYTHM","KOOPMAN","GNN")):
    d=np.load(f"{_BASE}/mamba_data.npz"); beats,feats0,y,pid=d["beat"],d["feats"],d["y"],d["pid"]
    cols=["feats0","WST","MORPHO","REPOL","DTW"]+list(fams)
    BB=[_Lnpy(n) for n in cols]
    if any(x is None for x in BB): raise RuntimeError("캐시 없음 → colab_prep_all.py 먼저")
    return beats,y,pid,np.concatenate(BB,1).astype("float32"),"+".join(fams)

def diag_atrial(fams=("RHYTHM","KOOPMAN","GNN")):
    beats,y,pid,BEST,bb=_bestF(fams); print(f"백본: {bb}")
    m1=np.isin(pid,_DS1); m2=np.isin(pid,_DS2); y1,y2=y[m1],y[m2]
    print("심방(P) 잔차 계산..."); A=extract_atrial_features(beats,pid,y)
    def ev(X):
        sc=StandardScaler().fit(np.nan_to_num(X[m1])); X1=np.nan_to_num(sc.transform(np.nan_to_num(X[m1]))); X2=np.nan_to_num(sc.transform(np.nan_to_num(X[m2])))
        clf=LogisticRegression(max_iter=4000,C=0.5,class_weight={0:1,1:3,2:1.5}).fit(X1,y1)
        return average_precision_score((y2==1).astype(int),clf.predict_proba(X2)[:,1])
    bS=ev(BEST)
    print(f"\n=== 심방잔차 6특징: 단일AUC(DS1/DS2) / best 증분 (best S={bS:.4f}) ===")
    for k,nm in enumerate(ATR_NAMES):
        a1=roc_auc_score((y1==1).astype(int),A[m1,k]); a1=max(a1,1-a1)
        a2=roc_auc_score((y2==1).astype(int),A[m2,k]); a2=max(a2,1-a2)
        S=ev(np.concatenate([BEST,A[:,[k]]],1))
        print(f"  {nm:10s}: DS1={a1:.3f} DS2={a2:.3f}  +best→{S:.4f} ({S-bS:+.4f}) {'★' if S>bS+1e-4 else ''}")
    print(f"  +심방잔차 전부: S={ev(np.concatenate([BEST,A],1)):.4f}  (로지스틱=참고, 판정은 CNN)")
    np.save(f"{_FEATDIR}/ATRIAL.npy",A); print("  → ATRIAL.npy 저장(sweep 편입 가능)")
    global _ATRIAL; _ATRIAL=A; return A

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

def run_atrial_cnn(fams=("RHYTHM","KOOPMAN","GNN"), seeds=None):
    import torch, torch.nn as nn, torch.nn.functional as Fn
    from sklearn.preprocessing import RobustScaler
    from sklearn.model_selection import GroupShuffleSplit
    seeds=seeds or list(range(2000,2015)); dev="cuda" if torch.cuda.is_available() else "cpu"
    beats,y,pid,BEST,bb=_bestF(fams); print(f"백본: {bb}"); A=extract_atrial_features(beats,pid,y); ref=np.empty_like(beats)
    for p in np.unique(pid): m=pid==p; ref[m]=np.median(beats[m],0,keepdims=True)
    ref=ref.astype("float32"); m1=np.isin(pid,_DS1); m2=np.isin(pid,_DS2); y2=y[m2]
    Sw=auto_weights(y[m1]); nc=np.array([(y[m1]==k).sum() for k in range(3)],np.float32); mc=(1.0/np.power(nc,0.25)); mc=(mc/mc.max()*0.5).astype("float32")
    CFG={f"[{bb}]":BEST, f"[{bb}]+심방잔차":np.concatenate([BEST,A],1).astype("float32")}
    def met(p,yy): return (average_precision_score((yy==1).astype(int),p[:,1]),average_precision_score((yy==2).astype(int),p[:,2]))
    @torch.no_grad()
    def pred(M,b,r,ft):
        M.eval(); o=[]
        for i in range(0,len(b),4096):
            o.append(torch.softmax(M(torch.from_numpy(b[i:i+4096]).to(dev),torch.from_numpy(r[i:i+4096]).to(dev),torch.from_numpy(ft[i:i+4096]).to(dev)),-1).cpu().numpy())
        return np.concatenate(o)
    def train_one(F,seed):
        b1,r1,f1a,y1,p1=beats[m1],ref[m1],F[m1],y[m1],pid[m1]; b2,r2,f2a=beats[m2],ref[m2],F[m2]
        torch.manual_seed(seed); np.random.seed(seed)
        tr,va=next(GroupShuffleSplit(1,test_size=0.2,random_state=seed).split(f1a,y1,groups=p1))
        sc=RobustScaler().fit(f1a[tr]); f1=np.nan_to_num(sc.transform(f1a),posinf=0,neginf=0).astype("float32"); f2=np.nan_to_num(sc.transform(f2a),posinf=0,neginf=0).astype("float32")
        M=_net(F.shape[1]).to(dev); opt=torch.optim.AdamW(M.parameters(),lr=1e-3,weight_decay=1e-4)
        cw=torch.tensor([1.,Sw,1.5],device=dev); mcv=torch.from_numpy(mc).to(dev)
        ds=torch.utils.data.TensorDataset(*[torch.from_numpy(x) for x in (b1[tr],r1[tr],f1[tr],y1[tr])]); dl=torch.utils.data.DataLoader(ds,batch_size=512,shuffle=True); best=-1; bs=None
        for ep in range(15):
            M.train()
            for bb,rr,ff,yy in dl:
                bb,rr,ff,yy=(t.to(dev) for t in (bb,rr,ff,yy)); opt.zero_grad()
                lo=M(bb,rr,ff); lg=lo-torch.zeros_like(lo).scatter_(1,yy[:,None],mcv[yy][:,None])
                ce=Fn.cross_entropy(lg,yy,reduction="none"); wv=cw[yy]; loss=(ce*wv).sum()/wv.sum()
                loss.backward(); torch.nn.utils.clip_grad_norm_(M.parameters(),1.0); opt.step()
            pv=pred(M,b1[va],r1[va],f1[va]); s,v=met(pv,y1[va])
            if 0.5*(s+v)>best: best=0.5*(s+v); bs={k:vv.cpu() for k,vv in M.state_dict().items()}
        M.load_state_dict(bs); return pred(M,b2,r2,f2)
    def trim(Pn):
        medS=np.median(Pn[:,:,1],0); corr=np.array([np.corrcoef(Pn[i,:,1],medS)[0,1] for i in range(len(Pn))])
        keep=np.argsort(-corr)[:max(1,int(round(len(Pn)*0.8)))]; P=Pn[keep].mean(0); return P/P.sum(1,keepdims=True)
    res={}
    print(f"margin CNN {len(seeds)}seed, Sw={Sw:.1f}")
    for nm,F in CFG.items():
        Pt=trim(np.stack([train_one(F,s) for s in seeds],0)); S,V=met(Pt,y2); pr,se,f1=_f1(y2,Pt[:,1]); res[nm]=(S,pr,se,f1)
        print(f"  {nm:16s} S={S:.4f} PREC={pr:.3f} SEN={se:.3f} F1={f1:.3f}")
    b=res[f"[{bb}]"]; a=res[f"[{bb}]+심방잔차"]
    print(f"\n▶ ΔS={a[0]-b[0]:+.4f} ΔPREC={a[1]-b[1]:+.3f} ΔSEN={a[2]-b[2]:+.3f} ΔF1={a[3]-b[3]:+.3f}")
    print(f"  ★ ΔSEN>0 이면서 PREC 유지 = 심방잔차가 subtle S를 잡아 민감도 회복(Pareto 개선).")
    return res

# 여러 백본 한 번에 비교 (균형형 / 정밀형 / 4가지)
def run_atrial_backbones(seeds=None):
    R={}
    for fams in [("RHYTHM","KOOPMAN","GNN"),("KOOPMAN","AE","GNN"),("RHYTHM","KOOPMAN","AE","GNN")]:
        print("\n"+"="*58); R["+".join(fams)]=run_atrial_cnn(fams,seeds)
    return R
