# =============================================================================
#  colab_step27_mfconv.py  —  [STEP 27] Farag식 매치드필터 conv (동결 표현) 하이브리드
#
#  F1 분해: 우리 약점은 정밀도(0.64 vs Farag 0.83), 민감도는 비슷(0.75 vs 0.82).
#  = 오경보(N/V를 S로) 과다. 매치드필터 = "S 템플릿과 실제론 안 닮음"을 기각 → 정밀도↑.
#  step17(스칼라 최대상관=WST와 중복→실패)와 달리, Farag처럼 CNN 내부 '동결 conv층'으로:
#   DS1 클래스 템플릿(kmeans)을 conv 커널로 초기화·동결 → 비트 전체에 슬라이딩 상관 '지도'
#   → BatchNorm 재보정(비학습=일반화 교훈) → 작은 학습 conv → 우리 최고모델에 가지로 결합.
#
#  검증: best(26+WST+morpho+repolK) vs best+MFconv, 15seed paired + 트림.
#        정밀도가 목표라 PR-AUC + best-F1(PREC/SEN/F1) 둘 다 보고.
#  선행 로드: step12(_WST)·step15(extract_morpho)·step18(extract_repol)
#  실행:
#    exec(open('/content/drive/MyDrive/mitbih/colab_step27_mfconv.py').read())
#    run_mf(Kwst=40)
# =============================================================================
import os
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import average_precision_score, precision_recall_curve

_DS1=[101,106,108,109,112,114,115,116,118,119,122,124,201,203,205,207,208,209,215,220,223,230]
_DS2=[100,103,105,111,113,117,121,123,200,202,210,212,213,214,219,221,222,228,231,232,233,234]
_SAVE="/content/drive/MyDrive/mitbih/ablation_step27"; _C={}
_REPOLK_IDX=[0,1,4,5]

def build_mf_templates(beats, y, mask, W=64, K=8):
    """DS1(mask)에서 클래스별 K개 매치드필터 템플릿 (R정렬 윈도, 2리드, 단위정규화)."""
    L=beats.shape[2]; VM=np.sqrt(beats[:,0]**2+beats[:,1]**2); R=VM.argmax(1); half=W//2
    idxs=np.where(mask)[0]; Wa=np.zeros((len(idxs),2,W),np.float32)
    for j,i in enumerate(idxs):
        s=int(np.clip(R[i]-half,0,L-W)); Wa[j]=beats[i,:,s:s+W]
    flat=Wa.reshape(len(idxs),-1); flat=flat/(np.linalg.norm(flat,axis=1,keepdims=True)+1e-6)
    Wa=flat.reshape(-1,2,W); yy=y[idxs]; T=[]
    for c in [0,1,2]:
        sub=Wa[yy==c]; k=min(K,max(1,len(sub)//50))
        C=KMeans(k,n_init=4,random_state=0).fit(sub.reshape(len(sub),-1)).cluster_centers_.reshape(k,2,W)
        C=C/(np.linalg.norm(C.reshape(k,-1),axis=1,keepdims=True).reshape(k,1,1)+1e-6)
        T.append(C.astype("float32"))
    return np.concatenate(T,0).astype("float32")           # (nT,2,W)

def _net(fdim, templates=None):
    import torch, torch.nn as nn
    nT=0 if templates is None else templates.shape[0]; W=0 if templates is None else templates.shape[2]
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
            s.use_mf=nT>0; extra=0
            if s.use_mf:
                s.mf=nn.Conv1d(2,nT,W,padding=W//2,bias=False)                 # 매치드필터 = 동결 conv
                s.mf.weight.data=torch.from_numpy(templates); s.mf.weight.requires_grad=False
                s.mfbn=nn.BatchNorm1d(nT)                                       # BN 재보정(일반화)
                s.mfhead=nn.Sequential(nn.Conv1d(nT,32,5,padding=2),nn.BatchNorm1d(32),nn.ReLU(),nn.AdaptiveAvgPool1d(1))
                extra=32
            s.cls=nn.Sequential(nn.Linear(192+extra,64),nn.ReLU(),nn.Linear(64,3))
        def forward(s,b,r,ft):
            z1=s.e(b); z2=s.e(r); zb=s.sia(torch.cat([z1,z2,z1-z2,(z1-z2).abs()],-1))
            z=z1+torch.sigmoid(s.gate(torch.cat([z1,zb],-1)))*zb
            zp=torch.softmax((z@s.proto.t())*(64**-0.5),-1)@s.proto
            parts=[z,zp,s.fm(ft)]
            if s.use_mf:
                m=torch.relu(s.mfbn(s.mf(b))); parts.append(s.mfhead(m).squeeze(-1))
            return s.cls(torch.cat(parts,-1))
    return Net()

def _f1(y2,s):
    p,r,_=precision_recall_curve((y2==1).astype(int),s); f=2*p*r/(p+r+1e-9); i=int(np.nanargmax(f))
    return p[i],r[i],f[i]

def run_mf(Kwst=40, W=64, K=8, seeds=None):
    import torch, torch.nn as nn
    from sklearn.preprocessing import RobustScaler
    from sklearn.model_selection import GroupShuffleSplit
    from sklearn.feature_selection import SelectKBest, f_classif
    seeds=seeds or list(range(1000,1015)); dev="cuda" if torch.cuda.is_available() else "cpu"
    d=np.load("/content/drive/MyDrive/mitbih/mamba_data.npz")
    beats,feats0,y,pid=d["beat"],d["feats"],d["y"],d["pid"]
    if "ref" not in _C:
        r=np.empty_like(beats)
        for p in np.unique(pid): m=pid==p; r[m]=np.median(beats[m],axis=0,keepdims=True)
        _C["ref"]=r.astype("float32")
    ref=_C["ref"]
    Xw=globals().get("_WST",None); Xw=Xw if Xw is not None else compute_wst_features(beats)
    Xm=globals().get("_MORPHO",None); Xm=Xm if Xm is not None else extract_morpho_features(beats,ref,pid)
    Xr=globals().get("_REPOL",None); Xr=Xr if Xr is not None else extract_repol_features(beats,ref,pid)
    m1=np.isin(pid,_DS1); m2=np.isin(pid,_DS2); y2=y[m2]
    Xwk=np.nan_to_num(SelectKBest(f_classif,k=min(Kwst,Xw.shape[1])).fit(np.nan_to_num(Xw[m1]),y[m1]).transform(np.nan_to_num(Xw))).astype("float32")
    F=np.concatenate([feats0,Xwk,Xm,Xr[:,_REPOLK_IDX]],1).astype("float32")     # best 특징(동일)
    TMPL=build_mf_templates(beats,y,m1,W,K)                                      # 템플릿=DS1만(라벨 정당)
    print(f"best dim={F.shape[1]}  /  매치드필터 템플릿 {TMPL.shape[0]}개 (클래스별 K={K}, W={W})")
    def met(p,yy): return (average_precision_score((yy==1).astype(int),p[:,1]),average_precision_score((yy==2).astype(int),p[:,2]))
    @torch.no_grad()
    def pred(M,b,r,ft):
        M.eval(); o=[]
        for i in range(0,len(b),4096):
            o.append(torch.softmax(M(torch.from_numpy(b[i:i+4096]).to(dev),torch.from_numpy(r[i:i+4096]).to(dev),torch.from_numpy(ft[i:i+4096]).to(dev)),-1).cpu().numpy())
        return np.concatenate(o)
    def train_one(templates,seed):
        b1,r1,f1a,y1,p1=beats[m1],ref[m1],F[m1],y[m1],pid[m1]; b2,r2,f2a=beats[m2],ref[m2],F[m2]
        torch.manual_seed(seed); np.random.seed(seed)
        tr,va=next(GroupShuffleSplit(1,test_size=0.2,random_state=seed).split(f1a,y1,groups=p1))
        sc=RobustScaler().fit(f1a[tr]); f1=np.nan_to_num(sc.transform(f1a),posinf=0,neginf=0).astype("float32"); f2=np.nan_to_num(sc.transform(f2a),posinf=0,neginf=0).astype("float32")
        M=_net(F.shape[1],templates).to(dev)
        opt=torch.optim.AdamW([p for p in M.parameters() if p.requires_grad],lr=1e-3,weight_decay=1e-4)
        lf=nn.CrossEntropyLoss(weight=torch.tensor([1.,3.,1.5],device=dev))
        ds=torch.utils.data.TensorDataset(*[torch.from_numpy(x) for x in (b1[tr],r1[tr],f1[tr],y1[tr])]); dl=torch.utils.data.DataLoader(ds,batch_size=512,shuffle=True); best=-1; bs=None
        for ep in range(15):
            M.train()
            for bb,rr,ff,yy in dl:
                bb,rr,ff,yy=(t.to(dev) for t in (bb,rr,ff,yy)); opt.zero_grad()
                loss=lf(M(bb,rr,ff),yy); loss.backward(); torch.nn.utils.clip_grad_norm_(M.parameters(),1.0); opt.step()
            pv=pred(M,b1[va],r1[va],f1[va]); s,v=met(pv,y1[va])
            if 0.5*(s+v)>best: best=0.5*(s+v); bs={k:v.cpu() for k,v in M.state_dict().items()}
        M.load_state_dict(bs); return pred(M,b2,r2,f2)
    def trim(Pn):
        medS=np.median(Pn[:,:,1],0); corr=np.array([np.corrcoef(Pn[i,:,1],medS)[0,1] for i in range(len(Pn))])
        keep=np.argsort(-corr)[:max(1,int(round(len(Pn)*0.8)))]; P=Pn[keep].mean(0); return P/P.sum(1,keepdims=True)
    R={"no":[],"mf":[]}
    for seed in seeds:
        R["no"].append(train_one(None,seed)); R["mf"].append(train_one(TMPL,seed))
        print(f"  seed {seed}:  best S={met(R['no'][-1],y2)[0]:.4f}   +MFconv S={met(R['mf'][-1],y2)[0]:.4f}")
    os.makedirs(_SAVE,exist_ok=True)
    print(f"\n{'='*56}")
    for tag,nm in [("no","best        "),("mf","best+MFconv ")]:
        Pn=np.stack(R[tag],0); np.savez(os.path.join(_SAVE,f"{tag}.npz"),P=Pn,y=y2,pid=pid[m2])
        Pt=trim(Pn); S,V=met(Pt,y2); pr,se,f1=_f1(y2,Pt[:,1])
        print(f"[{nm}] 트림  S_PR-AUC={S:.4f}  V={V:.4f}   |  best-F1: PREC={pr:.3f} SEN={se:.3f} F1={f1:.3f}")
    print(f"\n▶ +MFconv 가 PREC(정밀도)·F1을 올리면 = Farag 기법이 우리 약점(오경보) 교정 성공.")
    print(f"  Farag 기준 PREC 0.827/SEN 0.816/F1 0.82.  우리 시작점 PREC 0.642/SEN 0.750/F1 0.692.")
    return R
