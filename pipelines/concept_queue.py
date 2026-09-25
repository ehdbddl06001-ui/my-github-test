"""concept_queue.py — 내 오답 가운데 **이론 정리본이 없는 것**을 골라 루틴에 넘길 큐를 만든다(결정론).

2026-09-20 사용자 지시: 틀린 문항의 이론 정리는 매일 루틴이 자동으로 쓰게 한다.
「무엇을 쓸지」는 여기서 기계적으로 고르고(누가 몇 번 틀렸나·정리본이 있나), 「무엇을 쓸지의 내용」은
사람이 검토하는 콘텐츠라 `/gen-concept` 규칙을 따라 모델이 쓴다. 이 스크립트는 글을 쓰지 않는다.

큐는 세 갈래다.
  note   — 학습 목표(objective)는 붙어 있는데 그 정리본이 아직 없는 오답. 정리본을 새로 쓴다.
  link   — 학습 목표가 없는 문항의 오답. 먼저 목표를 정해 문항에 `objective` 를 붙이고,
           그 목표의 정리본이 없으면 note 로 이어진다(같은 주제의 오답은 한 줄로 묶어 보여 준다).
  touch  — 정리본이 **이미 있는** 목표에서 새로 틀린 보기가 그 정리본의 `pitfalls[].covers` 에 없을 때.
           새 정리본을 쓰지 않고 혼동 항목 하나를 더하거나 고치는 **가벼운 손질**만 한다(2026-09-22 —
           정리본이 쌓이면 대부분의 오답은 이쪽이 된다).
  variant — 정리본이 있는 목표에서 **틀린 문항마다 변형 2개**(of: <문항>)가 아직 없을 때(2026-09-23 사용자 채택 —
           「오답 → 변형 문항 → 간격을 두고 다시 출제」). 하나는 결정적 단서를 바꿔 답이 바뀌고(flip: true —
           문항 design.switch 가 씨앗), 하나는 겉모습만 바꾸고 답은 그대로(flip: false). 앱 「오늘 다시 풀 것」이
           예정일(learning_log.schedule)에 이 변형을 먼저 낸다 — 그래서 예정일이 이른 것부터 준다.
  dist   — 내가 **실제로 고른 오답 보기**에 문항의 `distractors.<보기>` 설명이 없을 때. 그 보기 하나의 설명
           (왜 그럴듯한가·왜 정답이 먼저인가·가르는 소견·그 보기가 맞는 경우)을 문항에 더한다(선지 보정 —
           고른 보기만. 영상 문항은 빌더 파생물이라 제외).
  restyle — 판형 2(`note_form: 2`, 2026-09-25 사용자 요청 「이전 모델이 만든 오답 정리본을 더 좋은 스타일로」)로
           아직 옮기지 않은 정리본. 새 글을 쓰는 게 아니라 **있는 내용을 판형 2 순서·예산으로 다시 배치**한다
           (결론·시험 단서·왜 → 틀린 보기별 pitfalls → 표·도식 → 목표에 맞춘 본문). 오답이 걸린 목표부터,
           그다음 오래된 것부터. note·link·touch 가 비었을 때 gap 보다 먼저 한다.
  gap    — 오답과 무관하게 **기본틀(content/outline/subjects.yaml)에서 아직 비어 있는 자리**.
           오답 큐가 비었을 때 커리큘럼 순서대로 한 칸씩 채우라고 내놓는다(2026-09-21 추가).
           이미 단원이 있는 책만 대상으로 하고, 그 책의 해리슨 서술 순서에서 앞쪽 빈 슬롯부터 준다.
우선순위 = 반복 오답·후속 확인 실패·표시(learning_log 의 priority)를 그대로 쓴다.

오답의 원천은 둘이다(2026-09-23).
  학습 기록  state/learning_sync/events.json — 2026-09-18 학습 흐름이 생긴 뒤의 풀이만 있다.
  오답 목록  state/wrong_sync/<exam>.json   — 앱 오답노트(기기에서 동기화). 그 전의 오답도 여기 남아 있다.
학습 기록에 **오답으로 남지 않은** 문항만 오답 목록에서 채운다(`wrongnote_events`). 실제 풀이가 있으면 그 기록이
우선이다. 채운 사건은 큐 계산에만 쓰고 events.json 에 쓰지 않는다(사용자 기록을 지어내지 않는다).

사용:
  python pipelines/concept_queue.py                 # 큐 출력 + state/concept_queue.json 갱신
  python pipelines/concept_queue.py --limit 3       # 오늘 쓸 상위 N개만(루틴 상한)
  python pipelines/concept_queue.py --events <파일> # 다른 학습 기록으로(시험·검증용)
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import learning_log as ll
import outline as ol
from concepts import load_concepts, load_questions

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "state" / "concept_queue.json"
WRONG_SYNC = ROOT / "state" / "wrong_sync"


def load_wrong_notes(folder: Path = WRONG_SYNC) -> dict[str, dict]:
    """{문항id: 오답노트 항목} — kmle·usmle·imaging 오답 목록을 합친다. 읽을 수 없는 파일은 건너뛴다."""
    out: dict[str, dict] = {}
    for f in sorted(folder.glob("*.json")) if folder.exists() else []:
        try:
            items = json.loads(f.read_text(encoding="utf-8")).get("items") or {}
        except (OSError, ValueError, AttributeError):
            continue
        rows = items.values() if isinstance(items, dict) else items
        for it in rows:
            if isinstance(it, dict) and it.get("id"):
                out[str(it["id"])] = it
    return out


def wrongnote_events(wrongnote: dict[str, dict], events: list[dict]) -> list[dict]:
    """학습 기록에 오답이 없는 오답노트 항목을 큐 계산용 「오답 사건」으로 바꾼다(저장하지 않음)."""
    logged = {e.get("qid") for e in events if e.get("kind") == "answer" and not e.get("ok")}
    out = []
    for qid, it in sorted(wrongnote.items()):
        if qid in logged:
            continue
        day = str(it.get("date") or "")[:10]
        out.append({"eid": f"wrongnote:{qid}", "kind": "answer", "ok": False, "qid": qid,
                    "t": f"{day}T00:00:00Z" if day else "", "day": day, "mode": "wrongnote",
                    "chosenText": str(it.get("chosenText") or ""), "answerText": str(it.get("answerText") or "")})
    return out


def build(events: list[dict], wrongnote: dict[str, dict] | None = None) -> dict:
    """wrongnote: 오답 목록({문항id: 항목}). 넘기면 학습 기록에 없는 오답을 채운다(None = 학습 기록만)."""
    concepts, _ = load_concepts()
    questions = load_questions()
    from_note = wrongnote_events(wrongnote or {}, events)
    events = list(events) + from_note
    obj_of = {q: m.get("objective") for q, m in questions.items() if m.get("objective")}
    S = ll.states(events, obj_of)
    sched = ll.schedule(events, obj_of)
    notes: list[dict] = []
    variants: list[dict] = []
    dists: list[dict] = []
    touches: list[dict] = []
    links: dict[tuple[str, str], dict] = {}
    for key, s in S.items():
        if not s.status or not s.wrongs:
            continue
        dists.extend(_dists(s, questions))
        if s.objective:
            if s.objective in concepts:
                touches.extend(_touches(s, concepts[s.objective], questions))
                variants.extend(_variants(s, concepts[s.objective], questions, (sched.get(key) or {}).get("due", "")))
                continue                                  # 정리본이 이미 있다 — 새 혼동만 손질 대상으로
            q = next((questions[q] for q in s.qids if q in questions), {})
            notes.append({"objective": s.objective, "topic": str(q.get("topic", "")),
                          "subtopic": str(q.get("subtopic", "")), "questions": list(s.qids),
                          "wrongs": s.wrongs, "priority": s.priority})
        else:
            qid = key[2:]
            q = questions.get(qid)
            if not q:
                continue                                  # 사라진 문항(덱에서 빠짐) — 큐에 올리지 않는다
            k = (str(q.get("topic", "")), str(q.get("subtopic", "")))
            e = links.setdefault(k, {"topic": k[0], "subtopic": k[1], "questions": [], "wrongs": 0, "priority": 0})
            e["questions"].append(qid)
            e["wrongs"] += s.wrongs
            e["priority"] = max(e["priority"], s.priority)
    gaps = _gaps(concepts, questions, S)
    restyles = _restyles(concepts, S)
    notes.sort(key=lambda x: (-x["priority"], -x["wrongs"], x["objective"]))
    link_list = sorted(links.values(), key=lambda x: (-x["priority"], -x["wrongs"], x["topic"], x["subtopic"]))
    variants.sort(key=lambda x: (x["due"] or "9999", -x["priority"], x["qid"]))
    seen_d: set[str] = set()
    dists = [d for d in dists if not (d["key"] in seen_d or seen_d.add(d["key"]))]
    return {"generated": ll.kst_day(""), "note": notes, "link": link_list, "touch": touches,
            "variant": variants, "dist": dists, "restyle": restyles, "gap": gaps,
            "counts": {"note": len(notes), "link": len(link_list), "touch": len(touches), "gap": len(gaps),
                       "restyle": len(restyles),
                       "variant": len(variants), "dist": len(dists),
                       "wrong_objectives_with_note": sum(1 for s in S.values() if s.objective and s.wrongs and s.objective in concepts),
                       "from_wrongnote": len(from_note)}}


def _letter(q: dict, text: str) -> str:
    """고른 보기 글자 → A~E(보기 순서가 바뀌어도 글자로 맞춘다)."""
    import re
    for i, opt in enumerate(q.get("choices") or []):
        if re.sub(r"^[A-E①-⑤][.)]?\s*", "", str(opt)).strip() == str(text).strip():
            return "ABCDE"[i]
    return ""


def _touches(s, concept: dict, questions: dict) -> list[dict]:
    covered = {str(c) for p in concept.get("pitfalls") or [] if isinstance(p, dict) for c in p.get("covers") or []}
    out, seen = [], set()
    for ch in s.chosen:
        qid = ch.get("qid") or ""
        q = questions.get(qid) or {}
        key = f"{qid}:{_letter(q, ch.get('text', ''))}"
        if key.endswith(":") or key in covered or key in seen:
            continue
        seen.add(key)
        out.append({"objective": concept.get("id"), "title": str(concept.get("title", "")), "cover": key,
                    "chosen": ch.get("text", ""), "answer": ch.get("answer", ""), "day": ch.get("day", "")})
    return out


def _variants(s, concept: dict, questions: dict, due: str) -> list[dict]:
    """틀린 문항마다 of 가 그 문항인 변형이 2개 미만이면 한 줄."""
    have: dict[str, int] = {}
    for v in concept.get("variants") or []:
        if isinstance(v, dict) and v.get("of"):
            have[str(v["of"])] = have.get(str(v["of"]), 0) + 1
    out = []
    for qid in s.wrong_qids:
        q = questions.get(qid or "")
        if not q or "#" in str(qid) or have.get(qid, 0) >= 2:
            continue                                  # 사라진 문항·변형 자체의 오답·이미 둘 있음
        d = q.get("design") if isinstance(q.get("design"), dict) else {}
        out.append({"objective": concept.get("id"), "qid": qid, "exam": str(q.get("type", "")), "have": have.get(qid, 0),
                    "need": 2 - have.get(qid, 0), "due": due, "priority": s.priority,
                    "seed": "design.switch" if isinstance(d.get("switch"), dict) else ("design.discriminator" if d.get("discriminator") else "해설")})
    return out


def _dists(s, questions: dict) -> list[dict]:
    """고른 오답 보기에 distractors 설명이 없는 KMLE·USMLE 문항."""
    out = []
    for ch in s.chosen:
        qid = ch.get("qid") or ""
        q = questions.get(qid)
        if not q or str(q.get("type")) not in ("kmle", "usmle"):
            continue
        L = _letter(q, ch.get("text", ""))
        dist = q.get("distractors") if isinstance(q.get("distractors"), dict) else {}
        if not L or L == str(q.get("answer", "")).strip().upper()[:1] or L in dist:
            continue
        out.append({"key": f"{qid}:{L}", "qid": qid, "letter": L, "path": q.get("path", ""),
                    "chosen": ch.get("text", ""), "answer": ch.get("answer", ""), "day": ch.get("day", "")})
    return out


def _restyles(concepts: dict, S: dict) -> list[dict]:
    """판형 2 로 옮길 정리본 — 오답이 걸린 목표(우선순위 높은 것) 먼저, 그다음 id 순(대체로 오래된 과부터)."""
    pri: dict[str, int] = {}
    for s in S.values():
        if s.objective and s.wrongs:
            pri[s.objective] = max(pri.get(s.objective, 0), s.priority or 1)
    out = [{"objective": cid, "path": str(c.get("path", "")), "priority": pri.get(cid, 0),
            "title": str(c.get("title", ""))}
           for cid, c in concepts.items() if c.get("note_form") != 2]
    return sorted(out, key=lambda x: (-x["priority"], x["objective"]))


def _gaps(concepts: dict, questions: dict, S: dict) -> list[dict]:
    """기본틀에서 빈 슬롯 — 이미 단원이 있는 책만, 그 책의 순서대로 앞에서부터."""
    import yaml
    books_cfg = yaml.safe_load((ROOT / "pipelines" / "books_config.yaml").read_text(encoding="utf-8")) or {}
    bmap = dict(books_cfg.get("books") or {})
    books, _ = ol.load()
    have: dict[str, int] = {}                       # 책 → 그 책에 쌓인 정리본 수
    for c in concepts.values():
        b = bmap.get(str(c.get("topic") or ""))
        if b:
            have[b] = have.get(b, 0) + 1
    filled = {str(c.get("outline") or "") for c in concepts.values()}
    out: list[dict] = []
    for book, slots in books.items():
        if book not in have:
            continue                                 # 아직 시작하지 않은 과는 오답이 이끌게 둔다
        # 「이어서 읽기」 — 이미 쓴 단원 다음 자리부터 채운다. 앞에서부터 채우면 그 과에서
        # 이미 공부한 자리와 동떨어진 장(예: 신장내과 51장 간질성 방광염)이 먼저 나온다.
        last = max((sl.order for sl in slots if sl.id in filled), default=-1)
        nxt = next((sl for sl in slots if sl.id not in filled and sl.order > last), None)             or next((sl for sl in slots if sl.id not in filled), None)
        if nxt:
            out.append({"book": book, "slot": nxt.id, "title": nxt.title,
                        "source": nxt.source, "chapters": nxt.chapters, "have": have[book]})
    out.sort(key=lambda g: (-g["have"], g["book"]))
    return out


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--events", help="학습 기록 파일(기본: state/learning_sync/events.json + 수신함)")
    ap.add_argument("--limit", type=int, default=0, help="오늘 처리할 상위 N개만 출력(0=전부)")
    ap.add_argument("--json", action="store_true", help="사람이 읽는 줄 대신 JSON 만")
    ap.add_argument("--wrong-sync", help="오답 목록 폴더(기본: state/wrong_sync)")
    ap.add_argument("--no-wrongnote", action="store_true", help="학습 기록만 쓴다(오답 목록 무시)")
    a = ap.parse_args(argv)
    if a.events:
        events = ll.read_events(Path(a.events))
    else:
        ll.sync_inbox()
        events = ll.read_events(ll.SYNC_FILE)
    q = build(events, None if a.no_wrongnote else load_wrong_notes(Path(a.wrong_sync) if a.wrong_sync else WRONG_SYNC))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(q, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
    note, link, touch, var, dist, gap = q["note"], q["link"], q["touch"], q["variant"], q["dist"], q["gap"]
    rs = q["restyle"]
    if a.limit:
        note, link, touch, var, dist, gap, rs = (x[:a.limit] for x in (note, link, touch, var, dist, gap, rs))
    if a.json:
        print(json.dumps({"note": note, "link": link, "touch": touch, "variant": var, "dist": dist, "restyle": rs, "gap": gap,
                          "counts": q["counts"]}, ensure_ascii=False, indent=1))
        return 0
    if not events and not q["counts"]["from_wrongnote"]:
        print("학습 기록이 없다 — 앱의 「학습 기록 내보내기」가 드라이브 수신함에 들어왔는지 본다(동기화 미설정이면 정상).")
    print(f"정리본 대기(note) {q['counts']['note']}건 · 목표 연결 대기(link) {q['counts']['link']}건 · "
          f"손질 대기(touch) {q['counts']['touch']}건 · 변형 대기(variant) {q['counts']['variant']}건 · "
          f"오답 보기 설명 대기(dist) {q['counts']['dist']}건 · "
          f"이미 정리본이 있는 오답 목표 {q['counts']['wrong_objectives_with_note']}개 · "
          f"오답 목록에서 채운 오답 {q['counts']['from_wrongnote']}건")
    for n in note:
        print(f"  [note] {n['objective']}  오답 {n['wrongs']}회 · 우선순위 {n['priority']} · {n['topic']}/{n['subtopic']} · 문항 {', '.join(n['questions'][:4])}")
    for l in link:
        print(f"  [link] {l['topic']}/{l['subtopic']}  오답 {l['wrongs']}회 · 우선순위 {l['priority']} · 문항 {', '.join(l['questions'][:4])}")
    for t in touch:
        print(f"  [touch] {t['objective']}  새 혼동 {t['cover']} 「{str(t['chosen'])[:30]}」 → 정답 「{str(t['answer'])[:30]}」")
    for v in var:
        print(f"  [variant] {v['objective']}  문항 {v['qid']} 변형 {v['need']}개 더 · 예정일 {v['due'] or '-'} · 씨앗 {v['seed']}")
    for d in dist:
        print(f"  [dist] {d['qid']} 보기 {d['letter']} 「{str(d['chosen'])[:30]}」 설명 없음 · {d['path']}")
    if not note and not link and not touch:
        for r in rs:
            print(f"  [restyle] {r['objective']}  {r['title'][:40]}" + (f" · 오답 우선순위 {r['priority']}" if r["priority"] else "")
                  + f" · {r['path']}")
        if rs:
            print(f"  (판형 2 로 옮길 정리본 {q['counts']['restyle']}개 남음 — /gen-concept 「판형 2로 옮기기」)")
        for g in gap:
            print(f"  [gap]  {g['book']} {g['slot']}  {g['title']}  {g['source']}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
