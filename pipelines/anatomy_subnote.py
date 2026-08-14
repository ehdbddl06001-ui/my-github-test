#!/usr/bin/env python3
"""anatomy_subnote.py — 회차 '서브노트' PDF 렌더러 (결정론).

사용자가 쓰던 서브노트 조판(섹션 바 · 콜아웃 칩 · 조밀한 표 · 경로 박스)을
그대로 재현한다. 내용은 `content/anatomy/notes/*.md` 카드가 Source of Truth이고,
이 스크립트는 **조판만** 한다(LLM이 레이아웃을 즉흥으로 만들지 않게).

카드 본문 문법
  ## 1. 한글 제목 | English            → 보라 섹션 바
  ### 1) 소제목 (english)              → 좌측 바 + 굵은 소제목
  - 불릿, **강조**, ==형광==, `영문`   → 인라인 스타일
  | a | b |                            → 표(첫 행 헤더, 얼룩무늬)
  > [!기출] 라벨 :: 본문               → 콜아웃(기출/교수강조/주의/임상/TIP/암기)
  => A → B → C                         → 경로(흐름) 박스

사용:
  python pipelines/anatomy_subnote.py --card content/anatomy/notes/<파일>.md \
      --output .private/anatomy/pdf/subnote-s02.pdf
  python pipelines/anatomy_subnote.py --selftest
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import pymupdf
import yaml

ROOT = Path(__file__).resolve().parent.parent

PORTRAIT = (595, 842)
LANDSCAPE = (842, 595)          # A4 가로 — 좌 도해 / 우 표
MARGIN = 40
FONT_NAME = "kr"
FIG_FRAC = 0.48                 # 가로 모드에서 왼쪽 도해 열이 차지하는 비율

INK = (0.13, 0.14, 0.18)
MUTED = (0.45, 0.47, 0.53)
RULE = (0.80, 0.83, 0.88)
PURPLE = (0.40, 0.29, 0.64)
PURPLE_SOFT = (0.93, 0.91, 0.98)
EN = (0.30, 0.45, 0.72)
HL = (1.0, 0.93, 0.45)

# 콜아웃: (칩·바 색, 배경색)
CALLOUTS = {
    "기출":   ((0.78, 0.18, 0.36), (0.99, 0.93, 0.95)),
    "교수강조": ((0.83, 0.48, 0.08), (1.00, 0.96, 0.89)),
    "주의":   ((0.76, 0.16, 0.16), (1.00, 0.93, 0.93)),
    "임상":   ((0.10, 0.42, 0.72), (0.92, 0.95, 1.00)),
    "TIP":    ((0.09, 0.52, 0.32), (0.91, 0.97, 0.93)),
    "암기":   ((0.42, 0.29, 0.64), (0.94, 0.92, 0.99)),
}


def _font() -> pymupdf.Font:
    return pymupdf.Font("korea")


class Sub:
    """서브노트 조판기 — y커서를 들고 위에서 아래로 쌓는다."""

    def __init__(self, doc: pymupdf.Document, title: str, subtitle: str,
                 split: bool = False):
        self.doc, self.title, self.subtitle = doc, title, subtitle
        self.split = split
        self.PW, self.PH = LANDSCAPE if split else PORTRAIT
        self.font = _font()
        self.fontbuf = self.font.buffer
        self.page = None
        self.y = 0.0
        # 현재 글 흐름이 쓰는 열
        self.x0 = MARGIN
        self.x1 = self.PW - MARGIN
        self.top = MARGIN            # 열 시작 y(2단에서 섹션 바 아래)
        self.cur_fig = None          # (png경로, 캡션) — 2단에서 페이지마다 다시 그린다
        self.cur_sec = None          # (kr, en)
        self.new_page()

    @property
    def width(self) -> float:
        return self.x1 - self.x0

    # ── 페이지 ────────────────────────────────────────────
    def new_page(self, plain: bool = False):
        self.page = self.doc.new_page(width=self.PW, height=self.PH)
        self.page.insert_font(fontname=FONT_NAME, fontbuffer=self.fontbuf)
        self.x0, self.x1 = MARGIN, self.PW - MARGIN
        self.y = self.top = MARGIN
        if self.split and not plain and self.cur_sec:
            self._compose_split(cont=True)
        return self.page

    def _compose_split(self, cont: bool = False):
        """가로 2단 골격: 위 섹션 바(전폭) → 왼쪽 도해 → 오른쪽이 글 흐름."""
        kr, en = self.cur_sec
        self.x0, self.x1 = MARGIN, self.PW - MARGIN
        self.y = MARGIN
        self._bar(kr + (" (이어서)" if cont else ""), en)
        top = self.y
        fig_w = (self.PW - 2 * MARGIN) * FIG_FRAC
        if self.cur_fig:
            self._draw_figure(MARGIN, top, fig_w, self.PH - MARGIN - 20 - top)
        # 이후 글은 오른쪽 열에만 흐른다
        self.x0 = MARGIN + fig_w + 18 if self.cur_fig else MARGIN
        self.x1 = self.PW - MARGIN
        self.y = self.top = top

    def _ensure(self, need: float):
        if self.y + need > self.PH - MARGIN - 18:
            self.new_page()

    def _w(self, s: str, size: float) -> float:
        return self.font.text_length(s, fontsize=size)

    # ── 인라인 스팬 ───────────────────────────────────────
    def _spans(self, s: str):
        """**굵게** / ==형광== / `영문` 을 스팬으로 쪼갠다."""
        out, buf = [], ""
        i = 0
        while i < len(s):
            for mark, kind, ln in (("**", "b", 2), ("==", "h", 2), ("`", "c", 1)):
                if s.startswith(mark, i):
                    end = s.find(mark, i + ln)
                    if end != -1:
                        if buf:
                            out.append((buf, "n")); buf = ""
                        out.append((s[i + ln:end], kind))
                        i = end + ln
                        break
            else:
                buf += s[i]; i += 1
                continue
        if buf:
            out.append((buf, "n"))
        return out

    def _style(self, kind: str, base_color):
        if kind == "b":
            return base_color, True, None
        if kind == "h":
            return INK, True, HL
        if kind == "c":
            return EN, False, None
        return base_color, False, None

    def rich(self, s: str, size: float = 9.8, color=INK, x0: float | None = None,
             width: float | None = None, leading: float = 14, gap: float = 3,
             indent: float = 0):
        """인라인 스타일을 살려 줄바꿈하며 그린다."""
        x0 = (self.x0 if x0 is None else x0) + indent
        width = (self.width - indent) if width is None else width
        spans = self._spans(s)
        # 단어 단위 토큰으로 펼치기(한글은 글자 단위로도 끊을 수 있게 공백 기준 + 길면 강제)
        toks = []
        for text, kind in spans:
            for piece in re.split(r"(\s+)", text):
                if piece:
                    toks.append((piece, kind))
        line, line_w = [], 0.0
        self._ensure(leading)
        for piece, kind in toks:
            w = self._w(piece, size)
            if line_w + w > width and line:
                self._draw_line(line, x0, size, color, leading)
                line, line_w = [], 0.0
                if piece.isspace():
                    continue
            line.append((piece, kind, w)); line_w += w
        if line:
            self._draw_line(line, x0, size, color, leading)
        self.y += gap

    def measure(self, s: str, size: float, width: float, leading: float) -> float:
        """그리지 않고 높이만 계산한다(콜아웃·경로 박스 배경을 먼저 깔기 위해).
        임시 페이지를 만들어 재던 방식은 delete_page가 기존 Page 객체를 무효화해서 못 쓴다."""
        toks = []
        for text, kind in self._spans(s):
            for piece in re.split(r"(\s+)", text):
                if piece:
                    toks.append(piece)
        lines, line_w = 1, 0.0
        for piece in toks:
            w = self._w(piece, size)
            if line_w + w > width and line_w > 0:
                lines += 1
                line_w = 0.0 if piece.isspace() else w
            else:
                line_w += w
        return lines * leading

    def _put(self, pt, s: str, size: float, color, bold: bool = False):
        """텍스트 1회 출력. bold는 0.3pt 어긋나게 두 번 그려 흉내낸다 —
        render_mode=2(면+선)는 이 폰트에서 속 빈 윤곽으로 렌더된다(2026-08-14 실측)."""
        self.page.insert_text(pt, s, fontname=FONT_NAME, fontsize=size, color=color)
        if bold:
            self.page.insert_text((pt[0] + 0.3, pt[1]), s, fontname=FONT_NAME,
                                  fontsize=size, color=color)

    def _draw_line(self, line, x0, size, color, leading):
        self._ensure(leading)
        x = x0
        for piece, kind, w in line:
            col, bold, hl = self._style(kind, color)
            if hl and piece.strip():
                self.page.draw_rect(pymupdf.Rect(x, self.y + 2.5, x + w, self.y + size + 3.5),
                                    color=None, fill=hl)
            self._put((x, self.y + size), piece, size, col, bold)
            x += w
        self.y += leading

    # ── 블록 ──────────────────────────────────────────────
    def section_bar(self, kr: str, en: str = "", fig=None):
        """가로 2단 모드에서는 섹션마다 새 페이지를 열고 좌 도해 / 우 본문을 짠다."""
        if self.split:
            self.cur_sec, self.cur_fig = (kr, en), fig
            self.new_page(plain=True)
            self._compose_split(cont=False)
            return
        self._bar(kr, en)

    def _bar(self, kr: str, en: str = ""):
        self._ensure(52)
        self.y += 6
        r = pymupdf.Rect(self.x0, self.y, self.x1, self.y + 28)
        self.page.draw_rect(r, color=None, fill=PURPLE, radius=0.22)
        self._put((self.x0 + 12, self.y + 19), kr, 12.5, (1, 1, 1), bold=True)
        if en:
            self.page.insert_text((self.x0 + 16 + self._w(kr, 12.5), self.y + 19), en,
                                  fontname=FONT_NAME, fontsize=9.5, color=(0.82, 0.78, 0.94))
        self.y += 38

    def _svg_png(self, svg: Path, scale: float = 2.6) -> Path | None:
        """SVG를 chromium으로 래스터화(QA 때 보는 것과 같은 렌더러) 후 캐시."""
        import hashlib, re as _re, subprocess, tempfile
        if not svg.exists():
            return None
        raw = svg.read_text(encoding="utf-8", errors="ignore")
        m = _re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', raw)
        w, h = (float(m.group(1)), float(m.group(2))) if m else (880.0, 700.0)
        key = hashlib.sha256((str(svg) + str(svg.stat().st_mtime) + str(scale))
                             .encode()).hexdigest()[:16]
        out = Path(tempfile.gettempdir()) / f"subnote_fig_{key}.png"
        if out.exists():
            return out
        cmd = ["/opt/pw-browsers/chromium", "--headless", "--disable-gpu", "--no-sandbox",
               f"--screenshot={out}", f"--window-size={int(w*scale)},{int(h*scale)}",
               "--hide-scrollbars", "--force-device-scale-factor=1",
               f"file://{svg.resolve()}"]
        try:
            subprocess.run(cmd, capture_output=True, timeout=90)
        except Exception:
            return None
        return out if out.exists() else None

    def _draw_figure(self, x: float, y: float, w: float, h: float):
        png, caption = self.cur_fig
        p = ROOT / png if not Path(png).is_absolute() else Path(png)
        img = self._svg_png(p) if p.suffix == ".svg" else (p if p.exists() else None)
        if img is None:
            self.page.insert_text((x, y + 12), f"[도해 없음: {png}]", fontname=FONT_NAME,
                                  fontsize=9, color=(0.7, 0.2, 0.2))
            return
        pix = pymupdf.Pixmap(str(img))
        if pix.alpha:
            pix = pymupdf.Pixmap(pix, 0)
        scale = min(w / pix.width, (h - 16) / pix.height)
        dw, dh = pix.width * scale, pix.height * scale
        rect = pymupdf.Rect(x, y, x + dw, y + dh)
        self.page.insert_image(rect, pixmap=pix)
        self.page.draw_rect(rect, color=RULE, width=0.7)
        if caption:
            self.page.insert_text((x, y + dh + 11), caption, fontname=FONT_NAME,
                                  fontsize=8, color=MUTED)

    def subsection(self, s: str):
        self._ensure(26)
        self.y += 4
        self.page.draw_rect(pymupdf.Rect(self.x0, self.y + 1, self.x0 + 3, self.y + 14),
                            color=None, fill=PURPLE)
        self._put((self.x0 + 10, self.y + 12), s, 10.8, PURPLE, bold=True)
        self.y += 22

    def bullet(self, s: str, indent: float = 0):
        self._ensure(15)
        self.page.insert_text((self.x0 + 4 + indent, self.y + 9.8), "•",
                              fontname=FONT_NAME, fontsize=9.8, color=PURPLE)
        self.rich(s, x0=self.x0 + 14 + indent, width=self.width - 14 - indent, gap=1.5)

    def callout(self, kind: str, label: str, body: str):
        accent, bg = CALLOUTS.get(kind, CALLOUTS["TIP"])
        chip_w = self._w(kind, 8) + 12
        body_h = self.measure(body, 9.5, self.width - 32 - chip_w, 13.5)
        h = body_h + (15 if label else 0) + 12

        self._ensure(h + 8)
        r = pymupdf.Rect(self.x0, self.y, self.x1, self.y + h)
        self.page.draw_rect(r, color=None, fill=bg, radius=0.12)
        self.page.draw_rect(pymupdf.Rect(self.x0, self.y, self.x0 + 3, self.y + h),
                            color=None, fill=accent)
        y0 = self.y
        if label:
            self._put((self.x0 + 12, y0 + 13), label, 9.2, accent, bold=True)
            self.y = y0 + 17
        else:
            self.y = y0 + 5
        # 칩
        chip_w = self._w(kind, 8) + 12
        self.page.draw_rect(pymupdf.Rect(self.x0 + 12, self.y + 1, self.x0 + 12 + chip_w, self.y + 13),
                            color=None, fill=accent, radius=0.25)
        self.page.insert_text((self.x0 + 18, self.y + 10.4), kind, fontname=FONT_NAME,
                              fontsize=8, color=(1, 1, 1))
        self.rich(body, size=9.5, x0=self.x0 + 20 + chip_w, width=self.width - 32 - chip_w,
                  leading=13.5, gap=0)
        self.y = y0 + h + 8

    def pathbox(self, s: str):
        h = self.measure(s, 9.5, self.width - 24, 14) + 12
        self._ensure(h + 6)
        y0 = self.y
        self.page.draw_rect(pymupdf.Rect(self.x0, y0, self.x1, y0 + h),
                            color=None, fill=PURPLE_SOFT, radius=0.12)
        self.y = y0 + 6
        self.rich(s, size=9.5, x0=self.x0 + 12, width=self.width - 24, leading=14, gap=0)
        self.y = y0 + h + 8

    def table(self, rows: list[list[str]], size: float = 8.6):
        if not rows:
            return
        ncol = max(len(r) for r in rows)
        rows = [r + [""] * (ncol - len(r)) for r in rows]
        # 열폭: 내용 길이 비례(최소 8%)
        want = [max(self._w(self._plain(r[c]), size) for r in rows) + 12
                for c in range(ncol)]
        tot = sum(want)
        W = self.width
        cols = [max(W * 0.08, W * w / tot) for w in want]
        s = W / sum(cols)
        cols = [c * s for c in cols]

        for ri, row in enumerate(rows):
            cells = []
            hmax = 0.0
            for ci, cell in enumerate(row):
                lines = self._cell_lines(cell, size, cols[ci] - 10)
                cells.append(lines)
                hmax = max(hmax, len(lines) * (size + 3.4) + 6)
            self._ensure(hmax + 2)
            y0 = self.y
            x = self.x0
            for ci, lines in enumerate(cells):
                r = pymupdf.Rect(x, y0, x + cols[ci], y0 + hmax)
                if ri == 0:
                    self.page.draw_rect(r, color=RULE, fill=PURPLE_SOFT, width=0.5)
                else:
                    self.page.draw_rect(r, color=RULE,
                                        fill=(0.985, 0.985, 0.99) if ri % 2 else None, width=0.5)
                ty = y0 + size + 3
                for ln in lines:
                    self._draw_cell(ln, x + 5, ty, size,
                                    PURPLE if ri == 0 else INK, bold=(ri == 0))
                    ty += size + 3.4
                x += cols[ci]
            self.y = y0 + hmax
        self.y += 8

    def _plain(self, s: str) -> str:
        return "".join(text for text, _ in self._spans(s))

    def _cell_lines(self, s: str, size: float, width: float):
        """셀도 스팬 단위로 줄바꿈한다. 문자열로 자르면 **·==·` 마커가 그대로 찍힌다."""
        toks = []
        for text, kind in self._spans(re.sub(r"\s+", " ", s).strip()):
            for piece in re.split(r"(\s+)", text):
                if piece:
                    toks.append((piece, kind))
        # 한글은 공백 없이 길게 이어지는 토큰이 흔하다 → 열 폭을 넘으면 글자 단위로 쪼갠다.
        # (안 쪼개면 셀 밖으로 삐져나가고 다음 열 배경에 덮여 글자가 사라진다 — 실측)
        split = []
        for piece, kind in toks:
            if self._w(piece, size) <= width or piece.isspace():
                split.append((piece, kind)); continue
            buf = ""
            for ch in piece:
                if self._w(buf + ch, size) > width and buf:
                    split.append((buf, kind)); buf = ch
                else:
                    buf += ch
            if buf:
                split.append((buf, kind))
        toks = split
        lines, cur, w = [], [], 0.0
        for piece, kind in toks:
            pw = self._w(piece, size)
            if w + pw > width and cur:
                lines.append(cur); cur, w = [], 0.0
                if piece.isspace():
                    continue
            cur.append((piece, kind, pw)); w += pw
        if cur:
            lines.append(cur)
        return lines or [[]]

    def _draw_cell(self, line, x: float, y: float, size: float, color, bold: bool):
        for piece, kind, w in line:
            col, b, hl = self._style(kind, color)
            if hl and piece.strip():
                self.page.draw_rect(pymupdf.Rect(x, y - size + 1, x + w, y + 2),
                                    color=None, fill=HL)
            self._put((x, y), piece, size, col, b or bold)
            x += w

    # ── 문서 ──────────────────────────────────────────────
    def cover(self, meta: dict):
        """세로: 위에서 아래로. 가로: 왼쪽 제목 / 오른쪽 범례(넘침 방지)."""
        half = self.PW * 0.52
        self.x0, self.x1 = MARGIN, (half - 14) if self.split else self.PW - MARGIN
        self.y = 96 if self.split else 150
        self.rich(meta.get("kicker", "MedKOS · 임상해부학술기 3Q"), size=10, color=MUTED, gap=6)
        self.rich(f"**{self.title}**", size=20, color=INK, leading=28, gap=8)
        self.rich(self.subtitle, size=11, color=PURPLE, gap=12)
        for ln in meta.get("cover_lines", []):
            self.rich(ln, size=9.5, color=INK, gap=2)
        self.y += 10
        self.callout("주의", "공개 금지",
                     "개인 학습용 정리본. 카데바·실습영상 파생 정보를 포함할 수 있으므로 "
                     "웹 게시·재배포 금지, 개인 Drive/로컬 보관만.")

        desc = {"기출": "실제 출제·기출 포인트", "교수강조": "수업에서 강조된 부분",
                "주의": "함정·헷갈리는 지점", "임상": "임상 적용",
                "TIP": "이해 요령", "암기": "암기법·연상"}
        if self.split:
            self.x0, self.x1 = half + 14, self.PW - MARGIN
            self.y = 96
        self.subsection("범례 LEGEND")
        if self.split:
            # 칩 + 설명 한 줄짜리 목록 — 콜아웃 6개를 쌓으면 페이지를 넘긴다
            for k in ("기출", "교수강조", "주의", "임상", "TIP", "암기"):
                accent, bg = CALLOUTS[k]
                w = self._w(k, 8) + 12
                self.page.draw_rect(pymupdf.Rect(self.x0, self.y + 1, self.x0 + w, self.y + 13),
                                    color=None, fill=accent, radius=0.25)
                self.page.insert_text((self.x0 + 6, self.y + 10.4), k, fontname=FONT_NAME,
                                      fontsize=8, color=(1, 1, 1))
                self.page.insert_text((self.x0 + w + 10, self.y + 10.4), desc[k],
                                      fontname=FONT_NAME, fontsize=9.2, color=INK)
                self.y += 19
            self.y += 8
            self.callout("TIP", "읽는 법",
                         "**왼쪽은 도해(위치·구도), 오른쪽은 표(구조·신경·혈관)** 다. "
                         "같은 페이지에서 위치와 이름을 함께 확인하고, 퀴즈판으로 번호핀을 답한 뒤 "
                         "문항 카드로 채점한다.")
        else:
            for k in ("기출", "교수강조", "주의", "임상", "TIP", "암기"):
                self.callout(k, "", desc[k])
        self.x0, self.x1 = MARGIN, self.PW - MARGIN

    def footer_all(self):
        n = len(self.doc)
        for i, page in enumerate(self.doc, 1):
            page.insert_font(fontname=FONT_NAME, fontbuffer=self.fontbuf)
            label = f"{self.title} — {i} / {n}"
            w = self.font.text_length(label, fontsize=8)
            page.insert_text(((self.PW - w) / 2, self.PH - 22), label,
                             fontname=FONT_NAME, fontsize=8, color=PURPLE)


CALLOUT_RE = re.compile(r"^>\s*\[!(?P<k>[^\]]+)\]\s*(?P<rest>.*)$")


FIG_RE = re.compile(r"^!fig\s+(?P<path>\S+)(?:\s*\|\s*(?P<cap>.*))?$")


def render_body(b: Sub, body: str):
    """`## ` 를 만나면 섹션을 끊고, 그 섹션의 `!fig` 를 먼저 찾아 좌측에 건다."""
    raw = body.splitlines()
    blocks, cur = [], []
    for ln in raw:
        if ln.startswith("## "):
            if cur:
                blocks.append(cur)
            cur = [ln]
        else:
            cur.append(ln)
    if cur:
        blocks.append(cur)
    for blk in blocks:
        fig = None
        rest = []
        for ln in blk:
            m = FIG_RE.match(ln.strip())
            if m:
                fig = (m.group("path"), (m.group("cap") or "").strip())
            else:
                rest.append(ln)
        if rest and rest[0].startswith("## "):
            head = rest[0][3:]
            kr, _, en = head.partition("|")
            b.section_bar(kr.strip(), en.strip(), fig=fig)
            rest = rest[1:]
        _render_lines(b, rest)


def _render_lines(b: Sub, lines: list[str]):
    i, table_buf = 0, []

    def flush_table():
        nonlocal table_buf
        if table_buf:
            b.table(table_buf); table_buf = []

    while i < len(lines):
        ln = lines[i].rstrip()
        if ln.startswith("|") and ln.endswith("|"):
            cells = [c.strip() for c in ln.strip("|").split("|")]
            if not all(set(c) <= set("-: ") for c in cells):
                table_buf.append(cells)
            i += 1
            continue
        flush_table()
        if not ln.strip():
            b.y += 3
        elif ln.startswith("## "):
            head = ln[3:]
            kr, _, en = head.partition("|")
            b.section_bar(kr.strip(), en.strip())
        elif ln.startswith("### "):
            b.subsection(ln[4:].strip())
        elif CALLOUT_RE.match(ln):
            m = CALLOUT_RE.match(ln)
            rest = m.group("rest")
            label, _, text = rest.partition("::")
            if text:
                b.callout(m.group("k").strip(), label.strip(), text.strip())
            else:
                b.callout(m.group("k").strip(), "", label.strip())
        elif ln.startswith("=> "):
            b.pathbox(ln[3:].strip())
        elif ln.startswith("- "):
            b.bullet(ln[2:].strip())
        elif ln.startswith("  - "):
            b.bullet(ln[4:].strip(), indent=14)
        else:
            b.rich(ln.strip())
        i += 1
    flush_table()


def build(card_path: Path, output: str, root: Path = ROOT) -> Path:
    raw = card_path.read_text(encoding="utf-8")
    if not raw.startswith("---"):
        raise SystemExit("frontmatter 없음")
    _, fm, body = raw.split("---", 2)
    meta = yaml.safe_load(fm) or {}

    out = root / output
    priv = (root / ".private").resolve()
    if priv not in out.resolve().parents:
        raise SystemExit(f"출력은 .private/ 아래여야 한다: {out}")
    out.parent.mkdir(parents=True, exist_ok=True)

    doc = pymupdf.open()
    b = Sub(doc, meta.get("pdf_title") or meta.get("subtotopic", "") or meta.get("subtopic", "서브노트"),
            meta.get("pdf_subtitle", ""),
            split=str(meta.get("layout", "")).lower() in ("split", "landscape", "가로"))
    b.cover(meta)
    if not b.split:
        b.new_page(plain=True)
    render_body(b, body)
    b.footer_all()
    try:
        doc.subset_fonts()          # 한글 폰트 통째 삽입 방지(1.7MB → 수십 KB)
    except Exception:
        pass
    doc.save(str(out), deflate=True, garbage=3)
    doc.close()
    return out


def selftest() -> int:
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        (root / ".private/anatomy/pdf").mkdir(parents=True)
        card = root / "c.md"
        card.write_text("---\nsubtopic: 테스트\npdf_subtitle: sub\n---\n"
                        "## 1. 제목 | English\n### 1) 소제목\n"
                        "- 불릿 **강조** ==형광== `english`\n"
                        "| 근육 | 신경 |\n|---|---|\n| 등세모근 | 더부신경 |\n"
                        "> [!기출] 라벨 :: 본문 내용\n=> A → B → C\n", encoding="utf-8")
        out = build(card, ".private/anatomy/pdf/t.pdf", root=root)
        assert out.exists() and out.stat().st_size > 900
        d = pymupdf.open(str(out))
        txt = "".join(p.get_text() for p in d)
        for must in ("제목", "등세모근", "더부신경", "기출", "A → B → C"):
            assert must in txt, f"누락: {must}"
        assert out.stat().st_size < 400_000, f"폰트 서브셋 실패? {out.stat().st_size}"
        d.close()
    print("[ OK ] anatomy_subnote selftest")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--card"); ap.add_argument("--output")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not (a.card and a.output):
        print("--card/--output 필요 (또는 --selftest)"); return 2
    p = build(Path(a.card), a.output)
    print(f"생성: {p} ({p.stat().st_size/1024:.0f}KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
