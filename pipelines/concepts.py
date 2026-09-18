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
LETTERS = "ABCDE"
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


def md_to_html(md: str) -> str:
    import markdown  # 표준 파이썬 markdown — 결과는 반드시 sanitize 를 거친다
    return sanitize(markdown.markdown(md, extensions=["tables"], output_format="html"))


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
        if not (safe_url(s.get("url")) or s.get("doi") or s.get("pmid")):
            errs.append(f"sources[{i}] 는 https url·doi·pmid 중 하나로 찾아갈 수 있어야 한다")
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
    return errs


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
        errs = list(d.errors) + validate_concept(m, p)
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
