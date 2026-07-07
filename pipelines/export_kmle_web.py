"""
export_kmle_web.py — content/kmle/**/*.md 를 웹 퀴즈용 JS 번들로 내보낸다.

배경: 인터랙티브 퀴즈(docs/app.js)의 KMLE는 원래 옛 quiz.py 트랙(docs/questions.js)
에서만 나왔고, MedKOS의 Source of Truth 인 content/kmle/*.md(매일 루틴이 생성)는
퀴즈에 뜨지 않았다. 이 스크립트가 그 간극을 메운다.

MedKOS 원칙: Markdown(content/kmle/**/*.md)이 원본, 이 번들은 파생물이다.
export_usmle_web.py 와 대칭이며 파싱 로직을 재사용한다(step/exam_subject 없음).

산출물: window.KMLE_CONTENT_QUESTIONS (docs/questions_kmle_content.js)
  app.js 가 기존 window.KMLE_QUESTIONS(레거시)와 합쳐서 KMLE 덱을 만든다.

사용: python pipelines/export_kmle_web.py
"""
from __future__ import annotations

import json
from pathlib import Path

from frontmatter import load
from export_usmle_web import (
    LETTERS,
    clean_option,
    explanation_items,
    explanation_text,
    split_stem,
)

ROOT = Path(__file__).resolve().parent.parent
KMLE_DIR = ROOT / "content" / "kmle"
OUT = ROOT / "docs" / "questions_kmle_content.js"


def build_record(path: Path) -> dict | None:
    d = load(path)
    if d.errors:
        print(f"[SKIP] {path.name}: {d.errors}")
        return None
    m = d.meta
    vignette, question = split_stem(m.get("stem", ""))
    ans = str(m.get("answer", "")).strip().upper()
    return {
        "id": d.id,
        "exam": "kmle",
        "subject": m.get("topic", ""),
        "subject_file": m.get("topic", ""),
        "subtopic": m.get("subtopic", ""),
        "type": m.get("subtopic", ""),
        "difficulty": m.get("difficulty"),
        "created": str(m.get("date", "") or ""),   # '오늘의 문항' 필터용
        "vignette": vignette,
        "question": question,
        "options": [clean_option(o) for o in m.get("choices", [])],
        "answer": LETTERS.get(ans, 0),
        "explanationText": explanation_text(d.body),
        "explanationItems": explanation_items(d.body),
        "source": m.get("source", ""),
        "vitals": m.get("vitals", []) or [],
        "labs": m.get("labs", []) or [],
        "appendix": m.get("appendix") or None,
    }


def load_records() -> list[dict]:
    records = []
    for p in sorted(KMLE_DIR.rglob("*.md")):
        rec = build_record(p)
        if rec:
            records.append(rec)
    # 최신순: created desc, 그다음 id desc (오늘의 문항이 위로)
    records.sort(key=lambda r: (r["created"], r["id"]), reverse=True)
    return records


def main() -> int:
    records = load_records()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(records, ensure_ascii=False, indent=1)
    OUT.write_text(
        "// 자동 생성 파일 — 수정하지 마세요.\n"
        "// 원본: content/kmle/**/*.md  →  `python pipelines/export_kmle_web.py`로 재생성\n"
        "window.KMLE_CONTENT_QUESTIONS = " + payload + ";\n",
        encoding="utf-8",
    )
    print(f"생성: {OUT.relative_to(ROOT)} ({len(records)}문항)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
