---
id: cn.onc.her2-breast-cancer.trastuzumab-baseline-echo
type: concept
topic: Hematology-Oncology
see_also: [Pathology, Cardiology]
date: 2026-10-03
updated: 2026-10-03
version: 2
outline: h79            # 해리슨 21판 79장 Breast Cancer(혈액종양내과 책)
confidence: medium
review_status: unreviewed
note_form: 2            # 판형 2(2026-09-25)
title: "HER2 양성 유방암 — 표적치료 전에는 심초음파"
objective: "HER2 면역조직화학 3+ 유방암에서 트라스투주맙을 쓰기 전 좌심실 기능 검사를 고른다"
objective_kind: 검사 선택
condition: HER2 양성 유방암(HER2-positive breast cancer)의 항 HER2 치료 전 평가
exams: [usmle, kmle]
summary:
  - "결론: 트라스투주맙 시작 전 심초음파로 좌심실 박출률을 재고, 치료 중에도 반복한다."
  - "시험 단서: 종양 세포막 전체가 진한 갈색 HER2 염색(IHC 3+) + 표적 단일클론항체(trastuzumab) 계획."
  - "왜: 트라스투주맙의 주된 독성은 심근 기능 저하다 — 다른 장기 기저 검사는 다른 약의 몫이다."
  - "골밀도 검사는 아로마테이스 억제제(ER 양성·폐경 후) 몫 — ER·PR 음성이면 내분비 치료 대상이 아니다."
  - "IHC 3+ 양성·0–1+ 음성·2+ 는 FISH 로 확인(HER2/CEP17 ≥ 2.0 이면 증폭)."
pitfalls:
  - contrast: "골밀도 검사 vs 심초음파"
    point: "골밀도 검사는 아로마테이스 억제제가 에스트로겐을 고갈시켜 골다공증을 일으키기 때문에 하는 검사다. ER·PR 음성 종양은 내분비 치료 대상이 아니고, 계획된 표적항체(트라스투주맙)의 독성은 심장이다."
    exception: "ER 양성 폐경 후 환자가 아로마테이스 억제제를 시작하면 골밀도 검사가 맞다."
    cites: ["harrison-21: 79장 p.620", "harrison-21: 79장 p.623"]
    covers: ["imaging-2026-0205:D"]
  - contrast: "폐기능·청력·안과 검사 — 항암 전 기저 검사면 다 같은가?"
    point: "기저 검사는 약의 표적 장기를 따른다: 블레오마이신 → 폐기능, 시스플라틴 → 청력, 에탐부톨 → 시력. 염색이 표적을, 표적이 약을, 약이 위험 장기를 정한다."
  - contrast: "트라스투주맙 심독성 = 안트라사이클린 심근병증?"
    point: "안트라사이클린(독소루비신)은 누적 용량에 따른 울혈성 심부전이다. 트라스투주맙은 심근 기능 저하로, 증상 있는 심부전은 드물며 안트라사이클린과 동시에 주면 더 자주 생겨 동시 투여를 피한다."
    cites: ["harrison-21: 79장 p.621", "harrison-21: 79장 p.622"]
tables:
  - id: baseline
    section: "가르는 소견 — 약이 위험 장기를 정한다"
    title: "치료 전 기저 검사 — 약과 위험 장기"
    role: differential
    span: column
    columns: ["약", "주된 독성", "기저 검사"]
    rows:
      - ["트라스투주맙(항 HER2 항체)", "심근 기능 저하 [[harrison-21: 79장 p.622]]", "심초음파(좌심실 박출률), 치료 중 3개월마다 [[harrison-21: 79장 p.622]]"]
      - ["안트라사이클린", "누적 용량 의존 울혈성 심부전 [[harrison-21: 79장 p.621]]", "좌심실 기능 평가"]
      - ["아로마테이스 억제제(ER 양성)", "골다공증·골절 [[harrison-21: 79장 p.620]]", "골밀도 검사를 일반 폐경 여성보다 자주 [[harrison-21: 79장 p.623]]"]
      - ["블레오마이신 · 시스플라틴 · 에탐부톨", "폐섬유화 · 청력 소실 · 시신경염", "폐기능 · 청력 · 시력 검사 [[?harrison-21]]"]
  - id: her2
    section: "기전 — 수용체 과발현에서 표적치료와 심장까지"
    title: "HER2 판정"
    role: criteria
    span: column
    columns: ["결과", "판정", "다음"]
    rows:
      - ["IHC 3+", "양성", "FISH 불필요 → 항 HER2 치료 [[harrison-21: 79장 p.620]]"]
      - ["IHC 2+", "경계", "반사 FISH — HER2/CEP17 ≥ 2.0 이면 증폭 [[harrison-21: 79장 p.620]]"]
      - ["IHC 0–1+", "음성", "항 HER2 치료 이득 없음 [[harrison-21: 79장 p.620]]"]
criteria:
  - id: her2-status
    name: HER2 판정
    kind: 진단 기준
    population: "모든 원발·전이 유방암 생검"
    statement: "ER 과 HER2 는 가장 중요한 예측 인자로 모든 생검에서 검사한다. IHC 3+ 양성, 0–1+ 음성, 2+ 는 반사 FISH 로 HER2/CEP17 비 ≥ 2.0 이면 증폭 [[harrison-21: 79장 p.620]]"
    exceptions: "HER2 음성 종양에는 트라스투주맙의 이득이 없다 [[harrison-21: 79장 p.620]]"
    source: harrison-21
    basis: current
    exams: [usmle, kmle]
  - id: trastuzumab-cardiac
    name: 트라스투주맙 심장 감시
    kind: 치료 권고
    population: "보조·수술 전 트라스투주맙을 받는 HER2 양성 유방암"
    statement: "트라스투주맙은 심근 기능 저하를 일으킬 수 있어 기저·연속 심초음파 감시가 필요하다. 치료 중 3개월마다 하고, 끝난 뒤에는 하지 않는다 [[harrison-21: 79장 p.622]]"
    exceptions: "심장 이상 병력이 있으면 쓰지 않거나 경험 있는 심장내과와 함께 본다. 안트라사이클린과 동시 투여는 피한다 [[harrison-21: 79장 p.621–622]]. 박출률이 얼마 떨어지면 중단하는지는 이 정리본에서 대조하지 않았다"
    source: harrison-21
    basis: current
    exams: [usmle, kmle]
sources:
  - id: harrison-21
    org: "McGraw Hill"
    title: "Harrison's Principles of Internal Medicine, 21st ed. — Chapter 79: Breast Cancer"
    kind: textbook
    year: 2022
    citation: "Loscalzo J, Kasper DL, Longo DL, et al (eds). Harrison's Principles of Internal Medicine, 21e. 79장 p.620–623"
    url: "https://accessmedicine.mhmedical.com/book.aspx?bookid=3095"
    checked_at: 2026-10-03
    checked: "본문 대조(드라이브 장별 문서 79장) — p.620 ER·HER2 는 가장 중요한 예측 인자, IHC 3+ 양성·0–1+ 음성·2+ 반사 FISH·HER2/CEP17 ≥ 2.0 증폭, HER2 음성에는 트라스투주맙 이득 없음, 아로마테이스 억제제가 골다공증·골절을 일으키거나 악화 · p.621 트라스투주맙의 주된 독성은 심장 기능 저하이고 독소루비신과 동시 투여 때 더 잦아 동시 투여를 피함, 안트라사이클린은 누적 용량 관련 울혈성 심부전 · p.622 기저·연속 심초음파 감시, 증상 있는 심부전은 드묾, 심장 이상 병력이면 쓰지 않거나 심장내과와, 치료 중 3개월마다 심초음파·끝난 뒤에는 안 함 · p.623 아로마테이스 억제제 사용 중 골밀도를 더 자주. 블레오마이신·시스플라틴·에탐부톨 독성은 이 장에 없음"
    verified: text
diagram:
  title: "HER2 판정에서 표적치료 전 검사까지"
  nodes:
    - {id: start, kind: start, text: "침윤성 유방암 생검"}
    - {id: ihc, kind: decision, text: "HER2 IHC 결과는?"}
    - {id: fish, kind: info, text: "반사 FISH — HER2/CEP17 비"}
    - {id: neg, kind: alert, text: "HER2 음성 — 항 HER2 치료 이득 없음"}
    - {id: tras, kind: step, text: "트라스투주맙(± 퍼투주맙) 계획"}
    - {id: hx, kind: decision, text: "심장 이상 병력이 있나?"}
    - {id: echo, kind: end, text: "기저 심초음파 → 치료 중 3개월마다"}
    - {id: cardio, kind: alert, text: "쓰지 않거나 심장내과와 함께"}
  edges:
    - {from: start, to: ihc}
    - {from: ihc, to: tras, label: "3+"}
    - {from: ihc, to: fish, label: "2+"}
    - {from: ihc, to: neg, label: "0–1+"}
    - {from: fish, to: tras, label: "≥ 2.0"}
    - {from: fish, to: neg, label: "< 2.0"}
    - {from: tras, to: hx}
    - {from: hx, to: echo, label: "없음"}
    - {from: hx, to: cardio, label: "있음"}
diagram_notes:
  - "트라스투주맙은 독소루비신과 동시에 주면 심기능 저하가 더 잦아 동시 투여를 피한다 — 대개 탁산과 함께 준다."
  - "치료가 끝난 뒤에는 심초음파를 계속하지 않는다."
  - "ER 양성 폐경 후 환자가 아로마테이스 억제제를 쓰면 그때는 골밀도 검사를 더 자주 한다."
checks:
  - q: "HER2 IHC 3+ 유방암에 트라스투주맙을 시작하기 전 꼭 하는 검사는?"
    a: "심초음파(좌심실 박출률). 트라스투주맙의 주된 독성이 심근 기능 저하라 기저와 치료 중 3개월마다 잰다."
  - q: "IHC 2+ 이면 어떻게 판정하나?"
    a: "경계 — 반사 FISH 로 HER2/CEP17 비 ≥ 2.0 이면 증폭(양성)."
  - q: "골밀도 검사는 어떤 유방암 치료 전에 하나?"
    a: "아로마테이스 억제제(ER 양성, 대개 폐경 후) — 에스트로겐 고갈로 골다공증·골절이 늘기 때문이다."
variants:
  - id: v1
    of: imaging-2026-0205
    flip: true
    changed: "24세·ER/PR 음성·HER2 3+·표적 항체 계획 → 63세 폐경 후·ER/PR 양성·HER2 음성(IHC 1+)·수술 후 레트로졸 계획 ⇒ 정답이 심초음파에서 골밀도 검사로"
    context: "같은 유방암 치료 전 기저 검사, 표적이 HER2 가 아니라 에스트로겐 수용체"
    stem: "A 63-year-old woman comes for follow-up 4 weeks after lumpectomy and sentinel lymph node biopsy for a 1.8-cm invasive ductal carcinoma of the right breast. Her last menstrual period was 11 years ago. Pathology showed negative margins and no nodal metastases. The tumor is estrogen receptor-positive and progesterone receptor-positive, and HER2 immunohistochemistry is 1+. She will begin radiation therapy followed by 5 years of letrozole. Which of the following is the most appropriate test to obtain before starting the endocrine therapy?"
    choices: ["A. Pulmonary function testing", "B. Audiometry", "C. Ophthalmologic examination", "D. Bone densitometry", "E. Echocardiography"]
    answer: "D"
    explanation: "HER2 1+ is negative, so trastuzumab is not indicated and there is no reason for baseline cardiac monitoring. The planned drug is an aromatase inhibitor, which depletes estrogen and causes or worsens osteoporosis and fractures; bone density should be checked at baseline and more often than in average postmenopausal women."
    kind: application
  - id: v2
    of: imaging-2026-0205
    flip: false
    changed: "24세 여자·유방 종괴로 내원·HER2 를 그림으로 제시 → 41세 여자·검진 유방촬영 이상·HER2 를 IHC 3+ 로 글로 제시, 계획을 트라스투주맙+퍼투주맙으로 명시 ⇒ 답은 그대로 심초음파"
    context: "겉모습(나이·내원 경위·제시 방식)만 바꾸고 HER2 3+·항 HER2 항체 단서는 남긴 변형"
    stem: "A 41-year-old woman is referred after a screening mammogram showed a 2.5-cm spiculated mass in the left breast. She has hypothyroidism treated with levothyroxine and no other medical problems. Pulse is 72/min and blood pressure is 118/74 mm Hg. Core needle biopsy shows invasive ductal carcinoma; the tumor is estrogen receptor-negative, progesterone receptor-negative, and HER2 3+ by immunohistochemistry. Neoadjuvant paclitaxel with trastuzumab and pertuzumab is planned. Which of the following is the most appropriate test to obtain before starting treatment?"
    choices: ["A. Bone densitometry", "B. Pulmonary function testing", "C. Echocardiography", "D. Audiometry", "E. Ophthalmologic examination"]
    answer: "C"
    explanation: "The decisive cues are unchanged: HER2 3+ is positive without FISH, and anti-HER2 antibodies are planned. Trastuzumab can cause cardiac muscle dysfunction, so baseline echocardiography is required and is repeated every 3 months during therapy. Age, presentation, and hypothyroidism do not change the organ at risk."
    kind: application
figures:
- id: f1
  file: docs/assets/figures/hpa-erbb2_141672_a_4_8.jpg
  kind: histology
  at: 기전 — 수용체 과발현에서 표적치료와 심장까지
  shows: 유방 관암종의 ERBB2(HER2) 면역조직화학 — 강한 염색
  look_for:
  - 종양 세포 둥지의 세포막을 따라 갈색이 둘러싼 그물 모양
  - 둥지 사이 간질은 푸른 대조염색만(음성)
  label: Breast cancer(표본 진단 Duct carcinoma), ERBB2 면역조직화학
  label_basis: dataset_expert
  reference: 조직 종류·표본 진단 = 표본 기록(병리의사 SNOMED 주석), 세포별 염색 강도 = HPA 병리의사 주석(이 항체·조직의 요약 — 사진 한 장 단위가 아님)
  paper: Uhlén M 외. Tissue-based map of the human proteome. Science 2015;347:1260419
  doi: 10.1126/science.1260419
  credit: Human Protein Atlas, ERBB2 / Breast cancer (CC BY 4.0), https://images.proteinatlas.org/62555/141672_A_4_8.jpg
  license: Creative Commons Attribution 4.0 International
  url: https://www.proteinatlas.org/ENSG00000141736-ERBB2/cancer/breast+cancer
  asset: HPA-ERBB2_141672_A_4_8
  paper_cited_by: 14435
---

## 판단 — 왜 심초음파가 먼저인가
- 염색이 표적을 정한다: 종양 세포막 전체가 진하게 물드는 HER2 3+ 는 양성이라 항 HER2 항체(트라스투주맙) 대상이다 [[harrison-21: 79장 p.620]].
- 약이 위험 장기를 정한다: 트라스투주맙의 주된 독성은 심근 기능 저하라 기저와 치료 중 연속 심초음파가 필요하다 [[harrison-21: 79장 p.621–622]].
- ER·PR 음성이면 내분비 치료(아로마테이스 억제제)의 이득이 없어 골밀도 검사가 치료 전 검사로 오지 않는다 [[harrison-21: 79장 p.620]].

## 기전 — 수용체 과발현에서 표적치료와 심장까지
HER2(human epidermal growth factor receptor 2, c-neu/erbB2)는 세포막 수용체 티로신 키나아제다. 유전자 증폭으로 단백이 과발현되면 세포 표면에 수용체가 많아져 면역조직화학(immunohistochemistry, IHC)에서 세포막 전체가 둘러싸이듯 물든다. 판정은 IHC 단백 과발현이나 FISH(fluorescence in situ hybridization) 유전자 증폭으로 한다 [[harrison-21: 79장 p.620]].
- 과발현된 세포 표면 단백이 곧 항체의 표적이라, HER2 양성일 때만 트라스투주맙이 재발·사망 위험을 줄인다 [[harrison-21: 79장 p.620]].
- 같은 수용체 경로를 막는 것이 심근 기능을 떨어뜨릴 수 있다 — 증상 있는 심부전은 드물지만 무증상 기능 저하를 잡으려고 박출률을 잰다 [[harrison-21: 79장 p.622]]. 심근세포에서 HER2 신호가 하는 역할의 세부 기전은 해리슨 이 장에 없어 대조하지 않았다.

## 가르는 소견 — 약이 위험 장기를 정한다
- 보기의 기저 검사는 모두 어떤 약의 정답이다. 「표적 → 약 → 위험 장기」 순서로 하나만 남긴다.
- 안트라사이클린과 트라스투주맙은 둘 다 심장이지만 성격이 다르다: 안트라사이클린은 누적 용량 의존 울혈성 심부전, 트라스투주맙은 심근 기능 저하이고 둘을 동시에 주면 더 잦다 [[harrison-21: 79장 p.621]].

## 선택 — 언제 쓰지 않거나 심장내과와 보나
- 심장 이상 병력이 있으면 트라스투주맙을 쓰지 않거나 경험 있는 심장내과와 함께 본다 [[harrison-21: 79장 p.622]].
- 치료 중 3개월마다 심초음파, 치료가 끝난 뒤에는 하지 않는다 [[harrison-21: 79장 p.622]].
- 트라스투주맙은 탁산과 함께 주는 것이 좋고, 위험이 낮은 T1–2·림프절 음성이면 파클리탁셀+트라스투주맙으로 충분하다. 퍼투주맙을 더하면 수술 전 치료에서 병리적 완전관해가 늘어난다 [[harrison-21: 79장 p.621]].

## 권고와 예외
- 첫 투여 때 주입 관련 알레르기 반응이 있을 수 있으나 대개 다시 생기지 않는다 [[harrison-21: 79장 p.622]].
- 박출률이 얼마나 떨어지면 중단·재개하는지(수치 기준)는 이 정리본에서 대조하지 않았다(검토 항목).

## 시험 쟁점 — 충돌·맥락·새 근거
- 해당 없음(대조: 해리슨 79장 p.620–623)
