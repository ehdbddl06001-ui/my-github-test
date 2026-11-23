"""build_books.py — 오답·표시가 쌓인 학습 목표를 과별 누적 PDF 학습서로 만든다(아이패드 정독용).

판형 2 (2026-09-18 사용자 지시 — 이전 PDF 구성 요구보다 우선)
- 목적: 부족한 주제의 **의학 내용**을 밀도 있게 읽는다. 개념·병태생리·기준·감별·검사 해석·치료·알고리즘 중심.
- PDF 에서 뺀다(앱·원본 데이터에는 그대로 남는다): 단원이 들어온 이유·오답 날짜·문항 번호·선택 기록, 해설 열람·
  정리본 읽음·복습 상태, 스스로 묻기·정답·변형 문제 안내, 내용 변경이 없는 변경 이력, 내부 ID·파일 경로·기술 설명,
  반복되는 사용법. 오답에서 드러난 혼동은 일반화해 「혼동하기 쉬운 점」으로 본문에 넣는다(왜 골랐는지 추측하지 않는다).
- 역할 구분: 요약 = 전체 관계, 본문 = 이유, 표 = 차이 비교, 도식 = 흐름. 도식 아래에 노드를 다시 나열하지 않고
  그림만으로 전달되지 않는 조건·예외(`diagram_notes`)만 쓴다(글 대체본은 앱에 있다).
- 권고는 세로 카드 대신 비교표. 진단 기준·중증도·치료 기준을 종류별 표로 나누고, 다른 지침을 설명 없이 합치지 않는다.
- A4 가로 2단(CSS 다단). 넓은 표·큰 도식만 두 단 전체(column-span). 단원·소제목마다 강제 쪽 나눔 없음,
  나눔 제어는 제목-첫 문단·표의 행·작은 그림 단위로만. 큰 표는 행 경계에서 나뉘고 열 제목이 반복된다.
- 근거는 번호([n 쪽·절])로 본문에 달고 단원 끝에 정리. 원문 본문과 대조하지 않은 근거에는 †.
- 판 번호·갱신일은 머리줄·꼬리말로 작게. 실질 내용 변경만 책 끝 「이번 판의 내용 변경」에(없으면 쓰지 않는다).

그 밖(판형 1과 같음): 과별 책·권 나눔·전체 목차, 렌더 후 검증(글꼴 임베드·한글 검색·차례 링크·책갈피·쪽 경계·
도식 한 쪽·고립된 제목·빈 쪽), 바뀐 것이 없으면 건너뜀, 실패하면 이전 PDF 유지, 되풀이해도 같은 결과.

배치(2026-11-23, 판형 13): 도식 · 그림의 자리는 책을 Chromium 에 한 번 올려 재서 고르고(book_layout.py — 선택지마다
책 전체를 PDF 로 다시 그리던 것을 바꿨다), PDF 는 고른 배치로 한 번 그려 검증한다. 측정이 예측하지 못한 배치 오류는
그 둘레만 PDF 로 고치고, 측정이 안 되면 그전 탐색으로 간다(`--layout search` 로 고를 수도 있다).

사용:
  python pipelines/build_books.py                       # 바뀐 책만 만들고 검증(업로드 없음)
  python pipelines/build_books.py --upload              # + Google Drive 갱신(drive_books.py)
  python pipelines/build_books.py --force --only 신장내과
  python pipelines/build_books.py --force --only 신장내과 --layout search   # 그전 방식(선택지마다 PDF 로 — 느리다)
  python pipelines/build_books.py --events <학습기록.json> --state-dir <임시> --out <임시> --preview
"""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import sys
import tempfile
import traceback
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import yaml

import book_layout as bl
import decision_diagram as dd
import english_terms as et
import learning_log as ll
import note_parts as parts
import outline as ol
from concepts import BASIS, linked_questions, load_concepts, load_questions, render_cites, root_supports, safe_url, source_numbers

ROOT = Path(__file__).resolve().parent.parent
CONFIG = Path(__file__).with_name("books_config.yaml")
STATE_DIR = ROOT / "state" / "books"
SOURCE_CHECKS = ROOT / "state" / "source_checks.json"
KST = timezone(timedelta(hours=9))
VERIFIED_LABEL = {"text": "본문 대조", "abstract": "초록만 대조†", "citation": "서지만 확인†"}

# 판형 수치(mm·pt). 실제 렌더를 보고 정했다 — 페이지를 줄이려고 본문 글자를 더 줄이지 않는다.
PAGE = dict(w=210, h=297, mt=9, mb=11, ml=10, mr=10, gap=6)       # 2026-09-27 A4 세로 2단(해리슨식) — 아이패드에서 확대해 읽는다
COLW = (PAGE["w"] - PAGE["ml"] - PAGE["mr"] - PAGE["gap"]) / 2      # 한 단 92 mm — 표·그림은 모두 이 폭 안
BODY_PT, LINE = 8.4, 1.36
MM_PX = 96 / 25.4
DIAGRAM_MAX_SCALE = 0.8           # 도식 글자 최대 약 7.8pt(본문 8.4pt 보다 조금 작게)
DIA_FLOOR_PT = 5.2                # 한 단 도식 글자 하한(작게 두고 확대 — 벡터라 선명)
DIA_FULL_FLOOR_PT = 6.2           # 두 단 전체 도식 글자 하한
DIA_SHRINK_FLOOR_PT = 5.6         # 쪽 맞춤 축소의 하한
CAPTION_PX = 36
# 그림(2026-09-27) — 한 단 그림은 「그림 왼쪽 · 설명 오른쪽」, 심전도는 두 단 전체(12유도는 폭이 있어야 읽힌다).
# 크기 상한은 단 높이(189 mm)의 약 35 % — 그림이 단 끝에 못 들어가 다음 단으로 넘어가도 빈 공간이 30 % 기준을 넘지 않게.
FIG_MAX_H = 80.0                  # 한 단 그림 최대 높이(mm) — 폭은 한 단 전체
FIG_MIN = {"column": (38.0, 16.0)}    # 인쇄 뒤 이보다 작으면 읽기 어렵다(검증)
FIG_BASIS = {"dataset_expert": "전문가 판정 데이터셋 라벨", "published_figure": "동료 심사 논문의 그림 설명"}


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
    key: str                      # 개념 id(목표) — 안정 ID(PDF 에는 싣지 않는다)
    book: str
    concept: dict | None          # None 이면 「정리본 준비 중」 임시 단원
    state: ll.State
    questions: list[str]
    title: str = ""
    flags: list[str] = field(default_factory=list)   # 출처 개정 확인 필요 등
    slot: str = ""                # 기본틀(content/outline/subjects.yaml)의 슬롯 id — 책 안의 자리
    group: str = ""               # 그 슬롯이 속한 묶음(해리슨 절 이름 등) — 차례의 중간 머리글
    # 판형 12 — 다른 단원과의 이음: series(같은 질환의 단원들) · roots(기초 뿌리) · supports(기초 단원이 받치는 임상 단원).
    # 항목마다 {key, title, kind, book} — 같은 책이면 쪽으로 가는 링크, 다른 책이면 책 이름을 적는다.
    links: dict = field(default_factory=dict)

    @property
    def anchor(self) -> str:
        return "u-" + re.sub(r"[^a-z0-9]+", "-", self.key.lower()).strip("-")


@dataclass
class Book:
    name: str
    units: list[Unit] = field(default_factory=list)
    pending: list[tuple[ll.State, dict]] = field(default_factory=list)   # 목표 없는 문항 오답 — PDF 에 싣지 않음(앱에 있음)
    elsewhere: list[tuple[str, str]] = field(default_factory=list)       # 학문별 책: 다른 책에 실린 그 학문 단원 (제목, 책)


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
            q0 = next((questions[q] for q in s.qids if q in questions), {})
            if c:
                name, title = book_of(c.get("topic"), cfg), str(c.get("title"))
            else:
                name = book_of(q0.get("topic"), cfg)
                title = str(q0.get("subtopic") or q0.get("topic") or "정리본 준비 중")
            u = Unit(key=s.objective, book=name, concept=c, state=s, questions=links.get(s.objective, list(s.qids)), title=title,
                     slot=str((c or {}).get("outline") or ""))
            if c:
                for src in c.get("sources") or []:
                    st = source_state.get(source_key(src)) or {}
                    if st.get("status") in ("changed", "failed"):
                        u.flags.append(f"출처 개정 확인 필요 — {src.get('org')} {src.get('year')}: {st.get('note', '')}")
            books.setdefault(name, Book(name)).units.append(u)
        else:
            q = questions.get(key[2:], {})
            books.setdefault(book_of(q.get("topic"), cfg), Book(book_of(q.get("topic"), cfg))).pending.append((s, q))
    # 오답과 연결되지 않은 정리본(기본틀 빈칸 채우기·예전 시연 단원)도 싣는다 — 2026-09-22 사용자 지시로
    # 「학습서」와 「학습서_검증」을 한 벌로 합쳤다. 학습서는 오답 목록이 아니라 과별 교과서처럼 쌓인다.
    if cfg.get("include_all_concepts", True):
        have = {u.key for b in books.values() for u in b.units}
        for cid, c in concepts.items():
            if cid in have:
                continue
            name = book_of(c.get("topic"), cfg)
            u = Unit(key=cid, book=name, concept=c, state=ll.State(key=cid, objective=cid),
                     questions=links.get(cid, []), title=str(c.get("title")), slot=str(c.get("outline") or ""))
            for src in c.get("sources") or []:
                st = source_state.get(source_key(src)) or {}
                if st.get("status") in ("changed", "failed"):
                    u.flags.append(f"출처 개정 확인 필요 — {src.get('org')} {src.get('year')}: {st.get('note', '')}")
            books.setdefault(name, Book(name)).units.append(u)
    # 기초의학 학문별 책(2026-11-21) — ① 전공 교과서와 대조하지 않은 기초 단원은 머리에 표시한다
    # ② 임상 책에 실린 정리본이 학문 꼬리표(discipline)를 달고 있으면 그 학문 책의 목차 쪽에 제목만 적는다(본문은 한 책에만).
    dmap = cfg.get("disciplines") or {}
    for b in books.values():
        for u in b.units:
            c = u.concept or {}
            if c.get("layer") == "basic" and c.get("textbook_check") != "checked":
                u.flags.append("전공 교과서 미대조")
    for cid, c in sorted(concepts.items()):
        home = dmap.get(str(c.get("discipline") or ""))
        at = book_of(c.get("topic"), cfg)
        if home and home != at and home in books and at in books:
            books[home].elsewhere.append((str(c.get("title")), at))
    for b in books.values():
        b.elsewhere.sort(key=lambda x: (x[1], x[0]))
    # 판형 12 — 단원끼리의 이음(같은 질환 · 기초 뿌리 · 받치는 임상 단원). 원고를 고치지 않고 id · roots 에서 계산한다.
    where = {u.key: b.name for b in books.values() for u in b.units}
    ser, sup = parts.series(concepts), root_supports(concepts)
    ref = lambda cid: {"key": cid, "title": str(concepts[cid].get("title")), "kind": str(concepts[cid].get("objective_kind") or ""),
                       "book": where.get(cid, "")}
    for b in books.values():
        for u in b.units:
            c = u.concept or {}
            lk = {"series": [ref(x["id"]) for x in ser.get(u.key, []) if x["id"] in concepts],
                  "roots": [ref(r) for r in c.get("roots") or [] if r in concepts],
                  "supports": [ref(x) for x in sup.get(u.key, []) if x in concepts] if c.get("layer") == "basic" else []}
            u.links = {k: v for k, v in lk.items() if v}
    # 단원 순서 = 기본틀(해리슨 서술 순서). 배치되지 않은 단원은 맨 뒤에 제목순으로 남는다.
    slots = ol.index(ol.load()[0])
    for b in books.values():
        for u in b.units:
            u.group = (slots.get(u.slot).part if slots.get(u.slot) else "") or ""
        b.units.sort(key=lambda u: (*ol.order_key(u.slot, slots), u.title, u.key))
    return {k: b for k, b in books.items() if b.units}      # 정리본 단원이 없는 책은 만들지 않는다


def volumes(book: Book, cfg: dict) -> list[tuple[str, list[Unit]]]:
    n = max(1, int(cfg.get("volume_max_units") or 40))
    if len(book.units) <= n:
        return [(book.name, book.units)]
    return [(f"{book.name} {i // n + 1}권", book.units[i:i + n]) for i in range(0, len(book.units), n)]


# ── 오답에서 드러난 혼동 → 일반화한 「혼동하기 쉬운 점」 ────────────────
def _dist_for(q: dict, chosen_text: str) -> tuple[str, dict] | None:
    """고른 보기 글자로 문항의 distractors 항목을 찾는다(보기 순서가 바뀌어도 글자로 맞춘다)."""
    dist = q.get("distractors") if isinstance(q.get("distractors"), dict) else None
    if not dist:
        return None
    for i, opt in enumerate(q.get("choices") or []):
        o = re.sub(r"^[A-E][.)]\s*", "", str(opt)).strip()
        if o == str(chosen_text).strip() and "ABCDE"[i] in dist:
            return "ABCDE"[i], dist["ABCDE"[i]]
    return None


def auto_pitfalls(u: Unit, questions: dict) -> list[dict]:
    """정리본의 pitfalls 가 다루지 않는 오답만 문항의 `discriminator`·`when_right` 로 일반화한다.
    `tempting`(왜 끌렸나)은 학습자의 이유를 추측하는 글이라 쓰지 않는다. 날짜·문항 번호도 싣지 않는다."""
    covered = {str(c) for pf in (u.concept or {}).get("pitfalls") or [] for c in pf.get("covers") or []}
    out, seen = [], set()
    for ch in u.state.chosen:
        q = questions.get(ch["qid"], {})
        hit = _dist_for(q, ch["text"])
        if not hit:
            continue
        letter, d = hit
        key = f"{ch['qid']}:{letter}"
        if key in covered or key in seen or not d.get("discriminator"):
            continue
        seen.add(key)
        ans = str(q.get("answer", "")).strip().upper()[:1]
        ans_text = next((re.sub(r"^[A-E][.)]\s*", "", str(o)) for i, o in enumerate(q.get("choices") or []) if "ABCDE"[i] == ans), "")
        out.append({"contrast": f"{ch['text']} ↔ {ans_text}", "point": d.get("discriminator", ""),
                    "exception": d.get("when_right", ""), "key": key})
    return out


# ── 지문(PDF 에 실리는 것만 — 학습 활동 기록은 넣지 않는다) ──────────────
def unit_fingerprint(u: Unit, questions: dict | None = None) -> dict:
    fp = {"concept": (u.concept or {}).get("hash"), "version": (u.concept or {}).get("version"),
          "title": u.title, "src": u.flags,
          "auto": [p["key"] for p in auto_pitfalls(u, questions or {})],
          "stub": [] if u.concept else [(q, (questions or {}).get(q, {}).get("explanation")) for q in u.questions]}
    if u.links:                                     # 있을 때만 — 이음이 없는 단원의 지문은 그대로다
        fp["links"] = {k: [(x["key"], x["title"], x["book"]) for x in v] for k, v in u.links.items()}
    return fp


def volume_hash(title: str, units: list[Unit], pending: list, cfg: dict, questions: dict | None = None,
                elsewhere: list | None = None) -> str:
    payload = {"t": title, "tv": cfg.get("template_version"), "gl": et.digest(),
               "units": [(u.key, unit_fingerprint(u, questions)) for u in units]}
    if elsewhere:                                   # 있을 때만 넣는다 — 다른 책들의 해시는 그대로다
        payload["else"] = [list(x) for x in elsewhere]
    return hashlib.sha256(json.dumps(payload, ensure_ascii=False, sort_keys=True, default=str).encode()).hexdigest()[:20]


# ── 도식: 읽을 수 있는 크기로 한 단 또는 두 단 전체에 맞춘다 ──────────────
_FIT_MEMO: dict[tuple, tuple[dict, bool]] = {}


def fit_diagram(spec: dict, force_full: bool = False, shrink: float = 1.0, force_col: bool = False) -> dict:
    """한 단 안(우선) 또는 두 단 전체(넓은 도식) — 2026-09-27 해리슨식 세로 2단.
    점수 = 항목 중간 끊김 ×0.4pt + 줄바꿈 ×0.12pt − 글자 크기. 두 단 전체는 흐름을 가르므로 +1.0pt, 양옆이 비면 더 벌점.
    한 단(92 mm)에서는 넓은 도식이 3 pt 까지 작아지거나 항목이 잘려(사용자: 「줄이 바뀌면 보기 불편」) 넓은 도식은 두 단 전체로 간다.
    shrink(<1) = 쪽 맞춤 탐색이 정한 축소(빈칸·좁은 띠를 없애려고, 글자 ≥ DIA_SHRINK_FLOOR_PT)."""
    H = (PAGE["h"] - PAGE["mt"] - PAGE["mb"]) * MM_PX
    places = [("column", COLW * MM_PX, H * 0.72, DIA_FLOOR_PT, 0.0),
              ("full", (PAGE["w"] - PAGE["ml"] - PAGE["mr"]) * MM_PX, H * 0.55, DIA_FULL_FLOOR_PT, 1.0)]
    if force_full:
        places = places[1:]
    elif force_col:                                # 배치 탐색: 두 단 폭이 밀려 큰 빈칸이 생길 때 한 단으로(글자 ≥ DIA_FLOOR_PT)
        places = places[:1]
    paras = sum(len(str(x["text"]).split("\n")) for x in spec["nodes"])
    # 같은 도식 · 같은 자리 종류의 계산은 한 번만 — 차례 쪽 번호를 맞추는 재렌더와 배치 탐색이 같은 도식을 수십 번 다시 짰다(도식 하나에 층 배치 16번)
    memo = (json.dumps(spec, ensure_ascii=False, sort_keys=True, default=str), force_full, force_col)
    hit = _FIT_MEMO.get(memo)
    if hit is None:
        cands = []
        for nw in range(180, 481, 20):
            geo = dd.layout(spec, node_w=nw, rank_gap="auto", wrap_fn=dd.phrase_wrap)
            bad = dd.bad_breaks(geo, spec)
            wraps = sum(len(n["lines"]) for n in geo["nodes"]) - paras
            for place, W, MH, floor, pen in places:
                s = round(min(W / geo["w"], MH / geo["h"], DIAGRAM_MAX_SCALE), 3)
                pt = 13 * 0.75 * s
                used = geo["w"] * s / W                    # 두 단 폭 가운데 도식이 실제로 쓰는 몫 — 좁은 도식을 넓게 깔면 양옆이 빈다
                pen2 = pen + (5 * max(0.0, 0.85 - used) if place == "full" else 0.0)
                cands.append(dict(geo=geo, place=place, node_w=nw, scale=s, pt=pt, bad=bad, lines=wraps,
                                  ok=pt >= floor, score=bad * 0.4 + wraps * 0.12 - pt + pen2))
        ok = [c for c in cands if c["ok"]]
        hit = _FIT_MEMO[memo] = (min(ok, key=lambda c: (c["score"], -c["scale"])) if ok else max(cands, key=lambda c: c["scale"]), bool(ok))
    best, ok = hit
    if shrink < 1.0 and best["pt"] * shrink >= DIA_SHRINK_FLOOR_PT:
        best = dict(best, scale=round(best["scale"] * shrink, 3), pt=best["pt"] * shrink, shrink=shrink)
    return dict({k: v for k, v in best.items() if k != "ok"}, ok=bool(ok))

# ── HTML ────────────────────────────────────────────────────────────
CSS = """
@font-face{font-family:BookKR; src:url("%(regular)s"); font-weight:400}
@font-face{font-family:BookKR; src:url("%(bold)s"); font-weight:700}
@page{size:%(pw)smm %(ph)smm; margin:%(mt)smm %(mr)smm %(mb)smm %(ml)smm}
:root{--ink:#1d2733; --muted:#5b6778; --accent:#1f5fae; --accent-soft:#eaf1fb; --rule:#cfd7e3; --zebra:#f6f8fb; --warn:#b4610e; --warn-soft:#fff5e8}
html{font-family:BookKR, sans-serif; font-size:%(body)spt; line-height:%(line)s; color:var(--ink)}
body{margin:0}
.cols{column-count:2; column-gap:%(gap)smm; column-rule:0.4pt solid #d8dee8}
.span{column-span:none}
.diablock{column-span:all; break-inside:avoid; margin:1.5mm 0 2mm}
.diablock figure.dia{margin:0 0 1mm}
.diablock .dnotes{margin:0}
.tocpage{break-after:page}      /* 목차는 따로 한 쪽 — 본문은 다음 쪽 첫머리부터 */
a{color:inherit; text-decoration:none}

.bookhead{border-bottom:1.4pt solid var(--ink); padding-bottom:1.2mm; margin:0 0 2mm; display:flex; gap:4mm; align-items:baseline}
.bookhead h1{font-size:16pt; margin:0}
.bookhead .bm{font-size:8.4pt; color:var(--muted)}
.toc{font-size:8.8pt; line-height:1.34; margin:2mm 0 2.5mm; columns:2; column-gap:8mm; column-rule:0.4pt solid #d8dee8}
.toc ol{list-style:none; margin:0; padding:0}
.toc li{display:flex; align-items:baseline; gap:1.5mm; padding:0.2mm 0; break-inside:avoid}
.toc li::after{content:""; flex:1 1 auto; border-bottom:0.5pt dotted #9aa6b6; margin:0 1mm; order:2}
.toc .pg{order:3; flex:0 0 7mm; text-align:right; color:var(--muted)}
.toc li.grp{display:block; margin:1.6mm 0 0.3mm; font-size:7.8pt; font-weight:700; color:var(--accent)}
.toc li.grp::after{display:none}
.legend{font-size:7.6pt; color:var(--muted); margin:0 0 1.5mm}

section.unit{counter-reset:sec}
.unit-head{margin:3mm 0 1.6mm}
.uhg{break-inside:avoid; break-after:avoid}      /* 제목+학습 목표는 붙이고 한눈에 첫 줄까지 끌고 간다 — 긴 한눈에 때문에 머리 전체가 밀려 단이 비지 않게 */
.sum li{break-inside:avoid}
.uh{border-top:2.2pt solid var(--accent); padding-top:1.2mm; margin:0 0 1.2mm}
.uh h2{font-size:11.6pt; line-height:1.25; margin:0}
.um{font-size:6.8pt; color:var(--muted); margin-top:0.4mm}
.um .flag{color:#b3261e; font-weight:700}
.goal{background:var(--accent-soft); border-radius:1mm; padding:1mm 1.8mm; margin:0 0 1.2mm; font-size:8.2pt}
.goal .k{font-weight:700; color:var(--accent); margin-right:1.5mm}
.sum{border:0.5pt solid var(--rule); border-radius:1mm; padding:1.1mm 1.8mm; margin:0; font-size:8pt}
.sum > b{display:block; font-size:8pt; color:var(--accent); margin-bottom:0.3mm}
.sum ul{margin:0; padding-left:3.6mm}
.sum li{margin:0 0 0.3mm}

h3{counter-increment:sec; font-size:9.6pt; line-height:1.28; margin:2.4mm 0 0.8mm; border-left:0.9mm solid var(--accent); padding-left:1.5mm; break-after:avoid}
h3::before{content:counter(sec) ". "; color:var(--accent)}
h3 + *{break-before:avoid}
h3.deep{border-left-color:#9aa6b6}
h3.deep::after{content:"  심화"; font-size:7pt; color:var(--muted); font-weight:400}
h4{font-size:8.8pt; margin:1.4mm 0 0.5mm; break-after:avoid}
h4.cont{display:none}
p{margin:0 0 1mm; orphans:2; widows:2}
ul,ol{margin:0 0 1mm; padding-left:3.8mm}
li{margin:0 0 0.35mm}
.cite{font-size:6.2pt; color:#8591a3; vertical-align:0.4pt}

table{border-collapse:collapse; width:100%%; table-layout:fixed; font-size:7.8pt; line-height:1.28; margin:0.6mm 0 0.5mm;
      border-top:1pt solid var(--ink); border-bottom:1pt solid var(--ink)}
thead{display:table-header-group}
tr{break-inside:avoid}
th{text-align:left; font-weight:700; color:var(--accent); border-bottom:0.7pt solid var(--ink); padding:0.6mm 1mm}
td{border-bottom:0.35pt solid var(--rule); padding:0.6mm 1mm; vertical-align:top; overflow-wrap:anywhere}
tbody tr:nth-child(even) td{background:var(--zebra)}
.tb{margin:1.4mm 0 1.8mm}
.tb .tt{font-weight:700; font-size:8.6pt; margin:0 0 0.5mm; break-after:avoid}
.tb .tt::before{content:"표  "; color:var(--accent)}
.tb .tn{font-size:7pt; color:var(--muted); margin-top:0.4mm}
td, th{word-break:keep-all; overflow-wrap:break-word}      /* 한글 낱말 중간(「단 / 서」)에서 끊지 않는다 */
table.c3{font-size:7.3pt}
table.c4{font-size:6.9pt}
table.c2 .cite, table.c3 .cite, table.c4 .cite{font-size:5.9pt}
table.rec{border:0.8pt solid var(--ink); font-size:7.5pt; line-height:1.3}
table.rec tr.rh th{background:#e6edf7; color:var(--ink); font-weight:700; border-top:0.8pt solid var(--ink); border-bottom:0.4pt solid var(--rule); padding:0.7mm 1.2mm}
table.rec tr.rh{break-after:avoid}
table.rec td{border-bottom:0.35pt solid var(--rule); padding:0.5mm 1.2mm; background:none !important}
table.rec td.k{color:var(--accent); font-weight:700; white-space:nowrap; background:#f7f9fc !important; border-right:0.4pt solid var(--rule)}
table.rec .cite{white-space:nowrap; font-size:5.9pt}
table.rec .tag{font-size:6.4pt; color:var(--muted); font-weight:400}

figure.dia{margin:1.6mm 0; break-inside:avoid; text-align:center; border:0.5pt solid var(--rule); border-radius:1mm; padding:1mm 0 0.8mm; background:#fbfcfe}
figure.dia figcaption{font-weight:700; font-size:8pt; text-align:left; margin:0 1.5mm 0.6mm; color:var(--accent)}
figure.dia .svgw{margin:0 auto}
figure.dia .svgw svg{width:100%%; height:100%%}
.dnotes{font-size:7.8pt; background:#f5f7fa; border-radius:1mm; padding:1mm 1.8mm; margin:0 0 1.4mm}
.dnotes h4{margin:0 0 0.4mm; font-size:8pt; color:var(--muted)}

figure.fig{margin:1.6mm 0; break-inside:avoid; border:0.5pt solid var(--rule); border-radius:1mm; padding:1.2mm}
figure.fig img{display:block; margin:0 auto 1mm; background:#fff}
figure.fig figcaption{font-size:7.6pt; line-height:1.3}
figure.fig .ft{font-weight:700; font-size:8.2pt; color:var(--accent); margin-bottom:0.4mm}
figure.fig ul{margin:0.3mm 0 0.6mm; padding-left:3.4mm}
figure.fig .fl{margin:0.5mm 0}
figure.fig .fc{font-size:6.6pt; color:var(--muted); overflow-wrap:anywhere}

ul.pit{list-style:none; padding:0; margin:0}
ul.pit li{background:#f3f6fa; border-left:0.9mm solid #9aa6b6; padding:0.8mm 1.6mm; margin:0 0 0.7mm; break-inside:avoid}
ul.pit li > b:first-child{color:var(--ink)}
.pit .ex{color:var(--muted)}

/* 판형 12(2026-11-23) — 한눈에 칸 · 같은 질환 · 기초 뿌리 · 기준 카드 · 혼동 카드 · 시험 쟁점 카드 · 절 지도.
   한 가지 톤(네이비 + 중립 회색) · 글자 라벨만 — 필기 앱에서 펜 · 형광펜 색이 돋보이게. 풀이는 note_parts.py(웹 앱과 같은 함수). */
.um .ok{border:0.4pt solid var(--rule); border-radius:0.8mm; padding:0 1mm; white-space:nowrap}
.hx{font-size:7.4pt; line-height:1.35; margin:0 0 0.8mm}
.hx .k{font-weight:700; color:var(--accent); margin-right:1.2mm}
.hx .here{font-weight:700; border:0.4pt solid var(--accent); border-radius:0.8mm; padding:0 0.8mm}
.hx .sep{color:var(--muted); margin:0 1mm}
.slots{margin:0; font-size:8pt}
.slot{display:grid; grid-template-columns:17mm 1fr; column-gap:1.5mm; border:0.5pt solid var(--rule); border-radius:1mm;
      padding:0.8mm 1.5mm; margin:0 0 0.6mm; break-inside:avoid}
.slot .sk{font-size:6.9pt; font-weight:700; color:var(--accent); line-height:1.5}
.slot.k-conclusion{background:var(--accent-soft); border-left:0.9mm solid var(--accent)}
.slot.k-conclusion .st{font-weight:700}
.slot.k-avoid{border-left:0.9mm solid #9aa6b6}
ul.sl{list-style:none; margin:0; padding:0}
ul.sl li{margin:0; padding:0 0 0 1.5mm; border-left:0.5mm solid #b9c3d1; break-inside:avoid}
ul.sl li + li{margin-top:0.5mm}
ul.sl.sub{margin:0.4mm 0 0 0.5mm}
ul.sl + .sll, ul.sl + ul.sl{margin-top:0.7mm}
.slot.k-conclusion ul.sl li{border-left-color:var(--accent)}
ul.more{margin:0.4mm 0 0; padding-left:3.6mm; font-size:8pt}
ul.more li{margin:0 0 0.3mm; break-inside:avoid}
.pk{font-size:6.6pt; font-weight:700; color:var(--accent); margin-right:1.2mm}
.pc{border:0.5pt solid var(--rule); border-radius:1mm; margin:0 0 0.7mm; break-inside:avoid; overflow:hidden}
.pc .pa{background:#f3f6fa; padding:0.7mm 1.5mm; font-weight:700}
.pc .pb{padding:0.7mm 1.5mm}
.pc .px{color:var(--muted); border-top:0.35pt dashed var(--rule); margin-top:0.5mm; padding-top:0.5mm}
.crit{border:0.5pt solid var(--rule); border-left:0.9mm solid var(--accent); border-radius:1mm; padding:0.8mm 1.5mm; margin:0.6mm 0 0.8mm; break-inside:avoid; font-size:7.8pt; background:#fbfcfe}
.crit .ch{font-weight:700; color:var(--accent)}
.crit .ct{font-size:6.4pt; color:var(--muted); font-weight:400; margin-left:1mm}
.crit .cs{margin:0.3mm 0}
.crit .cm{font-size:7.2pt; color:var(--muted)}
.iz{border:0.5pt solid var(--rule); border-radius:1mm; padding:0.8mm 1.5mm; margin:0 0 0.8mm; break-inside:avoid; background:#fbfcfe; font-size:7.8pt}
.iz .ih{font-weight:700; margin-bottom:0.5mm}
.iz .ii{font-size:6.6pt; border:0.4pt solid var(--accent); border-radius:0.7mm; padding:0 0.8mm; margin-right:1mm; color:var(--accent)}
.iz .i2{display:grid; grid-template-columns:1fr 1fr; column-gap:1.2mm}
.iz .i2 > div{border:0.4pt solid var(--rule); border-radius:0.8mm; padding:0.5mm 1mm; background:#fff}
.iz .iw{margin-top:0.5mm}
.iz .is{margin-top:0.6mm; padding:0.5mm 1.2mm; border-left:0.9mm solid var(--accent); background:var(--accent-soft); font-weight:700}
.iz.note{color:var(--muted); font-size:7.4pt}
.cl{border:0.5pt solid var(--rule); border-radius:1mm; padding:0.8mm 1.5mm; margin:0 0 0.8mm; break-inside:avoid; font-size:7.8pt}
.cl .lh{font-weight:700; color:var(--accent); margin-bottom:0.3mm}
.cl ul{list-style:none; margin:0; padding:0}
.cl li{display:flex; gap:1.2mm; align-items:baseline; border-bottom:0.35pt dashed var(--rule); padding:0.3mm 0; margin:0}
.cl li:last-child{border-bottom:0}
.cl .bx{flex:none; width:1.9mm; height:1.9mm; border:0.5pt solid #7f8b9c; border-radius:0.4mm}
.cl .lt{flex:1 1 auto}
.cl .lp{flex:none; font-weight:700; color:var(--accent)}
.cl .lc{margin-top:0.5mm}
.cmap{border:0.5pt solid var(--rule); border-radius:1mm; padding:1mm 1.5mm 0.6mm; margin:3mm 0 1mm; break-inside:avoid}
.cmap .mh{font-weight:700; font-size:8.6pt; color:var(--accent); margin-bottom:0.5mm}
.cmap table{font-size:7.2pt; border-top:0.6pt solid var(--ink); border-bottom:0.6pt solid var(--ink); margin:0}
.cmap td.mk{color:var(--muted); white-space:nowrap}

.refs{font-size:6.8pt; line-height:1.28; padding-left:4mm; margin:0 0 0.5mm; color:#3d4857}
.refs li{margin-bottom:0.2mm}
.refs a{overflow-wrap:anywhere}
.refnote{font-size:6.6pt; color:var(--muted); margin:0 0 1mm}
.muted{color:var(--muted)}
"""


def css(fonts: dict) -> str:
    return CSS % {**fonts, "pw": PAGE["w"], "ph": PAGE["h"], "mt": PAGE["mt"], "mb": PAGE["mb"], "ml": PAGE["ml"],
                  "mr": PAGE["mr"], "gap": PAGE["gap"], "body": BODY_PT, "line": LINE}


def stack_wide_tables(fragment: str, max_cols: int = 3) -> str:
    """정화된(속성 없는) 본문 HTML 속 표 — 한 단(92 mm)에 3칸 넘는 표는 행 카드로, 남는 표에는 칸 수 class(글자 크기)를 단다."""
    def conv(m: re.Match) -> str:
        t = m.group(0)
        heads = re.findall(r"<th>(.*?)</th>", t, re.S)
        if len(heads) <= max_cols:
            return t.replace("<table>", f'<table class="c{len(heads)}">', 1)
        out = []
        for r in re.findall(r"<tr>(.*?)</tr>", t, re.S):
            cells = re.findall(r"<td>(.*?)</td>", r, re.S)
            if cells:
                out.append("<p>" + " · ".join(f"<b>{h}</b> {c}" for h, c in zip(heads, cells)) + "</p>")
        return "".join(out)
    return re.sub(r"<table>.*?</table>", conv, fragment, flags=re.S)

BLOCK_TAGS = ("p", "ul", "ol", "table", "blockquote", "h3", "h4", "div")


def split_blocks(fragment: str) -> list[str]:
    """정화된 HTML 을 최상위 블록 목록으로(중첩 목록은 바깥 목록 하나로 둔다)."""
    out, depth, start = [], 0, 0
    for m in re.finditer(r"<(/?)(%s)>" % "|".join(BLOCK_TAGS), fragment):
        if not m.group(1):
            if depth == 0:
                start = m.start()
            depth += 1
        else:
            depth -= 1
            if depth == 0:
                out.append(fragment[start:m.end()])
    return out or ([fragment] if fragment.strip() else [])


def _cell(text: Any, c: dict, anchor: str) -> str:
    """표 칸·노트: escape → **굵게** → 근거 번호."""
    s = esc(text)
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    return render_cites(s, c, "pdf", anchor)


def col_widths(columns: list, rows: list) -> list[float]:
    """열 너비(%) — 칸 글자 길이에 비례하되 짧은 열도 제목이 한 줄에 들어가게. 고정 표 배치로 강제한다."""
    strip = lambda s: re.sub(r"\[\[[^\]]*\]\]", "000000", str(s))
    w = []
    for j, h in enumerate(columns):
        lens = [len(strip(r[j])) for r in rows if j < len(r)] or [0]
        avg = sum(lens) / len(lens)
        w.append(max(len(str(h)) * 1.2 + 3, min(avg, 90) ** 0.8, 7.0))
    s = sum(w)
    return [round(x / s * 100, 1) for x in w]


def colgroup(widths: list[float]) -> str:
    return "<colgroup>" + "".join(f'<col style="width:{x}%">' for x in widths) + "</colgroup>"


def record_table(title: str, columns: list, rows: list, note_html: str = "") -> str:
    """칸이 많은 표 → 「항목 머리줄 + 이름|내용 두 칸」 표(한 단 폭). 이름 칸은 한 줄 — 길면 글씨를 줄인다(사용자 2026-09-27)."""
    keys = [re.sub(r"<[^>]+>", "", str(h)) for h in columns[1:]]
    em = max((sum(0.3 if ch == " " else (1.0 if ord(ch) >= 0x2E80 else 0.58) for ch in k) for k in keys), default=3.0)
    ksize = 7.4 if em <= 6.5 else (6.9 if em <= 9 else 6.4)
    kw = em * ksize * 0.3528 * 1.05 + 2.8            # 글자 폭(em) × 글자 크기(pt→mm) + 좌우 여백
    body = []
    for r in rows:
        head, rest = r[0], r[1:]
        body.append(f'<tr class="rh"><th colspan="2">{head}</th></tr>')
        body += [f'<tr><td class="k" style="font-size:{ksize}pt">{esc(h)}</td><td>{v}</td></tr>'
                 for h, v in zip(columns[1:], rest) if re.sub(r"<[^>]+>", "", str(v)).strip() not in ("", "—")]
    return (f'<div class="tb rec"><div class="tt">{title}</div><table class="rec"><colgroup><col style="width:{kw:.1f}mm"><col></colgroup>'
            f'<tbody>{"".join(body)}</tbody></table>{note_html}</div>')


def table_html(tb: dict, c: dict, anchor: str) -> str:
    """한 단 폭. 3칸 이하(또는 짧은 4칸)는 표 그대로(칸 수만큼 글씨를 줄인다), 그보다 넓으면 항목 표(record_table)."""
    cols = tb.get("columns") or []
    rows_ = tb.get("rows") or []
    note = f'<div class="tn">{_cell(tb["note"], c, anchor)}</div>' if tb.get("note") else ""
    strip = lambda s: re.sub(r"\[\[[^\]]*\]\]", "", str(s))
    cells = [len(strip(x)) for r in rows_ for x in r] or [0]
    if len(cols) <= 3 or (len(cols) == 4 and sum(cells) / len(cells) <= 24):
        head = colgroup(col_widths(cols, rows_)) + "<thead><tr>" + "".join(f"<th>{esc(h)}</th>" for h in cols) + "</tr></thead>"
        rows = "".join("<tr>" + "".join(f"<td>{_cell(x, c, anchor)}</td>" for x in r) + "</tr>" for r in rows_)
        return (f'<div class="tb"><div class="tt">{esc(tb.get("title"))}</div>'
                f'<table class="c{len(cols)}">{head}<tbody>{rows}</tbody></table>{note}</div>')
    rows = [[f"<b>{_cell(r[0], c, anchor)}</b>"] + [_cell(x, c, anchor) for x in r[1:]] for r in rows_]
    return record_table(esc(tb.get("title")), cols, rows, note)


def criteria_tables(c: dict, anchor: str) -> str:
    """기준을 종류별 항목 표로(기준 이름 머리줄 + 대상·내용·예외·근거). 다른 지침의 기준은 항목을 나눠 합치지 않는다."""
    groups: dict[str, list[dict]] = {}
    for cr in c.get("criteria") or []:
        groups.setdefault(str(cr.get("kind", "기준")), []).append(cr)
    out = []
    for kind, crs in groups.items():
        rows = []
        for cr in crs:
            loc = f": {cr['locator']}" if cr.get("locator") else ""
            cite = render_cites(esc(f"[[{cr['source']}{loc}]]"), c, "pdf", anchor) if cr.get("source") else ""
            ex = "·".join(e.upper() for e in cr.get("exams") or [])
            tag = f' <span class="tag">{esc(ex)}{" · " + esc(BASIS.get(cr.get("basis"), "")) if cr.get("basis") else ""}</span>'
            rows.append([f"<b>{esc(cr.get('name'))}</b>{tag}", esc(cr.get("population")), _cell(cr.get("statement"), c, anchor),
                         _cell(cr.get("exceptions") or "—", c, anchor), cite])
        out.append(record_table(f"기준 — {esc(kind)}", ["기준", "대상", "내용", "예외", "근거"], rows))
    return "".join(out)


def criteria_cards(c: dict, anchor: str) -> list[str]:
    """기준 하나 = 한 단 카드 하나(판형 12). 이름 · 내용(수치 · 컷오프)을 먼저 읽고, 대상 · 예외는 작게 덧붙인다.

    판형 11 은 종류별 「항목 표」(두 단 전체)로 실었는데, 같은 수치가 본문 표에도 있어 길게 겹쳤고 두 단 전체 블록이라
    도식 바로 뒤에서 단을 억지로 나눴다. 다른 지침의 기준은 카드를 나눠 합치지 않는다."""
    out = []
    for cr in c.get("criteria") or []:
        if not isinstance(cr, dict):
            continue
        loc = f": {cr['locator']}" if cr.get("locator") else ""
        cite = render_cites(esc(f"[[{cr['source']}{loc}]]"), c, "pdf", anchor) if cr.get("source") else ""
        ex = "·".join(e.upper() for e in cr.get("exams") or [])
        tag = " · ".join(x for x in (str(cr.get("kind") or ""), ex, BASIS.get(cr.get("basis"), "")) if x)
        st = _cell(cr.get("statement"), c, anchor)
        out.append(f'<div class="crit"><div class="ch">{esc(cr.get("name"))}<span class="ct">{esc(tag)}</span></div>'
                   f'<div class="cs">{st}{" " + cite if cite and cite not in st else ""}</div>'
                   + (f'<div class="cm"><span class="pk">대상</span>{esc(cr.get("population"))}</div>' if cr.get("population") else "")
                   + (f'<div class="cm"><span class="pk">예외</span>{_cell(cr["exceptions"], c, anchor)}</div>' if cr.get("exceptions") else "")
                   + "</div>")
    return out


def issue_cards(c: dict, anchor: str, html_: str) -> tuple[bool, list[str]]:
    """「시험 쟁점」 절 → (해당 없음인가, 카드들). 네 칸을 못 찾은 항목은 글 그대로 싣는다(모양을 지어내지 않는다)."""
    r = parts.exam_issues(html_)
    if r["none"]:
        return True, []
    cell = lambda k, v, cls: (f'<div class="{cls}"><span class="pk">{k}</span>{render_cites(v, c, "pdf", anchor)}</div>' if v else "")
    out = []
    for it in r["issues"]:
        if not (it["exam"] or it["other"] or it["why"] or it["onexam"]):
            out.append(f'<div class="iz note">{render_cites(it["body"], c, "pdf", anchor)}</div>')
            continue
        head = " · ".join(x for x in (it["kind"], it["title"]) if x)
        out.append(f'<div class="iz"><div class="ih"><span class="ii">{esc(it["id"])}</span>{esc(head)}</div>'
                   + (f'<div>{render_cites(it["body"], c, "pdf", anchor)}</div>' if it["body"] else "")
                   + f'<div class="i2">{cell("시험 기준", it["exam"], "ia")}{cell("다른 기준", it["other"], "io")}</div>'
                   + cell("왜 다른가", it["why"], "iw") + cell("시험에서는", it["onexam"], "is") + "</div>")
    return False, out


def checklist_cards(c: dict, anchor: str) -> list[str]:
    """점수 · 진단 기준 체크리스트(선택 필드 checklists — CURB-65 · CHA2DS2-VASc · Wells · Jones 처럼 항목을 세는 기준)."""
    out = []
    for ck in c.get("checklists") or []:
        if not isinstance(ck, dict) or not ck.get("name") or not isinstance(ck.get("items"), list):
            continue
        items = []
        for it in ck["items"]:
            label, pts = (it.get("label"), it.get("points")) if isinstance(it, dict) else (it, "")
            if str(label or "").strip():
                items.append(f'<li><span class="bx"></span><span class="lt">{_cell(label, c, anchor)}</span>'
                             + (f'<span class="lp">{esc(pts)}</span>' if str(pts or "").strip() else "") + "</li>")
        if items:
            out.append(f'<div class="cl"><div class="lh">{esc(ck["name"])}</div><ul>{"".join(items)}</ul>'
                       + (f'<div class="lc"><span class="pk">판정</span>{_cell(ck["cutoffs"], c, anchor)}</div>' if ck.get("cutoffs") else "")
                       + "</div>")
    return out


def link_line(label: str, items: list[dict], book_title: str, here: str = "") -> str:
    """머리의 한 줄 — 같은 질환 · 기초 뿌리. 같은 책이면 그 단원으로 가는 링크, 다른 책이면 책 이름을 괄호로."""
    def one(x: dict) -> str:
        text = x.get("kind") or x["title"]
        if x["key"] == here:
            return f'<span class="here">{esc(text)}</span>'
        name = esc(x["title"] if label != "같은 질환" else f'{text} — {x["title"]}')
        anchor = "u-" + re.sub(r"[^a-z0-9]+", "-", x["key"].lower()).strip("-")
        return (f'<a href="#{anchor}">{name}</a>' if x.get("book") == book_title
                else f'{name}<span class="muted">({esc(x.get("book") or "다른 책")})</span>')
    sep = '<span class="sep">→</span>' if label == "같은 질환" else '<span class="sep">·</span>'
    return f'<div class="hx"><span class="k">{esc(label)}</span>{sep.join(one(x) for x in items)}</div>'


def diagram_html(c: dict, anchor: str, force_full: bool = False, shrink: float = 1.0, pad: float = 0.0,
                 force_col: bool = False) -> tuple[str, dict | None]:
    """두 단 폭 도식은 「도식에 담기지 않은 조건·예외」까지 한 덩어리(두 단 폭·쪼개지 않음) — 쪽 끝 좁은 틈에서
    좌→우→다음 쪽으로 오가며 읽히던 문제(사용자 2026-09-27)."""
    spec = c.get("diagram")
    if not spec:
        return "", None
    fit = fit_diagram(spec, force_full, shrink, force_col)
    g, s = fit["geo"], fit["scale"]
    svg = dd.to_svg(g, None, dd.LIGHT)
    fig = (f'<figure class="dia"><figcaption>[도식] {esc(spec.get("title"))}</figcaption>'
           f'<div class="svgw" style="width:{g["w"] * s:.0f}px;height:{g["h"] * s:.0f}px">{svg}</div></figure>')
    notes = c.get("diagram_notes") or []
    nh = ('<div class="dnotes"><h4>도식에 담기지 않은 조건·예외</h4><ul>'
          + "".join(f"<li>{_cell(n, c, anchor)}</li>" for n in notes) + "</ul></div>") if notes else ""
    if fit["place"] == "full":
        # pad = 배치 탐색이 넣는 아래 여백 — 도식 아래 좁은 띠(좌→우→다음 쪽)를 다음 쪽으로 넘긴다(빈칸 < 20%)
        style = f' style="margin-bottom:{2 + pad:.0f}mm"' if pad else ""
        return f'<div class="diablock"{style}>{fig}{nh}</div>', fit
    return fig + nh, fit


def figure_html(f: dict, scale: float = 1.0) -> tuple[str, str, dict]:
    """(배치 종류, HTML, 검증 정보). 모든 그림을 한 단 폭으로 — 그림 위, 설명 아래(해리슨식 2단, 폭이 중간에 바뀌지 않게)."""
    from PIL import Image
    path = ROOT / str(f.get("file", ""))
    with Image.open(path) as im:
        w, h = im.size
    ar = w / h if h else 1.0
    ww = COLW - 3
    hh = ww / ar
    if hh > FIG_MAX_H:
        hh = FIG_MAX_H
        ww = hh * ar
    ww, hh = ww * scale, hh * scale              # 배치 탐색이 쪽 끝에 조금 모자란 그림을 줄인다(0.75배까지, 검증 최소 크기 이상)
    look = "".join(f"<li>{esc(x)}</li>" for x in f.get("look_for") or [])
    cited = f" · 피인용 {f['paper_cited_by']}회" if f.get("paper_cited_by") else ""
    paper = f" · {esc(f.get('paper'))}{cited}" if f.get("paper") else ""
    cap = (f'<div class="ft">[그림] {esc(f.get("shows"))}</div>'
           + (f"<ul>{look}</ul>" if look else "")
           + f'<div class="fl"><b>데이터 라벨</b> {esc(f.get("label"))}</div>'
           + f'<div class="fc">라벨 근거: {esc(FIG_BASIS.get(f.get("label_basis"), f.get("label_basis")))} — {esc(f.get("reference"))}{paper}'
           + f' · 출처 {esc(f.get("credit"))} · {esc(f.get("license"))} · 「보는 곳」은 검토 전 설명'
           + (f' · {esc(f.get("marked"))}' if f.get("marked") else "") + '</div>')
    html_ = (f'<figure class="fig"><img src="{path.resolve().as_uri()}" alt="{esc(f.get("shows"))}" '
             f'style="width:{ww:.1f}mm;height:{hh:.1f}mm"><figcaption>{cap}</figcaption></figure>')
    return "flow", html_, {"id": f.get("id"), "place": "column", "w": ww, "h": hh,
                           "probe": f"[그림] {str(f.get('shows') or '')}"[:14]}

def unit_html(u: Unit, cfg: dict, questions: dict, book_title: str, dia_at: int | str | None = None,
              crit_end: bool = False, fig_pos: dict | None = None) -> tuple[str, dict]:
    """(HTML, 검증용 정보). 학습 활동 기록·문항 번호·내부 ID 는 싣지 않는다."""
    c, a = u.concept, u.anchor
    info: dict = {"diagram": None, "sections": [], "figures": [], "fig_choices": {}, "fig_at": {}}
    if not c:            # 정리본 준비 중 — 문항 해설에서 옮긴 요약(검토 전)
        body = []
        for qid in u.questions:
            q = questions.get(qid, {})
            d = q.get("design") or {}
            if d.get("summary"):
                body.append(f"<p>{esc(d['summary'])}</p>")
            if q.get("explanation"):
                body.append(f"<p>{esc(q['explanation'])}</p>")
        pits = auto_pitfalls(u, questions)
        pit = ('<h3>혼동하기 쉬운 점</h3><ul class="pit">' + "".join(
            f"<li><b>{esc(p['contrast'])}</b> — {esc(p['point'])}" + (f' <span class="ex">예외: {esc(p["exception"])}</span>' if p["exception"] else "")
            + "</li>" for p in pits) + "</ul>") if pits else ""
        return (f'<section class="unit"><div class="unit-head"><div class="uh" id="{a}"><h2>{esc(u.title)}</h2>'
                f'<div class="um">{esc(book_title)} · 정리본 준비 중 — 문항 해설에서 옮긴 요약, 의학 내용 검토 전</div></div></div>'
                + "".join(body) + pit + "</section>"), info
    meta = [esc(book_title), f"정리본 v{esc(c.get('version'))}", f"{esc(c.get('updated', c.get('date')))} 갱신"]
    rs = c.get("review_status")
    meta.append("의학 내용 검토 완료" if rs == "reviewed" else "의학 내용 검토 전(형식 검사만)")
    flags = "".join(f' · <span class="flag">확인 필요 — {esc(f)}</span>' for f in u.flags)
    secs = c.get("sections") or []
    # 「시험 쟁점」(판형 12) — 해당 없음 한 줄이면 절을 세우지 않고 머리에 「해리슨 대조 · 충돌 없음」으로 줄이고, 쟁점이 있으면 카드로 싣는다
    issue_i = next((i for i, s in enumerate(secs) if parts.is_issue_title(s["title"])), None)
    issue_none, issue_blocks = issue_cards(c, a, secs[issue_i]["html"]) if issue_i is not None else (False, [])
    if issue_none:
        meta.append('<span class="ok">해리슨 대조 · 충돌 없음</span>')
    # 제목·학습 목표·한눈에를 한 덩어리로 — 단 끝에 제목만 떨어지지 않게(사용자 2026-09-27)
    head = f'<div class="uh" id="{a}"><h2>{esc(u.title)}</h2><div class="um">{" · ".join(meta)}{flags}</div></div>'
    if c.get("objective"):
        head += f'<div class="goal"><span class="k">학습 목표</span>{_cell(c["objective"], c, a)}</div>'
    if len(u.links.get("series") or []) > 1:
        head += link_line("같은 질환", u.links["series"], book_title, u.key)
    ep = c.get("exam_points") if isinstance(c.get("exam_points"), dict) else {}
    for k_, lab in (("kmle", "KMLE 포인트"), ("usmle", "USMLE 포인트")):      # 국내 기준 · 약제 · 역학이 미국과 다를 때만 적는 한 줄
        if str(ep.get(k_) or "").strip():
            head += f'<div class="hx"><span class="k">{lab}</span>{_cell(ep[k_], c, a)}</div>'
    if u.links.get("roots"):
        head += link_line("기초 뿌리", u.links["roots"], book_title)
    head = f'<div class="uhg">{head}</div>'
    if c.get("summary"):
        # 한눈에(판형 12) — 요약의 머리말(결론 · 시험 단서 · 왜 · 쓰지 않는 약)을 칸으로 세운다. 머리말이 없는 줄은 아래 목록으로.
        slots = parts.summary_slots(c["summary"])

        def lines(s: dict) -> str:
            """칸 안의 줄 — 한 줄에 이어 쓴 나열(약 이름 · 단서)을 덩이마다 줄을 바꾼다(note_parts.slot_groups, 앱과 같은 규칙)."""
            gs = s["groups"]
            if sum(len(g["items"]) + bool(g["lead"]) for g in gs) <= 1:
                return _cell(s["text"], c, a)
            return "".join((f'<div class="sll">{_cell(g["lead"], c, a)}</div>' if g["lead"] else "")
                           + f'<ul class="sl{" sub" if g["lead"] else ""}">' + "".join(f"<li>{_cell(x, c, a)}</li>" for x in g["items"]) + "</ul>" for g in gs)

        main = [s for s in slots if s["kind"] != "more"]
        head += '<div class="slots">' + "".join(
            f'<div class="slot k-{s["kind"]}"><div class="sk">{esc(s["label"])}</div><div class="st">{lines(s)}</div></div>' for s in main) + "</div>"
        more = [s for s in slots if s["kind"] == "more"]
        if more:
            head += '<ul class="more">' + "".join(f"<li>{lines(s)}</li>" for s in more) + "</ul>"
    h = [f'<section class="unit"><div class="unit-head">{head}</div>']
    tables = [t for t in c.get("tables") or [] if isinstance(t, dict)]
    placed: set[str] = set()
    titles = [s["title"] for s in secs]
    # 기준 카드의 자리 = 「무엇을 하나」 절의 앞. 판형 2 의 절 이름은 「선택 — …」「권고와 예외」다 — 판형 11 은 「치료…」만 찾아
    # 판형 2 정리본 전부(212편)에서 기준이 맨 끝(시험 쟁점 뒤)으로 밀렸다.
    crit_at = next((i for i, t in enumerate(titles) if t.startswith(("치료", "선택", "권고"))), len(secs))
    tx_at = crit_at
    if crit_end:                  # 배치 탐색: 기준을 본문 끝으로(판형 11 의 두 단 전체 표 때 쓰던 길 — 카드는 한 단이라 거의 쓰이지 않는다)
        crit_at = len(secs)
    crit_blocks = [("flow", x) for x in criteria_cards(c, a)]
    # 본문을 블록(제목·문단·목록·표) 단위로 편다 — 큰 도식은 블록 경계 어디에든 끼울 수 있게(빈 공간을 줄이는 배치 탐색용)
    blocks: list[tuple[str, str]] = []            # (kind, html) kind: head · flow · span
    dia_default = None
    for i, s in enumerate(secs):
        if i == crit_at:
            blocks += crit_blocks
        if i == issue_i:                                # 시험 쟁점 — 해당 없음이면 싣지 않고(머리의 표시), 쟁점이면 카드
            if issue_blocks:
                info["sections"].append(s["title"])
                blocks.append(("head", f'<h3 id="{a}-s{i}">시험 쟁점</h3>'))
                blocks += [("flow", x) for x in issue_blocks]
            continue
        info["sections"].append(s["title"])
        deep_cls = ' class="deep"' if s["deep"] else ""
        blocks.append(("head", f'<h3 id="{a}-s{i}"{deep_cls}>{esc(s["title"])}</h3>'))
        for b in split_blocks(render_cites(stack_wide_tables(s["html"]), c, "pdf", a)):
            blocks.append(("flow", b))
        for tb in tables:
            if tb.get("section") == s["title"]:
                blocks.append(("span" if tb.get("span") == "full" else "flow", table_html(tb, c, a))); placed.add(tb["id"])
        if i == (tx_at if tx_at < len(secs) else len(secs) - 1):
            dia_default = len(blocks)              # 기본: 치료 절 끝
    if crit_at >= len(secs):
        blocks += crit_blocks
    for tb in tables:
        if tb["id"] not in placed:
            blocks.append(("span" if tb.get("span") == "full" else "flow", table_html(tb, c, a)))
    cls = checklist_cards(c, a)
    if cls:
        blocks.append(("head", "<h3>점수 · 기준 체크리스트</h3>"))
        blocks += [("flow", x) for x in cls]
    if dia_default is None:
        dia_default = len(blocks)
    pits = [dict(p, cites=p.get("cites") or []) for p in c.get("pitfalls") or []] + auto_pitfalls(u, questions)
    if pits:
        blocks.append(("head", "<h3>혼동하기 쉬운 점</h3>"))
        # 혼동 카드(판형 12) — 위 칸 「혼동」(무엇과 헷갈리나), 아래 칸 「기준」(그래서 무엇으로 가르나) + 예외. 카드 하나가 블록 하나라
        # 도식이 카드 사이 어디에든 들어갈 수 있다.
        for pf in pits:
            cites = " ".join(render_cites(esc(f"[[{x}]]"), c, "pdf", a) for x in pf.get("cites") or [])
            blocks.append(("flow", f'<div class="pc"><div class="pa"><span class="pk">혼동</span>{esc(pf["contrast"])}</div>'
                           f'<div class="pb"><span class="pk">기준</span>{_cell(pf["point"], c, a)}{" " + cites if cites else ""}'
                           + (f'<div class="px"><span class="pk">예외</span>{_cell(pf["exception"], c, a)}</div>' if pf.get("exception") else "")
                           + "</div></div>"))
    force_full = dia_at == "full"
    choices = [k for k in range(1, len(blocks) + 1) if blocks[k - 1][0] != "head"]
    if dia_at is None or force_full or dia_at not in choices:
        dia_at = dia_default if dia_default in choices else (choices[-1] if choices else len(blocks))
    info["dia_at"], info["dia_default"], info["dia_choices"] = dia_at, dia_default, choices
    fp = fig_pos or {}
    dh, fit = diagram_html(c, a, force_full, float(fp.get(f"{a}#shrink", 1.0)), float(fp.get(f"{a}#pad", 0)), bool(fp.get(f"{a}#col")))
    sec_of = []
    cur = ""
    for kind, html_ in blocks:
        if kind == "head":
            cur = re.sub(r"<[^>]+>", "", html_)
        sec_of.append(cur)
    inserts: dict[int, list[tuple[str, str]]] = {}      # k → blocks[k] 앞(= 앞의 k 블록 뒤)에 넣을 것
    # 그림(2026-09-27): 기본 자리는 `at` 절의 첫 문단 뒤 — 제목과 첫 설명을 읽고 바로 그림을 본다. 배치 탐색이 같은 절 안에서 옮긴다.
    for f in c.get("figures") or []:
        if not isinstance(f, dict) or not f.get("file") or not (ROOT / str(f["file"])).exists():
            continue
        kind_, fh, finfo = figure_html(f, float((fig_pos or {}).get(f"{a}#figscale:{f.get('id')}", 1.0)))
        at_title = str(f.get("at") or "")
        idx = [k for k in range(len(blocks)) if sec_of[k] == at_title] or [k for k in range(len(blocks)) if sec_of[k]]
        flows = [k + 1 for k in idx if blocks[k][0] != "head"]
        fchoices = flows or [max(idx) + 1 if idx else len(blocks)]
        want = (fig_pos or {}).get(f"{a}#fig:{f.get('id')}")
        pos = want if want in fchoices else fchoices[0]
        info["fig_choices"][f.get("id")], info["fig_at"][f.get("id")] = fchoices, pos
        info["figures"].append(finfo)
        inserts.setdefault(pos, []).append((kind_, fh))
    if dh:
        # 도식이 한 절의 중간에 끼면, 도식 뒤에서 그 절이 이어진다는 것을 작은 제목으로 알린다(읽는 순서가 끊겨 보이지 않게)
        items = [("flow" if fit and fit["place"] == "column" else "span", dh)]
        if 0 < dia_at < len(blocks) and blocks[dia_at][0] == "flow" and sec_of[dia_at - 1] == sec_of[dia_at] and sec_of[dia_at]:
            items.append(("flow", f'<h4 class="cont">{esc(sec_of[dia_at])} — 이어서</h4>'))
        inserts.setdefault(dia_at, []).extend(items)
        info["diagram"] = fit
    merged: list[tuple[str, str]] = []
    for k in range(len(blocks) + 1):
        merged += inserts.get(k, [])
        if k < len(blocks):
            merged.append(blocks[k])
    h += [b for _, b in merged]
    if u.links.get("supports"):                             # 기초 단원 — 이 기전이 받치는 임상 단원(역방향 모음)
        h.append("<h3>이 기전이 받치는 임상 단원</h3><ul>" + "".join(
            "<li>" + (f'<a href="#u-{re.sub(r"[^a-z0-9]+", "-", x["key"].lower()).strip("-")}">{esc(x["title"])}</a>' if x.get("book") == book_title
                      else f'{esc(x["title"])} <span class="muted">({esc(x.get("book") or "다른 책")})</span>') + "</li>"
            for x in u.links["supports"]) + "</ul>")
    # 근거
    nums = source_numbers(c)
    h.append("<h3>근거</h3><ol class=\"refs\">")
    dag = False
    for s in c.get("sources") or []:
        n = nums[str(s.get("id"))]
        url = safe_url(s.get("url")) or (f"https://doi.org/{s['doi']}" if s.get("doi") else "")
        lvl = s.get("verified", "citation")
        dag |= lvl != "text"
        link = f' <a href="{esc(url)}">{esc(("doi:" + s["doi"]) if s.get("doi") else url)}</a>' if url else ""
        h.append(f'<li id="{a}-ref-{n}" value="{n}">{esc(s.get("org"))}. {esc(s.get("title"))}. {esc(s.get("citation") or s.get("year"))}.{link}'
                 f' <span class="muted">— {VERIFIED_LABEL.get(lvl, lvl)} {esc(s.get("checked_at"))}</span></li>')
    h.append("</ol>")
    if dag or "[[?" in json.dumps(c, ensure_ascii=False, default=str):
        h.append('<div class="refnote">† 원문 본문과 대조하지 않은 근거(초록·서지만 확인) — 현행 권고로 단정하지 않는다.</div>')
    h.append("</section>")
    return "".join(h), info


def book_html(title: str, units: list[Unit], cfg: dict, questions: dict, meta: dict,
              pagemap: dict[str, int] | None, fonts: dict, changes: list[str],
              dia_pos: dict | None = None) -> tuple[str, dict]:
    infos = {}
    bodies = []
    # 절 지도(판형 12) — 해리슨 절(차례의 중간 머리글)에 단원이 셋 이상이면 그 절 첫머리에 「단원 · 목표 종류 · 핵심 결론」을 한 표로 먼저 보인다.
    # 원고에서 뽑은 것이다(요약의 「결론:」 줄) — 새 내용을 쓰지 않는다. 결론 줄이 없는 단원은 제목만 싣는다.
    by_group: dict[str, list[Unit]] = {}
    for u in units:
        if u.group and u.concept:
            by_group.setdefault(u.group, []).append(u)
    mapped: set[str] = set()
    for u in units:
        g = u.group
        if g and g not in mapped and len(by_group.get(g, [])) >= 3:
            mapped.add(g)
            rows = []
            for x in by_group[g]:
                concl = next((s["text"] for s in parts.summary_slots(x.concept.get("summary")) if s["kind"] == "conclusion"), "")
                concl = re.sub(r"\s*\[\[[^\]]*\]\]", "", concl)
                rows.append(f'<tr><td><a href="#{x.anchor}">{esc(x.title)}</a></td>'
                            f'<td class="mk">{esc(x.concept.get("objective_kind") or "")}</td><td>{esc(concl)}</td></tr>')
            bodies.append(f'<div class="cmap"><div class="mh">{esc(g)} — 단원 지도</div><table>'
                          '<colgroup><col style="width:34%"><col style="width:13%"><col></colgroup>'
                          f'<tbody>{"".join(rows)}</tbody></table></div>')
        uh, info = unit_html(u, cfg, questions, title, (dia_pos or {}).get(u.anchor),
                             bool((dia_pos or {}).get(u.anchor + "#crit_end")), dia_pos)
        bodies.append(uh); infos[u.anchor] = info
    pg = lambda k: str(pagemap.get(k, "")) if pagemap else "…"
    toc, grp = "", ""
    for u in units:
        if u.group and u.group != grp:                       # 해리슨 절 이름을 차례의 중간 머리글로
            grp = u.group
            toc += f'<li class="grp">{esc(grp)}</li>'
        toc += f'<li><a href="#{u.anchor}">{esc(u.title)}</a><span class="pg">{pg(u.anchor)}</span></li>'
    h = [f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>{esc(title)} — {esc(cfg["title"])} 판 {meta["version"]}</title>'
         f"<style>{css(fonts)}</style></head><body>",
         # 목차는 따로 한 쪽(두 단 목차) — 본문은 다음 쪽 첫머리부터(사용자 2026-09-27). 두 단 흐름 안에서는 쪽 나눔이 먹지 않아 밖에 둔다.
         f'<div class="tocpage"><div class="bookhead"><h1>{esc(title)}</h1><span class="bm">{esc(cfg["title"])} · 판 {meta["version"]} · {esc(meta["date"])}</span></div>'
         f'<nav class="toc"><ol>{toc}</ol></nav>'
         + (f'<div class="legend"><b>다른 책에 실린 {esc(title)} 단원</b> — '
            + esc(" · ".join(f"{t_}({b_})" for t_, b_ in meta["elsewhere"])) + "</div>" if meta.get("elsewhere") else "")
         + (f'<div class="legend"><b>이번 판의 내용 변경</b> — {esc(" · ".join(changes))}</div>' if changes else "")
         + '<div class="legend">[n 쪽·절] = 단원 끝 「근거」의 번호와 원문 위치 · † = 원문 본문과 대조하지 않은 근거</div></div>'
         + '<main class="cols">']
    h += bodies
    h.append("</main></body></html>")
    return "".join(h), infos


# ── 렌더링 · 위치 · 검증 ─────────────────────────────────────────────
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
            page.pdf(path=str(out), width=f"{PAGE['w']}mm", height=f"{PAGE['h']}mm", print_background=True,
                     display_header_footer=True, header_template="<span></span>",
                     footer_template=('<div style="font-family:NanumGothic,\'Noto Sans KR\',sans-serif;font-size:7.5pt;color:#667;'
                                      f'width:100%;text-align:center">{esc(footer)} · <span class="pageNumber"></span> / '
                                      '<span class="totalPages"></span></div>'),
                     margin={"top": f"{PAGE['mt']}mm", "bottom": f"{PAGE['mb']}mm", "left": f"{PAGE['ml']}mm",
                             "right": f"{PAGE['mr']}mm"},
                     prefer_css_page_size=True, tagged=True, outline=True)
        finally:
            page.close()


def locate(pdf_path: Path) -> dict[str, int]:
    """차례 링크가 가리키는 이름 붙은 목적지 → 쪽(1-based). Chromium 이 링크 대상마다 목적지를 만든다."""
    import pymupdf
    pm: dict[str, int] = {}
    with pymupdf.open(pdf_path) as doc:
        for p in doc:
            for ln in p.get_links():
                if ln.get("kind") in (pymupdf.LINK_NAMED, pymupdf.LINK_GOTO) and ln.get("nameddest") and ln.get("page", -1) >= 0:
                    pm.setdefault(ln["nameddest"], ln["page"] + 1)
    return pm


def set_metadata(pdf_path: Path, title: str, meta: dict) -> None:
    import pymupdf
    doc = pymupdf.open(pdf_path)
    doc.set_metadata({"title": f"{title} — MedKOS 과별 학습서 판 {meta['version']}", "author": "MedKOS",
                      "subject": f"과별 학습서 {meta['date']}", "creator": "MedKOS build_books.py"})
    tmp = pdf_path.with_suffix(".tmp.pdf")
    doc.save(tmp, garbage=3, deflate=True)
    doc.close()
    tmp.replace(pdf_path)


def validate_pdf(pdf_path: Path, title: str, units: list[Unit], pm: dict[str, int], infos: dict) -> tuple[list[str], list[str]]:
    """(오류, 참고). 오류가 하나라도 있으면 최신본을 바꾸지 않는다."""
    import pymupdf
    errs, notes = [], []
    doc = pymupdf.open(pdf_path)
    W, H = doc[0].rect.width, doc[0].rect.height
    if W > H:
        errs.append("세로 판형이 아니다")
    notemb = {f[3] for p in doc for f in p.get_fonts(full=True) if f[1] in ("n/a", "") and f[2] != "Type3"}
    if notemb:
        errs.append(f"임베드되지 않은 글꼴: {sorted(notemb)}")
    texts = [" ".join(p.get_text().split()) for p in doc]
    # 가로로 넘치는 요소가 있으면 Chromium 이 쪽 전체를 축소 인쇄한다 — 본문 글자 크기가 설계값과 같은지로 잡는다
    import collections
    sizes = collections.Counter(round(sp["size"], 1) for p in doc for b in p.get_text("dict")["blocks"] if b.get("type") == 0
                                for ln in b["lines"] for sp in ln["spans"]
                                if len(sp["text"].strip()) > 3 and BODY_PT * 0.9 <= sp["size"] <= BODY_PT * 1.05)
    if sizes:
        body = sizes.most_common(1)[0][0]
        if abs(body - BODY_PT) > 0.15:
            errs.append(f"본문 글자가 {body}pt 로 인쇄됐다(설계 {BODY_PT}pt) — 가로로 넘치는 요소 때문에 쪽 전체가 축소됐다")
    if title.split()[0] not in " ".join(texts):
        errs.append("책 이름을 글자로 찾지 못했다(이미지 PDF?)")
    for u in units:
        if u.anchor not in pm:
            errs.append(f"차례 링크가 단원을 가리키지 않는다: {u.title}")
            continue
        probe = re.sub(r"\s+", " ", u.title)[:10]
        # search_for 는 한 줄 안에서만 찾는다 — 제목이 「—」 뒤에서 줄바꿈되면(서버 글꼴 폭 차이) 못 찾았다(2026-09-22).
        # 쪽 글자에서 공백을 모두 뺀 뒤 비교한다.
        flat = re.sub(r"\s+", "", doc[pm[u.anchor] - 1].get_text())
        if re.sub(r"\s+", "", probe) not in flat:
            errs.append(f"단원 첫 쪽에서 제목 검색 실패: {probe}")
        if u.concept and re.search(re.escape(u.key), " ".join(texts)):
            errs.append(f"내부 ID 가 PDF 에 보인다: {u.key}")
    order = [pm[u.anchor] for u in units if u.anchor in pm]
    if order != sorted(order):
        errs.append("단원 쪽 순서가 차례와 다르다")
    toc = doc.get_toc()
    for u in units:
        if not any(re.sub(r"\s+", " ", u.title)[:10] in re.sub(r"\s+", " ", t[1]) for t in toc):
            errs.append(f"책갈피에 단원이 없다: {u.title}")
    for pat, what in ((r"단원 ID|content/concepts|\.md\b", "내부 경로·ID"), (r"스스로 묻기|해설 열람|정리본 읽음|복습 필요|변형 문제", "학습 활동 기록")):
        hit = [i + 1 for i, t in enumerate(texts) if re.search(pat, t)]
        if hit:
            errs.append(f"{what} 문구가 남아 있다({hit}쪽)")
    top, bottom = PAGE["mt"] * 72 / 25.4, H - PAGE["mb"] * 72 / 25.4
    mid = W / 2
    h3_size = 9.6
    for p in doc:
        spans = [sp for b in p.get_text("dict")["blocks"] if b.get("type") == 0
                 for ln in b.get("lines", []) for sp in ln.get("spans", []) if sp["text"].strip()]
        for sp in spans:
            if sp["bbox"][2] > W - 4 or sp["bbox"][0] < 4:
                errs.append(f"{p.number + 1}쪽 글자가 좌우 가장자리를 넘는다: {sp['text'][:20]!r}")
                break
        # 단별로 내용이 덮는 세로 구간(글자 줄 + 선·도형) — 두 단 전체 요소는 양쪽에 센다
        segs = {0: [], 1: []}
        # 단 사이 세로줄(column-rule)은 내용이 아니다 — 가운데의 가는 세로선은 뺀다
        items = [(sp["bbox"], sp) for sp in spans] + [((d["rect"].x0, d["rect"].y0, d["rect"].x1, d["rect"].y1), None)
                                                      for d in p.get_drawings() if d.get("rect") is not None
                                                      and not (d["rect"].width < 3 and abs((d["rect"].x0 + d["rect"].x1) / 2 - mid) < 6)]
        # 그림(래스터)도 내용이다 — 세지 않으면 그림 자리를 빈 공간으로 오판한다(2026-09-27)
        items += [(tuple(im["bbox"]), None) for im in p.get_image_info()]
        for (x0, y0, x1, y1), _ in items:
            if y1 <= top - 1 or y0 >= bottom + 1:
                continue
            cols = [0, 1] if (x0 < mid - 20 and x1 > mid + 20) else [0 if (x0 + x1) / 2 < mid else 1]
            for c in cols:
                segs[c].append((max(y0, top), min(y1, bottom)))
        cov = 0.0
        col_cov = {}
        for c in (0, 1):
            cur, tot = None, 0.0
            for a0, a1 in sorted(segs[c]):
                if cur and a0 <= cur[1] + 6:
                    cur = (cur[0], max(cur[1], a1))
                else:
                    if cur:
                        tot += cur[1] - cur[0]
                    cur = (a0, a1)
            if cur:
                tot += cur[1] - cur[0]
            col_cov[c] = tot / (bottom - top)
            cov += col_cov[c] / 2
        if 0 < p.number < doc.page_count - 1:          # 1쪽 = 목차 쪽(따로 한 쪽이라 여백이 정상)
            if cov < 0.5:
                errs.append(f"{p.number + 1}쪽에 빈 공간이 크다(내용 {cov:.0%})")
            # 단 아래쪽 빈 공간 — 그 아래에 아무것도(두 단 전체 요소도) 없는 채로 30% 넘게 비었으면 배치 문제다.
            # 두 단 전체 표 앞에서 양쪽 단이 고르게 나뉜 경우는 아래에 그 표가 있으므로 빈 공간으로 치지 않는다.
            for c, name in ((0, "왼쪽"), (1, "오른쪽")):
                low = max([a1 for a0, a1 in segs[c]] or [top])
                gap = (bottom - low) / (bottom - top)
                if gap > 0.3:
                    errs.append(f"{p.number + 1}쪽 {name} 단 아래가 비어 있다(빈 공간 {gap:.0%})")
        # 두 단 폭 도식 위·아래에 남은 두 단 글 띠가 본문 높이 20% 미만 — 좌→우→다음 쪽으로 오가며 읽힌다(사용자 2026-09-27)
        full_w = (PAGE["w"] - PAGE["ml"] - PAGE["mr"]) * 72 / 25.4
        # 두 단 폭 덩어리 = 본문 폭 80% 넘는 도형(도식 틀 + 붙은 조건·예외 상자 배경). 가는 가로줄(머리 밑줄)은 뺀다
        wide_ = [d["rect"] for d in p.get_drawings() if d.get("rect") is not None and d["rect"].width > 0.8 * full_w and d["rect"].height > 3]
        spans_ = wide_ if any(r.height > 40 for r in wide_) else []
        if spans_ and p.number < doc.page_count - 1:
            y0_, y1_ = min(r.y0 for r in spans_), max(r.y1 for r in spans_)
            hh_ = bottom - top
            below_ = [sp for sp in spans if sp["bbox"][1] > y1_ + 2 and sp["bbox"][3] < bottom]
            above_ = [sp for sp in spans if sp["bbox"][3] < y0_ - 2 and sp["bbox"][1] > top]
            if below_ and (bottom - y1_) < 0.2 * hh_:
                errs.append(f"{p.number + 1}쪽 두 단 도식 아래 좁은 띠(빈 공간 아님, {(bottom - y1_) / hh_:.0%}) — 좌우로 오가며 읽힌다")
            elif above_ and (y0_ - top) < 0.2 * hh_ and any(sp["bbox"][0] > mid for sp in above_):
                errs.append(f"{p.number + 1}쪽 두 단 도식 위 좁은 띠({(y0_ - top) / hh_:.0%}) — 좌우로 오가며 읽힌다")
        if p.number == doc.page_count - 1 and cov < 0.12:
            notes.append(f"마지막 쪽 내용이 적다({cov:.0%})")
        # 고립된 제목: 소제목 아래 같은 단에 이어지는 글이 없다
        for sp in spans:
            if any(abs(sp["size"] - hs) < 0.05 for hs in (h3_size, 8.8, 8.6, 11.6)) and sp["flags"] & 16:
                c = 0 if (sp["bbox"][0] + sp["bbox"][2]) / 2 < mid else 1
                below = [o for o in spans if o is not sp and o["bbox"][1] > sp["bbox"][3] - 1
                         and (0 if (o["bbox"][0] + o["bbox"][2]) / 2 < mid else 1) == c]
                if not below:
                    errs.append(f"{p.number + 1}쪽 고립된 제목: {sp['text'][:20]!r}")
    pt = 72 / 25.4
    for u in units:
        for fi in infos.get(u.anchor, {}).get("figures") or []:
            pages = [i for i, t in enumerate(texts) if fi["probe"] in t]
            if not pages:
                errs.append(f"그림 설명을 찾지 못했다: {u.title} {fi['probe']}")
                continue
            imgs = [im for im in doc[pages[0]].get_image_info()]
            mw, mh = FIG_MIN[fi["place"]]
            if not any((im["bbox"][2] - im["bbox"][0]) >= mw * pt * 0.97 and (im["bbox"][3] - im["bbox"][1]) >= mh * pt * 0.97 for im in imgs):
                errs.append(f"그림이 설명과 같은 쪽에 읽을 크기로 없다({pages[0] + 1}쪽): {u.title} {fi['probe']}")
    for u in units:
        fit = infos.get(u.anchor, {}).get("diagram")
        if not fit:
            continue
        if not fit["ok"]:
            errs.append(f"도식이 읽을 크기로 한 쪽에 들어가지 않는다(배율 {fit['scale']}) — 도식을 의미 단위로 나눠라: {u.title}")
        head = f"[도식] {u.concept['diagram'].get('title')}"[:16]
        last = fit["geo"]["nodes"][-1]["lines"][0][:8]
        pages = [i for i, t in enumerate(texts) if head in t]
        if not pages or last not in texts[pages[0]]:
            errs.append(f"도식이 한 쪽에 온전히 있지 않다: {u.title}")
    doc.close()
    return errs, notes


def preview(pdf_path: Path, out_dir: Path, pages: list[int] | None = None, zoom: float = 1.2) -> list[Path]:
    import pymupdf
    out_dir.mkdir(parents=True, exist_ok=True)
    res = []
    with pymupdf.open(pdf_path) as doc:
        for n in pages or range(1, doc.page_count + 1):
            if 1 <= n <= doc.page_count:
                p = out_dir / f"{pdf_path.stem}_p{n:02d}.png"
                doc[n - 1].get_pixmap(matrix=pymupdf.Matrix(zoom, zoom)).save(p)
                res.append(p)
    return res


# ── 전체 목차 ───────────────────────────────────────────────────────
def index_html(books_meta: list[dict], cfg: dict, fonts: dict, date: str) -> str:
    h = [f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>{esc(cfg["title"])} 전체 목차</title>'
         f"<style>{css(fonts)}</style></head><body>"
         f'<div class="bookhead"><h1>{esc(cfg["title"])} — 전체 목차</h1>'
         f'<span class="bm">{esc(date)} · 책 {len(books_meta)}권</span></div><main class="cols">']
    for b in books_meta:
        h.append(f'<h3>{esc(b["title"])}</h3><p class="refnote">{esc(b["file"])} · 판 {b["version"]} · {b["pages"]}쪽</p><ul>')
        h += [f'<li>{esc(u["title"])} <span class="refnote">{u.get("page") or ""}쪽</span></li>' for u in b["units"]]
        h.append("</ul>")
    h.append("</main></body></html>")
    return "".join(h)


# ── 실행 ───────────────────────────────────────────────────────────
def _changes(prev: dict, units: list[Unit]) -> list[str]:
    """실질 내용 변경만(새 단원·정리본 판 변경·빠진 단원). 학습 상태·판형 변경은 싣지 않는다. 첫 판은 빈 목록."""
    if not prev:
        return []
    old = prev.get("units") or {}
    out = []
    for u in units:
        o = old.get(u.key)
        if not o:
            out.append(f"새 단원: {u.title}")
        elif o.get("concept_version") != (u.concept or {}).get("version"):
            out.append(f"내용 갱신: {u.title} (정리본 v{o.get('concept_version')} → v{(u.concept or {}).get('version')})")
        elif o.get("concept_hash") != (u.concept or {}).get("hash"):
            out.append(f"내용 수정: {u.title}")
    keys = {u.key for u in units}
    out += [f"빠진 단원(다른 권으로 이동 등): {v.get('title', k)}" for k, v in old.items() if k not in keys]
    return out


# ── 배치 탐색 ───────────────────────────────────────────────────────
# 평가(trial)를 갈아 끼울 수 있게 한 탐색 — 같은 선택지 · 같은 순서 · 같은 점수를
#   · `MeasuredBook.evaluate`(PDF 없이 잰다 — 기본, 2026-11-23)와
#   · PDF 로 그려 검증하는 `pdf_trial`(지금까지의 방식 — `--layout search`, 측정이 안 되는 책, 예측에 없던 오류 고치기)
# 이 함께 쓴다. trial(pos) → (오류 목록, 쪽 수, 단원 정보, 단원 쪽).
MEASURE_MARGIN = 0.01             # 측정으로 고를 때는 문턱을 1 %p 엄하게(빈칸 29 % 부터 문제) — 실제 PDF 에서 아슬아슬하게 걸리지 않게
REPAIR_RENDERS = 6                # 예측에 없던 오류를 PDF 로 고쳐 볼 때의 렌더 예산(책마다)


def placement_score(errs: list[str], npg: int) -> tuple[int, int]:
    le = bl.layout_errors(errs)
    return (len(le) + 100 * (len(errs) - len(le)), npg)


def _last_problem_page(errs: list[str]) -> int | None:
    """배치 문제가 있는 마지막 쪽. 쪽을 모르는 오류(배치 외)가 섞여 있으면 None — 어느 단원도 건너뛰지 않는다."""
    le = bl.layout_errors(errs)
    if not le or len(le) != len(errs):
        return None
    return max(bl.error_key(e)[0] for e in le)


def units_near(units: list[Unit], pm: dict, pages: list[int]) -> set[str]:
    """그 쪽들에 닿는 단원 — 앞쪽 첫머리를 차지한 단원부터 그 쪽에서 시작하는 단원까지(흐름은 앞에서 뒤로만 간다)."""
    out: set[str] = set()
    starts = [(pm.get(u.anchor) or 0, u.anchor) for u in units]
    for p in pages:
        before = [s for s, _ in starts if 0 < s <= p - 1]
        lo = max(before) if before else 0
        out |= {a for s, a in starts if lo <= s <= p}
    return out


def search_placement(units: list[Unit], trial, start: tuple, pos0: dict | None = None, prune: bool = False,
                     only: set[str] | None = None, budget: int | None = None, goal=None) -> tuple[dict, int]:
    """도식 · 그림의 자리 · 축소 · 여백을 하나씩 바꿔 가며 배치 오류가 가장 적은 배치를 고른다 → (배치, 시도 수).

    start = 지금 배치(pos0)의 (오류, 쪽 수, 단원 정보, 단원 쪽). prune = 측정 탐색용 가지치기:
    목표(goal — 기본은 배치 오류 0)에 닿으면 멈추고, 마지막 문제 쪽보다 뒤에서 시작하는 단원은 건너뛴다
    (흐름은 앞에서 뒤로만 가므로 뒤 단원을 바꿔도 앞쪽 문제는 그대로다). prune 이 꺼져 있으면 2026-09~11 의 탐색 그대로다."""
    errs, npg, infos, pm = start
    goal = goal or (lambda es: not bl.layout_errors(es))
    best = (*placement_score(errs, npg), dict(pos0 or {}))
    best_errs, best_pm = errs, pm
    tried = 0
    spent = lambda: budget is not None and tried >= budget
    for u in units:
        if (only is not None and u.anchor not in only) or spent():
            continue
        if prune:
            if goal(best_errs):
                break
            last = _last_problem_page(best_errs)
            if last is not None and (best_pm.get(u.anchor) or 0) > last:
                continue
        info = infos.get(u.anchor) or {}
        # 그림(2026-09-27): 같은 절 안의 다른 문단 뒤로 옮겨 본다 — 뒤쪽부터(그림이 너무 일찍 와서 단이 비는 일이 많다)
        for fid, fch in (info.get("fig_choices") or {}).items():
            key = f"{u.anchor}#fig:{fid}"
            # 같은 절 안 다른 자리(뒤쪽부터) → 지금 자리에서 줄이기(0.85·0.75배)
            fopts = [({key: p_}) for p_ in sorted((q for q in fch if q != info["fig_at"].get(fid)), reverse=True)[:6]]
            fopts += [{f"{u.anchor}#figscale:{fid}": s} for s in (0.85, 0.75)]
            for opt in fopts:
                if not bl.layout_errors(errs) or spent():
                    break
                tried += 1
                cand = dict(best[2], **opt)
                e2, g2, _, p2 = trial(cand)
                score = (*placement_score(e2, g2), cand)
                if score[:2] < best[:2]:
                    best, best_errs, best_pm = score, e2, p2
                if not bl.layout_errors(e2):
                    errs = e2
                    break
        if not info.get("diagram") or (prune and goal(best_errs)):
            continue
        # 기본 위치(치료 절 뒤)에 가까운 곳부터 — 흐름 도식이 관련 본문에서 멀어지지 않게
        d0 = info["dia_default"]
        later = sorted(q for q in info["dia_choices"] if q > d0)
        earlier = sorted((q for q in info["dia_choices"] if q < d0), reverse=True)
        order = later + earlier    # 빈 공간은 대개 도식이 너무 일찍 와서 생긴다 — 뒤쪽부터
        per_unit = 0                          # 단원마다 따로 센다 — 앞 단원이 예산을 다 쓰면 뒤 단원은 시도조차 못 했다(2026-09-22)
        # 두 단 폭 도식: ① 아래 여백으로 좁은 띠 넘기기 ② 지금 자리에서 줄이기 ③ 한 단으로 ④ 자리 옮기기
        full = (info.get("diagram") or {}).get("place") == "full"
        at = info["dia_at"]
        opts = []
        if full:
            opts += [(at, 1.0, pad, False) for pad in (14, 28, 42)]
            opts += [(at, f, 0, False) for f in (0.88, 0.76)]
            if fit_diagram(u.concept["diagram"], force_col=True)["ok"]:
                opts += [(q, 1.0, 0, True) for q in [at] + order[:3]]
        opts += [(q, 1.0, 0, False) for q in order] + [(q, 0.88, 0, False) for q in order[:4]]
        for p_, shrink, pad, col in opts:
            if (p_ == at and shrink == 1.0 and not pad and not col) or per_unit >= 20 or spent():
                continue
            if (info.get("diagram") or {}).get("pt", 99) * shrink < DIA_SHRINK_FLOOR_PT:
                continue
            per_unit += 1
            tried += 1
            cand = dict(best[2], **{u.anchor: p_, u.anchor + "#shrink": shrink, u.anchor + "#pad": pad, u.anchor + "#col": col})
            e2, g2, _, p2 = trial(cand)
            score = (*placement_score(e2, g2), cand)
            if score[:2] < best[:2]:
                best, best_errs, best_pm = score, e2, p2
            if not bl.layout_errors(e2) or (prune and goal(best_errs)):
                break
    return best[2], tried


def settle_bands(units: list[Unit], trial, state: tuple, pos: dict, prune: bool = False) -> tuple[dict, int]:
    """고른 배치에 두 단 도식 아래 좁은 띠가 남았을 때 — 책 앞쪽 도식부터 차례로 아래 여백을 정한다 → (배치, 시도 수).

    앞 도식의 여백이 뒤 내용을 밀어 뒤 도식에 새 띠를 만들 수 있다. 판단 기준 = (배치 외 오류, −첫 문제 쪽, 문제 수, 쪽 수):
    앞쪽 문제를 뒤로 밀어내며 차례로 정하고, 끝에 원래 배치와 문제 수로 비교한다."""
    errs, npg, infos, pm = state

    def pkey(es: list[str], pages: int) -> tuple:
        le = bl.layout_errors(es)
        first = min([int(m.group(1)) for e in le for m in [re.match(r"(\d+)쪽", e)] if m] or [10 ** 6])
        return (len(es) - len(le), -first, len(le), pages)

    before = placement_score(errs, npg)
    cur = (pkey(errs, npg), dict(pos))
    cur_errs, cur_pm = errs, pm
    tried = 0
    for u in units:
        if (infos.get(u.anchor, {}).get("diagram") or {}).get("place") != "full":
            continue
        if prune:
            last = _last_problem_page(cur_errs)
            if last is not None and (cur_pm.get(u.anchor) or 0) > last:
                continue
        for pad in (14, 28, 42):
            tried += 1
            cand = dict(cur[1], **{u.anchor + "#pad": pad})
            e2, g2, _, p2 = trial(cand)
            if pkey(e2, g2) < cur[0]:
                cur, cur_errs, cur_pm = (pkey(e2, g2), cand), e2, p2
        if cur[0][2] == 0:
            break
    if (cur[0][2] + 100 * cur[0][0], cur[0][3]) < before:
        return cur[1], tried
    return pos, tried


class MeasuredBook:
    """측정용 탭에 올려 둔 책 한 권. `evaluate(pos)` 가 그 배치의 (배치 문제, 쪽 수, 단원 정보, 단원 쪽)을 PDF 없이 준다.

    배치가 달라진 단원만 `unit_html` 로 다시 만들어 갈아 끼운다 — 마지막 PDF 와 같은 함수가 만든 HTML 이다."""

    def __init__(self, browser, box: tuple[float, float], title: str, units: list[Unit], cfg: dict, questions: dict,
                 meta: dict, fonts: dict, changes: list[str]):
        html_text, self.infos = book_html(title, units, cfg, questions, meta, None, fonts, changes, {})
        self.title, self.units, self.cfg, self.questions = title, units, cfg, questions
        self.sig = {u.anchor: () for u in units}
        self.lab = bl.Lab(browser, html_text, box)

    @staticmethod
    def unit_sig(anchor: str, pos: dict) -> tuple:
        return tuple(sorted(((k, v) for k, v in pos.items() if k == anchor or k.startswith(anchor + "#")), key=lambda kv: kv[0]))

    def evaluate(self, pos: dict) -> tuple[list[str], int, dict, dict]:
        swaps = []
        for u in self.units:
            sig = self.unit_sig(u.anchor, pos)
            if sig != self.sig[u.anchor]:
                h, info = unit_html(u, self.cfg, self.questions, self.title, pos.get(u.anchor),
                                    bool(pos.get(u.anchor + "#crit_end")), pos)
                swaps.append((u.anchor, h))
                self.infos[u.anchor], self.sig[u.anchor] = info, sig
        m = self.last = self.lab.measure(swaps)
        titles = {u.anchor: u.title for u in self.units}
        errs = bl.problems(m, MEASURE_MARGIN) + [f"도식이 한 쪽에 온전히 있지 않다: {titles.get(a, a)}" for a in m.get("split") or []]
        return errs, int(m["pages"]), dict(self.infos), m["pm"]

    def close(self) -> None:
        self.lab.close()


def build(cfg: dict, events: list[dict], state_dir: Path, out_dir: Path, force: bool = False,
          only: str | None = None, want_preview: bool = False, fail_on: str | None = None,
          layout: str | None = None) -> dict:
    """layout = 배치를 정하는 방식 — "measure"(기본: 한 번 올려 재고 고른 배치만 PDF 로) · "search"(지금까지의 방식: 선택지마다 PDF 로).
    비우면 books_config.yaml `layout`(없으면 measure). `layout_search` 에 적힌 책은 언제나 search."""
    layout = layout or str(cfg.get("layout") or "measure")
    if layout not in ("measure", "search"):
        raise ValueError(f"layout 은 measure · search 중 하나: {layout}")
    probe: dict = {}                  # 인쇄 쪽 상자(탐침 PDF 로 한 번 잰다 — 책마다 다시 재지 않는다)
    started = now_kst()
    date = started.strftime("%Y-%m-%d")
    manifest_path = state_dir / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8")) if manifest_path.exists() else {"books": {}}
    run: dict[str, Any] = {"started": started.isoformat(timespec="seconds"), "built": [], "skipped": [], "failed": {},
                           "retry": [], "previews": [], "validation": {}, "notes": {}}
    concepts, cerrs = load_concepts()
    questions = load_questions()
    S = ll.states(events, {q: m.get("objective") for q, m in questions.items() if m.get("objective")})
    source_state = json.loads(SOURCE_CHECKS.read_text(encoding="utf-8")) if SOURCE_CHECKS.exists() else {}
    books = plan(concepts, questions, S, cfg, source_state)
    run["concept_errors"] = cerrs
    live = {t for b in books.values() for t, _ in volumes(b, cfg)}
    for t_, m_ in manifest["books"].items():
        if t_ not in live and not m_.get("retired"):
            # 이 판형 기준으로 실을 단원이 없는 책(예: 학습 목표 없는 문항 오답만 있던 책). 드라이브의 옛 파일은 지우지 않는다.
            m_["retired"] = date
            run.setdefault("retired", []).append(t_)
    fonts = {"regular": find_font(cfg["fonts"]["regular"]), "bold": find_font(cfg["fonts"]["bold"])}
    out_dir.mkdir(parents=True, exist_ok=True)
    todo = []
    for b in books.values():
        for title, units in volumes(b, cfg):
            if only and only not in (b.name, title):
                continue
            hsh = volume_hash(title, units, [], cfg, questions, b.elsewhere)
            prev = manifest["books"].get(title, {})
            fname = f"MedKOS_학습서_{slug(title)}.pdf"
            same = prev.get("hash") == hsh
            uploaded = (prev.get("drive") or {}).get("version") == prev.get("version")
            if not force and same and ((out_dir / fname).exists() or uploaded):
                run["skipped"].append(title)          # 변화 없음(최신본이 로컬 또는 드라이브에 있다)
                continue
            todo.append((title, [et.unit(u) for u in units], hsh, prev, fname, b.elsewhere))
    if not todo:
        run["result"] = "skipped"
        run["finished"] = now_kst().isoformat(timespec="seconds")
        _write_run(state_dir, run)
        return run
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        try:
            for title, units, hsh, prev, fname, elsewhere in todo:
                try:
                    if fail_on and fail_on == title:
                        raise RuntimeError("시험용 강제 실패(--fail-on)")
                    # 내용이 같으면(업로드 재시도·새 러너) 판 번호를 올리지 않는다 — 되풀이해도 같은 결과
                    version = int(prev.get("version", 0)) + (0 if prev.get("hash") == hsh and prev.get("version") else 1)
                    meta = {"version": version, "date": date, "elsewhere": elsewhere}
                    changes = prev.get("changes", []) if prev.get("hash") == hsh else _changes(prev, units)
                    footer = f"{title} · 판 {version} · {date}"
                    tmp = out_dir / (fname + ".building.pdf")
                    stats = {"renders": 0}

                    def render_once(dia_pos: dict[str, int], passes: int = 3, pm: dict | None = None) -> tuple[list, list, dict, dict, int]:
                        new: dict = {}
                        for _ in range(passes):         # 차례 쪽 번호를 넣고 흐름이 안정될 때까지
                            html_text, infos = book_html(title, units, cfg, questions, meta, pm, fonts, changes, dia_pos)
                            render_pdf(browser, html_text, tmp, footer)
                            stats["renders"] += 1
                            new = locate(tmp)
                            # 차례에 실리는 것은 단원 쪽뿐이다 — 측정으로 얻은 쪽 번호(pm)가 맞으면 한 번에 끝난다
                            if pm is not None and all(new.get(u.anchor) == pm.get(u.anchor) for u in units):
                                break
                            pm = new
                        set_metadata(tmp, title, meta)
                        errs, notes = validate_pdf(tmp, title, units, new, infos)
                        import pymupdf
                        with pymupdf.open(tmp) as d_:
                            npg = d_.page_count
                        return errs, notes, new, infos, npg

                    def pdf_trial(pos: dict) -> tuple[list, int, dict, dict]:
                        e2, _, p2, i2, g2 = render_once(pos, passes=1)
                        return e2, g2, i2, p2

                    layout_err = bl.layout_errors
                    mode = "search" if title in (cfg.get("layout_search") or []) else layout
                    pos: dict = {}
                    tried, searched, surprise, fell_back = 0, False, [], ""
                    book = None
                    if mode == "measure":
                        # 한 번 올려 재는 배치 — 책을 Chromium 에 올려 두고 바뀐 단원만 갈아 끼워 잰다. PDF 는 고른 배치로만 그린다.
                        try:
                            if "error" in probe:        # 탐침이 한 번 실패한 환경 — 책마다 다시 해 보지 않는다
                                raise RuntimeError(probe["error"])
                            if "box" not in probe:
                                try:
                                    probe["box"] = bl.print_box(lambda h_, p_: render_pdf(browser, h_, p_, ""), PAGE)
                                except Exception as e:
                                    probe["error"] = f"쪽 상자 탐침 실패 — {type(e).__name__}: {e}"
                                    raise RuntimeError(probe["error"])
                            book = MeasuredBook(browser, probe["box"], title, units, cfg, questions, meta, fonts, changes)
                            e0, g0, i0, p0 = book.evaluate({})
                            pred, ppm = e0, p0
                            if layout_err(e0):
                                searched = True
                                pos, tried = search_placement(units, book.evaluate, (e0, g0, i0, p0), prune=True)
                                pred, g1, i1, ppm = book.evaluate(pos)
                                if any("좁은 띠" in e for e in pred):
                                    pos, t2 = settle_bands(units, book.evaluate, (pred, g1, i1, ppm), pos, prune=True)
                                    tried += t2
                                    pred, g1, i1, ppm = book.evaluate(pos)
                        except Exception as e:          # 측정이 안 되는 책 · 환경 — 지금까지의 탐색(PDF 로 그려 보기)으로 되돌아간다
                            fell_back = f"{type(e).__name__}: {str(e)[:160]}"
                            mode, pos, tried, searched = "search", {}, 0, False
                        finally:
                            if book:
                                book.close()
                    if mode == "measure":
                        errs, notes, pm, infos, npg = render_once(pos, pm=ppm)
                        # 측정이 예측하지 못한 배치 오류가 실제 PDF 에 있으면(측정은 큰 책에서 1% 안팎이 실제와 다르다) 그 쪽 둘레의
                        # 단원만 지금까지의 탐색으로 — PDF 로 그려 보며 — 고친다. 예측했던 오류는 측정 탐색이 이미 선택지를 다 써 본 것이다.
                        known = {bl.error_key(e) for e in layout_err(pred)}
                        surprise = [e for e in layout_err(errs) if bl.error_key(e) not in known]
                        if surprise:
                            searched = True
                            near = units_near(units, pm, [bl.error_key(e)[0] for e in surprise])
                            pos2, t2 = search_placement(units, pdf_trial, (errs, npg, infos, pm), pos0=pos, prune=True, only=near,
                                                        budget=REPAIR_RENDERS,
                                                        goal=lambda es: all(bl.error_key(e) in known for e in layout_err(es)))
                            tried += t2
                            pos = pos2
                            if t2:                      # 시도들이 임시 PDF 를 덮어썼다 — 고른 배치로 다시 그린다
                                errs, notes, pm, infos, npg = render_once(pos, pm=pm)
                    else:
                        errs, notes, pm, infos, npg = render_once(pos)
                        if layout_err(errs):
                            # 큰 도식이 전체 너비 표 바로 뒤에 오면 쪽 끝의 남은 높이에 못 들어가 다음 쪽으로 밀린다 —
                            # 도식을 다른 절 뒤로 옮겨 가며 빈 공간이 가장 적은 배치를 고른다(단원 내용 순서는 그대로).
                            searched = True
                            pos, tried = search_placement(units, pdf_trial, (errs, npg, infos, pm))
                            # 마지막: 고른 배치 위에서도 두 단 도식 아래 좁은 띠가 남으면 그 도식 아래 여백으로 넘긴다(자리·축소를 바꾼 뒤라 다시 본다)
                            errs, notes, pm, infos, npg = render_once(pos)
                            if any("좁은 띠" in e for e in errs):
                                pos, t2 = settle_bands(units, pdf_trial, (errs, npg, infos, pm), pos)
                                tried += t2
                                errs, notes, pm, infos, npg = render_once(pos)
                    run.setdefault("renders", {})[title] = stats["renders"]
                    if searched or fell_back:
                        rec = {"mode": mode, "tried": tried, "renders": stats["renders"], "diagram_after_section": pos}
                        if surprise:
                            rec["unpredicted"] = surprise[:8]
                        if fell_back:
                            rec["measure_failed"] = fell_back
                        run.setdefault("layout_trials", {})[title] = rec
                    # 어떤 배치로도 없애지 못한 빈 공간은 책 전체를 막지 않고 참고로 남긴다(이전 판형의 책이 계속 남는 편이 더 나쁘다)
                    left = layout_err(errs)
                    if left:
                        errs = [e for e in errs if e not in left]
                        notes = notes + [f"배치 탐색 뒤에도 남은 빈 공간: {e}" for e in left]
                    run["validation"][title] = errs
                    run["notes"][title] = notes
                    if errs:
                        raise RuntimeError("검증 실패: " + "; ".join(errs[:6]))
                    final = out_dir / fname
                    tmp.replace(final)                 # 검증을 통과한 뒤에만 최신본을 바꾼다
                    import pymupdf
                    with pymupdf.open(final) as d:
                        pages = d.page_count
                    manifest["books"][title] = {
                        "hash": hsh, "version": version, "date": date, "file": fname, "pages": pages,
                        "template_version": cfg.get("template_version"),
                        "units": {u.key: {"title": u.title, "page": (pm or {}).get(u.anchor),
                                          "concept_hash": (u.concept or {}).get("hash"),
                                          "concept_version": (u.concept or {}).get("version")} for u in units},
                        "drive": prev.get("drive"), "archive": prev.get("archive", []), "changes": changes,
                    }
                    run["built"].append(title)
                    if want_preview:
                        run["previews"] += [str(p) for p in preview(final, out_dir / "_preview")]
                except Exception as e:                  # 이 책만 실패 — 이전 PDF·기록은 그대로
                    run["failed"][title] = f"{type(e).__name__}: {e}"
                    run["retry"].append(title)
                    run.setdefault("trace", {})[title] = traceback.format_exc()[-1500:]
                    bad = out_dir / (fname + ".building.pdf")
                    if bad.exists():                   # 진단용으로만 남긴다(최신본·업로드 대상 아님)
                        bad.replace(out_dir / (fname[:-4] + ".failed.pdf"))
            if run["built"]:
                metas = [{"title": t, "file": m["file"], "version": m["version"], "pages": m.get("pages", "?"),
                          "units": [{"key": k, **v} for k, v in m["units"].items()]}
                         for t, m in sorted(manifest["books"].items()) if not m.get("retired")]
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
    _append_changelog(state_dir, run, manifest)
    return run


def _write_run(state_dir: Path, run: dict) -> None:
    state_dir.mkdir(parents=True, exist_ok=True)
    (state_dir / "last_run.json").write_text(json.dumps(run, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")


def _append_changelog(state_dir: Path, run: dict, manifest: dict) -> None:
    """판 기록(저장소·앱 쪽 보존용). PDF 에는 내용 변경만 싣지만 여기에는 판형 변경도 남긴다."""
    if not run["built"] and not run["failed"]:
        return
    lines = [f"\n## {run['started']}\n"]
    for t in run["built"]:
        m = manifest["books"][t]
        lines.append(f"- {t} 판 {m['version']} ({m['pages']}쪽, 판형 {m.get('template_version')}): "
                     + ("; ".join(m.get("changes") or []) or "내용 변경 없음"))
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
    ap.add_argument("--layout", choices=["measure", "search"],
                    help="배치를 정하는 방식 — measure(기본: 한 번 올려 재기) · search(선택지마다 PDF 로 그려 보기 — 느리다)")
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
    run = build(cfg, events, state_dir, out_dir, force=a.force, only=a.only, want_preview=a.preview, fail_on=a.fail_on,
                layout=a.layout)
    print(json.dumps({k: run[k] for k in ("result", "built", "skipped", "failed", "retry")}, ensure_ascii=False, indent=1))
    for t, n in (run.get("renders") or {}).items():
        lt = (run.get("layout_trials") or {}).get(t) or {}
        print(f"  배치 {t}: PDF {n}번" + (f" · {lt.get('mode')} 탐색 {lt.get('tried')}번" if lt else "")
              + (f" · 측정 실패 → 옛 탐색({lt['measure_failed']})" if lt.get("measure_failed") else "")
              + (f" · 예측에 없던 오류 {len(lt['unpredicted'])}건을 PDF 로 고침" if lt.get("unpredicted") else ""))
    for t, errs in run.get("validation", {}).items():
        print(f"  검증 {t}: {'통과' if not errs else errs}")
    for t, ns in run.get("notes", {}).items():
        for n in ns:
            print(f"  참고 {t}: {n}")
    if a.upload:
        import drive_books
        up = drive_books.upload(cfg, state_dir, out_dir, run)
        print(json.dumps(up, ensure_ascii=False, indent=1))
        if up.get("result") == "failed":
            return 1
    return 1 if run["result"] in ("failed",) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
