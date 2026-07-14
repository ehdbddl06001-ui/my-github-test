"""
merge_state.py — state/*.json 전용 git 머지 드라이버(결정론 합집합/최댓값).

왜 필요한가:
  state/id_counter.json·seen_topics.json·seen_papers.json·ailab_progress.json 은
  여러 루틴이 각자 브랜치에서 '추가'만 하는 결정론 레지스트리다. 두 브랜치가 같은
  파일의 다른 자리를 늘리면 git의 라인 단위 3-way 병합이 충돌(conflict)을 내지만,
  실제 정답은 항상 하나뿐이다 = 양쪽을 합친다(카운터는 최댓값, 레지스트리는 합집합).
  이 드라이버가 그 결정론 병합을 자동으로 수행해 '가짜 충돌'을 없앤다.

git 연결(.gitattributes + git config):
  state/*.json merge=medkos-state
  merge.medkos-state.driver = python3 pipelines/merge_state.py %O %A %B %P
  (%O=공통조상, %A=ours=출력대상, %B=theirs, %P=파일경로)
  → 병합 결과를 %A 에 쓰고 exit 0 이면 성공. .claude SessionStart 훅이 매 컨테이너에서
    이 driver 를 git config 에 등록한다(임시 컨테이너 안전).

병합 규칙(재귀):
  - dict  : 키 합집합, 겹치면 값끼리 재귀 병합
  - 숫자  : 최댓값 (카운터/주차/지표값)
  - 문자열: 최댓값(lexicographic). ISO 날짜는 이게 '가장 최근'과 같다.
  - list  : 순서 보존 합집합(중복 제거)
값은 이 4개 파일에서 leaf 가 (날짜문자열·정수·실수·짧은 라벨)뿐이라 위 규칙이 안전하다.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path


def merge(a, b):
    """ours(a) 와 theirs(b) 를 결정론적으로 합친다. 조상은 볼 필요 없다(추가-전용)."""
    if a is None:
        return b
    if b is None:
        return a
    if isinstance(a, dict) and isinstance(b, dict):
        out = dict(a)
        for k, vb in b.items():
            out[k] = merge(a[k], vb) if k in a else vb
        return out
    if isinstance(a, list) and isinstance(b, list):
        out = list(a)
        for x in b:
            if x not in out:
                out.append(x)
        return out
    if isinstance(a, bool) or isinstance(b, bool):
        return a or b
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return max(a, b)
    # 문자열(주로 ISO 날짜) 및 그 외: lexicographic 최댓값 = 최신 날짜
    return max(a, b, key=str)


def _load(path: str) -> object:
    p = Path(path)
    if not p.exists() or not p.read_text(encoding="utf-8").strip():
        return {}
    return json.loads(p.read_text(encoding="utf-8"))


def main(argv: list[str]) -> int:
    # argv: [O, A, B, P]  — A 가 출력 대상
    if len(argv) < 3:
        print("usage: merge_state.py %O %A %B [%P]", file=sys.stderr)
        return 2
    _base, ours, theirs = argv[0], argv[1], argv[2]
    merged = merge(_load(ours), _load(theirs))
    Path(ours).write_text(
        json.dumps(merged, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return 0


def _selftest() -> int:
    """PR #28 의 실제 충돌을 재현해 union 이 나오는지 확인."""
    main_side = {"paper-2026": 80, "usmle-2026": 42, "kmle-2026": 169}
    pr_side = {"paper-2026": 73, "usmle-2026": 48, "kmle-2026": 169}
    got = merge(main_side, pr_side)
    assert got == {"paper-2026": 80, "usmle-2026": 48, "kmle-2026": 169}, got

    m_topics = {"usmle": {"A": "2026-07-13"}, "paper": {"P1": "2026-07-13"}}
    p_topics = {"usmle": {"B": "2026-07-13"}, "paper": {"P1": "2026-07-10"}}
    got2 = merge(m_topics, p_topics)
    assert got2 == {
        "usmle": {"A": "2026-07-13", "B": "2026-07-13"},
        "paper": {"P1": "2026-07-13"},  # 겹치면 최신 날짜
    }, got2

    ai_a = {"week": 2, "done": {"1": {"value": 0.83}}}
    ai_b = {"week": 3, "done": {"1": {"value": 0.80}, "2": {"value": 0.9}}}
    got3 = merge(ai_a, ai_b)
    assert got3["week"] == 3 and got3["done"]["1"]["value"] == 0.83, got3
    print("merge_state selftest OK")
    return 0


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "--selftest":
        raise SystemExit(_selftest())
    raise SystemExit(main(sys.argv[1:]))
