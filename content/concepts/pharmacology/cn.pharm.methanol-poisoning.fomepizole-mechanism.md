---
id: cn.pharm.methanol-poisoning.fomepizole-mechanism
type: concept
topic: Emergency Medicine
see_also: [Pharmacology, Nephrology, Ophthalmology]
date: 2026-11-10
updated: 2026-11-10
version: 1
outline: h459            # 기본틀 슬롯 — 해리슨 21판 459장(22판 470장) Poisoning and Drug Overdose
confidence: medium
review_status: unreviewed
note_form: 2            # 판형 2(2026-09-25)
title: "메탄올 중독 — 해독제는 첫 효소 ADH 를 막는다"
objective: "메탄올 중독에서 포메피졸이 알코올 탈수소효소를 경쟁적으로 억제해 포름산 생성을 막는 기전을 보조 치료의 기전과 구별한다"
objective_kind: 기전
condition: 메탄올 중독(methanol poisoning)
exams: [usmle, kmle]
summary:
  - "결론: 포메피졸(fomepizole)은 알코올 탈수소효소(ADH)를 경쟁 억제해 메탄올이 포름산이 되는 첫 단계를 막는다."
  - "시험 단서: 밀주·워셔액 뒤 늦게 온 「눈보라」 시야·시신경 유두 충혈 + 음이온 차·삼투압 차 모두 큰 산증(osmolal gap)."
  - "왜: 독은 메탄올이 아니라 대사물 포름산이다 — 삼투압 차가 남아 있으면 막을 메탄올이 아직 많다."
  - "엽산·폴린산은 이미 생긴 포름산의 대사를 돕는 보조 치료, 탄산수소나트륨은 산증 교정 — 해독제가 아니다."
  - "삼투압 차 = 측정 − (2Na + BUN/2.8 + 포도당/18), 10 넘으면 의미 있다. 늦게 오면 차는 줄고 음이온 차가 커진다."
pitfalls:
  - contrast: "엽산·폴린산(포름산 산화 촉진) vs 포메피졸(ADH 억제) — 독이 포름산이니 그걸 없애는 약이 해독제?"
    point: "해리슨은 고용량 폴린산·엽산을 「대사를 돕는」 보조 치료로, 포메피졸·에탄올을 따로 적는다 [[harrison-22: 470장 p.3714]]. 포메피졸은 ADH 를 두고 메탄올과 경쟁해 포름산이 생기는 것 자체를 막는다 [[harrison-22: 58장 p.371]]. 삼투압 차가 남아 있으면 아직 대사되지 않은 메탄올이 많다는 뜻이라 첫 단계를 막는 쪽이 해독의 중심이다."
    exception: "포메피졸이 이미 들어간 뒤 「포름산 제거를 돕는 보조 약물의 기전」을 묻는다면 엽산 의존 경로로 포름산을 CO2 로 산화시키는 것이 답이다 [[?goldfrank-11]]."
    cites: ["harrison-22: 470장 p.3714", "harrison-22: 58장 p.371"]
    covers: ["usmle-2026-0254:B"]
  - contrast: "알데히드 탈수소효소(ALDH) 억제 — 같은 경로의 효소를 막으면 해독?"
    point: "메탄올 → (ADH) 포름알데히드 → (ALDH) 포름산. 둘째 효소를 막으면(디설피람의 작용점) 포름알데히드가 쌓일 뿐이다. 해리슨도 포름알데히드와 포름산을 모두 독성 대사물로 적는다 [[harrison-22: 58장 p.371]] — 첫 단계를 막아야 둘 다 줄어든다."
    cites: ["harrison-22: 58장 p.371"]
  - contrast: "삼투압 차가 정상이면 독성 알코올이 아니다?"
    point: "삼투압 차는 모 알코올을 반영해 먼저 오르고, 대사가 진행되면 줄면서 음이온 차가 커진다 [[harrison-22: 58장 p.371]]. 늦게 온 환자에서 차가 작아도 메탄올을 배제하지 못한다 — 그때는 포메피졸의 이득이 줄고 투석의 몫이 커진다."
    cites: ["harrison-22: 58장 p.371"]
tables:
  - id: methanol-steps
    section: "기전 — 메탄올에서 포름산으로"
    title: "메탄올 대사의 단계와 약의 자리"
    role: comparison
    span: column
    columns: ["단계", "효소·작용", "약", "역할"]
    rows:
      - ["메탄올 → 포름알데히드", "알코올 탈수소효소(ADH) [[harrison-22: 58장 p.371]]", "포메피졸·에탄올 — 경쟁 억제 [[harrison-22: 58장 p.371]]", "해독제 — 독성 대사물 생성 차단"]
      - ["포름알데히드 → 포름산", "알데히드 탈수소효소(ALDH) [[?goldfrank-11]]", "(디설피람이 막는 자리)", "해독 아님 — 막으면 포름알데히드가 쌓인다"]
      - ["포름산 → CO2", "엽산 의존 산화 [[?goldfrank-11]]", "고용량 폴린산·엽산 [[harrison-22: 470장 p.3714]]", "보조 — 대사를 돕는다"]
      - ["포름산의 독성", "산증·망막/시신경 독성 [[harrison-22: 470장 p.3714]]", "탄산수소나트륨·혈액투석 [[harrison-22: 470장 p.3714]]", "산증 교정·메탄올과 포름산 제거"]
criteria:
  - id: meoh-antidote
    name: 포메피졸·에탄올 적응
    kind: 치료 권고
    population: "메탄올 중독(의심 포함)"
    statement: "음이온 차 대사성 산증, 시력 증상, 메탄올 농도 > 6 mmol/L(20 mg/dL), 또는 농도를 곧 잴 수 없을 때 에탄올 유사 중독·삼투압 차 증가가 있으면 에탄올이나 포메피졸을 준다 [[harrison-22: 470장 p.3714]]. 포메피졸이 우선이고 에탄올은 포메피졸이 없을 때 쓴다 [[harrison-22: 58장 p.371]]"
    exceptions: "삼투압 차·음이온 차가 함께 크면 농도 결과를 기다리느라 치료를 늦추지 않는다 [[harrison-22: 58장 p.371]]"
    source: harrison-22
    basis: current
    exams: [usmle, kmle]
  - id: meoh-hd
    name: 혈액투석 적응
    kind: 치료 권고
    population: "메탄올 중독"
    statement: "지속되는 음이온 차 산증, 임상 호전 없음, 신기능 저하에 혈액투석. 메탄올 > 15 mmol/L(50 mg/dL)이면 제거를 앞당기고 치료 기간을 줄이려고 투석한다 [[harrison-22: 470장 p.3714]]"
    exceptions: "해리슨 58장의 pH < 7.3 · 삼투압 차 > 20 기준은 에틸렌글리콜 절에 적힌 것이다(메탄올은 「치료가 비슷하다」고만 적는다) [[harrison-22: 58장 p.371]]"
    source: harrison-22
    basis: current
    exams: [usmle, kmle]
sources:
  - id: harrison-22
    org: "McGraw Hill"
    title: "Harrison's Principles of Internal Medicine, 22nd ed. — Chapter 470: Poisoning and Drug Overdose; Chapter 58: Acidosis and Alkalosis"
    kind: textbook
    year: 2025
    citation: "Harrison's Principles of Internal Medicine, 22e. 470장 p.3705, 3714(표 470-4) · 58장 p.371"
    checked_at: 2026-11-10
    checked: "본문 대조(드라이브 H22_470·H22_58 문서). 470장 p.3705 — 삼투압 차 > 10 mmol/L 은 저분자 용질(메탄올 포함)을 시사, 진행된 메탄올 중독에서 음이온 차 산증이 흔함. p.3714 표 470-4 메탄올 행 — 에탄올 유사 CNS 억제·삼투압 증가, 대사물 포름산이 음이온 차 산증·망막 독성; 초기 삼투압 차, 늦은 산증, 시야(흐림·점·실명)·망막(부종·충혈) 이상; 치료: 최근 섭취면 위 흡인, 탄산수소나트륨, 대사를 돕는 고용량 폴린산·엽산, 산증·시력 증상·농도 > 6 mmol/L(20 mg/dL)·농도 미확인 시 삼투압 차에 에탄올 또는 포메피졸, 지속 산증·호전 없음·신기능 저하에 투석, > 15 mmol/L(50 mg/dL)이면 투석으로 제거 단축. 58장 p.371 — 삼투압 계산식 2Na + BUN/2.8 + 포도당/18, 높은 음이온 차 + 삼투압 차는 에틸렌글리콜·메탄올 강력 시사, 농도를 기다리며 치료를 늦추지 않음, 삼투압 차가 먼저 오르고 줄면서 음이온 차가 커짐; 포메피졸과 에탄올 모두 ADH 대사를 두고 경쟁, 포메피졸이 1차(에탄올은 없을 때), 부하 15 mg/kg 뒤 10 mg/kg 12시간마다, pH 정상 또는 삼투압 차 < 10 까지; 메탄올 대사물 포름알데히드·포름산이 시신경·CNS 손상, 메탄올 치료는 에틸렌글리콜과 비슷. ALDH 단계·엽산 의존 포름산 산화·시토크롬 산화효소 기전은 두 장에 없다"
    verified: text
  - id: goldfrank-11
    org: "McGraw Hill"
    title: "Goldfrank's Toxicologic Emergencies, 11th ed. — Toxic alcohols"
    kind: textbook
    year: 2019
    citation: "Nelson LS, Howland MA, Lewin NA, et al (eds). Goldfrank's Toxicologic Emergencies, 11e. Toxic alcohols(장·쪽 미대조)"
    checked_at: 2026-11-10
    checked: "서지만 — 문항 출처로 적힌 교과서. 이 세션에서 원문 미대조(ALDH 단계, 엽산 의존 포름산 산화, 포름산의 시토크롬 c 산화효소 억제 서술의 근거)"
    verified: citation
diagram:
  title: "독성 알코올 의심 산증 — 해독제까지"
  nodes:
    - {id: start, kind: start, text: "음이온 차 대사성 산증 + 알코올 섭취 의심"}
    - {id: gap, kind: decision, text: "삼투압 차가 10을 넘는가?"}
    - {id: gapask, kind: info, text: "측정·계산 삼투압 · 에탄올 · 독성 알코올 농도"}
    - {id: other, kind: end, text: "다른 원인 평가 — 늦은 내원은 차가 줄 수 있다"}
    - {id: clue, kind: decision, text: "시야 이상·시신경 유두 충혈?"}
    - {id: meoh, kind: step, text: "메탄올 — 포름산이 시신경 독성"}
    - {id: eg, kind: step, text: "에틸렌글리콜 — 옥살산 결정·신손상"}
    - {id: block, kind: step, text: "포메피졸: ADH 경쟁 억제 → 대사물 차단"}
    - {id: hd, kind: decision, text: "산증 지속·호전 없음·신기능 저하?"}
    - {id: dial, kind: end, text: "혈액투석 + 포메피졸 지속"}
    - {id: keep, kind: end, text: "포메피졸·탄산수소나트륨 지속, 재평가"}
  edges:
    - {from: start, to: gap}
    - {from: gap, to: clue, label: "예"}
    - {from: gap, to: other, label: "아니오"}
    - {from: gap, to: gapask, label: "모름"}
    - {from: gapask, to: clue, label: "차 > 10"}
    - {from: gapask, to: other, label: "차 정상"}
    - {from: clue, to: meoh, label: "예"}
    - {from: clue, to: eg, label: "아니오"}
    - {from: meoh, to: block}
    - {from: eg, to: block}
    - {from: block, to: hd}
    - {from: hd, to: dial, label: "예"}
    - {from: hd, to: keep, label: "아니오"}
diagram_notes:
  - "삼투압 차 = 측정 삼투압 − (2Na + BUN/2.8 + 포도당/18) [[harrison-22: 58장 p.371]]. 10 넘으면 저분자 용질을 시사한다 [[harrison-22: 470장 p.3705]] — 에탄올도 차를 만들므로 에탄올 농도를 함께 본다."
  - "삼투압 차와 음이온 차가 함께 크면 농도 결과를 기다리지 않고 포메피졸을 시작한다 [[harrison-22: 58장 p.371]]."
  - "메탄올 치료의 보조: 탄산수소나트륨(산증 교정), 고용량 폴린산·엽산(대사 촉진), 최근 섭취면 위 흡인 [[harrison-22: 470장 p.3714]]."
  - "포메피졸 용량: 부하 15 mg/kg 정주 뒤 10 mg/kg 12시간마다, pH 정상 또는 삼투압 차 < 10 까지 — 해리슨은 에틸렌글리콜 절에 적고 메탄올은 같다고 한다 [[harrison-22: 58장 p.371]]."
checks:
  - q: "메탄올 중독에서 포메피졸의 작용점과 그 결과는?"
    a: "알코올 탈수소효소를 경쟁 억제 → 메탄올이 포름알데히드·포름산으로 바뀌지 않는다. 메탄올은 그대로 남아 투석·폐로 천천히 제거된다."
  - q: "엽산·폴린산과 포메피졸의 역할 차이는?"
    a: "엽산·폴린산은 이미 생긴 포름산을 CO2 로 대사하도록 돕는 보조 치료, 포메피졸은 포름산이 생기기 전 첫 단계를 막는 해독제."
  - q: "삼투압 차가 큰 것이 해독제 선택에 주는 정보는?"
    a: "대사되지 않은 모 알코올이 아직 많다 — ADH 를 막으면 앞으로 생길 독성 대사물을 막을 수 있다."
variants:
  - id: v1
    of: usmle-2026-0254
    flip: true
    changed: "fomepizole already running and the question asks for the mechanism of the added vitamin (leucovorin) → answer shifts from competitive inhibition of alcohol dehydrogenase to folate-dependent oxidation of formate to CO2"
    context: "Same poisoning; the antidote has already been given and the adjunct drug's mechanism is asked"
    stem: "A 39-year-old man is brought to the emergency department 18 hours after drinking several cups of windshield washer fluid during a suicide attempt. He reports blurred vision with 'spots' in both eyes. Pulse is 110/min and respirations are 30/min and deep. Funduscopic examination shows bilateral optic disc hyperemia. Arterial pH is 7.08, serum bicarbonate 6 mEq/L, anion gap 32 mEq/L, and the osmolal gap 24 mOsm/kg H2O. Serum ethanol is undetectable. Intravenous fomepizole and sodium bicarbonate are started, and hemodialysis is arranged. The toxicologist also recommends high-dose intravenous leucovorin. This additional drug most likely benefits the patient by which of the following mechanisms?"
    choices:
      - "A. Competitive inhibition of alcohol dehydrogenase"
      - "B. Inhibition of aldehyde dehydrogenase"
      - "C. Enhancement of folate-dependent oxidation of formate to carbon dioxide"
      - "D. Replenishment of hepatic glutathione stores"
      - "E. Chelation of formate for renal excretion"
    answer: "C"
    explanation: "바뀐 단서는 해독제 포메피졸이 이미 들어갔고 「추가한 폴린산」의 기전을 묻는다는 점이다. 해리슨은 고용량 폴린산·엽산을 메탄올 대사를 돕는 보조 치료로 적는다(470장 p.3714) — 엽산 의존 경로로 포름산을 CO2 로 산화시켜 독성 대사물의 제거를 앞당긴다. ADH 경쟁 억제(A)는 이미 준 포메피졸의 기전이고, ALDH 억제(B)는 포름알데히드를 쌓을 뿐이며, 글루타티온 보충(D)은 아세트아미노펜 해독제, 포름산을 킬레이트하는 약(E)은 없다."
    kind: application
  - id: v2
    of: usmle-2026-0254
    flip: false
    changed: "patient (52-year-old woman), source (methanol-containing solvent in a workshop), visual complaint (dim, cloudy vision) and lab presentation changed; the antidote mechanism is still asked while the osmolal gap remains high → answer unchanged (competitive inhibition of alcohol dehydrogenase)"
    context: "Different patient and source; same poisoning and same antidote question"
    stem: "A 52-year-old woman who restores furniture is brought to the emergency department by her husband because she has had vomiting, abdominal pain, and 'cloudy, dim' vision since waking. He found an open bottle of solvent labeled as containing methanol on the kitchen table. Respirations are 26/min. The pupils are dilated and react poorly to light. Serum sodium is 138 mEq/L, chloride 100 mEq/L, bicarbonate 10 mEq/L, glucose 90 mg/dL, and BUN 12 mg/dL; measured serum osmolality is 322 mOsm/kg H2O. Serum ethanol is undetectable and lactate is 2.1 mmol/L. The specific antidote recommended for this patient acts by which of the following mechanisms?"
    choices:
      - "A. Acceleration of formate oxidation to carbon dioxide"
      - "B. Competitive inhibition of alcohol dehydrogenase"
      - "C. Inhibition of aldehyde dehydrogenase"
      - "D. Alkalinization of urine to trap formate"
      - "E. Regeneration of reduced glutathione"
    answer: "B"
    explanation: "환자·노출 경로·시야 호소·제시 순서는 바뀌었지만 결정적 단서는 그대로다 — 음이온 차 28(138−100−10)의 산증, 계산 삼투압 ≈ 286 이라 삼투압 차 ≈ 36(대사되지 않은 메탄올이 많다), 시야 이상, 에탄올 음성. 해독제 포메피졸은 메탄올과 ADH 를 두고 경쟁해 포름알데히드·포름산 생성을 막는다(해리슨 58장 p.371). 포름산 산화 촉진(A)은 폴린산의 보조 작용, ALDH 억제(C)는 해독이 아니며, 소변 알칼리화(D)는 살리실산 치료, 글루타티온 재생(E)은 아세트아미노펜 해독제다."
    kind: application
figures_none: 해독제의 효소 기전(대사 경로)이 목표 — 안저 사진은 진단 단서일 뿐 기전 판단을 돕지 않는다
---

## 판단 — 왜 ADH 억제가 해독제인가
- 메탄올 자체는 에탄올처럼 중추신경을 누를 뿐이고, 산증과 망막 독성은 대사물 **포름산**이 만든다 [[harrison-22: 470장 p.3714]].
- 포메피졸과 에탄올은 **알코올 탈수소효소(alcohol dehydrogenase, ADH)** 를 두고 메탄올과 경쟁해 그 첫 단계를 막는다 [[harrison-22: 58장 p.371]] — 포름알데히드도 포름산도 생기지 않는다.
- 삼투압 차가 크다 = 아직 대사되지 않은 모 알코올이 많다 = 막으면 앞으로 생길 독을 막는다.
- 엽산·폴린산(대사 촉진)·탄산수소나트륨(산증 교정)은 보조 치료다 [[harrison-22: 470장 p.3714]] — 표 「메탄올 대사의 단계와 약의 자리」.

## 기전 — 메탄올에서 포름산으로
메탄올(분자량 32)은 흡수되면 혈장 삼투압을 올린다 — 그래서 삼투압 차가 음이온 차보다 먼저 나타난다 [[harrison-22: 58장 p.371]]. 간의 ADH 가 메탄올을 포름알데히드로, 알데히드 탈수소효소가 포름산으로 바꾼다 [[?goldfrank-11]]. 해리슨은 포름알데히드와 포름산이 시신경·중추신경을 심하게 손상한다고 적는다 [[harrison-22: 58장 p.371]]. 포름산은 미토콘드리아 호흡(시토크롬 c 산화효소)을 억제해 대사 요구가 큰 시신경·망막을 먼저 망가뜨리고 [[?goldfrank-11]], 젖산·케톤산이 더해져 산증이 깊어진다 [[harrison-22: 58장 p.371]]. 포름산은 엽산 의존 경로로 CO2 가 되는데 사람에서는 이 경로가 느려 쌓인다 [[?goldfrank-11]] — 폴린산·엽산이 「대사를 돕는」 이유다 [[harrison-22: 470장 p.3714]].

## 가르는 소견 — 메탄올이라는 근거와 시점
- 초기: 에탄올 유사 중독·구역·구토와 삼투압 차. 늦게: 음이온 차 산증, 시야 흐림·점·실명, 망막 부종·충혈 [[harrison-22: 470장 p.3714]]. 섭취 뒤 수 시간~하루 늦게 증상이 오는 것은 독이 대사물이기 때문이다.
- 높은 음이온 차 + 삼투압 차 → 에틸렌글리콜·메탄올을 강하게 시사 [[harrison-22: 58장 p.371]]. 에틸렌글리콜은 옥살산칼슘 결정뇨·신부전, 메탄올은 시야·망막 이상이 가른다 [[harrison-22: 470장 p.3714]]. 아이소프로필 알코올은 삼투압 차만 있고 음이온 차 산증이 없다 [[harrison-22: 58장 p.371]].
- 음성 결과의 한계: 삼투압 차는 시간이 지나면 줄어든다 — 늦게 온 환자에서 차가 작아도 메탄올을 배제하지 못한다. 에탄올이 함께 있으면 차의 일부를 에탄올이 설명한다.

## 선택 — 해독제·보조·투석
- 해독제: 포메피졸이 1차, 에탄올은 없을 때 [[harrison-22: 58장 p.371]]. 적응 기준은 표 대신 기준 「포메피졸·에탄올 적응」.
- 보조: 탄산수소나트륨, 고용량 폴린산·엽산, 최근 섭취면 위 흡인 [[harrison-22: 470장 p.3714]].
- 투석: 지속 산증·호전 없음·신기능 저하, 또는 메탄올 > 50 mg/dL 로 제거를 앞당길 때 [[harrison-22: 470장 p.3714]]. 포메피졸은 메탄올을 없애지 않고 대사만 멈추므로, 남은 메탄올·포름산을 치우는 것은 투석이다.
- 재평가: pH·음이온 차·삼투압 차의 추이, 시력. 포메피졸은 pH 정상 또는 삼투압 차 < 10 까지 [[harrison-22: 58장 p.371]].

## 권고와 예외
- 삼투압 차와 음이온 차가 모두 크면 농도를 기다리지 않는다 [[harrison-22: 58장 p.371]].
- ALDH 단계·엽산 의존 포름산 산화·시토크롬 c 산화효소 억제는 해리슨 두 장에 없다 — 독성학 교과서 근거이며 원문 미대조(검토 항목).

## 시험 쟁점 — 충돌·맥락·새 근거
- **Z1 맥락 · 에탄올을 해독제로 쓰는가** — 시험 기준: 포메피졸이 1차, 에탄올은 포메피졸이 없을 때 [[harrison-22: 58장 p.371]] / 다른 기준: 해리슨 표 470-4 는 「에탄올 또는 포메피졸」로 나란히 적는다 [[harrison-22: 470장 p.3714]] / 왜 다른가: 같은 원리(ADH 경쟁)이고 에탄올은 의식 저하·혈중 농도 조절이 어렵다는 차이를 58장이 적는다 / 시험에서는: USMLE·KMLE 모두 「가장 적절한 해독제」는 포메피졸, 기전은 둘 다 ADH 경쟁 억제.
