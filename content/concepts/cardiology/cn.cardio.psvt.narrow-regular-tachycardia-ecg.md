---
id: cn.cardio.psvt.narrow-regular-tachycardia-ecg
type: concept
topic: Cardiology
see_also: [Emergency Medicine]
date: 2026-11-09
updated: 2026-11-09
version: 2
outline: h249            # 기본틀 슬롯 — 해리슨 21판 249장(22판 256장) Paroxysmal Supraventricular Tachycardias
confidence: medium
review_status: unreviewed
note_form: 2
title: "발작성 상심실빈맥 — P파 없는 규칙적 좁은 QRS 빈맥"
objective: "규칙적인 좁은 QRS 빈맥에서 박동수·P파 위치·조동파 유무로 발작성 상심실빈맥을 판독하고 2:1 심방조동·심방세동·동빈맥·심실빈맥과 가른다"
objective_kind: 진단
condition: 발작성 상심실빈맥(paroxysmal supraventricular tachycardia, PSVT) — 방실결절 회귀빈맥(AVNRT)·방실 회귀빈맥(AVRT)
exams: [kmle, usmle]
summary:
  - "결론: 갑자기 시작한 규칙적 좁은 QRS 빈맥 + QRS 앞 P파 없음 + 조동파 없음 = 발작성 상심실빈맥(PSVT)."
  - "시험 단서: 「갑자기 시작·저절로 멎은 두근거림」, 목의 두근거림(cannon a파), 박동수 150 에 고정되지 않음."
  - "왜: 방실결절 회귀에서는 심방과 심실이 거의 동시에 탈분극해 역행 P파가 QRS 안이나 바로 끝에 숨는다."
  - "2:1 심방조동은 심방 240~300회/분의 절반 — 심실 140~150회/분에 고정, II·III·aVF 톱니파."
  - "불규칙하면 심방세동, QRS 가 넓으면 넓은 QRS 빈맥(심실빈맥으로 보고 처치)으로 따로 판단한다."
pitfalls:
  - contrast: "2:1 심방조동 vs 발작성 상심실빈맥"
    point: "둘 다 규칙적 좁은 QRS 빈맥이다. 전형적 조동은 심방 240~300회/분이 2:1 로 내려와 심실 140~150회/분에 머물고, II·III·aVF 에 음성 톱니파가 T파와 겹쳐 숨는다. 박동수가 150 에서 벗어나고(예: 170~200) 하벽 유도 기준선에 톱니가 없으면 PSVT 가 먼저다."
    exception: "항부정맥제·심방 질환이 있으면 조동의 심방 박동수가 느려질 수 있다 — 애매하면 미주신경 자극·아데노신으로 방실전도를 잠깐 막아 조동파를 드러낸다."
    cites: ["harrison-22: 257장 p.1943", "harrison-22: 256장 p.1942"]
    covers: ["imaging-2026-0582:C"]
  - contrast: "빠른 심실 반응의 심방세동 vs PSVT"
    point: "심방세동은 R-R 간격이 불규칙하다. 박동수가 빨라 언뜻 규칙적으로 보여도 긴 리듬 띠에서 간격을 재 보면 가를 수 있다. PSVT 는 R-R 이 고르다."
    cites: ["harrison-22: 256장 p.1943"]
  - contrast: "동빈맥 vs PSVT"
    point: "동빈맥은 QRS 마다 앞에 II 양성 P파가 있고, 서서히 빨라지고 서서히 느려진다(발열·빈혈·통증 같은 원인). PSVT 는 갑자기 켜지고 꺼지며 QRS 앞 P파가 없다."
    cites: ["harrison-22: 256장 p.1939"]
  - contrast: "심실빈맥 vs PSVT"
    point: "QRS 가 좁으면(< 120 ms) 흥분이 히스-푸르키네 계를 타고 내려온 것이다 — 심실빈맥이 아니다. 넓은 QRS 빈맥은 각차단 변행전도·조기흥분 빈맥과 함께 감별하되 증명되기 전까지 심실빈맥으로 다룬다."
    cites: ["harrison-22: 256장 p.1943"]
tables:
  - id: narrow-regular
    section: "가르는 소견 — 박동수·P파·톱니파"
    title: "규칙적 좁은 QRS 빈맥 — 무엇이 가르나"
    role: differential
    span: column
    columns: ["판독", "박동수·시작", "P파 · 심방파"]
    rows:
      - ["방실결절 회귀빈맥(AVNRT)", "갑자기 시작·종료", "QRS 안이나 끝 — V1 가성 r′·II·III·aVF 가성 S [[harrison-22: 256장 p.1939]]"]
      - ["정방향 방실 회귀빈맥(AVRT)", "갑자기 시작·종료", "QRS 뒤 ST 분절 안(R-P < P-R) [[harrison-22: 256장 p.1941]]"]
      - ["2:1 심방조동", "140~150회/분에 고정", "II·III·aVF 음성 톱니파, 심방 240~300회/분 [[harrison-22: 257장 p.1943]]"]
      - ["심방빈맥", "다양", "QRS 앞 다른 모양 P파, 등전위 구간 [[harrison-22: 256장 p.1938]]"]
      - ["동빈맥", "서서히 변함", "QRS 앞 정상 P파"]
criteria:
  - id: avnrt-p
    name: 방실결절 회귀빈맥의 P파 위치
    kind: 진단 소견
    population: "규칙적 좁은 QRS 빈맥"
    statement: "전형적 방실결절 회귀빈맥은 심방과 심실이 거의 동시에 활성화되어 P파가 QRS 중·직전·직후에 그려져 잘 안 보이고, 흔히 QRS 끝에서 V1 가성 r′·II·III·aVF 가성 S파로 보인다 [[harrison-22: 256장 p.1939]]"
    exceptions: "비전형 형태는 P파가 QRS 사이 아무 곳에나 늦게 와 하벽 유도 역위 P파가 다음 T파 안에 보인다 [[harrison-22: 256장 p.1939]]"
    source: harrison-22
    basis: current
    exams: [kmle, usmle]
  - id: flutter-21
    name: 2:1 심방조동
    kind: 진단 소견
    population: "규칙적 좁은 QRS 빈맥"
    statement: "전형적 심방조동은 심방 240~300회/분, 흔히 2:1 방실전도로 심실 140~150회/분의 규칙적 빈맥이 되고 조동파가 T파와 구별하기 어렵다. 방실전도를 늘리는 조작이 조동파를 드러낸다 [[harrison-22: 257장 p.1943]]"
    exceptions: "심방 질환·항부정맥제가 있으면 심방 박동수가 더 느릴 수 있다 [[harrison-22: 257장 p.1943]]"
    source: harrison-22
    basis: current
    exams: [kmle, usmle]
sources:
  - id: harrison-22
    org: "McGraw Hill"
    title: "Harrison's Principles of Internal Medicine, 22nd ed. — Chapter 256: Paroxysmal Supraventricular Tachycardias (p.1938–1943, 257장 첫 쪽 포함)"
    kind: textbook
    year: 2025
    citation: "Harrison's Principles of Internal Medicine, 22e. 256장 p.1938–1943"
    checked_at: 2026-11-09
    checked: "드라이브 22판 장별 문서 H22_256 본문 대조 — 심방빈맥은 등전위 구간이 있는 뚜렷한 P파, 방실차단 조작이 P파를 드러냄(p.1938) · AVNRT 가 PSVT 의 가장 흔한 형태, 20~40대·여성에 흔함, 노인에서 빠르면 협심증·저혈압·실신, 심방·심실 동시 활성화로 P파가 QRS 안·끝에 숨어 V1 가성 r′·하벽 가성 S, 비전형은 T파 안 역위 P파, cannon a파로 목 두근거림, 방실결절 차단이 빈맥을 끝냄(p.1939) · 정방향 AVRT 는 P파가 항상 QRS 뒤 ST 분절 안(R-P < P-R)(p.1941) · 급성 처치: 12유도 기록, 불안정하면 동기화 전기충격, 안정하면 미주신경 자극 → 아데노신, 방실차단으로 잠깐 느려지며 P파가 드러나면 심방빈맥·조동(p.1942) · 넓은 QRS 빈맥은 증명 전까지 심실빈맥으로, 매우 불규칙한 넓은 QRS 는 조기흥분 심방세동(p.1943) · 257장: 조동 심방 240~300회/분, 2:1 전도로 140~150회/분, 하벽 음성 톱니파(p.1943)"
    verified: text
diagram:
  title: "규칙적 좁은 QRS 빈맥 — 무엇인가"
  nodes:
    - {id: start, kind: start, text: "빠른 맥, QRS < 120 ms"}
    - {id: regular, kind: decision, text: "R-R 간격이 고른가?"}
    - {id: af, kind: end, text: "심방세동(빠른 심실 반응)"}
    - {id: pwave, kind: decision, text: "QRS 앞에 정상 P파가 있나?"}
    - {id: sinus, kind: end, text: "동빈맥 — 원인을 찾는다"}
    - {id: saw, kind: decision, text: "하벽 톱니파·150회/분 고정?"}
    - {id: vagal, kind: info, text: "미주신경 자극·아데노신 중 기록"}
    - {id: flutter, kind: end, text: "2:1 심방조동"}
    - {id: psvt, kind: end, text: "발작성 상심실빈맥"}
  edges:
    - {from: start, to: regular}
    - {from: regular, to: af, label: "불규칙"}
    - {from: regular, to: pwave, label: "규칙"}
    - {from: pwave, to: sinus, label: "있음"}
    - {from: pwave, to: saw, label: "없음"}
    - {from: saw, to: flutter, label: "예"}
    - {from: saw, to: psvt, label: "아니오"}
    - {from: saw, to: vagal, label: "애매"}
    - {from: vagal, to: psvt, label: "갑자기 멎음"}
    - {from: vagal, to: flutter, label: "톱니파 드러남"}
diagram_notes:
  - "방실차단으로 잠깐 느려졌다 다시 빨라지며 P파가 계속 보이면 심방빈맥이나 심방조동이다 [[harrison-22: 256장 p.1942]]."
  - "QRS ≥ 120 ms 인 빈맥은 이 도식 밖 — 증명되기 전까지 심실빈맥으로 다룬다 [[harrison-22: 256장 p.1943]]."
  - "불안정(저혈압과 의식저하·호흡곤란)하면 판독보다 QRS 동기화 전기적 동율동전환이 먼저다 [[harrison-22: 256장 p.1942]]."
checks:
  - q: "규칙적 좁은 QRS 빈맥 170회/분, QRS 앞 P파 없음, V1 끝에 작은 r′, 하벽 톱니파 없음. 판독은?"
    a: "발작성 상심실빈맥(전형적 방실결절 회귀빈맥). V1 의 r′ 은 QRS 끝에 숨은 역행 P파다."
  - q: "2:1 심방조동을 의심하게 하는 박동수와 유도는?"
    a: "심실 140~150회/분에 고정, II·III·aVF 의 음성 톱니파(심방 240~300회/분)."
variants:
  - id: v1
    of: imaging-2026-0582
    flip: true
    changed: "박동수 170회/분·하벽 톱니파 없음 → 150회/분에 고정·II·III·aVF 음성 톱니파·심방 300회/분 ⇒ 정답이 발작성 상심실빈맥에서 2:1 전도의 심방조동으로"
    context: "같은 응급실 상황, 소견을 글로 바꾼 변형(그림 없음)"
    stem: "76세 여자가 2시간 전부터 가슴이 빠르게 뛴다며 응급실에 왔다. 고혈압과 만성 폐쇄성 폐질환으로 치료받고 있다. 흉통은 없고 약간 숨이 차다. 혈압 132/78 mmHg, 호흡 20회/분, 산소포화도 94 % 이다. 맥은 빠르고 규칙적이다. 혈청 칼륨 4.2 mEq/L 이다. 12유도 심전도에서 QRS 폭은 0.08초, 심실 박동수는 150회/분으로 기록 내내 변하지 않으며, II·III·aVF 에서 기준선이 등전위 구간 없이 음성 톱니 모양으로 이어지고 그 톱니의 주기는 300회/분이다. 심전도 판독으로 가장 적절한 것은?"
    choices: ["A. 발작성 상심실빈맥", "B. 동빈맥", "C. 2:1 전도의 심방조동", "D. 빠른 심실 반응의 심방세동", "E. 심실빈맥"]
    answer: "C"
    explanation: "하벽 유도의 음성 톱니파가 300회/분이고 심실이 그 절반인 150회/분에 고정되어 있으니 2:1 전도의 전형적 심방조동이다. 원래 문항은 박동수가 150 에서 벗어난 170회/분이고 톱니파가 없어 발작성 상심실빈맥이었다. R-R 이 규칙적이라 심방세동이 아니고, QRS 가 좁아 심실빈맥이 아니다."
    kind: application
  - id: v2
    of: imaging-2026-0582
    flip: false
    changed: "74세 여자·텔레비전 시청 중·심전도 그림 → 28세 남자·계단을 오르다가·소견을 글로 제시 ⇒ 갑작스런 시작·규칙적 좁은 QRS·P파 없음·톱니파 없음이라는 결정 단서는 같아 답은 그대로 발작성 상심실빈맥"
    context: "겉모습만 바꾼 글 변형(그림 없음)"
    stem: "28세 남자가 회사 계단을 오르다가 갑자기 가슴이 빠르게 뛰기 시작해 40분 뒤 응급실에 왔다. 고등학생 때부터 비슷한 일이 몇 번 있었는데 숨을 참으면 멎었다고 한다. 목이 두근거리는 느낌이 있다. 혈압 122/74 mmHg, 호흡 18회/분이다. 맥은 빠르고 규칙적이다. 혈청 칼륨 4.0 mEq/L 이다. 12유도 심전도에서 QRS 폭은 0.08초, 심실 박동수는 190회/분으로 규칙적이며, QRS 앞에 P파가 보이지 않고 V1 의 QRS 끝에 작은 r′ 이, II·III·aVF 에 작은 S파가 있다. 기준선에 톱니 모양 파형은 없다. 심전도 판독으로 가장 적절한 것은?"
    choices: ["A. 심실빈맥", "B. 2:1 전도의 심방조동", "C. 빠른 심실 반응의 심방세동", "D. 동빈맥", "E. 발작성 상심실빈맥"]
    answer: "E"
    explanation: "나이·성별·발생 상황이 바뀌었지만 결정 단서는 같다 — 갑자기 시작한 규칙적 좁은 QRS 빈맥, QRS 앞 P파 없음, 톱니파 없음, 박동수가 150 에 고정되지 않음. V1 끝의 r′ 과 하벽의 작은 S 는 QRS 끝에 숨은 역행 P파로 전형적 방실결절 회귀빈맥의 모습이다. 목 두근거림은 닫힌 삼첨판에 심방이 수축해 생기는 cannon a파다."
    kind: application
figures:
- id: f1
  file: docs/assets/figures/ptbxl-07889.png
  kind: ecg
  at: 기전 — 방실결절 안의 두 길에서 숨은 P파로
  shows: 발작성 상심실빈맥 — 규칙적인 좁은 QRS 빈맥, QRS 앞 P파 없음
  look_for:
  - 긴 II 리듬 띠의 고른 R-R 간격과 좁은 QRS
  - II·III·aVF 기준선에 톱니 모양 조동파가 없음
  label: paroxysmal supraventricular tachycardia (SCP PSVT, 가능도 100)
  label_basis: dataset_expert
  reference: 심장내과 전문의의 SCP-ECG 판독을 두 번째 전문의가 검증 — 해당 진술의 가능도 100 인 기록만
  paper: Wagner P 외. PTB-XL, a large publicly available electrocardiography dataset. Sci Data 2020;7:154
  doi: 10.1038/s41597-020-0495-6
  credit: PTB-XL ECG dataset v1.0.3 (PhysioNet, CC BY 4.0) · record 7889
  license: Creative Commons Attribution 4.0 International
  url: https://physionet.org/content/ptb-xl/1.0.3/records500/07000/#files-panel
  asset: PTBXL-07889
  paper_cited_by: 1213
---

## 판단 — 왜 발작성 상심실빈맥이 먼저인가
- **규칙성**: R-R 이 고르면 심방세동이 아니다. **폭**: QRS < 120 ms 면 흥분이 히스-푸르키네 계로 내려온 상심실성 빈맥이다 [[harrison-22: 256장 p.1943]].
- **P파**: QRS 마다 앞에 정상 P파가 있으면 동빈맥, 없으면 P파가 QRS 안·뒤에 숨은 회귀빈맥을 먼저 생각한다 [[harrison-22: 256장 p.1939]].
- **박동수와 톱니파**: 140~150회/분에 고정되고 하벽에 톱니파가 있으면 2:1 심방조동, 그렇지 않으면 PSVT [[harrison-22: 257장 p.1943]].
- 애매하면 미주신경 자극·아데노신을 주며 기록한다 — 빈맥이 갑자기 멎으면 방실결절 의존(PSVT), 잠깐 느려지며 심방파가 드러나면 심방빈맥·조동 [[harrison-22: 256장 p.1942]].

## 기전 — 방실결절 안의 두 길에서 숨은 P파로
방실결절로 들어가는 길이 둘(느린 길·빠른 길)이면, 흥분이 느린 길로 내려가 빠른 길로 거꾸로 올라오는 회귀가 생긴다 — 방실결절 회귀빈맥(atrioventricular nodal reentry tachycardia, AVNRT)으로 PSVT 의 가장 흔한 형태이고 20~40대·여성에 많다 [[harrison-22: 256장 p.1939]]. 결절에서 심방까지와 심실까지의 시간이 비슷해 심방과 심실이 거의 동시에 탈분극하므로 P파가 QRS 속에 묻히거나 끝에 붙어 V1 의 가성 r′, II·III·aVF 의 가성 S파로 보인다 [[harrison-22: 256장 p.1939]]. 닫힌 삼첨판에 심방이 수축하면 목정맥에 cannon a파가 생겨 목이 두근거린다 [[harrison-22: 256장 p.1939]]. 부전도로를 거꾸로 올라오는 정방향 방실 회귀빈맥(atrioventricular reciprocating tachycardia, AVRT)은 심실이 먼저 깨야 하므로 P파가 늘 QRS 뒤, ST 분절 안에 온다 [[harrison-22: 256장 p.1941]].

## 가르는 소견 — 박동수·P파·톱니파
- 전형적 심방조동은 삼첨판륜을 도는 거대 회귀로 심방 240~300회/분, II·III·aVF 음성 톱니파를 만든다. 2:1 이면 심실 140~150회/분이고 조동파가 T파와 겹쳐 놓치기 쉽다 [[harrison-22: 257장 p.1943]].
- 회로가 심방 안에서 닫혀 있는 심방빈맥·조동은 방실차단을 일으켜도 멎지 않고 심방파만 드러난다. 방실결절이 회로에 들어 있는 AVNRT·AVRT 는 방실차단이 빈맥을 끝낸다 [[harrison-22: 256장 p.1939]].
- 정상 소견의 해석 한계: 한 유도에서 P파가 안 보여도 없는 것이 아니다 — V1 끝·하벽 끝부분과 T파 안을 같이 본다 [[harrison-22: 256장 p.1939]].

## 권고와 예외
- 판독을 위해 12유도를 기록하되, 저혈압과 의식저하·호흡곤란이 있으면 QRS 동기화 전기적 동율동전환이 먼저다 [[harrison-22: 256장 p.1942]].
- 안정하면 미주신경 자극(경동맥 잡음·뇌졸중 병력이 없을 때 경동맥동 마사지, 협조되면 발살바) → 정맥 아데노신 순서다 [[harrison-22: 256장 p.1942]]. 아데노신은 심장이식 환자에서 금기이고, 최대 15 % 에서 짧은 심방세동을 일으켜 WPW 에서는 조심한다 [[harrison-22: 256장 p.1943]].
- 노인에서 빠른 PSVT 는 협심증·폐부종·저혈압·실신을 일으킬 수 있다 [[harrison-22: 256장 p.1939]].

## 시험 쟁점 — 충돌·맥락·새 근거
- 해당 없음(대조: 해리슨 22판 256장 p.1938–1943, 257장 p.1943)
