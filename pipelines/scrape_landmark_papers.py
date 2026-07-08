"""
scrape_landmark_papers.py — 주제(파트)별 '꼭 봐야 하는' 고인용 랜드마크 논문을 정리한다.

`scrape_papers.py`(최신순)와 짝을 이루는 반대편 축이다.
  - scrape_papers  : 최근 N일의 '최신 연구'(recency). sort=date.
  - scrape_landmark: 파트별 '반드시 읽어야 할 고인용 논문'(impact). 인용수로 랭킹.

MedKOS 원칙 준수:
  - 결정론적 작업(후보수집·인용집계·랭킹·ID발급·중복판정)은 이 파이썬이 담당한다.
    LLM이 '이게 유명한 논문' 이라고 기억으로 고르지 않는다 — 숫자(인용)로 고른다.
  - 원본은 content/papers/{연도}/*.md (Source of Truth). SQLite·docs 번들·Drive는 파생물.
  - 중복 방지는 scrape_papers 와 **같은** state/seen_papers.json(PMID)을 공유한다.
    → 같은 논문이 '최신' 피드와 '랜드마크' 피드에 중복 저장되지 않는다.
  - 카드는 '사실 메타데이터 + 초록 + 인용지표'만 담고 confidence: medium.
    임상적 해석(Summary/Clinical Impact/My Ideas)은 나중에 /gen-paper로 채운다.

랭킹 데이터 출처: NIH iCite API (무료, API 키 불필요).
  - citation_count         : 총 피인용수
  - relative_citation_ratio: RCR — 같은 분야·같은 시기 대비 정규화 인용지표(1.0=평균).
                             분야가 다른 논문을 공정하게 비교할 수 있어 랭킹 tie-break에 씀.
  - nih_percentile         : NIH 기준 상위 백분위
  https://icite.od.nih.gov/api

후보 논문 출처: NCBI PubMed E-utilities(esearch/efetch) — scrape_papers 와 동일.

사용:
  python pipelines/scrape_landmark_papers.py                       # 전체 주제, 주제당 2편
  python pipelines/scrape_landmark_papers.py --topic Cardiology --max 3
  python pipelines/scrape_landmark_papers.py --min-citations 100 --since-year 2010
  python pipelines/scrape_landmark_papers.py --dry-run             # 저장 없이 랭킹만 출력
  python pipelines/scrape_landmark_papers.py \
      --fixture pipelines/fixtures/pubmed_sample.xml \
      --icite-fixture pipelines/fixtures/icite_sample.json --topic Cardiology  # 오프라인 테스트
"""
from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.parse
from datetime import date
from pathlib import Path

# scrape_papers 와 같은 폴더 → 파싱·직렬화·네트워크·상태 헬퍼를 그대로 재사용한다.
from scrape_papers import (
    EUTILS,
    PAPERS_DIR,
    ROOT,
    TOPICS,
    _get,
    _slug,
    _yaml_list,
    efetch,
    parse_articles,
)
from state import mark_paper_seen, next_id, paper_seen, record_topic

ICITE = "https://icite.od.nih.gov/api/pubs"

# 랜드마크는 '개별 관찰연구'보다 근거수준이 높은 설계에서 나온다. 후보 풀을 이런
# 설계로 편향시켜 신호를 높인다(--no-evidence-filter 로 끌 수 있음).
EVIDENCE_FILTER = (
    'AND ("Randomized Controlled Trial"[Publication Type] '
    'OR "Meta-Analysis"[Publication Type] '
    'OR "Systematic Review"[Publication Type] '
    'OR "Guideline"[Publication Type] '
    'OR "Practice Guideline"[Publication Type] '
    'OR "Review"[Publication Type])'
)


# ── 후보 풀 수집(관련도순, 최신순 아님) ────────────────────────────────────
def search_pool(query: str, pool: int, since_year: int | None) -> list[str]:
    """주제 검색어에 맞는 후보 PMID 풀을 관련도순으로 모은다(랭킹은 인용으로 다시 함)."""
    if since_year:
        query = f'({query}) AND ("{since_year}"[Date - Publication] : "3000"[Date - Publication])'
    params = {
        "db": "pubmed",
        "term": query,
        "retmax": str(pool),
        "retmode": "json",
        "sort": "relevance",   # 최신이 아니라 '관련도 높은 큰 풀'을 뽑고, 인용으로 랭킹한다
    }
    url = f"{EUTILS}/esearch.fcgi?" + urllib.parse.urlencode(params)
    data = json.loads(_get(url))
    return data.get("esearchresult", {}).get("idlist", [])


# ── iCite 인용지표 ─────────────────────────────────────────────────────────
def _num(v):
    """iCite가 null/문자열로 줄 수 있는 값을 float 또는 None 으로."""
    if v in (None, "", "NA"):
        return None
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def icite(pmids: list[str], fixture: str | None = None) -> dict[str, dict]:
    """PMID → {citations, rcr, nih_percentile, year}. 200개씩 배치로 조회."""
    if fixture:
        raw = json.loads(Path(fixture).read_text(encoding="utf-8")).get("data", [])
        rows = raw
    else:
        rows = []
        for i in range(0, len(pmids), 200):
            batch = pmids[i:i + 200]
            url = f"{ICITE}?" + urllib.parse.urlencode({"pmids": ",".join(batch), "legacy": "false"})
            rows.extend(json.loads(_get(url)).get("data", []))
            time.sleep(0.3)  # API 예절
    out: dict[str, dict] = {}
    for r in rows:
        pmid = str(r.get("pmid", ""))
        if not pmid:
            continue
        cc = _num(r.get("citation_count"))
        out[pmid] = {
            "citations": int(cc) if cc is not None else 0,
            "rcr": _num(r.get("relative_citation_ratio")),
            "nih_percentile": _num(r.get("nih_percentile")),
            "year": r.get("year"),
        }
    return out


# ── 랭킹 ───────────────────────────────────────────────────────────────────
def rank(recs: list[dict], metrics: dict[str, dict], min_citations: int) -> list[dict]:
    """각 논문에 인용지표를 붙이고, 인용수 → RCR 순으로 정렬한 뒤 하한선으로 거른다."""
    scored = []
    for rec in recs:
        m = metrics.get(rec["pmid"])
        if not m or m["citations"] < min_citations:
            continue
        rec = {**rec, **m}
        scored.append(rec)
    scored.sort(key=lambda r: (r["citations"], r["rcr"] or 0.0), reverse=True)
    return scored


# ── 카드 생성 ──────────────────────────────────────────────────────────────
def render_card(rec: dict, topic: str, doc_id: str, today: str) -> str:
    rcr = f"{rec['rcr']:.2f}" if rec.get("rcr") is not None else ""
    pct = f"{rec['nih_percentile']:.1f}" if rec.get("nih_percentile") is not None else ""
    fm = [
        "---",
        f"id: {doc_id}",
        "type: paper",
        f"topic: {topic}",
        f'source: "PubMed / {rec["journal"]}"' if rec["journal"] else 'source: "PubMed"',
        f'journal: "{rec["journal"]}"',
        f'pmid: "{rec["pmid"]}"',
        f'doi: "{rec["doi"]}"' if rec["doi"] else 'doi: ""',
        f"authors: {_yaml_list(rec['authors'])}",
        f'url: "{rec["url"]}"',
        f'pubdate: "{rec["pubdate"]}"' if rec["pubdate"] else 'pubdate: ""',
        "landmark: true",
        f"citations: {rec['citations']}",
    ]
    if rcr:
        fm.append(f"rcr: {rcr}")
    if pct:
        fm.append(f"nih_percentile: {pct}")
    fm += [
        "confidence: medium",
        f"date: {today}",
        "tags: [landmark, highly-cited, pubmed]",
        "related: []",
        "---",
    ]
    # 인용지표 한 줄 요약(사람이 왜 '꼭 봐야 하는지' 근거를 바로 보게)
    cite_bits = [f"피인용 {rec['citations']}회"]
    if rcr:
        cite_bits.append(f"RCR {rcr} (분야평균=1.0)")
    if pct:
        cite_bits.append(f"NIH 상위 백분위 {pct}")
    cite_line = " · ".join(cite_bits)

    body = f"""
## Title
{rec['title']}

## Authors
{', '.join(rec['authors']) or '(정보 없음)'}

## Journal / DOI
{rec['journal'] or '(정보 없음)'}{' · DOI: ' + rec['doi'] if rec['doi'] else ''} · PMID: {rec['pmid']}
{rec['url']}

## Why must-read
파트({topic}) 내 고인용 랜드마크로 선정. {cite_line}.
(인용지표 출처: NIH iCite. 인용수는 시간에 따라 변하므로 재수집 시 갱신될 수 있음.)

## Abstract
{rec['abstract'] or '(PubMed에 초록 없음)'}

## Summary
<!-- TODO: /gen-paper 로 핵심을 자기 언어로 요약 -->

## Clinical Impact
<!-- TODO: 이 연구가 왜 practice-changing인가 -->

## Guideline 변화
<!-- TODO: 이전 가이드라인과 무엇이 달라졌나 -->

## My Ideas
<!-- TODO: 후속 아이디어/연구 메모 -->
"""
    return "\n".join(fm) + "\n" + body


def save_card(rec: dict, topic: str, today: str) -> Path:
    doc_id = next_id("paper")
    year = today[:4]
    out_dir = PAPERS_DIR / year
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"{today}_{doc_id}_landmark_{_slug(rec['title'])}.md"
    path.write_text(render_card(rec, topic, doc_id, today), encoding="utf-8")
    mark_paper_seen(rec["pmid"], today)
    record_topic("paper", f"[landmark] {topic} - {rec['title'][:50]}", today)
    return path


# ── 오케스트레이션 ──────────────────────────────────────────────────────────
def run(topics: dict[str, str], pool: int, per_topic: int, min_citations: int,
        since_year: int | None, evidence_filter: bool, dry_run: bool,
        fixture: str | None, icite_fixture: str | None) -> int:
    today = date.today().isoformat()
    saved, skipped = 0, 0

    for topic, query in topics.items():
        if evidence_filter and not fixture:
            query = f"{query} {EVIDENCE_FILTER}"
        try:
            if fixture:
                recs = parse_articles(Path(fixture).read_bytes())
            else:
                pmids = search_pool(query, pool, since_year)
                if not pmids:
                    print(f"[{topic}] 후보 논문 없음")
                    continue
                recs = parse_articles(efetch(pmids))
                time.sleep(0.4)  # NCBI 예절
            metrics = icite([r["pmid"] for r in recs], icite_fixture)
        except Exception as e:  # 네트워크·파싱 실패는 한 주제만 건너뛰고 계속
            print(f"[{topic}] 가져오기 실패: {e}", file=sys.stderr)
            continue

        ranked = rank(recs, metrics, min_citations)
        if not ranked:
            print(f"[{topic}] 인용 {min_citations}회 이상 후보 없음")
            continue

        taken = 0
        for rec in ranked:
            if taken >= per_topic:
                break
            if paper_seen(rec["pmid"]):
                skipped += 1
                continue
            if dry_run:
                rcr = f" RCR {rec['rcr']:.2f}" if rec.get("rcr") is not None else ""
                print(f"[{topic}] TOP  인용 {rec['citations']:>5}{rcr}  {rec['pmid']}  {rec['title'][:64]}")
                saved += 1
                taken += 1
                continue
            path = save_card(rec, topic, today)
            print(f"[{topic}] 저장 (인용 {rec['citations']}) {path.relative_to(ROOT)}")
            saved += 1
            taken += 1

    verb = "선정" if dry_run else "저장"
    print(f"\n랜드마크 {verb} {saved}편, 중복 건너뜀 {skipped}편")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="파트별 고인용 랜드마크 논문 → Markdown 카드")
    ap.add_argument("--pool", type=int, default=80,
                    help="주제당 후보 풀 크기(관련도순 esearch retmax, 기본 80)")
    ap.add_argument("--max", type=int, default=2, dest="per_topic",
                    help="주제당 저장할 상위 편수(기본 2)")
    ap.add_argument("--min-citations", type=int, default=50,
                    help="이 인용수 미만은 제외(기본 50)")
    ap.add_argument("--since-year", type=int,
                    help="이 연도 이후 게재만 후보로(생략 시 제한 없음)")
    ap.add_argument("--no-evidence-filter", action="store_true",
                    help="RCT·메타분석·가이드라인·리뷰 편향 필터를 끈다")
    ap.add_argument("--topic", help="이 주제 하나만 (TOPICS의 key)")
    ap.add_argument("--dry-run", action="store_true", help="저장하지 않고 랭킹만")
    ap.add_argument("--fixture", help="efetch XML 파일을 주입해 오프라인 테스트")
    ap.add_argument("--icite-fixture", help="iCite JSON 파일을 주입해 오프라인 테스트")
    args = ap.parse_args()

    topics = TOPICS
    if args.topic:
        if args.topic not in TOPICS:
            print(f"알 수 없는 주제: {args.topic} (가능: {', '.join(TOPICS)})", file=sys.stderr)
            return 2
        topics = {args.topic: TOPICS[args.topic]}

    return run(
        topics, args.pool, args.per_topic, args.min_citations, args.since_year,
        not args.no_evidence_filter, args.dry_run, args.fixture, args.icite_fixture,
    )


if __name__ == "__main__":
    raise SystemExit(main())
