# =============================================================================
#  colab_step35_dtw.py  —  [STEP 35] (나) DTW 탄력정렬: 조기성(모양=같음,타이밍=다름)
#
#  출처: DTW는 고전 시계열 정렬 알고리즘(Sakoe-Chiba, 음성인식). Farag 논문 아님.
#  우리 생리통찰(S=조기성=시간 당겨짐)에서 합성한 적응 — 환자 자기 정상과 DTW 정렬해
#  '워핑(타이밍 이탈)'을 조기성 척도로. 모양 vs 타이밍을 분리(아직 못 판 축).
#
#  6특징(P·QRS·T 각): · DTW거리(시간왜곡 허용 후 모양차) · 워핑이득=유클리드-DTW(순수 타이밍이탈)
#   워핑이득↑ = "모양은 정상인데 타이밍만 당겨짐"=S.  전부 환자 정상 대비, label-free.
#
#  ★ 검증: best 위 단일스캔 + _DTW 캐시(→ step32 diag_combos가 7조건으로 시너지 판단).
#  선행 캐시: _WST, _MORPHO, _REPOL (best 비교용)
#  실행:
#    exec(open('/content/drive/MyDrive/mitbih/colab_step35_dtw.py').read())
#    diag_dtw()          # 이후 step32 diag_combos() 하면 DTW 포함해 재구성
# =============================================================================
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.metrics import average_precision_score, roc_auc_score

_DS1=[101,106,108,109,112,114,115,116,118,119,122,124,201,203,205,207,208,209,215,220,223,230]
_DS2=[100,103,105,111,113,117,121,123,200,202,210,212,213,214,219,221,222,228,231,232,233,234]
_REPOLK_IDX=[0,1,4,5]
DTW_NAMES=[f"{s}_{w}" for s in ["P","QRS","T"] for w in ["DTW거리","워핑이득"]]

def _allbeat_median_ref(beats,pid):
    r=np.empty_like(beats)
    for p in np.unique(pid):
        m=pid==p; r[m]=np.median(beats[m],axis=0,keepdims=True)
    return r.astype("float32")

def _dtw_band(B, r, radius=8):
    """밴드제한 DTW, 비트축(n) 벡터화. B:(n,W) z-정규화, r:(W,) z-정규화 → dtw거리(n,)."""
    n,W=B.shape; INF=np.float32(1e18)
    prev=np.full((n,W+1),INF,np.float32); prev[:,0]=0.0                 # 행 i=0
    for i in range(1,W+1):
        cur=np.full((n,W+1),INF,np.float32)
        jlo=max(1,i-radius); jhi=min(W,i+radius)
        for j in range(jlo,jhi+1):
            c=np.abs(B[:,i-1]-r[j-1])
            cur[:,j]=c+np.minimum(np.minimum(prev[:,j],cur[:,j-1]),prev[:,j-1])
        prev=cur
    return prev[:,W]/W

def extract_dtw_features(beats,refs,pid,radius=8):
    """P·QRS·T 구간 DTW거리 + 워핑이득(유클리드-DTW=타이밍이탈). 전부 환자 정상 대비."""
    N=len(beats); F=np.zeros((N,6),np.float32); eps=1e-6
    def zn(x):                                                          # 구간 z-정규화(모양/타이밍만)
        return (x-x.mean(-1,keepdims=True))/(x.std(-1,keepdims=True)+eps)
    for p in np.unique(pid):
        idx=np.where(pid==p)[0]; b=beats[idx]
        VMb=np.sqrt(b[:,0]**2+b[:,1]**2); rr=refs[idx[0]]; VMr=np.sqrt(rr[0]**2+rr[1]**2)
        L=VMb.shape[1]; R=int(np.argmax(VMr))
        segs={"P":(max(0,R-70),max(6,R-25)),"QRS":(max(0,R-18),min(L,R+18)),"T":(min(L-6,R+25),min(L,R+120))}
        cols=[]
        for nm,(s,e) in segs.items():
            if e-s<6: s,e=max(0,R-18),min(L,R+18)
            bs=zn(VMb[:,s:e]); rs=zn(VMr[s:e][None])[0]
            dtw=_dtw_band(bs,rs,radius)
            eucl=np.sqrt(((bs-rs)**2).mean(-1))
            cols+=[dtw, eucl-dtw]                                       # 워핑이득 = 타이밍이탈
        F[idx]=np.stack(cols,1)
    return np.nan_to_num(F,posinf=0,neginf=0).astype("float32")

def _load():
    d=np.load("/content/drive/MyDrive/mitbih/mamba_data.npz"); return d["beat"],d["feats"],d["y"],d["pid"]
def _ev(X,m1,m2,y1,y2):
    sc=StandardScaler().fit(np.nan_to_num(X[m1]))
    X1=np.nan_to_num(sc.transform(np.nan_to_num(X[m1]))); X2=np.nan_to_num(sc.transform(np.nan_to_num(X[m2])))
    clf=LogisticRegression(max_iter=5000,C=0.5,class_weight={0:1,1:3,2:1.5}).fit(X1,y1)
    return average_precision_score((y2==1).astype(int),clf.predict_proba(X2)[:,1])

def diag_dtw():
    beats,feats,y,pid=_load(); ref=_allbeat_median_ref(beats,pid)
    Xd=extract_dtw_features(beats,ref,pid)
    m1=np.isin(pid,_DS1); m2=np.isin(pid,_DS2); y1,y2=y[m1],y[m2]
    print("=== DTW 6특징 단변량 S ROC-AUC (DS2) ===")
    for k,nm in enumerate(DTW_NAMES):
        c=Xd[m2,k]
        if np.std(c)<1e-9: print(f"  {nm:12s}: (상수)"); continue
        a=roc_auc_score((y2==1).astype(int),c); a=max(a,1-a); print(f"  {nm:12s}: {a:.3f}  {'█'*int((a-0.5)*40)}")
    base=_ev(feats,m1,m2,y1,y2)
    Xw=globals().get("_WST",None); Xm=globals().get("_MORPHO",None); Xr=globals().get("_REPOL",None)
    print(f"\n=== 로지스틱 증분 (기준 26 S={base:.4f}) ===")
    for nm,X in [("DTW6만",Xd),("26+DTW",np.concatenate([feats,Xd],1))]:
        print(f"  {nm:16s}: S={_ev(X,m1,m2,y1,y2):.4f}")
    if Xw is not None and Xm is not None and Xr is not None:
        Xwk=np.nan_to_num(SelectKBest(f_classif,k=40).fit(np.nan_to_num(Xw[m1]),y1).transform(np.nan_to_num(Xw)))
        BEST=np.concatenate([feats,Xwk,Xm,Xr[:,_REPOLK_IDX]],1); bS=_ev(BEST,m1,m2,y1,y2)
        print(f"  {'best':16s}: S={bS:.4f}")
        print(f"  {'best+DTW':16s}: S={_ev(np.concatenate([BEST,Xd],1),m1,m2,y1,y2):.4f}")
        print(f"\n=== best 위 단일특징 스캔 ===")
        for k,nm in enumerate(DTW_NAMES):
            S=_ev(np.concatenate([BEST,Xd[:,[k]]],1),m1,m2,y1,y2); print(f"  +{nm:12s}: {S:.4f} ({S-bS:+.4f})  {'★' if S>bS else ''}")
    print(f"\n  ★ _DTW 캐시됨 → step32 diag_combos() 하면 DTW 포함 7조건으로 시너지/조합 재구성.")
    global _DTW; _DTW=Xd
    return Xd
