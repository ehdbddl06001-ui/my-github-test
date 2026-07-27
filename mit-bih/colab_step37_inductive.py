# =============================================================================
#  colab_step37_inductive.py  —  [STEP 37] A(환자적응) vs B(완전 inductive) 기준 비교
#
#  방법론: A=주보고(라벨엄격 + 무라벨 개인 median ref = 표준 inter-patient).
#          B=강건성증명(DS2 완전 미사용: ref를 DS1 전역 정상 템플릿으로 → 완전 inductive).
#  '정상 대비' 특징(morph·repol·segT·VCG·DTW)은 ref에 의존 → A/B로 재추출해 격차 측정.
#  = median 개인적응이 버는 양 = B로 갈 때 페널티. (WST는 ref무관, 동일.)
#
#  선행 캐시(함수): extract_morpho_features, extract_repol_features, _WST
#                 (있으면) extract_segdev/segT, extract_vcg, extract_dtw
#  실행:
#    exec(open('/content/drive/MyDrive/mitbih/colab_step37_inductive.py').read())
#    diag_AB()
# =============================================================================
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.metrics import average_precision_score, precision_recall_curve

_DS1=[101,106,108,109,112,114,115,116,118,119,122,124,201,203,205,207,208,209,215,220,223,230]
_DS2=[100,103,105,111,113,117,121,123,200,202,210,212,213,214,219,221,222,228,231,232,233,234]
_REPOLK_IDX=[0,1,4,5]; _SEG_IDX=[9,10,8,4]

def _refA(beats,pid):                                   # 개인 median (무라벨 환자적응)
    r=np.empty_like(beats)
    for p in np.unique(pid): m=pid==p; r[m]=np.median(beats[m],axis=0,keepdims=True)
    return r.astype("float32")

def _refB(beats,y,pid):                                 # DS1 전역 정상 템플릿 (DS2 완전 미사용)
    m1=np.isin(pid,_DS1); tN=np.median(beats[m1&(y==0)],axis=0)   # (2,L)
    return np.tile(tN[None],(len(beats),1,1)).astype("float32")

def _f1(y2,s):
    p,r,_=precision_recall_curve((y2==1).astype(int),s); f=2*p*r/(p+r+1e-9); i=int(np.nanargmax(f)); return p[i],r[i],f[i]

def diag_AB(Kwst=40):
    d=np.load("/content/drive/MyDrive/mitbih/mamba_data.npz")
    beats,feats,y,pid=d["beat"],d["feats"],d["y"],d["pid"]
    m1=np.isin(pid,_DS1); m2=np.isin(pid,_DS2); y1,y2=y[m1],y[m2]
    Xw=globals()["_WST"]
    Xwk=np.nan_to_num(SelectKBest(f_classif,k=min(Kwst,Xw.shape[1])).fit(np.nan_to_num(Xw[m1]),y1).transform(np.nan_to_num(Xw)))
    refA=_refA(beats,pid); refB=_refB(beats,y,pid)
    emorph=globals()["extract_morpho_features"]; erepol=globals()["extract_repol_features"]
    eseg=globals().get("extract_segdev_features",None); evcg=globals().get("extract_vcg_features",None); edtw=globals().get("extract_dtw_features",None)
    def build(ref):
        Xm=emorph(beats,ref,pid); Xr=erepol(beats,ref,pid)
        best=np.concatenate([feats,Xwk,Xm,Xr[:,_REPOLK_IDX]],1)
        full=best
        if eseg is not None: full=np.concatenate([full,eseg(beats,ref,pid)[:,_SEG_IDX]],1)
        if evcg is not None: full=np.concatenate([full,evcg(beats,ref,pid)],1)
        if edtw is not None: full=np.concatenate([full,edtw(beats,ref,pid,y)],1)
        return best,full
    def S(X):
        sc=StandardScaler().fit(np.nan_to_num(X[m1])); X1=np.nan_to_num(sc.transform(np.nan_to_num(X[m1]))); X2=np.nan_to_num(sc.transform(np.nan_to_num(X[m2])))
        clf=LogisticRegression(max_iter=5000,C=0.5,class_weight={0:1,1:3,2:1.5}).fit(X1,y1)
        p2=clf.predict_proba(X2)[:,1]; pr,se,f1=_f1(y2,p2)
        return average_precision_score((y2==1).astype(int),p2),pr,se,f1
    print("=== A(개인 median ref) vs B(DS1 전역 정상 = 완전 inductive) — 로지스틱 ===")
    rows=[]
    for tag,ref in [("A 개인적응",refA),("B 완전inductive",refB)]:
        best,full=build(ref)
        bS=S(best); fS=S(full)
        rows.append((tag,bS,fS))
        print(f"[{tag}] best(26+WST+morph+repol): S={bS[0]:.4f} F1={bS[3]:.3f}   |  full(+segT/VCG/DTW): S={fS[0]:.4f} F1={fS[3]:.3f}")
    (_,bA,fA),(_,bB,fB)=rows[0],rows[1]
    print(f"\n▶ A−B 격차(개인적응 이득):  best {bA[0]-bB[0]:+.4f}   full {fA[0]-fB[0]:+.4f}")
    print(f"  격차 작으면 = 완전 inductive에서도 견고(논문 강한 주장).  크면 = 환자적응 의존도 큼.")
    print(f"  (로지스틱 근사 — 최종은 CNN A/B로 확인)")
    return rows
