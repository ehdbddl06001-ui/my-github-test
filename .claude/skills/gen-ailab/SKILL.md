---
name: gen-ailab
description: 의료 AI·코딩 학습 카드(type ailab)를 표준 frontmatter가 붙은 .md로 생성한다. 공개 프로젝트(Keras/PyTorch/MONAI 등) 분석, 주간 실습 주제, 오픈 데이터 실습 노트를 도식(Mermaid)·지시어 해설과 함께 정리. "AI 카드 만들어", "이 프로젝트 분석", "뇌종양 분할 정리", "Keras 예제 뜯어줘" 요청에 트리거.
---

# ailab 카드 생성 규칙

의료 AI/코딩 공부용 카드를 `content/ailab/`에 만든다. 규격은 `schemas/frontmatter.md`의
**AI/코딩 학습(`ailab`)** 절을 따른다. 결정론적인 것(데이터 목록·주차)은 직접 세지 말고
`pipelines/datasets.py`를 인용한다.

## 입력
- 프로젝트 URL(예: keras.io 예제) 또는 주제/데이터셋 키(예: `ptb-xl`).
- 없으면 `python pipelines/datasets.py`의 이번 주 주제를 대상으로 삼는다.

## 순서
1. **ID 발급** — `python -c "from pipelines.state import next_id; print(next_id('ailab'))"`
2. **frontmatter** — 공통 필수(`id/type/topic/date/confidence`) + 선택(`kind/framework/
   arch/modality/level/project_url/dataset/dataset_url/colab_url/notebook/week`).
   - `kind`: `project`(프로젝트 분석)·`roadmap`·`weekly`(주간 실습)·`concept`.
   - `dataset`은 `pipelines/datasets.py`의 key와 **반드시 일치**시킨다.
   - `date`는 KST 기준 오늘(`TZ=Asia/Seoul date +%F`).
3. **본문 섹션(관례 준수 — 웹 피드가 파싱)**:
   `## Overview` → `## Architecture`(Mermaid 또는 ASCII 도식) → `## Data` →
   `## Code walkthrough`(핵심 코드, 대표 골격) → `## Instructions`(지시어→무엇을
   시키는가 표) → `## Exercises`(직접 해볼 것) → `## Resources` → `## My notes`(빈 칸).
   - **Architecture는 반드시 도식을 넣는다**(```mermaid ...``` 권장). 사용자가 구조를
     '보고' 이해하는 게 목적.
   - **Instructions 표**가 이 카드의 핵심: 코드의 각 지시어가 모델에게 뭘 시키는지 한국어로.
4. **정직성** — 공식 문서/코드 기반이면 `confidence: high`, 해석·추정이 섞이면 `medium`.
   실제 API 세부가 확실치 않으면 "원본과 대조하라"고 명시하고 medium으로 둔다.
5. **주제 기록** — `python -c "from pipelines.state import record_topic; record_topic('ailab', '<topic>')"`
6. **검증·색인·번들·커밋** — 아래 공통 마무리.

## 공통 마무리 (커밋 전 필수)
```
python pipelines/indexer.py --check          # frontmatter 검증(실패 시 중단)
python pipelines/indexer.py                  # SQLite 재빌드
python pipelines/export_ailab_web.py         # → docs/ailab.js (홈페이지 🤖 AI랩)
python pipelines/export_search_web.py        # → docs/search-index.js (통합검색 갱신)
```
새 `.md` + `state/*.json` + 재생성된 `docs/` 번들을 **같은 커밋**에 포함한다.

## 커밋 정책
- `ailab`는 신규 타입이라 self-verify 한계가 있다 → **claude/ 브랜치에 push 후 PR**로 검수.
  (paper/disease/drug와 같은 규칙.)
