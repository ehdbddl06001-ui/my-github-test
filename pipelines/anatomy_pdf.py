#!/usr/bin/env python3
"""anatomy_pdf.py — 회차별 해부학 학습자료 PDF 생성 (결정론).

복원 이미지(퀴즈판/정답판) + 문항 카드(frontmatter)를 받아
[표지 → 학습 개요 → 문제 → 정답·해설] 구조의 PDF를 만든다.

중요 제약
  - 산출 PDF는 카데바 사진·e-Anatomy 캡처 파생물을 포함하므로 **repo 커밋 금지**.
    출력은 반드시 `.private/anatomy/pdf/`(gitignore) 아래로만 쓴다.
  - 레이아웃·페이지 구성은 전부 이 스크립트가 결정한다(LLM은 manifest 내용만 작성).

사용:
  python pipelines/anatomy_pdf.py --manifest .private/anatomy/pdf/s03_manifest.json
  python pipelines/anatomy_pdf.py --selftest

manifest 형식(JSON):
{
  "title": "해부학 3Q 3회차 학습자료",
  "session_no": 3,
  "class_date": "2026-08-24",
  "scope": "다리오금·종아리 / 뒤통수밑삼각",
  "overview": [{"heading": "다리오금", "body": "..."}],
  "questions": [{"card": "content/.../anatomy-2026-0017.md",
                 "quiz_image": ".private/.../q5183_p1_quiz.png",
                 "clean_image": ".private/.../q5183_p1_clean.png"}],
  "output": ".private/anatomy/pdf/anatomy-3q-s03-study.pdf"
}
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import pymupdf
import yaml

ROOT = Path(__file__).resolve().parent.parent

PAGE_W, PAGE_H = 595, 842  # A4 portrait (pt)
MARGIN = 48
BODY_W = PAGE_W - 2 * MARGIN
FONT_NAME = "kr"

INK = (0.12, 0.14, 0.17)
ACCENT = (0.05, 0.42, 0.65)
WARN = (0.72, 0.14, 0.14)
MUTED = (0.42, 0.45, 0.50)
RULE = (0.78, 0.82, 0.86)


def _font_buffer() -> bytes:
    return pymupdf.Font("korea").buffer


def _load_card(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        raise ValueError(f"frontmatter 없음: {path}")
    fm = text.split("---", 2)[1]
    return yaml.safe_load(fm)


class Builder:
    """페이지 커서를 들고 다니며 블록을 흘려 넣는 단순 조판기."""

    def __init__(self, doc: pymupdf.Document, fontbuf: bytes):
        self.doc = doc
        self.fontbuf = fontbuf
        self.font = pymupdf.Font(fontbuffer=fontbuf)
        self.page = None
        self.y = MARGIN

    def new_page(self):
        self.page = self.doc.new_page(width=PAGE_W, height=PAGE_H)
        self.page.insert_font(fontname=FONT_NAME, fontbuffer=self.fontbuf)
        self.y = MARGIN
        return self.page

    def _ensure(self, need: float):
        if self.page is None or self.y + need > PAGE_H - MARGIN:
            self.new_page()

    def _wrap(self, text: str, size: float, width: float) -> list[str]:
        lines: list[str] = []
        for para in text.split("\n"):
            if not para:
                lines.append("")
                continue
            cur = ""
            for word in para.split(" "):
                cand = word if not cur else cur + " " + word
                if self.font.text_length(cand, size) <= width:
                    cur = cand
                    continue
                if cur:
                    lines.append(cur)
                # 한 단어가 폭을 넘으면 글자 단위로 쪼갠다
                while self.font.text_length(word, size) > width:
                    k = 1
                    while k < len(word) and self.font.text_length(word[:k + 1], size) <= width:
                        k += 1
                    lines.append(word[:k])
                    word = word[k:]
                cur = word
            lines.append(cur)
        return lines

    def text(self, s: str, size: float = 10.5, color=INK, indent: float = 0,
             leading: float | None = None, gap: float = 6):
        width = BODY_W - indent
        lines = self._wrap(s, size, width)
        lh = leading or size * 1.55
        for ln in lines:
            self._ensure(lh)
            self.page.insert_text((MARGIN + indent, self.y + size),
                                  ln, fontname=FONT_NAME, fontsize=size, color=color)
            self.y += lh
        self.y += gap

    def heading(self, s: str, size: float = 15, color=ACCENT, rule: bool = True):
        self._ensure(size * 2.4)
        self.y += 4
        self.page.insert_text((MARGIN, self.y + size), s,
                              fontname=FONT_NAME, fontsize=size, color=color)
        self.y += size * 1.35
        if rule:
            self.page.draw_line((MARGIN, self.y), (PAGE_W - MARGIN, self.y),
                                color=RULE, width=0.8)
            self.y += 10

    def image(self, path: Path, max_h: float = 430, max_px: int = 1500, jpg_q: int = 82):
        """긴 변 max_px로 축소 + JPEG 재압축 후 삽입(PDF 용량 억제)."""
        raw = pymupdf.Pixmap(str(path))
        if raw.alpha:
            raw = pymupdf.Pixmap(raw, 0)  # JPEG는 알파 불가
        if max(raw.width, raw.height) > max_px:
            s = max_px / max(raw.width, raw.height)
            tmp = pymupdf.open()
            tp = tmp.new_page(width=raw.width * s, height=raw.height * s)
            tp.insert_image(tp.rect, pixmap=raw)
            raw = tp.get_pixmap(dpi=72)
            tmp.close()
        stream = raw.tobytes("jpeg", jpg_quality=jpg_q)
        w, h = raw.width, raw.height
        scale = min(BODY_W / w, max_h / h, 1.0)
        dw, dh = w * scale, h * scale
        self._ensure(dh + 8)
        x0 = MARGIN + (BODY_W - dw) / 2
        rect = pymupdf.Rect(x0, self.y, x0 + dw, self.y + dh)
        self.page.insert_image(rect, stream=stream)
        self.page.draw_rect(rect, color=RULE, width=0.8)
        self.y += dh + 12

    def spacer(self, h: float):
        self._ensure(1)
        self.y += h


def build_pdf(manifest: dict, root: Path = ROOT) -> Path:
    out = root / manifest["output"]
    priv = (root / ".private").resolve()
    if priv not in out.resolve().parents:
        raise ValueError(f"출력은 .private/ 아래여야 한다 (카데바 파생물): {out}")
    out.parent.mkdir(parents=True, exist_ok=True)

    doc = pymupdf.open()
    b = Builder(doc, _font_buffer())

    # ── 표지 ───────────────────────────────────────────────
    b.new_page()
    b.spacer(150)
    b.text("MedKOS · 임상해부학술기 3Q", size=12, color=MUTED, gap=2)
    b.text(manifest["title"], size=24, color=INK, leading=34, gap=10)
    b.text(f"수업일 {manifest['class_date']}  ·  {manifest['session_no']}회차", size=12, color=ACCENT, gap=4)
    b.text(f"범위: {manifest.get('scope', '')}", size=11, color=INK, gap=4)
    b.text(f"생성일 {manifest.get('generated', '')}", size=10, color=MUTED, gap=24)
    b.text("개인 학습용 — 공개·재배포 금지", size=12, color=WARN, gap=2)
    b.text("본 자료는 카데바 사진 및 e-Anatomy 실습영상 캡처의 필기 제거·복원 파생물을 "
           "포함합니다. 웹 게시·공유 불가, 로컬/개인 Drive 보관만 허용.", size=9.5, color=MUTED)

    # ── 학습 개요 ──────────────────────────────────────────
    if manifest.get("overview"):
        b.new_page()
        b.heading("학습 개요", size=17)
        for sec in manifest["overview"]:
            b.heading(sec["heading"], size=12.5, color=INK, rule=False)
            b.text(sec["body"], size=10.5, indent=6)

    # ── 문제 ──────────────────────────────────────────────
    cards = []
    for i, q in enumerate(manifest["questions"], 1):
        card = _load_card(root / q["card"])
        cards.append((i, q, card))
        b.new_page()
        b.heading(f"문제 {i}", size=15)
        b.text(card.get("stem", ""), size=11, gap=10)
        quiz = root / q["quiz_image"]
        if quiz.exists():
            b.image(quiz, max_h=520)
        else:
            b.text(f"[이미지 없음: {q['quiz_image']}]", size=10, color=WARN)

    # ── 정답·해설 ─────────────────────────────────────────
    b.new_page()
    b.heading("정답 · 해설", size=17)
    for i, q, card in cards:
        b._ensure(360)  # 정답 제목·해설·이미지가 페이지 경계에서 갈라지지 않게
        b.heading(f"정답 {i} — {card.get('answer', '')}", size=12.5, color=WARN, rule=False)
        b.text(card.get("explanation", ""), size=10, indent=6, gap=4)
        clean = q.get("clean_image")
        if clean and (root / clean).exists():
            b.image(root / clean, max_h=280)
        b.spacer(8)

    # 페이지 번호
    for n, page in enumerate(doc, 1):
        page.insert_font(fontname=FONT_NAME, fontbuffer=b.fontbuf)
        page.insert_text((PAGE_W / 2 - 8, PAGE_H - 24), f"- {n} -",
                         fontname=FONT_NAME, fontsize=9, color=MUTED)

    doc.save(str(out), deflate=True, garbage=3)
    doc.close()
    return out


def selftest() -> int:
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        (root / ".private/anatomy/pdf").mkdir(parents=True)
        (root / "content").mkdir()
        # 더미 이미지
        pix = pymupdf.Pixmap(pymupdf.csRGB, pymupdf.IRect(0, 0, 320, 200))
        pix.clear_with(120)
        img = root / ".private/anatomy/pdf/dummy.png"
        pix.save(str(img))
        # 더미 카드
        card = root / "content/q1.md"
        card.write_text("---\nid: t-1\nstem: \"핀 ①이 가리키는 근육은?\"\n"
                        "answer: \"등세모근 (trapezius)\"\nexplanation: \"얕은층 근육이다.\"\n---\n",
                        encoding="utf-8")
        manifest = {
            "title": "셀프테스트 자료", "session_no": 0, "class_date": "2026-01-01",
            "scope": "테스트", "generated": "2026-01-01",
            "overview": [{"heading": "개요", "body": "테스트 본문 " * 40}],
            "questions": [{"card": "content/q1.md",
                           "quiz_image": ".private/anatomy/pdf/dummy.png",
                           "clean_image": ".private/anatomy/pdf/dummy.png"}],
            "output": ".private/anatomy/pdf/out.pdf",
        }
        out = build_pdf(manifest, root=root)
        doc = pymupdf.open(str(out))
        assert doc.page_count >= 4, f"페이지 부족: {doc.page_count}"
        full = "".join(p.get_text() for p in doc)
        for token in ("셀프테스트", "문제 1", "등세모근", "공개·재배포 금지"):
            assert token in full, f"본문 누락: {token}"
        # .private 밖 출력은 거부
        bad = dict(manifest, output="docs/leak.pdf")
        try:
            build_pdf(bad, root=root)
            raise AssertionError("출력 경로 가드 실패")
        except ValueError:
            pass
    print("anatomy_pdf selftest OK")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        return selftest()
    if not args.manifest:
        ap.error("--manifest 또는 --selftest 필요")
    manifest = json.loads(Path(args.manifest).read_text(encoding="utf-8"))
    out = build_pdf(manifest)
    print(json.dumps({"output": str(out.relative_to(ROOT)),
                      "pages": pymupdf.open(str(out)).page_count}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
