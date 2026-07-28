# =============================================================================
#  cnn_base_psa2_step1.py  —  [STEP 1] 목적함수(loss) 정비판
#
#  변경 원칙: 아키텍처는 원본과 100% 동일. 오직 "학습 목적함수 / 샘플링"만 바꿈.
#  → 41번 정체의 원인이 '죽어있는 모듈(Siamese/Prototype에 자기 손실이 없음)'인지
#    깨끗하게 분리 측정(ablation)하기 위함.
#
#  추가된 것 (모두 Cfg 스위치로 on/off):
#    · FocalLoss        : 희소 클래스 S의 hard example에 집중 (loss_type="focal")
#    · SupConLoss       : 임베딩 z를 클래스별로 뭉치게 하는 지도 대비손실
#                         → Siamese/Prototype 이름값을 하게 만드는 진짜 metric 신호
#    · balanced_sampler : 배치 안에 S/V 양성이 충분히 들어오게 (SupCon·Focal 둘 다 이득)
#    · proj_head        : SupCon 전용 128D 투영 헤드 (분류 경로엔 영향 없음)
#
#  ── ablation 실행법 (각 config로 SEEDS 3개 평균 S_PR_AUC 비교) ──
#    A(원본재현): loss_type="wce",   supcon_weight=0.0, balanced_sampler=False
#    B(+focal)  : loss_type="focal", supcon_weight=0.0, balanced_sampler=False
#    C(+supcon) : loss_type="wce",   supcon_weight=0.2, balanced_sampler=True
#    D(full)    : loss_type="focal", supcon_weight=0.2, balanced_sampler=True
#
#  입력: mamba_data.npz (원본과 동일)
#  실행: python cnn_base_psa2_step1.py
# =============================================================================
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from sklearn.preprocessing import RobustScaler
from sklearn.model_selection import GroupShuffleSplit
from sklearn.metrics import average_precision_score, precision_recall_fscore_support


class Cfg:
    n_leads=2; beat_len=300; feat_dim=26; n_classes=3; emb_dim=64
    n_proto=32
    class_w=(1.0,3.0,1.5); lr=1e-3; epochs=15; batch=512; seed=1000
    label_free_ref=False     # True면 ref를 전체비트 median으로 재계산(완전 라벨-프리)

    # ---- [STEP 1] 목적함수 스위치 (여기만 바꿔서 ablation) ----
    loss_type="focal"        # "wce"(원본 가중CE) | "focal"
    focal_gamma=2.0          # focal 집중도 (0이면 사실상 가중CE)
    supcon_weight=0.2        # 0.0이면 SupCon off. 총손실 = cls + w*supcon
    supcon_temp=0.1          # SupCon 온도
    balanced_sampler=True    # True면 클래스균형 WeightedRandomSampler로 배치 구성

DS1_IDS=[101,106,108,109,112,114,115,116,118,119,122,124,201,203,205,207,208,209,215,220,223,230]
DS2_IDS=[100,103,105,111,113,117,121,123,200,202,210,212,213,214,219,221,222,228,231,232,233,234]
SEEDS=[1000,1001,1002]     # 최종은 list(range(1000,1015))
OUT_DIR="."


# ---- 3층 1D-CNN 인코더 (원본 그대로) ----
class CNNEncoder(nn.Module):
    def __init__(self,cfg):
        super().__init__()
        self.net=nn.Sequential(
            nn.Conv1d(cfg.n_leads,32,7,padding=3), nn.BatchNorm1d(32), nn.ReLU(), nn.MaxPool1d(2),
            nn.Conv1d(32,64,5,padding=2),          nn.BatchNorm1d(64), nn.ReLU(), nn.MaxPool1d(2),
            nn.Conv1d(64,128,3,padding=1),         nn.BatchNorm1d(128),nn.ReLU(), nn.AdaptiveAvgPool1d(1),
        )
        self.proj=nn.Linear(128,cfg.emb_dim)
    def forward(self,wave):                    # [B,2,L]
        return self.proj(self.net(wave).squeeze(-1))   # [B,emb]


# ---- ① Siamese 자기대비 (원본 그대로) ----
class SiameseContrast(nn.Module):
    def __init__(self,emb,out):
        super().__init__(); self.fc=nn.Sequential(nn.Linear(emb*4,out),nn.ReLU())
    def forward(self,z1,z2):
        return self.fc(torch.cat([z1,z2,z1-z2,(z1-z2).abs()],dim=-1))

# ---- ② PrototypeBank (원본 그대로) ----
class PrototypeBank(nn.Module):
    def __init__(self,emb,n_proto):
        super().__init__(); self.proto=nn.Parameter(torch.randn(n_proto,emb)*0.1); self.scale=emb**-0.5
    def forward(self,z):
        return torch.softmax((z@self.proto.t())*self.scale,dim=-1)@self.proto

# ---- ③ 게이트드 잔차 (원본 그대로) ----
class GatedResidual(nn.Module):
    def __init__(self,emb):
        super().__init__(); self.gate=nn.Linear(emb*2,emb)
    def forward(self,z,zb):
        return z+torch.sigmoid(self.gate(torch.cat([z,zb],dim=-1)))*zb

# ---- 26D 공학특징 MLP (원본 그대로) ----
class FeatureMLP(nn.Module):
    def __init__(self,feat_dim,out):
        super().__init__(); self.net=nn.Sequential(nn.Linear(feat_dim,64),nn.ReLU(),nn.Linear(64,out),nn.ReLU())
    def forward(self,f): return self.net(f)


# ---- 전체 base_psa2 (원본 구조 + SupCon용 proj_head만 추가) ----
class CNNBasePSA2(nn.Module):
    def __init__(self,cfg):
        super().__init__(); self.cfg=cfg
        self.encoder=CNNEncoder(cfg)                          # 공유 인코더
        self.siamese=SiameseContrast(cfg.emb_dim,cfg.emb_dim) # ①
        self.gate=GatedResidual(cfg.emb_dim)                  # ③
        self.proto=PrototypeBank(cfg.emb_dim,cfg.n_proto)     # ②
        self.feat_mlp=FeatureMLP(cfg.feat_dim,cfg.emb_dim)    # 공학특징
        self.classifier=nn.Sequential(
            nn.Linear(cfg.emb_dim*3,cfg.emb_dim),nn.ReLU(),
            nn.Linear(cfg.emb_dim,cfg.n_classes))
        # [STEP 1] SupCon 전용 투영 헤드 — 분류 경로엔 안 들어감(순수 학습신호용)
        self.proj_head=nn.Sequential(
            nn.Linear(cfg.emb_dim,cfg.emb_dim),nn.ReLU(),nn.Linear(cfg.emb_dim,128))
    def forward(self,beat,ref,feats,return_emb=False):
        z1=self.encoder(beat); z2=self.encoder(ref)           # 가중치 공유
        zb=self.siamese(z1,z2)                                # 자기대비
        z=self.gate(z1,zb)                                    # 게이트드 잔차 (환자적응 beat 임베딩)
        z_proto=self.proto(z)                                 # 프로토타입
        z_feat=self.feat_mlp(feats)                           # 공학특징
        logits=self.classifier(torch.cat([z,z_proto,z_feat],dim=-1))
        if return_emb:
            emb=F.normalize(self.proj_head(z),dim=-1)         # SupCon용 L2정규화 임베딩
            return logits,emb
        return logits


# ---- [STEP 1] Focal Loss (다중클래스, alpha=class_w) ----
class FocalLoss(nn.Module):
    def __init__(self,alpha,gamma=2.0):
        super().__init__()
        self.register_buffer("alpha",torch.tensor(alpha,dtype=torch.float32))
        self.gamma=gamma
    def forward(self,logits,y):
        logp=F.log_softmax(logits,dim=1)
        logpt=logp.gather(1,y.view(-1,1)).squeeze(1)
        pt=logpt.exp()
        at=self.alpha.to(logits.device)[y]
        return (-at*(1-pt).pow(self.gamma)*logpt).mean()

# ---- [STEP 1] Supervised Contrastive Loss (배치 내 라벨 사용) ----
class SupConLoss(nn.Module):
    def __init__(self,temperature=0.1):
        super().__init__(); self.t=temperature
    def forward(self,feats,labels):
        # feats: [B,D] (L2정규화 완료), labels: [B]
        device=feats.device; B=feats.size(0)
        sim=(feats@feats.t())/self.t
        sim=sim-sim.max(dim=1,keepdim=True)[0].detach()       # 수치안정
        labels=labels.view(-1,1)
        pos=(labels==labels.t()).float()
        self_mask=1-torch.eye(B,device=device)
        pos=pos*self_mask                                     # 자기 자신 제외
        exp=torch.exp(sim)*self_mask
        logp=sim-torch.log(exp.sum(1,keepdim=True)+1e-12)
        pos_cnt=pos.sum(1)
        mean_logp_pos=(pos*logp).sum(1)/pos_cnt.clamp(min=1)
        valid=pos_cnt>0                                       # 배치에 같은클래스 없으면 제외
        return -(mean_logp_pos[valid]).mean() if valid.any() else feats.sum()*0.0


# ---- 데이터 (원본 그대로) ----
def load_data(cfg):
    d=np.load("mamba_data.npz")
    beats,refs=d["beat"],d["ref"]
    feats,y,pid=d["feats"],d["y"],d["pid"]
    if cfg.label_free_ref:
        refs=np.empty_like(beats)
        for p in np.unique(pid):
            m=pid==p; refs[m]=np.median(beats[m],axis=0,keepdims=True)
        refs=refs.astype("float32")
    return beats,refs,feats,y,pid

def subset(arrs,mask): return tuple(a[mask] for a in arrs)

def _loader(arrs,batch,shuffle,cfg=None,balanced=False):
    beat,ref,feats,y=arrs
    ds=torch.utils.data.TensorDataset(torch.from_numpy(np.asarray(beat)),
        torch.from_numpy(np.asarray(ref)),torch.from_numpy(np.asarray(feats)),
        torch.from_numpy(np.asarray(y)))
    if balanced and shuffle:                                 # [STEP 1] 클래스균형 샘플러
        yv=np.asarray(y).astype(int)
        cnt=np.bincount(yv,minlength=3).astype(np.float64)
        w=1.0/np.clip(cnt,1,None)
        samp_w=torch.from_numpy(w[yv]).double()
        sampler=torch.utils.data.WeightedRandomSampler(samp_w,num_samples=len(yv),replacement=True)
        return torch.utils.data.DataLoader(ds,batch_size=batch,sampler=sampler)
    return torch.utils.data.DataLoader(ds,batch_size=batch,shuffle=shuffle)


# ---- 학습/평가 ----
def make_cls_loss(cfg,device):
    if cfg.loss_type=="focal":
        return FocalLoss(cfg.class_w,cfg.focal_gamma).to(device)
    return nn.CrossEntropyLoss(weight=torch.tensor(cfg.class_w,dtype=torch.float32,device=device))

@torch.no_grad()
def evaluate(model,loader,device):
    model.eval(); probs,ys=[],[]
    for beat,ref,feats,y in loader:
        p=torch.softmax(model(beat.to(device),ref.to(device),feats.to(device)),-1)
        probs.append(p.cpu().numpy()); ys.append(y.numpy())
    probs=np.concatenate(probs); ys=np.concatenate(ys)
    return probs,ys

def metrics(probs,y):
    s=average_precision_score((y==1).astype(int),probs[:,1])
    v=average_precision_score((y==2).astype(int),probs[:,2])
    n=average_precision_score((y==0).astype(int),probs[:,0])
    pred=probs.argmax(1)
    p,r,f,_=precision_recall_fscore_support(y,pred,labels=[0,1,2],zero_division=0)
    return {"S_PR_AUC":s,"V_PR_AUC":v,"macro_PR_AUC":(n+s+v)/3,
            "S_Se":r[1],"S_P":p[1],"S_F1":f[1],"V_Se":r[2],"V_P":p[2],"V_F1":f[2]}

def train(model,tr_loader,va_loader,cfg,device):
    opt=torch.optim.AdamW(model.parameters(),lr=cfg.lr,weight_decay=1e-4)
    cls_loss=make_cls_loss(cfg,device)
    supcon=SupConLoss(cfg.supcon_temp).to(device)
    use_sc=cfg.supcon_weight>0
    best=-1; best_state=None
    for ep in range(cfg.epochs):
        model.train()
        for beat,ref,feats,y in tr_loader:
            beat,ref,feats,y=(t.to(device) for t in (beat,ref,feats,y))
            opt.zero_grad()
            if use_sc:
                logits,emb=model(beat,ref,feats,return_emb=True)
                loss=cls_loss(logits,y)+cfg.supcon_weight*supcon(emb,y)
            else:
                loss=cls_loss(model(beat,ref,feats),y)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(),1.0); opt.step()
        pr,ys=evaluate(model,va_loader,device); m=metrics(pr,ys)
        score=0.5*(m["S_PR_AUC"]+m["V_PR_AUC"])                # 정직한 모델선택(val-macro)
        if score>best: best=score; best_state={k:v.cpu() for k,v in model.state_dict().items()}
        print(f"  epoch {ep:02d}  val S={m['S_PR_AUC']:.4f}  V={m['V_PR_AUC']:.4f}")
    if best_state: model.load_state_dict(best_state)
    return model

def run_one_seed(cfg,seed,ds1,ds2,device):
    torch.manual_seed(seed); np.random.seed(seed)
    beats1,refs1,feats1,y1,pid1=ds1; beats2,refs2,feats2,y2,pid2=ds2
    gss=GroupShuffleSplit(n_splits=1,test_size=0.2,random_state=seed)
    tr_idx,va_idx=next(gss.split(feats1,y1,groups=pid1))       # record 겹침 없는 val
    sc=RobustScaler().fit(feats1[tr_idx])                      # 극단열 강건, DS1 fit
    f1=np.nan_to_num(sc.transform(feats1),posinf=0,neginf=0).astype("float32")
    f2=np.nan_to_num(sc.transform(feats2),posinf=0,neginf=0).astype("float32")
    tr=(beats1[tr_idx],refs1[tr_idx],f1[tr_idx],y1[tr_idx])
    va=(beats1[va_idx],refs1[va_idx],f1[va_idx],y1[va_idx])
    te=(beats2,refs2,f2,y2)
    model=CNNBasePSA2(cfg).to(device)
    model=train(model,
                _loader(tr,cfg.batch,True,cfg,balanced=cfg.balanced_sampler),
                _loader(va,cfg.batch,False),cfg,device)
    probs,ys=evaluate(model,_loader(te,cfg.batch,False),device)
    return probs,ys,pid2


def main():
    cfg=Cfg()
    device="cuda" if torch.cuda.is_available() else "cpu"
    print(f"device={device}  [STEP1] loss={cfg.loss_type} gamma={cfg.focal_gamma} "
          f"supcon_w={cfg.supcon_weight} balanced={cfg.balanced_sampler}")
    beats,refs,feats,y,pid=load_data(cfg)
    ds1=subset((beats,refs,feats,y,pid),np.isin(pid,DS1_IDS))
    ds2=subset((beats,refs,feats,y,pid),np.isin(pid,DS2_IDS))
    print(f"DS1 N={len(ds1[3])}  DS2 N={len(ds2[3])}  params={sum(p.numel() for p in CNNBasePSA2(cfg).parameters()):,}")
    rows=[]
    for seed in SEEDS:
        print(f"[seed {seed}]")
        probs,ys,pp=run_one_seed(cfg,seed,ds1,ds2,device)
        np.savez(f"{OUT_DIR}/cnn_base_s{seed}.npz",prob=probs,y=ys,pid=pp)  # base_psa2 포맷
        m=metrics(probs,ys); rows.append(m)
        print(f"  => DS2  S_PR_AUC={m['S_PR_AUC']:.4f}  V_PR_AUC={m['V_PR_AUC']:.4f}  "
              f"macro={m['macro_PR_AUC']:.4f}  S_Se={m['S_Se']:.3f}  S+P={m['S_P']:.3f}")
    print("\n===== 집계 (원본 목표: S 0.613 / V 0.932) =====")
    for k in ["S_PR_AUC","V_PR_AUC","macro_PR_AUC","S_Se","S_P","S_F1"]:
        v=np.array([r[k] for r in rows]); print(f"{k:12s} = {v.mean():.4f} ± {v.std():.4f}")
    print("\ndump: cnn_base_s1000~ .npz (개인화 run_pers 에 그대로 투입 가능)")


if __name__=="__main__":
    main()
