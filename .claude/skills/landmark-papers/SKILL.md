---
name: landmark-papers
description: 파트(주제)별로 '꼭 봐야 하는' 고인용 랜드마크 논문을 정리해 content/papers/에 Markdown 카드로 저장하고 홈페이지 번들을 재생성한다. 최신 논문(scrape-papers)과 짝을 이루는 impact 축. "랜드마크 논문", "꼭 봐야 하는 논문", "고인용 논문 정리", "필독 논문", "많이 인용된 논문" 요청에 트리거.
---

# 랜드마크(고인용) 논문 정리 절차

`scrape-papers`(최신 연구, recency)와 짝을 이루는 반대편 축이다. 이 스킬은 파트별로
**반드시 읽어야 할 고인용 논문(impact)**을 인용수로 랭킹해 정리한다.

결정론적 작업(후보수집·인용집계·랭킹·ID발급·중복판정)은 파이썬
(`pipelines/scrape_landmark_papers.py`)이 담당한다. LLM이 '이게 유명한 논문'이라고
기억으로 고르지 않는다 — **숫자(인용)로 고른다.** 이 스킬은 그 파이프라인을 올바른
순서로 호출하는 얇은 래퍼다.

## 순서

1. **누가 랭킹에 오르는지 미리보기(선택, 저장 안 함)**
   ```
   python pipelines/scrape_landmark_papers.py --dry-run
   # 특정 주제만: --topic Cardiology
   ```
2. **랭킹 → 상위 카드 저장** (편수·하한선·연도는 인자로 조정)
   ```
   python pipelines/scrape_landmark_papers.py --max 2 --min-citations 50
   # 최근 것만: --since-year 2010    설계 편향 끄기: --no-evidence-filter
   ```
   - 인용지표는 **NIH iCite**(무료, 키 불필요)에서 가져온다: 총 피인용수 + RCR(분야
     정규화 인용지표, 1.0=평균) + NIH 백분위. 인용수 우선, RCR로 tie-break.
   - 중복은 `scrape_papers`와 **공유하는** `state/seen_papers.json`(PMID)로 자동 판별한다.
     같은 논문이 '최신' 피드와 '랜드마크' 피드에 중복 저장되지 않는다.
   - id는 `state.next_id('paper')`로만 발급된다. 카드 파일명에 `_landmark_`가 붙는다.
3. **검증 + 색인**
   ```
   python pipelines/indexer.py --check   # 실패하면 멈추고 원인 보고
   python pipelines/indexer.py
   ```
4. **홈페이지 번들 재생성** (피드에 ⭐ 랜드마크 배지·인용순 정렬이 뜨게 하려면 필수)
   ```
   python pipelines/export_papers_web.py   # content/papers/**/*.md → docs/papers.js
   ```
5. **커밋** — 새 `content/papers/**` + `state/seen_papers.json`(+ 필요시 `id_counter.json`,
   `seen_topics.json`) + `docs/papers.js`를 **같은 커밋**에 포함해 push.
   신규 paper 타입이므로 self-verify 한계를 고려해 **PR로** 올리는 것을 원칙으로 한다.

## 카드는 무엇을 담나

스크랩 카드와 같은 골격 + 인용 메타(`landmark: true`, `citations`, `rcr`,
`nih_percentile`)와 `## Why must-read` 섹션(선정 근거 한 줄). 사실 메타 + 초록 +
인용지표까지만 담고 `confidence: medium`. 임상적 해석(Summary/Clinical Impact/My
Ideas)은 이후 `/gen-paper`로 사람·LLM이 검수해 채운다.

## 주제 늘리기 / 후보 편향

- 주제는 `scrape_papers.py`의 `TOPICS`를 **그대로 공유**한다(한 곳에서 관리).
- 기본적으로 RCT·메타분석·체계적 문헌고찰·가이드라인·리뷰로 후보 풀을 편향시킨다
  (`EVIDENCE_FILTER`). 끄려면 `--no-evidence-filter`.

## 자동화

- 매주는 `.github/workflows/landmark-papers.yml`(cron)이 위 2~5단계를 대신 돌린다.
  인용수는 매일 바뀌지 않으므로 최신 스크랩(매일)과 달리 **주간** 주기가 적절하다.

## 최신 vs 랜드마크

- 최신(`scrape-papers`): 최근 N일 새 논문, `sort=date`, `tags: [scraped, pubmed]`. 매일.
- 랜드마크(이 스킬): 파트별 고인용, 인용 랭킹, `tags: [landmark, highly-cited, pubmed]`. 주간.
