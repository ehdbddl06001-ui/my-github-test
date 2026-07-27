# =============================================================================
#  colab_step68_oppoint.py  —  [STEP 68] DS1-최적화 동작점 함수 (SEN 상승 + 오라클 누출 제거)
#
#  문제: 지금까지 SEN/PREC/F1 은 DS2 라벨로 F1최적 임계를 고른 '오라클 임계'(작은 누출).
#        게다가 임계가 고정 스칼라 → 환자별 점수 baseline 차이를 못 흡수(inter-patient 근본문제).
#  해결: 동작점을 '환자별로 변하는 함수'로 만들고 그 파라미터를 DS1 에서만 최적화 → DS2 동결적용.
#    A. 고정         : t=argmax F1(calib)                   (정직 베이스라인, 오라클 누출 제거)
#    B. 목표-SEN     : calib SEN=target 되는 t               (SEN 다이얼)
#    C. 환자별 적응  : 결정점 = s - median_p(s) 후 전역 t    (★변수 자체가 바뀌는 함수, 무라벨)
#  ★핵심(예측기 일치): 임계와 그 적용 대상 DS2 예측이 반드시 '같은 단일 모델'에서 나와야 스케일 일치.
#    각 시드: DS1을 fit/calib 환자분할 → fit 학습 → 그 모델로 calib(held-out DS1)·DS2 예측
#           → 그 모델 calib에서 임계 t → 그 모델 DS2 점수를 (s2 - t)로 '정렬' → 시드평균 후 0에서 결정.
#    (다수결은 각 모델 SEN을 깨서 X. 정렬점수평균이 캘리브레이션 보존 — 시뮬 검증됨.)
#  무결성: 임계는 calib=held-out DS1 환자에서만. DS2 절대 안 봄. 오라클(DS2 F1최적)은 상한참고만.
#  ★ val≠test 때문에 calib→DS2 전이 갭을 병기(calib 값과 DS2 값 나란히).
#
#  선행: colab_prep_all.py + colab_step67_selfref.py (Drive)
#  실행:
#    exec(open('/content/drive/MyDrive/mitbih/colab_step68_oppoint.py').read())
#    run_oppoint(target_sen=0.82)     # 8시드 자기캘리브+정렬평균 (학습 8회)
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

def run_oppoint(fams=("RHYTHM","KOOPMAN","AE","GNN"), seeds=tuple(range(8)), target_sen=0.82,
                frac=0.6, conf_cut=0.879, use_robust=True, cal_frac=0.25):
    """모델별 자기-캘리브레이션 + 정렬점수 평균(예측기 불일치 제거).
       각 시드: DS1을 fit/calib 환자분할 → fit학습 → 그 모델로 calib·DS2 예측
       → 그 모델 calib에서 임계 t → 그 모델 DS2 점수를 (s2-t)로 정렬 → 시드평균 후 0에서 결정.
       S_PR은 DS2 확률평균(임계무관)."""
    from sklearn.model_selection import GroupShuffleSplit
    _determinism()
    beats,y,pid,F,tag=_bestF(fams)
    m1=np.isin(pid,_DS1); m2=np.isin(pid,_DS2); y2=y[m2]; pid2=pid[m2]
    Sw=auto_weights(y[m1]); nc=np.array([(y[m1]==k).sum() for k in range(3)],np.float32)
    mc=(1.0/np.power(nc,0.25)); mc=(mc/mc.max()*0.5).astype("float32")
    if use_robust:
        ref,info=robust_template(beats,pid,frac=frac,conf_cut=conf_cut,verbose=True)
    else:
        ref=_median_ref(beats,pid)
    idx1=np.where(m1)[0]; idx2=np.where(m2)[0]; y1=y[idx1]; p1=pid[idx1]
    seeds=list(seeds)
    print(f"\n백본 feats0+WST+MORPHO+REPOL+DTW+{tag}  ref={'robust' if use_robust else 'median'}  Sw={Sw:.2f}")
    print(f"모델별 자기캘리브 + 정렬점수평균: {len(seeds)}시드(각 fit{1-cal_frac:.0%}/calib{cal_frac:.0%} 환자분할) — DS2 미사용")
    METHODS=["A.고정F1", f"B.목표SEN={target_sen}", "C.환자별적응", f"C+목표SEN={target_sen}"]
    dels={k:[] for k in METHODS}; cals={k:[] for k in METHODS}; P2prob=[]
    for s in seeds:
        fit_l,cal_l=next(GroupShuffleSplit(1,test_size=cal_frac,random_state=s).split(idx1,y1,groups=p1))
        fit=idx1[fit_l]; cal=idx1[cal_l]
        pv,p2=_train_fold(F,beats,ref,y,pid,mc,Sw,fit,cal,idx2,s)   # pv=calib예측, p2=DS2예측 (같은 모델)
        P2prob.append(p2)
        sc=pv[:,1]; yc=y1[cal_l]; pc=p1[cal_l]; s2=p2[:,1]         # 같은 모델의 calib·DS2 S-score
        # 각 모델 점수를 자기 임계로 '정렬'(s2 - t): 캘리브레이션 보존(다수결은 SEN 깨짐)
        tA=_best_t_f1(sc,yc);            dels["A.고정F1"].append(s2-tA);       cals["A.고정F1"].append(_binmet(sc,yc,tA))
        tB=_t_for_sen(sc,yc,target_sen); dels[f"B.목표SEN={target_sen}"].append(s2-tB); cals[f"B.목표SEN={target_sen}"].append(_binmet(sc,yc,tB))
        cc=_pp_center(sc,pc); c2=_pp_center(s2,pid2)               # 환자별 baseline 제거(같은 모델 안)
        tC=_best_t_f1(cc,yc);            dels["C.환자별적응"].append(c2-tC);   cals["C.환자별적응"].append(_binmet(cc,yc,tC))
        tCs=_t_for_sen(cc,yc,target_sen);dels[f"C+목표SEN={target_sen}"].append(c2-tCs); cals[f"C+목표SEN={target_sen}"].append(_binmet(cc,yc,tCs))
    Pens=np.stack(P2prob,0).mean(0)                                 # 확률평균(임계무관 S_PR용)
    S_PR=average_precision_score((y2==1).astype(int),Pens[:,1]); V_PR=average_precision_score((y2==2).astype(int),Pens[:,2])
    print(f"\n임계무관: S_PR(DS2)={S_PR:.4f}  V_PR(DS2)={V_PR:.4f}  (동작점과 무관, 랭킹력)")
    t_or=_best_t_f1(Pens[:,1],y2); om=_binmet(Pens[:,1],y2,t_or)   # 오라클(DS2 F1최적) — 누출 상한
    print("\n=== 동작점 함수 (임계는 각 모델 calib=held-out DS1 에서 결정 → 정렬점수 평균) ===")
    print(f"  [참고상한] 오라클(DS2)  DS2 SEN={om[1]:.3f} PREC={om[0]:.3f} F1={om[2]:.3f}  (누출-상한, 채택 아님)")
    def _boolmet(v,yy):
        yp=(yy==1); tp=float((v&yp).sum()); fp=float((v&~yp).sum()); fn=float((~v&yp).sum())
        pr=tp/(tp+fp+1e-9); se=tp/(tp+fn+1e-9); return pr,se,2*pr*se/(pr+se+1e-9)
    RES={}
    for k in METHODS:
        v=np.mean(dels[k],0)>=0                                     # 정렬점수 평균 후 0에서 결정
        pr,se,f1=_boolmet(v,y2)
        cm=np.mean(cals[k],0)                                       # calib 평균(전이 참고)
        print(f"  {k:16s}| calib SEN={cm[1]:.3f} PREC={cm[0]:.3f} F1={cm[2]:.3f}"
              f"   →  DS2 SEN={se:.3f} PREC={pr:.3f} F1={f1:.3f}")
        RES[k]=(pr,se,f1)
    print(f"\n  ★ B/C+목표SEN 의 DS2 SEN 이 {target_sen} 근처면 = SEN 정직 다이얼 성공(오라클 아님).")
    print(f"     C가 A보다 DS2 F1↑면 = 환자별 baseline 흡수 이득(무라벨 개인화).")
    print(f"     DS2 F1가 오라클상한({om[2]:.3f})에 근접할수록 = 누출없이 다 짜낸 것.")
    return dict(S_PR=S_PR, V_PR=V_PR, oracle=om, res=RES, Pens=Pens, y2=y2, pid2=pid2)
