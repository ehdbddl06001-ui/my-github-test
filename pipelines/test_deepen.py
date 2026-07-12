"""
test_deepen.py — 심화 큐(deepen.py)의 정합성 검사. 표준 라이브러리 assert만 사용.

  python pipelines/test_deepen.py     # 실패 시 exit code 1

deepen.py는 상태를 쓰지 않는 읽기 전용이므로, 여기서는 큐 규칙의 불변식만 확인한다:
  - 심화 큐 ⊆ 완료 주차 (완료하지 않은 주차는 심화 대상이 될 수 없다)
  - 이미 deepdive 카드가 있는 주차는 큐에 없다
  - work_order()는 큐의 가장 이른 주차를 집는다(강제 지정 시 그 주차)
  - work_order()의 achieved/source_card가 실제 state·content와 일치한다
"""
from __future__ import annotations

import sys

from deepen import (
    completed_weeks, deepdive_weeks, pending_deepdives, work_order,
    card_for_week, achieved,
)
from state import ailab_progress


def test_queue_subset_of_completed() -> None:
    done = set(completed_weeks())
    pending = pending_deepdives()
    assert set(pending) <= done, "심화 큐에 완료되지 않은 주차가 들어 있음"
    # 큐는 오름차순
    assert pending == sorted(pending), "심화 큐가 오름차순이 아님"


def test_deepened_weeks_excluded() -> None:
    have = deepdive_weeks()
    assert not (set(pending_deepdives()) & have), "이미 심화한 주차가 큐에 남아 있음"


def test_work_order_picks_earliest() -> None:
    pending = pending_deepdives()
    wo = work_order()
    if not pending:
        assert wo is None, "심화할 게 없는데 작업지시서가 나옴"
        return
    assert wo is not None and wo["week"] == pending[0], "가장 이른 대기 주차를 집지 않음"
    assert wo["already_deepened"] is False, "대상 주차가 이미 심화됨으로 표시됨"


def test_forced_week_and_fields() -> None:
    done = completed_weeks()
    if not done:
        return  # 완료 주차가 없으면 검증 생략
    w = done[0]
    wo = work_order(w)
    assert wo is not None and wo["week"] == w
    # achieved가 state와 일치
    entry = ailab_progress()["done"][str(w)]
    assert wo["achieved"]["value"] == entry.get("value")
    assert wo["achieved"]["metric"] == entry.get("metric")
    # source_card는 실제 카드 조회 결과와 일치(있으면 문자열, 없으면 None)
    assert wo["source_card"] == card_for_week(w)


def main() -> int:
    tests = [
        test_queue_subset_of_completed,
        test_deepened_weeks_excluded,
        test_work_order_picks_earliest,
        test_forced_week_and_fields,
    ]
    failed = 0
    for t in tests:
        try:
            t()
            print(f"[ OK ] {t.__name__}")
        except AssertionError as e:
            failed += 1
            print(f"[FAIL] {t.__name__}: {e}")
    print(f"\n{len(tests) - failed}/{len(tests)} 통과 · 완료 {completed_weeks()} · "
          f"심화됨 {sorted(deepdive_weeks())} · 대기 {pending_deepdives()}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
