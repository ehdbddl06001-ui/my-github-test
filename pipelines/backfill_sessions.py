#!/usr/bin/env python3
"""backfill_sessions.py — `scheduled_dates` 가 빠진 anatomy 문항에 회차를 채운다(결정론).

왜 필요한가: 초기에 만든 문항들은 `scheduled_dates` 가 없어 **회차 필터·일일 큐에
잡히지 않는다**(웹 '오늘의 문항'·데일리 플랜이 못 고름). 그런데 그 카드의 `source`
문자열에는 과거 학기의 담당교수·날짜가 박혀 있어 **그걸로 회차를 정하면 안 된다**
(CLAUDE.md 원칙). 그래서 `region`/`subregion`/`subtopic` — 즉 **부위**만 보고
`anatomy_schedule.session_for_region()` 으로 회차를 찾는다.

사용:
  python pipelines/backfill_sessions.py --dry-run   # 무엇이 어떻게 바뀌는지만
  python pipelines/backfill_sessions.py             # 실제 기록
  python pipelines/backfill_sessions.py --selftest
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import anatomy_schedule as sched  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
QDIR = ROOT / "content/anatomy/questions"

FIELD_RE = re.compile(r"^(?P<k>region|subregion|subtopic|priority|exam_phase):\s*(?P<v>.+)$",
                      re.M)


def _fields(text: str) -> dict:
    return {m.group("k"): m.group("v").strip().strip('"\'') for m in FIELD_RE.finditer(text)}


def decide(text: str) -> tuple[int | None, str]:
    """부위만 보고 회차를 정한다. 반환 (회차, 판정에 쓴 문자열)."""
    f = _fields(text)
    # 순서가 중요하다. 한 문자열로 합쳐 '가장 긴 키워드'로 고르면 영문 슬러그(gluteal, 7자)가
    # 한글 구조명(볼기피부신경, 6자)을 길이로 이겨 버린다 — 문자 폭이 다르니 길이 비교가
    # 스크립트를 넘나들면 안 된다. 그래서 **구조 이름(subtopic) → 부위 슬러그(subregion)
    # → 큰 부위(region)** 순으로 좁은 근거부터 본다.
    # 예: '위볼기피부신경'(얕은근막 → 1회차)이 subregion=gluteal(2회차)에 끌려가지 않는다.
    for key in ("subtopic", "subregion", "region"):
        v = f.get(key)
        if not v:
            continue
        no = sched.session_for_region(v)
        if no:
            return no, f"{key}={v}"
    return None, ""


def apply(path: Path, dry: bool) -> str | None:
    raw = path.read_text(encoding="utf-8")
    if re.search(r"^scheduled_dates:", raw, re.M):
        return None
    no, why = decide(raw)
    if not no:
        return f"SKIP  {path.name}  (부위로 회차를 못 정함 — 사람이 판단)"
    d = sched.SCHEDULE_2026[no - 1]["date"].isoformat()
    line = f"scheduled_dates: [{d}]\n"
    if re.search(r"^priority:", raw, re.M):
        new = re.sub(r"^(priority:)", line + r"\1", raw, count=1, flags=re.M)
    else:
        new = re.sub(r"^(tags:)", line + r"\1", raw, count=1, flags=re.M)
    if new == raw:
        return f"SKIP  {path.name}  (삽입 위치를 못 찾음)"
    if not dry:
        path.write_text(new, encoding="utf-8")
    return f"{'DRY ' if dry else 'SET '} {path.name}  → {no}회차 {d}   ({why})"


def run(dry: bool) -> int:
    rows = [r for p in sorted(QDIR.rglob("*.md")) if (r := apply(p, dry))]
    for r in rows:
        print(" ", r)
    done = sum(1 for r in rows if not r.startswith("SKIP"))
    print(f"{done}건 회차 배정 · {len(rows) - done}건 보류")
    return 0


def selftest() -> int:
    cases = [
        ("subregion: superficial-back", 2),
        ("subregion: popliteal-fossa", 3),
        ("subregion: pelvic-diaphragm", 14),
        ("subregion: parotid", 4),
        ("subregion: anterior-neck", 6),
    ]
    for text, want in cases:
        got, _ = decide(text + "\n")
        assert got == want, f"{text} → {got} (기대 {want})"
    # 교수명·과거 학기 날짜가 있어도 그것으로 정하지 않는다
    txt = 'source: "3회차(0825) 허미선pf.pdf"\nsubregion: superficial-back\n'
    got, why = decide(txt)
    assert got == 2 and "subregion" in why, f"교수명/날짜에 끌려감: {got} {why}"
    # 구조 이름이 부위 슬러그를 이긴다 — 얕은근막의 피부신경은 볼기 해부(2회차)가 아니라 1회차
    txt = "subtopic: 위볼기피부신경 실사 spotter\nsubregion: gluteal\nregion: back\n"
    got, why = decide(txt)
    assert got == 1 and "subtopic" in why, f"슬러그에 끌려감: {got} {why}"
    print("[ OK ] backfill_sessions selftest")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    return run(a.dry_run)


if __name__ == "__main__":
    sys.exit(main())
