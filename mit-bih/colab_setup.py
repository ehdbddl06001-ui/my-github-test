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
    miss = [n for n in names if n not in g]
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


def _bootstrap_cell():
    print("  import urllib.request as u, json")
    print(f"  R=\"{REPO}\"; B=\"{BRANCH}\"")
    print("  S=json.load(u.urlopen(f\"https://api.github.com/repos/{R}/commits/"
          "{B.replace('/','%2F')}\"))[\"sha\"]")
    print("  exec(u.urlopen(f\"https://raw.githubusercontent.com/{R}/{S}/mit-bih/"
          "colab_setup.py\").read().decode())")
    print("  sync()")


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
    print("  ── 무엇이 없다고 나오면 이 셀을 통째로 다시 실행하세요 ──")
    _bootstrap_cell()
    print("  ※ NameError 가 의심되면 먼저: require('rr_audit_dbs','bench_afib')")
    return got


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
