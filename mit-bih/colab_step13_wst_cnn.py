# =============================================================================
#  colab_step13_wst_cnn.py  —  [STEP 13] WST 상위특징을 CNN에 (15seed paired)
#
#  step12: 26+WST 로지스틱 증분 +0.110(P파 +0.08보다 강함). CNN서 살아남나?
#  P파 교훈: 252개 다 넣으면 특징MLP 교란 → DS1에서 top-K 선별해 추가.
#  label-free(all-beat median ref), base26 vs 26+WST_topK paired 앙상블 비교.
#
#  선행 로드: colab_step12_wst.py (compute_wst_features; diag_wst 돌렸으면 _WST 캐시)
#  준비:  !pip install kymatio -q
#  실행:
#    exec(open('/content/drive/MyDrive/mitbih/colab_step13_wst_cnn.py').read())
#    run_wst_cnn(K=40)                         # 기본 15 seed
#    run_wst_cnn(K=40, seeds=[1000,1001,1002,1003,1004])  # 빠른 5 seed
# =============================================================================
import os
import numpy as np
from sklearn.metrics import average_precision_score

_DS1=[101,106,108,109,112,114,115,116,118,119,122,124,201,203,205,207,208,209,215,220,223,230]
_DS2=[100,103,105,111,113,117,121,123,200,202,210,212,213,214,219,221,222,228,231,232,233,234]
_SAVE="/content/drive/MyDrive/mitbih/ablation_step13"
_C={}

def _build_net(fdim):
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

def run_wst_cnn(K=40, seeds=None):
    import torch, torch.nn as nn
    from sklearn.preprocessing import RobustScaler
    from sklearn.model_selection import GroupShuffleSplit
    from sklearn.feature_selection import SelectKBest, f_classif
    seeds=seeds or list(range(1000,1015)); dev="cuda" if torch.cuda.is_available() else "cpu"
    d=np.load("/content/drive/MyDrive/mitbih/mamba_data.npz")
    beats,feats0,y,pid=d["beat"],d["feats"],d["y"],d["pid"]
    # label-free ref(all-beat median)
    if "ref" not in _C:
        r=np.empty_like(beats)
        for p in np.unique(pid):
            m=pid==p; r[m]=np.median(beats[m],axis=0,keepdims=True)
        _C["ref"]=r.astype("float32")
    ref=_C["ref"]
    # WST (step12 캐시 재사용 or 계산)
    Xw = globals().get("_WST", None)
    if Xw is None:
        print("WST 계산..."); Xw=compute_wst_features(beats)
    m1=np.isin(pid,_DS1); m2=np.isin(pid,_DS2)
    # DS1에서 상위 K개 WST 선별(라벨=DS1, 정당)
    sel=SelectKBest(f_classif,k=min(K,Xw.shape[1])).fit(np.nan_to_num(Xw[m1]),y[m1])
    Xwk=np.nan_to_num(sel.transform(np.nan_to_num(Xw))).astype("float32")
    feat_full=np.concatenate([feats0,Xwk],1).astype("float32")   # 26+K
    print(f"WST 상위 {Xwk.shape[1]}개 선별 → combined feat_dim={feat_full.shape[1]}")

    def met(p,yy): return (average_precision_score((yy==1).astype(int),p[:,1]),average_precision_score((yy==2).astype(int),p[:,2]))
    @torch.no_grad()
    def predict(M,b,r,ft):
        M.eval(); o=[]
        for i in range(0,len(b),4096):
            o.append(torch.softmax(M(torch.from_numpy(b[i:i+4096]).to(dev),torch.from_numpy(r[i:i+4096]).to(dev),
                torch.from_numpy(ft[i:i+4096]).to(dev)),-1).cpu().numpy())
        return np.concatenate(o)
    def train_one(F,seed):
        b1,r1,ft1,y1,p1=beats[m1],ref[m1],F[m1],y[m1],pid[m1]; b2,r2,ft2,y2=beats[m2],ref[m2],F[m2],y[m2]
        torch.manual_seed(seed); np.random.seed(seed)
        tr,va=next(GroupShuffleSplit(1,test_size=0.2,random_state=seed).split(ft1,y1,groups=p1))
        sc=RobustScaler().fit(ft1[tr])
        f1=np.nan_to_num(sc.transform(ft1),posinf=0,neginf=0).astype("float32"); f2=np.nan_to_num(sc.transform(ft2),posinf=0,neginf=0).astype("float32")
        M=_build_net(F.shape[1]).to(dev); opt=torch.optim.AdamW(M.parameters(),lr=1e-3,weight_decay=1e-4)
        lf=nn.CrossEntropyLoss(weight=torch.tensor([1.,3.,1.5],device=dev))
        ds=torch.utils.data.TensorDataset(*[torch.from_numpy(x) for x in (b1[tr],r1[tr],f1[tr],y1[tr])])
        dl=torch.utils.data.DataLoader(ds,batch_size=512,shuffle=True); best=-1; bs=None
        for ep in range(15):
            M.train()
            for bb,rr,ff,yy in dl:
                bb,rr,ff,yy=(t.to(dev) for t in (bb,rr,ff,yy)); opt.zero_grad()
                loss=lf(M(bb,rr,ff),yy); loss.backward(); torch.nn.utils.clip_grad_norm_(M.parameters(),1.0); opt.step()
            pv=predict(M,b1[va],r1[va],f1[va]); s,v=met(pv,y1[va])
            if 0.5*(s+v)>best: best=0.5*(s+v); bs={k:v.cpu() for k,v in M.state_dict().items()}
        M.load_state_dict(bs); return predict(M,b2,r2,f2),y2
    res={"base26":{"S":[],"pr":[]},"wst":{"S":[],"pr":[]}}
    feat26=feats0.astype("float32")
    for seed in seeds:
        for tag,F in [("base26",feat26),("wst",feat_full)]:
            P,y2=train_one(F,seed); s,v=met(P,y2); res[tag]["S"].append(s); res[tag]["pr"].append(P)
        print(f"  seed {seed}:  base26 S={res['base26']['S'][-1]:.4f}   26+WST S={res['wst']['S'][-1]:.4f}")
    y2=y[m2]; print(f"\n{'='*54}")
    for tag,nm in [("base26","base26    "),("wst","26+WST_top")]:
        Sarr=np.array(res[tag]["S"]); ens=np.stack(res[tag]["pr"],0).mean(0); ens=ens/ens.sum(1,keepdims=True); es,ev=met(ens,y2)
        os.makedirs(os.path.join(_SAVE,tag),exist_ok=True); np.savez(os.path.join(_SAVE,tag,"ens.npz"),prob=ens,y=y2,pid=pid[m2])
        print(f"[{nm}] 개별S={Sarr.mean():.4f}±{Sarr.std():.4f}  ▶앙상블S={es:.4f}  V={ev:.4f}"); res[tag]["ensS"]=es
    dS=res["wst"]["ensS"]-res["base26"]["ensS"]
    print(f"\n▶ (26+WST) − base26 앙상블 S = {dS:+.4f}   ({len(seeds)} seed, K={K})")
    print("   >+0.05: WST가 CNN서 벽 넘음(P파와 달리 흡수 안됨).  ~0/음수: CNN이 흡수.")
    return res
