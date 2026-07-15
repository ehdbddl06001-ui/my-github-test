"""
fetch_project.py — AI랩 실습에서 '분석 대상 공개 저장소(오픈소스)'를 결정론적으로 받아오는 유틸.

MedKOS 원칙: 결정론은 코드가 맡는다. 어떤 공개 저장소를, 어느 브랜치/커밋으로, 어디에 받을지는
LLM이 아니라 이 레지스트리(PROJECTS)가 정한다. 카드(content/ailab/*.md)는 그 코드를 '해석'만 한다.

왜 clone(복제)이고 vendor(복사 커밋)가 아닌가:
  대상 저장소 상당수가 GPL 등 copyleft 라이선스라, 소스를 이 repo에 복사·커밋하면 라이선스가
  전염된다. 그래서 코드는 '받아서 읽을' 뿐 커밋하지 않는다(기본 대상 디렉토리 projects/ 는
  .gitignore). 이 유틸은 그 '받기'를 재현 가능하게 만든다(어느 저장소·어느 ref 인지 고정).

사용:
  python pipelines/fetch_project.py --list
  python pipelines/fetch_project.py --download ptbxl-benchmark
  python pipelines/fetch_project.py --download ptbxl-benchmark --dest /content/oss --ref <commit>
  python pipelines/fetch_project.py --selftest      # 네트워크 없이 레지스트리 무결성 검사
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
# 받은 오픈소스가 놓이는 기본 위치. 커밋하지 않는다(.gitignore).
DEFAULT_DEST = ROOT / "projects"

# ── 공개 프로젝트 레지스트리(사실 목록) ──────────────────────────────────────
# 각 항목은 사실(fact)이다. 링크·라이선스·핵심 파일이 바뀌면 여기만 고치면
# 카드/노트북이 함께 정합성을 유지한다(파생물이므로).
PROJECTS: list[dict] = [
    {
        "key": "ptbxl-benchmark",
        "name": "PTB-XL Deep Learning Benchmark (ecg_ptbxl_benchmarking)",
        "week": 2,
        "repo": "https://github.com/helme/ecg_ptbxl_benchmarking.git",
        "ref": "master",                 # 재현성을 원하면 --ref <commit-sha> 로 고정
        "license": "GPL-3.0",            # ⚠️ copyleft — repo 에 복사·커밋하지 말 것
        "modality": "ecg",
        "dataset": "ptb-xl",
        "paper": "Strodthoff et al., Deep Learning for ECG Analysis: "
                 "Benchmarks and Insights from PTB-XL, IEEE JBHI 25(5):1519-1528, 2021",
        "key_files": [
            ("code/models/resnet1d.py", "ResNet1d·BasicBlock1d·Bottleneck1d·resnet1d_wang 정의"),
            ("code/experiments/scp_experiment.py", "SCP_Experiment.perform() — 학습·예측·저장"),
            ("code/utils/utils.py", "evaluate_experiment() — macro-AUROC·임계값 탐색"),
            ("code/reproduce_results.py", "논문 전체 실험 재현 진입점"),
            ("get_datasets.sh", "PTB-XL·ICBEB 데이터 내려받기 스크립트"),
        ],
        "note": "2주차(ailab-2026-0012·0013)의 레퍼런스. GPL 이므로 받아서 '읽기'만 한다.",
    },
]

_BY_KEY = {p["key"]: p for p in PROJECTS}
_REQUIRED = ("key", "name", "repo", "ref", "license", "key_files")


def get_project(key: str) -> dict:
    if key not in _BY_KEY:
        raise KeyError(
            f"알 수 없는 프로젝트 key: {key!r}. "
            f"가능한 값: {', '.join(sorted(_BY_KEY))}"
        )
    return _BY_KEY[key]


def _print_list() -> None:
    print("── 받을 수 있는 공개 프로젝트(오픈소스) ─────────────────────")
    for p in PROJECTS:
        wk = f"{p['week']}주차" if p.get("week") else "-"
        print(f"\n  🔑 {p['key']}   ({wk} · {p['license']})")
        print(f"     {p['name']}")
        print(f"     ↳ {p['repo']}  @ {p['ref']}")
        if p.get("paper"):
            print(f"     📄 {p['paper']}")
        print("     주요 파일:")
        for rel, desc in p["key_files"]:
            print(f"        - {rel:<40} {desc}")
    print("\n받기: python pipelines/fetch_project.py --download <key> [--ref <commit>] [--dest <경로>]")


def download(key: str, dest: Path | None = None, ref: str | None = None,
             force: bool = False) -> Path:
    """지정한 프로젝트를 dest 아래로 git clone 한다(얕은 복제 + ref 체크아웃).

    반환: 받은 저장소의 로컬 경로. 코드는 커밋하지 않는다(읽기 전용 참고).
    """
    proj = get_project(key)
    ref = ref or proj["ref"]
    dest = Path(dest) if dest else DEFAULT_DEST
    repo_dirname = proj["repo"].rstrip("/").split("/")[-1]
    if repo_dirname.endswith(".git"):
        repo_dirname = repo_dirname[:-4]
    target = dest / repo_dirname

    if target.exists():
        if force:
            shutil.rmtree(target)
        else:
            print(f"이미 존재합니다: {target}  (다시 받으려면 --force)")
            _print_keyfiles(proj, target)
            return target

    dest.mkdir(parents=True, exist_ok=True)
    print(f"▶ clone: {proj['repo']}  →  {target}")
    # 얕은 복제 후 원하는 ref 로 체크아웃(브랜치명·태그·커밋 모두 대응).
    subprocess.run(
        ["git", "clone", "--filter=blob:none", proj["repo"], str(target)],
        check=True,
    )
    try:
        subprocess.run(["git", "-C", str(target), "checkout", ref], check=True)
    except subprocess.CalledProcessError:
        print(f"⚠️ ref '{ref}' 체크아웃 실패 — 기본 브랜치 그대로 둡니다.", file=sys.stderr)

    print(f"✅ 완료: {target}   (라이선스: {proj['license']} — repo 에 복사·커밋하지 마세요)")
    _print_keyfiles(proj, target)
    return target


def _print_keyfiles(proj: dict, target: Path) -> None:
    print("   먼저 읽어볼 파일:")
    for rel, desc in proj["key_files"]:
        exists = "✓" if (target / rel).exists() else "·"
        print(f"     {exists} {target / rel}   ({desc})")


def selftest() -> int:
    """네트워크 없이 레지스트리 무결성만 검사(회귀 테스트용)."""
    seen: set[str] = set()
    for p in PROJECTS:
        for field in _REQUIRED:
            assert p.get(field), f"{p.get('key')}: 필수 필드 누락 → {field}"
        assert p["key"] not in seen, f"중복 key: {p['key']}"
        seen.add(p["key"])
        assert p["repo"].startswith("http"), f"{p['key']}: repo 는 URL 이어야 함"
        assert isinstance(p["key_files"], list) and p["key_files"], \
            f"{p['key']}: key_files 는 비어있지 않은 리스트여야 함"
        for item in p["key_files"]:
            assert isinstance(item, tuple) and len(item) == 2, \
                f"{p['key']}: key_files 항목은 (경로, 설명) 튜플이어야 함"
    print(f"✅ selftest 통과 — 프로젝트 {len(PROJECTS)}개, key 유일성·필수필드 OK")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="AI랩 공개 프로젝트(오픈소스) 받기")
    ap.add_argument("--list", action="store_true", help="받을 수 있는 프로젝트 목록")
    ap.add_argument("--download", metavar="KEY", help="해당 key 프로젝트를 clone")
    ap.add_argument("--dest", help=f"받을 위치(기본: {DEFAULT_DEST.relative_to(ROOT)}/)")
    ap.add_argument("--ref", help="브랜치/태그/커밋(재현성 위해 커밋 고정 권장)")
    ap.add_argument("--force", action="store_true", help="이미 있으면 지우고 다시 받기")
    ap.add_argument("--selftest", action="store_true", help="네트워크 없이 레지스트리 검사")
    args = ap.parse_args()

    if args.selftest:
        return selftest()
    if args.list or not args.download:
        _print_list()
        return 0
    download(args.download, dest=args.dest, ref=args.ref, force=args.force)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
