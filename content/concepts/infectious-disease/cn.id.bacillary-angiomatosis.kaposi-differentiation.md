---
id: cn.id.bacillary-angiomatosis.kaposi-differentiation
type: concept
topic: Infectious Disease
see_also: [Microbiology, Dermatology]
date: 2026-09-25
updated: 2026-09-25
version: 1
outline: h172            # 기본틀 슬롯(content/outline/subjects.yaml)
confidence: medium
review_status: unreviewed
note_form: 2            # 판형 2(2026-09-25)
title: "세균성 혈관종증 — 카포시육종과 조직으로 가른다"
objective: "진행성 HIV 환자의 붉은 자주색 결절에서 생검 조직·염색 소견으로 세균성 혈관종증(Bartonella)을 카포시육종·파종 감염과 감별한다"
objective_kind: 감별
condition: 세균성 혈관종증(bacillary angiomatosis) · 세균성 자반증(bacillary peliosis)
exams: [usmle, kmle]
summary:
  - "결론: 호중구 섞인 소엽상 모세혈관 증식 + 은염색 간균 무리 = 세균성 혈관종증(Bartonella), 항생제로 낫는다."
  - "시험 단서: CD4 < 100 + 쉽게 피 나는 붉은 자주색 결절 + 발열 + 고양이 긁힘(cat scratch) 또는 몸니·노숙."
  - "왜: 모양은 카포시육종(Kaposi sarcoma)과 같아도 원인이 세균이라, 조직의 호중구·균이 종양과 가른다."
  - "B. henselae = 고양이·간 자반증(peliosis hepatis), B. quintana = 몸니·노숙·뼈 용해 병변."
  - "치료: 에리트로마이신 또는 독시사이클린 3개월(자반증은 4개월), CD4 > 200 까지 억제 치료."
pitfalls:
  - contrast: "카포시육종(HHV-8) vs 세균성 혈관종증"
    point: "둘 다 붉은 자주색 혈관성 결절이다. 카포시육종은 방추세포 다발·틈새 모양 혈관 공간이고 호중구·세균이 없다. 호중구 + 은염색 간균이면 Bartonella 다."
    cites: ["harrison-21: 172장 p.1332", "robbins-10"]
    covers: ["usmle-2026-0171:A"]
  - contrast: "파종 MAC — 전신 소견이 같으면?"
    point: "CD4 < 50·발열·체중감소·간비대·ALP 상승은 파종 MAC 과 겹쳐 가르지 못한다. MAC 은 항산성 염색에서 보이고 혈관 증식 결절을 만들지 않는다 — 은염색 양성·항산성 음성이면 Bartonella."
    exception: "세균성 혈관종증의 결절형은 진균·마이코박테리아 감염 결절과 닮아 보인다 — 그래서 생검·염색이 필요하다."
    cites: ["harrison-21: 172장 p.1332", "nih-oi"]
    covers: ["usmle-2026-0171:C"]
  - contrast: "이차 매독 — 은염색에서 균이 보이면?"
    point: "매독 나선균도 은염색에 보일 수 있지만, 이차 매독은 손발바닥을 포함한 구리색 구진이고 모세혈관 증식성 결절이 아니다."
    cites: ["nih-oi"]
    covers: ["usmle-2026-0171:B"]
  - contrast: "파종 크립토코쿠스증 — 피부 구진 + 진행성 HIV?"
    point: "크립토코쿠스는 효모(간균이 아니다)이고 배꼽 모양 구진을 만든다. 혈청 크립토코쿠스 항원 음성이면 가능성이 낮다."
    cites: ["nih-oi"]
    covers: ["usmle-2026-0171:E"]
tables:
  - id: ddx
    section: "가르는 소견 — 조직·염색이 가른다"
    title: "진행성 HIV 의 붉은 자주색 피부 결절 감별"
    role: differential
    span: column
    columns: ["질환", "조직·염색", "임상 단서"]
    rows:
      - ["세균성 혈관종증(Bartonella)", "소엽상 소혈관 증식 + 커진 내피세포 + 호중구 우세 침윤, 과립성 덩어리, Warthin-Starry 은염색 간균 무리 [[harrison-21: 172장 p.1332]]", "CD4 < 100, 발열·체중감소, 고양이·몸니 노출 [[harrison-21: 172장 p.1332]]"]
      - ["카포시육종(HHV-8)", "방추세포 다발 + 틈새 모양 혈관 공간 + 적혈구 유출, LANA 면역염색 양성 [[?robbins-10]]", "구강·위장관 침범이 흔하다 [[?nih-oi]]"]
      - ["파종 MAC", "항산성 염색 양성 균 [[?nih-oi]]", "CD4 < 50, 발열·간비대·ALP 상승 — 피부 결절은 드묾 [[?nih-oi]]"]
      - ["화농성 육아종(pyogenic granuloma)", "소엽상 모세혈관 증식이나 세균 없음 [[?robbins-10]]", "면역정상인에게도 흔한 단발 병변 [[harrison-21: 172장 p.1332]]"]
  - id: tx
    section: "선택 — 진단이 치료를 바꾼다"
    title: "Bartonella 혈관 증식 병변의 치료(성인)"
    role: treatment
    span: column
    columns: ["병형", "치료", "주의"]
    rows:
      - ["세균성 혈관종증", "에리트로마이신 500 mg 하루 4번 또는 독시사이클린 100 mg 하루 2번, 3개월 [[harrison-21: 172장 p.1331]]", "다른 마크롤라이드도 대체 가능할 것 [[harrison-21: 172장 p.1331]]"]
      - ["세균성 자반증(간·비장)", "같은 약, 4개월 [[harrison-21: 172장 p.1331]]", "영상에서 간 저음영 병변 [[harrison-21: 172장 p.1332]]"]
      - ["HIV 환자 재발 방지", "마크롤라이드 또는 독시사이클린 억제 치료를 CD4 > 200/µL 까지 [[harrison-21: 172장 p.1333]]", "재발하면 평생 억제가 필요할 수 있다 [[harrison-21: 172장 p.1333]]"]
criteria:
  - id: ba-dx
    name: 진단
    kind: 진단 기준
    population: "심한 면역저하(주로 CD4 < 100/µL 인 HIV)"
    statement: "세균성 혈관종증·자반증은 조직검사로 진단한다 — 은염색에서 간균 무리, 배양은 대개 음성, 혈액 배양은 양성일 수 있다 [[harrison-21: 172장 p.1332]]"
    exceptions: "혈청검사 해석은 이 정리본에서 다루지 않았다"
    source: harrison-21
    basis: current
    exams: [usmle, kmle]
sources:
  - id: harrison-21
    org: "McGraw Hill"
    title: "Harrison's Principles of Internal Medicine, 21st ed. — Chapter 172: Bartonella Infections, Including Cat-Scratch Disease"
    kind: textbook
    year: 2022
    citation: "Loscalzo J, Kasper DL, Longo DL, et al (eds). Harrison's Principles of Internal Medicine, 21e. 172장 p.1328–1333 (Table 172-1, Table 172-2, Bacillary Angiomatosis and Peliosis)"
    checked_at: 2026-09-25
    checked: "본문 대조(드라이브 172장 문서) — p.1329 Table 172-1: B. henselae(고양이, 세균성 혈관종증·자반증), B. quintana(몸니) · p.1331 Table 172-2: 세균성 혈관종증 에리트로마이신 500 mg qid 또는 독시사이클린 100 mg bid 3개월, 자반증 4개월, 다른 마크롤라이드 대체 가능 · p.1332: 심한 면역저하(HIV CD4 < 100/µL), 간·비장 병변은 B. henselae 만, 피하·용해성 뼈 병변은 B. quintana 에 많다, 고양이·고양이 벼룩 노출, MAC 예방 마크롤라이드·ART 로 발생 감소, 병변은 무통의 황갈·적·자색, 결절형은 진균·마이코박테리아 감염과 닮음, 감별에 카포시육종·화농성 육아종·피하 종양·verruga peruana, 병리 = 커진 내피세포의 소엽상 소혈관 증식 + 호중구 우세 혼합 침윤, Warthin-Starry 은염색 간균 무리, 배양 대개 음성, 조직으로 진단, 혈액 배양 양성 가능 · p.1333: 억제 치료 CD4 > 200/µL 까지, 재발 시 평생. 카포시육종의 조직 소견(방추세포·틈새 공간·LANA)·파종 MAC·매독·크립토코쿠스 소견은 이 장에 없다"
    verified: text
  - id: robbins-10
    org: "Elsevier"
    title: "Robbins & Cotran Pathologic Basis of Disease, 10th ed. — Chapter 11: Blood Vessels (Vascular Tumors)"
    kind: textbook
    year: 2020
    citation: "Kumar V, Abbas AK, Aster JC. Robbins & Cotran Pathologic Basis of Disease, 10e. Ch 11"
    checked_at: 2026-09-25
    checked: "서지만(기억) — 카포시육종의 방추세포·틈새 공간·LANA 소견과 화농성 육아종 서술은 원문과 대조하지 않았다. 쪽수 없음"
    verified: citation
  - id: nih-oi
    org: "Panel on Guidelines for the Prevention and Treatment of Opportunistic Infections in Adults and Adolescents With HIV (NIH/CDC/HIVMA-IDSA)"
    title: "Guidelines for the Prevention and Treatment of Opportunistic Infections in Adults and Adolescents With HIV — Bartonellosis; Mycobacterium avium Complex; Syphilis; Cryptococcosis"
    kind: guideline
    url: "https://clinicalinfo.hiv.gov/en/guidelines/hiv-clinical-guidelines-adult-and-adolescent-opportunistic-infections"
    year: 2024
    checked_at: 2026-09-25
    checked: "서지만(기억) — 컨테이너가 기관 누리집·PubMed 를 막아 원문을 열지 못했다. MAC·매독·크립토코쿠스·카포시육종 임상 소견과 억제 치료 중단 세부 조건은 대조하지 않았다. 연도는 최신 개정 추정 · url 은 지침 첫 화면(기억, 열어 보지 않음)"
    verified: citation
diagram:
  title: "진행성 HIV 의 붉은 자주색 결절 — 조직으로 가르기"
  nodes:
    - {id: start, kind: start, text: "진행성 HIV + 붉은 자주색 구진·결절"}
    - {id: hist, kind: decision, text: "생검 조직·염색 소견은?"}
    - {id: bx, kind: info, text: "생검 — 은염색·항산성 염색·LANA 염색"}
    - {id: ks, kind: end, text: "카포시육종(HHV-8) — ART ± 항암"}
    - {id: mac, kind: alert, text: "파종 MAC 등 다른 감염 — 결절은 드묾"}
    - {id: expo, kind: decision, text: "고양이 노출·간 자반증인가?"}
    - {id: hens, kind: end, text: "B. henselae — 마크롤라이드·독시 3~4개월"}
    - {id: quin, kind: end, text: "B. quintana — 뼈 병변 확인, 같은 치료"}
  edges:
    - {from: start, to: hist}
    - {from: hist, to: expo, label: "호중구·은염색 간균"}
    - {from: hist, to: ks, label: "방추세포·틈새"}
    - {from: hist, to: mac, label: "항산균 양성"}
    - {from: hist, to: bx, label: "생검 전"}
    - {from: bx, to: expo, label: "간균 있으면"}
    - {from: bx, to: ks, label: "LANA 양성"}
    - {from: expo, to: hens, label: "예"}
    - {from: expo, to: quin, label: "몸니·노숙"}
diagram_notes:
  - "모양·색·발열·CD4 만으로는 가르지 못한다 — 세균성 혈관종증의 결절형은 진균·마이코박테리아 감염 결절과도 닮았다. 조직검사가 진단이다."
  - "Bartonella 는 배양이 대개 음성이다 — 배양 음성으로 배제하지 않는다. 혈액 배양은 양성일 수 있다."
  - "간·비장 병변(자반증)은 B. henselae 만 만든다. 피하·용해성 뼈 병변은 B. quintana 에 많다."
  - "HIV 환자는 치료 뒤 CD4 > 200/µL 까지 억제 치료를 이어 간다."
checks:
  - q: "진행성 HIV 의 붉은 자주색 결절에서 세균성 혈관종증과 카포시육종을 가르는 조직 소견은?"
    a: "세균성 혈관종증 = 소엽상 소혈관 증식에 호중구 우세 침윤 + 은염색 간균 무리. 카포시육종 = 방추세포 다발·틈새 모양 혈관 공간·적혈구 유출, 세균 없음."
  - q: "간 자반증(peliosis hepatis)이 있으면 어느 Bartonella 인가?"
    a: "B. henselae — 간·비장 병변은 B. henselae 만 만든다. 뼈 용해 병변은 B. quintana 쪽이다."
  - q: "세균성 혈관종증과 자반증의 치료 기간은?"
    a: "에리트로마이신 또는 독시사이클린 — 혈관종증 3개월, 자반증 4개월. HIV 환자는 CD4 > 200/µL 까지 억제 치료."
variants:
  - id: v1
    of: usmle-2026-0171
    flip: true
    changed: "조직을 호중구·은염색 간균에서 방추세포 다발·틈새 공간·LANA 양성으로 → 정답이 Bartonella 에서 HHV-8 로"
    context: "같은 환자 뼈대, 결정적 조직 소견만 카포시육종으로"
    stem: "A 41-year-old man with HIV infection who stopped antiretroviral therapy 18 months ago comes to the physician because of multiple purple skin lesions for 2 months. He has had low-grade fevers and a 3-kg weight loss. He owns two cats. Examination shows several violaceous, nonblanching plaques and nodules 0.5 to 2 cm in diameter on the trunk, legs and hard palate. His CD4+ T-lymphocyte count is 38/mm³. Biopsy of a nodule shows fascicles of spindle cells forming slit-like vascular spaces with extravasated erythrocytes and hemosiderin. There are no neutrophilic infiltrates. A Warthin-Starry silver stain and an acid-fast stain are negative. Immunohistochemical staining of the spindle cell nuclei for latency-associated nuclear antigen is positive. Which of the following is the most likely causal agent?"
    choices: ["A. Bartonella henselae", "B. Human herpesvirus 8", "C. Mycobacterium avium complex", "D. Bartonella quintana", "E. Epstein-Barr virus"]
    answer: "B"
    explanation: "고양이 노출·발열·CD4 38 은 그대로지만, 조직이 방추세포 다발 + 틈새 모양 혈관 공간 + 적혈구 유출이고 호중구·은염색 간균이 없으며 LANA 가 양성이다 — HHV-8 의 카포시육종이다. 고양이 노출은 조직 소견을 이기지 못한다. 경구개 병변도 카포시육종에 흔한 부위다."
    kind: application
  - id: v2
    of: usmle-2026-0171
    flip: false
    changed: "나이·성별·부위·내원 경위·간 소견 제시(촉진 → CT 저음영)를 바꾸고 조직(호중구·은염색 간균·방추세포 없음·항산성 음성)과 고양이 노출은 남김 → 정답 그대로 B. henselae"
    context: "겉모습을 바꾼 같은 판단 — 응급실, 여성, 다리 병변, 영상의 간 병변"
    stem: "A 46-year-old woman with untreated HIV infection is brought to the emergency department because of fever, chills and night sweats for 3 weeks. She feeds several stray cats near her home. Examination shows a dozen friable, bright red papules 3 to 10 mm in diameter on both legs; one is ulcerated and bleeding. Her CD4+ T-lymphocyte count is 27/mm³ and serum alkaline phosphatase is 290 U/L. Abdominal CT shows multiple small hypodense lesions throughout the liver. Biopsy of a papule shows lobular clusters of small blood vessels lined by enlarged endothelial cells, a neutrophil-predominant infiltrate and granular amphophilic material. Spindle cell fascicles are absent. A Warthin-Starry stain shows clumps of small bacilli; Ziehl-Neelsen staining is negative. Which of the following is the most likely causal organism?"
    choices: ["A. Mycobacterium avium complex", "B. Bartonella henselae", "C. Human herpesvirus 8", "D. Histoplasma capsulatum", "E. Bartonella bacilliformis"]
    answer: "B"
    explanation: "다리 병변·여성·응급실·CT 간 저음영으로 겉모습은 바뀌었지만 결정적 단서 — 호중구 우세 소엽상 혈관 증식 + 은염색 간균, 방추세포 없음, 항산성 음성 — 가 그대로라 세균성 혈관종증이다. 간 병변(자반증)과 고양이 노출은 B. henselae 를 가리킨다. B. bacilliformis 는 안데스 모래파리 매개로 여행력이 없다."
    kind: application
---

## 판단 — 왜 조직이 먼저인가
- 진행성 HIV 의 붉은 자주색 결절은 **모양으로 가르지 못한다** — 카포시육종(Kaposi sarcoma)·화농성 육아종(pyogenic granuloma)·피하 종양·verruga peruana 가 모두 감별 대상이다 [[harrison-21: 172장 p.1332]].
- 발열·체중감소·야간 발한 같은 전신 증상도 흔해 파종 감염과 겹친다. 세균성 혈관종증(bacillary angiomatosis)은 **조직검사로 진단**한다 [[harrison-21: 172장 p.1332]].
- 감별이 치료를 바꾼다 — 세균성 혈관종증은 항생제로 낫고, 카포시육종은 ART·항암 쪽이다.

## 기전 — 세균이 혈관 증식을 일으킨다
Bartonella 는 까다롭게 자라는 세포 내 그람음성 간균이다. 면역정상인에게 B. henselae 는 고양이 긁힘 뒤 국소 림프절염(고양이 긁힘병)으로 그치지만, CD4 < 100/µL 의 심한 면역저하에서는 혈관 내피를 자극해 **신생혈관 증식 병변**을 만든다 [[harrison-21: 172장 p.1328, p.1332]]. 그래서 병변은 혈관종처럼 붉고 잘 부서져 피가 나며, 조직에 균 덩어리와 호중구가 섞인다. 간·비장에 가면 혈액이 찬 작은 낭(자반증, peliosis)을 만들어 간비대·ALP 상승·영상의 저음영 병변이 된다 [[harrison-21: 172장 p.1332]].

## 가르는 소견 — 조직·염색이 가른다
- **은염색(Warthin-Starry)** 에서 간균 무리 — Bartonella 는 그람 염색으로 잘 안 보인다. 배양은 대개 음성이라 음성으로 배제하지 않는다 [[harrison-21: 172장 p.1332]].
- 방추세포가 없고 호중구가 있다는 것이 카포시육종과의 경계다. 항산성 염색 음성은 파종 MAC 가능성을 낮춘다.
- 노출이 종을 가른다: 고양이·고양이 벼룩 → B. henselae(간·비장 병변은 이 종만), 몸니·노숙 → B. quintana(피하·용해성 뼈 병변이 많다) [[harrison-21: 172장 p.1332]].

## 선택 — 진단이 치료를 바꾼다
- 마크롤라이드 또는 독시사이클린을 **오래** 쓴다 — 혈관종증 3개월, 자반증 4개월 [[harrison-21: 172장 p.1331]].
- HIV 환자는 ART 를 다시 시작하고, CD4 > 200/µL 까지 억제 치료를 이어 간다 [[harrison-21: 172장 p.1333]].

## 권고와 예외
- 1차 예방 항생제는 권하지 않는다. 고양이 벼룩 관리·고양이 긁힘 피하기(B. henselae), 몸니 치료(B. quintana)가 예방이다 [[harrison-21: 172장 p.1333]].
- MAC 예방으로 쓰는 마크롤라이드·리파부틴과 ART 보급 뒤 발생이 줄었다 [[harrison-21: 172장 p.1332]].
- 카포시육종·MAC·매독·크립토코쿠스의 세부 소견은 해리슨 이 장과 대조하지 않았다(검토 항목).

## 시험 쟁점 — 충돌·맥락·새 근거
- **Z1 맥락 · 억제 치료를 끊는 조건** — 시험 기준: CD4 > 200/µL 까지 억제 치료, 재발하면 평생 [[harrison-21: 172장 p.1333]] / 다른 기준: 미국 HIV 기회감염 지침은 CD4 > 200 이 일정 기간 유지되는 등의 조건을 덧붙인다 [[?nih-oi]] / 왜 다른가: 교과서는 요약, 지침은 유지 기간·치료 반응까지 정한다 / 시험에서는: KMLE·USMLE 모두 「CD4 > 200 까지」로 충분하다.
- **Z2 맥락 · 치료 기간 3개월 vs 4개월** — 시험 기준: 피부 혈관종증 3개월, 간·비장 자반증 4개월 [[harrison-21: 172장 p.1331]] / 다른 기준: 「최소 3개월」로 묶어 쓰는 자료가 있다 [[?nih-oi]] / 왜 다른가: 자반증을 따로 두는지의 차이 / 시험에서는: KMLE·USMLE 모두 기간보다 약(마크롤라이드·독시사이클린)을 묻는다.
