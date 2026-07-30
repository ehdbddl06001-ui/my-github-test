# =============================================================================
#  colab_setup.py  —  GitHub → Drive 동기화 (긴 여정용 부트스트랩)
#
#  왜 필요한가: 코드는 GitHub 브랜치에 있고 Colab 은 Drive 를 본다. 둘이 어긋나면
#    · svdb_rhythm.py 가 Drive 에 없다        → NameError: attach_arms
#    · svdb_bench.py 가 옛 버전(레지스트리 없음) → RuntimeError: register_arm 없음
#  이 두 가지가 반복될 수밖에 없으므로, 한 셀로 끝내는 동기화 도구를 둔다.
#
#  ── Colab 첫 셀 (이것만 복사하면 됨) ─────────────────────────────────────────
#    import urllib.request as u, json
#    R="ehdbddl06001-ui/my-github-test"; B="claude/svdb-rhythm-sequence-model-h5t30u"
#    S=json.load(u.urlopen(f"https://api.github.com/repos/{R}/commits/{B.replace('/','%2F')}"))["sha"]
#    exec(u.urlopen(f"https://raw.githubusercontent.com/{R}/{S}/mit-bih/colab_setup.py").read().decode())
#    sync()          # 체인 파일까지 새로 받으려면 sync(chain=True)
#  ─────────────────────────────────────────────────────────────────────────────
#  ★셀 안에서 SHA 를 먼저 푸는 이유: raw 의 '브랜치 이름' URL 은 CDN 캐시 때문에
#    push 직후에도 옛 파일을 준다. 이 셀 자신이 그 함정에 빠지면 아무리 고쳐도
#    반영이 안 되므로, 부트스트랩 단계부터 SHA 로 고정한다(resolve_sha 주석 참조).
#
#  sync() 가 하는 일: 최신 파일 내려받기 → Drive 저장 → globals 로 로드 → 검증.
#  이후 바로:  rr_audit();  attach_arms();  OUT=bench_models(n_rep=1);  report(OUT)
#
#  코드를 고친 뒤에는 sync() 만 다시 돌리면 된다(런타임 재시작 불필요).
# =============================================================================
import os
import urllib.request

REPO   = "ehdbddl06001-ui/my-github-test"
BRANCH = "claude/svdb-rhythm-sequence-model-h5t30u"

# ★경고: colab_step6x/7x 레거시 파일들은 _BASE 를 자기 안에서 하드코딩한다
#   (`_BASE="/content/drive/MyDrive/mitbih"`). 따라서 base 를 다른 값으로 바꾸면
#   CORE 파일만 그 경로를 쓰고 체인은 여전히 Drive 를 본다 — 반쪽짜리가 된다.
#   기본값을 벗어나려면 레거시 파일들을 함께 고쳐야 한다. sync() 가 drift 를 경고한다.
_DEFAULT_BASE = "/content/drive/MyDrive/mitbih"
_BASE  = globals().get("_BASE", _DEFAULT_BASE)

# 리듬 시퀀스 모델 실행에 필요한 최소 집합(순서 = 로드 순서)
CORE = ["svdb_bench.py", "svdb_rhythm.py", "svdb_labels.py", "ecg_multidb.py",
        "rhythm_bench.py", "afib_bench.py"]
# B1~B4 기준선이 의존하는 체인. 이미 Drive 에 있으면 굳이 안 받아도 된다.
CHAIN = ["colab_step67_selfref.py", "colab_step68_oppoint.py",
         "colab_step69_ratepoint.py", "colab_step70_evalintegrity.py",
         "colab_step12_wst.py", "colab_step15_morpho.py", "colab_step18_repol.py",
         "colab_step49_rhythm2.py", "colab_step52_newfeats.py",
         "svdb_prep.py"]


def resolve_sha(branch=None, verbose=True):
    """브랜치 → 커밋 SHA.

    ★왜 SHA 를 쓰는가: raw.githubusercontent.com 의 '브랜치 이름' URL 은 CDN 캐시를
      타서 push 직후 몇 분간 **옛 파일**을 돌려준다(실측 확인). 쿼리스트링·no-cache
      헤더로도 우회되지 않는다. 반면 **SHA 로 고정한 raw URL 은 불변**이라 항상
      정확한 내용을 준다. 그래서 API 로 SHA 를 먼저 받고 그 SHA 로 파일을 받는다.
      덤으로 '어떤 코드가 이 수치를 냈는가'가 SHA 로 기록된다(연구 재현성).
    """
    import json
    import urllib.parse
    b = urllib.parse.quote(branch or BRANCH, safe="")
    url = f"https://api.github.com/repos/{REPO}/commits/{b}"
    try:
        req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json",
                                                   "Cache-Control": "no-cache"})
        with urllib.request.urlopen(req) as r:
            sha = json.load(r)["sha"]
        if verbose:
            print(f"  코드 버전 {sha[:10]}  ({branch or BRANCH})")
        return sha
    except Exception as e:
        print(f"  ⚠ SHA 조회 실패({type(e).__name__}) → 브랜치 URL 로 대체합니다.")
        print(f"    이 경우 CDN 캐시 때문에 방금 push 한 수정이 안 보일 수 있습니다"
              f"(몇 분 뒤 재시도).")
        return None


def _raw(fn, ref=None):
    """ref 는 SHA(권장) 또는 브랜치 이름."""
    return f"https://raw.githubusercontent.com/{REPO}/{ref or BRANCH}/mit-bih/{fn}"


def fetch(files=None, branch=None, base=None, verbose=True, ref=None):
    """GitHub 에서 내려받아 Drive 에 저장. 반환: 저장된 경로 리스트.
       ref 를 주면 그 SHA 로 고정해 받는다(캐시 문제 없음)."""
    base = base or _BASE
    files = files or CORE
    ref = ref or resolve_sha(branch, verbose=verbose) or (branch or BRANCH)
    os.makedirs(base, exist_ok=True)
    out = []
    for fn in files:
        url = _raw(fn, ref)
        try:
            req = urllib.request.Request(
                url, headers={"Cache-Control": "no-cache", "Pragma": "no-cache"})
            with urllib.request.urlopen(req) as r:
                body = r.read()
        except Exception as e:
            print(f"  ✗ {fn}: {type(e).__name__} {e}")
            print(f"    URL: {url}")
            continue
        # HTML(404 페이지)을 파이썬으로 저장하는 사고 방지
        if body[:20].lstrip().startswith(b"<"):
            print(f"  ✗ {fn}: 파이썬이 아닌 응답(브랜치/경로 확인) → 저장 안 함")
            continue
        p = f"{base}/{fn}"
        with open(p, "wb") as f:
            f.write(body)
        out.append(p)
        if verbose:
            print(f"  ↓ {fn}  {len(body):,} bytes")
    return out


def _defs(path):
    """파일의 최상위 공개 함수 이름들.

    ★왜 파싱하는가: 검증용 심볼 목록을 손으로 관리하면 새 파일을 추가할 때마다
      갱신을 잊고, 그러면 그 파일이 안 실렸는데도 '준비 완료'가 찍혀 NameError 가
      난다(실제로 attach_arms·db_audit·bench_transfer·rr_audit_dbs 에서 4번 발생).
      코드에서 목록을 유도하면 이 실수 자체가 불가능해진다.
    """
    import ast
    try:
        tree = ast.parse(open(path, encoding="utf-8").read())
    except Exception as e:
        print(f"  ⚠ {os.path.basename(path)} 파싱 실패({type(e).__name__}) — 검증 생략")
        return []
    return [n.name for n in tree.body
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
            and not n.name.startswith("_")]


def require(*names):
    """쓰려는 함수가 로드돼 있는지 먼저 확인한다. 없으면 어느 파일에서 오는지 알려준다.

    긴 실험을 돌리기 직전에 부르면, 30분 학습 뒤에 NameError 로 날리는 일이 없다.
    """
    g = globals()
    miss = []
    for n in names:                      # ★함수 이름 / 파일 이름 둘 다 받는다
        want, _ = _resolve_name(n, g)
        miss += [x for x in want if x not in g]
    miss = sorted(set(miss))
    if not miss:
        print(f"  ✔ {', '.join(names)} 준비됨")
        return True
    where = {}
    for fn in list(g.get("CORE", CORE)):
        p = f"{g.get('_BASE', _BASE)}/{fn}"
        if os.path.exists(p):
            for d in _defs(p):
                where.setdefault(d, fn)
    print("  ✗ 없는 함수:")
    for n in miss:
        print(f"      {n}()  ← {where.get(n, '(어느 파일인지 미상 — 최신 코드일 수 있음)')}")
    print("  → 아래 부트스트랩 셀을 통째로 다시 실행하세요.")
    _bootstrap_cell()
    return False


def code_version(verbose=True):
    """★메모리에 로드된 코드가 최신인지 확인한다(파일은 안 받는다).

    NameError 가 반복된 진짜 이유: **파일을 내려받아도 이미 메모리에 있는 정의는
    바뀌지 않는다.** 새 함수는 exec 를 다시 해야 생긴다. 그런데 부트스트랩 셀은
    노트북 위쪽에 있어 실험 셀만 다시 돌리기 쉽고, 그러면 옛 코드로 몇 십 분짜리
    작업을 다시 돌린 뒤에야 NameError 를 만난다(실제로 그렇게 됐다).
    그래서 '지금 뭐가 올라와 있는지'를 한 줄로 볼 수 있게 한다.
    """
    g = globals()
    cur = g.get("CODE_SHA")
    rem = resolve_sha(verbose=False)
    if verbose:
        print(f"  메모리에 로드된 코드: {str(cur)[:10] if cur else '(모름 — sync 를 한 적 없음)'}")
        print(f"  GitHub 최신        : {str(rem)[:10] if rem else '(조회 실패)'}")
    if cur and rem and cur != rem:
        print(f"\n  ⚠ 코드가 최신이 아닙니다. 아래 셀을 다시 실행하세요:")
        _bootstrap_cell()
        return False
    if verbose and cur and rem:
        print(f"  ✔ 최신입니다.")
    return bool(cur and rem and cur == rem)


def _resolve_name(n, g):
    """이름 하나를 '확인해야 할 함수 목록'으로 푼다.

    ★함수 이름과 **파일 이름**을 둘 다 받는다. 이게 없어서 실제로 막혔다:
      go("afib_bench") 를 안내했는데 afib_bench 는 파일이지 변수가 아니라서
      globals 에 영원히 안 생기고, sync 가 멀쩡히 끝났는데도 매번
      "아직 없는 함수: ['afib_bench']" 로 튕겼다. 이름이 파일이면 그 파일의
      공개 함수가 **전부** 로드됐는지로 판정하는 게 사용자가 의도한 뜻이다.

    반환: (확인할 이름들, 출처설명) — 파일로 해석되면 이름들이 그 파일의 공개 함수.
    """
    if n in g:
        return [n], None
    base = g.get("_BASE", _BASE)
    for cand in (n, f"{n}.py"):
        if cand.endswith(".py") and os.path.exists(f"{base}/{cand}"):
            d = _defs(f"{base}/{cand}")
            if d:
                return d, cand
    return [n], None


def go(*names):
    """★한 줄로 '최신 코드 확보 + 필요한 함수 존재 확인'.

    실험 셀 **맨 위에 이 한 줄만** 두면 순서를 틀릴 수가 없다:
        go('build_atrial_feats', 'atrial_audit')     # 함수 이름
        go('afib_bench')                             # 파일 이름도 됨
    없으면 알아서 최신을 받아 로드하고, 그래도 없으면 부트스트랩 셀을 찍는다.
    """
    if not code_version(verbose=False):
        print("  ↻ 코드가 최신이 아니라 동기화합니다…")
        sync(verbose=False)
    g = globals()
    miss, srcs = [], []
    for n in names:
        want, src = _resolve_name(n, g)
        gone = [x for x in want if x not in g]
        miss += gone
        if src and not gone:
            srcs.append(f"{n}({len(want)}개 함수)")
        elif not gone:
            srcs.append(n)
    if miss:
        print(f"  ✗ 아직 없는 함수: {sorted(set(miss))[:8]}")
        print(f"  → 아래 셀을 통째로 다시 실행하세요(메모리의 옛 정의는 그래야 바뀝니다):")
        _bootstrap_cell()
        raise RuntimeError(f"{sorted(set(miss))[:8]} 없음 — 위 부트스트랩 셀을 실행하세요.")
    print(f"  ✔ 최신 코드({str(g.get('CODE_SHA'))[:10]})로 {', '.join(srcs)} 준비됨")
    return True


def _bootstrap_cell(mount=True):
    """복구 셀을 그대로 찍는다. ★런타임이 끊기면 메모리의 정의가 전부 사라지므로
       Drive 마운트부터 다시 해야 한다 — 그래서 마운트 줄을 함께 넣는다."""
    if mount:
        print("  from google.colab import drive; drive.mount('/content/drive')")
    print("  import urllib.request as u, json")
    print(f"  R=\"{REPO}\"; B=\"{BRANCH}\"")
    print("  S=json.load(u.urlopen(f\"https://api.github.com/repos/{R}/commits/"
          "{B.replace('/','%2F')}\"))[\"sha\"]")
    print("  exec(u.urlopen(f\"https://raw.githubusercontent.com/{R}/{S}/mit-bih/"
          "colab_setup.py\").read().decode())")
    print("  sync(); cache_status()")


def sync(files=None, branch=None, base=None, load=True, chain=False, verbose=True,
         self_update=True):
    """내려받기 + 로드 + 검증. 이 함수 하나로 준비가 끝난다.

    ★self_update: colab_setup.py **자신을 먼저 갱신**한다.
      이게 없으면 새 파일을 CORE 에 추가해도 노트북 메모리의 옛 sync() 가 옛 목록을
      쓰기 때문에 그 파일이 영영 안 받아진다. 실제로 ecg_multidb.py 를 추가한 뒤
      sync() 가 3개만 받아 `NameError: db_audit` 이 났다. 그래서 자기 자신부터 받는다.
    """
    base = base or _BASE
    print(f"동기화: {REPO}@{branch or BRANCH} → {base}")
    if not os.path.isdir(base):
        print(f"  ⚠ {base} 없음 — Drive 마운트가 안 됐을 수 있습니다:")
        print(f"    from google.colab import drive; drive.mount('/content/drive')")
    ref = resolve_sha(branch, verbose=verbose)
    g0 = globals()
    if self_update and files is None:
        me = fetch(["colab_setup.py"], base=base, ref=ref, verbose=False)
        if me:
            try:
                exec(open(me[0]).read(), g0)        # CORE/CHAIN/need 목록이 최신이 됨
                if verbose and set(g0.get("CORE", CORE)) != set(CORE):
                    print(f"  ↻ 파일 목록 갱신: {sorted(set(g0['CORE']) - set(CORE))} 추가")
            except Exception as e:
                print(f"  ⚠ colab_setup 자기갱신 실패({type(e).__name__}) — 옛 목록으로 진행")
    files = list(files or g0.get("CORE", CORE))
    if chain:
        files = list(g0.get("CHAIN", CHAIN)) + files   # 체인 먼저, 그 다음 CORE
    got = fetch(files, branch=branch, base=base, verbose=verbose, ref=ref)
    if not load:
        return got

    g = globals()
    g["_BASE"] = base                                # 이후 모든 스크립트가 이 경로를 씀
    g["CODE_SHA"] = ref                              # 실험 기록용: 이 수치를 낸 코드 버전
    for p in got:
        try:
            exec(open(p).read(), g)
        except Exception as e:
            print(f"  ✗ 로드 실패 {os.path.basename(p)}: {type(e).__name__}: {e}")

    # _BASE drift — 레거시 파일이 자기 경로로 되덮었는지 확인
    if g.get("_BASE") != base:
        print(f"  ⚠ _BASE 가 '{g.get('_BASE')}' 로 되덮였습니다(레거시 파일의 하드코딩).")
        print(f"    요청한 base='{base}' 는 CORE 파일 저장에만 적용됩니다.")

    # ── 검증 ────────────────────────────────────────────────────────────────
    # ★손으로 관리하는 심볼 목록을 쓰지 않는다. 예전엔 need={...} 를 직접 적어
    #   뒀는데, 새 파일(afib_bench.py)을 추가하고 그 목록을 갱신하지 않으면
    #   그 파일이 안 실렸는데도 '준비 완료'가 찍혔다 → NameError 가 반복됐다.
    #   대신 **받은 파일을 파싱해 최상위 공개 함수를 뽑아** globals 와 대조한다.
    #   목록이 코드에서 유도되므로 파일을 아무리 추가해도 다시 어긋나지 않는다.
    print()
    bad = []
    owner = {}                       # 심볼 → 먼저 정의한 파일
    clash = []
    for p in got:
        fn = os.path.basename(p)
        want = _defs(p)
        if not want:
            continue
        gone = [n for n in want if n not in g]
        if gone:
            bad.append((fn, gone))
            print(f"  ✗ {fn}: 공개 함수 {len(gone)}/{len(want)}개 누락 → {gone[:6]}")
        elif verbose:
            print(f"  ✔ {fn}: 공개 함수 {len(want)}개 로드")
        # ★이름 충돌 검사 — CORE 는 **같은 globals** 로 순서대로 exec 되므로
        #   같은 이름이 두 파일에 있으면 나중 파일이 조용히 덮어쓴다. 예외도
        #   에러도 안 나고 "그 함수가 다른 일을 하기 시작"할 뿐이라 가장 찾기 어렵다.
        #   (실제로 afib_bench 의 register_arm 이 svdb_bench 의 것을 덮어써서
        #    attach_arms 가 1층 arm 을 2층 레지스트리에 넣을 뻔했다.)
        for n in want:
            if n in owner and n != "selftest":
                clash.append((n, owner[n], fn))
            owner[n] = fn
    if clash:
        print(f"\n  ⚠ 이름 충돌 {len(clash)}건 — 나중 파일이 앞 파일을 덮어씁니다:")
        for n, a, b in clash:
            print(f"      {n}()  {a} → {b}")
        print(f"    한쪽 이름을 바꿔야 합니다(예: register_arm → register_afib_arm).")
    if bad:
        print(f"\n  → 위 파일의 로드가 실패했습니다. 바로 위의 '✗ 로드 실패' 줄에"
              f" 원인이 있습니다.\n    없으면 {base} 의 파일 내용을 확인하세요.")
    else:
        print("\n  ✔ 준비 완료.  다음 순서로 실행하세요:")
        print("      cache_status()                # Drive 에 이미 뭐가 있는지 (다운로드 전 확인)")
        print("      # ★2층(리듬·질환축) — 지금 여기:")
        print("      rr_audit_dbs()                # 리듬별 환자수·MDE (신호 안 받음, 수 분)")
        print("      build_rr_corpus(dbs=('afdb','mitdb'))   # 먼저 작게 배관 검증")
        print("      d = load_rr(); w = make_windows(d, W=128)")
        print("      OUT = bench_afib(w, k=3); report_afib(OUT)")
        print("      ※ make_windows 의 [검정력] 표가 '★불가'면 모델을 돌리지 말고")
        print("         ltafdb 를 먼저 넣으세요 (LAYER2_AFIB.md §1).")
        print()
        print("      # 1층(비트) 결과를 다시 보려면(학습 0초):")
        print("      OUT = load_out('rsn_adathr_rep3'); report(OUT)")
        print()
        print("      # ★새 arm 만 돌릴 때 — 기준선·기존 arm 재학습 금지(시간 낭비):")
        print("      OLD = load_out('rsn_adathr_rep3')")
        print("      attach_arms(which=('R8',))")
        print("      NEW = bench_models(n_rep=3, only=['R8...'])")
        print("      OUT = merge_out(NEW, OLD); save_out(OUT, 'next'); report(OUT)")
        if g.get("CODE_SHA"): print(f"    (실험 기록용 코드 버전: CODE_SHA={g['CODE_SHA'][:10]})")
    # ★새 파일이 CORE 에 추가되면 메모리의 옛 sync() 는 그걸 모른다. self_update 가
    #   그걸 막지만, self_update 자체가 없던 버전에서 넘어올 때는 한 번은 아래 셀이
    #   필요하다. 매번 보여줘서 "sync() 만 하면 되겠지"로 막히는 일을 없앤다.
    print()
    print(f"  ┏━ 지금 메모리에 올라온 코드 버전: {str(ref)[:10] if ref else '(미상)'}")
    print(f"  ┗━ ★실험 셀 맨 위에 go(...) 한 줄을 두면 순서를 틀릴 수 없습니다:")
    print(f"       go('build_atrial_feats', 'atrial_audit')")
    print("  ── 그래도 없다고 나오면 이 셀을 통째로 다시 실행 ──")
    _bootstrap_cell()
    return got


def mem_report(top=12, verbose=True):
    """★지금 RAM 을 뭐가 먹고 있는지 — "왜 런타임이 죽었나" 에 대한 답.

    Colab 무료 티어는 약 12.7GB 다. 이 프로젝트에서 실제로 큰 것은:
      · afib_rr.npz 의 db 열   12M개 문자열 배열 = **386MB** (한 번 복사하면 두 배)
      · w["seq"]               창 80,602 × 4 × 128 float32 = 165MB
      · torch 사본             _fit_win 의 X = torch.tensor(w["seq"]) = +165MB
    여기에 `np.array(list(map(str, dbv)))` 같은 한 줄이 12M개 파이썬 str 객체
    (≈700MB)를 만들면 순식간에 넘친다 — 실제로 그렇게 죽었다.
    """
    g = globals()
    import gc
    rows = []
    for k, v in list(g.items()):
        if k.startswith("_") or k in ("In", "Out"):
            continue
        try:
            if isinstance(v, dict):
                nb = sum(getattr(x, "nbytes", 0) for x in v.values()
                         if hasattr(x, "nbytes"))
                if nb:
                    rows.append((k, nb, f"dict({len(v)}키)"))
            elif hasattr(v, "nbytes"):
                rows.append((k, int(v.nbytes), type(v).__name__))
        except Exception:
            pass
    rows.sort(key=lambda r: -r[1])
    tot_os = None
    try:
        import psutil
        pm = psutil.Process().memory_info().rss / 1e9
        vm = psutil.virtual_memory()
        tot_os = (pm, vm.total / 1e9, vm.available / 1e9)
    except Exception:
        pass
    if verbose:
        print("\n=== RAM 현황 ===")
        if tot_os:
            print(f"  이 프로세스 {tot_os[0]:.2f} GB / 전체 {tot_os[1]:.1f} GB "
                  f"(남음 {tot_os[2]:.2f} GB)")
        else:
            print("  (psutil 없음 — 전체 사용량은 못 봄. pip install psutil)")
        print(f"  {'이름':<22}{'크기':>10}   종류")
        for k, nb, t in rows[:top]:
            print(f"  {k:<22}{nb/1e6:>9.1f}MB   {t}")
        s = sum(r[1] for r in rows)
        print(f"  {'(합계)':<22}{s/1e6:>9.1f}MB  ← globals 의 배열만. "
              f"torch 사본·순간할당은 안 잡힌다")
        print(f"\n  ▸ 정리:  free_big('d')  또는  free_big('d','w','OUT')")
        print(f"  ▸ 코퍼스는 파일에 있으니 필요할 때 다시 load_rr() 하면 된다")
    gc.collect()
    return rows


def free_big(*names, verbose=True):
    """큰 객체를 globals 에서 지우고 gc 를 돌린다.

    ★del 만으로는 안 줄어드는 경우가 있다: 노트북의 `Out[...]`·`_`·`__` 가 옛 값을
      붙잡고 있으면 참조가 남는다. 그래서 그것들도 함께 비운다.
    """
    import gc
    g = globals()
    freed = 0
    for n in names:
        v = g.pop(n, None)
        if v is not None:
            freed += (sum(getattr(x, "nbytes", 0) for x in v.values()
                          if hasattr(x, "nbytes")) if isinstance(v, dict)
                      else getattr(v, "nbytes", 0))
    for n in ("_", "__", "___"):
        if n in g:
            g[n] = None
    try:                                    # IPython 의 출력 캐시가 최대 용의자다
        ip = g.get("get_ipython", lambda: None)()
        if ip is not None:
            ip.user_ns.get("Out", {}).clear()
    except Exception:
        pass
    gc.collect()
    if verbose:
        print(f"  ✔ {', '.join(names)} 해제 (배열 {freed/1e6:.0f}MB) + 출력캐시 비움")
    return freed


def which():
    """지금 globals 에 무엇이 로드돼 있는지 점검(NameError 원인 추적용)."""
    g = globals()
    for k, src in [("bench_models", "svdb_bench.py"), ("register_arm", "svdb_bench.py"),
                   ("attach_arms", "svdb_rhythm.py"), ("rr_audit", "svdb_rhythm.py"),
                   ("report", "svdb_rhythm.py"), ("patient_breakdown", "svdb_rhythm.py"),
                   ("robust_template", "colab_step67_selfref.py"),
                   ("_best_t_f1", "colab_step68_oppoint.py")]:
        print(f"  {'✔' if k in g else '✗'} {k:20s} ← {src}")
    print(f"  _BASE = {g.get('_BASE')}")
