# =============================================================================
#  colab_step25_xlead.py  —  [STEP 25] 새 정보 축: 리드 간 전도 시간차(cross-lead lag)
#
#  재조합은 ~0.68 천장. 0.68을 넘으려면 새 정보. 이 축은 기존이 구조적으로 못 담음:
#   · morpho·repol은 VM=√(l0²+l1²) 위 계산 → 두 리드 상대 위상/시간차를 버림.
#   · WST는 translation-invariant, 26개는 비트별 스칼라 → 리드 간 lag 없음.
#  이소성 비트는 전기축·활성화 순서가 바뀜 → 리드 간 lag/coherence 변화. 파형만 필요(자체완결).
#
#  9특징: (P·QRS·T 구간별) 리드0↔리드1 정규화 상호상관의 최적 lag & 최대 coherence
#         + lag의 환자정상(ref) 대비. 전부 label-free.
#  ★ 검증: 우리 최고 특징집합(26+WST+morpho+repolK) '위에' 새 정보를 더하나?
#    로지스틱 증분: 26 / xlead / 26+xlead / best / best+xlead.  best+xlead>best 면 가치.
#
#  선행(캐시): _WST, extract_morpho_features/_MORPHO, extract_repol_features/_REPOL
#  실행:
#    exec(open('/content/drive/MyDrive/mitbih/colab_step25_xlead.py').read())
#    diag_xlead()
# =============================================================================
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.metrics import average_precision_score, roc_auc_score

_DS1=[101,106,108,109,112,114,115,116,118,119,122,124,201,203,205,207,208,209,215,220,223,230]
_DS2=[100,103,105,111,113,117,121,123,200,202,210,212,213,214,219,221,222,228,231,232,233,234]
_REPOLK_IDX=[0,1,4,5]
XLEAD_NAMES=["P_lag","P_coh","QRS_lag","QRS_coh","T_lag","T_coh","P_lag(정상대비)","QRS_lag(정상대비)","T_lag(정상대비)"]

def _xcorr_lag(a,b,maxlag=12):
    """행별(비트별) 리드0(a)↔리드1(b) 정규화 상호상관의 (최적 lag, 최대 coherence)."""
    eps=1e-6; a=a-a.mean(1,keepdims=True); b=b-b.mean(1,keepdims=True)
    a=a/(a.std(1,keepdims=True)+eps); b=b/(b.std(1,keepdims=True)+eps); W=a.shape[1]
    best=np.full(len(a),-2.0,np.float32); lag=np.zeros(len(a),np.float32)
    for L in range(-maxlag,maxlag+1):
        if L>=0: c=(a[:,L:]*b[:,:W-L]).mean(1)
        else:    c=(a[:,:W+L]*b[:,-L:]).mean(1)
        m=c>best; best[m]=c[m].astype(np.float32); lag[m]=L
    return lag,best

def _allbeat_median_ref(beats,pid):
    r=np.empty_like(beats)
    for p in np.unique(pid):
        m=pid==p; r[m]=np.median(beats[m],axis=0,keepdims=True)
    return r.astype("float32")

def extract_xlead_features(beats,refs,pid,maxlag=12):
    """리드 간 lag/coherence 9특징 (P·QRS·T 구간). refs=환자 정상 기준."""
    N=len(beats); F=np.zeros((N,9),np.float32)
    for p in np.unique(pid):
        idx=np.where(pid==p)[0]; b=beats[idx]; r=refs[idx]
        VMr=np.sqrt(r[:,0]**2+r[:,1]**2); L=b.shape[2]; R=int(np.argmax(VMr[0]))
        wins={"P":(max(0,R-100),max(4,R-25)),"QRS":(max(0,R-15),min(L,R+15)),"T":(min(L-4,R+25),min(L,R+120))}
        col={}
        for nm,(s,e) in wins.items():
            if e-s<6: s,e=max(0,R-15),min(L,R+15)
            lg,co=_xcorr_lag(b[:,0,s:e],b[:,1,s:e],maxlag)
            lgr,_=_xcorr_lag(r[:,0,s:e],r[:,1,s:e],maxlag)
            col[nm+"_lag"]=lg; col[nm+"_coh"]=co; col[nm+"_lagN"]=lg-lgr
        F[idx]=np.stack([col["P_lag"],col["P_coh"],col["QRS_lag"],col["QRS_coh"],
                         col["T_lag"],col["T_coh"],col["P_lagN"],col["QRS_lagN"],col["T_lagN"]],1)
    return np.nan_to_num(F,posinf=0,neginf=0).astype("float32")

def _load():
    d=np.load("/content/drive/MyDrive/mitbih/mamba_data.npz"); return d["beat"],d["feats"],d["y"],d["pid"]

def _ev(X,m1,m2,y1,y2):
    sc=StandardScaler().fit(np.nan_to_num(X[m1]))
    X1=np.nan_to_num(sc.transform(np.nan_to_num(X[m1]))); X2=np.nan_to_num(sc.transform(np.nan_to_num(X[m2])))
    clf=LogisticRegression(max_iter=5000,C=0.5,class_weight={0:1,1:3,2:1.5}).fit(X1,y1)
    return average_precision_score((y2==1).astype(int),clf.predict_proba(X2)[:,1])

def diag_xlead(maxlag=12):
    beats,feats,y,pid=_load()
    ref=_allbeat_median_ref(beats,pid)
    Xx=extract_xlead_features(beats,ref,pid,maxlag)
    m1=np.isin(pid,_DS1); m2=np.isin(pid,_DS2); y1,y2=y[m1],y[m2]
    print("=== xlead 9특징 단변량 S ROC-AUC (DS2) ===")
    for k,nm in enumerate(XLEAD_NAMES):
        c=Xx[m2,k]
        if np.std(c)<1e-9: print(f"  {nm:14s}: (상수)"); continue
        a=roc_auc_score((y2==1).astype(int),c); a=max(a,1-a)
        print(f"  {nm:14s}: {a:.3f}  {'█'*int((a-0.5)*40)}")
    base=_ev(feats,m1,m2,y1,y2)
    print(f"\n=== DS1→DS2 로지스틱 증분 (기준 26 S={base:.4f}) ===")
    rows=[("xlead9만",Xx),("26+xlead",np.concatenate([feats,Xx],1))]
    Xw=globals().get("_WST",None); Xm=globals().get("_MORPHO",None); Xr=globals().get("_REPOL",None)
    if Xw is not None and Xm is not None and Xr is not None:
        Xwk=np.nan_to_num(SelectKBest(f_classif,k=40).fit(np.nan_to_num(Xw[m1]),y1).transform(np.nan_to_num(Xw)))
        BEST=np.concatenate([feats,Xwk,Xm,Xr[:,_REPOLK_IDX]],1)      # 26+WST+morpho+repolK (최고)
        rows+=[("best(26+WST+mor+rep)",BEST),("best+xlead",np.concatenate([BEST,Xx],1))]
    for nm,X in rows:
        S=_ev(X,m1,m2,y1,y2); print(f"  {nm:22s}: S={S:.4f}  (증분 {S-base:+.4f})")
    if Xw is not None:
        print("\n  ★ 'best+xlead' > 'best' 면 → 리드간 lag가 기존이 못 담은 새 정보 추가(→CNN 검증).")
    else:
        print("\n  (best 비교하려면 step12·15·18 먼저 로드해 _WST·_MORPHO·_REPOL 캐시)")
    global _XLEAD; _XLEAD=Xx
    return Xx
