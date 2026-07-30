# =============================================================================
#  ecg_multidb.py  —  다중 DB 통합: 5-class 비트 + 리듬(질병) 라벨
#
#  ── 왜 방향을 바꾸는가 ──────────────────────────────────────────────────────
#  목표가 "SVEB 뿐 아니라 질환·파형 전반에서 정답률이 높은 모델" 이라면 SVDB 하나로는
#  불가능하다. `label_audit()` 실측이 그것을 확정했다:
#     SVDB:  F=23, Q=79 (99% 주장에 필요한 381개의 6%·21%)
#            리듬 주석 보유 레코드 1/78, 라벨 종류도 'N' 하나
#     → SVDB 는 S 를 풍부하게 담은 **3-class SVEB 벤치마크**이지 다질환 데이터가 아니다.
#
#  이미 Drive 에 세 DB 가 있다. 합치면 클래스·질환·환자 수가 모두 늘어난다:
#     mamba_data.npz  MIT-BIH Arrhythmia  99,871비트 / 48레코드  — F·/(페이스)·리듬 주석 풍부
#     svdb_data.npz   MIT-BIH SVDB       184,397비트 / 78레코드  — S 가 풍부
#     incart_data.npz INCART             175,571비트 / 75레코드  — V 가 풍부(20,006)
#
#  ★RSN 이 이 통합에 유리한 이유: 리듬 채널을 전부 무차원(환자별 med/MAD 정규화 +
#    tanh)으로 설계했다. 심박수·진폭·샘플링에 불변이라 DB 를 섞어도 축이 흔들리지
#    않는다. PAPER §6.5 가 교차DB 에서 이 성질을 이미 검증했다(RHYTHM 7.9× lift).
#
#  ── 무엇을 만드나 ───────────────────────────────────────────────────────────
#   db_audit(dbs)    : DB 별·통합 재고조사 + 클래스/리듬별 검정력. **먼저 이걸 볼 것**
#   incart_groups()  : INCART 의 레코드→환자 묶기(PAPER §6.5 L3 미해결 문제)
#   build_multi(dbs) : 통합 데이터셋 생성 (환자 ID 전역 유일, 5-class + 리듬)
#
#  ⚠ 검정력 교환을 알고 들어갈 것: SVDB 는 S 보유 73환자(MDE 0.07)였다. MIT-BIH 는
#    S 보유 16환자(MDE 0.16)다. **통합하면 S 검정력은 늘지만, MIT-BIH 만 쓰면 줄어든다.**
#    클래스마다 검정력이 다르므로 db_audit 이 클래스별로 따로 계산해 준다.
#
#  선행: svdb_labels.py 가 같은 globals 에 로드돼 있어야 한다(AAMI5/BEAT_SYMS 등 재사용).
#  실행:
#    db_audit()                       # ① DB별·통합 재고 (.atr 만, 수 분)
#    build_multi(dbs=("mitdb","svdb"))  # ② 통합 npz 생성
#
#  자기검증: python ecg_multidb.py --selftest   (svdb_labels.py 를 자동 로드)
# =============================================================================
import os
import numpy as np

_BASE  = globals().get("_BASE", "/content/drive/MyDrive/mitbih")
_FS_DST = 360
_L, _RPRE = 300, 100

DB_SPEC = {
    "mitdb":    dict(name="MIT-BIH Arrhythmia", pid0=0,    note="F·페이스박·리듬주석 풍부"),
    "svdb":     dict(name="MIT-BIH SVDB",       pid0=1000, note="S 가 풍부(12,196)"),
    "incartdb": dict(name="St.Petersburg INCART", pid0=2000, note="V 가 풍부(20,006)"),
}

# ─────────────────────────────────────────────────────────────────────────────
#  2층(리듬·질환축) 전용 DB 명세 — ★신호(.dat) 를 받지 않는다
#
#  왜 따로 두는가: 1층(비트 N/S/V/F/Q)은 **감사된 비트 라벨**이 필요해 mitdb·svdb·
#  incartdb 로 제한된다. 2층(AFIB/AFL/…)은 **R위치 + 리듬 라벨**만 있으면 되고,
#  그 조건을 만족하는 DB 가 훨씬 많다. 두 층의 가용 DB 집합이 다르다는 것이
#  "하나의 다중클래스 softmax" 가 아니라 **층으로 나눠야 하는 실질적 이유**다.
#
#  ★.dat 를 안 받는 것이 핵심 실용 이득. 신호 용량(WFDB format 212 = 1.5 B/표본):
#      afdb   250Hz×2리드×10h  = 27 MB/레코드 × 23 ≈ 620 MB
#      ltafdb 128Hz×2리드×24h  = 33 MB/레코드 × 84 ≈ 2.8 GB
#      mitdb  360Hz×2리드×30m  =  2 MB/레코드 × 48 ≈  95 MB
#    주석(.atr/.qrs)만 받으면 전부 합쳐 수십 MB다.
#    (초안에 'afdb ~15GB' 라고 적었던 것은 과대 추정이었다 — 실제는 ~620MB.)
#    형태 축이 필요하면 §5 build_atrial_feats 가 레코드 하나씩 받아 특징만 남기고
#    신호를 버린다 → 최종 파일 1MB 미만.
#
#  ★afdb 주의: 비트 주석(.qrs)은 **자동검출·미감사**다. R위치로는 쓸 수 있지만
#    AAMI 비트 클래스로는 절대 쓰면 안 된다 → y5 = -1(미상)로 박아 둔다.
# ─────────────────────────────────────────────────────────────────────────────
RRDB_SPEC = {
    "afdb":     dict(name="MIT-BIH AF (AFDB)", pid0=3000, fs=250,
                     beat_ext="qrs", rhy_ext="atr", beat_audited=False,
                     extra_recs=("00735", "03665"),
                     note="AFIB/AFL/J/N 전량 라벨. AF 검출의 사실상 표준 벤치마크"),
    "ltafdb":   dict(name="Long-Term AF (LTAFDB)", pid0=4000, fs=128,
                     beat_ext="atr", rhy_ext="atr", beat_audited=False,
                     note="84레코드 24~25시간. 지속·발작 혼재 → burden 평가의 핵심"),
    "nsrdb":    dict(name="MIT-BIH Normal Sinus", pid0=5000, fs=128,
                     beat_ext="atr", rhy_ext="atr", beat_audited=True,
                     default_rhythm="N",
                     note="정상동조율 18명. 리듬 주석이 없어 N 으로 가정(음성대조 전용)"),
    "mitdb":    dict(name="MIT-BIH Arrhythmia", pid0=0, fs=360,
                     beat_ext="atr", rhy_ext="atr", beat_audited=True,
                     note="리듬 주석 보유. 1층·2층 공통"),
    "svdb":     dict(name="MIT-BIH SVDB", pid0=1000, fs=128,
                     beat_ext="atr", rhy_ext="atr", beat_audited=True,
                     note="리듬 주석 1/78 레코드뿐 — 2층 기여 거의 없음"),
    "incartdb": dict(name="St.Petersburg INCART", pid0=2000, fs=257,
                     beat_ext="atr", rhy_ext="atr", beat_audited=True,
                     note="리듬 주석 없음 — 2층 기여 없음"),
}


def _cache_dir(db, ann_only, dldir=None):
    """다운로드 캐시 위치를 정한다.

    ★기본을 Drive 로 두는 이유: `/content` 는 **런타임 컨테이너의 임시 디스크**다.
      세션이 끊기면 통째로 사라져서 같은 파일을 매번 다시 받게 된다. 지금까지
      build_multi 가 `/content/{db}_raw` 를 써서 정확히 그 일이 벌어졌다.

    ★그런데 신호(.dat)까지 받는 경로는 Drive 로 옮기면 안 된다: incartdb 원신호만
      ~2GB 라 Drive 용량을 조용히 잡아먹는다. 그래서 갈라 놓는다.
        주석만(2층 RR 코퍼스, 전부 합쳐 ~60MB) → Drive 캐시  ← 이득이 명확
        신호까지(1층 build_multi, ~수 GB)      → /content (원하면 dldir 로 지정)
    """
    if dldir:
        return dldir
    return f"{_BASE}/raw_ann/{db}" if ann_only else f"/content/{db}_raw"


def rate_correct_audit(atrial=None, corpus=None, W=128, stride=None, min_win=5,
                       exps=(1 / 3, 1 / 2, 2 / 3, 1.0), targets=("rt_med", "pr_med"),
                       verbose=True):
    """★심박수 보정 후에도 rt_med·pr_med 가 판별력을 갖는지 (§12.7 의 열린 고리).

    ── 문제 ────────────────────────────────────────────────────────────────
    rt_med(R→T 정점 시간)·pr_med 는 **절대 시간**이라 심박수가 빨라지면 그냥
    짧아진다. 그런데 심박수는 이미 RR 축이 전부 갖고 있다. 그래서 보정 없이 쓰면
    형태축의 기여가 아니라 **심박수를 두 번 세는 것**일 수 있다. §12.7 에서
    `rt_med` 에 '⚠심박수 교란 — 점검 후 판단' 을 달고 미뤄 둔 검사가 이것이다.

    ── 보정식 ──────────────────────────────────────────────────────────────
    임상의 QT 보정과 같은 형태를 쓴다:  x_c = x / RR**α
        α=1/2  Bazett      α=1/3  Fridericia      α=2/3  (더 강한 보정)
        α=1.0  완전 비율화(심박 주기의 몇 %인가)
    ★그런데 α 를 고르는 것 자체가 가정이다. 그래서 **데이터에서 추정한 α** 도 함께
      본다: 정상동조율(N) 창에서 log(x) 를 log(RR) 에 회귀한 기울기가 곧 이 표본의
      α 다(N 만 쓰는 이유: 부정맥 창에서는 RR 자체가 리듬의 신호라 기울기가 오염된다).
      추정 α 로 보정하면 잔여 상관이 **정의상** 0 에 가까워야 하고, 그게 맞는지도 검산한다.

    ── 판정 논리 (이게 요점) ───────────────────────────────────────────────
    보정 뒤에 잔여 상관 |ρ| 는 내려가야 한다. 그 다음이 진짜 질문이다:
      · 판별 AUC 가 **유지되면** → 그 특징에는 심박수와 **독립인 형태 정보**가 있다(채택)
      · 판별 AUC 가 **사라지면** → 원래 판별력은 심박수였다(형태축 기여로 세지 말 것)
    즉 보정은 특징을 '개선'하는 작업이 아니라 **정체를 밝히는 검사**다.
    """
    g = globals()
    win_starts = g["win_starts"]
    stride = int(stride or W)
    a = np.load(atrial or f"{_BASE}/afib_atrial.npz", allow_pickle=True)
    d = np.load(corpus or f"{_BASE}/afib_rr.npz", allow_pickle=True)
    names = [str(x) for x in a["names"]]
    K = {(int(p), int(s)): i for i, (p, s) in enumerate(a["key"])}
    rn = [str(x) for x in d["rhythm_names"]]
    pid, rhy, pre = d["pid"], d["rhythm"], d["pre_rr"]
    # ★한 번 정렬해 환자 경계를 구한다. for p: flatnonzero(pid == p) 는 환자마다
    #   12M 원소를 전부 훑어(불리언 12MB 할당) 157번 반복한다 — 느리고 RAM 을 튀게
    #   한다. 코퍼스는 이미 (환자, 시간) 순이므로 경계만 찾으면 슬라이스로 끝난다.
    order = np.argsort(pid, kind="stable")
    ps_sorted = pid[order]
    bnd = np.flatnonzero(np.diff(ps_sorted)) + 1
    groups = list(zip(np.r_[0, bnd], np.r_[bnd, len(ps_sorted)]))
    FEAT = a["feat"]
    lab, feat, who, rrw = [], [], [], []
    for g0, g1 in groups:
        idx = order[g0:g1]
        p = int(ps_sorted[g0])
        rhy_p = rhy[idx]; pre_p = pre[idx]
        for s in win_starts(len(idx), W, stride):
            j = K.get((p, int(s)))
            if j is None:
                continue
            u, c = np.unique(rhy_p[s:s + W], return_counts=True)
            k = int(np.argmax(c))
            if c[k] / W < 0.90:
                continue
            lab.append(rn[u[k]]); feat.append(FEAT[j]); who.append(p)
            rrw.append(float(np.median(pre_p[s:s + W])) / 360.0)
    lab = np.array(lab); feat = np.array(feat); who = np.array(who)
    rrw = np.array(rrw)
    from scipy.stats import spearmanr

    print(f"\n=== 심박수 보정 감사  창 {len(lab):,} / 환자 {len(np.unique(who))} ===")
    print(f"  보정식  x_c = x / RR^α   (RR = 창 중앙 RR, 초)")

    def _pauc(v, A, B, band=None):
        """환자단위 AUC — (환자,리듬) 중앙값을 표본 1개로 센다(창 많은 환자 방지).
           band=(lo,hi) 를 주면 창 중앙 RR 이 그 구간인 창만 쓴다(심박수 맞춤)."""
        xs, ys = [], []
        for nm, pos in ((A, 1), (B, 0)):
            for p in np.unique(who[lab == nm]):
                m = (lab == nm) & (who == p)
                if band is not None:
                    m = m & (rrw >= band[0]) & (rrw <= band[1])
                if m.sum() >= min_win and np.isfinite(v[m]).any():
                    xs.append(float(np.nanmedian(v[m]))); ys.append(pos)
        xs, ys = np.array(xs), np.array(ys, bool)
        return _auc_rank(xs, ys), int(ys.sum()), int((~ys).sum())

    def _auc_matched(v, A, B, bin_w=0.06, min_pat=3):
        """★심박수를 **좁은 구간으로 층화**해 낸 AUC — 이 감사의 결정적 지표.

        왜 층화인가: 'ρ 가 작다'로는 부족하다(Spearman 은 크기를 안 보므로 무한히
        작은 의존도 ρ=1 을 낼 수 있다). 그리고 겹치는 구간을 10~90 퍼센타일처럼
        넓게 잡으면 그 안에서도 두 리듬의 평균 심박수가 여전히 다르므로, **순수
        심박수 특징이 통과해 버린다**(합성 검증에서 실제로 통과했다).
        그래서 RR 을 {bin_w}초 폭 구간으로 잘라 **구간 안에서** AUC 를 내고, 양쪽
        모두 환자 {min_pat}명 이상인 구간만 써서 가중평균한다. 구간 안에서는 심박수가
        사실상 같으므로, 거기서도 갈린다면 그것은 심박수가 아니다.

        판정 가능한 구간이 없으면 nan → '판정 불가'. 겹침이 없다는 사실 자체가
        정직한 답이고, 비맞춤 AUC 로 되돌아가면 결론이 조용히 위조된다.
        """
        ra, rb = rrw[lab == A], rrw[lab == B]
        if len(ra) < min_win or len(rb) < min_win:
            return float("nan"), 0
        lo = max(ra.min(), rb.min()); hi = min(ra.max(), rb.max())
        if not (hi > lo):
            return float("nan"), 0
        edges = np.arange(lo, hi + bin_w, bin_w)
        num = den = 0.0; nbin = 0
        for i in range(len(edges) - 1):
            b0, b1 = edges[i], edges[i + 1]
            xs, ys = [], []
            for nm, pos in ((A, 1), (B, 0)):
                for p in np.unique(who[lab == nm]):
                    m = (lab == nm) & (who == p) & (rrw >= b0) & (rrw < b1)
                    if m.sum() >= 1 and np.isfinite(v[m]).any():
                        xs.append(float(np.nanmedian(v[m]))); ys.append(pos)
            xs, ys = np.array(xs), np.array(ys, bool)
            na, nb = int(ys.sum()), int((~ys).sum())
            if na < min_pat or nb < min_pat:
                continue
            a_ = _auc_rank(xs, ys)
            if np.isfinite(a_):
                wgt = min(na, nb)
                num += wgt * a_; den += wgt; nbin += 1
        # ★맞춤 표본이 너무 적으면 AUC 는 잡음이다. 구간 1개 × 환자 3명으로 나온
        #   0.667 을 '판별력' 으로 읽으면 안 된다(합성 검증에서 그렇게 오판했다).
        #   MDE 논리와 같다 — 표본이 없으면 '판정 불가' 라고 말한다.
        if nbin < 2 or den < 12:
            return float("nan"), nbin
        return (num / den if den else float("nan")), nbin

    out = {}
    for tname in targets:
        if tname not in names:
            print(f"  · {tname}: 특징에 없음 — 건너뜀"); continue
        x = feat[:, names.index(tname)].astype("float64")
        okm = np.isfinite(x) & np.isfinite(rrw) & (rrw > 0)
        # ★α 를 N 창에서 추정 (부정맥 창은 RR 자체가 리듬 신호라 제외)
        nm_ = okm & (lab == "N") & (x > 0)
        a_fit = float("nan")
        if nm_.sum() >= 50:
            a_fit = float(np.polyfit(np.log(rrw[nm_]), np.log(x[nm_]), 1)[0])
        cand = list(exps) + ([a_fit] if np.isfinite(a_fit) else [])
        tags = [f"α={e:.3f}" for e in exps] + ([f"α={a_fit:.3f}(추정)"]
                                               if np.isfinite(a_fit) else [])
        head = f"\n  ── {tname} ──"
        if np.isfinite(a_fit):
            head += f"   N 창에서 추정한 α = {a_fit:.3f}"
        else:
            head += "   (N 창이 50개 미만이라 α 추정 불가)"
        print(head)
        print(f"    {'보정':<16}{'ρ|N':>7}{'전체 환자AUC':>24} |"
              f"{'★심박수 맞춘 AUC':>24}   판정")
        print(f"    {'':<16}{'':>7}{'AFIB/N  AFL/AFIB   AFL/N':>24} |"
              f"{'AFIB/N  AFL/AFIB   AFL/N':>24}")
        print(f"    (★오른쪽 = 두 리듬의 창 중앙 RR 이 **겹치는 구간**의 창만 써서 낸 AUC."
              f"\n     ρ 는 크기를 안 보므로 이것이 결정적 검사다.)")
        rows = []
        for tag, e in [("보정 없음(α=0)", 0.0)] + list(zip(tags, cand)):
            v = np.where(okm, x / np.power(np.where(rrw > 0, rrw, 1.0), e), np.nan)
            m2 = np.isfinite(v)
            # ★교란 ρ 는 **리듬 안에서** 재야 한다 ─────────────────────────
            #   리듬이 심박수를 정하므로(AFIB 빠름·N 느림), 리듬을 잘 가르는 특징은
            #   무엇이든 RR 과 상관이 생긴다. 그래서 '주변(marginal) ρ' 로 교란을
            #   판정하면 **좋은 판별자를 심박수 대리로 오판한다** — 합성 검증에서
            #   판별 AUC 1.000 인 순수 형태 특징이 ρ=0.49 로 그렇게 오판됐다.
            #   N 창 안에서는 심박수 변동이 리듬이 아니라 생리적 변동이므로,
            #   N 안의 ρ 가 우리가 원하는 '심박수 의존성' 이다.
            #   (§12.7 의 rt_med '⚠심박수 교란' 판정도 주변 ρ 로 내린 것이라
            #    같은 결함을 갖는다 — 이 감사가 그것을 다시 판정한다.)
            mn = m2 & (lab == "N")
            rho_n = (spearmanr(v[mn], rrw[mn]).statistic if mn.sum() > 20
                     else float("nan"))
            rho_n = abs(float(rho_n)) if np.isfinite(rho_n) else float("nan")
            rho_m = (spearmanr(v[m2], rrw[m2]).statistic if m2.sum() > 20
                     else float("nan"))
            rho_m = abs(float(rho_m)) if np.isfinite(rho_m) else float("nan")
            PAIRS = (("AFIB", "N"), ("AFL", "AFIB"), ("AFL", "N"))
            au = [_pauc(v, A, B)[0] for A, B in PAIRS]
            # ★겹침이 없으면 nan 이어야 한다. band=None 을 그대로 넘기면
            #   _pauc 가 '맞춤 안 함'으로 해석해 **비맞춤 AUC 를 돌려준다** —
            #   '심박수를 맞춰도 갈린다'는 결론이 조용히 위조된다(합성 검증이 잡았다).
            mres = [_auc_matched(v, A, B) for A, B in PAIRS]
            aum = [r_[0] for r_ in mres]; nbins = [r_[1] for r_ in mres]
            dmax = max((abs(u - 0.5) for u in au if np.isfinite(u)), default=float("nan"))
            dmm = max((abs(u - 0.5) for u in aum if np.isfinite(u)), default=float("nan"))
            # ★보정으로 값이 상수가 되면 AUC 는 부동소수 잡음의 순위일 뿐이다.
            #   합성 검증에서 완전 보정된 특징(정보 0)이 AUC 0.667 로 찍혀
            #   '형태 정보 있음' 이라는 반대 결론이 났다. 정보량을 먼저 본다.
            fv = v[m2]
            spread = (float(np.subtract(*np.percentile(fv, [75, 25])))
                      / max(abs(float(np.median(fv))), 1e-12)) if len(fv) > 4 else 0.0
            if spread < 1e-3:
                verd = "✗정보 소멸 — 보정 후 상수(원래 판별력은 전부 심박수였다)"
                au = aum = [float("nan")] * 3; dmax = dmm = float("nan")
            elif not np.isfinite(dmax):
                verd = "환자 부족"
            elif dmax < 0.10:
                verd = "✗판별력 없음"
            elif not np.isfinite(dmm):
                verd = (f"판정 불가 — 심박수 맞춤 표본 부족(적격 구간 "
                        f"{max(nbins)}개)")
            else:
                # ★이진 판정을 하지 않는다. '심박수를 맞추면 판별력이 얼마나
                #   줄어드는가' 를 비율로 보고한다. 구간 폭(0.06초) 안에 남는
                #   잔여 심박수 기울기 때문에 순수 심박수 특징도 맞춤 AUC 가
                #   정확히 0.5 가 되지는 않는다 — 그래서 어떤 고정 문턱으로
                #   '독립' 을 선언해도 합성 검증에서 오판이 났다. 검증할 수 없는
                #   문턱을 쓰는 대신 숫자를 내놓고 애매하면 애매하다고 말한다.
                red = dmm / dmax if dmax > 0 else float("nan")
                keep_pct = 100 * red
                if red < 0.35:
                    verd = f"✗판별력의 {100-keep_pct:.0f}% 가 심박수 — 형태 기여 미미"
                elif red > 0.75:
                    verd = f"★심박수 맞춰도 {keep_pct:.0f}% 유지 — 독립인 형태 정보"
                else:
                    verd = (f"△부분적 — 심박수 맞추면 판별력 {100-keep_pct:.0f}% 감소"
                            f"(해석 필요)")
            print(f"    {tag:<16}{rho_n:>7.3f}" +
                  "".join(f"{u:>8.3f}" if np.isfinite(u) else f"{'—':>8}"
                          for u in au) + " |" +
                  "".join(f"{u:>8.3f}" if np.isfinite(u) else f"{'—':>8}"
                          for u in aum) + f"   {verd}")
            rows.append(dict(tag=tag, exp=e, rho=rho_n, rho_marg=rho_m, auc=au,
                             auc_matched=aum, nbins=nbins, spread=spread,
                             verdict=verd))
        out[tname] = dict(a_fit=a_fit, rows=rows)
        # 검산: 추정 α 로 보정하면 잔여 상관이 거의 0 이어야 한다
        if np.isfinite(a_fit):
            r_fit = [r for r in rows if "추정" in r["tag"]
                     and "소멸" not in r["verdict"]]
            if r_fit and r_fit[0]["rho"] > 0.25:
                print(f"    ⚠ 추정 α 로 보정했는데 잔여 |ρ|={r_fit[0]['rho']:.3f} 다."
                      f" 관계가 로그선형이 아니거나")
                print(f"      N 창의 심박수 범위가 좁아 기울기가 불안정하다는 뜻이다.")
    print(f"\n  ※ 보정은 특징을 '개선'하는 작업이 아니라 **정체를 밝히는 검사**다.")
    print(f"    보정 뒤 판별력이 사라지면 그 특징의 원래 판별력은 심박수였고,")
    print(f"    남으면 심박수와 독립인 형태 정보가 있다는 뜻이다.")
    return out


def cache_status(base=None, verbose=True):
    """지금 Drive 에 무엇이 이미 있는지 보여 준다 — "또 받아야 하나?" 에 대한 답.

    파생 npz(한 번 만들면 끝)와 원본 주석 캐시(DB별)를 나눠서 센다.
    """
    b = base or _BASE
    print(f"\n=== Drive 캐시 현황  {b} ===")
    print("  ── 만들어진 데이터셋(다시 안 만들어도 됨) ──")
    for fn, what in [("svdb_data.npz", "1층 SVDB 원본"),
                     ("svdb_data5.npz", "1층 SVDB 5-class"),
                     ("ecg_multi.npz", "1층 통합(mitdb+svdb+incartdb)"),
                     ("afib_rr.npz", "2층 RR 코퍼스"),
                     ("afib_atrial.npz", "2층-B 심방활동·P-QRS-T 특징")]:
        p = f"{b}/{fn}"
        if os.path.exists(p):
            print(f"    ✔ {fn:<18} {os.path.getsize(p)/1e6:>8.1f} MB  {what}")
        else:
            print(f"    · {fn:<18} {'—':>8}     {what} (아직 없음)")
    # ★심방특징 조각 — "런타임이 죽었는데 어디까지 됐나"에 대한 답
    pr = f"{b}/atrial_parts"
    if os.path.isdir(pr):
        fs = [f for f in os.listdir(pr) if f.endswith(".npz")]
        per = {}
        for f in fs:
            per[f.split("_", 1)[0]] = per.get(f.split("_", 1)[0], 0) + 1
        mb = sum(os.path.getsize(f"{pr}/{f}") for f in fs) / 1e6
        print(f"  ── 심방특징 조각(레코드별, 이어하기용) ──")
        print(f"    ✔ 레코드 {len(fs)}개 계산 완료  {mb:.1f} MB  "
              f"{ {k: v for k, v in sorted(per.items())} }")
        print(f"    → build_atrial_feats(...) 를 다시 부르면 나머지만 계산합니다.")
    print("  ── 원본 주석 캐시(있으면 다운로드를 건너뜀) ──")
    root = f"{b}/raw_ann"
    if not os.path.isdir(root):
        print(f"    · {root} 없음 — 첫 실행에서 만들어집니다")
        return
    for db in sorted(os.listdir(root)):
        d = f"{root}/{db}"
        if not os.path.isdir(d):
            continue
        fs = os.listdir(d)
        mb = sum(os.path.getsize(f"{d}/{f}") for f in fs) / 1e6
        print(f"    ✔ {db:<12} 파일 {len(fs):>4}개  {mb:>7.1f} MB")


def _need(name):
    """svdb_labels.py 에서 오는 심볼을 빌려 쓴다(중복 정의하지 않는다)."""
    g = globals()
    if name not in g:
        raise RuntimeError(f"'{name}' 없음 — svdb_labels.py 를 먼저 exec 하세요 "
                           f"(colab_setup.sync() 가 함께 로드합니다).")
    return g[name]


# ─────────────────────────────────────────────────────────────────────────────
#  1. INCART 레코드 → 환자 묶기  (PAPER §6.5 L3)
# ─────────────────────────────────────────────────────────────────────────────
def incart_groups(dldir=None, verbose=True):
    """INCART 75레코드를 32환자로 묶는 **휴리스틱**.

    ★문제: INCART 는 75레코드가 32환자에서 나왔다. 레코드를 환자로 세면
      GroupKFold 가 같은 환자를 학습·테스트에 동시에 넣어 **환자분리가 깨진다**.
      PAPER §6.5 가 L3 로 '미해결'이라 기록해 둔 바로 그 문제다.

    ★해법(휴리스틱): .hea 주석의 (나이, 성별, 진단) 문자열이 같은 레코드를 한 환자로
      묶는다. 공식 매핑이 아니므로 **완벽하지 않다** — 같은 나이·성별·진단인 다른
      환자가 합쳐질 수 있다(보수적 방향: 환자 수를 과소평가 → 검정력을 낮게 잡음).
      과대평가(누설)보다 과소평가가 안전하므로 이 방향을 택한다.
      공식 매핑이 생기면 patient_map 인자로 덮어쓸 것.
    """
    _ensure = _need("_ensure"); _ensure("wfdb")
    import wfdb
    dldir = _cache_dir("incartdb", ann_only=True, dldir=dldir)  # .hea 만 → Drive 캐시
    os.makedirs(dldir, exist_ok=True)
    try:
        recs = wfdb.get_record_list("incartdb")
    except Exception:
        recs = [f"I{i:02d}" for i in range(1, 76)]
    key2pid, out = {}, {}
    for rec in recs:
        try:
            for ext in ("hea",):
                fp = f"{dldir}/{rec}.{ext}"
                if not (os.path.exists(fp) and os.path.getsize(fp) > 0):
                    wfdb.dl_files("incartdb", dldir, [f"{rec}.{ext}"])
            h = wfdb.rdheader(f"{dldir}/{rec}")
            key = " | ".join(str(c).strip() for c in (h.comments or []))
        except Exception as e:
            key = f"__fail_{rec}"
            if verbose:
                print(f"  ⚠ {rec} 헤더 실패({type(e).__name__}) → 단독 환자로 취급")
        if key not in key2pid:
            key2pid[key] = len(key2pid)
        out[rec] = key2pid[key]
    if verbose:
        print(f"  INCART: {len(out)}레코드 → {len(key2pid)}환자 (헤더 (나이·성별·진단) 기준)")
        if len(key2pid) > 40:
            print(f"    ⚠ 32명보다 많다 — 헤더가 환자를 잘 구분 못 하는 것일 수 있다.")
        print(f"    ⚠ 휴리스틱이다. 과소추정(환자 합쳐짐)은 안전하나 과대추정은 누설이다.")
    return out


# ─────────────────────────────────────────────────────────────────────────────
#  2. 다중 DB 재고조사
# ─────────────────────────────────────────────────────────────────────────────
def db_audit(dbs=("mitdb", "svdb", "incartdb"), n_rec=None, target=0.99, verbose=True):
    """DB 별로 재고조사하고 **통합 시** 클래스·리듬별 검정력을 계산한다."""
    label_audit = _need("label_audit"); AAMI5 = _need("AAMI5"); CLS5 = _need("CLS5")
    n_for = _need("n_for_halfwidth"); pw = _need("power_for_accuracy")
    per, sym_all, rhy_all, rhyrec_all, symrec_all = {}, {}, {}, {}, {}
    for db in dbs:
        print(f"\n{'='*66}\n▶ {db}  ({DB_SPEC.get(db,{}).get('name',db)})\n{'='*66}")
        try:
            r = label_audit(db=db, n_rec=n_rec, target=target, verbose=verbose)
        except Exception as e:
            print(f"  ✗ {db} 실패: {type(e).__name__}: {e}"); continue
        per[db] = r
        for s, c in r["sym_counts"].items():
            sym_all[s] = sym_all.get(s, 0) + c
        for s, v in (r.get("sym_records") or {}).items():
            symrec_all.setdefault(s, set()).update(f"{db}:{x}" for x in v)
        for k, c in r["rhy_counts"].items():
            rhy_all[k] = rhy_all.get(k, 0) + c
            rhyrec_all.setdefault(k, set()).update(
                f"{db}:{x}" for x in r["rhy_records"].get(k, []))
    if not per:
        return {}

    print(f"\n{'='*66}\n▶ 통합 ({'+'.join(per)})\n{'='*66}")
    agg = {}
    for s, c in sym_all.items():
        a = AAMI5.get(s)
        if a is not None:
            agg[a] = agg.get(a, 0) + c
    need = n_for(0.01, target)
    recs_of = {}
    for s, v in symrec_all.items():
        a = AAMI5.get(s)
        if a is not None:
            recs_of.setdefault(a, set()).update(v)
    print(f"=== AAMI 5-class 통합 분포 ===")
    print(f"  {'클래스':<5}{'통합비트':>11}{'레코드':>7}  " + "".join(f"{d:>11}" for d in per)
          + "   판정(비트/레코드)")
    for a in range(5):
        row = [sum(c for s, c in per[d]["sym_counts"].items() if AAMI5.get(s) == a) for d in per]
        tot = agg.get(a, 0); nr = len(recs_of.get(a, ()))
        m1 = "✓" if tot >= need else "✗"
        m2 = "✓" if nr >= 8 else ("△" if nr >= 4 else "✗")
        print(f"  {CLS5[a]:<5}{tot:>11,}{nr:>7}  " + "".join(f"{v:>11,}" for v in row)
              + f"      {m1} / {m2}")
    print(f"  ※ 비트 {need:,}개 이상이면 ✓. ★레코드는 8명 이상 ✓ / 4~7명 △ / 3명 이하 ✗")
    print(f"     ★★비트가 충분해도 레코드가 적으면 환자단위 매크로 평가가 성립하지 않는다.")
    for a in range(5):
        tot = agg.get(a, 0); nr = len(recs_of.get(a, ()))
        if tot >= need and nr < 8:
            print(f"    ⚠ {CLS5[a]}: 비트 {tot:,}개는 충분하나 **레코드 {nr}개뿐** —"
                  f" 환자단위로는 검정 불가")
    for a in range(5):
        tot = agg.get(a, 0)
        if 0 < tot < need:
            print(f"    ⚠ {CLS5[a]}: 통합해도 {tot:,}개 — 여전히 부족하다")

    print(f"\n=== 리듬(질병) 라벨 통합 ===")
    print(f"  {'리듬':<12}{'비트수':>12}{'레코드':>8}   {target:.0%} 주장 시 CI   환자분리 평가")
    for k, c in sorted(rhy_all.items(), key=lambda kv: -kv[1]):
        nr = len(rhyrec_all.get(k, ()))
        h = pw(c, target)
        # 환자분리 평가는 '그 리듬을 가진 레코드 수'가 유효표본이다(HANDOFF §2)
        ok = "가능" if nr >= 8 else ("한계적" if nr >= 4 else "불가(레코드 부족)")
        print(f"  {k:<12}{c:>12,}{nr:>8}   ±{100*h:>7.2f}%      {ok}")
    print(f"  ※ 비트 수가 많아도 **레코드 수**가 적으면 환자분리 평가가 안 된다.")
    print(f"     같은 환자의 같은 에피소드를 반복 세는 것이라 독립 표본이 아니기 때문이다.")
    return dict(per_db=per, sym=sym_all, agg=agg, rhythm=rhy_all,
                class_records={CLS5[a]: sorted(v) for a, v in recs_of.items()},
                rhythm_records={k: sorted(v) for k, v in rhyrec_all.items()})


# ─────────────────────────────────────────────────────────────────────────────
#  3. 통합 데이터셋 생성
# ─────────────────────────────────────────────────────────────────────────────
def build_multi(dbs=("mitdb", "svdb", "incartdb"), out=None, n_rec=None,
                realign=True, patient_map=None, raw_dir=None, verbose=True):
    """여러 DB 를 하나의 npz 로. 환자 ID 는 **전역 유일**하게 재배정한다.

    저장 키
      beat[N,2,300] y5(0..4) y3(3-class, F/Q=-1) sym pid(전역) db(출처)
      rhythm(리듬 id) rhythm_names  pre_rr post_rr(★비트 주석만) rr_edge

    ★환자 ID 가 전역 유일해야 하는 이유: GroupKFold 가 pid 로 분할하는데 DB 마다
      0부터 시작하면 서로 다른 환자가 같은 그룹으로 묶여 **환자분리가 깨진다**.
      DB_SPEC 의 pid0 오프셋으로 겹치지 않게 한다.
    """
    _ensure = _need("_ensure"); _ensure("wfdb")
    import wfdb
    from scipy.signal import resample_poly
    AAMI5 = _need("AAMI5"); BEAT_SYMS = _need("BEAT_SYMS")
    beat_only_rr = _need("beat_only_rr"); rhythm_per_beat = _need("rhythm_per_beat")
    CLS5 = _need("CLS5")

    BEAT = []; Y5 = []; SYM = []; PID = []; DB = []; PRE = []; POST = []
    RHY = []; EDGE = []
    rnames = {}
    pmap = dict(patient_map or {})
    if "incartdb" in dbs and not any(k.startswith("I") for k in pmap):
        pmap.update({k: v for k, v in incart_groups(verbose=verbose).items()})

    for db in dbs:
        off = DB_SPEC.get(db, {}).get("pid0", 0)
        dldir = _cache_dir(db, ann_only=False, dldir=raw_dir)
        os.makedirs(dldir, exist_ok=True)
        try:
            recs = wfdb.get_record_list(db)
        except Exception:
            print(f"  ✗ {db}: 레코드 목록 실패"); continue
        if n_rec:
            recs = recs[:n_rec]
        rec2pid = {}
        print(f"\n▶ {db}: {len(recs)}레코드")
        for ri, rec in enumerate(recs):
            try:
                for ext in ("hea", "dat", "atr"):
                    fp = f"{dldir}/{rec}.{ext}"
                    if os.path.exists(fp) and os.path.getsize(fp) > 0:
                        continue
                    for _ in range(3):
                        try:
                            wfdb.dl_files(db, dldir, [f"{rec}.{ext}"]); break
                        except Exception:
                            pass
                r = wfdb.rdrecord(f"{dldir}/{rec}"); ann = wfdb.rdann(f"{dldir}/{rec}", "atr")
            except Exception as e:
                print(f"  ✗ {rec}: {type(e).__name__}"); continue
            if r.p_signal is None or r.p_signal.shape[1] < 2:
                print(f"  ✗ {rec}: 2리드 미만"); continue
            fs = int(getattr(r, "fs", _FS_DST))
            sig = r.p_signal[:, :2].T
            if fs != _FS_DST:
                sig = np.stack([resample_poly(sig[c], _FS_DST, fs) for c in range(2)])
            scale = _FS_DST / fs
            samp = (np.asarray(ann.sample) * scale).astype(int)
            sym = list(ann.symbol)
            aux = list(getattr(ann, "aux_note", []) or [None] * len(sym))
            T = sig.shape[1]
            bmask = np.array([s in BEAT_SYMS for s in sym])
            if not bmask.any():
                continue
            bsamp = samp[bmask]; bsym = np.array(sym)[bmask]
            if realign:
                w = int(_FS_DST * 50 / 1000.0); new = []
                for s0 in bsamp:
                    a0, b0 = max(0, s0 - w), min(T, s0 + w + 1)
                    if b0 - a0 < 3:
                        new.append(s0); continue
                    vm = np.sqrt(sig[0, a0:b0] ** 2 + sig[1, a0:b0] ** 2)
                    new.append(a0 + int(np.argmax(vm)))
                bsamp = np.array(new)
            pre, post, edge = beat_only_rr(bsamp)
            rp = rhythm_per_beat(samp, sym, aux, bsamp)
            # 환자 ID: INCART 는 매핑, 나머지는 레코드=환자
            key = pmap.get(rec, None)
            if key is None:
                rec2pid.setdefault(rec, len(rec2pid)); key = rec2pid[rec]
            gpid = off + int(key)
            for i in range(len(bsamp)):
                lab = AAMI5.get(bsym[i])
                if lab is None:
                    continue
                R0 = int(bsamp[i]); a1, b1 = R0 - _RPRE, R0 - _RPRE + _L
                if a1 < 0 or b1 > T:
                    continue
                seg = sig[:, a1:b1].astype("float32")
                seg = (seg - seg.mean(1, keepdims=True)) / (seg.std(1, keepdims=True) + 1e-6)
                nm = rp[i] or "(미상)"
                if nm not in rnames:
                    rnames[nm] = len(rnames)
                BEAT.append(seg); Y5.append(lab); SYM.append(str(bsym[i]))
                PID.append(gpid); DB.append(db); PRE.append(pre[i]); POST.append(post[i])
                RHY.append(rnames[nm]); EDGE.append(edge[i])
            if verbose and ((ri + 1) % 20 == 0 or ri == len(recs) - 1):
                print(f"    {ri+1}/{len(recs)}  누적 {len(BEAT):,}")

    if not BEAT:
        raise RuntimeError("비트가 하나도 수집되지 않았습니다.")
    BEAT = np.stack(BEAT); Y5 = np.array(Y5, np.int64); PID = np.array(PID, np.int64)
    Y3 = np.where(Y5 <= 2, Y5, -1).astype(np.int64)
    inv = [None] * len(rnames)
    for k, v in rnames.items():
        inv[v] = k
    out = out or f"{_BASE}/ecg_multi.npz"
    np.savez(out, beat=BEAT, y5=Y5, y3=Y3, y=Y3, pid=PID, db=np.array(DB),
             sym=np.array(SYM), pre_rr=np.array(PRE, "float32"),
             post_rr=np.array(POST, "float32"), rhythm=np.array(RHY, np.int64),
             rhythm_names=np.array(inv), rr_edge=np.array(EDGE, bool))
    print(f"\n✔ 저장 {out}   비트 {len(Y5):,}  환자 {len(np.unique(PID))}")
    for c in range(5):
        k = int((Y5 == c).sum())
        print(f"    {CLS5[c]} {k:>9,} ({100*k/len(Y5):5.2f}%)")
    dbu, dbc = np.unique(np.array(DB), return_counts=True)
    print(f"  출처: " + "  ".join(f"{d}={c:,}" for d, c in zip(dbu, dbc)))
    print(f"  리듬 {len(inv)}종: {inv[:12]}{' ...' if len(inv)>12 else ''}")
    print(f"  ★pid 는 전역 유일(DB별 오프셋) — GroupKFold 환자분리가 DB 를 넘어 유효")
    print(f"  ★RR 은 비트 주석만으로 계산 — 비-비트 주석 오염 없음")
    return out


# ─────────────────────────────────────────────────────────────────────────────
#  4. 2층(리듬축) RR 코퍼스 — 주석만 받아서 만든다
# ─────────────────────────────────────────────────────────────────────────────
def _rr_records(db, dldir, exts, verbose=True):
    """레코드 목록 + 필요한 주석 확장자만 내려받는다(.dat 는 받지 않는다)."""
    _ensure = _need("_ensure"); _ensure("wfdb")
    import wfdb
    spec = RRDB_SPEC[db]
    try:
        recs = list(wfdb.get_record_list(db))
    except Exception:
        print(f"  ✗ {db}: 레코드 목록 실패"); return []
    # RECORDS 에 안 실렸지만 주석만 존재하는 레코드(afdb 00735/03665)
    for r in spec.get("extra_recs", ()):
        if r not in recs:
            recs.append(r)
    os.makedirs(dldir, exist_ok=True)
    got = []; n_hit = 0; n_new = 0
    for rec in recs:
        ok = True
        for ext in exts:
            fp = f"{dldir}/{rec}.{ext}"
            if os.path.exists(fp) and os.path.getsize(fp) > 0:
                n_hit += 1; continue          # ★캐시 적중 — 다시 받지 않는다
            for _ in range(3):
                try:
                    wfdb.dl_files(db, dldir, [f"{rec}.{ext}"]); break
                except Exception:
                    pass
            if os.path.exists(fp) and os.path.getsize(fp) > 0:
                n_new += 1
            else:
                ok = False; break
        if ok:
            got.append(rec)
    if verbose:
        mb = sum(os.path.getsize(f"{dldir}/{f}") for f in os.listdir(dldir)) / 1e6
        print(f"  캐시 {dldir}  ({mb:.1f} MB)  기존 {n_hit}개 재사용 / 새로 {n_new}개")
    if verbose and len(got) != len(recs):
        miss = [r for r in recs if r not in got]
        print(f"  ⚠ {db}: 주석 확보 {len(got)}/{len(recs)}  누락 {miss[:6]}")
    return got


def _rr_one_record(db, rec, dldir):
    """한 레코드 → (t360, rhythm_name_per_beat, sym_per_beat).

    t360 = 비트 위치를 360Hz 샘플로 환산한 값(build_multi 와 같은 규약).
    """
    import wfdb
    spec = RRDB_SPEC[db]
    BEAT_SYMS = _need("BEAT_SYMS"); rhythm_per_beat = _need("rhythm_per_beat")
    hd = wfdb.rdheader(f"{dldir}/{rec}")
    fs = float(getattr(hd, "fs", spec.get("fs", 360)) or spec.get("fs", 360))
    sc = _FS_DST / fs

    ba = wfdb.rdann(f"{dldir}/{rec}", spec["beat_ext"])
    bsym = np.asarray(list(ba.symbol))
    bkeep = np.array([s in BEAT_SYMS for s in bsym])
    if not bkeep.any():
        return None
    bsamp = np.asarray(ba.sample)[bkeep]
    bsym = bsym[bkeep]

    if spec["rhy_ext"] == spec["beat_ext"]:
        ra = ba
    else:
        ra = wfdb.rdann(f"{dldir}/{rec}", spec["rhy_ext"])
    aux = list(getattr(ra, "aux_note", []) or [None] * len(ra.symbol))
    rp = rhythm_per_beat(np.asarray(ra.sample), list(ra.symbol), aux, bsamp)
    dflt = spec.get("default_rhythm")
    rp = [(r or dflt or "(미상)") for r in rp]
    return (np.asarray(bsamp, np.float64) * sc), rp, bsym


def rr_audit_dbs(dbs=("afdb", "ltafdb", "nsrdb", "mitdb"), dldir=None, verbose=True):
    """★2층 진입 전 필수 — 리듬별 '보유 환자 수'와 그로부터 나오는 MDE 를 센다.

    모델을 짜기 전에 이걸 먼저 보는 이유: 리듬 클래스의 검정력은 비트 수가 아니라
    **그 리듬을 가진 환자 수**로 정해진다. AFIB 10명이면 MDE 0.198 이고, 그 상태에서
    나온 F1 0.75 와 0.95 는 구분되지 않는다 — 어떤 모델을 붙여도 해석이 안 된다.
    신호를 안 받으므로 몇 분이면 끝난다.
    """
    tot = {}
    for db in dbs:
        spec = RRDB_SPEC.get(db)
        if spec is None:
            print(f"  ✗ {db}: RRDB_SPEC 에 없음"); continue
        dd = _cache_dir(db, ann_only=True, dldir=dldir)
        exts = sorted({"hea", spec["beat_ext"], spec["rhy_ext"]})
        recs = _rr_records(db, dd, exts, verbose=verbose)
        per = {}
        nbeat = 0
        for rec in recs:
            try:
                got = _rr_one_record(db, rec, dd)
            except Exception as e:
                print(f"  ✗ {db}/{rec}: {type(e).__name__}"); continue
            if got is None:
                continue
            t, rp, _ = got
            nbeat += len(t)
            for nm in set(rp):
                per.setdefault(nm, set()).add(f"{db}:{rec}")
        print(f"\n▶ {spec['name']}  레코드 {len(recs)}  비트 {nbeat:,}")
        if not spec["beat_audited"]:
            print(f"    ⚠ 비트 주석 미감사(.{spec['beat_ext']}) → R위치 전용, AAMI 라벨 금지")
        for nm, s in sorted(per.items(), key=lambda kv: -len(kv[1])):
            print(f"    {nm:<12}{len(s):>4}레코드")
            tot.setdefault(nm, set()).update(s)
    print(f"\n=== 통합 리듬 재고 ===")
    print(f"  {'리듬':<12}{'환자':>6}{'MDE(σ=.32)':>12}{'MDE(σ=.20)':>12}")
    for nm, s in sorted(tot.items(), key=lambda kv: -len(kv[1])):
        n = len(s)
        print(f"  {nm:<12}{n:>6}{1.96*0.32/max(np.sqrt(n),1):>12.3f}"
              f"{1.96*0.20/max(np.sqrt(n),1):>12.3f}")
    print(f"  ※ σ 는 아직 가정이다. 첫 실행 뒤 환자별 F1 의 실측 표준편차로 갱신할 것.")
    return {k: sorted(v) for k, v in tot.items()}


def build_rr_corpus(dbs=("afdb", "ltafdb", "nsrdb", "mitdb"), out=None,
                    dldir=None, n_rec=None, verbose=True):
    """2층용 RR 코퍼스 npz. 신호를 받지 않으므로 작고 빠르다(수십 MB).

    저장 키 (전부 비트 단위 1차원, 길이 N)
      t       비트 시각(초)          — 에피소드·burden 계산의 기준
      pre_rr  직전 RR(360Hz 샘플)    — rr_context 규약과 동일
      post_rr 직후 RR(360Hz 샘플)
      rr_edge 레코드 경계 플래그
      pid     전역 유일 환자 ID      — GroupKFold 가 DB 를 넘어 유효
      db      출처
      rhythm  리듬 id  / rhythm_names
      y5      AAMI 비트 클래스(감사된 DB만, 나머지는 -1)
    """
    AAMI5 = _need("AAMI5"); beat_only_rr = _need("beat_only_rr")
    warn_if_gpu("RR 코퍼스 생성")
    T = []; PRE = []; POST = []; EDGE = []; PID = []; DB = []; RHY = []; Y5 = []
    rnames = {}
    p2rec = {}      # pid → "db:rec". ★2층-B(심방활동)가 신호를 다시 찾으려면 필수
    for db in dbs:
        spec = RRDB_SPEC.get(db)
        if spec is None:
            print(f"  ✗ {db}: RRDB_SPEC 에 없음"); continue
        off = spec["pid0"]
        dd = _cache_dir(db, ann_only=True, dldir=dldir)
        exts = sorted({"hea", spec["beat_ext"], spec["rhy_ext"]})
        recs = _rr_records(db, dd, exts, verbose=verbose)
        if n_rec:
            recs = recs[:n_rec]
        # ★pid 는 레코드 이름의 사전순 위치로 고정한다. enumerate 위치를 쓰면 한
        #   레코드의 다운로드가 실패한 실행과 성공한 실행에서 같은 환자가 다른 ID 를
        #   받아 재현성이 깨진다.
        rec2pid = {r: i for i, r in enumerate(sorted(recs))}
        print(f"\n▶ {spec['name']}: {len(recs)}레코드")
        for ri, rec in enumerate(recs):
            try:
                got = _rr_one_record(db, rec, dd)
            except Exception as e:
                print(f"  ✗ {rec}: {type(e).__name__}"); continue
            if got is None:
                continue
            t360, rp, bsym = got
            pre, post, edge = beat_only_rr(t360)          # 이미 360Hz 환산됨
            gpid = off + rec2pid[rec]
            p2rec[gpid] = f"{db}:{rec}"
            for i in range(len(t360)):
                nm = rp[i]
                if nm not in rnames:
                    rnames[nm] = len(rnames)
                T.append(t360[i] / _FS_DST); PRE.append(pre[i]); POST.append(post[i])
                EDGE.append(edge[i]); PID.append(gpid); DB.append(db)
                RHY.append(rnames[nm])
                Y5.append(AAMI5.get(bsym[i], -1) if spec["beat_audited"] else -1)
            if verbose and ((ri + 1) % 20 == 0 or ri == len(recs) - 1):
                print(f"    {ri+1}/{len(recs)}  누적 {len(T):,}")
    if not T:
        raise RuntimeError("비트가 하나도 수집되지 않았습니다.")
    inv = [None] * len(rnames)
    for k, v in rnames.items():
        inv[v] = k
    out = out or f"{_BASE}/afib_rr.npz"
    np.savez(out, t=np.array(T, "float32"), pre_rr=np.array(PRE, "float32"),
             post_rr=np.array(POST, "float32"), rr_edge=np.array(EDGE, bool),
             pid=np.array(PID, np.int64), db=np.array(DB),
             rhythm=np.array(RHY, np.int64), rhythm_names=np.array(inv),
             y5=np.array(Y5, np.int64),
             pid_uniq=np.array(sorted(p2rec), np.int64),
             pid_rec=np.array([p2rec[k] for k in sorted(p2rec)]))
    mb = os.path.getsize(out) / 1e6
    print(f"\n✔ 저장 {out}  ({mb:.1f} MB)  비트 {len(T):,}  환자 {len(set(PID))}")
    R = np.array(RHY)
    P = np.array(PID)
    print(f"  {'리듬':<12}{'비트':>12}{'환자':>6}{'비율':>8}")
    for i, nm in enumerate(inv):
        m = R == i
        print(f"  {nm:<12}{int(m.sum()):>12,}{len(np.unique(P[m])):>6}"
              f"{100*m.mean():>7.2f}%")
    print(f"  ★신호(.dat)는 받지 않았다 → 형태축은 이 코퍼스로 못 돈다(2층-B 는 mitdb 계열)")
    return out


# ─────────────────────────────────────────────────────────────────────────────
#  5. 2층-B: 심방활동(atrial activity) 축 — RR 이 못 보는 유일한 물리 신호
#
#  ── 왜 이 축인가 (생리로 정해진다, 취향이 아니다) ──────────────────────────
#    리듬      심방 활동                          RR
#    N        뚜렷한 P파, QRS 앞 1:1, 형태 일정    규칙적
#    AFIB     f파 — 무질서, 350~600/분             ★불규칙
#    AFL      F파 — 톱니, 240~340/분, ★규칙적 반복  ★규칙적(2:1·3:1 전도)
#
#  → N vs AFIB 는 RR 만으로 갈린다(실측 F1 0.92, 이미 포화).
#  → **AFL 은 RR 이 N 과 거의 같아 구조적으로 못 갈린다**(실측: RSN 이 A1 보다 낮음).
#    AFL 을 가르는 유일한 신호가 심방 활동이고, 그건 파형에만 있다.
#
#  ── 어떻게 뽑나: QRST 소거 → 잔차 스펙트럼 (Bollmann/Stridh 계열 표준) ─────
#    1) 레코드별 평균 QRST 템플릿을 만들어 박마다 빼면 남는 것이 심방 활동이다
#       (심실 성분이 심방 성분보다 10~50배 커서 빼기 전에는 안 보인다)
#    2) 3~12 Hz 대역통과 — 기저동요와 잔여 T파를 제거
#    3) 창(=128박, 약 100초)마다 Welch PSD → 주파수 분해능 ~0.01 Hz
#       ★박 하나(TQ 0.45초)로 스펙트럼을 보면 분해능이 2.2 Hz 라 AFL(4~5.7Hz)과
#         AFIB(5.8~10Hz)이 안 갈린다. 반드시 창 단위여야 한다.
#
#  ── 저장 전략: 신호를 저장하지 않는다 ──────────────────────────────────────
#    레코드 하나씩 받아 → 특징 계산 → 신호 버림. 결과는 창당 스칼라 8개뿐이라
#    최종 파일이 1 MB 미만이다. (afdb 원신호는 ~620MB 로 Drive 에 두기엔 아깝고,
#    ltafdb 는 ~2.8GB 라 애초에 부담이다.)
#
#  ★창 정의가 afib_bench.make_windows 와 **정확히 같아야** 한다 → 같은 win_starts()
#    를 쓴다. 어긋나면 에러 없이 '다른 창의 특징'이 붙는다.
# ─────────────────────────────────────────────────────────────────────────────
#  심방활동(잔차 스펙트럼) 8종 — AFIB/AFL 의 f·F 파 전용
SPEC_NAMES = ["daf", "sc", "sent", "afl_ratio", "aa_rel", "av_ratio", "av_int",
              "aa_snr", "daf_vh"]
#  P-QRS-T '관계' 11종 — ★원신호에서 잰다(아래 주석의 이유)
PQ_NAMES = ["p_amp", "p_cons", "pr_med", "pr_cv", "t_amp", "rt_med", "rt_cv",
            "tp_rms", "pt_ratio", "pqt_ok", "lead"]
ATR_NAMES = SPEC_NAMES + PQ_NAMES


def _atrial_residual(sig, rpk, fs):
    """QRST 소거 → 심방 잔차. sig[n] 1리드, rpk = R 표본위치.

    평균이 아니라 **중앙값** 템플릿을 쓴다: 이소성 박·잡음 구간이 섞여도 템플릿이
    끌려가지 않는다(평균은 한 번의 큰 잡음에 무너진다).
    """
    a = int(0.25 * fs); b = int(0.45 * fs)          # R 전 250ms ~ 후 450ms = QRST
    ok = rpk[(rpk >= a) & (rpk + b < len(sig))]
    if len(ok) < 8:
        return None
    seg = np.stack([sig[r - a:r + b] for r in ok])
    seg = seg - np.median(seg[:, :int(0.05 * fs)], axis=1, keepdims=True)  # 등전위 정렬
    tpl = np.median(seg, axis=0)
    res = sig.astype("float32").copy()
    for r in ok:                                     # 박마다 템플릿 감산
        res[r - a:r + b] -= tpl
    return res


def _bandpass(x, fs, lo=3.0, hi=12.0):
    from scipy.signal import butter, filtfilt
    ny = 0.5 * fs
    hi = min(hi, ny * 0.95)
    if lo >= hi:
        return x
    b, a = butter(3, [lo / ny, hi / ny], btype="band")
    return filtfilt(b, a, x)


def _spec_win_feats(res, i0, i1, fs, med_rr, qrs_amp):
    """한 창의 **잔차** → 심방활동 스펙트럼 특징 8종. 실패하면 None.

    ★av_ratio 착안(사용자 제안 '1:1:1 비율'의 스펙트럼판):
        av_ratio = 심방 주파수(Hz) × 심실 RR(초) = 심실 1박당 심방 편위 수
      정상 1, AFL 2:1 → 2, 3:1 → 3 처럼 **정수**에 붙는다. AFIB 는 심방이
      무질서해 정수에 안 붙는다 → av_int(가장 가까운 정수까지의 거리)가 커진다.
    ★단 정상동조율에서는 av_ratio 를 믿으면 안 된다(아래 _pqrst_win_feats 주석 참조:
      P 가 템플릿과 함께 지워진다). 그래서 aa_rel(잔차/QRS 진폭)을 같이 준다 —
      aa_rel 이 낮으면 '뚜렷한 비-R고정 심방활동이 없음'이고, 모델이 그 조건부를
      스스로 배울 수 있다. 사람이 임계를 정해 주지 않는다.
    """
    from scipy.signal import welch
    x = res[i0:i1]
    if len(x) < int(4 * fs):                         # 4초 미만이면 스펙트럼이 무의미
        return None
    nper = min(len(x), int(8 * fs))
    f, P = welch(x, fs=fs, nperseg=nper, noverlap=nper // 2)
    band = (f >= 3.0) & (f <= 12.0)
    if band.sum() < 8 or P[band].sum() <= 0:
        return None
    fb, Pb = f[band], P[band]
    k = int(np.argmax(Pb))
    daf = float(fb[k])                                # 지배 심방 주파수
    near = np.abs(fb - daf) <= 0.5
    sc = float(Pb[near].sum() / Pb.sum())             # 스펙트럼 집중도 ★AFL↑ AFIB↓
    p = Pb / Pb.sum()
    sent = float(-(p[p > 0] * np.log(p[p > 0])).sum() / np.log(len(p)))
    afl = (fb >= 3.5) & (fb <= 5.5)                   # 조동 대역(240~330/분)
    fib = (fb > 5.5) & (fb <= 9.0)                    # 세동 대역(330~540/분)
    ratio = float(Pb[afl].sum() / (Pb[fib].sum() + 1e-12))
    rel = float(np.sqrt(np.mean(x ** 2)) / (qrs_amp + 1e-9))
    av = float(daf * med_rr)                          # 심실 1박당 심방 편위 수
    avi = float(abs(av - round(av)))                  # 정수와의 거리 ★AFL↓ AFIB↑
    nb = (f > 12.0) & (f <= min(20.0, 0.45 * fs))     # 12~20Hz 를 잡음 바닥으로
    snr = float(Pb.mean() / (P[nb].mean() + 1e-12)) if nb.sum() > 3 else float("nan")
    # ★daf 가 진짜 심방 주파수인지 '심실 박동의 고조파'인지 구분하는 진단값.
    #   전도비가 고정이면 심방 주파수 = 심실 주파수의 정수배라 둘이 겹친다. 그때
    #   daf 를 심방 활동의 증거로 읽으면 안 된다 → 모델에 그 조건을 알려 준다.
    vh = 1.0 / max(med_rr, 1e-6)
    dvh = float(abs(daf - round(daf / vh) * vh))
    return [daf, sc, sent, ratio, rel, av, avi, snr, dvh]


def _pqrst_win_feats(x, rpk, s, e, fs):
    """한 창의 **원신호** → P-QRS-T '관계' 특징 11종.

    ★★왜 잔차가 아니라 원신호인가 — 이 절의 존재 이유
      QRST 템플릿 감산은 **R 에 시간고정된 성분을 전부 지운다**. 정상동조율에서는
      PR 간격이 일정해 P 도 R 에 고정돼 있으므로 **P 가 템플릿과 함께 지워진다**.
      그래서 잔차로는 "정상에는 P 가 1:1로 있다"를 절대 못 잰다 — 잔차에서 정상은
      '아무것도 없음'으로 보인다. 잔차는 AFIB/AFL 의 f·F 파(비-R고정) 전용이고,
      **P·T 계측은 반드시 원신호에서** 해야 한다.

    ★무엇을 재는가 (임상 판독의 순서 그대로)
      1:1:1 비율 : 박마다 P 가 하나씩 있는가 → p_amp, pqt_ok(P·T 둘 다 잡힌 박의 비율)
      전도 일관성: PR 이 일정한가 → pr_cv. 정상 낮음 / AFL 은 전도비가 바뀌며 커짐
      탈분극-재분극: R→T 정점 시간과 그 변동 → rt_med, rt_cv
      등전위 구간 : T 정점~다음 P 사이가 **평평한가** → tp_rms(그 구간의 RMS/QRS진폭).
                   정상은 평평해 낮고, AFL 은 톱니가, AFIB 는 f파가 채워 높아진다.
                   ★이것이 사용자가 말한 "1:1:1 비율이 무너진다"의 직접 측정이다 —
                     정상은 한 박에 P 하나뿐이라 그 사이가 비어 있어야 한다.
      P/T 균형   : pt_ratio = P진폭/T진폭
    """
    n = len(rpk)
    e = min(e, n - 1)
    if e - s < 8:
        return None
    pa = []; ta = []; pr = []; rt = []; tp = []; segs = []
    for i in range(s, e):
        r0, r1 = int(rpk[i]), int(rpk[i + 1])
        rr = (r1 - r0) / fs
        if not (0.2 <= rr <= 3.0) or r0 < int(0.06 * fs) or r1 + 1 > len(x):
            continue
        qa = float(np.ptp(x[max(0, r0 - int(0.05 * fs)):r0 + int(0.05 * fs)]))
        if qa <= 1e-9:
            continue
        base = float(np.median(x[r0:r1]))
        # T: R 후 100ms ~ min(450ms, 0.55·RR)
        t_lo = r0 + int(0.10 * fs); t_hi = r0 + int(min(0.45, 0.55 * rr) * fs)
        # P: 다음 R 전 min(320ms, 0.45·RR) ~ 40ms
        p_lo = r1 - int(min(0.32, 0.45 * rr) * fs); p_hi = r1 - int(0.04 * fs)
        if t_hi - t_lo < 3 or p_hi - p_lo < 3:
            continue
        tt = t_lo + int(np.argmax(np.abs(x[t_lo:t_hi] - base)))
        p_lo = max(p_lo, tt + int(0.04 * fs))         # ★T 를 P 로 오인하지 않게
        if p_hi - p_lo < 3:
            continue
        pp = p_lo + int(np.argmax(np.abs(x[p_lo:p_hi] - base)))
        pa.append(abs(x[pp] - base) / qa); ta.append(abs(x[tt] - base) / qa)
        pr.append((r1 - pp) / fs); rt.append((tt - r0) / fs)
        # 등전위(TP) 구간의 RMS — 정상은 비어 평평, AFL/AFIB 는 심방파가 채운다
        g0, g1 = tt + int(0.05 * fs), pp - int(0.02 * fs)
        tp.append(float(np.sqrt(np.mean((x[g0:g1] - base) ** 2)) / qa)
                  if g1 - g0 >= 3 else np.nan)
        L = int(0.20 * fs)                            # P 창(다음 R 기준 고정 길이)
        if r1 - L >= 0:
            q = x[r1 - L - int(0.04 * fs):r1 - int(0.04 * fs)]
            if len(q) == L:
                segs.append((q - q.mean()) / (q.std() + 1e-9))
    if len(pa) < 5:
        return None
    cons = np.nan
    if len(segs) >= 3:
        c = [float(np.dot(segs[j], segs[j + 1]) / len(segs[j]))
             for j in range(len(segs) - 1)]
        cons = float(np.median(c))                    # 박간 P 형태 상관 ★정상↑ AFIB↓
    cv = lambda v: float(np.std(v) / (abs(np.mean(v)) + 1e-9))
    return [float(np.median(pa)), cons, float(np.median(pr)), cv(pr),
            float(np.median(ta)), float(np.median(rt)), cv(rt),
            float(np.nanmedian(tp)) if np.isfinite(tp).any() else float("nan"),
            float(np.median(pa) / (np.median(ta) + 1e-9)),
            len(pa) / max(e - s, 1), 0.0]


def _reconstruct_pid_rec(d, dbs, dldir=None, verbose=True):
    """pid_rec 이 없는 옛 코퍼스를 위해 pid → "db:rec" 를 **규칙으로** 복원한다.

    build_rr_corpus 가 쓴 규칙 그대로다: gpid = pid0 + sorted(recs).index(rec).
    주석이 이미 캐시돼 있으므로 목록만 다시 세면 되고 다운로드는 없다.

    ★안전장치: 복원한 pid 집합이 코퍼스에 실제로 있는 pid 를 **전부 덮지 못하면**
      사용하지 않고 예외를 던진다. 어긋난 매핑으로 신호를 붙이면 에러 없이
      '남의 심전도'가 붙는다 — 이번 프로젝트에서 가장 위험한 종류의 버그다.
    """
    have = set(int(x) for x in np.unique(d["pid"]))
    out = {}
    for db in dbs:
        spec = RRDB_SPEC.get(db)
        if spec is None:
            continue
        dd = _cache_dir(db, ann_only=True, dldir=dldir)
        exts = sorted({"hea", spec["beat_ext"], spec["rhy_ext"]})
        recs = _rr_records(db, dd, exts, verbose=False)
        for i, rec in enumerate(sorted(recs)):
            out[spec["pid0"] + i] = f"{db}:{rec}"
    tgt = {p for p in have
           if any(RRDB_SPEC[db]["pid0"] <= p < RRDB_SPEC[db]["pid0"] + 1000
                  for db in dbs if db in RRDB_SPEC)}
    miss = tgt - set(out)
    if miss:
        raise RuntimeError(
            f"pid_rec 복원 실패 — 코퍼스의 pid {sorted(miss)[:5]} 를 레코드에 대응시킬 "
            f"수 없습니다. 주석 캐시가 코퍼스 생성 때와 다릅니다. "
            f"build_rr_corpus() 를 다시 돌려 pid_rec 을 심으세요(주석은 캐시됨).")
    if verbose:
        print(f"  ↻ pid_rec 이 없어 규칙으로 복원했습니다 "
              f"({len(tgt)}개 pid 전부 대응 확인). 다음 build_rr_corpus 부터는 저장됩니다.")
    return out


def warn_if_gpu(task="이 작업"):
    """★GPU 런타임이 붙어 있는데 GPU 를 쓰지 않는 작업이면 알려 준다.

    왜 필요한가: Colab 의 컴퓨팅 단위는 **GPU 런타임이 붙어 있는 동안 시간으로**
    소모된다 — 실제로 GPU 를 쓰는지와 무관하다. 그런데 코퍼스 생성·심방특징 추출은
    numpy/scipy 전용이라 GPU 사용률이 0% 다. 즉 다운로드로 90분을 보내면 GPU 를
    한 번도 안 쓰면서 90분치 단위가 빠진다. 실제로 그렇게 소모된 것을 사용자가
    먼저 발견했다. 이 함수는 그 낭비를 시작 시점에 드러낸다.
    """
    try:
        import torch
        if not torch.cuda.is_available():
            return False
        name = torch.cuda.get_device_name(0)
    except Exception:
        return False
    print(f"\n  ⚠ GPU({name})가 붙어 있는데 {task}은 **GPU 를 쓰지 않습니다**"
          f"(numpy/scipy 전용).")
    print(f"    Colab 컴퓨팅 단위는 GPU 런타임이 붙어 있는 시간으로 소모되므로,"
          f" 이 작업은\n    런타임 유형을 **CPU 로 바꿔** 돌리는 것이 이득입니다"
          f"(결과 파일은 동일).")
    print(f"    GPU 는 bench_afib(학습)에서만 필요합니다 → 특징 추출을 CPU 로 끝낸 뒤"
          f" GPU 로 전환.")
    return True


def _dl_rec(db, rec, dd):
    """레코드 하나의 .hea/.dat 를 내려받는다(이미 있으면 건너뜀). 스레드에서 호출 가능."""
    for ext in ("hea", "dat"):
        fp = f"{dd}/{rec}.{ext}"
        if os.path.exists(fp) and os.path.getsize(fp) > 0:
            continue
        import wfdb                            # 받을 것이 있을 때만 필요하다
        wfdb.dl_files(db, dd, [f"{rec}.{ext}"])
    return True


def _part_path(base, db, rec, W, stride):
    """레코드 하나의 특징 조각 경로. ★Drive 에 둔다 — 런타임이 죽어도 살아남아야 한다."""
    return f"{base}/atrial_parts/{db}_{str(rec).replace('/', '_')}_W{W}s{stride}.npz"


def build_atrial_feats(dbs=("afdb", "mitdb"), corpus=None, out=None, W=128,
                       stride=None, dldir=None, verbose=True, resume=True,
                       keep_sig=False, max_rec=None, prefetch=3):
    """창별 심방활동 + P-QRS-T 관계 특징 → afib_atrial.npz (창당 19개 스칼라).

    ★corpus 의 pid_rec 매핑이 필요하다. 없으면(옛 코퍼스) 어느 pid 가 어느 레코드인지
      알 수 없어 신호를 못 붙인다 → build_rr_corpus 를 다시 돌려야 한다(주석은 캐시돼
      있으므로 몇 분이면 끝난다).

    ★★이어하기(resume) — 왜 필요한가
      ltafdb 는 84 레코드 × 24시간이라 전체가 수십 분 걸린다. 예전 구현은 **모든
      결과를 메모리에만 쌓다가 마지막에 한 번 저장**했다. 그래서 ltafdb/113 쯤에서
      런타임이 죽자 **그때까지 계산한 25,000 창이 통째로 사라졌다.** 오래 걸리는
      작업이 중간 산출물을 안 남기는 것은 그 자체가 결함이다.
      이제 레코드 하나가 끝날 때마다 Drive 에 조각으로 저장하고(<20KB), 다시 부르면
      이미 있는 레코드를 건너뛴다. 런타임이 몇 번 죽어도 이어서 끝난다.

    ★keep_sig=False: 계산이 끝난 신호 파일(.dat/.hea)을 지운다. 조각이 Drive 에
      남으므로 신호를 남겨 둘 이유가 없고, ltafdb 전체는 ~3GB 라 /content 를 채운다.
    """
    _ensure = _need("_ensure"); _ensure("wfdb"); _ensure("scipy")
    import wfdb
    g = globals()
    if "win_starts" not in g:
        raise RuntimeError("win_starts 없음 — afib_bench.py 를 먼저 로드하세요.")
    win_starts = g["win_starts"]
    stride = int(stride or W)
    d = np.load(corpus or f"{_BASE}/afib_rr.npz", allow_pickle=True)
    pid, t = d["pid"], d["t"]
    if "pid_rec" in d.files:
        p2r = dict(zip([int(x) for x in d["pid_uniq"]],
                       [str(x) for x in d["pid_rec"]]))
    else:
        # 옛 코퍼스 — 매핑을 규칙으로 복원한다(735MB 를 다시 만들지 않기 위해).
        p2r = _reconstruct_pid_rec(d, dbs, dldir=dldir, verbose=verbose)

    warn_if_gpu("심방특징 추출")
    parts = f"{_BASE}/atrial_parts"
    os.makedirs(parts, exist_ok=True)
    todo = []
    for p in np.unique(pid):
        tag = p2r.get(int(p))
        if tag is None:
            continue
        db, rec = tag.split(":", 1)
        if db in dbs:
            todo.append((int(p), db, rec))
    targets = list(todo)                       # 조각 모을 때 쓸 전체 목록(자르지 않음)
    if resume:
        todo = [x for x in todo
                if not os.path.exists(_part_path(_BASE, x[1], x[2], W, stride))]
    if verbose:
        print(f"\n[심방특징] 대상 레코드 {len(targets)}  이미 계산됨 "
              f"{len(targets)-len(todo)}  남음 {len(todo)}")
        # ★남은 다운로드 용량을 **미리** 보여 준다. 레코드 길이는 코퍼스의 t 에서
        #   직접 구한다(하드코딩하면 DB 를 추가할 때 틀린 값이 남는다).
        #   WFDB format 212 = 샘플당 1.5바이트, 2채널 가정.
        per = {}
        for p, db, rec in todo:
            tt = t[pid == p]
            if not len(tt):
                continue
            mb = float(tt.max()) * RRDB_SPEC[db]["fs"] * 2 * 1.5 / 1e6
            a, b = per.get(db, (0, 0.0))
            per[db] = (a + 1, b + mb)
        if per:
            print(f"  남은 다운로드(신호):")
            for db, (k, mb) in sorted(per.items()):
                print(f"    {db:<10} {k:>4}레코드  {mb/1000:>6.2f} GB  "
                      f"(레코드당 ~{mb/max(k,1):.0f} MB)")
            tot = sum(v[1] for v in per.values())
            print(f"    합계 {tot/1000:.2f} GB  —  keep_sig={keep_sig} 이므로 디스크 최대"
                  f" 점유는 레코드 1개분뿐")
        if len(todo) < len(targets):
            print(f"  ↻ 이어하기: 완료된 레코드는 건너뜁니다(조각 {parts})")
    if max_rec:
        todo = todo[:int(max_rec)]
        print(f"  (max_rec={max_rec} → 이번 실행은 {len(todo)}개만 처리)")

    # ── 다운로드 선행 인출(prefetch) ──────────────────────────────────────────
    #  ★실측: ltafdb 레코드 1개의 **계산**은 31초인데 실제로는 ~6분이 걸린다.
    #    차이(~5.5분)는 전부 PhysioNet 다운로드다(34MB ≈ 100KB/s). 즉 이 작업은
    #    CPU 병목이 아니라 **네트워크 병목**이고, 계산을 최적화해도 6분은 안 줄어든다.
    #    그래서 다음 레코드들을 미리 받아 둔다 — 계산과 다운로드가 겹치고,
    #    동시 연결이 여러 개면 단일 연결 속도 제한도 우회된다.
    ex = None
    if prefetch and prefetch > 1 and len(todo) > 1:
        from concurrent.futures import ThreadPoolExecutor
        ex = ThreadPoolExecutor(max_workers=int(prefetch))
        if verbose:
            print(f"  ⇉ 다운로드 선행 인출 {prefetch}개 동시 "
                  f"(디스크 최대 ~{34*prefetch}MB 점유)")
    fut = {}

    def _submit(i):
        if ex is None or not (0 <= i < len(todo)):
            return
        _, db_, rec_ = todo[i]
        dd_ = _cache_dir(db_, ann_only=False, dldir=dldir)
        os.makedirs(dd_, exist_ok=True)
        fut[i] = ex.submit(_dl_rec, db_, rec_, dd_)

    for i in range(min(int(prefetch or 1), len(todo))):
        _submit(i)

    n_ok = n_bad = 0
    for i, (p, db, rec) in enumerate(todo):
        _submit(i + int(prefetch or 1))        # 계산하는 동안 뒤쪽을 받아 둔다
        pp = _part_path(_BASE, db, rec, W, stride)
        idx = np.flatnonzero(pid == p)
        starts = win_starts(len(idx), W, stride)
        if not starts:
            fut.pop(i, None)                   # 선행 인출을 버려도 파일은 캐시에 남는다
            continue
        dd = _cache_dir(db, ann_only=False, dldir=dldir)
        os.makedirs(dd, exist_ok=True)
        try:
            if i in fut:
                fut.pop(i).result()            # 미리 받던 것이 끝나길 기다림
            else:
                _dl_rec(db, rec, dd)
            r = wfdb.rdrecord(f"{dd}/{rec}")
        except Exception as e:
            print(f"  ✗ {db}/{rec}: 신호 로드 실패 {type(e).__name__}"); n_bad += 1; continue
        fs = float(r.fs)
        sig = np.asarray(r.p_signal, "float32")
        nlead = min(2, sig.shape[1])
        # ★리드를 **여기서 한 번** 잘라 둔다. 예전엔 창마다 sig[:, c] 를 다시
        #   잘랐는데, 그건 비연속 슬라이스라 매번 복사본을 만든다. ltafdb 한
        #   레코드가 2,200만 샘플이라 창 800개 × 리드 2개 = 복사 1,600회(회당
        #   ~88MB)가 됐다. 런타임이 죽은 유력한 원인이다.
        col = [np.ascontiguousarray(sig[:, c]) for c in range(nlead)]
        del r                                  # p_signal 은 float64 라 원본이 4배 크다
        rpk = np.round(np.asarray(t[idx], np.float64) * fs).astype(int)
        rpk = np.clip(rpk, 0, len(sig) - 1)
        # 리드별로 (a) 심방 잔차 (b) 원신호 를 준비한다.
        #  ★(a)와 (b)는 서로 대체 불가다: 잔차는 R 고정 성분을 지우므로 AFIB/AFL 의
        #    f·F 파에는 이상적이지만 정상 P 를 함께 지운다. P·T 계측은 원신호에서.
        res = []
        for c in range(nlead):
            rr_ = _atrial_residual(col[c], rpk, fs)
            res.append(_bandpass(rr_, fs) if rr_ is not None else None)
        if all(v is None for v in res):
            n_bad += 1; continue
        nf = len(ATR_NAMES)
        KEY, F = [], []                       # ★레코드 하나치만 담는다(조각 저장)
        for s in starts:
            s2 = min(s + W - 1, len(rpk) - 1)
            i0, i1 = rpk[s], rpk[s2]
            med_rr = float(np.median(np.diff(rpk[s:s2 + 1]))) / fs if s2 > s else 0.8
            best = None
            for c, rv in enumerate(res):
                if rv is None:
                    continue
                qa = float(np.median([np.ptp(col[c][max(0, int(rp) - int(0.05 * fs)):
                                                    int(rp) + int(0.05 * fs)])
                                      for rp in rpk[s:s2 + 1:8]] or [1.0]))
                fs_ = _spec_win_feats(rv, i0, i1, fs, med_rr, qa)
                if fs_ is None:
                    continue
                fp_ = _pqrst_win_feats(col[c], rpk, s, s2, fs)
                fp_ = fp_ if fp_ is not None else [float("nan")] * len(PQ_NAMES)
                fp_[-1] = float(c)
                cand = fs_ + fp_
                if best is None or cand[1] > best[1]:    # sc 가 큰 리드 채택
                    best = cand
            KEY.append((int(p), int(s)))
            F.append(best if best is not None else [float("nan")] * nf)
        # ★레코드가 끝나는 즉시 Drive 에 조각 저장 — 다음 줄에서 죽어도 안 잃는다
        np.savez(pp, key=np.array(KEY, np.int64), feat=np.array(F, "float32"),
                 names=np.array(ATR_NAMES), W=int(W), stride=int(stride))
        n_ok += 1
        del sig, res, col
        if not keep_sig:                       # 신호는 조각을 남긴 뒤엔 쓸모없다
            for ext in ("hea", "dat"):
                try:
                    os.remove(f"{dd}/{rec}.{ext}")
                except OSError:
                    pass
        if verbose:
            print(f"    {db}/{rec}: 창 {len(KEY)} 저장  "
                  f"({n_ok}/{len(todo)}, 남음 {len(todo)-n_ok})", flush=True)

    if ex is not None:
        for f in fut.values():                 # 남은 선행 인출 취소(다음 실행이 다시 받음)
            f.cancel()
        ex.shutdown(wait=False)

    # ── 조각 모으기 — 이번에 만든 것 + 예전 실행이 남긴 것 ────────────────────
    KEY, F = [], []
    miss = []
    for p, db, rec in targets:                 # ★max_rec 로 잘리기 전의 전체 목록
        pp = _part_path(_BASE, db, rec, W, stride)
        if not os.path.exists(pp):
            miss.append(f"{db}/{rec}"); continue
        a = np.load(pp, allow_pickle=True)
        KEY.append(a["key"]); F.append(a["feat"])
    if not F:
        raise RuntimeError("특징이 하나도 안 만들어졌습니다 — dbs 가 코퍼스에 있는지 확인.")
    KEY = np.concatenate(KEY); F = np.concatenate(F)
    out = out or f"{_BASE}/afib_atrial.npz"
    np.savez(out, key=KEY.astype(np.int64), feat=F.astype("float32"),
             names=np.array(ATR_NAMES), W=int(W), stride=int(stride))
    A = F.astype("float32")
    print(f"\n✔ 저장 {out}  ({os.path.getsize(out)/1e6:.2f} MB)  "
          f"창 {len(F):,}  레코드 {n_ok} 신규 / {len(targets)-len(todo)} 재사용 "
          f"/ {n_bad} 실패")
    if miss:
        print(f"  ⚠ 조각 없는 레코드 {len(miss)}개: {miss[:6]}{' …' if len(miss) > 6 else ''}")
        print(f"    → 같은 명령을 다시 부르면 이 레코드만 이어서 계산합니다.")
    bad = int(np.isnan(A[:, 0]).sum())
    print(f"  추출 실패 창 {bad:,} ({100*bad/len(A):.1f}%) → NaN 으로 남김(0 으로 위장 안 함)")
    print(f"  ★신호는 저장하지 않았다 — 레코드마다 계산 후 버렸다")
    return out


def _auc_rank(x, pos):
    """순위 기반 AUC(=Mann-Whitney U). NaN 제외, 동점은 평균순위."""
    from scipy.stats import rankdata
    m = np.isfinite(x)
    x, pos = np.asarray(x)[m], np.asarray(pos, bool)[m]
    n1 = int(pos.sum()); n0 = int((~pos).sum())
    if n1 < 2 or n0 < 2:
        return float("nan")
    r = rankdata(x)
    return float((r[pos].sum() - n1 * (n1 + 1) / 2) / (n1 * n0))


def atrial_audit(atrial=None, corpus=None, W=128, stride=None, min_win=5,
                 verbose=True):
    """★모델 이전의 기전 검증 (사전등록 H-P / H-R).

    ── 이 함수가 반드시 두 층위로 보는 이유 ─────────────────────────────────
    창 단위로만 보면 **창을 많이 가진 소수 환자가 결론을 만든다**. AFL 은 환자가
    7명뿐이라 한 명이 창 50개를 내면 그 사람 하나가 '기전 확인'을 만들어낼 수 있다.
    그래서 (환자, 리듬) 칸마다 중앙값을 내어 **환자 단위 AUC**를 따로 계산하고,
    창 AUC 와 크게 벌어지면 경고한다. 벌어짐 자체가 진단 정보다.
    """
    g = globals()
    win_starts = g["win_starts"]
    stride = int(stride or W)
    a = np.load(atrial or f"{_BASE}/afib_atrial.npz", allow_pickle=True)
    d = np.load(corpus or f"{_BASE}/afib_rr.npz", allow_pickle=True)
    names = [str(x) for x in a["names"]]
    K = {(int(p), int(s)): i for i, (p, s) in enumerate(a["key"])}
    rn = [str(x) for x in d["rhythm_names"]]
    pid, rhy, pre = d["pid"], d["rhythm"], d["pre_rr"]
    lab, feat, who, rrw = [], [], [], []
    for p in np.unique(pid):
        idx = np.flatnonzero(pid == p)
        for s in win_starts(len(idx), W, stride):
            j = K.get((int(p), int(s)))
            if j is None:
                continue
            w = rhy[idx][s:s + W]
            u, c = np.unique(w, return_counts=True)
            k = int(np.argmax(c))
            if c[k] / W < 0.90:
                continue
            lab.append(rn[u[k]]); feat.append(a["feat"][j]); who.append(int(p))
            # ★창의 중앙 RR — '이 특징이 사실은 심박수 아닌가' 를 검사하기 위한 것
            rrw.append(float(np.median(pre[idx][s:s + W])) / 360.0)
    lab = np.array(lab); feat = np.array(feat); who = np.array(who)
    rrw = np.array(rrw)
    TGT = ("N", "AFIB", "AFL")

    # ── (환자, 리듬) 칸별 중앙값 — 환자 단위 통계의 기본 단위 ────────────────
    cells = {}                       # (pid, rhythm) → 특징 중앙값
    for nm in TGT:
        for p in np.unique(who[lab == nm]) if (lab == nm).any() else []:
            m = (lab == nm) & (who == p)
            if m.sum() >= min_win:
                cells[(int(p), nm)] = np.nanmedian(feat[m], axis=0)

    print(f"\n=== 심방활동 특징 감사  창 {len(lab):,} / 환자 {len(np.unique(who))} ===")
    print(f"  ('환자' 열 = 그 리듬 창을 {min_win}개 이상 가진 환자 / 조금이라도 가진 환자)")
    nsp = len(SPEC_NAMES)

    def _tbl(title, cols):
        print(f"\n  [{title}]  (창 중앙값)")
        print(f"  {'리듬':<7}{'창':>7}{'환자':>7}" + "".join(f"{names[i]:>10}" for i in cols))
        for nm in TGT:
            m = lab == nm
            npat = len({k[0] for k in cells if k[1] == nm})
            nall = len(np.unique(who[m])) if m.any() else 0
            # '환자' 는 창 min_win 개 이상을 가진 환자 수 / 그 리듬을 가진 전체 환자 수.
            # 둘이 크게 다르면 대부분의 환자가 그 리듬을 아주 조금만 가졌다는 뜻이다.
            pc = f"{npat}/{nall}"
            if m.sum() < min_win:
                print(f"  {nm:<7}{int(m.sum()):>7}{pc:>7}   (표본 부족)"); continue
            v = np.nanmedian(feat[m], axis=0)
            print(f"  {nm:<7}{int(m.sum()):>7}{pc:>7}"
                  + "".join(f"{v[i]:>10.3f}" for i in cols))

    _tbl("심방활동 스펙트럼 (QRST 소거 잔차)", list(range(nsp)))
    _tbl("P-QRS-T 관계 (원신호)", list(range(nsp, len(names) - 1)))

    # ── 판별력: 창 AUC vs 환자 AUC ───────────────────────────────────────
    def _cmp(a_nm, b_nm):
        wm = np.isin(lab, [a_nm, b_nm])
        if wm.sum() < 10:
            print(f"\n  [{a_nm} vs {b_nm}] 표본 부족 — 생략"); return
        wpos = lab[wm] == a_nm
        ck = [k for k in cells if k[1] in (a_nm, b_nm)]
        cX = np.array([cells[k] for k in ck]); cpos = np.array([k[1] == a_nm for k in ck])
        na, nb = int(cpos.sum()), int((~cpos).sum())
        print(f"\n  [{a_nm} vs {b_nm}]  창 {int(wm.sum()):,}  |  환자칸 {a_nm} {na} vs {b_nm} {nb}")
        if na < 2 or nb < 2:
            print(f"    ⚠ 환자칸이 2개 미만 — 환자단위 AUC 계산 불가. 창 AUC 만 참고할 것.")
        print(f"    {'특징':<11}{'창AUC':>8}{'환자AUC':>9}   판정")
        rows = []
        for i, n in enumerate(names):
            if n == "lead":
                continue
            aw = _auc_rank(feat[wm][:, i], wpos)
            ap = _auc_rank(cX[:, i], cpos) if (na >= 2 and nb >= 2) else float("nan")
            rows.append((max(aw, 1 - aw) if np.isfinite(aw) else 0, i, n, aw, ap))
        for _, i, n, aw, ap in sorted(rows, reverse=True)[:8]:
            d_ = abs(aw - 0.5)
            if not np.isfinite(ap):
                v = "환자단위 미산출"
            elif abs(aw - ap) > 0.15:
                v = "⚠창≫환자 — 소수 환자가 끎"
            elif d_ < 0.10:
                v = "판별력 낮음"
            else:
                v = "★일치(견고)"
            aps = f"{ap:>9.3f}" if np.isfinite(ap) else f"{'—':>9}"
            print(f"    {n:<11}{aw:>8.3f}{aps}   {v}")

    _cmp("AFL", "AFIB")
    _cmp("AFL", "N")
    _cmp("AFIB", "N")

    # ── ★심박수 교란 점검 ───────────────────────────────────────────────
    #  절대 시간 특징(pr_med·rt_med 등)은 심박수가 빨라지면 그냥 짧아진다.
    #  그런데 심박수는 **이미 RR 축(1층·2층 시퀀스)이 갖고 있는 정보**다.
    #  RR 과 강하게 붙은 특징의 판별력은 '새 정보'가 아니라 중복이므로,
    #  형태축의 기여로 계상하면 안 된다. 여기서 그것을 먼저 걸러 낸다.
    from scipy.stats import spearmanr
    print(f"\n  [심박수 교란 점검]  특징 vs 창 중앙 RR 의 |Spearman ρ|")
    print(f"    (|ρ|>0.5 면 그 특징의 판별력은 대부분 심박수다 — 형태축 기여로 세지 말 것)")
    conf = {}
    for i, n in enumerate(names):
        if n == "lead":
            continue
        m = np.isfinite(feat[:, i])
        if m.sum() < 20:
            continue
        r = spearmanr(feat[m, i], rrw[m]).statistic
        conf[n] = abs(float(r)) if np.isfinite(r) else 0.0
    for n, r in sorted(conf.items(), key=lambda kv: -kv[1])[:8]:
        v = "⚠심박수 대리" if r > 0.5 else ("주의" if r > 0.35 else "독립적")
        print(f"    {n:<11}|ρ|={r:.3f}   {v}")

    # ── 사전등록 판정 ────────────────────────────────────────────────────
    def med(nm, i):
        m = lab == nm
        return float(np.nanmedian(feat[m, i])) if m.sum() >= min_win else float("nan")
    i_sc, i_daf = names.index("sc"), names.index("daf")
    i_tp, i_prcv = names.index("tp_rms"), names.index("pr_cv")
    print(f"\n  === 사전등록 판정 ===")
    sc_fl, sc_fb = med("AFL", i_sc), med("AFIB", i_sc)
    print(f"  [H-P] 집중도 sc: AFL {sc_fl:.3f} vs AFIB {sc_fb:.3f}  "
          f"→ {'★기전 확인' if sc_fl > sc_fb else '✗ 예상과 반대 — 추출 점검'}")
    df_fl, df_fb, df_n = med("AFL", i_daf), med("AFIB", i_daf), med("N", i_daf)
    print(f"  [H-P] 지배주파수 daf: N {df_n:.2f} / AFIB {df_fb:.2f} / AFL {df_fl:.2f} Hz"
          f"  (문헌 AFL 4~5.7, AFIB 5.8~10)")
    if abs(df_fb - df_n) < 0.5:
        print(f"    ✗ AFIB 의 daf 가 정상과 거의 같다 → daf 는 심방 주파수가 아니라")
        print(f"      **QRST 소거 잔차**를 재고 있다. daf 를 단독 근거로 쓰면 안 된다.")
        print(f"      (스펙트럼 '모양' 지표 sc·sent·afl_ratio 는 이 오염에 덜 민감하다)")
    tp_n, tp_fl, tp_fb = med("N", i_tp), med("AFL", i_tp), med("AFIB", i_tp)
    pv_n, pv_fb = med("N", i_prcv), med("AFIB", i_prcv)
    print(f"  [H-R] 등전위 tp_rms: N {tp_n:.4f} / AFIB {tp_fb:.4f} / AFL {tp_fl:.4f}"
          f"  → {'★확인' if (tp_fl > tp_n and tp_fb > tp_n) else '미확인'}")
    print(f"  [H-R] PR 변동 pr_cv: N {pv_n:.4f} / AFIB {pv_fb:.4f}"
          f"  → {'★확인' if pv_fb > pv_n else '미확인'}")
    print(f"\n  ※ '⚠창≫환자' 가 붙은 특징은 소수 환자가 만든 것이다. 그 특징에 기댄")
    print(f"    결론은 환자 수를 늘리기 전까지 유보한다(사전등록 §8.4).")
    return dict(lab=lab, feat=feat, who=who, names=names, cells=cells)


# ─────────────────────────────────────────────────────────────────────────────
#  6. 자기검증
# ─────────────────────────────────────────────────────────────────────────────
def _synth_ecg(kind="N", secs=120, fs=250, seed=0):
    """합성 심전도 — 추출 로직을 데이터 없이 검증하기 위한 것.

    N    : P(PR 160ms 고정) - QRS - T,  HR 60         → 한 박에 P 하나, TP 평평
    AFL  : F파 톱니 5Hz(300/분) 연속 + 2:1 전도(HR 150) → TP 구간이 톱니로 채워짐
    AFIB : f파 무질서 6~9Hz + RR 불규칙                → TP 채워짐 + 불규칙
    반환 (신호, R위치)
    """
    rng = np.random.RandomState(seed)
    n = int(secs * fs); x = np.zeros(n, "float64")
    g = lambda c, w, a: a * np.exp(-0.5 * ((np.arange(n) - c) / (w * fs)) ** 2)
    if kind == "AFL":
        rr = 0.4; f_at = 5.0
        x += 0.15 * np.abs(((np.arange(n) / fs * f_at) % 1.0) - 0.5) * 4 - 0.3
    elif kind == "AFIB":
        rr = None
        # f파는 진폭·주파수·위상이 모두 무질서해야 한다. 위상이 이어지는 sine 은
        # 실제보다 훨씬 규칙적이라 스펙트럼 집중도를 과대평가한다.
        for _ in range(int(secs * 7)):
            c = rng.randint(0, n); w = rng.uniform(0.010, 0.030)
            x += rng.choice([-1, 1]) * rng.uniform(0.03, 0.10) * \
                 np.exp(-0.5 * ((np.arange(n) - c) / (w * fs)) ** 2)
    else:
        rr = 1.0
    t = 0.5; R = []
    while t < secs - 1.0:
        r = int(t * fs); R.append(r)
        x += g(r, 0.012, 1.0) - g(r - int(0.022 * fs), 0.008, 0.18) \
             - g(r + int(0.022 * fs), 0.008, 0.25)          # QRS
        x += g(r + int(0.30 * fs), 0.045, 0.28)             # T
        if kind == "N":
            x += g(r - int(0.16 * fs), 0.022, 0.14)         # P (R 에 고정)
        step = rr if rr else float(np.clip(0.55 + rng.randn() * 0.16, 0.3, 1.6))
        t += step
    x += rng.randn(n) * 0.008
    return x.astype("float32"), np.array(R, np.int64)


def selftest_atrial(verbose=True):
    """★심방·PQRST 추출이 생리와 맞는 방향으로 움직이는지 합성 심전도로 검증.

    실데이터에서 H-P 가 실패했을 때 '추출이 틀렸나 / 데이터가 그런가'를 가르려면
    추출이 옳다는 독립 증거가 있어야 한다. 이것이 그 증거다.
    """
    ok = lambda c, m: (_ for _ in ()).throw(AssertionError(m)) if not c else print(f"  ✔ {m}")
    fs = 250; W = 96
    got = {}
    for kind in ("N", "AFL", "AFIB"):
        x, R = _synth_ecg(kind, secs=200, fs=fs, seed=1)
        res = _bandpass(_atrial_residual(x, R, fs), fs)
        s, e = 0, min(W - 1, len(R) - 1)
        med_rr = float(np.median(np.diff(R[s:e + 1]))) / fs
        qa = float(np.median([np.ptp(x[r - 12:r + 12]) for r in R[s:e + 1:8]]))
        sp = _spec_win_feats(res, R[s], R[e], fs, med_rr, qa)
        pq = _pqrst_win_feats(x, R, s, e, fs)
        got[kind] = dict(zip(ATR_NAMES, (sp or [np.nan] * len(SPEC_NAMES))
                                + (pq or [np.nan] * len(PQ_NAMES))))
    if verbose:
        keys = ["daf", "daf_vh", "sc", "av_ratio", "aa_rel", "tp_rms", "p_amp", "pr_cv"]
        print(f"\n  {'리듬':<6}" + "".join(f"{k:>10}" for k in keys))
        for k, v in got.items():
            print(f"  {k:<6}" + "".join(f"{v[n]:>10.3f}" for n in keys))
    N, FL, FB = got["N"], got["AFL"], got["AFIB"]
    # ── ① P-QRS-T 관계(원신호) — 사용자 착안. 여기가 AFL 의 주 판별축이다 ──────
    ok(FL["tp_rms"] > N["tp_rms"] * 1.5,
       f"AFL: 등전위 구간이 톱니로 채워짐 (tp_rms {FL['tp_rms']:.3f} > N {N['tp_rms']:.3f})")
    ok(FB["tp_rms"] > N["tp_rms"] * 1.5,
       f"AFIB: 등전위 구간이 f파로 채워짐 (tp_rms {FB['tp_rms']:.3f})")
    ok(N["pr_cv"] < 0.05, f"정상: PR 이 일정 (pr_cv {N['pr_cv']:.4f}) — 1:1 전도")
    ok(FB["pr_cv"] > N["pr_cv"] * 3,
       f"AFIB: PR 이 일정하지 않음 ({FB['pr_cv']:.3f}) — P 가 R 에 안 묶임")

    # ── ② 잔차 스펙트럼 — ★알려진 한계를 '검증'으로 못 박는다 ─────────────────
    #  고정비 AFL 에서는 조동파가 R 에 시간고정이라 QRST 평균감산이 **조동파까지
    #  함께 지운다**. 그래서 잔차의 daf 는 조동 주파수를 못 준다. 이건 합성으로
    #  재현되는 구조적 성질이지 버그가 아니다 — 문서·특징(daf_vh)으로 드러내고,
    #  AFL 판별은 ①(원신호 P-QRS-T)에 맡긴다.
    ok(FL["daf_vh"] < 0.5,
       f"AFL: daf 가 심실 고조파와 겹침 (거리 {FL['daf_vh']:.3f}Hz) → daf 를 심방 "
       f"증거로 읽으면 안 되는 상황이 daf_vh 로 드러남")
    ok(FB["daf_vh"] > FL["daf_vh"],
       f"AFIB: daf 가 심실 고조파에서 떨어져 있음 ({FB['daf_vh']:.3f} > {FL['daf_vh']:.3f})")
    ok(FB["aa_rel"] > N["aa_rel"] * 3,
       f"AFIB: 비-R고정 심방활동이 크다 (aa_rel {FB['aa_rel']:.3f} vs N {N['aa_rel']:.3f})")
    ok(N["aa_rel"] < 0.02,
       f"정상: 잔차가 거의 0 (aa_rel {N['aa_rel']:.4f}) — P 가 R 고정이라 템플릿과 "
       f"함께 지워진다. ★그래서 정상 P 계측은 원신호에서만 가능하다")
    print("=== 심방 추출 검증 통과 ===")
    print("  ※ 확인된 구조적 한계: 고정비 AFL 은 잔차 스펙트럼으로 못 잡는다.")
    print("     AFL 판별은 원신호 P-QRS-T 관계(tp_rms 등)가 담당한다.")
    return got


def selftest():
    ok = lambda c, m: (_ for _ in ()).throw(AssertionError(m)) if not c else print(f"  ✔ {m}")
    print("=== ecg_multidb 자기검증 ===")
    ok(len(set(v["pid0"] for v in DB_SPEC.values())) == len(DB_SPEC), "DB별 pid 오프셋이 서로 다름")
    offs = sorted(v["pid0"] for v in DB_SPEC.values())
    ok(all(offs[i + 1] - offs[i] >= 1000 for i in range(len(offs) - 1)),
       "오프셋 간격 ≥1000 (레코드 수보다 크므로 충돌 불가)")
    # _need 가 없는 심볼에 대해 명확히 실패하는지
    try:
        _need("__없는심볼__"); ok(False, "없는 심볼에 예외")
    except RuntimeError as e:
        ok("svdb_labels" in str(e), "없는 심볼이면 svdb_labels 를 먼저 로드하라고 안내")
    ok(callable(db_audit) and callable(build_multi), "공개 함수 존재")
    # ── 2층 RR 코퍼스 명세 ──
    ok(len(set(v["pid0"] for v in RRDB_SPEC.values())) == len(RRDB_SPEC),
       "RRDB_SPEC 도 pid 오프셋이 서로 다름")
    for db, v in RRDB_SPEC.items():
        if db in DB_SPEC:
            ok(v["pid0"] == DB_SPEC[db]["pid0"],
               f"{db}: 두 명세의 pid 오프셋 일치(코퍼스를 섞어도 환자가 안 뒤섞임)")
    ok(RRDB_SPEC["afdb"]["beat_audited"] is False,
       "afdb 는 비트 미감사로 표시됨(AAMI 라벨 오용 차단)")
    ok(callable(build_rr_corpus) and callable(rr_audit_dbs), "2층 공개 함수 존재")
    ok(len(ATR_NAMES) == len(SPEC_NAMES) + len(PQ_NAMES) == 20, "심방 특징 20종")
    try:
        selftest_atrial(verbose=True)
    except ImportError:
        print("  · scipy 없음 — 심방 추출 검증 건너뜀")
    print("=== 전 항목 통과 ===")
    return True


if __name__ == "__main__":
    import sys
    if "--selftest" in sys.argv:
        _here = os.path.dirname(os.path.abspath(__file__))
        exec(open(f"{_here}/svdb_labels.py").read(), globals())   # 의존 심볼 로드
        selftest()
