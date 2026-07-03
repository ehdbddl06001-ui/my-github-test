"""
export_search_web.py — content/ 전체를 홈페이지 통합검색·대시보드용 JS 번들로 내보낸다.

GitHub Pages 는 정적이라 SQLite 를 직접 못 쓴다. 그래서 CLI(search.py)는 SQLite FTS5 를
직접 조회하고, 웹은 이 스크립트가 만든 색인 번들을 브라우저에서 검색한다. 둘 다 원본은
content/**/*.md 하나다(대칭: export_usmle_web.py / export_papers_web.py).

산출물: docs/search-index.js
  window.MEDKOS_INDEX = { generated, repo, branch, stats{...}, docs[ {...} ] }
  각 doc: id, type, topic, subtopic, tags[], source, confidence, date, path, text(검색용)

사용: python pipelines/export_search_web.py
"""
from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path

from frontmatter import Doc, load

ROOT = Path(__file__).resolve().parent.parent
CONTENT_DIR = ROOT / "content"
OUT = ROOT / "docs" / "search-index.js"

REPO = "ehdbddl06001-ui/my-github-test"
BRANCH = "main"
SNIPPET_LEN = 240


def _strip_md(text: str) -> str:
    """검색·미리보기용으로 마크다운 장식을 대충 걷어낸다."""
    text = re.sub(r"[#>*`|_-]+", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def build_record(d: Doc) -> dict:
    m = d.meta
    if d.is_question:
        # 문제형은 stem + 보기 + 해설을 검색 텍스트로(정답 자체는 넣지 않는다).
        body = "\n".join(filter(None, [
            m.get("stem", ""),
            " ".join(str(c) for c in m.get("choices", []) or []),
            m.get("explanation", ""),
        ]))
    else:
        body = d.body
    clean = _strip_md(body)
    return {
        "id": d.id,
        "type": d.type,
        "topic": m.get("topic", "") or "",
        "subtopic": m.get("subtopic", "") or "",
        "tags": [str(t) for t in (m.get("tags", []) or [])],
        "source": m.get("source", "") or "",
        "confidence": m.get("confidence", "") or "",
        "date": str(m.get("date", "") or ""),
        "path": str(d.path.relative_to(ROOT)),
        "snippet": clean[:SNIPPET_LEN],
        # 검색 대상 텍스트(제목+주제+태그+본문). 소문자는 브라우저에서 처리.
        "text": " ".join(filter(None, [
            m.get("topic", ""), m.get("subtopic", ""),
            " ".join(str(t) for t in (m.get("tags", []) or [])),
            m.get("source", ""), clean,
        ])),
    }


def build_stats(docs: list[dict]) -> dict:
    by_type: dict[str, int] = {}
    by_topic: dict[str, int] = {}
    by_conf: dict[str, int] = {}
    for d in docs:
        by_type[d["type"]] = by_type.get(d["type"], 0) + 1
        if d["topic"]:
            by_topic[d["topic"]] = by_topic.get(d["topic"], 0) + 1
        c = d["confidence"] or "?"
        by_conf[c] = by_conf.get(c, 0) + 1
    tags = {t for d in docs for t in d["tags"]}
    return {
        "total": len(docs),
        "byType": by_type,
        "byTopic": dict(sorted(by_topic.items(), key=lambda kv: (-kv[1], kv[0]))),
        "byConfidence": by_conf,
        "tagCount": len(tags),
    }


def load_records() -> list[dict]:
    records = []
    for p in sorted(CONTENT_DIR.rglob("*.md")):
        d = load(p)
        if d.errors:
            print(f"[SKIP] {p.name}: {d.errors}")
            continue
        records.append(build_record(d))
    # 최신순
    records.sort(key=lambda r: (r["date"], r["id"]), reverse=True)
    return records


def main() -> int:
    docs = load_records()
    payload = {
        "generated": date.today().isoformat(),
        "repo": REPO,
        "branch": BRANCH,
        "stats": build_stats(docs),
        "docs": docs,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(
        "// 자동 생성 파일 — 수정하지 마세요.\n"
        "// 원본: content/**/*.md  →  `python pipelines/export_search_web.py`로 재생성\n"
        "window.MEDKOS_INDEX = " + json.dumps(payload, ensure_ascii=False, indent=1) + ";\n",
        encoding="utf-8",
    )
    st = payload["stats"]
    print(f"생성: {OUT.relative_to(ROOT)} ({st['total']}개 문서)  "
          + ", ".join(f"{k}:{v}" for k, v in sorted(st["byType"].items())))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
