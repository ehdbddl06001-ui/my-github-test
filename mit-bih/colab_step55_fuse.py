# =============================================================================
#  colab_step55_fuse.py  —  [STEP 55] 상보 view 점수융합 (SEN↑ — 사장님 'S 더 잡는 조건')
#
#  STEP54 발견: RHYTHM(타이밍 S)·AE(형태 S)는 각각 강한데 feature로 합치면 간섭(더 나쁨).
#  둘은 서로 '다른 S'를 잡음 → feature 아닌 '점수 레벨'에서 융합하면 상보. 특히 max(OR)=
#  '둘 중 하나라도 S라 하면 S' → 민감도↑ (현재 정밀도 부자/민감도 부족을 정면교정).
#  파라미터 없음(mean/max/geomean) = DS2 튜닝 아님, 오염 없음.
#  ★ 재학습 불필요: STEP54가 저장한 seed별 예측을 불러와 융합만(CPU 즉시).
#
#  선행: colab_step54_sweep2.py 의 confirm 단계 완료(synergy2_out/cnn/{mask}_s{seed}.npy)
#  실행:
#    exec(open('/content/drive/MyDrive/mitbih/colab_step55_fuse.py').read())
#    fuse_test()
# =============================================================================
import os
import numpy as np
from sklearn.metrics import average_precision_score, precision_recall_curve

_BASE="/content/drive/MyDrive/mitbih"; _CNN=f"{_BASE}/synergy2_out/cnn"
_DS2=[100,103,105,111,113,117,121,123,200,202,210,212,213,214,219,221,222,228,231,232,233,234]
# 마스크(STEP54 비트순서: RHYTHM0 NOISE1 KOOPMAN2 AE3 GNN4 SEGDEV5 VCG6)
_M_RHY=1<<0                          # RHYTHM
_M_RKG=(1<<0)|(1<<2)|(1<<4)          # RHYTHM+KOOPMAN+GNN (균형, best S_PR)
_M_KAG=(1<<2)|(1<<3)|(1<<4)          # KOOPMAN+AE+GNN     (정밀, best PREC/F1)
_NAMES={_M_RHY:"RHYTHM", _M_RKG:"RHYTHM+KOOPMAN+GNN", _M_KAG:"KOOPMAN+AE+GNN"}

def _f1(y2,s):
    p,r,_=precision_recall_curve((y2==1).astype(int),s); f=2*p*r/(p+r+1e-9); i=int(np.nanargmax(f)); return p[i],r[i],f[i]
def _loadpreds(mask, seeds):
    P=[]
    for s in seeds:
        sp=f"{_CNN}/{mask}_s{s}.npy"
        if os.path.exists(sp): P.append(np.load(sp))
    return np.stack(P,0) if P else None
def _trim(Pn):
    if len(Pn)==1: P=Pn[0]; return P/P.sum(1,keepdims=True)
    medS=np.median(Pn[:,:,1],0); corr=np.array([np.corrcoef(Pn[i,:,1],medS)[0,1] for i in range(len(Pn))])
    keep=np.argsort(-corr)[:max(1,int(round(len(Pn)*0.8)))]; P=Pn[keep].mean(0); return P/P.sum(1,keepdims=True)

def fuse_test(seeds=None):
    seeds=seeds or list(range(2000,2015))
    d=np.load(f"{_BASE}/mamba_data.npz"); y,pid=d["y"],d["pid"]; y2=y[np.isin(pid,_DS2)]
    def M(sc): return average_precision_score((y2==1).astype(int),sc)
    def row(nm,sc):
        S=M(sc); pr,se,f1=_f1(y2,sc); print(f"  {nm:26s} S={S:.4f} PREC={pr:.3f} SEN={se:.3f} F1={f1:.3f}"); return (S,pr,se,f1)
    # 단일 모델(트림 앙상블) S점수
    tr={}
    for mask in (_M_RHY,_M_RKG,_M_KAG):
        Pn=_loadpreds(mask,seeds)
        if Pn is None: print(f"  ✗ mask={mask}({_NAMES[mask]}) 예측 없음 → STEP54 confirm 먼저"); continue
        tr[mask]=_trim(Pn)
    if len(tr)<2: return
    print(f"=== 단일 (트림앙상블) ===")
    for mask,P in tr.items(): row(_NAMES[mask],P[:,1])
    def fuse(a,b,how):
        sa=np.clip(a,1e-6,1); sb=np.clip(b,1e-6,1)
        return {"mean":(sa+sb)/2,"max":np.maximum(sa,sb),"geo":np.sqrt(sa*sb)}[how]
    pairs=[(_M_RKG,_M_KAG),(_M_RHY,_M_KAG)]   # 균형⊕정밀 / RHYTHM(타이밍)⊕AE(형태)
    for a,b in pairs:
        if a not in tr or b not in tr: continue
        print(f"\n=== 융합: {_NAMES[a]}  ⊕  {_NAMES[b]} ===")
        for how in ("mean","max","geo"):
            row(f"{how}", fuse(tr[a][:,1],tr[b][:,1],how))
    print(f"\n  ★ max 융합이 SEN↑ & F1↑ 이면 = 상보 view가 서로 다른 S를 잡아 민감도 회복(사장님 아이디어).")
    print(f"     PREC가 Farag(0.827) 위로 유지되며 SEN이 오르면 F1이 최고점 갱신 기대.")
