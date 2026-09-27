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

사용:
  python pipelines/build_books.py                       # 바뀐 책만 만들고 검증(업로드 없음)
  python pipelines/build_books.py --upload              # + Google Drive 갱신(drive_books.py)
  python pipelines/build_books.py --force --only 신장내과
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

import decision_diagram as dd
import english_terms as et
import learning_log as ll
import outline as ol
from concepts import BASIS, linked_questions, load_concepts, load_questions, render_cites, safe_url, source_numbers

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

    @property
    def anchor(self) -> str:
        return "u-" + re.sub(r"[^a-z0-9]+", "-", self.key.lower()).strip("-")


@dataclass
class Book:
    name: str
    units: list[Unit] = field(default_factory=list)
    pending: list[tuple[ll.State, dict]] = field(default_factory=list)   # 목표 없는 문항 오답 — PDF 에 싣지 않음(앱에 있음)


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
    return {"concept": (u.concept or {}).get("hash"), "version": (u.concept or {}).get("version"),
            "title": u.title, "src": u.flags,
            "auto": [p["key"] for p in auto_pitfalls(u, questions or {})],
            "stub": [] if u.concept else [(q, (questions or {}).get(q, {}).get("explanation")) for q in u.questions]}


def volume_hash(title: str, units: list[Unit], pending: list, cfg: dict, questions: dict | None = None) -> str:
    payload = {"t": title, "tv": cfg.get("template_version"), "gl": et.digest(),
               "units": [(u.key, unit_fingerprint(u, questions)) for u in units]}
    return hashlib.sha256(json.dumps(payload, ensure_ascii=False, sort_keys=True, default=str).encode()).hexdigest()[:20]


# ── 도식: 읽을 수 있는 크기로 한 단 또는 두 단 전체에 맞춘다 ──────────────
def fit_diagram(spec: dict, force_full: bool = False, shrink: float = 1.0) -> dict:
    """한 단 안(우선) 또는 두 단 전체(넓은 도식) — 2026-09-27 해리슨식 세로 2단.
    점수 = 항목 중간 끊김 ×0.4pt + 줄바꿈 ×0.12pt − 글자 크기. 두 단 전체는 흐름을 가르므로 +1.0pt, 양옆이 비면 더 벌점.
    한 단(92 mm)에서는 넓은 도식이 3 pt 까지 작아지거나 항목이 잘려(사용자: 「줄이 바뀌면 보기 불편」) 넓은 도식은 두 단 전체로 간다.
    shrink(<1) = 쪽 맞춤 탐색이 정한 축소(빈칸·좁은 띠를 없애려고, 글자 ≥ DIA_SHRINK_FLOOR_PT)."""
    H = (PAGE["h"] - PAGE["mt"] - PAGE["mb"]) * MM_PX
    places = [("column", COLW * MM_PX, H * 0.72, DIA_FLOOR_PT, 0.0),
              ("full", (PAGE["w"] - PAGE["ml"] - PAGE["mr"]) * MM_PX, H * 0.55, DIA_FULL_FLOOR_PT, 1.0)]
    if force_full:
        places = places[1:]
    paras = sum(len(str(x["text"]).split("\n")) for x in spec["nodes"])
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
    best = min(ok, key=lambda c: (c["score"], -c["scale"])) if ok else max(cands, key=lambda c: c["scale"])
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
.unit-head{break-inside:avoid; margin:3mm 0 1.6mm}
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
ul.pit li{background:var(--warn-soft); border-left:0.9mm solid var(--warn); padding:0.8mm 1.6mm; margin:0 0 0.7mm; break-inside:avoid}
ul.pit li > b:first-child{color:var(--warn)}
.pit .ex{color:var(--muted)}

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


def diagram_html(c: dict, anchor: str, force_full: bool = False, shrink: float = 1.0) -> tuple[str, dict | None]:
    """두 단 폭 도식은 「도식에 담기지 않은 조건·예외」까지 한 덩어리(두 단 폭·쪼개지 않음) — 쪽 끝 좁은 틈에서
    좌→우→다음 쪽으로 오가며 읽히던 문제(사용자 2026-09-27)."""
    spec = c.get("diagram")
    if not spec:
        return "", None
    fit = fit_diagram(spec, force_full, shrink)
    g, s = fit["geo"], fit["scale"]
    svg = dd.to_svg(g, None, dd.LIGHT)
    fig = (f'<figure class="dia"><figcaption>[도식] {esc(spec.get("title"))}</figcaption>'
           f'<div class="svgw" style="width:{g["w"] * s:.0f}px;height:{g["h"] * s:.0f}px">{svg}</div></figure>')
    notes = c.get("diagram_notes") or []
    nh = ('<div class="dnotes"><h4>도식에 담기지 않은 조건·예외</h4><ul>'
          + "".join(f"<li>{_cell(n, c, anchor)}</li>" for n in notes) + "</ul></div>") if notes else ""
    if fit["place"] == "full":
        return f'<div class="diablock">{fig}{nh}</div>', fit
    return fig + nh, fit


def figure_html(f: dict) -> tuple[str, str, dict]:
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
    flags = "".join(f' · <span class="flag">⚠ {esc(f)}</span>' for f in u.flags)
    # 제목·학습 목표·한눈에를 한 덩어리로 — 단 끝에 제목만 떨어지지 않게(사용자 2026-09-27)
    head = f'<div class="uh" id="{a}"><h2>{esc(u.title)}</h2><div class="um">{" · ".join(meta)}{flags}</div></div>'
    if c.get("objective"):
        head += f'<div class="goal"><span class="k">학습 목표</span>{_cell(c["objective"], c, a)}</div>'
    if c.get("summary"):
        head += '<div class="sum"><b>한눈에</b><ul>' + "".join(f"<li>{_cell(x, c, a)}</li>" for x in c["summary"]) + "</ul></div>"
    h = [f'<section class="unit"><div class="unit-head">{head}</div>']
    secs = c.get("sections") or []
    tables = [t for t in c.get("tables") or [] if isinstance(t, dict)]
    placed: set[str] = set()
    titles = [s["title"] for s in secs]
    crit_at = next((i for i, t in enumerate(titles) if t.startswith("치료")), len(secs))
    tx_at = crit_at
    if crit_end:                  # 배치 탐색: 기준표(두 단 전체)를 본문 끝으로 — 도식 바로 뒤 강제 단 나눔을 피한다
        crit_at = len(secs)
    # 본문을 블록(제목·문단·목록·표) 단위로 편다 — 큰 도식은 블록 경계 어디에든 끼울 수 있게(빈 공간을 줄이는 배치 탐색용)
    blocks: list[tuple[str, str]] = []            # (kind, html) kind: head · flow · span
    dia_default = None
    for i, s in enumerate(secs):
        if i == crit_at and c.get("criteria"):
            blocks.append(("span", criteria_tables(c, a)))
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
    if crit_at >= len(secs) and c.get("criteria"):
        blocks.append(("span", criteria_tables(c, a)))
    for tb in tables:
        if tb["id"] not in placed:
            blocks.append(("span" if tb.get("span") == "full" else "flow", table_html(tb, c, a)))
    if dia_default is None:
        dia_default = len(blocks)
    pits = [dict(p, cites=p.get("cites") or []) for p in c.get("pitfalls") or []] + auto_pitfalls(u, questions)
    if pits:
        blocks.append(("head", "<h3>혼동하기 쉬운 점</h3>"))
        items = []
        for pf in pits:
            cites = " ".join(render_cites(esc(f"[[{x}]]"), c, "pdf", a) for x in pf.get("cites") or [])
            items.append(f"<li><b>{esc(pf['contrast'])}</b> — {_cell(pf['point'], c, a)}"
                         + (f' <span class="ex">예외: {_cell(pf["exception"], c, a)}</span>' if pf.get("exception") else "")
                         + (f" {cites}" if cites else "") + "</li>")
        # 두세 항목씩 나눠 둔다 — 도식이 그 사이에도 들어갈 수 있게(목록은 같은 모양으로 이어 보인다)
        for k in range(0, len(items), 2):
            blocks.append(("flow", '<ul class="pit">' + "".join(items[k:k + 2]) + "</ul>"))
    force_full = dia_at == "full"
    choices = [k for k in range(1, len(blocks) + 1) if blocks[k - 1][0] != "head"]
    if dia_at is None or force_full or dia_at not in choices:
        dia_at = dia_default if dia_default in choices else (choices[-1] if choices else len(blocks))
    info["dia_at"], info["dia_default"], info["dia_choices"] = dia_at, dia_default, choices
    dh, fit = diagram_html(c, a, force_full, float((fig_pos or {}).get(f"{a}#shrink", 1.0)))
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
        kind_, fh, finfo = figure_html(f)
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
    for u in units:
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
        spans_ = [d["rect"] for d in p.get_drawings() if d.get("rect") is not None and d["rect"].width > 0.8 * full_w and d["rect"].height > 40]
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
            if any(abs(sp["size"] - hs) < 0.05 for hs in (h3_size, 8.8, 8.6)) and sp["flags"] & 16:
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


def build(cfg: dict, events: list[dict], state_dir: Path, out_dir: Path, force: bool = False,
          only: str | None = None, want_preview: bool = False, fail_on: str | None = None) -> dict:
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
            hsh = volume_hash(title, units, [], cfg, questions)
            prev = manifest["books"].get(title, {})
            fname = f"MedKOS_학습서_{slug(title)}.pdf"
            same = prev.get("hash") == hsh
            uploaded = (prev.get("drive") or {}).get("version") == prev.get("version")
            if not force and same and ((out_dir / fname).exists() or uploaded):
                run["skipped"].append(title)          # 변화 없음(최신본이 로컬 또는 드라이브에 있다)
                continue
            todo.append((title, [et.unit(u) for u in units], hsh, prev, fname))
    if not todo:
        run["result"] = "skipped"
        run["finished"] = now_kst().isoformat(timespec="seconds")
        _write_run(state_dir, run)
        return run
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        try:
            for title, units, hsh, prev, fname in todo:
                try:
                    if fail_on and fail_on == title:
                        raise RuntimeError("시험용 강제 실패(--fail-on)")
                    # 내용이 같으면(업로드 재시도·새 러너) 판 번호를 올리지 않는다 — 되풀이해도 같은 결과
                    version = int(prev.get("version", 0)) + (0 if prev.get("hash") == hsh and prev.get("version") else 1)
                    meta = {"version": version, "date": date}
                    changes = prev.get("changes", []) if prev.get("hash") == hsh else _changes(prev, units)
                    footer = f"{title} · 판 {version} · {date}"
                    tmp = out_dir / (fname + ".building.pdf")
                    def render_once(dia_pos: dict[str, int], passes: int = 3) -> tuple[list, list, dict, dict, int]:
                        pm = None
                        for _ in range(passes):         # 차례 쪽 번호를 넣고 흐름이 안정될 때까지
                            html_text, infos = book_html(title, units, cfg, questions, meta, pm, fonts, changes, dia_pos)
                            render_pdf(browser, html_text, tmp, footer)
                            new = locate(tmp)
                            if new == pm:
                                break
                            pm = new
                        set_metadata(tmp, title, meta)
                        errs, notes = validate_pdf(tmp, title, units, pm or {}, infos)
                        import pymupdf
                        with pymupdf.open(tmp) as d_:
                            npg = d_.page_count
                        return errs, notes, pm or {}, infos, npg

                    dia_pos: dict[str, int] = {}
                    errs, notes, pm, infos, npg = render_once(dia_pos)
                    layout_err = lambda es: [e for e in es if "빈 공간" in e or "고립된 제목" in e or "좁은 띠" in e]
                    tried = 0
                    if layout_err(errs):
                        # 큰 도식이 전체 너비 표 바로 뒤에 오면 쪽 끝의 남은 높이에 못 들어가 다음 쪽으로 밀린다 —
                        # 도식을 다른 절 뒤로 옮겨 가며 빈 공간이 가장 적은 배치를 고른다(단원 내용 순서는 그대로).
                        best = (len(layout_err(errs)), npg, dict(dia_pos))
                        for u in units:
                            info = infos.get(u.anchor) or {}
                            # 그림(2026-09-27): 같은 절 안의 다른 문단 뒤로 옮겨 본다 — 뒤쪽부터(그림이 너무 일찍 와서 단이 비는 일이 많다)
                            for fid, fch in (info.get("fig_choices") or {}).items():
                                key = f"{u.anchor}#fig:{fid}"
                                for pos in sorted((q for q in fch if q != info["fig_at"].get(fid)), reverse=True)[:6]:
                                    if not layout_err(errs):
                                        break
                                    tried += 1
                                    trial = dict(best[2], **{key: pos})
                                    e2, n2, p2, i2, g2 = render_once(trial, passes=1)
                                    score = (len(layout_err(e2)), g2, trial)
                                    if score[:2] < best[:2]:
                                        best = score
                                    if not layout_err(e2):
                                        errs = e2
                                        break
                            if not info.get("diagram"):
                                continue
                            # 기본 위치(치료 절 뒤)에 가까운 곳부터 — 흐름 도식이 관련 본문에서 멀어지지 않게
                            d0 = info["dia_default"]
                            later = sorted(q for q in info["dia_choices"] if q > d0)
                            earlier = sorted((q for q in info["dia_choices"] if q < d0), reverse=True)
                            order = later + earlier    # 빈 공간은 대개 도식이 너무 일찍 와서 생긴다 — 뒤쪽부터
                            per_unit = 0                          # 단원마다 따로 센다 — 앞 단원이 예산을 다 쓰면 뒤 단원은 시도조차 못 했다(2026-09-22)
                            # 두 단 폭 도식은 먼저 지금 자리에서 조금 줄여 본다(쪽 끝에 조금 모자라 밀리거나 좁은 띠가 남는 경우), 그다음 자리 옮기기
                            shrinks = [(info["dia_at"], f) for f in (0.88, 0.76)] if (info.get("diagram") or {}).get("place") == "full" else []
                            for pos, shrink in shrinks + [(q, 1.0) for q in order] + [(q, 0.88) for q in order[:4]]:
                                if (pos == info["dia_at"] and shrink == 1.0) or per_unit >= 16:
                                    continue
                                if (info.get("diagram") or {}).get("pt", 99) * shrink < DIA_SHRINK_FLOOR_PT:
                                    continue
                                per_unit += 1
                                tried += 1
                                trial = dict(best[2], **{u.anchor: pos, u.anchor + "#shrink": shrink})
                                e2, n2, p2, i2, g2 = render_once(trial, passes=1)
                                score = (len(layout_err(e2)), g2, trial)
                                if score[:2] < best[:2]:
                                    best = score
                                if not layout_err(e2):
                                    break
                        errs, notes, pm, infos, npg = render_once(best[2])
                        run.setdefault("layout_trials", {})[title] = {"tried": tried, "diagram_after_section": best[2]}
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
