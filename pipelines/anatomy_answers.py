"""
anatomy_answers.py — 답만 있는 자료(`tagging 2차.pdf`)의 결정론 파싱.

텍스트 스냅샷(`.private/anatomy/text/a2-tagging2.txt`)에서:
  - `NN. 구조명(english)` → 번호 항목 = 과거 태깅 답 후보:
      answer_only_candidate: true, priority: high
  - `● / • 구조명(english)` → 번호 없는 항목 = 같은 부위의 후보/교란/관계 학습용.
      "시험에 안 나온 항목"이라고 단정하지 않는다(priority: normal).
  - 원래 질문·핀 위치·사진은 **복원하지 않는다**(없는 것을 아는 척 금지, spec D5).

출력: `content/anatomy/answers/<sid>.md` (kind: answer_list, items[] frontmatter).
재실행 idempotent(파일 갱신만, id 유지).

사용:
  python pipelines/anatomy_answers.py --source-id a2-tagging2 [--dry-run]
"""
from __future__ import annotations

import argparse
import re
import sys
import unicodedata
from datetime import date
from pathlib import Path

try:
    from frontmatter import split_frontmatter
    from anatomy_extract import extract_terms
    from anatomy_classify import classify_region, classify_structures
except ModuleNotFoundError:
    from pipelines.frontmatter import split_frontmatter
    from pipelines.anatomy_extract import extract_terms
    from pipelines.anatomy_classify import classify_region, classify_structures

import yaml

ROOT = Path(__file__).resolve().parent.parent
ANSWERS_DIR = ROOT / "content" / "anatomy" / "answers"
DEFAULT_PRIVATE = ROOT / ".private" / "anatomy"

NUMBERED_RE = re.compile(r"^(\d{1,3})\\?\.\s*(.+)$")
BULLET_RE = re.compile(r"^[●•]\s*(.+)$")
GROUP_RE = re.compile(r"^\\?\[\s*(.+?)\s*\\?\]$")
# region 헤더: "Upper Limb: Axilla" / "머리 Head : Orbit" / "배벽 Abdominal wall" 등
HEADER_RE = re.compile(
    r"^(?!\d)(?=.*[A-Za-z]{3})(?![●•\\\[])(.{2,60})$"
)
HEADER_TOKENS = ["limb", "head", "pharynx", "larynx", "abdominal", "pelvis",
                 "perineum", "thorax", "back", "neck", "wall", "cavity",
                 "orbit", "ear", "hand", "tongue", "skull"]

# region 헤더 → region (헤더가 있으면 개별 용어 키워드보다 우선한다)
HEADER_REGION = [
    ("upper limb", "upper-limb"), ("lower limb", "lower-limb"),
    ("skull", "head"), ("head", "head"), ("orbit", "head"), ("ear", "head"),
    ("tongue", "head"), ("pharynx", "neck"), ("larynx", "neck"), ("neck", "neck"),
    ("abdominal", "abdomen"), ("perineum", "pelvis-perineum"),
    ("pelvis", "pelvis-perineum"), ("thorax", "thorax"), ("back", "back"),
]


def header_region(header: str) -> str | None:
    low = header.lower()
    for token, region in HEADER_REGION:
        if token in low:
            return region
    return None


def parse_items(text: str) -> list[dict]:
    items: list[dict] = []
    region_header = ""
    group = ""
    for raw in unicodedata.normalize("NFC", text).splitlines():
        ln = raw.strip()
        if not ln:
            continue
        g = GROUP_RE.match(ln)
        if g:
            group = g.group(1)
            continue
        m = NUMBERED_RE.match(ln)
        b = BULLET_RE.match(ln) if not m else None
        if m or b:
            body = (m.group(2) if m else b.group(1)).strip()
            terms = extract_terms(body)
            ko = terms[0]["ko"] if terms else re.sub(r"\(.*$", "", body).strip()
            en = terms[0]["en"] if terms else ""
            if not ko:
                continue
            region = header_region(region_header)
            if not region:
                region, _conf = classify_region(" ".join([region_header, group, ko]))
            items.append({
                "no": int(m.group(1)) if m else None,
                "ko": ko, "en": en,
                "region_header": region_header, "group": group,
                "region": region,
                "structure_classes": classify_structures([{"ko": ko, "en": en}]),
                "answer_only_candidate": bool(m),
                "priority": "high" if m else "normal",
            })
            continue
        low = ln.lower()
        if HEADER_RE.match(ln) and any(t in low for t in HEADER_TOKENS) \
                and "(" not in ln and len(ln) < 60:
            region_header = ln
            group = ""
    return items


def run(private: Path, sid: str, dry: bool) -> int:
    snap = private / "text" / f"{sid}.txt"
    if not snap.exists():
        print(f"[INFO] 스냅샷 없음: {snap} — 기존 카드 유지")
        return 0
    src_card = ROOT / "content" / "anatomy" / "sources" / f"{sid}.md"
    if not src_card.exists():
        print(f"[FAIL] source_doc 카드 없음: {sid}")
        return 1
    src, _ = split_frontmatter(src_card.read_text(encoding="utf-8"))
    items = parse_items(snap.read_text(encoding="utf-8"))
    if not items:
        print("[FAIL] 파싱 결과 0건 — 빈 결과를 커밋하지 않는다")
        return 1
    out = ANSWERS_DIR / f"{sid}.md"
    old_id = None
    if out.exists():
        old, _ = split_frontmatter(out.read_text(encoding="utf-8"))
        old_id = old.get("id")
    n_num = sum(1 for i in items if i["answer_only_candidate"])
    today = date.today().isoformat()
    meta = {
        "id": old_id or f"anatomy-ans-{sid}",
        "type": "anatomy", "kind": "answer_list", "topic": "Anatomy",
        "subtopic": "Tagging 2 answer-only material",
        "date": today, "updated": today,
        "confidence": "medium",  # 항목은 실측이지만 '과거 답'인지는 번호 표기 추정
        "source": src.get("source_file_name", sid),
        "source_id": sid, "source_file_id": src["source_file_id"],
        "exam_phase": "tagging-2",
        "n_items": len(items), "n_numbered": n_num,
        "publishable": False,
        "items": items,
    }
    by_region: dict[str, int] = {}
    for i in items:
        by_region[i["region"]] = by_region.get(i["region"], 0) + 1
    body = (
        "## Answer-only 자료 파싱 결과\n\n"
        f"- 총 {len(items)}개 구조물, 번호 항목(과거 태깅 답 후보) {n_num}개.\n"
        f"- 부위 분포: " + ", ".join(f"{k} {v}" for k, v in sorted(by_region.items())) + "\n\n"
        "> 번호 항목은 `answer_only_candidate: true / priority: high`로만 기록한다.\n"
        "> 원래 질문·핀 위치·사진을 복원한 것처럼 가장하지 않는다. 새 문항은 강의\n"
        "> PDF에서 같은 구조가 확인될 때만 생성한다(아니면 needs_review 격리).\n"
    )
    if not dry:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text("---\n" + yaml.safe_dump(
            meta, allow_unicode=True, sort_keys=False, default_flow_style=None, width=100
        ) + "---\n\n" + body, encoding="utf-8")
    print(f"answers {sid}: {len(items)}개(번호 {n_num}){' (dry-run)' if dry else ''}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source-id", default="a2-tagging2")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--private-assets-dir", default=str(DEFAULT_PRIVATE))
    a = ap.parse_args()
    private = Path(a.private_assets_dir)
    if not private.is_absolute():
        private = ROOT / private
    return run(private, a.source_id, a.dry_run)


if __name__ == "__main__":
    sys.exit(main())
