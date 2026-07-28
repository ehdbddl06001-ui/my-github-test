# =============================================================================
#  colab_step67_selfref.py  —  [STEP 67] 강건 자기-정상 템플릿 (라벨프리 개인화)
#
#  아이디어(사용자): 라벨을 안 쓰고, 환자 본인 초기/전체 파형에서 '정상 파형'을 스스로
#  분석해 기준(ref)으로. 초반이 비정상이어도 AI가 쓸 수 있는 파형을 골라 베이스를 만든다.
#  → 핵심통찰: 정상(동율동)은 거의 항상 다수(majority). 시간위치가 아니라 '가장 조밀한 형태
#    군집'을 정상으로 잡으면 소수 이소성/나쁜 초반에 안 흔들린다(robust M-estimator).
#
#  현재 모델은 ref=median(전체비트) → 이소성까지 섞여 흐릿. 이를 반복 절삭 템플릿으로 교체:
#   1) T0=median  2) 각 비트 상관거리로 인라이어(가까운 frac%)만 유지  3) T=인라이어 평균
#   4) 수렴까지 반복  5) 신뢰도(인라이어 상관 중앙값) 낮으면 median 폴백(플래그만 리포트)
#  라벨 0, 본인 파형만, 하이퍼파라미터는 DS1에서. → 오염 경계 깨끗.
#
#  A/B: 특징 고정, ref만 median vs robust-template 비교(순수 대조). 15seed 트림앙상블.
#  덤: 신뢰도 낮은 DS2 환자가 실제 AF/심방 환자와 겹치는지(방법이 스스로 어려운 환자를 아는가).
#
#  선행: colab_prep_all.py
#  실행:
#    exec(open('/content/drive/MyDrive/mitbih/colab_step67_selfref.py').read())
#    diag_selfref()                 # 신뢰도 분포·플래그 환자 확인(학습 불필요, 빠름)
#    run_selfref(fams=("RHYTHM","KOOPMAN","AE","GNN"))   # median vs robust A/B
# =============================================================================
import os
import numpy as np
from sklearn.metrics import average_precision_score, precision_recall_curve

_BASE="/content/drive/MyDrive/mitbih"; _FEATDIR=f"{_BASE}/synergy_feats"
_DS1=[101,106,108,109,112,114,115,116,118,119,122,124,201,203,205,207,208,209,215,220,223,230]
_DS2=[100,103,105,111,113,117,121,123,200,202,210,212,213,214,219,221,222,228,231,232,233,234]
# DS2 중 심방세동/조동·심방 활동 두드러진 레코드(참고용, 라벨 아님 — 플래그 검증에만)
_AF_REF=[202,210,219,221]

def _f1(y2,s):
    p,r,_=precision_recall_curve((y2==1).astype(int),s); f=2*p*r/(p+r+1e-9); i=int(np.nanargmax(f)); return p[i],r[i],f[i]
def auto_weights(y1,beta=0.9999):
    nN=(y1==0).sum(); nS=max((y1==1).sum(),1); eff=lambda n:(1-beta)/(1-beta**n+1e-12); return float(eff(nS)/eff(nN))
def _Lnpy(n):
    p=f"{_FEATDIR}/{n}.npy"; return np.load(p) if os.path.exists(p) else None
def _bestF(fams):
    d=np.load(f"{_BASE}/mamba_data.npz"); beats,y,pid=d["beat"],d["y"],d["pid"]
    BB=[_Lnpy(n) for n in ["feats0","WST","MORPHO","REPOL","DTW"]+list(fams)]
    if any(x is None for x in BB): raise RuntimeError("캐시 없음 → colab_prep_all.py 먼저")
    return beats,y,pid,np.concatenate(BB,1).astype("float32"),"+".join(fams)
def _determinism():
    import torch
    os.environ["CUBLAS_WORKSPACE_CONFIG"]=":4096:8"
    torch.backends.cudnn.deterministic=True; torch.backends.cudnn.benchmark=False
    try: torch.use_deterministic_algorithms(True, warn_only=True)
    except Exception as e: print("  det note:", type(e).__name__, e)

# ─────────────── 강건 자기-템플릿 ───────────────
def _corr_rows(X, t):
    """각 행(비트)과 템플릿 t의 피어슨 상관(진폭·오프셋 불변)."""
    Xc=X-X.mean(1,keepdims=True); tc=t-t.mean()
    num=(Xc*tc).sum(1); den=np.sqrt((Xc**2).sum(1))*np.sqrt((tc**2).sum())+1e-9
    return num/den

def _median_ref(beats, pid):
    r=np.empty_like(beats)
    for p in np.unique(pid): m=pid==p; r[m]=np.median(beats[m],0,keepdims=True)
    return r.astype("float32")

def robust_template(beats, pid, frac=0.6, n_iter=6, conf_cut=0.85, verbose=True):
    """환자별 반복 절삭 정상 템플릿. 신뢰도<conf_cut 이면 median 폴백(플래그).
       반환: ref(비트별 그 환자 템플릿), info=[(pid, conf, flagged, keep_frac)...]"""
    ref=np.empty_like(beats); info=[]
    for p in np.unique(pid):
        idx=np.where(pid==p)[0]; B=beats[idx].astype(np.float64); n=len(B)
        X=B.reshape(n,-1)                                   # (n, 2*300)
        T=np.median(B,0)                                    # 초기: 좌표별 median
        keep=np.ones(n,bool)
        for _ in range(n_iter):
            c=_corr_rows(X, T.reshape(-1))
            thr=np.quantile(c, 1.0-frac)                    # 상위 frac% 인라이어
            nk=c>=thr
            if nk.sum()<3: break
            Tn=B[nk].mean(0)
            done=np.array_equal(nk,keep); keep=nk; T=Tn
            if done: break
        cfin=float(np.median(_corr_rows(X, T.reshape(-1))[keep]))   # 신뢰도=인라이어 상관 중앙값
        flagged=cfin<conf_cut
        if flagged: T=np.median(B,0)                        # 폴백=기존 median(안전)
        ref[idx]=T[None].astype(beats.dtype)
        info.append((int(p), cfin, bool(flagged), float(keep.mean())))
    if verbose:
        d2=[x for x in info if x[0] in _DS2]
        fl=[x[0] for x in d2 if x[2]]
        print(f"  강건템플릿: frac={frac} conf_cut={conf_cut}  DS2 플래그(폴백) 환자={fl}")
        print(f"  참고 AF/심방 환자={_AF_REF}  → 겹침={sorted(set(fl)&set(_AF_REF))}  "
              f"(방법이 스스로 어려운 환자를 아는가)")
    return ref.astype("float32"), info

# ─────────────── 모델(기존 아키텍처 그대로) ───────────────
def _net(fdim):
    import torch, torch.nn as nn
    class Enc(nn.Module):
        def __init__(s):
            super().__init__(); s.net=nn.Sequential(
                nn.Conv1d(2,32,7,padding=3),nn.BatchNorm1d(32),nn.ReLU(),nn.MaxPool1d(2),
                nn.Conv1d(32,64,5,padding=2),nn.BatchNorm1d(64),nn.ReLU(),nn.MaxPool1d(2),
                nn.Conv1d(64,128,3,padding=1),nn.BatchNorm1d(128),nn.ReLU(),nn.AdaptiveAvgPool1d(1))
            s.proj=nn.Linear(128,64)
        def forward(s,w): return s.proj(s.net(w).squeeze(-1))
    class Net(nn.Module):
        def __init__(s):
            super().__init__(); s.e=Enc(); s.sia=nn.Sequential(nn.Linear(256,64),nn.ReLU())
            s.gate=nn.Linear(128,64); s.proto=nn.Parameter(torch.randn(32,64)*0.1)
            s.fm=nn.Sequential(nn.Linear(fdim,64),nn.ReLU(),nn.Linear(64,64),nn.ReLU())
            s.cls=nn.Sequential(nn.Linear(192,64),nn.ReLU(),nn.Linear(64,3))
        def forward(s,b,r,ft):
            z1=s.e(b); z2=s.e(r); zb=s.sia(torch.cat([z1,z2,z1-z2,(z1-z2).abs()],-1))
            z=z1+torch.sigmoid(s.gate(torch.cat([z1,zb],-1)))*zb
            zp=torch.softmax((z@s.proto.t())*(64**-0.5),-1)@s.proto
            return s.cls(torch.cat([z,zp,s.fm(ft)],-1))
    return Net()

def _train_seed(F, beats, ref, y, pid, mc, Sw, seed):
    """best-epoch DS2 예측 반환(ref만 다르게 넣어 A/B)."""
    import torch, torch.nn as nn, torch.nn.functional as Fn
    from sklearn.preprocessing import RobustScaler
    from sklearn.model_selection import GroupShuffleSplit
    dev="cuda" if torch.cuda.is_available() else "cpu"; m1=np.isin(pid,_DS1); m2=np.isin(pid,_DS2)
    b1,r1,f1a,y1,p1=beats[m1],ref[m1],F[m1],y[m1],pid[m1]; b2,r2,f2a=beats[m2],ref[m2],F[m2]
    torch.manual_seed(seed); np.random.seed(seed)
    tr,va=next(GroupShuffleSplit(1,test_size=0.2,random_state=seed).split(f1a,y1,groups=p1))
    sc=RobustScaler().fit(f1a[tr]); f1=np.nan_to_num(sc.transform(f1a),posinf=0,neginf=0).astype("float32"); f2=np.nan_to_num(sc.transform(f2a),posinf=0,neginf=0).astype("float32")
    M=_net(F.shape[1]).to(dev); opt=torch.optim.AdamW(M.parameters(),lr=1e-3,weight_decay=1e-4)
    cw=torch.tensor([1.,Sw,1.5],device=dev); mcv=torch.from_numpy(mc).to(dev)
    def met(p,yy): return 0.5*(average_precision_score((yy==1).astype(int),p[:,1])+average_precision_score((yy==2).astype(int),p[:,2]))
    @torch.no_grad()
    def pred(b,r,ft):
        M.eval(); o=[]
        for i in range(0,len(b),4096):
            o.append(torch.softmax(M(torch.from_numpy(b[i:i+4096]).to(dev),torch.from_numpy(r[i:i+4096]).to(dev),torch.from_numpy(ft[i:i+4096]).to(dev)),-1).cpu().numpy())
        return np.concatenate(o)
    Xtr=[torch.from_numpy(x) for x in (b1[tr],r1[tr],f1[tr],y1[tr])]
    ds=torch.utils.data.TensorDataset(*Xtr); dl=torch.utils.data.DataLoader(ds,batch_size=512,shuffle=True); best=-1; bs=None
    for ep in range(15):
        M.train()
        for bb,rr,ff,yy in dl:
            bb,rr,ff,yy=(t.to(dev) for t in (bb,rr,ff,yy)); opt.zero_grad()
            lo=M(bb,rr,ff); lg=lo-torch.zeros_like(lo).scatter_(1,yy[:,None],mcv[yy][:,None])
            ce=Fn.cross_entropy(lg,yy,reduction="none"); loss=(ce*cw[yy]).sum()/cw[yy].sum()
            loss.backward(); torch.nn.utils.clip_grad_norm_(M.parameters(),1.0); opt.step()
        pv=pred(b1[va],r1[va],f1[va]); v=met(pv,y1[va])
        if v>best: best=v; bs={k:vv.cpu() for k,vv in M.state_dict().items()}
    M.load_state_dict(bs); return pred(b2,r2,f2)

def _trim(Pn):
    if len(Pn)==1: P=Pn[0]; return P/P.sum(1,keepdims=True)
    medS=np.median(Pn[:,:,1],0); corr=np.array([np.corrcoef(Pn[i,:,1],medS)[0,1] for i in range(len(Pn))])
    keep=np.argsort(-corr)[:max(1,int(round(len(Pn)*0.8)))]; P=Pn[keep].mean(0); return P/P.sum(1,keepdims=True)

def diag_selfref(fams=("RHYTHM","KOOPMAN","AE","GNN"), frac=0.6, conf_cut=0.85):
    """학습 없이: 신뢰도 분포 + 플래그 환자 + median 대비 템플릿이 실제로 달라졌는지."""
    beats,y,pid,F,tag=_bestF(fams)
    refR,info=robust_template(beats,pid,frac=frac,conf_cut=conf_cut,verbose=True)
    refM=_median_ref(beats,pid)
    c1=np.array([x[1] for x in info if x[0] in _DS1]); c2=np.array([x[1] for x in info if x[0] in _DS2])
    print(f"\n  신뢰도(인라이어 상관 중앙값) 분포:")
    print(f"    DS1: 중앙 {np.median(c1):.3f}  [{c1.min():.3f}, {c1.max():.3f}]  (← conf_cut 은 DS1에서 정함)")
    print(f"    DS2: 중앙 {np.median(c2):.3f}  [{c2.min():.3f}, {c2.max():.3f}]")
    print(f"    DS1 5퍼센타일={np.percentile(c1,5):.3f}  → 이 근처를 conf_cut 후보로(권장)")
    # 템플릿이 median과 얼마나 달라졌나(비플래그 환자에서)
    dif=[]
    for p in np.unique(pid):
        if any(x[0]==p and x[2] for x in info): continue   # 폴백된 환자 제외
        m=pid==p; dif.append(float(np.abs(refR[m][0]-refM[m][0]).mean()))
    print(f"  비플래그 환자 |robust-median| 평균편차: {np.mean(dif):.4f} (0이면 median과 동일=효과없음)")
    return info

def run_selfref(fams=("RHYTHM","KOOPMAN","AE","GNN"), seeds=None, frac=0.6, conf_cut=0.85):
    _determinism()
    seeds=list(seeds) if seeds is not None else list(range(2000,2015))
    beats,y,pid,F,tag=_bestF(fams)
    m1=np.isin(pid,_DS1); m2=np.isin(pid,_DS2); y2=y[m2]
    Sw=auto_weights(y[m1]); nc=np.array([(y[m1]==k).sum() for k in range(3)],np.float32); mc=(1.0/np.power(nc,0.25)); mc=(mc/mc.max()*0.5).astype("float32")
    refM=_median_ref(beats,pid)
    refR,info=robust_template(beats,pid,frac=frac,conf_cut=conf_cut,verbose=True)
    def sm(p): S=average_precision_score((y2==1).astype(int),p[:,1]); V=average_precision_score((y2==2).astype(int),p[:,2]); pr,se,f1=_f1(y2,p[:,1]); return S,pr,se,f1,V
    print(f"\n백본: feats0+WST+MORPHO+REPOL+DTW+{tag}  결정성 ON  {len(seeds)}seed  Sw={Sw:.2f}")
    RES={}
    for nm,ref in [("median(기존)",refM),("robust-template(라벨프리)",refR)]:
        P=np.stack([_train_seed(F,beats,ref,y,pid,mc,Sw,s) for s in seeds],0)
        per=np.array([sm(p) for p in P]); lbl=["S_PR","PREC","SEN","F1","V_PR"]
        print(f"\n=== {nm} — 개별 시드 분포 ===")
        for i,l in enumerate(lbl):
            v=per[:,i]; print(f"  {l:5s}: 평균 {v.mean():.4f} ± {v.std():.4f}  [최소 {v.min():.4f}, 최대 {v.max():.4f}]")
        S,pr,se,f1,V=sm(_trim(P)); print(f"  트림앙상블: S_PR={S:.4f} PREC={pr:.3f} SEN={se:.3f} F1={f1:.3f}  V_PR={V:.4f}")
        RES[nm]=(_trim(P), per)
    a=sm(RES["median(기존)"][0]); b=sm(RES["robust-template(라벨프리)"][0])
    print(f"\n▶ robust vs median (트림앙상블): ΔS_PR={b[0]-a[0]:+.4f} ΔPREC={b[1]-a[1]:+.3f} ΔSEN={b[2]-a[2]:+.3f} ΔF1={b[3]-a[3]:+.4f} ΔV_PR={b[4]-a[4]:+.4f}")
    print(f"  ★ ΔF1>0 & 개별 σ 안 커짐 = 라벨프리 자기-템플릿이 정직하게 개인화 이득. 채택.")
    print(f"    (conf_cut 은 DS1에서 정한 값 고정 — DS2로 튜닝 금지. diag_selfref 의 DS1 5퍼센타일 참고)")
    return dict(res=RES, info=info)
