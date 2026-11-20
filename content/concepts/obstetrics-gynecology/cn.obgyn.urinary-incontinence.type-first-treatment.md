---
id: cn.obgyn.urinary-incontinence.type-first-treatment
type: concept
topic: Obstetrics & Gynecology
see_also: [Urology]
date: 2026-11-20
updated: 2026-11-20
version: 1
outline: gyn.urogyn     # 기본틀 슬롯(content/outline/subjects.yaml) — 산부인과 「골반장기탈출증과 요실금」(해리슨 대조 대상 아님)
confidence: medium
review_status: unreviewed
note_form: 2            # 판형 2(2026-09-25) — 기본틀 [gap] 으로 쓴 정리본(오답 연결 없음)
title: "여성 요실금 — 새는 상황과 잔뇨가 첫 치료를 정한다"
objective: "여성 요실금을 새는 상황(기침·재채기 vs 갑작스러운 요의)과 기본 평가(소변검사·잔뇨)로 복압성·절박성·범람으로 가르고 유형별 첫 치료를 고른다"
objective_kind: 치료
condition: 여성 요실금(urinary incontinence in women) — 복압성·절박성·혼합성·범람(일류성)
exams: [kmle, usmle]
summary:
  - "결론: 기침·재채기 때 새면 골반저근 운동, 갑자기 마려워 새면 방광 훈련(실패하면 약), 잔뇨가 많으면 범람 — 원인 교정·도뇨."
  - "시험 단서: 힘줄 때 소량(stress UI) vs 참지 못하는 요의(urgency UI) vs 잔뇨↑·방광 팽만(overflow, incomplete emptying)."
  - "왜: 복압성은 요도 지지·괄약근 약화, 절박성은 배뇨근 과활동이라 고치는 곳(골반저 vs 방광)이 다르다."
  - "복압성에는 전신 약물을 권하지 않고, 비수술 치료 전 요역동학 검사는 필요 없다 — 소변검사로 감염·혈뇨를 먼저 거른다."
  - "잔뇨(노인 기준): 0–100 mL 정상, 100–200 mL 증상과 함께 해석, >200 mL 비정상 — 기준은 자료마다 다르다(시험 쟁점)."
pitfalls:
  - contrast: "복압성 요실금 — 약부터?"
    point: "ACP 는 복압성 요실금에 전신 약물 치료를 권하지 않고(강한 권고), 골반저근 운동을 1차로 권한다 [[acp-2014]]. 둘록세틴은 부작용(구역·자살 사고) 우려로 1차로 쓰지 않는다 [[aoki-2017: Medical interventions — SNRIs]]."
    cites: ["acp-2014", "aoki-2017: Medical interventions"]
  - contrast: "절박성 요실금 = 바로 항무스카린제?"
    point: "ACP 는 방광 훈련을 먼저 권하고, 방광 훈련이 실패하면 약물을 권한다 [[acp-2014]]. 약은 효과가 몇 주 뒤에 나타나므로 시작 전 증상을 기록해 비교한다 [[aoki-2017: Medical interventions]]."
    exception: "1차 진료에서는 행동 치료와 함께 항무스카린제를 시작하기도 한다 — 시험 쟁점 Z3."
  - contrast: "요역동학 검사부터?"
    point: "합병증 없는 복압성·절박성·혼합성 요실금에는 비수술 치료 전에 요역동학 검사를 권하지 않는다 — 초기 평가 뒤에도 진단이 불확실하거나, 증상과 진찰이 어긋나거나, 치료에 실패했을 때 한다 [[aoki-2017: Urodynamic studies]]."
  - contrast: "잔뇨가 많은데 항콜린제?"
    point: "항콜린 작용 약·마약성 진통제는 불완전 배뇨를 일으키는 원인 약이다 — 잔뇨가 많으면 원인 약을 줄이고, 이중 배뇨·간헐 도뇨로 비운다 [[harrison-22: 489장 p.3890]] [[harrison-22: 489장 p.3893]]."
  - contrast: "기침 유발 검사 음성 = 복압성 아님?"
    point: "2–4기 골반장기탈출증은 요도를 꺾어 기침 유발 검사가 거짓 음성일 수 있다 — 탈출을 손가락으로 밀어 올리고 다시 검사하는 방법이 있으나 근거는 제한적이다 [[aoki-2017: Physical examination]]."
  - contrast: "전신 호르몬 요법이 요실금을 줄인다?"
    point: "전신 호르몬 대체 요법은 요실금을 악화시켰다(특히 에스트로겐+프로게스테론) [[aoki-2017: Vaginal oestrogen]]. 위축 변화가 있으면 저용량 질 에스트로겐을 쓴다 — 요실금의 주 치료는 아니다 [[harrison-22: 489장 p.3890]]."
tables:
  - id: ui-type-clues
    title: "요실금 유형 — 새는 상황과 기본 평가"
    role: differential
    span: column
    section: "가르는 소견 — 언제 새는가와 잔뇨"
    columns: ["유형", "새는 상황", "기전", "기본 평가에서"]
    rows:
      - ["복압성(stress UI)", "기침·재채기·운동 때 [[aoki-2017: 머리말]]", "요도 과운동(지지 소실)·괄약근 약화 [[aoki-2017: Stress urinary incontinence]]", "기침 유발 검사 양성(방광 약 300 mL) [[aoki-2017: Physical examination]]"]
      - ["절박성(urgency UI)", "갑작스럽고 참기 어려운 요의와 함께 [[aoki-2017: 머리말]]", "배뇨근 과활동·낮은 유순도·방광 과민 [[aoki-2017: Urgency urinary incontinence]]", "소변검사로 감염을 배제해야 과민성 방광으로 본다 [[aoki-2017: Urinalysis]]"]
      - ["혼합성(mixed UI)", "두 상황 모두 [[aoki-2017: 머리말]]", "두 기전이 겹친다", "더 괴로운 증상을 정해 치료 순서를 잡는다 [[aoki-2017: Diagnosis]]"]
      - ["범람(overflow) — 불완전 배뇨 동반", "요의·힘줌과 무관하게 샌다 — 3IQ 는 「다른 원인」으로 분류 [[harrison-22: 489장 p.3891]]", "방광이 다 비지 않는다 — 원인 약·변 매복·출구 꺾임 [[harrison-22: 489장 p.3890]]", "잔뇨 >200 mL(노인) 비정상 [[harrison-22: 489장 p.3891]]"]
  - id: ui-first-treatment
    title: "유형별 첫 치료와 다음 단계"
    role: treatment
    span: column
    section: "선택 — 유형별 첫 치료와 다음 단계"
    columns: ["유형", "첫 치료", "다음 단계·주의"]
    rows:
      - ["복압성", "골반저근 운동(강한 권고·높은 질) [[acp-2014]]", "전신 약물 ✗ [[acp-2014]]. 보존 치료 뒤 중부요도 슬링(1차 수술) [[aoki-2017: Stress incontinence surgery]]"]
      - ["절박성", "방광 훈련(강한 권고·중등도 질) [[acp-2014]]", "실패하면 약 — 내약성·부작용·편의·비용으로 고른다 [[acp-2014]]"]
      - ["혼합성", "골반저근 운동 + 방광 훈련 [[acp-2014]]", "수술은 복압성 성분만 고친다 — 절박성 치료가 따로 필요할 수 있다 [[aoki-2017: Stress incontinence surgery]]"]
      - ["범람(불완전 배뇨)", "원인 약 정리·방광 훈련·이중 배뇨·간헐 도뇨 [[harrison-22: 489장 p.3893]]", "요폐·출구 폐쇄는 전문의 의뢰 [[aoki-2017: Symptoms and risk factors]]. 유치 도뇨는 선택된 환자만 [[harrison-22: 489장 p.3893]]"]
      - ["비만한 여성(모든 유형)", "체중 감량·운동 [[acp-2014]]", "기저 체중 3–5 % 이상 감량에서 복압성 삽화 47 % 감소 [[aoki-2017: Weight loss]]"]
diagram:
  title: "여성 요실금 — 기본 평가에서 첫 치료까지"
  nodes:
    - {id: start, kind: start, text: "여성 요실금 — 새는 상황을 묻는다"}
    - {id: ua, kind: decision, text: "소변검사에서 감염·혈뇨?"}
    - {id: fix, kind: alert, text: "감염 치료·혈뇨 평가를 먼저"}
    - {id: pvr, kind: decision, text: "잔뇨가 많은가?"}
    - {id: overflow, kind: alert, text: "범람 — 원인 약 정리·이중 배뇨·도뇨"}
    - {id: when, kind: decision, text: "언제 새는가?"}
    - {id: diary, kind: info, text: "배뇨일지·기침 유발 검사로 확인"}
    - {id: sui, kind: end, text: "복압성 — 골반저근 운동"}
    - {id: uui, kind: end, text: "절박성 — 방광 훈련, 실패 시 약"}
    - {id: mui, kind: end, text: "혼합성 — 골반저근 운동 + 방광 훈련"}
  edges:
    - {from: start, to: ua}
    - {from: ua, to: fix, label: "있음"}
    - {from: ua, to: pvr, label: "없음"}
    - {from: pvr, to: overflow, label: "많음"}
    - {from: pvr, to: when, label: "정상"}
    - {from: when, to: sui, label: "기침·재채기"}
    - {from: when, to: uui, label: "갑작스러운 요의"}
    - {from: when, to: mui, label: "둘 다"}
    - {from: when, to: diary, label: "불분명"}
    - {from: diary, to: sui, label: "기침 때 샘"}
    - {from: diary, to: uui, label: "요의 때 샘"}
diagram_notes:
  - "잔뇨 측정은 배뇨 증상·증상 있는 골반장기탈출·만져지는 방광이 있을 때 권하며, 초음파(방광 스캐너)로 잰다 [[aoki-2017: Post-void residual volume assessment]]. 노인은 병력·진찰만으로 불완전 배뇨를 찾기 어려워 대부분 잰다 [[harrison-22: 489장 p.3891]]."
  - "재발성 요로감염·무균 농뇨·혈뇨·지속 누출(누공 의심)·요폐·신경 증상·골반 방사선·요로 수술력은 전문의 의뢰 [[aoki-2017: Symptoms and risk factors]]."
  - "노인·쇠약자는 가역 원인(섬망·감염·약·정신 질환·과다 수분·운동 제한·변 매복)을 먼저 찾는다 [[aoki-2017: Symptoms and risk factors]] [[harrison-22: 489장 p.3890]]."
  - "비만하면 유형과 무관하게 체중 감량·운동을 더한다 [[acp-2014]]."
checks:
  - q: "기침할 때 소량씩 새는 45세 여성, 소변검사 정상·잔뇨 정상. 첫 치료는?"
    a: "골반저근 운동. 복압성 요실금에는 전신 약물을 권하지 않고, 비수술 치료 전 요역동학 검사도 필요 없다."
  - q: "절박성 요실금에서 약을 시작하는 시점은(ACP)?"
    a: "방광 훈련이 실패한 뒤. 약은 내약성·부작용·편의·비용으로 고르고, 효과는 몇 주 뒤에 판단한다."
  - q: "요실금 여성의 잔뇨가 많으면 어떤 치료를 피하고 무엇을 하나?"
    a: "방광 수축을 더 줄이는 항콜린 작용 약 등 원인 약을 줄이고, 이중 배뇨·간헐 도뇨로 비운다. 요폐·출구 폐쇄는 전문의에게 보낸다."
sources:
  - id: aoki-2017
    org: "Aoki Y, Brown HW, Brubaker L, Cornu JN, Daly JO, Cartwright R (Nature Reviews Disease Primers)"
    title: "Urinary incontinence in women"
    kind: review
    year: 2017
    citation: "Nat Rev Dis Primers 2017;3:17042"
    doi: "10.1038/nrdp.2017.42"
    pmid: "28681849"
    url: "https://pmc.ncbi.nlm.nih.gov/articles/PMC5878864/"
    checked_at: 2026-11-20
    checked: "PMC 전문(PMC5878864) 대조 — 머리말(IUGA/ICS 정의: 복압성 = 기침·재채기·신체 활동과 함께, 절박성 = 갑작스럽고 미루기 어려운 요의와 함께, 혼합성), Mechanisms(복압성 = 요도 과운동·괄약근 약화·해먹 가설, 절박성 = 배뇨근 과활동·낮은 유순도·방광 과민), Diagnosis(병력·진찰·소변검사·잔뇨·전문의 의뢰 조건, 우세 증상으로 치료 방향), Symptoms and risk factors(의뢰 조건·노인 가역 원인 DIPPERS), Physical examination(기침 유발 검사 방광 약 300 mL·민감도·특이도 높음, 2–4기 탈출의 거짓 음성), Urinalysis(감염 선별, 과민성 방광 진단에 감염 배제 필요), Post-void residual volume assessment(측정 적응·초음파, 직후 >30 mL·10분 뒤 100 mL까지, ≥100 mL 재측정, 배뇨 장애가 치료 선택을 바꿈), Urodynamic studies(비수술 치료 전 비권고, 불확실·불일치·실패 때), Weight loss(3–5 % 감량 → 복압성 삽화 47 % 감소), PFMT(감독 PFMT 근거가 복압성에서 가장 강함, 절박성은 덜함, 장기 근거 부족), Medical interventions(효과 몇 주 뒤, 질 에스트로겐·전신 HRT 악화, 항무스카린 부작용·노인 인지, 미라베그론 고혈압, 둘록세틴 1차 아님), Stress incontinence surgery(보존 치료 먼저, 중부요도 슬링 1차 수술·완치 >80 %, 혼합성은 절박성 보조 치료 필요). 이 고찰에는 「overflow」라는 용어가 없다"
    verified: text
  - id: harrison-22
    org: "McGraw Hill"
    title: "Harrison's Principles of Internal Medicine, 22nd ed. — Chapter 489: Caring for the Geriatric Patient"
    kind: textbook
    year: 2025
    citation: "Harrison's Principles of Internal Medicine, 22e. 489장 Caring for the Geriatric Patient — Urinary Incontinence and Overactive Bladder, 인쇄쪽 3889–3893(표 489-10·489-11·489-12, 그림 489-9)"
    checked_at: 2026-11-20
    checked: "드라이브 22판 장 문서(489장)로 본문 대조 — p.3890 표 489-10 가역 원인(요로감염·위축성 질염·변 매복·고혈당·과다 카페인/수분·섬망·약: 이뇨제, 항콜린제와 마약성 진통제 = 불완전 배뇨, α 작용제, ACE 억제제 = 기침, 경구 에스트로겐은 요실금 유발·악화)·선 자세 기침 유발 검사, p.3891 3IQ(새는 상황으로 유형 구분, 활동·요의 없이 새면 「다른 원인」)·노인 대부분 잔뇨 측정, 잔뇨 0–100 정상·100–200 증상과 해석·>200 mL 비정상, 의뢰 조건, 항무스카린제·β3 작용제 = 과민성 방광·절박성, α 작용제는 FDA 미승인, p.3892 표 489-11 병력·진찰, p.3893 표 489-12 유형별 주 치료(복압성: 골반근 운동·행동·α 작용제·국소 에스트로겐·주입·수술 / 절박성: 골반근 운동·시간 배뇨·이중 배뇨·약 / 불완전 배뇨 동반: α 차단제(남성)·방광 훈련·이중 배뇨·간헐 도뇨·선택적 유치 도뇨). 노인 대상 장이라 젊은 여성 수치로 옮기지 않았다"
    verified: text
  - id: acp-2014
    org: "American College of Physicians (Qaseem A, et al.)"
    title: "Nonsurgical management of urinary incontinence in women: a clinical practice guideline from the American College of Physicians"
    kind: guideline
    year: 2014
    citation: "Ann Intern Med 2014;161(6):429-440"
    doi: "10.7326/M13-2410"
    pmid: "25222388"
    url: "https://doi.org/10.7326/M13-2410"
    checked_at: 2026-11-20
    checked: "PubMed 초록과 대조 — 권고 6개와 등급: 복압성 PFMT 1차(강·높음), 절박성 방광 훈련(강·중등도), 혼합성 PFMT+방광 훈련(강·중등도), 복압성 전신 약물 반대(강·낮음), 방광 훈련 실패 시 절박성 약물(강·높음, 내약성·부작용·편의·비용으로 선택), 비만 여성 체중 감량·운동(강·중등도). 전문은 PMC 에 없어 보지 못했다"
    verified: abstract
  - id: dumoulin-2018
    org: "Dumoulin C, Cacciari LP, Hay-Smith EJC (Cochrane 체계적 고찰)"
    title: "Pelvic floor muscle training versus no treatment, or inactive control treatments, for urinary incontinence in women"
    kind: review
    year: 2018
    citation: "Cochrane Database Syst Rev 2018;10:CD005654"
    doi: "10.1002/14651858.CD005654.pub4"
    pmid: "30288727"
    url: "https://pmc.ncbi.nlm.nih.gov/articles/PMC6516955/"
    checked_at: 2026-11-20
    checked: "PubMed 초록과 대조 — 31개 시험·1,817명, 복압성에서 PFMT 군 완치 보고 56 % vs 6 %(RR 8.38, 95 % CI 3.68–19.07, 높은 질), 모든 유형 35 % vs 6 %(RR 5.34, 중등도), 절박성 단독·혼합성 연구는 각 1개뿐, 부작용 드묾·경미, 추적 대개 12개월 미만. PMC 전문은 열지 않았다"
    verified: abstract
  - id: lukacz-2017
    org: "Lukacz ES, Santiago-Lastra Y, Albo ME, Brubaker L (JAMA 종설)"
    title: "Urinary Incontinence in Women: A Review"
    kind: review
    year: 2017
    citation: "JAMA 2017;318(16):1592-1604"
    doi: "10.1001/jama.2017.12137"
    pmid: "29067433"
    url: "https://doi.org/10.1001/jama.2017.12137"
    checked_at: 2026-11-20
    checked: "PubMed 초록과 대조 — 감염·혈뇨 배제, 심각한 기저 병변이 없으면 감독 없는 골반근 운동·생활 교정 시작, 절박성 약물은 광범위한 평가 없이 시작하고 제때 재평가, 중부요도 슬링 증상 호전 48–90 %·그물 합병증 <5 %. 전문은 보지 못했다"
    verified: abstract
  - id: al-dossari-2024
    org: "Al-Dossari R, Kalra M, Adkison J, Nguyen BM (J Am Board Fam Med 종설)"
    title: "Non-Surgical Management of Urinary Incontinence"
    kind: review
    year: 2024
    citation: "J Am Board Fam Med 2024;37(5):909-918"
    doi: "10.3122/jabfm.2023.230471R1"
    pmid: "39978852"
    url: "https://doi.org/10.3122/jabfm.2023.230471R1"
    checked_at: 2026-11-20
    checked: "PubMed 초록과 대조 — 유형에 복압성·절박성(과민성 방광)·혼합성·신경인성·범람(overflow)을 나눔, 절박성 1차 = 행동 치료, 복압성 1차 = PFMT·질 기구, 항무스카린제·β3 작용제는 행동 치료로 호전되지 않을 때, β3 작용제는 항콜린 부작용이 적음, BPH 범람 요실금(남성) α1 차단제 1차, 신경인성 방광은 깨끗한 간헐 도뇨 1차(카테터 관련 감염 위험). 전문은 보지 못했다"
    verified: abstract
figures_none: 판단 목표 — 새는 상황·소변검사·잔뇨 수치로 가르고 영상 소견이 시험 단서가 아니다
---

## 판단 — 왜 새는 상황과 잔뇨로 첫 치료가 갈리나
- 요실금은 증상만으로 원인이 정해지지 않는다 — 병력·진찰·소변검사·잔뇨 측정 뒤 대부분 복압성·절박성·혼합성으로 잠정 진단한다 [[aoki-2017: Diagnosis]].
- **새는 상황**이 유형을 가른다: 기침·재채기·운동 때면 복압성(stress), 갑작스럽고 참기 어려운 요의와 함께면 절박성(urgency), 둘 다면 혼합성(mixed) [[aoki-2017: 머리말]] [[harrison-22: 489장 p.3891]].
- **소변검사**는 감염을 거르는 관문이다 — 감염을 배제해야 과민성 방광으로 진단하고, 혈뇨·당뇨도 함께 본다 [[aoki-2017: Urinalysis]] [[lukacz-2017]].
- **잔뇨**가 많으면 저장 문제가 아니라 비우지 못하는 문제다 — 범람(일류성) 요실금(overflow; 해리슨은 「불완전 배뇨를 동반한 요실금」)으로 치료가 완전히 달라진다 [[harrison-22: 489장 p.3893]] [[al-dossari-2024]].
- 유형마다 고치는 곳이 다르다: 복압성은 골반저(골반저근 운동), 절박성은 방광(방광 훈련 → 약), 범람은 비우기(원인 교정·도뇨) [[acp-2014]] [[harrison-22: 489장 p.3893]].

## 기전 — 저장에서 누출로
정상 방광은 교감신경 우세로 낮은 압력에서 소변을 저장하고(편안한 한계 약 500 mL), 부교감신경(S2–S4)이 배뇨를 맡는다 [[aoki-2017: Bladder structure and function]].
- **복압성**: 질 앞벽의 골반 내 근막이 요도를 받치는 「해먹」이 분만·비만·만성 기침·변비·폐경으로 약해지면, 복압이 오를 때 요도가 눌리지 않고 아래로 밀려 요도압이 방광압보다 낮아진다(요도 과운동). 괄약근 자체가 약하면 내인성 괄약근 결손이다 [[aoki-2017: Stress urinary incontinence]].
- **절박성**: 채우는 동안 배뇨근이 저절로 수축(배뇨근 과활동)하거나, 유순도가 낮거나(방사선·장기 도뇨 뒤), 방광 감각이 과민해 요의가 괄약근 저항을 넘는다 [[aoki-2017: Urgency urinary incontinence]]. 그래서 약은 무스카린 수용체를 막거나 β3 수용체를 자극해 배뇨근을 이완시킨다 [[aoki-2017: Urgency urinary incontinence]].
- **범람**: 항콜린 작용 약·마약성 진통제가 배뇨를 불완전하게 하고, 변 매복이 출구를 부분적으로 막아 방광이 다 비지 않는다 [[harrison-22: 489장 p.3890]]. 2–4기 골반장기탈출증은 요도를 꺾을 수 있다 [[aoki-2017: Physical examination]].

## 가르는 소견 — 언제 새는가와 잔뇨
- 기침 유발 검사(방광 약 300 mL, 누운 자세 또는 선 자세에서 세게 기침) 양성은 복압성 진단에 민감도·특이도가 높다 [[aoki-2017: Physical examination]].
- 잔뇨는 배뇨 증상·증상 있는 탈출·만져지는 방광이 있을 때 재고, 초음파로 잴 수 있다 [[aoki-2017: Post-void residual volume assessment]]. 노인은 병력·진찰만으로 불완전 배뇨를 찾기 어려워 대부분 잰다 [[harrison-22: 489장 p.3891]].
- 정상·음성 결과의 한계: 탈출이 있으면 기침 유발 검사가 거짓 음성일 수 있고 [[aoki-2017: Physical examination]], 잔뇨는 방광이 찬 상태에서 재야 하며 힘주면 값이 달라진다 [[harrison-22: 489장 p.3891]]. 노인은 무증상 세균뇨가 흔해 소변검사 양성만으로 항생제를 쓰지 않는다 [[aoki-2017: Urinalysis]].

## 선택 — 유형별 첫 치료와 다음 단계
- 복압성: 골반저근 운동이 1차다 [[acp-2014]]. 무치료 대비 완치 보고 56 % vs 6 %(RR 8.38, 높은 질 근거)이고 부작용은 드물다 [[dumoulin-2018]]. 기침 등 복압이 오르기 직전과 그동안 골반저근을 수축하도록 가르친다 [[aoki-2017: PFMT]].
- 절박성: 방광 훈련(배뇨 간격을 계획적으로 늘림)을 먼저, 실패하면 약 [[acp-2014]] [[aoki-2017: PFMT]]. 항무스카린제는 입마름·변비·흐린 시야·졸림·혼동을 일으키고 노인에서는 인지 영향이 우려돼 대안을 권한다. 미라베그론(β3 작용제)은 입마름이 적지만 고혈압을 악화시킬 수 있다 [[aoki-2017: Medical interventions]].
- 재평가: 약 효과는 몇 주 뒤에 나타나므로 시작 전 증상을 기록해 비교한다 [[aoki-2017: Medical interventions]]. 보존 치료가 실패하면 복압성은 중부요도 슬링을 고려한다 [[aoki-2017: Stress incontinence surgery]].

## 권고와 예외
- 합병증 없는 요실금의 비수술 치료 전에는 요역동학 검사를 하지 않는다 [[aoki-2017: Urodynamic studies]].
- 재발성 요로감염·무균 농뇨·혈뇨·지속 누출(누공)·요폐·신경 증상·골반 방사선은 전문의에게 보낸다 [[aoki-2017: Symptoms and risk factors]].
- 비만하면 체중 감량·운동을 권한다 [[acp-2014]]. 전신 호르몬 요법은 요실금을 악화시킨다 [[aoki-2017: Vaginal oestrogen]].
- 약 용량, 젊은 여성의 범람 요실금 원인(신경인성 방광 등) 세부는 대조하지 않았다(검토 항목).

## 시험 쟁점 — 충돌·맥락·새 근거
- **Z1 충돌 · 복압성 요실금의 약물** — 시험 기준: 전신 약물을 권하지 않는다, 골반저근 운동 [[acp-2014]] / 다른 기준: 노인 복압성의 주 치료 목록에 α 작용제(FDA 미승인)를 올린다 [[harrison-22: 489장 p.3893]] / 왜 다른가: ACP 는 여성 전체 대상 근거 등급 지침, 해리슨 표는 노인 진료 교과서 목록 / 시험에서는: KMLE·USMLE 모두 첫 치료는 골반저근 운동, 약물은 오답으로 본다.
- **Z2 맥락 · 잔뇨 기준** — 시험 기준: 노인은 0–100 mL 정상, 100–200 mL 증상과 함께, >200 mL 비정상 [[harrison-22: 489장 p.3891]] / 다른 기준: 배뇨 직후 >30 mL(10분 뒤면 100 mL까지)를 증가로 정의, ≥100 mL 면 재측정, 의미 있는 값은 임상의마다 크게 다르다 [[aoki-2017: Post-void residual volume assessment]] / 왜 다른가: 측정 시점·방법·대상 나이 / 시험에서는: 숫자보다 「잔뇨가 크게 늘고 방광이 만져진다 → 범람」을 묻는다.
- **Z3 충돌 · 절박성의 약 시작 시점** — 시험 기준: 방광 훈련 먼저, 실패하면 약 [[acp-2014]] / 다른 기준: 1차 진료에서 행동 치료와 함께 항무스카린제를 1차로 쓰기도 하고 [[aoki-2017: Medical interventions]], 절박성 약은 광범위한 평가 없이 시작할 수 있다 [[lukacz-2017]] / 왜 다른가: ACP 는 근거 등급의 순서, 종설은 실제 진료 관행 / 시험에서는: 「첫 치료」를 물으면 방광 훈련, 「훈련 실패 뒤」면 약.
- **Z4 맥락 · 혼합성의 첫 치료** — 시험 기준: 골반저근 운동 + 방광 훈련 [[acp-2014]] / 다른 기준: 우세 증상을 정하고 대개 절박성 쪽 치료부터 이득을 본다 [[aoki-2017: Diagnosis]] / 왜 다른가: 같은 행동 치료 안에서 무엇을 앞세우는가의 차이 / 시험에서는: 행동 치료 둘을 함께 고른다.
