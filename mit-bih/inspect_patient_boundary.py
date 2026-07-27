# =============================================================================
#  inspect_patient_boundary.py  —  환자별 결정경계가 어떻게 달라지는지 관찰
#
#  FiLM 모델에서 S클래스 로짓은:
#     logit_S(h;p) = w_S_eff(p)·h + b_S_eff(p)
#        w_S_eff(p) = W_out[S] ⊙ (1+γ(g_p))       # 초평면 '방향'
#        b_S_eff(p) = W_out[S]·β(g_p) + b_out[S]   # 초평면 '절편'(=검출 문턱)
#  환자 p 마다 g_p 가 다르면 방향·절편이 달라진다 → 환자별 결정경계.
#
#  이 스크립트는 학습된 film 모델을 받아 DS2 환자별로 위를 추출해:
#    [수치] 절편 b_S_eff 의 환자간 분산, 방향 w_S_eff 의 회전(코사인),
#           그리고 '전역 경계 vs 환자 경계'의 환자내 S 분리도(ROC-AUC) 비교
#    [그림] ① γ 히트맵(환자×hidden)  ② 환자별 절편 막대  ③ 예시 환자 S-score 히스토그램
#           ④ 전역 vs 환자 경계 분리도 산점도
#  → 저장: SAVE_DIR/figs/*.png
#
#  선행: colab_step3.py 를 먼저 exec 해서 클래스/함수가 정의돼 있어야 함.
#  실행:
#    exec(open('/content/drive/MyDrive/mitbih/colab_step3.py').read())
#    exec(open('/content/drive/MyDrive/mitbih/inspect_patient_boundary.py').read())
#    inspect_boundary(seed=1000)     # 한 seed film 모델 학습 후 분석
# =============================================================================
import os
import numpy as np
import torch
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.preprocessing import RobustScaler
from sklearn.model_selection import GroupShuffleSplit
from sklearn.metrics import roc_auc_score

S_IDX = 1   # S(SVEB) 클래스 인덱스


@torch.no_grad()
def _hidden(model, beat, ref, feats):
    """분류기 은닉표현 h (FiLM 적용 '전') 를 계산."""
    z1=model.encoder(beat); z2=model.encoder(ref)
    zb=model.siamese(z1,z2); z=model.gate(z1,zb)
    z_proto=model.proto(z); z_feat=model.feat_mlp(feats)
    h=model.cls_hidden(torch.cat([z,z_proto,z_feat],dim=-1))
    return h, z2

@torch.no_grad()
def _patient_gamma_beta(model, ref_vec, device):
    """환자 기준파형 ref(1개)로 g_p, γ_p, β_p 계산."""
    ref_t=torch.from_numpy(ref_vec[None]).to(device)          # [1,2,300]
    z2=model.encoder(ref_t)
    g=model.patient_head(z2)
    gamma,beta=model.film(g).chunk(2,dim=-1)
    return g[0].cpu().numpy(), gamma[0].cpu().numpy(), beta[0].cpu().numpy()

def _train_film_seed(seed, device):
    """colab_step3 의 정의를 재사용해 film 모델 1개 학습."""
    cfg=Cfg(); cfg.patient_adapt=True; cfg.label_free_ref=True; cfg.val_split="gss"
    beats,refs,feats,y,pid=load_data(cfg)
    ds1=subset((beats,refs,feats,y,pid),np.isin(pid,DS1_IDS))
    ds2=subset((beats,refs,feats,y,pid),np.isin(pid,DS2_IDS))
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
    return model,(b2,r2,f2,y2,p2)

def inspect_boundary(seed=1000, example_patients=None):
    device="cuda" if torch.cuda.is_available() else "cpu"
    figdir=os.path.join(SAVE_DIR,"figs"); os.makedirs(figdir,exist_ok=True)
    print(f"[inspect] film seed={seed} 학습 중...")
    model,(b2,r2,f2,y2,p2)=_train_film_seed(seed,device); model.eval()

    W_out=model.cls_out.weight.detach().cpu().numpy()   # [3,64]
    b_out=model.cls_out.bias.detach().cpu().numpy()      # [3]
    wS_glob=W_out[S_IDX]; bS_glob=float(b_out[S_IDX])

    pats=sorted(np.unique(p2).tolist())
    gammas=[]; betas=[]; wS_eff=[]; bS_eff=[]
    for p in pats:
        ref_vec=r2[p2==p][0]                             # label-free ref (환자당 동일)
        _,gamma,beta=_patient_gamma_beta(model,ref_vec,device)
        gammas.append(gamma); betas.append(beta)
        wS_eff.append(wS_glob*(1.0+gamma))
        bS_eff.append(float(wS_glob@beta+bS_glob))
    gammas=np.array(gammas); wS_eff=np.array(wS_eff); bS_eff=np.array(bS_eff)

    # ---- [수치] 환자간 경계 변이 ----
    cos=np.array([float(wS_eff[i]@wS_glob/((np.linalg.norm(wS_eff[i])+1e-9)*(np.linalg.norm(wS_glob)+1e-9)))
                  for i in range(len(pats))])
    print("\n===== 환자별 결정경계 변이 =====")
    print(f"  S 절편 b_S_eff : 평균={bS_eff.mean():.3f}  std={bS_eff.std():.3f}  "
          f"범위=[{bS_eff.min():.3f}, {bS_eff.max():.3f}]  (환자마다 검출 문턱이 이만큼 이동)")
    print(f"  S 방향 회전    : 전역경계와 코사인 평균={cos.mean():.4f}  min={cos.min():.4f}  "
          f"(1.0에서 멀수록 방향이 환자별로 회전)")

    # ---- [수치] 전역 경계 vs 환자 경계: 환자내 S 분리도 ----
    beat_t=torch.from_numpy(b2).to(device); ref_t=torch.from_numpy(r2).to(device); ft_t=torch.from_numpy(f2).to(device)
    H=[]
    for i in range(0,len(y2),4096):
        h,_=_hidden(model,beat_t[i:i+4096],ref_t[i:i+4096],ft_t[i:i+4096]); H.append(h.cpu().numpy())
    H=np.concatenate(H)                                  # [N,64]
    auc_glob=[]; auc_pat=[]; used=[]
    for i,p in enumerate(pats):
        m=p2==p; yy=(y2[m]==S_IDX).astype(int)
        if yy.sum()<5 or yy.sum()==m.sum(): continue     # S가 너무 적으면 스킵
        s_glob=H[m]@wS_glob+bS_glob
        s_pat =H[m]@wS_eff[i]+bS_eff[i]
        auc_glob.append(roc_auc_score(yy,s_glob)); auc_pat.append(roc_auc_score(yy,s_pat)); used.append(p)
    auc_glob=np.array(auc_glob); auc_pat=np.array(auc_pat)
    print(f"\n  [환자내 S 분리도 ROC-AUC]  전역경계={auc_glob.mean():.4f}  →  환자경계={auc_pat.mean():.4f}  "
          f"({'✅ 환자적응이 분리 개선' if auc_pat.mean()>auc_glob.mean() else '⚠ 개선 없음'})  "
          f"(대상 {len(used)}명)")

    # ---- [그림] ----
    # ① γ 히트맵
    plt.figure(figsize=(10,5))
    plt.imshow(gammas,aspect="auto",cmap="RdBu_r",vmin=-np.abs(gammas).max(),vmax=np.abs(gammas).max())
    plt.colorbar(label="γ (hidden feature scale shift)"); plt.xlabel("hidden dim (64)"); plt.ylabel("DS2 patient")
    plt.yticks(range(len(pats)),pats,fontsize=6); plt.title(f"Per-patient FiLM γ (seed {seed})")
    plt.tight_layout(); f1=os.path.join(figdir,f"fig1_gamma_heatmap_s{seed}.png"); plt.savefig(f1,dpi=130); plt.close()

    # ② 환자별 S 절편 막대
    order=np.argsort(bS_eff)
    plt.figure(figsize=(10,4))
    plt.bar(range(len(pats)),bS_eff[order]-bS_glob)
    plt.axhline(0,color="k",lw=0.8); plt.xticks(range(len(pats)),[pats[i] for i in order],rotation=90,fontsize=6)
    plt.ylabel("b_S_eff(p) − b_S_global"); plt.title(f"환자별 S 검출 문턱 이동 (seed {seed})")
    plt.tight_layout(); f2=os.path.join(figdir,f"fig2_bias_shift_s{seed}.png"); plt.savefig(f2,dpi=130); plt.close()

    # ③ 예시 환자 S-score 히스토그램 (절편 차이가 큰 두 환자 + 중간)
    if example_patients is None:
        ex=[used[int(np.argmax(auc_pat))]] if used else []
        ex=list(dict.fromkeys([pats[order[0]],pats[order[-1]]]+ex))[:3]
    else:
        ex=example_patients
    plt.figure(figsize=(11,3.2))
    for j,p in enumerate(ex):
        i=pats.index(p); m=p2==p; yy=y2[m]
        s_pat=H[m]@wS_eff[i]+bS_eff[i]
        ax=plt.subplot(1,len(ex),j+1)
        ax.hist(s_pat[yy!=S_IDX],bins=40,alpha=.6,label="non-S",density=True)
        ax.hist(s_pat[yy==S_IDX],bins=40,alpha=.6,label="S",density=True,color="crimson")
        ax.axvline(0,color="k",lw=1,ls="--"); ax.set_title(f"pt {p}  (b={bS_eff[i]:.2f})",fontsize=9)
        ax.set_xlabel("환자 S-score  w_S_eff·h + b_S_eff");
        if j==0: ax.legend(fontsize=8)
    plt.suptitle(f"환자별 S 경계 위에서의 S vs non-S 분리 (문턱=0, seed {seed})",fontsize=10)
    plt.tight_layout(); f3=os.path.join(figdir,f"fig3_score_hist_s{seed}.png"); plt.savefig(f3,dpi=130); plt.close()

    # ④ 전역 vs 환자 경계 분리도 산점도
    plt.figure(figsize=(4.6,4.6))
    plt.scatter(auc_glob,auc_pat,s=18)
    lo=min(auc_glob.min(),auc_pat.min())-.02; hi=max(auc_glob.max(),auc_pat.max())+.02
    plt.plot([lo,hi],[lo,hi],"k--",lw=.8); plt.xlim(lo,hi); plt.ylim(lo,hi)
    plt.xlabel("전역 경계 S ROC-AUC"); plt.ylabel("환자 경계 S ROC-AUC")
    plt.title("대각선 위 = 환자적응이 그 환자에서 개선")
    plt.tight_layout(); f4=os.path.join(figdir,f"fig4_glob_vs_patient_s{seed}.png"); plt.savefig(f4,dpi=130); plt.close()

    print(f"\n그림 저장: {figdir}/  (fig1~fig4_*_s{seed}.png)")
    return dict(bS_eff=bS_eff, cos=cos, auc_glob=float(auc_glob.mean()),
                auc_pat=float(auc_pat.mean()), patients=pats, used=used)
