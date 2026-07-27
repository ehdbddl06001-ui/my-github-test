# =============================================================================
#  colab_step68_oppoint.py  —  [STEP 68] DS1-최적화 동작점 함수 (SEN 상승 + 오라클 누출 제거)
#
#  문제: 지금까지 SEN/PREC/F1 은 DS2 라벨로 F1최적 임계를 고른 '오라클 임계'(작은 누출).
#        게다가 임계가 고정 스칼라 → 환자별 점수 baseline 차이를 못 흡수(inter-patient 근본문제).
#  해결: 동작점을 '환자별로 변하는 함수'로 만들고 그 파라미터를 DS1 에서만 최적화 → DS2 동결적용.
#    A. 고정         : t=argmax F1(DS1-OOF)                 (정직 베이스라인, 오라클 누출 제거)
#    B. 목표-SEN     : DS1-OOF SEN=target 되는 t             (SEN 다이얼)
#    C. 환자별 적응  : 결정점 = s - median_p(s) 후 전역 t    (★변수 자체가 바뀌는 함수, 무라벨)
#    D. 공변량-선형  : t_i = t0 + β·z_i (z=강건템플릿 신뢰도) (학습형, 실험적)
#  무결성: 임계용 DS1 점수는 GroupKFold(5) out-of-fold(모든 DS1 환자 정확히 1회 held-out).
#          DS2 절대 안 봄. 오라클(DS2 F1최적)은 '상한 참고'로만 나란히.
#  ★ 발견(val≠test) 때문에 DS1→DS2 전이 갭을 반드시 같이 본다: DS1-OOF 값과 DS2 값을 병기.
#
#  선행: colab_prep_all.py + colab_step67_selfref.py (Drive)
#  실행:
#    exec(open('/content/drive/MyDrive/mitbih/colab_step68_oppoint.py').read())
#    run_oppoint(target_sen=0.82)     # 3seed × GroupKFold5 = 15 학습(STEP67과 동일 예산)
# =============================================================================
import os
import numpy as np
from sklearn.metrics import average_precision_score

_BASE="/content/drive/MyDrive/mitbih"
# STEP67 재사용(robust_template·_net·_bestF·_median_ref·auto_weights·_DS1/_DS2·_determinism)
if "robust_template" not in globals():
    exec(open(f"{_BASE}/colab_step67_selfref.py").read(), globals())

# ─────────────── 동작점(threshold) 유틸: S(1) vs rest 이진 ───────────────
def _binmet(s, y, t):
    pos=s>=t; yp=(y==1)
    tp=float((pos&yp).sum()); fp=float((pos&~yp).sum()); fn=float((~pos&yp).sum())
    prec=tp/(tp+fp+1e-9); sen=tp/(tp+fn+1e-9); f1=2*prec*sen/(prec+sen+1e-9)
    return prec,sen,f1

def _best_t_f1(s, y, n=300):
    ts=np.unique(np.quantile(s, np.linspace(0.50,0.9995,n)))
    best=(-1.0, ts[0])
    for t in ts:
        f1=_binmet(s,y,t)[2]
        if f1>best[0]: best=(f1,t)
    return float(best[1])

def _t_for_sen(s, y, target, n=800):
    """DS1-OOF에서 SEN>=target 만족하는 임계 중 가장 높은 것(=PREC 최대)."""
    ts=np.unique(np.quantile(s, np.linspace(0.001,0.9995,n)))
    ok=[t for t in ts if _binmet(s,y,t)[1]>=target]
    return float(max(ok)) if ok else float(ts[0])

def _logit(s): s=np.clip(s,1e-6,1-1e-6); return np.log(s/(1-s))

def _pp_center(s, pid):
    """환자별 baseline 제거(로짓에서 본인 중앙값 빼기) → 동작점이 환자별로 이동. 무라벨."""
    l=_logit(s); out=l.copy()
    for p in np.unique(pid):
        m=pid==p; out[m]=l[m]-np.median(l[m])
    return out

# ─────────────── OOF 학습: DS1 held-out 점수 + DS2 예측 ───────────────
def _train_fold(F, beats, ref, y, pid, mc, Sw, tr_idx, va_idx, m2_idx, seed):
    """tr로 학습(best-epoch by va내부split), va(=held-out DS1)와 DS2 예측 반환."""
    import torch, torch.nn as nn, torch.nn.functional as Fn
    from sklearn.preprocessing import RobustScaler
    from sklearn.model_selection import GroupShuffleSplit
    dev="cuda" if torch.cuda.is_available() else "cpu"
    bT,rT,fTa,yT,pT=beats[tr_idx],ref[tr_idx],F[tr_idx],y[tr_idx],pid[tr_idx]
    bV,rV,fVa=beats[va_idx],ref[va_idx],F[va_idx]
    b2,r2,f2a=beats[m2_idx],ref[m2_idx],F[m2_idx]
    torch.manual_seed(seed); np.random.seed(seed)
    # 학습 내부에서 다시 작은 val로 best-epoch (tr 그룹 기준)
    it,iv=next(GroupShuffleSplit(1,test_size=0.2,random_state=seed).split(fTa,yT,groups=pT))
    sc=RobustScaler().fit(fTa[it])
    f_tr=np.nan_to_num(sc.transform(fTa),posinf=0,neginf=0).astype("float32")
    f_v =np.nan_to_num(sc.transform(fVa),posinf=0,neginf=0).astype("float32")
    f_2 =np.nan_to_num(sc.transform(f2a),posinf=0,neginf=0).astype("float32")
    M=_net(F.shape[1]).to(dev); opt=torch.optim.AdamW(M.parameters(),lr=1e-3,weight_decay=1e-4)
    cw=torch.tensor([1.,Sw,1.5],device=dev); mcv=torch.from_numpy(mc).to(dev)
    def met(p,yy): return 0.5*(average_precision_score((yy==1).astype(int),p[:,1])+average_precision_score((yy==2).astype(int),p[:,2]))
    @torch.no_grad()
    def pred(b,r,ft):
        M.eval(); o=[]
        for i in range(0,len(b),4096):
            o.append(torch.softmax(M(torch.from_numpy(b[i:i+4096]).to(dev),torch.from_numpy(r[i:i+4096]).to(dev),torch.from_numpy(ft[i:i+4096]).to(dev)),-1).cpu().numpy())
        return np.concatenate(o)
    Xtr=[torch.from_numpy(x) for x in (bT[it],rT[it],f_tr[it],yT[it])]
    ds=torch.utils.data.TensorDataset(*Xtr); dl=torch.utils.data.DataLoader(ds,batch_size=512,shuffle=True); best=-1; bs=None
    for ep in range(15):
        M.train()
        for bb,rr,ff,yy in dl:
            bb,rr,ff,yy=(t.to(dev) for t in (bb,rr,ff,yy)); opt.zero_grad()
            lo=M(bb,rr,ff); lg=lo-torch.zeros_like(lo).scatter_(1,yy[:,None],mcv[yy][:,None])
            ce=Fn.cross_entropy(lg,yy,reduction="none"); loss=(ce*cw[yy]).sum()/cw[yy].sum()
            loss.backward(); torch.nn.utils.clip_grad_norm_(M.parameters(),1.0); opt.step()
        pv=pred(bT[iv],rT[iv],f_tr[iv]); v=met(pv,yT[iv])
        if v>best: best=v; bs={k:vv.cpu() for k,vv in M.state_dict().items()}
    M.load_state_dict(bs)
    return pred(bV,rV,f_v), pred(b2,r2,f_2)

def run_oppoint(fams=("RHYTHM","KOOPMAN","AE","GNN"), seeds=(0,1,2), target_sen=0.82,
                frac=0.6, conf_cut=0.879, use_robust=True):
    from sklearn.model_selection import GroupKFold
    _determinism()
    beats,y,pid,F,tag=_bestF(fams)
    m1=np.isin(pid,_DS1); m2=np.isin(pid,_DS2); y2=y[m2]; pid2=pid[m2]
    Sw=auto_weights(y[m1]); nc=np.array([(y[m1]==k).sum() for k in range(3)],np.float32)
    mc=(1.0/np.power(nc,0.25)); mc=(mc/mc.max()*0.5).astype("float32")
    # ref: robust-template(STEP67 채택본) 또는 median
    if use_robust:
        ref,info=robust_template(beats,pid,frac=frac,conf_cut=conf_cut,verbose=True)
        conf={p:c for (p,c,fl,kf) in info}
    else:
        ref=_median_ref(beats,pid); conf={p:1.0 for p in np.unique(pid)}
    idx1=np.where(m1)[0]; idx2=np.where(m2)[0]; y1=y[idx1]; p1=pid[idx1]
    # ── OOF: DS1 모든 환자 1회 held-out + DS2 예측 누적 ──
    oof=np.zeros((len(idx1),3),np.float64); oof_n=np.zeros(len(idx1)); P2=[]
    print(f"\n백본 feats0+WST+MORPHO+REPOL+DTW+{tag}  ref={'robust' if use_robust else 'median'}  Sw={Sw:.2f}")
    print(f"OOF GroupKFold(5) × {len(seeds)}seed = {5*len(seeds)} 학습 (DS2 절대 미사용)")
    gkf=GroupKFold(n_splits=5)
    for s in seeds:
        for tr_l,va_l in gkf.split(idx1, y1, groups=p1):
            tr=idx1[tr_l]; va=idx1[va_l]
            pv,p2=_train_fold(F,beats,ref,y,pid,mc,Sw,tr,va,idx2,s)
            oof[va_l]+=pv; oof_n[va_l]+=1; P2.append(p2)
    oof/=np.maximum(oof_n,1)[:,None]                 # DS1 OOF 평균(각 환자 held-out만)
    P2=np.stack(P2,0); Pt2=_trim(P2)                 # DS2 트림앙상블
    sv=oof[:,1]; s2=Pt2[:,1]                          # S-score
    # 환자별 covariate(신뢰도) 벡터
    zc1=np.array([conf[p] for p in p1]); zc2=np.array([conf[p] for p in pid2])
    S_PR=average_precision_score((y2==1).astype(int),s2)
    print(f"\n임계무관: S_PR(DS2)={S_PR:.4f}  V_PR(DS2)={average_precision_score((y2==2).astype(int),Pt2[:,2]):.4f}  (동작점과 무관, 랭킹력)")

    def rep(name, tD1, applyfn):
        """DS1-OOF와 DS2 각각에서 (PREC,SEN,F1) 보고 — 전이갭 노출."""
        p1m=_binmet(applyfn(sv,p1,'d1'), y1, tD1); p2m=_binmet(applyfn(s2,pid2,'d2'), y2, tD1)
        print(f"  {name:16s}| DS1-OOF SEN={p1m[1]:.3f} PREC={p1m[0]:.3f} F1={p1m[2]:.3f}"
              f"   →  DS2 SEN={p2m[1]:.3f} PREC={p2m[0]:.3f} F1={p2m[2]:.3f}")
        return p2m

    ident=lambda s,pid,who: s
    print("\n=== 동작점 함수 (임계는 DS1-OOF에서 결정 → DS2 동결적용) ===")
    # 참고 상한: 오라클(DS2 F1최적) — 누출, 상한 표시용만
    t_or=_best_t_f1(s2,y2); om=_binmet(s2,y2,t_or)
    print(f"  [참고상한] 오라클(DS2)  DS2 SEN={om[1]:.3f} PREC={om[0]:.3f} F1={om[2]:.3f}  (누출-상한, 채택 아님)")
    # A. 고정
    tA=_best_t_f1(sv,y1); rep("A.고정F1", tA, ident)
    # B. 목표-SEN
    tB=_t_for_sen(sv,y1,target_sen); rep(f"B.목표SEN={target_sen}", tB, ident)
    # C. 환자별 적응(로짓 중앙값 제거)
    cv=_pp_center(sv,p1); c2=_pp_center(s2,pid2); tC=_best_t_f1(cv,y1)
    def applyC(s,pid,who): return cv if who=='d1' else c2
    rep("C.환자별적응", tC, applyC)
    # C+목표SEN
    tCs=_t_for_sen(cv,y1,target_sen); rep(f"C+목표SEN={target_sen}", tCs, applyC)
    # D. 공변량-선형 t_i=t0+β·(z-z̄): DS1 grid fit
    z1c=zc1-zc1.mean(); z2c=zc2-zc2.mean()
    bestD=(-1,0,tA)
    for t0 in np.quantile(sv,np.linspace(0.6,0.98,25)):
        for be in np.linspace(-0.5,0.5,21):
            ti=t0+be*z1c; f1=_binmet_vec(sv,y1,ti)
            if f1>bestD[0]: bestD=(f1,be,t0)
    _,beD,t0D=bestD
    tiD1=t0D+beD*z1c; tiD2=t0D+beD*z2c
    d1=_binmet_vec(sv,y1,tiD1,ret=True); d2=_binmet_vec(s2,y2,tiD2,ret=True)
    print(f"  {'D.공변량선형':16s}| DS1-OOF SEN={d1[1]:.3f} PREC={d1[0]:.3f} F1={d1[2]:.3f}"
          f"   →  DS2 SEN={d2[1]:.3f} PREC={d2[0]:.3f} F1={d2[2]:.3f}   (β={beD:+.2f})")
    print(f"\n  ★ 채택기준: DS2 F1가 오라클상한에 근접 + SEN이 목표 근처 + DS1→DS2 갭 작음.")
    print(f"     C(환자별적응)가 A(고정)보다 DS2 F1↑면 = 환자별 baseline 흡수 이득(무라벨 개인화).")
    print(f"     B/C+목표SEN 으로 SEN을 원하는 값에 정직하게 고정 가능(오라클 아님).")
    return dict(S_PR=S_PR, sv=sv, y1=y1, p1=p1, s2=s2, y2=y2, pid2=pid2, conf=conf)

def _binmet_vec(s, y, t_vec, ret=False):
    """환자별(또는 비트별) 임계 벡터 t_vec 로 이진지표."""
    pos=s>=t_vec; yp=(y==1)
    tp=float((pos&yp).sum()); fp=float((pos&~yp).sum()); fn=float((~pos&yp).sum())
    prec=tp/(tp+fp+1e-9); sen=tp/(tp+fn+1e-9); f1=2*prec*sen/(prec+sen+1e-9)
    return (prec,sen,f1) if ret else f1
