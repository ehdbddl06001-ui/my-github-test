---
id: cn.prev.outbreak-investigation.epidemic-curve-and-steps
type: concept
topic: Preventive Medicine
see_also: [Infectious Disease]
date: 2026-11-20
updated: 2026-11-20
version: 1
outline: prev.infection-control   # 기본틀 슬롯(content/outline/subjects.yaml) — 예방의학 손 슬롯 「감염병 관리와 역학조사」
confidence: medium
review_status: unreviewed
note_form: 2            # 판형 2(2026-09-25) — 기본틀 빈 슬롯으로 쓴 정리본(오답 연결 없음)
title: "집단 발병 — 유행 곡선으로 전파 양식을 읽는다"
objective: "집단 발병에서 유행 곡선의 모양으로 전파 양식을 가려 역학조사의 다음 단계를 고른다"
objective_kind: 다음 처치
condition: 집단 발병(outbreak) 역학조사 — 유행 곡선(epidemic curve) · 공통 감염원(common source) · 전파성(propagated) 유행 · 기초감염재생산수(R0) · 집단면역(herd immunity)
exams: [kmle, usmle]
summary:
  - "결론: 가파르게 올라 완만히 내려가는 한 봉우리는 단일 노출, 고원은 지속 노출, 잠복기 간격의 여러 봉우리는 사람 간 전파."
  - "시험 단서: 「같은 식사 뒤 하루 사이 환자 집중」(point source), 「몇 주째 비슷한 수」(continuous), 「약 1 잠복기마다 새 봉우리」(propagated)."
  - "왜: 한 번의 짧은 노출이면 모든 환자가 한 잠복기 안에 생기고, 사람 간 전파는 세대마다 잠복기만큼 늦게 다음 환자를 만든다."
  - "단계: 유행 확인 → 진단 확인 → 환자 정의 → 사례 찾기 → 기술 역학 → 가설 → 분석 → 관리 · 감시 · 소통 — 관리는 끝까지 기다리지 않는다."
  - "집단면역 임계값 = 1 − 1/R0(R0 4 → 75 %). 면역이 고르지 않으면 넘어도 국소 유행이 남는다."
pitfalls:
  - contrast: "환자 수가 늘었으니 바로 유행?"
    point: "먼저 평소 기대치와 비교한다. 보고 방식·환자 정의 변경, 관심 증가, 새 진단 검사, 오진·검사 오류, 인구 변화(휴양지·대학가)만으로도 겉보기 증가가 생긴다 [[cdc-poe-l6: Step 2 Establish the existence of an outbreak]]."
  - contrast: "환자 정의에 의심 노출(예: 특정 음식 섭취)을 넣는다?"
    point: "환자 정의에는 조사하려는 노출을 넣지 않는다 — 넣으면 그 노출과의 연관을 검정할 수 없다. 임상 기준 + 사람·장소·시간 제한으로 만든다 [[cdc-poe-l6: Step 4 Construct a working case definition]]."
  - contrast: "환자 정의는 처음부터 엄격하게?"
    point: "초기에는 민감한 정의로 문제의 규모를 잡고, 분석 단계에서 특이하게 좁힌다(위양성이 분석 결과를 흐린다). 확진·추정·의심 범주를 둔다. 새로 알려진 병은 처음부터 특이한 정의로 시작하기도 한다 [[cdc-poe-l6: Step 4 Construct a working case definition]]."
  - contrast: "관리 조치는 분석이 끝난 뒤?"
    point: "관리·예방 조치는 조사가 끝나기 전에도 시작할 수 있다 — 감염원과 전파 경로를 알게 되는 즉시 시행한다. 단계 순서는 개념상의 순서이고 여러 단계를 동시에 한다 [[cdc-poe-l6: Step 11 Implement control and prevention measures]]."
  - contrast: "명단이 분명한 소규모 모임에 환자-대조군 연구?"
    point: "참석자 명단처럼 작고 잘 정해진 집단이면 후향적 코호트로 노출군·비노출군 발병률을 비교한다(상대위험도). 집단이 불분명하고 빨리 결론내야 하면 환자-대조군 연구(교차비)를 쓴다 [[cdc-poe-l6: Step 8 Evaluate hypotheses epidemiologically]]."
  - contrast: "집단면역 임계값을 넘으면 모두 안전?"
    point: "1 − 1/R0 는 고르게 섞이고 면역이 감염을 완전히 막는다는 가정에서 나온다. 면역이 시간에 따라 약해지거나(백일해·로타바이러스) 감수성자가 한곳에 모여 있으면 전체 면역률이 임계값을 넘어도 국소 유행이 생긴다 [[randolph-2020: Establishing Herd Immunity within Populations]]."
tables:
  - id: curve
    section: "가르는 소견 — 유행 곡선의 모양"
    title: "유행 곡선 모양 → 전파 양식"
    role: differential
    span: column
    columns: ["전파 양식", "노출", "곡선 모양", "곡선에서 읽는 것"]
    rows:
      - ["공통 감염원 · 단일 노출(point source)", "같은 감염원에 짧은 시간 한 번", "가파른 상승 + 더 완만한 하강의 한 봉우리 — 모든 환자가 한 잠복기 안 [[cdc-poe-l1: Common-source outbreaks]]", "환자 발생 범위 ≈ 그 병원체의 잠복기 범위 → 노출 시점 추정 [[cdc-poe-l6: Step 6 Epidemic curve]]"]
      - ["공통 감염원 · 지속 노출(continuous)", "같은 감염원에 며칠~몇 주 이상 계속", "더 평평하고 넓은 봉우리 — 고원(plateau) [[cdc-poe-l1: Common-source outbreaks]] [[cdc-poe-l6: Step 6 Epidemic curve]]", "감염원이 아직 남아 있을 수 있다"]
      - ["공통 감염원 · 간헐 노출(intermittent)", "같은 감염원에 띄엄띄엄", "들쭉날쭉 — 노출 시기를 그대로 반영 [[cdc-poe-l1: Common-source outbreaks]] [[cdc-poe-l6: Step 6 Epidemic curve]]", "노출이 반복되는 시점"]
      - ["전파성(propagated) · 사람 간", "사람에서 사람으로(직접 접촉 · 매개체)", "약 한 잠복기 간격의 잇단 봉우리, 몇 세대 뒤 잦아든다(홍역 예: 약 11일 간격) [[cdc-poe-l1: Propagated outbreaks]]", "세대 간격 ≈ 잠복기"]
      - ["혼합(mixed)", "공통 감염원 뒤 2차 사람 간 전파", "첫 공통 감염원 봉우리 뒤 작은 봉우리들 [[cdc-poe-l1: Mixed epidemics]]", "2차 전파 차단이 필요"]
    note: "곡선 모양은 cdc-poe-l1 Lesson 1 Section 11 과 cdc-poe-l6 Lesson 6 Step 6. 바깥값(outlier)은 이른·늦은 노출이나 자료 오류를 알려 준다."
  - id: steps
    section: "선택 — 지금 어느 단계이고 다음은 무엇인가"
    title: "집단 발병 조사 단계(CDC 표 6.2)"
    role: comparison
    span: column
    columns: ["단계", "할 일", "놓치기 쉬운 점"]
    rows:
      - ["1 현장 준비", "지식·물품·보호구, 역할·기관 분담·소통 계획", "—"]
      - ["2 유행 확인", "관찰 수를 기대 수(감시 자료·지역·국가 자료)와 비교", "보고·정의 변경 등 겉보기 증가를 거른다. 중증·전파력이 크면 적은 수라도 조사"]
      - ["3 진단 확인", "임상·검사 소견 검토, 확인 검사, 환자 면담, 임상 특징 분포", "검사 오류를 걸러 관리 조치가 맞는 병을 겨누게 한다"]
      - ["4 환자 정의", "임상 기준 + 사람·장소·시간 제한, 확진·추정·의심", "조사할 노출은 넣지 않는다"]
      - ["5 사례 찾기·기록", "능동·수동 감시, 환자에게 다른 환자를 묻기, 선 목록(line listing)", "—"]
      - ["6 기술 역학", "시간(유행 곡선)·장소(점 지도·발생률 지도)·사람(나이·성·관련 요인)", "잠복기를 모르면 여러 시간 간격으로 그려 본다"]
      - ["7 가설 세우기", "병의 알려진 특성, 환자와 열린 면담, 기술 역학 양상", "자연 전파로 설명되지 않으면 의도적 원인도 고려"]
      - ["8 가설 검정", "후향적 코호트(발병률·상대위험도) 또는 환자-대조군(교차비)", "대조군 선택이 결과를 좌우한다"]
      - ["9–10 다듬기·검사실·환경 대조", "결과가 불분명하면 가설로 돌아가고, 검사실·환경 조사로 확인", "—"]
      - ["11–13 관리 · 감시 · 소통", "감염원·전파 경로를 알면 즉시 관리, 감시로 효과 확인, 결과 공유", "관리는 조사가 끝나기 전에도 시작"]
    note: "단계 이름·내용은 cdc-poe-l6 Lesson 6 Section 2 표 6.2. 순서는 개념상이며 처음 세 단계의 순서는 매우 가변적이다."
criteria:
  - id: hit
    name: 집단면역 임계값(herd immunity threshold)
    kind: 계산식
    population: "고르게 섞이고 면역이 감염을 막는다고 가정한 집단"
    statement: "임계값 = 1 − 1/R0. R0 = 완전히 감수성인 집단에 감염자 1명이 들어왔을 때 감염 기간 동안 생기는 평균 2차 감염자 수. 예: R0 4 → 0.75, R0 3 → 약 67 % [[randolph-2020: Basic Concepts of Herd Immunity]]"
    exceptions: "면역 비율이 임계값을 넘으면 실효감염재생산수(Re · Rt)가 1 아래로 내려가 유행이 줄어든다. 고른 섞임·감염 차단 면역(sterilizing immunity)이라는 가정이 깨지면(면역 약화 · 감수성자 집단) 실제 보호는 덜하다 [[randolph-2020: Establishing Herd Immunity within Populations]]"
    source: randolph-2020
    basis: current
    exams: [kmle, usmle]
sources:
  - id: cdc-poe-l1
    org: "CDC"
    title: "Principles of Epidemiology in Public Health Practice, 3rd ed. — Lesson 1 Section 11: Epidemic Disease Occurrence"
    kind: guideline
    year: 2012
    url: "https://archive.cdc.gov/www_cdc_gov/csels/dsepd/ss1978/lesson1/section11.html"
    checked_at: 2026-11-20
    checked: "CDC 보관 사이트의 Lesson 1 Section 11 쪽을 WebFetch 로 읽음 — 풍토병·유행·집단 발병·집락·범유행 정의, 공통 감염원(단일·지속·간헐), 전파성, 혼합 유행의 정의와 유행 곡선 모양(단일 노출: 가파른 상승·완만한 하강, 모든 환자가 한 잠복기 안 / 지속: 더 평평하고 넓은 봉우리 / 간헐: 노출 시기 반영 / 전파성: 약 한 잠복기 간격 봉우리, 홍역 예 약 11일 / 혼합: 공통 감염원 봉우리 뒤 2차 전파). 웹판 요약 도구로 읽었다. 판 연도(3rd ed. 2006 · 2012 갱신)는 서지 기억이라 확인 필요"
    verified: text
  - id: cdc-poe-l6
    org: "CDC"
    title: "Principles of Epidemiology in Public Health Practice, 3rd ed. — Lesson 6 Section 2: Steps of an Outbreak Investigation"
    kind: guideline
    year: 2012
    url: "https://archive.cdc.gov/www_cdc_gov/csels/dsepd/ss1978/lesson6/section2.html"
    checked_at: 2026-11-20
    checked: "CDC 보관 사이트의 Lesson 6 Section 2 쪽 앞 100,000자(전체 약 120,000자)를 WebFetch 로 읽음 — 표 6.2 의 13단계 이름과 순서, 각 단계 요점(유행 확인의 겉보기 증가 원인, 진단 확인, 환자 정의: 임상 기준+사람·장소·시간, 노출 제외, 확진·추정·의심, 초기 민감·분석 시 특이; 사례 찾기·선 목록; 유행 곡선이 알려 주는 것·모양별 전파 양식·시간 간격 선택·단일 노출 때 노출 기간 추정법; 가설; 후향적 코호트 vs 환자-대조군; 관리는 조사 완료 전에도·감염원과 경로를 알면 즉시; 감시; 소통; 단계는 개념상 순서·동시 진행). 마지막 약 20,000자는 읽지 않았다. 판 연도는 서지 기억이라 확인 필요"
    verified: text
  - id: randolph-2020
    org: "Randolph HE, Barreiro LB"
    title: "Herd Immunity: Understanding COVID-19"
    kind: review
    year: 2020
    citation: "Immunity 2020;52(5):737-741"
    doi: "10.1016/j.immuni.2020.04.012"
    pmid: "32433946"
    url: "https://pmc.ncbi.nlm.nih.gov/articles/PMC7236739/"
    checked_at: 2026-11-20
    checked: "PMC7236739 전문(PubMed MCP)을 처음부터 끝까지 읽음 — 집단면역 = 면역자가 충분할 때 감수성자가 받는 간접 보호, R0 정의(완전 감수성 집단에서 1명이 만드는 평균 2차 감염), 임계값 1 − 1/R0(R0 4 → 0.75, R0 3 → 약 67 %), Re·Rt 정의와 예방접종 목표(Re < 1), 가정(고른 섞임·감염 차단 면역), R0 는 병원체와 집단에 따라 다르다, 면역이 감염 전파를 막아야 한다, 면역 약화(백일해·로타바이러스)·감수성자 집단에서 국소 유행. 서지(권 52 · 5호 · 737–741)는 PubMed 메타데이터로 확인"
    verified: text
diagram:
  title: "집단 발병 — 유행 확인에서 관리까지"
  nodes:
    - {id: start, kind: start, text: "평소보다 환자가 많다는 보고"}
    - {id: excess, kind: decision, text: "기대치보다 실제로 많은가?"}
    - {id: base, kind: info, text: "감시 자료·지역 자료로 기대치를 구한다"}
    - {id: artifact, kind: end, text: "유행 아님 — 보고·정의·검사 변화 확인"}
    - {id: define, kind: step, text: "진단 확인 → 환자 정의 → 사례 찾기"}
    - {id: curve, kind: decision, text: "유행 곡선 모양은?"}
    - {id: point, kind: end, text: "단일 노출 — 노출 시점 역산, 공동 노출 조사"}
    - {id: cont, kind: alert, text: "지속·간헐 노출 — 감염원 즉시 차단"}
    - {id: prop, kind: end, text: "사람 간 전파 — 격리·접촉자 관리·예방접종"}
  edges:
    - {from: start, to: excess}
    - {from: excess, to: define, label: "많다"}
    - {from: excess, to: artifact, label: "아니다"}
    - {from: excess, to: base, label: "기대치 모름"}
    - {from: base, to: define, label: "초과"}
    - {from: base, to: artifact, label: "기대 범위"}
    - {from: define, to: curve}
    - {from: curve, to: point, label: "한 봉우리"}
    - {from: curve, to: cont, label: "고원·들쭉날쭉"}
    - {from: curve, to: prop, label: "잇단 봉우리"}
diagram_notes:
  - "단일 노출의 노출 시점 추정: 봉우리(또는 중앙값 환자)에서 평균 잠복기만큼, 첫 환자에서 최소 잠복기만큼 거슬러 올라간다. 두 추정이 가까우면 그 사이를 노출 기간으로 보고 양쪽을 20–50 % 넓힌다 [[cdc-poe-l6: Step 6 Epidemic curve]]."
  - "가설은 분석 역학으로 검정한다 — 작은 명단 집단은 후향적 코호트, 집단이 불분명하면 환자-대조군. 강한 용의 노출은 노출군 발병률이 높고 비노출군이 낮으며 대부분의 환자를 설명한다 [[cdc-poe-l6: Step 8 Evaluate hypotheses epidemiologically]]."
  - "사람 간 전파 유행의 관리에서 예방접종이 막을 수 있는 크기는 집단면역 임계값(1 − 1/R0)이 정한다 [[randolph-2020: Basic Concepts of Herd Immunity]]."
checks:
  - q: "결혼식 피로연 다음 날 하객 40명이 구토·설사로 왔고 환자는 하루 반 사이에 몰렸다가 서서히 줄었다. 전파 양식과 다음에 할 일은?"
    a: "공통 감염원 단일 노출(point source). 환자 정의를 세우고 하객 명단으로 후향적 코호트를 짜 음식별 발병률(상대위험도)을 비교한다."
  - q: "약 한 잠복기 간격으로 봉우리가 잇달아 나타나는 유행 곡선의 뜻은?"
    a: "사람 간 전파(propagated) — 세대마다 잠복기만큼 늦게 다음 환자가 생긴다."
  - q: "R0 가 4 인 병원체의 집단면역 임계값은?"
    a: "1 − 1/4 = 0.75, 즉 집단의 75 %가 면역이어야 지속 전파가 끊긴다(고른 섞임·감염 차단 면역 가정)."
figures_none: "유행 곡선은 개념 도식이고 실제 영상 소견이 시험 단서가 아니다"
---

## 판단 — 왜 유행 곡선을 먼저 그리나
- 유행 곡선은 규모, 시간 추세, 지금 유행이 오르는 중·봉우리·내리막 중 어디인지, 그리고 **모양으로 전파 양식**을 알려 준다 [[cdc-poe-l6: Step 6 Epidemic curve]].
- 전파 양식이 다음 조치를 정한다 — 공통 감염원이면 그 감염원을 찾아 막고, 사람 간 전파면 사람 사이의 고리를 끊는다 [[cdc-poe-l1: Common-source outbreaks]] [[cdc-poe-l1: Propagated outbreaks]].
- 곡선을 그리기 전에 **유행인지부터** 확인한다. 기대치보다 많지 않으면 조사 대상이 아니다(다만 중증·전파력이 크면 적은 수도 조사) [[cdc-poe-l6: Step 2 Establish the existence of an outbreak]].

## 기전 — 노출 방식이 곡선 모양을 만든다
- **단일 노출**: 모두 짧은 시간에 같은 감염원에 노출되므로 환자는 한 잠복기 안에 모두 생긴다. 발생 범위가 그 병원체의 잠복기 분포를 그대로 보여 준다 [[cdc-poe-l1: Common-source outbreaks]].
- **지속 노출**: 노출 날짜가 길게 퍼지고 잠복기도 겹쳐 봉우리가 넓고 평평해진다 [[cdc-poe-l1: Common-source outbreaks]].
- **사람 간 전파**: 1세대 환자가 감염력을 가진 뒤 2세대를 만들고, 그 간격이 대략 잠복기라 봉우리가 잠복기 간격으로 잇달아 선다. 감수성자가 줄면서 몇 세대 뒤 잦아든다 [[cdc-poe-l1: Propagated outbreaks]].
- **R0 와 집단면역**: R0 는 완전히 감수성인 집단에서 감염자 1명이 만드는 평균 2차 감염자 수다. 면역 비율이 1 − 1/R0 를 넘으면 실효재생산수가 1 아래로 내려가 전파가 유지되지 못한다. R0 는 병원체뿐 아니라 인구 밀도·접촉 양상에 따라 달라 임계값도 집단마다 다르다 [[randolph-2020: Basic Concepts of Herd Immunity]] [[randolph-2020: Establishing Herd Immunity within Populations]].

## 가르는 소견 — 유행 곡선의 모양
- 표가 다섯 가지 모양을 나란히 놓는다. x 축 시간 간격은 잠복기에 맞추고, 병·잠복기를 모르면 여러 간격으로 그려 양상이 가장 잘 보이는 것을 쓴다 [[cdc-poe-l6: Step 6 Epidemic curve]].
- 바깥값(outlier)은 버리지 않는다 — 감염원에 먼저·나중에 노출된 사람이거나 자료 오류일 수 있다 [[cdc-poe-l6: Step 6 Epidemic curve]].

## 선택 — 지금 어느 단계이고 다음은 무엇인가
- 표가 CDC 의 13단계를 정리한다. 시험에서 「다음 단계」는 대개 유행 확인 → 진단 확인 → 환자 정의 → 기술 역학(곡선) → 가설 → 분석의 흐름에서 묻는다 [[cdc-poe-l6: Step 2 Establish the existence of an outbreak]].
- 순서는 개념상이다 — 여러 단계를 동시에 하고, 처음 세 단계의 순서는 크게 바뀐다. 관리 조치는 감염원·경로를 아는 즉시 시행한다 [[cdc-poe-l6: Step 11 Implement control and prevention measures]].
- 분석 설계: 명단이 분명한 작은 집단은 후향적 코호트(노출·비노출 발병률, 상대위험도·기여위험도), 집단이 불분명하고 빨리 알아야 하면 환자-대조군(교차비 — 드문 병에서 상대위험도에 가깝다) [[cdc-poe-l6: Step 8 Evaluate hypotheses epidemiologically]].

## 권고와 예외
- 검사실·환경 조사는 역학적 결론을 확인하고 왜 일어났는지를 설명한다 — 역학 분석을 대신하지 않는다 [[cdc-poe-l6: Step 8 Evaluate hypotheses epidemiologically]].
- 집단면역이 실제로 생기려면 면역이 질병뿐 아니라 **전파**를 막아야 한다. 무증상 감염자가 전파하는 병원체는 임상 소견으로 면역 정도를 가늠하기 어렵다 [[randolph-2020: Establishing Herd Immunity within Populations]].
- 한국 「감염병의 예방 및 관리에 관한 법률」의 신고·역학조사 절차와 질병관리청 지침은 대조하지 않았다(검토 항목). 백신 효과를 반영한 접종 목표율 공식도 읽은 출처에 없어 싣지 않았다.

## 시험 쟁점 — 충돌·맥락·새 근거
- **Z1 맥락 · 조사 단계의 순서** — 시험 기준: CDC 표 6.2 는 현장 준비 → 유행 확인 → 진단 확인 → 환자 정의 → … 순이다 [[cdc-poe-l6: Step 2 Establish the existence of an outbreak]] / 다른 기준: 같은 자료가 처음 세 단계(준비·유행 확인·진단 확인)의 순서는 매우 가변적이라고 쓴다 [[cdc-poe-l6: Table 6.2 순서 설명]]. 국내 교과서의 단계 이름·순서는 대조하지 않았다 / 왜 다른가: 단계는 개념상의 순서이고 실제로는 동시에 진행한다 / 시험에서는: 보기 중 「유행 확인(기대치와 비교)」이 「진단 확인」과 함께 나오면 둘 다 초기 단계다 — 문항이 「가장 먼저」를 물으면 국내 교과서 순서를 확인해야 한다(검토 항목). 「관리는 분석이 끝난 뒤」는 KMLE·USMLE 모두 오답으로 본다.
