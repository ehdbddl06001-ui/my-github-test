# =============================================================================
#  grand_ensemble_v2.py  —  label-free 조건별 라우팅으로 헤드룸 먹기 (재학습 없음)
#
#  grand() 발견: 헤드룸(+0.24)의 대부분은 '좋은 S모델을 나쁜 모델과 평균하지 마라'.
#  이번: DS2 라벨 없이 '어디서 어느 모델을 믿을지' 판단하는 조건 신호를 테스트.
#    · confidence 가중: 비트마다 확신하는 모델에 가중(per-beat 라우팅)
#    · agreement 게이팅: 모델 불일치 큰 '어려운 비트' 분석
#    · 계열 라우팅과 결합
#  모든 전략은 '사전 정의'(구조/신호 기반) — DS2 결과로 고르는 반칙 아님.
#
#  실행:
#    exec(open('/content/drive/MyDrive/mitbih/grand_ensemble_v2.py').read())
#    grand2()
# =============================================================================
import os, glob
import numpy as np
from sklearn.metrics import average_precision_score, roc_auc_score

ROOT="/content/drive/MyDrive/mitbih"
V_EXPERT_KEYS=["temporal","dual"]

def _S(p,y): return average_precision_score((y==1).astype(int),p[:,1])
def _V(p,y): return average_precision_score((y==2).astype(int),p[:,2])
def _pp(p,y,pid,min_s=5):
    a=[]
    for q in np.unique(pid):
        m=pid==q; yy=(y[m]==1).astype(int)
        if yy.sum()<min_s or yy.sum()==m.sum(): continue
        a.append(roc_auc_score(yy,p[m,1]))
    return float(np.mean(a)) if a else float("nan")
def _n(p): return p/p.sum(1,keepdims=True)

def grand2(exclude_keys=("film",)):
    files=sorted(glob.glob(os.path.join(ROOT,"ablation_step*","**","cnn_*.npz"),recursive=True))
    names=[]; probs=[]; y=None; pid=None
    for fp in files:
        nm=os.path.relpath(fp,ROOT)
        if any(k in nm for k in exclude_keys): continue
        d=np.load(fp)
        if y is None: y,pid=d["y"],d["pid"]
        elif not (np.array_equal(d["y"],y) and np.array_equal(d["pid"],pid)): continue
        names.append(nm); probs.append(d["prob"])
    P=np.stack(probs,0)                                  # [M,N,3]
    M=len(names); print(f"{M}개 모델 로드\n")
    vmask=np.array([any(k in nm for k in V_EXPERT_KEYS) for nm in names])
    Spool=P[~vmask]; Vpool=P[vmask]                      # S계열 / V계열

    def report(tag,ens): print(f"  {tag:34s} S={_S(ens,y):.4f}  V={_V(ens,y):.4f}  환자별={_pp(ens,y,pid):.4f}")

    print("=== [실사용·label-free] 전략별 ===")
    uni=_n(P.mean(0)); report("① 균일(전체)",uni)

    # ② 계열 라우팅 (V←V계열, S/N←S계열)
    Ss=_n(Spool.mean(0)); Vs=_n(Vpool.mean(0))
    routed=_n(np.stack([Ss[:,0],Ss[:,1],Vs[:,2]],1)); report("② 계열 라우팅",routed)

    # ③ confidence 가중(per-beat): 비트마다 확신(max prob) 큰 모델에 가중
    conf=P.max(-1)                                        # [M,N]
    w=conf/ (conf.sum(0,keepdims=True)+1e-9)
    cw=_n((w[...,None]*P).sum(0)); report("③ confidence 가중(전체)",cw)

    # ④ confidence 가중 + 계열 라우팅 (S는 S계열 내 confidence, V는 V계열)
    wc=lambda Q:( (Q.max(-1)/(Q.max(-1).sum(0,keepdims=True)+1e-9))[...,None]*Q ).sum(0)
    Sc=_n(wc(Spool)); Vc=_n(wc(Vpool))
    cwr=_n(np.stack([Sc[:,0],Sc[:,1],Vc[:,2]],1)); report("④ conf가중+계열 라우팅",cwr)

    # ⑤ S-confidence 라우팅: S결정은 'S를 확신하는 모델'에 가중 (p[:,1] 큰 모델)
    ws=P[:,:,1]/(P[:,:,1].sum(0,keepdims=True)+1e-9)
    Sconf=(ws*P[:,:,1]).sum(0)                            # S열만 재조합
    scr=np.stack([Ss[:,0],Sconf,Vs[:,2]],1); scr=_n(scr); report("⑤ S-확신 라우팅+V계열",scr)

    # 오라클(상한, 라벨 봄): 계열별 최고 + per-beat 최고
    bestS=Spool[np.argmax([_S(p,y) for p in Spool])]
    bestV=Vpool[np.argmax([_V(p,y) for p in Vpool])]
    orc=_n(np.stack([bestS[:,0],bestS[:,1],bestV[:,2]],1))
    # per-beat 오라클: 각 비트에서 정답 S모델 중 최대 S확률(절대 상한)
    perbeat_S=Spool[:,:,1].max(0)
    pb=np.stack([1-perbeat_S-Vs[:,2].clip(0,1-perbeat_S),perbeat_S,Vs[:,2]],1); pb=_n(pb.clip(1e-6,None))
    print("\n=== [오라클·상한, 라벨 봐야 가능] ===")
    print(f"  모델선택 오라클     S={_S(orc,y):.4f}  V={_V(orc,y):.4f}")
    print(f"  per-beat S 오라클   S={_S(pb,y):.4f}  (비트마다 S 최고모델 = 절대상한)")
    print(f"\n  → label-free 최고(위①~⑤ 중) vs per-beat 오라클 격차가 '남은 여지'")
    return dict(y=y,pid=pid,names=names)
