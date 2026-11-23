"""book_layout.py — 과별 학습서의 배치를 PDF 로 그리지 않고 잰다(build_books.py 의 배치 탐색용, 2026-11-23).

왜: 배치 탐색은 도식 · 그림 자리를 하나 바꿀 때마다 책 전체를 PDF 로 다시 그리고 검증했다(81쪽 책 한 번에 30초 —
순환기내과는 882번, 4시간). 여기서는 책을 Chromium 에 **한 번** 올리고, 바뀐 단원만 갈아 끼운 뒤 블록의 자리를 재서
`validate_pdf` 의 배치 검사(빈 공간 · 단 아래 빈칸 · 두 단 도식 위아래 좁은 띠 · 고립된 제목)를 같은 식으로 계산한다
(81쪽 책 한 번에 0.3초 안팎). PDF 는 고른 배치로 마지막에만 그리고, 진짜 검증은 그 PDF 로 한다.

화면에서 인쇄 쪽 나눔을 얻는 법(실제 PDF 와 대조해 정했다):
- `emulate_media("print")` 만으로는 쪽이 나뉘지 않는다. body 를 **바깥 다단**(단 하나 = 한 쪽)으로 만들면 안쪽 두 단
  (`.cols`)이 쪽마다 나뉘고 `getClientRects()` 가 조각마다 사각형을 준다 — 쪽 = floor(x / 쪽 폭).
- 쪽 상자 크기는 mm 를 px 로 바꾼 값(718.11 × 1046.92)이 아니다. Chromium 은 쪽과 여백을 정수 px 로 맞춰 **719 × 1047**
  로 배치한다(단 폭이 0.45 px 달라 줄바꿈이 가끔 어긋났다). 버전 · 운영체제에 기대지 않게 `print_box` 가 탐침 PDF 로 잰다.
- `overflow:hidden` 상자(혼동 카드)는 화면에서는 쪼개지지 않는 덩어리, 인쇄에서는 쪼개진다 → 잴 때는 푼다.
- 그 배치가 **그리기 단계에 닿으면 탭이 죽는다**(Chromium 151, 반복되는 표 머리줄). 측정 CSS 는 `html.mm` 아래에만 두고
  한 번의 evaluate 안에서 class 를 켜고 · 재고 · 끈다. 평소에는 body 를 `content-visibility:hidden` 으로 감춰 둔다.
- 그래도 큰 책에서는 1 % 안팎이 실제와 다르다(81쪽 책의 제목 387개 중 4개가 다른 단 — 쪽 끝에서 카드가 쪼개지는 자리).
  그래서 측정은 **고르는 데만** 쓰고, 결과는 PDF 검증이 정한다(build_books 의 「예측에 없던 오류 → PDF 로 고치기」).
"""
from __future__ import annotations

import json
import math
import tempfile
from pathlib import Path
from typing import Callable

PX_PT = 96 / 72

# 쪽 상자 탐침 — 폭 100% 막대 하나 + 0.25 px 줄을 두 쪽 넘게 채운다. 2쪽에 들어간 줄 수 × 0.25 = 쪽 높이.
PROBE_ROW = 0.25


def probe_html(page: dict) -> str:
    rows = "".join('<div class="r"></div>' for _ in range(int(page["h"] * 96 / 25.4 / PROBE_ROW * 2.3)))
    return (f'<!doctype html><html><head><meta charset="utf-8"><style>'
            f'@page{{size:{page["w"]}mm {page["h"]}mm; margin:{page["mt"]}mm {page["mr"]}mm {page["mb"]}mm {page["ml"]}mm}}'
            f'html,body{{margin:0}} .w{{height:20px;background:#00f}} .r{{height:{PROBE_ROW}px;width:40px;background:#f00;break-inside:avoid}}'
            f'</style></head><body><div class="w"></div>{rows}</body></html>')


def print_box(render: Callable[[str, Path], None], page: dict) -> tuple[float, float]:
    """인쇄 배치의 본문 상자(CSS px). `render(html, pdf_path)` 는 책과 같은 설정으로 PDF 를 만드는 함수."""
    import pymupdf
    with tempfile.TemporaryDirectory() as td:
        out = Path(td) / "probe.pdf"
        render(probe_html(page), out)
        with pymupdf.open(out) as doc:
            if doc.page_count < 3:
                raise RuntimeError("쪽 상자 탐침이 세 쪽이 안 된다")
            bars = [d["rect"] for d in doc[0].get_drawings() if d.get("fill") and d["fill"][2] > 0.9 and d["fill"][0] < 0.1]
            rows = [d["rect"] for d in doc[1].get_drawings() if d.get("fill") and d["fill"][0] > 0.9 and d["fill"][2] < 0.1]
    if not bars or not rows:
        raise RuntimeError("쪽 상자 탐침에서 도형을 찾지 못했다")
    w, h = max(r.width for r in bars) * PX_PT, len(rows) * PROBE_ROW
    mm = 96 / 25.4
    want = ((page["w"] - page["ml"] - page["mr"]) * mm, (page["h"] - page["mt"] - page["mb"]) * mm)
    if abs(w - want[0]) > 4 or abs(h - want[1]) > 4:          # 여백 반올림은 1~2 px 안이다 — 그보다 크면 탐침을 못 믿는다
        raise RuntimeError(f"쪽 상자 탐침 값이 이상하다: {w:.2f}×{h:.2f}px (설계 {want[0]:.2f}×{want[1]:.2f})")
    return round(w * 64) / 64, round(h * 64) / 64


def measure_css(w: float, h: float) -> str:
    return (
        # 평소에는 배치 · 그리기를 하지 않는다. display:none 은 배치 나무를 버렸다 다시 지어 한 번 재는 데 두 배 넘게 걸렸다(81쪽 0.47초 → 0.19초)
        "html:not(.mm) body{content-visibility:hidden}"
        "html.mm,html.mm body{margin:0;padding:0}"
        f"html.mm body{{width:{w}px;height:{h}px;column-count:1;column-width:{w}px;column-gap:0;column-fill:auto}}"
        "html.mm .tocpage{break-after:column}"                     # 바깥 다단 안에서는 쪽 나눔 대신 단 나눔
        "html.mm body *{overflow:visible !important}"              # 화면의 overflow:hidden 상자는 안 쪼개진다 — 인쇄는 쪼갠다
    )


# 한 번의 호출 안에서: 단원 갈아 끼우기 → 측정 CSS 켜기 → 재기 → 끄기. 측정 배치가 그리기 단계에 닿지 않게 한다.
MEASURE_JS = r"""
(arg) => {
  for (const [anchor, html] of arg.swaps) {
    const el = document.getElementById(anchor);
    const sec = el && el.closest('section.unit');
    if (!sec) throw new Error('단원을 찾지 못했다: ' + anchor);
    sec.outerHTML = html;
  }
  const root = document.documentElement;
  const T0 = performance.now();
  root.classList.add('mm');
  try {
    const bb = document.body.getBoundingClientRect();
    const PW = bb.width, PH = bb.height, mid = PW / 2, EDGE = 20 * 96 / 72, PT = 96 / 72;
    const pages = Math.max(1, Math.round(root.scrollWidth / PW));
    const P = [];
    for (let i = 0; i < pages; i++) P.push({t: [[], []], x1: [], b: [[], []], wide: [], orph: []});
    const place = (r) => {
      if (r.width <= 0.5 || r.height <= 0.5) return null;
      const pg = Math.floor((r.left + 0.5) / PW);
      if (pg < 0 || pg >= pages) return null;
      const x0 = r.left - pg * PW, x1 = r.right - pg * PW, y0 = Math.max(0, r.top), y1 = Math.min(PH, r.bottom);
      if (y1 <= y0) return null;
      // validate_pdf 와 같은 규칙: 가운데를 20pt 넘게 걸치면 두 단 모두, 아니면 중심이 있는 단
      return {pg, x0, x1, y0, y1, both: x0 < mid - EDGE && x1 > mid + EDGE, c: (x0 + x1) / 2 < mid ? 0 : 1};
    };
    const T1 = performance.now();
    // 글줄
    const rg = document.createRange();
    const tw = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
    let n;
    while ((n = tw.nextNode())) {
      if (!n.nodeValue.trim()) continue;
      const pe = n.parentElement;
      if (!pe || pe.closest('svg')) continue;
      rg.selectNodeContents(n);
      for (const r of rg.getClientRects()) {
        const q = place(r);
        if (!q) continue;
        P[q.pg].t[q.c].push([q.y0, q.y1]);
        if (q.both) P[q.pg].b[1 - q.c].push([q.y0, q.y1]);          // 두 단 폭 글은 다른 단의 내용으로도 센다
        else if (q.x0 > mid) P[q.pg].x1.push([q.y0, q.y1]);          // 오른쪽 단에만 있는 글(두 단 도식 위 띠 판정)
      }
    }
    const T2 = performance.now();
    // 상자(배경 · 테두리가 있는 블록, 그림, 도식) — 상자 안쪽은 다시 보지 않는다
    const BLOCK = new Set(['DIV', 'SECTION', 'P', 'UL', 'OL', 'LI', 'TABLE', 'FIGURE', 'FIGCAPTION', 'H1', 'H2', 'H3', 'H4', 'NAV', 'MAIN', 'BLOCKQUOTE']);
    const boxy = (el) => {
      const cs = getComputedStyle(el);
      if (cs.backgroundColor !== 'rgba(0, 0, 0, 0)' && cs.backgroundColor !== 'transparent') return true;
      for (const s of ['Top', 'Right', 'Bottom', 'Left'])
        if (cs['border' + s + 'Style'] !== 'none' && parseFloat(cs['border' + s + 'Width']) > 0) return true;
      return false;
    };
    const walk = (el) => {
      for (const ch of el.children) {
        const tag = ch.tagName;
        const isBox = tag === 'IMG' || tag === 'svg' || (BLOCK.has(tag) && boxy(ch));
        if (isBox) {
          for (const r of ch.getClientRects()) {
            const q = place(r);
            if (!q) continue;
            for (const c of (q.both ? [0, 1] : [q.c])) P[q.pg].b[c].push([q.y0, q.y1]);
            if (q.x1 - q.x0 > 0.8 * PW && q.y1 - q.y0 > 3 * PT) P[q.pg].wide.push([q.y0, q.y1]);
          }
        } else if (BLOCK.has(tag)) walk(ch);
      }
    };
    walk(document.body);
    const T3 = performance.now();
    // 고립된 제목: 제목의 마지막 줄 아래, 같은 단에 이어지는 글이 없다
    for (const el of document.querySelectorAll('h2, h3, h4, .tb .tt, .cmap .mh')) {
      rg.selectNodeContents(el);
      const rs = rg.getClientRects();
      if (!rs.length) continue;
      const q = place(rs[rs.length - 1]);
      if (!q) continue;
      if (!P[q.pg].t[q.c].some(([a]) => a > q.y1 - PT)) P[q.pg].orph.push(el.textContent.trim().slice(0, 20));
    }
    // 겹치거나 붙은 구간을 합쳐 보낸다(2px 안 — 문단 안의 줄들이 한 구간이 된다)
    const merge = (v) => {
      v.sort((a, b) => a[0] - b[0]);
      const out = [];
      for (const [a, b] of v) {
        const last = out[out.length - 1];
        if (last && a <= last[1] + 2) last[1] = Math.max(last[1], b); else out.push([a, b]);
      }
      return out.map(([a, b]) => [Math.round(a * 100) / 100, Math.round(b * 100) / 100]);
    };
    for (const pg of P) { pg.t = pg.t.map(merge); pg.b = pg.b.map(merge); pg.x1 = merge(pg.x1); }
    const pm = {};
    for (const el of document.querySelectorAll('.uh[id]')) {
      const r = el.getClientRects()[0];
      if (r) pm[el.id] = Math.floor((r.left + 0.5) / PW) + 1;
    }
    // 조각난 도식(한 단 · 한 쪽에 들어가지 못해 쪼개졌다) — 그 단원의 머리 id 로 알린다
    const split = [];
    for (const f of document.querySelectorAll('figure.dia')) {
      if (f.getClientRects().length < 2) continue;
      const sec = f.closest('section.unit'), h = sec && sec.querySelector('.uh[id]');
      if (h) split.push(h.id);
    }
    // 글자열 하나로 보낸다 — 겹친 배열 수천 개를 그대로 넘기면 주고받는 데만 0.3초가 든다
    return JSON.stringify({pages, PW, PH, P, pm, split, ms: [T1 - T0, T2 - T1, T3 - T2, performance.now() - T3].map(Math.round)});
  } finally {
    root.classList.remove('mm');
  }
}
"""

LAYOUT_WORDS = ("빈 공간", "고립된 제목", "좁은 띠")


def layout_errors(errs: list[str]) -> list[str]:
    """검증 오류 가운데 배치 문제(빈 공간 · 고립된 제목 · 좁은 띠)만."""
    return [e for e in errs if any(w in e for w in LAYOUT_WORDS)]


def error_key(e: str) -> tuple[int, str]:
    """(쪽, 종류) — 측정의 예측과 PDF 검증의 오류를 맞대는 열쇠(% 값은 조금 달라도 같은 문제다)."""
    import re
    m = re.match(r"(\d+)쪽", e)
    kind = next((k for k in ("빈 공간이 크다", "왼쪽 단 아래", "오른쪽 단 아래", "도식 아래 좁은 띠", "도식 위 좁은 띠", "고립된 제목") if k in e), "기타")
    return (int(m.group(1)) if m else 0, kind)


def _covered(segs: list, tol: float) -> float:
    cur, tot = None, 0.0
    for a0, a1 in sorted(segs):
        if cur and a0 <= cur[1] + tol:
            cur = (cur[0], max(cur[1], a1))
        else:
            if cur:
                tot += cur[1] - cur[0]
            cur = (a0, a1)
    if cur:
        tot += cur[1] - cur[0]
    return tot


def problems(m: dict, margin: float = 0.0) -> list[str]:
    """측정값 → `validate_pdf` 와 같은 글귀의 배치 문제 목록. 순수 함수(시험에서 손으로 만든 값으로 고정한다).

    m = {pages, PH, P:[{t:[왼,오], b:[왼,오], x1, wide, orph}]} — t 글줄 · b 상자의 세로 구간(px, 쪽 상자 위쪽이 0),
    x1 오른쪽 단에만 있는 글줄, wide 두 단 폭 상자, orph 아래에 글이 없는 제목.
    margin = 문턱을 그만큼 엄하게(0.01 이면 빈칸 29 % 부터 문제로) — 측정이 실제와 조금 달라도 탐색이 아슬아슬한 배치를 고르지 않게."""
    H, n = float(m["PH"]), int(m["pages"])
    errs: list[str] = []
    for i, pg in enumerate(m["P"]):
        no = i + 1
        segs = {c: [tuple(x) for x in pg["t"][c]] + [tuple(x) for x in pg["b"][c]] for c in (0, 1)}
        cov = sum(_covered(segs[c], 6 * PX_PT) / H / 2 for c in (0, 1))
        if 0 < i < n - 1:                                  # 1쪽 = 목차 쪽, 마지막 쪽은 덜 차도 정상
            if cov < 0.5 + margin:
                errs.append(f"{no}쪽에 빈 공간이 크다(내용 {cov:.0%})")
            for c, name in ((0, "왼쪽"), (1, "오른쪽")):
                low = max([b for _, b in segs[c]] or [0.0])
                gap = (H - low) / H
                if gap > 0.3 - margin:
                    errs.append(f"{no}쪽 {name} 단 아래가 비어 있다(빈 공간 {gap:.0%})")
        wide = [tuple(x) for x in pg.get("wide") or []]
        if wide and any(b - a > 40 * PX_PT for a, b in wide) and i < n - 1:
            y0, y1 = min(a for a, _ in wide), max(b for _, b in wide)
            text = pg["t"][0] + pg["t"][1]
            below = any(a > y1 + 2 * PX_PT for a, _ in text)
            above = any(b < y0 - 2 * PX_PT for _, b in text)
            if below and (H - y1) < (0.2 + margin) * H:
                errs.append(f"{no}쪽 두 단 도식 아래 좁은 띠(빈 공간 아님, {(H - y1) / H:.0%}) — 좌우로 오가며 읽힌다")
            elif above and y0 < (0.2 + margin) * H and any(b < y0 - 2 * PX_PT for _, b in pg.get("x1") or []):
                errs.append(f"{no}쪽 두 단 도식 위 좁은 띠({y0 / H:.0%}) — 좌우로 오가며 읽힌다")
        for text_ in pg.get("orph") or []:
            errs.append(f"{no}쪽 고립된 제목: {text_!r}")
    return errs


class Lab:
    """책 한 권을 올려 둔 측정용 탭. `measure(swaps)` = 단원 HTML 을 갈아 끼우고 잰 값."""

    def __init__(self, browser, html_text: str, box: tuple[float, float]):
        self._td = tempfile.TemporaryDirectory()
        src = Path(self._td.name) / "book.html"            # 파일로 열어야 글꼴 · 그림(file://)이 읽힌다
        src.write_text(html_text, encoding="utf-8")
        self.page = browser.new_page(viewport={"width": math.ceil(box[0]) + 1, "height": math.ceil(box[1]) + 3})
        try:
            self.page.emulate_media(media="print")
            self.page.goto(src.as_uri(), wait_until="load")
            self.page.evaluate("document.fonts.ready")
            self.page.add_style_tag(content=measure_css(*box))
        except Exception:
            self.close()
            raise
        self.count = 0

    def measure(self, swaps: list[tuple[str, str]] | None = None) -> dict:
        self.count += 1
        return json.loads(self.page.evaluate(MEASURE_JS, {"swaps": [list(s) for s in swaps or []]}))

    def close(self) -> None:
        try:
            self.page.close()
        except Exception:
            pass
        self._td.cleanup()
