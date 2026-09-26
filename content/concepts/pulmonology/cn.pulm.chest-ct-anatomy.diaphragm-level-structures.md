---
id: cn.pulm.chest-ct-anatomy.diaphragm-level-structures
type: concept
topic: Pulmonology
see_also: [Anatomy, Radiology]
date: 2026-09-23
updated: 2026-09-26
version: 2
outline: h286            # 기본틀 슬롯(content/outline/subjects.yaml) — 해리슨 21판 286장 Diagnostic Procedures in Respiratory Disease(호흡기내과 책)
confidence: medium
review_status: unreviewed
note_form: 2            # 판형 2(2026-09-25) — [restyle] 재배치만, 새 사실 없음
title: "흉부 CT 가로막 높이 — 구조를 자리로 확정하고 높이를 붙인다"
objective: "심실 높이·폐 바닥 흉부 CT 축상면에서 가로막 주변 정상 구조(하행대동맥·식도·홀정맥·가로막돔과 간)를 위치·모양·위아래 연속성으로 식별해 병변(경화·무기폐·흉수·종괴)과 가르고, 각 구조가 가로막을 지나는 높이(대정맥구멍 T8·식도구멍 T10·대동맥구멍 T12)에 연결한다"
objective_kind: 감별
condition: 흉부 CT 정상 해부 — 세로칸·가로막
exams: [kmle, usmle]
summary:
  - "결론: 척추체 왼쪽 앞의 크고 둥근 단면은 하행대동맥(T12), 폐 바닥 앞쪽의 균질한 둥근 음영은 가로막돔과 간이다."
  - "시험 단서: 심실 높이·폐 바닥 축상 CT(폐창), 증상 없는 검진 — 대동맥구멍(aortic hiatus)·가로막돔(hemidiaphragm dome)."
  - "왜: 폐창에서는 폐보다 짙은 구조가 모두 희게 뭉친다 — 밀도가 아니라 자리·모양·위아래 연속성으로 읽는다."
  - "가로막 구멍: 대정맥구멍 T8(중심널힘줄) · 식도구멍 T10(오른다리 근육) · 대동맥구멍 T12(두 다리·정중활꼴인대 뒤)."
  - "돔 단서: 매끈한 볼록 경계·완전히 균질·주변 폐 정상·아래 단면에서 간과 이어짐 — 한 장으로 병변을 부르지 않는다."
criteria:
  - id: hiatus-levels
    name: 가로막 구멍의 척추 높이
    kind: 해부 기준
    population: "성인 가로막"
    statement: "대정맥구멍 T8(중심널힘줄 안, 아래대정맥·오른가로막신경 가지) · 식도구멍 T10(오른다리 근육섬유, 식도·앞뒤 미주신경줄기) · 대동맥구멍 T12(두 다리와 정중활꼴인대 뒤·척추체 앞, 대동맥·가슴림프관·홀정맥) [[?moore-coa]]"
    exceptions: "높이는 호흡·자세·개인에 따라 한 척추 정도 달라질 수 있다 — 시험은 T8·T10·T12 를 쓴다"
    source: moore-coa
    basis: current
    exams: [kmle, usmle]
  - id: ct-window
    name: CT 감쇠값과 창 설정
    kind: 검사 원리
    population: "흉부 CT"
    statement: "감쇠는 하운스필드 단위로 재며 물 0, 공기 −1000 HU 이다. 창 너비·중심을 골라 보여 줄 범위를 정한다 — 폐창에서는 폐보다 짙은 구조가 모두 희게, 세로칸창에서는 폐가 검게 보인다. 창 설정은 복셀의 HU 값을 바꾸지 않는다 [[harrison-21: 286장 p.2143]]"
    exceptions: "창 설정으로는 병변과 정상 구조가 갈리지 않는다 — 위치·모양·연속성으로 가른다"
    source: harrison-21
    basis: current
    exams: [kmle, usmle]
sources:
  - id: harrison-21
    org: "McGraw Hill"
    title: "Harrison's Principles of Internal Medicine, 21st ed. — Chapter 286: Diagnostic Procedures in Respiratory Disease"
    kind: textbook
    year: 2022
    citation: "Loscalzo J, Fauci AS, Kasper DL, et al (eds). Harrison's Principles of Internal Medicine, 21e. 286장 Diagnostic Procedures in Respiratory Disease(Washko GR, Goldberg HJ, Shafiq M), 인쇄쪽 2140–2146"
    checked_at: 2026-09-23
    checked: "드라이브 장 문서로 본문 대조. p.2143 흉부 사진(2차원 투영이라 겹친 구조를 여러 방향으로 풀어야 함, 가로막 거상은 폐 밖 원인), CT(흉곽 모든 구조의 공간 재구성, 감쇠 HU — 물 0·공기 −1000, 창 너비·중심, 폐창에서는 짙은 구조가 희게·세로칸창에서는 폐가 검게, 창은 HU 값을 바꾸지 않음), 2차 폐소엽. p.2144 폐동맥 줄기 > 3 cm. p.2145 전리 방사선. 가로막 구멍 높이·가로막돔 부분용적 효과는 이 장이 다루지 않는다(해부학·영상의학 교과서 몫)"
    verified: text
  - id: moore-coa
    org: "Wolters Kluwer"
    title: "Clinically Oriented Anatomy — Diaphragm (apertures) and posterior mediastinum"
    kind: textbook
    year: 2018
    citation: "Moore KL, Dalley AF, Agur AMR. Clinically Oriented Anatomy, 8th ed. Wolters Kluwer; 2018 — 가로막 구멍(대정맥구멍·식도구멍·대동맥구멍)"
    checked_at: 2026-09-23
    checked: "서지만(원문 미대조 — 이 컨테이너에서 교과서 본문을 열지 못했다). 문항 해설이 인용한 출처이며 쪽수는 확인하지 못했다(검토 항목)"
    verified: citation
  - id: webb-thoracic
    org: "Wolters Kluwer"
    title: "Thoracic Imaging: Pulmonary and Cardiovascular Radiology — diaphragm and partial-volume effects at the lung bases"
    kind: textbook
    year: 2017
    citation: "Webb WR, Higgins CB. Thoracic Imaging: Pulmonary and Cardiovascular Radiology, 3rd ed. Wolters Kluwer; 2017"
    checked_at: 2026-09-23
    checked: "서지만(원문 미대조). 문항 해설이 인용한 출처이며 가로막돔 부분용적 서술의 쪽수는 확인하지 못했다(검토 항목)"
    verified: citation
tables:
  - id: ct-structures-ventricle-level
    title: "심실 높이 축상 CT — 척추체 앞 구조와 가로막 통과 높이"
    role: comparison
    span: full
    section: "가르는 소견 — 척추체 앞 구조의 자리·모양"
    columns: ["구조", "축상면의 자리·모양", "가로막 통과", "함께 지나는 것"]
    rows:
      - ["하행대동맥", "척추체 **왼쪽 앞**에 붙은 크고(지름 2–3 cm) 둥근 단면, 위아래 단면에서 같은 자리", "대동맥구멍 T12 — 두 다리·정중활꼴인대 뒤 [[?moore-coa]]", "가슴림프관, 홀정맥"]
      - ["식도", "대동맥의 **오른쪽 앞**, 정중 가까이, 납작하고 안에 공기가 있을 수 있음", "식도구멍 T10 — 오른다리 근육섬유 [[?moore-coa]]", "앞·뒤 미주신경줄기"]
      - ["아래대정맥", "심실 높이 흉강에는 거의 없음(간 위 짧은 구간), 척추 오른쪽 앞", "대정맥구멍 T8 — 중심널힘줄 안 [[?moore-coa]]", "오른가로막신경 가지"]
      - ["홀정맥", "척추체 **오른쪽 앞**의 작은 점", "대동맥구멍(또는 오른다리) [[?moore-coa]]", "—"]
    note: "배쪽 가지 높이(복강동맥 T12 부근·위창자간막동맥 L1·아래창자간막동맥 L3·대동맥 갈림 L4)는 「가로막 통과」와 다른 질문이다 — 원문 미대조."
  - id: base-density-differential
    title: "폐 바닥의 연부조직 음영 — 가로막돔 vs 병변"
    role: differential
    span: full
    section: "가르는 소견 — 폐 바닥의 둥근 음영"
    columns: ["소견", "모양·내부", "주변 폐", "위아래 단면"]
    rows:
      - ["가로막돔 + 간(정상)", "매끈하고 폐 쪽으로 볼록, 완전히 균질, 오른쪽 앞 바닥", "정상, 부피 감소 없음", "아래로 갈수록 커져 간과 이어짐 [[?webb-thoracic]]"]
      - ["폐엽 경화", "폐엽 모양, **공기기관지조영상**, 불균질", "부피 유지, 틈새가 곧은 경계", "폐엽 범위에 머묾"]
      - ["무기폐", "쐐기·삼각형, 혈관이 모임", "**부피 감소** — 틈새·폐문·세로칸이 끌려감", "폐엽 범위에 머묾"]
      - ["흉수", "흉벽을 따른 초승달, 누운 자세에서 **뒤쪽(의존 부위)**", "앞쪽으로 눌린 폐, 메니스커스", "뒤쪽 바닥에 층을 이룸"]
      - ["폐 종괴", "불규칙·분엽·침상 경계, 들어가는 혈관", "대개 정상", "가로막 아래 간과 이어지지 않는 독립 구조"]
    note: "모든 행은 문항 해설과 영상의학 교과서 서술을 따른 것이며 교과서 원문 쪽수는 미대조(†)."
pitfalls:
  - contrast: "식도구멍(T10) vs 대동맥구멍(T12) — 「척추 앞의 둥근 관 = 식도」"
    point: "폐창에서는 세로칸 구조가 모두 희게 뭉쳐 보여 밀도로는 대동맥과 식도가 갈리지 않는다 [[harrison-21: 286장 p.2143]]. 가르는 것은 자리와 모양이다 — 척추체 **왼쪽 앞**에 붙은 크고 **둥근** 단면은 하행대동맥이고, 식도는 그 **오른쪽 앞·정중** 가까이의 납작한 관이다. 구조를 확정한 뒤 높이를 붙이면 대동맥은 T12, 식도는 T10 이다 [[?moore-coa]]."
    exception: "그림의 구조가 정중 앞의 납작하고 공기가 든 관이라면 식도이고 답은 T10 이다."
    covers: ["imaging-2026-0012:B"]
  - contrast: "가로막돔(간) vs 폐 종괴 — 「폐로 둘러싸인 둥근 음영 = 종괴」"
    point: "축상면은 휘어진 가로막돔의 꼭대기를 잘라 간을 폐 한가운데의 둥근 연부조직 음영으로 보이게 한다. 종괴와 가르는 단서는 매끈하게 볼록한 경계·완전히 균질한 내부(공기기관지조영상·들어가는 혈관 없음)·정상인 주변 폐, 그리고 아래 단면에서 간과 이어지는 연속성이다 [[?webb-thoracic]]. 한 장으로 병변을 부르지 말고 위아래로 넘겨 본다."
    exception: "경계가 불규칙·분엽·침상이고, 가로막 아래에서 간과 이어지지 않는 독립 구조로 남으면 종괴를 의심한다."
    covers: ["imaging-2026-0013:D"]
  - contrast: "가로막돔 vs 경화·흉수·무기폐"
    point: "경화는 폐엽 모양에 공기기관지조영상이 있고, 흉수는 누운 환자에서 뒤쪽 흉벽을 따라 초승달로 고이며, 무기폐는 틈새·폐문·세로칸을 끌어당긴다. 증상 없는 건강검진 환자의 앞쪽 오른쪽 바닥에 있는 매끈하고 균질한 음영에는 이 셋의 특징이 없다."
    exception: "발열·기침과 함께 공기기관지조영상이 보이면 경화, 뒤쪽 의존 부위의 초승달이면 흉수다."
diagram:
  title: "폐 바닥·심실 높이 축상 CT — 이 둥근 음영은 무엇인가?"
  nodes:
    - {id: start, kind: start, text: "축상 CT 의 둥근 연부조직 음영 — 창·단면 높이 확인"}
    - {id: where, kind: decision, text: "척추체 앞인가, 폐 바닥인가?"}
    - {id: info, kind: info, text: "위아래 단면·세로칸창으로 연속성 확인"}
    - {id: side, kind: decision, text: "왼쪽 앞 둥근 단면인가, 정중 납작한 관인가?"}
    - {id: aorta, kind: end, text: "하행대동맥 — 대동맥구멍 T12"}
    - {id: eso, kind: end, text: "식도 — 식도구멍 T10"}
    - {id: dome, kind: decision, text: "매끈·균질·폐 정상·아래로 간과 이어지나?"}
    - {id: normal, kind: end, text: "가로막돔과 간 — 정상(부분용적 효과)"}
    - {id: lesion, kind: alert, text: "병변 — 경화·무기폐·흉수·종괴는 표로 가른다"}
  edges:
    - {from: start, to: where}
    - {from: where, to: side, label: "척추체 앞"}
    - {from: where, to: dome, label: "폐 바닥"}
    - {from: where, to: info, label: "한 단면뿐"}
    - {from: info, to: side, label: "세로칸 구조"}
    - {from: info, to: dome, label: "가로막 근처"}
    - {from: side, to: aorta, label: "왼쪽 앞·둥긂"}
    - {from: side, to: eso, label: "정중·납작"}
    - {from: dome, to: normal, label: "모두 예"}
    - {from: dome, to: lesion, label: "하나라도 아니오"}
diagram_notes:
  - "표준 표시 방향은 환자의 오른쪽이 그림의 왼쪽이다 — 「왼쪽 앞」은 환자 기준이다."
  - "창 설정은 보이는 방식만 바꾼다(HU 값은 그대로) [[harrison-21: 286장 p.2143]]. 폐창에서 세로칸 구조를 가를 때는 밀도가 아니라 자리로 읽는다."
  - "오른쪽 돔이 왼쪽보다 높아 폐 바닥 단면에서는 오른쪽이 먼저 잘린다 — 같은 높이에서 왼쪽 바닥은 폐가 정상으로 남는다."
  - "홀정맥도 대동맥구멍(또는 오른다리)으로 지나지만 척추 오른쪽 앞의 작은 점이라 「왼쪽 앞의 큰 둥근 단면」과 헷갈리지 않는다."
  - "대동맥구멍으로는 가슴림프관·홀정맥이, 식도구멍으로는 앞·뒤 미주신경줄기가 함께 지난다 [[?moore-coa]]."
  - "병변 쪽 단서 — 공기기관지조영상(경화), 부피 감소(무기폐), 누운 자세 뒤쪽 초승달(흉수), 불규칙 경계로 간과 떨어진 독립 구조(종괴)."
checks:
  - q: "가로막의 세 구멍과 척추 높이는?"
    a: "대정맥구멍 T8(중심널힘줄), 식도구멍 T10(오른다리 근육), 대동맥구멍 T12(두 다리·정중활꼴인대 뒤)."
  - q: "심실 높이 축상 CT 에서 하행대동맥과 식도를 어떻게 가르나?"
    a: "대동맥은 척추체 왼쪽 앞의 크고 둥근 단면, 식도는 그 오른쪽 앞·정중의 납작한 관(공기가 있을 수 있음)."
  - q: "폐창에서 세로칸 구조가 모두 희게 보이는 이유는?"
    a: "폐창은 낮은 감쇠(폐)에 맞춘 창이라 그보다 짙은 구조가 모두 흰색으로 표시된다. HU 값이 바뀐 것이 아니다."
  - q: "폐 바닥의 앞쪽 오른쪽 둥근 음영이 가로막돔임을 보여 주는 네 단서는?"
    a: "매끈한 볼록 경계, 완전히 균질한 내부, 정상인 주변 폐(부피 감소 없음), 아래 단면에서 간과 이어짐."
  - q: "대동맥구멍으로 대동맥과 함께 지나는 구조는?"
    a: "가슴림프관과 홀정맥."
variants:
  - id: v1
    of: imaging-2026-0012
    flip: true
    changed: "묻는 구조를 「척추체 왼쪽 앞의 크고 둥근 단면」에서 「그 오른쪽 앞·정중 가까이의 납작하고 안에 공기가 보이는 관」으로 바꿈 → 구조가 식도가 되어 답이 T12 에서 T10 으로 바뀜"
    context: "단서를 바꿔 답이 바뀌는 변형 — 대동맥 대신 식도"
    stem: "58세 남자가 3년 전 발견된 작은 폐결절의 추적 관찰을 위해 흉부 CT 를 찍었다. 결절은 크기 변화가 없다. 심실 높이의 축상면에서 하행대동맥의 오른쪽 앞, 정중선 가까이에 가운데 작은 공기 음영이 있는 납작한 관 구조물이 보인다. 이 구조물이 가로막을 통과하는 척추 높이는?"
    choices: ["A. 제8등뼈(T8)", "B. 제10등뼈(T10)", "C. 제12등뼈(T12)", "D. 제1허리뼈(L1)", "E. 제4허리뼈(L4)"]
    answer: "B"
    explanation: "하행대동맥의 오른쪽 앞·정중 가까이에 있는 납작하고 안에 공기가 보이는 관은 식도다. 식도는 가로막 오른다리의 근육섬유가 감싸는 식도구멍을 T10 높이에서 지난다 [[?moore-coa]]. 원래 문항은 척추체 왼쪽 앞의 크고 둥근 단면(하행대동맥)을 물어 T12 가 답이었다 — 같은 높이의 영상이라도 「어느 구조인가」가 답을 가른다. T8 은 아래대정맥, L1 은 위창자간막동맥 기시, L4 는 대동맥 갈림 높이다."
    kind: application
  - id: v2
    of: imaging-2026-0012
    flip: false
    changed: "성별·나이(45세 남자)·검사 경위(교통사고 뒤 외상 CT)·창(세로칸창)·제시 순서를 바꾸고 「척추체 왼쪽 앞의 크고 둥근 단면」은 그대로 → 답은 여전히 T12"
    context: "겉모습만 바꾸고 답은 같은 변형 — 외상 CT·세로칸창"
    stem: "45세 남자가 교통사고 뒤 응급실에서 흉부 CT 를 찍었다. 갈비뼈 골절이나 기흉은 없다. 세로칸창의 심실 높이 축상면에서 척추체 왼쪽 앞에 붙어 있는 지름 약 2.5 cm 의 둥글고 균질한 구조물이 보이고, 위아래 단면에서도 같은 자리에 이어진다. 이 구조물이 배안으로 내려가려고 가로막을 지나는 척추 높이는?"
    choices: ["A. 제12등뼈(T12)", "B. 제8등뼈(T8)", "C. 제10등뼈(T10)", "D. 제3허리뼈(L3)", "E. 제1허리뼈(L1)"]
    answer: "A"
    explanation: "창 설정·검사 이유·환자가 달라도 결정 단서(척추체 왼쪽 앞, 크고 둥근 단면, 위아래로 같은 자리)는 그대로이므로 구조는 하행대동맥이다. 대동맥은 가로막의 두 다리와 정중활꼴인대 뒤의 대동맥구멍을 T12 높이에서 지난다 [[?moore-coa]]. 세로칸창은 연부조직 구조를 구분해 보여 줄 뿐 위치 관계로 읽는 방법은 같다 [[harrison-21: 286장 p.2143]]. T8 은 아래대정맥, T10 은 식도, L1·L3 은 배쪽 가지의 기시 높이다."
    kind: application
  - id: v3
    of: imaging-2026-0013
    flip: true
    changed: "「증상 없음, 매끈하고 균질한 앞쪽 음영, 주변 폐 정상」을 「5일간 발열·가래 기침, 뒤쪽 바닥의 폐엽 모양 음영 안에 가지 치는 공기 음영, 틈새가 곧은 경계」로 바꿈 → 답이 가로막돔에서 오른아래엽 경화로 바뀜"
    context: "Changed cue — air bronchograms in a lobe-shaped posterior opacity"
    stem: "A 67-year-old woman comes to the physician because of 5 days of fever and a cough productive of yellow sputum. Her temperature is 38.9°C and respirations are 24/min. Crackles are heard over the right lung base posteriorly. An axial CT image of the chest at the level of the lung bases (lung window) shows a dense opacity filling the posterior basal right lower lobe; branching tubular air lucencies run through it, its anterior border is a straight line along the major fissure, and the right hilum and mediastinum are in normal position. Which of the following best explains the opacity?"
    choices: ["A. Dome of the right hemidiaphragm with the liver beneath it", "B. Loculated right pleural effusion", "C. Consolidation of the right lower lobe", "D. Mass arising in the right middle lobe", "E. Atelectasis of the right lower lobe"]
    answer: "C"
    explanation: "Branching air lucencies inside a lobe-shaped opacity are air bronchograms: the alveoli are filled but the bronchi stay open, which is consolidation, and fever with productive cough fits pneumonia. A straight border along the fissure with no shift of the hilum or mediastinum means the lobe has kept its volume, arguing against atelectasis. In the original item the density was anterior, perfectly homogeneous with a smooth convex edge, in an asymptomatic patient — the diaphragmatic dome. An effusion would be a dependent crescent along the chest wall, and a mass would be a separate structure with an irregular edge [[?webb-thoracic]]."
    kind: application
  - id: v4
    of: imaging-2026-0013
    flip: false
    changed: "성별·나이(59세 남자)·검사 경위(전 흡연자의 저선량 폐암 선별 CT)·제시 순서를 바꾸고 「앞쪽 오른쪽 바닥, 매끈한 볼록 경계, 완전히 균질, 주변 폐 정상, 아래 단면에서 간과 이어짐」은 그대로 → 답은 여전히 가로막돔과 간"
    context: "Same decisive cues, different story — lung cancer screening CT in a former smoker"
    stem: "A 59-year-old man with a 35-pack-year smoking history who quit 5 years ago undergoes low-dose CT of the chest for lung cancer screening. He has no symptoms. On one axial image through the lung bases, a round, homogeneous soft-tissue density with a smooth, convex margin occupies the anterior right lower hemithorax, and aerated lung surrounds it without distortion. On the next caudal images the density becomes progressively larger and becomes continuous with the liver. Which of the following best explains the density?"
    choices: ["A. Primary lung carcinoma in the right middle lobe", "B. Round atelectasis of the right lower lobe", "C. Dome of the right hemidiaphragm with the liver beneath it", "D. Loculated right pleural effusion", "E. Consolidation of the right lower lobe"]
    answer: "C"
    explanation: "Smoking history raises the pretest probability of cancer, but it does not change what the image shows. A smooth convex margin, perfect homogeneity, normal surrounding lung and — decisively — continuity with the liver on caudal images identify the top of the right hemidiaphragmatic dome cut by the axial plane, a geometric partial-volume effect rather than a lesion [[?webb-thoracic]]. A carcinoma would remain a separate structure with an irregular edge, atelectasis would show volume loss, an effusion would lie posteriorly, and consolidation would contain air bronchograms."
    kind: application
---

## 판단 — 왜 구조를 먼저 확정하고 높이를 붙이나
- 영상 판독의 흔한 두 오류는 「정상 구조를 병변으로 부르기」와 「구조를 잘못 식별해 엉뚱한 높이를 붙이기」다.
- 폐창에서는 세로칸 구조가 모두 희게 뭉쳐 밀도로 갈리지 않는다 [[harrison-21: 286장 p.2143]] — 자리·모양으로 대동맥인지 식도인지 먼저 정한다.
- 구조가 정해지면 높이는 따라온다: 대동맥 T12, 식도 T10, 아래대정맥 T8 [[?moore-coa]].
- 폐 바닥의 둥근 음영은 한 장이 아니라 위아래 연속성으로 판단한다 — 아래로 간과 이어지면 가로막돔이다 [[?webb-thoracic]].

## 기전 — 휘어진 가로막과 창 설정에서 소견으로
CT 는 감쇠를 하운스필드 단위(물 0, 공기 −1000 HU)로 재고, 창 너비·중심은 보여 줄 범위만 고른다 — 창을 바꿔도 HU 값은 그대로다 [[harrison-21: 286장 p.2143]]. CT 는 흉곽을 공간적으로 재구성하지만 [[harrison-21: 286장 p.2143]] 한 장의 축상면은 얇은 판이라, 휘어진 가로막돔을 비스듬히 자르면 간의 꼭대기가 폐로 둘러싸인 「덩이」처럼 보인다(부분용적·기하학 효과). 오른쪽 돔은 아래에 간이 있어 왼쪽보다 높아 먼저 잘린다. 가로막은 가운데가 중심널힘줄, 가장자리가 근육인 돔이고, 뒤쪽 두 다리(crura)가 허리뼈에 붙으며 정중활꼴인대가 대동맥 위로 아치를 이룬다. 대정맥구멍(T8)은 널힘줄 안이라 들숨에 벌어져 정맥 환류를 돕고, 식도구멍(T10)은 오른다리 근육이 감싸 수축할 때 역류를 막는 조임근이 되며, 대동맥구멍(T12)은 가로막을 뚫지 않고 그 뒤로 지나 수축해도 눌리지 않는다 [[?moore-coa]].

## 가르는 소견 — 척추체 앞 구조의 자리·모양
- 하행대동맥은 뒤세로칸에서 척추체 왼쪽 앞을 따라 내려가므로 위아래 모든 단면에서 같은 자리에 크고 둥글게 잘린다.
- 식도는 비어 있을 때 납작하고 안에 공기가 있을 수 있으며, 홀정맥은 척추체 오른쪽 앞의 작은 점이다. 심실 높이의 흉강에는 아래대정맥이 거의 보이지 않는다.

## 가르는 소견 — 폐 바닥의 둥근 음영
- 네 질문: 공기기관지조영상이 있는가(경화) · 부피가 줄어 틈새·폐문·세로칸이 끌려가는가(무기폐) · 누운 자세 뒤쪽 흉벽을 따라 초승달로 고였는가(흉수) · 경계가 불규칙하고 간과 떨어진 독립 구조인가(종괴).
- 넷 모두 아니고 경계가 매끈하게 볼록하며 속이 간 실질처럼 완전히 균질하고 아래로 커져 간과 이어지면 가로막돔이다 [[?webb-thoracic]].
- 증상이 없다는 병력은 경화의 가능성을 낮추지만, 흡연력 같은 병력이 영상 소견 자체를 바꾸지는 않는다.

## 권고와 예외
- 확인 순서: 위아래 단면 넘겨 보기 → 창 바꾸기(폐창은 실질, 세로칸창은 연부조직, HU 는 그대로 [[harrison-21: 286장 p.2143]]) → 관상·시상 재구성으로 돔과 간·대동맥 경로를 한 장에 본다.
- 정상 구조이므로 치료 대상이 아니다 — 이 목표의 「처치」는 추가 검사를 하지 않는 것이다. 가로막돔을 종괴로 부르면 불필요한 추적 CT·조직검사로 이어진다. 판독 전에 연속성을 한 번 더 확인하고, 독립 구조로 남는 음영만 병변으로 기술한다.
- 해리슨 286장은 CT 감쇠·창 설정 원리까지만 다루고, 가로막 구멍 높이와 가로막돔 부분용적 효과는 다루지 않는다. 그 서술은 해부학·흉부영상 교과서(Moore·Webb)를 따랐으나 원문 쪽수는 대조하지 못했다(검토 항목).

## 시험 쟁점 — 충돌·맥락·새 근거
- 해당 없음(대조: 해리슨 286장 p.2143~2145 — CT 원리·창 설정 서술이 이 정리본과 일치. 가로막 구멍 높이는 해리슨이 다루지 않아 대조 범위 밖)

## (심화) 왜 대동맥은 가로막을 「뚫지」 않는가
대정맥구멍은 중심널힘줄 안에 있어 가로막이 수축할수록 벌어지고, 식도구멍은 근육에 싸여 수축할수록 조여진다. 대동맥은 이 둘과 달리 가로막 뒤, 두 다리와 정중활꼴인대가 만든 아치 아래로 지나간다. 들숨마다 가로막이 수축해도 심장에서 나온 고압의 혈류가 눌리지 않게 하는 배치다 [[?moore-coa]]. 그래서 대동맥구멍은 세 구멍 중 가장 낮고(T12) 가장 뒤에 있으며, 영상에서 하행대동맥이 가로막 높이까지 척추체 왼쪽 앞에 붙어 있는 이유이기도 하다. 식도는 T10 에서 앞으로 나와 오른다리를 지나 위와 만나고, 아래대정맥은 T8 에서 중심널힘줄을 지나 바로 오른심방으로 들어간다 — 세 구조가 「뒤에서 앞으로, 아래에서 위로」 배열된다.
