---
name: scrape-papers
description: PubMed에서 관심 주제의 최신 논문을 긁어와 content/papers/에 Markdown 카드로 저장하고 홈페이지 번들을 재생성한다. "논문 스크랩", "오늘 논문 긁어와", "최신 논문 수집" 요청에 트리거.
---

# 논문 스크랩 실행 절차

결정론적 수집은 파이썬(`pipelines/scrape_papers.py`)이 담당한다. LLM이 직접 세거나
파일을 만들지 않는다. 이 스킬은 그 파이프라인을 올바른 순서로 호출하는 얇은 래퍼다.

## 순서

1. **무엇을 가져올지 미리보기(선택)**
   ```
   python pipelines/scrape_papers.py --dry-run
   ```
2. **스크랩 → 카드 저장** (주제·기간·편수는 인자로 조정)
   ```
   python pipelines/scrape_papers.py --days 7 --max 3
   # 특정 주제만: --topic Cardiology
   ```
   - 중복은 `state/seen_papers.json`(PMID)로 자동 판별한다. 이미 저장한 논문은 건너뛴다.
   - id는 `state.next_id('paper')`로만 발급된다.
3. **검증 + 색인**
   ```
   python pipelines/indexer.py --check   # 실패하면 멈추고 원인 보고
   python pipelines/indexer.py
   ```
4. **홈페이지 번들 재생성** (논문 피드에 새 논문이 뜨게 하려면 필수)
   ```
   python pipelines/export_papers_web.py   # content/papers/**/*.md → docs/papers.js
   ```
5. **커밋** — 새 `content/papers/**` + `state/seen_papers.json`(+ 필요시 `id_counter.json`,
   `seen_topics.json`) + `docs/papers.js`를 **같은 커밋**에 포함해 push.

## 자동화

- 매일은 `.github/workflows/scrape-papers.yml`(cron 21:00 UTC)가 위 1~5단계를 대신 돌린다.
- main에 커밋되면 `drive-sync.yml`이 Google Drive로 백업하고 `pages.yml`이 홈페이지를 배포한다.

## 주제 늘리기

`pipelines/scrape_papers.py`의 `TOPICS` 딕셔너리에 `주제: PubMed 검색어`를 추가한다.
저널을 한정하려면 검색어에 `AND "Circulation"[Journal]` 같은 절을 덧붙인다.

## 스크랩 vs 요약

- 스크랩(이 스킬): 사실 메타데이터 + 원문 초록만, `confidence: medium`. 매일 자동.
- 요약(`/gen-paper`): 스크랩된 카드의 Summary/Clinical Impact/My Ideas를 사람·LLM이 채움.
