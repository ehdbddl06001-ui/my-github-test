"""
anatomy_mask.py — 페이지 이미지에서 '명칭(label) 영역만' 가리는 마스크 생성·검증.

원칙(spec §8):
  1) 원본 이미지는 절대 변경하지 않는다 — 원본 PNG · mask JSON · quiz render 분리.
  2) 마스크 대상은 텍스트 레이어 bbox에서 찾은 해부 용어 label. leader line/pin/
     화살표/방향표시(L/R 등)는 텍스트가 아니므로 건드리지 않는다.
  3) label bbox + padding → mask polygon JSON (`.private/anatomy/masks/`).
  4) quiz render는 label을 불투명 중립색 박스로 가린 별도 PNG.
  5) 검증: 정답 용어의 **모든** 출현 bbox가 마스크에 완전히 포함되어야 한다.
     하나라도 밖에 있으면 그 페이지는 `leak` — 자동 공개 금지, review queue.
  6) 텍스트 레이어가 없으면(OCR 엔진 부재, spec D6) 마스크를 만들지 않고
     review queue로 보낸다. 가짜 마스크를 만들지 않는다.
  7) publishable 은 이 스크립트가 절대 true로 만들지 않는다(사람 검수 전용).

사용:
  python pipelines/anatomy_mask.py --source-id a2-s14 [--page 3] [--dry-run]
      [--private-assets-dir .private/anatomy] [--contact-sheet]
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_PRIVATE = ROOT / ".private" / "anatomy"
PAD = 3.0          # pt — label bbox 주위 여유
NEUTRAL = (73, 84, 100)  # 불투명 중립색

# 방향표시·기호 등 마스크 금지 토큰(역할 보존 — spec §8-4)
KEEP_TOKENS = {"L", "R", "A", "P", "ant", "post", "anterior", "posterior",
               "medial", "lateral", "sup", "inf"}


def is_label_term(term: dict) -> bool:
    """마스크 대상 여부: ko(en) 페어로 검출된 해부 용어만. 방향표시는 제외."""
    en = term.get("en", "").strip()
    return bool(term.get("ko")) and en.lower() not in {t.lower() for t in KEEP_TOKENS}


def build_masks(extract_rec: dict, pad: float = PAD) -> dict:
    """추출 JSON → mask JSON. 텍스트 레이어 없으면 status=needs_review."""
    if not extract_rec.get("has_text_layer"):
        return {"source_id": extract_rec.get("source_id"),
                "page": extract_rec.get("page"),
                "status": "needs_review",
                "reason": "no_text_layer_and_no_ocr",
                "masks": []}
    masks = []
    for t in extract_rec.get("terms", []):
        if not is_label_term(t):
            continue
        x0, y0, x1, y1 = t["bbox"]
        masks.append({
            "label_ko": t["ko"], "label_en": t["en"],
            "polygon": [[x0 - pad, y0 - pad], [x1 + pad, y0 - pad],
                        [x1 + pad, y1 + pad], [x0 - pad, y1 + pad]],
        })
    # 번호핀: 위→아래, 왼→오른 순으로 결정론 배번(문항이 ①②…로 참조)
    for i, m in enumerate(sorted(masks, key=lambda m: (m["polygon"][0][1],
                                                       m["polygon"][0][0])), 1):
        m["pin"] = i
    rec = {"source_id": extract_rec.get("source_id"),
           "page": extract_rec.get("page"),
           "status": "masked" if masks else "no_labels",
           "masks": masks}
    # 재작화 권고 휴리스틱: 가린 면적이 크거나 라벨이 너무 많으면 패치로도
    # 어색함이 남는다 → 원본 게시 대신 클로드 자체 제작 SVG 재작화를 권고.
    w = extract_rec.get("width") or 595
    h = extract_rec.get("height") or 842
    area = sum((m["polygon"][2][0] - m["polygon"][0][0])
               * (m["polygon"][2][1] - m["polygon"][0][1]) for m in masks)
    if masks and (area / (w * h) > 0.08 or len(masks) > 12):
        rec["redraw_recommended"] = True
    return rec


def _inside(bbox: list[float], polygon: list[list[float]]) -> bool:
    """bbox가 (축정렬) polygon 사각형 안에 완전히 들어가는가."""
    xs = [p[0] for p in polygon]
    ys = [p[1] for p in polygon]
    return (bbox[0] >= min(xs) and bbox[1] >= min(ys)
            and bbox[2] <= max(xs) and bbox[3] <= max(ys))


def verify_leakage(extract_rec: dict, mask_rec: dict) -> dict:
    """마스크 밖에 정답 문자열이 남아 있는지 재검사(텍스트 레이어 기반).

    반환: {"ok": bool, "leaks": [{"term", "bbox"}...]}
    마스킹된 용어의 모든 출현(같은 ko 또는 en)이 어느 마스크에든 완전히 포함돼야 한다.
    """
    masked_terms = {(m["label_ko"], m["label_en"]) for m in mask_rec.get("masks", [])}
    if not masked_terms:
        return {"ok": True, "leaks": []}
    kos = {k for k, _ in masked_terms}
    ens = {e.lower() for _, e in masked_terms}
    polygons = [m["polygon"] for m in mask_rec["masks"]]
    leaks = []
    for blk in extract_rec.get("blocks", []):
        text = blk.get("text", "")
        hit = any(k in text for k in kos) or any(e in text.lower() for e in ens)
        if hit and not any(_inside(blk["bbox"], poly) for poly in polygons):
            leaks.append({"text": text[:60], "bbox": blk["bbox"]})
    return {"ok": not leaks, "leaks": leaks}


def _sample_bg(img, box: list[float], margin: int = 6) -> tuple[int, int, int]:
    """마스크 사각형 바로 바깥 띠에서 채널별 중앙값 색을 뽑는다(자연 패치용).

    결정론(중앙값)이고, 결과는 항상 불투명 단색이라 정답이 비칠 수 없다.
    띠를 못 만들면(이미지 가장자리 등) NEUTRAL로 폴백.
    """
    x0, y0, x1, y1 = (int(v) for v in box)
    ox0, oy0 = max(0, x0 - margin), max(0, y0 - margin)
    ox1, oy1 = min(img.width, x1 + margin), min(img.height, y1 + margin)
    px = img.load()
    samples = []
    for x in range(ox0, ox1):
        for y in list(range(oy0, min(y0, oy1))) + list(range(max(y1, oy0), oy1)):
            samples.append(px[x, y])
    for y in range(max(oy0, y0), min(oy1, y1)):
        for x in list(range(ox0, min(x0, ox1))) + list(range(max(x1, ox0), ox1)):
            samples.append(px[x, y])
    if not samples:
        return NEUTRAL
    med = tuple(sorted(s[c] for s in samples)[len(samples) // 2] for c in range(3))
    return med


PIN_FILL = (234, 179, 8)     # 번호핀 원
PIN_TEXT = (14, 24, 38)      # 번호 숫자


def render_quiz(page_png: Path, mask_rec: dict, page_size: tuple[float, float],
                out_png: Path, style: str = "patch") -> None:
    """원본 PNG는 그대로 두고, 마스크를 덮은 문제용 PNG를 별도로 만든다.

    style="patch"(기본): 주변 배경색을 샘플링해 메워 어색한 구멍을 줄이고,
    각 자리에 번호핀(①②… 대응 숫자)을 찍는다. style="box": 과거의 중립색 박스.
    어느 쪽이든 채움은 완전 불투명 — 정답 텍스트는 절대 비치지 않는다.
    """
    from PIL import Image, ImageDraw

    img = Image.open(page_png).convert("RGB")
    sx = img.width / page_size[0]
    sy = img.height / page_size[1]
    draw = ImageDraw.Draw(img)
    for m in mask_rec.get("masks", []):
        xs = [p[0] * sx for p in m["polygon"]]
        ys = [p[1] * sy for p in m["polygon"]]
        box = [min(xs), min(ys), max(xs), max(ys)]
        fill = _sample_bg(img, box) if style == "patch" else NEUTRAL
        draw.rectangle(box, fill=fill)
        if style == "patch" and m.get("pin"):
            cx = (box[0] + box[2]) / 2
            cy = (box[1] + box[3]) / 2
            r = max(9, min(14, int((box[3] - box[1]) / 2)))
            draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=PIN_FILL)
            draw.text((cx, cy), str(m["pin"]), fill=PIN_TEXT, anchor="mm")
    out_png.parent.mkdir(parents=True, exist_ok=True)
    img.save(out_png)


def contact_sheet(page_png: Path, quiz_png: Path, mask_rec: dict,
                  page_size: tuple[float, float], out_png: Path) -> None:
    """QA용 전/후/경계 overlay 비교 시트(비공개 산출물)."""
    from PIL import Image, ImageDraw

    before = Image.open(page_png).convert("RGB")
    after = Image.open(quiz_png).convert("RGB")
    overlay = before.copy()
    d = ImageDraw.Draw(overlay)
    sx = overlay.width / page_size[0]
    sy = overlay.height / page_size[1]
    for m in mask_rec.get("masks", []):
        xs = [p[0] * sx for p in m["polygon"]]
        ys = [p[1] * sy for p in m["polygon"]]
        d.rectangle([min(xs), min(ys), max(xs), max(ys)], outline=(255, 0, 0), width=3)
    w, h = before.size
    sheet = Image.new("RGB", (w * 3 + 20, h), (255, 255, 255))
    sheet.paste(before, (0, 0))
    sheet.paste(overlay, (w + 10, 0))
    sheet.paste(after, (w * 2 + 20, 0))
    out_png.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out_png)


def run(private: Path, sid: str, only_page: int | None, dry: bool, sheet: bool,
        style: str = "patch") -> int:
    extract_dir = private / "extract" / sid
    revs = sorted(extract_dir.glob("rev-*"))
    if not revs:
        print(f"[INFO] extract 산출물 없음: {extract_dir} — anatomy_extract.py 먼저")
        return 0
    rev = revs[-1]
    review, ok_pages, leaks, redraws = [], 0, 0, []
    for ej in sorted(rev.glob("page-*.json")):
        rec = json.loads(ej.read_text(encoding="utf-8"))
        pno = rec["page"]
        if only_page and pno != only_page:
            continue
        mask_rec = build_masks(rec)
        check = verify_leakage(rec, mask_rec)
        if not check["ok"]:
            mask_rec["status"] = "leak"
            mask_rec["leaks"] = check["leaks"]
            leaks += 1
        if mask_rec["status"] in {"needs_review", "leak"}:
            review.append({"page": pno, "status": mask_rec["status"]})
        if mask_rec.get("redraw_recommended"):
            redraws.append(pno)
        out = private / "masks" / sid / f"page-{pno:04d}.mask.json"
        if not dry:
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(json.dumps(mask_rec, ensure_ascii=False, indent=1),
                           encoding="utf-8")
        page_png = private / "pages" / sid / rev.name / f"page-{pno:04d}.png"
        if mask_rec["status"] == "masked" and page_png.exists() and not dry:
            size = (rec.get("width") or 595, rec.get("height") or 842)
            quiz_png = private / "render" / sid / f"page-{pno:04d}.quiz.png"
            render_quiz(page_png, mask_rec, size, quiz_png, style=style)
            if sheet:
                contact_sheet(page_png, quiz_png, mask_rec, size,
                              private / "qa" / sid / f"page-{pno:04d}.sheet.png")
            ok_pages += 1
    # review queue 기록(비공개)
    if review and not dry:
        rq = private / "review" / f"{sid}.json"
        rq.parent.mkdir(parents=True, exist_ok=True)
        rq.write_text(json.dumps(review, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"mask: 렌더 {ok_pages} · review 대기 {len(review)} · leak {leaks}"
          f" · 재작화 권고 {len(redraws)}{'p' + str(redraws) if redraws else ''}"
          f"{' (dry-run)' if dry else ''}")
    if redraws:
        print("  → 가린 면적이 커서 패치로도 어색함 — 해당 페이지는 원본 게시 대신"
              " 클로드 자체 제작 SVG 재작화(4b QA 루프)로 문항화할 것.")
    return 1 if leaks else 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source-id", required=True)
    ap.add_argument("--page", type=int)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--contact-sheet", action="store_true")
    ap.add_argument("--style", choices=["patch", "box"], default="patch",
                    help="patch(기본): 주변색 자연 패치+번호핀 / box: 중립색 박스")
    ap.add_argument("--private-assets-dir", default=str(DEFAULT_PRIVATE))
    a = ap.parse_args()
    private = Path(a.private_assets_dir)
    if not private.is_absolute():
        private = ROOT / private
    return run(private, a.source_id, a.page, a.dry_run, a.contact_sheet, a.style)


if __name__ == "__main__":
    sys.exit(main())
