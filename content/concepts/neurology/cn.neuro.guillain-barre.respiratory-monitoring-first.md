---
id: cn.neuro.guillain-barre.respiratory-monitoring-first
type: concept
topic: Neurology
see_also: [Emergency Medicine]
date: 2026-09-23
updated: 2026-09-23
version: 1
outline: h447            # 기본틀 슬롯 — 해리슨 21판 447장 Guillain-Barré Syndrome and Other Immune-Mediated Neuropathies
confidence: medium
review_status: unreviewed
title: "길랑-바레 증후군의 첫 처치 — 활력징후가 안정해도 입원해 폐활량을 재는 것이 먼저다(면역치료는 그 안에서)"
objective: "빠르게 오르는 대칭성 이완마비·건반사 소실·연수 증상으로 길랑-바레 증후군을 알아보고, 활력징후가 안정적이어도 가장 먼저 할 일이 감시 병상 입원과 연속 폐활량(FVC)·최대흡기압 측정임을 고르며, 면역치료(IVIG·혈장교환)·신경전도검사·스테로이드·외래 추적이 그 순서에서 어디에 있는지 가른다"
objective_kind: 다음 처치
condition: 길랑-바레 증후군(악화기)
exams: [usmle, kmle]
summary:
  - "길랑-바레 증후군 = 감염 1–3주 뒤 말초신경·신경근에 대한 자가면역 공격. 수 시간~수일에 걸쳐 오르는 대칭성 이완마비 + 건반사 소실, 감각 증상은 가볍다."
  - "악화기의 목숨을 가르는 것은 진단 확정이 아니라 호흡근·연수 마비와 자율신경 불안정이다. 최대 30 % 가 인공호흡을 필요로 한다."
  - "그래서 첫 처치 = 감시 병상(대개 중환자실) 입원 + 연속 폐활량·최대흡기압·심전도·혈압 감시. 지금 숨이 괜찮다는 것은 몇 시간 뒤를 보장하지 않는다."
  - "면역치료(IVIG 2 g/kg 5일 또는 혈장교환)는 진단 뒤 가능한 한 빨리 — 하루하루가 중요하다. 감시와 경쟁하는 것이 아니라 감시 안에서 시작한다."
  - "스테로이드는 길랑-바레에 효과가 없다(만성형 CIDP 와 다른 점). 신경전도·뇌척수액은 첫 주에 정상일 수 있어 결과를 기다리며 감시·치료를 늦추지 않는다."
criteria:
  - id: gbs-clinical
    name: 길랑-바레 증후군의 임상 양상(해리슨)
    kind: 정의
    population: "급성 근력저하로 온 환자"
    statement: "빠르게 진행하는 건반사 소실성 운동마비. 흔히 다리에서 시작해 오르며 수 시간~수일에 걸쳐 진행하고, 얼굴 양측 마비가 절반, 하부 뇌신경 침범으로 분비물 처리·기도 유지가 어려워질 수 있다. 발열·전신 증상은 시작 때 없고 있으면 진단을 의심한다 [[harrison-21: 447장 p.3501]]"
    exceptions: "20–30 % 는 캄필로박터 제주니 감염이 선행하고, 비슷한 비율로 CMV·EBV 등 헤르페스바이러스 감염이 선행한다 [[harrison-21: 447장 p.3501]]"
    source: harrison-21
    basis: current
    exams: [usmle, kmle]
  - id: gbs-ventilation-risk
    name: 인공호흡 위험 인자(해리슨)
    kind: 중증도
    population: "길랑-바레 증후군 입원 환자"
    statement: "대부분 입원이 필요하고 최대 30 % 가 경과 중 인공호흡을 필요로 한다. 입원 때 심한 근력저하, 빠른 진행 속도, 첫 주의 얼굴·연수 약화가 인공호흡 필요와 연관된다 [[harrison-21: 447장 p.3501]]"
    exceptions: "자율신경 침범(혈압 급변·기립저혈압·부정맥)은 근력저하가 가벼운 환자에게도 오고 치명적일 수 있어 따로 감시한다 [[harrison-21: 447장 p.3501]]"
    source: harrison-21
    basis: current
    exams: [usmle, kmle]
  - id: gbs-monitoring
    name: 악화기 감시(해리슨)
    kind: 치료 권고
    population: "악화 중인 길랑-바레 증후군"
    statement: "악화기에는 대부분 중환자 병상에서 감시하며 폐활량, 심장 리듬, 혈압, 영양, 심부정맥혈전 예방, 기관절개(삽관 2주 뒤 고려), 흉부 물리치료에 주의한다 [[harrison-21: 447장 p.3504]]"
    exceptions: "이미 정체기에 이른 아주 가벼운 환자는 IVIG·혈장교환 없이 보존적으로 볼 수 있다 [[harrison-21: 447장 p.3504]]"
    source: harrison-21
    basis: current
    exams: [usmle, kmle]
  - id: gbs-intubation-numbers
    name: 삽관을 고려하는 호흡 수치(「20/30/40」)
    kind: 치료 기준
    population: "연속 호흡 측정 중인 길랑-바레"
    statement: "폐활량 < 20 mL/kg, 최대흡기압이 −30 cmH2O 보다 약함, 최대호기압 < 40 cmH2O, 또는 빠르게 떨어지는 추세면 선택적 삽관을 고려한다 [[?lawn-2001]]"
    exceptions: "해리슨 447장은 폐활량 감시를 적을 뿐 삽관 역치 수치를 제시하지 않는다 — 수치는 원문을 대조하지 못한 출처의 것이다(검토 항목)"
    source: lawn-2001
    basis: current
    exams: [usmle, kmle]
  - id: gbs-immunotherapy
    name: 면역치료(해리슨)
    kind: 치료 권고
    population: "길랑-바레 증후군(진행 중이거나 걸을 수 없는 환자)"
    statement: "진단 뒤 가능한 한 빨리 시작한다 — 하루하루가 중요하다. IVIG(2 g/kg 을 5일에 나눠) 또는 혈장교환(40–50 mL/kg 씩 7–10일에 4–5회)은 효과가 같고 병용은 더 낫지 않다. 치료는 인공호흡 필요를 거의 절반(27 → 14 %)으로 줄이고 1년 완전 회복을 55 → 68 % 로 늘린다 [[harrison-21: 447장 p.3504]]"
    exceptions: "첫 운동 증상 뒤 약 2주가 지나 정체기에 이르렀으면 대개 치료 적응이 없다. 한 치료에 뚜렷한 호전이 없다고 다른 치료로 바꾸는 근거는 없다 [[harrison-21: 447장 p.3504]]"
    source: harrison-21
    basis: current
    exams: [usmle, kmle]
sources:
  - id: harrison-21
    org: "McGraw Hill"
    title: "Harrison's Principles of Internal Medicine, 21st ed. — Chapter 447: Guillain-Barré Syndrome and Other Immune-Mediated Neuropathies"
    kind: textbook
    year: 2022
    citation: "Loscalzo J, Fauci AS, Kasper DL, et al (eds). Harrison's Principles of Internal Medicine, 21e. 447장(Hauser SL, Amato AA), 인쇄쪽 3501–3506"
    checked_at: 2026-09-23
    checked: "드라이브 장 문서로 본문 대조. p.3501 임상 양상(상행성 이완마비, 얼굴 양측 마비 50 %, 연수 약화·기도, 인공호흡 최대 30 %와 위험 인자, 발열 없음, 자율신경 침범, 정체기 4주 이내, 선행 감염 캄필로박터 20–30 %), p.3503 뇌척수액(단백 1–10 g/L·세포 증가 없음, 48시간 이내 정상일 수 있음), p.3504 진단 전 치료 시작·치료(하루하루 중요, 2주·정체기, IVIG 2 g/kg 5일·혈장교환 동등, 병용 이득 없음, 인공호흡 27→14 %, 1년 회복 55→68 %, 무반응 시 교체 근거 없음, 악화기 중환자 감시 항목, 가벼운 정체기 환자 보존 치료), p.3506 스테로이드는 CIDP 에 듣고 GBS 에는 안 듣는다"
    verified: text
  - id: lawn-2001
    org: "Archives of Neurology"
    title: "Anticipating mechanical ventilation in Guillain-Barré syndrome"
    kind: other
    year: 2001
    citation: "Lawn ND, Fletcher DD, Henderson RD, Wolter TD, Wijdicks EF. Arch Neurol 2001;58(6):893-898"
    url: "https://jamanetwork.com/journals/jamaneurology"
    checked_at: 2026-09-23
    checked: "서지만 확인(원문 미대조 — 검토 항목). 이 컨테이너는 PubMed·doi 접근이 막혀 「20/30/40」 수치를 원문과 대조하지 못했다"
    verified: citation
tables:
  - id: gbs-first-hours
    title: "길랑-바레 의심 환자의 첫 몇 시간 — 무엇을 먼저, 무엇을 함께"
    role: treatment
    span: full
    section: 치료
    columns: ["순서", "무엇을", "왜", "근거"]
    rows:
      - ["1", "감시 병상 입원 + 폐활량·최대흡기압 연속 측정, 심전도·혈압 감시, 연하 평가", "호흡근·연수 마비와 자율신경 불안정이 몇 시간 만에 올 수 있다", "[[harrison-21: 447장 p.3501]] [[harrison-21: 447장 p.3504]]"]
      - ["1과 함께", "IVIG 또는 혈장교환을 가능한 한 빨리", "치료가 인공호흡 필요를 거의 절반으로 줄인다", "[[harrison-21: 447장 p.3504]]"]
      - ["병행", "뇌척수액·신경전도검사 — 흉내 질환 배제", "첫 주에는 정상일 수 있다 — 결과를 기다리며 치료를 늦추지 않는다", "[[harrison-21: 447장 p.3504]]"]
      - ["추세 악화 시", "선택적 삽관", "응급 삽관보다 안전하다", "[[?lawn-2001]]"]
    note: "「무엇이 먼저인가」 문항에서 감시가 앞서는 이유는 면역치료가 덜 중요해서가 아니라, 면역치료의 효과가 며칠~몇 주 뒤에 나타나는 동안 환자를 지켜 주는 것이 감시이기 때문이다."
  - id: gbs-wrong-choices
    title: "첫 처치로 틀린 선택들 — 이유가 다르다"
    role: comparison
    span: column
    section: 감별
    columns: ["선택", "왜 첫 처치가 아닌가", "언제 맞는가"]
    rows:
      - ["호흡 평가 없이 IVIG 만", "효과가 나기까지 호흡부전을 막아 주지 못한다", "감시 체계 안에서는 가능한 한 빨리"]
      - ["스테로이드", "길랑-바레에 효과 없음 [[harrison-21: 447장 p.3506]]", "CIDP"]
      - ["신경전도검사 먼저", "초기엔 정상일 수 있고 기다리면 늦는다 [[harrison-21: 447장 p.3504]]", "진단이 불확실하고 감시가 이미 된 뒤"]
      - ["외래 추적", "진행 속도를 예측할 수 없다", "정체기에 이른 아주 가벼운 환자 [[harrison-21: 447장 p.3504]]"]
    note: "네 선택 모두 「지금 괜찮다」를 「앞으로도 괜찮다」로 읽는 순서 문제다."
pitfalls:
  - contrast: "IVIG 즉시(호흡 평가 없이) vs 입원·연속 폐활량 감시 — 「표준 치료니까 바로」"
    point: "IVIG 는 길랑-바레의 표준 면역치료이고 가능한 한 빨리 시작한다 [[harrison-21: 447장 p.3504]]. 그러나 효과는 첫 주 끝 무렵이나 몇 주 뒤에야 나타나므로 [[harrison-21: 447장 p.3504]] 그 사이 호흡근·연수 마비를 잡아 줄 수 없다. 3일 만에 발에서 손까지 오르고 연하곤란이 있는 환자는 인공호흡 위험 인자(빠른 진행·연수 약화)를 가진다 [[harrison-21: 447장 p.3501]]. 첫 처치는 감시 병상 입원과 연속 폐활량 측정이고, IVIG 는 그 안에서 시작한다."
    exception: "이미 입원해 폐활량을 재며 안정적으로 감시 중이라면 다음 처치는 IVIG(또는 혈장교환)다."
    covers: ["usmle-2026-0041:B"]
  - contrast: "스테로이드 vs 면역글로불린 — 「탈수초 염증이니 스테로이드」"
    point: "만성 염증성 탈수초 다발신경병(CIDP)은 스테로이드에 반응하지만 길랑-바레는 반응하지 않는다 [[harrison-21: 447장 p.3506]]. 급성 탈수초라는 겉모습이 같아도 약이 다르다."
    exception: "8주 넘게 진행하거나 재발하면 CIDP 를 생각한다 — 그때는 스테로이드가 맞다."
  - contrast: "안정 활력징후 → 외래 vs 입원 — 「지금 숨이 괜찮다」"
    point: "정체기는 거의 4주 이내에 오지만 [[harrison-21: 447장 p.3501]] 그 전까지 진행 속도를 예측할 수 없다. 자율신경 침범은 가벼운 환자에게도 오고 치명적일 수 있다 [[harrison-21: 447장 p.3501]]."
    exception: "이미 정체기에 이른 아주 가벼운 환자는 면역치료 없이 보존적으로 볼 수 있다 [[harrison-21: 447장 p.3504]] — 그래도 판단은 진찰·측정 뒤다."
  - contrast: "신경전도검사·뇌척수액 먼저 vs 감시·치료 먼저 — 「확진 뒤에 치료」"
    point: "뇌척수액 단백은 첫 주 끝에야 오르고 48시간 이내엔 정상일 수 있으며 [[harrison-21: 447장 p.3503]], 신경전도 소견도 초기엔 미미하다. 강하게 의심되면 특징 소견을 기다리지 않고 치료를 시작한다 [[harrison-21: 447장 p.3504]]."
    exception: "뇌척수액 세포가 계속 많으면 다른 진단(척수염·HIV·림프종 등)을 찾는다 [[harrison-21: 447장 p.3503]]."
diagram:
  title: "길랑-바레 의심 — 첫 처치의 순서"
  nodes:
    - {id: start, kind: start, text: "수 시간~수일 오르는 대칭성 이완마비 + 건반사 소실(± 선행 감염)"}
    - {id: info, kind: info, text: "폐활량·최대흡기압, 기침·연하, 목 굴곡력, 혈압·심전도 변동을 잰다 — 활력징후만으로 판단하지 않는다"}
    - {id: resp, kind: decision, text: "호흡·연수 기능이 위험한가? (폐활량 < 20 mL/kg 또는 빠른 하강, 분비물 처리 불가)"}
    - {id: intub, kind: end, text: "중환자실 · 선택적 삽관 + 면역치료"}
    - {id: phase, kind: decision, text: "아직 악화 중인가, 정체기인가?"}
    - {id: icu, kind: end, text: "감시 병상 입원 · 연속 폐활량/최대흡기압 · 자율신경 감시 + 가능한 한 빨리 IVIG 또는 혈장교환"}
    - {id: mild, kind: end, text: "정체기의 아주 가벼운 환자 — 보존 치료 가능(입원 관찰 뒤 판단)"}
  edges:
    - {from: start, to: info}
    - {from: info, to: resp, label: "측정 완료"}
    - {from: resp, to: intub, label: "위험"}
    - {from: resp, to: phase, label: "아직 안전"}
    - {from: phase, to: icu, label: "악화 중(대부분)"}
    - {from: phase, to: mild, label: "정체기 + 걸을 수 있음"}
diagram_notes:
  - "폐활량 20 mL/kg 등 삽관 수치는 해리슨이 제시하지 않으며 원문 미대조 출처의 것이다 [[?lawn-2001]]."
  - "빠른 진행·첫 주의 얼굴·연수 약화·입원 때 심한 근력저하는 인공호흡 위험을 높인다 [[harrison-21: 447장 p.3501]] — 수치가 괜찮아도 이 경우 감시 간격을 좁힌다."
  - "면역치료는 첫 운동 증상 뒤 약 2주 안에 의미가 있다 [[harrison-21: 447장 p.3504]]."
  - "스테로이드는 어느 갈래에도 없다 [[harrison-21: 447장 p.3506]]."
checks:
  - q: "선행 설사 2주 뒤 3일간 오르는 대칭성 근력저하·건반사 소실·가벼운 연하곤란, 활력징후 안정. 가장 먼저 할 일은?"
    a: "감시 병상 입원과 연속 폐활량·최대흡기압 측정(자율신경 감시 포함). 면역치료는 그 안에서 가능한 한 빨리."
  - q: "길랑-바레에서 인공호흡이 필요해질 위험 인자 셋은?"
    a: "입원 때 심한 근력저하, 빠른 진행 속도, 첫 주의 얼굴·연수 약화."
  - q: "IVIG 와 혈장교환 중 무엇이 나은가? 병용은?"
    a: "효과가 같다. 병용은 단독보다 유의하게 낫지 않다."
  - q: "길랑-바레에 스테로이드를 쓰지 않는 이유는?"
    a: "효과가 없다 — 스테로이드에 반응하는 것은 CIDP 다."
  - q: "증상 첫날 뇌척수액이 정상이면 길랑-바레를 배제하나?"
    a: "아니다. 단백은 첫 주 끝에야 오르고 48시간 이내엔 정상일 수 있다."
variants:
  - id: v1
    of: usmle-2026-0041
    flip: true
    changed: "환자를 「응급실 도착 직후」에서 「이미 중환자실에 입원해 연속 폐활량 측정 중이며 수치가 안정적이지만 걸을 수 없음」으로 바꿈 → 감시가 이미 갖춰졌으므로 답이 「입원·폐활량 감시」에서 「IVIG 시작」으로 바뀜"
    context: "단서를 바꿔 답이 바뀌는 변형 — 감시가 이미 갖춰진 환자"
    stem: "A 41-year-old man was admitted to the intensive care unit 6 hours ago with 4 days of ascending, symmetric weakness that began after an upper respiratory infection. He now cannot walk without assistance. Deep tendon reflexes are absent. Forced vital capacity has been measured every 4 hours and is stable at 38 mL/kg; negative inspiratory force is -48 cm H2O. He handles his secretions without difficulty. Cerebrospinal fluid analysis shows protein 72 mg/dL with 2 cells/µL. Blood pressure and cardiac rhythm have remained stable on telemetry. Which of the following is the most appropriate next step in management?"
    choices: ["A. Oral prednisone taper", "B. Intravenous immunoglobulin, 2 g/kg divided over 5 days", "C. Elective endotracheal intubation now", "D. Repeat nerve conduction studies in 2 weeks before deciding on therapy", "E. Discharge with outpatient physical therapy"]
    answer: "B"
    explanation: "Monitoring is already in place and respiratory function is safe, so the next step is disease-modifying immunotherapy: IVIG (or plasma exchange, equally effective) should be started as soon as possible in a patient who is still progressing and cannot walk. Glucocorticoids do not help GBS, intubation is not indicated with an FVC of 38 mL/kg and strong NIF, and waiting for repeat studies loses the treatment window. In the original item the patient had just arrived and the order of steps was the question — monitoring first."
    kind: application
  - id: v2
    of: usmle-2026-0041
    flip: false
    changed: "나이·성별(58세 남자), 선행 감염(설사 → 상기도 감염), 첫 증상(발 저림 → 양측 얼굴 약화 동반)을 바꾸고 「빠른 상행 진행 + 건반사 소실 + 연수 침범 + 활력징후 안정 + 응급실 첫 대면」은 그대로 → 답은 여전히 입원·연속 폐활량 감시"
    context: "겉모습만 바꾸고 답은 같은 변형 — 얼굴 약화가 함께 온 중년 남자"
    stem: "A 58-year-old man is brought to the emergency department by his wife because he has had difficulty climbing stairs for 2 days and today cannot button his shirt. He also notices that he cannot whistle and that liquids occasionally come back through his nose. Ten days ago he had a sore throat and cough that resolved. Examination shows bilateral facial weakness, symmetric weakness of all four limbs that is worse in the legs, and absent reflexes. Temperature is 36.9°C, pulse 92/min, respirations 16/min, blood pressure 132/80 mm Hg, and oxygen saturation 98% on room air. Which of the following is the most appropriate next step in management?"
    choices: ["A. Obtain nerve conduction studies before deciding on admission", "B. Intravenous methylprednisolone for 5 days", "C. Admit to a monitored unit for serial forced vital capacity and negative inspiratory force measurements", "D. Outpatient MRI of the spine and neurology follow-up in 1 week", "E. Give one dose of intravenous immunoglobulin in the emergency department and discharge home"]
    answer: "C"
    explanation: "Rapidly ascending areflexic weakness with bilateral facial and bulbar involvement after an infection is Guillain-Barré syndrome. Rapid progression and early facial/bulbar weakness predict the need for ventilation, so normal oxygen saturation and vital signs do not make him safe; the first step is admission with serial FVC/NIF monitoring, with IVIG or plasma exchange started promptly within that setting. Steroids are ineffective, and nerve studies can be normal early and must not delay monitoring."
    kind: application
---

## 정의
길랑-바레 증후군은 말초신경과 신경근을 공격하는 급성 자가면역 다발신경병이다. 빠르게 진행하는 건반사 소실성 운동마비로, 흔히 다리에서 시작해 오르고(「고무 다리」), 수 시간~수일에 걸쳐 진행하며 손발 저림이 동반된다. 얼굴 양측 마비가 절반에서, 하부 뇌신경 침범으로 분비물 처리·기도 유지 곤란이 흔히 온다 [[harrison-21: 447장 p.3501]]. 이 정리본의 목표는 진단 자체보다, **진단을 떠올린 순간 무엇을 가장 먼저 해야 하는가**다.

## 병태생리
정상에서 말초 운동신경은 수초 덕분에 도약 전도로 빠르게 신호를 보낸다. 선행 감염(캄필로박터 제주니 20–30 %, CMV·EBV 등 헤르페스바이러스 비슷한 비율 [[harrison-21: 447장 p.3501]])이 신경 성분과 닮은 항원에 대한 면역 반응을 일으키면, 수초 또는 축삭 막이 공격받아 전도가 막힌다. 신경근·근위부 신경이 먼저 다쳐 뇌척수액 단백이 오르지만 염증 세포는 늘지 않는다(단백–세포 해리) [[harrison-21: 447장 p.3503]]. 심한 경우 축삭 변성이 오고 회복이 훨씬 늦다.

호흡은 횡격막(목 신경근 C3–5)과 늑간근, 기도 보호는 하부 뇌신경이 맡는다. 마비가 이 높이까지 오르면 **폐활량이 떨어지는 속도**가 곧 생명의 문제다. 자율신경 섬유도 같이 다쳐 혈압이 크게 오르내리고 부정맥이 생긴다 [[harrison-21: 447장 p.3501]].

## 기전에서 소견으로
- **상행성 대칭 약화·건반사 소실**: 긴 신경부터·근위 신경근에서 전도 차단 → 반사는 첫 며칠 안에 약해지거나 사라진다 [[harrison-21: 447장 p.3501]].
- **감각은 가볍다**: 저림은 흔하지만 객관적 감각 소실은 적다.
- **얼굴·연수 약화**: 삼킴 곤란, 목소리 변화, 분비물 처리 곤란 — 기도 위험의 신호. 초기엔 뇌간 허혈로 오인되기도 한다 [[harrison-21: 447장 p.3501]].
- **통증**: 목·어깨·등 통증이 초기 절반에서 [[harrison-21: 447장 p.3501]].
- **발열 없음**: 시작 때 발열·전신 증상이 있으면 진단을 의심한다 [[harrison-21: 447장 p.3501]].
- **정상 활력징후의 한계**: 호흡근은 여력이 크다가 한꺼번에 무너진다. 산소포화도는 환기 실패의 늦은 지표이므로, 폐활량·흡기압을 직접 재야 한다.

## 감별
- **척수 질환(횡단척수염·압박)**: 감각 수준·방광 기능 이상 — 뚜렷하면 척수 영상 [[harrison-21: 447장 p.3501]].
- **뇌간 허혈**: 연수 약화로 시작할 때 혼동 [[harrison-21: 447장 p.3501]].
- **CIDP**: 8주 넘게 진행하거나 재발 — 스테로이드에 반응한다 [[harrison-21: 447장 p.3506]].
- **소아마비·급성 이완성 척수염·라임·CMV 다발신경근염**: 뇌척수액 세포 증가가 가른다 [[harrison-21: 447장 p.3504]].
- **중증근무력증·보툴리눔 중독**: 반사 보존·동공(보툴리눔), 피로성 약화 — 이 정리본의 주제는 아니다.

## 검사
- **호흡 측정(가장 먼저·반복)**: 폐활량(FVC), 최대흡기압(NIF). 한 번 값보다 추세가 중요하다.
- **뇌척수액**: 단백 1–10 g/L(100–1000 mg/dL), 세포 증가 없음. 48시간 이내엔 정상일 수 있고 첫 주 끝에 대개 오른다. 세포 10–100/µL 는 가끔 있지만 계속 많으면 다른 진단 [[harrison-21: 447장 p.3503]].
- **신경전도검사**: 초기엔 미미할 수 있다. 강하게 의심되면 특징 소견을 기다리지 않고 치료한다 [[harrison-21: 447장 p.3504]].
- **HIV 검사**: 위험 인자나 뇌척수액 세포 증가가 있으면 [[harrison-21: 447장 p.3504]].
- **음성 결과의 해석**: 첫날 정상 뇌척수액·정상 신경전도는 길랑-바레를 배제하지 못한다.

## 치료
**1. 감시.** 악화기에는 대부분 중환자 병상에서 폐활량, 심장 리듬, 혈압, 영양, 심부정맥혈전 예방, 흉부 물리치료를 챙기고, 삽관 2주 뒤 기관절개를 고려한다 [[harrison-21: 447장 p.3504]]. 폐활량 < 20 mL/kg 이나 빠른 하강, 흡기압 약화는 선택적 삽관을 고려할 신호다 [[?lawn-2001]].

**2. 면역치료.** 진단 뒤 가능한 한 빨리 — 하루하루가 중요하다. IVIG(2 g/kg 을 5일에 나눠) 또는 혈장교환(40–50 mL/kg 씩 7–10일에 4–5회)은 효과가 같고 병용은 더 낫지 않다. 인공호흡 필요를 거의 절반(27 → 14 %)으로 줄이고 1년 완전 회복을 55 → 68 % 로 늘린다 [[harrison-21: 447장 p.3504]]. 첫 운동 증상 뒤 약 2주가 지나 정체기에 이르렀으면 대개 적응이 없다 [[harrison-21: 447장 p.3504]].

**3. 스테로이드 없음.** 길랑-바레에는 효과가 없다 [[harrison-21: 447장 p.3506]].

**반응 확인·재평가.** 호전은 첫 주 끝 무렵에 오거나 몇 주 늦을 수 있고, 한 치료에 뚜렷한 호전이 없다고 다른 치료로 바꾸는 근거는 없다 [[harrison-21: 447장 p.3504]]. 약 85 % 가 몇 달~1년 안에 기능을 회복하고, 최적 환경의 사망률은 5 % 미만이며 사망은 주로 폐 합병증 때문이다 [[harrison-21: 447장 p.3504]].

## 권고와 예외
- 활력징후가 안정적이어도 악화 중인 길랑-바레는 감시 병상에 입원한다.
- 면역치료와 감시는 경쟁 관계가 아니다 — 감시를 갖춘 뒤(같은 시간대에) 가능한 한 빨리 시작한다.
- 확진 검사를 기다리며 감시·치료를 늦추지 않는다.
- 정체기에 이른 아주 가벼운 환자는 면역치료 없이 볼 수 있다 [[harrison-21: 447장 p.3504]].
- 삽관 역치 「20/30/40」은 해리슨 밖의 출처로, 원문 미대조다(검토 항목).

## 시험 쟁점 — 충돌·맥락·새 근거
- **Z1 맥락 · 「감시 먼저」와 「치료는 하루라도 빨리」** — 시험 기준: 응급실 첫 대면에서 「가장 먼저」를 물으면 입원·연속 폐활량 감시다(문항 해설) / 다른 기준: 해리슨은 진단 뒤 가능한 한 빨리 면역치료를 시작하라고(하루하루가 중요하다) 적고, 악화기엔 중환자 감시를 따로 적어 둘 사이에 순서를 두지 않는다 [[harrison-21: 447장 p.3504]] / 왜 다른가: 시험은 한 가지 「첫 행동」을 고르게 하려고 순서를 묻지만 실제로는 같은 시간대에 함께 한다 / 시험에서는: USMLE·KMLE 모두 보기에 「호흡 평가 없이」 같은 순서 단서가 있으면 감시를 고르고, 이미 감시 중이면 IVIG·혈장교환을 고른다.

## (심화) 왜 산소포화도가 아니라 폐활량인가
호흡근 약화는 먼저 폐활량과 기침력을 깎는다. 환자는 얕고 빠른 호흡으로 분시환기량을 유지하고, 무기폐가 생기기 전까지 산소포화도는 정상에 머문다. 이산화탄소가 오르고 포화도가 떨어질 때는 이미 여력이 바닥난 뒤다. 그래서 길랑-바레 감시는 「지금의 가스교환」이 아니라 「남은 여력의 추세」를 재는 폐활량·흡기압으로 한다. 해리슨이 악화기 감시 항목의 첫머리에 폐활량을 두는 것도 같은 이유로 읽을 수 있다 [[harrison-21: 447장 p.3504]].
