# =============================================================================
#  afib_bench.py  —  2층(리듬·질환축) 하니스: AFIB / AFL / N
#
#  ── 왜 '층'으로 나누는가 (구조적 이유, 취향이 아니다) ────────────────────────
#  1층(비트 N/S/V/F/Q)과 2층(리듬 AFIB/AFL/…)은 **직교**한다. AFIB 구간의 박은
#  대부분 AAMI 클래스 N 이다. 그래서 하나의 다중클래스 softmax 로 합칠 수 없다.
#  더 결정적인 것은 **가용 데이터가 다르다**는 점이다:
#     1층 : 감사된 비트 라벨 필요 → mitdb·svdb·incartdb (환자 201)
#     2층 : R위치 + 리듬 라벨만 필요 → + afdb·ltafdb·nsrdb (환자 130+)
#  두 층의 DB 집합이 다르므로 층을 나누는 것이 데이터를 버리지 않는 유일한 방법이다.
#
#  ── 왜 비트가 아니라 '창(window)' 인가 ──────────────────────────────────────
#  AF 는 에피소드 현상이다. 문헌 표준 단위도 30초~128박 창이다. 그리고 현실적으로:
#     ltafdb(84레코드×24시간) ≈ 970만 박. 비트마다 ±64박 문맥을 실체화하면
#     970만 × 4 × 129 × 4B = **20 GB** → Colab 에서 불가능.
#     창(W=128, 비중첩)으로 만들면 7.6만 창 × 4 × 128 × 4B = **156 MB**.
#  같은 정보를 128배 중복 저장하지 않는 것뿐이고, 인코더는 1층과 **동일한 RSN**이다.
#  → "1층에서 이긴 RR 시퀀스 인코더가 2층으로 그대로 전이되는가" 가 검증 가능해진다.
#
#  ── 반드시 알고 들어갈 것: 이 과제는 이미 포화에 가깝다 ─────────────────────
#  RR 기반 AF 검출은 문헌에서 Se/Sp 95%+ 다. 그러므로 "AF 를 검출했다"는 결과는
#  기여가 아니다. 실제로 열려 있는 곳은 셋이고, 사전등록도 그쪽에 건다:
#     (a) AFL(심방조동) — RR 이 규칙적이라 RR-only 는 **구조적으로** 실패한다.
#         여기가 형태축(P/F파)이 필요한 지점이다.
#     (b) 짧은 발작 에피소드 — burden 정확도가 여기서 갈린다.
#     (c) 교차DB 일반화(afdb 학습 → ltafdb 검증).
#
#  ── 지표: 비트단위 F1 을 주 지표로 쓰지 않는다 ─────────────────────────────
#     창단위 환자매크로 F1  (1층과 같은 추정량 — 층 간 비교 가능)
#     에피소드 Se/PPV       (중첩 기준. AAMI EC57 / IEC 60601-2-47 계열)
#     AF burden r + Bland-Altman  (임상에서 실제로 쓰는 숫자)
#
#  실행:
#     rr_audit_dbs()                      # ① 리듬별 환자 수·MDE (신호 안 받음, 수 분)
#     build_rr_corpus()                   # ② afib_rr.npz 생성 (수십 MB)
#     d = load_rr(); w = make_windows(d)   # ③ 창 구성
#     OUT = bench_afib(w); report_afib(OUT)
#
#  자기검증: python afib_bench.py --selftest   (합성 RR 로 wfdb/torch 없이 검증)
# =============================================================================
import numpy as np

_BASE = globals().get("_BASE", "/content/drive/MyDrive/mitbih")
FS_RR = 360.0                 # 저장 규약: pre_rr/post_rr 는 360Hz 샘플
RR_LO, RR_HI = 0.20, 3.00     # 생리적 범위(초) — 1층과 동일
EWMA_A = 0.3
W_WIN = 128                   # 창 길이(박). 128박 ≈ 90~150초 — 문헌 표준대
PURITY = 0.90                 # 창의 90% 이상이 한 리듬일 때만 그 리듬으로 라벨

# 2층에서 다루는 리듬. 그 밖(SVTA/B/T/VT…)은 1층 하니스(bench_rhythm)에서 다룬다.
AF_CLASSES = ("N", "AFIB", "AFL")

ARMS = {}


def register_afib_arm(name, fn):
    """★이름에 afib 를 붙인 이유: CORE 파일들은 같은 globals 로 exec 되므로
       svdb_bench.register_arm 과 이름이 겹치면 나중에 로드되는 쪽이 덮어쓴다.
       그러면 attach_arms() 가 1층 arm 을 2층 레지스트리에 넣는 조용한 사고가 난다.
       rhythm_bench 가 register_rhythm_arm 을 쓰는 것과 같은 이유다."""
    ARMS[name] = fn
    return name


def clear_afib_arms():
    ARMS.clear()


# ─────────────────────────────────────────────────────────────────────────────
#  1. 코퍼스 로드
# ─────────────────────────────────────────────────────────────────────────────
def load_rr(path=None, verbose=True):
    """build_rr_corpus 가 만든 afib_rr.npz 를 읽는다."""
    d = np.load(path or f"{_BASE}/afib_rr.npz", allow_pickle=True)
    out = {k: d[k] for k in d.files}
    out["rhythm_names"] = [str(x) for x in d["rhythm_names"]]
    if verbose:
        R, P = out["rhythm"], out["pid"]
        print(f"[2층] 비트 {len(P):,}  환자 {len(np.unique(P))}  "
              f"리듬 {len(out['rhythm_names'])}종")
    return out


# ─────────────────────────────────────────────────────────────────────────────
#  2. 창 구성 — 1층 RSN 과 같은 무차원 4채널
# ─────────────────────────────────────────────────────────────────────────────
def _rec_channels(rr):
    """한 레코드의 RR 열(초) → (4, n) 채널 + 레코드 통계.

    채널 정의는 1층 rr_context 와 **동일**하다(무차원 → DB·심박수 불변):
      ch0 clip(log(RR/med), ±1.5)     ch1 clip(dRR/med, ±1.5)
      ch2 tanh(innov/3MAD)            ch3 유효 마스크
    ★정규화 통계(med/MAD)는 창이 아니라 **레코드** 기준이다. 창 기준으로 잡으면
      "이 구간의 심박이 기저보다 빠르다"는 정보가 창마다 지워진다.
    """
    n = len(rr)
    valid = (rr >= RR_LO) & (rr <= RR_HI)
    ref = rr[valid] if valid.any() else rr
    med = float(np.median(ref)) if len(ref) else 0.8
    med = med if med > 1e-3 else 0.8
    mad = float(np.median(np.abs(ref - med))) if len(ref) else 0.05
    mad = mad if mad > 1e-4 else 0.05

    ch0 = np.clip(np.log(np.maximum(rr, 1e-3) / med), -1.5, 1.5)
    d = np.zeros(n); d[1:] = np.diff(rr)
    ch1 = np.clip(d / med, -1.5, 1.5)
    # 인과적 EWMA 잔차 — 미래를 안 본다(스트리밍 구현 가능)
    ew = np.empty(n); e = med
    innov = np.empty(n)
    for i in range(n):
        innov[i] = rr[i] - e
        e = (1 - EWMA_A) * e + EWMA_A * (rr[i] if valid[i] else e)
        ew[i] = e
    ch2 = np.tanh(innov / (3 * mad))
    ch3 = valid.astype("float64")
    C = np.stack([ch0 * ch3, ch1 * ch3, ch2 * ch3, ch3]).astype("float32")
    return C, med, mad, valid


def _win_aux(rr, valid, med_rec):
    """창당 스칼라 10종 = A1(고전 RR산포 기준선)의 특징벡터이자 RSN 의 보조입력.

    전부 무차원(med 로 나누거나 비율)이라 DB·심박수에 불변이다.
    """
    v = rr[valid]
    if len(v) < 4:
        return np.zeros(10, "float32")
    med_w = float(np.median(v)) or med_rec
    dv = np.diff(v)
    rmssd = float(np.sqrt(np.mean(dv ** 2)))
    pnn50 = float(np.mean(np.abs(dv) > 0.05))
    cv = float(np.std(v) / (np.mean(v) + 1e-9))
    # ΔRR 샤논 엔트로피 — AF 검출 고전 특징(Dash 2009 계열). 16구간 히스토그램.
    h, _ = np.histogram(np.clip(dv / med_w, -0.5, 0.5), bins=16, range=(-0.5, 0.5))
    p = h / max(h.sum(), 1)
    ent = float(-(p[p > 0] * np.log(p[p > 0])).sum() / np.log(16))
    sd1 = float(np.std(dv) / np.sqrt(2))
    sd2 = float(np.sqrt(max(2 * np.var(v) - sd1 ** 2, 1e-12)))
    q1, q3 = np.percentile(v, [25, 75])
    return np.array([med_w / med_rec, rmssd / med_w, pnn50, cv, ent,
                     sd1 / med_w, sd2 / med_w, sd1 / (sd2 + 1e-9),
                     (q3 - q1) / med_w, float(valid.mean())], "float32")


def win_starts(n, W, stride):
    """레코드 길이 n 에서 창 시작 인덱스들.

    ★make_windows 와 build_atrial_feats 가 **반드시 이 함수를 함께** 써야 두 결과의
      창이 1:1 로 대응한다. 각자 range() 를 따로 적으면 어긋나도 아무 에러가 안 나고
      **다른 창의 특징이 붙는다** — 찾기 가장 어려운 종류의 버그다.
    """
    return list(range(0, n - W + 1, stride)) if n >= W else []


def make_windows(d, W=W_WIN, stride=None, purity=PURITY, classes=AF_CLASSES,
                 dbs=None, verbose=True):
    """비트 코퍼스 → 창 데이터셋.

    ★dbs 로 DB 를 골라낼 수 있다. 심방활동 특징(2층-B)은 신호를 받은 DB 에만
      있으므로, 그 축을 쓰는 실험에서는 dbs=("afdb","mitdb") 처럼 좁혀야 한다.
      좁히지 않으면 대부분의 창이 특징 없이(NaN→중앙값 대체) 들어와 형태축의
      효과가 희석된다 — 있지도 않은 정보를 '효과 없음'으로 오판하게 된다.

    반환 dict: seq[Nw,4,W] aux[Nw,10] y[Nw] pid db dur(초) nov(비중첩 플래그)
               t0(창 시작 시각) pur(순도) classes
    ★'전이구간'(순도 < purity)은 y=-1 로 남기고 학습·평가에서 뺀다. 리듬이 바뀌는
      경계를 어느 한쪽 라벨로 우겨넣으면 그 오답이 모델 탓으로 계상된다.
    """
    stride = int(stride or W)
    names = d["rhythm_names"]
    want = {nm: i for i, nm in enumerate(classes)}
    pid, rhy = d["pid"], d["rhythm"]
    pre, dbv = d["pre_rr"], d["db"]
    if dbs is not None:
        keep_db = np.isin(np.array(list(map(str, dbv))), list(dbs))
        if not keep_db.any():
            raise RuntimeError(f"dbs={dbs} 에 해당하는 비트가 없습니다 — "
                               f"코퍼스의 DB: {sorted(set(map(str, dbv)))}")
        pid, rhy, pre, dbv = pid[keep_db], rhy[keep_db], pre[keep_db], dbv[keep_db]
        if verbose:
            print(f"  [DB 필터] {list(dbs)} → 비트 {int(keep_db.sum()):,} / "
                  f"{len(keep_db):,}  환자 {len(np.unique(pid))}")
    SEQ = []; AUX = []; Y = []; PID = []; DB = []; DUR = []; NOV = []; T0 = []; PUR = []
    KEY = []                                   # (pid, 창 시작 비트인덱스) — 심방특징 결합키
    n_trans = 0
    for p in np.unique(pid):
        idx = np.flatnonzero(pid == p)              # 레코드 내 시간순(저장 순서)
        if len(idx) < W:
            continue
        rr = np.asarray(pre[idx], np.float64) / FS_RR
        C, med, mad, valid = _rec_channels(rr)
        lab = np.array([want.get(names[r], -1) for r in rhy[idx]])
        tt = np.concatenate([[0.0], np.cumsum(rr[1:])])
        db0 = str(dbv[idx[0]])
        for s in win_starts(len(idx), W, stride):
            sl = slice(s, s + W)
            l = lab[sl]
            u, c = np.unique(l, return_counts=True)
            j = int(np.argmax(c)); pu = c[j] / W
            y = int(u[j]) if (pu >= purity and u[j] >= 0) else -1
            if y < 0:
                n_trans += 1
            SEQ.append(C[:, sl]); AUX.append(_win_aux(rr[sl], valid[sl], med))
            Y.append(y); PID.append(int(p)); DB.append(db0)
            DUR.append(float(rr[sl].sum())); T0.append(float(tt[s]))
            NOV.append(s % W == 0); PUR.append(float(pu)); KEY.append((int(p), int(s)))
    if not SEQ:
        raise RuntimeError(f"창이 하나도 안 만들어졌습니다 — W={W} 가 레코드 길이보다 큰지 확인.")
    w = dict(seq=np.stack(SEQ), aux=np.stack(AUX), y=np.array(Y, np.int64),
             pid=np.array(PID, np.int64), db=np.array(DB),
             dur=np.array(DUR, "float32"), nov=np.array(NOV, bool),
             t0=np.array(T0, "float32"), pur=np.array(PUR, "float32"),
             key=np.array(KEY, np.int64), W=int(W), stride=int(stride),
             classes=list(classes))
    if verbose:
        keep = w["y"] >= 0
        gb = w["seq"].nbytes / 1e6
        print(f"\n[창] W={W} stride={stride}  총 {len(w['y']):,}창 ({gb:.0f} MB)  "
              f"비중첩 {int(w['nov'].sum()):,}")
        print(f"  {'리듬':<8}{'창':>10}{'환자':>6}{'비율':>8}")
        for i, nm in enumerate(classes):
            m = w["y"] == i
            print(f"  {nm:<8}{int(m.sum()):>10,}{len(np.unique(w['pid'][m])):>6}"
                  f"{100*m.mean():>7.2f}%")
        print(f"  전이구간(순도<{purity}) {n_trans:,} → 학습·평가 제외")
        _mde(w, verbose=True)
    return w


def _mde(w, sigma=0.32, verbose=True):
    """클래스별 검정력. ★모델을 붙이기 전에 이 표를 먼저 볼 것."""
    out = {}
    for i, nm in enumerate(w["classes"]):
        n = len(np.unique(w["pid"][w["y"] == i]))
        out[nm] = (float(1.96 * sigma / max(np.sqrt(n), 1)), n)
    if verbose:
        print(f"\n  [검정력] 환자별 F1 의 σ≈{sigma} 가정")
        print(f"  {'리듬':<8}{'환자':>6}{'MDE':>8}   판정 가능 여부")
        for nm, (h, n) in out.items():
            v = "충분" if h <= 0.07 else ("한계" if h <= 0.12 else "★불가 — 데이터부터")
            print(f"  {nm:<8}{n:>6}{h:>8.3f}   {v}")
    return out


# ─────────────────────────────────────────────────────────────────────────────
#  3. 지표 — 창 / 에피소드 / burden
# ─────────────────────────────────────────────────────────────────────────────
def _f1_af(v, yp):
    tp = float((v & yp).sum()); fp = float((v & ~yp).sum()); fn = float((~v & yp).sum())
    return 0.0 if tp == 0 else 2 * tp / (2 * tp + fp + fn)


def win_macro(pred, y, pid, classes, detail=False):
    """창단위 **환자매크로 F1** — 1층과 같은 추정량이라 층 간 비교가 성립한다.

    detail=True 면 (평균, 환자수, 환자별 F1 벡터, 환자 id 벡터)를 준다.
    ★벡터가 필요한 이유: 두 팔을 비교하려면 **같은 환자에서 짝지은 차이**를 봐야
      한다. 평균만 있으면 짝을 못 짓고, 그러면 검정력을 크게 낭비한다.
    """
    out = {}
    ps = np.unique(pid)
    for c, nm in enumerate(classes):
        v = []; ids = []
        for p in ps:
            m = pid == p
            if not (y[m] == c).any():
                continue                       # 그 리듬이 없는 환자는 제외(1층 규약)
            v.append(_f1_af(pred[m] == c, y[m] == c)); ids.append(p)
        mu = float(np.mean(v)) if v else float("nan")
        out[nm] = ((mu, len(v), np.array(v), np.array(ids)) if detail
                   else (mu, len(v)))
    return out


def _arm_vecs(OUT, arm, cls):
    """한 팔의 (환자 id, 환자별 F1) — 팔 사이 짝짓기용."""
    W = OUT["w"]; r = OUT["res"][arm]; m = r["mask"]
    d = win_macro(r["pred"][m], W["y"][m], W["pid"][m], OUT["classes"], detail=True)
    _, _, v, ids = d[cls]
    return ids, v


def _burden_vec(pred, y, pid, dur, cls_idx):
    """환자별 (id, 실제 burden%, 예측 burden%). 환자 순서를 고정해 팔 사이 짝을 맞춘다."""
    ps = np.unique(pid)
    tb = np.zeros(len(ps)); pb = np.zeros(len(ps))
    for i, p in enumerate(ps):
        m = pid == p
        tot = float(dur[m].sum())
        if tot <= 0:
            continue
        tb[i] = 100.0 * float(dur[m][y[m] == cls_idx].sum()) / tot
        pb[i] = 100.0 * float(dur[m][pred[m] == cls_idx].sum()) / tot
    return ps, tb, pb


def burden_metrics(pred, y, pid, dur, cls_idx, verbose=True, name="AFIB"):
    """AF burden(= AF 시간 / 전체 시간) 추정 정확도 — Pearson r + Bland-Altman.

    ★임상에서 실제로 쓰는 숫자는 "이 박이 AF 냐"가 아니라 "이 환자가 하루의 몇 %를
      AF 로 보내느냐"다. 항응고 결정·재발 감시가 전부 burden 기준이다.
      그래서 F1 이 같아도 burden 오차가 다르면 임상 가치가 다르다.
    ★시간 가중이다(창마다 길이가 다르므로 창 개수로 세면 편향된다).
    """
    ids, tb, pb = _burden_vec(pred, y, pid, dur, cls_idx)
    n = len(tb)
    nan = float("nan")
    out = dict(n=n, true=tb, pred=pb, r=nan, r_ci=(nan, nan), bias=nan, sd=nan,
               loa=(nan, nan))
    if n < 3:
        return out          # ★환자가 3명 미만이면 상관·LoA 를 계산하지 않는다
    r = float(np.corrcoef(tb, pb)[0, 1]) if tb.std() > 0 and pb.std() > 0 else nan
    dif = pb - tb
    bias = float(dif.mean()); sd = float(dif.std(ddof=1))
    loa = (bias - 1.96 * sd, bias + 1.96 * sd)
    # Fisher z 로 r 의 95% CI (n 이 작을 때 r 을 점추정만 보고하면 과신한다)
    if np.isfinite(r) and abs(r) < 0.999 and n > 3:
        z = np.arctanh(r); se = 1 / np.sqrt(n - 3)
        ci = (float(np.tanh(z - 1.96 * se)), float(np.tanh(z + 1.96 * se)))
    else:
        ci = (nan, nan)
    out.update(r=r, r_ci=ci, bias=bias, sd=sd, loa=loa)
    if verbose:
        print(f"    {name} burden  n={n}  r={r:.3f} [{ci[0]:.3f},{ci[1]:.3f}]  "
              f"편향 {bias:+.2f}%p  LoA [{loa[0]:+.2f},{loa[1]:+.2f}]%p")
    return out


def _runs(v):
    """불리언 열 → [(시작, 끝)] 연속 구간 목록."""
    out = []; i = 0; n = len(v)
    while i < n:
        if v[i]:
            j = i
            while j + 1 < n and v[j + 1]:
                j += 1
            out.append((i, j)); i = j + 1
        else:
            i += 1
    return out


def episode_metrics(pred, y, pid, t0, nov, cls_idx, short_win=3, verbose=True,
                    name="AFIB"):
    """에피소드 단위 Se/PPV (중첩 기준) — 짧은 발작을 따로 본다.

    ★중첩 기준: 참 에피소드는 예측 에피소드와 1창이라도 겹치면 검출로 친다.
      창단위 F1 은 긴 에피소드 하나가 지배하지만, 임상적으로는 "발작을 놓쳤는가"가
      질문이므로 에피소드를 1건씩 세는 지표가 따로 필요하다.
    ★비중첩 창만 쓴다(중첩 창을 쓰면 같은 에피소드를 여러 번 센다).
    """
    hit = tot = phit = ptot = 0
    shit = stot = 0
    for p in np.unique(pid):
        m = (pid == p) & nov
        if m.sum() < 2:
            continue
        o = np.argsort(t0[m])
        yt = (y[m][o] == cls_idx); yp = (pred[m][o] == cls_idx)
        for a, b in _runs(yt):
            tot += 1
            d = yp[a:b + 1].any()
            hit += int(d)
            if b - a + 1 <= short_win:
                stot += 1; shit += int(d)
        for a, b in _runs(yp):
            ptot += 1; phit += int(yt[a:b + 1].any())
    se = hit / tot if tot else float("nan")
    ppv = phit / ptot if ptot else float("nan")
    sse = shit / stot if stot else float("nan")
    if verbose:
        print(f"    {name} 에피소드  Se {se:.3f} ({hit}/{tot})  "
              f"PPV {ppv:.3f} ({phit}/{ptot})  짧은발작(≤{short_win}창) Se {sse:.3f} ({shit}/{stot})")
    return dict(se=se, ppv=ppv, n_true=tot, n_pred=ptot, se_short=sse, n_short=stot)


# ─────────────────────────────────────────────────────────────────────────────
#  3.5 짝지은 검정 — 사전등록 H-J / H-K 의 실제 판정
#
#  ★왜 '짝'을 지어야 하는가 (이 절 전체의 근거)
#    두 팔의 신뢰구간이 안 겹치면 다르다 — 이 논리는 **독립 표본**일 때만 맞다.
#    여기서는 같은 68명을 두 모델이 각각 잰 것이라 환자 한 명이 두 값에 동시에
#    영향을 준다(어려운 환자는 양쪽 다 틀린다). 그 상관을 무시하면 차이의 분산을
#    과대평가해 **실제로 있는 차이를 놓친다**.
#    그래서 재표집 단위를 '창'이 아니라 **환자**로 두고, 같은 환자 집합에서 두 팔의
#    값을 함께 뽑는다. 1층 paired() 와 같은 구조다.
# ─────────────────────────────────────────────────────────────────────────────
def sigma_measured(OUT, verbose=True):
    """환자별 F1 의 **실측** 표준편차 → 가정 σ=0.32 를 대체하고 MDE 를 다시 계산.

    ★사전등록(LAYER2_AFIB.md §1)에 "첫 실행 뒤 실측 σ 로 갱신한다"고 적어 둔 절차다.
      σ 를 가정값으로 놔두면 MDE 가 가정이고, 그 위에서 내린 판정도 가정이 된다.
      팔마다 σ 가 다르므로 **가장 큰 σ**(보수적)를 쓴다.
    """
    cls = OUT["classes"]; out = {}; dead = set()
    arms = [a for a in OUT["res"] if not a.startswith("A0")]
    for c in cls:
        sg, n, mx = 0.0, 0, 0.0
        for a in arms:
            ids, v = _arm_vecs(OUT, a, c)
            if len(v) > 1:
                sg = max(sg, float(v.std(ddof=1))); n = len(v)
                mx = max(mx, float(np.nanmax(v)) if len(v) else 0.0)
        # ★σ=0 을 '검정력 무한'으로 읽으면 안 된다. 전 팔이 그 리듬을 통째로 못
        #   맞히면 환자별 F1 이 전부 0 이라 표준편차도 0 이 되고, MDE 0.000 이
        #   찍힌다. 실제로 LODO 에서 AFL 이 그랬다. 이건 완벽한 검정력이 아니라
        #   **측정 자체가 안 된 것**이다.
        if sg == 0.0 and mx == 0.0 and n:
            dead.add(c)
        out[c] = (sg, n, float(1.96 * sg / max(np.sqrt(n), 1)) if n else float("nan"))
    if verbose:
        print(f"\n  [검정력 갱신] 환자별 F1 의 **실측** σ (팔 중 최댓값 = 보수적)")
        print(f"  {'리듬':<8}{'환자':>6}{'σ(가정)':>10}{'σ(실측)':>10}{'MDE(실측)':>11}")
        for c, (sg, n, m) in out.items():
            flag = "  ✗측정 불가" if c in dead else ""
            print(f"  {c:<8}{n:>6}{0.32:>10.3f}{sg:>10.3f}{m:>11.3f}{flag}")
        print(f"  ※ 실측 σ 가 가정보다 작으면 검정력이 생각보다 좋다는 뜻이다(반대면 나쁘다).")
        for c in sorted(dead):
            print(f"  ✗ {c}: 모든 팔의 환자별 F1 이 **전부 0** → σ=0 은 검정력이 완벽하다는"
                  f" 뜻이 아니라\n     그 리듬이 한 번도 검출되지 않았다는 뜻이다."
                  f" MDE 0.000 을 신뢰하지 말 것.")
    return out


def paired_win(OUT, new, base, cls="AFIB", B=5000, seed=0, verbose=True):
    """H-J: 창 F1 을 **같은 환자에서 짝지어** 비교."""
    ia, va = _arm_vecs(OUT, base, cls)
    ib, vb = _arm_vecs(OUT, new, cls)
    if len(ia) != len(ib) or not np.array_equal(ia, ib):
        raise RuntimeError("두 팔의 환자 집합이 다릅니다 — 짝을 지을 수 없습니다.")
    d = vb - va
    n = len(d)
    rng = np.random.RandomState(seed)
    bs = np.array([d[rng.randint(0, n, n)].mean() for _ in range(B)])
    lo, hi = np.percentile(bs, [2.5, 97.5])
    out = dict(delta=float(d.mean()), ci=(float(lo), float(hi)), n=n,
               p_one=float((bs <= 0).mean()))
    # ★두 팔 모두 그 리듬을 **한 번도 못 맞힌** 경우 — Δ=0 은 "차이 없음"이 아니라
    #   "정보 없음"이다. LODO 에서 AFL 이 전 팔 0.000 이 나왔는데 '미달(0 포함)'로
    #   찍혀서, 검정이 성립한 것처럼 보였다. 이런 건 판정에서 빼야 한다.
    dead = bool(np.all(va == 0) and np.all(vb == 0))
    out["dead"] = dead
    if verbose:
        if dead:
            print(f"    [{cls}] {new} − {base}  ✗판정 불가 — 두 팔 모두 F1=0"
                  f"(그 리듬을 아무도 검출 못 함). n={n}")
        else:
            v = "★유의(0 배제)" if lo > 0 else ("역행" if hi < 0 else "미달(0 포함)")
            print(f"    [{cls}] {new} − {base}  Δ={out['delta']:+.4f} "
                  f"[{lo:+.4f},{hi:+.4f}]  n={n}  {v}")
    return out


def paired_burden(OUT, new, base, cls="AFIB", B=5000, seed=0, verbose=True):
    """H-K: burden 추정 오차를 **같은 환자에서 짝지어** 비교.

    세 통계를 함께 본다 — 하나만 보면 오도되기 쉽다:
      ratio_LoA  = SD(new 오차) / SD(base 오차)   <1 이면 new 가 좁다
                   (Bland-Altman 폭은 3.92×SD 이므로 SD 비 = 폭 비)
      d_medAE    = |오차| 중앙값의 차               SD 는 이상치 몇 명에 좌우되므로
                   중앙값도 같이 본다(둘의 방향이 다르면 '소수 환자 이야기'다)
      d_r        = Pearson r 의 차
    """
    W = OUT["w"]; ci = OUT["classes"].index(cls)
    ra, rb = OUT["res"][base], OUT["res"][new]
    ma, mb = ra["mask"], rb["mask"]
    pa, ta, qa = _burden_vec(ra["pred"][ma], W["y"][ma], W["pid"][ma], W["dur"][ma], ci)
    pb_, tb, qb = _burden_vec(rb["pred"][mb], W["y"][mb], W["pid"][mb], W["dur"][mb], ci)
    if not np.array_equal(pa, pb_):
        raise RuntimeError("두 팔의 환자 집합이 다릅니다 — 짝을 지을 수 없습니다.")
    if not np.allclose(ta, tb):
        raise RuntimeError("실제 burden 이 팔마다 다릅니다 — 마스크가 어긋났습니다.")
    ea, eb = qa - ta, qb - tb                     # 팔별 오차(%p)
    n = len(ta)

    def stat(k):
        sa, sb = ea[k].std(ddof=1), eb[k].std(ddof=1)
        ra_ = np.corrcoef(ta[k], qa[k])[0, 1] if ta[k].std() > 0 and qa[k].std() > 0 else np.nan
        rb_ = np.corrcoef(tb[k], qb[k])[0, 1] if tb[k].std() > 0 and qb[k].std() > 0 else np.nan
        return (sb / sa if sa > 0 else np.nan,
                float(np.median(np.abs(eb[k])) - np.median(np.abs(ea[k]))),
                float(rb_ - ra_))

    obs = stat(np.arange(n))
    rng = np.random.RandomState(seed)
    bs = np.array([stat(rng.randint(0, n, n)) for _ in range(B)])
    ci95 = np.nanpercentile(bs, [2.5, 97.5], axis=0)
    out = dict(n=n,
               ratio_loa=obs[0], ratio_ci=(float(ci95[0, 0]), float(ci95[1, 0])),
               d_medae=obs[1],   medae_ci=(float(ci95[0, 1]), float(ci95[1, 1])),
               d_r=obs[2],       r_ci=(float(ci95[0, 2]), float(ci95[1, 2])),
               loa_base=3.92 * ea.std(ddof=1), loa_new=3.92 * eb.std(ddof=1))
    if verbose:
        v = ("★유의(1 배제)" if out["ratio_ci"][1] < 1 else
             ("역행" if out["ratio_ci"][0] > 1 else "미달(1 포함)"))
        print(f"    [{cls}] {new} vs {base}  n={n}")
        print(f"      LoA 폭  {out['loa_base']:.1f} → {out['loa_new']:.1f} %p"
              f"   비 {out['ratio_loa']:.3f} [{out['ratio_ci'][0]:.3f},"
              f"{out['ratio_ci'][1]:.3f}]  {v}")
        print(f"      |오차| 중앙값 차 {out['d_medae']:+.2f}%p "
              f"[{out['medae_ci'][0]:+.2f},{out['medae_ci'][1]:+.2f}]"
              f"   r 차 {out['d_r']:+.3f} [{out['r_ci'][0]:+.3f},{out['r_ci'][1]:+.3f}]")
    return out


def burden_outliers(OUT, arm, cls="AFIB", k=6, verbose=True):
    """burden 오차가 큰 환자 상위 k명 — LoA 를 넓히는 것이 '전반'인지 '몇 명'인지 가른다."""
    W = OUT["w"]; ci = OUT["classes"].index(cls); r = OUT["res"][arm]; m = r["mask"]
    ids, t, q = _burden_vec(r["pred"][m], W["y"][m], W["pid"][m], W["dur"][m], ci)
    e = q - t
    o = np.argsort(-np.abs(e))[:k]
    if verbose:
        print(f"\n    [{arm}] {cls} burden 오차 상위 {k}명 "
              f"(전체 |오차| 합 대비 이들의 비중 "
              f"{100*np.abs(e[o]).sum()/max(np.abs(e).sum(),1e-9):.0f}%)")
        print(f"      {'환자':>6}{'실제%':>9}{'예측%':>9}{'오차%p':>9}")
        for i in o:
            print(f"      {ids[i]:>6}{t[i]:>9.1f}{q[i]:>9.1f}{e[i]:>+9.1f}")
    return ids[o], t[o], q[o], e[o]


# ─────────────────────────────────────────────────────────────────────────────
#  4. 팔(arm) — A0 자명 / A1 고전 RR산포 / A2 RSN / A3 RSN+도메인
# ─────────────────────────────────────────────────────────────────────────────
def _torch():
    import torch
    return torch, torch.nn


def _aux_cols(w, mode):
    """팔이 쓸 보조특징 열을 고른다.

    ★★이 함수가 없어서 실제로 사고가 났다 — attach_atrial(w) 가 w["aux"] 를
      10 → 31 열로 늘리는데, 모든 팔이 w["aux"] 를 통째로 쓰고 있었다. 그 결과
      'RR 산포 기준선(A1)'·'RSN(A2)' 까지 심방 특징을 받아 **팔의 정의가 조용히
      바뀌었고**, A2 와 A4 는 비트 단위로 같은 예측을 냈다(= 비교가 무의미).
      이제 팔마다 mode 를 선언해야 하고, 선언하지 않으면 열이 안 붙는다.

      "none"   보조특징 없음 (시퀀스만)
      "rr"     RR 산포 10종만        ← A1·A2·A2c·A3 의 정의
      "atrial" 심방·P-QRS-T 특징만   ← A4c
      "all"    둘 다                 ← A4
    """
    n = w["aux"].shape[1]
    nrr = int(w.get("n_rr", n))          # attach_atrial 이 없으면 전부 RR
    if mode == "none":
        return np.zeros(0, int)
    if mode == "rr":
        return np.arange(nrr)
    if mode == "atrial":
        if nrr >= n:
            raise RuntimeError("심방특징이 없습니다 — attach_atrial(w) 를 먼저 하세요.")
        return np.arange(nrr, n)
    if mode == "all":
        return np.arange(n)
    raise ValueError(f"알 수 없는 aux mode: {mode}")


def _fit_win(w, tr, te, ncls, seed, use_seq=True, aux="rr", n_domain=0,
             epochs=20, bs=256, lr=1e-3):
    """창 분류기 학습. 인코더는 1층과 **같은** `_rsn`(형태 가지 끔).

    aux 는 반드시 명시한다(_aux_cols 참조). 기본값을 "rr" 로 둔 것은, 실수로
    빠뜨렸을 때 **팔이 조용히 강해지는 쪽이 아니라 원래 정의대로** 돌게 하기 위함이다.
    """
    torch, nn = _torch()
    g = globals()
    if "_rsn" not in g:
        raise RuntimeError("_rsn 없음 — svdb_rhythm.py 를 먼저 로드하세요 (colab_setup.sync()).")
    torch.manual_seed(seed); np.random.seed(seed)
    dev = "cuda" if torch.cuda.is_available() else "cpu"
    L = w["seq"].shape[2]
    cols = _aux_cols(w, aux)
    daux = len(cols)
    net = g["_rsn"](4, L, daux, use_morph=False, use_seq=use_seq,
                    n_class=ncls, n_domain=n_domain).to(dev)
    dom_ids = None
    if n_domain > 0:
        uds = sorted(set(map(str, w["db"])))
        dm = {d: i for i, d in enumerate(uds)}
        dom_ids = np.array([dm[str(x)] for x in w["db"]], np.int64)

    X = torch.tensor(w["seq"])
    A = torch.tensor(w["aux"][:, cols] if daux else
                     np.zeros((len(w["y"]), 1), "float32"))
    Y = torch.tensor(w["y"])
    # 클래스 불균형 보정 — N 이 압도적이라 보정 없이는 AFL 이 학습되지 않는다
    cnt = np.bincount(w["y"][tr], minlength=ncls).astype("float64")
    cw = torch.tensor((cnt.sum() / np.maximum(cnt, 1)) ** 0.5, dtype=torch.float32).to(dev)
    opt = torch.optim.Adam(net.parameters(), lr=lr)
    lossf = nn.CrossEntropyLoss(weight=cw)
    dummy = torch.zeros(bs, 2, 8)                       # 형태 가지 미사용 자리표
    for ep in range(epochs):
        net.train(); perm = np.random.permutation(tr)
        for i in range(0, len(perm), bs):
            b = perm[i:i + bs]
            sq = X[b].to(dev); ax = A[b].to(dev); yy = Y[b].to(dev)
            dm_ = torch.tensor(dom_ids[b]).to(dev) if dom_ids is not None else None
            o = net(sq, dummy[:len(b)].to(dev), ax, None, dm_)
            o = o[0] if isinstance(o, tuple) else o
            loss = lossf(o, yy)
            opt.zero_grad(); loss.backward()
            nn.utils.clip_grad_norm_(net.parameters(), 5.0); opt.step()
    net.eval(); P = []
    with torch.no_grad():
        for i in range(0, len(te), 4096):
            b = te[i:i + 4096]
            dm_ = torch.tensor(dom_ids[b]).to(dev) if dom_ids is not None else None
            o = net(X[b].to(dev), dummy[:1].expand(len(b), -1, -1).to(dev),
                    A[b].to(dev), None, dm_)
            o = o[0] if isinstance(o, tuple) else o
            P.append(torch.softmax(o, -1).cpu().numpy())
    return np.concatenate(P)


def _arm_trivial(w, tr, te, ncls, seed, epochs=20):
    """A0. 항상 다수 클래스 — 자명한 하한. 이 아래면 모델이 해로운 것이다."""
    c = np.bincount(w["y"][tr], minlength=ncls).argmax()
    p = np.zeros((len(te), ncls), "float32"); p[:, c] = 1.0
    return p


def _arm_rrdisp(w, tr, te, ncls, seed, epochs=20):
    """A1. 고전 RR산포 스칼라 10종 → MLP. **문헌 기준선**.

    RMSSD·pNN50·CV·ΔRR 엔트로피·Poincaré 는 1990~2010년대 AF 검출기의 표준 특징이다.
    RSN 이 이것을 못 이기면 시퀀스 인코더는 2층에서 값을 못 한 것이다.
    """
    torch, nn = _torch()
    torch.manual_seed(seed); np.random.seed(seed)
    dev = "cuda" if torch.cuda.is_available() else "cpu"
    A = torch.tensor(w["aux"][:, _aux_cols(w, "rr")])   # ★RR 산포 10종만 — 문헌 기준선
    Y = torch.tensor(w["y"])
    net = nn.Sequential(nn.Linear(A.shape[1], 64), nn.ReLU(), nn.Dropout(0.1),
                        nn.Linear(64, 64), nn.ReLU(), nn.Linear(64, ncls)).to(dev)
    cnt = np.bincount(w["y"][tr], minlength=ncls).astype("float64")
    cw = torch.tensor((cnt.sum() / np.maximum(cnt, 1)) ** 0.5, dtype=torch.float32).to(dev)
    opt = torch.optim.Adam(net.parameters(), lr=1e-3)
    lossf = nn.CrossEntropyLoss(weight=cw)
    for ep in range(epochs):
        net.train(); perm = np.random.permutation(tr)
        for i in range(0, len(perm), 256):
            b = perm[i:i + 256]
            loss = lossf(net(A[b].to(dev)), Y[b].to(dev))
            opt.zero_grad(); loss.backward(); opt.step()
    net.eval()
    with torch.no_grad():
        return torch.softmax(net(A[te].to(dev)), -1).cpu().numpy()


def _arm_rsn(w, tr, te, ncls, seed, epochs=20):
    """A2. RSN 시퀀스 + RR 산포. ★심방특징은 쓰지 않는다(A4 와의 대비를 위해)."""
    return _fit_win(w, tr, te, ncls, seed, use_seq=True, aux="rr", epochs=epochs)


def _arm_rsn_nodisp(w, tr, te, ncls, seed, epochs=20):
    """A2c. RSN 시퀀스만(스칼라 보조 전부 제거) — A2 의 이득이 스칼라 덕인지 가르는 대조군."""
    return _fit_win(w, tr, te, ncls, seed, use_seq=True, aux="none", epochs=epochs)


def attach_atrial(w, path=None, verbose=True):
    """창별 심방활동 특징 8종을 w["aux"] 에 이어 붙인다(10 → 18).

    ★결합은 (pid, 창 시작 비트인덱스) 키로 한다. 순서가 같을 것이라고 **가정하지
      않는다** — 가정하면 어긋나도 에러가 안 나고 다른 창의 특징이 붙는다.
    ★추출 실패 창은 NaN 이다. 신경망에 NaN 을 넣으면 손실이 통째로 NaN 이 되므로
      그 열의 중앙값으로 채우고, '채웠음' 표시 열을 하나 더 붙인다(정보를 숨기지
      않으면서 학습은 가능하게).
    """
    a = np.load(path or f"{_BASE}/afib_atrial.npz", allow_pickle=True)
    if int(a["W"]) != int(w["W"]) or int(a["stride"]) != int(w["stride"]):
        raise RuntimeError(
            f"창 설정 불일치: 특징 W={int(a['W'])}/stride={int(a['stride'])} vs "
            f"창 W={w['W']}/stride={w['stride']} — 같은 값으로 다시 만드세요.")
    names = [str(x) for x in a["names"]]
    K = {(int(p), int(s)): i for i, (p, s) in enumerate(a["key"])}
    F = a["feat"]
    M = np.full((len(w["y"]), F.shape[1]), np.nan, "float32")
    hit = 0
    for r, (p, s) in enumerate(w["key"]):
        j = K.get((int(p), int(s)))
        if j is not None:
            M[r] = F[j]; hit += 1
    miss = np.isnan(M[:, 0])
    med = np.nanmedian(M, axis=0)
    med = np.where(np.isfinite(med), med, 0.0)
    M = np.where(np.isnan(M), med, M).astype("float32")
    w = dict(w)
    w["n_rr"] = int(w["aux"].shape[1])      # ★RR/심방 경계 — 팔이 열을 고르는 기준
    w["aux"] = np.concatenate([w["aux"], M, miss.astype("float32")[:, None]], 1)
    w["aux_names"] = ([f"rr{i}" for i in range(w["n_rr"])] + names + ["atr_missing"])
    if verbose:
        print(f"\n[심방활동 결합] 창 {len(w['y']):,} 중 {hit:,} 결합 "
              f"({100*hit/len(w['y']):.1f}%)  보조특징 10 → {w['aux'].shape[1]}")
        print(f"  추출 실패·미결합 {int(miss.sum()):,} → 열 중앙값으로 대체 + 표시열 추가")
        if hit == 0:
            print(f"  ✗ 하나도 결합되지 않았습니다 — 코퍼스와 특징의 W/stride 또는 "
                  f"pid 규약이 다릅니다.")
    return w


def _arm_rsn_atrial(w, tr, te, ncls, seed, epochs=20):
    """A4. RSN + RR산포 + **심방활동**. A2 와의 차이가 곧 심방축의 순효과다."""
    return _fit_win(w, tr, te, ncls, seed, use_seq=True, aux="all", epochs=epochs)


def _arm_atrial_only(w, tr, te, ncls, seed, epochs=20):
    """A4c. 심방활동 스칼라만(시퀀스 제거) — AFL 의 이득이 정말 심방축에서
       오는지 가르는 대조군. A4 만 보면 RSN 덕인지 심방 덕인지 알 수 없다."""
    return _fit_win(w, tr, te, ncls, seed, use_seq=False, aux="atrial", epochs=epochs)


def _arm_rsn_dom(w, tr, te, ncls, seed, epochs=20):
    """A3. RSN + DB 조건부 FiLM. ★같은 DB 안에서만 오르면 사전확률 암기다 →
       판정은 반드시 bench_afib(split="db") 로 한다."""
    return _fit_win(w, tr, te, ncls, seed, use_seq=True, aux="rr",
                    n_domain=len(set(map(str, w["db"]))), epochs=epochs)


# ★A4 계열은 attach_atrial() 을 거친 w 에서만 의미가 있다. 기본 팔에 넣으면
#   심방특징 없이 조용히 돌아 "심방축은 효과 없음" 이라는 가짜 결론을 만든다.
ATRIAL_ARMS = {
    "A4.RSN+심방활동": _arm_rsn_atrial,
    "A4c.심방활동만": _arm_atrial_only,
}

# ★팔이 실제로 어떤 입력을 받는지 함수에 못 박아 두고, 벤치 시작 때 출력한다.
#   (한 번 두 팔이 같은 입력을 받는 배선 오류로 사전등록 비교가 통째로 무효가 된
#    적이 있다. 선언을 눈에 보이게 두는 것이 재발 방지의 절반이다.)
for _f, _seq, _ax in ((_arm_trivial, False, "none"), (_arm_rrdisp, False, "rr"),
                      (_arm_rsn, True, "rr"), (_arm_rsn_nodisp, True, "none"),
                      (_arm_rsn_dom, True, "rr"), (_arm_rsn_atrial, True, "all"),
                      (_arm_atrial_only, False, "atrial")):
    _f._use_seq, _f._aux_mode = _seq, _ax
del _f, _seq, _ax

DEFAULT_ARMS = {
    "A0.자명": _arm_trivial,
    "A1.RR산포": _arm_rrdisp,
    "A2.RSN": _arm_rsn,
    "A2c.RSN(스칼라X)": _arm_rsn_nodisp,
    "A3.RSN+도메인": _arm_rsn_dom,
}


# ─────────────────────────────────────────────────────────────────────────────
#  5. 벤치
# ─────────────────────────────────────────────────────────────────────────────
def _cost(w, arms, folds, epochs):
    """연산량 환산 비용 경고 — 추측이 아니라 MAC 을 세어 **실측 앵커**와 비교한다.

    앵커: 이미 돌려 본 SVDB 벤치 = 87 TMAC = 실측 '수십 분'(L4).
    ltafdb 를 넣으면 창이 10만 개까지 늘어 몇 시간이 될 수 있으므로, 돌리기 전에
    숫자를 보여 준다. 먼저 dbs=("afdb","mitdb") 로 배관을 검증하는 것을 권한다.
    """
    L = w["seq"].shape[2]
    mac = 4 * 64 * 5 * L                       # 첫 conv (k=5)
    rf, d = 5, 1
    while rf < L and d <= 64:                  # _rsn 의 수용야 자동확장과 동일한 규칙
        d *= 2; mac += 64 * 64 * 3 * L; rf += 2 * d
    nseq = sum(1 for a in arms if a.startswith(("A2", "A3")))
    ntr = sum(len(tr) for _, tr, _ in folds)
    tot = nseq * ntr * epochs * 3 * mac        # 순전파+역전파 ≈ 3배
    r = tot / 87e12
    print(f"    수용야 {rf}/{L}  창당 {mac/1e6:.1f} MMAC  학습창·에폭 {nseq*ntr*epochs:,}")
    print(f"    연산량 {tot/1e12:.0f} TMAC ≈ SVDB 벤치(실측 '수십 분')의 {r:.1f}배 "
          f"→ L4 기준 대략 {int(20*r)}~{int(35*r)}분 예상.")
    if rf < L:
        print(f"    ⚠ 수용야 {rf} < 창 {L} — 창 끝을 아예 못 본다. W 를 줄일 것.")
    if r > 3:
        print(f"    ⚠ 먼저 dbs=(\"afdb\",\"mitdb\") + k=3 으로 배관을 검증하고 늘릴 것.")


def bench_afib(w, k=5, n_rep=1, split="patient", only=None, epochs=20, verbose=True):
    """창단위 2층 벤치.

    split="patient" : GroupKFold(환자)  — 같은 DB 안 일반화
    split="db"      : leave-one-DB-out — ★A3(도메인 FiLM)의 진짜 판정
    """
    from sklearn.model_selection import GroupKFold
    y, pid, dbv = w["y"], w["pid"], np.array(list(map(str, w["db"])))
    keep = np.flatnonzero(y >= 0)                 # 전이구간 제외
    cls = w["classes"]; ncls = len(cls)
    arms = dict(DEFAULT_ARMS)
    # 심방특징이 실제로 붙어 있을 때만 A4 계열을 켠다(가짜 음성 결론 방지)
    if w["aux"].shape[1] > 10:
        arms.update(ATRIAL_ARMS)
    elif any(a.startswith("A4") for a in (only or ())):
        raise RuntimeError("A4 계열은 심방특징이 필요합니다 — "
                           "w = attach_atrial(w) 를 먼저 하세요.")
    arms.update(ARMS)
    if only:
        arms = {a: f for a, f in arms.items() if a in set(only)}
    OUT = {"classes": cls, "res": {}, "split": split}
    folds = []
    if split == "db":
        for db in sorted(set(dbv[keep])):
            te = keep[dbv[keep] == db]; tr = keep[dbv[keep] != db]
            if len(np.unique(y[te])) < 2:
                print(f"  ⚠ {db}: 테스트에 클래스가 1종뿐 → 건너뜀"); continue
            folds.append((f"LODO:{db}", tr, te))
    else:
        for rep in range(n_rep):
            gkf = GroupKFold(n_splits=k)
            for fi, (a, b) in enumerate(gkf.split(keep, y[keep], groups=pid[keep])):
                folds.append((f"r{rep}f{fi}", keep[a], keep[b]))
    print(f"\n=== 2층 벤치 [{split}]  팔 {len(arms)} × 폴드 {len(folds)} = "
          f"{len(arms)*len(folds)}회 학습 ===")
    _cost(w, arms, folds, epochs)
    nrr = int(w.get("n_rr", w["aux"].shape[1])); nall = w["aux"].shape[1]
    print(f"    보조특징: RR {nrr}열" + (f" + 심방 {nall-nrr}열 = {nall}" if nall > nrr
                                        else " (심방특징 없음)"))
    for a, f in arms.items():                 # ★팔별 실제 입력 선언 — 배선 감사용
        md = getattr(f, "_aux_mode", "?"); sq = getattr(f, "_use_seq", None)
        nc = len(_aux_cols(w, md)) if md in ("none", "rr", "atrial", "all") else -1
        print(f"      {a:<18} 시퀀스 {'O' if sq else 'X' if sq is False else '?'}  "
              f"보조 {md}({nc}열)")
    for nm, fn in arms.items():
        P = np.full(len(y), -1, np.int64)
        S = np.zeros((len(y), ncls), "float32")
        for fname, tr, te in folds:
            pr = fn(w, tr, te, ncls, seed=abs(hash(fname)) % 10000, epochs=epochs)
            P[te] = pr.argmax(1); S[te] = pr
            if verbose:
                print(f"  {nm:<18}{fname}  학습 {len(tr):,} / 테스트 {len(te):,}")
        m = P >= 0
        OUT["res"][nm] = dict(pred=P, score=S, mask=m)
    OUT["w"] = dict(y=y, pid=pid, db=dbv, dur=w["dur"], nov=w["nov"], t0=w["t0"])
    _check_distinct(OUT)
    return OUT


def _check_distinct(OUT, verbose=True):
    """★서로 다른 팔이 **똑같은 예측**을 냈는지 검사한다.

    왜 필요한가: 실제로 A2 와 A4 가 비트 단위로 같은 예측을 낸 적이 있다. 두 팔이
    같은 함수를 호출하고 있었는데(둘 다 w["aux"] 전체를 씀), 표에는 서로 다른
    이름으로 나란히 찍히니 **'효과 없음'으로 읽히고 넘어갈 뻔했다.** 값이 같으면
    그것은 결과가 아니라 배선 오류다. 조용히 지나가지 않게 여기서 잡는다.
    """
    ks = [k for k in OUT["res"] if not k.startswith("A0")]
    dup = []
    for i in range(len(ks)):
        for j in range(i + 1, len(ks)):
            a, b = OUT["res"][ks[i]]["pred"], OUT["res"][ks[j]]["pred"]
            if a.shape == b.shape and np.array_equal(a, b):
                dup.append((ks[i], ks[j]))
    if dup and verbose:
        print(f"\n  ✗✗ 배선 오류: 서로 다른 팔이 **동일한 예측**을 냈습니다")
        for a, b in dup:
            print(f"      {a}  ≡  {b}")
        print(f"      → 두 팔이 같은 입력·같은 함수를 쓰고 있습니다. 결과가 아니라 버그입니다.")
        print(f"      → 각 팔의 aux 모드(_aux_cols)와 use_seq 를 확인하세요.")
    elif verbose:
        print(f"  ✔ 팔 {len(ks)}개가 서로 다른 예측을 냄(배선 정상)")
    return dup


def report_afib(OUT, base="A1.RR산포", show=True):
    """창 F1 / 에피소드 / burden 을 한 판에. ★사전등록 가설도 함께 판정한다."""
    cls = OUT["classes"]; W = OUT["w"]
    y, pid = W["y"], W["pid"]
    rows = {}
    print(f"\n=== 2층 결과 [{OUT['split']}] — 창단위 환자매크로 F1 ===")
    hdr = "  " + f"{'arm':<20}" + "".join(f"{c:>9}" for c in cls) + f"{'평균':>9}"
    print(hdr)
    for nm, r in OUT["res"].items():
        m = r["mask"]
        f = win_macro(r["pred"][m], y[m], pid[m], cls)
        rows[nm] = f
        vals = [f[c][0] for c in cls]
        print("  " + f"{nm:<20}" + "".join(f"{v:>9.3f}" for v in vals)
              + f"{np.nanmean(vals):>9.3f}")
    print("  " + f"{'(보유 환자 수)':<20}" + "".join(f"{rows[list(rows)[0]][c][1]:>9}" for c in cls))

    if not show:
        return rows
    for nm, r in OUT["res"].items():
        if nm.startswith("A0"):
            continue
        print(f"\n  ── {nm} ──")
        m = r["mask"]
        for ci, c in enumerate(cls):
            if c == "N":
                continue
            episode_metrics(r["pred"][m], y[m], pid[m], W["t0"][m], W["nov"][m],
                            ci, name=c)
            burden_metrics(r["pred"][m], y[m], pid[m], W["dur"][m], ci, name=c)

    # ── 검정력 갱신: 가정 σ 를 실측으로 대체 ──────────────────────────────
    sigma_measured(OUT)

    # ── 사전등록 가설 판정 ────────────────────────────────────────────────
    #  ★판정은 **짝지은 부트스트랩**으로 한다. 예전엔 '2×MDE 막대'를 썼는데 그건
    #    어림이다. MDE 는 "이 표본에서 검출 가능한 최소 효과"이지 "이 비교의 불확실성"이
    #    아니다. 두 팔이 같은 환자를 보므로 짝지으면 훨씬 좁은 구간이 나온다.
    if base in rows:
        print(f"\n=== 사전등록 판정 (기준 {base}, 짝지은 부트스트랩 B=5000) ===")
        cand = [a for a in ("A2.RSN", "A2c.RSN(스칼라X)", "A3.RSN+도메인") if a in rows]
        print(f"\n  [H-J] 창 F1 — 95% CI 가 0 을 배제해야 지지")
        for nm in cand:
            for c in cls:
                if c == "N":
                    continue
                try:
                    paired_win(OUT, nm, base, cls=c)
                except Exception as e:
                    print(f"    [{c}] {nm}: 검정 실패 {type(e).__name__}: {e}")
        print(f"\n  [H-K] burden 오차 — LoA 폭 비의 95% CI 가 1 을 배제해야 지지")
        for nm in cand:
            for c in cls:
                if c == "N":
                    continue
                try:
                    paired_burden(OUT, nm, base, cls=c)
                except Exception as e:
                    print(f"    [{c}] {nm}: 검정 실패 {type(e).__name__}: {e}")
        # ── H-N/H-O/H-Q: 심방축의 **순효과**. 기준은 A1 이 아니라 A2 다 ──────
        #  ★이 블록이 없어서 A4 가 사전등록 표에 통째로 빠진 적이 있다. 팔은 돌았고
        #    F1 도 찍혔는데 검정만 안 돼서, 표를 눈으로 비교하고 넘어갈 뻔했다.
        #    가설이 있으면 검정도 자동으로 돌아야 한다 — 손으로 고른 목록은 또 샌다.
        a2, a4, a4c = "A2.RSN", "A4.RSN+심방활동", "A4c.심방활동만"
        if a4 in rows and a2 in rows:
            print(f"\n  [H-N/H-O] 심방축 순효과 — A4 − A2 (기준이 A1 이 아님에 주의)")
            print(f"    H-N: AFL 에서 > 0 이어야 지지 / H-O: AFIB 에서 ≈ 0 이 예측")
            for c in cls:
                if c == "N":
                    continue
                try:
                    paired_win(OUT, a4, a2, cls=c)
                except Exception as e:
                    print(f"    [{c}] {a4}: 검정 실패 {type(e).__name__}: {e}")
        if a4 in rows and a4c in rows:
            print(f"\n  [H-Q] 시퀀스가 정말 필요한가 — A4 − A4c (AFL 에서 > 0 이어야 지지)")
            for c in cls:
                if c == "N":
                    continue
                try:
                    paired_win(OUT, a4, a4c, cls=c)
                except Exception as e:
                    print(f"    [{c}] {a4} vs {a4c}: 검정 실패 {type(e).__name__}: {e}")

        print(f"\n  ※ Bonferroni: 위 비교가 k 개면 유의수준을 k 로 나눠야 한다."
              f" 95% CI 는 보정 전 값이므로,\n    경계에 걸친 결과는 지지로 읽지 않는다.")
        print(f"  ※ H-L(AFL 에서 A2−A1 ≤ 0)은 **영가설 방향의 예측**이다. AFL 은 환자 수가"
              f" 적어\n    크기는 보고하지 않고 방향만 취한다(사전등록 §8.4).")
        # ★A3 은 split="patient" 에서 유의해도 지지로 읽으면 안 된다 ────────────
        if OUT["split"] != "db" and "A3.RSN+도메인" in rows:
            dbs = sorted(set(map(str, OUT["w"]["db"])))
            print(f"\n  ✗ [A3 판정 보류] split=\"{OUT['split']}\" 에서는 A3 을 판정하지 않는다"
                  f"(사전등록 §5·§6).")
            print(f"    A3 은 창이 어느 DB 에서 왔는지를 입력으로 받는다. 지금 DB 는 {dbs} 이고")
            print(f"    각 DB 의 리듬 구성이 크게 다르므로, 'DB 이름'만으로 리듬을 상당 부분")
            print(f"    맞힐 수 있다 — 일반화가 아니라 **사전확률 암기**다. 위 A3 결과가")
            print(f"    유의하게 나왔다면 그것이야말로 암기를 의심할 근거다.")
            print(f"    → 판정: OUT_db = bench_afib(w, split=\"db\"); report_afib(OUT_db)")
            for db in dbs:                      # 암기가 실제로 가능한지 수치로 보인다
                m = (np.array(list(map(str, OUT["w"]["db"]))) == db) & (OUT["w"]["y"] >= 0)
                if m.sum():
                    cnt = np.bincount(OUT["w"]["y"][m], minlength=len(cls))
                    top = cnt.argmax()
                    print(f"      {db:<10} 창 {int(m.sum()):>6,}  최빈 {cls[top]} "
                          f"{100*cnt[top]/m.sum():.1f}%  ← DB 이름만으로 이만큼 맞힌다")
    return rows


# ─────────────────────────────────────────────────────────────────────────────
#  6. 자기검증 — 합성 RR 로 wfdb/torch 없이 로직만 검증
# ─────────────────────────────────────────────────────────────────────────────
def _synth_rr(n_pat=12, n_beat=1200, seed=0):
    """합성 코퍼스: 환자마다 N 구간과 AFIB 구간을 번갈아 만든다.
    AFIB 는 RR 이 불규칙(σ 큼), AFL 은 규칙적이되 빠름 — ★AFL 이 RR 로 구분 안 되는
    구조를 일부러 재현한다(H-L 이 검증 가능한 실험인지 확인하기 위함)."""
    rng = np.random.RandomState(seed)
    T = []; PRE = []; PID = []; RHY = []; DB = []
    names = ["N", "AFIB", "AFL"]
    for p in range(n_pat):
        base = rng.uniform(0.7, 1.0)
        rr = []; lab = []
        while len(rr) < n_beat:
            k = rng.choice([0, 1, 2], p=[0.6, 0.3, 0.1])
            m = rng.randint(150, 400)
            if k == 0:
                v = base + rng.randn(m) * 0.03
            elif k == 1:
                v = base + rng.randn(m) * 0.18          # AF: 불규칙
            else:
                v = base * 0.65 + rng.randn(m) * 0.02   # AFL: 규칙적·빠름
            rr += list(np.clip(v, 0.25, 2.5)); lab += [k] * m
        rr = np.array(rr[:n_beat]); lab = np.array(lab[:n_beat])
        T += list(np.cumsum(rr)); PRE += list(rr * FS_RR)
        PID += [p] * n_beat; RHY += list(lab); DB += ["synth"] * n_beat
    return dict(t=np.array(T, "float32"), pre_rr=np.array(PRE, "float32"),
                post_rr=np.array(PRE, "float32"), pid=np.array(PID, np.int64),
                rhythm=np.array(RHY, np.int64), rhythm_names=names,
                db=np.array(DB), rr_edge=np.zeros(len(T), bool),
                y5=np.full(len(T), -1, np.int64))


def selftest():
    ok = lambda c, m: (_ for _ in ()).throw(AssertionError(m)) if not c else print(f"  ✔ {m}")
    print("=== afib_bench 자기검증 ===")
    d = _synth_rr()
    w = make_windows(d, W=64, verbose=False)
    ok(w["seq"].shape[1] == 4 and w["seq"].shape[2] == 64, "창 텐서 모양 [N,4,64]")
    ok(w["aux"].shape[1] == 10, "보조 스칼라 10종")
    ok(np.isfinite(w["seq"]).all() and np.isfinite(w["aux"]).all(), "NaN/Inf 없음")
    ok(w["nov"].sum() == len(w["y"]), "stride=W 면 모든 창이 비중첩")
    ok((w["y"] == -1).sum() > 0, "전이구간이 -1 로 분리됨")

    # 채널이 무차원인지: RR 을 통째로 2배(심박 절반)해도 채널이 거의 같아야 한다
    d2 = dict(d); d2["pre_rr"] = d["pre_rr"] * 1.5
    w2 = make_windows(d2, W=64, verbose=False)
    dev = float(np.abs(w["seq"][:, :3] - w2["seq"][:, :3]).max())
    ok(dev < 0.05, f"심박 1.5배에도 채널 불변(최대차 {dev:.4f}) — DB 간 전이의 전제")

    # AFL 이 RR 산포로 구분 안 되는가(= H-L 이 유의미한 실험인가)
    aux, yy = w["aux"], w["y"]
    ent_n = aux[yy == 0, 4].mean(); ent_af = aux[yy == 1, 4].mean(); ent_fl = aux[yy == 2, 4].mean()
    ok(ent_af > ent_n + 0.05, f"AFIB 는 ΔRR 엔트로피가 높다 ({ent_af:.3f} vs N {ent_n:.3f})")
    ok(abs(ent_fl - ent_n) < abs(ent_af - ent_n),
       f"AFL 은 N 과 산포가 비슷하다 ({ent_fl:.3f}) — RR-only 로는 못 가른다")

    # 지표 로직
    yv = np.array([0, 1, 1, 0, 1, 1, 1, 0]); pv = np.array([0, 1, 0, 0, 1, 1, 1, 0])
    pv_ = np.arange(8) * 0; pidv = np.zeros(8, np.int64)
    t0 = np.arange(8, dtype="float32"); nov = np.ones(8, bool)
    e = episode_metrics(pv, yv, pidv, t0, nov, 1, verbose=False)
    ok(e["n_true"] == 2 and e["se"] == 1.0, "에피소드: 참 2건 모두 중첩 검출")
    ok(e["n_pred"] == 2 and e["ppv"] == 1.0, "에피소드: 예측 2건 모두 참과 중첩")
    dur = np.ones(8, "float32")
    b = burden_metrics(pv, yv, pidv, dur, 1, verbose=False)
    ok(b["n"] == 1, "burden: 환자 1명")
    f = win_macro(pv, yv, pidv, ["N", "AFIB"])
    # 참 AFIB 5창 중 4창 적중(TP=4), 위양성 0, 위음성 1 → F1 = 8/9
    ok(abs(f["AFIB"][0] - 8 / 9) < 1e-9, "창 F1 계산 정확 (TP4/FP0/FN1 → 8/9)")
    ok(np.isnan(win_macro(np.zeros(4, np.int64), np.zeros(4, np.int64),
                          np.zeros(4, np.int64), ["N", "AFIB"])["AFIB"][0]),
       "그 리듬이 없는 환자만 있으면 NaN (0 으로 위장하지 않음)")

    # burden 은 시간가중이어야 한다 — 창 길이가 다르면 개수 세기와 달라진다
    #  AF 창은 index 1,2,4,5,6 → 시간 9+1+1+1+1 = 13, 전체 16 → 81.25%
    #  창 개수로 세면 5/8 = 62.5% 라 다른 값이 나온다.
    dur2 = np.array([1, 9, 1, 1, 1, 1, 1, 1], "float32")
    b2 = burden_metrics(yv, yv, pidv, dur2, 1, verbose=False)
    ok(abs(b2["true"][0] - 100 * 13 / 16) < 1e-4,
       f"burden 이 시간가중 ({b2['true'][0]:.2f}% ≠ 개수기준 62.50%)")

    ok(set(DEFAULT_ARMS) >= {"A0.자명", "A1.RR산포", "A2.RSN", "A3.RSN+도메인"}, "기본 팔 등록")

    # ── 짝지은 검정 (H-J / H-K) ────────────────────────────────────────────
    #  torch 없이 검증하려고 예측을 손으로 만든 가짜 OUT 을 쓴다.
    rng = np.random.RandomState(0)
    wf = make_windows(_synth_rr(n_pat=40, n_beat=1500, seed=1), W=64, verbose=False)
    keep = wf["y"] >= 0
    yv, pidv = wf["y"], wf["pid"]

    def mkout(preds):
        return dict(classes=wf["classes"], split="patient",
                    res={k: dict(pred=np.where(keep, p, -1), mask=keep.copy(),
                                 score=None) for k, p in preds.items()},
                    w=dict(y=yv, pid=pidv, db=wf["db"], dur=wf["dur"],
                           nov=wf["nov"], t0=wf["t0"]))

    def noisy(flip):
        p = yv.copy()
        f = rng.rand(len(p)) < flip
        p[f] = rng.randint(0, 3, f.sum())
        return p

    perfect = yv.copy()
    O = mkout({"A1.RR산포": noisy(0.30), "A2.RSN": noisy(0.05), "same": None})
    O["res"]["same"] = dict(pred=np.where(keep, O["res"]["A1.RR산포"]["pred"], -1),
                            mask=keep.copy(), score=None)

    # (1) 같은 예측끼리는 차이가 정확히 0이고 CI 도 0을 포함해야 한다
    s = paired_win(O, "same", "A1.RR산포", cls="AFIB", B=400, verbose=False)
    ok(abs(s["delta"]) < 1e-12 and s["ci"][0] <= 0 <= s["ci"][1],
       "짝지은 F1: 동일 예측 → Δ=0, CI 가 0 포함")
    sb = paired_burden(O, "same", "A1.RR산포", cls="AFIB", B=400, verbose=False)
    ok(abs(sb["ratio_loa"] - 1.0) < 1e-12 and sb["ratio_ci"][0] <= 1 <= sb["ratio_ci"][1],
       "짝지은 burden: 동일 예측 → 비=1, CI 가 1 포함")

    # (2) 명백히 나은 팔은 잡아내야 한다(검정력 확인 — 통계가 무디면 여기서 걸린다)
    s2 = paired_win(O, "A2.RSN", "A1.RR산포", cls="AFIB", B=1000, verbose=False)
    ok(s2["delta"] > 0 and s2["ci"][0] > 0, f"짝지은 F1: 5%오류 > 30%오류 검출 (Δ={s2['delta']:+.3f})")
    sb2 = paired_burden(O, "A2.RSN", "A1.RR산포", cls="AFIB", B=1000, verbose=False)
    ok(sb2["ratio_loa"] < 1 and sb2["ratio_ci"][1] < 1,
       f"짝지은 burden: LoA 폭 비 {sb2['ratio_loa']:.3f}, CI 상한 {sb2['ratio_ci'][1]:.3f} < 1")

    # (3) 환자 집합이 어긋나면 조용히 넘어가지 말고 예외를 던져야 한다
    Obad = mkout({"A1.RR산포": noisy(0.3), "A2.RSN": noisy(0.1)})
    Obad["res"]["A2.RSN"]["mask"] = keep & (pidv != pidv.max())
    try:
        paired_burden(Obad, "A2.RSN", "A1.RR산포", cls="AFIB", B=50, verbose=False)
        ok(False, "환자 집합 불일치에 예외")
    except RuntimeError:
        ok(True, "환자 집합이 어긋나면 예외 — 잘못된 짝짓기를 조용히 통과시키지 않음")

    # (4) 실측 σ 가 계산되고 유한해야 한다
    sg = sigma_measured(O, verbose=False)
    ok(all(np.isfinite(v[0]) and v[0] >= 0 for v in sg.values()), "실측 σ 가 유한·비음수")

    # ── 배선 검증 (★ A2 ≡ A4 사고 재발 방지) ─────────────────────────────
    #  심방특징이 붙은 w 를 흉내 내고, 팔마다 **다른 열**을 받는지 직접 센다.
    wa = dict(w); wa["n_rr"] = 10
    wa["aux"] = np.concatenate([w["aux"], np.zeros((len(w["y"]), 21), "float32")], 1)
    ok(len(_aux_cols(wa, "rr")) == 10 and len(_aux_cols(wa, "all")) == 31 and
       len(_aux_cols(wa, "atrial")) == 21 and len(_aux_cols(wa, "none")) == 0,
       "aux 모드별 열 수: none 0 / rr 10 / atrial 21 / all 31")
    md = {a: getattr(f, "_aux_mode", None)
          for a, f in {**DEFAULT_ARMS, **ATRIAL_ARMS}.items()}
    ok(all(v is not None for v in md.values()), "모든 팔이 aux 모드를 선언함")
    ok(md["A2.RSN"] == "rr" and md["A4.RSN+심방활동"] == "all",
       "A2 는 RR 만, A4 는 RR+심방 — 두 팔의 차이가 곧 심방축의 순효과")
    ok(len(_aux_cols(wa, md["A2.RSN"])) != len(_aux_cols(wa, md["A4.RSN+심방활동"])),
       "A2 와 A4 가 실제로 다른 입력을 받음(같으면 비교가 무의미)")
    ok(getattr(_arm_atrial_only, "_use_seq") is False, "A4c 는 시퀀스를 쓰지 않음")
    # 심방특징이 없는 w 에서 "atrial" 을 요구하면 조용히 0열이 아니라 예외여야 한다
    try:
        _aux_cols(w, "atrial"); ok(False, "심방특징 없이 atrial 요구 시 예외")
    except RuntimeError:
        ok(True, "심방특징 없이 A4c 를 돌리면 예외 — 빈 입력으로 조용히 돌지 않음")
    dup = _check_distinct(mkout({"A1.RR산포": perfect.copy(), "A2.RSN": perfect.copy()}),
                          verbose=False)
    ok(len(dup) == 1, "동일 예측 두 팔을 배선 오류로 검출")
    print("=== 전 항목 통과 ===")
    return True


if __name__ == "__main__":
    import sys
    if "--selftest" in sys.argv:
        selftest()
