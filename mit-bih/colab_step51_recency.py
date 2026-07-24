# =============================================================================
#  colab_step51_recency.py  —  [STEP 51] recency(α) 스윕 — "최근에 가중치↑ → 정확도↑?" 직접검증
#
#  사장님 직관: 변화(최근사건)에 가중치를 더 주면 정확도가 오를 것. 우리 리듬/노이즈
#  innovation의 예측기(EWMA)는 pred_t=α·x_{t-1}+(1-α)·pred_{t-1} → α가 recency 세기.
#  지금 α=0.3 고정. 이를 스윕해 '최근 가중 세기'의 최적점을 실제 margin CNN으로 찾는다.
#  (Weighted Conformal은 보정/기권층이라 AUC 안 올림 → 정확도 레버는 이 α 튜닝이 맞음.)
#   · α↑(0.5~0.7): 최근 리듬 민감(드리프트 추적↑, 노이즈↑)  · α↓(0.1~0.2): 안정, 적응 느림
#  base+리듬10(α)로 α별 비교. Drive 영속(α·seed마다 저장)·재개가능.
#
#  선행: _WST,_MORPHO,_REPOL,_DTW (recover) + step49(extract_rhythm_v2) Drive
#  실행:
#    exec(open('/content/drive/MyDrive/mitbih/colab_step51_recency.py').read())
#    run_recency()            # α 스윕(재개가능). 재시작 후 같은 줄 다시 → 이어서
#    recency_report()         # 저장된 결과만 보기
# =============================================================================
import os, json
import numpy as np
from sklearn.metrics import average_precision_score, precision_recall_curve
from sklearn.feature_selection import SelectKBest, f_classif

_BASE="/content/drive/MyDrive/mitbih"; _OUT=f"{_BASE}/recency_out"
_DS1=[101,106,108,109,112,114,115,116,118,119,122,124,201,203,205,207,208,209,215,220,223,230]
_DS2=[100,103,105,111,113,117,121,123,200,202,210,212,213,214,219,221,222,228,231,232,233,234]
_REPOLK_IDX=[0,1,4,5]; _ALPHAS=[0.1,0.2,0.3,0.5,0.7]

def _f1(y2,s):
    p,r,_=precision_recall_curve((y2==1).astype(int),s); f=2*p*r/(p+r+1e-9); i=int(np.nanargmax(f)); return p[i],r[i],f[i]
def auto_weights(y1,beta=0.9999):
    nN=(y1==0).sum(); nS=max((y1==1).sum(),1); eff=lambda n:(1-beta)/(1-beta**n+1e-12); return float(eff(nS)/eff(nN))

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

def _bestF():
    d=np.load(f"{_BASE}/mamba_data.npz"); beats,feats0,y,pid=d["beat"],d["feats"],d["y"],d["pid"]; m1=np.isin(pid,_DS1)
    Xw=globals().get("_WST"); Xm=globals().get("_MORPHO"); Xr=globals().get("_REPOL"); Xd=globals().get("_DTW")
    Xwk=np.nan_to_num(SelectKBest(f_classif,k=min(40,Xw.shape[1])).fit(np.nan_to_num(Xw[m1]),y[m1]).transform(np.nan_to_num(Xw)))
    BEST=np.concatenate([feats0,Xwk,Xm,Xr[:,_REPOLK_IDX],Xd],1).astype("float32")
    return beats,feats0,y,pid,BEST

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
    medS=np.median(Pn[:,:,1],0); corr=np.array([np.corrcoef(Pn[i,:,1],medS)[0,1] for i in range(len(Pn))])
    keep=np.argsort(-corr)[:max(1,int(round(len(Pn)*0.8)))]; P=Pn[keep].mean(0); return P/P.sum(1,keepdims=True)

def run_recency(alphas=None, seeds=None):
    alphas=alphas or _ALPHAS; seeds=seeds or list(range(1000,1010)); os.makedirs(_OUT,exist_ok=True)
    if "extract_rhythm_v2" not in globals(): exec(open(f"{_BASE}/colab_step49_rhythm2.py").read(), globals())
    beats,feats0,y,pid,BEST=_bestF(); ref=np.empty_like(beats)
    for p in np.unique(pid): m=pid==p; ref[m]=np.median(beats[m],0,keepdims=True)
    ref=ref.astype("float32")
    m1=np.isin(pid,_DS1); m2=np.isin(pid,_DS2); y2=y[m2]
    Sw=auto_weights(y[m1]); nc=np.array([(y[m1]==k).sum() for k in range(3)],np.float32); mc=(1.0/np.power(nc,0.25)); mc=(mc/mc.max()*0.5).astype("float32")
    sumpath=f"{_OUT}/summary.jsonl"; done={}
    if os.path.exists(sumpath):
        for ln in open(sumpath):
            try: r=json.loads(ln); done[r["tag"]]=r
            except: pass
    print(f"recency(α) 스윕 {alphas}, {len(seeds)}seed, Sw={Sw:.1f}")
    def run_cfg(tag, F):
        if tag in done: print(f"  {tag} 이미 완료(스킵)"); return done[tag]
        preds=[]
        for seed in seeds:
            sp=f"{_OUT}/{tag}_s{seed}.npy"
            if os.path.exists(sp): preds.append(np.load(sp)); continue
            P=_train_seed(F,beats,ref,y,pid,mc,Sw,seed); np.save(sp,P.astype("float32")); preds.append(P)
        Pt=_trim(np.stack(preds,0)); S=average_precision_score((y2==1).astype(int),Pt[:,1])
        Vv=average_precision_score((y2==2).astype(int),Pt[:,2]); pr,se,f1=_f1(y2,Pt[:,1])
        rec={"tag":tag,"S":float(S),"PREC":float(pr),"SEN":float(se),"F1":float(f1),"V":float(Vv)}
        with open(sumpath,"a") as fp: fp.write(json.dumps(rec)+"\n"); done[tag]=rec
        print(f"  {tag:16s} S={S:.4f} PREC={pr:.3f} SEN={se:.3f} F1={f1:.3f}"); return rec
    run_cfg("base(α무관)", BEST)                                  # recency 무관 기준
    for a in alphas:
        R=globals()["extract_rhythm_v2"](beats,feats0,pid,y,alpha=a,verbose=False)
        run_cfg(f"α={a}", np.concatenate([BEST,R],1).astype("float32"))
    recency_report()

def recency_report():
    sumpath=f"{_OUT}/summary.jsonl"
    if not os.path.exists(sumpath): print("결과 없음. run_recency() 먼저."); return
    rows=[json.loads(l) for l in open(sumpath)]
    base=next((r for r in rows if r["tag"].startswith("base")),None)
    ar=[r for r in rows if r["tag"].startswith("α")]; ar.sort(key=lambda r:-r["S"])
    print(f"\n=== recency(α) 스윕 결과 (S_PR 순) ===")
    print(f"{'설정':>12} {'S_PR':>7} {'PREC':>6} {'SEN':>6} {'F1':>6}")
    if base: print(f"{base['tag']:>12} {base['S']:7.4f} {base['PREC']:6.3f} {base['SEN']:6.3f} {base['F1']:6.3f}")
    for r in ar: print(f"{r['tag']:>12} {r['S']:7.4f} {r['PREC']:6.3f} {r['SEN']:6.3f} {r['F1']:6.3f}")
    if ar:
        best=ar[0]; print(f"\n▶ 최적 recency = {best['tag']} (S={best['S']:.4f}, PREC={best['PREC']:.3f})")
        print(f"  현재고정 α=0.3 대비 더 좋으면 → '최근 가중↑ 정확도↑' 사장님 가설 성립, 그 α 채택.")
