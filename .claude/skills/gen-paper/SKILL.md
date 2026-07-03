---
name: gen-paper
description: 논문(PDF/초록/제목)을 받아 표준 frontmatter가 붙은 요약 카드 .md를 content/papers/에 생성한다. "논문 요약", "이 논문 카드로", "paper of the day" 요청에 트리거.
---

# 논문 요약 카드 생성 규칙

> 매일 자동 수집은 `/scrape-papers`(PubMed → 사실 메타데이터 + 초록, `confidence: medium`)가
> 담당한다. 이 스킬은 그렇게 수집된 카드(또는 직접 받은 논문)의 **해석 섹션**
> (Summary/Clinical Impact/Guideline 변화/My Ideas)을 채우는 단계다. 초록을 요약으로
> 옮길 때 원문을 길게 복사하지 말고 자기 언어로 재서술한다.

## 필드
- `type: paper`, `topic`(예: Cardiology), `source`(저널), `confidence`
- `related` 에 관련 질환/약물 카드 id를 연결(지식 그래프).
- `id` 는 `state.next_id('paper')`.

## 저장 경로
`content/papers/{연도}/{date}_{slug}.md`

## 본문 섹션(고정)
```
## Title
## Authors
## Journal / DOI
## Summary
## Strength
## Weakness
## Clinical Impact      ← 이 연구가 왜 practice-changing인가
## Guideline 변화       ← 이전 가이드라인과 무엇이 달라졌나(있으면)
## My Ideas             ← 후속 아이디어/연구 메모
```

## 원칙
- 원문을 그대로 길게 옮기지 말고 자신의 언어로 요약한다.
- 저작권: 원문 직접 인용은 짧게, 핵심은 재서술한다.
- Clinical Impact와 Guideline 변화는 임상 추론 훈련의 핵심이므로 반드시 채운다.
