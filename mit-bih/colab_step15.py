# =============================================================================
#  colab_step15.py  —  [STEP 1.5] 분할(val/train) 고치기 · 측정 신뢰성 확보
#
#  STEP1 결론: Focal/oversampling 은 inter-patient 에서 오히려 해로움(폐기).
#              baseline A 가 이미 S_PR_AUC≈0.673 (>목표 0.613). 진짜 병목은
#              "val 이 S 를 못 재서 모델선택이 깨지고, seed 마다 S-heavy 환자가
#               train 에서 빠지면 성능/분산이 폭발" 하는 것.
#
#  이번 변경: 오직 '분할 방식'만 바꿈 (다른 요소는 baseline 고정 → 효과 분리).
#    · GroupShuffleSplit(무작위)  →  StratifiedGroupKFold(S 비율 맞춘 환자분할)
#      → val 에 S 가 반드시 들어와 측정 가능 + train 에서 S 안 빠짐 → 분산↓
#  진단 출력 추가: seed 별 val/train 의 S 개수, val 환자 목록,
#                 그리고 best-epoch vs last-epoch 의 DS2 성능(모델선택이 돕는지).
#
#  실행: 라이브러리 셀로 exec 후
#        run_split("A_gss")   # 원래 방식 재현(무작위 분할)
#        run_split("A_sgkf")  # 고친 방식(계층 분할)  ← 이게 STEP1.5
# =============================================================================
import os, json
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from sklearn.preprocessing import RobustScaler
from sklearn.model_selection import GroupShuffleSplit, StratifiedGroupKFold
from sklearn.metrics import average_precision_score, precision_recall_fscore_support

DATA_PATH = "/content/drive/MyDrive/mitbih/mamba_data.npz"
SAVE_DIR  = "/content/drive/MyDrive/mitbih/ablation_step15"

DS1_IDS=[101,106,108,109,112,114,115,116,118,119,122,124,201,203,205,207,208,209,215,220,223,230]
DS2_IDS=[100,103,105,111,113,117,121,123,200,202,210,212,213,214,219,221,222,228,231,232,233,234]
SEEDS=[1000,1001,1002,1003,1004]     # STEP1 보다 늘려 분산을 제대로 봄. 최종은 range(1000,1015).


class Cfg:
    n_leads=2; beat_len=300; feat_dim=26; n_classes=3; emb_dim=64
    n_proto=32
    class_w=(1.0,3.0,1.5); lr=1e-3; epochs=15; batch=512
    label_free_ref=False
    # ---- baseline 고정 (STEP1 에서 해롭다고 증명된 것들은 off) ----
    loss_type="wce"; focal_gamma=2.0; supcon_weight=0.0; supcon_temp=0.1; balanced_sampler=False
    # ---- [STEP 1.5] 이번 변경 대상 ----
    val_split="sgkf"        # "gss"(원래 무작위) | "sgkf"(계층 환자분할)
    n_folds=5               # sgkf 폴드 수(=val 비율 1/n_folds)


# ─────────── 모델 (원본 구조, STEP1 과 동일) ───────────
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

class CNNBasePSA2(nn.Module):
    def __init__(self,cfg):
        super().__init__(); self.cfg=cfg
        self.encoder=CNNEncoder(cfg)
        self.siamese=SiameseContrast(cfg.emb_dim,cfg.emb_dim)
        self.gate=GatedResidual(cfg.emb_dim)
        self.proto=PrototypeBank(cfg.emb_dim,cfg.n_proto)
        self.feat_mlp=FeatureMLP(cfg.feat_dim,cfg.emb_dim)
        self.classifier=nn.Sequential(
            nn.Linear(cfg.emb_dim*3,cfg.emb_dim),nn.ReLU(),nn.Linear(cfg.emb_dim,cfg.n_classes))
        self.proj_head=nn.Sequential(
            nn.Linear(cfg.emb_dim,cfg.emb_dim),nn.ReLU(),nn.Linear(cfg.emb_dim,128))
    def forward(self,beat,ref,feats,return_emb=False):
        z1=self.encoder(beat); z2=self.encoder(ref)
        zb=self.siamese(z1,z2); z=self.gate(z1,zb)
        z_proto=self.proto(z); z_feat=self.feat_mlp(feats)
        logits=self.classifier(torch.cat([z,z_proto,z_feat],dim=-1))
        if return_emb: return logits,F.normalize(self.proj_head(z),dim=-1)
        return logits


# ─────────── 손실(있지만 기본 off) ───────────
class FocalLoss(nn.Module):
    def __init__(self,alpha,gamma=2.0):
        super().__init__(); self.register_buffer("alpha",torch.tensor(alpha,dtype=torch.float32)); self.gamma=gamma
    def forward(self,logits,y):
        logp=F.log_softmax(logits,dim=1); logpt=logp.gather(1,y.view(-1,1)).squeeze(1); pt=logpt.exp()
        return (-self.alpha.to(logits.device)[y]*(1-pt).pow(self.gamma)*logpt).mean()

class SupConLoss(nn.Module):
    def __init__(self,temperature=0.1):
        super().__init__(); self.t=temperature
    def forward(self,feats,labels):
        device=feats.device; B=feats.size(0)
        sim=(feats@feats.t())/self.t; sim=sim-sim.max(dim=1,keepdim=True)[0].detach()
        labels=labels.view(-1,1); pos=(labels==labels.t()).float(); self_mask=1-torch.eye(B,device=device); pos=pos*self_mask
        exp=torch.exp(sim)*self_mask; logp=sim-torch.log(exp.sum(1,keepdim=True)+1e-12)
        cnt=pos.sum(1); mlp=(pos*logp).sum(1)/cnt.clamp(min=1); valid=cnt>0
        return -(mlp[valid]).mean() if valid.any() else feats.sum()*0.0


# ─────────── 데이터/학습/평가 ───────────
def load_data(cfg):
    d=np.load(DATA_PATH)
    beats,refs=d["beat"],d["ref"]; feats,y,pid=d["feats"],d["y"],d["pid"]
    if cfg.label_free_ref:
        refs=np.empty_like(beats)
        for p in np.unique(pid):
            m=pid==p; refs[m]=np.median(beats[m],axis=0,keepdims=True)
        refs=refs.astype("float32")
    return beats,refs,feats,y,pid

def subset(arrs,mask): return tuple(a[mask] for a in arrs)

def _loader(arrs,batch,shuffle,balanced=False):
    beat,ref,feats,y=arrs
    ds=torch.utils.data.TensorDataset(torch.from_numpy(np.asarray(beat)),
        torch.from_numpy(np.asarray(ref)),torch.from_numpy(np.asarray(feats)),
        torch.from_numpy(np.asarray(y)))
    if balanced and shuffle:
        yv=np.asarray(y).astype(int); cnt=np.bincount(yv,minlength=3).astype(np.float64)
        w=1.0/np.clip(cnt,1,None); sampler=torch.utils.data.WeightedRandomSampler(
            torch.from_numpy(w[yv]).double(),num_samples=len(yv),replacement=True)
        return torch.utils.data.DataLoader(ds,batch_size=batch,sampler=sampler)
    return torch.utils.data.DataLoader(ds,batch_size=batch,shuffle=shuffle)

def make_cls_loss(cfg,device):
    if cfg.loss_type=="focal": return FocalLoss(cfg.class_w,cfg.focal_gamma).to(device)
    return nn.CrossEntropyLoss(weight=torch.tensor(cfg.class_w,dtype=torch.float32,device=device))

@torch.no_grad()
def evaluate(model,loader,device):
    model.eval(); probs,ys=[],[]
    for beat,ref,feats,y in loader:
        p=torch.softmax(model(beat.to(device),ref.to(device),feats.to(device)),-1)
        probs.append(p.cpu().numpy()); ys.append(y.numpy())
    return np.concatenate(probs),np.concatenate(ys)

def metrics(probs,y):
    s=average_precision_score((y==1).astype(int),probs[:,1])
    v=average_precision_score((y==2).astype(int),probs[:,2])
    n=average_precision_score((y==0).astype(int),probs[:,0])
    pred=probs.argmax(1); p,r,f,_=precision_recall_fscore_support(y,pred,labels=[0,1,2],zero_division=0)
    return {"S_PR_AUC":float(s),"V_PR_AUC":float(v),"macro_PR_AUC":float((n+s+v)/3),
            "S_Se":float(r[1]),"S_P":float(p[1]),"S_F1":float(f[1]),
            "V_Se":float(r[2]),"V_P":float(p[2]),"V_F1":float(f[2])}

def split_ds1(cfg,seed,feats1,y1,pid1):
    if cfg.val_split=="sgkf":
        spl=StratifiedGroupKFold(n_splits=cfg.n_folds,shuffle=True,random_state=seed)
        return next(spl.split(feats1,y1,groups=pid1))
    spl=GroupShuffleSplit(n_splits=1,test_size=0.2,random_state=seed)
    return next(spl.split(feats1,y1,groups=pid1))

def train(model,tr_loader,va_loader,cfg,device):
    opt=torch.optim.AdamW(model.parameters(),lr=cfg.lr,weight_decay=1e-4)
    cls_loss=make_cls_loss(cfg,device); supcon=SupConLoss(cfg.supcon_temp).to(device)
    use_sc=cfg.supcon_weight>0; best=-1; best_state=None; last_state=None; best_ep=-1
    for ep in range(cfg.epochs):
        model.train()
        for beat,ref,feats,y in tr_loader:
            beat,ref,feats,y=(t.to(device) for t in (beat,ref,feats,y)); opt.zero_grad()
            if use_sc:
                logits,emb=model(beat,ref,feats,return_emb=True)
                loss=cls_loss(logits,y)+cfg.supcon_weight*supcon(emb,y)
            else:
                loss=cls_loss(model(beat,ref,feats),y)
            loss.backward(); torch.nn.utils.clip_grad_norm_(model.parameters(),1.0); opt.step()
        pr,ys=evaluate(model,va_loader,device); m=metrics(pr,ys)
        score=0.5*(m["S_PR_AUC"]+m["V_PR_AUC"])
        last_state={k:v.cpu() for k,v in model.state_dict().items()}
        if score>best: best=score; best_ep=ep; best_state={k:v.cpu() for k,v in last_state.items()}
        print(f"    epoch {ep:02d}  val S={m['S_PR_AUC']:.4f}  V={m['V_PR_AUC']:.4f}")
    return best_state,last_state,best_ep

def run_one_seed(cfg,seed,ds1,ds2,device):
    torch.manual_seed(seed); np.random.seed(seed)
    beats1,refs1,feats1,y1,pid1=ds1; beats2,refs2,feats2,y2,pid2=ds2
    tr_idx,va_idx=split_ds1(cfg,seed,feats1,y1,pid1)
    # --- 진단: 분할이 S 를 어떻게 나눴나 ---
    print(f"    [split={cfg.val_split}] val환자={sorted(np.unique(pid1[va_idx]).tolist())}")
    print(f"    train S={int((y1[tr_idx]==1).sum())}  val S={int((y1[va_idx]==1).sum())}  "
          f"(전체 DS1 S={int((y1==1).sum())})")
    sc=RobustScaler().fit(feats1[tr_idx])
    f1=np.nan_to_num(sc.transform(feats1),posinf=0,neginf=0).astype("float32")
    f2=np.nan_to_num(sc.transform(feats2),posinf=0,neginf=0).astype("float32")
    tr=(beats1[tr_idx],refs1[tr_idx],f1[tr_idx],y1[tr_idx])
    va=(beats1[va_idx],refs1[va_idx],f1[va_idx],y1[va_idx])
    te_loader=_loader((beats2,refs2,f2,y2),cfg.batch,False)
    model=CNNBasePSA2(cfg).to(device)
    best_state,last_state,best_ep=train(model,
        _loader(tr,cfg.batch,True,balanced=cfg.balanced_sampler),
        _loader(va,cfg.batch,False),cfg,device)
    # best-epoch DS2 (주 지표)
    model.load_state_dict(best_state); probs,ys=evaluate(model,te_loader,device); m_best=metrics(probs,ys)
    # last-epoch DS2 (모델선택이 돕는지 진단)
    model.load_state_dict(last_state); pl,yl=evaluate(model,te_loader,device); m_last=metrics(pl,yl)
    print(f"    => DS2  best(ep{best_ep:02d}) S={m_best['S_PR_AUC']:.4f} | "
          f"last(ep14) S={m_last['S_PR_AUC']:.4f}   V(best)={m_best['V_PR_AUC']:.4f}")
    return probs,ys,pid2,m_best,m_last


PRESETS={
    "A_gss":  dict(val_split="gss"),    # 원래 무작위 분할 재현(대조군)
    "A_sgkf": dict(val_split="sgkf"),   # 계층 환자분할(STEP1.5 처방)
}

def run_split(tag, seeds=None, **override):
    assert tag in PRESETS, f"tag must be one of {list(PRESETS)}"
    cfg=Cfg()
    for k,v in {**PRESETS[tag], **override}.items(): setattr(cfg,k,v)
    seeds=seeds or SEEDS; device="cuda" if torch.cuda.is_available() else "cpu"
    out=os.path.join(SAVE_DIR,tag); os.makedirs(out,exist_ok=True)
    print(f"===== {tag} =====  val_split={cfg.val_split} loss={cfg.loss_type} "
          f"supcon={cfg.supcon_weight} balanced={cfg.balanced_sampler}  device={device}")
    beats,refs,feats,y,pid=load_data(cfg)
    ds1=subset((beats,refs,feats,y,pid),np.isin(pid,DS1_IDS))
    ds2=subset((beats,refs,feats,y,pid),np.isin(pid,DS2_IDS))
    rows_best,rows_last=[],[]
    for seed in seeds:
        print(f"  [seed {seed}]")
        probs,ys,pp,mb,ml=run_one_seed(cfg,seed,ds1,ds2,device)
        np.savez(os.path.join(out,f"cnn_{tag}_s{seed}.npz"),prob=probs,y=ys,pid=pp)
        rows_best.append(mb); rows_last.append(ml)
    def agg(rows,k):
        a=np.array([r[k] for r in rows]); return a.mean(),a.std()
    summary={"tag":tag,"val_split":cfg.val_split,"seeds":list(seeds),
             "per_seed_best":rows_best,"per_seed_last":rows_last}
    with open(os.path.join(out,f"summary_{tag}.json"),"w") as fp: json.dump(summary,fp,indent=2)
    print(f"\n----- {tag} 집계 (best-epoch, 원본목표 S 0.613/V 0.932) -----")
    for k in ["S_PR_AUC","V_PR_AUC","macro_PR_AUC","S_Se","S_P","S_F1"]:
        m,s=agg(rows_best,k); print(f"  {k:12s} = {m:.4f} ± {s:.4f}")
    ms,ss=agg(rows_best,"S_PR_AUC"); ml,sl=agg(rows_last,"S_PR_AUC")
    print(f"  [진단] S best={ms:.4f}±{ss:.4f}  vs  last={ml:.4f}±{sl:.4f}  "
          f"(std 가 줄고 best≈last 면 분할·선택이 안정됨)")
    print(f"\n저장됨: {out}/")
    return summary
