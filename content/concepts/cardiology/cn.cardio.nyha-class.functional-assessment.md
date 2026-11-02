---
id: cn.cardio.nyha-class.functional-assessment
type: concept
topic: Cardiology
see_also: []
date: 2026-11-03
updated: 2026-11-03
version: 1
outline: h236
confidence: medium
review_status: unreviewed
note_form: 2
title: "NYHA 기능 등급 — 증상을 부르는 활동 수준"
objective: "심장질환 환자의 증상이 어느 정도의 활동에서 나타나는지로 NYHA 기능 등급(I~IV)을 매긴다"
objective_kind: 진단
condition: 심장질환의 기능 장애(New York Heart Association functional classification)
exams: [kmle, usmle]
summary:
  - "결론: 일상 활동에 증상 없음 I · 일상 활동에 증상 II · 일상보다 가벼운 활동에 증상 III · 안정 시 증상 IV."
  - "시험 단서: 「몇 층·몇 걸음에서 숨이 찬가」, 안정 시 증상 유무(NYHA functional class)."
  - "왜: 등급은 진단명·심초음파가 아니라 증상을 부르는 활동의 양으로 정한다 — 심한 병변도 증상이 없으면 I."
  - "같은 호흡곤란도 평소 활동량·치료 중인지에 따라 무게가 다르다 — 최적 이뇨제 중의 증상이 더 무겁다."
  - "등급(장애의 정도)이 검사의 범위·속도와 치료 전략을 정한다."
pitfalls:
  - contrast: "안정 시 무증상 = I 등급?"
    point: "안정 시 증상이 없는 것은 I~III 모두 같다. 일상보다 가벼운 활동(몇 걸음 평지)에서 증상이 나면 안정 시 무증상이어도 III 이다."
    cites: ["harrison-22: 243장 p.1842"]
  - contrast: "심한 판막 협착 = 높은 등급?"
    point: "등급은 해부학적 중증도가 아니라 기능 장애다. 해부학적으로 심한 판막질환도 증상이 없으면 I — 이때는 6~12개월마다 임상·비침습 검사로 추적한다."
    cites: ["harrison-22: 243장 p.1842", "harrison-22: 243장 p.1843"]
  - contrast: "II vs III — 경계는?"
    point: "일상 활동(평소 하던 계단·걷기)에서 증상이면 II, 그보다 가벼운 활동에서 증상이면 III. 「숨이 차다」만으로는 등급을 못 매긴다 — 활동의 양과 속도를 묻는다."
    cites: ["harrison-22: 243장 p.1842"]
tables:
  - id: nyha
    section: "가르는 소견 — 어느 활동에서 증상이 나나"
    title: "NYHA 기능 등급"
    role: criteria
    span: column
    columns: ["등급", "신체 활동 제한", "증상이 나는 때"]
    rows:
      - ["I", "제한 없음", "일상 활동에서 증상 없음 [[harrison-22: 243장 p.1842]]"]
      - ["II", "약간 제한", "일상 활동에서 증상 [[harrison-22: 243장 p.1842]]"]
      - ["III", "뚜렷한 제한", "일상보다 가벼운 활동에서 증상, 안정 시 무증상 [[harrison-22: 243장 p.1842]]"]
      - ["IV", "불편 없이 어떤 활동도 못 함", "안정 시에도 증상 [[harrison-22: 243장 p.1842]]"]
criteria:
  - id: nyha-class
    name: NYHA 기능 분류
    kind: 진단 기준
    population: "심장질환이 알려졌거나 의심되는 환자"
    statement: "I 일상 활동에 증상 없음 · II 일상 활동이 증상을 일으킴(약간 제한) · III 일상보다 가벼운 활동이 증상을 일으키나 안정 시 무증상(뚜렷한 제한) · IV 불편 없이 어떤 활동도 못 하고 안정 시 증상 [[harrison-22: 243장 p.1842]]"
    exceptions: "해부학적 중증도가 아니라 기능 장애를 나타낸다 — 같은 등급이라도 평소 활동량·치료 여부를 함께 본다 [[harrison-22: 243장 p.1842]]"
    source: harrison-22
    basis: current
    exams: [kmle, usmle]
sources:
  - id: harrison-22
    org: "McGraw Hill"
    title: "Harrison's Principles of Internal Medicine, 22nd ed. — Chapter 243: Approach to the Patient with Possible Cardiovascular Disease"
    kind: textbook
    year: 2025
    citation: "Harrison's Principles of Internal Medicine, 22e. 243장 p.1841–1843"
    checked_at: 2026-11-03
    checked: "드라이브 22판 장별 문서 H22_243 본문 대조 — 활동 시 나타나고 안정 시 사라지는 호흡곤란·흉부 불편이 심장질환의 특징, 반대 양상은 드묾(p.1841) · NYHA 완전 진단 요소(원인·해부·생리·기능 장애), Table 243-1 NYHA 기능 분류 I~IV, 장애의 중증도가 검사의 범위·속도와 치료 전략을 정함, 기능 장애 평가: 증상 전 활동의 수준과 속도, 평소 활동량(잘 단련된 마라톤 선수의 2층 호흡곤란이 좌식 생활자의 1층 호흡곤란보다 의미가 클 수 있음), 최적 이뇨제 치료 중의 증상이 더 무거움, 6개월~1년 전에 하던 일과 비교(p.1842) · 해부학적으로 심한 무증상·경증 판막질환은 6~12개월마다 임상·비침습 검사로 추적(p.1843). ACC/AHA 심부전 단계(A~D)는 이 장에 없다(대조하지 않음)"
    verified: text
diagram:
  title: "NYHA 기능 등급 — 증상을 부르는 활동으로"
  nodes:
    - {id: start, kind: start, text: "심장질환 환자의 호흡곤란·피로·흉부 불편"}
    - {id: rest, kind: decision, text: "안정 시에도 증상이 있나?"}
    - {id: ask, kind: info, text: "몇 층·몇 걸음에서, 어떤 속도로 증상이 나나 묻는다"}
    - {id: ordinary, kind: decision, text: "일상 활동에서 증상이 나나?"}
    - {id: less, kind: decision, text: "일상보다 가벼운 활동에서도 나나?"}
    - {id: c1, kind: end, text: "I 등급 — 제한 없음"}
    - {id: c2, kind: end, text: "II 등급 — 약간 제한"}
    - {id: c3, kind: end, text: "III 등급 — 뚜렷한 제한"}
    - {id: c4, kind: alert, text: "IV 등급 — 안정 시 증상"}
  edges:
    - {from: start, to: rest}
    - {from: rest, to: c4, label: "예"}
    - {from: rest, to: ordinary, label: "아니오"}
    - {from: rest, to: ask, label: "모르겠음"}
    - {from: ask, to: c4, label: "안정 시 증상"}
    - {from: ask, to: ordinary, label: "활동 시만"}
    - {from: ordinary, to: c1, label: "아니오"}
    - {from: ordinary, to: less, label: "예"}
    - {from: less, to: c3, label: "예"}
    - {from: less, to: c2, label: "아니오"}
diagram_notes:
  - "평소 활동량으로 보정한다 — 잘 단련된 사람의 2층 호흡곤란이 좌식 생활자의 1층 호흡곤란보다 의미가 클 수 있다 [[harrison-22: 243장 p.1842]]."
  - "최적 용량의 이뇨제·심부전 치료 중에도 남는 증상은 치료 없이 생긴 같은 증상보다 무겁다 [[harrison-22: 243장 p.1842]]."
  - "진행은 6개월~1년 전에 하던 일 중 지금 못 하는 것을 물어 본다 [[harrison-22: 243장 p.1842]]."
checks:
  - q: "평지를 몇 걸음만 걸어도 숨이 차지만 앉아 있으면 편하다. NYHA 등급은?"
    a: "III. 일상보다 가벼운 활동에서 증상이 나고 안정 시에는 없다."
  - q: "중증 대동맥판 협착이 있으나 증상이 없다. NYHA 등급과 할 일은?"
    a: "I. 등급은 기능 장애로 매긴다. 해부학적으로 심한 판막질환은 6~12개월마다 임상·비침습 검사로 추적한다."
variants:
  - id: v1
    context: "같은 목표, 다른 맥락 — 안정 시 무증상이라는 단서에 끌리지 않게"
    stem: "72세 여자가 확장성 심근병증으로 외래에 왔다. 최근 석 달 사이 집 안에서 화장실까지 걸어가거나 옷을 갈아입을 때 숨이 차서 쉬어야 한다. 의자에 앉아 있거나 누워 있을 때는 숨이 차지 않는다. 석 달 전에는 동네 시장까지 천천히 다녀올 수 있었다. 혈압 112/70 mmHg, 맥박 84회/분이다. 이 환자의 현재 NYHA 기능 등급은?"
    choices: ["A. I 등급", "B. II 등급", "C. III 등급", "D. IV 등급", "E. 안정 시 무증상이라 등급을 매길 수 없다"]
    answer: "C"
    explanation: "화장실까지 걷기·옷 갈아입기는 일상보다 가벼운 활동이다. 그 활동에서 증상이 나고 안정 시에는 없으므로 III 등급이다. 안정 시 증상이 있어야 IV 이고, 안정 시 무증상은 I~III 의 공통점이라 등급을 가르지 못한다."
    kind: application
figures_none: "기능 등급은 증상과 활동량으로 매긴다 — 영상 소견이 시험 단서가 아니다"
---

## 판단 — 왜 활동의 양이 등급을 정하나
- 심근·관상동맥 기능은 안정 시에는 충분해도 활동 중에는 모자랄 수 있다 — 그래서 심장 증상은 **활동 시 나타나고 안정 시 사라진다** [[harrison-22: 243장 p.1841]].
- 등급은 「숨이 차다」가 아니라 **증상 전 활동의 수준과 속도**로 매긴다. 계단 두 층을 뛰어오른 뒤의 호흡곤란과 평지 몇 걸음 뒤의 호흡곤란은 장애의 크기가 전혀 다르다 [[harrison-22: 243장 p.1842]].
- 안정 시 증상은 IV 만의 소견이다. 안정 시 무증상은 I~III 를 가르지 못한다.
- 기능 장애의 중증도가 검사의 범위·속도와 치료 전략을 정한다 [[harrison-22: 243장 p.1842]].

## 기전 — 공급·수요 불균형에서 증상으로
심장 증상은 주로 심근 허혈(산소 공급과 수요의 불균형), 수축·이완 장애, 혈류 폐쇄(판막 협착), 비정상 리듬에서 온다 [[harrison-22: 243장 p.1841]]. 펌프 기능이 떨어지면 피로와 함께 기능이 떨어진 심실 상류의 혈관 내 압력이 올라 말초 부종이나 폐울혈·호흡곤란이 생긴다. 활동은 산소 수요와 심박출 요구를 늘리므로, 여유가 줄어들수록 더 가벼운 활동에서 증상이 나타난다 — NYHA 등급은 이 여유의 크기를 활동량으로 잰 것이다.

## 가르는 소견 — 어느 활동에서 증상이 나나
- 일상 활동의 기준은 환자 자신이다: 평소 하던 일(출근길 계단, 장보기)에서 증상이 나면 II, 그보다 가벼운 일(집 안 걷기, 옷 입기)에서 나면 III.
- 평소 활동량을 함께 본다 — 잘 단련된 마라톤 선수의 2층 호흡곤란이 좌식 생활자의 1층 호흡곤란보다 의미가 클 수 있다 [[harrison-22: 243장 p.1842]].
- 호흡곤란·흉부 불편·부종·실신은 심장 밖 원인(폐질환·비만·불안, 신장·간질환, 신경 질환)에서도 나므로, 등급을 매기기 전에 그 증상이 심장 때문인지를 진찰과 비침습 검사로 확인한다 [[harrison-22: 243장 p.1841]].

## 선택 — 등급을 쓰는 곳
- NYHA 의 완전한 심장 진단은 원인 · 해부학적 이상 · 생리적 장애(부정맥·심부전·허혈) · **기능 장애** 네 가지를 함께 적는다 — 기능 등급은 그 마지막 칸이다 [[harrison-22: 243장 p.1841–1842]].
- 진행은 6개월~1년 전에 하던 일 가운데 지금 못 하는 것을 물어 가늠한다 [[harrison-22: 243장 p.1842]].
- 해부학적으로 심한 판막질환이 무증상·경증이면 6~12개월마다 임상·비침습 검사로 추적한다 — 심실 기능 악화의 초기 징후가 증상 전 수술의 신호일 수 있다 [[harrison-22: 243장 p.1843]].

## 권고와 예외
- 치료 맥락으로 보정한다: 최적 용량의 이뇨제·심부전 치료를 받는데도 남은 부종·호흡곤란은 치료 없이 생긴 같은 증상보다 무겁다 [[harrison-22: 243장 p.1842]].
- 등급은 증상의 보고에 기대므로 같은 환자도 치료에 따라 등급이 오르내린다.

## 시험 쟁점 — 충돌·맥락·새 근거
- 해당 없음(대조: 해리슨 22판 243장 p.1841~1843). ACC/AHA 심부전 단계(A~D)와의 관계는 이 장에 없어 다루지 않았다(검토 항목).
