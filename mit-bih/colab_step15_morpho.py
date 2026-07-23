# =============================================================================
#  colab_step15_morpho.py  —  [STEP 15] 적분(에너지) 기반 종합 형태 특징
#
#  사장님 아이디어: 적분=에너지. P/QRS/T 각 파동의 에너지(적분)와 지속시간·간격·
#  조기성·노이즈를 종합 분석. 전부 환자 정상(ref) 대비 = 개인 함수.
#  16개 특징: 에너지(적분)·에너지비·지속시간·PR간격(P-QRS)·조기P(PR편차)·RT·P진폭·노이즈.
#
#  ★ 핵심 검증 ★ 이미 통한 WST(+0.072)를 '넘어서' 정보를 더하는가?
#    로지스틱: 26 / morpho / 26+morpho / 26+WST / 26+WST+morpho 증분 비교.
#    26+WST+morpho > 26+WST 면 → morpho가 WST가 못 잡는 걸 추가(가치). 아니면 WST가 이미 커버.
#
#  선행(WST 비교 원하면): colab_step12_wst.py 로드해 _WST 캐시.
#  실행:
#    exec(open('/content/drive/MyDrive/mitbih/colab_step15_morpho.py').read())
#    diag_morpho()
# =============================================================================
import numpy as np
from scipy.ndimage import uniform_filter1d
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score, roc_auc_score

_DS1=[101,106,108,109,112,114,115,116,118,119,122,124,201,203,205,207,208,209,215,220,223,230]
_DS2=[100,103,105,111,113,117,121,123,200,202,210,212,213,214,219,221,222,228,231,232,233,234]
MORPHO_NAMES=["P/QRS에너지","T/QRS에너지","P에너지(정상대비)","QRS에너지(정상대비)","T에너지(정상대비)",
              "P지속","QRS지속","T지속","P지속(정상대비)","T지속(정상대비)",
              "PR간격(P-QRS)","조기P(PR편차)","RT간격","P진폭","노이즈","전체에너지(정상대비)"]

def _allbeat_median_ref(beats,pid):
    r=np.empty_like(beats)
    for p in np.unique(pid):
        m=pid==p; r[m]=np.median(beats[m],axis=0,keepdims=True)
    return r.astype("float32")

def extract_morpho_features(beats,refs,pid):
    """적분(에너지)+지속+간격 종합 형태특징. refs=환자 정상 기준(개인함수)."""
    N=len(beats); F=np.zeros((N,16),np.float32); eps=1e-6
    for p in np.unique(pid):
        idx=np.where(pid==p)[0]; b=beats[idx]; r=refs[idx]
        VMb=np.sqrt(b[:,0]**2+b[:,1]**2); VMr=np.sqrt(r[:,0]**2+r[:,1]**2)   # 벡터크기=순간 에너지
        L=VMb.shape[1]; R=int(np.argmax(VMr[0]))
        Qs,Qe=max(0,R-20),min(L,R+20); Ps,Pe=max(0,R-100),max(Qs- (0), R-25)
        if Pe-Ps<4: Ps,Pe=max(0,R-100),max(4,R-25)
        Ts,Te=min(L-4,R+25),min(L,R+140)
        E=lambda VM,s,e: VM[:,s:e].sum(1)                                    # 적분(에너지)
        def dur(VM,s,e,thr=0.3):
            seg=VM[:,s:e]; mx=seg.max(1,keepdims=True)+eps
            return (seg>thr*mx).sum(1).astype(np.float32)                    # 지속(에너지>임계 폭)
        pk=lambda VM,s,e: np.argmax(VM[:,s:e],1)
        qE,pE,tE=E(VMb,Qs,Qe),E(VMb,Ps,Pe),E(VMb,Ts,Te)
        qEr,pEr,tEr=E(VMr,Qs,Qe),E(VMr,Ps,Pe),E(VMr,Ts,Te)
        pdur,qdur,tdur=dur(VMb,Ps,Pe),dur(VMb,Qs,Qe),dur(VMb,Ts,Te)
        pdurr,tdurr=dur(VMr,Ps,Pe),dur(VMr,Ts,Te)
        ppk,ppkr,tpk=pk(VMb,Ps,Pe),pk(VMr,Ps,Pe),pk(VMb,Ts,Te)
        PR=(R-(Ps+ppk)).astype(np.float32); PRr=(R-(Ps+ppkr)).astype(np.float32)
        pamp=VMb[np.arange(len(idx)),(Ps+ppk).clip(0,L-1)]/(VMb[:,min(R,L-1)]+eps)
        sm=uniform_filter1d(VMb,size=7,axis=1); noise=np.abs(VMb-sm).sum(1)/(VMb.sum(1)+eps)  # 고주파 노이즈
        cols=[pE/(qE+eps), tE/(qE+eps), pE/(pEr+eps), qE/(qEr+eps), tE/(tEr+eps),
              pdur, qdur, tdur, pdur/(pdurr+eps), tdur/(tdurr+eps),
              PR, PR-PRr, ((Ts+tpk)-R).astype(np.float32), pamp, noise, VMb.sum(1)/(VMr.sum(1)+eps)]
        F[idx]=np.stack(cols,1)
    return np.nan_to_num(F,posinf=0,neginf=0).astype("float32")

def _load():
    d=np.load("/content/drive/MyDrive/mitbih/mamba_data.npz"); return d["beat"],d["feats"],d["y"],d["pid"]

def _ev(X,m1,m2,y1,y2):
    sc=StandardScaler().fit(np.nan_to_num(X[m1]))
    X1=np.nan_to_num(sc.transform(np.nan_to_num(X[m1]))); X2=np.nan_to_num(sc.transform(np.nan_to_num(X[m2])))
    clf=LogisticRegression(max_iter=5000,C=0.5,class_weight={0:1,1:3,2:1.5}).fit(X1,y1)
    p2=clf.predict_proba(X2)
    return average_precision_score((y2==1).astype(int),p2[:,1])

def diag_morpho():
    beats,feats,y,pid=_load()
    ref=_allbeat_median_ref(beats,pid)                    # label-free 정상 기준
    Xm=extract_morpho_features(beats,ref,pid)
    m1=np.isin(pid,_DS1); m2=np.isin(pid,_DS2); y1,y2=y[m1],y[m2]
    print("=== morpho 16특징 단변량 S ROC-AUC (DS2) ===")
    for k,nm in enumerate(MORPHO_NAMES):
        c=Xm[m2,k]
        if np.std(c)<1e-9: print(f"  {nm:16s}: (상수)"); continue
        a=roc_auc_score((y2==1).astype(int),c); a=max(a,1-a)
        print(f"  {nm:16s}: {a:.3f}  {'█'*int((a-0.5)*40)}")
    base=_ev(feats,m1,m2,y1,y2)
    print(f"\n=== DS1→DS2 로지스틱 증분 (기준 26개 S={base:.4f}) ===")
    rows=[("morpho16만",Xm),("26+morpho",np.concatenate([feats,Xm],1))]
    Xw=globals().get("_WST",None)
    if Xw is not None:
        from sklearn.feature_selection import SelectKBest,f_classif
        Xwk=np.nan_to_num(SelectKBest(f_classif,k=40).fit(np.nan_to_num(Xw[m1]),y1).transform(np.nan_to_num(Xw)))
        rows+=[("26+WST",np.concatenate([feats,Xwk],1)),
               ("26+WST+morpho",np.concatenate([feats,Xwk,Xm],1))]
    for nm,X in rows:
        S=_ev(X,m1,m2,y1,y2); print(f"  {nm:16s}: S={S:.4f}  (증분 {S-base:+.4f})")
    if Xw is not None:
        print("\n  ★ '26+WST+morpho' > '26+WST' 면 → morpho가 WST 못잡는 정보 추가(가치).")
    else:
        print("\n  (WST 비교하려면 colab_step12_wst.py 먼저 로드해 _WST 캐시)")
    global _MORPHO; _MORPHO=Xm
    return Xm
