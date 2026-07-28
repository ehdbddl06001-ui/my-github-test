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
    dldir = dldir or "/content/incart_raw"
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
                realign=True, patient_map=None, verbose=True):
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
        dldir = f"/content/{db}_raw"; os.makedirs(dldir, exist_ok=True)
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
#  4. 자기검증
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
    print("=== 전 항목 통과 ===")
    return True


if __name__ == "__main__":
    import sys
    if "--selftest" in sys.argv:
        _here = os.path.dirname(os.path.abspath(__file__))
        exec(open(f"{_here}/svdb_labels.py").read(), globals())   # 의존 심볼 로드
        selftest()
