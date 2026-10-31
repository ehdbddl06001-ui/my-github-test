---
id: cn.cardio.systolic-murmur.dynamic-auscultation
type: concept
topic: Cardiology
see_also: []
date: 2026-11-01
updated: 2026-11-01
version: 1
outline: h42
confidence: medium
review_status: unreviewed
note_form: 2
title: "수축기 잡음 — 손 조작으로 원인을 가른다"
objective: "수축기 잡음이 발살바·서기·쪼그려 앉기·손쥐기에 어떻게 변하는지로 폐쇄성 비후성 심근병증·승모판 탈출증과 대동맥판 협착·승모판 역류를 가른다"
objective_kind: 감별
condition: 수축기 잡음의 동적 청진(dynamic auscultation) — 폐쇄성 비후성 심근병증(HOCM)·승모판 탈출증(MVP)·대동맥판 협착(AS)·승모판 역류(MR)
exams: [kmle, usmle]
summary:
  - "결론: 발살바·일어서기에 커지는 수축기 잡음은 HOCM 또는 MVP — 나머지 대부분은 작아진다."
  - "시험 단서: 젊은 운동선수의 흉골 좌연 수축기 잡음, 발살바(Valsalva)에 커지고 쪼그려 앉으면(squatting) 작아짐."
  - "왜: 심실이 작아질수록 유출로 폐쇄(HOCM)와 판막 탈출(MVP)이 심해진다 — 다른 잡음은 흐름이 줄어 작아진다."
  - "손쥐기(handgrip)로 후부하를 올리면 MR·VSD 는 커지고 AS·HOCM 은 작아지거나 그대로다."
  - "HOCM 과 MVP 는 조작 반응이 같다 — 좌심실 비대(HOCM) vs 비구출성 클릭(MVP)으로 가른다."
pitfalls:
  - contrast: "대동맥판 협착 vs 폐쇄성 비후성 심근병증"
    point: "둘 다 구출성 수축기 잡음이고 손쥐기에 작아진다. 발살바·서기에 AS 는 작아지고 HOCM 은 커진다. HOCM 은 경동맥 맥박 상승이 빠르고, 심한 AS 는 작고 늦다(parvus et tardus)."
    cites: ["harrison-22: 44장 p.285", "harrison-22: 44장 p.290"]
  - contrast: "HOCM vs 승모판 탈출증 — 둘 다 발살바에 커지면?"
    point: "조작만으로는 못 가른다. 심전도·초음파의 좌심실 비대면 HOCM, 비구출성 클릭이 있으면 MVP 다."
    cites: ["harrison-22: 44장 p.285"]
  - contrast: "들숨에 커지는 잡음 = 왼쪽?"
    point: "들숨에 커지는 것은 오른쪽 잡음(삼첨판 역류·폐동맥판)이다. 왼쪽 잡음은 그대로이거나 작아진다."
    cites: ["harrison-22: 44장 p.289"]
tables:
  - id: maneuvers
    section: "가르는 소견 — 조작별 반응"
    title: "조작에 따른 수축기 잡음 변화"
    role: differential
    span: column
    columns: ["조작(혈역학)", "커진다", "작아진다"]
    rows:
      - ["발살바 긴장기·일어서기(전부하↓)", "HOCM · MVP(더 길어짐)", "대부분(AS·MR 등) [[harrison-22: 44장 p.290]]"]
      - ["쪼그려 앉기(전부하·후부하↑)", "흐름이 느는 잡음(원문 미대조)", "HOCM · MVP(클릭이 S1 에서 멀어짐) [[harrison-22: 44장 p.290]]"]
      - ["손쥐기·혈압대 압박(후부하↑)", "MR · VSD · AR(확장기)", "AS · HOCM(또는 변화 없음) [[harrison-22: 44장 p.289]]"]
      - ["기외수축 다음 박동", "AS 등 유출로 폐쇄", "MR 은 일정 [[harrison-22: 44장 p.285]]"]
      - ["들숨", "오른쪽 잡음(TR·PR)", "왼쪽 잡음은 그대로·감소 [[harrison-22: 44장 p.289]]"]
criteria:
  - id: hocm-murmur
    name: 폐쇄성 비후성 심근병증 잡음
    kind: 진찰 소견
    population: "수축기 잡음 환자"
    statement: "흉골 좌연~첨부의 중기 수축기 잡음, 대개 3도 이하. 전부하·후부하를 줄이거나(발살바·서기·혈관확장제) 수축력을 올리면 커지고, 전부하·후부하를 올리거나(쪼그려 앉기·다리 들기·수액·승압제) 베타차단제로 수축력을 줄이면 작아진다 [[harrison-22: 44장 p.285]]"
    exceptions: "경동맥 상승은 빠르고 정상 크기, 드물게 이봉맥. 확진은 경흉부 심초음파 [[harrison-22: 44장 p.285]]"
    source: harrison-22
    basis: current
    exams: [kmle, usmle]
sources:
  - id: harrison-22
    org: "McGraw Hill"
    title: "Harrison's Principles of Internal Medicine, 22nd ed. — Chapter 44: Approach to the Patient with a Heart Murmur"
    kind: textbook
    year: 2025
    citation: "Harrison's Principles of Internal Medicine, 22e. 44장 p.284–290"
    checked_at: 2026-11-01
    checked: "드라이브 22판 장별 문서 H22_044 본문 대조 — Table 44-1 잡음 원인(p.284) · AS 잡음은 기외수축 다음 박동에 커지고 MR 은 일정, 심한 AS 의 parvus et tardus · HOCM 잡음 위치·3도 이하·전부하/후부하 감소와 수축력 증가에 커짐, 쪼그려 앉기·다리 들기·수액·승압제·베타차단제에 작아짐, 경동맥 상승 빠름, LVH, 확진 TTE · MVP 와 조작 반응이 같아 LVH·클릭으로 구분(p.285) · MVP 서기/쪼그려 앉기 반응(p.286) · 들숨에 오른쪽 잡음 커짐, 손쥐기·일과성 동맥 폐쇄에 MR·VSD 커지고 AS·HOCM 작아지거나 그대로, Table 44-2(p.289) · 발살바 긴장기에 대부분 작아지나 MVP·HOCM 은 커짐, 쪼그려 앉기에 작아짐, 다리 들기(p.290)"
    verified: text
diagram:
  title: "수축기 잡음 — 조작으로 가르기"
  nodes:
    - {id: start, kind: start, text: "수축기 잡음이 들린다"}
    - {id: insp, kind: decision, text: "들숨에 커지는가?"}
    - {id: right, kind: end, text: "오른쪽 잡음(삼첨판·폐동맥판)"}
    - {id: valsalva, kind: decision, text: "발살바·일어서기에 커지는가?"}
    - {id: test, kind: info, text: "발살바·서기·쪼그려 앉기를 시킨다"}
    - {id: lvh, kind: decision, text: "좌심실 비대인가, 비구출성 클릭인가?"}
    - {id: hocm, kind: end, text: "폐쇄성 비후성 심근병증"}
    - {id: mvp, kind: end, text: "승모판 탈출증"}
    - {id: grip, kind: decision, text: "손쥐기에 커지는가?"}
    - {id: mr, kind: end, text: "승모판 역류·심실중격결손"}
    - {id: as, kind: end, text: "대동맥판 협착 쪽"}
  edges:
    - {from: start, to: insp}
    - {from: insp, to: right, label: "예"}
    - {from: insp, to: valsalva, label: "아니오"}
    - {from: valsalva, to: lvh, label: "커짐"}
    - {from: valsalva, to: grip, label: "작아짐"}
    - {from: valsalva, to: test, label: "안 해 봄"}
    - {from: test, to: lvh, label: "커짐"}
    - {from: test, to: grip, label: "작아짐"}
    - {from: lvh, to: hocm, label: "비대"}
    - {from: lvh, to: mvp, label: "클릭"}
    - {from: grip, to: mr, label: "커짐"}
    - {from: grip, to: as, label: "작아짐·그대로"}
diagram_notes:
  - "쪼그려 앉기는 전부하와 후부하를 함께 올려 HOCM·MVP 잡음을 작고 짧게 만든다. 쪼그려 앉지 못하면 다리 들기 — HOCM 은 작아지나 MVP 에는 효과가 적다."
  - "AS 와 MR 이 첨부에서 헷갈리면 기외수축 다음 박동을 듣는다 — AS 는 커지고 MR 은 일정하다."
  - "어느 쪽이든 원인과 중증도는 경흉부 심초음파로 확인한다."
checks:
  - q: "발살바에 커지고 쪼그려 앉으면 작아지는 수축기 잡음 둘은?"
    a: "폐쇄성 비후성 심근병증과 승모판 탈출증 — 심실이 작아질수록 폐쇄·탈출이 심해진다."
  - q: "손쥐기에 커지는 수축기 잡음은?"
    a: "승모판 역류·심실중격결손. 후부하가 오르면 역방향 흐름이 늘어난다. AS·HOCM 은 작아지거나 그대로."
variants:
  - id: v1
    context: "같은 목표의 적용 — 젊은 운동선수의 수축기 잡음"
    stem: "19세 남자 대학 농구 선수가 운동 전 검진에서 심잡음이 들려 왔다. 최근 운동 중 어지러운 적이 한 번 있었다. 흉골 좌연 아래쪽에서 3/6도 중기 수축기 잡음이 들리고, 누운 자세에서 일어서면 커지며 쪼그려 앉으면 작아진다. 비구출성 클릭은 없고, 경동맥 맥박 상승은 빠르다. 심전도에서 좌심실 비대 소견이 있다. 가장 가능성 높은 진단은?"
    choices: ["A. 대동맥판 협착", "B. 승모판 탈출증", "C. 폐쇄성 비후성 심근병증", "D. 심실중격결손", "E. 무해성 잡음"]
    answer: "C"
    explanation: "일어서기(전부하 감소)에 커지고 쪼그려 앉기(전부하·후부하 증가)에 작아지는 수축기 잡음은 HOCM 과 MVP 둘뿐이다. 클릭이 없고 좌심실 비대가 있어 HOCM 이다. 대동맥판 협착은 일어서면 작아지고 경동맥 상승이 늦다."
    kind: application
figures_none: 청진 조작에 따른 소리 변화가 단서 — 판독할 영상 소견이 시험 단서가 아니다
---

## 판단 — 왜 조작 반응이 원인을 가르나
- 대부분의 잡음은 **흐름의 양**에 비례한다 — 발살바 긴장기·일어서기로 정맥 환류가 줄면 작아진다 [[harrison-22: 44장 p.290]].
- HOCM·MVP 는 반대다 — 심실이 작아질수록 유출로 폐쇄가 심해지고 판막이 일찍 탈출해 커진다 [[harrison-22: 44장 p.290]].
- 후부하(손쥐기)는 역방향 흐름(MR·VSD)을 늘리고 순방향 유출 기울기(AS·HOCM)는 줄인다 [[harrison-22: 44장 p.289]].

## 기전 — 심실 크기가 폐쇄를 정한다
HOCM 에서는 두꺼운 중격과 승모판 앞첨판이 수축기에 유출로를 좁힌다. 심실 안 혈액이 적을수록(전부하·후부하 감소, 수축력 증가) 둘이 더 가까워져 동적 유출로 기울기와 잡음이 커지고, 잡음은 유출로 폐쇄와 MR 이 섞인 모양이다 [[harrison-22: 44장 p.285]]. 쪼그려 앉으면 정맥 환류와 후부하가 함께 올라 심실이 커지므로 잡음이 작고 짧아진다 [[harrison-22: 44장 p.290]]. MVP 도 심실이 작으면 탈출이 수축기 일찍 일어나 클릭과 잡음이 S1 쪽으로 당겨진다 [[harrison-22: 44장 p.286]].

## 가르는 소견 — 조작별 반응
- HOCM 과 MVP 는 조작 반응이 같아 동반 소견으로 가른다 — HOCM 은 좌심실 비대, MVP 는 비구출성 클릭 [[harrison-22: 44장 p.285]].
- HOCM 의 경동맥 상승은 빠르고 정상 크기, 심한 AS 는 작고 늦다 — 노인의 굳은 동맥에서는 덜 정확하다 [[harrison-22: 44장 p.285]].
- 왼쪽 잡음은 날숨 끝에 잘 들리고, 오른쪽 잡음은 들숨에 커진다 [[harrison-22: 44장 p.289]].

## 권고와 예외
- 조작은 원인의 단서일 뿐 — 원인·중증도·좌심실 기능은 경흉부 심초음파로 확인한다 [[harrison-22: 44장 p.285]].
- 정상 심박출량에서 2번째 오른쪽 늑간의 진전과 4도 이상의 잡음은 심한 AS 를 시사하지만, 심부전·저심박출에서는 AS 잡음이 작아진다 [[harrison-22: 44장 p.285]].

## 시험 쟁점 — 충돌·맥락·새 근거
- 해당 없음(대조: 해리슨 22판 44장 p.284–290)
