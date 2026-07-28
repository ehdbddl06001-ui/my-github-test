# =============================================================================
#  colab_step43_leadablation.py  —  [STEP 43] 리드 의존도 (두 리드 주의점 정량화)
#
#  MIT-BIH 채널2 불일치(V1 40 / V2·V4·V5 8, 102·104는 채널1도 V5=제외). 논문 한계로 명시하되,
#  '우리 모델이 불일치한 2번 리드에 얼마나 의존하나'를 테스트로 방어:
#   Dual(양 리드) vs MLII-only(채널2=0 → VM=|lead0|, WST·morph·repol·DTW 재계산) 15seed 비교.
#   차이 작으면=2번리드 의존 낮음(불일치 위협 작음).  크면=의존 큼(정직히 한계 명시).
#  주의: 26 de Chazal 특징은 npz에 미리 계산돼 있어 양쪽 동일(부분 ablation — 방향은 유효).
#
#  선행: compute_wst_features, extract_morpho/repol/dtw 함수 로드 + 캐시 _WST·_MORPHO·_REPOL·_DTW
#  실행:
#    exec(open('/content/drive/MyDrive/mitbih/colab_step43_leadablation.py').read())
#    run_leadablation()          # WST 재계산 있어 느림(수분). seeds 조절 가능
# =============================================================================
import numpy as np
from sklearn.metrics import average_precision_score, precision_recall_curve

_DS1=[101,106,108,109,112,114,115,116,118,119,122,124,201,203,205,207,208,209,215,220,223,230]
_DS2=[100,103,105,111,113,117,121,123,200,202,210,212,213,214,219,221,222,228,231,232,233,234]
_C={}; _REPOLK_IDX=[0,1,4,5]

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
def _medref(beats,pid):
    r=np.empty_like(beats)
    for p in np.unique(pid): m=pid==p; r[m]=np.median(beats[m],axis=0,keepdims=True)
    return r.astype("float32")

def auto_weights(y1, beta=0.9999):
    """DS1 클래스수에서 S가중치 계산(하드코딩 금지·DB전이): 유효표본수(Cui 2019)."""
    nN=(y1==0).sum(); nS=max((y1==1).sum(),1)
    eff=lambda n:(1-beta)/(1-beta**n+1e-12)
    return float(eff(nS)/eff(nN))                     # N대비 S배수 (MIT-BIH면 ≈11)

def run_leadablation(Kwst=40, Sw=None, seeds=None, recompute_wst=True):
    import torch, torch.nn as nn
    from sklearn.preprocessing import RobustScaler
    from sklearn.model_selection import GroupShuffleSplit
    from sklearn.feature_selection import SelectKBest, f_classif
    seeds=seeds or list(range(1000,1010)); dev="cuda" if torch.cuda.is_available() else "cpu"
    d=np.load("/content/drive/MyDrive/mitbih/mamba_data.npz"); beats,feats0,y,pid=d["beat"],d["feats"],d["y"],d["pid"]
    m1=np.isin(pid,_DS1); m2=np.isin(pid,_DS2); y2=y[m2]
    if Sw is None: Sw=auto_weights(y[m1]); print(f"S가중치 자동계산(유효표본수, DS1 클래스수 유래)= {Sw:.2f}  (DS2 튜닝 아님)")
    def buildF(bb, Xw, Xm, Xr, Xd):
        Xwk=np.nan_to_num(SelectKBest(f_classif,k=min(Kwst,Xw.shape[1])).fit(np.nan_to_num(Xw[m1]),y[m1]).transform(np.nan_to_num(Xw))).astype("float32")
        return np.concatenate([feats0,Xwk,Xm,Xr[:,_REPOLK_IDX],Xd],1).astype("float32")
    # Dual (캐시)
    refD=_medref(beats,pid)
    Fdual=buildF(beats, globals()["_WST"], globals()["_MORPHO"], globals()["_REPOL"], globals()["_DTW"])
    # MLII-only: 채널2=0 → 재계산
    print("MLII-only 재계산 중 (WST 포함이라 수분 소요)...")
    bM=beats.copy(); bM[:,1,:]=0.0; refM=_medref(bM,pid)
    WSTm=compute_wst_features(bM) if recompute_wst else globals()["_WST"]
    Mm=extract_morpho_features(bM,refM,pid); Rm=extract_repol_features(bM,refM,pid); Dm=extract_dtw_features(bM,refM,pid,y)
    Fmlii=buildF(bM, WSTm, Mm, Rm, Dm)
    CFG={"Dual(양리드)":(beats,refD,Fdual),"MLII-only(채널2=0)":(bM,refM,Fmlii)}
    def met(p,yy): return (average_precision_score((yy==1).astype(int),p[:,1]),average_precision_score((yy==2).astype(int),p[:,2]))
    @torch.no_grad()
    def pred(M,b,r,ft):
        M.eval(); o=[]
        for i in range(0,len(b),4096):
            o.append(torch.softmax(M(torch.from_numpy(b[i:i+4096]).to(dev),torch.from_numpy(r[i:i+4096]).to(dev),torch.from_numpy(ft[i:i+4096]).to(dev)),-1).cpu().numpy())
        return np.concatenate(o)
    def train_one(bb,rf,F,seed):
        b1,r1,f1a,y1,p1=bb[m1],rf[m1],F[m1],y[m1],pid[m1]; b2,r2,f2a=bb[m2],rf[m2],F[m2]
        torch.manual_seed(seed); np.random.seed(seed)
        tr,va=next(GroupShuffleSplit(1,test_size=0.2,random_state=seed).split(f1a,y1,groups=p1))
        sc=RobustScaler().fit(f1a[tr]); f1=np.nan_to_num(sc.transform(f1a),posinf=0,neginf=0).astype("float32"); f2=np.nan_to_num(sc.transform(f2a),posinf=0,neginf=0).astype("float32")
        M=_net(F.shape[1]).to(dev); opt=torch.optim.AdamW(M.parameters(),lr=1e-3,weight_decay=1e-4)
        lf=nn.CrossEntropyLoss(weight=torch.tensor([1.,Sw,1.5],device=dev))
        ds=torch.utils.data.TensorDataset(*[torch.from_numpy(x) for x in (b1[tr],r1[tr],f1[tr],y1[tr])]); dl=torch.utils.data.DataLoader(ds,batch_size=512,shuffle=True); best=-1; bs=None
        for ep in range(15):
            M.train()
            for a,c,e,g in dl:
                a,c,e,g=(t.to(dev) for t in (a,c,e,g)); opt.zero_grad()
                loss=lf(M(a,c,e),g); loss.backward(); torch.nn.utils.clip_grad_norm_(M.parameters(),1.0); opt.step()
            pv=pred(M,b1[va],r1[va],f1[va]); s,v=met(pv,y1[va])
            if 0.5*(s+v)>best: best=0.5*(s+v); bs={k:v.cpu() for k,v in M.state_dict().items()}
        M.load_state_dict(bs); return pred(M,b2,r2,f2)
    def trim(Pn):
        medS=np.median(Pn[:,:,1],0); corr=np.array([np.corrcoef(Pn[i,:,1],medS)[0,1] for i in range(len(Pn))])
        keep=np.argsort(-corr)[:max(1,int(round(len(Pn)*0.8)))]; P=Pn[keep].mean(0); return P/P.sum(1,keepdims=True)
    print(f"\nS가중치={Sw}, {len(seeds)}seed")
    res={}
    for nm,(bb,rf,F) in CFG.items():
        Pt=trim(np.stack([train_one(bb,rf,F,s) for s in seeds],0)); S,V=met(Pt,y2); pr,se,f1=_f1(y2,Pt[:,1]); res[nm]=(S,pr,se,f1)
        print(f"  {nm:20s} 트림 S={S:.4f}  PREC={pr:.3f} SEN={se:.3f} F1={f1:.3f}")
    dS=res["Dual(양리드)"][0]-res["MLII-only(채널2=0)"][0]
    print(f"\n▶ 2번 리드 기여(Dual − MLII):  ΔS={dS:+.4f}")
    print(f"  작으면(≲0.03) = 2번 리드 의존 낮음 → 채널 불일치가 성능 위협 작음(논문 방어).")
    print(f"  크면 = 2번 리드 크게 활용 → 불일치를 정직한 한계로 명시.")
    return res
