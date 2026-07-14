"""
test_state.py — 상태를 content 에서 파생하는 로직 회귀 테스트(pytest 없이 assert).

핵심: 커밋되는 공유 상태 없이도 (1) ID가 content 최댓값에서 단조 발급되고,
(2) 최근 주제가 frontmatter 에서 나오며, (3) PMID 중복이 저장 카드로 판정되는지.
"""
from __future__ import annotations

import sys
import tempfile
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import state  # noqa: E402


def test_next_id_derives_from_content_and_is_monotonic() -> None:
    y = date.today().year
    # 캐시를 임시 파일로 격리(컨테이너 실제 캐시 오염 방지 + 결정성)
    tmp = Path(tempfile.mkdtemp()) / ".id_cache.json"
    orig = state.ID_CACHE
    state.ID_CACHE = tmp
    try:
        for t in ("kmle", "usmle", "paper"):
            floor = state._max_content_id(t, y)
            a = state.next_id(t)
            b = state.next_id(t)
            na, nb = int(a.rsplit("-", 1)[1]), int(b.rsplit("-", 1)[1])
            assert a.startswith(f"{t}-{y}-"), a
            assert na == floor + 1, (t, na, floor)          # content 바닥값+1
            assert nb == floor + 2, (t, nb, floor)          # 같은 프로세스 내 단조 증가
    finally:
        state.ID_CACHE = orig


def test_max_content_id_matches_actual_files() -> None:
    y = date.today().year
    # content 에 실제 usmle-<y>-0048 등이 있으므로 최댓값은 0 보다 커야 한다.
    assert state._max_content_id("usmle", y) >= 1
    assert state._max_content_id("kmle", y) >= 1


def test_recent_topics_from_frontmatter() -> None:
    topics = state.recent_topics("usmle", 3650)  # 넉넉한 창(10년)
    assert isinstance(topics, list)
    # "topic - subtopic" 형태로 합쳐 나오는지(적어도 하나는 ' - ' 포함)
    assert any(" - " in t for t in topics), topics


def test_paper_seen_and_runtime_mark() -> None:
    # 존재하지 않을 PMID 는 미저장, mark 후엔 같은 실행 내에서 저장된 것으로 취급
    fake = "999999999"
    assert state.paper_seen(fake) is False
    state.mark_paper_seen(fake)
    assert state.paper_seen(fake) is True


def test_record_topic_is_noop() -> None:
    assert state.record_topic("kmle", "X - Y") is None


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    passed = 0
    for fn in fns:
        fn()
        passed += 1
        print(f"[ OK ] {fn.__name__}")
    print(f"\n{passed}/{len(fns)} 통과")
