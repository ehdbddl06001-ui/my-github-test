# =============================================================================
#  colab_step11_combined.py  —  [STEP 11] 크루드+분리 P파 다 합쳐 CNN (15seed paired)
#
#  두 P파 아이디어 결합: 26 + 크루드8(step9) + 분리8(step10) = 42 특징.
#  모든 것 label-free: ref·P파 모두 '자기예측 정상'(라벨 미사용).
#  같은 seed·같은 ref로 base26 vs combined42 를 paired 비교(공정).
#
#  선행 로드(3개):
#    colab_step9_pwave.py    (extract_pwave_features)
#    colab_step9c_labelfree.py (_selfpred_ref)
#    colab_step10_denoise.py (extract_pwave_denoised)
#  실행:
#    exec(open('.../colab_step11_combined.py').read())
#    run_combined()                         # 기본 15 seed
#    run_combined(seeds=[1000,1001,1002,1003,1004])   # 빠른 5 seed
# =============================================================================
import os
import numpy as np
from sklearn.metrics import average_precision_score, roc_auc_score

_DS1=[101,106,108,109,112,114,115,116,118,119,122,124,201,203,205,207,208,209,215,220,223,230]
_DS2=[100,103,105,111,113,117,121,123,200,202,210,212,213,214,219,221,222,228,231,232,233,234]
_SAVE="/content/drive/MyDrive/mitbih/ablation_step11"
_CACHE={}

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
            super().__init__(); s.e=Enc()
            s.sia=nn.Sequential(nn.Linear(256,64),nn.ReLU()); s.gate=nn.Linear(128,64)
            s.proto=nn.Parameter(torch.randn(32,64)*0.1)
            s.fm=nn.Sequential(nn.Linear(fdim,64),nn.ReLU(),nn.Linear(64,64),nn.ReLU())
            s.cls=nn.Sequential(nn.Linear(192,64),nn.ReLU(),nn.Linear(64,3))
        def forward(s,b,r,ft):
            z1=s.e(b); z2=s.e(r); zb=s.sia(torch.cat([z1,z2,z1-z2,(z1-z2).abs()],-1))
            z=z1+torch.sigmoid(s.gate(torch.cat([z1,zb],-1)))*zb
            zp=torch.softmax((z@s.proto.t())*(64**-0.5),-1)@s.proto
            return s.cls(torch.cat([z,zp,s.fm(ft)],-1))
    return Net()

def run_combined(seeds=None):
    import torch, torch.nn as nn
    from sklearn.preprocessing import RobustScaler
    from sklearn.model_selection import GroupShuffleSplit
    seeds=seeds or list(range(1000,1015)); dev="cuda" if torch.cuda.is_available() else "cpu"
    d=np.load("/content/drive/MyDrive/mitbih/mamba_data.npz")
    beats,feats0,y,pid=d["beat"],d["feats"],d["y"],d["pid"]
    if "ref" not in _CACHE:
        print("자기예측 정상 ref 생성..."); _CACHE["ref"]=_selfpred_ref(beats,feats0,y,pid,dev)
    ref=_CACHE["ref"]
    if "feat" not in _CACHE:
        print("크루드8 + 분리8 계산...")
        Xc=extract_pwave_features(beats,ref,pid); Xd=extract_pwave_denoised(beats,ref,pid)
        _CACHE["feat"]=np.concatenate([feats0,Xc,Xd],1).astype("float32")   # 26+8+8=42
    feat_full=_CACHE["feat"]
    m1=np.isin(pid,_DS1); m2=np.isin(pid,_DS2)

    def met(p,yy): return (average_precision_score((yy==1).astype(int),p[:,1]),average_precision_score((yy==2).astype(int),p[:,2]))
    @torch.no_grad()
    def predict(M,b,r,ft):
        M.eval(); o=[]
        for i in range(0,len(b),4096):
            o.append(torch.softmax(M(torch.from_numpy(b[i:i+4096]).to(dev),torch.from_numpy(r[i:i+4096]).to(dev),
                torch.from_numpy(ft[i:i+4096]).to(dev)),-1).cpu().numpy())
        return np.concatenate(o)
    def train_one(FE,seed):
        F=FE; fdim=F.shape[1]
        b1,r1,ft1,y1,p1=beats[m1],ref[m1],F[m1],y[m1],pid[m1]
        b2,r2,ft2,y2=beats[m2],ref[m2],F[m2],y[m2]
        torch.manual_seed(seed); np.random.seed(seed)
        tr,va=next(GroupShuffleSplit(1,test_size=0.2,random_state=seed).split(ft1,y1,groups=p1))
        sc=RobustScaler().fit(ft1[tr])
        f1=np.nan_to_num(sc.transform(ft1),posinf=0,neginf=0).astype("float32")
        f2=np.nan_to_num(sc.transform(ft2),posinf=0,neginf=0).astype("float32")
        M=_build_net(fdim).to(dev); opt=torch.optim.AdamW(M.parameters(),lr=1e-3,weight_decay=1e-4)
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

    res={"base26":{"S":[],"pr":[]},"combined42":{"S":[],"pr":[]}}
    feat26=feats0.astype("float32")
    for seed in seeds:
        for tag,FE in [("base26",feat26),("combined42",feat_full)]:
            P,y2=train_one(FE,seed); s,v=met(P,y2); res[tag]["S"].append(s); res[tag]["pr"].append(P)
        print(f"  seed {seed}:  base26 S={res['base26']['S'][-1]:.4f}   combined42 S={res['combined42']['S'][-1]:.4f}")
    print(f"\n{'='*56}")
    y2=y[m2]
    for tag in ["base26","combined42"]:
        Sarr=np.array(res[tag]["S"]); ens=np.stack(res[tag]["pr"],0).mean(0); ens=ens/ens.sum(1,keepdims=True)
        es,ev=met(ens,y2)
        os.makedirs(os.path.join(_SAVE,tag),exist_ok=True); np.savez(os.path.join(_SAVE,tag,"ens.npz"),prob=ens,y=y2,pid=pid[m2])
        print(f"[{tag:11s}] 개별S={Sarr.mean():.4f}±{Sarr.std():.4f}   ▶앙상블S={es:.4f}  V={ev:.4f}")
        res[tag]["ensS"]=es
    dS=res["combined42"]["ensS"]-res["base26"]["ensS"]
    print(f"\n▶ combined − base26 (앙상블 S) = {dS:+.4f}   ({len(seeds)} seed)")
    print("   >+0.05: 두 P파 아이디어 합본이 CNN서 벽 넘음.  ~0: CNN이 흡수(정보는 실재하나 순증 없음).")
    return res
