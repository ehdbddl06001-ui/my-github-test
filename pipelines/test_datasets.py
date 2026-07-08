"""
test_datasets.py — 오픈데이터 레지스트리(datasets.py)의 정합성 검사.

pytest 없이도 돈다(표준 라이브러리 assert만). 커밋 전 한 번 돌리면 커리큘럼과
데이터셋 목록이 어긋나는 실수(오타·삭제)를 조용히 지나치지 않는다.

  python pipelines/test_datasets.py     # 실패 시 exit code 1
"""
from __future__ import annotations

import sys

from datasets import (
    DATASETS, CURRICULUM, MODALITY_LABELS, TOTAL_WEEKS,
    topic_for_week, current_topic, weekly_topic, get_dataset,
)

VALID_ACCESS = {"open", "registration", "credentialed"}
REQUIRED_KEYS = {"key", "name", "modality", "task", "url", "license", "access"}


def test_dataset_shape() -> None:
    keys = [d["key"] for d in DATASETS]
    assert len(keys) == len(set(keys)), "데이터셋 key가 중복됨"
    for d in DATASETS:
        missing = REQUIRED_KEYS - set(d)
        assert not missing, f"{d.get('key')}: 필수 필드 누락 {missing}"
        assert d["access"] in VALID_ACCESS, f"{d['key']}: access 값 오류 {d['access']}"
        assert d["modality"] in MODALITY_LABELS, f"{d['key']}: 미등록 modality {d['modality']}"
        assert d["url"].startswith("http"), f"{d['key']}: url 형식 오류"


def test_curriculum_links() -> None:
    for i, item in enumerate(CURRICULUM):
        for k in ("goal", "dataset", "arch", "why"):
            assert item.get(k), f"CURRICULUM[{i}] 필드 누락: {k}"
        assert get_dataset(item["dataset"]) is not None, (
            f"CURRICULUM[{i}]의 dataset '{item['dataset']}'가 DATASETS에 없음"
        )


def test_sequential_weeks() -> None:
    # 1주차 = 커리큘럼 첫 항목(신호), 순서대로 진행
    w1 = topic_for_week(1)
    assert w1["week"] == 1
    assert w1["dataset_key"] == CURRICULUM[0]["dataset"], "1주차가 커리큘럼 첫 항목이 아님"
    # 마지막 주차 = 커리큘럼 마지막 항목
    wl = topic_for_week(TOTAL_WEEKS)
    assert wl["dataset_key"] == CURRICULUM[-1]["dataset"]
    # 범위를 벗어나면 1~TOTAL로 클램프
    assert topic_for_week(0)["week"] == 1
    assert topic_for_week(999)["week"] == TOTAL_WEEKS
    # weekly_topic()은 현재 주차 별칭
    assert weekly_topic()["week"] == current_topic()["week"]


def test_completion_gates() -> None:
    # 모든 주차에 완료 게이트(metric·target·deliverable)가 있어야 한다
    for i, item in enumerate(CURRICULUM, start=1):
        assert item.get("metric"), f"{i}주차: metric 누락"
        assert item.get("target") is not None, f"{i}주차: target 누락"
        assert isinstance(item["target"], (int, float)), f"{i}주차: target은 숫자여야 함"
        assert item.get("deliverable"), f"{i}주차: deliverable 누락"
        t = topic_for_week(i)
        assert t["metric"] == item["metric"] and t["target"] == item["target"]


def main() -> int:
    tests = [test_dataset_shape, test_curriculum_links, test_sequential_weeks,
             test_completion_gates]
    failed = 0
    for t in tests:
        try:
            t()
            print(f"[ OK ] {t.__name__}")
        except AssertionError as e:
            failed += 1
            print(f"[FAIL] {t.__name__}: {e}")
    print(f"\n{len(tests) - failed}/{len(tests)} 통과"
          f" · 데이터셋 {len(DATASETS)}종 · 커리큘럼 {len(CURRICULUM)}주")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
