# =============================================================================
#  colab_step8_stack.py  —  학습된 라우터(스태킹)가 새 환자에서 실제로 살리나
#
#  hardness: 못맞힘 3.4%(정보없음 적음) but per-beat 오라클 0.966은 57모델 max 착시.
#  grand2:   단순 confidence 라우팅(③④⑤)이 계열라우팅 ②(0.595) 못 넘음.
#  → 진짜 질문: '학습된 메타 라우터'가 새 환자에서 ②를 넘나?
#
#  방법(재학습 없음, 저장 예측 위 스태킹):
#    X = 각 모델의 DS2 확률들[N, M*3], y, pid
#    GroupKFold(환자 단위): 일부 DS2환자로 메타 학습 → 못 본 DS2환자 예측(OOF)
#    = '새 환자로의 라우터 일반화'를 정직하게 추정.
#  ※ CV 학습에 DS2 라벨을 쓰므로 '배포 가능 수치'는 아니고, 라우터 잠재력의 정직한 상한.
#     이게 ②(0.595)를 넘으면 → DS1-학습 배포판 제작 가치. 못 넘으면 → 데이터 한계.
#
#  실행:
#    exec(open('/content/drive/MyDrive/mitbih/colab_step8_stack.py').read())
#    stack()
# =============================================================================
import os, glob
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GroupKFold
from sklearn.metrics import average_precision_score, roc_auc_score

ROOT="/content/drive/MyDrive/mitbih"

def _S(p,y): return average_precision_score((y==1).astype(int),p[:,1])
def _V(p,y): return average_precision_score((y==2).astype(int),p[:,2])
def _pp(p,y,pid,min_s=5):
    a=[]
    for q in np.unique(pid):
        m=pid==q; yy=(y[m]==1).astype(int)
        if yy.sum()<min_s or yy.sum()==m.sum(): continue
        a.append(roc_auc_score(yy,p[m,1]))
    return float(np.mean(a)) if a else float("nan")

def stack(exclude_keys=("film",), C=0.3, n_splits=5):
    files=sorted(glob.glob(os.path.join(ROOT,"ablation_step*","**","cnn_*.npz"),recursive=True))
    probs=[]; y=None; pid=None; names=[]
    for fp in files:
        nm=os.path.relpath(fp,ROOT)
        if any(k in nm for k in exclude_keys): continue
        d=np.load(fp)
        if y is None: y,pid=d["y"],d["pid"]
        elif not (np.array_equal(d["y"],y) and np.array_equal(d["pid"],pid)): continue
        probs.append(d["prob"]); names.append(nm)
    P=np.stack(probs,0)                                  # [M,N,3]
    M,N,_=P.shape
    X=P.transpose(1,0,2).reshape(N,M*3)                  # [N, M*3] 메타 입력
    print(f"{M}개 모델 → 메타입력 {X.shape}, 환자 {len(np.unique(pid))}명\n")

    # 기준선(비교용): 균일 앙상블, 계열 라우팅
    uni=P.mean(0); uni=uni/uni.sum(1,keepdims=True)
    print(f"[기준] 균일 앙상블         S={_S(uni,y):.4f}  V={_V(uni,y):.4f}  환자별={_pp(uni,y,pid):.4f}")

    # 환자 단위 CV 스태킹 (OOF)
    oof=np.zeros((N,3)); gkf=GroupKFold(n_splits=n_splits)
    for tr,te in gkf.split(X,y,groups=pid):
        clf=LogisticRegression(max_iter=2000,C=C,class_weight={0:1.0,1:3.0,2:1.5})
        clf.fit(X[tr],y[tr]); oof[te]=clf.predict_proba(X[te])
    print(f"[스태킹] 환자CV 메타라우터  S={_S(oof,y):.4f}  V={_V(oof,y):.4f}  환자별={_pp(oof,y,pid):.4f}")
    print(f"          (C={C}, {n_splits}-fold 환자분리)")

    dS=_S(oof,y)-0.5953
    print(f"\n  → 스태킹 S − 계열라우팅(0.595) = {dS:+.4f}")
    print("     >+0.03 이면: 학습된 라우터가 새 환자에서 실제로 살림 → DS1-배포판 제작 가치")
    print("     ~0 이면:     라우터도 새 환자엔 일반화 못함 → 데이터 한계 확정")
    return dict(oof=oof,y=y,pid=pid)
