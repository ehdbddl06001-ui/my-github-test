# =============================================================================
#  colab_step69_ratepoint.py  —  [STEP 69] 알람률 동작점 + 232 병목 규명
#
#  STEP68 진단(232 지배)의 최소수정 반영:
#   1) 다이얼 목표: SEN → '예측양성률(알람률)'. SEN은 양성집합 구성이 DS1≠DS2라 전이불가;
#      알람률은 음성(90%+, 안정) 앵커라 calib→DS2 전이됨. 임상도 조절하는 건 알람률.
#   2) _pp_center2: 환자별 로짓 2성분 분리 → '낮은 성분(정상baseline)'으로 센터링(단봉이면 median).
#      232처럼 S가 과반이어도 안 뒤집힘(기존 median 센터링의 가정위반 수정).
#   3) GroupKFold: 모든 DS1 환자가 calib에 정확히 1회(209 포함 우연 제거).
#   4) 오라클을 '각 방법의 정렬델타'에서 계산(공정 상한 — STEP68은 Pens에서 뽑아 불공정했음).
#   5) 레코드별 DS2 분해 출력 → 232 지배와 '랭킹O/임계X' 병목을 그림으로.
#  ★ 핵심 발견 프레이밍: S_PR 높음(랭킹 충분)인데 정직 동작점 F1 낮음 = inter-patient 병목.
#
#  선행: colab_prep_all.py + colab_step67_selfref.py + colab_step68_oppoint.py (Drive)
#  실행:
#    exec(open('/content/drive/MyDrive/mitbih/colab_step69_ratepoint.py').read())
#    verify_232()                 # 232가 DS2 S를 지배하는지 한 줄 검증(빠름)
#    run_ratepoint()              # 알람률 동작점 + 레코드별 분해 (GroupKFold5 × 2rep = 10학습)
# =============================================================================
import os
import numpy as np
from sklearn.metrics import average_precision_score

_BASE="/content/drive/MyDrive/mitbih"
if "_train_fold" not in globals():
    exec(open(f"{_BASE}/colab_step68_oppoint.py").read(), globals())   # STEP68→STEP67 helper 전부

def verify_232():
    """232가 DS2 S(상심실)를 실제로 지배하는지 실측(진단의 근거)."""
    d=np.load(f"{_BASE}/mamba_data.npz"); y,pid=d["y"],d["pid"]
    m2=np.isin(pid,_DS2); y2=y[m2]; p2=pid[m2]
    totS=int((y2==1).sum())
    per=[(int(p),int(((p2==p)&(y2==1)).sum())) for p in np.unique(p2)]
    per=sorted(per,key=lambda x:-x[1])
    print(f"DS2 총 S={totS}.  레코드별 S 상위:")
    for p,c in per[:6]:
        print(f"  rec {p}: S={c}  ({100*c/max(totS,1):.1f}% of DS2 S)")
    top=per[0]
    print(f"  → 최다 레코드 {top[0]}가 DS2 S의 {100*top[1]/max(totS,1):.1f}% 지배. "
          f"{'★232 지배 확정' if top[0]==232 and top[1]/max(totS,1)>0.5 else '분포 확인'}")
    return per

# ─────────────── 수정: 2성분 강건 환자별 센터링 ───────────────
def _pp_center2(s, pid, sep=1.0):
    """환자별 로짓을 2성분(1D k-means)으로 나눠 '낮은 성분'으로 센터링.
       두 성분이 충분히 분리(|Δ|>sep)될 때만 적용, 아니면 median(단봉). S 과반에도 강건."""
    l=_logit(s); out=l.copy()
    for p in np.unique(pid):
        m=pid==p; v=l[m]
        if len(v)<20:
            c=np.median(v)
        else:
            c0,c1=np.percentile(v,[25,75])
            for _ in range(25):
                a=np.abs(v-c0)<=np.abs(v-c1)
                if a.sum()==0 or (~a).sum()==0: break
                n0,n1=v[a].mean(),v[~a].mean()
                if abs(n0-c0)<1e-6 and abs(n1-c1)<1e-6: c0,c1=n0,n1; break
                c0,c1=n0,n1
            c = min(c0,c1) if abs(c1-c0)>sep else np.median(v)   # 분리되면 낮은성분, 아니면 median
        out[m]=v-c
    return out

def _t_for_rate(s, rate):
    """예측양성률=rate 되는 임계(상위 rate 분위). 음성 앵커라 전이 안정. 무라벨."""
    return float(np.quantile(s, 1.0-rate))

def _best_rate_f1(s, y, rates=None):
    """calib에서 F1 최대인 알람률."""
    rates=rates if rates is not None else np.linspace(0.01,0.20,40)
    best=(-1.0, rates[0])
    for r in rates:
        f1=_binmet(s,y,_t_for_rate(s,r))[2]
        if f1>best[0]: best=(f1,r)
    return float(best[1])

def _boolmet(v, yy):
    yp=(yy==1); tp=float((v&yp).sum()); fp=float((v&~yp).sum()); fn=float((~v&yp).sum())
    pr=tp/(tp+fp+1e-9); se=tp/(tp+fn+1e-9); return pr,se,2*pr*se/(pr+se+1e-9)

def run_ratepoint(fams=("RHYTHM","KOOPMAN","AE","GNN"), n_rep=2, target_sen=0.82,
                  frac=0.6, conf_cut=0.879, use_robust=True):
    from sklearn.model_selection import GroupKFold
    _determinism()
    beats,y,pid,F,tag=_bestF(fams)
    m1=np.isin(pid,_DS1); m2=np.isin(pid,_DS2); y2=y[m2]; pid2=pid[m2]
    Sw=auto_weights(y[m1]); nc=np.array([(y[m1]==k).sum() for k in range(3)],np.float32)
    mc=(1.0/np.power(nc,0.25)); mc=(mc/mc.max()*0.5).astype("float32")
    ref = robust_template(beats,pid,frac=frac,conf_cut=conf_cut,verbose=True)[0] if use_robust else _median_ref(beats,pid)
    idx1=np.where(m1)[0]; idx2=np.where(m2)[0]; y1=y[idx1]; p1=pid[idx1]
    print(f"\n백본 feats0+WST+MORPHO+REPOL+DTW+{tag}  ref={'robust' if use_robust else 'median'}  Sw={Sw:.2f}")
    print(f"GroupKFold(5) × {n_rep}rep = {5*n_rep}학습. 다이얼: SEN vs 알람률 대조. DS2 미사용")
    # 방법: 각 모델 calib에서 임계 결정 → 그 모델 DS2 점수 정렬(s2-t) 누적(정렬점수평균)
    METH=["A.F1(raw)", f"B.SEN={target_sen}(raw)", "R.최적알람률(raw)", "C2.강건센터+F1"]
    dels={k:[] for k in METH}; cals={k:[] for k in METH}; rate_used=[]
    gkf=GroupKFold(n_splits=5)
    for rep in range(n_rep):
        # rep마다 환자 순서를 살짝 흔들어 폴드 다양화(라벨 무관, 결정적)
        order=np.argsort([(hash((int(p),rep))%1000) for p in p1])
        for tr_o,va_o in gkf.split(idx1[order], y1[order], groups=p1[order]):
            tr=idx1[order][tr_o]; va=idx1[order][va_o]
            seed=1000*rep+int(va_o[0])
            pv,p2=_train_fold(F,beats,ref,y,pid,mc,Sw,tr,va,idx2,seed)
            sc=pv[:,1]; yc=y[va]; pc=pid[va]; s2=p2[:,1]
            tA=_best_t_f1(sc,yc);            dels["A.F1(raw)"].append(s2-tA);          cals["A.F1(raw)"].append(_binmet(sc,yc,tA))
            tB=_t_for_sen(sc,yc,target_sen); dels[f"B.SEN={target_sen}(raw)"].append(s2-tB); cals[f"B.SEN={target_sen}(raw)"].append(_binmet(sc,yc,tB))
            rr=_best_rate_f1(sc,yc); tR=_t_for_rate(sc,rr); rate_used.append(rr)
            dels["R.최적알람률(raw)"].append(s2-tR);          cals["R.최적알람률(raw)"].append(_binmet(sc,yc,tR))
            cc=_pp_center2(sc,pc); c2=_pp_center2(s2,pid2); tC=_best_t_f1(cc,yc)
            dels["C2.강건센터+F1"].append(c2-tC);             cals["C2.강건센터+F1"].append(_binmet(cc,yc,tC))
    # S_PR: raw vs 강건센터 (전이되는 랭킹 이득 확인) — 정렬점수 평균의 랭킹으로 계산
    def ens(k): return np.mean(dels[k],0)                    # 정렬점수 평균(방법별)
    sA=ens("A.F1(raw)")
    S_PR_raw=average_precision_score((y2==1).astype(int), sA)
    S_PR_cen=average_precision_score((y2==1).astype(int), ens("C2.강건센터+F1"))
    print(f"\n임계무관 랭킹(정렬점수 기준): S_PR raw={S_PR_raw:.4f}  강건센터={S_PR_cen:.4f}  Δ={S_PR_cen-S_PR_raw:+.4f}")
    print(f"  (Δ>0 이면 환자별 센터가 '전이되는' 랭킹 이득. ≤0 이면 232류가 센터로 손해 → raw 유지)")
    print(f"\n=== 동작점: calib(held-out DS1)에서 결정 → 정렬점수평균 → DS2 (오라클=각 방법 자체 상한) ===")
    RES={}
    for k in METH:
        me=ens(k); v=me>=0; pr,se,f1=_boolmet(v,y2); cm=np.mean(cals[k],0)
        t_or=_best_t_f1(me+1e-9*0, y2)  # 방법 자체 점수에서 오라클(공정 상한)
        om=_binmet(me,y2,t_or)
        print(f"  {k:16s}| calib SEN={cm[1]:.3f} PREC={cm[0]:.3f} F1={cm[2]:.3f}"
              f"  → DS2 SEN={se:.3f} PREC={pr:.3f} F1={f1:.3f}   [오라클상한 F1={om[2]:.3f}]")
        RES[k]=dict(ds2=(pr,se,f1), calib=tuple(cm), oracle=om[2])
    print(f"\n  평균 최적알람률(calib)={np.mean(rate_used):.3f}  (이 근처가 DS2 알람률로도 전이될 것)")
    # ── 레코드별 DS2 분해(A 방법 기준): 232 병목 가시화 ──
    vA=sA>=0
    print(f"\n=== 레코드별 DS2 분해 (A.F1 기준) — 232 병목 확인 ===")
    rows=[]
    for p in np.unique(pid2):
        mp=pid2==p; ns=int((y2[mp]==1).sum())
        if ns==0: continue
        vp=vA[mp]; yp=(y2[mp]==1)
        tp=int((vp&yp).sum()); sen=tp/max(ns,1); fp=int((vp&~yp).sum())
        rows.append((int(p),ns,sen,fp))
    for p,ns,sen,fp in sorted(rows,key=lambda x:-x[1])[:8]:
        mark="★232" if p==232 else ""
        print(f"  rec {p}: S={ns:4d}  SEN={sen:.3f}  FP={fp:4d}  {mark}")
    print(f"\n  ★ S_PR는 충분한데(랭킹O) 정직 동작점 F1은 낮다(임계X) = inter-patient 병목.")
    print(f"    알람률(R)이 SEN(B)보다 calib→DS2 갭이 작으면 = '알람률이 전이되는 다이얼'(임상적으로도 옳음).")
    return dict(S_PR_raw=S_PR_raw, S_PR_cen=S_PR_cen, res=RES, y2=y2, pid2=pid2, rate=float(np.mean(rate_used)))
