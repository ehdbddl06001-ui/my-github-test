---
id: cn.physio.hypoxemia.shunt-oxygen-unresponsive
type: concept
topic: Physiology
see_also: [Pulmonology, Anesthesiology]
date: 2026-11-24
updated: 2026-11-24
version: 1
outline: physio.respiratory   # 생리학 책 「호흡 — 환기·가스 교환·조절」
layer: basic            # 기초 정리본 — 임상 정리본의 roots 가 가리키는 기전 단위
discipline: physiology
system: respiratory
objective_kind: 기전
textbook_check: pending
confidence: medium
review_status: unreviewed
note_form: 2
title: "저산소혈증 기전 — 산소에 안 오르면 션트"
objective: "PaCO2 와 폐포-동맥 산소분압 차이(A-a 차이)로 저산소혈증의 다섯 기전을 나누고, 100 % 산소 흡입에 PaO2 가 거의 오르지 않는 것이 환기 없는 폐포를 지나는 혈액(션트)의 표지인 이유를 설명한다"
condition: 저산소혈증(hypoxemia)의 기전 감별 — 폐내 션트(intrapulmonary shunt), 무기폐
exams: [usmle, kmle]
summary:
  - "결론: A-a 차이가 크고 100 % 산소에도 PaO2 가 거의 오르지 않으면 션트(shunt)다."
  - "시험 단서: 수술 뒤 얕은 호흡 · 한 엽의 균질 음영과 용적 감소(atelectasis), PaCO2 정상~낮음, 100 % O2 뒤 PaO2 < 100 mm Hg."
  - "왜: 환기가 전혀 없는 폐포를 지난 혈액은 흡입 산소를 만나지 못한 채 동맥혈에 섞인다."
  - "낮은 V/Q · 확산 장애 · 환기 저하는 환기가 남아 있어 100 % 산소 몇 분이면 PaO2 가 크게 오른다."
pitfalls:
  - contrast: "확산 장애 — 「막이 두꺼우면 산소가 못 건넌다」 vs 산소 농도를 올리면"
    point: "확산 장애는 폐포에 환기가 되는 상태라, 100 % 산소로 폐포 PO2 를 크게 올리면 두꺼운 막을 건너는 압력 차이가 커져 PaO2 가 오른다. 이 환자는 산소에도 PaO2 가 78 mm Hg 에 그쳤고, 수술 뒤 하루 만에 막이 두꺼워질 병(간질성 폐질환)도 없으며 영상은 용적이 줄어든 엽 — 무기폐다. 확산 장애는 해리슨이 중심 청색증의 원인 목록에 올리는 기전이다 [[harrison-22: 42장 p.278]]."
    exception: "운동처럼 모세혈관 통과 시간이 짧아지면 확산 장애의 저산소혈증이 드러난다 — 안정 시 PaO2 로는 잘 안 보인다."
    cites: ["harrison-22"]
    covers: ["usmle-2026-0292:B"]
  - contrast: "낮은 V/Q vs 션트 — 둘 다 A-a 차이가 크다"
    point: "가장 흔한 저산소증은 환기가 부족한 폐포의 관류(V/Q 불균형)이고 100 % 산소 몇 분이면 교정된다. 무기폐처럼 환기가 아예 없는 폐포의 관류(폐내 우좌 션트)는 100 % 산소로 일부만 교정된다 [[harrison-22: 42장 p.277]]."
    cites: ["harrison-22"]
    covers: ["usmle-2026-0292:D"]
  - contrast: "통증으로 얕게 숨쉰다 = 전체 폐포 환기 저하?"
    point: "전체 환기 저하는 PaCO2 가 오르는 저산소혈증이다 [[harrison-22: 42장 p.277]]. 이 환자는 PaCO2 34 mm Hg 로 오히려 과환기이고 A-a 차이가 크다 — 얕은 호흡은 전체 환기가 아니라 한 엽을 닫아(무기폐) 문제를 만들었다."
    cites: ["harrison-22"]
    covers: ["usmle-2026-0292:A"]
tables:
  - id: mechanisms
    section: "고장 — 다섯 기전이 PaO2 를 낮추는 방식"
    title: "저산소혈증의 기전 — PaCO2 · A-a 차이 · 100 % 산소 반응"
    role: comparison
    span: full
    columns: ["기전", "PaCO2", "A-a 차이", "100 % O2", "예"]
    rows:
      - ["흡입 산소 분압 저하", "낮음(과환기)", "정상", "교정", "고지대 [[harrison-22: 42장 p.277]]"]
      - ["폐포 환기 저하", "높음", "정상", "교정", "아편유사제 과량 · 신경근 질환 [[harrison-22: 42장 p.277]]"]
      - ["V/Q 불균형(낮은 V/Q)", "정상~낮음", "증가", "교정", "COPD · 천식 · 폐렴 일부 [[harrison-22: 42장 p.277]]"]
      - ["확산 장애", "정상~낮음", "증가", "교정", "간질성 폐질환 [[harrison-22: 42장 p.278]]"]
      - ["션트(V/Q = 0)", "정상~낮음", "증가", "거의 안 오름", "무기폐 · 폐동정맥루 · 청색증 선천 심질환 [[harrison-22: 42장 p.277]]"]
    note: "흡입 산소 저하 · 환기 저하 · 낮은 V/Q · 션트의 산소 반응은 해리슨 42장이 적는다. 확산 장애의 산소 반응은 해리슨에 없는 생리학 교과서 서술이다(전공 교과서 미대조)."
checks:
  - q: "해수면에서 PaO2 56 · PaCO2 34 mm Hg 다. A-a 차이는 얼마이고 무엇을 뜻하나?"
    a: "PAO2 ≈ 0.21 × (760 − 47) − 34/0.8 ≈ 150 − 43 ≈ 107 mm Hg 라 A-a 차이는 약 51 mm Hg 로 크다. 흡입 산소 저하나 전체 환기 저하가 아니라 폐 안의 가스 교환 장애(V/Q 불균형 · 확산 · 션트)다."
  - q: "션트에서 100 % 산소가 PaO2 를 거의 올리지 못하는 이유는?"
    a: "환기가 없는 폐포를 지난 혈액은 흡입 산소를 만나지 못한다. 정상 폐포를 지난 혈액은 이미 거의 포화되어 산소를 더 실을 수 없으므로, 섞인 동맥혈의 PaO2 는 조금만 오른다."
sources:
  - id: harrison-22
    org: "McGraw Hill"
    title: "Harrison's Principles of Internal Medicine, 22nd ed."
    kind: textbook
    year: 2025
    citation: "Loscalzo J, Fauci AS, Kasper DL, et al (eds). Harrison's Principles of Internal Medicine, 22e. 42장 Hypoxia and Cyanosis(Loscalzo J) p.276–279"
    checked_at: 2026-11-24
    checked: "본문 대조(드라이브 문서 H22_042) — p.276–277 저산소 폐혈관 수축이 환기가 나쁜 곳의 혈액을 잘 환기되는 곳으로 돌린다(V/Q 불균형을 줄임); p.277 가장 흔한 호흡성 저산소증은 환기가 나쁜 폐포의 관류(V/Q 불균형), 환기 저하는 PaCO2 상승, 이 둘은 100 % O2 몇 분으로 대개 교정, 환기 없는 폐 부분의 관류(무기폐 · 폐동정맥 연결)인 폐내 우좌 션트는 FiO2 100 % 로 일부만 교정, 고지대 FiO2 저하는 과환기로 PaCO2 저하, 폐외 우좌 션트도 100 % O2 로 정상화 안 됨; p.278 표 42-1 중심 청색증 원인에 폐포 환기 저하 · V/Q 불균일 · 확산 장애 · 해부학적 션트"
    verified: text
variants:
  - id: v1
    of: usmle-2026-0292
    flip: true
    changed: "100% O2 for 20 minutes raises PaO2 only to 78 → to 540 mm Hg, and the x-ray shows patchy basal opacities with retained secretions rather than a collapsed lobe — the lung units are still partly ventilated, so the answer moves from shunt to low V/Q units"
    context: "Postoperative hypoxemia that corrects with 100% oxygen"
    stem: "A 63-year-old woman develops shortness of breath on the second day after an open cholecystectomy. Incisional pain has made her reluctant to cough, and she has a moist cough with thick sputum she cannot bring up. She has never smoked. The hospital is at sea level. Temperature is 37.4 °C (99.3 °F), pulse is 98/min, respirations are 24/min, and oxygen saturation is 89% on room air. Coarse crackles are heard over both lung bases; there is no dullness to percussion. Arterial blood gas on room air shows pH 7.46, PCO2 35 mm Hg, and PO2 58 mm Hg. After 20 minutes of 100% oxygen through a tight-fitting reservoir mask, PO2 is 540 mm Hg and PCO2 is 36 mm Hg. A chest x-ray shows patchy opacities at both bases without volume loss. Which of the following is the most likely primary mechanism of this patient's hypoxemia?"
    choices: ["A. Reduced overall alveolar ventilation that raises alveolar carbon dioxide", "B. Impaired diffusion of oxygen across a thickened alveolar-capillary membrane", "C. Reduced partial pressure of oxygen in the inspired air", "D. Lung units whose ventilation is reduced relative to their perfusion", "E. Blood flow through alveoli that are perfused but not ventilated"]
    answer: "D"
    explanation: "The A-a gradient is wide (PAO2 about 106 vs PaO2 58) with a normal PCO2, so the problem is gas exchange within the lung, not hypoventilation (A) or low inspired oxygen (C). Unlike the original item, 100% oxygen raised PaO2 to 540 mm Hg: the poorly ventilated units still receive some ventilation, nitrogen is washed out, and their alveolar PO2 climbs. That response marks low V/Q units, here from secretions partly blocking small airways. A true shunt (E) would barely respond. Diffusion impairment (B) also corrects with oxygen but needs a thickened membrane that a 2-day postoperative patient does not have."
    kind: application
  - id: v2
    of: usmle-2026-0292
    flip: false
    changed: "postoperative atelectasis in a 67-year-old man → lobar pneumococcal pneumonia with dense consolidation in a 49-year-old woman, presented with different labs order — alveoli filled with exudate are still perfused but not ventilated, and PaO2 barely rises on 100% oxygen, so the answer stays shunt"
    context: "Dense lobar consolidation with oxygen-refractory hypoxemia"
    stem: "A 49-year-old woman comes to the emergency department because of 3 days of fever, productive cough with rust-colored sputum, and right-sided pleuritic chest pain. She has no history of lung disease. The hospital is at sea level. Temperature is 39.2 °C (102.6 °F), pulse is 112/min, respirations are 28/min, and oxygen saturation is 86% on room air. There is bronchial breathing with increased tactile fremitus over the right lower chest. A chest x-ray shows dense consolidation of the entire right lower lobe with air bronchograms. Arterial blood gas on room air shows pH 7.48, PCO2 32 mm Hg, and PO2 52 mm Hg; after 20 minutes of 100% oxygen through a tight-fitting reservoir mask, PO2 is 74 mm Hg. Which of the following best explains the response of her arterial PO2 to 100% oxygen?"
    choices: ["A. Reduced overall alveolar ventilation that raises alveolar carbon dioxide", "B. Impaired diffusion of oxygen across a thickened alveolar-capillary membrane", "C. Reduced partial pressure of oxygen in the inspired air", "D. Lung units whose ventilation is reduced relative to their perfusion", "E. Blood flow through alveoli that are perfused but not ventilated"]
    answer: "E"
    explanation: "The setting changes from postoperative collapse to pneumonia, but the decisive finding is the same: a wide A-a gradient with low PCO2, and PaO2 that rises only from 52 to 74 mm Hg on 100% oxygen. Alveoli filled with exudate receive blood but no gas, so that blood never meets the inspired oxygen — an intrapulmonary shunt. Low V/Q units (D) and diffusion impairment (B) would correct, hypoventilation (A) would raise PCO2, and low inspired oxygen (C) is excluded at sea level."
    kind: application
figures_none: "기전 목표 — 혈액가스 수치와 산소 반응으로 가른다(흉부 X선 그림은 임상 정리본 몫)"
---

## 정상 — 폐포 산소와 A-a 차이
동맥혈 산소분압(PaO2)은 폐포 산소분압(PAO2)을 넘지 못한다. 폐포 기체식 PAO2 = FiO2 × (대기압 − 47) − PaCO2/0.8 로, 해수면 실내 공기에서 약 150 − PaCO2/0.8 이다. 정상 폐는 폐포와 동맥 사이 차이(A-a 차이)가 작다. 환기와 관류가 고르지 않은 곳이 생기면 저산소 폐혈관 수축이 환기가 나쁜 곳의 혈액을 잘 환기되는 곳으로 돌려 불균형을 줄인다 [[harrison-22: 42장 p.277]].

## 고장 — 다섯 기전이 PaO2 를 낮추는 방식
- **폐포에 산소가 덜 들어온다** — 흡입 산소 분압 저하(고지대)와 전체 폐포 환기 저하. 폐 자체는 정상이라 A-a 차이가 정상이다. 환기 저하는 PaCO2 가 오르고, 고지대는 과환기로 PaCO2 가 내려간다 [[harrison-22: 42장 p.277]].
- **폐 안에서 교환이 어긋난다** — A-a 차이가 커진다. 환기가 부족한 폐포의 관류(낮은 V/Q)가 가장 흔하고 [[harrison-22: 42장 p.277]], 두꺼워진 막을 건너는 확산 장애 [[harrison-22: 42장 p.278]], 환기가 전혀 없는 폐포의 관류(션트, V/Q = 0)가 있다 — 무기폐 · 폐동정맥 연결 [[harrison-22: 42장 p.277]].

## 소견으로 — 100 % 산소 반응이 가르는 이유
- 낮은 V/Q 와 환기 저하는 100 % 산소 몇 분으로 대개 교정된다 [[harrison-22: 42장 p.277]] — 환기가 조금이라도 있으면 질소가 씻겨 나가고 폐포 PO2 가 수백 mm Hg 로 오른다.
- 션트는 FiO2 100 % 로 일부만 교정된다 [[harrison-22: 42장 p.277]]. 환기 없는 폐포를 지난 혈액은 산소를 못 만나고, 정상 폐포를 지난 혈액은 이미 포화되어 산소를 더 실을 수 없다. 폐 밖의 우좌 션트(청색증 선천 심질환)도 같다 [[harrison-22: 42장 p.277]].
- 션트 환자도 저산소증이 호흡을 자극하므로 PaCO2 는 정상이거나 낮다.

## 임상 판단으로 — 이 기전이 가르는 선택
- 수술 뒤 통증으로 깊게 숨쉬지 못하면 한 엽이 닫혀(무기폐) 션트가 생긴다 — 산소 농도를 올리기보다 기침 · 심호흡 · 흡인으로 폐포를 다시 연다.
- 산소에 잘 오르는 저산소혈증(낮은 V/Q)은 산소 투여 자체가 치료가 된다.

## 시험 쟁점 — 충돌·맥락·새 근거
- **Z1 맥락 · 확산 장애의 산소 반응** — 시험 기준: 확산 장애는 환기가 되는 폐포라 100 % 산소로 교정된다(생리학 교과서 서술 — 전공 교과서 미대조) / 다른 기준: 해리슨 42장은 확산 장애를 중심 청색증의 원인 목록에만 올리고 산소 반응을 적지 않는다 [[harrison-22: 42장 p.278]] / 왜 다른가: 임상 교과서는 흔한 두 기전(V/Q · 환기 저하)과 션트만 산소 반응으로 대조한다 / 시험에서는: USMLE · KMLE 모두 「100 % 산소에 거의 안 오름」은 션트 하나만 가리킨다.
