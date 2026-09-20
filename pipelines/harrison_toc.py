"""harrison_toc.py — 해리슨 21판 PDF 의 목차를 한 번만 기계로 뽑아 `content/outline/harrison_toc.json` 으로 굳힌다.

왜: 과별 학습서의 단원 순서를 「해리슨 서술 순서」로 맞추기 위해서다(2026-09-21 사용자 지시).
순서를 정할 때마다 4,132쪽짜리 PDF 를 다시 열면 토큰이 든다 — **목차를 한 번 파일로 만들어 두면
그 뒤로는 이 JSON 만 읽는다.** 정리본을 쓸 때도 이 JSON 이 「그 주제는 몇 장·PDF 몇 쪽」을 알려 주므로
해당 장만 읽으면 된다(`harrison_read.py`).

PDF 에는 북마크가 없다. 앞쪽 목차 지면(PDF 6~16쪽)의 줄을 상태 기계로 읽는다:
  PART n Title            부(part) 시작. 제목이 다음 줄로 이어질 수 있다.
  SECTION n Title         절(section) 시작. 〃
  n Title ......... 123   장(chapter)과 인쇄쪽. 제목이 여러 줄로 이어질 수 있고, 다음 줄은 저자다.

인쇄쪽 ↔ PDF 인덱스: **PDF 인덱스 = 인쇄쪽 + 40**(표지·목차 분량, 2026-09-05 실측).
장의 끝쪽은 다음 장 시작 − 1 로 잡는다(마지막 장은 본문 끝).

사용:
  python pipelines/harrison_toc.py                 # 추출 → content/outline/harrison_toc.json
  python pipelines/harrison_toc.py --check         # 파일이 최신인지·알려진 기준점이 맞는지만 본다
  python pipelines/harrison_toc.py --pdf <경로>    # 다른 위치의 PDF

저작권: 이 스크립트는 **목차(장 번호·제목·쪽)** 만 저장한다. 본문 텍스트는 저장소에 넣지 않는다.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "content" / "outline" / "harrison_toc.json"
DEFAULT_PDF = Path(r"G:\내 드라이브\교과서\Harrison_s Principles of Internal Medicine, Twenty-First Edition.pdf")
TOC_PAGES = range(6, 17)          # PDF 인덱스(0부터) — Contents 지면
OFFSET = 40                       # PDF 인덱스 = 인쇄쪽 + OFFSET
BODY_END = 4131                   # 본문 마지막 PDF 인덱스(뒤는 찾아보기)

PART = re.compile(r"^\s*PART\s+(\d+)\s*(.*)$")
SECTION = re.compile(r"^\s*SECTION\s+(\d+)\s*(.*)$")
CH_START = re.compile(r"^\s*(\d{1,3})\s+(\S.*)$")
CH_END = re.compile(r"^(.*?)\s*\.{3,}\s*(\d{1,4})\s*$")
SKIP = re.compile(r"^\s*(CONTENTS|Contents|[ivxl]+|\s*)\s*$")

# 뽑은 결과가 맞는지 보는 기준점(본문에서 직접 확인한 것) — 하나라도 어긋나면 멈춘다.
ANCHORS = {53: ("Fluid and Electrolyte Disturbances", 338),        # 본문 PDF 378쪽에 장 표제 확인(2026-09-21)
           392: ("Disorders of the Female Reproductive System", 3027)}


def clean(s: str) -> str:
    return re.sub(r"\s+", " ", s.replace("\u2019", "'")).strip()


def parse(pdf: Path) -> dict:
    import pymupdf

    doc = pymupdf.open(pdf)
    parts: list[dict] = []
    part: dict | None = None
    section: str | None = None
    section_n: int | None = None
    chapters: list[dict] = []
    buf: list[str] = []
    ch_no: int | None = None
    heading: list[str] | None = None          # PART/SECTION 제목이 다음 줄로 이어질 때
    heading_kind = ""

    def flush_heading() -> None:
        nonlocal heading, heading_kind, part, section, section_n
        if heading is None:
            return
        title = clean(" ".join(heading[1:]))
        if heading_kind == "part":
            part = {"n": int(heading[0]), "title": title, "chapters": []}
            parts.append(part)
            section, section_n = None, None
        else:
            section, section_n = title, int(heading[0])
        heading, heading_kind = None, ""

    for i in TOC_PAGES:
        for raw in doc[i].get_text().splitlines():
            line = raw.rstrip()
            if SKIP.match(line):
                flush_heading()
                continue
            m = PART.match(line)
            if m:
                flush_heading()
                heading, heading_kind = [m.group(1), m.group(2)], "part"
                continue
            m = SECTION.match(line)
            if m:
                flush_heading()
                heading, heading_kind = [m.group(1), m.group(2)], "section"
                continue
            m = CH_START.match(line) if ch_no is None else None
            if m:
                flush_heading()
                ch_no, buf = int(m.group(1)), [m.group(2)]
            elif ch_no is not None:
                buf.append(line)
            elif heading is not None:
                heading.append(line)            # PART/SECTION 제목의 이어지는 줄
                continue
            else:
                continue
            m = CH_END.match(" ".join(buf))
            if not m or ch_no is None:
                continue
            title, page = clean(m.group(1)), int(m.group(2))
            if part is not None and 1 <= page <= BODY_END - OFFSET:
                chapters.append({"n": ch_no, "title": title, "page": page,
                                 "part": part["n"], "section": section, "section_n": section_n})
                part["chapters"].append(ch_no)
            ch_no, buf = None, []

    chapters.sort(key=lambda c: c["n"])
    for a, b in zip(chapters, chapters[1:] + [None]):
        a["pdf"] = a["page"] + OFFSET
        a["pdf_end"] = (b["page"] + OFFSET - 1) if b else BODY_END
    return {"edition": "21", "source": pdf.name, "offset": OFFSET,
            "note": "인쇄쪽 = pdf − offset. pdf/pdf_end 는 0부터 세는 PDF 인덱스(pymupdf 기준)",
            "parts": [{"n": p["n"], "title": p["title"],
                       "chapters": [c["n"] for c in chapters if c["part"] == p["n"]]} for p in parts],
            "chapters": chapters}


def verify(data: dict) -> list[str]:
    errs = []
    by_n = {c["n"]: c for c in data["chapters"]}
    for n, (title, page) in ANCHORS.items():
        c = by_n.get(n)
        if not c:
            errs.append(f"{n}장이 목차에 없다")
        elif title.lower() not in c["title"].lower() or c["page"] != page:
            errs.append(f"{n}장이 기준점과 다르다: {c['title']!r} p.{c['page']} (기대 {title!r} p.{page})")
    ns = [c["n"] for c in data["chapters"]]
    missing = [n for n in range(1, max(ns) + 1) if n not in set(ns)] if ns else []
    if missing:
        errs.append(f"빠진 장 번호 {missing[:10]}{'…' if len(missing) > 10 else ''}")
    if len(ns) != len(set(ns)):
        errs.append("장 번호가 중복됐다")
    if not any(p["title"].startswith("Disorders of the Cardiovascular") for p in data["parts"]):
        errs.append("부(part) 제목을 제대로 읽지 못했다")
    return errs


def load() -> dict:
    return json.loads(OUT.read_text(encoding="utf-8"))


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--pdf", default=str(DEFAULT_PDF))
    ap.add_argument("--check", action="store_true", help="이미 만든 JSON 만 검사한다(PDF 없이)")
    a = ap.parse_args(argv)
    if a.check:
        if not OUT.exists():
            print(f"{OUT.relative_to(ROOT)} 가 없다 — `python pipelines/harrison_toc.py` 로 한 번 만든다")
            return 1
        data = load()
    else:
        pdf = Path(a.pdf)
        if not pdf.exists():
            print(f"PDF 를 찾지 못했다: {pdf}")
            return 1
        data = parse(pdf)
    errs = verify(data)
    for e in errs:
        print("  ✗", e)
    if errs:
        return 1
    if not a.check:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
    print(f"부 {len(data['parts'])} · 장 {len(data['chapters'])} — {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
