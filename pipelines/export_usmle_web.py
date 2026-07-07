"""
export_usmle_web.py — content/usmle/*.md 를 웹 퀴즈용 JS 번들로 내보낸다.

MedKOS 원칙: Markdown(content/usmle/*.md)이 원본, 웹 번들은 파생물이다.
KMLE의 `quiz.py --export`(JSON→docs/questions.js)와 대칭이며, 이쪽은
frontmatter가 붙은 .md 를 읽어 docs/questions_usmle.js 를 만든다.

산출물: window.USMLE_QUESTIONS (docs/questions_usmle.js)
  각 레코드: id, exam, step, subject, subtopic, type, difficulty,
             vignette, question, options[], answer(1-based), explanationText, source

사용: python pipelines/export_usmle_web.py
"""
from __future__ import annotations

import json
import re
from pathlib import Path

from frontmatter import load

ROOT = Path(__file__).resolve().parent.parent
USMLE_DIR = ROOT / "content" / "usmle"
OUT = ROOT / "docs" / "questions_usmle.js"

LETTERS = {c: i + 1 for i, c in enumerate("ABCDE")}


def split_stem(stem: str) -> tuple[str, str]:
    """증례 본문(vignette)과 마지막 질문 문장(question)을 분리한다."""
    stem = (stem or "").strip()
    parts = re.split(r"(?<=[.?!])\s+", stem)
    if len(parts) >= 2:
        return " ".join(parts[:-1]).strip(), parts[-1].strip()
    return "", stem


def clean_option(opt: str) -> str:
    """'A. 텍스트' → '텍스트' (앞 글머리 라벨 제거; 웹에서 A~E를 다시 붙인다)."""
    return re.sub(r"^\s*[A-E][.)]\s*", "", str(opt)).strip()


def explanation_text(body: str) -> str:
    """본문의 '## 정답 및 해설' 섹션을 사람이 읽을 텍스트로 추출한다."""
    if "## 정답 및 해설" not in body:
        return ""
    sec = body.split("## 정답 및 해설", 1)[1]
    lines: list[str] = []
    for raw in sec.splitlines():
        s = raw.rstrip()
        if s.strip().startswith(">"):   # '> 정답: X' 인용줄은 앱이 채점으로 표시하므로 제외
            continue
        lines.append(s.replace("**", ""))
    return "\n".join(lines).strip()


def build_record(path: Path) -> dict | None:
    d = load(path)
    if d.errors:
        print(f"[SKIP] {path.name}: {d.errors}")
        return None
    m = d.meta
    vignette, question = split_stem(m.get("stem", ""))
    ans = str(m.get("answer", "")).strip().upper()
    subject = m.get("exam_subject") or m.get("topic", "")
    return {
        "id": d.id,
        "exam": "usmle",
        "step": m.get("step", ""),
        "subject": subject,
        "subject_file": subject,
        "subtopic": m.get("subtopic", ""),
        "type": m.get("subtopic", ""),
        "difficulty": m.get("difficulty"),
        "created": str(m.get("date", "") or ""),   # '오늘의 문항'(웹 today 모드) 필터용
        "vignette": vignette,
        "question": question,
        "options": [clean_option(o) for o in m.get("choices", [])],
        "answer": LETTERS.get(ans, 0),
        "explanationText": explanation_text(d.body),
        "source": m.get("source", ""),
    }


def load_records() -> list[dict]:
    """content/usmle/*.md 를 읽어 퀴즈용 레코드 리스트로 반환(웹·CLI 공용)."""
    records = []
    for p in sorted(USMLE_DIR.glob("*.md")):
        rec = build_record(p)
        if rec:
            records.append(rec)
    return records


def main() -> int:
    records = load_records()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(records, ensure_ascii=False, indent=1)
    OUT.write_text(
        "// 자동 생성 파일 — 수정하지 마세요.\n"
        "// 원본: content/usmle/*.md  →  `python pipelines/export_usmle_web.py`로 재생성\n"
        "window.USMLE_QUESTIONS = " + payload + ";\n",
        encoding="utf-8",
    )
    steps = {}
    for r in records:
        steps[r["step"]] = steps.get(r["step"], 0) + 1
    print(f"생성: {OUT.relative_to(ROOT)} ({len(records)}문항)  " + ", ".join(f"{k}:{v}" for k, v in sorted(steps.items())))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
