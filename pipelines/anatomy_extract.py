"""
anatomy_extract.py — 페이지별 텍스트 블록 + bounding box 추출(binary lane).

`.private/anatomy/originals/<source-id>.pdf` 를 열어 페이지마다
`.private/anatomy/extract/<source-id>/rev-<n>/page-NNNN.json` 을 만든다:

  {"page": 12, "width": 595, "height": 842, "has_text_layer": true,
   "blocks": [{"text": "겨드랑동맥(axillary artery)", "bbox": [x0,y0,x1,y1]}, ...],
   "terms": [{"ko": "겨드랑동맥", "en": "axillary artery", "bbox": [...]}, ...]}

- 텍스트 레이어가 없는 페이지는 `has_text_layer: false` 로 기록한다. 이 컨테이너에는
  OCR 엔진이 없으므로(spec D6) 그런 페이지는 **자동 공개 금지 + review queue**가
  기본값이다 — 가짜 OCR 결과를 만들지 않는다.
- 재실행 idempotent: 이미 있는 JSON은 건너뛴다(--force 로 재추출).

사용:
  python pipelines/anatomy_extract.py [--source-id a2-s14] [--page 12] [--force]
      [--private-assets-dir .private/anatomy]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_PRIVATE = ROOT / ".private" / "anatomy"

# '한국어명(english name)' 페어 — 강의 PDF·tagging 자료의 지배적 표기 규약.
TERM_RE = re.compile(
    r"([가-힣][가-힣0-9·\s]{0,30}?)\s*\(\s*([A-Za-z][A-Za-z\s,\-']{2,60}?)\s*\)"
)


def extract_terms(text: str) -> list[dict]:
    out = []
    for m in TERM_RE.finditer(text):
        ko = m.group(1).strip()
        en = re.sub(r"\s+", " ", m.group(2).strip())
        if ko and en:
            out.append({"ko": ko, "en": en})
    return out


def extract_page(page) -> dict:
    """PyMuPDF page → 블록/용어 dict."""
    d = page.get_text("dict")
    blocks = []
    for b in d.get("blocks", []):
        if b.get("type") != 0:  # 텍스트 블록만
            continue
        text = " ".join(
            s["text"] for line in b.get("lines", []) for s in line.get("spans", [])
        ).strip()
        if text:
            blocks.append({"text": text, "bbox": list(b["bbox"])})
    terms = []
    for blk in blocks:
        for t in extract_terms(blk["text"]):
            t["bbox"] = blk["bbox"]
            terms.append(t)
    return {
        "width": d.get("width"), "height": d.get("height"),
        "has_text_layer": bool(blocks),
        "blocks": blocks, "terms": terms,
    }


def run(private: Path, only_sid: str | None, only_page: int | None, force: bool) -> int:
    import fitz

    originals = private / "originals"
    if not originals.exists():
        print(f"[INFO] {originals} 없음 — extract 대상 없음")
        return 0
    errors = []
    n = 0
    for pdf in sorted(originals.glob("*.pdf")):
        sid = pdf.stem
        if only_sid and sid != only_sid:
            continue
        # 최신 rev 디렉토리와 짝을 맞춘다(없으면 rev-1).
        revs = sorted((private / "pages" / sid).glob("rev-*")) or [Path("rev-1")]
        rev_name = revs[-1].name
        out_dir = private / "extract" / sid / rev_name
        try:
            doc = fitz.open(pdf)
            for i in range(doc.page_count):
                pno = i + 1
                if only_page and pno != only_page:
                    continue
                out = out_dir / f"page-{pno:04d}.json"
                if out.exists() and not force:
                    continue
                rec = {"source_id": sid, "page": pno, **extract_page(doc[i])}
                out.parent.mkdir(parents=True, exist_ok=True)
                out.write_text(json.dumps(rec, ensure_ascii=False), encoding="utf-8")
                n += 1
            doc.close()
        except Exception as e:
            errors.append({"source_id": sid, "error": str(e)})
    for e in errors:
        print(f"[FAIL] {e['source_id']}: {e['error']}")
    print(f"extract 완료: {n}페이지")
    return 1 if errors else 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source-id")
    ap.add_argument("--page", type=int)
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--private-assets-dir", default=str(DEFAULT_PRIVATE))
    a = ap.parse_args()
    private = Path(a.private_assets_dir)
    if not private.is_absolute():
        private = ROOT / private
    return run(private, a.source_id, a.page, a.force)


if __name__ == "__main__":
    sys.exit(main())
