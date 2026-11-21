---
id: cn.neph.adpkd.aneurysm-screening-mra
type: concept
topic: Nephrology
see_also: [Neurology]
date: 2026-11-21
updated: 2026-11-21
version: 1
outline: h315           # 기본틀 슬롯(content/outline/subjects.yaml) — 해리슨 22판 327장
confidence: medium
review_status: unreviewed
note_form: 2            # 판형 2(2026-09-25)
title: "다낭신 — 동맥류 가족력이면 증상 없어도 뇌 MRA"
objective: "상염색체 우성 다낭신장병 환자에서 뇌동맥류 가족력과 증상 유무를 보고 뇌동맥류 선별 검사를 고른다"
objective_kind: 검사 선택
condition: 상염색체 우성 다낭신장병(ADPKD)의 두개내 동맥류(intracranial aneurysm)
exams: [kmle, usmle]
summary:
  - "결론: 다낭신 + 뇌동맥류·거미막하출혈 가족력이면 증상이 없어도 뇌 MR 혈관조영술(MRA)로 선별한다."
  - "시험 단서: 부모 투석 + 양쪽 다발 신장낭종·간낭종 + 친척의 젊은 뇌출혈 사망(family history of aneurysm), 무증상."
  - "왜: 다낭신은 동맥류가 4~5배 흔하고 가족력이 파열 위험 인자다 — 파열 전 동맥류는 혈관 영상만 보여 준다."
  - "쓰지 않는다: 비조영 CT·요추천자(이미 생긴 출혈을 찾는다), 카테터 혈관조영(침습 — 출혈 확진·치료 계획용)."
  - "심장초음파·대장내시경·신동맥 영상·신장 조직검사는 증상이나 다른 단서가 있을 때만 — 일상 선별이 아니다."
pitfalls:
  - contrast: "비조영 CT·요추천자 vs MRA — 「뇌출혈이 걱정되면 CT」?"
    point: "비조영 CT 는 이미 생긴 거미막하출혈의 혈액을 찾는 검사이고, 요추천자는 CT 가 음성인데 출혈이 의심될 때 쓴다. 두통·신경학적 증상이 없는 사람의 파열 전 동맥류는 혈관 영상(MRA)으로만 찾는다."
    exception: "갑작스러운 심한 두통(경고 두통 포함)이 있으면 선별이 아니라 출혈 진단이다 — 비조영 CT 먼저, 음성이면 요추천자."
    cites: ["harrison-22-sah: 440장 p.3459", "harrison-22: 327장 p.2432"]
    covers: ["kmle-2026-1649:D", "kmle-2026-1649:A"]
  - contrast: "카테터 뇌혈관조영 vs MRA — 「표준 검사」라서?"
    point: "카테터 혈관조영은 동맥류 해부를 가장 자세히 보지만 침습적이고 뇌졸중 등 합병증 위험이 있다. 증상 없는 사람의 선별은 비침습 MRA 로 하고, 카테터는 출혈 확진 뒤나 치료 계획 때 쓴다."
    cites: ["harrison-22-sah: 440장 p.3459"]
    covers: ["kmle-2026-1649:E"]
  - contrast: "경흉부 심장초음파 — 다낭신에 판막 이상이 흔하니?"
    point: "승모판 탈출증은 다낭신의 최대 30% 에 있지만 대부분 무증상이다. 잡음·심부전 증상이 없으면 이 문항형에서 가족력이 가리키는 검사는 뇌동맥류 선별이다."
    cites: ["harrison-22: 327장 p.2432"]
    covers: ["kmle-2026-1649:C", "kmle-2026-1874:D"]
  - contrast: "젊은 고혈압 = 신동맥 협착 검사?"
    point: "다낭신의 고혈압은 레닌-안지오텐신-알도스테론계 활성·교감신경 항진으로 사구체여과율이 떨어지기 전에 흔히 생긴다 — 원인이 이미 설명된다. 조영 CT 는 신기능이 떨어진 환자에게 조영제 신독성 부담도 있다."
    cites: ["harrison-22: 327장 p.2432–2433"]
    covers: ["kmle-2026-1874:E"]
  - contrast: "혈뇨 + 신장 혹 = 신장 조직검사?"
    point: "다낭신은 가족력과 영상(나이별 낭종 수)으로 진단한다. 육안 혈뇨는 낭종 파열로 흔히 생긴다(약 40%). 애매하면 조직이 아니라 유전자 검사를 본다."
    cites: ["harrison-22: 327장 p.2432–2433"]
    covers: ["kmle-2026-1874:A"]
  - contrast: "대장 게실이 늘어나니 대장내시경?"
    point: "다낭신에서 대장 게실·복벽 탈장이 더 흔하지만 증상 없는 선별 대상이 아니다."
    cites: ["harrison-22: 327장 p.2432"]
    covers: ["kmle-2026-1874:C"]
tables:
  - id: who
    section: "선택 — 선별 대상과 방법"
    title: "뇌동맥류 — 누구에게 무엇을"
    role: tests
    span: column
    columns: ["상황", "검사", "근거·주의"]
    rows:
      - ["무증상 + 동맥류·거미막하출혈 가족력", "비조영 뇌 MRA 로 선별", "가족력 = 파열 위험 인자 [[harrison-22: 327장 p.2432]]"]
      - ["무증상 + 가족력 없음", "일률 선별 안 함", "선별의 역할 불명확 [[harrison-22: 327장 p.2432]] — 지침의 추가 대상은 시험 쟁점 Z1"]
      - ["갑작스러운 심한 두통·신경학적 이상", "비조영 CT → 음성이면 요추천자", "선별이 아니라 출혈 진단 [[harrison-22-sah: 440장 p.3459]]"]
      - ["선별에서 동맥류 발견·출혈 확진", "CT 혈관조영·카테터 혈관조영", "위치·해부 확인과 치료 계획 [[harrison-22-sah: 440장 p.3459]]"]
  - id: tests
    section: "가르는 소견 — 출혈 검사와 선별 검사"
    title: "검사가 보는 것"
    role: comparison
    span: column
    columns: ["검사", "보는 것", "한계"]
    rows:
      - ["비조영 MRA(TOF)", "파열 전 동맥류", "조영제·방사선 없음 [[?kdigo-adpkd-2025]]"]
      - ["비조영 CT", "거미막하 혈액(72시간 안 95% 이상)", "파열 전 동맥류는 못 본다"]
      - ["요추천자", "CT 음성일 때 혈액·황색 변색", "출혈이 있어야 의미"]
      - ["카테터 혈관조영", "가장 자세한 해부(4혈관)", "침습 — 뇌졸중 등 합병증"]
    note: "harrison-22-sah: 440장 p.3459"
criteria:
  - id: ica-screen-family
    name: 뇌동맥류 선별(Harrison)
    kind: 검사 기준
    population: "증상 없는 ADPKD 환자 중 두개내 동맥류 가족력이 있는 사람"
    statement: "증상 전 MRA 로 두개내 동맥류를 선별할 수 있다. 가족력이 없는 무증상 환자의 영상 선별 역할은 불명확하다"
    exceptions: "출혈 증상이 있으면 선별이 아니라 비조영 CT·요추천자로 출혈을 진단한다"
    source: harrison-22
    locator: "327장 p.2432"
    basis: current
    exams: [kmle, usmle]
sources:
  - id: harrison-22
    org: "McGraw Hill"
    title: "Harrison's Principles of Internal Medicine, 22nd ed. — Chapter 327: Polycystic Kidney Disease and Other Inherited Disorders of Tubule Growth and Development"
    kind: textbook
    year: 2025
    citation: "Loscalzo J, Fauci AS, Kasper DL, et al (eds). Harrison's Principles of Internal Medicine, 22e. McGraw Hill; 2025. 327장 p.2430–2436"
    checked_at: 2026-11-21
    checked: "본문 대조(PC, 드라이브 원본 PDF 327장 p.2430–2433, 머리 인쇄쪽 확인) — p.2430 Table 327-1 ADPKD 에 지주막하출혈 동반; p.2431 PKD1 ~85%·PKD2 ~15%, 유병률 1:1000–1:400; p.2432 옆구리 통증 ~60%·낭종 파열 육안 혈뇨 ~40%·결석 ~20%, 고혈압이 GFR 감소 전에 생기고 RAAS 활성·교감 항진이 원인, 두개내 동맥류 4–5배·가족력이 파열 위험 인자·고혈압/흡연의 독립성 불명확·경고 두통 20–50%·출혈 진단은 CT 먼저 요추천자로 확인·무증상 환자 영상 선별 역할 불명확·가족력 있으면 MRA 로 증상 전 선별, 승모판 탈출 최대 30%(대부분 무증상)·대장 게실·복벽 탈장 증가, 진단은 가족력+양측 다발 낭종·나이별 낭종 수 기준; p.2433 CT 의 방사선·조영제 신독성, 애매하면 유전자 검사, 혈압 목표 140/90(JNC VIII)·더 엄격한 조절이 더 이롭지 않다·HALT PKD 엄격 조절이 낭종 성장 늦춤, 첫 문장 「FDA 승인 특이 치료 없음」과 뒤 문장 「FDA 가 빠른 진행 위험군에 톨밥탄 적응」, 톨밥탄 부작용 간기능 장애·다음다갈. MRA 가 조영제 없는 TOF 라는 서술은 이 장에 없다"
    verified: text
  - id: harrison-22-sah
    org: "McGraw Hill"
    title: "Harrison's Principles of Internal Medicine, 22nd ed. — Chapter 440: Subarachnoid Hemorrhage"
    kind: textbook
    year: 2025
    citation: "Loscalzo J, Fauci AS, Kasper DL, et al (eds). Harrison's Principles of Internal Medicine, 22e. McGraw Hill; 2025. 440장 p.3457–3461"
    checked_at: 2026-11-21
    checked: "본문 대조(PC, 원본 PDF 440장 p.3458–3459) — p.3458 미파열 동맥류는 대부분 무증상, 크기·위치가 파열 위험을 정하고 예방 치료의 득실은 시술 합병증률에 달림; p.3459 72시간 안 고품질 비조영 CT 에서 95% 이상 혈액이 보임, 음성이면 요추천자(황색 변색), CT 없을 때만 영상 전 요추천자, 출혈 확진 뒤 4혈관 카테터 혈관조영으로 동맥류 해부·다른 미파열 동맥류 확인, CT 혈관조영이 대안, 카테터 혈관조영은 침습적이고 뇌졸중 등 합병증 위험"
    verified: text
  - id: kdigo-adpkd-2025
    org: "KDIGO ADPKD Work Group"
    title: "KDIGO 2025 Clinical Practice Guideline for the Evaluation, Management, and Treatment of Autosomal Dominant Polycystic Kidney Disease (ADPKD)"
    kind: guideline
    year: 2025
    citation: "Kidney Int 2025;107(2S):S1–S239"
    doi: "10.1016/j.kint.2024.07.009"
    pmid: "39848759"
    url: "https://doi.org/10.1016/j.kint.2024.07.009"
    checked_at: 2026-11-21
    checked: "서지만 — PubMed 메타데이터로 제목·권호·쪽·DOI·PMID 확인(본문은 초록 없음, 요약본 PMID 39848746 은 초록만). 선별 추가 대상·TOF MRA·혈압 목표 등 권고 원문은 대조하지 못했다"
    verified: citation
diagram:
  title: "다낭신 — 뇌동맥류 검사 고르기"
  nodes:
    - {id: start, kind: start, text: "다낭신 — 가족력 + 양쪽 다발 신장낭종"}
    - {id: sx, kind: decision, text: "갑작스러운 심한 두통·신경 이상?"}
    - {id: bleed, kind: end, text: "출혈 진단 — 비조영 CT, 음성이면 요추천자"}
    - {id: fh, kind: decision, text: "동맥류·거미막하출혈 가족력?"}
    - {id: fhask, kind: info, text: "가족의 뇌출혈·급사·동맥류 병력을 묻는다"}
    - {id: other, kind: decision, text: "고위험 직업·큰 수술 예정·희망?"}
    - {id: mra, kind: end, text: "비조영 뇌 MRA(TOF)로 선별"}
    - {id: none, kind: end, text: "일률 선별 안 함 — 혈압 조절·금연"}
  edges:
    - {from: start, to: sx}
    - {from: sx, to: bleed, label: "있음"}
    - {from: sx, to: fh, label: "없음"}
    - {from: fh, to: mra, label: "있음"}
    - {from: fh, to: fhask, label: "모름"}
    - {from: fh, to: other, label: "없음"}
    - {from: fhask, to: mra, label: "있으면"}
    - {from: fhask, to: other, label: "없으면"}
    - {from: other, to: mra, label: "있음"}
    - {from: other, to: none, label: "없음"}
diagram_notes:
  - "「가족력」은 친척의 동맥류·거미막하출혈 — 문항에서는 「40대 갑작스러운 뇌출혈 사망」처럼 진단명 없이 나오기도 한다."
  - "고위험 직업·큰 수술 전·본인 희망으로 선별을 넓히는 갈래는 지침 원문을 대조하지 못했다 [[?kdigo-adpkd-2025]] — 해리슨은 가족력만 든다."
  - "선별에서 동맥류가 나오면 크기·위치로 치료를 정하고, 그때 CT 혈관조영·카테터 혈관조영으로 해부를 본다 [[harrison-22-sah: 440장 p.3458–3459]]."
  - "재선별 간격은 이 정리본에서 대조하지 않았다(검토 항목)."
checks:
  - q: "증상 없는 다낭신 환자 중 누구를 뇌동맥류 선별하고, 무엇으로 하나?"
    a: "두개내 동맥류·거미막하출혈 가족력이 있는 사람 — 비침습 MRA 로 한다."
  - q: "선별에 비조영 CT 를 쓰지 않는 이유는?"
    a: "비조영 CT 는 이미 생긴 거미막하 혈액을 찾는 검사라 파열 전 동맥류를 보지 못한다. 출혈 증상이 있을 때의 첫 검사다."
  - q: "다낭신 환자가 갑자기 생애 최악의 두통을 호소하면 첫 검사는?"
    a: "선별이 아니라 출혈 진단 — 비조영 CT, 음성이면 요추천자."
figures_none: 무증상 환자에게 어떤 선별 검사를 고르느냐가 목표라 영상 판독이 단서가 아니다
---

## 판단 — 왜 MRA 선별이 먼저인가
- 다낭신(ADPKD)에서 두개내 동맥류는 일반인보다 4~5배 흔하고 파열하면 사망률이 높다. **가족 중 동맥류**가 있으면 파열 위험이 더 크다 [[harrison-22: 327장 p.2432]].
- 그래서 가족력이 있으면 **증상이 없어도** 파열 전에 찾는다 — 해리슨은 이때 MRA 로 증상 전 선별을 한다고 쓴다 [[harrison-22: 327장 p.2432]].
- 선별은 비침습이어야 한다. 조영제가 필요 없는 TOF MRA 는 신기능이 떨어지기 시작한 다낭신 환자에게도 부담이 적다 [[?kdigo-adpkd-2025]].
- 두통·신경학적 이상이 있으면 질문이 바뀐다 — 선별이 아니라 출혈 진단(비조영 CT → 요추천자)이다.

## 기전 — 폴리시스틴 이상에서 동맥류까지
PKD1(약 85%)·PKD2(약 15%)가 만드는 폴리시스틴-1·2(polycystin)는 일차 섬모와 세포막에서 칼슘 신호를 조절한다. 기능을 잃으면 cAMP 가 늘어 낭종 상피가 증식하고 액체를 분비한다 [[harrison-22: 327장 p.2430–2431]]. 폴리시스틴은 거의 모든 조직에 있어, 혈관 평활근·근섬유모세포의 결함이 동맥류를 직접 일으킬 수 있다 [[harrison-22: 327장 p.2432]].
- 고혈압이 흔하지만 고혈압·흡연이 동맥류 파열의 독립 위험 인자인지는 불명확하다 — 가족력만 확립된 위험 인자다 [[harrison-22: 327장 p.2432]].
- 파열 전 20~50% 가 「경고 두통」을 겪는다 — 이 두통은 선별 대상이 아니라 출혈 검사 대상이다.
- 다른 혈관 이상(뇌동맥 확장증 → 박리·뇌졸중), 승모판 탈출(최대 30%), 대장 게실·복벽 탈장도 흔하다.

## 가르는 소견 — 출혈 검사와 선별 검사
검사는 **증상**이 고른다. 비조영 CT 는 72시간 안에 95% 이상에서 거미막하 혈액을 보여 주지만 혈액이 없으면 말할 것이 없다 — 음성이어도 동맥류는 배제되지 않는다 [[harrison-22-sah: 440장 p.3459]]. 카테터 혈관조영은 출혈 확진 뒤 해부를 보고 시술을 하는 검사다.
- 다낭신 진단 자체는 가족력 + 초음파 낭종 수(15~29세 2개 이상, 30~59세 양쪽 각 2개 이상, 60세 이상 양쪽 각 4개 이상)로 하고, 애매하면 유전자 검사를 본다 — 조직검사가 아니다 [[harrison-22: 327장 p.2432–2433]].

## 선택 — 선별 대상과 방법
- 가족력(+) → 비조영 MRA. 가족력(−)·무증상 → 해리슨은 일률 선별의 역할이 불명확하다고 본다 [[harrison-22: 327장 p.2432]].
- 동맥류가 나오면 크기·위치가 파열 위험을 정한다 — 작은 미파열 동맥류의 파열률은 낮고, 예방 치료의 득실은 시술 합병증률에 달린다 [[harrison-22-sah: 440장 p.3458]].

## 권고와 예외
- 혈압은 레닌-안지오텐신-알도스테론계 차단(안지오텐신전환효소억제제·안지오텐신수용체차단제)이 중심이다 [[harrison-22: 327장 p.2433]] — 동맥류 선별과 별개로 함께 한다.
- 빠르게 진행할 위험이 큰 성인은 톨밥탄(V2 수용체 길항제)을 고려한다. 간기능 장애·다음다갈이 부작용이다 [[harrison-22: 327장 p.2433]].
- 선별 간격, 고위험 직업·수술 전 선별은 대조하지 않았다(검토 항목).

## 시험 쟁점 — 충돌·맥락·새 근거
- **Z1 맥락 · 가족력이 없으면 선별하는가** — 시험 기준: 동맥류·거미막하출혈 가족력이 있으면 MRA 선별 [[harrison-22: 327장 p.2432]] / 다른 기준: 해리슨은 가족력 없는 무증상 환자의 선별 역할이 불명확하다고 쓰고, 문항 해설은 지침이 고위험 직업·큰 수술 전 등으로 대상을 넓힌다고 적지만 원문을 대조하지 못했다 [[?kdigo-adpkd-2025]] / 왜 다른가: 작은 미파열 동맥류는 파열률이 낮고 예방 시술에 합병증이 있어 이득이 대상에 따라 다르다 [[harrison-22-sah: 440장 p.3458]] / 시험에서는: KMLE · USMLE 모두 「다낭신 + 가족력 + 무증상」 → MRA, 가족력이 없으면 MRA 를 일률 정답으로 두지 않는다.
- **Z2 충돌 · 톨밥탄은 승인된 치료인가** — 시험 기준: 빠른 진행 위험군에 톨밥탄 — FDA 가 그 환자에게만 적응을 두었다 [[harrison-22: 327장 p.2433]] / 다른 기준: 같은 쪽 치료 절 첫 문장은 낭종 성장·신기능 감소를 막는 FDA 승인 치료가 없다고 쓴다 [[harrison-22: 327장 p.2433]] / 왜 다른가: 같은 장 안의 서술이 어긋난다 — 옛 판 문장이 남은 것으로 보이나 확인하지 못했다 / 시험에서는: KMLE · USMLE 모두 빠른 진행 위험 다낭신의 진행 억제약은 톨밥탄(간기능 감시)으로 답한다.
- **Z3 새 근거 · 혈압 목표** — 시험 기준: 레닌-안지오텐신계 차단으로 혈압 조절 [[harrison-22: 327장 p.2433]] / 다른 기준: 해리슨은 JNC VIII 의 140/90 mmHg 를 목표로 들고 더 엄격한 조절이 더 이롭지 않다고 쓰면서, HALT PKD 에서 엄격한 조절이 낭종 성장을 늦췄다고도 쓴다 [[harrison-22: 327장 p.2433]]; KDIGO 2025 의 목표 수치는 원문을 대조하지 못했다 [[?kdigo-adpkd-2025]] / 왜 다른가: 나이·신기능(젊고 GFR 보존 vs 중등도 이상)에 따라 낮은 목표의 득실이 다르다 / 시험에서는: KMLE · USMLE 모두 약 선택(ACE 억제제·ARB)을 묻고, 목표 수치를 물으면 최신 지침 원문 확인이 필요하다.
