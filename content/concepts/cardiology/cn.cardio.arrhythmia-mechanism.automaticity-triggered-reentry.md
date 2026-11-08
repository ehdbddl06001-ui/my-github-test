---
id: cn.cardio.arrhythmia-mechanism.automaticity-triggered-reentry
type: concept
topic: Cardiology
see_also: [Pharmacology, Physiology]
date: 2026-11-09
updated: 2026-11-09
version: 1
outline: h243            # 기본틀 슬롯 — 해리슨 21판 243장(22판 250장) Principles of Clinical Cardiac Electrophysiology
confidence: medium
review_status: unreviewed
note_form: 2
title: "빈맥의 세 기전 — 자동능·촉발·회귀가 치료를 정한다"
objective: "빈맥을 자동능 항진·촉발 활동(조기·지연 후탈분극)·회귀로 나누고 기전마다 맞는 치료(4기 억제·유발 요인 교정·불응기 연장·회로 절제)를 설명한다"
objective_kind: 기전
condition: 빈맥성 부정맥의 기전(mechanisms of tachyarrhythmias)
exams: [kmle, usmle]
summary:
  - "결론: 자동능 항진은 4기 억제, 촉발 활동은 유발 요인 교정, 회귀는 불응기 연장·회로 절제로 다스린다."
  - "시험 단서: QT 연장+저칼륨·저마그네슘·서맥 → 조기 후탈분극(EAD)·염전성 심실빈맥(TdP), 디곡신 중독 → 지연 후탈분극(DAD)."
  - "왜: 회귀는 일방향 차단과 느린 전도가 있어야 돌고, 회로 길이가 파장(전도속도 × 불응기)보다 길 때 유지된다."
  - "전도만 늦추는 약(Na 통로 차단제)은 흥분 간극을 넓혀 오히려 회귀를 부를 수 있다 — 항부정맥제의 부정맥 유발."
  - "해부학적 회귀(조동·AVNRT·AVRT·흉터 VT)는 절제로 끊기고, 기능적 회귀(심방세동·심실세동)는 절제로 잘 안 끊긴다."
pitfalls:
  - contrast: "느린 전도 = 항부정맥 효과?"
    point: "회귀를 끊는 것은 파장(전도속도 × 불응기)을 회로보다 길게 만드는 것이다. 불응기를 늘리는 K 통로 차단제는 파장을 늘리지만, 전도만 늦추면 파장이 짧아져 흥분 간극이 커지고 회귀가 쉬워진다 [[harrison-22: 250장 p.1914]]."
    cites: ["harrison-22: 250장 p.1914"]
  - contrast: "EAD vs DAD"
    point: "조기 후탈분극은 2~3기(재분극 중)에 생기고 QT 연장이 바탕이라 염전성 심실빈맥을 부른다. 지연 후탈분극은 4기에 세포 안 Ca 과부하로 생기고 디곡신 중독·허혈·카테콜아민이 원인이며 양방향 심실빈맥이 대표다 [[harrison-22: 250장 p.1913]]."
    cites: ["harrison-22: 250장 p.1913"]
  - contrast: "촉발 활동 = 항부정맥제?"
    point: "촉발 활동은 유발 요인을 없애는 것이 가장 효과적이다 — 디곡신 제거, QT 연장 약 중단, 필요하면 심박수를 올려 QT 를 줄인다 [[harrison-22: 250장 p.1914]]."
    cites: ["harrison-22: 250장 p.1914"]
tables:
  - id: mechanisms
    section: "가르는 소견 — 기전별 원인·예·치료"
    title: "빈맥의 세 기전"
    role: differential
    span: column
    columns: ["기전", "생기는 곳·원인", "예 · 치료"]
    rows:
      - ["자동능 항진", "4기 자발 탈분극이 빨라짐 — 동결절·방실결절·히스-푸르키네, 폐정맥, 경색 경계부", "특발성 VT·심방빈맥·재관류 PVC · Ca 통로 차단제·β 차단제·이바브라딘, 병소 절제 [[harrison-22: 250장 p.1913]] [[harrison-22: 250장 p.1914]]"]
      - ["촉발 — EAD", "2~3기, QT 연장(약·저칼륨·저마그네슘·서맥)", "TdP · 유발 요인 교정, 심박수 올리기 [[harrison-22: 250장 p.1913]] [[harrison-22: 250장 p.1914]]"]
      - ["촉발 — DAD", "4기, 세포 안 Ca 과부하(디곡신·허혈·카테콜아민)", "양방향 VT · 디곡신 제거 [[harrison-22: 250장 p.1913]] [[harrison-22: 250장 p.1914]]"]
      - ["회귀", "일방향 차단 + 느린 전도, 회로 > 파장", "조동·AVNRT·AVRT·흉터 VT · 불응기 연장(K 통로 차단), 회로 절제 [[harrison-22: 250장 p.1914]]"]
diagram:
  title: "빈맥 기전에서 치료로"
  nodes:
    - {id: start, kind: start, text: "빈맥, 기전을 생각한다"}
    - {id: mech, kind: decision, text: "어떤 기전인가?"}
    - {id: ep, kind: info, text: "기전 불명 → 전기생리검사"}
    - {id: auto, kind: end, text: "자동능 — 4기 억제·병소 절제"}
    - {id: trig, kind: end, text: "촉발 — 유발 요인 교정"}
    - {id: anat, kind: decision, text: "고정된 회로가 있나?"}
    - {id: ablate, kind: end, text: "해부학적 회귀 — 회로 절제"}
    - {id: func, kind: end, text: "기능적 회귀 — 약·전기충격"}
  edges:
    - {from: start, to: mech}
    - {from: mech, to: auto, label: "자동능"}
    - {from: mech, to: trig, label: "후탈분극"}
    - {from: mech, to: anat, label: "회귀"}
    - {from: mech, to: ep, label: "모름"}
    - {from: ep, to: anat, label: "회귀 유발"}
    - {from: ep, to: auto, label: "병소 확인"}
    - {from: anat, to: ablate, label: "예"}
    - {from: anat, to: func, label: "아니오"}
diagram_notes:
  - "4기 억제 = Ca 통로 차단제·β 차단제(교감 입력 차단)·이바브라딘(If 차단) [[harrison-22: 250장 p.1914]]."
  - "촉발 활동의 교정 = 디곡신 제거, QT 연장 약 중단, 심박수를 올려 QT 단축 [[harrison-22: 250장 p.1914]]."
  - "자동능 빈맥은 전기생리검사에서 유발되지 않을 수 있다 [[harrison-22: 250장 p.1915]]."
  - "기능적 회귀(심방세동·심실세동)는 고정 회로가 없어 절제로 기질을 끊기 어렵다 [[harrison-22: 250장 p.1914]]."
checks:
  - q: "회귀가 시작·유지되는 두 조건은?"
    a: "일방향 차단과 느린 전도. 회로 길이가 파장(전도속도 × 불응기)보다 길면 흥분 간극이 생겨 계속 돈다."
  - q: "디곡신 중독의 양방향 심실빈맥은 어떤 기전인가?"
    a: "지연 후탈분극(4기, 세포 안 Ca 과부하)에 의한 촉발 활동."
sources:
  - id: harrison-22
    org: "McGraw Hill"
    title: "Harrison's Principles of Internal Medicine, 22nd ed. — Chapter 250: Principles of Clinical Cardiac Electrophysiology"
    kind: textbook
    year: 2025
    citation: "Harrison's Principles of Internal Medicine, 22e. 250장 p.1910–1917"
    checked_at: 2026-11-09
    checked: "드라이브 22판 장별 문서 H22_250 본문 대조 — 활동전위 0~4기와 심전도 대응(p.1910–1911) · Na·Ca 통로가 탈분극, K 통로가 재분극, K 통로 변이가 긴 QT(p.1911) · 심방·심실은 Na, 결절은 Ca 가 상승기를 이끌어 Na 차단제는 심방·심실, Ca 차단제는 결절에 듣는다, 동결절 4기 If(이바브라딘 표적), 푸르키네 2~3 m/s vs 심근 0.3~0.4 m/s(p.1912) · 기전 분류(자동능·촉발·회귀, 표 250-1), 미주신경 IKACh 과분극·β1 L형 Ca, 폐정맥·경색 경계부 자동능, EAD 2~3기·QT 연장·저칼륨·저마그네슘·서맥·TdP, DAD 4기·세포 안 Ca·디곡신·허혈·카테콜아민·양방향 VT(p.1913) · 회귀의 일방향 차단·느린 전도, 파장 = 전도속도 × 불응기, 흥분 간극, 해부학적(조동·AVNRT·AVRT·흉터 VT) vs 기능적(AF·VF) 회귀, 치료: 자동능 4기 억제, 촉발 유발 요인 교정, 회귀 불응기 연장(K 차단), 전도만 늦추면 부정맥 유발, 해부학적 회로는 절제로 끊기고 기능적 회귀는 절제가 비효과적(p.1914) · 자동능 빈맥은 전기생리검사에서 유발되지 않을 수 있음(p.1915)"
    verified: text
figures_none: "기전 목표 — 영상 소견이 아니라 활동전위·회로 개념이 시험 단서다"
---

## 기전 — 정상 활동전위에서 세 가지 이상으로
심방·심실 근육세포의 활동전위는 0기(빠른 상승, Na 유입) → 1기(초기 재분극) → 2기(고원기, Ca 유입과 K 유출의 균형) → 3기(재분극, 주로 IKr·IKs) → 4기(휴지기)로 이어지고, 심실의 0기는 QRS, 1~2기는 ST, 3기는 T파에 대응한다 [[harrison-22: 250장 p.1910]] [[harrison-22: 250장 p.1911]]. 동결절은 4기에 If(funny current)로 천천히 탈분극해 스스로 박동을 만들고(자동능), 미주신경(IKACh 개방 → 과분극)은 이를 늦추며 β1 자극(L형 Ca 통로)은 빠르게 한다 [[harrison-22: 250장 p.1912]] [[harrison-22: 250장 p.1913]].
- **자동능 항진(enhanced automaticity)**: 4기 탈분극이 비정상적으로 빨라지거나, 폐정맥·관상정맥동·유출로·경색 경계부처럼 평소에는 자동능이 없는 곳이 박동을 만든다 [[harrison-22: 250장 p.1913]].
- **촉발 활동(triggered activity)**: 앞선 활동전위 끝의 후탈분극이 역치에 닿아 새 박동을 일으킨다. 조기 후탈분극(early afterdepolarization, EAD)은 2~3기, 지연 후탈분극(delayed afterdepolarization, DAD)은 4기에 생긴다 [[harrison-22: 250장 p.1913]].
- **회귀(reentry)**: 흥분파가 원을 돌며 다시 깨운다. 일방향 차단과 느린 전도가 필요하고, 회로 길이가 파장(λ = 전도속도 θ × 불응기 tr)보다 길어 흥분 간극이 남을 때 유지된다 [[harrison-22: 250장 p.1914]].

## 가르는 소견 — 기전별 원인·예·치료
- 결절 조직은 Ca 가, 심방·심실은 Na 가 상승기를 이끈다 — 그래서 Ca 통로 차단제는 결절 빈맥에, Na 통로 차단제는 심방·심실 빈맥에 듣는다 [[harrison-22: 250장 p.1912]].
- 해부학적 회귀는 흉터·부전도로·판륜 같은 고정 장벽을 돌아 안정하고, 기능적 회귀(심방세동·심실세동)는 불응 조직 둘레를 돌아 불안정하며 여러 회로가 떠돈다 [[harrison-22: 250장 p.1914]].
- 허혈·경색은 흉터 섬(해부학적 회귀 기질)과 경계부 손상 심근(자동능·촉발)을 함께 만들고, 커넥신 감소로 전도를 늦춘다 [[harrison-22: 250장 p.1914]].

## 선택 — 기전에 맞춘 치료
- 자동능: 4기 탈분극을 늦춘다(Ca 통로 차단제·β 차단제·이바브라딘), 병소를 찾아 절제·격리한다 [[harrison-22: 250장 p.1914]].
- 촉발 활동: 유발 요인 교정이 가장 효과적이다 [[harrison-22: 250장 p.1914]].
- 회귀: 불응기를 늘려(K 통로 차단제) 파장을 회로보다 길게 한다. Na 통로 차단제는 전도를 충분히 늦춰 회로를 끊을 만큼 써야 하며, 어중간하면 흥분 간극을 넓혀 부정맥을 부른다 [[harrison-22: 250장 p.1914]]. 해부학적 회로는 절제선으로 끊는다 [[harrison-22: 250장 p.1914]].
- 정상 결과의 해석 한계: 자동능 빈맥은 일시적·다인성이라 전기생리검사에서 유발되지 않을 수 있다 — 유발되지 않았다고 배제하지 않는다 [[harrison-22: 250장 p.1915]].

## 권고와 예외
- 휴식 심전도는 약 6초만 기록하므로 간헐적 부정맥은 증상 빈도에 맞춘 장시간 감시로 잡는다(매일 증상이면 24~48시간 Holter) [[harrison-22: 250장 p.1915]].

## 시험 쟁점 — 충돌·맥락·새 근거
- 해당 없음(대조: 해리슨 22판 250장 p.1910–1915)
