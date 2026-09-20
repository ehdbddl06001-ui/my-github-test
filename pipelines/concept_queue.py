"""concept_queue.py — 내 오답 가운데 **이론 정리본이 없는 것**을 골라 루틴에 넘길 큐를 만든다(결정론).

2026-09-20 사용자 지시: 틀린 문항의 이론 정리는 매일 루틴이 자동으로 쓰게 한다.
「무엇을 쓸지」는 여기서 기계적으로 고르고(누가 몇 번 틀렸나·정리본이 있나), 「무엇을 쓸지의 내용」은
사람이 검토하는 콘텐츠라 `/gen-concept` 규칙을 따라 모델이 쓴다. 이 스크립트는 글을 쓰지 않는다.

큐는 세 갈래다.
  note   — 학습 목표(objective)는 붙어 있는데 그 정리본이 아직 없는 오답. 정리본을 새로 쓴다.
  link   — 학습 목표가 없는 문항의 오답. 먼저 목표를 정해 문항에 `objective` 를 붙이고,
           그 목표의 정리본이 없으면 note 로 이어진다(같은 주제의 오답은 한 줄로 묶어 보여 준다).
  gap    — 오답과 무관하게 **기본틀(content/outline/subjects.yaml)에서 아직 비어 있는 자리**.
           오답 큐가 비었을 때 커리큘럼 순서대로 한 칸씩 채우라고 내놓는다(2026-09-21 추가).
           이미 단원이 있는 책만 대상으로 하고, 그 책의 해리슨 서술 순서에서 앞쪽 빈 슬롯부터 준다.
우선순위 = 반복 오답·후속 확인 실패·표시(learning_log 의 priority)를 그대로 쓴다.

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


def build(events: list[dict]) -> dict:
    concepts, _ = load_concepts()
    questions = load_questions()
    S = ll.states(events, {q: m.get("objective") for q, m in questions.items() if m.get("objective")})
    notes: list[dict] = []
    links: dict[tuple[str, str], dict] = {}
    for key, s in S.items():
        if not s.status or not s.wrongs:
            continue
        if s.objective:
            if s.objective in concepts:
                continue                                  # 정리본이 이미 있다 — 오답은 그 단원에 모인다
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
    notes.sort(key=lambda x: (-x["priority"], -x["wrongs"], x["objective"]))
    link_list = sorted(links.values(), key=lambda x: (-x["priority"], -x["wrongs"], x["topic"], x["subtopic"]))
    return {"generated": ll.kst_day(""), "note": notes, "link": link_list, "gap": gaps,
            "counts": {"note": len(notes), "link": len(link_list), "gap": len(gaps),
                       "wrong_objectives_with_note": sum(1 for s in S.values() if s.objective and s.wrongs and s.objective in concepts)}}


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
    a = ap.parse_args(argv)
    if a.events:
        events = ll.read_events(Path(a.events))
    else:
        ll.sync_inbox()
        events = ll.read_events(ll.SYNC_FILE)
    q = build(events)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(q, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
    note, link, gap = q["note"], q["link"], q["gap"]
    if a.limit:
        note, link, gap = note[:a.limit], link[:a.limit], gap[:a.limit]
    if a.json:
        print(json.dumps({"note": note, "link": link, "gap": gap, "counts": q["counts"]}, ensure_ascii=False, indent=1))
        return 0
    if not events:
        print("학습 기록이 없다 — 앱의 「학습 기록 내보내기」가 드라이브 수신함에 들어왔는지 본다(동기화 미설정이면 정상).")
    print(f"정리본 대기(note) {q['counts']['note']}건 · 목표 연결 대기(link) {q['counts']['link']}건 · "
          f"이미 정리본이 있는 오답 목표 {q['counts']['wrong_objectives_with_note']}개")
    for n in note:
        print(f"  [note] {n['objective']}  오답 {n['wrongs']}회 · 우선순위 {n['priority']} · {n['topic']}/{n['subtopic']} · 문항 {', '.join(n['questions'][:4])}")
    for l in link:
        print(f"  [link] {l['topic']}/{l['subtopic']}  오답 {l['wrongs']}회 · 우선순위 {l['priority']} · 문항 {', '.join(l['questions'][:4])}")
    if not note and not link:
        for g in gap:
            print(f"  [gap]  {g['book']} {g['slot']}  {g['title']}  {g['source']}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
