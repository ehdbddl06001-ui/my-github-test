"""
anatomy_inventory.py — Drive 폴더 목록(listing JSON) → source_doc 카드(manifest).

Drive 조회는 세션(MCP)만 할 수 있으므로, 이 스크립트는 세션이 저장한 listing JSON을
입력으로 받아 `content/anatomy/sources/<source-id>.md` (kind: source_doc) 카드를
결정론적으로 만들거나 갱신한다. manifest의 SoT는 이 카드들이다(별도 상태 JSON 없음).

listing JSON 형식(세션이 MCP search_files 결과에서 추출):
  {"folders": {"해부1": "<folderId>", ...},
   "files": [{"id","title","fileSize","modifiedTime","mimeType","folder"}...]}

규칙:
- 같은 file ID 재실행 → 카드 갱신만(중복 생성 없음, idempotent).
- 같은 file ID인데 modifiedTime/size가 바뀌면 revision을 올리고 status를 `stale`로.
- listing에 없다고 기존 카드를 지우지 않는다(네트워크 부재 안전).
- 1회차·8회차(Tagging 1 원본) 부재는 missing_sources 카드에 기록만(추측 생성 금지).

사용:
  python pipelines/anatomy_inventory.py --listing state/.anatomy_listing.json [--dry-run]
  python pipelines/anatomy_inventory.py --check     # 카드 무결성 검증만
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from datetime import date
from pathlib import Path

try:
    from frontmatter import load, split_frontmatter
except ModuleNotFoundError:
    from pipelines.frontmatter import load, split_frontmatter

import yaml

ROOT = Path(__file__).resolve().parent.parent
SOURCES_DIR = ROOT / "content" / "anatomy" / "sources"

FOLDER_SLUG = {"해부1": "a1", "해부2": "a2"}
# 알려진 회차 목록(2026 시간표 기준 15차시 + tagging). 1·8회차 원본은 현재 Drive에 없다.
EXPECTED_SESSIONS = list(range(1, 16))


def source_id_for(title: str, folder: str) -> str:
    """결정론 source-id. 예: '14차시(0930) 문용석pf.pdf' + 해부2 → 'a2-s14'."""
    slug = FOLDER_SLUG.get(folder, re.sub(r"[^a-z0-9]+", "", folder.lower()) or "ax")
    t = unicodedata.normalize("NFC", title)
    m = re.match(r"^\s*(\d+)\s*(?:회차|차시)", t)
    if m:
        return f"{slug}-s{int(m.group(1)):02d}"
    if "tagging" in t.lower():
        m2 = re.search(r"(\d+)", t)
        return f"{slug}-tagging{m2.group(1) if m2 else ''}"
    if "수업계획서" in t:
        return f"{slug}-plan"
    base = re.sub(r"[^0-9A-Za-z가-힣]+", "-", t.rsplit(".", 1)[0]).strip("-").lower()
    return f"{slug}-{base[:40]}"


def session_no(title: str) -> int | None:
    m = re.match(r"^\s*(\d+)\s*(?:회차|차시)", unicodedata.normalize("NFC", title))
    return int(m.group(1)) if m else None


def _dump_yaml(meta: dict) -> str:
    return yaml.safe_dump(meta, allow_unicode=True, sort_keys=False,
                          default_flow_style=None, width=100)


def card_path(source_id: str) -> Path:
    return SOURCES_DIR / f"{source_id}.md"


def load_existing() -> dict[str, dict]:
    """기존 source_doc 카드 → {source_file_id: meta}."""
    out: dict[str, dict] = {}
    if SOURCES_DIR.exists():
        for p in sorted(SOURCES_DIR.glob("*.md")):
            meta, _ = split_frontmatter(p.read_text(encoding="utf-8"))
            if meta.get("kind") == "source_doc" and meta.get("source_file_id"):
                meta["_path"] = p
                out[str(meta["source_file_id"])] = meta
    return out


def build_card(f: dict, existing: dict | None, today: str) -> tuple[dict, bool]:
    """listing 항목 → source_doc frontmatter. (meta, changed) 반환."""
    sid = source_id_for(f["title"], f.get("folder", ""))
    sess = session_no(f["title"])
    fresh = {
        "id": existing.get("id") if existing else f"anatomy-src-{sid}",
        "type": "anatomy",
        "kind": "source_doc",
        "topic": "Anatomy",
        "subtopic": f.get("folder", ""),
        "date": str(existing.get("date")) if existing else today,
        "updated": today,
        "confidence": "high",  # 파일 메타는 Drive 실측
        "source": "Google Drive (3Q 해부학)",
        "source_id": sid,
        "source_file_id": f["id"],
        "source_file_name": f["title"],
        "file_size": int(f.get("fileSize", 0) or 0),
        "modified_time": f.get("modifiedTime", ""),
        "mime_type": f.get("mimeType", ""),
        "session_no": sess,
        # 과거 학기 파일명 날짜는 일정으로 쓰지 않는다(anatomy_schedule.py가 단일 기준).
        "legacy_filename_date": True,
        "sha256": existing.get("sha256") if existing else None,
        "revision": existing.get("revision", 1) if existing else 1,
        "status": existing.get("status", "listed") if existing else "listed",
        "pages": existing.get("pages") if existing else None,
        "publishable": False,
    }
    changed = True
    if existing:
        same = (existing.get("modified_time") == fresh["modified_time"]
                and int(existing.get("file_size", 0)) == fresh["file_size"])
        if same:
            changed = False
        else:
            fresh["revision"] = int(existing.get("revision", 1)) + 1
            fresh["status"] = "stale"  # 재-ingest 필요
    return fresh, changed


def body_for(meta: dict) -> str:
    return (
        f"## Source\n\n"
        f"- 파일: `{meta['source_file_name']}` (Drive file ID `{meta['source_file_id']}`)\n"
        f"- 폴더: {meta['subtopic']} · 크기 {meta['file_size']:,} bytes · "
        f"Drive modified {meta['modified_time']}\n"
        f"- 처리 상태: `{meta['status']}` · revision {meta['revision']}\n\n"
        f"> 원본 PDF는 커밋하지 않는다. 페이지 파생물은 `.private/anatomy/`(git 무시),\n"
        f"> 커밋되는 것은 용어·분류·관계 카드뿐이다.\n"
    )


def write_card(meta: dict, dry: bool) -> Path:
    meta = {k: v for k, v in meta.items() if not k.startswith("_")}
    p = card_path(meta["source_id"])
    text = f"---\n{_dump_yaml(meta)}---\n\n{body_for(meta)}"
    if not dry:
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")
    return p


def write_missing_card(missing: list[int], today: str, dry: bool) -> Path:
    p = SOURCES_DIR / "missing-sources.md"
    old = {}
    if p.exists():
        old, _ = split_frontmatter(p.read_text(encoding="utf-8"))
    meta = {
        "id": old.get("id", "anatomy-src-missing"),
        "type": "anatomy", "kind": "source_doc", "topic": "Anatomy",
        "subtopic": "missing_source",
        "date": str(old.get("date", today)), "updated": today,
        "confidence": "high", "source": "Google Drive (3Q 해부학)",
        "source_id": "missing", "source_file_id": "missing_source",
        "status": "missing_source", "missing_sessions": missing,
        "publishable": False, "revision": int(old.get("revision", 0)) + 1,
    }
    body = (
        "## Missing sources\n\n"
        f"- Drive에 원본이 없는 회차: {', '.join(str(m) for m in missing)}\n"
        "- 1회차(orientation), 8회차(Tagging 1 원본)는 현재 폴더에 없다.\n"
        "- **없는 파일을 추측해 만들지 않는다** — 업로드되면 inventory가 자동 반영한다.\n"
    )
    if not dry:
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(f"---\n{_dump_yaml(meta)}---\n\n{body}", encoding="utf-8")
    return p


def run(listing_path: Path, dry: bool) -> int:
    if not listing_path.exists():
        print(f"[SKIP] listing 없음: {listing_path} — 기존 manifest 유지(아무것도 지우지 않음)")
        return 0
    listing = json.loads(listing_path.read_text(encoding="utf-8"))
    files = listing.get("files", [])
    if not files:
        print("[SKIP] listing이 비어 있음 — 기존 manifest 유지")
        return 0
    existing = load_existing()
    today = date.today().isoformat()
    n_new = n_upd = n_same = 0
    seen_sessions: set[int] = set()
    for f in sorted(files, key=lambda x: x["id"]):
        old = existing.get(f["id"])
        meta, changed = build_card(f, old, today)
        if meta.get("session_no"):
            seen_sessions.add(meta["session_no"])
        if old and not changed:
            n_same += 1
            continue
        write_card(meta, dry)
        if old:
            n_upd += 1
        else:
            n_new += 1
    missing = [s for s in EXPECTED_SESSIONS if s not in seen_sessions]
    write_missing_card(missing, today, dry)
    print(f"inventory: 신규 {n_new} · 갱신 {n_upd} · 변경없음 {n_same} · "
          f"누락 회차 {missing}{' (dry-run)' if dry else ''}")
    return 0


def check() -> int:
    bad = 0
    if SOURCES_DIR.exists():
        for p in sorted(SOURCES_DIR.glob("*.md")):
            d = load(p)
            if d.errors:
                bad += 1
                print(f"[FAIL] {p}: {d.errors}")
    print("sources 검증 통과" if not bad else f"sources 검증 실패 {bad}건")
    return 1 if bad else 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--listing", default="state/.anatomy_listing.json")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    if a.check:
        return check()
    return run(ROOT / a.listing if not Path(a.listing).is_absolute() else Path(a.listing), a.dry_run)


if __name__ == "__main__":
    sys.exit(main())
