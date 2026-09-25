---
id: cn.pharm.thiopurine-interaction.xanthine-oxidase-inhibition
type: concept
topic: Rheumatology
see_also: [Pharmacology, Gastroenterology]
date: 2026-09-25
updated: 2026-09-25
version: 1
outline: h372            # 기본틀 슬롯 — 해리슨 372장(통풍)의 요산 강하제 자리
confidence: medium
review_status: unreviewed
note_form: 2            # 판형 2(2026-09-25)
title: "티오퓨린 + 알로푸리놀 — 막힌 불활성 출구"
objective: "티오퓨린 복용자에게 새로 생긴 골수 억제를 크산틴 산화효소 억제에 의한 6-MP 불활성화 차단으로 설명한다"
objective_kind: 기전
condition: 티오퓨린(아자티오프린·6-메르캅토퓨린)–크산틴 산화효소 억제제 상호작용(thiopurine–xanthine oxidase inhibitor interaction)
exams: [usmle, kmle]
summary:
  - "결론: 티오퓨린을 오래 안정적으로 쓰던 사람이 요산 강하제 추가 뒤 범혈구감소면 알로푸리놀의 크산틴 산화효소 억제다."
  - "시험 단서: 아자티오프린(azathioprine)·6-MP 수년 안정 + 통풍약 추가 수주 뒤 발열·호중구감소 + 요산 저하."
  - "왜: 6-MP 의 불활성화 출구(xanthine oxidase)가 막히면 HGPRT 쪽 활성 6-티오구아닌 뉴클레오타이드가 쌓인다."
  - "함께 써야 하면 아자티오프린·6-MP 를 평소의 1/3~1/4 로 줄이고 혈구를 자주 본다(알로푸리놀 허가사항)."
  - "프로베네시드(요산 배설)·나프록센·프레드니손은 6-MP 대사를 막지 않는다. 콜히친은 신부전·CYP3A4 억제제가 있어야 쌓인다."
pitfalls:
  - contrast: "프로베네시드 vs 알로푸리놀 — 둘 다 요산을 낮추는데?"
    point: "요산 저하는 두 약이 모두 설명한다. 골수 억제를 설명하려면 6-MP 를 불활성화하는 효소가 막혀야 하는데, 프로베네시드는 요세관 요산 재흡수를 막아 배설을 늘리는 약이라 크산틴 산화효소·TPMT 를 건드리지 않는다. 해리슨도 프로베네시드를 알로푸리놀과 함께 쓸 수 있는 요산 배설제로 적는다 [[harrison-21: 372장 p.2865]]."
    exception: "프로베네시드는 신세관 분비를 막아 메토트렉세이트 같은 다른 약을 쌓을 수 있다 — 상대가 티오퓨린이 아니면 판단이 달라진다 [[?allopurinol-label]]."
    cites: ["harrison-21: 372장 p.2865"]
    covers: ["usmle-2026-0172:A"]
  - contrast: "콜히친 — 매일 먹는 통풍 예방약이고 골수도 억제하는데?"
    point: "콜히친은 P-당단백(P-glycoprotein)과 CYP3A4 로 제거되므로 신기능 저하나 클라리트로마이신 같은 억제제가 있을 때 쌓인다 [[harrison-21: 372장 p.2864]]. 신기능이 정상이고 억제제가 없으며 요산이 떨어졌다면 새 약은 요산 강하제 쪽이다. 콜히친은 요산을 낮추지 않는다."
    cites: ["harrison-21: 372장 p.2864"]
    covers: ["usmle-2026-0172:B"]
  - contrast: "나프록센 — 통풍 예방으로 매일 쓰일 수 있는데?"
    point: "요산 강하제를 시작할 때 발작 예방으로 나프록센 250 mg 하루 2번을 쓰기도 한다 [[harrison-21: 372장 p.2865]]. 그러나 요산을 낮추지 않고 6-MP 대사와 무관하며, 세 계열이 모두 떨어지는 골수 억제는 드물다."
    cites: ["harrison-21: 372장 p.2865"]
    covers: ["usmle-2026-0172:D"]
  - contrast: "프레드니손 — 면역억제제니까 혈구도 줄이나?"
    point: "글루코코르티코이드는 호중구를 혈관벽에서 떼어 내(탈변연, demargination) 오히려 백혈구 수를 늘리고 골수를 억제하지 않는다. 범혈구감소의 원인 약으로 맞지 않는다."
    covers: ["usmle-2026-0172:E"]
tables:
  - id: routes
    section: "기전 — 6-MP 의 세 갈래와 막힌 출구"
    title: "6-MP 가 가는 세 갈래"
    role: comparison
    span: column
    columns: ["효소", "산물", "성격", "막히거나 모자라면"]
    rows:
      - ["HGPRT", "6-티오구아닌 뉴클레오타이드(6-TGN)", "활성 — 골수 억제·면역억제의 본체", "—"]
      - ["TPMT", "6-메틸메르캅토퓨린", "불활성 [[harrison-21: 326장 p.2484]]", "결핍·이형접합이면 6-TGN 이 쌓인다 [[harrison-21: 326장 p.2484]]"]
      - ["크산틴 산화효소(xanthine oxidase)", "6-티오요산", "불활성", "알로푸리놀·페북소스타트가 막으면 6-TGN 이 쌓인다 [[?allopurinol-label]]"]
  - id: gout-drugs
    section: "가르는 소견 — 어느 통풍약인가"
    title: "통풍약과 티오퓨린 골수 억제"
    role: differential
    span: column
    columns: ["약", "작용", "요산", "티오퓨린과"]
    rows:
      - ["알로푸리놀·페북소스타트", "크산틴 산화효소 억제 [[harrison-21: 372장 p.2865]]", "낮춘다", "6-MP 불활성화 차단 → 골수 억제"]
      - ["프로베네시드", "요산 배설 촉진 [[harrison-21: 372장 p.2865]]", "낮춘다", "6-MP 대사와 무관"]
      - ["콜히친", "항염증 — P-당단백·CYP3A4 로 제거 [[harrison-21: 372장 p.2864]]", "그대로", "무관. 신부전·억제제 병용 시 자체 독성"]
      - ["나프록센·프레드니손", "항염증 [[harrison-21: 372장 p.2864]]", "그대로", "무관. 프레드니손은 백혈구를 늘린다"]
criteria:
  - id: xo-dose-cut
    name: 병용 시 감량
    kind: 치료 권고
    population: "아자티오프린·6-MP 복용자에게 알로푸리놀을 함께 쓸 때"
    statement: "아자티오프린·6-MP 를 평소 용량의 1/3~1/4 로 줄이고 혈구를 자주 확인한다"
    exceptions: "허가사항 문구는 원문을 대조하지 못했다(서지만). 페북소스타트는 병용 금기로 표시된다는 것도 원문 미대조"
    source: allopurinol-label
    basis: current
    exams: [usmle, kmle]
  - id: tpmt-monitor
    name: TPMT 와 혈구 감시
    kind: 검사 기준
    population: "티오퓨린 복용자"
    statement: "골수 억제는 용량 의존적이고 늦게 오기도 하므로 혈구·간기능을 정기적으로 본다. TPMT 결핍(약 1/300)·이형접합(약 11 %)은 활성 6-티오구아닌이 쌓여 독성 위험이 높다 [[harrison-21: 326장 p.2484]]"
    exceptions: "TPMT 활성이 정상이어도 크산틴 산화효소 억제제를 더하면 같은 축적이 온다"
    source: harrison-21
    basis: current
    exams: [usmle, kmle]
sources:
  - id: harrison-21
    org: "McGraw Hill"
    title: "Harrison's Principles of Internal Medicine, 21st ed. — Chapter 372: Gout and Other Crystal-Associated Arthropathies; Chapter 326: Inflammatory Bowel Disease"
    kind: textbook
    year: 2022
    citation: "Loscalzo J, Kasper DL, Longo DL, et al (eds). Harrison's Principles of Internal Medicine, 21e. 372장 p.2862–2867(통풍) · 326장 p.2483–2484(아자티오프린·6-MP)"
    checked_at: 2026-09-25
    checked: "본문 대조(드라이브 장별 문서). 372장 p.2864 — 급성 발작 약(NSAID·콜히친·글루코코르티코이드), 콜히친은 P-glycoprotein·CYP3A4 로 제거되어 신질환·클라리트로마이신 등 억제제 병용 시 감량, 기저 혈색소·백혈구·간기능 측정. p.2865 — 알로푸리놀은 크산틴 산화효소 억제제로 1차 요산 강하제, 페북소스타트도 크산틴 산화효소 억제제, 프로베네시드는 2차 요산 배설제로 단독 또는 알로푸리놀과 병용, 요산 강하제 시작 시 콜히친 0.6 mg 1–2회/일 또는 나프록센 250 mg bid 예방. 326장 p.2483–2484 — 아자티오프린은 6-MP 로 바뀌어 활성 산물(thioinosinic acid)로 대사, 골수 억제(특히 백혈구감소)는 용량 의존적이고 늦게 올 수 있어 CBC 정기 감시, TPMT 결핍 1/300·이형접합 11 % 는 활성 6-티오구아닌 대사물 축적으로 독성 위험. 해리슨 두 장 모두 알로푸리놀–아자티오프린 상호작용·크산틴 산화효소에 의한 6-MP 불활성화·감량 비율을 다루지 않는다(검색어 allopurinol·xanthine 이 326장에 없음)."
    verified: text
  - id: allopurinol-label
    org: "U.S. FDA / DailyMed"
    title: "Allopurinol (Zyloprim) prescribing information — Drug interactions: mercaptopurine and azathioprine"
    kind: other
    year: 2023
    url: "https://dailymed.nlm.nih.gov/dailymed/search.cfm?labeltype=all&query=allopurinol"
    checked_at: 2026-09-25
    checked: "기억·서지만 — 컨테이너에서 원문을 열지 못했다. 병용 시 아자티오프린·6-MP 를 평소의 1/3~1/4 로 감량한다는 문구와 판 연도는 대조하지 않았다"
    verified: citation
  - id: cpic-2019
    org: "Clinical Pharmacogenetics Implementation Consortium (Relling MV et al.)"
    title: "CPIC Guideline for Thiopurine Dosing Based on TPMT and NUDT15 Genotypes: 2018 Update"
    kind: guideline
    year: 2019
    citation: "Clin Pharmacol Ther 2019;105(5):1095-1105"
    doi: "10.1002/cpt.1304"
    url: "https://doi.org/10.1002/cpt.1304"
    checked_at: 2026-09-25
    checked: "서지만(기억) — PubMed·doi.org 가 막혀 원문·PMID 를 확인하지 못했다. NUDT15 결핍도 활성 대사물 축적 위험이라는 서술의 근거로만 든다"
    verified: citation
diagram:
  title: "티오퓨린 복용자의 새 골수 억제 — 원인 약 찾기"
  nodes:
    - {id: start, kind: start, text: "티오퓨린 안정 복용 중 새 범혈구감소"}
    - {id: newdrug, kind: decision, text: "최근 추가한 약이 있는가?"}
    - {id: drugask, kind: info, text: "약 목록·시작 날짜·요산 추이를 확인"}
    - {id: base, kind: end, text: "용량·TPMT/NUDT15·다른 원인 평가"}
    - {id: which, kind: decision, text: "크산틴 산화효소를 막는 약인가?"}
    - {id: xo, kind: end, text: "알로푸리놀·페북소스타트 — 활성형 축적"}
    - {id: colch, kind: decision, text: "콜히친 + 신부전·CYP3A4 억제제?"}
    - {id: colchtox, kind: alert, text: "콜히친 축적 독성 의심"}
    - {id: other, kind: end, text: "그 약 자체의 독성·다른 원인 평가"}
  edges:
    - {from: start, to: newdrug}
    - {from: newdrug, to: which, label: "있음"}
    - {from: newdrug, to: base, label: "없음"}
    - {from: newdrug, to: drugask, label: "모름"}
    - {from: drugask, to: which, label: "있으면"}
    - {from: drugask, to: base, label: "없으면"}
    - {from: which, to: xo, label: "예"}
    - {from: which, to: colch, label: "아니오"}
    - {from: colch, to: colchtox, label: "예"}
    - {from: colch, to: other, label: "아니오"}
diagram_notes:
  - "요산이 새 약 뒤 떨어졌다면 그 약은 요산 강하제다 — 그중 6-MP 대사를 막는 것은 크산틴 산화효소 억제제뿐이다(프로베네시드는 배설 촉진)."
  - "TPMT 활성이 정상이어도 크산틴 산화효소 경로가 막히면 활성 6-TGN 이 쌓인다 — 정상 TPMT 는 상호작용을 배제하지 않는다."
  - "TPMT 결핍에 의한 골수 억제는 대개 투약 초기에 오고, 몇 년 안정 뒤 새로 생긴 억제는 새 약·용량 변화를 먼저 찾는다."
  - "콜히친 축적은 신부전·P-당단백/CYP3A4 억제제(클라리트로마이신 등)가 있을 때 의심한다 [[harrison-21: 372장 p.2864]]."
checks:
  - q: "6-MP 를 불활성화하는 두 효소와 그 산물은?"
    a: "TPMT → 6-메틸메르캅토퓨린, 크산틴 산화효소 → 6-티오요산. 활성 경로는 HGPRT → 6-티오구아닌 뉴클레오타이드."
  - q: "알로푸리놀을 더했을 때 아자티오프린 골수 억제가 커지는 이유는?"
    a: "크산틴 산화효소가 막혀 6-MP 가 HGPRT 쪽으로 몰리고 활성 6-TGN 이 쌓이기 때문. 병용하려면 아자티오프린을 1/3~1/4 로 줄인다."
  - q: "TPMT 활성 정상이면 이 상호작용을 배제할 수 있나?"
    a: "아니다. TPMT 는 다른 출구다 — 크산틴 산화효소 출구가 막히면 TPMT 가 정상이어도 활성형이 쌓인다."
variants:
  - id: v1
    of: usmle-2026-0172
    flip: true
    changed: "크레아티닌 0.9·요산 저하·설사·근력 약화 없음 → 크레아티닌 3.1·클라리트로마이신 10일 병용·심한 설사 뒤 근력 약화·요산 8.9 그대로 ⇒ 정답이 알로푸리놀에서 콜히친으로"
    context: "단서를 바꿔 답이 바뀌는 변형 — 신부전과 CYP3A4/P-gp 억제제가 있는 통풍 예방약 복용자"
    stem: "A 67-year-old man is brought to the emergency department because of profuse watery diarrhea and vomiting for 4 days followed by difficulty climbing stairs and rising from a chair. He has chronic kidney disease and Crohn disease that has been in remission with azathioprine at the same dose for 3 years; his blood counts were normal 2 months ago. Six weeks ago he was started on a daily medication to prevent recurrent gout attacks, and 10 days ago he began a course of clarithromycin for community-acquired pneumonia. Temperature is 37.9°C, pulse 104/min, and blood pressure 104/66 mm Hg. There is symmetric proximal muscle weakness. Laboratory studies show hemoglobin 9.4 g/dL, leukocyte count 2,100/mm3, platelet count 88,000/mm3, creatinine 3.1 mg/dL (baseline 2.8 mg/dL), creatine kinase 1,650 U/L, and serum uric acid 8.9 mg/dL (8.7 mg/dL six weeks ago). Which of the following drugs is the most likely cause of this patient's current condition?"
    choices: ["A. Allopurinol", "B. Probenecid", "C. Prednisone", "D. Colchicine", "E. Naproxen"]
    answer: "D"
    explanation: "바뀐 단서는 신부전(크레아티닌 3.1), CYP3A4·P-당단백 억제제인 클라리트로마이신 병용, 설사가 먼저 오고 근병증(근위부 약화·CK 상승)이 뒤따른 경과, 그리고 요산이 그대로라는 점이다. 콜히친은 P-당단백과 CYP3A4 로 제거되므로 신질환이나 클라리트로마이신이 있으면 쌓인다(해리슨 372장 p.2864). 요산이 떨어지지 않았으니 새 예방약은 요산 강하제가 아니다 — 알로푸리놀(크산틴 산화효소 억제로 6-MP 축적)·프로베네시드는 맞지 않는다. 프레드니손은 골수를 억제하지 않고, 나프록센은 이 경과를 설명하지 못한다."
    kind: application
  - id: v2
    of: usmle-2026-0172
    flip: false
    changed: "52세 남자·크론병·아자티오프린·인후통/구내염 → 61세 여자·자가면역 간염·6-MP 직접 복용·잇몸 출혈과 점상출혈, 요산 저하는 먼저 제시 ⇒ 답은 그대로 알로푸리놀"
    context: "겉모습을 바꿔도 답은 그대로인 변형 — 다른 병·다른 티오퓨린·다른 증상"
    stem: "A 61-year-old woman comes to the physician because of gum bleeding, easy bruising, and fatigue for 1 week. Her serum uric acid was 9.4 mg/dL two months ago and is now 4.6 mg/dL. She has autoimmune hepatitis that has been controlled for 4 years with prednisone 5 mg daily and mercaptopurine at an unchanged dose, with normal blood counts at every visit; thiopurine methyltransferase activity was normal before mercaptopurine was started. After two gout attacks this year, a new daily medication was added 6 weeks ago to keep her from having further attacks. Temperature is 37.2°C. There are petechiae on both legs. Hemoglobin is 9.1 g/dL, leukocyte count 1,600/mm3 with an absolute neutrophil count of 400/mm3, and platelet count 41,000/mm3. Creatinine and liver enzymes are within normal limits. Which of the following drugs is the most likely cause of this patient's current condition?"
    choices: ["A. Colchicine", "B. Allopurinol", "C. Probenecid", "D. Indomethacin", "E. Prednisone"]
    answer: "B"
    explanation: "겉모습(성별·기저 질환·아자티오프린 대신 6-MP·출혈 증상·요산을 먼저 제시)은 바뀌었지만 결정적 단서는 그대로다 — 오래 안정적이던 티오퓨린 + 새 통풍 예방약 수주 뒤 세 계열 감소 + 요산 저하 + 정상 TPMT·신기능. 알로푸리놀이 크산틴 산화효소를 막아 6-MP 가 활성 6-TGN 쪽으로 몰렸다. 프로베네시드도 요산을 낮추지만 6-MP 대사를 막지 않고, 콜히친은 신기능 정상이면 쌓일 조건이 약하며 요산을 낮추지 않는다. 프레드니손은 4년간 같은 용량이었다."
    kind: application
---

## 기전 — 6-MP 의 세 갈래와 막힌 출구
아자티오프린은 흡수 뒤 빠르게 6-메르캅토퓨린(6-MP)으로 바뀐다 [[harrison-21: 326장 p.2483]]. 6-MP 는 세 갈래로 나뉜다(표).
- **활성 쪽(HGPRT)**: 6-티오구아닌 뉴클레오타이드(6-TGN)가 되어 DNA 에 끼어들고 퓨린 합성을 막는다 — 분열이 빠른 림프구와 골수 전구세포가 멈추는 것이 면역억제이자 골수 억제다.
- **불활성 출구 두 개**: TPMT 의 메틸화와 크산틴 산화효소(xanthine oxidase)의 산화. 출구가 좁아지면 같은 용량에서도 더 많은 6-MP 가 활성 쪽으로 흘러간다.
- TPMT 결핍·이형접합에서 활성 6-티오구아닌이 쌓여 독성이 커지는 것 [[harrison-21: 326장 p.2484]]과 같은 원리로, **알로푸리놀이 크산틴 산화효소 출구를 막아도** 6-TGN 이 쌓인다 [[?allopurinol-label]]. 알로푸리놀이 요산을 낮추는 바로 그 작용(크산틴 산화효소 억제 [[harrison-21: 372장 p.2865]])이 상호작용의 원인이다.
- 결과는 용량을 몇 배로 올린 것과 같은 골수 억제 — 호중구감소로 발열·인후염·구내염, 혈소판감소로 출혈이 온다. 골수 억제는 용량 의존적이고 늦게 오기도 한다 [[harrison-21: 326장 p.2484]].

## 가르는 소견 — 어느 통풍약인가
- **시간 관계**: 같은 용량으로 오래 안정 → 새 약 수주 뒤 감소. TPMT 결핍에 의한 독성은 대개 시작 초기에 오므로, 늦게 새로 생긴 억제는 새 약을 먼저 찾는다.
- **요산**: 새 약 뒤 요산이 떨어졌으면 요산 강하제다. 그중 6-MP 출구를 막는 것은 크산틴 산화효소 억제제(알로푸리놀·페북소스타트)뿐이다 — 프로베네시드는 배설을 늘릴 뿐이다 [[harrison-21: 372장 p.2865]].
- **콜히친의 조건**: 콜히친도 매일 예방약으로 쓰이지만 쌓이려면 신질환이나 P-당단백·CYP3A4 억제제가 있어야 한다 [[harrison-21: 372장 p.2864]]. 크레아티닌 정상·억제제 없음·요산 저하는 콜히친 쪽을 약하게 만든다.
- 정상 TPMT 는 이 상호작용을 배제하지 않는다 — 다른 출구의 이야기다.

## 선택 — 함께 써야 할 때
- 알로푸리놀이 꼭 필요하면 아자티오프린·6-MP 를 평소의 1/3~1/4 로 줄이고 혈구를 자주 본다 [[?allopurinol-label]].
- 요산만 낮추면 되는데 감량·감시가 어렵다면 6-MP 대사와 무관한 요산 배설제(프로베네시드 — 신기능이 좋을 때)를 생각할 수 있다 [[harrison-21: 372장 p.2865]].
- 이미 범혈구감소·호중구감소성 발열이 왔다면 두 약을 멈추고 발열성 호중구감소증으로 처치한다.

## 권고와 예외
- 티오퓨린 복용 중에는 용량과 무관하게 혈구·간기능을 정기적으로 본다 [[harrison-21: 326장 p.2484]]. 통풍약을 새로 시작할 때 기저 혈구를 재는 것도 같은 이유다 [[harrison-21: 372장 p.2864]].
- 감량 비율(1/3~1/4)과 페북소스타트 병용 금기 표시는 허가사항 원문을 대조하지 못했다(검토 항목).
- NUDT15 결핍도 활성 대사물이 쌓이는 쪽이다 [[?cpic-2019]] — 동아시아인에서 중요하다는 점은 원문 미대조.

## 시험 쟁점 — 충돌·맥락·새 근거
- **Z1 맥락 · 「통풍 예방약」이 가리키는 약** — 시험 기준: 요산이 떨어진 매일 약 = 요산 강하제, 그중 알로푸리놀이 1차 [[harrison-21: 372장 p.2865]] / 다른 기준: 요산 강하제를 시작할 때 발작 예방으로 콜히친 0.6 mg 1–2회/일이나 나프록센 250 mg bid 를 매일 쓴다 [[harrison-21: 372장 p.2865]] / 왜 다른가: 「발작 예방」에는 요산 강하와 항염증 예방 두 뜻이 있다 / 시험에서는: KMLE · USMLE 모두 요산 추이·신기능·병용약으로 가른다. 나프록센을 「예방에 쓰지 않는 약」으로 외우지 않는다.
- **Z2 새 근거 · 상호작용의 근거 위치** — 시험 기준: 알로푸리놀 + 티오퓨린 = 감량 필요 [[?allopurinol-label]] / 다른 기준: 해리슨 21판은 통풍 장(372장 p.2862–2867)과 염증성 장질환 장(326장 p.2483–2484) 모두에서 이 상호작용을 다루지 않고 TPMT 만 적는다 / 왜 다른가: 약물 상호작용은 약리 교과서·허가사항의 영역이다 / 시험에서는: KMLE · USMLE 모두 표준 약리 사실로 출제된다.
