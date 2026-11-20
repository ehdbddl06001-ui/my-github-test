---
id: cn.ent.adult-neck-mass.malignancy-workup
type: concept
topic: Otorhinolaryngology
see_also: [Hematology & Oncology]
date: 2026-11-20
updated: 2026-11-20
version: 1
outline: ent.head-neck-tumor   # 기본틀 슬롯(content/outline/subjects.yaml) — 이비인후과 손 슬롯 「두경부 종양과 침샘 질환」
confidence: medium
review_status: unreviewed
note_form: 2            # 판형 2(2026-09-25) — 기본틀 빈 슬롯으로 쓴 정리본(오답 연결 없음)
title: "성인 목덩이 — 악성 위험이면 영상·세침흡인 먼저"
objective: "성인의 목덩이에서 악성 위험 소견(감염 병력 없이 2주 이상 지속 · 고정 · 단단함 · 1.5 cm 초과 · 피부 궤양)을 가려, 항생제로 지켜보지 않고 조영 CT/MRI 와 세침흡인검사로 진행하는 다음 검사를 고른다"
objective_kind: 검사 선택
condition: 성인 목덩이(adult neck mass) — 두경부 편평세포암 전이(metastatic head and neck squamous cell carcinoma) 배제
exams: [kmle, usmle]
figures_none: "검사 순서를 고르는 목표 — 영상 소견 판독이 시험 단서가 아니다"
summary:
  - "결론: 악성 위험이 높은 성인 목덩이는 조영 CT(또는 MRI)와 세침흡인검사(FNA)로 간다 — 절개 생검을 먼저 하지 않는다."
  - "시험 단서: 감염 병력 없이 2주 넘게 그대로인 목덩이, 고정·단단함·1.5 cm 초과, 흡연·음주, 쉰 목소리·연하곤란·귀 통증."
  - "왜: 성인의 지속 목덩이는 대부분 종양이고 악성이 가장 많다 — 처음이자 유일한 소견이 두경부암 전이일 수 있다."
  - "세균 감염 징후가 없으면 항생제를 일상적으로 주지 않는다 — 항생제를 계속하는 동안 조기 진단 기회를 잃는다."
  - "낭성 목덩이도 진단이 나올 때까지 양성으로 단정하지 않는다(HPV 관련 인두암 전이 가능)."
pitfalls:
  - contrast: "성인 목덩이 → 먼저 항생제 2주 써 보고 판단?"
    point: "세균 감염 증상·징후가 없으면 항생제를 일상적으로 처방하지 않는다. 항생제로 치료한 병변이 곧 줄지 않는데 항생제만 이어 가면 조기 진단 기회를 잃는다 [[pynnonen-neck-mass-2017: 반대 권고(항생제)]] [[harrison-22: 82장 p.611]]."
  - contrast: "진단이 안 나오면 곧바로 절개(개방) 생검?"
    point: "먼저 FNA 를 한다. FNA · 영상 · 추가 검사로도 진단이나 원발 부위가 안 나오면, 개방 생검 전에 마취하 상부 호흡소화관 검사를 한다 — 숨은 원발 부위를 찾아 생검하는 것이 먼저다 [[pynnonen-neck-mass-2017: KAS 7, KAS 10]]."
  - contrast: "낭성 덩어리 = 아가미틈 낭종(양성)?"
    point: "악성 위험이 있는 성인의 낭성 목덩이는 FNA · 영상에서 낭성으로 보여도 진단이 나올 때까지 계속 평가하고 양성으로 단정하지 않는다 [[pynnonen-neck-mass-2017: KAS 8]]."
  - contrast: "목덩이 영상 = 초음파면 충분?"
    point: "악성 위험이 높은 목덩이의 영상은 조영 증강 목 CT 또는 MRI 가 강한 권고다 — 원발 부위·병기까지 본다 [[pynnonen-neck-mass-2017: 강한 권고(영상)]] [[harrison-22: 82장 p.611]]."
  - contrast: "목덩이만 만지고 영상으로 넘어간다?"
    point: "악성 위험이 높으면 후두 · 혀뿌리 · 인두 점막을 직접 보는 표적 진찰을 한다(직접 하거나 의뢰) — 원발 병변이 여기서 보일 수 있다 [[pynnonen-neck-mass-2017: KAS 6]]."
tables:
  - id: risk
    section: "가르는 소견 — 악성 위험이 높은 목덩이"
    title: "악성 위험을 올리는 소견"
    role: differential
    span: column
    columns: ["어디서", "소견", "근거"]
    rows:
      - ["병력 — 경과", "감염 원인 병력이 없고 2주 이상 크기 변동 없이 지속, 또는 기간 불명", "[[pynnonen-neck-mass-2017: KAS 1]]"]
      - ["진찰 — 덩어리", "하나 이상: 주위 조직에 고정 · 단단함 · 크기 >1.5 cm · 덮인 피부 궤양", "[[pynnonen-neck-mass-2017: KAS 2]]"]
      - ["병력 — 위험 요인", "흡연 · 음주(함께면 상승 작용) · 무연 담배, HPV(구인두 — 40~50대) · EBV(비인두)", "[[harrison-22: 82장 p.610~611]]"]
      - ["병력 — 동반 증상", "2–4주 넘게 지속하는 두경부 증상 · 쉰 목소리 · 연하곤란 · 연하통 · 귀 통증 · 한쪽 장액성 중이염 · 코막힘 · 코피(비인두)", "[[harrison-22: 82장 p.611]]"]
    note: "가이드라인 KAS 3 은 「그 밖의 의심 소견」을 병력 · 진찰로 찾으라고만 적는다(초록) — 위험 요인 · 동반 증상 줄은 해리슨 22판 82장에서 가져왔다."
  - id: workup
    section: "선택 — 영상, FNA, 그다음"
    title: "악성 위험이 높을 때 검사 순서"
    role: tests
    span: column
    columns: ["순서", "검사", "주의"]
    rows:
      - ["1", "표적 진찰 — 후두 · 혀뿌리 · 인두 점막 [[pynnonen-neck-mass-2017: KAS 6]]", "환자에게 위험이 높다는 뜻과 검사를 설명한다 [[pynnonen-neck-mass-2017: KAS 5]]"]
      - ["2", "조영 증강 목 CT 또는 MRI [[pynnonen-neck-mass-2017: 강한 권고(영상)]]", "림프절 침범이면 흉부 · 상복부 CT, PET 으로 원격 전이 [[harrison-22: 82장 p.611]]"]
      - ["3", "FNA — 개방 생검 대신 [[pynnonen-neck-mass-2017: KAS 7]]", "낭성이어도 진단까지 평가 지속 [[pynnonen-neck-mass-2017: KAS 8]]"]
      - ["4", "진단이 안 나오면 병력 · 진찰에 맞춘 추가 검사 [[pynnonen-neck-mass-2017: KAS 9]]", "—"]
      - ["5", "마취하 상부 호흡소화관 검사(내시경 · 표적 생검) — 개방 생검 전에 [[pynnonen-neck-mass-2017: KAS 10]]", "편평세포암이면 비인두 · 편도 · 혀뿌리 · 이상와를 표적 생검 [[harrison-22: 82장 p.612]]"]
criteria:
  - id: high-risk
    name: 악성 위험이 높은 성인 목덩이(AAO-HNSF 2017)
    kind: 분류
    population: "18세 이상, 목덩이"
    statement: "① 감염 원인 병력이 없고 2주 이상 크기 변동 없이 지속(또는 기간 불명), 또는 ② 진찰에서 고정 · 단단함 · >1.5 cm · 피부 궤양 중 하나 이상 — 그 밖의 의심 소견은 병력 · 진찰로 찾는다 [[pynnonen-neck-mass-2017: KAS 1, KAS 2, KAS 3]]"
    exceptions: "소아에는 적용하지 않는다. 갑상선 · 침샘 · 하악 · 치성 기원이 확실한 덩어리의 관리는 이 지침 범위 밖이다 [[pynnonen-neck-mass-2017: Purpose]]"
    source: pynnonen-neck-mass-2017
    basis: current
    exams: [kmle, usmle]
sources:
  - id: pynnonen-neck-mass-2017
    org: "AAO-HNSF (Pynnonen MA, Gillespie MB, Roman B, et al.)"
    title: "Clinical Practice Guideline: Evaluation of the Neck Mass in Adults"
    kind: guideline
    year: 2017
    citation: "Otolaryngol Head Neck Surg 2017;157(2_suppl):S1-S30"
    doi: "10.1177/0194599817722550"
    pmid: "28891406"
    checked_at: 2026-11-20
    checked: "PubMed 초록(PMID 28891406)의 목적 · 범위와 행동 지침 전부를 읽음 — 성인 지속 목덩이는 대부분 종양이고 악성이 가장 많음 · 증상 없는 목덩이가 두경부암의 첫 · 유일 소견일 수 있음; 강한 권고: 악성 위험이 높으면 조영 목 CT(또는 MRI); KAS 1(감염 병력 없음 + ≥2주 변동 없이 지속 또는 기간 불명) · 2(고정 · 단단함 · >1.5 cm · 피부 궤양) · 3(병력 · 진찰로 기타 의심 소견) · 4(저위험은 재평가 기준 설명 · 추적 계획 기록) · 5(위험 설명) · 6(후두 · 혀뿌리 · 인두 표적 진찰) · 7(개방 생검 대신 FNA) · 8(낭성도 진단까지) · 9(추가 검사) · 10(개방 생검 전 마취하 상부 호흡소화관 검사); 반대 권고: 세균 감염 징후 없으면 일상적 항생제 금지; 18세 미만 · 갑상선 · 침샘 · 하악 · 치성 기원 관리는 범위 밖. 요약판(PMID 28891424)은 초록만. 전문은 접근하지 못해(PMC 없음) KAS 근거 본문은 대조하지 않았다"
    verified: abstract
  - id: harrison-22
    org: "McGraw Hill"
    title: "Harrison's Principles of Internal Medicine, 22nd ed."
    kind: textbook
    year: 2025
    citation: "82장 Head and Neck Cancer(Vokes EE), 인쇄쪽 610~614"
    checked_at: 2026-11-20
    checked: "드라이브 22판 82장 문서(H22 p.610~614) 전부 읽음 — 위험 요인(흡연 · 음주 상승 작용, 무연 담배, EBV-비인두, HPV-구인두 · 40~50대), 증상이 2–4주 넘으면 이비인후과 진찰, 항생제로 낫지 않는 병변에 항생제만 이어 가면 조기 진단 기회 상실(p.611), 비인두암 증상(한쪽 장액성 중이염 · 코막힘 · 코피), HPV 종양은 목 림프절이 첫 소견, 원발 불명 경부 림프절(그림 82-1 — FNA 또는 림프절 절제, 편평세포암이면 범내시경 · 표적 생검), CT/MRI · 흉부 CT · PET 병기, 쇄골위 림프절은 흉부 · 복부 원발 가능(p.611~612), 침샘 종양 — 귀밑샘은 대부분 양성 · 턱밑 · 혀밑샘은 절반 · 소침샘은 대부분 악성(p.610)"
    verified: text
diagram:
  title: "성인 목덩이 — 위험 가르기에서 진단까지"
  nodes:
    - {id: start, kind: start, text: "성인 목덩이"}
    - {id: infect, kind: decision, text: "세균 감염 증상·징후?"}
    - {id: abx, kind: step, text: "감염 치료 · 짧게 재평가"}
    - {id: gone, kind: decision, text: "덩어리 소실?"}
    - {id: obs, kind: end, text: "재평가 기준 설명 · 추적 계획"}
    - {id: risk, kind: decision, text: "악성 위험 높음?"}
    - {id: exam, kind: step, text: "후두 · 혀뿌리 · 인두 표적 진찰"}
    - {id: ct, kind: step, text: "조영 목 CT 또는 MRI → FNA"}
    - {id: dx, kind: decision, text: "진단 · 원발 부위 나옴?"}
    - {id: treat, kind: end, text: "두경부암 전문의 — 병기 · 치료"}
    - {id: more, kind: info, text: "병력 · 진찰에 맞춘 추가 검사"}
    - {id: eua, kind: alert, text: "마취하 내시경 · 표적 생검 → 그다음 개방 생검"}
  edges:
    - {from: start, to: infect}
    - {from: infect, to: abx, label: "있음"}
    - {from: infect, to: risk, label: "없음"}
    - {from: abx, to: gone}
    - {from: gone, to: obs, label: "예"}
    - {from: gone, to: risk, label: "아니오"}
    - {from: risk, to: obs, label: "아니오"}
    - {from: risk, to: exam, label: "예"}
    - {from: exam, to: ct}
    - {from: ct, to: dx}
    - {from: dx, to: treat, label: "예"}
    - {from: dx, to: more, label: "아니오"}
    - {from: more, to: eua}
diagram_notes:
  - "「악성 위험 높음」은 기준 칸(감염 병력 없이 ≥2주 지속 · 기간 불명, 또는 고정 · 단단함 · >1.5 cm · 피부 궤양 중 하나)과 병력의 의심 소견으로 정한다 [[pynnonen-neck-mass-2017: KAS 1, KAS 2, KAS 3]]."
  - "위험이 높지 않아도 끝이 아니다 — 다시 와야 할 기준을 알려 주고 소실 또는 최종 진단을 확인할 추적 계획을 기록한다 [[pynnonen-neck-mass-2017: KAS 4]]."
  - "FNA · 영상에서 낭성이어도 진단이 나올 때까지 평가를 이어 간다 [[pynnonen-neck-mass-2017: KAS 8]]."
  - "「감염 치료 · 짧게 재평가」 칸의 재평가 간격은 지침 초록에 수치가 없다 — 항생제로 곧 줄지 않으면 악성 평가로 넘어간다 [[harrison-22: 82장 p.611]]."
checks:
  - q: "58세 흡연자, 3주째 그대로인 단단한 2.5 cm 목덩이, 발열 · 통증 없음. 다음 검사는?"
    a: "후두 · 혀뿌리 · 인두 표적 진찰과 조영 목 CT(또는 MRI), 그리고 FNA. 항생제 시험 치료나 절개 생검을 먼저 하지 않는다."
  - q: "FNA · CT · 추가 검사로도 진단과 원발 부위가 안 나왔다. 개방 생검 전에 할 것은?"
    a: "마취하 상부 호흡소화관 검사(범내시경 · 비인두 · 편도 · 혀뿌리 · 이상와 표적 생검)."
  - q: "45세 비흡연자의 목에 낭성 덩어리가 있다. 아가미틈 낭종으로 보고 끝내도 되나?"
    a: "안 된다. 악성 위험이 있는 성인의 낭성 목덩이는 진단이 나올 때까지 평가한다 — HPV 관련 구인두암은 목 림프절이 첫 소견일 수 있다."
---

## 판단 — 왜 항생제 관찰이 아니라 영상·FNA 인가
- 소아의 목덩이는 대부분 감염이지만 **성인의 지속 목덩이는 대부분 종양이고 악성이 가장 많다** — 증상 없는 덩어리가 두경부 편평세포암(head and neck squamous cell carcinoma, HNSCC) · 림프종 · 갑상선암 · 침샘암의 첫 소견일 수 있다 [[pynnonen-neck-mass-2017: Objective]].
- 전이성 두경부암은 진단이 늦어지면 병기가 올라가 예후가 나빠진다. 그래서 위험이 높으면 바로 **조영 CT/MRI**(강한 권고)와 **FNA** 로 간다 [[pynnonen-neck-mass-2017: 강한 권고(영상), KAS 7]].
- 세균 감염 징후가 없으면 항생제를 일상적으로 주지 않는다 [[pynnonen-neck-mass-2017: 반대 권고(항생제)]]. 항생제로 곧 낫지 않는 병변에 항생제만 이어 가면 조기 진단 기회를 잃는다 [[harrison-22: 82장 p.611]].
- 절개 생검보다 FNA 가 먼저인 이유: 원발 부위를 찾는 검사(표적 진찰 · 영상 · 마취하 내시경)가 남아 있을 때 목을 먼저 열지 않는다 — 지침은 개방 생검 전 마취하 상부 호흡소화관 검사를 권한다 [[pynnonen-neck-mass-2017: KAS 7, KAS 10]].

## 기전 — 점막 암에서 목 림프절로
- 두경부 상피암은 부비동 · 구강 · 비인두 · 구인두 · 하인두 · 후두 점막에서 생기는 편평세포암이 대부분이다. 흡연과 음주는 상승 작용을 하는 가장 큰 환경 요인이고, EBV 는 비인두암, HPV-16 은 구인두(편도 · 혀뿌리)암과 연관된다 [[harrison-22: 82장 p.610]].
- 구인두 · 하인두암은 초기에 증상이 거의 없고, HPV 관련 종양은 **목 림프절 비대가 첫 소견**인 경우가 많다 — 원발 병변이 작아 진찰 · 내시경에서 안 보일 수 있다(원발 불명암) [[harrison-22: 82장 p.611~612]].
- 위쪽 목 림프절의 편평세포암은 두경부 점막에서 왔을 가능성이 높고, 쇄골위 림프절은 흉부 · 복부 원발일 수도 있다 [[harrison-22: 82장 p.611]].

## 가르는 소견 — 악성 위험이 높은 목덩이
- 표가 지침의 두 기준(경과 · 진찰)과 해리슨의 위험 요인 · 동반 증상을 나란히 놓는다.
- 위험이 높지 않다고 판정해도 재평가 기준을 알려 주고 추적 계획을 남긴다 — 「낮음」은 배제가 아니다 [[pynnonen-neck-mass-2017: KAS 4]].
- 침샘 덩어리는 위치가 악성 가능성을 바꾼다 — 귀밑샘 종양은 대부분 양성, 턱밑 · 혀밑샘은 절반, 소침샘은 대부분 악성이다 [[harrison-22: 82장 p.610]].

## 선택 — 영상, FNA, 그다음
- 표가 다섯 단계를 순서대로 놓는다. 영상은 원발 부위와 범위를, FNA 는 조직 진단을 준다.
- FNA 가 편평세포암이면 범내시경(panendoscopy)으로 의심 부위와 흔한 원발 부위(비인두 · 편도 · 혀뿌리 · 이상와)를 생검한다 [[harrison-22: 82장 p.612]]. 림프절 침범이 있으면 흉부 · 상복부 CT 로 원격 전이와 둘째 원발 폐암을 본다 [[harrison-22: 82장 p.611]].
- 진단이 나오지 않으면 병력 · 진찰에 맞춘 추가 검사 → 마취하 상부 호흡소화관 검사 → 그다음에 개방 생검 [[pynnonen-neck-mass-2017: KAS 9, KAS 10]].

## 권고와 예외
- 이 지침은 18세 이상에만 적용한다. 갑상선 · 침샘 · 하악 · 치성 기원으로 확인된 덩어리의 관리, 진단 뒤 치료는 범위 밖이다 [[pynnonen-neck-mass-2017: Purpose]].
- 백반증(leukoplakia) · 홍반증(erythroplakia)은 이형성 · 상피내암일 수 있어 생검한다 [[harrison-22: 82장 p.611]].
- 국내 교과서 · KMLE 해설의 검사 순서 문구는 대조하지 않았다(검토 항목).

## 시험 쟁점 — 충돌·맥락·새 근거
- **Z1 충돌 · 원발 불명 목 림프절 — FNA 만인가, 절제도 되나** — 시험 기준: 악성 위험 목덩이는 개방 생검 대신 FNA, 개방 생검은 마취하 상부 호흡소화관 검사 뒤 [[pynnonen-neck-mass-2017: KAS 7, KAS 10]] / 다른 기준: 해리슨 22판은 원발이 안 보이는 림프절 침범에서 FNA 또는 림프절 절제(특히 한 개만 침범해 보일 때)로 진단한다고 적는다 [[harrison-22: 82장 p.612]] / 왜 다른가: 지침은 첫 진료의(1차 · 응급 · 치과)가 할 「첫 조직 검사」를 정하고, 해리슨 그림 82-1 은 종양 전문의의 진단 경로(림프종 · 육종 감별 포함)를 그린다 / 시험에서는: KMLE 는 국내 교과서와 대조하지 않았다(검토 항목) · USMLE 의 다음 검사 문항은 FNA 를 고른다(내 판단 — 지침 기준).
