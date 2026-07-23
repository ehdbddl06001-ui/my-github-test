# =============================================================================
#  colab_step47_synergy.py  —  [STEP 47] 전체 시너지 역학실험 (폐기 아이디어 총소환, 밤샘)
#
#  지금까지의 모든 특징군(확정 코어 + 폐기된 것 전부)을 백본에 넣고 2^10 조합 시너지 탐색.
#  feats0(26 de Chazal)는 항상 base. 10개 군을 켜고/끄며(=1024조합) '넣고 빼는' 시너지 지도.
#   코어:  WST(40선택) MORPHO(16) REPOL(4=[0,1,4,5]) DTW(15)
#   시너지: SEGDEV(11) VCG(12)
#   폐기부활: PWAVE(8) XLEAD(9) DENOISE(8) MF(7)      ('적분'은 MORPHO/REPOL에 내장)
#   (2D-DTW는 STEP45에서 정밀도 붕괴 확인 → 제외)
#
#  ★ 크래시-안전/재개가능/Drive 영속:
#    - prep: 각 군 특징행렬을 Drive .npy로 1회 저장(재시작 시 로드→즉시, WST·DTW 재계산 회피)
#    - stage1: 1024 로지스틱 완전탐색, 조합마다 stage1.jsonl 즉시 append (done 스킵)
#    - stage2: 상위K + 레퍼런스 margin CNN 15seed, seed마다 .npy 저장 (중간 죽어도 재개)
#    - 언제 재시작하든 run_synergy() 다시 부르면 이어서 진행. 결과는 synergy_report()로 확인.
#
#  실행(자기 전):
#    exec(open('/content/drive/MyDrive/mitbih/colab_step47_synergy.py').read())
#    run_synergy()                 # prep→stage1→stage2 전자동. 밤새 돌림.
#  재시작 후(이어서):  같은 두 줄 다시 → 남은 것만 진행
#  결과만 보기:        synergy_report()
# =============================================================================
import os, json, itertools
import numpy as np
from sklearn.metrics import average_precision_score, precision_recall_curve

_BASE="/content/drive/MyDrive/mitbih"
_FEATDIR=f"{_BASE}/synergy_feats"; _OUTDIR=f"{_BASE}/synergy_out"; _CNNDIR=f"{_OUTDIR}/cnn"
_DS1=[101,106,108,109,112,114,115,116,118,119,122,124,201,203,205,207,208,209,215,220,223,230]
_DS2=[100,103,105,111,113,117,121,123,200,202,210,212,213,214,219,221,222,228,231,232,233,234]
# 군 순서=비트순서. (소스파일, 컴퓨트키)
_FAM=["WST","MORPHO","REPOL","DTW","SEGDEV","VCG","PWAVE","XLEAD","DENOISE","MF"]
_SRC={"WST":"colab_step12_wst.py","MORPHO":"colab_step15_morpho.py","REPOL":"colab_step18_repol.py",
      "DTW":"colab_step35_dtw.py","SEGDEV":"colab_step28_segdev.py","VCG":"colab_step33_vcg.py",
      "PWAVE":"colab_step9_pwave.py","XLEAD":"colab_step25_xlead.py","DENOISE":"colab_step10_denoise.py",
      "MF":"colab_step17_mf.py"}
_REF_MASKS={"feats0_only":0,
            "core_best(W+M+R+D)":0b0000001111,           # WST+MORPHO+REPOL+DTW
            "synergy6(+SEG+VCG)":0b0000111111}           # +SEGDEV+VCG

def _ensure(pkg):
    import importlib,subprocess,sys
    try: importlib.import_module(pkg)
    except ModuleNotFoundError:
        print(f"'{pkg}' 설치..."); subprocess.run([sys.executable,"-m","pip","install","-q",pkg],check=True)

def _medref(beats,pid):
    r=np.empty_like(beats)
    for p in np.unique(pid): m=pid==p; r[m]=np.median(beats[m],axis=0,keepdims=True)
    return r.astype("float32")
def _f1(y2,s):
    p,r,_=precision_recall_curve((y2==1).astype(int),s); f=2*p*r/(p+r+1e-9); i=int(np.nanargmax(f)); return p[i],r[i],f[i]
def auto_weights(y1,beta=0.9999):
    nN=(y1==0).sum(); nS=max((y1==1).sum(),1); eff=lambda n:(1-beta)/(1-beta**n+1e-12); return float(eff(nS)/eff(nN))
def _maskname(mask): return "+".join([_FAM[i] for i in range(len(_FAM)) if mask>>i&1]) or "feats0only"

# ─────────────────────────── prep: 특징행렬 Drive 영속 ───────────────────────────
def synergy_prep(force=False):
    os.makedirs(_FEATDIR,exist_ok=True); os.makedirs(_CNNDIR,exist_ok=True)
    d=np.load(f"{_BASE}/mamba_data.npz"); beats,feats0,y,pid=d["beat"],d["feats"],d["y"],d["pid"]
    np.save(f"{_FEATDIR}/feats0.npy",feats0.astype("float32"))
    np.save(f"{_FEATDIR}/y.npy",y); np.save(f"{_FEATDIR}/pid.npy",pid)
    m1=np.isin(pid,_DS1); ref=None
    from sklearn.feature_selection import SelectKBest, f_classif
    g=globals()
    def _need(fam): return force or not os.path.exists(f"{_FEATDIR}/{fam}.npy")
    if any(_need(f) for f in _FAM): ref=_medref(beats,pid)
    for fam in _FAM:
        fp=f"{_FEATDIR}/{fam}.npy"
        if not _need(fam): print(f"  {fam:8s} 캐시 있음(Drive)"); continue
        try:
            exec(open(f"{_BASE}/{_SRC[fam]}").read(), g)          # 추출기 로드
            if fam=="WST":
                _ensure("kymatio"); print(f"  {fam:8s} 계산(수분)...")
                raw=g["compute_wst_features"](beats)
                sel=SelectKBest(f_classif,k=min(40,raw.shape[1])).fit(np.nan_to_num(raw[m1]),y[m1])
                mat=np.nan_to_num(sel.transform(np.nan_to_num(raw))).astype("float32")   # WST40 고정선택
            elif fam=="MORPHO": mat=g["extract_morpho_features"](beats,ref,pid)
            elif fam=="REPOL":  mat=g["extract_repol_features"](beats,ref,pid)[:,[0,1,4,5]].astype("float32")
            elif fam=="DTW":    print(f"  {fam:8s} 계산(수분)..."); mat=g["extract_dtw_features"](beats,ref,pid,y)
            elif fam=="SEGDEV": mat=g["extract_segdev_features"](beats,ref,pid)
            elif fam=="VCG":    mat=g["extract_vcg_features"](beats,ref,pid)
            elif fam=="PWAVE":  mat=g["extract_pwave_features"](beats,ref,pid)
            elif fam=="XLEAD":  mat=g["extract_xlead_features"](beats,ref,pid)
            elif fam=="DENOISE":mat=g["extract_pwave_denoised"](beats,ref,pid)
            elif fam=="MF":
                T,Xn=g["build_templates"](beats,y,m1); mat=g["extract_mf_features"](Xn,T)
            mat=np.nan_to_num(mat).astype("float32"); np.save(fp,mat)
            print(f"  {fam:8s} 저장 dim={mat.shape[1]} → {fp}")
        except Exception as e:
            print(f"  ✗ {fam} 실패: {type(e).__name__}: {e} → 이 군 제외하고 진행")
    avail=[f for f in _FAM if os.path.exists(f"{_FEATDIR}/{f}.npy")]
    print(f"\n✔ prep 완료. 사용가능 군: {avail}")
    return avail

def _loadfeats():
    F={"feats0":np.load(f"{_FEATDIR}/feats0.npy")};
    for fam in _FAM:
        fp=f"{_FEATDIR}/{fam}.npy"
        if os.path.exists(fp): F[fam]=np.load(fp)
    y=np.load(f"{_FEATDIR}/y.npy"); pid=np.load(f"{_FEATDIR}/pid.npy")
    return F,y,pid
def _availmask(F):
    m=0
    for i,fam in enumerate(_FAM):
        if fam in F: m|=1<<i
    return m
def _buildX(F,mask):
    parts=[F["feats0"]]
    for i,fam in enumerate(_FAM):
        if mask>>i&1 and fam in F: parts.append(F[fam])
    return np.concatenate(parts,1).astype("float32")

# ─────────────────────────── stage1: 로지스틱 완전탐색 ───────────────────────────
def _done_masks(path):
    s=set()
    if os.path.exists(path):
        for ln in open(path):
            try: s.add(json.loads(ln)["mask"])
            except: pass
    return s
def synergy_stage1():
    from sklearn.preprocessing import StandardScaler
    from sklearn.linear_model import LogisticRegression
    F,y,pid=_loadfeats(); avail=_availmask(F)
    m1=np.isin(pid,_DS1); m2=np.isin(pid,_DS2); y1,y2=y[m1],y[m2]
    path=f"{_OUTDIR}/stage1.jsonl"; done=_done_masks(path)
    allmasks=[mask for mask in range(1<<len(_FAM)) if (mask & ~avail)==0]      # 사용가능 군만
    todo=[mk for mk in allmasks if mk not in done]
    print(f"stage1 로지스틱: 전체 {len(allmasks)} 조합, 남은 {len(todo)} (done {len(done)})")
    for c,mask in enumerate(todo):
        X=_buildX(F,mask)
        sc=StandardScaler().fit(np.nan_to_num(X[m1]))
        X1=np.nan_to_num(sc.transform(np.nan_to_num(X[m1]))); X2=np.nan_to_num(sc.transform(np.nan_to_num(X[m2])))
        clf=LogisticRegression(max_iter=3000,C=0.5,class_weight={0:1,1:3,2:1.5}).fit(X1,y1)
        p=clf.predict_proba(X2)[:,1]; S=average_precision_score((y2==1).astype(int),p); pr,se,f1=_f1(y2,p)
        with open(path,"a") as fptr: fptr.write(json.dumps({"mask":mask,"n":int(bin(mask).count("1")),"dim":int(X.shape[1]),"S":float(S),"PREC":float(pr),"SEN":float(se),"F1":float(f1)})+"\n")
        if (c+1)%50==0 or c==len(todo)-1: print(f"  {c+1}/{len(todo)}  최근 mask={mask}({_maskname(mask)[:40]}) S={S:.4f}")
    print(f"✔ stage1 완료 → {path}")

# ─────────────────────────── stage2: margin CNN 15seed 확정 ───────────────────────────
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

def _train_seed(mask, seed, F, y, pid, beats, ref, mc, Sw):
    import torch, torch.nn as nn, torch.nn.functional as Fn
    from sklearn.preprocessing import RobustScaler
    from sklearn.model_selection import GroupShuffleSplit
    dev="cuda" if torch.cuda.is_available() else "cpu"
    X=_buildX(F,mask); m1=np.isin(pid,_DS1); m2=np.isin(pid,_DS2)
    b1,r1,f1a,y1,p1=beats[m1],ref[m1],X[m1],y[m1],pid[m1]; b2,r2,f2a=beats[m2],ref[m2],X[m2]
    torch.manual_seed(seed); np.random.seed(seed)
    tr,va=next(GroupShuffleSplit(1,test_size=0.2,random_state=seed).split(f1a,y1,groups=p1))
    sc=RobustScaler().fit(f1a[tr]); f1=np.nan_to_num(sc.transform(f1a),posinf=0,neginf=0).astype("float32"); f2=np.nan_to_num(sc.transform(f2a),posinf=0,neginf=0).astype("float32")
    M=_net(X.shape[1]).to(dev); opt=torch.optim.AdamW(M.parameters(),lr=1e-3,weight_decay=1e-4)
    cw=torch.tensor([1.,Sw,1.5],device=dev); mcv=torch.from_numpy(mc).to(dev)
    def met(p,yy): return 0.5*(average_precision_score((yy==1).astype(int),p[:,1])+average_precision_score((yy==2).astype(int),p[:,2]))
    @torch.no_grad()
    def pred(b,r,ft):
        M.eval(); o=[]
        for i in range(0,len(b),4096):
            o.append(torch.softmax(M(torch.from_numpy(b[i:i+4096]).to(dev),torch.from_numpy(r[i:i+4096]).to(dev),torch.from_numpy(ft[i:i+4096]).to(dev)),-1).cpu().numpy())
        return np.concatenate(o)
    ds=torch.utils.data.TensorDataset(*[torch.from_numpy(x) for x in (b1[tr],r1[tr],f1[tr],y1[tr])]); dl=torch.utils.data.DataLoader(ds,batch_size=512,shuffle=True); best=-1; bs=None
    for ep in range(15):
        M.train()
        for bb,rr,ff,yy in dl:
            bb,rr,ff,yy=(t.to(dev) for t in (bb,rr,ff,yy)); opt.zero_grad()
            lo=M(bb,rr,ff); lg=lo-torch.zeros_like(lo).scatter_(1,yy[:,None],mcv[yy][:,None])
            ce=Fn.cross_entropy(lg,yy,reduction="none"); w=cw[yy]; loss=(ce*w).sum()/w.sum()
            loss.backward(); torch.nn.utils.clip_grad_norm_(M.parameters(),1.0); opt.step()
        v=met(pred(b1[va],r1[va],f1[va]),y1[va])
        if v>best: best=v; bs={k:vv.cpu() for k,vv in M.state_dict().items()}
    M.load_state_dict(bs); return pred(b2,r2,f2)

def _trim(Pn):
    medS=np.median(Pn[:,:,1],0); corr=np.array([np.corrcoef(Pn[i,:,1],medS)[0,1] for i in range(len(Pn))])
    keep=np.argsort(-corr)[:max(1,int(round(len(Pn)*0.8)))]; P=Pn[keep].mean(0); return P/P.sum(1,keepdims=True)

def synergy_stage2_cnn(masks, seeds=None):
    seeds=seeds or list(range(1000,1015))
    d=np.load(f"{_BASE}/mamba_data.npz"); beats,y,pid=d["beat"],d["y"],d["pid"]; ref=_medref(beats,pid)
    F,_,_=_loadfeats(); m1=np.isin(pid,_DS1); m2=np.isin(pid,_DS2); y2=y[m2]
    Sw=auto_weights(y[m1]); nc=np.array([(y[m1]==k).sum() for k in range(3)],np.float32); mc=1.0/np.power(nc,0.25); mc=(mc/mc.max()*0.5).astype("float32")
    print(f"stage2 CNN(margin): {len(masks)}조합 × {len(seeds)}seed, Sw={Sw:.1f}, margins={np.round(mc,3)}")
    sumpath=f"{_OUTDIR}/stage2.jsonl"; done_sum=_done_masks(sumpath)
    for mask in masks:
        if mask in done_sum: print(f"  mask={mask} 이미 확정(스킵)"); continue
        preds=[]
        for seed in seeds:
            sp=f"{_CNNDIR}/{mask}_s{seed}.npy"
            if os.path.exists(sp): preds.append(np.load(sp)); continue
            P=_train_seed(mask,seed,F,y,pid,beats,ref,mc,Sw); np.save(sp,P.astype("float32")); preds.append(P)
        Pn=np.stack(preds,0); Pt=_trim(Pn)
        S=average_precision_score((y2==1).astype(int),Pt[:,1]); pr,se,f1=_f1(y2,Pt[:,1])
        with open(sumpath,"a") as fptr: fptr.write(json.dumps({"mask":int(mask),"name":_maskname(mask),"S":float(S),"PREC":float(pr),"SEN":float(se),"F1":float(f1),"seeds":len(seeds)})+"\n")
        print(f"  ✔ mask={mask} {_maskname(mask)[:44]:44s} S={S:.4f} PREC={pr:.3f} SEN={se:.3f} F1={f1:.3f}")
    print(f"✔ stage2 완료 → {sumpath}")

# ─────────────────────────── 결과 리포트 ───────────────────────────
def synergy_report(top=25):
    p1=f"{_OUTDIR}/stage1.jsonl"; p2=f"{_OUTDIR}/stage2.jsonl"
    if not os.path.exists(p1) and not os.path.exists(p2):
        print("아직 저장된 결과 없음. 먼저 run_synergy() 로 실험을 돌려줘 (수 시간).")
        print("  진행 중 확인: stage1은 조합마다, stage2는 seed마다 Drive에 즉시 쌓임 →")
        print("  중간에 synergy_report() 부르면 그때까지 완료분을 보여줌.")
        return
    if os.path.exists(p1):
        rows=[json.loads(l) for l in open(p1)]
        rows.sort(key=lambda r:-r["S"])
        print(f"=== STAGE1(로지스틱) 상위 {top} / 총 {len(rows)} 조합 ===")
        print(f"{'S_PR':>7} {'PREC':>6} {'F1':>6} {'n':>2} {'dim':>4}  조합")
        for r in rows[:top]:
            print(f"{r['S']:7.4f} {r['PREC']:6.3f} {r['F1']:6.3f} {r['n']:2d} {r['dim']:4d}  {_maskname(r['mask'])}")
        # 각 군의 '켜졌을 때 평균 S' (한계기여) 요약
        print(f"\n--- 군별 평균 S (켜짐 vs 꺼짐) : 시너지/기여 요약 ---")
        for i,fam in enumerate(_FAM):
            on=[r["S"] for r in rows if r["mask"]>>i&1]; off=[r["S"] for r in rows if not(r["mask"]>>i&1)]
            if on and off: print(f"  {fam:8s}: 켜짐 {np.mean(on):.4f}  꺼짐 {np.mean(off):.4f}  Δ{np.mean(on)-np.mean(off):+.4f}")
    if os.path.exists(p2):
        rows=[json.loads(l) for l in open(p2)]; rows.sort(key=lambda r:-r["S"])
        print(f"\n=== STAGE2(margin CNN 15seed) 확정 {len(rows)} 조합 ===")
        print(f"{'S_PR':>7} {'PREC':>6} {'SEN':>6} {'F1':>6}  조합")
        for r in rows: print(f"{r['S']:7.4f} {r['PREC']:6.3f} {r['SEN']:6.3f} {r['F1']:6.3f}  {r['name']}")

# ─────────────────────────── 오케스트레이터 ───────────────────────────
def run_synergy(topK=12, stage2_seeds=None):
    print("="*70+"\n[STEP47] 전체 시너지 역학실험 — prep→stage1→stage2 (재개가능, Drive영속)\n"+"="*70)
    synergy_prep()
    synergy_stage1()
    # stage1 상위 topK + 레퍼런스 마스크 선정
    rows=[json.loads(l) for l in open(f"{_OUTDIR}/stage1.jsonl")]; rows.sort(key=lambda r:-r["S"])
    masks=[r["mask"] for r in rows[:topK]]
    for nm,mk in _REF_MASKS.items():
        if mk not in masks: masks.append(mk)
    print(f"\nstage2 대상 {len(masks)}조합(상위{topK}+레퍼런스). CNN 15seed 시작...")
    synergy_stage2_cnn(masks, seeds=stage2_seeds)
    print("\n"+"="*70); synergy_report()
    print("\n자고 일어나서: synergy_report() 만 불러도 저장된 결과 확인 가능.")
