# =============================================================================
#  colab_step53_topauc.py  —  [STEP 53] big-hitter(고AUC) 특징만 골라 빠른 CNN 파악
#
#  전략: 128 조합 대신, 모든 후보 특징군의 단일 판별력이 '특징적으로 큰' 것만 골라 테스트.
#   ① rank_auc(): 후보 전 특징의 단일 AUC 랭킹 (선택은 DS1만=무오염, DS2는 참고표기)
#   ② run_topauc_cnn(thresh): DS1 AUC≥thresh 인 특징만 백본에 얹어 margin CNN 15seed
#      → base / +리듬10(참고) / +TOPAUC(선별) 비교.
#  ⚠️ 단일AUC는 higher-order 시너지를 놓칠 수 있음(약한특징이 조합서 삼) → 빠른 파악용.
#     TOPAUC가 +리듬10보다 낮으면 full sweep으로.
#
#  선행: colab_prep_all.py 실행(synergy_feats/*.npy: 백본+후보군 전부)
#  실행:
#    exec(open('/content/drive/MyDrive/mitbih/colab_step53_topauc.py').read())
#    rank_auc()                       # 먼저 랭킹 보고 thresh 감 잡기(빠름)
#    run_topauc_cnn(thresh=0.62)      # 선별 특징 CNN (Drive 영속)
# =============================================================================
import os, json
import numpy as np
from sklearn.metrics import average_precision_score, precision_recall_curve, roc_auc_score

_BASE="/content/drive/MyDrive/mitbih"; _FEATDIR=f"{_BASE}/synergy_feats"; _OUT=f"{_BASE}/topauc_out"
_DS1=[101,106,108,109,112,114,115,116,118,119,122,124,201,203,205,207,208,209,215,220,223,230]
_DS2=[100,103,105,111,113,117,121,123,200,202,210,212,213,214,219,221,222,228,231,232,233,234]
_BACKBONE=["feats0","WST","MORPHO","REPOL","DTW"]
_CAND=["RHYTHM","NOISE","KOOPMAN","AE","GNN","SEGDEV","VCG"]     # 후보 특징군(고AUC 선별 대상)

def _f1(y2,s):
    p,r,_=precision_recall_curve((y2==1).astype(int),s); f=2*p*r/(p+r+1e-9); i=int(np.nanargmax(f)); return p[i],r[i],f[i]
def auto_weights(y1,beta=0.9999):
    nN=(y1==0).sum(); nS=max((y1==1).sum(),1); eff=lambda n:(1-beta)/(1-beta**n+1e-12); return float(eff(nS)/eff(nN))
def _L(name):
    p=f"{_FEATDIR}/{name}.npy"; return np.load(p) if os.path.exists(p) else None

def _load():
    d=np.load(f"{_BASE}/mamba_data.npz"); beats,y,pid=d["beat"],d["y"],d["pid"]
    BB=[ _L(n) for n in _BACKBONE ]
    if any(b is None for b in BB): raise RuntimeError("백본 캐시 없음 → colab_prep_all.py 먼저")
    back=np.concatenate(BB,1).astype("float32")
    cand={n:_L(n) for n in _CAND if _L(n) is not None}
    return beats,y,pid,back,cand

def rank_auc():
    beats,y,pid,back,cand=_load(); m1=np.isin(pid,_DS1); m2=np.isin(pid,_DS2); y1,y2=y[m1],y[m2]
    print(f"후보군: {list(cand.keys())}\n{'특징':>16} {'DS1_AUC':>8} {'DS2_AUC':>8}   (선택은 DS1만)")
    rows=[]
    for fam,mat in cand.items():
        for k in range(mat.shape[1]):
            c1=mat[m1,k]; c2=mat[m2,k]
            if np.std(c1)<1e-9: continue
            a1=roc_auc_score((y1==1).astype(int),c1); a1=max(a1,1-a1)
            a2=roc_auc_score((y2==1).astype(int),c2); a2=max(a2,1-a2)
            rows.append((f"{fam}[{k}]",a1,a2,fam,k))
    for nm,a1,a2,fam,k in sorted(rows,key=lambda r:-r[1]):
        bar="█"*int((a1-0.5)*40); print(f"{nm:>16} {a1:8.3f} {a2:8.3f}   {bar}")
    print("\n  ▶ DS1_AUC 큰 것부터 = big hitter. run_topauc_cnn(thresh=?) 로 임계 골라 테스트.")
    return rows

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
    medS=np.median(Pn[:,:,1],0); corr=np.array([np.corrcoef(Pn[i,:,1],medS)[0,1] for i in range(len(Pn))])
    keep=np.argsort(-corr)[:max(1,int(round(len(Pn)*0.8)))]; P=Pn[keep].mean(0); return P/P.sum(1,keepdims=True)

def run_topauc_cnn(thresh=0.62, seeds=None):
    seeds=seeds or list(range(2000,2015)); os.makedirs(_OUT,exist_ok=True)
    beats,y,pid,back,cand=_load(); ref=np.empty_like(beats)
    for p in np.unique(pid): m=pid==p; ref[m]=np.median(beats[m],0,keepdims=True)
    ref=ref.astype("float32"); m1=np.isin(pid,_DS1); m2=np.isin(pid,_DS2); y1,y2=y[m1],y[m2]
    # DS1 AUC로 big-hitter 선별(무오염)
    sel=[]; selnames=[]
    for fam,mat in cand.items():
        for k in range(mat.shape[1]):
            c1=mat[m1,k]
            if np.std(c1)<1e-9: continue
            a1=roc_auc_score((y1==1).astype(int),c1); a1=max(a1,1-a1)
            if a1>=thresh: sel.append(mat[:,[k]]); selnames.append(f"{fam}[{k}]({a1:.2f})")
    TOP=np.concatenate(sel,1).astype("float32") if sel else np.zeros((len(y),0),"float32")
    rhy=cand.get("RHYTHM")
    print(f"DS1_AUC≥{thresh} 선별 {len(selnames)}개: {selnames}")
    Sw=auto_weights(y1); nc=np.array([(y1==k).sum() for k in range(3)],np.float32); mc=(1.0/np.power(nc,0.25)); mc=(mc/mc.max()*0.5).astype("float32")
    CFG={"base":back}
    if rhy is not None: CFG["+리듬10(참고)"]=np.concatenate([back,rhy],1).astype("float32")
    if TOP.shape[1]>0: CFG[f"+TOPAUC({len(selnames)})"]=np.concatenate([back,TOP],1).astype("float32")
    def met(p,yy): return (average_precision_score((yy==1).astype(int),p[:,1]),average_precision_score((yy==2).astype(int),p[:,2]))
    sumpath=f"{_OUT}/summary.jsonl"; done={}
    if os.path.exists(sumpath):
        for ln in open(sumpath):
            try: r=json.loads(ln); done[r["tag"]]=r
            except: pass
    print(f"margin CNN {len(seeds)}seed, Sw={Sw:.1f}")
    for tag,F in CFG.items():
        if tag in done: r=done[tag]; print(f"  {tag:16s} S={r['S']:.4f} PREC={r['PREC']:.3f} SEN={r['SEN']:.3f} F1={r['F1']:.3f} (캐시)"); continue
        preds=[]
        for s in seeds:
            sp=f"{_OUT}/{tag.replace('/','_')}_s{s}.npy"
            if os.path.exists(sp): preds.append(np.load(sp)); continue
            P=_train_seed(F,beats,ref,y,pid,mc,Sw,s); np.save(sp,P.astype("float32")); preds.append(P)
        Pt=_trim(np.stack(preds,0)); S,V=met(Pt,y2); pr,se,f1=_f1(y2,Pt[:,1])
        rec={"tag":tag,"S":float(S),"PREC":float(pr),"SEN":float(se),"F1":float(f1)}
        with open(sumpath,"a") as fp: fp.write(json.dumps(rec)+"\n"); done[tag]=rec
        print(f"  {tag:16s} S={S:.4f} PREC={pr:.3f} SEN={se:.3f} F1={f1:.3f}")
    print(f"\n  ★ +TOPAUC ≥ +리듬10 이면 = big-hitter 선별로 충분(빠른길). 낮으면 = 조합시너지 놓침 → full sweep.")
    return done
