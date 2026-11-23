"""note_parts.py — 정리본 원고에서 **보여 주는 조각**을 풀어낸다(2026-11-23 vNext Phase 3).

웹 앱(export_concepts_web.py → docs/learn.js)과 PDF 학습서(build_books.py)가 같은 풀이를 쓴다 — 두 곳이 따로 풀면 모양이 갈라진다.
원고(정리본 .md)는 고치지 않는다: 판형 2 가 이미 정해 둔 머리말(「결론:」「시험 단서:」「왜:」 · 「시험 쟁점」의 네 칸)을 읽기만 한다.
화면도 파일도 쓰지 않는 순수 함수뿐이다 — `test_learning_books.py` `NoteParts` 가 시험한다.

  summary_slots(summary)      요약 줄 → 결론 · 발문 단서 · 기전 · 금기 칸(머리말이 없는 줄은 「더 알아 둘 것」)
  exam_issues(section_html)   「시험 쟁점」 절 → 해당 없음(대조한 곳) 또는 쟁점 목록(시험 기준 / 다른 기준 / 왜 다른가 / 시험에서는)
  is_issue_title(title)       그 절의 제목인가
  series(concepts)            같은 질환(id 의 셋째 마디)의 다른 목표 단원 — 기전 → 진단 → 감별 → 검사 → 치료 → 다음 처치 순
  outline_order(books)        {슬롯 id: (책, 책 안 순서)} — 서가 · 목차를 기본틀 순서로 늘어놓는다
"""
from __future__ import annotations

import html
import re
from typing import Any

# 요약 줄의 머리말 → (칸 종류, 화면에 적는 이름). 이름은 글자 라벨만 쓴다(장식 이모티콘 없음 — CLAUDE.md 「시각 절제」).
SLOT_LABEL = {"conclusion": "핵심 결론", "cue": "발문 단서", "why": "왜 이 판단인가", "avoid": "금기 · 피할 약", "more": ""}
_SLOT_PREFIX = [
    (re.compile(r"^결론\s*[:：]\s*"), "conclusion"),
    (re.compile(r"^시험\s*단서\s*[:：]\s*"), "cue"),
    (re.compile(r"^왜\s*[:：]\s*"), "why"),
    # 「쓰지 않는 약:」「쓰지 않는다:」「쓰지 않는 것:」「쓰지 않는 처치:」「피할 약:」「금기:」
    (re.compile(r"^(?:쓰지\s*않는(?:다|\s*[가-힣]{1,4})?|피할\s*[가-힣]{1,4}|금기)\s*[:：]\s*"), "avoid"),
]


def summary_slots(summary: list[Any] | None) -> list[dict]:
    """요약 줄마다 {kind, label, text, raw, groups}. raw = 머리말 그대로(「결론:」) — 필기 종이의 옛 판형이 줄 모양을 지키려고 쓴다.
    groups = 그 칸을 줄로 나눈 것(slot_groups) — 한 줄에 이어 쓴 나열을 덩이마다 줄을 바꿔 보여 준다."""
    out = []
    for line in summary or []:
        s = str(line).strip()
        kind, raw = "more", ""
        for pat, k in _SLOT_PREFIX:
            m = pat.match(s)
            if m:
                kind, raw, s = k, m.group(0).strip(), s[m.end():]
                break
        out.append({"kind": kind, "label": SLOT_LABEL[kind], "text": s, "raw": raw, "groups": slot_groups(kind, s)})
    return out


# ── 칸 안의 줄 나누기(2026-11-23 사용자 「약제 같은 부분이 다 한 줄이라 읽기 어렵다 — 줄을 띄워」) ─────────────
# 원고는 한 줄이다(「베라파밀·딜티아젬(음성 변력), NSAID·티아졸리딘디온, ACE 억제제+ARB+MRA 3제」). 보여 줄 때 덩이마다 줄을 바꾼다.
# 실제 요약 1,000여 줄로 본 규칙 — 넓히기 전에 `NoteParts` 시험의 예를 늘려 확인한다:
#   · 모든 칸: 문장 끝(「다. 」)에서 줄을 바꾼다.
#   · 발문 단서 · 금기(나열이 본래 모양인 칸): 괄호 · 낫표 · 근거 표시 **밖의** 쉼표(, )와 빗금( / )에서 줄을 바꾼다.
#   · 금기: 가운뎃점(·)으로 셋 이상 이은 덩이도 한 줄씩(도파민 1차·전분 수액·CVP 고정 목표).
#   · 결론 · 왜(문장인 칸): 쉼표로는 자르지 않는다. 다만 「… 약은 A·B·C·D다」처럼 **「은/는」 뒤가 끝까지 나열**이면 머리 줄 + 항목 줄로 편다.
#   가운뎃점을 아무 데서나 자르지 않는 까닭: 「열감·부종·통증(6주 미만) — 화농성 관절염·통풍·골절이 …」 같은 문장이 조각난다.
_OPEN, _CLOSE = "(（[「『", ")）]」』"
_SENT_END = re.compile(r"(?<=[가-힣a-zA-Z0-9)\]」%])\.\s+(?=\S)")
_CONNECT = (" — ", "→", " = ", " vs ", " + ", "+ ", " 또는 ", "면 ", "하고 ")       # 이런 말이 든 덩이는 나열이 아니라 문장이다


def _top_split(s: str, seps: tuple[str, ...]) -> list[str]:
    """괄호 · 낫표 · 근거 표시([[…]]) 밖에서만 seps 로 자른다(구분자는 버린다)."""
    out, buf, depth, i = [], [], 0, 0
    while i < len(s):
        ch = s[i]
        if ch in _OPEN:
            depth += 1
        elif ch in _CLOSE and depth:
            depth -= 1
        if depth == 0:
            hit = next((x for x in seps if s.startswith(x, i)), None)
            if hit:
                out.append("".join(buf))
                buf = []
                i += len(hit)
                continue
        buf.append(ch)
        i += 1
    out.append("".join(buf))
    return [x.strip() for x in out if x.strip()]


def _outside(s: str) -> str:
    """괄호 · 낫표 · 근거 표시 안을 지운 글 — 나열인지 문장인지 볼 때 쓴다."""
    out, depth = [], 0
    for ch in s:
        if ch in _OPEN:
            depth += 1
        elif ch in _CLOSE and depth:
            depth -= 1
        elif depth == 0:
            out.append(ch)
    return "".join(out)


def _dot_items(part: str) -> list[str] | None:
    """가운뎃점으로 셋 이상 이은 **순수한 나열**이면 항목들, 아니면 None."""
    items = _top_split(part, ("·",))
    if len(items) < 3 or any(x in _outside(part) for x in _CONNECT):
        return None
    return items


def slot_groups(kind: str, text: Any) -> list[dict]:
    """칸의 글 → [{lead, items}] — lead 는 나열 앞의 머리 줄(없으면 ""), items 는 한 줄씩 보일 덩이.
    나눌 것이 없으면 [{lead: "", items: [글 전체]}] 한 덩이다(그리는 쪽은 그때 줄 목록을 세우지 않는다)."""
    s = str(text or "").strip()
    if not s:
        return []
    groups: list[dict] = []

    def plain(x: str) -> None:
        if groups and not groups[-1]["lead"]:
            groups[-1]["items"].append(x)
        else:
            groups.append({"lead": "", "items": [x]})

    for sent in _SENT_END.split(s):
        sent = sent.strip()
        if not sent:
            continue
        if kind in ("cue", "avoid"):
            for part in _top_split(sent, (", ", " / ")):
                items = _dot_items(part) if kind == "avoid" else None
                for x in items or [part]:
                    plain(x)
            continue
        lead, items = _lead_list(sent) if kind in ("conclusion", "why") else ("", None)
        if items:
            groups.append({"lead": lead, "items": items})
        else:
            plain(sent)
    return groups


def _lead_list(sent: str) -> tuple[str, list[str] | None]:
    """「… 약은 A·B·C·D다」 → (「… 약은」, [A, B, C, D다]). 문장이 통째로 「머리말 + 짧은 이름들의 나열」일 때만 편다.

    조건(실제 요약에서 오탐 5건을 걸러 낸 값): 쉼표가 없고 · 첫 가운뎃점 앞의 마지막 「은/는 」까지가 머리말이고 · 항목이 셋 이상이며 ·
    모든 항목이 괄호 밖 16자 이하 · 띄어쓰기 한 번 이하(이름이지 문장이 아니다). 「… 종괴는 수술 전에 AFP·β-hCG·LDH 를 잰다」 같은 문장은 걸린다."""
    if ", " in _outside(sent):
        return "", None
    # 괄호 · 낫표 밖의 글자 자리만 본다(「RAAS 차단(ACE 억제제·ARB 또는 ARNI)」 안의 가운뎃점 · 「또는」에 걸리지 않게)
    top, depth = [], 0
    for i, ch in enumerate(sent):
        if ch in _OPEN:
            depth += 1
        elif ch in _CLOSE and depth:
            depth -= 1
        elif depth == 0:
            top.append(i)
    first = next((i for i in top if sent[i] == "·"), -1)
    if first < 0:
        return "", None
    cut = max((i for i in top if i < first and sent[i] in "은는" and sent[i + 1:i + 2] == " " and sent[i - 1:i] != "또"), default=-1)
    if cut < 2:
        return "", None
    lead, rest = sent[:cut + 1].strip(), sent[cut + 2:].strip()
    items = _dot_items(rest)
    if not items:
        return "", None
    for x in items:
        o = _outside(x).strip().rstrip(".")
        if len(o) > 16 or o.count(" ") > 1:
            return "", None
    return lead, items


ISSUE_TITLE = "시험 쟁점"
_FIELDS = [("exam", "시험 기준"), ("other", "다른 기준"), ("why", "왜 다른가"), ("onexam", "시험에서는")]
_FIELD_RE = re.compile(r"(?:^|\s/\s|\s*/\s*)(시험 기준|다른 기준|왜 다른가|시험에서는)\s*[:：]\s*")
_LI_RE = re.compile(r"<li>(.*?)</li>", re.S)
_HEAD_RE = re.compile(r"^\s*<strong>\s*(Z\d+)\s*([^·<]*?)\s*(?:·\s*(.*?))?\s*</strong>\s*(?:—|-|:)?\s*", re.S)
_TAGS = re.compile(r"<[^>]+>")


def is_issue_title(title: Any) -> bool:
    return str(title or "").strip().startswith(ISSUE_TITLE)


def _plain(s: str) -> str:
    return html.unescape(_TAGS.sub("", s)).strip()


def exam_issues(section_html: str) -> dict:
    """「시험 쟁점」 절의 HTML(정화된 본문) → {"none": True, "ref": "대조: …"} 또는 {"none": False, "issues": [...]}.

    쟁점 하나 = {id: "Z1", kind: "충돌", title, exam, other, why, onexam}(칸 값은 HTML 조각 — 근거 표시 `[[…]]` 가 들어 있을 수 있다).
    네 칸 가운데 하나도 못 찾은 항목은 body 에 통째로 담는다(모양을 지어내지 않는다).
    """
    items = _LI_RE.findall(section_html or "")
    text = _plain(section_html or "")
    if not items or (len(items) == 1 and _plain(items[0]).startswith("해당 없음")) or text.startswith("해당 없음"):
        m = re.search(r"해당 없음\s*[(（]\s*(.*?)\s*[)）]\s*$", _plain(items[0]) if items else text)
        return {"none": True, "ref": m.group(1) if m else ""}
    issues = []
    for i, li in enumerate(items, 1):
        m = _HEAD_RE.match(li)
        zid, kind, title, rest = (m.group(1), (m.group(2) or "").strip(), (m.group(3) or "").strip(), li[m.end():]) if m else (f"Z{i}", "", "", li)
        it = {"id": zid, "kind": kind, "title": _plain(title), "exam": "", "other": "", "why": "", "onexam": "", "body": ""}
        marks = list(_FIELD_RE.finditer(rest))
        if marks:
            names = {ko: key for key, ko in _FIELDS}
            for j, mk in enumerate(marks):
                end = marks[j + 1].start() if j + 1 < len(marks) else len(rest)
                it[names[mk.group(1)]] = rest[mk.end():end].strip()
            lead = rest[:marks[0].start()].strip()
            if lead:
                it["body"] = lead
        else:
            it["body"] = rest.strip()
        issues.append(it)
    return {"none": False, "issues": issues}


# 같은 질환의 단원을 늘어놓는 순서 — 판단이 흘러가는 순서(왜 생기나 → 무엇인가 → 무엇과 다른가 → 무엇을 찍나 → 무엇을 하나)
KIND_ORDER = ["기전", "진단", "감별", "검사 선택", "치료", "다음 처치", "금기", "예후"]


def series_key(cid: str) -> str:
    """정리본 id `cn.<과>.<주제>.<목표>` 의 <주제>. 과가 달라도(순환기 · 소아) 같은 질환이면 한 묶음이다."""
    p = str(cid).split(".")
    return p[2] if len(p) >= 4 and p[0] == "cn" else ""


def series(concepts: dict[str, dict]) -> dict[str, list[dict]]:
    """{정리본 id: [같은 질환의 단원 전부(자신 포함) — {id, title, kind}]}. 혼자인 정리본은 싣지 않는다."""
    groups: dict[str, list[str]] = {}
    for cid in concepts:
        k = series_key(cid)
        if k:
            groups.setdefault(k, []).append(cid)
    out: dict[str, list[dict]] = {}
    rank = {k: i for i, k in enumerate(KIND_ORDER)}
    for ids in groups.values():
        if len(ids) < 2:
            continue
        ids.sort(key=lambda x: (rank.get(str(concepts[x].get("objective_kind") or ""), len(KIND_ORDER)), x))
        row = [{"id": x, "title": str(concepts[x].get("title", "")), "kind": str(concepts[x].get("objective_kind") or "")} for x in ids]
        for x in ids:
            out[x] = row
    return out


def outline_order(books: dict[str, list]) -> dict[str, tuple[str, int]]:
    """{슬롯 id: (책, 책 안에서의 순서)} — outline.load() 의 books 를 받는다."""
    out: dict[str, tuple[str, int]] = {}
    for book, slots in books.items():
        for i, sl in enumerate(slots):
            out[sl.id] = (book, i)
    return out
