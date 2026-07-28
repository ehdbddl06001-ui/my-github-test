# =============================================================================
#  colab_step35_dtw.py  —  [STEP 35 v2] DTW 조기성 + 클래스템플릿 판별 (정밀판)
#
#  v1: QRS_워핑이득 +0.123 (best 위 단일 역대최대). DTW=조기성/변행 축이 강함 → 정밀화:
#   ① 분절 세분화 P·PR·QRS·ST·T (5구간, 국소 워핑)
#   ② ★DTW 클래스템플릿 판별자: dtw(자기정상) + dtw(N템플릿) + [dtwN-dtwS]=시간왜곡 허용 S닮음
#      (Farag whole-beat MF는 QRS공유로 죽었지만, DTW로 시간불변 매치드필터 부활)
#   ③ 구간 고정길이 리샘플(템플릿 비교 안정)
#  15특징(5구간×[자기DTW거리, 워핑이득, S-N판별]). 템플릿=DS1만(라벨 정당), label-free 추론.
#
#  ★ 검증: best 위 단일스캔 + _DTW 캐시(→ step32/31/36에서 사용).
#  선행 캐시(비교용): _WST, _MORPHO, _REPOL
#  실행:
#    exec(open('/content/drive/MyDrive/mitbih/colab_step35_dtw.py').read())
#    diag_dtw()
# =============================================================================
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.metrics import average_precision_score, roc_auc_score

_DS1=[101,106,108,109,112,114,115,116,118,119,122,124,201,203,205,207,208,209,215,220,223,230]
_DS2=[100,103,105,111,113,117,121,123,200,202,210,212,213,214,219,221,222,228,231,232,233,234]
_REPOLK_IDX=[0,1,4,5]
_SEG_ORDER=["P","PR","QRS","ST","T"]
DTW_NAMES=[f"{s}_{w}" for s in _SEG_ORDER for w in ["자기DTW","워핑이득","S-N판별"]]
_LSEG=32   # 구간 리샘플 길이

def _allbeat_median_ref(beats,pid):
    r=np.empty_like(beats)
    for p in np.unique(pid):
        m=pid==p; r[m]=np.median(beats[m],axis=0,keepdims=True)
    return r.astype("float32")

def _resamp_mat(w,L=_LSEG):
    x=np.linspace(0,w-1,L); lo=np.floor(x).astype(int); hi=np.minimum(lo+1,w-1); fr=x-lo
    M=np.zeros((L,w),np.float32); M[np.arange(L),lo]+=1-fr; M[np.arange(L),hi]+=fr; return M

def _zn(x): return (x-x.mean(-1,keepdims=True))/(x.std(-1,keepdims=True)+1e-6)

def _dtw_band(B, r, radius=6):
    """밴드제한 DTW, 비트축 벡터화. B:(n,L) r:(L,) → 거리(n,)."""
    n,W=B.shape; INF=np.float32(1e18)
    prev=np.full((n,W+1),INF,np.float32); prev[:,0]=0.0
    for i in range(1,W+1):
        cur=np.full((n,W+1),INF,np.float32); jlo=max(1,i-radius); jhi=min(W,i+radius)
        for j in range(jlo,jhi+1):
            c=np.abs(B[:,i-1]-r[j-1])
            cur[:,j]=c+np.minimum(np.minimum(prev[:,j],cur[:,j-1]),prev[:,j-1])
        prev=cur
    return prev[:,W]/W

def _segwin(R,L):
    return {"P":(max(0,R-70),max(6,R-32)),"PR":(max(0,R-32),max(8,R-12)),"QRS":(max(0,R-14),min(L,R+14)),
            "ST":(min(L-6,R+14),min(L,R+45)),"T":(min(L-6,R+45),min(L,R+120))}

def extract_dtw_features(beats,refs,pid,y=None,radius=6):
    """5구간 × [자기정상 DTW거리, 워핑이득, N/S템플릿 판별]. 템플릿=DS1."""
    if y is None: y=np.load("/content/drive/MyDrive/mitbih/mamba_data.npz")["y"]
    N=len(beats); nseg=len(_SEG_ORDER); F=np.zeros((N,nseg*3),np.float32); eps=1e-6
    m1=np.isin(pid,_DS1)
    # 1) 모든 비트의 구간 리샘플·z정규 VM 을 먼저 계산(템플릿용)
    SEGZ={s:np.zeros((N,_LSEG),np.float32) for s in _SEG_ORDER}
    Mcache={}
    for p in np.unique(pid):
        idx=np.where(pid==p)[0]; b=beats[idx]; VMb=np.sqrt(b[:,0]**2+b[:,1]**2)
        rr=refs[idx[0]]; VMr=np.sqrt(rr[0]**2+rr[1]**2); L=VMb.shape[1]; R=int(np.argmax(VMr))
        for s,(a,e) in _segwin(R,L).items():
            if e-a<4: a,e=max(0,R-14),min(L,R+14)
            w=e-a
            if w not in Mcache: Mcache[w]=_resamp_mat(w)
            SEGZ[s][idx]=_zn(VMb[:,a:e]@Mcache[w].T)
    # 2) 클래스 템플릿(DS1 N/S 중앙값) + 각 구간 특징
    for si,s in enumerate(_SEG_ORDER):
        Z=SEGZ[s]
        tN=np.median(Z[m1&(y==0)],0); tS=np.median(Z[m1&(y==1)],0)
        dN=_dtw_band(Z,tN,radius); dS=_dtw_band(Z,tS,radius)
        F[:,si*3+2]=dN-dS                                   # S-N판별(>0 = S 더 닮음)
    # 3) 자기 정상(ref) 대비 DTW·워핑이득 (구간별, 환자별 ref 리샘플)
    for p in np.unique(pid):
        idx=np.where(pid==p)[0]; b=beats[idx]; VMb=np.sqrt(b[:,0]**2+b[:,1]**2)
        rr=refs[idx[0]]; VMr=np.sqrt(rr[0]**2+rr[1]**2); L=VMb.shape[1]; R=int(np.argmax(VMr))
        for si,s in enumerate(_SEG_ORDER):
            a,e=_segwin(R,L)[s]
            if e-a<4: a,e=max(0,R-14),min(L,R+14)
            w=e-a; M=Mcache[w]
            bz=_zn(VMb[:,a:e]@M.T); rz=_zn((VMr[a:e]@M.T)[None])[0]
            dtw=_dtw_band(bz,rz,radius); eucl=np.sqrt(((bz-rz)**2).mean(-1))
            F[idx,si*3]=dtw; F[idx,si*3+1]=eucl-dtw
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
    Xd=extract_dtw_features(beats,ref,pid,y)
    m1=np.isin(pid,_DS1); m2=np.isin(pid,_DS2); y1,y2=y[m1],y[m2]
    print("=== DTW 15특징 단변량 S ROC-AUC (DS2) ===")
    for k,nm in enumerate(DTW_NAMES):
        c=Xd[m2,k]
        if np.std(c)<1e-9: print(f"  {nm:12s}: (상수)"); continue
        a=roc_auc_score((y2==1).astype(int),c); a=max(a,1-a); print(f"  {nm:12s}: {a:.3f}  {'█'*int((a-0.5)*40)}")
    base=_ev(feats,m1,m2,y1,y2)
    Xw=globals().get("_WST",None); Xm=globals().get("_MORPHO",None); Xr=globals().get("_REPOL",None)
    print(f"\n=== 로지스틱 증분 (기준 26 S={base:.4f}) ===")
    for nm,X in [("DTW15만",Xd),("26+DTW",np.concatenate([feats,Xd],1))]:
        print(f"  {nm:16s}: S={_ev(X,m1,m2,y1,y2):.4f}")
    if Xw is not None and Xm is not None and Xr is not None:
        Xwk=np.nan_to_num(SelectKBest(f_classif,k=40).fit(np.nan_to_num(Xw[m1]),y1).transform(np.nan_to_num(Xw)))
        BEST=np.concatenate([feats,Xwk,Xm,Xr[:,_REPOLK_IDX]],1); bS=_ev(BEST,m1,m2,y1,y2)
        print(f"  {'best':16s}: S={bS:.4f}")
        print(f"  {'best+DTW':16s}: S={_ev(np.concatenate([BEST,Xd],1),m1,m2,y1,y2):.4f}")
        print(f"\n=== best 위 단일특징 스캔 ===")
        for k,nm in enumerate(DTW_NAMES):
            S=_ev(np.concatenate([BEST,Xd[:,[k]]],1),m1,m2,y1,y2); print(f"  +{nm:12s}: {S:.4f} ({S-bS:+.4f})  {'★' if S>bS else ''}")
    print(f"\n  ★ _DTW 캐시됨(15특징) → step32 diag_combos()/step31/36에서 사용.")
    global _DTW; _DTW=Xd
    return Xd
