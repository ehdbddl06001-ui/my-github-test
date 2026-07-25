# =============================================================================
#  colab_crossdb.py  —  [교차DB ②③] MIT-BIH 학습 → INCART 적용 (외부 검증)
#
#  MIT-BIH 전체로 학습한 앙상블을 INCART(다른 DB)에 재학습·튜닝 없이 적용 → 진짜 일반화 검증.
#  v1 특징(두 DB에서 우리 코드가 동일 계산하는 자립 특징): WST+MORPHO+REPOL+KOOPMAN+GNN.
#   (제외: feats0[외부]·RHYTHM[feats0-RR]·DTW[DS1템플릿]·AE[모델저장] → v2에서)
#  스케일 매칭: 두 DB 비트를 per-beat z정규(진폭 불일치 제거). WST 선택은 MIT-BIH서 fit·양쪽 적용.
#  두 가지 보고: (a) raw-transfer  (b) BN-적응(INCART 입력분포로 BatchNorm 재보정, 라벨X=오염X).
#   raw가 낮고 BN적응이 회복되면 = '모델 과적합 아니라 분포 shift'였음(해석 분리).
#
#  선행: colab_prep_all.py(MIT-BIH 캐시) + incart_data.npz(전처리 완료) + 추출기 소스들 Drive에
#  실행:
#    exec(open('/content/drive/MyDrive/mitbih/colab_crossdb.py').read())
#    run_crossdb(seeds=list(range(2000,2010)))   # ~10seed 앙상블
# =============================================================================
import os
import numpy as np
from sklearn.metrics import average_precision_score, precision_recall_curve

_BASE="/content/drive/MyDrive/mitbih"; _FEATDIR=f"{_BASE}/synergy_feats"
_DS1=[101,106,108,109,112,114,115,116,118,119,122,124,201,203,205,207,208,209,215,220,223,230]
_DS2=[100,103,105,111,113,117,121,123,200,202,210,212,213,214,219,221,222,228,231,232,233,234]

def _f1(y2,s):
    p,r,_=precision_recall_curve((y2==1).astype(int),s); f=2*p*r/(p+r+1e-9); i=int(np.nanargmax(f)); return p[i],r[i],f[i]
def auto_weights(y1,beta=0.9999):
    nN=(y1==0).sum(); nS=max((y1==1).sum(),1); eff=lambda n:(1-beta)/(1-beta**n+1e-12); return float(eff(nS)/eff(nN))
def _znorm(b):  # 비트별 리드별 z (진폭 스케일 매칭)
    return ((b-b.mean(2,keepdims=True))/(b.std(2,keepdims=True)+1e-6)).astype("float32")
def _medref(beats,pid):
    r=np.empty_like(beats)
    for p in np.unique(pid): m=pid==p; r[m]=np.median(beats[m],0,keepdims=True)
    return r.astype("float32")
def _determinism():
    import torch
    os.environ["CUBLAS_WORKSPACE_CONFIG"]=":4096:8"; torch.backends.cudnn.deterministic=True; torch.backends.cudnn.benchmark=False
    try: torch.use_deterministic_algorithms(True, warn_only=True)
    except Exception: pass

def _incart_feats():
    """INCART 비트에서 v1 자립특징 계산(우리 추출기). 이미 저장돼 있으면 로드."""
    fp=f"{_BASE}/incart_feats.npz"
    if os.path.exists(fp):
        d=np.load(fp); print("  INCART 특징 캐시 로드"); return {k:d[k] for k in d.files}
    g=globals()
    for src in ("colab_step15_morpho.py","colab_step18_repol.py","colab_step52_newfeats.py"):
        exec(open(f"{_BASE}/{src}").read(), g)
    d=np.load(f"{_BASE}/incart_data.npz"); beats,y,pid=d["beat"],d["y"],d["pid"]; ref=_medref(beats,pid)
    print("  INCART 특징 계산: MORPHO·REPOL·KOOPMAN·GNN·WST...")
    F={"MORPHO":g["extract_morpho_features"](beats,ref,pid),
       "REPOL":g["extract_repol_features"](beats,ref,pid)[:,[0,1,4,5]].astype("float32"),
       "KOOPMAN":g["extract_koopman_features"](beats,pid,y),
       "GNN":g["extract_gnn_features"](beats,pid,y)}
    exec(open(f"{_BASE}/colab_step12_wst.py").read(), g); F["WST_raw"]=g["compute_wst_features"](beats)
    np.savez(f"{_BASE}/incart_feats.npz",**F); print("  → incart_feats.npz 저장")
    return F

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

def run_crossdb(seeds=None, Kwst=40):
    import torch, torch.nn as nn, torch.nn.functional as Fn
    from sklearn.preprocessing import RobustScaler
    from sklearn.feature_selection import SelectKBest, f_classif
    _determinism(); seeds=list(seeds) if seeds is not None else list(range(2000,2010)); dev="cuda" if torch.cuda.is_available() else "cpu"
    # ── MIT-BIH (학습) ──
    d=np.load(f"{_BASE}/mamba_data.npz"); mb=_znorm(d["beat"]); my=d["y"]; mpid=d["pid"]; mref=_medref(mb,mpid)
    exec(open(f"{_BASE}/colab_step12_wst.py").read(), globals()); mWSTraw=globals()["compute_wst_features"](d["beat"])
    sel=SelectKBest(f_classif,k=Kwst).fit(np.nan_to_num(mWSTraw),my)           # WST 선택 = MIT-BIH서 fit
    def wsel(raw): return np.nan_to_num(sel.transform(np.nan_to_num(raw))).astype("float32")
    Fm=np.concatenate([wsel(mWSTraw), np.load(f"{_FEATDIR}/MORPHO.npy"), np.load(f"{_FEATDIR}/REPOL.npy"),
                       np.load(f"{_FEATDIR}/KOOPMAN.npy"), np.load(f"{_FEATDIR}/GNN.npy")],1).astype("float32")
    # ── INCART (테스트) ──
    di=np.load(f"{_BASE}/incart_data.npz"); ib=_znorm(di["beat"]); iy=di["y"]; ipid=di["pid"]; iref=_medref(ib,ipid)
    IF=_incart_feats()
    Fi=np.concatenate([wsel(IF["WST_raw"]), IF["MORPHO"], IF["REPOL"], IF["KOOPMAN"], IF["GNN"]],1).astype("float32")
    print(f"MIT-BIH {len(my)}비트(N/S/V={int((my==0).sum())}/{int((my==1).sum())}/{int((my==2).sum())}) → INCART {len(iy)}비트(N/S/V={int((iy==0).sum())}/{int((iy==1).sum())}/{int((iy==2).sum())})")
    print(f"특징차원 {Fm.shape[1]}  (WST{Kwst}+MORPHO16+REPOL4+KOOPMAN5+GNN5)")
    Sw=auto_weights(my); nc=np.array([(my==k).sum() for k in range(3)],np.float32); mc=(1.0/np.power(nc,0.25)); mc=(mc/mc.max()*0.5).astype("float32")
    def met(p,yy): return (average_precision_score((yy==1).astype(int),p[:,1]),average_precision_score((yy==2).astype(int),p[:,2]))
    @torch.no_grad()
    def pred(M,b,r,ft,bn=False):
        if bn:  # BN 적응: INCART 입력으로 BatchNorm 통계 재보정(라벨X)
            for mod in M.modules():
                if isinstance(mod,nn.BatchNorm1d): mod.reset_running_stats(); mod.momentum=None
            M.train()
            for i in range(0,len(b),512): M(torch.from_numpy(b[i:i+512]).to(dev),torch.from_numpy(r[i:i+512]).to(dev),torch.from_numpy(ft[i:i+512]).to(dev))
        M.eval(); o=[]
        for i in range(0,len(b),4096):
            o.append(torch.softmax(M(torch.from_numpy(b[i:i+4096]).to(dev),torch.from_numpy(r[i:i+4096]).to(dev),torch.from_numpy(ft[i:i+4096]).to(dev)),-1).cpu().numpy())
        return np.concatenate(o)
    def train_one(seed):
        torch.manual_seed(seed); np.random.seed(seed)
        sc=RobustScaler().fit(Fm); f_tr=np.nan_to_num(sc.transform(Fm),posinf=0,neginf=0).astype("float32")
        f_in=np.nan_to_num(sc.transform(Fi),posinf=0,neginf=0).astype("float32")
        M=_net(Fm.shape[1]).to(dev); opt=torch.optim.AdamW(M.parameters(),lr=1e-3,weight_decay=1e-4)
        cw=torch.tensor([1.,Sw,1.5],device=dev); mcv=torch.from_numpy(mc).to(dev)
        ds=torch.utils.data.TensorDataset(*[torch.from_numpy(x) for x in (mb,mref,f_tr,my)]); dl=torch.utils.data.DataLoader(ds,batch_size=512,shuffle=True)
        for ep in range(15):
            M.train()
            for bb,rr,ff,yy in dl:
                bb,rr,ff,yy=(t.to(dev) for t in (bb,rr,ff,yy)); opt.zero_grad()
                lo=M(bb,rr,ff); lg=lo-torch.zeros_like(lo).scatter_(1,yy[:,None],mcv[yy][:,None])
                ce=Fn.cross_entropy(lg,yy,reduction="none"); loss=(ce*cw[yy]).sum()/cw[yy].sum()
                loss.backward(); torch.nn.utils.clip_grad_norm_(M.parameters(),1.0); opt.step()
        praw=pred(M,ib,iref,f_in,bn=False)
        Mbn=_net(Fm.shape[1]).to(dev); Mbn.load_state_dict(M.state_dict()); pbn=pred(Mbn,ib,iref,f_in,bn=True)
        return praw,pbn
    def trim(Pn):
        medS=np.median(Pn[:,:,1],0); corr=np.array([np.corrcoef(Pn[i,:,1],medS)[0,1] for i in range(len(Pn))])
        keep=np.argsort(-corr)[:max(1,int(round(len(Pn)*0.8)))]; P=Pn[keep].mean(0); return P/P.sum(1,keepdims=True)
    print(f"\n결정성 ON  {len(seeds)}seed 앙상블 (MIT-BIH 전체 학습 → INCART)")
    RAW=[]; BN=[]
    for s in seeds: pr,pb=train_one(s); RAW.append(pr); BN.append(pb)
    for nm,P in [("raw-transfer",np.stack(RAW,0)),("BN-adapted",np.stack(BN,0))]:
        Pt=trim(P); S,V=met(Pt,iy); pr,se,f1=_f1(iy,Pt[:,1])
        print(f"  {nm:14s}: S_PR={S:.4f} PREC={pr:.3f} SEN={se:.3f} F1={f1:.3f}  (V_PR={V:.3f})")
    print(f"\n  ★ S_PR가 MIT-BIH(0.78)에 가까우면 = 진짜 일반화(외부DB 전이). BN적응이 raw보다 크게↑면 = 분포shift가 주원인.")
    return dict(raw=np.stack(RAW,0), bn=np.stack(BN,0), iy=iy)
