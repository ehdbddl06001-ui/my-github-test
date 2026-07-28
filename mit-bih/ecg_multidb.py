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
#  ★.dat 를 안 받는 것이 핵심 실용 이득: afdb 23레코드 × 10시간 신호 = ~15GB /
#    ltafdb 84레코드 × 24시간 = 그 이상. 주석(.atr/.qrs)만 받으면 전부 수십 MB다.
#    대신 형태(morphology) 축은 이 코퍼스에서 못 쓴다 → 2층-B 는 mitdb 계열로만.
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
                     ("afib_rr.npz", "2층 RR 코퍼스")]:
        p = f"{b}/{fn}"
        if os.path.exists(p):
            print(f"    ✔ {fn:<18} {os.path.getsize(p)/1e6:>8.1f} MB  {what}")
        else:
            print(f"    · {fn:<18} {'—':>8}     {what} (아직 없음)")
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
    T = []; PRE = []; POST = []; EDGE = []; PID = []; DB = []; RHY = []; Y5 = []
    rnames = {}
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
             y5=np.array(Y5, np.int64))
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
#  5. 자기검증
# ─────────────────────────────────────────────────────────────────────────────
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
    print("=== 전 항목 통과 ===")
    return True


if __name__ == "__main__":
    import sys
    if "--selftest" in sys.argv:
        _here = os.path.dirname(os.path.abspath(__file__))
        exec(open(f"{_here}/svdb_labels.py").read(), globals())   # 의존 심볼 로드
        selftest()
