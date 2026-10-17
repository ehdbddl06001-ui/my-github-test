---
id: cn.id.covid19-pneumonia.tocilizumab-add-on
type: concept
topic: Infectious Disease
see_also: [Pulmonology]
date: 2026-10-18
updated: 2026-10-18
version: 1
outline: h199            # 해리슨 21판 199장 Common Viral Respiratory Infections, Including COVID-19(감염내과 책)
confidence: medium
review_status: unreviewed
note_form: 2            # 판형 2(2026-09-25)
title: "COVID-19 폐렴 악화 — 스테로이드 증량 아닌 IL-6 차단"
objective: "덱사메타손 중에도 산소 요구량이 빠르게 늘고 CRP 가 높은 COVID-19 폐렴에 토실리주맙을 더하는 것을 고른다"
objective_kind: 치료
condition: 입원한 중증·진행성 COVID-19 폐렴(severe or progressive COVID-19 pneumonia)의 면역조절 치료
exams: [usmle, kmle]
summary:
  - "결론: 덱사메타손 중에도 빠르게 악화하는 COVID-19 폐렴에는 토실리주맙(tocilizumab)을 더한다."
  - "시험 단서: SARS-CoV-2 양성 + 양측 폐렴 + 덱사메타손 중 하루 새 고유량 산소로 악화 + CRP 높음 + 프로칼시토닌 낮음."
  - "왜: 2주째 저산소증은 숙주 염증(IL-6)이 몰고 간다 — 같은 약 증량이 아니라 다른 경로를 막아야 사망률이 준다."
  - "고용량 스테로이드 증량·이버멕틴은 쓰지 않는다. 회복기 혈장은 고역가·병 초기·체액면역 결핍 환자에 한정된다."
pitfalls:
  - contrast: "회복기 혈장 — 항체를 주면 바이러스가 줄 것?"
    point: "회복기 혈장의 중화항체 역가는 대개 낮아 효과가 제한적이고, 허가도 고역가 혈장을 입원 초기 또는 체액면역이 손상된 환자에만 쓰도록 좁혀졌다 [[harrison-21: 199장 p.1510]]. 발병 7일 넘게 지나 염증으로 악화하는 단계에서는 항바이러스·항체보다 면역조절이 답이다."
    exception: "B세포 고갈 치료(리툭시맙 등)로 항체를 못 만드는 환자의 병 초기라면 고역가 회복기 혈장을 고려한다."
    covers: ["imaging-2026-0344:D"]
  - contrast: "덱사메타손으로 안 되면 스테로이드를 더 세게?"
    point: "고용량 글루코코르티코이드는 고혈당·동반 감염 위험을 늘리고 [[harrison-21: 199장 p.1510]], 표준 용량보다 사망률을 낮추지 못했다 [[?nih-covid]]. 덱사메타손은 유지하고 다른 경로(IL-6 수용체·JAK)를 막는 약을 더한다."
  - contrast: "열·CRP 상승 = 세균 동반 감염?"
    point: "COVID-19 의 염증 자체가 열과 CRP 를 올린다. 프로칼시토닌이 낮고 엽성 경화·화농성 객담이 없으면 경험적 광범위 항생제 근거는 부족하다 [[harrison-21: 199장 p.1510~1511]]."
    exception: "엽성 경화·화농성 객담·높은 프로칼시토닌이면 세균 동반 감염 치료가 먼저다."
tables:
  - id: covid-immunomod-choice
    section: "선택 — 무엇을 더하고 무엇을 쓰지 않나"
    title: "입원 COVID-19 — 덱사메타손 위에 더할 것"
    role: treatment
    span: column
    columns: ["약", "작용", "쓰는 때", "주의"]
    rows:
      - ["토실리주맙", "IL-6 수용체 단클론항체", "덱사메타손 중 중증·진행 [[harrison-21: 199장 p.1510]]", "활동성 세균·진균 감염 [[?nih-covid]]"]
      - ["바리시티닙", "JAK1/2 억제", "산소·기계환기 필요 [[harrison-21: 199장 p.1510]]", "해리슨 21판은 렘데시비르 병용 허가만 서술"]
      - ["고용량 스테로이드", "같은 경로 증량", "근거 없음 [[?nih-covid]]", "고혈당·동반 감염 [[harrison-21: 199장 p.1510]]"]
      - ["회복기 혈장", "다클론 중화항체", "고역가 · 입원 초기 · 체액면역 결핍 [[harrison-21: 199장 p.1510]]", "역가가 낮아 효과 제한"]
diagram:
  title: "입원 COVID-19 폐렴 — 덱사메타손 중 악화"
  nodes:
    - {id: start, kind: start, text: "SARS-CoV-2 폐렴 입원 — 산소 투여 중"}
    - {id: dexa, kind: step, text: "덱사메타손 시작(± 렘데시비르)"}
    - {id: prog, kind: decision, text: "덱사메타손 중에도 빠르게 악화하는가?"}
    - {id: ask, kind: info, text: "산소 요구 변화·CRP·감염 징후 확인"}
    - {id: stable, kind: end, text: "안정 → 덱사메타손 유지"}
    - {id: infx, kind: decision, text: "세균·진균 동반 감염 징후?"}
    - {id: abx, kind: end, text: "있음 → 동반 감염부터 치료"}
    - {id: toci, kind: end, text: "없음 → 토실리주맙(또는 바리시티닙) 추가"}
  edges:
    - {from: start, to: dexa}
    - {from: dexa, to: prog}
    - {from: prog, to: infx, label: "급속 악화"}
    - {from: prog, to: stable, label: "안정"}
    - {from: prog, to: ask, label: "정보 없음"}
    - {from: ask, to: infx, label: "악화·CRP 높음"}
    - {from: ask, to: stable, label: "안정"}
    - {from: infx, to: abx, label: "있음"}
    - {from: infx, to: toci, label: "없음"}
diagram_notes:
  - "「빠른 악화」 — 고유량 산소·비침습 환기·기계환기로 올라가는 산소 요구. 시험에서 흔히 CRP ≥ 7.5 mg/dL 를 함께 준다 [[?recovery-toci-2021]]."
  - "덱사메타손은 끊지 않는다 — 토실리주맙은 덱사메타손에 **더하는** 약이다 [[harrison-21: 199장 p.1510]]."
  - "토실리주맙 전 확인: 활동성 세균·진균 감염, 심한 호중구감소, 크게 오른 간효소. IL-6 차단 뒤에는 열·CRP 가 눌려 이후 감염을 알아보기 어렵다 [[?nih-covid]]."
  - "저산소증의 기준은 실내 공기 산소포화도 ≤ 94 % 다 [[harrison-21: 199장 p.1510]]."
checks:
  - q: "덱사메타손 중에도 산소 요구가 빠르게 늘고 CRP 가 높은 COVID-19 폐렴에서 다음 약물 치료는?"
    a: "덱사메타손을 유지하고 토실리주맙(IL-6 수용체 차단, 또는 바리시티닙)을 더한다."
  - q: "회복기 혈장을 고려할 수 있는 환자는?"
    a: "고역가 혈장을 입원 초기 또는 체액면역이 손상된 환자에게."
  - q: "토실리주맙을 더하기 전에 확인할 것은?"
    a: "세균·진균 동반 감염이 없는지(프로칼시토닌·영상), 심한 호중구감소·간효소 상승이 없는지."
variants:
  - id: v1
    of: imaging-2026-0344
    flip: true
    changed: "양쪽 하폐야 간유리 음영·프로칼시토닌 0.1 → 오른쪽 아래엽 엽성 경화·녹슨 화농성 객담·백혈구 18,500·프로칼시토닌 6.2 → 답이 토실리주맙에서 세균 동반 폐렴 치료(세프트리악손+아지트로마이신)로 바뀜"
    context: "단서를 바꿔 답이 바뀌는 변형 — COVID-19 입원 중 세균 동반 감염"
    stem: "A 46-year-old man is admitted to the hospital because of fever, cough, and shortness of breath for 6 days. A nasopharyngeal swab is positive for SARS-CoV-2 by RT-PCR. He is treated with dexamethasone and 2 L/min of oxygen by nasal cannula. Over the next 36 hours, his oxygen requirement increases to 6 L/min, and he begins coughing up rust-colored purulent sputum. Temperature is 39.2°C (102.6°F), pulse is 112/min, and respirations are 26/min. Bronchial breath sounds are heard over the right lower lung field. Leukocyte count is 18,500/mm3 with 88% neutrophils. Serum procalcitonin concentration is 6.2 ng/mL. A chest x-ray shows dense consolidation of the right lower lobe with air bronchograms. Sputum Gram stain shows many neutrophils and gram-positive diplococci. In addition to continuing dexamethasone, which of the following is the most appropriate next step in pharmacotherapy?"
    choices: ["A. Tocilizumab", "B. Ceftriaxone and azithromycin", "C. High-dose intravenous methylprednisolone", "D. COVID-19 convalescent plasma", "E. Ivermectin"]
    answer: "B"
    explanation: "Lobar consolidation with purulent sputum, neutrophilic leukocytosis, a high procalcitonin, and gram-positive diplococci point to a bacterial (pneumococcal) superinfection, so antibiotics come first. Tocilizumab is avoided while an active bacterial infection is untreated. In the original item, both lower zones were hazy, procalcitonin was low, and the worsening was driven by inflammation — so tocilizumab was added instead."
    kind: application
  - id: v2
    of: imaging-2026-0344
    flip: false
    changed: "40세 여자 → 63세 남자, 고유량 산소 → 비침습 환기, CRP 14 → 19 mg/dL, 렘데시비르 언급 삭제 — 「덱사메타손 중 빠른 악화 + 높은 CRP + 세균 감염 징후 없음」은 그대로 → 답은 여전히 토실리주맙"
    context: "겉모습만 바꾸고 답은 같은 변형 — 고령 남성, 비침습 환기"
    stem: "A 63-year-old man with hypertension is hospitalized on day 8 of a SARS-CoV-2 infection with fever and dyspnea. Dexamethasone and supplemental oxygen were started on admission 2 days ago. Since then his oxygen needs have escalated, and he now requires noninvasive positive-pressure ventilation with an FiO2 of 0.7 to maintain oxygen saturation at 92%. Temperature is 38.4°C (101.1°F), pulse is 104/min, and blood pressure is 138/82 mm Hg. Diffuse crackles are heard bilaterally. Leukocyte count is 6800/mm3, absolute neutrophil count is 5100/mm3, and serum C-reactive protein concentration is 19 mg/dL (N <0.5). Serum procalcitonin concentration is 0.08 ng/mL, and serum ALT activity is 41 U/L. Chest x-ray shows bilateral peripheral hazy opacities. Blood and sputum cultures show no growth to date. In addition to continuing dexamethasone, which of the following is the most appropriate next step in pharmacotherapy?"
    choices: ["A. Pulse-dose intravenous methylprednisolone", "B. Hydroxychloroquine", "C. Tocilizumab", "D. Piperacillin-tazobactam and vancomycin", "E. COVID-19 convalescent plasma"]
    answer: "C"
    explanation: "Age, sex, the level of respiratory support, and the CRP value changed, but the decisive clues did not: rapid worsening despite dexamethasone, a markedly high CRP, and no sign of bacterial infection (low procalcitonin, negative cultures, normal neutrophils and ALT). Adding the IL-6 receptor blocker tocilizumab to dexamethasone is the step with mortality benefit; pulse steroids add no benefit, and convalescent plasma is limited to early disease or impaired humoral immunity."
    kind: application
sources:
  - id: harrison-21
    org: "McGraw Hill"
    title: "Harrison's Principles of Internal Medicine, 21st ed. — Chapter 199: Common Viral Respiratory Infections, Including COVID-19"
    kind: textbook
    year: 2022
    citation: "Loscalzo J, Fauci AS, Kasper DL, et al (eds). Harrison's Principles of Internal Medicine, 21e. 199장 Common Viral Respiratory Infections, Including COVID-19, 인쇄쪽 1510–1511"
    checked_at: 2026-10-18
    checked: "드라이브 장 문서로 본문 대조. p.1510 근거가 가장 강한 치료(덱사메타손·렘데시비르±바리시티닙·토실리주맙·단클론항체), 중증 = 실내 공기 산소포화도 ≤94 % 저산소증, 바리시티닙은 렘데시비르 병용으로 산소·기계환기 환자에 EUA(2021년 5월 기준), 글루코코르티코이드 중 덱사메타손 근거가 가장 많고 고용량 시 고혈당·동반 감염 감시, IL-6 억제제 중 토실리주맙 근거가 가장 강하고 중증·진행성 COVID-19 에 덱사메타손에 더하기를 권함, 회복기 혈장은 역가가 낮아 효과 제한·2021년 2월 EUA 를 고역가·입원 초기·체액면역 손상 환자로 축소. p.1510–1511 세균 동반 감염 빈도 불확실, 다른 적응 없이 경험적 광범위 항생제 권고 근거 부족, 시작했다면 근거 없으면 줄이거나 중단"
    verified: text
  - id: recovery-toci-2021
    org: "RECOVERY Collaborative Group"
    title: "Tocilizumab in patients admitted to hospital with COVID-19 (RECOVERY): a randomised, controlled, open-label, platform trial"
    kind: trial
    year: 2021
    citation: "Lancet 2021;397(10285):1637-1645"
    pmid: "33933206"
    checked_at: 2026-10-18
    checked: "서지만(문항 imaging-2026-0344 해설 근거 목록에서 옮김, 원문·초록 미대조 — 컨테이너가 PubMed 를 막음). PMID 는 기억으로 적었다(학습서 워크플로가 확인 — 검토 항목). 저산소증·CRP ≥7.5 mg/dL 환자의 사망률 감소 서술에 쓴다"
    verified: citation
  - id: nih-covid
    org: "NIH COVID-19 Treatment Guidelines Panel"
    title: "Coronavirus Disease 2019 (COVID-19) Treatment Guidelines — Therapeutic management of hospitalized adults (final version)"
    kind: guideline
    year: 2024
    citation: "National Institutes of Health. COVID-19 Treatment Guidelines (archived final version)"
    url: "https://www.covid19treatmentguidelines.nih.gov/"
    checked_at: 2026-10-18
    checked: "서지만(문항 해설 근거 목록에서 옮김, 원문 미대조 — 판·연도는 검토 항목). 고용량 스테로이드 무익, 토실리주맙 투여 전 확인 사항, 덱사메타손과 바리시티닙 병용 서술에 쓴다"
    verified: citation
figures_none: 약물 선택 목표 — 답은 산소 요구 추이·CRP·프로칼시토닌으로 갈리고, 흉부 X선의 양측 음영은 바이러스 폐렴 확인일 뿐 판단 단서가 아니다(코호트 영상은 병변 단위 라벨도 없음)
---

## 판단 — 왜 토실리주맙이 먼저인가
- 이 환자는 이미 덱사메타손을 맞고 있는데도 하루 만에 저유량 → 고유량 산소로 올라갔고 CRP 가 높다 — **진행성 중증 COVID-19** 이다.
- 그 단계의 악화는 바이러스 증식보다 **숙주 염증**이 몰고 가며, IL-6 는 그 중심 매개체다. IL-6 수용체를 막는 토실리주맙을 덱사메타손에 더하는 근거가 가장 강하다 [[harrison-21: 199장 p.1510]] [[?recovery-toci-2021]].
- 같은 경로를 더 세게 누르는 고용량 스테로이드는 이득 없이 고혈당·동반 감염만 늘린다 [[harrison-21: 199장 p.1510]] [[?nih-covid]].
- 낮은 프로칼시토닌·정상 간효소는 「세균 동반 감염 아님」과 「토실리주맙 금기 아님」 두 역할을 한다.

## 기전 — 바이러스 단계에서 염증 단계로
SARS-CoV-2 는 첫 주에 기도·폐포 상피에서 증식하고, 이때는 항바이러스제와 중화항체가 의미가 크다. 둘째 주에 접어들며 일부 환자에서 숙주 면역 반응이 커져 D-이합체·페리틴·CRP·IL-6 가 오르고, 이 수치가 높을수록 중증이다 [[harrison-21: 199장 p.1510]]. IL-6 는 간에서 CRP 를 만들게 하고 열을 내며 모세혈관 누출을 키워 폐포를 물로 채운다 — 그래서 산소 요구가 갑자기 늘어난다. 덱사메타손은 염증을 넓게 누르지만, 그 위에서도 진행하면 IL-6 신호 자체(수용체)를 막거나 여러 사이토카인 신호가 모이는 JAK 를 막아야 한다. 이미 염증 단계에 들어선 환자에게 바이러스 항체(회복기 혈장)를 주는 것은 원인이 바뀐 뒤의 치료다.

## 선택 — 무엇을 더하고 무엇을 쓰지 않나
- 덱사메타손은 유지하고 그 위에 **면역조절제 하나**를 더한다(표). 해리슨 21판은 토실리주맙 근거가 가장 강하다고 서술한다 [[harrison-21: 199장 p.1510]].
- 회복기 혈장은 중화항체 역가가 대개 낮고, 허가도 고역가 혈장 · 입원 초기 · 체액면역 손상 환자로 좁혀졌다 [[harrison-21: 199장 p.1510]].
- 세균 동반 감염의 빈도는 불확실하고, 다른 적응 없이 경험적 광범위 항생제를 쓸 근거는 부족하다 — 시작했다면 근거가 없을 때 줄이거나 끊는다 [[harrison-21: 199장 p.1510~1511]].
- 투여 뒤에는 IL-6 차단이 열·CRP 를 누르므로 새 감염을 증상·영상·배양으로 감시한다 [[?nih-covid]].

## 권고와 예외
- 저산소증(실내 공기 산소포화도 ≤ 94 %)이 있으면 산소를 주고, 호흡부전이면 삽관·기계환기로 간다 [[harrison-21: 199장 p.1510]].
- 활동성 세균·진균 감염, 심한 호중구감소, 크게 오른 간효소가 있으면 토실리주맙을 미룬다 [[?nih-covid]].
- 이버멕틴은 COVID-19 치료 근거가 없다 — 분선충증 같은 기생충 감염(면역억제 전 선제 치료 등)에 쓰는 약이다.

## 시험 쟁점 — 충돌·맥락·새 근거
- **Z1 새 근거 · 바리시티닙의 병용 약** — 시험 기준: 덱사메타손에 토실리주맙 또는 바리시티닙을 더한다 [[?nih-covid]] / 다른 기준: 바리시티닙은 렘데시비르와 병용으로 산소·기계환기 환자에 긴급사용 허가(2021년 5월 기준) [[harrison-21: 199장 p.1510]] / 왜 다른가: 해리슨 21판 원고 시점 이후 바리시티닙을 덱사메타손과 함께 쓴 자료가 쌓였다(원문 미대조) / 시험에서는: KMLE · USMLE 모두 보기에 있으면 토실리주맙이 가장 안전한 답, 바리시티닙은 대안으로 알아 둔다.
- **Z2 맥락 · 회복기 혈장의 허가 범위** — 시험 기준: 입원한 진행성 환자에게는 쓰지 않는다 / 다른 기준: 2020년 8월 역가와 무관하게 입원 환자 EUA → 2021년 2월 고역가 · 입원 초기 · 체액면역 손상 환자로 축소 [[harrison-21: 199장 p.1510]] / 왜 다른가: 시점별 허가 변화 / 시험에서는: KMLE · USMLE 모두 「체액면역 결핍 + 병 초기」일 때만 답이 된다.
