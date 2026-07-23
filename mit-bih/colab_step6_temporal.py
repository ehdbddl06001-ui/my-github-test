# =============================================================================
#  colab_step6_temporal.py  —  [STEP 2] 시계열 문맥: 이웃 beat 형태 추가
#
#  가설: SVEB(S)는 '조기성(prematurity)+주변 리듬 문맥'이 핵심. 지금 CNN은 현재 beat
#        1개(300 sample)만 봄. RR 스칼라(feats에 이미 있음)를 넘어, 이전/다음 beat의
#        '실제 형태'를 주면 새 정보가 들어간다.
#
#  ★ 데이터 재생성 불필요 ★  npz의 t(시간)+pid로 환자별 시간정렬 →
#     이전/다음 beat 파형을 '이미 있는 다른 행'에서 인덱싱해 구성.
#
#  모델: 공유 인코더로 prev/cur/next 인코딩 → 이웃차이 [z_prev−z_cur, z_next−z_cur]를
#        temporal_head로 요약해 융합에 추가. 나머지(ref/siamese/proto/feats)는 동일.
#  비교:  base (현재 beat만)  vs  temporal (이웃 추가)  — 같은 저울(gss+앙상블, 이중지표).
#
#  실행:
#    exec(open('/content/drive/MyDrive/mitbih/colab_step6_temporal.py').read())
#    run_temporal("base"); run_temporal("temporal")
# =============================================================================
import os, json
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from sklearn.preprocessing import RobustScaler
from sklearn.model_selection import GroupShuffleSplit
from sklearn.metrics import average_precision_score, precision_recall_fscore_support, roc_auc_score

DATA_PATH = "/content/drive/MyDrive/mitbih/mamba_data.npz"
SAVE_DIR  = "/content/drive/MyDrive/mitbih/ablation_step6"

DS1_IDS=[101,106,108,109,112,114,115,116,118,119,122,124,201,203,205,207,208,209,215,220,223,230]
DS2_IDS=[100,103,105,111,113,117,121,123,200,202,210,212,213,214,219,221,222,228,231,232,233,234]
SEEDS=[1000,1001,1002,1003,1004]


class Cfg:
    n_leads=2; beat_len=300; feat_dim=26; n_classes=3; emb_dim=64; n_proto=32
    class_w=(1.0,3.0,1.5); lr=1e-3; epochs=15; batch=512
    label_free_ref=True
    use_temporal=True


class CNNEncoder(nn.Module):
    def __init__(self,cfg):
        super().__init__()
        self.net=nn.Sequential(
            nn.Conv1d(cfg.n_leads,32,7,padding=3), nn.BatchNorm1d(32), nn.ReLU(), nn.MaxPool1d(2),
            nn.Conv1d(32,64,5,padding=2),          nn.BatchNorm1d(64), nn.ReLU(), nn.MaxPool1d(2),
            nn.Conv1d(64,128,3,padding=1),         nn.BatchNorm1d(128),nn.ReLU(), nn.AdaptiveAvgPool1d(1),
        )
        self.proj=nn.Linear(128,cfg.emb_dim)
    def forward(self,wave): return self.proj(self.net(wave).squeeze(-1))

class SiameseContrast(nn.Module):
    def __init__(self,emb,out):
        super().__init__(); self.fc=nn.Sequential(nn.Linear(emb*4,out),nn.ReLU())
    def forward(self,z1,z2): return self.fc(torch.cat([z1,z2,z1-z2,(z1-z2).abs()],dim=-1))

class PrototypeBank(nn.Module):
    def __init__(self,emb,n_proto):
        super().__init__(); self.proto=nn.Parameter(torch.randn(n_proto,emb)*0.1); self.scale=emb**-0.5
    def forward(self,z): return torch.softmax((z@self.proto.t())*self.scale,dim=-1)@self.proto

class GatedResidual(nn.Module):
    def __init__(self,emb):
        super().__init__(); self.gate=nn.Linear(emb*2,emb)
    def forward(self,z,zb): return z+torch.sigmoid(self.gate(torch.cat([z,zb],dim=-1)))*zb

class FeatureMLP(nn.Module):
    def __init__(self,feat_dim,out):
        super().__init__(); self.net=nn.Sequential(nn.Linear(feat_dim,64),nn.ReLU(),nn.Linear(64,out),nn.ReLU())
    def forward(self,f): return self.net(f)

class CNNTemporal(nn.Module):
    def __init__(self,cfg):
        super().__init__(); self.use_temporal=cfg.use_temporal
        self.encoder=CNNEncoder(cfg)
        self.siamese=SiameseContrast(cfg.emb_dim,cfg.emb_dim)
        self.gate=GatedResidual(cfg.emb_dim)
        self.proto=PrototypeBank(cfg.emb_dim,cfg.n_proto)
        self.feat_mlp=FeatureMLP(cfg.feat_dim,cfg.emb_dim)
        cls_in=cfg.emb_dim*3
        if cfg.use_temporal:
            self.temporal_head=nn.Sequential(nn.Linear(cfg.emb_dim*2,cfg.emb_dim),nn.ReLU())
            cls_in=cfg.emb_dim*4
        self.classifier=nn.Sequential(nn.Linear(cls_in,cfg.emb_dim),nn.ReLU(),nn.Linear(cfg.emb_dim,cfg.n_classes))
    def forward(self,beat,prev,nxt,ref,feats):
        z1=self.encoder(beat); z2=self.encoder(ref)
        zb=self.siamese(z1,z2); z=self.gate(z1,zb)
        parts=[z,self.proto(z),self.feat_mlp(feats)]
        if self.use_temporal:
            zp=self.encoder(prev); zn=self.encoder(nxt)
            parts.append(self.temporal_head(torch.cat([zp-z1,zn-z1],dim=-1)))  # 이웃 형태 차이
        return self.classifier(torch.cat(parts,dim=-1))


def make_cls_loss(cfg,device):
    return nn.CrossEntropyLoss(weight=torch.tensor(cfg.class_w,dtype=torch.float32,device=device))

def build_neighbors(beats,pid,t):
    """환자별 시간순으로 각 beat의 이전/다음 beat 파형 구성 (edge는 자기 자신)."""
    prev=beats.copy(); nxt=beats.copy()
    for p in np.unique(pid):
        idx=np.where(pid==p)[0]
        order=idx[np.argsort(t[idx],kind="stable")]   # 시간순
        prev[order[1:]]=beats[order[:-1]]
        nxt[order[:-1]]=beats[order[1:]]
    return prev.astype("float32"),nxt.astype("float32")

def load_data(cfg):
    d=np.load(DATA_PATH)
    beats,refs=d["beat"],d["ref"]; feats,y,pid,t=d["feats"],d["y"],d["pid"],d["t"]
    if cfg.label_free_ref:
        refs=np.empty_like(beats)
        for p in np.unique(pid):
            m=pid==p; refs[m]=np.median(beats[m],axis=0,keepdims=True)
        refs=refs.astype("float32")
    prev,nxt=build_neighbors(beats,pid,t)
    return beats,prev,nxt,refs,feats,y,pid

def subset(arrs,mask): return tuple(a[mask] for a in arrs)
def _loader(arrs,batch,shuffle):
    ds=torch.utils.data.TensorDataset(*[torch.from_numpy(np.asarray(a)) for a in arrs])
    return torch.utils.data.DataLoader(ds,batch_size=batch,shuffle=shuffle)

@torch.no_grad()
def predict(model,beat,prev,nxt,ref,feats,device,batch=4096):
    model.eval(); out=[]
    for i in range(0,len(beat),batch):
        sl=slice(i,i+batch)
        args=[torch.from_numpy(a[sl]).to(device) for a in (beat,prev,nxt,ref,feats)]
        out.append(torch.softmax(model(*args),-1).cpu().numpy())
    return np.concatenate(out)

def metrics(probs,y):
    s=average_precision_score((y==1).astype(int),probs[:,1]); v=average_precision_score((y==2).astype(int),probs[:,2])
    n=average_precision_score((y==0).astype(int),probs[:,0])
    pred=probs.argmax(1); p,r,f,_=precision_recall_fscore_support(y,pred,labels=[0,1,2],zero_division=0)
    return {"S_PR_AUC":float(s),"V_PR_AUC":float(v),"macro_PR_AUC":float((n+s+v)/3),
            "S_Se":float(r[1]),"S_P":float(p[1]),"S_F1":float(f[1])}

def per_patient_S_auc(probs,y,pid,min_s=5):
    a=[]
    for p in np.unique(pid):
        m=pid==p; yy=(y[m]==1).astype(int)
        if yy.sum()<min_s or yy.sum()==m.sum(): continue
        a.append(roc_auc_score(yy,probs[m,1]))
    return (float(np.mean(a)) if a else float("nan")),len(a)

def train(model,tr,va,cfg,device):
    opt=torch.optim.AdamW(model.parameters(),lr=cfg.lr,weight_decay=1e-4)
    cls=make_cls_loss(cfg,device); best=-1; bs=None; tl=_loader(tr,cfg.batch,True)
    for ep in range(cfg.epochs):
        model.train()
        for beat,prev,nxt,ref,feats,y in tl:
            beat,prev,nxt,ref,feats,y=(t.to(device) for t in (beat,prev,nxt,ref,feats,y)); opt.zero_grad()
            loss=cls(model(beat,prev,nxt,ref,feats),y); loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(),1.0); opt.step()
        pv=predict(model,va[0],va[1],va[2],va[3],va[4],device); m=metrics(pv,va[5])
        sc=0.5*(m["S_PR_AUC"]+m["V_PR_AUC"])
        if sc>best: best=sc; bs={k:v.cpu() for k,v in model.state_dict().items()}
    if bs: model.load_state_dict(bs)
    return model

PRESETS={"base":dict(use_temporal=False), "temporal":dict(use_temporal=True)}

def run_temporal(tag, seeds=None, **override):
    assert tag in PRESETS
    cfg=Cfg()
    for k,v in {**PRESETS[tag],**override}.items(): setattr(cfg,k,v)
    seeds=seeds or SEEDS; device="cuda" if torch.cuda.is_available() else "cpu"
    out=os.path.join(SAVE_DIR,tag); os.makedirs(out,exist_ok=True)
    print(f"===== {tag} =====  use_temporal={cfg.use_temporal} label_free_ref={cfg.label_free_ref}  device={device}")
    beats,prev,nxt,refs,feats,y,pid=load_data(cfg)
    ds1=subset((beats,prev,nxt,refs,feats,y,pid),np.isin(pid,DS1_IDS))
    ds2=subset((beats,prev,nxt,refs,feats,y,pid),np.isin(pid,DS2_IDS))
    b1,pv1,nx1,r1,ft1,y1,p1=ds1; b2,pv2,nx2,r2,ft2,y2,p2=ds2
    print(f"params={sum(pp.numel() for pp in CNNTemporal(cfg).parameters()):,}")
    rows=[]; pp_rows=[]; probs_list=[]
    for seed in seeds:
        torch.manual_seed(seed); np.random.seed(seed)
        tr_idx,va_idx=next(GroupShuffleSplit(1,test_size=0.2,random_state=seed).split(ft1,y1,groups=p1))
        sc=RobustScaler().fit(ft1[tr_idx])
        f1=np.nan_to_num(sc.transform(ft1),posinf=0,neginf=0).astype("float32")
        f2=np.nan_to_num(sc.transform(ft2),posinf=0,neginf=0).astype("float32")
        tr=(b1[tr_idx],pv1[tr_idx],nx1[tr_idx],r1[tr_idx],f1[tr_idx],y1[tr_idx])
        va=(b1[va_idx],pv1[va_idx],nx1[va_idx],r1[va_idx],f1[va_idx],y1[va_idx])
        M=CNNTemporal(cfg).to(device)
        M=train(M,tr,va,cfg,device)
        pr=predict(M,b2,pv2,nx2,r2,f2,device)
        np.savez(os.path.join(out,f"cnn_{tag}_s{seed}.npz"),prob=pr,y=y2,pid=p2)
        m=metrics(pr,y2); ppa,ppn=per_patient_S_auc(pr,y2,p2)
        rows.append(m); pp_rows.append(ppa); probs_list.append(pr)
        print(f"  [seed {seed}]  전역S={m['S_PR_AUC']:.4f}  V={m['V_PR_AUC']:.4f}  환자별S_AUC={ppa:.4f}")
    Sarr=np.array([r["S_PR_AUC"] for r in rows]); ppa_arr=np.array(pp_rows)
    ens=np.stack(probs_list,0).mean(0); ens=ens/ens.sum(1,keepdims=True)
    me=metrics(ens,y2); mpp,mppn=per_patient_S_auc(ens,y2,p2)
    summary={"tag":tag,"use_temporal":cfg.use_temporal,"seeds":list(seeds),
             "per_seed":rows,"per_seed_patientAUC":pp_rows,"ensemble":me,"ensemble_patientAUC":mpp}
    with open(os.path.join(out,f"summary_{tag}.json"),"w") as fp: json.dump(summary,fp,indent=2)
    print(f"\n----- {tag} -----")
    print(f"  [전역] 개별S={Sarr.mean():.4f}±{Sarr.std():.4f}  ▶앙상블S={me['S_PR_AUC']:.4f}  V={me['V_PR_AUC']:.4f}")
    print(f"  [환자별] 개별={ppa_arr.mean():.4f}±{ppa_arr.std():.4f}  ▶앙상블={mpp:.4f}({mppn}명)")
    print(f"저장됨: {out}/")
    return summary
