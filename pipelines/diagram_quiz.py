#!/usr/bin/env python3
"""diagram_quiz.py — 라벨판 SVG 에서 **퀴즈판**을 만든다(결정론).

자체 제작 도해는 `-labeled.svg` 한 벌만 손으로 그리고, 번호핀만 남긴 `-quiz.svg` 는
여기서 기계적으로 뽑는다. 두 벌을 따로 그리면 반드시 어긋난다 — 라벨을 고쳤는데
퀴즈판은 옛 이름을 가리키는 사고가 나기 때문이다.

규칙: `<g class="ans" data-n="N"> … </g>` 안의 `<text class="lab">` · `<text class="en">`
      을 지운다. 도형·번호핀(`class="pin"`, `class="pinn"`)은 그대로 남는다.
      `ans` 밖의 글자(제목·요약·범례)는 손대지 않는다 — 그건 답이 아니라 안내문이다.

사용:
  python pipelines/diagram_quiz.py --svg docs/assets/anatomy/diag-popliteal-labeled.svg
  python pipelines/diagram_quiz.py --all
  python pipelines/diagram_quiz.py --selftest
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "docs/assets/anatomy"

ANS_RE = re.compile(r'<g class="ans"[^>]*>.*?</g>', re.S)
DROP_RE = re.compile(r'\s*<text class="(?:lab|en)"[^>]*>.*?</text>', re.S)


def to_quiz(svg: str) -> str:
    """라벨판 → 퀴즈판. `ans` 그룹 안의 이름표만 지운다."""
    return ANS_RE.sub(lambda m: DROP_RE.sub("", m.group(0)), svg)


STYLE_RE = re.compile(r"<style>(.*?)</style>", re.S)
RULE_RE = re.compile(r"\.([\w-]+)\s*\{([^}]*)\}")
# rx/ry 는 CSS 로 주면 렌더러가 무시한다 → 속성으로 옮긴다
ATTR_ONLY = {"rx", "ry"}


def inline_css(svg: str) -> str:
    """`.클래스{...}` 규칙을 **요소 속성으로 펴 넣는다**.

    PDF 렌더러(PyMuPDF)는 SVG 의 **요소 선택자**(`text{...}`)는 읽지만 **클래스 선택자**는
    무시한다 — 클래스로만 색·크기를 준 도해는 예습 PDF 에서 통째로 검게 나온다(실측).
    웹에서는 잘 보여서 더 늦게 발견된다. 그래서 자산을 만들 때 아예 속성으로 펴 둔다.
    """
    m = STYLE_RE.search(svg)
    if not m:
        return svg
    rules = {k: v.strip().rstrip(";") for k, v in RULE_RE.findall(m.group(1))}
    if not rules:
        return svg

    def fix(tag: str) -> str:
        cm = re.search(r'class="([^"]+)"', tag)
        if not cm:
            return tag
        decls: list[tuple[str, str]] = []
        for cls in cm.group(1).split():
            for d in rules.get(cls, "").split(";"):
                if ":" in d:
                    p, v = d.split(":", 1)
                    decls.append((p.strip(), v.strip()))
        if not decls:
            return tag
        attrs = " ".join(f'{p}="{v}"' for p, v in decls if p in ATTR_ONLY)
        style = ";".join(f"{p}:{v}" for p, v in decls if p not in ATTR_ONLY)
        add = (f' {attrs}' if attrs else "") + (f' style="{style}"' if style else "")
        close = "/>" if tag.rstrip().endswith("/>") else ">"
        core = tag.rstrip()[:-len(close)].rstrip()
        return core + add + close

    # 클래스 규칙만 걷어내고 요소 선택자(text{...})는 남긴다
    kept = RULE_RE.sub("", m.group(1)).strip()
    body = svg[m.end():]
    body = re.sub(r"<(?!/)[^>]+>", lambda t: fix(t.group(0)), body)
    head = svg[:m.start()] + (f"<style>{kept}</style>" if kept else "")
    return head + body


def pins(svg: str) -> list[int]:
    return sorted(int(n) for n in re.findall(r'<g class="ans" data-n="(\d+)"', svg))


def answers(svg: str) -> list[tuple[int, str]]:
    """(번호, 라벨 첫 줄) — 문항 카드의 정답표를 사람이 옮겨 적지 않게 한다."""
    out = []
    for m in ANS_RE.finditer(svg):
        n = int(re.search(r'data-n="(\d+)"', m.group(0)).group(1))
        lab = re.search(r'<text class="lab"[^>]*>(.*?)</text>', m.group(0), re.S)
        if lab:
            txt = re.sub(r"<[^>]+>", "", lab.group(1))
            out.append((n, " ".join(txt.split())))
    return sorted(out)


def build(labeled: Path, dry: bool) -> Path:
    out = labeled.with_name(labeled.name.replace("-labeled.svg", "-quiz.svg"))
    svg = labeled.read_text(encoding="utf-8")
    flat = inline_css(svg)
    if flat != svg and not dry:      # 라벨판 자체도 속성으로 펴서 저장(멱등)
        labeled.write_text(flat, encoding="utf-8")
    svg = flat
    ns = pins(svg)
    if not ns:
        raise SystemExit(f"{labeled.name}: `class=\"ans\"` 그룹이 없다 — 퀴즈판을 못 만든다")
    if ns != list(range(1, len(ns) + 1)):
        raise SystemExit(f"{labeled.name}: 번호가 1..N 이 아니다 → {ns}")
    if not dry:
        out.write_text(to_quiz(svg), encoding="utf-8")
    print(f"  {'DRY ' if dry else 'MADE'} {out.name}  (핀 {len(ns)})")
    return out


def selftest() -> int:
    src = ('<svg><g class="ans" data-n="1"><rect/>'
           '<circle class="pin"/><text class="pinn">1</text>'
           '<text class="lab">정강신경</text><text class="en">tibial n.</text></g>'
           '<text class="h">제목은 남는다</text></svg>')
    q = to_quiz(src)
    assert "정강신경" not in q and "tibial" not in q, q
    assert 'class="pin"' in q and ">1<" in q, q
    assert "제목은 남는다" in q, "안내문까지 지웠다"
    assert pins(src) == [1]
    assert answers(src) == [(1, "정강신경")]
    # 클래스 규칙은 속성으로 펴지고, 요소 선택자는 남는다
    css = ('<svg><defs><style>text{stroke:#000}.lab{fill:#fff;font-size:12px}'
           '.panel{fill:#111;rx:10}</style></defs>'
           '<text class="lab">가</text><rect class="panel"/></svg>')
    f = inline_css(css)
    assert 'style="fill:#fff;font-size:12px"' in f, f
    assert 'rx="10"' in f and 'style="fill:#111"' in f, f
    assert "text{stroke:#000}" in f and ".lab{" not in f, f
    assert inline_css(f) == f, "멱등이 아니다"
    print("[ OK ] diagram_quiz selftest")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--svg")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--answers", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    todo = ([Path(a.svg)] if a.svg else
            [p for p in sorted(ASSETS.glob("*-labeled.svg"))
             if '<g class="ans"' in p.read_text(encoding="utf-8")])
    if not todo:
        print("대상 없음 — `class=\"ans\"` 를 쓴 라벨판이 있어야 한다")
        return 2
    for p in todo:
        if a.answers:
            print(f"{p.name}")
            for n, t in answers(p.read_text(encoding="utf-8")):
                print(f"  {n:2d}. {t}")
            continue
        build(p, a.dry_run)
    return 0


if __name__ == "__main__":
    sys.exit(main())
