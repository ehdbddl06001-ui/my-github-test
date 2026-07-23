# =============================================================================
#  colab_step32_synergy.py  —  [STEP 32] 백본 선정: Shapley 기여 + 시너지(교호) 분석
#
#  사장님 설계: ① 모든 조합서 공통 증가하는 조건 → 백본  ② 단독은 애매해도 특정 교집합이
#  보편적 시너지면 그 조합도 백본. 나머지(부분집단마다 갈리는 것)만 전문가 차별자.
#
#  도구: 조건 5개(WST·morph·repol·segT·xlead)의
#   · Shapley 값 = 모든 32조합 문맥의 평균 한계기여 (보편 도움 = 백본 후보)
#   · 부분집단(환자그룹)별 leave-one-out 부호 = 보편(+everywhere)이냐 조건부냐
#   · 시너지 행렬 = S(a+b)-S(a)-S(b)+base (교집합 교호작용)
#  → 백본 = base + (Shapley 높고 모든그룹 +) + (보편 시너지쌍).  나머지 = 차별자.
#
#  선행 캐시: _WST, _MORPHO, _REPOL, _SEGDEV, _XLEAD
#  실행:
#    exec(open('/content/drive/MyDrive/mitbih/colab_step32_synergy.py').read())
#    diag_synergy()
# =============================================================================
import math
import numpy as np
from itertools import combinations
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.metrics import average_precision_score

_DS1=[101,106,108,109,112,114,115,116,118,119,122,124,201,203,205,207,208,209,215,220,223,230]
_DS2=[100,103,105,111,113,117,121,123,200,202,210,212,213,214,219,221,222,228,231,232,233,234]
_REPOLK_IDX=[0,1,4,5]; _SEG_IDX=[9,10,8,4]

def _load():
    d=np.load("/content/drive/MyDrive/mitbih/mamba_data.npz"); return d["beat"],d["feats"],d["y"],d["pid"]

def diag_synergy(Kwst=40, ngroup=4):
    beats,feats0,y,pid=_load(); m1=np.isin(pid,_DS1); m2=np.isin(pid,_DS2); y1,y2=y[m1],y[m2]
    Xw=globals()["_WST"]; Xm=globals()["_MORPHO"]; Xr=globals()["_REPOL"]; Xs=globals()["_SEGDEV"]; Xx=globals()["_XLEAD"]
    Xwk=np.nan_to_num(SelectKBest(f_classif,k=40).fit(np.nan_to_num(Xw[m1]),y1).transform(np.nan_to_num(Xw)))
    COND={"WST":Xwk,"morph":Xm,"repol":Xr[:,_REPOLK_IDX],"segT":Xs[:,_SEG_IDX],"xlead":Xx}
    Xv=globals().get("_VCG",None)                          # step33 리드-벡터관계 — 있으면 시너지에 포함
    if Xv is not None: COND["VCG"]=Xv
    else: print("(주의: _VCG 없음 → step33 diag_vcg() 먼저 돌리면 VCG 포함해 재구성됨)\n")
    names=list(COND); n=len(names); memo={}
    def P(sub):
        key=tuple(sorted(sub))
        if key in memo: return memo[key]
        X=np.concatenate([feats0]+[COND[c] for c in key],1) if key else feats0
        sc=StandardScaler().fit(np.nan_to_num(X[m1]))
        X1=np.nan_to_num(sc.transform(np.nan_to_num(X[m1]))); X2=np.nan_to_num(sc.transform(np.nan_to_num(X[m2])))
        clf=LogisticRegression(max_iter=4000,C=0.5,class_weight={0:1,1:3,2:1.5}).fit(X1,y1)
        p2=clf.predict_proba(X2)[:,1]; memo[key]=p2; return p2
    AP=lambda mask,p: average_precision_score((y2[mask]==1).astype(int),p[mask]) if (y2[mask]==1).sum()>0 else np.nan
    S=lambda sub: average_precision_score((y2==1).astype(int),P(sub))
    base=S(())
    print(f"기준 26 S={base:.4f}\n")
    # ── Shapley ──
    print("=== 조건별 Shapley 기여 (모든 조합 문맥 평균) vs 단독증분 ===")
    phi={c:0.0 for c in names}
    for c in names:
        others=[x for x in names if x!=c]
        for k in range(len(others)+1):
            w=math.factorial(k)*math.factorial(n-k-1)/math.factorial(n)
            for sub in combinations(others,k): phi[c]+=w*(S(tuple(sub)+(c,))-S(tuple(sub)))
    for c in sorted(names,key=lambda z:-phi[z]):
        solo=S((c,))-base
        print(f"  {c:7s}: Shapley={phi[c]:+.4f}   단독증분={solo:+.4f}")
    # ── 부분집단(환자그룹)별 보편성: full - leave-one-out ──
    print(f"\n=== 보편성: {ngroup}개 환자그룹에서 leave-one-out 부호 (풀셋 대비) ===")
    pidg=pid[m2]; upat=np.array_split(np.unique(pidg),ngroup)
    gmask=[np.isin(pidg,g) for g in upat]
    pall=P(tuple(names))
    for c in names:
        pwoc=P(tuple(x for x in names if x!=c))
        margs=[AP(gm,pall)-AP(gm,pwoc) for gm in gmask]
        pos=sum(1 for mval in margs if mval>0)
        tag="보편(+전부)→백본" if pos==ngroup else ("조건부(갈림)→차별자" if 0<pos<ngroup else "보편해로움")
        print(f"  {c:7s}: 그룹부호 {['%+.3f'%mv for mv in margs]}  ({pos}/{ngroup}+)  {tag}")
    # ── 시너지(교호) 행렬 ──
    print(f"\n=== 시너지: S(a+b)-S(a)-S(b)+base  (>0=교집합 시너지) ===")
    for a,b in combinations(names,2):
        syn=S((a,b))-S((a,))-S((b,))+base
        if abs(syn)>0.005: print(f"  {a:6s}+{b:7s}: {syn:+.4f}  {'★시너지' if syn>0.01 else ('▽상쇄' if syn<-0.01 else '')}")
    print(f"\n  ★ Shapley 높고 '보편(+전부)'인 조건 = 백본.  '조건부(갈림)' = 전문가 차별자.")
    print(f"    ★시너지 쌍은 함께 백본 채택 검토.  (로지스틱 근사 → 최종은 CNN 확인)")
    return dict(shapley=phi,base=base)

def diag_combos(Kwst=40, top=18):
    """전체 조합 지형: 모든 2^n 부분집합 S(고차 3·4·5·6개 동시 포함) + 크기별 최고 + 고차시너지.
       _VCG 캐시 있으면 6조건 포함. 실행: diag_vcg() 먼저 → diag_combos()."""
    beats,feats0,y,pid=_load(); m1=np.isin(pid,_DS1); m2=np.isin(pid,_DS2); y1,y2=y[m1],y[m2]
    Xw=globals()["_WST"]; Xm=globals()["_MORPHO"]; Xr=globals()["_REPOL"]; Xs=globals()["_SEGDEV"]; Xx=globals()["_XLEAD"]
    Xwk=np.nan_to_num(SelectKBest(f_classif,k=40).fit(np.nan_to_num(Xw[m1]),y1).transform(np.nan_to_num(Xw)))
    COND={"WST":Xwk,"morph":Xm,"repol":Xr[:,_REPOLK_IDX],"segT":Xs[:,_SEG_IDX],"xlead":Xx}
    Xv=globals().get("_VCG",None)
    if Xv is not None: COND["VCG"]=Xv
    else: print("(주의: _VCG 없음 → diag_vcg() 먼저 돌리면 VCG 포함)\n")
    names=list(COND); memo={}
    def P(sub):
        key=tuple(sorted(sub))
        if key in memo: return memo[key]
        X=np.concatenate([feats0]+[COND[c] for c in key],1) if key else feats0
        sc=StandardScaler().fit(np.nan_to_num(X[m1]))
        X1=np.nan_to_num(sc.transform(np.nan_to_num(X[m1]))); X2=np.nan_to_num(sc.transform(np.nan_to_num(X[m2])))
        clf=LogisticRegression(max_iter=4000,C=0.5,class_weight={0:1,1:3,2:1.5}).fit(X1,y1)
        p2=clf.predict_proba(X2)[:,1]; memo[key]=p2; return p2
    S=lambda sub: average_precision_score((y2==1).astype(int),P(sub))
    base=S(()); solo={c:S((c,))-base for c in names}
    allsubs=[c for k in range(1,len(names)+1) for c in combinations(names,k)]
    res=sorted(((sub,S(sub)) for sub in allsubs), key=lambda x:-x[1])
    print(f"기준 26 S={base:.4f}   (전체 {len(allsubs)}조합, 조건 {len(names)}개)\n")
    print(f"=== 상위 {top} 조합 (S, 고차시너지=가법초과) ===")
    for sub,s in res[:top]:
        exc=s-base-sum(solo[c] for c in sub)
        print(f"  {'+'.join(sub):32s} S={s:.4f}  (고차시너지 {exc:+.4f})")
    print(f"\n=== 크기별 최고 조합 (동시 몇 개가 최적인가) ===")
    for k in range(1,len(names)+1):
        bs=max((c for c in combinations(names,k)),key=lambda c:S(c)); s=S(bs)
        exc=s-base-sum(solo[c] for c in bs)
        print(f"  {k}개: {'+'.join(bs):32s} S={s:.4f}  (고차시너지 {exc:+.4f})")
    best=res[0]
    print(f"\n▶ 전체 최고: {'+'.join(best[0])}  S={best[1]:.4f}")
    print(f"  크기별 최고가 계속 오르면 = 많이 넣을수록 좋음. 어느 크기서 꺾이면 = 그 조합이 백본.")
    print(f"  '고차시너지'가 큰 조합 = 개별 합보다 폭발(교집합 가치) → 백본 우선.")
    return res
