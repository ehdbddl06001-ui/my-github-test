"""outline.py — 과별 학습서의 「기본틀」(단원이 꽂히는 순서)을 읽고 검사한다.

원본은 두 파일이다.
  content/outline/subjects.yaml      과 → 슬롯 순서(사람이 정한 배치). 해리슨 장 번호를 가리킨다.
  content/outline/harrison_toc.json  해리슨 21판 목차(기계로 한 번 뽑은 것 — `harrison_toc.py`).

이 모듈이 하는 일은 **순서를 주는 것**뿐이다. 정리본의 내용은 건드리지 않는다.
정리본은 frontmatter `outline: <슬롯 id>` 로 자기 자리를 밝힌다. 비우면 책 맨 뒤 「배치 대기」로 간다.

사용:
  python pipelines/outline.py                      # 틀 전체 검사(빠진 장·중복·책 이름)
  python pipelines/outline.py --book 순환기내과    # 그 과의 순서와 「작성됨/대기」
  python pipelines/outline.py --gaps [--book …]    # 아직 정리본이 없는 슬롯(커리큘럼 빈칸)
  python pipelines/outline.py --find "long QT"     # 슬롯·해리슨 장 제목에서 찾기(PDF 를 열지 않는다)
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
SUBJECTS = ROOT / "content" / "outline" / "subjects.yaml"
TOC = ROOT / "content" / "outline" / "harrison_toc.json"
BOOKS_CFG = ROOT / "pipelines" / "books_config.yaml"
ID_RE = re.compile(r"^[a-z0-9]+(?:[.-][a-z0-9]+)*$")


@dataclass
class Slot:
    id: str
    title: str
    book: str
    order: int
    chapters: list[int] = field(default_factory=list)
    part: str = ""                      # 해리슨 부·절 이름(책의 중간 머리글로 쓴다)

    @property
    def source(self) -> str:
        if not self.chapters:
            return ""
        ns = self.chapters
        return f"해리슨 21판 {ns[0]}장" if len(ns) == 1 else f"해리슨 21판 {ns[0]}~{ns[-1]}장"


def parse_range(spec) -> list[int]:
    """"236-283" · "392" · [392, 393] → [정수…]"""
    if isinstance(spec, int):
        return [spec]
    if isinstance(spec, list):
        out: list[int] = []
        for s in spec:
            out += parse_range(s)
        return out
    out = []
    for piece in str(spec).split(","):
        piece = piece.strip()
        if not piece:
            continue
        if "-" in piece:
            a, b = piece.split("-", 1)
            out += list(range(int(a), int(b) + 1))
        else:
            out.append(int(piece))
    return out


def load_toc() -> dict[int, dict]:
    data = json.loads(TOC.read_text(encoding="utf-8"))
    return {c["n"]: c for c in data["chapters"]}


def load() -> tuple[dict[str, list[Slot]], list[str]]:
    """{책: [슬롯…]} 과 오류 목록. 오류가 있어도 만들 수 있는 만큼은 만든다(학습서를 멈추지 않는다)."""
    errs: list[str] = []
    if not SUBJECTS.exists() or not TOC.exists():
        return {}, [f"기본틀 파일이 없다: {SUBJECTS.name} · {TOC.name}"]
    cfg = yaml.safe_load(SUBJECTS.read_text(encoding="utf-8")) or {}
    toc = load_toc()
    books_cfg = yaml.safe_load(BOOKS_CFG.read_text(encoding="utf-8")) or {}
    known_books = set((books_cfg.get("books") or {}).values())

    out: dict[str, list[Slot]] = {}
    seen_ids: dict[str, str] = {}
    used_ch: dict[int, str] = {}
    for sub in cfg.get("subjects") or []:
        book = str(sub.get("book", "")).strip()
        if not book:
            errs.append("book 이름이 없는 과가 있다")
            continue
        if known_books and book not in known_books:
            errs.append(f"{book}: books_config.yaml 의 책 이름에 없다(과목 매핑을 먼저 넣는다)")
        slots: list[Slot] = []
        for item in sub.get("outline") or []:
            chapters = parse_range(item.get("chapters")) if item.get("chapters") else []
            for n in chapters:
                if n not in toc:
                    errs.append(f"{book}: 해리슨 {n}장이 목차에 없다")
                elif n in used_ch and used_ch[n] != book:
                    errs.append(f"해리슨 {n}장이 두 책에 있다({used_ch[n]} · {book})")
                else:
                    used_ch[n] = book
            if item.get("id"):                                  # 손으로 적은 슬롯 하나
                sid = str(item["id"])
                title = str(item.get("title") or "").strip()
                if not title:
                    errs.append(f"{book}: 슬롯 {sid} 에 title 이 없다")
                # 손으로 적은 슬롯은 해리슨 절에 속하지 않는다 — 차례 머리글 없이 그 자리에 놓인다
                slots.append(Slot(sid, title, book, len(slots), chapters))
            else:                                               # 장마다 슬롯 하나
                for n in chapters:
                    c = toc.get(n)
                    if not c:
                        continue
                    slots.append(Slot(f"h{n}", c["title"], book, len(slots), [n], c.get("section") or ""))
        for s in slots:
            if not ID_RE.match(s.id):
                errs.append(f"{book}: 슬롯 id {s.id!r} 는 소문자·숫자·점·하이픈만")
            if s.id in seen_ids:
                errs.append(f"슬롯 id 가 겹친다: {s.id}({seen_ids[s.id]} · {book})")
            seen_ids[s.id] = book
        out[book] = slots
    missing = sorted(set(toc) - set(used_ch))
    if missing:
        errs.append(f"어느 과에도 넣지 않은 해리슨 장 {len(missing)}개: {missing[:12]}{'…' if len(missing) > 12 else ''}")
    return out, errs


def index(books: dict[str, list[Slot]]) -> dict[str, Slot]:
    return {s.id: s for slots in books.values() for s in slots}


def order_key(slot_id: str, idx: dict[str, Slot]) -> tuple[int, str]:
    """build_books 가 단원을 정렬할 때 쓴다. 배치되지 않은 단원은 맨 뒤로."""
    s = idx.get(slot_id or "")
    return (s.order, "") if s else (10**6, slot_id or "")


def written(concepts: dict) -> dict[str, list[str]]:
    """{슬롯 id: [정리본 id…]}"""
    out: dict[str, list[str]] = {}
    for cid, c in concepts.items():
        sid = str(c.get("outline") or "")
        if sid:
            out.setdefault(sid, []).append(cid)
    return out


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--book")
    ap.add_argument("--gaps", action="store_true", help="정리본이 없는 슬롯만")
    ap.add_argument("--find", help="슬롯·해리슨 장 제목 검색")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)

    books, errs = load()
    for e in errs:
        print("  ✗", e)
    try:
        sys.path.insert(0, str(ROOT / "pipelines"))
        from concepts import load_concepts
        concepts, _ = load_concepts()
    except Exception:                                            # 정리본을 못 읽어도 틀은 볼 수 있다
        concepts = {}
    done = written(concepts)

    if a.find:
        q = a.find.lower()
        for book, slots in books.items():
            for s in slots:
                if q in s.title.lower() or q in s.id.lower():
                    print(f"  {book:10} {s.id:10} {s.title[:60]:62} {s.source}")
        return 0

    picked = {a.book: books[a.book]} if a.book and a.book in books else books
    if a.book and a.book not in books:
        print(f"그런 책이 없다: {a.book} — {', '.join(books)}")
        return 1
    if a.json:
        print(json.dumps({b: [{"id": s.id, "title": s.title, "chapters": s.chapters,
                               "concepts": done.get(s.id, [])} for s in sl] for b, sl in picked.items()},
                         ensure_ascii=False, indent=1))
        return 0

    for book, slots in picked.items():
        n_done = sum(1 for s in slots if done.get(s.id))
        print(f"\n■ {book} — 슬롯 {len(slots)}개 · 정리본 있는 슬롯 {n_done}개")
        if not a.book and not a.gaps:
            continue
        head = ""
        for s in slots:
            cs = done.get(s.id, [])
            if a.gaps and cs:
                continue
            if s.part and s.part != head:
                head = s.part
                print(f"   — {head}")
            mark = "✓" if cs else "·"
            print(f"   {mark} {s.id:10} {s.title[:56]:58} {s.source}{'  ' + ', '.join(cs) if cs else ''}")
    unplaced = [cid for cid, c in concepts.items() if not c.get("outline")]
    if unplaced:
        print(f"\n배치 대기(정리본에 outline 이 없다) {len(unplaced)}개: {', '.join(unplaced[:6])}")
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
