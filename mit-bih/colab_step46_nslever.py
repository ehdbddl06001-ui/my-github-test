# =============================================================================
#  colab_step46_nslever.py  —  [STEP 46] N/S 잔여 레버 진단 (P파 재평가 + 타이밍 스캔)
#
#  질문: 강한 기반(best+DTW) 위에서 N/S를 '더' 가를 레버가 남았나?
#  SVEB=심실위 조기박동 → QRS는 N과 공유, 판별정보는 (1)P파(이소성) (2)조기성(RR)뿐.
#  둘 다 이미 부분적으로 건드림(P파=STEP9, 타이밍=feats0 de Chazal). 지금 기반 위 재평가:
#   A) P파 8특징(STEP9: P-on-T·이상P·P축·P피크이동 등)을 best+DTW 위에 단일스캔(ΔS)
#   B) feats0 26개 각 컬럼의 S 판별력 스캔 → 타이밍(RR) 특징이 얼마나 강한지·덜 쓰였는지
#   C) best+DTW +P파8 / +P파(양성만) 조합 증분
#  → ΔS>0 인 특징만 STEP45(margin CNN)에 승격. 아니면 'N/S는 이 기반에서 천장' 정직히 확정.
#
#  선행 캐시: _WST,_MORPHO,_REPOL,_DTW  (+ step9 파일이 Drive에 있어야 P파 추출기 로드)
#  실행:
#    exec(open('/content/drive/MyDrive/mitbih/colab_step46_nslever.py').read())
#    diag_nslever()
# =============================================================================
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.metrics import average_precision_score, roc_auc_score

_BASE="/content/drive/MyDrive/mitbih"
_DS1=[101,106,108,109,112,114,115,116,118,119,122,124,201,203,205,207,208,209,215,220,223,230]
_DS2=[100,103,105,111,113,117,121,123,200,202,210,212,213,214,219,221,222,228,231,232,233,234]
_REPOLK_IDX=[0,1,4,5]
PW_NAMES=["P/QRST비율","P비율(정상대비)","T잔차(P-on-T)","P잔차(이상P)","전체형태편차",
          "P축방향편차","P피크이동(조기성)","전체VM비"]

def _medref(beats,pid):
    r=np.empty_like(beats)
    for p in np.unique(pid): m=pid==p; r[m]=np.median(beats[m],axis=0,keepdims=True)
    return r.astype("float32")

def _ev(X,m1,m2,y1,y2):
    sc=StandardScaler().fit(np.nan_to_num(X[m1]))
    X1=np.nan_to_num(sc.transform(np.nan_to_num(X[m1]))); X2=np.nan_to_num(sc.transform(np.nan_to_num(X[m2])))
    clf=LogisticRegression(max_iter=5000,C=0.5,class_weight={0:1,1:3,2:1.5}).fit(X1,y1)
    return average_precision_score((y2==1).astype(int),clf.predict_proba(X2)[:,1])

def diag_nslever():
    d=np.load(f"{_BASE}/mamba_data.npz"); beats,feats0,y,pid=d["beat"],d["feats"],d["y"],d["pid"]
    ref=_medref(beats,pid); m1=np.isin(pid,_DS1); m2=np.isin(pid,_DS2); y1,y2=y[m1],y[m2]
    # P파 추출기 확보(STEP9)
    if "extract_pwave_features" not in globals():
        print("P파 추출기 없음 → step9 로드..."); exec(open(f"{_BASE}/colab_step9_pwave.py").read(), globals())
    Xpw=globals()["extract_pwave_features"](beats,ref,pid)
    # best+DTW 기반
    Xw=globals().get("_WST"); Xm=globals().get("_MORPHO"); Xr=globals().get("_REPOL"); Xd=globals().get("_DTW")
    Xwk=np.nan_to_num(SelectKBest(f_classif,k=40).fit(np.nan_to_num(Xw[m1]),y1).transform(np.nan_to_num(Xw)))
    BEST=np.concatenate([feats0,Xwk,Xm,Xr[:,_REPOLK_IDX],Xd],1); bS=_ev(BEST,m1,m2,y1,y2)

    print(f"=== A) P파 8특징: DS2 단변량 S 판별력 + best+DTW 위 증분 (best S={bS:.4f}) ===")
    pos=[]
    for k,nm in enumerate(PW_NAMES):
        c=Xpw[m2,k]
        if np.std(c)<1e-9: print(f"  {nm:16s}: (상수)"); continue
        a=roc_auc_score((y2==1).astype(int),c); a=max(a,1-a)
        S=_ev(np.concatenate([BEST,Xpw[:,[k]]],1),m1,m2,y1,y2)
        star="★" if S>bS+1e-4 else ""
        if S>bS+1e-4: pos.append(k)
        print(f"  {nm:16s}: AUC={a:.3f}  +best→S={S:.4f} ({S-bS:+.4f}) {star}")

    print(f"\n=== B) feats0(26 de Chazal) 각 컬럼 S 판별력 (타이밍/RR 레버 확인) ===")
    order=[]
    for k in range(feats0.shape[1]):
        c=feats0[m2,k]
        if np.std(c)<1e-9: order.append((k,0.5)); continue
        a=roc_auc_score((y2==1).astype(int),c); order.append((k,max(a,1-a)))
    for k,a in sorted(order,key=lambda t:-t[1])[:10]:
        bar="█"*int((a-0.5)*40); print(f"  feats0[{k:2d}]: AUC={a:.3f}  {bar}")
    print("  (상위가 RR/조기성일 가능성↑ — de Chazal 26D 앞부분이 RR간격. 강하면 타이밍은 이미 반영됨)")

    print(f"\n=== C) 조합 증분 (best+DTW 기준 S={bS:.4f}) ===")
    print(f"  +P파 8개 전부   : S={_ev(np.concatenate([BEST,Xpw],1),m1,m2,y1,y2):.4f}")
    if pos:
        print(f"  +P파 양성만{tuple(pos)}: S={_ev(np.concatenate([BEST,Xpw[:,pos]],1),m1,m2,y1,y2):.4f}")
        print(f"\n  ★ 양성 P파 특징을 STEP45(margin CNN) F에 추가해 15seed로 최종확인.")
    else:
        print(f"\n  ▶ best+DTW 위에서 P파가 ΔS>0 없음 = 이 기반은 P파 정보를 이미 흡수(DTW-P/morph).")
        print(f"     → N/S는 단일 리드쌍 MIT-BIH에서 이 근처가 물리적 천장. margin-best로 확정 권장.")
    global _PWAVE; _PWAVE=Xpw
    return dict(bS=bS, pos=pos)
