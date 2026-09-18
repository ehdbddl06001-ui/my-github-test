"""build_books.py — 오답·표시가 쌓인 학습 목표를 과별 누적 PDF 학습서로 만든다(아이패드용).

2026-09-18 사용자 지시 요약
- 과별 책(설정으로 권 나눔) · 주제별 단원 · 전체 목차. 오답 + 사용자가 표시한 것(찍었다·이해 안 됨·반복 혼동·정리본 원함)만.
- 해설 열람 · 정리본 읽음 · 이해 표시 · 이후 적용 성공을 구분한다. 재확인 완료 단원도 지우지 않고 상태만 바꾼다.
- 단원: 들어온 이유와 연결 오답 · 정의 · 병태생리 · 기전→소견 · 기준 · 감별 · 검사 · 치료 · 권고와 예외 ·
  판단 도식(일반 구조 — 사례 경로는 문항 화면에서만) · 내 반복 혼동 · 스스로 묻기 · 출처와 마지막 검토일.
- 기준·권고는 대상 집단·종류·예외·발행 기관·연도·확인일을 남기고 KMLE/USMLE·기출 근거/현행 권고를 가른다.
- 콘텐츠 원본은 content/concepts(웹과 같은 적재 결과 — concepts.py). 내용 상태와 학습자 상태를 섞지 않는다.
- 반복 오답은 단원을 다시 만들지 않고 연결 오답·반복 혼동에만 더한다. 사용자 메모는 따로 보관해 옮겨 싣기만 한다.
- 글자 PDF(한글 글꼴 임베드) · 한 단 · 이름/버전/날짜 · 누르는 차례 · 책갈피 · 쪽 번호 · 교차 링크 · 출처 링크 ·
  연결 문항 ID · 읽기 좋은 크기. 넓은 표는 나누고, 도식은 벡터로 한 쪽 안에서 자르지 않는다.
- 실제로 렌더링해 검증한다(글꼴·줄바꿈·차례 링크·쪽 나눔·한글 검색). 검증을 통과한 파일만 최신본을 바꾼다.
- 바뀐 것이 없으면 건너뛴다. 실패하면 이전 PDF 를 그대로 두고 원인·재시도 대상을 남긴다. 되풀이해도 결과가 같다.

사용:
  python pipelines/build_books.py                       # 바뀐 책만 만들고 검증(업로드 없음)
  python pipelines/build_books.py --upload              # + Google Drive 갱신(drive_books.py)
  python pipelines/build_books.py --force --only 소아청소년과
  python pipelines/build_books.py --events <학습기록.json> --state-dir <임시> --out <임시>   # 검증·시연용
  python pipelines/build_books.py --preview             # 검수용 PNG(out/_preview)
"""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import shutil
import sys
import tempfile
import traceback
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import yaml

import decision_diagram as dd
import learning_log as ll
from concepts import BASIS, linked_questions, load_concepts, load_questions, safe_url

ROOT = Path(__file__).resolve().parent.parent
CONFIG = Path(__file__).with_name("books_config.yaml")
STATE_DIR = ROOT / "state" / "books"
SOURCE_CHECKS = ROOT / "state" / "source_checks.json"
KST = timezone(timedelta(hours=9))


def now_kst() -> datetime:
    return datetime.now(KST)


def load_config(path: Path = CONFIG) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def esc(s: Any) -> str:
    return html.escape(str(s if s is not None else ""), quote=True)


def slug(s: str) -> str:
    return re.sub(r"[^0-9A-Za-z가-힣]+", "_", s).strip("_")


# ── 계획: 어떤 단원이 어느 책에 ─────────────────────────────────────
@dataclass
class Unit:
    key: str                      # 개념 id(목표) — 안정 ID
    book: str
    concept: dict | None          # None 이면 「정리본 작성 대기」 임시 단원
    state: ll.State
    questions: list[str]          # 같은 목표로 연결된 문항 전부
    title: str = ""
    flags: list[str] = field(default_factory=list)   # 출처 갱신 확인 필요 등

    @property
    def anchor(self) -> str:
        return "u-" + re.sub(r"[^a-z0-9]+", "-", self.key.lower()).strip("-")


@dataclass
class Book:
    name: str
    units: list[Unit] = field(default_factory=list)
    pending: list[tuple[ll.State, dict]] = field(default_factory=list)   # 목표가 없는 문항 오답(연결 대기)


def book_of(topic: str, cfg: dict) -> str:
    return (cfg.get("books") or {}).get(str(topic or ""), str(topic or "기타") or "기타")


def included(s: ll.State, cfg: dict) -> bool:
    if not s.status:
        return False
    if s.wrongs:
        return True
    if cfg.get("include_later") and s.later:
        return True
    return any(s.flags.get(f) for f in cfg.get("include_flags") or [])


def source_key(s: dict) -> str:
    return str(s.get("doi") or s.get("pmid") or s.get("url") or s.get("id"))


def plan(concepts: dict, questions: dict, S: dict[str, ll.State], cfg: dict, source_state: dict) -> dict[str, Book]:
    links = linked_questions(questions)
    books: dict[str, Book] = {}
    for key, s in S.items():
        if not included(s, cfg):
            continue
        if s.objective:
            c = concepts.get(s.objective)
            if c:
                name = book_of(c.get("topic"), cfg)
                title = str(c.get("title"))
            else:
                q = next((questions[q] for q in s.qids if q in questions), {})
                name = book_of(q.get("topic"), cfg)
                title = f"정리본 작성 대기 — {s.objective}"
            u = Unit(key=s.objective, book=name, concept=c, state=s, questions=links.get(s.objective, list(s.qids)), title=title)
            if c:
                for src in c.get("sources") or []:
                    st = source_state.get(source_key(src)) or {}
                    if st.get("status") in ("changed", "failed"):
                        u.flags.append(f"업데이트 확인 필요 — {src.get('org')} {src.get('year')}: {st.get('note', '')}")
            books.setdefault(name, Book(name)).units.append(u)
        else:
            q = questions.get(key[2:], {})
            name = book_of(q.get("topic"), cfg)
            books.setdefault(name, Book(name)).pending.append((s, q))
    for b in books.values():
        b.units.sort(key=lambda u: (u.title, u.key))
        b.pending.sort(key=lambda p: p[0].key)
    return books


def volumes(book: Book, cfg: dict) -> list[tuple[str, list[Unit]]]:
    n = max(1, int(cfg.get("volume_max_units") or 40))
    if len(book.units) <= n:
        return [(book.name, book.units)]
    return [(f"{book.name} {i // n + 1}권", book.units[i:i + n]) for i in range(0, len(book.units), n)]


# ── 지문(바뀐 것이 없으면 건너뛰기) ─────────────────────────────────
def unit_fingerprint(u: Unit) -> dict:
    s = u.state
    return {
        "concept": (u.concept or {}).get("hash"), "version": (u.concept or {}).get("version"),
        "status": s.status, "wrongs": s.wrongs, "chosen": s.chosen, "reasons": s.reasons,
        "flags": {k: v for k, v in s.flags.items() if v}, "evidence": s.evidence(), "memo": s.memo,
        "later": s.later, "checks": [s.checks_ok, s.checks_miss], "questions": u.questions, "src": u.flags,
    }


def volume_hash(title: str, units: list[Unit], pending: list, cfg: dict) -> str:
    payload = {"t": title, "tv": cfg.get("template_version"), "web": cfg.get("web_base"),
               "units": [(u.key, unit_fingerprint(u)) for u in units],
               "pending": [(s.key, s.wrongs, s.chosen, s.flags) for s, _ in pending]}
    return hashlib.sha256(json.dumps(payload, ensure_ascii=False, sort_keys=True, default=str).encode()).hexdigest()[:20]


# ── HTML ────────────────────────────────────────────────────────────
CSS = """
@font-face{font-family:BookKR; src:url("%(regular)s"); font-weight:400}
@font-face{font-family:BookKR; src:url("%(bold)s"); font-weight:700}
@page{size:A4; margin:16mm 15mm 18mm 15mm}
html{font-family:BookKR, sans-serif; font-size:11.5pt; line-height:1.62; color:#1b2430}
body{margin:0}
h1{font-size:22pt; margin:0 0 6mm}
h2{font-size:16pt; margin:0 0 2mm; line-height:1.35}
h3{font-size:12.5pt; margin:6mm 0 2mm; padding-bottom:1mm; border-bottom:0.6pt solid #b8c2d0; break-after:avoid}
h4{font-size:11.5pt; margin:4mm 0 1mm; break-after:avoid}
p,li{orphans:2; widows:2}
a{color:#0b57d0; text-decoration:none}
.page{break-before:page}
.cover{padding-top:40mm}
.cover .meta{color:#4a5566; font-size:11pt}
.box{border:0.8pt solid #b8c2d0; border-radius:3mm; padding:3mm 4mm; margin:3mm 0; break-inside:avoid}
.muted{color:#4a5566}
.small{font-size:9.5pt}
.toc{list-style:none; padding:0; margin:0}
.toc li{display:flex; align-items:baseline; gap:2mm; padding:1.2mm 0; border-bottom:0.3pt dotted #c8d0dc; break-inside:avoid}
.toc .st{flex:0 0 22mm; font-size:9.5pt}
.toc a{flex:1}
.toc .pg{flex:0 0 12mm; text-align:right; font-variant-numeric:tabular-nums}
.stag{display:inline-block; border:0.6pt solid #8a96a8; border-radius:1.5mm; padding:0 1.6mm; font-size:9pt; margin-right:1.5mm}
.st-need{border-color:#b3261e; color:#b3261e}
.st-doing{border-color:#8a5a00; color:#8a5a00}
.st-done{border-color:#1e7a44; color:#1e7a44}
.warn{border-color:#b3261e; background:#fdf1f0}
.unit-meta{font-size:9.5pt; color:#4a5566; margin-bottom:2mm}
.evid{display:flex; flex-wrap:wrap; gap:2mm; margin:2mm 0}
.evid span{border:0.6pt solid #b8c2d0; border-radius:1.5mm; padding:0.5mm 2mm; font-size:9.5pt}
.summary{background:#f3f6fa}
.summary ul{margin:1mm 0; padding-left:5mm}
.crit{border:0.6pt solid #c8d0dc; border-radius:2mm; padding:2mm 3mm; margin:2mm 0; break-inside:avoid}
.crit dt{font-weight:700; font-size:9.5pt; color:#4a5566}
.crit dd{margin:0 0 1mm 0}
figure.dia{break-inside:avoid; margin:3mm 0; text-align:center}
figure.dia svg{max-width:100%%; height:auto; max-height:215mm}
figure.dia figcaption{font-size:9.5pt; color:#4a5566}
.steps{font-size:10pt; padding-left:6mm}
.steps li{break-inside:avoid}
.err{border-left:1mm solid #b3261e; padding:1mm 3mm; margin:2mm 0; break-inside:avoid}
.memo{border-left:1mm solid #7c5cff; padding:1mm 3mm; margin:2mm 0; background:#f6f3ff}
.rowcard{border:0.6pt solid #c8d0dc; border-radius:2mm; padding:2mm 3mm; margin:2mm 0; break-inside:avoid}
table{border-collapse:collapse; width:100%%; table-layout:fixed; word-break:keep-all; overflow-wrap:anywhere; font-size:10pt}
td,th{border:0.5pt solid #b8c2d0; padding:1mm 1.5mm; vertical-align:top}
.deep h3::after{content:" (심화)"; color:#4a5566; font-size:10pt}
code{font-size:9.5pt}
"""


def stack_wide_tables(fragment: str, max_cols: int = 4) -> str:
    """정화된(속성 없는) HTML 의 표 가운데 열이 많은 것을 행 카드로 바꾼다 — 좁은 화면·A4 에서 잘리지 않게."""
    def conv(m: re.Match) -> str:
        t = m.group(0)
        heads = re.findall(r"<th>(.*?)</th>", t, re.S)
        if len(heads) <= max_cols:
            return t
        rows = re.findall(r"<tr>(.*?)</tr>", t, re.S)
        out = []
        for r in rows:
            cells = re.findall(r"<td>(.*?)</td>", r, re.S)
            if not cells:
                continue
            out.append('<div class="rowcard">' + "".join(
                f"<div><b>{h}</b> {c}</div>" for h, c in zip(heads, cells)) + "</div>")
        return "".join(out)
    return re.sub(r"<table>.*?</table>", conv, fragment, flags=re.S)


def status_tag(st: str | None) -> str:
    if not st:
        return ""
    return f'<span class="stag st-{st}">{esc(ll.STATUS[st])}</span>'


def weblink(cfg: dict, **q: str) -> str:
    base = safe_url(cfg.get("web_base")) or ""
    if not base:
        return ""
    return base + "index.html?" + "&".join(f"{k}={esc(v)}" for k, v in q.items())


def unit_html(u: Unit, cfg: dict, questions: dict, answers: list, book_names: dict) -> str:
    c, s = u.concept, u.state
    h = [f'<section class="page unit" id="{u.anchor}">']
    h.append(f"<h2>{esc(u.title)}</h2>")
    rev = (c or {}).get("review_status", "unreviewed")
    rev_txt = ("내용 검토 완료 — " + esc((c or {}).get("reviewed_by", ""))) if rev == "reviewed" else \
        "의학적 내용 검토 전(형식 검사만 통과)" if c else "임시 단원 — 문항 해설에서 옮김, 검토 전"
    h.append(f'<div class="unit-meta">{status_tag(s.status)} 단원 ID {esc(u.key)} · '
             + (f"v{esc(c.get('version'))} · 최근 갱신 {esc(c.get('updated', c.get('date')))} · " if c else "")
             + f"{rev_txt}</div>")
    ev = s.evidence()
    h.append('<div class="evid">' + "".join(f"<span>{esc(k)} {'✓' if v else '–'}</span>" for k, v in ev.items()) + "</div>")
    for f in u.flags:
        h.append(f'<div class="box warn"><b>{esc(f)}</b><br><span class="small">내용은 그대로 두었다. 출처의 개정 여부를 사람이 확인한 뒤 정리본을 고친다.</span></div>')
    if c:
        h.append('<div class="box summary"><b>빠른 요약</b><ul>' + "".join(f"<li>{esc(x)}</li>" for x in c.get("summary") or []) + "</ul></div>")
        h.append(f'<div class="small"><b>학습 목표</b> ({esc(c.get("objective_kind"))}) {esc(c.get("objective"))}</div>')

    # 들어온 이유 · 연결 오답
    h.append("<h3>이 단원이 들어온 이유</h3>")
    if s.chosen:
        for ch in s.chosen:
            q = questions.get(ch["qid"], {})
            link = weblink(cfg, q=ch["qid"]) if not str(ch["qid"]).count("#") else ""
            dist = _dist_for(q, ch["text"])
            h.append('<div class="err">' + f'{esc(ch["day"])} · 문항 '
                     + (f'<a href="{link}">{esc(ch["qid"])}</a>' if link else esc(ch["qid"]))
                     + (" (변형 문제)" if ch.get("mode") == "variant" else "")
                     + f'<br>고른 답 <b>{esc(ch["text"])}</b> → 정답 <b>{esc(ch["answer"])}</b>'
                     + (f'<br><span class="small">왜 끌리는가: {esc(dist.get("tempting"))}</span>' if dist else "") + "</div>")
    marks = [ll.FLAGS[k] for k, v in s.flags.items() if v and k in ll.FLAGS]
    if s.later:
        marks.append("나중에 복습으로 저장")
    if marks:
        h.append(f'<p class="small">표시: {esc(" · ".join(marks))}</p>')
    if s.reasons:
        h.append('<p class="small">스스로 고른 틀린 이유: ' + esc(" · ".join(f"{ll.REASONS.get(k, k)}×{n}" for k, n in s.reasons.items())) + "</p>")
    others = [q for q in u.questions if q not in s.wrong_qids]
    if others:
        h.append('<p class="small">같은 목표의 다른 문항(다음 날 이후 풀면 「이후 적용」 확인): '
                 + ", ".join(f'<a href="{weblink(cfg, q=q)}">{esc(q)}</a>' for q in others) + "</p>")

    if c:
        for sec in c.get("sections") or []:
            h.append(f'<div class="{"deep" if sec["deep"] else ""}"><h3>{esc(sec["title"])}</h3>{stack_wide_tables(sec["html"])}</div>')
        if c.get("criteria"):
            h.append("<h3>기준·권고 — 대상·종류·예외·출처</h3>")
            srcs = {str(x.get("id")): x for x in c.get("sources") or []}
            for cr in c["criteria"]:
                src = srcs.get(str(cr.get("source")), {})
                exams = " · ".join(str(e).upper() for e in cr.get("exams") or [])
                h.append('<dl class="crit">'
                         f'<dt>{esc(cr.get("name"))} — {esc(cr.get("kind"))}</dt><dd></dd>'
                         f'<dt>대상 집단</dt><dd>{esc(cr.get("population"))}</dd>'
                         f'<dt>내용</dt><dd>{esc(cr.get("statement"))}</dd>'
                         + (f'<dt>예외·한계</dt><dd>{esc(cr.get("exceptions"))}</dd>' if cr.get("exceptions") else "")
                         + f'<dt>근거 구분 · 시험</dt><dd>{esc(BASIS.get(cr.get("basis"), cr.get("basis")))} · {esc(exams)}</dd>'
                         f'<dt>발행 기관·연도 · 확인일</dt><dd>{esc(src.get("org"))} {esc(src.get("year"))} · 확인 {esc(src.get("checked_at"))}</dd>'
                         "</dl>")
        if c.get("geo"):
            spec = c["diagram"]
            h.append("<h3>임상 판단 도식 — 일반 구조</h3>")
            h.append('<p class="small muted">이 책에는 일반 구조만 싣는다. 각 문항의 경로·선택한 오답과 갈리는 곳은 앱의 문항 화면에서 본다.'
                     ' 모든 노드 윗줄에 종류(판단·처치·추가 정보 필요·결론)가 글자로 적혀 있다.</p>')
            h.append(f'<figure class="dia"><figcaption>[도식] {esc(spec.get("title"))}</figcaption>'
                     f'{dd.to_svg(c["geo"], None, dd.LIGHT)}<figcaption>도식 끝 — 글로 읽는 판은 아래</figcaption></figure>')
            h.append('<ol class="steps">' + "".join(
                f'<li value="{st["num"]}"><b>[{esc(st["kind"])}]</b> {esc(st["text"])}'
                + ("".join(f'<br>· {esc(b["label"])} → {b["to"]}번' for b in st["branches"]) if len(st["branches"]) > 1 else
                   ("".join(f' → {b["to"]}번' for b in st["branches"])))
                + "</li>" for st in dd.text_steps(spec)) + "</ol>")
    else:
        h.append("<h3>문항 해설에서 옮긴 내용(임시)</h3>")
        for qid in u.questions:
            q = questions.get(qid, {})
            d = q.get("design") or {}
            h.append(f'<div class="box"><b>{esc(qid)}</b> {esc(q.get("subtopic", ""))}<br>'
                     + (f"핵심 판단: {esc(d.get('summary'))}<br>" if d.get("summary") else "")
                     + f'{esc(q.get("explanation", ""))}</div>')
        h.append('<p class="small muted">이 목표의 정리본이 아직 없다. 다음 정리본 작성 때 이 단원이 정식 단원으로 바뀐다.</p>')

    # 내 반복 혼동 — 문항마다의 혼동을 그대로 보존
    h.append("<h3>내 반복 혼동</h3>")
    agg: dict[tuple[str, str], int] = {}
    for ch in s.chosen:
        agg[(ch["qid"], ch["text"])] = agg.get((ch["qid"], ch["text"]), 0) + 1
    if agg:
        for (qid, text), n in agg.items():
            dist = _dist_for(questions.get(qid, {}), text)
            h.append(f'<div class="err"><b>{esc(text)}</b> — {n}회 ({esc(qid)})'
                     + (f'<br>가르는 소견: {esc(dist.get("discriminator"))}' if dist else "")
                     + (f'<br>이 보기가 맞는 경우: {esc(dist.get("when_right"))}' if dist and dist.get("when_right") else "") + "</div>")
    else:
        h.append('<p class="small muted">오답 기록은 없고 표시만 있다.</p>')
    if s.memo:
        h.append(f'<div class="memo"><b>내 메모</b> <span class="small muted">(직접 쓴 것 — 자동 생성·수정 안 함, {esc(s.memo_t[:10])})</span><br>{esc(s.memo)}</div>')

    if c and c.get("checks"):
        h.append("<h3>스스로 묻기</h3><ol>")
        for i, ck in enumerate(c["checks"], 1):
            aid = f"{u.anchor}-a{i}"
            answers.append((aid, u, i, ck))
            h.append(f'<li>{esc(ck.get("q"))} <a class="small" href="#{aid}">답 보기 ›</a></li>')
        h.append("</ol>")
        if c.get("variants"):
            h.append(f'<p class="small">변형 문제 {len(c["variants"])}개는 앱의 <a href="{weblink(cfg, concept=u.key)}">개념 복습</a>에서 푼다 '
                     "(다음 날 이후 맞히면 「이후 적용 성공」).</p>")
    if c and c.get("see_also"):
        names = sorted({book_of(t, {"books": book_names}) for t in c["see_also"]})
        h.append(f'<p class="small">함께 볼 과: {esc(" · ".join(names))}</p>')

    if c:
        h.append("<h3>출처와 마지막 검토일</h3><ul class=\"small\">")
        for src in c.get("sources") or []:
            url = safe_url(src.get("url")) or (f"https://doi.org/{src['doi']}" if src.get("doi") else "")
            h.append(f'<li>{esc(src.get("org"))}. {esc(src.get("title"))}. {esc(src.get("citation") or src.get("year"))}'
                     + (f' <a href="{esc(url)}">{esc(url)}</a>' if url else "")
                     + f'<br>확인 {esc(src.get("checked_at"))} — {esc(src.get("checked"))}</li>')
        h.append(f'</ul><p class="small muted">정리본 v{esc(c.get("version"))} · 최근 갱신 {esc(c.get("updated", c.get("date")))} · '
                 f'검토 상태 {esc(c.get("review_status"))}' + (f' ({esc(c.get("reviewed_by"))})' if c.get("reviewed_by") else "")
                 + f' · 원본 {esc(c.get("path"))}</p>')
    h.append("</section>")
    return "".join(h)


def _dist_for(q: dict, chosen_text: str) -> dict | None:
    """고른 보기 글자로 문항의 distractors 항목을 찾는다(보기 순서가 바뀌어도 글자로 맞춘다)."""
    dist = q.get("distractors") if isinstance(q.get("distractors"), dict) else None
    if not dist:
        return None
    for i, opt in enumerate(q.get("choices") or []):
        o = re.sub(r"^[A-E][.)]\s*", "", str(opt)).strip()
        if o == str(chosen_text).strip():
            return dist.get("ABCDE"[i])
    return None


def book_html(title: str, units: list[Unit], pending: list, cfg: dict, questions: dict, meta: dict,
              pagemap: dict[str, int] | None, fonts: dict, changes: list[str]) -> str:
    answers: list = []
    body_units = "".join(unit_html(u, cfg, questions, answers, cfg.get("books") or {}) for u in units)
    counts = {k: sum(1 for u in units if u.state.status == k) for k in ll.STATUS}
    pg = lambda a: str(pagemap.get(a, "")) if pagemap else "…"
    h = [f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>{esc(cfg["title"])} — {esc(title)}</title>'
         f"<style>{CSS % fonts}</style></head><body>"]
    h.append(f'<section class="cover"><h1>{esc(title)}</h1>'
             f'<p class="meta">{esc(cfg["title"])} · 판 v{meta["version"]} · {esc(meta["date"])} 생성</p>'
             f'<div class="box"><b>이 책에 든 것</b><br>단원 {len(units)}개 — 복습 필요 {counts["need"]} · 복습 중 {counts["doing"]} · '
             f'재확인 완료 {counts["done"]}' + (f" · 정리본 없는 오답 {len(pending)}문항" if pending else "") + "</div>"
             '<div class="box small"><b>읽는 법</b><br>'
             "· 상태: <b>복습 필요</b> = 틀렸고 아직 후속 확인 없음 / <b>복습 중</b> = 인출 확인·변형 문제 등을 시작함 / "
             "<b>재확인 완료</b> = 다음 날 이후 같은 목표의 다른 문항·변형 문제를 맞힘. 완료 단원도 지우지 않는다.<br>"
             "· 해설 열람 · 정리본 읽음 · 이해 표시 · 이후 적용 성공은 서로 다른 증거다. 이 PDF 를 연 것만으로는 아무것도 완료되지 않는다.<br>"
             "· 「의학적 내용 검토 전」 단원은 자동 형식 검사만 통과했다. 기준·권고는 발행 기관·연도·확인일과 함께 읽는다.<br>"
             "· 도식: 모든 칸 윗줄의 글자(판단·평가·처치·추가 정보 필요·결론)로 종류를 구분한다. 색에 기대지 않는다.</div>"
             '<p class="small muted">최신본은 같은 파일로 갱신된다. 필기는 사본(또는 archive/ 의 날짜별 판)에 하길 권한다 — '
             "최신본에 직접 필기가 감지되면 자동 갱신이 그 파일을 덮어쓰지 않고 멈춘다.</p></section>")
    # 차례
    h.append('<section class="page"><h2 id="toc">차례</h2><ul class="toc">')
    h.append(f'<li><span class="st"></span><a href="#status">상태별 복습 목록</a><span class="pg">{pg("status")}</span></li>')
    for u in units:
        h.append(f'<li><span class="st">{status_tag(u.state.status)}</span><a href="#{u.anchor}">{esc(u.title)}</a>'
                 f'<span class="pg">{pg(u.anchor)}</span></li>')
    if pending:
        h.append(f'<li><span class="st"></span><a href="#pending">정리본 없는 오답(연결 대기)</a><span class="pg">{pg("pending")}</span></li>')
    h.append(f'<li><span class="st"></span><a href="#answers">스스로 묻기 답</a><span class="pg">{pg("answers")}</span></li>')
    h.append(f'<li><span class="st"></span><a href="#changes">이번 판에서 바뀐 것</a><span class="pg">{pg("changes")}</span></li></ul></section>')
    # 상태별 목록(PDF 안의 필터)
    h.append('<section class="page" id="status"><h2>상태별 복습 목록</h2><p class="small muted">우선순위(반복 오답·후속 확인 실패·표시)가 높은 순. 정해진 복습 간격은 두지 않는다.</p>')
    for st in ("need", "doing", "done"):
        us = sorted([u for u in units if u.state.status == st], key=lambda u: -u.state.priority)
        h.append(f"<h3>{esc(ll.STATUS[st])} ({len(us)})</h3>")
        h.append("<ul>" + ("".join(f'<li><a href="#{u.anchor}">{esc(u.title)}</a> <span class="small muted">오답 {u.state.wrongs} · '
                                   f'후속 확인 실패 {u.state.follow_fails} · {pg(u.anchor)}쪽</span></li>' for u in us) or "<li class='muted'>없음</li>") + "</ul>")
    h.append("</section>")
    h.append(body_units)
    if pending:
        h.append('<section class="page" id="pending"><h2>정리본 없는 오답(연결 대기)</h2>'
                 '<p class="small muted">학습 목표(objective)가 아직 붙지 않은 문항이다. 질환명으로 묶지 않고 문항별로 둔다 — 목표가 정해지면 해당 단원으로 옮겨진다.</p>')
        for s, q in pending:
            qid = s.key[2:]
            last = s.chosen[-1] if s.chosen else {}
            h.append(f'<div class="err"><a href="{weblink(cfg, q=qid)}">{esc(qid)}</a> {esc(q.get("subtopic", ""))} · {status_tag(s.status)}'
                     f'<br>{esc(str(q.get("stem", ""))[:160])}…'
                     + (f'<br>고른 답 <b>{esc(last.get("text"))}</b> → 정답 <b>{esc(last.get("answer"))}</b>' if last else "") + "</div>")
        h.append("</section>")
    h.append('<section class="page" id="answers"><h2>스스로 묻기 답</h2>')
    for aid, u, i, ck in answers:
        h.append(f'<div class="box" id="{aid}"><b>{esc(u.title)} — Q{i}</b><br>{esc(ck.get("q"))}<br><br>{esc(ck.get("a"))}'
                 f'<br><a class="small" href="#{u.anchor}">‹ 단원으로</a></div>')
    h.append("</section>")
    h.append('<section class="page" id="changes"><h2>이번 판에서 바뀐 것</h2><ul>'
             + "".join(f"<li>{esc(x)}</li>" for x in (changes or ["첫 판"])) + "</ul></section>")
    h.append("</body></html>")
    return "".join(h)


# ── 렌더링 · 위치 찾기 · 검증 ────────────────────────────────────────
def find_font(paths: list[str]) -> str:
    for p in paths:
        if Path(p).exists():
            return Path(p).resolve().as_uri()
    raise FileNotFoundError(f"한글 글꼴이 없다: {paths}")


def render_pdf(browser, html_text: str, out: Path, footer: str) -> None:
    with tempfile.TemporaryDirectory() as td:
        src = Path(td) / "book.html"
        src.write_text(html_text, encoding="utf-8")
        page = browser.new_page()
        try:
            page.goto(src.as_uri(), wait_until="load")
            page.evaluate("document.fonts.ready")
            page.pdf(path=str(out), format="A4", print_background=True, display_header_footer=True,
                     header_template="<span></span>",
                     footer_template=('<div style="font-family:NanumGothic,\'Noto Sans KR\',sans-serif;font-size:8pt;color:#667;'
                                      f'width:100%;text-align:center">{esc(footer)} · <span class="pageNumber"></span> / '
                                      '<span class="totalPages"></span></div>'),
                     margin={"top": "16mm", "bottom": "18mm", "left": "15mm", "right": "15mm"}, tagged=True, outline=False)
        finally:
            page.close()


def locate(pdf_path: Path, units: list[Unit], has_pending: bool) -> dict[str, int]:
    """각 단원이 시작하는 쪽(1-based). 단원 머리의 「단원 ID <id>」로 찾는다(차례·목록에는 ID 를 싣지 않는다)."""
    import pymupdf
    doc = pymupdf.open(pdf_path)
    pm: dict[str, int] = {}
    texts = [" ".join(p.get_text().split()) for p in doc]
    for u in units:
        needle = f"단원 ID {u.key}"
        for i, t in enumerate(texts):
            if needle in t:
                pm[u.anchor] = i + 1
                break
    heads = {"status": "상태별 복습 목록", "pending": "정리본 없는 오답(연결 대기)",
             "answers": "스스로 묻기 답", "changes": "이번 판에서 바뀐 것"}
    for key, needle in heads.items():
        if key == "pending" and not has_pending:
            continue
        for i, t in enumerate(texts):
            if i >= 2 and t.startswith(needle):        # 각 절은 새 쪽의 첫 줄에서 시작한다(차례 쪽은 「차례」로 시작)
                pm[key] = i + 1
                break
    doc.close()
    return pm


def set_outline(pdf_path: Path, title: str, units: list[Unit], pm: dict[str, int], has_pending: bool, meta: dict) -> None:
    import pymupdf
    doc = pymupdf.open(pdf_path)
    toc = [[1, "표지", 1], [1, "차례", 2], [1, "상태별 복습 목록", pm.get("status", 3)], [1, "단원", pm.get(units[0].anchor, 3) if units else 3]]
    for u in units:
        toc.append([2, f"[{ll.STATUS.get(u.state.status, '')}] {u.title}", pm.get(u.anchor, 1)])
    if has_pending:
        toc.append([1, "정리본 없는 오답(연결 대기)", pm.get("pending", 1)])
    toc += [[1, "스스로 묻기 답", pm.get("answers", 1)], [1, "이번 판에서 바뀐 것", pm.get("changes", 1)]]
    doc.set_toc(toc)
    doc.set_metadata({"title": f"{title} — MedKOS 학습서 v{meta['version']}", "author": "MedKOS",
                      "subject": f"과별 누적 학습서 {meta['date']}", "creator": "MedKOS build_books.py",
                      "keywords": ", ".join(u.key for u in units)})
    tmp = pdf_path.with_suffix(".tmp.pdf")
    doc.save(tmp, garbage=3, deflate=True)
    doc.close()
    tmp.replace(pdf_path)


def validate_pdf(pdf_path: Path, title: str, units: list[Unit], pm: dict[str, int], has_pending: bool) -> list[str]:
    import pymupdf
    errs: list[str] = []
    doc = pymupdf.open(pdf_path)
    if doc.page_count < 3:
        errs.append(f"쪽 수가 너무 적다({doc.page_count})")
    # 글꼴 임베드
    notemb = set()
    for p in doc:
        for f in p.get_fonts(full=True):
            if f[1] in ("n/a", "") and f[2] not in ("Type3",):
                notemb.add(f[3])
    if notemb:
        errs.append(f"임베드되지 않은 글꼴: {sorted(notemb)}")
    # 한글 글자 추출·검색
    all_text = " ".join(" ".join(p.get_text().split()) for p in doc)
    if title.split()[0] not in all_text:
        errs.append("책 이름을 글자로 찾지 못했다(이미지 PDF?)")
    for u in units:
        if u.anchor not in pm:
            errs.append(f"단원 위치를 찾지 못했다: {u.key}")
            continue
        page = doc[pm[u.anchor] - 1]
        probe = re.sub(r"\s+", " ", u.title)[:12]
        if not page.search_for(probe):
            errs.append(f"단원 첫 쪽에서 제목 검색 실패: {probe}")
    order = [pm[u.anchor] for u in units if u.anchor in pm]
    if order != sorted(order):
        errs.append("단원 쪽 순서가 차례와 다르다")
    # 차례 링크(2쪽~)가 단원 쪽을 가리키는가
    targets = []
    toc_end = (pm.get("status") or 3) - 1                  # 차례는 2쪽부터 상태별 목록 앞까지
    for pno in range(1, max(2, toc_end)):
        for ln in doc[pno].get_links():
            # Chromium 은 이름 붙은 목적지(LINK_NAMED)로 만든다 — PyMuPDF 가 쪽으로 풀어 준다
            if ln.get("kind") in (pymupdf.LINK_GOTO, pymupdf.LINK_NAMED) and ln.get("page", -1) >= 0:
                targets.append((pno, ln["from"].y0, ln["page"] + 1))
    targets.sort()
    want = [pm.get("status")] + [pm.get(u.anchor) for u in units]
    got = [t[2] for t in targets][:len(want)]
    if got != want:
        errs.append(f"차례 링크가 어긋난다: 기대 {want} / 실제 {got}")
    # 책갈피
    toc = doc.get_toc()
    if len([t for t in toc if t[0] == 2]) != len(units):
        errs.append(f"책갈피 단원 수 {len([t for t in toc if t[0] == 2])} ≠ {len(units)}")
    # 글자가 쪽 밖으로 나가지 않는가
    for p in doc:
        r = p.rect
        for b in p.get_text("blocks"):
            if b[2] > r.x1 - 5 or b[0] < 5 or b[3] > r.y1 - 2:
                errs.append(f"{p.number + 1}쪽 글자가 쪽 가장자리를 넘는다: {b[4][:30]!r}")
                break
    # 도식은 한 쪽 안에(머리 캡션과 끝 캡션이 같은 쪽)
    for u in units:
        if u.concept and u.concept.get("geo"):
            head = f"[도식] {u.concept['diagram'].get('title')}"[:18]
            heads = [p.number for p in doc if head in " ".join(p.get_text().split())]
            ends = [p.number for p in doc if "도식 끝 — 글로 읽는 판은 아래" in p.get_text() and p.number in heads]
            if not heads or not ends:
                errs.append(f"도식이 한 쪽에 온전히 있지 않다: {u.key}")
    doc.close()
    return errs


def preview(pdf_path: Path, out_dir: Path, pages: list[int], zoom: float = 1.4) -> list[Path]:
    import pymupdf
    out_dir.mkdir(parents=True, exist_ok=True)
    doc = pymupdf.open(pdf_path)
    res = []
    for n in pages:
        if 1 <= n <= doc.page_count:
            p = out_dir / f"{pdf_path.stem}_p{n:02d}.png"
            doc[n - 1].get_pixmap(matrix=pymupdf.Matrix(zoom, zoom)).save(p)
            res.append(p)
    doc.close()
    return res


# ── 전체 목차 ───────────────────────────────────────────────────────
def index_html(books_meta: list[dict], cfg: dict, fonts: dict, date: str) -> str:
    h = [f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>{esc(cfg["title"])} 전체 목차</title>'
         f"<style>{CSS % fonts}</style></head><body><h1>{esc(cfg['title'])} — 전체 목차</h1>"
         f'<p class="muted">{esc(date)} 기준 · 책 {len(books_meta)}권</p>']
    for b in books_meta:
        h.append(f'<h3>{esc(b["title"])} <span class="small muted">({esc(b["file"])} · v{b["version"]} · {b["pages"]}쪽)</span></h3><ul>')
        for u in b["units"]:
            h.append(f'<li>{status_tag(u["status"])}{esc(u["title"])} <span class="small muted">{u["page"]}쪽 · '
                     f'<a href="{weblink(cfg, concept=u["key"])}">앱에서 열기</a></span></li>')
        h.append("</ul>")
    h.append("</body></html>")
    return "".join(h)


# ── 실행 ───────────────────────────────────────────────────────────
def build(cfg: dict, events: list[dict], state_dir: Path, out_dir: Path, force: bool = False,
          only: str | None = None, want_preview: bool = False, fail_on: str | None = None) -> dict:
    started = now_kst()
    date = started.strftime("%Y-%m-%d")
    manifest_path = state_dir / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8")) if manifest_path.exists() else {"books": {}}
    run: dict[str, Any] = {"started": started.isoformat(timespec="seconds"), "built": [], "skipped": [], "failed": {},
                           "retry": [], "previews": [], "validation": {}}
    concepts, cerrs = load_concepts()
    questions = load_questions()
    S = ll.states(events)
    source_state = json.loads(SOURCE_CHECKS.read_text(encoding="utf-8")) if SOURCE_CHECKS.exists() else {}
    books = plan(concepts, questions, S, cfg, source_state)
    run["concept_errors"] = cerrs
    fonts = {"regular": find_font(cfg["fonts"]["regular"]), "bold": find_font(cfg["fonts"]["bold"])}
    out_dir.mkdir(parents=True, exist_ok=True)
    todo = []
    for b in books.values():
        vols = volumes(b, cfg)
        for vi, (title, units) in enumerate(vols):
            pending = b.pending if vi == len(vols) - 1 else []
            if only and only not in (b.name, title):
                continue
            hsh = volume_hash(title, units, pending, cfg)
            prev = manifest["books"].get(title, {})
            fname = f"MedKOS_학습서_{slug(title)}.pdf"
            same = prev.get("hash") == hsh
            uploaded = (prev.get("drive") or {}).get("version") == prev.get("version")
            if not force and same and ((out_dir / fname).exists() or uploaded):
                run["skipped"].append(title)          # 변화 없음(최신본이 로컬 또는 드라이브에 있다)
                continue
            todo.append((title, units, pending, hsh, prev, fname))
    if not todo:
        run["result"] = "skipped"
        run["finished"] = now_kst().isoformat(timespec="seconds")
        _write_run(state_dir, run)
        return run
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        try:
            for title, units, pending, hsh, prev, fname in todo:
                try:
                    if fail_on and fail_on == title:
                        raise RuntimeError("시험용 강제 실패(--fail-on)")
                    # 내용이 같으면(업로드 재시도·새 러너) 판 번호를 올리지 않는다 — 되풀이해도 같은 결과
                    version = int(prev.get("version", 0)) + (0 if prev.get("hash") == hsh and prev.get("version") else 1)
                    meta = {"version": version, "date": date}
                    changes = prev.get("changes") if prev.get("hash") == hsh and prev.get("changes") else _changes(prev, units, pending)
                    footer = f"{title} · v{version} · {date}"
                    tmp = out_dir / (fname + ".building.pdf")
                    html1 = book_html(title, units, pending, cfg, questions, meta, None, fonts, changes)
                    render_pdf(browser, html1, tmp, footer)
                    pm = locate(tmp, units, bool(pending))
                    html2 = book_html(title, units, pending, cfg, questions, meta, pm, fonts, changes)
                    render_pdf(browser, html2, tmp, footer)
                    pm2 = locate(tmp, units, bool(pending))
                    if pm2 != pm:                      # 쪽 번호를 넣어 흐름이 바뀌었으면 한 번 더
                        html2 = book_html(title, units, pending, cfg, questions, meta, pm2, fonts, changes)
                        render_pdf(browser, html2, tmp, footer)
                        pm = locate(tmp, units, bool(pending))
                    set_outline(tmp, title, units, pm, bool(pending), meta)
                    errs = validate_pdf(tmp, title, units, pm, bool(pending))
                    run["validation"][title] = errs
                    if errs:
                        raise RuntimeError("검증 실패: " + "; ".join(errs[:6]))
                    final = out_dir / fname
                    tmp.replace(final)                 # 검증을 통과한 뒤에만 최신본을 바꾼다
                    import pymupdf
                    with pymupdf.open(final) as d:
                        pages = d.page_count
                    manifest["books"][title] = {
                        "hash": hsh, "version": version, "date": date, "file": fname, "pages": pages,
                        "units": {u.key: {"title": u.title, "status": u.state.status, "page": pm.get(u.anchor),
                                          "concept_hash": (u.concept or {}).get("hash"),
                                          "concept_version": (u.concept or {}).get("version"), "wrongs": u.state.wrongs}
                                  for u in units},
                        "pending": [s.key for s, _ in pending],
                        "drive": prev.get("drive"), "archive": prev.get("archive", []),
                        "changes": changes,
                    }
                    run["built"].append(title)
                    if want_preview:
                        pgs = [1, 2, 3] + sorted({v for k, v in pm.items() if k.startswith("u-")})
                        pgs += [p + 1 for p in pgs[3:]]
                        run["previews"] += [str(p) for p in preview(final, out_dir / "_preview", sorted(set(pgs)))]
                except Exception as e:                  # 이 책만 실패 — 이전 PDF·기록은 그대로
                    run["failed"][title] = f"{type(e).__name__}: {e}"
                    run["retry"].append(title)
                    run.setdefault("trace", {})[title] = traceback.format_exc()[-1500:]
                    (out_dir / (fname + ".building.pdf")).unlink(missing_ok=True)
            # 전체 목차(책이 하나라도 새로 만들어졌을 때)
            if run["built"]:
                metas = []
                for t, m in sorted(manifest["books"].items()):
                    metas.append({"title": t, "file": m["file"], "version": m["version"], "pages": m.get("pages", "?"),
                                  "units": [{"key": k, **v} for k, v in m["units"].items()]})
                idx = out_dir / "MedKOS_학습서_전체목차.pdf"
                tmp = out_dir / "index.building.pdf"
                render_pdf(browser, index_html(metas, cfg, fonts, date), tmp, f"전체 목차 · {date}")
                tmp.replace(idx)
                manifest["index"] = {"file": idx.name, "date": date, "drive": (manifest.get("index") or {}).get("drive")}
        finally:
            browser.close()
    manifest["updated"] = date
    state_dir.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
    run["result"] = "failed" if run["failed"] and not run["built"] else ("partial" if run["failed"] else "ok")
    run["finished"] = now_kst().isoformat(timespec="seconds")
    _write_run(state_dir, run)
    _append_changelog(state_dir, run, manifest, date)
    return run


def _changes(prev: dict, units: list[Unit], pending: list) -> list[str]:
    if not prev:
        return [f"첫 판 — 단원 {len(units)}개"]
    old = prev.get("units") or {}
    out = []
    for u in units:
        o = old.get(u.key)
        if not o:
            out.append(f"새 단원: {u.title}")
            continue
        if o.get("concept_version") != (u.concept or {}).get("version") or o.get("concept_hash") != (u.concept or {}).get("hash"):
            out.append(f"내용 갱신: {u.title} (v{o.get('concept_version')} → v{(u.concept or {}).get('version')})")
        if o.get("status") != u.state.status:
            out.append(f"상태 변경: {u.title} — {ll.STATUS.get(o.get('status'), o.get('status'))} → {ll.STATUS.get(u.state.status)}")
        if o.get("wrongs", 0) < u.state.wrongs:
            out.append(f"오답 추가: {u.title} ({o.get('wrongs', 0)} → {u.state.wrongs})")
    gone = [v.get("title", k) for k, v in old.items() if k not in {u.key for u in units}]
    out += [f"이 책에서 빠짐(다른 권으로 이동 등): {t}" for t in gone]
    if len(pending) != len(prev.get("pending") or []):
        out.append(f"정리본 없는 오답 {len(prev.get('pending') or [])} → {len(pending)}문항")
    return out or ["표시·기록만 바뀜"]


def _write_run(state_dir: Path, run: dict) -> None:
    state_dir.mkdir(parents=True, exist_ok=True)
    (state_dir / "last_run.json").write_text(json.dumps(run, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")


def _append_changelog(state_dir: Path, run: dict, manifest: dict, date: str) -> None:
    if not run["built"] and not run["failed"]:
        return
    lines = [f"\n## {run['started']}\n"]
    for t in run["built"]:
        m = manifest["books"][t]
        lines.append(f"- {t} v{m['version']} ({m['pages']}쪽): " + "; ".join(m.get("changes") or []))
    for t, e in run["failed"].items():
        lines.append(f"- ✗ {t}: {e} — 이전 판 유지, 다음 실행에서 재시도")
    p = state_dir / "CHANGELOG.md"
    head = "" if p.exists() else "# 과별 학습서 판 기록(build_books.py 가 덧붙인다)\n"
    with p.open("a", encoding="utf-8", newline="\n") as f:
        f.write(head + "\n".join(lines) + "\n")


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--only")
    ap.add_argument("--events", help="학습 기록 파일(기본: state/learning_sync/events.json + 수신함)")
    ap.add_argument("--state-dir", default=str(STATE_DIR))
    ap.add_argument("--out")
    ap.add_argument("--preview", action="store_true")
    ap.add_argument("--upload", action="store_true", help="검증을 통과한 책을 Google Drive 에 갱신")
    ap.add_argument("--fail-on", help=argparse.SUPPRESS)
    a = ap.parse_args(argv)
    cfg = load_config()
    if a.events:
        events = ll.read_events(Path(a.events))
    else:
        import drive_books                     # 드라이브 수신함(앱에서 내보낸 기록) → state/learning_inbox → 병합
        print("수신함:", drive_books.pull_inbox(cfg, ll.INBOX))
        ll.sync_inbox()
        events = ll.read_events(ll.SYNC_FILE)
    out_dir = Path(a.out) if a.out else ROOT / cfg.get("out_dir", "build/books")
    state_dir = Path(a.state_dir)
    run = build(cfg, events, state_dir, out_dir, force=a.force, only=a.only, want_preview=a.preview, fail_on=a.fail_on)
    print(json.dumps({k: run[k] for k in ("result", "built", "skipped", "failed", "retry")}, ensure_ascii=False, indent=1))
    for t, errs in run.get("validation", {}).items():
        print(f"  검증 {t}: {'통과' if not errs else errs}")
    if a.upload:
        import drive_books
        up = drive_books.upload(cfg, state_dir, out_dir, run)
        print(json.dumps(up, ensure_ascii=False, indent=1))
        if up.get("result") == "failed":
            return 1
    return 1 if run["result"] in ("failed",) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
