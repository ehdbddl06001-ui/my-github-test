---
id: cn.ortho.scaphoid-fracture.occult-imaging
type: concept
topic: Orthopedics
see_also: [Emergency Medicine, Radiology]
date: 2026-10-09
updated: 2026-10-09
version: 2
outline: ortho.upper-limb      # 정형외과 손 슬롯 「상지 골절과 탈구」(해리슨 대조 대상 아님)
confidence: medium
review_status: unreviewed
note_form: 2            # 판형 2(2026-09-25) — 결론·시험 단서·왜 → 혼동 → 표·도식 → 목표에 맞춘 본문
title: "잠복 주상골 골절 — 정상 X선이어도 엄지 포함 고정"
objective: "손을 짚고 넘어진 뒤 코담배갑 압통·엄지 축 방향 압박통이 있는데 첫 X선이 정상이면 잠복 주상골 골절로 보고 엄지 포함 부목으로 고정한 뒤 10~14일 뒤 재촬영(또는 MRI)함을 고른다"
objective_kind: 다음 처치
condition: 잠복 주상골 골절
exams: [kmle, usmle]
summary:
  - "결론: 코담배갑 압통이 있으면 첫 X선이 정상이어도 엄지 포함 부목 고정 → 10~14일 뒤 재촬영 또는 MRI."
  - "시험 단서: 손 짚고 넘어짐(FOOSH) + 해부학적 코담배갑(anatomical snuffbox) 압통·엄지 축 방향 압박통 + 정상 X선."
  - "왜: 전위 없는 주상골 골절선은 첫 X선에 안 보이고, 놓치면 역행성 혈류 때문에 불유합·무혈성 괴사가 생긴다."
  - "관혈적 정복·내고정은 전위(1 mm 초과)·근위부 골절이 영상으로 확인됐을 때만 — 확인 전에는 고정과 재평가다."
  - "압통이 코담배갑이 아니라 원위 요골 성장판 둘레면 Salter-Harris I 형 의심 — 단상지 고정 후 재평가."
criteria:
  - id: occult-scaphoid-suspicion
    name: 잠복 주상골 골절을 의심하는 조건
    kind: 진단 기준
    population: "손을 짚고 넘어진 뒤 손목 통증, 첫 X선 정상"
    statement: "코담배갑 압통 또는 엄지 축 방향 압박통이 있으면 정상 X선을 「골절 없음」으로 받아들이지 않고 잠복 골절로 다룬다 [[?campbell-14: Fractures and dislocations of the wrist — scaphoid]]"
    exceptions: "두 소견이 모두 없고 압통이 다른 곳(원위 요골 성장판 등)에 있으면 그 부위의 손상으로 판단한다"
    source: campbell-14
    basis: current
    exams: [kmle, usmle]
  - id: occult-scaphoid-management
    name: 첫 X선 정상인 의심 주상골 골절의 처치
    kind: 치료 기준
    population: "임상적으로 주상골 골절이 의심되나 첫 X선이 정상"
    statement: "엄지를 포함한 부목으로 고정하고 10~14일 뒤 다시 촬영하거나, 가능하면 MRI 로 확인한다 [[?acr-hand-wrist-2018]] [[?campbell-14: Fractures and dislocations of the wrist — scaphoid]]"
    exceptions: "MRI 를 바로 쓸 수 있으면 첫날에도 골수 부종으로 확인할 수 있다 — 재촬영과 MRI 의 선택 순서는 원문 미대조"
    source: acr-hand-wrist-2018
    basis: current
    exams: [kmle, usmle]
sources:
  - id: campbell-14
    org: "Elsevier"
    title: "Campbell's Operative Orthopaedics, 14th ed. — Fractures and dislocations of the wrist"
    kind: textbook
    year: 2021
    citation: "Azar FM, Beaty JH (eds). Campbell's Operative Orthopaedics, 14th ed. 장 'Fractures and dislocations of the wrist' — scaphoid fractures: occult fracture, immobilization, repeat imaging(쪽 미확인)"
    checked_at: 2026-10-09
    checked: "서지만(원문 미대조 — 검토 항목). 문항 imaging-2026-0263 해설의 근거 목록에서 옮겼고 이 컨테이너에서 교과서 본문을 열지 못했다"
    verified: citation
  - id: acr-hand-wrist-2018
    org: "American College of Radiology"
    title: "ACR Appropriateness Criteria: Acute Hand and Wrist Trauma (2018 update)"
    kind: guideline
    year: 2018
    citation: "American College of Radiology. ACR Appropriateness Criteria — Acute Hand and Wrist Trauma, 2018 update (suspected scaphoid fracture with normal radiographs)"
    url: "https://acsearch.acr.org/list"
    checked_at: 2026-10-09
    checked: "서지만(원문 미대조 — 검토 항목). 이 컨테이너는 PubMed·doi 접근이 막혀 원문·PMID 를 확인하지 못했다. PMID·DOI 를 기억으로 적지 않았다. url 은 ACR 적합성 기준 목록 쪽(주제 'Acute Hand and Wrist Trauma' 를 거기서 찾는다)"
    verified: citation
tables:
  - id: wrist-tenderness-site
    title: "손 짚고 넘어진 손목, X선 정상 — 압통 자리가 처치를 정한다"
    role: differential
    span: column
    section: "가르는 소견 — 압통 자리와 정상 X선의 한계"
    columns: ["압통 자리·소견", "의심", "처치"]
    rows:
      - ["코담배갑 압통 · 엄지 축 방향 압박통", "잠복 주상골 골절", "엄지 포함 부목 → 10~14일 뒤 재촬영 또는 MRI [[?campbell-14: Fractures and dislocations of the wrist — scaphoid]]"]
      - ["원위 요골 성장판 둘레 압통·부종(청소년)", "Salter-Harris I 형", "단상지 고정 후 재평가"]
      - ["국소 압통·압박통 없음", "단순 염좌·타박", "보호대·증상 조절, 활동 재개"]
    note: "모두 교과서·지침 원문 미대조(†)."
  - id: scaphoid-management-ladder
    title: "주상골 골절 — 영상 결과에 따른 처치"
    role: treatment
    span: column
    section: "선택 — 확인 전에는 고정, 확인 뒤에는 전위가 정한다"
    columns: ["영상", "처치", "이 처치가 틀리는 때"]
    rows:
      - ["첫 X선 정상 + 임상 의심", "엄지 포함 부목 → 재촬영·MRI", "압통·압박통이 없을 때(과잉 고정)"]
      - ["골절선 보임, 전위 없음", "엄지 포함 석고 고정", "전위·근위부 골절일 때"]
      - ["전위 1 mm 초과 또는 근위부 골절", "관혈적 정복·내고정", "골절이 아직 확인되지 않았을 때"]
      - ["재촬영·MRI 정상", "고정 풀고 활동 재개", "증상이 남으면 재평가"]
    note: "전위 기준 1 mm 는 문항 해설의 서술이며 원문 미대조(†)."
pitfalls:
  - contrast: "X선 정상이니 염좌 — 탄력붕대?"
    point: "탄력붕대와 증상에 맡기는 처치는 코담배갑 압통도 엄지 축 방향 압박통도 없는 단순 염좌의 선택이다. 전위 없는 주상골 골절선은 첫 X선에서 보이지 않는 일이 흔하므로, 두 소견이 있으면 정상 X선은 골절을 배제하지 못한다. 고정하지 않고 움직이면 불유합·무혈성 괴사 위험이 커진다 [[?campbell-14: Fractures and dislocations of the wrist — scaphoid]]."
    exception: "코담배갑 압통·압박통이 없고 다른 국소 압통도 없으면 탄력붕대·증상 조절이 맞다."
    covers: ["imaging-2026-0263:E"]
  - contrast: "주상골 의심 vs 원위 요골 성장판 손상"
    point: "청소년은 성장판이 열려 있어 성장판 손상을 먼저 떠올리기 쉽지만, 고정 범위와 확인 방법은 압통 자리가 정한다. 압통이 코담배갑이면 엄지까지 고정하고 주상골을 다시 본다. 성장판 손상이 의심돼도 장상지 석고 6주는 과하다."
    exception: "압통·부종이 원위 요골 성장판 둘레에 있고 코담배갑은 멀쩡하면 Salter-Harris I 형으로 보고 단상지 고정 후 재평가한다."
    covers: ["imaging-2026-0263:B"]
  - contrast: "주상골 의심이면 바로 수술?"
    point: "관혈적 정복·내고정은 영상에서 전위된(1 mm 초과) 골절이나 근위부 골절이 확인됐을 때의 치료다. 골절이 아직 보이지도 않은 단계에서는 고정하고 영상으로 확인하는 것이 먼저다."
    exception: "재촬영·CT·MRI 에서 전위된 허리 골절이나 근위부 골절이 확인되면 수술이 정답이 된다."
    covers: ["imaging-2026-0263:A"]
  - contrast: "진통제 후 바로 운동 복귀?"
    point: "운동 복귀는 숨은 골절을 배제한 뒤의 일이다. 주상골 골절을 고정 없이 움직이면 골절면이 계속 움직여 불유합으로 갈 수 있다."
    exception: "국소 압통·압박통이 전혀 없는 가벼운 타박이면 진통제와 활동 재개가 맞다."
    covers: ["imaging-2026-0263:C"]
diagram:
  title: "손 짚고 넘어진 손목 — X선이 정상일 때"
  nodes:
    - {id: start, kind: start, text: "손 짚고 넘어진 뒤 손목 통증"}
    - {id: snuff, kind: decision, text: "코담배갑 압통·엄지 축 압박통?"}
    - {id: physis, kind: decision, text: "원위 요골 성장판 압통?"}
    - {id: sh1, kind: end, text: "SH I 의심 → 단상지 고정 후 재평가"}
    - {id: sprain, kind: end, text: "염좌 — 보호대·증상 조절"}
    - {id: xr, kind: step, text: "손목 전후면·측면·주상골 X선"}
    - {id: read, kind: decision, text: "주상골 골절선이 보이는가?"}
    - {id: occult, kind: info, text: "잠복 골절 가능 — 정상 X선으로 배제 못 함"}
    - {id: spica, kind: step, text: "엄지 포함 부목 → 10~14일 뒤 재촬영·MRI"}
    - {id: recheck, kind: decision, text: "재촬영·MRI에서 골절?"}
    - {id: clear, kind: end, text: "골절 배제 — 고정 풀고 활동 재개"}
    - {id: disp, kind: decision, text: "전위 1 mm 초과·근위부 골절?"}
    - {id: orif, kind: end, text: "관혈적 정복·내고정"}
    - {id: cast, kind: end, text: "엄지 포함 석고 고정"}
  edges:
    - {from: start, to: snuff}
    - {from: snuff, to: xr, label: "있음"}
    - {from: snuff, to: physis, label: "없음"}
    - {from: physis, to: sh1, label: "있음"}
    - {from: physis, to: sprain, label: "없음"}
    - {from: xr, to: read}
    - {from: read, to: disp, label: "보임"}
    - {from: read, to: occult, label: "안 보임"}
    - {from: occult, to: spica}
    - {from: spica, to: recheck}
    - {from: recheck, to: disp, label: "골절 확인"}
    - {from: recheck, to: clear, label: "정상"}
    - {from: disp, to: orif, label: "예"}
    - {from: disp, to: cast, label: "아니오"}
diagram_notes:
  - "손가락 감각·모세혈관 재충만 이상이나 변형이 있으면 이 도식보다 전위된 골절·탈구에 대한 응급 처치가 우선이다."
  - "MRI 를 바로 쓸 수 있으면 첫날에도 골수 부종으로 골절을 확인할 수 있다 — 재촬영을 기다리지 않고 MRI 로 갈 수 있다."
  - "재촬영·MRI 가 정상이어도 압통이 계속되면 다시 평가한다."
  - "청소년도 성장판이 닫혀 가는 나이라 성인형 주상골 골절이 생긴다."
checks:
  - q: "손을 짚고 넘어진 뒤 코담배갑 압통이 있는데 첫 X선이 정상이면 다음 처치는?"
    a: "엄지 포함 부목으로 고정하고 10~14일 뒤 재촬영하거나 MRI 로 확인한다."
  - q: "주상골 골절이 첫 X선에 안 보이는 이유는?"
    a: "비스듬히 놓인 작은 뼈의 전위 없는 가는 골절선이라 겹쳐 보이지 않는다. 1~2주 뒤 골절선 가장자리가 흡수되어 드러난다."
  - q: "주상골 골절을 놓치면 왜 위험한가?"
    a: "혈류가 원위부에서 근위부로 역행하므로 허리·근위부 골절에서 근위 조각이 무혈성 괴사·불유합으로 갈 수 있다."
  - q: "주상골 골절에 관혈적 정복·내고정이 정답이 되는 조건은?"
    a: "영상에서 전위(1 mm 초과)된 골절이나 근위부 골절이 확인될 때."
variants:
  - id: v1
    of: imaging-2026-0263
    flip: true
    changed: "압통 자리를 「코담배갑 압통·엄지 축 방향 압박통」에서 「원위 요골 성장판 둘레 압통·부종, 코담배갑 압통과 엄지 압박통 없음」으로 바꿈 → 주상골이 아니라 Salter-Harris I 형 의심이 되어 답이 「엄지 포함 부목 후 재촬영」에서 「단상지 고정 후 재평가」로 바뀜"
    context: "단서를 바꿔 답이 바뀌는 변형 — 압통이 성장판 둘레"
    stem: "13세 남자가 어제 축구를 하다 넘어지며 왼손을 뻗어 바닥을 짚은 뒤 생긴 손목 통증으로 내원하였다. 진찰에서 원위 요골 성장판 둘레에 국소 압통과 경한 부종이 있으나 해부학적 코담배갑에는 압통이 없고, 엄지를 축 방향으로 밀어도 통증이 없다. 변형은 없고 손가락 감각과 모세혈관 재충만 시간은 정상이다. 손목 전후면·측면 X선에서 골절선·전위는 보이지 않고 성장판 폭도 정상이다. 다음 처치로 가장 적절한 것은?"
    choices: ["A. 엄지를 포함한 부목으로 고정하고 10~14일 뒤 주상골을 재촬영한다", "B. 단상지 고정을 하고 1~2주 뒤 다시 평가한다", "C. 관혈적 정복과 내고정을 한다", "D. 진통제만 주고 바로 운동에 복귀시킨다", "E. 장상지 석고로 6주 고정한다"]
    answer: "B"
    explanation: "압통이 코담배갑이 아니라 원위 요골 성장판 둘레에 있고 엄지 압박통도 없다. X선이 정상이어도 성장판 위 국소 압통은 전위 없는 Salter-Harris I 형을 배제하지 못하므로 단상지로 고정하고 1~2주 뒤 다시 본다. 엄지 포함 부목·주상골 재촬영은 코담배갑 압통이 있을 때, 수술은 전위된 골절이 확인됐을 때의 선택이고, 장상지 6주는 과하다. 원래 문항은 압통이 코담배갑에 있어 주상골을 다시 봐야 했다 — 「어디를 누를 때 아픈가」가 답을 가른다."
    kind: application
  - id: v2
    of: imaging-2026-0263
    flip: false
    changed: "나이·성별(24세 여자)·기전(빙판에서 미끄러짐)·손(왼쪽)·제시 순서를 바꾸고 「손 짚고 넘어짐·코담배갑 압통·엄지 축 방향 압박통·X선 정상」은 그대로 → 답은 여전히 엄지 포함 부목 고정 후 재촬영"
    context: "겉모습만 바꾸고 답은 같은 변형 — 성인, 빙판 낙상"
    stem: "24세 여자가 2일 전 빙판에서 미끄러지며 왼손을 짚은 뒤 손목 통증이 가라앉지 않아 내원하였다. 손목 전후면·측면과 주상골 사진에서 골절선·전위·연부조직 종창은 보이지 않았다. 진찰에서 엄지를 축 방향으로 밀면 통증이 심해지고, 해부학적 코담배갑에 뚜렷한 압통이 있다. 손가락 감각과 혈류는 정상이고 변형은 없다. 다음 처치로 가장 적절한 것은?"
    choices: ["A. 탄력붕대를 감고 증상이 남을 때만 다시 오게 한다", "B. 관혈적 정복과 내고정을 한다", "C. 엄지를 포함한 부목으로 고정하고 10~14일 뒤 재촬영한다", "D. 진통제를 주고 바로 일상 활동을 하게 한다", "E. 단상지 석고를 6주 한다"]
    answer: "C"
    explanation: "나이·기전·제시 순서가 달라도 결정 단서는 같다 — 손을 짚고 넘어진 뒤 코담배갑 압통과 엄지 축 방향 압박통이 있으면 정상 X선은 주상골 골절을 배제하지 못한다. 엄지까지 고정해 주상골의 움직임을 막고 10~14일 뒤 재촬영하거나 MRI 로 확인한다 [[?campbell-14: Fractures and dislocations of the wrist — scaphoid]]. 탄력붕대·진통제는 압통·압박통이 없는 염좌, 수술은 전위가 확인된 골절의 선택이고, 엄지를 빼고 6주를 고정하는 것은 확인 없이 기간만 정한 처치다."
    kind: application
figures:
- id: f1
  file: docs/assets/figures/graz-0663_0857365894_01_wri-r1_m014.jpg
  kind: radiograph
  at: 가르는 소견 — 압통 자리와 정상 X선의 한계
  shows: 골절이 보이지 않는 청소년 손목 전후면 X선 — 주상골 골절이 의심돼도 첫 X선은 이렇게 정상일 수 있다
  look_for:
  - 주상골 피질이 끊긴 곳 없이 이어진다
  - 원위 요골·척골 성장판이 열려 있다
  label: pediatric wrist radiograph without fracture
  label_basis: dataset_expert
  reference: 소아 손목 X선의 골절·골막반응 등을 전문가가 상자로 주석
  paper: Nagy E 외. A pediatric wrist trauma X-ray dataset (GRAZPEDWRI-DX) for machine learning. Sci Data 2022;9:222
  doi: 10.1038/s41597-022-01328-z
  credit: GRAZPEDWRI-DX (figshare, CC BY 4.0)
  license: Creative Commons Attribution 4.0 International
  url: https://figshare.com/articles/dataset/GRAZPEDWRI-DX/14825193
  asset: GRAZ-0663_0857365894_01_WRI-R1_M014
  paper_cited_by: 101
---

## 판단 — 왜 정상 X선이어도 엄지 포함 고정이 먼저인가
- 손을 짚고 넘어진 뒤 **해부학적 코담배갑(anatomical snuffbox) 압통**과 **엄지 축 방향 압박통**은 주상골(scaphoid) 골절을 의심하게 하는 진찰 소견이다 [[?campbell-14: Fractures and dislocations of the wrist — scaphoid]].
- 전위 없는 주상골 골절은 첫 X선에서 보이지 않는 일이 흔하다 — 정상 X선은 「골절 없음」이 아니다.
- 놓치고 움직이면 불유합(nonunion)·무혈성 괴사(avascular necrosis)로 갈 수 있으므로, 확인 전에는 **엄지 포함 부목(thumb spica splint)** 으로 고정하고 10~14일 뒤 재촬영하거나 MRI 로 확인한다 [[?acr-hand-wrist-2018]].
- 수술은 영상으로 전위·근위부 골절이 확인된 뒤의 선택이다.

## 기전 — 역행성 혈류에서 불유합으로
**정상**: 주상골은 근위·원위 손목뼈 줄을 잇는 막대처럼 비스듬히 놓여 있어, 손목을 뒤로 젖힌 채 손을 짚으면 요골 끝과 손바닥 사이에서 허리(중간부)에 굽힘 힘이 몰린다. 표면 대부분이 관절 연골이라 혈관이 들어올 자리가 좁고, 혈액은 주로 원위부(결절 쪽)에서 들어와 근위부로 **거꾸로** 흐른다.

**이상**: 허리나 근위부가 부러지면 근위 조각으로 가는 혈류가 끊긴다. 고정하지 않은 채 손목을 움직이면 골절면이 계속 움직여 붙지 못하고(불유합), 근위 조각은 무혈성 괴사에 빠진다. 불유합이 진행하면 손목뼈 배열이 무너지는 관절염(SNAC 손목, scaphoid nonunion advanced collapse)으로 이어진다.

**왜 첫 X선이 정상인가**: 비스듬히 놓인 작은 뼈의 전위 없는 골절선은 머리카락처럼 가늘어 전후면·측면에서 다른 뼈와 겹친다. 1~2주 지나면 골절선 가장자리가 흡수되어 넓어지므로 재촬영에서 드러난다. MRI 는 첫날에도 골수 부종으로 골절을 보여 준다.

## 가르는 소견 — 압통 자리와 정상 X선의 한계
- **압통 자리**가 의심 부위와 고정 범위를 정한다(표). 코담배갑·엄지 축 방향 압박통이면 엄지까지 고정하고 주상골을 다시 본다.
- **청소년**: 성장판이 열려 있어 원위 요골 성장판 손상(Salter-Harris I 형)을 떠올리기 쉽지만, 성장판 둘레에 압통·부종이 없으면 그쪽 가능성은 낮다. 이 나이에도 성인형 주상골 골절이 생긴다.
- **신경혈관 정상·변형 없음**은 응급 정복이 필요한 전위 골절·탈구가 아님을 보여 줄 뿐, 주상골 골절을 배제하지 않는다.
- **정상 X선의 한계**: 임상 의심이 있으면 정상 X선을 근거로 고정을 생략하지 않는다. 재촬영·MRI 가 정상이어야 배제한다.

## 선택 — 확인 전에는 고정, 확인 뒤에는 전위가 정한다
- **확인 전**: 엄지 포함 부목 고정 → 10~14일 뒤 재촬영, 가능하면 MRI [[?acr-hand-wrist-2018]].
- **골절 확인, 전위 없음**: 엄지 포함 석고 고정.
- **전위 1 mm 초과 또는 근위부 골절**: 관혈적 정복·내고정 [[?campbell-14: Fractures and dislocations of the wrist — scaphoid]].
- **재평가**: 재촬영·MRI 가 정상이면 고정을 풀고 활동을 재개한다. 압통이 계속되면 다시 평가한다.
- **하지 않는 것**: 확인 전 탄력붕대·진통제만으로 활동 복귀, 확인 전 수술 — 이유는 표 「주상골 골절 — 영상 결과에 따른 처치」.

## 권고와 예외
- 재촬영과 MRI 중 무엇을 먼저 쓸지(MRI 를 바로 쓸 수 있는가)는 기관 여건에 따라 다르다. ACR 적합성 기준의 세부 권고 순서는 원문을 대조하지 못했다(검토 항목). 문항의 정답 기준은 「엄지 포함 부목 → 10~14일 뒤 재촬영(또는 MRI)」이다.
- 전위 기준 1 mm 는 문항 해설의 서술이며 교과서 원문은 대조하지 못했다(검토 항목).
- 이 슬롯(ortho.upper-limb)은 해리슨이 다루지 않는 자리라 해리슨 대조 대상이 아니다. Campbell·ACR 은 서지만 남겼다(†).
