"""export_concepts_web.py — content/concepts/**/*.md 를 웹 앱의 오답 뒤 학습 흐름용 번들로 내보낸다.

산출물: window.MEDKOS_CONCEPTS (docs/concepts.js) = {개념 id: 정리본}
  · 본문은 Markdown → HTML 을 여기서 허용 태그만 남겨 정화한다(concepts.sanitize). 앱이 한 번 더 정화한다.
  · 도식은 SVG 문자열이 아니라 **배치(geometry)** 로 싣는다 — 앱이 createElementNS·textContent 로 그려
    콘텐츠 글자가 마크업으로 해석될 길이 없고, 사례 경로·선택한 오답의 갈림 지점을 그 자리에서 표시한다.
  · 글 대체본(steps)도 같은 그래프에서 만든다 — 도식이 안 그려져도 학습이 끊기지 않는다.
  · 변형 문제는 이 번들에만 있다 — 일반 덱(questions*.js)에 섞이지 않는다(지연된 적용 확인 전용).

MedKOS 원칙: Markdown 이 원본, 이 번들은 파생물이다. publish.py 가 자동 실행한다.
사용: python pipelines/export_concepts_web.py
"""
from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

import decision_diagram as dd
from concepts import LETTERS, linked_questions, load_concepts, load_questions, render_cites, safe_url

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "concepts.js"


def _source(s: dict) -> dict:
    url = safe_url(s.get("url")) or (f"https://doi.org/{s['doi']}" if s.get("doi") else "") \
        or (f"https://pubmed.ncbi.nlm.nih.gov/{s['pmid']}/" if s.get("pmid") else "")
    return {k: str(s.get(k, "") or "") for k in ("id", "org", "title", "kind", "citation", "checked", "doi", "pmid", "verified")} | {
        "year": str(s.get("year", "") or ""), "checkedAt": str(s.get("checked_at", "") or ""), "url": safe_url(url)}


def _variant(cid: str, v: dict) -> dict:
    ans = str(v.get("answer", "A")).strip().upper()[:1]
    opts = [str(o) for o in v.get("choices") or []]
    clean = [o[3:].strip() if len(o) > 2 and o[0] in LETTERS and o[1] in ".)" else o for o in opts]
    return {"id": f"{cid}#{v.get('id')}", "context": str(v.get("context", "") or ""), "stem": str(v.get("stem", "")),
            "options": clean, "answer": LETTERS.index(ans) + 1 if ans in LETTERS else 1,
            "explanation": str(v.get("explanation", "") or "")}


def _web(s, c: dict) -> str:
    """표 칸·혼동 항목 글 → escape · **굵게** · 근거 번호(<sup>). 앱이 한 번 더 허용 태그만 남긴다."""
    return render_cites(re.sub(r"\*\*(.+?)\*\*", lambda m: f"<b>{m.group(1)}</b>", html.escape(str(s or ""), quote=False)), c, "web")


def blocking(errs: list[str]) -> list[str]:
    """[WARN] 이 아닌 것만 — concepts.py 의 CLI 와 같은 기준이다.

    2026-09-23 실측: 해리슨 대조 없음 [WARN](클라우드 루틴은 드라이브를 못 읽어 정상적으로 남는다)을
    오류로 세어 exit 1 → publish.py 가 그날 문항 32개까지 통째로 못 올렸다. WARN 은 보고만 하고 막지 않는다.
    """
    return [e for e in errs if "[WARN]" not in e]


def build() -> tuple[dict, list[str]]:
    concepts, errors = load_concepts()
    links = linked_questions(load_questions())
    out = {}
    for cid, c in concepts.items():
        spec = c.get("diagram")
        out[cid] = {
            "id": cid, "title": str(c.get("title", "")), "objective": str(c.get("objective", "")),
            "objectiveKind": str(c.get("objective_kind", "")), "condition": str(c.get("condition", "")),
            "topic": str(c.get("topic", "")), "seeAlso": [str(x) for x in c.get("see_also") or []],
            "version": c.get("version"), "updated": str(c.get("updated", c.get("date", "")) or ""),
            "reviewStatus": str(c.get("review_status", "unreviewed")), "hash": c["hash"],
            "summary": [str(x) for x in c.get("summary") or []],
            "sections": [dict(s, html=render_cites(s["html"], c, "web")) for s in c["sections"]],
            "tables": [{"title": str(tb.get("title", "")), "columns": [str(x) for x in tb.get("columns") or []],
                        "rows": [[_web(x, c) for x in r] for r in tb.get("rows") or []], "note": _web(tb.get("note"), c)}
                       for tb in c.get("tables") or [] if isinstance(tb, dict)],
            "pitfalls": [{"contrast": str(pf.get("contrast", "")), "point": _web(pf.get("point"), c),
                          "exception": _web(pf.get("exception"), c),
                          "cites": " ".join(_web(f"[[{x}]]", c) for x in pf.get("cites") or [])}
                         for pf in c.get("pitfalls") or [] if isinstance(pf, dict)],
            "diagramNotes": [_web(x, c) for x in c.get("diagram_notes") or []],
            "criteria": [{k: (str(v) if not isinstance(v, list) else [str(x) for x in v]) for k, v in cr.items()}
                         for cr in c.get("criteria") or [] if isinstance(cr, dict)],
            "sources": [_source(s) for s in c.get("sources") or [] if isinstance(s, dict)],
            "checks": [{"q": str(k.get("q", "")), "a": str(k.get("a", ""))} for k in c.get("checks") or [] if isinstance(k, dict)],
            "variants": [_variant(cid, v) for v in c.get("variants") or [] if isinstance(v, dict)],
            "diagramTitle": str((spec or {}).get("title", "")),
            "geo": c.get("geo"),
            "steps": dd.text_steps(spec) if c.get("geo") else [],
            "questions": links.get(cid, []),
            "hasErrors": bool(blocking(c["errors"])),
        }
    return out, errors


def main() -> int:
    data, errors = build()
    for e in errors:
        print("  ⚠" if "[WARN]" in e else "  ✗", e)
    OUT.write_text(
        "// 자동 생성 파일 — 수정하지 마세요.\n"
        "// 원본: content/concepts/**/*.md  →  `python pipelines/export_concepts_web.py`로 재생성\n"
        "window.MEDKOS_CONCEPTS = " + json.dumps(data, ensure_ascii=False, indent=1) + ";\n",
        encoding="utf-8", newline="\n",
    )
    print(f"생성: {OUT.relative_to(ROOT)} ({len(data)}개 정리본)")
    return 1 if blocking(errors) else 0


if __name__ == "__main__":
    sys.exit(main())
