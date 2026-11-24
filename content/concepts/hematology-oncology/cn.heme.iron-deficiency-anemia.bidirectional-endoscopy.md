---
id: cn.heme.iron-deficiency-anemia.bidirectional-endoscopy
type: concept
topic: Hematology
see_also: [Gastroenterology]
date: 2026-11-24
updated: 2026-11-24
version: 1
outline: h97            # 해리슨 21판 97장 Iron Deficiency and Other Hypoproliferative Anemias → 22판 102장
roots_none: "남성·폐경 여성 철결핍에서 원인 검사를 고르는 순서 — 원인의 빈도·연령(위장관 출혈·대장암)이 판단을 가르고 기초 기전이 답을 바꾸지 않는다"
confidence: medium
review_status: unreviewed
note_form: 2
title: "철결핍 빈혈 — 남성은 위·대장 내시경을 함께"
objective: "남성·폐경 여성에서 철결핍 빈혈이 확인되면 위장관 잠혈 손실·종양을 원인으로 보고 대장내시경과 상부 위장관 내시경을 함께 하며, 분변검사·철분만 투여·혈색소 전기영동·골수 검사가 왜 다음 단계가 아닌지 가른다"
objective_kind: 검사 선택
condition: 성인 남성·폐경 여성의 철결핍 빈혈(iron-deficiency anemia)
exams: [usmle, kmle]
summary:
  - "결론: 남성·폐경 여성의 철결핍 빈혈은 위장관 출혈로 보고 대장·상부 위장관 내시경(bidirectional endoscopy)을 함께 한다."
  - "시험 단서: 소구성·RDW 증가, ferritin < 30 μg/L·트랜스페린 포화도 < 15 %, 고기를 먹는 남성, 출혈 증상·흑색변 없음."
  - "왜: 식사로 설명되지 않는 철 손실은 대개 위장관 잠혈이고, 그중 놓치면 안 되는 것이 대장암(특히 우측)이다."
  - "다음 단계가 아닌 것: 분변 잠혈·면역화학검사(선별용), 철분만 주고 기다리기, 혈색소 전기영동, 골수 검사."
pitfalls:
  - contrast: "가족에 지중해빈혈 소형 → 혈색소 전기영동?"
    point: "지중해빈혈 소형도 소구성이지만 ferritin·트랜스페린 포화도가 정상~높고 RDW 는 정상이다. ferritin 이 낮으면 이미 철결핍이 증명된 것이라 전기영동은 다음 행동을 바꾸지 않는다 — 남은 질문은 「철이 어디로 새는가」다."
    exception: "ferritin 이 정상인데 소구성이고 RDW 가 정상이면 그때 지중해빈혈 형질을 전기영동으로 확인한다. 두 병이 겹쳐도 철결핍의 원인 검사는 따로 해야 한다."
    cites: ["harrison-22"]
    covers: ["usmle-2026-0293:D"]
  - contrast: "분변 면역화학검사(FIT) — 선별검사 vs 진단 검사"
    point: "분변 잠혈·면역화학검사는 증상 없는 평균 위험군에서 대장내시경 대상을 고르는 선별검사다. 철결핍 빈혈은 그 자체로 내시경 적응증이고, 출혈이 간헐적이며 상부 위장관 병변은 잘 잡지 못해 음성이어도 원인을 배제하지 못한다."
    covers: ["usmle-2026-0293:B"]
  - contrast: "철분만 주고 3개월 뒤 혈색소?"
    point: "철분 보충은 시작하되 원인 검사를 미루는 근거가 되지 않는다. 혈색소가 회복되어도 출혈 병변(대장암 등)은 그대로 자란다."
    cites: ["harrison-22"]
    covers: ["usmle-2026-0293:C"]
  - contrast: "철결핍을 확진하려면 골수 검사?"
    point: "골수 철 염색이 표준이지만 거의 필요 없고 지나치게 침습적이다 — ferritin < 30 μg/L 하나로 민감도 92 %·특이도 98 % 다."
    cites: ["harrison-22"]
    covers: ["usmle-2026-0293:E"]
tables:
  - id: ddx
    section: "가르는 소견 — 철결핍인가, 지중해빈혈 형질인가"
    title: "소구성 빈혈의 철 지표"
    role: comparison
    span: full
    columns: ["지표", "철결핍", "염증 빈혈", "지중해빈혈 형질"]
    rows:
      - ["ferritin(μg/L)", "낮다(≤ 15–30)", "정상~높다(> 100)", "정상~높다"]
      - ["트랜스페린 포화도", "낮다(< 10 %)", "낮다(< 20 %)", "정상~높다"]
      - ["MCV", "낮다(< 80 fL)", "낮다~정상", "낮다"]
      - ["RDW", "높다", "정상", "낮다~정상"]
    note: "해리슨 22판 표 102-3 에서 옮겼다 [[harrison-22: 102장 p.767]]."
diagram:
  title: "철결핍 빈혈 — 원인 검사 고르기"
  nodes:
    - {id: start, kind: start, text: "소구성 빈혈 — 피로·호흡곤란"}
    - {id: info, kind: info, text: "ferritin·트랜스페린 포화도·RDW"}
    - {id: iron, kind: decision, text: "ferritin < 30 μg/L 인가?"}
    - {id: other, kind: end, text: "형질·염증 빈혈 감별 — 전기영동 등"}
    - {id: who, kind: decision, text: "남성 또는 폐경 여성인가?"}
    - {id: young, kind: step, text: "월경·임신·식사 먼저 확인"}
    - {id: egd, kind: end, text: "대장 + 상부 위장관 내시경, 철분 시작"}
    - {id: obvious, kind: decision, text: "월경·식사로 설명되는가?"}
    - {id: oral, kind: end, text: "철분 보충 후 반응 재평가"}
  edges:
    - {from: start, to: info}
    - {from: info, to: iron}
    - {from: iron, to: other, label: "아니다"}
    - {from: iron, to: who, label: "그렇다"}
    - {from: who, to: egd, label: "그렇다"}
    - {from: who, to: young, label: "아니다"}
    - {from: young, to: obvious}
    - {from: obvious, to: oral, label: "그렇다"}
    - {from: obvious, to: egd, label: "아니다"}
diagram_notes:
  - "흑색변·혈변이 없어도, 분변 잠혈이 음성이어도 남성·폐경 여성의 철결핍은 내시경 적응증이다."
  - "두 내시경이 정상이면 셀리악병·위축성 위염·소장(혈관이형성 등)을 이어서 찾는다 — 해리슨 표 102-2 의 원인 목록."
  - "염증이 있으면 ferritin 이 올라가 철결핍을 가린다 — 이때는 트랜스페린 포화도를 함께 본다."
checks:
  - q: "63세 남자, ferritin 6 μg/L, 흑색변 없음. 분변 면역화학검사가 음성이면 내시경을 생략해도 되는가?"
    a: "아니다. 분변검사는 증상 없는 선별용이고 출혈이 간헐적이라 음성이 원인을 배제하지 못한다. 철결핍 빈혈 자체가 대장·상부 위장관 내시경의 적응증이다."
  - q: "소구성인데 ferritin 이 정상이고 RDW 가 정상, 적혈구 수가 많다. 다음 검사는?"
    a: "지중해빈혈 형질을 생각해 혈색소 전기영동을 한다. 철결핍이 증명되지 않았으므로 내시경의 근거가 없다."
variants:
  - id: v1
    of: usmle-2026-0293
    flip: true
    changed: "ferritin 6·트랜스페린 포화도 5 %·RDW 증가 → ferritin 140·포화도 32 %·RDW 정상·적혈구 수 6.1백만(철결핍이 아님) ⇒ 정답이 양방향 내시경에서 혈색소 전기영동으로"
    context: "같은 무증상 소구성 빈혈, 그러나 철 지표가 정상인 경우"
    stem: "A 63-year-old man comes to the physician for follow-up after a routine blood count showed anemia. He feels well and exercises regularly. He has had no black stools, visible blood in the stool, or weight loss. He eats a mixed diet, takes no medications, and had a normal colonoscopy 2 years ago. His parents emigrated from southern Italy, and his brother has 'mild anemia that never needed treatment.' Vital signs are within normal limits, and examination shows no pallor or splenomegaly. Laboratory studies show a hemoglobin of 11.9 g/dL, mean corpuscular volume of 64 μm3, red blood cell count of 6.1 million/mm3, red cell distribution width of 13.1%, serum ferritin of 140 ng/mL, and transferrin saturation of 32%. A peripheral smear shows microcytic, hypochromic cells with target cells. Which of the following is the most appropriate next step in evaluation?"
    choices: ["A. Colonoscopy and upper endoscopy", "B. Hemoglobin electrophoresis", "C. Oral ferrous sulfate and repeat complete blood count in 3 months", "D. Fecal immunochemical test", "E. Bone marrow aspiration with iron stain"]
    answer: "B"
    explanation: "The changed clue is the iron panel: ferritin and transferrin saturation are normal, RDW is normal, and the red cell count is high despite marked microcytosis — the pattern of thalassemia trait rather than iron deficiency [[harrison-22: 102장 p.767]]. Without iron deficiency there is no blood loss to trace, so endoscopy and stool testing are not indicated (his colonoscopy is also recent), and iron would only add to normal stores. Hemoglobin electrophoresis characterizes the trait; a bone marrow iron stain is unnecessary when serum iron studies are clear."
    kind: application
  - id: v2
    of: usmle-2026-0293
    flip: false
    changed: "63세 남자의 운동 시 호흡곤란 → 58세 폐경 여성의 얼음 씹기(pagophagia)·피로, FIT 음성 결과를 먼저 제시, 가족력 대신 채식 아닌 식사 — ferritin 낮은 철결핍 + 남성·폐경 여성이라는 결정적 단서는 그대로라 답은 양방향 내시경"
    context: "FIT 음성을 가지고 온 폐경 여성"
    stem: "A 58-year-old woman comes to the physician because of 2 months of fatigue and a craving to chew ice. Her last menstrual period was 6 years ago, and she has had no postmenopausal vaginal bleeding. She eats meat and fish regularly. She has had no abdominal pain, change in bowel habits, black stools, or blood in the stool. A fecal immunochemical test she completed 1 month ago at a health fair was negative. She takes no aspirin, nonsteroidal anti-inflammatory drugs, or anticoagulants. The conjunctivae are pale, and the abdomen is soft without masses. Pelvic examination is normal. Laboratory studies show a hemoglobin of 9.4 g/dL, mean corpuscular volume of 70 μm3, red cell distribution width of 18.5%, platelet count of 470,000/mm3, serum ferritin of 5 ng/mL, and transferrin saturation of 4%. Which of the following is the most appropriate next step in evaluation?"
    choices: ["A. Repeat fecal immunochemical test in 1 year", "B. Hemoglobin electrophoresis", "C. Colonoscopy and upper endoscopy", "D. Oral ferrous sulfate and repeat complete blood count in 3 months", "E. Transvaginal ultrasonography"]
    answer: "C"
    explanation: "The deciding clues are unchanged: a low ferritin and transferrin saturation with a high RDW prove iron deficiency, and in a postmenopausal woman with no menstrual or dietary explanation the source is presumed gastrointestinal [[harrison-22: 102장 p.765]]. A negative screening FIT does not exclude an intermittently bleeding colon cancer or an upper GI lesion, so both colonoscopy and upper endoscopy are needed while iron is started. Electrophoresis does not address a proven iron deficiency, and there is no postmenopausal bleeding to prompt pelvic imaging."
    kind: application
figures_none: "원인 검사(내시경) 선택 문제 — 판독할 영상·사진 소견이 시험 단서가 아니다"
sources:
  - id: harrison-22
    org: "McGraw Hill"
    title: "Harrison's Principles of Internal Medicine, 22nd ed."
    kind: textbook
    year: 2025
    citation: "Harrison's Principles of Internal Medicine, 22e. 102장 Iron Deficiency and Other Acquired Anemias Due to Decreased Erythrocyte Production p.762–769"
    checked_at: 2026-11-24
    checked: "본문 대조(드라이브 장별 문서 H22_102) — p.764 ferritin 감소·트랜스페린 포화도 < 15–20 % 면 소구성·저색소성 · p.765 진단은 검사 후 원인 찾기의 두 단계, 남성·폐경 여성은 악성 종양·중대한 출혈을 배제하려 영상·내시경이 필수, 골수 철 염색이 표준이나 거의 필요 없고 침습적, ferritin < 30 μg/L 민감도 92 %·특이도 98 % · p.766 표 102-2 원인(위장관: 식도염·궤양·혈관이형성·악성 종양 특히 우측 대장암, 흡수 저하: 셀리악·H. pylori·위축성 위염), 중증 철결핍의 혈소판 증가, 경구 철분 최소 3개월 · p.767 표 102-3 철결핍·염증·혼합·지중해빈혈 형질의 지표를 확인했다. 분변 면역화학검사의 위치는 이 장에 없다"
    verified: text
---

## 판단 — 왜 두 내시경을 함께 하나
- 철결핍 빈혈의 진단은 두 단계다 — 검사로 철결핍을 확인하고, 그다음 원인을 찾는다. 남성·폐경 여성은 악성 종양과 중대한 출혈을 배제하려 내시경이 필수다 [[harrison-22: 102장 p.765]].
- 고기를 먹는 성인 남성은 섭취 부족으로 설명되지 않는다. 월경도 없으니 남는 철 손실 경로는 위장관 잠혈이다.
- 출혈원은 상부(식도염·궤양·혈관이형성)와 하부(대장암, 특히 우측)에 모두 있고, 흡수 장애(셀리악병·위축성 위염)도 상부 내시경에서 찾는다 [[harrison-22: 102장 p.766]] — 한쪽만 보면 놓친다.

## 기전 — 왜 소구성이 되고 왜 잠혈인가
- 저장 철이 먼저 바닥나 ferritin 이 떨어지고, 트랜스페린 포화도가 15–20 % 아래로 내려가면 적혈구 조혈에 철이 모자라 저색소성·소구성이 된다 [[harrison-22: 102장 p.764]].
- 하루 1–2 mL 의 피가 계속 새면 흑색변 없이 철만 빠져나간다 — 출혈 증상이 없다는 것이 출혈이 없다는 뜻이 아니다.
- 철이 모자라면 공통 전구세포가 거핵구 쪽으로 기울어 혈소판이 늘 수 있다 [[harrison-22: 102장 p.766]].

## 가르는 소견 — 철결핍인가, 지중해빈혈 형질인가
- ferritin < 30 μg/L 하나로 철결핍을 진단한다(민감도 92 %·특이도 98 %). 골수 철 염색은 거의 필요 없다 [[harrison-22: 102장 p.765]].
- 지중해빈혈 형질은 ferritin·포화도가 정상~높고 RDW 가 낮거나 정상이다 [[harrison-22: 102장 p.767]] — 가족력만으로 철결핍을 덮지 않는다.

## 선택 — 원인 검사와 철 보충
- 내시경과 함께 경구 철분을 시작한다. 혈색소 회복과 저장 철을 채우려면 최소 3개월 쓴다 [[harrison-22: 102장 p.766]].
- 분변 잠혈·면역화학검사는 증상 없는 사람의 선별검사다. 철결핍 빈혈이 있으면 결과와 무관하게 내시경으로 간다.

## 권고와 예외
- 젊은 월경 여성은 월경량·임신·식사를 먼저 보고, 설명되지 않거나 위장관 증상·가족력이 있으면 내시경으로 간다.
- 두 내시경이 정상인데 철결핍이 계속되면 소장(혈관이형성·종양)과 셀리악병을 찾는다 [[harrison-22: 102장 p.766]].

## 시험 쟁점 — 충돌·맥락·새 근거
- 해당 없음(대조: 해리슨 22판 102장 p.764~767)
