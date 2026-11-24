---
id: cn.neuro.acute-vestibular-syndrome.central-signs-mri
type: concept
topic: Neurology
see_also: [Otorhinolaryngology, Emergency Medicine]
date: 2026-11-24
updated: 2026-11-24
version: 1
outline: h22             # 기본틀 슬롯 — 해리슨 21판 22장 Dizziness and Vertigo(22판 24장)
confidence: medium
review_status: unreviewed
note_form: 2
title: "급성 전정 증후군 — 정상 머리 충동 검사는 중추다"
objective: "지속되는 급성 전정 증후군에서 머리 충동 검사·안진 방향·체간 운동실조로 중추(소뇌·뇌간 경색)를 가려 CT 가 정상이어도 뇌 MRI 로 가야 함을 판단한다"
objective_kind: 진단
condition: 급성 전정 증후군(acute vestibular syndrome) — 소뇌 경색 대 전정신경염
exams: [usmle, kmle]
figures_none: 침상 진찰(눈 움직임)로 가르는 목표 — 정지 사진으로 보여 줄 소견이 아니다
summary:
  - "결론: 쉬지 않는 급성 어지럼에서 머리 충동 검사가 정상이면 말초가 아니라 중추 — 뇌 MRI 를 한다."
  - "시험 단서: 수 시간~며칠 계속되는 회전성 어지럼·구토·안진(acute vestibular syndrome), 혈관 위험 인자, CT 정상."
  - "왜: 전정신경염은 한쪽 전정안반사가 망가져 교정 단속운동이 생기는데, 소뇌 경색은 이 반사가 보존된다."
  - "중추 징후: 주시 방향에 따라 바뀌는 안진, 순수 수직·회선 안진, 사위, 앉지 못하는 체간 운동실조."
  - "사지 협조 검사가 정상이어도, 비조영 CT 가 정상이어도 소뇌 경색을 배제하지 못한다."
pitfalls:
  - contrast: "「머리를 움직이면 심해진다」 = 양성 돌발성 두위현훈(BPPV)?"
    point: "BPPV 는 머리 위치를 바꿀 때 1분 안(보통 15~20초) 생겼다 사라지는 발작이다. 가만히 누워 있어도 몇 시간 계속되는 어지럼은 급성 전정 증후군이고, 머리를 움직이면 심해지는 것은 어느 전정 병변에서나 생긴다."
    cites: ["harrison-22: 24장 p.163"]
    covers: ["usmle-2026-0294:A"]
  - contrast: "지속성 회전 어지럼 + 청력 정상 = 전정신경염?"
    point: "전정신경염이면 병든 쪽으로 머리를 돌릴 때 교정 단속운동이 생기고 안진은 한 방향으로만 뛴다. 급성 지속성 어지럼에서 머리 충동 검사가 정상이면 말초 병변 가능성이 낮고 중추를 의심한다."
    exception: "중추 징후가 없어도 혈관 위험 인자가 있는 고령이면 뇌졸중을 평가한다 — 진찰만으로 중추를 늘 배제하지는 못한다."
    cites: ["harrison-22: 24장 p.163"]
    covers: ["usmle-2026-0294:B"]
  - contrast: "메니에르병·전정 편두통 — 발작성 어지럼과의 혼동"
    point: "메니에르병은 저음역 청력 저하·귀 먹먹함을 동반한 몇 시간짜리 발작이 되풀이되고, 전정 편두통은 편두통 병력·빛 공포와 몇 분~몇 시간 발작이다. 처음 생겨 쉬지 않고 계속되는 어지럼과 앉지 못하는 운동실조에는 맞지 않는다."
    cites: ["harrison-22: 24장 p.164"]
    covers: ["usmle-2026-0294:D", "usmle-2026-0294:E"]
tables:
  - id: periph-central
    section: "가르는 소견 — 말초 대 중추"
    title: "급성 지속성 어지럼 — 말초와 중추를 가르는 침상 소견"
    role: comparison
    span: full
    columns: ["소견", "말초(전정신경염)", "중추(소뇌·뇌간 경색)"]
    rows:
      - ["머리 충동 검사", "병든 쪽으로 돌리면 교정 단속운동", "정상 — 교정 단속운동 없음"]
      - ["안진", "한 방향 수평(병변 반대쪽으로 뜀), 고정하면 줄어듦", "주시 방향에 따라 바뀜, 순수 수직·회선, 고정해도 안 줄어듦"]
      - ["눈 정렬", "정상", "수직 사위(가림 검사에서 교정 움직임)"]
      - ["동반 증상", "한쪽 청력 저하는 말초 쪽", "복시·구음장애·사지 운동실조·감각 이상"]
    note: "해리슨 Table 24-1 의 말초·중추 구분 [[harrison-22: 24장 p.163]]. 심한 체간 운동실조(붙잡지 않고 앉지 못함)는 표에 없는 임상 단서로 덧붙였다."
diagram:
  title: "쉬지 않는 급성 어지럼 — 말초인가 중추인가"
  nodes:
    - {id: start, kind: start, text: "갑작스러운 지속성 어지럼·구토·안진"}
    - {id: info, kind: info, text: "지속 시간·청력·신경 증상·혈관 위험 인자"}
    - {id: dur, kind: decision, text: "가만히 있어도 계속되는가?"}
    - {id: bppv, kind: end, text: "위치 유발·1분 안 — 딕스-홀파이크"}
    - {id: hit, kind: decision, text: "머리 충동 검사에 교정 단속운동?"}
    - {id: other, kind: decision, text: "다른 중추 징후나 혈관 위험이 있나?"}
    - {id: neuritis, kind: end, text: "전정신경염 — 대증 치료·조기 재활"}
    - {id: mri, kind: end, text: "중추 의심 — 뇌 MRI(확산강조)"}
  edges:
    - {from: start, to: info}
    - {from: info, to: dur}
    - {from: dur, to: bppv, label: "아니다"}
    - {from: dur, to: hit, label: "그렇다"}
    - {from: hit, to: mri, label: "없다(정상)"}
    - {from: hit, to: other, label: "있다"}
    - {from: other, to: mri, label: "있다"}
    - {from: other, to: neuritis, label: "없다"}
diagram_notes:
  - "다른 중추 징후 = 방향이 바뀌는 안진 · 순수 수직/회선 안진 · 수직 사위 · 복시·구음장애·사지 운동실조 · 앉지 못하는 체간 운동실조."
  - "비조영 CT 는 후두와 경색을 놓치기 쉽다 — CT 정상은 이 도식의 갈래를 바꾸지 않는다."
  - "새로 생긴 한쪽 청력 저하는 말초 쪽이지만, 내이 동맥 경색처럼 중추 혈관 원인일 수도 있어 혈관 위험이 크면 영상을 본다."
checks:
  - q: "머리 충동 검사에서 교정 단속운동이 생기는 이유는?"
    a: "머리를 병든 쪽으로 빨리 돌릴 때 그쪽 전정안반사가 약해 눈이 머리와 함께 끌려가고, 표적을 놓친 뒤 반대 방향 단속운동으로 다시 잡는다."
  - q: "급성 지속성 어지럼 환자의 손가락-코 검사가 정상이다. 소뇌 경색을 배제할 수 있나?"
    a: "아니다. 소뇌 충부 병변은 사지가 아니라 체간 운동실조(앉기·서기 불가)로 나타난다."
  - q: "주시 방향에 따라 바뀌는 수평 안진은 어디 병변인가?"
    a: "소뇌 경로(중추). 말초 병변의 안진은 한 방향으로만 뛴다."
variants:
  - id: v1
    of: usmle-2026-0294
    flip: true
    changed: "Normal head impulse, direction-changing nystagmus, cannot sit → corrective saccade on rightward head turns, unidirectional left-beating nystagmus suppressed by fixation, walks with a wide base — the bedside findings turn peripheral, so vestibular neuritis becomes the answer"
    context: "Same acute vestibular syndrome with peripheral bedside signs and no vascular risk factors"
    stem: "A 41-year-old woman comes to the emergency department 14 hours after the sudden onset of continuous room-spinning vertigo that began when she woke up. The vertigo is present even when she lies still and is worse with head movement; she has vomited four times. She had a sore throat and runny nose 10 days ago. She has no headache, hearing loss, tinnitus, ear fullness, double vision, or difficulty speaking or swallowing. She has no history of migraine and takes no medications. Temperature is 37.0°C (98.6°F), pulse is 88/min, and blood pressure is 124/78 mm Hg. There is horizontal nystagmus that beats to the left in all directions of gaze and decreases when she fixates on a target. When her head is turned rapidly to the right while she looks at the examiner's nose, her eyes move with the head and then make a leftward corrective movement back to the target; head turns to the left are normal. Alternate cover testing shows no vertical refixation. Hearing, facial movements, limb strength, sensation, and finger-to-nose testing are normal. She can sit unaided and walks with a wide-based, unsteady gait. Which of the following is the most likely diagnosis?"
    choices: ["A. Benign paroxysmal positional vertigo", "B. Vestibular neuritis", "C. Cerebellar infarction", "D. Ménière disease", "E. Vestibular migraine"]
    answer: "B"
    explanation: "This is still an acute vestibular syndrome (continuous vertigo for hours), but every bedside sign is now peripheral: an abnormal head impulse test to the right (corrective saccade), unidirectional nystagmus that is suppressed by fixation, no skew deviation, and she can sit unaided. In the original item the normal head impulse test, direction-changing nystagmus, and inability to sit pointed to a central lesion. Positional vertigo lasts under a minute, Ménière disease brings aural symptoms, and vestibular migraine needs a migraine history."
    kind: application
  - id: v2
    of: usmle-2026-0294
    flip: false
    changed: "Man watching TV → 72-year-old woman with atrial fibrillation waking with vertigo, findings listed in a different order and skew deviation replaces gaze-evoked nystagmus as the extra sign; normal head impulse and inability to stand remain, so the answer is still cerebellar infarction"
    context: "Acute vestibular syndrome with a normal head impulse test in a patient with atrial fibrillation"
    stem: "A 72-year-old woman is brought to the emergency department 6 hours after she awoke with severe, constant dizziness and vomiting. She says the room has been spinning without pause even while she lies still. She has atrial fibrillation and stopped taking her anticoagulant 2 weeks ago. She has no headache, hearing loss, tinnitus, or ear fullness. Pulse is 104/min and irregularly irregular; blood pressure is 158/88 mm Hg. Rapid head turns to either side while she looks at the examiner's nose produce no corrective eye movement. Alternate cover testing shows the left eye moving down to refixate. There is a horizontal right-beating nystagmus. Speech, facial sensation, and limb strength are normal, and heel-to-shin testing is normal bilaterally. She cannot stand without support. A noncontrast CT of the head is normal. Which of the following is the most likely diagnosis?"
    choices: ["A. Vestibular neuritis", "B. Benign paroxysmal positional vertigo", "C. Ménière disease", "D. Cerebellar infarction", "E. Labyrinthitis"]
    answer: "D"
    explanation: "Continuous vertigo for hours is an acute vestibular syndrome. A normal head impulse test in this setting argues against a peripheral lesion, and the vertical refixation on cover testing (skew deviation) and inability to stand are central signs. With atrial fibrillation off anticoagulation, a cardioembolic cerebellar infarction is most likely; normal heel-to-shin testing and a normal CT do not exclude it, so brain MRI with diffusion-weighted imaging follows. Unidirectional nystagmus alone does not make it peripheral when the head impulse test is normal."
    kind: application
sources:
  - id: harrison-22
    org: "McGraw Hill"
    title: "Harrison's Principles of Internal Medicine, 22nd ed."
    kind: textbook
    year: 2025
    citation: "Harrison's Principles of Internal Medicine, 22e. 24장 Dizziness and Vertigo p.162–165"
    checked_at: 2026-11-24
    checked: "본문 대조(드라이브 장별 문서 H22_024) — p.162 동반 증상(한쪽 청력 저하는 말초, 복시·감각 이상·사지 운동실조는 중추)·눈 정렬 가림 검사에서 수직 사위는 뇌간·소뇌, p.163 주시 유발 안진·하향 안진은 소뇌 경로·말초는 한 방향 수평 안진, 머리 충동 검사(교정 단속운동), 급성 전정 증후군에서 머리 충동 검사가 정상이면 말초 병변 가능성 낮음·혈관 위험 인자가 있는 고령은 특이 소견이 없어도 뇌졸중 평가, BPPV 발작 <1분(15~20초), Table 24-1, p.164 전정 편두통·메니에르병, p.165 중추성 급성 어지럼은 응급·모든 중추 의심 환자에게 뇌 MRI"
    verified: text
---

## 판단 — 왜 중추이고 MRI 인가
- 급성 전정 증후군에서 가장 중요한 질문은 병변이 생명을 위협하는 중추(소뇌·뇌간 경색·출혈)인가, 말초(전정신경염)인가다 [[harrison-22: 24장 p.163]].
- 머리 충동 검사가 정상이면 급성 말초 병변 가능성이 낮다 — 지속성 어지럼에서 머리 충동 징후가 없으면 중추를 생각한다 [[harrison-22: 24장 p.163]].
- 방향이 바뀌는 주시 유발 안진은 소뇌 경로 병변의 안진이다 [[harrison-22: 24장 p.163]].
- 중추가 의심되면 모두 뇌 MRI 를 한다. 진찰만으로 늘 배제되지 않으므로 혈관 위험 인자가 있는 고령은 특이 소견이 없어도 뇌졸중을 평가한다 [[harrison-22: 24장 p.163]] [[harrison-22: 24장 p.165]].

## 기전 — 전정 입력의 비대칭에서 소견으로
양쪽 미로의 입력은 평소 균형을 이룬다. 한쪽 전정신경이 갑자기 꺼지면 머리가 계속 도는 것처럼 신호가 기울어 가만히 있어도 어지럼·구역·안진이 계속된다 [[harrison-22: 24장 p.163]]. 머리 충동 검사는 작고 빠른 머리 회전으로 전정안반사(VOR)를 본다 — 약한 쪽으로 돌리면 눈이 머리를 따라가 버려 반대 방향 교정 단속운동이 생긴다 [[harrison-22: 24장 p.163]]. 소뇌 경색은 미로·전정신경을 건드리지 않아 이 반사가 남는다. 대신 주시 유지·눈 정렬·체간 균형을 맡는 소뇌·뇌간 회로가 깨져 방향이 바뀌는 안진, 사위, 앉지 못하는 운동실조가 나온다.

## 가르는 소견 — 말초 대 중추
- 시간: BPPV 는 1분 안, 전정 편두통·메니에르병 발작은 흔히 몇 시간이고, 쉬지 않고 계속되는 급성 어지럼은 전정신경염 또는 중추 병변이다 [[harrison-22: 24장 p.162]] [[harrison-22: 24장 p.163]].
- 한쪽 청력 저하·귀 먹먹함은 말초 쪽, 복시·구음장애·감각 이상·사지 운동실조는 중추 쪽이다 [[harrison-22: 24장 p.162]].
- 사지 협조 검사 정상은 소뇌 충부 경색을 배제하지 못한다. 비조영 CT 는 후두와 경색에 둔감하다 — 다음 검사는 확산강조 MRI 다.

## 권고와 예외
- 중추성 급성 어지럼은 응급이다 — 신경과 평가와 뇌 MRI [[harrison-22: 24장 p.165]].
- 전정신경염으로 결론 나면 전정 억제제는 처음 며칠만 쓰고, 일찍 움직이게 하고 전정 재활을 한다 [[harrison-22: 24장 p.163]].

## 시험 쟁점 — 충돌·맥락·새 근거
- 해당 없음(대조: 해리슨 22판 24장 p.162~165)
