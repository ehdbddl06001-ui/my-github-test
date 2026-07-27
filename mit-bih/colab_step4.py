# =============================================================================
#  colab_step4.py  —  [STEP 4] 파라미터-free 환자적응 (AdaBN)
#
#  STEP3 계열 결론: 학습된 환자적응(FiLM)은 22명 과적합으로 기각.
#  이번: 학습되는 환자→파라미터 매핑이 '전혀 없는' 적응 → 과적합 불가능.
#    AdaBN(Adaptive BatchNorm): 학습 가중치 고정, 테스트 때 각 환자 본인 beat로
#    BatchNorm 통계(mean/var)만 갱신 → 그 환자 분포에 정렬. 라벨 미사용.
#
#  설계: 같은 학습모델 M 하나에서
#    · none  : 전역 BN(DS1 학습 통계)으로 DS2 예측 (baseline)
#    · adabn : 환자별 BN 통계로 DS2 예측 (파라미터-free 적응)
#    두 예측을 나란히 → AdaBN 순효과만 분리. 전역/환자별 이중지표 + 앙상블.
#
#  실행:
#    exec(open('/content/drive/MyDrive/mitbih/colab_step4.py').read())
#    run_adapt()                    # none vs adabn 동시 비교
#    run_adapt(label_free_ref=True) # (기본) 라벨-프리 ref
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
SAVE_DIR  = "/content/drive/MyDrive/mitbih/ablation_step4"

DS1_IDS=[101,106,108,109,112,114,115,116,118,119,122,124,201,203,205,207,208,209,215,220,223,230]
DS2_IDS=[100,103,105,111,113,117,121,123,200,202,210,212,213,214,219,221,222,228,231,232,233,234]
SEEDS=[1000,1001,1002,1003,1004]


class Cfg:
    n_leads=2; beat_len=300; feat_dim=26; n_classes=3; emb_dim=64
    n_proto=32
    class_w=(1.0,3.0,1.5); lr=1e-3; epochs=15; batch=512
    val_split="gss"
    label_free_ref=True


# ─────────── 모델 (원본 base_psa2, FiLM 없음) ───────────
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
    def forward(self,beat,ref,feats):
        z1=self.encoder(beat); z2=self.encoder(ref)
        zb=self.siamese(z1,z2); z=self.gate(z1,zb)
        z_proto=self.proto(z); z_feat=self.feat_mlp(feats)
        return self.classifier(torch.cat([z,z_proto,z_feat],dim=-1))


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
def predict_adabn(model,beats,refs,feats,pid,device):
    """각 환자 본인 beat로 BN 통계만 갱신 후 그 환자 예측 (파라미터-free, 라벨 미사용)."""
    probs_all=np.zeros((len(beats),3),dtype=np.float32)
    for p in np.unique(pid):
        idx=np.where(pid==p)[0]
        m=copy.deepcopy(model)
        for mod in m.modules():                       # BN을 환자통계 누적 모드로
            if isinstance(mod,nn.BatchNorm1d):
                mod.reset_running_stats(); mod.momentum=None; mod.train()
        b=torch.from_numpy(beats[idx]).to(device); r=torch.from_numpy(refs[idx]).to(device)
        f=torch.from_numpy(feats[idx]).to(device)
        m(b,r,f)                                       # 통계 누적(한 번의 forward=환자 전체)
        m.eval()                                       # 갱신된 환자별 BN 통계로 예측
        probs_all[idx]=torch.softmax(m(b,r,f),-1).cpu().numpy()
    return probs_all

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

def train(model,tr,va,cfg,device):
    opt=torch.optim.AdamW(model.parameters(),lr=cfg.lr,weight_decay=1e-4)
    cls_loss=make_cls_loss(cfg,device); best=-1; best_state=None
    tr_loader=_loader(tr,cfg.batch,True)
    for ep in range(cfg.epochs):
        model.train()
        for beat,ref,feats,y in tr_loader:
            beat,ref,feats,y=(t.to(device) for t in (beat,ref,feats,y)); opt.zero_grad()
            loss=cls_loss(model(beat,ref,feats),y)
            loss.backward(); torch.nn.utils.clip_grad_norm_(model.parameters(),1.0); opt.step()
        pv=predict_global(model,va[0],va[1],va[2],device); m=metrics(pv,va[3])
        score=0.5*(m["S_PR_AUC"]+m["V_PR_AUC"])
        if score>best: best=score; best_state={k:v.cpu() for k,v in model.state_dict().items()}
    if best_state: model.load_state_dict(best_state)
    return model

def run_adapt(seeds=None, **override):
    cfg=Cfg()
    for k,v in override.items(): setattr(cfg,k,v)
    seeds=seeds or SEEDS; device="cuda" if torch.cuda.is_available() else "cpu"
    os.makedirs(SAVE_DIR,exist_ok=True)
    print(f"===== STEP4 AdaBN =====  label_free_ref={cfg.label_free_ref}  device={device}")
    beats,refs,feats,y,pid=load_data(cfg)
    ds1=subset((beats,refs,feats,y,pid),np.isin(pid,DS1_IDS))
    ds2=subset((beats,refs,feats,y,pid),np.isin(pid,DS2_IDS))
    b1,r1,ft1,y1,p1=ds1; b2,r2,ft2,y2,p2=ds2
    res={"none":{"g":[],"pp":[],"probs":[]}, "adabn":{"g":[],"pp":[],"probs":[]}}
    for seed in seeds:
        torch.manual_seed(seed); np.random.seed(seed)
        tr_idx,va_idx=next(GroupShuffleSplit(1,test_size=0.2,random_state=seed).split(ft1,y1,groups=p1))
        sc=RobustScaler().fit(ft1[tr_idx])
        f1=np.nan_to_num(sc.transform(ft1),posinf=0,neginf=0).astype("float32")
        f2=np.nan_to_num(sc.transform(ft2),posinf=0,neginf=0).astype("float32")
        M=CNNBasePSA2(cfg).to(device)
        M=train(M,(b1[tr_idx],r1[tr_idx],f1[tr_idx],y1[tr_idx]),
                (b1[va_idx],r1[va_idx],f1[va_idx],y1[va_idx]),cfg,device)
        pn=predict_global(M,b2,r2,f2,device)          # none
        pa=predict_adabn(M,b2,r2,f2,p2,device)        # adabn (같은 가중치)
        for tag,pr in [("none",pn),("adabn",pa)]:
            m=metrics(pr,y2); ppa,ppn=per_patient_S_auc(pr,y2,p2)
            res[tag]["g"].append(m); res[tag]["pp"].append(ppa); res[tag]["probs"].append(pr)
        print(f"  [seed {seed}]  none: 전역S={res['none']['g'][-1]['S_PR_AUC']:.4f} 환자별={res['none']['pp'][-1]:.4f}"
              f"  |  adabn: 전역S={res['adabn']['g'][-1]['S_PR_AUC']:.4f} 환자별={res['adabn']['pp'][-1]:.4f}")
    summary={}
    print(f"\n{'='*64}")
    for tag in ["none","adabn"]:
        g=res[tag]["g"]; pp=np.array(res[tag]["pp"])
        Sarr=np.array([r["S_PR_AUC"] for r in g])
        ens=np.stack(res[tag]["probs"],0).mean(0); ens=ens/ens.sum(1,keepdims=True)
        me=metrics(ens,y2); mpp,mppn=per_patient_S_auc(ens,y2,p2)
        np.savez(os.path.join(SAVE_DIR,f"ens_{tag}.npz"),prob=ens,y=y2,pid=p2)
        summary[tag]={"individual_S_mean":float(Sarr.mean()),"individual_S_std":float(Sarr.std()),
                      "ensemble_global":me,"individual_patientAUC":float(pp.mean()),"ensemble_patientAUC":mpp}
        print(f"[{tag:5s}]  전역: 개별S={Sarr.mean():.4f}±{Sarr.std():.4f}  ▶앙상블S={me['S_PR_AUC']:.4f} V={me['V_PR_AUC']:.4f}"
              f"   |  환자별: 개별={pp.mean():.4f}  ▶앙상블={mpp:.4f}({mppn}명)")
    with open(os.path.join(SAVE_DIR,"summary_step4.json"),"w") as fp: json.dump(summary,fp,indent=2)
    dg=summary["adabn"]["ensemble_global"]["S_PR_AUC"]-summary["none"]["ensemble_global"]["S_PR_AUC"]
    dp=summary["adabn"]["ensemble_patientAUC"]-summary["none"]["ensemble_patientAUC"]
    print(f"\n▶ AdaBN 순효과(앙상블):  전역S {dg:+.4f}   환자별 {dp:+.4f}   "
          f"{'✅ 파라미터-free 적응이 기여' if (dg>0 or dp>0) else '⚠ 이득 없음'}")
    print(f"저장됨: {SAVE_DIR}/")
    return summary
