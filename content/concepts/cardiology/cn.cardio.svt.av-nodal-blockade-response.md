---
id: cn.cardio.svt.av-nodal-blockade-response
type: concept
topic: Cardiology
see_also: [cn.cardio.psvt.narrow-regular-tachycardia-ecg, cn.cardio.atrial-flutter.stable-rate-control-first, cn.cardio.palpitations.arrhythmia-evaluation]
date: 2026-11-12
updated: 2026-11-12
version: 1
outline: h246            # 기본틀 슬롯 — 해리슨 21판 246장(22판 253장) Approach to Supraventricular Arrhythmias
confidence: medium
review_status: unreviewed
note_form: 2
title: "좁은 QRS 빈맥 — 방실결절을 막아 기전을 가른다"
objective: "안정된 규칙적 좁은 QRS 빈맥에서 미주신경 자극·아데노신에 대한 반응으로 방실결절 의존 회귀빈맥과 심방 기원 빈맥·동빈맥을 가른다"
objective_kind: 감별
condition: 상심실빈맥(supraventricular tachycardia, SVT) — 좁은 QRS 빈맥(narrow-complex tachycardia)
exams: [kmle, usmle]
summary:
  - "결론: 방실결절을 잠깐 막았을 때 멎으면 결절 의존 회귀, 심방파가 계속되면 심방 기원, 서서히 느려지면 동·접합부."
  - "시험 단서: 안정된 규칙적 좁은 QRS 빈맥(narrow-complex tachycardia), 미주신경 자극(vagal maneuver)·아데노신(adenosine) 후 리듬 띠."
  - "왜: 방실결절 회귀빈맥·방실 회귀빈맥은 회로에 결절이 들어 있어 끊기고, 심방조동·심방빈맥은 결절 밖 회로라 심실만 느려진다."
  - "가장 흔한 상심실빈맥은 동빈맥이다 — 먼저 원인(운동·발열·급성 질환)을 찾고 원인을 고친다."
  - "아데노신 6 또는 12 mg. 아데노신에 멎어도 심방빈맥을 배제하지 못한다(아데노신 민감 심방빈맥)."
pitfalls:
  - contrast: "아데노신에 멎었다 = 방실결절 회귀로 확정?"
    point: "아데노신으로 끝나는 빈맥에는 방실결절 회귀빈맥(AVNRT)·방실 회귀빈맥(AVRT) 말고도 아데노신 민감 국소 심방빈맥과 다발성(fascicular) 심실빈맥이 있다. 종료는 결절 의존을 강하게 시사할 뿐 확정이 아니다."
    cites: ["harrison-22: 253장 p.1933"]
  - contrast: "아데노신 뒤 빈맥이 계속 = 치료 실패?"
    point: "심실이 잠깐 멈추는 동안 심방파(톱니파·다른 모양 P파)가 그대로 이어지면 그 자체가 진단이다 — 결절이 회로에 없는 심방조동·심방빈맥이다. 이때는 결절 차단으로 빈맥이 끝나지 않는다."
    cites: ["harrison-22: 253장 p.1932", "harrison-22: 253장 p.1933"]
  - contrast: "서서히 느려졌다 다시 빨라짐 vs 갑자기 종료"
    point: "동빈맥·접합부 빈맥은 결절 차단에 잠깐 느려졌다가 되돌아간다. 동빈맥이면 리듬을 끊을 대상이 아니라 원인을 고칠 대상이다."
    cites: ["harrison-22: 253장 p.1933", "harrison-22: 253장 p.1935"]
  - contrast: "반응 없음 = 상심실빈맥 아님?"
    point: "아무 변화가 없으면 먼저 용량·효과 부족을 생각한다(6 mg 뒤 12 mg). 반응 없음만으로 기전을 정하지 않는다."
    cites: ["harrison-22: 253장 p.1933"]
  - contrast: "경동맥동 마사지는 누구에게나?"
    point: "경동맥 죽상경화가 의심되면 마사지가 색전을 떨어뜨릴 수 있어 조심하거나 하지 않는다 — 다른 미주신경 자극이나 아데노신으로 넘어간다."
    cites: ["harrison-22: 253장 p.1933"]
tables:
  - id: avn-block-response
    section: "가르는 소견 — 방실결절을 막았을 때의 반응"
    title: "미주신경 자극·아데노신 반응 — 무엇을 생각하나"
    role: differential
    span: column
    columns: ["반응", "생각할 빈맥"]
    rows:
      - ["빈맥이 멎음", "방실결절 회귀빈맥 · 방실 회귀빈맥 · 아데노신 민감 심방빈맥 · 다발성 심실빈맥 [[harrison-22: 253장 p.1933]]"]
      - ["심실만 멈추고 심방파 계속", "심방조동 · 심방빈맥 [[harrison-22: 253장 p.1933]]"]
      - ["서서히 느려졌다 되돌아감", "동빈맥 · 접합부 빈맥 [[harrison-22: 253장 p.1933]]"]
      - ["변화 없음", "용량·효과 부족 [[harrison-22: 253장 p.1933]]"]
  - id: vagal-maneuvers
    section: "선택 — 미주신경 자극에서 아데노신으로"
    title: "미주신경 자극 방법"
    role: treatment
    span: column
    columns: ["방법", "원리"]
    rows:
      - ["숨 참고 힘주기(발살바 수기) 약 15초", "흉강 내압 상승 [[harrison-22: 253장 p.1934]]"]
      - ["주사기에 세게 불기", "흉강 내압 상승 [[harrison-22: 253장 p.1934]]"]
      - ["다리 갑자기 들기", "정맥 환류 증가 [[harrison-22: 253장 p.1934]]"]
      - ["얼굴 찬물 담그기", "잠수 반사(diver's reflex) [[harrison-22: 253장 p.1934]]"]
      - ["경동맥동 마사지", "경동맥동 → 미주신경 — 경동맥 죽상경화면 조심 [[harrison-22: 253장 p.1933–1934]]"]
criteria:
  - id: svt-def
    name: 상심실빈맥의 정의
    kind: 정의
    population: "심박수 > 100회/분의 빈맥"
    statement: "심실보다 위(심방·방실 접합부)에서 시작하거나 그 전도에 의존하는 빈맥. 대부분 QRS < 120 ms 의 좁은 QRS 빈맥이고 QRS 모양은 동리듬 때와 같다 [[harrison-22: 253장 p.1932]]"
    exceptions: "각차단이나 부전도로(accessory pathway) 전도가 있으면 넓은 QRS 가 되어 심실빈맥과 감별해야 한다 [[harrison-22: 253장 p.1932]]"
    source: harrison-22
    basis: current
    exams: [kmle, usmle]
  - id: atrial-origin
    name: 심방 기원 빈맥의 판별 소견
    kind: 진단 소견
    population: "규칙적 좁은 QRS 빈맥"
    statement: "심실로 전도되지 않는 박동이 있어도 빈맥이 계속되면 방실결절이 회로에 없다 — 심방 기원 빈맥(심방조동·심방빈맥) [[harrison-22: 253장 p.1932]]"
    exceptions: "드물게 히스속 아래 2:1 차단을 동반한 방실결절 회귀빈맥도 심방이 심실보다 많다 [[harrison-22: 253장 p.1933]]"
    source: harrison-22
    basis: current
    exams: [kmle, usmle]
sources:
  - id: harrison-22
    org: "McGraw Hill"
    title: "Harrison's Principles of Internal Medicine, 22nd ed. — Chapter 253: Approach to Supraventricular Arrhythmias"
    kind: textbook
    year: 2025
    citation: "Harrison's Principles of Internal Medicine, 22e. 253장 p.1932–1935"
    checked_at: 2026-11-12
    checked: "드라이브 22판 장별 문서 H22_253 본문 대조 — 상심실빈맥 정의(> 100회/분, QRS < 120 ms, 각차단·부전도로면 넓은 QRS → 심실빈맥 감별), 표 253-1 기전(심방 기원 = 비전도 박동에도 빈맥 지속; 방실결절 회귀빈맥 = P파가 QRS 끝 또는 안 보임·건강한 젊은 성인에서 가장 흔한 발작성 지속 빈맥·여자에 많음; 정방향 방실 회귀빈맥; 조기흥분 심방세동 불규칙 넓은 QRS > 250회/분; 다초점 심방빈맥 = 폐질환), 증상(p.1932) · 그림 253-1(12유도·긴 리듬 띠, 불규칙 → 심방세동·다초점, 1:1 → 접합부·AVNRT·ORT·심방빈맥, 심방 > 심실 → 조동·심방빈맥·드물게 히스속 아래 2:1 AVNRT), 그림 253-2(결절 차단 반응: 종료 = AVNRT·AVRT·아데노신 민감 심방빈맥·다발성 심실빈맥 / 심방 지속 = 조동·심방빈맥 / 느려짐 = 동빈맥·접합부 / 무반응 = 용량·효과 부족), 무증상은 대개 치료·추가 평가 불필요, 증상 때 심전도, 안정 시 조기흥분 = AVRT 시사, 경동맥동 마사지는 경동맥 죽상경화 시 조심, 아데노신 6·12 mg, 아데노신 종료가 심방빈맥 배제 못함, 일시 부정맥은 활동 심전도·웨어러블, 운동 검사, 전기생리검사는 대개 절제 때, PSVT 는 구조 심질환 없는 사람에 흔함(p.1933) · 표 253-2 미주신경 자극(힘주기 15초·주사기 불기·다리 들기·찬물 잠수 반사·경동맥동 마사지)(p.1934) · 가장 흔한 상심실빈맥은 동빈맥 — 먼저 고려하고 원인 치료, 저혈압·의식 저하·협심증·심부전이면 즉시 치료(p.1935)"
    verified: text
diagram:
  title: "좁은 QRS 빈맥 — 방실결절 차단으로 가르기"
  nodes:
    - {id: start, kind: start, text: "좁은 QRS 빈맥 — 12유도·긴 리듬 띠"}
    - {id: sinus, kind: decision, text: "원인이 있는 동빈맥인가?"}
    - {id: cause, kind: end, text: "원인 치료"}
    - {id: unstable, kind: decision, text: "저혈압·의식 저하·협심증·심부전?"}
    - {id: urgent, kind: alert, text: "즉시 치료(리듬 종류에 맞춰)"}
    - {id: irregular, kind: decision, text: "R-R 간격이 불규칙한가?"}
    - {id: af, kind: end, text: "심방세동·다초점 심방빈맥"}
    - {id: block, kind: step, text: "미주신경 자극 → 아데노신 6·12 mg"}
    - {id: resp, kind: decision, text: "결절 차단에 어떻게 반응하나?"}
    - {id: reentry, kind: end, text: "결절 의존 회귀(AVNRT·AVRT) 시사"}
    - {id: atrial, kind: end, text: "심방조동·심방빈맥"}
    - {id: slow, kind: end, text: "동빈맥·접합부 빈맥"}
    - {id: dose, kind: info, text: "용량·투여 확인 후 다시 본다"}
  edges:
    - {from: start, to: sinus}
    - {from: sinus, to: cause, label: "예"}
    - {from: sinus, to: unstable, label: "아니오"}
    - {from: unstable, to: urgent, label: "있음"}
    - {from: unstable, to: irregular, label: "없음"}
    - {from: irregular, to: af, label: "불규칙"}
    - {from: irregular, to: block, label: "규칙"}
    - {from: block, to: resp}
    - {from: resp, to: reentry, label: "멎음"}
    - {from: resp, to: atrial, label: "심방파 계속"}
    - {from: resp, to: slow, label: "서서히 느려짐"}
    - {from: resp, to: dose, label: "변화 없음"}
    - {from: dose, to: reentry, label: "멎음"}
    - {from: dose, to: atrial, label: "심방파 드러남"}
diagram_notes:
  - "아데노신에 멎어도 아데노신 민감 심방빈맥·다발성 심실빈맥일 수 있다 — 「시사」이지 확정이 아니다 [[harrison-22: 253장 p.1933]]."
  - "경동맥 죽상경화가 의심되면 경동맥동 마사지는 조심하거나 하지 않는다 [[harrison-22: 253장 p.1933]]."
  - "넓은 QRS 빈맥은 이 도식 밖 — 심실빈맥과 감별한다 [[harrison-22: 253장 p.1932]]."
checks:
  - q: "24세 여자, 갑자기 시작한 두근거림, 규칙적 좁은 QRS 빈맥 180회/분, 혈압 정상. 아데노신 6 mg 뒤 빈맥이 갑자기 멎었다. 가장 가능성 높은 기전은?"
    a: "방실결절이 회로에 든 회귀빈맥(방실결절 회귀빈맥 또는 방실 회귀빈맥). 단, 아데노신 민감 심방빈맥을 완전히 배제하지는 못한다."
  - q: "아데노신 뒤 QRS 가 몇 초 사라진 사이 하벽 유도에 톱니파가 계속 보였다. 무엇인가?"
    a: "심방조동 — 방실결절 밖 회로라 결절 차단은 심실 반응만 늦춘다."
figures_none: 방실결절 차단 전후의 리듬 띠 변화(시간 경과)가 핵심이라 단일 심전도 사진으로 보여 줄 수 없다 — 판단 도식과 표가 맞다
---

## 판단 — 왜 방실결절 차단 반응이 먼저인가
- **동빈맥부터 지운다**: 가장 흔한 상심실빈맥은 운동·스트레스·급성 질환에 따른 동빈맥이고, 그때는 원인을 치료한다 [[harrison-22: 253장 p.1935]].
- **불안정하면 기다리지 않는다**: 저혈압·의식 저하·협심증·심부전이 있으면 리듬 종류에 맞춘 즉시 치료가 먼저다 [[harrison-22: 253장 p.1935]].
- **증상이 있을 때 심전도**: 진단에는 증상 때의 12유도 심전도와 긴 리듬 띠가 필요하다. 지나가는 부정맥은 활동 심전도나 손목시계·스마트폰 심전도로 잡는다 [[harrison-22: 253장 p.1933]].
- **안정된 규칙적 좁은 QRS 빈맥이면**: 미주신경 자극, 안 되면 아데노신 6 또는 12 mg 으로 방실결절을 잠깐 막는다 — 결절 의존 빈맥은 끝나고, 결절 밖 빈맥은 정체가 드러난다 [[harrison-22: 253장 p.1933]].

## 기전 — 회로에 방실결절이 있는가
상심실빈맥(SVT)은 심실보다 위에서 시작하거나 심방·방실결절을 거치는 전도에 의존하는 빈맥이다. 흥분이 히스-푸르키네 계를 타고 내려오므로 대부분 QRS 가 120 ms 보다 좁고 동리듬 때와 모양이 같다 [[harrison-22: 253장 p.1932]]. 병적 빈맥은 회로의 위치로 나뉜다 — 방실결절에 의존하는 회귀(방실결절 회귀빈맥 AVNRT, 부전도로를 쓰는 방실 회귀빈맥 AVRT), 심방 안의 큰 회귀(심방조동), 자동능이나 작은 회귀로 생기는 국소 심방빈맥이다 [[harrison-22: 253장 p.1932]]. 결절이 회로의 한 고리면 결절을 잠깐 막는 순간 회로가 끊긴다. 결절이 회로 밖이면 심방은 계속 돌고 심실로 내려가는 박동만 줄어 심방파가 드러난다 — 그래서 심실로 전도되지 않는 박동에도 빈맥이 이어지면 심방 기원이다 [[harrison-22: 253장 p.1932]].

## 가르는 소견 — 방실결절을 막았을 때의 반응
- 먼저 리듬 띠의 규칙성과 심방·심실 박동 비를 본다. 심방·심실이 모두 불규칙하면 심방세동(여러 모양 P파면 다초점 심방빈맥), 1:1 이면 접합부 빈맥·방실결절 회귀빈맥·정방향 방실 회귀빈맥·심방빈맥, 심방이 심실보다 많으면 심방조동·심방빈맥을 생각한다 [[harrison-22: 253장 p.1933]].
- 방실결절 회귀빈맥은 P파가 QRS 끝에 보이거나 아예 안 보이고, 건강한 젊은 성인에서 가장 흔한 발작성 지속 빈맥이며 여자에 많다 [[harrison-22: 253장 p.1932]].
- 동리듬 심전도에 심실 조기흥분이 있으면 부전도로를 쓰는 방실 회귀빈맥을 시사한다 [[harrison-22: 253장 p.1933]].
- 반응의 해석 한계: 종료는 결절 의존을 시사할 뿐이고, 변화 없음은 먼저 용량·효과 부족이다 [[harrison-22: 253장 p.1933]].

## 선택 — 미주신경 자극에서 아데노신으로
- 미주신경 자극으로 방실 차단을 먼저 시도하고, 실패하면 아데노신 6 또는 12 mg 을 준다 — 결절 의존 빈맥은 대개 끝나고, 심방빈맥·심방조동은 진단된다 [[harrison-22: 253장 p.1933]].
- 같은 진단 효과는 베라파밀·베타차단제로 결절 차단을 늘려도 얻는다(그림 253-2) [[harrison-22: 253장 p.1933]].
- 전기생리검사는 기전 확인·위험 평가가 필요할 때 하지만 대개 카테터 절제 때 함께 한다 [[harrison-22: 253장 p.1933]].

## 권고와 예외
- 무증상으로 우연히 찍힌 상심실 부정맥은 대부분 치료나 추가 평가가 필요 없다 [[harrison-22: 253장 p.1933]].
- 발작성 상심실빈맥은 구조 심질환이 없는 사람에 흔하고, 심방세동은 여러 심장병과 동반된다 — 병력·진찰에서 이상이 있으면 심장 평가를 더한다 [[harrison-22: 253장 p.1933]].
- 조기흥분 심방세동은 불규칙한 넓은 QRS 빈맥으로 분당 250회를 넘을 수 있다 — 좁은 QRS 도식으로 다루지 않는다 [[harrison-22: 253장 p.1932]].

## 시험 쟁점 — 충돌·맥락·새 근거
- 해당 없음(대조: 해리슨 22판 253장 p.1932~1935)
