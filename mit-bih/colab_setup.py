# =============================================================================
#  colab_setup.py  —  GitHub → Drive 동기화 (긴 여정용 부트스트랩)
#
#  왜 필요한가: 코드는 GitHub 브랜치에 있고 Colab 은 Drive 를 본다. 둘이 어긋나면
#    · svdb_rhythm.py 가 Drive 에 없다        → NameError: attach_arms
#    · svdb_bench.py 가 옛 버전(레지스트리 없음) → RuntimeError: register_arm 없음
#  이 두 가지가 반복될 수밖에 없으므로, 한 셀로 끝내는 동기화 도구를 둔다.
#
#  ── Colab 첫 셀 (이것만 복사하면 됨) ─────────────────────────────────────────
#    import urllib.request as _u
#    _B="claude/svdb-rhythm-sequence-model-h5t30u"
#    exec(_u.urlopen(f"https://raw.githubusercontent.com/ehdbddl06001-ui/"
#                    f"my-github-test/{_B}/mit-bih/colab_setup.py").read().decode())
#    sync()
#  ─────────────────────────────────────────────────────────────────────────────
#
#  sync() 가 하는 일: 최신 파일 내려받기 → Drive 저장 → globals 로 로드 → 검증.
#  이후 바로:  rr_audit();  attach_arms();  OUT=bench_models(n_rep=1);  report(OUT)
#
#  코드를 고친 뒤에는 sync() 만 다시 돌리면 된다(런타임 재시작 불필요).
# =============================================================================
import os
import time
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
CORE = ["svdb_bench.py", "svdb_rhythm.py"]
# B1~B4 기준선이 의존하는 체인. 이미 Drive 에 있으면 굳이 안 받아도 된다.
CHAIN = ["colab_step67_selfref.py", "colab_step68_oppoint.py",
         "colab_step69_ratepoint.py", "colab_step70_evalintegrity.py",
         "colab_step12_wst.py", "colab_step15_morpho.py", "colab_step18_repol.py",
         "colab_step49_rhythm2.py", "colab_step52_newfeats.py",
         "svdb_prep.py"]


def _raw(fn, branch=None, bust=True):
    """raw.githubusercontent.com URL.

    ★캐시 우회가 필수인 이유: raw 는 CDN 캐시를 두어서, push 직후 몇 분간 **옛 파일**을
      돌려준다. 코드를 고치고 곧바로 sync() 하는 반복 작업에서 이걸 모르면
      "고쳤는데 왜 그대로지?" 로 시간을 버린다. 쿼리스트링으로 캐시를 우회한다.
    """
    u = f"https://raw.githubusercontent.com/{REPO}/{branch or BRANCH}/mit-bih/{fn}"
    return f"{u}?_={int(time.time())}" if bust else u


def fetch(files=None, branch=None, base=None, verbose=True):
    """GitHub 에서 내려받아 Drive 에 저장. 반환: 저장된 경로 리스트."""
    base = base or _BASE
    files = files or CORE
    os.makedirs(base, exist_ok=True)
    out = []
    for fn in files:
        url = _raw(fn, branch)
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


def sync(files=None, branch=None, base=None, load=True, chain=False, verbose=True):
    """내려받기 + 로드 + 검증. 이 함수 하나로 준비가 끝난다."""
    base = base or _BASE
    files = list(files or CORE)
    if chain:
        files = CHAIN + files                       # 체인 먼저, 그 다음 CORE
    print(f"동기화: {REPO}@{branch or BRANCH} → {base}")
    if not os.path.isdir(base):
        print(f"  ⚠ {base} 없음 — Drive 마운트가 안 됐을 수 있습니다:")
        print(f"    from google.colab import drive; drive.mount('/content/drive')")
    got = fetch(files, branch=branch, base=base, verbose=verbose)
    if not load:
        return got

    g = globals()
    g["_BASE"] = base                                # 이후 모든 스크립트가 이 경로를 씀
    for p in got:
        try:
            exec(open(p).read(), g)
        except Exception as e:
            print(f"  ✗ 로드 실패 {os.path.basename(p)}: {type(e).__name__}: {e}")

    # _BASE drift — 레거시 파일이 자기 경로로 되덮었는지 확인
    if g.get("_BASE") != base:
        print(f"  ⚠ _BASE 가 '{g.get('_BASE')}' 로 되덮였습니다(레거시 파일의 하드코딩).")
        print(f"    요청한 base='{base}' 는 CORE 파일 저장에만 적용됩니다.")

    # 검증 — 무엇이 준비됐는지 이름으로 확인한다
    need = {"register_arm": "svdb_bench.py (arm 레지스트리)",
            "bench_models": "svdb_bench.py",
            "attach_arms":  "svdb_rhythm.py",
            "rr_audit":     "svdb_rhythm.py",
            "report":       "svdb_rhythm.py",
            "patient_breakdown": "svdb_rhythm.py"}
    miss = {k: v for k, v in need.items() if k not in g}
    print()
    if miss:
        print("  ✗ 준비 안 됨:")
        for k, v in miss.items():
            print(f"      {k}()  ← {v}")
        print(f"    → sync(chain=True) 를 시도하거나 {base} 의 파일을 확인하세요.")
    else:
        print("  ✔ 준비 완료.  다음 순서로 실행하세요:")
        print("      rr_audit()                    # RR 위생 점검(먼저)")
        print("      attach_arms()                 # R0/R1/R2 등록")
        print("      OUT = bench_models(n_rep=1)   # 벤치(GPU, 수십 분)")
        print("      report(OUT)                   # 판정 + 환자별 분해")
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
