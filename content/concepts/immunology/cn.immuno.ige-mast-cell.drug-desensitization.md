---
id: cn.immuno.ige-mast-cell.drug-desensitization
type: concept
topic: Immunology
see_also: [Infectious Disease, Obstetrics & Gynecology]
date: 2026-11-28
updated: 2026-11-28
version: 1
outline: immuno.hypersensitivity   # 면역학 책 「과민반응」
layer: basic            # 기초 정리본 — 임상 정리본의 roots 가 가리키는 기전 단위
discipline: immunology
system: immune
objective_kind: 기전
textbook_check: unavailable
confidence: medium
review_status: unreviewed
note_form: 2
title: "IgE 비만세포 반응 — 탈감작은 잠시 신호를 끈다"
objective: "IgE 매개 약물 알레르기에서 항원이 비만세포 · 호염기구의 IgE 수용체를 교차결합해 매개물을 쏟는 과정을 설명하고, 작은 용량을 차례로 올리는 탈감작이 그 신호를 일시적으로 막는 이유와 그 상태가 투약을 멈추면 사라지는 이유를 가른다"
condition: IgE 매개 약물 과민반응과 약물 탈감작(IgE-mediated drug allergy, drug desensitization)
exams: [usmle, kmle]
summary:
  - "결론: 탈감작은 약을 아주 적은 용량부터 몇 시간에 걸쳐 올려 비만세포의 IgE 신호를 잠시 끄는 일이다 — 투약이 끊기면 다시 반응한다."
  - "시험 단서: 페니실린 아나필락시스 병력인데 그 약이 유일한 1차 치료(임신 중 매독 등) — IgE-mediated (type I) hypersensitivity, desensitization."
  - "왜: 낮은 용량의 항원이 억제 경로를 켜 IgE 수용체에 탈인산화효소를 불러 매개물 방출을 막고, 목표 용량에 이르러도 아나필락시스가 오지 않는다."
  - "중증 피부 이상반응(SJS · TEN · DRESS) · 혈구감소 · 혈청병 · 혈관염은 탈감작 금기 — 미량으로도 심한 반응이 온다."
pitfalls:
  - contrast: "탈감작 = 알레르기가 낫는다?"
    point: "탈감작은 일시적인 관용이라 지속되는 관용을 만들지 않는다. 투약마다 다시 하거나, 약의 반감기 두 배 이상 쉬면 다시 해야 한다 — 계속 투여하는 동안만 유지된다 [[harrison-22: 365장 p.2816]]."
  - contrast: "스테로이드 · 항히스타민 전처치로 대신?"
    point: "전처치는 처음 증상에 맞춰 고르는 보조일 뿐이고, 스테로이드는 아나필락시스를 막지 못한다 [[harrison-22: 365장 p.2816]]. 피부시험 양성인 IgE 감작 환자는 재노출 때 아나필락시스 위험이 높아 탈감작이 필요하다 [[harrison-22: 365장 p.2818]]."
  - contrast: "모든 약물 반응에 탈감작?"
    point: "탈감작 적응은 1형(IgE 의존 · 비의존) · 사이토카인 방출 · 혼합 · 가벼운 지연형 4형 반응이다. 중증 피부 이상반응 · 2형 · 3형 · 혈관염 · 단일 장기 독성은 금기다 [[harrison-22: 365장 p.2815]] [[harrison-22: 365장 p.2818]]."
tables:
  - id: phenotypes
    title: "약물 과민반응 — 탈감작을 하나"
    role: comparison
    span: column
    section: "고장 — IgE 가 비만세포를 깨운다"
    columns: ["반응", "탈감작"]
    rows:
      - ["1형(IgE 의존 · 비의존) · 사이토카인 방출 · 혼합", "적응 [[harrison-22: 365장 p.2816]]"]
      - ["가벼운 지연형 4형(전신 증상 없는 반점구진 발진)", "적응 [[harrison-22: 365장 p.2815]]"]
      - ["중증 피부 이상반응 · 2형 · 3형 · 혈관염 · 단일 장기 독성", "금기 — 약을 피한다 [[harrison-22: 365장 p.2815]]"]
checks:
  - q: "탈감작한 환자가 약을 며칠 쉬었다가 다시 맞을 때는?"
    a: "탈감작은 일시적이라 반감기 두 배 이상 쉬었으면 다시 탈감작해야 한다."
  - q: "탈감작이 아나필락시스를 막는 기전은?"
    a: "낮은 용량의 항원이 비만세포 · 호염기구의 억제 경로를 켜 IgE 수용체에 탈인산화효소를 불러 신호 전달과 매개물 방출을 막는다."
variants:
  - id: v1
    flip: false
    changed: "핵심 변형 — 탈감작 상태가 투약을 멈추면 사라진다는 것을 묻는다"
    context: "페니실린 아나필락시스 병력 환자의 탈감작 뒤 치료 중단"
    stem: "A 34-year-old woman with a history of penicillin-induced anaphylaxis and a positive penicillin skin test has enterococcal endocarditis. She undergoes a multistep intravenous penicillin desensitization and tolerates full-dose therapy without reaction. One week later, therapy is interrupted for 3 days because of a lost intravenous line. Before penicillin is restarted, which of the following is the most appropriate next step?"
    choices: ["A. Repeat the desensitization protocol", "B. Restart the full dose with diphenhydramine premedication", "C. Restart the full dose with methylprednisolone premedication", "D. Restart the full dose because tolerance is now permanent", "E. Switch permanently to a cephalosporin"]
    answer: "A"
    explanation: "Desensitization produces only a temporary state of tolerance: escalating low doses engage inhibitory mast cell and basophil pathways that block IgE receptor signaling, and the state lasts only while the drug keeps being given. After a pause of two or more half-lives the patient is again at risk of anaphylaxis, so the protocol must be repeated. Antihistamine or corticosteroid premedication does not protect against anaphylaxis."
    kind: application
figures_none: 면역 기전 목표 — 판독할 영상 · 사진 소견이 시험 단서가 아니다
sources:
  - id: harrison-22
    org: "McGraw Hill"
    title: "Harrison's Principles of Internal Medicine, 22nd ed."
    kind: textbook
    year: 2025
    citation: "Harrison's Principles of Internal Medicine, 22e. 364장 Anaphylaxis p.2812–2814 · 365장 Desensitization p.2814–2818"
    checked_at: 2026-11-28
    checked: "본문 대조(드라이브 22판 장별 문서 H22_364 · H22_365) — 364장 p.2812 비만세포 과립(히스타민 · 트립타제 · 키마제 · 헤파린 · TNF-α) 탈과립, 류코트리엔 · 프로스타글란딘 D2 · PAF, 히스타민 → 홍조 · 두드러기 · 고용량에서 저혈압, 류코트리엔 · PGD2 → 기관지 수축 · 혈관 투과성, 항원이 IgE 결합 FcεRI 를 교차결합, IgE 는 적응 면역 감작의 결과, 반복 노출이 위험 인자, 약물이 합텐으로 단백과 결합 · p.2813 비-IgE 비만세포 활성(MRGPRX2)은 첫 노출에도 가능, 트립타제 60~90분 정점 · p.2814 탈감작은 일시적 관용, 페니실린에서 수십 년 입증, 아주 낮은 용량부터 몇 시간에 걸쳐 올림, 반감기에 맞춰 계속 투여하면 유지 / 365장 p.2815 1형 = 비만세포 · 호염기구 활성, IgE 감작은 반복 노출 필요, 지연형 중 탈감작 가능은 전신 증상 없는 반점구진 발진, 중증 피부 이상반응 · 2형 · 3형 · 혈관염 · 단일 장기 독성은 금기, 피부시험 — 아나필락시스는 매개물 고갈로 거짓 음성, 페니실린 · 카보플라틴은 피부시험 음성에서 아나필락시스 보고 없음, IgE 탈감작은 저용량 항원이 켜는 억제 경로 — 탈인산화효소가 IgE 수용체로 와 신호 전달 · 매개물 방출 차단, 탈감작 중 피부시험 일시 음전, 12단계 3백 프로토콜 5.7시간 · p.2816 스테로이드는 아나필락시스를 막지 못함, 오말리주맙 보조, 지속 관용 아님 · 매 노출마다 또는 반감기 2배 이상 쉬면 반복 · p.2818 피부시험 양성은 재노출 시 탈감작 필요, 돌파 반응 10~30 %, 페니실린 탈감작이 아나필락시스 병력 · 피부시험 양성 매독 임신부에 쓰임, 임신은 돌파 반응 위험 인자"
    verified: text
---

## 정상 — 감작이 IgE 를 비만세포에 입힌다
- 약을 반복해 만나면 적응 면역이 그 약에 대한 IgE 를 만든다 — 약은 흔히 합텐으로 몸의 단백과 붙어 면역원이 된다 [[harrison-22: 364장 p.2812]].
- 만들어진 IgE 는 비만세포 · 호염기구의 고친화 수용체(FcεRI)에 붙어 있다. 그래서 IgE 감작은 반복 노출이 필요하고, 항생제 · 항암제에서 전형적이다 [[harrison-22: 365장 p.2815]].

## 고장 — IgE 가 비만세포를 깨운다
- 다시 들어온 항원이 IgE 가 붙은 FcεRI 를 교차결합하면 신호가 켜져 과립이 쏟아진다(탈과립) [[harrison-22: 364장 p.2812]].
- 미리 든 히스타민 · 트립타제가 곧바로 나오고, 류코트리엔 · 프로스타글란딘 D2 · 혈소판 활성화 인자가 새로 만들어진다. 히스타민은 홍조 · 두드러기 · 가려움, 고농도에서 저혈압 · 빈맥을, 류코트리엔과 PGD2 는 기관지 수축과 혈관 투과성 증가를 일으킨다 [[harrison-22: 364장 p.2812]].
- IgE 없이 비만세포가 직접 깨는 반응(MRGPRX2 — 퀴놀론 · 반코마이신 · 근이완제)은 첫 노출에도 생긴다 [[harrison-22: 364장 p.2813]].

## 소견으로 — 몇 분 안의 전신 반응
- 1형 반응은 가려움 · 홍조 · 두드러기 · 혈관부종 · 쌕쌕거림 · 목 조임 · 저혈압으로 오고, 비만세포 과립에서 나온 혈청 트립타제가 오른다 [[harrison-22: 365장 p.2815]].
- 피부시험은 IgE 반응을 국소 팽진 · 발적으로 보여 준다. 반응 직후에는 매개물이 고갈돼 거짓 음성이 날 수 있다 [[harrison-22: 365장 p.2815]].

## 임상 판단으로 — 꼭 필요한 약이면 탈감작
- 원인 약이 유일하거나 가장 좋은 치료일 때, 아주 낮은 용량부터 일정 간격으로 두 배씩 올려 몇 시간 안에 목표 용량에 이른다. 낮은 용량의 항원이 억제 경로를 켜 IgE 수용체에 탈인산화효소를 불러 신호를 막는다 — 탈감작 중에는 피부시험도 잠시 음성이 된다 [[harrison-22: 365장 p.2815]].
- 이 관용은 일시적이다 — 투약을 이어 가는 동안만 유지되고, 반감기 두 배 이상 쉬면 다시 한다 [[harrison-22: 365장 p.2816]].
- 페니실린 아나필락시스 병력 · 피부시험 양성인 임신 중 매독이 대표적 적응이다 — 임상 판단은 `cn.id.syphilis-pregnancy.penicillin-desensitization` [[harrison-22: 365장 p.2818]].

## 시험 쟁점 — 충돌·맥락·새 근거
- 해당 없음(대조: 해리슨 22판 364장 p.2812~2814 · 365장 p.2815~2818)
