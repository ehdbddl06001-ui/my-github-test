---
name: gen-card
description: 질환(disease) 또는 약물(drug) 참고 카드를 표준 frontmatter가 붙은 .md로 생성한다. "질환 카드 만들어", "약물 정리", "ARDS 카드", "메로페넴 카드" 요청에 트리거.
---

# 질환/약물 카드 생성 규칙

## 필드
- `type: disease` 또는 `type: drug`
- `id` 는 `state.next_id('disease')` / `next_id('drug')`
  또는 안정적 슬러그(예: `disease-heart-failure`, `drug-sglt2i`)를 쓴다.
- `related` 로 관련 문제/논문/다른 카드를 연결.
- 교과서 기반이면 `edition`(예: `Robbins 10e`, `Katzung 15e`)과 `source` 명시.

## 저장 경로
- 질환 → `content/diseases/{id}.md`
- 약물 → `content/drugs/{id}.md`

## 본문 섹션
질환:
```
## Definition / ## Pathophysiology / ## Diagnosis /
## Treatment / ## Guideline / ## Recent papers / ## My Notes
```
약물:
```
## Class / ## Mechanism / ## Indications / ## Dosing /
## Adverse effects / ## Interactions / ## My Notes
```

## 원칙
- 교과서·강의·논문이 충돌하면 각 출처를 표기하고 confidence로 신뢰도를 남긴다.
- OCR로 뽑은 그림/표는 원본 이미지 경로도 함께 남긴다(오인식 대비).
- 판(edition)이 바뀌면 새 파일로 만들지 말고 같은 파일을 수정하고 `updated`를 갱신한다.
