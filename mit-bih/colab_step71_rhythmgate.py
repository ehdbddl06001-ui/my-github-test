# =============================================================================
#  colab_step71_rhythmgate.py  —  [STEP 71] 리듬 신뢰도 게이트 (하드 레코드 공략)
#
#  STEP70 정직진단: 환자매크로 F1 ≈ 0.34 (44-CV 0.342±0.126)가 진짜 성능. micro 0.76은 232 착시.
#  실패 레코드가 한 종류다: 200(SEN .07~.17) 213(.07~.14) 210(.23) 113(.17) 219(FP폭발)
#   → 전부 AF·nodal·flutter 계열 = RR innovation(조기성)이 물리적으로 무의미해지는 환자.
#  처방: 환자별 '리듬 불규칙도'를 라벨프리로 재고, ①특징으로 넣고 ②게이트로 쓴다.
#   불규칙(AF) → RR축 신뢰↓·형태축↑ / 규칙적 → RR축 신뢰↑ (S/V class-aware 게이트와 같은 수법)
#  ★ STEP67 conf_cut이 못 잡던 '어려운 환자 자가인식'의 정답: 형태지표로 리듬장애를 잡으려 한 게
#    범주오류였다. 리듬장애는 리듬지표로 잡아야 한다.
#
#  불규칙도(라벨0, 환자 본인 RR-innovation 캐시에서): std(pre innov)·median|innov|·std(보상지수)
#   ·RR innovation 엔트로피 → DS1 통계로 표준화 → per-beat 브로드캐스트.
#  ★ 평가는 '환자단위 매크로 F1'이 유일 채택기준(micro는 232 지배라 헤드라인 금지).
#
#  선행: colab_step67~70 (Drive)
#  실행:
#    exec(open('/content/drive/MyDrive/mitbih/colab_step71_rhythmgate.py').read())
#    diag_irreg()                 # 불규칙도가 실제 AF레코드를 집어내나(학습없음, 빠름)
#    OUT=run_gate(n_rep=3)        # 게이트 없음 vs 있음 — 환자매크로 F1 기준 A/B
# =============================================================================
import os
import numpy as np
from sklearn.metrics import average_precision_score

_BASE="/content/drive/MyDrive/mitbih"; _FEATDIR=f"{_BASE}/synergy_feats"
if "_pp_center2" not in globals():
    exec(open(f"{_BASE}/colab_step70_evalintegrity.py").read(), globals())   # 70→69→68→67
_AF_LIKE=[200,202,210,213,219,221,222]     # 참고: AF/flutter/nodal 계열(라벨 아님, 진단표시용)

def _prf2(v, yy):
    yp=(yy==1); tp=float((v&yp).sum()); fp=float((v&~yp).sum()); fn=float((~v&yp).sum())
    pr=tp/(tp+fp+1e-9); se=tp/(tp+fn+1e-9); return pr,se,2*pr*se/(pr+se+1e-9)

def _macroF1(v, y2, pid2, exclude=()):
    f=[]
    for p in np.unique(pid2):
        if p in exclude: continue
        m=pid2==p
        if (y2[m]==1).sum()==0: continue
        f.append(_prf2(v[m],y2[m])[2])
    return float(np.mean(f)), float(np.std(f)), len(f)

# ─────────────── 리듬 불규칙도(라벨프리, 환자 본인 RR-innovation) ───────────────
def rhythm_irregularity(pid, RHY=None, verbose=True):
    """환자별 리듬 불규칙도 4종 → per-beat 브로드캐스트 (N,4). 라벨 0, 본인 RR만.
       RHYTHM 캐시 컬럼: 6=RR조기성(pre innov) 7=|조기성| 8=보상휴지 9=보상성지수"""
    if RHY is None: RHY=np.load(f"{_FEATDIR}/RHYTHM.npy")
    pre=RHY[:,6]; ab=RHY[:,7]; comp=RHY[:,9]
    Z=np.zeros((len(pid),4),np.float32); per={}
    for p in np.unique(pid):
        m=pid==p; v=pre[m]
        s1=float(np.std(v))                                   # 조기성 산포(AF↑)
        s2=float(np.median(ab[m]))                            # 전형적 |조기성|(AF↑)
        s3=float(np.std(comp[m]))                             # 보상성 산포(AF↑)
        h,_=np.histogram(v,bins=16,range=(-1,1)); pmf=h/max(h.sum(),1)
        s4=float(-(pmf[pmf>0]*np.log(pmf[pmf>0])).sum())      # innovation 엔트로피(AF↑)
        Z[m]=[s1,s2,s3,s4]; per[int(p)]=(s1,s2,s3,s4)
    if verbose:
        m1=np.isin(pid,_DS1); mu=Z[m1].mean(0); sd=Z[m1].std(0)+1e-6
        print(f"  불규칙도 DS1 기준 표준화 μ={np.round(mu,3)} σ={np.round(sd,3)}")
    return Z, per

def _standardize_ds1(Z, pid):
    m1=np.isin(pid,_DS1); mu=Z[m1].mean(0); sd=Z[m1].std(0)+1e-6
    return ((Z-mu)/sd).astype("float32")

def diag_irreg():
    """불규칙도가 실제 AF 레코드를 집어내는지(학습 없음). STEP67 형태 conf와 대조."""
    d=np.load(f"{_BASE}/mamba_data.npz"); pid=d["pid"]
    Z,per=rhythm_irregularity(pid)
    Zs=_standardize_ds1(Z,pid)
    score={}
    for p in np.unique(pid):
        m=pid==p; score[int(p)]=float(Zs[m][0].mean())        # 4지표 평균 = 종합 불규칙도
    d2=sorted([(p,s) for p,s in score.items() if p in _DS2], key=lambda x:-x[1])
    print("\n DS2 리듬 불규칙도 상위(=AF/nodal 후보, 라벨프리):")
    for p,s in d2[:8]:
        mk="★AF계열" if p in _AF_LIKE else ""
        print(f"   rec {p}: 불규칙도={s:+.2f}  {mk}")
    hi=[p for p,s in d2[:7]]
    print(f"\n  상위7 중 AF계열 적중: {sorted(set(hi)&set(_AF_LIKE))}  ({len(set(hi)&set(_AF_LIKE))}/7)")
    print(f"  → 적중 높으면: 리듬지표가 '어려운 환자'를 라벨없이 식별(STEP67 형태 conf는 실패했던 것)")
    return score

# ─────────────── 게이트 네트워크 ───────────────
def _net_gate(fdim, rdim, zdim=4, use_gate=True):
    """RHYTHM블록(rdim)과 나머지(fdim-rdim)를 분리 인코딩 → 불규칙도 z로 게이트 융합."""
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
            s.fr=nn.Sequential(nn.Linear(rdim,32),nn.ReLU(),nn.Linear(32,64),nn.ReLU())      # RR축
            s.fo=nn.Sequential(nn.Linear(fdim-rdim,64),nn.ReLU(),nn.Linear(64,64),nn.ReLU()) # 형태축
            s.g=nn.Sequential(nn.Linear(zdim,16),nn.ReLU(),nn.Linear(16,1))                  # 리듬신뢰 게이트
            s.use=use_gate
            s.cls=nn.Sequential(nn.Linear(192,64),nn.ReLU(),nn.Linear(64,3))
        def forward(s,b,r,ft,fr,z):
            z1=s.e(b); z2=s.e(r); zb=s.sia(torch.cat([z1,z2,z1-z2,(z1-z2).abs()],-1))
            zz=z1+torch.sigmoid(s.gate(torch.cat([z1,zb],-1)))*zb
            zp=torch.softmax((zz@s.proto.t())*(64**-0.5),-1)@s.proto
            hr=s.fr(fr); ho=s.fo(ft)
            if s.use:
                w=torch.sigmoid(s.g(z))          # w=리듬 신뢰도(불규칙↑ → 학습으로 w↓ 유도)
                fus=w*hr+(1-w)*ho                # 불규칙하면 형태축으로 무게 이동
            else:
                fus=0.5*(hr+ho)                  # 게이트 없음(동일 용량 대조)
            return s.cls(torch.cat([zz,zp,fus],-1))
    return Net()

def _train_gate(Fo, Fr, Z, beats, ref, y, pid, mc, Sw, tr, va, te, seed, use_gate):
    import torch, torch.nn.functional as Fn
    from sklearn.preprocessing import RobustScaler
    from sklearn.model_selection import GroupShuffleSplit
    dev="cuda" if torch.cuda.is_available() else "cpu"
    torch.manual_seed(seed); np.random.seed(seed)
    it,iv=next(GroupShuffleSplit(1,test_size=0.2,random_state=seed).split(Fo[tr],y[tr],groups=pid[tr]))
    so=RobustScaler().fit(Fo[tr][it]); sr=RobustScaler().fit(Fr[tr][it])
    T=lambda X,s: np.nan_to_num(s.transform(X),posinf=0,neginf=0).astype("float32")
    M=_net_gate(Fo.shape[1]+Fr.shape[1], Fr.shape[1], Z.shape[1], use_gate).to(dev)
    opt=torch.optim.AdamW(M.parameters(),lr=1e-3,weight_decay=1e-4)
    cw=torch.tensor([1.,Sw,1.5],device=dev); mcv=torch.from_numpy(mc).to(dev)
    def pack(idx): return (beats[idx],ref[idx],T(Fo[idx],so),T(Fr[idx],sr),Z[idx],y[idx])
    trb,trr,tro,trf,trz,try_=pack(tr[it]); vab,var_,vao,vaf,vaz,vay=pack(tr[iv])
    teb,ter,teo,tef,tez,_=pack(te)
    @torch.no_grad()
    def pred(b,r,o,f,z):
        M.eval(); out=[]
        for i in range(0,len(b),4096):
            t=lambda x: torch.from_numpy(x[i:i+4096]).to(dev)
            out.append(torch.softmax(M(t(b),t(r),t(o),t(f),t(z)),-1).cpu().numpy())
        return np.concatenate(out)
    ds=torch.utils.data.TensorDataset(*[torch.from_numpy(x) for x in (trb,trr,tro,trf,trz,try_)])
    dl=torch.utils.data.DataLoader(ds,batch_size=512,shuffle=True); best=-1; bs=None
    for ep in range(15):
        M.train()
        for bb,rr,oo,ff,zz,yy in dl:
            bb,rr,oo,ff,zz,yy=(t.to(dev) for t in (bb,rr,oo,ff,zz,yy)); opt.zero_grad()
            lo=M(bb,rr,oo,ff,zz); lg=lo-torch.zeros_like(lo).scatter_(1,yy[:,None],mcv[yy][:,None])
            ce=Fn.cross_entropy(lg,yy,reduction="none"); loss=(ce*cw[yy]).sum()/cw[yy].sum()
            loss.backward(); torch.nn.utils.clip_grad_norm_(M.parameters(),1.0); opt.step()
        pv=pred(vab,var_,vao,vaf,vaz)
        v=0.5*(average_precision_score((vay==1).astype(int),pv[:,1])+average_precision_score((vay==2).astype(int),pv[:,2]))
        if v>best: best=v; bs={k:vv.cpu() for k,vv in M.state_dict().items()}
    M.load_state_dict(bs)
    va_all=pack(va); pv=pred(va_all[0],va_all[1],va_all[2],va_all[3],va_all[4])
    return pv, pred(teb,ter,teo,tef,tez)

def run_gate(fams=("RHYTHM","KOOPMAN","AE","GNN"), n_rep=3, frac=0.6, conf_cut=0.879):
    """게이트 없음 vs 있음 — 환자매크로 F1(유일 채택기준) + 232제외 + S_PR."""
    from sklearn.model_selection import GroupKFold
    _determinism()
    beats,y,pid,F,tag=_bestF(fams)
    # 특징 분리: RHYTHM(10) vs 나머지
    RHY=np.load(f"{_FEATDIR}/RHYTHM.npy"); rd=RHY.shape[1]
    base=[np.load(f"{_FEATDIR}/{n}.npy") for n in ["feats0","WST","MORPHO","REPOL","DTW"]]
    rest=[np.load(f"{_FEATDIR}/{n}.npy") for n in fams if n!="RHYTHM"]
    Z,_=rhythm_irregularity(pid,RHY,verbose=True); Z=_standardize_ds1(Z,pid)
    Fo=np.concatenate(base+rest+[Z],1).astype("float32")     # 형태축(+불규칙도 특징으로도)
    Fr=RHY.astype("float32")                                 # RR축
    m1=np.isin(pid,_DS1); m2=np.isin(pid,_DS2); y2=y[m2]; pid2=pid[m2]
    Sw=auto_weights(y[m1]); nc=np.array([(y[m1]==k).sum() for k in range(3)],np.float32)
    mc=(1.0/np.power(nc,0.25)); mc=(mc/mc.max()*0.5).astype("float32")
    ref=robust_template(beats,pid,frac=frac,conf_cut=conf_cut,verbose=False)[0]
    idx1=np.where(m1)[0]; idx2=np.where(m2)[0]; y1=y[idx1]; p1=pid[idx1]
    print(f"\n특징 분리: RR축 {Fr.shape[1]}차원 | 형태축 {Fo.shape[1]}차원(불규칙도4 포함)")
    print(f"GroupKFold(5) × {n_rep}rep = {5*n_rep}학습/arm.  채택기준=환자매크로 F1")
    gkf=GroupKFold(n_splits=5); RES={}
    for use_gate in (False,True):
        dC=[]
        for rep in range(n_rep):
            order=np.argsort([(hash((int(p),rep))%1000) for p in p1])
            for tr_o,va_o in gkf.split(idx1[order],y1[order],groups=p1[order]):
                tr=idx1[order][tr_o]; va=idx1[order][va_o]; seed=1000*rep+int(va_o[0])
                pv,p2=_train_gate(Fo,Fr,Z,beats,ref,y,pid,mc,Sw,tr,va,idx2,seed,use_gate)
                sc=pv[:,1]; yc=y[va]; pc=pid[va]; s2=p2[:,1]
                cc=_pp_center2(sc,pc); c2=_pp_center2(s2,pid2); tC=_best_t_f1(cc,yc)
                dC.append(c2-tC)
        s=np.mean(dC,0); v=s>=0
        mac,sd,n=_macroF1(v,y2,pid2); macx,sdx,nx=_macroF1(v,y2,pid2,exclude=(232,))
        ex=pid2!=232; prx,sex,f1x=_prf2(v[ex],y2[ex]); pr,se,f1=_prf2(v,y2)
        spr=average_precision_score((y2==1).astype(int),s); sprx=average_precision_score((y2[ex]==1).astype(int),s[ex])
        nm="게이트ON" if use_gate else "게이트OFF"
        print(f"\n[{nm}]  ★환자매크로 F1={mac:.3f} ±{sd:.3f} (n={n})   232제외 매크로={macx:.3f}")
        print(f"        232제외 micro F1={f1x:.3f} (SEN {sex:.3f}/PREC {prx:.3f})   micro(참고)={f1:.3f}")
        print(f"        S_PR 전체={spr:.3f}  232제외={sprx:.3f}")
        # 하드 레코드 개별
        hard=[200,213,210,113,219]
        hs=[]
        for p in hard:
            mp=pid2==p
            if (y2[mp]==1).sum()==0: continue
            a,b_,c=_prf2(v[mp],y2[mp]); hs.append(f"{p}:F1={c:.2f}(SEN{b_:.2f})")
        print(f"        하드레코드 {' '.join(hs)}")
        RES[nm]=dict(macro=mac,macro_ex=macx,micro_ex=f1x,S_PR_ex=sprx,v=v,s=s)
    a=RES["게이트OFF"]; b=RES["게이트ON"]
    print(f"\n▶ 게이트 효과: Δ환자매크로={b['macro']-a['macro']:+.3f}  Δ232제외매크로={b['macro_ex']-a['macro_ex']:+.3f}"
          f"  ΔS_PR(232제외)={b['S_PR_ex']-a['S_PR_ex']:+.3f}")
    print(f"  ★ 환자매크로 Δ>0 이고 하드레코드 F1이 오르면 = 리듬게이트 채택. micro는 헤드라인 금지.")
    return RES
