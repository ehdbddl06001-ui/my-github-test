---
id: cn.path.ovarian-mature-cystic-teratoma.malignant-transformation-type
type: concept
topic: Obstetrics & Gynecology
see_also: [Pathology]
date: 2026-10-03
updated: 2026-10-03
version: 2
outline: gyn.oncology            # 산부인과 손 슬롯 「부인암 — 자궁경부·자궁내막·난소·융모성 질환」(해리슨 대조 대상 아님 — outline.py --harrison)
confidence: medium
review_status: unreviewed
note_form: 2            # 판형 2(2026-09-25) — 결론·시험 단서·왜 → 혼동 → 표·도식 → 목표에 맞춘 본문
title: "성숙낭성기형종 — 악성 변화는 편평 내막에서"
objective: "털·뼈를 담은 난소 낭종을 성숙낭성기형종으로 알아보고, 그 악성 변화의 가장 흔한 조직형(편평세포암)을 고른다"
objective_kind: 기전
condition: 난소 성숙낭성기형종(유피낭종, mature cystic teratoma · dermoid cyst)의 악성 변화
exams: [usmle, kmle]
summary:
  - "결론: 털·뼈가 든 난소 낭종(성숙낭성기형종)의 악성 변화는 약 80 % 가 편평세포암(squamous cell carcinoma)이다."
  - "시험 단서: 폐경 후·10 cm 넘는 낭종·벽의 고형 결절 + 열린 표본의 엉킨 털과 뼈 조각(dermoid cyst)."
  - "왜: 악성 변화는 가장 많은 조직에서 생긴다 — 낭종 벽은 각질형 편평상피(피부와 같은 내막)로 덮여 있다."
  - "선암·흑색종·카르시노이드는 드문 나머지다. 유두갑상샘암은 갑상샘 조직이 대부분인 난소갑상샘종(struma ovarii)에서."
pitfalls:
  - contrast: "유두갑상샘암 — 기형종이니 갑상샘 조직에서?"
    point: "갑상샘암은 종괴가 거의 갑상샘 여포로 된 고형의 난소갑상샘종(struma ovarii)에서 생긴다. 털과 피지가 찬 낭종(성숙낭성기형종)의 주 조직은 각질형 편평 내막이라 악성 변화도 편평세포암이 가장 흔하다 [[?robbins-10]] [[?hackethal-2008]]."
    exception: "갈색의 고형 종괴가 갑상샘 여포로 되어 있고(때로 갑상샘기능항진) 그 안에 침윤암이 있으면 유두갑상샘암이 맞다."
    covers: ["imaging-2026-0193:C"]
  - contrast: "편평세포암 vs 선암"
    point: "선암은 기형종 안의 샘(호흡기·장) 상피에서 생기는 두 번째 조직형이지만 소수다. 샘 구조·점액이 있어야 선암을 고른다 [[?hackethal-2008]]."
  - contrast: "낭종이 크고 CA 125 가 올랐으니 상피성 난소암?"
    point: "CA 125 는 악성 변화에서도 오를 수 있으나 조직형을 가르지 못한다. 털·뼈가 보이면 기형종에서 출발해 조직형을 정한다."
tables:
  - id: mct-malignancy-types
    section: "가르는 소견 — 어느 조직에서 생겼나"
    title: "기형종의 악성 변화 — 기원 조직과 조직형"
    role: differential
    span: column
    columns: ["조직형", "기원 조직", "가르는 소견"]
    rows:
      - ["편평세포암(가장 흔함, 약 80 %)", "각질형 편평 내막", "각화하는 침윤암, 흔히 벽의 고형 결절 [[?hackethal-2008]]"]
      - ["선암", "샘(호흡기·장) 상피", "샘 구조·점액 [[?robbins-10]]"]
      - ["유두갑상샘암", "난소갑상샘종의 갑상샘 조직", "갑상샘 여포가 대부분인 고형 종괴 [[?robbins-10]]"]
      - ["카르시노이드", "장·호흡기 상피의 신경내분비 세포", "작은 노란 고형 결절, 신경내분비 표지 [[?robbins-10]]"]
      - ["흑색종", "피부 성분의 멜라닌세포", "색소, S100·SOX10 양성 [[?robbins-10]]"]
diagram:
  title: "털·뼈가 든 난소 종괴 — 악성 변화의 조직형"
  nodes:
    - {id: start, kind: start, text: "난소 종괴 — 열린 표본에 털·뼈·피지"}
    - {id: what, kind: decision, text: "낭종인가, 갑상샘 고형 종괴인가?"}
    - {id: mct, kind: step, text: "성숙낭성기형종 — 편평 내막이 주 조직"}
    - {id: struma, kind: end, text: "난소갑상샘종 → 암이면 유두갑상샘암"}
    - {id: risk, kind: decision, text: "폐경 후·10 cm 이상·벽 결절?"}
    - {id: ask, kind: info, text: "나이·크기·벽 결절·자라는 속도를 확인"}
    - {id: benign, kind: end, text: "양성 기형종 — 온전히 절제"}
    - {id: histo, kind: decision, text: "결절의 침윤암은 어떤 조직인가?"}
    - {id: scc, kind: end, text: "각화 침윤암 → 편평세포암(약 80 %)"}
    - {id: adeno, kind: end, text: "샘·점액 → 선암(드묾)"}
  edges:
    - {from: start, to: what}
    - {from: what, to: mct, label: "털·피지 낭종"}
    - {from: what, to: struma, label: "갑상샘 여포"}
    - {from: mct, to: risk}
    - {from: risk, to: histo, label: "있음"}
    - {from: risk, to: benign, label: "없음"}
    - {from: risk, to: ask, label: "정보 없음"}
    - {from: ask, to: histo, label: "위험인자 있음"}
    - {from: ask, to: benign, label: "없음"}
    - {from: histo, to: scc, label: "각화 편평"}
    - {from: histo, to: adeno, label: "샘 구조"}
diagram_notes:
  - "악성 변화는 성숙낭성기형종의 약 1–2 % 로 드물다 — 위험인자는 45세 넘는 나이, 10 cm 넘는 크기, 빠른 성장, 조영되는 벽 고형 결절이다 [[?hackethal-2008]]."
  - "흑색종·카르시노이드도 기형종에서 생길 수 있으나 드물다 — 색소·신경내분비 표지로 가른다(표)."
  - "수술 중 낭종이 터지면 악성 세포가 퍼져 예후가 나빠진다 — 온전히 꺼내려 한다 [[?hackethal-2008]]."
checks:
  - q: "털과 뼈가 든 난소 낭종의 악성 변화에서 가장 흔한 조직형과 그 이유는?"
    a: "편평세포암(약 80 %) — 낭종 벽이 각질형 편평상피로 덮여 있어 가장 많은 조직에서 암이 생긴다."
  - q: "기형종에서 유두갑상샘암이 생기는 조건은?"
    a: "종괴가 거의 갑상샘 조직으로 된 난소갑상샘종(struma ovarii)일 때."
  - q: "성숙낭성기형종의 악성 변화 위험인자 넷은?"
    a: "45세 넘는 나이(대개 폐경 후), 10 cm 넘는 크기, 빠른 성장, 벽의 고형 결절."
variants:
  - id: v1
    of: imaging-2026-0193
    flip: true
    changed: "털·뼈가 찬 낭종 → 갑상샘 여포가 대부분인 갈색 고형 종괴(+ 갑상샘기능항진 증상), 결절의 침윤암에 유두 모양 핵 소견 → 답이 편평세포암에서 유두갑상샘암으로 바뀜"
    context: "단서를 바꿔 답이 바뀌는 변형 — 기형종이지만 갑상샘 조직이 주"
    stem: "A 48-year-old woman comes to the physician because of a 4-month history of pelvic pressure, palpitations, and a 3-kg weight loss. Her pulse is 104/min. Serum thyroid-stimulating hormone concentration is decreased; her thyroid gland is normal on palpation and ultrasonography. Pelvic ultrasonography shows a 7-cm solid left adnexal mass. At surgery, the cut surface of the ovarian mass is solid and brown. Microscopic examination shows that most of the mass consists of thyroid follicles filled with colloid. One area contains an invasive tumor with papillae and nuclei showing grooves and clearing. Which of the following is the most likely type of this malignancy?"
    choices: ["A. Squamous cell carcinoma", "B. Adenocarcinoma", "C. Papillary thyroid carcinoma", "D. Granulosa cell tumor", "E. Carcinoid tumor"]
    answer: "C"
    explanation: "This teratoma is made mostly of thyroid tissue — struma ovarii — which can cause hyperthyroidism with a normal cervical thyroid. A malignancy arising in it follows that tissue: papillae with grooved, cleared nuclei mark papillary thyroid carcinoma. In the original item the cyst was filled with hair and bone, so the dominant tissue was keratinizing squamous lining and squamous cell carcinoma was the most likely malignancy."
    kind: application
  - id: v2
    of: imaging-2026-0193
    flip: false
    changed: "나이 65 → 58세, 증상(복부 팽만 → 우연한 영상 발견), 왼쪽, 표지자를 CA 125 → SCC 항원, 낭종 파열 없음으로 바꾸고 「털·뼈가 든 큰 낭종 + 벽 결절의 침윤암」은 그대로 → 답은 여전히 편평세포암"
    context: "겉모습만 바꾸고 답은 같은 변형 — 우연히 발견된 큰 유피낭종"
    stem: "A 58-year-old woman is found to have a left adnexal mass on CT performed after a minor car accident. She has no symptoms. Menopause occurred 7 years ago. Pelvic ultrasonography shows an 11-cm cystic mass with echogenic fat, calcification, and a 3-cm solid nodule in its wall that has enlarged on a repeat scan 3 months later. Serum squamous cell carcinoma antigen concentration is increased. The mass is removed intact. The opened cyst contains sebaceous material and matted hair; microscopic examination of the wall nodule shows an invasive malignant tumor. Which of the following is the most likely type of this malignancy?"
    choices: ["A. Clear cell carcinoma", "B. Malignant melanoma", "C. Papillary thyroid carcinoma", "D. Squamous cell carcinoma", "E. Adenocarcinoma"]
    answer: "D"
    explanation: "Age, side, how the mass was found, the marker, and the absence of rupture changed, but the decisive clues did not: a postmenopausal woman with a large hair-containing cyst (mature cystic teratoma) and an enlarging solid wall nodule. Malignancy arises from the dominant tissue, the keratinizing squamous lining, so squamous cell carcinoma is most likely; a raised SCC antigen fits but is not needed for the answer. Adenocarcinoma and melanoma are rare transformations, and papillary thyroid carcinoma requires struma ovarii."
    kind: application
sources:
  - id: hackethal-2008
    org: "Hackethal A 외 (체계적 문헌고찰)"
    title: "Squamous-cell carcinoma in mature cystic teratoma of the ovary: systematic review and analysis of published data"
    kind: review
    year: 2008
    citation: "Lancet Oncol 2008;9(12):1173"
    doi: "10.1016/S1470-2045(08)70306-1"
    checked_at: 2026-10-03
    checked: "서지만(문항 imaging-2026-0193 해설 근거 목록에서 옮김, 원문·초록 미대조 — 컨테이너가 PubMed 를 막음). PMID 를 확인하지 못했고 DOI 는 기억으로 적었다(학습서 워크플로가 DOI 로 확인 — 검토 항목). 악성 변화 빈도·위험인자·편평세포암 비율·파열과 예후 서술에 쓴다"
    verified: citation
  - id: robbins-10
    org: "Elsevier"
    title: "Robbins & Cotran Pathologic Basis of Disease, 10th ed. — The Female Genital Tract (germ cell tumors of the ovary: teratomas)"
    kind: textbook
    year: 2020
    citation: "Kumar V, Abbas AK, Aster JC (eds). Robbins & Cotran Pathologic Basis of Disease, 10e. ch. The Female Genital Tract — Teratomas"
    checked_at: 2026-10-03
    checked: "서지만(문항 해설 근거 목록에서 옮김, 원문 미대조 — 검토 항목). 성숙낭성기형종의 구성(각질형 편평 내막·피부 부속기·로키탄스키 결절), 난소갑상샘종·카르시노이드 등 특수 기형종 서술에 쓴다"
    verified: citation
  - id: cureus-2025-mct-scc
    org: "Cureus (증례 보고, PMC Open Access)"
    title: "Unexpected Malignancy: Squamous Cell Carcinoma Arising in an Ovarian Mature Cystic Teratoma Diagnosed Postoperatively"
    kind: other
    year: 2025
    citation: "Cureus 2025;17(12):e98775"
    doi: "10.7759/cureus.98775"
    url: "https://pmc.ncbi.nlm.nih.gov/articles/PMC12780604/"
    checked_at: 2026-10-03
    checked: "그림 2(열린 적출 표본 — 털·뼈 조각이 든 터진 낭종)와 그 설명만 확인(exam-builder 풀 기록). 본문은 열지 않았다"
    verified: citation
figures:
- id: f1
  file: docs/assets/figures/pmc-pmc12780604_figure2.jpg
  kind: photo
  at: 기전 — 세 배엽에서 편평 내막으로
  shows: 터진 난소 낭종(성숙낭성기형종) — 내강의 털·뼈 조각 덩어리
  look_for:
  - 위쪽 화살표 — 엉킨 털과 뼈 조각 덩어리
  - 별 — 열린 낭종 벽의 매끈한 안쪽 면
  label: '「Ruptured right ovarian cyst (white star) containing hair and bone fragments (black arrow).」 — Unexpected Malignancy: Squamous Cell Carcinoma Arising in an Ovarian Mature Cystic Teratoma Diagnosed Postoperatively'
  label_basis: published_figure
  reference: 동료 심사 논문의 그림 설명(저자가 그 소견이라고 쓴 그림)
  paper: 'Unexpected Malignancy: Squamous Cell Carcinoma Arising in an Ovarian Mature Cystic Teratoma Diagnosed Postoperatively'
  doi: 10.7759/cureus.98775
  credit: 'Unexpected Malignancy: Squamous Cell Carcinoma Arising in an Ovarian Mature Cystic Teratoma Diagnosed Postoperatively. Cureus. 2025 Dec 8;17(12):e98775. doi: 10.7759/cureus.98775 (CC BY) — Figure 2'
  license: CC BY
  url: https://pmc.ncbi.nlm.nih.gov/articles/PMC12780604/
  asset: PMC-PMC12780604_Figure2
  from_question: imaging-2026-0193
---

## 판단 — 왜 편평세포암이 먼저인가
- 먼저 낭종의 이름을 붙인다: 열린 표본의 **엉킨 털·피지·뼈 조각** = 성숙낭성기형종(유피낭종, dermoid cyst).
- 악성 변화는 그 종양에서 **가장 많은 조직**에서 생긴다. 유피낭종의 벽은 피부처럼 각질형 편평상피로 덮여 있어, 악성 변화의 약 80 % 가 편평세포암이다 [[?hackethal-2008]].
- 다른 조직형은 그 조직이 **주가 될 때** 고른다 — 갑상샘 조직이 대부분(난소갑상샘종)이면 유두갑상샘암, 샘·점액이면 선암.
- 나이(폐경 후)·크기(10 cm 넘음)·벽 결절은 「악성 변화가 있는가」를 시사하고, 조직형은 바꾸지 않는다.

## 기전 — 세 배엽에서 편평 내막으로
성숙낭성기형종은 생식세포에서 생긴 양성 종양으로 세 배엽 조직을 모두 만들 수 있지만, **외배엽이 우세**하다. 낭종 벽은 각질형 편평상피와 피부 부속기(털집·피지샘)로 덮여 내강에 피지와 털이 찬다. 뼈·치아(중배엽)는 흔히 벽에서 솟은 결절(로키탄스키 결절, Rokitansky protuberance)에 모인다 [[?robbins-10]]. 악성 변화는 피부암과 같은 길을 밟아 이 편평 내막에서 생기며, 흔히 그 결절 자리에 침윤암으로 나타난다 [[?hackethal-2008]].

## 가르는 소견 — 어느 조직에서 생겼나
- 침윤암의 조직 모양이 기원 조직을 말해 준다(표). 각화가 있으면 편평세포암, 샘·점액이면 선암, 갑상샘 여포가 바탕이면 유두갑상샘암.
- CA 125·SCC 항원은 악성 변화에서 오를 수 있지만 조직형을 정하지 못하고, 정상이어도 악성 변화를 배제하지 않는다 [[?hackethal-2008]].

## 권고와 예외
- 악성 변화는 드물어(약 1–2 %) 대부분의 유피낭종은 양성이다 — 젊은 여성의 작은 유피낭종에서 악성 변화를 먼저 떠올리지 않는다 [[?hackethal-2008]].
- 수술 중 파열은 예후를 나쁘게 하므로 낭종을 온전히 꺼낸다. 병기·치료 세부는 이 정리본에서 대조하지 않았다(검토 항목).
- 근거는 모두 원문 미대조(†)다 — 빈도 수치는 사람 검토가 필요하다.
