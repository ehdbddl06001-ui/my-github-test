# =============================================================================
#  colab_step9_pwave.py  —  [STEP 9] 벡터-에너지 기반 P파 특징 (정보 추가)
#
#  사장님 물리 아이디어 구현 (환자 정상 기준의 P파 함수):
#   · 벡터크기 VM(t)=√(lead1²+lead2²)  = 리드 독립 전기에너지
#   · 벡터방향 ang(t)=atan2(lead2,lead1) = 전기벡터 방향(이소성 초점→P축 변화)
#   · 환자 정상 ref로 P/QRS/T 영역·에너지 기준 설정
#   · residual = beat − (QRS로 스케일한 정상) → 남는 에너지 = 숨은/더해진 P (P-on-T)
#  → 8개 '환자상대' 특징. 기존 26D와 다른 정보(벡터방향·에너지분해·residual).
#
#  이건 재조합이 아니라 '정보 추가'라 천장을 올릴 수 있음. 두 단계로 검증:
#    A) diagnose()   — 학습 없이 각 특징의 S 판별력(단변량 AUC) 확인 (좋은 기준인가?)
#    B) run_pwave()  — 특징 추가 전/후 모델 성능 비교 (base26 vs pwave34)
#
#  실행:
#    exec(open('/content/drive/MyDrive/mitbih/colab_step9_pwave.py').read())
#    diagnose()                 # 먼저: 특징이 S를 실제로 가르나?
#    run_pwave("base26"); run_pwave("pwave")   # 다음: 모델에서 오르나?
# =============================================================================
import os, json
import numpy as np
from sklearn.metrics import average_precision_score, roc_auc_score

DATA_PATH="/content/drive/MyDrive/mitbih/mamba_data.npz"
SAVE_DIR ="/content/drive/MyDrive/mitbih/ablation_step9"
DS1_IDS=[101,106,108,109,112,114,115,116,118,119,122,124,201,203,205,207,208,209,215,220,223,230]
DS2_IDS=[100,103,105,111,113,117,121,123,200,202,210,212,213,214,219,221,222,228,231,232,233,234]
SEEDS=[1000,1001,1002,1003,1004]
PW_NAMES=["P/QRST비율","P비율(정상대비)","T잔차(P-on-T)","P잔차(이상P)","전체형태편차",
          "P축방향편차","P피크위치편차","전체VM비"]

# ─────────── 사장님 아이디어: 벡터-에너지 P파 특징 (numpy, 환자 정상 기준) ───────────
def extract_pwave_features(beats,refs,pid):
    N=len(beats); F=np.zeros((N,8),dtype=np.float32); eps=1e-6
    for p in np.unique(pid):
        idx=np.where(pid==p)[0]; b=beats[idx]; r=refs[idx]        # [n,2,300]
        VMb=np.sqrt(b[:,0]**2+b[:,1]**2); VMr=np.sqrt(r[:,0]**2+r[:,1]**2)
        angb=np.arctan2(b[:,1],b[:,0]);   angr=np.arctan2(r[:,1],r[:,0])
        L=VMb.shape[1]; R=int(np.argmax(VMr[0]))                  # 환자 정상 R 위치(ref 일정)
        Ps,Pe=max(0,R-90),max(2,R-25)                            # P 영역(QRS 이전)
        Qs,Qe=max(0,R-25),min(L,R+25)                            # QRS
        Ts,Te=min(L-2,R+30),min(L,R+130)                         # T
        if Pe-Ps<3: Ps,Pe=max(0,R-90),max(3,R-25)
        pE=VMb[:,Ps:Pe].sum(1); qE=VMb[:,Qs:Qe].sum(1); tE=VMb[:,Ts:Te].sum(1)
        pEr=VMr[:,Ps:Pe].sum(1); qEr=VMr[:,Qs:Qe].sum(1); tEr=VMr[:,Ts:Te].sum(1)
        f1=pE/(qE+tE+eps)                                        # ① P 에너지 비율
        f2=f1/(pEr/(qEr+tEr+eps)+eps)                           # ② 정상 대비
        scale=(qE/(qEr+eps))[:,None]; resid=VMb-scale*VMr        # QRS로 스케일한 정상 제거
        f3=np.clip(resid[:,Ts:Te],0,None).sum(1)/(qE+eps)       # ③ T영역 잔차=숨은 P(P-on-T)
        f4=np.clip(resid[:,Ps:Pe],0,None).sum(1)/(qE+eps)       # ④ P영역 이상 에너지
        f5=np.abs(resid).sum(1)/(qE+eps)                        # ⑤ 정상 형태 대비 전체 편차
        wb=VMb[:,Ps:Pe]; wr=VMr[:,Ps:Pe]                        # ⑥ P 벡터방향 편차(이소성)
        ab=np.arctan2((wb*np.sin(angb[:,Ps:Pe])).sum(1),(wb*np.cos(angb[:,Ps:Pe])).sum(1))
        ar=np.arctan2((wr*np.sin(angr[:,Ps:Pe])).sum(1),(wr*np.cos(angr[:,Ps:Pe])).sum(1))
        f6=np.arctan2(np.sin(ab-ar),np.cos(ab-ar))
        f7=(np.argmax(VMb[:,Ps:Pe],1)-np.argmax(VMr[:,Ps:Pe],1)).astype(np.float32)  # ⑦ P피크 위치이동(조기성)
        f8=VMb.sum(1)/(VMr.sum(1)+eps)                          # ⑧ 전체 VM 에너지비
        F[idx]=np.stack([f1,f2,f3,f4,f5,f6,f7,f8],1)
    return np.nan_to_num(F,posinf=0,neginf=0).astype("float32")

def load_all():
    d=np.load(DATA_PATH); return d["beat"],d["ref"],d["feats"],d["y"],d["pid"]

# ─────────── A) 학습 없이 특징 판별력 진단 ───────────
def diagnose():
    beats,refs,feats,y,pid=load_all()
    Xpw=extract_pwave_features(beats,refs,pid)
    m2=np.isin(pid,DS2_IDS); yd=y[m2]; Xd=Xpw[m2]
    print(f"=== P파 벡터-에너지 특징 8개: DS2에서 S 단변량 판별력 ===")
    print(f"(ROC-AUC 0.5=무의미, >0.65 유망, >0.7 강함 / S beat {int((yd==1).sum())}개)\n")
    for k,nm in enumerate(PW_NAMES):
        col=Xd[:,k]
        if np.std(col)<1e-9: print(f"  {nm:16s}: (상수)"); continue
        auc=roc_auc_score((yd==1).astype(int),col)
        auc=max(auc,1-auc)                                       # 방향 무관 판별력
        pr =average_precision_score((yd==1).astype(int),col if roc_auc_score((yd==1).astype(int),col)>=0.5 else -col)
        bar="█"*int((auc-0.5)*40)
        print(f"  {nm:16s}: ROC-AUC={auc:.3f}  S_PR-AUC={pr:.3f}  {bar}")
    # 조합(8개 로지스틱) 판별력 — 기존 26D와 별개로 얼마나 S를 가르나
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import GroupKFold
    oof=np.zeros(len(yd)); pidd=pid[m2]
    for tr,te in GroupKFold(5).split(Xd,yd,groups=pidd):
        c=LogisticRegression(max_iter=1000,class_weight={0:1,1:3,2:1.5}).fit(Xd[tr],yd[tr])
        oof[te]=c.predict_proba(Xd[te])[:,1]
    print(f"\n  ▶ 8개 특징만으로 S 판별(환자CV): S_PR-AUC={average_precision_score((yd==1).astype(int),oof):.3f}")
    print(f"     (이게 높으면 = 기존 26D 없이도 P파 특징이 S를 가른다 = 정보 추가 성공 신호)")

# ─────────── B) 모델에 추가해 성능 비교 (torch 필요) ───────────
def run_pwave(tag, seeds=None):
    import torch, torch.nn as nn, torch.nn.functional as F
    from sklearn.preprocessing import RobustScaler
    from sklearn.model_selection import GroupShuffleSplit
    use_pw = (tag=="pwave")
    seeds=seeds or SEEDS; device="cuda" if torch.cuda.is_available() else "cpu"
    beats,refs,feats,y,pid=load_all()
    refs_lf=np.empty_like(beats)                                 # label-free ref(전체 median)
    for p in np.unique(pid):
        m=pid==p; refs_lf[m]=np.median(beats[m],axis=0,keepdims=True)
    refs_lf=refs_lf.astype("float32")
    if use_pw:
        Xpw=extract_pwave_features(beats,refs,pid)               # ref(정상템플릿)로 P특징
        feats=np.concatenate([feats,Xpw],1).astype("float32")
    fdim=feats.shape[1]
    print(f"===== {tag} =====  feat_dim={fdim} ({'26+8' if use_pw else '26'})  device={device}")

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
            super().__init__(); s.e=Enc()
            s.sia=nn.Sequential(nn.Linear(256,64),nn.ReLU())
            s.gate=nn.Linear(128,64)
            s.proto=nn.Parameter(torch.randn(32,64)*0.1)
            s.fm=nn.Sequential(nn.Linear(fdim,64),nn.ReLU(),nn.Linear(64,64),nn.ReLU())
            s.cls=nn.Sequential(nn.Linear(192,64),nn.ReLU(),nn.Linear(64,3))
        def forward(s,b,r,ft):
            z1=s.e(b); z2=s.e(r); zb=s.sia(torch.cat([z1,z2,z1-z2,(z1-z2).abs()],-1))
            z=z1+torch.sigmoid(s.gate(torch.cat([z1,zb],-1)))*zb
            zp=torch.softmax((z@s.proto.t())*(64**-0.5),-1)@s.proto
            return s.cls(torch.cat([z,zp,s.fm(ft)],-1))

    def loader(a,bs,sh):
        ds=torch.utils.data.TensorDataset(*[torch.from_numpy(np.asarray(x)) for x in a])
        return torch.utils.data.DataLoader(ds,batch_size=bs,shuffle=sh)
    @torch.no_grad()
    def pred(m,b,r,ft):
        m.eval(); o=[]
        for i in range(0,len(b),4096):
            o.append(torch.softmax(m(torch.from_numpy(b[i:i+4096]).to(device),
                torch.from_numpy(r[i:i+4096]).to(device),torch.from_numpy(ft[i:i+4096]).to(device)),-1).cpu().numpy())
        return np.concatenate(o)
    def met(pb,yy):
        return (average_precision_score((yy==1).astype(int),pb[:,1]),
                average_precision_score((yy==2).astype(int),pb[:,2]))

    m1=np.isin(pid,DS1_IDS); m2=np.isin(pid,DS2_IDS)
    b1,r1,ft1,y1,p1=beats[m1],refs_lf[m1],feats[m1],y[m1],pid[m1]
    b2,r2,ft2,y2=beats[m2],refs_lf[m2],feats[m2],y[m2]
    os.makedirs(os.path.join(SAVE_DIR,tag),exist_ok=True); probs=[]
    for seed in seeds:
        torch.manual_seed(seed); np.random.seed(seed)
        tr,va=next(GroupShuffleSplit(1,test_size=0.2,random_state=seed).split(ft1,y1,groups=p1))
        sc=RobustScaler().fit(ft1[tr])
        f1=np.nan_to_num(sc.transform(ft1),posinf=0,neginf=0).astype("float32")
        f2=np.nan_to_num(sc.transform(ft2),posinf=0,neginf=0).astype("float32")
        M=Net().to(device); opt=torch.optim.AdamW(M.parameters(),lr=1e-3,weight_decay=1e-4)
        lossf=nn.CrossEntropyLoss(weight=torch.tensor([1.,3.,1.5],device=device))
        best=-1; bs=None; tl=loader((b1[tr],r1[tr],f1[tr],y1[tr]),512,True)
        for ep in range(15):
            M.train()
            for bb,rr,ff,yy in tl:
                bb,rr,ff,yy=(t.to(device) for t in (bb,rr,ff,yy)); opt.zero_grad()
                loss=lossf(M(bb,rr,ff),yy); loss.backward()
                torch.nn.utils.clip_grad_norm_(M.parameters(),1.0); opt.step()
            pv=pred(M,b1[va],r1[va],f1[va]); s,v=met(pv,y1[va])
            if 0.5*(s+v)>best: best=0.5*(s+v); bs={k:v.cpu() for k,v in M.state_dict().items()}
        M.load_state_dict(bs); pr=pred(M,b2,r2,f2); probs.append(pr)
        s,v=met(pr,y2); print(f"  [seed {seed}]  S={s:.4f}  V={v:.4f}")
    ens=np.stack(probs,0).mean(0); ens=ens/ens.sum(1,keepdims=True)
    s,v=met(ens,y2)
    print(f"\n----- {tag} -----  ▶앙상블 S={s:.4f}  V={v:.4f}")
    np.savez(os.path.join(SAVE_DIR,tag,"ens.npz"),prob=ens,y=y2,pid=pid[m2])
    return dict(S=s,V=v)
