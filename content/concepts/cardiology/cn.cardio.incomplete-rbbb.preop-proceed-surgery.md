---
id: cn.cardio.incomplete-rbbb.preop-proceed-surgery
type: concept
topic: Cardiology
see_also: [General Surgery]
date: 2026-09-28
updated: 2026-09-28
version: 2
outline: h240           # 기본틀 슬롯 — 해리슨 21판 240장 Electrocardiography(수술 전 평가는 480장도 대조)
confidence: medium
review_status: unreviewed
note_form: 2
title: "수술 전 불완전 우각차단 — 증상·운동능력이 검사를 정한다"
objective: "수술 전 심전도의 불완전 우각차단에서 증상·운동능력(4 METs)·S2 분열·심잡음으로 추가 심장 검사 없이 수술할지를 정한다"
objective_kind: 다음 처치
condition: 불완전 우각차단(incomplete right bundle branch block)의 수술 전 평가
exams: [kmle, usmle]
summary:
  - "결론: 증상 없고 4 METs 이상, S2 생리적 분열·심잡음 없음이면 불완전 우각차단만으로 검사하지 않고 수술한다."
  - "시험 단서: 수술 전 심전도 V1 rSR′·QRS < 120 ms(incomplete RBBB) + 계단 두 층을 증상 없이 오른다."
  - "왜: 검사는 결과가 처치를 바꿀 때만 한다 — 운동능력이 충분하면 비침습 검사가 계획을 바꾸지 않는다."
  - "검사로 가는 조건: 고정 분열 S2·유출 심잡음(심방중격결손 → 심초음파), 실신·두근거림(→ 심전도 감시)."
pitfalls:
  - contrast: "24시간 활동 심전도 감시 vs 수술 진행"
    point: "활동 심전도(Holter)는 간헐적 부정맥·전도 차단을 찾는 검사라 두근거림·실신이 있을 때 결과가 처치를 바꾼다. 증상 없는 고정된 불완전 우각차단은 찾을 간헐적 사건이 없다."
    exception: "불완전 우각차단에 설명되지 않는 실신이 겹치면 감시가 다음 단계다."
    covers: ["imaging-2026-0135:E"]
  - contrast: "심초음파 vs 수술 진행 — 「우각차단 = 구조 이상?」"
    point: "불완전 우각차단은 심방중격결손(우심실 용적 과부하)의 단서일 수 있지만 [[harrison-21: 240장 p.1826]], 고정 분열 S2·유출 심잡음이 없으면 가능성이 낮아 심초음파가 계획을 바꾸지 않는다."
  - contrast: "부하검사 vs 수술 진행 — 「고위험 수술이면 부하검사?」"
    point: "위험이 높은 수술이어도 운동능력이 4 METs 이상이면 비침습 검사 없이 수술한다. 부하검사는 운동능력이 낮거나 모를 때, 결과가 처치를 바꿀 때만 [[harrison-21: 480장 p.3769]]."
tables:
  - id: next-step
    section: "선택 — 검사가 필요한 조건"
    title: "수술 전 불완전 우각차단 — 다음 단계를 바꾸는 소견"
    role: treatment
    span: column
    columns: ["소견", "다음 단계"]
    rows:
      - ["증상 없음 + ≥ 4 METs + 생리적 S2 분열·심잡음 없음", "추가 검사 없이 수술 [[harrison-21: 480장 p.3769]]"]
      - ["고정 분열 S2 + 좌측 흉골상연 유출 심잡음·우축편위", "경흉부 심초음파 — 심방중격결손 확인 [[harrison-21: 240장 p.1826]]"]
      - ["실신·두근거림", "활동 심전도 감시·전도계 평가"]
      - ["운동능력 < 4 METs 또는 모름 + 위험 높은 수술", "결과가 처치를 바꿀 때만 약물 부하검사 [[harrison-21: 480장 p.3769–3770]]"]
      - ["V1–V2 ST 올라감이 동반된 우각차단 모양", "Brugada 양상 감별 [[harrison-21: 240장 p.1828]]"]
criteria:
  - id: irbbb-def
    name: 우각차단의 심전도 기준
    kind: 진단 기준
    population: "심실 내 전도 장애"
    statement: "완전 차단은 가장 넓은 QRS ≥ 120 ms, 불완전 차단은 약 110–120 ms. 우각차단은 끝 QRS 벡터가 오른쪽·앞으로 — V1 rSR′, V6 qRS [[harrison-21: 240장 p.1827]]"
    exceptions: "문항·지침에 따라 불완전 차단을 「QRS < 120 ms 인 rSR′」로만 적기도 한다(아래 시험 쟁점)"
    source: harrison-21
    basis: current
    exams: [kmle, usmle]
  - id: preop-mets
    name: 수술 전 심장 검사 — 운동능력
    kind: 검사 권고
    population: "위험이 높은(MACE ≥ 1%) 비심장 수술을 앞둔 환자"
    statement: "운동능력 ≥ 4 METs(계단 두 층·네 블록 걷기)면 비침습 심장 검사 없이 수술. < 4 METs 이거나 모르면 결과가 처치를 바꿀 때만 약물 부하검사 [[harrison-21: 480장 p.3769]]"
    exceptions: "응급 수술은 위험 평가 없이 진행, 급성 관상동맥증후군은 먼저 평가·치료 [[harrison-21: 480장 p.3770]]"
    source: harrison-21
    basis: current
    exams: [kmle, usmle]
sources:
  - id: harrison-21
    org: "McGraw Hill"
    title: "Harrison's Principles of Internal Medicine, 21st ed. — Chapter 480: Medical Evaluation of the Surgical Patient · Chapter 240: Electrocardiography"
    kind: textbook
    year: 2022
    citation: "Loscalzo J, Fauci AS, Kasper DL, et al (eds). Harrison's Principles of Internal Medicine, 21e. 480장 p.3769–3772 · 240장 p.1826–1828"
    checked_at: 2026-09-28
    checked: "드라이브 장 문서로 본문 대조. 480장 p.3769 — 12유도 심전도로 평가 시작, 건강한 환자의 선택 수술엔 검사 불필요, 단계적 위험 평가(MACE < 1% / 상승), ≥ 4 METs 면 추가 비침습 검사 없이 수술, < 4 METs·모름은 결과가 처치를 바꿀 때 약물 부하검사; p.3770 그림 480-1(응급 수술·ACS 단계), 저위험군 일상적 부하검사 권고 안 함; p.3771 표 480-3(계단 두 층·네 블록), 표 480-4(정형외과 수술은 중간 위험). 240장 p.1826 — 이차공 심방중격결손의 우심실 용적 과부하는 흔히 불완전·완전 우각차단 모양 + 오른쪽 QRS 축; p.1827 — 완전 ≥ 120 ms, 불완전 약 110–120 ms, V1 rSR′·V6 qRS; p.1828 — 구조 심질환 없는 사람에서 우각차단이 좌각차단보다 흔함, ASD 같은 선천 질환에서도, Brugada 양상. 우각차단 자체의 수술 전 위험·S2 고정 분열은 이 두 장에 없다"
    verified: text
  - id: thompson-2024
    org: "AHA/ACC"
    title: "2024 AHA/ACC/ACS/ASNC/HRS/SCA/SCCT/SCMR/SVM guideline for perioperative cardiovascular management for noncardiac surgery"
    kind: guideline
    year: 2024
    citation: "Thompson A, et al. Circulation 2024;150:e351"
    doi: "10.1161/CIR.0000000000001285"
    checked_at: 2026-09-28
    checked: "서지만(원문 미대조 — 이 컨테이너는 출판사·PubMed 를 막는다). 문항 해설 근거 목록에서 옮김. DOI 는 기억으로 적었다(학습서 워크플로가 PMID 를 찾아 확인)"
    verified: citation
diagram:
  title: "수술 전 불완전 우각차단 — 검사할까, 수술할까"
  nodes:
    - {id: start, kind: start, text: "수술 전 심전도 — V1 rSR′, QRS < 120 ms"}
    - {id: symp, kind: decision, text: "실신·두근거림·심부전 증상?"}
    - {id: exam, kind: decision, text: "고정 분열 S2·유출 심잡음?"}
    - {id: mets, kind: decision, text: "4 METs 이상을 증상 없이?"}
    - {id: ask, kind: info, text: "계단 두 층·네 블록 걷기를 묻는다"}
    - {id: monitor, kind: alert, text: "심전도 감시·전도계 평가"}
    - {id: echo, kind: alert, text: "경흉부 심초음파 — 심방중격결손 확인"}
    - {id: stress, kind: alert, text: "처치가 바뀔 때만 약물 부하검사"}
    - {id: go, kind: end, text: "추가 검사 없이 수술"}
  edges:
    - {from: start, to: symp}
    - {from: symp, to: monitor, label: "실신·두근거림"}
    - {from: symp, to: exam, label: "없음"}
    - {from: exam, to: echo, label: "있음"}
    - {from: exam, to: mets, label: "없음"}
    - {from: mets, to: go, label: "예"}
    - {from: mets, to: stress, label: "아니오"}
    - {from: mets, to: ask, label: "모름"}
    - {from: ask, to: go, label: "가능"}
    - {from: ask, to: stress, label: "불가·모름"}
diagram_notes:
  - "응급 수술은 이 흐름 없이 진행하고, 급성 관상동맥증후군이 있으면 그 평가·치료가 먼저다 [[harrison-21: 480장 p.3770]]."
  - "백내장·일부 내시경·표재 수술처럼 MACE < 1% 인 수술은 운동능력과 무관하게 검사 없이 수술한다 [[harrison-21: 480장 p.3769]]."
  - "V1–V2 ST 올라감을 동반한 우각차단 모양은 Brugada 양상으로 따로 본다 [[harrison-21: 240장 p.1828]]."
checks:
  - q: "수술 전 비침습 심장 검사 없이 수술할 수 있는 운동능력 기준은?"
    a: "4 METs 이상 — 계단 두 층이나 네 블록을 증상 없이."
  - q: "불완전 우각차단에서 심초음파로 가게 하는 진찰 소견은?"
    a: "고정 분열 S2 와 좌측 흉골상연 유출 심잡음 — 이차공 심방중격결손의 우심실 용적 과부하."
  - q: "활동 심전도 감시가 다음 단계가 되는 경우는?"
    a: "두근거림·설명되지 않는 실신처럼 간헐적 부정맥·전도 차단을 찾아야 할 증상이 있을 때."
variants:
  - id: v1
    of: imaging-2026-0135
    flip: true
    changed: "「S2 생리적 분열·심잡음 없음」을 「S2 가 호흡과 무관하게 넓게 고정 분열 + 좌측 흉골상연 2/6 수축기 유출 심잡음」으로 바꿈 → 추가 검사 없이 수술이 아니라 경흉부 심초음파가 정답"
    context: "단서를 바꿔 답이 바뀌는 변형 — 고정 분열 S2"
    stem: "A 58-year-old woman is evaluated before elective left total hip arthroplasty. She walks her dog 3 km every morning and climbs two flights of stairs without chest pain or dyspnea. She has no history of syncope or palpitations. Blood pressure is 128/78 mm Hg and pulse is 76/min. The second heart sound is widely split and does not change with respiration. A grade 2/6 midsystolic murmur is heard at the left upper sternal border. A 12-lead ECG shows sinus rhythm, an rSR′ pattern in V1 with a QRS duration of 110 ms, and a QRS axis of +100°. Which of the following is the most appropriate next step in management?"
    choices: ["A. Proceed with surgery without further cardiac testing", "B. Transthoracic echocardiography", "C. Exercise electrocardiographic stress testing", "D. 24-hour ambulatory electrocardiographic monitoring", "E. Coronary CT angiography"]
    answer: "B"
    explanation: "The ECG is again incomplete RBBB and functional capacity is good, but a fixed split S2 with a pulmonary flow murmur and a rightward axis points to right ventricular volume overload from an ostium secundum atrial septal defect, which Harrison links to an incomplete or complete RBBB pattern with a rightward QRS axis [[harrison-21: 240장 p.1826]]. Echocardiography now can change management. In the original item S2 split physiologically and there was no murmur, so no test would change the plan. Stress testing and coronary CT address ischemia, and ambulatory monitoring addresses symptoms she does not have."
    kind: application
  - id: v2
    of: imaging-2026-0135
    flip: false
    changed: "나이·성별(45세 남자)·수술 종류(복강경 담낭절제술)·운동능력 표현(주 3회 조깅)·제시 순서를 바꾸고 「증상 없음 + ≥ 4 METs + 생리적 S2 분열·심잡음 없음 + 불완전 우각차단」은 그대로 → 답은 여전히 추가 검사 없이 수술"
    context: "겉모습만 바꾸고 답은 같은 변형 — 담낭절제술 전 평가"
    stem: "A 45-year-old man is referred by his surgeon because the preoperative ECG before elective laparoscopic cholecystectomy was read as abnormal. The ECG shows sinus rhythm at 72/min, an rSR′ complex in V1, a QRS duration of 104 ms, and a narrow slurred S wave in leads I and V6. He jogs 5 km three times a week without chest discomfort, dyspnea, palpitations, or light-headedness. He takes no medications. On examination, the second heart sound splits on inspiration and becomes single on expiration, and there are no murmurs, gallops, or edema. Which of the following is the most appropriate next step in management?"
    choices: ["A. Transthoracic echocardiography", "B. 24-hour ambulatory electrocardiographic monitoring", "C. Dobutamine stress echocardiography", "D. Proceed with surgery without further cardiac testing", "E. Cardiology referral for electrophysiologic study"]
    answer: "D"
    explanation: "The decisive cues are unchanged: an isolated incomplete RBBB, no symptoms, functional capacity well above 4 METs, physiologic S2 splitting, and no murmur. Right bundle branch block is common in people without structural heart disease [[harrison-21: 240장 p.1828]], and patients with ≥ 4 METs proceed to surgery without noninvasive testing [[harrison-21: 480장 p.3769]]. The age, operation, and way exercise capacity is described differ from the original item, but none of them changes the decision."
    kind: application
figures:
- id: f1
  file: docs/assets/figures/ptbxl-18334.png
  kind: ecg
  at: 기전 — 늦게 전도되는 우각에서 rSR′ 로
  shows: 불완전 우각차단 — 동리듬, V1 rSR′, 좁은 QRS
  look_for:
  - V1 의 두 번째 양성파(R′)
  - I·V6 의 끌리는 S 파
  label: incomplete right bundle branch block (SCP IRBBB, 가능도 100)
  label_basis: dataset_expert
  reference: 심장내과 전문의의 SCP-ECG 판독을 두 번째 전문의가 검증 — 해당 진술의 가능도 100 인 기록만
  paper: Wagner P 외. PTB-XL, a large publicly available electrocardiography dataset. Sci Data 2020;7:154
  doi: 10.1038/s41597-020-0495-6
  credit: PTB-XL ECG dataset v1.0.3 (PhysioNet, CC BY 4.0) · record 18334
  license: Creative Commons Attribution 4.0 International
  url: https://physionet.org/content/ptb-xl/1.0.3/records500/18000/#files-panel
  asset: PTBXL-18334
  paper_cited_by: 1213
---

## 판단 — 왜 추가 검사 없이 수술이 먼저인가
- 수술 전 심장 평가는 단계로 간다: 응급인가 → 급성 관상동맥증후군인가 → 수술·환자 위험(MACE ≥ 1%) → **운동능력** [[harrison-21: 480장 p.3769–3770]].
- 운동능력이 4 METs 이상(계단 두 층·네 블록)이면 위험이 높은 수술이어도 비침습 심장 검사 없이 수술한다 [[harrison-21: 480장 p.3769]]. 무릎 관절 치환 같은 정형외과 수술은 중간 위험이다 [[harrison-21: 480장 p.3772]].
- 불완전 우각차단 하나는 이 단계 어디에도 걸리지 않는다. 검사는 **결과가 처치를 바꿀 때만** 한다.
- 검사로 넘어가게 하는 것은 심전도가 아니라 **동반 소견**이다 — 고정 분열 S2·유출 심잡음(구조), 실신·두근거림(리듬).

## 기전 — 늦게 전도되는 우각에서 rSR′ 로
우각은 가늘고 길어 전도가 늦어지기 쉽다. 좌심실은 좌각으로 정상 순서대로 먼저 탈분극하고(V1 작은 r, V6 R), 우심실은 늦게 왼쪽에서 건너온 흥분으로 활성화된다. 그래서 QRS 끝에 **오른쪽·앞으로 향하는 힘**이 더해진다 — V1 의 두 번째 R′ 와 I·V6 의 끌리는 S 다 [[harrison-21: 240장 p.1827]]. QRS 가 120 ms 이상이면 완전, 약 110–120 ms 면 불완전 차단이다 [[harrison-21: 240장 p.1827]]. 구조 심질환이 없는 사람에서 우각차단은 좌각차단보다 흔하다 [[harrison-21: 240장 p.1828]]. 반면 이차공 심방중격결손은 우심실 용적 과부하로 불완전·완전 우각차단 모양과 오른쪽 QRS 축을 만든다 [[harrison-21: 240장 p.1826]] — 그래서 같은 심전도에서 진찰 소견이 둘을 가른다.

## 선택 — 검사가 필요한 조건
- 표가 다음 단계를 정한다. 좌각차단은 관상동맥질환·고혈압 심질환·대동맥판 질환·심근병증의 표지인 경우가 많아 같은 논리로 넘기지 않는다 [[harrison-21: 240장 p.1828]].
- 부하검사를 해도, 수술 전 관상동맥 재관류는 수술과 무관하게 적응이 있을 때만 한다 [[harrison-21: 480장 p.3770]].

## 권고와 예외
- 응급 수술·급성 관상동맥증후군은 이 흐름 밖이다 [[harrison-21: 480장 p.3770]].
- 해리슨 두 장은 「불완전 우각차단이 그 자체로 수술 전 위험을 높이지 않는다」를 직접 쓰지 않는다 — 이 결론은 운동능력 규칙과 「구조 질환 없는 사람에 흔함」에서 나온다. 2024 AHA/ACC 지침 원문은 열지 못했다[[?thompson-2024]](검토 항목).
- S2 고정 분열·유출 심잡음의 기전은 이 두 장에서 대조하지 않았다(검토 항목).

## 시험 쟁점 — 충돌·맥락·새 근거
- **Z1 맥락 · 불완전 우각차단의 QRS 폭** — 시험 기준: 불완전 차단은 QRS 약 110–120 ms [[harrison-21: 240장 p.1827]] / 다른 기준: 문항 해설은 「rSR′ + QRS < 120 ms」로만 적었다(하한 없음) [[?thompson-2024]] / 왜 다른가: 해리슨은 정상 QRS 상한을 100–110 ms 로 두어 그 위를 불완전 차단으로 부르고, 문항은 완전 차단(≥ 120 ms)과의 경계만 말했다 / 시험에서는: KMLE·USMLE 모두 「V1 rSR′ + QRS < 120 ms = 불완전 우각차단」으로 읽으면 된다 — 답을 가르는 것은 폭이 아니라 동반 소견이다.
- **Z2 새 근거 · 수술 전 평가 지침의 판** — 시험 기준: 해리슨 21판 그림 480-1(2014 ACC/AHA 흐름)의 ≥ 4 METs 규칙 [[harrison-21: 480장 p.3769–3770]] / 다른 기준: 2024 AHA/ACC 지침 [[?thompson-2024]] — 원문 미대조 / 왜 다른가: 해리슨 21판 뒤에 개정 / 시험에서는: 「증상 없고 계단 두 층 가능 → 검사 없이 수술」은 두 판 모두에서 문항 해설과 같다(개정 세부는 검토 항목).
