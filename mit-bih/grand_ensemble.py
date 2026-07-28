# =============================================================================
#  grand_ensemble.py  —  '어디서 잘 되는지'를 활용한 결합 (재학습 없음)
#
#  아이디어(사장님): 모델마다 S/V 강점이 다르다(temporal→V, base→S). 이를 활용해
#                    클래스별로 강한 모델을 쓰면 더 오를 수 있다 = Mixture-of-Experts.
#
#  모든 스텝의 저장된 DS2 예측(npz, 같은 DS2·같은 순서)을 모아:
#    · 모델별 S/V PR-AUC 랭킹
#    · [실사용] 전체 균일 앙상블
#    · [실사용] 구조적 사전지식 라우팅: V는 temporal계열, S/N은 그 외
#    · [오라클] 클래스별 최고 모델로 라우팅 (라벨 봐야 가능=상한, 실사용 불가)
#      → 오라클 vs 실사용 격차 = '어디서 잘 되는지 알면' 얻을 수 있는 헤드룸
#
#  실행:
#    exec(open('/content/drive/MyDrive/mitbih/grand_ensemble.py').read())
#    grand()
# =============================================================================
import os, glob
import numpy as np
from sklearn.metrics import average_precision_score, roc_auc_score

ROOT="/content/drive/MyDrive/mitbih"
# 라우팅용: 이름에 이 키워드가 있으면 'V 전문가'로 취급(구조적 사전지식)
V_EXPERT_KEYS=["temporal","dual"]

def _S(probs,y): return average_precision_score((y==1).astype(int),probs[:,1])
def _V(probs,y): return average_precision_score((y==2).astype(int),probs[:,2])
def _pp(probs,y,pid,min_s=5):
    a=[]
    for p in np.unique(pid):
        m=pid==p; yy=(y[m]==1).astype(int)
        if yy.sum()<min_s or yy.sum()==m.sum(): continue
        a.append(roc_auc_score(yy,probs[m,1]))
    return float(np.mean(a)) if a else float("nan")

def _norm(p): return p/p.sum(1,keepdims=True)

def grand(exclude_keys=("film",)):
    # film은 실패로 판명 → 기본 제외(원하면 exclude_keys=() 로 포함)
    files=sorted(glob.glob(os.path.join(ROOT,"ablation_step*","**","cnn_*.npz"),recursive=True))
    models=[]; y_ref=None; pid_ref=None
    for fp in files:
        name=os.path.relpath(fp,ROOT)
        if any(k in name for k in exclude_keys): continue
        d=np.load(fp); prob,y,pid=d["prob"],d["y"],d["pid"]
        if y_ref is None: y_ref,pid_ref=y,pid
        elif not (np.array_equal(y,y_ref) and np.array_equal(pid,pid_ref)):
            print(f"  [skip 정렬불일치] {name}"); continue
        models.append((name,prob))
    if not models: print("[!] npz 없음"); return
    y,pid=y_ref,pid_ref
    print(f"총 {len(models)}개 모델 예측 로드 (DS2 정렬 일치 확인)\n")

    # 모델별 S/V 랭킹
    stats=[(n,_S(p,y),_V(p,y)) for n,p in models]
    print("=== 모델별 강점 (S 상위 8 / V 상위 8) ===")
    for n,s,v in sorted(stats,key=lambda x:-x[1])[:8]: print(f"  S={s:.3f} V={v:.3f}  {n}")
    print("  ...")
    for n,s,v in sorted(stats,key=lambda x:-x[2])[:8]: print(f"  V={v:.3f} S={s:.3f}  {n}")

    P=np.stack([p for _,p in models],0)                    # [M,N,3]

    # [실사용] 전체 균일 앙상블
    uni=_norm(P.mean(0))
    print(f"\n[실사용] 전체 균일 앙상블({len(models)}개): S={_S(uni,y):.4f}  V={_V(uni,y):.4f}  환자별={_pp(uni,y,pid):.4f}")

    # [실사용] 구조적 라우팅: V는 V전문가 평균, S/N은 그 외 평균
    vmask=np.array([any(k in n for k in V_EXPERT_KEYS) for n,_ in models])
    if vmask.any() and (~vmask).all()==False:
        Vsrc=_norm(P[vmask].mean(0)); Ssrc=_norm(P[~vmask].mean(0))
        routed=np.stack([Ssrc[:,0],Ssrc[:,1],Vsrc[:,2]],1); routed=_norm(routed)
        print(f"[실사용] 사전지식 라우팅(V←temporal계열 {vmask.sum()}개 / S←그외 {(~vmask).sum()}개): "
              f"S={_S(routed,y):.4f}  V={_V(routed,y):.4f}  환자별={_pp(routed,y,pid):.4f}")

    # [오라클] 클래스별 최고 모델로 라우팅 (라벨 봐야 가능 → 상한, 실사용 불가)
    bestS=max(models,key=lambda m:_S(m[1],y)); bestV=max(models,key=lambda m:_V(m[1],y))
    orc=np.stack([bestS[1][:,0],bestS[1][:,1],bestV[1][:,2]],1); orc=_norm(orc)
    print(f"\n[오라클·상한] S←{bestS[0].split('/')[-1]} / V←{bestV[0].split('/')[-1]}: "
          f"S={_S(orc,y):.4f}  V={_V(orc,y):.4f}")
    print(f"  → 헤드룸(오라클 S − 균일 S) = {_S(orc,y)-_S(uni,y):+.4f}  "
          f"(클수록 '어디서 잘되는지 알면' 얻을 여지 큼)")
    return dict(uniform=uni,y=y,pid=pid)
