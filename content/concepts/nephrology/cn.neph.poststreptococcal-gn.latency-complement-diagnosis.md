---
id: cn.neph.poststreptococcal-gn.latency-complement-diagnosis
type: concept
topic: Nephrology
see_also: [Pediatrics]
date: 2026-09-23
updated: 2026-10-05
version: 3
outline: h314            # 기본틀 슬롯(content/outline/subjects.yaml)
confidence: medium
review_status: unreviewed
note_form: 2            # 판형 2(2026-09-25) — 결론·시험 단서·왜 → 혼동 → 표·도식 → 목표에 맞춘 본문
title: "연쇄구균감염후사구체신염 — 잠복기와 C3로 가른다"
objective: "선행 감염과의 간격(잠복기)과 혈청 보체(C3)로 연쇄구균감염후사구체신염을 IgA신병증 등 다른 사구체질환과 감별해 진단하고, 면역복합체 손상으로 신염증후군이 생기는 이유를 설명한다"
objective_kind: 진단
condition: 연쇄구균감염후사구체신염(poststreptococcal glomerulonephritis, PSGN)
exams: [kmle, usmle]
summary:
  - "결론: 인두염 1~3주(농가진 2~6주) 뒤의 신염증후군 + C3 감소·C4 정상이면 연쇄구균감염후사구체신염이다."
  - "시험 단서: 소아, 콜라색 소변·눈 주위 부종·고혈압·적혈구원주, ASO·anti-DNase 상승(low C3, latent period)."
  - "왜: 항체가 만들어질 시간이 필요해 잠복기가 생기고, 면역복합체가 보체를 소모해 C3 가 떨어진다."
  - "IgA신병증은 감염 도중·직후 육안적 혈뇨가 반복되고 C3 가 정상 — 「간격」과 「C3」가 두 축이다."
  - "치료는 지지요법(혈압·부종, 필요 시 투석) — 반월체가 있어도 면역억제제는 쓰지 않는다. 소아는 3~6주에 회복."
pitfalls:
  - contrast: "상기도감염 뒤 혈뇨 = IgA신병증?"
    point: "두 질환 모두 상기도감염과 혈뇨가 이어진다. 가르는 것은 간격과 보체다 — PSGN 은 1~3주 잠복 뒤 신염증후군과 C3 저하, IgA신병증은 감염 도중·직후 육안적 혈뇨가 반복되며 C3 는 정상이다. 저보체 자체가 IgA신병증을 거스르는 소견이다."
    exception: "잠복기가 애매하면 C3 추적이 도움이 된다 — PSGN 의 저보체는 회복과 함께 정상화되고, 지속되면 C3 사구체병증·막증식사구체신염 등 다른 저보체 사구체신염을 찾는다(정상화 시점은 해리슨 본문에 수치 없음)."
    cites: ["harrison-21: 314장 p.2337·2339"]
    covers: ["kmle-2026-0073:A"]
  - contrast: "신염증후군 vs 신증후군(미세변화)"
    point: "미세변화신증후군은 사구체 족세포 이상으로 대량 단백뇨·저알부민혈증·부종이 오지만 적혈구원주·고혈압·보체 저하가 없다. 적혈구원주는 사구체 기원의 출혈을 뜻해 신염 쪽으로 기운다."
    exception: "PSGN 에서도 소아 5%·성인 20%는 신증후군 범위 단백뇨를 보인다 [[harrison-21: 314장 p.2337]]."
    cites: ["harrison-21: 314장 p.2337"]
  - contrast: "항생제를 쓰면 신염을 막는다?"
    point: "항생제는 신염 발생을 줄이지 못한다. 활동성 감염이 있으면 환자와 동거인에게 균 제거 목적으로 준다."
    cites: ["harrison-21: 314장 p.2337"]
tables:
  - id: psgn-vs-iga
    title: "상기도감염 뒤 혈뇨 — PSGN 과 IgA신병증"
    role: differential
    span: column
    section: "가르는 소견 — 간격과 C3"
    columns: ["항목", "PSGN", "IgA신병증"]
    rows:
      - ["감염과의 간격", "인두염 1~3주 · 농가진 2~6주 뒤", "감염 도중 또는 직후"]
      - ["혈청 C3", "첫 주 약 90% 감소(C4 정상)", "정상"]
      - ["경과", "대개 한 번, 재발 드묾", "육안적 혈뇨가 반복"]
      - ["확진", "임상+보체+연쇄구균 항체 — 생검 드묾", "신생검(메산지움 IgA 침착)"]
    note: "harrison-21: 314장 p.2337·2339"
  - id: other-dx
    title: "그 밖의 감별 — 무엇이 가르나"
    role: differential
    span: column
    section: "가르는 소견 — 간격과 C3"
    columns: ["질환", "가르는 소견"]
    rows:
      - ["다른 저보체 사구체신염(루푸스신염·막증식사구체신염·감염내막염 관련)", "선행 연쇄구균 감염·잠복기·항체가 없음, 루푸스는 C3·C4 함께 감소와 전신 증상"]
      - ["미세변화신증후군", "적혈구원주·고혈압 없는 대량 단백뇨"]
      - ["알포트증후군", "가족력·감각신경성 난청"]
      - ["용혈요독증후군", "혈성 설사 뒤 용혈·혈소판감소·급성신손상"]
diagram:
  title: "신염증후군에서 PSGN 가르기 — 간격과 C3"
  nodes:
    - {id: start, kind: start, text: "혈뇨·적혈구원주·고혈압·부종(신염증후군)"}
    - {id: lat, kind: decision, text: "선행 감염과의 간격은?"}
    - {id: latask, kind: info, text: "인두염·농가진 시기와 이전 혈뇨를 묻는다"}
    - {id: iga, kind: alert, text: "IgA신병증 쪽 — 감염 도중·직후, 반복"}
    - {id: c3, kind: decision, text: "혈청 C3·C4 는?"}
    - {id: psgn, kind: end, text: "PSGN — ASO·anti-DNase 확인, 지지요법"}
    - {id: lupus, kind: alert, text: "루푸스신염 등 다른 저보체 신염 평가"}
    - {id: other, kind: alert, text: "C3 정상 — PSGN 멀어짐, 다른 사구체질환"}
  edges:
    - {from: start, to: lat}
    - {from: lat, to: c3, label: "1~3주·2~6주"}
    - {from: lat, to: iga, label: "도중·직후"}
    - {from: lat, to: latask, label: "모름"}
    - {from: latask, to: c3, label: "잠복 있음"}
    - {from: latask, to: iga, label: "잠복 없음"}
    - {from: c3, to: psgn, label: "C3↓·C4 정상"}
    - {from: c3, to: lupus, label: "C3·C4 모두↓"}
    - {from: c3, to: other, label: "C3 정상"}
diagram_notes:
  - "C3 저하가 회복 뒤에도 지속되면 C3 사구체병증·막증식사구체신염 등 다른 저보체 사구체신염을 찾는다(정상화 시점은 해리슨 본문에 수치 없음)."
  - "ASO 는 약 30%·anti-DNase 는 약 70% 에서 오른다 — ASO 음성만으로 배제하지 않는다 [[harrison-21: 314장 p.2337]]."
  - "전형적이면 신생검은 거의 필요 없다. 급속 진행·보체 저하 지속처럼 비전형적이면 다른 진단을 위해 고려한다."
  - "반월체가 있어도 면역억제제의 역할은 없다 — 혈압·부종 조절, 필요 시 투석 [[harrison-21: 314장 p.2337]]."
checks:
  - q: "인두염 2주 뒤 콜라색 소변·고혈압·적혈구원주가 생긴 소아에서 진단을 가장 강하게 지지하는 혈액 소견 한 쌍은?"
    a: "C3(CH50) 감소와 C4 정상, 그리고 ASO·anti-DNase 역가 상승."
  - q: "PSGN 에 반월체가 보이면 면역억제제를 쓰는가?"
    a: "쓰지 않는다. 지지요법(혈압·부종 조절, 필요 시 투석)이 치료다."
sources:
  - id: harrison-21
    org: "McGraw Hill"
    title: "Harrison's Principles of Internal Medicine, 21st ed. — Chapter 314: Glomerular Diseases"
    kind: textbook
    year: 2022
    citation: "Loscalzo J, Kasper DL, Longo DL, et al (eds). Harrison's Principles of Internal Medicine, 21e. 314장 p.2331–2349"
    checked_at: 2026-09-23
    checked: "본문 대조(드라이브 문서) — p.2337 PSGN: 인두염 1~3주·농가진 2~6주 잠복, 항생제가 신염 발생을 줄이지 못함, 신염증후군 양상, 첫 주 90% CH50·C3 감소·C4 정상, ASO 30%·anti-DNase 70%, 생검 드묾, 지지요법·면역억제 역할 없음, 소아 3~6주 회복. p.2339 IgA신병증: 상기도감염 도중·직후 육안적 혈뇨 반복"
    verified: text
variants:
  - id: v1
    of: kmle-2026-0073
    flip: true
    changed: "혈뇨가 인두염 2주 뒤가 아니라 인두염 이틀째에 시작하고, 전에도 감기 때마다 같은 일이 있었으며 C3 가 정상 → 잠복기 없는 반복 육안적 혈뇨·정상 보체이므로 답이 감염후사구체신염에서 IgA신병증으로 바뀜"
    context: "단서를 바꿔 답이 바뀌는 변형 — 잠복기 없음·C3 정상"
    stem: "17세 남자가 목이 아프고 열이 난 지 이틀째에 콜라색 소변이 나와 왔다. 1년 전 감기에 걸렸을 때도 같은 일이 있었고 며칠 뒤 저절로 맑아졌다. 혈압 124/78 mmHg, 부종은 없다. 소변검사에서 변형 적혈구와 단백뇨 1+가 있고, 혈청 크레아티닌 0.9 mg/dL, C3·C4 는 정상이다. 가장 가능성이 높은 진단은?"
    choices: ["A. IgA신병증", "B. 감염후사구체신염", "C. 미세변화신증후군", "D. 알포트증후군", "E. 용혈요독증후군"]
    answer: "A"
    explanation: "상기도감염 도중(이틀째)에 육안적 혈뇨가 나타나고 같은 일이 반복되며 C3 가 정상이면 IgA신병증이다 [[harrison-21: 314장 p.2339]]. 감염후사구체신염은 면역 반응이 만들어질 1~3주 잠복기가 필요하고 첫 주에 C3 가 떨어진다 [[harrison-21: 314장 p.2337]]. 미세변화는 신증후군, 알포트는 가족력·난청, 용혈요독증후군은 용혈·혈소판감소가 단서다."
    kind: application
  - id: v2
    of: kmle-2026-0073
    flip: false
    changed: "나이·성별(10세 여아)·내원 경위(학교 검진 뒤 부모가 부종 발견)·제시 순서를 바꾸고, 인두염 뒤 약 2주 잠복·신염증후군·C3 감소·ASO 상승은 그대로 → 답은 여전히 감염후사구체신염"
    context: "겉모습만 바꾸고 답은 같은 변형 — 아침 얼굴 부종으로 온 여아"
    stem: "10세 여아가 사흘 전부터 아침에 눈꺼풀이 붓고 소변량이 줄어 어머니와 함께 왔다. 혈압은 138/92 mmHg 이다. 소변은 짙은 갈색이며 적혈구원주와 단백뇨 2+가 보인다. 혈청 C3 는 낮고 C4 는 정상, 항스트렙토리신O(ASO) 역가는 높다. 보호자에 따르면 약 2주 전 열과 인후통으로 며칠 앓았다고 한다. 가장 가능성이 높은 진단은?"
    choices: ["A. 미세변화신증후군", "B. IgA신병증", "C. 감염후사구체신염", "D. 루푸스신염", "E. 알포트증후군"]
    answer: "C"
    explanation: "제시 순서와 환자는 달라도 결정 단서 — 인두염 약 2주 뒤의 신염증후군(갈색뇨·적혈구원주·고혈압·부종), C3 감소·C4 정상, ASO 상승 — 는 같으므로 감염후사구체신염이다 [[harrison-21: 314장 p.2337]]. IgA신병증은 감염 직후 혈뇨·정상 C3, 루푸스신염은 C3·C4 가 함께 낮고 전신 증상이 있다, 미세변화는 적혈구원주·고혈압이 없는 신증후군이다."
    kind: application
figures:
- id: f1
  file: docs/assets/figures/pmc-pmc12554364_figure3-240-205-750-564.jpg
  kind: histology
  at: 기전에서 소견으로
  shows: 연쇄구균감염후사구체신염 전자현미경 — 상피하 전자밀도 침착(hump)
  look_for:
  - 사구체 기저막 바깥(상피 쪽)에 붙은 둥근 전자밀도 덩어리(빨간 화살촉)
  - 같은 논문 그림의 형광은 C3 과립상 침착
  label: '「Renal biopsy findings diagnostic for acute post-streptococcal glomerulonephritis (APSGN). (A) H&E stain showing a cellular crescent (arrow) compressing the glomerular tuft. (B) Periodic acid–Schiff (PAS) stain highlighting the crescent (arrow) and diffuse glomerular hypercellularity. (C) H&E stain demonstrating a prominent neutrophilic infiltrate (arrow) within the glomerulus. (D) Immunofluorescence microscopy revealing strong (3+) granular staining for C3 along capillary loops and in the mesangium. (E, F) Electron photomicrographs showing characteristic subepithelial electron-dense ‘humps’ (red arrows).」 — A Child With Anuric Acute Kidney Injury With Subsequent Hypertensive Encephalopathy: A Case Report'
  label_basis: published_figure
  reference: 동료 심사 논문의 그림 설명(저자가 그 소견이라고 쓴 그림)
  paper: 'A Child With Anuric Acute Kidney Injury With Subsequent Hypertensive Encephalopathy: A Case Report. Cureus'
  doi: 10.7759/cureus.93307
  credit: 'A Child With Anuric Acute Kidney Injury With Subsequent Hypertensive Encephalopathy: A Case Report. Cureus. 2025 Sep 26;17(9):e93307. doi: 10.7759/cureus.93307 (CC BY) — Figure 3'
  license: CC BY
  url: https://pmc.ncbi.nlm.nih.gov/articles/PMC12554364/
  asset: PMC-PMC12554364_Figure3
  privacy_check: 전자현미경 — 식별 정보 없음
  crop: 240,205,750,564
---

## 판단 — 왜 간격과 C3 인가
- 상기도감염 뒤 혈뇨라는 겉모습은 PSGN 과 IgA신병증이 같다 — 답을 가르는 것은 **감염과의 간격**과 **혈청 C3** 두 축이다(표).
- PSGN 은 항체가 만들어질 1~3주(농가진 2~6주) 잠복기가 있고, 첫 주에 약 90% 에서 C3·CH50 이 낮고 C4 는 정상이다 [[harrison-21: 314장 p.2337]].
- IgA신병증은 감염 **도중·직후** 육안적 혈뇨가 반복되고 보체가 정상이다 [[harrison-21: 314장 p.2339]]. 정상 C3 는 PSGN 을 멀어지게 한다.
- 선행 감염은 배양(10~70% 로 일정치 않음)보다 ASO(30%)·anti-DNase(70%)·antihyaluronidase(40%) 역가로 확인한다 [[harrison-21: 314장 p.2337]].

## 기전에서 소견으로
**연쇄구균감염후사구체신염(PSGN)** 은 신염원성 A군 연쇄구균의 인두·피부 감염 뒤 면역복합체 매개로 생기는 급성 내모세혈관 증식성 사구체신염으로, 급성 신염증후군의 원형이다. 개발도상국에서는 2~14세 소아에서 유행성으로, 선진국에서는 산발적으로 노인·쇠약 환자에게 더 많다 [[harrison-21: 314장 p.2337]].
정상 사구체 모세혈관벽(내피 · 기저막 · 족세포)은 적혈구와 알부민을 혈관 안에 붙잡아 둔다. PSGN 에서는 연쇄구균 항원(SPEB·NAPlr 이 후보)과 항체가 만든 면역복합체가 내피하·상피하(「혹, hump」)에 쌓이고, 보체가 활성화되며 호중구가 모인다 [[harrison-21: 314장 p.2337]].
- 모세혈관벽 손상 → 적혈구가 사구체로 빠져나가 세뇨관에서 원주가 되어 **적혈구원주·콜라색 소변**.
- 사구체 염증·증식으로 여과 면적이 줄면 나트륨·수분이 저류 → **부종(눈 주위)·고혈압·핍뇨**. 신피막이 부어 옆구리 통증이 올 수 있다.
- 면역복합체가 보체를 소모 → **CH50·C3 감소, C4 정상**(대체 경로 중심).
- 단백뇨는 대개 신증후군 범위 아래지만 소아 5%·성인 20% 는 신증후군 범위다.

## 가르는 소견 — 간격과 C3
- 보체가 낮으면 저보체 사구체신염(PSGN · 루푸스신염 · 막증식사구체신염 · 감염내막염 관련)으로 범위가 좁혀지고, 그중 선행 감염·잠복기·연쇄구균 항체가 PSGN 을 고른다.
- 소변검사: 혈뇨·적혈구원주·농뇨·단백뇨. 전형적이면 신생검은 거의 필요 없다.

## 권고와 예외
- 치료는 지지요법 — 혈압·부종 조절(염분·수분 제한, 이뇨제), 필요하면 투석. 활동성 연쇄구균 감염이 있으면 환자와 동거인에게 항생제를 준다. 반월체가 있어도 면역억제제의 역할은 없다 [[harrison-21: 314장 p.2337]].
- 소아는 대부분 3~6주 안에 질소혈증·혈뇨·단백뇨가 완전히 회복하지만 3~10% 는 현미경적 혈뇨·단백뇨·고혈압이 남는다. 노인은 예후가 나빠 질소혈증(최대 60%)·신증후군·말기신부전이 더 많다 [[harrison-21: 314장 p.2337]]. 재발은 드물다.

## 시험 쟁점 — 충돌·맥락·새 근거
- 해당 없음(대조: 해리슨 314장 p.2337·2339)
