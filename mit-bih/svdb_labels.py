# =============================================================================
#  svdb_labels.py  —  라벨 재고조사 + 확장 추출 (5-class 비트 + 리듬/질병 라벨)
#
#  ── 왜 이게 필요한가 ────────────────────────────────────────────────────────
#  목표가 "S·V·N 및 그 외 비트를 99% 이상 + 질병 진단 99% 이상" 이라면, 지금
#  파이프라인에는 **구조적 격차 두 개**가 있다. 둘 다 코드로 확인된 사실이다:
#
#   (1) '그 외의 비트'가 데이터에 아예 없다.
#       svdb_prep.py:29
#         _AAMI={'N':0,'L':0,'R':0,'e':0,'j':0, 'A':1,'a':1,'J':1,'S':1, 'V':2,'E':2}
#         ...  lab=_AAMI.get(sym[i],None);  if lab is None: continue     ← 버림
#       즉 F(융합박)·Q(분류불가)·/(페이스박) 등은 svdb_data.npz 에 존재하지 않는다.
#       없는 클래스는 정확도를 측정할 수도, 올릴 수도 없다.
#
#   (2) 질병(리듬) 라벨을 한 번도 읽지 않는다.
#       repo 전체에 aux_note 참조가 없다. WFDB 는 리듬 구간을 '+' 주석의
#       aux_note("(AFIB", "(B", "(SVTA" ...)로 표시하는데, 이걸 전부 버리고 있다.
#
#  ★두 문제는 연결돼 있다: svdb_rhythm.rr_audit() 이 경고한 'pre_rr 오염'의 범인이
#    바로 그 '+' 주석이다. svdb_prep 은 rr=np.diff(ann.sample) 로 **모든 주석**의
#    간격을 RR 로 쓰기 때문에, '+' 가 낀 자리에서 가짜 RR 이 생긴다.
#    → 여기서는 RR 을 **비트 주석만으로** 계산해 그 오염을 원천 제거한다.
#
#  ── 무엇을 만드나 ───────────────────────────────────────────────────────────
#   label_audit()   : 무엇이 있고 무엇을 버리고 있는지 전수 조사 + 99% 검정력 계산
#   build_labeled() : svdb_data5.npz 생성
#                     y5     0=N 1=S 2=V 3=F 4=Q   (AAMI 5-class, 전 비트 보존)
#                     y3     기존 3-class (F/Q 는 -1)  ← 기존 결과 재현용
#                     sym    원 심볼(정보 무손실)
#                     rhythm 비트가 속한 리듬 에피소드 id  ← 질병 진단 라벨
#                     pre_rr/post_rr : ★비트 주석만으로 계산(오염 없음)
#
#   ★비파괴 설계: 기존 svdb_data.npz 를 덮지 않는다. y3>=0 으로 거르면 기존
#     데이터셋이 그대로 재현되므로, 0.534 기준선의 유효성이 유지된다.
#
#  ── 실행 (Colab) ────────────────────────────────────────────────────────────
#    label_audit()                 # ① 먼저. 무엇이 있는지 보고 나서 정한다
#    build_labeled()               # ② svdb_data5.npz 생성 (전체 78레코드)
#
#  자기검증(데이터 없이):  python svdb_labels.py --selftest
# =============================================================================
import numpy as np

_BASE  = globals().get("_BASE", "/content/drive/MyDrive/mitbih")
_DLDIR = "/content/svdb_raw"
_FS_SRC, _FS_DST = 128, 360
_L, _RPRE = 300, 100

# ── AAMI 5-class 매핑 (ANSI/AAMI EC57) ──────────────────────────────────────
#  기존 _AAMI 는 여기서 N/S/V 만 남긴 부분집합이다. F·Q 를 되살린다.
AAMI5 = {
    # N: 정상 및 각차단 계열
    'N': 0, 'L': 0, 'R': 0, 'e': 0, 'j': 0,
    # S: 상심실성 이소성
    'A': 1, 'a': 1, 'J': 1, 'S': 1,
    # V: 심실성 이소성
    'V': 2, 'E': 2,
    # F: 융합박 (정상 + 심실) ← 지금까지 버려짐
    'F': 3,
    # Q: 분류불가 / 페이스 ← 지금까지 버려짐
    '/': 4, 'f': 4, 'Q': 4,
}
CLS5 = ["N", "S", "V", "F", "Q"]

# WFDB 비트 주석 심볼 전체(이 밖은 리듬·잡음·구간 표시 등 비-비트)
BEAT_SYMS = set("NLRBAaJSVrFejnE/fQ?")


# ─────────────────────────────────────────────────────────────────────────────
#  1. 순수 로직 (wfdb 없이 검증 가능)
# ─────────────────────────────────────────────────────────────────────────────
def parse_rhythm(aux):
    """aux_note → 리듬 이름. '(AFIB\\x00' → 'AFIB'. 리듬 표기가 아니면 None."""
    if not aux:
        return None
    s = str(aux).strip().strip("\x00").strip()
    if not s.startswith("("):
        return None
    s = s[1:].strip().strip("\x00")
    return s or None


def rhythm_per_beat(samp, sym, aux, beat_pos):
    """각 비트가 속한 리듬 에피소드 이름을 앞으로 채워(forward-fill) 돌려준다.

    WFDB 규약: 리듬은 '+' 주석의 aux_note 로 '여기서부터 이 리듬'을 표시한다.
    다음 리듬 표기가 나오기 전까지 유효하므로 forward-fill 이 정확한 해석이다.
    첫 리듬 표기 이전 구간은 None(미상) — 라벨을 지어내지 않는다.
    """
    marks = []                                   # (sample, rhythm)
    for i in range(len(sym)):
        r = parse_rhythm(aux[i] if aux is not None else None)
        if r:
            marks.append((int(samp[i]), r))
    marks.sort()
    if not marks:
        return [None] * len(beat_pos)
    ms = np.array([m[0] for m in marks])
    names = [m[1] for m in marks]
    # beat_pos 각각에 대해 '자기 이하의 마지막 마크'
    idx = np.searchsorted(ms, np.asarray(beat_pos), side="right") - 1
    return [names[i] if i >= 0 else None for i in idx]


def beat_only_rr(beat_samp, fs=_FS_DST, fallback=None):
    """★비트 주석만으로 RR 계산 — '+' 등 비-비트 주석 오염을 원천 제거.

    svdb_prep.py 는 rr=np.diff(ann.sample) 로 **모든** 주석 간격을 쓴다. 리듬 변경
    표시('+')가 비트 사이에 끼면 그 자리에서 RR 이 쪼개져 가짜 값이 된다.
    여기서는 비트 위치만 diff 하므로 그런 일이 생기지 않는다.
    반환: (pre, post)  단위 = 샘플(fs 기준). 첫/끝은 이웃값으로 채우고 플래그를 남긴다.
    """
    s = np.asarray(beat_samp, np.int64)
    n = len(s)
    if n < 2:
        v = float(fallback if fallback is not None else 0.83 * fs)
        return np.full(n, v, "float32"), np.full(n, v, "float32"), np.zeros(n, bool)
    d = np.diff(s).astype("float64")              # 길이 n-1
    pre = np.empty(n); post = np.empty(n)
    pre[1:] = d; pre[0] = d[0]                    # 첫 비트의 pre 는 미상 → 이웃 복제
    post[:-1] = d; post[-1] = d[-1]               # 끝 비트의 post 는 미상 → 이웃 복제
    edge = np.zeros(n, bool); edge[0] = True; edge[-1] = True
    return pre.astype("float32"), post.astype("float32"), edge


def power_for_accuracy(n, p=0.99, conf=1.96):
    """정확도 p 를 주장할 때 표본 n 에서의 95% CI 반폭. n=0 이면 inf."""
    if n <= 0:
        return float("inf")
    return float(conf * np.sqrt(p * (1 - p) / n))


def n_for_halfwidth(h, p=0.99, conf=1.96):
    """CI 반폭 h 를 얻는 데 필요한 최소 표본 수."""
    return int(np.ceil(conf ** 2 * p * (1 - p) / (h ** 2)))


def summarize(sym_counts, rhy_counts, rhy_records=None, sym_records=None, target=0.99):
    """재고조사 결과 출력 + 99% 주장 가능성 판정. (표준출력용, 순수 계산)"""
    tot = sum(sym_counts.values())
    print(f"\n=== 비트 심볼 재고 (총 {tot:,}) ===")
    print(f"  {'심볼':<6}{'개수':>10}{'비율':>9}  {'AAMI':<5} {'현행 처리':<10} 99% 주장 시 CI")
    keep3 = {'N', 'L', 'R', 'e', 'j', 'A', 'a', 'J', 'S', 'V', 'E'}
    drop = 0
    for s, c in sorted(sym_counts.items(), key=lambda kv: -kv[1]):
        a = AAMI5.get(s)
        an = CLS5[a] if a is not None else "—"
        cur = "사용" if s in keep3 else "★버려짐"
        if s not in keep3:
            drop += c
        h = power_for_accuracy(c, target)
        hs = "측정불가" if not np.isfinite(h) else f"±{100*h:.2f}%"
        print(f"  {s:<6}{c:>10,}{100*c/max(tot,1):>8.2f}%  {an:<5} {cur:<10} {hs}")
    print(f"\n  현행 파이프라인이 버리는 비트: {drop:,} ({100*drop/max(tot,1):.2f}%)")

    print(f"\n=== AAMI 5-class 로 확장하면 ===")
    agg = {}
    for s, c in sym_counts.items():
        a = AAMI5.get(s)
        if a is not None:
            agg[a] = agg.get(a, 0) + c
    need = n_for_halfwidth(0.01, target)
    for a in range(5):
        c = agg.get(a, 0)
        h = power_for_accuracy(c, target)
        ok = "가능" if c >= need else f"불가(최소 {need:,} 필요)"
        hs = "—" if not np.isfinite(h) else f"±{100*h:.2f}%"
        print(f"  {CLS5[a]:<3} {c:>10,}   {target:.0%} 주장 CI {hs:>10}   {ok}")
    print(f"  ※ {target:.0%} 를 ±1%p 정밀도로 주장하려면 클래스당 {need:,}개 이상 필요.")
    print(f"     표본이 적은 클래스는 '{target:.0%} 달성'을 통계적으로 말할 수 없다.")

    if rhy_counts:
        print(f"\n=== 리듬(질병) 라벨 재고 — 지금 100% 버려지는 정보 ===")
        rt = sum(rhy_counts.values())
        print(f"  {'리듬':<10}{'비트수':>10}{'비율':>9}{'레코드':>8}   99% 주장 시 CI")
        for r, c in sorted(rhy_counts.items(), key=lambda kv: -kv[1]):
            nr = len((rhy_records or {}).get(r, []))
            h = power_for_accuracy(c, target)
            hs = "—" if not np.isfinite(h) else f"±{100*h:.2f}%"
            print(f"  {r:<10}{c:>10,}{100*c/max(rt,1):>8.2f}%{nr:>8}   {hs}")
        print(f"  ※ 레코드 수가 적은 리듬은 환자분리 평가에서 검정 불가"
              f"(HANDOFF §2 의 검정력 논리와 동일).")
    return dict(total=tot, dropped=drop, agg=agg)


# ─────────────────────────────────────────────────────────────────────────────
#  2. wfdb 래퍼 (Colab 실행용)
# ─────────────────────────────────────────────────────────────────────────────
def _ensure(pkg):
    import importlib, subprocess, sys
    try:
        importlib.import_module(pkg)
    except ModuleNotFoundError:
        subprocess.run([sys.executable, "-m", "pip", "install", "-q", pkg], check=True)


def _records(db="svdb"):
    _ensure("wfdb"); import wfdb
    try:
        return wfdb.get_record_list(db)
    except Exception:
        return [str(i) for i in range(800, 895)]


def _load_ann(rec, db="svdb", dldir=None):
    _ensure("wfdb"); import wfdb, os
    dldir = dldir or _DLDIR
    os.makedirs(dldir, exist_ok=True)
    for ext in ("hea", "atr"):
        fp = f"{dldir}/{rec}.{ext}"
        if os.path.exists(fp) and os.path.getsize(fp) > 0:
            continue
        for _ in range(3):
            try:
                wfdb.dl_files(db, dldir, [f"{rec}.{ext}"]); break
            except Exception:
                pass
    return wfdb.rdann(f"{dldir}/{rec}", "atr")


def label_audit(db="svdb", recs=None, dldir=None, n_rec=None, target=0.99, verbose=True):
    """전 레코드의 비트 심볼·리듬 라벨 전수 조사. 신호는 안 받으므로 빠르다(.atr만)."""
    recs = recs or _records(db)
    if n_rec:
        recs = recs[:n_rec]
    sym_counts, rhy_counts = {}, {}
    rhy_records, sym_records = {}, {}
    nonbeat = {}
    bad = []
    print(f"라벨 재고조사: {db}, {len(recs)}레코드 (.atr 만 읽음)")
    for ri, rec in enumerate(recs):
        try:
            ann = _load_ann(rec, db, dldir)
        except Exception as e:
            bad.append((rec, f"{type(e).__name__}")); continue
        sym = list(ann.symbol)
        samp = np.asarray(ann.sample)
        aux = list(getattr(ann, "aux_note", []) or [None] * len(sym))
        bmask = np.array([s in BEAT_SYMS for s in sym])
        for s in np.array(sym)[bmask]:
            sym_counts[s] = sym_counts.get(s, 0) + 1
            sym_records.setdefault(s, set()).add(rec)
        # ★비-비트 주석도 센다. svdb_prep 은 rr=np.diff(ann.sample) 로 '모든 주석'의
        #   간격을 RR 로 쓰므로, 비트 사이에 낀 비-비트 주석이 가짜 RR 을 만든다.
        #   rr_audit 이 센 '생리범위 밖 RR' 의 원인을 여기서 확인할 수 있다.
        for s in np.array(sym)[~bmask]:
            nonbeat[s] = nonbeat.get(s, 0) + 1
        rp = rhythm_per_beat(samp, sym, aux, samp[bmask])
        for r in rp:
            k = r or "(미상)"
            rhy_counts[k] = rhy_counts.get(k, 0) + 1
            rhy_records.setdefault(k, set()).add(rec)
        if verbose and ((ri + 1) % 20 == 0 or ri == len(recs) - 1):
            print(f"  {ri+1}/{len(recs)}  누적비트 {sum(sym_counts.values()):,}")
    if bad:
        print(f"  ⚠ 읽기 실패 {len(bad)}건: {bad[:5]}")
    out = summarize(sym_counts, rhy_counts, rhy_records, sym_records, target)
    if nonbeat:
        nb = sum(nonbeat.values())
        print(f"\n=== 비-비트 주석 (RR 오염의 원인 후보) ===")
        print(f"  총 {nb:,}개 — svdb_prep 의 np.diff(ann.sample) 는 이것들의 간격도 RR 로 쓴다")
        for s2, c in sorted(nonbeat.items(), key=lambda kv: -kv[1])[:12]:
            print(f"    '{s2}'  {c:,}")
        print(f"  → 비트 사이에 낀 것만큼 가짜 RR 이 생긴다. rr_audit 의 '생리범위 밖'과 대조할 것.")
        print(f"     svdb_labels.beat_only_rr() 는 비트 주석만 diff 하므로 이 오염이 없다.")
    else:
        print(f"\n  비-비트 주석 없음 → svdb_prep 의 RR 오염 가설은 이 DB 에서 기각.")
    out.update(nonbeat=nonbeat, sym_counts=sym_counts, rhy_counts=rhy_counts,
               rhy_records={k: sorted(v) for k, v in rhy_records.items()}, failed=bad)
    return out


def build_labeled(db="svdb", recs=None, dldir=None, n_rec=None, out=None,
                  realign=True, verbose=True):
    """svdb_data5.npz 생성 — 전 비트(5-class) + 리듬 라벨 + 오염 없는 RR.

    ★기존 svdb_data.npz 를 덮지 않는다. y3>=0 으로 거르면 기존 데이터셋이 재현된다.
    """
    _ensure("wfdb"); import wfdb, os
    from scipy.signal import resample_poly
    recs = recs or _records(db)
    if n_rec:
        recs = recs[:n_rec]
    dldir = dldir or _DLDIR
    os.makedirs(dldir, exist_ok=True)
    BEAT = []; Y5 = []; SYM = []; PID = []; PRE = []; POST = []; RHY = []; EDGE = []
    rnames = {}
    shifts = []
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
            print(f"  ✗ {rec}: {type(e).__name__} {e}"); continue
        if r.p_signal is None or r.p_signal.shape[1] < 2:
            print(f"  ✗ {rec}: 2리드 아님"); continue
        fs_src = int(getattr(r, "fs", _FS_SRC))
        sig = r.p_signal[:, :2].T
        if fs_src != _FS_DST:
            sig = np.stack([resample_poly(sig[c], _FS_DST, fs_src) for c in range(2)])
        scale = _FS_DST / fs_src
        samp = (np.asarray(ann.sample) * scale).astype(int)
        sym = list(ann.symbol)
        aux = list(getattr(ann, "aux_note", []) or [None] * len(sym))
        T = sig.shape[1]

        bmask = np.array([s in BEAT_SYMS for s in sym])
        bsamp = samp[bmask]; bsym = np.array(sym)[bmask]
        if realign:                                       # svdb_prep 과 동일한 R 재정합
            new = []
            for s in bsamp:
                w = int(_FS_DST * 50 / 1000.0)
                a, b = max(0, s - w), min(T, s + w + 1)
                if b - a < 3:
                    new.append(s); continue
                vm = np.sqrt(sig[0, a:b] ** 2 + sig[1, a:b] ** 2)
                new.append(a + int(np.argmax(vm)))
            new = np.array(new)
            shifts.append(float(np.mean(np.abs(new - bsamp)) / _FS_DST * 1000)); bsamp = new

        pre, post, edge = beat_only_rr(bsamp)              # ★비트만으로 RR
        rp = rhythm_per_beat(samp, sym, aux, bsamp)

        for i in range(len(bsamp)):
            lab = AAMI5.get(bsym[i])
            if lab is None:                                # BEAT_SYMS 이지만 AAMI 미정의
                continue
            R = int(bsamp[i]); a, b2 = R - _RPRE, R - _RPRE + _L
            if a < 0 or b2 > T:
                continue
            seg = sig[:, a:b2].astype("float32")
            seg = (seg - seg.mean(1, keepdims=True)) / (seg.std(1, keepdims=True) + 1e-6)
            nm = rp[i] or "(미상)"
            if nm not in rnames:
                rnames[nm] = len(rnames)
            BEAT.append(seg); Y5.append(lab); SYM.append(bsym[i]); PID.append(ri)
            PRE.append(pre[i]); POST.append(post[i]); RHY.append(rnames[nm]); EDGE.append(edge[i])
        if verbose and ((ri + 1) % 10 == 0 or ri == len(recs) - 1):
            print(f"  {ri+1}/{len(recs)}  누적비트 {len(BEAT):,}")

    BEAT = np.stack(BEAT); Y5 = np.array(Y5, np.int64); PID = np.array(PID, np.int64)
    Y3 = np.where(Y5 <= 2, Y5, -1).astype(np.int64)        # 기존 3-class 재현용
    out = out or f"{_BASE}/svdb_data5.npz"
    inv = [None] * len(rnames)
    for k, v in rnames.items():
        inv[v] = k
    np.savez(out, beat=BEAT, y5=Y5, y3=Y3, y=Y3, pid=PID,
             sym=np.array(SYM), pre_rr=np.array(PRE, "float32"),
             post_rr=np.array(POST, "float32"), rhythm=np.array(RHY, np.int64),
             rhythm_names=np.array(inv), rr_edge=np.array(EDGE, bool))
    print(f"\n✔ 저장 {out}   비트 {len(Y5):,}")
    for c in range(5):
        k = int((Y5 == c).sum())
        print(f"    {CLS5[c]} {k:>8,} ({100*k/max(len(Y5),1):.2f}%)")
    print(f"  리듬 라벨 {len(inv)}종: {inv}")
    if shifts:
        print(f"  R 재정합 평균 이동 {np.mean(shifts):.1f} ms")
    print(f"  ★기존 재현: y3>=0 으로 거르면 svdb_data.npz 와 같은 3-class 집합")
    print(f"  ★RR 은 비트 주석만으로 계산 → '+' 오염 없음(rr_edge=True 는 레코드 양끝)")
    return out


# ─────────────────────────────────────────────────────────────────────────────
#  3. 자기검증
# ─────────────────────────────────────────────────────────────────────────────
def selftest():
    ok = lambda c, m: (_ for _ in ()).throw(AssertionError(m)) if not c else print(f"  ✔ {m}")
    print("=== svdb_labels 자기검증 ===")

    # parse_rhythm
    ok(parse_rhythm("(AFIB\x00") == "AFIB", "aux_note 파싱 '(AFIB\\x00' → AFIB")
    ok(parse_rhythm("(N") == "N", "'(N' → N")
    ok(parse_rhythm("") is None and parse_rhythm(None) is None, "빈 aux → None")
    ok(parse_rhythm("some note") is None, "리듬 표기 아닌 aux → None")

    # rhythm_per_beat: '+' 마크가 비트 사이에 낀 실제 구조를 모사
    samp = [0,   10,  20,  30,  40,  50,  60]
    sym  = ["+", "N", "N", "+", "V", "V", "N"]
    aux  = ["(N", "",  "",  "(AFIB", "", "", ""]
    bpos = [10, 20, 40, 50, 60]
    rp = rhythm_per_beat(np.array(samp), sym, aux, bpos)
    ok(rp == ["N", "N", "AFIB", "AFIB", "AFIB"], f"리듬 forward-fill {rp}")
    rp2 = rhythm_per_beat(np.array([5, 10]), ["N", "N"], ["", ""], [5, 10])
    ok(rp2 == [None, None], "리듬 표기 없으면 None(지어내지 않음)")
    rp3 = rhythm_per_beat(np.array([0, 10, 20]), ["N", "+", "N"], ["", "(AFIB", ""], [0, 20])
    ok(rp3 == [None, "AFIB"], "첫 마크 이전 비트는 None")

    # beat_only_rr: '+' 오염이 없는지 — 핵심 검증
    #   비트가 100 간격, 그 사이에 '+' 주석이 끼어 있는 상황
    all_samp = np.array([0, 50, 100, 200, 300])          # 50 은 '+' (비트 아님)
    all_sym  = ["N", "+", "N", "N", "N"]
    bm = np.array([s in BEAT_SYMS for s in all_sym])
    pre, post, edge = beat_only_rr(all_samp[bm])
    ok(np.allclose(pre[1:], [100, 100, 100]), f"비트만 RR: pre={pre.tolist()} (100 균일)")
    ok(np.allclose(post[:-1], [100, 100, 100]), f"비트만 RR: post={post.tolist()}")
    # 기존 방식과 대조 — 오염이 실제로 발생함을 보인다
    old = np.diff(all_samp)                               # svdb_prep 방식
    ok(old[0] == 50, f"기존 방식은 '+' 때문에 RR=50 이라는 가짜 값 발생 (old={old.tolist()})")
    ok(edge[0] and edge[-1] and not edge[1:-1].any(), "양끝만 edge 플래그")

    # 단일 비트 / 빈 입력
    p, q, e = beat_only_rr(np.array([5]))
    ok(len(p) == 1 and np.isfinite(p[0]), "비트 1개도 안전")

    # AAMI5 커버리지
    ok(AAMI5['F'] == 3 and AAMI5['/'] == 4, "F→3, /→4 (기존에 버려지던 클래스)")
    old_map = {'N','L','R','e','j','A','a','J','S','V','E'}
    added = set(AAMI5) - old_map
    ok(added == {'F', '/', 'f', 'Q'}, f"되살린 심볼 {sorted(added)}")

    # 검정력 계산
    ok(n_for_halfwidth(0.01) == 381, f"99%±1%p 최소표본 {n_for_halfwidth(0.01)}")
    ok(power_for_accuracy(0) == float("inf"), "표본 0 → 측정불가")
    h = power_for_accuracy(10000)
    ok(abs(h - 1.96*np.sqrt(0.99*0.01/10000)) < 1e-12, f"CI 반폭 계산 ±{100*h:.3f}%")

    # summarize 가 죽지 않는지 (출력 경로 전체)
    summarize({'N': 90000, 'A': 2000, 'V': 7000, 'F': 800, '/': 12},
              {'N': 80000, 'AFIB': 15000, 'B': 200}, {'N': ['1'], 'AFIB': ['2'], 'B': ['3']})
    print("=== 전 항목 통과 ===")
    return True


if __name__ == "__main__":
    import sys
    if "--selftest" in sys.argv:
        selftest()
