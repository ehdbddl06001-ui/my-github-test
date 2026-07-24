# =============================================================================
#  colab_step49_rhythm2.py  —  [STEP 49] 리듬 innovation 정제 + 실제 CNN 결정판정
#
#  STEP48: 타이밍 innovation 단일 AUC 역대최강(RR조기성abs 0.843, 보상성 0.804)인데
#  best 위 증분은 음수. 원인 (1)조기성이 feats0에 이미 있음=중복 (2)스케일 폭발(feats0[15]
#  innov=48만, MAD≈0 상수컬럼) → 선형모델 오염. → 정제 후 '실제 margin CNN'에서 재판정:
#   · robust: 스케일 바닥값 + tanh-squash로 폭발 제거(AUC 보존), 상수컬럼 자동배제
#   · margin CNN 15seed: base vs +타이밍3(정제) vs +전체 → S_PR·PREC·SEN·F1 + V_PR(보상성=S/V?)
#  로지스틱 증분(선형)이 아니라 비선형·정밀도·S/V로 봐야 진짜 기여를 안다.
#
#  선행 캐시: _WST,_MORPHO,_REPOL,_DTW  (recover/bootstrap)
#  실행:
#    exec(open('/content/drive/MyDrive/mitbih/colab_step49_rhythm2.py').read())
#    diag_rhythm2()             # 정제 특징 단일AUC + 자동식별 점검(폭발 사라졌나)
#    run_rhythm_cnn()           # 결정판정: 실제 margin CNN 15seed (느림)
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
RHY_NAMES=["형태잔차P","형태잔차T","형태잔차총","국소놀람K","예측상관역","형태점프",
           "RR조기성","RR조기성abs","보상휴지","보상성지수(S<<0)"]
_TIMING3=[7,8,9]   # RR조기성abs, 보상휴지, 보상성지수(강한 3)

def _ewma_causal(X, alpha):
    pred=np.zeros_like(X); acc=X[0].copy()
    for t in range(1,len(X)): pred[t]=acc; acc=alpha*X[t]+(1-alpha)*acc
    pred[0]=X[0]; return pred
def _segwin(R,L):
    return {"P":(max(0,R-90),max(3,R-25)),"QRS":(max(0,R-25),min(L,R+25)),"T":(min(L-2,R+30),min(L,R+130))}
def _f1(y2,s):
    p,r,_=precision_recall_curve((y2==1).astype(int),s); f=2*p*r/(p+r+1e-9); i=int(np.nanargmax(f)); return p[i],r[i],f[i]
def auto_weights(y1,beta=0.9999):
    nN=(y1==0).sum(); nS=max((y1==1).sum(),1); eff=lambda n:(1-beta)/(1-beta**n+1e-12); return float(eff(nS)/eff(nN))

def extract_rhythm_v2(beats, feats0, pid, y=None, alpha=0.3, K=8, verbose=True):
    """robust innovation: 스케일 바닥값 + tanh-squash(폭발 제거, AUC 보존), 상수컬럼 배제."""
    if y is None: y=np.load(f"{_BASE}/mamba_data.npz")["y"]
    N=len(beats); eps=1e-6; m1=np.isin(pid,_DS1); C=feats0.shape[1]
    # feats0 각 컬럼 인과 innovation + robust squash
    innovF=np.zeros_like(feats0,dtype=np.float32)
    # 전역 스케일(컬럼별 typical MAD) — 바닥값용
    gsc=np.zeros(C)
    perp_scale=np.zeros((len(np.unique(pid)),C))
    for pi,p in enumerate(np.unique(pid)):
        idx=np.where(pid==p)[0]; X=feats0[idx].astype(np.float64)
        perp_scale[pi]=np.median(np.abs(X-np.median(X,0,keepdims=True)),0)
    gsc=np.median(perp_scale,0)+eps                                   # 컬럼별 대표 스케일
    valid=gsc>1e-9                                                    # 상수(거의)컬럼 배제
    for p in np.unique(pid):
        idx=np.where(pid==p)[0]; X=feats0[idx].astype(np.float64)
        pred=_ewma_causal(X,alpha); res=X-pred
        sc=np.median(np.abs(X-np.median(X,0,keepdims=True)),0,keepdims=True)
        sc=np.maximum(sc, 0.2*gsc[None,:])                            # 스케일 바닥값(폭발 방지)
        innovF[idx]=np.tanh((res/(sc+eps))/3.0).astype(np.float32)    # tanh-squash → (-1,1)
    # pre/post 자동식별: 유효컬럼 중 DS1 S평균 innov 최소/최대
    meanS=np.array([innovF[m1&(y==1),c].mean() if valid[c] else 0.0 for c in range(C)])
    pre_col=int(np.argmin(meanS)); post_col=int(np.argmax(meanS))
    if verbose:
        print(f"  [자동식별v2] pre=feats0[{pre_col}] meanInnov@S={meanS[pre_col]:+.3f}  "
              f"post=feats0[{post_col}] meanInnov@S={meanS[post_col]:+.3f}  (폭발 없어야 정상, |·|<1)")
    F=np.zeros((N,10),np.float32)
    for p in np.unique(pid):
        idx=np.where(pid==p)[0]; b=beats[idx]
        VM=np.sqrt(b[:,0]**2+b[:,1]**2).astype(np.float64); L=VM.shape[1]
        R=int(np.argmax(np.median(VM,0))); w=_segwin(R,L)
        pred=_ewma_causal(VM,alpha); res=VM-pred
        qE=np.abs(VM[:,w["QRS"][0]:w["QRS"][1]]).sum(1)+eps
        F[idx,0]=np.abs(res[:,w["P"][0]:w["P"][1]]).sum(1)/qE
        F[idx,1]=np.abs(res[:,w["T"][0]:w["T"][1]]).sum(1)/qE
        F[idx,2]=np.abs(res).sum(1)/(np.abs(VM).sum(1)+eps)
        for i in range(len(idx)):
            lo=max(0,i-K); ref=np.median(VM[lo:i],0) if i>0 else VM[i]
            F[idx[i],3]=np.sqrt(((VM[i]-ref)**2).mean())/(np.sqrt((ref**2).mean())+eps)
        pm=pred-pred.mean(1,keepdims=True); vm=VM-VM.mean(1,keepdims=True)
        F[idx,4]=1-(pm*vm).sum(1)/(np.sqrt((pm**2).sum(1))*np.sqrt((vm**2).sum(1))+eps)
        F[idx,5]=np.abs(res).sum(1)/(np.abs(np.vstack([res[:1],res[:-1]])).sum(1)+eps)
        pr=innovF[idx,pre_col]; po=innovF[idx,post_col]
        F[idx,6]=pr; F[idx,7]=np.abs(pr); F[idx,8]=po; F[idx,9]=pr+po
    return np.nan_to_num(F,posinf=0,neginf=0).astype("float32")

def _bestF():
    d=np.load(f"{_BASE}/mamba_data.npz"); beats,feats0,y,pid=d["beat"],d["feats"],d["y"],d["pid"]
    m1=np.isin(pid,_DS1)
    Xw=globals().get("_WST"); Xm=globals().get("_MORPHO"); Xr=globals().get("_REPOL"); Xd=globals().get("_DTW")
    Xwk=np.nan_to_num(SelectKBest(f_classif,k=min(40,Xw.shape[1])).fit(np.nan_to_num(Xw[m1]),y[m1]).transform(np.nan_to_num(Xw)))
    BEST=np.concatenate([feats0,Xwk,Xm,Xr[:,_REPOLK_IDX],Xd],1).astype("float32")
    return beats,feats0,y,pid,BEST

def diag_rhythm2():
    beats,feats0,y,pid,BEST=_bestF()
    m1=np.isin(pid,_DS1); m2=np.isin(pid,_DS2); y1,y2=y[m1],y[m2]
    print("정제 리듬 innovation 계산...")
    Xrh=extract_rhythm_v2(beats,feats0,pid,y)
    def ev(X):
        sc=StandardScaler().fit(np.nan_to_num(X[m1])); X1=np.nan_to_num(sc.transform(np.nan_to_num(X[m1]))); X2=np.nan_to_num(sc.transform(np.nan_to_num(X[m2])))
        clf=LogisticRegression(max_iter=5000,C=0.5,class_weight={0:1,1:3,2:1.5}).fit(X1,y1)
        return average_precision_score((y2==1).astype(int),clf.predict_proba(X2)[:,1])
    bS=ev(BEST)
    print(f"\n=== 정제 10특징: 단일AUC / best 증분 (best S={bS:.4f}) ===")
    for k,nm in enumerate(RHY_NAMES):
        c=Xrh[m2,k]; a=roc_auc_score((y2==1).astype(int),c); a=max(a,1-a)
        S=ev(np.concatenate([BEST,Xrh[:,[k]]],1))
        print(f"  {nm:14s}: AUC={a:.3f}  +best→{S:.4f} ({S-bS:+.4f}) {'★' if S>bS+1e-4 else ''}")
    print(f"\n  +타이밍3(정제) : S={ev(np.concatenate([BEST,Xrh[:,_TIMING3]],1)):.4f}")
    print(f"  +전체10        : S={ev(np.concatenate([BEST,Xrh],1)):.4f}")
    print(f"\n  ★ 정제 후에도 증분 음수면 = 조기성은 feats0에 이미 흡수(진짜 중복). 양수면 스케일버그였음.")
    print(f"     최종 판정은 run_rhythm_cnn()의 PREC·V_PR로.")
    global _RHYTHM2; _RHYTHM2=Xrh
    return Xrh

# ─────────────── 결정판정: 실제 margin CNN 15seed ───────────────
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

def run_rhythm_cnn(seeds=None):
    import torch, torch.nn as nn, torch.nn.functional as Fn
    from sklearn.preprocessing import RobustScaler
    from sklearn.model_selection import GroupShuffleSplit
    seeds=seeds or list(range(1000,1015)); dev="cuda" if torch.cuda.is_available() else "cpu"
    beats,feats0,y,pid,BEST=_bestF(); ref=np.empty_like(beats)
    for p in np.unique(pid): m=pid==p; ref[m]=np.median(beats[m],0,keepdims=True)
    ref=ref.astype("float32")
    Xrh=extract_rhythm_v2(beats,feats0,pid,y,verbose=True)
    m1=np.isin(pid,_DS1); m2=np.isin(pid,_DS2); y2=y[m2]
    Sw=auto_weights(y[m1]); nc=np.array([(y[m1]==k).sum() for k in range(3)],np.float32); mc=(1.0/np.power(nc,0.25)); mc=(mc/mc.max()*0.5).astype("float32")
    CFG={"base(best+DTW)":BEST,
         "base+타이밍3":np.concatenate([BEST,Xrh[:,_TIMING3]],1).astype("float32"),
         "base+리듬10":np.concatenate([BEST,Xrh],1).astype("float32")}
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
        Pt=trim(np.stack([train_one(F,s) for s in seeds],0)); S,V=met(Pt,y2); pr,se,f1=_f1(y2,Pt[:,1]); res[nm]=(S,pr,se,f1,V)
        print(f"  {nm:16s} S={S:.4f} PREC={pr:.3f} SEN={se:.3f} F1={f1:.3f}  V_PR={V:.4f}")
    b=res["base(best+DTW)"]
    print(f"\n▶ base 대비:")
    for nm,(S,pr,se,f1,V) in res.items():
        if nm=="base(best+DTW)": continue
        print(f"  {nm:16s}: ΔS={S-b[0]:+.4f} ΔPREC={pr-b[1]:+.3f} ΔSEN={se-b[2]:+.3f} ΔF1={f1-b[3]:+.3f} ΔV_PR={V-b[4]:+.4f}")
    print(f"\n  ★ ΔPREC>0 = 조기성 확증이 N→S 오경보 기각(정밀도 기여). ΔV_PR>0 = 보상성지수가 S/V 분리 기여.")
    print(f"     둘 다 ≈0 이면 = 시퀀스 정보가 feats0에 완전 흡수(정직한 천장 확인).")
    return res
