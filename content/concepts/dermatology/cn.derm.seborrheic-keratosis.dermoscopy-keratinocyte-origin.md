---
id: cn.derm.seborrheic-keratosis.dermoscopy-keratinocyte-origin
type: concept
topic: Dermatology
see_also: [Pathology]
date: 2026-09-28
updated: 2026-09-28
version: 2
outline: h56            # 기본틀 슬롯 — 해리슨 21판 56장 Approach to the Patient with a Skin Disorder
confidence: medium
review_status: unreviewed
note_form: 2
title: "지루각화증 — 갈색이어도 멜라닌세포 병변이 아니다"
objective: "노인 몸통의 갈색 병변에서 더모스코피의 좁쌀 모양 낭·면포 모양 구멍·뇌이랑 구조와 색소망 부재로 표피 각질세포 증식(지루각화증)을 멜라닌세포 병변과 구별한다"
objective_kind: 진단
condition: 지루각화증(seborrheic keratosis)
exams: [kmle, usmle]
summary:
  - "결론: 색소망 없이 좁쌀 모양 낭·면포 모양 구멍·뇌이랑 구조가 보이면 표피 각질세포 증식 = 지루각화증."
  - "시험 단서: 노인 몸통의 경계 뚜렷한 「붙인 듯한(stuck-on)」 갈색 판 + 더모스코피 milia-like cyst·comedo-like opening."
  - "왜: 갈색은 각질세포가 받은 멜라닌 탓이다 — 멜라닌세포 병변을 가르는 것은 색이 아니라 색소망·소구·줄무늬다."
  - "구조가 애매하거나 최근 변한 병변은 색만으로 판정하지 않고 생검한다."
pitfalls:
  - contrast: "경계부 멜라닌세포 증식(흑색종·경계모반) vs 각질세포 증식 — 「갈색 = 멜라닌세포?」"
    point: "경계부 멜라닌세포 병변은 표피 능선을 따라 멜라닌이 모여 색소망·소구·줄무늬를 만든다. 색소망이 없고 각질 구조(좁쌀 모양 낭·면포 모양 구멍)가 있으면 멜라닌은 각질세포에 옮겨진 것이다 [[?argenziano-2003]]."
    exception: "심하게 색소가 많은 지루각화증은 흑색종처럼 어둡고 불규칙해 보일 수 있다 — 구조가 애매하면 생검한다."
    covers: ["imaging-2026-0137:A"]
  - contrast: "진피 모반 vs 지루각화증"
    point: "진피 모반은 진피에 둥지를 튼 모반세포로, 부드러운 돔 모양 구진이며 각질 구조가 없다. 지루각화증은 표피가 두꺼워진 판이라 표면이 거칠고 「붙인 듯」하다 [[harrison-21: 56장 p.369–370]]."
tables:
  - id: origin-ddx
    section: "가르는 소견 — 색소망이냐 각질 구조냐"
    title: "갈색 병변 — 기원 세포와 더모스코피"
    role: differential
    span: column
    columns: ["병변(기원 세포)", "가르는 소견"]
    rows:
      - ["지루각화증(표피 각질세포)", "좁쌀 모양 낭·면포 모양 구멍·뇌이랑 구조, 색소망 없음, 경계 뚜렷 [[?argenziano-2003]]"]
      - ["흑색종·경계모반(경계부 멜라닌세포)", "색소망(흑색종은 비정형)·소구·줄무늬·청백색 베일"]
      - ["진피 모반(진피 모반세포)", "부드러운 돔 구진, 소구·쉼표 모양 혈관"]
      - ["피부섬유종(진피 섬유모세포)", "단단한 구진, 옆에서 누르면 움푹(dimple) [[harrison-21: 56장 p.370]]"]
      - ["피지샘 증식(피지샘 세포)", "얼굴의 노란 배꼽 구진, 왕관 모양 혈관"]
criteria:
  - id: sk-clinical
    name: 지루각화증의 임상 양상
    kind: 진단 기준
    population: "색소성 피부 병변"
    statement: "몸통·얼굴·팔다리의 갈색 판, 붙어 있는 기름진 비늘, 「붙인 듯한(stuck-on)」 모양 [[harrison-21: 56장 p.370]]"
    exceptions: "더모스코피 구조와 기원 세포는 해리슨에 없다 — [[?argenziano-2003]]·[[?bolognia-4]]"
    source: harrison-21
    basis: current
    exams: [kmle, usmle]
  - id: dermoscopy-step1
    name: 더모스코피 1단계 — 멜라닌세포 병변인가
    kind: 진단 기준
    population: "색소성 피부 병변"
    statement: "색소망·집합 소구·줄무늬가 있으면 멜라닌세포 병변, 없으면 비멜라닌세포 병변의 특징(지루각화증의 좁쌀 모양 낭·면포 모양 구멍 등)을 찾는다 [[?argenziano-2003]]"
    exceptions: "더모스코피는 육안에 안 보이는 구조를 보여 주며 색소 병변 평가에 특히 유용하다 [[harrison-21: 56장 p.373]]"
    source: argenziano-2003
    basis: current
    exams: [kmle, usmle]
sources:
  - id: harrison-21
    org: "McGraw Hill"
    title: "Harrison's Principles of Internal Medicine, 21st ed. — Chapter 56: Approach to the Patient with a Skin Disorder"
    kind: textbook
    year: 2022
    citation: "Loscalzo J, Fauci AS, Kasper DL, et al (eds). Harrison's Principles of Internal Medicine, 21e. 56장 p.369–373"
    checked_at: 2026-09-28
    checked: "드라이브 장 문서로 본문 대조. p.369 — 흑색종 ABCDE(그림 56-1), 모반은 모반멜라닌세포의 양성 증식으로 모양이 규칙적이고 색이 고름(그림 56-2); p.370 표 56-4 — 지루각화증: 몸통·얼굴·팔다리, 붙어 있는 기름진 비늘의 갈색 판, 「stuck on」; 피부섬유종: 옆에서 누르면 움푹; p.372 그림 56-6 분포(등의 지루각화증); p.373 — 더모스코피는 육안에 안 보이는 구조·색·양상을 보여 주며 색소 병변 평가에 특히 유용. 지루각화증의 기원 세포(각질세포)·더모스코피 구조(좁쌀 모양 낭·면포 모양 구멍)는 이 장에 없다"
    verified: text
  - id: argenziano-2003
    org: "Argenziano G, Soyer HP, et al (합의 회의)"
    title: "Dermoscopy of pigmented skin lesions: results of a consensus meeting via the Internet"
    kind: review
    year: 2003
    citation: "J Am Acad Dermatol 2003;48(5):679-693"
    doi: "10.1067/mjd.2003.281"
    checked_at: 2026-09-28
    checked: "서지만(원문 미대조 — 이 컨테이너는 PubMed·doi.org 를 막는다). 문항 해설 근거 목록에서 옮겼고, DOI 는 기억으로 적었다(학습서 워크플로가 PMID 를 찾아 확인)"
    verified: citation
  - id: bolognia-4
    org: "Elsevier"
    title: "Dermatology, 4th ed. — Benign epidermal tumors and proliferations"
    kind: textbook
    year: 2018
    citation: "Bolognia JL, Schaffer JV, Cerroni L (eds). Dermatology, 4th ed. — seborrheic keratosis(쪽 미확인)"
    checked_at: 2026-09-28
    checked: "서지만(원문 미대조 — 검토 항목)"
    verified: citation
diagram:
  title: "갈색 병변 — 더모스코피로 기원 세포 가르기"
  nodes:
    - {id: start, kind: start, text: "노인 몸통의 경계 뚜렷한 갈색 판"}
    - {id: net, kind: decision, text: "색소망·소구·줄무늬가 있는가?"}
    - {id: look, kind: info, text: "더모스코피로 구조를 본다 — 색만으로 판정 않음"}
    - {id: mel, kind: alert, text: "멜라닌세포 병변 — 비정형이면 생검"}
    - {id: horn, kind: decision, text: "좁쌀 모양 낭·면포 모양 구멍·뇌이랑?"}
    - {id: sk, kind: end, text: "지루각화증 — 표피 각질세포 증식"}
    - {id: bx, kind: alert, text: "구조 애매·최근 변화 → 생검"}
  edges:
    - {from: start, to: net}
    - {from: start, to: look, label: "미시행"}
    - {from: look, to: net, label: "시행"}
    - {from: net, to: mel, label: "있음"}
    - {from: net, to: horn, label: "없음"}
    - {from: horn, to: sk, label: "있음"}
    - {from: horn, to: bx, label: "없음·애매"}
diagram_notes:
  - "색소 기저세포암도 색소망이 없지만 나뭇가지 모양 혈관·청회색 난원 둥지·잎 모양 영역·궤양을 보인다 — 각질 구조가 없으면 이쪽을 생각한다 [[?argenziano-2003]]."
  - "지루각화증의 갈색은 증식한 각질세포에 옮겨진 멜라닌이다 — 멜라닌세포 수가 늘어난 것이 아니다 [[?bolognia-4]]."
checks:
  - q: "더모스코피에서 색소 병변을 볼 때 가장 먼저 묻는 질문은?"
    a: "멜라닌세포 병변인가 — 색소망·소구·줄무늬가 있는가."
  - q: "좁쌀 모양 낭과 면포 모양 구멍은 무엇을 반영하나?"
    a: "두꺼워진 표피 안의 각질 낭과 표면으로 열린 각질 마개 — 지루각화증의 표지."
  - q: "지루각화증이 갈색인 이유는?"
    a: "증식한 표피 각질세포가 멜라닌을 받았기 때문이다 — 멜라닌세포 증식이 아니다."
variants:
  - id: v1
    of: imaging-2026-0137
    flip: true
    changed: "「색소망 없음 + 좁쌀 모양 낭·면포 모양 구멍·뇌이랑 구조」를 「비정형 색소망(굵고 불규칙하게 끊김) + 불규칙 소구 + 청백색 베일, 1년 사이 커짐」으로 바꿈 → 각질세포가 아니라 경계부 멜라닌세포 증식(흑색종)이 정답"
    context: "단서를 바꿔 답이 바뀌는 변형 — 비정형 색소망"
    stem: "A 72-year-old man comes to the physician because his daughter noticed that a brown spot on his upper back has become larger over the past year. It is not painful and has never bled. He worked as a fisherman for 45 years. Examination shows a 1.2-cm, flat, brown-black lesion with an irregular border on the upper back. Dermoscopy shows a thick, irregular pigment network that ends abruptly at the periphery, irregularly distributed dots and globules, and a central blue-white veil. No milia-like cysts or comedo-like openings are seen. The lesion is most likely a proliferation of which of the following cell types?"
    choices: ["A. Epidermal keratinocytes", "B. Melanocytes at the dermoepidermal junction", "C. Dermal fibroblasts", "D. Sebaceous gland cells", "E. Nevus cells nested in the dermis"]
    answer: "B"
    explanation: "A pigment network, irregular globules, and a blue-white veil are melanocytic structures, and the lesion has changed in size, one of the ABCDE warning signs [[harrison-21: 56장 p.369]]. This is a proliferation of junctional melanocytes (melanoma until proven otherwise) [[?argenziano-2003]]. In the original item there was no pigment network and there were keratin structures (milia-like cysts, comedo-like openings), so the pigment belonged to keratinocytes."
    kind: application
  - id: v2
    of: imaging-2026-0137
    flip: false
    changed: "나이·성별(68세 여자)·부위(아래 등→허리)·내원 경위(속옷에 걸려 피부과 방문)·병력(가려움 대신 여러 개)·제시 순서를 바꾸고 「경계 뚜렷한 갈색 판 + 색소망 없음 + 좁쌀 모양 낭·면포 모양 구멍」은 그대로 → 답은 여전히 표피 각질세포"
    context: "겉모습만 바꾸고 답은 같은 변형 — 허리의 붙인 듯한 갈색 판"
    stem: "A 68-year-old woman comes to the dermatology clinic because a raised brown spot on her lower back catches on her waistband. She has had several similar spots on her trunk for years. She has type 2 diabetes treated with metformin. Examination shows a 1-cm, sharply demarcated, slightly raised brown plaque with a rough, waxy surface that looks stuck on to the skin. Dermoscopy shows multiple round white-yellow milia-like cysts and dark comedo-like openings with no pigment network. The lesion is most likely a proliferation of which of the following cell types?"
    choices: ["A. Dermal fibroblasts", "B. Nevus cells nested in the dermis", "C. Epidermal keratinocytes", "D. Melanocytes at the dermoepidermal junction", "E. Sebaceous gland cells"]
    answer: "C"
    explanation: "The decisive cues are unchanged: a sharply demarcated stuck-on brown plaque [[harrison-21: 56장 p.370]] with milia-like cysts and comedo-like openings and no pigment network [[?argenziano-2003]]. That is seborrheic keratosis, a benign proliferation of epidermal keratinocytes. The patient's sex, site, reason for visit, and diabetes differ from the original item but do not change the reading."
    kind: application
figures:
- id: f1
  file: docs/assets/figures/isic-isic_0001104.jpg
  kind: dermoscopy
  at: 기전 — 두꺼워진 표피에서 각질 구조로
  shows: 조직검사로 확진된 지루각화증의 더모스코피
  look_for:
  - 병변 안의 흰·노란 둥근 좁쌀 모양 낭
  - 짙은 갈색 면포 모양 구멍
  - 색소망 없이 가장자리의 굵은 손가락 모양 구조
  label: Seborrheic keratosis — 조직병리 확진
  label_basis: dataset_expert
  reference: 이미지마다 조직병리 검사로 확진(ISIC 기록 diagnosis_confirm_type = histopathology)
  paper: 'Codella NCF 외. Skin lesion analysis toward melanoma detection: a challenge at ISBI 2017. ISBI 2018:168-172'
  doi: 10.1109/ISBI.2018.8363547
  credit: ISIC Archive ISIC_0001104 (CC-0)
  license: CC0 1.0 Universal
  url: https://www.isic-archive.com/collections?imageId=ISIC_0001104
  asset: ISIC-ISIC_0001104
  paper_cited_by: 1935
---

## 판단 — 왜 각질세포 증식인가
- 더모스코피는 먼저 **멜라닌세포 병변인가**를 묻는다 — 색소망·소구·줄무늬가 그 표지다 [[?argenziano-2003]]. 더모스코피는 육안에 안 보이는 구조를 보여 주며 색소 병변 평가에 특히 유용하다 [[harrison-21: 56장 p.373]].
- 색소망이 없고 **좁쌀 모양 낭(milia-like cyst)·면포 모양 구멍(comedo-like opening)·뇌이랑 구조**가 있으면 표피 각질세포 증식, 지루각화증이다.
- 임상 모양도 맞는다 — 몸통의 기름진 비늘이 붙은 갈색 판, 「붙인 듯한」 모양 [[harrison-21: 56장 p.370]].

## 기전 — 두꺼워진 표피에서 각질 구조로
지루각화증은 기저세포 모양의 각질세포가 증식해 표피가 위로 두꺼워진 판이다. 두꺼운 표피 안에 갇힌 각질 덩어리(각질 낭)는 위에서 보면 흰·노란 **좁쌀 모양 낭**, 표면으로 열린 각질 마개는 짙은 **면포 모양 구멍**으로 보인다. 주름진 유두종 표면은 틈과 융기를 만들어 **뇌이랑 모양**이 된다. 증식은 표피 위쪽으로만 일어나 경계가 뚜렷하고 「붙인 듯」하다 [[?bolognia-4]]. 갈색은 증식한 각질세포가 이웃 멜라닌세포로부터 받은 멜라닌이다 — 그래서 색은 짙어도 멜라닌이 표피 능선을 따라 모여 만드는 색소망은 생기지 않는다.

## 가르는 소견 — 색소망이냐 각질 구조냐
- 표가 기원 세포별 소견이다. 색(갈색·검정)은 기원을 가르지 못한다.
- **음성 소견의 한계**: 색소망이 없다고 모두 지루각화증은 아니다 — 색소 기저세포암·무색소 흑색종도 색소망이 없다. 각질 구조가 **함께** 있어야 한다.
- 노인 몸통의 여러 개 병변·자외선 노출 직업은 흑색종 위험을 떠올리게 하지만 진단은 구조로 한다.

## 권고와 예외
- 구조가 분명하고 변화가 없으면 임상 진단으로 끝나고 치료는 필요 없다. 구조가 애매하거나 최근 변했으면 생검한다(흑색종 ABCDE 의 E) [[harrison-21: 56장 p.369]].
- 더모스코피 구조의 정의와 지루각화증의 조직 기원은 해리슨 56장에 없어 [[?argenziano-2003]]·[[?bolognia-4]] 서지만 남겼다(†, 검토 항목).

## 시험 쟁점 — 충돌·맥락·새 근거
- 해당 없음(대조: 해리슨 56장 p.369–373 — 임상 양상·더모스코피 용도만 다루고 어긋난 서술 없음).
