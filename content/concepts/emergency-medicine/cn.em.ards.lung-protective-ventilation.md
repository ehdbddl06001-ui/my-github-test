---
id: cn.em.ards.lung-protective-ventilation
type: concept
topic: Emergency Medicine
see_also: [Pulmonology, Cardiology]
date: 2026-09-23
updated: 2026-09-23
version: 1
outline: h301            # 기본틀 슬롯(content/outline/subjects.yaml) — 해리슨 21판 301장 Acute Respiratory Distress Syndrome(응급의학과 책)
confidence: medium
review_status: unreviewed
title: "급성호흡곤란증후군 — 심장 원인을 배제한 뒤 첫 처치는 저일회호흡량 폐보호 환기"
objective: "양측 폐 음영과 저산소혈증이 심부전·용적 과부하로 설명되지 않을 때 Berlin 기준(발병 시기·양측 음영·PEEP ≥ 5 에서 PaO2/FiO2·정수압성 부종 배제)으로 급성호흡곤란증후군과 중증도를 판단하고, 첫 처치로 일회호흡량 6 mL/kg 예측체중·고평부압 ≤ 30 cm H2O 폐보호 환기를 고르며, 이뇨·PEEP·복와위의 자리를 가른다"
objective_kind: 다음 처치
condition: 급성호흡곤란증후군(ARDS)
exams: [kmle, usmle]
summary:
  - "ARDS 는 폐포-모세혈관 장벽이 손상돼 단백이 많은 부종액이 폐포를 채우는 염증성(투과성) 부종이다. 심부전의 정수압성 부종과 흉부 사진은 비슷할 수 있어, 심장 원인을 객관적으로 배제해야 진단이 선다."
  - "Berlin 기준: 유발 요인·호흡 증상 뒤 1주 안 발병 · 흉수·허탈·결절로 설명되지 않는 양측 음영 · 정수압성 부종이 주원인이 아님 · PEEP ≥ 5 cm H2O 에서 PaO2/FiO2 로 경증(200–300)·중등증(100–200)·중증(≤ 100)."
  - "부종은 아래쪽(의존 부위) 폐에 몰려 통기되는 폐가 작다. 정상 크기의 일회호흡량은 이 작은 폐를 과팽창시키고(volutrauma), 허탈된 폐포를 매 호흡마다 열고 닫아(atelectrauma) 손상을 키운다."
  - "그래서 첫 처치는 혈액가스 정상화가 아니라 폐보호 환기다 — 일회호흡량 6 mL/kg 예측체중, 고평부압 ≤ 30 cm H2O(ARDS Network: 사망 40 % → 31 %). 고탄산혈증은 허용한다."
  - "PEEP 는 허탈을 막아 산소화를 돕고(낮추지 않는다), 중증(PaO2/FiO2 < 150)은 복와위로 사망률이 줄었다. 체액은 저혈압·저관류가 없는 한 제한·이뇨로 좌심방압을 낮게 유지한다 — 이뇨는 금기가 아니라 환기 설정 다음의 보조다."
criteria:
  - id: berlin-2012
    name: ARDS 진단 기준(Berlin)
    kind: 진단 기준
    population: "급성 저산소성 호흡부전 성인"
    statement: "발병: 알려진 유발 요인 또는 새롭거나 악화된 호흡 증상 뒤 1주 안 · 영상: 흉수·폐엽/폐 허탈·결절로 충분히 설명되지 않는 양측 음영 · 부종의 원인: 정수압성 부종이 호흡부전의 주원인이 아님(유발 요인이 없으면 심초음파 같은 객관적 평가로 배제) · 산소화: PEEP ≥ 5 cm H2O 에서 경증 200 < PaO2/FiO2 ≤ 300, 중등증 100 < … ≤ 200, 중증 ≤ 100 mm Hg [[harrison-21: 301장 p.2226]]"
    exceptions: "PaO2/FiO2 는 PEEP ≥ 5 에서 잰 값이어야 한다 — PEEP 없이 잰 비율로 등급을 매기지 않는다. 2023–2024 「새 전 세계 정의」는 고유량 비강 산소·SpO2/FiO2 를 받아들인다는 보고가 있으나 원문 미대조 [[?global-ards-2024]]"
    source: harrison-21
    basis: current
    exams: [kmle, usmle]
  - id: lpv-armanet
    name: 폐보호 환기
    kind: 치료 권고
    population: "기계환기 중인 ARDS"
    statement: "일회호흡량 6 mL/kg 예측체중(키·성별로 계산), 고평부압 ≤ 30 cm H2O(흡기 끝 0.5초 멈춤에서 잰 값). 12 mL/kg·≤ 50 cm H2O 와 비교한 무작위 시험에서 사망률 31 % 대 40 % — 해리슨 권고 등급 A [[harrison-21: 301장 p.2228–2229]]"
    exceptions: "산증은 pH ≥ 7.30 을 목표로 호흡수(≤ 35회/분)로 보정한다 — 일회호흡량을 늘려 PaCO2 를 맞추지 않는다 [[harrison-21: 301장 p.2229]]"
    source: harrison-21
    basis: current
    exams: [kmle, usmle]
  - id: prone-severe
    name: 복와위 환기
    kind: 치료 권고
    population: "중증 ARDS(PaO2/FiO2 < 150 mm Hg)"
    statement: "복와위 환기로 28일 사망률이 32.8 % 에서 16.0 % 로 줄었다(2013 시험). 숙련된 팀이 필요하다 — 권고 등급 B [[harrison-21: 301장 p.2228]]"
    exceptions: "삽관관 빠짐·중심정맥관 이탈·정형외과적 손상 위험이 있다 [[harrison-21: 301장 p.2228]]"
    source: harrison-21
    basis: current
    exams: [kmle, usmle]
  - id: fluid-conservative
    name: 체액 관리
    kind: 치료 권고
    population: "ARDS"
    statement: "좌심방 충만압을 낮게 유지(수액 제한·이뇨제)하면 산소화·폐 역학이 좋아지고 기계환기·ICU 기간이 준다. 저혈압·주요 장기(콩팥) 저관류가 한계다 — 권고 등급 B [[harrison-21: 301장 p.2228]]"
    exceptions: "쇼크·저관류가 있으면 이뇨보다 관류 유지(평균동맥압 ≥ 65 mm Hg)가 앞선다 [[harrison-21: 301장 p.2229]]"
    source: harrison-21
    basis: current
    exams: [kmle, usmle]
sources:
  - id: harrison-21
    org: "McGraw Hill"
    title: "Harrison's Principles of Internal Medicine, 21st ed. — Chapter 301: Acute Respiratory Distress Syndrome"
    kind: textbook
    year: 2022
    citation: "Loscalzo J, Fauci AS, Kasper DL, et al (eds). Harrison's Principles of Internal Medicine, 21e. 301장 Acute Respiratory Distress Syndrome(Baron RM, Levy BD), 인쇄쪽 2225–2229"
    checked_at: 2026-09-23
    checked: "드라이브 장 문서로 본문 대조. p.2225 정의(급성 호흡곤란·저산소혈증·미만성 침윤), 원인(폐렴·패혈증 40–60 %, 흡인·외상·다량 수혈·약물 과다), 직접/간접 손상 표. p.2226 삼출기(내피·제1형 폐포세포 손상, 단백 부종, 유리막, 의존 부위 부종·허탈 → 단락·저산소혈증, 사강 증가로 고탄산혈증), 흉부 사진이 심인성 부종과 구별 어려움·심비대·흉수·혈관 재분포가 없을 수 있음, 유발 요인 없으면 심초음파로 정수압성 부종 배제, 표 301-2 Berlin(1주·양측 음영·PEEP ≥ 5 의 PaO2/FiO2 경증/중등증/중증), 감별(심인성 부종·양측 폐렴·폐포 출혈). p.2228 volutrauma·atelectrauma, 의존 부위 위주 이질성, ARDS Network 6 대 12 mL/kg 예측체중·고평부압 ≤ 30 대 ≤ 50·사망 31 % 대 40 %, PEEP 최적 설정 합의 없음, 복와위(PaO2/FiO2 < 150, 32.8 → 16.0 %), 재개방 수기·고빈도 환기 이득 없음, ECMO 선택적 구조 치료, 체액 제한·이뇨(저혈압·저관류가 한계), 신경근차단 48시간(첫 시험 이득, 후속 시험 이득 없음), 스테로이드 일상 사용 근거 없음, 흡입 혈관확장제 생존 이득 없음. p.2229 표 301-3 권고 등급(저일회호흡량 A, 좌심방압 최소화 B, 고PEEP·복와위·ECMO B, 재개방 수기 C, 고빈도 D, 스테로이드 D), 그림 301-5 목표(VT ≤ 6 mL/kg PBW, Pplat ≤ 30, RR ≤ 35, FiO2 ≤ 0.6, SpO2 88–95 %, MAP ≥ 65, pH ≥ 7.30), 중증도별 사망(LUNG SAFE 34.9/40.3/46.1 %). 이 장은 비-COVID ARDS 만 다룬다(COVID ARDS 는 199장 — 읽지 않음)"
    verified: text
  - id: berlin-jama-2012
    org: "ARDS Definition Task Force"
    title: "Acute respiratory distress syndrome: the Berlin Definition"
    kind: guideline
    year: 2012
    citation: "ARDS Definition Task Force; Ranieri VM, Rubenfeld GD, Thompson BT, et al. JAMA 2012;307(23):2526-2533"
    doi: "10.1001/jama.2012.5669"
    url: "https://doi.org/10.1001/jama.2012.5669"
    checked_at: 2026-09-23
    checked: "서지만(원문 미대조 — 이 컨테이너는 doi·PubMed 접근이 막혀 있다). 기준 문구는 해리슨 301장 표 301-2 로 대조했다. DOI 는 접근이 막혀 확인하지 못한 값이다"
    verified: citation
  - id: ardsnet-arma-2000
    org: "Acute Respiratory Distress Syndrome Network"
    title: "Ventilation with lower tidal volumes as compared with traditional tidal volumes for acute lung injury and the acute respiratory distress syndrome"
    kind: trial
    year: 2000
    citation: "N Engl J Med 2000;342(18):1301-1308"
    doi: "10.1056/NEJM200005043421801"
    url: "https://doi.org/10.1056/NEJM200005043421801"
    checked_at: 2026-09-23
    checked: "서지만(원문 미대조 — doi 접근 막힘). 설계·결과(6 대 12 mL/kg PBW, 사망 31 % 대 40 %)는 해리슨 301장 p.2228 서술로 대조했다. 문항 해설의 861명·39.8 % 대 31.0 % 는 원문 미대조"
    verified: citation
  - id: global-ards-2024
    org: "American Thoracic Society (ATS)"
    title: "A New Global Definition of Acute Respiratory Distress Syndrome"
    kind: guideline
    year: 2024
    citation: "Matthay MA, Arabi Y, Arroliga AC, et al. Am J Respir Crit Care Med 2024;209(1):37-47"
    doi: "10.1164/rccm.202303-0558WS"
    url: "https://doi.org/10.1164/rccm.202303-0558WS"
    checked_at: 2026-09-23
    checked: "서지만(원문 미대조 — doi·PubMed 접근 막힘). 고유량 비강 산소·SpO2/FiO2 수용 등 내용은 확인하지 못해 [[?]] 로만 인용한다. 서지 세부(권·쪽·DOI)는 기억에서 옮긴 것이라 검토 항목"
    verified: citation
  - id: acc-aha-hf-2022
    org: "American Heart Association / American College of Cardiology / Heart Failure Society of America"
    title: "2022 AHA/ACC/HFSA Guideline for the Management of Heart Failure"
    kind: guideline
    year: 2022
    citation: "Heidenreich PA, Bozkurt B, Aguilar D, et al. Circulation 2022;145(18):e895-e1032"
    doi: "10.1161/CIR.0000000000001063"
    url: "https://doi.org/10.1161/CIR.0000000000001063"
    checked_at: 2026-09-23
    checked: "서지만(원문 미대조 — doi 접근 막힘). 심인성 폐부종의 울혈 치료(고리 이뇨제 정맥 투여)와 BNP 의 쓰임은 원문 문구를 대조하지 못했다"
    verified: citation
tables:
  - id: ards-vs-hydrostatic
    title: "양측 폐 음영 + 저산소혈증 — ARDS 와 심인성 폐부종 가르기"
    role: differential
    span: full
    section: 감별
    columns: ["구분", "ARDS(투과성 부종)", "심인성 폐부종(정수압성)", "가르는 근거"]
    rows:
      - ["기전", "폐포-모세혈관 장벽 손상 → 단백 많은 부종액 [[harrison-21: 301장 p.2225–2226]]", "좌심방압 상승 → 모세혈관 정수압 상승", "장벽이 망가졌나, 압력이 높나"]
      - ["선행 사건", "폐렴·패혈증·흡인·외상·수혈 뒤 1주 안 [[harrison-21: 301장 p.2225]]", "심근경색·심근병증·판막병·용적 과부하", "유발 요인이 없으면 심장 원인을 객관적으로 배제해야 한다"]
      - ["흉부 사진", "양측 음영, 심비대·흉수·혈관 재분포가 없을 수 있음 [[harrison-21: 301장 p.2226]]", "심비대·흉수·상엽 혈관 재분포·Kerley B 선", "사진만으로는 구별되지 않는 경우가 많다 [[harrison-21: 301장 p.2226]]"]
      - ["심장 평가", "심초음파 좌심실 기능 정상, 경정맥 팽대·말초 부종 없음", "좌심실 확장·수축 저하 또는 중증 판막병, 경정맥 팽대", "심초음파가 객관적 배제 수단 [[harrison-21: 301장 p.2226]]"]
      - ["첫 처치", "폐보호 환기(6 mL/kg PBW, Pplat ≤ 30)·PEEP [[harrison-21: 301장 p.2228]]", "이뇨제·혈관확장제, 원인 심질환 치료 [[?acc-aha-hf-2022]]", "진단이 처치를 가른다"]
    note: "BNP 는 심부전 쪽 근거를 보태지만 이 표의 판정 기준(Berlin)에는 들어가지 않는다 — 문항 해설의 「> 400 pg/mL」 문턱은 원문 미대조."
  - id: ards-severity-actions
    title: "Berlin 중증도와 더하는 처치"
    role: severity
    span: column
    section: 치료
    columns: ["중증도(PEEP ≥ 5)", "PaO2/FiO2", "모두에게", "더하는 것"]
    rows:
      - ["경증", "200 < … ≤ 300", "6 mL/kg PBW, Pplat ≤ 30, PEEP, 보수적 체액", "—"]
      - ["중등증", "100 < … ≤ 200", "위와 같음", "PaO2/FiO2 < 150 이면 복와위 [[harrison-21: 301장 p.2228]]"]
      - ["중증", "≤ 100", "위와 같음", "복와위, 동조 불량이면 신경근차단, 반응 없으면 ECMO 센터 [[harrison-21: 301장 p.2228]]"]
    note: "등급 경계는 해리슨 표 301-2(p.2226). 복와위 문턱(< 150)은 등급 경계(200·100)와 다르다."
pitfalls:
  - contrast: "이뇨+PEEP 감량 vs 폐보호 환기 — 「양측 음영 + 저산소 = 폐부종 = 이뇨」"
    point: "양측 폐 음영과 수포음은 ARDS 와 심인성 부종에 모두 있고 흉부 사진으로는 가려지지 않는 일이 많다 [[harrison-21: 301장 p.2226]]. 가르는 것은 심장 쪽 근거다 — 경정맥 팽대·말초 부종이 없고 심초음파 좌심실 기능이 정상이면 부종은 정수압성이 아니라 투과성이다. 이때 PEEP 를 낮추면 허탈된 폐포가 더 닫혀 단락이 커진다(PEEP 는 허탈을 막는 처치다 [[harrison-21: 301장 p.2228]]). 진단이 ARDS 로 서면 첫 결정은 환기 설정 — 6 mL/kg PBW·Pplat ≤ 30 이다."
    exception: "경정맥 팽대·확장되고 수축이 떨어진 좌심실·심비대와 흉수가 있으면 심인성 부종이고 이뇨제가 앞선다 [[?acc-aha-hf-2022]]. 또 ARDS 로 확진된 뒤에도 저혈압이 없으면 보수적 체액·이뇨는 권고되는 보조다 [[harrison-21: 301장 p.2228]] — 틀린 것은 「이뇨」 자체가 아니라 「PEEP 감량」과 「환기보다 먼저」라는 순서다."
    covers: ["imaging-2026-0063:A"]
  - contrast: "12 mL/kg vs 6 mL/kg — 「호흡성 산증을 교정」"
    point: "ARDS 폐는 아래쪽이 부종·허탈로 차 있어 통기되는 폐가 작다. 정상 크기의 일회호흡량은 남은 정상 폐포를 과팽창시킨다(volutrauma) [[harrison-21: 301장 p.2228]]. 목표는 혈액가스 정상화가 아니라 폐 손상을 늘리지 않는 것 — 산증은 호흡수(≤ 35)로 보정하고 pH ≥ 7.30 까지 고탄산혈증을 허용한다 [[harrison-21: 301장 p.2229]]."
    exception: "없음 — 12 mL/kg 는 ARDS 에서 정답이 되는 조건이 없다."
  - contrast: "예측체중 vs 실제 체중"
    point: "폐 크기는 키와 성별로 정해지고 체중이 늘어도 커지지 않는다. 그래서 일회호흡량은 예측체중(PBW)으로 계산한다 [[harrison-21: 301장 p.2228]] — 비만 환자에게 실제 체중을 쓰면 과팽창이 된다."
    exception: "PBW 계산식 자체(키·성별)는 이 정리본의 출처로 대조하지 않았다."
  - contrast: "중증 ARDS 의 보조 처치 — 스테로이드·흡입 산화질소"
    point: "스테로이드는 일상 사용 근거가 없고(권고 등급 D), 흡입 산화질소·에포프로스테놀은 산소화를 잠깐 올릴 뿐 생존·환기 기간을 개선하지 못했다 [[harrison-21: 301장 p.2228–2229]]. 중증에서 사망률을 낮춘 것은 복와위다."
    exception: "해리슨 301장은 비-COVID ARDS 를 다룬다. COVID-19 ARDS 의 스테로이드는 199장이 다룬다(이 정리본에서 읽지 않음)."
diagram:
  title: "양측 폐 음영 + 급성 저산소혈증 — ARDS 인가, 첫 처치는?"
  nodes:
    - {id: start, kind: start, text: "급성 저산소성 호흡부전, 흉부 사진 양측 음영 — 산소·필요하면 삽관"}
    - {id: cardiac, kind: decision, text: "정수압성(심장) 부종으로 충분히 설명되는가? 경정맥 팽대·말초 부종·심초음파 좌심실 기능"}
    - {id: info, kind: info, text: "심초음파·혈역학 평가가 아직 없다 — 유발 요인이 없으면 객관적 평가로 심장 원인을 배제해야 한다"}
    - {id: hf, kind: end, text: "심인성 폐부종 — 이뇨제·혈관확장제, 원인 심질환 치료"}
    - {id: pf, kind: decision, text: "PEEP ≥ 5 에서 PaO2/FiO2 는? (1주 안 발병, 흉수·허탈·결절로 설명 안 되는 양측 음영)"}
    - {id: other, kind: alert, text: "> 300 — ARDS 기준 밖: 폐렴·폐포 출혈 등 다른 원인을 찾는다"}
    - {id: lpv, kind: step, text: "ARDS — 6 mL/kg 예측체중, 고평부압 ≤ 30, PEEP/FiO2 조정, 고탄산혈증 허용"}
    - {id: sev, kind: decision, text: "PaO2/FiO2 < 150 인가?"}
    - {id: prone, kind: end, text: "복와위 환기(± 동조 불량 시 신경근차단, 반응 없으면 ECMO 센터)"}
    - {id: keep, kind: end, text: "폐보호 환기 유지 + 저혈압 없으면 보수적 체액·이뇨, 원인(폐렴·패혈증) 치료"}
  edges:
    - {from: start, to: cardiac}
    - {from: cardiac, to: hf, label: "예 — 심장 근거 있음"}
    - {from: cardiac, to: pf, label: "아니오 — 심장 근거 없음"}
    - {from: cardiac, to: info, label: "평가 전"}
    - {from: info, to: hf, label: "좌심실 기능 저하·울혈"}
    - {from: info, to: pf, label: "심장 원인 배제"}
    - {from: pf, to: other, label: "> 300"}
    - {from: pf, to: lpv, label: "≤ 300"}
    - {from: lpv, to: sev}
    - {from: sev, to: prone, label: "예"}
    - {from: sev, to: keep, label: "아니오"}
diagram_notes:
  - "심인성 부종과 ARDS 는 함께 있을 수 있다 — Berlin 은 「정수압성 부종이 주원인이 아님」을 요구하지 「심장병이 없음」을 요구하지 않는다 [[harrison-21: 301장 p.2226]]."
  - "PaO2/FiO2 는 PEEP ≥ 5 cm H2O 에서 잰 값이다. 삽관 전 비재호흡 마스크의 FiO2 는 정확하지 않아 등급 계산에 쓰지 않는다."
  - "PEEP 의 최적 설정법은 합의가 없다(ARDS Network PEEP–FiO2 표, 압력-용적 곡선, 식도압 등) [[harrison-21: 301장 p.2228]] — 시험은 「PEEP 를 낮추지 않는다」까지를 묻는다."
  - "체액 제한·이뇨는 폐보호 환기와 경쟁하는 선택이 아니라 그 뒤의 보조이며, 저혈압·저관류가 한계다 [[harrison-21: 301장 p.2228]]."
checks:
  - q: "Berlin 기준의 네 요소는?"
    a: "1주 안 발병, 흉수·허탈·결절로 설명되지 않는 양측 음영, 정수압성 부종이 주원인이 아님(필요하면 심초음파로 배제), PEEP ≥ 5 에서 PaO2/FiO2 ≤ 300(경증 200–300, 중등증 100–200, 중증 ≤ 100)."
  - q: "PEEP 10 에서 FiO2 0.8 로 PaO2 68 mm Hg 이다. 중증도는?"
    a: "PaO2/FiO2 = 85 → 중증(≤ 100)."
  - q: "폐보호 환기의 두 숫자와 근거 시험의 결과는?"
    a: "일회호흡량 6 mL/kg 예측체중, 고평부압 ≤ 30 cm H2O. ARDS Network 시험에서 12 mL/kg 대비 사망 40 % → 31 %."
  - q: "왜 예측체중으로 계산하는가?"
    a: "폐 크기는 키·성별로 정해지고 체중이 늘어도 커지지 않기 때문이다."
  - q: "사망률을 낮춘 중증 ARDS 의 추가 처치와 그 문턱은?"
    a: "복와위 환기, PaO2/FiO2 < 150(28일 사망 32.8 % → 16.0 %)."
  - q: "ARDS 에서 이뇨제는 금기인가?"
    a: "아니다. 저혈압·저관류가 없으면 좌심방압을 낮게 유지하는 보수적 체액·이뇨가 권고된다. 다만 첫 처치(환기 설정)를 대신하지 않고, PEEP 를 낮추는 것은 틀리다."
variants:
  - id: v1
    of: imaging-2026-0063
    flip: true
    changed: "「경정맥 팽대 없음·BNP 낮음·심초음파 좌심실 기능 정상·발열성 호흡기 감염 선행」을 「경정맥 팽대·양측 다리 오목부종·S3·심초음파 좌심실 확장과 박출률 20 %·흉부 사진 심비대와 양측 흉수」로 바꿈 → 부종이 정수압성이라 답이 「폐보호 환기」에서 「정맥 고리 이뇨제+혈관확장제」로 바뀜"
    context: "Changed cue — hydrostatic (cardiogenic) edema instead of ARDS"
    stem: "A 63-year-old man comes to the emergency department because of 2 days of progressive shortness of breath; he now has to sleep sitting up. He had an anterior myocardial infarction 3 years ago. He has not had fever or cough. His pulse is 112/min, respirations are 30/min, and blood pressure is 164/98 mm Hg. Oxygen saturation is 86% on room air and 93% on a nonrebreather mask. Jugular venous pressure is elevated, an S3 gallop is heard, crackles are present over both lung fields, and there is pitting edema of both legs. A chest radiograph shows an enlarged cardiac silhouette, bilateral perihilar opacities, and small bilateral pleural effusions. Bedside echocardiography shows a dilated left ventricle with an ejection fraction of 20%. Which of the following is the most appropriate next step in management?"
    choices: ["A. Intravenous loop diuretic with a vasodilator", "B. Intubation with a tidal volume of 12 mL/kg predicted body weight", "C. Prone positioning", "D. Intravenous glucocorticoids", "E. Inhaled nitric oxide"]
    answer: "A"
    explanation: "Bilateral opacities with hypoxemia are not specific: here elevated jugular venous pressure, an S3, leg edema, cardiomegaly with effusions and a dilated, poorly contracting left ventricle explain the edema by hydrostatic pressure, so the Berlin requirement that hydrostatic edema is not the primary cause is not met and this is not ARDS [[harrison-21: 301장 p.2226]]. Decongestion with an intravenous loop diuretic and a vasodilator treats the cause [[?acc-aha-hf-2022]]. In the original item the same radiographic pattern came with a normal ventricle, no venous distention and a preceding febrile illness — that is what made lung-protective ventilation the answer. Prone positioning is for severe ARDS, 12 mL/kg is never lung-protective, and glucocorticoids and inhaled nitric oxide do not treat hydrostatic edema."
    kind: application
  - id: v2
    of: imaging-2026-0063
    flip: false
    changed: "성별·나이(58세 여자)·유발 사건(약물 과다 복용 뒤 위 내용물 흡인)·제시 순서·수치를 바꾸고 「1주 안 발병·양측 음영·PEEP ≥ 5 에서 PaO2/FiO2 ≤ 100·심장 원인 배제」는 그대로 → 답은 여전히 6 mL/kg PBW·고평부압 ≤ 30"
    context: "Same decisive cues, different story — aspiration-related ARDS"
    stem: "A 58-year-old woman is found unresponsive at home next to empty pill bottles, with vomitus around her mouth. She is intubated in the emergency department and admitted to the intensive care unit. Over the next 24 hours her oxygenation worsens. A chest radiograph shows new bilateral airspace opacities without cardiomegaly or pleural effusion. Transthoracic echocardiography shows normal left ventricular size and function, and there is no jugular venous distention. She is 165 cm tall and weighs 92 kg. On a positive end-expiratory pressure of 12 cm H2O and an FiO2 of 0.9, arterial PaO2 is 72 mm Hg and PaCO2 is 52 mm Hg. Which of the following ventilator strategies is most appropriate now?"
    choices: ["A. Tidal volume based on her actual weight of 92 kg to lower the PaCO2", "B. Reduce PEEP to 5 cm H2O and give intravenous furosemide", "C. Tidal volume of 6 mL/kg predicted body weight with plateau pressure 30 cm H2O or less", "D. Increase tidal volume to 10 mL/kg predicted body weight until the pH is normal", "E. High-frequency oscillatory ventilation"]
    answer: "C"
    explanation: "Aspiration of gastric contents is a direct cause of ARDS [[harrison-21: 301장 p.2225]]. Onset within a week, new bilateral opacities, a normal ventricle without venous distention, and a PaO2/FiO2 of 80 (72/0.9) on PEEP 12 meet the Berlin definition of severe ARDS [[harrison-21: 301장 p.2226]]. The story changed, but the decisive cues did not, so the answer is still lung-protective ventilation: 6 mL/kg of predicted (not actual) body weight with plateau pressure ≤ 30 cm H2O; the modest hypercapnia is tolerated [[harrison-21: 301장 p.2228–2229]]. Lowering PEEP de-recruits alveoli, and high-frequency oscillation has not been shown to help [[harrison-21: 301장 p.2228]]."
    kind: application
---

## 정의
급성호흡곤란증후군(ARDS)은 빠르게 시작한 심한 호흡곤란·저산소혈증·미만성 폐 침윤으로 호흡부전에 이르는 임상 증후군이며, 폐렴·패혈증·흡인·외상·다량 수혈 같은 직접·간접 손상이 원인이다 [[harrison-21: 301장 p.2225]]. 이 정리본의 목표는 원인 나열이 아니라, **양측 폐 음영과 저산소혈증을 보았을 때 심장 원인을 배제해 ARDS 와 중증도를 판단하고, 첫 처치로 폐보호 환기를 고르며 이뇨·PEEP·복와위의 자리를 가르는 것**이다.

## 병태생리
정상 폐포는 얇은 제1형 폐포세포와 모세혈관 내피가 단단한 장벽을 이루어 혈장 단백과 물이 폐포로 새지 않는다. 제2형 폐포세포가 만드는 표면활성제는 폐포가 숨을 내쉴 때 닫히지 않게 한다.

ARDS 의 삼출기(첫 7일)에는 이 내피와 제1형 세포가 손상돼 장벽이 무너지고, **단백이 많은 부종액**이 간질과 폐포를 채운다. 염증성 사이토카인이 호중구를 끌어들이고, 단백·세포 잔해·기능을 잃은 표면활성제가 유리막을 만든다 [[harrison-21: 301장 p.2226]]. 부종은 중력 방향의 **아래쪽(의존 부위) 폐**에 몰리고 그 부분이 허탈되어 폐 유순도가 떨어진다. 피가 통기되지 않는 폐포를 지나므로 **단락**이 생겨 산소를 올려도 PaO2 가 잘 오르지 않고, 미세혈관 폐쇄로 사강이 늘어 고탄산혈증도 생긴다 [[harrison-21: 301장 p.2226]].

처치를 정하는 것은 이 불균일성이다. CT 에서 보듯 손상은 아래쪽에 몰리고 위쪽은 비교적 남아 있어 **통기되는 폐가 작다**. 이 작은 폐에 정상 크기의 일회호흡량을 넣으면 남은 폐포가 과팽창하고(volutrauma), 허탈된 폐포는 호흡마다 열리고 닫히며 다친다(atelectrauma) [[harrison-21: 301장 p.2228]]. 인공호흡기는 생명을 구하지만 설정이 틀리면 손상을 키운다.

## 기전에서 소견으로
- **발병 시기**: 유발 사건 뒤 대개 12–36시간, 늦으면 5–7일에 호흡곤란이 시작된다 — 그래서 Berlin 은 「1주 안」을 요구한다 [[harrison-21: 301장 p.2226]].
- **빠른 호흡·저산소혈증**: 유순도 저하로 호흡일이 늘고, 단락 때문에 FiO2 를 올려도 SpO2 가 덜 오른다(문항: 비재호흡 마스크에서 90 %).
- **흉부 사진**: 폐부종에 맞는 양측 음영, 흔히 폐야의 3/4 이상. 심인성 부종과 구별되지 않을 수 있으나 심비대·흉수·혈관 재분포는 없을 수 있다 [[harrison-21: 301장 p.2226]].
- **PaO2/FiO2**: 산소화 장애의 크기. PEEP 가 허탈된 폐포를 열어 값을 바꾸므로 PEEP ≥ 5 에서 잰 값으로 등급을 매긴다.
- **심장 평가(정상이 의미 있는 음성)**: 경정맥 팽대·말초 부종이 없고 심초음파 좌심실 기능이 정상이면 정수압성 부종이 주원인이 아니다. 유발 요인이 없을 때는 이 객관적 평가가 필수다 [[harrison-21: 301장 p.2226]].

## 감별
흔한 감별은 **심인성 폐부종·양측 폐렴·폐포 출혈**이고, 드물게 급성 간질성 폐렴·과민성 폐렴·방사선 폐렴·신경성 폐부종이 있다 [[harrison-21: 301장 p.2226]]. 저산소혈증이 심한데 폐가 깨끗하면 폐색전증, 한쪽 호흡음 소실·과투과성이면 기흉을 먼저 생각한다 — 둘 다 「양측 실질 음영」과 맞지 않는다.

## 검사
1. **동맥혈가스(PEEP ≥ 5 에서)** — PaO2/FiO2 로 중증도: 경증 200–300, 중등증 100–200, 중증 ≤ 100 [[harrison-21: 301장 p.2226]].
2. **흉부 사진·CT** — 양측 음영이 흉수·허탈·결절로 설명되지 않음을 확인. CT 는 의존 부위 위주의 불균일한 침범을 보여 준다.
3. **심초음파·혈역학 평가** — 정수압성 부종 배제. 유발 요인이 없으면 반드시 [[harrison-21: 301장 p.2226]].
4. **원인 검사** — 폐렴 병원체·패혈증 원인. 검사 수치는 대개 비특이적이고 원인 질환을 반영한다.

## 치료
1. **폐보호 환기(첫 결정)** — 일회호흡량 6 mL/kg 예측체중, 고평부압 ≤ 30 cm H2O. 12 mL/kg 와 비교해 사망 40 % → 31 % [[harrison-21: 301장 p.2228]]. 산증은 호흡수(≤ 35)로 보정하고 pH ≥ 7.30 까지 고탄산혈증을 허용한다 [[harrison-21: 301장 p.2229]].
2. **PEEP·FiO2** — 허탈을 막아 FiO2 를 낮추면서 산소화(SpO2 88–95 %)를 얻는다. 최적 설정법은 합의가 없다 [[harrison-21: 301장 p.2228–2229]].
3. **복와위** — PaO2/FiO2 < 150 이면 28일 사망 32.8 % → 16.0 % [[harrison-21: 301장 p.2228]].
4. **보수적 체액·이뇨** — 저혈압·저관류가 없으면 좌심방압을 낮게 유지해 폐부종을 줄인다(등급 B) [[harrison-21: 301장 p.2228–2229]].
5. **선택적 처치** — 동조 불량이면 48시간 신경근차단, 표준 치료에 반응 없는 중증은 ECMO 구조 치료. 재개방 수기(고PEEP 와 함께면 사망 증가 보고)·고빈도 환기·스테로이드 일상 사용·흡입 혈관확장제는 이득이 입증되지 않았다 [[harrison-21: 301장 p.2228–2229]].
6. **반응 확인·재평가** — 고평부압을 매번 재고(> 30 이면 일회호흡량을 더 낮춤), PaO2/FiO2 가 150 아래로 머물면 복와위, 원인(폐렴·패혈증)의 치료 반응을 본다. 사망은 대부분 패혈증·다장기부전 같은 폐 밖 원인이라 일반 중환자 관리가 예후를 좌우한다 [[harrison-21: 301장 p.2229]].

## 권고와 예외
- 「양측 음영 + 저산소혈증」은 곧 심부전이 아니다 — 경정맥·부종·심초음파로 정수압성 부종을 먼저 가른다.
- ARDS 의 첫 처치는 6 mL/kg PBW·Pplat ≤ 30. PaCO2 를 맞추려고 일회호흡량을 늘리지 않는다.
- PEEP 는 낮추지 않는다. 이뇨는 금기가 아니라 저혈압이 없을 때의 보조다.
- 중증(PaO2/FiO2 < 150)은 복와위를 더한다.
- 해리슨 301장은 비-COVID ARDS 를 다룬다. COVID-19 ARDS(199장)는 읽지 않았다.

## 시험 쟁점 — 충돌·맥락·새 근거
- **Z1 충돌 · ARDS 에서 이뇨제는 틀린 답인가** — 시험 기준: 심장 원인이 배제된 ARDS 의 **첫** 처치는 폐보호 환기이고, 「이뇨+PEEP 감량」은 오답이다(PEEP 감량이 허탈을 키운다) [[harrison-21: 301장 p.2228]] / 다른 기준: 해리슨은 저혈압·저관류가 없으면 수액 제한·이뇨로 좌심방압을 낮추는 것을 ARDS 관리의 중요한 부분(등급 B)으로 권한다 [[harrison-21: 301장 p.2228–2229]] — 문항 해설의 「이뇨는 혈관 내 용적만 줄인다」는 이보다 강한 표현이다 / 왜 다른가: 문항은 「다음 처치 하나」를, 해리슨은 전체 관리 묶음을 말한다 / 시험에서는: KMLE·USMLE 모두 「첫 처치」를 물으면 폐보호 환기, 「체액 전략」을 물으면 보수적 체액(저혈압 없을 때)을 고른다.
- **Z2 새 근거 · ARDS 의 정의** — 시험 기준: Berlin(PEEP ≥ 5 에서 PaO2/FiO2) [[harrison-21: 301장 p.2226]] / 다른 기준: 2023–2024 「새 전 세계 정의」는 비삽관 고유량 산소 환자와 SpO2/FiO2 도 포함한다고 알려져 있으나 원문 미대조 [[?global-ards-2024]] / 왜 다른가: 해리슨 21판(2022) 이후 개정 / 시험에서는: KMLE·USMLE 모두 당분간 Berlin 네 요소와 100·200·300 경계를 묻는다.
- **Z3 맥락 · COVID-19 ARDS** — 시험 기준: 해리슨 301장은 비-COVID ARDS 를 다루며 스테로이드 일상 사용을 권하지 않는다(등급 D) [[harrison-21: 301장 p.2228–2229]] / 다른 기준: COVID-19 ARDS 의 권고는 해리슨 199장에 따로 있다(읽지 않음 [[?harrison-21: 199장]]) / 왜 다른가: 원인 질환별 치료가 다르다 / 시험에서는: 문항에 COVID-19 가 명시되지 않으면 일반 ARDS 원칙(폐보호 환기)으로 푼다.

## (심화) 왜 「혈액가스를 맞추는 환기」에서 「폐를 지키는 환기」로 바뀌었나
2000년 이전에는 인공호흡의 목표가 PaCO2·pH 를 정상으로 되돌리는 것이었고, 10–15 mL/kg 의 일회호흡량이 흔했다. 그러나 ARDS 폐의 CT 는 손상이 아래쪽에 몰리고 위쪽의 정상 폐는 작다는 것을 보여 주었고, 동물 실험은 큰 일회호흡량 자체가 폐를 다치게 한다는 것을 보여 주었다. ARDS Network 시험은 6 mL/kg·고평부압 ≤ 30 이 12 mL/kg 보다 사망률을 낮춘다는 것을 증명했다 [[harrison-21: 301장 p.2228]]. 이후 대부분의 약물 시험(스테로이드·표면활성제·혈관확장제)은 실패했고, 사망률을 바꾼 것은 여전히 「폐를 덜 다치게 하는」 처치 — 저일회호흡량과 중증에서의 복와위 — 였다. 남은 논쟁은 PEEP 를 어떻게 정할지이며, 해리슨은 합의가 없다고 적는다 [[harrison-21: 301장 p.2228]].
