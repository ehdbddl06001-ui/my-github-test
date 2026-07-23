# =============================================================================
#  colab_step19_repolk.py  —  [STEP 19] 재분극 '믿을 수 있는 소수' 를 CNN에
#
#  STEP18 단일-특징 스캔: repol 12개 통째로는 독(중복-L2), 하지만 개별론 일부 +.
#  '테스트로 고르기' 함정을 피해, 부호 일관(절대·정상대비 둘다 +) + morpho 신규
#  기준으로 4개만 채택:
#    RT중심(무게중심, 절대/정상대비)  +  T비대칭(왜도/skew, 절대/정상대비)
#    · skew = morpho에 아예 없던 새 축(재분극 비대칭)  · RT중심 = morpho RT간격의 강건판
#  로지스틱 +0.02~0.04는 노이즈 바닥 안 → CNN 15seed paired(진짜 저울)로 확인.
#
#  선행 로드(캐시): colab_step12_wst.py(_WST), colab_step15_morpho.py(extract_morpho_features),
#                   colab_step18_repol.py(extract_repol_features/_REPOL)
#  실행:
#    exec(open('/content/drive/MyDrive/mitbih/colab_step19_repolk.py').read())
#    run_repolk(Kwst=40)
# =============================================================================
import os
import numpy as np
from sklearn.metrics import average_precision_score

_DS1=[101,106,108,109,112,114,115,116,118,119,122,124,201,203,205,207,208,209,215,220,223,230]
_DS2=[100,103,105,111,113,117,121,123,200,202,210,212,213,214,219,221,222,228,231,232,233,234]
_SAVE="/content/drive/MyDrive/mitbih/ablation_step19"; _C={}
_REPOLK_IDX=[0,1,4,5]   # RT중심(절대),RT중심(정상대비),T비대칭(절대),T비대칭(정상대비)

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

def _robust(Pn,y2,met):
    def norm(p): return p/p.sum(1,keepdims=True)
    medS=np.median(Pn[:,:,1],0); corr=np.array([np.corrcoef(Pn[i,:,1],medS)[0,1] for i in range(len(Pn))])
    keep=np.argsort(-corr)[:max(1,int(round(len(Pn)*0.8)))]
    return met(norm(Pn.mean(0)),y2)[0], met(norm(Pn[keep].mean(0)),y2)[0]   # (균일S, 트림S)

def run_repolk(Kwst=40, seeds=None):
    import torch, torch.nn as nn
    from sklearn.preprocessing import RobustScaler
    from sklearn.model_selection import GroupShuffleSplit
    from sklearn.feature_selection import SelectKBest, f_classif
    seeds=seeds or list(range(1000,1015)); dev="cuda" if torch.cuda.is_available() else "cpu"
    d=np.load("/content/drive/MyDrive/mitbih/mamba_data.npz")
    beats,feats0,y,pid=d["beat"],d["feats"],d["y"],d["pid"]
    if "ref" not in _C:
        r=np.empty_like(beats)
        for p in np.unique(pid):
            m=pid==p; r[m]=np.median(beats[m],axis=0,keepdims=True)
        _C["ref"]=r.astype("float32")
    ref=_C["ref"]
    Xw=globals().get("_WST",None); Xw=Xw if Xw is not None else compute_wst_features(beats)
    Xm=globals().get("_MORPHO",None); Xm=Xm if Xm is not None else extract_morpho_features(beats,ref,pid)
    Xr=globals().get("_REPOL",None); Xr=Xr if Xr is not None else extract_repol_features(beats,ref,pid)
    Rk=Xr[:,_REPOLK_IDX].astype("float32")                          # 믿을 수 있는 4개
    m1=np.isin(pid,_DS1); m2=np.isin(pid,_DS2); y2=y[m2]
    Xwk=np.nan_to_num(SelectKBest(f_classif,k=min(Kwst,Xw.shape[1])).fit(np.nan_to_num(Xw[m1]),y[m1]).transform(np.nan_to_num(Xw))).astype("float32")
    Fwm =np.concatenate([feats0,Xwk,Xm],1).astype("float32")        # 26+WST+morpho (기준)
    Fwmr=np.concatenate([feats0,Xwk,Xm,Rk],1).astype("float32")     # +repolK(4)
    print(f"26+WST+morpho dim={Fwm.shape[1]}  /  +repolK dim={Fwmr.shape[1]}  (추가4: RT중심x2, T비대칭x2)")
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
    R={"wm":[],"wmr":[]}
    for seed in seeds:
        R["wm"].append(train_one(Fwm,seed)); R["wmr"].append(train_one(Fwmr,seed))
        print(f"  seed {seed}:  base S={met(R['wm'][-1],y2)[0]:.4f}   +repolK S={met(R['wmr'][-1],y2)[0]:.4f}")
    os.makedirs(_SAVE,exist_ok=True)
    print(f"\n{'='*52}")
    out={}
    for tag,nm in [("wm","26+WST+morpho"),("wmr","+repolK(4) ")]:
        Pn=np.stack(R[tag],0); np.savez(os.path.join(_SAVE,f"{tag}.npz"),P=Pn,y=y2,pid=pid[m2])
        uS,tS=_robust(Pn,y2,met); out[tag]=(uS,tS)
        print(f"[{nm}] 균일S={uS:.4f}  트림S={tS:.4f}")
    print(f"\n▶ (+repolK − base):  균일 {out['wmr'][0]-out['wm'][0]:+.4f}   트림 {out['wmr'][1]-out['wm'][1]:+.4f}")
    print("   >+0.03: 재분극(비대칭·RT중심)이 CNN서도 새 정보.  ~0/음수: 흡수(스칼라 천장 확정).")
    return out
