"""
anatomy_classify.py — 페이지/섹션 텍스트 → 부위·층·구조종류 분류 + source_page 카드 생성.

입력:
  binary lane: `.private/anatomy/extract/<sid>/rev-<n>/page-NNNN.json`
  text lane  : `.private/anatomy/text/<sid>.txt` (Drive MCP 스냅샷 — 페이지 번호 없음)
출력:
  `content/anatomy/pages/<sid>/page-NNNN.md`  (binary lane)
  `content/anatomy/pages/<sid>/sec-NN-<slug>.md` (text lane)

카드에는 **용어 목록·분류·관계 요약만** 담는다 — 강의 원문 전문을 커밋하지 않는다
(저작권, spec D3). 분류 confidence가 임계값(0.6) 미만이면 needs_review: true.
2026 일정 매핑은 anatomy_schedule.py 의 SCHEDULE_2026 로만 한다(과거 날짜 금지).

사용:
  python pipelines/anatomy_classify.py --source-id a2-s14 [--dry-run] [--check]
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
    from anatomy_extract import extract_terms
    from anatomy_schedule import SCHEDULE_2026, TAGGING_1
except ModuleNotFoundError:
    from pipelines.frontmatter import load, split_frontmatter
    from pipelines.anatomy_extract import extract_terms
    from pipelines.anatomy_schedule import SCHEDULE_2026, TAGGING_1

import yaml

ROOT = Path(__file__).resolve().parent.parent
PAGES_DIR = ROOT / "content" / "anatomy" / "pages"
DEFAULT_PRIVATE = ROOT / ".private" / "anatomy"
CONF_THRESHOLD = 0.6

# 부위 키워드(한국어 용어 → region). 결정론 분류의 1차 축.
REGION_KEYWORDS: dict[str, list[str]] = {
    "back": ["등", "척주", "척수", "뒤통수밑", "어깨뼈부위", "볼기"],
    "thorax": ["가슴", "심장", "허파", "세로칸", "갈비", "기관지", "가슴막"],
    "upper-limb": ["팔", "겨드랑", "위팔", "아래팔", "손", "어깨관절", "팔꿉", "손목",
                   "노뼈", "자뼈", "빗장", "부리돌기", "돌림근띠"],
    "lower-limb": ["다리", "넓적다리", "종아리", "발", "무릎", "다리오금", "정강", "종아리뼈"],
    "head": ["머리", "얼굴", "눈확", "귀", "코안", "입안", "혀", "머리뼈", "뇌", "관자"],
    "neck": ["목", "인두", "후두", "갑상", "목뿔"],
    "abdomen": ["배", "복막", "위창자", "간", "지라", "콩팥", "샘창자", "이자", "창자",
                "고샅", "배벽", "가로막", "부신"],
    "pelvis-perineum": ["골반", "샅", "항문", "방광", "자궁", "난소", "전립샘", "음경",
                        "음낭", "질", "곧창자", "정낭", "회음", "요도", "요관"],
}

STRUCTURE_KEYWORDS: dict[str, list[str]] = {
    "artery": ["동맥"], "vein": ["정맥"], "nerve": ["신경"],
    "muscle": ["근", "근육"], "bone": ["뼈"], "joint": ["관절"],
    "ligament": ["인대"], "fascia": ["근막", "널힘줄"],
    "lymphatic": ["림프"], "organ": ["샘", "방광", "자궁", "고환", "난소", "간", "콩팥"],
    "duct": ["관", "요관", "정관"], "foramen": ["구멍", "굴", "틈새"],
}

LAYER_KEYWORDS: dict[str, list[str]] = {
    "skin": ["피부"], "superficial-fascia": ["얕은근막", "피부밑"],
    "deep-fascia": ["깊은근막"], "superficial": ["얕은"],
    "intermediate": ["중간층"], "deep": ["깊은"],
    "cavity-visceral": ["안(", "공간", "내장", "복막"],
}


def classify_region(text: str) -> tuple[str, float]:
    """키워드 히트 비율로 region과 confidence를 계산(결정론)."""
    scores = {r: sum(text.count(k) for k in ks) for r, ks in REGION_KEYWORDS.items()}
    total = sum(scores.values())
    if total == 0:
        return "multi", 0.0
    best = max(sorted(scores), key=lambda r: scores[r])
    conf = scores[best] / total
    if conf < 0.5 and len([s for s in scores.values() if s > 0]) > 1:
        return ("multi", round(conf, 2)) if conf < 0.34 else (best, round(conf, 2))
    return best, round(conf, 2)


def classify_structures(terms: list[dict]) -> list[str]:
    found = set()
    for t in terms:
        ko = t.get("ko", "")
        for cls, kws in STRUCTURE_KEYWORDS.items():
            if any(kw in ko for kw in kws):
                found.add(cls)
                break
    return sorted(found)


def classify_layers(text: str) -> list[str]:
    return sorted({layer for layer, kws in LAYER_KEYWORDS.items()
                   if any(k in text for k in kws)})


def scheduled_dates_for(text: str, region: str) -> list[str]:
    """2026 일정표에서 topic 토큰이 텍스트에 등장하는 수업일을 찾는다(결정론)."""
    hits = []
    for s in SCHEDULE_2026:
        if s.get("exam"):
            continue
        for topic in s["topics"]:
            tokens = [t for t in re.split(r"[·/,\s]+", topic) if len(t) >= 2]
            if tokens and sum(1 for t in tokens if t in text) >= max(1, len(tokens) // 2):
                hits.append(s["date"].isoformat())
                break
    return sorted(set(hits))


def exam_phase_for_dates(dates: list[str]) -> str:
    if not dates:
        return "tagging-2"  # 근거 없으면 남은 시험 쪽으로 두되 needs_review와 함께
    first = date.fromisoformat(dates[0])
    return "tagging-1" if first <= TAGGING_1 else "tagging-2"


def _write_card(path: Path, meta: dict, body: str, dry: bool) -> None:
    if dry:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("---\n" + yaml.safe_dump(
        meta, allow_unicode=True, sort_keys=False, default_flow_style=None, width=100
    ) + "---\n\n" + body, encoding="utf-8")


def build_page_meta(sid: str, file_id: str, file_name: str, text: str,
                    terms: list[dict], today: str, *,
                    page: int | None, section: str | None,
                    existing_id: str | None) -> dict:
    region, conf = classify_region(text)
    dates = scheduled_dates_for(text, region)
    needs_review = conf < CONF_THRESHOLD or not terms
    suffix = f"p{page:04d}" if page else re.sub(r"[^0-9a-z가-힣]+", "-", (section or "sec").lower())[:30]
    meta = {
        "id": existing_id or f"anatomy-pg-{sid}-{suffix}",
        "type": "anatomy", "kind": "source_page",
        "topic": "Anatomy", "subtopic": section or f"page {page}",
        "date": today, "confidence": "medium" if not needs_review else "low",
        "source": file_name,
        "source_id": sid, "source_file_id": file_id, "source_file_name": file_name,
        "source_page": page,
        "region": region, "classification_confidence": conf,
        "structure_classes": classify_structures(terms),
        "layers": classify_layers(text),
        "scheduled_dates": dates,
        "exam_phase": exam_phase_for_dates(dates),
        "terms": [{"ko": t["ko"], "en": t["en"]} for t in terms],
        "publishable": False,
        "needs_review": needs_review,
    }
    if page is None:
        meta["extraction"] = "drive-mcp-text"
        meta["section"] = section or "unknown"
    return meta


def body_for(meta: dict) -> str:
    lines = [f"## 구조물 용어 ({len(meta['terms'])}개)\n"]
    for t in meta["terms"]:
        lines.append(f"- {t['ko']} ({t['en']})")
    lines.append("\n> 분류: region={region} (conf {conf}) · layers={layers} · "
                 "classes={cls}".format(region=meta["region"],
                                        conf=meta["classification_confidence"],
                                        layers=meta["layers"] or "-",
                                        cls=meta["structure_classes"] or "-"))
    lines.append("> 원문 전문은 커밋하지 않는다(저작권) — `.private/anatomy/` 참조.")
    return "\n".join(lines) + "\n"


TEXT_SECTION_RE = re.compile(r"^(?:\\?<(?P<ang>[^>]{2,40})\\?>|(?P<num>\d{1,2})\\?\)\s*(?P<title>\S.{0,40}))\s*$")


def split_sections(text: str) -> list[tuple[str, str]]:
    """text lane 스냅샷 → (섹션제목, 본문) 목록. 헤더가 없으면 전체 1개."""
    lines = text.splitlines()
    sections: list[tuple[str, list[str]]] = []
    cur_title, cur = "본문", []
    for ln in lines:
        m = TEXT_SECTION_RE.match(ln.strip())
        if m:
            if cur and any(s.strip() for s in cur):
                sections.append((cur_title, cur))
            cur_title = (m.group("ang") or m.group("title") or "섹션").strip()
            cur = []
        else:
            cur.append(ln)
    if cur and any(s.strip() for s in cur):
        sections.append((cur_title, cur))
    return [(t, "\n".join(c)) for t, c in sections]


def _existing_ids(sid: str) -> dict[str, str]:
    """이미 만든 카드의 파일명 → id (재실행 시 id 재발급 방지)."""
    out = {}
    d = PAGES_DIR / sid
    if d.exists():
        for p in d.glob("*.md"):
            meta, _ = split_frontmatter(p.read_text(encoding="utf-8"))
            if meta.get("id"):
                out[p.name] = str(meta["id"])
    return out


def _source_card(sid: str) -> dict | None:
    p = ROOT / "content" / "anatomy" / "sources" / f"{sid}.md"
    if not p.exists():
        return None
    meta, _ = split_frontmatter(p.read_text(encoding="utf-8"))
    return meta


def run_text_lane(private: Path, sid: str, dry: bool) -> int:
    src = _source_card(sid)
    if not src:
        print(f"[FAIL] source_doc 카드 없음: {sid}")
        return 1
    snap = private / "text" / f"{sid}.txt"
    if not snap.exists():
        print(f"[INFO] 텍스트 스냅샷 없음: {snap}")
        return 0
    text = unicodedata.normalize("NFC", snap.read_text(encoding="utf-8"))
    today = date.today().isoformat()
    existing = _existing_ids(sid)
    n = 0
    # 섹션이 너무 잘게 쪼개지면(실습 지침의 번호 목록) 큰 덩어리만 카드로 만든다.
    sections = [(t, b) for t, b in split_sections(text) if len(b) >= 250]
    if not sections:
        sections = [("전체", text)]
    for i, (title, body_text) in enumerate(sections, 1):
        terms = extract_terms(body_text)
        slug = re.sub(r"[^0-9A-Za-z가-힣]+", "-", title).strip("-").lower()[:24] or f"s{i}"
        fname = f"sec-{i:02d}-{slug}.md"
        meta = build_page_meta(
            sid, src["source_file_id"], src.get("source_file_name", sid),
            body_text, terms, today, page=None, section=title,
            existing_id=existing.get(fname),
        )
        _write_card(PAGES_DIR / sid / fname, meta, body_for(meta), dry)
        n += 1
    print(f"classify(text lane) {sid}: 섹션 카드 {n}개{' (dry-run)' if dry else ''}")
    return 0


def run_binary_lane(private: Path, sid: str, only_page: int | None, dry: bool) -> int:
    src = _source_card(sid)
    if not src:
        print(f"[FAIL] source_doc 카드 없음: {sid}")
        return 1
    revs = sorted((private / "extract" / sid).glob("rev-*"))
    if not revs:
        print(f"[INFO] extract 산출물 없음 — text lane만 시도 가능: {sid}")
        return 0
    today = date.today().isoformat()
    existing = _existing_ids(sid)
    n = 0
    for ej in sorted(revs[-1].glob("page-*.json")):
        rec = json.loads(ej.read_text(encoding="utf-8"))
        pno = rec["page"]
        if only_page and pno != only_page:
            continue
        text = " ".join(b["text"] for b in rec.get("blocks", []))
        fname = f"page-{pno:04d}.md"
        meta = build_page_meta(
            sid, src["source_file_id"], src.get("source_file_name", sid),
            text, rec.get("terms", []), today, page=pno, section=None,
            existing_id=existing.get(fname),
        )
        if not rec.get("has_text_layer"):
            meta["needs_review"] = True
            meta["confidence"] = "low"
        _write_card(PAGES_DIR / sid / fname, meta, body_for(meta), dry)
        n += 1
    print(f"classify(binary lane) {sid}: 페이지 카드 {n}개{' (dry-run)' if dry else ''}")
    return 0


def check() -> int:
    bad = 0
    if PAGES_DIR.exists():
        for p in sorted(PAGES_DIR.rglob("*.md")):
            d = load(p)
            if d.errors:
                bad += 1
                print(f"[FAIL] {p}: {d.errors}")
    print("pages 검증 통과" if not bad else f"pages 검증 실패 {bad}건")
    return 1 if bad else 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source-id")
    ap.add_argument("--page", type=int)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--private-assets-dir", default=str(DEFAULT_PRIVATE))
    a = ap.parse_args()
    if a.check:
        return check()
    if not a.source_id:
        print("--source-id 필요(또는 --check)")
        return 2
    private = Path(a.private_assets_dir)
    if not private.is_absolute():
        private = ROOT / private
    rc = run_binary_lane(private, a.source_id, a.page, a.dry_run)
    rc2 = run_text_lane(private, a.source_id, a.dry_run)
    return rc or rc2


if __name__ == "__main__":
    sys.exit(main())
