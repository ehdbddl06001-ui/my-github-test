# =============================================================================
#  colab_step44_nsdiscrim.py  —  [STEP 44] N/S 판별 강화 (정밀도=오경보 병목 직공)
#
#  병목: 민감도(SEN)는 높은데 정밀도(PREC)가 낮음 = N을 S로 오경보. Farag PREC 0.827.
#  'Normal을 더 확실히 배우고 S와 가르는' 표현(embedding)수준 개입 4종을 best 위에서 비교:
#   1) base            : 현재 best+DTW_full
#   2) aux (보조헤드)   : 공유 인코더에 N-vs-S 이진 판별 헤드(멀티태스크) → 임베딩을 N/S로 분리
#   3) aux+combine     : 위 + 테스트 S = √(softmax_S · sigmoid_aux)  (두 헤드 합의)
#   4) hardN (경계N채굴): DTW S-N판별로 'S처럼 생긴 N'을 DS1에서 식별→upweight(파라미터-free 식별)
#   5) margin (LDAM)   : 소수 S에 큰 margin 강제(불균형 정석, m_c ∝ 1/n_c^{1/4})
#  전부 15seed 트림, PREC/SEN/F1/PR-AUC 비교 → SEN 안죽이고 PREC↑ 가 승자.
#  S가중치는 STEP42 유효표본수 공식(DS1 클래스수 유래, DS2 튜닝 아님)에서 자동.
#
#  선행 캐시: _WST, _MORPHO, _REPOL, _DTW(15특징 v2)
#  실행:
#    exec(open('/content/drive/MyDrive/mitbih/colab_step44_nsdiscrim.py').read())
#    run_nsdiscrim()            # 느리면 seeds=list(range(1000,1008))
# =============================================================================
import os
import numpy as np
from sklearn.metrics import average_precision_score, precision_recall_curve

_DS1=[101,106,108,109,112,114,115,116,118,119,122,124,201,203,205,207,208,209,215,220,223,230]
_DS2=[100,103,105,111,113,117,121,123,200,202,210,212,213,214,219,221,222,228,231,232,233,234]
_SAVE="/content/drive/MyDrive/mitbih/ablation_step44"; _C={}
_REPOLK_IDX=[0,1,4,5]; _DTW_SN_IDX=[2,5,8,11,14]   # DTW S-N판별(구간별)

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
            s.aux=nn.Linear(192,1)                                   # N-vs-S 보조 판별헤드
        def forward(s,b,r,ft):
            z1=s.e(b); z2=s.e(r); zb=s.sia(torch.cat([z1,z2,z1-z2,(z1-z2).abs()],-1))
            z=z1+torch.sigmoid(s.gate(torch.cat([z1,zb],-1)))*zb
            zp=torch.softmax((z@s.proto.t())*(64**-0.5),-1)@s.proto
            h=torch.cat([z,zp,s.fm(ft)],-1)
            return s.cls(h), s.aux(h).squeeze(-1)                    # (3클래스 logit, N-vs-S logit)
    return Net()

def _f1(y2,s):
    p,r,_=precision_recall_curve((y2==1).astype(int),s); f=2*p*r/(p+r+1e-9); i=int(np.nanargmax(f)); return p[i],r[i],f[i]

def auto_weights(y1, beta=0.9999):
    nN=(y1==0).sum(); nS=max((y1==1).sum(),1)
    eff=lambda n:(1-beta)/(1-beta**n+1e-12); return float(eff(nS)/eff(nN))

def run_nsdiscrim(Kwst=40, Sw=None, seeds=None, lam_aux=0.5):
    import torch, torch.nn as nn, torch.nn.functional as Fn
    from sklearn.preprocessing import RobustScaler
    from sklearn.model_selection import GroupShuffleSplit
    from sklearn.feature_selection import SelectKBest, f_classif
    seeds=seeds or list(range(1000,1015)); dev="cuda" if torch.cuda.is_available() else "cpu"
    d=np.load("/content/drive/MyDrive/mitbih/mamba_data.npz"); beats,feats0,y,pid=d["beat"],d["feats"],d["y"],d["pid"]
    if "ref" not in _C:
        r=np.empty_like(beats)
        for p in np.unique(pid): m=pid==p; r[m]=np.median(beats[m],axis=0,keepdims=True)
        _C["ref"]=r.astype("float32")
    ref=_C["ref"]
    Xw=globals().get("_WST"); Xm=globals().get("_MORPHO"); Xr=globals().get("_REPOL"); Xd=globals().get("_DTW")
    m1=np.isin(pid,_DS1); m2=np.isin(pid,_DS2); y2=y[m2]
    if Sw is None: Sw=auto_weights(y[m1]); print(f"S가중치 자동(유효표본수, DS1유래)= {Sw:.2f}  (DS2 튜닝 아님)")
    Xwk=np.nan_to_num(SelectKBest(f_classif,k=min(Kwst,Xw.shape[1])).fit(np.nan_to_num(Xw[m1]),y[m1]).transform(np.nan_to_num(Xw))).astype("float32")
    F=np.concatenate([feats0,Xwk,Xm,Xr[:,_REPOLK_IDX],Xd],1).astype("float32")     # best + DTW_full
    # --- 경계N(하드N) 가중: DTW S-N판별 평균이 클수록 'S처럼 생긴 N' → DS1-N 내 순위로 1..2배 ---
    sn=np.nan_to_num(Xd[:,_DTW_SN_IDX]).mean(1)                     # 높을수록 S쪽
    hardw=np.ones(len(y),np.float32); dn=m1&(y==0)
    if dn.sum()>1:
        rk=sn[dn].argsort().argsort()/(dn.sum()-1)                 # DS1-N 백분위 순위 0..1
        hw=np.ones(len(y),np.float32); tmp=np.ones(dn.sum(),np.float32)+rk; hw[dn]=tmp
        hardw=hw                                                    # 하드N→~2.0, 나머지 1.0
    # --- LDAM margin: m_c ∝ 1/n_c^{1/4}, 최대margin=0.5 ---
    nc=np.array([ (y[m1]==k).sum() for k in range(3) ],np.float32); mc=1.0/np.power(nc,0.25)
    mc=(mc/mc.max()*0.5).astype("float32")                         # (3,)  최소클래스=0.5
    print(f"base dim={F.shape[1]}, hardN(경계N) upweight max={hardw[m1&(y==0)].max():.2f}, LDAM margins={np.round(mc,3)}")
    def met(p,yy): return (average_precision_score((yy==1).astype(int),p[:,1]),average_precision_score((yy==2).astype(int),p[:,2]))
    @torch.no_grad()
    def pred(M,b,r,ft):
        M.eval(); P=[]; A=[]
        for i in range(0,len(b),4096):
            lo,au=M(torch.from_numpy(b[i:i+4096]).to(dev),torch.from_numpy(r[i:i+4096]).to(dev),torch.from_numpy(ft[i:i+4096]).to(dev))
            P.append(torch.softmax(lo,-1).cpu().numpy()); A.append(torch.sigmoid(au).cpu().numpy())
        return np.concatenate(P), np.concatenate(A)
    def train_one(seed,mode):
        b1,r1,f1a,y1,p1,hw1=beats[m1],ref[m1],F[m1],y[m1],pid[m1],hardw[m1]; b2,r2,f2a=beats[m2],ref[m2],F[m2]
        torch.manual_seed(seed); np.random.seed(seed)
        tr,va=next(GroupShuffleSplit(1,test_size=0.2,random_state=seed).split(f1a,y1,groups=p1))
        sc=RobustScaler().fit(f1a[tr]); f1=np.nan_to_num(sc.transform(f1a),posinf=0,neginf=0).astype("float32"); f2=np.nan_to_num(sc.transform(f2a),posinf=0,neginf=0).astype("float32")
        M=_net(F.shape[1]).to(dev); opt=torch.optim.AdamW(M.parameters(),lr=1e-3,weight_decay=1e-4)
        cw=torch.tensor([1.,Sw,1.5],device=dev); mcv=torch.from_numpy(mc).to(dev)
        ds=torch.utils.data.TensorDataset(*[torch.from_numpy(x) for x in (b1[tr],r1[tr],f1[tr],y1[tr],hw1[tr])])
        dl=torch.utils.data.DataLoader(ds,batch_size=512,shuffle=True); best=-1; bs=None
        for ep in range(15):
            M.train()
            for bb,rr,ff,yy,hh in dl:
                bb,rr,ff,yy,hh=(t.to(dev) for t in (bb,rr,ff,yy,hh)); opt.zero_grad()
                lo,au=M(bb,rr,ff)
                lg=lo.clone()
                if mode=="margin":                                  # 참클래스 logit에서 margin 차감
                    lg=lg-torch.zeros_like(lg).scatter_(1,yy[:,None],mcv[yy][:,None])
                ce=Fn.cross_entropy(lg,yy,reduction="none")
                w=cw[yy]*(hh if mode=="hardN" else 1.0)             # hardN만 경계N 가중
                loss=(ce*w).sum()/w.sum()
                if mode in ("aux","aux+combine"):                   # N/S 보조 BCE(멀티태스크)
                    ns=yy!=2
                    if ns.any(): loss=loss+lam_aux*Fn.binary_cross_entropy_with_logits(au[ns],(yy[ns]==1).float())
                loss.backward(); torch.nn.utils.clip_grad_norm_(M.parameters(),1.0); opt.step()
            Pv,Av=pred(M,b1[va],r1[va],f1[va]); s,v=met(Pv,y1[va])
            if 0.5*(s+v)>best: best=0.5*(s+v); bs={k:v.cpu() for k,v in M.state_dict().items()}
        M.load_state_dict(bs); P2,A2=pred(M,b2,r2,f2)
        if mode=="aux+combine":                                     # 두 헤드 합의(기하평균)로 S점수 교체
            sc2=np.sqrt(np.clip(P2[:,1],0,1)*np.clip(A2,0,1)); P2=P2.copy(); P2[:,1]=sc2
            P2=P2/np.clip(P2.sum(1,keepdims=True),1e-9,None)
        return P2
    def trim(Pn):
        medS=np.median(Pn[:,:,1],0); corr=np.array([np.corrcoef(Pn[i,:,1],medS)[0,1] for i in range(len(Pn))])
        keep=np.argsort(-corr)[:max(1,int(round(len(Pn)*0.8)))]; P=Pn[keep].mean(0); return P/P.sum(1,keepdims=True)
    os.makedirs(_SAVE,exist_ok=True); res={}
    MODES=["base","aux","aux+combine","hardN","margin"]
    print(f"\n{len(seeds)}seed, lam_aux={lam_aux}")
    for mode in MODES:
        Pn=np.stack([train_one(s,mode) for s in seeds],0); np.savez(os.path.join(_SAVE,mode.replace("+","_")+".npz"),P=Pn,y=y2)
        Pt=trim(Pn); S,V=met(Pt,y2); pr,se,f1=_f1(y2,Pt[:,1]); res[mode]=(S,pr,se,f1)
        print(f"  {mode:14s} 트림 S={S:.4f}  PREC={pr:.3f} SEN={se:.3f} F1={f1:.3f}")
    b=res["base"]
    print(f"\n{'='*58}\n▶ base 대비 (정밀도 병목 완화 겨냥):")
    for mode,(S,pr,se,f1) in res.items():
        if mode=="base": continue
        print(f"  {mode:14s}: ΔPREC={pr-b[1]:+.3f}  ΔSEN={se-b[2]:+.3f}  ΔF1={f1-b[3]:+.3f}  ΔS={S-b[0]:+.4f}")
    print(f"\n  ★ SEN 유지하며 PREC↑ = N/S 판별 개선 성공. 승자 위에 2D-DTW 얹어 마무리.")
    return res
