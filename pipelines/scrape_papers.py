"""
scrape_papers.py — 매일 PubMed에서 관심 주제의 최신 논문을 긁어와 Markdown 카드로 저장한다.

MedKOS 원칙 준수:
  - 결정론적 작업(가져오기·파싱·ID발급·중복판정)은 이 파이썬이 담당한다. LLM이 숫자를 세지 않는다.
  - 원본은 content/papers/{연도}/*.md (Source of Truth). SQLite·docs 번들·Drive는 파생물.
  - 중복 방지는 컨테이너 메모리가 아니라 state/seen_papers.json (PMID 단위)로만 판정한다.
  - 스크랩 카드는 '사실 메타데이터 + 원문 초록'만 담는다(confidence: medium).
    임상적 해석(Summary/Clinical Impact/My Ideas)은 나중에 /gen-paper(사람·LLM 검수)로 채운다.

데이터 출처: NCBI PubMed E-utilities (esearch + efetch). 무료, API 키 불필요.
  https://www.ncbi.nlm.nih.gov/books/NBK25501/

사용:
  python pipelines/scrape_papers.py                 # 설정된 주제 전부, 최근 7일, 주제당 최대 3편
  python pipelines/scrape_papers.py --days 3 --max 2
  python pipelines/scrape_papers.py --topic Cardiology
  python pipelines/scrape_papers.py --dry-run       # 저장하지 않고 무엇을 가져올지만 출력
  python pipelines/scrape_papers.py --fixture t.xml --topic Cardiology  # 오프라인 테스트(efetch XML 주입)
"""
from __future__ import annotations

import argparse
import re
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import date
from pathlib import Path

# state.py 와 같은 폴더에서 실행되므로 직접 import 가능
from state import mark_paper_seen, next_id, paper_seen, record_topic

ROOT = Path(__file__).resolve().parent.parent
PAPERS_DIR = ROOT / "content" / "papers"
EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"

# ── 관심 주제 설정 ────────────────────────────────────────────────────────
# key = topic(카드의 topic/검색·연결 기준, 영문으로 통일), value = PubMed 검색어.
# 여기만 고치면 주제를 늘리거나 검색어를 바꿀 수 있다.
# 신뢰도 있는 저널로 한정하고 싶으면 검색어에 AND "Circulation"[Journal] 등을 덧붙인다.
# 우선순위 정밀도를 위해 OR/AND 는 괄호로 명시한다.
TOPICS: dict[str, str] = {
    # 심장학
    "Cardiology": '("heart failure"[Title/Abstract] OR "atrial fibrillation"[Title/Abstract])',
    # 감염내과
    "Infectious Disease": '("antimicrobial resistance"[Title/Abstract] OR "sepsis"[Title/Abstract])',
    # 신장내과
    "Nephrology": '("chronic kidney disease"[Title/Abstract] OR "SGLT2"[Title/Abstract])',
    # 혈액종양내과
    "Hematology-Oncology": '("immunotherapy"[Title/Abstract] OR "leukemia"[Title/Abstract] '
                           'OR "lymphoma"[Title/Abstract] OR "multiple myeloma"[Title/Abstract])',
    # 병리학
    "Pathology": '("digital pathology"[Title/Abstract] OR "molecular pathology"[Title/Abstract] '
                 'OR "histopathology"[Title/Abstract])',
    # 진단검사의학
    "Laboratory Medicine": '("laboratory medicine"[Title/Abstract] OR "clinical chemistry"[Title/Abstract] '
                           'OR "diagnostic accuracy"[Title/Abstract])',
    # 소아청소년과
    "Pediatrics": '("pediatric"[Title/Abstract] OR "children"[Title/Abstract]) '
                  'AND "randomized controlled trial"[Publication Type]',
    # 외과
    "Surgery": '("surgical"[Title/Abstract] OR "postoperative"[Title/Abstract]) '
               'AND ("outcome"[Title/Abstract] OR "complication"[Title/Abstract])',
}

UA = "MedKOS-paper-scraper/1.0 (https://github.com/ehdbddl06001-ui/my-github-test)"


# ── 네트워크 ──────────────────────────────────────────────────────────────
def _get(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read()


def esearch(query: str, days: int, retmax: int) -> list[str]:
    """검색어에 맞는 최근 논문 PMID 목록(최신순)."""
    params = {
        "db": "pubmed",
        "term": query,
        "retmax": str(retmax),
        "retmode": "json",
        "sort": "date",
        "datetype": "edat",       # Entrez 등재일 기준
        "reldate": str(days),     # 최근 N일
    }
    url = f"{EUTILS}/esearch.fcgi?" + urllib.parse.urlencode(params)
    import json
    data = json.loads(_get(url))
    return data.get("esearchresult", {}).get("idlist", [])


def efetch(pmids: list[str]) -> bytes:
    """PMID 목록의 상세 정보를 PubMed XML로 가져온다."""
    params = {"db": "pubmed", "id": ",".join(pmids), "retmode": "xml"}
    url = f"{EUTILS}/efetch.fcgi?" + urllib.parse.urlencode(params)
    return _get(url)


# ── 파싱 ──────────────────────────────────────────────────────────────────
def _text(el: ET.Element | None) -> str:
    if el is None:
        return ""
    return "".join(el.itertext()).strip()


def parse_articles(xml_bytes: bytes) -> list[dict]:
    """efetch PubMed XML → 논문 레코드 리스트."""
    root = ET.fromstring(xml_bytes)
    out: list[dict] = []
    for art in root.findall(".//PubmedArticle"):
        medline = art.find(".//MedlineCitation")
        if medline is None:
            continue
        pmid = _text(medline.find("PMID"))
        article = medline.find("Article")
        if article is None or not pmid:
            continue

        title = _text(article.find("ArticleTitle")).rstrip(".")
        journal = _text(article.find(".//Journal/Title"))

        # 초록(여러 AbstractText 섹션을 라벨과 함께 합침)
        abs_parts = []
        for at in article.findall(".//Abstract/AbstractText"):
            label = at.get("Label")
            body = _text(at)
            abs_parts.append(f"**{label}:** {body}" if label else body)
        abstract = "\n\n".join(p for p in abs_parts if p)

        # 저자 (최대 8명 + et al.)
        authors = []
        for a in article.findall(".//AuthorList/Author"):
            last, fore = _text(a.find("LastName")), _text(a.find("ForeName"))
            name = " ".join(p for p in [last, fore] if p) or _text(a.find("CollectiveName"))
            if name:
                authors.append(name)
        if len(authors) > 8:
            authors = authors[:8] + ["et al."]

        # DOI
        doi = ""
        for eid in article.findall(".//ELocationID"):
            if eid.get("EIdType") == "doi":
                doi = _text(eid)
                break

        # 게재일(연-월-일 가능한 만큼)
        pd = article.find(".//Journal/JournalIssue/PubDate")
        y, m, d = _text(pd.find("Year")) if pd is not None else "", "", ""
        if pd is not None:
            m, d = _text(pd.find("Month")), _text(pd.find("Day"))
        pubdate = "-".join(p for p in [y, _month(m), d.zfill(2) if d else ""] if p)

        out.append({
            "pmid": pmid,
            "title": title or "(제목 없음)",
            "journal": journal,
            "abstract": abstract,
            "authors": authors,
            "doi": doi,
            "pubdate": pubdate,
            "url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
        })
    return out


_MONTHS = {m: f"{i:02d}" for i, m in enumerate(
    ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], 1)}


def _month(m: str) -> str:
    """'Jul' 또는 '7' → '07' (실패 시 원문 유지)."""
    if not m:
        return ""
    if m in _MONTHS:
        return _MONTHS[m]
    return m.zfill(2) if m.isdigit() else m


# ── 카드 생성 ──────────────────────────────────────────────────────────────
def _slug(title: str) -> str:
    s = re.sub(r"[^A-Za-z0-9가-힣]+", "_", title).strip("_")
    return (s[:60] or "paper").lower()


def _yaml_list(items: list[str]) -> str:
    """YAML 인라인 리스트로 안전하게 직렬화(따옴표 처리)."""
    return "[" + ", ".join('"' + str(i).replace('"', "'") + '"' for i in items) + "]"


def render_card(rec: dict, topic: str, doc_id: str, today: str) -> str:
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
        "confidence: medium",
        f"date: {today}",
        "tags: [scraped, pubmed]",
        "related: []",
        "---",
    ]
    body = f"""
## Title
{rec['title']}

## Authors
{', '.join(rec['authors']) or '(정보 없음)'}

## Journal / DOI
{rec['journal'] or '(정보 없음)'}{' · DOI: ' + rec['doi'] if rec['doi'] else ''} · PMID: {rec['pmid']}
{rec['url']}

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
    path = out_dir / f"{today}_{doc_id}_{_slug(rec['title'])}.md"
    path.write_text(render_card(rec, topic, doc_id, today), encoding="utf-8")
    mark_paper_seen(rec["pmid"], today)
    record_topic("paper", f"{topic} - {rec['title'][:50]}", today)
    return path


# ── 오케스트레이션 ──────────────────────────────────────────────────────────
def run(topics: dict[str, str], days: int, per_topic: int,
        dry_run: bool, fixture: str | None) -> int:
    today = date.today().isoformat()
    saved, skipped = 0, 0

    for topic, query in topics.items():
        try:
            if fixture:
                recs = parse_articles(Path(fixture).read_bytes())
            else:
                pmids = esearch(query, days, per_topic)
                if not pmids:
                    print(f"[{topic}] 최근 {days}일 새 논문 없음")
                    continue
                recs = parse_articles(efetch(pmids))
                time.sleep(0.4)  # NCBI 예절(초당 3회 제한)
        except Exception as e:  # 네트워크·파싱 실패는 한 주제만 건너뛰고 계속
            print(f"[{topic}] 가져오기 실패: {e}", file=sys.stderr)
            continue

        for rec in recs:
            if paper_seen(rec["pmid"]):
                skipped += 1
                continue
            if dry_run:
                print(f"[{topic}] NEW  {rec['pmid']}  {rec['title'][:70]}")
                saved += 1
                continue
            path = save_card(rec, topic, today)
            print(f"[{topic}] 저장 {path.relative_to(ROOT)}")
            saved += 1

    verb = "가져올 새 논문" if dry_run else "저장"
    print(f"\n{verb} {saved}편, 중복 건너뜀 {skipped}편")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="PubMed 최신 논문 → Markdown 카드")
    ap.add_argument("--days", type=int, default=7, help="최근 N일(기본 7)")
    ap.add_argument("--max", type=int, default=3, dest="per_topic",
                    help="주제당 최대 편수(기본 3)")
    ap.add_argument("--topic", help="이 주제 하나만 (TOPICS의 key)")
    ap.add_argument("--dry-run", action="store_true", help="저장하지 않고 목록만")
    ap.add_argument("--fixture", help="efetch XML 파일을 주입해 오프라인 테스트")
    args = ap.parse_args()

    topics = TOPICS
    if args.topic:
        if args.topic not in TOPICS:
            print(f"알 수 없는 주제: {args.topic} (가능: {', '.join(TOPICS)})", file=sys.stderr)
            return 2
        topics = {args.topic: TOPICS[args.topic]}

    return run(topics, args.days, args.per_topic, args.dry_run, args.fixture)


if __name__ == "__main__":
    raise SystemExit(main())
