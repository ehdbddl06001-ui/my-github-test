---
id: cn.ortho.atlas-burst-fracture.mechanism
type: concept
topic: Orthopedics
see_also: [Emergency Medicine, Radiology]
date: 2026-11-02
updated: 2026-11-02
version: 2
outline: ortho.spine      # 정형외과 손 슬롯 「척추 — 추간판 탈출·협착·척추 골절」(해리슨 대조 대상 아님 — 경추 외상의 고정·영상 선택만 해리슨 22판 19장으로 확인)
confidence: low
review_status: unreviewed
note_form: 2            # 판형 2(2026-09-25)
title: "고리뼈 파열 — 앞·뒤고리가 다 끊기면 축성 압박"
objective: "고리뼈(C1) 축상 CT 에서 앞고리·뒤고리 골절 위치를 읽어 축성 압박(고리 파열, Jefferson 골절)과 과신전(뒤고리 단독 골절) 기전을 구별한다"
objective_kind: 기전
condition: 고리뼈(C1, atlas) 고리 파열 — 제퍼슨 골절(Jefferson fracture)의 손상 기전
exams: [usmle, kmle]
summary:
  - "결론: 앞고리와 뒤고리가 함께 끊긴 고리뼈 골절은 머리 꼭대기로 들어온 축성 압박(axial loading)이다."
  - "시험 단서: 얕은 물 다이빙·머리부터 떨어짐 + 위쪽 목 통증, 신경 결손 없음 + C1 축상 CT 의 여러 곳 고리 골절(Jefferson fracture)."
  - "왜: 뒤통수관절융기가 쐐기 모양 가쪽덩이를 바깥으로 벌려야 앞고리까지 끊긴다 — 과신전은 뒤고리만 집는다."
  - "조각이 바깥으로 벌어져 척추관이 넓어지므로 신경 결손이 드물다 — 신경 진찰 정상은 기전 판단을 바꾸지 않는다."
  - "안정성은 가로인대(transverse ligament)가 정한다 — 끊겼으면 불안정이다."
pitfalls:
  - contrast: "과신전 vs 축성 압박 — 「C1 고리 골절이면 과신전」"
    point: "과신전은 뒤고리가 뒤통수뼈와 C2 가시돌기 사이에 끼어 양쪽 뒤고리만 끊긴다. 앞고리까지 끊겼다면 고리를 바깥으로 벌리는 힘, 곧 머리 꼭대기의 축성 압박이 필요하다 [[?jefferson-1920]] [[?rockwood-9]]."
    exception: "축상 CT 에서 앞고리가 온전하고 뒤고리만 양쪽에서 끊겼다면 과신전 기전이 답이다."
    covers: ["imaging-2026-0508:B"]
  - contrast: "과굴곡 vs 축성 압박 — 「목뼈 골절이면 굽힘」"
    point: "과굴곡은 아래 목뼈(C3~C7) 몸통의 앞쪽 쐐기 압박·굽힘 눈물방울 골절을 만든다. 고리뼈에는 몸통이 없어 굽힘이 고리 파열을 만들지 않는다 [[?rockwood-9]]."
    covers: ["imaging-2026-0508:C"]
  - contrast: "신경 결손이 없으니 가벼운 손상?"
    point: "고리 파열은 척추관을 넓혀 신경 결손이 드물 뿐이다. 안정성은 가로인대가 정하므로 신경 진찰이 정상이어도 목 고정을 유지하고 평가한다 [[harrison-22: 19장 p.132]]."
tables:
  - id: c1-mechanism
    title: "고리뼈 골절 — 끊긴 자리가 기전을 말한다"
    role: differential
    span: column
    section: "가르는 소견 — 축상 CT 에서 앞고리와 뒤고리를 따로 본다"
    columns: ["끊긴 자리", "기전", "전형적 상황"]
    rows:
      - ["앞고리 + 뒤고리(2~4곳)", "축성 압박 — 가쪽덩이가 바깥으로 벌어짐 [[?jefferson-1920]]", "얕은 물 다이빙, 머리부터 떨어짐 [[?rockwood-9]]"]
      - ["뒤고리만 양쪽, 앞고리 온전", "과신전 — 뒤통수뼈와 C2 사이에 끼임 [[?rockwood-9]]", "턱·이마를 부딪쳐 목이 뒤로 꺾임"]
      - ["치아돌기 끝 작은 조각", "가쪽 굽힘 — 날개인대 견열 [[?rockwood-9]]", "—"]
      - ["골절 없이 가쪽덩이-치아돌기 비대칭", "회전 — 고리중쇠 회전 아탈구 [[?rockwood-9]]", "흔히 소아"]
    note: "C3~C7 몸통의 앞쪽 쐐기 압박은 과굴곡이다 — 고리뼈에는 몸통이 없다."
criteria:
  - id: c-spine-trauma-imaging
    name: 경추 외상 — 고정과 영상
    kind: 검사 선택
    population: "목 외상 환자"
    statement: "경추 골절·탈구는 척수 손상이 동반되면 생명을 위협하며, 불안정한 척추로 인한 추가 척수 손상을 막도록 목 고정이 필수다 [[harrison-22: 19장 p.132]]. 척추 골절이 의심되면 CT 를 쓴다 [[harrison-22: 19장 p.130]]"
    exceptions: "CT 는 척수·연부조직을 잘 보지 못한다 — 척수·인대 평가는 MRI [[harrison-22: 19장 p.130]]"
    source: harrison-22
    locator: "19장 p.130 Imaging · p.132 Traumatic"
    basis: current
    exams: [usmle, kmle]
sources:
  - id: harrison-22
    org: "McGraw Hill"
    title: "Harrison's Principles of Internal Medicine, 22nd ed. — Chapter 19: Neck Pain"
    kind: textbook
    year: 2025
    citation: "Harrison's Principles of Internal Medicine, 22e. 19장 p.129–133"
    checked_at: 2026-11-02
    checked: "드라이브 H22_019 문서 대조 — p.129: 경추 운동의 50% 가 고리중쇠관절(C1-C2)에서 나온다. p.130: 척추 골절이 의심되면 CT, CT 는 연부조직이 잘 안 보여 척수 평가에 부적합하고 MRI 가 연부조직의 표준, 최근 머리·목 외상은 추가 검사가 필요한 소견(Table 19-2). p.132: 외상성 경추 골절·탈구는 척수 손상이 동반되면 생명을 위협하고, 불안정성으로 인한 추가 척수 손상을 막도록 목 고정이 필수. 고리뼈 골절의 기전·분류·안정성 기준은 이 장에 없다"
    verified: text
  - id: jefferson-1920
    org: "Br J Surg"
    title: "Fracture of the atlas vertebra: report of four cases, and a review of those previously recorded"
    kind: other
    year: 1920
    url: "https://pubmed.ncbi.nlm.nih.gov/?term=Jefferson+fracture+of+the+atlas+vertebra+1920"
    citation: "Jefferson G. Br J Surg 1920;7(27):407-422"
    checked_at: 2026-11-02
    checked: "서지만(문항 imaging-2026-0508 해설의 근거 목록에서 옮김, 원문 미대조 — 이 컨테이너는 PubMed·doi.org 를 막는다. PMID·DOI 미확인, url 은 PubMed 검색 링크). 축성 압박으로 고리가 파열된다는 기전 서술에만 쓴다 — 검토 항목"
    verified: citation
  - id: rockwood-9
    org: "Wolters Kluwer"
    title: "Rockwood and Green's Fractures in Adults, 9th ed. — Cervical Spine Fractures and Dislocations"
    kind: textbook
    year: 2019
    citation: "Tornetta P III, Ricci WM, Ostrum RF, et al (eds). Rockwood and Green's Fractures in Adults, 9e. Wolters Kluwer; 2019. 장: Cervical Spine Fractures and Dislocations (쪽 미확인)"
    checked_at: 2026-11-02
    checked: "서지만(문항 해설의 근거 목록에서 옮김, 원문 미대조 — 쪽수 미확인). 과신전·과굴곡·가쪽 굽힘·회전 기전별 골절 양상과 가로인대 안정성 서술에만 쓴다 — 검토 항목"
    verified: citation
  - id: pmc-c1c2-2023
    org: "Front Surg"
    title: "Case report: Interdisciplinary treatment of complex C1/C2 fractures in a patient with concomitant three-vessel coronary artery disease requiring bypass surgery"
    kind: other
    year: 2023
    doi: "10.3389/fsurg.2023.1123947"
    url: "https://pmc.ncbi.nlm.nih.gov/articles/PMC10228685/"
    citation: "Front Surg 2023;10:1123947 (CC BY) — Figure 1"
    checked_at: 2026-11-02
    checked: "그림 설명(풀 기록에 저장된 원문 캡션)만 확인 — 축상 CT(C)에서 불안정 제퍼슨 골절(오른쪽 앞고리 골절, 뒤고리 두 곳 골절, 왼쪽 가쪽덩이 골절, 노란 화살표). 본문은 열지 않았다"
    verified: citation
diagram:
  title: "위쪽 목 외상 — 고리뼈 골절의 기전과 안정성"
  nodes:
    - {id: start, kind: start, text: "머리 외상 뒤 위쪽 목 통증"}
    - {id: immob, kind: step, text: "목 고정 → 경추 CT"}
    - {id: ring, kind: decision, text: "C1 고리는 어디서 끊겼나?"}
    - {id: info, kind: info, text: "축상 CT 로 앞고리·뒤고리를 따로 본다"}
    - {id: burst, kind: step, text: "앞·뒤 모두 → 축성 압박(파열)"}
    - {id: post, kind: end, text: "뒤고리만 양쪽 → 과신전"}
    - {id: lig, kind: decision, text: "가로인대가 끊겼나?"}
    - {id: stable, kind: end, text: "안정 → 보조기 고정"}
    - {id: unstable, kind: end, text: "불안정 → 고정술 검토"}
  edges:
    - {from: start, to: immob}
    - {from: immob, to: ring}
    - {from: ring, to: burst, label: "앞·뒤 모두"}
    - {from: ring, to: post, label: "뒤고리만"}
    - {from: ring, to: info, label: "애매"}
    - {from: info, to: burst, label: "앞고리도 끊김"}
    - {from: info, to: post, label: "앞고리 온전"}
    - {from: burst, to: lig}
    - {from: lig, to: stable, label: "온전"}
    - {from: lig, to: unstable, label: "파열·견열"}
diagram_notes:
  - "불안정 분절로 인한 추가 척수 손상을 막도록 영상 전에 목을 고정한다 [[harrison-22: 19장 p.132]]."
  - "골절은 CT 로 보고, 척수·인대(가로인대 포함)는 CT 로 잘 안 보이므로 MRI 를 더한다 [[harrison-22: 19장 p.130]]."
  - "가로인대 파열 단서: 입벌림 영상에서 양쪽 가쪽덩이가 C2 밖으로 합쳐 약 7 mm 넘게 벌어짐, 또는 CT·MRI 의 뼈 견열 [[?rockwood-9]]."
  - "C1 골절이 있으면 C2 도 본다 — 문항 그림의 원 증례는 제퍼슨 골절에 II형 치아돌기 골절이 함께 있었다 [[?pmc-c1c2-2023]]."
checks:
  - q: "얕은 물에 다이빙해 머리 꼭대기를 부딪친 뒤 위쪽 목 통증. C1 축상 CT 에서 앞고리 1곳과 뒤고리 2곳이 끊겼다. 기전은?"
    a: "머리 꼭대기에서 뒤통수관절융기를 거쳐 전달된 축성 압박 — 고리 파열(제퍼슨 골절)."
  - q: "C1 뒤고리만 양쪽에서 끊기고 앞고리가 온전하면 기전은?"
    a: "과신전 — 뒤고리가 뒤통수뼈와 C2 사이에 끼인다."
  - q: "제퍼슨 골절에서 신경 결손이 드문 이유와, 안정성을 정하는 구조는?"
    a: "조각이 바깥으로 벌어져 척추관이 넓어지기 때문이다. 안정성은 가로인대가 정한다."
variants:
  - id: v1
    of: imaging-2026-0508
    flip: true
    changed: "다이빙으로 머리 꼭대기를 부딪침 + 앞·뒤고리 모두 골절 → 넘어지며 턱을 부딪쳐 목이 뒤로 꺾임 + 앞고리 온전, 뒤고리만 양쪽 골절로 바꿈 → 답이 축성 압박에서 과신전으로 바뀜"
    context: "단서를 바꿔 답이 바뀌는 변형 — 앞고리가 온전하다"
    stem: "A 68-year-old woman is brought to the emergency department after she tripped on the sidewalk and struck her chin on a concrete step, forcing her head backward. She reports pain at the back of the upper neck. Pulse is 84/min, and blood pressure is 136/80 mm Hg. She has a laceration under the chin and is wearing a rigid cervical collar. Strength, sensation, and reflexes are normal in all extremities. Axial CT of the upper cervical spine at the level of C1 shows a fracture on each side of the posterior arch; the anterior arch and lateral masses are intact, and the dens is centered. Which of the following mechanisms most likely produced this injury?"
    choices: ["A. Axial compression transmitted from the vertex through the occipital condyles", "B. Hyperextension compressing the posterior arch between the occiput and C2", "C. Hyperflexion with compression of the anterior vertebral body", "D. Lateral flexion with avulsion of the alar ligament from the dens", "E. Rotational force causing atlantoaxial facet subluxation"]
    answer: "B"
    explanation: "When only the posterior arch is broken on both sides and the anterior arch is intact, the arch was pinched between the occiput and the C2 spinous process as the head was forced backward — hyperextension [[?rockwood-9]]. In the original item the anterior arch was also broken, which requires an axial load spreading the lateral masses outward (a burst, Jefferson fracture) [[?jefferson-1920]]. Hyperflexion compresses the bodies of lower cervical vertebrae; C1 has no body. Neck immobilization is maintained while the injury is evaluated [[harrison-22: 19장 p.132]]."
    kind: application
  - id: v2
    of: imaging-2026-0508
    flip: false
    changed: "나이·성별(70세 남성 → 27세 여성)·외상 경위(얕은 물 다이빙 → 말에서 떨어져 머리 꼭대기로 착지)·동반 질환을 바꾸고 「앞고리와 뒤고리가 모두 끊긴 C1 고리」는 그대로 → 답은 여전히 축성 압박"
    context: "겉모습만 바꾸고 답은 같은 변형 — 다른 환자, 같은 고리 파열"
    stem: "A 27-year-old woman is brought to the emergency department 40 minutes after she was thrown from a horse and landed on the top of her head. She wore a helmet. She reports severe pain at the base of the skull and holds her head still. She has no medical history. Pulse is 96/min, and blood pressure is 124/76 mm Hg. A rigid cervical collar is in place. Neurologic examination is normal. Axial CT at the level of C1 shows two fractures of the anterior arch and two fractures of the posterior arch, with the lateral masses displaced outward. Which of the following mechanisms most likely produced this injury?"
    choices: ["A. Rotational force causing atlantoaxial facet subluxation", "B. Hyperflexion with compression of the anterior vertebral body", "C. Axial compression transmitted from the vertex through the occipital condyles", "D. Hyperextension compressing the posterior arch between the occiput and C2", "E. Lateral flexion with avulsion of the alar ligament from the dens"]
    answer: "C"
    explanation: "Whatever the patient or the exact story, a C1 ring broken both in front and behind with outward displacement of the lateral masses is a burst (Jefferson) fracture from axial loading on the vertex [[?jefferson-1920]]. Hyperextension breaks only the posterior arch [[?rockwood-9]]. The normal neurologic examination fits, because the fragments widen the canal; stability depends on the transverse ligament, so the collar stays on while it is assessed [[harrison-22: 19장 p.132]]."
    kind: application
figures:
- id: f1
  file: docs/assets/figures/pmc-pmc10228685_figure1_c.jpg
  kind: ct
  at: 가르는 소견 — 축상 CT 에서 앞고리와 뒤고리를 따로 본다
  shows: '고리뼈(C1) 축상 CT — 불안정 제퍼슨 골절(저자 캡션: 오른쪽 앞고리, 뒤고리 두 곳, 왼쪽 가쪽덩이 골절)'
  look_for:
  - 위쪽 화살표 — 앞고리의 끊긴 자리
  - 아래쪽 화살표 셋 — 뒤고리와 가쪽덩이 쪽의 끊긴 자리
  - 고리 가운데의 치아돌기
  label: '「Preoperative CT scan (bone window) of craniocervical junction. (A) Sagittal CT revealed a dislocated odontoid type II-C fracture (red arrow) and an intradiploic arachnoid cyst in posterior wall of the posterior fossa (blue circle). (B) Coronal CT revealed no lateral dislocation of the fracture of the odontoid process (red arrow). (C) Axial CT scan revealed an unstable Jefferson''s fracture (with fracture of the anterior arch on the right, dual fractures of the posterior arch and fracture of the left lateral mass of C1) (yellow arrows).」 — Case report: Interdisciplinary treatment of complex C1/C2 fractures in a patient with concomitant three-vessel coronary artery disease requiring bypass surgery'
  label_basis: published_figure
  reference: 동료 심사 논문의 그림 설명(저자가 그 소견이라고 쓴 그림)
  paper: 'Case report: Interdisciplinary treatment of complex C1/C2 fractures in a patient with concomitant three-vessel coronary artery disease requiring bypass surgery. Frontiers in Surgery'
  doi: 10.3389/fsurg.2023.1123947
  credit: 'Case report: Interdisciplinary treatment of complex C1/C2 fractures in a patient with concomitant three-vessel coronary artery disease requiring bypass surgery. Front Surg. 2023 May 16;10:1123947. doi: 10.3389/fsurg.2023.1123947 (CC BY) — Figure 1'
  license: CC BY
  url: https://pmc.ncbi.nlm.nih.gov/articles/PMC10228685/
  asset: PMC-PMC10228685_Figure1_C
  from_question: imaging-2026-0508
---

## 판단 — 왜 축성 압박이 먼저인가
- 결정적 소견은 **앞고리가 끊겼는가**다. 고리는 앞에서 붙잡혀 있으면 한 쪽만 끊기기 어렵다 — 앞과 뒤가 모두 끊겼다면 고리를 바깥으로 벌리는 힘이 있었다 [[?jefferson-1920]].
- 그 힘은 머리 꼭대기로 들어온 축성 하중이다. 얕은 물 다이빙·머리부터 떨어짐이 전형적 이야기다 [[?rockwood-9]].
- 과신전은 뒤고리만, 과굴곡은 아래 목뼈 몸통을 다친다 — 표 참고. 신경 진찰 정상은 고리 파열에서 흔해 기전을 바꾸지 않는다.

## 기전 — 쐐기가 고리를 벌린다
고리뼈(atlas)는 몸통이 없는 고리다. 양옆의 가쪽덩이(lateral mass)는 바깥이 두껍고 안쪽이 얇은 쐐기 모양이며, 윗면이 뒤통수관절융기(occipital condyle)를 받친다. 머리 꼭대기에 힘이 들어오면 관절융기가 쐐기를 아래로 박아 가쪽덩이를 바깥으로 벌리고, 고리는 앞고리·뒤고리와 가쪽덩이가 만나는 얇은 곳에서 끊긴다 [[?jefferson-1920]].
- **왜 신경이 대개 멀쩡한가**: 조각이 바깥으로 벌어져 척추관이 오히려 넓어진다.
- **왜 가로인대가 안정성을 정하나**: 가로인대(transverse atlantal ligament)는 치아돌기를 앞고리 뒤에 붙잡는다. 가쪽덩이가 너무 벌어져 이 인대가 끊기면 C1-C2 가 불안정해진다 [[?rockwood-9]]. 경추 운동의 절반이 이 고리중쇠관절에서 나온다 [[harrison-22: 19장 p.129]].

## 가르는 소견 — 축상 CT 에서 앞고리와 뒤고리를 따로 본다
- 판독 순서: ① 앞고리가 이어져 있나 ② 뒤고리가 몇 곳에서 끊겼나 ③ 가쪽덩이가 바깥으로 밀렸나 ④ 치아돌기가 고리 가운데에 있나 ⑤ C2 도 보았나.
- **해석 한계**: 한 장의 축상 영상에서 얇은 골절선은 놓치기 쉽다 — 위·아래 단면과 재구성을 함께 본다. 가로인대 자체는 CT 로 보이지 않으므로 벌어짐·견열 조각으로 짐작하고 MRI 로 확인한다 [[harrison-22: 19장 p.130]].

## 권고와 예외
- 경추 골절이 의심되면 불안정성으로 인한 추가 척수 손상을 막도록 목을 고정하고, 골절은 CT 로 본다 [[harrison-22: 19장 p.130]] [[harrison-22: 19장 p.132]].
- 안정 파열은 보조기, 가로인대 파열은 고정술을 검토한다는 치료 갈래는 원문 대조하지 못했다(검토 항목).

## 시험 쟁점 — 충돌·맥락·새 근거
- 해당 없음(대조: 해리슨 22판 19장 p.129~132 — 경추 외상의 고정·영상 선택만 다루고 고리뼈 골절의 기전·분류는 없다).

## (심화) 고리가 한 곳만 끊길 수 있나
닫힌 고리는 대개 두 곳 이상에서 끊긴다. 뒤고리 단독 골절은 앞고리가 온전해 고리가 「경첩」처럼 버티는 상황 — 뒤쪽에서만 집는 과신전 — 이고, 앞·뒤가 모두 끊긴 파열은 바깥으로 벌리는 힘이 있었다는 뜻이다 [[?jefferson-1920]] [[?rockwood-9]]. 그래서 축상 CT 한 장에서 「앞고리가 이어졌는가」 하나가 기전 문항의 답을 가른다.
