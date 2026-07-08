"""
state.py — 루틴이 임시 컨테이너에서 돌아도 일관성을 유지하기 위한 상태 관리.

컨테이너는 매 실행마다 새로 뜨므로, 다음 상태는 반드시 repo 안 파일에서 읽어야 한다.
  - state/id_counter.json : 타입별 마지막 일련번호  → ID 충돌/역행 방지
  - state/seen_topics.json: 타입별 {주제: 마지막 날짜}  → N일 중복 방지(lookback)

루틴 흐름:
  1) 실행 시작 시 recent_topics() 로 최근 다룬 주제를 제외 힌트로 사용
  2) 콘텐츠 생성마다 next_id() 로 ID 발급
  3) 생성 후 record_topic() 로 기록
  4) 상태 파일을 같은 커밋에 포함시켜 push
"""
from __future__ import annotations

import json
from datetime import date, datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATE_DIR = ROOT / "state"
ID_FILE = STATE_DIR / "id_counter.json"
TOPIC_FILE = STATE_DIR / "seen_topics.json"
# 논문 스크랩 중복 방지: 이미 카드로 저장한 PubMed PMID → 저장일
PAPER_FILE = STATE_DIR / "seen_papers.json"
# AI랩 실습 진도: 커리큘럼(datasets.py)을 1→12 '순서대로' 진행하기 위한 현재 주차/완료기록.
# 달력(ISO 주차)이 아니라 사람의 진도를 따른다 → 임시 컨테이너에서 돌아도 순서가 유지된다.
AILAB_PROGRESS_FILE = STATE_DIR / "ailab_progress.json"


def _read(path: Path) -> dict:
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {}


def _write(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True),
        encoding="utf-8",
    )


def next_id(doc_type: str, year: int | None = None) -> str:
    """예: next_id('kmle') -> 'kmle-2026-0143' (카운터를 즉시 증가·저장)."""
    year = year or date.today().year
    counters = _read(ID_FILE)
    key = f"{doc_type}-{year}"
    n = counters.get(key, 0) + 1
    counters[key] = n
    _write(ID_FILE, counters)
    return f"{doc_type}-{year}-{n:04d}"


def recent_topics(doc_type: str, days: int = 14) -> list[str]:
    """최근 `days`일 안에 이미 다룬 주제 목록(중복 생성 방지용)."""
    seen = _read(TOPIC_FILE).get(doc_type, {})
    cutoff = datetime.now() - timedelta(days=days)
    out = []
    for topic, d in seen.items():
        try:
            if datetime.fromisoformat(str(d)) >= cutoff:
                out.append(topic)
        except ValueError:
            continue
    return sorted(out)


def record_topic(doc_type: str, topic: str, when: str | None = None) -> None:
    when = when or date.today().isoformat()
    seen = _read(TOPIC_FILE)
    seen.setdefault(doc_type, {})[topic] = when
    _write(TOPIC_FILE, seen)


# ── 논문 스크랩 전용: PMID 단위 중복 방지 ────────────────────────────────
# 논문은 '주제'가 아니라 개별 문헌(PMID)이 단위라 seen_topics 와 분리해 관리한다.
# 임시 컨테이너에서 매일 돌아도, 이미 저장한 PMID는 state 파일로만 판별한다.

def paper_seen(pmid: str) -> bool:
    """이 PMID를 이미 카드로 저장했는가?"""
    return str(pmid) in _read(PAPER_FILE)


def mark_paper_seen(pmid: str, when: str | None = None) -> None:
    """PMID를 저장 완료로 기록(같은 커밋에 포함시켜 push)."""
    when = when or date.today().isoformat()
    seen = _read(PAPER_FILE)
    seen[str(pmid)] = when
    _write(PAPER_FILE, seen)


# ── AI랩 실습 진도(순차 1→12) ─────────────────────────────────────────────
# datasets.py 의 CURRICULUM 을 달력이 아니라 '완료할 때마다 한 칸' 진행한다.

def ailab_week() -> int:
    """현재 진행 중인 실습 주차(1-based). 기록이 없으면 1주차부터."""
    return int(_read(AILAB_PROGRESS_FILE).get("week", 1))


def set_ailab_week(n: int) -> None:
    """현재 주차를 n으로 지정(건너뛰기/되돌리기)."""
    data = _read(AILAB_PROGRESS_FILE)
    data["week"] = int(n)
    _write(AILAB_PROGRESS_FILE, data)


def mark_ailab_done(
    week: int, when: str | None = None,
    metric: str | None = None, value: float | None = None,
) -> None:
    """해당 주차를 완료로 기록(달성 지표·값도 함께 남길 수 있다)."""
    when = when or date.today().isoformat()
    data = _read(AILAB_PROGRESS_FILE)
    entry: dict = {"date": when}
    if metric:
        entry["metric"] = metric
    if value is not None:
        entry["value"] = value
    data.setdefault("done", {})[str(week)] = entry
    _write(AILAB_PROGRESS_FILE, data)


def advance_ailab_week(
    total: int, metric: str | None = None, value: float | None = None,
) -> int:
    """현재 주차를 완료 처리하고 다음(최대 total)으로 이동. 새 현재 주차를 반환."""
    cur = ailab_week()
    mark_ailab_done(cur, metric=metric, value=value)
    nxt = min(cur + 1, int(total))
    set_ailab_week(nxt)
    return nxt


def ailab_progress() -> dict:
    """{'week': 현재주차, 'done': {주차: 완료일}} 형태로 진도 전체를 반환."""
    d = _read(AILAB_PROGRESS_FILE)
    return {"week": int(d.get("week", 1)), "done": d.get("done", {}) or {}}


if __name__ == "__main__":
    # 데모: 오늘 KMLE에서 피해야 할 주제와 다음 ID 확인
    print("최근 14일 KMLE 주제:", recent_topics("kmle"))
    print("다음 KMLE ID(미리보기 아님, 실제 증가):", next_id("kmle"))
    print("AI랩 현재 주차:", ailab_week())
