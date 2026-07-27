# =============================================================================
#  colab_step17_mf.py  —  [STEP 17] 매치드 필터(Matched Filter) 특징
#
#  Farag 2023: DS1 클래스 템플릿으로 초기화한 non-trainable Conv1D = matched filtering
#  → inter-patient SVEB F1 ~0.82 (마킹·SMOTE 없음). 비학습 템플릿=일반화(우리 AdaBN 교훈과 일치).
#
#  구현(우리 세팅): DS1에서 N/S/V 클래스별 템플릿 K개(kmeans) → 각 beat와 정규화 상호상관
#  → "N/S/V 형태 닮음" 특징. inter-patient 정당(템플릿=DS1 라벨만, DS2 라벨 미사용).
#  검증: 26 / MF / 26+MF / (있으면)26+WST+morpho / +MF  로지스틱 증분.
#
#  선행(비교 원하면): colab_step12_wst.py(_WST), colab_step15_morpho.py(_MORPHO)
#  실행:
#    exec(open('/content/drive/MyDrive/mitbih/colab_step17_mf.py').read())
#    diag_mf()
# =============================================================================
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.metrics import average_precision_score, roc_auc_score

_DS1=[101,106,108,109,112,114,115,116,118,119,122,124,201,203,205,207,208,209,215,220,223,230]
_DS2=[100,103,105,111,113,117,121,123,200,202,210,212,213,214,219,221,222,228,231,232,233,234]

def _load():
    d=np.load("/content/drive/MyDrive/mitbih/mamba_data.npz"); return d["beat"],d["feats"],d["y"],d["pid"]

def build_templates(beats, y, train_mask, n_per_class=8):
    """DS1(train)에서 클래스별 매치드필터 템플릿 K개 (both-lead 정규화 파형)."""
    X=beats.reshape(len(beats),-1).astype("float32")
    Xn=X/(np.linalg.norm(X,axis=1,keepdims=True)+1e-8)
    T={}
    for c in [0,1,2]:
        idx=np.where(train_mask&(y==c))[0]
        k=min(n_per_class,max(1,len(idx)//50))
        km=KMeans(n_clusters=k,n_init=4,random_state=0).fit(Xn[idx])
        C=km.cluster_centers_; T[c]=C/(np.linalg.norm(C,axis=1,keepdims=True)+1e-8)
    return T,Xn

def extract_mf_features(Xn,T):
    """각 beat와 N/S/V 템플릿의 최대 정규화 상호상관(=matched filter 출력) + 마진."""
    cN=(Xn@T[0].T).max(1); cS=(Xn@T[1].T).max(1); cV=(Xn@T[2].T).max(1)
    F=np.stack([cN,cS,cV, cS-cN, cS-cV, cV-cN, cS-np.maximum(cN,cV)],1)  # 7 특징
    return np.nan_to_num(F).astype("float32")

def _ev(X,m1,m2,y1,y2):
    sc=StandardScaler().fit(np.nan_to_num(X[m1]))
    X1=np.nan_to_num(sc.transform(np.nan_to_num(X[m1]))); X2=np.nan_to_num(sc.transform(np.nan_to_num(X[m2])))
    clf=LogisticRegression(max_iter=5000,C=0.5,class_weight={0:1,1:3,2:1.5}).fit(X1,y1)
    p2=clf.predict_proba(X2); return average_precision_score((y2==1).astype(int),p2[:,1])

def diag_mf(n_per_class=8):
    beats,feats,y,pid=_load()
    m1=np.isin(pid,_DS1); m2=np.isin(pid,_DS2); y1,y2=y[m1],y[m2]
    T,Xn=build_templates(beats,y,m1,n_per_class)                 # 템플릿=DS1만
    Xmf=extract_mf_features(Xn,T)
    print("=== MF 7특징 단변량 S ROC-AUC (DS2) ===")
    for k,nm in enumerate(["N상관","S상관","V상관","S-N","S-V","V-N","S-max(N,V)"]):
        a=roc_auc_score((y2==1).astype(int),Xmf[m2,k]); a=max(a,1-a); print(f"  {nm:10s}: {a:.3f}  {'█'*int((a-0.5)*40)}")
    base=_ev(feats,m1,m2,y1,y2)
    print(f"\n=== DS1→DS2 로지스틱 증분 (기준 26 S={base:.4f}) ===")
    rows=[("MF만",Xmf),("26+MF",np.concatenate([feats,Xmf],1))]
    Xw=globals().get("_WST",None); Xm=globals().get("_MORPHO",None)
    if Xw is not None and Xm is not None:
        Xwk=np.nan_to_num(SelectKBest(f_classif,k=40).fit(np.nan_to_num(Xw[m1]),y1).transform(np.nan_to_num(Xw)))
        WM=np.concatenate([feats,Xwk,Xm],1)
        rows+=[("26+WST+morpho",WM),("26+WST+morpho+MF",np.concatenate([WM,Xmf],1))]
    for nm,X in rows:
        print(f"  {nm:18s}: S={_ev(X,m1,m2,y1,y2):.4f}  (증분 {_ev(X,m1,m2,y1,y2)-base:+.4f})")
    if Xw is not None:
        print("\n  ★ '+MF' > '26+WST+morpho' 면 → MF가 또 다른 정보 추가.")
    global _MF; _MF=Xmf
    return Xmf
