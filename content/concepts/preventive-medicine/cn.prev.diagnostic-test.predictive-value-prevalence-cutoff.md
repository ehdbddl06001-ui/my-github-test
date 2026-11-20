---
id: cn.prev.diagnostic-test.predictive-value-prevalence-cutoff
type: concept
topic: Preventive Medicine
see_also: [Internal Medicine]
date: 2026-11-20
updated: 2026-11-20
version: 1
outline: prev.test-validity   # 기본틀 슬롯(content/outline/subjects.yaml) — 예방의학 손 슬롯 「검사의 타당도」
confidence: medium
review_status: unreviewed
note_form: 2            # 판형 2(2026-09-25) — 기본틀 빈 슬롯으로 쓴 정리본(오답 연결 없음)
title: "검사 타당도 — 유병률은 예측도만, 기준점은 둘 다"
objective: "2×2 표에서 민감도·특이도·예측도·우도비를 계산하고, 유병률이나 판정 기준점이 바뀔 때 어느 지표가 어느 쪽으로 움직이는지 고른다"
objective_kind: 검사 선택
condition: 진단·선별검사의 타당도(validity) — 민감도(sensitivity) · 특이도(specificity) · 예측도(predictive value) · 우도비(likelihood ratio)
exams: [kmle, usmle]
summary:
  - "결론: 유병률이 바뀌면 예측도만 움직이고(양성예측도는 같은 방향), 기준점이 바뀌면 민감도·특이도가 반대로 움직인다."
  - "시험 단서: 같은 검사를 선별(무증상)과 진료(증상) 집단에 쓸 때 양성예측도(PPV)·음성예측도(NPV) 비교."
  - "왜: 민감도·특이도는 질병 유무로 나눈 세로 칸의 비율, 예측도는 검사 결과로 나눈 가로 칸의 비율이다."
  - "우도비: LR+ = 민감도/(1−특이도), LR− = (1−민감도)/특이도 — 사전확률과 함께 써야 사후확률이 된다."
  - "예외: 중증 환자가 많은 집단에서는 민감도도 달라진다 — 민감도·특이도가 유병률과 완전히 무관하지는 않다."
pitfalls:
  - contrast: "민감도 vs 양성예측도"
    point: "민감도는 질병이 있는 사람 가운데 양성 비율(TP/(TP+FN)), 양성예측도는 양성인 사람 가운데 질병 비율(TP/(TP+FP))이다. 분모가 다르다 — 민감도가 높아도 위양성이 많으면 양성 결과가 질병을 뜻하지 않는다 [[trevethan-2017: Defining Sensitivity and PPV]]."
  - contrast: "특이도 높은 검사가 음성 → 배제?"
    point: "배제(rule out)는 민감도가 매우 높은 검사의 음성(SnNout), 확진(rule in)은 특이도가 매우 높은 검사의 양성(SpPin)이다. 거꾸로 짝지으면 「역의 혼동」이다 [[harrison-22: 4장 p.24]] [[trevethan-2017: Uses and Misuses of Sensitivity and Specificity]]."
  - contrast: "유병률이 낮아지면 민감도·특이도도 떨어진다?"
    point: "2×2 표 계산에서 유병률은 예측도만 바꾼다. 유병률이 낮으면 특이도가 높아도 위양성 수가 진양성을 넘어 양성예측도가 크게 떨어진다 — 특이도 99.995 % 의 HIV 선별에서도 유병률 0.01 % 이면 양성의 HIV 가능성이 67 % 였다 [[harrison-22: 4장 p.25]]."
  - contrast: "기준점을 올리면 민감도·특이도 둘 다 오른다?"
    point: "기준점을 엄격하게(예: 올림) 하면 민감도는 내려가고 특이도는 오른다. 느슨하게 하면 반대다 — 이 맞교환을 그린 것이 ROC 곡선이다 [[harrison-22: 4장 p.24]]."
  - contrast: "예측도 = 검사의 고유한 정확도?"
    point: "예측도는 그 표본의 유병률로 계산된 확률이라, 유병률이 같은 집단에만 옮겨 쓸 수 있다. 해리슨은 그래서 「양성/음성 뒤 사후확률」이라는 말을 권한다 [[harrison-22: 4장 p.24]]."
tables:
  - id: formulas
    section: "기전 — 세로 칸과 가로 칸"
    title: "2×2 표에서 나오는 지표"
    role: tests
    span: column
    columns: ["지표", "식", "분모(누구 가운데)", "유병률에 따라"]
    rows:
      - ["민감도", "TP/(TP+FN) — 위음성률 = 1−민감도", "질병 있는 사람", "표 계산에서는 그대로"]
      - ["특이도", "TN/(TN+FP) — 위양성률 = 1−특이도", "질병 없는 사람", "표 계산에서는 그대로"]
      - ["양성예측도", "TP/(TP+FP)", "검사 양성인 사람", "유병률↑ → 오른다"]
      - ["음성예측도", "TN/(TN+FN)", "검사 음성인 사람", "유병률↑ → 내려간다"]
      - ["LR+ · LR−", "민감도/(1−특이도) · (1−민감도)/특이도", "질병 있는 쪽 확률 ÷ 없는 쪽 확률", "그대로 — 사전확률과 따로 곱한다"]
    note: "식은 harrison-22 4장 표 4-1 · p.25, 예측도 정의는 trevethan-2017. 「유병률에 따라」 칸은 아래 계산 예(정리본이 만든 숫자)로 Bayes 식에서 나온 방향이다."
  - id: worked
    section: "가르는 계산 — 유병률과 기준점을 바꿔 보기"
    title: "1,000명 계산 예(정리본이 만든 숫자)"
    role: comparison
    span: column
    columns: ["상황", "TP · FN · FP · TN", "PPV", "NPV"]
    rows:
      - ["민감도 90 %·특이도 90 %, 유병률 50 %", "450 · 50 · 50 · 450", "90 %", "90 %"]
      - ["같은 검사, 유병률 10 %", "90 · 10 · 90 · 810", "50 %", "98.8 %"]
      - ["같은 검사, 유병률 1 %", "9 · 1 · 99 · 891", "8.3 %", "99.9 %"]
      - ["유병률 10 %, 기준점을 올려 민감도 70 %·특이도 98 %", "70 · 30 · 18 · 882", "79.5 %", "96.7 %"]
    note: "첫 줄은 해리슨의 예(사전확률 0.50·민감도·특이도 0.90 → 양성 뒤 0.90)와 같다 [[harrison-22: 4장 p.24]]. 나머지 줄은 같은 식에 숫자만 바꿔 넣은 계산이다. LR+ 는 앞 세 줄 모두 9, LR− 는 0.11 이다 [[harrison-22: 4장 p.25]]."
diagram:
  title: "지표 문항 — 무엇이 바뀌었나"
  nodes:
    - {id: start, kind: start, text: "검사 지표를 묻는 문항"}
    - {id: table, kind: info, text: "2×2 표를 세운다 — 열 = 질병 유무, 행 = 검사 결과"}
    - {id: what, kind: decision, text: "바뀐 것은 무엇인가?"}
    - {id: prev, kind: decision, text: "유병률이 어느 쪽으로?"}
    - {id: up, kind: end, text: "PPV 오름 · NPV 내림 · 민감도·특이도·LR 그대로"}
    - {id: down, kind: end, text: "PPV 내림 · NPV 오름 · 민감도·특이도·LR 그대로"}
    - {id: cut, kind: decision, text: "기준점을 엄격하게 했나?"}
    - {id: strict, kind: end, text: "민감도↓ · 특이도↑ — 위양성↓, 위음성↑"}
    - {id: lax, kind: end, text: "민감도↑ · 특이도↓ — 위양성↑, 위음성↓"}
    - {id: spec, kind: alert, text: "집단의 중증도가 다르면 민감도도 바뀐다"}
  edges:
    - {from: start, to: table}
    - {from: table, to: what}
    - {from: what, to: prev, label: "유병률"}
    - {from: what, to: cut, label: "판정 기준점"}
    - {from: what, to: spec, label: "대상 집단"}
    - {from: prev, to: up, label: "올랐다"}
    - {from: prev, to: down, label: "내렸다"}
    - {from: cut, to: strict, label: "엄격"}
    - {from: cut, to: lax, label: "느슨"}
diagram_notes:
  - "기준점을 엄격하게 하면 위양성이 줄어 PPV 는 대개 오르고 NPV 는 내려간다 — 표의 계산 예(유병률 10 %)에서 PPV 50 → 79.5 %, NPV 98.8 → 96.7 %. 예측도는 기준점·대상 집단·기준 검사를 바꾸면 함께 바뀐다 [[trevethan-2017: Assessing Desirable Predictive Values…]]."
  - "입원·증상·의뢰 집단은 유병률뿐 아니라 진행된 질병의 비율도 높아 민감도가 더 높게, 외래 집단은 특이도가 더 높게 나오기 쉽다 [[harrison-22: 4장 p.26]]."
  - "검사를 이어서 할 때 앞 검사의 사후확률을 다음 검사의 사전확률로 쓰는 것은 두 검사가 조건부 독립일 때만 맞다 [[harrison-22: 4장 p.26]]."
checks:
  - q: "유병률 10 %, 민감도 90 %·특이도 90 % 인 검사를 1,000명에게 했다. 양성예측도는?"
    a: "TP 90, FP 90 → 90/180 = 50 %. 유병률 50 % 일 때(90 %)보다 낮다."
  - q: "민감도 90 %·특이도 55 % 인 검사의 양성 우도비는?"
    a: "0.90/(1−0.55) = 2.0. 민감도가 높아도 특이도가 낮으면 LR+ 가 작아 양성이 진단 확률을 크게 올리지 못한다."
  - q: "선별검사의 판정 기준점을 낮추면(느슨하게) 민감도·특이도는?"
    a: "민감도는 오르고 특이도는 내려간다 — 위음성이 줄고 위양성이 는다."
sources:
  - id: harrison-22
    org: "McGraw Hill (Loscalzo J, Fauci AS, Kasper DL, et al., eds.)"
    title: "Harrison's Principles of Internal Medicine, 22nd ed."
    kind: textbook
    year: 2025
    url: "https://accessmedicine.mhmedical.com/book.aspx?bookid=3541"
    checked_at: 2026-11-20
    checked: "22판 4장 Decision-Making in Clinical Medicine 드라이브 문서(H22_4)에서 p.23 끝~p.26 「Quantitative Methods / Measures of Disease Probability and Bayes' Rule / Applications to Diagnostic Testing in CAD」 를 읽음 — 표 4-1(TP·FP·FN·TN, 민감도 TP/(TP+FN), 위음성률 1−민감도, 특이도 TN/(TN+FP), 위양성률 1−특이도), SnNout·SpPin, 기준점을 엄격하게 하면 민감도↓·특이도↑, ROC 곡선(민감도 vs 1−특이도, 면적 0.5~1.0), 기준점 선택은 치료의 이득·해와 유병률에 따름(p.24); Bayes 식(사전확률·민감도·위양성률), 사전확률 0.50·민감도·특이도 0.90 → 0.90, 예측도 대신 사후확률이라는 말을 권함(p.24); LR+ = 민감도/(1−특이도), 0.90/0.10 = 9, 대부분 1.5~20, >10 은 확진, 민감도 90 %·특이도 55 % → 2.0, LR− = (1−민감도)/특이도, <0.10 은 배제, 0.11 예, 선별에서는 사전확률이 낮아 특이도가 중요 — HIV 첫 헌혈 여성 특이도 99.995 %·유병률 0.01 % → 67 %, 사전확률 30~70 % 일 때 변화가 가장 큼(p.25); 조건부 독립 가정, 민감도·특이도가 유병률 무관이라는 가정은 흔히 틀림(1혈관 30 % vs 3혈관 80 %), 입원 집단 민감도↑·외래 특이도↑(p.26)"
    verified: text
  - id: trevethan-2017
    org: "Trevethan R"
    title: "Sensitivity, Specificity, and Predictive Values: Foundations, Pliabilities, and Pitfalls in Research and Practice"
    kind: review
    year: 2017
    citation: "Front Public Health 2017;5:307"
    doi: "10.3389/fpubh.2017.00307"
    pmid: "29209603"
    url: "https://pmc.ncbi.nlm.nih.gov/articles/PMC5701930/"
    checked_at: 2026-11-20
    checked: "PMC5701930 전문(PubMed MCP)을 처음부터 끝까지 읽음 — 민감도는 기준 검사 양성(a·c 칸), PPV 는 선별 양성(a·b 칸), 특이도는 b·d, NPV 는 c·d 칸에 근거한다는 정의; 민감도↔PPV·특이도↔NPV 혼동과 「역의 혼동」; SnNout·SpPin 은 매우 높을 때만; 네 지표는 검사의 엄격도와 표본의 유병률에 따라 바뀜; 예측도가 너무 높거나 낮으면 기준점·표본·기준 검사를 바꿔 조정할 수 있고 그러면 민감도·특이도도 바뀜. PMC 텍스트에서 식(그림 1의 공식)이 빠져 있어 식은 해리슨 표 4-1 로 확인했다"
    verified: text
figures_none: "수치·식·지표의 방향을 묻는 목표다 — 영상 소견이 시험 단서가 아니다"
---

## 판단 — 왜 「무엇이 바뀌었나」부터 보는가
- 지표 문항은 **분모가 무엇인가**로 갈린다. 민감도·특이도는 질병 유무(기준 검사)로 나눈 집단 안의 비율이고, 예측도는 검사 결과로 나눈 집단 안의 비율이다 [[trevethan-2017: Defining Sensitivity and PPV]] [[harrison-22: 4장 p.24]].
- 그래서 **유병률**이 바뀌면 질병 있는 쪽과 없는 쪽의 사람 수 비가 바뀌어 예측도가 움직이고, **판정 기준점(cutoff)** 이 바뀌면 한 집단 안의 양성·음성 비율이 바뀌어 민감도와 특이도가 반대로 움직인다 [[harrison-22: 4장 p.24]].
- 개인에게 「양성이니 병이 있을 확률은?」을 답하는 지표는 예측도(사후확률)다. 민감도·특이도는 기준 검사에 견준 검사의 성질이다 [[trevethan-2017: Summary Regarding Definitions]].

## 기전 — 세로 칸과 가로 칸
- 기준 검사(reference/gold standard)로 질병 유무를 정하고 같은 사람에게 새 검사를 해 2×2 표의 네 칸(TP·FP·FN·TN)을 채운다. 대상은 실제로 그 검사를 쓸 사람들과 닮아야 하고, 기준 검사가 일부에만 시행되면 추정이 치우친다 [[harrison-22: 4장 p.23]].
- 사전확률(pretest probability)은 보통 그 집단의 유병률이나 임상 맥락으로 정한다. Bayes 식은 사전확률·민감도·위양성률로 양성 뒤 사후확률(= 양성예측도)을 계산한다: 사후확률 = (사전확률 × 민감도) ÷ [(사전확률 × 민감도) + (1 − 사전확률) × 위양성률] [[harrison-22: 4장 p.24]].
- 식에서 사전확률이 작아지면 분모의 위양성 항이 커져 양성예측도가 떨어진다. 같은 이유로 음성 쪽에서는 위음성 사람이 줄어 음성예측도가 오른다(표의 계산 예).
- 우도비(likelihood ratio)는 같은 결과가 질병 있는 사람에서 나올 확률을 없는 사람에서 나올 확률로 나눈 값이라, 사전확률과 따로 검사의 판별력을 나타낸다. 의학 검사의 LR+ 는 대부분 1.5~20 이고, >10 이면 대개 특이도가 높아 확진에, LR− <0.10 이면 대개 민감도가 높아 배제에 쓴다 [[harrison-22: 4장 p.25]].

## 가르는 계산 — 유병률과 기준점을 바꿔 보기
- 표의 앞 세 줄은 같은 검사(민감도·특이도 90 %)를 유병률 50 → 10 → 1 % 집단에 쓴 것이다. 민감도·특이도·우도비는 그대로인데 PPV 는 90 → 50 → 8.3 % 로 떨어지고 NPV 는 오른다.
- 선별(무증상) 상황은 사전확률이 특히 낮아 특이도가 중요해진다. 정확한 검사(LR+ 10)라도 사전확률 20 % 에서는 양성 하나로 확진 범위(예: 80 %)에 이르지 못한다 [[harrison-22: 4장 p.25]].
- 넷째 줄은 같은 유병률에서 기준점을 올린 것이다. 민감도↓·특이도↑ 로 위양성이 줄어 PPV 가 오르고, 위음성이 늘어 NPV 가 내려간다.
- 검사가 진단을 가장 크게 바꾸는 때는 사전확률이 30~70 % 로 가장 불확실할 때다 [[harrison-22: 4장 p.25]].

## 선택 — 기준점은 이득과 해로 정한다
- 치료가 안전하고 이득이 크며 검사 위험이 낮으면 민감도 높은 기준점(ROC 곡선 오른쪽 위), 치료의 해가 크면 특이도 높은 기준점(왼쪽 아래)을 고른다(예: 신생아 페닐케톤뇨증 선별 vs 암 항암치료) [[harrison-22: 4장 p.24]].
- ROC 곡선(receiver operating characteristic curve)은 기준점마다 민감도(y)와 1−특이도(x)를 찍은 것이고, 곡선 아래 면적은 0.5(동전 던지기)~1.0(완벽한 검사)이다 [[harrison-22: 4장 p.24]].
- 유병률도 기준점 선택에 들어간다 — 유병률이 낮으면 위양성의 해(예: 결혼 전 HIV 검사) 또는 위음성의 해(예: 헌혈자 HIV 검사)에 더 무게가 실린다 [[harrison-22: 4장 p.24]].

## 권고와 예외
- 검사를 설명할 때는 네 지표를 모두, 기준 검사와 표본의 유병률과 함께 보고해야 해석할 수 있다 [[trevethan-2017: The Importance of Full Disclosure of Information in Research]].
- 예측도가 높지 않아도 되는 상황이 있다 — 확인 검사가 싸고 쉬우면 낮은 양성예측도를 받아들일 수 있고, 질병이 심각·전염성·조기 치료 이득이 크면 높은 음성예측도가 필요하다 [[trevethan-2017: Assessing Desirable Predictive Values…]].
- 우도비와 사전확률로 사후확률을 구하는 오즈(odds) 형식 계산은 원문을 읽지 못해 싣지 않았다(검토 항목) — 확률 형식 Bayes 식만 실었다.
- 국내 예방의학 교과서의 용어(「타당도」 아래 지표 묶음)와 대조하지 않았다(검토 항목).

## 시험 쟁점 — 충돌·맥락·새 근거
- **Z1 맥락 · 민감도·특이도는 유병률과 무관한가** — 시험 기준: 2×2 표 계산 문항에서는 유병률이 바뀌어도 민감도·특이도·우도비는 그대로, 예측도만 바뀐다 [[harrison-22: 4장 p.24]] / 다른 기준: 해리슨은 「민감도·특이도가 유병률과 무관하다」는 가정이 흔히 틀린다고 쓴다 — 운동부하검사 민감도는 1혈관 질환 약 30 %, 3혈관 질환 약 80 % [[harrison-22: 4장 p.26]] / 왜 다른가: 실제 집단은 유병률이 높을 때 중증 환자 비율도 높아(스펙트럼) 민감도가 함께 오른다. 표 계산은 같은 질병 스펙트럼을 가정한다 / 시험에서는: KMLE·USMLE 모두 숫자를 주고 유병률만 바꾸면 「예측도만 변한다」로 답하고, 「입원 vs 외래 집단에서 민감도가 다른 이유」를 물으면 스펙트럼으로 답한다(이 구분은 정리본의 판단이다).
</content>
</invoke>
