---
id: cn.cardio.atrial-fibrillation.doac-nonvalvular-anticoagulation
type: concept
topic: Cardiology
see_also: [cn.cardio.palpitations.arrhythmia-evaluation]
date: 2026-11-11
updated: 2026-11-11
version: 2
outline: h251
confidence: medium
review_status: unreviewed
note_form: 2
title: "심방세동 — 뇌졸중 예방은 점수로 항응고제"
objective: "혈역학적으로 안정한 비판막성 심방세동에서 CHA₂DS₂-VASc 점수로 항응고 여부를 정하고 직접 경구 항응고제를 고른다"
objective_kind: 치료
condition: 심방세동(atrial fibrillation, AF)
exams: [kmle, usmle]
summary:
  - "결론: 안정한 비판막성 심방세동은 CHA₂DS₂-VASc 로 위험을 매겨 경구 항응고제(대개 직접 경구 항응고제)를 준다."
  - "시험 단서: 우연히 발견된 불규칙한 맥, P파 없는 불규칙 RR, 고혈압·고령 — 증상 없음(asymptomatic AF)."
  - "왜: 수축 못 하는 좌심방이에 고인 피가 피브린 혈전을 만든다 — 혈소판이 아니라 응고 연쇄를 막아야 한다."
  - "아스피린·클로피도그렐은 와파린보다 예방 효과가 떨어지고 출혈은 적지 않다 — 단독 예방 약이 아니다."
  - "승모판 협착·기계판막이면 와파린만. 저혈압·폐부종·허혈이면 먼저 즉시 율동전환."
pitfalls:
  - contrast: "아스피린 vs 경구 항응고제"
    point: "심방세동 혈전은 피가 고여 생긴 피브린 혈전이라 항혈소판제로는 부족하다. 와파린은 위약보다 뇌졸중을 64 %, 항혈소판제보다 37 % 더 줄이고, 아스피린은 출혈 위험도 적지 않다."
    cites: ["harrison-22: 258장 p.1950–1951"]
    covers: ["imaging-2026-0607:B"]
  - contrast: "증상 없고 심박수 정상 = 지켜본다?"
    point: "뇌졸중 위험은 증상·심박수가 아니라 위험인자가 정한다. 동리듬이 유지되는 것처럼 보여도 무증상 발작이 흔해 점수대로 항응고한다."
    cites: ["harrison-22: 258장 p.1951"]
  - contrast: "불규칙한 맥 = 즉시 율동전환?"
    point: "즉시 율동전환은 혈역학 악화·폐부종·허혈이 있을 때다. 지속 시간을 모르거나 48시간이 넘으면 전환 자체가 혈전색전 위험이라 항응고가 먼저다."
    cites: ["harrison-22: 258장 p.1949"]
tables:
  - id: af-antithrombotic
    section: "선택 — 어떤 약으로 막나"
    title: "심방세동 뇌졸중 예방 — 약 고르기"
    role: treatment
    span: column
    columns: ["상황", "선택"]
    rows:
      - ["비판막성, 위험인자 ≥ 1(여성 단독 제외)", "경구 항응고제 — 직접 경구 항응고제가 와파린과 같거나 조금 낫다 [[harrison-22: 258장 p.1950]]"]
      - ["류마티스 승모판 협착 · 기계판막", "와파린(직접 경구 항응고제는 기계판막에서 열등) [[harrison-22: 258장 p.1950–1951]]"]
      - ["위험인자 0(또는 여성만)", "항응고 없이 위험인자 재평가 [[harrison-22: 258장 p.1950]]"]
      - ["항혈소판제 단독", "권하지 않음 — 와파린보다 열등, 출혈 적지 않음 [[harrison-22: 258장 p.1951]]"]
criteria:
  - id: chadsvasc
    name: CHA₂DS₂-VASc 점수
    kind: 위험 점수
    population: "비판막성 심방세동"
    statement: "심부전 1 · 고혈압 1 · 75세 이상 2 · 당뇨 1 · 뇌졸중/일과성 허혈발작 2 · 혈관질환 1 · 65~74세 1 · 여성 1. 미국·유럽은 여성 단독이 아닌 1점 이상에서 항응고를 권한다 [[harrison-22: 258장 p.1950]]"
    exceptions: "비대심근병증·승모판 협착·뇌졸중 병력은 점수와 무관하게 고위험이라 금기가 없으면 항응고 [[harrison-22: 258장 p.1950]]"
    source: harrison-22
    basis: current
    exams: [kmle, usmle]
sources:
  - id: harrison-22
    org: "McGraw Hill"
    title: "Harrison's Principles of Internal Medicine, 22nd ed. — Chapter 258: Atrial Fibrillation"
    kind: textbook
    year: 2025
    citation: "Harrison's Principles of Internal Medicine, 22e. 258장 p.1947–1951"
    checked_at: 2026-11-11
    checked: "드라이브 22판 장별 문서 H22_258 본문 대조 — 정의·불규칙 심실 반응(p.1947) · 혈역학 악화·폐부종·허혈이면 즉시 율동전환, 48시간 넘거나 모르면 전환 전후 항응고, 좌심방 기절(p.1949) · 승모판 협착·비대심근병증·뇌졸중 병력 고위험, CHA2DS2-VASc(그림 258-3) ≥ 1(여성 단독 제외) 항응고 권고, 항혈소판 단독 부족, 와파린 위약 대비 64 %·항혈소판 대비 37 % 감소, 직접 경구 항응고제 비열등·통합 분석 0.4–0.7 % 우월, 류마티스 승모판 협착·기계판막은 와파린(p.1950) · 직접 경구 항응고제 신기능 용량 조절, 아스피린·클로피도그렐 와파린보다 열등·출혈 적지 않음, 동리듬 유지돼도 점수대로 항응고(p.1951)"
    verified: text
  - id: acc-aha-2023
    org: "ACC/AHA/ACCP/HRS"
    title: "2023 ACC/AHA/ACCP/HRS Guideline for the Diagnosis and Management of Atrial Fibrillation"
    kind: guideline
    year: 2024
    citation: "Joglar JA et al. J Am Coll Cardiol 83:109, 2024 (해리슨 258장 참고문헌)"
    doi: 10.1016/j.jacc.2023.08.017
    checked_at: 2026-11-11
    checked: "서지만 — 해리슨 258장 참고문헌에서 확인. 권고 본문·등급은 원문 미대조(루틴 컨테이너가 PubMed 차단, PMID 미확인). DOI 는 기억으로 적었다 — 학습서 워크플로가 확인"
    verified: citation
diagram:
  title: "심방세동 — 뇌졸중 예방 판단"
  nodes:
    - {id: start, kind: start, text: "심전도 심방세동(P파 없음·불규칙 RR)"}
    - {id: unstable, kind: decision, text: "저혈압·폐부종·허혈이 있나?"}
    - {id: shock, kind: alert, text: "즉시 동기화 전기 율동전환"}
    - {id: valve, kind: decision, text: "승모판 협착·기계판막인가?"}
    - {id: echo, kind: info, text: "심초음파로 판막 확인"}
    - {id: warfarin, kind: end, text: "와파린"}
    - {id: score, kind: decision, text: "성별 외 위험인자가 있나?"}
    - {id: doac, kind: end, text: "직접 경구 항응고제"}
    - {id: observe, kind: end, text: "항응고 없이 위험인자 재평가"}
  edges:
    - {from: start, to: unstable}
    - {from: unstable, to: shock, label: "있음"}
    - {from: unstable, to: valve, label: "없음"}
    - {from: valve, to: warfarin, label: "예"}
    - {from: valve, to: score, label: "아니오"}
    - {from: valve, to: echo, label: "모름"}
    - {from: echo, to: warfarin, label: "있음"}
    - {from: echo, to: score, label: "없음"}
    - {from: score, to: doac, label: "1점 이상"}
    - {from: score, to: observe, label: "0점"}
diagram_notes:
  - "점수: 심부전·고혈압·당뇨·혈관질환·65~74세·여성 각 1, 75세 이상·뇌졸중/TIA 각 2 [[harrison-22: 258장 p.1950]]."
  - "비대심근병증·뇌졸중 병력은 점수와 무관하게 항응고 대상 [[harrison-22: 258장 p.1950]]."
  - "직접 경구 항응고제는 신기능에 따라 용량을 조절한다 [[harrison-22: 258장 p.1951]]."
checks:
  - q: "73세 남자, 고혈압만 있는 비판막성 심방세동. 점수와 처치는?"
    a: "65~74세 1 + 고혈압 1 = 2점. 직접 경구 항응고제."
  - q: "왜 아스피린이 아닌가?"
    a: "심방세동 혈전은 정체로 생긴 피브린 혈전이고, 아스피린은 와파린보다 덜 막으면서 출혈은 적지 않다."
variants:
  - id: v1
    of: imaging-2026-0607
    flip: true
    changed: "흉통·호흡곤란 없음, 혈압 132/80 → 30분 전부터 숨이 차고 가슴을 쥐어짜며 혈압 78/50, 양폐 수포음 ⇒ 정답이 아픽사반에서 즉시 동기화 전기 율동전환으로"
    context: "같은 환자 뼈대, 혈역학 불안정 단서를 넣은 글 변형(그림 없음)"
    stem: "73세 남자가 30분 전부터 갑자기 숨이 차고 가슴을 쥐어짜는 듯 아파 응급실에 왔다. 고혈압으로 암로디핀을 먹고 있다. 혈압 78/50 mmHg, 맥박 158회/분(불규칙), 산소포화도 86 % 이고 양쪽 폐에서 수포음이 들린다. 심전도에서 P파가 보이지 않고 RR 간격이 완전히 불규칙한 좁은 QRS 빈맥이다. 가장 적절한 처치는?"
    choices: ["A. 아픽사반 경구 투여를 시작한다", "B. 아스피린 경구 투여를 시작한다", "C. 즉시 동기화 전기 율동전환을 한다", "D. 경식도 심초음파 후 율동전환을 계획한다", "E. 디곡신 정맥 주사 후 경과를 본다"]
    answer: "C"
    explanation: "리듬은 같은 심방세동이지만 저혈압·폐부종·허혈성 흉통이 있어 혈역학적으로 불안정하다. 이때는 뇌졸중 예방보다 심박출 회복이 먼저라 즉시 동기화 전기 율동전환을 한다. 항응고는 전환과 함께 시작하되, 안정될 때까지 미루지 않는다."
    kind: application
  - id: v2
    of: imaging-2026-0607
    flip: false
    changed: "73세 남자·고혈압 → 68세 여자·당뇨 없음·검진 심전도, 소견을 글로 제시 ⇒ 65~74세 1 + 여성 1 + 고혈압 1 = 3점, 비판막성·안정이라 답은 그대로 직접 경구 항응고제"
    context: "겉모습만 바꾼 글 변형(그림 없음)"
    stem: "68세 여자가 건강검진 심전도에서 이상이 있다는 말을 듣고 왔다. 증상은 없고 언제부터인지 모른다. 고혈압으로 약을 먹고 있으며 당뇨병·심부전·뇌졸중 병력은 없다. 혈압 128/76 mmHg, 맥박 82회/분(불규칙)이다. 심초음파에서 판막 이상은 없고 혈청 크레아티닌은 0.8 mg/dL 이다. 심전도에서 P파가 없고 기저선이 잔물결 모양이며 RR 간격이 완전히 불규칙하다. 가장 적절한 처치는?"
    choices: ["A. 아스피린 경구 투여", "B. 클로피도그렐 경구 투여", "C. 리바록사반 경구 투여", "D. 즉시 전기 율동전환", "E. 항혈전 치료 없이 1년 뒤 재평가"]
    answer: "C"
    explanation: "나이·성별·발견 경위가 바뀌었지만 결정 단서는 같다 — 안정한 비판막성 심방세동, 성별 외 위험인자(65~74세·고혈압)가 있다. 경구 항응고제 대상이고 직접 경구 항응고제가 먼저다. 항혈소판제는 예방 효과가 떨어지고, 지속 시간을 모르는 심방세동을 항응고 없이 전환하면 혈전색전 위험이 있다."
    kind: application
figures:
- id: f1
  file: docs/assets/figures/ptbxl-14102.png
  kind: ecg
  at: 기전 — 떨기만 하는 심방에 고이는 피
  shows: 심방세동
  look_for:
  - II 리듬 스트립 — 구분되는 P파 없이 흔들리는 기저선
  - QRS 사이 간격이 규칙 없이 매번 다름
  label: atrial fibrillation (SCP AFIB, 가능도 100)
  label_basis: dataset_expert
  reference: 심장내과 전문의의 SCP-ECG 판독을 두 번째 전문의가 검증 — 해당 진술의 가능도 100 인 기록만
  paper: Wagner P 외. PTB-XL, a large publicly available electrocardiography dataset. Sci Data 2020;7:154
  doi: 10.1038/s41597-020-0495-6
  credit: PTB-XL ECG dataset v1.0.3 (PhysioNet, CC BY 4.0) · record 14102
  license: Creative Commons Attribution 4.0 International
  url: https://physionet.org/content/ptb-xl/1.0.3/records500/14000/#files-panel
  asset: PTBXL-14102
  paper_cited_by: 1213
---

## 판단 — 왜 항응고제가 먼저인가
- **안정한가**: 저혈압·폐부종·허혈이 없으면 오늘의 문제는 리듬이 아니라 뇌졸중 예방이다 [[harrison-22: 258장 p.1949]].
- **판막성인가**: 류마티스 승모판 협착·기계판막이면 와파린만 쓴다 [[harrison-22: 258장 p.1950]].
- **점수**: 비판막성이면 CHA₂DS₂-VASc 로 매기고, 여성 단독이 아닌 1점 이상이면 항응고를 권한다 [[harrison-22: 258장 p.1950]].
- **약**: 직접 경구 항응고제(direct oral anticoagulant)는 와파린에 비열등하고, 통합 분석에서 사망·뇌졸중·대출혈·두개내출혈이 조금 적다 [[harrison-22: 258장 p.1950]].

## 기전 — 떨기만 하는 심방에 고이는 피
심방세동은 무질서하고 빠른 심방 흥분으로 심방의 조직적 수축이 사라진 상태다. 방실결절이 그 흥분 중 일부만 통과시켜 심실 박동이 불규칙해진다 [[harrison-22: 258장 p.1947]]. 수축하지 못하는 좌심방, 특히 막다른 주머니인 좌심방이(left atrial appendage)에서 피가 정체해 피브린 혈전이 생기고, 떨어지면 뇌색전이 된다. 동리듬으로 돌아온 뒤에도 심방 기능은 몇 주 늦게 회복돼(심방 기절, atrial stunning) 그 사이에도 혈전이 생길 수 있다 [[harrison-22: 258장 p.1949]]. 그래서 예방 약은 혈소판이 아니라 응고 연쇄를 막는 항응고제다.

## 선택 — 어떤 약으로 막나
- 와파린은 위약보다 연간 뇌졸중을 64 %, 항혈소판제보다 37 % 줄인다 [[harrison-22: 258장 p.1950]].
- 직접 경구 항응고제는 효과가 빨리 나고 혈액 검사로 용량을 맞출 필요가 없지만, 다비가트란·리바록사반·아픽사반은 신장으로 배설돼 신기능에 맞춰 용량을 줄인다 [[harrison-22: 258장 p.1951]].
- 기계판막에서는 직접 경구 항응고제가 와파린보다 판막 혈전·색전을 덜 막는다 [[harrison-22: 258장 p.1951]].

## 권고와 예외
- 즉시 율동전환은 혈역학 악화·폐부종·관상동맥 허혈이 있을 때다. 지속 시간이 48시간을 넘거나 모르면 위험 점수가 낮아도 전환 후 혈전색전 위험이 커서, 전환 전 3주·후 최소 4주 항응고하거나 경식도 심초음파로 혈전을 배제한다 [[harrison-22: 258장 p.1949]].
- 리듬 조절로 동리듬이 유지되는 것처럼 보여도 무증상 발작이 흔해 항응고는 점수대로 유지한다 [[harrison-22: 258장 p.1951]].

## 시험 쟁점 — 충돌·맥락·새 근거
- **Z1 맥락 · 남자 1점에서 항응고** — 시험 기준: 남자 2점 이상(여자 3점 이상)이면 항응고를 권한다 — 문항 해설이 인용한 2023 미국 지침의 기준 [[?acc-aha-2023]] / 다른 기준: 해리슨은 미국·유럽이 여성 단독이 아닌 1점 이상에서 항응고를 권한다고 쓴다 [[harrison-22: 258장 p.1950]] / 왜 다른가: 1점은 이득과 출혈이 비슷한 구간이라 지침이 권고 강도를 낮춰 두는 자리 — 2023 미국 지침의 등급은 원문 미대조 [[?acc-aha-2023]] / 시험에서는: KMLE · USMLE 모두 2점 이상(남자)이면 항응고가 정답, 1점 남자는 「고려」 수준으로 묻는 문항이 나오면 보기의 표현을 본다.
