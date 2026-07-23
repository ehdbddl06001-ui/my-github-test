# =============================================================================
#  colab_step12_wst.py  —  [STEP 12] Wavelet Scattering(WST) 특징을 우리 세팅에서
#
#  논문(Ait Bourkha 2025)의 98.5%는 intra-patient(비트 무작위 80/20)+SMOTE+15클래스
#  accuracy → 과대평가. 우리와 비교 불가. 단 '특징 추출법(WST)'은 진짜 좋음 → 빌린다.
#  우리 무기 = 정직한 inter-patient + label-free + 증분 검증 방법론.
#
#  WST = 이동불변 다중스케일 형태 특징(kymatio). 각 비트(2 lead)에서 계산, 시간평균.
#  검증: 26 vs WST vs 26+WST (DS1학습→DS2, 로지스틱 증분). P파(+0.06~0.08)보다 크면
#        더 강한 정보 → CNN 테스트 가치.
#
#  준비:  !pip install kymatio -q
#  실행:
#    exec(open('/content/drive/MyDrive/mitbih/colab_step12_wst.py').read())
#    diag_wst()
# =============================================================================
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score, roc_auc_score

_DS1=[101,106,108,109,112,114,115,116,118,119,122,124,201,203,205,207,208,209,215,220,223,230]
_DS2=[100,103,105,111,113,117,121,123,200,202,210,212,213,214,219,221,222,228,231,232,233,234]

def _load():
    d=np.load("/content/drive/MyDrive/mitbih/mamba_data.npz")
    return d["beat"],d["feats"],d["y"],d["pid"]

def compute_wst_features(beats,J=6,Q=8,chunk=2048,log=True):
    """각 비트 2 lead에 1D Wavelet Scattering, 시간평균 → 고정 특징벡터[N,2P]."""
    import torch
    from kymatio.torch import Scattering1D
    dev="cuda" if torch.cuda.is_available() else "cpu"
    T=beats.shape[2]; S=Scattering1D(J=J,shape=T,Q=Q).to(dev)
    per_lead=[]
    for lead in range(beats.shape[1]):
        x=beats[:,lead,:]; outs=[]
        for i in range(0,len(x),chunk):
            xb=torch.from_numpy(np.ascontiguousarray(x[i:i+chunk])).float().to(dev)
            with torch.no_grad():
                sx=S(xb)                       # [b, P, Tds]
            outs.append(sx.mean(dim=-1).cpu().numpy())   # 시간평균 [b,P]
        per_lead.append(np.concatenate(outs,0))
    X=np.concatenate(per_lead,1).astype("float32")       # [N, 2P]
    if log: X=np.log1p(np.abs(X))*np.sign(X)             # 스케터링 계수 왜도 완화
    return np.nan_to_num(X)

def _evalset(X,m1,m2,y1,y2):
    sc=StandardScaler().fit(np.nan_to_num(X[m1]))
    X1=np.nan_to_num(sc.transform(np.nan_to_num(X[m1]))); X2=np.nan_to_num(sc.transform(np.nan_to_num(X[m2])))
    clf=LogisticRegression(max_iter=5000,C=0.5,class_weight={0:1,1:3,2:1.5}).fit(X1,y1)
    p2=clf.predict_proba(X2)
    return (average_precision_score((y2==1).astype(int),p2[:,1]),average_precision_score((y2==2).astype(int),p2[:,2]))

def diag_wst(J=6,Q=8):
    beats,feats,y,pid=_load()
    print(f"WST 계산 중 (J={J},Q={Q})...")
    Xw=compute_wst_features(beats,J=J,Q=Q)
    print(f"WST 특징 차원: {Xw.shape[1]}\n")
    m1=np.isin(pid,_DS1); m2=np.isin(pid,_DS2); y1,y2=y[m1],y[m2]
    base=_evalset(feats,m1,m2,y1,y2)
    print(f"=== DS1학습→DS2 (inter-patient, 로지스틱) ===")
    print(f"기준선 26개만       : S={base[0]:.4f}  V={base[1]:.4f}")
    for nm,X in [("WST만",Xw),("26 + WST",np.concatenate([feats,Xw],1))]:
        S,V=_evalset(X,m1,m2,y1,y2)
        print(f"{nm:18s}: S={S:.4f}(증분 {S-base[0]:+.4f})  V={V:.4f}")
    print("\n  → '26+WST' 증분이 P파(+0.06~0.08)보다 크면: WST가 더 강한 정보 → CNN 테스트로.")
    print("     비슷/작으면: WST도 단일비트 형태라 26·CNN이 이미 상당부분 커버.")
    # 캐시로 남겨 CNN 단계 재사용
    global _WST; _WST=Xw
    return Xw
