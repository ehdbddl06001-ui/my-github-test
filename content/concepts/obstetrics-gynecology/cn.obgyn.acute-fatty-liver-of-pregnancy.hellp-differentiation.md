---
id: cn.obgyn.acute-fatty-liver-of-pregnancy.hellp-differentiation
type: concept
topic: Obstetrics & Gynecology
see_also: [Gastroenterology]
date: 2026-09-25
updated: 2026-09-25
version: 1
outline: ob.medical-complications   # 기본틀 슬롯(content/outline/subjects.yaml)
confidence: medium
review_status: unreviewed
note_form: 2            # 판형 2(2026-09-25)
title: "급성 임신 지방간 — HELLP와는 간부전으로 가른다"
objective: "임신 3분기 간효소 상승 환자에서 간 합성 기능 부전과 미세혈관병성 용혈 소견으로 급성 임신 지방간과 HELLP 증후군을 감별한다"
objective_kind: 감별
condition: 급성 임신 지방간(acute fatty liver of pregnancy, AFLP)
exams: [usmle, kmle]
summary:
  - "결론: 3분기 간효소 상승에 저혈당·INR 연장·섬유소원 저하·뇌증이 앞서면 HELLP 가 아니라 급성 임신 지방간이다."
  - "시험 단서: 35주 전후 구토·상복부 통증·황달·갈증 + 혈당↓·INR↑, 분열적혈구 없음 = AFLP(acute fatty liver)."
  - "왜: AFLP 는 간세포 자체가 지방으로 기능을 잃고, HELLP 는 내피 손상으로 적혈구가 깨지는 병이다."
  - "HELLP 의 중심은 용혈(분열적혈구·LDH 상승)·혈소판감소와 전자간증 — 합성 기능은 대개 늦게까지 남는다."
  - "치료는 둘 다 모체 안정(포도당·혈장·혈액제제) 뒤 분만 — 감별은 치료보다 원인·신생아 검사를 바꾼다."
pitfalls:
  - contrast: "HELLP 증후군 vs 급성 임신 지방간"
    point: "같은 3분기·상복부 통증·간효소 상승·혈소판감소를 공유한다. 가르는 것은 간 합성 기능(혈당·INR·섬유소원·암모니아)과 용혈(분열적혈구·LDH)이다 — 간부전이 앞서고 용혈이 약하면 AFLP."
    exception: "두 질환은 같은 스펙트럼에 있어 겹칠 수 있고, HELLP 도 진행하면 파종혈관내응고로 응고장애가 온다 — 한 소견이 아니라 조합으로 본다."
    cites: ["harrison-21: 479장 p.3763", "harrison-21: 479장 p.3767"]
    covers: ["usmle-2026-0175:A"]
  - contrast: "임신 담즙정체 vs 급성 임신 지방간"
    point: "임신 담즙정체(intrahepatic cholestasis)는 심한 가려움과 담즙산 상승이 핵심이고 간부전을 만들지 않는다. 가려움 없이 저혈당·응고장애가 있으면 담즙정체가 아니다."
    cites: ["harrison-21: 479장 p.3767"]
    covers: ["usmle-2026-0175:C"]
  - contrast: "급성 바이러스 간염 vs 급성 임신 지방간"
    point: "바이러스 간염도 황달·간부전을 만들지만 시기와 무관하고 혈청검사로 가른다. 혈청검사 음성 + 3분기 + 갈증·저혈당 조합은 AFLP 쪽이다."
    exception: "E형 간염은 임신 중 중증이 될 수 있어 흔한 A·B·C형이 음성이면 필요 시 추가 검사한다 [[?acg-2016]]."
    covers: ["usmle-2026-0175:D"]
  - contrast: "혈전혈소판감소자색반(TTP) vs 급성 임신 지방간"
    point: "TTP 는 미세혈관병성 용혈이 필수라 분열적혈구가 있어야 하고, 응고인자 합성은 보존돼 INR 이 정상인 것이 전형이다. 분열적혈구 없음 + INR 연장은 TTP 보다 간부전이다."
    covers: ["usmle-2026-0175:E"]
tables:
  - id: ddx
    section: "가르는 소견 — 간부전인가, 용혈인가"
    title: "임신 3분기 간효소 상승 감별"
    role: differential
    span: full
    columns: ["질환", "중심 병리", "가르는 소견", "처치"]
    rows:
      - ["급성 임신 지방간(AFLP)", "간세포 미세수포 지방증 → 간부전", "빌리루빈·암모니아 뚜렷이 상승, 저혈당 [[harrison-21: 479장 p.3767]] · INR↑·섬유소원↓·뇌증·갈증·급성 신손상 [[?acg-2016]]", "안정 후 분만 + 보존 치료 [[harrison-21: 479장 p.3767]] · 신생아 지방산 산화 검사 [[?acg-2016]]"]
      - ["HELLP 증후군", "전자간증의 중증 아형 — 내피 손상·미세혈관병성 용혈 [[harrison-21: 479장 p.3763]]", "분열적혈구·LDH 상승·혈소판감소, 대개 고혈압·단백뇨 [[?acg-2016]]", "안정 후 분만(전자간증 중증에 준함) [[harrison-21: 479장 p.3763]]"]
      - ["임신 담즙정체", "담즙 대사 변화", "3분기 심한 가려움 + 담즙산 상승, 간효소는 있거나 없음 [[harrison-21: 479장 p.3767]]", "우르소디올, 태아 감시, 37주까지 분만 [[harrison-21: 479장 p.3767]]"]
      - ["급성 바이러스 간염", "바이러스성 간세포 손상", "시기 무관, 혈청검사 양성", "원인별"]
      - ["TTP", "ADAMTS13 결핍 미세혈전", "분열적혈구 필수, INR 정상이 전형", "혈장교환"]
    note: "LDH 의 HELLP 기준값(흔히 ≥ 600 U/L)은 이 정리본에서 원문 대조하지 않았다 [[?acg-2016]]."
criteria:
  - id: aflp-vs-hellp
    name: AFLP 를 가르는 소견
    kind: 감별 기준
    population: "임신 3분기 간효소 상승 산모"
    statement: "급성 임신 지방간은 빌리루빈·암모니아의 뚜렷한 상승과 저혈당으로 구별된다(해리슨은 HELLP·전자간증과 같은 스펙트럼에 둔다) [[harrison-21: 479장 p.3767]]"
    exceptions: "HELLP 도 진행하면 응고장애가 생긴다 [[harrison-21: 479장 p.3763]] — 용혈·고혈압 동반 여부를 함께 본다"
    source: harrison-21
    basis: current
    exams: [usmle, kmle]
  - id: aflp-management
    name: 치료
    kind: 치료 권고
    population: "급성 임신 지방간"
    statement: "분만과 보존 치료(포도당·혈장·혈액제제로 교정) [[harrison-21: 479장 p.3767]]"
    exceptions: "신생아 LCHAD 등 지방산 산화 결함 검사, 다음 임신 재발 상담 [[?acg-2016]]"
    source: harrison-21
    basis: current
    exams: [usmle, kmle]
sources:
  - id: harrison-21
    org: "McGraw Hill"
    title: "Harrison's Principles of Internal Medicine, 21st ed. — Chapter 479: Medical Disorders During Pregnancy"
    kind: textbook
    year: 2022
    citation: "Loscalzo J, Kasper DL, Longo DL, et al (eds). Harrison's Principles of Internal Medicine, 21e. 479장 p.3763(Preeclampsia · HELLP), p.3767(Gastrointestinal and Liver Disease)"
    checked_at: 2026-09-25
    checked: "본문 대조(드라이브 479장 문서) — p.3763: 전자간증 중증 소견(혈압 ≥160/110, 혈소판 <100×10⁹/L, 크레아티닌 >1.1, 트랜스아미나제 2배), HELLP 는 중증 전자간증의 특수 아형, 응고장애·간피막 파열은 전자간증의 말단장기 합병증, 내피 손상(항혈관신생 인자) 기전, 분만이 결정적 치료. p.3767: 임신 담즙정체는 3분기 심한 가려움 + 담즙산 상승, 37주까지 분만·우르소디올; 급성 임신 지방간은 드문 합병증으로 HELLP·전자간증과 같은 스펙트럼, 빌리루빈·암모니아의 뚜렷한 상승과 저혈당으로 구별, 치료는 분만 + 보존 치료. 해리슨에 없는 것: AFLP 의 INR·섬유소원·요붕증·신손상, LCHAD 연관, Swansea 기준, HELLP 의 LDH 기준값·분열적혈구 서술, TTP 감별"
    verified: text
  - id: acg-2016
    org: "American College of Gastroenterology (Tran TT, Ahn J, Reau NS)"
    title: "ACG Clinical Guideline: Liver Disease and Pregnancy"
    kind: guideline
    year: 2016
    citation: "Am J Gastroenterol 2016;111(2):176-194"
    doi: "10.1038/ajg.2015.430"
    url: "https://doi.org/10.1038/ajg.2015.430"
    checked_at: 2026-09-25
    checked: "서지만(기억·문항 출처 인용 — 이 컨테이너는 PubMed·doi.org 를 막아 원문·PMID 를 확인하지 못했다). AFLP 의 응고장애·저혈당·신생아 LCHAD 검사, HELLP 의 LDH 기준 서술은 원문 미대조"
    verified: citation
  - id: chng-2002
    org: "Ch'ng CL, Morgan M, Hainsworth I, Kingham JG"
    title: "Prospective study of liver dysfunction in pregnancy in Southwest Wales"
    kind: other
    year: 2002
    citation: "Gut 2002;51(6):876-880"
    doi: "10.1136/gut.51.6.876"
    url: "https://doi.org/10.1136/gut.51.6.876"
    checked_at: 2026-09-25
    checked: "서지만(기억 — Swansea 기준의 출처. 원문·PMID 미확인)"
    verified: citation
diagram:
  title: "임신 3분기 간효소 상승 — 간부전인가, 용혈인가"
  nodes:
    - {id: start, kind: start, text: "3분기 구토·상복부 통증·황달, AST/ALT 상승"}
    - {id: itch, kind: decision, text: "심한 가려움이 주증상, 간부전 없음?"}
    - {id: icp, kind: end, text: "임신 담즙정체 — 담즙산 확인"}
    - {id: labs, kind: info, text: "혈당·INR·섬유소원·도말·LDH 확인"}
    - {id: synth, kind: decision, text: "저혈당·INR↑·섬유소원↓·뇌증?"}
    - {id: viral, kind: decision, text: "간염 혈청검사 양성?"}
    - {id: hep, kind: end, text: "급성 바이러스 간염"}
    - {id: aflp, kind: end, text: "급성 임신 지방간 → 안정 후 분만"}
    - {id: hemo, kind: decision, text: "분열적혈구·LDH↑·혈소판↓?"}
    - {id: hellp, kind: end, text: "HELLP 증후군 → 안정 후 분만"}
    - {id: other, kind: alert, text: "다른 원인 — 전자간증·담도 질환 재평가"}
  edges:
    - {from: start, to: itch}
    - {from: itch, to: icp, label: "예"}
    - {from: itch, to: labs, label: "아니오"}
    - {from: labs, to: synth}
    - {from: synth, to: viral, label: "간부전 있음"}
    - {from: synth, to: hemo, label: "간부전 없음"}
    - {from: viral, to: hep, label: "양성"}
    - {from: viral, to: aflp, label: "음성"}
    - {from: hemo, to: hellp, label: "있음"}
    - {from: hemo, to: other, label: "없음"}
diagram_notes:
  - "AFLP 와 HELLP 는 겹칠 수 있다 — 간부전과 용혈이 함께 있으면 둘 다 분만이 치료라 처치는 같고, AFLP 면 신생아 지방산 산화 검사를 더한다."
  - "HELLP 도 진행하면 파종혈관내응고로 INR·섬유소원이 나빠진다 — 간부전 갈래는 용혈이 약할 때의 판단이다."
  - "HELLP 의 약 15 % 는 고혈압이 없다고 알려져 있어 혈압이 낮다는 것만으로 배제하지 않는다(원문 미대조)."
  - "분열적혈구는 HELLP·TTP 모두에서 필요한 소견 — 없으면 둘 다 가능성이 낮아진다."
checks:
  - q: "임신 35주 간효소 상승 환자에서 AFLP 를 HELLP 와 가르는 검사 소견 세 가지는?"
    a: "저혈당, INR 연장·섬유소원 저하(응고인자 합성 저하), 빌리루빈·암모니아의 뚜렷한 상승 — 간 합성 기능 부전. HELLP 는 분열적혈구·LDH 상승(용혈)과 혈소판감소가 중심."
  - q: "AFLP 와 HELLP 의 치료는 어떻게 다른가?"
    a: "치료 원칙은 같다 — 모체 안정(포도당·혈장·혈액제제) 뒤 분만. AFLP 면 신생아 지방산 산화 결함(LCHAD) 검사와 재발 상담을 더한다."
  - q: "가려움이 심하고 담즙산이 오른 3분기 산모 — AFLP 인가?"
    a: "아니다. 임신 담즙정체다. 간부전을 만들지 않고, 우르소디올·태아 감시·37주까지 분만."
variants:
  - id: v1
    of: usmle-2026-0175
    flip: true
    changed: "혈압 138/86·요단백 미량·분열적혈구 없음·LDH 420·혈당 52·INR 1.9·섬유소원 110 을 혈압 168/110·요단백 3+·분열적혈구 있음·LDH 900·혈당·INR·섬유소원 정상으로 바꿈 → 간부전 없이 용혈+중증 전자간증이 중심이므로 답이 급성 임신 지방간에서 HELLP 증후군으로 바뀜"
    context: "단서를 바꿔 답이 바뀌는 변형 — 용혈과 중증 고혈압"
    stem: "A 31-year-old primigravid woman at 34 weeks' gestation comes to the emergency department because of epigastric and right upper quadrant pain and nausea for 1 day. She has had a mild headache since this morning. Her pregnancy had been uncomplicated, and her blood pressure was 118/74 mm Hg 2 weeks ago. Temperature is 36.9°C, pulse is 96/min, respirations are 18/min, and blood pressure is 168/110 mm Hg on two readings 15 minutes apart. She is alert and not jaundiced. There is right upper quadrant tenderness. The fetal heart rate is 145/min. Laboratory studies show hemoglobin 9.8 g/dL, leukocyte count 12,000/mm³, platelet count 72,000/mm³, AST 210 U/L, ALT 180 U/L, total bilirubin 1.6 mg/dL, glucose 94 mg/dL, INR 1.0, fibrinogen 420 mg/dL, creatinine 0.9 mg/dL, and LDH 900 U/L. Urine dipstick shows 3+ protein. A peripheral blood smear shows schistocytes. Which of the following is the most likely diagnosis?"
    choices: ["A. Acute fatty liver of pregnancy", "B. Intrahepatic cholestasis of pregnancy", "C. HELLP syndrome", "D. Acute viral hepatitis", "E. Thrombotic thrombocytopenic purpura"]
    answer: "C"
    explanation: "중증 범위 혈압(≥160/110)·단백뇨 3+ 의 전자간증 위에 분열적혈구·LDH 900(용혈), 혈소판 72,000, AST/ALT 상승이 겹쳤다 = HELLP 증후군. 혈당·INR·섬유소원이 정상이라 간 합성 기능은 보존돼 있어 AFLP 가 아니다. TTP 도 분열적혈구가 있지만 중증 고혈압·단백뇨와 3분기 간효소 상승의 조합은 HELLP 쪽이다. 원래 문항은 용혈이 없고 간부전이 앞섰다 — 간부전 대 용혈이 답을 바꾼다."
    kind: application
  - id: v2
    of: usmle-2026-0175
    flip: false
    changed: "나이·산과력(37세 경산부, 36주)·내원 경위(산전 진찰에서 식욕부진·구토로 의뢰)·증상 제시 순서와 보기 순서를 바꾸고, 저혈당·INR 연장·섬유소원 저하·분열적혈구 없음·경한 혈압은 그대로 → 답은 여전히 급성 임신 지방간"
    context: "겉모습만 바꾸고 답은 같은 변형 — 산전 진찰에서 의뢰된 경산부"
    stem: "A 37-year-old woman, gravida 3, para 2, at 36 weeks' gestation is referred from a routine prenatal visit because of 4 days of anorexia, nausea and vomiting. She reports drinking large amounts of water and waking at night to urinate. She has no itching, headache or visual changes. She takes no medications other than a prenatal vitamin. Temperature is 37.0°C, pulse is 100/min, respirations are 18/min, and blood pressure is 134/84 mm Hg. Her sclerae are icteric, and she is slow to answer questions but oriented. The abdomen is mildly tender in the right upper quadrant. The fetal heart rate is 140/min. Laboratory studies show platelet count 118,000/mm³, AST 260 U/L, ALT 240 U/L, total bilirubin 6.4 mg/dL, glucose 48 mg/dL, INR 2.0, fibrinogen 120 mg/dL, creatinine 1.6 mg/dL, and LDH 380 U/L. Urine dipstick shows trace protein. A peripheral blood smear shows no schistocytes. Serologic tests for hepatitis A, B and C are negative. Which of the following is the most likely diagnosis?"
    choices: ["A. Thrombotic thrombocytopenic purpura", "B. HELLP syndrome", "C. Acute viral hepatitis", "D. Acute fatty liver of pregnancy", "E. Intrahepatic cholestasis of pregnancy"]
    answer: "D"
    explanation: "환자의 나이·산과력·내원 경위는 바뀌었지만 결정적 단서 — 저혈당 48·INR 2.0·섬유소원 120·느린 반응(간부전), 다음다뇨(요붕증), 분열적혈구 없음·LDH 380(용혈 약함), 경한 혈압·미량 단백뇨, 간염 혈청검사 음성 — 은 그대로다. 간 합성 기능 부전이 앞서므로 여전히 급성 임신 지방간이다."
    kind: application
---

## 판단 — 왜 HELLP가 아니라 급성 임신 지방간인가
- 두 질환은 3분기·상복부 통증·간효소 상승·혈소판감소를 공유하므로 **공통 소견으로는 가르지 못한다**.
- 급성 임신 지방간(AFLP)은 **간세포 자체가 기능을 잃는** 병이다 — 저혈당, 빌리루빈·암모니아의 뚜렷한 상승이 해리슨이 드는 구별점이다 [[harrison-21: 479장 p.3767]]. INR 연장·섬유소원 저하·뇌증도 같은 간부전의 표현이다 [[?acg-2016]].
- HELLP 증후군(hemolysis, elevated liver enzymes, low platelets)은 **중증 전자간증의 특수 아형**이다 [[harrison-21: 479장 p.3763]] — 중심은 내피 손상에 따른 미세혈관병성 용혈과 혈소판 소모다.
- 그래서 「간부전이 앞서고 용혈·고혈압이 약하다」면 AFLP, 「용혈이 뚜렷하고 합성 기능이 남아 있다」면 HELLP 로 기운다.

## 기전 — 지방산 산화에서 간부전으로
정상 간은 공복에 글리코겐 분해·당신생으로 혈당을 지키고, 응고인자·섬유소원을 만들고, 암모니아를 요소로 바꾸고, 빌리루빈을 포합해 내보낸다. AFLP 에서는 간세포에 미세수포 지방이 쌓여 이 기능들이 한꺼번에 떨어진다 → 저혈당, INR 연장·섬유소원 저하, 암모니아 상승·뇌증, 고빌리루빈혈증 [[harrison-21: 479장 p.3767]]. 태아의 긴사슬 지방산 β산화 결함(LCHAD 결핍)이 있으면 태아·태반 쪽 지방산 대사물이 모체 간에 부담을 준다는 연관이 알려져 있다 [[?acg-2016]]. 갈증·다뇨(일과성 요붕증)와 급성 신손상이 동반될 수 있다 [[?acg-2016]].
HELLP 는 태반의 항혈관신생 인자 과잉과 내피 손상에서 시작한다 [[harrison-21: 479장 p.3763]] → 손상된 미세혈관을 지나는 적혈구가 깨지고(분열적혈구·LDH 상승) 혈소판이 소모되며, 간 문맥주위 괴사로 효소가 오른다. 응고장애는 진행된 합병증이다 [[harrison-21: 479장 p.3763]].

## 가르는 소견 — 간부전인가, 용혈인가
- **간부전 쪽**: 혈당, INR, 섬유소원, 암모니아, 의식. 임신 중 섬유소원은 원래 높아야 하므로 「정상 하한」도 이미 낮은 값이다.
- **용혈 쪽**: 말초혈액 도말의 분열적혈구, LDH, 혈소판. 분열적혈구가 없으면 HELLP·TTP 가 모두 멀어진다.
- **전자간증 쪽**: 중증 소견은 혈압 ≥ 160/110 mmHg, 혈소판 < 100 × 10⁹/L, 크레아티닌 > 1.1 mg/dL, 트랜스아미나제 정상의 2배 [[harrison-21: 479장 p.3763]]. 혈압이 낮다고 HELLP 를 배제하지는 않는다.
- 가려움 + 담즙산 상승이면 임신 담즙정체, 혈청검사 양성이면 바이러스 간염 — 표 참고.

## 처치 — 둘 다 안정 후 분만
- AFLP: 분만 + 보존 치료 [[harrison-21: 479장 p.3767]] — 포도당, 신선동결혈장·동결침전제제·혈소판 등으로 교정 [[?acg-2016]]. 산후 신생아 지방산 산화 결함 검사, 다음 임신 재발 상담 [[?acg-2016]].
- HELLP: 중증 전자간증에 준해 분만이 결정적 치료다 [[harrison-21: 479장 p.3763]].
- 재평가: 분만 뒤 혈당·INR·의식·신기능이 회복되는지 본다 — 회복이 늦으면 간이식 센터 논의가 필요할 수 있다 [[?acg-2016]].

## 권고와 예외
- 감별은 처치(분만)를 바꾸지 않는 경우가 많다 — 시험에서는 진단명을 묻고, 실제에서는 교정·분만을 미루지 않는다.
- HELLP 의 LDH 기준값(흔히 ≥ 600 U/L)과 Swansea 기준(6개 이상)은 원문을 대조하지 않았다(검토 항목) [[?acg-2016]] [[?chng-2002]].
- 임신 담즙정체의 분만 시기를 담즙산 수치로 세분하는 권고는 이 정리본에서 대조하지 않았다. 해리슨은 37주까지 분만으로 적는다 [[harrison-21: 479장 p.3767]].

## 시험 쟁점 — 충돌·맥락·새 근거
- **Z1 맥락 · AFLP 와 HELLP 는 겹치는 스펙트럼** — 시험 기준: 저혈당·빌리루빈·암모니아 상승(간부전)이 앞서면 AFLP [[harrison-21: 479장 p.3767]] / 다른 기준: 해리슨은 AFLP 를 HELLP·전자간증과 같은 스펙트럼에 두고, 응고장애를 전자간증의 말단장기 합병증으로도 적는다 [[harrison-21: 479장 p.3763]] / 왜 다른가: 두 질환이 한 환자에서 겹쳐 나타날 수 있어 응고장애 하나로는 가르지 못한다 / 시험에서는: KMLE · USMLE 모두 조합(간부전 + 용혈 약함 → AFLP, 용혈 + 중증 고혈압 → HELLP)으로 묻고, 치료는 둘 다 분만이라 답이 갈리지 않는다.
