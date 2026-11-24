---
id: cn.pharm.lithium.renal-handling-dialyzability
type: concept
topic: Pharmacology
see_also: [Emergency Medicine, Psychiatry, Nephrology]
date: 2026-11-24
updated: 2026-11-24
version: 1
outline: pharm.toxicology   # 약리학 책 「독성학·해독제」
layer: basic            # 기초 정리본 — 임상 정리본의 roots 가 가리키는 기전 단위
discipline: pharmacology
system: nervous
textbook_check: pending
confidence: medium
review_status: unreviewed
note_form: 2
title: "리튬 약동학 — 콩팥이 내보내고 투석이 잘 뺀다"
objective: "리튬이 단백 결합 없는 작은 이온으로 콩팥으로만 나가고 근위세뇨관에서 나트륨과 함께 재흡수되는 성질로, 탈수·티아지드·NSAID·ACE억제제가 농도를 올리는 이유와 뇌로 천천히 들어가는 분포 때문에 만성 축적이 낮은 혈중 농도에서도 중증 신경독성을 내는 이유, 그리고 혈액투석이 잘 듣는 이유를 설명한다"
objective_kind: 기전
condition: 리튬의 콩팥 배설·분포와 중독(lithium pharmacokinetics)
exams: [usmle, kmle]
summary:
  - "결론: 리튬은 콩팥으로만 나가고 뇌에는 천천히 차므로, 배설이 막히면 쌓이고 투석으로 잘 빠진다."
  - "시험 단서: 리튬 복용 + 티아지드·NSAID·ACE억제제·탈수 시작 뒤 실조·근간대경련(chronic lithium toxicity)."
  - "왜: 근위세뇨관이 리튬을 나트륨처럼 재흡수해, 나트륨·용적이 줄면 리튬 재흡수가 늘어난다."
  - "작은 이온·단백 결합 없음·작은 분포용적이라 혈액투석이 잘 빼고, 활성탄에는 붙지 않는다."
  - "만성 축적은 뇌 조직까지 평형이라 같은 혈중 농도에서도 급성보다 독성이 크다."
pitfalls:
  - contrast: "혈중 농도가 같으면 독성도 같다?"
    point: "리튬은 조직(뇌)으로 천천히 분포한다. 급성 과량 직후에는 혈중 농도가 높아도 뇌 농도는 아직 낮고, 몇 주에 걸친 만성 축적은 뇌까지 평형이라 더 낮은 농도에서 중증 신경독성이 나온다 [[harrison-22: 470장 p.3715]]."
  - contrast: "투석이 끝나면 끝?"
    point: "투석은 혈중 리튬을 빨리 빼지만 조직에 남은 리튬이 다시 혈중으로 나와 농도가 반동해 오른다 [[harrison-22: 470장 p.3707]]. 투석 뒤 다시 재고 필요하면 반복한다."
  - contrast: "모든 중독에 활성탄?"
    point: "리튬은 이온화된 무기물이라 활성탄에 잘 흡착되지 않는다 [[harrison-22: 470장 p.3708]]. 위장관 제거가 필요하면 전장관 세척이다."
tables:
  - id: dialyzability
    title: "투석으로 잘 빠지는 독성 물질의 성질 — 리튬과 대조"
    role: comparison
    span: column
    section: "임상 판단으로 — 왜 투석이 듣는가"
    columns: ["성질(해리슨)", "리튬"]
    rows:
      - ["분자량 < 500 Da", "작은 1가 양이온(원자량 약 7)"]
      - ["물에 잘 녹는다", "체액에 녹아 있다"]
      - ["단백 결합이 낮다", "결합하지 않는다"]
      - ["분포용적 < 1 L/kg", "체액에 퍼지는 작은 용적"]
      - ["몸의 제거가 느리다", "콩팥 기능이 떨어지면 더 느려진다"]
    note: "왼쪽 칸 [[harrison-22: 470장 p.3709]]. 오른쪽 칸의 리튬 성질은 표준 약리(전공 교과서 미대조)."
checks:
  - q: "티아지드가 리튬 농도를 올리는 기전은?"
    a: "원위세뇨관 나트륨 재흡수를 막아 나트륨·용적이 줄면 근위세뇨관의 나트륨 재흡수가 보상적으로 늘고, 리튬도 나트륨과 함께 더 재흡수된다."
  - q: "리튬이 혈액투석으로 잘 제거되는 성질 셋은?"
    a: "작은 분자(이온), 단백 결합이 없음, 작은 분포용적."
  - q: "투석 뒤 리튬 농도를 다시 재는 이유는?"
    a: "조직에 남은 리튬이 혈중으로 재분포해 농도가 반동해 오르기 때문이다."
sources:
  - id: harrison-22
    org: "McGraw Hill"
    title: "Harrison's Principles of Internal Medicine, 22nd ed."
    kind: textbook
    year: 2025
    citation: "Loscalzo J, Fauci AS, Kasper DL, et al (eds). Harrison's Principles of Internal Medicine, 22e. 470장 Poisoning and Drug Overdose p.3703–3716"
    checked_at: 2026-11-24
    checked: "본문 대조(드라이브 22판 장별 문서 H22_470) — p.3704 표 470-1 「Slow distribution」에 리튬, p.3705 리튬이 낮은 음이온차의 원인, p.3707 체외 제거 뒤 조직에서 재분포해 혈중 농도 반동(예: 리튬), p.3708 이온화된 무기물(리튬 포함)은 활성탄에 잘 흡착되지 않음, p.3709 투석이 잘 되는 성질(< 500 Da·수용성·낮은 단백 결합·분포용적 < 1 L/kg·긴 반감기)과 리튬 중증 중독에서 투석 고려, p.3715 표의 리튬 행(이온 수송·Na,K-ATPase 간섭, 실조·근간대경련·뇌병증·신성 요붕증, 만성 중독이 급성보다 낮은 농도에서 독성, 투석 적응). 근위세뇨관의 나트륨 연동 재흡수와 티아지드·NSAID·ACE억제제 상호작용 기전은 이 장에 없어 표준 약리로 두었다(전공 교과서 미대조)"
    verified: text
variants:
  - id: v1
    flip: false
    changed: "핵심 변형 — 리튬 축적의 콩팥 기전(근위세뇨관 나트륨 연동 재흡수)을 묻는다"
    context: "리튬을 먹던 환자에서 이뇨제 시작 뒤 생긴 독성의 기전"
    stem: "A 58-year-old woman with bipolar disorder has taken lithium at a stable dose for 6 years with serum levels of 0.6–0.8 mEq/L. Three weeks ago hydrochlorothiazide was started for hypertension. She now has a coarse tremor, unsteady gait, and slurred speech. Her serum lithium level is 2.1 mEq/L, sodium is 136 mEq/L, and creatinine is 1.1 mg/dL. Which of the following best explains the rise in her lithium level?"
    choices: ["A. Inhibition of hepatic lithium metabolism", "B. Displacement of lithium from plasma protein binding sites", "C. Increased proximal tubular reabsorption of lithium along with sodium after volume contraction", "D. Increased gastrointestinal absorption of lithium", "E. Increased secretion of lithium by the distal tubule"]
    answer: "C"
    explanation: "Lithium is not metabolized or protein bound and leaves the body almost entirely through the kidney. The thiazide blocks distal sodium reabsorption; the resulting volume contraction makes the proximal tubule reabsorb more sodium, and lithium follows sodium along the same pathway, so lithium clearance falls and the level rises over weeks. Hepatic metabolism and protein displacement do not apply to lithium, and absorption is already nearly complete."
    kind: application
figures_none: 약동학 기전 — 영상 소견이 단서가 아니다
---

## 정상 — 나트륨처럼 걸러지고 재흡수된다
리튬은 작은 1가 양이온이다. 장에서 거의 다 흡수되고, 혈장 단백에 붙지 않으며, 대사되지 않는다. 사구체에서 자유롭게 걸러진 뒤 대부분 **근위세뇨관에서 나트륨과 같은 길로 재흡수**되고, 남은 것이 소변으로 나간다 — 몸 밖으로 나가는 길은 사실상 콩팥 하나다. 몸 안에서는 체액에 퍼지지만 세포 안·뇌로는 천천히 들어간다 [[harrison-22: 470장 p.3704]].

## 고장 — 나트륨이 모자라면 리튬을 붙잡는다
- **용적·나트륨 결핍**(구토·설사·발열·저염식): 근위세뇨관이 나트륨을 더 붙잡으면서 리튬도 함께 재흡수한다.
- **티아지드**: 원위세뇨관 나트륨 재흡수를 막아 용적이 줄면, 근위세뇨관 재흡수가 보상으로 늘어 리튬 청소율이 떨어진다.
- **NSAID · ACE억제제 · ARB**: 사구체 여과를 떨어뜨려(수입세동맥 확장 차단 · 수출세동맥 이완) 걸러지는 리튬 자체가 준다.
- **콩팥 기능 저하**: 유일한 배설 길이 좁아진다. 리튬 자체가 신성 요붕증을 일으켜 물을 잃으면 용적이 줄어 악순환이 된다 [[harrison-22: 470장 p.3715]].
- 이 고리들은 몇 주에 걸쳐 천천히 쌓이게 하므로, 뇌 조직 농도까지 혈중과 평형을 이룬다.

## 소견으로 — 뇌가 먼저 상한다
리튬은 세포막 이온 수송·Na⁺,K⁺-ATPase·아데닐산 고리화효소·신경전달물질 분비를 방해한다 [[harrison-22: 470장 p.3715]]. 그래서 오심·설사 다음에 실조·안진·과반사·근간대경련·무도무정위운동·뇌병증이, 중증이면 혼수·경련·부정맥이 오고, 지속되거나 영구적인 뇌병증·운동장애가 남을 수 있다 [[harrison-22: 470장 p.3715]].
- **만성 축적**은 뇌까지 평형이라 혈중 농도가 그리 높지 않아도 신경독성이 크다 — 독성은 만성 중독에서 급성보다 낮은 농도에서 생긴다 [[harrison-22: 470장 p.3715]].
- **급성 과량**은 처음에 혈중 농도가 높아도 뇌로의 분포가 늦어 위장 증상이 앞서고, 서방형이면 증상이 늦게 온다 [[harrison-22: 470장 p.3715]].
- 리튬은 혈중 음이온차를 낮게 만들 수 있다 [[harrison-22: 470장 p.3705]].

## 임상 판단으로 — 왜 투석이 듣는가
- 리튬은 투석이 잘 되는 성질(작은 분자 · 수용성 · 낮은 단백 결합 · 작은 분포용적)을 모두 갖췄다 [[harrison-22: 470장 p.3709]]. 그래서 중증 신경독성이나 콩팥 기능 저하로 스스로 못 내보낼 때 혈액투석이 가장 빠른 제거 수단이다 — 적응 기준은 임상 정리본에 둔다.
- 투석 뒤 조직의 리튬이 재분포해 혈중 농도가 반동하므로 다시 잰다 [[harrison-22: 470장 p.3707]].
- 활성탄은 리튬에 듣지 않는다 [[harrison-22: 470장 p.3708]]. 정맥 수액은 근위세뇨관 재흡수 자극(용적 결핍)을 풀어 배설을 돕는 보조다.

## 시험 쟁점 — 충돌·맥락·새 근거
- 해당 없음(대조: 해리슨 470장 p.3704~3715)
