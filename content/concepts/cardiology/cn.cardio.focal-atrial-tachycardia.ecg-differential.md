---
id: cn.cardio.focal-atrial-tachycardia.ecg-differential
type: concept
topic: Cardiology
see_also: [cn.cardio.svt.av-nodal-blockade-response, cn.cardio.psvt.narrow-regular-tachycardia-ecg, cn.cardio.atrial-flutter.stable-rate-control-first, cn.cardio.arrhythmia-mechanism.automaticity-triggered-reentry]
date: 2026-11-13
updated: 2026-11-13
version: 1
outline: h248            # 기본틀 슬롯 — 해리슨 21판 248장(22판 255장) Focal Atrial Tachycardia
confidence: medium
review_status: unreviewed
note_form: 2
title: "국소 심방빈맥 — P파 모양과 방실 차단 반응으로 가른다"
objective: "규칙적 좁은 QRS 빈맥에서 P파 모양·시작 양상·방실 차단 반응으로 국소 심방빈맥을 동빈맥·방실결절 의존 빈맥과 가른다"
objective_kind: 감별
condition: 국소 심방빈맥(focal atrial tachycardia, AT)
exams: [kmle, usmle]
summary:
  - "결론: 동리듬과 다른 모양의 뚜렷한 P파가 빠르게 이어지고, 방실 차단이 생겨도 심방 박동이 그대로면 국소 심방빈맥이다."
  - "시험 단서: P파 사이 등전위선(isoelectric line), RP > PR, 방실 차단 동반(특히 디곡신 복용), 갑작스런 시작·끝 또는 warm-up."
  - "왜: 회로가 심방 안에만 있어 방실결절을 막아도 끊기지 않는다 — 심실 반응만 줄고 P파가 드러난다."
  - "불안정하면 심장율동전환, 안정되면 아데노신 → 비디하이드로피리딘 칼슘통로차단제·베타차단제, 재발하면 절제(> 80 % 성공)."
  - "무증상 비지속 심방빈맥(활동 심전도에서 흔함)은 치료하지 않는다."
pitfalls:
  - contrast: "국소 심방빈맥 vs 동빈맥"
    point: "1:1 전도면 RP > PR 로 동빈맥처럼 보인다. P파 모양이 동리듬 때와 다르면 국소 심방빈맥이다. 동결절 가까운 분계능선(crista terminalis) 위쪽 초점은 P파가 같아 보이므로 갑작스런 시작·끝으로 가른다."
    cites: ["harrison-22: 255장 p.1937"]
  - contrast: "아데노신에 안 멎음 = 심방빈맥 아님?"
    point: "거꾸로다. 방실결절에 의존하지 않으므로 방실 차단이 생겨도 빈맥은 계속되고 심방 박동수도 변하지 않는다 — 결절 의존 빈맥(방실결절 회귀빈맥·방실 회귀빈맥)과 가르는 소견이다. 다만 유발 활동(triggered activity)이 기전이면 충분한 아데노신에 멎기도 한다."
    cites: ["harrison-22: 255장 p.1937", "harrison-22: 255장 p.1938"]
  - contrast: "국소 심방빈맥 vs 심방조동"
    point: "국소 초점은 심방 주기의 짧은 부분에서만 흥분이 퍼져 P파 사이에 등전위선이 남는다. 심방조동·대회귀 심방빈맥은 흥분이 주기 내내 돌아 기저선이 없다(톱니파)."
    cites: ["harrison-22: 255장 p.1937"]
  - contrast: "방실 차단을 동반한 심방빈맥 = 흔한 형태일 뿐?"
    point: "방실 차단을 동반한 심방빈맥은 디기탈리스(digitalis) 독성의 특징이다. 새로 생긴 심방빈맥은 바탕 질환·약물 독성의 신호일 수 있어 유발 인자를 찾는다."
    cites: ["harrison-22: 255장 p.1937", "harrison-22: 255장 p.1938"]
  - contrast: "율동전환 후 곧 재발 = 실패한 시술?"
    point: "심장율동전환이 듣지 않고 바로 재발하면 자동능 항진이 기전임을 시사한다. 그때는 율동전환을 되풀이하지 않고 심박수 조절·항부정맥제·절제로 간다."
    cites: ["harrison-22: 255장 p.1938"]
tables:
  - id: at-vs-rivals
    section: "가르는 소견 — 동빈맥·결절 의존 빈맥·조동과의 경계"
    title: "규칙적 좁은 QRS 빈맥에서 국소 심방빈맥 가르기"
    role: differential
    span: column
    columns: ["혼동 대안", "국소 심방빈맥 쪽 소견"]
    rows:
      - ["동빈맥", "P파 모양이 동리듬과 다름 · 갑작스런 시작·끝 [[harrison-22: 255장 p.1937]]"]
      - ["방실결절 회귀빈맥 · 방실 회귀빈맥", "방실 차단에도 빈맥·심방 박동수 그대로 · warm-up·cool-down [[harrison-22: 255장 p.1937]]"]
      - ["심방조동 · 대회귀 심방빈맥", "P파가 뚜렷하고 사이에 등전위선 [[harrison-22: 255장 p.1937]]"]
  - id: at-p-axis
    section: "기전 — 초점에서 P파로"
    title: "P파 모양으로 짐작하는 초점 위치"
    role: differential
    span: column
    columns: ["P파", "초점"]
    rows:
      - ["V1 단상 양성 · I·aVL 음성", "좌심방 [[harrison-22: 255장 p.1937]]"]
      - ["II·III·aVF 양성", "위쪽(상대정맥·상폐정맥) [[harrison-22: 255장 p.1937]]"]
      - ["II·III·aVF 음성", "아래쪽(관상정맥동 입구) [[harrison-22: 255장 p.1937]]"]
      - ["동리듬보다 폭이 좁음", "심방중격 [[harrison-22: 255장 p.1937]]"]
      - ["동리듬과 같아 보임", "분계능선 위쪽(동결절 근처) [[harrison-22: 255장 p.1937]]"]
  - id: at-management
    section: "선택 — 급성기와 재발"
    title: "국소 심방빈맥 치료 순서"
    role: treatment
    span: column
    columns: ["상황", "치료"]
    rows:
      - ["혈역학적 불안정", "심장율동전환 [[harrison-22: 255장 p.1938]]"]
      - ["안정", "아데노신 → 안 들으면 비디하이드로피리딘 칼슘통로차단제·베타차단제 → 안 들으면 율동전환 [[harrison-22: 255장 p.1938]]"]
      - ["재발·지속(incessant)", "항부정맥제 또는 카테터 절제 [[harrison-22: 255장 p.1938]]"]
      - ["무증상 비지속(활동 심전도)", "치료하지 않음 [[harrison-22: 255장 p.1937]]"]
criteria:
  - id: at-def
    name: 국소 심방빈맥의 정의
    kind: 정의
    population: "규칙적 좁은 QRS 빈맥"
    statement: "심방의 한 초점에서 자동능 항진·유발 활동·작은 회귀로 생기는 빈맥. 「국소」는 전형·비전형 심방조동과 구별하는 말이지 기전을 뜻하지 않는다 [[harrison-22: 255장 p.1937]]"
    exceptions: "폐정맥·관상정맥동·대정맥으로 뻗은 심방 조직에서도 생긴다 [[harrison-22: 255장 p.1937]]"
    source: harrison-22
    basis: current
    exams: [kmle, usmle]
  - id: at-ablation
    name: 카테터 절제 적응
    kind: 치료 적응
    population: "국소 심방빈맥"
    statement: "약이 듣지 않거나 원하지 않는 재발성 유증상 심방빈맥, 또는 빈맥 유발 심근병증을 일으키는 지속성(incessant) 심방빈맥 — 성공률 > 80 % [[harrison-22: 255장 p.1938]]"
    exceptions: "심방세동·조동의 전구일 수 있으나 장기 항응고 적응은 불분명하고 같다고 보지 않는다 [[harrison-22: 255장 p.1938]]"
    source: harrison-22
    basis: current
    exams: [kmle, usmle]
sources:
  - id: harrison-22
    org: "McGraw Hill"
    title: "Harrison's Principles of Internal Medicine, 22nd ed. — Chapter 255: Focal Atrial Tachycardia"
    kind: textbook
    year: 2025
    citation: "Harrison's Principles of Internal Medicine, 22e. 255장 p.1937–1938"
    checked_at: 2026-11-13
    checked: "드라이브 22판 장별 문서 H22_255 본문 대조 — 기전(자동능 항진·유발 자동능·병든 심방의 작은 회귀, 「국소」는 조동과 구별하는 말), 발생 부위(폐정맥·관상정맥동·대정맥 포함), 카테터 절제 의뢰 PSVT 의 약 10 %, 비지속형은 활동 심전도에서 흔하고 나이에 따라 늘며 무증상이면 치료 권고 안 함, 심방세동·조동의 전구, 섬유화(이전 절제 포함)·교감 자극·바탕 질환·약물 독성, 방실 차단 동반 심방빈맥 = 디기탈리스 독성 특징, 지속형은 빈맥 유발 심근병증, 1:1 또는 벤케바흐·고정(2:1·3:1) 차단, 방실 차단에 안 멎고 심방 박동수 불변 → 결절 의존 SVT 와 구별, warm-up·cool-down, P파 사이 등전위선(조동과 대조), 1:1 이면 PR < RP 로 동빈맥 닮음·P파 모양으로 구별, 초점 위치별 P파(중격 = 좁은 P, 좌심방 = V1 단상 양성·I·aVL 음성, 위쪽 = 하벽 양성, 관상정맥동 입구 = 하벽 음성, 분계능선 위쪽 = 동빈맥과 같음 → 갑작스런 시작·끝)(p.1937) · 경동맥동 마사지·발살바·아데노신으로 방실 차단을 만들어 P파 노출, 급성 치료는 다른 PSVT 와 같으나 반응은 기전에 따라 다름(회귀 = 아데노신·미주신경 자극에 차단만 늘고 안 멎음, 충분한 아데노신에 멎으면 유발 활동, 율동전환 후 즉시 재발 = 자동능), 베타차단제·칼슘통로차단제는 방실 차단을 늘려 심실 반응을 늦추나 큰 용량 필요할 때 있음, 유발 인자·병발 질환 교정·바탕 심질환 배제, 그림 255-3(불안정 → 율동전환 / 안정 → 아데노신 → 비DHP CCB·베타차단제 → 율동전환, 재발·지속 → 항부정맥제(표 250-2)·카테터 절제), 재발 시 베타차단제·딜티아젬·베라파밀·플레카이니드·프로파페논·디소피라미드·소탈롤·아미오다론(장기 사용은 독성으로 피하는 경우 많음), 절제 > 80 % 효과(약 실패·거부한 재발 유증상, 빈맥 유발 심근병증), 장기 항응고 적응 불분명(p.1938)"
    verified: text
diagram:
  title: "규칙적 좁은 QRS 빈맥 — 국소 심방빈맥 가르기"
  nodes:
    - {id: start, kind: start, text: "규칙적 좁은 QRS 빈맥 — 12유도·리듬 띠"}
    - {id: unstable, kind: decision, text: "혈역학적으로 불안정한가?"}
    - {id: dccv, kind: alert, text: "심장율동전환"}
    - {id: pwave, kind: decision, text: "P파가 동리듬 때와 같은가?"}
    - {id: onset, kind: decision, text: "갑자기 시작·끝났나?"}
    - {id: sinus, kind: end, text: "동빈맥 — 원인 치료"}
    - {id: block, kind: step, text: "미주신경 자극·아데노신으로 방실 차단"}
    - {id: resp, kind: decision, text: "방실 차단 때 심방 박동은?"}
    - {id: avdep, kind: end, text: "결절 의존 빈맥(AVNRT·AVRT) 시사"}
    - {id: at, kind: end, text: "국소 심방빈맥"}
    - {id: flutter, kind: end, text: "심방조동·대회귀 심방빈맥"}
    - {id: more, kind: info, text: "증상 때 기록·이전 심전도와 비교"}
  edges:
    - {from: start, to: unstable}
    - {from: unstable, to: dccv, label: "예"}
    - {from: unstable, to: pwave, label: "아니오"}
    - {from: pwave, to: onset, label: "같음"}
    - {from: pwave, to: block, label: "다름·안 보임"}
    - {from: onset, to: sinus, label: "서서히"}
    - {from: onset, to: at, label: "갑자기"}
    - {from: onset, to: more, label: "모름"}
    - {from: more, to: block}
    - {from: block, to: resp}
    - {from: resp, to: avdep, label: "빈맥이 멎음"}
    - {from: resp, to: at, label: "뚜렷한 P파 계속"}
    - {from: resp, to: flutter, label: "톱니파 계속"}
diagram_notes:
  - "유발 활동이 기전인 심방빈맥은 충분한 아데노신에 멎기도 한다 — 「멎음」은 결절 의존을 시사할 뿐이다 [[harrison-22: 255장 p.1938]]."
  - "방실 차단을 동반한 심방빈맥이면 디기탈리스 독성을 먼저 생각한다 [[harrison-22: 255장 p.1937]]."
  - "무증상 비지속 심방빈맥은 치료하지 않는다 [[harrison-22: 255장 p.1937]]."
checks:
  - q: "68세 남자, 디곡신 복용 중. 심전도에서 분당 180회의 뚜렷한 P파가 등전위선을 사이에 두고 이어지고 2:1 로 심실에 전도된다. 먼저 생각할 것은?"
    a: "방실 차단을 동반한 심방빈맥 — 디기탈리스 독성의 특징이다."
  - q: "규칙적 좁은 QRS 빈맥에서 아데노신 뒤 QRS 가 잠시 사라졌는데, 동리듬과 다른 모양의 P파가 같은 박동수로 계속 보였다. 무엇인가?"
    a: "국소 심방빈맥 — 방실결절이 회로 밖이라 차단에도 심방 박동이 그대로다."
figures_wanted:
- source: PMC_OA
  shows: 동리듬과 다른 모양의 뚜렷한 P파가 등전위선을 사이에 두고 이어지는 국소 심방빈맥
  query: '"focal atrial tachycardia" AND "electrocardiogram" AND "case report"'
  caption_terms:
  - atrial tachycardia
  modality: ECG
---

## 판단 — 왜 P파와 방실 차단 반응을 먼저 보나
- **불안정하면 리듬 판독보다 율동전환**이 먼저다 [[harrison-22: 255장 p.1938]].
- **P파 모양부터**: 1:1 전도면 동빈맥처럼 PR < RP 로 보이므로, 동리듬 때와 다른 P파가 국소 심방빈맥의 첫 단서다 [[harrison-22: 255장 p.1937]].
- **P파가 숨어 있으면 방실 차단을 만든다**: 심박수에 따라 P파가 T파에 겹치거나 2:1 전도 때 QRS 와 겹친다 — 경동맥동 마사지·발살바 수기·아데노신으로 방실 차단을 늘리면 드러난다 [[harrison-22: 255장 p.1937–1938]].
- **차단 뒤 심방 박동이 그대로면** 결절 의존 빈맥이 아니다 [[harrison-22: 255장 p.1937]].

## 기전 — 초점에서 P파로
국소 심방빈맥(focal atrial tachycardia)은 심방 한 곳의 자동능 항진, 유발 자동능(triggered automaticity), 병든 심방 조직의 작은 회귀(microreentry)로 생긴다 [[harrison-22: 255장 p.1937]]. 섬유화 부위(이전 절제 부위 포함)의 손상됐지만 살아 있는 세포가 자동능을 띠거나, 섬유화 경계의 느린 전도 구역이 작은 회귀를 만든다. 교감 자극이 부추기므로 새로 생긴 심방빈맥은 바탕 질환·약물 독성의 신호일 수 있다 [[harrison-22: 255장 p.1937]]. 흥분이 한 점에서 퍼져 심방 주기의 짧은 부분만 차지하므로 P파가 뚜렷하고 그 사이에 등전위선이 남는다 — 주기 내내 흥분이 도는 심방조동과 다른 점이다 [[harrison-22: 255장 p.1937]]. 초점은 분계능선·판막륜·심방중격·흉곽 정맥(상대정맥·관상정맥동·폐정맥)으로 뻗은 심방근처럼 구조가 복잡한 곳에 많고, P파 모양으로 위치를 짐작한다 [[harrison-22: 255장 p.1937]]. 자동능 항진이면 시작 뒤 빨라지는 warm-up, 끝나기 전 느려지는 cool-down 이 흔하다 [[harrison-22: 255장 p.1937]].

## 가르는 소견 — 동빈맥·결절 의존 빈맥·조동과의 경계
- 방실 전도는 1:1 이거나 벤케바흐·고정(2:1·3:1) 차단을 보인다. 방실결절에 의존하지 않으므로 방실 차단에도 멎지 않고 심방 박동수도 변하지 않는다 — 방실결절 회귀빈맥(AVNRT)·방실 회귀빈맥(AVRT)과 가르는 핵심이다 [[harrison-22: 255장 p.1937]].
- 방실결절 회귀빈맥은 대개 P파가 안 보이거나 RP < PR, 국소 심방빈맥은 대개 RP > PR 이다(그림 255-1) [[harrison-22: 255장 p.1937]].
- 동결절 가까운 분계능선 위쪽 초점은 P파가 동빈맥과 같아 보인다 — 이때는 갑작스런 시작·끝이 국소 심방빈맥 쪽이다 [[harrison-22: 255장 p.1937]].

## 선택 — 급성기와 재발
- 갑자기 시작한 지속성 심방빈맥의 급성 치료는 다른 발작성 상심실빈맥과 같지만, 약 반응은 기전에 따라 다르다 [[harrison-22: 255장 p.1938]]. 회귀가 기전이면 아데노신·미주신경 자극이 차단만 늘리고 멈추지 못하고, 충분한 아데노신에 멎으면 유발 활동, 율동전환 뒤 곧 재발하면 자동능을 시사한다 [[harrison-22: 255장 p.1938]].
- 베타차단제·칼슘통로차단제는 방실 차단을 늘려 심실 반응을 늦추고 견디기 쉽게 하지만 큰 용량이 필요할 때가 있다 [[harrison-22: 255장 p.1938]].
- 재발하면 베타차단제, 딜티아젬·베라파밀, 플레카이니드·프로파페논·디소피라미드·소탈롤·아미오다론이 듣지만 독성·부작용으로 장기 사용을 피하는 경우가 많다 [[harrison-22: 255장 p.1938]].
- 카테터 절제는 > 80 % 에서 효과가 있고, 약이 듣지 않거나 원하지 않는 재발성 유증상 심방빈맥과 빈맥 유발 심근병증을 일으키는 지속형에 권고한다 [[harrison-22: 255장 p.1938]].

## 권고와 예외
- 활동 심전도에서 흔히 보이는 무증상 비지속 심방빈맥은 「SVT」로 보고돼도 치료를 권고하지 않는다. 다만 잦은 심방 기외수축·짧은 심방빈맥이 증상을 일으키면 국소 심방빈맥과 같은 치료가 필요할 수 있다 [[harrison-22: 255장 p.1937]].
- 유발 인자와 병발 질환을 찾아 고치고 바탕 심장병을 배제한다 [[harrison-22: 255장 p.1938]].
- 심방세동·심방조동의 전구가 될 수 있지만 뇌졸중 위험과 장기 항응고 적응은 불분명하고 심방세동과 같다고 보지 않는다 [[harrison-22: 255장 p.1938]].

## 시험 쟁점 — 충돌·맥락·새 근거
- 해당 없음(대조: 해리슨 22판 255장 p.1937~1938)
