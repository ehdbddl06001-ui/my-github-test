# =============================================================================
#  colab_step36_moe2.py  —  [STEP 36] 라우팅 수정 MoE (N비트 2단계 + 소프트 라우팅)
#
#  STEP31 진단: 오라클 0.753(정밀도 0.688!)인데 정직 라우팅 0.515<최고단일 → 라우팅 병목.
#  원인: 쉬운 N비트(모든 전문가 다 맞힘)가 무작위 승자로 배정 오염 → 라우터가 B로 쏠림.
#  수정(사장님 N비트 아이디어):
#   ① N비트 2단계 필터: 모든 전문가가 확신으로 S·V 아니라 하면 → '확실한 N' 확정, 라우팅 제외.
#   ② 애매한 비트만 군집·라우팅.  ③ 소프트 라우팅(라우터 확률로 가중, 치명적 오배정 방지).
#  재학습 없음 — step31 experts.npz 재사용. DS2는 평가만.
#
#  선행: run_specialist()가 ablation_step31/experts.npz 저장. 캐시 _WST·_MORPHO·_REPOL·_SEGDEV·_XLEAD
#  실행:
#    exec(open('/content/drive/MyDrive/mitbih/colab_step36_moe2.py').read())
#    run_moe2()
# =============================================================================
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.metrics import average_precision_score, precision_recall_curve

_DS1=[101,106,108,109,112,114,115,116,118,119,122,124,201,203,205,207,208,209,215,220,223,230]
_DS2=[100,103,105,111,113,117,121,123,200,202,210,212,213,214,219,221,222,228,231,232,233,234]
_SAVE="/content/drive/MyDrive/mitbih/ablation_step31"; _REPOLK_IDX=[0,1,4,5]; _SEG_IDX=[9,10,8,4]

def _f1(y2,s):
    p,r,_=precision_recall_curve((y2==1).astype(int),s); f=2*p*r/(p+r+1e-9); i=int(np.nanargmax(f)); return p[i],r[i],f[i]

def run_moe2(tauS=0.08, tauV=0.20, soft=True, Kwst=40):
    E=np.load(_SAVE+"/experts.npz")
    names=[k[4:] for k in E.files if k.startswith("oof_")]
    OA=np.stack([E[f"oof_{n}"] for n in names],0); DA=np.stack([E[f"ds2_{n}"] for n in names],0)  # (K,N,3)
    y1=E["y1"]; y2=E["y2"]; N1=OA.shape[1]; N2=DA.shape[1]
    d=np.load("/content/drive/MyDrive/mitbih/mamba_data.npz")
    beats,feats0,y,pid=d["beat"],d["feats"],d["y"],d["pid"]
    ref=np.empty_like(beats)
    for p in np.unique(pid): m=pid==p; ref[m]=np.median(beats[m],axis=0,keepdims=True)
    ref=ref.astype("float32")
    Xw=globals()["_WST"]; Xm=globals()["_MORPHO"]; Xr=globals()["_REPOL"]; Xs=globals()["_SEGDEV"]; Xx=globals()["_XLEAD"]
    m1=np.isin(pid,_DS1); m2=np.isin(pid,_DS2)
    Xwk=np.nan_to_num(SelectKBest(f_classif,k=40).fit(np.nan_to_num(Xw[m1]),y[m1]).transform(np.nan_to_num(Xw)))
    G=np.concatenate([feats0,Xwk,Xm,Xr[:,_REPOLK_IDX],Xs[:,_SEG_IDX],Xx],1)
    Xv=globals().get("_VCG",None)
    if Xv is not None: G=np.concatenate([G,Xv],1)
    scg=StandardScaler().fit(np.nan_to_num(G[m1])); G1=np.nan_to_num(scg.transform(np.nan_to_num(G[m1]))); G2=np.nan_to_num(scg.transform(np.nan_to_num(G[m2])))
    met=lambda P: average_precision_score((y2==1).astype(int),P[:,1])
    norm=lambda P: P/P.sum(-1,keepdims=True)
    # ── ① 확실한 N 필터 (모든 전문가가 S·V 아님) ──
    def clearN(A): return (A[:,:,1].max(0)<tauS)&(A[:,:,2].max(0)<tauV)
    cN1,cN2=clearN(OA),clearN(DA); amb1,amb2=~cN1,~cN2
    print(f"확실한N 필터: DS1 {cN1.mean()*100:.1f}% N확정 / 애매 {amb1.sum()} (그중 S={int(((amb1)&(y1==1)).sum())}/{int((y1==1).sum())})")
    print(f"            DS2 {cN2.mean()*100:.1f}% N확정 / 애매 {amb2.sum()} (그중 S={int(((amb2)&(y2==1)).sum())}/{int((y2==1).sum())})  ← 필터가 놓친 S 적어야")
    # ── ② 애매 비트만 승자배정·라우터 ──
    win=OA[:,np.arange(N1),y1].argmax(0)
    rf=RandomForestClassifier(n_estimators=300,max_depth=14,n_jobs=-1,random_state=0,class_weight="balanced")
    cv=cross_val_score(rf,G1[amb1],win[amb1],cv=3).mean(); rf.fit(G1[amb1],win[amb1])
    print(f"라우터(애매만) CV 승자예측={cv:.3f} (무작위={1/len(names):.3f})  ← N오염 제거 후 개선?")
    meanA=norm(DA.mean(0))                                              # 기본(확실한N에 사용, S낮음)
    def assemble(route_amb):
        P=meanA.copy(); P[amb2]=route_amb; return norm(P)
    # ③ 소프트 vs 하드 라우팅 (애매 비트)
    cls=list(rf.classes_)
    if soft:
        pr=rf.predict_proba(G2[amb2])                                  # (n_amb,|cls|)
        route=np.einsum('nk,knc->nc',pr,np.stack([DA[c,amb2] for c in cls],0))
    else:
        sel=rf.predict(G2[amb2]); route=DA[sel,np.where(amb2)[0]]
    moe2=assemble(norm(route))
    # ── 비교 ──
    best_single=max(names,key=lambda n:met(DA[names.index(n)]))
    uni=norm(DA.mean(0))
    honest_all=DA[rf.predict(G2),np.arange(N2)]                        # 필터없이 전체 라우팅(step31식)
    oracle=DA[DA[:,np.arange(N2),y2].argmax(0),np.arange(N2)]
    print(f"\n{'='*54}\n[DS2] (라우팅=특징만, 오라클=라벨 천장)")
    for nm,P in [(f"최고단일({best_single})",DA[names.index(best_single)]),("균일",uni),
                 ("전체 라우팅(step31식)",honest_all),("★2단계+소프트 MoE",moe2),("오라클",oracle)]:
        pr,se,f1=_f1(y2,P[:,1]); print(f"  {nm:22s} S={met(P):.4f}  PREC={pr:.3f} SEN={se:.3f} F1={f1:.3f}")
    print(f"\n▶ '2단계+소프트'가 최고단일·전체라우팅 넘으면 = 라우팅 병목 해소(오라클 0.75로 접근).")
    print(f"  tauS·tauV(확실한N 문턱)·soft 조절로 튜닝 가능.")
    return dict(moe2=moe2,rf=rf)
