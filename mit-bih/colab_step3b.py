# =============================================================================
#  colab_step3b.py  —  [STEP 3b] 바운드 FiLM + 전역/환자별 이중 지표
#
#  STEP3 진단: FiLM γ가 무한정 커져(+7~8) 일부 환자 hidden을 폭발 →
#              환자별 S-score 스케일이 수천배씩 달라짐 → 전역 PR-AUC 붕괴.
#              (환자 안 분리도는 오히려 0.806→0.813 개선)
#
#  이번 수정(둘):
#   1) 바운드 FiLM:  γ = film_scale·tanh(·),  β = bias_scale·tanh(·)
#      → γ∈(-0.5,0.5) 로 폭주 제거, 환자간 점수 비교가능성 유지. init=0 → 항등 시작.
#   2) 이중 지표:  전역 S_PR_AUC(전체 DS2 한 줄 세우기) +
#                 환자별 S ROC-AUC 평균(환자마다 제 기준 = 사장님 가설의 옳은 저울)
#
#  비교:  base_lf(FiLM 없음)  vs  film(바운드 FiLM)  — 두 지표 모두에서.
#  실행:
#    exec(open('/content/drive/MyDrive/mitbih/colab_step3b.py').read())
#    run_pa("base_lf"); run_pa("film")
#    # 스케일 튜닝: run_pa("film", film_scale=0.3) 또는 1.0
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
SAVE_DIR  = "/content/drive/MyDrive/mitbih/ablation_step3b"

DS1_IDS=[101,106,108,109,112,114,115,116,118,119,122,124,201,203,205,207,208,209,215,220,223,230]
DS2_IDS=[100,103,105,111,113,117,121,123,200,202,210,212,213,214,219,221,222,228,231,232,233,234]
SEEDS=[1000,1001,1002,1003,1004]


class Cfg:
    n_leads=2; beat_len=300; feat_dim=26; n_classes=3; emb_dim=64
    n_proto=32
    class_w=(1.0,3.0,1.5); lr=1e-3; epochs=15; batch=512
    val_split="gss"
    label_free_ref=True
    patient_adapt=True
    # ---- [STEP 3b] 바운드 FiLM ----
    film_scale=0.5          # γ 진폭 한계 (±0.5 → (1+γ)∈[0.5,1.5])
    film_bias_scale=0.5     # β 진폭 한계


# ─────────── 모델 ───────────
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
    def __init__(self,cfg):
        super().__init__(); self.cfg=cfg; self.patient_adapt=cfg.patient_adapt
        self.film_scale=cfg.film_scale; self.film_bias_scale=cfg.film_bias_scale
        self.encoder=CNNEncoder(cfg)
        self.siamese=SiameseContrast(cfg.emb_dim,cfg.emb_dim)
        self.gate=GatedResidual(cfg.emb_dim)
        self.proto=PrototypeBank(cfg.emb_dim,cfg.n_proto)
        self.feat_mlp=FeatureMLP(cfg.feat_dim,cfg.emb_dim)
        self.cls_hidden=nn.Sequential(nn.Linear(cfg.emb_dim*3,cfg.emb_dim),nn.ReLU())
        self.cls_out=nn.Linear(cfg.emb_dim,cfg.n_classes)
        self.patient_head=nn.Sequential(nn.Linear(cfg.emb_dim,cfg.emb_dim),nn.ReLU())
        self.film=nn.Linear(cfg.emb_dim,cfg.emb_dim*2)
        nn.init.zeros_(self.film.weight); nn.init.zeros_(self.film.bias)   # 시작=항등
        self.proj_head=nn.Sequential(nn.Linear(cfg.emb_dim,cfg.emb_dim),nn.ReLU(),nn.Linear(cfg.emb_dim,128))
    def forward(self,beat,ref,feats,return_emb=False):
        z1=self.encoder(beat); z2=self.encoder(ref)
        zb=self.siamese(z1,z2); z=self.gate(z1,zb)
        z_proto=self.proto(z); z_feat=self.feat_mlp(feats)
        h=self.cls_hidden(torch.cat([z,z_proto,z_feat],dim=-1))
        if self.patient_adapt:
            g=self.patient_head(z2)
            graw,braw=self.film(g).chunk(2,dim=-1)
            gamma=self.film_scale*torch.tanh(graw)          # ★ 폭주 제거(바운드)
            beta =self.film_bias_scale*torch.tanh(braw)
            h=(1.0+gamma)*h+beta
        logits=self.cls_out(h)
        if return_emb: return logits,F.normalize(self.proj_head(z),dim=-1)
        return logits


def make_cls_loss(cfg,device):
    return nn.CrossEntropyLoss(weight=torch.tensor(cfg.class_w,dtype=torch.float32,device=device))

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

def per_patient_S_auc(probs,y,pid,min_s=5):
    """환자마다 제 기준(그 환자 beat만)으로 S ROC-AUC → 평균. 사장님 가설의 저울."""
    aucs=[]
    for p in np.unique(pid):
        m=pid==p; yy=(y[m]==1).astype(int)
        if yy.sum()<min_s or yy.sum()==m.sum(): continue
        aucs.append(roc_auc_score(yy,probs[m,1]))
    return (float(np.mean(aucs)) if aucs else float("nan")), len(aucs)

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
    b1,r1,ft1,y1,p1=ds1; b2,r2,ft2,y2,p2=ds2
    gss=GroupShuffleSplit(n_splits=1,test_size=0.2,random_state=seed)
    tr_idx,va_idx=next(gss.split(ft1,y1,groups=p1))
    sc=RobustScaler().fit(ft1[tr_idx])
    f1=np.nan_to_num(sc.transform(ft1),posinf=0,neginf=0).astype("float32")
    f2=np.nan_to_num(sc.transform(ft2),posinf=0,neginf=0).astype("float32")
    tr=(b1[tr_idx],r1[tr_idx],f1[tr_idx],y1[tr_idx]); va=(b1[va_idx],r1[va_idx],f1[va_idx],y1[va_idx])
    model=CNNBasePSA2PA(cfg).to(device)
    model=train(model,_loader(tr,cfg.batch,True),_loader(va,cfg.batch,False),cfg,device)
    probs,ys=evaluate(model,_loader((b2,r2,f2,y2),cfg.batch,False),device)
    return probs,ys,p2


PRESETS={
    "base_lf": dict(patient_adapt=False, label_free_ref=True),
    "film":    dict(patient_adapt=True,  label_free_ref=True),
}

def run_pa(tag, seeds=None, **override):
    assert tag in PRESETS
    cfg=Cfg()
    for k,v in {**PRESETS[tag], **override}.items(): setattr(cfg,k,v)
    seeds=seeds or SEEDS; device="cuda" if torch.cuda.is_available() else "cpu"
    out=os.path.join(SAVE_DIR,tag); os.makedirs(out,exist_ok=True)
    print(f"===== {tag} =====  patient_adapt={cfg.patient_adapt} film_scale={cfg.film_scale} "
          f"label_free_ref={cfg.label_free_ref}  device={device}")
    beats,refs,feats,y,pid=load_data(cfg)
    ds1=subset((beats,refs,feats,y,pid),np.isin(pid,DS1_IDS))
    ds2=subset((beats,refs,feats,y,pid),np.isin(pid,DS2_IDS))
    rows=[]; pp_rows=[]; probs_list=[]; y_ref=None; pid_ref=None
    for seed in seeds:
        print(f"  [seed {seed}]")
        probs,ys,pp=run_one_seed(cfg,seed,ds1,ds2,device)
        np.savez(os.path.join(out,f"cnn_{tag}_s{seed}.npz"),prob=probs,y=ys,pid=pp)
        m=metrics(probs,ys); ppa,ppn=per_patient_S_auc(probs,ys,pp)
        rows.append(m); pp_rows.append(ppa); probs_list.append(probs); y_ref=ys; pid_ref=pp
        print(f"    => DS2  전역S={m['S_PR_AUC']:.4f}  V={m['V_PR_AUC']:.4f}  |  환자별S_AUC={ppa:.4f}({ppn}명)")
    def agg(k): a=np.array([r[k] for r in rows]); return a.mean(),a.std()
    ens=np.stack(probs_list,0).mean(0); ens=ens/ens.sum(1,keepdims=True)
    me=metrics(ens,y_ref); mpp,mppn=per_patient_S_auc(ens,y_ref,pid_ref)
    ppa_arr=np.array(pp_rows)
    summary={"tag":tag,"config":{k:getattr(cfg,k) for k in
             ["patient_adapt","film_scale","film_bias_scale","label_free_ref","val_split","class_w","epochs"]},
             "seeds":list(seeds),"per_seed_global":rows,"per_seed_patientAUC":pp_rows,
             "ensemble_global":me,"ensemble_patientAUC":mpp}
    with open(os.path.join(out,f"summary_{tag}.json"),"w") as fp: json.dump(summary,fp,indent=2)
    ms,ss=agg("S_PR_AUC")
    print(f"\n----- {tag} -----")
    print(f"  [전역 지표]  개별 S={ms:.4f}±{ss:.4f}   ▶앙상블 S={me['S_PR_AUC']:.4f}  V={me['V_PR_AUC']:.4f}")
    print(f"  [환자별 지표] 개별 S_AUC={ppa_arr.mean():.4f}±{ppa_arr.std():.4f}   ▶앙상블 S_AUC={mpp:.4f}({mppn}명)")
    print(f"\n저장됨: {out}/")
    return summary
