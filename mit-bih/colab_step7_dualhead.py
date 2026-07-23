# =============================================================================
#  colab_step7_dualhead.py  —  [STEP 7] 클래스별 분기: P파 attention(S) + temporal(V)
#
#  발견한 S/V 비대칭:
#    · V 신호 = 형태+이웃 리듬 문맥  → temporal(이웃 beat)이 도움 (STEP6 확인)
#    · S 신호 = 조기성(RR,이미 feats) + P파 형태 이상 → 이웃형태는 독, P파가 답
#      (SVEB=심방 이소성 → P파 모양 다름. 근데 avg-pool이 작은 P파를 씻어냄.)
#
#  처방(PDF ⑤ Attention/P-wave, 미탐색 항목 + 사장님 'QRS 숨은 P파' 아이디어):
#    · Attention pooling 인코더: avg-pool 옆에 시간축 attention-pool 추가 → P파 영역
#      에 가중 가능한 임베딩 z_att 산출.
#    · 클래스별 헤드로 신호 라우팅(서로 오염 방지):
#        N 헤드 = 공통          S 헤드 = 공통+P파attention(temporal 제외)
#        V 헤드 = 공통+temporal(P파 제외)
#
#  비교:  base(단일헤드, 현재 beat, avg-pool만)  vs  dual(클래스별 분기)
#  실행:
#    exec(open('/content/drive/MyDrive/mitbih/colab_step7_dualhead.py').read())
#    run_dual("base"); run_dual("dual")
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
SAVE_DIR  = "/content/drive/MyDrive/mitbih/ablation_step7"

DS1_IDS=[101,106,108,109,112,114,115,116,118,119,122,124,201,203,205,207,208,209,215,220,223,230]
DS2_IDS=[100,103,105,111,113,117,121,123,200,202,210,212,213,214,219,221,222,228,231,232,233,234]
SEEDS=[1000,1001,1002,1003,1004]


class Cfg:
    n_leads=2; beat_len=300; feat_dim=26; n_classes=3; emb_dim=64; n_proto=32
    class_w=(1.0,3.0,1.5); lr=1e-3; epochs=15; batch=512
    label_free_ref=True
    dual=True                       # True: 클래스별 분기(P파+temporal), False: 단일헤드 baseline


# ---- Attention-pooling 인코더 (avg + 시간축 attention) ----
class Encoder(nn.Module):
    def __init__(self,cfg):
        super().__init__()
        self.conv=nn.Sequential(
            nn.Conv1d(cfg.n_leads,32,7,padding=3), nn.BatchNorm1d(32), nn.ReLU(), nn.MaxPool1d(2),
            nn.Conv1d(32,64,5,padding=2),          nn.BatchNorm1d(64), nn.ReLU(), nn.MaxPool1d(2),
            nn.Conv1d(64,128,3,padding=1),         nn.BatchNorm1d(128),nn.ReLU(),
        )                                                  # [B,128,L] (풀링 전)
        self.proj=nn.Linear(128,cfg.emb_dim)               # avg-pool 경로
        self.att=nn.Linear(128,1)                          # 시간축 attention 점수
        self.proj_att=nn.Linear(128,cfg.emb_dim)           # attention-pool 경로(P파 집중 가능)
    def forward(self,wave,want_att=False):
        h=self.conv(wave)                                  # [B,128,L]
        z_avg=self.proj(h.mean(-1))
        if not want_att: return z_avg
        ht=h.transpose(1,2)                                # [B,L,128]
        w=torch.softmax(self.att(ht),dim=1)                # [B,L,1] 시간 가중
        z_att=self.proj_att((ht*w).sum(1))                 # [B,emb]
        return z_avg,z_att

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

class DualHeadNet(nn.Module):
    def __init__(self,cfg):
        super().__init__(); self.dual=cfg.dual; E=cfg.emb_dim
        self.encoder=Encoder(cfg)
        self.siamese=SiameseContrast(E,E); self.gate=GatedResidual(E)
        self.proto=PrototypeBank(E,cfg.n_proto); self.feat_mlp=FeatureMLP(cfg.feat_dim,E)
        self.common=nn.Sequential(nn.Linear(E*3,E),nn.ReLU())     # 공통 trunk [z,z_proto,z_feat]->E
        if cfg.dual:
            self.temporal_head=nn.Sequential(nn.Linear(E*2,E),nn.ReLU())  # V용 이웃문맥
            self.head_N=nn.Linear(E,1)
            self.head_S=nn.Linear(E*2,1)     # 공통 + P파 attention
            self.head_V=nn.Linear(E*2,1)     # 공통 + temporal
        else:
            self.classifier=nn.Linear(E,cfg.n_classes)
    def forward(self,beat,prev,nxt,ref,feats):
        if self.dual:
            z1,z_att=self.encoder(beat,want_att=True)      # z_att=P파 집중 가능
        else:
            z1=self.encoder(beat)
        z2=self.encoder(ref)
        zb=self.siamese(z1,z2); z=self.gate(z1,zb)
        hc=self.common(torch.cat([z,self.proto(z),self.feat_mlp(feats)],dim=-1))  # [B,E]
        if not self.dual:
            return self.classifier(hc)
        zp=self.encoder(prev); zn=self.encoder(nxt)
        z_temp=self.temporal_head(torch.cat([zp-z1,zn-z1],dim=-1))                # V용
        lN=self.head_N(hc)
        lS=self.head_S(torch.cat([hc,z_att],dim=-1))       # S: 공통 + P파 (temporal 없음)
        lV=self.head_V(torch.cat([hc,z_temp],dim=-1))      # V: 공통 + temporal (P파 없음)
        return torch.cat([lN,lS,lV],dim=-1)                # [B,3]


def make_cls_loss(cfg,device):
    return nn.CrossEntropyLoss(weight=torch.tensor(cfg.class_w,dtype=torch.float32,device=device))

def build_neighbors(beats,pid,t):
    prev=beats.copy(); nxt=beats.copy()
    for p in np.unique(pid):
        idx=np.where(pid==p)[0]; order=idx[np.argsort(t[idx],kind="stable")]
        prev[order[1:]]=beats[order[:-1]]; nxt[order[:-1]]=beats[order[1:]]
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

PRESETS={"base":dict(dual=False),"dual":dict(dual=True)}

def run_dual(tag, seeds=None, **override):
    assert tag in PRESETS
    cfg=Cfg()
    for k,v in {**PRESETS[tag],**override}.items(): setattr(cfg,k,v)
    seeds=seeds or SEEDS; device="cuda" if torch.cuda.is_available() else "cpu"
    out=os.path.join(SAVE_DIR,tag); os.makedirs(out,exist_ok=True)
    print(f"===== {tag} =====  dual={cfg.dual}  device={device}")
    beats,prev,nxt,refs,feats,y,pid=load_data(cfg)
    ds1=subset((beats,prev,nxt,refs,feats,y,pid),np.isin(pid,DS1_IDS))
    ds2=subset((beats,prev,nxt,refs,feats,y,pid),np.isin(pid,DS2_IDS))
    b1,pv1,nx1,r1,ft1,y1,p1=ds1; b2,pv2,nx2,r2,ft2,y2,p2=ds2
    print(f"params={sum(pp.numel() for pp in DualHeadNet(cfg).parameters()):,}")
    rows=[]; pp_rows=[]; probs_list=[]
    for seed in seeds:
        torch.manual_seed(seed); np.random.seed(seed)
        tr_idx,va_idx=next(GroupShuffleSplit(1,test_size=0.2,random_state=seed).split(ft1,y1,groups=p1))
        sc=RobustScaler().fit(ft1[tr_idx])
        f1=np.nan_to_num(sc.transform(ft1),posinf=0,neginf=0).astype("float32")
        f2=np.nan_to_num(sc.transform(ft2),posinf=0,neginf=0).astype("float32")
        tr=(b1[tr_idx],pv1[tr_idx],nx1[tr_idx],r1[tr_idx],f1[tr_idx],y1[tr_idx])
        va=(b1[va_idx],pv1[va_idx],nx1[va_idx],r1[va_idx],f1[va_idx],y1[va_idx])
        M=DualHeadNet(cfg).to(device); M=train(M,tr,va,cfg,device)
        pr=predict(M,b2,pv2,nx2,r2,f2,device)
        np.savez(os.path.join(out,f"cnn_{tag}_s{seed}.npz"),prob=pr,y=y2,pid=p2)
        m=metrics(pr,y2); ppa,ppn=per_patient_S_auc(pr,y2,p2)
        rows.append(m); pp_rows.append(ppa); probs_list.append(pr)
        print(f"  [seed {seed}]  전역S={m['S_PR_AUC']:.4f}  V={m['V_PR_AUC']:.4f}  환자별S_AUC={ppa:.4f}")
    Sarr=np.array([r["S_PR_AUC"] for r in rows]); Varr=np.array([r["V_PR_AUC"] for r in rows]); ppa_arr=np.array(pp_rows)
    ens=np.stack(probs_list,0).mean(0); ens=ens/ens.sum(1,keepdims=True)
    me=metrics(ens,y2); mpp,mppn=per_patient_S_auc(ens,y2,p2)
    summary={"tag":tag,"dual":cfg.dual,"seeds":list(seeds),"per_seed":rows,
             "per_seed_patientAUC":pp_rows,"ensemble":me,"ensemble_patientAUC":mpp}
    with open(os.path.join(out,f"summary_{tag}.json"),"w") as fp: json.dump(summary,fp,indent=2)
    print(f"\n----- {tag} -----")
    print(f"  [전역] 개별S={Sarr.mean():.4f}±{Sarr.std():.4f}  ▶앙상블S={me['S_PR_AUC']:.4f}  V={me['V_PR_AUC']:.4f}")
    print(f"  [환자별] 개별={ppa_arr.mean():.4f}±{ppa_arr.std():.4f}  ▶앙상블={mpp:.4f}({mppn}명)")
    print(f"저장됨: {out}/")
    return summary
