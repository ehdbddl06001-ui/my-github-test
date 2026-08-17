#!/usr/bin/env python3
"""anatomy_subnote.py — 회차 서브노트 한 파일 만들기 (결정론).

`kind: study_guide` 카드 1장을 받아 **회차 산출물 한 벌**을 만든다.

  왼쪽 = 도해(라벨판 SVG 또는 실사 복원본)   오른쪽 = 근육표·혈관표·신경표·콜아웃
  뒤   = 그 회차 태깅 문항(퀴즈판) + 정답·해설 합본

`anatomy_pdf.py` 와의 차이: 저쪽은 [표지→개요→문제→정답]의 세로 A4 문제집이고,
이쪽은 **가로 A4 펼침 지면에 도해와 표를 나란히** 놓는 공부용 서브노트다.
필기 여백을 오른쪽 아래에 남기지 않고 지면을 꽉 채운다 — 인쇄해서 옆에 두고 본다.

중요 제약(anatomy_pdf.py 와 동일)
  - 출력은 반드시 `.private/anatomy/pdf/` 아래. repo 커밋·웹 게시 금지.
  - 조판은 전부 이 스크립트가 정한다. LLM은 카드 본문만 쓴다(Source of Truth 유지).
  - 도해는 카드 본문이 참조하는 `docs/assets/anatomy/*-labeled.svg` 를 그대로 렌더한다
    — 여기서 새 그림을 만들지 않는다(lane 분리, docs/ANATOMY_VISUALS.md §0).

사용:
  python pipelines/anatomy_subnote.py --card content/anatomy/notes/anatomy-2026-0034-s01-study.md \
      --output .private/anatomy/pdf/subnote-s01.pdf
  python pipelines/anatomy_subnote.py --selftest
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path

import pymupdf
import yaml

ROOT = Path(__file__).resolve().parent.parent

PAGE_W, PAGE_H = 842, 595          # A4 가로
MARGIN = 34
GUTTER = 18
HEAD_H = 30                        # 머리띠 높이
FOOT_H = 20
FONT_NAME = "kr"

INK = (0.12, 0.14, 0.17)
ACCENT = (0.05, 0.42, 0.65)
WARN = (0.72, 0.14, 0.14)
MUTED = (0.42, 0.45, 0.50)
RULE = (0.78, 0.82, 0.86)
BAND = (0.93, 0.96, 0.98)

# 카드 본문에서 도해를 찾는 패턴 — 라벨판만 왼쪽 레인에 올린다(퀴즈판은 문항 쪽).
ASSET_RE = re.compile(r"assets/anatomy/([A-Za-z0-9\-]+-labeled)\.svg")


def _font_buffer() -> bytes:
    return pymupdf.Font("korea").buffer


def load_card(path: Path) -> tuple[dict, str]:
    """frontmatter dict 와 본문을 함께 돌려준다."""
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        raise ValueError(f"frontmatter 없음: {path}")
    _, fm, body = text.split("---", 2)
    return yaml.safe_load(fm), body


def strip_inline(s: str) -> str:
    return s.replace("**", "").replace("`", "")


def _wide(ch: str) -> bool:
    """전각(한글·CJK) 여부 — 관계도 격자에서 두 칸을 차지한다."""
    return unicodedata.east_asian_width(ch) in ("W", "F")


# ── 본문 파서 ─────────────────────────────────────────────────────────────

def parse_blocks(body: str, drop_sections: tuple[str, ...] = ("0.",)) -> list[dict]:
    """마크다운-라이트 본문 → 블록 리스트.

    `drop_sections` 로 시작하는 `## ` 절은 통째로 버린다(기본: 0. 딸린 시각 자료 —
    그 도해가 바로 왼쪽 레인에 실리므로 파일명 표를 다시 실을 이유가 없다).
    """
    lines = body.split("\n")
    blocks: list[dict] = []
    para: list[str] = []
    table: list[list[str]] = []
    skipping = False
    i = 0

    def flush_para():
        nonlocal para
        if para:
            blocks.append({"kind": "para", "text": strip_inline(" ".join(para))})
            para = []

    def flush_table():
        nonlocal table
        if table:
            blocks.append({"kind": "table", "rows": table})
            table = []

    while i < len(lines):
        s = lines[i].strip()

        if s.startswith("## "):
            flush_para()
            flush_table()
            title = strip_inline(s[3:])
            skipping = title.startswith(drop_sections)
            if not skipping:
                blocks.append({"kind": "h2", "text": title})
            i += 1
            continue
        if skipping:
            i += 1
            continue

        if s.startswith("|"):
            flush_para()
            cells = [strip_inline(c.strip()) for c in s.strip("|").split("|")]
            if not all(set(c) <= {"-", ":", ""} for c in cells):   # 구분행 버림
                table.append(cells)
            i += 1
            continue
        flush_table()

        if s.startswith("```"):
            flush_para()
            block = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                block.append(lines[i].rstrip())
                i += 1
            i += 1
            blocks.append({"kind": "code", "lines": block})
            continue

        if s.startswith("### "):
            flush_para()
            blocks.append({"kind": "h3", "text": strip_inline(s[4:])})
        elif s.startswith("> "):
            flush_para()
            blocks.append({"kind": "callout", "text": strip_inline(s[2:])})
        elif s.startswith("- "):
            flush_para()
            item = [s[2:]]
            while i + 1 < len(lines) and lines[i + 1].startswith("  ") and lines[i + 1].strip():
                nxt = lines[i + 1].strip()
                if nxt.startswith(("- ", "|", "```", "#", "> ")):
                    break
                item.append(nxt)
                i += 1
            blocks.append({"kind": "bullet", "text": strip_inline(" ".join(item))})
        elif re.match(r"^\d+\.\s", s):
            flush_para()
            blocks.append({"kind": "num", "text": strip_inline(s)})
        elif s:
            para.append(s)
        else:
            flush_para()
        i += 1

    flush_para()
    flush_table()
    return blocks


def find_diagrams(body: str, root: Path) -> list[Path]:
    """본문이 참조하는 라벨판 SVG를 등장 순서대로(중복 제거) 돌려준다."""
    out: list[Path] = []
    for name in ASSET_RE.findall(body):
        p = root / "docs" / "assets" / "anatomy" / f"{name}.svg"
        if p.exists() and p not in out:
            out.append(p)
    return out


def session_questions(session_no: int, root: Path) -> list[tuple[Path, dict]]:
    """그 회차 문항 카드를 id 순으로. 정답이 없는 카드는 뺀다."""
    found = []
    qdir = root / "content" / "anatomy" / "questions"
    for path in sorted(qdir.rglob("*.md")):
        meta, _ = load_card(path)
        if meta.get("kind") != "question" or meta.get("session_no") != session_no:
            continue
        if not meta.get("answer"):
            continue
        found.append((path, meta))
    found.sort(key=lambda t: str(t[1].get("id", "")))
    return found


def question_image(meta: dict, root: Path) -> Path | None:
    """문항 카드가 가리키는 그림. 웹 자산(SVG)이든 실사 복원본(.private)이든."""
    for key in ("quiz_image", "web_asset", "image"):
        val = meta.get(key)
        if not val:
            continue
        cand = root / val if not str(val).startswith("assets/") else root / "docs" / val
        if cand.exists():
            return cand
    return None


# ── 조판기 ────────────────────────────────────────────────────────────────

class Subnote:
    """가로 지면 위에서 '왼쪽 그림 레인 + 오른쪽 글 레인'을 흘리는 조판기."""

    def __init__(self, doc: pymupdf.Document, fontbuf: bytes, header: str):
        self.doc = doc
        self.fontbuf = fontbuf
        self.font = pymupdf.Font(fontbuffer=fontbuf)
        self.header = header
        self.page = None
        self.x0 = MARGIN
        self.x1 = PAGE_W - MARGIN
        self.y = MARGIN + HEAD_H
        self.y1 = PAGE_H - MARGIN - FOOT_H
        self.pending: list[tuple[Path, str]] = []   # 왼쪽 레인에 남은 (그림, 설명)

    # 지면 --------------------------------------------------------------
    def _band(self, note: str = ""):
        self.page.draw_rect(pymupdf.Rect(0, 0, PAGE_W, MARGIN + HEAD_H - 12),
                            color=None, fill=BAND)
        self.page.insert_text((MARGIN, 26), self.header, fontname=FONT_NAME,
                              fontsize=9.5, color=MUTED)
        if note:
            w = self.font.text_length(note, 9.5)
            self.page.insert_text((PAGE_W - MARGIN - w, 26), note,
                                  fontname=FONT_NAME, fontsize=9.5, color=ACCENT)

    def new_page(self, note: str = "", image: Path | None = None, caption: str = "",
                 img_ratio: float = 0.46):
        """새 지면. image 가 있으면 왼쪽 레인에 깔고 글 레인을 오른쪽으로 좁힌다."""
        self.page = self.doc.new_page(width=PAGE_W, height=PAGE_H)
        self.page.insert_font(fontname=FONT_NAME, fontbuffer=self.fontbuf)
        self._band(note)
        self.x0, self.x1 = MARGIN, PAGE_W - MARGIN
        self.y = MARGIN + HEAD_H
        if image is not None:
            box = pymupdf.Rect(MARGIN, self.y,
                               MARGIN + (PAGE_W - 2 * MARGIN - GUTTER) * img_ratio,
                               self.y1)
            self.draw_image(image, box, caption)
            self.x0 = box.x1 + GUTTER
        return self.page

    def _ensure(self, need: float):
        """자리가 없으면 다음 지면으로. 남은 그림이 있으면 그 그림과 함께 편다."""
        if self.page is None or self.y + need > self.y1:
            if self.pending:
                img, cap = self.pending.pop(0)
                self.new_page(image=img, caption=cap)
            else:
                self.new_page()

    # 요소 --------------------------------------------------------------
    def draw_image(self, path: Path, box: pymupdf.Rect, caption: str = ""):
        """SVG는 벡터를 그대로 렌더(글자가 깨지지 않게), 래스터는 JPEG 재압축."""
        cap_h = 22 if caption else 0
        area = pymupdf.Rect(box.x0, box.y0, box.x1, box.y1 - cap_h)
        if path.suffix.lower() == ".svg":
            src = pymupdf.open(str(path))
            sr = src[0].rect
            # 표시 크기의 2배 픽셀로 렌더 → 확대해도 라벨이 읽힌다.
            scale = min(area.width / sr.width, area.height / sr.height)
            pix = src[0].get_pixmap(dpi=int(max(72, min(150, 72 * scale * 2))))
            stream = pix.tobytes("png")
            w, h = pix.width, pix.height
            src.close()
        else:
            pix = pymupdf.Pixmap(str(path))
            if pix.alpha:
                pix = pymupdf.Pixmap(pix, 0)
            stream = pix.tobytes("jpeg", jpg_quality=62)
            w, h = pix.width, pix.height
        s = min(area.width / w, area.height / h)
        dw, dh = w * s, h * s
        x = area.x0 + (area.width - dw) / 2
        rect = pymupdf.Rect(x, area.y0, x + dw, area.y0 + dh)
        self.page.insert_image(rect, stream=stream)
        self.page.draw_rect(rect, color=RULE, width=0.7)
        if caption:
            for i, ln in enumerate(self._wrap(caption, 8.5, box.width)[:2]):
                self.page.insert_text((box.x0, rect.y1 + 12 + i * 11), ln,
                                      fontname=FONT_NAME, fontsize=8.5, color=MUTED)

    def flow_image(self, path: Path, caption: str = "", min_h: float = 200):
        """글 흐름 안에 그림을 넣는다 — 남은 지면을 꽉 채운다(퀴즈판은 클수록 좋다)."""
        if self.y1 - self.y < min_h:
            self._ensure(self.y1 - self.y + 1)      # 자리가 모자라면 다음 지면으로
        self.draw_image(path, pymupdf.Rect(self.x0, self.y, self.x1, self.y1), caption)
        self.y = self.y1

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
                while self.font.text_length(word, size) > width:
                    k = 1
                    while k < len(word) and self.font.text_length(word[:k + 1], size) <= width:
                        k += 1
                    lines.append(word[:k])
                    word = word[k:]
                cur = word
            lines.append(cur)
        return lines

    @property
    def width(self) -> float:
        return self.x1 - self.x0

    def text(self, s: str, size: float = 9.4, color=INK, indent: float = 0,
             gap: float = 4, leading: float | None = None):
        lh = leading or size * 1.5
        for ln in self._wrap(s, size, self.width - indent):
            self._ensure(lh)
            self.page.insert_text((self.x0 + indent, self.y + size), ln,
                                  fontname=FONT_NAME, fontsize=size, color=color)
            self.y += lh
        self.y += gap

    def spacer(self, h: float):
        """빈 지면을 만들지 않는 여백 — 지면 끝에서는 그냥 멈춘다."""
        if self.page is None:
            self.new_page()
        self.y = min(self.y + h, self.y1)

    def heading(self, s: str, size: float = 12.5, color=ACCENT, rule: bool = True):
        self._ensure(size * 2.6)
        self.y += 3
        self.page.insert_text((self.x0, self.y + size), s, fontname=FONT_NAME,
                              fontsize=size, color=color)
        self.y += size * 1.3
        if rule:
            self.page.draw_line((self.x0, self.y), (self.x1, self.y), color=RULE, width=0.8)
            self.y += 7

    def callout(self, s: str, size: float = 9.2, color=WARN):
        lines = self._wrap(s, size, self.width - 18)
        h = len(lines) * size * 1.45 + 12
        self._ensure(h)
        rect = pymupdf.Rect(self.x0, self.y, self.x1, self.y + h)
        self.page.draw_rect(rect, color=None, fill=(0.99, 0.96, 0.94))
        self.page.draw_line((self.x0, self.y), (self.x0, self.y + h), color=color, width=2.2)
        yy = self.y + 6
        for ln in lines:
            self.page.insert_text((self.x0 + 10, yy + size), ln, fontname=FONT_NAME,
                                  fontsize=size, color=INK)
            yy += size * 1.45
        self.y += h + 8

    def code_block(self, lines: list[str], size: float = 7.6):
        """관계도(ASCII 트리)는 **글자 격자**로 찍는다.

        본문 트리는 터미널 등폭을 전제로 쓰였는데 한글 폰트는 비례폭이라 그냥 흘리면
        `│`·`├` 가 위아래로 어긋난다. 그래서 칸 폭을 괘선문자 폭으로 잡고
        전각(한글)만 두 칸을 주어 원문의 열 정렬을 되살린다.
        """
        pad = 7
        lines = list(lines) or [""]
        cells = [sum(2 if _wide(ch) else 1 for ch in ln) for ln in lines]
        need = max(cells) if cells else 1
        cw = self.font.text_length("─", size)
        while size > 5.0 and need * cw > self.width - 2 * pad:
            size -= 0.3
            cw = self.font.text_length("─", size)
        lh = size * 1.42
        h = len(lines) * lh + 2 * pad
        self._ensure(min(h, self.y1 - (MARGIN + HEAD_H)))
        y0 = self.y
        self.page.draw_rect(pymupdf.Rect(self.x0, y0, self.x1, y0 + h),
                            color=RULE, fill=(0.96, 0.97, 0.985), width=0.7)
        y = y0 + pad
        for ln in lines:
            x = self.x0 + pad
            for ch in ln:
                if ch != " ":
                    self.page.insert_text((x, y + size), ch, fontname=FONT_NAME,
                                          fontsize=size, color=INK)
                x += cw * (2 if _wide(ch) else 1)
            y += lh
        self.y = y0 + h + 8

    def table(self, rows: list[list[str]], size: float = 8.0):
        if not rows:
            return
        ncol = max(len(r) for r in rows)
        rows = [r + [""] * (ncol - len(r)) for r in rows]
        need = [max(self.font.text_length(r[c], size) for r in rows) + 9 for c in range(ncol)]
        # 좁은 열(순서·부위 같은 한두 단어)은 필요한 만큼 다 주고, 남는 폭만 긴 열끼리
        # 비례 배분한다. 그냥 비례로 나누면 '얕은근막'이 '얕은근/막'으로 잘린다.
        fair = self.width / ncol
        widths = [min(n, fair) for n in need]
        slack = self.width - sum(widths)
        hungry = sum(max(n - f, 0) for n, f in zip(need, widths))
        if slack > 0 and hungry > 0:
            widths = [w + slack * max(n - w, 0) / hungry for w, n in zip(widths, need)]
        elif slack > 0:
            widths = [w + slack / ncol for w in widths]
        lh = size * 1.38
        header = rows[0]
        for ri, row in enumerate(rows):
            cells = [self._wrap(cell, size, widths[c] - 7) for c, cell in enumerate(row)]
            rh = max(len(cl) for cl in cells) * lh + 6
            before = self.page
            self._ensure(rh)
            if ri and self.page is not before:      # 지면이 넘어가면 머리행을 다시 찍는다
                self._draw_row(header, widths, size, lh, True)
                self._ensure(rh)
            self._draw_row(row, widths, size, lh, ri == 0)
        self.y += 8

    def _draw_row(self, row: list[str], widths: list[float], size: float,
                  lh: float, header: bool):
        cells = [self._wrap(cell, size, widths[c] - 7) for c, cell in enumerate(row)]
        rh = max(len(cl) for cl in cells) * lh + 6
        x = self.x0
        for c, cl in enumerate(cells):
            rect = pymupdf.Rect(x, self.y, x + widths[c], self.y + rh)
            self.page.draw_rect(rect, color=RULE, width=0.55,
                                fill=(0.92, 0.95, 0.97) if header else None)
            ty = self.y + 4
            for ln in cl:
                self.page.insert_text((x + 3.5, ty + size), ln, fontname=FONT_NAME,
                                      fontsize=size, color=ACCENT if header else INK)
                ty += lh
            x += widths[c]
        self.y += rh

    def blocks(self, blocks: list[dict]):
        for b in blocks:
            k = b["kind"]
            if k == "h2":
                self.heading(b["text"])
            elif k == "h3":
                self.heading(b["text"], size=10.4, color=INK, rule=False)
            elif k == "table":
                self.table(b["rows"])
            elif k == "code":
                self.code_block(b["lines"])
            elif k == "callout":
                self.callout(b["text"])
            elif k == "bullet":
                self.text("•  " + b["text"], indent=6, gap=1)
            elif k == "num":
                self.text(b["text"], indent=6, gap=1)
            else:
                self.text(b["text"], gap=3)


def _answer_lines(answer: str) -> list[str]:
    """'1 A / 2 B / ...' 형식이면 줄로 쪼갠다(태깅 채점이 쉬워진다)."""
    parts = [p.strip() for p in answer.split(" / ") if p.strip()]
    return parts if len(parts) > 1 else [answer.strip()]


def build_subnote(card_path: Path, output: str, root: Path = ROOT) -> dict:
    out = root / output
    priv = (root / ".private").resolve()
    if priv not in out.resolve().parents:
        raise ValueError(f"출력은 .private/ 아래여야 한다: {out}")
    out.parent.mkdir(parents=True, exist_ok=True)

    meta, body = load_card(card_path)
    if meta.get("kind") != "study_guide":
        raise ValueError(f"study_guide 카드가 아니다: {card_path} (kind={meta.get('kind')})")
    session_no = meta.get("session_no")
    diagrams = find_diagrams(body, root)
    blocks = parse_blocks(body)
    questions = session_questions(session_no, root) if session_no else []

    doc = pymupdf.open()
    header = f"MedKOS · 임상해부학술기 3Q · {session_no}회차 서브노트"
    b = Subnote(doc, _font_buffer(), header)
    b.pending = [(p, f"도해 {i + 1}. {p.stem.replace('diag-', '').replace('-labeled', '')}")
                 for i, p in enumerate(diagrams)]

    # ── 1면: 제목 + 첫 도해 + 본문 시작 ────────────────────────────────
    first = b.pending.pop(0) if b.pending else (None, "")
    sched = ", ".join(str(d) for d in meta.get("scheduled_dates", []))
    b.new_page(note=f"수업일 {sched}", image=first[0], caption=first[1])
    b.text(strip_inline(str(meta.get("subtopic", meta.get("id", "")))), size=13.5,
           leading=19, gap=3)
    b.text(f"{session_no}회차 · 수업일 {sched} · 생성 {meta.get('date', '')} · "
           f"개인 학습용(공개·재배포 금지)", size=8.6, color=MUTED, gap=6)
    b.blocks(blocks)

    # ── 태깅 문항 ─────────────────────────────────────────────────────
    if questions:
        b.pending = []                     # 도해 레인은 여기서 닫는다
        b.new_page(note="태깅 연습")
        b.heading(f"태깅 문항 {len(questions)}개 — 퀴즈판 번호를 한·영으로 답한다", size=13)
        b.text("정답은 마지막 절에 모아 두었다. 번호핀 순서와 정답 번호는 1:1이다.",
               size=9, color=MUTED)
        for n, (path, q) in enumerate(questions, 1):
            img = question_image(q, root)
            if img is not None:
                # 그림 문항은 한 지면을 통째로 쓴다 — 지문을 위에 두고 퀴즈판을 크게.
                b.new_page(note=f"문항 {n} / {len(questions)}")
            else:
                # 그림 없는 관계형 문항은 이어 붙인다(한 문항이 한 지면을 비워 두지 않게).
                b._ensure(96)
            b.heading(f"문항 {n}. {strip_inline(str(q.get('subtopic', '')))}", size=11.5)
            b.text(strip_inline(str(q.get("stem", ""))), size=9.6)
            for ch in q.get("choices", []) or []:
                b.text("·  " + strip_inline(str(ch)), size=9.2, indent=6, gap=1)
            if img is not None:
                b.flow_image(img, f"{q.get('id', '')} · {q.get('question_style', '')}")
            b.spacer(6)

        # ── 정답 · 해설 ───────────────────────────────────────────────
        b.new_page(note="정답")
        b.heading("정답 · 해설", size=13)
        for n, (path, q) in enumerate(questions, 1):
            b._ensure(60)
            b.heading(f"정답 {n} — {q.get('id', '')}", size=10.6, color=WARN, rule=False)
            for ln in _answer_lines(str(q.get("answer", ""))):
                b.text(ln, size=8.9, indent=8, gap=0)
            if q.get("explanation"):
                b.text(strip_inline(str(q["explanation"])), size=8.7, color=MUTED,
                       indent=8, gap=7)

    for n, page in enumerate(doc, 1):
        page.insert_font(fontname=FONT_NAME, fontbuffer=b.fontbuf)
        page.insert_text((PAGE_W / 2 - 8, PAGE_H - 18), f"- {n} -",
                         fontname=FONT_NAME, fontsize=8.5, color=MUTED)
    try:
        doc.subset_fonts()                 # 한글 폰트 통짜 임베드는 1.7MB
    except Exception:
        pass
    doc.save(str(out), deflate=True, garbage=3)
    pages = doc.page_count
    doc.close()
    return {"output": str(out.relative_to(root)), "pages": pages,
            "kb": round(out.stat().st_size / 1024, 1),
            "diagrams": [p.name for p in diagrams],
            "questions": [q.get("id") for _, q in questions]}


def selftest() -> int:
    import tempfile
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" width="400" height="300">'
           '<rect width="400" height="300" fill="#0e1826"/>'
           '<text x="20" y="40" fill="#e6edf3" font-size="18">등세모근 trapezius</text></svg>')
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        (root / "docs/assets/anatomy").mkdir(parents=True)
        (root / "content/anatomy/notes").mkdir(parents=True)
        (root / "content/anatomy/questions/tagging-1").mkdir(parents=True)
        (root / ".private/anatomy/pdf").mkdir(parents=True)
        (root / "docs/assets/anatomy/diag-test-labeled.svg").write_text(svg, encoding="utf-8")
        (root / "docs/assets/anatomy/diag-test-quiz.svg").write_text(svg, encoding="utf-8")

        card = root / "content/anatomy/notes/s01-study.md"
        card.write_text(
            "---\nid: a-1\nkind: study_guide\nsession_no: 1\n"
            "subtopic: \"1회차 종합 정리\"\nscheduled_dates: [2026-08-18]\ndate: 2026-08-16\n---\n\n"
            "## 0. 딸린 시각 자료\n\n| 도해 | 라벨판 |\n|---|---|\n"
            "| 층 | `assets/anatomy/diag-test-labeled.svg` |\n\n"
            "## 1. 층 구조\n\n| 순서 | 층 |\n|---|---|\n| 1 | 표피 |\n| 2 | 진피 |\n\n"
            "본문 문단이다. " * 60 + "\n\n```\n트리 A\n └ 트리 B\n```\n\n- 불릿 하나\n",
            encoding="utf-8")
        q = root / "content/anatomy/questions/tagging-1/q1.md"
        q.write_text("---\nid: a-9\nkind: question\nsession_no: 1\nquestion_style: spotter\n"
                     "subtopic: 층 태깅\nweb_asset: assets/anatomy/diag-test-quiz.svg\n"
                     "stem: \"1–2를 답하시오.\"\nanswer: \"1 표피 epidermis / 2 진피 dermis\"\n"
                     "explanation: \"겉에서 속으로.\"\n---\n\n## 문제\n", encoding="utf-8")

        res = build_subnote(card, ".private/anatomy/pdf/out.pdf", root=root)
        doc = pymupdf.open(str(root / res["output"]))
        full = "".join(p.get_text() for p in doc)
        assert doc.page_count >= 3, f"페이지 부족: {doc.page_count}"
        for token in ("1회차 종합 정리", "층 구조", "문항 1", "정답 1", "표피 epidermis"):
            assert token in full, f"본문 누락: {token}"
        assert "딸린 시각 자료" not in full, "0절(도해 파일명 표)이 안 걸러졌다"
        assert res["diagrams"] == ["diag-test-labeled.svg"], res["diagrams"]
        assert res["questions"] == ["a-9"], res["questions"]
        assert doc[0].get_images(), "1면에 도해가 안 실렸다"
        doc.close()

        try:                                  # .private 밖 출력은 거부
            build_subnote(card, "docs/leak.pdf", root=root)
            raise AssertionError("출력 경로 가드 실패")
        except ValueError:
            pass
    print("anatomy_subnote selftest OK")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--card", help="study_guide 카드(.md)")
    ap.add_argument("--output", help=".private/anatomy/pdf/subnote-sNN.pdf")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        return selftest()
    if not args.card or not args.output:
        ap.error("--card 와 --output 이 함께 필요하다 (또는 --selftest)")
    res = build_subnote(ROOT / args.card, args.output)
    print(json.dumps(res, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
