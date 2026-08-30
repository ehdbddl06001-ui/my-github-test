#!/usr/bin/env python3
"""anatomy_export_questions.py — 회차 문항을 **Drive 에 넣을 수 있는 텍스트**로 내보낸다.

왜 따로 있나: 서브노트 PDF 는 실사 복원본을 합본하므로 `.private/` 를 벗어나지 못하고,
MCP 로 올리면 파일 크기의 2배가 토큰으로 나간다(1.2MB ≈ 90만 토큰, 2026-08-14 실측).
반면 **문항의 글(지문·정답·해설)은 이미지가 아니라 텍스트**라 그대로 Docs 로 올릴 수
있고 비용이 거의 없다. 그래서 이 스크립트는 그림을 빼고 글만 모아 한 파일로 만든다
(사용자 지시 2026-08-30: "만든 문항들은 드라이브에 저장할 수 있도록").

  python pipelines/anatomy_export_questions.py --session 5
  python pipelines/anatomy_export_questions.py --session 5 --output .private/anatomy/export/s05.md

규칙
- 정답을 **문제 뒤로 분리**한다(`answer_separated`). 앞은 풀 수 있게, 뒤에 정답·해설.
- 범위 표기는 `–`(en dash). `~` 는 Docs 변환에서 취소선으로 오해석된다(2026-08-12 실측).
- 그림이 있는 문항은 '그림 문항'으로 표시만 하고 이미지를 넣지 않는다 — 그림은
  서브노트 PDF 로 따로 받는다(이 파일은 Drive 보관·검색용 텍스트본).
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QDIR = ROOT / "content/anatomy/questions"


def _fm(path: Path) -> dict:
    """frontmatter 만 얕게 읽는다(값은 문자열/리스트 그대로)."""
    txt = path.read_text(encoding="utf-8")
    if not txt.startswith("---"):
        return {}
    body = txt.split("---", 2)[1]
    out, key = {}, None
    for line in body.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if not line[0].isspace() and ":" in line:
            key, _, val = line.partition(":")
            key = key.strip()
            out[key] = val.strip().strip('"')
        elif key:
            out[key] = f"{out.get(key, '')} {line.strip()}".strip()
    return out


def collect(session: int) -> list[dict]:
    rows = []
    for p in sorted(QDIR.rglob("*.md")):
        fm = _fm(p)
        if str(fm.get("session_no", "")).strip() != str(session):
            continue
        if not fm.get("stem"):
            continue
        rows.append(fm | {"_path": p})
    rows.sort(key=lambda r: r.get("id", ""))
    return rows


def render(session: int, rows: list[dict]) -> str:
    if not rows:
        return f"# {session}회차 문항\n\n문항이 없다.\n"
    pics = sum(1 for r in rows if r.get("asset_ref"))
    out = [
        f"# {session}회차 실사·관계형 문항 ({len(rows)}문항)",
        "",
        f"- 그림 문항 {pics}개 · 글 문항 {len(rows) - pics}개",
        "- 정답은 **뒤쪽 '정답 및 해설'** 에 모아 두었다 — 먼저 풀고 내려가서 맞춰 볼 것.",
        "- 그림은 이 파일에 없다(서브노트 PDF 로 따로 받는다). 여기 있는 것은 글뿐이다.",
        "",
        "## 문제",
        "",
    ]
    for i, r in enumerate(rows, 1):
        tag = " *(그림 문항 — 서브노트 PDF 참조)*" if r.get("asset_ref") else ""
        out += [f"**{i}. [{r.get('id', '?')}]**{tag}", "", r.get("stem", "").strip(), ""]
    out += ["", "## 정답 및 해설", ""]
    for i, r in enumerate(rows, 1):
        out += [f"**{i}. [{r.get('id', '?')}]**", "",
                f"정답 — {r.get('answer', '').strip()}", ""]
        if r.get("explanation"):
            out += [r["explanation"].strip(), ""]
    text = "\n".join(out)
    # Docs 변환에서 `~` 는 취소선이 된다 — 범위는 en dash 로 통일한다.
    return text.replace("~", "–")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--session", type=int, required=True)
    ap.add_argument("--output")
    a = ap.parse_args()
    rows = collect(a.session)
    text = render(a.session, rows)
    out = Path(a.output) if a.output else ROOT / f".private/anatomy/export/s{a.session:02d}-questions.md"
    if ".private" not in out.parts:
        print("출력은 .private/ 아래여야 한다 — 카데바 파생 문항이다", file=sys.stderr)
        return 2
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8")
    print(f"생성: {out} ({len(rows)}문항 · {len(text)}자)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
