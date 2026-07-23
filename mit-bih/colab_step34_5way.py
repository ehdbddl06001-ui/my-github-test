# =============================================================================
#  colab_step34_5way.py  —  [STEP 34] 5-way 조합 CNN 검증 (고차시너지 확인)
#
#  step32 diag_combos: 전체 최고 = WST+morph+repol+segT+VCG (로지스틱 0.728, 고차시너지 +0.345).
#  segT·VCG는 단독/pairwise론 손해였는데 repol과 셋이 뭉치면 폭발 = 사장님 '교집합 시너지' 증명.
#  단 로지스틱 → CNN서 줄 수 있음(morph·segT 전례). 그래서 CNN 15seed로 0.72 넘는지 확인.
#
#  best(26+WST+morph+repolK) vs 5way(+segT4 +VCG12), 15seed paired + 트림, PR-AUC + F1.
#  xlead는 제외(step32서 유일한 독, 5→6서 0.728→0.498 파괴).
#  선행 캐시: _WST, extract_morpho/_MORPHO, extract_repol/_REPOL, extract_segdev/_SEGDEV, extract_vcg/_VCG
#  실행:
#    exec(open('/content/drive/MyDrive/mitbih/colab_step34_5way.py').read())
#    run_5way(Kwst=40)
# =============================================================================
import os
import numpy as np
from sklearn.metrics import average_precision_score, precision_recall_curve

_DS1=[101,106,108,109,112,114,115,116,118,119,122,124,201,203,205,207,208,209,215,220,223,230]
_DS2=[100,103,105,111,113,117,121,123,200,202,210,212,213,214,219,221,222,228,231,232,233,234]
_SAVE="/content/drive/MyDrive/mitbih/ablation_step34"; _C={}
_REPOLK_IDX=[0,1,4,5]; _SEG_IDX=[9,10,8,4]

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

def run_5way(Kwst=40, seeds=None):
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
    Xw=globals().get("_WST",None); Xw=Xw if Xw is not None else compute_wst_features(beats)
    Xm=globals().get("_MORPHO",None); Xm=Xm if Xm is not None else extract_morpho_features(beats,ref,pid)
    Xr=globals().get("_REPOL",None); Xr=Xr if Xr is not None else extract_repol_features(beats,ref,pid)
    Xs=globals().get("_SEGDEV",None); Xs=Xs if Xs is not None else extract_segdev_features(beats,ref,pid)
    Xv=globals().get("_VCG",None); Xv=Xv if Xv is not None else extract_vcg_features(beats,ref,pid)
    m1=np.isin(pid,_DS1); m2=np.isin(pid,_DS2); y2=y[m2]
    Xwk=np.nan_to_num(SelectKBest(f_classif,k=min(Kwst,Xw.shape[1])).fit(np.nan_to_num(Xw[m1]),y[m1]).transform(np.nan_to_num(Xw))).astype("float32")
    Fb =np.concatenate([feats0,Xwk,Xm,Xr[:,_REPOLK_IDX]],1).astype("float32")               # best
    F5 =np.concatenate([feats0,Xwk,Xm,Xr[:,_REPOLK_IDX],Xs[:,_SEG_IDX],Xv],1).astype("float32")  # +segT +VCG
    print(f"best dim={Fb.shape[1]}  /  5way dim={F5.shape[1]}  (추가: segT4 + VCG12)")
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
        lf=nn.CrossEntropyLoss(weight=torch.tensor([1.,3.,1.5],device=dev))
        ds=torch.utils.data.TensorDataset(*[torch.from_numpy(x) for x in (b1[tr],r1[tr],f1[tr],y1[tr])]); dl=torch.utils.data.DataLoader(ds,batch_size=512,shuffle=True); best=-1; bs=None
        for ep in range(15):
            M.train()
            for bb,rr,ff,yy in dl:
                bb,rr,ff,yy=(t.to(dev) for t in (bb,rr,ff,yy)); opt.zero_grad()
                loss=lf(M(bb,rr,ff),yy); loss.backward(); torch.nn.utils.clip_grad_norm_(M.parameters(),1.0); opt.step()
            pv=pred(M,b1[va],r1[va],f1[va]); s,v=met(pv,y1[va])
            if 0.5*(s+v)>best: best=0.5*(s+v); bs={k:v.cpu() for k,v in M.state_dict().items()}
        M.load_state_dict(bs); return pred(M,b2,r2,f2)
    def trim(Pn):
        medS=np.median(Pn[:,:,1],0); corr=np.array([np.corrcoef(Pn[i,:,1],medS)[0,1] for i in range(len(Pn))])
        keep=np.argsort(-corr)[:max(1,int(round(len(Pn)*0.8)))]; P=Pn[keep].mean(0); return P/P.sum(1,keepdims=True)
    R={"b":[],"5":[]}
    for seed in seeds:
        R["b"].append(train_one(Fb,seed)); R["5"].append(train_one(F5,seed))
        print(f"  seed {seed}:  best S={met(R['b'][-1],y2)[0]:.4f}   5way S={met(R['5'][-1],y2)[0]:.4f}")
    os.makedirs(_SAVE,exist_ok=True)
    print(f"\n{'='*56}")
    for tag,nm in [("b","best  "),("5","5way  ")]:
        Pn=np.stack(R[tag],0); np.savez(os.path.join(_SAVE,f"{tag}.npz"),P=Pn,y=y2,pid=pid[m2])
        Pt=trim(Pn); S,V=met(Pt,y2); pr,se,f1=_f1(y2,Pt[:,1])
        print(f"[{nm}] 트림 S={S:.4f} V={V:.4f}  |  best-F1: PREC={pr:.3f} SEN={se:.3f} F1={f1:.3f}")
    print(f"\n▶ 5way가 best(트림~0.72) 넘으면 = 고차시너지가 CNN서도 진짜(새 최고, MoE보다 간단).")
    print(f"  ~0/음수면 = 로지스틱 시너지가 CNN엔 흡수 → MoE/전문화로.")
    return R
