# =============================================================================
#  colab_step3.py  —  [STEP 3] 환자별 적응 함수 g(patient) : label-free FiLM
#
#  가설(사장님):  ŷ = f(x, g(patient))   — 환자마다 결정경계가 달라야 한다.
#  구현: 환자 임베딩 g(patient)로 분류기 은닉층을 FiLM(γ,β) 조정.
#        logit = cls_out( (1+γ(g))⊙h + β(g) ),  h = 융합표현
#
#  ★ 제약 못박기 ★
#   1) TEST 라벨 미사용: g(patient)=patient_head(encoder(ref)),
#      ref 는 label_free_ref=True (그 환자 '전체 beat' median; 라벨 안 씀).
#   2) HyperNetwork 아님: 전체 가중치 생성(과적합 위험) 대신 FiLM 조건화.
#   3) γ,β init=0 → 학습 시작은 baseline 과 동일(항등). 도움될 때만 적응 켜짐.
#
#  프로토콜: 무작위분할(gss) + seed 앙상블(확정된 공식 저울).
#  비교:  base_lf (label-free ref, FiLM 없음)  vs  film (STEP 3)
#         → 앙상블 S 가 오르면 '환자 적응'이 실제로 기여.
#
#  실행:
#    exec(open('/content/drive/MyDrive/mitbih/colab_step3.py').read())
#    run_pa("base_lf")   # label-free 대조군
#    run_pa("film")      # STEP 3 환자적응
# =============================================================================
import os, json
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from sklearn.preprocessing import RobustScaler
from sklearn.model_selection import GroupShuffleSplit
from sklearn.metrics import average_precision_score, precision_recall_fscore_support

DATA_PATH = "/content/drive/MyDrive/mitbih/mamba_data.npz"
SAVE_DIR  = "/content/drive/MyDrive/mitbih/ablation_step3"

DS1_IDS=[101,106,108,109,112,114,115,116,118,119,122,124,201,203,205,207,208,209,215,220,223,230]
DS2_IDS=[100,103,105,111,113,117,121,123,200,202,210,212,213,214,219,221,222,228,231,232,233,234]
SEEDS=[1000,1001,1002,1003,1004]     # 최종은 range(1000,1015)


class Cfg:
    n_leads=2; beat_len=300; feat_dim=26; n_classes=3; emb_dim=64
    n_proto=32
    class_w=(1.0,3.0,1.5); lr=1e-3; epochs=15; batch=512
    loss_type="wce"; focal_gamma=2.0; supcon_weight=0.0; supcon_temp=0.1; balanced_sampler=False
    val_split="gss"                 # 확정: 무작위분할
    # ---- [STEP 3] ----
    label_free_ref=True             # ★ 라벨-프리 환자 기준(전체 beat median)
    patient_adapt=True              # FiLM 환자적응 on/off


# ─────────── 모델 (원본 + FiLM 환자적응) ───────────
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

class CNNBasePSA2PA(nn.Module):
    """원본 base_psa2 + label-free 환자적응(FiLM). patient_adapt=False면 baseline과 동일."""
    def __init__(self,cfg):
        super().__init__(); self.cfg=cfg; self.patient_adapt=cfg.patient_adapt
        self.encoder=CNNEncoder(cfg)
        self.siamese=SiameseContrast(cfg.emb_dim,cfg.emb_dim)
        self.gate=GatedResidual(cfg.emb_dim)
        self.proto=PrototypeBank(cfg.emb_dim,cfg.n_proto)
        self.feat_mlp=FeatureMLP(cfg.feat_dim,cfg.emb_dim)
        # 분류기를 은닉/출력으로 분리(사이에 FiLM 삽입) — patient_adapt=False면 원본과 동일
        self.cls_hidden=nn.Sequential(nn.Linear(cfg.emb_dim*3,cfg.emb_dim),nn.ReLU())
        self.cls_out=nn.Linear(cfg.emb_dim,cfg.n_classes)
        # ---- 환자 함수 g(patient) & FiLM ----
        self.patient_head=nn.Sequential(nn.Linear(cfg.emb_dim,cfg.emb_dim),nn.ReLU())
        self.film=nn.Linear(cfg.emb_dim,cfg.emb_dim*2)      # → (γ, β)
        nn.init.zeros_(self.film.weight); nn.init.zeros_(self.film.bias)  # 시작=항등
        self.proj_head=nn.Sequential(nn.Linear(cfg.emb_dim,cfg.emb_dim),nn.ReLU(),nn.Linear(cfg.emb_dim,128))
    def forward(self,beat,ref,feats,return_emb=False):
        z1=self.encoder(beat); z2=self.encoder(ref)          # z2=환자 기준 임베딩(label-free ref)
        zb=self.siamese(z1,z2); z=self.gate(z1,zb)
        z_proto=self.proto(z); z_feat=self.feat_mlp(feats)
        h=self.cls_hidden(torch.cat([z,z_proto,z_feat],dim=-1))   # [B,emb]
        if self.patient_adapt:
            g=self.patient_head(z2)                          # g(patient), TEST 라벨 미사용
            gamma,beta=self.film(g).chunk(2,dim=-1)
            h=(1.0+gamma)*h+beta                             # FiLM: γ,β init 0 → 항등 시작
        logits=self.cls_out(h)
        if return_emb: return logits,F.normalize(self.proj_head(z),dim=-1)
        return logits


# ─────────── 손실 (기본 wce) ───────────
def make_cls_loss(cfg,device):
    return nn.CrossEntropyLoss(weight=torch.tensor(cfg.class_w,dtype=torch.float32,device=device))


# ─────────── 데이터/학습/평가 ───────────
def load_data(cfg):
    d=np.load(DATA_PATH)
    beats,refs=d["beat"],d["ref"]; feats,y,pid=d["feats"],d["y"],d["pid"]
    if cfg.label_free_ref:                                   # ★ 환자별 전체 beat median (라벨 미사용)
        refs=np.empty_like(beats)
        for p in np.unique(pid):
            m=pid==p; refs[m]=np.median(beats[m],axis=0,keepdims=True)
        refs=refs.astype("float32")
    return beats,refs,feats,y,pid

def subset(arrs,mask): return tuple(a[mask] for a in arrs)

def _loader(arrs,batch,shuffle):
    beat,ref,feats,y=arrs
    ds=torch.utils.data.TensorDataset(torch.from_numpy(np.asarray(beat)),
        torch.from_numpy(np.asarray(ref)),torch.from_numpy(np.asarray(feats)),
        torch.from_numpy(np.asarray(y)))
    return torch.utils.data.DataLoader(ds,batch_size=batch,shuffle=shuffle)

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
            "S_Se":float(r[1]),"S_P":float(p[1]),"S_F1":float(f[1])}

def train(model,tr_loader,va_loader,cfg,device):
    opt=torch.optim.AdamW(model.parameters(),lr=cfg.lr,weight_decay=1e-4)
    cls_loss=make_cls_loss(cfg,device); best=-1; best_state=None
    for ep in range(cfg.epochs):
        model.train()
        for beat,ref,feats,y in tr_loader:
            beat,ref,feats,y=(t.to(device) for t in (beat,ref,feats,y)); opt.zero_grad()
            loss=cls_loss(model(beat,ref,feats),y)
            loss.backward(); torch.nn.utils.clip_grad_norm_(model.parameters(),1.0); opt.step()
        pr,ys=evaluate(model,va_loader,device); m=metrics(pr,ys)
        score=0.5*(m["S_PR_AUC"]+m["V_PR_AUC"])
        if score>best: best=score; best_state={k:v.cpu() for k,v in model.state_dict().items()}
        print(f"    epoch {ep:02d}  val S={m['S_PR_AUC']:.4f}  V={m['V_PR_AUC']:.4f}")
    if best_state: model.load_state_dict(best_state)
    return model

def run_one_seed(cfg,seed,ds1,ds2,device):
    torch.manual_seed(seed); np.random.seed(seed)
    beats1,refs1,feats1,y1,pid1=ds1; beats2,refs2,feats2,y2,pid2=ds2
    gss=GroupShuffleSplit(n_splits=1,test_size=0.2,random_state=seed)
    tr_idx,va_idx=next(gss.split(feats1,y1,groups=pid1))
    sc=RobustScaler().fit(feats1[tr_idx])
    f1=np.nan_to_num(sc.transform(feats1),posinf=0,neginf=0).astype("float32")
    f2=np.nan_to_num(sc.transform(feats2),posinf=0,neginf=0).astype("float32")
    tr=(beats1[tr_idx],refs1[tr_idx],f1[tr_idx],y1[tr_idx])
    va=(beats1[va_idx],refs1[va_idx],f1[va_idx],y1[va_idx])
    model=CNNBasePSA2PA(cfg).to(device)
    model=train(model,_loader(tr,cfg.batch,True),_loader(va,cfg.batch,False),cfg,device)
    probs,ys=evaluate(model,_loader((beats2,refs2,f2,y2),cfg.batch,False),device)
    return probs,ys,pid2


PRESETS={
    "base_lf": dict(patient_adapt=False, label_free_ref=True),   # label-free 대조군(FiLM 없음)
    "film":    dict(patient_adapt=True,  label_free_ref=True),   # STEP 3 환자적응
}

def run_pa(tag, seeds=None, **override):
    assert tag in PRESETS
    cfg=Cfg()
    for k,v in {**PRESETS[tag], **override}.items(): setattr(cfg,k,v)
    seeds=seeds or SEEDS; device="cuda" if torch.cuda.is_available() else "cpu"
    out=os.path.join(SAVE_DIR,tag); os.makedirs(out,exist_ok=True)
    print(f"===== {tag} =====  patient_adapt={cfg.patient_adapt} label_free_ref={cfg.label_free_ref} "
          f"split={cfg.val_split}  device={device}")
    beats,refs,feats,y,pid=load_data(cfg)
    ds1=subset((beats,refs,feats,y,pid),np.isin(pid,DS1_IDS))
    ds2=subset((beats,refs,feats,y,pid),np.isin(pid,DS2_IDS))
    print(f"params={sum(p.numel() for p in CNNBasePSA2PA(cfg).parameters()):,}")
    rows=[]; probs_list=[]; y_ref=None
    for seed in seeds:
        print(f"  [seed {seed}]")
        probs,ys,pp=run_one_seed(cfg,seed,ds1,ds2,device)
        np.savez(os.path.join(out,f"cnn_{tag}_s{seed}.npz"),prob=probs,y=ys,pid=pp)
        m=metrics(probs,ys); rows.append(m); probs_list.append(probs); y_ref=ys
        print(f"    => DS2  S={m['S_PR_AUC']:.4f}  V={m['V_PR_AUC']:.4f}  macro={m['macro_PR_AUC']:.4f}")
    # 개별 집계
    def agg(k): a=np.array([r[k] for r in rows]); return a.mean(),a.std()
    # ★ seed 앙상블(확률평균) — 공식 저울
    ens=np.stack(probs_list,0).mean(0); ens=ens/ens.sum(1,keepdims=True)
    me=metrics(ens,y_ref)
    summary={"tag":tag,"config":{k:getattr(cfg,k) for k in
             ["patient_adapt","label_free_ref","val_split","loss_type","class_w","epochs","batch","lr"]},
             "seeds":list(seeds),"per_seed":rows,
             "individual_mean":{k:agg(k)[0] for k in rows[0]},
             "individual_std":{k:agg(k)[1] for k in rows[0]},
             "ensemble":me}
    with open(os.path.join(out,f"summary_{tag}.json"),"w") as fp: json.dump(summary,fp,indent=2)
    ms,ss=agg("S_PR_AUC"); mv,sv=agg("V_PR_AUC")
    print(f"\n----- {tag} -----")
    print(f"  개별 평균      S={ms:.4f} ± {ss:.4f}   V={mv:.4f} ± {sv:.4f}")
    print(f"  ▶ 앙상블(공식) S={me['S_PR_AUC']:.4f}            V={me['V_PR_AUC']:.4f}   "
          f"macro={me['macro_PR_AUC']:.4f}")
    print(f"     앙상블 S_Se={me['S_Se']:.3f}  S_P={me['S_P']:.3f}  S_F1={me['S_F1']:.3f}")
    print(f"\n저장됨: {out}/")
    return summary
