---
id: cn.ortho.salter-harris-ii.healing-callus-cast
type: concept
topic: Orthopedics
see_also: [Pediatrics, Emergency Medicine]
date: 2026-11-09
updated: 2026-11-09
version: 2
outline: ortho.pediatric         # 정형외과 손 슬롯 「소아 정형 — 성장판 손상·고관절 이형성」(해리슨 대조 대상 아님)
confidence: medium
review_status: unreviewed
note_form: 2
title: "놓친 Salter-Harris II — 골막 신생골은 가골, 석고 고정"
objective: "넘어진 지 2주 된 소아 손목 X선에서 성장판을 지나 골간단으로 이어지는 골절선과 골막 신생골을 치유 중인 Salter-Harris II 골절로 읽고 석고 고정을 고른다"
objective_kind: 치료
condition: 소아 원위 요골 Salter-Harris II 형 골절(치유기)
exams: [kmle, usmle]
summary:
  - "결론: 외상 2주 뒤 성장판→골간단 골절선 + 매끈한 골막 신생골 = 치유 중 Salter-Harris II, 전위 없으면 석고 고정."
  - "시험 단서: 「염좌」로 보낸 소아 손목(FOOSH), 원위 요골 성장판 위 국소 압통, 열 없음·CRP 정상."
  - "왜: 골막이 두껍고 골형성이 활발한 소아는 1~2주에 골막 가골이 생긴다 — 감염이 아니라 치유의 증거다."
  - "X선이 이미 골절을 보여 주므로 MRI 는 치료를 바꾸지 않는다 — MRI 는 X선이 정상인데 압통이 남을 때."
  - "급성·크게 전위된 골절은 정복(필요하면 핀), 외상 없이 열·CRP 상승·용해성 병변이면 골수염 평가."
pitfalls:
  - contrast: "영상 추가(MRI) vs X선으로 끝난 진단"
    point: "MRI 는 X선에 골절선이 없는데 성장판·주상골 압통이 계속될 때 숨은 골절을 찾는 검사다. 이 X선은 이미 성장판을 지나 골간단으로 나가는 골절선과 가골을 보여 준다 — 진단이 끝났으니 추가 영상은 치료(석고 고정)를 바꾸지 않는다 [[?rockwood-9: Fractures of the distal radius and ulna]]."
    exception: "X선이 정상이고 성장판 위 압통이 뚜렷하면 Salter-Harris I 형을 배제하지 못해 고정 후 재평가하거나 MRI 를 고려한다."
    cites: ["?rockwood-9: Fractures of the distal radius and ulna"]
    covers: ["imaging-2026-0576:D"]
  - contrast: "골막 신생골 = 골수염?"
    point: "분명한 외상, 좋아지는 통증, 열 없음·CRP 정상, 성장판을 지나는 골절선이 있으면 골막 신생골은 골절 가골이다. 골수염은 외상이 없거나 사소하고, 통증이 나빠지며, 열·CRP 상승과 골간단 용해성 병변을 보인다."
    cites: ["?rockwood-9: Fractures of the distal radius and ulna"]
  - contrast: "성장판 골절 = 정복·핀?"
    point: "도수 정복·경피 핀은 급성이고 전위·각형성이 큰 골절의 처치다. 2주가 지나 가골이 생긴 비전위 골절을 늦게 정복하면 성장판을 더 다치게 한다 — 그대로 석고로 고정한다 [[?rockwood-9: Fractures of the distal radius and ulna]]."
    cites: ["?rockwood-9: Fractures of the distal radius and ulna"]
tables:
  - id: salter-harris
    section: "가르는 소견 — 골절선이 어디를 지나는가"
    title: "Salter-Harris 분류 — 골절선의 경로"
    role: differential
    span: column
    columns: ["유형", "골절선", "특징"]
    rows:
      - ["I", "성장판만 가로지름", "X선이 정상일 수 있음 — 압통으로 의심 [[?salter-harris-1963]]"]
      - ["II", "성장판 → 골간단", "가장 흔함, 골간단 삼각 조각(Thurston Holland) [[?salter-harris-1963]]"]
      - ["III", "성장판 → 골단(관절면)", "관절면 침범 — 해부학적 정복 [[?salter-harris-1963]]"]
      - ["IV", "골간단 → 성장판 → 골단", "관절면·성장판 모두 — 정복·고정 [[?salter-harris-1963]]"]
      - ["V", "성장판 압궤", "처음 X선은 정상일 수 있고 나중에 성장 장애 [[?salter-harris-1963]]"]
diagram:
  title: "소아 손목 외상 2주 뒤 — 무엇을 할까"
  nodes:
    - {id: start, kind: start, text: "넘어진 뒤 2주 지속되는 손목 통증"}
    - {id: sys, kind: decision, text: "열·CRP 상승·악화하는 통증?"}
    - {id: osteo, kind: alert, text: "골수염 평가 — 영상·항생제·생검"}
    - {id: xr, kind: decision, text: "X선에 성장판 골절선이 보이나?"}
    - {id: occult, kind: info, text: "압통 지속 → 고정 후 재평가·MRI"}
    - {id: disp, kind: decision, text: "전위·각형성이 큰가?"}
    - {id: cast, kind: end, text: "석고 고정 3~4주"}
    - {id: ortho, kind: end, text: "정형외과 — 정복 여부 판단"}
  edges:
    - {from: start, to: sys}
    - {from: sys, to: osteo, label: "예"}
    - {from: sys, to: xr, label: "아니오"}
    - {from: xr, to: disp, label: "예"}
    - {from: xr, to: occult, label: "아니오"}
    - {from: disp, to: cast, label: "아니오"}
    - {from: disp, to: ortho, label: "예"}
diagram_notes:
  - "2주가 지나 가골이 생긴 골절을 늦게 정복하면 성장판을 더 다칠 수 있다 — 정복 여부는 정형외과가 정한다 [[?rockwood-9: Fractures of the distal radius and ulna]]."
  - "성장판 골절은 고정 뒤 성장 장애(성장 정지·각 변형)를 추적한다 [[?rockwood-9: Fractures of the distal radius and ulna]]."
  - "2세 미만, 설명과 맞지 않는 손상, 시기가 다른 여러 골절이면 학대 평가(골격 조사)를 한다 — 이 도식 밖."
checks:
  - q: "넘어진 지 2주, 원위 요골 성장판에서 배측 골간단으로 나가는 골절선과 얇은 골막 신생골, 열 없음·CRP 정상. 다음 처치는?"
    a: "치유 중인 Salter-Harris II 골절 — 단상지 석고 고정 3~4주."
  - q: "이 소견을 골수염과 무엇으로 가르나?"
    a: "분명한 외상·좋아지는 통증·열 없음·CRP 정상·성장판을 지나는 골절선(용해성 병변 아님)."
sources:
  - id: rockwood-9
    org: "Wolters Kluwer"
    title: "Rockwood and Wilkins' Fractures in Children, 9th ed. — Fractures of the distal radius and ulna"
    kind: textbook
    year: 2019
    citation: "Waters PM, Skaggs DL, Flynn JM (eds). Rockwood and Wilkins' Fractures in Children, 9th ed. 장 'Fractures of the distal radius and ulna'(쪽 미확인)"
    checked_at: 2026-11-09
    checked: "서지만(원문 미대조 — 검토 항목). 문항 해설의 근거 목록에서 옮겼고 이 컨테이너에서 교과서 본문을 열지 못했다. 고정 기간·늦은 정복의 위험은 원문 미대조"
    verified: citation
  - id: salter-harris-1963
    org: "J Bone Joint Surg Am"
    title: "Injuries involving the epiphyseal plate"
    kind: other
    year: 1963
    citation: "Salter RB, Harris WR. Injuries involving the epiphyseal plate. J Bone Joint Surg Am. 1963;45(3):587-622"
    url: "https://journals.lww.com/jbjsjournal/"
    checked_at: 2026-11-09
    checked: "서지만(원문 미대조 — 검토 항목). 분류의 다섯 유형은 이 원 논문의 것이다. PMID·DOI 미확인 — url 은 학술지 누리집이다"
    verified: citation
variants:
  - id: v1
    of: imaging-2026-0576
    flip: true
    changed: "분명한 넘어짐·열 없음·CRP 정상·성장판 골절선 → 외상 없음·38.9 °C 발열·CRP 상승·골간단 용해성 병변과 골막 반응 ⇒ 정답이 석고 고정에서 정맥 항생제와 골생검으로"
    context: "같은 소아 손목 통증, 소견을 글로 바꾼 변형(그림 없음)"
    stem: "A 9-year-old boy is brought to the physician because of left wrist pain that has worsened over 2 weeks. There was no injury. He has had a temperature of 38.9°C (102°F) for 4 days and now refuses to use his hand. Examination shows warmth, swelling, and point tenderness over the dorsal aspect of the distal radius. Sensation and capillary refill in the hand are normal. Serum C-reactive protein concentration is markedly elevated. A lateral radiograph of the wrist shows an ill-defined lytic area in the distal radial metaphysis with periosteal new bone along the dorsal cortex; no fracture line crosses the physis. Which of the following is the most appropriate next step in management?"
    choices: ["A. Short arm cast immobilization for 3 to 4 weeks", "B. Intravenous cefazolin and bone biopsy", "C. Closed reduction and percutaneous pinning", "D. Repeat radiograph in 2 weeks", "E. Skeletal survey for suspected physical abuse"]
    answer: "B"
    explanation: "Without trauma, with fever, worsening pain, an elevated CRP, and a lytic metaphyseal area, the periosteal new bone now signals infection rather than fracture healing — acute hematogenous osteomyelitis, treated with intravenous antistaphylococcal antibiotics and bone sampling. In the original item, a clear fall, normal CRP, and a fracture line through the physis made the periosteal reaction fracture callus, treated with a cast."
    kind: application
  - id: v2
    of: imaging-2026-0576
    flip: false
    changed: "12세 여아·롤러스케이트·X선 그림 → 13세 남아·축구 중 손 짚고 넘어짐·소견을 글로 제시 ⇒ 2주 경과·열 없음·CRP 정상·성장판→골간단 골절선과 매끈한 골막 신생골·전위 없음이라는 결정 단서는 같아 답은 그대로 석고 고정"
    context: "겉모습만 바꾼 글 변형(그림 없음)"
    stem: "13세 남자가 2주 전 축구를 하다 손을 짚고 넘어진 뒤 오른쪽 손목 통증이 계속되어 왔다. 넘어진 날 동네 의원에서 염좌라는 말을 듣고 압박 붕대를 감았다. 통증은 줄었지만 팔굽혀펴기를 하면 다시 아프다. 열은 없다. 원위 요골 배측, 손목 주름 바로 위에 국소 압통과 약간의 부종이 있고 손의 감각과 모세혈관 재충만은 정상이다. 혈청 C 반응단백은 정상이다. 손목 측면 단순 X선에서 열려 있는 원위 요골 성장판에서 배측 골간단으로 비스듬히 나가는 골절선과 배측 피질을 따라 얇고 매끈한 골막 신생골이 보이며 전위·각형성은 거의 없다. 가장 적절한 처치는?"
    choices: ["A. 손목 MRI 를 찍는다", "B. 정맥 세파졸린을 투여하고 골생검을 한다", "C. 도수 정복 후 경피 핀 고정을 한다", "D. 단상지 석고로 3~4주 고정한다", "E. 신체 학대를 의심해 골격 조사를 한다"]
    answer: "D"
    explanation: "환자와 사고 상황이 바뀌었지만 결정 단서는 같다 — 분명한 외상 2주 뒤, 열 없음·CRP 정상, 성장판을 지나 골간단으로 나가는 골절선(Salter-Harris II)과 매끈한 골막 신생골(가골), 전위 없음. 치유 중인 비전위 골절이라 석고로 고정한다. X선이 이미 진단을 했으므로 MRI 는 치료를 바꾸지 않고, 늦은 정복은 성장판을 더 다치게 한다."
    kind: application
figures:
- id: f1
  file: docs/assets/figures/graz-0819_0768805556_02_wri-l2_f012.jpg
  kind: radiograph
  at: 기전 — 약한 성장판에서 두꺼운 골막의 가골로
  shows: 소아 원위 요골 성장판 골절(AO 소아 23r-E/2.1 — Salter-Harris II 형), 손목 측면
  look_for:
  - 열린 원위 요골 성장판과 그 바로 위 배측 골간단의 골절 부위
  - 배측 피질을 따라 얇게 붙은 골막 신생골
  label: healing pediatric wrist fracture (periosteal reaction) · AO/OTA 소아 분류 23r-E/2.1; 23u-E/7 — 골절 주석 상자 1개
  label_basis: dataset_expert
  reference: 소아 손목 X선의 골절·골막반응 등을 전문가가 상자로 주석
  paper: Nagy E 외. A pediatric wrist trauma X-ray dataset (GRAZPEDWRI-DX) for machine learning. Sci Data 2022;9:222
  doi: 10.1038/s41597-022-01328-z
  credit: GRAZPEDWRI-DX (figshare, CC BY 4.0)
  license: Creative Commons Attribution 4.0 International
  url: https://figshare.com/articles/dataset/GRAZPEDWRI-DX/14825193
  asset: GRAZ-0819_0768805556_02_WRI-L2_F012
  paper_cited_by: 101
---

## 판단 — 왜 석고 고정이 먼저인가
- **진단은 X선이 끝냈다**: 골절선이 성장판을 지나 골간단으로 나가면 Salter-Harris II 형이다 [[?salter-harris-1963]]. 추가 영상은 치료를 바꾸지 않는다.
- **골막 신생골은 시간표다**: 외상 2주 뒤 매끈한 골막 반응은 가골이다 — 열·CRP 가 정상이면 감염을 먼저 생각할 이유가 없다.
- **전위가 없으면 정복하지 않는다**: 이미 붙기 시작한 비전위 골절은 석고로 3~4주 더 고정한다 [[?rockwood-9: Fractures of the distal radius and ulna]].

## 기전 — 약한 성장판에서 두꺼운 골막의 가골로
소아의 연골 성장판은 주변 인대·뼈보다 약해서, 어른이라면 손목 염좌가 될 손 짚고 넘어짐(fall on an outstretched hand, FOOSH)이 성장판을 떼어 낸다. II 형은 골절선이 성장판의 비대층을 따라가다 골간단으로 빠져나가, 골단에 붙은 골간단 삼각 조각(Thurston Holland 조각)을 남긴다 [[?salter-harris-1963]]. 소아 골막은 두껍고 골형성 능력이 커서 외상 뒤 1~2주면 골막 아래 새 뼈(가골)가 X선에 보인다 [[?rockwood-9: Fractures of the distal radius and ulna]]. 첫날 X선에서 골절선이 미묘해 염좌로 보냈다가, 2주 뒤 가골로 골절이 드러나는 경우가 흔하다.

## 가르는 소견 — 골절선이 어디를 지나는가
- 다섯 유형은 골절선이 성장판·골간단·골단 중 어디를 지나는지로 나뉜다(표). 관절면을 지나는 III·IV 형은 해부학적 정복이 필요하다 [[?salter-harris-1963]].
- 정상 X선의 해석 한계: I·V 형은 처음 X선이 정상일 수 있다 — 성장판 위 압통이 남으면 고정 후 재평가하고, 그때 MRI 가 의미를 가진다.
- 골수염과의 구분은 영상만이 아니라 외상력·통증 경과·발열·CRP 를 함께 본다.

## 권고와 예외
- 성장판 골절은 고정 뒤 성장 정지·각 변형이 생길 수 있어 추적한다 [[?rockwood-9: Fractures of the distal radius and ulna]].
- 2세 미만, 설명과 맞지 않는 손상, 시기가 다른 여러 골절이면 학대를 평가한다.
