# =============================================================================
#  colab_step38_stack2.py  —  [STEP 38] 정밀 스태킹: 확률보정 + 신뢰도-인지 메타
#
#  라우팅 3연속 실패(오라클↑ 정직↓). 원인: '선택'은 near-tie 노이즈에 취약.
#  → '결합'을 정밀화해 오라클(union 상한 0.82)에 최대한 접근:
#   ① 전문가 S확률 isotonic 보정(DS1 OOF) — 스케일 통일(안 하면 결합 손해)
#   ② 신뢰도-인지 메타특징: 보정S확률(K)·V확률(K) + [max·mean·std S, S>0.3 전문가수, 불일치] + 생리특징
#   ③ 메타모델(GBM)이 '언제 어느 전문가를 믿을지' 학습 → S 재판정
#  재학습 없음 — step31 experts.npz 재사용. DS1 라벨만(정직), DS2 평가만.
#
#  선행: run_specialist()가 experts.npz 저장. 캐시 _WST·_MORPHO·_REPOL·_SEGDEV (+_VCG·_DTW)
#  실행:
#    exec(open('/content/drive/MyDrive/mitbih/colab_step38_stack2.py').read())
#    run_stack2()
# =============================================================================
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.isotonic import IsotonicRegression
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.metrics import average_precision_score, precision_recall_curve

_DS1=[101,106,108,109,112,114,115,116,118,119,122,124,201,203,205,207,208,209,215,220,223,230]
_DS2=[100,103,105,111,113,117,121,123,200,202,210,212,213,214,219,221,222,228,231,232,233,234]
_SAVE="/content/drive/MyDrive/mitbih/ablation_step31"; _REPOLK_IDX=[0,1,4,5]; _SEG_IDX=[9,10,8,4]

def _f1(y2,s):
    p,r,_=precision_recall_curve((y2==1).astype(int),s); f=2*p*r/(p+r+1e-9); i=int(np.nanargmax(f)); return p[i],r[i],f[i]

def run_stack2(tauS=0.08, tauV=0.20, ambiguous_only=True):
    E=np.load(_SAVE+"/experts.npz")
    names=[k[4:] for k in E.files if k.startswith("oof_")]
    OA=np.stack([E[f"oof_{n}"] for n in names],0); DA=np.stack([E[f"ds2_{n}"] for n in names],0)
    y1=E["y1"]; y2=E["y2"]; K=len(names); N1=OA.shape[1]; N2=DA.shape[1]
    d=np.load("/content/drive/MyDrive/mitbih/mamba_data.npz"); beats,feats0,y,pid=d["beat"],d["feats"],d["y"],d["pid"]
    ref=np.empty_like(beats)
    for p in np.unique(pid): m=pid==p; ref[m]=np.median(beats[m],axis=0,keepdims=True)
    ref=ref.astype("float32")
    Xw=globals()["_WST"]; Xm=globals()["_MORPHO"]; Xr=globals()["_REPOL"]; Xs=globals()["_SEGDEV"]
    m1=np.isin(pid,_DS1); m2=np.isin(pid,_DS2)
    Xwk=np.nan_to_num(SelectKBest(f_classif,k=40).fit(np.nan_to_num(Xw[m1]),y[m1]).transform(np.nan_to_num(Xw)))
    G=np.concatenate([feats0,Xwk,Xm,Xr[:,_REPOLK_IDX],Xs[:,_SEG_IDX]],1)
    for nm in ["_VCG","_DTW"]:
        Xx=globals().get(nm,None)
        if Xx is not None: G=np.concatenate([G,Xx],1)
    G1=np.nan_to_num(G[m1]); G2=np.nan_to_num(G[m2])
    met=lambda s: average_precision_score((y2==1).astype(int),s)
    # ① isotonic 보정(DS1 OOF에서 학습 → 양쪽 적용)
    calO=np.zeros((K,N1)); calD=np.zeros((K,N2))
    for k in range(K):
        ir=IsotonicRegression(out_of_bounds="clip").fit(OA[k,:,1],(y1==1).astype(float))
        calO[k]=ir.predict(OA[k,:,1]); calD[k]=ir.predict(DA[k,:,1])
    # ② 신뢰도-인지 메타특징
    def meta(cal,A,Gd):
        S=cal.T                                            # (N,K) 보정 S확률
        extra=np.stack([S.max(1),S.mean(1),S.std(1),(S>0.3).sum(1),A[:,:,2].T.max(1)],1)  # max/mean/std/카운트/maxV
        return np.concatenate([S,A[:,:,2].T,extra,Gd],1)
    M1=meta(calO,OA,G1); M2=meta(calD,DA,G2)
    # ③ 메타모델 (애매 비트만 학습 권장 — N오염 제거)
    clearN=lambda A:(A[:,:,1].max(0)<tauS)&(A[:,:,2].max(0)<tauV)
    cN1,cN2=clearN(OA),clearN(DA); amb1,amb2=~cN1,~cN2
    tr=amb1 if ambiguous_only else np.ones(N1,bool)
    meta_clf=HistGradientBoostingClassifier(max_iter=400,learning_rate=0.05,max_leaf_nodes=31,l2_regularization=1.0,
                                            class_weight="balanced",random_state=0)
    meta_clf.fit(M1[tr],(y1[tr]==1).astype(int))
    stackS=calD.mean(0).copy()                             # 확실한N 기본=평균 보정S(낮음)
    stackS[amb2]=meta_clf.predict_proba(M2[amb2])[:,1]
    # 참고선
    best_single=max(range(K),key=lambda k:met(DA[k,:,1]))
    uni=DA[:,:,1].mean(0)
    maxvote=calD.max(0)                                    # 최대 보정S (고민감 결합)
    oracle=DA[DA[:,np.arange(N2),y2].argmax(0),np.arange(N2)][:,1]
    print(f"전문가 {K}개, 애매비트 학습={amb1.sum()}(S={int((amb1&(y1==1)).sum())})")
    print(f"\n{'='*54}\n[DS2] (스태킹=DS1라벨만, 오라클=DS2라벨 상한)")
    for nm,s in [(f"최고단일({names[best_single]})",DA[best_single,:,1]),("균일",uni),
                 ("보정 max-vote",maxvote),("★정밀 스태킹",stackS),("오라클(상한)",oracle)]:
        pr,se,f1=_f1(y2,s); print(f"  {nm:20s} S={met(s):.4f}  PREC={pr:.3f} SEN={se:.3f} F1={f1:.3f}")
    print(f"\n▶ ★정밀 스태킹이 최고단일 넘고 오라클 쪽으로 가면 = 보정+신뢰도결합이 병목 완화.")
    print(f"  단, MoE 전문가는 2-seed 약체 → 최종은 강한(15-seed) 전문가로 재확인 필요.")
    return dict(stackS=stackS, meta=meta_clf)
