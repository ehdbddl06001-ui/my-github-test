#!/usr/bin/env python3
"""publish.py — 만든 자료를 **한 명령으로** 검증·재색인·병합·푸시한다(결정론).

왜 필요한가: '커밋 전 필수 순서'(CLAUDE.md)가 다섯 단계인데 루틴이 한 단계라도
빠뜨리면 조용히 어긋난다 — 번들을 안 만들면 홈페이지가 안 바뀌고, main 을 안 당기면
푸시가 막히고, PR 을 열어 두고 끝내면 그날 자료가 영영 main 에 안 올라간다
(2026-08-17 실측: 루틴이 만든 서브노트 생성기가 병합되지 않아 다음 날 루틴이 같은
파일을 처음부터 다시 만들었다).

기본 동작은 **main 직접 푸시**다. 대신 아무거나 못 올리게 경로를 검사한다:

  자동 병합 허용(content lane)  content/** · docs/** · notebooks/** ·
                                state/ailab_progress.json · .private 제외
  사람 검토 필요(code lane)     pipelines/** · .claude/** · CLAUDE.md ·
                                .github/** · schemas/** · 그 밖 전부

코드 레인이 섞여 있으면 **거부하고** 브랜치+PR 을 쓰라고 알린다. 매일 도는 루틴은
콘텐츠만 만들므로 늘 통과하고, 파이프라인을 고치는 작업은 사람이 보게 된다.

사용:
  python pipelines/publish.py -m "커밋 메시지"          # 검증→번들→main 푸시
  python pipelines/publish.py -m "..." --dry-run        # 무엇을 할지만
  python pipelines/publish.py -m "..." --branch claude/x  # 브랜치로(코드 변경용)
  python pipelines/publish.py --selftest
"""
from __future__ import annotations

import argparse
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# 콘텐츠 레인 — 결정론 파이프라인이 만들고 테스트가 지키는 산출물만.
CONTENT_PREFIXES = ("content/", "docs/", "notebooks/", "research/")
CONTENT_FILES = ("state/ailab_progress.json",)

# 번들 재생성 순서(색인 → 각 뷰). 하나라도 빠지면 홈페이지가 낡는다.
BUNDLES = [
    "indexer.py", "export_anatomy_web.py", "export_search_web.py",
    "export_diagrams_web.py", "export_kmle_web.py", "export_usmle_web.py",
    "export_papers_web.py", "export_ailab_web.py",
]


def classify(paths: list[str]) -> tuple[list[str], list[str]]:
    """(콘텐츠 레인, 코드 레인) 으로 가른다."""
    content, code = [], []
    for p in paths:
        if p in CONTENT_FILES or p.startswith(CONTENT_PREFIXES):
            content.append(p)
        else:
            code.append(p)
    return content, code


def _run(cmd: list[str], **kw) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, **kw)


def changed_paths() -> list[str]:
    r = _run(["git", "status", "--porcelain"])
    out = []
    for ln in r.stdout.splitlines():
        p = ln[3:].strip()
        if " -> " in p:            # 이름 변경
            p = p.split(" -> ")[1]
        if p:
            out.append(p.strip('"'))
    return out


def push_with_backoff(branch: str, dry: bool) -> bool:
    """네트워크 실패만 재시도한다(2·4·8·16초). 거절(non-fast-forward)은 즉시 실패."""
    for i, wait in enumerate((2, 4, 8, 16, 0)):
        if dry:
            print(f"  [dry] git push -u origin {branch}")
            return True
        r = _run(["git", "push", "-u", "origin", branch])
        if r.returncode == 0:
            print(r.stderr.strip().splitlines()[-1] if r.stderr.strip() else "pushed")
            return True
        err = (r.stderr or "").lower()
        if "rejected" in err or "non-fast-forward" in err:
            print(f"  푸시 거절 — 먼저 main 을 병합해야 한다:\n{r.stderr}")
            return False
        if not wait:
            print(f"  푸시 실패:\n{r.stderr}")
            return False
        print(f"  푸시 실패({i + 1}회) — {wait}초 뒤 재시도")
        time.sleep(wait)
    return False


def question_paths(content: list[str]) -> list[str]:
    """문항(kmle/usmle) 경로만 추린다."""
    return [p for p in content
            if p.startswith("content/kmle/") or p.startswith("content/usmle/")]


def blocks_question_branch(content: list[str], code: list[str], branch: str,
                           allow_question_branch: bool) -> list[str]:
    """문항을 브랜치로 빼려는 시도인가? 막아야 할 문항 경로를 돌려준다(없으면 빈 리스트).

    문항 PR 은 병합이 늦으면 `next_id()` 가 그 문항을 못 본다(ID 는 저장된 content 에서
    계산한다) → 다음 날 루틴이 **같은 ID 를 재발급**한다. 2026-07~08 에 PR
    #32·#33·#35·#36·#38·#39 가 전부 `usmle-2026-0049~0054` 를 만들었고, 그 사이 main 이
    같은 ID 를 다른 문항으로 채워 6건 모두 병합 불가가 됐다(문항만 새 ID 로 이식해 구제).
    코드가 섞여 있으면 코드 레인 규칙(사람 검토)이 우선이므로 여기서는 막지 않는다.
    """
    if branch == "main" or code or allow_question_branch:
        return []
    return question_paths(content)


def publish(message: str, branch: str, dry: bool, allow_code: bool,
            allow_question_branch: bool = False) -> int:
    paths = changed_paths()
    if not paths:
        print("변경 없음 — 할 일 없음.")
        return 0
    content, code = classify(paths)
    print(f"변경 {len(paths)}건 — 콘텐츠 {len(content)} · 코드 {len(code)}")
    if code and branch == "main" and not allow_code:
        print("\n코드 레인이 섞여 있어 main 직접 푸시를 거부한다:")
        for p in code[:12]:
            print(f"  - {p}")
        if len(code) > 12:
            print(f"  … 외 {len(code) - 12}건")
        print("\n→ `--branch claude/<작업>` 으로 올리고 PR 을 연 뒤, 테스트를 확인하고"
              " **같은 세션에서 병합**한다. 열어 두고 끝내지 않는다.")
        return 2

    # 반대 방향 가드: 순수 문항을 브랜치로 빼는 것을 막는다(사유는 함수 주석).
    questions = blocks_question_branch(content, code, branch, allow_question_branch)
    if questions:
        print(f"\n문항({len(questions)}건)만 바뀌었는데 브랜치 '{branch}' 로 올리려 한다 — 거부한다:")
        for p in questions[:8]:
            print(f"  - {p}")
        if len(questions) > 8:
            print(f"  … 외 {len(questions) - 8}건")
        print("\n문항 PR 은 병합이 늦으면 next_id 가 같은 ID 를 재발급해 충돌을 만든다"
              "(2026-07~08 실측: PR 6건이 같은 usmle-2026-0049~0054 를 생성).")
        print("→ `--branch main`(기본값)으로 올려 즉시 홈페이지에 반영한다.")
        print("→ 정말 브랜치로 올려야 하면 `--allow-question-branch` 를 붙이고,"
              " **같은 세션에서 병합**한다.")
        return 2

    # 1) frontmatter 검증 — 실패하면 아무것도 하지 않는다
    r = _run([sys.executable, "pipelines/indexer.py", "--check"])
    print(" ", (r.stdout or r.stderr).strip().splitlines()[-1])
    if r.returncode:
        return 1

    # 2) 색인 + 번들 재생성
    for b in BUNDLES:
        if not (ROOT / "pipelines" / b).exists():
            continue
        r = _run([sys.executable, f"pipelines/{b}"])
        if r.returncode:
            print(f"  {b} 실패:\n{r.stdout}{r.stderr}")
            return 1
        last = (r.stdout or "").strip().splitlines()
        print("  " + (last[-1] if last else b))

    # 3) main 동기화(충돌 예방) — 병합으로 남의 content 가 들어오면 2단계를 다시 돈다
    _run(["git", "fetch", "origin", "main"])
    before = _run(["git", "rev-parse", "HEAD"]).stdout.strip()
    if not dry:
        _run(["git", "add", "-A"])
        _run(["git", "commit", "-q", "-m", message])
        m = _run(["git", "merge", "origin/main", "--no-edit"])
        if m.returncode:
            print(f"  병합 충돌 — 사람이 풀어야 한다:\n{m.stdout}{m.stderr}")
            return 1
        if _run(["git", "rev-parse", "HEAD"]).stdout.strip() != before:
            for b in BUNDLES:                      # 병합 직후 번들은 낡아 있다
                if (ROOT / "pipelines" / b).exists():
                    _run([sys.executable, f"pipelines/{b}"])
            if changed_paths():
                _run(["git", "add", "-A"])
                _run(["git", "commit", "-q", "-m", f"{message} (번들 재생성)"])
    else:
        print(f"  [dry] git add -A && git commit -m {message!r} && git merge origin/main")

    # 4) 푸시
    return 0 if push_with_backoff(branch, dry) else 1


def selftest() -> int:
    content, code = classify([
        "content/anatomy/questions/tagging-1/anatomy-2026-0096.md",
        "docs/search-index.js", "state/ailab_progress.json",
        "pipelines/anatomy_subnote.py", "CLAUDE.md", ".claude/skills/x/SKILL.md",
    ])
    assert content == ["content/anatomy/questions/tagging-1/anatomy-2026-0096.md",
                       "docs/search-index.js", "state/ailab_progress.json"], content
    assert code == ["pipelines/anatomy_subnote.py", "CLAUDE.md",
                    ".claude/skills/x/SKILL.md"], code
    # 비공개 렌더는 애초에 gitignore 라 목록에 안 뜨지만, 뜨더라도 코드 레인으로 막힌다
    assert classify([".private/anatomy/render/x.png"])[1], "비공개 경로가 콘텐츠로 샜다"

    # 문항을 브랜치로 빼려는 시도는 거부돼야 한다(ID 재발급 사고 방지).
    # 2026-07~08: 문항 PR 6건이 병합되지 않아 usmle-2026-0049~0054 가 다섯 번 재발급됐다.
    q = ["content/usmle/usmle-2026-0049.md", "docs/questions_usmle.js"]
    assert blocks_question_branch(q, [], "claude/x", False) == \
        ["content/usmle/usmle-2026-0049.md"], "문항의 브랜치 발행을 막지 못했다"
    assert blocks_question_branch(q, [], "main", False) == [], "main 푸시를 막았다"
    assert blocks_question_branch(q, [], "claude/x", True) == [], \
        "명시 허용(--allow-question-branch)까지 막았다"
    assert blocks_question_branch(q, ["pipelines/x.py"], "claude/x", False) == [], \
        "코드가 섞이면 코드 레인 규칙이 우선이어야 한다"
    assert blocks_question_branch(["content/papers/2026/x.md"], [], "claude/x", False) == [], \
        "논문 카드의 브랜치 발행까지 막았다"
    assert blocks_question_branch(["content/kmle/2026/k.md"], [], "claude/x", False) == \
        ["content/kmle/2026/k.md"], "KMLE 도 동일하게 막혀야 한다"
    print("[ OK ] publish selftest")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("-m", "--message", help="커밋 메시지")
    ap.add_argument("--branch", default="main")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--allow-code", action="store_true",
                    help="코드 레인 변경도 main 에 직접 푸시(사람이 확인했을 때만)")
    ap.add_argument("--allow-question-branch", action="store_true",
                    help="문항(kmle/usmle)을 브랜치로 올린다 — PR 을 같은 세션에서 병합할 때만")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not a.message:
        print("-m '커밋 메시지' 가 필요하다 (또는 --selftest)")
        return 2
    return publish(a.message, a.branch, a.dry_run, a.allow_code,
                   a.allow_question_branch)


if __name__ == "__main__":
    sys.exit(main())
