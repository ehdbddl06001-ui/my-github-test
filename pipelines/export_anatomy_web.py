"""
export_anatomy_web.py — content/anatomy/ → docs/anatomy-data.js (자동 생성, 수정 금지).

공개 게이트(spec §6):
  - needs_review: true 인 concept/question은 내보내지 않는다.
  - 이미지 자산은 frontmatter `publishable: true`이고 실제로 docs/assets/anatomy/ 에
    존재하는 파일만 참조한다(.private 경로는 절대 내보내지 않음).
  - Drive URL·file ID·토큰은 웹 번들에 넣지 않는다. 출처 표시는 파일명+페이지만.

산출: window.MEDKOS_ANATOMY = { generated, schedule, deadlines, concepts, questions,
                                daily, glossary, answersStats, sources }
사용: python pipelines/export_anatomy_web.py
"""
from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path

try:
    from frontmatter import split_frontmatter
    import anatomy_schedule as sched
except ModuleNotFoundError:
    from pipelines.frontmatter import split_frontmatter
    from pipelines import anatomy_schedule as sched

ROOT = Path(__file__).resolve().parent.parent
ANAT = ROOT / "content" / "anatomy"
OUT = ROOT / "docs" / "anatomy-data.js"
PUBLIC_ASSETS = ROOT / "docs" / "assets" / "anatomy"

FORBIDDEN_SUBSTR = (".private", "drive.google.com", "token", "rclone")


def _load(sub: str) -> list[tuple[dict, str]]:
    out = []
    d = ANAT / sub
    if d.exists():
        for p in sorted(d.rglob("*.md")):
            meta, body = split_frontmatter(p.read_text(encoding="utf-8"))
            if meta.get("type") == "anatomy":
                out.append((meta, body))
    return out


def _refs(meta: dict) -> list[dict]:
    """출처 표시용 — 파일명 + 페이지/섹션만(파일 ID·URL 제외)."""
    out = []
    for r in meta.get("source_refs", []) or []:
        out.append({
            "file": r.get("source_file_name") or r.get("file") or "",
            "page": r.get("page"),
            "section": r.get("section"),
        })
    return out


def _asset(meta: dict) -> str | None:
    """publishable=true 이고 docs/assets/anatomy/ 에 실존하는 이미지 경로만."""
    if meta.get("publishable") is not True:
        return None
    ref = str(meta.get("web_asset", "") or "")
    if not ref or any(s in ref for s in FORBIDDEN_SUBSTR):
        return None
    p = ROOT / "docs" / ref.lstrip("/")
    if not p.exists() or PUBLIC_ASSETS not in p.parents:
        return None
    return ref


def export_concepts() -> list[dict]:
    out = []
    for meta, body in _load("concepts"):
        if meta.get("kind") != "concept" or meta.get("needs_review") is True:
            continue
        out.append({
            "id": meta["id"], "title": meta.get("subtopic", ""),
            "region": meta.get("region", "multi"),
            "subregion": meta.get("subregion", ""),
            "layer": meta.get("layer", ""),
            "conceptStyle": meta.get("concept_style", ""),
            "relations": meta.get("relations", []) or [],
            "structureClasses": meta.get("structure_classes", []) or [],
            "examPhase": meta.get("exam_phase", ""),
            "confidence": meta.get("confidence", ""),
            "classificationConfidence": meta.get("classification_confidence"),
            "tree": meta.get("tree"),  # 분지/주행 시각화용 {name, children[]}
            "refs": _refs(meta),
            "body": body.strip(),
        })
    return out


def export_questions() -> list[dict]:
    out = []
    for meta, body in _load("questions"):
        if meta.get("kind") != "question" or meta.get("needs_review") is True:
            continue
        out.append({
            "id": meta["id"], "style": meta.get("question_style", ""),
            "region": meta.get("region", "multi"),
            "subregion": meta.get("subregion", ""),
            "examPhase": meta.get("exam_phase", ""),
            "stem": meta.get("stem", ""),
            "choices": meta.get("choices") or None,
            "answer": str(meta.get("answer", "")),
            "explanation": meta.get("explanation", ""),
            "confidence": meta.get("confidence", ""),
            "answerOnlyBacked": bool(meta.get("answer_only_backed")),
            "image": _asset(meta),
            "refs": _refs(meta),
        })
    return out


def export_daily() -> list[dict]:
    out = []
    for meta, _ in _load("daily"):
        if meta.get("kind") != "daily_plan":
            continue
        out.append({
            "date": str(meta.get("date", "")), "phase": meta.get("phase", ""),
            "examPhase": meta.get("exam_phase", ""),
            "regions": meta.get("regions", []) or [],
            "concepts": meta.get("concept_ids", {}) or {},
            "questions": meta.get("question_ids", []) or [],
            "review": meta.get("review", {}) or {},
            "estMinutes": meta.get("est_minutes"),
        })
    out.sort(key=lambda d: d["date"], reverse=True)
    return out[:30]


def export_glossary() -> list[dict]:
    seen: dict[str, dict] = {}
    for meta, _ in _load("pages"):
        for t in meta.get("terms", []) or []:
            key = t.get("ko", "")
            if key and key not in seen:
                seen[key] = {"ko": t["ko"], "en": t.get("en", ""),
                             "region": meta.get("region", "multi")}
    for meta, _ in _load("answers"):
        for i in meta.get("items", []) or []:
            key = i.get("ko", "")
            if key and key not in seen:
                seen[key] = {"ko": key, "en": i.get("en", ""),
                             "region": i.get("region", "multi"),
                             "priority": i.get("priority", "normal")}
            elif key and i.get("priority") == "high":
                seen[key]["priority"] = "high"
    return sorted(seen.values(), key=lambda x: (x["region"], x["ko"]))


def export_answers_stats() -> dict:
    stats = {"total": 0, "numbered": 0, "byRegion": {}}
    for meta, _ in _load("answers"):
        stats["total"] += int(meta.get("n_items", 0))
        stats["numbered"] += int(meta.get("n_numbered", 0))
        for i in meta.get("items", []) or []:
            r = i.get("region", "multi")
            stats["byRegion"][r] = stats["byRegion"].get(r, 0) + 1
    return stats


def export_sources() -> list[dict]:
    out = []
    for meta, _ in _load("sources"):
        if meta.get("kind") != "source_doc":
            continue
        out.append({
            "name": meta.get("source_file_name", meta.get("source_id", "")),
            "folder": meta.get("subtopic", ""),
            "status": meta.get("status", ""),
            "pages": meta.get("pages"),
            "session": meta.get("session_no"),
        })
    return out


def main() -> int:
    schedule = [{
        "date": s["date"].isoformat(), "topics": s["topics"],
        "regions": s.get("regions", []), "exam": s.get("exam"),
    } for s in sched.SCHEDULE_2026]
    payload = {
        "generated": date.today().isoformat(),
        "deadlines": {"tagging1": sched.TAGGING_1.isoformat(),
                      "tagging2": sched.TAGGING_2.isoformat(),
                      "end": sched.END_DATE.isoformat()},
        "schedule": schedule,
        "concepts": export_concepts(),
        "questions": export_questions(),
        "daily": export_daily(),
        "glossary": export_glossary(),
        "answersStats": export_answers_stats(),
        "sources": export_sources(),
    }
    blob = json.dumps(payload, ensure_ascii=False, indent=1)
    for bad in FORBIDDEN_SUBSTR:
        if bad in blob:
            print(f"[FAIL] 금지 문자열이 번들에 포함됨: {bad} — 내보내기 중단")
            return 1
    OUT.write_text(
        "// 자동 생성 파일 — 수정하지 마세요.\n"
        "// 원본: content/anatomy/**/*.md → `python pipelines/export_anatomy_web.py`\n"
        "window.MEDKOS_ANATOMY = " + blob + ";\n",
        encoding="utf-8",
    )
    print(f"생성: {OUT.relative_to(ROOT)} (개념 {len(payload['concepts'])} · "
          f"문항 {len(payload['questions'])} · 용어 {len(payload['glossary'])} · "
          f"daily {len(payload['daily'])})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
