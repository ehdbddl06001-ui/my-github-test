---
id: cn.peds.stec-hus.supportive-no-antibiotics
type: concept
topic: Pediatrics
see_also: [Nephrology, Infectious Disease]
date: 2026-09-23
updated: 2026-09-23
version: 1
outline: peds.renal      # 기본틀 슬롯(content/outline/subjects.yaml) — 해리슨 대조 대상 아님(손 슬롯)
confidence: medium
review_status: unreviewed
title: "소아 STEC 용혈요독증후군 — 시가독소의 혈관 손상에서 지지치료·항생제 회피까지"
objective: "시가독소가 신장 미세혈관 내피를 손상해 혈전성 미세혈관병증을 만드는 기전으로 혈성 설사 뒤의 용혈·혈소판감소·급성 신손상을 설명하고, 전형적 소아 STEC-HUS 의 치료로 수액·전해질·투석 중심의 지지치료를 고르며 항생제·지사제·예방적 혈소판 수혈·혈장교환을 피하는 이유와 TTP·비전형 HUS 와의 경계를 판단한다"
objective_kind: 치료
condition: 시가독소 생성 대장균 용혈요독증후군(STEC-HUS)
exams: [usmle, kmle]
summary:
  - "시가독소 생성 대장균(O157:H7 등)은 덜 익힌 간 쇠고기·생채소로 들어와 3–4일 잠복 뒤 대장에 붙어 복통과 설사를 일으키고, 설사는 흔히 육안적 혈변으로 바뀐다. 열은 대개 없다 [[harrison-21: 161장 p.1268]]."
  - "대장에서 흡수된 시가독소가 혈류를 타고(적혈구가 운반) 신장·뇌의 작은 혈관 내피에 붙는다. 독소 A 소단위가 리보솜을 멈춰 내피가 손상되고 혈전성 미세혈관병증이 생긴다 [[harrison-21: 161장 p.1268]]."
  - "그 결과가 설사 2–14일 뒤의 삼징 — 분열적혈구가 있는 용혈성 빈혈·혈소판감소·급성 신손상(때로 뇌병증)이다. 10세 미만 감염 아동의 약 15% 에서 생기고, 미국 소아 HUS 의 90% 가 STEC 때문이다 [[harrison-21: 161장 p.1268]]."
  - "치료는 지지치료다 — 수액·전해질·혈압 관리, 필요하면 투석. 항생제는 독소 생산·방출을 늘려 HUS 위험을 높일 수 있어 피한다 [[harrison-21: 161장 p.1270]]. 지사제도 피한다 [[?tarr-2005]]."
  - "혈장교환은 STEC-HUS 에 이득이 없고, 에쿨리주맙(C5 억제)의 가치는 정해지지 않았다 [[harrison-21: 161장 p.1270]] — 혈장교환은 ADAMTS13 결핍 TTP 의 치료다 [[?isth-ttp-2020]]."
pitfalls:
  - contrast: "「혈전성 미세혈관병증 = 혈장교환」 vs 설사 선행 소아 STEC-HUS"
    point: "분열적혈구·혈소판감소·장기 손상은 TTP 와 HUS 가 공유하는 결과일 뿐 원인이 다르다. TTP 는 ADAMTS13 결핍으로 초거대 폰빌레브란트 인자가 쌓인 것이라 혈장교환으로 효소를 채우고 자가항체를 걷어 낸다. STEC-HUS 는 시가독소의 내피 손상이라 혈장에 보충할 것이 없고, 혈장교환은 이득이 없다 [[harrison-21: 161장 p.1270]]. 설사 선행·시가독소 확인·소아·신손상 우세가 STEC-HUS 쪽이다."
    exception: "설사 선행이 없거나 가족력·재발이 있으면 비전형(보체) HUS, 성인·신경 증상 우세·ADAMTS13 현저 저하면 TTP 를 생각한다 [[?isth-ttp-2020]]."
    cites: ["harrison-21", "?isth-ttp-2020"]
    covers: ["usmle-2026-0030:D"]
  - contrast: "「세균 감염 = 항생제로 빨리 없앤다」"
    point: "STEC 장염은 대개 5–10일에 저절로 낫는다. 항생제는 세균이 죽거나 스트레스를 받을 때 시가독소 생산·방출을 늘려 HUS 위험을 높일 수 있다 — 그래서 열 없는 혈성 설사에서는 원인균이 확인되기 전에도 항생제를 피한다 [[harrison-21: 161장 p.1268, p.1270]]."
    cites: ["harrison-21", "?wong-2000"]
  - contrast: "혈소판 3–4만인데 예방적 수혈?"
    point: "혈소판은 미세혈전에 소모되어 낮다. 출혈이 없으면 수혈로 얻는 것이 적고 미세혈전을 더할 수 있다는 우려가 있어, 활동성 출혈이나 시술 때로 제한한다(원문 미대조 — 검토 항목) [[?tarr-2005]]."
criteria:
  - id: stec-abx
    name: 항생제 회피
    kind: 치료 기준
    population: "STEC 감염이 의심되거나 확인된 설사(열 없는 혈성 설사)"
    statement: "항생제를 쓰지 않는다 — HUS 발생을 늘릴 수 있다(시가독소 생산·방출 증가 추정) [[harrison-21: 161장 p.1270]]"
    exceptions: "소아 코호트에서 항생제와 HUS 위험 증가의 연관을 보고한 연구가 근거로 인용된다 — 원문 미대조 [[?wong-2000]] · 메타분석 [[?freedman-2016]]"
    source: harrison-21
    basis: current
    exams: [usmle, kmle]
  - id: hus-plasma
    name: HUS 에서 혈장교환
    kind: 치료 기준
    population: "STEC-HUS"
    statement: "혈장교환은 이득이 없다. 에쿨리주맙의 가치는 정해지지 않았다 [[harrison-21: 161장 p.1270]]"
    exceptions: "TTP(ADAMTS13 결핍)는 혈장교환이 치료의 축이다 [[?isth-ttp-2020]]"
    source: harrison-21
    basis: current
    exams: [usmle, kmle]
  - id: stec-test
    name: 진단 검사
    kind: 검사 기준
    population: "지역사회 획득 설사"
    statement: "CDC 는 모든 지역사회 획득 설사에서 배양(분리주 확보)과 시가독소(또는 유전자) 검출을 함께 하도록 권한다 — 혈변·분변 백혈구가 늘 있지는 않아서다. O157 은 소르비톨 비발효로 선별한다 [[harrison-21: 161장 p.1269]]"
    exceptions: "비 O157 STEC 는 선택 배지가 없어 독소 검출이 필요하다 [[harrison-21: 161장 p.1269]]"
    source: harrison-21
    basis: current
    exams: [usmle, kmle]
sources:
  - id: harrison-21
    org: "McGraw Hill"
    title: "Harrison's Principles of Internal Medicine, 21st ed. — Chapter 161: Diseases Caused by Gram-Negative Enteric Bacilli"
    kind: textbook
    year: 2022
    citation: "Loscalzo J, Kasper DL, Longo DL, et al (eds). Harrison's Principles of Internal Medicine, 21e. 161장 p.1268–1270 (Shiga toxin–producing E. coli)"
    checked_at: 2026-09-23
    checked: "본문 대조(드라이브 161장 문서) — p.1268: 덜 익힌 간 쇠고기·생채소 유행, 시가독소(Stx2 가 HUS 에 더 중요) A 소단위가 28S rRNA 를 잘라 단백 합성 억제, 3–4일 잠복, 비혈성 설사 → 육안적 혈변, 복통·분변 백혈구 흔하고 열은 드묾, 5–10일 자기 제한, HUS 는 설사 2–14일 뒤·10세 미만 감염 아동의 약 15%·미국 소아 HUS 의 90%, 적혈구가 독소를 신장·뇌 소혈관 내피로 운반해 혈전성 미세혈관병증 → 용혈성 빈혈·혈소판감소·신부전·뇌병증 · p.1269: CDC 는 모든 지역사회 설사에 배양+시가독소 검출 권고, O157 은 소르비톨 비발효 · p.1270: STEC 항생제는 HUS 를 늘릴 수 있어 피함, HUS 에 혈장교환 이득 없음, 에쿨리주맙 가치 미정. 지사제·혈소판 수혈·수액 요법 세부는 이 장에 없다. 슬롯 peds.renal 은 해리슨 대조 대상이 아닌 손 슬롯이나 근거로 이 장을 읽었다"
    verified: text
  - id: tarr-2005
    org: "Tarr PI, Gordon CA, Chandler WL (종설)"
    title: "Shiga-toxin-producing Escherichia coli and haemolytic uraemic syndrome"
    kind: review
    year: 2005
    citation: "Lancet 2005;365(9464):1073-1086"
    doi: "10.1016/S0140-6736(05)71144-2"
    url: "https://doi.org/10.1016/S0140-6736(05)71144-2"
    checked_at: 2026-09-23
    checked: "서지만 — 이 컨테이너에서 doi·PubMed 접근 차단으로 지사제 회피·혈소판 수혈 제한 서술을 원문과 대조하지 못했다"
    verified: citation
  - id: wong-2000
    org: "Wong CS, Jelacic S, Habeeb RL, et al (전향 코호트)"
    title: "The risk of the hemolytic-uremic syndrome after antibiotic treatment of Escherichia coli O157:H7 infections"
    kind: other
    year: 2000
    citation: "N Engl J Med 2000;342(26):1930-1936"
    doi: "10.1056/NEJM200006293422601"
    url: "https://doi.org/10.1056/NEJM200006293422601"
    checked_at: 2026-09-23
    checked: "서지만 — 원문·초록 접근 차단(수치 인용하지 않음)"
    verified: citation
  - id: freedman-2016
    org: "Freedman SB, Xie J, Neufeld MS, et al (체계적 문헌고찰·메타분석)"
    title: "Shiga toxin-producing Escherichia coli infection, antibiotics, and risk of developing hemolytic uremic syndrome: a meta-analysis"
    kind: review
    year: 2016
    citation: "Clin Infect Dis 2016;62(10):1251-1258"
    doi: "10.1093/cid/ciw099"
    url: "https://doi.org/10.1093/cid/ciw099"
    checked_at: 2026-09-23
    checked: "서지만 — 원문·초록 접근 차단(수치 인용하지 않음)"
    verified: citation
  - id: isth-ttp-2020
    org: "International Society on Thrombosis and Haemostasis"
    title: "ISTH guideline for treatment of thrombotic thrombocytopenic purpura"
    kind: guideline
    year: 2020
    citation: "Zheng XL, et al. J Thromb Haemost 2020;18(10):2496-2502"
    doi: "10.1111/jth.15010"
    url: "https://doi.org/10.1111/jth.15010"
    checked_at: 2026-09-23
    checked: "서지만 — 원문 접근 차단. 서지 세부(권·쪽·doi)도 원문으로 확인하지 못했다 — 검토 항목"
    verified: citation
diagram:
  title: "혈성 설사 뒤 창백·핍뇨 — 전형적 STEC-HUS 인가, 치료는 무엇인가"
  nodes:
    - {id: start, kind: start, text: "혈성 설사 며칠 뒤 창백·기면·소변 감소"}
    - {id: tma, kind: decision, text: "분열적혈구 용혈성 빈혈 + 혈소판감소 + 급성 신손상이 있는가?"}
    - {id: labs, kind: info, text: "혈구·말초혈액 도말(분열적혈구)·LDH·크레아티닌·전해질을 확인한다"}
    - {id: enteritis, kind: alert, text: "아직 HUS 아님 — 설사 지지치료, 항생제·지사제 피하고 2주간 혈구·신기능 감시(이 도식 범위 밖)"}
    - {id: cause, kind: decision, text: "설사가 선행했고 시가독소 생성균이 확인되었나?"}
    - {id: ttp, kind: alert, text: "설사 선행 없음·신경 증상 우세·ADAMTS13 현저 저하 — TTP: 혈장교환(이 도식 범위 밖)"}
    - {id: ahus, kind: alert, text: "설사 선행 없음·가족력·재발 — 비전형(보체) HUS: 에쿨리주맙 고려(이 도식 범위 밖)"}
    - {id: support, kind: end, text: "전형적 STEC-HUS — 수액·전해질·혈압 관리, 적응 시 투석 · 항생제·지사제·예방적 혈소판 수혈·혈장교환은 하지 않는다"}
  edges:
    - {from: start, to: tma}
    - {from: tma, to: cause, label: "셋 다 있음"}
    - {from: tma, to: enteritis, label: "없음"}
    - {from: tma, to: labs, label: "검사 전"}
    - {from: labs, to: cause, label: "셋 다 있으면"}
    - {from: labs, to: enteritis, label: "없으면"}
    - {from: cause, to: support, label: "예(소아·혈성 설사 선행)"}
    - {from: cause, to: ttp, label: "성인·신경 증상·ADAMTS13 저하"}
    - {from: cause, to: ahus, label: "설사 없음·가족력·재발"}
diagram_notes:
  - "열 없는 혈성 설사는 그 자체로 STEC 를 의심할 단서다 — 원인균이 확인되기 전에도 항생제를 삼간다 [[harrison-21: 161장 p.1270]]."
  - "HUS 는 설사가 좋아질 무렵(2–14일 뒤) 온다. 설사가 멎었다고 끝이 아니다 [[harrison-21: 161장 p.1268]]."
  - "재평가: 소변량·크레아티닌·칼륨·혈압·혈색소·혈소판을 매일, 의식 변화(뇌병증)를 본다. 무뇨·조절 안 되는 전해질·체액 과다는 투석 적응이다(세부 기준 원문 미대조)."
checks:
  - q: "STEC 장염에서 항생제를 피하는 이유는?"
    a: "항생제가 시가독소 생산·방출을 늘려 HUS 위험을 높일 수 있기 때문이다. 장염 자체는 5–10일에 저절로 낫는다."
  - q: "STEC-HUS 에서 혈장교환이 1차가 아닌 이유는?"
    a: "원인이 시가독소의 내피 손상이라 혈장으로 보충하거나 제거할 대상(TTP 의 ADAMTS13·자가항체)이 없다. 해리슨은 이득이 없다고 적는다."
  - q: "HUS 의 삼징과 그것이 생기는 자리는?"
    a: "분열적혈구 용혈성 빈혈·혈소판감소·급성 신손상. 시가독소가 신장(과 뇌)의 작은 혈관 내피를 손상해 미세혈전이 생기고, 적혈구가 그 사이를 지나며 부서지고 혈소판이 소모된다."
variants:
  - id: v1
    of: usmle-2026-0030
    flip: true
    changed: "4세·덜 익힌 햄버거 뒤 혈성 설사 선행·시가독소 생성균 확인·크레아티닌 3배 → 38세 여성·설사 선행 없음·혼돈과 말더듬·크레아티닌 경미 상승·ADAMTS13 활성 <10% ⇒ 정답이 지지치료에서 즉시 혈장교환으로"
    context: "단서를 바꿔 답이 바뀌는 변형 — 설사 없는 성인의 혈전성 미세혈관병증"
    stem: "A 38-year-old woman is brought to the emergency department with 2 days of fatigue, headache, and episodes of confusion and slurred speech that resolve within minutes. She has had no diarrhea, vomiting, or recent travel, and takes no medications. Temperature is 37.9 C. There are scattered petechiae on the legs. Hemoglobin is 7.8 g/dL with many schistocytes on the peripheral smear, platelet count is 12,000/microL, LDH is markedly elevated, and creatinine is 1.3 mg/dL. Stool studies are negative for Shiga toxin. ADAMTS13 activity is below 10%. Which of the following is the most appropriate management?"
    choices: ["A. Empiric antibiotics directed at enteric pathogens", "B. Loperamide with oral rehydration", "C. Platelet transfusion to a target above 50,000/microL", "D. Urgent plasma exchange", "E. Supportive care with fluids and electrolytes alone"]
    answer: "D"
    explanation: "The changed clues are the absence of preceding diarrhea or Shiga toxin, an adult patient, fluctuating neurologic deficits with only mild renal injury, and severely reduced ADAMTS13 activity — thrombotic thrombocytopenic purpura. Plasma exchange replaces the deficient enzyme and removes the inhibiting autoantibody and is the urgent first step [[?isth-ttp-2020]]. In typical pediatric STEC-HUS, by contrast, plasma exchange offers no benefit and care is supportive [[harrison-21: 161장 p.1270]]. Supportive care alone would miss a rapidly fatal disorder, antibiotics and loperamide have no role, and platelet transfusion is avoided unless there is life-threatening bleeding."
    kind: application
  - id: v2
    of: usmle-2026-0030
    flip: false
    changed: "나이·성별(7세 남아)·노출원(체험 농장 방문)·제시 순서(핍뇨 먼저 알아챔)를 바꾸고, 혈성 설사 선행·분열적혈구·혈소판감소·급성 신손상·시가독소 확인은 유지 ⇒ 답은 그대로 지지치료"
    context: "겉모습만 바꾸고 답은 같은 변형 — 체험 농장 방문 뒤"
    stem: "A 7-year-old boy is brought to the pediatrician because his parents noticed he has barely urinated in the past day. One week ago, after a class trip to a petting farm, he developed abdominal cramps and diarrhea that became bloody on the third day; the diarrhea has now nearly resolved. He has had no fever. He appears pale and puffy around the eyes. Blood pressure is 118/76 mm Hg. Hemoglobin is 7.9 g/dL with fragmented red cells on the smear, platelet count is 52,000/microL, and creatinine is 2.4 mg/dL (baseline 0.5 mg/dL). A stool assay is positive for Shiga toxin. Which of the following is the most appropriate management?"
    choices: ["A. Oral azithromycin to eradicate the organism", "B. Plasma exchange started later today", "C. Supportive fluid and electrolyte care, dialysis if needed", "D. Prophylactic platelet transfusion before any procedure", "E. Loperamide to control the residual diarrhea"]
    answer: "C"
    explanation: "The deciding clues are unchanged: bloody diarrhea without fever preceding a triad of microangiopathic hemolysis, thrombocytopenia, and acute kidney injury in a child, with Shiga toxin confirmed [[harrison-21: 161장 p.1268]]. Management is supportive — fluids, electrolytes, blood pressure control, and dialysis when indicated. Antibiotics may increase the risk of HUS and plasma exchange has shown no benefit [[harrison-21: 161장 p.1270]]; antimotility agents and prophylactic platelet transfusion are avoided [[?tarr-2005]]."
    kind: application
---

## 정의
용혈요독증후군(HUS)은 분열적혈구가 있는 용혈성 빈혈·혈소판감소·급성 신손상을 특징으로 하는 혈전성 미세혈관병증이다. 소아 HUS 의 대부분(미국 90%)은 시가독소 생성 대장균(STEC, 대표 O157:H7)의 장염 뒤에 오는 **전형적 HUS** 다 [[harrison-21: 161장 p.1268]].

## 병태생리
- **감염**: 덜 익힌 간 쇠고기·생채소·동물 접촉으로 들어온 STEC 가 3–4일 잠복 뒤 대장에 붙는다. 처음에는 물설사, 곧 육안적 혈변이 되고 복통이 심하며 열은 드물다 [[harrison-21: 161장 p.1268]].
- **독소**: 시가독소(특히 Stx2)는 B 소단위로 글로보실 세라마이드를 가진 세포에 붙고, A 소단위가 28S rRNA 를 잘라 단백 합성을 멈춘다 [[harrison-21: 161장 p.1268]].
- **전신화**: 장에서 흡수된 독소가 적혈구에 실려 신장·뇌 소혈관 내피로 간다. 내피가 손상되면 그 자리에 혈소판·피브린 미세혈전이 생긴다 [[harrison-21: 161장 p.1268]].

## 기전에서 소견으로
- 미세혈전 사이를 지나는 적혈구가 찢김 → **분열적혈구**, LDH 상승, 용혈성 빈혈(창백).
- 미세혈전에 혈소판 소모 → **혈소판감소**(출혈은 대개 경미).
- 사구체 모세혈관 폐쇄 → **급성 신손상**(핍뇨·부종·고혈압·고칼륨).
- 뇌 소혈관 → 기면·경련 같은 뇌병증.
- 시점: 설사 2–14일 뒤, 설사가 나아질 무렵 [[harrison-21: 161장 p.1268]].

## 감별
- **TTP**: ADAMTS13 결핍, 대개 성인, 신경 증상 우세, 신손상은 상대적으로 가벼움 → 혈장교환 [[?isth-ttp-2020]].
- **비전형(보체 매개) HUS**: 설사 선행 없음, 가족력·재발 → 보체 억제제.
- **파종혈관내응고**: PT·aPTT 연장, 피브리노겐 감소(패혈증) — HUS 는 응고 검사가 대개 정상에 가깝다(원문 미대조).
- 열 없는 혈성 설사는 장중첩·염증성 장질환으로 오인되기 쉽다 [[harrison-21: 161장 p.1268]].

## 검사
혈구·말초 도말(분열적혈구), LDH·간접 빌리루빈·합토글로빈, 크레아티닌·전해질, 소변검사. 대변 배양과 시가독소(또는 유전자) 검출을 함께 한다 [[harrison-21: 161장 p.1269]].

## 치료
- **지지치료가 전부다** — 체액량·전해질(특히 칼륨)·혈압 관리, 영양, 적응이 되면 투석.
- **피할 것**: 항생제(HUS 위험 증가) [[harrison-21: 161장 p.1270]], 지사제(로페라마이드) [[?tarr-2005]], 예방적 혈소판 수혈(활동성 출혈·시술 때만), 혈장교환(이득 없음) [[harrison-21: 161장 p.1270]].
- 재평가: 소변량·크레아티닌·칼륨·혈압·혈색소·혈소판·의식. 신기능 회복 뒤에도 단백뇨·고혈압을 추적한다(장기 추적 기간은 원문 미대조).

## 권고와 예외
- 2011 독일 유행의 ST-EAEC(O104:H4)는 성인, 특히 젊은 여성에서 HUS 가 많았다 — 「HUS = 소아」가 절대 규칙은 아니다 [[harrison-21: 161장 p.1268]].
- 에쿨리주맙의 STEC-HUS 에서의 가치는 정해지지 않았다 [[harrison-21: 161장 p.1270]] — 중증 신경 침범 등에서 쓰이는 사례는 이 정리본에서 대조하지 않았다.

## 시험 쟁점 — 충돌·맥락·새 근거
- **Z1 새 근거 · STEC-HUS 에 에쿨리주맙** — 시험 기준: 전형적 STEC-HUS 는 지지치료, 보체 억제제는 비전형 HUS 의 약 / 다른 기준: 해리슨은 STEC-HUS 에서 C5 억제(에쿨리주맙)의 가치가 「정해지지 않았다」고 적는다 [[harrison-21: 161장 p.1270]] / 왜 다른가: 유행 때 중증 환자에 쓰인 관찰 자료가 있으나 대조 시험 근거가 부족하다(관찰 자료 원문 미대조) / 시험에서는: USMLE · 전형적 소아 STEC-HUS 의 답은 지지치료, 에쿨리주맙은 설사 없는 비전형 HUS · KMLE 도 같은 흐름.

## (심화) 「하지 말 것」 네 가지가 보기로 나오는 이유
이 문항의 오답 넷(항생제·지사제·예방적 혈소판·혈장교환)은 모두 「무언가를 적극적으로 하는」 선택이다. 각각 독소 방출 증가, 독소의 장 체류 증가, 미세혈전 우려, 원인이 다른 질환(TTP)의 치료라는 서로 다른 이유로 빠진다 — 지지치료가 답인 것은 「할 게 없어서」가 아니라 넷을 각각 배제했기 때문이다.
