---
id: cn.cardio.complete-av-block.permanent-pacemaker
type: concept
topic: Cardiology
see_also: [cn.cardio.sinus-node-dysfunction.symptom-correlated-pacing, cn.cardio.lyme-carditis.heart-block-management]
date: 2026-11-11
updated: 2026-11-11
version: 1
outline: h245
confidence: medium
review_status: unreviewed
note_form: 2
title: "완전 방실차단 — 되돌릴 원인 없으면 영구 조율"
objective: "가역 원인이 없는 후천성 완전(3도)·Mobitz II 방실차단에서 증상과 무관하게 영구 심박조율기를 고른다"
objective_kind: 다음 처치
condition: 완전 방실차단(complete atrioventricular block, third-degree AV block)
exams: [kmle, usmle]
summary:
  - "결론: 되돌릴 원인이 없는 후천성 완전·고도·Mobitz II 방실차단은 증상이 없어도 영구 심박조율기다."
  - "시험 단서: 노인의 실신·운동 시 어지럼, 느리고 규칙적인 맥, 목정맥 대포 a파(cannon a wave), P파와 QRS 가 따로 논다."
  - "왜: 차단이 히스속 아래면 이탈 리듬이 느리고 불안정해 언제든 무수축으로 갈 수 있다 — 약은 그 부위에 듣지 않는다."
  - "먼저 되돌릴 원인: 베타차단제·베라파밀·딜티아젬·디곡신, 전해질, 허혈, 라임 심장염, 수면무호흡."
  - "Mobitz I·1도는 증상과 맞물릴 때만 조율(신경근육병·라민 A/C 심근병증은 예외)."
pitfalls:
  - contrast: "아트로핀 vs 영구 조율"
    point: "아트로핀·이소프로테레놀은 자율신경이 닿는 방실결절의 전도만 좋게 한다. 넓은 QRS 이탈 리듬(히스속 아래 차단)에는 효과가 없고 오히려 차단이 나빠 보일 수 있다. 응급에는 경피 조율이 다리를 놓고, 결론은 영구 조율이다."
    cites: ["harrison-22: 252장 p.1927", "harrison-22: 252장 p.1929"]
  - contrast: "혈역학이 안정적이면 활동 심전도로 지켜본다?"
    point: "동결절 기능 장애와 달리 후천성 완전·Mobitz II 차단은 증상-리듬 상관을 확인할 필요가 없다. 차단 자체가 무수축 위험이라 증상과 무관하게 조율한다."
    cites: ["harrison-22: 252장 p.1924", "harrison-22: 252장 p.1930"]
  - contrast: "급성 하벽 심근경색의 완전 차단 = 영구 조율?"
    point: "하벽 경색의 고도 차단은 90 % 가 히스속 위(방실결절)이고 좁은 이탈 리듬이 분당 40회 넘게 유지돼 대개 회복된다. 전벽 경색의 차단은 히스속 아래·넓고 불안정한 이탈 리듬이라 임시 조율이 필요하다."
    cites: ["harrison-22: 252장 p.1926"]
tables:
  - id: avb-pacing
    section: "선택 — 차단 종류별 영구 조율"
    title: "방실차단 — 영구 조율을 언제 하나"
    role: treatment
    span: column
    columns: ["차단", "영구 조율"]
    rows:
      - ["후천성 완전·고도·Mobitz II(가역 원인 없음)", "증상과 무관하게 권고 [[harrison-22: 252장 p.1930]]"]
      - ["Mobitz I · 1도", "증상이 차단과 맞물릴 때만 — 신경근육병·라민 A/C 는 무증상도 고려 [[harrison-22: 252장 p.1930]]"]
      - ["증상성 비가역 2·3도(부위·원인 무관)", "조율 [[harrison-22: 252장 p.1930]]"]
      - ["약·전해질·허혈·라임·수면무호흡", "원인을 먼저 고친다 [[harrison-22: 252장 p.1929–1930]]"]
criteria:
  - id: avb-ecg
    name: 방실차단 심전도 분류
    kind: 진단 기준
    population: "PR 연장 또는 전도되지 않는 P파가 있는 심전도"
    statement: "1도 = 모든 P파 전도·PR > 200 ms · Mobitz I = PR 이 점점 늘다 전도 실패 · Mobitz II = 일정한 PR 뒤 전도 실패(대개 넓은 QRS) · 3도 = 심방과 심실의 완전 해리, 심실 박동이 심방보다 느림 [[harrison-22: 252장 p.1925]]"
    exceptions: "2:1 차단은 심전도로 I형·II형을 가를 수 없다 — PR < 160 ms 에 QRS 가 넓으면 히스속 아래(II형) 가능성이 높다 [[harrison-22: 252장 p.1925]]"
    source: harrison-22
    basis: current
    exams: [kmle, usmle]
sources:
  - id: harrison-22
    org: "McGraw Hill"
    title: "Harrison's Principles of Internal Medicine, 22nd ed. — Chapter 252: The Bradyarrhythmias: Disorders of the Atrioventricular Node"
    kind: textbook
    year: 2025
    citation: "Harrison's Principles of Internal Medicine, 22e. 252장 p.1924–1930"
    checked_at: 2026-11-11
    checked: "드라이브 22판 장별 문서 H22_252 본문 대조 — 젊은 성인 일시 차단은 미주 긴장, 히스속 아래 차단은 무증상이어도 조율 가능(p.1924) · 표 252-1 분류, Mobitz II 는 히스속 아래·이탈 리듬 불안정·무증상이어도 조율, 2:1 구분 불가, 넓은 QRS 이탈 = 원위 히스/각, 좁은 QRS = 방실결절·접합부 이탈이 빠르고 안정(p.1925) · 표 252-2 원인(약·라임·사르코이드·심내막염 농양 등), 하벽 경색 고도 차단 90 % 히스속 근위·좁은 이탈 > 40회·대개 가역, 전벽 경색은 원위·임시 조율(p.1926) · 미주 자극은 결절에만, 아트로핀·이소프로테레놀은 결절 전도를 개선하고 결절 아래는 악화되어 보일 수 있음(p.1927) · 후천성 완전 차단은 전기생리검사 역할 적고 조율이 거의 항상 적응, 급성 처치 = 가역 원인 제거·이탈 리듬 안정성·임시 조율, 아트로핀·이소프로테레놀은 결절 차단에서만, 경피 → 정맥 경유 임시 조율(p.1929) · 가역 원인, 후천성 Mobitz II·고도·3도는 증상과 무관하게 영구 조율, 그 밖은 증상 상관, 신경근육병은 1도·Mobitz I 도 조율, 증상성 비가역 2·3도는 부위·원인 무관 조율(그림 252-5, p.1930)"
    verified: text
diagram:
  title: "방실차단 — 영구 조율로 가는 길"
  nodes:
    - {id: start, kind: start, text: "P파와 QRS 가 따로 노는 느린 맥"}
    - {id: unstable, kind: decision, text: "저혈압·의식 저하가 있나?"}
    - {id: temp, kind: alert, text: "임시 조율(경피 → 정맥 경유) 후 재판단"}
    - {id: cause, kind: decision, text: "되돌릴 원인이 있나?"}
    - {id: fix, kind: end, text: "원인 교정 후 차단 재평가"}
    - {id: check, kind: info, text: "약·전해질·허혈·라임 확인"}
    - {id: type, kind: decision, text: "완전·고도·Mobitz II 인가?"}
    - {id: ppm, kind: end, text: "영구 심박조율기"}
    - {id: symp, kind: decision, text: "증상이 차단과 맞물리나?"}
    - {id: observe, kind: end, text: "관찰"}
  edges:
    - {from: start, to: unstable}
    - {from: unstable, to: temp, label: "있음"}
    - {from: unstable, to: cause, label: "없음"}
    - {from: cause, to: fix, label: "있음"}
    - {from: cause, to: type, label: "없음"}
    - {from: cause, to: check, label: "모름"}
    - {from: check, to: fix, label: "찾음"}
    - {from: check, to: type, label: "없음"}
    - {from: type, to: ppm, label: "예"}
    - {from: type, to: symp, label: "1도·Mobitz I"}
    - {from: symp, to: ppm, label: "예"}
    - {from: symp, to: observe, label: "아니오"}
diagram_notes:
  - "불안정해 임시 조율을 했으면, 안정된 뒤 같은 순서(가역 원인 → 차단 종류)로 영구 조율을 정한다 [[harrison-22: 252장 p.1929]]."
  - "넓은 QRS 이탈 리듬 = 히스속 아래 차단 — 느리고 불안정하며 아트로핀이 듣지 않는다 [[harrison-22: 252장 p.1925]] [[harrison-22: 252장 p.1929]]."
  - "신경근육병·라민 A/C 심근병증은 1도·Mobitz I 도 조율 대상 [[harrison-22: 252장 p.1930]]."
  - "급성 하벽 경색의 좁은 이탈 리듬 > 40회/분은 대개 저절로 회복 — 임시 조율이 보통 필요 없다 [[harrison-22: 252장 p.1926]]."
checks:
  - q: "76세, 운동 시 어지럼, 넓은 QRS 이탈 리듬의 완전 방실차단, 약·라임 없음. 다음 처치는?"
    a: "영구 심박조율기. 되돌릴 원인이 없는 후천성 완전 차단은 혈역학이 안정적이어도 조율한다."
  - q: "왜 아트로핀이 아닌가?"
    a: "아트로핀은 미주신경이 닿는 방실결절 전도만 개선한다. 넓은 이탈 리듬은 히스속 아래 차단이다."
figures_wanted:
- source: PTBXL
  shows: 완전 방실차단 — P파와 QRS 의 해리
  codes:
  - 3AVB
  at: 기전 — 차단 위치가 이탈 리듬을 정한다
---

## 판단 — 왜 영구 조율이 먼저인가
- **불안정한가**: 저혈압·의식 저하면 먼저 경피 조율, 이어 정맥 경유 임시 조율로 다리를 놓는다 [[harrison-22: 252장 p.1929]].
- **되돌릴 수 있나**: 약(베타차단제·베라파밀·딜티아젬·디곡신)·전해질·허혈·라임 심장염·수면무호흡을 먼저 확인한다 [[harrison-22: 252장 p.1926]] [[harrison-22: 252장 p.1930]].
- **차단 종류**: 후천성 Mobitz II·고도·3도는 되돌릴 원인이 없으면 증상과 무관하게 영구 조율한다 [[harrison-22: 252장 p.1930]]. 전기생리검사는 거의 필요 없다 [[harrison-22: 252장 p.1929]].

## 기전 — 차단 위치가 이탈 리듬을 정한다
방실결절은 교감·부교감 신경을 많이 받지만 히스속과 그 아래 전도계는 자율신경의 영향을 받지 않는다 [[harrison-22: 252장 p.1925]]. 완전 차단이면 심방과 심실이 따로 뛰고(방실 해리), 심실은 아래쪽 박동원이 만든 이탈 리듬으로 뛴다. 차단이 방실결절·근위 히스속이면 접합부에서 좁은 QRS 이탈 리듬이 나와 빠르고 안정적이다. 차단이 원위 히스속·각이면 넓은 QRS 이탈 리듬이 나와 느리고 불안정해 무수축으로 갈 수 있다 [[harrison-22: 252장 p.1925]]. 심방 수축이 닫힌 삼첨판에 부딪히면 목정맥에 대포 a파가 보인다.

## 가르는 소견 — 결절 차단과 결절 아래 차단
- 미주 자극·경동맥동 마사지는 결절 전도만 늦춘다. 아트로핀·이소프로테레놀·운동은 결절 전도를 좋게 하고 결절 아래 전도는 오히려 나빠 보이게 할 수 있다 [[harrison-22: 252장 p.1927]].
- 선천성 완전 차단(좁은 QRS)은 운동하면 심박수가 오르지만, 후천성(특히 넓은 QRS)은 오르지 않는다 [[harrison-22: 252장 p.1927]].

## 선택 — 차단 종류별 영구 조율
- 증상이 있는 비가역 2·3도 차단은 원인과 차단 위치에 관계없이 조율한다. 증상에는 서맥·저심박출뿐 아니라 심부전 악화·협심증·필수 약을 못 쓰는 경우도 들어간다 [[harrison-22: 252장 p.1930]].
- 아트로핀·이소프로테레놀은 결절 차단에서 임시 보조일 뿐이다 [[harrison-22: 252장 p.1929]].

## 권고와 예외
- 급성 하벽 경색의 고도 차단은 90 % 가 히스속 근위이고 좁은 이탈 리듬이 40회/분을 넘어 대개 가역이며 임시 조율이 보통 필요 없다. 전벽 경색의 고도 차단은 광범위 경색·원위 차단을 뜻해 임시 조율이 필요하다 [[harrison-22: 252장 p.1926]].
- 젊은 성인의 일시적 방실차단은 대개 높은 미주 긴장 때문이고(최대 10 %), 수면 중 미주성 차단은 수면무호흡 치료가 먼저다 [[harrison-22: 252장 p.1924]] [[harrison-22: 252장 p.1930]].

## 시험 쟁점 — 충돌·맥락·새 근거
- 해당 없음(대조: 해리슨 22판 252장 p.1924~1930)
