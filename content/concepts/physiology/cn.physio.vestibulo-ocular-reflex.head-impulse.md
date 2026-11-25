---
id: cn.physio.vestibulo-ocular-reflex.head-impulse
type: concept
topic: Physiology
see_also: [Neurology, Otolaryngology]
date: 2026-11-25
updated: 2026-11-25
version: 1
outline: physio.neuro       # 생리학 책 「신경계 — 감각·운동·자율신경」
layer: basic            # 기초 정리본 — 임상 정리본의 roots 가 가리키는 기전 단위
discipline: physiology
system: nervous
textbook_check: pending
confidence: medium
review_status: unreviewed
note_form: 2
title: "전정안반사 — 한쪽이 꺼지면 머리 충동에 눈이 따라간다"
objective: "양쪽 미로의 긴장성 입력 균형과 전정안반사(VOR)로, 한쪽 말초 전정 손상이 지속성 어지럼·한 방향 안진·비정상 머리 충동 검사를 만들고 소뇌·뇌간 병변은 반사를 남긴 채 방향이 바뀌는 안진을 만드는 이유를 설명한다"
objective_kind: 기전
condition: 전정안반사와 전정 비대칭(vestibulo-ocular reflex, vestibular asymmetry)
exams: [usmle, kmle]
summary:
  - "결론: 머리 충동 검사가 비정상이면 반사 고리의 말초(미로·전정신경)가 꺼진 것이고, 정상이면 말초 손상이 아니다."
  - "시험 단서: 가만히 있어도 계속되는 어지럼 + 안진, 한쪽으로 빠르게 머리를 돌릴 때 교정 단속운동(catch-up saccade)."
  - "왜: 양쪽 미로의 쉬는 신호가 서로 상쇄되다가 한쪽이 꺼지면 뇌는 머리가 계속 도는 것으로 읽는다."
  - "양쪽이 함께 꺼지면 비대칭이 없어 어지럼 대신 불균형·동요시(oscillopsia)가 생긴다."
pitfalls:
  - contrast: "머리 충동 검사 정상 = 안심?"
    point: "지속성 어지럼이 있는데 머리 충동 검사가 정상이면 반사 고리의 말초가 살아 있다는 뜻이라, 어지럼은 소뇌·뇌간 쪽에서 왔다고 본다 [[harrison-22: 24장 p.163]]."
  - contrast: "안진이 있으면 다 말초?"
    point: "말초 손상의 안진은 한 방향이고 손상 반대쪽으로 빠른 성분이 뛰며 주시로 억제된다. 주시 방향에 따라 바뀌거나 순수 수직·회전형이거나 주시로 줄지 않으면 중추다 [[harrison-22: 24장 p.163]]."
  - contrast: "천천히 자라는 전정신경초종도 어지럼?"
    point: "결손이 천천히 생기면 중추가 보상해 어지럼이 거의 없다 — 머리 충동 검사만 손상 쪽에서 비정상이다 [[harrison-22: 24장 p.164]]."
tables:
  - id: lesion-pattern
    title: "병변 자리에 따른 전정 소견"
    role: comparison
    span: column
    section: "소견으로 — 머리 충동 검사와 안진이 생기는 이유"
    columns: ["병변", "어지럼", "머리 충동 검사", "안진"]
    rows:
      - ["한쪽 말초, 갑자기", "지속성 회전성", "손상 쪽으로 돌릴 때 교정 단속운동", "한 방향, 손상 반대쪽으로 뜀"]
      - ["한쪽 말초, 천천히", "거의 없음(보상)", "손상 쪽 비정상", "뚜렷하지 않음"]
      - ["양쪽 말초", "없음 — 불균형·동요시", "양쪽 모두 비정상", "없음"]
      - ["소뇌·뇌간", "지속성일 수 있음", "정상", "방향이 바뀜·수직·주시로 안 줄어듦"]
    note: "[[harrison-22: 24장 p.163–164]]"
checks:
  - q: "오른쪽 전정신경염에서 머리를 오른쪽으로 빠르게 돌리면 눈은 어떻게 움직이는가?"
    a: "오른쪽 반사가 약해 눈이 머리를 따라 오른쪽으로 끌려가고, 표적으로 돌아오려 왼쪽으로 교정 단속운동이 생긴다."
  - q: "양쪽 전정 기능이 함께 떨어진 환자에게 회전성 어지럼이 없는 이유는?"
    a: "양쪽 입력이 함께 줄어 비대칭이 없기 때문이다 — 대신 어둠에서 불균형, 걸을 때 동요시가 생긴다."
variants:
  - id: v1
    flip: false
    changed: "핵심 변형 — 지속성 어지럼에서 정상 머리 충동 검사가 뜻하는 반사 고리의 자리를 묻는다"
    context: "급성 지속성 어지럼, 머리 충동 검사 정상"
    stem: "A 67-year-old man with hypertension and diabetes has had constant vertigo, nausea, and unsteadiness since he woke up 6 hours ago. He cannot sit without support. Nystagmus beats to the left on left gaze and to the right on right gaze. When the examiner rapidly rotates his head about 20 degrees to either side while he fixates on the examiner's nose, his eyes stay on the target without any corrective saccade. Hearing is normal. Which of the following best explains the head impulse finding?"
    choices: ["A. Loss of tonic firing of the left vestibular nerve", "B. Loss of tonic firing of both vestibular nerves", "C. An intact labyrinth-to-vestibular-nerve limb of the vestibulo-ocular reflex", "D. Otoconia displaced into the posterior semicircular canal", "E. Endolymphatic hydrops of one labyrinth"]
    answer: "C"
    explanation: "A normal head impulse test means the peripheral limb of the vestibulo-ocular reflex (labyrinth and vestibular nerve) is working on both sides; a unilateral or bilateral nerve loss would produce catch-up saccades. Together with direction-changing gaze-evoked nystagmus and inability to sit, this points to a cerebellar or brainstem lesion. BPPV and Ménière's disease cause episodic, not constant, vertigo."
    kind: application
figures_none: 반사 기전 — 영상 소견이 단서가 아니다(안진은 동영상 소견)
sources:
  - id: harrison-22
    org: "McGraw Hill"
    title: "Harrison's Principles of Internal Medicine, 22nd ed."
    kind: textbook
    year: 2025
    citation: "Harrison's Principles of Internal Medicine, 22e. 24장 Dizziness and Vertigo p.162–165"
    checked_at: 2026-11-25
    checked: "본문 대조(드라이브 22판 장별 문서 H22_024) — p.162 급성 한쪽 손상은 양쪽 미로 입력의 갑작스러운 불균형으로 어지럼, 양쪽 손상은 불균형·동요시, 대칭적 양쪽 저하는 어지럼 없음 · p.163 머리 충동 검사(약 20도의 빠른 회전, VOR 결손 시 반대 방향 교정 단속운동, 한쪽·양쪽 결손 구별), 표 24-1(말초 안진은 한 방향·손상 반대쪽으로 뜀·주시로 억제, 방향이 바뀌는 안진·순수 수직/회전형은 중추, 지속성 어지럼에서 머리 충동 징후가 없으면 중추) · p.164 전정신경초종은 서서히 생겨 중추 보상으로 어지럼이 없고 손상 쪽 머리 충동 검사 비정상, 양쪽 저하는 양방향 비정상·어둠에서 불균형. 반규관 유모세포의 긴장성 발화와 양쪽 상쇄 기전 서술은 이 장에 없어 표준 생리로 두었다(전공 교과서 미대조)"
    verified: text
---

## 정상 — 양쪽 미로가 쉬는 신호를 상쇄한다
반규관의 유모세포는 머리가 가만히 있어도 전정신경에 일정한 신호(긴장성 발화)를 보낸다. 머리가 한쪽으로 돌면 그쪽 신경 발화가 늘고 반대쪽은 줄어, 뇌간 전정핵은 **양쪽의 차이**를 머리 회전으로 읽는다. 전정안반사(vestibulo-ocular reflex, VOR)는 이 차이로 눈을 머리와 반대 방향으로 같은 크기만큼 돌려, 머리가 움직여도 시선이 표적에 머문다.

## 고장 — 한쪽이 꺼지면 머리가 도는 것으로 읽힌다
한쪽 미로나 전정신경이 갑자기 꺼지면 가만히 있어도 양쪽 차이가 생겨 뇌는 머리가 계속 도는 것으로 읽는다 — 지속성 회전성 어지럼·구역·안진·불균형이다 [[harrison-22: 24장 p.162]] [[harrison-22: 24장 p.163]]. 양쪽이 함께 꺼지면 차이가 없어 어지럼은 없고, 머리가 움직일 때 시선을 붙잡지 못해 동요시와 어둠 속 불균형이 생긴다 [[harrison-22: 24장 p.164]]. 결손이 천천히 생기면 중추가 그 비대칭을 보상한다 [[harrison-22: 24장 p.164]].

## 소견으로 — 머리 충동 검사와 안진이 생기는 이유
- 머리 충동 검사: 약 20도의 빠른 회전에서 약한 쪽으로 돌리면 반사가 모자라 눈이 머리에 끌려가고, 표적으로 돌아오는 반대 방향 교정 단속운동이 보인다 [[harrison-22: 24장 p.163]].
- 말초 안진: 건강한 쪽 우세로 눈이 손상 쪽으로 천천히 밀리고, 빠른 성분은 손상 반대쪽으로 뛴다. 시각 고정이 이 안진을 억제한다 [[harrison-22: 24장 p.163]].
- 소뇌·뇌간 병변은 반사 고리의 말초를 건드리지 않아 머리 충동 검사가 정상이다. 대신 주시를 붙잡는 회로가 깨져 주시 방향마다 바뀌는 안진이 나온다 [[harrison-22: 24장 p.163]].

## 임상 판단으로 — 정상 반사가 중추를 가리킨다
- 급성 지속성 어지럼에서 머리 충동 검사가 정상이면 말초 손상 가능성이 낮아 중추(뇌졸중)를 평가한다 — 임상 판단은 `cn.neuro.acute-vestibular-syndrome.central-signs-mri`.
- 천천히 진행하는 한쪽 감각신경성 난청 + 손상 쪽 머리 충동 검사 이상은 소뇌교각 종양을 생각한다 [[harrison-22: 24장 p.164]].

## 시험 쟁점 — 충돌·맥락·새 근거
- 해당 없음(대조: 해리슨 22판 24장 p.162~164)
