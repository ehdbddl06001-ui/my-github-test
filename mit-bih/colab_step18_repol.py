# =============================================================================
#  colab_step18_repol.py  —  [STEP 18] 재분극(Repolarization, RT/T파) 정밀 특징
#
#  STEP15 morpho 단변량서 S를 가장 잘 가른 축 = 재분극:
#    RT간격 0.846(최강) · T지속 0.826 · T/QRS에너지 0.785  >> P파.
#  SVEB(조기 심방수축)이 QT/재분극 타이밍을 바꾸기 때문. WST(형태)와 물리적으로 다른 축.
#  단 morpho는 argmax/임계값 기반(거침). 여기선 T파를 '에너지 모멘트'로 강건하게 잰다:
#    무게중심(RT중심)·2차모멘트(폭)·3차모멘트(비대칭)·누적90%(T끝/JT)·ST레벨.
#  전부 환자 정상(ref=환자 median beat) 대비 = 개인 함수. label-free(DS2 라벨 미사용).
#
#  ★ 검증 ★ 이미 쓰는 morpho(RT/T 거친 버전) '위에' 정밀 재분극이 정보를 더하나?
#    로지스틱: 26 / repol / 26+repol / 26+WST+morpho / 26+WST+morpho+repol 증분.
#    26+WST+morpho+repol > 26+WST+morpho 면 → 정밀 재분극이 새 정보(가치).
#
#  선행(비교): colab_step12_wst.py(_WST), colab_step15_morpho.py(_MORPHO)
#  실행:
#    exec(open('/content/drive/MyDrive/mitbih/colab_step18_repol.py').read())
#    diag_repol()
# =============================================================================
import numpy as np
from scipy.ndimage import uniform_filter1d
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.metrics import average_precision_score, roc_auc_score

_DS1=[101,106,108,109,112,114,115,116,118,119,122,124,201,203,205,207,208,209,215,220,223,230]
_DS2=[100,103,105,111,113,117,121,123,200,202,210,212,213,214,219,221,222,228,231,232,233,234]
REPOL_NAMES=["RT중심(무게중심)","RT중심(정상대비)","T폭(2차모멘트)","T폭(정상대비)",
             "T비대칭(왜도)","T비대칭(정상대비)","ST레벨(ST/QRS)","ST레벨(정상대비)",
             "T에너지분율","T진폭(정상대비)","JT간격(QRS끝-T끝)","JT간격(정상대비)"]

def _allbeat_median_ref(beats,pid):
    r=np.empty_like(beats)
    for p in np.unique(pid):
        m=pid==p; r[m]=np.median(beats[m],axis=0,keepdims=True)
    return r.astype("float32")

def _tmoments(VM, R, L):
    """VM(=순간 에너지, n×L)에서 재분극(T파) 에너지 모멘트. R=정상 QRS피크 위치."""
    eps=1e-6
    Qe=min(L, R+20)                                  # QRS 끝(대략)
    Ts,Te=min(L-4, R+25), min(L, R+140)              # T 탐색창
    if Te-Ts<6: Ts,Te=max(0,L-40), L
    seg=VM[:,Ts:Te]                                  # (n,w)
    w=seg.shape[1]; ix=np.arange(w,dtype=np.float32)
    tot=seg.sum(1)+eps
    c=(seg*ix).sum(1)/tot                            # 창 내 무게중심(상대)
    RTc=(Ts+c)-R                                     # R→T 무게중심 = 강건 RT
    var=(seg*(ix-c[:,None])**2).sum(1)/tot
    Twid=np.sqrt(np.clip(var,0,None))                # T폭(2차모멘트)
    skew=(seg*(ix-c[:,None])**3).sum(1)/tot/(Twid**3+eps)   # T비대칭(3차모멘트)
    cum=np.cumsum(seg,1)/(seg.sum(1,keepdims=True)+eps)
    t90=(cum>=0.9).argmax(1).astype(np.float32)      # 누적90% = T끝(강건)
    JT=(Ts+t90)-Qe                                   # QRS끝→T끝
    Tamp=seg.max(1)                                  # T 피크 진폭
    Tener=seg.sum(1)                                 # T 에너지(적분)
    STs,STe=min(L-2,R+12),min(L,R+32)                # ST 분절
    STe=max(STe,STs+2)
    STlev=VM[:,STs:STe].sum(1)/(VM[:,max(0,R-18):Qe].sum(1)+eps)   # ST/QRS 에너지
    Ttot=Tener/(VM.sum(1)+eps)                       # T 에너지분율
    return dict(RTc=RTc,Twid=Twid,skew=skew,JT=JT,Tamp=Tamp,STlev=STlev,Tfrac=Ttot)

def extract_repol_features(beats,refs,pid):
    """정밀 재분극 12특징. refs=환자 정상 median(개인 함수 기준)."""
    N=len(beats); F=np.zeros((N,12),np.float32); eps=1e-6
    for p in np.unique(pid):
        idx=np.where(pid==p)[0]; b=beats[idx]; r=refs[idx]
        VMb=np.sqrt(b[:,0]**2+b[:,1]**2); VMr=np.sqrt(r[:,0]**2+r[:,1]**2)
        L=VMb.shape[1]; R=int(np.argmax(VMr[0]))
        mb=_tmoments(VMb,R,L); mr=_tmoments(VMr,R,L)   # mr: 환자 정상(창별 스칼라, 브로드캐스트)
        cols=[mb["RTc"],            mb["RTc"]-mr["RTc"],
              mb["Twid"],           mb["Twid"]/(mr["Twid"]+eps),
              mb["skew"],           mb["skew"]-mr["skew"],
              mb["STlev"],          mb["STlev"]-mr["STlev"],
              mb["Tfrac"],          mb["Tamp"]/(mr["Tamp"]+eps),
              mb["JT"],             mb["JT"]-mr["JT"]]
        F[idx]=np.stack(cols,1)
    return np.nan_to_num(F,posinf=0,neginf=0).astype("float32")

def _load():
    d=np.load("/content/drive/MyDrive/mitbih/mamba_data.npz"); return d["beat"],d["feats"],d["y"],d["pid"]

def _ev(X,m1,m2,y1,y2):
    sc=StandardScaler().fit(np.nan_to_num(X[m1]))
    X1=np.nan_to_num(sc.transform(np.nan_to_num(X[m1]))); X2=np.nan_to_num(sc.transform(np.nan_to_num(X[m2])))
    clf=LogisticRegression(max_iter=5000,C=0.5,class_weight={0:1,1:3,2:1.5}).fit(X1,y1)
    p2=clf.predict_proba(X2)
    return average_precision_score((y2==1).astype(int),p2[:,1])

def diag_repol():
    beats,feats,y,pid=_load()
    ref=_allbeat_median_ref(beats,pid)
    Xr=extract_repol_features(beats,ref,pid)
    m1=np.isin(pid,_DS1); m2=np.isin(pid,_DS2); y1,y2=y[m1],y[m2]
    print("=== repol 12특징 단변량 S ROC-AUC (DS2) ===")
    for k,nm in enumerate(REPOL_NAMES):
        c=Xr[m2,k]
        if np.std(c)<1e-9: print(f"  {nm:16s}: (상수)"); continue
        a=roc_auc_score((y2==1).astype(int),c); a=max(a,1-a)
        print(f"  {nm:16s}: {a:.3f}  {'█'*int((a-0.5)*40)}")
    base=_ev(feats,m1,m2,y1,y2)
    print(f"\n=== DS1→DS2 로지스틱 증분 (기준 26개 S={base:.4f}) ===")
    rows=[("repol12만",Xr),("26+repol",np.concatenate([feats,Xr],1))]
    Xw=globals().get("_WST",None); Xm=globals().get("_MORPHO",None)
    if Xw is not None and Xm is not None:
        Xwk=np.nan_to_num(SelectKBest(f_classif,k=40).fit(np.nan_to_num(Xw[m1]),y1).transform(np.nan_to_num(Xw)))
        WM=np.concatenate([feats,Xwk,Xm],1)
        rows+=[("26+WST+morpho",WM),("26+WST+morpho+repol",np.concatenate([WM,Xr],1))]
    for nm,X in rows:
        S=_ev(X,m1,m2,y1,y2); print(f"  {nm:20s}: S={S:.4f}  (증분 {S-base:+.4f})")
    if Xw is not None:
        print("\n  ★ '+repol' > '26+WST+morpho' 면 → 정밀 재분극이 새 정보 추가.")
    else:
        print("\n  (WST·morpho 비교하려면 step12·step15 먼저 로드해 _WST·_MORPHO 캐시)")
    global _REPOL; _REPOL=Xr
    return Xr

# 정상대비(비율/차이) 특징 인덱스 = 환자 베이스라인 제거 → 이동에 강함. Tfrac(8)도 within-beat 비율.
_REL_IDX=[1,3,5,7,8,9,11]

def diag_repol_shift():
    """왜 고단변량 특징이 모델서 떨어지나 = DS1→DS2 분포이동(covariate shift) 진단.
       + 이동에 강한 '정상대비'만 남겨 재검(구제 가능성)."""
    beats,feats,y,pid=_load()
    ref=_allbeat_median_ref(beats,pid)
    Xr=globals().get("_REPOL",None); Xr=Xr if Xr is not None else extract_repol_features(beats,ref,pid)
    m1=np.isin(pid,_DS1); m2=np.isin(pid,_DS2); y1,y2=y[m1],y[m2]
    print("=== 특징별 [단변량AUC] vs [DS1→DS2 이동량(σ)] ===")
    print("   (이동량 = |mean_DS2-mean_DS1| / std_DS1. 큰 값 = 전달 안 되는 베이스라인=독)")
    print(f"   {'특징':16s} {'단변량':>7s} {'이동σ':>7s}  판정")
    for k,nm in enumerate(REPOL_NAMES):
        c2=Xr[m2,k]
        auc=roc_auc_score((y2==1).astype(int),c2); auc=max(auc,1-auc)
        sd1=Xr[m1,k].std()+1e-9; shift=abs(Xr[m2,k].mean()-Xr[m1,k].mean())/sd1
        rel="(정상대비)" if k in _REL_IDX else "(절대)   "
        flag="← 고단변량·고이동=독" if (auc>0.75 and shift>0.5) else ""
        print(f"   {nm:16s} {auc:7.3f} {shift:7.2f}  {rel}{flag}")
    base=_ev(feats,m1,m2,y1,y2)
    print(f"\n=== 재검: 전체 vs 정상대비만 (기준 26 S={base:.4f}) ===")
    rows=[("26+repol전체",np.concatenate([feats,Xr],1)),
          ("26+repol정상대비만",np.concatenate([feats,Xr[:,_REL_IDX]],1))]
    Xw=globals().get("_WST",None); Xm=globals().get("_MORPHO",None)
    if Xw is not None and Xm is not None:
        Xwk=np.nan_to_num(SelectKBest(f_classif,k=40).fit(np.nan_to_num(Xw[m1]),y1).transform(np.nan_to_num(Xw)))
        WM=np.concatenate([feats,Xwk,Xm],1)
        rows+=[("26+WST+morpho",WM),
               ("  +repol전체",np.concatenate([WM,Xr],1)),
               ("  +repol정상대비만",np.concatenate([WM,Xr[:,_REL_IDX]],1))]
    for nm,X in rows:
        S=_ev(X,m1,m2,y1,y2); print(f"  {nm:20s}: S={S:.4f}  (증분 {S-base:+.4f})")
    print("\n  → 절대 특징이 고단변량인데 이동도 크면: 단변량은 함정, 정상대비만 남기면 덜 깎임.")
    return Xr
