# =============================================================================
#  colab_step45_finale.py  —  [STEP 45] margin(LDAM) 확정 + 2D-DTW(QRS) 마지막 확인
#
#  STEP44 승자 = LDAM margin (PR-AUC·PREC·F1 ↑, SEN 유지, 파라미터-free). 이를 새 기준으로:
#   1) margin-best                : best+DTW_full + LDAM margin  (새 기준)
#   2) margin-best + 2D-QRS자기DTW : 사장님 2D-DTW 중 최강 단일(QRS 자기DTW) 1개 추가
#   3) margin-best + 2D-full(15)   : 2D-DTW 15특징 전부 추가 (블록이 도움되나)
#  전부 동일 구조·동일 시드(내부 비교 유효), 15seed 트림. 2D가 margin 위에서도 이득인지 최종판정.
#  margin·S가중치 모두 DS1 클래스수 유래(파라미터-free, DS2 튜닝 아님).
#
#  선행 캐시: _WST,_MORPHO,_REPOL,_DTW  (+ _DTWMV 없으면 step41에서 자동생성)
#  실행:
#    exec(open('/content/drive/MyDrive/mitbih/colab_step45_finale.py').read())
#    run_finale()               # 느리면 seeds=list(range(1000,1008))
# =============================================================================
import os
import numpy as np
from sklearn.metrics import average_precision_score, precision_recall_curve

_BASE="/content/drive/MyDrive/mitbih"
_DS1=[101,106,108,109,112,114,115,116,118,119,122,124,201,203,205,207,208,209,215,220,223,230]
_DS2=[100,103,105,111,113,117,121,123,200,202,210,212,213,214,219,221,222,228,231,232,233,234]
_SAVE=f"{_BASE}/ablation_step45"; _C={}; _REPOLK_IDX=[0,1,4,5]
_QRS_SELF_IDX=6           # 2D-DTW: _SEG=[P,PR,QRS,ST,T]×[자기DTW,워핑이득,S-N] → QRS자기DTW=2*3+0

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
def auto_weights(y1, beta=0.9999):
    nN=(y1==0).sum(); nS=max((y1==1).sum(),1)
    eff=lambda n:(1-beta)/(1-beta**n+1e-12); return float(eff(nS)/eff(nN))

def run_finale(Kwst=40, Sw=None, seeds=None):
    import torch, torch.nn as nn, torch.nn.functional as Fn
    from sklearn.preprocessing import RobustScaler
    from sklearn.model_selection import GroupShuffleSplit
    from sklearn.feature_selection import SelectKBest, f_classif
    seeds=seeds or list(range(1000,1015)); dev="cuda" if torch.cuda.is_available() else "cpu"
    d=np.load(f"{_BASE}/mamba_data.npz"); beats,feats0,y,pid=d["beat"],d["feats"],d["y"],d["pid"]
    if "ref" not in _C:
        r=np.empty_like(beats)
        for p in np.unique(pid): m=pid==p; r[m]=np.median(beats[m],axis=0,keepdims=True)
        _C["ref"]=r.astype("float32")
    ref=_C["ref"]
    Xw=globals().get("_WST"); Xm=globals().get("_MORPHO"); Xr=globals().get("_REPOL"); Xd=globals().get("_DTW")
    m1=np.isin(pid,_DS1); m2=np.isin(pid,_DS2); y2=y[m2]
    if Sw is None: Sw=auto_weights(y[m1]); print(f"S가중치 자동(유효표본수, DS1유래)= {Sw:.2f}")
    # 2D-DTW 캐시 확보(없으면 step41에서 생성)
    Xmv=globals().get("_DTWMV")
    if Xmv is None:
        print("2D-DTW(_DTWMV) 없음 → step41 로드해 생성(수분)...")
        exec(open(f"{_BASE}/colab_step41_dtwmv.py").read(), globals())
        Xmv=globals()["extract_dtwmv_features"](beats,ref,pid,y); globals()["_DTWMV"]=Xmv
    Xwk=np.nan_to_num(SelectKBest(f_classif,k=min(Kwst,Xw.shape[1])).fit(np.nan_to_num(Xw[m1]),y[m1]).transform(np.nan_to_num(Xw))).astype("float32")
    Fbase=np.concatenate([feats0,Xwk,Xm,Xr[:,_REPOLK_IDX],Xd],1).astype("float32")     # best+DTW_full
    qrs=Xmv[:,[_QRS_SELF_IDX]].astype("float32")
    CFG={"margin-best":Fbase,
         "margin-best+2D-QRS":np.concatenate([Fbase,qrs],1).astype("float32"),
         "margin-best+2D-full":np.concatenate([Fbase,Xmv],1).astype("float32")}
    print("구성:",{k:v.shape[1] for k,v in CFG.items()})
    nc=np.array([(y[m1]==k).sum() for k in range(3)],np.float32); mc=1.0/np.power(nc,0.25); mc=(mc/mc.max()*0.5).astype("float32")
    print(f"LDAM margins={np.round(mc,3)}  (전부 파라미터-free, DS2 튜닝 아님)")
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
                lo=M(bb,rr,ff)
                lg=lo-torch.zeros_like(lo).scatter_(1,yy[:,None],mcv[yy][:,None])   # LDAM: 참클래스 margin 차감
                ce=Fn.cross_entropy(lg,yy,reduction="none"); w=cw[yy]; loss=(ce*w).sum()/w.sum()
                loss.backward(); torch.nn.utils.clip_grad_norm_(M.parameters(),1.0); opt.step()
            pv=pred(M,b1[va],r1[va],f1[va]); s,v=met(pv,y1[va])
            if 0.5*(s+v)>best: best=0.5*(s+v); bs={k:v.cpu() for k,v in M.state_dict().items()}
        M.load_state_dict(bs); return pred(M,b2,r2,f2)
    def trim(Pn):
        medS=np.median(Pn[:,:,1],0); corr=np.array([np.corrcoef(Pn[i,:,1],medS)[0,1] for i in range(len(Pn))])
        keep=np.argsort(-corr)[:max(1,int(round(len(Pn)*0.8)))]; P=Pn[keep].mean(0); return P/P.sum(1,keepdims=True)
    os.makedirs(_SAVE,exist_ok=True); res={}
    print(f"\n{len(seeds)}seed (LDAM margin 적용)")
    for name,F in CFG.items():
        Pn=np.stack([train_one(F,s) for s in seeds],0); np.savez(os.path.join(_SAVE,name.replace("+","_")+".npz"),P=Pn,y=y2)
        Pt=trim(Pn); S,V=met(Pt,y2); pr,se,f1=_f1(y2,Pt[:,1]); res[name]=(S,pr,se,f1)
        print(f"  {name:22s} 트림 S={S:.4f}  PREC={pr:.3f} SEN={se:.3f} F1={f1:.3f}")
    b=res["margin-best"]
    print(f"\n{'='*58}\n▶ margin-best 대비:")
    for name,(S,pr,se,f1) in res.items():
        if name=="margin-best": continue
        print(f"  {name:22s}: ΔS={S-b[0]:+.4f}  ΔPREC={pr-b[1]:+.3f}  ΔSEN={se-b[2]:+.3f}  ΔF1={f1-b[3]:+.3f}")
    print(f"\n  ★ 2D가 margin 위에서도 ΔS>0 & ΔPREC>0 이면 최종모델에 포함. 아니면 margin-best로 확정.")
    return res
