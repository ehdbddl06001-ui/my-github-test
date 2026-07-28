# =============================================================================
#  colab_step65_stats.py  —  [STEP 65] 통계 검증: val 선택 불가능성 + 앙상블 신뢰구간
#
#  발견을 p-value로 못박는다:
#   ① 순위상관(Pearson/Spearman/Kendall) + p — DS1-val이 DS2를 예측 못함(선택 불가능)
#   ② 순열검정(Monte Carlo) — val필터 이득이 우연과 구분되나
#   ③ Bootstrap CI — 최종 trimmed ensemble의 S_PR/F1 95% 신뢰구간(헤드라인 숫자에 오차막대)
#  ①②는 (vals, d2) 배열만 있으면 즉시(학습 불필요). ③은 STEP62 저장 예측(stable_out) 로드.
#
#  실행:
#    exec(open('/content/drive/MyDrive/mitbih/colab_step65_stats.py').read())
#    stats_selection()                 # 저장된 STEP63 배열로 즉시 (아래 기본값)
#    stats_bootstrap(fams=("RHYTHM","KOOPMAN","AE","GNN"))   # 앙상블 95% CI
# =============================================================================
import os
import numpy as np
from sklearn.metrics import average_precision_score, precision_recall_curve

_BASE="/content/drive/MyDrive/mitbih"; _STABLE=f"{_BASE}/stable_out"
_DS1=[101,106,108,109,112,114,115,116,118,119,122,124,201,203,205,207,208,209,215,220,223,230]
_DS2=[100,103,105,111,113,117,121,123,200,202,210,212,213,214,219,221,222,228,231,232,233,234]

# STEP63 결과(원하면 네 최신 배열로 교체)
_VALS=[0.50365751,0.89406681,0.85026659,0.66153447,0.15674157,0.7568426,0.90288269,0.0777679,0.48605399,0.74792888,0.27741571,0.90255612,0.15651072,0.72706329,0.14336847,0.60939972,0.68174589,0.1983768,0.93560753,0.91408316]
_D2  =[0.74763659,0.74482688,0.76605661,0.76051697,0.6007808,0.56418314,0.72662851,0.79626935,0.82415419,0.48295845,0.77457992,0.81484766,0.74859994,0.81528881,0.79302721,0.80346987,0.78983968,0.50891148,0.83480256,0.77536877]

def stats_selection(vals=None, d2=None, keep_frac=0.7, nperm=10000):
    from scipy import stats
    vals=np.array(vals if vals is not None else _VALS); d2=np.array(d2 if d2 is not None else _D2)
    n=len(vals); k=int(round(n*keep_frac))
    print("=== ① 순위상관: DS1-val ↔ DS2 (선택 가능성) ===")
    for nm,(c,p) in {"Pearson":stats.pearsonr(vals,d2),"Spearman":stats.spearmanr(vals,d2),"Kendall":stats.kendalltau(vals,d2)}.items():
        print(f"  {nm:9s}: {c:+.3f}  p={p:.3f}  {'(비유의: 선택근거 없음)' if p>0.05 else '(유의)'}")
    print("\n=== ② 순열검정: val-top{} vs 무작위-{} (DS2 평균) ===".format(k,k))
    obs=d2[np.argsort(-vals)[:k]].mean()
    rng=np.random.RandomState(0); null=np.array([d2[rng.choice(n,k,replace=False)].mean() for _ in range(nperm)])
    pval=float((null>=obs).mean())
    print(f"  val-top{k} DS2평균 = {obs:.4f}   무작위 분포 {null.mean():.4f}±{null.std():.4f} (상위5%={np.percentile(null,95):.4f})")
    print(f"  순열 p = {pval:.3f}  {'→ val필터 이득 = 우연(pure chance)' if pval>0.05 else '→ 유의'}")
    print("\n▶ 논문 문장: 'DS1-val↔DS2 순위상관 비유의(Spearman ρ={:.2f} p={:.2f}; Kendall τ={:.2f} p={:.2f}); "
          "val기반 선택 이득은 순열검정서 우연과 구분 안 됨(p={:.2f}) → 무지도 trimmed ensemble 보고.'".format(
          stats.spearmanr(vals,d2)[0],stats.spearmanr(vals,d2)[1],stats.kendalltau(vals,d2)[0],stats.kendalltau(vals,d2)[1],pval))
    return dict(spearman=stats.spearmanr(vals,d2), kendall=stats.kendalltau(vals,d2), perm_p=pval)

def _trim(Pn):
    if len(Pn)==1: P=Pn[0]; return P/P.sum(1,keepdims=True)
    medS=np.median(Pn[:,:,1],0); corr=np.array([np.corrcoef(Pn[i,:,1],medS)[0,1] for i in range(len(Pn))])
    keep=np.argsort(-corr)[:max(1,int(round(len(Pn)*0.8)))]; P=Pn[keep].mean(0); return P/P.sum(1,keepdims=True)

def stats_bootstrap(fams=("RHYTHM","KOOPMAN","AE","GNN"), seeds=None, B=2000):
    """STEP62 저장 예측으로 trimmed ensemble의 S_PR/PREC/SEN/F1 95% CI (DS2 부트스트랩)."""
    seeds=list(seeds) if seeds is not None else list(range(2000,2020))
    d=np.load(f"{_BASE}/mamba_data.npz"); y,pid=d["y"],d["pid"]; y2=y[np.isin(pid,_DS2)]
    tag="+".join(fams).replace("+","_")
    P=[]
    for s in seeds:
        sp=f"{_STABLE}/{tag}_s{s}.npy"
        if os.path.exists(sp): P.append(np.load(sp))
    if len(P)<2: print(f"✗ 저장 예측 부족({_STABLE}) → STEP62 run_stable 먼저"); return
    Pt=_trim(np.stack(P,0)); sc=Pt[:,1]
    def mets(idx):
        yy=y2[idx]; ss=sc[idx]
        S=average_precision_score((yy==1).astype(int),ss)
        p,r,_=precision_recall_curve((yy==1).astype(int),ss); f=2*p*r/(p+r+1e-9); i=int(np.nanargmax(f))
        return S,p[i],r[i],f[i]
    base=mets(np.arange(len(y2)))
    rng=np.random.RandomState(0); n=len(y2)
    boot=np.array([mets(rng.randint(0,n,n)) for _ in range(B)])   # DS2 비트 부트스트랩
    lbl=["S_PR","PREC","SEN","F1"]
    print(f"=== ③ Bootstrap 95% CI (trimmed ensemble, {len(P)}seed, B={B}) ===")
    for i,l in enumerate(lbl):
        lo,hi=np.percentile(boot[:,i],[2.5,97.5]); print(f"  {l:5s} = {base[i]:.3f}  [95% CI {lo:.3f} – {hi:.3f}]")
    print(f"\n▶ 논문 보고: 'S_PR {base[0]:.3f} [{np.percentile(boot[:,0],2.5):.3f}–{np.percentile(boot[:,0],97.5):.3f}], "
          f"F1 {base[3]:.3f} [{np.percentile(boot[:,3],2.5):.3f}–{np.percentile(boot[:,3],97.5):.3f}] (inter-patient, 무지도 trim ensemble)'")
    return dict(point=base, boot=boot)
