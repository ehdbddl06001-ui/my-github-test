"""
apply_notes.py — 홈페이지에서 내보낸 논문 노트(.json)를 각 카드의 ## My Ideas 에 반영한다.

홈페이지(docs/papers.html)의 '내 생각/아이디어'는 브라우저(localStorage)에만 남는다.
'🗒 내 노트 내보내기(.json)'로 받은 medkos-notes.json 을 이 스크립트에 넘기면,
해당 논문 카드(content/papers/**/*.md)의 ## My Ideas 섹션에 노트를 써 넣는다.
그러면 노트가 GitHub(버전관리)·Google Drive(백업)에 영구 저장되고, 다시 웹으로 배포된다.

입력 형식(둘 다 허용):
  { "paper-2026-0001": { "text": "…", "updated": "2026-07-02T…" }, ... }
  { "paper-2026-0001": "…", ... }

사용:
  python pipelines/apply_notes.py medkos-notes.json
  python pipelines/apply_notes.py medkos-notes.json --dry-run
그 다음:
  python pipelines/indexer.py --check && python pipelines/indexer.py
  python pipelines/export_papers_web.py
  git add content/papers docs/papers.js && git commit -m "논문 노트 반영" && git push
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

from frontmatter import load

ROOT = Path(__file__).resolve().parent.parent
PAPERS_DIR = ROOT / "content" / "papers"
IDEAS_HEADER = "## My Ideas"


def index_cards() -> dict[str, Path]:
    """frontmatter id → 파일 경로."""
    out: dict[str, Path] = {}
    for p in PAPERS_DIR.rglob("*.md"):
        d = load(p)
        if d.id:
            out[d.id] = p
    return out


def set_updated(text: str, when: str) -> str:
    """frontmatter 블록의 updated: 를 추가하거나 교체한다."""
    if not text.startswith("---"):
        return text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return text
    fm = parts[1]
    if re.search(r"^updated:.*$", fm, flags=re.M):
        fm = re.sub(r"^updated:.*$", f"updated: {when}", fm, flags=re.M)
    else:
        fm = fm.rstrip("\n") + f"\nupdated: {when}\n"
    return "---" + fm + "---" + parts[2]


def replace_ideas(text: str, note: str) -> str:
    """## My Ideas 섹션 본문을 note 로 교체(다음 '## ' 헤더 전까지). 없으면 끝에 추가."""
    block = f"{IDEAS_HEADER}\n{note.rstrip()}\n"
    if IDEAS_HEADER not in text:
        sep = "" if text.endswith("\n") else "\n"
        return text + sep + "\n" + block
    before, after = text.split(IDEAS_HEADER, 1)
    # My Ideas 다음에 또 다른 섹션이 있으면 그 앞까지만 교체
    m = re.search(r"\n## ", after)
    tail = after[m.start():] if m else ""
    return before + block + (tail + "\n" if tail else "")


def main() -> int:
    ap = argparse.ArgumentParser(description="브라우저 논문 노트(.json)를 카드 My Ideas에 반영")
    ap.add_argument("notes_json", help="홈페이지에서 내보낸 medkos-notes.json")
    ap.add_argument("--dry-run", action="store_true", help="쓰지 않고 무엇이 바뀔지만 출력")
    args = ap.parse_args()

    try:
        data = json.loads(Path(args.notes_json).read_text(encoding="utf-8"))
    except Exception as e:
        print(f"노트 파일을 읽을 수 없습니다: {e}", file=sys.stderr)
        return 2

    cards = index_cards()
    applied, missing = 0, []
    today = date.today().isoformat()

    for doc_id, val in data.items():
        note = val.get("text", "") if isinstance(val, dict) else str(val)
        when = (val.get("updated", "") or "")[:10] if isinstance(val, dict) else ""
        when = when or today
        if not note.strip():
            continue
        path = cards.get(doc_id)
        if not path:
            missing.append(doc_id)
            continue
        text = path.read_text(encoding="utf-8")
        new = set_updated(replace_ideas(text, note), when)
        if args.dry_run:
            print(f"[DRY] {doc_id} → {path.relative_to(ROOT)}  ({len(note)}자)")
        else:
            path.write_text(new, encoding="utf-8")
            print(f"반영 {doc_id} → {path.relative_to(ROOT)}")
        applied += 1

    print(f"\n{'반영 예정' if args.dry_run else '반영'} {applied}건" +
          (f", 매칭 실패 {len(missing)}건: {', '.join(missing)}" if missing else ""))
    if not args.dry_run and applied:
        print("다음: python pipelines/indexer.py --check && python pipelines/export_papers_web.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
