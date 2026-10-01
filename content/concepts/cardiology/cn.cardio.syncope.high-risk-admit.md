---
id: cn.cardio.syncope.high-risk-admit
type: concept
topic: Cardiology
see_also: [Emergency Medicine, Neurology]
date: 2026-10-02
updated: 2026-10-02
version: 1
outline: h21            # 기본틀 슬롯(content/outline/subjects.yaml) — 해리슨 21판 21장 Syncope
confidence: low         # 출처 본문을 이 세션에서 대조하지 못했다(sources.checked)
review_status: unreviewed
note_form: 2            # 판형 2(2026-09-25) — 결론·시험 단서·왜 → 혼동 → 표·도식 → 목표에 맞춘 본문
title: "실신 — 고위험 소견이 입원을 정한다"
objective: "실신 첫 평가(병력·기립 혈압·12유도 심전도)에서 고위험 소견을 가려 입원·심장 정밀평가와 귀가를 고른다"
objective_kind: 다음 처치
condition: 실신(syncope) — 첫 평가와 위험 층화
exams: [kmle, usmle]
summary:
  - "결론: 고위험 소견이 하나라도 있으면 입원·심전도 감시·심장 평가, 반사성 저위험만 있으면 귀가."
  - "시험 단서: 운동 중·누운 채 실신, 전구 없는 실신, 구조 심질환, 심전도 이상 = 고위험 실신(high-risk syncope)."
  - "왜: 심장성 실신은 부정맥·유출로 폐쇄가 다시 오면 급사로 이어진다 — 반사성 실신은 예후가 좋다."
  - "모든 실신에 병력·진찰(기립 혈압)·12유도 심전도. 뇌 CT·뇌파·경동맥 초음파는 단서 없으면 하지 않는다."
  - "기립성 저혈압: 일어선 뒤 3분 안 수축기 ≥20 mmHg 또는 이완기 ≥10 mmHg 하강."
pitfalls:
  - contrast: "실신이면 뇌 CT·뇌파부터?"
    point: "실신은 뇌 전체의 일시적 관류 저하라 국소 신경학 결손·두부 외상이 없으면 뇌 영상·뇌파가 원인을 찾지 못한다. 먼저 할 것은 12유도 심전도와 기립 혈압이고, 위험을 가르는 것도 이 둘과 병력이다."
    exception: "국소 신경학 결손, 의식 회복 지연, 머리 외상이 있으면 그 이유로 영상을 찍는다."
    cites: ["?acc-aha-hrs-syncope-2017", "?esc-syncope-2018"]
  - contrast: "젊고 다시 멀쩡하면 반사성 실신?"
    point: "나이보다 상황이 먼저다. 운동 중 실신, 누운 자세의 실신, 두근거림 직후 실신, 젊은 나이 급사 가족력은 젊어도 고위험이다 — 비후성 심근병증·QT 연장·브루가다·WPW 같은 부정맥 기질을 심전도에서 찾는다."
    cites: ["?esc-syncope-2018", "?harrison-21"]
  - contrast: "경련 움직임이 있었으니 뇌전증 발작?"
    point: "실신에서도 뇌 저관류로 짧은 근간대 움직임이 생길 수 있다(경련성 실신). 몇 초로 짧고, 의식 회복이 빠르며 회복 뒤 혼동이 짧다. 혀 옆면 깨묾·길게 이어지는 발작 후 혼동은 발작 쪽이다."
    cites: ["?harrison-21"]
  - contrast: "전구 증상이 있으면 안전?"
    point: "전형적 반사성 전구(오래 서 있음·더위·통증·공포 뒤 어지럼·식은땀·구역)는 저위험이다. 전구가 없거나 몇 초 안 되는 실신은 구조 심질환·심전도 이상과 함께 있으면 고위험으로 본다."
    cites: ["?esc-syncope-2018"]
tables:
  - id: risk
    section: "가르는 소견 — 고위험과 저위험"
    title: "실신 첫 평가 — 위험을 가르는 소견"
    role: severity
    span: column
    columns: ["영역", "고위험(입원·심장 평가)", "저위험(반사성·기립성 쪽)"]
    rows:
      - ["상황", "운동 중, 누운 자세, 두근거림 직후, 새 흉통·호흡곤란·복통·두통 동반 [[?esc-syncope-2018]]", "오래 서 있음·덥고 붐빔·통증·공포, 기침·배뇨·배변, 식사 뒤, 일어설 때"]
      - ["병력", "구조 심질환·관상동맥질환(심부전·낮은 박출률·심근경색 과거), 젊은 나이 급사 가족력 [[?esc-syncope-2018]]", "같은 양상의 반복 실신이 오래, 심질환 없음"]
      - ["진찰", "설명 안 되는 수축기 <90 mmHg, 깨어 있는데 서맥 <40회/분, 새 수축기 잡음, 위장관 출혈 단서 [[?esc-syncope-2018]]", "정상(기립 혈압 하강은 기립성 쪽)"]
      - ["심전도", "급성 허혈, 모비츠 II·완전 방실차단, 심실빈맥, 3초 넘는 동정지, 브루가다 1형, 반복 QTc 연장, 각차단·병적 Q파 [[?esc-syncope-2018]]", "정상"]
  - id: disp
    section: "선택 — 입원·관찰·귀가"
    title: "위험군에 따른 다음 처치"
    role: treatment
    span: column
    columns: ["위험군", "다음 처치", "주의"]
    rows:
      - ["고위험 소견 하나 이상", "입원 또는 즉시 정밀평가 — 심전도 감시, 심초음파, 필요하면 운동부하·전기생리 검사 [[?esc-syncope-2018]] [[?acc-aha-hrs-syncope-2017]]", "원인 질환(출혈·폐색전·대동맥 박리·급성 관상증후군)이 보이면 그 치료가 먼저"]
      - ["저위험 소견만(반사성·기립성 전형)", "귀가 — 기전 설명, 유발 상황 피하기, 전구 때 눕기", "기립성이면 약물(이뇨제·혈관확장제)·탈수·출혈을 확인"]
      - ["어느 쪽도 아님", "응급실 관찰 또는 실신 클리닉에서 이어 평가 [[?esc-syncope-2018]]", "귀가시킬 때도 재발 시 다시 오도록 설명"]
criteria:
  - id: syn-initial
    name: 첫 평가
    kind: 검사 권고
    population: "실신으로 온 모든 환자"
    statement: "자세한 병력(목격자 포함), 기립 혈압을 포함한 진찰, 12유도 심전도를 시행한다 [[?acc-aha-hrs-syncope-2017]] [[?esc-syncope-2018]]"
    exceptions: "혈액검사·뇌 영상·뇌파·경동맥 초음파는 임상 단서가 있을 때만"
    source: acc-aha-hrs-syncope-2017
    basis: current
    exams: [kmle, usmle]
  - id: syn-highrisk
    name: 고위험 실신의 처치
    kind: 치료 기준
    population: "첫 평가에서 고위험 소견이 하나 이상인 실신"
    statement: "응급실에서 즉시 정밀평가하거나 입원해 심전도 감시·심장 평가를 한다 [[?esc-syncope-2018]]"
    exceptions: "원인이 분명한 중증 질환(출혈·폐색전 등)이면 그 질환의 처치를 따른다"
    source: esc-syncope-2018
    basis: current
    exams: [kmle, usmle]
  - id: syn-lowrisk
    name: 저위험 실신의 처치
    kind: 치료 기준
    population: "반사성·기립성 실신 전형 소견만 있는 실신"
    statement: "입원·추가 검사 없이 귀가시키고 기전과 유발 회피를 설명한다 [[?esc-syncope-2018]]"
    exceptions: "고위험 소견이 하나라도 섞이면 저위험으로 보지 않는다"
    source: esc-syncope-2018
    basis: current
    exams: [kmle, usmle]
  - id: syn-orthostatic
    name: 기립성 저혈압 정의
    kind: 진단 기준
    population: "누운 자세에서 일어선 성인"
    statement: "일어선 뒤 3분 안에 수축기 혈압 20 mmHg 이상 또는 이완기 혈압 10 mmHg 이상 떨어짐 [[?acc-aha-hrs-syncope-2017]]"
    exceptions: "정상이어도 반사성·심장성 실신을 배제하지 않는다. 지연형은 3분 뒤에 떨어진다"
    source: acc-aha-hrs-syncope-2017
    basis: current
    exams: [kmle, usmle]
sources:
  - id: harrison-21
    org: "McGraw Hill"
    title: "Harrison's Principles of Internal Medicine, 21st ed. — Chapter 21: Syncope"
    kind: textbook
    year: 2022
    citation: "Loscalzo J, Kasper DL, Longo DL, et al (eds). Harrison's Principles of Internal Medicine, 21e. 21장 Syncope, 인쇄쪽 152–158(장 범위 — harrison_toc.json)"
    checked_at: 2026-10-02
    checked: "본문 미대조 — 드라이브 장별 문서(1JXLPmz8ebxitfBzURdnyJvLi6u4Yx6FRaw9d3M3_7uM)는 있으나 이 세션에 Google Drive 커넥터가 없었고, 원본 PDF 도 컨테이너에 없어 harrison_read.py --slot h21 이 실패했다. 장 번호·제목·쪽 범위만 harrison_toc.json 에서 확인. 다음 PC 세션·루틴에서 그 장을 읽고 [[harrison-21: 21장 p.N]] 으로 바꾼다"
    verified: citation
  - id: esc-syncope-2018
    org: "European Society of Cardiology (ESC)"
    title: "2018 ESC Guidelines for the diagnosis and management of syncope"
    kind: guideline
    year: 2018
    citation: "Brignole M, et al. Eur Heart J 2018;39(21):1883–1948"
    doi: "10.1093/eurheartj/ehy037"
    url: "https://doi.org/10.1093/eurheartj/ehy037"
    checked_at: 2026-10-02
    checked: "서지만 — 서지·DOI 는 기억으로 적었다. 이 컨테이너가 doi.org·PubMed·Crossref 를 막아 서지 확인·권고 본문(위험 층화 표·처치 경로) 대조를 못 했고 PMID 도 확인하지 못해 적지 않았다(학습서 워크플로가 DOI 로 찾는다)"
    verified: citation
  - id: acc-aha-hrs-syncope-2017
    org: "ACC/AHA/HRS"
    title: "2017 ACC/AHA/HRS Guideline for the Evaluation and Management of Patients With Syncope"
    kind: guideline
    year: 2017
    citation: "Shen WK, et al. Circulation 2017;136(5):e60–e122"
    doi: "10.1161/CIR.0000000000000499"
    url: "https://doi.org/10.1161/CIR.0000000000000499"
    checked_at: 2026-10-02
    checked: "서지만 — 서지·DOI 는 기억으로 적었다. 이 컨테이너가 doi.org·PubMed·Crossref 를 막아 서지 확인·권고 본문(첫 평가·기립성 저혈압 정의·일상 검사 비권고) 대조를 못 했고 PMID 도 확인하지 못해 적지 않았다"
    verified: citation
diagram:
  title: "실신 — 첫 평가에서 입원·귀가까지"
  nodes:
    - {id: start, kind: start, text: "갑자기 의식을 잃고 저절로 빨리 회복"}
    - {id: tloc, kind: decision, text: "실신(뇌 전체 일시 저관류)인가?"}
    - {id: tlocask, kind: info, text: "목격자 병력·혈당·신경학 진찰 확보"}
    - {id: other, kind: alert, text: "실신 아님 — 발작·대사·외상 따로 평가"}
    - {id: eval, kind: step, text: "병력 · 기립 혈압 · 12유도 심전도"}
    - {id: risk, kind: decision, text: "고위험 소견(표)이 있는가?"}
    - {id: admit, kind: end, text: "입원 · 심전도 감시 · 심초음파 등 심장 평가"}
    - {id: home, kind: end, text: "귀가 — 기전 설명 · 유발 상황 피하기"}
    - {id: obs, kind: end, text: "응급실 관찰 또는 실신 클리닉 평가"}
  edges:
    - {from: start, to: tloc}
    - {from: tloc, to: eval, label: "예"}
    - {from: tloc, to: other, label: "아니오"}
    - {from: tloc, to: tlocask, label: "불확실"}
    - {from: tlocask, to: eval, label: "실신 쪽"}
    - {from: tlocask, to: other, label: "다른 원인"}
    - {from: eval, to: risk}
    - {from: risk, to: admit, label: "하나 이상"}
    - {from: risk, to: home, label: "저위험만"}
    - {from: risk, to: obs, label: "어느 쪽도 아님"}
diagram_notes:
  - "고위험 소견의 목록(상황·병력·진찰·심전도)은 표에 있다 — 하나만 있어도 고위험이다."
  - "출혈·폐색전·대동맥 박리·급성 관상증후군처럼 원인이 바로 보이면 위험 층화보다 그 질환의 처치가 먼저다."
  - "혈액검사·뇌 영상·뇌파·경동맥 초음파는 일상적으로 하지 않는다 — 국소 신경학 결손·외상·출혈 의심 같은 단서가 있을 때만."
  - "기립 혈압이 정상이어도 반사성·심장성 실신은 배제되지 않는다."
checks:
  - q: "실신 환자 모두에게 하는 첫 평가 세 가지는?"
    a: "목격자를 포함한 병력, 기립 혈압을 포함한 진찰, 12유도 심전도."
  - q: "28세 남자가 축구 경기 중 쓰러졌다가 곧 회복했다. 지금 증상이 없다. 귀가시키지 않는 이유는?"
    a: "운동 중 실신은 고위험 상황이다 — 비후성 심근병증·부정맥 같은 심장성 원인을 감시·심초음파로 찾을 때까지 귀가시키지 않는다."
  - q: "실신 뒤 몇 초간 팔다리가 떨렸다. 뇌전증으로 보고 뇌파부터 하는가?"
    a: "아니다. 뇌 저관류로도 짧은 근간대 움직임이 생긴다(경련성 실신). 회복이 빠르고 혼동이 짧으면 실신으로 평가한다."
variants:
  - id: v1
    flip: true
    changed: "오래 서 있다 전구 뒤 쓰러진 젊은 여성(저위험) → 누운 채 전구 없이 의식을 잃은 심근경색 과거 환자 ⇒ 정답이 귀가에서 입원·심장 평가로"
    context: "같은 목표, 단서를 바꿔 답이 바뀌는 변형 — 고위험 실신"
    stem: "68세 남자가 저녁에 소파에 누워 텔레비전을 보다가 아무 예고 없이 의식을 잃었고, 30초 뒤 저절로 깨어났다고 배우자가 데려왔다. 4년 전 심근경색으로 스텐트를 넣었다. 지금은 증상이 없다. 혈압 124/76 mmHg, 맥박 72회/분, 신경학적 진찰은 정상이고 혈당은 112 mg/dL 이다. 12유도 심전도에서 동율동, 하벽 유도의 병적 Q파가 보인다. 가장 적절한 처치는?"
    choices: ["A. 기립 경사 검사 예약 후 귀가", "B. 입원해 심전도 감시와 심초음파", "C. 뇌 CT 후 이상 없으면 귀가", "D. 뇌파 검사", "E. 경동맥 초음파"]
    answer: "B"
    explanation: "누운 자세에서 전구 없이 생긴 실신, 심근경색 과거(구조 심질환), 심전도의 병적 Q파는 모두 고위험 소견이다 — 반흔 관련 심실빈맥 같은 심장성 원인을 찾을 때까지 입원해 감시하고 심기능을 본다. 신경학적 결손이 없으므로 뇌 CT·뇌파·경동맥 초음파는 원인을 찾지 못하고, 기립 경사 검사는 반사성 실신이 의심될 때의 검사다."
    kind: application
figures_none: 위험 층화는 병력·혈압·심전도 소견 목록으로 판단한다 — 대표 영상 소견이 없다(심전도 이상은 각 부정맥 정리본에서 그림으로)
---

## 판단 — 왜 고위험 소견이 입원을 정하나
- 실신의 원인은 반사성(혈관미주신경성·상황성)이 가장 흔하고 예후가 좋다. 문제는 드문 **심장성 실신**(부정맥·대동맥판 협착·비후성 심근병증의 유출로 폐쇄)으로, 다음 발작이 급사일 수 있다 [[?harrison-21]].
- 그래서 첫 평가의 목적은 원인 확정이 아니라 **위험 층화**다 — 병력·기립 혈압·12유도 심전도만으로 고위험 소견을 찾는다 [[?esc-syncope-2018]].
- 고위험 소견이 하나라도 있으면 입원·심전도 감시·심장 평가, 반사성·기립성 전형만 있으면 귀가, 어느 쪽도 아니면 관찰한다(표).
- 뇌 영상·뇌파는 실신의 원인을 찾지 못한다 — 국소 신경학 결손·외상이 없으면 하지 않는다 [[?acc-aha-hrs-syncope-2017]].

## 기전 — 뇌 관류 저하에서 실신으로
의식은 뇌간 망상활성계와 양쪽 대뇌의 관류에 달려 있어, 뇌 전체 혈류가 몇 초만 끊겨도 의식을 잃는다. 뇌 관류압은 혈압이 정하고, 혈압은 심박출량 × 말초혈관저항이다 [[?harrison-21]].
- 반사성: 미주신경 항진(서맥)과 교감신경 철수(혈관 확장)가 함께 와서 혈압이 떨어진다 — 전구(어지럼·식은땀·구역)가 있고 눕히면 곧 회복된다.
- 기립성: 일어설 때 다리로 몰리는 피를 교감신경 반사가 보상하지 못한다(자율신경병증·약물·탈수·출혈).
- 심장성: 부정맥이나 고정된 유출로 폐쇄가 심박출량 자체를 떨어뜨린다 — 자세·전구와 상관없이, 운동이나 누운 자세에서도 온다. 그래서 「상황」이 원인을 가르는 단서가 된다.

## 가르는 소견 — 고위험과 저위험
- 같은 실신이라도 **언제·어떤 자세로·무엇과 함께** 쓰러졌는지가 기전을 가른다. 운동 중·누운 채·두근거림 직후는 심장성 쪽이다.
- 12유도 심전도가 정상이어도 간헐적 부정맥은 배제되지 않는다 — 고위험 상황·병력이 있으면 감시를 이어 간다.
- 기립 혈압 정상도 반사성·심장성 실신을 배제하지 않는다.

## 선택 — 입원·관찰·귀가
- 고위험이면 입원(또는 응급실 즉시 정밀평가)에서 심전도 감시와 심초음파로 구조 심질환·부정맥을 찾고, 필요하면 운동부하·전기생리 검사로 이어 간다 [[?esc-syncope-2018]].
- 원인 질환이 바로 보이면(위장관 출혈·폐색전·대동맥 박리·급성 관상증후군) 그 처치가 먼저다.
- 저위험 귀가 때는 기전을 설명하고 유발 상황을 피하며, 전구가 오면 눕거나 앉게 한다. 기립성이면 원인 약물·탈수를 고친다.

## 권고와 예외
- 위험 층화 점수(샌프란시스코 실신 규칙·캐나다 실신 위험 점수 등)는 임상 판단을 보조할 뿐 단독으로 입원을 정하지 않는다 — 이 정리본에서 원문은 대조하지 않았다(검토 항목).
- 고위험 소견 목록의 세부(심전도 기준·수치)는 ESC 2018 위험 층화 표 기준으로 적었으나 원문 대조 전이다(검토 항목).
- 해리슨 21장과의 대조가 남았다 — 다음 세션에서 그 장을 읽고 인쇄쪽을 단다(검토 항목).
