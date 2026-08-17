"""
export_diagrams_web.py — `docs/assets/anatomy/*.svg` 를 **만든 날짜순 갤러리 데이터**로 뽑는다.

왜 필요한가: 도해·트리는 content 카드(.md)가 아니라 자산 파일이라 검색 색인
(`search-index.js`)에 안 잡힌다. 그래서 "새 자료" 목록에 도해가 통째로 빠져 있었다
(사용자 지적 2026-08-16). 여기서 자산의 메타(만든 날짜·회차·종류·라벨/퀴즈 쌍)를
결정론적으로 뽑아 `docs/diagrams-data.js` 로 내보낸다.

만든 날짜 = **git 에 처음 추가된 커밋 날짜**(KST). git 이 없거나 미추적이면 파일 mtime.
회차 = 파일명(`tree-sNN-*`) 또는 그 파일을 `!fig` 로 거는 서브노트의 `session_no`.

실행: python pipelines/export_diagrams_web.py
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "docs" / "assets" / "anatomy"
NOTES = ROOT / "content" / "anatomy" / "notes"
OUT = ROOT / "docs" / "diagrams-data.js"
KST = timezone(timedelta(hours=9))

KIND_LABEL = {
    "tree-nerve": "신경 계보",
    "tree-vessel": "혈관 계보(동맥+정맥)",
    "tree-bundle": "신경혈관다발",
    "diag": "위치 도해",
}


def _git_added_date(rel: str) -> str:
    """파일이 git 에 처음 들어온 커밋의 날짜(KST). 미추적이면 빈 문자열."""
    try:
        r = subprocess.run(
            ["git", "log", "--diff-filter=A", "--follow", "--format=%aI", "--", rel],
            cwd=ROOT, capture_output=True, text=True, timeout=20)
        lines = [x for x in r.stdout.strip().splitlines() if x]
        if not lines:
            return ""
        # --follow 는 오래된 것이 마지막에 온다
        return datetime.fromisoformat(lines[-1]).astimezone(KST).date().isoformat()
    except Exception:
        return ""


def _kind(name: str) -> str:
    if name.startswith("tree-"):
        for k in ("nerve", "vessel", "bundle"):
            if f"-{k}-" in name:
                return f"tree-{k}"
        return "tree-nerve"
    return "diag"


def _session(name: str, fig_map: dict[str, int]) -> int | None:
    m = re.match(r"tree-s(\d{2})-", name)
    if m:
        return int(m.group(1))
    return fig_map.get(name)


def _title(svg: str, fallback: str) -> str:
    m = re.search(r'aria-label="([^"]+)"', svg)
    if m:
        return m.group(1).split(" — ")[0].strip()
    return fallback


def _fig_map() -> dict[str, int]:
    """SVG 파일 → 그 파일을 참조하는 카드의 회차.

    서브노트의 `!fig` 뿐 아니라 문항 카드의 `web_asset` 도 본다(퀴즈판은 대개
    문항 카드에서만 참조된다). session_no 가 없으면 scheduled_dates 로 역산한다.
    """
    sys.path.insert(0, str(Path(__file__).parent))
    try:
        from anatomy_schedule import session_no_for_date
        from datetime import date as _date
    except Exception:                                   # 스케줄 모듈이 없어도 동작
        session_no_for_date = lambda d: None            # noqa: E731

    out: dict[str, int] = {}
    content = ROOT / "content" / "anatomy"
    for p in sorted(content.rglob("*.md")):
        s = p.read_text(encoding="utf-8")
        names = set(re.findall(r"assets/anatomy/([\w.-]+\.svg)", s))
        if not names:
            continue
        m = re.search(r"^session_no:\s*(\d+)", s, re.M)
        no = int(m.group(1)) if m else None
        if no is None:
            d = re.search(r"^scheduled_dates:\s*\[(\d{4})-(\d{2})-(\d{2})", s, re.M)
            if d:
                try:
                    no = session_no_for_date(_date(*(int(x) for x in d.groups())))
                except Exception:
                    no = None
        if no:
            for f in names:
                out.setdefault(f, no)
    return out


def collect() -> list[dict]:
    fig_map = _fig_map()
    sys.path.insert(0, str(Path(__file__).parent))
    try:
        from anatomy_schedule import unit_label
    except Exception:                                   # 스케줄 모듈이 없어도 동작
        def unit_label(meta):                           # noqa: ANN001
            no = meta.get("session_no")
            return f"{no}회차" if no else ""

    rows: list[dict] = []
    for p in sorted(ASSETS.glob("*.svg")):
        name = p.name
        svg = p.read_text(encoding="utf-8")
        rel = str(p.relative_to(ROOT))
        date = _git_added_date(rel) or datetime.fromtimestamp(
            p.stat().st_mtime, tz=KST).date().isoformat()
        stem = name[:-4]
        variant = ("quiz" if stem.endswith("-quiz")
                   else "labeled" if stem.endswith("-labeled") else "single")
        base = re.sub(r"-(quiz|labeled)$", "", stem)
        session = _session(name, fig_map)
        rows.append({
            "file": name,
            "base": base,
            "variant": variant,
            "kind": _kind(name),
            "kindLabel": KIND_LABEL[_kind(name)],
            "session": session,
            # 날짜순 타임라인에서 카드와 같은 소속 배지를 달기 위한 라벨('2회차 · 등').
            "unit": unit_label({"session_no": session}) if session else "",
            "title": _title(svg, base),
            "date": date,
            "bytes": p.stat().st_size,
        })
    # 만든 날짜 최신순, 같은 날은 회차·이름순
    rows.sort(key=lambda r: (r["date"], -(r["session"] or 0), r["base"]), reverse=True)
    return rows


def main() -> int:
    rows = collect()
    pairs = len({r["base"] for r in rows})
    payload = {
        "generated": datetime.now(tz=KST).date().isoformat(),
        "count": len(rows),
        "groups": pairs,
        "items": rows,
    }
    OUT.write_text(
        "// 자동 생성 파일 — 수정하지 마세요.\n"
        "// 원본: docs/assets/anatomy/*.svg  →  `python pipelines/export_diagrams_web.py`\n"
        "window.MEDKOS_DIAGRAMS = " + json.dumps(payload, ensure_ascii=False, indent=1) + ";\n",
        encoding="utf-8")
    print(f"생성: {OUT.relative_to(ROOT)} (파일 {len(rows)} · 도해 {pairs}종)")
    return 0


def selftest() -> int:
    rows = collect()
    assert rows, "SVG를 하나도 못 찾음"
    assert all(r["date"] for r in rows), "날짜 없는 자산"
    # 라벨판/퀴즈판은 같은 base 로 묶여야 짝으로 보인다
    quiz = {r["base"] for r in rows if r["variant"] == "quiz"}
    lab = {r["base"] for r in rows if r["variant"] == "labeled"}
    assert quiz <= lab, f"퀴즈판만 있고 라벨판이 없는 도해: {quiz - lab}"
    # 트리는 파일명에서 회차가 나와야 한다
    for r in rows:
        if r["file"].startswith("tree-"):
            assert r["session"], f"{r['file']}: 회차 미상"
    print(f"[ OK ] export_diagrams_web selftest (파일 {len(rows)})")
    return 0


if __name__ == "__main__":
    sys.exit(selftest() if "--selftest" in sys.argv else main())
