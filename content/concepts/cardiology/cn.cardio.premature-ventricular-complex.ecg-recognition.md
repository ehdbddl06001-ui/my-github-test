---
id: cn.cardio.premature-ventricular-complex.ecg-recognition
type: concept
topic: Cardiology
see_also: []
date: 2026-11-01
updated: 2026-11-01
version: 2
outline: h252
confidence: medium
review_status: unreviewed
note_form: 2
title: "심실 기외수축 — 조기·P파 없음·넓은 QRS"
objective: "심전도에서 조기에 오는 넓고 기이한 QRS·앞선 조기 P파 없음·반대 방향 T파로 심실 기외수축을 읽고 각차단·변행전도 심방 기외수축과 가른다"
objective_kind: 진단
condition: 심실 기외수축(premature ventricular complex, PVC)
exams: [kmle, usmle]
summary:
  - "결론: 예정보다 일찍 온 넓고(> 0.12초) 기이한 QRS + 앞에 조기 P파 없음 + 반대 방향 T파 = 심실 기외수축."
  - "시험 단서: 「쿵 하고 내려앉는」 두근거림, 가끔 불규칙한 맥, 리듬 스트립 중간에 끼어든 넓은 박동 하나."
  - "왜: 심실 근육에서 시작한 흥분은 퍼킨제 전도계를 못 타 천천히 번진다 — 그래서 넓고, 재분극도 거꾸로 선다."
  - "넓다는 것만으로 각차단이 아니다 — 각차단은 제때 오고 정상 PR 의 P파가 앞에 있다."
  - "구조 심질환·심전도 이상이 없으면 대개 양성 — 안심시키기와 카페인·술 줄이기."
pitfalls:
  - contrast: "간헐적 좌각차단 vs 심실 기외수축"
    point: "둘 다 QRS 가 넓지만, 각차단 박동은 예정된 때에 오고 앞에 정상 PR 간격의 P파가 있다. 넓은 박동이 일찍 오고 앞에 P파가 없으면 심실에서 시작한 박동이다. 먼저 「언제 왔나」와 「앞에 P파가 있나」를 본다."
    cites: ["harrison-22: 259장 p.1954"]
    covers: ["imaging-2026-0491:A"]
  - contrast: "변행전도 심방 기외수축 vs 심실 기외수축"
    point: "변행전도면 넓은 박동 바로 앞 T파에 조기 P파가 겹쳐 그 T파 모양이 다른 T파와 달라지고, QRS 가 대개 전형적 우각차단 모양이다. 앞 T파가 다른 T파와 같으면 숨은 P파가 없다."
  - contrast: "넓은 박동 하나 = 비지속성 심실빈맥?"
    point: "심실빈맥은 3개 이상 연달아, 분당 100회 넘게. 하나는 기외수축, 둘은 쌍발(couplet)이다."
    cites: ["harrison-22: 259장 p.1954"]
tables:
  - id: wide-beat
    section: "가르는 소견 — 넓은 박동 하나를 만났을 때"
    title: "넓은 QRS 박동 — 무엇이 가르나"
    role: differential
    span: column
    columns: ["판독", "때", "앞의 P파"]
    rows:
      - ["심실 기외수축", "조기", "없음 · T파는 QRS 와 반대 [[harrison-22: 259장 p.1954]]"]
      - ["변행전도 심방 기외수축", "조기", "있음(앞 T파에 묻혀 T 모양 변형) · 대개 우각차단 모양"]
      - ["간헐적 각차단", "제때", "있음, PR 정상"]
      - ["비지속성 심실빈맥", "3개 이상 연속, > 100회/분", "없음 · 30초 안에 멈춤 [[harrison-22: 259장 p.1955]]"]
criteria:
  - id: pvc-def
    name: 심실 기외수축·심실빈맥 정의
    kind: 진단 기준
    population: "넓은 QRS 박동이 보이는 심전도"
    statement: "심실 기외수축은 다음 상심실 박동보다 일찍 오는 단일 심실 박동이다. 둘 연속은 쌍발, 3개 이상·분당 100회 초과는 심실빈맥이고 30초 안에 저절로 멈추면 비지속성이다 [[harrison-22: 259장 p.1954–1955]]"
    exceptions: "QRS 는 대개 0.12초를 넘지만 드물게 좁을 수 있다 [[harrison-22: 259장 p.1954]]"
    source: harrison-22
    basis: current
    exams: [kmle, usmle]
sources:
  - id: harrison-22
    org: "McGraw Hill"
    title: "Harrison's Principles of Internal Medicine, 22nd ed. — Chapter 259: Approach to Ventricular Arrhythmias · Chapter 260: PVCs, NSVT, and AIVR"
    kind: textbook
    year: 2025
    citation: "Harrison's Principles of Internal Medicine, 22e. 259장 p.1954–1957 · 260장 p.1960"
    checked_at: 2026-11-01
    checked: "드라이브 22판 장별 문서 H22_259 본문 대조 — 심실 기원 흥분은 퍼킨제계보다 느리게 번져 QRS > 0.12초, PVC 정의(다음 상심실 박동보다 일찍 오는 단일 박동)·단일/다형·쌍발, VT = 3개 이상 > 100회/분(p.1954) · 비지속성 < 30초(p.1955) · QRS 모양으로 기원(V1 LBBB 모양 = 우심실·중격, RBBB 모양 = 좌심실), 이분맥 시 가성 서맥(p.1956) · 정상 심장·정상 심전도면 안심과 카페인·술 제거, 무증상 증상 평가에 12유도 심전도·심초음파(p.1957) · 260장: PVC 는 교감 자극·허혈·저산소·전해질 이상 신호, 저칼륨혈증 교정, 다형·RBBB 모양은 구조 질환 시사(p.1960). 변행전도 심방 기외수축의 T파 속 P파·보상 휴지는 이 장에 없다(원문 미대조)"
    verified: text
diagram:
  title: "넓은 QRS 박동 하나 — 어디서 왔나"
  nodes:
    - {id: start, kind: start, text: "리듬 중간에 넓은 QRS 박동"}
    - {id: early, kind: decision, text: "예정보다 일찍 왔나?"}
    - {id: bbb, kind: end, text: "간헐적 각차단 쪽"}
    - {id: pwave, kind: decision, text: "바로 앞 T파에 조기 P파가 숨어 있나?"}
    - {id: look, kind: info, text: "앞 T파를 다른 T파와 겹쳐 비교"}
    - {id: apc, kind: end, text: "변행전도 심방 기외수축"}
    - {id: count, kind: decision, text: "3개 이상 연달아 나오나?"}
    - {id: pvc, kind: end, text: "심실 기외수축"}
    - {id: vt, kind: alert, text: "심실빈맥 — 지속 시간·혈역학 평가"}
  edges:
    - {from: start, to: early}
    - {from: early, to: pwave, label: "예"}
    - {from: early, to: bbb, label: "제때"}
    - {from: pwave, to: apc, label: "있음"}
    - {from: pwave, to: count, label: "없음"}
    - {from: pwave, to: look, label: "모르겠음"}
    - {from: look, to: apc, label: "T 모양 다름"}
    - {from: look, to: count, label: "T 모양 같음"}
    - {from: count, to: pvc, label: "하나·둘"}
    - {from: count, to: vt, label: "3개 이상"}
diagram_notes:
  - "기외수축 뒤 휴지는 흔히 완전 보상 — 동방결절이 재설정되지 않아 다음 동박동이 제 리듬대로 온다(원문 미대조)."
  - "V1 에서 좌각차단 모양이면 우심실·중격 기원(정상 심장에 흔함), 우각차단 모양이면 좌심실 기원(구조 질환 가능성 더 높음) [[harrison-22: 260장 p.1960]]."
  - "이분맥이면 기외수축이 맥박을 만들지 못해 맥박 수가 가짜로 느리게 잡힐 수 있다 [[harrison-22: 259장 p.1956]]."
checks:
  - q: "넓은 QRS 박동이 일찍 왔고 앞에 P파가 없다. 판독은?"
    a: "심실 기외수축. 넓은 이유는 퍼킨제계를 못 타고 근육으로 천천히 번지기 때문이다."
  - q: "간헐적 각차단과 무엇으로 가르나?"
    a: "때와 P파. 각차단 박동은 제때 오고 정상 PR 의 P파가 앞에 있다."
variants:
  - id: v1
    of: imaging-2026-0491
    flip: true
    changed: "넓은 박동 앞 T파가 다른 T파와 같음(숨은 P파 없음)·기이한 QRS → 넓은 박동 바로 앞 T파 끝이 뾰족하게 솟아 다른 T파와 모양이 다르고 QRS 가 전형적 우각차단 모양(rSR′) ⇒ 정답이 심실 기외수축에서 변행전도를 동반한 심방 기외수축으로"
    context: "같은 증상, 넓은 박동 앞에 조기 P파 단서를 넣은 글 변형(그림 없음)"
    stem: "39세 여자가 한 달 전부터 가끔 가슴이 덜컥하는 느낌으로 왔다. 흉통·실신은 없고 혈압 116/70 mmHg, 맥박 66회/분으로 가끔 불규칙하다. 혈청 칼륨은 4.2 mEq/L 이다. 12유도 심전도의 리듬 스트립에서 동리듬 사이에 일찍 오는 넓은 QRS 박동이 하나 있다. 그 박동 바로 앞 T파의 끝이 뾰족하게 솟아 다른 T파와 모양이 다르고, 넓은 박동의 QRS 는 V1 에서 rSR′ 모양이다. 심전도 판독으로 가장 적절한 것은?"
    choices: ["A. 간헐적 좌각차단", "B. 비지속성 심실빈맥", "C. 심실 기외수축", "D. 변행전도를 동반한 심방 기외수축", "E. 2도 방실차단(Mobitz II형)"]
    answer: "D"
    explanation: "넓은 박동이 일찍 온 것은 같지만, 바로 앞 T파 모양이 달라진 것은 그 T파 위에 조기 P파가 겹쳤다는 뜻이다 — 박동은 심방에서 시작했고, 아직 불응기인 우각을 지나지 못해 우각차단 모양(rSR′)으로 넓어졌다. 앞 T파가 다른 T파와 같았다면 숨은 P파가 없어 심실 기외수축이다."
    kind: application
  - id: v2
    of: imaging-2026-0491
    flip: false
    changed: "41세 여자·쉴 때 두근거림·커피 → 23세 남자 대학생·시험 기간 에너지음료 뒤 건너뛰는 느낌, 소견을 글로 제시 ⇒ 조기 + 앞 P파 없음 + 넓고 기이한 QRS + 반대 방향 T파라는 결정 단서는 같아 답은 그대로 심실 기외수축"
    context: "겉모습만 바꾼 글 변형(그림 없음)"
    stem: "23세 남자 대학생이 시험 기간에 에너지음료를 하루 4캔씩 마시면서 심장이 가끔 한 번 건너뛰는 느낌이 들어 왔다. 실신·흉통·운동 시 호흡곤란은 없고 가족 중 돌연사는 없다. 맥박 74회/분으로 가끔 쉬었다 뛴다. 심잡음은 없다. 12유도 심전도의 리듬 스트립에서 동리듬 사이에 예정보다 일찍 오는 박동이 두 번 보인다. 그 박동의 QRS 는 0.14초로 넓고 모양이 기이하며, 앞의 T파는 다른 T파와 모양이 같고, 뒤따르는 T파는 QRS 와 반대 방향이다. 심전도 판독으로 가장 적절한 것은?"
    choices: ["A. 심실 기외수축", "B. 간헐적 우각차단", "C. 비지속성 심실빈맥", "D. 변행전도를 동반한 심방 기외수축", "E. 심실 쌍발"]
    answer: "A"
    explanation: "나이·성별·유발 요인이 바뀌었지만 결정 단서는 같다 — 일찍 온 넓고 기이한 QRS, 앞 T파 모양이 같아 숨은 조기 P파가 없음, 반대 방향 T파. 따로 떨어진 두 박동이라 쌍발(연속 2개)도 심실빈맥(3개 이상)도 아니다. 구조 이상 단서가 없으면 안심시키고 자극제를 줄인다."
    kind: application
figures:
- id: f1
  file: docs/assets/figures/ptbxl-18790.png
  kind: ecg
  at: 기전 — 퍼킨제 고속도로를 못 탄 흥분
  shows: 동리듬 사이에 끼어든 심실 기외수축
  look_for:
  - II 리듬 스트립 중간·뒤쪽의 일찍 온 넓고 기이한 QRS
  - 넓은 박동 뒤 QRS 와 반대 방향의 T파
  label: ventricular premature complex (SCP PVC, 가능도 100)
  label_basis: dataset_expert
  reference: 심장내과 전문의의 SCP-ECG 판독을 두 번째 전문의가 검증 — 해당 진술의 가능도 100 인 기록만
  paper: Wagner P 외. PTB-XL, a large publicly available electrocardiography dataset. Sci Data 2020;7:154
  doi: 10.1038/s41597-020-0495-6
  credit: PTB-XL ECG dataset v1.0.3 (PhysioNet, CC BY 4.0) · record 18790
  license: Creative Commons Attribution 4.0 International
  url: https://physionet.org/content/ptb-xl/1.0.3/records500/18000/#files-panel
  asset: PTBXL-18790
  paper_cited_by: 1213
---

## 판단 — 넓은 박동 하나를 읽는 순서
- **언제 왔나**: 예정보다 일찍 온 박동이 기외수축이다. 제때 온 넓은 박동은 각차단 쪽이다.
- **앞에 P파가 있나**: 앞 T파가 다른 T파와 같으면 숨은 조기 P파가 없다 — 심실 기원.
- **몇 개인가**: 하나는 기외수축, 둘은 쌍발, 3개 이상·100회 초과는 심실빈맥이다 [[harrison-22: 259장 p.1954]].

## 기전 — 퍼킨제 고속도로를 못 탄 흥분
정상 흥분은 히스-퍼킨제계를 타고 두 심실을 거의 동시에 탈분극시켜 QRS 가 좁다. 심실 근육의 한 곳에서 시작한 흥분은 근육에서 근육으로 천천히 번져 QRS 가 대개 0.12초를 넘게 넓어진다 [[harrison-22: 259장 p.1954]]. 탈분극 순서가 바뀌면 재분극 순서도 따라 바뀌어 T파가 QRS 와 반대로 선다(이차성 ST-T 변화, 허혈이 아니다). 처음 흥분한 자리가 QRS 모양을 정하므로 V1 모양과 전두면 축으로 기원 위치를 짐작한다 [[harrison-22: 259장 p.1956]].

## 가르는 소견 — 넓은 박동 하나를 만났을 때
- 다형(모양이 여럿)이거나 V1 우각차단 모양이면 구조 심질환 가능성이 더 높다 [[harrison-22: 260장 p.1960]].
- 기외수축은 교감 자극·허혈·저산소·전해질 이상(특히 저칼륨혈증)의 신호일 수 있다 [[harrison-22: 260장 p.1960]].

## 권고와 예외
- 구조 심질환이 없고 평소 심전도가 정상이면 안심시키기와 카페인·술 같은 악화 요인 제거로 충분한 경우가 많다 [[harrison-22: 259장 p.1957]].
- 실신·운동 중 증상·돌연사 가족력·심전도 이상이 있으면 심초음파 등으로 구조 질환을 평가한다 [[harrison-22: 259장 p.1957]].

## 시험 쟁점 — 충돌·맥락·새 근거
- 해당 없음(대조: 해리슨 22판 259장 p.1954–1957 · 260장 p.1960)
