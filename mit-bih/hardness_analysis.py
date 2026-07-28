# =============================================================================
#  hardness_analysis.py  —  놓치는 S 비트가 '정보없음'인가 '라우팅가능'인가
#
#  사장님 질문: 앙상블/라우팅이 쉬운 데이터로만 기준 세우고, 진짜 어려운 ECG는
#              못 고치는 것 아닌가? → 측정으로 답한다.
#
#  각 진짜-S 비트마다 '57개 모델 중 몇 개가 S로 맞히나'를 세어 분류:
#    · 아무도 못 맞힘         = 정보 없음(조합 불가) → 외부데이터만이 답 (사장님 우려)
#    · 소수만 맞힘            = 라우팅하면 살릴 수 있음 (고칠 여지)
#    · 다수 맞힘              = 쉬운 비트
#  + per-beat 오라클 recall(비트마다 맞히는 모델이 하나라도 있으면 정답) = 라우팅 상한
#  + '아무도 못 맞히는' 비트가 특정 DS2 환자에 몰리는지(=그 환자 형태 학습불가)
#
#  실행:
#    exec(open('/content/drive/MyDrive/mitbih/hardness_analysis.py').read())
#    hardness()
# =============================================================================
import os, glob
import numpy as np

ROOT="/content/drive/MyDrive/mitbih"

def hardness(exclude_keys=("film",)):
    files=sorted(glob.glob(os.path.join(ROOT,"ablation_step*","**","cnn_*.npz"),recursive=True))
    probs=[]; y=None; pid=None
    for fp in files:
        nm=os.path.relpath(fp,ROOT)
        if any(k in nm for k in exclude_keys): continue
        d=np.load(fp)
        if y is None: y,pid=d["y"],d["pid"]
        elif not (np.array_equal(d["y"],y) and np.array_equal(d["pid"],pid)): continue
        probs.append(d["prob"])
    P=np.stack(probs,0); M=P.shape[0]
    print(f"{M}개 모델\n")

    pred=P.argmax(-1)                       # [M,N]
    Smask=y==1; nS=int(Smask.sum())
    Scorrect=(pred[:,Smask]==1)             # [M, nS]  각 모델이 각 S비트 맞혔나
    per_beat_hits=Scorrect.sum(0)           # [nS]  그 S비트를 맞힌 모델 수
    frac=per_beat_hits/M

    print(f"=== 진짜 S 비트 {nS}개: '몇 %의 모델이 맞히나' 분포 ===")
    cats=[("아무도 못 맞힘 (정보 없음)", per_beat_hits==0),
          ("1~10% 모델만 (라우팅 여지 큼)", (frac>0)&(frac<=0.10)),
          ("10~50% 모델 (라우팅 여지)", (frac>0.10)&(frac<=0.50)),
          ("50%+ 모델 (쉬운 비트)", frac>0.50)]
    for name,mask in cats:
        print(f"  {name:28s}: {mask.sum():5d}개  ({100*mask.mean():.1f}%)")

    oracle_recall=(per_beat_hits>0).mean()  # 비트마다 하나라도 맞히면 정답
    uni_recall=(np.stack(probs,0).mean(0).argmax(-1)[Smask]==1).mean()
    print(f"\n  균일 앙상블 S recall     = {uni_recall:.3f}")
    print(f"  per-beat 오라클 recall   = {oracle_recall:.3f}  (비트마다 맞히는 모델 있으면 채택)")
    print(f"  → 격차 {oracle_recall-uni_recall:.3f} = '라우팅으로 살릴 여지'")
    print(f"  → '아무도 못 맞힘' {100*(per_beat_hits==0).mean():.1f}% = 조합으론 절대 못 고침(정보 부족)")

    # '아무도 못 맞히는' S 비트가 환자별로 몰리나
    never_pid=pid[Smask][per_beat_hits==0]
    if len(never_pid):
        import collections
        Spid=pid[Smask]
        print(f"\n=== '아무도 못 맞히는' S 비트의 환자 분포 (상위) ===")
        cnt=collections.Counter(never_pid.tolist())
        for p,c in sorted(cnt.items(),key=lambda x:-x[1])[:8]:
            tot=int((Spid==p).sum())
            print(f"  환자 {p}: {c}/{tot}개 못맞힘 ({100*c/tot:.0f}% of 그 환자 S)")
    return dict(frac=frac,per_beat_hits=per_beat_hits,oracle_recall=float(oracle_recall))
