# =============================================================================
#  colab_step10_denoise.py  —  [STEP 10] 벡터 일관성 P파 분리(denoise) + 개인함수
#
#  15seed 결과: 크루드 P파 8특징은 CNN을 못 이김(CNN이 raw에서 이미 추출).
#  → CNN이 '스스로 못 만드는' 것을 줘야 함 = 겹친 신호를 분리한 깨끗한 P.
#
#  사장님 아이디어 구현 (전부 환자 정상 기준 = 개인 함수):
#   1) 환자 정상 QRS·T 템플릿을 스케일 맞춰 빼기 → residual = P + 노이즈 + 오차
#   2) 벡터 방향 일관성으로 분리:
#      · 환자 정상 P축 θ_p (정상 beat의 P영역 벡터 평균방향)
#      · coh(t)=resid·(cosθ_p,sinθ_p)  = 정상축 정렬성분(진짜 기대 P)
#      · perp(t)=resid·(-sinθ_p,cosθ_p) = 축 이탈성분(노이즈/이소성)
#      · 저역통과 smooth(P파는 매끈, 노이즈는 고주파) → 노이즈 제거
#   3) 분리된 깨끗한 P에서 벡터 특징: coherence비, 이탈에너지, 위치, 극성 등
#      SVEB=이소성→정상축 coherence↓·이탈에너지↑ (판별)
#
#  검증: 크루드8 vs denoise8 의 '증분' 비교 (로지스틱, label-free ref).
#        denoise가 더 크면 → CNN이 못 뽑던 정보 → CNN 테스트 가치.
#
#  실행:
#    exec(open('.../colab_step9_pwave.py').read())        # extract_pwave_features(크루드)
#    exec(open('.../colab_step10_denoise.py').read())
#    diag_denoise()
# =============================================================================
import numpy as np
from scipy.ndimage import uniform_filter1d
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score, roc_auc_score

_DS1=[101,106,108,109,112,114,115,116,118,119,122,124,201,203,205,207,208,209,215,220,223,230]
_DS2=[100,103,105,111,113,117,121,123,200,202,210,212,213,214,219,221,222,228,231,232,233,234]

def _allbeat_median_ref(beats,pid):
    r=np.empty_like(beats)
    for p in np.unique(pid):
        m=pid==p; r[m]=np.median(beats[m],axis=0,keepdims=True)
    return r.astype("float32")

def extract_pwave_denoised(beats,refs,pid):
    """벡터 일관성으로 P를 노이즈에서 분리 후 특징. refs=환자 정상 기준(개인함수)."""
    N=len(beats); F=np.zeros((N,8),dtype=np.float32); eps=1e-6
    for p in np.unique(pid):
        idx=np.where(pid==p)[0]; b=beats[idx]; r=refs[idx]        # [n,2,300]
        VMr=np.sqrt(r[:,0]**2+r[:,1]**2); L=VMr.shape[1]; R=int(np.argmax(VMr[0]))
        Ps,Pe=max(0,R-95),max(3,R-15)                            # 넓은 P 탐색(이동 대비)
        Qs,Qe=max(0,R-25),min(L,R+25); Ts,Te=min(L-2,R+30),min(L,R+130)
        # 환자 정상 P축 θ_p (정상 P영역 벡터 평균방향)
        angr=np.arctan2(r[0,1,Ps:Pe],r[0,0,Ps:Pe]); wgt=VMr[0,Ps:Pe]
        th=np.arctan2((wgt*np.sin(angr)).sum(),(wgt*np.cos(angr)).sum())
        ct,st=np.cos(th),np.sin(th)
        # QRS 스케일로 정상 제거 → residual (per lead)
        qE=np.sqrt(b[:,0,Qs:Qe]**2+b[:,1,Qs:Qe]**2).sum(1)
        qEr=np.sqrt(r[:,0,Qs:Qe]**2+r[:,1,Qs:Qe]**2).sum(1)
        scale=(qE/(qEr+eps))[:,None]
        res0=b[:,0]-scale*r[:,0]; res1=b[:,1]-scale*r[:,1]        # [n,300]
        coh = res0*ct+res1*st                                    # 정상축 정렬(진짜 기대 P)
        perp=-res0*st+res1*ct                                    # 축 이탈(노이즈/이소성)
        coh_s=uniform_filter1d(coh,size=11,axis=1)               # 저역통과 denoise
        # 정상 자신의 coh(기준화용)
        cohr=(r[:,0]*ct+r[:,1]*st); cohr_s=uniform_filter1d(cohr,size=11,axis=1)
        Pr=slice(Ps,Pe); Tr=slice(Ts,Te)
        cohE=(coh_s[:,Pr]**2).sum(1); perpE=(perp[:,Pr]**2).sum(1)
        cohEr=(cohr_s[:,Pr]**2).sum(1)
        f1=cohE/(qE**2+eps)                                      # ① 정렬(진짜)P 에너지
        f2=perpE/(qE**2+eps)                                     # ② 이탈(노이즈/이소성) 에너지
        f3=cohE/(cohE+perpE+eps)                                 # ③ coherence비(1=깨끗한 정상P,낮음=이소성/노이즈)
        f4=cohE/(cohEr+eps)                                      # ④ 정상 대비 P 세기
        peak=np.argmax(np.abs(coh_s[:,Pr]),1)
        f5=peak.astype(np.float32)-np.argmax(np.abs(cohr_s[:,Pr]),1)   # ⑤ P 위치이동(조기성)
        f6=coh_s[np.arange(len(idx)),Ps+peak]                    # ⑥ P 극성·진폭(이소성은 역전 가능)
        f7=(coh_s[:,Tr]**2).sum(1)/(qE**2+eps)                   # ⑦ T영역 정렬성분(P-on-T 숨은 P)
        f8=perpE/(cohE+eps)                                      # ⑧ 노이즈/신호 비(SNR 역수)
        F[idx]=np.stack([f1,f2,f3,f4,f5,f6,f7,f8],1)
    return np.nan_to_num(F,posinf=0,neginf=0).astype("float32")

def _evalset(X,m1,m2,y1,y2):
    sc=StandardScaler().fit(np.nan_to_num(X[m1]))
    X1=np.nan_to_num(sc.transform(np.nan_to_num(X[m1]))); X2=np.nan_to_num(sc.transform(np.nan_to_num(X[m2])))
    clf=LogisticRegression(max_iter=5000,C=1.0,class_weight={0:1,1:3,2:1.5}).fit(X1,y1)
    p2=clf.predict_proba(X2)
    return (average_precision_score((y2==1).astype(int),p2[:,1]),average_precision_score((y2==2).astype(int),p2[:,2]))

def diag_denoise():
    d=np.load("/content/drive/MyDrive/mitbih/mamba_data.npz")
    beats,feats,y,pid=d["beat"],d["feats"],d["y"],d["pid"]
    ref_lf=_allbeat_median_ref(beats,pid)                        # label-free 정상 기준
    m1=np.isin(pid,_DS1); m2=np.isin(pid,_DS2); y1,y2=y[m1],y[m2]
    Xcrude=extract_pwave_features(beats,ref_lf,pid)             # step9 크루드
    Xden  =extract_pwave_denoised(beats,ref_lf,pid)            # step10 분리
    base=_evalset(feats,m1,m2,y1,y2)
    print(f"기준선 26개만: S={base[0]:.4f}  V={base[1]:.4f}  (label-free ref)\n")
    for nm,X in [("26 + 크루드P파8",np.concatenate([feats,Xcrude],1)),
                 ("26 + 분리(denoise)P파8",np.concatenate([feats,Xden],1)),
                 ("26 + 크루드8 + 분리8",np.concatenate([feats,Xcrude,Xden],1))]:
        S,V=_evalset(X,m1,m2,y1,y2)
        print(f"  {nm:24s}: S={S:.4f}(증분 {S-base[0]:+.4f})  V={V:.4f}")
    # 분리 특징 단변량 판별력
    print("\n분리 특징 단변량 S ROC-AUC:")
    names=["정렬P에너지","이탈에너지","coherence비","정상대비P","P위치이동","P극성진폭","T영역정렬(P-on-T)","노이즈/신호비"]
    Xd2=Xden[m2]
    for k,n in enumerate(names):
        c=Xd2[:,k]
        if np.std(c)<1e-9: print(f"  {n:16s}: (상수)"); continue
        a=roc_auc_score((y2==1).astype(int),c); a=max(a,1-a)
        print(f"  {n:16s}: {a:.3f}  {'█'*int((a-0.5)*40)}")
    print("\n  → '분리8' 증분이 '크루드8'보다 크면: 벡터분리가 CNN이 못뽑던 정보 추가 → CNN 테스트 가치")
