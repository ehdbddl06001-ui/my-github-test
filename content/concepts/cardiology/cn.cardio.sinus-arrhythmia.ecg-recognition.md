---
id: cn.cardio.sinus-arrhythmia.ecg-recognition
type: concept
topic: Cardiology
see_also: [cn.cardio.premature-ventricular-complex.ecg-recognition, cn.cardio.palpitations.arrhythmia-evaluation]
date: 2026-11-11
updated: 2026-11-11
version: 1
outline: h247
confidence: medium
review_status: unreviewed
note_form: 2
title: "동부정맥 — 같은 P파, 서서히 변하는 PP"
objective: "모든 QRS 앞에 같은 동성 P파가 있고 PP 간격만 호흡에 따라 서서히 변하는 리듬을 동부정맥으로 읽고 심방 기외수축과 가른다"
objective_kind: 진단
condition: 동부정맥(sinus arrhythmia)
exams: [kmle, usmle]
summary:
  - "결론: P파 모양이 모두 같고 PP 간격만 0.12초 넘게 서서히 늘었다 줄었다 하면 동부정맥 — 정상 소견이다."
  - "시험 단서: 젊고 건강한 사람, 쉴 때·깊은 호흡 때 「맥이 고르지 않다」, 증상 없음, 검사 정상(respiratory sinus arrhythmia)."
  - "왜: 들숨에 미주신경 긴장이 반사적으로 줄어 동결절이 빨라지고 날숨에 되돌아온다 — 박동원은 그대로 동결절이다."
  - "P파 모양이 다른 박동이 일찍 끼어들면 동부정맥이 아니라 심방 기외수축이다."
  - "무증상 동부정맥은 더 검사하지 않는다."
pitfalls:
  - contrast: "심방 기외수축 vs 동부정맥"
    point: "심방 기외수축은 동성 P파와 모양이 다른 P파를 가진 박동이 갑자기 일찍 온다. 동부정맥은 P파 모양이 모두 같고 간격이 한 박동씩 서서히 변한다. 먼저 「P파 모양이 다른 박동이 있나」와 「간격 변화가 갑작스러운가」를 본다."
    cites: ["harrison-22: 253장 p.1932", "harrison-22: 254장 p.1935"]
    covers: ["imaging-2026-0608:C"]
  - contrast: "불규칙한 맥 = 부정맥 검사가 필요하다?"
    point: "동부정맥은 건강한 사람의 정상 생리이고 쉴 때 흔하며 운동으로 심박수가 오르면 사라진다. 무증상이면 심장 검사를 더 하지 않는다."
    cites: ["harrison-22: 254장 p.1935"]
  - contrast: "불규칙 RR = 심방세동?"
    point: "심방세동은 구분되는 P파가 없다. 모든 QRS 앞에 같은 P파가 보이면 박동원이 동결절이다."
    cites: ["harrison-22: 253장 p.1932"]
tables:
  - id: irregular-narrow
    section: "가르는 소견 — 좁은 QRS 의 불규칙한 리듬"
    title: "좁은 QRS 불규칙 리듬 — 무엇이 가르나"
    role: differential
    span: column
    columns: ["판독", "P파", "간격 변화"]
    rows:
      - ["동부정맥", "모두 같은 동성 P파", "PP 가 호흡 따라 서서히 > 0.12초 변동 [[harrison-22: 254장 p.1935]]"]
      - ["심방 기외수축", "일찍 온 박동만 다른 P파", "갑자기 이른 박동 [[harrison-22: 253장 p.1932]]"]
      - ["심방세동", "구분되는 P파 없음", "규칙 없이 매번 다름 [[harrison-22: 253장 p.1932]]"]
      - ["이소성 심방 리듬", "동성과 다른 P파로 지속", "대개 규칙적 [[harrison-22: 253장 p.1932]]"]
criteria:
  - id: sa-def
    name: 동부정맥 정의
    kind: 진단 기준
    population: "불규칙한 맥이 있는 심전도"
    statement: "동결절에서 시작한 리듬(동성 P파)이면서 PP 간격 차이가 120 ms 를 넘는 것. P파 모양이 서로 다르면 동부정맥보다 심방 기외수축일 가능성이 높다 [[harrison-22: 254장 p.1935]]"
    exceptions: "동결절 안에서 박동을 시작하는 자리는 심박수에 따라 위·아래로 옮겨 가 심박수가 다를 때 P파가 약간 달라 보일 수 있다 [[harrison-22: 251장 p.1918]]"
    source: harrison-22
    basis: current
    exams: [kmle, usmle]
sources:
  - id: harrison-22
    org: "McGraw Hill"
    title: "Harrison's Principles of Internal Medicine, 22nd ed. — Chapter 251: Disorders of the Sinoatrial Node · Chapter 253: Approach to Supraventricular Arrhythmias · Chapter 254: Physiologic and Nonphysiologic Sinus Rhythm"
    kind: textbook
    year: 2025
    citation: "Harrison's Principles of Internal Medicine, 22e. 251장 p.1917–1919, 1922 · 253장 p.1932–1933 · 254장 p.1935–1936"
    checked_at: 2026-11-11
    checked: "드라이브 22판 장별 문서 H22_251·H22_253·H22_254 본문 대조 — 동결절은 평소 부교감 우세, 미주 긴장이 빠지면 빨라짐(251장 p.1917) · 박동 시작 자리 이동으로 심박수에 따라 P파가 약간 다를 수 있음(p.1918) · 동방 Wenckebach 는 휴지 앞 PP 가 점점 짧아짐(p.1919) · 단련된 운동선수 안정 시 40회 미만 가능(p.1922) · 표 253-1: 심방 기외수축 = 동성 P파와 다른 이른 심방 박동, 동부정맥 = 동성 P파·PP 가 호흡에 따라 변함, 이소성 심방 리듬 = 동성과 다른 P파의 규칙 리듬(253장 p.1932) · 무증상 상심실 부정맥 대부분 치료·검사 불필요(p.1933) · 동성 P파 축(II·III·aVF 양성, aVR 음성), 동부정맥 정의 PP 차이 > 120 ms, P파 모양이 다르면 심방 기외수축, 쉴 때 흔하고 운동 시 사라짐, 호흡성·심실성·비위상성 세 유형, 들숨 시 미주 긴장 반사적 억제, 무증상이면 추가 검사 불필요(254장 p.1935). Mobitz I 방실차단 서술은 252장 — 이번에 대조하지 않음"
    verified: text
diagram:
  title: "좁은 QRS 의 불규칙한 리듬 — 어디서 왔나"
  nodes:
    - {id: start, kind: start, text: "불규칙한 맥 · 좁은 QRS"}
    - {id: pwave, kind: decision, text: "QRS 마다 구분되는 P파가 있나?"}
    - {id: af, kind: end, text: "심방세동 쪽"}
    - {id: shape, kind: decision, text: "P파 모양이 모두 같나?"}
    - {id: compare, kind: info, text: "리듬 스트립 P파를 겹쳐 비교"}
    - {id: pac, kind: end, text: "심방 기외수축"}
    - {id: drop, kind: decision, text: "P파 뒤 QRS 가 빠지나?"}
    - {id: avb, kind: alert, text: "방실차단 — PR 변화 확인"}
    - {id: sa, kind: end, text: "동부정맥(정상)"}
  edges:
    - {from: start, to: pwave}
    - {from: pwave, to: af, label: "없음"}
    - {from: pwave, to: shape, label: "있음"}
    - {from: shape, to: pac, label: "이른 박동만 다름"}
    - {from: shape, to: drop, label: "모두 같음"}
    - {from: shape, to: compare, label: "모르겠음"}
    - {from: compare, to: pac, label: "다른 P파"}
    - {from: compare, to: drop, label: "같은 P파"}
    - {from: drop, to: avb, label: "빠짐"}
    - {from: drop, to: sa, label: "안 빠짐"}
diagram_notes:
  - "동부정맥은 PP 차이 > 120 ms, 쉴 때 흔하고 운동으로 빨라지면 사라진다 [[harrison-22: 254장 p.1935]]."
  - "숨 참기로 휴지가 과장될 수 있고 폐쇄성 수면무호흡에서 흔하다 [[harrison-22: 254장 p.1935]]."
  - "휴지 직전 PP 가 점점 짧아지다 P파가 빠지면 동방 Wenckebach 차단이다 — 동부정맥과 달리 P파 자체가 빠진다 [[harrison-22: 251장 p.1919]]."
checks:
  - q: "28세 여자, 모든 QRS 앞에 같은 P파, PP 가 0.84~1.1초로 서서히 변한다. 판독은?"
    a: "동부정맥. P파 모양이 같고 변화가 서서히 오므로 박동원은 동결절이다."
  - q: "심방 기외수축과 무엇으로 가르나?"
    a: "P파 모양과 간격 변화의 양상. 심방 기외수축은 다른 P파의 박동이 갑자기 일찍 온다."
variants:
  - id: v1
    of: imaging-2026-0608
    flip: true
    changed: "모든 박동의 P파가 같고 PP 가 서서히 변함 → 동리듬 사이에 모양이 다른(II 에서 낮고 뾰족한) P파를 가진 박동이 갑자기 일찍 오고 뒤에 휴지가 따름 ⇒ 정답이 동부정맥에서 심방 기외수축으로"
    context: "같은 환자 뼈대, 이른 박동 단서를 넣은 글 변형(그림 없음)"
    stem: "A 28-year-old woman comes to the physician because she has noticed that her pulse seems to skip occasionally while she rests in the evening. She has no chest pain, dyspnea, or syncope. She drinks three cups of coffee daily and takes no medications. Her pulse is 70/min and occasionally irregular; blood pressure is 110/70 mm Hg. Cardiac examination shows no murmurs. Serum electrolyte concentrations and thyroid function are normal. A rhythm strip shows sinus beats with identical upright P waves in lead II, interrupted by single beats that arrive abruptly early; each early beat is preceded by a P wave that is smaller and peaked, unlike the sinus P waves, and is followed by a pause. The QRS complexes are narrow. Which of the following is the most likely diagnosis?"
    choices: ["A. Atrial fibrillation", "B. Sinus arrhythmia", "C. Premature atrial contractions", "D. Second-degree atrioventricular block, Mobitz type I", "E. Ectopic atrial rhythm"]
    answer: "C"
    explanation: "The decisive change is the early beat with a P wave of a different shape. Sinus arrhythmia keeps one P-wave shape and changes the interval gradually; an abrupt early atrial beat with a distinct P wave is a premature atrial contraction. An ectopic atrial rhythm would show the different P wave continuously, not as isolated early beats."
    kind: application
  - id: v2
    of: imaging-2026-0608
    flip: false
    changed: "28세 여자·요가 호흡 → 16세 남자 수영 선수·학교 검진 심전도, 소견을 글로 제시 ⇒ 같은 동성 P파·일정한 PR·PP 가 호흡에 따라 서서히 변함이라는 결정 단서는 같아 답은 그대로 동부정맥"
    context: "겉모습만 바꾼 글 변형(그림 없음)"
    stem: "A 16-year-old boy who swims competitively is referred after a school screening ECG was read as irregular. He has no palpitations, chest pain, or syncope and takes no medications. His pulse is 56/min and varies slightly; blood pressure is 112/64 mm Hg. Examination shows no murmurs. On the ECG, every narrow QRS complex is preceded by an upright P wave in leads II and aVF with the same shape and a constant PR interval of 0.16 seconds. The P-P interval lengthens and shortens smoothly from 0.9 to 1.2 seconds in a repeating pattern, and no P wave is left without a QRS complex. Which of the following is the most likely diagnosis?"
    choices: ["A. Sinus arrhythmia", "B. Premature atrial contractions", "C. Sinoatrial exit block", "D. Atrial fibrillation", "E. Second-degree atrioventricular block, Mobitz type I"]
    answer: "A"
    explanation: "Age, sex, and setting changed, but the deciding clues did not: one sinus P-wave shape, a constant PR, and a P-P interval that drifts smoothly by more than 120 ms without dropped P waves or QRS complexes. That is sinus arrhythmia, a normal finding in a fit adolescent, and an asymptomatic patient needs no further cardiac testing."
    kind: application
figures_wanted:
- source: PMC_OA
  shows: 동부정맥 — 같은 P파와 서서히 변하는 PP 간격
  at: 기전 — 호흡이 미주신경을 흔든다
  query: '"sinus arrhythmia" AND (ECG OR electrocardiogram) AND ("case report" OR respiratory)'
  caption_terms:
  - sinus arrhythmia
  modality: ECG
figures_rejected:
- asset: PMC-PMC13420558_Figure1
  reason: 그림은 2:1 방실차단 + 심실위상성(ventriculophasic) 동부정맥·우각차단 — 전도 안 된 P파가 끼어 있어 목표(모든 P파가 전도되고 PP가 호흡에 따라 서서히 변하는 호흡성 동부정맥)와 다르고 방실차단과 혼동을 준다
---

## 판단 — P파와 간격 변화로 읽는 순서
- **P파가 있나**: 모든 QRS 앞에 구분되는 P파가 있으면 심방세동이 아니다 [[harrison-22: 253장 p.1932]].
- **모양이 같나**: II·III·aVF 양성, aVR 음성의 같은 동성 P파면 박동원은 동결절이다 [[harrison-22: 254장 p.1935]]. 일찍 온 박동만 P파가 다르면 심방 기외수축이다 [[harrison-22: 253장 p.1932]].
- **어떻게 변하나**: 간격이 한 박동씩 서서히, 호흡 주기에 맞춰 변하고 PP 차이가 120 ms 를 넘으면 동부정맥이다 [[harrison-22: 254장 p.1935]].

## 기전 — 호흡이 미주신경을 흔든다
동결절은 평소 부교감 신경이 우세하게 조절하고, 부교감 긴장이 빠지면 자발 탈분극이 빨라져 심박수가 오른다 [[harrison-22: 251장 p.1917]]. 들숨 때 미주신경 긴장이 반사적으로 억제되어 동결절이 빨라지고, 날숨 때 긴장이 돌아와 느려진다 — 호흡성 동부정맥(respirophasic)이다 [[harrison-22: 254장 p.1935]]. 박동원이 바뀌지 않으므로 P파 모양과 PR 간격은 그대로이고 시점만 서서히 바뀐다. 미주 긴장이 높은 젊고 단련된 사람에서 두드러지고, 운동으로 미주 긴장이 빠지면 사라진다 [[harrison-22: 254장 p.1935]]. 심실 기외수축이나 방실차단 뒤 PP 가 짧아지는 심실성(ventriculophasic), 호흡·심장 주기와 무관한 비위상성(nonphasic) 유형도 있다 [[harrison-22: 254장 p.1935]].

## 가르는 소견 — 좁은 QRS 의 불규칙한 리듬
- 심방 기외수축은 일찍 오는 심방 박동이 동성 P파와 다른 모양을 가진다. 이단맥·삼단맥처럼 규칙적으로 반복될 수도 있다 [[harrison-22: 253장 p.1932]].
- 동결절의 박동 시작 자리는 심박수에 따라 옮겨 가 심박수가 다를 때 P파가 약간 달라 보일 수 있다 — 한 박동만 갑자기 다른 P파인지, 심박수에 따라 서서히 달라지는지를 본다 [[harrison-22: 251장 p.1918]].
- 동방 Wenckebach 차단은 휴지 직전 PP 가 점점 짧아지고 P파가 아예 빠진다. 동부정맥은 P파가 빠지지 않는다 [[harrison-22: 251장 p.1919]].

## 권고와 예외
- 무증상 동부정맥은 원인과 무관하게 추가 심장 검사가 필요 없고 병적이지 않다 [[harrison-22: 254장 p.1935]]. 무증상 상심실 부정맥 대부분은 치료나 추가 평가가 필요 없다 [[harrison-22: 253장 p.1933]].
- 숨 참기로 휴지가 과장될 수 있어, 수면 중 긴 휴지가 반복되면 폐쇄성 수면무호흡을 생각한다 [[harrison-22: 254장 p.1935]].

## 시험 쟁점 — 충돌·맥락·새 근거
- 해당 없음(대조: 해리슨 22판 251장 p.1917~1919 · 253장 p.1932~1933 · 254장 p.1935)
