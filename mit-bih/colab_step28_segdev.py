# =============================================================================
#  colab_step28_segdev.py  —  [STEP 28] 개인 정상 대비 '분절별' 매치드필터/편차
#
#  (가) 개인화 P구간 매치드필터 + 사장님 아이디어(T-P-R 분절을 잘라 개인 정상 리듬과 비교).
#  Farag whole-beat MF는 S/N 둘 다 QRS 같아 실패(step27). 여기선 QRS 빼고 P·PR·ST·T에
#  집중 + 전부 환자 자신의 정상(ref) 대비 = S vs N(정밀도) 정면 공략.
#
#  11특징(전부 개인 정상 대비):
#   P상관·P지연·P에너지 / T상관·T지연·T에너지 / P-T혼동 / PR간격편차 / QRS-T시작편차 / ST상관 / 분절총편차
#   · P상관↓·P지연≠0 = 비정상/조기 P   · QRS-T편차 = 느린 회복   · PR편차 = 전도이상   · P-T혼동 = P가 T닮음
#
#  ★ 검증: best(26+WST+morpho+repolK) 위에 얹어 살아남나 + 단일특징 스캔.
#  선행 로드: step12(_WST)·step15(extract_morpho)·step18(extract_repol)
#  실행:
#    exec(open('/content/drive/MyDrive/mitbih/colab_step28_segdev.py').read())
#    diag_segdev()
# =============================================================================
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.metrics import average_precision_score, roc_auc_score

_DS1=[101,106,108,109,112,114,115,116,118,119,122,124,201,203,205,207,208,209,215,220,223,230]
_DS2=[100,103,105,111,113,117,121,123,200,202,210,212,213,214,219,221,222,228,231,232,233,234]
_REPOLK_IDX=[0,1,4,5]
SEG_NAMES=["P상관","P지연","P에너지","T상관","T지연","T에너지","P-T혼동","PR간격편차","QRS-T시작편차","ST상관","분절총편차"]

def _allbeat_median_ref(beats,pid):
    r=np.empty_like(beats)
    for p in np.unique(pid):
        m=pid==p; r[m]=np.median(beats[m],axis=0,keepdims=True)
    return r.astype("float32")

def extract_segdev_features(beats,refs,pid,W=18,maxlag=8):
    """분절별 개인정상 대비. refs=환자 median(개인 리듬 기준)."""
    N=len(beats); F=np.zeros((N,11),np.float32); eps=1e-6
    def corr(bw,rw):                                   # bw:(n,Wl) rw:(Wl,) 정규화 상관
        a=bw-bw.mean(-1,keepdims=True); c=rw-rw.mean()
        return (a*c).sum(-1)/(np.sqrt((a**2).sum(-1))*np.sqrt((c**2).sum())+eps)
    for p in np.unique(pid):
        idx=np.where(pid==p)[0]; b=beats[idx]
        VMb=np.sqrt(b[:,0]**2+b[:,1]**2)               # (n,L)
        rr=refs[idx][0]; VMr=np.sqrt(rr[0]**2+rr[1]**2) # 환자 정상 VM (L,)
        L=VMb.shape[1]; R=int(np.argmax(VMr)); thr=0.3*VMr[R]
        q_on=R
        while q_on>0 and VMr[q_on]>thr: q_on-=1
        q_off=R
        while q_off<L-1 and VMr[q_off]>thr: q_off+=1
        Ps,Pe=max(0,R-70),max(2,q_on-2); p_pk=Ps+int(np.argmax(VMr[Ps:Pe])) if Pe>Ps+1 else max(1,R-40)
        Ts,Te=min(L-2,q_off+2),min(L,R+140); t_pk=Ts+int(np.argmax(VMr[Ts:Te])) if Te>Ts+1 else min(L-2,R+80)
        st_c=int((q_off+t_pk)//2)
        def win1(sig,c):                               # 1D ref 윈도 (2W+1,)
            s=int(np.clip(c-W,0,L-(2*W+1))); return sig[s:s+2*W+1]
        def winN(c):                                   # 비트 윈도 (n,2W+1)
            s=int(np.clip(c-W,0,L-(2*W+1))); return VMb[:,s:s+2*W+1]
        rP,rT,rST=win1(VMr,p_pk),win1(VMr,t_pk),win1(VMr,st_c)
        bP,bT,bST=winN(p_pk),winN(t_pk),winN(st_c)
        P_corr,T_corr,ST_corr=corr(bP,rP),corr(bT,rT),corr(bST,rST)
        PT=corr(bP,rT)                                 # P구간이 정상 T를 닮았나 (P-T 혼동)
        def lag(c,rw):                                 # 정상 템플릿을 비트 넓은창서 슬라이딩 → 최적 지연
            s=int(np.clip(c-W-maxlag,0,L-(2*W+1+2*maxlag))); wide=VMb[:,s:s+2*W+1+2*maxlag]
            c0=rw-rw.mean(); best=np.full(len(idx),-2.0,np.float32); bl=np.zeros(len(idx),np.float32)
            for dd in range(0,2*maxlag+1):
                seg=wide[:,dd:dd+2*W+1]; a=seg-seg.mean(1,keepdims=True)
                cc=(a*c0).sum(1)/(np.sqrt((a**2).sum(1))*np.sqrt((c0**2).sum())+eps)
                m=cc>best; best[m]=cc[m]; bl[m]=dd-maxlag
            return bl
        P_lag,T_lag=lag(p_pk,rP),lag(t_pk,rT)
        Ev=lambda c: VMb[:,max(0,c-W):c+W+1].sum(1)
        Er=lambda c: VMr[max(0,c-W):c+W+1].sum()
        P_e,T_e=Ev(p_pk)/(Er(p_pk)+eps),Ev(t_pk)/(Er(t_pk)+eps)
        bp=Ps+np.argmax(VMb[:,Ps:Pe],1) if Pe>Ps+1 else np.full(len(idx),p_pk)   # 비트 P피크 위치
        bt=Ts+np.argmax(VMb[:,Ts:Te],1) if Te>Ts+1 else np.full(len(idx),t_pk)
        PR_dev=(p_pk-bp).astype(np.float32)            # 정상대비 P가 얼마나 이동(조기/전도)
        QT_dev=(bt-t_pk).astype(np.float32)            # 정상대비 T시작 이동(회복 느림/빠름)
        seg_tot=np.abs(bP-rP).sum(-1)/(np.abs(rP).sum()+eps)+np.abs(bT-rT).sum(-1)/(np.abs(rT).sum()+eps)
        F[idx]=np.stack([P_corr,P_lag,P_e,T_corr,T_lag,T_e,PT,PR_dev,QT_dev,ST_corr,seg_tot],1)
    return np.nan_to_num(F,posinf=0,neginf=0).astype("float32")

def _load():
    d=np.load("/content/drive/MyDrive/mitbih/mamba_data.npz"); return d["beat"],d["feats"],d["y"],d["pid"]
def _ev(X,m1,m2,y1,y2):
    sc=StandardScaler().fit(np.nan_to_num(X[m1]))
    X1=np.nan_to_num(sc.transform(np.nan_to_num(X[m1]))); X2=np.nan_to_num(sc.transform(np.nan_to_num(X[m2])))
    clf=LogisticRegression(max_iter=5000,C=0.5,class_weight={0:1,1:3,2:1.5}).fit(X1,y1)
    return average_precision_score((y2==1).astype(int),clf.predict_proba(X2)[:,1])

def diag_segdev():
    beats,feats,y,pid=_load(); ref=_allbeat_median_ref(beats,pid)
    Xs=extract_segdev_features(beats,ref,pid)
    m1=np.isin(pid,_DS1); m2=np.isin(pid,_DS2); y1,y2=y[m1],y[m2]
    print("=== segdev 11특징 단변량 S ROC-AUC (DS2) ===")
    for k,nm in enumerate(SEG_NAMES):
        c=Xs[m2,k]
        if np.std(c)<1e-9: print(f"  {nm:12s}: (상수)"); continue
        a=roc_auc_score((y2==1).astype(int),c); a=max(a,1-a); print(f"  {nm:12s}: {a:.3f}  {'█'*int((a-0.5)*40)}")
    base=_ev(feats,m1,m2,y1,y2)
    Xw=globals().get("_WST",None); Xm=globals().get("_MORPHO",None); Xr=globals().get("_REPOL",None)
    print(f"\n=== 로지스틱 증분 (기준 26 S={base:.4f}) ===")
    for nm,X in [("segdev11만",Xs),("26+segdev",np.concatenate([feats,Xs],1))]:
        print(f"  {nm:16s}: S={_ev(X,m1,m2,y1,y2):.4f}")
    if Xw is not None and Xm is not None and Xr is not None:
        Xwk=np.nan_to_num(SelectKBest(f_classif,k=40).fit(np.nan_to_num(Xw[m1]),y1).transform(np.nan_to_num(Xw)))
        BEST=np.concatenate([feats,Xwk,Xm,Xr[:,_REPOLK_IDX]],1); bS=_ev(BEST,m1,m2,y1,y2)
        print(f"  {'best':16s}: S={bS:.4f}")
        print(f"  {'best+segdev':16s}: S={_ev(np.concatenate([BEST,Xs],1),m1,m2,y1,y2):.4f}")
        print(f"\n=== best 위 단일특징 스캔 (부호일관·노이즈바닥 초과 봐야) ===")
        for k,nm in enumerate(SEG_NAMES):
            S=_ev(np.concatenate([BEST,Xs[:,[k]]],1),m1,m2,y1,y2)
            print(f"  +{nm:12s}: {S:.4f} ({S-bS:+.4f})  {'★' if S>bS else ''}")
        print("\n  ★ best 위에서 오르는 특징(특히 P상관·P-T혼동·QRS-T편차)이 있으면 → 정밀도용 신호 → CNN 승격.")
    else:
        print("\n  (best 비교하려면 step12·15·18 먼저 로드해 _WST·_MORPHO·_REPOL 캐시)")
    global _SEGDEV; _SEGDEV=Xs
    return Xs
