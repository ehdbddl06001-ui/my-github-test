---
id: cn.physio.distal-rta.alpha-intercalated-h-secretion
type: concept
topic: Nephrology
see_also: [Physiology, Rheumatology]
date: 2026-11-03
updated: 2026-11-03
version: 1
outline: h55
confidence: medium
review_status: unreviewed
note_form: 2
title: "원위 신세관산증 — 산혈증에도 소변 pH 가 5.5 를 넘는다"
objective: "정상 음이온 차 대사산증에서 소변 음이온 차·소변 pH·혈청 칼륨으로 원위(1형) 신세관산증을 가려 집합관 H+ 분비 장애로 설명하고 근위(2형)·4형과 구별한다"
objective_kind: 기전
condition: 원위(1형) 신세관산증(distal renal tubular acidosis, type 1 RTA)
exams: [usmle, kmle]
summary:
  - "결론: 정상 음이온 차 산증 + 소변 음이온 차 양수 + 소변 pH > 5.5 + 저칼륨 = 원위(1형) 신세관산증."
  - "시험 단서: 신석회화·결석, 근력 저하(저칼륨), 쇼그렌병·암포테리신 B — distal (type 1) RTA."
  - "왜: 집합관이 H+ 를 내보내지 못해 산혈증에도 소변을 산성화하지 못하고 암모늄 배설이 낮다."
  - "근위(2형)는 혈청 중탄산이 낮아진 상태에서 소변 pH < 5.5 로 산성화된다 — 흔히 Fanconi(포도당뇨·인산뇨)."
  - "4형은 고칼륨혈증 — 알도스테론 결핍·저항, 고칼륨이 암모니아 생성을 억제한다."
pitfalls:
  - contrast: "근위(2형) vs 원위(1형) — 둘 다 저칼륨에 소변 pH 가 높을 수 있다?"
    point: "근위형의 소변 pH 는 혈청 중탄산이 낮아진 상태에서는 5.5 아래로 내려가고, 알칼리를 투여할 때만 5.5 를 넘는다. 이미 산혈증(중탄산 낮음)인데 소변 pH 가 5.5 를 넘으면 원위형이다. 신석회화·결석도 원위형의 특징이다(저구연산뇨·고칼슘뇨)."
    exception: "근위형은 흔히 포도당뇨·아미노산뇨·인산뇨(Fanconi)를 동반한다 — 정상 혈당의 포도당뇨가 보이면 근위형 쪽이다."
    cites: ["harrison-22: 58장 p.372"]
    covers: ["usmle-2026-0236:A"]
  - contrast: "4형 vs 1형"
    point: "4형은 칼륨·산 분비가 함께 떨어져 GFR 저하에 비해 고칼륨혈증이 크다. 칼륨이 낮으면 4형이 아니다."
    cites: ["harrison-22: 58장 p.372"]
  - contrast: "설사 vs 신세관산증 — 소변 pH 가 6 을 넘으면 신장 탓?"
    point: "설사에서도 산혈증·저칼륨이 암모늄 생성을 늘려 소변 pH 가 6 을 넘을 수 있다. 소변 음이온 차가 음수(암모늄 많음)면 위장관, 양수(암모늄 적음)면 신세관이다."
    exception: "소변 음이온 차는 실제 소변 암모늄과의 상관이 약하다는 연구가 있다 — 가능하면 소변 암모늄을 잰다."
    cites: ["harrison-22: 58장 p.372"]
tables:
  - id: nagma
    section: "가르는 소견 — 소변 음이온 차·소변 pH·칼륨"
    title: "정상 음이온 차 대사산증 — 어디서 산이 남나"
    role: differential
    span: column
    columns: ["원인", "소변 음이온 차·pH", "칼륨·동반 소견"]
    rows:
      - ["설사(위장관 중탄산 손실)", "음수(암모늄↑), pH 대개 > 6 [[harrison-22: 58장 p.372]]", "저칼륨, 설사 병력"]
      - ["원위(1형) 신세관산증", "양수(암모늄↓), 산혈증에도 pH > 5.5 [[harrison-22: 58장 p.372]]", "저칼륨, 저구연산뇨·고칼슘뇨 → 결석·신석회화·뼈 질환 [[harrison-22: 58장 p.372]]"]
      - ["근위(2형) 신세관산증", "중탄산 낮을 때 pH < 5.5, 알칼리 투여 시 > 5.5 [[harrison-22: 58장 p.372]]", "포도당뇨·아미노산뇨·인산뇨(Fanconi), 알칼리 치료 중 저칼륨 [[harrison-22: 58장 p.372]]"]
      - ["4형(전반적 원위 네프론 장애)", "암모늄 배설 늘 감소 [[harrison-22: 58장 p.372]]", "GFR 에 비해 큰 고칼륨, 당뇨병성 신증·폐쇄성 요로병증·간질 질환 [[harrison-22: 58장 p.372]]"]
criteria:
  - id: drta
    name: 원위(1형) 신세관산증의 특징
    kind: 진단 기준
    population: "정상 음이온 차 대사산증"
    statement: "저칼륨혈증, 정상 음이온 차 대사산증, 낮은 소변 암모늄 배설(소변 음이온 차 양수), 그 산혈증에 맞지 않게 높은 소변 pH(> 5.5). 대부분 저구연산뇨·고칼슘뇨가 있어 신결석·신석회화·뼈 질환이 흔하다 [[harrison-22: 58장 p.372]]"
    exceptions: "약물(암포테리신 B·이포스파미드)과 유전 원인이 있다 [[harrison-22: 58장 p.372]]. 쇼그렌병의 간질 신염이 신세관 기능 장애와 산증을 일으키고, 치료하지 않은 산증은 신석회화로 갈 수 있다 [[harrison-22: 373장 p.2877]]"
    source: harrison-22
    basis: current
    exams: [usmle, kmle]
  - id: uag
    name: 소변 음이온 차
    kind: 계산
    population: "정상 음이온 차 대사산증"
    statement: "소변 음이온 차 = [Na+ + K+]u − [Cl−]u. 음수면 소변 암모늄이 적절히 늘어 신장 밖 원인, 양수면 암모늄이 낮아 신세관 원인을 시사한다 [[harrison-22: 58장 p.372]]"
    exceptions: "계산값과 실제 소변 암모늄의 상관이 약하다는 연구가 있어 소변 암모늄 직접 측정을 권한다 [[harrison-22: 58장 p.372]]"
    source: harrison-22
    basis: current
    exams: [usmle, kmle]
  - id: drta-tx
    name: 원위 신세관산증의 치료
    kind: 치료 권고
    population: "원위(1형) 신세관산증"
    statement: "먼저 저칼륨혈증을 교정하고, 그 뒤 구연산 나트륨이나 NaHCO3 로 혈청 중탄산을 24~26 meq/L 로 유지한다 — 결석 빈도 감소·골밀도 개선·성장 회복·신기능 보존 [[harrison-22: 58장 p.373]]"
    exceptions: "근위형은 알칼리가 소변 중탄산·칼륨 배설을 늘려 칼륨 보충이 거의 늘 필요하다 [[harrison-22: 58장 p.373]]"
    source: harrison-22
    basis: current
    exams: [usmle, kmle]
sources:
  - id: harrison-22
    org: "McGraw Hill"
    title: "Harrison's Principles of Internal Medicine, 22nd ed. — Chapter 58: Acidosis and Alkalosis; Chapter 373: Sjögren's Disease"
    kind: textbook
    year: 2025
    citation: "Harrison's Principles of Internal Medicine, 22e. 58장 p.367, 372–373; 373장 p.2877–2879"
    checked_at: 2026-11-03
    checked: "드라이브 22판 장별 문서 H22_58·H22_373 본문 대조 — Winter 식 Paco2 = 1.5×HCO3 + 8 ± 2(58장 p.367) · 정상 음이온 차 산증은 Cl·HCO3 상호 변화, 설사에서 소변 pH 대개 > 6(암모늄↑), 소변 음이온 차 정의·해석·상관 한계, 근위형(Fanconi, 중탄산 낮을 때 pH < 5.5·알칼리 시 > 5.5, 알칼리 치료 시 저칼륨), 원위형 특징(저칼륨·정상 음이온 차·암모늄↓·pH > 5.5·저구연산뇨·고칼슘뇨·결석·신석회화·뼈 질환), 4형(고칼륨 불균형, 암모늄 감소), 표 58-5 약물 원인(암포테리신 B·이포스파미드)(58장 p.372) · 치료: 원위형 칼륨 먼저 교정 뒤 알칼리로 HCO3 24–26, 근위형 칼륨 보충, 4형 고칼륨이 암모니아 생성 억제(58장 p.373) · 쇼그렌병 간질 신염·신세관 기능 장애 ± 산증·치료 안 한 산증의 신석회화(373장 p.2877), 신세관산증 증상이 쇼그렌병을 의심할 단서(373장 p.2878), 신세관산증 환자에 경구 NaHCO3(373장 p.2879). 집합관 α-사이세포 H+-ATPase 라는 세포 수준 기전은 이 두 장에서 확인하지 않았다(표 58-5 의 유전자 설명은 대조에 쓰지 않음)"
    verified: text
diagram:
  title: "정상 음이온 차 대사산증 — 어느 신세관인가"
  nodes:
    - {id: start, kind: start, text: "정상 음이온 차 대사산증"}
    - {id: uag, kind: decision, text: "소변 음이온 차가 양수인가?"}
    - {id: calc, kind: info, text: "소변 Na·K·Cl 로 음이온 차 계산"}
    - {id: gi, kind: end, text: "신장 밖 원인 — 설사 등 위장관 손실"}
    - {id: k, kind: decision, text: "혈청 칼륨이 높은가?"}
    - {id: type4, kind: end, text: "4형 — 알도스테론 결핍·저항"}
    - {id: uph, kind: decision, text: "산혈증에서 소변 pH > 5.5 인가?"}
    - {id: distal, kind: end, text: "원위(1형) — 집합관 H+ 분비 장애"}
    - {id: prox, kind: end, text: "근위(2형) — 중탄산 재흡수 장애"}
  edges:
    - {from: start, to: uag}
    - {from: uag, to: k, label: "양수"}
    - {from: uag, to: gi, label: "음수"}
    - {from: uag, to: calc, label: "모름"}
    - {from: calc, to: k, label: "양수"}
    - {from: calc, to: gi, label: "음수"}
    - {from: k, to: type4, label: "높음"}
    - {from: k, to: uph, label: "낮음"}
    - {from: uph, to: distal, label: "예"}
    - {from: uph, to: prox, label: "아니오"}
diagram_notes:
  - "근위형은 흔히 포도당뇨·아미노산뇨·인산뇨(Fanconi)를 동반한다 — 소변 음이온 차만으로 원위형과 늘 갈리지는 않는다 [[harrison-22: 58장 p.372]]."
  - "원위형의 신결석·신석회화는 저구연산뇨·고칼슘뇨 때문이다 [[harrison-22: 58장 p.372]]."
  - "원인: 쇼그렌병(간질 신염) [[harrison-22: 373장 p.2877]], 약물(암포테리신 B·이포스파미드) [[harrison-22: 58장 p.372]]."
  - "호흡 보상 확인: 예상 Paco2 = 1.5 × HCO3 + 8 ± 2(Winter 식) [[harrison-22: 58장 p.367]]."
checks:
  - q: "중탄산 15, 음이온 차 9, 소변 음이온 차 +29, 소변 pH 6.6, 칼륨 2.9. 어느 신세관산증인가?"
    a: "원위(1형). 산혈증인데 소변을 산성화하지 못하고(pH > 5.5) 암모늄 배설이 낮으며(음이온 차 양수) 칼륨이 낮다."
  - q: "근위형도 소변 pH 가 높을 수 있는데 원위형과 무엇으로 가르나?"
    a: "혈청 중탄산이 이미 낮을 때의 소변 pH. 근위형은 그때 5.5 아래로 산성화되고, 알칼리를 줄 때만 5.5 를 넘는다."
variants:
  - id: v1
    of: usmle-2026-0236
    flip: true
    changed: "결석·신수질 석회화·쇼그렌병·산혈증에도 소변 pH 6.6·포도당뇨 없음 → 다발골수종 경쇄·정상 혈당의 포도당뇨·저인산혈증·아미노산뇨·산혈증에서 소변 pH 5.1 ⇒ 정답이 원위 H+ 분비 장애에서 근위 중탄산 재흡수 감소로"
    context: "같은 정상 음이온 차 산증, 원인과 소변 소견을 바꾼 변형"
    stem: "A 63-year-old man comes to the physician because of fatigue and low back pain for 4 months. He has not had vomiting or diarrhea and takes no medications. Examination shows tenderness over the lumbar spine. Serum studies show sodium 138 mEq/L, potassium 3.1 mEq/L, chloride 113 mEq/L, bicarbonate 16 mEq/L, glucose 94 mg/dL, phosphorus 1.9 mg/dL and creatinine 1.1 mg/dL. Arterial pH is 7.32. Urinalysis shows pH 5.1 and 2+ glucose, and urine amino acids are increased. Serum protein electrophoresis shows a monoclonal spike, and urine immunofixation shows free κ light chains. An x-ray of the abdomen shows no renal calcifications. Which of the following best explains his acid-base disturbance?"
    choices: ["A. Decreased bicarbonate reabsorption in the proximal tubule", "B. Impaired hydrogen ion secretion by α-intercalated cells of the collecting duct", "C. Reduced aldosterone effect on the cortical collecting duct", "D. Loss of bicarbonate from the gastrointestinal tract", "E. Accumulation of unmeasured organic acids in the plasma"]
    answer: "A"
    explanation: "The anion gap is normal (138 − 113 − 16 = 9). With bicarbonate already low, he can acidify the urine to pH 5.1, so distal H+ secretion is intact. Glucosuria with a normal serum glucose, hypophosphatemia and aminoaciduria indicate generalized proximal tubular dysfunction (Fanconi syndrome) from light chains — proximal (type 2) RTA with reduced bicarbonate reabsorption. Potassium is low, so this is not type 4."
    kind: application
  - id: v2
    of: usmle-2026-0236
    flip: false
    changed: "41세 여자·쇼그렌병·결석 → 29세 여자·암포테리신 B 치료 중, 결석 대신 신석회화만, 수치를 바꿈 ⇒ 정상 음이온 차·소변 음이온 차 양수·산혈증에도 소변 pH > 5.5·저칼륨이라는 결정 단서는 같아 답은 그대로 원위 H+ 분비 장애"
    context: "겉모습만 바꾼 변형"
    stem: "A 29-year-old woman is being treated in the hospital for disseminated cryptococcal infection. On day 12 of amphotericin B therapy, she reports leg weakness. She has not had vomiting or diarrhea. Serum studies show sodium 140 mEq/L, potassium 2.8 mEq/L, chloride 116 mEq/L, bicarbonate 16 mEq/L, glucose 101 mg/dL, phosphorus 3.4 mg/dL and creatinine 1.0 mg/dL. Arterial pH is 7.32. Urine studies show pH 6.4, sodium 50 mEq/L, potassium 35 mEq/L, chloride 55 mEq/L, and no glucose. Which of the following best explains her acid-base disturbance?"
    choices: ["A. Loss of bicarbonate from the gastrointestinal tract", "B. Reduced aldosterone effect on the cortical collecting duct", "C. Decreased bicarbonate reabsorption in the proximal tubule", "D. Impaired hydrogen ion secretion by α-intercalated cells of the collecting duct", "E. Accumulation of unmeasured organic acids in the plasma"]
    answer: "D"
    explanation: "The cause and patient differ, but the deciding clues are the same: normal anion gap (140 − 116 − 16 = 8), positive urine anion gap (50 + 35 − 55 = +30, low ammonium), urine pH above 5.5 despite acidemia, and hypokalemia. This is distal (type 1) RTA; amphotericin B is a recognized drug cause. No glucosuria and a normal phosphorus argue against proximal RTA, and the low potassium argues against type 4."
    kind: application
figures_none: "수치(음이온 차·소변 pH·칼륨)로 판단하는 기전 목표 — 신석회화 영상은 정답을 가르는 단서가 아니다"
---

## 기전 — 집합관이 산을 내보내지 못하면
콩팥은 매일 생기는 비휘발성 산을 근위세관의 중탄산 재흡수와 원위 네프론의 H+ 분비(적정산·암모늄으로 배설)로 처리한다. 원위(1형)에서는 집합관의 H+ 분비가 떨어져 산혈증인데도 소변을 산성화하지 못하고(pH > 5.5), H+ 를 가둘 암모늄 배설도 낮다(소변 음이온 차 양수) [[harrison-22: 58장 p.372]]. H+ 를 내보내는 세포가 집합관의 α-사이세포(H+-ATPase)라는 세포 수준의 설명은 해리슨 이 장에서 확인하지 않았다. 대부분 저구연산뇨·고칼슘뇨가 함께 생겨 알칼리 소변에서 인산칼슘이 가라앉아 신결석·신석회화·뼈 질환이 흔하고, 저칼륨혈증이 근력 저하를 낸다 [[harrison-22: 58장 p.372]].

## 가르는 소견 — 소변 음이온 차·소변 pH·칼륨
- **음이온 차가 정상인가**: 정상 음이온 차 산증에서는 Cl 상승이 HCO3 감소와 거의 같다 — 어긋나면 혼합 장애를 생각한다 [[harrison-22: 58장 p.372]].
- **위장관인가 콩팥인가**: 소변 음이온 차 [Na+ + K+]u − [Cl−]u 가 음수면 암모늄 배설이 늘어 위장관, 양수면 신세관이다. 설사에서도 소변 pH 는 대개 6 을 넘으므로 pH 만으로 가르지 않는다 [[harrison-22: 58장 p.372]].
- **어느 신세관인가**: 칼륨이 높으면 4형, 낮으면 소변 pH 를 본다 — 중탄산이 이미 낮은데 pH > 5.5 면 원위, < 5.5 면 근위 [[harrison-22: 58장 p.372]].
- 호흡 보상은 Winter 식(1.5 × HCO3 + 8 ± 2)으로 확인한다 [[harrison-22: 58장 p.367]].

## 권고와 예외
- 원위형은 먼저 저칼륨을 교정한 뒤 알칼리로 중탄산 24~26 meq/L 를 유지하면 결석이 줄고 골밀도·성장·신기능이 지켜진다 [[harrison-22: 58장 p.373]].
- 쇼그렌병은 간질 신염으로 신세관 기능 장애와 산증을 일으킬 수 있고, 신세관산증 증상은 쇼그렌병을 의심할 단서다. 신세관산증 환자에게 경구 NaHCO3 를 준다 [[harrison-22: 373장 p.2877]] [[harrison-22: 373장 p.2878]] [[harrison-22: 373장 p.2879]].
- 약물(암포테리신 B·이포스파미드)도 원위형을 일으킨다 [[harrison-22: 58장 p.372]].

## 시험 쟁점 — 충돌·맥락·새 근거
- **Z1 새 근거 · 소변 음이온 차의 신뢰도** — 시험 기준: 소변 음이온 차 양수 = 암모늄 배설 낮음 = 신세관 원인 [[harrison-22: 58장 p.372]] / 다른 기준: 계산값과 실제 소변 암모늄의 상관이 약해 소변 암모늄을 직접 재자는 제안 [[harrison-22: 58장 p.372]] / 왜 다른가: 소변에 다른 음이온(케톤 등)이 많으면 계산이 암모늄을 반영하지 못한다(원문 미대조) / 시험에서는: KMLE · USMLE 모두 소변 음이온 차 해석을 그대로 묻는다.
