# =============================================================================
#  colab_step23_moe.py  —  [STEP 23] 다축 전문가 + 축별 게이트 + 조합 탐색(비누출)
#
#  사장님 그림: 축(RR·WST·morpho·T파…)마다 개별 게이트 Fn을 만들고, 비트별로 각 축을
#  얼마나 쓸지 판단. '다 합친 게 최고'가 아닐 수 있으니 서로 다른 Fn 조합을 비교해
#  DS1에서 정답률 최고 조합을 찾아 그 조합만 DS2에 채용.
#
#  전문가(축) 4:  base=26(RR·간격) / +WST / +morpho / +repol(RT중심·T비대칭)
#  게이트 g: 비트 형태특징(morpho+repol) → 포함된 전문가들에 softmax 가중(비트별).
#            최종 = Σ w_k(beat)·E_k.  DS1 OOF(전문가가 안 본 비트)로 학습.
#  조합 탐색: 15개 부분집합 각각 게이트 씌워 ★DS1 held-out★ S로 채점 → 최고 조합 선택
#            → DS2 적용.  (DS2로 고르면 누출 → DS2는 평가만.  DS2-oracle은 상한 참고.)
#
#  선행(캐시): _WST, extract_morpho_features, extract_repol_features/_REPOL
#  실행:
#    exec(open('/content/drive/MyDrive/mitbih/colab_step23_moe.py').read())
#    run_moe(Kwst=40)         # 느리면 nseed_full=1
# =============================================================================
import os
import numpy as np
from itertools import combinations
from sklearn.metrics import average_precision_score

_DS1=[101,106,108,109,112,114,115,116,118,119,122,124,201,203,205,207,208,209,215,220,223,230]
_DS2=[100,103,105,111,113,117,121,123,200,202,210,212,213,214,219,221,222,228,231,232,233,234]
_SAVE="/content/drive/MyDrive/mitbih/ablation_step23"; _C={}
_REPOLK_IDX=[0,1,4,5]

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

def run_moe(Kwst=40, nseed_oof=1, nseed_full=2, seed0=1000):
    import torch, torch.nn as nn, torch.nn.functional as Fn
    from sklearn.preprocessing import RobustScaler
    from sklearn.model_selection import GroupShuffleSplit, GroupKFold
    from sklearn.feature_selection import SelectKBest, f_classif
    dev="cuda" if torch.cuda.is_available() else "cpu"
    d=np.load("/content/drive/MyDrive/mitbih/mamba_data.npz")
    beats,feats0,y,pid=d["beat"],d["feats"],d["y"],d["pid"]
    if "ref" not in _C:
        r=np.empty_like(beats)
        for p in np.unique(pid):
            m=pid==p; r[m]=np.median(beats[m],axis=0,keepdims=True)
        _C["ref"]=r.astype("float32")
    ref=_C["ref"]
    Xw=globals().get("_WST",None); Xw=Xw if Xw is not None else compute_wst_features(beats)
    Xm=globals().get("_MORPHO",None); Xm=Xm if Xm is not None else extract_morpho_features(beats,ref,pid)
    Xr=globals().get("_REPOL",None); Xr=Xr if Xr is not None else extract_repol_features(beats,ref,pid)
    m1=np.isin(pid,_DS1); m2=np.isin(pid,_DS2)
    Xwk=np.nan_to_num(SelectKBest(f_classif,k=min(Kwst,Xw.shape[1])).fit(np.nan_to_num(Xw[m1]),y[m1]).transform(np.nan_to_num(Xw))).astype("float32")
    # ── 축별 전문가(각각 26에 한 축씩) ──
    EXPERTS={"base":feats0.astype("float32"),
             "wst":np.concatenate([feats0,Xwk],1).astype("float32"),
             "morph":np.concatenate([feats0,Xm],1).astype("float32"),
             "repol":np.concatenate([feats0,Xr[:,_REPOLK_IDX]],1).astype("float32")}
    names=list(EXPERTS)
    y1,p1=y[m1],pid[m1]; y2=y[m2]; b1,r1,b2,r2=beats[m1],ref[m1],beats[m2],ref[m2]; N1=int(m1.sum())
    def met(p,yy): return (average_precision_score((yy==1).astype(int),p[:,1]),average_precision_score((yy==2).astype(int),p[:,2]))
    @torch.no_grad()
    def _pred(M,sc,b,r,Fraw):
        f=np.nan_to_num(sc.transform(Fraw),posinf=0,neginf=0).astype("float32"); M.eval(); o=[]
        for i in range(0,len(b),4096):
            o.append(torch.softmax(M(torch.from_numpy(b[i:i+4096]).to(dev),torch.from_numpy(r[i:i+4096]).to(dev),torch.from_numpy(f[i:i+4096]).to(dev)),-1).cpu().numpy())
        return np.concatenate(o)
    def fit_expert(Fd1, tr_local, seed):
        torch.manual_seed(seed); np.random.seed(seed)
        a,vb=next(GroupShuffleSplit(1,test_size=0.2,random_state=seed).split(Fd1[tr_local],y1[tr_local],groups=p1[tr_local]))
        tr=tr_local[a]; va=tr_local[vb]
        sc=RobustScaler().fit(Fd1[tr]); f=np.nan_to_num(sc.transform(Fd1),posinf=0,neginf=0).astype("float32")
        M=_net(Fd1.shape[1]).to(dev); opt=torch.optim.AdamW(M.parameters(),lr=1e-3,weight_decay=1e-4)
        lf=nn.CrossEntropyLoss(weight=torch.tensor([1.,3.,1.5],device=dev))
        ds=torch.utils.data.TensorDataset(*[torch.from_numpy(x) for x in (b1[tr],r1[tr],f[tr],y1[tr])])
        dl=torch.utils.data.DataLoader(ds,batch_size=512,shuffle=True); best=-1; bs=None
        for ep in range(15):
            M.train()
            for bb,rr,ff,yy in dl:
                bb,rr,ff,yy=(t.to(dev) for t in (bb,rr,ff,yy)); opt.zero_grad()
                loss=lf(M(bb,rr,ff),yy); loss.backward(); torch.nn.utils.clip_grad_norm_(M.parameters(),1.0); opt.step()
            pv=_pred(M,sc,b1[va],r1[va],Fd1[va]); s,v=met(pv,y1[va])
            if 0.5*(s+v)>best: best=0.5*(s+v); bs={k:v.cpu() for k,v in M.state_dict().items()}
        M.load_state_dict(bs); return M,sc
    # ── 전문가별 OOF(게이트/선택용) + 전체DS1→DS2 ──
    oof={}; ds2={}; gkf=GroupKFold(2)
    for ei,nm in enumerate(names):
        Fd1=EXPERTS[nm][m1]; Fd2=EXPERTS[nm][m2]; oo=np.zeros((N1,3),np.float32)
        for fa,fb in gkf.split(Fd1,y1,p1):
            acc=np.zeros((len(fb),3),np.float32)
            for s in range(nseed_oof):
                M,sc=fit_expert(Fd1,fa,seed0+ei*10+s); acc+=_pred(M,sc,b1[fb],r1[fb],Fd1[fb])
            oo[fb]=acc/nseed_oof
        acc=np.zeros((int(m2.sum()),3),np.float32)
        for s in range(nseed_full):
            M,sc=fit_expert(Fd1,np.arange(N1),seed0+ei*10+100+s); acc+=_pred(M,sc,b2,r2,Fd2)
        oof[nm]=oo; ds2[nm]=acc/nseed_full
        print(f"  expert {nm:6s}: OOF S={met(oo,y1)[0]:.3f}  DS2 S={met(ds2[nm],y2)[0]:.3f}")
    os.makedirs(_SAVE,exist_ok=True)
    np.savez(os.path.join(_SAVE,"experts.npz"),**{f"oof_{n}":oof[n] for n in names},**{f"ds2_{n}":ds2[n] for n in names},y1=y1,y2=y2,p1=p1)
    # ── 게이트: 형태특징 → 포함 전문가 softmax 가중 (비트별) ──
    G=np.concatenate([Xm,Xr],1).astype("float32"); scg=RobustScaler().fit(np.nan_to_num(G[m1]))
    g1=torch.from_numpy(np.nan_to_num(scg.transform(np.nan_to_num(G[m1])),posinf=0,neginf=0).astype("float32")).to(dev)
    g2=torch.from_numpy(np.nan_to_num(scg.transform(np.nan_to_num(G[m2])),posinf=0,neginf=0).astype("float32")).to(dev)
    yt=torch.from_numpy(y1.astype("int64")).to(dev); wcls=torch.tensor([1.,3.,1.5],device=dev)
    OOF={n:torch.from_numpy(oof[n]).to(dev) for n in names}; DS2={n:torch.from_numpy(ds2[n]).to(dev) for n in names}
    def fit_gate(sub, idx, iters=400, seed=0):
        torch.manual_seed(seed)
        gate=nn.Sequential(nn.Linear(G.shape[1],32),nn.ReLU(),nn.Linear(32,len(sub))).to(dev)
        opt=torch.optim.Adam(gate.parameters(),lr=3e-3,weight_decay=1e-3)
        Ps=torch.stack([OOF[n] for n in sub],1)            # (N1,K,3)
        gi=g1[idx]; Pi=Ps[idx]; yi=yt[idx]
        for it in range(iters):
            w=torch.softmax(gate(gi),-1)                    # (n,K)
            final=(w[:,:,None]*Pi).sum(1)
            loss=Fn.nll_loss(torch.log(final.clamp_min(1e-6)),yi,weight=wcls)
            opt.zero_grad(); loss.backward(); opt.step()
        return gate
    @torch.no_grad()
    def gate_apply(gate, sub, gfeat, PRED):
        w=torch.softmax(gate(gfeat),-1); Ps=torch.stack([PRED[n] for n in sub],1)
        return (w[:,:,None]*Ps).sum(1).cpu().numpy()
    # ── 조합 탐색: DS1 held-out(환자분리)로 채점 → 최고 선택 ──
    gss=GroupShuffleSplit(1,test_size=0.25,random_state=42); gtr,gva=next(gss.split(g1.cpu(),y1,groups=p1))
    subs=[c for k in range(1,len(names)+1) for c in combinations(names,k)]
    print(f"\n조합 탐색: {len(subs)}개 (DS1 held-out {len(gva)}비트로 채점)")
    sel=[]
    for sub in subs:
        gate=fit_gate(sub,gtr,iters=300)
        val=gate_apply(gate,sub,g1[gva],{n:OOF[n][torch.from_numpy(gva).to(dev)] for n in sub})
        sel.append((sub,met(val,y1[gva])[0]))
    sel.sort(key=lambda x:-x[1])
    print("  DS1 held-out S 상위 6:")
    for sub,s in sel[:6]: print(f"    {'+'.join(sub):22s}  DS1val S={s:.4f}")
    best_sub=sel[0][0]
    # ── 최고 조합 게이트를 전체 DS1로 재학습 → DS2 적용 ──
    gate=fit_gate(best_sub,np.arange(N1),iters=500)
    gated2=gate_apply(gate,best_sub,g2,DS2)
    with torch.no_grad(): w2=torch.softmax(gate(g2),-1).cpu().numpy()
    np.savez(os.path.join(_SAVE,"gate.npz"),best_sub=list(best_sub),w2=w2,gated2=gated2,y2=y2,pid2=pid[m2])
    # ── 참고선들 ──
    def norm(P): return P/P.sum(-1,keepdims=True)
    full=gate_apply(fit_gate(tuple(names),np.arange(N1),iters=500),tuple(names),g2,DS2)   # 전축 MoE
    uni=norm(sum(ds2[n] for n in names)/len(names))                                       # 균일 평균
    # DS2-oracle 조합(누출 상한, 참고): 각 조합 전체DS1 게이트 → DS2 S 최댓값
    orc=("",-1)
    for sub in subs:
        gp=gate_apply(fit_gate(sub,np.arange(N1),iters=300),sub,g2,DS2); s=met(gp,y2)[0]
        if s>orc[1]: orc=('+'.join(sub),s)
    print(f"\n{'='*60}\n[DS2 결과]  (조합 선택은 DS1만, DS2는 평가만)")
    for n in names: print(f"  단일 {n:6s}         S={met(ds2[n],y2)[0]:.4f}")
    print(f"  균일평균(4축)        S={met(uni,y2)[0]:.4f}")
    print(f"  전축 MoE(게이트)     S={met(full,y2)[0]:.4f}")
    print(f"  ★DS1선택 조합[{'+'.join(best_sub)}] S={met(gated2,y2)[0]:.4f}")
    print(f"\n  S비트 게이트가중 평균: "+", ".join(f"{n}={w2[y2==1,i].mean():.2f}" for i,n in enumerate(best_sub)))
    print(f"  [참고·누출상한] DS2-oracle 조합[{orc[0]}] S={orc[1]:.4f}")
    print(f"\n▶ DS1선택 조합이 단일최고·균일보다 높으면 = 축별 게이트+조합선택 성립(사장님 구조).")
    print(f"  DS2-oracle과 큰 차 없으면 선택이 견고. 차가 크면 선택이 DS1서 최적조합을 못 집음.")
    return dict(best_sub=best_sub,gated2=gated2,w2=w2,oof=oof,ds2=ds2)
