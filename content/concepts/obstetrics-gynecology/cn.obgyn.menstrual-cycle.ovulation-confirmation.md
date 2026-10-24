---
id: cn.obgyn.menstrual-cycle.ovulation-confirmation
type: concept
topic: Obstetrics and Gynecology
see_also: [Endocrinology]
date: 2026-10-25
updated: 2026-10-25
version: 1
outline: ob.anatomy-cycle   # 여성 생식기의 구조와 월경주기 — 해리슨 21판 392장
confidence: medium
review_status: unreviewed
note_form: 2            # 판형 2(2026-09-25)
title: "월경주기 — 배란 확인은 배란 7일 뒤 프로게스테론"
objective: "배란 여부를 확인할 때 황체기 길이가 일정하다는 점을 이용해 배란 약 7일 뒤(다음 월경 약 7일 전) 혈청 프로게스테론으로 판정한다"
objective_kind: 검사 선택
condition: 배란 확인(confirmation of ovulation)
exams: [kmle, usmle]
summary:
  - "결론: 배란 확인은 배란 약 7일 뒤 혈청 프로게스테론(serum progesterone) > 3 ng/mL 로 한다."
  - "시험 단서: 임신을 원하는 여성의 「배란이 되는가」 질문, 주기 길이(25~35일)와 다음 월경 예정일이 주어진다."
  - "왜: 프로게스테론은 배란 뒤 황체(corpus luteum)만 낸다 — 황체기는 12~14일로 일정해 다음 월경에서 거꾸로 시점을 잡는다."
  - "주기 길이의 차이는 난포기에서 온다 — 긴 주기에서 「28일 주기 기준 날짜」로 뽑으면 너무 이르다."
  - "기초체온 0.24°C 상승·소변 LH 급증 검사·초음파 황체도 증거지만, 월경전 증상이 없다고 무배란은 아니다."
pitfalls:
  - contrast: "주기가 길어도 같은 날짜에 채혈?"
    point: "주기 길이의 차이는 난포기 길이에서 오고 황체기는 12~14일로 거의 일정하다. 그래서 채혈 시점은 월경 시작일이 아니라 배란(또는 다음 월경 예정일)에서 잡는다 — 긴 주기에서 이르게 뽑으면 배란 전 값이 나온다 [[harrison-21: 392장 p.3031]]."
  - contrast: "월경전 증상이 없으면 무배란?"
    point: "더부룩함·유방 압통·기분 변화·식욕 같은 월경전 증상은 배란 주기에 흔하지만, 없다고 해서 무배란의 근거가 되지는 않는다 [[harrison-21: 392장 p.3031]]."
  - contrast: "소변 LH 급증 = 그 순간 배란?"
    point: "배란은 LH 급증 약 36시간 뒤에 온다. 소변 LH 검사는 성교 시점을 맞추는 데 쓰고, 배란이 실제로 일어났는지는 황체기 프로게스테론·기초체온·초음파로 본다 [[harrison-21: 392장 p.3031]]."
  - contrast: "난소 예비력 — 인히빈 B vs AMH?"
    point: "항뮐러관호르몬(anti-müllerian hormone, AMH)은 작은 난포의 과립막세포가 내고 주기 내내 비교적 안정해 인히빈 B보다 낫다. AMH 는 배란 확인 검사가 아니라 난소 예비력 지표다 [[harrison-21: 392장 p.3030]]."
criteria:
  - id: ovulation-progesterone
    name: 배란 확인 — 황체기 프로게스테론
    kind: 진단 기준
    population: "배란 여부를 확인하려는 가임기 여성"
    statement: "배란 약 7일 뒤 혈청 프로게스테론 > 3 ng/mL 이면 배란이 있었다고 본다 [[harrison-21: 392장 p.3031]]"
    exceptions: "황체기는 12~14일로 일정하므로 배란 약 7일 뒤는 다음 월경 약 5~7일 전에 해당한다(해리슨 수치에서 계산). 시점이 이르면 배란 전 값이 나와 해석할 수 없다"
    source: harrison-21
    locator: "392장 p.3031 Clinical Assessment of Ovarian Function"
    basis: current
    exams: [kmle, usmle]
tables:
  - id: ovulation-evidence
    title: "배란의 증거 — 무엇을 보고, 한계는 무엇인가"
    role: tests
    span: column
    section: "가르는 소견 — 배란의 증거와 그 한계"
    columns: ["방법", "보는 것", "한계"]
    rows:
      - ["혈청 프로게스테론", "배란 약 7일 뒤 > 3 ng/mL", "시점이 맞아야 해석된다"]
      - ["기초체온", "주기 후반 0.24°C(> 0.5°F) 상승", "올라간 뒤에야 알 수 있다 — 지난 배란의 증거"]
      - ["소변 LH 급증 검사", "LH 급증 — 약 36시간 뒤 배란", "배란 예측용 — 배란이 일어났다는 증거는 아니다"]
      - ["초음파", "우세 난포 성장·붕괴, 황체, 분비기 내막 에코", "여러 번 봐야 한다"]
      - ["월경전 증상·배란통", "배란 주기에 흔하다", "없다고 무배란이 아니다"]
    note: "harrison-21: 392장 p.3031 본문에서 골라 옮김."
diagram:
  title: "배란 확인 — 시점을 먼저 잡는다"
  nodes:
    - {id: start, kind: start, text: "배란이 되는지 확인하려는 가임기 여성"}
    - {id: regular, kind: decision, text: "주기가 25~35일로 규칙적인가?"}
    - {id: irregular, kind: end, text: "무배란 가능성 — 월경 이상으로 평가"}
    - {id: timing, kind: info, text: "주기 길이 · 다음 월경 예정일 확인"}
    - {id: draw, kind: step, text: "배란 약 7일 뒤 혈청 프로게스테론"}
    - {id: level, kind: decision, text: "프로게스테론 > 3 ng/mL 인가?"}
    - {id: ovulatory, kind: end, text: "배란이 있었다"}
    - {id: when, kind: decision, text: "채혈이 배란 약 7일 뒤였나?"}
    - {id: anov, kind: end, text: "무배란 의심 — 원인 평가"}
    - {id: redraw, kind: end, text: "시점을 맞춰 다시 채혈"}
  edges:
    - {from: start, to: regular}
    - {from: regular, to: timing, label: "예"}
    - {from: regular, to: irregular, label: "아니오"}
    - {from: timing, to: draw}
    - {from: draw, to: level}
    - {from: level, to: ovulatory, label: "예"}
    - {from: level, to: when, label: "아니오"}
    - {from: when, to: anov, label: "예"}
    - {from: when, to: redraw, label: "아니오(이름)"}
diagram_notes:
  - "황체기는 12~14일로 일정하고 주기 길이의 차이는 난포기에서 온다 — 채혈 시점은 다음 월경 예정일에서 거꾸로 센다 [[harrison-21: 392장 p.3031]]."
  - "초경 뒤 2~4년은 무배란·불규칙 주기가 흔하고, 폐경이 가까워지면 무배란 주기가 늘어 출혈이 불규칙해진다 — 이 시기의 불규칙 주기는 그 자체로 이상이 아닐 수 있다 [[harrison-21: 392장 p.3031]]."
  - "보조 증거: 기초체온 주기 후반 0.24°C 상승, 초음파의 우세 난포 붕괴·황체·분비기 내막 에코 [[harrison-21: 392장 p.3031]]."
checks:
  - q: "배란이 있었는지 확인하는 혈청 검사와 기준, 채혈 시점은?"
    a: "배란 약 7일 뒤 혈청 프로게스테론 > 3 ng/mL."
  - q: "35일 주기 여성의 프로게스테론 채혈 시점을 28일 주기와 같은 날짜로 잡으면 안 되는 이유는?"
    a: "황체기는 12~14일로 일정하고 주기가 긴 만큼 난포기가 길다 — 배란이 늦어 같은 날짜면 배란 전 값이 나온다."
  - q: "소변 LH 급증 검사가 알려 주는 것은?"
    a: "약 36시간 뒤 배란이 올 것 — 성교 시점을 맞추는 데 쓴다."
sources:
  - id: harrison-21
    org: "McGraw Hill"
    title: "Harrison's Principles of Internal Medicine, 21st ed. — Chapter 392: Disorders of the Female Reproductive System"
    kind: textbook
    year: 2022
    citation: "Loscalzo J, Fauci AS, Kasper DL, et al (eds). Harrison's Principles of Internal Medicine, 21e. 392장 Disorders of the Female Reproductive System(Hall JE, Dokras A), 인쇄쪽 3027–3032"
    checked_at: 2026-10-25
    checked: "드라이브 장 문서(인쇄쪽 3027–3032)로 본문 대조. p.3027 난소 발생·원시난포·생식세포 수. p.3028 우세 난포(FSH 수용체·아로마타제·에스트라디올·인히빈 A), 배란 전 5~6일 급성장, FSH 가 과립막세포에 LH 수용체 유도, LH 급증이 감수분열 재개·배란 유도, 배란 뒤 황체화. p.3029 2세포 모형(LH-난포막세포 안드로겐, FSH-과립막세포 아로마타제 → 에스트라디올), 황체에서 황체화 과립막세포가 프로게스테론의 주된 근원, LH 와 hCG 가 같은 수용체. p.3030 hCG 가 임신 첫 10주 황체 유지, 프로게스테론의 분비기 내막·자궁경부 점액 점도 증가·기초체온 상승, 인히빈 B·A, AMH(작은 난포, 주기 내내 안정, 난소 예비력 지표), GnRH 박동 빈도와 LH/FSH, 음성 되먹임·에스트로겐 양성 되먹임(뇌하수체)에 의한 LH 급증. p.3031 난포기(FSH 20~30% 상승으로 동원, 단일 난포 선택), 에스트라디올 지수적 상승 → LH 급증, 황체기(황체 수명 유한, hCG 구조, 태반이 6~10주에 넘겨받음), 주기 평가(초경 뒤 2~4년 내 규칙화, 28일·25~35일, 개인 내 ±2일, 황체기 12~14일 일정·주기 차이는 난포기, 출혈 4~6일, 35세 넘으면 짧아짐, 폐경 전 무배란 증가, 규칙 출혈이면 대개 배란, 배란통, 월경전 증상 부재는 무배란 근거 아님, 프로게스테론 > 3 ng/mL 배란 약 7일 뒤·기초체온 0.24°C(> 0.5°F)·소변 LH 급증 검사, 배란은 LH 급증 약 36시간 뒤, 초음파 소견). p.3032 사춘기·성조숙증(이 정리본에는 쓰지 않음). 「다음 월경 약 5~7일 전」은 황체기 12~14일에서 계산한 것이다"
    verified: text
figures_none: 목표가 검사 선택과 채혈 시점(프로게스테론 기준치·황체기 길이)이라 영상 소견이 시험 단서가 아니다
---

## 판단 — 왜 배란 7일 뒤 프로게스테론인가
- 프로게스테론(progesterone)은 배란 뒤 생긴 **황체(corpus luteum)의 황체화 과립막세포**가 주로 낸다 — 배란이 없으면 황체가 없고 프로게스테론도 오르지 않는다 [[harrison-21: 392장 p.3029]].
- 그래서 배란 약 7일 뒤 혈청 프로게스테론 > 3 ng/mL 이면 배란이 있었다고 본다 [[harrison-21: 392장 p.3031]].
- **시점은 다음 월경에서 거꾸로 센다.** 황체기는 12~14일로 일정하고 주기 길이의 차이는 난포기에서 온다 — 주기가 길면 배란이 늦다 [[harrison-21: 392장 p.3031]].
- 규칙적으로 매달 출혈하는 여성은 대개 배란 주기다. 규칙성 자체가 첫 단서이고, 검사는 그것을 확인한다 [[harrison-21: 392장 p.3031]].

## 기전 — 난포에서 황체로, 에스트라디올에서 프로게스테론으로
난포기에는 FSH 를 받는 과립막세포가 난포막세포(theca cell)의 안드로겐을 아로마타제로 바꿔 에스트라디올을 만든다(2세포 모형, two-cell model) [[harrison-21: 392장 p.3029]]. 앞 주기 황체기 끝에 FSH 가 20~30% 오르면 난포 무리가 동원되고, 에스트라디올·인히빈이 FSH 를 눌러 대개 하나의 우세 난포만 자란다 [[harrison-21: 392장 p.3030–3031]]. 우세 난포의 에스트라디올이 지수적으로 오르면 뇌하수체에 **양성 되먹임**이 걸려 LH 급증(LH surge)이 오고, 약 36시간 뒤 배란한다 [[harrison-21: 392장 p.3030–3031]]. 터진 난포는 LH 로 황체화해 프로게스테론·인히빈 A·에스트라디올을 내고, 프로게스테론은 에스트로겐으로 준비된 내막을 분비기로 바꾸고 자궁경부 점액을 끈끈하게 하며 기초체온을 올린다 [[harrison-21: 392장 p.3030–3031]]. 황체는 LH 에 대한 민감도가 줄어 수명이 정해져 있고(그래서 황체기 길이가 일정하다), 임신하면 영양막의 hCG 가 같은 LH 수용체에 붙어 태반이 넘겨받는 6~10주까지 황체를 유지한다 [[harrison-21: 392장 p.3029, p.3031]].

## 가르는 소견 — 배란의 증거와 그 한계
- 기초체온(basal body temperature)은 프로게스테론의 체온 조절 효과로 주기 후반에 0.24°C(> 0.5°F) 오른다 — 오른 뒤에야 알 수 있어 지난 배란의 증거다 [[harrison-21: 392장 p.3031]].
- 소변 LH 급증 검사(ovulation predictor kit)는 배란을 **예측**한다. 배란은 급증 약 36시간 뒤라 성교 시점을 맞추는 데 쓴다 [[harrison-21: 392장 p.3031]].
- 초음파는 난포 동의 성장과 에스트라디올에 따른 내막 두께를 보고, 우세 난포의 붕괴·황체·분비기 내막의 특징적 에코로 배란을 보여 준다 [[harrison-21: 392장 p.3031]].
- **해석의 한계**: 배란통(mittelschmerz)과 월경전 증상은 배란 주기에 흔하지만 없다고 무배란은 아니다. 프로게스테론은 시점이 이르면 배란 전 값이라 낮게 나온다 [[harrison-21: 392장 p.3031]].

## 권고와 예외
- 정상 주기: 첫날부터 다음 월경 전날까지 약 28일(25~35일), 한 여성의 주기 간 변동은 ±2일, 출혈 4~6일 [[harrison-21: 392장 p.3031]].
- 초경 뒤 2~4년은 무배란·불규칙 주기가 흔하고, 35세가 넘으면 주기가 짧아지며, 폐경이 가까워지면 무배란 주기가 늘어 출혈이 불규칙해진다 [[harrison-21: 392장 p.3031]].
- 난소 예비력은 배란 확인과 다른 질문이다 — 항뮐러관호르몬(AMH)이 주기 내내 비교적 안정해 인히빈 B보다 낫고, 20대 초반에 가장 높고 폐경 무렵 크게 준다. 다낭난소증후군에서는 작은 난포가 많아 높다 [[harrison-21: 392장 p.3030]].

## 시험 쟁점 — 충돌·맥락·새 근거
- 해당 없음(대조: 해리슨 392장 p.3027~3032)
