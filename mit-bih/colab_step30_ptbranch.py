# =============================================================================
#  colab_step30_ptbranch.py  —  [STEP 30] P/T 집중 conv 샴 분기 (구조 도전)
#
#  whole-beat MF(step27) 실패 = QRS가 지배(S/N 공유). 그래서 QRS를 마스킹(0)하고
#  P·T 구간만 남긴 비트를 '별도 conv 샴 분기'로 → 환자 정상(ref)의 같은 마스킹본과 비교.
#  = P/T 집중 + 개인화(자기 정상 대비) + 표현학습(스칼라 아님→흡수 회피 시도).
#  best(26+WST+morpho+repolK, ~0.72) 위에 가지로 결합. 정밀도 목표라 PR-AUC + F1 둘 다.
#
#  선행 로드: step12(_WST)·step15(extract_morpho)·step18(extract_repol)
#  실행:
#    exec(open('/content/drive/MyDrive/mitbih/colab_step30_ptbranch.py').read())
#    run_pt(Kwst=40)
# =============================================================================
import os
import numpy as np
from sklearn.metrics import average_precision_score, precision_recall_curve

_DS1=[101,106,108,109,112,114,115,116,118,119,122,124,201,203,205,207,208,209,215,220,223,230]
_DS2=[100,103,105,111,113,117,121,123,200,202,210,212,213,214,219,221,222,228,231,232,233,234]
_SAVE="/content/drive/MyDrive/mitbih/ablation_step30"; _C={}
_REPOLK_IDX=[0,1,4,5]

def _mask_qrs(beats, ref, pid, half=20):
    """환자 정상 R기준 QRS(±half) 0마스킹 → P·T만 남김."""
    out=np.empty_like(beats); L=beats.shape[2]
    for p in np.unique(pid):
        idx=np.where(pid==p)[0]
        VMr=np.sqrt(ref[idx[0],0]**2+ref[idx[0],1]**2); R=int(np.argmax(VMr))
        m=np.ones(L,np.float32); m[max(0,R-half):min(L,R+half)]=0.0
        out[idx]=beats[idx]*m
    return out.astype("float32")

def _net(fdim, use_pt=False):
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
            s.use_pt=use_pt; extra=0
            if use_pt:
                s.pte=Enc(); s.psia=nn.Sequential(nn.Linear(256,64),nn.ReLU()); extra=64   # P/T 집중 샴
            s.cls=nn.Sequential(nn.Linear(192+extra,64),nn.ReLU(),nn.Linear(64,3))
        def forward(s,b,r,ft,bpt,rpt):
            z1=s.e(b); z2=s.e(r); zb=s.sia(torch.cat([z1,z2,z1-z2,(z1-z2).abs()],-1))
            z=z1+torch.sigmoid(s.gate(torch.cat([z1,zb],-1)))*zb
            zp=torch.softmax((z@s.proto.t())*(64**-0.5),-1)@s.proto
            parts=[z,zp,s.fm(ft)]
            if s.use_pt:
                p1=s.pte(bpt); p2=s.pte(rpt); parts.append(s.psia(torch.cat([p1,p2,p1-p2,(p1-p2).abs()],-1)))
            return s.cls(torch.cat(parts,-1))
    return Net()

def _f1(y2,s):
    p,r,_=precision_recall_curve((y2==1).astype(int),s); f=2*p*r/(p+r+1e-9); i=int(np.nanargmax(f)); return p[i],r[i],f[i]

def run_pt(Kwst=40, half=20, seeds=None):
    import torch, torch.nn as nn
    from sklearn.preprocessing import RobustScaler
    from sklearn.model_selection import GroupShuffleSplit
    from sklearn.feature_selection import SelectKBest, f_classif
    seeds=seeds or list(range(1000,1015)); dev="cuda" if torch.cuda.is_available() else "cpu"
    d=np.load("/content/drive/MyDrive/mitbih/mamba_data.npz")
    beats,feats0,y,pid=d["beat"],d["feats"],d["y"],d["pid"]
    if "ref" not in _C:
        r=np.empty_like(beats)
        for p in np.unique(pid): m=pid==p; r[m]=np.median(beats[m],axis=0,keepdims=True)
        _C["ref"]=r.astype("float32")
    ref=_C["ref"]
    BPT=_mask_qrs(beats,ref,pid,half); RPT=_mask_qrs(ref,ref,pid,half)             # QRS 마스킹(P/T만)
    Xw=globals().get("_WST",None); Xw=Xw if Xw is not None else compute_wst_features(beats)
    Xm=globals().get("_MORPHO",None); Xm=Xm if Xm is not None else extract_morpho_features(beats,ref,pid)
    Xr=globals().get("_REPOL",None); Xr=Xr if Xr is not None else extract_repol_features(beats,ref,pid)
    m1=np.isin(pid,_DS1); m2=np.isin(pid,_DS2); y2=y[m2]
    Xwk=np.nan_to_num(SelectKBest(f_classif,k=min(Kwst,Xw.shape[1])).fit(np.nan_to_num(Xw[m1]),y[m1]).transform(np.nan_to_num(Xw))).astype("float32")
    F=np.concatenate([feats0,Xwk,Xm,Xr[:,_REPOLK_IDX]],1).astype("float32")         # best 특징(동일)
    print(f"best dim={F.shape[1]}  /  P/T분기: QRS±{half} 마스킹, 별도 conv 샴")
    def met(p,yy): return (average_precision_score((yy==1).astype(int),p[:,1]),average_precision_score((yy==2).astype(int),p[:,2]))
    @torch.no_grad()
    def pred(M,b,r,ft,bpt,rpt):
        M.eval(); o=[]
        for i in range(0,len(b),4096):
            sl=slice(i,i+4096); T=lambda x:torch.from_numpy(x[sl]).to(dev)
            o.append(torch.softmax(M(T(b),T(r),T(ft),T(bpt),T(rpt)),-1).cpu().numpy())
        return np.concatenate(o)
    def train_one(use_pt,seed):
        b1,r1,f1a,y1,p1=beats[m1],ref[m1],F[m1],y[m1],pid[m1]; b2,r2,f2a=beats[m2],ref[m2],F[m2]
        bp1,rp1,bp2,rp2=BPT[m1],RPT[m1],BPT[m2],RPT[m2]
        torch.manual_seed(seed); np.random.seed(seed)
        tr,va=next(GroupShuffleSplit(1,test_size=0.2,random_state=seed).split(f1a,y1,groups=p1))
        sc=RobustScaler().fit(f1a[tr]); f1=np.nan_to_num(sc.transform(f1a),posinf=0,neginf=0).astype("float32"); f2=np.nan_to_num(sc.transform(f2a),posinf=0,neginf=0).astype("float32")
        M=_net(F.shape[1],use_pt).to(dev); opt=torch.optim.AdamW(M.parameters(),lr=1e-3,weight_decay=1e-4)
        lf=nn.CrossEntropyLoss(weight=torch.tensor([1.,3.,1.5],device=dev))
        ds=torch.utils.data.TensorDataset(*[torch.from_numpy(x) for x in (b1[tr],r1[tr],f1[tr],bp1[tr],rp1[tr],y1[tr])])
        dl=torch.utils.data.DataLoader(ds,batch_size=512,shuffle=True); best=-1; bs=None
        for ep in range(15):
            M.train()
            for bb,rr,ff,bpp,rpp,yy in dl:
                bb,rr,ff,bpp,rpp,yy=(t.to(dev) for t in (bb,rr,ff,bpp,rpp,yy)); opt.zero_grad()
                loss=lf(M(bb,rr,ff,bpp,rpp),yy); loss.backward(); torch.nn.utils.clip_grad_norm_(M.parameters(),1.0); opt.step()
            pv=pred(M,b1[va],r1[va],f1[va],bp1[va],rp1[va]); s,v=met(pv,y1[va])
            if 0.5*(s+v)>best: best=0.5*(s+v); bs={k:v.cpu() for k,v in M.state_dict().items()}
        M.load_state_dict(bs); return pred(M,b2,r2,f2,bp2,rp2)
    def trim(Pn):
        medS=np.median(Pn[:,:,1],0); corr=np.array([np.corrcoef(Pn[i,:,1],medS)[0,1] for i in range(len(Pn))])
        keep=np.argsort(-corr)[:max(1,int(round(len(Pn)*0.8)))]; P=Pn[keep].mean(0); return P/P.sum(1,keepdims=True)
    R={"b":[],"pt":[]}
    for seed in seeds:
        R["b"].append(train_one(False,seed)); R["pt"].append(train_one(True,seed))
        print(f"  seed {seed}:  best S={met(R['b'][-1],y2)[0]:.4f}   +P/T분기 S={met(R['pt'][-1],y2)[0]:.4f}")
    os.makedirs(_SAVE,exist_ok=True)
    print(f"\n{'='*56}")
    for tag,nm in [("b","best       "),("pt","best+P/T분기")]:
        Pn=np.stack(R[tag],0); np.savez(os.path.join(_SAVE,f"{tag}.npz"),P=Pn,y=y2,pid=pid[m2])
        Pt=trim(Pn); S,V=met(Pt,y2); pr,se,f1=_f1(y2,Pt[:,1])
        print(f"[{nm}] 트림 S={S:.4f} V={V:.4f}  |  best-F1: PREC={pr:.3f} SEN={se:.3f} F1={f1:.3f}")
    print(f"\n▶ +P/T분기가 S·특히 PREC/F1 올리면 = P/T 집중 표현이 정밀도 보강(구조 도전 성공).")
    return R
