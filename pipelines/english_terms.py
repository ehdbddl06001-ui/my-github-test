"""학습서 조판용 「english(한글)」 표기(2026-09-27 사용자: 「약제나 영어이름은 영어(한글) 순서로」).

① 약·약군: content/glossary/verified.json(약 = RxNorm, 약군 = MeSH 로 확인)에 있는 것만.
   단원에서 처음 나오면 english(한글), 그 뒤는 english. 괄호 안에서는 괄호를 겹치지 않고 「english 한글」.
② 원고에 이미 「한글(English)」로 쓴 용어(한글 4음절 이상 한 낱말, 끝이 조사·어미가 아닌 것) → 「English(한글)」 순서만 바꾼다.
   앞 낱말까지 한 용어일 수 있는 경우(「세균성 혈관종증(…)」)는 그대로 둔다.
새 영어 이름을 지어내지 않는다 — 원고에 없던 영어는 ①의 확인된 약 이름뿐. 원고 파일은 바꾸지 않는다(조판 때만).
"""
from __future__ import annotations

import copy
import dataclasses
import hashlib
import json
import re
from pathlib import Path

VERIFIED = Path(__file__).resolve().parent.parent / "content" / "glossary" / "verified.json"
_ENDING = tuple("다면고며서게지니요라해던은는을를이가의에로와과도만")
SKIP = {"id", "type", "topic", "see_also", "date", "updated", "version", "outline", "confidence", "review_status", "exams",
        "sources", "path", "hash", "errors", "geo", "figures", "figures_wanted", "figures_rejected", "figures_none", "kind",
        "from", "to", "anchor", "key", "file", "url", "doi", "basis", "objective_kind", "source", "locator"}
ORDER = ["title", "objective", "condition", "summary", "sections", "criteria", "tables", "diagram", "diagram_notes",
         "pitfalls", "checks", "variants"]
_PAIR_RE = re.compile(r"(?<![가-힣])([가-힣]{4,})\(([A-Za-z][A-Za-z0-9 '\-]{1,40})\)")


def load_terms(path: Path = VERIFIED) -> dict[str, str]:
    if not path.exists():
        return {}
    g = json.loads(path.read_text(encoding="utf-8"))
    return {ko: v["en"] for ko, v in {**g.get("drugs", {}), **g.get("classes", {})}.items()}


TERM = load_terms()


def digest() -> str:
    """책 해시에 넣는다 — 약 이름 표가 바뀌면 책을 다시 만든다."""
    return hashlib.sha256(json.dumps(TERM, ensure_ascii=False, sort_keys=True).encode()).hexdigest()[:12]


def _term_re(terms: dict[str, str]) -> re.Pattern | None:
    if not terms:
        return None
    alt = "|".join(sorted(map(re.escape, terms), key=len, reverse=True))
    return re.compile(r"(?<![가-힣])(" + alt + r")(\(([^()]*)\))?")


_TERM_RE = _term_re(TERM)


def text(s: str, seen: set, terms: dict[str, str] | None = None) -> str:
    terms = TERM if terms is None else terms
    rx = _TERM_RE if terms is TERM else _term_re(terms)

    def pair(m: re.Match) -> str:
        ko, en = m.group(1), m.group(2)
        if ko.endswith(_ENDING) or ko in terms:
            return m.group(0)
        pre = s[:m.start()]
        if pre.endswith(" ") and re.search(r"[가-힣]$", pre.rstrip()) and not pre.rstrip().endswith(_ENDING):
            return m.group(0)
        return f"{en}({ko})"
    s = _PAIR_RE.sub(pair, s)
    if rx is None:
        return s

    def render(ko: str, inside: bool) -> str:
        en = terms[ko]
        if en in seen:
            return en
        seen.add(en)
        return f"{en} {ko}" if inside else f"{en}({ko})"

    def term(m: re.Match) -> str:
        ko, paren, inner = m.group(1), m.group(2), m.group(3)
        en = terms[ko]
        before = s[:m.start()]
        inside = before.count("(") > before.count(")")
        if paren and en.lower() in (inner or "").lower():       # 원고가 이미 같은 영어를 괄호로 달았다
            return render(ko, inside)
        if paren:                                                 # 「칼슘통로차단제(딜티아젬·베라파밀)」
            inner2 = rx.sub(lambda mm: render(mm.group(1), True) + (mm.group(2) or ""), inner)
            if en in seen:
                return f"{en}({inner2})"
            seen.add(en)
            return f"{en}({ko}; {inner2})"
        return render(ko, inside)
    return rx.sub(term, s)


def _walk(x, seen: set, key: str | None = None):
    if key in SKIP:
        return x
    if isinstance(x, str):
        return text(x, seen)
    if isinstance(x, list):
        return [_walk(v, seen) for v in x]
    if isinstance(x, dict):
        return {k: _walk(v, seen, k) for k, v in x.items()}
    return x


def concept(c: dict) -> dict:
    """정리본 한 개(단원)를 조판용으로 — 복사본을 돌려준다. 단원마다 「처음 나옴」을 따로 센다."""
    c, seen = copy.deepcopy(c), set()
    for k in ORDER + [k for k in c if k not in ORDER]:
        if k in c:
            c[k] = _walk(c[k], seen, k)
    return c


def unit(u):
    """build_books.Unit → 제목·정리본을 english(한글)로 바꾼 복사본."""
    if not u.concept:
        return u
    c = concept(u.concept)
    title = c.get("title") if u.title == u.concept.get("title") else text(u.title, set())
    return dataclasses.replace(u, concept=c, title=title)
