---
id: cn.cardio.heart-failure.natriuretic-peptide-echo-diagnosis
type: concept
topic: Cardiology
see_also: [cn.cardio.nyha-class.functional-assessment, cn.cardio.edema.generalized-cause, cn.cardio.jugular-venous-pulse.waveform-diagnosis]
date: 2026-11-17
updated: 2026-11-17
version: 1
outline: h257            # 기본틀 슬롯 — 해리슨 22판 264장 Heart Failure: Pathophysiology and Diagnosis
confidence: high
review_status: unreviewed
note_form: 2            # 판형 2(2026-09-25) — 기본틀 [gap] 으로 쓴 정리본(오답 연결 없음)
title: "심부전 진단 — 펩타이드로 거르고 심초음파로 나눈다"
objective: "숨참·부종 환자에서 나트륨이뇨펩타이드 값을 비만·신장·나이 같은 교란 요인과 함께 해석하고, 심초음파 박출률로 심부전을 확인·분류한다"
objective_kind: 진단
condition: 심부전(heart failure) — 박출률 감소(HFrEF)·경도 감소(HFmrEF)·보존(HFpEF)
exams: [kmle, usmle]
summary:
  - "결론: 심부전 의심이면 BNP·NT-proBNP 로 뒷받침하고 심초음파 박출률로 확인·분류한다 [[harrison-22: 264장 p.1977, p.1985]]"
  - "시험 단서: 숨참·기좌호흡(orthopnea)·발작성 야간 호흡곤란(PND)·부종 + 폐질환이 함께 있어 원인이 애매한 환자 → BNP."
  - "왜: BNP 는 심방·심실 벽 긴장(wall stress)에 분비된다 — 아주 낮으면 비만이 아닌 환자에서 심부전을 배제하는 데 쓴다 [[harrison-22: 264장 p.1985–1986]]"
  - "높이는 요인: 나이·여성·만성 콩팥병·심방세동·폐색전증·폐동맥 고혈압. 낮추는 요인: 비만 [[harrison-22: 264장 p.1985]]"
  - "심전도·흉부 X선에 심부전 진단 소견은 없다 — 원인(비대·경색·전도장애)과 다른 숨참 원인을 찾는 검사다 [[harrison-22: 264장 p.1985]]"
pitfalls:
  - contrast: "BNP 정상 = 비만 환자도 심부전 배제?"
    point: "비만에서는 나트륨이뇨펩타이드가 거짓으로 낮다. 아주 낮은 값으로 배제하는 것은 비만이 아닌 환자에서다 [[harrison-22: 264장 p.1985–1986]]"
    exception: "만성 심부전에서는 림프 배출이 늘어 흉부 X선 울혈 소견도 없을 수 있다 — 정상 X선도 배제 근거가 아니다 [[harrison-22: 264장 p.1985]]"
  - contrast: "BNP 상승 = 심부전 확진?"
    point: "BNP 는 보조 도구다. 나이·여성·만성 콩팥병, 심방세동·폐색전증·폐동맥 고혈압도 값을 올린다 — 구조·기능 이상은 심초음파로 확인한다 [[harrison-22: 264장 p.1985]]"
  - contrast: "박출률이 정상이면 심부전이 아니다?"
    point: "심부전 환자의 절반 가까이는 박출률 보존(≥50 %)이다. 박출률은 진단 여부가 아니라 유형(HFrEF·HFmrEF·HFpEF)을 나눈다 [[harrison-22: 264장 p.1977]]"
  - contrast: "심부전이 있으면 「수축기 심부전」「이완기 심부전」으로 부른다?"
    point: "박출률과 관계없이 대부분 수축·이완 이상을 함께 가져 옛 용어는 버렸다. 박출률로 HFrEF·HFmrEF·HFpEF 로 나눈다 [[harrison-22: 264장 p.1977]]"
tables:
  - id: hf-ef-class
    section: "가르는 소견 — 박출률이 유형을 나눈다"
    title: "박출률에 따른 심부전 분류"
    role: criteria
    span: column
    columns: ["유형", "좌심실 박출률(LVEF)"]
    rows:
      - ["박출률 감소 심부전(HFrEF)", "≤ 40 % [[harrison-22: 264장 p.1977]]"]
      - ["박출률 경도 감소 심부전(HFmrEF)", "41–49 % [[harrison-22: 264장 p.1977]]"]
      - ["박출률 보존 심부전(HFpEF)", "≥ 50 % — 이 범위면 수축 기능을 정상으로 본다 [[harrison-22: 264장 p.1977, p.1985]]"]
  - id: np-confounders
    section: "기전 — 벽 긴장에서 펩타이드로"
    title: "나트륨이뇨펩타이드를 흔드는 요인"
    role: differential
    span: column
    columns: ["방향", "요인"]
    rows:
      - ["올린다(심장 밖)", "나이, 여성, 만성 콩팥병 [[harrison-22: 264장 p.1985]]"]
      - ["올린다(다른 심혈관 질환)", "심방세동, 폐색전증, 폐동맥 고혈압 [[harrison-22: 264장 p.1985]]"]
      - ["낮춘다", "비만 [[harrison-22: 264장 p.1985]]"]
      - ["심부전 안에서", "HFrEF 가 HFpEF 보다 높은 경향 [[harrison-22: 264장 p.1985]]"]
criteria:
  - id: hf-universal-def
    name: 심부전 보편 정의
    kind: 진단
    population: "심부전이 의심되는 성인"
    statement: "구조·기능적 심장 이상으로 생긴 심부전 증상·징후가 있고, 나트륨이뇨펩타이드 상승 또는 심인성 폐·전신 울혈의 객관적 증거 중 하나 이상이 뒷받침할 때 [[harrison-22: 264장 p.1976]]"
    exceptions: "AHA/ACC/HFSA 는 충만·박출 장애로 생긴 증상·징후의 임상 증후군으로, ESC 는 주요 증상(숨참·발목 부종·피로)과 징후를 강조해 정의한다 [[harrison-22: 264장 p.1975]]"
    source: harrison-22
    basis: current
    exams: [kmle, usmle]
  - id: hf-np-use
    name: 나트륨이뇨펩타이드 사용
    kind: 검사 해석
    population: "숨참이 있는 외래 환자"
    statement: "BNP·NT-proBNP 는 진단의 보조 도구다 — 임상적으로 애매하거나 폐질환이 함께 있을 때 심부전 판단을 돕고, 만성 심부전에서는 중증도·예후 판정에 쓴다 [[harrison-22: 264장 p.1985]]"
    exceptions: "비만이면 거짓으로 낮은 값, 나이·여성·만성 콩팥병·심방세동·폐색전증·폐동맥 고혈압이면 상승 — 값 하나로 확진·배제하지 않는다. 절단값은 이 정리본에서 대조하지 않았다"
    source: harrison-22
    basis: current
    exams: [kmle, usmle]
sources:
  - id: harrison-22
    org: "McGraw Hill"
    title: "Harrison's Principles of Internal Medicine, 22nd ed. — Chapter 264: Heart Failure: Pathophysiology and Diagnosis"
    kind: textbook
    year: 2025
    citation: "Harrison's Principles of Internal Medicine, 22e. 264장 p.1975–1986"
    checked_at: 2026-11-17
    checked: "드라이브 22판 장별 문서 H22_264 본문 대조 — AHA/ACC/HFSA·ESC 정의(p.1975), 그림 264-1 보편 정의: 구조·기능 이상에 의한 증상·징후 + 나트륨이뇨펩타이드 상승 또는 심인성 울혈의 객관적 증거(p.1976), 박출률 ≤40 % 약 절반·보존 ≥50 %·경도 감소 41–49 %, 수축기/이완기 심부전 용어 폐기·HFrEF/HFmrEF/HFpEF 분류(p.1977), 그림 264-8 초기 평가(병력·진찰·검사·흉부 X선·심전도·심초음파 → 원인 → 위험 분류), 심첨 박동 아래·왼쪽 이동, S3 는 용적 과부하·빈맥·나쁜 예후, S4 는 고혈압 HFpEF 에서 가능·비특이, 간비대는 전신 정맥 울혈의 초기 징후, 대량 복수는 수축성 심낭염·간부전 탐색, 증상·징후는 특이도·민감도 모두 낮음, 일반 검사(대사 패널·혈구·응고·소변), 저나트륨은 예후 불량(p.1984), 흉부 X선 심흉곽비 >0.5·폐정맥 울혈·상엽 재분포·소엽간 중격 비후, 만성 심부전에서는 림프 배출 증가로 울혈 소견이 없을 수 있음, 심전도는 진단 패턴 없음 — 좌심실 비대·좌심방 확대는 HFpEF, Q 파는 허혈, 저전압+가성 경색은 아밀로이드, 전도 장애는 사르코이드·샤가스, 심방세동 최대 40 %, QRS 폭·LBBB 는 재동기화 판단, 심초음파 LVEF ≥50 % 면 수축 기능 정상, CMR 은 원인 감별, BNP·NT-proBNP 는 벽 긴장에 심방·심실에서 분비·보조 진단 도구·HFrEF > HFpEF·비만에서 거짓으로 낮은 값·외래 숨참에서 애매하거나 폐질환 동반 시 도움·중증도·예후·나이·여성·CKD·심방세동·폐색전증·폐동맥 고혈압이 올림, 관상동맥 조영은 허혈성 원인 배제(p.1985), 감별: 폐질환과 심장 원인 구분 어려움·PND 유사 증상은 기침·객담으로 풀리면 폐, 앉아야 풀리면 심장, 아주 낮은 BNP 는 비만이 아닌 환자에서 숨참의 원인으로 심부전 배제, 표 264-8 감별(p.1986). BNP 절단값은 이 장에 없다"
    verified: text
diagram:
  title: "심부전 의심 — 확인과 분류"
  nodes:
    - {id: start, kind: start, text: "숨참·기좌호흡·부종으로 심부전 의심"}
    - {id: base, kind: step, text: "병력·진찰·혈액검사·흉부 X선·심전도"}
    - {id: obese, kind: info, text: "비만·콩팥병·심방세동 여부 확인"}
    - {id: np, kind: decision, text: "BNP·NT-proBNP 가 높은가?"}
    - {id: lowrule, kind: end, text: "비만 아니면 심부전 가능성 낮음 — 다른 원인"}
    - {id: echo, kind: step, text: "심초음파 — 구조·판막·박출률"}
    - {id: ef, kind: decision, text: "좌심실 박출률은?"}
    - {id: hfref, kind: end, text: "HFrEF(≤40 %)"}
    - {id: hfmref, kind: end, text: "HFmrEF(41–49 %)"}
    - {id: hfpef, kind: end, text: "HFpEF(≥50 %) — 이완 이상·울혈 근거로"}
  edges:
    - {from: start, to: base}
    - {from: base, to: obese}
    - {from: obese, to: np}
    - {from: np, to: echo, label: "높음"}
    - {from: np, to: lowrule, label: "아주 낮음"}
    - {from: echo, to: ef}
    - {from: ef, to: hfref, label: "≤40 %"}
    - {from: ef, to: hfmref, label: "41–49 %"}
    - {from: ef, to: hfpef, label: "≥50 %"}
diagram_notes:
  - "BNP 상승은 나이·여성·만성 콩팥병·심방세동·폐색전증·폐동맥 고혈압으로도 생긴다 — 높음 갈래도 심초음파로 구조 이상을 확인한다."
  - "비만이면 BNP 가 거짓으로 낮다 — 낮아도 임상 의심이 크면 심초음파로 간다."
  - "유형을 정한 뒤 원인을 찾는다: 허혈(관상동맥 조영·CT), 침윤·염증(CMR·PET, 필요하면 심내막 생검)."
figures_none: "판단은 펩타이드 값의 교란 요인과 박출률 수치로 가린다 — 영상 소견 하나가 시험 단서가 아니다"
checks:
  - q: "BMI 38 인 62세 여자의 숨참. NT-proBNP 가 정상 범위다. 심부전을 배제할 수 있나?"
    a: "아니다. 비만은 나트륨이뇨펩타이드를 거짓으로 낮춘다 — 의심이 남으면 심초음파로 구조·박출률을 본다."
  - q: "만성 콩팥병과 심방세동이 있는 78세에서 BNP 가 높다. 그것만으로 심부전인가?"
    a: "아니다. 나이·콩팥병·심방세동 모두 BNP 를 올린다. 심초음파로 구조·기능 이상을 확인해야 한다."
  - q: "숨참·부종이 있고 심초음파 LVEF 가 55 % 다. 심부전이 아닌가?"
    a: "박출률 보존 심부전(HFpEF, ≥50 %)일 수 있다. 이완 충만 이상·좌심실 비대·펩타이드 상승·울혈 근거로 판단한다."
---

## 판단 — 왜 「펩타이드 → 심초음파」인가
- 심부전의 증상·징후는 **특이도·민감도가 모두 낮다** — 고령·심혈관 질환·고혈압·당뇨·만성 콩팥병이 있는 환자에서는 의심을 낮추지 말고 검사로 확인한다 [[harrison-22: 264장 p.1984]].
- BNP·NT-proBNP 는 **보조 도구**다. 임상이 애매하거나 폐질환이 함께 있을 때 판단을 돕고, 아주 낮으면 비만이 아닌 환자에서 숨참의 원인으로 심부전을 배제하는 데 쓴다 [[harrison-22: 264장 p.1985–1986]].
- 확인과 분류는 **심초음파**가 한다 — 심실 크기·기능, 판막, 심낭 삼출, 혈전을 빠르게 보고, 박출률로 유형을 나눈다 [[harrison-22: 264장 p.1985]].
- 흉부 X선·심전도는 진단 검사가 아니라 **원인과 다른 숨참 원인**(폐렴·COPD)을 찾는 검사다 [[harrison-22: 264장 p.1985]].

## 기전 — 벽 긴장에서 펩타이드로
BNP 와 NT-proBNP 는 심방·심실의 **벽 긴장(wall stress)** 이 늘면 분비된다 — 그래서 확장·압력 부하가 큰 HFrEF 가 HFpEF 보다 대개 높다 [[harrison-22: 264장 p.1985]]. 나트륨이뇨펩타이드는 신경호르몬 축에 맞서는 대항 조절 물질로, 네프릴리신(neprilysin)이 분해한다 [[harrison-22: 264장 p.1980]]. 값은 심장 밖 요인에도 흔들린다 — 나이·여성·만성 콩팥병은 올리고, 비만은 낮춘다. 심방세동·폐색전증·폐동맥 고혈압처럼 심방·우심실에 부하를 주는 다른 심혈관 질환도 올린다 [[harrison-22: 264장 p.1985]].

## 가르는 소견 — 박출률이 유형을 나눈다
- 심부전 환자의 약 절반이 박출률 감소(≤40 %), 나머지는 보존(≥50 %) 또는 경도 감소(41–49 %)다 [[harrison-22: 264장 p.1977]].
- 박출률과 관계없이 대부분 수축·이완 이상을 함께 가지므로 「수축기·이완기 심부전」이라는 옛 용어는 버렸다. 유형은 인구 특성·동반 질환·**치료 반응**이 달라 나눈다 [[harrison-22: 264장 p.1977]].
- 진찰: S3 는 용적 과부하·빈맥에서 들리며 심한 혈역학 장애와 나쁜 예후를 뜻한다. S4 는 비특이적이지만 고혈압성 HFpEF 에서 들릴 수 있다. 심첨 박동은 아래·왼쪽으로 밀린다 [[harrison-22: 264장 p.1984]].
- 흉부 X선: 심흉곽비 > 0.5, 폐정맥 울혈, 상엽 혈관 재분포, 소엽간 중격 비후. 만성 심부전에서는 림프 배출이 늘어 이런 소견이 없을 수 있다 [[harrison-22: 264장 p.1985]].
- 심전도는 원인의 실마리다 — 좌심실 비대·좌심방 확대는 HFpEF(고혈압·대동맥판 협착·비후성 심근병증), Q 파는 허혈, 저전압+가성 경색은 아밀로이드증, 전도 장애는 사르코이드증·샤가스병 [[harrison-22: 264장 p.1985]].

## 권고와 예외
- 숨참에서 심장·폐 원인을 가르기 어렵다. 밤에 깨는 숨참이 기침·가래로 풀리면 폐, 일어나 앉아야 풀리면 심장 쪽이다. 두 병이 함께 있으면 구분이 불가능할 수 있어, 이뇨 뒤 폐기능 검사나 심폐 운동 검사가 돕는다 [[harrison-22: 264장 p.1986]].
- 유형이 정해지면 원인을 찾는다 — 관상동맥 조영으로 되돌릴 수 있는 허혈성 원인을 배제하고, CMR 로 허혈·심근염·아밀로이드증·혈색소증을 가른다 [[harrison-22: 264장 p.1985]].
- 혈액검사: 저나트륨은 입원 시 나쁜 예후의 지표이고, 우심부전의 간 울혈은 아미노전이효소·ALP·빌리루빈을 조금 올려 담도 질환과 혼동될 수 있다 [[harrison-22: 264장 p.1984]].
- BNP·NT-proBNP 의 진단 절단값은 이 장에 없어 대조하지 않았다(검토 항목).

## 시험 쟁점 — 충돌·맥락·새 근거
- **Z1 맥락 · 심부전 정의** — 시험 기준: 구조·기능 이상에 의한 증상·징후 + 펩타이드 상승 또는 울혈의 객관적 증거(보편 정의) [[harrison-22: 264장 p.1976]] / 다른 기준: AHA/ACC/HFSA 는 충만·박출 장애의 임상 증후군, ESC 는 주요 증상과 징후 중심 [[harrison-22: 264장 p.1975]] / 왜 다른가: 학회마다 강조점이 다르고 보편 정의는 둘을 묶으려는 합의안 / 시험에서는: KMLE · USMLE 모두 「증상·징후 + 심장 구조·기능 이상 확인(심초음파)」으로 답한다.
