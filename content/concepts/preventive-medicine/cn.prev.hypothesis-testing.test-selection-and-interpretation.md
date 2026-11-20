---
id: cn.prev.hypothesis-testing.test-selection-and-interpretation
type: concept
topic: Preventive Medicine
date: 2026-11-20
updated: 2026-11-20
version: 1
outline: prev.statistics   # 기본틀 슬롯(content/outline/subjects.yaml) — 예방의학 손 슬롯 「보건통계와 가설검정」
confidence: medium
review_status: unreviewed
note_form: 2            # 판형 2(2026-09-25) — 기본틀 빈 슬롯으로 쓴 정리본(오답 연결 없음)
title: "가설검정 — 변수 종류·집단 수·짝으로 고른다"
objective: "결과 변수의 종류(범주·연속), 비교 집단 수, 짝지음 여부와 정규성으로 알맞은 통계 검정을 고른다"
objective_kind: 검사 선택
condition: 통계 검정 선택(statistical test selection) — 카이제곱 검정 · t 검정 · 분산분석 · 상관/회귀와 비모수 검정
exams: [kmle, usmle]
summary:
  - "결론: 비율은 카이제곱(짝이면 McNemar), 평균 둘은 t 검정, 셋 이상은 분산분석, 관계·예측은 상관·회귀."
  - "시험 단서: 「치료 전후 같은 환자」(짝) · 「세 연령군의 혈압」(세 집단) · 「흡연 여부와 폐암 여부」(범주×범주)."
  - "왜: 검정은 비교할 대표값(비율·평균·순위)과 관측의 독립성에 맞춰 만든다 — 짝지은 자료에 독립 검정을 쓰면 결론이 바뀐다."
  - "정규분포가 아니거나 순위 자료면 짝이 되는 비모수 검정(Mann-Whitney · Wilcoxon 부호순위 · Kruskal-Wallis)."
  - "해석: p 값은 귀무가설이 참일 확률이 아니다 — 1종 오류 = α, 2종 오류 = β = 1−검정력."
pitfalls:
  - contrast: "짝지은 자료에 독립 t 검정(또는 그 반대)?"
    point: "같은 대상을 두 시점·두 방법으로 잰 자료는 짝지은 t 검정, 서로 다른 대상 두 군은 독립 t 검정이다. 같은 수축기 혈압 자료에서 독립 t 검정은 p = 0.061, 짝지은 t 검정은 p = 0.011 로 결론이 갈렸다 — 짝이 아닌 자료에 짝 검정을 쓰면 없는 차이를 「유의」하다고 낸다 [[mishra-2019: Impact of Wrong Selection of the Statistical Methods]]."
  - contrast: "세 집단 평균을 t 검정 여러 번?"
    point: "세 집단 이상의 평균 비교는 t 검정을 확장한 분산분석(ANOVA)으로 한다 — 독립이면 일원 분산분석, 같은 대상 반복 측정이면 반복측정 분산분석 [[mishra-2019: Selection between Parametric and Nonparametric Methods]]."
  - contrast: "치료 전후 양성/음성 비율에 카이제곱?"
    point: "카이제곱·Fisher 정확 검정은 독립 집단 사이의 비율(두 범주형 변수의 연관) 비교다. 같은 대상의 전후 비율 변화는 McNemar 검정(셋 이상 짝 집단이면 Cochran Q) [[mishra-2019: Statistical Methods to Compare the Proportions]]."
  - contrast: "p = 0.03 → 귀무가설이 참일 확률 3 %?"
    point: "p 값은 귀무가설과 모든 가정이 맞다고 할 때 관찰한 만큼(또는 더) 극단적인 검정통계량이 나올 확률이다. 가설이 참일 확률도, 우연만으로 생겼을 확률도 아니다 [[greenland-2016: Common misinterpretations of single P values]]."
  - contrast: "p > 0.05 → 차이가 없다?"
    point: "p > 0.05 는 귀무가설이 자료와 어긋나지 않는 여러 가설 가운데 하나라는 뜻일 뿐이다. 작은 연구에서는 큰 효과도 유의하지 않게 나온다 — 신뢰구간이 중요한 효과 크기를 포함하는지 본다 [[greenland-2016: Common misinterpretations of single P values]]."
  - contrast: "p 가 아주 작으면 임상적으로 중요한 효과?"
    point: "큰 연구에서는 아주 작은 효과도 통계적으로 유의하다. 효과의 크기는 점추정치와 신뢰구간으로 판단한다 [[greenland-2016: Common misinterpretations of single P values]]."
tables:
  - id: compare
    section: "선택 — 검정 고르기 표"
    title: "연속·순위 자료 — 모수 검정과 비모수 짝"
    role: comparison
    span: column
    columns: ["비교 상황", "모수(정규·평균)", "비모수(비정규·순위)", "예"]
    rows:
      - ["독립 두 집단", "독립 표본 t 검정", "Mann-Whitney U(Wilcoxon 순위합)", "치료군 vs 대조군 평균 동맥압"]
      - ["짝지은 두 집단", "짝지은 t 검정", "Wilcoxon 부호순위 검정", "같은 환자 치료 전 vs 후"]
      - ["독립 세 집단 이상", "일원 분산분석", "Kruskal-Wallis H", "세 연령군의 이완기 혈압"]
      - ["짝지은 세 집단 이상", "반복측정 분산분석", "Friedman 검정", "같은 환자 3시점 측정"]
      - ["두 연속 변수의 선형 관계", "Pearson 상관계수", "Spearman 순위상관", "키와 몸무게"]
      - ["결과 하나를 독립변수로 예측", "선형 회귀(결과가 연속)", "비선형·로그선형 회귀", "나이로 혈압 예측"]
    note: "mishra-2019 표 1 과 「Type and distribution of the data used」 절(이완기 혈압·평균 동맥압 예). 「예」 칸의 키·몸무게 · 3시점 · 나이 예는 정리본이 붙인 것이다."
  - id: proportion
    section: "선택 — 검정 고르기 표"
    title: "범주 자료(비율)와 그 밖의 방법"
    role: comparison
    span: column
    columns: ["목적", "방법", "자료 조건"]
    rows:
      - ["독립 집단 사이 두 범주형 변수의 연관", "Pearson 카이제곱 · Fisher 정확 검정", "변수 범주 2개 이상"]
      - ["짝지은 집단의 비율 변화", "McNemar(2집단) · Cochran Q(3집단 이상)", "변수 범주 2개"]
      - ["범주형(이분) 결과를 예측", "로지스틱 회귀", "독립변수는 범주·연속 모두 가능"]
      - ["생존 시간 비교·예측", "Kaplan-Meier 곡선 비교 · Cox 회귀", "결과(사건 유무) + 추적 시간"]
      - ["두 측정 방법의 일치도", "kappa(명목·순위) · 급내상관계수(연속)", "같은 대상을 두 방법으로"]
    note: "mishra-2019 표 2 · 표 3 과 「Other Statistical Methods」 절."
  - id: interpret
    section: "해석 — p 값·신뢰구간·오류·검정력"
    title: "검정 결과를 읽는 말"
    role: comparison
    span: column
    columns: ["용어", "뜻", "아닌 것"]
    rows:
      - ["p 값", "모든 가정과 검정 가설이 맞을 때 관찰한 만큼 이상 극단적인 통계량이 나올 확률 — 0~1 의 연속적 적합도", "가설이 참일 확률 · 우연만으로 생겼을 확률"]
      - ["유의수준 α", "연구 전에 정하는 기준(보통 0.05) — 참인 귀무가설을 기각하는 비율(1종 오류)", "자료에서 계산하는 p 값"]
      - ["95 % 신뢰구간", "같은 방식으로 반복하면 95 % 가 참값을 포함하는 구간 — p > 0.05 인 효과 크기의 범위", "이 구간에 참값이 있을 확률 95 %"]
      - ["검정력 · β", "대립가설이 맞을 때 귀무가설을 기각할 연구 전 확률 · β(2종 오류) = 1 − 검정력", "관찰 자료로 계산해 결과를 해석하는 값"]
    note: "greenland-2016 의 「Uncertainty, probability, and statistical significance」 · 「Moving from tests to estimates」 · 「Common misinterpretations of power」 절."
diagram:
  title: "통계 검정 고르기"
  nodes:
    - {id: start, kind: start, text: "두 변수를 비교·연관 짓는 문항"}
    - {id: check, kind: info, text: "결과 변수 종류·집단 수·짝지음·정규성을 확인"}
    - {id: type, kind: decision, text: "결과 변수는 무엇인가?"}
    - {id: catpair, kind: decision, text: "같은 대상을 짝지어 쟀나?"}
    - {id: mcn, kind: end, text: "McNemar(셋 이상 Cochran Q)"}
    - {id: chi, kind: end, text: "카이제곱 · Fisher 정확 검정"}
    - {id: ngrp, kind: decision, text: "비교 집단은 몇 개인가?"}
    - {id: two, kind: end, text: "독립 t 검정 · 짝이면 짝지은 t 검정"}
    - {id: three, kind: end, text: "일원 분산분석 · 짝이면 반복측정"}
    - {id: rel, kind: end, text: "상관(Pearson) · 회귀(선형·로지스틱)"}
    - {id: np, kind: alert, text: "정규성 위반·순위 자료 → 비모수 짝 검정"}
  edges:
    - {from: start, to: check}
    - {from: check, to: type}
    - {from: type, to: catpair, label: "범주(비율)"}
    - {from: type, to: ngrp, label: "연속(평균)"}
    - {from: type, to: rel, label: "관계·예측"}
    - {from: catpair, to: mcn, label: "예"}
    - {from: catpair, to: chi, label: "아니오"}
    - {from: ngrp, to: two, label: "2개"}
    - {from: ngrp, to: three, label: "3개 이상"}
    - {from: ngrp, to: np, label: "정규성 위반"}
diagram_notes:
  - "모수 검정은 변수가 연속이고 대략 정규분포라는 가정에 기댄다. 정규분포가 아니거나 명목·순위·이산 자료면 비모수 검정을 쓴다 — 비모수는 평균 대신 중앙값·평균 순위를 비교해 이상값의 영향을 덜 받지만, 가정이 맞을 때는 모수 검정이 차이를 더 잘 찾는다 [[mishra-2019: Advantage and Disadvantages of Nonparametric Methods…]]."
  - "작은 표본(집단당 평균 15개 이하)에서는 정규성 검정이 비정규를 잘 못 잡아 아주 정규적일 때만 모수 검정을, 큰 표본에서는 반대로 아주 비정규적일 때만 비모수 검정을 권한다. t 검정·분산분석은 집단마다 관측이 2개 이상이어야 표준편차를 구한다 [[mishra-2019: Advantage and Disadvantages of Nonparametric Methods…]]."
  - "결과가 범주형이면 회귀도 로지스틱 회귀(이분 결과는 이항, 셋 이상은 다항), 연속이면 선형 회귀다 [[mishra-2019: Type and distribution of the data used]]."
checks:
  - q: "같은 고혈압 환자 30명의 약 복용 전후 수축기 혈압(정규분포)을 비교하는 검정은?"
    a: "짝지은 t 검정. 정규분포가 아니면 Wilcoxon 부호순위 검정."
  - q: "흡연자·비흡연자 사이 폐암 발생 비율을 비교하는 검정은?"
    a: "카이제곱 검정(또는 Fisher 정확 검정) — 독립 두 집단의 범주형 결과."
  - q: "검정력 80 % 인 연구에서 2종 오류 확률은?"
    a: "β = 1 − 0.80 = 0.20 — 대립가설이 맞는데 귀무가설을 기각하지 못할 연구 전 확률."
sources:
  - id: mishra-2019
    org: "Mishra P, Pandey CM, Singh U, Keshri A, Sabaretnam M"
    title: "Selection of appropriate statistical methods for data analysis"
    kind: review
    year: 2019
    citation: "Ann Card Anaesth 2019;22(3):297-301"
    doi: "10.4103/aca.ACA_248_18"
    pmid: "31274493"
    url: "https://pmc.ncbi.nlm.nih.gov/articles/PMC6639881/"
    checked_at: 2026-11-20
    checked: "PMC6639881 전문(PubMed MCP)을 처음부터 끝까지 읽음 — 검정 선택 세 요인(목적·자료 종류와 분포·짝 여부), 정규면 평균·비정규면 중앙값·범주는 비율·순위는 평균 순위, 이완기 혈압 세 연령군 = 일원 분산분석/Kruskal-Wallis, 평균 동맥압 두 군 = 독립 t/Mann-Whitney, 짝이면 짝지은 t; 모수 = 평균 비교·연속·대략 정규 가정; 표 1(한 표본·독립 두 군·짝 두 군·독립 셋 이상·짝 셋 이상·Pearson/Spearman·선형/비선형 회귀); 비율 비교는 비모수 — 독립 집단 카이제곱·Fisher, 짝 McNemar·Cochran Q, 비율 Z 검정(표 2); ICC·kappa·로지스틱·생존분석·ROC(표 3); 모수가 더 강력·비모수는 이상값에 강함·집단당 2개 이상 관측·표본 15개 기준의 정규성 판단; 표본 크기는 효과 크기와 반비례(신뢰수준 95 %·검정력 80 % 흔히); 독립 t p = 0.061 vs 짝지은 t p = 0.011 예. PMC 텍스트에서 「t」「F」 같은 기울임 글자가 일부 빠져 있어 한 표본 검정 행은 싣지 않았다"
    verified: text
  - id: greenland-2016
    org: "Greenland S, Senn SJ, Rothman KJ, Carlin JB, Poole C, Goodman SN, Altman DG"
    title: "Statistical tests, P values, confidence intervals, and power: a guide to misinterpretations"
    kind: review
    year: 2016
    citation: "Eur J Epidemiol 2016;31(4):337-50"
    doi: "10.1007/s10654-016-0149-3"
    pmid: "27209009"
    url: "https://pmc.ncbi.nlm.nih.gov/articles/PMC4877414/"
    checked_at: 2026-11-20
    checked: "PMC4877414 전문(PubMed MCP)을 처음부터 끝까지 읽음 — 검정 가설·귀무가설 정의, p 값 = 모든 모형 가정이 맞을 때 관찰값 이상 극단적인 통계량 확률(0~1 의 적합도), α 는 미리 정하는 기준이고 p 는 자료에서 계산, p > 0.05 인 효과 크기 범위 = 95 % 신뢰구간·반복 시 95 % 포함(포함 확률은 개별 구간의 성질이 아님), 단일 p 값 오해(가설 참 확률·우연만의 확률·p > 0.05 = 효과 없음·큰 연구의 작은 효과·작은 연구의 큰 효과·기각 시 5 % 오류), 검정력 = 대립가설이 맞을 때 기각할 연구 전 확률·1 − 검정력 = 2종(β) 오류, 관찰 검정력은 p 값의 변환, 80 % 검정력 두 연구가 모두 유의할 확률 64 %. PMC 텍스트에서 25개 오해의 굵은 제목 문장이 빠져 있어 오해 번호는 인용하지 않고 해설 문장만 근거로 썼다"
    verified: text
figures_none: "검정 선택과 해석 용어를 묻는 목표다 — 영상 소견이 시험 단서가 아니다"
---

## 판단 — 왜 「결과 변수」부터 보는가
- 검정 선택은 세 가지로 정한다: 연구 목적, 자료의 종류와 분포, 관측이 짝지어졌는지 [[mishra-2019: Factors Influencing Selection of Statistical Methods]].
- 결과 변수가 **범주형**이면 비율을, **연속형**이면 평균(정규) 또는 중앙값·순위(비정규)를 비교한다. 목적이 **관계·예측**이면 비교 검정이 아니라 상관·회귀다 [[mishra-2019: Type and distribution of the data used]].
- 그다음 집단 수(둘 vs 셋 이상)와 짝 여부(같은 대상 반복 측정 vs 서로 다른 대상)로 칸이 정해진다 [[mishra-2019: Observations are paired or unpaired]].

## 기전 — 검정은 대표값과 독립성에 맞춰 만든다
- 모수 검정(t 검정·분산분석·Pearson 상관·선형 회귀)은 평균과 표준편차로 유의성을 계산해, 변수가 연속이고 대략 정규분포라는 가정이 필요하다 [[mishra-2019: Concept of Parametric and Nonparametric Methods]].
- 비율을 비교하는 방법(카이제곱·Fisher·McNemar·Cochran Q)은 모수 대응이 없는 비모수 방법이다 [[mishra-2019: Statistical Methods to Compare the Proportions]].
- 짝지은 자료는 같은 사람 안의 차이를 보므로 사람 사이 변동을 빼고 계산한다 — 독립 자료에 짝 검정을 쓰거나 그 반대면 p 값이 달라져 결론이 바뀐다(혼동 항목의 p 0.061 vs 0.011) [[mishra-2019: Impact of Wrong Selection of the Statistical Methods]].
- p 값은 검정통계량(t·카이제곱 등)으로 자료와 모형 예측 사이의 거리를 재서 구한다. 검정하는 것은 귀무가설 하나가 아니라 무작위 배정·결측·분석 선택까지 포함한 **모형 전체**다 [[greenland-2016: Uncertainty, probability, and statistical significance]].

## 선택 — 검정 고르기 표
- 연속·순위 자료는 첫 표, 범주 자료와 생존·일치도는 둘째 표로 고른다.
- 표본 크기에 정해진 최소는 없다 — 신뢰수준(보통 95 %)·검정력(보통 80 %)·효과 크기로 정하며, 효과 크기가 클수록 필요한 표본은 작다. 표본이 모자라면 검정력이 낮아 실제 차이도 유의하지 않게 나온다 [[mishra-2019: Minimum Sample Size Required for Statistical Methods]].

## 해석 — p 값·신뢰구간·오류·검정력
- 셋째 표가 용어의 뜻과 흔한 오해를 나란히 놓는다.
- 귀무가설이 참인데 기각하면 1종 오류다. α = 0.05 는 그런 기각이 **많은 연구를 반복할 때** 일어나는 비율이지, 이번 한 번 기각이 틀렸을 확률이 아니다 — 귀무가설이 참이면 기각한 그 판단은 100 % 틀린 것이다 [[greenland-2016: Common misinterpretations of single P values]].
- 95 % 신뢰구간 바깥의 효과 크기는 그 크기를 검정하면 p ≤ 0.05 가 나오는 값들이다 — 그래서 귀무값(차이 0, 비 1)이 구간 밖이면 귀무가설 검정도 p ≤ 0.05 다 [[greenland-2016: Moving from tests to estimates]].
- 검정력은 연구를 설계할 때 쓰는 값이다. 관찰 자료로 계산한 검정력은 p 값을 바꿔 쓴 것이라 결과 해석에 새 정보를 주지 않는다 [[greenland-2016: Common misinterpretations of power]].

## 권고와 예외
- 「유의/비유의」 두 갈래로만 보고하지 말고 정확한 p 값과 신뢰구간을 함께 본다. 매우 작을 때(예: 0.001 미만)만 부등호로 적는다 [[greenland-2016: Common misinterpretations of single P values]].
- 분석을 결과의 p 값에 따라 골라 보고하면(선택 보고·출판 비뚤림) p 값과 신뢰구간의 뜻 자체가 무너진다 [[greenland-2016: A statistical model is much more than an equation with Greek letters]].
- 카이제곱 대신 Fisher 정확 검정을 쓰는 기대빈도 기준(예: 기대빈도가 작은 칸)은 읽은 출처에 수치가 없어 싣지 않았다(검토 항목).
- 국내 예방의학 교과서의 검정 이름 표기와 대조하지 않았다(검토 항목).

## 시험 쟁점 — 충돌·맥락·새 근거
- **Z1 맥락 · 「p > 0.05 이면 차이가 없다」** — 시험 기준: p > 0.05 는 「귀무가설을 기각하지 못한다」이지 「차이가 없음을 증명했다」가 아니다 [[greenland-2016: Common misinterpretations of single P values]] / 다른 기준: 고전적 이분법(Neyman-Pearson)은 α 를 미리 정하고 기각/채택 두 갈래로 판정한다 — 같은 글이 이 이분법을 해석에 해롭다고 본다 [[greenland-2016: Uncertainty, probability, and statistical significance]] / 왜 다른가: 판정 규칙(설계 단계의 오류율 관리)과 증거의 크기(효과 크기·신뢰구간)를 한 숫자로 섞기 때문이다 / 시험에서는: KMLE 는 「귀무가설 기각 여부」로 답하는 문항이 흔할 것으로 보고 그렇게 답하되 「귀무가설 채택 = 효과 없음 증명」 보기는 고르지 않는다 · USMLE 는 신뢰구간이 귀무값을 포함하는지로 유의성을 판정하는 문항에 같은 규칙을 쓴다(두 시험의 출제 경향은 이 정리본의 판단이다 — 검토 항목).
</content>
</invoke>
