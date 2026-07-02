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

## USMLE 전용 규칙 (반드시 지킬 것)
- frontmatter에 `step`("Step 1" 또는 "Step 2")과 `exam_subject`를 **반드시** 넣는다.
  없으면 `indexer.py --check`에서 실패하고 웹/CLI 퀴즈에 분류되지 않는다.
  - Step 1 과목: Pharmacology, Immunology, Biochemistry, Microbiology, Pathology, Physiology
  - Step 2 과목: Internal Medicine, Surgery, Neurology, Pediatrics, Obstetrics & Gynecology, Psychiatry
- stem·보기는 실제 시험 형식대로 **영문**, 해설은 한글(핵심 용어 영어 병기)로 쓴다.
- 본문 `## 정답 및 해설`은 `- **키**: 값` 불릿 구조를 유지한다
  (`export_usmle_web.py`가 이 텍스트를 파싱해 웹/CLI 해설로 사용).
- 생성 후 반드시 `python pipelines/export_usmle_web.py`로 `docs/questions_usmle.js`를
  재생성해 같은 커밋에 포함한다(안 하면 개인 페이지에 새 문항이 안 뜬다).

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
