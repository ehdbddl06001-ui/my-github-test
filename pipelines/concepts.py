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


def sections(body: str) -> list[dict]:
    """`## 제목` 단위로 나눈다. 「(심화)」로 시작하는 절은 웹에서 접힌다(PDF 는 모두 편다)."""
    out: list[dict] = []
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
                errs.append(f"[WARN] 해리슨 대조 없음 — 슬롯 {slot} = 해리슨 {', '.join(map(str, sl.chapters))}장. "
                            f"그 장을 읽고 harrison-21 출처(verified: text)와 [[harrison-21: 장 p.N]] 을 단다")
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
    return errs


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
    return CITE_RE.sub(rep, text)


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
    qs = load_questions()
    links = linked_questions(qs)
    for cid, c in cs.items():
        print(f"{cid}  v{c.get('version')}  {c.get('review_status')}  문항 {len(links.get(cid, []))}  hash {c['hash']}")
    for qid, m in qs.items():
        if m.get("objective"):
            for lvl, msg in question_learning_errors(m, cs.get(str(m["objective"]))):
                errs.append(f"{m['path']}: [{lvl}] {msg}")
    for e in errs:
        print("  ✗", e)
    sys.exit(1 if any("[WARN]" not in e for e in errs) else 0)
