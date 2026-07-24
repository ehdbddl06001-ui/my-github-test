# =============================================================================
#  colab_step48_rhythm.py  —  [STEP 48] 리듬 예측잔차(innovation) 특징 — 사장님 SDE/LSTM 아이디어
#
#  아이디어: 개인 정상 리듬은 예측가능한 동역학(선형 SDE=칼만). 그 예측을 벗어나는 '델타'=
#  외부작용을 받은 신호 = 이소성(S/V). 지금까지 우린 '정적 개인기준(_REF)'만 썼고 시간순
#  시퀀스는 안 봄. 여기선 각 환자 자기 시퀀스에 자기지도로 인과예측(EWMA=이산 선형SDE) →
#  예측잔차(innovation)를 특징화. 라벨 불필요(DS2도 자기 리듬만) → inter-patient 깨끗(Setting A).
#   · 형태 innovation(자립): P/QRS/T 잔차E, 국소-K 놀람, 예측상관, 점프
#   · 타이밍 innovation: RR 정규화잔차(조기성), 보상휴지, (pre+post-2·예측)=보상성지수(S≪0,V≈0)
#     RR 컬럼은 'innov가 S에 가장 크게 반응'하는 feats0 컬럼으로 DS1에서 자동식별(오염 없음).
#  ※ 무파라미터 예측기부터(과적합 회피). 신호 확인되면 LSTM(학습판) 후속 비교.
#
#  선행 캐시(diag 비교용): _WST,_MORPHO,_REPOL,_DTW
#  실행:
#    exec(open('/content/drive/MyDrive/mitbih/colab_step48_rhythm.py').read())
#    diag_rhythm()          # 자동식별 RR컬럼 출력 + 단일스캔 + best 위 증분. 캐시 _RHYTHM
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
RHY_NAMES=["형태잔차P","형태잔차T","형태잔차총","국소놀람K","예측상관역","형태점프",
           "RR조기성","RR조기성abs","보상휴지","보상성지수(S<<0)"]

def _ewma_causal(X, alpha):
    """인과 EWMA: pred[t]=과거(<t)만의 지수평활. X:(n,...) 시퀀스축=0. pred[t]는 t를 안 봄."""
    pred=np.zeros_like(X); acc=X[0].copy()
    for t in range(1,len(X)):
        pred[t]=acc; acc=alpha*X[t]+(1-alpha)*acc
    pred[0]=X[0]; return pred

def _segwin(R,L):
    return {"P":(max(0,R-90),max(3,R-25)),"QRS":(max(0,R-25),min(L,R+25)),"T":(min(L-2,R+30),min(L,R+130))}

def extract_rhythm_features(beats, feats0, pid, y=None, alpha=0.3, K=8, pre_col=None, post_col=None, verbose=True):
    if y is None: y=np.load(f"{_BASE}/mamba_data.npz")["y"]
    N=len(beats); eps=1e-6; m1=np.isin(pid,_DS1)
    # ── 타이밍 컬럼 자동식별: feats0 각 컬럼의 인과 innovation이 DS1에서 S에 얼마나 반응하나 ──
    innovF=np.zeros_like(feats0,dtype=np.float32)
    for p in np.unique(pid):
        idx=np.where(pid==p)[0]; X=feats0[idx].astype(np.float64)
        pred=_ewma_causal(X,alpha); res=X-pred
        scale=np.median(np.abs(X-np.median(X,0,keepdims=True)),0,keepdims=True)+eps
        innovF[idx]=(res/scale).astype(np.float32)
    if pre_col is None or post_col is None:
        meanS=np.array([innovF[m1&(y==1),c].mean() for c in range(feats0.shape[1])])  # DS1 S beat 평균 innov
        pc=int(np.argmin(meanS)); qc=int(np.argmax(meanS))                            # 조기(음) / 휴지(양)
        pre_col=pc if pre_col is None else pre_col; post_col=qc if post_col is None else post_col
        if verbose:
            print(f"  [자동식별] pre(조기)=feats0[{pre_col}] meanInnov@S={meanS[pre_col]:+.2f}  "
                  f"post(휴지)=feats0[{post_col}] meanInnov@S={meanS[post_col]:+.2f}")
    F=np.zeros((N,10),np.float32)
    for p in np.unique(pid):
        idx=np.where(pid==p)[0]; b=beats[idx]
        VM=np.sqrt(b[:,0]**2+b[:,1]**2).astype(np.float64)          # (n,L)
        L=VM.shape[1]; R=int(np.argmax(np.median(VM,0))); w=_segwin(R,L)
        pred=_ewma_causal(VM,alpha); res=VM-pred                    # 형태 예측잔차
        qE=VM[:,w["QRS"][0]:w["QRS"][1]].__abs__().sum(1)+eps
        F[idx,0]=np.abs(res[:,w["P"][0]:w["P"][1]]).sum(1)/qE       # 형태잔차 P
        F[idx,1]=np.abs(res[:,w["T"][0]:w["T"][1]]).sum(1)/qE       # 형태잔차 T
        F[idx,2]=np.abs(res).sum(1)/(np.abs(VM).sum(1)+eps)         # 형태잔차 총
        # 국소-K 놀람: 직전 K개 중앙형태 대비 거리
        for i in range(len(idx)):
            lo=max(0,i-K); ref=np.median(VM[lo:i],0) if i>0 else VM[i]
            F[idx[i],3]=np.sqrt(((VM[i]-ref)**2).mean())/(np.sqrt((ref**2).mean())+eps)
        # 예측상관역(1-corr): 예측과 안 닮을수록 큼
        pm=pred-pred.mean(1,keepdims=True); vm=VM-VM.mean(1,keepdims=True)
        cc=(pm*vm).sum(1)/(np.sqrt((pm**2).sum(1))*np.sqrt((vm**2).sum(1))+eps)
        F[idx,4]=1-cc
        F[idx,5]=np.abs(res).sum(1)/ (np.abs(np.vstack([res[:1],res[:-1]])).sum(1)+eps)  # 형태 점프(직전 대비)
        # 타이밍 innovation (자동식별 컬럼)
        pr=innovF[idx,pre_col]; po=innovF[idx,post_col]
        F[idx,6]=pr; F[idx,7]=np.abs(pr); F[idx,8]=po; F[idx,9]=pr+po                    # 보상성지수: S불완전≪0, V완전≈0
    return np.nan_to_num(F,posinf=0,neginf=0).astype("float32")

def _ev(X,m1,m2,y1,y2):
    sc=StandardScaler().fit(np.nan_to_num(X[m1]))
    X1=np.nan_to_num(sc.transform(np.nan_to_num(X[m1]))); X2=np.nan_to_num(sc.transform(np.nan_to_num(X[m2])))
    clf=LogisticRegression(max_iter=5000,C=0.5,class_weight={0:1,1:3,2:1.5}).fit(X1,y1)
    return average_precision_score((y2==1).astype(int),clf.predict_proba(X2)[:,1])

def diag_rhythm():
    d=np.load(f"{_BASE}/mamba_data.npz"); beats,feats0,y,pid=d["beat"],d["feats"],d["y"],d["pid"]
    m1=np.isin(pid,_DS1); m2=np.isin(pid,_DS2); y1,y2=y[m1],y[m2]
    print("리듬 innovation 특징 계산(인과 EWMA)...")
    Xrh=extract_rhythm_features(beats,feats0,pid,y)
    print(f"\n=== 리듬 10특징: DS2 단변량 S 판별력 ===")
    for k,nm in enumerate(RHY_NAMES):
        c=Xrh[m2,k]
        if np.std(c)<1e-9: print(f"  {nm:14s}: (상수)"); continue
        a=roc_auc_score((y2==1).astype(int),c); a=max(a,1-a)
        print(f"  {nm:14s}: AUC={a:.3f}  {'█'*int((a-0.5)*40)}")
    Xw=globals().get("_WST"); Xm=globals().get("_MORPHO"); Xr=globals().get("_REPOL"); Xd=globals().get("_DTW")
    Xwk=np.nan_to_num(SelectKBest(f_classif,k=40).fit(np.nan_to_num(Xw[m1]),y1).transform(np.nan_to_num(Xw)))
    BEST=np.concatenate([feats0,Xwk,Xm,Xr[:,_REPOLK_IDX],Xd],1); bS=_ev(BEST,m1,m2,y1,y2)
    print(f"\n=== best+DTW 위 증분 (best S={bS:.4f}) ===")
    pos=[]
    for k,nm in enumerate(RHY_NAMES):
        S=_ev(np.concatenate([BEST,Xrh[:,[k]]],1),m1,m2,y1,y2)
        if S>bS+1e-4: pos.append(k)
        print(f"  +{nm:14s}: S={S:.4f} ({S-bS:+.4f})  {'★' if S>bS+1e-4 else ''}")
    print(f"\n  +리듬 10개 전부 : S={_ev(np.concatenate([BEST,Xrh],1),m1,m2,y1,y2):.4f}")
    if pos: print(f"  +양성만{tuple(pos)}: S={_ev(np.concatenate([BEST,Xrh[:,pos]],1),m1,m2,y1,y2):.4f}")
    print(f"\n  ★ ΔS>0 있으면 시퀀스 예측잔차가 정적기준 위에 정보 추가 → STEP47 sweep에 RHYTHM 군 편입/CNN 승격.")
    print(f"     특히 '보상성지수'가 강하면 S/V 분리에도 기여(APC 불완전 vs PVC 완전 보상휴지).")
    global _RHYTHM; _RHYTHM=Xrh
    return dict(bS=bS,pos=pos)
