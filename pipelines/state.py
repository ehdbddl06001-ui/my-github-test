"""
state.py — 루틴 상태를 'content/ 파생물'로 다룬다(충돌 원천 제거).

과거엔 state/id_counter.json·seen_topics.json·seen_papers.json 을 **커밋**했다가,
여러 루틴이 각자 브랜치에서 같은 파일을 늘리며 merge 충돌(dirty PR)을 냈다. 이제는
CLAUDE.md 대원칙("content/**/*.md 가 유일한 Source of Truth")에 맞춰 이 세 가지를
**저장된 content 에서 그때그때 파생**한다 → 커밋하는 공유 상태가 없으니 두 브랜치가
같은 파일을 건드릴 일이 애초에 없다(= 충돌 불가).

  - next_id(type)     : content 안 해당 타입의 최대 일련번호 + 1 (역행·재사용 방지)
  - recent_topics(t)  : content frontmatter 의 topic/subtopic·date 에서 최근 주제 산출
  - paper_seen(pmid)  : content/papers frontmatter 의 pmid 스캔으로 중복 판정
  - record_topic()·mark_paper_seen() : 파생물화로 사실상 no-op(주제/PMID는 저장된
    카드가 SoT). 단, mark_paper_seen 은 '한 실행 안에서' 같은 PMID 재저장을 막도록
    프로세스 메모리 집합에만 등록한다(디스크/커밋 없음).

단조 발급 보장(임시 컨테이너 안전):
  next_id 는 content 최댓값을 '바닥'으로 삼고, 여기에 **gitignore 된** 컨테이너 로컬
  캐시(state/.id_cache.json)를 겹쳐, 파일을 아직 안 썼어도 같은 컨테이너 안에서는
  번호가 겹치지 않게 한다. 캐시는 커밋되지 않으므로 충돌을 만들지 않고, 새 컨테이너에선
  content 바닥값으로부터 정확히 이어진다.

여전히 파일 기반인 것: state/ailab_progress.json(주간 단일트랙 진도 포인터). 동시성이
낮아 충돌이 드물고, 혹시 갈라져도 머지 드라이버(pipelines/merge_state.py)가 union 한다.
"""
from __future__ import annotations

import json
import re
from datetime import date, datetime, timedelta
from pathlib import Path

# frontmatter 파서는 실행 방식(`python pipelines/x.py` vs `python -c "from pipelines..."`)에
# 따라 top-level 로도, 패키지로도 임포트될 수 있어 둘 다 대응한다.
try:  # `python pipelines/*.py` (sys.path[0] == pipelines/)
    from frontmatter import split_frontmatter
except ModuleNotFoundError:  # `python -c "from pipelines.state import ..."` (repo root)
    from pipelines.frontmatter import split_frontmatter

ROOT = Path(__file__).resolve().parent.parent
STATE_DIR = ROOT / "state"
CONTENT_DIR = ROOT / "content"
# 컨테이너 로컬 ID 캐시(커밋 금지 — .gitignore). content 바닥값 위에 겹쳐 단조 발급 보장.
ID_CACHE = STATE_DIR / ".id_cache.json"
# AI랩 실습 진도: 커리큘럼(datasets.py)을 1→12 '순서대로' 진행하는 현재 주차/완료기록.
# (달력이 아니라 사람의 진도) — 유일하게 커밋되는 상태이며 머지 드라이버가 보호한다.
AILAB_PROGRESS_FILE = STATE_DIR / "ailab_progress.json"

# 타입 → content 하위 디렉토리
TYPE_DIR = {
    "kmle": "kmle", "usmle": "usmle", "basic": "basic", "paper": "papers",
    "disease": "diseases", "drug": "drugs", "ailab": "ailab",
}


def _read(path: Path) -> dict:
    if path.exists() and path.read_text(encoding="utf-8").strip():
        return json.loads(path.read_text(encoding="utf-8"))
    return {}


def _write(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True),
        encoding="utf-8",
    )


def _type_dir(doc_type: str) -> Path:
    return CONTENT_DIR / TYPE_DIR.get(doc_type, doc_type)


def _max_content_id(doc_type: str, year: int) -> int:
    """content 안 해당 타입-연도의 최대 일련번호(없으면 0). id 는 frontmatter 가 진실."""
    prefix = f"{doc_type}-{year}-"
    pat = re.compile(rf'^id:\s*["\']?{re.escape(prefix)}0*(\d+)', re.MULTILINE)
    best = 0
    d = _type_dir(doc_type)
    if d.exists():
        for p in d.rglob("*.md"):
            m = pat.search(p.read_text(encoding="utf-8"))
            if m:
                best = max(best, int(m.group(1)))
    return best


def next_id(doc_type: str, year: int | None = None) -> str:
    """예: next_id('kmle') -> 'kmle-2026-0170'. content 최댓값+1 을 컨테이너 캐시로 단조 보장."""
    year = year or date.today().year
    key = f"{doc_type}-{year}"
    floor = _max_content_id(doc_type, year)
    cache = _read(ID_CACHE)
    n = max(floor, int(cache.get(key, 0))) + 1
    cache[key] = n
    _write(ID_CACHE, cache)
    return f"{doc_type}-{year}-{n:04d}"


def recent_topics(doc_type: str, days: int = 14) -> list[str]:
    """최근 `days`일 안에 이미 다룬 주제(content frontmatter 파생, 중복 생성 방지용)."""
    cutoff = datetime.now() - timedelta(days=days)
    out: set[str] = set()
    d = _type_dir(doc_type)
    if not d.exists():
        return []
    for p in d.rglob("*.md"):
        meta, _ = split_frontmatter(p.read_text(encoding="utf-8"))
        if str(meta.get("type", "")) != doc_type:
            continue
        try:
            if datetime.fromisoformat(str(meta.get("date"))) < cutoff:
                continue
        except (ValueError, TypeError):
            continue
        topic = meta.get("topic")
        if not topic:
            continue
        sub = meta.get("subtopic")
        out.add(f"{topic} - {sub}" if sub else str(topic))
    return sorted(out)


def record_topic(doc_type: str, topic: str, when: str | None = None) -> None:
    """no-op(호환용). 주제는 저장된 content frontmatter(topic/subtopic)가 SoT다."""
    return None


# ── 논문 스크랩 전용: PMID 단위 중복 방지 ────────────────────────────────
# 저장된 논문 카드(content/papers)의 frontmatter `pmid` 를 스캔해 판정한다(파생물).
# 한 실행 안에서 방금 저장한 PMID 재저장을 막기 위한 프로세스 메모리 집합만 추가로 둔다.
_RUNTIME_PMIDS: set[str] = set()
_content_pmids_cache: set[str] | None = None


def _content_pmids() -> set[str]:
    global _content_pmids_cache
    if _content_pmids_cache is None:
        s: set[str] = set()
        d = CONTENT_DIR / "papers"
        pat = re.compile(r'^pmid:\s*["\']?(\d+)', re.MULTILINE)
        if d.exists():
            for p in d.rglob("*.md"):
                m = pat.search(p.read_text(encoding="utf-8"))
                if m:
                    s.add(m.group(1))
        _content_pmids_cache = s
    return _content_pmids_cache


def paper_seen(pmid: str) -> bool:
    """이 PMID를 이미 카드로 저장했는가? (content 스캔 + 같은 실행 내 등록분)"""
    pmid = str(pmid)
    return pmid in _content_pmids() or pmid in _RUNTIME_PMIDS


def mark_paper_seen(pmid: str, when: str | None = None) -> None:
    """같은 실행 안에서 중복 저장을 막도록 프로세스 메모리에만 등록(디스크/커밋 없음)."""
    _RUNTIME_PMIDS.add(str(pmid))


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
    # 데모(비파괴): 다음 ID '미리보기'는 캐시를 건드리지 않도록 바닥값+1 로 보여준다.
    y = date.today().year
    print("최근 14일 KMLE 주제:", recent_topics("kmle"))
    print("다음 KMLE ID(미리보기):", f"kmle-{y}-{_max_content_id('kmle', y) + 1:04d}")
    print("AI랩 현재 주차:", ailab_week())
