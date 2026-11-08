---
id: cn.cardio.complete-rbbb.ecg-recognition
type: concept
topic: Cardiology
see_also: []
date: 2026-11-02
updated: 2026-11-09
version: 4
outline: h240
confidence: medium
review_status: unreviewed
note_form: 2
title: "완전 우각차단 — 넓은 QRS·V1 rsR′·V6 넓은 S"
objective: "심전도에서 QRS 폭·V1 끝부분 방향·전두면 축으로 완전 우각차단을 읽고 좌각차단·좌전섬유속 차단과 가른다"
objective_kind: 진단
condition: 완전 우각차단(complete right bundle branch block, RBBB)
exams: [kmle, usmle]
summary:
  - "결론: QRS ≥ 0.12초 + V1 rsR′(끝이 위로) + I·V6 넓은 S파 = 완전 우각차단."
  - "시험 단서: 수술 전·검진 심전도, 넓게 분열된 S2, V1 의 「토끼 귀」 모양(RSR′, complete RBBB)."
  - "왜: 우심실이 늦게 탈분극해 QRS 끝부분 벡터가 오른쪽·앞(V1 쪽)으로 향한다."
  - "QRS 가 넓지 않고 축만 −45° 보다 왼쪽이면 좌전섬유속 차단 — 각차단이 아니라 축의 문제다."
  - "QRS 110~120 ms 에 같은 모양이면 불완전 우각차단."
pitfalls:
  - contrast: "좌전섬유속 차단 vs 완전 우각차단"
    point: "섬유속 차단은 QRS 폭을 크게 늘리지 않고 전두면 축만 옮긴다 — 좌전섬유속 차단은 축이 −45° 보다 왼쪽이다. QRS 가 0.12초 이상 넓고 V1 끝이 위로(R′) 서면 우각차단이다. 먼저 폭을, 다음에 V1 끝 방향을, 마지막에 축을 본다."
    exception: "둘이 함께 있을 수 있다(우각차단 + 좌전섬유속 차단 = 이섬유속 차단) — 넓은 V1 rsR′ 에 축이 −45° 보다 왼쪽이면 둘 다 읽는다."
    cites: ["harrison-22: 247장 p.1872"]
    covers: ["imaging-2026-0514:D"]
  - contrast: "불완전 우각차단 vs 완전 우각차단"
    point: "V1 rsR′ 모양만으로는 둘을 가르지 못한다 — 폭이 가른다. 가장 넓은 유도의 QRS 가 120 ms 이상이면 완전, 약 110~120 ms 면 불완전 우각차단이다. 불완전형은 I·V6 끝 S파도 작고 좁다."
    exception: "심방중격결손의 우심실 용적 과부하도 불완전·완전 우각차단 양상을 만든다 — S2 고정 분열·우심실 확장 소견이 함께면 구조 질환을 찾는다."
    cites: ["harrison-22: 247장 p.1871"]
    covers: ["imaging-2026-0584:C"]
  - contrast: "완전 좌각차단 vs 완전 우각차단"
    point: "둘 다 QRS ≥ 0.12초. 좌각차단은 V1 이 넓고 깊은 QS(끝이 아래로), V6 은 q 없는 넓은 R 이다. V1 끝이 위로 서는 R′ 이면 우각차단이다."
    cites: ["harrison-22: 247장 p.1871"]
  - contrast: "브루가다 양상 vs 우각차단"
    point: "브루가다 양상은 우각차단과 비슷한 V1·V2 모양에 ST 상승이 붙는다 — 단순 우각차단의 오른쪽 가슴 유도 T파는 QRS 끝과 반대일 뿐 ST 가 위로 볼록하게 솟지 않는다."
    cites: ["harrison-22: 247장 p.1872"]
  - contrast: "우각차단의 T파 역위 = 허혈?"
    point: "각차단에서는 T파가 QRS 마지막 굴절과 반대로 서는 것이 이차성 변화다. 우각차단에서 V1~V3 의 T파 역위는 기대되는 소견이다."
    cites: ["harrison-22: 247장 p.1872"]
tables:
  - id: wide-qrs
    section: "가르는 소견 — 폭·V1 끝·축"
    title: "각차단·섬유속 차단 — 무엇이 가르나"
    role: differential
    span: column
    columns: ["판독", "QRS 폭", "V1 · V6 · 축"]
    rows:
      - ["완전 우각차단", "≥ 120 ms", "V1 rsR′ · V6 qRS(넓은 S) [[harrison-22: 247장 p.1871]]"]
      - ["불완전 우각차단", "110~120 ms", "같은 모양 [[harrison-22: 247장 p.1871]]"]
      - ["완전 좌각차단", "≥ 120 ms", "V1 넓은 QS · V6 넓은 R(q 없음) [[harrison-22: 247장 p.1871]]"]
      - ["좌전섬유속 차단", "거의 늘지 않음", "축 −45° 보다 왼쪽 [[harrison-22: 247장 p.1872]]"]
      - ["좌후섬유속 차단", "거의 늘지 않음", "축 +110~120° 보다 오른쪽, 단독은 매우 드묾 [[harrison-22: 247장 p.1872]]"]
criteria:
  - id: bbb-width
    name: 각차단의 QRS 폭
    kind: 진단 기준
    population: "넓은 QRS 의 12유도 심전도"
    statement: "완전 각차단은 가장 넓은 QRS 가 120 ms 이상, 불완전 각차단은 약 110~120 ms 이다. 우각차단은 끝 QRS 벡터가 오른쪽·앞으로 향해 대개 V1 rsR′·V6 qRS 를 만든다 [[harrison-22: 247장 p.1871]]"
    exceptions: "고칼륨혈증·1군 항부정맥제·삼환계 항우울제 같은 바깥 요인도 QRS 를 넓히고, 조기흥분(WPW)도 QRS 를 넓힌다 [[harrison-22: 247장 p.1872]]"
    source: harrison-22
    basis: current
    exams: [kmle, usmle]
  - id: fascicular
    name: 섬유속 차단
    kind: 진단 기준
    population: "축 편위가 있는 심전도"
    statement: "좌전·좌후섬유속 차단은 QRS 폭을 크게 늘리지 않고 전두면 축을 옮긴다 — 좌전은 −45° 보다 왼쪽, 좌후는 +110~120° 보다 오른쪽 [[harrison-22: 247장 p.1872]]"
    exceptions: "좌후섬유속 차단은 우축 편위의 다른 원인을 배제해야 한다 [[harrison-22: 247장 p.1872]]"
    source: harrison-22
    basis: current
    exams: [kmle, usmle]
sources:
  - id: harrison-22
    org: "McGraw Hill"
    title: "Harrison's Principles of Internal Medicine, 22nd ed. — Chapter 247: Electrocardiography"
    kind: textbook
    year: 2025
    citation: "Harrison's Principles of Internal Medicine, 22e. 247장 p.1868–1873"
    checked_at: 2026-11-02
    checked: "드라이브 22판 장별 문서 H22_247 본문 대조 — 히스속이 좌우 각으로, 좌각은 좌전·좌후 섬유속으로 나뉨(p.1868) · 좌축 편위 원인에 좌전섬유속 차단(p.1870) · 심방중격결손의 우심실 용적 과부하는 불완전·완전 우각차단 양상, 완전 각차단 QRS ≥ 120 ms·불완전 110~120 ms, 우각차단 끝 벡터 오른쪽·앞(V1 rsR′·V6 qRS), 좌각차단 V1 QS·V6 R, 구조 질환 없는 사람에서는 우각차단이 좌각차단보다 흔함, 선천(심방중격결손)·후천(판막·허혈) 질환에서도(p.1871) · 각차단의 이차성 ST-T(T파는 QRS 마지막 굴절과 반대), 브루가다 양상, 섬유속 차단은 QRS 를 크게 늘리지 않고 축 이동(좌전 < −45°, 좌후 > +110~120°), 고칼륨혈증·약물·WPW 도 QRS 를 넓힘(p.1872). S2 분열 기전은 이 장에 없다(원문 미대조)"
    verified: text
diagram:
  title: "넓은 QRS 리듬 — 어느 각인가"
  nodes:
    - {id: start, kind: start, text: "동리듬, 모든 박동의 QRS 가 넓어 보임"}
    - {id: width, kind: decision, text: "QRS 폭이 120 ms 이상인가?"}
    - {id: measure, kind: info, text: "가장 넓은 유도에서 QRS 폭을 잰다"}
    - {id: axis, kind: decision, text: "전두면 축이 −45° 보다 왼쪽인가?"}
    - {id: lafb, kind: end, text: "좌전섬유속 차단"}
    - {id: normal, kind: end, text: "각차단 아님 — 다른 소견을 본다"}
    - {id: v1, kind: decision, text: "V1 QRS 끝부분이 위로(R′) 서나?"}
    - {id: rbbb, kind: end, text: "완전 우각차단"}
    - {id: lbbb, kind: alert, text: "완전 좌각차단 — 구조 심질환 평가"}
  edges:
    - {from: start, to: width}
    - {from: width, to: v1, label: "예"}
    - {from: width, to: axis, label: "아니오"}
    - {from: width, to: measure, label: "모르겠음"}
    - {from: measure, to: v1, label: "≥ 120 ms"}
    - {from: measure, to: axis, label: "< 120 ms"}
    - {from: axis, to: lafb, label: "예"}
    - {from: axis, to: normal, label: "아니오"}
    - {from: v1, to: rbbb, label: "rsR′"}
    - {from: v1, to: lbbb, label: "넓은 QS"}
diagram_notes:
  - "QRS 110~120 ms 에 V1 rsR′ 이면 불완전 우각차단 [[harrison-22: 247장 p.1871]]."
  - "넓은 우각차단에 축까지 −45° 보다 왼쪽이면 우각차단 + 좌전섬유속 차단을 함께 읽는다."
  - "고칼륨혈증·1군 항부정맥제·삼환계 항우울제·조기흥분도 QRS 를 넓힌다 — 전해질·약을 확인한다 [[harrison-22: 247장 p.1872]]."
  - "V1·V2 에 우각차단 비슷한 모양과 ST 상승이 함께면 브루가다 양상을 생각한다 [[harrison-22: 247장 p.1872]]."
checks:
  - q: "QRS 0.14초, V1 rsR′, I·V6 넓은 S파. 판독은?"
    a: "완전 우각차단. 늦은 우심실 탈분극이 끝 벡터를 오른쪽·앞(V1 쪽)으로 끌어간다."
  - q: "좌전섬유속 차단을 우각차단과 무엇으로 가르나?"
    a: "QRS 폭. 섬유속 차단은 폭을 크게 늘리지 않고 축만 −45° 보다 왼쪽으로 옮긴다."
variants:
  - id: v1
    of: imaging-2026-0514
    flip: true
    changed: "QRS 0.14초·V1 rsR′·I·V6 넓은 S파 → QRS 0.09초·V1 정상 rS·II·III·aVF 깊은 S·축 −60° ⇒ 정답이 완전 우각차단에서 좌전섬유속 차단으로"
    context: "같은 수술 전 상황, 소견을 글로 바꾼 변형(그림 없음)"
    stem: "68세 남자가 담낭절제술을 앞두고 수술 전 검사를 받았다. 증상은 없고 매일 40분씩 걷는다. 고혈압으로 약을 먹고 있다. 혈압 134/82 mmHg, 맥박 72회/분이다. 심잡음은 없고 제2심음은 정상으로 분열된다. 혈청 칼륨 4.3 mEq/L 이다. 12유도 심전도는 동리듬이고 QRS 폭은 0.09초이다. V1 은 작은 r 과 깊은 S 의 rS 모양이고 I·aVL 은 qR, II·III·aVF 는 깊은 S파가 있는 rS 모양이며 전두면 QRS 축은 −60°이다. 심전도 판독으로 가장 적절한 것은?"
    choices: ["A. 우심실 비대", "B. 완전 우각차단", "C. 완전 좌각차단", "D. 좌전섬유속 차단", "E. 좌후섬유속 차단"]
    answer: "D"
    explanation: "QRS 가 0.09초로 넓지 않아 각차단이 아니고, V1 끝이 위로 서는 R′ 도 없다. 축만 −45° 보다 왼쪽(−60°)으로 옮겨 갔으니 좌전섬유속 차단이다. 좌후섬유속 차단은 축이 +110~120° 보다 오른쪽이다."
    kind: application
  - id: v2
    of: imaging-2026-0514
    flip: false
    changed: "66세 남자·탈장 수술 전 검사 → 54세 여자·직장 건강검진, 소견을 글로 제시 ⇒ QRS ≥ 0.12초·V1 rsR′·I·V6 넓은 S파라는 결정 단서는 같아 답은 그대로 완전 우각차단"
    context: "겉모습만 바꾼 글 변형(그림 없음)"
    stem: "54세 여자가 직장 건강검진에서 심전도 이상 소견을 듣고 왔다. 두근거림·호흡곤란·실신은 없고 등산을 즐긴다. 혈압 118/74 mmHg, 맥박 70회/분이다. 제2심음은 넓게 분열되며 들숨에 더 벌어지고 심잡음은 없다. 흉부 X선은 정상이다. 12유도 심전도는 동리듬이고 QRS 폭은 0.13초이다. V1 은 rsR′ 모양으로 끝부분이 위로 넓게 서 있고, I·V5·V6 에는 넓고 둔한 S파가 있다. 전두면 축은 +40°이다. 심전도 판독으로 가장 적절한 것은?"
    choices: ["A. 브루가다 1형 양상", "B. 완전 좌각차단", "C. 좌전섬유속 차단", "D. 완전 우각차단", "E. 우심실 비대"]
    answer: "D"
    explanation: "나이·성별·검사 경위가 바뀌었지만 결정 단서는 같다 — QRS ≥ 0.12초, V1 끝이 위로 서는 rsR′, I·V6 넓은 S파. 축은 정상이라 좌전섬유속 차단은 함께 있지 않고, ST 상승이 없어 브루가다 양상도 아니다. S2 분열이 들숨에 더 벌어져 고정 분열(심방중격결손)이 아니다."
    kind: application
  - id: v3
    of: imaging-2026-0584
    flip: true
    changed: "QRS 0.10초·I·V6 작은 S → QRS 0.13초·I·V6 넓고 둔한 S ⇒ 정답이 불완전 우각차단에서 완전 우각차단으로"
    context: "같은 입사 검진 상황, 소견을 글로 바꾼 변형(그림 없음)"
    stem: "A 37-year-old man undergoes a preemployment medical examination. He has no symptoms and jogs regularly. He has never had palpitations or syncope, and there is no family history of sudden cardiac death. His pulse is 76/min, and blood pressure is 122/76 mm Hg. Cardiac examination shows wide splitting of the second heart sound that increases with inspiration; there are no murmurs. Serum electrolyte concentrations are within the reference range. A 12-lead ECG shows sinus rhythm with a PR interval of 0.16 seconds, a QRS duration of 0.13 seconds, an rsR′ pattern in lead V1 with a broad terminal R′, broad slurred S waves in leads I and V6, no ST-segment elevation in V1 or V2, and a frontal-plane QRS axis of +60°. Which of the following is the most likely interpretation of this ECG?"
    choices: ["A. Left anterior fascicular block", "B. Sinus rhythm with incomplete RBBB", "C. Sinus rhythm with complete RBBB", "D. Type 1 Brugada pattern", "E. Wolff-Parkinson-White pattern"]
    answer: "C"
    explanation: "The V1 rsR′ shape is the same as in the original item, but the QRS is now 0.13 seconds with broad S waves in I and V6. A QRS of 120 ms or more with this morphology is complete RBBB; 110 to 120 ms would be incomplete. There is no ST elevation (not Brugada), the PR interval is normal without a delta wave (not WPW), and the axis is normal (no left anterior fascicular block)."
    kind: application
  - id: v4
    of: imaging-2026-0584
    flip: false
    changed: "37세 남자 입사 검진·심전도 그림 → 24세 여자 대학 체육 특기생 검진·소견을 글로 제시 ⇒ V1 rsR′·QRS 0.10초라는 결정 단서는 같아 답은 그대로 불완전 우각차단"
    context: "겉모습만 바꾼 글 변형(그림 없음)"
    stem: "A 24-year-old woman comes for a preparticipation sports examination before joining her university rowing team. She has no symptoms and trains 6 days a week. She has never fainted, and there is no family history of sudden death. She takes no medications. Her pulse is 58/min, and blood pressure is 112/70 mm Hg. Cardiac examination shows physiologic splitting of the second heart sound and no murmurs. A 12-lead ECG shows sinus bradycardia with a PR interval of 0.18 seconds, a QRS duration of 0.10 seconds, an rSr′ pattern in lead V1 with a small, narrow terminal r′, small narrow S waves in leads I and V6, no ST-segment elevation in V1 or V2, and a QRS axis of +75°. Which of the following is the most likely interpretation of this ECG?"
    choices: ["A. Type 1 Brugada pattern", "B. Sinus rhythm with complete RBBB", "C. Wolff-Parkinson-White pattern", "D. Sinus rhythm with incomplete RBBB", "E. Left posterior fascicular block"]
    answer: "D"
    explanation: "Age, sex, and the reason for the ECG changed, but the deciding findings did not: an rSr′ in V1 with a QRS under 0.12 seconds is incomplete RBBB. Complete RBBB needs a QRS of 120 ms or more. There is no coved ST elevation (Brugada), no short PR or delta wave (WPW), and the axis is not right of +110° (left posterior fascicular block)."
    kind: application
figures:
- id: f1
  file: docs/assets/figures/ptbxl-00903.png
  kind: ecg
  at: 기전 — 늦게 깨는 우심실
  shows: 완전 우각차단 — 넓은 QRS 와 V1 rsR′
  look_for:
  - V1 의 끝부분이 위로 넓게 솟은 R′
  - I·V5·V6 끝부분의 넓고 둔한 S파
  label: complete right bundle branch block (SCP CRBBB, 가능도 100)
  label_basis: dataset_expert
  reference: 심장내과 전문의의 SCP-ECG 판독을 두 번째 전문의가 검증 — 해당 진술의 가능도 100 인 기록만
  paper: Wagner P 외. PTB-XL, a large publicly available electrocardiography dataset. Sci Data 2020;7:154
  doi: 10.1038/s41597-020-0495-6
  credit: PTB-XL ECG dataset v1.0.3 (PhysioNet, CC BY 4.0) · record 903
  license: Creative Commons Attribution 4.0 International
  url: https://physionet.org/content/ptb-xl/1.0.3/records500/00000/#files-panel
  asset: PTBXL-00903
  paper_cited_by: 1213
  from_question: imaging-2026-0514
- id: f2
  file: docs/assets/figures/ptbxl-05455.png
  kind: ecg
  at: 가르는 소견 — 폭·V1 끝·축
  shows: 불완전 우각차단 — QRS 가 넓지 않은 우각차단 양상
  look_for:
  - 모든 유도의 QRS 폭이 0.12초(작은 칸 3개)에 못 미침
  - V5·V6 끝부분의 작고 좁은 S파
  label: incomplete right bundle branch block (SCP IRBBB, 가능도 100)
  label_basis: dataset_expert
  reference: 심장내과 전문의의 SCP-ECG 판독을 두 번째 전문의가 검증 — 해당 진술의 가능도 100 인 기록만
  paper: Wagner P 외. PTB-XL, a large publicly available electrocardiography dataset. Sci Data 2020;7:154
  doi: 10.1038/s41597-020-0495-6
  credit: PTB-XL ECG dataset v1.0.3 (PhysioNet, CC BY 4.0) · record 5455
  license: Creative Commons Attribution 4.0 International
  url: https://physionet.org/content/ptb-xl/1.0.3/records500/05000/#files-panel
  asset: PTBXL-05455
  paper_cited_by: 1213
---

## 판단 — 넓은 QRS 를 읽는 순서
- **폭**: QRS ≥ 120 ms 면 완전 각차단, 110~120 ms 면 불완전 [[harrison-22: 247장 p.1871]]. 폭이 늘지 않았다면 각차단이 아니다.
- **V1 끝 방향**: 끝이 위로(R′) 서면 우각차단, 넓고 깊은 QS 면 좌각차단 [[harrison-22: 247장 p.1871]].
- **축**: 폭이 정상인데 축이 −45° 보다 왼쪽이면 좌전섬유속 차단 [[harrison-22: 247장 p.1872]].

## 기전 — 늦게 깨는 우심실
정상 흥분은 히스속에서 좌우 각으로 갈라져 두 심실을 거의 동시에 탈분극시킨다 [[harrison-22: 247장 p.1868]]. 우각이 막히면 좌심실이 먼저, 우심실은 근육을 따라 천천히 늦게 탈분극한다. 그래서 QRS 가 넓어지고, QRS 끝 벡터가 늦은 쪽 — 오른쪽·앞 — 으로 향한다: V1 에서는 끝에 위로 솟는 R′, I·V6 에서는 끝에 넓은 S 가 된다 [[harrison-22: 247장 p.1871]]. 탈분극 순서가 바뀌어 재분극도 바뀌므로 T파는 QRS 마지막 굴절과 반대로 선다(이차성 변화) [[harrison-22: 247장 p.1872]]. 우심실 수축이 늦어 폐동맥판이 늦게 닫히면 S2 가 넓게 분열된다(원문 미대조).

## 가르는 소견 — 폭·V1 끝·축
- 좌각은 좌전·좌후 섬유속으로 나뉜다. 섬유속 하나만 막히면 나머지가 좌심실을 빠르게 깨우므로 QRS 는 거의 넓어지지 않고 축만 옮겨 간다 [[harrison-22: 247장 p.1872]].
- 우각차단은 구조 심질환이 없는 사람에게 좌각차단보다 흔하고, 심방중격결손 같은 선천 질환과 판막·허혈 질환에서도 생긴다 [[harrison-22: 247장 p.1871]].
- QRS 를 넓히는 바깥 요인(고칼륨혈증·1군 항부정맥제·삼환계 항우울제)과 조기흥분을 먼저 배제한다 [[harrison-22: 247장 p.1872]].

## 권고와 예외
- 우각차단에서 오른쪽 가슴 유도의 T파 역위는 기대되는 이차성 변화이지만, 왼쪽 가슴 유도의 T파 역위는 허혈 등 다른 이상의 표지일 수 있다 [[harrison-22: 247장 p.1872]].
- 오른쪽 가슴 유도에 우각차단 비슷한 모양과 ST 상승이 함께면 브루가다 양상을 따로 생각한다 [[harrison-22: 247장 p.1872]].

## 시험 쟁점 — 충돌·맥락·새 근거
- 해당 없음(대조: 해리슨 22판 247장 p.1868–1873)
