---
id: cn.pharm.nondihydropyridine-ccb.av-node-negative-inotropy
type: concept
topic: Pharmacology
see_also: [Cardiology, Physiology]
date: 2026-11-26
updated: 2026-11-26
version: 1
outline: pharm.cardiovascular-renal   # 약리학 책 「심혈관·신장 약물」
layer: basic            # 기초 정리본 — 임상 정리본의 roots 가 가리키는 기전 단위
discipline: pharmacology
system: cardiovascular
objective_kind: 기전
textbook_check: pending
confidence: medium
review_status: unreviewed
note_form: 2
title: "베라파밀 · 딜티아젬 — 방실결절과 수축을 함께 늦춘다"
objective: "방실결절의 활동전위가 칼슘 전류로 오르고 심실 근육의 고원기도 칼슘 전류가 받친다는 데서, 비디하이드로피리딘 칼슘통로차단제가 방실 전도를 늦추면서 수축력도 떨어뜨리는 이유와 디곡신 · 베타차단제와의 차이를 설명한다"
condition: 비디하이드로피리딘 칼슘통로차단제(non-dihydropyridine calcium channel blocker) — 베라파밀(verapamil) · 딜티아젬(diltiazem)
exams: [usmle, kmle]
summary:
  - "결론: 베라파밀 · 딜티아젬은 L형 칼슘통로를 막아 방실결절 전도를 늦추고, 같은 통로를 쓰는 심실 근육의 수축력도 떨어뜨린다."
  - "시험 단서: 심방세동 심박수 조절 · 4군 항부정맥제(class IV), 박출률 감소 · 저혈압에서 악화 — negative inotropy."
  - "왜: 결절 세포의 상승기(0기)는 나트륨이 아니라 칼슘 전류가 만들고, 심실 근육의 고원기(2기)도 칼슘 전류가 받친다."
  - "디곡신은 음성 변력 작용이 없어 수축이 약한 심장에서 심박수 조절에 써 왔다."
pitfalls:
  - contrast: "칼슘통로차단제 = 다 같은 약?"
    point: "4군 항부정맥제로 분류되는 것은 심장에 선택적인 베라파밀 · 딜티아젬이다 [[harrison-22: 250장 p.1916]]. 혈관을 주로 넓히는 디하이드로피리딘(암로디핀 등)은 방실결절을 늦추는 심박수 조절 약으로 쓰지 않는다(전공 교과서 미대조)."
  - contrast: "음성 변력 = 칼슘통로차단제만?"
    point: "베타차단제도 음성 변력 작용이 있고 디곡신만 없다 [[harrison-22: 258장 p.1949]]. 박출률 감소 심부전에서 베타차단제를 쓰는 것은 그 약이 장기 예후를 바꾸기 때문이지 음성 변력이 없어서가 아니다(임상 정리본 몫)."
tables:
  - id: currents
    section: "고장 — 같은 통로가 전도와 수축을 함께 맡는다"
    title: "L형 칼슘 전류가 하는 일과 막았을 때"
    role: comparison
    span: column
    columns: ["자리", "칼슘 전류의 역할", "막으면"]
    rows:
      - ["동결절 · 방실결절", "상승기(0기)를 만든다 [[harrison-22: 250장 p.1917]], 4기 자동능을 돕는다 [[harrison-22: 250장 p.1913]]", "방실 전도 지연 → 심실 박동수 감소"]
      - ["심실 근육", "고원기(2기)를 칼륨 전류와 맞서 받친다 [[harrison-22: 250장 p.1911]]", "수축력 감소(음성 변력) — 약한 좌심실에서 심부전 악화"]
variants:
  - id: v1
    flip: false
    context: "같은 기전 — 결절 전도를 늦추는 이온"
    stem: "A 68-year-old woman with atrial fibrillation and a ventricular rate of 132/min is given intravenous diltiazem, and her ventricular rate falls to 96/min. Her blood pressure is 124/76 mm Hg. Echocardiography shows a left ventricular ejection fraction of 60%. The drug most likely slowed her ventricular rate by reducing which of the following in atrioventricular nodal cells?"
    choices:
      - "A. Calcium-mediated phase 0 depolarization"
      - "B. Fast sodium-mediated phase 0 depolarization"
      - "C. Delayed rectifier potassium current during phase 3"
      - "D. Activity of the Na+/K+-ATPase"
      - "E. Funny (If) current through HCN channels"
    answer: "A"
    explanation: "In sinoatrial and atrioventricular nodal cells the action potential upstroke is carried by calcium rather than sodium current. Diltiazem, a cardioselective (class IV) calcium channel blocker, slows this upstroke and therefore atrioventricular conduction, lowering the ventricular rate in atrial fibrillation. The same L-type calcium current supports the ventricular plateau, so the drug also lowers contractility — tolerated here because the ejection fraction is preserved. Fast sodium current drives the upstroke of atrial and ventricular myocytes, not nodal cells; Na+/K+-ATPase is the target of digoxin."
    kind: application
figures_none: "기전 목표 — 심전도 소견이 아니라 이온 전류로 설명한다"
sources:
  - id: harrison-22
    org: "McGraw Hill"
    title: "Harrison's Principles of Internal Medicine, 22nd ed."
    kind: textbook
    year: 2025
    citation: "Loscalzo J, Fauci AS, Kasper DL, et al (eds). Harrison's Principles of Internal Medicine, 22e. 250장 Principles of Clinical Cardiac Electrophysiology p.1910–1917 · 258장 Atrial Fibrillation p.1947–1954"
    checked_at: 2026-11-26
    checked: "본문 대조(드라이브 22판 장별 문서 H22_250 · H22_258) — 250장 p.1911 고원기(2기)는 재분극 칼륨 전류와 탈분극 칼슘 전류의 균형, 칼슘 전류 불활성화로 3기; p.1912 방실결절은 느리게 전도, 심방-심실의 유일한 전기 연결, 자율신경에 민감; p.1913 β1 자극이 L형 칼슘통로를 활성화해 4기 탈분극 · 자동능 증가; p.1916 4군 = 심장 선택적 칼슘통로차단제 베라파밀 · 딜티아젬, 디곡신은 Na⁺/K⁺ 펌프 차단; p.1917 결절 세포의 상승기(0기)는 나트륨이 아니라 칼슘 전류로 느리다. 258장 p.1949 심박수 조절의 목표는 이완기 충만 시간 연장, 급성 조절에 베타차단제 · 베라파밀 · 딜티아젬, 디곡신은 칼슘통로차단제 · 베타차단제의 음성 변력 작용이 없어 심부전에 취약한 심근병증에 써 왔다"
    verified: text
---

## 정상 — 결절은 칼슘으로, 근육은 나트륨으로 오른다
동결절 · 방실결절 세포의 활동전위 상승기(0기)는 심방 · 심실 근육보다 느리고, 나트륨이 아니라 칼슘 전류가 만든다 [[harrison-22: 250장 p.1917]]. 그래서 방실결절은 자극을 천천히 전하며, 정상 심장에서 심방과 심실을 잇는 유일한 전기 통로다 [[harrison-22: 250장 p.1912]]. 심실 근육은 빠른 나트륨 전류로 오른 뒤, 탈분극 칼슘 전류와 재분극 칼륨 전류가 맞서는 고원기(2기)를 지난다 [[harrison-22: 250장 p.1911]]. 고원기에 들어온 칼슘이 수축을 일으키는 방아쇠다(전공 교과서 미대조).

## 고장 — 같은 통로가 전도와 수축을 함께 맡는다
베라파밀 · 딜티아젬은 심장에 선택적인 칼슘통로차단제로 4군 항부정맥제다 [[harrison-22: 250장 p.1916]]. 결절에서 칼슘 전류가 줄면 상승기가 더 느려져 방실 전도가 늦어지고, 심방세동에서 심실로 넘어가는 자극 수가 준다. 같은 L형 칼슘 전류가 심실 근육의 고원기를 받치므로 수축력도 함께 떨어진다 — 칼슘통로차단제와 베타차단제의 음성 변력 작용이다 [[harrison-22: 258장 p.1949]].

## 소견으로 — 심박수는 내려가지만 약한 심장은 더 약해진다
- 심박수가 내려가면 이완기 충만 시간이 늘어 심박출량과 증상이 좋아진다 [[harrison-22: 258장 p.1949]].
- 좌심실이 이미 약하면 수축력 감소가 이 이득을 넘어서 심박출량이 떨어지고 심부전이 악화한다.
- 디곡신은 이 음성 변력 작용이 없어 혈압이 불안정하거나 심부전에 취약한 심근병증 환자에서 심박수 조절에 써 왔다 [[harrison-22: 258장 p.1949]].

## 임상 판단으로 — 이 기전이 가르는 선택
- 박출률이 보존된 심방세동은 베타차단제와 베라파밀 · 딜티아젬이 모두 급성 심박수 조절 약이다 [[harrison-22: 258장 p.1949]].
- 박출률이 줄었으면 음성 변력이 큰 베라파밀 · 딜티아젬을 피하고 베타차단제 · 디곡신으로 조절한다(임상 정리본 `cn.cardio.atrial-fibrillation.hfref-rate-control-drug`).

## 시험 쟁점 — 충돌·맥락·새 근거
- 해당 없음(대조: 해리슨 22판 250장 p.1911~1917, 258장 p.1949)
