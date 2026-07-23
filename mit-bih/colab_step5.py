# =============================================================================
#  colab_step5.py  —  [STEP 5] label-free win 통합: 깨끗한 ref + AdaBN(α 스윕)
#
#  지금까지의 label-free win(직교 2개):
#    · 자기예측 정상 ref (STEP3c base_clean): 전역S 0.476→0.504 (+0.028)
#    · AdaBN 환자적응     (STEP4)          : 전역S 0.475→0.516 (+0.041), 분산 반감
#      단 AdaBN은 V를 −0.04 깎음(과한 재정규화).
#
#  이번: 둘을 합치고 AdaBN 강도 α로 V 하락을 조절.
#    ref = 자기예측 정상(깨끗)         (label-free)
#    BN  = α·전역통계 + (1-α)·환자통계  (α=1 전역=none, α=0 완전 AdaBN)
#    → α 스윕으로 'S는 얻고 V는 지키는' 최적점 탐색. 전역/환자별 이중지표 + 앙상블.
#
#  실행:
#    exec(open('/content/drive/MyDrive/mitbih/colab_step5.py').read())
#    run_consol()                      # α=[1.0,0.5,0.25,0.0] 스윕
# =============================================================================
import os, json, copy
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from sklearn.preprocessing import RobustScaler
from sklearn.model_selection import GroupShuffleSplit
from sklearn.metrics import average_precision_score, precision_recall_fscore_support, roc_auc_score

DATA_PATH = "/content/drive/MyDrive/mitbih/mamba_data.npz"
SAVE_DIR  = "/content/drive/MyDrive/mitbih/ablation_step5"

DS1_IDS=[101,106,108,109,112,114,115,116,118,119,122,124,201,203,205,207,208,209,215,220,223,230]
DS2_IDS=[100,103,105,111,113,117,121,123,200,202,210,212,213,214,219,221,222,228,231,232,233,234]
SEEDS=[1000,1001,1002,1003,1004]
ALPHAS=[1.0,0.5,0.25,0.0]        # 1.0=none(전역BN) ... 0.0=완전 AdaBN


class Cfg:
    n_leads=2; beat_len=300; feat_dim=26; n_classes=3; emb_dim=64; n_proto=32
    class_w=(1.0,3.0,1.5); lr=1e-3; epochs=15; batch=512; bootstrap_epochs=8
    selfpred_q=0.5


# ─────────── 모델 (원본 base_psa2) ───────────
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
        super().__init__()
        self.encoder=CNNEncoder(cfg); self.siamese=SiameseContrast(cfg.emb_dim,cfg.emb_dim)
        self.gate=GatedResidual(cfg.emb_dim); self.proto=PrototypeBank(cfg.emb_dim,cfg.n_proto)
        self.feat_mlp=FeatureMLP(cfg.feat_dim,cfg.emb_dim)
        self.classifier=nn.Sequential(nn.Linear(cfg.emb_dim*3,cfg.emb_dim),nn.ReLU(),nn.Linear(cfg.emb_dim,cfg.n_classes))
    def forward(self,beat,ref,feats):
        z1=self.encoder(beat); z2=self.encoder(ref)
        zb=self.siamese(z1,z2); z=self.gate(z1,zb)
        return self.classifier(torch.cat([z,self.proto(z),self.feat_mlp(feats)],dim=-1))


def make_cls_loss(cfg,device):
    return nn.CrossEntropyLoss(weight=torch.tensor(cfg.class_w,dtype=torch.float32,device=device))

def load_raw():
    d=np.load(DATA_PATH); return d["beat"],d["feats"],d["y"],d["pid"]

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
def predict_global(model,beats,refs,feats,device,batch=4096):
    model.eval(); out=[]
    for i in range(0,len(beats),batch):
        b=torch.from_numpy(beats[i:i+batch]).to(device); r=torch.from_numpy(refs[i:i+batch]).to(device)
        f=torch.from_numpy(feats[i:i+batch]).to(device)
        out.append(torch.softmax(model(b,r,f),-1).cpu().numpy())
    return np.concatenate(out)

@torch.no_grad()
def predict_adabn_alpha(model,beats,refs,feats,pid,device,alpha):
    """BN = α·전역 + (1-α)·환자.  α=1 → none, α=0 → 완전 AdaBN. label-free."""
    if alpha>=1.0:
        return predict_global(model,beats,refs,feats,device)
    gstats={n:(m.running_mean.clone(),m.running_var.clone())
            for n,m in model.named_modules() if isinstance(m,nn.BatchNorm1d)}
    probs=np.zeros((len(beats),3),dtype=np.float32)
    for p in np.unique(pid):
        idx=np.where(pid==p)[0]
        m=copy.deepcopy(model)
        for mod in m.modules():
            if isinstance(mod,nn.BatchNorm1d): mod.reset_running_stats(); mod.momentum=None; mod.train()
        b=torch.from_numpy(beats[idx]).to(device); r=torch.from_numpy(refs[idx]).to(device); f=torch.from_numpy(feats[idx]).to(device)
        m(b,r,f)                                             # 환자 통계 누적
        for n,mod in m.named_modules():
            if isinstance(mod,nn.BatchNorm1d):
                gm,gv=gstats[n]
                mod.running_mean.copy_(alpha*gm+(1-alpha)*mod.running_mean)
                mod.running_var.copy_(alpha*gv+(1-alpha)*mod.running_var)
        m.eval(); probs[idx]=torch.softmax(m(b,r,f),-1).cpu().numpy()
    return probs

def selfpred_normal_ref(model,beats,refs0,feats,pid,device,q=0.5):
    pnorm=predict_global(model,beats,refs0,feats,device)[:,0]
    ref=np.empty_like(beats)
    for p in np.unique(pid):
        m=np.where(pid==p)[0]; k=max(5,int(q*len(m)))
        idx=m[np.argsort(-pnorm[m])[:k]]; ref[m]=np.median(beats[idx],axis=0,keepdims=True)
    return ref.astype("float32")

def metrics(probs,y):
    s=average_precision_score((y==1).astype(int),probs[:,1]); v=average_precision_score((y==2).astype(int),probs[:,2])
    n=average_precision_score((y==0).astype(int),probs[:,0])
    return {"S_PR_AUC":float(s),"V_PR_AUC":float(v),"macro_PR_AUC":float((n+s+v)/3)}

def per_patient_S_auc(probs,y,pid,min_s=5):
    a=[]
    for p in np.unique(pid):
        m=pid==p; yy=(y[m]==1).astype(int)
        if yy.sum()<min_s or yy.sum()==m.sum(): continue
        a.append(roc_auc_score(yy,probs[m,1]))
    return (float(np.mean(a)) if a else float("nan")),len(a)

def train(model,tr,va,cfg,device,epochs):
    opt=torch.optim.AdamW(model.parameters(),lr=cfg.lr,weight_decay=1e-4)
    cls=make_cls_loss(cfg,device); best=-1; bs=None; tl=_loader(tr,cfg.batch,True)
    for ep in range(epochs):
        model.train()
        for beat,ref,feats,y in tl:
            beat,ref,feats,y=(t.to(device) for t in (beat,ref,feats,y)); opt.zero_grad()
            loss=cls(model(beat,ref,feats),y); loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(),1.0); opt.step()
        pv=predict_global(model,va[0],va[1],va[2],device); m=metrics(pv,va[3])
        sc=0.5*(m["S_PR_AUC"]+m["V_PR_AUC"])
        if sc>best: best=sc; bs={k:v.cpu() for k,v in model.state_dict().items()}
    if bs: model.load_state_dict(bs)
    return model

def run_consol(seeds=None, alphas=None, **override):
    cfg=Cfg()
    for k,v in override.items(): setattr(cfg,k,v)
    seeds=seeds or SEEDS; alphas=alphas or ALPHAS
    device="cuda" if torch.cuda.is_available() else "cpu"; os.makedirs(SAVE_DIR,exist_ok=True)
    print(f"===== STEP5 통합 =====  깨끗한ref(q={cfg.selfpred_q}) + AdaBN α스윕{alphas}  device={device}")
    beats,feats,y,pid=load_raw(); ref0=allbeat_median_ref(beats,pid)
    m1=np.isin(pid,DS1_IDS); m2=np.isin(pid,DS2_IDS)
    b1,ft1,y1,p1,r01=beats[m1],feats[m1],y[m1],pid[m1],ref0[m1]
    b2,ft2,y2,p2,r02=beats[m2],feats[m2],y[m2],pid[m2],ref0[m2]
    probs_by_alpha={a:[] for a in alphas}
    for seed in seeds:
        torch.manual_seed(seed); np.random.seed(seed)
        tr_idx,va_idx=next(GroupShuffleSplit(1,test_size=0.2,random_state=seed).split(ft1,y1,groups=p1))
        sc=RobustScaler().fit(ft1[tr_idx])
        f1=np.nan_to_num(sc.transform(ft1),posinf=0,neginf=0).astype("float32")
        f2=np.nan_to_num(sc.transform(ft2),posinf=0,neginf=0).astype("float32")
        # Stage1 부트스트랩 → Stage2 깨끗한 ref
        M0=CNNBasePSA2(cfg).to(device)
        M0=train(M0,(b1[tr_idx],r01[tr_idx],f1[tr_idx],y1[tr_idx]),(b1[va_idx],r01[va_idx],f1[va_idx],y1[va_idx]),cfg,device,cfg.bootstrap_epochs)
        r1c=selfpred_normal_ref(M0,b1,r01,f1,p1,device,cfg.selfpred_q)
        r2c=selfpred_normal_ref(M0,b2,r02,f2,p2,device,cfg.selfpred_q)
        # Stage3 본모델(깨끗한 ref)
        M1=CNNBasePSA2(cfg).to(device)
        M1=train(M1,(b1[tr_idx],r1c[tr_idx],f1[tr_idx],y1[tr_idx]),(b1[va_idx],r1c[va_idx],f1[va_idx],y1[va_idx]),cfg,device,cfg.epochs)
        for a in alphas:
            probs_by_alpha[a].append(predict_adabn_alpha(M1,b2,r2c,f2,p2,device,a))
        print(f"  [seed {seed}] 완료")
    print(f"\n{'='*70}\n α(BN)  |  앙상블 전역S   V      macro  |  환자별S_AUC")
    summary={}
    for a in alphas:
        ens=np.stack(probs_by_alpha[a],0).mean(0); ens=ens/ens.sum(1,keepdims=True)
        me=metrics(ens,y2); mpp,_=per_patient_S_auc(ens,y2,p2)
        np.savez(os.path.join(SAVE_DIR,f"ens_alpha{a}.npz"),prob=ens,y=y2,pid=p2)
        summary[str(a)]={"ensemble":me,"ensemble_patientAUC":mpp}
        tagname="none " if a>=1.0 else ("adabn" if a<=0.0 else f"α={a}")
        print(f"  {a:.2f} {tagname:5s}|   {me['S_PR_AUC']:.4f}    {me['V_PR_AUC']:.4f}  {me['macro_PR_AUC']:.4f} |   {mpp:.4f}")
    with open(os.path.join(SAVE_DIR,"summary_step5.json"),"w") as fp: json.dump(summary,fp,indent=2)
    best_a=max(alphas,key=lambda a:summary[str(a)]["ensemble"]["S_PR_AUC"])
    print(f"\n▶ 전역S 최고: α={best_a}  S={summary[str(best_a)]['ensemble']['S_PR_AUC']:.4f} "
          f"V={summary[str(best_a)]['ensemble']['V_PR_AUC']:.4f}")
    print(f"  (비교: STEP4 AdaBN-only 0.516 / base_clean 0.504 / leaky A_gss 0.649)")
    print(f"저장됨: {SAVE_DIR}/")
    return summary
