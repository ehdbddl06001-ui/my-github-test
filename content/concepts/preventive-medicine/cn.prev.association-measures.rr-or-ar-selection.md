---
id: cn.prev.association-measures.rr-or-ar-selection
type: concept
topic: Preventive Medicine
date: 2026-11-20
updated: 2026-11-20
version: 1
outline: prev.epi-measures   # 기본틀 슬롯(content/outline/subjects.yaml) — 예방의학 손 슬롯 「역학 지표 — 유병률·발생률·위험도」
confidence: medium
review_status: unreviewed
note_form: 2            # 판형 2(2026-09-25) — 기본틀 빈 슬롯으로 쓴 정리본(오답 연결 없음)
title: "역학 지표 — 설계가 쓸 수 있는 지표를 정한다"
objective: "2×2 표와 연구 설명에서 발생률·유병률·상대위험도·교차비·기여위험도를 계산하고, 연구 설계에 맞는 연관성 지표(코호트 = 상대위험도, 환자-대조군 = 교차비)를 고른다"
objective_kind: 검사 선택
condition: 역학 지표(measures of frequency and association) — 발생률(incidence) · 유병률(prevalence) · 상대위험도(risk ratio) · 교차비(odds ratio) · 기여위험도(risk difference)
figures_none: "영상 소견이 아니라 2×2 표와 계산이 시험 단서다 — 표로 충분하다"
exams: [kmle, usmle]
summary:
  - "결론: 노출군·비노출군을 따라가 위험을 잰 코호트는 상대위험도, 환자·대조군을 골라 노출을 본 연구는 교차비다."
  - "시험 단서: 「환자 100명과 대조군 200명」처럼 연구자가 수를 정했으면 위험(a/(a+b))을 구할 수 없다(odds ratio = ad/bc)."
  - "왜: 대조군 수는 연구자가 정하고 원 인구 크기를 모르니 위험·위험비가 없다 — 교차비만 남는다."
  - "드문 질환이면 교차비 ≈ 상대위험도. 기여위험도 = 위험 차, 기여위험분율 = 위험 차 ÷ 노출군 위험."
  - "유병률 = 기존+새 환자, 발생률 = 새 환자만. 완치 없이 생존만 늘면 유병률이 오른다."
pitfalls:
  - contrast: "환자-대조군 연구에서 상대위험도를 계산?"
    point: "대조군 수는 연구자가 정하고 환자가 나온 인구의 크기를 대개 모르므로, 전형적 환자-대조군 연구에서는 위험·발생률·위험비·율비를 계산할 수 없다. 교차비(ad/bc)가 선택 지표다 [[cdc-epi-lesson3: Section 5 — Odds ratio]]."
  - contrast: "교차비는 언제나 상대위험도와 같다?"
    point: "질병이 드물 때만 교차비가 상대위험도의 적절한 근삿값이다. CDC 의 예(위험 5 % 대 1 %)에서 상대위험도 5.0, 교차비 5.2 로 벌어지기 시작한다 [[cdc-epi-lesson3: Section 5 — Odds ratio, Table 3.15]]."
  - contrast: "유병률이 높다 = 발생률이 높다?"
    point: "유병률은 발생률과 이환 기간을 함께 반영한다. 유병률이 높은 것은 발생률이 높거나, 완치 없이 오래 생존하거나, 둘 다일 수 있다. 낮은 유병률은 낮은 발생률·빠른 사망·빠른 회복을 뜻할 수 있다 [[cdc-epi-lesson3: Section 2 — Prevalence]]."
  - contrast: "발생률 분모에 이미 병이 있는 사람도?"
    point: "발생률(위험)의 분모는 관찰 시작 시점의 인원이고, 그 병이 생길 수 있는 「위험 인구」로 한정한다 — 이미 병이 있거나 걸릴 수 없는 사람은 뺀다 [[cdc-epi-lesson3: Section 2 — Incidence proportion]]."
  - contrast: "상대위험도가 크면 공중보건 영향도 크다?"
    point: "영국 의사 코호트에서 흡연의 율비는 폐암 14.6, 관상동맥질환 1.61 이었지만 율 차는 폐암 232, 관상동맥질환 382(10만 명·년당)로 관상동맥질환이 더 컸다. 비(ratio)는 연관의 세기, 차(difference)는 영향의 크기다 [[strobe-ee-2007: Box 7]]."
tables:
  - id: measures
    section: "선택 — 설계마다 쓸 수 있는 지표"
    title: "2×2 표 지표 — 행 = 노출, 열 = 질병(a·b / c·d)"
    role: criteria
    span: column
    columns: ["지표", "공식", "무엇을 말하나", "쓸 수 있는 설계"]
    rows:
      - ["발생 위험(발생비율·발병률)", "노출군 a/(a+b), 비노출군 c/(c+d) — 분모 = 시작 시점 위험 인구 [[cdc-epi-lesson3: Section 2]]", "처음에 병이 없던 인구에서 새로 생긴 비율", "코호트(닫힌 코호트) [[strobe-ee-2007: Box 1]]"]
      - ["발생률(인년 율)", "새 환자 수 ÷ 각자 관찰된 시간의 합 [[cdc-epi-lesson3: Section 2]]", "시간을 분모에 직접 넣은 발생", "코호트(열린 코호트는 율·율비만) [[strobe-ee-2007: Box 1]]"]
      - ["유병률", "기존+새 환자 ÷ 같은 시기 인구 [[cdc-epi-lesson3: Section 2]]", "한 시점(시점)·기간(기간) 동안 병을 가진 비율", "단면 연구 [[strobe-ee-2007: Box 1]]"]
      - ["상대위험도(위험비·RR)", "[a/(a+b)] ÷ [c/(c+d)] — 1.0 같음, >1 노출군 위험 증가, <1 감소 [[cdc-epi-lesson3: Section 5]]", "연관의 세기", "코호트 · 무작위 대조 시험"]
      - ["교차비(OR)", "(a/b) ÷ (c/d) = ad/bc [[cdc-epi-lesson3: Section 5]]", "환자군·대조군의 노출 오즈 비 — 드문 질환에서 RR 근사", "환자-대조군(선택 지표) [[cdc-epi-lesson3: Section 5]]"]
      - ["기여위험도(위험 차)", "노출군 위험 − 비노출군 위험 [[cdc-epi-lesson3: Section 6]]", "노출로 더 생긴 절대 위험(초과 위험)", "위험을 구할 수 있는 설계(코호트·시험)"]
      - ["기여위험분율", "(노출군 위험 − 비노출군 위험) ÷ 노출군 위험 × 100 % [[cdc-epi-lesson3: Section 6]]", "노출군 환자 중 노출 탓인 비율", "같음 — 단일 위험 요인을 가정"]
    note: "공식은 cdc-epi-lesson3 Section 2·5·6, 설계별로 구할 수 있는 지표는 strobe-ee-2007 Box 1·7 과 CDC Section 5(환자-대조군에서 위험비 불가). 「쓸 수 있는 설계」의 상대위험도·기여위험도 칸은 위험을 직접 잰다는 정의에서 내가 이은 것이다."
diagram:
  title: "연구 설명에서 지표 고르기"
  nodes:
    - {id: start, kind: start, text: "연구 설명 + 2×2 표"}
    - {id: sample, kind: decision, text: "무엇을 기준으로 뽑았나?"}
    - {id: info, kind: info, text: "표본 추출·시간 순서를 다시 읽는다"}
    - {id: cc, kind: step, text: "교차비 ad/bc — 위험·RR 계산 불가"}
    - {id: cs, kind: end, text: "유병률 · 유병률비 — 시간 순서 불확실"}
    - {id: risk, kind: decision, text: "무엇을 묻나?"}
    - {id: rr, kind: end, text: "상대위험도 = 위험 ÷ 위험"}
    - {id: ar, kind: end, text: "기여위험도 = 위험 − 위험, 분율 = 차 ÷ 노출 위험"}
    - {id: rare, kind: decision, text: "질병이 드문가?"}
    - {id: orrr, kind: end, text: "교차비를 상대위험도 근삿값으로 읽는다"}
    - {id: noapprox, kind: alert, text: "교차비를 상대위험도로 바꿔 읽지 않는다"}
  edges:
    - {from: start, to: sample}
    - {from: sample, to: cc, label: "질병 유무"}
    - {from: sample, to: cs, label: "한 시점 전원"}
    - {from: sample, to: risk, label: "노출 후 추적"}
    - {from: sample, to: info, label: "불분명"}
    - {from: info, to: cc, label: "환자·대조군"}
    - {from: info, to: risk, label: "추적 코호트"}
    - {from: risk, to: rr, label: "연관의 세기"}
    - {from: risk, to: ar, label: "초과 위험"}
    - {from: cc, to: rare}
    - {from: rare, to: orrr, label: "드묾"}
    - {from: rare, to: noapprox, label: "흔함"}
diagram_notes:
  - "환자-대조군 연구의 교차비는 대조군을 어떻게 뽑았는지에 따라 위험비·율비·(유병) 교차비로 해석된다 — 열린 코호트에서 표본을 뽑은 연구는 율비를 직접 추정한다 [[strobe-ee-2007: Box 1]]. 시험의 「드문 질환 가정」은 그중 위험비로 읽을 때의 조건이다."
  - "단면 연구는 코호트처럼 노출군별 유병률을 비교하거나 환자-대조군처럼 노출 오즈를 비교해 분석할 수 있지만, 노출이 질병보다 먼저였는지 정하기 어렵다(선천·유전 노출은 예외) [[strobe-ee-2007: Box 1]]."
  - "기여위험분율은 하나의 위험 요인이 그 병을 일으킨다고 가정한다 — 여러 요인이 상호작용하면 맞지 않을 수 있다 [[cdc-epi-lesson3: Section 6]]."
checks:
  - q: "노출군 2,000명 중 100명, 비노출군 8,000명 중 80명이 발병했다. 상대위험도·교차비·기여위험도·기여위험분율은?"
    a: "위험 5 %·1 % → RR 5.0, OR = (100×7,920)÷(1,900×80) = 5.2, 기여위험도 4 %(100명당 4명), 기여위험분율 = 4÷5 = 80 %."
  - q: "폐암 환자 200명과 건강한 대조군 400명의 과거 흡연을 비교했다. 보고할 연관성 지표와 그 이유는?"
    a: "교차비. 대조군 수를 연구자가 정했고 원 인구 크기를 모르므로 위험·상대위험도를 계산할 수 없다."
  - q: "완치는 못 하지만 생존을 늘리는 새 치료가 보급되면 그 병의 발생률과 유병률은?"
    a: "발생률은 그대로(새 환자 수는 변하지 않음), 유병률은 오른다(이환 기간이 길어짐)."
sources:
  - id: cdc-epi-lesson3
    org: "U.S. Centers for Disease Control and Prevention"
    title: "Principles of Epidemiology in Public Health Practice, 3rd ed. (SS1978) — Lesson 3: Measures of Risk"
    kind: textbook
    year: 2006
    citation: "CDC. Principles of Epidemiology in Public Health Practice, Third Edition (2006, 2011 갱신). Lesson 3, Sections 1·2·5·6 (archive.cdc.gov 보관판)"
    url: "https://archive.cdc.gov/www_cdc_gov/csels/dsepd/ss1978/lesson3/section5.html"
    checked_at: 2026-11-20
    checked: "archive.cdc.gov 보관판 Lesson 3 Section 1(비·비율·율 정의 — 「율」을 시간 단위 측정에만 쓰는 학자도 있음, 발병률은 비율), Section 2(발생비율 = 새 환자 ÷ 시작 시점 인구, 분모는 위험 인구로 한정 · 인년 발생률 = 새 환자 ÷ 관찰 시간 합 · 유병률 = 기존+새 환자, 시점/기간 유병률 · 유병률은 발생률과 이환 기간에 달림 — 높은 유병률 = 높은 발생률 또는 완치 없는 긴 생존, 낮은 유병률 = 낮은 발생률·빠른 사망·빠른 회복 · 만성질환은 발병 시점을 정하기 어려워 유병률을 잰다), Section 5(위험비 정의·1.0/>1/<1 해석·예시 · 율비 · 교차비 = ad/bc(교차곱 비) · 드문 질환이면 교차비가 위험비의 근삿값 · 표 3.15 RR 5.0 vs OR 5.2 · 「대조군 수는 연구자가 정하고 원 인구 크기를 모르므로 환자-대조군에서 위험·율·위험비·율비 계산 불가」, 교차비가 환자-대조군의 선택 지표), Section 6(기여위험분율 공식·흡연 폐암 예 87.7 %·단일 위험 요인 가정 · 백신 효과 = 1 − 위험비 · 분자를 위험 차·초과 위험이라 부름)를 WebFetch 로 읽음. 판 연도는 과정 첫 쪽(「Book originally published: October 2006 · updated: November 2011」)에서 확인"
    verified: text
  - id: strobe-ee-2007
    org: "Vandenbroucke JP, von Elm E, Altman DG, et al. (STROBE Initiative)"
    title: "Strengthening the Reporting of Observational Studies in Epidemiology (STROBE): explanation and elaboration"
    kind: consensus
    year: 2007
    citation: "PLoS Med 2007;4(10):e297"
    doi: "10.1371/journal.pmed.0040297"
    pmid: "17941715"
    url: "https://pmc.ncbi.nlm.nih.gov/articles/PMC2020496/"
    checked_at: 2026-11-20
    checked: "PMC2020496 전문(PubMed MCP) Box 1(코호트 = 노출을 먼저 재고 결과 발생을 추적, 닫힌 코호트는 위험·율·위험비·율비, 열린 코호트는 율·율비 · 환자-대조군 = 환자·대조군의 노출 오즈 비, 표본 추출에 따라 위험비·율비·유병 교차비로 해석, 대부분 열린 코호트에서 뽑아 율비 직접 추정 · 단면 = 한 시점 전원, 유병률 비교 또는 노출 오즈 비교, 노출의 시간 선후를 정하기 어려움)과 Box 7(누적 발생 vs 발생률, 시점·기간 유병률, 상대위험 = 위험비·율비, 영국 의사 흡연 율비 폐암 14.6·관상동맥질환 1.61 vs 율 차 232·382/10만 인년, 비 지표는 원인 연구용 연관의 세기, 인구기여분율은 용어가 통일되지 않음)을 읽음"
    verified: text
---

## 판단 — 왜 설계부터 보는가
- 같은 2×2 표라도 **표본을 어떻게 뽑았는지**가 쓸 수 있는 지표를 정한다. 노출군·비노출군을 정해 결과를 추적한 코호트는 위험(누적 발생)과 위험비·율비를 직접 계산한다 [[strobe-ee-2007: Box 1]].
- 환자-대조군 연구에서는 대조군 수를 연구자가 정하고 원 인구 크기를 대개 모른다 — 그래서 위험·율·위험비를 구할 수 없고 교차비가 선택 지표다 [[cdc-epi-lesson3: Section 5 — Odds ratio]].
- 질병이 드물면 교차비가 위험비의 적절한 근삿값이다 [[cdc-epi-lesson3: Section 5 — Odds ratio]].
- 「얼마나 강한가」(비)와 「얼마나 더 생기나」(차)는 다른 질문이다 — 비가 큰 노출이 차는 더 작을 수 있다 [[strobe-ee-2007: Box 7]].

## 기전 — 빈도에서 연관으로
- **발생(incidence)** 은 새 환자만 센다. 처음에 병이 없던 인구에서 생긴 비율이 발생비율(incidence proportion, 위험·발병률)이고, 분모는 시작 시점의 위험 인구다. 관찰 시간이 사람마다 다르면 분모에 인년(person-time)을 넣은 발생률(incidence rate)을 쓴다 [[cdc-epi-lesson3: Section 2]].
- **유병(prevalence)** 은 새 환자와 기존 환자를 모두 센다(시점 유병률·기간 유병률). 유병률은 발생과 이환 기간을 함께 반영한다 — 그래서 발병 시점을 정하기 어려운 만성질환(당뇨·골관절염)에서는 유병률을 잰다 [[cdc-epi-lesson3: Section 2]].
- **연관(association)** 은 두 집단의 빈도를 비교한 것이다. 위험끼리 나누면 위험비, 율끼리 나누면 율비, 오즈끼리 나누면 교차비다 [[cdc-epi-lesson3: Section 5]]. 위험끼리 빼면 위험 차(초과 위험)이고, 그것을 노출군 위험으로 나누면 기여위험분율이다 [[cdc-epi-lesson3: Section 6]].

## 선택 — 설계마다 쓸 수 있는 지표
- 표가 지표마다 공식·뜻·설계를 나란히 놓는다. 계산은 행 = 노출, 첫 열 = 질병인 표준 배치를 먼저 확인한다 [[cdc-epi-lesson3: Section 5 — Table 3.12A]].
- 예: 노출군 2,000명 중 100명(5 %), 비노출군 8,000명 중 80명(1 %) → 위험비 5.0, 교차비 5.2 [[cdc-epi-lesson3: Section 5 — Table 3.15]]. 같은 숫자로 위험 차 4 %, 기여위험분율 80 %(내 계산).
- 백신 효과는 1 − 위험비, 곧 백신 접종군에서 줄어든 질병의 비율이다 [[cdc-epi-lesson3: Section 6 — Vaccine efficacy]].

## 권고와 예외
- 상대 지표(비)는 연관의 세기를 보여 원인 연구에 가장 쓸모 있고, 인과가 확인된 뒤에 절대 지표로 옮겨 공중보건 정책의 영향을 가늠한다 [[strobe-ee-2007: Box 7]].
- 인구기여분율(population attributable fraction)은 정의·용어가 통일되지 않았다 — 이 정리본은 공식을 싣지 않는다 [[strobe-ee-2007: Box 7]].
- 유병률 ≈ 발생률 × 이환 기간 같은 정량 관계식은 읽은 출처에 없어 싣지 않았다(검토 항목).
- 국내 예방의학 교과서의 한국어 지표 이름(「기여위험도」·「기여위험분율」 등)과의 대응은 대조하지 않았다(검토 항목).

## 시험 쟁점 — 충돌·맥락·새 근거
- **Z1 맥락 · 교차비 ≈ 상대위험도의 조건** — 시험 기준: 질병이 드물 때 교차비가 위험비에 근사한다 [[cdc-epi-lesson3: Section 5 — Odds ratio]] / 다른 기준: 교차비가 무엇을 추정하는지는 대조군 표본 추출 방식에 달려 있어, 열린 코호트에서 뽑은 환자-대조군 연구는 율비를 직접 추정한다 [[strobe-ee-2007: Box 1]] / 왜 다른가: CDC 는 위험비로 읽을 때를, STROBE 는 표본 추출 설계 전체를 말한다 / 시험에서는: KMLE·USMLE 모두 「드문 질환이면 OR ≈ RR」로 답한다(내 판단 — 문항 대조 안 함).
- **Z2 맥락 · 「율(rate)」이라는 말** — 시험 기준: 발병률(attack rate)·유병률(prevalence rate)은 이름에 rate 가 붙어도 비율(proportion)이다 [[cdc-epi-lesson3: Section 1 — Rate]] / 다른 기준: 시간 단위로 표현한 측정에만 「율」을 쓰는 역학자도 있다 [[cdc-epi-lesson3: Section 1 — Rate]] / 왜 다른가: 관행 용어와 엄밀한 정의의 차이 / 시험에서는: 분모에 시간(인년)이 있으면 발생률, 사람 수만 있으면 발생비율·유병률로 읽는다.
