# =============================================================================
#  colab_step14_robust.py  —  [STEP 14] WST + 붕괴 seed 제어(합의 가중 앙상블)
#
#  step13: 26+WST가 CNN서 +0.072(15seed, label-free 최고 0.565). 단 일부 seed 붕괴
#  (예: 1012 0.65→0.29). 사장님 아이디어: 붕괴 케이스를 가중치로 조절.
#
#  구현(label-free): per-seed 예측 저장 → 붕괴 seed는 다른 seed 합의(median)와 크게
#  어긋남 → 합의 상관으로 가중치 자동 하향. DS2 라벨 미사용.
#    · 균일 앙상블  vs  합의-가중 앙상블  vs  트림(하위 상관 seed 제거)
#
#  선행 로드: colab_step12_wst.py (compute_wst_features / _WST 캐시)
#  실행:
#    exec(open('/content/drive/MyDrive/mitbih/colab_step14_robust.py').read())
#    run_wst_robust(K=40)                     # 15 seed
# =============================================================================
import os
import numpy as np
from sklearn.metrics import average_precision_score

_DS1=[101,106,108,109,112,114,115,116,118,119,122,124,201,203,205,207,208,209,215,220,223,230]
_DS2=[100,103,105,111,113,117,121,123,200,202,210,212,213,214,219,221,222,228,231,232,233,234]
_SAVE="/content/drive/MyDrive/mitbih/ablation_step14"; _C={}

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

def run_wst_robust(K=40, seeds=None):
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
    Xw=globals().get("_WST",None)
    if Xw is None: print("WST 계산..."); Xw=compute_wst_features(beats)
    m1=np.isin(pid,_DS1); m2=np.isin(pid,_DS2); y2=y[m2]
    sel=SelectKBest(f_classif,k=min(K,Xw.shape[1])).fit(np.nan_to_num(Xw[m1]),y[m1])
    Xwk=np.nan_to_num(sel.transform(np.nan_to_num(Xw))).astype("float32")
    F=np.concatenate([feats0,Xwk],1).astype("float32")
    def met(p,yy): return (average_precision_score((yy==1).astype(int),p[:,1]),average_precision_score((yy==2).astype(int),p[:,2]))
    @torch.no_grad()
    def pred(M,b,r,ft):
        M.eval(); o=[]
        for i in range(0,len(b),4096):
            o.append(torch.softmax(M(torch.from_numpy(b[i:i+4096]).to(dev),torch.from_numpy(r[i:i+4096]).to(dev),torch.from_numpy(ft[i:i+4096]).to(dev)),-1).cpu().numpy())
        return np.concatenate(o)
    b1,r1,ft1a,y1,p1=beats[m1],ref[m1],F[m1],y[m1],pid[m1]; b2,r2,ft2a=beats[m2],ref[m2],F[m2]
    perseed=[]
    for seed in seeds:
        torch.manual_seed(seed); np.random.seed(seed)
        tr,va=next(GroupShuffleSplit(1,test_size=0.2,random_state=seed).split(ft1a,y1,groups=p1))
        sc=RobustScaler().fit(ft1a[tr])
        f1=np.nan_to_num(sc.transform(ft1a),posinf=0,neginf=0).astype("float32"); f2=np.nan_to_num(sc.transform(ft2a),posinf=0,neginf=0).astype("float32")
        M=_net(F.shape[1]).to(dev); opt=torch.optim.AdamW(M.parameters(),lr=1e-3,weight_decay=1e-4)
        lf=nn.CrossEntropyLoss(weight=torch.tensor([1.,3.,1.5],device=dev))
        ds=torch.utils.data.TensorDataset(*[torch.from_numpy(x) for x in (b1[tr],r1[tr],f1[tr],y1[tr])])
        dl=torch.utils.data.DataLoader(ds,batch_size=512,shuffle=True); best=-1; bs=None
        for ep in range(15):
            M.train()
            for bb,rr,ff,yy in dl:
                bb,rr,ff,yy=(t.to(dev) for t in (bb,rr,ff,yy)); opt.zero_grad()
                loss=lf(M(bb,rr,ff),yy); loss.backward(); torch.nn.utils.clip_grad_norm_(M.parameters(),1.0); opt.step()
            pv=pred(M,b1[va],r1[va],f1[va]); s,v=met(pv,y1[va])
            if 0.5*(s+v)>best: best=0.5*(s+v); bs={k:v.cpu() for k,v in M.state_dict().items()}
        M.load_state_dict(bs); P=pred(M,b2,r2,f2); perseed.append(P)
        print(f"  seed {seed}:  S={met(P,y2)[0]:.4f}")
    Pn=np.stack(perseed,0)                                   # [nS,N,3]
    os.makedirs(_SAVE,exist_ok=True); np.savez(os.path.join(_SAVE,"perseed.npz"),P=Pn,y=y2,pid=pid[m2])
    def norm(p): return p/p.sum(1,keepdims=True)
    medS=np.median(Pn[:,:,1],0)                              # 합의(붕괴에 강건)
    corr=np.array([np.corrcoef(Pn[i,:,1],medS)[0,1] for i in range(len(seeds))])
    # ① 균일  ② median(붕괴 자연 무시)  ③ 합의-가중(softmax 날카롭게)  ④ 트림
    uni=norm(Pn.mean(0))
    med=norm(np.median(Pn,0))
    w=np.exp(np.clip(corr,0,None)/0.05); w=w/w.sum()          # 온도 0.05로 붕괴 강하게 하향
    wt=norm((w[:,None,None]*Pn).sum(0))
    keep=np.argsort(-corr)[:max(1,int(round(len(seeds)*0.8)))]
    trim=norm(Pn[keep].mean(0))
    print(f"\n{'='*50}\n  붕괴진단(합의상관): {np.round(corr,2)}")
    print(f"  최저상관 seed={seeds[int(np.argmin(corr))]}  제거된 seed(트림)={[seeds[i] for i in range(len(seeds)) if i not in keep]}")
    print(f"  가중치: {np.round(w,3)}")
    best=("",-1)
    for nm,P in [("① 균일",uni),("② median(강건)",med),("③ 합의-가중",wt),("④ 트림(하위20%제거)",trim)]:
        s,v=met(P,y2); print(f"  {nm:20s}: S={s:.4f}  V={v:.4f}")
        if s>best[1]: best=(nm,s)
    print(f"\n  기준 step13 균일=0.565.  최고={best[0]} S={best[1]:.4f}")
    print(f"  → 0.565 넘으면 = 붕괴 제어가 성능↑ (사장님 아이디어 성립)")
    return dict(perseed=Pn,corr=corr)
