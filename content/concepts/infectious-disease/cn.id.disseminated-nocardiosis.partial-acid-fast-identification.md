---
id: cn.id.disseminated-nocardiosis.partial-acid-fast-identification
type: concept
topic: Infectious Disease
see_also: [Microbiology, Nephrology]
discipline: microbiology
date: 2026-11-24
updated: 2026-11-25
version: 1
outline: h174            # 해리슨 21판 174장 Nocardiosis → 22판 179장
roots: [cn.micro.mycolic-acid-cell-wall.acid-fastness]
confidence: medium
review_status: unreviewed
note_form: 2
title: "파종 노카르디아증 — 가지 친 그람 양성 균은 부분 항산성"
objective: "면역억제 환자의 공동 폐 결절과 다발 뇌농양에서 가늘고 염주 모양으로 가지 치는 그람 양성 실 모양 균이 보이면 노카르디아로 보고, 약산 탈색에도 남는 부분 항산성으로 방선균·결핵균·곰팡이·효모와 가른다"
objective_kind: 감별
condition: 파종 노카르디아증(disseminated nocardiosis)
exams: [usmle, kmle]
summary:
  - "결론: 면역억제 + 공동 폐 결절 + 뇌농양 + 가지 치는 그람 양성 실 모양 균 = 노카르디아, 약산 탈색에 남는 부분 항산성이다."
  - "시험 단서: 장기이식·스테로이드, 수주의 발열·기침, 다엽 고리 조영 뇌병변, thin beaded branching gram-positive filaments."
  - "왜: 세포벽 미콜산이 결핵균보다 짧아 강한 산-알코올에는 빠지고 약산(modified Kinyoun)에는 붉은색이 남는다."
  - "치료는 트리메토프림-설파메톡사졸이 중심, 중증·뇌 침범은 2–3제 병용, 면역억제 환자 12개월."
pitfalls:
  - contrast: "가지 친 그람 양성 실 vs 피막 효모(크립토코쿠스)"
    point: "인도 잉크로 드러나는 두꺼운 다당 피막은 둥근 효모인 크립토코쿠스의 특징이다. 이식 환자의 폐 결절·뇌 병변이라는 겉모습은 같아도, 그람 염색에서 실처럼 가지를 치는 균이 보였다면 효모가 아니다 — 혈청 크립토코쿠스 항원 음성도 같은 쪽을 가리킨다."
    covers: ["usmle-2026-0291:C"]
  - contrast: "부분 항산성(노카르디아) vs 진짜 항산성(결핵균)"
    point: "결핵균은 강한 산-알코올에도 붉은색이 남고 cord 를 만들지만, 그람 염색에서 가지 치는 실 모양으로 보이지 않는다. 노카르디아는 약산으로 탈색할 때만 남는다 — 탈색제의 세기가 둘을 가른다."
    cites: ["harrison-22"]
    covers: ["usmle-2026-0291:E"]
  - contrast: "노카르디아 vs 방선균(Actinomyces)"
    point: "둘 다 가지 치는 그람 양성 실이지만 방선균은 혐기성·비항산성이고 구강·경부의 누공과 노란 알갱이를 만드는 국소 감염이다. 노카르디아는 호기성이고 면역억제 환자에서 폐 → 뇌로 혈행 파종한다."
    exception: "노카르디아도 피부 접종 뒤 방선균종(actinomycetoma)을 만들면 누공과 흰 알갱이가 나온다 — 이때는 발·다리가 흔하고 전신 파종은 드물다."
    cites: ["harrison-22"]
    covers: ["usmle-2026-0291:A"]
  - contrast: "예각으로 가지 치는 격벽 균사(아스페르길루스)?"
    point: "아스페르길루스는 곰팡이 균사로, 폭 약 1 μm 의 세균 실보다 훨씬 굵고 격벽이 있다. 은 염색은 노카르디아도 물들이므로 염색 하나로 가르지 않고 굵기·격벽·갈락토만난을 본다."
    cites: ["harrison-22"]
    covers: ["usmle-2026-0291:D"]
tables:
  - id: ddx
    section: "가르는 소견 — 가지 치는 균과 닮은 것들"
    title: "면역억제 환자의 폐·뇌 병변에서 보이는 균"
    role: comparison
    span: full
    columns: ["균", "모양·염색", "산소", "전형 임상"]
    rows:
      - ["노카르디아", "가늘고 염주 모양 가지 친 그람 양성 실, 부분 항산성", "호기성", "공동 폐 결절 → 다발 뇌농양·피하 농양"]
      - ["방선균", "가지 친 그람 양성 실, 비항산성", "혐기성", "구강·경부 덩이와 누공, 노란 알갱이"]
      - ["결핵균", "가는 막대, 산-알코올에도 항산성", "호기성", "상엽 공동, 수주의 기침·체중 감소"]
      - ["아스페르길루스", "예각으로 가지 치는 격벽 균사(곰팡이)", "—", "호중구 감소 환자의 결절·halo, 갈락토만난"]
      - ["크립토코쿠스", "둥근 효모, 두꺼운 피막(인도 잉크)", "—", "뇌수막염, 혈청 항원 양성"]
    note: "노카르디아의 모양·염색은 해리슨 22판 179장 p.1358, p.1360 에서 확인했다 [[harrison-22: 179장 p.1358]] [[harrison-22: 179장 p.1360]]."
diagram:
  title: "면역억제 환자의 폐 결절 + 뇌 병변 — 균 가리기"
  nodes:
    - {id: start, kind: start, text: "면역억제 + 폐 결절 + 고리 조영 뇌병변"}
    - {id: info, kind: info, text: "기관지폐포세척액 그람 염색·배양"}
    - {id: fil, kind: decision, text: "가늘게 가지 치는 그람 양성 실인가?"}
    - {id: other, kind: end, text: "균사·효모·막대 — 다른 기회감염"}
    - {id: afb, kind: decision, text: "약산 탈색에 붉은색이 남는가?"}
    - {id: noc, kind: end, text: "노카르디아 — 뇌 MRI, 병용 치료"}
    - {id: act, kind: end, text: "방선균 쪽 — 혐기 배양, 누공 확인"}
  edges:
    - {from: start, to: info}
    - {from: info, to: fil}
    - {from: fil, to: other, label: "아니다"}
    - {from: fil, to: afb, label: "그렇다"}
    - {from: afb, to: noc, label: "남는다"}
    - {from: afb, to: act, label: "빠진다"}
diagram_notes:
  - "노카르디아를 의심하면 검사실에 알린다 — 2주 넘게 자라고, 결핵균 배양의 오염 제거 처리는 노카르디아를 죽인다."
  - "폐 외 노카르디아증은 증상이 없어도 조영 뇌 MRI 로 뇌농양을 찾는다."
  - "중증 경험 치료: 트리메토프림-설파메톡사졸·리네졸리드·아미카신·이미페넴 중 2–3제(뇌 침범이면 이미페넴 대신 메로페넴)."
checks:
  - q: "노카르디아가 약산 탈색에서만 항산성인 이유는?"
    a: "세포벽에 미콜산이 있지만 탄소 45–65 개로 결핵균보다 짧아, 강한 산-알코올에는 염색이 빠지고 약산에는 남는다."
  - q: "신장이식 환자의 폐 노카르디아증에서 신경 증상이 없다. 뇌 영상이 필요한가?"
    a: "필요하다. 피부·눈의 일차 감염이 아니면 증상과 무관하게 조영 뇌 MRI 로 뇌농양을 찾는다 — 뇌 침범은 치료 약·기간(12개월)을 바꾼다."
variants:
  - id: v1
    of: usmle-2026-0291
    flip: true
    changed: "이식 환자의 폐 → 뇌 파종 → 면역 정상인 남자의 발치 뒤 턱 덩이·누공·노란 알갱이, 약산 탈색에 염색이 빠짐 ⇒ 정답이 부분 항산성에서 혐기성 성장·노란 알갱이(방선균)로"
    context: "같은 가지 치는 그람 양성 실, 그러나 구강·경부 국소 감염"
    stem: "A 46-year-old man comes to the physician because of a painless, slowly enlarging swelling at the angle of his left jaw for 2 months. Three months ago he had a left lower molar extracted. He has no fever and takes no medications; he has no history of transplantation, corticosteroid use, or HIV infection. Examination shows a firm, woody, nontender mass over the left mandibular angle with two small sinus tracts draining thick pus containing pale yellow grains. Chest x-ray is normal. Gram stain of the crushed grains shows branching gram-positive filaments; a modified acid-fast stain using weak acid decolorization is negative. Further laboratory testing of this organism is most likely to show which of the following?"
    choices: ["A. Strictly anaerobic growth, with yellow granules in the pus", "B. Retention of carbol fuchsin after decolorization with a weak acid", "C. A thick polysaccharide capsule outlined by India ink", "D. Septate hyphae that branch at acute angles on silver stain", "E. Retention of carbol fuchsin after decolorization with acid-alcohol, with serpentine cords"]
    answer: "A"
    explanation: "The changed clues are the host and site: an immunocompetent man with a woody cervicofacial mass and draining sinuses after a dental extraction, with yellow grains and branching gram-positive filaments that are NOT acid-fast even with weak acid. This is cervicofacial actinomycosis, an anaerobic, non-acid-fast organism of the oral flora. Nocardia would retain stain after weak-acid decolorization and typically disseminates from the lung in immunocompromised hosts [[harrison-22: 179장 p.1358, p.1360]]; capsule, septate hyphae, and acid-alcohol fastness point to Cryptococcus, Aspergillus, and Mycobacterium tuberculosis."
    kind: application
  - id: v2
    of: usmle-2026-0291
    flip: false
    changed: "54세 신장이식 여성 → 61세 심장이식 남성, 폐 증상보다 팔의 피하 농양과 두통을 먼저 제시, 그람 염색 검체를 기관지폐포세척액에서 피하 농양 흡인액으로 — 면역억제 + 폐 결절 + 뇌 병변 + 가지 치는 그람 양성 실이라는 결정적 단서는 그대로라 답은 부분 항산성"
    context: "심장이식 환자의 피하 농양에서 먼저 균을 본 경우"
    stem: "A 61-year-old man comes to the physician because of a tender lump on his right forearm for 10 days and a dull headache for 1 week. Fourteen months ago he received a heart transplant; he takes tacrolimus, mycophenolate mofetil, and prednisone, which was increased 2 months ago for an episode of rejection. He has had a low-grade fever and a mild cough. Temperature is 38.1 C. There is a 3-cm fluctuant, erythematous subcutaneous nodule on the right forearm without a history of trauma. Neurologic examination shows mild right-sided weakness. CT of the chest shows two nodules in the left lung, one with a cavity, and MRI of the brain shows a multiloculated ring-enhancing lesion in the left parietal lobe. Gram stain of pus aspirated from the forearm nodule shows thin, beaded, branching gram-positive filaments. Serum galactomannan and cryptococcal antigen are negative. Further laboratory testing of this organism is most likely to show which of the following?"
    choices: ["A. Strictly anaerobic growth, with sulfur granules in the pus", "B. Encapsulated budding yeast on mucicarmine stain", "C. Retention of carbol fuchsin after decolorization with a weak acid", "D. Broad, ribbon-like hyphae with right-angle branching", "E. Retention of carbol fuchsin after acid-alcohol decolorization, with cord formation"]
    answer: "C"
    explanation: "The deciding clues are unchanged: augmented immunosuppression after transplantation, a cavitating lung nodule, a multiloculated brain abscess, and a subcutaneous abscess — the lung, CNS, and skin are the classic sites of disseminated nocardiosis — with thin, beaded, branching gram-positive filaments [[harrison-22: 179장 p.1359, p.1360]]. Nocardia contains mycolic acids and is acid-fast only with weak-acid decolorization [[harrison-22: 179장 p.1358, p.1360]]. Actinomyces is anaerobic and non-acid-fast, Cryptococcus is an encapsulated yeast, Mucorales form broad ribbon-like hyphae, and M. tuberculosis is acid-alcohol fast and does not branch."
    kind: application
sources:
  - id: harrison-22
    org: "McGraw Hill"
    title: "Harrison's Principles of Internal Medicine, 22nd ed."
    kind: textbook
    year: 2025
    citation: "Harrison's Principles of Internal Medicine, 22e. 179장 Nocardiosis p.1358–1362"
    checked_at: 2026-11-24
    checked: "본문 대조(드라이브 장별 문서 H22_179) — p.1358 그람 양성·약한 항산성·카탈라아제 양성, 미콜산(탄소 45–65)·트레할로스, 호기성 토양 부생균, 위험인자(장기이식·스테로이드·면역억제제·HIV, 이식 환자의 거부반응 증강·칼시뉴린 억제제 농도), 흡입 뒤 발병 · p.1359 폐 노카르디아증은 아급성, 결절 공동화, 폐렴의 1/3 까지 파종, 중추신경이 파종의 2/3, 다엽 고리 조영 뇌농양 · p.1360 피하 농양, 방선균종의 흰 알갱이, 진단은 폭 1 μm·길이 50 μm 까지의 가지 친 염주 모양 그람 양성 실, 약산 탈색(modified Kinyoun 등)에서 항산성, 은 염색에 물듦, 배양 최대 2주·검사실에 알림, 결핵균 오염 제거 처리 금지 · p.1361 폐 외 노카르디아증은 증상과 무관하게 조영 뇌 MRI · p.1362 트리메토프림-설파메톡사졸이 1차, 중증 경험 치료 2–3제(뇌 침범이면 메로페넴), 면역억제·뇌 침범 12개월, 일차 예방은 권하지 않음을 확인했다. 방선균·아스페르길루스·크립토코쿠스 서술은 이 장에 없다(다른 장 미대조)"
    verified: text
figures_wanted:
- source: PMC_OA
  shows: 노카르디아의 염색 — 가늘게 가지 치는 그람 양성 실과 약산 탈색 항산 염색
  at: 기전 — 미콜산이 염색을 정한다
  query: '"nocardia" AND ("modified acid-fast" OR "Kinyoun") AND "Gram stain"'
  caption_terms:
  - Nocardia
  - acid-fast
  modality: HISTOLOGY_HE
figures_rejected:
- asset: PMC-PMC13437361_Figure2
  reason: 네 패널 합본(759×472)이라 그람 염색 한 패널이 340×220 픽셀로 인쇄 기준 미달 · 약산 항산 염색 패널(B)은 붉은 실이 이 해상도에서 뚜렷하지 않다
---

## 판단 — 왜 부분 항산성인가
- 면역억제 환자의 공동 폐 결절과 다엽 고리 조영 뇌농양은 노카르디아의 전형적 파종이다 — 폐렴의 1/3 까지 파종하고, 파종의 2/3 가 중추신경이다 [[harrison-22: 179장 p.1359]].
- 첫 진단 단계는 객담·고름에서 폭 약 1 μm 의 가늘고 염주 모양으로 가지 치는 그람 양성 실을 찾는 것이다 [[harrison-22: 179장 p.1360]].
- 이 모양이 보이면 남는 후보는 노카르디아와 방선균이다. 약산 탈색에서 붉은색이 남으면 노카르디아다 [[harrison-22: 179장 p.1360]].

## 기전 — 미콜산이 염색을 정한다
노카르디아는 결핵균과 같은 Mycobacteriales 목으로 세포벽에 미콜산이 있지만, 길이가 탄소 45–65 개로 짧다 [[harrison-22: 179장 p.1358]]. 그래서 강한 산-알코올에는 카볼 푹신이 빠지고, 약산(modified Kinyoun 등)으로 탈색하면 남는다 — 「약한 항산성」이다 [[harrison-22: 179장 p.1360]].
- 흡입한 균사 조각을 호중구가 잡아도 잘 죽이지 못하고, 균은 산화물을 중화하고 포식소체-리소좀 융합을 막아 식세포 안에서 버틴다 [[harrison-22: 179장 p.1358]]. 세포 면역이 눌린 장기이식 환자에서 퍼지는 까닭이다.
- 혈액 배양은 흔히 음성이지만 혈행으로 뇌·피부에 퍼진다 [[harrison-22: 179장 p.1359]].

## 가르는 소견 — 가지 치는 균과 닮은 것들
- 노카르디아는 호기성이라 혐기 배양 소견이 답이 아니다. 고름 속 알갱이는 피부 방선균종에서 흰색으로 나오고, 폐·뇌 파종에서는 전형적이지 않다 [[harrison-22: 179장 p.1360]].
- 은 염색은 노카르디아도 물들인다 [[harrison-22: 179장 p.1360]] — 균사인지 세균 실인지는 굵기로 가른다.

## 선택 — 확인한 뒤 할 일
- 증상과 무관하게 조영 뇌 MRI 로 뇌농양을 찾는다 [[harrison-22: 179장 p.1361]].
- 1차 약은 트리메토프림-설파메톡사졸이다. 중증은 2–3제 병용으로 시작하고 호전되면 경구 단독으로 잇는다. 면역억제·뇌 침범은 12개월 [[harrison-22: 179장 p.1362]].

## 권고와 예외
- 주폐포자충 예방용 트리메토프림-설파메톡사졸은 위험을 줄이지만 없애지 못한다 — 예방을 끊은 이식 환자에서 특히 의심한다 [[harrison-22: 179장 p.1362]].
- 위험인자 없이 파종 노카르디아증이 생기면 HIV 와 숨은 면역 결함(만성 육아종병 등)을 찾는다 [[harrison-22: 179장 p.1358]] [[harrison-22: 179장 p.1361]].

## 시험 쟁점 — 충돌·맥락·새 근거
- 해당 없음(대조: 해리슨 22판 179장 p.1358~1362)
