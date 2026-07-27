# =============================================================================
#  colab_step70_evalintegrity.py  —  [STEP 70] 평가 무결성: C2 전수 분해 · 232 제외 · 환자매크로
#
#  STEP69에서 C2(강건 2성분 센터)가 정직 DS2 F1 0.778(오라클 0.824의 94%)을 냈다. 단 유보:
#   · 232가 DS2 S의 75.2% → 비트풀링 micro는 232가 지배. 0.778이 232 덕인지 고른 개선인지 불명.
#   · DS2가 쉬워서(232+유병률2배) 정직추정치는 232제외·환자매크로 쪽이 진짜.
#  그래서 C2를 다음으로 정직하게 재보고:
#   (1) C2 vs A(raw) 22레코드 전수 분해 (S수·SEN·FP), FP순·S순 정렬 — 개선이 어디서 났나
#   (2) micro / 232제외 micro / 환자단위 매크로(비트풀링 아님) / S_PR 232제외
#   (3) 전체 FP 분포(상위8 밖 ~1500개 FP 위치)
#   (4) [옵션] cv44(): 고정 DS1/DS2 대신 44레코드 grouped repeated CV — 단일 레코드 테스트지배 제거
#  ★ 알람률 다이얼은 반증됨(유병률 2배차) → 승리 원인은 오직 환자별 센터링. 여기에 집중.
#
#  선행: colab_step67~69 (Drive)
#  실행:
#    exec(open('/content/drive/MyDrive/mitbih/colab_step70_evalintegrity.py').read())
#    OUT=eval_c2(n_rep=5)         # 고정 DS1/DS2 전수 분해(핵심)
#    cv44(n_rep=2)               # (옵션·무거움) 44레코드 CV — 232 지배 제거한 성능
# =============================================================================
import os
import numpy as np
from sklearn.metrics import average_precision_score

_BASE="/content/drive/MyDrive/mitbih"
if "_pp_center2" not in globals():
    exec(open(f"{_BASE}/colab_step69_ratepoint.py").read(), globals())   # 69→68→67 helper 전부

def _prf(v, yy):
    yp=(yy==1); tp=float((v&yp).sum()); fp=float((v&~yp).sum()); fn=float((~v&yp).sum())
    pr=tp/(tp+fp+1e-9); se=tp/(tp+fn+1e-9); return pr,se,2*pr*se/(pr+se+1e-9)

def _c2_and_raw_decisions(fams, n_rep, frac, conf_cut, use_robust, target_sen=0.82):
    """STEP69 C2 학습 반복 → DS2에서 C2·A(raw) 결정벡터 반환(재학습, 결정적)."""
    from sklearn.model_selection import GroupKFold
    _determinism()
    beats,y,pid,F,tag=_bestF(fams)
    m1=np.isin(pid,_DS1); m2=np.isin(pid,_DS2); y2=y[m2]; pid2=pid[m2]
    Sw=auto_weights(y[m1]); nc=np.array([(y[m1]==k).sum() for k in range(3)],np.float32)
    mc=(1.0/np.power(nc,0.25)); mc=(mc/mc.max()*0.5).astype("float32")
    ref = robust_template(beats,pid,frac=frac,conf_cut=conf_cut,verbose=False)[0] if use_robust else _median_ref(beats,pid)
    idx1=np.where(m1)[0]; idx2=np.where(m2)[0]; y1=y[idx1]; p1=pid[idx1]
    dC=[]; dA=[]
    gkf=GroupKFold(n_splits=5)
    for rep in range(n_rep):
        order=np.argsort([(hash((int(p),rep))%1000) for p in p1])
        for tr_o,va_o in gkf.split(idx1[order], y1[order], groups=p1[order]):
            tr=idx1[order][tr_o]; va=idx1[order][va_o]; seed=1000*rep+int(va_o[0])
            pv,p2=_train_fold(F,beats,ref,y,pid,mc,Sw,tr,va,idx2,seed)
            sc=pv[:,1]; yc=y[va]; pc=pid[va]; s2=p2[:,1]
            tA=_best_t_f1(sc,yc); dA.append(s2-tA)
            cc=_pp_center2(sc,pc); c2=_pp_center2(s2,pid2); tC=_best_t_f1(cc,yc); dC.append(c2-tC)
    return dict(y2=y2,pid2=pid2,vA=(np.mean(dA,0)>=0),vC=(np.mean(dC,0)>=0),
                sA=np.mean(dA,0),sC=np.mean(dC,0),tag=tag)

def eval_c2(fams=("RHYTHM","KOOPMAN","AE","GNN"), n_rep=5, frac=0.6, conf_cut=0.879, use_robust=True):
    D=_c2_and_raw_decisions(fams,n_rep,frac,conf_cut,use_robust)
    y2,pid2,vA,vC,sA,sC=D["y2"],D["pid2"],D["vA"],D["vC"],D["sA"],D["sC"]
    print(f"\n백본 …+{D['tag']}  n_rep={n_rep}  (C2=강건2성분센터, A=raw)")
    # (2) 종합 지표
    for nm,v,s in [("A.raw",vA,sA),("C2.센터",vC,sC)]:
        pr,se,f1=_prf(v,y2)
        ex=pid2!=232; pe,se2,f2=_prf(v[ex],y2[ex])            # 232 제외 micro
        # 환자단위 매크로(S>0 환자만)
        mf=[];
        for p in np.unique(pid2):
            mp=pid2==p
            if (y2[mp]==1).sum()==0: continue
            mf.append(_prf(v[mp],y2[mp])[2])
        spr=average_precision_score((y2==1).astype(int),s); spx=average_precision_score((y2[ex]==1).astype(int),s[ex])
        print(f"\n[{nm}] micro F1={f1:.3f} (SEN {se:.3f}/PREC {pr:.3f})")
        print(f"      232제외 micro F1={f2:.3f} (SEN {se2:.3f}/PREC {pe:.3f})   ← 진짜 난이도")
        print(f"      환자매크로 F1={np.mean(mf):.3f} ±{np.std(mf):.3f} (S>0 {len(mf)}명, 비트풀링 아님)")
        print(f"      S_PR 전체={spr:.3f}  232제외={spx:.3f}")
    # (1) 레코드별 전수 분해: C2 vs A
    print(f"\n=== 22레코드 전수 분해 (S수순) : A.raw → C2.센터 ===")
    print(f"  {'rec':>4} {'S':>5} {'N등':>6} | {'A_SEN':>5} {'A_FP':>5} | {'C2_SEN':>6} {'C2_FP':>5}")
    tblA_fp=0; tblC_fp=0
    rows=[]
    for p in np.unique(pid2):
        mp=pid2==p; ns=int((y2[mp]==1).sum()); nn=int((y2[mp]!=1).sum())
        aS=(vA[mp]&(y2[mp]==1)).sum()/max(ns,1); aF=int((vA[mp]&(y2[mp]!=1)).sum())
        cS=(vC[mp]&(y2[mp]==1)).sum()/max(ns,1); cF=int((vC[mp]&(y2[mp]!=1)).sum())
        tblA_fp+=aF; tblC_fp+=cF
        rows.append((int(p),ns,nn,aS,aF,cS,cF))
    for p,ns,nn,aS,aF,cS,cF in sorted(rows,key=lambda x:-x[1]):
        mk="★232" if p==232 else ""
        print(f"  {p:>4} {ns:>5} {nn:>6} | {aS:>5.2f} {aF:>5} | {cS:>6.2f} {cF:>5}  {mk}")
    print(f"  {'합계 FP':>18} |       {tblA_fp:>5} |        {tblC_fp:>5}   (C2가 FP {100*(1-tblC_fp/max(tblA_fp,1)):.0f}% 절감)")
    # (3) FP 순 정렬(상위8 밖 FP 위치)
    print(f"\n=== FP 상위 레코드 (A.raw 기준, ~1500개 나머지 FP 위치) ===")
    for p,ns,nn,aS,aF,cS,cF in sorted(rows,key=lambda x:-x[4])[:10]:
        print(f"  rec {p}: A_FP={aF:>5} → C2_FP={cF:>5}   (S={ns}, N={nn})")
    print(f"\n  ★ C2 개선이 232 밖 레코드(특히 FP 큰 222 등)에서도 고르면 = 진짜 표현개선.")
    print(f"    232제외 micro·환자매크로가 헤드라인이어야 정직(리뷰어가 232 먼저 찾음).")
    return D

def cv44(fams=("RHYTHM","KOOPMAN","AE","GNN"), n_rep=2, k=5, frac=0.6, conf_cut=0.879, use_robust=True):
    """44레코드 grouped repeated CV: 어떤 단일 레코드도 테스트셋 지배 못하게.
       각 폴드: 테스트=held-out 레코드, 학습=나머지, calib=학습에서 그룹분할 → C2 적용. 무거움."""
    from sklearn.model_selection import GroupKFold, GroupShuffleSplit
    _determinism()
    beats,y,pid,F,tag=_bestF(fams)
    allrec=np.unique(pid); Sw=auto_weights(y[np.isin(pid,_DS1)])
    nc=np.array([(y[np.isin(pid,_DS1)]==kk).sum() for kk in range(3)],np.float32); mc=(1.0/np.power(nc,0.25)); mc=(mc/mc.max()*0.5).astype("float32")
    ref = robust_template(beats,pid,frac=frac,conf_cut=conf_cut,verbose=False)[0] if use_robust else _median_ref(beats,pid)
    idxall=np.arange(len(y))
    foldF1=[]; print(f"44레코드 grouped CV: {k}fold × {n_rep}rep = {k*n_rep}학습 (무거움)")
    gkf=GroupKFold(n_splits=k)
    for rep in range(n_rep):
        order=np.argsort([(hash((int(p),rep+7))%1000) for p in pid])
        for tr_o,te_o in gkf.split(idxall[order], y[order], groups=pid[order]):
            tr=idxall[order][tr_o]; te=idxall[order][te_o]
            # calib: 학습 레코드에서 그룹분할(fit/calib 환자 분리)
            fit_o,cal_o=next(GroupShuffleSplit(1,test_size=0.25,random_state=rep).split(tr,y[tr],groups=pid[tr]))
            fit=tr[fit_o]; calx=tr[cal_o]
            pv,pte=_train_fold(F,beats,ref,y,pid,mc,Sw,fit,calx,te,1000*rep+int(te_o[0]))
            sc=pv[:,1]; yc=y[calx]; pc=pid[calx]; ste=pte[:,1]; yte=y[te]; pte_id=pid[te]
            cc=_pp_center2(sc,pc); cteN=_pp_center2(ste,pte_id); tC=_best_t_f1(cc,yc)
            v=(cteN-tC)>=0
            # 환자매크로 F1(S>0)
            mf=[_prf(v[pte_id==p],yte[pte_id==p])[2] for p in np.unique(pte_id) if (yte[pte_id==p]==1).sum()>0]
            if mf: foldF1.append(np.mean(mf))
    foldF1=np.array(foldF1)
    print(f"\n▶ 44레코드 CV 환자매크로 F1 = {foldF1.mean():.3f} ± {foldF1.std():.3f}  (폴드 {len(foldF1)})")
    print(f"  이게 고정 DS2(232지배) 0.778보다 '전형 구성'의 정직 추정치. 리뷰어 방어용 핵심 숫자.")
    return foldF1
