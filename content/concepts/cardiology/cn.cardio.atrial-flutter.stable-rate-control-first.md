---
id: cn.cardio.atrial-flutter.stable-rate-control-first
type: concept
topic: Cardiology
see_also: [Emergency Medicine]
date: 2026-09-23
updated: 2026-09-23
version: 1
outline: h250            # 기본틀 슬롯(content/outline/subjects.yaml)
confidence: medium
review_status: unreviewed
title: "심방조동 — 톱니파 인식에서 안정형 첫 처치(심박수 조절·항응고 판단)까지"
objective: "규칙적인 좁은 QRS 빈맥에서 톱니 모양 조동파와 2:1 전도로 전형적 심방조동을 알아보고, 방실결절 비의존 거대 회귀회로라 아데노신이 종료하지 못하는 이유를 설명한 뒤, 혈역학이 안정하고 지속시간이 불확실하면 동율동전환보다 심박수 조절과 항응고 판단을 먼저 고른다"
objective_kind: 다음 처치
condition: 전형적 심방조동(삼첨판 협부 의존)
exams: [usmle, kmle]
summary:
  - "전형적 심방조동은 삼첨판륜을 도는 우심방의 거대 회귀회로다. 회로가 심방 안에서 닫혀 있어 방실결절은 회로의 일부가 아니다 — 방실결절은 심방 신호 중 몇 개를 심실로 보낼지만 정한다 [[harrison-21: 250장 p.1899]]."
  - "심방 속도 240–300회/분이 2:1 로 전도되면 심실은 130–150회/분의 규칙적인 빈맥이 되고, 조동파가 T파에 묻혀 PSVT 처럼 보인다. II·III·aVF 의 음성 톱니파가 단서다 [[harrison-21: 250장 p.1899]]."
  - "아데노신·미주신경 자극은 방실결절을 잠시 막아 조동파를 드러낼 뿐 회로를 끊지 못한다 — 방실결절이 회로에 들어 있는 PSVT(AVNRT·AVRT)에서만 종료 약이다 [[harrison-21: 250장 p.1899]]."
  - "불안정(저혈압·흉통·의식저하·폐부종)하면 즉시 전기적 동율동전환. 안정하면 방실결절 차단제(IV 베타차단제 또는 딜티아젬·베라파밀)로 심박수를 조절한다 [[harrison-21: 250장 p.1900, Fig 250-3 p.1902]]."
  - "혈전색전 위험은 심방세동과 비슷하게 본다. 48시간을 넘었거나 시작 시점을 모르면 동율동전환 전에 항응고(또는 경식도 초음파로 좌심방이 혈전 배제)가 필요하고, 장기 항응고는 CHA2DS2-VASc 로 정한다 [[harrison-21: 250장 p.1900]]."
pitfalls:
  - contrast: "「안정형 규칙적 좁은 QRS 빈맥 = 아데노신」 vs 심방조동"
    point: "아데노신은 방실결절이 회로의 일부일 때만 빈맥을 끝낸다. 심방조동은 심방 안에서 닫힌 거대 회귀회로라 방실전도만 잠깐 끊겨 조동파가 드러나고 리듬은 그대로 이어진다. 톱니파가 이미 보이면 아데노신은 진단도 치료도 더하지 않는다."
    exception: "심방파가 보이지 않는 규칙적 좁은 QRS 빈맥에서는 아데노신이 진단(조동파 노출)과 치료(PSVT 종료)를 겸한다."
    cites: ["harrison-21"]
    covers: ["usmle-2026-0046:B"]
  - contrast: "「리듬을 되돌리면 끝」 vs 지속시간 불명"
    point: "전기적이든 약물(아미오다론)이든 동율동으로 돌아가는 순간 기절해 있던 좌심방이 수축을 되찾아 이미 생긴 혈전이 떨어질 수 있다. 시작 시점을 모르면 48시간이 넘은 것으로 본다 — 항응고 3주 또는 경식도 초음파 배제가 먼저다."
    exception: "혈역학이 불안정하면 항응고를 기다리지 않고 동율동전환한다."
    cites: ["harrison-21", "?acc-aha-af-2023"]
  - contrast: "심방조동 vs 다초점 심방빈맥(MAT) — 둘 다 COPD 환자에서"
    point: "MAT 는 P파 모양이 3가지 이상이고 P파 사이 등전위선이 있으며 리듬이 불규칙하다. 기저 폐질환 치료가 핵심이고 전기적 동율동전환은 효과가 없다. 조동은 한 가지 모양의 톱니파가 규칙적으로 이어진다 [[harrison-21: 250장 p.1901]]."
criteria:
  - id: afl-unstable
    name: 불안정 심방조동
    kind: 치료 기준
    population: "혈역학 불안정 또는 심한 증상의 심방조동"
    statement: "동기화 전기적 동율동전환(저에너지) [[harrison-21: 250장 p.1900, Fig 250-3 p.1902]]"
    exceptions: "불안정하면 지속시간·항응고 상태와 무관하게 먼저 전환한다"
    source: harrison-21
    basis: current
    exams: [usmle, kmle]
  - id: afl-stable-rate
    name: 안정형 심박수 조절
    kind: 치료 기준
    population: "혈역학이 안정한 심방조동"
    statement: "IV 베타차단제 또는 IV 딜티아젬·베라파밀로 심박수 조절(Fig 250-3 에서 IIa B). 조동은 심방세동보다 심박수 조절이 더 어렵다 [[harrison-21: 250장 p.1900, p.1902]]"
    exceptions: "리듬 조절을 택하면 동기화 동율동전환(I B)·이부틸리드·도페틸리드가 도식에 있다 — 항응고 조건을 먼저 맞춘다"
    source: harrison-21
    basis: current
    exams: [usmle, kmle]
  - id: afl-anticoag
    name: 전환 전 항응고
    kind: 치료 기준
    population: "동율동전환을 계획하는 심방조동"
    statement: "지속 48시간을 넘으면 전환 전에 항응고, 혈전색전 위험이 높으면(CHA2DS2-VASc) 장기 항응고 — 심방세동과 같은 원칙 [[harrison-21: 250장 p.1900–1901]]"
    exceptions: "시작 시점을 모르면 48시간 초과로 취급한다. 3주 항응고 대신 경식도 초음파로 좌심방이 혈전을 배제하는 길은 지침 세부로 이 정리본에서는 원문 미대조 [[?acc-aha-af-2023]]"
    source: harrison-21
    basis: current
    exams: [usmle, kmle]
sources:
  - id: harrison-21
    org: "McGraw Hill"
    title: "Harrison's Principles of Internal Medicine, 21st ed. — Chapter 250: Common Atrial Flutter and Macroreentrant and Multifocal Atrial Tachycardias"
    kind: textbook
    year: 2022
    citation: "Loscalzo J, Kasper DL, Longo DL, et al (eds). Harrison's Principles of Internal Medicine, 21e. 250장 p.1899–1902"
    checked_at: 2026-09-23
    checked: "본문 대조(드라이브 250장 문서) — p.1899: 삼첨판륜 회귀회로·협부 의존·반시계 방향이 II/III/aVF 음성 톱니파·심방 240–300회/분·2:1 전도로 130–150회/분·방실결절 차단 조작이 조동파를 드러냄, 249장 말미 PSVT 에서 아데노신은 방실결절 전도를 막아 종료 · p.1900: 불안정·심한 증상이면 전기적 전환, 아니면 방실결절 차단제로 심박수 조절(심방세동보다 어려움), 혈전색전 위험은 심방세동과 비슷, 48시간 초과 시 전환 전 항응고, CHA2DS2-VASc 로 장기 항응고 · p.1901: 협부 절제 >95%, 5년 내 약 50% 심방세동, MAT 정의·폐질환 환자는 베타차단제 불내성 흔함 · p.1902 Fig 250-3: 안정형 IV 베타차단제 또는 IV 딜티아젬·베라파밀(IIa B), 동기화 전환(I B)"
    verified: text
  - id: acc-aha-af-2023
    org: "ACC/AHA/ACCP/HRS"
    title: "2023 ACC/AHA/ACCP/HRS Guideline for the Diagnosis and Management of Atrial Fibrillation"
    kind: guideline
    year: 2023
    citation: "Joglar JA, et al. Circulation 2024;149:e1–e156"
    doi: "10.1161/CIR.0000000000001193"
    url: "https://doi.org/10.1161/CIR.0000000000001193"
    checked_at: 2026-09-23
    checked: "서지만 — 이 컨테이너에서 doi·PubMed 접근 차단으로 권고 본문(3주 항응고·TEE 전략)은 대조하지 못했다"
    verified: citation
diagram:
  title: "규칙적인 좁은 QRS 빈맥 — 심방조동 인식과 첫 처치"
  nodes:
    - {id: start, kind: start, text: "규칙적인 좁은 QRS 빈맥(심실 130–150회/분)"}
    - {id: stable, kind: decision, text: "혈역학이 안정한가? 저혈압·흉통·의식저하·폐부종"}
    - {id: dccv, kind: end, text: "즉시 동기화 전기적 동율동전환"}
    - {id: waves, kind: decision, text: "II·III·aVF 에 톱니 모양 조동파가 보이는가?"}
    - {id: expose, kind: info, text: "조동파가 T파에 묻혀 불분명 — 미주신경 자극·아데노신으로 방실전도를 잠시 늦춰 심방파를 드러낸다"}
    - {id: psvt, kind: alert, text: "심방파 없이 빈맥이 끝나면 방실결절 의존 PSVT(AVNRT·AVRT) — 이 도식 범위 밖"}
    - {id: rate, kind: step, text: "심방조동 — IV 베타차단제 또는 딜티아젬·베라파밀로 심박수 조절"}
    - {id: onset, kind: decision, text: "시작 48시간 미만이 확실한가?"}
    - {id: early, kind: end, text: "조기 동율동전환을 고려할 수 있다(항응고 병행) · 장기 항응고는 CHA2DS2-VASc"}
    - {id: delay, kind: end, text: "심박수 조절 유지 + 항응고 3주(또는 경식도 초음파로 혈전 배제) 뒤 동율동전환 · 장기 항응고는 CHA2DS2-VASc"}
  edges:
    - {from: start, to: stable}
    - {from: stable, to: dccv, label: "불안정"}
    - {from: stable, to: waves, label: "안정"}
    - {from: waves, to: rate, label: "톱니파 보임"}
    - {from: waves, to: expose, label: "불분명"}
    - {from: expose, to: rate, label: "톱니파 드러남"}
    - {from: expose, to: psvt, label: "빈맥 종료"}
    - {from: rate, to: onset}
    - {from: onset, to: early, label: "48시간 미만 확실"}
    - {from: onset, to: delay, label: "48시간 이상 · 시점 불명"}
diagram_notes:
  - "아데노신은 조동을 끝내지 못한다 — 심방파를 드러내는 진단 도구일 뿐이다. 조동파가 이미 보이면 쓸 이유가 없다."
  - "시작 시점이 불확실하면(「어제쯤부터일 수도」) 48시간 이상으로 취급한다."
  - "재발하는 전형적 조동은 삼첨판 협부 도자 절제가 95% 넘게 없앤다 — 1차 치료로도 고려된다. 절제 뒤에도 약 절반은 5년 안에 심방세동이 생겨 항응고 판단은 계속된다 [[harrison-21: 250장 p.1901]]."
checks:
  - q: "심방조동에서 아데노신이 리듬을 끝내지 못하는 이유는?"
    a: "회귀회로가 삼첨판륜을 도는 심방 안에서 닫혀 있고 방실결절은 회로에 들어 있지 않다. 방실전도만 잠시 막혀 조동파가 드러날 뿐이다."
  - q: "심실 150회/분의 규칙적 좁은 QRS 빈맥을 보면 무엇을 먼저 의심해야 하나?"
    a: "2:1 전도의 심방조동(심방 약 300회/분). II·III·aVF 에서 T파에 묻힌 톱니파를 찾는다."
  - q: "안정한 심방조동인데 시작 시점을 모른다. 오늘 동율동전환하지 않는 이유는?"
    a: "48시간 초과로 취급하므로 좌심방이 혈전 가능성이 있다. 전환 순간 혈전이 떨어질 수 있어 항응고(또는 경식도 초음파 배제)가 먼저이고, 그동안은 심박수 조절을 한다."
variants:
  - id: v1
    of: usmle-2026-0046
    flip: true
    changed: "안정·시작 시점 불명(48시간 초과로 취급) → 수축기 혈압 78 mmHg·흉통·차갑고 축축한 피부로 불안정 ⇒ 정답이 IV 베타차단제 심박수 조절에서 즉시 동기화 전기적 동율동전환으로"
    context: "단서를 바꿔 답이 바뀌는 변형 — 혈역학 불안정한 심방조동"
    stem: "A 66-year-old woman with a history of hypertension is brought to the emergency department with palpitations that began at an uncertain time over the past day. She now reports chest pressure and lightheadedness. Blood pressure is 78/50 mm Hg, pulse is 150/min and regular, and respirations are 24/min. Her skin is cool and clammy, and she is slow to answer questions. An ECG shows a regular narrow-complex tachycardia with negative sawtooth atrial waves in leads II, III, and aVF and 2:1 atrioventricular conduction. Serum potassium is 4.0 mEq/L. Which of the following is the most appropriate next step in management?"
    choices: ["A. Synchronized electrical cardioversion now", "B. Intravenous metoprolol for rate control", "C. Intravenous adenosine bolus", "D. Start anticoagulation and plan cardioversion in 3 weeks", "E. Intravenous diltiazem infusion"]
    answer: "A"
    explanation: "The changed clue is hemodynamic instability: hypotension, chest pressure, altered mentation, and poor perfusion. Unstable atrial flutter is treated with immediate synchronized cardioversion regardless of duration or anticoagulation status [[harrison-21: 250장 p.1900]]. Beta-blockers and diltiazem would worsen hypotension, adenosine only transiently blocks the AV node without terminating the atrial macroreentrant circuit, and waiting 3 weeks is not safe in an unstable patient. In the original case the patient was warm and well perfused, so rate control came first."
    kind: application
  - id: v2
    of: usmle-2026-0046
    flip: false
    changed: "나이·성별(64세 여성)·기저질환(고혈압·당뇨)·내원 경위(정기 진료 중 발견)·제시 순서를 바꾸고, 안정 혈역학·톱니파 2:1 전도·시작 시점 불명은 유지 ⇒ 답은 그대로 심박수 조절"
    context: "겉모습만 바꾸고 답은 같은 변형 — 외래에서 발견된 심방조동"
    stem: "A 64-year-old woman with hypertension and type 2 diabetes is found to have a pulse of 146/min at a routine clinic visit. She has noticed fatigue and occasional fluttering in her chest for 'a few days, maybe longer.' Blood pressure is 124/78 mm Hg, and she has no chest pain, dyspnea at rest, or confusion. Lungs are clear. An ECG shows a regular narrow-complex rhythm with a continuous sawtooth baseline in the inferior leads and two atrial waves for every QRS complex. Electrolytes and TSH are within normal limits. Which of the following is the most appropriate next step in management?"
    choices: ["A. Intravenous adenosine to terminate the rhythm", "B. Rate control with an atrioventricular nodal blocking agent", "C. Electrical cardioversion today without imaging", "D. Oral amiodarone loading for cardioversion this week", "E. Urgent catheter ablation of the cavotricuspid isthmus today"]
    answer: "B"
    explanation: "The deciding clues are unchanged: stable hemodynamics, sawtooth flutter waves with 2:1 conduction, and an onset that cannot be dated within 48 hours. Rate control with a beta-blocker or nondihydropyridine calcium channel blocker comes first, and anticoagulation must be addressed before any rhythm-control attempt [[harrison-21: 250장 p.1900]]. Adenosine cannot terminate a macroreentrant atrial circuit; cardioversion or pharmacologic conversion without anticoagulation risks embolic stroke; ablation is an elective option for recurrent flutter, not an emergency first step."
    kind: application
---

## 정의
심방조동은 심방 안의 거대 회귀회로로 생기는 규칙적인 심방 빈맥이다. **전형적(흔한) 심방조동**은 삼첨판륜을 도는 우심방 회로로, 하대정맥과 삼첨판륜 사이의 좁은 통로(삼첨판 협부)를 반드시 지나가므로 「협부 의존 조동」이라고도 한다 [[harrison-21: 250장 p.1899]].

## 병태생리
정상에서는 동결절의 한 번의 흥분이 심방을 한 번 지나고 끝난다. 심방에 흉터(노화·심장 수술)나 우심·폐혈관 질환이 있으면 전도가 느린 부위와 기능적 차단선(분계능선)이 생겨, 흥분이 삼첨판륜을 따라 계속 돌 수 있는 길이 만들어진다 [[harrison-21: 250장 p.1899]]. 이 회로는 **심방 안에서만** 닫혀 있다. 방실결절은 회로 밖에서 심방의 신호를 몇 개 걸러 심실로 보낼지만 정한다.

## 기전에서 소견으로
- 회로가 약 300회/분으로 돌아 심방 속도 240–300회/분 → 방실결절이 절반만 통과시키면(2:1) 심실 130–150회/분의 **규칙적인** 좁은 QRS 빈맥 [[harrison-21: 250장 p.1899]].
- 반시계 방향 회로의 탈분극 방향 때문에 II·III·aVF 에서 **음성 톱니파**, V1 에서 양성 P파가 보인다.
- 2:1 전도에서는 조동파 하나가 T파에 겹쳐 PSVT 처럼 보인다. 방실결절 전도를 늦추는 조작(미주신경 자극·아데노신·방실결절 차단제)을 하면 전도 비가 높아져 톱니파가 드러난다 [[harrison-21: 250장 p.1899]].

## 감별
- **PSVT(AVNRT·AVRT)**: 방실결절이 회로의 일부 → 아데노신·미주신경 자극으로 **종료**된다 [[harrison-21: 249장 p.1899]].
- **다초점 심방빈맥(MAT)**: P파 모양 3가지 이상, 등전위선 있음, 불규칙, 100–150회/분. 중증 폐질환·급성 질환에서. 기저 질환 치료, 전기적 전환은 효과 없음 [[harrison-21: 250장 p.1901]].
- **심방세동**: 불규칙하게 불규칙, 뚜렷한 심방파 없음.

## 검사
12유도 심전도(하벽 유도 톱니파, 전도 비), 전해질·갑상선 기능(유발 요인), 심초음파. 동율동전환을 계획하면 좌심방이 혈전을 보기 위한 경식도 초음파.

## 치료
1. **불안정** → 즉시 동기화 전기적 동율동전환(저에너지로 잘 전환된다).
2. **안정** → 방실결절 차단제(IV 베타차단제·딜티아젬·베라파밀)로 심박수 조절. 심방세동보다 조절이 어렵다 [[harrison-21: 250장 p.1900]].
3. **항응고 판단** — 혈전색전 위험은 심방세동과 비슷하게 본다. 48시간 넘게 지속했거나 시점을 모르면 전환 전 항응고, 장기 항응고는 CHA2DS2-VASc [[harrison-21: 250장 p.1900]].
4. **리듬 조절** — 첫 발작은 전환 뒤 장기 항부정맥제 없이 지켜볼 수 있다. 재발하면 삼첨판 협부 도자 절제(>95% 성공, 1차 치료로도 고려) [[harrison-21: 250장 p.1900–1901]].
- 재평가: 심박수 조절 뒤 심실 반응, 증상, 혈압을 다시 본다. 조절이 안 되면 항응고 조건을 맞춘 뒤 리듬 조절로 넘어간다.

## 권고와 예외
- 불안정하면 항응고를 기다리지 않는다.
- 아미오다론은 약물적 전환을 일으킬 수 있으므로, 항응고가 안 된 지속시간 불명 조동에서 「심박수 조절 목적」이라도 전환 위험을 생각해야 한다(이 정리본에서는 원문 미대조 — 검토 항목).
- 항부정맥제(플레카이니드·프로파페논·아미오다론)를 쓰던 심방세동 환자가 조동으로 나타날 수 있다 — 약이 심방 전도를 늦춰 회귀를 돕는다 [[harrison-21: 250장 p.1899]].

## 시험 쟁점 — 충돌·맥락·새 근거
- **Z1 맥락 · COPD 환자에서 베타차단제** — 시험 기준: 안정형 조동의 심박수 조절은 IV 베타차단제 또는 딜티아젬·베라파밀(둘 다 IIa B) [[harrison-21: 250장 p.1902]] / 다른 기준: 해리슨은 MAT 절에서 중증 폐질환 환자가 베타차단제를 잘 견디지 못한다고 적는다 [[harrison-21: 250장 p.1901]] / 왜 다른가: 기관지 수축 위험 때문에 실제로는 비DHP 칼슘통로차단제나 β1 선택 약을 고르는 경우가 많다 / 시험에서는: USMLE · 보기에 심박수 조절 약이 하나뿐이면 그것이 답(「첫 단계는 심박수 조절」을 묻는다), 둘 다 있으면 폐질환 정도를 본다 · KMLE 도 같은 원칙.
- 그 밖에 해리슨과 어긋난 곳 없음(대조: 해리슨 250장 p.1899–1902).

## (심화) 왜 이 문항은 「리듬 인식」 문항인가
보기 다섯 개 중 넷은 「리듬을 지금 끝낸다」(전기·아데노신·아미오다론·TEE 없는 전환)이다. 톱니파를 알아보면 아데노신이 빠지고, 지속시간 불명을 읽으면 전환 셋이 빠진다 — 인식과 항응고 판단 두 단계가 이어져야 답이 남는다.
