---
id: cn.em.trauma-primary-survey.next-priority-intervention
type: concept
topic: Emergency Medicine
see_also: [General Surgery]
date: 2026-11-20
updated: 2026-11-20
version: 1
outline: em.trauma   # 기본틀 슬롯(content/outline/subjects.yaml) — 응급의학과 손 슬롯 「외상 초기 평가(ATLS)」
confidence: medium
review_status: unreviewed
note_form: 2            # 판형 2(2026-09-25) — 기본틀 빈 슬롯으로 쓴 정리본(오답 연결 없음)
title: "다발 외상 — 막힌 칸부터, 대량 외출혈은 먼저"
objective: "다발 외상 환자의 일차 평가(대량 외출혈 → 기도·경추 → 호흡 → 순환·출혈 → 신경 → 노출)에서 제시된 소견이 어느 칸을 막는지 찾아, 지금 먼저 할 처치를 고른다"
objective_kind: 다음 처치
condition: 다발 외상(multiple trauma)의 일차 평가(primary survey) — 대량 외출혈 · 기도 폐쇄 · 긴장성 기흉 · 심장눌림증 · 대량 혈흉 · 골반 출혈
exams: [kmle, usmle]
summary:
  - "결론: 앞 칸이 막혔으면 뒤 칸 검사를 미루고 그 자리에서 푼다 — 대량 외출혈 → 기도 → 호흡 → 순환 순."
  - "시험 단서: 사지 대량 출혈, GCS ≤8, 한쪽 호흡음 소실+저혈압, eFAST 심낭액, 불안정 골반+쇼크(primary survey)."
  - "왜: 기도·호흡이 막히면 산소가, 출혈이 계속되면 운반할 혈액이 없어진다 — 원인 진단보다 생명 처치가 먼저."
  - "긴장성 기흉은 임상 진단 — 흉부 X선을 기다리지 않고 바늘 감압한다."
  - "출혈이 멎기 전 소생 목표는 수축기 80–90 mmHg — 중증 뇌손상(GCS ≤8)은 평균동맥압 ≥80 mmHg."
pitfalls:
  - contrast: "긴장성 기흉 — 흉부 X선으로 확인한 뒤 감압?"
    point: "진행하는 호흡곤란·저혈압·한쪽 호흡음 소실로 강하게 의심되면 영상 확인을 기다리지 않고 즉시 바늘 감압한다 — 영상을 기다리는 동안 폐쇄성 쇼크가 진행한다 [[cn-prehospital-2026: Recommendation — Breathing]]."
  - contrast: "사지에서 피가 뿜어도 기도부터?"
    point: "생명을 위협하는 외출혈은 기도보다 먼저 직접 압박·지혈대로 막는다(<C>ABCDE · xABCDE) [[euro-bleeding-2023: R5 Rationale]] [[cn-prehospital-2026: Recommendation — X]]. 순서 논쟁은 시험 쟁점 Z1."
  - contrast: "출혈성 쇼크 — 혈압이 정상이 될 때까지 수액?"
    point: "출혈이 멎기 전에는 제한 수액으로 수축기 80–90 mmHg(평균 50–60)를 목표로 한다. 혈압을 정상으로 올리면 생긴 혈전이 떨어져 출혈이 늘 수 있다 [[euro-bleeding-2023: R13]] [[cn-prehospital-2026: Recommendation — Circulation]]. 중증 뇌손상은 예외(평균 ≥80 mmHg)."
  - contrast: "혈압·첫 혈색소가 정상 = 큰 출혈 없음?"
    point: "젊은 환자는 혈액 손실이 30 %를 넘을 때까지 혈압을 유지할 수 있고, 첫 혈색소 정상은 초기 출혈을 가린다 — 쇼크지수(맥박/수축기 ≥0.9–1.0)와 반복 측정으로 본다 [[cn-prehospital-2026: Recommendation — TXA]] [[euro-bleeding-2023: R5 Rationale]] [[euro-bleeding-2023: R9]]."
  - contrast: "골반 결속대는 장골능 높이에?"
    point: "결속대는 장골능이 아니라 큰돌기(greater trochanter) 높이에 두고, 무릎을 모으고 발목을 안으로 돌린 뒤 조인다 [[cn-prehospital-2026: Recommendation — Pelvic binder]]."
  - contrast: "트라넥삼산은 저혈압이 생긴 뒤에?"
    point: "출혈 중이거나 큰 출혈 위험이 있으면 손상 후 3시간 안에 가능한 한 빨리 준다 — 1 g 을 10분에 걸쳐, 이어 1 g 을 8시간 [[euro-bleeding-2023: R23]]. 3시간 이후에는 효과가 없거나 해로울 수 있다 [[cn-prehospital-2026: Recommendation — TXA]]."
  - contrast: "Beck 세 징후가 없으면 심장눌림증 배제?"
    point: "고전적인 Beck 세 징후(저혈압 포함)는 흔히 나타나지 않는다 — 외상 환자의 심낭액은 eFAST 로 직접 본다 [[alerhand-tamponade-2022: Abstract]] [[bella-efast-2025: 3.3 Pericardial effusion]]."
tables:
  - id: blocks
    section: "가르는 소견 — 어느 칸이 막혔나"
    title: "일차 평가 — 소견 → 막힌 칸 → 지금 할 처치"
    role: treatment
    span: column
    columns: ["소견", "칸", "지금 할 처치"]
    rows:
      - ["사지·접합부에서 생명을 위협하는 외출혈", "x / <C>", "직접 압박 → 안 되면 지혈대(감은 시각 기록), 접합부는 상처 채움+최소 3분 압박 [[euro-bleeding-2023: R2]] [[cn-prehospital-2026: Recommendation — X]]"]
      - ["기도 폐쇄 · 의식 저하(GCS ≤8) · 저환기 · 저산소", "A", "지체 없이 기관삽관 또는 다른 기도 확보 — 경추 손상 의심이면 손으로 일직선 고정 [[euro-bleeding-2023: R3]] [[cn-prehospital-2026: Recommendation — Airway]]"]
      - ["진행하는 호흡곤란 + 저혈압 + 한쪽 호흡음 소실", "B", "긴장성 기흉 — 영상 없이 바늘 감압, 실패하면 손가락 흉강창 등 확실한 감압 [[cn-prehospital-2026: Recommendation — Breathing]]"]
      - ["외상 + 저혈압 + eFAST 심낭액", "C", "심장눌림증 — 수혈하며 응급 감압. 심한 흉부 외상의 혈심낭은 응급 수술 적응 [[alerhand-tamponade-2022: Abstract]]"]
      - ["저혈압 + eFAST 흉강액", "C", "혈흉 — 흉관 삽입(배액·환기) 후 출혈량으로 수술 판단 [[feenstra-chest-tube-2018: Background]] [[bella-efast-2025: 3.4]]"]
      - ["불안정 골반 + 설명되지 않는 쇼크", "C", "골반 결속대 → 가능한 한 빨리 골반 고리 고정, 계속 출혈이면 복막외 채움·혈관색전 [[euro-bleeding-2023: R20]] [[euro-bleeding-2023: R21]]"]
      - ["분명한 출혈원 + 극단적 출혈성 쇼크", "C", "즉시 출혈 조절 시술(수술) — 검사를 더 하지 않는다 [[euro-bleeding-2023: R6]]"]
    note: "출혈원이 불분명하지만 즉시 조절할 필요가 없으면 eFAST·조영 전신 CT 로 찾는다 [[euro-bleeding-2023: R7]] [[euro-bleeding-2023: R8]]. 대량 혈흉의 개흉 기준 수치(배액량)는 읽은 출처에 없어 싣지 않았다(검토 항목)."
criteria:
  - id: permissive-hypotension
    name: 출혈 조절 전 소생 목표(허용 저혈압)
    kind: 치료 목표
    population: "출혈이 멎지 않은 외상 환자"
    statement: "제한 수액 전략으로 수축기 80–90 mmHg(평균동맥압 50–60 mmHg)를 큰 출혈이 멎을 때까지 목표로 한다. 수액만으로 목표에 못 미치면 노르에피네프린을 더한다 [[euro-bleeding-2023: R13]] [[euro-bleeding-2023: R14]]"
    exceptions: "중증 외상성 뇌손상(GCS ≤8)은 평균동맥압 ≥80 mmHg [[euro-bleeding-2023: R13]]. 척수손상도 금기이고, 노인·만성 고혈압은 신중히 [[euro-bleeding-2023: R13 Rationale]]"
    source: euro-bleeding-2023
    basis: current
    exams: [kmle, usmle]
sources:
  - id: euro-bleeding-2023
    org: "Task Force for Advanced Bleeding Care in Trauma (Rossaint R, Afshari A, Bouillon B, et al.)"
    title: "The European guideline on management of major bleeding and coagulopathy following trauma: sixth edition"
    kind: guideline
    year: 2023
    citation: "Crit Care 2023;27(1):80"
    doi: "10.1186/s13054-023-04327-7"
    pmid: "36859355"
    url: "https://pmc.ncbi.nlm.nih.gov/articles/PMC9977110/"
    checked_at: 2026-11-20
    checked: "PMC9977110 전문(PubMed MCP)에서 권고 R1–R39 문장 전부와 R2·R5·R6·R13·R20·R21 근거 절을 읽음 — R2 국소 압박·보조 지혈대, R3 기도 폐쇄·GCS ≤8·저환기·저산소면 지체 없이 삽관·정상 환기, R5 근거 절 「ATLS ABCDE 가 <C>ABCDE 로 바뀌었다」·쇼크지수 0.5–0.7 정상·≥0.9–1.0 대량수혈 연관, R6 분명한 출혈원·극단 쇼크는 즉시 출혈 조절, R7–R8 eFAST·조영 전신 CT, R9 첫 Hb 정상이 초기 출혈을 가림, R13 수축기 80–90(평균 50–60)·GCS ≤8 은 평균 ≥80·뇌손상·척수손상 금기·노인/만성 고혈압 신중, R14 노르에피네프린, R20 골반 결속대·골반 고리 조기 고정, R21 복막외 채움·REBOA, R23 트라넥삼산 3시간 안 1 g/10분 + 1 g/8시간"
    verified: text
  - id: cn-prehospital-2026
    org: "Trauma Society of the Chinese Medical Association 등 (Li Y, Lang L, Zhang J, et al.)"
    title: "Chinese expert consensus on the prehospital management of major trauma"
    kind: consensus
    year: 2026
    citation: "Chin J Traumatol 2026;29(2):79-89"
    doi: "10.1016/j.cjtee.2026.01.002"
    pmid: "41813488"
    url: "https://pmc.ncbi.nlm.nih.gov/articles/PMC13070844/"
    checked_at: 2026-11-20
    checked: "PMC13070844 전문을 처음부터 끝까지 읽음(권고 머리글이 PMC 텍스트에서 빠져 있어 인용 위치는 X·Airway·Breathing·Circulation·TXA·Pelvic binder·Disability·Exposure·SMR 절 이름으로 적음) — xABCDE 평가 틀, 사지 출혈은 상용 지혈대 우선·접합부는 상처 채움+최소 3분 압박·지혈대 시각 기록, 기도는 단계적·경추 의심 시 손 일직선 고정, 긴장성 기흉 세 징후(진행 호흡곤란·저혈압·한쪽 호흡음 소실)면 영상 기다리지 않고 바늘 감압·성인 5번째 갈비사이 중간겨드랑선 선호·2번째 갈비사이 빗장중간선은 긴 바늘(≥8 cm)로·소아는 2번째·5 cm 바늘 실패율 >40 %·실패 시 손가락 흉강창, 허용 저혈압 노뼈동맥 촉지 또는 수축기 90·뇌손상은 수축기 ≥110 또는 평균 ≥80, 젊은 환자는 30 % 손실까지 혈압 유지, 트라넥삼산 3시간 안 1 g 10분 이상·3시간 이후 무효·유해 가능, 골반 결속대 적응 셋·큰돌기 높이·무릎 모으고 발목 안쪽 회전, 노인 수축기 <110 저혈압 기준, 저체온 <35 °C 와 수액 가온, 척추 운동 제한은 선택적·관통상은 이송 지연 금지, ATLS 11판이 IMIST-AMBO 인계를 채택했다는 언급"
    verified: text
  - id: thim-abcde-2012
    org: "Thim T, Krarup NH, Grove EL, Rohde CV, Løfgren B"
    title: "Initial assessment and treatment with the Airway, Breathing, Circulation, Disability, Exposure (ABCDE) approach"
    kind: review
    year: 2012
    citation: "Int J Gen Med 2012;5:117-21"
    doi: "10.2147/IJGM.S28478"
    pmid: "22319249"
    url: "https://pmc.ncbi.nlm.nih.gov/articles/PMC3273374/"
    checked_at: 2026-11-20
    checked: "PMC3273374 전문을 읽음 — ABCDE 는 평가와 처치를 동시에·한 칸의 생명 위협을 처치한 뒤 다음 칸, 근거는 전문가 합의, 심정지에는 ABCDE 대신 CPR, B 에서 경정맥 확장·기관 편위 관찰·긴장성 기흉은 2번째 갈비사이 빗장중간선 바늘 감압, 재평가 반복, ATLS 의 기원"
    verified: text
  - id: bella-efast-2025
    org: "Bella FM, Bonfichi A, Esposito C, et al."
    title: "Extended Focused Assessment with Sonography for Trauma in the Emergency Department: A Comprehensive Review"
    kind: review
    year: 2025
    citation: "J Clin Med 2025;14(10):3457"
    doi: "10.3390/jcm14103457"
    pmid: "40429451"
    url: "https://pmc.ncbi.nlm.nih.gov/articles/PMC12112529/"
    checked_at: 2026-11-20
    checked: "PMC12112529 전문을 읽음 — 3.3 정확도(심낭액 메타분석 민감도 91 %·특이도 94 %, 기흉은 폐 초음파가 앙와위 흉부 X선보다 민감, 복강 실질 손상은 자유액 없으면 민감도 낮음), 3.4 ABCDE 안의 eFAST(B 에서 긴장성 기흉 배제, C 에서 혈심낭·혈흉·혈복강, 불안정 환자의 혈복강은 바로 개복으로), 저혈압 소생 목표 표기(관통 70·둔상 90·두부 110 mmHg)"
    verified: text
  - id: feenstra-chest-tube-2018
    org: "Feenstra TM, Dickhoff C, Deunk J"
    title: "Systematic review and meta-analysis of tube thoracostomy following traumatic chest injury; suction versus water seal"
    kind: review
    year: 2018
    citation: "Eur J Trauma Emerg Surg 2018;44(6):819-827"
    doi: "10.1007/s00068-018-0942-7"
    pmid: "29546613"
    url: "https://pmc.ncbi.nlm.nih.gov/articles/PMC6267148/"
    checked_at: 2026-11-20
    checked: "PMC6267148 전문을 읽음 — 배경 절: 외상성 기흉·혈흉·혈기흉은 공기·액체를 빼 환기와 심장 기능을 개선하려고 흉관 삽입이 필요할 수 있고, 적응과 삽입은 ATLS·ETC 원칙상 필수 술기. 본론(흡인 대 수봉)은 이 목표와 무관해 인용하지 않음. 대량 혈흉 개흉 기준 수치는 이 논문에 없다"
    verified: text
  - id: alerhand-tamponade-2022
    org: "Alerhand S, Adrian RJ, Long B, Avila J"
    title: "Pericardial tamponade: A comprehensive emergency medicine and echocardiography review"
    kind: review
    year: 2022
    citation: "Am J Emerg Med 2022;58:159-174"
    doi: "10.1016/j.ajem.2022.05.001"
    pmid: "35696801"
    checked_at: 2026-11-20
    checked: "PubMed 초록만 읽음(PMC 전문 없음) — Beck 세 징후는 흔히 나타나지 않음, 혈역학 불안정·악화 임박·심정지면 응급 심낭천자, 심한 흉부 외상은 응급 수술 적응, 외상성 혈심낭은 시술 전 혈액제제, 양압 환기·진정은 심박출을 낮춰 가능하면 피함"
    verified: abstract
  - id: galvagno-atls10-2019
    org: "Galvagno SM Jr, Nahmias JT, Young DA"
    title: "Advanced Trauma Life Support Update 2019: Management and Applications for Adults and Special Populations"
    kind: review
    year: 2019
    citation: "Anesthesiol Clin 2019;37(1):13-32"
    doi: "10.1016/j.anclin.2018.09.009"
    pmid: "30711226"
    checked_at: 2026-11-20
    checked: "PubMed 초록만 읽음(PMC 전문 없음 — 요청된 「ATLS 10판 변경점」 논문) — 10판은 정형화된 접근, 결정질 수액 지침 완화, 영상 후두경, 점탄성 검사로 수혈 결정, 척추 고정 대신 척추 운동 제한. 바늘 감압 위치 변경 여부는 초록에 없어 대조하지 않음"
    verified: abstract
diagram:
  title: "다발 외상 일차 평가 — 막힌 칸에서 멈춰 푼다"
  nodes:
    - {id: start, kind: start, text: "다발 외상 — 일차 평가 시작"}
    - {id: x, kind: decision, text: "생명 위협 외출혈?"}
    - {id: hx, kind: step, text: "직접 압박 · 지혈대(시각 기록)"}
    - {id: a, kind: decision, text: "기도 폐쇄 · GCS ≤8 · 저산소?"}
    - {id: intub, kind: step, text: "기관삽관 + 경추 손 고정"}
    - {id: b, kind: decision, text: "한쪽 호흡음 소실 + 저혈압?"}
    - {id: needle, kind: step, text: "영상 없이 바늘 감압"}
    - {id: c, kind: decision, text: "쇼크가 계속되나?"}
    - {id: scan, kind: info, text: "eFAST · 골반 진찰로 출혈 위치"}
    - {id: tamp, kind: end, text: "심장눌림증 — 수혈하며 응급 감압·수술"}
    - {id: hemo, kind: end, text: "혈흉 — 흉관 삽입 → 수술 판단"}
    - {id: pelvis, kind: end, text: "골반 — 결속대 → 고정·색전"}
    - {id: abd, kind: end, text: "혈복강 — 즉시 출혈 조절 수술"}
    - {id: dnode, kind: end, text: "D(GCS·동공) → E(노출·보온) → 재평가"}
  edges:
    - {from: start, to: x}
    - {from: x, to: hx, label: "있음"}
    - {from: x, to: a, label: "없음"}
    - {from: hx, to: a}
    - {from: a, to: intub, label: "예"}
    - {from: a, to: b, label: "아니오"}
    - {from: intub, to: b}
    - {from: b, to: needle, label: "예"}
    - {from: b, to: c, label: "아니오"}
    - {from: needle, to: c}
    - {from: c, to: scan, label: "예"}
    - {from: c, to: dnode, label: "아니오"}
    - {from: scan, to: tamp, label: "심낭액"}
    - {from: scan, to: hemo, label: "흉강액"}
    - {from: scan, to: pelvis, label: "골반 불안정"}
    - {from: scan, to: abd, label: "복강액"}
diagram_notes:
  - "각 칸은 「평가하며 처치」한다 — 막힌 것을 풀고 다음 칸으로 가며, 처치 효과가 나타나는 데 몇 분이 걸리므로 악화되면 처음부터 다시 평가한다 [[thim-abcde-2012: ABCDE principles]]."
  - "심정지(무반응·비정상 호흡·무맥)면 ABCDE 가 아니라 CPR 이다 [[thim-abcde-2012: Which patients need ABCDE?]]."
  - "바늘 감압이 실패하면 위치를 바꾸거나 손가락 흉강창 같은 확실한 감압으로 넘어간다 [[cn-prehospital-2026: Recommendation — Breathing]]."
  - "출혈원이 불분명한데 즉시 조절할 필요가 없으면 eFAST·조영 전신 CT 로 찾는다. eFAST 는 실질 손상만 있고 자유액이 없으면 민감도가 낮다 [[euro-bleeding-2023: R7]] [[bella-efast-2025: 3.5 Limitations]]."
  - "D 에서는 저혈압(수축기 <90)·저산소(SpO₂ <90 %)가 2차 뇌손상의 주원인이라 먼저 교정한다. E 는 노출과 동시에 보온 — 저체온(<35 °C)은 응고장애를 키운다 [[cn-prehospital-2026: Recommendation — Disability]] [[cn-prehospital-2026: Recommendation — Exposure]]."
checks:
  - q: "오토바이 사고 환자 — 넓적다리에서 피가 뿜고, 코골이 소리가 난다. 가장 먼저 할 것은?"
    a: "넓적다리 출혈을 직접 압박·지혈대로 먼저 막는다(<C>ABCDE·xABCDE). 이어 턱 들기·흡인 등으로 기도를 연다."
  - q: "흉부 둔상 후 호흡곤란이 심해지고 혈압 80/50, 오른쪽 호흡음이 없다. 흉부 X선 촬영이 준비 중이다. 다음 처치는?"
    a: "영상을 기다리지 않고 오른쪽 바늘 감압(긴장성 기흉). 실패하면 손가락 흉강창 등으로 넘어간다."
  - q: "뇌손상 없는 출혈성 쇼크 환자의 출혈 조절 전 혈압 목표는? 중증 뇌손상(GCS ≤8)이 있으면?"
    a: "수축기 80–90 mmHg(평균 50–60). 중증 뇌손상이면 평균동맥압 ≥80 mmHg."
figures_none: "영상 소견이 아니라 소견→처치 순서 판단이 목표다 — eFAST 화면은 이 목표의 단서가 아니라 출혈 위치를 찾는 도구로만 쓴다"
---

## 판단 — 왜 막힌 칸을 먼저 푸는가
- 일차 평가는 진단 순서가 아니라 **생명 위협을 찾고 그 자리에서 푸는 순서**다. 앞 칸의 생명 위협을 처치한 뒤 다음 칸으로 간다 [[thim-abcde-2012: ABCDE principles]].
- 원인 진단보다 처치가 먼저다 — 원인이 불분명해도 생명을 살리는 처치를 시작하고, 확진은 그다음이다 [[thim-abcde-2012: ABCDE principles]]. 긴장성 기흉을 X선으로 확인하지 않고 감압하는 것이 대표다 [[cn-prehospital-2026: Recommendation — Breathing]].
- 생명을 위협하는 외출혈은 기도보다 앞에 둔다(<C>ABCDE) — 유럽 외상 출혈 지침은 ATLS 의 ABCDE 가 <C>ABCDE 로 바뀌었다고 쓴다 [[euro-bleeding-2023: R5 Rationale]].
- 분명한 출혈원이 있고 극단적 쇼크면 검사를 더 하지 않고 즉시 출혈 조절로 간다 [[euro-bleeding-2023: R6]].

## 기전 — 산소가 세포에 닿지 못하는 다섯 길
- **기도 폐쇄**: 의식 저하가 흔한 원인이고, 완전 폐쇄면 애써 숨쉬어도 공기가 들어가지 않아(시소 호흡) 곧 심정지로 간다 [[thim-abcde-2012: A – Airway]].
- **긴장성 기흉(tension pneumothorax)**: 한쪽 흉강 압력이 올라 정맥 환류가 막히는 폐쇄성 쇼크다 — 그래서 저혈압·한쪽 호흡음 소실이 함께 오고, 감압하면 바로 풀린다 [[cn-prehospital-2026: Recommendation — Breathing]].
- **심장눌림증(cardiac tamponade)**: 심낭 안 피가 저압인 오른심방·오른심실부터 눌러 채움을 막는다 [[bella-efast-2025: 3.4]]. 양압 환기·진정은 심박출을 더 떨어뜨린다 [[alerhand-tamponade-2022: Abstract]].
- **출혈**: 정상 혈압으로 서둘러 올리면 생긴 혈전이 떨어져 출혈이 늘 수 있어, 멎기 전에는 낮은 목표를 유지한다 [[cn-prehospital-2026: Recommendation — Circulation]]. 저체온·산증·응고장애가 서로를 키운다 [[cn-prehospital-2026: Recommendation — Exposure]].
- **골반 고리 손상**: 후복막 출혈은 압박이 어렵다 — 결속대가 골반 고리를 닫아 부피를 줄이고 출혈 부위에 압박을 건다 [[cn-prehospital-2026: Recommendation — Pelvic binder]].

## 가르는 소견 — 어느 칸이 막혔나
- 표가 소견별로 막힌 칸과 지금 할 처치를 나란히 놓는다.
- **음성 결과의 한계**: 첫 혈색소 정상은 초기 출혈을 가리고 [[euro-bleeding-2023: R9]], 젊은 환자의 정상 혈압은 큰 손실을 가린다 [[cn-prehospital-2026: Recommendation — TXA]]. 쇼크지수(맥박/수축기)는 건강한 성인 0.5–0.7, ≥0.9–1.0 이면 대량수혈 위험이 오른다 [[euro-bleeding-2023: R5 Rationale]]. 노인은 수축기 <110 을 저혈압으로 본다 [[cn-prehospital-2026: Recommendation — Elderly]].

## 선택 — 출혈 조절과 소생
- 출혈 조절까지의 시간을 줄이는 것이 첫 목표다 — 중증 외상은 적절한 외상센터로 바로 이송한다 [[euro-bleeding-2023: R1]].
- 수액은 생리식염수 또는 균형 결정질로 시작하고, 중증 두부 외상에는 젖산 링거 같은 저장성 수액을 피한다 [[euro-bleeding-2023: R15]].
- 트라넥삼산은 출혈 중이거나 위험이 크면 손상 후 3시간 안에 가능한 한 빨리 준다 [[euro-bleeding-2023: R23]].
- 노르에피네프린은 제한 수액으로 목표 혈압에 못 미칠 때만 더한다 [[euro-bleeding-2023: R14]].

## 권고와 예외
- 중증 뇌손상(GCS ≤8)은 허용 저혈압의 예외다 — 평균동맥압 ≥80 mmHg [[euro-bleeding-2023: R13]].
- 척추 운동 제한은 고위험군에만 선택적으로 하고, 몸통 관통상은 척추 고정 때문에 출혈 조절 수술을 늦추지 않는다 [[cn-prehospital-2026: Recommendation — SMR]].
- 대량 혈흉의 개흉 기준 수치와 국내 교과서·KMLE 해설의 순서 표기는 대조하지 않았다(검토 항목).

## 시험 쟁점 — 충돌·맥락·새 근거
- **Z1 충돌 · 대량 외출혈과 기도의 순서** — 시험 기준: 생명을 위협하는 외출혈은 기도보다 먼저 압박·지혈대(<C>ABCDE · xABCDE) [[euro-bleeding-2023: R5 Rationale]] [[cn-prehospital-2026: Recommendation — X]] / 다른 기준: 고전 ABCDE 는 기도→호흡→순환 순이고 출혈은 C 칸에서 다룬다 [[thim-abcde-2012: ABCDE principles]] / 왜 다른가: 대량 외출혈 조절 경험의 상당 부분이 군 전투 외상 처치(TCCC)에서 왔고, 지혈대가 생존을 늘렸다는 민간 코호트도 있다 [[cn-prehospital-2026: Recommendation — X]] [[euro-bleeding-2023: R2 Rationale]] / 시험에서는: KMLE 는 국내 교과서·해설과 대조하지 않았다(검토 항목) · USMLE 도 대조하지 않았다 — 발문에 「뿜는」 사지 출혈이 명시되면 압박·지혈대를, 아니면 기도를 첫 처치로 고른다.
- **Z2 충돌 · 바늘 감압 위치** — 시험 기준: 성인은 5번째 갈비사이 중간겨드랑선이 선호된다(가슴벽이 얇아 성공률이 높고 속가슴혈관을 피함) [[cn-prehospital-2026: Recommendation — Breathing]] / 다른 기준: 2012 종설은 2번째 갈비사이 빗장중간선을 쓴다 [[thim-abcde-2012: B – Breathing]] / 왜 다른가: 2번째 갈비사이에서 5 cm 바늘의 실패율이 40 %를 넘을 수 있어서다. 소아는 여전히 2번째 갈비사이 빗장중간선, 성인도 옆가슴 접근이 막히면 ≥8 cm 바늘로 2번째 갈비사이 [[cn-prehospital-2026: Recommendation — Breathing]] / 시험에서는: ATLS 10판 원문은 읽지 못했다(†Galvagno 초록에 위치 언급 없음) — 처치 선택 문항에서는 위치보다 「영상 없이 즉시 감압」이 가르는 근거다.
- **Z3 맥락 · 허용 저혈압의 숫자** — 시험 기준: 수축기 80–90 mmHg(평균 50–60), 중증 뇌손상은 평균 ≥80 [[euro-bleeding-2023: R13]] / 다른 기준: 병원 전 합의는 노뼈동맥 촉지 또는 수축기 90, 뇌손상은 수축기 ≥110 또는 평균 ≥80 [[cn-prehospital-2026: Recommendation — Circulation]]; eFAST 종설은 관통 70·둔상 90·두부 110 mmHg 를 적는다 [[bella-efast-2025: 3.4]] / 왜 다른가: 대상(병원 전 vs 병원)과 손상 기전에 따라 목표를 나눈 방식이 다르다 / 시험에서는: 숫자 하나보다 「출혈이 멎기 전엔 정상 혈압을 목표로 하지 않는다 · 뇌손상은 예외」로 답한다.
- **Z4 새 근거 · 척추 고정에서 척추 운동 제한으로** — 시험 기준: 선택적 척추 운동 제한, 긴 척추판은 구출용으로만 [[cn-prehospital-2026: Recommendation — SMR]] / 다른 기준: ATLS 10판도 척추 고정 대신 척추 운동 제한을 강조한다 [[galvagno-atls10-2019: Abstract]] / 왜 다른가: 긴 고정은 욕창·통증·환기 제한을 만들고 관통상에서는 출혈 조절을 늦춘다 [[cn-prehospital-2026: Recommendation — SMR]] / 시험에서는: 둔상·의식 저하 환자의 경추 보호는 그대로 A 칸에 둔다.
