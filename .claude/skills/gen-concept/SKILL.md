---
name: gen-concept
description: 내가 틀린 문항의 이론 정리본(content/concepts, type&#58; concept)을 쓰고 문항에 학습 목표를 연결한다. "정리본 써줘", "오답 이론 정리", "학습 목표 붙여줘", 매일 루틴의 정리본 단계에서 트리거.
---

# 개념 정리본 생성 규칙

정리본은 **학습 목표 단위**의 이론 카드다. 웹 앱(오답 뒤 학습 흐름)과 과별 PDF 학습서가 같은 원본을 쓴다.
계약은 `schemas/frontmatter.md` 의 「개념 정리본(concept)」·「오답 뒤 학습 흐름」 절이 원본이다 — 필드 이름은 거기서 확인한다.

## 무엇을 쓸지는 큐가 정한다(고르지 말 것)

```
python pipelines/concept_queue.py --limit <오늘 상한>
```
- `[note]` — 목표는 있는데 정리본이 없는 오답 → 정리본을 새로 쓴다.
- `[link]` — 목표가 없는 오답 → 문항에 `objective` 를 붙이고, 그 목표의 정리본이 없으면 이어서 쓴다.
- 큐가 비어 있으면 **아무것도 만들지 않는다**(학습 기록이 아직 저장소에 없을 때가 대부분 — 정상이다).

## 학습 목표(objective) 정하기

- id 형식 `cn.<과>.<주제>.<목표>` — 소문자·숫자·하이픈. 파일은 `content/concepts/<과 폴더>/<id>.md`.
- **질환명으로 합치지 않는다.** 같은 질환이라도 평가 목표가 다르면 다른 정리본이다
  (예: `cn.derm.pityriasis-versicolor.diagnosis` ≠ `…treatment`).
- 이미 있는 목표로 묶을 수 있으면 새로 만들지 말고 그 문항에 기존 id 를 붙인다(`python pipelines/concept_queue.py` 의
  「이미 정리본이 있는 오답 목표」 수가 그 결과다).
- 문항에는 `objective` 와 함께 가능하면 `distractors`(보기별 tempting·answer_first·discriminator·when_right·split)와
  `case_path`(도식 노드 경로, 문항에 없는 정보는 `state: unknown`)를 적는다 — 형식은 린터가 본다.

## 자리 정하기 — 기본틀 슬롯(`outline`)

정리본은 과별 학습서 안에서 **해리슨 21판의 서술 순서**로 꽂힌다. 그 자리를 frontmatter `outline:` 에 적는다.

```
python pipelines/outline.py --book 순환기내과 --gaps     # 그 과의 빈 자리
python pipelines/outline.py --find "arrhythmia"          # 슬롯·해리슨 장 제목 검색(PDF 를 열지 않는다)
```
- 슬롯 id 는 `h<장번호>`(해리슨이 다루는 주제) 또는 손으로 정한 id(`ob.labor`·`peds.neuro` 처럼 해리슨에 없는 과).
- 한 슬롯에 정리본이 여러 개 있어도 된다(같은 장 안의 다른 학습 목표). 순서만 정해 줄 뿐이다.
- 적을 자리가 마땅치 않으면 `content/outline/subjects.yaml` 에 슬롯을 **추가**한다(해리슨 장은 한 과에만).
- 비워 두면 책 맨 뒤 「배치 대기」로 가고 린터가 WARN 을 낸다.

## 해리슨을 읽어야 할 때 — 그 장만 읽는다

```
python pipelines/harrison_read.py --slot h255                 # 그 슬롯의 장 전체(기본 12,000자)
python pipelines/harrison_read.py --chapter 255 --grep "QT"   # 그 장에서 맞는 줄만
python pipelines/harrison_read.py --chapter 255 --pages 1925  # 인쇄쪽으로 더 좁히기
```
4,132쪽 PDF 를 통째로 뒤지지 않는다. 읽은 쪽은 `[[harrison-21: 255장 p.1925]]` 처럼 인용하고
`sources[].verified: text` 로 올린다(본문을 저장소 파일로 저장하지 않는다 — 교과서 저작권).

## 내용 — 깊이 규칙(PDF 학습서가 이 순서로 읽힌다)

정상 기능 → 이상이 생기는 기전 → 증상·검사 소견 → 감별·기준 → 치료 선택 → 반응 확인·재평가.
원인·치료명 나열로 설명을 대신하지 않는다. 다음은 분량을 줄이려고 빼지 않는다:
정상 생리와 병태생리의 연결 · 소견이 생기는 이유 · 수치의 단위·적용 조건 · 정상/음성 결과의 해석 한계 ·
치료의 적응·금기·예외 · 효과와 재평가 기준 · 근거와 검토 상태.

역할을 나눈다 — `summary`=전체 관계, 본문=이유, `tables`=차이 비교, `diagram`=흐름,
`diagram_notes`=그림만으로 전달되지 않는 조건·예외, `pitfalls`=혼동하기 쉬운 점(오답을 **일반화**해서).
`pitfalls[].covers` 에 `<문항id>:<보기>` 를 적으면 학습서가 그 오답을 중복해서 싣지 않는다.
학습자가 왜 그 보기를 골랐는지 **추측하지 않는다**(린터가 막는다).

## 근거 — 확인한 것만

- 본문·표·혼동 항목의 수치와 권고에는 `[[출처id: 쪽·절·표]]` 로 위치를 단다.
- `sources[].verified` 는 실제로 어디까지 봤는지다: `text`(권고 본문 대조) · `abstract`(초록만) · `citation`(서지만).
  text 가 아니면 화면·PDF 에 † 가 붙는다. 원문을 못 본 주장은 `[[?출처id]]`.
- 교과서는 `G:\내 드라이브\교과서\` 의 Harrison(인쇄쪽 = PDF 인덱스 − 40)·Guyton(스캔본, 렌더해서 읽기)을 인용할 수 있다.
  논문·지침은 PubMed·기관 쪽에서 **실제로 열어 본 뒤** 서지와 쪽수를 적는다. 없는 출처·안 본 쪽수를 만들지 않는다.
- 다른 나라·기관의 기준은 `criteria` 행을 나눠 쓰고 설명 없이 합치지 않는다(KMLE/USMLE 는 `exams` 로 구분).
- `review_status: unreviewed` 로 둔다. 사람이 본 뒤에만 `reviewed`+`reviewed_by`+`review_note`.

## 도식

`decision_diagram.py` 규격: 세로, 판단 노드는 갈래 2개 이상·조건 라벨 필수, 「추가 정보 필요(info)」 노드 1개 이상,
순환 없음, 결론 노드에서 선이 나가지 않는다. 한 단에 읽을 크기로 들어가야 한다(학습서 검증이 막는다) —
층이 8개를 넘으면 단계를 합치거나 의미 단위로 나눈다.

## 검증 — 커밋 전 필수

```
python pipelines/concepts.py                     # 정리본 계약·도식·근거 표시 검사(오류 0이어야 함)
python pipelines/lint_questions.py <objective 를 붙인 문항들>
python pipelines/export_concepts_web.py          # docs/concepts.js (publish.py 가 자동 실행하지만 미리 확인)
```
정리본을 만들었으면 과별 PDF 학습서는 다음 06:30 KST 실행이 자동으로 반영한다(`.github/workflows/books.yml`).
