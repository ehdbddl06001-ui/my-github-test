---
id: cn.cardio.long-qt-syndrome.first-line-drug
type: concept
topic: Cardiology
see_also: [Pediatrics, Emergency Medicine]
date: 2026-09-21
updated: 2026-09-29
version: 4
outline: h255            # 기본틀 슬롯(content/outline/subjects.yaml)
confidence: medium
review_status: unreviewed
note_form: 2            # 판형 2(2026-09-25) — 결론·시험 단서·왜 → 혼동 → 표·도식 → 목표에 맞춘 본문
title: "선천 QT연장증후군 — 1차 약은 비선택 베타차단제"
objective: "심실 재분극의 생리로 QT 연장이 토르사드 드 푸앵트로 이어지는 기전을 설명하고, 후천 원인을 걸러 선천 QT연장증후군을 진단한 뒤 비선택 베타차단제를 1차로 고르고 QT 연장 약물을 피해야 하는 이유를 판단한다"
objective_kind: 치료
condition: 선천 QT연장증후군
exams: [kmle, usmle]
summary:
  - "결론: 후천 원인이 없는 선천 QT연장증후군의 1차 약은 증상과 무관하게 비선택 베타차단제(나돌롤·프로프라놀롤)."
  - "시험 단서: 운동·수영·소리 중 전조 없는 실신 + 젊은 급사 가족력 + 반복 QTc ≥480 ms = 선천 QT연장증후군(long QT syndrome)."
  - "왜: 교감 자극 때 재분극을 줄일 IKs 가 없어(LQT1) 토르사드가 난다 — 그 방아쇠를 끊는 약이 먼저다."
  - "쓰지 않는 약: 소탈롤·아미오다론·IA군(IKr 차단 → QT 더 연장), 칼슘통로차단제(기전 무관)."
  - "심정지 생존자는 ICD, 약물 중 재발은 LCSD·ICD, LQT3 는 메실레틴 추가 — 첫 진단에서 ICD 부터 넣지 않는다."
pitfalls:
  - contrast: "「심실빈맥 예방 = 아미오다론·소탈롤」 vs QT연장증후군"
    point: "Ⅲ군 항부정맥제는 IKr 을 막아 재분극을 더 늘린다. 다른 심실빈맥에서는 예방약이지만 QT연장증후군에서는 토르사드를 부르는 약이다. 소탈롤이 베타차단 작용을 가져도 IKr 차단 때문에 쓰지 않는다."
    exception: "베타차단제 자체는 QT 를 늘리지 않는다 — 나돌롤·프로프라놀롤처럼 비선택 약제를 고른다."
    cites: ["?esc-va-2022", "?aha-va-2017"]
    covers: ["kmle-2026-1035:B", "kmle-2026-1035:C"]
  - contrast: "플레카이니드·메실레틴(Na⁺ 통로 차단제)의 자리"
    point: "late Na⁺ 전류 억제는 SCN5A 기능획득(LQT3)에서만 기전적으로 맞는다. 운동·수영 유발형(LQT1)에는 근거가 없고, IC군은 구조 심질환·허혈에서 부정맥을 유발할 수 있다. 메실레틴도 LQT3 에서 베타차단제에 더하는 약이지 대체약이 아니다."
    cites: ["?esc-va-2022"]
    covers: ["kmle-2026-1035:D"]
  - contrast: "칼슘통로차단제로 「빈맥을 막는다」?"
    point: "딜티아젬·베라파밀은 방실결절 전도를 늦춰 상심실성 빈맥의 심실 반응을 조절할 뿐, 재분극 연장과 조기후탈분극을 막지 못한다. QT연장증후군의 부정맥은 방실결절과 무관하다."
    cites: ["?esc-va-2022"]
    covers: ["kmle-2026-1035:E"]
  - contrast: "선택적 β1 차단제(메토프롤롤·아테놀롤)로 대신하기"
    point: "LQT1·LQT2 에서 메토프롤롤은 나돌롤·프로프라놀롤보다 증상 재발(돌파 사건)이 많았다는 관찰 자료가 있어, 지침은 비선택 약제를 우선한다. 「베타차단제면 아무거나」가 아니다."
    cites: ["?chockalingam-2012", "?esc-va-2022"]
  - contrast: "증상이 없고 QTc 가 정상인 유전자 양성 가족"
    point: "베타차단제는 QT 연장이 기록된 환자에서 1차 권고이고, 유전자 양성이지만 QTc 가 정상인 사람에게는 「고려」로 한 단계 낮다. 다만 QT 연장 약물 회피·전해질 관리·유발 상황 교육은 모두에게 한다."
    cites: ["?esc-va-2022"]
criteria:
  - id: lqts-dx-esc
    name: 진단(ESC 2022)
    kind: 진단 기준
    population: "2차 원인이 없는 환자"
    statement: "반복 측정한 12유도 심전도에서 QTc ≥480 ms(증상 유무 무관) 또는 LQTS 진단 점수 >3 이면 진단한다. QTc 460–479 ms 에 원인 불명의 부정맥성 실신이 있으면 진단을 고려한다"
    exceptions: "약물·전해질·서맥 등 후천 원인이 있으면 먼저 교정한 뒤 판단한다. 쪽·권고표 번호는 본문 미대조"
    source: esc-va-2022
    locator: "LQTS 권고표(본문 미대조 — 루틴 컨테이너에서 접근 차단)"
    basis: current
    exams: [kmle, usmle]
  - id: lqts-bb-esc
    name: 1차 약물(ESC 2022)
    kind: 치료 기준
    population: "QT 연장이 기록된 LQTS 환자"
    statement: "비선택 베타차단제(나돌롤 또는 프로프라놀롤)를 권고한다(Class I). 유전자 양성이지만 QTc 가 정상이면 베타차단제를 고려한다(Class IIa)"
    exceptions: "천식 등 금기·불내성이면 좌심장 교감신경 절제술을 대안으로. 쪽 번호 미대조"
    source: esc-va-2022
    locator: "LQTS 권고표(본문 미대조)"
    basis: current
    exams: [kmle, usmle]
  - id: lqts-bb-aha
    name: 1차 약물(AHA/ACC/HRS 2017)
    kind: 치료 기준
    population: "LQTS 환자(증상 유무 무관)"
    statement: "베타차단제를 권고한다(Class I). 심정지 생존자·최적 베타차단제 중 실신 반복은 ICD, 베타차단제 불내성·실패는 LCSD 를 권고"
    exceptions: "약제 이름(나돌롤 우선)은 ESC 가 더 구체적이다. 쪽 번호 미대조"
    source: aha-va-2017
    locator: "선천 LQTS 절 권고표(본문 미대조)"
    basis: current
    exams: [kmle, usmle]
sources:
  - id: harrison-21
    org: "McGraw Hill"
    title: "Harrison's Principles of Internal Medicine, 21st ed. — Chapter 255: Polymorphic Ventricular Tachycardia and Ventricular Fibrillation"
    kind: textbook
    year: 2022
    citation: "Loscalzo J, Kasper DL, Longo DL, et al (eds). Harrison's Principles of Internal Medicine, 21e. 255장 p.1923–1926"
    checked_at: 2026-09-21
    checked: "본문 대조(드라이브 PDF, 255장 p.1925) — LQT1/LQT2 에서 비선택 베타차단제(나돌롤·프로프라놀롤)를 선호한다는 서술, LQT1 은 운동(특히 수영)·LQT2 는 소리·감정·LQT3 는 수면 중 발생, 위험 표지(QTc >500 ms·여성·실신/심정지 병력), 베타차단제에도 실신이 반복되면 ICD 고려, 유전자 양성이며 QTc 정상인 사람을 포함해 QT 연장 약물 회피가 필수라는 서술을 확인했다"
    verified: text
  - id: esc-va-2022
    org: "European Society of Cardiology"
    title: "2022 ESC Guidelines for the management of patients with ventricular arrhythmias and the prevention of sudden cardiac death"
    kind: guideline
    year: 2022
    citation: "Zeppenfeld K, Tfelt-Hansen J, de Riva M, et al. Eur Heart J 2022;43(40):3997–4126"
    doi: "10.1093/eurheartj/ehac262"
    pmid: "36017572"
    checked_at: 2026-09-21
    checked: "서지만 — 루틴 컨테이너의 네트워크 정책이 PubMed·OUP 접근을 막아 권고 본문·쪽수를 대조하지 못했다. LQTS 진단 기준·나돌롤/프로프라놀롤 Class I·메실레틴(LQT3)·LCSD·ICD 서술은 기억에 근거하며 사람 대조가 필요하다"
    verified: citation
  - id: aha-va-2017
    org: "American Heart Association / American College of Cardiology / Heart Rhythm Society"
    title: "2017 AHA/ACC/HRS Guideline for Management of Patients With Ventricular Arrhythmias and the Prevention of Sudden Cardiac Death"
    kind: guideline
    year: 2018
    citation: "Al-Khatib SM, Stevenson WG, Ackerman MJ, et al. Circulation 2018;138(13):e272–e391"
    doi: "10.1161/CIR.0000000000000549"
    pmid: "29084731"
    checked_at: 2026-09-21
    checked: "서지만 — ahajournals.org 접근 차단으로 권고 본문 미대조"
    verified: citation
  - id: schwartz-2013
    org: "European Heart Journal"
    title: "The long QT syndrome: a transatlantic clinical approach to diagnosis and therapy"
    kind: review
    year: 2013
    citation: "Schwartz PJ, Ackerman MJ. Eur Heart J 2013;34(40):3109–3116"
    doi: "10.1093/eurheartj/eht089"
    pmid: "23509228"
    checked_at: 2026-09-21
    checked: "서지만 — 진단 점수(Schwartz score) 항목·배점은 기억에 근거, 원문 표 미대조"
    verified: citation
  - id: chockalingam-2012
    org: "Journal of the American College of Cardiology"
    title: "Not all beta-blockers are equal in the management of long QT syndrome types 1 and 2: higher recurrence of events under metoprolol"
    kind: other
    year: 2012
    citation: "Chockalingam P, Crotti L, Girardengo G, et al. J Am Coll Cardiol 2012;60(20):2092–2099"
    doi: "10.1016/j.jacc.2012.07.046"
    pmid: "23083782"
    pmcid: "PMC3515779"
    checked_at: 2026-09-21
    checked: "초록 대조(PubMed, PMID 23083782) — LQT1/LQT2 382명(프로프라놀롤 134·메토프롤롤 147·나돌롤 101)에서 증상이 있던 환자의 돌파 사건이 메토프롤롤군에서 많았고(교정 오즈비 3.95, 95% CI 1.2–13.1, p=0.025), 프로프라놀롤과 나돌롤은 동등했다. 본문·표는 보지 못했다"
    verified: abstract
tables:
  - id: genotypes
    section: "기전 — 재분극 예비력에서 토르사드까지"
    title: "주요 유전형 — 통로·유발 상황·치료의 특징"
    role: comparison
    span: full
    columns: ["유형(유전자)", "이온 전류 변화", "전형적 유발 상황", "심전도 T파", "치료의 특징", "근거"]
    rows:
      - ["LQT1 (KCNQ1)", "IKs 기능 소실 — 교감신경 자극 때 재분극을 단축시키는 예비 전류가 없다", "운동, 특히 수영·다이빙", "기저가 넓은 T파", "베타차단제 효과가 가장 크다. 경쟁 수영은 제한", "[[?esc-va-2022]] [[?schwartz-2013]]"]
      - ["LQT2 (KCNH2/hERG)", "IKr 기능 소실 — 약물성 QT 연장과 같은 통로", "갑작스러운 소리(알람·전화), 감정, 산후", "낮고 갈라진(notched) T파", "베타차단제 + 칼륨 유지(저칼륨 회피). 산후 9개월까지 위험", "[[?esc-va-2022]] [[?schwartz-2013]]"]
      - ["LQT3 (SCN5A)", "late Na⁺ 전류 기능 획득 — 고평부가 길어진다", "수면·안정, 서맥", "긴 등전위 ST 뒤 늦은 T파", "베타차단제에 메실레틴을 더한다(late INa 억제). 서맥 의존이라 심박 유지가 중요", "[[?esc-va-2022]]"]
    note: "세 유형이 전체의 대부분을 차지한다. 유전형은 유발 상황·치료 추가를 정하지만, 1차 약물이 베타차단제라는 점은 공통이다 [[?esc-va-2022]]."
  - id: acquired
    section: "가르는 소견 — 후천 원인과 QTc 측정"
    title: "QT 연장의 후천 원인"
    role: differential
    span: column
    columns: ["원인 갈래", "대표 예", "확인 방법"]
    rows:
      - ["약물(IKr 차단)", "Ⅲ군·IA군 항부정맥제, 마크롤라이드·플루오로퀴놀론, 항정신병약·삼환계·온단세트론·메타돈", "복용력, crediblemeds 목록"]
      - ["전해질", "저칼륨·저마그네슘·저칼슘", "혈청 전해질"]
      - ["서맥·전도 장애", "완전 방실차단, 심한 동서맥", "심전도 리듬"]
      - ["구조·대사", "심근경색·심근병증, 갑상샘저하증, 저체온, 뇌출혈", "심초음파·TSH·병력"]
    note: "후천 원인이 있으면 「원인 교정」이 치료이며, 급성 토르사드에는 정맥 마그네슘·심박 올리기(임시 조율·이소프로테레놀)를 쓴다 — 선천형의 만성 치료(베타차단제)와 구분한다 [[?esc-va-2022]]."
  - id: score
    section: "가르는 소견 — 후천 원인과 QTc 측정"
    title: "LQTS 진단 점수(Schwartz) — 주요 항목"
    role: criteria
    span: column
    columns: ["항목", "점수"]
    rows:
      - ["QTc ≥480 ms / 460–479 / 450–459(남)", "3 / 2 / 1"]
      - ["운동 부하 회복 4분에 QTc ≥480 ms", "1"]
      - ["토르사드 드 푸앵트 기록(실신과 중복 불가)", "2"]
      - ["T파 교대(alternans) / 3유도 이상 갈라진 T파", "1 / 1"]
      - ["스트레스 중 실신 / 스트레스 없는 실신", "2 / 1"]
      - ["가족 중 확진 LQTS / 30세 미만 원인 불명 급사", "1 / 0.5"]
    note: "합계 ≥3.5 이면 높은 확률. 항목·배점은 2011 개정판 기억에 근거하며 원문 표 미대조(†) [[?schwartz-2013]]."
  - id: treatment
    section: "선택 — 단계별로 무엇을 더하나"
    title: "선천 LQTS 치료 — 적응과 한계"
    role: treatment
    span: full
    columns: ["치료", "적응", "기전·목적", "한계·주의", "근거"]
    rows:
      - ["비선택 베타차단제(나돌롤·프로프라놀롤)", "QT 연장이 기록된 모든 환자(증상 무관). 유전자 양성·QTc 정상은 고려", "교감신경 자극에 의한 재분극 이질성·EAD 억제. LQT1 에서 효과 최대", "선택적 β1 차단제는 돌파 사건이 더 많았다. 천식·서맥에서 불내성 가능", "[[?esc-va-2022]] [[?aha-va-2017]] [[chockalingam-2012]]"]
      - ["QT 연장 약물 회피·전해질 관리·유발 상황 교육", "모든 환자·가족", "재분극 예비력을 더 깎지 않는다", "설사·구토 뒤 저칼륨, 새 처방 때마다 목록 확인", "[[?esc-va-2022]]"]
      - ["메실레틴", "LQT3 에서 베타차단제에 추가", "late Na⁺ 전류 억제로 QT 단축", "LQT1·LQT2 에는 근거 없음", "[[?esc-va-2022]]"]
      - ["좌심장 교감신경 절제술(LCSD)", "베타차단제 불내성·금기, 또는 베타차단제 중 실신 반복·ICD 거부·ICD 다발 쇼크", "심장으로 가는 교감신경 입력 차단", "수술 합병증(호너 증후군 등), 완전 예방은 아님", "[[?esc-va-2022]] [[?aha-va-2017]]"]
      - ["ICD (+베타차단제)", "심정지 생존자. 최적 약물 중에도 실신·토르사드 반복이면 고려", "치명적 부정맥의 종료", "부적절 쇼크·젊은 환자의 장기 합병증 — 첫 진단에서 ICD 부터 넣지 않는다", "[[?esc-va-2022]] [[?aha-va-2017]]"]
    note: "QTc >500 ms, 심정지·실신 병력, 여성(사춘기 이후), 유전형이 위험도를 정하며, 위험도가 치료 강도(약물 → LCSD·ICD)를 결정한다 [[?esc-va-2022]]."
diagram:
  title: "운동 중 실신 + QT 연장 — 후천 원인 배제에서 1차 약까지"
  nodes:
    - {id: start, kind: start, text: "운동·감정 유발 실신 → 반복 12유도 심전도 QTc"}
    - {id: acq, kind: decision, text: "후천 원인(QT 약·저K·저Mg·서맥)?"}
    - {id: info, kind: info, text: "복용력·전해질·TSH·심초음파 확인"}
    - {id: fix, kind: step, text: "원인 교정(약 중단·전해질 보충) 뒤 QTc 재측정"}
    - {id: dx, kind: decision, text: "QTc ≥480 ms 반복 또는 점수 >3?"}
    - {id: other, kind: end, text: "기준 미달 — 신경심장성 실신·간질 등 평가"}
    - {id: lqts, kind: step, text: "선천 LQTS — 유전자·가족 선별, QT 약 회피"}
    - {id: bb, kind: step, text: "1차: 비선택 베타차단제(나돌롤·프로프라놀롤)"}
    - {id: risk, kind: decision, text: "심정지 병력, 또는 약물 중 재발?"}
    - {id: icd, kind: end, text: "ICD(+베타차단제) — 심정지 생존자"}
    - {id: esc, kind: end, text: "강화 — LCSD, ICD 고려, LQT3 면 메실레틴"}
    - {id: follow, kind: end, text: "베타차단제 유지 · QTc·증상 정기 추적"}
  edges:
    - {from: start, to: acq}
    - {from: acq, to: fix, label: "있음"}
    - {from: acq, to: dx, label: "없음"}
    - {from: acq, to: info, label: "확인 전"}
    - {from: info, to: dx}
    - {from: fix, to: dx}
    - {from: dx, to: lqts, label: "충족"}
    - {from: dx, to: other, label: "미달"}
    - {from: lqts, to: bb}
    - {from: bb, to: risk}
    - {from: risk, to: icd, label: "심정지 병력"}
    - {from: risk, to: esc, label: "약물 중 재발"}
    - {from: risk, to: follow, label: "없음"}
diagram_notes:
  - "후천 원인에는 갑상샘저하·심근 질환도 있다(후천 원인 표). QTc 460–479 ms 에 원인 불명의 부정맥성 실신이 있으면 진단을 고려한다."
  - "선천 LQTS 로 진단되면 유전자 검사·가족 선별과 함께 전해질 관리·유발 상황 교육을 하고, 새 처방 때마다 QT 연장 약물을 확인한다."
  - "「원인 교정 뒤 재측정」에서도 QTc 가 길게 남으면 선천형이 약물로 드러난 것일 수 있다(특히 LQT2) — 후천 원인이 있다고 선천형을 지우지 않는다."
  - "유전자 양성이지만 QTc 가 정상이고 증상이 없는 가족은 베타차단제가 「고려」 수준이며, 회피·교육은 동일하게 한다."
  - "급성 토르사드 발작 중의 처치(정맥 마그네슘·심박 올리기)는 이 도식 밖이다 — 이 도식은 재발 예방(만성 치료)을 다룬다."
  - "권고 등급·문구는 지침 본문과 미대조(†)이므로 사람 검토 뒤 reviewed 로 바꾼다."
checks:
  - q: "LQT1 환자가 운동 중에 유독 부정맥이 나는 이유와, 그것이 베타차단제 선택과 어떻게 이어지는가?"
    a: "교감신경 자극 때 심박이 빨라지면 재분극을 짧게 만드는 IKs 가 필요한데, LQT1 은 그 통로가 기능을 잃어 QT 가 오히려 길어지고 재분극 이질성이 커진다. 교감신경 입력을 막는 비선택 베타차단제가 그 방아쇠를 없앤다."
  - q: "베타차단 작용이 있는 소탈롤을 QT연장증후군에 쓰면 안 되는 이유는?"
    a: "소탈롤은 IKr 도 차단해 재분극을 더 늘린다(Ⅲ군). 베타차단 효과보다 QT 연장·토르사드 유발 위험이 앞선다."
  - q: "선천 LQTS 로 진단된 16세, 심정지 병력 없음. 첫 치료로 ICD 를 넣지 않는 이유는?"
    a: "1차는 베타차단제이고, ICD 는 심정지 생존자 또는 최적 약물 중 실신·토르사드 재발에서 고려한다. 젊은 환자는 부적절 쇼크·장기 합병증 부담이 크다."
variants:
  - id: v1
    context: "같은 목표, 다른 맥락 — 베타차단제 복용 중 심정지"
    stem: "20세 남자가 축구 경기 중 쓰러져 목격자 심폐소생술과 자동제세동기 1회 쇼크 뒤 회복돼 응급실에 왔다. 3년 전 선천 QT연장증후군으로 진단받아 나돌롤을 규칙적으로 복용하고 있다. 혈압 118/72 mmHg, 맥박 58회/분, 호흡 16회/분, 체온 36.8 ℃. 심전도는 동리듬에 QTc 520 ms 이고 칼륨·마그네슘은 정상, 심초음파는 정상이다. 재발 예방을 위해 가장 적절한 것은?"
    choices: ["A. 나돌롤 증량 후 경과 관찰", "B. 삽입형 제세동기 삽입", "C. 아미오다론 추가", "D. 메실레틴 추가", "E. 딜티아젬 추가"]
    answer: "B"
    explanation: "베타차단제를 잘 복용하던 중 심정지가 왔으므로 약물 최적화 단계를 넘어섰다. 심정지 생존자는 ICD 적응이며 베타차단제는 유지한다. 아미오다론은 QT 를 더 늘리고, 메실레틴은 LQT3 보조약이며 운동 유발형에 근거가 없고, 딜티아젬은 기전과 무관하다."
    kind: application
  - id: v2
    of: kmle-2026-1035
    flip: true
    changed: "유발 상황을 수영에서 수면 중으로, T파를 긴 등전위 ST 뒤 늦게 나오는 모양으로 바꾸고 SCN5A 변이·베타차단제 복용 중 재발을 더함 → LQT3 이므로 답이 「베타차단제 시작」에서 「메실레틴 추가」로 바뀜"
    context: "단서를 바꿔 답이 바뀌는 변형 — 수면 중 사건, LQT3"
    stem: "19세 남자가 밤에 자다가 숨을 헐떡이며 몸이 굳는 것을 가족이 두 번 목격해 왔다. 두 번 모두 1분 안에 저절로 깨어났다. 1년 전 선천 QT연장증후군으로 진단받아 프로프라놀롤을 빠짐없이 복용하고 있다. 혈압 116/70 mmHg, 맥박 52회/분. 심전도는 동서맥에 QTc 530 ms 이며 등전위 ST 분절이 길게 이어진 뒤 늦게 나타나는 T파가 보인다. 칼륨·마그네슘·TSH 는 정상이고 심초음파는 정상, 유전자 검사에서 SCN5A 기능획득 변이가 확인되었다. 심정지 병력은 없다. 다음 치료로 가장 적절한 것은?"
    choices: ["A. 메실레틴 추가", "B. 아미오다론 추가", "C. 프로프라놀롤을 소탈롤로 교체", "D. 딜티아젬 추가", "E. 프로프라놀롤 중단"]
    answer: "A"
    explanation: "수면·서맥 중 사건, 늦게 나오는 T파, SCN5A 기능획득 변이는 LQT3 다. 탈분극 뒤에도 새는 late Na⁺ 전류가 고평부를 늘리므로, 이를 막는 메실레틴을 베타차단제에 더하는 것이 기전에 맞는다 [[?esc-va-2022]]. 베타차단제는 끊지 않는다. 아미오다론·소탈롤은 IKr 을 막아 QT 를 더 늘리고, 딜티아젬은 방실결절 약이라 재분극과 무관하다. 원래 문항(수영 중 실신·넓은 T파 = LQT1 양상, 치료 전)에서는 메실레틴이 아니라 베타차단제 시작이 먼저였다."
    kind: application
  - id: v3
    of: kmle-2026-1035
    flip: false
    changed: "나이·성별(14세 남자)·유발 상황(달리기 중)·가족력(형의 급사)·제시 순서를 바꾸고 QTc 연장·후천 원인 없음·치료 전 상태는 그대로 → 답은 여전히 비선택 베타차단제"
    context: "겉모습만 바꾸고 답은 같은 변형 — 운동 중 실신한 남학생"
    stem: "14세 남자가 체육 시간에 달리기를 하다 전조 없이 쓰러져 30초쯤 뒤 스스로 깨어났다. 1년 전에도 축구 중 비슷한 일이 있었다. 형이 17세에 운동 중 급사했다. 복용 약물은 없고 신경학적 진찰은 정상이다. 혈압 112/70 mmHg, 맥박 66회/분. 심초음파는 구조 정상이며 칼륨·마그네슘·칼슘·TSH 도 정상이다. 반복한 12유도 심전도에서 QTc 는 500 ms, 505 ms 이고 기저가 넓은 T파가 보인다. 재발 예방을 위해 시작할 약물로 가장 적절한 것은?"
    choices: ["A. 나돌롤", "B. 아미오다론", "C. 소탈롤", "D. 메실레틴", "E. 베라파밀"]
    answer: "A"
    explanation: "운동 중 전조 없는 반복 실신, 젊은 가족의 급사, 후천 원인이 없는 상태에서 반복 QTc ≥480 ms 는 선천 QT연장증후군이고 넓은 T파·운동 유발은 LQT1 양상이다. 나이·성별·운동 종류가 달라져도 결정 단서(QT 연장 + 교감신경 유발 + 치료 전)가 같으므로 1차는 비선택 베타차단제(나돌롤)다 [[?esc-va-2022]]. 아미오다론·소탈롤은 QT 를 더 늘리고, 메실레틴은 LQT3 에서 베타차단제에 더하는 약이며, 베라파밀은 방실결절 약이라 토르사드를 막지 못한다."
    kind: application
figures:
- id: f1
  file: docs/assets/figures/ptbxl-00320.png
  kind: ecg
  at: 가르는 소견 — 후천 원인과 QTc 측정
  shows: QT 연장 — 느린 동리듬에서 늦게 끝나는 T파
  look_for:
  - QRS 시작에서 T파 끝까지를 RR 간격과 견준다(심박수 약 55회/분이라 보정 필요)
  - T파 끝이 가장 분명한 유도(대개 II·V5)에서 잰다
  label: long QT-interval (SCP LNGQT, 가능도 100)
  label_basis: dataset_expert
  reference: 심장내과 전문의의 SCP-ECG 판독을 두 번째 전문의가 검증 — 해당 진술의 가능도 100 인 기록만
  paper: Wagner P 외. PTB-XL, a large publicly available electrocardiography dataset. Sci Data 2020;7:154
  doi: 10.1038/s41597-020-0495-6
  credit: PTB-XL ECG dataset v1.0.3 (PhysioNet, CC BY 4.0) · record 320
  license: Creative Commons Attribution 4.0 International
  url: https://physionet.org/content/ptb-xl/1.0.3/records500/00000/#files-panel
  asset: PTBXL-00320
  paper_cited_by: 1213
---

## 판단 — 왜 비선택 베타차단제가 먼저인가
- 부정맥의 방아쇠는 교감신경 자극이다 — 운동·감정으로 심박이 오를 때 재분극이 충분히 짧아지지 못해 토르사드가 난다. 그 입력을 막는 비선택 베타차단제가 QT 연장이 기록된 환자의 1차 약이다(증상 유무 무관) [[harrison-21: 255장 p.1925]] [[?esc-va-2022]].
- 「베타차단제면 아무거나」가 아니다 — LQT1·LQT2 에서 메토프롤롤은 나돌롤·프로프라놀롤보다 돌파 사건이 많았다 [[chockalingam-2012]].
- 다른 심실빈맥의 예방약(Ⅲ군·IA군)은 IKr 을 막아 재분극 예비력을 더 깎는다 — 이 질환에서는 토르사드를 부르는 약이다.
- 치료 강도는 위험도(심정지·실신 병력, QTc >500 ms, 사춘기 이후 여성, 유전형)가 올린다. 첫 진단·무증상에서 ICD 부터 넣지 않는다.

## 기전 — 재분극 예비력에서 토르사드까지
QT 간격은 심실 탈분극 시작(Q)부터 재분극 끝(T파 끝)까지 — 심실 활동전위 길이의 표면 지표다. 고평부(2기)는 들어오는 L형 칼슘 전류와 나가는 지연 정류 칼륨 전류(IKr·IKs)의 균형이고, IKr 과 IKs 는 서로를 보완한다 — 하나가 약해져도 다른 하나가 재분극을 끝내는 **재분극 예비력(repolarization reserve)**. 선천 QT연장증후군(LQTS)은 이 예비력이 이온 통로 유전자 변이로 깎인 상태다.
- 재분극이 길어지면 고평부 동안 L형 칼슘 통로가 다시 열려 **조기후탈분극(EAD)** 이 생긴다. 심근 층마다 활동전위 길이가 달라 이질성이 커진 상태에서 EAD 가 조기 박동을 일으키면 QRS 축이 꼬이듯 바뀌는 다형 심실빈맥 — **토르사드 드 푸앵트(torsades de pointes)** 가 된다.
- 대부분 수 초 만에 멈춰 「전조 없이 쓰러졌다 곧 깨어남」(부정맥성 실신)이 되고, 멈추지 않으면 심실세동 → 급사. 경련·실금이 동반돼 간질로 오인되지만 뇌파는 정상이고 QT 가 답을 준다.
- 유전형마다 깎이는 길이 달라 유발 상황과 추가 약이 다르다(유전형 표). LQT1 의 IKs 는 교감 자극(β → cAMP → PKA)으로 커져 빠른 심박에서 활동전위를 줄이는 전류라, 없으면 운동 — 특히 찬물에 얼굴이 닿는 수영 — 이 방아쇠가 되고 베타차단제가 가장 잘 듣는다 [[?esc-va-2022]] [[?schwartz-2013]]. LQT2 는 저칼륨이 IKr 을 더 줄여 칼륨 유지가 치료의 일부, LQT3 는 서맥일수록 고평부가 길어져 수면 중 사건이 난다.

## 가르는 소견 — 후천 원인과 QTc 측정
- **후천 원인을 먼저 거른다**(후천 원인 표): 약물·전해질·서맥·갑상샘저하·심근 질환이 같은 통로를 눌러 QT 를 늘리고, 그때 치료는 원인 제거다. 급성 토르사드 발작의 정맥 마그네슘·심박 올리기(임시 조율·이소프로테레놀)는 선천형의 만성 예방(베타차단제)과 반대 방향의 개입이다 [[?esc-va-2022]].
- 원인을 고친 뒤에도 QTc 가 길게 남으면 선천형이 약물로 드러난 것일 수 있다(특히 LQT2) — 후천 원인이 있다고 선천형을 지우지 않는다.
- **QTc 재기**: 심박으로 보정한다(Bazett: QT/√RR). II·V5 에서 T파 끝을 접선법으로 정하고 U파는 넣지 않는다. 성인 참고 상한은 남 450 ms·여 460 ms 근처, 500 ms 를 넘으면 위험이 뚜렷이 오른다. Bazett 은 빈맥에서 과보정하므로 심박 100 을 넘으면 다른 공식이나 안정 후 재측정 [[?esc-va-2022]].
- **진단**: 2차 원인이 없을 때 반복 QTc ≥480 ms 또는 진단 점수 >3(점수표). 점수는 진단 확률 도구이지 위험도 도구가 아니다 [[?schwartz-2013]]. 운동 부하 회복 4분 QTc ≥480 ms 는 점수 항목이다.
- **음성·정상의 한계**: 변이 보인자의 일부는 QTc 가 정상이라 한 번의 정상값이 선천형을 지우지 못한다 — 반복 측정·가족 심전도. 24시간 심전도·심초음파가 정상이어도, 유전자 검사(KCNQ1·KCNH2·SCN5A)가 음성이어도 임상 진단을 지우지 않는다 [[?esc-va-2022]].
- T파 모양은 유전형을 암시한다 — 기저가 넓은 T파(LQT1), 낮고 갈라진 T파(LQT2), 긴 등전위 ST 뒤 늦은 T파(LQT3) [[?schwartz-2013]].
- 실신의 상황이 단서다 — 운동·감정·소리·수면 중이면 부정맥성, 오래 선 뒤 어지럼·창백을 거치면 신경심장성, 전조 오라·혀 깨묾·긴 혼돈기면 간질 쪽. 구조 심질환(비후심근병증·부정맥유발성 심근병증)은 심초음파로 낮춘다.

## 선택 — 단계별로 무엇을 더하나
치료의 축은 「교감신경 방아쇠를 끊고, 재분극 예비력을 더 깎지 않는 것」(치료 표).
- **1차 — 비선택 베타차단제**: 나돌롤은 반감기가 길어 하루 1~2회로 혈중 농도가 고르다. 서맥·피로·천식 악화를 감시하고, 복용 중단이 사건의 흔한 계기임을 교육한다 [[?esc-va-2022]].
- **모든 환자**: QT 연장 약물 회피(새 처방마다 crediblemeds 목록), 구토·설사 뒤 칼륨 보충, 유발 상황 관리(LQT1 경쟁 수영 제한, LQT2 침실의 알람·전화 소리 줄이기).
- **금기 약**: 소탈롤·아미오다론·IA군(퀴니딘·프로카인아마이드·디소피라미드)은 IKr 을 막아 QT 를 늘린다. 플레카이니드는 LQT3 외에는 자리가 없고, 칼슘통로차단제는 방실결절 약이라 기전과 무관하다.
- **추가·강화**: LQT3 는 메실레틴 추가. 베타차단제 불내성·금기, 약물 중 실신 반복, ICD 거부·다발 쇼크는 LCSD. 심정지 생존자는 ICD 권고, 최적 약물에도 실신·토르사드 재발이면 ICD 고려 — 젊은 환자는 부적절 쇼크·장기 합병증 부담이 크다 [[?esc-va-2022]] [[?aha-va-2017]].
- **재평가**: 시작 뒤 심박 감소·순응도·QTc·실신 재발을 정기 추적하고, 재발이 있으면 「약물 실패」로 보고 LCSD·ICD 단계로 넘어간다.

## 권고와 예외
- 베타차단제는 QT 연장이 **기록된** 환자에서 Class I, 유전자 양성이지만 QTc 가 정상이면 한 단계 낮은 「고려」다. 다만 QT 연장 약물 회피는 유전자 양성·QTc 정상인 사람에게도 그대로 적용된다 [[harrison-21: 255장 p.1925]] [[?esc-va-2022]].
- 위험 인자(QTc >500 ms, 실신·심정지 병력, 사춘기 이후 여성, LQT2·LQT3, 산후)가 겹칠수록 치료 강도를 올린다. 2022 ESC 는 유전형·QTc·성별을 합친 위험 계산기를 제안한다 [[?esc-va-2022]].
- 임신·산후(특히 LQT2)는 베타차단제를 유지한다 — 중단이 사건을 부른다.
- 한국 약제 급여 기준(나돌롤 공급 상황 포함)은 대조하지 않았다.

## (심화) 유전형별 특성과 스포츠
- LQT1 은 사건의 대부분이 운동 중이고 베타차단제 반응이 가장 좋다. LQT2 는 소리·감정·산후, LQT3 는 수면·서맥이며 베타차단제 효과가 상대적으로 낮아 메실레틴을 더한다.
- 경쟁 스포츠는 과거 일괄 금지였으나, 최근 지침은 적절한 베타차단제·감시 아래 개별 판단으로 바뀌었다. 자동제세동기 접근과 동반자, 수영 제한(LQT1)은 유지된다 [[?esc-va-2022]].
- 청각 장애를 동반한 상염색체 열성형(Jervell–Lange-Nielsen)은 KCNQ1 양측 변이로 표현형이 심해 조기 강화 치료가 필요하다.
