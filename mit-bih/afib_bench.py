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


def make_windows(d, W=W_WIN, stride=None, purity=PURITY, classes=AF_CLASSES,
                 verbose=True):
    """비트 코퍼스 → 창 데이터셋.

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
    SEQ = []; AUX = []; Y = []; PID = []; DB = []; DUR = []; NOV = []; T0 = []; PUR = []
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
        for s in range(0, len(idx) - W + 1, stride):
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
            NOV.append(s % W == 0); PUR.append(float(pu))
    if not SEQ:
        raise RuntimeError(f"창이 하나도 안 만들어졌습니다 — W={W} 가 레코드 길이보다 큰지 확인.")
    w = dict(seq=np.stack(SEQ), aux=np.stack(AUX), y=np.array(Y, np.int64),
             pid=np.array(PID, np.int64), db=np.array(DB),
             dur=np.array(DUR, "float32"), nov=np.array(NOV, bool),
             t0=np.array(T0, "float32"), pur=np.array(PUR, "float32"),
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


def win_macro(pred, y, pid, classes):
    """창단위 **환자매크로 F1** — 1층과 같은 추정량이라 층 간 비교가 성립한다."""
    out = {}
    for c, nm in enumerate(classes):
        v = []
        for p in np.unique(pid):
            m = pid == p
            if not (y[m] == c).any():
                continue                       # 그 리듬이 없는 환자는 제외(1층 규약)
            v.append(_f1_af(pred[m] == c, y[m] == c))
        out[nm] = (float(np.mean(v)) if v else float("nan"), len(v))
    return out


def burden_metrics(pred, y, pid, dur, cls_idx, verbose=True, name="AFIB"):
    """AF burden(= AF 시간 / 전체 시간) 추정 정확도 — Pearson r + Bland-Altman.

    ★임상에서 실제로 쓰는 숫자는 "이 박이 AF 냐"가 아니라 "이 환자가 하루의 몇 %를
      AF 로 보내느냐"다. 항응고 결정·재발 감시가 전부 burden 기준이다.
      그래서 F1 이 같아도 burden 오차가 다르면 임상 가치가 다르다.
    ★시간 가중이다(창마다 길이가 다르므로 창 개수로 세면 편향된다).
    """
    tb, pb = [], []
    for p in np.unique(pid):
        m = pid == p
        tot = float(dur[m].sum())
        if tot <= 0:
            continue
        tb.append(100.0 * float(dur[m][y[m] == cls_idx].sum()) / tot)
        pb.append(100.0 * float(dur[m][pred[m] == cls_idx].sum()) / tot)
    tb, pb = np.array(tb), np.array(pb)
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
#  4. 팔(arm) — A0 자명 / A1 고전 RR산포 / A2 RSN / A3 RSN+도메인
# ─────────────────────────────────────────────────────────────────────────────
def _torch():
    import torch
    return torch, torch.nn


def _fit_win(w, tr, te, ncls, seed, use_seq=True, use_aux=True, n_domain=0,
             epochs=20, bs=256, lr=1e-3):
    """창 분류기 학습. 인코더는 1층과 **같은** `_rsn`(형태 가지 끔)."""
    torch, nn = _torch()
    g = globals()
    if "_rsn" not in g:
        raise RuntimeError("_rsn 없음 — svdb_rhythm.py 를 먼저 로드하세요 (colab_setup.sync()).")
    torch.manual_seed(seed); np.random.seed(seed)
    dev = "cuda" if torch.cuda.is_available() else "cpu"
    L = w["seq"].shape[2]
    daux = w["aux"].shape[1] if use_aux else 0
    net = g["_rsn"](4, L, daux, use_morph=False, use_seq=use_seq,
                    n_class=ncls, n_domain=n_domain).to(dev)
    dom_ids = None
    if n_domain > 0:
        uds = sorted(set(map(str, w["db"])))
        dm = {d: i for i, d in enumerate(uds)}
        dom_ids = np.array([dm[str(x)] for x in w["db"]], np.int64)

    X = torch.tensor(w["seq"]); A = torch.tensor(w["aux"] if use_aux else
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
    A = torch.tensor(w["aux"]); Y = torch.tensor(w["y"])
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
    """A2. RSN 시퀀스 — 1층에서 유일하게 살아남은 효과(R1−R5 = +0.105)의 이식."""
    return _fit_win(w, tr, te, ncls, seed, use_seq=True, use_aux=True, epochs=epochs)


def _arm_rsn_nodisp(w, tr, te, ncls, seed, epochs=20):
    """A2c. RSN 시퀀스만(스칼라 보조 제거) — A2 의 이득이 스칼라 덕인지 가르는 대조군."""
    return _fit_win(w, tr, te, ncls, seed, use_seq=True, use_aux=False, epochs=epochs)


def _arm_rsn_dom(w, tr, te, ncls, seed, epochs=20):
    """A3. RSN + DB 조건부 FiLM. ★같은 DB 안에서만 오르면 사전확률 암기다 →
       판정은 반드시 bench_afib(split="db") 로 한다."""
    return _fit_win(w, tr, te, ncls, seed, use_seq=True, use_aux=True,
                    n_domain=len(set(map(str, w["db"]))), epochs=epochs)


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
    arms = dict(DEFAULT_ARMS); arms.update(ARMS)
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
    return OUT


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

    # ── 사전등록 가설 판정 ────────────────────────────────────────────────
    if base in rows:
        print(f"\n=== 사전등록 판정 (기준 {base}, Bonferroni k=4) ===")
        mde = {c: 1.96 * 0.32 / max(np.sqrt(rows[base][c][1]), 1) for c in cls}
        for nm in ("A2.RSN", "A3.RSN+도메인"):
            if nm not in rows:
                continue
            for c in cls:
                if c == "N":
                    continue
                dlt = rows[nm][c][0] - rows[base][c][0]
                bar = mde[c] * 2.0        # Bonferroni k=4 ≈ z 1.96→2.50, 여유 있게 2×
                v = "★유의" if dlt > bar else ("미달" if dlt > 0 else "역행")
                print(f"  {nm} − {base}  [{c}]  Δ={dlt:+.3f}  기준 {bar:+.3f}  {v}")
        print(f"  ※ H-L(AFL 에서 A2−A1 ≤ 0)은 **영가설 방향의 예측**이다. 그것이 확인되면"
              f"\n    'AFL 은 RR 로 안 된다 → 형태축이 필요하다'의 직접 근거가 된다.")
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
    print("=== 전 항목 통과 ===")
    return True


if __name__ == "__main__":
    import sys
    if "--selftest" in sys.argv:
        selftest()
