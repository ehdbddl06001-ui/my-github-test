"""
test_landmark.py — 랜드마크(고인용) 논문 파이프라인 회귀 테스트.

배경(실측): 2026-07-13 ~ 08-10 의 주간 CI 5회가 모두 "success" 였는데 랜드마크 카드는
0편이었다. 로그를 보면 전 주제가 `인용 50회 이상 후보 없음` 을 찍었다 — iCite 인용지표가
한 건도 안 붙었는데, 값 없음을 `citations: 0` 으로 눌러쓰는 바람에 **장애가 '고인용
후보가 없다'는 정상 메시지로 위장**됐다. 여기 테스트는 그 위장을 막는다.

실행: python pipelines/test_landmark.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import scrape_landmark_papers as L

FAILS: list[str] = []


def check(name: str, cond: bool, detail: str = "") -> None:
    if cond:
        print(f"  ok  {name}")
    else:
        FAILS.append(f"{name}{' — ' + detail if detail else ''}")
        print(f"  FAIL {name} {detail}")


# ── 1. 인용수 필드 별칭 ────────────────────────────────────────────────────
def test_citation_field_aliases() -> None:
    """iCite 가 필드명을 바꿔도(별칭) 인용수를 읽어야 한다."""
    print("test_citation_field_aliases")
    for key in L.CITATION_KEYS:
        row = {"pmid": 1, key: 4321}
        check(f"{key} 로도 인용수를 읽는다", L._first(row, L.CITATION_KEYS) == 4321,
              f"got {L._first(row, L.CITATION_KEYS)}")


def test_missing_metric_is_none_not_zero() -> None:
    """값이 없으면 0 이 아니라 None — '인용 0회 논문'과 구분돼야 한다."""
    print("test_missing_metric_is_none_not_zero")
    row = {"pmid": 7, "year": 2010}          # 인용 관련 키가 통째로 없음
    check("인용 키가 없으면 None", L._first(row, L.CITATION_KEYS) is None)
    row_zero = {"pmid": 8, "citation_count": 0}
    check("진짜 0회는 0.0 으로 읽힌다", L._first(row_zero, L.CITATION_KEYS) == 0.0)


# ── 2. 장애가 '후보 없음'으로 위장되지 않는가 ──────────────────────────────
def test_coverage_detects_metric_outage() -> None:
    """지표를 하나도 못 읽으면 coverage()==0 이어야 한다(장애 신호)."""
    print("test_coverage_detects_metric_outage")
    broken = {"1": {"citations": None}, "2": {"citations": None}}
    healthy = {"1": {"citations": 1200}, "2": {"citations": None}}
    check("전부 None 이면 coverage 0", L.coverage(broken) == 0)
    check("하나라도 읽히면 coverage>0", L.coverage(healthy) == 1)


def test_rank_drops_unknown_metrics() -> None:
    """지표 없는(None) 논문은 하한선 비교에서 터지지 않고 조용히 제외돼야 한다."""
    print("test_rank_drops_unknown_metrics")
    recs = [{"pmid": "1", "title": "a"}, {"pmid": "2", "title": "b"}]
    metrics = {"1": {"citations": None, "rcr": None},
               "2": {"citations": 5000, "rcr": 12.0}}
    ranked = L.rank(recs, metrics, min_citations=1000)
    check("None 은 제외, 고인용만 남는다",
          [r["pmid"] for r in ranked] == ["2"], f"got {[r['pmid'] for r in ranked]}")


# ── 3. 50:50 균형 역산 ─────────────────────────────────────────────────────
def test_balance_deficit() -> None:
    """부족분은 '저장된 코퍼스 비율'에서 역산된다 — 주당 고정 편수가 아니다."""
    print("test_balance_deficit")
    orig = L.corpus_balance
    try:
        L.corpus_balance = lambda: (0, 220)      # 랜드마크 0, 최신 220
        check("0:220 에서 50% 목표면 220편 부족", L.balance_deficit(0.5) == 220,
              f"got {L.balance_deficit(0.5)}")
        L.corpus_balance = lambda: (100, 100)    # 이미 50:50
        check("이미 50:50 이면 부족 0", L.balance_deficit(0.5) == 0,
              f"got {L.balance_deficit(0.5)}")
        L.corpus_balance = lambda: (300, 100)    # 랜드마크 과잉
        check("과잉이면 음수가 아니라 0", L.balance_deficit(0.5) == 0,
              f"got {L.balance_deficit(0.5)}")
        L.corpus_balance = lambda: (0, 300)
        check("30% 목표는 약 129편", L.balance_deficit(0.3) == 129,
              f"got {L.balance_deficit(0.3)}")
    finally:
        L.corpus_balance = orig


# ── 4. 큰 풀을 쪼개지 않으면 URI 가 넘친다(414) ────────────────────────────
def test_pmid_requests_are_chunked() -> None:
    """pool 400 을 한 URL 에 붙이면 efetch 가 414 로 죽는다(2026-08-17 CI 실측)."""
    print("test_pmid_requests_are_chunked")
    pmids = [str(30000000 + i) for i in range(400)]
    batches = list(L._chunks(pmids))
    check("400개가 여러 배치로 쪼개진다", len(batches) > 1, f"got {len(batches)}")
    check("배치 크기가 상한을 넘지 않는다", all(len(b) <= L.CHUNK for b in batches))
    check("쪼개도 원본이 보존된다", [p for b in batches for p in b] == pmids)
    longest = max(len(",".join(b)) for b in batches)
    check("배치 하나의 쿼리 길이가 2000자 미만", longest < 2000, f"got {longest}")


# ── 5. 기본값이 '진짜 랜드마크' 급인가 ─────────────────────────────────────
def test_defaults_are_landmark_grade() -> None:
    """기본 하한선이 낮으면(50회) 평범한 논문이 '꼭 봐야 함' 배지를 달고 올라온다."""
    print("test_defaults_are_landmark_grade")
    src = Path(L.__file__).read_text(encoding="utf-8")
    check("기본 min-citations 가 1000 이상",
          'default=1000' in src.replace(" ", ""), "기본 하한선이 낮아졌다")
    check("기본 pool 이 400 이상",
          'default=400' in src.replace(" ", ""), "후보 풀이 작으면 고인용을 못 만난다")


def main() -> int:
    test_citation_field_aliases()
    test_missing_metric_is_none_not_zero()
    test_coverage_detects_metric_outage()
    test_rank_drops_unknown_metrics()
    test_balance_deficit()
    test_pmid_requests_are_chunked()
    test_defaults_are_landmark_grade()
    print()
    if FAILS:
        print(f"실패 {len(FAILS)}건:")
        for f in FAILS:
            print(f"  - {f}")
        return 1
    print("전부 통과")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
