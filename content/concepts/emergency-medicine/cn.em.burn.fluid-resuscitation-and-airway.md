---
id: cn.em.burn.fluid-resuscitation-and-airway
type: concept
topic: Emergency Medicine
see_also: [General Surgery, Pulmonology]
date: 2026-11-20
updated: 2026-11-20
version: 1
outline: em.burn   # 기본틀 슬롯(content/outline/subjects.yaml) — 응급의학과 손 슬롯 「화상과 흡입손상」
confidence: medium
review_status: unreviewed
note_form: 2            # 판형 2(2026-09-25) — 기본틀 빈 슬롯으로 쓴 정리본(오답 연결 없음)
title: "화상 — 2도 이상만 세어 수액, 소변으로 조절"
objective: "화상 환자의 깊이와 2도 이상 화상의 체표면적(9의 법칙), 상기도 흡입손상 징후로 초기 수액량·소변량 목표와 조기 기관삽관 여부를 정한다"
objective_kind: 다음 처치
condition: 중증 화상(major burn)의 초기 소생 — 화상 쇼크 수액 소생(burn shock resuscitation)과 흡입손상(inhalation injury)
exams: [kmle, usmle]
summary:
  - "결론: 2도 이상 %TBSA 로 첫 24시간 젖산 링거량을 정하고(Parkland 4 mL/kg/%), 소변량으로 속도를 조절한다."
  - "시험 단서: 밀폐 공간 화재, 쉰 목소리·그렁거림·입안 물집, 얼굴 깊은 화상(inhalation injury) → 조기 기관삽관."
  - "왜: 화상 부위 모세혈관 누출로 혈관 내 용적이 빠지고, 상기도 부종은 소생 수액과 함께 첫 48시간 동안 커진다."
  - "1도 화상은 TBSA 에 넣지 않는다 — 공식은 시작 속도일 뿐이고, 절반은 「화상 시각」부터 8시간 안에 준다."
  - "성인 소변 목표는 약 0.5 mL/kg/h(30–50 mL/h) — 넘치게 주는 것(fluid creep)이 흔한 오류다."
pitfalls:
  - contrast: "1도(표피) 화상도 TBSA 에 더한다?"
    point: "화상 넓이는 1도 화상을 빼고 2도·3도 화상만 센다 [[giretzlehner-tbsa-2021: 1. Introduction]]. Parkland 공식의 %TBSA 도 2도·3도 화상 넓이다 [[dries-burn-2017: Resuscitation]]."
  - contrast: "공식의 첫 절반 — 병원 도착부터 8시간?"
    point: "첫 절반은 「화상을 입은 시각」부터 8시간, 나머지 절반은 이후 16시간에 준다. 늦게 도착하면 첫 8시간 몫을 더 짧은 시간에 넣어야 한다 [[dries-burn-2017: Resuscitation]]."
  - contrast: "공식으로 낸 양을 24시간 고정 주입?"
    point: "공식은 시작 속도를 정할 뿐이고, 곧바로 소변량 목표에 맞춰 시간마다 속도를 조절한다 [[jeschke-burn-2020: Secondary survey — fluid infusion rate]] [[dries-burn-2017: Resuscitation]]."
  - contrast: "얼굴 화상·입안 그을음만 있어도 바로 삽관?"
    point: "밀폐 공간 노출·얼굴 화상·입안 그을음은 그 자체로 흡입손상이 아니다 — 뒤 인두(부종·점막 탈락)와 성대 그을음을 진찰해 판단한다 [[jeschke-burn-2020: Primary survey]]. 불필요한 삽관은 인공호흡기 폐렴·성대 손상을 늘린다 [[jeschke-burn-2020: Diagnosis — smoke inhalation screening]] [[concannon-intubation-2023: Introduction]]."
  - contrast: "산소포화도·첫 흉부 X선 정상 = 흡입손상 배제?"
    point: "폐 염증 반응은 시간이 걸려 첫 산소화·흉부 X선이 정상이어도 배제하지 못한다 [[jeschke-burn-2020: Secondary survey]] [[tanizaki-inhalation-2015: Diagnosis]]. 부종이 없어도 첫 24시간(특히 8시간)은 낮은 문턱으로 지켜본다 [[tanizaki-inhalation-2015: Intubation]]."
  - contrast: "도착 시 카복시헤모글로빈 정상 = CO 중독 아님?"
    point: "현장 산소로 이미 떨어졌을 수 있어 도착 시 정상일 수 있다. 100 % 산소로 반감기가 약 4시간에서 약 45분으로 줄고, 카복시헤모글로빈 <5 %를 확인할 때까지 산소를 계속한다 [[jeschke-burn-2020: Box 2 Inhalation injury]]."
  - contrast: "화재 환자의 시안화물 의심 — 아질산염 해독제 키트?"
    point: "아질산염은 메트헤모글로빈을 만들어 CO 중독이 함께 있으면 저산소를 악화시킨다 — 화재 흡입에서는 하이드록소코발라민(70 mg/kg 정맥)이 1차 약이다 [[tanizaki-inhalation-2015: Cyanide poisoning]]."
tables:
  - id: depth
    section: "가르는 소견 — 깊이와 넓이"
    title: "화상 깊이 — TBSA 에 넣는가"
    role: differential
    span: column
    columns: ["깊이", "모습·통증", "치유", "TBSA"]
    rows:
      - ["1도(표재성, 표피만)", "붉고 아프다, 통증은 오래가지 않음", "약 1주 안에 저절로", "넣지 않음"]
      - ["표재성 부분층(2도 얕은)", "물집, 진물, 분홍 바탕이 눌렀다 다시 붉어짐, 매우 아픔", "약 2주, 수술 불필요", "넣음"]
      - ["심부 부분층(2도 깊은)", "창백·건조, 통증 감소(통각 수용체 일부 파괴), 털이 쉽게 빠짐", "3주 이상, 수술·흉터", "넣음"]
      - ["전층(3도)", "희고 가죽처럼 단단·건조, 아프지 않음", "가장자리에서만, 대개 수술", "넣음"]
    note: "깊이·치유 기준은 jeschke-burn-2020(Introduction)과 giretzlehner-tbsa-2021(1. Introduction). 침상 깊이 판정은 부정확하다고 두 출처 모두 적는다."
  - id: nines
    section: "가르는 소견 — 깊이와 넓이"
    title: "9의 법칙(성인) · 손바닥 법칙"
    role: criteria
    span: column
    columns: ["부위", "%TBSA"]
    rows:
      - ["머리·얼굴", "9"]
      - ["팔(한쪽)", "9"]
      - ["다리(한쪽)", "18"]
      - ["몸통 앞 · 몸통 뒤", "각 18"]
      - ["생식기 부위", "1"]
      - ["환자 손바닥(손가락 포함)", "약 1 — 작은·흩어진 화상"]
    note: "Wallace 1951 의 비율을 giretzlehner-tbsa-2021(3.3.1)에서 옮김 — 그 논문은 목 1 %도 따로 적는다. 소아는 Lund-Browder 도표를 쓴다 [[jeschke-burn-2020: Primary survey]]. 9의 법칙·손바닥 법칙 모두 넓이를 과대평가하기 쉽다 [[giretzlehner-tbsa-2021: 3.3.2]] [[giretzlehner-tbsa-2021: 3.4.2]]."
  - id: fluid
    section: "선택 — 수액량과 조절 지표"
    title: "초기 수액 — 시작량과 조절"
    role: treatment
    span: column
    columns: ["항목", "기준"]
    rows:
      - ["누가", "성인 2도 이상 >20 %TBSA 는 대개 정맥 수액 소생이 필요. 더 작아도 전기 손상·흡입손상·동반 외상이면 필요할 수 있음 [[jeschke-burn-2020: Management — fluid resuscitation]]"]
      - ["무엇을", "데운 젖산 링거(균형 결정질) [[jeschke-burn-2020: Management — fluid resuscitation]]"]
      - ["얼마나(시험 계산)", "Parkland: 4 mL × 체중(kg) × %TBSA(2·3도) = 첫 24시간 젖산 링거 — 절반은 화상 시각부터 8시간, 나머지는 16시간 [[dries-burn-2017: Resuscitation]]"]
      - ["시작량 범위", "미국화상학회 지침 2–4 mL/kg/%TBSA [[jeschke-burn-2020: Secondary survey — fluid infusion rate]]. 2024 지침은 2 mL/kg/% 로 시작을 권고 [[cartotto-aba-2024: Abstract]]"]
      - ["조절 지표", "소변량 — 성인(>30 kg) 0.5 mL/kg/h(약 30–50 mL/h), 30 kg 미만 소아 1 mL/kg/h [[giretzlehner-tbsa-2021: 2.1 Over-Resuscitation]]"]
      - ["넘칠 때", "결정질만 대량이면 과다 소생 — 알부민·혈장 「콜로이드 구조」를 고려 [[jeschke-burn-2020: Colloids: albumin or plasma]] [[cartotto-aba-2024: Abstract]]"]
    note: "Parkland·지침 범위·소변 목표가 출처마다 다른 점은 「시험 쟁점」 Z1·Z2."
criteria:
  - id: intubation-signs
    name: 화상 환자 조기 기관삽관을 고려할 징후
    kind: 처치 적응
    population: "화상·연기 흡입 환자"
    statement: "다음 중 하나라도 있으면 삽관을 고려한다 — 호흡곤란, 그렁거림(stridor), 저환기, 보조호흡근 사용, 입인두 물집·부종, 얼굴·목 깊은 화상. 상기도 부종·충혈이 보이면 즉시 삽관한다 [[tanizaki-inhalation-2015: Intubation]]"
    exceptions: "징후가 없어도 첫 24시간(특히 8시간)은 가까이 관찰하며 낮은 문턱을 유지한다 [[tanizaki-inhalation-2015: Intubation]]. 미국화상학회 기준은 민감도 77 %·특이도 46 %로 과다 삽관 우려가 있다 [[concannon-intubation-2023: Discussion]]"
    source: tanizaki-inhalation-2015
    basis: current
    exams: [kmle, usmle]
sources:
  - id: jeschke-burn-2020
    org: "Jeschke MG, van Baar ME, Choudhry MA, Chung KK, Gibran NS, Logsetty S"
    title: "Burn injury"
    kind: review
    year: 2020
    citation: "Nat Rev Dis Primers 2020;6(1):11"
    doi: "10.1038/s41572-020-0145-5"
    pmid: "32054846"
    url: "https://pmc.ncbi.nlm.nih.gov/articles/PMC7224101/"
    checked_at: 2026-11-20
    checked: "PMC7224101 전문(PubMed MCP)에서 Introduction(깊이 분류·주요 화상 기준), Box 2 Inhalation injury(세 유형·CO 반감기 4시간→약 45분·COHb <5 %까지 산소·도착 시 COHb 정상 가능·시안화물은 설명 안 되는 산증), Primary survey(ABCDE 순서·보온·성인 9의 법칙/소아 Lund-Browder·밀폐 공간·얼굴 화상·입안 그을음은 그 자체로 흡입손상 아님·뒤 인두와 성대 진찰·그렁거림·쉰 목소리·탄소 가래), Secondary survey(≥15 % 검사·산소화와 흉부 X선 정상이 배제 아님·ABA 지침 2–4 mL/kg/%·공식은 시작 속도·소변 목표 0.3–0.5 mL/kg/h·Rule of Tens), Management(>20 %TBSA 수액·데운 젖산 링거·콜로이드 구조·과다 소생의 구획증후군), 흡입손상 선별 도구 문단(불필요한 삽관 합병증)을 읽음. 9의 법칙 수치는 그림에만 있어 이 논문에서 옮기지 않음"
    verified: text
  - id: dries-burn-2017
    org: "Dries DJ, Marini JJ"
    title: "Management of Critical Burn Injuries: Recent Developments"
    kind: review
    year: 2017
    citation: "Korean J Crit Care Med 2017;32(1):9-21"
    doi: "10.4266/kjccm.2016.00969"
    pmid: "31723611"
    url: "https://pmc.ncbi.nlm.nih.gov/articles/PMC6786736/"
    checked_at: 2026-11-20
    checked: "PMC6786736 전문 중 Resuscitation · Pulmonary Issues · Conclusions 절을 읽음 — Parkland(Consensus) 공식 = 4 mL/kg/%TBSA 젖산 링거·첫 24시간·%TBSA 는 2도·3도 넓이·화상 시각부터 첫 8시간에 절반·이후 16시간에 절반, Parkland 센터 경험(적정 소생 = 소변 0.5–1.0 mL/kg/h, 48 %가 과다 소생), 공식은 초기 지침일 뿐 소변량으로 조절, <20 %TBSA 는 경구 소생 후보, 「쉽게 과다 소생된다 — 관류가 충분하면 줄인다」"
    verified: text
  - id: giretzlehner-tbsa-2021
    org: "Giretzlehner M, Ganitzer I, Haller H"
    title: "Technical and Medical Aspects of Burn Size Assessment and Documentation"
    kind: review
    year: 2021
    citation: "Medicina (Kaunas) 2021;57(3):242"
    doi: "10.3390/medicina57030242"
    pmid: "33807630"
    url: "https://pmc.ncbi.nlm.nih.gov/articles/PMC7999209/"
    checked_at: 2026-11-20
    checked: "PMC7999209 전문을 읽음 — 1. Introduction(1도·2a·2b·3도 모습과 치유 기간, 화상 넓이에서 1도 제외), 2.1 Over-Resuscitation(1979 NIH 회의: 첫 24시간 등장성 결정질 2–4 mL/kg/%·소변 30–50 mL/h, 소아 <30 kg 1 mL/kg/h·>30 kg 0.5 mL/kg/h, 과대평가가 과다 소생으로), 3.3 Rule of Nines(Wallace 1951: 팔 각 9·다리 각 18·몸통 앞·뒤 각 18·머리·얼굴 9·목 1·생식기 1, 과대평가 경향), 3.4 Rule of Palms(손바닥 약 1 %·실제는 더 작아 과대평가)"
    verified: text
  - id: tanizaki-inhalation-2015
    org: "Tanizaki S"
    title: "Assessing inhalation injury in the emergency room"
    kind: review
    year: 2015
    citation: "Open Access Emerg Med 2015;7:31-37"
    doi: "10.2147/OAEM.S74580"
    pmid: "27147888"
    url: "https://pmc.ncbi.nlm.nih.gov/articles/PMC4806805/"
    checked_at: 2026-11-20
    checked: "PMC4806805 전문을 읽음 — 세 유형(상기도 열손상·하기도 화학손상·CO/시안화물 대사 질식), 상기도 부종은 소생 후기에 생기고 첫 평가가 부종 정도를 잘 예측하지 못함, 삽관 고려 징후 6가지·상기도 부종/충혈이면 즉시 삽관·없어도 24시간(특히 8시간) 관찰, 첫 흉부 X선 대개 정상, 의심 시 100 % 산소, 시안화물 의심이면 해독제·하이드록소코발라민 70 mg/kg 1차·아질산염 키트는 CO 동반 시 금기, 원주형 몸통 전층 화상은 흉부 가피절개"
    verified: text
  - id: concannon-intubation-2023
    org: "Concannon E, Damkat Thomas L, Kerr L, et al."
    title: "Review of Indications for Endotracheal Intubation in Burn Patients with Suspected Inhalational Injury"
    kind: other
    year: 2023
    citation: "Eur Burn J 2023;4(2) — 논문 번호 ebj4020014"
    doi: "10.3390/ebj4020014"
    pmid: "39599924"
    url: "https://pmc.ncbi.nlm.nih.gov/articles/PMC11571857/"
    checked_at: 2026-11-20
    checked: "PMC11571857 전문을 읽음(단일 기관 후향 연구) — 상기도 부종은 첫 48시간에 진행해 조기 삽관을 정당화, 삽관 합병증·인공호흡기 폐렴, ABA 기준(민감도 77 %·특이도 46 %, ISBI 지침에 포함)과 Denver 기준, 기준에 맞춰 삽관해도 기관지경 정상이 많아 과다 삽관 우려, 이송 거리가 삽관 결정에 영향. ABA 기준 항목 표는 PMC 텍스트에 없어 옮기지 않음. 쪽수는 확인하지 않아 DOI 로만 적음"
    verified: text
  - id: cartotto-aba-2024
    org: "American Burn Association (Cartotto R, Johnson LS, Savetamal A, et al.)"
    title: "American Burn Association Clinical Practice Guidelines on Burn Shock Resuscitation"
    kind: guideline
    year: 2024
    citation: "J Burn Care Res 2024;45(3):565-589"
    doi: "10.1093/jbcr/irad125"
    pmid: "38051821"
    checked_at: 2026-11-20
    checked: "PubMed 초록만 읽음(PMC 전문 없음) — 대상 성인 ≥20 %TBSA 첫 48시간, 2 mL/kg/%TBSA 로 시작해 소생량을 줄이도록 권고, 큰 화상에서 알부민 고려, 복강·안압 선택적 감시, 고용량 비타민 C·신선동결혈장·조기 CRRT·승압제는 권고 불가"
    verified: abstract
diagram:
  title: "화상 초기 — 기도 먼저, 넓이로 수액, 소변으로 조절"
  nodes:
    - {id: start, kind: start, text: "화상 — 일차 평가(ABCDE) · 보온"}
    - {id: air, kind: decision, text: "상기도 손상 징후?"}
    - {id: intub, kind: step, text: "조기 기관삽관 · 100 % 산소"}
    - {id: obs, kind: info, text: "뒤 인두·성대 진찰 · 첫 24시간 관찰"}
    - {id: tbsa, kind: decision, text: "2도 이상 화상 >20 %TBSA?"}
    - {id: small, kind: end, text: "경구·유지 수액 — 동반 손상이면 정맥"}
    - {id: fluid, kind: step, text: "젖산 링거 2–4 mL/kg/% · 절반 8시간"}
    - {id: uo, kind: decision, text: "소변 약 0.5 mL/kg/h?"}
    - {id: keep, kind: end, text: "속도 유지 — 매시간 재평가"}
    - {id: up, kind: end, text: "주입 속도 올림"}
    - {id: down, kind: end, text: "주입 속도 줄임 — 과다 소생 피함"}
  edges:
    - {from: start, to: air}
    - {from: air, to: intub, label: "있음"}
    - {from: air, to: obs, label: "얼굴 화상만"}
    - {from: air, to: tbsa, label: "없음"}
    - {from: obs, to: intub, label: "부종·물집"}
    - {from: obs, to: tbsa, label: "정상"}
    - {from: intub, to: tbsa}
    - {from: tbsa, to: fluid, label: "예"}
    - {from: tbsa, to: small, label: "아니오"}
    - {from: fluid, to: uo}
    - {from: uo, to: keep, label: "맞음"}
    - {from: uo, to: up, label: "적음"}
    - {from: uo, to: down, label: "많음"}
diagram_notes:
  - "상기도 손상 징후 = 호흡곤란 · 그렁거림 · 저환기 · 보조호흡근 사용 · 입인두 물집·부종 · 얼굴·목 깊은 화상 [[tanizaki-inhalation-2015: Intubation]]."
  - "%TBSA 는 1도를 빼고 센다. 성인은 9의 법칙, 소아는 Lund-Browder [[giretzlehner-tbsa-2021: 1. Introduction]] [[jeschke-burn-2020: Primary survey]]."
  - "공식의 첫 8시간은 화상 시각부터 센다 [[dries-burn-2017: Resuscitation]]. 공식은 시작 속도만 정한다 [[jeschke-burn-2020: Secondary survey — fluid infusion rate]]."
  - "CO 중독이 의심되면 카복시헤모글로빈 <5 %까지 100 % 산소. 설명되지 않는 젖산 산증이면 시안화물을 의심해 하이드록소코발라민 [[jeschke-burn-2020: Box 2 Inhalation injury]] [[tanizaki-inhalation-2015: Cyanide poisoning]]."
  - "몸통을 둘러싼 전층 화상으로 흉곽이 굳으면 가피절개 [[tanizaki-inhalation-2015: Mechanical ventilation]]."
checks:
  - q: "70 kg 성인, 2도 화상 30 %TBSA(1도 화상 10 %는 별도). Parkland 로 첫 24시간 젖산 링거량과 첫 8시간 몫은?"
    a: "4 × 70 × 30 = 8,400 mL. 1도는 빼므로 30 %만 쓴다. 절반 4,200 mL 를 화상 시각부터 8시간 안에, 나머지를 이후 16시간에 — 그 뒤엔 소변량으로 조절."
  - q: "밀폐된 방 화재, 얼굴 화상·코털 그을림이 있고 목소리가 쉬고 그렁거림이 들린다. 다음 처치는?"
    a: "상기도 부종이 진행하기 전에 조기 기관삽관하고 100 % 산소를 준다."
  - q: "수액 소생 중 성인의 소변량이 2 mL/kg/h 로 계속 나온다. 어떻게 하나?"
    a: "과다 소생 — 주입 속도를 줄인다. 목표는 약 0.5 mL/kg/h(30–50 mL/h)."
figures_none: "판단이 넓이 계산·수액 공식·흡입손상 징후에 달려 있고 사진 소견이 시험 단서가 아니다 — 얼굴 화상 사진은 대표 소견이지만 얼굴이 드러나 싣지 않는다"
---

## 판단 — 왜 기도 다음에 넓이로 수액인가
- 화상도 일차 평가는 ABCDE 순서이고, 넓이 추정은 수액량을 정하므로 일차 평가 안에서 바로 한다. 체온을 잃지 않게 따뜻한 환경에서 본다 [[jeschke-burn-2020: Primary survey]].
- 상기도 부종은 첫 48시간 동안 진행하고 첫 평가가 그 정도를 잘 예측하지 못한다 — 징후가 있으면 부종이 커지기 전에 삽관한다 [[concannon-intubation-2023: Introduction]] [[tanizaki-inhalation-2015: Upper airway]].
- 수액 공식은 **시작 속도**만 정한다. 그 뒤의 정답은 소변량을 보고 속도를 바꾸는 것이다 [[jeschke-burn-2020: Secondary survey — fluid infusion rate]].

## 기전 — 피부 손상에서 쇼크와 기도 부종으로
- 큰 화상 직후 국소·전신 스트레스 반응이 시작되고 [[jeschke-burn-2020: Introduction]], 혈관 내피의 당질층이 떨어져 모세혈관으로 액체가 샌다 — 그래서 수액량을 넓이(%TBSA)로 정한다 [[giretzlehner-tbsa-2021: 2.1 Over-Resuscitation]] [[jeschke-burn-2020: Primary survey]]. 수액을 더 줄수록 누출이 늘어 「수액이 수액을 부른다」 [[giretzlehner-tbsa-2021: 2.1 Over-Resuscitation]].
- 뜨거운 공기는 열용량이 작고 상기도가 열을 식혀 대개 성대 위만 다친다. 그래서 흡입손상의 첫 위협은 혀·후두덮개 부종에 의한 상기도 폐쇄다. 수증기는 덜 식어 아래 기도까지 다칠 수 있다 [[tanizaki-inhalation-2015: Upper airway]] [[jeschke-burn-2020: Box 2 Inhalation injury]].
- 하기도는 연기 속 화학물질이 상피를 다쳐 섬모 청소가 멈추고 섬유소 원주가 기도를 막는다 — 염증이 하루 이틀 뒤에 드러나 첫 X선이 정상이다 [[tanizaki-inhalation-2015: Lower airway]] [[tanizaki-inhalation-2015: Diagnosis]].
- CO 는 산소보다 약 240배 강하게 헤모글로빈에 붙고 해리 곡선을 왼쪽으로 옮겨 조직에 산소가 덜 간다. 시안화물은 산화적 인산화를 막아 젖산 산증을 만든다 [[tanizaki-inhalation-2015: CO and cyanide]].

## 가르는 소견 — 깊이와 넓이
- 깊이는 표로 가르고, 1도는 넓이에서 뺀다. 9의 법칙 비율은 아래 표다.
- **추정의 한계**: 화상 센터 밖의 넓이·깊이 추정은 전문가조차 부정확하고 대개 과대평가한다 — 과대평가는 그대로 과다 소생이 된다 [[jeschke-burn-2020: Primary survey]] [[giretzlehner-tbsa-2021: 2.1 Over-Resuscitation]].

## 선택 — 수액량과 조절 지표
- 표가 누구에게·무엇을·얼마나·무엇으로 조절하는지를 정리한다. 시험 계산은 Parkland 공식으로 한다.
- 과다 소생은 사지·복부·눈 구획증후군을 만든다 [[jeschke-burn-2020: Management — fluid resuscitation]]. 결정질만 대량으로 필요하면 알부민·혈장을 더해 총량을 줄인다 [[jeschke-burn-2020: Colloids: albumin or plasma]].
- 20 % 미만 화상은 위장관이 멀쩡하면 경구 소생 후보다 [[dries-burn-2017: Resuscitation]].

## 권고와 예외
- 전기 손상은 피부 넓이보다 내부 손상이 커서 넓이 공식이 맞지 않는다 — 근육 파괴·미오글로빈뇨를 생각해 더 많은 수액이 필요할 수 있다 [[dries-burn-2017: Electrical and Lightning Injury]].
- 흡입손상으로 인공호흡이 필요하면 다른 ARDS 와 같은 폐 보호 환기를 쓴다 [[dries-burn-2017: Conclusions]].
- 하이드록소코발라민은 용어집에 없는 약 이름이다(원고 한글 유지). 국내 교과서·KMLE 해설의 소변 목표 수치는 대조하지 않았다(검토 항목).

## 시험 쟁점 — 충돌·맥락·새 근거
- **Z1 새 근거 · 시작 수액량 4 mL 대 2 mL** — 시험 기준: Parkland 4 mL/kg/%TBSA, 절반을 첫 8시간 [[dries-burn-2017: Resuscitation]] / 다른 기준: 미국화상학회 지침은 2–4 mL/kg/% 범위를 쓰고 [[jeschke-burn-2020: Secondary survey — fluid infusion rate]], 2024 지침은 2 mL/kg/% 로 시작하도록 권고한다 [[cartotto-aba-2024: Abstract]] / 왜 다른가: 실제 소생량이 Parkland 예측을 자주 넘고(fluid creep) 과다 소생 합병증이 커서 시작량을 낮췄다 [[dries-burn-2017: Resuscitation]] [[jeschke-burn-2020: Management — fluid resuscitation]] / 시험에서는: KMLE 는 국내 교과서·해설과 대조하지 않았다(검토 항목) · USMLE 해설이 2 mL 를 쓰는지도 대조하지 않았다 — 계산 문항은 문항이 지정한 공식을 따르고, 처치 선택 문항은 「시작량 뒤 소변량으로 조절」을 답의 근거로 삼는다. 2024 지침은 초록만 읽었다(†).
- **Z2 맥락 · 성인 소변 목표** — 시험 기준: 성인 0.5 mL/kg/h(약 30–50 mL/h), 30 kg 미만 소아 1 mL/kg/h [[giretzlehner-tbsa-2021: 2.1 Over-Resuscitation]] / 다른 기준: 0.3–0.5 mL/kg/h [[jeschke-burn-2020: Secondary survey — fluid infusion rate]]; Parkland 센터 연구는 0.5–1.0 을 적정, >1.0 을 과다로 정의했다 [[dries-burn-2017: Resuscitation]] / 왜 다른가: 과다 소생을 줄이려고 하한을 낮춘 최근 서술과 옛 센터 정의가 섞여 있다 / 시험에서는: 0.5 mL/kg/h 를 기준으로, 1 mL/kg/h 를 넘게 계속 나오면 속도를 줄이는 쪽으로 답한다.
- **Z3 충돌 · 흡입손상이 의심되면 모두 삽관?** — 시험 기준: 상기도 손상 징후가 있으면 조기 삽관 [[tanizaki-inhalation-2015: Intubation]] / 다른 기준: 기준대로 삽관한 환자의 기관지경이 정상인 경우가 많아 과다 삽관이 우려된다 — ABA 기준 특이도 46 % [[concannon-intubation-2023: Discussion]]; 밀폐 공간·얼굴 화상·그을음만으로는 흡입손상이 아니다 [[jeschke-burn-2020: Primary survey]] / 왜 다른가: 놓치면 기도를 잃고, 과하면 인공호흡기 폐렴이 는다 — 이송 거리가 길수록 문턱이 낮아진다 [[concannon-intubation-2023: Discussion]] / 시험에서는: 쉰 목소리·그렁거림·입인두 부종·호흡곤란 같은 「기도 징후」가 있으면 삽관, 얼굴 화상·그을음만이면 진찰·관찰로 답한다.
