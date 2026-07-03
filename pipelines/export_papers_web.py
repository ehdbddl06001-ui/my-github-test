"""
export_papers_web.py — content/papers/**/*.md 를 홈페이지용 JS 번들로 내보낸다.

MedKOS 원칙: Markdown(content/papers/**/*.md)이 원본, docs/papers.js는 파생물이다.
export_usmle_web.py 와 대칭. frontmatter + 본문 섹션을 읽어 window.PAPERS 를 만든다.

산출물: window.PAPERS (docs/papers.js) — 최신순 정렬
  각 레코드: id, topic, subtopic, title, authors[], journal, doi, pmid, url,
             pubdate, date, tags[], abstract, summary, clinicalImpact, myIdeas

사용: python pipelines/export_papers_web.py
"""
from __future__ import annotations

import json
from pathlib import Path

from frontmatter import load

ROOT = Path(__file__).resolve().parent.parent
PAPERS_DIR = ROOT / "content" / "papers"
OUT = ROOT / "docs" / "papers.js"


def section(body: str, name: str) -> str:
    """'## name' 섹션의 본문 텍스트를 추출(다음 '## '까지). TODO 주석은 제거."""
    marker = f"## {name}"
    if marker not in body:
        return ""
    rest = body.split(marker, 1)[1]
    # 다음 헤더 전까지
    lines: list[str] = []
    for line in rest.splitlines()[1:] if rest.startswith("\n") else rest.splitlines():
        if line.startswith("## "):
            break
        if line.strip().startswith("<!--"):   # TODO 자리표시자는 버림
            continue
        lines.append(line)
    return "\n".join(lines).strip()


def build_record(path: Path) -> dict | None:
    d = load(path)
    if d.errors:
        print(f"[SKIP] {path.name}: {d.errors}")
        return None
    m = d.meta
    return {
        "id": d.id,
        "topic": m.get("topic", ""),
        "subtopic": m.get("subtopic", ""),
        "title": section(d.body, "Title") or m.get("topic", ""),
        "authors": m.get("authors", []) or [],
        "journal": m.get("journal", "") or "",
        "doi": m.get("doi", "") or "",
        "pmid": str(m.get("pmid", "") or ""),
        "url": m.get("url", "") or "",
        "pubdate": str(m.get("pubdate", "") or ""),
        "date": str(m.get("date", "") or ""),
        "tags": m.get("tags", []) or [],
        "confidence": m.get("confidence", ""),
        "abstract": section(d.body, "Abstract"),
        "summary": section(d.body, "Summary"),
        "clinicalImpact": section(d.body, "Clinical Impact"),
        "myIdeas": section(d.body, "My Ideas"),
    }


def load_records() -> list[dict]:
    records = []
    for p in PAPERS_DIR.rglob("*.md"):
        rec = build_record(p)
        if rec:
            records.append(rec)
    # 최신순: date desc, 그다음 id desc
    records.sort(key=lambda r: (r["date"], r["id"]), reverse=True)
    return records


def main() -> int:
    records = load_records()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(records, ensure_ascii=False, indent=1)
    OUT.write_text(
        "// 자동 생성 파일 — 수정하지 마세요.\n"
        "// 원본: content/papers/**/*.md  →  `python pipelines/export_papers_web.py`로 재생성\n"
        "window.PAPERS = " + payload + ";\n",
        encoding="utf-8",
    )
    topics: dict[str, int] = {}
    for r in records:
        topics[r["topic"]] = topics.get(r["topic"], 0) + 1
    summary = ", ".join(f"{k}:{v}" for k, v in sorted(topics.items())) or "(없음)"
    print(f"생성: {OUT.relative_to(ROOT)} ({len(records)}편)  {summary}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
