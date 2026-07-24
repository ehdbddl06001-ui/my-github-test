# =============================================================================
#  colab_step52_newfeats.py  —  [STEP 52] 새 특징군 3종: Koopman/DMD · 개인정상AE · GNN구조
#
#  RHYTHM(시간 예측잔차)·NOISE(잔차성격)에 이어 서로 다른 축 3개:
#   · KOOPMAN(5) : 환자 정상 동역학을 선형연산자 A로 근사(DMD) → 예측잔차. RHYTHM의 연산자판.
#   · AE(5)      : DS1 정상비트로 conv denoising-AE 학습 → 재구성오차(형태 다양체 이탈).
#   · GNN(5)     : 환자별 kNN 그래프 구조통계(정상중심 거리·밀도·LOF). 관계 축, 학습X.
#  전부 개인화/자기지도라 inter-patient 깨끗(AE만 DS1 N라벨 사용, DS2는 통과만).
#
#  실행:
#    exec(open('/content/drive/MyDrive/mitbih/colab_step52_newfeats.py').read())
#    diag_newfeats()          # 3군 단일AUC + best 증분(참고). 캐시 _KOOPMAN,_AE,_GNN
# =============================================================================
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.metrics import average_precision_score, roc_auc_score

_BASE="/content/drive/MyDrive/mitbih"
_DS1=[101,106,108,109,112,114,115,116,118,119,122,124,201,203,205,207,208,209,215,220,223,230]
_DS2=[100,103,105,111,113,117,121,123,200,202,210,212,213,214,219,221,222,228,231,232,233,234]
_REPOLK_IDX=[0,1,4,5]
KOOP_NAMES=["예측잔차","P잔차비","예측코사인역","최대잔차","잔차백색성"]
AE_NAMES=["재구성MSE","P재구성","QRS재구성","T재구성","잠재이탈"]
GNN_NAMES=["정상중심거리","kNN밀도","kNN최대","LOF비","kNN분산"]

def _vm(beats): return np.sqrt(beats[:,0]**2+beats[:,1]**2).astype(np.float64)
def _resamp(V,L2):
    n,L=V.shape; x=np.linspace(0,L-1,L2); lo=np.floor(x).astype(int); hi=np.minimum(lo+1,L-1); fr=x-lo
    return V[:,lo]*(1-fr)+V[:,hi]*fr
def _zrow(X): return (X-X.mean(1,keepdims=True))/(X.std(1,keepdims=True)+1e-6)

# ─────────────── KOOPMAN / DMD ───────────────
def extract_koopman_features(beats, pid, y=None, L2=24, ridge=1e-2):
    N=len(beats); F=np.zeros((N,5),np.float32); eps=1e-6
    for p in np.unique(pid):
        idx=np.where(pid==p)[0]
        if len(idx)<5: continue
        X=_zrow(_resamp(_vm(beats[idx]),L2))                       # (n,L2) 비트형태 상태
        Xp,Xn=X[:-1],X[1:]                                         # 연속쌍
        G=Xp.T@Xp+ridge*np.eye(L2); A=np.linalg.solve(G,Xp.T@Xn)   # DMD: x_t ≈ x_{t-1}@A
        # robust 1-pass: 큰 잔차쌍 downweight 후 재적합
        r0=np.linalg.norm(Xn-Xp@A,axis=1); w=1.0/(1.0+ (r0/(np.median(r0)+eps))**2)
        Gw=(Xp*w[:,None]).T@Xp+ridge*np.eye(L2); A=np.linalg.solve(Gw,(Xp*w[:,None]).T@Xn)
        pred=Xp@A; res=Xn-pred                                     # (n-1,L2)  beat idx[1:]에 정렬
        rn=np.linalg.norm(res,axis=1)/(np.linalg.norm(Xn,axis=1)+eps)
        third=L2//3
        pr=np.abs(res[:,:third]).sum(1)/(np.abs(res).sum(1)+eps)
        cos=(Xn*pred).sum(1)/(np.linalg.norm(Xn,axis=1)*np.linalg.norm(pred,axis=1)+eps)
        mx=np.abs(res).max(1)
        wh=np.abs((res[:,1:]*res[:,:-1]).mean(1)/(res.var(1)+eps))
        F[idx[1:],0]=rn; F[idx[1:],1]=pr; F[idx[1:],2]=1-cos; F[idx[1:],3]=mx; F[idx[1:],4]=wh
    return np.nan_to_num(F,posinf=0,neginf=0).astype("float32")

# ─────────────── 개인 정상 AE (conv denoising) ───────────────
def extract_ae_features(beats, y, pid, epochs=20, bott=16, noise=0.1, seed=0):
    import torch, torch.nn as nn
    dev="cuda" if torch.cuda.is_available() else "cpu"
    N=len(beats); L=beats.shape[2]; m1=np.isin(pid,_DS1)
    Xb=beats.astype("float32").copy()
    mu=Xb.mean(2,keepdims=True); sd=Xb.std(2,keepdims=True)+1e-6; Xb=(Xb-mu)/sd    # 비트별 리드별 z
    class AE(nn.Module):
        def __init__(s):
            super().__init__()
            s.enc=nn.Sequential(nn.Conv1d(2,16,7,stride=2,padding=3),nn.ReLU(),
                                nn.Conv1d(16,32,5,stride=2,padding=2),nn.ReLU())    # (32, L/4)
            s.fl=L//4; s.tob=nn.Linear(32*s.fl,bott); s.fromb=nn.Linear(bott,32*s.fl)
            s.dec=nn.Sequential(nn.ConvTranspose1d(32,16,5,stride=2,padding=2,output_padding=1),nn.ReLU(),
                                nn.ConvTranspose1d(16,2,7,stride=2,padding=3,output_padding=1))
        def enc_z(s,x): return s.tob(s.enc(x).flatten(1))
        def forward(s,x):
            z=s.tob(s.enc(x).flatten(1)); h=s.fromb(z).view(-1,32,s.fl); return s.dec(h),z
    torch.manual_seed(seed); M=AE().to(dev); opt=torch.optim.AdamW(M.parameters(),1e-3,weight_decay=1e-5)
    tr=np.where(m1&(y==0))[0]                                       # DS1 정상만 학습
    Xt=torch.from_numpy(Xb[tr])
    dl=torch.utils.data.DataLoader(torch.utils.data.TensorDataset(Xt),batch_size=256,shuffle=True)
    for ep in range(epochs):
        M.train()
        for (xb,) in dl:
            xb=xb.to(dev); xn=xb+noise*torch.randn_like(xb)        # denoising
            rec,_=M(xn); loss=((rec-xb)**2).mean(); opt.zero_grad(); loss.backward(); opt.step()
    M.eval(); F=np.zeros((N,5),np.float32); Z=np.zeros((N,bott),np.float32)
    with torch.no_grad():
        for i in range(0,N,4096):
            xb=torch.from_numpy(Xb[i:i+4096]).to(dev); rec,z=M(xb)
            e=((rec-xb)**2).mean(1).cpu().numpy(); Z[i:i+4096]=z.cpu().numpy()      # (b,L) per-sample MSE
            F[i:i+4096,0]=e.mean(1)
            F[i:i+4096,1]=e[:,50:125].mean(1); F[i:i+4096,2]=e[:,125:175].mean(1); F[i:i+4096,3]=e[:,175:290].mean(1)
    cen=Z[m1&(y==0)].mean(0); F[:,4]=np.linalg.norm(Z-cen,axis=1)   # 정상 잠재중심 이탈
    return np.nan_to_num(F,posinf=0,neginf=0).astype("float32")

# ─────────────── GNN 구조특징 (kNN 그래프 통계) ───────────────
def extract_gnn_features(beats, pid, y=None, L2=24, k=10):
    from sklearn.neighbors import NearestNeighbors
    N=len(beats); F=np.zeros((N,5),np.float32); eps=1e-6
    for p in np.unique(pid):
        idx=np.where(pid==p)[0]; n=len(idx)
        if n<k+2: continue
        X=_zrow(_resamp(_vm(beats[idx]),L2)).astype("float32")
        F[idx,0]=np.linalg.norm(X-np.median(X,0,keepdims=True),axis=1)   # 정상중심(중앙값) 거리
        nn=NearestNeighbors(n_neighbors=k+1).fit(X); dist,nbr=nn.kneighbors(X)
        d=dist[:,1:]                                                    # self 제외
        md=d.mean(1); F[idx,1]=md; F[idx,2]=d[:,-1]                     # 밀도·k번째거리
        F[idx,3]=md/(md[nbr[:,1:]].mean(1)+eps)                         # LOF식 비
        F[idx,4]=d.std(1)
    return np.nan_to_num(F,posinf=0,neginf=0).astype("float32")

# ─────────────── 진단 ───────────────
def _bestF():
    d=np.load(f"{_BASE}/mamba_data.npz"); beats,feats0,y,pid=d["beat"],d["feats"],d["y"],d["pid"]; m1=np.isin(pid,_DS1)
    Xw=globals().get("_WST"); Xm=globals().get("_MORPHO"); Xr=globals().get("_REPOL"); Xd=globals().get("_DTW")
    Xwk=np.nan_to_num(SelectKBest(f_classif,k=min(40,Xw.shape[1])).fit(np.nan_to_num(Xw[m1]),y[m1]).transform(np.nan_to_num(Xw)))
    BEST=np.concatenate([feats0,Xwk,Xm,Xr[:,_REPOLK_IDX],Xd],1).astype("float32")
    return beats,feats0,y,pid,BEST

def diag_newfeats():
    beats,feats0,y,pid,BEST=_bestF(); m1=np.isin(pid,_DS1); m2=np.isin(pid,_DS2); y1,y2=y[m1],y[m2]
    print("KOOPMAN 계산..."); K=extract_koopman_features(beats,pid,y)
    print("AE 학습·계산(GPU)..."); A=extract_ae_features(beats,y,pid)
    print("GNN 계산..."); G=extract_gnn_features(beats,pid,y)
    def ev(X):
        sc=StandardScaler().fit(np.nan_to_num(X[m1])); X1=np.nan_to_num(sc.transform(np.nan_to_num(X[m1]))); X2=np.nan_to_num(sc.transform(np.nan_to_num(X[m2])))
        clf=LogisticRegression(max_iter=4000,C=0.5,class_weight={0:1,1:3,2:1.5}).fit(X1,y1)
        return average_precision_score((y2==1).astype(int),clf.predict_proba(X2)[:,1])
    bS=ev(BEST); print(f"\n(best S={bS:.4f}; 로지스틱은 innovation류 과소평가 — 최종은 sweep CNN)")
    for nm,mat,names in [("KOOPMAN",K,KOOP_NAMES),("AE",A,AE_NAMES),("GNN",G,GNN_NAMES)]:
        print(f"\n=== {nm} ===")
        for k,name in enumerate(names):
            c=mat[m2,k]; a=roc_auc_score((y2==1).astype(int),c); a=max(a,1-a)
            S=ev(np.concatenate([BEST,mat[:,[k]]],1))
            print(f"  {name:12s}: AUC={a:.3f}  +best→{S:.4f} ({S-bS:+.4f}) {'★' if S>bS+1e-4 else ''}")
        print(f"  +{nm} 전부: S={ev(np.concatenate([BEST,mat],1)):.4f}")
    global _KOOPMAN,_AE,_GNN; _KOOPMAN,_AE,_GNN=K,A,G
    return dict(KOOPMAN=K,AE=A,GNN=G)
