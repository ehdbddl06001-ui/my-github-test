# =============================================================================
#  svdb_rhythm.py  —  [SVDB 네이티브] 리듬 시퀀스 중심 모델 (RSN: Rhythm Sequence Net)
#
#  ── 왜 이 모델인가 (HANDOFF §3 결론1 + §5.3 방향 A) ───────────────────────────
#   결론1: S 검출을 결정하는 것은 리듬이다.  CNN(형태만) 0.164 → CNN+RR 0.484 (Δ+0.320)
#   결론2: 구조적 정교화(9특징군·샴·게이트·프로토타입)는 이득이 없었다 (Δ+0.050 비유의)
#   →  그런데 현행 모델은 그 '전부인 리듬'을 RHYTHM 10차원 + RR 2차원 = 12개 스칼라로
#      압축해 분류기에 곁들인다. EWMA 잔차를 비트당 스칼라로 접는 순간 "직전 8박이
#      어떤 패턴이었는가"(couplet/bigeminy/보상성 휴지의 문맥)가 소실된다.
#      ★이 병목을 푸는 것이 이 모델의 유일한 가설이다. 구조는 오히려 단순화한다.
#
#  ── 설계 원칙 (HANDOFF §5.1) ────────────────────────────────────────────────
#   1. 리듬을 1급 시민으로: RR '시퀀스'(±K박)를 주 인코더가 직접 처리. 형태는 보조.
#      용량 배분으로도 명시 — 리듬 64차원 vs 형태 16차원.
#   2. 단순하게: 게이트·프로토타입·샴 없음(결론2). 순수 concat + 선형 헤드.
#   3. MIT-BIH 유산 이식 금지: WST/MORPHO/REPOL/KOOPMAN/GNN/AE 캐시를 쓰지 않는다.
#      입력은 svdb_data.npz(beat, pre_rr, post_rr)에서만 유도한다.
#   4. +0.07 미만은 개선이라 부르지 않는다 (73환자 검정력 한계).
#
#  ── 무결성 (HANDOFF §7) ─────────────────────────────────────────────────────
#   · 라벨 미사용: RR 문맥 특징은 타이밍만으로 계산한다.
#   · 인과적(causal) 정규화: 환자별 med/MAD를 '직전 W박 이동창'에서 구한다.
#     → PAPER §9-6이 지적한 `_pp_center2`의 transductive 문제를 반복하지 않는다.
#   · 상수 하드코딩 최소화: 불균형 가중(Sw)·LDAM 마진은 하니스가 학습셋에서 유도한
#     값을 그대로 받아 쓴다(B2~B4와 동일). 임계도 calib에서만 결정.
#   · B2/B3/B4와 옵티마이저·epoch·batch·손실·임계법을 동일하게 맞춘다.
#     → 비교에서 달라지는 것은 '입력 표현과 인코더'뿐이다.
#
#  ── 사전등록 (SVDB_RHYTHM_DESIGN.md §3) ─────────────────────────────────────
#   주 가설 H-A : R1(RSN) − B4 ≥ +0.07  (대응 부트스트랩, Bonferroni k=3)
#   부가 R0(리듬만), R2(+Poincaré)는 탐색적. 결과를 보고 주가설을 바꾸지 않는다.
#
#  ── 사용법 (Colab) ──────────────────────────────────────────────────────────
#    exec(open('/content/drive/MyDrive/mitbih/svdb_bench.py').read())     # 하니스
#    exec(open('/content/drive/MyDrive/mitbih/svdb_rhythm.py').read())    # 이 파일
#    rr_audit()                    # ① RR 데이터 위생 점검(권장, 1분)
#    attach_arms()                 # ② R0/R1/R2 를 하니스에 arm으로 등록
#    OUT = bench_models(n_rep=1)   # ③ B0~B4C + R0/R1/R2 동일 폴드에서 학습·평가
#    report(OUT)                   # ④ 대응 부트스트랩 + Bonferroni + ±0.07 판정
#    repro_check(OUT)              # ⑤ 재현성(시드) 점검 — N3(SMOTE) 실패 재발 방지
#    literature_table(OUT, arm)    # ⑥ 비트풀링(micro) Se/+P/F1 — 문헌과 같은 잣대(비교불가 사유 병기)
#    burden_analysis(OUT, arm)     # ⑦ PAC burden 추정 정확도 — 임상 의의(Pearson + Bland-Altman)
#    compare_arms(OUT, a, b)       # ⑧ 두 arm 을 유병률 구간별로 비교(평균이 감추는 것)
#
#  자기검증(데이터 없이):  python svdb_rhythm.py --selftest
# =============================================================================
import numpy as np

# ★Colab 관례상 이 파일은 svdb_bench.py 와 '같은 globals'에 exec 된다.
#   따라서 하니스가 이미 정의한 이름(_BASE, _sv)을 덮어쓰면 안 된다 — 덮어쓰면
#   하니스 쪽 경로 설정이 조용히 무효화된다. 있으면 그대로 쓴다.
_BASE = globals().get("_BASE", "/content/drive/MyDrive/mitbih")

# 기본 하이퍼파라미터. 전부 '왜 이 값인가'가 아래 주석에 있고, 데이터에서 재유도할 수
# 있는 것(med/MAD/Sw/마진/임계)은 상수로 두지 않는다.
K_CTX   = 8      # ±8박 창 → 길이 17. 보상성 휴지·bigeminy·couplet 주기를 모두 덮는다.
W_NORM  = 128    # 인과적 med/MAD 이동창(박). 약 1.5분 — 체위·활동 변화보다 짧고
                 # 이소성 비율(최대 14.9%)보다 충분히 길어 median이 오염되지 않는다.
W_POIN  = 64     # Poincaré 국소 통계 창(박).
EWMA_A  = 0.3    # RHYTHM v2(colab_step49)와 동일한 α. 재유도 대상 아님(선행연구 고정값).
RR_LO   = 0.20   # 초. 생리적 하한(300 bpm). 이하는 결측 처리(주석 아티팩트, 아래 rr_audit 참조)
RR_HI   = 3.00   # 초. 생리적 상한(20 bpm). 이상은 결측 처리.
FS      = 360.0  # svdb_prep.py 가 360 Hz 로 리샘플했으므로 pre_rr/post_rr 단위는 360Hz 샘플.


# ─────────────────────────────────────────────────────────────────────────────
#  0. 데이터 접근 (자기검증 시 주입 가능)
# ─────────────────────────────────────────────────────────────────────────────
_DATA = None   # dict(beat,y,pid,pre_rr,post_rr) — set_data()로 주입하면 npz 대신 사용

def set_data(beat=None, y=None, pid=None, pre_rr=None, post_rr=None):
    """자기검증·소규모 시험용 데이터 주입. None 이면 해제(=npz 사용)."""
    global _DATA, _CTX
    _DATA = None if beat is None else dict(beat=beat, y=y, pid=pid, pre_rr=pre_rr, post_rr=post_rr)
    _CTX = None   # 문맥 캐시 무효화
    return _DATA is not None

def _rsn_sv():
    """(beat, y, pid, pre_rr, post_rr).

    우선순위: 주입 데이터 > 하니스의 _sv() > npz 직접 로드.
    ★하니스의 _sv 를 재정의하지 않고 '빌려 쓴다' — 데이터 경로를 한 곳으로 유지한다.
    """
    if _DATA is not None:
        d = _DATA
        return d["beat"], d["y"], d["pid"], d["pre_rr"], d["post_rr"]
    f = globals().get("_sv")
    if callable(f):
        return f()
    d = np.load(f"{_BASE}/svdb_data.npz")
    return d["beat"], d["y"], d["pid"], d["pre_rr"], d["post_rr"]


# ─────────────────────────────────────────────────────────────────────────────
#  1. RR 문맥 시퀀스 구성  (라벨 미사용 · 인과적 정규화 · 레코드 경계 차단)
# ─────────────────────────────────────────────────────────────────────────────
#
#  구간열(interval series) 정의 — svdb_prep.py 의 저장 규약에서 유도:
#    저장된 비트는 레코드 내 시간순이고, pre_rr[j] = 비트 j 로 '끝나는' RR,
#    post_rr[j] = 비트 j 에서 '시작하는' RR 이다. 비트가 건너뛰어지지 않았다면
#    post_rr[j] == pre_rr[j+1] 이므로, 한 레코드의 RR 열은
#        Aext = [pre_rr[0], pre_rr[1], ..., pre_rr[n-1], post_rr[n-1]]   (길이 n+1)
#    로 이어 붙일 수 있다. 비트 j 의 창은 Aext[j-K .. j+K] 이고
#    슬롯 k=0 이 자기 pre-RR, k=+1 이 자기 post-RR(=보상성 휴지 판별의 핵심)이다.
#
#  ★건너뜀 처리: svdb_prep 은 F/Q 등 AAMI 밖 심볼과 창이 잘리는 비트를 버린다.
#    그 지점에서는 post_rr[j] != pre_rr[j+1] 이므로 열에 '구멍'이 생긴다.
#    구멍을 건너 참조하는 슬롯은 mask=0 으로 끊는다(가짜 연속성 학습 방지).
#
def _ewma_causal_1d(x, alpha):
    """인과적 EWMA 예측(직전까지만 사용). colab_step49_rhythm2._ewma_causal 의 1D판."""
    pred = np.empty_like(x)
    acc = x[0]
    pred[0] = x[0]
    for t in range(1, len(x)):
        pred[t] = acc
        acc = alpha * x[t] + (1.0 - alpha) * acc
    return pred


def _trailing_med_mad(x, W):
    """직전 W개(자기 포함) 이동창의 median 과 MAD. 인과적.
       워밍업 구간은 x[0] 으로 edge-replicate 한다(미래 미사용)."""
    n = len(x)
    W = max(2, min(W, n))
    pad = np.concatenate([np.full(W - 1, x[0], dtype=x.dtype), x])
    sw = np.lib.stride_tricks.sliding_window_view(pad, W)      # (n, W)
    med = np.median(sw, axis=1)
    mad = np.median(np.abs(sw - med[:, None]), axis=1)
    return med, mad


def _poincare_local(A, valid, W):
    """국소 Poincaré/산포 통계 5종 (직전 W박, 인과적, 무차원).

    ★N1(리듬 게이트) 실패와의 차이 — HANDOFF §4 / PAPER §7-N1:
      N1 은 '불규칙도' 스칼라로 RR축을 **하드 차단**했고, 그 지표가 표적(이소성)에
      오염돼 S 많은 환자에서 S를 잡는 축을 스스로 껐다(자기파괴).
      여기서는 차단하지 않는다. 같은 정보를 **입력 채널로만** 주고, 어떻게 쓸지는
      학습 폴드가 정한다. AF('불규칙하게 불규칙' → 확산 구름)와 이소성('규칙 + 간헐
      조기박' → 이산 군집)의 분리는 sd1/sd2 와 이산성·첨도 대용치가 담당한다.
    """
    n = len(A)
    W = max(4, min(W, n))
    d = np.diff(A, prepend=A[0])
    pad = lambda z: np.concatenate([np.full(W - 1, z[0], dtype=z.dtype), z])
    swA = np.lib.stride_tricks.sliding_window_view(pad(A), W)
    swd = np.lib.stride_tricks.sliding_window_view(pad(d), W)
    med = np.median(swA, axis=1) + 1e-6
    sd1 = np.std(swd, axis=1) / np.sqrt(2.0)                    # 단기 변이(수직 산포)
    var = np.var(swA, axis=1)
    sd2 = np.sqrt(np.maximum(2.0 * var - sd1 ** 2, 0.0))        # 장기 변이(장축)
    ratio = sd1 / (sd2 + 1e-6)                                  # AF↑ / 이소성은 낮음
    disc = np.mean(np.abs(swd) > (0.15 * med)[:, None], axis=1)  # 큰 이탈의 '빈도'
    q = np.percentile(swd, [1, 25, 75, 99], axis=1)
    tail = (q[3] - q[0]) / (q[2] - q[1] + 1e-6)                 # 첨도 대용: 이소성↑ AF↓
    P = np.stack([sd1 / med, sd2 / med, ratio, disc, np.clip(tail, 0, 50) / 50.0], 1)
    P[~valid] = 0.0
    return np.nan_to_num(P).astype("float32")


def rr_context(pre, post, pid, K=K_CTX, W=W_NORM, WP=W_POIN, alpha=EWMA_A,
               poincare=True, causal_only=False, verbose=True):
    """RR 문맥 시퀀스 + 스칼라 보조특징 생성.

    반환 dict:
      seq  [N, C, L]  C=4 채널, L=2K+1
                      ch0 log(RR/med_j)      — 심박수 불변 상대 길이
                      ch1 dRR/med_j          — 무차원 1차 차분
                      ch2 tanh(innov/3MAD_j) — 인과적 EWMA 잔차, ★슬롯마다 보존
                      ch3 mask               — 유효 슬롯(경계·구멍·생리범위 밖 = 0)
      aux  [N, D]     D=5(+5) 스칼라 보조. [pre_s, post_s, med_j, pre/med, post/med]
                      (+ Poincaré 5종)
      info dict       진단용 카운트

    causal_only=True 면 미래 슬롯(k>=2)을 마스킹한다. k=+1(자기 post-RR)은 보상성
    휴지 판별에 필수라 남긴다 → 1박(≈0.8초) 지연의 스트리밍 구현이 가능하다.
    """
    pre = np.asarray(pre, np.float64) / FS      # 초
    post = np.asarray(post, np.float64) / FS
    pid = np.asarray(pid)
    N = len(pre)
    L = 2 * K + 1
    ks = np.arange(-K, K + 1)
    seq = np.zeros((N, 4, L), "float32")
    D = 5 + (5 if poincare else 0)
    aux = np.zeros((N, D), "float32")
    n_imp = 0; n_gap = 0; n_rec = 0

    for p in np.unique(pid):
        idx = np.flatnonzero(pid == p)          # 레코드 내 시간순(저장 순서)
        n = len(idx)
        if n < 2:
            continue
        n_rec += 1
        a = pre[idx]; b = post[idx]
        Aext = np.concatenate([a, [b[-1]]])     # 길이 n+1, 구간열

        # (a) 생리 범위 밖 = 결측. svdb_prep 의 pre_rr 은 주석열 diff 라서 '+'(리듬변경)
        #     같은 비-비트 주석이 끼면 0에 가까운 값이 섞일 수 있다(rr_audit 참조).
        ok = (Aext >= RR_LO) & (Aext <= RR_HI)
        n_imp += int((~ok).sum())
        if not ok.any():
            continue
        Afill = Aext.copy()
        if (~ok).any():                          # 통계·EWMA 오염 방지용 보간(마스크는 유지)
            Afill[~ok] = np.median(Aext[ok])

        # (b) 인과적 국소 척도
        med, mad = _trailing_med_mad(Afill, W)
        med = np.maximum(med, 1e-3)
        mad = np.maximum(mad, np.maximum(0.02, 0.05 * med))     # 스케일 바닥(폭발 방지)
        innov = Afill - _ewma_causal_1d(Afill, alpha)

        # (c) 연속성(구멍) — post[j] != pre[j+1] 이면 j~j+1 사이 비트가 버려진 것
        brk = np.zeros(n + 1, bool)
        if n >= 2:
            brk[1:n] = np.abs(b[:-1] - a[1:]) > (1.0 / FS)
        n_gap += int(brk.sum())
        cb = np.cumsum(brk.astype(np.int32))     # 슬롯 q 와 현재 j 가 같은 값이면 연속

        # (d) 창 수집
        j = np.arange(n)
        q = j[:, None] + ks[None, :]
        inr = (q >= 0) & (q <= n)
        qc = np.clip(q, 0, n)
        m = inr & (cb[qc] == cb[j][:, None]) & ok[qc] & (qc != 0)
        #  qc != 0 : 레코드 첫 구간은 svdb_prep 의 폴백(pre=rr[i]) 가능성이 있어 신뢰하지 않음
        if causal_only:
            m &= (ks[None, :] <= 1)

        mj = med[j][:, None]; dj = mad[j][:, None]
        c0 = np.clip(np.log(np.maximum(Afill[qc], 1e-3) / mj), -1.5, 1.5)
        dA = np.diff(Afill, prepend=Afill[0])
        c1 = np.clip(dA[qc] / mj, -1.5, 1.5)
        c2 = np.tanh(innov[qc] / (3.0 * dj))
        mm = m.astype("float32")
        seq[idx, 0] = (c0 * mm).astype("float32")
        seq[idx, 1] = (c1 * mm).astype("float32")
        seq[idx, 2] = (c2 * mm).astype("float32")
        seq[idx, 3] = mm

        # (e) 스칼라 보조 — B3(raw RR)의 정보를 포함해 RSN 이 B3 를 정보적으로 지배하게 한다
        mb = med[j]
        aux[idx, 0] = a
        aux[idx, 1] = b
        aux[idx, 2] = mb
        aux[idx, 3] = np.clip(a / mb, 0, 4)
        aux[idx, 4] = np.clip(b / mb, 0, 4)
        if poincare:
            aux[idx, 5:] = _poincare_local(Afill, ok, WP)[j]

    info = dict(n=N, records=n_rec, L=L, C=4, aux_dim=D,
                implausible=n_imp, gaps=n_gap, poincare=bool(poincare),
                causal_only=bool(causal_only), K=K, W=W)
    if verbose:
        print(f"  RR 문맥: seq{seq.shape} aux{aux.shape}  레코드 {n_rec}")
        print(f"    생리범위 밖 구간 {n_imp}  |  건너뜀(구멍) {n_gap}  |  "
              f"평균 유효슬롯 {seq[:,3].mean()*L:.1f}/{L}")
    return dict(seq=seq, aux=aux, info=info)


_CTX = None   # (K, W, WP, poincare, causal_only) -> dict

def prepare_context(K=K_CTX, W=W_NORM, WP=W_POIN, poincare=True,
                    causal_only=False, verbose=True):
    """RR 문맥을 한 번만 계산해 캐시(전 폴드 공용). 라벨 미사용이므로 폴드 밖 계산이
       누설이 아니다 — 타이밍만 쓰고, 정규화 통계도 '해당 환자 자신의 과거'뿐이다."""
    global _CTX
    key = (K, W, WP, bool(poincare), bool(causal_only))
    if _CTX is not None and _CTX["key"] == key:
        return _CTX
    _, _, pid, pre, post = _rsn_sv()
    if verbose:
        print(f"RR 문맥 계산 K=±{K} W={W} poincare={poincare} causal_only={causal_only}")
    c = rr_context(pre, post, pid, K=K, W=W, WP=WP, poincare=poincare,
                   causal_only=causal_only, verbose=verbose)
    c["key"] = key
    _CTX = c
    return c


# ─────────────────────────────────────────────────────────────────────────────
#  2. 모델 — RSN (Rhythm Sequence Net)
# ─────────────────────────────────────────────────────────────────────────────
# ── 분절(segment) 창 — 저장된 비트는 [2,300], R 피크가 인덱스 _RPRE=100 에 있다.
#   colab_step49._segwin 의 정의를 그대로 따르되 경계에 약간 여유를 준다:
#     P   (R-90, R-25) → (10, 75)     심방 탈분극  — 상심실성(S)의 기원 신호
#     QRS (R-25, R+25) → (75, 125)    심실 탈분극  — 전도이상·심실기원(V)·각차단
#     T   (R+30, R+130)→ (130, 230)   재분극       — 허혈·전해질·QT
#   ★질환마다 드러나는 분절이 다르므로 분절별로 따로 인코딩한다. 전체 비트를 한
#     CNN 에 넣고 GAP 를 걸면 300샘플 평균에 각 분절이 희석된다(P는 65/300).
SEGS = {"P": (5, 85), "QRS": (72, 130), "T": (128, 240)}
P_LO, P_HI = SEGS["P"]          # 하위호환


def _rsn(cseq, L, daux, use_morph=True, use_ref=False, use_pwave=False,
         segs=(), use_seq=True, w_r=64, w_m=16, w_a=16, w_p=16, p_drop=0.1):
    """리듬 주(主) · 형태 보조(補) 구조.

    리듬 가지: dilation 1-2-4 의 3층 TCN. 수용야 17 = 창 전체(K=8)를 정확히 덮는다.
      풀링은 [GAP, k=0 탭, k=+1 탭] 을 이어 붙인다 — 전역 문맥과 '자기 박의 조기성·
      보상성 휴지'를 동시에 남기기 위함(GAP만 쓰면 자기 박이 17분의 1로 희석된다).
    형태 가지: 채널 폭을 B2/B3(32-64-128)의 1/4로 줄인 소형 CNN.
      결론1(형태만 F1 0.164)에 따라 형태에 용량을 쓰지 않는다. 다만 V 판별에는
      형태가 유효하므로 제거하지 않고 '보조'로 남긴다(3-class 이기 때문).
    융합: 게이트·프로토타입·샴 없음(결론2). 단순 concat → 2층 선형 헤드.
    """
    import torch
    import torch.nn as nn

    class RSN(nn.Module):
        def __init__(s):
            super().__init__()
            # use_seq=False(R5 대조군)면 리듬 가지를 아예 만들지 않는다 —
            # 미사용 파라미터가 옵티마이저에 남으면 '순수 대조군'이라 말할 수 없다.
            s.rz = s.rp = None
            if use_seq:
                s.rz = nn.Sequential(
                    nn.Conv1d(cseq, 64, 5, padding=2), nn.BatchNorm1d(64), nn.GELU(),
                    nn.Conv1d(64, 64, 3, padding=2, dilation=2), nn.BatchNorm1d(64), nn.GELU(),
                    nn.Conv1d(64, 64, 3, padding=4, dilation=4), nn.BatchNorm1d(64), nn.GELU())
                s.rp = nn.Sequential(nn.Linear(64 * 3, w_r), nn.GELU())
            s.k0 = (L - 1) // 2                      # 슬롯 k=0 (자기 pre-RR)
            s.k1 = min(s.k0 + 1, L - 1)              # 슬롯 k=+1 (자기 post-RR)
            s.use_ref = bool(use_ref)
            mch = 6 if use_ref else 2          # [비트, 환자템플릿, 차이] 각 2리드
            s.mz = None
            if use_morph:
                s.mz = nn.Sequential(
                    nn.Conv1d(mch, 16, 7, padding=3), nn.BatchNorm1d(16), nn.ReLU(), nn.MaxPool1d(2),
                    nn.Conv1d(16, 32, 5, padding=2), nn.BatchNorm1d(32), nn.ReLU(), nn.MaxPool1d(2),
                    nn.Conv1d(32, 32, 3, padding=1), nn.BatchNorm1d(32), nn.ReLU(),
                    nn.AdaptiveAvgPool1d(1))
                s.mp = nn.Sequential(nn.Linear(32, w_m), nn.ReLU())
            # ★P파 가지 — S 의 유일한 비-RR 물리 신호(이소성 심방 초점 → P 형태·극성·시점 변화)
            #   전체 비트 CNN 은 GAP 로 300샘플을 평균내므로 65샘플짜리 P 가 희석된다.
            #   P 구간만 잘라 별도 인코딩하고, GAP 와 함께 GMP 를 써서 진폭·극성을 살린다.
            #   use_pwave 는 segs=("P",) 의 하위호환 별칭이다.
            s.segs = tuple(segs) if segs else (("P",) if use_pwave else ())
            s.use_seq = bool(use_seq)
            s.sz = nn.ModuleDict(); s.sp = nn.ModuleDict()
            for nm in s.segs:
                s.sz[nm] = nn.Sequential(
                    nn.Conv1d(mch, 32, 7, padding=3), nn.BatchNorm1d(32), nn.ReLU(), nn.MaxPool1d(2),
                    nn.Conv1d(32, 32, 5, padding=2), nn.BatchNorm1d(32), nn.ReLU())
                s.sp[nm] = nn.Sequential(nn.Linear(64, w_p), nn.ReLU())
            s.ap = nn.Sequential(nn.Linear(max(daux, 1), w_a), nn.ReLU()) if daux > 0 else None
            d = ((w_r if use_seq else 0) + (w_m if use_morph else 0)
                 + w_p * len(s.segs) + (w_a if daux > 0 else 0))
            s.cls = nn.Sequential(nn.Linear(d, 64), nn.ReLU(), nn.Dropout(p_drop), nn.Linear(64, 3))

        def _mk(s, bt, rf):
            """형태 입력 구성. use_ref 면 [비트, 환자템플릿, 비트−템플릿] (6채널).

            rf 가 없으면 템플릿=비트, 차이=0 으로 채운다 — '편차 정보 없음'이라는
            중립값이며 채널 수를 유지해 conv 가 깨지지 않게 한다.
            """
            if not s.use_ref:
                return bt
            if rf is None:
                return torch.cat([bt, bt, torch.zeros_like(bt)], 1)
            return torch.cat([bt, rf, bt - rf], 1)

        def forward(s, sq, bt, ax, rf=None):
            parts = []
            if s.use_seq:
                h = s.rz(sq)
                parts.append(s.rp(torch.cat([h.mean(-1), h[:, :, s.k0], h[:, :, s.k1]], -1)))
            x = s._mk(bt, rf) if (s.mz is not None or s.segs) else None
            if s.mz is not None:
                parts.append(s.mp(s.mz(x).squeeze(-1)))
            for nm in s.segs:                       # 분절별 인코딩 (P / QRS / T)
                lo, hi = SEGS[nm]
                q = s.sz[nm](x[:, :, lo:hi])
                parts.append(s.sp[nm](torch.cat([q.mean(-1), q.amax(-1)], -1)))
            if s.ap is not None:
                parts.append(s.ap(ax))
            return s.cls(torch.cat(parts, -1))

    return RSN()


# ─────────────────────────────────────────────────────────────────────────────
#  3. 학습·예측 — B2/B3/B4 와 동일 규약(공정 비교)
# ─────────────────────────────────────────────────────────────────────────────
def _fit_predict_rsn(SEQ, AUX, beats, y, tr, cal, te, Sw, mc, seed,
                     use_morph=True, epochs=15, bs=512, n_seed=1,
                     ref=None, use_ref=False, use_pwave=False, segs=(), use_seq=True):
    """(calib 확률, test 확률) 반환. 하니스 _fit_predict 와 동일한 옵티마이저·손실·
       epoch·batch·grad clip. 달라지는 것은 입력 표현과 인코더뿐이다.

    n_seed>1 이면 softmax 평균(무지도 앙상블). ★주 비교에서는 1로 둔다 —
    B2~B4 가 단일 시드이므로 앙상블은 부당한 분산 이득이 된다(PAPER §6.7).
    """
    import torch
    import torch.nn.functional as Fn
    from sklearn.preprocessing import RobustScaler

    dev = "cuda" if torch.cuda.is_available() else "cpu"
    # 스칼라 보조만 스케일링. 시퀀스 채널은 설계상 이미 무차원·유계라 건드리지 않는다.
    sc = RobustScaler().fit(AUX[tr])
    T = lambda X: np.nan_to_num(sc.transform(X), posinf=0, neginf=0).astype("float32")
    Atr, Aca, Ate = T(AUX[tr]), T(AUX[cal]), T(AUX[te])
    L = SEQ.shape[2]
    Pc = np.zeros((len(cal), 3), np.float64)
    Pt = np.zeros((len(te), 3), np.float64)

    for si in range(max(1, n_seed)):
        sd = int(seed) * 1000 + si
        torch.manual_seed(sd); np.random.seed(sd)
        M = _rsn(SEQ.shape[1], L, AUX.shape[1], use_morph=use_morph,
                 use_ref=use_ref, use_pwave=use_pwave, segs=segs, use_seq=use_seq).to(dev)
        opt = torch.optim.AdamW(M.parameters(), lr=1e-3, weight_decay=1e-4)
        cw = torch.tensor([1., Sw, 1.5], device=dev)
        mcv = torch.from_numpy(np.asarray(mc, "float32")).to(dev)

        # ref 가 필요한 구성이면 텐서에 함께 싣는다(없으면 더미 0 — 메모리 낭비 방지)
        need_ref = bool(use_ref) and ref is not None
        RT = (torch.from_numpy(ref[tr]) if need_ref
              else torch.zeros(len(tr), 1, 1, dtype=torch.float32))
        ds = torch.utils.data.TensorDataset(
            torch.from_numpy(SEQ[tr]), torch.from_numpy(beats[tr]),
            torch.from_numpy(Atr), RT, torch.from_numpy(y[tr]))
        dl = torch.utils.data.DataLoader(ds, batch_size=bs, shuffle=True)
        for _ in range(epochs):
            M.train()
            for sq, bt, ax, rf, yy in dl:
                sq, bt, ax, rf, yy = (t.to(dev) for t in (sq, bt, ax, rf, yy))
                opt.zero_grad()
                lo = M(sq, bt, ax, rf if need_ref else None)
                lg = lo - torch.zeros_like(lo).scatter_(1, yy[:, None], mcv[yy][:, None])
                ce = Fn.cross_entropy(lg, yy, reduction="none")
                loss = (ce * cw[yy]).sum() / cw[yy].sum()
                loss.backward()
                torch.nn.utils.clip_grad_norm_(M.parameters(), 1.0)
                opt.step()

        @torch.no_grad()
        def pred(idx, Ax):
            M.eval(); o = []
            for i in range(0, len(idx), 4096):
                sl = idx[i:i + 4096]
                sq = torch.from_numpy(SEQ[sl]).to(dev)
                bt = torch.from_numpy(beats[sl]).to(dev)
                ax = torch.from_numpy(Ax[i:i + 4096]).to(dev)
                rf = torch.from_numpy(ref[sl]).to(dev) if need_ref else None
                o.append(torch.softmax(M(sq, bt, ax, rf), -1).cpu().numpy())
            return np.concatenate(o)

        Pc += pred(cal, Aca); Pt += pred(te, Ate)

    n = max(1, n_seed)
    return Pc / n, Pt / n


# ─────────────────────────────────────────────────────────────────────────────
#  4. 하니스 arm 등록
# ─────────────────────────────────────────────────────────────────────────────
#  svdb_bench.bench_models() 는 폴드마다 EXTRA_ARMS 의 각 함수를 ctx 로 호출하고
#  길이 len(te) 의 bool 결정벡터를 받는다. ctx 키:
#    beats,y,pid,pre,post,refM,refR,tr,cal,te,Sw,mc,seed,rep,fold,best_t
#
# ─────────────────────────────────────────────────────────────────────────────
#  라벨프리 환자별 적응 임계 — §9.1 이 지목한 병목
# ─────────────────────────────────────────────────────────────────────────────
#  왜: 환자별 S 유병률이 0.07%~57.6%(800배)인데 임계는 전역 하나뿐이다.
#      그 결과 유병률↑ → 정밀도↑·민감도↓ 로 정반대 실패가 생기고(§6.2),
#      새 축이 순위를 개선해도 F1 으로 환산되지 않는다(rec43: PR-AUC 불변인데 F1 −0.217).
#
#  ★무결성: 테스트 환자에 대해서는 **그 환자 자신의 점수만** 쓴다(라벨 미사용).
#    '라벨프리 대용치 → 최적 임계 분위' 의 사상(mapping)만 **calib 라벨**로 학습한다.
#    HANDOFF §7-1(테스트 라벨로 어떤 결정도 하지 않는다), §7-3(개인화는 본인 신호만) 준수.
#
#  ⚠ 한계: 그 환자의 레코드 전체 점수로 분위를 잡으므로 **transductive** 다
#    (PAPER §9-6 이 `_pp_center2` 에 대해 지적한 것과 같은 성질). 스트리밍에는
#    이동창 버전이 필요하다. 오프라인 Holter 분석에는 그대로 적용 가능하다.
def _logit(p, eps=1e-6):
    p = np.clip(np.asarray(p, float), eps, 1 - eps)
    return np.log(p / (1 - p))


def _prev_proxy(s, t_global):
    """라벨 없이 구하는 '전역 규칙이 이 환자에서 몇 %를 양성이라 하는가'.

    ★2성분 군집(k-means)을 먼저 시도했다가 버렸다: 유병률이 낮은 환자의 점수 분포는
      사실상 단봉이라 2-means 가 '정상 덩어리'를 반으로 쪼개고, 유병률 0.5% 환자에
      0.983 같은 무의미한 값을 돌려준다(실측 확인). 봉우리가 두 개라는 가정이
      저유병 환자에서 깨지기 때문이다.

    대신 **전역 임계가 그 환자에서 실현하는 양성률**을 대용치로 쓴다. 이것은
      · 단봉/양봉에 무관하게 항상 잘 정의되고,
      · 우리가 고치려는 대상(전역 임계의 환자별 오작동)을 직접 측정하며,
      · 테스트 환자의 라벨을 전혀 쓰지 않는다(t_global 은 calib 에서 온 상수).
    """
    return float((np.asarray(s) >= t_global).mean())


def _fit_adaptive(sc, y_cal, pid_cal, best_t, t_global):
    """calib 에서 (라벨프리 대용치 x) → (F1 최적 임계의 분위 q) 사상을 학습.
       반환 (a, b) 또는 None(표본 부족 → 전역 임계 폴백)."""
    xs, qs = [], []
    for p in np.unique(pid_cal):
        m = pid_cal == p
        s = sc[m]; yy = y_cal[m]
        if (yy == 1).sum() < 3 or len(s) < 32:      # 최적 분위를 신뢰할 수 없는 환자 제외
            continue
        t = best_t(s, yy)
        xs.append(_prev_proxy(s, t_global))         # 전역 규칙이 실현하는 양성률
        qs.append(float((s < t).mean()))            # 그 환자의 최적 임계 '분위 순위'
    if len(xs) < 8:
        return None
    # 전역 임계가 함의하는 분위 → 실제 최적 분위. 둘 다 logit 공간에서 선형 적합.
    X = _logit(np.clip(1.0 - np.array(xs), 1e-4, 1 - 1e-4))
    Q = _logit(np.clip(np.array(qs), 1e-4, 1 - 1e-4))
    if np.std(X) < 1e-9:
        return None
    b, a = np.polyfit(X, Q, 1)                      # logit(q*) = a + b·logit(q_global)
    return (float(a), float(b))


def _apply_adaptive(st, pid_te, ab, t_global):
    """테스트 환자별 임계 적용. ab 가 None 이거나 환자가 너무 짧으면 전역 임계 폴백."""
    out = np.zeros(len(st), bool)
    for p in np.unique(pid_te):
        m = pid_te == p
        s = st[m]
        if ab is None or len(s) < 32:
            out[m] = s >= t_global; continue
        qg = _logit(np.clip(1.0 - _prev_proxy(s, t_global), 1e-4, 1 - 1e-4))
        q = 1.0 / (1.0 + np.exp(-(ab[0] + ab[1] * qg)))
        q = float(np.clip(q, 0.50, 0.9995))
        out[m] = s >= np.quantile(s, q)
    return out


def make_arm(use_morph=True, poincare=True, K=K_CTX, W=W_NORM, WP=W_POIN,
             causal_only=False, n_seed=1, epochs=15, use_ref=False, use_pwave=False,
             segs=(), use_seq=True, adaptive_thr=False):
    """RSN arm 클로저 생성. 문맥은 첫 호출에서 한 번만 계산해 캐시된다.

    use_ref/use_pwave 는 하니스가 ctx 로 넘겨주는 환자별 강건 템플릿(refR)을 쓴다.
    ★refR 은 라벨 없이 환자 본인 신호만으로 만든 '그 환자의 정상 모양'이다
      (colab_step67.robust_template). 지금까지 RSN 은 이걸 쓰지 않고 있었다.
    """
    def arm(ctx):
        c = prepare_context(K=K, W=W, WP=WP, poincare=poincare,
                            causal_only=causal_only, verbose=False)
        rf = ctx.get("refR") if (use_ref or use_pwave or segs) else None
        pc, pt = _fit_predict_rsn(
            c["seq"], c["aux"], ctx["beats"], ctx["y"],
            ctx["tr"], ctx["cal"], ctx["te"], ctx["Sw"], ctx["mc"], ctx["seed"],
            use_morph=use_morph, epochs=epochs, n_seed=n_seed,
            ref=rf, use_ref=(use_ref or use_pwave or bool(segs)),
            use_pwave=use_pwave, segs=segs, use_seq=use_seq)
        t = ctx["best_t"](pc[:, 1], ctx["y"][ctx["cal"]])     # 임계는 calib 에서만
        if adaptive_thr:
            # 사상만 calib 라벨로 학습하고, 테스트는 환자 자신의 점수만으로 임계를 정한다
            ab = _fit_adaptive(pc[:, 1], ctx["y"][ctx["cal"]], ctx["pid"][ctx["cal"]],
                               ctx["best_t"], t)
            return _apply_adaptive(pt[:, 1], ctx["pid"][ctx["te"]], ab, t), pt[:, 1]
        return (pt[:, 1] >= t), pt[:, 1]                       # (결정, 점수) — 점수는 사후 진단용
    return arm


ARM_SPEC = {
    # 표시이름                     : (형태가지, Poincaré, 환자템플릿, P파가지)
    "R0.RSN(리듬만)":              dict(use_morph=False, poincare=False),
    "R1.RSN(리듬+형태)":           dict(use_morph=True,  poincare=False),
    "R2.RSN(+Poincaré)":           dict(use_morph=True,  poincare=True),
    # ── 2차 (SVDB_RHYTHM_DESIGN §8 사전등록) ──
    #  R3: 형태 입력을 [비트, 환자템플릿, 차이]로 바꾼다. "이 환자의 정상 대비 얼마나
    #      다른가"는 지금까지 RSN 에 없던 정보다(refR 이 ctx 에 있는데 안 쓰고 있었다).
    "R3.RSN(+환자템플릿)":          dict(use_morph=True,  poincare=False, use_ref=True),
    #  R4: 위에 더해 P파 구간을 따로 인코딩한다. S 의 유일한 비-RR 물리 신호.
    #      순위한계 환자(RR 변동이 커서 조기성이 안 드러나는 17명)의 표적.
    "R4.RSN(+P파)":                dict(use_morph=True,  poincare=False, use_ref=True,
                                        use_pwave=True),
    # ── 3차 (SVDB_RHYTHM_DESIGN §10 사전등록) ──
    #  R5: 리듬 시퀀스 가지를 '제거'한 대조군. 나머지는 R1 과 완전히 동일하고 RR 은
    #      aux 스칼라로만 들어간다. → '펼치기'를 **단일 변수**로 검정하는 유일한 arm.
    #      (R1−B3 는 형태 CNN 용량까지 달라서 순수 대조가 아니다)
    "R5.RSN(시퀀스제거·대조)":       dict(use_morph=True,  poincare=False, use_seq=False),
    #  R6: 분절 형태 — P/QRS/T 를 각각 환자템플릿 대비로 인코딩.
    #      질환마다 드러나는 분절이 다르다(P:심방, QRS:전도·심실, T:재분극).
    "R6.RSN(+P/QRS/T)":            dict(use_morph=True,  poincare=False, use_ref=True,
                                        segs=("P", "QRS", "T")),
    # ── 4차 (SVDB_RHYTHM_DESIGN §12 사전등록) ──
    #  R7: R6 와 **모델이 완전히 동일**하고 임계 결정법만 환자별 적응으로 바꾼 arm.
    #      → R7 − R6 = '전역 임계 → 적응 임계' 의 순수 효과. 모델 변경 없음.
    "R7.RSN(+적응임계)":            dict(use_morph=True,  poincare=False, use_ref=True,
                                        segs=("P", "QRS", "T"), adaptive_thr=True),
}

def attach_arms(which=("R0", "R1", "R2"), K=K_CTX, n_seed=1, epochs=15,
                causal_only=False, verbose=True):
    """선택한 RSN arm 들을 svdb_bench 하니스에 등록한다."""
    g = globals()
    reg = g.get("register_arm")
    if reg is None:
        raise RuntimeError("svdb_bench.py 를 먼저 exec 하세요 (register_arm 없음). "
                           "이 저장소의 svdb_bench.py 는 arm 레지스트리를 포함합니다.")
    pre = tuple(w.split(".")[0] for w in which)
    n = 0
    for name, kw in ARM_SPEC.items():
        if name.split(".")[0] not in pre:
            continue
        reg(name, make_arm(K=K, n_seed=n_seed, epochs=epochs,
                           causal_only=causal_only, **kw))
        n += 1
    if verbose:
        print(f"✔ RSN arm {n}개 등록.  bench_models() 를 실행하면 B0~B4C 와 "
              f"동일 폴드·동일 임계규약으로 함께 평가됩니다.")
        print(f"  주 비교: 'R1.RSN(리듬+형태)' vs 'B4.본연구'  (사전등록 H-A)")
    return n


# ─────────────────────────────────────────────────────────────────────────────
#  5. 대응 부트스트랩 + Bonferroni + ±0.07 판정
# ─────────────────────────────────────────────────────────────────────────────
def paired(RES, a, b, B=5000, seed=0, k_bonf=1, mde=0.07, show=True):
    """같은 환자의 F1 차이에 대한 대응 부트스트랩(HANDOFF §6.2 확장판).
       k_bonf 개 비교에 대해 Bonferroni 보정 CI 를 함께 낸다."""
    d = np.asarray(RES[a]["fper"]) - np.asarray(RES[b]["fper"])
    rng = np.random.RandomState(seed); n = len(d)
    bs = np.array([d[rng.randint(0, n, n)].mean() for _ in range(B)])
    lo, hi = np.percentile(bs, [2.5, 97.5])
    alpha = 0.05 / max(1, k_bonf)
    blo, bhi = np.percentile(bs, [100 * alpha / 2, 100 * (1 - alpha / 2)])
    sig = (lo > 0) or (hi < 0)
    bsig = (blo > 0) or (bhi < 0)
    out = dict(delta=float(d.mean()), ci=(float(lo), float(hi)),
               bonf=(float(blo), float(bhi)), sig=bool(sig), bonf_sig=bool(bsig),
               n=n, se=float(bs.std(ddof=1)), meets_mde=bool(d.mean() >= mde and blo > 0))
    if show:
        v = "★확증(보정 후 유의)" if bsig else ("한계적(보정 전만 유의)" if sig else "유의하지 않음")
        print(f"  {a} − {b}: Δ={out['delta']:+.3f} [95%CI {lo:+.3f},{hi:+.3f}] "
              f"Bonf(k={k_bonf})[{blo:+.3f},{bhi:+.3f}]  {v}")
        if out["meets_mde"]:
            print(f"      → ★Δ≥{mde:.2f} 이고 보정 후 유의: '유의한 개선'으로 보고 가능")
        elif d.mean() >= mde:
            print(f"      → Δ는 {mde:.2f} 이상이나 보정 후 CI가 0을 포함 → 개선이라 쓰지 않는다")
    return out


def report(OUT, base="B4.본연구", mde=0.07, B=5000):
    """RSN arm 전체를 기준선 대비 판정. bench_models() 반환값을 그대로 넣는다."""
    R = OUT["res"]
    # ★R 로 시작하는 모든 확장 arm (예전엔 R0/R1/R2 만 하드코딩돼 R3~ 가 비교에서 빠졌다)
    import re as _re
    arms = [a for a in R if _re.match(r"^R\d+\.", a)]
    if not arms:
        print("RSN arm 결과가 없습니다. attach_arms() 후 bench_models() 를 실행하세요.")
        return {}
    k = len(arms)
    print(f"\n=== RSN 판정 (기준 {base}, 대응 부트스트랩 B={B}, Bonferroni k={k}) ===")
    print(f"  판정 규율: Δ≥{mde:.2f} 이고 보정 후 CI가 0을 배제해야 '유의한 개선'.")
    print(f"  (73환자 검정력: 매크로F1 95%CI ±0.073 — HANDOFF §2)\n")
    for a in arms:
        m = R[a]["macro"]; lo, hi = R[a]["ci"]
        print(f"  {a:22s} 매크로F1={m:.3f} [{lo:.3f}–{hi:.3f}]  micro={R[a]['micro']:.3f} "
              f"(SEN {R[a]['sen']:.3f}/PREC {R[a]['prec']:.3f})")
    print()
    out = {}
    for a in arms:
        out[a] = paired(R, a, base, B=B, k_bonf=k, mde=mde)
    # 리듬 시퀀스 자체의 기여(형태 통제): R1 vs B3(CNN+RR) — 압축된 RR 대비 시퀀스 이득
    if "R1.RSN(리듬+형태)" in R and "B3.CNN+RR" in R:
        print("\n  [기전 확인] 시퀀스화의 순효과 — 같은 RR 정보를 스칼라로 줬을 때 대비:")
        out["mech"] = paired(R, "R1.RSN(리듬+형태)", "B3.CNN+RR", B=B, k_bonf=k, mde=mde)
    if "R0.RSN(리듬만)" in R and "R1.RSN(리듬+형태)" in R:
        print("\n  [절제] 형태 가지의 기여:")
        out["morph"] = paired(R, "R1.RSN(리듬+형태)", "R0.RSN(리듬만)", B=B, k_bonf=k, mde=mde)
    # ★핵심 단일변수 검정들 — 어느 축이 실제로 일했는지 분해한다.
    #   전체 Δ(vs B4)만 보면 '가장 높은 arm' 이 좋아 보이지만, 증분을 보면
    #   대부분의 이득이 한 축에서 나왔다는 것이 드러날 수 있다.
    for a, b, nm in [
        ("R1.RSN(리듬+형태)", "R5.RSN(시퀀스제거·대조)",
         "[H-G] 리듬 시퀀스의 순수 효과 (다른 조건 완전 동일)"),
        ("R6.RSN(+P/QRS/T)", "R3.RSN(+환자템플릿)",
         "[H-H] 분절(P/QRS/T) 축의 순수 효과"),
        ("R4.RSN(+P파)", "R3.RSN(+환자템플릿)", "[절제] P파 축의 순수 효과"),
        ("R3.RSN(+환자템플릿)", "R1.RSN(리듬+형태)", "[절제] 환자템플릿의 순수 효과"),
    ]:
        if a in R and b in R:
            print(f"\n  {nm}:")
            out[f"{a}|{b}"] = paired(R, a, b, B=B, k_bonf=k, mde=mde)
    print("\n  ※ CI가 0을 포함하면 '개선'이라 쓰지 않는다 (HANDOFF §7-6).")
    # 최고 성적 arm 의 환자별 분해 — 다음 반복의 표적을 고르기 위한 것
    best = max(arms, key=lambda a: R[a]["macro"])
    patient_breakdown(OUT, best)
    return out


def error_profile(OUT, arm, topn=12, show=True):
    """★"이 환자가 왜 낮은가" — 환자별 오류를 FP/FN 으로 쪼개고 공변량과 대조한다.

    patient_breakdown() 이 '누가 낮은가'를 알려준다면, 이것은 '왜'의 첫 단계다.
    같은 낮은 F1 이라도 처방이 정반대이기 때문에 반드시 구분해야 한다:

      · FN 우세(놓침)  : S 를 못 잡는다 → 민감도 문제. 판별축이 약하거나 임계가 높다.
      · FP 우세(헛알람): 정상을 S 라 한다 → 특이도 문제. 그 환자의 '정상'이 특이하다
                         (동성부정맥·잦은 체위변화 등) → 개인 정규화가 필요하다는 신호.
      · 양쪽          : 축 자체가 그 환자에게 안 먹는다 → 새 축이 필요하다.

    함께 보는 공변량(원인 가설을 좁히기 위한 것):
      S유병률   극단적으로 낮으면 F1 은 몇 개만 틀려도 무너진다(지표의 성질).
      RR오염    생리범위 밖 RR 비율. rr_audit 이 센 949개가 특정 환자에 몰렸는지.
      RR변동    med 대비 MAD. 높으면 AF/동성부정맥 의심 → 리듬축이 흔들리는 환자.
    """
    R = OUT["res"].get(arm)
    if R is None:
        print(f"  ⚠ {arm} 없음"); return {}
    if "pred" not in R:
        print("  ⚠ 이 OUT 에는 pred(비트별 판정)가 없습니다 — 예전 코드로 만든 결과입니다.")
        print("    sync() 로 최신 svdb_bench.py 를 받은 뒤 bench_models() 를 다시 돌리면 생깁니다.")
        return {}
    y, pid, v = OUT["y"], OUT["pid"], np.asarray(R["pred"], bool)
    ps = np.array([int(p) for p in np.unique(pid) if (y[pid == p] == 1).sum() > 0])
    f = np.asarray(R["fper"], float)

    # 공변량: 원본 RR 을 OUT["order"] 로 정렬해 맞춘다
    pre = post = None
    if "order" in OUT:
        try:
            _, _, _, P0, Q0 = _rsn_sv()
            o = OUT["order"]
            pre = np.asarray(P0, float)[o] / FS
            post = np.asarray(Q0, float)[o] / FS
        except Exception:
            pass

    rows = []
    for i, p in enumerate(ps):
        m = pid == p
        yp = (y[m] == 1); vp = v[m]
        tp = int((vp & yp).sum()); fp = int((vp & ~yp).sum()); fn = int((~vp & yp).sum())
        prec = tp / max(tp + fp, 1); rec = tp / max(tp + fn, 1)
        contam = hrv = float("nan")
        if pre is not None:
            a = pre[m]; b = post[m]
            contam = float(np.mean((a < RR_LO) | (a > RR_HI) | (b < RR_LO) | (b > RR_HI)))
            med = np.median(a); hrv = float(np.median(np.abs(a - med)) / max(med, 1e-6))
        rows.append(dict(pid=int(p), f1=float(f[i]), tp=tp, fp=fp, fn=fn,
                         prec=prec, rec=rec, n_S=int(yp.sum()), n=int(m.sum()),
                         prev=float(yp.mean()), contam=contam, hrv=hrv))
    rows.sort(key=lambda r: r["f1"])
    if not show:
        return dict(rows=rows)

    def mode(r):
        if r["fn"] > 2 * max(r["fp"], 1): return "FN우세(놓침)"
        if r["fp"] > 2 * max(r["fn"], 1): return "FP우세(헛알람)"
        return "양쪽"

    print(f"\n  [오류 프로파일] {arm} — 최악 {min(topn,len(rows))}명")
    print(f"    {'rec':>4} {'F1':>6} {'PREC':>6} {'REC':>6} {'TP':>5} {'FP':>6} {'FN':>5} "
          f"{'S유병':>6} {'RR오염':>7} {'RR변동':>6}  실패양상")
    for r in rows[:topn]:
        print(f"    {r['pid']:4d} {r['f1']:6.3f} {r['prec']:6.3f} {r['rec']:6.3f} "
              f"{r['tp']:5d} {r['fp']:6d} {r['fn']:5d} {100*r['prev']:5.2f}% "
              f"{100*r['contam']:6.2f}% {r['hrv']:6.3f}  {mode(r)}")

    # 전체 경향 — 낮은 F1 이 무엇과 같이 가는가(원인 가설 좁히기)
    F = np.array([r["f1"] for r in rows])
    PR = np.array([r["prec"] for r in rows]); RC = np.array([r["rec"] for r in rows])
    print(f"\n    [전체 경향] 상관:")
    for k, nm in [("prev", "S유병률"), ("contam", "RR오염률"), ("hrv", "RR변동성")]:
        x = np.array([r[k] for r in rows], float)
        if np.isfinite(x).sum() < 5 or np.nanstd(x) == 0:
            continue
        g = np.isfinite(x)
        c = float(np.corrcoef(F[g], x[g])[0, 1])
        arrow = "낮을수록 F1 낮음" if c > 0.15 else ("높을수록 F1 낮음" if c < -0.15 else "관련 약함")
        print(f"      {nm:<10} ↔ F1  {c:+.3f}   {arrow}")

    # ★유병률은 F1 과의 상관만 보면 놓친다 — precision 과 recall 을 '반대 방향'으로
    #   밀기 때문에 F1 에서 상쇄되기 때문이다. 반드시 쪼개서 본다.
    pv = np.log10(np.maximum(np.array([r["prev"] for r in rows], float), 1e-6))
    cp = float(np.corrcoef(pv, PR)[0, 1]); cr = float(np.corrcoef(pv, RC)[0, 1])
    print(f"\n    [★유병률 효과 분해] log10(유병률) ↔ PREC {cp:+.3f} / REC {cr:+.3f}")
    if cp > 0.2 and cr < -0.2:
        print(f"      → 유병률이 높을수록 정밀도↑·민감도↓. 단일 전역 임계가 저유병 환자에겐")
        print(f"        너무 관대하고 고유병 환자에겐 너무 엄격하다는 신호입니다.")
        print(f"        F1 상관만 보면 두 효과가 상쇄돼 '관련 약함'으로 보입니다 — 반드시 쪼개 볼 것.")
        print(f"        → ceiling_analysis() 로 '임계 문제 vs 판별축 문제'를 판정하세요.")
    # 유병률 3분위별 요약
    prev = np.array([r["prev"] for r in rows], float)
    q = np.quantile(prev, [1/3, 2/3]); gg = np.digitize(prev, q)
    print(f"      {'구간':<10}{'n':>3}{'유병률중앙':>10}{'PREC':>8}{'REC':>8}{'F1':>8}")
    for i, nm in enumerate(["저유병", "중간", "고유병"]):
        m = gg == i
        if not m.any(): continue
        print(f"      {nm:<10}{int(m.sum()):>3}{100*np.median(prev[m]):>9.2f}%"
              f"{PR[m].mean():>8.3f}{RC[m].mean():>8.3f}{F[m].mean():>8.3f}")
    nfn = sum(1 for r in rows[:topn] if mode(r).startswith("FN"))
    nfp = sum(1 for r in rows[:topn] if mode(r).startswith("FP"))
    print(f"\n    최악 {min(topn,len(rows))}명의 실패양상: FN우세 {nfn} / FP우세 {nfp} / "
          f"양쪽 {min(topn,len(rows))-nfn-nfp}")
    print(f"      → FN 우세면 '판별축 부족', FP 우세면 '개인 정규화 부족'이 1순위 가설.")
    return dict(rows=rows)


# ─────────────────────────────────────────────────────────────────────────────
#  문헌 비교용 지표 + 임상 지표(PAC burden)
# ─────────────────────────────────────────────────────────────────────────────
#  문헌 대다수는 **비트풀링(micro) Se/+P** 를 MIT-BIH DS2 에서 보고한다. 본 연구의
#  주지표(환자단위 매크로 F1)와는 다른 잣대이므로 직접 비교할 수 없다(PAPER §2.2).
#  그럼에도 '같은 잣대로 환산하면 얼마인가'는 독자가 반드시 묻는 질문이라 산출한다.
#  ★비교불가 사유를 표와 함께 항상 출력한다 — 숫자만 떼어 인용되는 것을 막기 위함.
LIT_REF = [
    # (연구, 방식, Se, +P, F1, 데이터셋)   None = 미보고
    ("de Chazal 2004",      "LDA, 형태+RR",        0.76, 0.39, None, "MIT-BIH DS2"),
    ("Garcia 2017",         "VCG+PSO",             0.70, None, None, "MIT-BIH DS2"),
    ("Sellami & Hwang 2019", "batch-weighted CNN", 0.82, None, None, "MIT-BIH DS2"),
    ("Wang 2019",           "기호표현+multi-CNN",   None, None, 0.766, "MIT-BIH DS2"),
    ("Adversarial CNN 2021", "적대적 학습",         0.788, 0.908, None, "MIT-BIH DS2"),
]


def literature_table(OUT, arm, show=True):
    """비트풀링(micro) Se/+P/F1 — 문헌과 같은 잣대로 환산.

    ⚠ 이 값을 문헌과 직접 비교하면 안 된다:
      · 데이터셋이 다르다 (본 연구 SVDB 73환자 / 문헌 대다수 MIT-BIH DS2 22레코드)
      · S 유병률이 다르다 (SVDB 6.61% / DS2 3.73%) → +P 는 유병률에 직접 묶인다
      · 분할이 다르다 (환자 GroupKFold / de Chazal DS1-DS2 고정분할)
      · MIT-BIH DS2 는 단일 레코드(#232)가 S 의 75.2% 를 차지해 micro 를 지배한다
        (PAPER §5.2). SVDB 는 최다 14.9% 로 그 성질이 없다.
      → 맥락 제공용이며, 본 연구의 결론은 동일 프로토콜 재구현(B0~B4C)에만 근거한다.
    """
    R = OUT["res"].get(arm)
    if R is None or "pred" not in R:
        print(f"  ⚠ {arm} 의 pred 가 없습니다 — 최신 코드로 재실행하세요."); return {}
    y = np.asarray(OUT["y"]); v = np.asarray(R["pred"], bool)
    out = {}
    for cls, nm in [(1, "S(SVEB)"), (2, "V(VEB)")]:
        yp = (y == cls)
        if cls == 2:
            # V 는 이 3-class 모델에서 별도 임계를 두지 않았다 → 산출 생략(오도 방지)
            continue
        tp = float((v & yp).sum()); fp = float((v & ~yp).sum()); fn = float((~v & yp).sum())
        tn = float((~v & ~yp).sum())
        se = tp / (tp + fn + 1e-9); pp = tp / (tp + fp + 1e-9)
        sp = tn / (tn + fp + 1e-9); f1 = 2 * se * pp / (se + pp + 1e-9)
        out[nm] = dict(Se=se, PP=pp, Sp=sp, F1=f1, TP=int(tp), FP=int(fp), FN=int(fn))
    if not show:
        return out
    s = out["S(SVEB)"]
    print(f"\n  [문헌 비교용 지표] {arm}  — 비트풀링(micro), S vs rest")
    print(f"    Se(민감도) {s['Se']:.3f}   +P(정밀도) {s['PP']:.3f}   "
          f"Sp(특이도) {s['Sp']:.3f}   F1 {s['F1']:.3f}")
    print(f"    TP {s['TP']:,}  FP {s['FP']:,}  FN {s['FN']:,}")
    print(f"\n    {'연구':<22}{'방식':<22}{'Se':>7}{'+P':>7}{'F1':>7}  데이터셋")
    for nmr, how, se, pp, f1, ds in LIT_REF:
        f = lambda x: f"{x:.3f}" if x is not None else "  —  "
        print(f"    {nmr:<22}{how:<22}{f(se):>7}{f(pp):>7}{f(f1):>7}  {ds}")
    print(f"    {'▶ 본 연구 ('+arm.split('.')[0]+')':<44}"
          f"{s['Se']:>7.3f}{s['PP']:>7.3f}{s['F1']:>7.3f}  SVDB 73환자")
    print(f"\n    ⚠ 직접 비교 불가: 데이터셋·유병률(SVDB 6.61% vs DS2 3.73%)·분할이 다르다.")
    print(f"       특히 +P 는 유병률에 직접 묶이고, MIT-BIH DS2 는 #232 한 레코드가")
    print(f"       S 의 75.2% 를 차지해 micro 를 지배한다(SVDB 최다 14.9%).")
    print(f"       본 연구의 결론은 동일 프로토콜로 재구현한 B0~B4C 비교에만 근거한다.")
    return out


def burden_analysis(OUT, arm, bands=(1.0, 5.0, 10.0), show=True):
    """PAC(SVEB) burden 추정 정확도 — 임상에서 실제로 쓰는 양.

    ★왜 F1 과 별도로 봐야 하는가: 임상 판단은 '이 박이 PAC 인가'가 아니라
      '이 환자의 PAC 부담이 몇 %인가'로 내려진다(PAC burden 은 심방세동 발생·
      뇌졸중 위험의 예측인자로 쓰인다). burden 은 **개수의 비율**이라 위양성과
      위음성이 서로 상쇄될 수 있다 — F1 이 중간이어도 burden 추정은 정확할 수 있고,
      그 반대도 가능하다. 둘은 다른 질문이므로 따로 보고한다.

    산출: 환자별 예측 burden vs 실제 burden 의 Pearson/Spearman r,
          Bland-Altman(편향 + 일치한계), 임상 구간 일치율.
    """
    R = OUT["res"].get(arm)
    if R is None or "pred" not in R:
        print(f"  ⚠ {arm} 의 pred 가 없습니다 — 최신 코드로 재실행하세요."); return {}
    y = np.asarray(OUT["y"]); pid = np.asarray(OUT["pid"]); v = np.asarray(R["pred"], bool)
    ps = np.array([int(p) for p in np.unique(pid) if (y[pid == p] == 1).sum() > 0])
    true_b = np.array([100.0 * (y[pid == p] == 1).mean() for p in ps])
    pred_b = np.array([100.0 * v[pid == p].mean() for p in ps])
    d = pred_b - true_b
    bias = float(d.mean()); sd = float(d.std(ddof=1))
    loa = (bias - 1.96 * sd, bias + 1.96 * sd)
    pr = float(np.corrcoef(pred_b, true_b)[0, 1])
    rk = lambda x: np.argsort(np.argsort(x))
    sp = float(np.corrcoef(rk(pred_b), rk(true_b))[0, 1])
    band = lambda x: np.digitize(x, bands)
    agree = float((band(pred_b) == band(true_b)).mean())
    out = dict(pid=ps, true=true_b, pred=pred_b, pearson=pr, spearman=sp,
               bias=bias, sd=sd, loa=loa, band_agree=agree)
    if not show:
        return out
    print(f"\n  [PAC burden 추정 정확도] {arm}   n={len(ps)}환자")
    print(f"    실제 burden  중앙 {np.median(true_b):5.2f}%  범위 {true_b.min():.2f}~{true_b.max():.2f}%")
    print(f"    예측 burden  중앙 {np.median(pred_b):5.2f}%  범위 {pred_b.min():.2f}~{pred_b.max():.2f}%")
    print(f"    Pearson r = {pr:.3f}    Spearman ρ = {sp:.3f}")
    print(f"    Bland-Altman: 편향 {bias:+.2f}%p,  일치한계 [{loa[0]:+.2f}, {loa[1]:+.2f}]%p")
    print(f"      (편향>0 = 과대추정. 일치한계는 개별 환자 오차가 95% 들어가는 구간)")
    lab = [f"<{bands[0]:g}%"] + [f"{bands[i]:g}~{bands[i+1]:g}%" for i in range(len(bands)-1)] \
          + [f"≥{bands[-1]:g}%"]
    print(f"\n    임상 구간 일치율 {100*agree:.1f}%  (구간: {', '.join(lab)})")
    hdr = "실제 \\ 예측"
    print("      " + hdr.ljust(10) + "".join(f"{l:>10}" for l in lab))
    for i, l in enumerate(lab):
        row = [int(((band(true_b) == i) & (band(pred_b) == j)).sum()) for j in range(len(lab))]
        print(f"      {l:<10}" + "".join(f"{r:>10d}" for r in row))
    print(f"\n    ※ burden 은 위양성·위음성이 상쇄될 수 있어 F1 과 다른 질문이다.")
    print(f"       r 이 높고 편향이 작으면 '개별 비트는 틀려도 환자 부담 추정은 쓸 만하다'는 뜻.")
    return out


def compare_arms(OUT, a, b, strat="prev", nbin=3, show=True):
    """두 arm 을 **유병률 구간별로** 비교한다 — 평균만 보면 안 보이는 것을 드러낸다.

    ★왜: 환자별 효과가 방향이 다르면 평균에서 상쇄된다(§6.2 에서 유병률이 정밀도와
      민감도를 반대로 미는 것을 이미 겪었다). 특히 '환자별 적응' 계열은 어떤 구간을
      돕고 어떤 구간을 해치는지 봐야 실패 원인을 특정할 수 있다.
    """
    R = OUT["res"]
    if a not in R or b not in R:
        print(f"  ⚠ {a} 또는 {b} 없음"); return {}
    y, pid = OUT["y"], OUT["pid"]
    ps = np.array([int(p) for p in np.unique(pid) if (y[pid == p] == 1).sum() > 0])
    fa = np.asarray(R[a]["fper"], float); fb = np.asarray(R[b]["fper"], float)
    prev = np.array([float((y[pid == p] == 1).mean()) for p in ps])
    q = np.quantile(prev, np.linspace(0, 1, nbin + 1)[1:-1])
    g = np.digitize(prev, q)
    if not show:
        return dict(pid=ps, a=fa, b=fb, prev=prev, grp=g)
    print(f"\n  [구간별 비교] {a}  −  {b}")
    print(f"    {'구간':<10}{'n':>3}{'유병률중앙':>10}{b[:14]:>16}{a[:14]:>16}{'Δ':>9}")
    for i in range(nbin):
        m = g == i
        if not m.any(): continue
        nm = ["저유병", "중간", "고유병"][i] if nbin == 3 else f"Q{i+1}"
        print(f"    {nm:<10}{int(m.sum()):>3}{100*np.median(prev[m]):>9.2f}%"
              f"{fb[m].mean():>16.3f}{fa[m].mean():>16.3f}{fa[m].mean()-fb[m].mean():>+9.3f}")
    d = fa - fb
    print(f"    {'전체':<10}{len(d):>3}{'':>10}{fb.mean():>16.3f}{fa.mean():>16.3f}{d.mean():>+9.3f}")
    w, l = int((d > 0.01).sum()), int((d < -0.01).sum())
    print(f"    개선 {w}명 / 악화 {l}명 / 변화없음 {len(d)-w-l}명")
    if l > w:
        print(f"      → 악화가 더 많다. 구간별 부호가 갈리면 '방향이 틀린 것',"
              f" 전 구간에서 악화면 '적합 자체가 틀린 것'이다.")
    return dict(pid=ps, a=fa, b=fb, prev=prev, grp=g, delta=d)


def ceiling_analysis(OUT, arm, show=True):
    """★결정적 진단 — '순위(판별축)' 문제인가 '임계(동작점)' 문제인가.

    두 실패는 처방이 완전히 다른데 이진 판정만 보면 구분되지 않는다:
      · 순위가 나쁘다 → 점수 자체가 S 와 N 을 못 가른다 → **새 판별축이 필요**
      · 순위는 좋은데 임계가 안 맞는다 → 환자마다 최적 동작점이 다르다
        → **라벨프리 환자별 임계 적응이 필요** (모델은 그대로 둬도 된다)

    세 수치를 나란히 놓는다:
      현재        지금 쓰는 전역 임계의 환자매크로 F1
      오라클임계  환자마다 F1 최적 임계를 골랐을 때 (★테스트 라벨 사용 = 상한 참고용)
      PR-AUC      임계 무관 순위 품질

    ★오라클은 테스트 라벨을 쓰므로 **달성 가능한 성능이 아니다**(HANDOFF §7-1).
      '동작점만 완벽히 맞추면 어디까지 가는가'라는 상한을 재는 계측기일 뿐이다.
      현재와 오라클의 격차가 크면 임계 문제, 작으면 판별축 문제다.
    """
    R = OUT["res"].get(arm)
    if R is None or R.get("score") is None:
        print(f"  ⚠ {arm} 의 score 가 없습니다 — 최신 svdb_bench.py 로 재실행하면 저장됩니다.")
        return {}
    from sklearn.metrics import average_precision_score
    y, pid, s = OUT["y"], OUT["pid"], np.asarray(R["score"], float)
    ps = np.array([int(p) for p in np.unique(pid) if (y[pid == p] == 1).sum() > 0])
    cur = np.asarray(R["fper"], float)
    orc = np.zeros(len(ps)); ap = np.zeros(len(ps))
    for i, p in enumerate(ps):
        m = pid == p
        yp = (y[m] == 1); sp = s[m]
        ap[i] = average_precision_score(yp.astype(int), sp) if yp.any() and (~yp).any() else 1.0
        ts = np.unique(np.quantile(sp, np.linspace(0.0, 1.0, 200)))
        best = 0.0
        for t in ts:
            v = sp >= t
            tp = float((v & yp).sum()); fp = float((v & ~yp).sum()); fn = float((~v & yp).sum())
            pr = tp / (tp + fp + 1e-9); re = tp / (tp + fn + 1e-9)
            best = max(best, 2 * pr * re / (pr + re + 1e-9))
        orc[i] = best
    if not show:
        return dict(pid=ps, cur=cur, oracle=orc, prauc=ap)

    print(f"\n  [천장 분석] {arm}   n={len(ps)}")
    print(f"    현재(전역 임계)      매크로 F1 = {cur.mean():.3f}")
    print(f"    오라클 환자별 임계   매크로 F1 = {orc.mean():.3f}   (★테스트 라벨 사용 = 상한)")
    print(f"    임계 무관 PR-AUC     평균      = {ap.mean():.3f}")
    gap = orc.mean() - cur.mean()
    print(f"\n    동작점 격차 = {gap:+.3f}")
    if gap >= 0.10:
        print(f"      → ★임계(동작점) 문제가 큽니다. 순위는 이미 이만큼 좋은데 전역 임계가")
        print(f"        환자별 최적점을 못 맞추고 있습니다. 라벨프리 환자별 임계 적응이 1순위.")
    elif gap >= 0.05:
        print(f"      → 임계 문제가 유의미하지만 판별축 개선도 함께 필요합니다.")
    else:
        print(f"      → 임계로 얻을 여지가 작습니다. 판별축(새 입력 축)이 1순위.")
    # 유병률 구간별로 어디서 격차가 큰가
    prev = np.array([float((y[pid == p] == 1).mean()) for p in ps])
    q = np.quantile(prev, [1/3, 2/3]); g = np.digitize(prev, q)
    print(f"\n    유병률 구간별 (동작점 격차가 어디에 몰려 있나):")
    print(f"      {'구간':<12}{'n':>3}{'유병률중앙':>10}{'현재':>8}{'오라클':>8}{'격차':>8}{'PR-AUC':>8}")
    for i, nm in enumerate(["저유병", "중간", "고유병"]):
        m = g == i
        if not m.any(): continue
        print(f"      {nm:<12}{int(m.sum()):>3}{100*np.median(prev[m]):>9.2f}%"
              f"{cur[m].mean():>8.3f}{orc[m].mean():>8.3f}{orc[m].mean()-cur[m].mean():>+8.3f}{ap[m].mean():>8.3f}")
    return dict(pid=ps, cur=cur, oracle=orc, prauc=ap, gap=float(gap))


# ─────────────────────────────────────────────────────────────────────────────
#  결과 영속화 — 런타임이 끊겨도 OUT 을 잃지 않게 (긴 여정용)
# ─────────────────────────────────────────────────────────────────────────────
#  Colab 런타임은 몇십 분만 놀아도 끊긴다. 끊기면 메모리의 OUT(수십 분 GPU 학습의
#  산출물)이 통째로 사라진다. bench_models() 는 다시 돌리면 되지만 시간이 아깝다.
#  → 끝나면 바로 Drive 에 저장하고, 다음 세션에서 학습 없이 불러와 report/분해만 한다.
def save_out(OUT, name="rsn_last", base=None):
    """OUT 을 Drive 에 저장(pickle). 반환: 저장 경로.

    ★덮어쓰기 보호: 기존 파일이 지금 저장하려는 것보다 **더 많은 arm** 을 갖고 있으면
      (예: R0/R1/R2 가 든 결과를 B 계열만 있는 결과로 덮으려 할 때) 자동으로
      .bak.pkl 로 백업하고 경고한다. 수십 분 GPU 학습 결과를 실수로 날리지 않기 위함.
    """
    import os
    import pickle
    import shutil
    base = base or _BASE
    sha = globals().get("CODE_SHA")
    meta = dict(code_sha=sha)                          # 어떤 코드가 낸 결과인지 함께 박는다
    p = f"{base}/{name}.pkl"
    new_arms = set(OUT.get("res", {}))
    if os.path.exists(p):
        try:
            with open(p, "rb") as f:
                old = pickle.load(f)
            oo = old.get("OUT", old) if isinstance(old, dict) else old
            old_arms = set(oo.get("res", {}))
            lost = old_arms - new_arms
            if lost:
                bak = f"{base}/{name}.bak.pkl"
                shutil.copyfile(p, bak)
                print(f"  ⚠ 기존 저장본에만 있던 arm 이 사라집니다: {sorted(lost)}")
                print(f"    → 백업했습니다: {bak}  (load_out(name='{name}.bak') 로 복원)")
        except Exception:
            pass
    with open(p, "wb") as f:
        pickle.dump({"OUT": OUT, "meta": meta}, f)
    macros = {a: OUT["res"][a]["macro"] for a in OUT["res"]}
    print(f"✔ 저장 {p}")
    print(f"  코드버전 {str(sha)[:10]}  |  arms: " +
          ", ".join(f"{a.split('.')[0]}={m:.3f}" for a, m in macros.items()))
    return p


def merge_out(new_OUT, old_OUT, verbose=True):
    """새로 돌린 arm 결과를 옛 결과와 합친다 — **정렬이 완전히 같을 때만**.

    ★왜 안전한가: 폴드가 결정론적이다(GroupKFold + GroupShuffleSplit(random_state=rep)).
      같은 데이터·같은 n_rep·k 면 환자 배정과 평가 순서가 동일하므로, 따로 돌린
      결과라도 '같은 환자의 F1' 끼리 짝지을 수 있다 → 대응 부트스트랩이 유효하다.

    ★그래서 무엇을 검증하는가: y / pid / order 가 **완전히 일치**하는지. 하나라도
      다르면 두 실행이 다른 분할을 본 것이므로 합치기를 거부한다. 조용히 잘못된
      비교를 만드는 것보다 멈추는 편이 낫다.

    이름이 겹치면 new_OUT 이 이긴다(방금 돌린 것이 최신).
    """
    for k in ("y", "pid"):
        a, b = np.asarray(new_OUT.get(k)), np.asarray(old_OUT.get(k))
        if a.shape != b.shape or not np.array_equal(a, b):
            raise ValueError(
                f"합칠 수 없습니다: '{k}' 가 다릅니다(shape {a.shape} vs {b.shape}).\n"
                f"  두 실행이 서로 다른 분할을 봤다는 뜻입니다 — 데이터·n_rep·k 가\n"
                f"  같은지 확인하세요. 다르면 전부 다시 돌려야 합니다.")
    if "order" in new_OUT and "order" in old_OUT:
        if not np.array_equal(np.asarray(new_OUT["order"]), np.asarray(old_OUT["order"])):
            raise ValueError("합칠 수 없습니다: 'order'(평가 순서)가 다릅니다.")
    out = dict(old_OUT)
    out.update({k: v for k, v in new_OUT.items() if k != "res"})
    res = dict(old_OUT.get("res", {}))
    res.update(new_OUT.get("res", {}))
    out["res"] = res
    out["arms"] = list(res)
    if verbose:
        fresh = sorted(new_OUT.get("res", {}))
        kept = [a for a in old_OUT.get("res", {}) if a not in fresh]
        print(f"✔ 병합 완료 (정렬 검증 통과: 환자·폴드 동일)")
        print(f"  새로 학습: {fresh}")
        print(f"  재사용   : {kept}")
        print(f"  → report(OUT) 로 전체 대응비교가 그대로 가능합니다.")
    return out


def load_out(name="rsn_last", base=None, verbose=True):
    """Drive 에서 OUT 복원. 학습 없이 report(OUT)/patient_breakdown() 가능."""
    import pickle
    base = base or _BASE
    p = f"{base}/{name}.pkl"
    with open(p, "rb") as f:
        d = pickle.load(f)
    OUT = d["OUT"] if isinstance(d, dict) and "OUT" in d else d
    if verbose:
        sha = (d.get("meta") or {}).get("code_sha") if isinstance(d, dict) else None
        print(f"✔ 복원 {p}  (코드버전 {str(sha)[:10]})")
        print(f"  → report(OUT) 또는 patient_breakdown(OUT, 'R1.RSN(리듬+형태)') 바로 가능")
    return OUT


def patient_breakdown(OUT, arm, topn=10, targets=(0.50, 0.90, 0.99), show=True):
    """환자별 F1 분해 — '모든 ECG를 정답에' 목표의 실제 병목을 드러낸다.

    ★왜 이게 필요한가: 환자단위 매크로 F1 은 환자별 F1 의 '평균'이다. 따라서
      매크로 0.99 는 '73명 전원이 0.99 이상'을 뜻한다. 평균을 조금 올리는 개선과
      최악 환자를 끌어올리는 개선은 완전히 다른 작업이고, 목표가 후자라면
      **분산(꼬리)이 병목이지 평균이 아니다**. PAPER §5.3 의 σ≈0.32 가 그 크기다.
      매 반복에서 '어떤 환자가 여전히 실패하는가'를 보고 다음 수를 정하기 위한 도구.
    """
    y, pid = OUT["y"], OUT["pid"]
    ps = np.array([int(p) for p in np.unique(pid) if (y[pid == p] == 1).sum() > 0])
    f = np.asarray(OUT["res"][arm]["fper"], float)
    if len(f) != len(ps):
        print(f"  ⚠ 정렬 불일치(fper {len(f)} vs 환자 {len(ps)}) — 건너뜀"); return {}
    nS = np.array([int((y[pid == p] == 1).sum()) for p in ps])
    nB = np.array([int((pid == p).sum()) for p in ps])
    o = np.argsort(f)
    res = dict(pid=ps, f1=f, n_S=nS, n_beat=nB)
    if not show:
        return res
    q = np.percentile(f, [0, 25, 50, 75, 100])
    print(f"\n  [환자별 분해] {arm}   n={len(f)}")
    print(f"    평균 {f.mean():.3f}  |  최소 {q[0]:.3f}  Q1 {q[1]:.3f}  중앙 {q[2]:.3f}  "
          f"Q3 {q[3]:.3f}  최대 {q[4]:.3f}   (표준편차 {f.std(ddof=1):.3f})")
    for t in targets:
        k = int((f >= t).sum())
        print(f"    F1 ≥ {t:.2f} 인 환자: {k}/{len(f)} ({100*k/len(f):.0f}%)"
              f"{'   ← 매크로 ' + format(t,'.2f') + ' 은 이 값이 100% 여야 달성' if t == max(targets) else ''}")
    print(f"    최악 {min(topn, len(f))}명 (여기가 다음 반복의 표적):")
    print(f"      {'rec':>5} {'F1':>6} {'S비트':>7} {'총비트':>8} {'S비율':>7}")
    for i in o[:topn]:
        print(f"      {ps[i]:5d} {f[i]:6.3f} {nS[i]:7d} {nB[i]:8d} {100*nS[i]/nB[i]:6.2f}%")
    gap = float(np.maximum(max(targets) - f, 0).mean())
    print(f"    목표 {max(targets):.2f} 까지 평균 결손 {gap:.3f} "
          f"(전원 달성 시 매크로 = {max(targets):.2f})")
    return res


def repro_check(OUT, arm="R1.RSN(리듬+형태)", base="B4.본연구", n_rep=3, mde=0.07):
    """재현성 점검 안내 — N3(SMOTE 0.821→0.796) 재발 방지(HANDOFF §7-4).
       실제 재실행은 비용이 크므로, 여기서는 '무엇을 확인해야 하는가'를 고정한다."""
    R = OUT["res"]
    if arm not in R:
        print(f"{arm} 없음"); return
    d = np.asarray(R[arm]["fper"]) - np.asarray(R[base]["fper"])
    se = d.std(ddof=1) / np.sqrt(len(d))
    print(f"\n=== 재현성 점검 계획 (HANDOFF §7-4) ===")
    print(f"  현재 Δ({arm} − {base}) = {d.mean():+.3f}, 환자간 SE = {se:.3f} (n={len(d)})")
    print(f"  1) 시드 재현: bench_models(n_rep={n_rep}) 로 재실행 → Δ 가 {mde:.2f} 위에 머무는지.")
    print(f"  2) 시드 분산: attach_arms(n_seed=5) 는 '앙상블 이득' 확인용이며 주 비교에 쓰지 않는다.")
    print(f"  3) Δ 가 재실행에서 {mde:.2f} 아래로 내려가면 → 음성 결과로 PAPER §7 에 기록한다.")
    print(f"  ★좋은 결과일수록 먼저 의심한다. N3(SMOTE)는 재실행에서 무너졌다.")


# ─────────────────────────────────────────────────────────────────────────────
#  6. RR 데이터 위생 점검
# ─────────────────────────────────────────────────────────────────────────────
def rr_audit(verbose=True):
    """svdb_data.npz 의 RR 열 위생 점검.

    왜 필요한가: svdb_prep.py 는 rr=np.diff(ann.sample) 로 RR 을 만든 뒤 AAMI 밖
    심볼을 '비트'에서만 제외한다. WFDB 주석열에는 '+'(리듬 변경) 같은 비-비트 주석이
    자기 샘플 위치를 갖고 섞여 있어, 그 직후 비트의 pre_rr 이 0에 가까워질 수 있다.
    이 경우 기존 RHYTHM innovation 은 거대한 잔차를 만든다(step49 가 MIT-BIH 에서
    겪은 '스케일 폭발'과 같은 종류). rr_context 는 RR_LO/RR_HI 밖을 결측 처리하지만,
    실제로 얼마나 되는지는 데이터로 확인해야 한다.
    """
    _, y, pid, pre, post = _rsn_sv()
    a = np.asarray(pre, np.float64) / FS
    b = np.asarray(post, np.float64) / FS
    bad = (a < RR_LO) | (a > RR_HI) | (b < RR_LO) | (b > RR_HI)
    if verbose:
        print("=== RR 위생 점검 ===")
        print(f"  비트 {len(a)}  pre_rr 중앙 {np.median(a):.3f}s  post_rr 중앙 {np.median(b):.3f}s")
        print(f"  생리범위[{RR_LO},{RR_HI}]s 밖: {int(bad.sum())} ({100*bad.mean():.3f}%)")
        for lo, hi, nm in [(0, 0.05, "<50ms(주석 아티팩트 의심)"), (0.05, RR_LO, "50~200ms"),
                           (RR_HI, 1e9, ">3s")]:
            k = int((((a >= lo) & (a < hi)) | ((b >= lo) & (b < hi))).sum())
            print(f"    {nm:24s} {k}")
        if bad.any():
            recs = np.unique(pid[bad])
            print(f"  영향 레코드 {len(recs)}개: {recs[:12].tolist()}{' ...' if len(recs)>12 else ''}")
            print(f"    S 비트 중 해당: {int((bad & (y==1)).sum())} / S 전체 {int((y==1).sum())}")
        print("  → rr_context() 는 이 구간을 mask=0 으로 끊고 통계에서 제외한다.")
    return dict(n_bad=int(bad.sum()), frac=float(bad.mean()))


# ─────────────────────────────────────────────────────────────────────────────
#  7. 자기검증 (데이터·GPU 없이 실행 가능)
# ─────────────────────────────────────────────────────────────────────────────
def _synth(n_rec=6, n_beat=400, seed=0):
    """합성 SVDB: 정상 동율동 + APC(조기 + 불완전 보상성 휴지) + PVC(조기 + 완전 보상).
       형태는 N/S 를 거의 구분 못 하게, V만 넓은 QRS 로 만든다(실제 생리와 동형)."""
    rng = np.random.RandomState(seed)
    B = []; Y = []; P = []; PRE = []; POST = []
    # ★실제 규약과 맞춘다: R 피크는 인덱스 _RPRE=100, 길이 300.
    #   P파는 R-55 부근(= 인덱스 45) — P_LO..P_HI(5..85) 창 안에 들어온다.
    ix = np.arange(300.0)
    gauss = lambda c, w: np.exp(-((ix - c) / w) ** 2)
    qrs, qrs_w = gauss(100, 6), gauss(100, 17)          # 정상 QRS / 넓은 QRS(V)
    p_sinus = 0.18 * gauss(45, 9)                        # 동성 P (양성, 정위치)
    p_ecto = -0.14 * gauss(38, 7)                        # 이소성 P (극성·시점·크기 다름)
    for r in range(n_rec):
        base = rng.uniform(0.65, 1.05)                    # 환자별 심박수 차이
        rrs = []; labs = []
        prev_ect = False
        for i in range(n_beat):
            u = rng.rand()
            if prev_ect:
                labs.append(0); rrs.append(base * rng.uniform(1.05, 1.25)); prev_ect = False
            elif u < 0.09:
                labs.append(1); rrs.append(base * rng.uniform(0.55, 0.75)); prev_ect = True
            elif u < 0.15:
                labs.append(2); rrs.append(base * rng.uniform(0.50, 0.70)); prev_ect = True
            else:
                labs.append(0); rrs.append(base * rng.uniform(0.94, 1.06))
        rrs = np.array(rrs); labs = np.array(labs)
        for i in range(n_beat):
            if labs[i] == 2:                     # V: 넓은 QRS + P 없음(방실 해리)
                w = qrs_w; pw = 0.0 * ix
            elif labs[i] == 1:                   # S: QRS 는 정상과 같고 P 만 이소성
                w = qrs; pw = p_ecto
            else:                                # N: 정상
                w = qrs; pw = p_sinus
            base = w + pw
            seg = np.stack([base, 0.7 * base]) + rng.randn(2, 300) * 0.02
            seg = (seg - seg.mean(1, keepdims=True)) / (seg.std(1, keepdims=True) + 1e-6)
            B.append(seg.astype("float32")); Y.append(int(labs[i])); P.append(r)
            PRE.append(rrs[i] * FS)
            POST.append(rrs[i + 1] * FS if i + 1 < n_beat else rrs[i] * FS)
    return (np.stack(B), np.array(Y, np.int64), np.array(P, np.int64),
            np.array(PRE, "float32"), np.array(POST, "float32"))


def selftest(train=True):
    """설계 불변식 검증. 실패하면 즉시 예외."""
    ok = lambda c, m: (_ for _ in ()).throw(AssertionError(m)) if not c else print(f"  ✔ {m}")
    print("=== svdb_rhythm 자기검증 ===")
    beat, y, pid, pre, post = _synth()
    set_data(beat, y, pid, pre, post)
    try:
        c = rr_context(pre, post, pid, verbose=True)
        S, A = c["seq"], c["aux"]
        ok(S.shape == (len(y), 4, 2 * K_CTX + 1), f"seq 형상 {S.shape}")
        ok(A.shape[1] == 10, f"aux 차원 {A.shape[1]} (스칼라5 + Poincaré5)")
        ok(np.isfinite(S).all() and np.isfinite(A).all(), "NaN/Inf 없음")
        ok(np.abs(S[:, :3]).max() <= 1.5 + 1e-5, f"채널 유계 max={np.abs(S[:,:3]).max():.3f}")
        ok(set(np.unique(S[:, 3])) <= {0.0, 1.0}, "mask 는 0/1")

        # 경계 차단: 각 레코드 첫 비트는 과거 슬롯이 모두 무효여야 한다
        first = np.array([np.flatnonzero(pid == p)[0] for p in np.unique(pid)])
        ok(S[first, 3, :K_CTX].sum() == 0, "레코드 경계에서 과거 슬롯 차단")
        last = np.array([np.flatnonzero(pid == p)[-1] for p in np.unique(pid)])
        ok(S[last, 3, K_CTX + 2:].sum() == 0, "레코드 경계에서 미래 슬롯 차단")

        # 인과성: causal_only 면 k>=2 슬롯이 전부 무효
        c2 = rr_context(pre, post, pid, causal_only=True, verbose=False)
        ok(c2["seq"][:, 3, K_CTX + 2:].sum() == 0, "causal_only 에서 미래 슬롯 0")

        # 라벨 불변: y 를 뒤섞어도 문맥이 동일해야 한다(라벨 미사용 증명)
        c3 = rr_context(pre, post, pid, verbose=False)
        ok(np.array_equal(c3["seq"], S), "문맥은 라벨에 의존하지 않음(결정론적)")

        # 환자 이동불변: RR 을 통째로 1.3배(=느린 심박) 해도 무차원 채널은 거의 불변
        c4 = rr_context(pre * 1.3, post * 1.3, pid, verbose=False)
        dif = np.abs(c4["seq"][:, :3] - S[:, :3]).max()
        ok(dif < 0.05, f"심박수 스케일 불변 (최대편차 {dif:.4f})")

        # 건너뛴 비트(구멍) 처리: post[j] != pre[j+1] 이면 j 를 넘는 슬롯이 끊겨야 한다
        po = post.copy()
        jj = int(np.flatnonzero(pid == 0)[100])
        po[jj] = po[jj] * 1.7                              # 인위적 불연속(비트 유실 모사)
        c6 = rr_context(pre, po, pid, verbose=False)
        ok(c6["info"]["gaps"] >= 1, "건너뜀(구멍) 검출")
        ok(c6["seq"][jj, 3, K_CTX + 1:].sum() == 0,
           "구멍 이후 슬롯 차단(가짜 연속성 학습 방지)")
        ok(c6["seq"][jj + 1, 3, :K_CTX].sum() == 0, "구멍 이전 슬롯 차단(반대 방향)")
        ok(c6["seq"][jj + 4, 3, :K_CTX].sum() > 0, "구멍과 무관한 비트는 영향 없음")

        # 생리범위 밖 주입 → 마스킹되는지
        p2 = pre.copy(); p2[5] = 3.0                      # 3 샘플 = 8ms
        c5 = rr_context(p2, post, pid, verbose=False)
        ok(c5["info"]["implausible"] >= 1, "생리범위 밖 구간 검출")
        ok(c5["seq"][5, 3, K_CTX] == 0, "생리범위 밖 슬롯 mask=0")

        # 신호 존재 확인: S 비트의 ch2(innov) k=0 이 N 비트보다 유의하게 낮아야(조기=음의 잔차)
        i0 = S[:, 2, K_CTX]
        ok(i0[y == 1].mean() < i0[y == 0].mean() - 0.1,
           f"조기성 신호 방향 (S {i0[y==1].mean():+.3f} < N {i0[y==0].mean():+.3f})")

        if train:
            import torch
            M = _rsn(4, S.shape[2], A.shape[1])
            out = M(torch.from_numpy(S[:8]), torch.from_numpy(beat[:8]), torch.from_numpy(A[:8]))
            ok(tuple(out.shape) == (8, 3), f"모델 출력 형상 {tuple(out.shape)}")
            npar = sum(p.numel() for p in M.parameters())
            ok(npar < 200000, f"파라미터 {npar:,} (소형 유지)")

            # 환자템플릿·P파 가지 (R3/R4)
            refs = np.zeros_like(beat)
            for p in np.unique(pid):
                m = pid == p
                refs[m] = np.median(beat[m], 0, keepdims=True)
            M2 = _rsn(4, S.shape[2], A.shape[1], use_ref=True, segs=("P", "QRS", "T"))
            o2 = M2(torch.from_numpy(S[:8]), torch.from_numpy(beat[:8]),
                    torch.from_numpy(A[:8]), torch.from_numpy(refs[:8]))
            ok(tuple(o2.shape) == (8, 3), f"R6(+P/QRS/T) 출력 형상 {tuple(o2.shape)}")
            ok(sum(p.numel() for p in M2.parameters()) < 400000, "R6 도 소형 유지")
            # R5: 리듬 시퀀스 제거 대조군
            M5 = _rsn(4, S.shape[2], A.shape[1], use_seq=False)
            ok(tuple(M5(torch.from_numpy(S[:4]), torch.from_numpy(beat[:4]),
                        torch.from_numpy(A[:4])).shape) == (4, 3), "R5(시퀀스제거) 출력 형상")
            ok(not any("rz" in n for n, _ in M5.named_parameters()),
               "R5 에는 리듬 TCN 파라미터가 아예 없음(순수 대조군)")
            # 분절 창이 서로 겹치지 않고 비트 범위 안에 있는지
            for nm, (lo, hi) in SEGS.items():
                ok(0 <= lo < hi <= 300, f"분절 {nm} 창 [{lo},{hi}] 유효")
            # ref 없이 호출해도 죽지 않아야(폴백)
            ok(tuple(M2(torch.from_numpy(S[:4]), torch.from_numpy(beat[:4]),
                        torch.from_numpy(A[:4])).shape) == (4, 3), "ref 미제공 시 폴백 동작")
            # P 창이 실제로 P파를 담고 있는지 — 합성 데이터로 확인
            pn = beat[y == 0][:, 0, P_LO:P_HI].mean(0)
            pspk = beat[y == 1][:, 0, P_LO:P_HI].mean(0)
            ok(np.abs(pn - pspk).max() > 0.1,
               f"P 창[{P_LO}:{P_HI}]에서 N/S 가 구분됨 (최대차 {np.abs(pn-pspk).max():.3f})")

            # 실제 학습 1회 — 환자분리 분할에서 S 를 잡는지
            tr = np.flatnonzero(pid < 4); cal = np.flatnonzero(pid == 4); te = np.flatnonzero(pid == 5)
            Sw = float((y[tr] == 0).sum() / max((y[tr] == 1).sum(), 1))
            mc = np.array([0.3, 0.5, 0.4], "float32")
            pc, pt = _fit_predict_rsn(S, A, beat, y, tr, cal, te, Sw, mc, 0, epochs=4)
            ok(pc.shape == (len(cal), 3) and pt.shape == (len(te), 3), "예측 형상")
            from sklearn.metrics import average_precision_score
            ap = average_precision_score((y[te] == 1).astype(int), pt[:, 1])
            base = (y[te] == 1).mean()
            ok(ap > 3 * base, f"합성 S 검출 PR-AUC {ap:.3f} (기저 {base:.3f})")

        # arm 등록 계약 (하니스 스텁)
        g = globals()
        saved = g.get("register_arm")
        reg = {}
        g["register_arm"] = lambda n, f: reg.__setitem__(n, f)
        try:
            n = attach_arms(which=("R0","R1","R2","R3","R4","R5","R6","R7"), verbose=False)
            ok(n == 8 and len(reg) == 8, f"arm {n}개 등록")
            if train:
                ctx = dict(beats=beat, y=y, pid=pid, tr=np.flatnonzero(pid < 4),
                           cal=np.flatnonzero(pid == 4), te=np.flatnonzero(pid == 5),
                           Sw=8.0, mc=np.array([.3, .5, .4], "float32"), seed=0,
                           best_t=lambda s, yy: float(np.quantile(s, 0.9)))
                r = reg["R1.RSN(리듬+형태)"](ctx)
                ok(isinstance(r, tuple) and len(r) == 2, "arm 반환 계약((결정, 점수) 튜플)")
                v, sc = r
                ok(v.dtype == bool and len(v) == len(ctx["te"]), "결정 = bool[len(te)]")
                ok(len(sc) == len(ctx["te"]) and np.isfinite(sc).all(), "점수 = float[len(te)]")
        finally:
            if saved is None: g.pop("register_arm", None)
            else: g["register_arm"] = saved

        # paired 판정 로직
        R = {"a": dict(fper=np.full(73, 0.60)), "b": dict(fper=np.full(73, 0.52))}
        r = paired(R, "a", "b", B=500, k_bonf=3, show=False)
        ok(abs(r["delta"] - 0.08) < 1e-9 and r["meets_mde"], "paired: Δ=0.08 → MDE 충족")
        R2 = {"a": dict(fper=np.full(73, 0.55)), "b": dict(fper=np.full(73, 0.52))}
        ok(not paired(R2, "a", "b", B=500, k_bonf=3, show=False)["meets_mde"],
           "paired: Δ=0.03 → MDE 미달")

        # 적응 임계 — 유병률이 다른 환자들에서 전역 임계보다 나은가 (홀드아웃)
        def _bt(sx, yx, n=200):
            ts = np.unique(np.quantile(sx, np.linspace(.5, .9995, n))); best = (-1, ts[0])
            for t in ts:
                v = sx >= t; tp = (v & (yx == 1)).sum(); fp = (v & (yx != 1)).sum()
                fn = ((~v) & (yx == 1)).sum()
                pr = tp / (tp + fp + 1e-9); re = tp / (tp + fn + 1e-9)
                f = 2 * pr * re / (pr + re + 1e-9)
                if f > best[0]: best = (f, t)
            return float(best[1])

        def _mk(pvs, sd):
            r = np.random.RandomState(sd); A = []; B2 = []; C = []
            for i, pv in enumerate(pvs):
                n = 900; yy = (r.rand(n) < pv).astype(int)
                sc = np.clip(np.where(yy == 1, r.normal(.72, .16, n), r.normal(.28, .16, n)),
                             1e-4, 1 - 1e-4)
                A.append(sc); B2.append(yy); C.append(np.full(n, i))
            return np.concatenate(A), np.concatenate(B2), np.concatenate(C)

        def _mac(dec, yy, pp):
            f = []
            for i in np.unique(pp):
                m2 = pp == i; v = dec[m2]; q = yy[m2]
                tp = (v & (q == 1)).sum(); fp = (v & (q != 1)).sum(); fn = ((~v) & (q == 1)).sum()
                pr = tp / (tp + fp + 1e-9); re = tp / (tp + fn + 1e-9)
                f.append(2 * pr * re / (pr + re + 1e-9))
            return float(np.mean(f))

        pvs = [0.003, 0.006, 0.01, 0.02, 0.03, 0.05, 0.08, 0.12, 0.20, 0.30, 0.45, 0.57]
        Sc, Yc, Pc = _mk(pvs, 0); St, Yt, Pt = _mk(pvs, 7)     # calib / 홀드아웃 환자 분리
        tg = _bt(Sc, Yc)
        ok(abs(_prev_proxy(St[Pt == 0], tg) - _prev_proxy(St[Pt == 11], tg)) > 0.2,
           "prev_proxy 가 저유병/고유병 환자를 구분함")
        ab = _fit_adaptive(Sc, Yc, Pc, _bt, tg)
        ok(ab is not None, f"적응 사상 학습됨 (a,b)={tuple(round(v,3) for v in ab)}")
        m_g = _mac(St >= tg, Yt, Pt)
        m_a = _mac(_apply_adaptive(St, Pt, ab, tg), Yt, Pt)
        ok(m_a > m_g + 0.01, f"홀드아웃 환자에서 적응 임계 {m_a:.3f} > 전역 {m_g:.3f}")
        ok(np.array_equal(_apply_adaptive(St, Pt, None, tg), St >= tg),
           "사상 학습 실패 시 전역 임계로 폴백")
        ok(_fit_adaptive(Sc[:200], Yc[:200], Pc[:200], _bt, tg) is None,
           "calib 환자가 부족하면 None(무리하게 적합하지 않음)")

        # 문헌 비교표 / burden 분석 (합성 OUT 으로 계약 검증)
        nP = 400
        rr = np.random.RandomState(3)
        yy = np.concatenate([np.where(rr.rand(nP) < pv, 1, 0) for pv in (0.005, 0.03, 0.12)])
        pp = np.repeat([0, 1, 2], nP)
        vv = (yy == 1)
        flip = rr.rand(len(vv)) < 0.05                                  # 약간의 오류 주입
        vv[flip] = ~vv[flip]
        FAKE = dict(res={"R9.테스트": dict(pred=vv, fper=np.full(3, .8), macro=.8,
                                          ci=(.7, .9), micro=.8, prec=.8, sen=.8)},
                    y=yy, pid=pp)
        lt = literature_table(FAKE, "R9.테스트", show=False)
        ok("S(SVEB)" in lt and 0 <= lt["S(SVEB)"]["Se"] <= 1, "문헌 비교표: Se/+P/F1 산출")
        ok("V(VEB)" not in lt, "V 는 별도 임계가 없어 산출에서 제외(오도 방지)")
        ba = burden_analysis(FAKE, "R9.테스트", show=False)
        ok(len(ba["true"]) == 3 and len(ba["pred"]) == 3, "burden: 환자별 실제/예측 산출")
        ok(abs(ba["true"][2] - 12.0) < 4.0, f"burden 실제값 타당 ({ba['true'][2]:.1f}% ≈ 12%)")
        ok(ba["loa"][0] <= ba["bias"] <= ba["loa"][1], "Bland-Altman 일치한계가 편향을 포함")
        ok(-1 <= ba["pearson"] <= 1 and 0 <= ba["band_agree"] <= 1, "상관·구간일치율 범위")
        # 완벽 예측이면 편향 0, r=1
        FAKE["res"]["R9.테스트"]["pred"] = (yy == 1)
        b2 = burden_analysis(FAKE, "R9.테스트", show=False)
        ok(abs(b2["bias"]) < 1e-9 and abs(b2["pearson"] - 1) < 1e-9,
           "완벽 예측 → 편향 0, Pearson r=1")
        ok(b2["band_agree"] == 1.0, "완벽 예측 → 임상 구간 일치율 100%")

        # save_out/load_out 왕복 (런타임 복구용)
        import tempfile
        td = tempfile.mkdtemp()
        fake = dict(res={"R1.RSN(리듬+형태)": dict(macro=0.622, ci=(0.56, 0.68),
                    micro=0.565, prec=0.565, sen=0.566, fper=np.full(73, 0.622))},
                    y=np.array([1, 0]), pid=np.array([0, 0]))
        save_out(fake, name="t", base=td)
        back = load_out(name="t", base=td, verbose=False)
        ok(abs(back["res"]["R1.RSN(리듬+형태)"]["macro"] - 0.622) < 1e-9,
           "save_out/load_out 왕복(런타임 끊겨도 OUT 복원)")
    finally:
        set_data(None)
    print("=== 전 항목 통과 ===")
    return True


if __name__ == "__main__":
    import sys
    if "--selftest" in sys.argv:
        selftest(train="--fast" not in sys.argv)
