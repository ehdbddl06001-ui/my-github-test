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
def _rsn(cseq, L, daux, use_morph=True, w_r=64, w_m=16, w_a=16, p_drop=0.1):
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
            s.rz = nn.Sequential(
                nn.Conv1d(cseq, 64, 5, padding=2), nn.BatchNorm1d(64), nn.GELU(),
                nn.Conv1d(64, 64, 3, padding=2, dilation=2), nn.BatchNorm1d(64), nn.GELU(),
                nn.Conv1d(64, 64, 3, padding=4, dilation=4), nn.BatchNorm1d(64), nn.GELU())
            s.rp = nn.Sequential(nn.Linear(64 * 3, w_r), nn.GELU())
            s.k0 = (L - 1) // 2                      # 슬롯 k=0 (자기 pre-RR)
            s.k1 = min(s.k0 + 1, L - 1)              # 슬롯 k=+1 (자기 post-RR)
            s.mz = None
            if use_morph:
                s.mz = nn.Sequential(
                    nn.Conv1d(2, 16, 7, padding=3), nn.BatchNorm1d(16), nn.ReLU(), nn.MaxPool1d(2),
                    nn.Conv1d(16, 32, 5, padding=2), nn.BatchNorm1d(32), nn.ReLU(), nn.MaxPool1d(2),
                    nn.Conv1d(32, 32, 3, padding=1), nn.BatchNorm1d(32), nn.ReLU(),
                    nn.AdaptiveAvgPool1d(1))
                s.mp = nn.Sequential(nn.Linear(32, w_m), nn.ReLU())
            s.ap = nn.Sequential(nn.Linear(max(daux, 1), w_a), nn.ReLU()) if daux > 0 else None
            d = w_r + (w_m if use_morph else 0) + (w_a if daux > 0 else 0)
            s.cls = nn.Sequential(nn.Linear(d, 64), nn.ReLU(), nn.Dropout(p_drop), nn.Linear(64, 3))

        def forward(s, sq, bt, ax):
            h = s.rz(sq)
            z = s.rp(torch.cat([h.mean(-1), h[:, :, s.k0], h[:, :, s.k1]], -1))
            parts = [z]
            if s.mz is not None:
                parts.append(s.mp(s.mz(bt).squeeze(-1)))
            if s.ap is not None:
                parts.append(s.ap(ax))
            return s.cls(torch.cat(parts, -1))

    return RSN()


# ─────────────────────────────────────────────────────────────────────────────
#  3. 학습·예측 — B2/B3/B4 와 동일 규약(공정 비교)
# ─────────────────────────────────────────────────────────────────────────────
def _fit_predict_rsn(SEQ, AUX, beats, y, tr, cal, te, Sw, mc, seed,
                     use_morph=True, epochs=15, bs=512, n_seed=1):
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
        M = _rsn(SEQ.shape[1], L, AUX.shape[1], use_morph=use_morph).to(dev)
        opt = torch.optim.AdamW(M.parameters(), lr=1e-3, weight_decay=1e-4)
        cw = torch.tensor([1., Sw, 1.5], device=dev)
        mcv = torch.from_numpy(np.asarray(mc, "float32")).to(dev)

        ds = torch.utils.data.TensorDataset(
            torch.from_numpy(SEQ[tr]), torch.from_numpy(beats[tr]),
            torch.from_numpy(Atr), torch.from_numpy(y[tr]))
        dl = torch.utils.data.DataLoader(ds, batch_size=bs, shuffle=True)
        for _ in range(epochs):
            M.train()
            for sq, bt, ax, yy in dl:
                sq, bt, ax, yy = (t.to(dev) for t in (sq, bt, ax, yy))
                opt.zero_grad()
                lo = M(sq, bt, ax)
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
                o.append(torch.softmax(M(sq, bt, ax), -1).cpu().numpy())
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
def make_arm(use_morph=True, poincare=True, K=K_CTX, W=W_NORM, WP=W_POIN,
             causal_only=False, n_seed=1, epochs=15):
    """RSN arm 클로저 생성. 문맥은 첫 호출에서 한 번만 계산해 캐시된다."""
    def arm(ctx):
        c = prepare_context(K=K, W=W, WP=WP, poincare=poincare,
                            causal_only=causal_only, verbose=False)
        pc, pt = _fit_predict_rsn(
            c["seq"], c["aux"], ctx["beats"], ctx["y"],
            ctx["tr"], ctx["cal"], ctx["te"], ctx["Sw"], ctx["mc"], ctx["seed"],
            use_morph=use_morph, epochs=epochs, n_seed=n_seed)
        t = ctx["best_t"](pc[:, 1], ctx["y"][ctx["cal"]])     # 임계는 calib 에서만
        return pt[:, 1] >= t
    return arm


ARM_SPEC = {
    # 표시이름                     : (형태가지, Poincaré, 성격)
    "R0.RSN(리듬만)":              dict(use_morph=False, poincare=False),
    "R1.RSN(리듬+형태)":           dict(use_morph=True,  poincare=False),
    "R2.RSN(+Poincaré)":           dict(use_morph=True,  poincare=True),
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
    arms = [a for a in R if a.split(".")[0] in ("R0", "R1", "R2")]
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
    print(f"\n    [전체 경향] 낮은 F1 과 함께 가는 것:")
    for k, nm in [("prev", "S유병률"), ("contam", "RR오염률"), ("hrv", "RR변동성")]:
        x = np.array([r[k] for r in rows], float)
        if np.isfinite(x).sum() < 5 or np.nanstd(x) == 0:
            continue
        g = np.isfinite(x)
        c = float(np.corrcoef(F[g], x[g])[0, 1])
        arrow = "낮을수록 F1 낮음" if c > 0.15 else ("높을수록 F1 낮음" if c < -0.15 else "관련 약함")
        print(f"      {nm:<10} 상관 {c:+.3f}   {arrow}")
    nfn = sum(1 for r in rows[:topn] if mode(r).startswith("FN"))
    nfp = sum(1 for r in rows[:topn] if mode(r).startswith("FP"))
    print(f"\n    최악 {min(topn,len(rows))}명의 실패양상: FN우세 {nfn} / FP우세 {nfp} / "
          f"양쪽 {min(topn,len(rows))-nfn-nfp}")
    print(f"      → FN 우세면 '판별축 부족', FP 우세면 '개인 정규화 부족'이 1순위 가설.")
    return dict(rows=rows)


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
    t = np.linspace(-1, 1, 300)
    qrs = np.exp(-(t / 0.05) ** 2)
    qrs_w = np.exp(-(t / 0.14) ** 2)
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
            w = qrs_w if labs[i] == 2 else qrs
            seg = np.stack([w, 0.7 * w]) + rng.randn(2, 300) * 0.05
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
            n = attach_arms(verbose=False)
            ok(n == 3 and len(reg) == 3, f"arm {n}개 등록")
            if train:
                ctx = dict(beats=beat, y=y, pid=pid, tr=np.flatnonzero(pid < 4),
                           cal=np.flatnonzero(pid == 4), te=np.flatnonzero(pid == 5),
                           Sw=8.0, mc=np.array([.3, .5, .4], "float32"), seed=0,
                           best_t=lambda s, yy: float(np.quantile(s, 0.9)))
                v = reg["R1.RSN(리듬+형태)"](ctx)
                ok(v.dtype == bool and len(v) == len(ctx["te"]), "arm 반환 계약(bool[len(te)])")
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
