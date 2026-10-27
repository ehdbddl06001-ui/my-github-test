---
id: cn.ortho.odontoid-fracture.diagnosis
type: concept
topic: Orthopedics
see_also: [Emergency Medicine, Radiology]
date: 2026-10-27
updated: 2026-10-27
version: 2
outline: ortho.spine      # 정형외과 손 슬롯 「척추 — 추간판 탈출·협착·척추 골절」(해리슨 대조 대상 아님 — 경추 외상의 고정·영상 선택만 해리슨 17장으로 확인)
confidence: low
review_status: unreviewed
note_form: 2            # 판형 2(2026-09-25)
title: "치아돌기 골절 — 골절선이 허리에 머무나, 몸통으로 가나"
objective: "고령자 낙상 뒤 시상 경추 CT 에서 치아돌기 골절선이 기저부(허리)에 머무는지 C2 몸통으로 내려가는지 읽어 II형과 III형 치아돌기 골절을 구별한다"
objective_kind: 진단
condition: 고령자 저에너지 낙상 뒤 치아돌기(C2) 골절의 형 구분
exams: [usmle, kmle]
summary:
  - "결론: 골절선이 치아돌기 기저부(허리)를 가로지르고 C2 몸통으로 내려가지 않으면 II형, 몸통 해면골로 들어가면 III형이다."
  - "시험 단서: 고령자가 앞으로 넘어져 이마를 부딪친 뒤 위쪽 목 통증 + 시상 CT 의 치아돌기 골절선(type II odontoid fracture)."
  - "왜: 형은 골절선의 높이로 정한다 — 허리는 접촉면이 좁은 피질골이라 잘 안 붙고, 몸통은 넓은 해면골이라 잘 붙는다."
  - "조각이 몸통에 붙어 보인다고 III형이 아니다 — 선이 C2 몸통 해면골 안으로 들어갔는지를 끝까지 따라간다."
  - "65세 초과·골다공증이면 경미한 외상에도 경추 영상을 찍는다 — 급성 골절은 CT 가 1차 검사다."
criteria:
  - id: c-spine-imaging-elderly
    name: 경추 외상 — 누구를 무엇으로 찍나
    kind: 검사 선택
    population: "목 부위 외상 환자"
    statement: "캐나다 경추 규칙은 65세 초과·사지 감각 이상·위험한 기전이면 영상을 권하고, 진행된 골다공증·글루코코르티코이드 사용·암 환자는 경미한 외상에도 영상이 필요할 수 있다 [[harrison-21: 17장 p.127]]. 심한 외상 뒤 급성 골절은 CT 가 1차 검사이며 C1·C2 골절은 X 선보다 CT 가 잘 찾는다 [[harrison-21: 17장 p.120]] [[harrison-21: 17장 p.127]]"
    exceptions: "경미한 외상이나 CT 를 쓸 수 없는 곳에서는 단순 X 선을 쓴다. 척수·추골동맥 손상이 의심되면 MRI·MRA 를 쓴다 [[harrison-21: 17장 p.127]]"
    source: harrison-21
    locator: "17장 p.120 Imaging · p.127 Trauma to the cervical spine"
    basis: current
    exams: [usmle, kmle]
sources:
  - id: harrison-21
    org: "McGraw Hill"
    title: "Harrison's Principles of Internal Medicine, 21st ed. — Chapter 17: Back and Neck Pain"
    kind: textbook
    year: 2022
    citation: "Loscalzo J, Kasper DL, Longo DL, et al (eds). Harrison's Principles of Internal Medicine, 21e. 17장 p.117–129"
    checked_at: 2026-10-27
    checked: "드라이브 17장 문서 대조 — p.120: 중등도 이상 급성 외상의 선별은 CT, CT 가 두개경추·경흉추 이행부·C1·C2 골절·척추관 안 골편·정렬 이상에서 X 선보다 우수. p.127: 경추 외상(골절·아탈구)은 척수 압박 위험, 불안정 분절의 움직임을 막도록 즉시 목 고정, 심한 외상 뒤 급성 골절은 CT·경미한 외상이나 CT 불가 시 X 선, 척수·추골동맥 손상 의심 시 MRI·MRA, NEXUS 저위험 기준(정중선 압통·중독·신경 결손·주의 분산 손상 없음), 캐나다 경추 규칙(65세 초과·사지 감각 이상·위험한 기전), 진행된 골다공증·글루코코르티코이드·암이면 경미한 외상에도 영상. 치아돌기 골절의 분류·치료는 이 장에 없다"
    verified: text
  - id: anderson-1974
    org: "J Bone Joint Surg Am"
    title: "Fractures of the odontoid process of the axis"
    kind: other
    year: 1974
    url: "https://pubmed.ncbi.nlm.nih.gov/?term=Anderson+D%27Alonzo+fractures+of+the+odontoid+process+of+the+axis+1974"
    citation: "Anderson LD, D'Alonzo RT. J Bone Joint Surg Am 1974;56(8):1663-1674"
    checked_at: 2026-10-27
    checked: "서지만(문항 imaging-2026-0445 해설의 근거 목록에서 옮김, 원문 미대조 — 이 컨테이너는 PubMed 를 막는다. url 은 PubMed 검색 링크이고 PMID·DOI 는 확인하지 못했다). I~III형 분류와 형별 유합 경향 서술에만 쓴다 — 검토 항목"
    verified: citation
  - id: tintinalli-9
    org: "McGraw Hill"
    title: "Tintinalli's Emergency Medicine: A Comprehensive Study Guide, 9th ed. — Chapter 258: Spine Trauma"
    kind: textbook
    year: 2020
    citation: "Tintinalli JE, et al (eds). Tintinalli's Emergency Medicine, 9e. McGraw-Hill; 2020. Chapter 258"
    checked_at: 2026-10-27
    checked: "서지만(문항 해설의 근거 목록에서 옮김, 원문 미대조 — 쪽수 미확인). 고령자 저에너지 낙상과 치아돌기 골절의 연관 서술에만 쓴다 — 검토 항목"
    verified: citation
  - id: pmc-c1c2-2023
    org: "Front Surg"
    title: "Case report: Interdisciplinary treatment of complex C1/C2 fractures in a patient with concomitant three-vessel coronary artery disease requiring bypass surgery"
    kind: other
    year: 2023
    doi: "10.3389/fsurg.2023.1123947"
    url: "https://pmc.ncbi.nlm.nih.gov/articles/PMC10228685/"
    citation: "Front Surg 2023;10:1123947 (CC BY) — Figure 1"
    checked_at: 2026-10-27
    checked: "그림 설명(풀 기록에 저장된 원문 캡션)만 확인 — 70세 남성, 시상 CT(A)에서 전위된 치아돌기 II-C형 골절(빨간 화살표)과 후두와 뒤벽의 판간 거미막낭(파란 원), 관상 CT(B)에서 가쪽 전위 없음, 축상 CT(C)에서 불안정 제퍼슨 골절 동반. 본문은 열지 않았다"
    verified: citation
tables:
  - id: c2-fracture-differential
    title: "C2 높이 골절·이상 — 선이 어디를 지나나"
    role: differential
    span: full
    section: "가르는 소견 — 시상 CT 에서 골절선을 끝까지 따라간다"
    columns: ["진단", "골절선·소견", "뼈 접촉·유합", "전형적 상황"]
    rows:
      - ["II형 치아돌기 골절", "치아돌기 기저부(허리)를 가로지르고 C2 몸통으로 내려가지 않음 [[?anderson-1974]]", "좁은 피질골 접촉 — 불유합이 흔함 [[?anderson-1974]]", "고령자의 저에너지 낙상 [[?tintinalli-9]]"]
      - ["III형 치아돌기 골절", "C2 몸통 해면골 안으로 내려감 [[?anderson-1974]]", "넓은 해면골 접촉 — 대개 보조기로 붙음 [[?anderson-1974]]", "같은 기전, 더 낮은 높이"]
      - ["I형 치아돌기 골절", "치아돌기 끝의 견열 [[?anderson-1974]]", "드묾", "인대 견인"]
      - ["치아돌기뼈(os odontoideum)", "짧고 둥근 치아돌기 위에 매끈한 피질로 둘러싼 둥근 뼈조각, 급성 골절선 없음", "골절이 아님", "우연 발견·만성"]
      - ["행맨 골절", "C2 관절간부 양쪽 — 신경궁, 치아돌기가 아님", "—", "과신전 + 축 하중"]
    note: "형은 조각의 모양이 아니라 골절선의 높이로 정한다. 시상·관상 재구성을 함께 보면 선이 몸통으로 들어갔는지 확인하기 쉽다."
pitfalls:
  - contrast: "II형 vs III형 — 「조각이 몸통에 붙어 있으니 III형」"
    point: "형은 골절선이 지나는 높이로 정한다. 선이 치아돌기 허리를 가로지르고 C2 몸통 해면골로 내려가지 않으면 II형이다 [[?anderson-1974]]. 같은 고령자 낙상 기전이라 기전으로는 둘을 가르지 못하고, 영상에서 선을 끝까지 따라가야 한다."
    exception: "골절선이 치아돌기 아래 C2 몸통 해면골까지 내려갔다면 III형이 답이다 [[?anderson-1974]]."
    covers: ["imaging-2026-0445:C"]
  - contrast: "치아돌기뼈 vs 급성 II형 골절"
    point: "치아돌기뼈는 매끈하고 둥근 피질 가장자리를 가진 뼈조각이 짧은 치아돌기 위에 있고 급성 골절선이 없다. 낙상 직후의 날카로운 골절선과 전위는 급성 골절이다."
  - contrast: "행맨·제퍼슨 골절 — 층과 구조가 다르다"
    point: "행맨 골절은 C2 관절간부(신경궁), 제퍼슨 골절은 C1 고리의 파열이다. 시상 CT 에서 치아돌기 기저부를 지나는 선은 둘 다 아니다."
diagram:
  title: "고령자 낙상 뒤 목 통증 — 치아돌기 골절의 형"
  nodes:
    - {id: start, kind: start, text: "고령자가 넘어진 뒤 위쪽 목 통증"}
    - {id: immob, kind: step, text: "목 고정 → 경추 CT"}
    - {id: neuro, kind: decision, text: "신경 결손이 있나?"}
    - {id: mri, kind: step, text: "MRI 를 더한다(척수·추골동맥)"}
    - {id: line, kind: decision, text: "치아돌기 골절선은 어디를 지나나?"}
    - {id: info, kind: info, text: "시상·관상 재구성으로 선을 따라간다"}
    - {id: t2, kind: end, text: "허리를 가로지름 → II형"}
    - {id: t3, kind: end, text: "C2 몸통 해면골로 → III형"}
    - {id: t1, kind: end, text: "끝의 견열 → I형"}
  edges:
    - {from: start, to: immob}
    - {from: immob, to: neuro}
    - {from: neuro, to: mri, label: "있음"}
    - {from: neuro, to: line, label: "없음"}
    - {from: mri, to: line}
    - {from: line, to: t2, label: "기저부"}
    - {from: line, to: t3, label: "몸통 안"}
    - {from: line, to: t1, label: "끝"}
    - {from: line, to: info, label: "애매"}
    - {from: info, to: t2, label: "몸통 침범 없음"}
    - {from: info, to: t3, label: "몸통 침범"}
diagram_notes:
  - "경추 외상은 불안정 분절의 움직임이 척수를 다치게 하지 않도록 먼저 목을 고정한다 [[harrison-21: 17장 p.127]]."
  - "65세 초과는 캐나다 경추 규칙에서 영상 적응이고, 진행된 골다공증이면 경미한 외상에도 영상을 고려한다 [[harrison-21: 17장 p.127]]."
  - "C1·C2 골절은 X 선보다 CT 가 잘 찾는다 [[harrison-21: 17장 p.120]]. 척수·추골동맥 손상이 의심되면 MRI·MRA [[harrison-21: 17장 p.127]]."
  - "C2 골절이 있으면 C1 도 본다 — 문항 그림의 원 논문 환자는 II형 치아돌기 골절에 제퍼슨 골절이 함께 있었다 [[?pmc-c1c2-2023]]."
checks:
  - q: "70세 남성이 앞으로 넘어져 이마를 부딪친 뒤 위쪽 목 통증을 호소한다. 시상 CT 에서 치아돌기 기저부를 가로지르는 골절선이 C2 몸통으로 내려가지 않는다. 진단은?"
    a: "II형 치아돌기 골절."
  - q: "II형과 III형 치아돌기 골절을 가르는 영상 소견과, 그 구분이 중요한 이유는?"
    a: "골절선이 C2 몸통 해면골로 내려가면 III형, 허리에 머물면 II형이다. II형은 좁은 피질골 접촉이라 불유합이 흔하고 III형은 넓은 해면골이라 잘 붙는다."
  - q: "경추 외상에서 나이만으로 영상을 찍을 근거가 되는 규칙과 기준 나이는?"
    a: "캐나다 경추 규칙 — 65세 초과."
variants:
  - id: v1
    of: imaging-2026-0445
    flip: true
    changed: "골절선을 「치아돌기 기저부를 가로지르고 C2 몸통 침범 없음」에서 「치아돌기 아래 C2 몸통 해면골로 내려가 위관절면까지 닿음」으로 바꿈 → 답이 II형에서 III형 치아돌기 골절로 바뀜"
    context: "단서를 바꿔 답이 바뀌는 변형 — 골절선이 몸통으로 들어간다"
    stem: "A 76-year-old woman is brought to the emergency department after she slipped on a wet floor at home and struck her face on a cabinet. She reports pain in the upper neck that worsens when she tries to turn her head. She takes alendronate for osteoporosis. Vital signs are within normal limits. There is tenderness over the upper posterior cervical spine, and neurologic examination of all extremities is normal. A cervical collar is placed. Sagittal and coronal CT reconstructions show a fracture line that begins below the dens and extends down into the cancellous bone of the C2 body, reaching the superior articular facets; the C1 ring is intact. Which of the following is the most likely diagnosis?"
    choices: ["A. Avulsion of the tip of the dens (type I odontoid fracture)", "B. Fracture through the base of the dens (type II odontoid fracture)", "C. Fracture extending into the C2 vertebral body (type III odontoid fracture)", "D. Bilateral C2 pars interarticularis fracture (hangman fracture)", "E. Congenital separate ossicle above C2 (os odontoideum)"]
    answer: "C"
    explanation: "The type of odontoid fracture is set by the level of the fracture line. Here the line runs down into the cancellous C2 body and reaches the superior articular facets, so it is a type III fracture [[?anderson-1974]]. In the original item the line crossed the waist of the dens and stayed out of the body — type II. The mechanism (a low-energy fall in an older adult) is the same for both and does not separate them [[?tintinalli-9]]. CT is preferred because it detects C1 and C2 fractures better than plain films [[harrison-21: 17장 p.120]]. A hangman fracture involves the C2 pars, not the dens."
    kind: application
  - id: v2
    of: imaging-2026-0445
    flip: false
    changed: "성별·나이(70세 남성 → 81세 여성)·낙상 경위(집에서 걸려 넘어짐 → 계단 마지막 칸에서 앞으로 넘어짐)·복용약·영상 서술 순서를 바꾸고 「치아돌기 기저부를 가로지르고 C2 몸통으로 내려가지 않는 골절선」은 그대로 → 답은 여전히 II형"
    context: "겉모습만 바꾸고 답은 같은 변형 — 다른 환자, 같은 골절선"
    stem: "An 81-year-old woman is brought to the emergency department after missing the last step of a staircase and falling forward onto her face. She has neck pain at the base of the skull and refuses to move her head. She takes levothyroxine and atorvastatin. Blood pressure is 138/78 mm Hg. There is a bruise on the chin and tenderness over the upper posterior cervical spine. Strength, sensation, and reflexes are normal. A cervical collar is placed. Coronal and sagittal CT reconstructions show a fracture line crossing the narrow junction of the dens with the C2 body, with slight posterior displacement of the dens; the line does not enter the C2 vertebral body. Which of the following is the most likely diagnosis?"
    choices: ["A. Fracture through the base of the dens (type II odontoid fracture)", "B. Fracture extending into the C2 vertebral body (type III odontoid fracture)", "C. Bilateral C2 pars interarticularis fracture (hangman fracture)", "D. Burst fracture of the C1 ring (Jefferson fracture)", "E. Congenital separate ossicle above C2 (os odontoideum)"]
    answer: "A"
    explanation: "Whatever the patient's sex, age, or exact fall, a fracture line across the waist of the dens that does not enter the cancellous C2 body is a type II odontoid fracture [[?anderson-1974]]. It is typical of low-energy falls in older adults [[?tintinalli-9]], and patients older than 65 warrant cervical imaging after neck trauma [[harrison-21: 17장 p.127]]. A type III fracture would extend into the C2 body; os odontoideum has smooth corticated margins without an acute fracture line; a Jefferson fracture involves the C1 ring."
    kind: application
figures:
- id: f1
  file: docs/assets/figures/pmc-pmc10228685_figure1_a.jpg
  kind: ct
  at: 가르는 소견 — 시상 CT 에서 골절선을 끝까지 따라간다
  shows: '상부 경추 시상 CT — 전위된 II형 치아돌기 골절(저자 캡션: odontoid type II-C)'
  look_for:
  - 빨간 화살표 — 치아돌기 기저부를 비스듬히 가로지르는 골절선
  - 골절선 아래 C2 몸통 해면골은 이어져 있음
  label: '「Preoperative CT scan (bone window) of craniocervical junction. (A) Sagittal CT revealed a dislocated odontoid type II-C fracture (red arrow) and an intradiploic arachnoid cyst in posterior wall of the posterior fossa (blue circle). (B) Coronal CT revealed no lateral dislocation of the fracture of the odontoid process (red arrow). (C) Axial CT scan revealed an unstable Jefferson''s fracture (with fracture of the anterior arch on the right, dual fractures of the posterior arch and fracture of the left lateral mass of C1) (yellow arrows).」 — Case report: Interdisciplinary treatment of complex C1/C2 fractures in a patient with concomitant three-vessel coronary artery disease requiring bypass surgery'
  label_basis: published_figure
  reference: 동료 심사 논문의 그림 설명(저자가 그 소견이라고 쓴 그림)
  paper: 'Case report: Interdisciplinary treatment of complex C1/C2 fractures in a patient with concomitant three-vessel coronary artery disease requiring bypass surgery. Frontiers in Surgery'
  doi: 10.3389/fsurg.2023.1123947
  credit: 'Case report: Interdisciplinary treatment of complex C1/C2 fractures in a patient with concomitant three-vessel coronary artery disease requiring bypass surgery. Front Surg. 2023 May 16;10:1123947. doi: 10.3389/fsurg.2023.1123947 (CC BY) — Figure 1'
  license: CC BY
  url: https://pmc.ncbi.nlm.nih.gov/articles/PMC10228685/
  asset: PMC-PMC10228685_Figure1_A
  from_question: imaging-2026-0445
---

## 판단 — 왜 II형이 먼저인가
- 고령자가 앞으로 넘어져 이마를 부딪친 뒤의 위쪽 목 통증은 치아돌기 골절의 전형적 상황이다 [[?tintinalli-9]]. 65세 초과라 경추 영상의 적응이고 [[harrison-21: 17장 p.127]], C2 골절은 CT 가 잘 찾는다 [[harrison-21: 17장 p.120]].
- 결정적 소견은 **골절선의 높이**다. 선이 치아돌기 허리(기저부)를 가로지르고 C2 몸통 해면골로 내려가지 않으면 II형이다 [[?anderson-1974]].
- 정상 신경 진찰은 진단을 바꾸지 않고 치료 선택·긴급도에 쓰이는 정보다. 그림 안의 다른 표시(후두골 병변)는 진단과 무관하다.

## 기전 — 지렛대가 허리를 꺾는다
치아돌기는 환추(C1) 앞고리 뒤에 끼워진 축으로, 횡인대가 붙잡아 머리 회전의 중심이 된다. 앞으로 넘어져 이마를 부딪치면 머리가 꺾이고, C1 이 치아돌기를 C2 몸통에 대고 지렛대처럼 민다. 힘은 치아돌기와 몸통이 만나는 가장 좁은 곳 — 허리 — 에 모인다 [[?anderson-1974]]. 나이가 들면 뼈가 약해져 낮은 에너지로도 부러진다 [[?tintinalli-9]] — 진행된 골다공증 환자는 경미한 외상에도 영상을 고려하라는 이유다 [[harrison-21: 17장 p.127]].
- **왜 높이가 예후를 정하나**: 허리의 골절면은 좁고 대부분 피질골이라 접촉·혈류가 부족해 불유합이 흔하다. 몸통으로 내려간 골절은 넓은 해면골끼리 맞닿아 대개 보조기로 붙는다 [[?anderson-1974]]. 그래서 같은 「치아돌기 골절」이라도 형이 치료 방향을 가른다.

## 가르는 소견 — 시상 CT 에서 골절선을 끝까지 따라간다
- 판독 순서: ① 치아돌기에 급성 골절선이 있나(날카로운 선·전위) ② 그 선이 끝·허리·몸통 중 어디를 지나나 ③ 전위·각형성의 방향 ④ C1 고리도 보았나.
- **해석 한계**: 한 장의 시상 영상에서는 선이 몸통에 닿았는지 애매할 수 있다 — 관상 재구성을 함께 본다. 둥글고 매끈한 피질로 둘러싼 뼈조각은 급성 골절이 아니라 치아돌기뼈일 수 있다. 척수 손상 여부는 CT 가 아니라 MRI 로 본다 [[harrison-21: 17장 p.127]].
- C2 에 골절이 있으면 C1 도 확인한다 — 문항 그림의 원 증례는 II형 치아돌기 골절에 제퍼슨 골절이 동반되었다 [[?pmc-c1c2-2023]].

## 권고와 예외
- 경추 외상이 의심되면 영상 전에 목을 고정한다 [[harrison-21: 17장 p.127]]. NEXUS 저위험 기준(정중선 압통·중독·신경 결손·주의 분산 손상이 모두 없음)을 만족하면 의미 있는 손상 가능성이 낮지만, 캐나다 경추 규칙은 65세 초과면 영상을 권한다 [[harrison-21: 17장 p.127]].
- 심한 외상 뒤 급성 골절은 CT, 경미한 외상이나 CT 를 쓸 수 없으면 X 선, 척수·추골동맥 손상이 의심되면 MRI·MRA [[harrison-21: 17장 p.127]].
- 형별 치료(II형의 수술 고정 여부, III형의 보조기)는 이 정리본의 근거 논문을 원문 대조하지 못했다(검토 항목).

## 시험 쟁점 — 충돌·맥락·새 근거
- 해당 없음(대조: 해리슨 17장 p.120·127 — 경추 외상의 고정·영상 선택만 다루고 치아돌기 골절 분류는 없다).

## (심화) 같은 낙상, 다른 높이
젊은 성인의 상부 경추 골절은 대개 고에너지 손상이지만, 고령자는 서 있는 높이에서 넘어지는 것만으로 치아돌기가 부러진다 [[?tintinalli-9]]. 기전이 같아도 골절선이 허리에 머물면 붙기 어렵고, 몸통으로 내려가면 잘 붙는다 [[?anderson-1974]]. 시험이 「II형 vs III형」을 묻는 이유는 이름이 아니라 이 유합 차이 — 곧 치료 선택 — 때문이다.
