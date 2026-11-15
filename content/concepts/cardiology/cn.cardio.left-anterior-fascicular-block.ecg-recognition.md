---
id: cn.cardio.left-anterior-fascicular-block.ecg-recognition
type: concept
topic: Cardiology
see_also: [cn.cardio.qrs-axis.limb-lead-polarity, cn.cardio.complete-rbbb.ecg-recognition]
date: 2026-11-15
updated: 2026-11-15
version: 2
outline: h240            # 해리슨 21판 240장 Electrocardiography → 22판 247장
confidence: medium
review_status: unreviewed
note_form: 2
title: "좌각전섬유속차단 — 좁은 QRS 의 심한 좌축편위"
objective: "좁은 QRS 에 −45° 보다 심한 좌축편위(I 양성, II·III·aVF rS)를 좌각전섬유속차단으로 읽고 좌심실비대·하벽경색과 가른다"
objective_kind: 진단
condition: 좌각전섬유속차단(left anterior fascicular block)
exams: [usmle, kmle]
summary:
  - "결론: QRS 가 좁은데 축이 −45° 보다 왼쪽이면 좌각전섬유속차단 — 성인의 심한 좌축편위의 가장 흔한 원인이다."
  - "시험 단서: 무증상 고령·고혈압, 「축 이상」 검진 심전도, I·aVL 양성 + II·III·aVF 깊은 S(left anterior fascicular block)."
  - "왜: 섬유속차단은 QRS 폭을 크게 늘리지 않고 전두면 축만 옮긴다 — 각차단과 달리 QRS 가 좁다."
  - "좌심실비대는 전흉부 전압(SV1 + RV5/RV6 > 35 mm)과 높은 R 유도의 ST 하강·T 역위로 읽는다 — 축만으로 붙이지 않는다."
  - "하벽 유도가 음성일 때 첫 굴절이 작은 r 이면 섬유속차단, 병적 Q 면 하벽경색 쪽이다."
criteria:
  - id: lafb-axis
    name: 좌각전섬유속차단의 축 기준
    kind: 진단 기준
    population: "QRS 폭이 거의 정상인 좌축편위"
    statement: "섬유속차단은 QRS 폭을 크게 늘리지 않고 전두면 축만 옮긴다. 좌각전섬유속차단은 QRS 축이 −45° 보다 음이고, 성인에서 심한 좌축편위의 가장 흔한 원인이다 [[harrison-22: 247장 p.1872]]"
    exceptions: "하벽 유도의 rS·aVL 의 qR 같은 세부 형태 기준은 해리슨 본문에 없다 — AHA/ACCF/HRS 2009 권고(원문 미대조) [[?aha-ivcd-2009]]"
    source: harrison-22
    basis: current
    exams: [usmle, kmle]
  - id: lad-causes
    name: 좌축편위의 원인
    kind: 정의
    population: "성인 12유도 심전도"
    statement: "정상 QRS 축은 −30°~+100°, −30° 보다 음이면 좌축편위. 정상 변이일 수 있으나 좌심실비대·좌각전섬유속차단·하벽경색과 더 자주 연관된다 [[harrison-22: 247장 p.1870]]"
    exceptions: "−30°~−45° 의 가벼운 좌축편위는 섬유속차단 기준(−45° 초과)에 못 미친다 [[harrison-22: 247장 p.1872]]"
    source: harrison-22
    basis: current
    exams: [usmle, kmle]
sources:
  - id: harrison-22
    org: "McGraw Hill"
    title: "Harrison's Principles of Internal Medicine, 22nd ed. — Chapter 247: Electrocardiography"
    kind: textbook
    year: 2025
    citation: "Harrison's Principles of Internal Medicine, 22e. 247장 p.1868, 1870–1873"
    checked_at: 2026-11-15
    checked: "드라이브 22판 장별 문서 H22_247 본문 대조 — p.1868 전도계(좌다발가지가 앞·뒤 섬유속으로 나뉨) · p.1870 정상 QRS 축 −30°~+100°, 좌축편위 −30° 초과, 원인(정상 변이·좌심실비대·좌각전섬유속차단·하벽경색), 우축편위 원인 · p.1871 좌심실비대 전압 기준 SV1 + (RV5 또는 RV6) > 35 mm, 높은 R 유도의 ST 하강·T 역위(옛 「strain」), 사지유도 전압 RaVL + SV3 > 20/28 mm, 젊은 사람 정상 변이, 좌각차단으로 진행 · p.1872 섬유속차단은 QRS 폭을 크게 늘리지 않고 축만 옮김, 좌각전섬유속차단 축 −45° 초과·성인 심한 좌축편위 최다 원인, 좌각후섬유속차단 +110–120° 초과 · p.1873 경색 뒤 R파 감소·비정상 Q파(전벽·하벽 유도)"
    verified: text
  - id: aha-ivcd-2009
    org: "American Heart Association / American College of Cardiology Foundation / Heart Rhythm Society"
    title: "Recommendations for the Standardization and Interpretation of the Electrocardiogram, Part III: Intraventricular Conduction Disturbances"
    kind: guideline
    year: 2009
    citation: "Surawicz B, Childers R, Deal BJ, Gettes LS. Circulation 2009;119:e235-e240 (문항 해설에 적힌 권고)"
    url: "https://www.ahajournals.org/journal/circ"
    checked_at: 2026-11-15
    checked: "서지만 — 이 컨테이너에서 원문을 열지 못해 섬유속차단 형태 기준 문구를 대조하지 못했다(url 은 학술지 첫 화면, DOI·PMID 미확인)"
    verified: citation
tables:
  - id: lad-ddx
    title: "좌축편위 — 무엇이 가르나"
    role: differential
    span: column
    section: "가르는 소견 — 축 다음에 볼 곳"
    columns: ["판독", "QRS 폭·축", "가르는 소견"]
    rows:
      - ["좌각전섬유속차단", "좁음, −45° 보다 왼쪽 [[harrison-22: 247장 p.1872]]", "하벽 유도 rS(첫 굴절 작은 r) [[?aha-ivcd-2009]]"]
      - ["좌심실비대(strain)", "좁거나 약간 넓음, 축은 다양", "SV1 + RV5/6 > 35 mm, 높은 R 유도 ST 하강·T 역위 [[harrison-22: 247장 p.1871]]"]
      - ["하벽경색(오래된)", "좁음, 좌축 쪽일 수 있음 [[harrison-22: 247장 p.1870]]", "II·III·aVF 비정상 Q파 [[harrison-22: 247장 p.1873]]"]
      - ["좌각차단", "≥ 120 ms", "넓은 QRS — 섬유속차단은 폭을 크게 늘리지 않는다 [[harrison-22: 247장 p.1872]]"]
pitfalls:
  - contrast: "좌심실비대(strain) vs 좌각전섬유속차단 — 「고혈압 + 좌축편위 = 좌심실비대」"
    point: "좌축편위는 좌심실비대에서도 보이지만 좌심실비대는 전흉부 전압(SV1 + RV5/RV6 > 35 mm)과 높은 R 유도의 ST 하강·T 역위로 붙이는 진단이다 [[harrison-22: 247장 p.1871]]. 전압·재분극 이상 없이 좁은 QRS 와 −45° 보다 심한 좌축편위만 있으면 좌각전섬유속차단이다 [[harrison-22: 247장 p.1872]]."
    exception: "둘은 함께 있을 수 있다 — 전압 기준과 ST-T 변화가 있으면 좌심실비대를 따로 붙인다 [[harrison-22: 247장 p.1871]]."
    covers: ["imaging-2026-0668:A"]
  - contrast: "하벽 유도 음성 = 오래된 하벽경색?"
    point: "경색은 비정상 Q파를 남긴다 [[harrison-22: 247장 p.1873]]. 하벽 유도가 작은 r 로 시작해 깊은 S 로 끝나면(rS) 초기 하벽 벡터가 살아 있는 것이라 섬유속차단 쪽이다 [[?aha-ivcd-2009]]."
  - contrast: "좌축편위면 모두 좌각전섬유속차단?"
    point: "−30°~−45° 는 좌축편위이지만 섬유속차단 기준(−45° 초과)에 못 미친다. 정상 변이·좌심실비대·하벽경색도 좌축편위를 만든다 [[harrison-22: 247장 p.1870]]."
diagram:
  title: "좌축편위 심전도 — 어떤 판독인가"
  nodes:
    - {id: start, kind: start, text: "I 양성 · II·aVF 음성(좌축편위)"}
    - {id: width, kind: decision, text: "QRS ≥ 120 ms?"}
    - {id: lbbb, kind: end, text: "각차단 쪽(좌각차단 등)"}
    - {id: q, kind: decision, text: "II·III·aVF 첫 굴절이 Q파?"}
    - {id: imi, kind: end, text: "오래된 하벽경색"}
    - {id: info, kind: info, text: "전흉부 전압·ST-T 함께 확인"}
    - {id: lvh, kind: decision, text: "전압 기준 + ST 하강·T 역위?"}
    - {id: lvhend, kind: end, text: "좌심실비대(strain)"}
    - {id: deg, kind: decision, text: "축 −45° 보다 왼쪽?"}
    - {id: lafb, kind: end, text: "좌각전섬유속차단"}
    - {id: mild, kind: end, text: "가벼운 좌축편위 — 정상 변이 등"}
  edges:
    - {from: start, to: width}
    - {from: width, to: lbbb, label: "예"}
    - {from: width, to: q, label: "아니오"}
    - {from: q, to: imi, label: "Q파"}
    - {from: q, to: info, label: "작은 r"}
    - {from: info, to: lvh}
    - {from: lvh, to: lvhend, label: "있음"}
    - {from: lvh, to: deg, label: "없음"}
    - {from: deg, to: lafb, label: "예"}
    - {from: deg, to: mild, label: "아니오"}
diagram_notes:
  - "좌심실비대 전압: SV1 + (RV5 또는 RV6) > 35 mm, 사지유도 RaVL + SV3 > 20 mm(여자)·> 28 mm(남자). 젊은 사람·운동선수는 정상 변이로 전압이 높다 [[harrison-22: 247장 p.1871]]."
  - "좌심실비대와 좌각전섬유속차단은 함께 있을 수 있다 — 갈래가 하나로 끝나지 않으면 둘 다 적는다."
  - "aVL 의 qR, 하벽 rS 의 세부 기준은 AHA/ACCF/HRS 2009 권고에 있다(원문 미대조) [[?aha-ivcd-2009]]."
checks:
  - q: "좌각전섬유속차단의 축 기준과 QRS 폭은?"
    a: "축 −45° 보다 왼쪽, QRS 폭은 크게 늘지 않는다(좁다)."
  - q: "좌축편위에서 좌심실비대를 붙이려면 무엇이 더 있어야 하나?"
    a: "전흉부 전압 기준(SV1 + RV5/6 > 35 mm 등)과 높은 R 유도의 ST 하강·T 역위."
  - q: "하벽 유도 음성 QRS 에서 하벽경색과 섬유속차단을 가르는 것은?"
    a: "첫 굴절 — 병적 Q파면 경색, 작은 r 로 시작하면 섬유속차단."
variants:
  - id: v1
    of: imaging-2026-0668
    flip: true
    changed: "좁은 QRS·심한 좌축편위·전흉부 전압 정상 → SV1 + RV5 = 44 mm, V5·V6 의 하향 경사 ST 하강과 비대칭 T 역위, 축 −15° ⇒ 정답이 좌각전섬유속차단에서 좌심실비대(strain)로"
    context: "같은 고혈압 고령 여성, 전압·재분극 단서를 넣고 축 이상을 뺀 글 변형(그림 없음)"
    stem: "A 66-year-old woman comes to the clinic because a screening ECG at a health fair was reported as abnormal. She has had poorly controlled hypertension for 20 years. She has no chest pain, dyspnea, palpitations, or syncope and has never had a myocardial infarction. Her blood pressure is 168/96 mm Hg and pulse is 72/min. A sustained apical impulse is palpated. The ECG shows sinus rhythm, a QRS duration of 100 ms, and a frontal QRS axis of −15°. The S wave in V1 plus the R wave in V5 measures 44 mm, and V5 and V6 show downsloping ST-segment depression with asymmetric T-wave inversion. Leads II, III, and aVF begin with a small r wave. Which of the following is the most likely interpretation of this ECG?"
    choices: ["A. Left ventricular hypertrophy with strain", "B. Left anterior fascicular block", "C. Left posterior fascicular block", "D. Left bundle branch block", "E. Old inferior myocardial infarction"]
    answer: "A"
    explanation: "The deciding change is voltage plus repolarization: SV1 + RV5 above 35 mm with downsloping ST depression and asymmetric T inversion in the tall-R leads is left ventricular hypertrophy with the former 'strain' pattern. The axis of −15° is within normal limits, so the criterion for left anterior fascicular block (more negative than −45°) is not met, the QRS is not wide enough for a bundle branch block, and the inferior leads start with r rather than Q."
    kind: application
  - id: v2
    of: imaging-2026-0668
    flip: false
    changed: "66세 여성·검진 심전도 → 58세 남성·대장 수술 전 심전도, 소견을 글로 제시 ⇒ 좁은 QRS·축 −60°·하벽 rS·전압 정상이라는 결정 단서는 같아 답은 그대로 좌각전섬유속차단"
    context: "겉모습만 바꾼 글 변형(그림 없음)"
    stem: "A 58-year-old man has a preoperative ECG before elective colon surgery. He has type 2 diabetes mellitus and no cardiac symptoms; he walks 3 miles daily without difficulty. His blood pressure is 128/78 mm Hg and pulse is 66/min. The ECG shows sinus rhythm with a QRS duration of 96 ms and a frontal QRS axis of −60°. Lead I and aVL are predominantly positive, while II, III, and aVF each begin with a small r wave followed by a deep S wave. Precordial voltages are normal, and there are no ST-segment or T-wave abnormalities. Which of the following is the most likely interpretation of this ECG?"
    choices: ["A. Left ventricular hypertrophy with strain", "B. Left anterior fascicular block", "C. Left posterior fascicular block", "D. Left bundle branch block", "E. Old inferior myocardial infarction"]
    answer: "B"
    explanation: "The patient and setting changed, but the deciding clues did not: a narrow QRS with an axis more negative than −45°, inferior rS complexes, and no voltage or ST-T criteria for hypertrophy. That is left anterior fascicular block, the most common cause of marked left axis deviation in adults. The preserved initial r in the inferior leads argues against an old inferior infarction."
    kind: application
figures:
- id: f1
  file: docs/assets/figures/ptbxl-01766.png
  kind: ecg
  at: 기전 — 앞 섬유속이 막히면 축이 위로
  shows: 좌각전섬유속차단 — 좁은 QRS 와 심한 좌축편위
  look_for:
  - I·aVL 은 높은 R 로 양성
  - II·III·aVF 는 작은 r 뒤 깊은 S(rS)
  - QRS 폭이 좁다
  label: left anterior fascicular block (SCP LAFB, 가능도 100)
  label_basis: dataset_expert
  reference: 심장내과 전문의의 SCP-ECG 판독을 두 번째 전문의가 검증 — 해당 진술의 가능도 100 인 기록만
  paper: Wagner P 외. PTB-XL, a large publicly available electrocardiography dataset. Sci Data 2020;7:154
  doi: 10.1038/s41597-020-0495-6
  credit: PTB-XL ECG dataset v1.0.3 (PhysioNet, CC BY 4.0) · record 1766
  license: Creative Commons Attribution 4.0 International
  url: https://physionet.org/content/ptb-xl/1.0.3/records500/01000/#files-panel
  asset: PTBXL-01766
  paper_cited_by: 1213
---

## 판단 — 왜 좌각전섬유속차단인가
- **폭부터**: QRS 가 좁다 — 섬유속차단은 폭을 크게 늘리지 않고 축만 옮긴다 [[harrison-22: 247장 p.1872]]. 120 ms 를 넘으면 각차단을 먼저 본다.
- **축의 정도**: I 양성·II·aVF 음성이면 좌축편위이고, −45° 보다 왼쪽이면 좌각전섬유속차단 기준에 든다 [[harrison-22: 247장 p.1870]] [[harrison-22: 247장 p.1872]].
- **비대는 따로 확인**: 좌심실비대는 전흉부 전압과 ST-T 로 붙인다 — 축만으로 붙이지 않는다 [[harrison-22: 247장 p.1871]].
- **경색은 Q파로**: 하벽 유도의 첫 굴절이 Q파면 하벽경색, 작은 r 이면 섬유속차단 쪽이다 [[harrison-22: 247장 p.1873]] [[?aha-ivcd-2009]].

## 기전 — 앞 섬유속이 막히면 축이 위로
좌다발가지는 앞·뒤 두 섬유속으로 나뉜다 [[harrison-22: 247장 p.1868]]. 앞 섬유속은 좌심실의 앞·위쪽 벽을, 뒤 섬유속은 아래·뒤쪽 벽을 먼저 흥분시킨다. 앞 섬유속이 막히면 아래·뒤쪽 벽이 먼저 흥분해 처음 벡터가 잠깐 아래로 향하고(하벽 유도의 작은 r), 앞·위쪽 벽은 심근을 거쳐 늦게 흥분해 주된 벡터가 왼쪽 위로 향한다(하벽 유도의 깊은 S, I·aVL 양성) — 세부 형태는 권고 원문 미대조 [[?aha-ivcd-2009]]. 다발가지 본줄기는 살아 있어 QRS 폭은 크게 늘지 않고 전두면 축만 옮겨 간다 [[harrison-22: 247장 p.1872]]. 반대로 하벽경색은 하벽의 초기 벡터 자체를 없애 비정상 Q파를 남긴다 [[harrison-22: 247장 p.1873]].

## 가르는 소견 — 축 다음에 볼 곳
- 좌축편위 자체는 정상 변이·좌심실비대·좌각전섬유속차단·하벽경색 모두에서 생긴다 [[harrison-22: 247장 p.1870]] — 그래서 축 다음에 폭·첫 굴절·전압·ST-T 를 차례로 본다.
- **음성 결과의 해석 한계**: 좌심실비대의 전압 기준은 중년 이후·비만·흡연자에서 민감도가 낮다 [[harrison-22: 247장 p.1871]] — 전압이 정상이라고 비대가 없다는 뜻은 아니며, 비대 여부는 심초음파로 본다.

## 권고와 예외
- 무증상 단독 좌각전섬유속차단은 이 문항처럼 판독 문제다. 진행·처치 판단은 이 정리본에서 대조하지 않았다.
- 우각차단과 함께 오면(이섬유속차단) 의미가 달라진다 — cn.cardio.complete-rbbb.ecg-recognition 참고.

## 시험 쟁점 — 충돌·맥락·새 근거
- 해당 없음(대조: 해리슨 22판 247장 p.1868·1870–1873)
