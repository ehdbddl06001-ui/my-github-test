# =============================================================================
#  colab_step9b_diag.py  —  P파 특징의 '증분' 판별력 (스케일링 고침)
#
#  step9 diagnose 결과: 개별 P파 특징 ROC-AUC 0.74~0.80(강함). 단 조합 0.022는
#  스케일링 누락→로지스틱 수렴실패 버그였음.
#
#  진짜 질문: 26개 + P파 8개가 '새 환자(DS2)'에서 S 판별을 올리나? (정보가 새것인가)
#  방법: 표준화 후 DS1 학습→DS2 테스트 로지스틱으로 26 / 8 / 26+8 비교.
#        (선형 로지스틱이라 CNN의 하한 프록시지만, 26+8>>26 이면 CNN도 이득 가능성 큼)
#
#  실행:
#    exec(open('/content/drive/MyDrive/mitbih/colab_step9_pwave.py').read())   # extract_pwave_features
#    exec(open('/content/drive/MyDrive/mitbih/colab_step9b_diag.py').read())
#    diag2()
# =============================================================================
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score, roc_auc_score

def _load():
    d=np.load("/content/drive/MyDrive/mitbih/mamba_data.npz")
    return d["beat"],d["ref"],d["feats"],d["y"],d["pid"]

def diag2():
    DS1=[101,106,108,109,112,114,115,116,118,119,122,124,201,203,205,207,208,209,215,220,223,230]
    DS2=[100,103,105,111,113,117,121,123,200,202,210,212,213,214,219,221,222,228,231,232,233,234]
    beats,refs,feats,y,pid=_load()
    Xpw=extract_pwave_features(beats,refs,pid)                 # step9에서 정의됨
    m1=np.isin(pid,DS1); m2=np.isin(pid,DS2)
    y1,y2=y[m1],y[m2]

    def evalset(X):
        X1,X2=X[m1],X[m2]
        sc=StandardScaler().fit(np.nan_to_num(X1))
        X1=np.nan_to_num(sc.transform(np.nan_to_num(X1))); X2=np.nan_to_num(sc.transform(np.nan_to_num(X2)))
        clf=LogisticRegression(max_iter=5000,C=1.0,class_weight={0:1,1:3,2:1.5}).fit(X1,y1)
        p2=clf.predict_proba(X2)
        S=average_precision_score((y2==1).astype(int),p2[:,1])
        V=average_precision_score((y2==2).astype(int),p2[:,2])
        return S,V

    print("=== DS1 학습 → DS2 테스트 (표준화 로지스틱, inter-patient) ===")
    print(f"(S base rate ≈ {(y2==1).mean():.3f})\n")
    sets=[("26 기존특징만",feats),("P파 8개만",Xpw),("26 + P파 8 = 34",np.concatenate([feats,Xpw],1))]
    res={}
    for nm,X in sets:
        S,V=evalset(X); res[nm]=(S,V)
        print(f"  {nm:20s}: S_PR-AUC={S:.4f}   V_PR-AUC={V:.4f}")
    dS=res["26 + P파 8 = 34"][0]-res["26 기존특징만"][0]
    print(f"\n  ▶ 증분(34 − 26) S = {dS:+.4f}")
    print("     >+0.03: P파가 26개에 없던 새 S 정보를 더함 = 사장님 가설 성립 → CNN에 넣을 가치 큼")
    print("     ~0:     이미 26개에 있던 정보 = 중복(모델엔 안 오를 것)")
    return res
