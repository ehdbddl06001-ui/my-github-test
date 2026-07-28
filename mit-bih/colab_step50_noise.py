# =============================================================================
#  colab_step50_noise.py  —  [STEP 50] 잔차 '노이즈 성격' innovation — 사장님 '노이즈의 노이즈'
#
#  STEP49: 리듬 innovation(잔차 크기)이 CNN에서 대박(PREC 0.725→0.802). 한 단계 더:
#  잔차의 '성격'을 본다 = 칼만 innovation whiteness. 정상비트 잔차=백색노이즈(구조없음),
#  이소성 잔차=구조있음(코히런트 이상형태) → '정상 노이즈'가 아니라 '새 노이즈' 발생 =
#  심장상태 변화. 잔차의 백색성·스펙엔트로피·비가우시안성·정상노이즈 대비 divergence·
#  분산innovation(GARCH)으로 특징화. 크기가 아닌 '노이즈다움의 붕괴'를 잡는 새 축.
#
#  선행: _WST,_MORPHO,_REPOL,_DTW (recover) + step49(extract_rhythm_v2) Drive에 있어야
#  실행:
#    exec(open('/content/drive/MyDrive/mitbih/colab_step50_noise.py').read())
#    diag_noise()             # 노이즈성격 단일AUC + best 증분(빠름, 참고용)
#    run_noise_cnn()          # 결정판정: base vs +리듬10 vs +리듬10+노이즈 (margin CNN 15seed)
# =============================================================================
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.metrics import average_precision_score, precision_recall_curve, roc_auc_score

_BASE="/content/drive/MyDrive/mitbih"
_DS1=[101,106,108,109,112,114,115,116,118,119,122,124,201,203,205,207,208,209,215,220,223,230]
_DS2=[100,103,105,111,113,117,121,123,200,202,210,212,213,214,219,221,222,228,231,232,233,234]
_REPOLK_IDX=[0,1,4,5]
NOISE_NAMES=["잔차백색성","잔차저주파비","스펙엔트로피역","잔차첨도","스펙divergence","구조에너지비","분산innov(GARCH)"]

def _ewma_causal(X, alpha):
    pred=np.zeros_like(X); acc=X[0].copy()
    for t in range(1,len(X)): pred[t]=acc; acc=alpha*X[t]+(1-alpha)*acc
    pred[0]=X[0]; return pred
def _f1(y2,s):
    p,r,_=precision_recall_curve((y2==1).astype(int),s); f=2*p*r/(p+r+1e-9); i=int(np.nanargmax(f)); return p[i],r[i],f[i]
def auto_weights(y1,beta=0.9999):
    nN=(y1==0).sum(); nS=max((y1==1).sum(),1); eff=lambda n:(1-beta)/(1-beta**n+1e-12); return float(eff(nS)/eff(nN))
def _smooth(X,k=7):
    ker=np.ones(k)/k; return np.apply_along_axis(lambda v:np.convolve(v,ker,mode="same"),1,X)

def extract_noise_features(beats, pid, y=None, alpha=0.3, K=6, lowbins=15):
    """잔차의 '노이즈 성격' 7특징. 정상비트=백색노이즈, 이소성=구조 → 백색성 붕괴 포착."""
    if y is None: y=np.load(f"{_BASE}/mamba_data.npz")["y"]
    N=len(beats); eps=1e-6; F=np.zeros((N,7),np.float32)
    for p in np.unique(pid):
        idx=np.where(pid==p)[0]; b=beats[idx]
        VM=np.sqrt(b[:,0]**2+b[:,1]**2).astype(np.float64)          # (n,L)
        res=VM-_ewma_causal(VM,alpha)                              # 예측잔차(=innovation)
        n,L=res.shape
        # 1) 백색성: |lag1..K 자기상관| 합 (구조 있으면 큼)
        v=res.var(1)+eps; wh=np.zeros(n)
        for lag in range(1,K+1):
            wh+=np.abs((res[:,lag:]*res[:,:-lag]).mean(1)/v)
        F[idx,0]=wh
        # 스펙트럼
        S=np.abs(np.fft.rfft(res,axis=1))**2; S=S/(S.sum(1,keepdims=True)+eps)   # (n,nf) 정규 파워스펙
        F[idx,1]=S[:,:lowbins].sum(1)                              # 2) 저주파(구조)비
        F[idx,2]=1.0/(-(S*np.log(S+eps)).sum(1)+eps)               # 3) 스펙엔트로피 역(구조=낮은엔트로피=큰값)
        # 4) 첨도(비가우시안=구조/스파이크)
        m=res.mean(1,keepdims=True); d=res-m; F[idx,3]=(d**4).mean(1)/((d**2).mean(1)**2+eps)-3.0
        # 5) 정상노이즈 스펙트럼(환자 중앙값) 대비 log-스펙 divergence
        Snorm=np.median(S,0,keepdims=True)
        F[idx,4]=np.abs(np.log(S+eps)-np.log(Snorm+eps)).mean(1)
        # 6) 구조에너지비: 평활잔차(구조) / 전체잔차 에너지 (노이즈는 평활시 사라짐)
        rs=_smooth(res,7); F[idx,5]=(rs**2).sum(1)/((res**2).sum(1)+eps)
        # 7) 분산innovation(GARCH식): 비트별 잔차분산의 인과예측 대비 로그비
        vs=res.var(1); pv=_ewma_causal(vs[:,None],alpha)[:,0]; F[idx,6]=np.log((vs+eps)/(pv+eps))
    return np.nan_to_num(F,posinf=0,neginf=0).astype("float32")

def _bestF():
    d=np.load(f"{_BASE}/mamba_data.npz"); beats,feats0,y,pid=d["beat"],d["feats"],d["y"],d["pid"]; m1=np.isin(pid,_DS1)
    Xw=globals().get("_WST"); Xm=globals().get("_MORPHO"); Xr=globals().get("_REPOL"); Xd=globals().get("_DTW")
    Xwk=np.nan_to_num(SelectKBest(f_classif,k=min(40,Xw.shape[1])).fit(np.nan_to_num(Xw[m1]),y[m1]).transform(np.nan_to_num(Xw)))
    BEST=np.concatenate([feats0,Xwk,Xm,Xr[:,_REPOLK_IDX],Xd],1).astype("float32")
    return beats,feats0,y,pid,BEST
def _rhythm10(beats,feats0,pid,y):
    if "extract_rhythm_v2" not in globals(): exec(open(f"{_BASE}/colab_step49_rhythm2.py").read(), globals())
    return globals()["extract_rhythm_v2"](beats,feats0,pid,y,verbose=False)

def diag_noise():
    beats,feats0,y,pid,BEST=_bestF(); m1=np.isin(pid,_DS1); m2=np.isin(pid,_DS2); y1,y2=y[m1],y[m2]
    print("잔차 노이즈성격 계산...")
    Xn=extract_noise_features(beats,pid,y)
    def ev(X):
        sc=StandardScaler().fit(np.nan_to_num(X[m1])); X1=np.nan_to_num(sc.transform(np.nan_to_num(X[m1]))); X2=np.nan_to_num(sc.transform(np.nan_to_num(X[m2])))
        clf=LogisticRegression(max_iter=5000,C=0.5,class_weight={0:1,1:3,2:1.5}).fit(X1,y1)
        return average_precision_score((y2==1).astype(int),clf.predict_proba(X2)[:,1])
    bS=ev(BEST)
    print(f"\n=== 노이즈성격 7특징: 단일AUC / best 증분 (best S={bS:.4f}) ===")
    for k,nm in enumerate(NOISE_NAMES):
        c=Xn[m2,k]; a=roc_auc_score((y2==1).astype(int),c); a=max(a,1-a)
        S=ev(np.concatenate([BEST,Xn[:,[k]]],1))
        print(f"  {nm:16s}: AUC={a:.3f}  +best→{S:.4f} ({S-bS:+.4f}) {'★' if S>bS+1e-4 else ''}")
    print(f"  +노이즈7 전부 : S={ev(np.concatenate([BEST,Xn],1)):.4f}  (로지스틱은 과소평가—판정은 CNN)")
    global _NOISE; _NOISE=Xn; return Xn

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

def run_noise_cnn(seeds=None):
    import torch, torch.nn as nn, torch.nn.functional as Fn
    from sklearn.preprocessing import RobustScaler
    from sklearn.model_selection import GroupShuffleSplit
    seeds=seeds or list(range(1000,1015)); dev="cuda" if torch.cuda.is_available() else "cpu"
    beats,feats0,y,pid,BEST=_bestF(); ref=np.empty_like(beats)
    for p in np.unique(pid): m=pid==p; ref[m]=np.median(beats[m],0,keepdims=True)
    ref=ref.astype("float32")
    print("리듬10 + 노이즈7 계산...")
    R=_rhythm10(beats,feats0,pid,y); Xn=extract_noise_features(beats,pid,y)
    m1=np.isin(pid,_DS1); m2=np.isin(pid,_DS2); y2=y[m2]
    Sw=auto_weights(y[m1]); nc=np.array([(y[m1]==k).sum() for k in range(3)],np.float32); mc=(1.0/np.power(nc,0.25)); mc=(mc/mc.max()*0.5).astype("float32")
    CFG={"base+DTW":BEST,
         "+리듬10":np.concatenate([BEST,R],1).astype("float32"),
         "+리듬10+노이즈7":np.concatenate([BEST,R,Xn],1).astype("float32"),
         "+노이즈7만":np.concatenate([BEST,Xn],1).astype("float32")}
    print(f"margin CNN {len(seeds)}seed, Sw={Sw:.1f}")
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
                lo=M(bb,rr,ff); lg=lo-torch.zeros_like(lo).scatter_(1,yy[:,None],mcv[yy][:,None])
                ce=Fn.cross_entropy(lg,yy,reduction="none"); wv=cw[yy]; loss=(ce*wv).sum()/wv.sum()
                loss.backward(); torch.nn.utils.clip_grad_norm_(M.parameters(),1.0); opt.step()
            pv=pred(M,b1[va],r1[va],f1[va]); s,v=met(pv,y1[va])
            if 0.5*(s+v)>best: best=0.5*(s+v); bs={k:vv.cpu() for k,vv in M.state_dict().items()}
        M.load_state_dict(bs); return pred(M,b2,r2,f2)
    def trim(Pn):
        medS=np.median(Pn[:,:,1],0); corr=np.array([np.corrcoef(Pn[i,:,1],medS)[0,1] for i in range(len(Pn))])
        keep=np.argsort(-corr)[:max(1,int(round(len(Pn)*0.8)))]; P=Pn[keep].mean(0); return P/P.sum(1,keepdims=True)
    res={}
    for nm,F in CFG.items():
        Pt=trim(np.stack([train_one(F,s) for s in seeds],0)); S,V=met(Pt,y2); pr,se,f1=_f1(y2,Pt[:,1]); res[nm]=(S,pr,se,f1)
        print(f"  {nm:16s} S={S:.4f} PREC={pr:.3f} SEN={se:.3f} F1={f1:.3f}")
    b=res["+리듬10"]
    print(f"\n▶ +리듬10 대비 (노이즈성격이 리듬 위에 더 얹히나):")
    for nm,(S,pr,se,f1) in res.items():
        if nm=="+리듬10": continue
        print(f"  {nm:16s}: ΔS={S-b[0]:+.4f} ΔPREC={pr-b[1]:+.3f} ΔF1={f1-b[3]:+.3f}")
    print(f"\n  ★ +리듬10+노이즈7 이 +리듬10보다 PREC/S↑ = '노이즈다움 붕괴'가 추가정보(사장님 아이디어 성립).")
    return res
