---
id: cn.rheum.hemochromatosis-arthropathy.iron-studies
type: concept
topic: Rheumatology
see_also: [Gastroenterology, Hematology]
date: 2026-10-06
updated: 2026-10-06
version: 1
outline: h374            # 기본틀 슬롯(content/outline/subjects.yaml) — 해리슨 21판 374장 Arthritis Associated with Systemic Disease
confidence: medium
review_status: unreviewed
note_form: 2            # 판형 2(2026-09-25) — 기본틀 [gap] 으로 쓴 정리본(오답 연결 없음)
title: "혈색소증 관절병증 — 2·3번째 MCP 면 철 검사"
objective: "2·3번째 손허리손가락관절이 두드러진 골관절염 양상 관절병증에서 혈색소증을 의심해 트랜스페린 포화도·페리틴을 검사한다"
objective_kind: 진단
condition: 혈색소증 관절병증(hemochromatosis arthropathy)
exams: [kmle, usmle]
summary:
  - "결론: 양손 2·3번째 손허리손가락관절(MCP)이 두드러진 퇴행성 관절병증이면 트랜스페린 포화도·페리틴을 잰다."
  - "시험 단서: 50세 이후 비염증성 관절액 + 2·3번째 MCP 갈고리 모양 골극(hook-like osteophyte) ± 연골석회화."
  - "왜: 1차 골관절염은 PIP·DIP·첫째 손목손허리관절에 오고 MCP 를 주로 침범하지 않는다 — 분포가 전신 질환을 가리킨다."
  - "조기 진단에는 트랜스페린 포화도가 페리틴 상승보다 민감하다. 약 절반에 칼슘피로인산 결정 침착이 함께 있다."
  - "사혈은 혈색소증 치료지만 이미 생긴 관절염에는 효과가 적다 — 관절은 진통제·NSAID, 진행하면 관절치환."
pitfalls:
  - contrast: "1차 골관절염 vs 혈색소증 관절병증 — 「손의 퇴행성 관절염」"
    point: "둘 다 관절 간격 좁아짐·연골하 경화·낭종·골극을 보이지만 분포가 다르다. 1차 골관절염은 PIP·DIP·첫째 손목손허리관절, 혈색소증은 2·3번째 MCP 가 먼저이고 두드러진다 [[harrison-21: 374장 p.2871]]."
    exception: "MCP 침범이 가벼워도 2·3번째 MCP 가 주 소견이면 철 검사를 한다 [[harrison-21: 374장 p.2871]]."
  - contrast: "갈고리 골극 = 혈색소증 확진?"
    point: "갈고리 모양 골극은 특징적이지만 환자의 20 % 까지에서만 보이고 이 병에만 있는 소견도 아니다 — 진단은 철 검사로 한다 [[harrison-21: 374장 p.2871]]."
  - contrast: "페리틴 정상이면 배제?"
    point: "조기에는 트랜스페린 포화도 상승이 페리틴 상승보다 민감하다 — 포화도를 함께 본다 [[harrison-21: 374장 p.2871]]."
  - contrast: "사혈하면 관절도 좋아진다?"
    point: "사혈은 혈색소증 자체의 치료지만 이미 생긴 관절염에는 효과가 적고, 관절염과 연골석회화는 계속 진행할 수 있다 [[harrison-21: 374장 p.2871]]."
tables:
  - id: hh-ddx
    section: "가르는 소견 — 분포와 관절액"
    title: "손의 퇴행성 관절병증 — 어디에 오나"
    role: differential
    span: column
    columns: ["질환", "주로 침범하는 관절", "가르는 소견"]
    rows:
      - ["혈색소증 관절병증", "양손 2·3번째 MCP → 무릎·발목·어깨·엉덩관절", "갈고리 골극(≤20 %), 비염증성 관절액, 약 절반 CPP 침착 [[harrison-21: 374장 p.2871]]"]
      - ["1차 골관절염", "PIP·DIP·첫째 손목손허리관절", "MCP 는 주로 침범하지 않는다 [[harrison-21: 374장 p.2871]]"]
      - ["말단비대증 관절병증", "무릎·어깨·엉덩관절·손", "초기 관절 간격 넓어짐, 관절 이완, 비염증성 관절액 [[harrison-21: 374장 p.2871]]"]
criteria:
  - id: hh-arthro-eval
    name: 철 검사를 할 때
    kind: 진단 기준
    population: "손의 퇴행성 관절병증"
    statement: "2·3번째 MCP 에 두드러진 방사선·임상 소견이 있으면 가벼워도 페리틴과 철/총철결합능을 검사한다. 조기 진단에는 트랜스페린 포화도 상승이 페리틴보다 민감하다 [[harrison-21: 374장 p.2871]]"
    exceptions: "갈고리 골극은 20 % 까지에서만 보이고 특이적이지 않다 [[harrison-21: 374장 p.2871]]"
    source: harrison-21
    basis: current
    exams: [kmle, usmle]
  - id: hh-arthro-tx
    name: 관절병증 치료
    kind: 치료 권고
    population: "혈색소증 관절병증"
    statement: "혈색소증은 반복 사혈로 치료하지만 이미 생긴 관절염에는 효과가 적다. 관절 증상은 아세트아미노펜·NSAID, 급성 칼슘피로인산 관절염은 고용량 NSAID 나 짧은 글루코코르티코이드, 진행하면 엉덩·무릎 관절치환 [[harrison-21: 374장 p.2871]]"
    exceptions: "저용량 콜히친이 급성 발작 횟수를 줄일 수 있다 [[harrison-21: 374장 p.2871]]"
    source: harrison-21
    basis: current
    exams: [kmle, usmle]
sources:
  - id: harrison-21
    org: "McGraw Hill"
    title: "Harrison's Principles of Internal Medicine, 21st ed. — Chapter 374: Arthritis Associated with Systemic Disease, and Other Arthritides"
    kind: textbook
    year: 2022
    citation: "Loscalzo J, Fauci AS, Kasper DL, et al (eds). Harrison's Principles of Internal Medicine, 21e. 374장(Langford CA, Mandell BF), 인쇄쪽 2871"
    checked_at: 2026-10-06
    checked: "드라이브 장 문서(H21_374)로 본문 대조. p.2871 말단비대증 관절병증(연골 비대로 초기 관절 간격 넓어짐, 이완, 비염증성 관절액, CPP), 혈색소증 관절병증: 증상 40–60세, 관절병증 20–40 %·대개 50세 이후·첫 소견일 수 있음, 손 소관절 → 무릎·발목·어깨·엉덩관절, 2·3번째 MCP 가 먼저·가장 두드러짐(1차 골관절염은 주로 침범하지 않음), 조조강직·사용 시 통증, 1차 골관절염보다 통증 가볍고 일찍 시작, 방사선 관절 간격 좁아짐·연골하 경화·낭종·관절 주위 뼈 증식, 갈고리 골극 20 % 까지·비특이적, 2·3번째 MCP 소견이면 페리틴·철/TIBC 검사, PIP·DIP·첫째 CMC 의 전형적 골관절염 변화는 흔히 없음, 비염증성 관절액, 활막의 철 함유 세포, 약 절반 CPP 침착·후기 급성 CPP 관절염, 트랜스페린 포화도가 페리틴보다 민감, 철의 지질 과산화·피로인산분해효소 억제(연골석회화), 치료(반복 사혈은 기존 관절염에 효과 적음, 아세트아미노펜·NSAID, 급성 CPP 발작은 고용량 NSAID·짧은 글루코코르티코이드, 저용량 콜히친, 관절치환). 장 문서의 쪽 표지로는 이 절 전체가 p.2871 구간에 있다"
    verified: text
diagram:
  title: "손의 퇴행성 관절병증 — 분포에서 철 검사까지"
  nodes:
    - {id: start, kind: start, text: "중년 이후 손의 퇴행성 관절 통증·부기"}
    - {id: fluid, kind: decision, text: "관절액이 염증성인가?"}
    - {id: fluiddo, kind: info, text: "관절 흡인 — 세포 수·결정 확인"}
    - {id: infl, kind: alert, text: "염증성 관절염·결정 관절염 평가"}
    - {id: dist, kind: decision, text: "2·3번째 MCP 가 주로 침범됐나?"}
    - {id: oa, kind: end, text: "1차 골관절염 양상(PIP·DIP·첫째 CMC)"}
    - {id: iron, kind: step, text: "트랜스페린 포화도·페리틴 검사"}
    - {id: sat, kind: decision, text: "트랜스페린 포화도가 높은가?"}
    - {id: hh, kind: end, text: "혈색소증 관절병증 — 혈색소증 평가·사혈"}
    - {id: other, kind: end, text: "다른 원인(말단비대증 등) 찾기"}
  edges:
    - {from: start, to: fluid}
    - {from: fluid, to: infl, label: "염증성"}
    - {from: fluid, to: dist, label: "비염증성"}
    - {from: fluid, to: fluiddo, label: "미시행"}
    - {from: fluiddo, to: infl, label: "염증성"}
    - {from: fluiddo, to: dist, label: "비염증성"}
    - {from: dist, to: oa, label: "아니오"}
    - {from: dist, to: iron, label: "예"}
    - {from: iron, to: sat}
    - {from: sat, to: hh, label: "예"}
    - {from: sat, to: other, label: "아니오"}
diagram_notes:
  - "MCP 침범이 가벼워도 2·3번째 MCP 가 주 소견이면 철 검사를 한다. 갈고리 골극은 20 % 까지에서만 보이고 특이적이지 않다 [[harrison-21: 374장 p.2871]]."
  - "약 절반에 칼슘피로인산 결정 침착이 함께 있어, 후기에 급성 CPP 관절염 발작이 올 수 있다 — 결정이 보여도 혈색소증을 배제하지 않는다 [[harrison-21: 374장 p.2871]]."
  - "사혈은 기존 관절염·연골석회화의 진행을 막지 못한다 — 관절은 증상 치료, 진행하면 관절치환 [[harrison-21: 374장 p.2871]]."
checks:
  - q: "혈색소증 관절병증이 가장 먼저·두드러지게 침범하는 관절은?"
    a: "양손 2·3번째 손허리손가락관절(MCP)."
  - q: "1차 골관절염의 전형적 손 관절은?"
    a: "PIP·DIP·첫째 손목손허리관절 — MCP 는 주로 침범하지 않는다."
  - q: "혈색소증 조기 진단에 페리틴보다 민감한 검사는?"
    a: "트랜스페린 포화도."
variants:
  - id: v1
    context: "같은 목표 — 손 관절병증으로 처음 드러난 혈색소증"
    stem: "54세 남자가 2년 전부터 양손이 뻣뻣하고 물건을 쥘 때 아프다며 왔다. 아침 강직은 15분 정도다. 양손 둘째·셋째 손허리손가락관절이 단단하게 커져 있고 가볍게 압통이 있다. 손가락 끝마디 관절은 정상이다. 손 X선에서 둘째·셋째 손허리손가락관절의 관절 간격 좁아짐, 연골하 낭종, 갈고리 모양 골극이 있다. 무릎 관절액은 백혈구 400/µL 이다. 다음으로 해야 할 검사는?"
    choices: ["A. 혈청 트랜스페린 포화도·페리틴", "B. 혈청 요산", "C. 류마티스인자 반복 검사", "D. 손 MRI", "E. HLA-B27"]
    answer: "A"
    explanation: "비염증성 관절액과 1차 골관절염이 주로 침범하지 않는 2·3번째 MCP 의 퇴행성 변화(갈고리 골극)는 혈색소증 관절병증을 가리킨다 — 트랜스페린 포화도·페리틴(철/총철결합능)을 잰다. 조기에는 트랜스페린 포화도가 페리틴보다 민감하다 [[harrison-21: 374장 p.2871]]."
    kind: application
figures_wanted:
- source: PMC_OA
  shows: 혈색소증 관절병증 — 2·3번째 손허리손가락관절의 퇴행성 변화·갈고리 골극
  query: '"hemochromatosis" AND "metacarpophalangeal" AND "radiograph"'
  caption_terms:
  - metacarpophalangeal
  modality: XR
figures_rejected:
- asset: PMC-PMC9498090_Figure5
  reason: 그림 설명이 류마티스관절염의 절단성 관절염(arthritis mutilans)이다 — 미란·골소실·자쪽 편위이지 혈색소증의 2·3번째 MCP 퇴행성 변화·갈고리 골극이 아니다
---

## 판단 — 왜 2·3번째 MCP 가 철 검사를 부르나
- 1차 골관절염은 PIP·DIP·첫째 손목손허리관절(CMC)에 오고 MCP 를 주로 침범하지 않는다. 그래서 2·3번째 MCP 가 두드러진 퇴행성 관절병증은 **분포 자체가 전신 질환의 단서**다 [[harrison-21: 374장 p.2871]].
- 관절병증은 혈색소증 환자의 20–40 % 에 오고 대개 50세 이후 시작하며, **혈색소증의 첫 소견**일 수 있다 [[harrison-21: 374장 p.2871]].
- 진단은 방사선 소견이 아니라 철 검사로 한다 — 갈고리 골극은 특징적이지만 흔하지도 특이적이지도 않다.

## 기전 — 철 침착에서 연골 손상으로
혈색소증(hemochromatosis)은 장에서 철을 지나치게 흡수해 실질 세포에 철이 쌓이고 장기 기능이 떨어지는 철 저장 질환이다 [[harrison-21: 374장 p.2871]]. 관절에서는 활막 안층에 철 함유 세포가 늘고 섬유화·단핵구 침윤이 생긴다. 철은 슈퍼옥사이드 의존 지질 과산화를 촉매해 연골을 손상시키고, 동물 모델에서 3가 철은 콜라겐 형성을 방해하며 활막 세포의 리소좀 효소 방출을 늘린다. 철이 활막의 **피로인산분해효소를 억제**하면 피로인산이 쌓여 연골석회화(chondrocalcinosis)가 생긴다고 본다 — 약 절반에서 칼슘피로인산 결정 침착이 함께 보이는 이유다 [[harrison-21: 374장 p.2871]].

## 가르는 소견 — 분포와 관절액
- **증상**: 아침 강직과 사용 시 통증, 관절이 커지고 가볍게 아프다. 1차 골관절염보다 통증이 가볍고 일찍 시작하며 장애가 적다 [[harrison-21: 374장 p.2871]].
- **방사선**: 관절 간격 좁아짐, 연골하 경화·낭종, 관절 주위 뼈 증식, 갈고리 골극(20 % 까지). PIP·DIP·첫째 CMC 의 전형적 골관절염 변화는 흔히 없다 [[harrison-21: 374장 p.2871]].
- **관절액**: 비염증성 — 염증성 관절염과 다르다. 결정이 보여도(칼슘피로인산) 혈색소증을 배제하지 않는다.
- **철 검사**: 페리틴과 철/총철결합능. 조기에는 트랜스페린 포화도가 페리틴보다 민감하다 [[harrison-21: 374장 p.2871]].

## 선택 — 혈색소증 치료와 관절 치료는 따로
- 혈색소증은 반복 사혈(phlebotomy)로 치료한다. 그러나 이미 생긴 관절염에는 효과가 적고 관절염·연골석회화는 진행할 수 있다 [[harrison-21: 374장 p.2871]].
- 관절 증상은 아세트아미노펜·NSAID, 급성 칼슘피로인산 관절염 발작은 고용량 NSAID 또는 짧은 글루코코르티코이드, 저용량 콜히친이 발작 횟수를 줄일 수 있다. 진행한 엉덩·무릎 관절은 관절치환이 성공적이다 [[harrison-21: 374장 p.2871]].

## 권고와 예외
- 2·3번째 MCP 소견이 가벼워도 철 검사를 한다 [[harrison-21: 374장 p.2871]].
- 혈색소증 전신 평가(유전자 검사·간 평가 등)는 해리슨 414장의 범위라 이 정리본에서 대조하지 않았다(검토 항목).

## 시험 쟁점 — 충돌·맥락·새 근거
- 해당 없음(대조: 해리슨 374장 p.2871).

## (심화) 왜 철이 연골석회화를 부르나
피로인산은 연골 세포 주위에서 계속 만들어지고 피로인산분해효소가 이를 무기 인산으로 쪼개 칼슘피로인산 결정이 쌓이지 않게 한다. 철이 이 효소를 억제하면 피로인산이 남아 칼슘과 결정을 이룬다 [[harrison-21: 374장 p.2871]]. 그래서 혈색소증은 퇴행성 관절병증과 결정 관절염을 한 환자에게 함께 일으키고, 사혈로 철을 줄여도 이미 쌓인 결정과 손상된 연골은 되돌아오지 않는다.
