---
id: cn.cardio.complete-lbbb.discordant-st-not-stemi
type: concept
topic: Cardiology
see_also: []
date: 2026-11-03
updated: 2026-11-03
version: 2
outline: h240
confidence: medium
review_status: unreviewed
note_form: 2
title: "완전 좌각차단 — V1~V3 ST 상승은 반대 방향 이차 변화"
objective: "심전도에서 넓은 QRS·V1 넓은 QS·V6 q 없는 넓은 R 으로 완전 좌각차단을 읽고, QRS 와 반대 방향인 V1~V3 ST 상승을 급성 전벽 경색과 가른다"
objective_kind: 진단
condition: 완전 좌각차단(complete left bundle branch block, LBBB)
exams: [kmle, usmle]
summary:
  - "결론: QRS ≥ 0.12초 + V1 넓은 QS + I·aVL·V6 q 없는 넓은 R = 완전 좌각차단, V1~V3 ST 상승은 이차 변화."
  - "시험 단서: 고령·고혈압·심부전, 흉통 없음·트로포닌 정상인데 V1~V3 ST 상승(discordant ST elevation in LBBB)."
  - "왜: 탈분극 순서가 바뀌면 재분극도 바뀌어 ST-T 가 QRS 주 방향과 반대로 선다 — 깊은 QS 유도에서는 ST 가 올라간다."
  - "좌각차단은 관상동맥질환·고혈압성 심질환·대동맥판 질환·심근병증의 표지 — 원인 심질환을 찾는다."
  - "좌각차단은 급성 허혈의 심전도 변화를 가린다 — 경색 판단은 증상·트로포닌과 함께 한다."
pitfalls:
  - contrast: "급성 전벽 ST 상승 경색 vs 좌각차단의 V1~V3 ST 상승"
    point: "좌각차단에서 V1~V3 의 ST 상승은 깊은 QS 와 반대 방향인 기대되는 이차 변화다. QRS 가 넓고 V6 에 q 없는 넓은 R 이 있으면 먼저 좌각차단을 읽고, 흉통·트로포닌 상승이 없으면 경색으로 읽지 않는다."
    exception: "좌각차단은 급성 허혈 변화를 가리므로, 흉통과 트로포닌 상승이 있으면 좌각차단이 있어도 급성 경색을 배제하지 않는다."
    cites: ["harrison-22: 247장 p.1872", "harrison-22: 247장 p.1873"]
    covers: ["imaging-2026-0527:B"]
  - contrast: "좌심실 비대(strain) vs 좌각차단"
    point: "좌심실 비대는 전압이 크고 R 이 큰 유도에 ST 하강·T파 역위가 붙지만 QRS 는 0.12초 미만이고 중격 q 가 남는다. QRS ≥ 0.12초에 중격 q 가 사라졌으면 좌각차단이다. 좌심실 비대는 흔히 좌각차단으로 진행한다."
    cites: ["harrison-22: 247장 p.1871"]
  - contrast: "완전 우각차단 vs 완전 좌각차단"
    point: "둘 다 QRS ≥ 0.12초. V1 끝이 위로 서는 rsR′·V6 넓은 S 면 우각차단, V1 넓은 QS·V6 q 없는 넓은 R 이면 좌각차단."
    cites: ["harrison-22: 247장 p.1871"]
  - contrast: "인공 심박동기 리듬 vs 좌각차단"
    point: "우심실 조율은 좌각차단과 같은 QRS 모양을 만든다 — QRS 앞의 뾰족한(때로 아주 작은) 조율 스파이크를 찾는다."
    cites: ["harrison-22: 247장 p.1871"]
tables:
  - id: v1-st
    section: "가르는 소견 — 폭·중격 q·ST 방향"
    title: "V1~V3 ST 상승 — 무엇이 가르나"
    role: differential
    span: column
    columns: ["판독", "QRS", "ST·임상"]
    rows:
      - ["완전 좌각차단", "≥ 120 ms, V1 넓은 QS, V6 q 없는 넓은 R [[harrison-22: 247장 p.1871]]", "ST-T 가 QRS 마지막 굴절과 반대 — V1~V3 ST 상승은 이차 변화 [[harrison-22: 247장 p.1872]]"]
      - ["급성 전벽 경색", "대개 넓지 않음", "흉통·트로포닌 상승, ST 상승은 일차 변화(원문 미대조: 상호 하강 양상)"]
      - ["좌심실 비대", "< 120 ms, 전압 증가, 중격 q 유지", "R 큰 유도에 ST 하강·T 역위, V1~V2 ST 상승 흔함 [[harrison-22: 247장 p.1873]]"]
      - ["우심실 조율", "좌각차단과 같은 모양 + 앞의 조율 스파이크 [[harrison-22: 247장 p.1871]]", "이차 ST-T 변화 [[harrison-22: 247장 p.1872]]"]
criteria:
  - id: lbbb-pattern
    name: 좌각차단의 모양
    kind: 진단 기준
    population: "넓은 QRS 의 12유도 심전도"
    statement: "완전 각차단은 가장 넓은 QRS 가 120 ms 이상이다. 좌각차단은 주 QRS 벡터가 왼쪽·뒤로 향하고 중격 탈분극이 오른쪽에서 왼쪽으로 바뀌어 V1 에 넓고 주로 음성인 QS, V6 에 전부 양성인 R 을 만든다 [[harrison-22: 247장 p.1871]]"
    exceptions: "우심실 조율도 같은 모양을 만들며 조율 스파이크가 앞선다 [[harrison-22: 247장 p.1871]]"
    source: harrison-22
    basis: current
    exams: [kmle, usmle]
  - id: secondary-st
    name: 이차성 ST-T 변화
    kind: 진단 기준
    population: "각차단의 심전도"
    statement: "각차단에서는 T파가 QRS 마지막 굴절과 반대 극성이다 — 바뀐 탈분극 순서가 재분극 순서를 바꾼 결과다. 좌각차단의 V1·V2 ST 상승·큰 T파는 허혈 없이도 흔하다 [[harrison-22: 247장 p.1872]] [[harrison-22: 247장 p.1873]]"
    exceptions: "일차 변화(허혈·전해질·디곡신)가 함께 있을 수 있다 — 좌각차단에서 오른쪽 가슴 유도의 T파 역위는 허혈의 표지일 수 있다 [[harrison-22: 247장 p.1872]]. 좌각차단은 급성 허혈 변화를 가린다 [[harrison-22: 247장 p.1873]]"
    source: harrison-22
    basis: current
    exams: [kmle, usmle]
sources:
  - id: harrison-22
    org: "McGraw Hill"
    title: "Harrison's Principles of Internal Medicine, 22nd ed. — Chapter 247: Electrocardiography"
    kind: textbook
    year: 2025
    citation: "Harrison's Principles of Internal Medicine, 22e. 247장 p.1871–1874"
    checked_at: 2026-11-03
    checked: "드라이브 22판 장별 문서 H22_247 본문 대조 — 좌심실 비대의 strain(R 큰 유도 ST 하강·T 역위), 좌심실 비대는 흔히 불완전·완전 좌각차단으로 진행, 완전 각차단 QRS ≥ 120 ms, 좌각차단 주 벡터 왼쪽·뒤·중격 탈분극 오른쪽→왼쪽, V1 넓은 QS·V6 R, 우심실 조율이 같은 모양+스파이크, 좌각차단은 관상동맥질환·고혈압성 심질환·대동맥판 질환·심근병증의 표지(p.1871–1872) · 각차단의 이차 ST-T(T파는 QRS 마지막 굴절과 반대), 좌각차단에서 오른쪽 가슴 유도 T파 역위는 허혈 표지일 수 있음(p.1872) · 좌각차단·조율·WPW 가 급성 허혈 변화를 가림, V1·V2 ST 상승·큰 T파는 좌각차단·좌심실 비대에서 허혈 없이도 흔함(p.1873) · 표 247-1 ST 상승 감별에 좌심실 비대/좌각차단(p.1874). Sgarbossa 기준·급성 경색의 상호 하강은 이 장에서 확인하지 않았다"
    verified: text
diagram:
  title: "넓은 QRS 와 V1~V3 ST 상승 — 경색인가 좌각차단인가"
  nodes:
    - {id: start, kind: start, text: "V1~V3 ST 상승이 있는 심전도"}
    - {id: width, kind: decision, text: "QRS 가 120 ms 이상인가?"}
    - {id: measure, kind: info, text: "가장 넓은 유도에서 QRS 폭을 잰다"}
    - {id: narrow, kind: alert, text: "좁은 QRS ST 상승 — 급성 경색 평가"}
    - {id: shape, kind: decision, text: "V1 넓은 QS, V6 q 없는 넓은 R?"}
    - {id: other, kind: end, text: "다른 넓은 QRS — 우각차단·조율 등"}
    - {id: clin, kind: decision, text: "흉통이나 트로포닌 상승이 있나?"}
    - {id: lbbb, kind: end, text: "좌각차단 — ST 상승은 이차 변화"}
    - {id: acs, kind: alert, text: "좌각차단 + 급성 경색 의심 — 응급 평가"}
  edges:
    - {from: start, to: width}
    - {from: width, to: shape, label: "예"}
    - {from: width, to: narrow, label: "아니오"}
    - {from: width, to: measure, label: "모르겠음"}
    - {from: measure, to: shape, label: "≥ 120 ms"}
    - {from: measure, to: narrow, label: "< 120 ms"}
    - {from: shape, to: clin, label: "예"}
    - {from: shape, to: other, label: "아니오"}
    - {from: clin, to: lbbb, label: "없음"}
    - {from: clin, to: acs, label: "있음"}
diagram_notes:
  - "QRS 앞에 뾰족한 스파이크가 있으면 우심실 조율 — 좌각차단과 같은 모양이다 [[harrison-22: 247장 p.1871]]."
  - "좌각차단은 급성 허혈 변화를 가린다 — 흉통·트로포닌이 있으면 좌각차단이 있어도 경색을 배제하지 않는다 [[harrison-22: 247장 p.1873]]."
  - "좌각차단을 읽었으면 원인 심질환(관상동맥질환·고혈압성 심질환·대동맥판 질환·심근병증)을 찾는다 [[harrison-22: 247장 p.1871–1872]]."
checks:
  - q: "QRS 0.14초, V1 깊은 QS 에 ST 상승, V6 q 없는 넓은 R 에 ST 하강·T 역위. 흉통 없음·트로포닌 정상. 판독은?"
    a: "완전 좌각차단. ST-T 가 QRS 주 방향과 반대로 선 이차 변화라 전벽 경색으로 읽지 않는다."
  - q: "좌각차단에서 V6 의 중격 q 파가 사라지는 이유는?"
    a: "좌각이 막히면 중격 탈분극이 오른쪽에서 왼쪽으로 바뀌어, 정상의 왼쪽→오른쪽 초기 벡터가 만들던 작은 q 가 없어진다."
variants:
  - id: v1
    of: imaging-2026-0527
    flip: true
    changed: "흉통 없음·트로포닌 정상·QRS 0.14초 V1 QS → 1시간 지속 흉통·트로포닌 상승·QRS 0.09초에 V1~V4 ST 상승과 하벽 ST 하강 ⇒ 정답이 좌각차단에서 급성 전벽 ST 상승 경색으로"
    context: "같은 고령 남성, 소견을 글로 바꾼 변형(그림 없음)"
    stem: "An 84-year-old man is brought to the emergency department 1 hour after the onset of crushing substernal chest pain with diaphoresis. He has hypertension treated with amlodipine. Blood pressure is 102/64 mm Hg and pulse is 96/min. Crackles are heard at both lung bases. Serum troponin concentration is increased and is higher on repeat measurement 1 hour later. A 12-lead ECG shows sinus rhythm with a QRS duration of 90 ms, ST-segment elevation of 3–4 mm in leads V1 through V4 over upright R waves, and ST-segment depression in leads II, III and aVF. Small q waves are present in leads I and V6. Which of the following is the most likely interpretation of this ECG?"
    choices: ["A. Left bundle branch block", "B. Acute anterior ST-elevation myocardial infarction", "C. Right bundle branch block", "D. Left ventricular hypertrophy with strain pattern", "E. Ventricular preexcitation"]
    answer: "B"
    explanation: "The QRS is narrow (90 ms) and septal q waves are preserved, so there is no bundle branch block to explain the ST changes. ST elevation in V1–V4 with inferior ST depression, ongoing chest pain and a rising troponin indicate acute anterior ST-elevation infarction — here the ST elevation is a primary change, not a secondary change to abnormal depolarization."
    kind: application
  - id: v2
    of: imaging-2026-0527
    flip: false
    changed: "85세 남자·3개월 운동 시 호흡곤란 → 72세 여자·수술 전 검사, 심전도 소견을 글로 제시 ⇒ QRS ≥ 0.12초·V1 넓은 QS 에 반대 방향 ST 상승·V6 q 없는 넓은 R·흉통 없음·트로포닌 정상이라는 결정 단서는 같아 답은 그대로 좌각차단"
    context: "겉모습만 바꾼 글 변형(그림 없음)"
    stem: "A 72-year-old woman comes to the physician for a preoperative evaluation before elective hip replacement. She has had severe aortic stenosis treated with transcatheter aortic valve replacement 1 year ago. She has no chest pain and walks 1 km daily without symptoms. Blood pressure is 132/78 mm Hg and pulse is 72/min. Serum troponin concentration is within the reference range. A 12-lead ECG shows sinus rhythm with a QRS duration of 150 ms and no pacing spikes. Leads V1 through V3 show deep, wide QS complexes with 2-mm ST-segment elevation, and leads I, aVL and V6 show broad, notched R waves without q waves, with ST-segment depression and T-wave inversion. Which of the following is the most likely interpretation of this ECG?"
    choices: ["A. Acute anterior ST-elevation myocardial infarction", "B. Right bundle branch block", "C. Left bundle branch block", "D. Left ventricular hypertrophy with strain pattern", "E. Ventricular paced rhythm"]
    answer: "C"
    explanation: "The age, sex and setting differ, but the deciding clues are the same: QRS ≥ 120 ms, deep wide QS in V1–V3 and broad notched R without q in I, aVL and V6. The ST-T changes point opposite to the main QRS deflection, the expected secondary change of LBBB; she has no chest pain and a normal troponin. No pacing spikes precede the QRS, so this is not a paced rhythm. Aortic valve disease, including after transcatheter replacement, is a recognized setting for LBBB."
    kind: application
figures:
- id: f1
  file: docs/assets/figures/ptbxl-06661.png
  kind: ecg
  at: 기전 — 늦게 깨는 좌심실
  shows: 완전 좌각차단 — 넓은 QRS, V1~V3 깊은 QS 와 반대 방향 ST 상승
  look_for:
  - V1~V3 의 깊고 넓은 QS 와 그 뒤 위로 솟은 ST·T
  - I·aVL 의 q 없이 넓고 갈라진 R
  label: complete left bundle branch block (SCP CLBBB, 가능도 100)
  label_basis: dataset_expert
  reference: 심장내과 전문의의 SCP-ECG 판독을 두 번째 전문의가 검증 — 해당 진술의 가능도 100 인 기록만
  paper: Wagner P 외. PTB-XL, a large publicly available electrocardiography dataset. Sci Data 2020;7:154
  doi: 10.1038/s41597-020-0495-6
  credit: PTB-XL ECG dataset v1.0.3 (PhysioNet, CC BY 4.0) · record 6661
  license: Creative Commons Attribution 4.0 International
  url: https://physionet.org/content/ptb-xl/1.0.3/records500/06000/#files-panel
  asset: PTBXL-06661
  paper_cited_by: 1213
  from_question: imaging-2026-0527
---

## 판단 — 왜 경색이 아니라 좌각차단인가
- **폭부터**: QRS ≥ 120 ms 면 각차단을 먼저 읽는다 [[harrison-22: 247장 p.1871]]. 각차단이 있으면 ST-T 는 QRS 에 끌려간다.
- **모양**: V1 넓은 QS(주로 음성), I·aVL·V6 q 없는 넓은 R(전부 양성)은 좌각차단이다 [[harrison-22: 247장 p.1871]].
- **ST 방향**: 깊은 QS 유도(V1~V3)의 ST 상승은 QRS 와 반대 방향인 이차 변화다 [[harrison-22: 247장 p.1872]]. 흉통이 없고 트로포닌이 변하지 않으면 경색이 아니다.

## 기전 — 늦게 깨는 좌심실
정상에서는 좌각에서 시작한 중격 탈분극이 왼쪽→오른쪽으로 가서 V1 의 작은 r, V6 의 작은 중격 q 를 만든다. 좌각이 막히면 우각이 먼저 우심실과 중격을 깨우고, 중격 탈분극은 오른쪽→왼쪽으로 바뀐다. 좌심실은 근육을 따라 천천히 늦게 탈분극하므로 주 QRS 벡터가 왼쪽·뒤로 향한다 — V1 은 넓은 QS, V6 은 중격 q 없이 넓고 갈라진 R 이 된다 [[harrison-22: 247장 p.1871]]. 탈분극 순서가 바뀌면 재분극 순서도 바뀌어 ST-T 가 QRS 마지막 굴절과 반대로 선다 — 이것이 「이차성」 변화다. 허혈·전해질·디곡신처럼 심근 자체의 전기 성질이 바뀐 「일차성」 변화와 다르다 [[harrison-22: 247장 p.1872]].

## 가르는 소견 — 폭·중격 q·ST 방향
- V1·V2 의 ST 상승과 큰 양성 T파는 허혈이 없어도 좌각차단·좌심실 비대에서 흔하다 [[harrison-22: 247장 p.1873]]. 표 247-1 의 ST 상승 감별에도 「좌심실 비대/좌각차단」이 들어 있다 [[harrison-22: 247장 p.1874]].
- 좌심실 비대는 QRS 가 0.12초 미만이고 중격 q 가 남는다. 좌심실 비대는 흔히 불완전·완전 좌각차단으로 진행한다 [[harrison-22: 247장 p.1871]].
- 우심실 조율은 좌각차단과 같은 모양이므로 QRS 앞의 조율 스파이크를 찾는다 [[harrison-22: 247장 p.1871]].

## 권고와 예외
- 좌각차단은 급성 허혈·경색의 심전도 변화를 가린다 — 흉통과 트로포닌 상승이 있으면 심전도만으로 경색을 배제하지 않는다 [[harrison-22: 247장 p.1873]].
- 좌각차단에서 오른쪽 가슴 유도의 T파 역위(기대되는 방향과 다름)는 허혈 등 다른 이상의 표지일 수 있다 [[harrison-22: 247장 p.1872]].
- 좌각차단은 관상동맥질환(흔히 좌심실 기능 저하 동반)·고혈압성 심질환·대동맥판 질환(경피 대동맥판 치환 뒤 포함)·심근병증의 표지다 — 원인 심질환을 평가한다 [[harrison-22: 247장 p.1871–1872]].

## 시험 쟁점 — 충돌·맥락·새 근거
- 해당 없음(대조: 해리슨 22판 247장 p.1871–1874). 좌각차단 속 급성 경색을 가르는 Sgarbossa 기준은 해리슨 이 장에 없어 대조하지 않았다.
