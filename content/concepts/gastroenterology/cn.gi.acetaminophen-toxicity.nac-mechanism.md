---
id: cn.gi.acetaminophen-toxicity.nac-mechanism
type: concept
topic: Gastroenterology
see_also: [Emergency Medicine, Pharmacology]
date: 2026-09-23
updated: 2026-09-23
version: 1
outline: h340            # 기본틀 슬롯(content/outline/subjects.yaml)
confidence: medium
review_status: unreviewed
title: "아세트아미노펜 중독 — NAPQI·글루타티온 고갈과 N-아세틸시스테인의 기전"
objective: "아세트아미노펜의 정상 대사(포합 → 소량의 CYP2E1 경로 → 글루타티온 포합)와 과량에서 포합이 포화되고 글루타티온이 고갈되어 NAPQI 가 간세포 단백과 결합해 중심소엽 괴사를 일으키는 기전을 설명하고, N-아세틸시스테인이 설프히드릴기를 공급해 글루타티온을 다시 채운다는 기전을 CYP 억제·흡착·포합 효소 유도·수용체 길항과 구별한다"
objective_kind: 기전
condition: 아세트아미노펜(파라세타몰) 중독
exams: [usmle, kmle]
summary:
  - "치료 용량의 아세트아미노펜은 대부분 2상 반응(황산·글루쿠론산 포합)으로 무해한 대사물이 되고, 적은 양만 1상 반응(CYP2E1)으로 반응성 대사물 NAPQI 가 된다. NAPQI 는 간의 글루타티온과 결합해 수용성 머캅투르산으로 콩팥에서 배설된다 [[harrison-21: 340장 p.2588]]."
  - "과량이면 NAPQI 가 너무 많이 생기거나 글루타티온이 적어(굶주림·만성 음주) 글루타티온이 고갈되고, NAPQI 가 간세포 거대분자와 공유결합(단백 부가물)해 중심소엽(3구역) 괴사를 일으킨다 [[harrison-21: 340장 p.2588]]."
  - "N-아세틸시스테인(NAC)은 설프히드릴기를 공급해 글루타티온을 다시 채운다 — 그래서 이미 만들어지는 NAPQI 를 무해하게 만든다. CYP2E1 을 막거나 흡수를 막는 약이 아니다 [[harrison-21: 340장 p.2588]]."
  - "초기(4–12시간)에는 구역·구토 정도이고 간수치가 정상일 수 있다. 간 손상은 24–48시간에 드러나고 3–5일에 최고(AST/ALT >10,000 IU/L 도 흔함)다 — 그래서 치료는 증상이나 간수치가 아니라 혈중 농도(노모그램)로 정한다 [[harrison-21: 340장 p.2588]]."
  - "NAC 는 8시간 안에 시작해야 가장 효과적이고, 24–36시간에 주어도 부분적 효과가 있다. 흡착(활성탄·콜레스티라민)은 복용 30분이 지나면 효과가 없어 보인다 [[harrison-21: 340장 p.2588]]."
criteria:
  - id: apap-nac
    name: NAC 적응·시점
    kind: 치료 권고
    population: "급성 단회 아세트아미노펜 과량 복용"
    statement: "복용 4–8시간 혈중 농도를 노모그램에 찍어 위험을 판정하고, 높은 농도(해리슨: 4시간 >200 µg/mL 또는 8시간 >100 µg/mL)면 NAC 가 간 괴사를 크게 줄인다. 복용 8시간 안에 시작하고, 24–36시간에 주어도 부분적 효과가 있다 [[harrison-21: 340장 p.2588]]"
    exceptions: "복용량·시점이 불확실하거나 의식 저하·부인으로 병력이 불확실하면서 매우 높은 AST/ALT·낮은 빌리루빈이면 추정 진단으로 NAC 를 준다 — 안전하고 늦게 줘도 쓴다 [[harrison-21: 340장 p.2588]]"
    source: harrison-21
    basis: current
    exams: [kmle, usmle]
  - id: apap-risk
    name: 독성 문턱을 낮추는 조건
    kind: 위험 요인
    population: "아세트아미노펜 복용자"
    statement: "만성 음주(CYP2E1 유도 + 글루타티온 생성 억제 — 독성 용량이 2 g 까지 낮아질 수 있음), 굶주림·열성 질환으로 먹지 못함(글루타티온 감소), 페노바르비탈·이소니아지드 등 CYP 유도 약 [[harrison-21: 340장 p.2588]]"
    exceptions: "급성 음주가 급성 아세트아미노펜 손상을 키우는지는 논란이다"
    source: harrison-21
    basis: current
    exams: [kmle, usmle]
tables:
  - id: apap-antidote-mech
    title: "보기로 나오는 해독 기전 — 누구의 기전인가"
    role: comparison
    span: column
    section: "(심화) 해독 기전을 가르는 법"
    columns: ["기전", "해당 약·조치", "아세트아미노펜에서"]
    rows:
      - ["글루타티온 재보충(설프히드릴기 공급)", "N-아세틸시스테인", "정답 — NAPQI 를 무해화"]
      - ["장관 안에서 흡착", "활성탄·콜레스티라민", "복용 직후에만(30분 넘으면 효과 없어 보임)"]
      - ["CYP 억제로 독성 대사물 생성 차단", "포메피졸(알코올 탈수소효소 억제 — 메탄올·에틸렌글리콜)", "NAC 의 기전이 아니다"]
      - ["수용체 길항", "날록손(오피오이드)·플루마제닐", "아세트아미노펜은 수용체 독성이 아니다"]
    note: "NAC·흡착의 서술은 해리슨 340장 [[harrison-21: 340장 p.2588]]. 포메피졸·날록손 행은 비교를 위한 일반 약리 지식으로 이 정리본에서 원문 대조하지 않았다."
sources:
  - id: harrison-21
    org: "McGraw Hill"
    title: "Harrison's Principles of Internal Medicine, 21st ed. — Chapter 340: Toxic and Drug-Induced Hepatitis"
    kind: textbook
    year: 2022
    citation: "Loscalzo J, Kasper DL, Longo DL, et al (eds). Harrison's Principles of Internal Medicine, 21e. 340장 p.2584, 2588 (Acetaminophen Hepatotoxicity)"
    checked_at: 2026-09-23
    checked: "본문 대조(드라이브 340장 문서) — p.2584 아세트아미노펜은 직접 독소의 대표 · p.2588 중심소엽 괴사, 단회 10–15 g 에서 간 손상, 4시간 >300 µg/mL 는 중증 예측·<150 µg/mL 는 손상 가능성 매우 낮음, 4–12시간 구역·구토 → 24–48시간 간 손상 → 3–5일 최고(AST/ALT >10,000), 2상(황산·글루쿠론산)이 주 경로·CYP2E1 로 NAPQI·글루타티온 포합 → 머캅투르산, 글루타티온 고갈 시 단백 부가물, 음주·페노바르비탈·INH·굶주림이 위험을 높임(만성 음주자 2 g), 활성탄·콜레스티라민은 30분 넘으면 효과 없어 보임, 노모그램 4–8시간 농도, 4시간 >200·8시간 >100 µg/mL 에서 NAC 가 괴사를 크게 줄임, NAC 는 설프히드릴기를 공급해 글루타티온을 재보충, 8시간 안에 시작·24–36시간에도 부분 효과, 정맥 부하 140 mg/kg 뒤 70 mg/kg 4시간마다(문서 표기 그대로). 같은 쪽 앞부분은 「12시간 안이면 효과적」이라고도 적는다"
    verified: text
diagram:
  title: "아세트아미노펜 과량 복용 — NAC 판단"
  nodes:
    - {id: start, kind: start, text: "아세트아미노펜 과량 복용 의심"}
    - {id: time, kind: decision, text: "복용 시각을 알고 단회 급성 복용인가?"}
    - {id: timeask, kind: info, text: "복용 시각·양·제형, 다른 약·음주, 금식 여부를 확인한다"}
    - {id: level, kind: decision, text: "복용 4시간 이후 혈중 농도가 노모그램 치료선 위인가?"}
    - {id: nac, kind: end, text: "N-아세틸시스테인 — 8시간 안에 시작할수록 좋다(늦어도 준다)"}
    - {id: nonac, kind: end, text: "NAC 불필요 — 동반 복용 약·자해 위험 평가"}
    - {id: unk, kind: alert, text: "시각 불명·반복 과량·AST/ALT 상승 — 노모그램을 쓸 수 없다, NAC 를 준다"}
  edges:
    - {from: start, to: time}
    - {from: time, to: level, label: "예"}
    - {from: time, to: unk, label: "아니오"}
    - {from: time, to: timeask, label: "정보 없음"}
    - {from: timeask, to: level, label: "시각 확인"}
    - {from: timeask, to: unk, label: "불명"}
    - {from: level, to: nac, label: "위"}
    - {from: level, to: nonac, label: "아래"}
diagram_notes:
  - "4시간 전 농도는 흡수가 끝나지 않아 노모그램에 찍지 않는다 — 4시간 이후 농도를 쓴다(해리슨: 4–8시간 농도) [[harrison-21: 340장 p.2588]]."
  - "초기 간수치 정상은 안심 근거가 아니다 — 손상은 24–48시간 뒤에 드러난다."
  - "며칠에 걸친 반복 과량(하루 8 g, 진통제·오피오이드 복합제)은 단회 노모그램으로 판정하지 않는다 [[harrison-21: 340장 p.2588]]."
pitfalls:
  - contrast: "「독성 대사물을 만드는 효소를 막는다」 vs NAC 의 실제 작용점"
    point: "NAPQI 를 만드는 효소가 CYP2E1 인 것은 맞다. 그러나 NAC 는 그 효소를 막지 않는다 — 설프히드릴기를 공급해 고갈된 글루타티온을 다시 채워, 이미 만들어지는 NAPQI 를 무해한 머캅투르산으로 만든다. 「효소 억제로 독성 대사물 생성 차단」은 메탄올·에틸렌글리콜 중독의 포메피졸(알코올 탈수소효소 억제) 같은 다른 해독제의 틀이다."
    exception: "만성 음주자에서 CYP2E1 유도가 독성 문턱을 낮추는 것은 사실이다 — 효소는 위험 요인 설명에 등장하지 해독 기전에 등장하지 않는다 [[harrison-21: 340장 p.2588]]."
    cites: ["harrison-21"]
    covers: ["usmle-2026-0025:B"]
  - contrast: "NAC vs 활성탄"
    point: "활성탄·콜레스티라민은 장관 안의 남은 약을 흡착해 흡수를 막는 조치이고, 복용 30분이 지나면 효과가 없어 보인다. 10시간 뒤 온 환자의 간 보호는 NAC 의 글루타티온 재보충이 맡는다 [[harrison-21: 340장 p.2588]]."
    cites: ["harrison-21"]
checks:
  - q: "아세트아미노펜 과량에서 간세포 괴사가 일어나는 순서는?"
    a: "황산·글루쿠론산 포합 포화 → CYP2E1 경로로 NAPQI 증가 → 글루타티온 고갈 → NAPQI 가 간세포 거대분자와 공유결합(단백 부가물) → 중심소엽 괴사."
  - q: "N-아세틸시스테인의 해독 기전은?"
    a: "설프히드릴기를 공급해 글루타티온을 다시 채운다 — NAPQI 를 포합해 무해화할 능력을 되살린다."
  - q: "복용 10시간 뒤 간수치가 정상이면 NAC 를 미뤄도 되나?"
    a: "아니다. 간 손상은 24–48시간에 드러나므로 혈중 농도(노모그램)로 판단하고, 치료선 위면 즉시 준다 — 8시간이 지났어도 효과가 있다."
variants:
  - id: v1
    of: usmle-2026-0025
    flip: true
    changed: "time since ingestion 10 hours → 25 minutes, and the question asks about the first gut-directed intervention given → answer shifts from glutathione repletion (NAC) to adsorption of drug in the gut lumen (activated charcoal)"
    context: "Same overdose; the patient arrives while unabsorbed drug is still in the gut"
    stem: "A 19-year-old woman is brought to the emergency department 25 minutes after swallowing a large number of acetaminophen tablets in front of her roommate. She is alert, protecting her airway, and has not vomited. Before a serum drug level can be obtained, she is given a single oral dose of an agent that is intended to reduce the amount of drug that reaches her liver. Which of the following best describes the mechanism of this agent?"
    choices:
      - "A. Replenishing hepatic glutathione to conjugate a reactive metabolite"
      - "B. Inhibiting CYP2E1 so the parent drug is excreted unchanged"
      - "C. Binding the parent drug within the gut lumen to prevent its absorption"
      - "D. Inducing glucuronosyltransferase to speed phase II conjugation"
      - "E. Antagonizing the receptor that mediates the drug's central effects"
    answer: "C"
    explanation: "Activated charcoal adsorbs unabsorbed drug in the gut lumen; Harrison notes it (like cholestyramine) appears ineffective once more than 30 minutes have passed since acetaminophen ingestion, so it has a role only in a patient who arrives this early. The single changed clue — 25 minutes instead of 10 hours after ingestion, with the agent aimed at reducing drug reaching the liver — makes the original distractor about gut-lumen binding correct. N-acetylcysteine (A) is still given if the 4-hour level is above the treatment line, but it acts after absorption by repleting glutathione."
    kind: application
  - id: v2
    of: usmle-2026-0025
    flip: false
    changed: "age, sex, setting (single intentional ingestion discovered by a partner), timing 10 → 6 hours and answer order changed; level still above the treatment line and question still asks the antidote's hepatoprotective mechanism → answer unchanged (glutathione repletion)"
    context: "Different patient and presentation; same antidote and same mechanism question"
    stem: "A 34-year-old man is brought to the emergency department by his partner, who found empty packets of an over-the-counter analgesic 6 hours after he took them during an argument. He has mild nausea. Vital signs, examination, serum aminotransferases, and INR are normal. A serum drug level drawn at 4 hours is above the treatment line on the nomogram, and intravenous N-acetylcysteine is started. This drug prevents hepatocellular necrosis primarily by which of the following mechanisms?"
    choices:
      - "A. Adsorbing unabsorbed drug remaining in the stomach"
      - "B. Blocking the cytochrome P450 isoenzyme that oxidizes the drug"
      - "C. Accelerating renal excretion of the unchanged parent drug"
      - "D. Supplying sulfhydryl groups that restore hepatic glutathione, which conjugates the reactive metabolite NAPQI"
      - "E. Inducing sulfotransferase enzymes to increase sulfate conjugation"
    answer: "D"
    explanation: "N-acetylcysteine supplies sulfhydryl donor groups that replete glutathione, which detoxifies NAPQI to mercapturic acid before it binds covalently to hepatocyte proteins. Changing the patient, the setting and the time (6 rather than 10 hours) does not change the key clue — a level above the treatment line with NAC started — so the mechanism answer is the same. Normal aminotransferases early do not exclude injury, which appears 24–48 hours later."
    kind: application
---

## 정의
아세트아미노펜 중독은 한 번의 과량(자해) 또는 며칠에 걸친 반복 과량(진통·해열 목적의 중복 복용)으로 용량 의존적 중심소엽 간괴사가 생기는 상태다. 아세트아미노펜은 직접 독소형 간 손상의 대표이며, 서구에서 급성 간부전의 가장 흔한 원인이다 [[harrison-21: 340장 p.2584, p.2588]].

## 병태생리
정상: 대부분 2상 반응(황산·글루쿠론산 포합)으로 무해한 대사물이 되고, 적은 양이 CYP2E1(1상)으로 NAPQI 가 된다. NAPQI 는 「간 보호」 글루타티온과 결합해 머캅투르산으로 콩팥에서 나간다. 과량이면 포합 경로가 감당하지 못한 몫이 CYP2E1 로 가 NAPQI 가 많아지고, 글루타티온이 고갈되면 NAPQI 가 간세포 거대분자와 공유결합한다(아세트아미노펜-단백 부가물). 이것이 괴사로 이어진다고 보나 정확한 순서는 밝혀지지 않았다 [[harrison-21: 340장 p.2588]].

## 기전에서 소견으로
- 독성 대사물 생성과 괴사에는 시간이 걸린다 → 4–12시간에는 구역·구토·설사·복통 정도, 24–48시간에 간 손상이 드러나고 3–5일에 최고.
- 3구역(중심정맥 주변)은 CYP2E1 이 많아 NAPQI 가 가장 많이 생긴다 → 중심소엽 괴사.
- 급성 괴사 → AST/ALT 가 10,000 IU/L 를 넘기도 하는데 빌리루빈은 낮다 — 이 조합 자체가 아세트아미노펜을 의심하게 하는 단서다 [[harrison-21: 340장 p.2588]].
- 콩팥 손상·심근 손상이 동반될 수 있다.

## 감별
매우 높은 아미노전이효소를 만드는 다른 원인 — 허혈성 간염(쇼크), 급성 바이러스 간염, 버섯(아마니타) 중독. 병력을 부인하거나 의식이 떨어져 있으면 아세트아미노펜을 추정 진단하고 NAC 를 준다.

## 검사
복용 4시간 이후의 혈중 농도를 노모그램에 찍는다(해리슨: 4–8시간 농도). 초기 간수치·INR 정상은 안심 근거가 아니다. 반복 과량·시각 불명이면 노모그램을 쓸 수 없다.

## 치료
1. **NAC** — 노모그램 치료선 위면 즉시. 8시간 안에 시작하고, 24–36시간에도 부분적 효과가 있다. 해리슨은 정맥 부하 140 mg/kg 뒤 70 mg/kg 4시간마다를 적는다 [[harrison-21: 340장 p.2588]].
2. **흡착** — 활성탄·콜레스티라민은 복용 30분이 지나면 효과가 없어 보인다.
3. **반응 확인** — 간수치·INR·크레아티닌·의식을 추적하고, 간부전 징후(뇌병증·응고장애)가 보이면 간이식 가능 기관과 상의한다.

## 권고와 예외
- 만성 음주자는 CYP2E1 유도와 글루타티온 생성 억제로 독성 용량이 2 g 까지 낮아질 수 있다 [[harrison-21: 340장 p.2588]].
- 굶주림·열성 질환으로 먹지 못한 사람도 글루타티온이 적어 위험이 크다.
- FDA 는 하루 최대 용량을 4 g 에서 3 g 로 줄이라고 권했고, 오피오이드 복합제의 아세트아미노펜은 1정 325 mg 으로 제한했다(해리슨이 인용) [[harrison-21: 340장 p.2588]].

## 시험 쟁점 — 충돌·맥락·새 근거
- **Z1 충돌 · NAC 를 시작하는 노모그램 문턱과 시점** — 시험 기준: 복용 4시간 이후 농도가 노모그램 치료선 위면 NAC, 8시간 안에 시작이 가장 좋고 늦어도 준다 [[harrison-21: 340장 p.2588]] / 다른 기준: 해리슨 같은 쪽 안에서도 「4시간 >300 µg/mL 는 중증 예측, <150 은 손상 가능성 매우 낮음」「4시간 >200·8시간 >100 이면 NAC 가 괴사를 크게 줄임」「12시간 안이면 효과적」「8시간 안에 시작」이 함께 나온다 [[harrison-21: 340장 p.2588]] / 왜 다른가: 앞의 두 수치는 예후 예측, 뒤는 치료 효과를 입증한 집단의 기준이다. 미국 응급실의 치료선 수치는 이 정리본에서 원문 대조하지 못했다 / 시험에서는: USMLE 는 「치료선 위 → NAC」와 「8–10시간 안이면 거의 완전 예방, 늦어도 준다」를 묻는다. KMLE 도 수치 자체보다 「혈중 농도로 판단 · 간수치 정상이어도 준다」를 묻는다.

## (심화) 해독 기전을 가르는 법
표 「보기로 나오는 해독 기전」. 기전 문항은 해독제의 작용점을 사슬 위의 위치로 묻는다 — 흡수 전(흡착), 대사 효소(억제·유도), 독성 대사물 제거(포합 기질 공급), 표적 수용체(길항). NAC 는 「독성 대사물 제거」 칸에 있다.
