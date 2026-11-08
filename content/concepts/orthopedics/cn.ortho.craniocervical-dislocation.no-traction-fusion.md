---
id: cn.ortho.craniocervical-dislocation.no-traction-fusion
type: concept
topic: Orthopedics
see_also: [Emergency Medicine, Neurosurgery]
date: 2026-11-09
updated: 2026-11-09
version: 2
outline: ortho.spine      # 정형외과 손 슬롯 「척추 — 추간판 탈출·협착·척추 골절」(해리슨 대조 대상 아님 — 경추 외상 고정·영상·연성 보호대 서술만 해리슨 22판 19장으로 확인)
confidence: medium
review_status: unreviewed
note_form: 2
title: "두개경추 탈구 — 견인하지 말고 고정 후 유합"
objective: "경추 측면 X선에서 기저-치돌기 간격이 크게 벌어진 두개경추 탈구를 읽고, 견인·연성 보호대를 피해 엄격한 고정과 후두골-경추 유합술을 고른다"
objective_kind: 다음 처치
condition: 두개경추 탈구(craniocervical dislocation) · 고리뒤통수 탈구(atlanto-occipital dislocation)
exams: [kmle, usmle]
summary:
  - "결론: 기저-치돌기 간격이 크게 벌어진 두개경추 탈구는 견인 없이 엄격히 고정하고 후두골-경추 유합술을 한다."
  - "시험 단서: 고속 감속 손상 + 경추 측면에서 기저(basion)가 치돌기 끝보다 훨씬 위 + 척추앞 연부조직 부종."
  - "왜: 손상이 뼈가 아닌 인대(덮개막·날개인대)의 세로 분리라 견인은 분리를 키우고 인대는 저절로 붙지 않는다."
  - "신경 진찰이 정상이어도 불안정 손상이다 — 보호대를 풀거나 연성 보호대로 바꾸지 않는다."
  - "견인 정복이 맞는 것은 의식이 명료한 아래 경추 관절돌기 탈구 — 방향이 세로가 아니라 앞으로 미끄러짐."
pitfalls:
  - contrast: "신경 정상 = 연성 보호대로 충분?"
    point: "연성 보호대는 불안정 손상이 없는 급성 목 통증에서 움직임을 줄여 통증을 덜 뿐이다 [[harrison-22: 19장 p.132]]. 외상성 경추 골절·탈구는 불안정성으로 인한 추가 척수 손상을 막도록 고정이 필수다 [[harrison-22: 19장 p.132]]. 두개경추 탈구는 인대가 끊긴 세로 분리라 신경 진찰이 정상이어도 작은 움직임으로 연수·위쪽 척수가 늘어난다 — 「정복」할 대상도 아니고 보호대를 바꿀 대상도 아니다 [[?bellabarba-2006]]."
    exception: "X선·CT 에 골절·탈구가 없고 신경 정상인 근육 염좌라면 연성 보호대·진통제가 맞다 [[harrison-22: 19장 p.132]]."
    cites: ["harrison-22: 19장 p.132", "?bellabarba-2006"]
    covers: ["imaging-2026-0575:B"]
  - contrast: "탈구면 견인 vs 두개경추 탈구"
    point: "견인은 관절돌기가 걸려 앞으로 미끄러진 아래 경추 탈구를 되돌리는 방법이다. 두개경추 탈구는 머리뼈가 경추에서 위로 떨어진 세로 분리라, 견인하면 간격이 더 벌어진다 [[?bellabarba-2006]]."
    cites: ["?bellabarba-2006"]
  - contrast: "굴곡·신전 X선으로 불안정성 확인?"
    point: "굴곡·신전 X선은 불안정성을 선별하는 검사다 [[harrison-22: 19장 p.130]]. 이미 탈구가 보이는 환자에게 목을 굽히고 펴게 하면 그 자체가 손상을 키운다 — 명백한 탈구에서는 하지 않는다."
    cites: ["harrison-22: 19장 p.130"]
tables:
  - id: traction-or-not
    section: "가르는 소견 — 분리 방향이 처치를 정한다"
    title: "경추 탈구 — 견인할 것과 하지 말 것"
    role: treatment
    span: column
    columns: ["손상", "X선", "처치"]
    rows:
      - ["두개경추 탈구", "기저-치돌기 간격 확대(세로 분리), 척추앞 부종", "견인 금기 · 엄격한 고정 → 후두골-경추 유합술 [[?bellabarba-2006]]"]
      - ["아래 경추 관절돌기 탈구", "척추체가 앞으로 미끄러짐, 관절돌기 걸림", "의식 명료하면 두개골 집게 견인으로 정복 → 고정 [[?atls-10]]"]
      - ["근육 염좌(골절·탈구 없음)", "정상", "진통제, 필요하면 연성 보호대 [[harrison-22: 19장 p.132]]"]
diagram:
  title: "목 외상 측면 X선 — 견인할까"
  nodes:
    - {id: start, kind: start, text: "고에너지 외상, 경추 보호대 착용"}
    - {id: unstable, kind: decision, text: "골절·탈구가 보이나?"}
    - {id: ct, kind: info, text: "CT 로 골절, MRI 로 인대·척수"}
    - {id: sprain, kind: end, text: "염좌 — 진통제·연성 보호대"}
    - {id: dir, kind: decision, text: "분리 방향은?"}
    - {id: occ, kind: end, text: "고정 유지 → 후두골-경추 유합술"}
    - {id: facet, kind: end, text: "두개골 집게 견인으로 정복"}
  edges:
    - {from: start, to: unstable}
    - {from: unstable, to: dir, label: "예"}
    - {from: unstable, to: sprain, label: "아니오"}
    - {from: unstable, to: ct, label: "애매"}
    - {from: ct, to: dir, label: "손상 확인"}
    - {from: ct, to: sprain, label: "정상"}
    - {from: dir, to: occ, label: "세로(기저-치돌기)"}
    - {from: dir, to: facet, label: "앞 미끄러짐"}
diagram_notes:
  - "외상성 경추 골절·탈구는 영상 전부터 목을 고정한다 — 불안정 분절로 인한 추가 척수 손상을 막는다 [[harrison-22: 19장 p.132]]."
  - "골절은 CT, 척수·인대는 MRI — CT 는 연부조직을 잘 보지 못한다 [[harrison-22: 19장 p.130]]."
  - "견인 정복은 의식이 명료해 신경 변화를 바로 말할 수 있는 환자에서만 한다 [[?atls-10]]."
  - "명백한 탈구에서 굴곡·신전 X선은 찍지 않는다."
checks:
  - q: "기저-치돌기 간격이 크게 벌어진 경추 측면 X선, 신경 정상. 다음 처치는?"
    a: "견인하지 않고 엄격히 고정한 채 후두골-경추 유합술을 준비한다."
  - q: "두개경추 탈구에서 견인이 금기인 이유는?"
    a: "인대가 끊긴 세로 분리라 견인이 간격을 더 벌려 연수·위쪽 척수를 늘린다."
sources:
  - id: harrison-22
    org: "McGraw Hill"
    title: "Harrison's Principles of Internal Medicine, 22nd ed. — Chapter 19: Neck Pain"
    kind: textbook
    year: 2025
    citation: "Harrison's Principles of Internal Medicine, 22e. 19장 p.129–133"
    checked_at: 2026-11-09
    checked: "드라이브 H22_019 문서 대조 — p.130: 경추 X선(전후·측면·굴곡-신전)은 골절·불안정성 선별, 골절 의심 시 CT, CT 는 연부조직이 잘 안 보여 척수 평가에 부적합, MRI 가 연부조직 표준. p.132: 외상성 경추 골절·탈구는 척수 손상이 동반되면 생명을 위협하고 불안정성으로 인한 추가 손상을 막도록 목 고정이 필수 · 신경 소견 없는 급성 목 통증에 연성 보호대가 일부에서 통증을 덜어 줌. 두개경추 탈구의 진단 기준·치료는 이 장에 없다"
    verified: text
  - id: bellabarba-2006
    org: "J Neurosurg Spine"
    title: "Diagnosis and treatment of craniocervical dislocation in a series of 17 consecutive survivors during an 8-year period"
    kind: other
    year: 2006
    citation: "Bellabarba C, Mirza SK, West GA, et al. J Neurosurg Spine. 2006;4(6):429-440"
    doi: "10.3171/spi.2006.4.6.429"
    checked_at: 2026-11-09
    checked: "서지만(원문 미대조 — 검토 항목). 문항 해설의 근거 목록에서 옮겼고 이 컨테이너는 PubMed·doi 접근이 막혀 초록을 열지 못했다. PMID 미확인, DOI 는 기억으로 적은 값(학술지 DOI 형식) — 학습서 워크플로가 확인한다"
    verified: citation
  - id: atls-10
    org: "American College of Surgeons"
    title: "ATLS Advanced Trauma Life Support, 10th ed. — Spine and Spinal Cord Trauma"
    kind: textbook
    year: 2018
    citation: "American College of Surgeons. ATLS Student Course Manual, 10th ed. Ch. Spine and Spinal Cord Trauma(쪽 미확인)"
    checked_at: 2026-11-09
    checked: "서지만(원문 미대조 — 검토 항목). 문항 해설의 근거 목록에서 옮겼다"
    verified: citation
variants:
  - id: v1
    of: imaging-2026-0575
    flip: true
    changed: "기저-치돌기 간격 확대(세로 분리) → C5 척추체가 C6 위로 앞으로 절반 넘게 미끄러진 양쪽 관절돌기 탈구, 의식 명료 ⇒ 정답이 후두골-경추 유합술 준비에서 두개골 집게 견인 정복으로"
    context: "같은 교통사고 상황, 소견을 글로 바꾼 변형(그림 없음)"
    stem: "34세 남자가 승용차 운전 중 정면 충돌 사고를 당해 응급실로 이송되었다. 경추 보호대를 한 상태이며 목이 아프고 양손이 저리다고 한다. 의식은 명료하고 질문에 정확히 답한다. 혈압 124/78 mmHg, 맥박 88회/분, 호흡 18회/분이다. 양쪽 손가락 벌림 근력이 약간 떨어져 있고 하지 근력과 항문 괄약근 긴장도는 정상이다. 경추 측면 단순 X선에서 기저와 치돌기 끝의 간격은 정상이고, C5 척추체가 C6 위로 앞쪽으로 척추체 앞뒤 길이의 절반 넘게 미끄러져 있으며 양쪽 관절돌기가 서로 걸려 있다. 가장 적절한 처치는?"
    choices: ["A. 의식이 명료한 상태에서 두개골 집게로 경추 견인을 시작한다", "B. 도수 정복 후 연성 경추 보호대로 바꾼다", "C. 보호대를 풀고 굴곡·신전 X선을 찍는다", "D. 고용량 메틸프레드니솔론만 정맥 투여한다", "E. 견인 없이 후두골-경추 유합술을 준비한다"]
    answer: "A"
    explanation: "이번에는 두개경추 부위가 정상이고 아래 경추에서 척추체가 앞으로 미끄러진 양쪽 관절돌기 탈구다. 방향이 세로 분리가 아니라 앞 미끄러짐이라, 의식이 명료해 신경 변화를 바로 말할 수 있는 환자에서는 두개골 집게 견인으로 걸린 관절돌기를 풀어 정복한다. 원래 문항은 기저-치돌기 간격이 벌어진 세로 분리라 견인이 금기였다. 굴곡·신전 X선과 연성 보호대는 불안정 손상에서 위험하다."
    kind: application
  - id: v2
    of: imaging-2026-0575
    flip: false
    changed: "21세 여자 조수석 정면 충돌·X선 그림 → 45세 남자 오토바이 추락·소견을 글로 제시 ⇒ 기저-치돌기 간격 확대·척추앞 연부조직 부종·신경 정상이라는 결정 단서는 같아 답은 그대로 견인 없이 고정·유합술"
    context: "겉모습만 바꾼 글 변형(그림 없음)"
    stem: "45세 남자가 오토바이를 타다 넘어지며 머리부터 땅에 부딪혀 응급실로 이송되었다. 헬멧을 쓰고 있었고 경추 보호대를 한 상태이며 뒷목이 아프다고 한다. 의식은 명료하다. 혈압 130/80 mmHg, 맥박 96회/분, 호흡 18회/분이다. 사지의 근력·감각과 항문 괄약근 긴장도는 정상이다. 경추 측면 단순 X선에서 머리뼈 기저와 치돌기 끝 사이 간격이 정상보다 크게 넓어져 기저가 치돌기보다 훨씬 위에 있고 척추앞 연부조직이 두꺼워져 있다. 아래 경추 정렬은 정상이다. 가장 적절한 처치는?"
    choices: ["A. 보호대를 풀고 굴곡·신전 X선을 찍는다", "B. 경추를 엄격히 고정한 채 후두골-경추 유합술을 준비한다", "C. 두개골 집게로 경추 견인을 시작한다", "D. 신경 결손이 없으므로 연성 경추 보호대로 바꾸고 퇴원시킨다", "E. 고용량 메틸프레드니솔론을 정맥 투여한다"]
    answer: "B"
    explanation: "사고 기전과 환자가 바뀌었지만 결정 단서는 같다 — 기저-치돌기 간격이 크게 벌어진 세로 분리(두개경추 탈구)와 척추앞 부종. 인대 손상이라 저절로 붙지 않고 견인은 간격을 더 벌린다. 신경 진찰이 정상이어도 불안정 손상이므로 엄격히 고정하고 후두골-경추 유합술을 준비한다. 연성 보호대·굴곡-신전 촬영은 추가 척수 손상을 부른다."
    kind: application
figures:
- id: f1
  file: docs/assets/figures/pmc-pmc6946329_figure2_a.jpg
  kind: radiograph
  at: 기전 — 인대가 끊긴 세로 분리에서 척수 신장으로
  shows: 외상성 고리뒤통수·고리중쇠 세로 탈구 — 기저-치돌기 간격 확대와 고리뼈 앞고리 골절 조각
  look_for:
  - '가는 화살표: 치돌기 끝보다 훨씬 위에 떨어진 기저'
  - '굵은 화살표: 고리뼈 앞고리의 골절 조각'
  label: '「Lateral radiograph of the cervical spine revealed increased soft tissue swelling, horizontal split fracture of the anterior arch of the atlas (thick arrow), and increased basion-dental interval of 24 mm (arrow) (A). Sagittal MRI revealed complete rupture of the ligamentous complex (white arrows) and severe intramedullary cord hemorrhage at the occipito-cervical junction (thick arrow) (B). Coronal 2-D CT revealed vertical displacement of the occipital condyles (asterisks), and increased atlanto-axial joints (dotted arrows) (C). Sagittal 2-D CT revealed horizontal split fracture of the anterior arch of the atlas (thick arrows), increased atlanto-axial joints (dotted arrows), and increased basion-dental interval of 24 mm (arrow) (D). Axial CT revealed 2-part fracture of the atlas, including anterior arch fracture (thick arrow) and posterior arch fracture (arrow) (E and F). Parasagittal 2-D CT scans demonstrated vertical displacement of the occipital condyles (asterisks) with respect
    to the lateral mass of the atlas and posterior arch fracture of the atlas (arrowhead) (G and H). At 1 year post-surgery, plain radiographs of the cervical spine revealed solid fusion of the occipitocervical junction (I and J).」 — Traumatic combined vertical atlanto-occipital and atlanto-axial dislocations with 2-part fracture of the atlas: Two case reports'
  label_basis: published_figure
  reference: 동료 심사 논문의 그림 설명(저자가 그 소견이라고 쓴 그림)
  paper: 'Traumatic combined vertical atlanto-occipital and atlanto-axial dislocations with 2-part fracture of the atlas: Two case reports. Medicine'
  doi: 10.1097/MD.0000000000017776
  credit: 'Traumatic combined vertical atlanto-occipital and atlanto-axial dislocations with 2-part fracture of the atlas: Two case reports. Medicine (Baltimore). 2019 Nov 1;98(44):e17776. doi: 10.1097/MD.0000000000017776 (CC BY) — Figure 2'
  license: CC BY
  url: https://pmc.ncbi.nlm.nih.gov/articles/PMC6946329/
  asset: PMC-PMC6946329_Figure2_A
---

## 판단 — 왜 고정·유합이 먼저인가
- **분리 방향**: 기저가 치돌기 끝보다 크게 위로 떨어졌으면 머리뼈와 경추를 잇는 인대가 끊긴 세로 분리다 — 견인 금기 [[?bellabarba-2006]].
- **신경 정상의 의미**: 신경 결손이 없다는 것은 아직 척수가 다치지 않았다는 뜻일 뿐, 안정하다는 뜻이 아니다. 외상성 경추 탈구는 고정이 필수다 [[harrison-22: 19장 p.132]].
- **확정 처치**: 인대 손상은 저절로 붙지 않으므로 후두골과 위쪽 경추를 내고정해 유합한다 [[?bellabarba-2006]].

## 기전 — 인대가 끊긴 세로 분리에서 척수 신장으로
후두골-고리뼈-중쇠뼈 이음부의 안정은 뼈가 아니라 덮개막(tectorial membrane)·날개인대(alar ligament) 같은 인대가 만든다. 고속 감속 손상에서 머리가 몸통보다 늦게 멈추며 이 인대가 끊어지면 머리뼈가 경추에서 위로·앞으로 떨어지고, 그 사이를 지나는 연수·위쪽 척수가 늘어난다 [[?bellabarba-2006]]. 그래서 측면 X선에서 기저-치돌기 간격이 넓어지고 출혈로 척추앞 연부조직이 두꺼워진다. 경추 운동의 절반이 고리중쇠관절(C1-C2)에서 나올 만큼 이 이음부는 원래 움직임이 크다 [[harrison-22: 19장 p.129]] — 인대가 없으면 붙잡을 것이 없다.

## 가르는 소견 — 분리 방향이 처치를 정한다
- 아래 경추 관절돌기 탈구는 척추체가 앞으로 미끄러지고 관절돌기가 걸린 것이라, 길이 방향으로 당기면 걸림이 풀려 제자리로 돌아온다 [[?atls-10]]. 같은 「탈구」라도 두개경추 탈구에서는 당기는 방향이 곧 손상 방향이다.
- 골절은 CT 로, 인대·척수는 MRI 로 본다 — CT 는 연부조직을 잘 보지 못한다 [[harrison-22: 19장 p.130]].
- 정상 X선의 한계: 측면 X선에서 분리가 미묘하면 놓칠 수 있다 — 고에너지 손상에서 척추앞 부종이 있으면 CT·MRI 로 확인한다 [[harrison-22: 19장 p.130]].

## 권고와 예외
- 영상 전부터, 그리고 수술 전까지 엄격한 고정을 유지한다 [[harrison-22: 19장 p.132]].
- 굴곡·신전 X선은 불안정성 선별 검사지만 [[harrison-22: 19장 p.130]], 명백한 탈구에서는 찍지 않는다.
- 연성 보호대는 신경 소견 없는 급성 목 통증의 통증 완화용이다 [[harrison-22: 19장 p.132]] — 불안정 손상의 고정 수단이 아니다.
