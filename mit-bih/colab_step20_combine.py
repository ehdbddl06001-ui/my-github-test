# =============================================================================
#  colab_step20_combine.py  —  [STEP 20] base+repolK 풀 합의 가중(붕괴 판단·재가중)
#
#  STEP19: +repolK가 새 최고(트림0.680)지만 seed 양극단 — 1001은 base가 최고인데
#  repolK서 붕괴, 1012는 반대. '어느 seed가 좋은지가 feature set마다 다름'.
#  → base 15 + repolK 15 = 30 풀로 합치고, label-free 합의로 좋은 것만 골라 가중.
#    (DS2 라벨 미사용. 붕괴 판단 = 다른 모델 합의와의 어긋남 + 신호 붕괴(저분산).)
#
#  재학습 없음 — step19가 저장한 per-seed 예측을 읽어 조합만.
#  선행: run_repolk() 가 ablation_step19/wm.npz·wmr.npz 를 저장했어야 함.
#  실행:
#    exec(open('/content/drive/MyDrive/mitbih/colab_step20_combine.py').read())
#    run_combine()
# =============================================================================
import os
import numpy as np
from sklearn.metrics import average_precision_score

_SAVE="/content/drive/MyDrive/mitbih/ablation_step19"

def _met(P,y):
    return (average_precision_score((y==1).astype(int),P[:,1]),
            average_precision_score((y==2).astype(int),P[:,2]))

def _norm(P): return P/P.sum(-1,keepdims=True)

def _quality(Pn):
    """label-free per-seed 품질: (합의상관 corr) × (신호분산 살아있나). 붕괴→낮음."""
    S=Pn[:,:,1]                                    # (m,N) S-확률
    medS=np.median(S,0)                            # 합의(붕괴에 강건)
    corr=np.array([np.corrcoef(S[i],medS)[0,1] for i in range(len(S))])
    corr=np.nan_to_num(corr)                       # 상수예측 seed → nan → 0
    std=S.std(1); std=std/(np.median(std)+1e-9)    # 신호 붕괴(저분산) 감지
    q=np.clip(corr,0,None)*np.clip(std,0,1.5)      # 둘 다 좋아야 높은 품질
    return corr,std,q

def _agg(Pn, mode, temp=0.05, keep=0.8):
    corr,std,q=_quality(Pn); m=len(Pn)
    if mode=="uniform":
        w=np.ones(m)/m
    elif mode=="weighted":                         # 품질 softmax 가중
        w=np.exp(np.clip(q,0,None)/temp); w=w/w.sum()
    elif mode=="trim":                             # 하위 (1-keep) 품질 제거 후 균일
        k=max(1,int(round(m*keep))); idx=np.argsort(-q)[:k]
        w=np.zeros(m); w[idx]=1.0/k
    elif mode=="trim_weighted":                    # 트림 후 품질 가중
        k=max(1,int(round(m*keep))); idx=np.argsort(-q)[:k]
        w=np.zeros(m); wi=np.exp(np.clip(q[idx],0,None)/temp); w[idx]=wi/wi.sum()
    return _norm((w[:,None,None]*Pn).sum(0)), w

def run_combine(temp=0.05):
    dwm=np.load(os.path.join(_SAVE,"wm.npz")); dwr=np.load(os.path.join(_SAVE,"wmr.npz"))
    Pwm,Pwr,y=dwm["P"],dwr["P"],dwm["y"]
    assert np.array_equal(dwm["y"],dwr["y"]), "y 불일치 — 같은 run 아님"
    P30=np.concatenate([Pwm,Pwr],0)               # (30,N,3) 풀
    print(f"풀: base {len(Pwm)} + repolK {len(Pwr)} = {len(P30)} 모델")
    corr,std,q=_quality(P30)
    tags=[f"wm{i}" for i in range(len(Pwm))]+[f"wr{i}" for i in range(len(Pwr))]
    order=np.argsort(-q)
    print("\n품질 상위 6 / 하위 6 (label-free):")
    for i in list(order[:6]): print(f"  ▲ {tags[i]:6s} q={q[i]:.2f} (corr={corr[i]:.2f} std={std[i]:.2f})  S={_met(P30[i],y)[0]:.3f}")
    for i in list(order[-6:]): print(f"  ▼ {tags[i]:6s} q={q[i]:.2f} (corr={corr[i]:.2f} std={std[i]:.2f})  S={_met(P30[i],y)[0]:.3f}")
    print(f"\n{'='*56}\n[참고] 개별 config 트림(step19):")
    for nm,Pn in [("base(15)",Pwm),("repolK(15)",Pwr)]:
        Pt,_=_agg(Pn,"trim"); s,v=_met(Pt,y); print(f"  {nm:12s} 트림  S={s:.4f}  V={v:.4f}")
    print("\n[핵심] 30-풀 합의 조합:")
    res={}
    for mode in ["uniform","weighted","trim","trim_weighted"]:
        P,w=_agg(P30,mode,temp=temp,keep=0.8); s,v=_met(P,y); res[mode]=(s,v)
        nb=int((w[:len(Pwm)]>1e-6).sum()); nr=int((w[len(Pwm):]>1e-6).sum())
        print(f"  30-{mode:14s} S={s:.4f}  V={v:.4f}   (기여 base {nb}/repolK {nr})")
    best=max(res,key=lambda k:res[k][0])
    print(f"\n▶ 최고: 30-{best} S={res[best][0]:.4f}  (repolK 단독트림 0.680 대비 {res[best][0]-0.680:+.4f})")
    print("  >0.680: 두 풀 합의가 붕괴 상쇄로 추가 이득.  ≤: repolK 단독트림 유지.")
    return res
