"""
anatomy_daily.py — 오늘의 해부학 학습 세트를 결정론적으로 선택한다.

입력: content/anatomy/{concepts,questions,answers,daily}/ + anatomy_schedule.py
출력: content/anatomy/daily/<date>.md (kind: daily_plan)

규칙(spec §10):
  - 기본 세트는 20~35분 분량(개념 카드 ~5 + 문항 8~12 + 복습).
  - 다음 수업/시험 범위 우선. 수업일에는 그날 수업 예습을 최우선.
  - needs_review: true 카드는 공개 daily deck에 자동 포함하지 않는다.
  - 복습 슬롯: 1/3/7/14일 전 daily plan의 문항 id (오답 반영은 브라우저 localStorage).
  - phase별: t1-day·final-review = rapid review만 / t2-mock = 신규 축소·혼합 mock
  - 2026-10-20 이후: 아무것도 쓰지 않고 `completed` 보고(no-op).

사용:
  python pipelines/anatomy_daily.py --date 2026-08-13 [--plan] [--dry-run]
    --plan : 선택 결과와 '부족한 슬롯'(스킬이 생성해야 할 것)을 JSON으로 출력만.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import date, timedelta
from pathlib import Path

try:
    from frontmatter import split_frontmatter
    import anatomy_schedule as sched
except ModuleNotFoundError:
    from pipelines.frontmatter import split_frontmatter
    from pipelines import anatomy_schedule as sched

import yaml

ROOT = Path(__file__).resolve().parent.parent
ANAT = ROOT / "content" / "anatomy"

SLOT_SPEC = {  # phase → (개념 슬롯, 문항 수 범위)
    "t1-prep": {"preview": 1, "layer": 1, "branch": 1, "relation": 2, "q": (8, 12)},
    "t2-new": {"preview": 1, "layer": 1, "branch": 1, "relation": 2, "q": (8, 12)},
    "t2-mock": {"preview": 0, "layer": 1, "branch": 1, "relation": 2, "q": (10, 12)},
    "t1-day": {"preview": 0, "layer": 0, "branch": 0, "relation": 0, "q": (0, 6)},
    "final-review": {"preview": 0, "layer": 0, "branch": 0, "relation": 0, "q": (0, 6)},
}
CONCEPT_SLOT_KIND = {"layer": ["layer-order"], "branch": ["branch-tree", "course-tracing"],
                     "relation": ["relation", "distinction"]}


def _load_dir(sub: str) -> list[dict]:
    out = []
    d = ANAT / sub
    if d.exists():
        for p in sorted(d.rglob("*.md")):
            meta, _ = split_frontmatter(p.read_text(encoding="utf-8"))
            if meta.get("type") == "anatomy":
                meta["_path"] = str(p.relative_to(ROOT))
                out.append(meta)
    return out


def _deck_eligible(m: dict) -> bool:
    return m.get("needs_review") is not True


def _region_match(m: dict, regions: list[str]) -> int:
    return 1 if not regions or m.get("region") in regions or m.get("region") == "multi" else 0


def _rank(items: list[dict], regions: list[str], phase_exam: str) -> list[dict]:
    """결정론 순위: 부위 일치 → answer-only 우선순위 → 시험구간 일치 → id."""
    def key(m):
        return (
            -_region_match(m, regions),
            0 if m.get("priority") == "high" else 1,
            0 if m.get("exam_phase") == phase_exam else 1,
            str(m.get("id", "")),
        )
    return sorted([m for m in items if _deck_eligible(m)], key=key)


def _prev_plan_qids(d: date, days_ago: int) -> list[str]:
    p = ANAT / "daily" / f"{(d - timedelta(days=days_ago)).isoformat()}.md"
    if not p.exists():
        return []
    meta, _ = split_frontmatter(p.read_text(encoding="utf-8"))
    return list(meta.get("question_ids", []) or [])


def build_plan(d: date) -> dict:
    phase = sched.phase_for(d)
    if phase == "completed":
        return {"date": d.isoformat(), "phase": "completed",
                "action": "no-op — 2026-10-19 종료. 새 콘텐츠 생성·커밋 금지."}
    info = sched.summary(d)
    nxt = info["next_session"] or {}
    regions = []
    for s in sched.SCHEDULE_2026:
        if s["date"].isoformat() == (nxt.get("date") or ""):
            regions = s.get("regions", [])
    spec = SLOT_SPEC[phase]
    concepts = _load_dir("concepts")
    questions = _load_dir("questions")
    exam = info["exam_phase"]

    picked_concepts: dict[str, list[str]] = {}
    used: set[str] = set()
    for slot, styles in [("preview", None), ("layer", CONCEPT_SLOT_KIND["layer"]),
                         ("branch", CONCEPT_SLOT_KIND["branch"]),
                         ("relation", CONCEPT_SLOT_KIND["relation"])]:
        want = spec.get(slot, 0)
        if not want:
            continue
        pool = _rank(concepts, regions, exam)
        if styles:
            pool = [c for c in pool
                    if set(c.get("relations", []) or []) & {"branches-from", "covers",
                                                            "adjacent-to", "passes-through"}
                    or any(s in str(c.get("tags", [])) for s in styles)
                    or c.get("concept_style") in styles]
        sel = [c["id"] for c in pool if c["id"] not in used][:want]
        used.update(sel)
        picked_concepts[slot] = sel

    qmin, qmax = spec["q"]
    qpool = _rank(questions, regions, exam)
    # 스타일 균형: 같은 스타일이 절반을 넘지 않게 라운드로빈(결정론).
    by_style: dict[str, list[dict]] = {}
    for q in qpool:
        by_style.setdefault(q.get("question_style", "?"), []).append(q)
    qsel: list[str] = []
    while len(qsel) < qmax and any(by_style.values()):
        for style in sorted(by_style):
            if by_style[style] and len(qsel) < qmax:
                qsel.append(by_style[style].pop(0)["id"])
    review = {f"d-{n}": _prev_plan_qids(d, n) for n in (1, 3, 7, 14)}

    gaps = {}
    for slot in ("preview", "layer", "branch", "relation"):
        need = spec.get(slot, 0) - len(picked_concepts.get(slot, []))
        if need > 0:
            gaps[f"concept:{slot}"] = need
    if len(qsel) < qmin:
        gaps["question"] = qmin - len(qsel)

    return {
        "date": d.isoformat(), "phase": phase, "exam_phase": exam,
        "is_class_day": info["is_class_day"],
        "next_session": nxt, "regions": regions,
        "days_to_tagging1": info["days_to_tagging1"],
        "days_to_tagging2": info["days_to_tagging2"],
        "concepts": picked_concepts,
        "question_ids": qsel,
        "review": review,
        "gaps": gaps,
        "est_minutes": min(35, max(20, 2 * sum(len(v) for v in picked_concepts.values())
                                   + 2 * len(qsel) + 5)),
    }


def missing_dates(today: date, limit: int | None = None) -> list[date]:
    """START_DATE~어제 중 daily_plan 카드가 없는 날짜(밀린 날)를 오래된 순으로.

    주간 이용 한도 초과 등으로 루틴이 못 돈 날을 결정론적으로 찾는다.
    completed 구간(2026-10-20~)은 제외. limit이 있으면 앞에서부터 그만큼만.
    """
    out: list[date] = []
    d = sched.START_DATE
    while d < today:
        if sched.phase_for(d) != "completed" \
                and not (ANAT / "daily" / f"{d.isoformat()}.md").exists():
            out.append(d)
        d += timedelta(days=1)
    return out[:limit] if limit is not None else out


def write_plan(plan: dict, dry: bool) -> Path | None:
    if plan.get("phase") == "completed":
        print(json.dumps(plan, ensure_ascii=False))
        return None
    d = plan["date"]
    p = ANAT / "daily" / f"{d}.md"
    old_id = None
    if p.exists():
        old, _ = split_frontmatter(p.read_text(encoding="utf-8"))
        old_id = old.get("id")
    meta = {
        "id": old_id or f"anatomy-daily-{d}",
        "type": "anatomy", "kind": "daily_plan", "topic": "Anatomy",
        "subtopic": f"daily plan {d}", "date": d, "confidence": "high",
        "source": "pipelines/anatomy_daily.py (결정론 선택)",
        "exam_phase": plan["exam_phase"], "phase": plan["phase"],
        "regions": plan["regions"],
        "concept_ids": plan["concepts"], "question_ids": plan["question_ids"],
        "review": plan["review"], "est_minutes": plan["est_minutes"],
        "publishable": True,  # 계획 자체는 id 목록뿐(민감 자산 없음)
    }
    if plan.get("made_up_on"):  # 밀린 날을 나중에 따라잡아 만든 계획
        meta["made_up"] = True
        meta["generated_on"] = plan["made_up_on"]
    nxt = plan.get("next_session") or {}
    body = (
        f"## 오늘의 학습 ({d} · {plan['phase']})\n\n"
        f"- 다음 수업/시험: {nxt.get('date', '-')} {', '.join(nxt.get('topics', []) or [])}\n"
        f"- Tagging 1까지 {plan['days_to_tagging1']}일 · Tagging 2까지 {plan['days_to_tagging2']}일\n"
        f"- 예상 소요: 약 {plan['est_minutes']}분\n"
        f"- 문항 {len(plan['question_ids'])}개 · 개념 "
        f"{sum(len(v) for v in plan['concepts'].values())}개 · 복습 "
        f"{sum(len(v) for v in plan['review'].values())}개\n\n"
        "마지막에 **오늘 반드시 말로 설명할 3개 관계**를 웹 화면이 오늘 문항의 "
        "관계 카드에서 뽑아 보여준다.\n"
    )
    if not dry:
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("---\n" + yaml.safe_dump(
            meta, allow_unicode=True, sort_keys=False, default_flow_style=None, width=100
        ) + "---\n\n" + body, encoding="utf-8")
    print(f"daily plan {d}: 문항 {len(plan['question_ids'])} · gaps {plan['gaps'] or '없음'}"
          f"{' (dry-run)' if dry else ''}")
    return p


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", help="YYYY-MM-DD (기본: KST 오늘)")
    ap.add_argument("--plan", action="store_true", help="JSON 출력만(쓰기 없음)")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--backlog", action="store_true",
                    help="밀린 날짜(daily_plan 없는 과거 날짜) 목록만 JSON 출력")
    ap.add_argument("--catch-up", nargs="?", const=3, type=int, metavar="N",
                    help="밀린 날짜를 오래된 순으로 최대 N개(기본 3) 따라잡아 계획 생성")
    a = ap.parse_args()
    d = date.fromisoformat(a.date) if a.date else sched.kst_today()

    if a.backlog:
        print(json.dumps({"today": d.isoformat(),
                          "missing": [x.isoformat() for x in missing_dates(d)]},
                         ensure_ascii=False))
        return 0

    if a.catch_up:
        made = []
        for md in missing_dates(d, limit=max(0, a.catch_up)):
            plan = build_plan(md)
            plan["made_up_on"] = d.isoformat()
            write_plan(plan, a.dry_run)
            made.append(md.isoformat())
        remaining = [x.isoformat() for x in missing_dates(d)]
        print(f"catch-up: {len(made)}개 생성 {made} · 남은 밀린 날 "
              f"{len(remaining)}개{' (dry-run이라 미반영)' if a.dry_run else ''}")

    plan = build_plan(d)
    if a.plan:
        print(json.dumps(plan, ensure_ascii=False, indent=1))
        return 0
    write_plan(plan, a.dry_run)
    return 0


if __name__ == "__main__":
    sys.exit(main())
