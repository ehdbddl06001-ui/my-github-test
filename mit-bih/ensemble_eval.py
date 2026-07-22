# =============================================================================
#  ensemble_eval.py  —  저장된 seed별 DS2 확률을 앙상블(평균)해서 재평가
#
#  재학습 없이, 이미 저장된 cnn_*_s{seed}.npz (prob/y/pid)를 불러
#  · seed별 개별 S/V PR-AUC
#  · seed들을 확률평균한 '앙상블' S/V PR-AUC
#  를 비교한다. 개별은 고분산이어도 앙상블은 안정+상승하는지가 핵심 진단.
#
#  실행(Colab):
#    exec(open('/content/drive/MyDrive/mitbih/ensemble_eval.py').read())
#    ensemble_dir('/content/drive/MyDrive/mitbih/ablation_step15/A_gss')
#    ensemble_dir('/content/drive/MyDrive/mitbih/ablation_step15/A_sgkf')
#    # STEP1 것도 가능:
#    ensemble_dir('/content/drive/MyDrive/mitbih/ablation_step1/A')
# =============================================================================
import os, glob
import numpy as np
from sklearn.metrics import average_precision_score, precision_recall_fscore_support


def _prauc(probs, y):
    s=average_precision_score((y==1).astype(int), probs[:,1])
    v=average_precision_score((y==2).astype(int), probs[:,2])
    n=average_precision_score((y==0).astype(int), probs[:,0])
    pred=probs.argmax(1)
    p,r,f,_=precision_recall_fscore_support(y,pred,labels=[0,1,2],zero_division=0)
    return dict(S=float(s),V=float(v),macro=float((n+s+v)/3),
               S_Se=float(r[1]),S_P=float(p[1]),S_F1=float(f[1]))

def ensemble_dir(folder):
    files=sorted(glob.glob(os.path.join(folder,"cnn_*_s*.npz")))
    if not files:
        print(f"[!] npz 없음: {folder}"); return
    print(f"\n===== {os.path.basename(folder)}  ({len(files)} seeds) =====")
    probs_list=[]; y_ref=None; pid_ref=None
    per=[]
    for fp in files:
        d=np.load(fp); prob=d["prob"]; y=d["y"]; pid=d["pid"]
        if y_ref is None: y_ref=y; pid_ref=pid
        else:
            # 정렬 일치 확인 (DS2는 seed와 무관하게 같은 순서여야 함)
            assert np.array_equal(y,y_ref), f"y 불일치: {fp}"
            assert np.array_equal(pid,pid_ref), f"pid 불일치: {fp}"
        probs_list.append(prob)
        m=_prauc(prob,y)
        per.append(m)
        print(f"  {os.path.basename(fp):28s}  S={m['S']:.4f}  V={m['V']:.4f}  macro={m['macro']:.4f}")
    P=np.stack(probs_list,0)                       # [n_seed, N, 3]
    ens=P.mean(0)                                  # 확률 평균 앙상블
    ens=ens/ens.sum(1,keepdims=True)               # 재정규화(안전)
    me=_prauc(ens,y_ref)
    sS=np.array([m["S"] for m in per]); sV=np.array([m["V"] for m in per])
    print(f"  {'-'*70}")
    print(f"  개별 평균      S={sS.mean():.4f} ± {sS.std():.4f}   V={sV.mean():.4f} ± {sV.std():.4f}")
    print(f"  ▶ 앙상블(평균) S={me['S']:.4f}            V={me['V']:.4f}   macro={me['macro']:.4f}")
    print(f"     앙상블 S_Se={me['S_Se']:.3f}  S_P={me['S_P']:.3f}  S_F1={me['S_F1']:.3f}")
    gain=me['S']-sS.mean()
    print(f"  → 앙상블 S 이득 = {gain:+.4f} (개별평균 대비)   "
          f"{'✅ 앙상블이 분산 흡수+상승' if gain>0 else '⚠ 이득 없음'}")
    return me
