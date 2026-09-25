---
id: cn.obgyn.intrapartum-fhr.nichd-category
type: concept
topic: Obstetrics & Gynecology
date: 2026-09-23
updated: 2026-09-25
version: 2
outline: ob.labor            # 산부인과 손 슬롯 「정상 분만과 진통의 이상」(해리슨 대조 대상 아님 — outline.py --harrison)
confidence: medium
review_status: unreviewed
note_form: 2            # 판형 2(2026-09-25) — 결론·시험 단서·왜 → 혼동 → 표·도식 → 목표에 맞춘 본문
title: "분만 중 태아심박동 — 네 요소로 범주, 범주로 대응"
objective: "분만 중 태아심박동 기록에서 기저선·변이도·가속·감속을 차례로 읽어 NICHD 3단계 범주(I·II·III)를 정하고, 범주에 맞는 대응(일상 감시 · 원인 교정과 자궁내 소생술 · 신속 분만)을 고른다"
objective_kind: 감별
condition: 분만 중 전자태아감시(태아심박동 기록)
exams: [kmle, usmle]
summary:
  - "결론: 범주 I 은 네 조건 모두, III 은 특정 조합, 나머지는 모두 II — 대응은 I 감시 · II 소생술 · III 분만 준비."
  - "시험 단서: 분만 중 전자태아감시(electronic fetal monitoring) 기록 + NICHD 범주·조치 — 기저선을 눈금에 먼저 댄다."
  - "왜: 예후의 무게는 심박수가 아니라 변이도다 — 중등도 변이도·가속이면 그 시점 산증 가능성이 매우 낮다 [[?nichd-2008]]."
  - "범주 I: 기저 110–160/분 · 변이도 중등도(6–25/분) · 후기·가변감속 없음(조기감속·가속 무관) [[?nichd-2008]]."
  - "빈맥 + 중등도 변이도는 범주 II 지만 응급 분만 대상이 아니다. 지연임신 같은 배경은 기록을 대신하지 못한다 [[?acog-pb116]]."
criteria:
  - id: fhr-baseline
    name: 기저 심박수의 정의
    kind: 정의
    population: "분만 중 태아심박동 기록"
    statement: "10분 창에서 가속·감속·현저한 변이 구간을 빼고 5/분 단위로 반올림한 평균이며, 그 창에서 적어도 2분 동안 확인돼야 한다. 정상 110–160/분, 160/분 초과는 빈맥, 110/분 미만은 서맥 [[?nichd-2008]]"
    exceptions: "한 창에서 2분 이상 안정된 구간이 없으면 기저선은 「판정 불가」다 — 앞 10분 창을 참고한다"
    source: nichd-2008
    basis: current
    exams: [kmle, usmle]
  - id: fhr-variability
    name: 기저 변이도의 등급
    kind: 정의
    population: "분만 중 태아심박동 기록"
    statement: "변이도는 진폭(정점–바닥)으로 등급을 매긴다: 소실(보이지 않음) · 최소(5/분 이하) · 중등도(6–25/분) · 현저(25/분 초과) [[?nichd-2008]]"
    exceptions: "사인파형은 규칙적이고 매끄러운 파동이라 변이도로 세지 않는다"
    source: nichd-2008
    basis: current
    exams: [kmle, usmle]
  - id: fhr-accel-decel
    name: 가속과 감속의 정의
    kind: 정의
    population: "분만 중 태아심박동 기록"
    statement: "가속 — 32주 이후 15/분 이상·15초 이상(32주 전 10/분·10초). 조기·후기감속 — 시작에서 바닥까지 30초 이상 걸리는 완만한 감속으로, 조기는 바닥이 수축 정점과 겹치고 후기는 정점 뒤에 온다. 가변감속 — 30초 안에 떨어지는 급격한 감속, 15/분 이상·15초 이상·2분 미만. 지속감속 — 2분 이상 10분 미만. 「반복」 = 20분 동안 수축의 50 % 이상에 동반 [[?nichd-2008]]"
    exceptions: "15초 미만·15/분 미만의 짧은 하강은 감속으로 세지 않는다"
    source: nichd-2008
    basis: current
    exams: [kmle, usmle]
  - id: nichd-three-tier
    name: NICHD 3단계 범주
    kind: 분류
    population: "분만 중 태아심박동 기록"
    statement: "범주 I — 기저 110–160, 변이도 중등도, 후기·가변감속 없음(조기감속·가속 유무 무관). 범주 III — 변이도 소실과 반복 후기감속·반복 가변감속·서맥 중 하나, 또는 사인파형. 범주 II — 나머지 전부 [[?nichd-2008]]"
    exceptions: "범주는 그 시점의 판정이다 — 기록은 계속 바뀌므로 범주도 다시 매긴다"
    source: nichd-2008
    basis: current
    exams: [kmle, usmle]
  - id: category-management
    name: 범주별 대응
    kind: 치료 권고
    population: "분만 중 지속 전자태아감시"
    statement: "범주 I 은 일상 감시. 범주 II 는 원인 평가와 감시 지속, 필요하면 자궁내 소생술(체위 변경, 수액, 수축 과다면 옥시토신 중단·자궁이완제, 반복 가변감속이면 양수주입)을 하고 재평가한다. 범주 III 은 소생술을 하면서 호전되지 않으면 분만을 서두른다 [[?acog-pb116]] [[?acog-pb106]]"
    exceptions: "범주 II 에서 중등도 변이도나 가속이 있으면 산증 가능성이 낮아 감시를 이어 가는 쪽이다 — 변이도가 최소·소실로 떨어지거나 감속이 반복되면 대응 수위를 올린다"
    source: acog-pb116
    basis: current
    exams: [kmle, usmle]
sources:
  - id: nichd-2008
    org: "Eunice Kennedy Shriver National Institute of Child Health and Human Development · ACOG · SMFM (workshop)"
    title: "The 2008 National Institute of Child Health and Human Development Workshop Report on Electronic Fetal Monitoring: Update on Definitions, Interpretation, and Research Guidelines"
    kind: guideline
    year: 2008
    citation: "Macones GA, Hankins GDV, Spong CY, Hauth J, Moore T. Obstet Gynecol 2008;112(3):661-666"
    doi: "10.1097/AOG.0b013e3181841395"
    pmid: "18757666"   # 2026-09-25 PubMed esearch 로 DOI 확인·제목 일치
    checked_at: 2026-09-23
    checked: "서지만(원문 미대조 — 검토 항목). 이 컨테이너는 PubMed·doi 접근이 막혀 기저선·변이도·가속·감속 정의와 3단계 범주 표의 원문 문구를 대조하지 못했다. DOI 도 접근이 막혀 확인하지 못한 값이다. 정의 수치는 문항 해설(imaging-2026-0032·0048)이 이 보고서를 근거로 적은 것과 일치시켰다"
    verified: citation
  - id: acog-pb106
    org: "American College of Obstetricians and Gynecologists"
    title: "ACOG Practice Bulletin No. 106: Intrapartum Fetal Heart Rate Monitoring — Nomenclature, Interpretation, and General Management Principles"
    kind: guideline
    year: 2009
    citation: "Obstet Gynecol 2009;114(1):192-202"
    doi: "10.1097/AOG.0b013e3181aef106"
    pmid: "19546798"   # 2026-09-25 PubMed esearch 로 DOI 확인·제목 일치
    checked_at: 2026-09-23
    checked: "서지만(원문 미대조 — 검토 항목). 범주별 일반 관리 원칙의 원문 문구와 DOI 를 확인하지 못했다"
    verified: citation
  - id: acog-pb116
    org: "American College of Obstetricians and Gynecologists"
    title: "ACOG Practice Bulletin No. 116: Management of Intrapartum Fetal Heart Rate Tracings"
    kind: guideline
    year: 2010
    citation: "Obstet Gynecol 2010;116(5):1232-1240"
    doi: "10.1097/AOG.0b013e3182004fa9"
    pmid: "20966730"   # 2026-09-25 PubMed esearch 로 DOI 확인·제목 일치
    checked_at: 2026-09-23
    checked: "서지만(원문 미대조 — 검토 항목). 자궁내 소생술 표(체위·수액·옥시토신 중단·양수주입)·범주 II 관리 도식의 원문을 대조하지 못했다. DOI 는 접근이 막혀 확인하지 못한 값이다"
    verified: citation
  - id: acog-pb146
    org: "American College of Obstetricians and Gynecologists"
    title: "ACOG Practice Bulletin No. 146: Management of Late-Term and Postterm Pregnancies"
    kind: guideline
    year: 2014
    url: "https://www.acog.org/clinical/clinical-guidance/practice-bulletin"
    checked_at: 2026-09-23
    checked: "번호·제목·연도만(원문 미대조 — 검토 항목). 41주 이후 산전 감시·41–42주 유도 권고의 원문 문구, 이후 개정 여부를 확인하지 못했다. url 은 ACOG 진료지침 목록 쪽이다"
    verified: citation
tables:
  - id: fhr-categories
    title: "NICHD 3단계 범주 — 무엇이 범주를 가르나"
    role: criteria
    span: full
    section: "가르는 소견 — 네 요소를 읽어 범주로"
    columns: ["범주", "기저선", "변이도", "감속", "뜻", "대응"]
    rows:
      - ["I", "110–160/분", "중등도(6–25)", "후기·가변 없음(조기 허용)", "그 시점 산-염기 정상 [[?nichd-2008]]", "일상 감시"]
      - ["II", "빈맥·서맥(변이도 있음) 포함", "최소·현저, 또는 소실(반복 감속 없이)", "단발·반복 감속(변이도 있음), 지속감속", "불확정 — 산증을 단정도 배제도 못함", "원인 찾기 · 자궁내 소생술 · 재평가 [[?acog-pb116]]"]
      - ["III", "서맥(변이도 소실과 함께)", "소실", "반복 후기·반복 가변", "산증 위험 높음 [[?nichd-2008]]", "소생술 + 신속 분만 준비 [[?acog-pb116]]"]
      - ["III(사인파형)", "—", "변이 대신 매끄러운 파동 3–5회/분, 20분 이상", "—", "태아 빈혈 등", "신속 평가·분만 준비"]
    note: "범주 I 은 「모두」, 범주 III 은 「특정 조합」, 범주 II 는 「그 밖의 전부」 — 그래서 범주 II 가 가장 넓다. 모든 정의는 NICHD 2008 보고서(원문 미대조 †)."
  - id: fhr-rate-vs-variability
    title: "심박수 이상 vs 변이도 이상 — 무게가 다르다"
    role: comparison
    span: column
    section: "기전 — 산소 부족에서 변이도 소실로"
    columns: ["소견", "주된 원인", "산증의 신호인가"]
    rows:
      - ["빈맥(>160) + 중등도 변이도", "산모 발열·자궁내 감염, 탈수, β 작용제, 갑상선항진, 태아 빈혈", "아니다 — 원인을 교정하며 감시"]
      - ["변이도 최소·소실", "저산소로 인한 중추 억제, 수면 주기, 마약·황산마그네슘", "지속되면 그렇다 — 가장 무게가 큰 소견"]
      - ["반복 후기감속", "자궁태반 관류 부족", "변이도가 함께 줄면 그렇다"]
      - ["반복 가변감속", "제대 압박(양수과소·양막 파열 뒤)", "깊어지고 변이도가 줄면 그렇다"]
    note: "원인 목록은 문항 해설의 서술을 정리한 것이다 — 원문 대조 전(검토 항목)."
pitfalls:
  - contrast: "빈맥 + 중등도 변이도 vs 최소 변이도 + 반복 가변감속 — 「빈맥이면 나쁜 기록」"
    point: "범주는 네 요소를 따로 읽어 맞춘다. 기저선이 160/분을 넘으면 그것만으로 범주 I 에서 빠져 범주 II 가 되지만, 변이도가 6–25/분이고 수축 뒤 감속이 없으면 「최소 변이도」나 「반복 가변감속」이라는 말을 붙일 근거가 없다. 변이도는 진폭으로(5/분 이하 = 최소), 가변감속은 15/분 이상·15초 이상의 급격한 하강이 수축의 절반 이상에 동반될 때(반복)만 쓴다 [[?nichd-2008]]."
    exception: "빈맥과 함께 변이도가 5/분 이하로 줄거나 수축마다 급격한 하강이 생기면 그때는 최소 변이도·반복 가변감속이 되고, 변이도까지 사라지면 범주 III 으로 간다."
    covers: ["imaging-2026-0032:D"]
  - contrast: "안심되는 변이도·가속 vs 범주 I — 「좋아 보이면 범주 I」"
    point: "범주 I 은 기저선 110–160/분이라는 조건을 포함한다. 변이도·가속이 아무리 좋아도 기저선이 범위를 벗어나면 범주 II 다 — 기록의 눈금(150·160·180 선)에 기저선을 먼저 대 본다 [[?nichd-2008]]."
    exception: "범주 II 라도 중등도 변이도·가속이 있으면 산증 가능성은 낮다 — 범주와 산증 위험은 같은 말이 아니다."
    covers: ["imaging-2026-0032:A"]
  - contrast: "정상 기록의 지연임신 vs 응급 제왕절개 — 「42주·위험 배경이니 개입」"
    point: "응급 분만은 범주 III 이거나 범주 II 가 자궁내 소생술에도 악화될 때의 대응이다 [[?acog-pb116]]. 진통이 이미 시작된 지연임신에서 태아가 진통을 견디는지는 기록이 답한다 — 기저 정상·중등도 변이도·가속·반복 감속 없음(범주 I)이면 일상 감시하며 진통을 지켜본다. 산모의 주수·위험 배경은 감시의 강도를 올릴 이유이지 기록을 건너뛴 개입의 근거가 아니다 [[?acog-pb146]]."
    exception: "같은 산모에서 변이도가 사라지고 반복 후기감속이나 지속 서맥이 나타나면 범주 III 로 분만을 서두른다."
    covers: ["imaging-2026-0048:D"]
  - contrast: "산소·좌측와위 vs 경과 관찰 — 「해가 없으니 해 두자」"
    point: "자궁내 소생술은 교정할 이상(후기감속·반복 가변감속·변이도 감소·수축 과다)이 있을 때의 대응이다. 범주 I 기록에는 교정할 대상이 없으므로 시험은 일상 감시를 답으로 둔다 [[?acog-pb116]]."
    exception: "범주 II 의 반복 후기감속이 나타나면 체위 변경·수액·옥시토신 중단이 첫 대응이다."
  - contrast: "양수주입 vs 체위·산소 — 「가변감속이면 양수주입」"
    point: "양수주입은 양막이 파열된 뒤 제대 압박으로 반복 가변감속이 생기고 다른 소생술로 호전되지 않을 때 쓴다. 양막이 온전하거나 감속이 없으면 적응이 아니다 [[?acog-pb116]]."
    exception: "후기감속(관류 부족)에는 양수주입이 원인을 다루지 못한다 — 체위·수액·수축 조절이 먼저다."
diagram:
  title: "분만 중 태아심박동 기록 — 범주와 대응"
  nodes:
    - {id: start, kind: start, text: "분만 중 지속 전자태아감시 — 네 요소를 차례로 읽는다"}
    - {id: cat3, kind: decision, text: "범주 III 조합 또는 사인파형?"}
    - {id: info, kind: info, text: "기저선 불안정·신호 끊김 — 더 보거나 내부 감시"}
    - {id: cat1, kind: decision, text: "범주 I 조건을 모두 채우는가?"}
    - {id: cat2, kind: step, text: "범주 II — 원인 찾기 + 필요하면 자궁내 소생술"}
    - {id: reassure, kind: decision, text: "중등도 변이도 또는 가속이 있는가?"}
    - {id: end1, kind: end, text: "범주 I — 일상 감시, 진통 경과 관찰"}
    - {id: end2a, kind: end, text: "산증 가능성 낮음 — 원인 교정하며 감시·재평가"}
    - {id: end2b, kind: end, text: "산증 배제 못함 — 소생술에 반응 없으면 분만 서두름"}
    - {id: end3, kind: end, text: "범주 III — 자궁내 소생술과 동시에 신속 분만 준비"}
  edges:
    - {from: start, to: cat3}
    - {from: cat3, to: end3, label: "있음"}
    - {from: cat3, to: cat1, label: "없음"}
    - {from: cat3, to: info, label: "판독 불가"}
    - {from: info, to: cat1, label: "판독 가능해짐"}
    - {from: cat1, to: end1, label: "모두 충족"}
    - {from: cat1, to: cat2, label: "하나라도 벗어남"}
    - {from: cat2, to: reassure}
    - {from: reassure, to: end2a, label: "있음"}
    - {from: reassure, to: end2b, label: "없음(최소·소실 지속)"}
diagram_notes:
  - "범주 III 조합 = 변이도 소실 + (반복 후기감속 · 반복 가변감속 · 서맥 가운데 하나), 또는 사인파형 [[?nichd-2008]]."
  - "범주 I 조건 = 기저 110–160/분 · 변이도 중등도 · 후기·가변감속 없음 — 하나라도 벗어나면 범주 II."
  - "판독 불가 = 기저선이 2분 이상 안정되지 않거나 신호가 끊긴다 — 기록을 더 보고, 필요하면 내부 감시(두피 전극·자궁내압 카테터)."
  - "범주 II 의 원인 찾기 = 발열 · 수축 과다 · 저혈압 · 약물. 가속에는 자극으로 유도된 가속도 포함한다."
  - "「없음」 갈래 = 변이도가 최소·소실로 지속될 때."
  - "범주는 판정 시점의 것이다 — 범주 I 이던 기록도 몇 분 뒤 범주 II·III 로 바뀔 수 있어 매 평가마다 다시 매긴다."
  - "32주 전에는 가속 기준이 10/분·10초로 낮다 [[?nichd-2008]]."
  - "자궁내 소생술의 구체 조치(체위 · 수액 · 옥시토신 중단 · 자궁이완제 · 양막 파열 뒤 반복 가변감속의 양수주입)는 원인에 맞춰 고른다 [[?acog-pb116]]."
  - "외부 토코는 수축의 빈도와 시간만 보여 준다 — 진폭으로 수축 강도를 판단하지 않는다."
checks:
  - q: "범주 I 의 조건 넷은?"
    a: "기저 110–160/분, 변이도 중등도(6–25/분), 후기감속 없음, 가변감속 없음(조기감속·가속 유무는 무관)."
  - q: "범주 III 에 드는 두 가지 형태는?"
    a: "변이도 소실과 함께 반복 후기감속·반복 가변감속·서맥 중 하나, 또는 사인파형."
  - q: "기저 165/분, 변이도 8/분, 가속 있음, 감속 없음 — 범주는?"
    a: "범주 II(빈맥). 산증 가능성은 낮고, 산모 발열·감염·탈수·약물 등 원인을 찾으며 감시한다."
  - q: "중등도 변이도가 가진 뜻은?"
    a: "그 시점에 태아 대사성 산증 가능성이 매우 낮다는 뜻이다 — 가속이 있으면 더 확실하다."
  - q: "응급 분만을 고르는 기록은?"
    a: "범주 III, 또는 범주 II 가 자궁내 소생술에도 악화될 때."
variants:
  - id: v1
    of: imaging-2026-0032
    flip: true
    changed: "기저선 「160/분 선 위(≈163)」를 「140/분 안팎」으로 바꾸고 나머지(중등도 변이도·가속·감속 없음)는 그대로 → 기저선 조건이 채워져 답이 「범주 II 빈맥」에서 「범주 I」로 바뀜"
    context: "단서를 바꿔 답이 바뀌는 변형 — 기저선만 정상 범위로"
    stem: "A 26-year-old woman, gravida 1, para 0, at 40 weeks' gestation is in active labor with continuous external fetal monitoring. Her temperature is 37.0°C (98.6°F). Over a 10-minute window, the fetal heart rate baseline is 140/min with an amplitude of fluctuation of about 10/min. Two rises of 20/min lasting about 30 seconds each are seen. Contractions occur every 3 minutes, and none is followed by a fall in heart rate. Which of the following best describes this tracing according to the NICHD three-tier system?"
    choices: ["A. Category I", "B. Category II because of fetal tachycardia", "C. Category II because of minimal variability", "D. Category III because of recurrent variable decelerations", "E. Category III because of a sinusoidal pattern"]
    answer: "A"
    explanation: "Baseline 140/min lies within 110–160/min, fluctuation of about 10/min is moderate variability (6–25/min), the rises meet the acceleration definition (≥15/min for ≥15 s after 32 weeks), and there are no late or variable decelerations — every Category I condition is met [[?nichd-2008]]. In the original item the baseline sat above 160/min; that single element moved an otherwise reassuring tracing into Category II. Variability here is not minimal (≤5/min), and there are no decelerations or regular sine waves."
    kind: application
  - id: v2
    of: imaging-2026-0032
    flip: false
    changed: "산모 나이·경산 여부·양막 파열·산모 발열(38.4 ℃)을 새로 넣고 기저선 수치를 170/분으로 바꿨지만 「기저 >160 · 변이도 중등도 · 감속 없음」은 그대로 → 답은 여전히 「범주 II 빈맥(변이도 중등도, 감속 없음)」"
    context: "겉모습만 바꾸고 답은 같은 변형 — 발열 산모의 빈맥"
    stem: "A 31-year-old woman, gravida 3, para 2, at 39 weeks' gestation has had ruptured membranes for 20 hours and is now in labor. Her temperature is 38.4°C (101.1°F). Continuous external fetal monitoring over 10 minutes shows a baseline of 170/min with fluctuations of 10–15/min and one rise of 18/min lasting 25 seconds. Contractions occur every 4 minutes without any associated fall in fetal heart rate. Which of the following best describes this tracing according to the NICHD three-tier system?"
    choices: ["A. Category I: normal baseline with moderate variability", "B. Category II: fetal tachycardia with moderate variability and no decelerations", "C. Category II: minimal variability with recurrent late decelerations", "D. Category III: absent variability with fetal tachycardia", "E. Category III: sinusoidal pattern"]
    answer: "B"
    explanation: "A baseline above 160/min for the 10-minute window is fetal tachycardia, which excludes Category I; variability of 10–15/min is moderate and there are no decelerations, so nothing places it in Category III [[?nichd-2008]]. The fever, prolonged rupture of membranes and multiparity change the story, not the reading — the likely cause (intra-amniotic infection) is sought and treated while monitoring continues. Minimal variability requires amplitude ≤5/min, and Category III requires absent variability with recurrent decelerations or bradycardia, or a sinusoidal pattern."
    kind: application
  - id: v3
    of: imaging-2026-0048
    flip: true
    changed: "기록을 「기저 140~145·변이도 중등도·가속·반복 감속 없음」에서 「기저 145·변이도 중등도·대부분의 수축 정점 뒤 완만한 감속 반복」으로 바꿈 → 범주 II(반복 후기감속)라 답이 「지속 감시하며 경과 관찰」에서 「산소 투여와 좌측와위(자궁내 소생술)」로 바뀜"
    context: "단서를 바꿔 답이 바뀌는 변형 — 지연임신 진통 중 반복 후기감속"
    stem: "30세 초산부가 임신 42주 1일에 규칙적인 진통으로 입원하였다. 자궁경부는 5 cm 개대되었고 양막은 파열되지 않았다. 옥시토신은 투여하지 않았다. 지속 전자태아감시에서 기저 태아심박동은 145회/분, 변이도는 8~12회/분이다. 최근 20분 동안 3분 간격의 자궁수축 7회 가운데 5회에서 수축 정점이 지난 뒤 완만하게 시작해 수축이 끝난 뒤 회복되는 감속(최저 125회/분)이 보인다. 산모 혈압은 100/60 mmHg 이고 반듯이 누워 있다. 가장 먼저 할 조치는?"
    choices: ["A. 지속 감시하며 진통 경과 관찰", "B. 산소 투여와 좌측와위, 수액 투여", "C. 양수주입", "D. 응급 제왕절개술", "E. 옥시토신으로 진통 촉진"]
    answer: "B"
    explanation: "수축 정점 뒤에 최저점이 오는 완만한 감속이 수축의 절반 이상에 동반되면 반복 후기감속이다. 변이도는 중등도로 유지되어 범주 III 이 아니라 범주 II 이며, 자궁태반 관류를 높이는 자궁내 소생술(측와위로 대정맥 압박 해소·수액·산소)이 첫 대응이다 [[?acog-pb116]]. 원래 문항은 반복 감속이 없는 범주 I 이라 경과 관찰이 답이었다. 양수주입은 양막 파열 뒤 반복 가변감속의 대응이고, 응급 제왕절개는 변이도 소실이 겹치거나 소생술에도 악화될 때, 옥시토신은 관류를 더 줄이므로 금한다."
    kind: application
  - id: v4
    of: imaging-2026-0048
    flip: false
    changed: "지연임신·경산부를 「39주 초산부·양막 파열(맑은 양수)」로, 가속 대신 「수축과 겹치는 조기감속」을 넣고 「기저 정상·변이도 중등도·후기·가변감속 없음」은 그대로 → 범주 I 이라 답은 여전히 「지속 감시하며 진통 경과 관찰」"
    context: "겉모습만 바꾸고 답은 같은 변형 — 양막 파열·조기감속이 있는 범주 I"
    stem: "24세 초산부가 임신 39주 2일에 진통으로 입원하였다. 2시간 전 양막이 자연 파열되었고 양수는 맑다. 자궁경부는 7 cm 개대되었다. 지속 전자태아감시에서 기저 태아심박동은 130회/분, 변이도는 10~15회/분이다. 자궁수축이 시작될 때 함께 완만하게 떨어져 수축 정점에 최저점(118회/분)을 이루고 수축이 끝나면 기저선으로 돌아오는 감속이 대부분의 수축에서 보인다. 급격한 하강이나 수축 정점 뒤에 최저점이 오는 감속은 없다. 가장 적절한 조치는?"
    choices: ["A. 양수주입", "B. 산소 투여와 좌측와위", "C. 지속 감시하며 진통 경과 관찰", "D. 태아 두피 혈액 pH 검사", "E. 응급 제왕절개술"]
    answer: "C"
    explanation: "수축과 거울처럼 겹치는 완만한 감속은 조기감속으로, 태아 머리 압박에 의한 미주신경 반응이며 범주 I 에 허용된다. 기저 130회/분·변이도 중등도·후기·가변감속 없음이므로 범주 I 이고 일상 감시하며 진통을 지켜본다 [[?nichd-2008]]. 양막이 파열되었더라도 반복 가변감속이 없으면 양수주입의 적응이 아니고, 교정할 이상이 없어 소생술·침습 검사·응급 분만도 필요 없다."
    kind: application
---

## 판단 — 범주를 읽는 순서와 대응
- 분만 중 전자태아감시는 태아심박동과 자궁수축을 함께 기록해, 진통이라는 반복되는 산소 공급 감소를 태아가 견디고 있는지 판단하는 검사다. 기록을 **네 요소(기저선·변이도·가속·감속)로 쪼개 읽는다** [[?nichd-2008]].
- 범주를 가르는 규칙은 비대칭이다 — 범주 I 은 조건을 **모두** 채워야 하고, 범주 III 은 **특정 조합**만 들어가며, 나머지는 **모두** 범주 II 다 [[?nichd-2008]]. 그래서 좋아 보이는 기록도 한 요소(예: 기저선 165)가 벗어나면 범주 II 이고, 나빠 보이는 기록도 변이도가 남아 있으면 범주 III 이 아니다.
- 판정 순서를 「범주 III 조합이 있나 → 범주 I 을 모두 채우나 → 나머지는 II」로 두면 틀리지 않는다(도식).
- 대응은 범주를 따른다 — 응급 분만은 범주 III 이거나 범주 II 가 소생술에도 악화될 때다 [[?acog-pb116]].

## 기전 — 산소 부족에서 변이도 소실로
**정상 기능.** 태아 심박수는 동방결절의 고유 속도에 교감·부교감 신경의 끊임없는 조절이 얹힌 결과다. 뇌간과 대뇌피질이 산소를 충분히 받는 동안 자율신경은 박동마다 속도를 조금씩 바꾸고(변이도), 태아가 움직이면 교감 신경이 속도를 잠깐 올린다(가속). 자궁수축은 근육층을 지나는 나선동맥을 눌러 태반 사이 공간의 혈류를 잠시 줄이지만, 정상 태반의 예비력은 수축 사이의 회복으로 그 부족을 메운다.

**이상이 생기는 기전.** 세 가지 길이 있다. ① **머리 압박** — 두개 내압이 오르면 미주 반사로 수축과 동시에 심박이 완만히 떨어졌다 돌아온다(조기감속, 무해). ② **제대 압박** — 제대정맥·동맥이 눌리면 압수용체 반사로 심박이 **급격히** 떨어진다(가변감속). 양수과소·양막 파열 뒤 흔하다. ③ **자궁태반 관류 부족** — 수축 동안 산소가 모자라면 화학수용체를 거쳐 수축 정점이 **지난 뒤** 완만하게 떨어지고 늦게 회복한다(후기감속). 저산소가 계속되면 대사성 산증이 쌓이고 중추신경이 억제되어 **변이도가 줄다가 사라진다** — 그래서 변이도가 산증의 가장 중요한 창이다 [[?nichd-2008]].

**심박수 자체의 변화.** 빈맥은 대개 태아 밖의 자극이나 태아 빈혈·빈맥성 부정맥에서 온다(표). 변이도가 유지되면 자율신경이 제대로 일한다는 뜻이라, 빈맥만으로 산증을 뜻하지 않는다.

## 가르는 소견 — 네 요소를 읽어 범주로
- **기저선(baseline)** — 10분 창에서 가속·감속·현저 변이 구간을 뺀 평균을 5/분 단위로 반올림하고, 2분 이상 안정된 구간이 필요하다. 110–160 정상, 160 초과 빈맥, 110 미만 서맥 [[?nichd-2008]]. 눈금선(150·160·180)에 대 보고 읽는다.
- **변이도(variability)** — 진폭으로 등급을 매긴다: 소실 · 최소(≤5) · 중등도(6–25) · 현저(>25). 중등도면 그 시점의 산증 가능성이 매우 낮다 [[?nichd-2008]].
- **가속(acceleration)** — 32주 이후 15/분·15초 이상. 있으면 산증을 거의 배제한다.
- **감속(deceleration)** — 모양(완만 vs 급격)과 수축과의 시간 관계(동시 vs 정점 뒤)로 조기·후기·가변을 가르고, 20분 동안 수축의 절반 이상에 동반되면 「반복」이다. 15초 미만의 짧은 하강은 감속으로 세지 않는다 [[?nichd-2008]].
- **사인파형(sinusoidal pattern)** — 3–5회/분의 매끄러운 규칙 파동이 20분 이상, 변이도 없음. 태아 빈혈에서 전형적이다.

## 검사 — 외부·내부 감시와 산증 확인
- **외부 감시**(도플러 + 토코): 비침습이지만 산모 심박을 잡거나 신호가 끊길 수 있고, 토코는 수축의 **빈도와 시간**만 보여 준다(강도는 아님).
- **내부 감시**: 태아 두피 전극(신호가 나쁠 때), 자궁내압 카테터(수축 강도가 필요할 때) — 양막 파열 뒤에만 쓸 수 있다.
- **범주 II 에서 산증 여부 확인**: 두피 자극으로 가속이 유도되면 산증 가능성이 낮다. 태아 두피 혈액 pH 는 일부 기관에서 쓰는 보조 검사다.

## 선택 — 범주별 대응과 재평가
- **범주 I** — 일상 감시. 산모의 주수(지연임신)나 위험 배경은 감시를 지속할 이유이지, 정상 기록을 건너뛰고 개입할 근거가 아니다 [[?acog-pb146]].
- **범주 II** — 원인을 찾고(체온, 혈압, 수축 빈도, 약물) 원인에 맞춰 **자궁내 소생술(intrauterine resuscitation)**을 한다: 측와위(대정맥 압박 해소·제대 압박 이동), 수액, 수축 과다면 옥시토신 중단·자궁이완제, 양막 파열 뒤 반복 가변감속이 계속되면 양수주입 [[?acog-pb116]]. 중등도 변이도·가속이 있으면 감시를 이어 간다.
- **범주 III** — 소생술을 하면서 호전되지 않으면 분만을 서두른다(방법은 진통 단계에 따라) [[?acog-pb116]].
- **반응 확인·재평가**: 조치 뒤 기록을 다시 읽어 범주를 새로 매긴다. 범주 II 에서 변이도가 최소·소실로 떨어지거나 감속이 반복·심화되면 대응 수위를 올리고, 소생술로 감속이 사라지고 변이도가 유지되면 감시로 돌아간다.

## 권고와 예외
- 변이도가 가장 무거운 소견이다 — 중등도 변이도·가속은 그 시점의 산증을 거의 배제한다.
- 양수주입은 양막 파열 뒤 반복 가변감속에만, 옥시토신은 후기감속·수축 과다에서 멈춘다.
- 태아 부정맥 진단이나 진통 이상(분만 정지) 자체는 이 정리본의 범위 밖이다.
- 이 슬롯(분만)은 해리슨이 다루지 않는 자리라 해리슨 대조 대상이 아니다. NICHD 2008·ACOG 진료지침은 원문을 열지 못해 서지만 남겼다(검토 항목).

## (심화) 왜 범주 II 가 그렇게 넓은가
분만 중 감시의 목적은 「산증이 생기기 전에 알아채는 것」인데, 기록이 산증을 **확실히 배제**하는 경우(범주 I)와 **강하게 시사**하는 경우(범주 III)는 둘 다 좁다. 그 사이의 대부분은 태아가 스트레스에 반응하고 있지만 아직 보상 중인 상태라, 기록 하나로 정답을 내릴 수 없다. 그래서 NICHD 는 이 넓은 영역을 「불확정」으로 묶고 **변이도·가속이라는 보상의 증거**로 다시 가르게 했다 [[?nichd-2008]]. 범주 II 의 대응이 「원인 찾기」와 「소생술」이고, 범주 III 만 「분만을 서두름」인 이유다.
