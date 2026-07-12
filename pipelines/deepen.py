"""
deepen.py — AI랩 '주차 심화(deep-dive) 큐' 관리 + 결정론적 작업지시서 생성.

통과(check_week.py)는 진도를 '앞으로' 빼는 게이트다. 하지만 통과가 곧 '깊이 안다'는
아니다(1주차 회고에 그렇게 적혀 있다). 그래서 **완료된 주차를 되돌아보며 심화 카드
(kind: deepdive)를 한 장 쌓는** 별도의 축이 필요하다 — scrape/landmark 논문이
recency·impact 두 축으로 도는 것과 같은 구조다.

MedKOS 원칙대로 **무엇을 심화할지 고르는 결정론은 여기(코드)**가 하고, 실제 A~E 분석
(구조 파악·문제점·대안·모델 심화·자율학습 로드맵)은 `/deepen-week` 스킬(LLM)이 카드로
쓴다. 이 파일은 상태를 쓰지 않는다(읽기 전용·멱등). Source of Truth는 content/ 이므로,
'이미 심화한 주차'는 별도 state가 아니라 **content/ailab의 deepdive 카드에서 역산**한다.

큐 규칙:
  대상 = check_week가 완료 처리한 주차(state/ailab_progress.json 의 done) 중,
         아직 deepdive 카드가 없는 가장 이른 주차.
  → 매주 도는 루틴은 "완료했지만 아직 안 판 주차"를 하나씩 자동으로 집어 심화한다.

사용:
  python pipelines/deepen.py                 # 다음 심화 대상(작업지시서) 출력
  python pipelines/deepen.py --list          # 완료 주차별 심화 여부 큐 표시
  python pipelines/deepen.py --week 1         # 특정 주차를 강제로 대상 지정
  python pipelines/deepen.py --json           # 작업지시서를 JSON으로(스킬/도구가 파싱)
  python -c "from pipelines.deepen import work_order; print(work_order())"
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

# datasets.py/check_week.py 와 같은 이중 import 패턴(진입점에 따라 경로가 다름).
try:
    from datasets import topic_for_week, TOTAL_WEEKS
    from state import ailab_progress
    from frontmatter import load
except ImportError:  # `from pipelines.deepen import ...`
    from pipelines.datasets import topic_for_week, TOTAL_WEEKS
    from pipelines.state import ailab_progress
    from pipelines.frontmatter import load

ROOT = Path(__file__).resolve().parent.parent
AILAB_DIR = ROOT / "content" / "ailab"

DEEPDIVE_KIND = "deepdive"   # 심화 카드의 frontmatter kind
WEEKLY_KIND = "weekly"       # 원 실습 카드의 kind(심화의 원본)


def _int_or_none(v) -> int | None:
    try:
        return int(v)
    except (TypeError, ValueError):
        return None


def _cards() -> list:
    """content/ailab 하위의 모든 카드(파싱 성공한 것만)."""
    out = []
    if AILAB_DIR.exists():
        for p in sorted(AILAB_DIR.rglob("*.md")):
            d = load(p)
            if not d.errors:
                out.append(d)
    return out


def deepdive_weeks() -> set[int]:
    """이미 심화 카드(kind: deepdive)가 존재하는 주차 집합 — content에서 역산."""
    weeks: set[int] = set()
    for d in _cards():
        if d.meta.get("kind") == DEEPDIVE_KIND:
            w = _int_or_none(d.meta.get("week"))
            if w is not None:
                weeks.add(w)
    return weeks


def card_for_week(week: int, kind: str = WEEKLY_KIND) -> str | None:
    """해당 주차의 원 실습 카드 id(심화의 '원본'). 없으면 None."""
    for d in _cards():
        if d.meta.get("kind") == kind and _int_or_none(d.meta.get("week")) == week:
            return d.id
    return None


def completed_weeks() -> list[int]:
    """check_week가 완료 처리한 주차(오름차순)."""
    done = ailab_progress().get("done", {})
    return sorted(w for w in (_int_or_none(k) for k in done) if w is not None)


def achieved(week: int) -> dict:
    """그 주차가 통과할 때 남긴 지표·값·완료일(state/ailab_progress.json)."""
    entry = ailab_progress().get("done", {}).get(str(week), {})
    return {
        "metric": entry.get("metric"),
        "value": entry.get("value"),
        "date": entry.get("date"),
    }


def pending_deepdives() -> list[int]:
    """완료됐지만 아직 심화 카드가 없는 주차(오름차순 = 심화 대기 큐)."""
    have = deepdive_weeks()
    return [w for w in completed_weeks() if w not in have]


def work_order(week: int | None = None) -> dict | None:
    """다음 심화 대상의 작업지시서. week를 주면 그 주차를 강제 지정.

    반환 None = 심화할 게 없음(완료 주차를 모두 심화했거나, 완료 주차가 없음).
    """
    if week is None:
        pending = pending_deepdives()
        if not pending:
            return None
        week = pending[0]

    t = topic_for_week(week)
    return {
        "week": week,
        "total": TOTAL_WEEKS,
        "goal": t["goal"],
        "arch": t["arch"],
        "dataset_key": t["dataset_key"],
        "dataset_name": t["dataset_name"],
        "dataset_url": t["dataset_url"],
        "modality": t["modality"],
        # 심화의 '원본' — 이 카드와 대응 노트북을 읽어 A~E를 쓴다.
        "source_card": card_for_week(week),
        "notebook_hint": f"notebooks/ailab_week{week:02d}_*.ipynb",
        # 통과 당시 기록(정직한 출발점: '무엇으로' 통과했는지)
        "achieved": achieved(week),
        "already_deepened": week in deepdive_weeks(),
        "queue": pending_deepdives(),
    }


def _print_order(wo: dict) -> None:
    a = wo["achieved"]
    got = (f"{a['metric']}={a['value']}" if a.get("value") is not None else "기록 없음")
    print(f"── 심화 대상: {wo['week']}주차 / 총 {wo['total']}주 ──────────────────")
    print(f"  🎯 원 실습: {wo['goal']}  ({wo['arch']})")
    print(f"  📦 데이터: {wo['dataset_name']}  🔗 {wo['dataset_url']}")
    print(f"  🏁 통과 당시: {got}  ({a.get('date') or '?'})")
    print(f"  📄 원본 카드: {wo['source_card'] or '(없음)'}")
    print(f"  📓 노트북: {wo['notebook_hint']}")
    print(f"  {'⚠️ 이미 심화됨' if wo['already_deepened'] else '🟢 아직 심화 안 됨(대상)'}")
    print(f"  📋 심화 대기 큐: {wo['queue'] or '없음(모두 심화 완료)'}")
    print("\n  다음: `/deepen-week` 스킬이 이 주차의 카드·노트북을 읽어 A~E 심화 카드를 쓴다.")


def _print_queue() -> None:
    done = completed_weeks()
    have = deepdive_weeks()
    print(f"── 심화 큐 (완료 {len(done)}주 · 심화 완료 {len(have & set(done))}주) ──")
    if not done:
        print("  완료된 주차가 없습니다. 먼저 check_week.py로 한 주를 통과하세요.")
        return
    for w in done:
        mark = "✅ 심화됨" if w in have else "· 심화 대기"
        a = achieved(w)
        got = (f"{a['metric']}={a['value']}" if a.get("value") is not None else "")
        print(f"  {w:>2}주  {mark:<10} {got}")


def main() -> int:
    ap = argparse.ArgumentParser(description="AI랩 주차 심화(deep-dive) 큐 · 작업지시서")
    ap.add_argument("--list", action="store_true", help="완료 주차별 심화 여부 큐 표시")
    ap.add_argument("--week", type=int, help="특정 주차를 강제로 대상 지정")
    ap.add_argument("--json", action="store_true", help="작업지시서를 JSON으로 출력")
    args = ap.parse_args()

    if args.list:
        _print_queue()
        return 0

    wo = work_order(args.week)
    if wo is None:
        print("🟢 심화할 주차가 없습니다(완료 주차를 모두 심화했습니다).")
        _print_queue()
        return 0

    if args.json:
        print(json.dumps(wo, ensure_ascii=False, indent=2))
    else:
        _print_order(wo)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except BrokenPipeError:
        pass
