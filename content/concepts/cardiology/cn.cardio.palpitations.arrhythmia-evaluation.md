---
id: cn.cardio.palpitations.arrhythmia-evaluation
type: concept
topic: Cardiology
see_also: []
date: 2026-11-02
updated: 2026-11-02
version: 1
outline: h43
confidence: medium
review_status: unreviewed
note_form: 2
title: "심계항진 — 위험 부정맥 단서와 기록 방법"
objective: "심계항진 환자에서 위험한 부정맥을 시사하는 단서를 찾고, 증상 빈도에 맞는 심전도 기록 방법을 고른다"
objective_kind: 검사 선택
condition: 심계항진(palpitations) — 기외수축·빈맥·심방세동·비심장 원인의 감별과 심전도 기록
exams: [kmle, usmle]
summary:
  - "결론: 심계항진 평가의 첫 목표는 생명을 위협하는 부정맥인지 가리는 것 — 관상동맥질환과 실신·어지럼이 위험 단서다."
  - "시험 단서: 「건너뛰는 듯한(skipped beat)」 간헐적 두근거림은 기외수축, 규칙적 지속은 빈맥, 불규칙 지속은 심방세동(AF)."
  - "왜: 기외수축 뒤 쉼에 심실이 더 차고 그 박동이 세게 수축해(post-extrasystolic potentiation) 그 박동을 느낀다."
  - "기록: 운동 때만이면 운동 심전도, 드물면 Holter 보다 삽입형 루프 기록기·이동형 원격 측정이 유용하다."
  - "15분 넘게 지속되고 동반 증상이 많으면 정신과 원인(공황·불안)이 더 흔하다 — 그래도 위험 부정맥부터 배제한다."
pitfalls:
  - contrast: "부정맥이 있으면 심계항진도 있다?"
    point: "대부분의 부정맥은 심계항진을 일으키지 않는다. 증상이 없다고 부정맥이 배제되지 않고, 증상과 기록을 맞춰 봐야 한다(일지·표시)."
    cites: ["harrison-22: 45장 p.291"]
  - contrast: "드문 심계항진 — Holter vs 루프 기록기"
    point: "Holter 는 짧은 기간만 기록해 드문 증상에는 쓸모가 제한적이다. 드물게 되풀이되는 원인 불명 심계항진은 삽입형 루프 기록기·이동형 원격 측정이 낫다."
    cites: ["harrison-22: 45장 p.291"]
  - contrast: "자세에 따라 생기는 심계항진 = 불안?"
    point: "자세성 심계항진은 심장 안(심방 점액종)이나 옆(종격동 종괴)의 구조 이상을 시사한다 — 영상으로 확인할 단서다."
    cites: ["harrison-22: 45장 p.291"]
tables:
  - id: pattern
    section: "가르는 소견 — 양상과 원인"
    title: "심계항진 양상에 따른 흔한 원인"
    role: differential
    span: column
    columns: ["양상", "흔한 원인"]
    rows:
      - ["간헐적·「건너뛴다」", "심방·심실 기외수축 [[harrison-22: 45장 p.291]]"]
      - ["규칙적·지속", "상심실성·심실 빈맥 [[harrison-22: 45장 p.291]]"]
      - ["불규칙·지속", "심방세동 [[harrison-22: 45장 p.291]]"]
      - ["자세에 따라", "심방 점액종·종격동 종괴 [[harrison-22: 45장 p.291]]"]
      - ["15분 넘게·동반 증상 많음", "공황·불안·신체화 [[harrison-22: 45장 p.291]]"]
  - id: monitor
    section: "선택 — 언제 무엇으로 기록하나"
    title: "증상 빈도에 맞춘 심전도 기록"
    role: tests
    span: column
    columns: ["상황", "기록 방법"]
    rows:
      - ["지금 증상이 있다", "안정 시 12유도 심전도 [[harrison-22: 45장 p.291]]"]
      - ["운동이 유발한다", "운동 심전도 [[harrison-22: 45장 p.291]]"]
      - ["자주(하루 단위) 생긴다", "연속 심전도(Holter) [[harrison-22: 45장 p.291]]"]
      - ["드물게 되풀이된다", "삽입형·외부 루프 기록기, 이동형 원격 측정, 전화 전송 [[harrison-22: 45장 p.291]]"]
criteria:
  - id: high-risk
    name: 위험 부정맥을 시사하는 심계항진
    kind: 위험 평가
    population: "심계항진 환자"
    statement: "관상동맥질환이 있거나 그 위험인자가 있으면 심실 부정맥 위험이 가장 크다. 실신·어지럼 같은 혈역학 저하 증상이 함께 있으면 위험 부정맥을 더 시사한다 [[harrison-22: 45장 p.291]]"
    exceptions: "관상동맥질환에서는 협심증·호흡곤란, 심실 기능 이상·대동맥판 협착·비후성 심근병증·승모판 협착에서는 좌심방압 상승에 의한 호흡곤란이 동반될 수 있다 [[harrison-22: 45장 p.291]]"
    source: harrison-22
    basis: current
    exams: [kmle, usmle]
sources:
  - id: harrison-22
    org: "McGraw Hill"
    title: "Harrison's Principles of Internal Medicine, 22nd ed. — Chapter 45: Palpitations"
    kind: textbook
    year: 2025
    citation: "Harrison's Principles of Internal Medicine, 22e. 45장 p.291"
    checked_at: 2026-11-02
    checked: "드라이브 22판 장별 문서 H22_045 본문 대조(p.291) — 정의·자세성 심계항진과 점액종·종격동 종괴 · 원인 비율(심장 43%·정신 31%·기타 10%·불명 16%) · 기외수축 뒤 박동을 느끼는 기전(확장말기 크기 증가·post-extrasystolic potentiation) · 규칙 지속=빈맥, 불규칙 지속=AF · 대부분의 부정맥은 심계항진 없음 · 맥 짚기·두드려 보기 · 과역동 상태·대동맥판 역류·약물(담배·카페인·아미노필린·아트로핀·티록신·코카인·암페타민·대마) · 정신과 원인은 15분 초과·동반 증상 · 기타 원인(갑상선중독·알코올·흉벽 근수축·갈색세포종·전신 비만세포증·코로나 후 증후군) · 관상동맥질환·실신/어지럼 위험 단서 · 진찰(활력징후·경정맥압·청진)·12유도·운동 심전도·Holter·전화 전송·루프 기록기·이동형 원격 측정, Holter 제한적·루프와 원격 측정 비용효과 · 일지 필수 · 양성 기외수축 베타차단제·원인 물질 중단·인지치료·안심"
    verified: text
diagram:
  title: "심계항진 — 위험부터 가르고 기록한다"
  nodes:
    - {id: start, kind: start, text: "두근거림을 호소한다"}
    - {id: risk, kind: decision, text: "관상동맥질환·실신·어지럼이 있나?"}
    - {id: urgent, kind: end, text: "심실 부정맥 의심 — 기록·평가 서두름"}
    - {id: hx, kind: info, text: "양상·지속 시간·유발 요인을 묻고 맥을 짚는다"}
    - {id: now, kind: decision, text: "지금 증상이 있나?"}
    - {id: ecg, kind: end, text: "안정 시 12유도 심전도"}
    - {id: freq, kind: decision, text: "운동 유발인가, 얼마나 자주인가?"}
    - {id: ex, kind: end, text: "운동 심전도"}
    - {id: holter, kind: end, text: "연속 심전도(Holter)"}
    - {id: loop, kind: end, text: "루프 기록기·이동형 원격 측정"}
  edges:
    - {from: start, to: risk}
    - {from: risk, to: urgent, label: "있음"}
    - {from: risk, to: hx, label: "없음"}
    - {from: hx, to: now}
    - {from: now, to: ecg, label: "있음"}
    - {from: now, to: freq, label: "없음"}
    - {from: freq, to: ex, label: "운동 때"}
    - {from: freq, to: holter, label: "자주"}
    - {from: freq, to: loop, label: "드묾"}
diagram_notes:
  - "기록 방법과 상관없이 증상이 생긴 시각을 일지나 표시 버튼으로 남겨야 기록과 맞춰 읽을 수 있다."
  - "진찰은 활력징후·경정맥압과 맥박·흉부와 심장 청진 — 부정맥과 그 혈역학 결과를 함께 본다."
  - "갑상선중독·갈색세포종·카페인·담배·코카인·암페타민·대마 같은 수축력·교감 자극 원인을 함께 확인한다."
checks:
  - q: "기외수축에서 환자가 느끼는 박동은 어느 것이고 왜인가?"
    a: "기외수축 뒤의 박동 — 쉼 동안 심실이 더 차고 그 박동의 수축이 강해진다(post-extrasystolic potentiation)."
  - q: "한 달에 한두 번 생기는 원인 불명 심계항진의 기록 방법은?"
    a: "삽입형 루프 기록기나 이동형 원격 측정 — Holter 는 드문 증상에 쓸모가 제한적이다."
variants:
  - id: v1
    context: "같은 목표의 적용 — 드물게 되풀이되는 심계항진"
    stem: "34세 여자가 6개월 전부터 한 달에 한두 번, 갑자기 시작해 수 분 지속되는 규칙적인 두근거림으로 왔다. 실신이나 흉통은 없고 관상동맥질환 위험인자도 없다. 진찰과 안정 시 12유도 심전도, 갑상선 기능 검사는 정상이다. 24시간 Holter 검사에서는 증상이 없었고 기록도 정상이었다. 다음으로 할 검사는?"
    choices: ["A. 관상동맥 조영술", "B. 삽입형 루프 기록기", "C. 24시간 Holter 재검", "D. 운동 부하 심전도", "E. 흉부 CT"]
    answer: "B"
    explanation: "증상이 드물어 Holter 기록 기간에 잡히지 않았다. 드물게 되풀이되는 원인 불명 심계항진에는 삽입형 루프 기록기나 이동형 원격 측정이 유용하다. 운동 심전도는 운동이 유발할 때 고른다."
    kind: application
  - id: v2
    context: "같은 목표의 적용 — 위험 단서가 있는 심계항진(USMLE)"
    stem: "A 64-year-old man with a prior myocardial infarction comes to the clinic because of episodes of rapid regular heartbeat over the past 2 weeks. During one episode yesterday he became lightheaded and nearly fainted. His blood pressure is 128/78 mm Hg and pulse is 76/min and regular. A resting ECG shows Q waves in leads II, III, and aVF. Which of the following is the most likely cause of his palpitations?"
    choices: ["A. Panic disorder", "B. Premature atrial contractions", "C. Ventricular tachycardia", "D. Caffeine excess", "E. Thyrotoxicosis"]
    answer: "C"
    explanation: "Known coronary artery disease plus palpitations with near-syncope points to a ventricular arrhythmia, the life-threatening cause that must be pursued first. Sustained regular palpitations fit a tachycardia rather than isolated premature beats."
    kind: application
figures_none: 증상 양상·위험 단서·검사 선택이 목표 — 판독할 영상 소견이 시험 단서가 아니다
---

## 판단 — 왜 위험 단서를 먼저 보나
- 심계항진 평가의 첫 목표는 증상이 생명을 위협하는 부정맥 때문인지 가리는 것이다 [[harrison-22: 45장 p.291]].
- 관상동맥질환이나 그 위험인자가 있으면 심실 부정맥 위험이 가장 크고, 실신·어지럼이 함께 있으면 혈역학 저하를 시사한다 [[harrison-22: 45장 p.291]].
- 대부분의 심계항진 환자는 심각한 부정맥이나 구조적 심질환이 없다 — 위험 단서가 없을 때 양상과 빈도로 기록 방법을 고른다 [[harrison-22: 45장 p.291]].

## 기전 — 기외수축 뒤 박동을 느낀다
심계항진은 가슴이 「쿵」「두근」「파닥」하는 느낌, 곧 평소 의식하지 않던 심장 박동을 느끼는 것이다. 다른 자극이 적은 조용한 휴식 때 잘 느낀다. 간헐적 심계항진의 흔한 원인인 심방·심실 기외수축(premature contraction)에서 환자가 느끼는 것은 기외수축 자체가 아니라 그다음 박동이다 — 쉼 동안 심실 확장말기 크기가 커지고 그 박동의 수축력이 세지기(post-extrasystolic potentiation) 때문이다. 그래서 「건너뛰는」 느낌으로 호소한다. 운동·스트레스·갈색세포종의 카테콜아민 자극, 대동맥판 역류의 커진 심실과 과역동 심첨부, 수축력을 올리는 물질(담배·카페인·아미노필린·아트로핀·티록신·코카인·암페타민·대마)도 심계항진을 만든다 [[harrison-22: 45장 p.291]].

## 가르는 소견 — 양상과 원인
- 한 대규모 연구에서 원인은 심장 43%, 정신과 31%, 기타 10%, 불명 16%였다 [[harrison-22: 45장 p.291]].
- 증상이 있을 때 환자에게 리듬을 두드려 보게 하거나 맥을 짚게 하면 규칙·불규칙을 가를 수 있다 [[harrison-22: 45장 p.291]].
- 기타 원인 — 갑상선중독증, 알코올, 흉벽 골격근의 자발 수축, 갈색세포종, 전신 비만세포증, 코로나 후 증후군 [[harrison-22: 45장 p.291]].
- 대부분의 부정맥은 심계항진이 없다 — 증상이 없다는 것이 부정맥이 없다는 뜻은 아니다 [[harrison-22: 45장 p.291]].

## 선택 — 언제 무엇으로 기록하나
진찰에서 활력징후, 경정맥압과 맥박, 흉부·심장 청진으로 부정맥과 그 혈역학 결과를 본다. 기록은 증상 빈도에 맞춘다. Holter 는 임상 쓸모가 제한적이고, 드물게 되풀이되는 원인 불명 심계항진에서는 삽입형 루프 기록기와 이동형 원격 측정이 안전하고 비용효과가 나을 수 있다. 어느 방법이든 증상 시각을 일지나 표시로 남겨야 해석할 수 있다 [[harrison-22: 45장 p.291]].

## 권고와 예외
- 증상이 괴로운 양성 심방·심실 기외수축은 베타차단제로 조절할 수 있다 [[harrison-22: 45장 p.291]].
- 알코올·담배·불법 약물이 유발하면 끊게 하고, 처방약이 원인이면 가능할 때 다른 약으로 바꾼다 [[harrison-22: 45장 p.291]].
- 정신과 원인은 인지치료나 약물치료가 도움이 될 수 있다. 심각한 원인을 배제한 뒤에는 예후에 나쁜 영향이 없다고 안심시킨다 [[harrison-22: 45장 p.291]].

## 시험 쟁점 — 충돌·맥락·새 근거
- 해당 없음(대조: 해리슨 22판 45장 p.291)
