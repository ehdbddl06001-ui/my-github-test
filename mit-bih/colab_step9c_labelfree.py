# =============================================================================
#  colab_step9c_labelfree.py  —  P파 증분이 'label-free'로도 살아남나
#
#  step9b: 26+P파8 이 S를 +0.204 올림(0.267→0.472). 단 P파는 ref(정상비트 라벨로
#  만든 정상템플릿) 기준 → DS2 정상라벨 누출. V까지 +0.26 뛴 게 의심 정황.
#
#  검증: 정상 기준을 3가지로 바꿔 증분을 비교 —
#    (a) 정상템플릿 ref   : 누출(상한)
#    (b) 전체 median ref  : label-free (라벨 전혀 안 씀, 이상비트 섞임)
#    (c) 자기예측 정상 ref : label-free (모델이 정상이라 찍은 beat만; 깨끗)
#  (c)가 (a)에 근접하면 → P파 정보가 진짜(누출 아님). (b)~26수준이면 → 정상기준이 핵심.
#
#  실행:
#    exec(open('/content/drive/MyDrive/mitbih/colab_step9_pwave.py').read())   # extract_pwave_features
#    exec(open('/content/drive/MyDrive/mitbih/colab_step9c_labelfree.py').read())
#    diag_lf()                 # (a),(b) 즉시 (모델 불필요)
#    diag_lf(selfpred=True)    # (c) 추가 (bootstrap CNN 학습, torch 필요)
# =============================================================================
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score

DS1=[101,106,108,109,112,114,115,116,118,119,122,124,201,203,205,207,208,209,215,220,223,230]
DS2=[100,103,105,111,113,117,121,123,200,202,210,212,213,214,219,221,222,228,231,232,233,234]

def _load():
    d=np.load("/content/drive/MyDrive/mitbih/mamba_data.npz")
    return d["beat"],d["ref"],d["feats"],d["y"],d["pid"]

def _allbeat_median_ref(beats,pid):
    r=np.empty_like(beats)
    for p in np.unique(pid):
        m=pid==p; r[m]=np.median(beats[m],axis=0,keepdims=True)
    return r.astype("float32")

def _selfpred_ref(beats,feats,y,pid,device=None):
    # bootstrap CNN(전체 label-free ref로 8ep) → P(normal) 상위 절반 median = 깨끗한 정상
    import torch,torch.nn as nn
    from sklearn.preprocessing import RobustScaler
    from sklearn.model_selection import GroupShuffleSplit
    dev=device or ("cuda" if torch.cuda.is_available() else "cpu")
    ref0=_allbeat_median_ref(beats,pid)
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
            super().__init__(); s.e=Enc(); s.fm=nn.Sequential(nn.Linear(feats.shape[1],64),nn.ReLU(),nn.Linear(64,64),nn.ReLU())
            s.cls=nn.Sequential(nn.Linear(128,64),nn.ReLU(),nn.Linear(64,3))
        def forward(s,b,r,f): return s.cls(torch.cat([s.e(b),s.fm(f)],-1))
    m1=np.isin(pid,DS1)
    torch.manual_seed(0); np.random.seed(0)
    sc=RobustScaler().fit(feats[m1]); fa=np.nan_to_num(sc.transform(feats),posinf=0,neginf=0).astype("float32")
    M=Net().to(dev); opt=torch.optim.AdamW(M.parameters(),1e-3,weight_decay=1e-4)
    lf=nn.CrossEntropyLoss(weight=torch.tensor([1.,3.,1.5],device=dev))
    ds=torch.utils.data.TensorDataset(*[torch.from_numpy(x) for x in (beats[m1],ref0[m1],fa[m1],y[m1])])
    dl=torch.utils.data.DataLoader(ds,batch_size=512,shuffle=True)
    for ep in range(8):
        M.train()
        for b,r,f,yy in dl:
            b,r,f,yy=(t.to(dev) for t in (b,r,f,yy)); opt.zero_grad()
            loss=lf(M(b,r,f),yy); loss.backward(); opt.step()
    M.eval(); pn=np.zeros(len(beats))
    with torch.no_grad():
        for i in range(0,len(beats),4096):
            pn[i:i+4096]=torch.softmax(M(torch.from_numpy(beats[i:i+4096]).to(dev),
                torch.from_numpy(ref0[i:i+4096]).to(dev),torch.from_numpy(fa[i:i+4096]).to(dev)),-1)[:,0].cpu().numpy()
    r=np.empty_like(beats)
    for p in np.unique(pid):
        idx=np.where(pid==p)[0]; k=max(5,len(idx)//2)
        sel=idx[np.argsort(-pn[idx])[:k]]; r[idx]=np.median(beats[sel],axis=0,keepdims=True)
    return r.astype("float32")

def _evalset(X,m1,m2,y1,y2):
    sc=StandardScaler().fit(np.nan_to_num(X[m1]))
    X1=np.nan_to_num(sc.transform(np.nan_to_num(X[m1]))); X2=np.nan_to_num(sc.transform(np.nan_to_num(X[m2])))
    clf=LogisticRegression(max_iter=5000,C=1.0,class_weight={0:1,1:3,2:1.5}).fit(X1,y1)
    p2=clf.predict_proba(X2)
    return (average_precision_score((y2==1).astype(int),p2[:,1]),
            average_precision_score((y2==2).astype(int),p2[:,2]))

def diag_lf(selfpred=False):
    beats,ref_norm,feats,y,pid=_load()
    m1=np.isin(pid,DS1); m2=np.isin(pid,DS2); y1,y2=y[m1],y[m2]
    base=_evalset(feats,m1,m2,y1,y2)
    print(f"기준선 26개만: S={base[0]:.4f}  V={base[1]:.4f}\n")
    print("정상기준별  26+P파8  →  S 증분:")
    refs={"(a)정상템플릿 ref [누출]":ref_norm,
          "(b)전체 median ref [LF]":_allbeat_median_ref(beats,pid)}
    if selfpred:
        print("  ... (c) 자기예측 정상 ref 만드는 중(bootstrap CNN)"); refs["(c)자기예측 정상 ref [LF·깨끗]"]=_selfpred_ref(beats,feats,y,pid)
    for nm,rf in refs.items():
        Xpw=extract_pwave_features(beats,rf,pid)
        S,V=_evalset(np.concatenate([feats,Xpw],1),m1,m2,y1,y2)
        print(f"  {nm:26s}: S={S:.4f}(증분 {S-base[0]:+.4f})  V={V:.4f}")
    print("\n  → (b)/(c) 증분이 +0.05 이상이면: P파 정보가 label-free로도 실재(누출 아님).")
    print("     (b)/(c)가 ~0이면: +0.20은 '정상템플릿을 라벨로 알려준' 누출 효과였음.")
