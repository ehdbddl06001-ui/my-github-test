# =============================================================================
#  colab_step24_knn.py  —  [STEP 24] DS2 비트별 국소 최적 Fn조합 (DS1 kNN) + 선택 견고화
#
#  STEP23 발견: 전축 MoE(게이트)=0.688(최고급)·oracle 0.714 가능. 단 '조합 선택'이
#  단일 split 과적합으로 고장(wst 단독 0.493만 집음). → 두 가지로 해결:
#   (A) 전역 조합선택 견고화: 환자 K-fold CV로 채점 → 최고 조합 DS2 적용 (버그 수정).
#   (B) 사장님 아이디어: DS2 비트마다 가장 닮은 DS1 이웃을 찾아, 그 이웃에서 가장 잘 맞은
#       Fn 조합을 사용(비트별 국소 최적조합). hard(최적) + soft(국소역량 가중).
#  전부 DS1 라벨·특징으로만 조합 결정, DS2는 평가만(비누출). 재학습 없음(experts.npz 재사용).
#
#  선행: run_moe()가 ablation_step23/experts.npz 저장했어야 함. 캐시 _MORPHO·_REPOL 권장.
#  실행:
#    exec(open('/content/drive/MyDrive/mitbih/colab_step24_knn.py').read())
#    run_knn(k=300)
# =============================================================================
import numpy as np
from itertools import combinations
from sklearn.metrics import average_precision_score
from sklearn.preprocessing import RobustScaler
from sklearn.neighbors import NearestNeighbors
from sklearn.model_selection import GroupKFold

_DS1=[101,106,108,109,112,114,115,116,118,119,122,124,201,203,205,207,208,209,215,220,223,230]
_DS2=[100,103,105,111,113,117,121,123,200,202,210,212,213,214,219,221,222,228,231,232,233,234]
_SAVE="/content/drive/MyDrive/mitbih/ablation_step23"
NAMES=["base","wst","morph","repol"]

def _S(P,y): return average_precision_score((y==1).astype(int),P[:,1])
def _V(P,y): return average_precision_score((y==2).astype(int),P[:,2])
def _norm(P): return P/P.sum(-1,keepdims=True)
def _combos(): return [c for k in range(1,len(NAMES)+1) for c in combinations(NAMES,k)]
def _cpred(preds,sub): return np.mean([preds[n] for n in sub],axis=0)   # 조합 내부=균일평균

def _feats():
    """유사도용 형태특징 G=morpho+repol (표준화 전)."""
    d=np.load("/content/drive/MyDrive/mitbih/mamba_data.npz")
    beats,pid=d["beat"],d["pid"]
    Xm=globals().get("_MORPHO",None); Xr=globals().get("_REPOL",None)
    if Xm is None or Xr is None:
        r=np.empty_like(beats)
        for p in np.unique(pid):
            m=pid==p; r[m]=np.median(beats[m],axis=0,keepdims=True)
        r=r.astype("float32")
        Xm=Xm if Xm is not None else extract_morpho_features(beats,r,pid)
        Xr=Xr if Xr is not None else extract_repol_features(beats,r,pid)
    return np.concatenate([Xm,Xr],1).astype("float32"),pid

def run_knn(k=300, temp=0.02, nfold=5):
    e=np.load(_SAVE+"/experts.npz")
    oof={n:e[f"oof_{n}"] for n in NAMES}; ds2={n:e[f"ds2_{n}"] for n in NAMES}
    y1,y2,p1=e["y1"],e["y2"],e["p1"]
    G,pid=_feats(); m1=np.isin(pid,_DS1); m2=np.isin(pid,_DS2)
    sc=RobustScaler().fit(np.nan_to_num(G[m1]))
    g1=np.nan_to_num(sc.transform(np.nan_to_num(G[m1])),posinf=0,neginf=0)
    g2=np.nan_to_num(sc.transform(np.nan_to_num(G[m2])),posinf=0,neginf=0)
    subs=_combos()
    Coof={s:_cpred(oof,s) for s in subs}; Cds2={s:_cpred(ds2,s) for s in subs}
    # ── (A) 전역 조합선택: 환자 K-fold CV S ──
    gkf=GroupKFold(nfold)
    cvS={s:np.mean([_S(Coof[s][fb],y1[fb]) for _,fb in gkf.split(Coof[s],y1,p1)]) for s in subs}
    ordG=sorted(subs,key=lambda s:-cvS[s]); bestG=ordG[0]
    print("=== (A) 전역 조합선택 (DS1 환자 K-fold CV) 상위 6 ===")
    for s in ordG[:6]: print(f"   {'+'.join(s):20s}  CV-S={cvS[s]:.4f}   DS2-S={_S(Cds2[s],y2):.4f}")
    # ── (B) 비트별 국소조합: DS2 비트 → DS1 kNN → 이웃서 S 변별 최고 조합 ──
    # ★ 역량 = 국소 '균형' 정답도 = 0.5·(S이웃 평균 S확률) + 0.5·(비S이웃 평균 (1-S확률)).
    #   (단순 정답도는 다수(N)에 지배돼 'S 안부르는' 전문가가 이김 → S 변별로 교정)
    nn=NearestNeighbors(n_neighbors=k).fit(g1); _,idx=nn.kneighbors(g2)             # (N2,k)
    yn=y1[idx]; mS=(yn==1); nS=np.maximum(mS.sum(1),1); nO=np.maximum((~mS).sum(1),1)  # (N2,k),(N2,)
    def _localbal(SP):                                                              # SP:(N1,) S확률 → (N2,) 균형역량
        spn=SP[idx]
        return 0.5*(spn*mS).sum(1)/nS + 0.5*((1-spn)*(~mS)).sum(1)/nO
    loc=np.stack([_localbal(Coof[s][:,1]) for s in subs],1)                         # (N2,15)
    Cds2arr=np.stack([Cds2[s] for s in subs],0)                                     # (15,N2,3)
    pick=loc.argmax(1); Phard=Cds2arr[pick,np.arange(len(y2))]                      # hard: 국소 최적조합
    w=np.exp((loc-loc.max(1,keepdims=True))/temp); w=w/w.sum(1,keepdims=True)       # soft: 역량 softmax
    Psoft=_norm(np.einsum('jc,cjk->jk',w,Cds2arr))
    # 참고: 전문가 4개 직접 국소 soft 게이트
    locE=np.stack([_localbal(oof[n][:,1]) for n in NAMES],1)
    wE=np.exp((locE-locE.max(1,keepdims=True))/temp); wE=wE/wE.sum(1,keepdims=True)
    Eds2=np.stack([ds2[n] for n in NAMES],0); Pexp=_norm(np.einsum('jc,cjk->jk',wE,Eds2))
    # ── 비교 ──
    print(f"\n=== (B) 비트별 국소 kNN (k={k}) ===")
    print(f"   국소조합 hard        DS2-S={_S(Phard,y2):.4f}  V={_V(Phard,y2):.4f}")
    print(f"   국소조합 soft        DS2-S={_S(Psoft,y2):.4f}  V={_V(Psoft,y2):.4f}")
    print(f"   국소 전문가4 soft게이트 DS2-S={_S(Pexp,y2):.4f}  V={_V(Pexp,y2):.4f}")
    # 비트별로 실제 뽑힌 조합 분포
    from collections import Counter
    top=Counter('+'.join(subs[p]) for p in pick).most_common(5)
    print("   국소 hard가 고른 조합 상위:", ", ".join(f"{c}({n})" for c,n in top))
    print(f"\n=== 기준선 ===")
    print(f"   단일 wst             DS2-S={_S(ds2['wst'],y2):.4f}")
    print(f"   균일평균 4축          DS2-S={_S(_cpred(ds2,tuple(NAMES)),y2):.4f}")
    print(f"   ★(A)전역CV선택[{'+'.join(bestG)}] DS2-S={_S(Cds2[bestG],y2):.4f}")
    print(f"   (step23 전축게이트 0.688 / oracle 0.714 가 외부 기준)")
    best=max([("A전역CV",_S(Cds2[bestG],y2)),("B국소hard",_S(Phard,y2)),
              ("B국소soft",_S(Psoft,y2)),("B전문가soft",_S(Pexp,y2))],key=lambda x:x[1])
    print(f"\n▶ 최고: {best[0]} S={best[1]:.4f}")
    print("   국소(B)가 전역(A)보다 높으면 = 비트별 최적조합이 실제로 다름(사장님 가설 성립).")
    return dict(bestG=bestG,cvS=cvS,Phard=Phard,Psoft=Psoft,Pexp=Pexp,pick=pick)
