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
  root   — 정리본이 있는 **임상** 목표를 새로 틀렸는데 그 정리본에 기초 뿌리(`roots`)도 「없음」(`roots_none`)도 없을 때
           (2026-11-21 사용자 결정 — 임상 판단 밑의 기초 기전을 학문별 책에 따로 쌓는다). 기초 정리본은 **기전 단위**다:
           같은 기전의 기초 정리본이 이미 있으면(`concepts.py --basic`) 새로 쓰지 않고 `roots` 로 잇기만 한다.
           기초 기전이 없는 목표(검진 주기·법규·역학 계산·지침 수치)는 `roots_none` 에 이유를 적는다.
           **앞으로 틀리는 것부터** — 마지막 오답이 ROOTS_FROM 이후인 목표만(옛 정리본은 다시 틀릴 때 붙는다).
           예외 하나(2026-11-23 사용자 결정) — **반복 오답 상위 20개 임상 정리본**(2회 이상 틀린 것 · 오답 수 → 우선순위 → id)은 그 전 오답이라도
           올린다(`backfill: true`, 출력 「상위 20 소급」). 상위 20 은 뿌리가 붙었는지와 무관하게 전체 임상 정리본에서 뽑으므로
           뿌리를 단 자리를 21위가 채우지 않는다 — 소급은 많아야 20개에서 끝난다.
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
  figure — 정리본 그림(2026-09-27 사용자 요청 — 확실한 라벨의 심전도·조직·영상 사진). 세 갈래, 이 순서로:
           question = 이 목표의 영상 문항 그림이 그림 기준(concept_figures.eligibility)을 통과하는데 아직 안 붙었다
           attach   = figures_wanted 로 요청한 그림이 풀에 들어왔다(exam-builder 아침 수확 `opendata demand`)
           assess   = 그림을 붙일지·요청할지·필요 없는지 아직 판단하지 않았다(figures/figures_wanted/figures_none 모두 없음)
           풀(exam-builder)을 못 찾으면 assess 만 낸다.
  gap    — 오답과 무관하게 **기본틀(content/outline/subjects.yaml)에서 아직 비어 있는 자리**.
           오답 큐가 비었을 때 커리큘럼 순서대로 한 칸씩 채우라고 내놓는다(2026-09-21 추가).
           이미 단원이 있는 책만 대상으로 하고, 책마다 「이미 쓴 단원 다음 자리」의 빈 슬롯 하나를 준다.
           책 순서는 **정리본이 적은 책 먼저**(같으면 기본틀 순서) — 2026-11-23 사용자 선택. 그 전에는 많은 책이
           먼저라 루틴이 하루 하나씩 같은 과만 채웠다(10월 류마티스 12개 · 11월 순환기 23개).
           기초의학 학문별 책은 대상이 아니다(기초 정리본은 `root` 에서만 생긴다).
           **국시 핵심 공백 과목 먼저**(2026-11-23 사용자 결정) — `books_config.yaml` `gap_priority` 의 책(혈액종양 · 소화기 ·
           신경 · 감염 · 내분비 · 외과) 가운데 정리본이 `until`(12)개 미만인 책이 앞 묶음이고, 그 안에서도 적은 책부터다.
           12개가 된 책은 일반 순서로 내려간다 — 여섯 책이 모두 12개가 되면 전체 「적은 책 먼저」와 같아진다.
  verify — 원고에 **미대조 표시**가 남은 정리본(2026-11-23 사용자 결정). 표시 = `[[?출처…]]`(이 주장만 원문 미대조)와
           손으로 적은 `†`(용량 · 기간 · 세부 수치를 대조하지 못했다는 표시) — `concepts.unverified_marks`.
           오답이 걸린 목표(우선순위 높은 것) → 표시 많은 것 → id 순. **PC 세션 · Actions 전용**이다 — 클라우드 루틴은
           PubMed · 지침 원문을 못 연다. 그래서 기본 출력에는 건수 한 줄만 찍고 목록은 `--verify` 때만 찍는다(JSON 에는 늘 있다).
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
  python pipelines/concept_queue.py --verify --limit 20   # 미대조 표시 보강 목록(PC 세션 · Actions 전용)
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import learning_log as ll
import outline as ol
from concepts import is_basic, load_concepts, load_questions, unverified_marks
from traps import trap_tag
import kr_guidelines as krg

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "state" / "concept_queue.json"
WRONG_SYNC = ROOT / "state" / "wrong_sync"
ROOTS_FROM = "2026-11-21"     # 이 날 이후에 틀린 목표만 기초 뿌리를 묻는다(사용자 결정: 소급하지 않는다)
ROOT_BACKFILL_TOP = 20        # 예외 — 반복 오답 상위 N개 임상 정리본만 그 전 오답이라도 묻는다(2026-11-23 사용자 결정)
ROOT_BACKFILL_MIN_WRONGS = 2  # 「반복」 = 오답 2회 이상. 1회짜리로 20을 채우면 동률을 id 순으로 끊게 돼 앞 글자 과(알레르기 · 순환기)만 뽑힌다


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
    roots: list[dict] = []
    links: dict[tuple[str, str], dict] = {}
    top = root_backfill(S, concepts)
    for key, s in S.items():
        if not s.status or not s.wrongs:
            continue
        dists.extend(_dists(s, questions))
        if s.objective:
            if s.objective in concepts:
                touches.extend(_touches(s, concepts[s.objective], questions))
                variants.extend(_variants(s, concepts[s.objective], questions, (sched.get(key) or {}).get("due", "")))
                roots.extend(_roots(s, concepts[s.objective], top.get(s.objective, 0)))
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
    figures = _figures(concepts, questions, S)
    restyles = _restyles(concepts, S)
    krdiffs = _krdiffs(concepts, S)
    verifies = _verifies(concepts, S)
    notes.sort(key=lambda x: (-x["priority"], -x["wrongs"], x["objective"]))
    link_list = sorted(links.values(), key=lambda x: (-x["priority"], -x["wrongs"], x["topic"], x["subtopic"]))
    variants.sort(key=lambda x: (x["due"] or "9999", -x["priority"], x["qid"]))
    # 새로 틀린 목표 먼저(우선순위 순), 그 뒤에 상위 20 소급(순위 순)
    roots.sort(key=lambda x: (x["backfill"], x["rank"] if x["backfill"] else -x["priority"], x["objective"]))
    seen_d: set[str] = set()
    dists = [d for d in dists if not (d["key"] in seen_d or seen_d.add(d["key"]))]
    return {"generated": ll.kst_day(""), "note": notes, "link": link_list, "touch": touches, "root": roots,
            "variant": variants, "dist": dists, "restyle": restyles, "krdiff": krdiffs, "figure": figures, "gap": gaps, "verify": verifies,
            "counts": {"note": len(notes), "link": len(link_list), "touch": len(touches), "gap": len(gaps),
                       "restyle": len(restyles), "root": len(roots), "krdiff": len(krdiffs),
                       "root_backfill": sum(1 for r in roots if r["backfill"]),
                       "verify": len(verifies), "verify_marks": sum(v["marks"] for v in verifies),
                       "variant": len(variants), "dist": len(dists), "figure": len(figures),
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


def root_backfill(S: dict, concepts: dict) -> dict[str, int]:
    """{임상 정리본 id: 순위(1~ROOT_BACKFILL_TOP)} — 반복 오답 상위 N개(오답 수 → 우선순위 → id).

    **뿌리(`roots` · `roots_none`)가 붙었는지는 보지 않는다.** 붙은 것을 빼고 뽑으면 그 자리를 다음 순위가 채워
    옛 정리본 전체가 차례로 소급된다 — 사용자 결정은 「상위 20개만」이다. 기초 정리본(`layer: basic`)은 뺀다.
    오답이 ROOT_BACKFILL_MIN_WRONGS 회 미만인 목표는 「반복 오답」이 아니라서 순위에 넣지 않는다 — 그래서 20개보다 적을 수 있다
    (2026-11-23 실측: 2회 이상 틀린 임상 정리본 10개 · 1회 118개).
    """
    rows = sorted((-s.wrongs, -s.priority, s.objective) for s in S.values()
                  if s.objective and s.wrongs >= ROOT_BACKFILL_MIN_WRONGS and s.objective in concepts
                  and not is_basic(concepts[s.objective]))
    return {obj: i for i, (_, _, obj) in enumerate(rows[:ROOT_BACKFILL_TOP], 1)}


def _roots(s, concept: dict, rank: int = 0) -> list[dict]:
    """기초 뿌리를 아직 정하지 않은 임상 정리본 — 한 줄. 새로 틀린 목표이거나(ROOTS_FROM 이후),
    반복 오답 상위 20(rank ≥ 1 — `root_backfill`)이면 그 전 오답이라도 낸다(`backfill: true`)."""
    if is_basic(concept) or concept.get("roots") or concept.get("roots_none") is not None:
        return []
    backfill = (s.last_wrong_day or "") < ROOTS_FROM
    if backfill and not rank:
        return []
    return [{"objective": concept.get("id"), "title": str(concept.get("title", "")), "topic": str(concept.get("topic", "")),
             "path": str(concept.get("path", "")), "day": s.last_wrong_day, "priority": s.priority,
             "wrongs": s.wrongs, "backfill": backfill, "rank": rank}]


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
        tag = trap_tag(q)
        if tag and tag.get("id"):                     # 함정 계열 문항 — 변형 A 는 그 계열의 반대쪽(2026-09-29)
            seed = f"design.trap({tag['id']}) → " + ("mirror.when" if tag.get("side") == "trap" else "trap 조건")
        else:
            seed = "design.switch" if isinstance(d.get("switch"), dict) else ("design.discriminator" if d.get("discriminator") else "해설")
        out.append({"objective": concept.get("id"), "qid": qid, "exam": str(q.get("type", "")), "have": have.get(qid, 0),
                    "need": 2 - have.get(qid, 0), "due": due, "priority": s.priority, "seed": seed})
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


def load_kr() -> tuple[list[dict], dict]:
    """국내 vs 해리슨 대조 항목과 레지스트리 — 시험은 이 함수를 바꿔 끼운다(코드 시험이 실제 콘텐츠를 읽지 않게)."""
    return krg.diff_items(), krg.load_registry()


def _krdiffs(concepts: dict, S: dict, kr: tuple[list[dict], dict] | None = None) -> list[dict]:
    """국내 지침 ↔ 해리슨 차이를 아직 반영하지 않은 정리본 — 오답이 걸린 목표 먼저 → 남은 항목 많은 것 → id.

    짝 = 정리본 `outline` 슬롯이 대조 항목의 slot 이거나 그 지침 트랙의 slots 에 있다(`same` 항목은 뺀다).
    끝난 표시 = 정리본 frontmatter `kr_diffs`(반영함) · `kr_diffs_skip`(이 정리본 목표와 무관). 새 대조 항목이
    생기면 그 항목만 다시 뜬다. 규칙 /gen-concept 「국내 vs 해리슨([krdiff])」.
    """
    items, reg = kr if kr is not None else load_kr()
    if not items:
        return []
    tslots = krg.track_slots(reg)
    pri: dict[str, int] = {}
    for s in S.values():
        if s.objective and s.wrongs:
            pri[s.objective] = max(pri.get(s.objective, 0), s.priority or 1)
    out = []
    for cid, c in concepts.items():
        if is_basic(c):
            continue
        done = {str(x) for x in (c.get("kr_diffs") or [])} | {str(x) for x in (c.get("kr_diffs_skip") or [])}
        todo = [it for it in krg.items_for_slot(str(c.get("outline") or ""), items, tslots) if str(it.get("id")) not in done]
        if not todo:
            continue
        out.append({"objective": cid, "title": str(c.get("title", "")), "path": str(c.get("path", "")),
                    "slot": str(c.get("outline")), "items": [str(it["id"]) for it in todo],
                    "files": sorted({f"content/outline/kr_vs_harrison/{it['subject_slug']}.yaml" for it in todo}),
                    "wrong": cid in pri, "priority": pri.get(cid, 0)})
    return sorted(out, key=lambda x: (not x["wrong"], -x["priority"], -len(x["items"]), x["objective"]))


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


def _verifies(concepts: dict, S: dict) -> list[dict]:
    """미대조 표시(`[[?…]]` · 손으로 적은 †)가 남은 정리본 — 오답이 걸린 목표(우선순위 높은 것) → 표시 많은 것 → id.

    루틴이 처리하는 큐가 아니다(PubMed · 지침 원문을 못 연다) — PC 세션 · Actions 가 원문을 열어 표시를 지운다.
    """
    pri: dict[str, int] = {}
    for s in S.values():
        if s.objective and s.wrongs:
            pri[s.objective] = max(pri.get(s.objective, s.priority), s.priority)
    out = []
    for cid, c in concepts.items():
        m = unverified_marks(c)
        if not m["marks"]:
            continue
        out.append({"objective": cid, "title": str(c.get("title", "")), "path": str(c.get("path", "")),
                    "claims": m["claims"], "dagger": m["dagger"], "marks": m["marks"], "sources": m["sources"],
                    "wrong": cid in pri, "priority": pri.get(cid, 0)})
    return sorted(out, key=lambda x: (not x["wrong"], -x["priority"], -x["marks"], x["objective"]))


def _figures(concepts: dict, questions: dict, S: dict) -> list[dict]:
    import concept_figures as cf
    pool = cf.load_pool()
    prio = {s.objective: s.priority for s in S.values() if s.objective}
    out: list[dict] = []
    for cid, c in sorted(concepts.items()):
        have = {str(f.get("asset")) for f in c.get("figures") or [] if isinstance(f, dict)}
        full = len(have) >= cf.MAX_FIGURES
        if pool and not full:
            for qid, q in sorted(questions.items()):
                if q.get("objective") != cid or q.get("type") != "imaging":
                    continue
                asset = str((q.get("attribution") or {}).get("asset_id") or "")
                r = pool.get(asset)
                if r and asset not in have and not cf.eligibility(r):
                    out.append({"kind": "question", "concept": cid, "qid": qid, "asset": asset,
                                "label": cf.dataset_label(r), "priority": prio.get(cid, 0)})
            rej = {str(x.get("asset")) for x in c.get("figures_rejected") or [] if isinstance(x, dict)}
            for w in c.get("figures_wanted") or []:
                hits = [x for x in cf.wanted_fulfilled(w, pool, cid, rej) if x not in have]
                if hits:
                    out.append({"kind": "attach", "concept": cid, "request": w, "assets": hits[:3], "priority": prio.get(cid, 0)})
        if not (c.get("figures") or c.get("figures_wanted") or c.get("figures_none")):
            out.append({"kind": "assess", "concept": cid, "title": str(c.get("title", "")), "priority": prio.get(cid, 0)})
    rank = {"question": 0, "attach": 1, "assess": 2}
    out.sort(key=lambda x: (rank[x["kind"]], -x["priority"], x["concept"]))
    return out


def _books_cfg() -> dict:
    import yaml
    return yaml.safe_load((ROOT / "pipelines" / "books_config.yaml").read_text(encoding="utf-8")) or {}


def gap_priority(books_cfg: dict) -> tuple[set[str], int]:
    """(국시 핵심 공백 책, 기준 수) — books_config `gap_priority: {books: [...], until: N}`.
    키가 없거나 `books` 가 비었거나 `until` 이 양의 정수가 아니면 (빈 집합, 0) = 가중치 없음(전체 「적은 책 먼저」)."""
    gp = books_cfg.get("gap_priority")
    if not isinstance(gp, dict):
        return set(), 0
    books, until = gp.get("books"), gp.get("until")
    if not isinstance(books, list) or not books or isinstance(until, bool) or not isinstance(until, int) or until < 1:
        return set(), 0
    return {str(b) for b in books}, until


def _gaps(concepts: dict, questions: dict, S: dict, books_cfg: dict | None = None) -> list[dict]:
    """기본틀에서 빈 슬롯 — 이미 단원이 있는 책만, 책마다 하나(쓴 자리 다음). 정리본이 적은 책부터.

    루틴은 06시 실행마다 맨 앞 [gap] 하나만 쓴다. 많은 책을 앞에 두면 그 책만 계속 늘어난다(되먹임) —
    적은 책을 앞에 두면 하나 쓸 때마다 그 책이 뒤로 물러나 모든 과가 번갈아 채워진다.
    정리본이 0개인 책은 넣지 않는다(오답이 이끌게 둔다 — 사용자 선택).
    기초의학 학문별 책(books_config `disciplines` — 생리학 · 병리학 …)도 넣지 않는다: 기초 정리본은 틀린 문항의
    `[root]` 에서만 생긴다(2026-11-21 사용자 결정 — 소급 · 빈칸 채우기 ✗). 적은 책 먼저로 바꾸면 이 책들이 맨 앞에 온다.

    국시 핵심 공백 과목(2026-11-23 사용자 결정, `gap_priority`): 핵심 책 가운데 정리본이 `until` 개 **미만**인 책이
    앞 묶음(`core: true`)이고, 묶음 안 · 밖 모두 「적은 책 먼저 · 같으면 기본틀 순서」다. 하나 쓰면 그 책의 수가 올라
    묶음 안에서 뒤로 물러나고, `until` 개가 되면 묶음에서 빠진다 — 한 책만 계속 채우는 되먹임이 없다.
    핵심 책이라도 0개면 넣지 않는다. books_cfg 를 넘기면 그 설정으로 계산한다(시험용 · None = books_config.yaml).
    """
    books_cfg = _books_cfg() if books_cfg is None else books_cfg
    bmap = dict(books_cfg.get("books") or {})
    basic_books = set((books_cfg.get("disciplines") or {}).values())
    core_books, until = gap_priority(books_cfg)
    books, _ = ol.load()
    have: dict[str, int] = {}                       # 책 → 그 책에 쌓인 정리본 수
    for c in concepts.values():
        b = bmap.get(str(c.get("topic") or ""))
        if b:
            have[b] = have.get(b, 0) + 1
    filled = {str(c.get("outline") or "") for c in concepts.values()}
    out: list[dict] = []
    for book, slots in books.items():
        if book not in have or book in basic_books:
            continue                                 # 아직 시작하지 않은 과 · 기초의학 학문별 책은 오답이 이끌게 둔다
        # 「이어서 읽기」 — 이미 쓴 단원 다음 자리부터 채운다. 앞에서부터 채우면 그 과에서
        # 이미 공부한 자리와 동떨어진 장(예: 신장내과 51장 간질성 방광염)이 먼저 나온다.
        last = max((sl.order for sl in slots if sl.id in filled), default=-1)
        nxt = next((sl for sl in slots if sl.id not in filled and sl.order > last), None)             or next((sl for sl in slots if sl.id not in filled), None)
        if nxt:
            g = {"book": book, "slot": nxt.id, "title": nxt.title,
                 "source": nxt.source, "chapters": nxt.chapters, "have": have[book],
                 "core": book in core_books and have[book] < until}
            if g["core"]:
                g["core_until"] = until
            out.append(g)
    order = {b: i for i, b in enumerate(books)}
    # 핵심 공백 책(기준 수 미만) 먼저 → 적은 책 먼저 → 같으면 기본틀(subjects.yaml) 순서
    out.sort(key=lambda g: (not g["core"], g["have"], order[g["book"]]))
    return out


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--events", help="학습 기록 파일(기본: state/learning_sync/events.json + 수신함)")
    ap.add_argument("--limit", type=int, default=0, help="오늘 처리할 상위 N개만 출력(0=전부)")
    ap.add_argument("--json", action="store_true", help="사람이 읽는 줄 대신 JSON 만")
    ap.add_argument("--wrong-sync", help="오답 목록 폴더(기본: state/wrong_sync)")
    ap.add_argument("--no-wrongnote", action="store_true", help="학습 기록만 쓴다(오답 목록 무시)")
    ap.add_argument("--verify", action="store_true",
                    help="미대조 표시 보강 목록 [verify] 도 찍는다(PC 세션 · Actions 전용 — 루틴은 원문을 못 연다)")
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
    rs, fig, root, ver, krd = q["restyle"], q["figure"], q["root"], q["verify"], q["krdiff"]
    if a.limit:
        note, link, touch, var, dist, gap, rs, fig, root, ver, krd = (
            x[:a.limit] for x in (note, link, touch, var, dist, gap, rs, fig, root, ver, krd))
    if a.json:
        shown = {"note": note, "link": link, "touch": touch, "root": root, "variant": var, "dist": dist, "restyle": rs, "krdiff": krd, "figure": fig,
                 "gap": gap, "counts": q["counts"]}
        if a.verify:                                    # 목록은 청했을 때만 — 건수는 counts 에 늘 있다
            shown["verify"] = ver
        print(json.dumps(shown, ensure_ascii=False, indent=1))
        return 0
    if not events and not q["counts"]["from_wrongnote"]:
        print("학습 기록이 없다 — 앱의 「학습 기록 내보내기」가 드라이브 수신함에 들어왔는지 본다(동기화 미설정이면 정상).")
    print(f"정리본 대기(note) {q['counts']['note']}건 · 목표 연결 대기(link) {q['counts']['link']}건 · "
          f"손질 대기(touch) {q['counts']['touch']}건 · 기초 뿌리 대기(root) {q['counts']['root']}건 · "
          f"변형 대기(variant) {q['counts']['variant']}건 · "
          f"오답 보기 설명 대기(dist) {q['counts']['dist']}건 · 그림 대기(figure) {q['counts']['figure']}건 · "
          f"이미 정리본이 있는 오답 목표 {q['counts']['wrong_objectives_with_note']}개 · "
          f"오답 목록에서 채운 오답 {q['counts']['from_wrongnote']}건")
    print(f"미대조 표시 보강 대기(verify) {q['counts']['verify']}건 · 표시 {q['counts']['verify_marks']}개 — "
          f"PC 세션 · Actions 전용(루틴은 처리하지 않는다 · 목록은 --verify)")
    for n in note:
        print(f"  [note] {n['objective']}  오답 {n['wrongs']}회 · 우선순위 {n['priority']} · {n['topic']}/{n['subtopic']} · 문항 {', '.join(n['questions'][:4])}")
    for l in link:
        print(f"  [link] {l['topic']}/{l['subtopic']}  오답 {l['wrongs']}회 · 우선순위 {l['priority']} · 문항 {', '.join(l['questions'][:4])}")
    for t in touch:
        print(f"  [touch] {t['objective']}  새 혼동 {t['cover']} 「{str(t['chosen'])[:30]}」 → 정답 「{str(t['answer'])[:30]}」")
    for r in root:
        print(f"  [root] {r['objective']}  기초 뿌리 미정 · 마지막 오답 {r['day']} · 우선순위 {r['priority']} · {r['topic']} · {r['title'][:40]}"
              + (f" · 상위 {ROOT_BACKFILL_TOP} 소급(오답 {r['wrongs']}회 · {r['rank']}위)" if r["backfill"] else ""))
    if root:
        print("  (먼저 `python pipelines/concepts.py --basic` 으로 같은 기전의 기초 정리본이 있는지 본다 — /gen-concept 「[root]」)")
    for v in var:
        print(f"  [variant] {v['objective']}  문항 {v['qid']} 변형 {v['need']}개 더 · 예정일 {v['due'] or '-'} · 씨앗 {v['seed']}")
    for d in dist:
        print(f"  [dist] {d['qid']} 보기 {d['letter']} 「{str(d['chosen'])[:30]}」 설명 없음 · {d['path']}")
    for f in fig:
        if f["kind"] == "question":
            print(f"  [figure] {f['concept']}  영상 문항 {f['qid']} 의 그림 {f['asset']} 을 붙인다 — 라벨 {str(f['label'])[:50]}")
        elif f["kind"] == "attach":
            print(f"  [figure] {f['concept']}  요청한 그림이 풀에 들어옴 {', '.join(f['assets'])} — {f['request'].get('shows', '')}")
        else:
            print(f"  [figure] {f['concept']}  그림 판단 필요(붙임·요청·불필요) — {f['title'][:40]}")
    if not note and not link and not touch:
        for k in krd:
            print(f"  [krdiff] {k['objective']}  국내 vs 해리슨 항목 {len(k['items'])}개 미반영({', '.join(k['items'][:3])}"
                  + ("…" if len(k["items"]) > 3 else "") + f") · {', '.join(k['files'])}"
                  + (f" · 오답 우선순위 {k['priority']}" if k["wrong"] else ""))
        if krd:
            print(f"  (국내 지침 ↔ 해리슨 차이를 넣을 정리본 {q['counts']['krdiff']}개 — /gen-concept 「국내 vs 해리슨([krdiff])」)")
        for r in rs:
            print(f"  [restyle] {r['objective']}  {r['title'][:40]}" + (f" · 오답 우선순위 {r['priority']}" if r["priority"] else "")
                  + f" · {r['path']}")
        if rs:
            print(f"  (판형 2 로 옮길 정리본 {q['counts']['restyle']}개 남음 — /gen-concept 「판형 2로 옮기기」)")
        for g in gap:
            print(f"  [gap]  {g['book']} {g['slot']}  {g['title']}  {g['source']}"
                  + (f" · 핵심 과목 우선(정리본 {g['have']}/{g['core_until']})" if g["core"] else f" · 정리본 {g['have']}개"))
    if a.verify:
        for v in ver:
            print(f"  [verify] {v['objective']}  미대조 표시 {v['marks']}개([[?…]] {v['claims']} · † {v['dagger']})"
                  + (f" · 오답 우선순위 {v['priority']}" if v["wrong"] else "")
                  + (f" · 출처 {', '.join(v['sources'][:4])}" + ("…" if len(v["sources"]) > 4 else "") if v["sources"] else "")
                  + f" · {v['path']}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
