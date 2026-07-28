# =============================================================================
#  colab_step33_vcg.py  —  [STEP 33] 개인화 분절별 리드-간 벡터관계(VCG) 특징
#
#  사장님 통찰: V1/V2/V5는 Lead II와 벡터 각도가 다 달라(step25 raw cross-lead 실패 원인).
#  해법: 각도·벡터관계로 변환 + '환자 정상 대비'. 환자마다 리드종류는 고정 → "이 비트의
#  리드간 각도가 그 환자 평소와 얼마나 다른가"는 리드종류 무관 = 교란 제거. 개인화가 핵심.
#
#  P·QRS·T 각 구간에서 두 리드(l0,l1)의:
#   · 전기축 각도(2D 주성분 방향) 정상대비 편차   · 벡터루프 면적(부호=회전, VCG) 정상대비
#   · 리드 비율 정상대비                          · 리드간 상관
#  = 12특징. 전부 개인 정상 대비. label-free.
#
#  ★ 검증: best(26+WST+morpho+repolK) 위 로지스틱 증분 + 단일특징 스캔. 살면 CNN 승격.
#  선행 캐시: _WST, _MORPHO, _REPOL
#  실행:
#    exec(open('/content/drive/MyDrive/mitbih/colab_step33_vcg.py').read())
#    diag_vcg()
# =============================================================================
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.metrics import average_precision_score, roc_auc_score

_DS1=[101,106,108,109,112,114,115,116,118,119,122,124,201,203,205,207,208,209,215,220,223,230]
_DS2=[100,103,105,111,113,117,121,123,200,202,210,212,213,214,219,221,222,228,231,232,233,234]
_REPOLK_IDX=[0,1,4,5]
VCG_NAMES=[f"{s}_{w}" for s in ["P","QRS","T"] for w in ["축각도편차","루프면적편차","리드비율편차","리드상관"]]

def _allbeat_median_ref(beats,pid):
    r=np.empty_like(beats)
    for p in np.unique(pid):
        m=pid==p; r[m]=np.median(beats[m],axis=0,keepdims=True)
    return r.astype("float32")

def extract_vcg_features(beats,refs,pid):
    """개인화 분절별 리드-간 벡터관계(축각도·루프면적·비율·상관)."""
    N=len(beats); F=np.zeros((N,12),np.float32); eps=1e-6
    def axis(l0,l1):                                   # 2D 주성분 방향각 [-pi/2,pi/2] (축=orientation)
        c00=(l0*l0).mean(-1); c11=(l1*l1).mean(-1); c01=(l0*l1).mean(-1)
        return 0.5*np.arctan2(2*c01,(c00-c11)+eps)
    def area(l0,l1):                                   # 벡터루프 부호면적(회전방향, VCG)
        return 0.5*(l0[...,:-1]*l1[...,1:]-l1[...,:-1]*l0[...,1:]).sum(-1)
    def corr(l0,l1):
        a=l0-l0.mean(-1,keepdims=True); b=l1-l1.mean(-1,keepdims=True)
        return (a*b).sum(-1)/(np.sqrt((a*a).sum(-1))*np.sqrt((b*b).sum(-1))+eps)
    def wrap(d): return (d+np.pi/2)%np.pi-np.pi/2       # 축각도 차이 [-pi/2,pi/2]로 감기
    for p in np.unique(pid):
        idx=np.where(pid==p)[0]; b=beats[idx]; rr=refs[idx[0]]
        VMr=np.sqrt(rr[0]**2+rr[1]**2); L=b.shape[2]; R=int(np.argmax(VMr))
        segs={"P":(max(0,R-70),max(4,R-25)),"QRS":(max(0,R-18),min(L,R+18)),"T":(min(L-4,R+25),min(L,R+120))}
        cols=[]
        for nm,(s,e) in segs.items():
            if e-s<5: s,e=max(0,R-18),min(L,R+18)
            bl0,bl1=b[:,0,s:e],b[:,1,s:e]; rl0,rl1=rr[0,s:e],rr[1,s:e]
            aB,aR=axis(bl0,bl1),axis(rl0[None],rl1[None])[0]
            arB,arR=area(bl0,bl1),area(rl0[None],rl1[None])[0]
            ratB=np.abs(bl1).sum(-1)/(np.abs(bl0).sum(-1)+eps); ratR=np.abs(rl1).sum()/(np.abs(rl0).sum()+eps)
            cols+=[wrap(aB-aR), arB-arR, ratB-ratR, corr(bl0,bl1)]
        F[idx]=np.stack(cols,1)
    return np.nan_to_num(F,posinf=0,neginf=0).astype("float32")

def _load():
    d=np.load("/content/drive/MyDrive/mitbih/mamba_data.npz"); return d["beat"],d["feats"],d["y"],d["pid"]
def _ev(X,m1,m2,y1,y2):
    sc=StandardScaler().fit(np.nan_to_num(X[m1]))
    X1=np.nan_to_num(sc.transform(np.nan_to_num(X[m1]))); X2=np.nan_to_num(sc.transform(np.nan_to_num(X[m2])))
    clf=LogisticRegression(max_iter=5000,C=0.5,class_weight={0:1,1:3,2:1.5}).fit(X1,y1)
    return average_precision_score((y2==1).astype(int),clf.predict_proba(X2)[:,1])

def diag_vcg():
    beats,feats,y,pid=_load(); ref=_allbeat_median_ref(beats,pid)
    Xv=extract_vcg_features(beats,ref,pid)
    m1=np.isin(pid,_DS1); m2=np.isin(pid,_DS2); y1,y2=y[m1],y[m2]
    print("=== VCG 12특징 단변량 S ROC-AUC (DS2) ===")
    for k,nm in enumerate(VCG_NAMES):
        c=Xv[m2,k]
        if np.std(c)<1e-9: print(f"  {nm:16s}: (상수)"); continue
        a=roc_auc_score((y2==1).astype(int),c); a=max(a,1-a); print(f"  {nm:16s}: {a:.3f}  {'█'*int((a-0.5)*40)}")
    base=_ev(feats,m1,m2,y1,y2)
    Xw=globals().get("_WST",None); Xm=globals().get("_MORPHO",None); Xr=globals().get("_REPOL",None)
    print(f"\n=== 로지스틱 증분 (기준 26 S={base:.4f}) ===")
    for nm,X in [("VCG12만",Xv),("26+VCG",np.concatenate([feats,Xv],1))]:
        print(f"  {nm:16s}: S={_ev(X,m1,m2,y1,y2):.4f}")
    if Xw is not None and Xm is not None and Xr is not None:
        Xwk=np.nan_to_num(SelectKBest(f_classif,k=40).fit(np.nan_to_num(Xw[m1]),y1).transform(np.nan_to_num(Xw)))
        BEST=np.concatenate([feats,Xwk,Xm,Xr[:,_REPOLK_IDX]],1); bS=_ev(BEST,m1,m2,y1,y2)
        print(f"  {'best':16s}: S={bS:.4f}")
        print(f"  {'best+VCG':16s}: S={_ev(np.concatenate([BEST,Xv],1),m1,m2,y1,y2):.4f}")
        print(f"\n=== best 위 단일특징 스캔 ===")
        for k,nm in enumerate(VCG_NAMES):
            S=_ev(np.concatenate([BEST,Xv[:,[k]]],1),m1,m2,y1,y2); print(f"  +{nm:16s}: {S:.4f} ({S-bS:+.4f})  {'★' if S>bS else ''}")
        print("\n  ★ best 위 부호일관·노이즈바닥 초과 특징 있으면 → 리드-벡터관계가 새 정보 → CNN 승격.")
    else:
        print("\n  (best 비교하려면 step12·15·18 먼저 로드)")
    global _VCG; _VCG=Xv
    return Xv
