"""harrison_read.py — 해리슨 21판에서 **필요한 장만** 읽는다(전체를 훑지 않기 위한 도구).

왜: 정리본을 쓸 때 근거를 확인하려고 4,132쪽 PDF 를 뒤지면 토큰이 크게 든다. 기본틀(`outline.py`)이
「이 슬롯 = 해리슨 몇 장」을 이미 알고 있으므로, 그 장의 쪽 범위만 텍스트로 뽑아 읽으면 된다.

사용:
  python pipelines/harrison_read.py --chapter 255              # 그 장 전체(기본 12,000자까지)
  python pipelines/harrison_read.py --slot h255 --grep "QT"    # 슬롯으로 찾고, 맞는 줄만
  python pipelines/harrison_read.py --chapter 255 --pages 1923-1925   # 인쇄쪽으로 좁히기
  python pipelines/harrison_read.py --find "long QT"           # 어느 장인지부터 찾기(PDF 안 연다)

출력은 화면에만 쓴다. **본문을 저장소 파일로 저장하지 않는다**(교과서 저작권).
정리본에 인용할 때는 확인한 인쇄쪽을 `[[harrison-21: p.1923]]` 처럼 적는다.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "pipelines"))
import harrison_toc as ht                                        # noqa: E402
import outline as ol                                             # noqa: E402

PDF = ht.DEFAULT_PDF
MAX_CHARS = 12000


def chapter_of_slot(slot_id: str) -> list[int]:
    books, _ = ol.load()
    s = ol.index(books).get(slot_id)
    return s.chapters if s else []


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--chapter", type=int)
    ap.add_argument("--slot", help="기본틀 슬롯 id(h255 · gyn.infertility …)")
    ap.add_argument("--find", help="장 제목으로 찾기만 한다")
    ap.add_argument("--pages", help="인쇄쪽 범위로 좁힌다(예: 1923-1925)")
    ap.add_argument("--grep", help="그 장 안에서 이 말이 든 줄만")
    ap.add_argument("--max-chars", type=int, default=MAX_CHARS)
    ap.add_argument("--pdf", default=str(PDF))
    a = ap.parse_args(argv)

    toc = ht.load()
    by_n = {c["n"]: c for c in toc["chapters"]}
    if a.find:
        q = a.find.lower()
        for c in toc["chapters"]:
            if q in c["title"].lower():
                print(f"  {c['n']:3}장  {c['title'][:66]:68} 인쇄쪽 {c['page']}~{c['pdf_end'] - toc['offset']}")
        return 0

    ns = [a.chapter] if a.chapter else chapter_of_slot(a.slot or "")
    if not ns:
        print("--chapter 나 --slot 이 필요하다(어느 장인지 모르면 --find 로 먼저 찾는다)")
        return 1

    pdf = Path(a.pdf)
    if not pdf.exists():
        print(f"PDF 를 찾지 못했다: {pdf}")
        return 1
    import pymupdf

    doc = pymupdf.open(pdf)
    lo_p = hi_p = None
    if a.pages:
        m = re.match(r"\s*(\d+)\s*(?:-\s*(\d+))?\s*$", a.pages)
        if not m:
            print("--pages 는 1923 또는 1923-1925 형식")
            return 1
        lo_p, hi_p = int(m.group(1)), int(m.group(2) or m.group(1))

    total = 0
    for n in ns:
        c = by_n.get(n)
        if not c:
            print(f"{n}장이 목차에 없다")
            continue
        lo, hi = c["pdf"], c["pdf_end"]
        if lo_p is not None:
            lo, hi = max(lo, lo_p + toc["offset"]), min(hi, hi_p + toc["offset"])
        print(f"===== 해리슨 21판 {n}장 {c['title']} — 인쇄쪽 {lo - toc['offset']}~{hi - toc['offset']}"
              f" (PDF {lo}~{hi}) · {c.get('section') or ''}")
        for i in range(lo, hi + 1):
            text = doc[i].get_text()
            printed = i - toc["offset"]
            if a.grep:
                hits = [ln.strip() for ln in text.splitlines() if a.grep.lower() in ln.lower()]
                for h in hits:
                    print(f"  p.{printed}  {h}")
                    total += len(h)
            else:
                chunk = text.strip()
                if total + len(chunk) > a.max_chars:
                    print(f"--- 여기까지({a.max_chars}자). 더 보려면 --pages {printed}- 로 이어 읽는다")
                    return 0
                print(f"\n--- p.{printed}\n{chunk}")
                total += len(chunk)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
