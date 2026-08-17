#!/usr/bin/env python3
"""legacy_sources.py — 과거 학기 자료의 **교수명·날짜가 근거처럼 읽히지 않게** 표시한다.

배경: 업로드 스캔의 파일명은 `3회차(0825) 허미선pf.pdf` 처럼 **과거 학기**의 회차·날짜·
담당교수를 달고 있다. 2026 확정본(anatomy_schedule.SESSION_DETAILS)의 담당은 문용석·
김홍태 둘뿐이라 그 이름은 올해 수업과 아무 관계가 없는데, 카드의 `source` 문자열에
그대로 남아 있으면 나중에 "이 회차는 그 교수 자료" 로 잘못 읽힌다. 실제로 그 교수가
올해 수업에 들어오지 않는다는 사실이 확인됐다(2026-08-17).

원칙은 그대로다 — **회차 배정은 부위 기준**(session_for_region). 이 도구는 배정을
건드리지 않고, 파일명에서 온 교수명 뒤에 한 번만 꼬리표를 붙인다:

    3회차(0825) 허미선pf.pdf
    → 3회차(0825) 허미선pf.pdf〔과거 학기 파일명 — 2026 담당·회차 근거 아님〕

사용:
  python pipelines/legacy_sources.py --dry-run
  python pipelines/legacy_sources.py
  python pipelines/legacy_sources.py --selftest
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import anatomy_schedule as sched  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
SCAN_DIRS = ["content/anatomy"]

MARK = "〔과거 학기 파일명 — 2026 담당·회차 근거 아님〕"
# `…pf.pdf` / `…교수.pdf` 형태의 파일명에 붙은 한글 이름 2~4자
PROF_FILE_RE = re.compile(r"([가-힣]{2,4})\s*(pf|교수)\.pdf")


def current_professors() -> set[str]:
    """2026 확정본에 실제로 잡힌 담당교수 이름 집합."""
    out: set[str] = set()
    for d in sched.SESSION_DETAILS.values():
        for name in str(d.get("professor", "")).split("·"):
            if name.strip():
                out.add(name.strip())
    return out


def needs_mark(text: str, current: set[str]) -> list[str]:
    """표시가 필요한(=2026 담당이 아닌) 교수명 목록."""
    names = []
    for m in PROF_FILE_RE.finditer(text):
        name = m.group(1)
        if name in current:
            continue                      # 올해도 담당이면 오해 소지가 없다
        # 이미 표시된 자리는 건너뛴다 — 여러 번 돌려도 꼬리표가 겹치지 않게
        if text[m.end():m.end() + len(MARK)] == MARK:
            continue
        names.append(name)
    return names


def mark(text: str, current: set[str]) -> str:
    def rep(m):
        if m.group(1) in current:
            return m.group(0)
        tail = text[m.end():m.end() + len(MARK)]
        return m.group(0) if tail == MARK else m.group(0) + MARK
    return PROF_FILE_RE.sub(rep, text)


def run(dry: bool) -> int:
    current = current_professors()
    hit = 0
    for d in SCAN_DIRS:
        for p in sorted((ROOT / d).rglob("*.md")):
            raw = p.read_text(encoding="utf-8")
            names = needs_mark(raw, current)
            if not names:
                continue
            hit += 1
            print(f"  {'DRY ' if dry else 'MARK'} {p.relative_to(ROOT)}  ({', '.join(sorted(set(names)))})")
            if not dry:
                p.write_text(mark(raw, current), encoding="utf-8")
    print(f"{hit}개 카드 표시{' (dry-run)' if dry else ''} · 2026 담당: {', '.join(sorted(current))}")
    return 0


def selftest() -> int:
    cur = {"문용석", "김홍태"}
    s = 'source: "3회차(0825) 허미선pf.pdf — 업로드 스캔"'
    assert needs_mark(s, cur) == ["허미선"]
    out = mark(s, cur)
    assert MARK in out and out.index(MARK) == out.index("허미선pf.pdf") + len("허미선pf.pdf")
    # 멱등: 두 번 돌려도 꼬리표가 하나
    assert mark(out, cur) == out and out.count(MARK) == 1
    # 올해도 담당인 교수는 건드리지 않는다
    keep = 'source: "4회차(0828) 문용석pf.pdf"'
    assert needs_mark(keep, cur) == [] and mark(keep, cur) == keep
    # 실제 2026 확정본에 허미선이 없다는 사실이 이 도구의 전제다
    assert "허미선" not in current_professors()
    print("[ OK ] legacy_sources selftest")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    return selftest() if a.selftest else run(a.dry_run)


if __name__ == "__main__":
    sys.exit(main())
