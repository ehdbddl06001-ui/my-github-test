# =============================================================================
#  colab_step3c.py  —  [STEP 3c] 자기예측 정상비트로 강한 label-free g(patient)
#
#  STEP3b 결론: 바운드 FiLM은 폭주는 잡았으나 환자적응 순효과가 미미(+0.004).
#               원인 = g(patient)가 약함. all-beat median ref 는 그 환자의 V·S 이상
#               비트까지 섞여 '정상 기준'으로 오염돼 있음.
#
#  이번 처방: g(patient) 를 '자기예측 정상비트'로 강화 (DS2 라벨 미사용).
#   Stage1  부트스트랩 M0 : all-beat median ref 로 baseline 학습
#   Stage2  깨끗한 ref     : M0 이 매긴 P(normal) 상위 q(=0.5) beat 만 골라 median
#                           → 그 환자의 '진짜 정상 형태' (라벨 대신 자기예측)
#   Stage3  본모델 M1     : 깨끗한 ref 로 재학습. g(patient)=encoder(clean_ref)
#
#  비교(같은 깨끗한 ref 위에서):
#    base_clean (FiLM 없음)  vs  film_clean (FiLM 환자적응)
#    → film_clean 이 base_clean 을 (전역 or 환자별에서) 유의미하게 이기면 가설 입증.
#
#  실행:
#    exec(open('/content/drive/MyDrive/mitbih/colab_step3c.py').read())
#    run_sp("base_clean"); run_sp("film_clean")
#    # 자기예측 비율 튜닝: run_sp("film_clean", selfpred_q=0.3)
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
SAVE_DIR  = "/content/drive/MyDrive/mitbih/ablation_step3c"

DS1_IDS=[101,106,108,109,112,114,115,116,118,119,122,124,201,203,205,207,208,209,215,220,223,230]
DS2_IDS=[100,103,105,111,113,117,121,123,200,202,210,212,213,214,219,221,222,228,231,232,233,234]
SEEDS=[1000,1001,1002,1003,1004]


class Cfg:
    n_leads=2; beat_len=300; feat_dim=26; n_classes=3; emb_dim=64
    n_proto=32
    class_w=(1.0,3.0,1.5); lr=1e-3; epochs=15; batch=512
    bootstrap_epochs=8            # M0(부트스트랩)는 짧게
    val_split="gss"
    patient_adapt=True
    film_scale=0.5; film_bias_scale=0.5
    selfpred_q=0.5                # 각 환자 beat 중 P(normal) 상위 비율만 정상으로 채택


# ─────────── 모델 (STEP3b 바운드 FiLM 동일) ───────────
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
    def __init__(self,cfg,patient_adapt):
        super().__init__(); self.patient_adapt=patient_adapt
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
        nn.init.zeros_(self.film.weight); nn.init.zeros_(self.film.bias)
        self.proj_head=nn.Sequential(nn.Linear(cfg.emb_dim,cfg.emb_dim),nn.ReLU(),nn.Linear(cfg.emb_dim,128))
    def forward(self,beat,ref,feats):
        z1=self.encoder(beat); z2=self.encoder(ref)
        zb=self.siamese(z1,z2); z=self.gate(z1,zb)
        z_proto=self.proto(z); z_feat=self.feat_mlp(feats)
        h=self.cls_hidden(torch.cat([z,z_proto,z_feat],dim=-1))
        if self.patient_adapt:
            g=self.patient_head(z2)
            graw,braw=self.film(g).chunk(2,dim=-1)
            gamma=self.film_scale*torch.tanh(graw); beta=self.film_bias_scale*torch.tanh(braw)
            h=(1.0+gamma)*h+beta
        return self.cls_out(h)


def make_cls_loss(cfg,device):
    return nn.CrossEntropyLoss(weight=torch.tensor(cfg.class_w,dtype=torch.float32,device=device))

def load_raw():
    d=np.load(DATA_PATH)
    return d["beat"],d["feats"],d["y"],d["pid"]

def allbeat_median_ref(beats,pid):
    ref=np.empty_like(beats)
    for p in np.unique(pid):
        m=pid==p; ref[m]=np.median(beats[m],axis=0,keepdims=True)
    return ref.astype("float32")

def subset(arrs,mask): return tuple(a[mask] for a in arrs)

def _loader(arrs,batch,shuffle):
    ds=torch.utils.data.TensorDataset(*[torch.from_numpy(np.asarray(a)) for a in arrs])
    return torch.utils.data.DataLoader(ds,batch_size=batch,shuffle=shuffle)

@torch.no_grad()
def predict_probs(model,beats,refs,feats,device,batch=4096):
    model.eval(); out=[]
    for i in range(0,len(beats),batch):
        b=torch.from_numpy(beats[i:i+batch]).to(device); r=torch.from_numpy(refs[i:i+batch]).to(device)
        f=torch.from_numpy(feats[i:i+batch]).to(device)
        out.append(torch.softmax(model(b,r,f),-1).cpu().numpy())
    return np.concatenate(out)

def selfpred_normal_ref(model, beats, refs0, feats, pid, device, q=0.5):
    """M0 이 매긴 P(normal) 상위 q 비율 beat 로 환자별 정상 템플릿 (label-free)."""
    probs=predict_probs(model,beats,refs0,feats,device); pnorm=probs[:,0]
    ref_new=np.empty_like(beats)
    for p in np.unique(pid):
        m=np.where(pid==p)[0]
        k=max(5,int(q*len(m)))
        idx=m[np.argsort(-pnorm[m])[:k]]              # 가장 정상같은 k개
        ref_new[m]=np.median(beats[idx],axis=0,keepdims=True)
    return ref_new.astype("float32")

def metrics(probs,y):
    s=average_precision_score((y==1).astype(int),probs[:,1])
    v=average_precision_score((y==2).astype(int),probs[:,2])
    n=average_precision_score((y==0).astype(int),probs[:,0])
    pred=probs.argmax(1); p,r,f,_=precision_recall_fscore_support(y,pred,labels=[0,1,2],zero_division=0)
    return {"S_PR_AUC":float(s),"V_PR_AUC":float(v),"macro_PR_AUC":float((n+s+v)/3),
            "S_Se":float(r[1]),"S_P":float(p[1]),"S_F1":float(f[1])}

def per_patient_S_auc(probs,y,pid,min_s=5):
    aucs=[]
    for p in np.unique(pid):
        m=pid==p; yy=(y[m]==1).astype(int)
        if yy.sum()<min_s or yy.sum()==m.sum(): continue
        aucs.append(roc_auc_score(yy,probs[m,1]))
    return (float(np.mean(aucs)) if aucs else float("nan")),len(aucs)

def train(model,tr,va,cfg,device,epochs):
    opt=torch.optim.AdamW(model.parameters(),lr=cfg.lr,weight_decay=1e-4)
    cls_loss=make_cls_loss(cfg,device); best=-1; best_state=None
    tr_loader=_loader(tr,cfg.batch,True)
    for ep in range(epochs):
        model.train()
        for beat,ref,feats,y in tr_loader:
            beat,ref,feats,y=(t.to(device) for t in (beat,ref,feats,y)); opt.zero_grad()
            loss=cls_loss(model(beat,ref,feats),y)
            loss.backward(); torch.nn.utils.clip_grad_norm_(model.parameters(),1.0); opt.step()
        pv=predict_probs(model,va[0],va[1],va[2],device); m=metrics(pv,va[3])
        score=0.5*(m["S_PR_AUC"]+m["V_PR_AUC"])
        if score>best: best=score; best_state={k:v.cpu() for k,v in model.state_dict().items()}
    if best_state: model.load_state_dict(best_state)
    return model

def run_one_seed(cfg,seed,dsraw,device):
    beats,feats,y,pid,ref0=dsraw
    torch.manual_seed(seed); np.random.seed(seed)
    m1=np.isin(pid,DS1_IDS); m2=np.isin(pid,DS2_IDS)
    b1,ft1,y1,p1,r01=beats[m1],feats[m1],y[m1],pid[m1],ref0[m1]
    b2,ft2,y2,p2,r02=beats[m2],feats[m2],y[m2],pid[m2],ref0[m2]
    gss=GroupShuffleSplit(n_splits=1,test_size=0.2,random_state=seed)
    tr_idx,va_idx=next(gss.split(ft1,y1,groups=p1))
    sc=RobustScaler().fit(ft1[tr_idx])
    f1=np.nan_to_num(sc.transform(ft1),posinf=0,neginf=0).astype("float32")
    f2=np.nan_to_num(sc.transform(ft2),posinf=0,neginf=0).astype("float32")

    # --- Stage1: 부트스트랩 M0 (all-beat median ref, 적응 없음) ---
    M0=CNNBasePSA2PA(cfg,patient_adapt=False).to(device)
    M0=train(M0,(b1[tr_idx],r01[tr_idx],f1[tr_idx],y1[tr_idx]),
             (b1[va_idx],r01[va_idx],f1[va_idx],y1[va_idx]),cfg,device,cfg.bootstrap_epochs)

    # --- Stage2: 자기예측 정상 ref (DS1/DS2 모두 label-free) ---
    r1c=selfpred_normal_ref(M0,b1,r01,f1,p1,device,cfg.selfpred_q)
    r2c=selfpred_normal_ref(M0,b2,r02,f2,p2,device,cfg.selfpred_q)   # DS2도 라벨 없이 자기예측만

    # --- Stage3: 본모델 M1 (깨끗한 ref) ---
    M1=CNNBasePSA2PA(cfg,patient_adapt=cfg.patient_adapt).to(device)
    M1=train(M1,(b1[tr_idx],r1c[tr_idx],f1[tr_idx],y1[tr_idx]),
             (b1[va_idx],r1c[va_idx],f1[va_idx],y1[va_idx]),cfg,device,cfg.epochs)
    probs=predict_probs(M1,b2,r2c,f2,device)
    return probs,y2,p2


PRESETS={
    "base_clean": dict(patient_adapt=False),   # 깨끗한 ref, FiLM 없음 (ref 개선 효과만)
    "film_clean": dict(patient_adapt=True),    # 깨끗한 ref + FiLM 환자적응 (가설 시험)
}

def run_sp(tag, seeds=None, **override):
    assert tag in PRESETS
    cfg=Cfg()
    for k,v in {**PRESETS[tag], **override}.items(): setattr(cfg,k,v)
    seeds=seeds or SEEDS; device="cuda" if torch.cuda.is_available() else "cpu"
    out=os.path.join(SAVE_DIR,tag); os.makedirs(out,exist_ok=True)
    print(f"===== {tag} =====  patient_adapt={cfg.patient_adapt} selfpred_q={cfg.selfpred_q} "
          f"film_scale={cfg.film_scale}  device={device}")
    beats,feats,y,pid=load_raw(); ref0=allbeat_median_ref(beats,pid)
    dsraw=(beats,feats,y,pid,ref0)
    rows=[]; pp_rows=[]; probs_list=[]; y_ref=None; pid_ref=None
    for seed in seeds:
        print(f"  [seed {seed}] Stage1 M0 → Stage2 self-pred ref → Stage3 M1 ...")
        probs,ys,pp=run_one_seed(cfg,seed,dsraw,device)
        np.savez(os.path.join(out,f"cnn_{tag}_s{seed}.npz"),prob=probs,y=ys,pid=pp)
        m=metrics(probs,ys); ppa,ppn=per_patient_S_auc(probs,ys,pp)
        rows.append(m); pp_rows.append(ppa); probs_list.append(probs); y_ref=ys; pid_ref=pp
        print(f"    => DS2  전역S={m['S_PR_AUC']:.4f}  V={m['V_PR_AUC']:.4f}  |  환자별S_AUC={ppa:.4f}({ppn}명)")
    def agg(k): a=np.array([r[k] for r in rows]); return a.mean(),a.std()
    ens=np.stack(probs_list,0).mean(0); ens=ens/ens.sum(1,keepdims=True)
    me=metrics(ens,y_ref); mpp,mppn=per_patient_S_auc(ens,y_ref,pid_ref); ppa_arr=np.array(pp_rows)
    summary={"tag":tag,"config":{k:getattr(cfg,k) for k in
             ["patient_adapt","selfpred_q","film_scale","bootstrap_epochs","epochs"]},
             "seeds":list(seeds),"per_seed_global":rows,"per_seed_patientAUC":pp_rows,
             "ensemble_global":me,"ensemble_patientAUC":mpp}
    with open(os.path.join(out,f"summary_{tag}.json"),"w") as fp: json.dump(summary,fp,indent=2)
    ms,ss=agg("S_PR_AUC")
    print(f"\n----- {tag} -----")
    print(f"  [전역 지표]  개별 S={ms:.4f}±{ss:.4f}   ▶앙상블 S={me['S_PR_AUC']:.4f}  V={me['V_PR_AUC']:.4f}")
    print(f"  [환자별 지표] 개별 S_AUC={ppa_arr.mean():.4f}±{ppa_arr.std():.4f}   ▶앙상블 S_AUC={mpp:.4f}({mppn}명)")
    print(f"\n저장됨: {out}/")
    return summary
