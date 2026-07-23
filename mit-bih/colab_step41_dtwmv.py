# =============================================================================
#  colab_step41_dtwmv.py  —  [STEP 41] 다변량(2-리드) DTW — 사장님 아이디어
#
#  현 DTW는 VM=√(l0²+l1²) 1D → 두 리드 관계를 뭉개 버림. 사장님 제안:
#  각 시점을 2D 점 (leadII, V1)로 → 국소거리 √((Δl0)²+(Δl1)²) → 리드 간 관계 유지 + 시간왜곡.
#  = VCG(리드벡터)+DTW(탄력정렬) 융합. "lead II 정상인데 V1 이상"을 평면거리로 포착.
#
#  15특징(5구간×[자기DTW, 워핑이득, S-N판별]) — VM 대신 2-리드. 전부 개인정상 대비, 템플릿=DS1.
#  ★ 검증: best 위 로지스틱에서 VM-DTW vs 2D-DTW 직접 비교 + 단일스캔.
#  선행 캐시: _WST, _MORPHO, _REPOL (best), (있으면) extract_dtw_features(VM 비교용)
#  실행:
#    exec(open('/content/drive/MyDrive/mitbih/colab_step41_dtwmv.py').read())
#    diag_dtwmv()
# =============================================================================
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.metrics import average_precision_score, roc_auc_score

_DS1=[101,106,108,109,112,114,115,116,118,119,122,124,201,203,205,207,208,209,215,220,223,230]
_DS2=[100,103,105,111,113,117,121,123,200,202,210,212,213,214,219,221,222,228,231,232,233,234]
_REPOLK_IDX=[0,1,4,5]; _SEG=["P","PR","QRS","ST","T"]; _LSEG=32
DTWMV_NAMES=[f"{s}_{w}" for s in _SEG for w in ["자기DTW","워핑이득","S-N판별"]]

def _allbeat_median_ref(beats,pid):
    r=np.empty_like(beats)
    for p in np.unique(pid):
        m=pid==p; r[m]=np.median(beats[m],axis=0,keepdims=True)
    return r.astype("float32")

def _resamp(seg,L=_LSEG):                        # seg (...,w) → (...,L) 선형 리샘플
    w=seg.shape[-1]; x=np.linspace(0,w-1,L); lo=np.floor(x).astype(int); hi=np.minimum(lo+1,w-1); fr=x-lo
    return seg[...,lo]*(1-fr)+seg[...,hi]*fr

def _zn(x): return (x-x.mean(-1,keepdims=True))/(x.std(-1,keepdims=True)+1e-6)

def _dtw_mv(B, r, radius=6):
    """다변량 밴드 DTW. B:(n,C,L) r:(C,L) → 거리(n,). 국소거리=채널 유클리드."""
    n,C,W=B.shape; INF=np.float32(1e18)
    prev=np.full((n,W+1),INF,np.float32); prev[:,0]=0.0
    for i in range(1,W+1):
        cur=np.full((n,W+1),INF,np.float32); jlo=max(1,i-radius); jhi=min(W,i+radius)
        for j in range(jlo,jhi+1):
            c=np.sqrt(((B[:,:,i-1]-r[:,j-1])**2).sum(1))     # (n,) 채널 간 유클리드
            cur[:,j]=c+np.minimum(np.minimum(prev[:,j],cur[:,j-1]),prev[:,j-1])
        prev=cur
    return prev[:,W]/W

def _segwin(R,L):
    return {"P":(max(0,R-70),max(6,R-32)),"PR":(max(0,R-32),max(8,R-12)),"QRS":(max(0,R-14),min(L,R+14)),
            "ST":(min(L-6,R+14),min(L,R+45)),"T":(min(L-6,R+45),min(L,R+120))}

def extract_dtwmv_features(beats,refs,pid,y=None,radius=6):
    """2-리드 다변량 DTW: 5구간×[자기DTW, 워핑이득, S-N판별]. 채널=(leadII, V1)."""
    if y is None: y=np.load("/content/drive/MyDrive/mitbih/mamba_data.npz")["y"]
    N=len(beats); F=np.zeros((N,len(_SEG)*3),np.float32); eps=1e-6; m1=np.isin(pid,_DS1)
    # 구간별 리샘플·리드별 z정규 (n,2,L)
    SEGZ={s:np.zeros((N,2,_LSEG),np.float32) for s in _SEG}
    for p in np.unique(pid):
        idx=np.where(pid==p)[0]; b=beats[idx]; rr=refs[idx[0]]
        VMr=np.sqrt(rr[0]**2+rr[1]**2); L=b.shape[2]; R=int(np.argmax(VMr))
        for s,(a,e) in _segwin(R,L).items():
            if e-a<4: a,e=max(0,R-14),min(L,R+14)
            seg=_resamp(b[:,:,a:e])                         # (n,2,L)
            SEGZ[s][idx]=np.stack([_zn(seg[:,0]),_zn(seg[:,1])],1)
    # 클래스 템플릿(DS1 N/S 중앙값) + S-N판별
    for si,s in enumerate(_SEG):
        Z=SEGZ[s]                                            # (N,2,L)
        tN=np.median(Z[m1&(y==0)],0); tS=np.median(Z[m1&(y==1)],0)   # (2,L)
        F[:,si*3+2]=_dtw_mv(Z,tN,radius)-_dtw_mv(Z,tS,radius)
    # 자기 정상 대비 자기DTW·워핑이득
    for p in np.unique(pid):
        idx=np.where(pid==p)[0]; rr=refs[idx[0]]
        VMr=np.sqrt(rr[0]**2+rr[1]**2); L=rr.shape[1]; R=int(np.argmax(VMr))
        for si,s in enumerate(_SEG):
            a,e=_segwin(R,L)[s]
            if e-a<4: a,e=max(0,R-14),min(L,R+14)
            bz=SEGZ[s][idx]                                  # (n,2,L)
            rz=np.stack([_zn(_resamp(rr[0,a:e])[None])[0],_zn(_resamp(rr[1,a:e])[None])[0]],0)  # (2,L)
            dtw=_dtw_mv(bz,rz,radius); eucl=np.sqrt(((bz-rz[None])**2).sum(1).mean(-1))
            F[idx,si*3]=dtw; F[idx,si*3+1]=eucl-dtw
    return np.nan_to_num(F,posinf=0,neginf=0).astype("float32")

def _load():
    d=np.load("/content/drive/MyDrive/mitbih/mamba_data.npz"); return d["beat"],d["feats"],d["y"],d["pid"]
def _ev(X,m1,m2,y1,y2):
    sc=StandardScaler().fit(np.nan_to_num(X[m1]))
    X1=np.nan_to_num(sc.transform(np.nan_to_num(X[m1]))); X2=np.nan_to_num(sc.transform(np.nan_to_num(X[m2])))
    clf=LogisticRegression(max_iter=5000,C=0.5,class_weight={0:1,1:3,2:1.5}).fit(X1,y1)
    return average_precision_score((y2==1).astype(int),clf.predict_proba(X2)[:,1])

def diag_dtwmv():
    beats,feats,y,pid=_load(); ref=_allbeat_median_ref(beats,pid)
    Xmv=extract_dtwmv_features(beats,ref,pid,y)
    m1=np.isin(pid,_DS1); m2=np.isin(pid,_DS2); y1,y2=y[m1],y[m2]
    print("=== 2D-DTW 15특징 단변량 S ROC-AUC (DS2) ===")
    for k,nm in enumerate(DTWMV_NAMES):
        c=Xmv[m2,k]
        if np.std(c)<1e-9: print(f"  {nm:12s}: (상수)"); continue
        a=roc_auc_score((y2==1).astype(int),c); a=max(a,1-a); print(f"  {nm:12s}: {a:.3f}  {'█'*int((a-0.5)*40)}")
    Xw=globals().get("_WST"); Xm=globals().get("_MORPHO"); Xr=globals().get("_REPOL")
    Xwk=np.nan_to_num(SelectKBest(f_classif,k=40).fit(np.nan_to_num(Xw[m1]),y1).transform(np.nan_to_num(Xw)))
    BEST=np.concatenate([feats,Xwk,Xm,Xr[:,_REPOLK_IDX]],1); bS=_ev(BEST,m1,m2,y1,y2)
    print(f"\n=== 로지스틱: VM-DTW vs 2D-DTW (best S={bS:.4f}) ===")
    print(f"  best+2D-DTW      : S={_ev(np.concatenate([BEST,Xmv],1),m1,m2,y1,y2):.4f}")
    Xvm=globals().get("_DTW",None)
    if Xvm is not None:
        print(f"  best+VM-DTW(기존) : S={_ev(np.concatenate([BEST,Xvm],1),m1,m2,y1,y2):.4f}")
        print(f"  best+둘다         : S={_ev(np.concatenate([BEST,Xvm,Xmv],1),m1,m2,y1,y2):.4f}")
    print(f"\n=== best 위 2D-DTW 단일스캔 ===")
    for k,nm in enumerate(DTWMV_NAMES):
        S=_ev(np.concatenate([BEST,Xmv[:,[k]]],1),m1,m2,y1,y2); print(f"  +{nm:12s}: {S:.4f} ({S-bS:+.4f})  {'★' if S>bS else ''}")
    print(f"\n  ★ 2D-DTW > VM-DTW 면 = 리드관계 유지가 이득(사장님 아이디어 성립) → CNN 승격.")
    global _DTWMV; _DTWMV=Xmv
    return Xmv
