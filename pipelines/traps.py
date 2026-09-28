"""
traps.py — 함정 계열(trap family): 등록부 · 문항 검사 · 모자란 계열 큐 · 비슷한 문항 찾기 (결정론).

왜 (2026-09-29 사용자 요청):
  외부 문항(경골 골절 뒤 부은 종아리, 발등동맥 맥박이 「잘 만져지지 않는다」, 오답 넷이 모두 혈전·혈관 처치, 정답 근막절개)과
  비슷한 MedKOS 문항을 찾아보니 구획증후군 7문항이 모두 「맥박은 만져진다」 판이었다. 같은 학습 목표를 **같은 함정**
  (맥박이 만져지니 안심 → 관찰·영상으로 미룸)으로만 물어 온 것이다. 사용자: 「맥박이 약한데 혈전 계열 오답」처럼 보기를
  가르는 함정 계열이 다른 부분이 파악되면, 그것도 고려해서 문항을 만들 수 있게 하고 싶다.

함정 계열 = 발문의 한 소견(cue)이 보기 한 무리(lure 계열)로 끌어당기는데 정답은 다른 무리(truth 계열)에 있는 구조.
  trap   쪽 문항 — cue 가 있고 오답에 lure 계열이 lure.min 개 이상, 정답은 truth 계열.
  mirror 쪽 문항 — cue 가 있는데 이번에는 lure 계열이 정답(mirror.when 의 조건)이고 truth 계열 보기가 오답.
  한쪽만 내면 「맥박이 약해도 혈관 문제는 아니다」 같은 과잉 일반화를 가르친다 — 그래서 두 쪽을 따로 센다.

  등록부  content/traps/<id>.yaml   파일 하나가 계열 하나(콘텐츠 레인 — publish.py 가 바뀌면 check 를 돌린다)
  문항    design.trap: {id: <계열 id>, side: trap|mirror}   KMLE·USMLE(lint_questions.py 가 등록부와 대조)
  영상(imaging) 카드는 빌더 파생물이라 표시하지도 세지도 않는다(비슷한 문항 찾기에는 나온다).
  외부 문항(학교 시험 등)의 원문은 저장소에 넣지 않는다 — 등록부에는 함정의 구조만 적는다.

사용:
  python pipelines/traps.py check                          # 등록부 + 표시한 문항 — 오류 0 이어야 게시
  python pipelines/traps.py list [--brief]                 # 계열별 문항 수(시험 × trap/mirror)와 표시 안 된 후보
  python pipelines/traps.py queue --exam kmle --limit 2    # 문항이 모자란 계열 — 루틴이 오늘 세트에 먼저 넣는다
  python pipelines/traps.py similar --file q.txt [--top 10]   # 외부 문항과 비슷한 MedKOS 문항 + 걸리는 계열
"""
from __future__ import annotations

import argparse
import collections
import json
import math
import re
import sys
from pathlib import Path
from typing import Any

import yaml

from question_design import question_text_pool

ROOT = Path(__file__).resolve().parent.parent
TRAP_DIR = ROOT / "content" / "traps"
EVENTS = ROOT / "state" / "learning_sync" / "events.json"

ID_RE = re.compile(r"^tr\.[a-z0-9-]+\.[a-z0-9-]+$")
OBJ_RE = re.compile(r"^cn\.[a-z0-9-]+\.[a-z0-9-]+\.[a-z0-9-]+$")
CITE_RE = re.compile(r"\[\[\??([a-z0-9][a-z0-9-]*)")
EXAMS = ("kmle", "usmle")
SIDES = ("trap", "mirror")
STATUS = ("active", "retired")
VERIFIED = ("text", "abstract", "citation")
REVIEW = ("unreviewed", "reviewed", "needs_revision")
MODEL_NAMES = re.compile(r"(claude|gpt|gemini|llama|model|모델|\bai\b)", re.IGNORECASE)
LETTERS = "ABCDE"
DEFAULT_WANT = {"trap": 1, "mirror": 1}
DEFAULT_LURE_MIN = 2
MAX_CANDIDATES = 5


# ── 등록부 ──────────────────────────────────────────────────────────────────
def _compile(pats: Any, where: str, errs: list[str]) -> list[re.Pattern]:
    out: list[re.Pattern] = []
    if not isinstance(pats, list) or not pats:
        errs.append(f"{where}.patterns 는 비어 있지 않은 정규식 목록이어야 한다")
        return out
    for i, p in enumerate(pats, 1):
        try:
            out.append(re.compile(str(p), re.IGNORECASE))
        except re.error as e:
            errs.append(f"{where}.patterns[{i}] 정규식 오류: {e}")
    return out


def _hit(rx: list[re.Pattern], text: str) -> bool:
    return any(r.search(str(text or "")) for r in rx)


def _texts(m: dict[str, Any]) -> str:
    """근거 표시([[출처]])를 찾을 서술 전부."""
    parts = [str(m.get("why", "") or "")]
    parts += [str(x) for x in m.get("discriminators") or []]
    parts += [str(x) for x in m.get("write_notes") or []]
    mir = m.get("mirror") if isinstance(m.get("mirror"), dict) else {}
    parts.append(str(mir.get("when", "") or ""))
    return "\n".join(parts)


def validate_entry(m: dict[str, Any], path: Path | None = None) -> tuple[dict[str, Any], list[str], list[str]]:
    """(쓸 수 있는 항목, 오류, 경고). 오류가 있는 항목은 문항 검사에 쓰지 않는다."""
    errs: list[str] = []
    warns: list[str] = []
    tid = str(m.get("id", "") or "")
    if not ID_RE.match(tid):
        errs.append(f"id '{tid}' 형식 오류 — tr.<과>.<계열> (소문자·숫자·하이픈)")
    if path is not None and path.stem != tid:
        errs.append(f"파일 이름({path.name})이 id 와 다르다 — <id>.yaml")
    for k in ("title", "found_note", "why"):
        if not str(m.get(k, "") or "").strip():
            errs.append(f"{k} 가 비어 있다")
    status = str(m.get("status", "active") or "active")
    if status not in STATUS:
        errs.append(f"status 는 {'/'.join(STATUS)}")
    found = str(m.get("found", "") or "")
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", found):
        errs.append("found 는 등록일(YYYY-MM-DD)")
    exams = m.get("exams") or []
    if not isinstance(exams, list) or not exams or any(e not in EXAMS for e in exams):
        errs.append("exams 는 kmle/usmle 목록")
        exams = [e for e in exams if e in EXAMS] if isinstance(exams, list) else []
    objectives = m.get("objectives") or []
    if not isinstance(objectives, list):
        errs.append("objectives 는 정리본 id 목록")
        objectives = []
    for o in objectives:
        if not OBJ_RE.match(str(o)):
            errs.append(f"objectives '{o}' — 정리본 id 형식(cn.<과>.<주제>.<목표>)")
    topics = m.get("topics") or []
    if not isinstance(topics, list) or not topics:
        errs.append("topics 는 문항 topic 목록(표시 안 된 후보를 찾을 범위)")
        topics = []

    cue = m.get("cue") if isinstance(m.get("cue"), dict) else {}
    lure = m.get("lure") if isinstance(m.get("lure"), dict) else {}
    truth = m.get("truth") if isinstance(m.get("truth"), dict) else {}
    mirror = m.get("mirror") if isinstance(m.get("mirror"), dict) else {}
    if not str(cue.get("text", "") or "").strip():
        errs.append("cue.text — 보기 한 무리로 끌어당기는 소견을 한 줄로")
    cue_rx = _compile(cue.get("patterns"), "cue", errs)
    if not str(lure.get("family", "") or "").strip():
        errs.append("lure.family — 끌려가는 오답 계열의 이름")
    lure_rx = _compile(lure.get("patterns"), "lure", errs)
    lure_min = lure.get("min", DEFAULT_LURE_MIN)
    if not isinstance(lure_min, int) or not 1 <= lure_min <= 4:
        errs.append("lure.min 은 1~4 정수(trap 쪽 문항에 둘 lure 계열 오답 수)")
        lure_min = DEFAULT_LURE_MIN
    for k in ("family", "answer"):
        if not str(truth.get(k, "") or "").strip():
            errs.append(f"truth.{k} 가 비어 있다")
    truth_rx = _compile(truth.get("patterns"), "truth", errs)
    disc = m.get("discriminators")
    if not isinstance(disc, list) or len([d for d in disc if isinstance(d, str) and d.strip()]) < 2:
        errs.append("discriminators 는 두 계열을 가르는 소견 2개 이상(문장 목록)")
    want_raw = m.get("want") or {}
    if not isinstance(want_raw, dict):
        errs.append("want 는 {trap: N, mirror: N}")
        want_raw = {}
    want = {**DEFAULT_WANT, **want_raw}
    for k, v in want.items():
        if k not in SIDES or not isinstance(v, int) or v < 0:
            errs.append(f"want.{k} — trap/mirror 에 0 이상의 정수(시험마다 둘 문항 수)")
    if isinstance(want.get("mirror"), int) and want["mirror"] > 0:
        for k in ("when", "answer"):
            if not str(mirror.get(k, "") or "").strip():
                errs.append(f"mirror.{k} — lure 계열이 정답이 되는 조건과 그때의 정답(mirror 문항을 받지 않으면 want.mirror: 0)")
    wn = m.get("write_notes")
    if wn is not None and (not isinstance(wn, list) or not all(isinstance(x, str) and x.strip() for x in wn)):
        errs.append("write_notes 는 문항을 쓸 때 지킬 점(문장 목록)")

    # 자기 일관성 — 패턴이 어긋나면 그 계열로 쓴 문항이 모두 린터에서 막힌다
    t_ans, m_ans = str(truth.get("answer", "") or ""), str(mirror.get("answer", "") or "")
    if truth_rx and t_ans and not _hit(truth_rx, t_ans):
        errs.append("truth.answer 가 truth.patterns 에 걸리지 않는다")
    if lure_rx and t_ans and _hit(lure_rx, t_ans):
        errs.append("truth.answer 가 lure.patterns 에도 걸린다 — 두 계열의 패턴이 겹친다")
    if lure_rx and m_ans and not _hit(lure_rx, m_ans):
        errs.append("mirror.answer 가 lure.patterns 에 걸리지 않는다 — mirror 쪽 정답은 lure 계열이다")
    if truth_rx and m_ans and _hit(truth_rx, m_ans):
        errs.append("mirror.answer 가 truth.patterns 에 걸린다 — mirror 쪽 정답은 truth 계열이 아니다")
    for ex in lure.get("examples") or []:
        if lure_rx and not _hit(lure_rx, str(ex)):
            warns.append(f"lure.examples '{ex}' 가 lure.patterns 에 걸리지 않는다")
        if truth_rx and _hit(truth_rx, str(ex)):
            errs.append(f"lure.examples '{ex}' 가 truth.patterns 에 걸린다")

    # 출처 — 가르는 소견·mirror 조건은 확인한 것만(concept 정리본과 같은 규칙)
    srcs = m.get("sources")
    src_ids: set[str] = set()
    if not isinstance(srcs, list) or not srcs:
        errs.append("sources 가 비어 있다 — 가르는 소견·mirror 조건의 근거(실제로 확인한 것만)")
        srcs = []
    for i, s in enumerate(srcs, 1):
        if not isinstance(s, dict):
            errs.append(f"sources[{i}] 는 사전")
            continue
        for k in ("id", "org", "title", "year", "checked_at", "checked"):
            if not str(s.get(k, "") or "").strip():
                errs.append(f"sources[{i}] 필수 필드 누락: {k}")
        url = str(s.get("url", "") or "")
        if not (url.startswith("https://") or s.get("doi") or s.get("pmid")) and not (
                s.get("kind") == "textbook" and str(s.get("citation", "") or "").strip()):
            errs.append(f"sources[{i}] 는 https url·doi·pmid 중 하나로 찾아갈 수 있어야 한다(교과서는 판·장·쪽 citation)")
        if s.get("verified", "citation") not in VERIFIED:
            errs.append(f"sources[{i}].verified 는 {'/'.join(VERIFIED)}(무엇까지 대조했나)")
        src_ids.add(str(s.get("id")))
    for sid in sorted(set(CITE_RE.findall(_texts(m))) - src_ids):
        errs.append(f"근거 표시 [[{sid}]] 가 sources 에 없다 — 없는 출처를 인용하지 않는다")
    rs = m.get("review_status")
    if rs not in REVIEW:
        errs.append(f"review_status 는 {'/'.join(REVIEW)}")
    if rs == "reviewed":
        who = str(m.get("reviewed_by", "") or "")
        if not who or not str(m.get("review_note", "") or "").strip():
            errs.append("reviewed 는 reviewed_by·review_note 가 필요하다")
        elif MODEL_NAMES.search(who):
            errs.append("reviewed_by 가 모델이다 — 모델 간 동의는 의학적 검증이 아니다(사람이 표시)")

    entry = dict(m)
    entry.update({"id": tid, "status": status, "found": found, "exams": list(exams), "objectives": [str(o) for o in objectives],
                  "topics": [str(t) for t in topics], "want": want, "lure_min": lure_min,
                  "cue": cue, "lure": lure, "truth": truth, "mirror": mirror,
                  "_cue": cue_rx, "_lure": lure_rx, "_truth": truth_rx,
                  "path": str(path.relative_to(ROOT)).replace("\\", "/") if path and str(path).startswith(str(ROOT)) else str(path or "")})
    return entry, errs, warns


def load_registry(root: Path = TRAP_DIR) -> tuple[dict[str, dict], dict[str, list[str]], dict[str, list[str]]]:
    """({id: 쓸 수 있는 항목}, {파일: 오류}, {파일: 경고}). 오류가 있는 항목은 첫 dict 에 넣지 않는다."""
    ok: dict[str, dict] = {}
    errors: dict[str, list[str]] = {}
    warns: dict[str, list[str]] = {}
    seen: set[str] = set()
    for p in sorted(root.glob("*.yaml")) if root.exists() else []:
        key = p.name
        try:
            m = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
        except yaml.YAMLError as e:
            errors[key] = [f"YAML 오류: {e}"]
            continue
        if not isinstance(m, dict):
            errors[key] = ["최상위가 사전이 아니다"]
            continue
        entry, errs, ws = validate_entry(m, p)
        if entry["id"] in seen:
            errs.append(f"id 중복: {entry['id']}")
        seen.add(entry["id"])
        for r in entry.get("related") or []:
            if not (root / f"{r}.yaml").exists():
                ws.append(f"related '{r}' 가 등록부에 없다")
        if errs:
            errors[key] = errs
        else:
            ok[entry["id"]] = entry
        if ws:
            warns[key] = ws
    return ok, errors, warns


_CACHE: dict[str, Any] = {}


def registry(root: Path = TRAP_DIR) -> tuple[dict[str, dict], set[str]]:
    """(쓸 수 있는 항목, 오류가 있어 못 쓰는 id) — 린터가 문항마다 부르므로 한 번만 읽는다."""
    key = str(root)
    if key not in _CACHE:
        ok, errors, _ = load_registry(root)
        _CACHE[key] = (ok, {Path(f).stem for f in errors})
    return _CACHE[key]


# ── 문항 ────────────────────────────────────────────────────────────────────
def _choices(meta: dict[str, Any]) -> list[str]:
    return [re.sub(r"^\s*[A-E①-⑤][.)]?\s*", "", str(c)).strip() for c in meta.get("choices") or []]


def _answer_index(meta: dict[str, Any], n: int) -> int:
    a = str(meta.get("answer", "") or "").strip().upper()[:1]
    i = LETTERS.find(a) if a else -1
    return i if 0 <= i < n else -1


def _letters(v: Any) -> list[str]:
    if v is None or v == "":
        return []
    if isinstance(v, list):
        return [str(x).strip().upper()[:1] for x in v if str(x).strip()]
    return [x.strip().upper()[:1] for x in re.split(r"[,/·\s]+", str(v)) if x.strip()]


def trap_tag(meta: dict[str, Any]) -> dict[str, Any] | None:
    """문항의 design.trap → {id, side}. 없으면 None. 문자열 하나면 trap 쪽으로 본다."""
    d = meta.get("design")
    if not isinstance(d, dict) or d.get("trap") in (None, ""):
        return None
    t = d["trap"]
    if isinstance(t, str):
        return {"id": t.strip(), "side": "trap"}
    if isinstance(t, dict):
        return {"id": str(t.get("id", "") or "").strip(), "side": str(t.get("side", "") or "").strip()}
    return {"id": "", "side": "", "bad": True}


def question_findings(meta: dict[str, Any], qtype: str,
                      reg: tuple[dict[str, dict], set[str]] | None = None) -> list[tuple[str, str, str]]:
    """design.trap 이 있는 문항의 (level, code, msg). 등록부와 대조해 cue·정답·오답 계열 모양을 본다."""
    tag = trap_tag(meta)
    if tag is None:
        return []
    if tag.get("bad"):
        return [("ERROR", "trap-type", "design.trap 은 {id, side} 사전이어야 한다(문자열 하나면 trap 쪽 id).")]
    entries, invalid = registry() if reg is None else reg
    tid, side = tag["id"], tag["side"]
    e = entries.get(tid)
    if e is None:
        if tid in invalid:
            return [("ERROR", "trap-invalid", f"design.trap '{tid}' 의 등록부 항목에 오류가 있다 — `python pipelines/traps.py check`.")]
        return [("ERROR", "trap-unknown", f"design.trap '{tid}' 가 등록부(content/traps/)에 없다 — 계열을 먼저 등록한다(/gen-kmle 「함정 계열」).")]
    out: list[tuple[str, str, str]] = []
    if side not in SIDES:
        return [("ERROR", "trap-side", f"design.trap.side '{side}' 는 trap(함정에 걸리는 쪽)·mirror(lure 계열이 정답인 쪽) 중 하나.")]
    if e["status"] == "retired":
        out.append(("WARN", "trap-retired", f"계열 '{tid}' 은 retired — 새 문항에 쓰지 않는다."))
    if qtype not in e["exams"]:
        out.append(("WARN", "trap-exam", f"계열 '{tid}' 은 {'/'.join(e['exams'])} 용으로 등록됐다(이 문항은 {qtype}) — 등록부 exams 를 넓히거나 다른 계열을 쓴다."))
    if not _hit(e["_cue"], question_text_pool(meta)):
        out.append(("ERROR", "trap-cue-missing", f"발문·활력징후·검사에 계열의 단서가 없다 — 「{e['cue'].get('text', '')}」(등록부 cue.patterns)."))
    ch = _choices(meta)
    ai = _answer_index(meta, len(ch))
    if ai < 0:
        return out                                   # 보기·정답 형식은 다른 린트가 잡는다
    atext = ch[ai]
    others = [(LETTERS[i], c) for i, c in enumerate(ch) if i != ai]
    lure_l = [L for L, c in others if _hit(e["_lure"], c)]
    truth_l = [L for L, c in others if _hit(e["_truth"], c)]
    d = meta.get("design") if isinstance(meta.get("design"), dict) else {}
    rivals = set(_letters(d.get("rival")))
    fam_l, fam_t = e["lure"].get("family", ""), e["truth"].get("family", "")
    if side == "trap":
        if _hit(e["_lure"], atext):
            out.append(("ERROR", "trap-answer-is-lure", f"trap 쪽인데 정답이 lure 계열({fam_l})이다 — 이 모양이면 side: mirror."))
        elif not _hit(e["_truth"], atext):
            out.append(("ERROR", "trap-answer-not-truth", f"trap 쪽 정답은 truth 계열({fam_t} — 예: {e['truth'].get('answer', '')})이어야 한다."))
        if len(lure_l) < e["lure_min"]:
            out.append(("ERROR", "trap-lure-few", f"오답 가운데 lure 계열({fam_l})이 {len(lure_l)}개 — {e['lure_min']}개 이상이어야 함정이 선다."))
        if rivals and not rivals & set(lure_l):
            out.append(("WARN", "trap-rival-not-lure", "design.rival 이 lure 계열 보기가 아니다 — 이 계열에서 가장 끌리는 보기를 rival 로."))
        dist = meta.get("distractors") if isinstance(meta.get("distractors"), dict) else {}
        for L in sorted(rivals & set(lure_l)):
            dd = dist.get(L)
            if isinstance(dd, dict) and not str(dd.get("when_right", "") or "").strip():
                out.append(("WARN", "trap-when-right", f"distractors.{L}.when_right 에 lure 계열이 정답이 되는 조건(등록부 mirror.when)을 적는다."))
    else:
        if _hit(e["_truth"], atext):
            out.append(("ERROR", "mirror-answer-is-truth", f"mirror 쪽인데 정답이 truth 계열({fam_t})이다 — 이 모양이면 side: trap."))
        elif not _hit(e["_lure"], atext):
            out.append(("ERROR", "mirror-answer-not-lure", f"mirror 쪽 정답은 lure 계열({fam_l} — 예: {e['mirror'].get('answer', '')})이어야 한다."))
        if not truth_l:
            out.append(("ERROR", "mirror-no-truth-option", f"오답에 truth 계열({fam_t}) 보기가 없다 — mirror 쪽은 그 보기를 거르는 판단을 묻는다."))
        if rivals and not rivals & set(truth_l):
            out.append(("WARN", "mirror-rival-not-truth", "design.rival 이 truth 계열 보기가 아니다 — mirror 쪽에서 가장 끌리는 것은 truth 계열 보기다."))
    return out


def _shape(e: dict[str, Any], ch: list[str], ai: int) -> str | None:
    """표시 안 된 문항이 이 계열의 어느 쪽 모양인가(추정 — 사람·루틴이 확인한 뒤 표시한다)."""
    if not ch or ai < 0:
        return None
    a = ch[ai]
    others = [c for i, c in enumerate(ch) if i != ai]
    if _hit(e["_truth"], a) and not _hit(e["_lure"], a) and any(_hit(e["_lure"], c) for c in others):
        return "trap"
    if _hit(e["_lure"], a) and not _hit(e["_truth"], a):
        return "mirror"
    return None


def coverage(entries: dict[str, dict], questions: dict[str, dict]) -> dict[str, dict]:
    """{계열: {"tagged": {시험: {쪽: [문항]}}, "candidates": {시험: {쪽: [(문항, design 있음)]}}}}.
    candidates = 표시는 없지만 단서·정답·오답 모양이 그 쪽과 같은 문항(범위: 계열의 topics·objectives)."""
    out = {tid: {"tagged": {ex: {s: [] for s in SIDES} for ex in e["exams"]},
                 "candidates": {ex: {s: [] for s in SIDES} for ex in e["exams"]}}
           for tid, e in entries.items()}
    for qid, m in sorted(questions.items()):
        qt = str(m.get("type", "") or "")
        if qt not in EXAMS:
            continue
        tag = trap_tag(m)
        if tag and tag.get("id") in out and tag.get("side") in SIDES:
            if qt in out[tag["id"]]["tagged"]:
                out[tag["id"]]["tagged"][qt][tag["side"]].append(qid)
            continue
        pool = None
        ch = _choices(m)
        ai = _answer_index(m, len(ch))
        for tid, e in entries.items():
            if qt not in e["exams"]:
                continue
            if str(m.get("topic", "")) not in e["topics"] and str(m.get("objective", "")) not in e["objectives"]:
                continue
            pool = pool if pool is not None else question_text_pool(m)
            if not _hit(e["_cue"], pool):
                continue
            side = _shape(e, ch, ai)
            if side:
                out[tid]["candidates"][qt][side].append((qid, isinstance(m.get("design"), dict)))
    return out


def build_queue(entries: dict[str, dict], cov: dict[str, dict], exam: str | None = None) -> list[dict]:
    """문항이 want 보다 적은 (계열 × 시험 × 쪽). trap 쪽 먼저, 새로 등록한 계열 먼저."""
    items: list[dict] = []
    for tid, e in entries.items():
        if e["status"] != "active":
            continue
        for ex in e["exams"]:
            if exam and ex != exam:
                continue
            for side in SIDES:
                have = cov[tid]["tagged"][ex][side]
                need = e["want"][side] - len(have)
                if need <= 0:
                    continue
                cands = cov[tid]["candidates"][ex][side]
                items.append({
                    "trap": tid, "title": str(e.get("title", "")), "exam": ex, "side": side, "need": need,
                    "objective": e["objectives"][0] if e["objectives"] else "", "topics": e["topics"], "found": e["found"],
                    "cue": str(e["cue"].get("text", "")),
                    "answer": str(e["truth"].get("answer", "")) if side == "trap" else str(e["mirror"].get("answer", "")),
                    "lure": str(e["lure"].get("family", "")), "lure_examples": list(e["lure"].get("examples") or []),
                    "lure_min": e["lure_min"], "mirror_when": str(e["mirror"].get("when", "") or ""),
                    "tagged": {s: list(cov[tid]["tagged"][ex][s]) for s in SIDES},
                    "taggable": [q for q, has in cands if has][:MAX_CANDIDATES],
                    "candidates": [q for q, _ in cands][:MAX_CANDIDATES],
                    "path": e.get("path", ""),
                })
    items.sort(key=lambda x: (x["side"] != "trap", -int(x["found"].replace("-", "") or 0), x["trap"], x["exam"]))
    return items


# ── 비슷한 문항 찾기(외부 문항 → MedKOS) ────────────────────────────────────
CHOICE_LINE = re.compile(r"^\s*[○●◯]?\s*(?:[1-5①-⑤]|[A-Ea-e])\s*[.)]\s*(.+?)\s*$")


def split_external(text: str) -> tuple[str, list[str]]:
    """붙여 넣은 외부 문항 → (발문, 보기). 보기처럼 생긴 줄(1) · ① · A.)이 셋 이상이면 보기로 본다."""
    stem, ch = [], []
    for ln in str(text).splitlines():
        m = CHOICE_LINE.match(ln)
        (ch.append(m.group(1)) if m else stem.append(ln))
    if len(ch) < 3:
        return str(text), []
    return "\n".join(stem), ch


def _grams(text: str, n: int = 2) -> collections.Counter:
    t = re.sub(r"[\W_]+", "", str(text or "").casefold())
    return collections.Counter(t[i:i + n] for i in range(len(t) - n + 1))


def _qtext(m: dict[str, Any]) -> str:
    return str(m.get("stem", "") or "") + " " + " ".join(_choices(m))


def similar(text: str, questions: dict[str, dict], top: int = 10) -> list[tuple[float, str]]:
    """글자 두 개 묶음(bigram) TF-IDF 코사인 — 한국어·영어 모두. [(점수, 문항)] 높은 순."""
    docs = {qid: _grams(_qtext(m)) for qid, m in questions.items()}
    df: collections.Counter = collections.Counter()
    for g in docs.values():
        df.update(g.keys())
    n = len(docs) or 1

    def vec(c: collections.Counter) -> dict[str, float]:
        return {k: v * (math.log((n + 1) / (df.get(k, 0) + 1)) + 1) for k, v in c.items()}

    q = vec(_grams(text))
    qn = math.sqrt(sum(v * v for v in q.values())) or 1.0
    scored = []
    for qid, g in docs.items():
        v = vec(g)
        dot = sum(w * v[k] for k, w in q.items() if k in v)
        if dot:
            scored.append((dot / (qn * (math.sqrt(sum(x * x for x in v.values())) or 1.0)), qid))
    scored.sort(key=lambda x: (-x[0], x[1]))
    return scored[:top]


def trap_matches(text: str, choices: list[str], entries: dict[str, dict]) -> list[dict]:
    """외부 문항이 등록된 계열의 단서·보기 계열과 얼마나 맞는가."""
    out = []
    for tid, e in entries.items():
        cue = _hit(e["_cue"], text)
        opts = choices or [text]
        lure_n = sum(_hit(e["_lure"], c) for c in opts)
        truth_n = sum(_hit(e["_truth"], c) for c in opts)
        if cue or (choices and lure_n and truth_n):
            out.append({"trap": tid, "title": str(e.get("title", "")), "cue": cue, "lure": lure_n, "truth": truth_n})
    return sorted(out, key=lambda x: (not x["cue"], -(x["lure"] + x["truth"]), x["trap"]))


def solve_records(path: Path = EVENTS) -> dict[str, list[tuple[str, bool]]]:
    """{문항: [(날짜, 맞음)]} — 저장소에 동기화된 학습 기록만(기기에만 있는 풀이는 모른다)."""
    try:
        ev = json.loads(path.read_text(encoding="utf-8")).get("events") or []
    except (OSError, ValueError, AttributeError):
        return {}
    out: dict[str, list[tuple[str, bool]]] = collections.defaultdict(list)
    for x in ev:
        if isinstance(x, dict) and x.get("kind") == "answer" and x.get("qid"):
            out[str(x["qid"])].append((str(x.get("day") or "")[:10], bool(x.get("ok"))))
    return dict(out)


# ── 명령 ────────────────────────────────────────────────────────────────────
def _load_questions() -> dict[str, dict]:
    from concepts import load_questions
    return load_questions()


def cmd_check(root: Path) -> int:
    ok, errors, warns = load_registry(root)
    questions = _load_questions()
    reg = (ok, {Path(f).stem for f in errors})
    q_err, q_warn, tagged = [], [], 0
    for qid, m in sorted(questions.items()):
        if trap_tag(m) is None:
            continue
        tagged += 1
        for level, code, msg in question_findings(m, str(m.get("type", "")), reg):
            (q_err if level == "ERROR" else q_warn).append(f"{m.get('path', qid)}: [{level}] {code}: {msg}")
    for f, es in sorted(errors.items()):
        for x in es:
            print(f"  ✗ content/traps/{f}: {x}")
    for f, ws in sorted(warns.items()):
        for x in ws:
            print(f"  △ content/traps/{f}: {x}")
    for x in q_err + q_warn:
        print(f"  {'✗' if '[ERROR]' in x else '△'} {x}")
    n_err = sum(len(v) for v in errors.values()) + len(q_err)
    n_warn = sum(len(v) for v in warns.values()) + len(q_warn)
    print(f"함정 계열 {len(ok) + len(errors)}개(쓸 수 있음 {len(ok)}) · 표시한 문항 {tagged}개 — 오류 {n_err} · 경고 {n_warn}")
    return 1 if n_err else 0


def _fmt_cov(e: dict, cov: dict) -> str:
    parts = []
    for ex in e["exams"]:
        t = cov["tagged"][ex]
        parts.append(f"{ex} trap {len(t['trap'])}/{e['want']['trap']} · mirror {len(t['mirror'])}/{e['want']['mirror']}")
    return " | ".join(parts)


def cmd_list(root: Path, brief: bool) -> int:
    entries, errors, _ = load_registry(root)
    cov = coverage(entries, _load_questions())
    print(f"함정 계열 {len(entries)}개" + (f" (오류로 못 쓰는 항목 {len(errors)}개 — traps.py check)" if errors else ""))
    for tid, e in sorted(entries.items(), key=lambda x: (x[1]["status"] != "active", x[0])):
        mark = "" if e["status"] == "active" else " [retired]"
        print(f"{tid}{mark}  {e.get('title', '')}")
        print(f"   {_fmt_cov(e, cov[tid])}")
        if brief:
            continue
        print(f"   단서: {e['cue'].get('text', '')}")
        print(f"   오답 계열(lure): {e['lure'].get('family', '')} — 예: {', '.join(map(str, e['lure'].get('examples') or []))}")
        print(f"   정답 계열(truth): {e['truth'].get('family', '')} — {e['truth'].get('answer', '')}")
        if e["mirror"].get("when"):
            print(f"   mirror(lure 가 정답): {str(e['mirror']['when']).strip()[:160]}")
        for ex in e["exams"]:
            for s in SIDES:
                tg = cov[tid]["tagged"][ex][s]
                cd = cov[tid]["candidates"][ex][s]
                if tg:
                    print(f"   {ex} {s}: {', '.join(tg)}")
                if cd:
                    nd = sum(1 for _, has in cd if not has)
                    print(f"   {ex} {s} 표시 안 된 후보 {len(cd)}(design 없음 {nd}): {', '.join(q for q, _ in cd[:MAX_CANDIDATES])}")
    return 0


def cmd_queue(root: Path, exam: str | None, limit: int, as_json: bool) -> int:
    entries, errors, _ = load_registry(root)
    items = build_queue(entries, coverage(entries, _load_questions()), exam)
    shown = items[:limit] if limit else items
    if as_json:
        print(json.dumps({"items": shown, "total": len(items), "registry_errors": sorted(errors)}, ensure_ascii=False, indent=1))
        return 0
    print(f"함정 계열 대기 {len(items)}건" + (f"(시험 {exam})" if exam else "") + (f" · 등록부 오류 {len(errors)}개" if errors else ""))
    for it in shown:
        if it["side"] == "trap":
            print(f"  [trap] {it['trap']} · {it['exam']} · trap 쪽 {it['need']}문항 — 목표 {it['objective'] or '-'}")
            print(f"         단서: {it['cue']} / 오답에 lure 계열 ≥{it['lure_min']}: {it['lure']} / 정답: {it['answer']}")
        else:
            print(f"  [trap] {it['trap']} · {it['exam']} · mirror 쪽 {it['need']}문항(lure 계열이 정답) — 목표 {it['objective'] or '-'}")
            print(f"         단서: {it['cue']} / 정답: {it['answer']} / 조건: {it['mirror_when'][:120]}")
        if it["taggable"]:
            print(f"         표시할 수 있는 기존 문항(design 있음 — 확인 뒤 design.trap 만 붙여도 된다): {', '.join(it['taggable'])}")
        elif it["candidates"]:
            print(f"         비슷한 모양의 기존 문항(design 없음 — 새로 쓴다): {', '.join(it['candidates'])}")
    return 0


def cmd_similar(root: Path, text: str, top: int, answer: str | None) -> int:
    questions = _load_questions()
    entries, _, _ = load_registry(root)
    stem, choices = split_external(text)
    solved = solve_records()
    print(f"비슷한 MedKOS 문항(글자 bigram TF-IDF, 전체 {len(questions)}문항 · 보기 {len(choices)}개 인식)")
    for score, qid in similar(text, questions, top):
        m = questions[qid]
        ch = _choices(m)
        ai = _answer_index(m, len(ch))
        tag = trap_tag(m)
        rec = solved.get(qid) or []
        rec_s = ", ".join(f"{d} {'정답' if ok else '오답'}" for d, ok in rec[-3:]) if rec else "기록 없음"
        print(f"  {score:.3f}  {qid}  {m.get('date', '')}  [{m.get('topic', '')} / {str(m.get('subtopic', ''))[:50]}]")
        print(f"         정답: {ch[ai] if ai >= 0 else '?'} · 함정 표시: {(tag['id'] + ' ' + tag['side']) if tag else '-'} · 풀이: {rec_s}")
    hits = trap_matches(text, choices, entries)
    print("\n등록된 함정 계열과 대조:")
    if not hits:
        print("  맞는 계열 없음 — 위 문항들과 단서(cue)·오답 계열·정답 계열을 비교해 새 계열인지 판단한다(/gen-kmle 「함정 계열」).")
    ai = _answer_arg(answer, len(choices))
    for h in hits:
        shape = f" → 이 문항은 {_shape(entries[h['trap']], choices, ai) or '어느 쪽 모양도 아님'}" if ai >= 0 else ""
        print(f"  {h['trap']}  단서 {'있음' if h['cue'] else '없음'} · lure 계열 보기 {h['lure']} · truth 계열 보기 {h['truth']}{shape}")
    return 0


def _answer_arg(answer: str | None, n: int) -> int:
    """--answer 「3」·「C」·「③」 → 0부터 센 보기 번호(모르면 -1)."""
    a = str(answer or "").strip().upper()
    if not a or not n:
        return -1
    if a in ("①", "②", "③", "④", "⑤"):
        i = "①②③④⑤".index(a)
    elif len(a) == 1 and a in LETTERS:
        i = LETTERS.index(a)
    elif a.isdigit():
        i = int(a) - 1
    else:
        return -1
    return i if 0 <= i < n else -1


def main(argv: list[str]) -> int:
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    ap = argparse.ArgumentParser(description=__doc__.strip().splitlines()[0])
    ap.add_argument("--root", help="등록부 폴더(기본 content/traps — 시험용)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("check", help="등록부 + 표시한 문항 형식")
    p = sub.add_parser("list", help="계열별 문항 수")
    p.add_argument("--brief", action="store_true")
    p = sub.add_parser("queue", help="문항이 모자란 계열")
    p.add_argument("--exam", choices=EXAMS)
    p.add_argument("--limit", type=int, default=0)
    p.add_argument("--json", action="store_true")
    p = sub.add_parser("similar", help="외부 문항과 비슷한 MedKOS 문항")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--text")
    g.add_argument("--file")
    p.add_argument("--top", type=int, default=10)
    p.add_argument("--answer", help="외부 문항의 정답 번호(1~5)나 글자 — 주면 계열의 어느 쪽 모양인지 알려 준다")
    a = ap.parse_args(argv)
    root = Path(a.root) if a.root else TRAP_DIR
    if a.cmd == "check":
        return cmd_check(root)
    if a.cmd == "list":
        return cmd_list(root, a.brief)
    if a.cmd == "queue":
        return cmd_queue(root, a.exam, a.limit, a.json)
    text = Path(a.file).read_text(encoding="utf-8") if a.file else a.text
    return cmd_similar(root, text, a.top, a.answer)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
