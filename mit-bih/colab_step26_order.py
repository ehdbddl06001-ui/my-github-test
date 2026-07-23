# =============================================================================
#  colab_step26_order.py  —  [STEP 26] '판단 순서' 효과 진단
#
#  질문: 조건(WST·morpho·repol)을 얹는/판단하는 순서를 바꾸면 결과가 바뀌나?
#  답의 핵심:
#   (A) 연결(concat)은 교환법칙 성립 → 순서 무관, 최종 S 동일. 중간 증분만 재배치.
#   (B) 그리디 순서 → 어느 조건이 '기반'이고 어느 게 '문맥 의존'인지 드러남.
#   (C) 순차(boosting)는 순서 민감 → A→B→C ≠ 다른 순서. 최고/최악 순서 + 평평연결 대비.
#
#  선행(캐시): _WST, _MORPHO, _REPOL (step12·15·18)
#  실행:
#    exec(open('/content/drive/MyDrive/mitbih/colab_step26_order.py').read())
#    diag_order()
# =============================================================================
import numpy as np
from itertools import permutations
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.metrics import average_precision_score

_DS1=[101,106,108,109,112,114,115,116,118,119,122,124,201,203,205,207,208,209,215,220,223,230]
_DS2=[100,103,105,111,113,117,121,123,200,202,210,212,213,214,219,221,222,228,231,232,233,234]
_REPOLK_IDX=[0,1,4,5]

def _load():
    d=np.load("/content/drive/MyDrive/mitbih/mamba_data.npz"); return d["beat"],d["feats"],d["y"],d["pid"]
def _sig(z): return 1/(1+np.exp(-z))

def _S3(X,m1,m2,y1,y2):
    """3-class 로지스틱 S PR-AUC (concat 평가용)."""
    sc=StandardScaler().fit(np.nan_to_num(X[m1]))
    X1=np.nan_to_num(sc.transform(np.nan_to_num(X[m1]))); X2=np.nan_to_num(sc.transform(np.nan_to_num(X[m2])))
    clf=LogisticRegression(max_iter=5000,C=0.5,class_weight={0:1,1:3,2:1.5}).fit(X1,y1)
    return average_precision_score((y2==1).astype(int),clf.predict_proba(X2)[:,1])

def _conditions():
    beats,feats,y,pid=_load(); m1=np.isin(pid,_DS1); m2=np.isin(pid,_DS2); y1=y[m1]
    Xw=globals().get("_WST",None); Xm=globals().get("_MORPHO",None); Xr=globals().get("_REPOL",None)
    assert Xw is not None and Xm is not None and Xr is not None, "step12·15·18 먼저 로드(_WST·_MORPHO·_REPOL)"
    Xwk=np.nan_to_num(SelectKBest(f_classif,k=40).fit(np.nan_to_num(Xw[m1]),y1).transform(np.nan_to_num(Xw))).astype("float32")
    COND={"WST":Xwk,"morph":Xm.astype("float32"),"repol":Xr[:,_REPOLK_IDX].astype("float32")}
    return feats.astype("float32"),COND,m1,m2,y

def _stagewise(order, feats, COND, m1, m2, y1, y2, lr=0.5, alpha=10.0):
    """순차 boosting: base(26) 로짓에서 시작, 조건을 순서대로 잔차(residual)에 적합해 더함.
       잔차가 이전 단계에 의존 → 순서 민감."""
    yb1=(y1==1).astype(float)
    sc=StandardScaler().fit(np.nan_to_num(feats[m1]))
    B1=np.nan_to_num(sc.transform(np.nan_to_num(feats[m1]))); B2=np.nan_to_num(sc.transform(np.nan_to_num(feats[m2])))
    clf=LogisticRegression(max_iter=5000,C=0.5,class_weight={0:1,1:3}).fit(B1,(y1==1).astype(int))
    F1=clf.decision_function(B1); F2=clf.decision_function(B2)
    for c in order:
        X=np.concatenate([feats,COND[c]],1)
        scx=StandardScaler().fit(np.nan_to_num(X[m1]))
        X1=np.nan_to_num(scx.transform(np.nan_to_num(X[m1]))); X2=np.nan_to_num(scx.transform(np.nan_to_num(X[m2])))
        resid=yb1-_sig(F1)                                   # 이전 단계가 못 맞춘 부분
        reg=Ridge(alpha=alpha).fit(X1,resid)
        F1=F1+lr*reg.predict(X1); F2=F2+lr*reg.predict(X2)
    return average_precision_score((y2==1).astype(int),_sig(F2))

def diag_order():
    feats,COND,m1,m2,y=_conditions(); y1,y2=y[m1],y[m2]; names=list(COND)
    base=_S3(feats,m1,m2,y1,y2)
    # ── (A) 연결 순서 무관 ──
    print(f"=== (A) 연결(concat) 순서별 누적 S  (기준 26 S={base:.4f}) ===")
    finals=[]
    for od in [["WST","morph","repol"],["repol","morph","WST"],["morph","WST","repol"],["repol","WST","morph"]]:
        cur=feats; path=[]
        for c in od: cur=np.concatenate([cur,COND[c]],1); path.append(_S3(cur,m1,m2,y1,y2))
        finals.append(path[-1]); print(f"   {' → '.join(od):24s}: "+"  ".join(f"{c}={p:.4f}" for c,p in zip(od,path)))
    print(f"   → 최종 S 모두 {np.mean(finals):.4f} (편차 {np.ptp(finals):.5f}) : 연결은 순서 무관. 증분만 재배치.")
    # ── (B) 그리디 최적 순서 ──
    print(f"\n=== (B) 그리디 순서 (매 단계 S 최대화) ===")
    cur=feats; rem=set(names); chosen=[]
    while rem:
        best=max(rem,key=lambda c:_S3(np.concatenate([cur,COND[c]],1),m1,m2,y1,y2))
        cur=np.concatenate([cur,COND[best]],1); s=_S3(cur,m1,m2,y1,y2); chosen.append((best,s)); rem.discard(best)
    prev=base
    for c,s in chosen: print(f"   +{c:6s} → S={s:.4f}  (문맥증분 {s-prev:+.4f})"); prev=s
    # ── (C) 순차(boosting) 순서 민감 ──
    flat=_S3(np.concatenate([feats]+[COND[c] for c in names],1),m1,m2,y1,y2)
    print(f"\n=== (C) 순차 boosting: 순서가 최종을 바꾸나?  (평평연결 all-in S={flat:.4f}) ===")
    res=[]
    for od in permutations(names):
        s=_stagewise(list(od),feats,COND,m1,m2,y1,y2); res.append((od,s))
    res.sort(key=lambda x:-x[1])
    for od,s in res: print(f"   {' → '.join(od):24s}: S={s:.4f}")
    print(f"   최고={' → '.join(res[0][0])} ({res[0][1]:.4f})  최악={' → '.join(res[-1][0])} ({res[-1][1]:.4f})  격차={res[0][1]-res[-1][1]:.4f}")
    print(f"   → 격차 크면 순차구조는 순서 민감. 최고순서가 평평연결({flat:.4f})보다 높으면 순차가 이득.")
    return dict(greedy=chosen,boost=res,flat=flat)
