# =============================================================================
#  colab_common.py  —  DS1에서 유도해 DS2에 적용하는 '전이 하이퍼파라미터' 단일 출처
#
#  원칙: 학습에 쓰는 모든 하이퍼파라미터는 (a) DS1 클래스수/신호에서 결정론적으로 계산하거나
#        (b) 관례 상수여야 한다. DS2(테스트)로는 절대 튜닝하지 않는다(오염 금지).
#  스크립트마다 복붙하지 말고 이걸 먼저 exec 해서 공유:
#    exec(open('/content/drive/MyDrive/mitbih/colab_common.py').read())
#  검증 근거: STEP42 — Sw를 DS1-val로 튜닝하면 DS2 전이가 안 됨(평평) → 공식이 더 강건.
# =============================================================================
import numpy as np

def auto_weights(y_ds1, beta=0.9999):
    """S 클래스 가중치 = 유효표본수(Cui 2019)로 DS1 클래스수에서 계산. DS2 안 봄.
       MIT-BIH DS1이면 ~11. 다른 DB면 그 DB 클래스수로 자동으로 다른 값."""
    nN=(y_ds1==0).sum(); nS=max((y_ds1==1).sum(),1)
    eff=lambda n:(1-beta)/(1-beta**n+1e-12)
    return float(eff(nS)/eff(nN))

def ldam_margins(y_ds1, cap=0.5):
    """LDAM margin (Cao 2019) = DS1 클래스수에서 m_c ∝ 1/n_c^{1/4}, 최소클래스=cap. (3,) 반환."""
    nc=np.array([(y_ds1==k).sum() for k in range(3)],np.float32)
    mc=1.0/np.power(np.maximum(nc,1),0.25)
    return (mc/mc.max()*cap).astype("float32")

def scaled_lr(batch, base_lr=1e-3, base_batch=512, rule="sqrt"):
    """배치-LR 스케일링: 배치를 바꾸면 LR도 함께 조정(작은배치→작은LR).
       'linear'(Goyal 2017) 또는 'sqrt'(Krizhevsky, 노이즈 보존에 유리). 배치를 512로 고정하면
       base_lr 그대로. 하이퍼파라미터가 아니라 배치의 결정론적 함수라 비교 공정성 유지."""
    r = (batch/base_batch) if rule=="linear" else np.sqrt(batch/base_batch)
    return float(base_lr*r)

def transfer_report(y_ds1):
    """DS1에서 유도된 전이 하이퍼파라미터를 한눈에(논문 Methods용 provenance)."""
    nN=int((y_ds1==0).sum()); nS=int((y_ds1==1).sum()); nV=int((y_ds1==2).sum())
    Sw=auto_weights(y_ds1); mc=ldam_margins(y_ds1)
    print(f"[DS1 유도 전이 하이퍼파라미터]  (DS2 미사용)")
    print(f"  DS1 클래스수: N={nN} S={nS} V={nV}")
    print(f"  S 가중치(auto_weights, 유효표본수) = {Sw:.2f}")
    print(f"  LDAM margins(1/n^0.25)            = {np.round(mc,3)}")
    print(f"  LR@batch512={scaled_lr(512):.1e}  LR@batch256(sqrt)={scaled_lr(256):.1e}  LR@batch1024(sqrt)={scaled_lr(1024):.1e}")
    return dict(Sw=Sw, margins=mc.tolist(), nN=nN, nS=nS, nV=nV)
