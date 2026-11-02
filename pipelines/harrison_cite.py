"""harrison_cite.py — 문항 해설·영상 문항 refs 의 해리슨 인용을 **22판**으로 쓰고 검사한다.

2026-11-02 사용자 지시: 매일 KMLE·USMLE·영상 문항이 아직 「Harrison's … 21e」를 적고 있었다(규칙이 판을 말하지 않아
모델 기억의 21판이 나왔다). 드라이브에 22판 장별 DB(`content/outline/harrison22.json` — `harrison22_build.py`)가 있으니
문항도 22판으로 인용한다. **장 번호는 판마다 다르다**(21판 301장 ARDS → 22판 301장은 Bronchiectasis) — 기억으로 쓰지 말고
여기서 찾는다.

  python pipelines/harrison_cite.py --find "respiratory distress"   # 22판 장 번호·제목·인쇄쪽 + 붙여 쓸 인용
  python pipelines/harrison_cite.py --find ARDS                      # 약어는 제목 머리글자로도 찾는다
  python pipelines/harrison_cite.py --from21 301                     # 기억한 21판 장 → 22판 장
  python pipelines/harrison_cite.py --chapter 309                    # 그 장의 드라이브 문서 ID(원문을 읽을 때)
  python pipelines/harrison_cite.py --check <파일...>                # 인용 검사(은행 .py · 카드 .md 무엇이든)

인용 형식:
  MedKOS 해설 `**출처**` — `Harrison's Principles of Internal Medicine, 22e. <장>장 <제목>` (원문을 읽었으면 ` p.<쪽>`).
  영상 은행 refs(Vancouver) — `Loscalzo J, Fauci AS, Kasper DL, et al., eds. Harrison's Principles of Internal Medicine,
  22nd ed. McGraw Hill; 2025. Chapter <장>: <제목>`.
검사(`check_text`): 21판 인용 = ERROR(22판에 없는 21판 7·417·484장만 허용) · 22판 장 번호가 표에 없거나 제목이 그 장과
다름 = ERROR · 22판인데 장 번호 없음 / 판 표기 없음 = WARN. 쪽 번호는 읽지 않았으면 적지 않는다(검사기는 쪽을 판정하지 않는다).
"""
from __future__ import annotations

import argparse
import difflib
import json
import re
import sys
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
H22 = ROOT / "content" / "outline" / "harrison22.json"
TOC21 = ROOT / "content" / "outline" / "harrison_toc.json"

# 이 날짜(KST) 이후 문항은 22판으로 인용한다 — 그 전 문항의 21판 인용은 그대로 둔다
HARRISON22_FROM = "2026-11-03"

MEDKOS_FMT = "Harrison's Principles of Internal Medicine, 22e. {n}장 {title}"
REF_FMT = ("Loscalzo J, Fauci AS, Kasper DL, et al., eds. Harrison's Principles of Internal Medicine, 22nd ed. "
           "McGraw Hill; 2025. Chapter {n}: {title}")

MENTION = re.compile(r"Harrison(?:['’]s)?\b", re.I)
# 한 인용의 끝 — 줄바꿈 · MedKOS 출처 구분자 「 / 」 · 따옴표 · 다음 Harrison
SEG_END = re.compile(r"\n|\s/\s|\"|(?=Harrison)", re.I)
ED21 = re.compile(r"\b21(?:e\b|st\b|\s*판)|twenty-first", re.I)
ED22 = re.compile(r"\b22(?:e\b|nd\b|\s*판)|twenty-second", re.I)
CHAP = re.compile(r"(?:\bchapter|\bch\.?|\bchap\.?)\s*(\d{1,3})\b|(\d{1,3})\s*장", re.I)
# 장 번호 뒤 제목 — 「Chapter 309: Title」·「309장 Title」 (쪽 표기·괄호·마침표 앞까지)
TITLE_AFTER = re.compile(r"^\s*[:.\-–—]?\s*['‘\"]?(?!p\.\s*\d)([A-Za-z][^()\[\]\"'’]*?)\s*(?:['’\"]|\(|\)|\s[—–]\s|\.\s|\bp\.\s*\d|,\s*p|$)")
GONE_21 = {7, 417, 484}                                   # 22판에 없는 21판 장(harrison22_build.OVERRIDES)


@lru_cache(maxsize=1)
def table() -> dict:
    """22판 표(없으면 빈 dict — 검사는 판 표기만 본다)."""
    if not H22.is_file():
        return {}
    return json.loads(H22.read_text(encoding="utf-8"))


@lru_cache(maxsize=1)
def toc21() -> dict[int, str]:
    if not TOC21.is_file():
        return {}
    data = json.loads(TOC21.read_text(encoding="utf-8"))
    return {int(c["n"]): c["title"] for c in data.get("chapters", [])}


def _norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", s.lower().replace("’", "'")).strip()


def _initials(title: str) -> str:
    stop = {"and", "of", "the", "in", "to", "with", "for", "a", "an", "its", "other", "on"}
    return "".join(w[0] for w in _norm(title).split() if w not in stop)


def title_matches(cited: str, real: str) -> bool:
    a, b = _norm(cited), _norm(real)
    if not a or not b:
        return True
    if a in b or b in a:
        return True
    return difflib.SequenceMatcher(None, a, b).ratio() >= 0.75


def find(query: str, limit: int = 12) -> list[tuple[int, dict]]:
    """제목·부·절에서 찾는다(단어 AND). 대문자 약어(ARDS)는 제목 머리글자로도."""
    chs = table().get("chapters", {})
    words = _norm(query).split()
    acro = query.strip().lower() if re.fullmatch(r"[A-Z]{2,6}", query.strip()) else ""
    out = []
    for k, c in chs.items():
        hay = _norm(" ".join(str(c.get(f, "")) for f in ("title", "part", "section")))
        if (words and all(w in hay for w in words)) or (acro and acro in _initials(c.get("title", ""))):
            out.append((int(k), c))
    out.sort(key=lambda kc: (not all(w in _norm(kc[1]["title"]) for w in words), kc[0]))
    return out[:limit]


def by_title(title: str) -> list[int]:
    chs = table().get("chapters", {})
    if len(_norm(title)) < 6:
        return []
    exact = [int(k) for k, c in chs.items() if _norm(title) in _norm(c.get("title", ""))]
    return exact or [int(k) for k, c in chs.items() if title_matches(title, c.get("title", ""))]


def suggest21(n21: int | None, title: str | None) -> str:
    """21판 인용을 22판으로 바꿀 때 쓸 장."""
    h = table()
    cands: list[int] = []
    if n21 is not None:
        cands = [int(x) for x in h.get("from21", {}).get(str(n21), [])]
    if not cands and title:
        cands = by_title(title)
    chs = h.get("chapters", {})
    if not cands:
        return "`harrison_cite.py --find <주제>` 로 22판 장을 찾는다"
    return " · ".join(MEDKOS_FMT.format(n=j, title=chs[str(j)]["title"]) for j in cands if str(j) in chs)


def _segments(text: str):
    for m in MENTION.finditer(text):
        rest = text[m.end():m.end() + 220]
        end = SEG_END.search(rest)
        yield m.group(0) + (rest[:end.start()] if end else rest)


def _chapter_and_title(seg: str) -> tuple[int | None, str | None]:
    cm = CHAP.search(seg)
    if cm:
        n = int(cm.group(1) or cm.group(2))
        tm = TITLE_AFTER.match(seg[cm.end():])
        title = tm.group(1).strip() if tm and len(tm.group(1).strip()) >= 4 else None
        return n, title
    # 「21e(Hyperthyroidism — Graves' Ophthalmopathy)」·「ch. 'The vasculitis syndromes'」 꼴 — 번호 없이 제목만
    pm = re.search(r"(?:\(|ch\.?\s*['‘])([A-Za-z][^()'’]{3,})", seg)
    return None, (pm.group(1).split(" — ")[0].strip() if pm else None)


def check_text(text: str) -> list[tuple[str, str, str]]:
    """(level, code, msg) 목록. 인용마다 판·장 번호·제목을 본다."""
    out: list[tuple[str, str, str]] = []
    chs = table().get("chapters", {})
    seen: set[str] = set()
    for seg in _segments(text):
        key = _norm(seg)
        if key in seen:
            continue
        seen.add(key)
        short = seg.strip()[:110]
        n, title = _chapter_and_title(seg)
        if ED21.search(seg):
            if (n in GONE_21) or (title and any(title_matches(title, toc21().get(g, "~")) for g in GONE_21)):
                continue                                   # 22판에 없는 장 — 21판 인용이 맞다
            out.append(("ERROR", "harrison-21e",
                        f"해리슨 21판 인용 「{short}」 — 22판으로 바꾼다: {suggest21(n, title)}"))
            continue
        if not ED22.search(seg):
            out.append(("WARN", "harrison-edition",
                        f"해리슨 인용에 판이 없다 「{short}」 — 22판 장을 찾아 `{MEDKOS_FMT.format(n='<장>', title='<제목>')}` 로"))
            continue
        if not chs:
            continue                                       # 표가 없으면 판만 본다
        if n is None:
            hint = by_title(title) if title else []
            out.append(("WARN", "harrison-no-chapter",
                        f"22판 인용에 장 번호가 없다 「{short}」"
                        + (f" — 제목으로 보면 {', '.join(map(str, hint))}장" if hint else " — `harrison_cite.py --find` 로 장 번호를 붙인다")))
            continue
        real = chs.get(str(n))
        if real is None:
            out.append(("ERROR", "harrison-chapter",
                        f"22판에 {n}장이 없다 「{short}」 — `harrison_cite.py --find` 로 찾는다"))
        elif title and not title_matches(title, real["title"]):
            hint = by_title(title)
            out.append(("ERROR", "harrison-chapter",
                        f"22판 {n}장은 「{real['title']}」 — 인용한 제목 「{title}」과 다르다(21판 번호를 쓴 듯)"
                        + (f". 그 제목의 22판 장: {', '.join(map(str, hint))}장" if hint else "")))
    return out


def _print_chapter(n: int, c: dict) -> None:
    print(f"  {n:>3}장  {c['title']}  · 인쇄쪽 {c.get('page')}~{c.get('page_end')}  · {c.get('part', '')}")
    print(f"        해설  {MEDKOS_FMT.format(n=n, title=c['title'])}")
    print(f"        refs  {REF_FMT.format(n=n, title=c['title'])}")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--find", nargs="+", metavar="QUERY", help="22판 장 제목·부·절 검색(여러 개면 각각)")
    ap.add_argument("--from21", type=int, metavar="N", help="21판 장 번호 → 22판 장")
    ap.add_argument("--chapter", type=int, metavar="N", help="22판 장 정보와 드라이브 문서 ID")
    ap.add_argument("--check", nargs="+", metavar="FILE", help="파일의 해리슨 인용 검사(ERROR 면 exit 1)")
    a = ap.parse_args(argv)
    h = table()
    if not h:
        print(f"{H22.relative_to(ROOT)} 가 없다 — `python pipelines/harrison22_build.py` 로 만든다")
        return 1
    chs = h["chapters"]
    if a.find:
        for q in a.find:
            hits = find(q)
            print(f"「{q}」 — {len(hits)}장" + ("" if hits else " (다른 말·영어 제목으로 다시 찾는다)"))
            for n, c in hits:
                _print_chapter(n, c)
    if a.from21 is not None:
        t21 = toc21().get(a.from21, "?")
        js = h.get("from21", {}).get(str(a.from21))
        print(f"21판 {a.from21}장 {t21} → " + ("22판에 없음(21판으로 인용)" if js == [] else "22판"))
        for j in js or []:
            _print_chapter(int(j), chs[str(j)])
    if a.chapter is not None:
        c = chs.get(str(a.chapter))
        if not c:
            print(f"22판에 {a.chapter}장이 없다")
            return 1
        _print_chapter(a.chapter, c)
        print(f"        문서  {c.get('doc')} (드라이브 {h.get('folder')}/H22_{a.chapter:03d} — Google Drive 커넥터로 그 장만 읽는다)")
    if a.check:
        n_err = 0
        for f in a.check:
            fs = check_text(Path(f).read_text(encoding="utf-8"))
            for level, code, msg in fs:
                n_err += level == "ERROR"
                print(f"{f}: [{level}] {code}: {msg}")
        print(f"해리슨 인용 검사: 파일 {len(a.check)}개 · ERROR {n_err}")
        return 1 if n_err else 0
    if not (a.find or a.from21 is not None or a.chapter is not None):
        ap.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
