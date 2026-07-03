---
name: gen-basic
description: 기초의학(basic) 학습 카드를 표준 frontmatter가 붙은 .md로 생성한다. 생리학·생화학·약리학·해부·미생물·면역·병리의 개념을 임상과 연결해 정리. "기초의학 카드", "Daily Basic", "Starling force 정리", "산-염기 카드", "오늘 기초의학" 요청에 트리거.
---

# 기초의학(basic) 카드 생성 규칙

임상 문제(kmle/usmle)가 "무엇을 고르나"라면, 기초의학 카드는 "왜 그런가"를 남긴다.
매일 한 개념씩 쌓여 임상 지식의 뿌리가 되는 자산이다(계획의 MVP 항목 "Daily Basic").

## 필드 (schemas/frontmatter.md 준수)
- `type: basic`  (문제형이 아니므로 stem/choices/answer 없음)
- `id` 는 `state.next_id('basic')` 로만 발급 (예: `basic-2026-0007`)
- `topic` 은 분야를 쓴다: `Physiology` / `Biochemistry` / `Pharmacology` /
  `Anatomy` / `Microbiology` / `Immunology` / `Pathology`
- `subtopic` 에 구체 개념(예: `Starling forces`, `Anion gap`)
- `confidence`: 표준 교과서 근거면 `high`. 출처 충돌·불확실하면 낮추고 `source` 남김
- 선택: `edition`(예: `Guyton 14e`, `Lippincott 8e`), `tags`, `related`(연결된 질환/약물/문제 id)

## 저장 경로
- `content/basic/{id}.md`  (연도 폴더 없이 평면)

## 본문 섹션 (권장 순서)
```
## 핵심 개념      한두 문단으로 정의·큰 그림
## 기전          단계적 메커니즘(필요하면 마크다운 표)
## 임상 연결      이 개념이 어떤 질환·약물·검사로 이어지는가
## 오개념·함정    시험·임상에서 자주 틀리는 지점
## 한 줄 요약     시험 직전 회독용 1문장
```

## 원칙
- **정확성 우선**: 기초의학은 임상 판단의 뿌리라 틀리면 위로 다 번진다. 표준 교과서
  기준으로 쓰고, 애매하면 `confidence`를 낮추고 `source`/`edition`을 남긴다.
- 그림·그래프가 필요하면 **마크다운 표(텍스트)**로 대체한다. AI가 그린 의료 도해는
  부정확할 위험이 있어 실제 이미지 파일을 만들지 않는다(퀴즈 루틴과 동일한 원칙).
- OCR로 뽑은 표/그림을 넣을 때는 원본 이미지 경로를 함께 남긴다(오인식 대비).
- `related` 로 관련 질환/약물/문제 카드를 연결해 지식 그래프의 씨앗을 만든다.

## 최소 예시
```markdown
---
id: basic-2026-0007
type: basic
topic: Physiology
subtopic: Starling forces
source: "Guyton and Hall Textbook of Medical Physiology 14e"
edition: "Guyton 14e"
confidence: high
date: 2026-07-03
tags: [edema, capillary, oncotic-pressure]
related: [disease-heart-failure]
---

## 핵심 개념
모세혈관 벽을 사이에 둔 정수압·교질삼투압의 균형(Starling force)이 …

## 기전
| 힘 | 방향 | 설명 |
|---|---|---|
| 모세혈관 정수압 | 밖으로 | … |

## 임상 연결
…

## 오개념·함정
…

## 한 줄 요약
…
```

## 생성 후 (daily-run 이 대신 수행)
1. `python pipelines/indexer.py --check` → `indexer.py` (검증·색인)
2. `python pipelines/export_search_web.py` (통합검색 색인 갱신 → 웹에서 검색됨)
3. 새 `.md` + `state/*.json` + `docs/search-index.js` 를 같은 커밋에 포함
