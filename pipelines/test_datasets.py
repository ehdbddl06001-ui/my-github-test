"""
test_datasets.py — 오픈데이터 레지스트리(datasets.py)의 정합성 검사.

pytest 없이도 돈다(표준 라이브러리 assert만). 커밋 전 한 번 돌리면 커리큘럼과
데이터셋 목록이 어긋나는 실수(오타·삭제)를 조용히 지나치지 않는다.

  python pipelines/test_datasets.py     # 실패 시 exit code 1
"""
from __future__ import annotations

import sys
from datetime import date

from datasets import DATASETS, CURRICULUM, MODALITY_LABELS, weekly_topic, get_dataset

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


def test_weekly_topic_deterministic() -> None:
    d = date(2026, 7, 8)  # ISO week 28
    a, b = weekly_topic(d), weekly_topic(d)
    assert a == b, "weekly_topic이 같은 날짜에 다른 결과를 냄(비결정적)"
    assert a["week"] == 28
    # 커리큘럼 길이로 순환하므로 항상 유효한 항목을 가리킨다
    assert a["dataset_key"] == CURRICULUM[28 % len(CURRICULUM)]["dataset"]
    assert get_dataset(a["dataset_key"]) is not None


def main() -> int:
    tests = [test_dataset_shape, test_curriculum_links, test_weekly_topic_deterministic]
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
