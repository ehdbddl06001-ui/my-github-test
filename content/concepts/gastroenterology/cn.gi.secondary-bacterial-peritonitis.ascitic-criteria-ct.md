---
id: cn.gi.secondary-bacterial-peritonitis.ascitic-criteria-ct
type: concept
topic: Gastroenterology
see_also: [General Surgery, Infectious Disease]
date: 2026-11-24
updated: 2026-11-25
version: 1
outline: h344            # 기본틀 슬롯 — 해리슨 21판 344장 → 22판 355장 Cirrhosis and Its Complications
roots_none: "복수 검사 수치 기준(이차성 복막염 기준)으로 다음 검사를 고르는 진단 경로 — 지침 수치 기준이다"
confidence: medium
review_status: unreviewed
note_form: 2
title: "간경변 복막염 — 복수가 이차성을 말하면 바로 CT"
objective: "간경변 복수 환자의 세균 복막염에서 복수 총단백·포도당·LDH·여러 균으로 이차성 복막염을 의심하고, 천공·농양을 찾는 복부 CT 를 즉시 고른다"
objective_kind: 검사 선택
condition: 간경변 환자의 이차성 세균 복막염(secondary bacterial peritonitis)
exams: [kmle, usmle]
summary:
  - "결론: 복수 호중구 > 250/μL 에 이차성 기준이 겹치면 자발성으로 치료만 하지 말고 즉시 복부 조영증강 CT 로 천공·농양을 찾는다."
  - "시험 단서: 간경변 복수 + 열·복통, 복수 총단백 > 1 g/dL · 포도당 < 50 mg/dL · LDH > 혈청 상한, 여러 균(polymicrobial)."
  - "왜: 자발성 세균 복막염은 장내 세균이 넘어와 생긴 한 균 감염이라 단백이 낮다 — 장 내용물이 새면 여러 균과 염증 산물이 쌓인다."
  - "놓치면 수술이 늦는다: 이차성은 항생제만으로 낫지 않고 원인(천공·농양)을 고쳐야 한다."
pitfalls:
  - contrast: "복수가 탁하고 단백이 높다 = 암성 복수, 세포진부터?"
    point: "호중구 4,800/μL 의 열·복통은 세균 복막염이다. 이차성 기준(단백 > 1 g/dL · 포도당 < 50 mg/dL · LDH 상승)과 여러 균은 장 천공을 가리키므로 며칠 걸리는 세포진보다 원인을 바로 보여 주는 CT 가 먼저다 [[harrison-22: 355장 p.2716]] [[?aasld-ascites-2021]]."
    exception: "열·호중구 증가 없이 단백이 높고 체중이 빠지는 복수라면 세포진이 맞는 검사다."
    cites: ["harrison-22", "?aasld-ascites-2021"]
    covers: ["kmle-2026-1964:A"]
  - contrast: "간경변 복수 감염 = 자발성, 48시간 뒤 재천자로 반응 확인?"
    point: "자발성 세균 복막염은 장 밖 원인 없이 한 균(대장균 등)이 복수를 감염시킨 것이다. 두 균보다 많이 나오면 장 천공에 의한 이차성 복막염을 생각해야 한다 [[harrison-22: 355장 p.2716]]. 이차성은 기다리면 안 된다."
    exception: "전형적 자발성 세균 복막염에서 치료 48시간에 좋아지지 않으면 재천자로 반응을 본다 [[?aasld-ascites-2021]]."
    cites: ["harrison-22", "?aasld-ascites-2021"]
    covers: ["kmle-2026-1964:B"]
  - contrast: "결핵 PCR · 상부 위장관 내시경"
    point: "결핵성 복막염은 림프구 우세의 아급성 경과다. 내시경은 정맥류 출혈 평가이지 복막염 원인을 찾는 검사가 아니다 — 천공된 궤양이라도 CT 가 공기·유출을 보여 준다."
    cites: ["harrison-22"]
    covers: ["kmle-2026-1964:D", "kmle-2026-1964:E"]
tables:
  - id: sbp-vs-ssbp
    section: "가르는 소견 — 자발성인가 이차성인가"
    title: "자발성 대 이차성 세균 복막염"
    role: comparison
    span: full
    columns: ["항목", "자발성(SBP)", "이차성"]
    rows:
      - ["원인", "장내 세균의 전위 — 복강 안 원인 없음 [[harrison-22: 355장 p.2716]]", "천공·농양·허혈 등 복강 안 원인 [[harrison-22: 342장 p.2597]]"]
      - ["균", "한 종류(대장균 흔함)", "두 종류 넘게·혐기균·진균 [[harrison-22: 355장 p.2716]]"]
      - ["복수 총단백·포도당·LDH", "단백 낮음·포도당 정상·LDH 낮음", "단백 > 1 g/dL · 포도당 < 50 mg/dL · LDH > 혈청 상한 중 둘 이상 [[?aasld-ascites-2021]]"]
      - ["다음 검사·치료", "3세대 세팔로스포린 5일 + 알부민 [[harrison-22: 355장 p.2716]]", "즉시 복부 CT + 외과 협진, 광범위 항생제"]
diagram:
  title: "간경변 복수 + 열·복통 — 다음 검사"
  nodes:
    - {id: start, kind: start, text: "간경변 복수 + 열·복통 또는 악화"}
    - {id: info, kind: info, text: "복수 세포수·그람 염색·배양·단백·포도당·LDH"}
    - {id: pmn, kind: decision, text: "복수 호중구 > 250/μL 인가?"}
    - {id: noinf, kind: end, text: "세균 복막염 아님 — 다른 원인 평가"}
    - {id: sec, kind: decision, text: "이차성 기준·여러 균이 있는가?"}
    - {id: ct, kind: step, text: "즉시 복부 조영증강 CT + 외과 협진"}
    - {id: src, kind: end, text: "천공·농양 — 수술·배액 + 광범위 항생제"}
    - {id: sbp, kind: step, text: "자발성 — 세팔로스포린 + 알부민"}
    - {id: resp, kind: decision, text: "48시간에 임상이 좋아졌나?"}
    - {id: done, kind: end, text: "치료 마치고 예방 항생제"}
    - {id: retap, kind: end, text: "복수 재천자 — 이차성 다시 의심"}
  edges:
    - {from: start, to: info}
    - {from: info, to: pmn}
    - {from: pmn, to: noinf, label: "아니다"}
    - {from: pmn, to: sec, label: "그렇다"}
    - {from: sec, to: ct, label: "있다"}
    - {from: sec, to: sbp, label: "없다"}
    - {from: ct, to: src}
    - {from: sbp, to: resp}
    - {from: resp, to: done, label: "호전"}
    - {from: resp, to: retap, label: "불응"}
diagram_notes:
  - "이차성 기준: 복수 총단백 > 1 g/dL · 포도당 < 50 mg/dL · LDH > 혈청 정상 상한 중 둘 이상 [[?aasld-ascites-2021]]."
  - "CT 에서 원인이 없더라도 이차성 기준을 만족하면 외과와 함께 보고 혐기균까지 덮는 항생제를 쓴다."
  - "배양은 침대 곁에서 혈액배양병에 복수를 바로 넣는다 [[harrison-22: 355장 p.2716]]."
checks:
  - q: "자발성 세균 복막염에서 복수 단백이 낮은 것이 왜 진단에 도움이 되는가?"
    a: "낮은 단백 복수는 옵소닌(보체·면역글로불린)이 적어 장에서 넘어온 한 균이 자리 잡기 쉽다. 반대로 단백·LDH 가 높고 포도당이 낮으면 장 내용물 유출과 많은 균·호중구의 소비를 뜻해 이차성을 의심한다."
  - q: "복수 그람 염색에서 그람 양성 알균·그람 음성 막대균·효모가 함께 보이면?"
    a: "여러 균은 장 천공을 시사하므로 이차성 복막염을 의심해 즉시 복부 CT 와 외과 협진을 한다."
figures_none: "복수 검사 수치로 가르는 검사 선택이 목표 — 영상은 다음 단계의 결과이지 판단 단서가 아니다"
variants:
  - id: v1
    of: kmle-2026-1964
    flip: true
    changed: "이차성 기준·여러 균 → 단백 0.7 g/dL·포도당 정상·그람 음성 막대균 한 종류의 전형적 자발성 복막염에 48시간 치료 뒤 열·호중구가 그대로 — 정답이 복부 CT 에서 48시간 뒤 복수 재천자로 바뀐다"
    context: "전형적 자발성 세균 복막염의 치료 반응을 확인하는 경우"
    stem: "61세 여자가 알코올 간경변으로 복수가 있어 이뇨제를 먹던 중 열과 가벼운 복부 불편감으로 입원했다. 입원 때 복수 다형핵 백혈구 1,200/μL, 총단백 0.7 g/dL, 포도당 118 mg/dL, 젖산탈수소효소 120 IU/L(혈청 정상 상한 250), 그람 염색에서 그람 음성 막대균 한 종류가 보여 세포탁심과 알부민을 시작했다. 48시간이 지났지만 체온 38.2 ℃ 로 열이 남아 있고 복부 압통은 그대로이며 혈압 104/62 mmHg, 맥박 96회/분이다. 다음으로 시행할 검사로 가장 적절한 것은?"
    choices: ["A. 복수 세포진 검사", "B. 복수 재천자", "C. 상부 위장관 내시경", "D. 복수 결핵균 PCR", "E. 간 생검"]
    answer: "B"
    explanation: "단백이 낮고 포도당·LDH 가 정상이며 한 균만 보여 입원 때는 전형적 자발성 세균 복막염이었고, 원 문항처럼 즉시 CT 로 천공을 찾을 단서가 없었다. 그러나 48시간 치료에도 좋아지지 않으면 재천자로 호중구가 충분히 줄었는지 보아 치료 실패와 이차성 복막염 가능성을 다시 판단한다."
    kind: application
  - id: v2
    of: kmle-2026-1964
    flip: false
    changed: "58세 남자·B형 간염 간경변 → 66세 여자·알코올 간경변, 복통이 먼저가 아니라 혼돈으로 내원, 검사 제시 순서를 바꿈 — 이차성 기준과 여러 균이라는 결정적 단서는 그대로라 답은 복부 CT"
    context: "다른 인물·다른 첫 증상의 같은 이차성 복막염"
    stem: "66세 여자가 하루 전부터 말이 어눌하고 헛소리를 해서 가족이 데려왔다. 알코올 간경변으로 복수가 있어 이뇨제를 먹는다. 체온 38.6 ℃, 혈압 98/60 mmHg, 맥박 112회/분이고, 배가 불러 있으며 누르면 전체적으로 아파한다. 진단적 복수천자를 하고 정맥 항생제를 시작했다. 복수 그람 염색에서 그람 음성 막대균·그람 양성 알균이 함께 보이고, 복수 젖산탈수소효소 540 IU/L(혈청 정상 상한 250), 포도당 28 mg/dL, 총단백 2.2 g/dL, 다형핵 백혈구 6,100/μL 이다. 다음으로 시행할 검사로 가장 적절한 것은?"
    choices: ["A. 복부 조영증강 CT", "B. 48시간 뒤 복수 재천자", "C. 뇌 자기공명영상", "D. 복수 세포진 검사", "E. 혈청 암모니아 측정"]
    answer: "A"
    explanation: "혼돈으로 왔지만 열·복부 압통과 복수 호중구 6,100/μL 는 세균 복막염이고, 단백 > 1 g/dL·포도당 < 50 mg/dL·LDH 상승에 여러 균까지 보여 이차성 복막염이다. 혼돈은 감염이 부른 간성뇌증으로 설명된다. 천공·농양을 찾아 수술 여부를 정해야 하므로 즉시 복부 CT 를 찍고 외과에 알린다."
    kind: application
sources:
  - id: harrison-22
    org: "McGraw Hill"
    title: "Harrison's Principles of Internal Medicine, 22nd ed."
    kind: textbook
    year: 2025
    citation: "Harrison's Principles of Internal Medicine, 22e. 355장 Cirrhosis and Its Complications p.2708–2718 · 342장 Acute Appendicitis and Peritonitis p.2594–2598"
    checked_at: 2026-11-24
    checked: "본문 대조(드라이브 22판 장별 문서) — 355장 p.2716: SBP 는 복강 안 원인 없는 복수의 자발 감염, 입원 간경변 복수의 최대 30 %·병원 사망 25 %, 세균 전위, 대장균 등 장내 세균, 두 균보다 많으면 천공에 의한 이차성 복막염을 고려, 진단은 복수 호중구 > 250/μL, 침대 곁 혈액배양병, 3세대 세팔로스포린 5일 + 알부민(1일 1.5 g/kg, 3일 1.0 g/kg) · 342장 p.2597: 이차성 복막염은 속 빈 장기 천공, 원인 표, 복수가 있으면 단백·LDH·세포수 검사, 치료는 원인의 수술적 교정 포함"
    verified: text
  - id: aasld-ascites-2021
    org: "American Association for the Study of Liver Diseases"
    title: "Diagnosis, Evaluation, and Management of Ascites, Spontaneous Bacterial Peritonitis and Hepatorenal Syndrome: 2021 Practice Guidance by the AASLD"
    kind: guideline
    year: 2021
    citation: "Biggins SW, Angeli P, Garcia-Tsao G, et al. Hepatology 2021;74(2):1014–1048"
    doi: "10.1002/hep.31884"
    checked_at: 2026-11-24
    checked: "서지만 — 루틴 컨테이너가 PubMed·doi.org 를 막아 본문을 대조하지 못했다. 이차성 복막염 기준(총단백 > 1 g/dL · 포도당 < 50 mg/dL · LDH > 혈청 상한 중 둘)과 치료 48시간 불응 시 재천자는 기억에 근거하며 DOI 도 기억으로 적었다"
    verified: citation
---

## 판단 — 왜 지금 CT 인가
- 복수 호중구 > 250/μL 이면 세균 복막염이다 [[harrison-22: 355장 p.2716]]. 다음 질문은 「복강 안에 원인이 있는가」다.
- 이차성 기준(단백 > 1 g/dL · 포도당 < 50 mg/dL · LDH 상승)과 여러 균은 장 천공·농양을 가리킨다 [[?aasld-ascites-2021]]. 이차성은 원인을 수술·배액으로 고쳐야 낫는다 [[harrison-22: 342장 p.2597]].
- 그래서 항생제를 시작한 뒤 곧바로 천공·농양을 보여 주는 복부 조영증강 CT 를 찍고 외과에 알린다. 세포진·결핵 PCR·재천자는 이 질문에 답하지 못한다.

## 기전 — 장내 세균 전위와 장 유출
자발성 세균 복막염은 장내 세균이 장벽을 넘어 장간막 림프절로 가고 균혈증을 거쳐 복수에 자리 잡는 것이다 — 대장균 같은 한 균이 대부분이다 [[harrison-22: 355장 p.2716]]. 낮은 단백 복수는 방어 물질이 적어 이런 감염에 취약하다. 이차성은 천공된 장에서 내용물이 직접 새어 여러 균(혐기균·진균 포함)이 한꺼번에 들어온다. 많은 균과 호중구가 포도당을 소비해 포도당이 떨어지고, 염증과 조직 손상이 단백·LDH 를 올린다.

## 가르는 소견 — 자발성인가 이차성인가
- 두 균보다 많이 나오면 천공을 생각한다 [[harrison-22: 355장 p.2716]]. 그람 염색 한 번으로 그 단서가 먼저 보이기도 한다.
- 자발성 세균 복막염은 열·복통·의식 변화·급성 신손상으로 오거나 아무 증상 없이 올 수 있어, 입원한 간경변 복수 환자에게는 천자를 넓게 한다 [[harrison-22: 355장 p.2716]].

## 권고와 예외
- 자발성이면 3세대 세팔로스포린 5일과 알부민(1일 1.5 g/kg, 3일 1.0 g/kg)으로 신부전을 줄인다. 회복 뒤에는 퀴놀론 예방 [[harrison-22: 355장 p.2716]].
- 자발성으로 시작했어도 48시간에 좋아지지 않으면 재천자로 반응을 보고 이차성을 다시 생각한다 [[?aasld-ascites-2021]].

## 시험 쟁점 — 충돌·맥락·새 근거
- 해당 없음(대조: 해리슨 22판 355장 p.2716, 342장 p.2597 — 이차성 기준 수치는 해리슨에 없어 지침 미대조로 둔다)
