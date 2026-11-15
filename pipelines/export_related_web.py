"""export_related_web.py — 개념 정리본 ↔ 스크랩한 논문을 잇는 표를 만든다(결정론, 2026-11-15).

왜: 논문 피드(papers.html)와 정리본(학습서)이 따로 놀아서, 정리본을 읽다가 「이 질환으로 스크랩해 둔 논문」을 볼 길이 없었다.

잇는 규칙(보수적으로 — 틀린 연결은 없는 것보다 나쁘다):
  · 정리본의 영어 용어 = ① id 의 둘째 마디(`cn.cardio.atrial-fibrillation.…` → "atrial fibrillation")
                        ② `condition` 의 괄호 안 영어(`심방세동(atrial fibrillation, AF)` → "atrial fibrillation", 약어는 대문자 3자 이상만)
  · 논문 **제목**에 용어가 낱말 경계로 들어 있으면 연결(강함 `t`). 제목엔 없고 **초록**에 2번 이상(한 낱말 용어는 3번 이상) 나오면 연결(약함 `a`).
  · 약어(ARDS · CMR …)는 뜻이 여럿이라(AMR = 항체매개 거부 / 항균제 내성) 제목에서만, 그 정리본의 긴 용어가 논문 어딘가에 나올 때만 센다.
  · 제목 끝의 발행 기관 이름은 뺀다(「… a statement from the Committee on Rheumatic Fever, Endocarditis, and Kawasaki Disease」).
  · 너무 흔한 낱말 하나짜리 용어(GENERIC)는 쓰지 않는다. 정리본마다 최대 8편(제목 일치 먼저 · 최신순), 논문마다 정리본 최대 5개.
  · 의미 판단은 하지 않는다 — 글자가 겹친다는 사실만 적는다. 화면에도 「제목에 용어」/「초록에 용어」로 근거를 보인다.

산출물: docs/related.js
  window.MEDKOS_RELATED = { generated, concepts: { cid: [ {id, how, term} ] }, papers: { pid: {t, j, d, c: [cid]} }, titles: { cid: 제목 } }
  papers 에는 연결된 논문만(제목 · 학술지 · 날짜) — 첫 화면이 papers.js(2.5 MB)를 통째로 읽지 않게.

사용: python pipelines/export_related_web.py     (publish.py 번들 단계가 정리본 · 논문 번들 뒤에 돌린다)
"""
from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path

from concepts import load_concepts
from export_papers_web import load_records

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "related.js"

MAX_PER_CONCEPT = 8
MAX_PER_PAPER = 5
# 이것 하나만으로는 그 정리본의 주제라고 할 수 없는 낱말(둘째 마디가 이 낱말 하나면 용어로 쓰지 않는다)
GENERIC = {
    "disease", "syndrome", "infection", "cancer", "tumor", "tumour", "pain", "fever", "shock", "injury", "trauma", "bleeding",
    "screening", "diagnosis", "treatment", "therapy", "management", "evaluation", "anatomy", "physiology", "mechanism",
    "epidemiology", "classification", "ecg", "imaging", "pregnancy", "surgery", "children", "elderly", "drug", "drugs",
    "edema", "anemia", "sepsis", "stroke", "obesity", "hypertension", "diabetes", "pneumonia",
}
# 제목에서 이 뒤는 발행 기관 · 문서 종류다 — 주제가 아니다
TITLE_TAIL = re.compile(r"[:.]?\s*\b(?:an? (?:scientific |policy |clinical )?(?:statement|report|guideline|consensus)\b[^.]*? (?:for|from|of|by) |from the (?:American|European|Committee|Council|Society)\b|developed in collaboration with\b).*$", re.I | re.S)
STOP_TAIL = {"of", "and", "the", "in", "for", "with", "to", "vs", "versus", "or", "a", "an"}


def _clean(term: str) -> str:
    return re.sub(r"\s+", " ", term.replace("-", " ")).strip().lower()


def concept_terms(cid: str, c: dict) -> list[str]:
    """정리본 하나의 영어 용어(소문자 구, 약어는 원래 대문자 그대로) — 긴 것부터."""
    out: list[str] = []

    def add(t: str) -> None:
        t = t.strip(" .·—-")
        if not t or t in out:
            return
        out.append(t)

    parts = cid.split(".")
    if len(parts) >= 3:
        slug = _clean(parts[2])
        words = slug.split()
        if words and not (len(words) == 1 and (words[0] in GENERIC or len(words[0]) < 4)):
            add(slug)
    for inner in re.findall(r"\(([^()]*)\)", str(c.get("condition", ""))):
        for piece in re.split(r"[,;·/]| vs ", inner):
            piece = piece.strip()
            if not piece or re.search(r"[가-힣]", piece):
                continue
            if re.fullmatch(r"[A-Z][A-Z0-9]{2,7}", piece):          # 약어 — 대문자 3자 이상만(AF · MR · AS 같은 두 글자는 뜻이 여럿)
                add(piece)
                continue
            words = _clean(piece).split()
            while words and words[-1] in STOP_TAIL:
                words.pop()
            if len(words) >= 2 or (len(words) == 1 and len(words[0]) >= 5 and words[0] not in GENERIC):
                add(" ".join(words))
    return sorted(out, key=lambda t: (-len(t), t))


def _pattern(term: str) -> re.Pattern:
    if term.isupper():                                             # 약어는 대소문자를 가린다
        return re.compile(r"(?<![A-Za-z0-9])" + re.escape(term) + r"(?![A-Za-z0-9])")
    words = [re.escape(w) for w in term.split()]
    body = r"[\s\-]+".join(words)
    return re.compile(r"(?<![a-z0-9])" + body + r"(?:s|es)?(?![a-z0-9])", re.I)


def match(terms: list[str], title: str, abstract: str) -> tuple[str, str] | None:
    """(how, term) — how: 't' = 제목에 용어 · 'a' = 초록에 여러 번. 없으면 None."""
    head = TITLE_TAIL.sub("", title) or title
    both = title + " " + abstract
    phrases = [t for t in terms if not t.isupper()]
    # 약어는 제목에서만, 그리고 그 정리본의 긴 용어가 글 어딘가에 한 번은 나올 때만(AMR = 항체매개 거부 / 항균제 내성)
    spelled = any(_pattern(t).search(both) for t in phrases if " " in t)
    for t in terms:
        if (not t.isupper() or spelled) and _pattern(t).search(head):
            return "t", t
    for t in phrases:
        need = 2 if " " in t else 3
        if len(_pattern(t).findall(abstract)) >= need:
            return "a", t
    return None


def build(concepts: dict | None = None, papers: list[dict] | None = None) -> dict:
    if concepts is None:
        concepts, _ = load_concepts()
    if papers is None:
        papers = load_records()
    terms = {cid: concept_terms(cid, c) for cid, c in concepts.items()}
    by_concept: dict[str, list[dict]] = {}
    by_paper: dict[str, list[str]] = {}
    meta: dict[str, dict] = {}
    for p in papers:
        title, abstract = str(p.get("title", "")), str(p.get("abstract", ""))
        hits = []
        for cid, ts in terms.items():
            if not ts:
                continue
            m = match(ts, title, abstract)
            if m:
                hits.append((0 if m[0] == "t" else 1, cid, m))
        hits.sort()
        for _, cid, (how, term) in hits[:MAX_PER_PAPER]:
            by_concept.setdefault(cid, []).append({"id": p["id"], "how": how, "term": term, "_d": str(p.get("pubdate") or p.get("date") or "")})
            by_paper.setdefault(p["id"], []).append(cid)
            meta[p["id"]] = {"t": title, "j": str(p.get("journal", "")), "d": str(p.get("pubdate") or p.get("date") or "")}
    out_c: dict[str, list[dict]] = {}
    for cid, rows in by_concept.items():
        rows = sorted(rows, key=lambda r: r["_d"], reverse=True)       # 최신순
        rows = sorted(rows, key=lambda r: r["how"] != "t")              # 제목 일치 먼저(안정 정렬)
        out_c[cid] = [{"id": r["id"], "how": r["how"], "term": r["term"]} for r in rows[:MAX_PER_CONCEPT]]
    kept = {r["id"] for rows in out_c.values() for r in rows}
    out_p = {}
    for pid in sorted(kept):
        cids = [cid for cid in by_paper[pid] if any(r["id"] == pid for r in out_c.get(cid, []))]
        out_p[pid] = dict(meta[pid], c=cids)
    titles = {cid: str(concepts[cid].get("title", "")) for cid in sorted(out_c)}      # 논문 화면의 「관련 정리본」 이름표
    return {"generated": date.today().isoformat(), "concepts": dict(sorted(out_c.items())), "papers": out_p, "titles": titles}


def main() -> int:
    data = build()
    OUT.write_text(
        "// 자동 생성 파일 — 수정하지 마세요.\n"
        "// 원본: content/concepts · content/papers  →  `python pipelines/export_related_web.py`로 재생성\n"
        "window.MEDKOS_RELATED = " + json.dumps(data, ensure_ascii=False, indent=1) + ";\n",
        encoding="utf-8", newline="\n")
    n = sum(len(v) for v in data["concepts"].values())
    print(f"생성: {OUT.relative_to(ROOT)} (정리본 {len(data['concepts'])}개 ↔ 논문 {len(data['papers'])}편, 연결 {n}건)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
