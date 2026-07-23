# =============================================================================
#  colab_step9d_final.py  —  [최종] label-free P파 특징을 CNN에 (자기예측 정상 ref)
#
#  step9c: label-free P파 증분 확인 (자기예측 정상 ref: S +0.081, 로지스틱).
#  최종 확인: 그 P파 특징을 CNN에 넣어 앙상블 S가 노이즈 바닥(±0.05)을 넘나.
#    · 모든 것 label-free: 모델 ref·P파 ref 모두 '자기예측 정상'(라벨 미사용)
#    · base26(26특징) vs pwave34(26+P파8) 동일 저울(gss+앙상블)
#
#  선행 로드: colab_step9_pwave.py(extract_pwave_features), colab_step9c_labelfree.py(_selfpred_ref)
#  실행:
#    exec(open('.../colab_step9_pwave.py').read()); exec(open('.../colab_step9c_labelfree.py').read())
#    exec(open('.../colab_step9d_final.py').read())
#    run_final("base26"); run_final("pwave")
# =============================================================================
import os
import numpy as np
from sklearn.metrics import average_precision_score, roc_auc_score

_DS1=[101,106,108,109,112,114,115,116,118,119,122,124,201,203,205,207,208,209,215,220,223,230]
_DS2=[100,103,105,111,113,117,121,123,200,202,210,212,213,214,219,221,222,228,231,232,233,234]
_SEEDS=[1000,1001,1002,1003,1004]
_SAVE="/content/drive/MyDrive/mitbih/ablation_step9d"

_SPREF_CACHE={}   # 자기예측 정상 ref 캐시(재사용)

def run_final(tag, seeds=None):
    import torch, torch.nn as nn
    from sklearn.preprocessing import RobustScaler
    from sklearn.model_selection import GroupShuffleSplit
    use_pw=(tag=="pwave"); seeds=seeds or _SEEDS
    dev="cuda" if torch.cuda.is_available() else "cpu"
    d=np.load("/content/drive/MyDrive/mitbih/mamba_data.npz")
    beats,feats,y,pid=d["beat"],d["feats"],d["y"],d["pid"]
    # 자기예측 정상 ref (label-free) — 캐시
    if "ref" not in _SPREF_CACHE:
        print("자기예측 정상 ref 생성(bootstrap CNN)...")
        _SPREF_CACHE["ref"]=_selfpred_ref(beats,feats,y,pid,dev)   # step9c
    ref_lf=_SPREF_CACHE["ref"]
    if use_pw:
        Xpw=extract_pwave_features(beats,ref_lf,pid)              # step9, label-free ref
        feats=np.concatenate([feats,Xpw],1).astype("float32")
    fdim=feats.shape[1]
    print(f"===== {tag} =====  feat_dim={fdim}  device={dev}")

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
    def ld(a,bs,sh):
        ds=torch.utils.data.TensorDataset(*[torch.from_numpy(np.asarray(x)) for x in a])
        return torch.utils.data.DataLoader(ds,batch_size=bs,shuffle=sh)
    @torch.no_grad()
    def pr(m,b,r,ft):
        m.eval(); o=[]
        for i in range(0,len(b),4096):
            o.append(torch.softmax(m(torch.from_numpy(b[i:i+4096]).to(dev),
                torch.from_numpy(r[i:i+4096]).to(dev),torch.from_numpy(ft[i:i+4096]).to(dev)),-1).cpu().numpy())
        return np.concatenate(o)
    def met(p,yy): return (average_precision_score((yy==1).astype(int),p[:,1]),average_precision_score((yy==2).astype(int),p[:,2]))
    def ppa(p,yy,pp,ms=5):
        a=[]
        for q in np.unique(pp):
            m=pp==q; z=(yy[m]==1).astype(int)
            if z.sum()<ms or z.sum()==m.sum(): continue
            a.append(roc_auc_score(z,p[m,1]))
        return float(np.mean(a)) if a else float("nan")

    m1=np.isin(pid,_DS1); m2=np.isin(pid,_DS2)
    b1,r1,ft1,y1,p1=beats[m1],ref_lf[m1],feats[m1],y[m1],pid[m1]
    b2,r2,ft2,y2,p2=beats[m2],ref_lf[m2],feats[m2],y[m2],pid[m2]
    os.makedirs(os.path.join(_SAVE,tag),exist_ok=True); probs=[]; Ss=[]
    for seed in seeds:
        import torch as T; T.manual_seed(seed); np.random.seed(seed)
        tr,va=next(GroupShuffleSplit(1,test_size=0.2,random_state=seed).split(ft1,y1,groups=p1))
        sc=RobustScaler().fit(ft1[tr])
        f1=np.nan_to_num(sc.transform(ft1),posinf=0,neginf=0).astype("float32")
        f2=np.nan_to_num(sc.transform(ft2),posinf=0,neginf=0).astype("float32")
        M=Net().to(dev); opt=T.optim.AdamW(M.parameters(),lr=1e-3,weight_decay=1e-4)
        lf=nn.CrossEntropyLoss(weight=T.tensor([1.,3.,1.5],device=dev))
        best=-1; bs=None; tl=ld((b1[tr],r1[tr],f1[tr],y1[tr]),512,True)
        for ep in range(15):
            M.train()
            for bb,rr,ff,yy in tl:
                bb,rr,ff,yy=(t.to(dev) for t in (bb,rr,ff,yy)); opt.zero_grad()
                loss=lf(M(bb,rr,ff),yy); loss.backward(); T.nn.utils.clip_grad_norm_(M.parameters(),1.0); opt.step()
            pv=pr(M,b1[va],r1[va],f1[va]); s,v=met(pv,y1[va])
            if 0.5*(s+v)>best: best=0.5*(s+v); bs={k:v.cpu() for k,v in M.state_dict().items()}
        M.load_state_dict(bs); P=pr(M,b2,r2,f2); probs.append(P)
        s,v=met(P,y2); Ss.append(s); print(f"  [seed {seed}]  S={s:.4f}  V={v:.4f}")
    ens=np.stack(probs,0).mean(0); ens=ens/ens.sum(1,keepdims=True)
    s,v=met(ens,y2)
    np.savez(os.path.join(_SAVE,tag,"ens.npz"),prob=ens,y=y2,pid=p2)
    print(f"\n----- {tag} -----  개별S={np.mean(Ss):.4f}±{np.std(Ss):.4f}  ▶앙상블S={s:.4f}  V={v:.4f}  환자별={ppa(ens,y2,p2):.4f}")
    return dict(S=s,V=v)
