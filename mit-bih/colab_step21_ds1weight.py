# =============================================================================
#  colab_step21_ds1weight.py  —  [STEP 21] 붕괴 판단을 DS1에서 (비누출·inductive)
#
#  사장님 지적: step20 합의는 label-free지만 DS2 예측을 봐서(transductive) 계산 →
#  DS2-free가 아님. 정직하려면 '붕괴 판단 규칙'을 DS1에서만 정하고 DS2엔 눈감고 적용.
#
#  설계: DS1 고정 val split(모든 seed 공통) → seed마다
#    · DS1-val 성능(S+V)      = 품질신호1 (DS1 라벨=학습데이터, 정당)
#    · DS1-val 합의상관·분산   = 품질신호2 (붕괴 seed는 DS1서도 어긋남/뭉갬)
#  이 DS1-품질로만 DS2 앙상블 가중(눈감고 적용). 그리고 결정적 측정:
#    corr(DS1품질, 실제 DS2-S)  →  붕괴가 DS1서 예측되나?
#      높으면 = 비누출 가중 성립(진짜 승리).  ~0 = 붕괴는 DS2고유 → uniform이 정직.
#
#  선행(캐시): _WST, extract_morpho_features, extract_repol_features/_REPOL
#  실행:
#    exec(open('/content/drive/MyDrive/mitbih/colab_step21_ds1weight.py').read())
#    run_ds1weight(Kwst=40)
# =============================================================================
import os
import numpy as np
from sklearn.metrics import average_precision_score

_DS1=[101,106,108,109,112,114,115,116,118,119,122,124,201,203,205,207,208,209,215,220,223,230]
_DS2=[100,103,105,111,113,117,121,123,200,202,210,212,213,214,219,221,222,228,231,232,233,234]
_SAVE="/content/drive/MyDrive/mitbih/ablation_step21"; _C={}
_REPOLK_IDX=[0,1,4,5]

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

def run_ds1weight(Kwst=40, seeds=None, val_seed=42, temp=0.05):
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
    Rk=Xr[:,_REPOLK_IDX].astype("float32")
    m1=np.isin(pid,_DS1); m2=np.isin(pid,_DS2); y2=y[m2]
    Xwk=np.nan_to_num(SelectKBest(f_classif,k=min(Kwst,Xw.shape[1])).fit(np.nan_to_num(Xw[m1]),y[m1]).transform(np.nan_to_num(Xw))).astype("float32")
    Fwm =np.concatenate([feats0,Xwk,Xm],1).astype("float32")
    Fwmr=np.concatenate([feats0,Xwk,Xm,Rk],1).astype("float32")
    # ★ DS1 고정 val split (모든 seed·config 공통) — DS1서 붕괴판단이 목적
    y1=y[m1]; p1=pid[m1]
    tr,va=next(GroupShuffleSplit(1,test_size=0.2,random_state=val_seed).split(Fwm[m1],y1,groups=p1))
    print(f"DS1 고정 val: train {len(tr)} / val {len(va)} beats (val S={int((y1[va]==1).sum())}, V={int((y1[va]==2).sum())})")
    def met(p,yy): return (average_precision_score((yy==1).astype(int),p[:,1]),average_precision_score((yy==2).astype(int),p[:,2]))
    @torch.no_grad()
    def pred(M,b,r,ft):
        M.eval(); o=[]
        for i in range(0,len(b),4096):
            o.append(torch.softmax(M(torch.from_numpy(b[i:i+4096]).to(dev),torch.from_numpy(r[i:i+4096]).to(dev),torch.from_numpy(ft[i:i+4096]).to(dev)),-1).cpu().numpy())
        return np.concatenate(o)
    def train_one(F,seed):
        b1,r1,f1a=beats[m1],ref[m1],F[m1]; b2,r2,f2a=beats[m2],ref[m2],F[m2]
        torch.manual_seed(seed); np.random.seed(seed)                 # init·셔플만 seed, split은 고정
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
        M.load_state_dict(bs)
        Pv=pred(M,b1[va],r1[va],f1[va])                               # DS1-val 예측(고정 val, 공통)
        P2=pred(M,b2,r2,f2)                                           # DS2 예측
        vs,vv=met(Pv,y1[va])
        return P2,Pv,vs,vv
    P2s,Pvs,valS,valV=[],[],[],[]
    tags=[]
    for cfg,F in [("wm",Fwm),("wr",Fwmr)]:
        for seed in seeds:
            P2,Pv,vs,vv=train_one(F,seed); P2s.append(P2); Pvs.append(Pv); valS.append(vs); valV.append(vv); tags.append(f"{cfg}{seed}")
            print(f"  {cfg}{seed}:  DS1val S={vs:.3f} V={vv:.3f}   |  DS2 S={met(P2,y2)[0]:.3f}")
    P2=np.stack(P2s,0); Pv=np.stack(Pvs,0); valS=np.array(valS); valV=np.array(valV)
    os.makedirs(_SAVE,exist_ok=True); np.savez(os.path.join(_SAVE,"pool.npz"),P2=P2,Pv=Pv,valS=valS,valV=valV,y2=y2,tags=tags)
    # ---- DS1 전용 품질 신호 ----
    qperf=0.5*(valS+valV)                                             # ①DS1 성능
    Sv=Pv[:,:,1]; medv=np.median(Sv,0)
    cons=np.nan_to_num(np.array([np.corrcoef(Sv[i],medv)[0,1] for i in range(len(Sv))]))  # ②DS1 합의
    stdv=Sv.std(1); stdv=stdv/(np.median(stdv)+1e-9)
    qcons=np.clip(cons,0,None)*np.clip(stdv,0,1.5)
    ds2S=np.array([met(P2[i],y2)[0] for i in range(len(P2))])         # (평가용) 실제 DS2-S
    def cc(a,b): return float(np.corrcoef(a,b)[0,1])
    print(f"\n{'='*58}\n★ 붕괴는 DS1서 예측되나?  corr(DS1품질, 실제 DS2-S):")
    print(f"   DS1성능(qperf) ↔ DS2-S : {cc(qperf,ds2S):+.3f}")
    print(f"   DS1합의(qcons) ↔ DS2-S : {cc(qcons,ds2S):+.3f}")
    print("   (>+0.3 이면 DS1로 붕괴 예측 가능=비누출 가중 성립.  ~0 이면 DS2고유→uniform 정직)")
    # ---- DS1-품질로만 DS2 앙상블(눈감고 적용) ----
    def norm(P): return P/P.sum(-1,keepdims=True)
    def wsum(w): return norm((w[:,None,None]*P2).sum(0))
    def sm(q): e=np.exp(np.clip(q,0,None)/temp); return e/e.sum()
    def trim(q,keep=0.8):
        k=max(1,int(round(len(q)*keep))); idx=np.argsort(-q)[:k]; w=np.zeros(len(q)); w[idx]=1.0/k; return w
    uni=np.ones(len(P2))/len(P2)
    combos=[("uniform(기준)",uni),
            ("DS1성능-가중",sm(qperf)),("DS1성능-트림",trim(qperf)),
            ("DS1합의-가중",sm(qcons)),("DS1합의-트림",trim(qcons))]
    print(f"\n  [DS1규칙 → DS2적용]  (가중치는 DS1만 사용, DS2는 평가만)")
    base=None
    for nm,w in combos:
        s,v=met(wsum(w),y2)
        if nm.startswith("uniform"): base=s
        print(f"   {nm:14s}: S={s:.4f}  V={v:.4f}   ({s-base:+.4f} vs uniform)" if base is not None else "")
    # 참고: transductive(DS2 합의) — 누출 가능, 비교용
    S2=P2[:,:,1]; med2=np.median(S2,0); cons2=np.nan_to_num(np.array([np.corrcoef(S2[i],med2)[0,1] for i in range(len(S2))]))
    std2=S2.std(1); std2=std2/(np.median(std2)+1e-9); q2=np.clip(cons2,0,None)*np.clip(std2,0,1.5)
    st,_=met(wsum(trim(q2)),y2); print(f"\n   [참고·누출가능] DS2합의-트림(step20식): S={st:.4f}")
    print(f"   → DS1규칙이 uniform보다 확실히↑면 정직한 승리. DS2합의에만 근접하면 그 이득은 누출.")
    return dict(qperf=qperf,qcons=qcons,ds2S=ds2S)
