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
from gen_ecg_svg import ecg_svg

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


def explanation_items(body: str) -> list[dict]:
    """'## 정답 및 해설'의 `- **키**: 값` 불릿을 [{k, v}] 로 파싱한다.
    값이 여러 줄로 감싸져 있으면 한 값으로 병합한다(웹이 항목별 박스로 렌더)."""
    if "## 정답 및 해설" not in body:
        return []
    sec = body.split("## 정답 및 해설", 1)[1]
    items: list[dict] = []
    cur: dict | None = None
    for raw in sec.splitlines():
        st = raw.strip()
        if st.startswith(">"):          # '> 정답: X' 인용줄 제외
            continue
        m = re.match(r"^-\s*\*\*(.+?)\*\*\s*[:：]?\s*(.*)$", st)
        if m:
            if cur:
                items.append(cur)
            cur = {"k": m.group(1).strip(), "v": m.group(2).strip()}
        elif cur is not None and st:     # 이어지는 줄바꿈 값 병합
            cur["v"] = (cur["v"] + " " + st).strip()
    if cur:
        items.append(cur)
    for it in items:
        it["v"] = it["v"].replace("**", "").strip()
    return items


def render_figure(fig: dict | None, fname: str = "") -> str:
    """frontmatter의 figure 명세를 인라인 SVG 문자열로 렌더한다(결정론적 생성).
    현재 type=ecg 지원. 확장 시 여기서 분기한다(ctg·spirometry 등)."""
    if not isinstance(fig, dict):
        return ""
    kind = fig.get("type")
    try:
        if kind == "ecg":
            return ecg_svg(
                rhythm=fig.get("rhythm", "sinus"),
                rate=float(fig.get("rate", 75)),
                seconds=float(fig.get("seconds", 6)),
                label=fig.get("label"),
            )
    except Exception as e:  # 생성 실패해도 문항은 살린다
        print(f"[figure] {fname}: {e}")
    return ""


def build_record(path: Path) -> dict | None:
    d = load(path)
    if d.errors:
        print(f"[SKIP] {path.name}: {d.errors}")
        return None
    m = d.meta
    vignette, question = split_stem(m.get("stem", ""))
    ans = str(m.get("answer", "")).strip().upper()
    subject = m.get("exam_subject") or m.get("topic", "")
    figure_svg = render_figure(m.get("figure"), path.name)
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
        "explanationItems": explanation_items(d.body),
        "source": m.get("source", ""),
        # 구조화 임상 자료(선택): 활력징후·검사소견 박스, 해설 부록(결정표 등)
        "vitals": m.get("vitals", []) or [],
        "labs": m.get("labs", []) or [],
        "appendix": m.get("appendix") or None,
        "figureSvg": figure_svg,
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
