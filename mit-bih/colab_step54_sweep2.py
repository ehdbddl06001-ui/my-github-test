# =============================================================================
#  colab_step54_sweep2.py  —  [STEP 54] 고정백본 family 시너지 sweep (2^7=128, 밤샘·크래시안전)
#
#  백본 고정: feats0+WST40+MORPHO+REPOL4+DTW  (토글 안 함)
#  토글 7군: RHYTHM NOISE KOOPMAN AE GNN SEGDEV VCG  → 128 조합
#  목표: 신규축(AE·RHYTHM·GNN…)의 최소·최선 family 조합 확정(Occam). TOPAUC(31) 대체 후보.
#  2단계(비용↓): ① 128조합 × screen_seeds(4) 스크린 → ② 상위 topK + 레퍼런스 × confirm_seeds(15) 확정.
#  margin CNN(LDAM). 로지스틱 스크린 금지(innovation류 과소평가).
#
#  ★ 크래시안전/재개: seed 예측을 Drive에 즉시 저장({mask}_s{seed}.npy), 조합끝나면 jsonl append.
#    런타임 끊기면 run_sweep2() 다시 실행 → 완료분 스킵하고 이어서. 결과: sweep2_report().
#
#  선행: colab_prep_all.py 실행(synergy_feats/*.npy 전부)
#  실행(자기 전):
#    exec(open('/content/drive/MyDrive/mitbih/colab_step54_sweep2.py').read())
#    run_sweep2()                 # 밤새. 끊기면 같은 줄 다시 → 이어서
#  결과만:  sweep2_report()
# =============================================================================
import os, json
import numpy as np
from sklearn.metrics import average_precision_score, precision_recall_curve

_BASE="/content/drive/MyDrive/mitbih"; _FEATDIR=f"{_BASE}/synergy_feats"
_OUT=f"{_BASE}/synergy2_out"; _CNN=f"{_OUT}/cnn"
_DS1=[101,106,108,109,112,114,115,116,118,119,122,124,201,203,205,207,208,209,215,220,223,230]
_DS2=[100,103,105,111,113,117,121,123,200,202,210,212,213,214,219,221,222,228,231,232,233,234]
_BACKBONE=["feats0","WST","MORPHO","REPOL","DTW"]
_TOGGLE=["RHYTHM","NOISE","KOOPMAN","AE","GNN","SEGDEV","VCG"]      # 비트0..6
# 레퍼런스(항상 확정): 백본만 / RHYTHM / AE / RHYTHM+AE / RHYTHM+AE+GNN / 전체
_REFS={0:"backbone", 1<<0:"+RHYTHM", 1<<3:"+AE", (1<<0)|(1<<3):"+RHYTHM+AE",
       (1<<0)|(1<<3)|(1<<4):"+RHYTHM+AE+GNN", 127:"+ALL7"}

def _f1(y2,s):
    p,r,_=precision_recall_curve((y2==1).astype(int),s); f=2*p*r/(p+r+1e-9); i=int(np.nanargmax(f)); return p[i],r[i],f[i]
def auto_weights(y1,beta=0.9999):
    nN=(y1==0).sum(); nS=max((y1==1).sum(),1); eff=lambda n:(1-beta)/(1-beta**n+1e-12); return float(eff(nS)/eff(nN))
def _Lnpy(name):
    p=f"{_FEATDIR}/{name}.npy"; return np.load(p) if os.path.exists(p) else None
def _maskname(mask):
    on=[_TOGGLE[i] for i in range(len(_TOGGLE)) if mask>>i&1]; return "backbone" if not on else "+".join(on)

def _load():
    d=np.load(f"{_BASE}/mamba_data.npz"); beats,y,pid=d["beat"],d["y"],d["pid"]
    BB=[_Lnpy(n) for n in _BACKBONE]
    if any(b is None for b in BB): raise RuntimeError("백본 캐시 없음 → colab_prep_all.py 먼저")
    back=np.concatenate(BB,1).astype("float32")
    tog={n:_Lnpy(n) for n in _TOGGLE if _Lnpy(n) is not None}
    return beats,y,pid,back,tog
def _buildX(back,tog,mask):
    parts=[back]
    for i,n in enumerate(_TOGGLE):
        if mask>>i&1 and n in tog: parts.append(tog[n])
    return np.concatenate(parts,1).astype("float32")

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
    ds=torch.utils.data.TensorDataset(*[torch.from_numpy(x) for x in (b1[tr],r1[tr],f1[tr],y1[tr])]); dl=torch.utils.data.DataLoader(ds,batch_size=512,shuffle=True); best=-1; bs=None
    for ep in range(15):
        M.train()
        for bb,rr,ff,yy in dl:
            bb,rr,ff,yy=(t.to(dev) for t in (bb,rr,ff,yy)); opt.zero_grad()
            lo=M(bb,rr,ff); lg=lo-torch.zeros_like(lo).scatter_(1,yy[:,None],mcv[yy][:,None])
            ce=Fn.cross_entropy(lg,yy,reduction="none"); wv=cw[yy]; loss=(ce*wv).sum()/wv.sum()
            loss.backward(); torch.nn.utils.clip_grad_norm_(M.parameters(),1.0); opt.step()
        v=met(pred(b1[va],r1[va],f1[va]),y1[va])
        if v>best: best=v; bs={k:vv.cpu() for k,vv in M.state_dict().items()}
    M.load_state_dict(bs); return pred(b2,r2,f2)

def _trim(Pn):
    if len(Pn)==1: P=Pn[0]; return P/P.sum(1,keepdims=True)
    medS=np.median(Pn[:,:,1],0); corr=np.array([np.corrcoef(Pn[i,:,1],medS)[0,1] for i in range(len(Pn))])
    keep=np.argsort(-corr)[:max(1,int(round(len(Pn)*0.8)))]; P=Pn[keep].mean(0); return P/P.sum(1,keepdims=True)

def _eval_mask(mask, nseeds, ctx):
    """mask를 nseeds로 학습·평가. seed 예측을 Drive에 즉시저장(크래시안전). 트림 지표 반환."""
    beats,ref,y,pid,back,tog,mc,Sw,seeds,y2=ctx
    F=_buildX(back,tog,mask); preds=[]
    for s in seeds[:nseeds]:
        sp=f"{_CNN}/{mask}_s{s}.npy"
        if os.path.exists(sp):
            preds.append(np.load(sp)); continue
        P=_train_seed(F,beats,ref,y,pid,mc,Sw,s); np.save(sp,P.astype("float32")); preds.append(P)
    Pt=_trim(np.stack(preds,0)); S=average_precision_score((y2==1).astype(int),Pt[:,1])
    V=average_precision_score((y2==2).astype(int),Pt[:,2]); pr,se,f1=_f1(y2,Pt[:,1])
    return {"mask":int(mask),"name":_maskname(mask),"n":int(bin(mask).count("1")),
            "S":float(S),"PREC":float(pr),"SEN":float(se),"F1":float(f1),"V":float(V),"seeds":int(nseeds)}

def _done(path):
    s={}
    if os.path.exists(path):
        for ln in open(path):
            try: r=json.loads(ln); s[r["mask"]]=r
            except: pass
    return s

def run_sweep2(screen_seeds=4, confirm_seeds=15, topK=12):
    os.makedirs(_CNN,exist_ok=True)
    beats,y,pid,back,tog=_load(); ref=np.empty_like(beats)
    for p in np.unique(pid): m=pid==p; ref[m]=np.median(beats[m],0,keepdims=True)
    ref=ref.astype("float32"); m1=np.isin(pid,_DS1); m2=np.isin(pid,_DS2); y2=y[m2]
    Sw=auto_weights(y[m1]); nc=np.array([(y[m1]==k).sum() for k in range(3)],np.float32); mc=(1.0/np.power(nc,0.25)); mc=(mc/mc.max()*0.5).astype("float32")
    seeds=list(range(2000,2000+confirm_seeds))
    ctx=(beats,ref,y,pid,back,tog,mc,Sw,seeds,y2)
    print(f"토글군: {list(tog.keys())}  (백본 dim={back.shape[1]}, Sw={Sw:.1f})")
    # ── STAGE 1: 스크린(128 × screen_seeds) ──
    sp=f"{_OUT}/screen.jsonl"; done=_done(sp); allmasks=list(range(1<<len(_TOGGLE)))
    todo=[mk for mk in allmasks if mk not in done]
    print(f"[스크린] 전체 {len(allmasks)} 조합 × {screen_seeds}seed, 남은 {len(todo)}")
    for c,mask in enumerate(todo):
        rec=_eval_mask(mask,screen_seeds,ctx)
        with open(sp,"a") as fp: fp.write(json.dumps(rec)+"\n"); done[mask]=rec
        if (c+1)%10==0 or c==len(todo)-1: print(f"  스크린 {c+1}/{len(todo)}  최근 {rec['name'][:34]:34s} S={rec['S']:.4f}")
    # ── 상위 topK + 레퍼런스 선정 ──
    rows=sorted(done.values(),key=lambda r:-r["S"]); top=[r["mask"] for r in rows[:topK]]
    confirm_masks=list(dict.fromkeys(top+list(_REFS.keys())))
    print(f"[확정] 상위{topK}+레퍼런스 = {len(confirm_masks)} 조합 × {confirm_seeds}seed")
    # ── STAGE 2: 확정(topK+refs × confirm_seeds) ──
    cp=f"{_OUT}/confirm.jsonl"; cdone=_done(cp)
    todo2=[mk for mk in confirm_masks if mk not in cdone]
    for c,mask in enumerate(todo2):
        rec=_eval_mask(mask,confirm_seeds,ctx)
        with open(cp,"a") as fp: fp.write(json.dumps(rec)+"\n"); cdone[mask]=rec
        print(f"  확정 {c+1}/{len(todo2)}  {rec['name'][:34]:34s} S={rec['S']:.4f} PREC={rec['PREC']:.3f} SEN={rec['SEN']:.3f} F1={rec['F1']:.3f}")
    print("\n"+"="*60); sweep2_report()
    print("\n자고 일어나서: sweep2_report() 만 불러도 저장된 결과 확인. 끊겼으면 run_sweep2() 다시(이어서).")

def sweep2_report(top=20):
    sp=f"{_OUT}/screen.jsonl"; cp=f"{_OUT}/confirm.jsonl"
    if not os.path.exists(sp) and not os.path.exists(cp):
        print("결과 없음. run_sweep2() 먼저."); return
    if os.path.exists(sp):
        rows=[json.loads(l) for l in open(sp)]; rows.sort(key=lambda r:-r["S"])
        print(f"=== 스크린(4seed) 상위 {top} / 총 {len(rows)} 조합 ===")
        print(f"{'S_PR':>7} {'PREC':>6} {'F1':>6} {'n':>2}  조합")
        for r in rows[:top]: print(f"{r['S']:7.4f} {r['PREC']:6.3f} {r['F1']:6.3f} {r['n']:2d}  {r['name']}")
        print(f"\n--- 군별 평균 S(켜짐 vs 꺼짐) ---")
        for i,fam in enumerate(_TOGGLE):
            on=[r["S"] for r in rows if r["mask"]>>i&1]; off=[r["S"] for r in rows if not(r["mask"]>>i&1)]
            if on and off: print(f"  {fam:8s}: 켜짐 {np.mean(on):.4f}  꺼짐 {np.mean(off):.4f}  Δ{np.mean(on)-np.mean(off):+.4f}")
    if os.path.exists(cp):
        rows=[json.loads(l) for l in open(cp)]; rows.sort(key=lambda r:-r["S"])
        print(f"\n=== 확정(15seed) {len(rows)} 조합 (S_PR 순) ===")
        print(f"{'S_PR':>7} {'PREC':>6} {'SEN':>6} {'F1':>6} {'n':>2}  조합")
        for r in rows: print(f"{r['S']:7.4f} {r['PREC']:6.3f} {r['SEN']:6.3f} {r['F1']:6.3f} {r['n']:2d}  {r['name']}")
        best=rows[0]; print(f"\n▶ 확정 최고: {best['name']}  S={best['S']:.4f} PREC={best['PREC']:.3f} F1={best['F1']:.3f}")
        print(f"  더 단순한 조합이 근접하면(Occam) 그걸 최종 채택 권장.")
