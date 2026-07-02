---
name: gen-kmle
description: KMLE 또는 USMLE 시험 문제를 표준 frontmatter가 붙은 .md로 생성한다. "KMLE 문제 만들어", "USMLE 문항 생성", "국시 문제" 요청에 트리거.
---

# KMLE/USMLE 문제 생성 규칙

## 필드
`schemas/frontmatter.md` 의 문제형 규격을 그대로 따른다. 특히:
- `answer_separated: true` 필수. stem에는 정답 힌트를 넣지 않는다.
- `id` 는 `state.next_id('kmle')` 또는 `next_id('usmle')` 로만 발급.
- `topic` 은 16개 임상 과목 기준(내과/외과/소아/산부인과/…)에서 고른다.

## 저장 경로
- KMLE → `content/kmle/{연도}/{id}.md`
- USMLE → `content/usmle/{id}.md`

## 품질 규칙
1. 최근 `recent_topics()` 로 나온 주제는 피한다(중복 방지).
2. 임상 추론형으로 작성: 단순 암기보다 감별진단·치료선택 위주.
3. 근거가 불확실하면 `confidence: medium/low` 로 낮추고 `source`에 근거를 남긴다.
4. 생성 직후 스스로 정답의 타당성을 한 번 검증한다. 의학적 정확도는
   자기검증에 한계가 있으므로, 애매하면 문제를 버리고 다시 만든다.

## 본문 구조(사람이 읽는 부분)
```
## 문제
{stem}

- A. …
- B. …

## 정답 및 해설
> 정답: {answer}
{explanation}
```
