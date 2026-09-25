---
id: cn.biochem.mcad-deficiency.hypoketotic-hypoglycemia
type: concept
topic: Biochemistry
see_also: [Pediatrics, Endocrinology]
date: 2026-09-23
updated: 2026-09-25
version: 2
outline: basic.biochem   # 기본틀 슬롯(content/outline/subjects.yaml) — 해리슨 장 없음
confidence: medium
review_status: unreviewed
note_form: 2             # 판형 2(2026-09-25) — 결론·시험 단서·왜 → 혼동 → 표·도식 → 목표에 맞춘 본문
title: "MCAD 결핍 — 케톤 없는 공복 저혈당, C8 이 가른다"
objective: "공복 때 간이 지방산 β산화로 아세틸-CoA 를 만들어 케톤 생성과 당신생을 동시에 떠받치는 원리를 설명하고, 공복·감염 뒤 저케톤성 저혈당·정상 젖산·유리지방산 상승·아실카르니틴 C8 상승을 근거로 중쇄 아실-CoA 탈수소효소(MCAD) 결핍을 글리코겐 분해·당신생·케톤 합성·카르니틴 운반 결핍과 구별한다"
objective_kind: 기전
condition: 중쇄 아실-CoA 탈수소효소(MCAD) 결핍
exams: [usmle, kmle]
summary:
  - "결론: 공복 뒤 저케톤성 저혈당 + 유리지방산 상승 + 젖산 정상 + 아실카르니틴 C8 상승 = MCAD 결핍."
  - "시험 단서: 3–24개월, 장염·중이염으로 못 먹은 뒤 기면·경련, 케톤 음성(hypoketotic hypoglycemia), 옥타노일카르니틴(C8)."
  - "왜: β산화가 중쇄에서 멈춰 간의 아세틸-CoA 가 모자라다 — 케톤 원료와 당신생의 활성·에너지가 함께 끊긴다."
  - "케톤은 「저혈당에 비해 적절한가」로 본다. 케톤 상승이면 글리코겐 분해 장애, 젖산 상승이면 당신생 장애."
  - "유리지방산이 낮으면 고인슐린혈증. 급성기는 포도당 정맥 투여, 장기는 공복 회피 — 중쇄 중성지방(MCT)은 피한다."
pitfalls:
  - contrast: "간 글리코겐 인산화효소 결핍(당원병 Ⅵ형) vs MCAD 결핍 — 둘 다 공복 저혈당·간비대"
    point: "글리코겐 분해가 막혀도 지방산 β산화는 멀쩡해 공복 때 케톤이 잘 오른다(케톤성 저혈당, 대개 경증). MCAD 결핍은 β산화가 막혀 케톤이 오르지 않는다. 저혈당과 간비대만으로는 가를 수 없고, 소변·혈중 케톤이 가른다."
    exception: "당원병 Ⅰ형(포도당-6-인산분해효소)은 케톤이 낮을 수 있지만 젖산산증·고요산·고중성지방이 함께 온다."
    cites: ["?saudubray-iem"]
    covers: ["usmle-2026-0104:C"]
  - contrast: "HMG-CoA 분해효소 결핍 vs MCAD 결핍 — 둘 다 저케톤성 저혈당"
    point: "HMG-CoA 분해효소는 케톤 합성의 마지막 단계라, 결핍돼도 저케톤성 저혈당이 된다. 그러나 β산화는 끝까지 돌아 C8 이 쌓이지 않는다. 대신 류신 분해 중간물이 쌓여 대사성 산증과 소변 3-하이드록시-3-메틸글루타르산, 아실카르니틴 C5-OH 가 오른다. 「케톤이 없는 이유」를 물어도 C8 상승이 있으면 답은 β산화 단계(MCAD)다."
    cites: ["?saudubray-iem"]
    covers: ["usmle-2026-0044:E"]
  - contrast: "CPT Ⅰ 결핍 vs MCAD 결핍"
    point: "CPT Ⅰ 은 긴사슬 지방산을 미토콘드리아로 들이는 입구다. 결핍되면 역시 저케톤성 저혈당이지만 아실카르니틴이 만들어지지 않아 유리 카르니틴이 높고 긴사슬 아실카르니틴은 낮다 — C8 이 특이적으로 오르지 않는다. 중쇄 지방산은 CPT 없이 미토콘드리아에 들어가므로 CPT Ⅰ 결핍에서 중쇄 지방은 에너지원이 되지만, MCAD 결핍에서는 금기다."
    cites: ["?saudubray-iem"]
  - contrast: "피루브산 탈수소효소 결핍"
    point: "피루브산 → 아세틸-CoA 가 막혀 젖산·피루브산이 오르고 신경 증상이 주다. 공복 저혈당·C8 상승의 그림이 아니다."
    cites: ["?saudubray-iem"]
criteria:
  - id: mcad-screen
    name: 선별·확진(GeneReviews)
    kind: 진단 기준
    population: "신생아 선별 양성 또는 저케톤성 저혈당 영유아"
    statement: "혈장 아실카르니틴에서 C8 이 두드러지게 오르고 C6·C10·C10:1 이 함께 오르며 C8/C10 비가 높다. ACADM 유전자 검사(흔한 변이 c.985A>G)로 확진"
    exceptions: "대사위기 사이·포도당 투여 뒤에는 이상이 약해질 수 있다. 세부 비율 기준은 원문 미대조"
    source: genereviews-mcad
    locator: "Diagnosis 절(원문 미대조 — 루틴 컨테이너에서 NCBI 접근 차단)"
    basis: current
    exams: [usmle, kmle]
sources:
  - id: genereviews-mcad
    org: "GeneReviews (University of Washington, Seattle)"
    title: "Medium-Chain Acyl-Coenzyme A Dehydrogenase Deficiency"
    kind: review
    year: 2019
    citation: "Merritt JL 2nd, Chang IJ. Medium-Chain Acyl-Coenzyme A Dehydrogenase Deficiency. In: Adam MP, et al, eds. GeneReviews. Seattle (WA): University of Washington, Seattle; 2000 (updated 2019). NBK1424"
    url: "https://www.ncbi.nlm.nih.gov/books/NBK1424/"
    checked_at: 2026-09-23
    checked: "서지만 — 루틴 컨테이너의 네트워크 정책이 NCBI 접근을 막아 본문을 대조하지 못했다. 발병 연령·아실카르니틴 패턴·흔한 변이·치료(공복 회피·포도당) 서술은 기억에 근거하며 사람 대조가 필요하다"
    verified: citation
  - id: saudubray-iem
    org: "Springer"
    title: "Inborn Metabolic Diseases: Diagnosis and Treatment, 7th ed."
    kind: textbook
    year: 2022
    citation: "Saudubray JM, Baumgartner MR, García-Cazorla Á, Walter JH (eds). Inborn Metabolic Diseases: Diagnosis and Treatment, 7th ed. Berlin: Springer; 2022"
    doi: "10.1007/978-3-662-63123-2"
    checked_at: 2026-09-23
    checked: "서지만 — 본문(저혈당 감별·지방산 산화 장애 장)을 열어 보지 못했다. 감별표의 케톤·젖산·유리지방산 양상은 기억에 근거"
    verified: citation
tables:
  - id: fasting-ddx
    section: "가르는 소견 — 케톤·젖산·유리지방산으로 좁히기"
    title: "공복 저혈당 — 결손 단계별 검사 양상"
    role: differential
    span: full
    columns: ["결손(예)", "케톤", "젖산", "유리지방산", "가르는 검사", "근거"]
    rows:
      - ["MCAD (중쇄 β산화)", "낮음", "정상", "높음", "아실카르니틴 C8(·C6·C10:1) 상승", "[[?genereviews-mcad]]"]
      - ["CPT Ⅰ (카르니틴 운반 입구)", "낮음", "정상", "높음", "유리 카르니틴 높음, 긴사슬 아실카르니틴 낮음", "[[?saudubray-iem]]"]
      - ["HMG-CoA 분해효소 (케톤 합성 끝)", "낮음", "정상~상승", "높음", "대사성 산증, 소변 3-하이드록시-3-메틸글루타르산, C5-OH", "[[?saudubray-iem]]"]
      - ["포도당-6-인산분해효소 (당원병 Ⅰ형)", "낮음~중간", "높음", "높음", "젖산산증·고요산·고중성지방, 글루카곤에 무반응", "[[?saudubray-iem]]"]
      - ["간 글리코겐 인산화효소 (당원병 Ⅵ형)", "높음", "정상", "높음", "경한 저혈당·간비대, 아실카르니틴 정상", "[[?saudubray-iem]]"]
      - ["고인슐린혈증", "낮음", "정상", "낮음", "저혈당 때 인슐린 검출, 글루카곤에 혈당 반응", "[[?saudubray-iem]]"]
    note: "케톤은 「저혈당에 비해 적절한가」로 판단한다 — 같은 수치라도 혈당이 30 mg/dL 대이면 낮은 것이다. 검체는 저혈당 발작 중(포도당 투여 전)에 받아야 해석할 수 있다 [[?saudubray-iem]]."
diagram:
  title: "공복·감염 뒤 저혈당 영유아 — 결손 단계를 좁히는 순서"
  nodes:
    - {id: start, kind: start, text: "공복·구토·감염 뒤 기면·경련 — 포도당 전 검체"}
    - {id: ketone, kind: decision, text: "혈당에 비해 케톤이 적절히 올랐는가?"}
    - {id: ketotic, kind: end, text: "케톤성 저혈당 — 글리코겐 분해 장애·특발성"}
    - {id: ffa, kind: decision, text: "유리지방산이 올랐는가?"}
    - {id: insulin, kind: end, text: "고인슐린혈증 — 지방 분해·케톤 생성을 함께 누름"}
    - {id: lactate, kind: decision, text: "젖산이 올랐는가?"}
    - {id: gsd1, kind: end, text: "당신생 장애 — 당원병 Ⅰ형 등"}
    - {id: info, kind: info, text: "지방산 산화·케톤 합성 장애 — 아실카르니틴·유기산"}
    - {id: acyl, kind: decision, text: "아실카르니틴·유기산 양상은?"}
    - {id: mcad, kind: end, text: "C8 상승 → MCAD 결핍"}
    - {id: hmgcl, kind: end, text: "C5-OH·유기산 → HMG-CoA 분해효소 결핍"}
    - {id: cpt1, kind: end, text: "유리 카르니틴↑·긴사슬 아실카르니틴↓ → CPT Ⅰ"}
  edges:
    - {from: start, to: ketone}
    - {from: ketone, to: ketotic, label: "적절히 상승"}
    - {from: ketone, to: ffa, label: "낮음"}
    - {from: ffa, to: insulin, label: "낮음"}
    - {from: ffa, to: lactate, label: "높음"}
    - {from: lactate, to: gsd1, label: "높음"}
    - {from: lactate, to: info, label: "정상"}
    - {from: info, to: acyl}
    - {from: acyl, to: mcad, label: "C8 상승"}
    - {from: acyl, to: hmgcl, label: "C5-OH·유기산"}
    - {from: acyl, to: cpt1, label: "유리 카르니틴↑"}
diagram_notes:
  - "치료는 진단을 기다리지 않는다 — 저혈당이면 먼저 포도당을 주고, 검체(케톤·젖산·유리지방산·인슐린·아실카르니틴·암모니아)는 그 전에 받아 둔다."
  - "유리지방산 갈래는 「지방 분해가 일어났는가」를 묻는다. 케톤성 저혈당 갈래의 글리코겐 분해 장애는 간 인산화효소 결핍 등이다."
  - "당원병 Ⅰ형(포도당-6-인산분해효소 결핍)도 케톤이 낮게 나올 수 있어 「케톤 낮음」 갈래에서 젖산으로 한 번 더 가른다."
  - "HMG-CoA 분해효소 결핍의 유기산은 소변 3-하이드록시-3-메틸글루타르산이다."
  - "MCAD 결핍이면 포도당(10 %) 정맥 투여, 이후 공복 회피."
  - "각 갈래의 검사 양상은 원문 미대조(†) — 전형 양상이며 예외가 있다."
checks:
  - q: "MCAD 결핍에서 케톤도 안 생기고 당신생도 약해지는 이유를 한 물질로 설명하라."
    a: "아세틸-CoA. β산화가 중쇄에서 멈춰 간의 아세틸-CoA 가 모자라면 케톤 원료가 없고, 피루브산 카르복실화효소를 활성화할 아세틸-CoA 와 β산화의 ATP·NADH 도 부족해 당신생이 약해진다."
  - q: "저케톤성 저혈당 아이에서 유리지방산이 낮다면 무엇을 먼저 의심하나?"
    a: "고인슐린혈증. 인슐린이 지방 분해 자체를 막아 유리지방산과 케톤이 함께 낮다. 지방산 산화 장애는 지방 분해는 일어나 유리지방산이 높다."
  - q: "MCAD 결핍 환아의 장기 관리 원칙은?"
    a: "공복을 피한다(나이에 맞는 수유 간격, 아플 때 탄수화물 공급·먹지 못하면 병원에서 포도당 정맥 투여). 중쇄 중성지방(MCT) 식품은 피한다."
variants:
  - id: v1
    of: usmle-2026-0104
    flip: true
    changed: "urine ketones negative + C8 elevation → urine ketones strongly positive, normal acylcarnitine profile, milder hypoglycemia with prominent hepatomegaly and short stature ⇒ answer changes from MCAD to liver glycogen phosphorylase"
    context: "Same fasting hypoglycemia with hepatomegaly, but ketosis is intact"
    stem: "A 3-year-old boy is evaluated for morning irritability and sweating that resolve after breakfast. He is at the 5th percentile for height. Temperature is 36.8°C, pulse 110/min, respirations 24/min, and blood pressure 96/60 mm Hg. The liver edge is palpable 5 cm below the right costal margin; the spleen is not palpable. After an overnight fast, serum glucose is 54 mg/dL and urine ketones are strongly positive. Serum lactate, uric acid, and creatine kinase are within normal limits; AST and ALT are mildly elevated. Plasma acylcarnitine profile is normal. Deficiency of which of the following enzymes is the most likely cause?"
    choices: ["A. Carnitine palmitoyltransferase I", "B. Glucose-6-phosphatase", "C. Liver glycogen phosphorylase", "D. HMG-CoA lyase", "E. Medium-chain acyl-CoA dehydrogenase"]
    answer: "C"
    explanation: "Fasting hypoglycemia with hepatomegaly and growth delay but appropriately brisk ketosis, normal lactate, and a normal acylcarnitine profile indicates impaired hepatic glycogen breakdown with intact fatty acid oxidation — liver glycogen phosphorylase deficiency (Hers disease). In the original item the decisive clue was the absence of ketones with a C8 elevation, which places the block in beta-oxidation (MCAD). Glucose-6-phosphatase deficiency would add lactic acidosis and hyperuricemia; CPT I, HMG-CoA lyase, and MCAD deficiencies all prevent ketosis."
    kind: application
  - id: v2
    of: usmle-2026-0104
    flip: false
    changed: "age, sex, precipitating illness (otitis media instead of gastroenteritis), presentation (seizure), and order of data changed; hypoketotic hypoglycemia with C8 elevation kept ⇒ answer still MCAD"
    context: "Different child, same biochemical signature"
    stem: "A 22-month-old girl has a generalized seizure at home. For the past 36 hours she has had ear pain and fever and has eaten very little. Her 4-year-old brother died suddenly in his sleep at 16 months of age. Temperature is 38.4°C, pulse 150/min, respirations 34/min, and blood pressure 90/54 mm Hg. The liver is palpable 3 cm below the costal margin, and the right tympanic membrane is bulging. Plasma acylcarnitine analysis shows a marked increase in octanoylcarnitine with smaller increases in hexanoyl- and decenoylcarnitine. Serum glucose is 29 mg/dL, plasma free fatty acids are elevated, lactate is 1.5 mmol/L, and urine ketones are negative. Impaired activity of which of the following enzymes is the most likely cause?"
    choices: ["A. Carnitine palmitoyltransferase I", "B. Glucose-6-phosphatase", "C. Liver glycogen phosphorylase", "D. HMG-CoA lyase", "E. Medium-chain acyl-CoA dehydrogenase"]
    answer: "E"
    explanation: "The story is different — an older girl, an ear infection, a seizure, a sibling's sudden death — but the decisive clues are unchanged: hypoglycemia without ketosis despite high free fatty acids, normal lactate, and a C8-predominant acylcarnitine profile. That pattern localizes the block to medium-chain beta-oxidation (MCAD). Liver phosphorylase deficiency would allow ketosis; glucose-6-phosphatase deficiency would raise lactate; HMG-CoA lyase and CPT I deficiencies do not produce a C8 elevation."
    kind: application
  - id: v3
    of: usmle-2026-0044
    flip: true
    changed: "C8 elevation → C5-OH acylcarnitine and urinary 3-hydroxy-3-methylglutaric acid with metabolic acidosis ⇒ answer changes from MCAD to HMG-CoA lyase"
    context: "Hypoketotic hypoglycemia where beta-oxidation runs to completion"
    stem: "A 10-month-old boy is brought to the emergency department because of lethargy after 2 days of vomiting with a viral illness. Temperature is 37.9°C, pulse 160/min, respirations 44/min and deep, and blood pressure 88/52 mm Hg. Serum glucose is 31 mg/dL, bicarbonate 11 mEq/L, and ammonia mildly elevated; urine ketones are negative. Plasma free fatty acids are elevated and lactate is 2.4 mmol/L. Plasma acylcarnitine analysis shows elevated 3-hydroxyisovalerylcarnitine (C5-OH) with a normal octanoylcarnitine (C8) level, and urine organic acids show a large peak of 3-hydroxy-3-methylglutaric acid. Which of the following best explains the absence of ketosis in this child?"
    choices: ["A. Impaired carnitine palmitoyltransferase-1 activity prevents long-chain fatty acids from entering the mitochondria", "B. Deficient glucose-6-phosphatase activity prevents the final step of glycogenolysis and gluconeogenesis", "C. Deficient pyruvate dehydrogenase activity prevents conversion of pyruvate to acetyl-CoA", "D. Deficient medium-chain acyl-CoA dehydrogenase activity blocks beta-oxidation of medium-chain fatty acids, limiting the acetyl-CoA available for ketogenesis", "E. Deficient HMG-CoA lyase activity blocks the terminal step of ketone body synthesis"]
    answer: "E"
    explanation: "Beta-oxidation is intact here — C8 is normal — so acetyl-CoA is produced but cannot be turned into acetoacetate. HMG-CoA lyase is also the last step of leucine breakdown, which explains the C5-OH acylcarnitine, urinary 3-hydroxy-3-methylglutaric acid, and metabolic acidosis. In the original item the C8 elevation was the clue that placed the block upstream, in medium-chain beta-oxidation (MCAD)."
    kind: application
  - id: v4
    of: usmle-2026-0044
    flip: false
    changed: "age, sex, trigger (prolonged fast before a procedure instead of febrile illness), and presentation changed; hypoketotic hypoglycemia, high free fatty acids, normal lactate, and C8 elevation kept ⇒ answer still MCAD"
    context: "Same mechanism question in a different fasting setting"
    stem: "A 2-year-old boy is kept fasting for 16 hours before a scheduled dental procedure under anesthesia because of an operating room delay. He becomes pale, sweaty, and difficult to rouse. Temperature is 36.6°C, pulse 142/min, respirations 28/min, and blood pressure 94/58 mm Hg. Serum glucose is 36 mg/dL, plasma free fatty acids are 2.4 mmol/L, lactate is 1.2 mmol/L, and serum insulin is undetectable. Urine ketones are trace. A plasma acylcarnitine profile shows a prominent increase in octanoylcarnitine. Which of the following best explains why this child is not ketotic?"
    choices: ["A. Impaired carnitine palmitoyltransferase-1 activity prevents long-chain fatty acids from entering the mitochondria", "B. Deficient glucose-6-phosphatase activity prevents the final step of glycogenolysis and gluconeogenesis", "C. Deficient pyruvate dehydrogenase activity prevents conversion of pyruvate to acetyl-CoA", "D. Deficient medium-chain acyl-CoA dehydrogenase activity blocks beta-oxidation of medium-chain fatty acids, limiting the acetyl-CoA available for ketogenesis", "E. Deficient HMG-CoA lyase activity blocks the terminal step of ketone body synthesis"]
    answer: "D"
    explanation: "Undetectable insulin and high free fatty acids show that lipolysis is working; normal lactate argues against a gluconeogenic block. The octanoylcarnitine (C8) rise localizes the defect to medium-chain beta-oxidation, so the liver lacks acetyl-CoA for ketogenesis — MCAD deficiency. HMG-CoA lyase deficiency would leave C8 normal and raise C5-OH; CPT I deficiency would not generate medium-chain acylcarnitines."
    kind: application
---

## 기전 — 공복 에너지 전환에서 저케톤성 저혈당으로
**MCAD 결핍**(medium-chain acyl-CoA dehydrogenase deficiency)은 미토콘드리아 β산화에서 중쇄(대략 C12–C4) 아실-CoA 의 첫 탈수소 단계를 맡는 효소가 결핍된 상염색체 열성 질환이다(ACADM 유전자). 가장 흔한 지방산 산화 장애이고, 탠덤질량분석 신생아 선별로 대부분 증상 전에 발견된다 [[?genereviews-mcad]].
- **정상 공복**: 식후에는 포도당이 주 연료이고 남는 포도당은 글리코겐·지방으로 저장된다. 짧은 공복은 간 글리코겐 분해가 막는다(영유아는 글리코겐이 적어 이 단계가 짧다). 긴 공복에는 인슐린이 떨어지고 글루카곤이 올라 지방조직에서 유리지방산이 나온다. 긴사슬 지방산은 **카르니틴 셔틀**(CPT Ⅰ → 전위효소 → CPT Ⅱ)로, 중쇄 지방산은 카르니틴 없이 미토콘드리아에 들어가 β산화로 두 탄소씩 잘려 **아세틸-CoA** 가 된다.
- 간의 아세틸-CoA 는 ① HMG-CoA 합성효소·분해효소를 거쳐 **케톤체**(아세토아세트산·β-하이드록시부티르산)가 되어 뇌의 대체 연료가 되고, ② 피루브산 카르복실화효소를 활성화하며 β산화가 낸 ATP·NADH 와 함께 **당신생**을 돌린다 [[?genereviews-mcad]].
- **MCAD 가 없으면** 긴사슬은 중쇄까지 잘린 뒤 멈춘다. ① 아세틸-CoA 부족 → 케톤 생성 실패(뇌의 대체 연료 없음). ② 피루브산 카르복실화효소 활성화와 에너지 공급이 줄어 당신생도 약해져, 글리코겐이 바닥나는 순간 저혈당이 급격히 온다. ③ 옥타노일-CoA 등이 카르니틴에 붙어 **C8 아실카르니틴**으로 혈중에 나오고(진단 표지), 카르니틴이 소모되어 2차 카르니틴 결핍이 올 수 있다. 쌓인 중쇄 지방산과 에너지 부족이 간 기능 장애(고암모니아혈증·간효소 상승·지방간)와 뇌병증을 부른다 [[?genereviews-mcad]].
- 평소 잘 먹을 때는 증상이 없고 **공복이 길어질 때**만 문제다 — 선별과 공복 회피만으로 예후가 크게 달라지는 이유다.

## 가르는 소견 — 케톤·젖산·유리지방산으로 좁히기
- **유발·증상**: 장염·중이염 같은 흔한 감염으로 먹지 못하거나 토한 뒤, 또는 긴 금식 뒤 구토·기면 → 경련·혼수. 첫 발작은 대개 3–24개월이고 첫 발작에서 급사할 수 있어, 형제의 원인 불명 급사가 단서가 된다 [[?genereviews-mcad]].
- **MCAD 의 검사 양상**: 저혈당, **케톤 음성 또는 미량**(저혈당 정도에 비해 부적절), **유리지방산 상승**(지방 분해는 정상 작동), **젖산 정상**, 경한 고암모니아혈증·간효소 상승, 간비대(라이 증후군 유사). 아실카르니틴은 C8 이 두드러지고 C6·C10:1 이 함께 오르며, 소변 유기산에서 헥사노일글리신·수베릴글리신과 디카르복실산 [[?genereviews-mcad]].
- 공복 저혈당은 **어느 단계가 막혔나**로 푼다(감별표·도식). 케톤이 잘 오르는 갈래에는 간 인산화효소 외에 인산화효소 키나아제 결핍(당원병 Ⅸ형)과 특발성 케톤성 저혈당도 들어간다. 케톤 낮음·유리지방산 높음·젖산 정상이면 지방산 산화 또는 케톤 합성 장애이고, 효소는 아실카르니틴·소변 유기산이 가린다 [[?saudubray-iem]].

## 검사 — 발작 중 검체와 확진
1. **발작 중 검체(포도당 투여 전)**: 혈당·케톤(β-하이드록시부티르산)·유리지방산·젖산·인슐린·암모니아·간효소. 포도당을 준 뒤에는 양상이 흐려진다.
2. **혈장 아실카르니틴·유리 카르니틴**: C8 우세 상승과 C8/C10 비 상승이 특징적이다. 발작 사이에는 약해질 수 있다 [[?genereviews-mcad]].
3. **소변 유기산·아실글리신**: 헥사노일글리신·수베릴글리신.
4. **ACADM 유전자 검사**: 확진. 북유럽계에서 흔한 c.985A>G 변이 [[?genereviews-mcad]].

## 치료 — 포도당과 공복 회피
- **급성기**: 즉시 포도당 정맥 투여(10 % 포도당)로 저혈당을 교정하고 인슐린 분비를 끌어내 지방 분해를 멈춘다. 저혈당이 교정된 뒤에도 뇌병증이 남을 수 있어 포도당 주입을 유지한다 [[?genereviews-mcad]].
- **장기**: 공복 회피가 핵심 — 나이에 맞는 수유·식사 간격, 잠들기 전 탄수화물, 아플 때(구토·식이 거부) 조기 병원 방문과 포도당 정맥 투여 계획서. 중쇄 중성지방(MCT) 식품은 피한다. 카르니틴 보충은 논란이다 [[?genereviews-mcad]].

## 권고와 예외
- 선별 양성 신생아는 증상이 없어도 확진 전부터 공복 회피 지침을 준다.
- 성인기까지 진단되지 않다가 금식·음주·수술 전 금식에서 처음 드러나기도 한다 [[?genereviews-mcad]].
- 대상: 기초의학 슬롯이라 해리슨 대조 대상이 아니다. 서술은 원문 미대조(†)이므로 사람 대조가 필요하다.

## (심화) 왜 CPT Ⅰ 결핍에서는 중쇄 지방이 치료가 되고 MCAD 결핍에서는 금기인가
중쇄 지방산은 카르니틴 셔틀 없이 미토콘드리아로 들어간다. 그래서 입구(CPT Ⅰ)가 막힌 환자에게 MCT 는 셔틀을 우회해 β산화를 돌리는 연료가 된다. MCAD 결핍은 바로 그 중쇄 단계가 막힌 병이라, MCT 를 주면 처리하지 못하는 중쇄 대사물만 더 쌓인다 — 같은 「지방산 산화 장애」라도 막힌 자리가 치료를 뒤집는다 [[?saudubray-iem]].
