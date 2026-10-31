---
id: cn.cardio.ischemic-ecg-localization.culprit-artery
type: concept
topic: Cardiology
see_also: []
date: 2026-11-01
updated: 2026-11-01
version: 2
outline: h240
confidence: medium
review_status: unreviewed
note_form: 2
title: "허혈 심전도 위치 — 유도로 책임 혈관을 고른다"
objective: "허혈성 ST-T 변화가 모인 유도로 심근 벽을 정하고 책임 관상동맥(좌전하행지·회선지·우관상동맥)을 고른다"
objective_kind: 진단
condition: 관상동맥 질환의 허혈성 심전도 변화(전벽·하벽·측벽)
exams: [kmle, usmle]
summary:
  - "결론: V1~V4(± V5)·I·aVL = 전벽 → 좌전하행지(LAD). II·III·aVF = 하벽 → 대개 우관상동맥(RCA)."
  - "시험 단서: 운동 시 흉부 압박(stable angina) + 통증 없을 때 V2~V4 중심의 T파 역위."
  - "왜: 흉부 유도는 바로 밑 벽을 본다 — 좌전하행지가 중격·전벽에, 대각지가 고위 측벽(aVL)에 피를 준다."
  - "회선지는 I·aVL·V5·V6 중심, 또는 V1~V3 의 거울상 ST 하강(후벽)."
  - "비ST상승 변화는 ST상승보다 위치를 덜 정확히 가리킨다 — 예외: 흉부 유도 깊은 T파 역위는 좌전하행지 심한 협착."
pitfalls:
  - contrast: "우관상동맥 vs 좌전하행지"
    point: "우관상동맥은 대개 하벽을 맡아 II·III·aVF 에 변화가 생긴다. 변화가 V2~V5·aVL 에 모여 있고 하벽 유도가 깨끗하면 전벽, 곧 좌전하행지다."
    cites: ["harrison-22: 247장 p.1872"]
    covers: ["imaging-2026-0493:D"]
  - contrast: "aVL 이 있으니 측벽 = 회선지?"
    point: "aVL 은 좌전하행지의 대각지 영역(고위 측벽)도 본다. 역위의 중심이 V2~V4 면 좌전하행지다. 회선지는 I·aVL·V5·V6 가 주이고 V2~V4 변화가 적다."
    cites: ["harrison-22: 247장 p.1873"]
tables:
  - id: territory
    section: "가르는 소견 — 유도 묶음과 혈관"
    title: "유도 → 벽 → 책임 혈관"
    role: differential
    span: column
    columns: ["유도", "벽", "흔한 책임 혈관"]
    rows:
      - ["V1~V4(± V5), I·aVL", "중격·전벽(첨부·측벽 포함)", "좌전하행지 [[harrison-22: 247장 p.1872]]"]
      - ["II·III·aVF", "하벽", "대개 우관상동맥(우세형에 따라 회선지)"]
      - ["I·aVL·V5·V6", "측벽", "회선지 또는 대각지"]
      - ["V1~V3 ST 하강·큰 R(거울상)", "후벽", "회선지·우관상동맥 [[harrison-22: 247장 p.1872]]"]
      - ["우측 흉부 유도 ST 상승", "우심실", "근위 우관상동맥 [[harrison-22: 247장 p.1872]]"]
criteria:
  - id: lad-twi
    name: 흉부 유도 깊은 T파 역위
    kind: 판독 기준
    population: "허혈성 흉통 환자"
    statement: "여러 흉부 유도(V1~V4, 때로 I·aVL)의 깊은 T파 역위는 대개 좌전하행지의 심한 협착을 뜻한다(Wellens T파) [[harrison-22: 247장 p.1873]]"
    exceptions: "T파 역위는 비대·각차단·약물·뇌출혈 등에서도 생긴다 — 임상과 함께 [[harrison-22: 247장 p.1874]]"
    source: harrison-22
    basis: current
    exams: [kmle, usmle]
sources:
  - id: harrison-22
    org: "McGraw Hill"
    title: "Harrison's Principles of Internal Medicine, 22nd ed. — Chapter 247: Electrocardiography"
    kind: textbook
    year: 2025
    citation: "Harrison's Principles of Internal Medicine, 22e. 247장 p.1872–1874"
    checked_at: 2026-11-01
    checked: "드라이브 22판 장별 문서 H22_247 본문 대조 — 경벽 허혈은 ST 상승, 내막하 허혈은 그 위 유도의 ST 하강, 유도는 비ST상승보다 ST상승 허혈의 위치를 더 잘 가리킴, 전벽(첨부·측벽 포함) = V1~V6·I·aVL, 하벽 = II·III·aVF, 후벽 = V1~V3 거울상 ST 하강, 우심실 = 우측 흉부 유도(p.1872) · 흉부 유도 깊은 T파 역위(V1~V4, 때로 I·aVL)는 대개 좌전하행지 심한 협착, Fig. 247-12 Wellens(p.1873) · 뇌출혈의 깊은 T파 역위 등 비허혈 원인(p.1874). 혈관별 벽 배정(우관상동맥=하벽, 회선지=측벽)과 대각지-aVL 연결은 이 장 본문에 명시되지 않음(원문 미대조)"
    verified: text
diagram:
  title: "허혈성 ST-T 변화 — 어느 혈관인가"
  nodes:
    - {id: start, kind: start, text: "허혈성 ST-T 변화가 있는 심전도"}
    - {id: where, kind: info, text: "변화가 모인 유도 묶음을 표시"}
    - {id: inf, kind: decision, text: "II·III·aVF 에 모여 있나?"}
    - {id: rca, kind: end, text: "하벽 — 대개 우관상동맥"}
    - {id: ant, kind: decision, text: "중심이 V1~V4 인가?"}
    - {id: lad, kind: end, text: "전벽 — 좌전하행지"}
    - {id: lat, kind: decision, text: "I·aVL·V5·V6 또는 V1~V3 거울상?"}
    - {id: lcx, kind: end, text: "측벽·후벽 — 회선지"}
    - {id: other, kind: alert, text: "비허혈 원인(비대·각차단·약물) 확인"}
  edges:
    - {from: start, to: where}
    - {from: where, to: inf}
    - {from: inf, to: rca, label: "예"}
    - {from: inf, to: ant, label: "아니오"}
    - {from: ant, to: lad, label: "예"}
    - {from: ant, to: lat, label: "아니오"}
    - {from: lat, to: lcx, label: "예"}
    - {from: lat, to: other, label: "아니오"}
diagram_notes:
  - "aVL 은 대각지(좌전하행지 가지)의 고위 측벽도 본다 — aVL 이 있다고 바로 회선지로 가지 않는다."
  - "하벽은 우세 혈관에 따라 회선지일 수도 있다. 하벽 + 서맥·방실차단은 우관상동맥 쪽 단서다."
  - "비ST상승 변화(T파 역위·ST 하강)는 ST 상승보다 위치를 덜 정확히 가리킨다 [[harrison-22: 247장 p.1872]]."
checks:
  - q: "V2~V5·aVL 의 T파 역위, 하벽 유도는 정상. 책임 혈관은?"
    a: "좌전하행지 — 중격·전벽과 대각지의 고위 측벽."
  - q: "II·III·aVF 의 ST 상승이면?"
    a: "하벽 — 대개 우관상동맥."
variants:
  - id: v1
    of: imaging-2026-0493
    flip: true
    changed: "T-wave inversion in aVL and V2–V5 → ST elevation in II, III, aVF with reciprocal ST depression in I and aVL and sinus bradycardia ⇒ the territory moves from anterior to inferior, so the answer changes from LAD to right coronary artery"
    context: "Same patient frame, ischemic changes moved to the inferior leads (text, no image)"
    stem: "A 64-year-old man comes to the emergency department because of crushing substernal chest pain that began 50 minutes ago while he was shoveling snow. He has hypertension and smokes 1 pack of cigarettes daily. His pulse is 52/min and blood pressure is 104/66 mm Hg. A 12-lead ECG shows sinus rhythm with 3-mm ST-segment elevation in leads II, III, and aVF and ST-segment depression in leads I and aVL. The precordial leads show no ST elevation. Which of the following coronary arteries is most likely occluded?"
    choices: ["A. Left internal mammary artery", "B. Left anterior descending artery", "C. Left circumflex artery", "D. Right coronary artery", "E. Left main coronary artery"]
    answer: "D"
    explanation: "The ischemic changes now sit in II, III, and aVF (inferior wall) with reciprocal depression in I and aVL, and the precordial leads are spared. The inferior wall is usually supplied by the right coronary artery, which in most people also supplies the sinoatrial and atrioventricular nodes — consistent with the bradycardia. Changes centered on V1–V4 would have pointed to the LAD."
    kind: application
  - id: v2
    of: imaging-2026-0493
    flip: false
    changed: "70-year-old woman with stable exertional angina, image → 58-year-old man whose chest pain resolved 6 hours ago, ECG described in words with deep T-wave inversions in V1–V4 ⇒ inversion centered on the anterior precordial leads is unchanged, so the answer stays LAD"
    context: "Surface changed — different patient, pain-free after an episode, text description"
    stem: "A 58-year-old man comes to the emergency department because of an episode of chest pressure at rest that lasted 20 minutes and resolved 6 hours ago. He has hyperlipidemia. He is now pain free. His pulse is 78/min and blood pressure is 138/84 mm Hg. A 12-lead ECG shows sinus rhythm with deep, symmetric T-wave inversions in leads V1 through V4 and no ST elevation; the inferior leads are normal. Serum troponin is slightly elevated. Which of the following coronary arteries most likely has a critical stenosis?"
    choices: ["A. Right coronary artery", "B. Posterior descending artery", "C. Left anterior descending artery", "D. Left circumflex artery", "E. Acute marginal artery"]
    answer: "C"
    explanation: "Age, sex, and presentation changed, but the deciding clue is the same: T-wave inversion centered on the anterior precordial leads with normal inferior leads. Deep T-wave inversions across V1–V4 in a patient with ischemic chest pain typically indicate severe obstruction of the LAD. Inferior-lead changes would point to the right coronary artery; lateral-lead changes (I, aVL, V5, V6) to the circumflex."
    kind: application
figures:
- id: f1
  file: docs/assets/figures/ptbxl-04964.png
  kind: ecg
  at: 판단 — 왜 이 유도면 이 혈관인가
  shows: '전중격 유도의 허혈성 변화(라벨: ischemic in anteroseptal leads)'
  look_for:
  - V2~V5 의 얕은 T파 역위
  - aVL 의 T파 역위
  label: ischemic in anteroseptal leads (SCP ISCAS, 가능도 100)
  label_basis: dataset_expert
  reference: 심장내과 전문의의 SCP-ECG 판독을 두 번째 전문의가 검증 — 해당 진술의 가능도 100 인 기록만
  paper: Wagner P 외. PTB-XL, a large publicly available electrocardiography dataset. Sci Data 2020;7:154
  doi: 10.1038/s41597-020-0495-6
  credit: PTB-XL ECG dataset v1.0.3 (PhysioNet, CC BY 4.0) · record 4964
  license: Creative Commons Attribution 4.0 International
  url: https://physionet.org/content/ptb-xl/1.0.3/records500/04000/#files-panel
  asset: PTBXL-04964
  paper_cited_by: 1213
---

## 판단 — 왜 이 유도면 이 혈관인가
- 각 흉부 유도는 **바로 밑의 벽**을 본다. 전벽(첨부·측벽 포함) 허혈은 V1~V6 와 I·aVL, 하벽 허혈은 II·III·aVF 에 나타난다 [[harrison-22: 247장 p.1872]].
- 그래서 변화가 모인 **유도 묶음 → 벽 → 그 벽을 맡은 혈관** 순서로 고른다.
- 흉부 유도의 깊은 T파 역위는 좌전하행지의 심한 협착을 가리키는 대표 소견이다 [[harrison-22: 247장 p.1873]].

## 기전 — 허혈 층에 따라 ST 가 기운다
허혈 부위와 정상 부위 사이의 전압차가 손상 전류를 만들고, 이것이 ST 를 움직인다. 경벽 허혈이면 ST 벡터가 바깥(심외막)으로 향해 그 위 유도에 ST 상승이, 내막하 허혈이면 벡터가 안쪽으로 향해 ST 하강이 생긴다 [[harrison-22: 247장 p.1872]]. 완전히 막히지 않은 고정 협착은 주로 내막하 허혈을 일으키고, 재분극 지연이 T파를 그 부위에서 돌려세워 증상 없을 때도 T파 역위로 남을 수 있다 [[harrison-22: 247장 p.1873]].

## 가르는 소견 — 유도 묶음과 혈관
- 후벽 허혈은 직접 보는 유도가 없어 V1~V3 의 거울상 ST 하강으로 간접적으로 읽는다 [[harrison-22: 247장 p.1872]].
- 우심실 허혈은 우측 흉부 유도의 ST 상승으로 본다 [[harrison-22: 247장 p.1872]].
- **한계**: 정상 심전도 한 장으로 허혈을 배제하지 못한다 [[harrison-22: 247장 p.1873]]. T파 역위는 비대·각차단·약물·뇌출혈에서도 생긴다 [[harrison-22: 247장 p.1874]].

## 권고와 예외
- 혈관과 벽의 대응은 우세형·개인차에 따라 달라진다(하벽이 회선지일 수 있음).
- 안정 협심증의 다음 검사·치료는 이 정리본의 목표가 아니다.

## 시험 쟁점 — 충돌·맥락·새 근거
- **Z1 맥락 · 비ST상승 변화로 위치 정하기** — 시험 기준: T파 역위가 모인 유도로 벽과 혈관을 고른다(문항이 이렇게 묻는다) / 다른 기준: 유도는 비ST상승 허혈보다 ST상승 허혈의 위치를 더 잘 가리킨다 [[harrison-22: 247장 p.1872]] / 왜 다른가: 내막하 허혈의 ST 하강은 넓게 퍼져 책임 부위와 어긋날 수 있다 — 다만 흉부 유도 깊은 T파 역위는 좌전하행지를 비교적 잘 가리킨다 [[harrison-22: 247장 p.1873]] / 시험에서는: KMLE · USMLE 모두 유도 묶음 → 혈관 대응으로 답한다.
