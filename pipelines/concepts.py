"""concepts.py — 개념 정리본(`type: concept`)의 계약·적재·문항 연결(결정론).

2026-09-18 사용자 지시(오답 뒤 학습 흐름 · 과별 PDF 학습서):
- 개념 ID 는 **학습 목표** 단위다. 질환명으로 합치지 않는다 — 같은 질환이라도 평가 목표가 다르면
  다른 정리본이다(`cn.<과>.<주제>.<목표>`). 같은 원리를 반복해 틀린 문항들은 문항의 `objective` 로
  한 정리본에 모이고, 문항마다의 혼동(`distractors`)은 문항에 남는다.
- 정리본은 **미리 만들어 검토하는 콘텐츠**다. 앱·PDF 가 실시간으로 생성하지 않는다(브라우저에 API 키 없음).
- 내용 상태(이 파일 — 목표·출처·확인일·버전·검토 상태)와 학습자 상태(`learning_log.py`)를 섞지 않는다.
- 다른 모델이 동의했다고 검토 완료가 아니다 — `review_status: reviewed` 는 사람의 `reviewed_by`·`review_note` 로만.
- 확인하지 않은 기준·없는 출처를 만들지 않는다 — 출처마다 `checked_at`·`checked`(무엇을 대조했는가)를 남긴다.

웹(export_concepts_web.py)과 PDF(build_books.py)가 **같은 적재 결과**를 쓴다.
"""
from __future__ import annotations

import hashlib
import html
import re
from functools import lru_cache
from html.parser import HTMLParser
from pathlib import Path
from typing import Any

import decision_diagram as dd
from frontmatter import load, QUESTION_TYPES
from question_design import TARGETS

ROOT = Path(__file__).resolve().parent.parent
CONCEPT_DIR = ROOT / "content" / "concepts"
QUESTION_DIRS = [ROOT / "content" / d for d in ("kmle", "usmle", "imaging")]

ID_RE = re.compile(r"^cn\.[a-z0-9-]+\.[a-z0-9-]+\.[a-z0-9-]+$")
BASIS = {"current": "현행 권고", "past_exam": "기출 근거"}
EXAMS = ("kmle", "usmle")
SOURCE_KINDS = ("guideline", "consensus", "review", "textbook", "trial", "other")
# 출처를 어디까지 대조했는가 — text(권고·서술 본문과 대조) · abstract(초록만) · citation(서지만).
# text 가 아닌 출처를 근거로 든 곳에는 † 가 붙는다(검증된 현행 권고처럼 보이지 않게).
VERIFIED = ("text", "abstract", "citation")
TABLE_ROLES = ("differential", "treatment", "criteria", "severity", "tests", "monitoring", "comparison")
# 본문·표·혼동 항목 안의 근거 표시: [[출처id]] · [[출처id: 쪽·절·표]] · [[?출처id: …]](? = 이 주장은 원문 미대조)
CITE_RE = re.compile(r"\[\[(\?)?([a-z0-9][a-z0-9-]*)(?::\s*([^\]]+?))?\s*\]\]")
LETTERS = "ABCDE"
# 이 날짜 이후에 만든 KMLE·USMLE 문항은 학습 목표를 붙인다 — 오답이 이론 정리본으로 이어지게(2026-09-20 사용자 지시).
# 없다고 게시를 막지는 않는다(WARN) — 옛 문항 1,200여 개를 소급해서 막으면 매일 루틴이 멈춘다.
OBJECTIVE_REQUIRED_FROM = "2026-09-21"
MODEL_NAMES = re.compile(r"(claude|gpt|gemini|llama|model|모델|\bai\b)", re.IGNORECASE)
# 기초 뿌리(2026-11-21 사용자 결정) — 임상 정리본(판단)은 `roots` 로 기초 정리본(기전)을 가리킨다.
# 기초 정리본은 **기전 단위**라 임상 정리본 여러 개가 하나를 함께 가리킨다(문항마다 하나씩 만들지 않는다).
LAYERS = ("clinical", "basic")
SYSTEMS = ("cardiovascular", "respiratory", "renal", "gastrointestinal", "hepatobiliary", "endocrine-metabolic",
           "reproductive", "hematologic", "immune", "nervous", "musculoskeletal", "skin", "special-senses",
           "multisystem", "cell-molecular")
# 전공 교과서 대조 상태 — checked(본문과 대조) · pending(교과서는 있으나 아직 못 읽음) · unavailable(그 학문 교과서가 없음)
TEXTBOOK_CHECK = ("checked", "pending", "unavailable")


# ── 안전한 Markdown → HTML(허용 태그만, 속성 없음) ─────────────────────
SAFE_TAGS = {"p", "ul", "ol", "li", "strong", "em", "b", "i", "code", "h3", "h4", "table", "thead",
             "tbody", "tr", "th", "td", "br", "blockquote", "sub", "sup"}
DROP_WITH_CONTENT = {"script", "style", "iframe", "object", "embed", "svg", "math", "template", "noscript"}


class _Sanitizer(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.out: list[str] = []
        self.skip = 0

    def handle_starttag(self, tag, attrs):
        if tag in DROP_WITH_CONTENT:
            self.skip += 1
        elif not self.skip and tag in SAFE_TAGS:
            self.out.append("<br>" if tag == "br" else f"<{tag}>")

    def handle_startendtag(self, tag, attrs):
        if not self.skip and tag == "br":
            self.out.append("<br>")

    def handle_endtag(self, tag):
        if tag in DROP_WITH_CONTENT:
            self.skip = max(0, self.skip - 1)
        elif not self.skip and tag in SAFE_TAGS and tag != "br":
            self.out.append(f"</{tag}>")

    def handle_data(self, data):
        if not self.skip:
            self.out.append(html.escape(data, quote=False))


def sanitize(fragment: str) -> str:
    s = _Sanitizer()
    s.feed(fragment)
    s.close()
    return "".join(s.out)


def _normalize_lists(md: str) -> str:
    """문단 바로 아래에 붙은 목록 줄 앞에 빈 줄을 넣는다(Python-Markdown 은 빈 줄이 없으면 목록으로 읽지 않는다)."""
    out: list[str] = []
    item = re.compile(r"^\s*([-*+]|\d+\.)\s+")
    for ln in md.replace("\r\n", "\n").split("\n"):
        if item.match(ln) and out and out[-1].strip() and not item.match(out[-1]) and not out[-1].startswith((" ", "\t")):
            out.append("")
        out.append(ln)
    return "\n".join(out)


def md_to_html(md: str) -> str:
    import markdown  # 표준 파이썬 markdown — 결과는 반드시 sanitize 를 거친다
    return sanitize(markdown.markdown(_normalize_lists(md), extensions=["tables"], output_format="html"))


def split_sections(body: str) -> list[tuple[str, str]]:
    """본문을 `## 제목` 단위의 (제목, Markdown) 으로 나눈다 — 첫 `##` 앞의 글은 버린다."""
    out: list[tuple[str, str]] = []
    cur_title, buf = None, []
    for ln in body.replace("\r\n", "\n").split("\n"):
        m = re.match(r"^##\s+(.+?)\s*$", ln)
        if m:
            if cur_title is not None:
                out.append((cur_title, "\n".join(buf)))
            cur_title, buf = m.group(1), []
        elif cur_title is not None:
            buf.append(ln)
    if cur_title is not None:
        out.append((cur_title, "\n".join(buf)))
    return out


def sections(body: str) -> list[dict]:
    """`## 제목` 단위로 나눈다. 「(심화)」로 시작하는 절은 웹에서 접힌다(PDF 는 모두 편다)."""
    out = split_sections(body)
    res = []
    for title, md in out:
        deep = title.startswith("(심화)")
        res.append(dict(title=title.replace("(심화)", "").strip(), deep=deep, html=md_to_html(md.strip())))
    return res


def safe_url(u: Any) -> str:
    u = str(u or "").strip()
    return u if re.match(r"^https://[^\s\"'<>]+$", u) else ""


# ── 계약 검사 ───────────────────────────────────────────────────────
@lru_cache(maxsize=1)
def _outline_index() -> dict:
    """기본틀 슬롯 {id: Slot}. 파일이 없거나 깨져도 정리본 검사를 멈추지 않는다."""
    try:
        import outline as _ol
        return _ol.index(_ol.load()[0])
    except Exception:
        return {}


@lru_cache(maxsize=1)
def _book_map() -> dict:
    try:
        import yaml
        cfg = yaml.safe_load((ROOT / "pipelines" / "books_config.yaml").read_text(encoding="utf-8")) or {}
        return dict(cfg.get("books") or {})
    except Exception:
        return {}


@lru_cache(maxsize=1)
def _books_cfg() -> dict:
    try:
        import yaml
        return yaml.safe_load((ROOT / "pipelines" / "books_config.yaml").read_text(encoding="utf-8")) or {}
    except Exception:
        return {}


def discipline_books() -> dict:
    """{학문 꼬리표: 학문별 책 이름} — books_config.yaml `disciplines`."""
    return dict(_books_cfg().get("disciplines") or {})


def textbooks() -> dict:
    """{학문: {id, title, readable…}} — books_config.yaml `textbooks`."""
    return dict(_books_cfg().get("textbooks") or {})


def is_basic(meta: dict[str, Any]) -> bool:
    return meta.get("layer") == "basic"


def root_errors(meta: dict[str, Any]) -> list[str]:
    """기초 뿌리 필드 — layer · discipline · system · textbook_check(기초 정리본) / roots · roots_none(임상 정리본)."""
    errs: list[str] = []
    cid = str(meta.get("id", ""))
    layer = meta.get("layer", "clinical")
    if layer not in LAYERS:
        errs.append(f"layer 는 {'/'.join(LAYERS)}(없으면 clinical)")
    dmap = discipline_books()
    disc = meta.get("discipline")
    if disc is not None and dmap and disc not in dmap:
        errs.append(f"discipline '{disc}' 는 {'/'.join(dmap)} 중 하나(books_config.yaml disciplines)")
    roots, none = meta.get("roots"), meta.get("roots_none")
    if roots is not None:
        if not isinstance(roots, list) or not roots or not all(isinstance(r, str) and ID_RE.match(r) for r in roots):
            errs.append("roots 는 기초 정리본 id 목록(cn.<과>.<주제>.<목표>) — 뿌리가 없으면 roots_none 에 이유를 적는다")
        elif cid in roots:
            errs.append("roots 가 자기 자신을 가리킨다")
    if none is not None and not str(none).strip():
        errs.append("roots_none 은 기초 기전이 없는 이유 한 줄(검진 주기·법규·역학 계산·지침 수치 등)")
    if roots and none is not None:
        errs.append("roots 와 roots_none 을 함께 쓰지 않는다 — 뿌리가 있으면 roots, 없으면 roots_none")
    if layer == "basic":
        if not disc:
            errs.append("기초 정리본(layer: basic)은 discipline(학문)이 필요하다")
        elif dmap.get(disc) and _book_map().get(str(meta.get("topic") or "")) != dmap[disc]:
            errs.append(f"기초 정리본의 topic '{meta.get('topic')}' 이 학문별 책 「{dmap[disc]}」로 가지 않는다 — "
                        f"topic 을 그 학문 이름으로(books_config.yaml books)")
        if meta.get("system") not in SYSTEMS:
            errs.append(f"기초 정리본은 system(장기계통)이 필요하다 — {'/'.join(SYSTEMS)}")
        tb = meta.get("textbook_check")
        has_book = bool(disc and disc in textbooks())
        if tb not in TEXTBOOK_CHECK:
            errs.append(f"기초 정리본은 textbook_check 가 필요하다 — {'/'.join(TEXTBOOK_CHECK)}")
        elif tb == "checked" and not any(
                isinstance(s, dict) and s.get("kind") == "textbook" and s.get("verified") == "text"
                and not str(s.get("id", "")).startswith("harrison") for s in meta.get("sources") or []):
            errs.append("textbook_check: checked 인데 전공 교과서 출처(kind: textbook · verified: text, 해리슨 제외)가 없다")
        elif tb == "unavailable" and has_book:
            errs.append(f"[WARN] {disc} 는 교과서가 등록돼 있다(books_config.yaml textbooks) — textbook_check 는 pending 또는 checked")
        elif tb == "pending" and not has_book:
            errs.append(f"[WARN] {disc} 는 등록된 교과서가 없다 — textbook_check: unavailable")
        if roots is not None or none is not None:
            errs.append("기초 정리본에는 roots·roots_none 을 달지 않는다(뿌리는 임상 정리본이 가리킨다)")
    else:
        for k in ("system", "textbook_check"):
            if meta.get(k) is not None:
                errs.append(f"[WARN] {k} 는 기초 정리본(layer: basic)의 필드다")
    return errs


def root_link_errors(concepts: dict[str, dict]) -> dict[str, list[str]]:
    """{정리본 id: [오류…]} — roots 가 가리키는 정리본이 있고 기초 정리본인가(정리본 사이의 검사)."""
    out: dict[str, list[str]] = {}
    for cid, c in concepts.items():
        for r in c.get("roots") or []:
            t = concepts.get(str(r))
            if t is None:
                out.setdefault(cid, []).append(f"roots '{r}' 정리본이 없다 — 먼저 그 기초 정리본을 쓴다")
            elif not is_basic(t):
                out.setdefault(cid, []).append(f"roots '{r}' 는 기초 정리본(layer: basic)이 아니다")
    return out


def root_supports(concepts: dict[str, dict]) -> dict[str, list[str]]:
    """{기초 정리본 id: [그것을 뿌리로 삼는 임상 정리본 id…]} — roots 의 역방향(저장하지 않고 계산한다)."""
    out: dict[str, list[str]] = {}
    for cid, c in sorted(concepts.items()):
        for r in c.get("roots") or []:
            out.setdefault(str(r), []).append(cid)
    return out


def validate_concept(meta: dict[str, Any], path: Path | None = None) -> list[str]:
    errs: list[str] = []
    cid = str(meta.get("id", ""))
    if not ID_RE.match(cid):
        errs.append(f"concept id '{cid}' 형식 오류 — cn.<과>.<주제>.<학습목표> (소문자·숫자·하이픈)")
    if path is not None and path.stem != cid:
        errs.append(f"파일 이름({path.name})이 id 와 다르다 — <id>.md")
    for k in ("title", "objective", "condition"):
        if not str(meta.get(k, "") or "").strip():
            errs.append(f"concept 필수 필드 누락: {k}")
    if meta.get("objective_kind") not in TARGETS:
        errs.append(f"objective_kind 는 {'/'.join(TARGETS)} 중 하나")
    v = meta.get("version")
    if not isinstance(v, int) or v < 1:
        errs.append("version 은 1 이상의 정수(내용을 바꾸면 올린다)")
    slot = meta.get("outline")
    if slot is not None and not isinstance(slot, str):
        errs.append("outline 은 기본틀 슬롯 id(문자열)")
    elif not slot:
        errs.append("[WARN] outline(기본틀 슬롯)이 없다 — 책 맨 뒤 「배치 대기」로 간다. "
                    "`python pipelines/outline.py --book <과> --gaps` 로 자리를 고른다")
    else:
        idx = _outline_index()
        sl = idx.get(slot)
        if idx and not sl:
            errs.append(f"outline '{slot}' 가 기본틀에 없다 — `python pipelines/outline.py --find <말>` 로 찾는다")
        elif sl:
            want = _book_map().get(str(meta.get("topic") or ""))
            if want and sl.book != want:
                errs.append(f"[WARN] outline '{slot}' 는 {sl.book} 의 자리인데 이 정리본의 과는 {want} 다")
            # 해리슨 대조가 기본이다(2026-09-22 사용자 지시) — 그 장을 읽고 확인한 흔적이 없으면 알린다
            if sl.chapters and not any(str(x.get("id", "")).startswith("harrison") and x.get("verified") == "text"
                                       for x in meta.get("sources") or [] if isinstance(x, dict)):
                # 2026-10-31: 대조는 해리슨 22판 DB 로(22판에 없는 장만 21판) — harrison-21 로 이미 대조한 정리본도 유효하다
                where = (f"해리슨 22판 {', '.join(map(str, sl.chapters22))}장" if sl.chapters22
                         else f"해리슨 21판 {', '.join(map(str, sl.chapters))}장")
                ed = "22" if sl.chapters22 else "21"
                errs.append(f"[WARN] 해리슨 대조 없음 — 슬롯 {slot} = {where}. `outline.py --harrison {slot}` 로 "
                            f"그 장을 읽고 harrison-{ed} 출처(verified: text)와 [[harrison-{ed}: 장 p.N]] 을 단다")
    # 그림(2026-09-27) — 확실한 라벨만·출처·라이선스·파일. 규칙은 concept_figures.py
    from concept_figures import validate_figures
    errs += validate_figures(meta, [s["title"] for s in sections(str(meta.get("_body", "")))] if "_body" in meta else None)
    rs = meta.get("review_status")
    if rs not in ("unreviewed", "reviewed", "needs_revision"):
        errs.append("review_status 는 unreviewed/reviewed/needs_revision")
    if rs == "reviewed":
        who = str(meta.get("reviewed_by", "") or "")
        if not who or not str(meta.get("review_note", "") or "").strip():
            errs.append("reviewed 는 reviewed_by·review_note 가 필요하다")
        elif MODEL_NAMES.search(who):
            errs.append("reviewed_by 가 모델이다 — 모델 간 동의는 의학적 검증이 아니다(사람이 표시)")
    summ = meta.get("summary")
    if not isinstance(summ, list) or not summ or not all(isinstance(x, str) and x.strip() for x in summ):
        errs.append("summary 는 빠른 요약 문장 목록")
    exams = meta.get("exams") or []
    if not exams or any(e not in EXAMS for e in exams):
        errs.append("exams 는 kmle/usmle 목록")
    srcs = meta.get("sources")
    src_ids: set[str] = set()
    if not isinstance(srcs, list) or not srcs:
        errs.append("sources 가 비어 있다 — 확인한 출처만 적는다")
        srcs = []
    for i, s in enumerate(srcs, 1):
        if not isinstance(s, dict):
            errs.append(f"sources[{i}] 는 사전"); continue
        for k in ("id", "org", "title", "year", "checked_at", "checked"):
            if not str(s.get(k, "") or "").strip():
                errs.append(f"sources[{i}] 필수 필드 누락: {k}")
        if not (safe_url(s.get("url")) or s.get("doi") or s.get("pmid")) and not (
                s.get("kind") == "textbook" and str(s.get("citation", "")).strip()):
            errs.append(f"sources[{i}] 는 https url·doi·pmid 중 하나로 찾아갈 수 있어야 한다(교과서는 판·장·쪽 citation)")
        if s.get("doi") and not s.get("pmid") and not safe_url(s.get("url")) and s.get("kind") != "textbook":
            errs.append(f"[WARN] sources[{i}] 는 DOI 만 있다 — PubMed 에 있으면 pmid 를 붙인다(개정·철회 추적은 PMID 로 한다. "
                        f"컨테이너가 PubMed 를 막으면 그대로 둔다 — 학습서 워크플로가 DOI 로 PMID 를 찾아 본다)")
        if s.get("verified", "citation") not in VERIFIED:
            errs.append(f"sources[{i}].verified 는 {'/'.join(VERIFIED)}(무엇까지 대조했나)")
        if s.get("kind") and s["kind"] not in SOURCE_KINDS:
            errs.append(f"sources[{i}].kind 는 {'/'.join(SOURCE_KINDS)}")
        src_ids.add(str(s.get("id")))
    for i, c in enumerate(meta.get("criteria") or [], 1):
        if not isinstance(c, dict):
            errs.append(f"criteria[{i}] 는 사전"); continue
        for k in ("id", "name", "kind", "population", "statement", "source", "basis"):
            if not str(c.get(k, "") or "").strip():
                errs.append(f"criteria[{i}] 필수 필드 누락: {k}")
        if c.get("source") and str(c["source"]) not in src_ids:
            errs.append(f"criteria[{i}].source '{c['source']}' 가 sources 에 없다 — 없는 출처를 인용하지 않는다")
        if c.get("basis") and c["basis"] not in BASIS:
            errs.append(f"criteria[{i}].basis 는 current(현행 권고)/past_exam(기출 근거)")
        ce = c.get("exams") or []
        if any(e not in EXAMS for e in ce):
            errs.append(f"criteria[{i}].exams 는 kmle/usmle")
    if "diagram" in meta:
        errs += [f"diagram: {e}" for e in dd.validate(meta.get("diagram"))]
    dn = meta.get("diagram_notes")
    if dn is not None and (not isinstance(dn, list) or not all(isinstance(x, str) and x.strip() for x in dn)):
        errs.append("diagram_notes 는 문장 목록(도식만으로 전달되지 않는 조건·예외)")
    for i, pf in enumerate(meta.get("pitfalls") or [], 1):
        if not isinstance(pf, dict) or not str(pf.get("contrast", "")).strip() or not str(pf.get("point", "")).strip():
            errs.append(f"pitfalls[{i}] 는 {{contrast, point, exception?, cites?, covers?}}")
            continue
        if re.search(r"(모른다|몰랐|몰라서|이해하지 못|착각했을 것)", str(pf.get("point", "")) + str(pf.get("exception", ""))):
            errs.append(f"pitfalls[{i}] — 학습자가 왜 골랐는지 추측하거나 「모른다」고 쓰지 않는다(일반화한 구분점만)")
        for cv in pf.get("covers") or []:
            if not re.match(r"^[a-z]+-\d{4}-\d{4}:[A-E]$", str(cv)):
                errs.append(f"pitfalls[{i}].covers '{cv}' 형식은 <문항id>:<보기 letter>")
    for i, tb in enumerate(meta.get("tables") or [], 1):
        if not isinstance(tb, dict):
            errs.append(f"tables[{i}] 는 사전"); continue
        cols = tb.get("columns") or []
        if not tb.get("id") or not str(tb.get("title", "")).strip() or not isinstance(cols, list) or len(cols) < 2:
            errs.append(f"tables[{i}] 는 id·title·columns(2개 이상) 가 필요하다")
        if tb.get("role") not in TABLE_ROLES:
            errs.append(f"tables[{i}].role 은 {'/'.join(TABLE_ROLES)}")
        if tb.get("span", "column") not in ("full", "column"):
            errs.append(f"tables[{i}].span 은 full(두 단 전체) 또는 column")
        if tb.get("span", "column") == "column" and len(cols) > 4:
            errs.append(f"tables[{i}] 는 열이 {len(cols)}개 — 한 단 표는 4열까지(넓으면 span: full, 더 많으면 역할별로 나눈다)")
        if len(cols) > 6:
            errs.append(f"tables[{i}] 는 열이 {len(cols)}개 — 6열을 넘으면 역할별로 나눈다(글자를 줄여 욱여넣지 않는다)")
        for j, row in enumerate(tb.get("rows") or [], 1):
            if not isinstance(row, list) or len(row) != len(cols):
                errs.append(f"tables[{i}].rows[{j}] 칸 수가 열 수와 다르다")
    # 근거 표시가 가리키는 출처가 있는가
    for sid in sorted(cited_ids(meta) - src_ids):
        errs.append(f"근거 표시 [[{sid}]] 가 sources 에 없다 — 없는 출처를 인용하지 않는다")
    for i, ck in enumerate(meta.get("checks") or [], 1):
        if not isinstance(ck, dict) or not str(ck.get("q", "")).strip() or not str(ck.get("a", "")).strip():
            errs.append(f"checks[{i}] 는 {{q, a}}")
    vids = set()
    for i, v in enumerate(meta.get("variants") or [], 1):
        if not isinstance(v, dict):
            errs.append(f"variants[{i}] 는 사전"); continue
        for k in ("id", "stem", "choices", "answer", "explanation"):
            if not v.get(k):
                errs.append(f"variants[{i}] 필수 필드 누락: {k}")
        ch = v.get("choices") or []
        ans = str(v.get("answer", "")).strip().upper()[:1]
        if ans and (ans not in LETTERS or LETTERS.index(ans) >= len(ch)):
            errs.append(f"variants[{i}].answer '{ans}' 가 보기 범위를 벗어난다")
        if v.get("id") in vids:
            errs.append(f"variants id 중복: {v.get('id')}")
        vids.add(v.get("id"))
        # 오답에서 나온 변형(2026-09-23): of = 틀린 문항 id, changed = 무엇을 바꿨나, flip = 답이 바뀌는가
        if v.get("of") is not None:
            if not re.fullmatch(r"[a-z]+-\d{4}-\d{3,5}", str(v.get("of"))):
                errs.append(f"variants[{i}].of '{v.get('of')}' 는 문항 id(예: kmle-2026-1035)여야 한다")
            if not str(v.get("changed", "") or "").strip():
                errs.append(f"variants[{i}] 는 of 가 있으면 changed(바꾼 단서와 그 결과)를 적어야 한다")
            if not isinstance(v.get("flip"), bool):
                errs.append(f"variants[{i}].flip 은 true(단서를 바꿔 답이 바뀜)·false(겉모습만 바뀌고 답은 그대로)")
    errs += root_errors(meta)
    errs += style_warnings(meta)
    errs += polish_warnings(meta)
    return errs


# ── 판형 2(2026-09-25) 모양 예산 — `note_form: 2` 인 정리본만 본다(옛 정리본은 [restyle] 큐로 하나씩 옮긴다) ──
STYLE_SUMMARY = (3, 5)          # summary 줄 수
STYLE_LINE = 110                # summary 한 줄 글자 수
STYLE_TITLE = 40
STYLE_NODE = {"decision": 30, "start": 40, "step": 40, "info": 40, "alert": 40, "end": 40}
STYLE_EDGE_LABEL = 14
STYLE_LEADS = ("결론:", "시험 단서:")


def style_warnings(meta: dict[str, Any]) -> list[str]:
    if meta.get("note_form") != 2:
        return []
    w: list[str] = []
    title = str(meta.get("title", ""))
    if len(title) > STYLE_TITLE:
        w.append(f"[WARN] 판형 2: title {len(title)}자 > {STYLE_TITLE} — 「질환 — 판단 한 구절」")
    summ = [str(x) for x in meta.get("summary") or []]
    if not STYLE_SUMMARY[0] <= len(summ) <= STYLE_SUMMARY[1]:
        w.append(f"[WARN] 판형 2: summary {len(summ)}줄 — {STYLE_SUMMARY[0]}~{STYLE_SUMMARY[1]}줄")
    for i, lead in enumerate(STYLE_LEADS):
        if len(summ) <= i or not summ[i].startswith(lead):
            w.append(f"[WARN] 판형 2: summary {i + 1}번째 줄은 「{lead}」로 시작한다")
    for i, x in enumerate(summ, 1):
        if len(x) > STYLE_LINE:
            w.append(f"[WARN] 판형 2: summary {i}번째 줄 {len(x)}자 > {STYLE_LINE} — 나머지는 본문·표로")
    dia = meta.get("diagram")
    if isinstance(dia, dict):
        for n in dia.get("nodes") or []:
            lim = STYLE_NODE.get(str(n.get("kind")), 40)
            if isinstance(n, dict) and len(str(n.get("text", ""))) > lim:
                w.append(f"[WARN] 판형 2: 도식 노드 '{n.get('id')}' {len(str(n.get('text', '')))}자 > {lim} — "
                         f"기준 목록·용량·예외는 diagram_notes 나 표로 옮긴다")
        for e in dia.get("edges") or []:
            if isinstance(e, dict) and len(str(e.get("label", "") or "")) > STYLE_EDGE_LABEL:
                w.append(f"[WARN] 판형 2: 도식 갈래 라벨 '{e.get('label')}' > {STYLE_EDGE_LABEL}자")
    elif meta.get("objective_kind") not in ("기전",):
        w.append("[WARN] 판형 2: diagram 이 없다 — 판단 목표는 도식으로 흐름을 보인다(기전 목표만 생략 가능)")
    return w


# ── 분량·중복 린트(2026-11-23 사용자 결정) ── 모두 [WARN] 이다 — 관문(indexer --check · 코드 시험 · test_content ·
# export_concepts_web · publish)은 「[WARN]」이 든 줄을 막지 않는다. 옛 정리본을 일부러 다시 쓰라는 뜻이 아니라
# 새로 쓰거나 손질할 때 맞추라는 표지다.
POLISH_BODY = 3200      # 본문 글자 수 상한. 「본문」 = frontmatter 뒤의 Markdown 전체(`## 제목` 줄 · 근거 표시 `[[…]]` · (심화) 절 포함)를
                        # 줄 끝을 \n 으로 맞추고 앞뒤 공백을 뗀 길이. summary · 표 · 도식 같은 frontmatter 는 세지 않는다.
                        # 로더(load_concepts)가 `_body` 로 넘길 때만 센다(사전만 받은 검사에서는 건너뛴다).
POLISH_NOTES = 4        # diagram_notes 항목 수 상한
POLISH_DUP = 0.7        # summary 한 문장의 글자 2개 묶음 가운데 이 비율 이상이 `## 판단` 절의 한 문장에 그대로 있으면 되풀이
POLISH_DUP_MIN = 15     # 다듬은 길이가 이보다 짧은 문장은 견주지 않는다(짧은 구절의 우연한 겹침)
POLISH_KINDS = ("분량", "도식 설명", "중복", "변형 없음")
_ANY_CITE_RE = re.compile(r"\[\[[^\]]*\]\]")
_SUMMARY_LEAD_RE = re.compile(r"^(?:결론|시험 단서|왜)\s*:\s*")


def _norm_sentence(s: str) -> str:
    """견줄 문장 — 근거 표시 · 글머리표 · summary 머리말(결론: …)을 떼고, 공백 · 문장부호를 지운 소문자."""
    s = _ANY_CITE_RE.sub("", str(s))
    s = re.sub(r"^\s*(?:[-*+]|\d+\.)\s+", "", s)
    s = _SUMMARY_LEAD_RE.sub("", s.strip())
    return re.sub(r"[\W_]+", "", s).lower()


def _sentences(text: str) -> list[tuple[str, str]]:
    """[(다듬은 문장, 원문)] — 줄바꿈과 문장 끝(. ! ?) 뒤 공백에서 나눈다."""
    out = []
    for ln in str(text).replace("\r\n", "\n").split("\n"):
        for s in re.split(r"(?<=[.!?])\s+", ln):
            n = _norm_sentence(s)
            if n:
                out.append((n, s.strip()))
    return out


def _bigrams(n: str) -> set[str]:
    return {n[i:i + 2] for i in range(len(n) - 1)}


def summary_repeats(meta: dict[str, Any]) -> list[tuple[int, str, float]]:
    """summary 가 본문 `## 판단` 절의 문장을 되풀이하는 곳 — [(summary 줄 번호, 그 문장, 겹친 비율)].

    기준: summary 한 문장(다듬은 길이 ≥ POLISH_DUP_MIN)의 글자 2개 묶음 가운데 POLISH_DUP 이상이
    `## 판단 …` 절의 **한 문장**에 들어 있다. 뜻이 같은지는 보지 않는다 — 같은 글자가 되풀이되는지만 본다.
    2026-11-23 실측(정리본 212개 · 판단 절 196개): 다듬은 문장이 글자까지 같은 것 0개 · 0.9 → 5개 · 0.8 → 20개 · 0.7 → 33개 ·
    0.6 → 52개. 0.70~0.74 의 10문장은 읽어 보니 모두 같은 문장을 고쳐 쓴 것이었고, 0.60~0.64 의 14문장에는
    같은 낱말만 겹치는 다른 내용이 섞여 있어 0.7 로 잡았다.
    """
    judge = "\n".join(md for title, md in split_sections(str(meta.get("_body", "")))
                      if title.replace("(심화)", "").strip().startswith("판단"))
    js = [_bigrams(n) for n, _ in _sentences(judge) if len(n) >= POLISH_DUP_MIN]
    out: list[tuple[int, str, float]] = []
    if not js:
        return out
    for i, line in enumerate(meta.get("summary") or [], 1):
        for n, raw in _sentences(str(line)):
            if len(n) < POLISH_DUP_MIN:
                continue
            b = _bigrams(n)
            best = max(len(b & x) / len(b) for x in js)
            if best >= POLISH_DUP:
                out.append((i, raw, best))
    return out


def polish_warnings(meta: dict[str, Any]) -> list[str]:
    """분량 · 도식 설명 · summary↔판단 중복 · 변형 없음 — 전부 [WARN](커밋 · 게시를 막지 않는다)."""
    w: list[str] = []
    if "_body" in meta:
        n = len(str(meta.get("_body", "")).replace("\r\n", "\n").strip())
        if n > POLISH_BODY:
            w.append(f"[WARN] 분량: 본문 {n:,}자 > {POLISH_BODY:,} — 표 · 도식에 있는 것을 본문에서 다시 늘어놓지 않는다"
                     f"(판형 2 본문은 2,500자 안팎)")
        for i, raw, ratio in summary_repeats(meta):
            w.append(f"[WARN] 중복: summary {i}번째 줄 「{raw[:36]}」이 본문 「## 판단」 절의 문장을 되풀이한다"
                     f"(글자 겹침 {ratio:.0%}) — summary 는 결론 한 줄, 판단 절은 그 이유를 쓴다")
    dn = meta.get("diagram_notes")
    if isinstance(dn, list) and len(dn) > POLISH_NOTES:
        w.append(f"[WARN] 도식 설명: diagram_notes {len(dn)}줄 > {POLISH_NOTES} — 도식만으로 전달되지 않는 조건 · 예외만 남기고 "
                 f"기준 목록 · 수치는 표(tables) · criteria 로 옮긴다")
    if not [v for v in meta.get("variants") or [] if isinstance(v, dict)]:
        w.append("[WARN] 변형 없음: variants 가 하나도 없다 — 다시 풀어 볼 핵심 변형 문항을 1개 이상 둔다"
                 "(오답에서 나온 정리본은 틀린 문항마다 2개)")
    return w


def polish_kind(err: str) -> str | None:
    """오류 줄이 분량·중복 린트면 그 종류(POLISH_KINDS), 아니면 None — CLI 요약 · 보고용."""
    for k in POLISH_KINDS:
        if f"[WARN] {k}:" in err:
            return k
    return None


# ── 미대조 표시(2026-11-23 — 큐 `[verify]` 가 센다) ─────────────────
# 원고에 남는 표시는 둘이다.
#   `[[?출처id]]` · `[[?출처id: 위치]]` — 이 주장만 원문과 대조하지 않았다(CITE_RE 의 `?`). 화면 · PDF 에서 † 가 붙는다.
#   `†` — 원고에 손으로 적은 글자. 「원문 미대조(†)」「초록만 읽었다(†)」처럼 표 note · diagram_notes · 시험 쟁점 줄에
#          대조하지 못한 범위(용량 · 기간 · 세부 수치 · 지침 본문)를 밝힐 때 쓴다.
# `sources[].verified` 가 text 가 아니라서 **조판 때 붙는** † 는 원고의 표시가 아니므로 세지 않는다.
_MARK_SKIP = {"errors", "geo", "hash", "path"}


def _strings(v: Any, skip: set[str]) -> list[str]:
    if isinstance(v, str):
        return [v]
    if isinstance(v, dict):
        return [s for k, x in v.items() if k not in skip for s in _strings(x, skip)]
    if isinstance(v, (list, tuple)):
        return [s for x in v for s in _strings(x, skip)]
    return []


def unverified_marks(meta: dict[str, Any]) -> dict[str, Any]:
    """{claims: `[[?…]]` 수, dagger: 손으로 적은 † 수, marks: 둘의 합, sources: `[[?…]]` 가 가리키는 출처 id 목록}.

    적재된 정리본(frontmatter + `sections` 의 HTML — 근거 표시는 글자 그대로 남아 있다)이나
    `_body` 를 붙인 frontmatter 사전 어느 쪽이든 받는다(둘 다 있으면 본문은 `_body` 로 한 번만 센다).
    """
    skip = set(_MARK_SKIP) | ({"sections"} if "_body" in meta else set())
    claims = dagger = 0
    ids: set[str] = set()
    for s in _strings(meta, skip):
        dagger += s.count("†")
        for m in CITE_RE.finditer(s):
            if m.group(1):
                claims += 1
                ids.add(m.group(2))
    return {"claims": claims, "dagger": dagger, "marks": claims + dagger, "sources": sorted(ids)}


def diagram_fit_errors(concepts: dict[str, dict]) -> list[str]:
    """PDF 한 쪽에 읽을 수 있는 크기로 안 들어가는 도식 — 학습서 빌드가 그 책을 멈추므로 커밋 전에 막는다."""
    import build_books as bb                     # 늦게 가져온다(build_books 가 이 모듈을 가져온다)
    out = []
    for cid, c in concepts.items():
        if c.get("diagram") and not dd.validate(c["diagram"]):
            fit = bb.fit_diagram(c["diagram"])
            if not fit["ok"]:
                out.append(f"{c.get('path', cid)}: 도식이 읽을 크기로 한 쪽에 들어가지 않는다(글자 {fit['pt']:.1f}pt < "
                           f"{bb.DIA_FULL_FLOOR_PT}pt, 두 단 전체 기준) — 노드 글을 줄이거나(판단 ≤30자) 의미 단위로 나눈다")
    return out


def _cite_texts(meta: dict[str, Any]) -> list[str]:
    out = [str(meta.get("_body", ""))]
    for tb in meta.get("tables") or []:
        if isinstance(tb, dict):
            out.append(str(tb.get("note", "")))
            out += [str(c) for row in tb.get("rows") or [] if isinstance(row, list) for c in row]
    for pf in meta.get("pitfalls") or []:
        if isinstance(pf, dict):
            out += [str(pf.get("point", "")), str(pf.get("exception", ""))]
            out += [f"[[{c}]]" for c in pf.get("cites") or []]
    out += [str(x) for x in meta.get("diagram_notes") or []]
    return out


def cited_ids(meta: dict[str, Any]) -> set[str]:
    ids = {m.group(2) for s in _cite_texts(meta) for m in CITE_RE.finditer(s)}
    ids |= {str(c.get("source")) for c in meta.get("criteria") or [] if isinstance(c, dict) and c.get("source")}
    return ids


def source_numbers(meta: dict[str, Any]) -> dict[str, int]:
    """단원 안에서의 근거 번호 — sources 순서대로 1, 2, …"""
    return {str(s.get("id")): i for i, s in enumerate(meta.get("sources") or [], 1) if isinstance(s, dict)}


ID_MENTION_RE = re.compile(r"(?:<code>|`)?\b(cn\.[a-z0-9-]+\.[a-z0-9-]+\.[a-z0-9-]+)\b(?:</code>|`)?")


@lru_cache(maxsize=1)
def concept_titles() -> dict[str, str]:
    """{정리본 id: 제목} — frontmatter 만 읽는다(load_concepts 를 부르지 않아 순환이 없다)."""
    out: dict[str, str] = {}
    for f in CONCEPT_DIR.rglob("*.md") if CONCEPT_DIR.exists() else []:
        try:
            m = load(f).meta
        except Exception:
            continue
        if m.get("id") and m.get("title"):
            out[str(m["id"])] = str(m["title"])
    return out


def humanize_ids(text: str) -> str:
    """본문이 다른 정리본을 내부 id 로 가리키면(「cn.peds.….secondary-prophylaxis 가 다룬다」) 그 정리본 제목으로 바꾼다.
    2026-09-25: 루틴이 쓴 정리본 두 개가 id 를 본문에 적어 학습서 검증(「내부 ID 가 PDF 에 보인다」)이 안과·소아청소년과 책을 멈췄다.
    모르는 id 는 그대로 둔다(검증이 잡는다)."""
    titles = concept_titles()

    def rep(m: re.Match) -> str:
        t = titles.get(m.group(1))
        return f"「{t}」" if t else m.group(0)
    return ID_MENTION_RE.sub(rep, text)


def render_cites(text: str, meta: dict[str, Any], mode: str = "web", anchor: str = "") -> str:
    """[[id: 위치]] 를 번호 근거로 바꾼다. text 는 이미 escape·정화된 글이어야 한다(여기서 만드는 태그만 더해진다).
    mode=pdf 이면 단원 끝 참고문헌으로 가는 링크, web 이면 <sup>. 원문 본문과 대조하지 않은 근거에는 † 를 붙인다."""
    nums = source_numbers(meta)
    ver = {str(s.get("id")): s.get("verified", "citation") for s in meta.get("sources") or [] if isinstance(s, dict)}

    def rep(m: re.Match) -> str:
        unverified, sid, loc = m.group(1), m.group(2), (m.group(3) or "").strip()
        n = nums.get(sid)
        if n is None:
            return html.escape(m.group(0), quote=False)
        dagger = "†" if (unverified or ver.get(sid) != "text") else ""
        label = f"{n}{dagger}" + (f" {loc}" if loc else "")
        if mode == "pdf":
            return f'<a class="cite" href="#{anchor}-ref-{n}">[{label}]</a>'
        return f"<sup>[{label}]</sup>"
    return humanize_ids(CITE_RE.sub(rep, text))


def question_learning_errors(meta: dict[str, Any], concept: dict | None) -> list[tuple[str, str]]:
    """문항의 objective·distractors·case_path 형식. (level, msg) 목록."""
    out: list[tuple[str, str]] = []
    obj = meta.get("objective")
    dist = meta.get("distractors")
    case = meta.get("case_path")
    if obj is None and dist is None and case is None:
        return out
    if obj is not None and not ID_RE.match(str(obj)):
        out.append(("ERROR", f"objective '{obj}' 형식 오류 — 개념 정리본 id(cn.<과>.<주제>.<목표>)"))
    elif obj is not None and concept is None:
        out.append(("WARN", f"objective '{obj}' 의 정리본이 아직 없다 — 학습서에 「정리본 작성 대기」로 들어간다"))
    ver = meta.get("version")
    if ver is not None and (not isinstance(ver, int) or ver < 1):
        out.append(("ERROR", "version 은 1 이상의 정수(문항을 고치면 올린다)"))
    ans = str(meta.get("answer", "")).strip().upper()[:1]
    n = len(meta.get("choices") or [])
    split_nodes = []
    if dist is not None:
        if not isinstance(dist, dict):
            out.append(("ERROR", "distractors 는 {보기 letter: {...}} 사전"))
            dist = {}
        for letter, d in dist.items():
            L = str(letter).upper()
            if L not in LETTERS[:n] or L == ans:
                out.append(("ERROR", f"distractors.{letter} — 정답이 아닌 보기 letter 여야 한다"))
            if not isinstance(d, dict):
                out.append(("ERROR", f"distractors.{letter} 는 사전")); continue
            for k in ("tempting", "answer_first", "discriminator"):
                if not str(d.get(k, "") or "").strip():
                    out.append(("ERROR", f"distractors.{letter}.{k} 가 비어 있다"))
            text = " ".join(str(d.get(k, "")) for k in ("tempting", "answer_first", "discriminator"))
            if re.search(r"(모른다|몰랐|모르기 때문|이해하지 못)", text):
                out.append(("ERROR", f"distractors.{letter} — 학습자가 「모른다」고 단정하지 않는다(왜 끌리는가를 쓴다)"))
            if d.get("split"):
                split_nodes.append(str(d["split"]))
    if concept is not None and concept.get("diagram"):
        for e in dd.validate_case(concept["diagram"], case, split_nodes):
            out.append(("ERROR", f"case_path/split: {e}"))
    return out


# ── 적재 ───────────────────────────────────────────────────────────
def content_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()[:16]


def load_concepts(root: Path = CONCEPT_DIR) -> tuple[dict[str, dict], list[str]]:
    """{id: concept} 와 오류 목록. 오류가 있는 정리본도 버리지 않고 `errors` 를 달아 둔다(화면이 깨지지 않게)."""
    out: dict[str, dict] = {}
    errors: list[str] = []
    for p in sorted(root.rglob("*.md")) if root.exists() else []:
        d = load(p)
        m = d.meta
        errs = list(d.errors) + validate_concept({**m, "_body": d.body}, p)
        cid = str(m.get("id", p.stem))
        if cid in out:
            errs.append(f"concept id 중복: {cid}")
        c = dict(m)
        c["id"] = cid
        c["path"] = str(p.relative_to(ROOT)).replace("\\", "/")
        c["hash"] = content_hash(p)
        c["sections"] = sections(d.body)
        c["errors"] = errs
        try:
            c["geo"] = dd.layout(m["diagram"]) if m.get("diagram") else None
        except dd.DiagramError as e:
            c["geo"] = None
            errs.append(f"diagram: {e}")
        errors += [f"{c['path']}: {e}" for e in errs]
        out[cid] = c
    for cid, es in root_link_errors(out).items():              # 정리본 사이 — roots 가 가리키는 기초 정리본
        out[cid]["errors"] += es
        errors += [f"{out[cid]['path']}: {e}" for e in es]
    return out, errors


def load_questions() -> dict[str, dict]:
    """{qid: meta+{type, path}} — 학습 흐름에 필요한 필드만 쓰지만 전부 둔다."""
    qs: dict[str, dict] = {}
    for base in QUESTION_DIRS:
        for p in sorted(base.rglob("*.md")) if base.exists() else []:
            d = load(p)
            if d.type not in QUESTION_TYPES or not d.id:
                continue
            m = dict(d.meta)
            m["path"] = str(p.relative_to(ROOT)).replace("\\", "/")
            m["body"] = d.body
            qs[d.id] = m
    return qs


def linked_questions(questions: dict[str, dict]) -> dict[str, list[str]]:
    out: dict[str, list[str]] = {}
    for qid, m in questions.items():
        if m.get("objective"):
            out.setdefault(str(m["objective"]), []).append(qid)
    return {k: sorted(v) for k, v in out.items()}


def learning_fields(meta: dict[str, Any]) -> dict[str, Any]:
    """웹 문항 레코드에 덧붙일 학습 흐름 필드(없으면 null — 옛 문항은 그대로 동작)."""
    dist = meta.get("distractors") if isinstance(meta.get("distractors"), dict) else None
    clean = None
    if dist:
        clean = {}
        for k, d in dist.items():
            if isinstance(d, dict):
                clean[str(k).upper()] = {x: str(d.get(x, "") or "") for x in
                                         ("tempting", "answer_first", "discriminator", "when_right", "split")}
    case = meta.get("case_path") if isinstance(meta.get("case_path"), dict) else None
    visit = None
    if case and isinstance(case.get("visit"), list):
        visit = [{"node": str(v.get("node")), "state": str(v.get("state", "path")), "note": str(v.get("note", "") or "")}
                 for v in case["visit"] if isinstance(v, dict)]
    out = {
        "objective": str(meta["objective"]) if meta.get("objective") else None,
        "qversion": int(meta.get("version") or 1),
        "distractors": clean,
        "casePath": visit,
    }
    # 값이 있는 것만 싣는다(1,000여 문항 번들을 불리지 않게 — 앱은 없으면 기본값: 판 1, 흐름 필드 없음)
    return {k: v for k, v in out.items() if v and not (k == "qversion" and v == 1)}


if __name__ == "__main__":
    import sys
    cs, errs = load_concepts()
    if "--basic" in sys.argv[1:]:
        # 기초 정리본 목록 — [root] 를 처리할 때 「같은 기전의 기초 정리본이 이미 있는가」를 여기서 먼저 본다
        sup = root_supports(cs)
        rows = sorted((str(c.get("discipline")), str(c.get("system")), cid) for cid, c in cs.items() if is_basic(c))
        for disc, system, cid in rows:
            c = cs[cid]
            print(f"{disc:13} {system:20} {cid}  「{c.get('title')}」  교과서 {c.get('textbook_check')} · 받치는 임상 정리본 {len(sup.get(cid, []))}")
        print(f"기초 정리본 {len(rows)}개")
        sys.exit(0)
    qs = load_questions()
    links = linked_questions(qs)
    for cid, c in cs.items():
        print(f"{cid}  v{c.get('version')}  {c.get('review_status')}  문항 {len(links.get(cid, []))}  hash {c['hash']}")
    for qid, m in qs.items():
        if m.get("objective"):
            for lvl, msg in question_learning_errors(m, cs.get(str(m["objective"]))):
                errs.append(f"{m['path']}: [{lvl}] {msg}")
    errs += diagram_fit_errors(cs)
    for e in errs:
        print("  ✗", e)
    hard = [e for e in errs if "[WARN]" not in e]
    kinds = {k: sum(1 for e in errs if polish_kind(e) == k) for k in POLISH_KINDS}
    print(f"오류 {len(hard)}건 · 경고 {len(errs) - len(hard)}건(그중 " + " · ".join(f"{k} {n}" for k, n in kinds.items())
          + ") — 경고는 커밋을 막지 않는다")
    sys.exit(1 if hard else 0)
