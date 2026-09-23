---
id: cn.pulm.copd-exacerbation.hypercapnic-failure-niv
type: concept
topic: Pulmonology
see_also: [Emergency Medicine]
date: 2026-09-23
updated: 2026-09-23
version: 1
outline: h292            # 해리슨 21판 292장 Chronic Obstructive Pulmonary Disease(호흡기내과 책)
confidence: medium
review_status: unreviewed
title: "COPD 급성 악화의 급성 고탄산 호흡부전 — 금기가 없으면 비침습적 양압환기가 먼저, 삽관은 금기·실패 때"
objective: "COPD 급성 악화에서 동맥혈 가스로 급성 고탄산 호흡부전(산혈증 + PaCO₂ > 45 mmHg)을 알아보고, 의식·협조·기도 보호·혈역학이 유지되면 비침습적 양압환기를 고르며, 고유량 비강 산소·고농도 산소·즉시 삽관·헬리옥스가 각각 어떤 조건에서 답이 되는지 가른다"
objective_kind: 치료
condition: COPD 급성 악화 — 급성 고탄산 호흡부전
exams: [kmle, usmle]
summary:
  - "COPD 악화에서는 기도 저항과 동적 과팽창이 늘어 호흡근이 해야 할 일이 커지고, 호흡근이 지치면 폐포 환기가 줄어 PaCO₂ 가 오른다. 문제는 산소화보다 **환기**다."
  - "PaCO₂ 가 10 mmHg 오를 때 pH 는 급성이면 약 0.08, 만성이면 약 0.03 떨어진다. PaCO₂ > 45 mmHg 의 환기부전에 산혈증이 동반되면 급성(만성 위의 급성) 호흡부전이다 [[harrison-21: 292장 p.2186]]."
  - "PaCO₂ > 45 mmHg 의 호흡부전에서 비침습적 양압환기(NIPPV)를 시작하면 사망률·삽관 필요·치료 합병증·재원 기간이 모두 준다 [[harrison-21: 292장 p.2189]]."
  - "NIPPV 금기 — 심혈관 불안정, 의식 저하, 협조 불가, 다량 분비물·배출 불가, 마스크를 못 댈 안면 기형·외상, 극도 비만, 심한 화상. 이때와 초기 치료에도 심한 호흡곤란·생명을 위협하는 저산소혈증·심한 고탄산혈증/산혈증·호흡정지가 있으면 삽관한다 [[harrison-21: 292장 p.2189]]."
  - "산소는 저산소혈증을 교정할 만큼 준다. 목표 포화도는 해리슨 ≥ 90 %, GOLD 88–92 % 로 자료마다 다르다(시험 쟁점 Z1) [[harrison-21: 292장 p.2189]] [[?gold-2024]]."
criteria:
  - id: niv-harrison
    name: COPD 악화의 NIPPV·삽관(해리슨)
    kind: 치료 기준
    population: "COPD 급성 악화"
    statement: "PaCO₂ > 45 mmHg 의 호흡부전 → NIPPV(사망·삽관·합병증·재원 감소). 금기: 심혈관 불안정·의식 저하·협조 불가·다량 분비물/배출 불가·안면 기형·외상·극도 비만·심한 화상. 삽관: 초기 치료에도 심한 호흡곤란, 생명 위협 저산소혈증, 심한 고탄산혈증/산혈증, 뚜렷한 의식 저하, 호흡정지, 혈역학 불안정 [[harrison-21: 292장 p.2189]]"
    exceptions: "해리슨은 NIPPV 적응을 PaCO₂ 로만 적는다 — pH 기준(≤ 7.35)은 지침(GOLD·ERS/ATS) 기준이다"
    source: harrison-21
    locator: "292장 p.2189 Mechanical Ventilatory Support"
    basis: current
    exams: [kmle, usmle]
  - id: niv-ers-ats
    name: 급성 고탄산 호흡부전의 NIV(ERS/ATS 2017)
    kind: 치료 기준
    population: "COPD 악화로 인한 급성 또는 만성 위의 급성 고탄산 호흡부전"
    statement: "pH ≤ 7.35 이고 PaCO₂ > 45 mmHg 이면 bilevel NIV 를 권고한다. 고탄산혈증이지만 산혈증이 없으면 NIV 를 쓰지 않는다"
    exceptions: "권고 문구·등급은 원문 미대조 — 루틴 컨테이너에서 학술지 접근 차단"
    source: ers-ats-niv-2017
    locator: "권고 1(원문 미대조)"
    basis: current
    exams: [kmle, usmle]
sources:
  - id: harrison-21
    org: "McGraw Hill"
    title: "Harrison's Principles of Internal Medicine, 21st ed. — Chapter 292: Chronic Obstructive Pulmonary Disease"
    kind: textbook
    year: 2022
    citation: "Loscalzo J, Kasper DL, Longo DL, et al (eds). Harrison's Principles of Internal Medicine, 21e. 292장 p.2180–2189"
    checked_at: 2026-09-23
    checked: "본문 대조(드라이브 문서, 292장) — p.2186 PaCO₂ 10 mmHg 당 pH 변화 급성 0.08·만성 0.03, 환기부전 정의 PaCO₂ > 45 mmHg 와 급성은 산혈증 동반; p.2188 만성 안정기 산소요법의 사망 감소; p.2189 악화 시 흉부 X선·동맥혈 가스 적응(진행된 COPD·고탄산 병력·의식 변화·심한 고통), 입원 적응(호흡성 산증·고탄산혈증 등), 폐색전 고려, 전신 스테로이드, 악화 중 산소는 포화도 ≥ 90 % 유지·급성·만성 고탄산혈증 모두 분당 환기를 줄이지 않고 V/Q 변화로 PaCO₂ 가 약간 오를 수 있으나 산소를 주저하지 말 것, NIPPV 의 효과(PaCO₂ > 45 mmHg)·금기, 삽관 적응"
    verified: text
  - id: gold-2024
    org: "Global Initiative for Chronic Obstructive Lung Disease"
    title: "Global Strategy for the Diagnosis, Management, and Prevention of COPD — 2024 Report"
    kind: guideline
    year: 2024
    url: "https://goldcopd.org/2024-gold-report/"
    checked_at: 2026-09-23
    checked: "서지만 — 컨테이너에서 원문 접근을 확인하지 못했다. 악화 시 목표 포화도 88–92 %·NIV 적응은 원 문항 부록과 기억에 근거"
    verified: citation
  - id: ers-ats-niv-2017
    org: "European Respiratory Society / American Thoracic Society"
    title: "Official ERS/ATS clinical practice guidelines: noninvasive ventilation for acute respiratory failure"
    kind: guideline
    year: 2017
    citation: "Rochwerg B, Brochard L, Elliott MW, et al. Eur Respir J 2017;50(2):1602426"
    doi: "10.1183/13993003.02426-2016"
    checked_at: 2026-09-23
    checked: "서지만 — PubMed·doi 접근 차단으로 권고 본문 미대조. pH ≤ 7.35·PaCO₂ > 45 기준은 기억에 근거"
    verified: citation
tables:
  - id: resp-support
    section: "치료 — 환기를 돕는 도구 고르기"
    title: "COPD 악화의 호흡 보조 — 무엇이 어떤 문제를 푸는가"
    role: treatment
    span: full
    columns: ["도구", "푸는 문제", "고탄산 호흡부전에서", "답이 되는 경우", "근거"]
    rows:
      - ["비침습적 양압환기(BiPAP)", "흡기 보조로 호흡근 일을 덜고 폐포 환기를 늘린다", "금기가 없으면 1차 — 사망·삽관·재원 감소", "PaCO₂ > 45 + 산혈증, 의식·협조·기도 보호·혈역학 유지", "[[harrison-21: 292장 p.2189]] [[?ers-ats-niv-2017]]"]
      - ["기관삽관·침습적 환기", "기도 확보와 완전한 환기 대행", "NIPPV 금기이거나 시도 후 악화 때", "의식 저하·호흡정지·혈역학 불안정·다량 분비물, NIV 실패", "[[harrison-21: 292장 p.2189]]"]
      - ["고유량 비강 산소", "산소화, 비인두 사강 세척", "환기 보조 근거가 NIV 에 못 미친다", "고탄산혈증 없는 저산소성 호흡부전", "[[?ers-ats-niv-2017]]"]
      - ["조절 산소(벤투리·저유량)", "저산소혈증 교정", "필요한 만큼 — 과량은 V/Q 변화로 PaCO₂ 를 올릴 수 있다", "모든 저산소혈증 악화의 기본", "[[harrison-21: 292장 p.2189]]"]
      - ["헬리옥스", "기도 난류 저항 감소", "보조 수단 — 사망·삽관 감소 근거 없음", "일상적 적응 없음", "[[?gold-2024]]"]
    note: "산소·기관지확장제·전신 스테로이드·(적응 시) 항생제는 모든 악화의 바탕이고, 환기 보조는 그 위에 얹는다 [[harrison-21: 292장 p.2189]]."
pitfalls:
  - contrast: "고유량 비강 산소로 먼저 버텨 본다?"
    point: "고유량 비강 산소는 산소화 도구다. 산혈증을 동반한 고탄산 호흡부전은 환기가 문제라, 사망·삽관을 줄이는 근거가 확립된 NIPPV 가 먼저다."
    exception: "고탄산혈증 없는 저산소성 호흡부전이거나, NIPPV 를 견디지 못하는 환자의 대안으로는 고려할 수 있다."
    cites: ["harrison-21", "?ers-ats-niv-2017"]
    covers: ["kmle-2026-0966:B"]
  - contrast: "졸려 하니 바로 삽관?"
    point: "부르면 깨고 협조하며 기도를 지키고 가래를 뱉을 수 있으면 NIPPV 금기가 아니다. 삽관은 뚜렷한 의식 저하·호흡정지·혈역학 불안정·분비물 배출 불가, 또는 NIPPV 1–2시간 뒤 악화 때다."
    cites: ["harrison-21"]
  - contrast: "숨이 차니 비재호흡마스크 15 L/분?"
    point: "산소는 저산소혈증을 교정할 만큼 조절해서 준다. 과량 산소는 저산소성 폐혈관수축이 풀리며 V/Q 가 나빠져 PaCO₂ 를 올릴 수 있다 — 그렇다고 필요한 산소를 주저하지는 않는다."
    cites: ["harrison-21"]
diagram:
  title: "COPD 악화 — 동맥혈 가스로 환기부전을 가르고, 금기로 NIPPV 와 삽관을 가른다"
  nodes:
    - {id: start, kind: start, text: "COPD 악화 — 기관지확장제·전신 스테로이드·(적응 시) 항생제·조절 산소 시작"}
    - {id: info, kind: info, text: "동맥혈 가스(pH·PaCO₂·HCO₃⁻), 의식 수준, 분비물 배출, 혈역학, 흉부 X선으로 폐렴·기흉·심부전 확인"}
    - {id: acid, kind: decision, text: "PaCO₂ > 45 mmHg 이고 pH < 7.35 인가?"}
    - {id: noacid, kind: end, text: "약물 치료 + 조절 산소 유지, 반복 가스로 재평가"}
    - {id: contra, kind: decision, text: "NIPPV 금기가 있는가? (의식 저하·협조 불가·분비물 배출 불가·혈역학 불안정·안면 외상·호흡정지)"}
    - {id: intub, kind: end, text: "기관삽관·침습적 환기"}
    - {id: niv, kind: step, text: "NIPPV(BiPAP) 시작"}
    - {id: re, kind: decision, text: "1–2시간 뒤 pH·PaCO₂·호흡수·의식이 좋아지는가?"}
    - {id: cont, kind: end, text: "NIPPV 유지, 호전되면 점차 이탈"}
  edges:
    - {from: start, to: info}
    - {from: info, to: acid}
    - {from: acid, to: noacid, label: "아니오"}
    - {from: acid, to: contra, label: "예"}
    - {from: contra, to: intub, label: "있음"}
    - {from: contra, to: niv, label: "없음"}
    - {from: niv, to: re}
    - {from: re, to: cont, label: "좋아짐"}
    - {from: re, to: intub, label: "악화·무호전"}
diagram_notes:
  - "HCO₃⁻ 가 높으면(예: 31 mmol/L) 만성 고탄산혈증이 있었다는 뜻이다. 그 위에서 pH 가 떨어졌다면 만성 위의 급성 악화다 [[harrison-21: 292장 p.2186]]."
  - "재평가 시점 1–2시간은 지침 관행이다 [[?ers-ats-niv-2017]]."
checks:
  - q: "pH 7.27, PaCO₂ 70, HCO₃⁻ 31 은 어떤 상태인가?"
    a: "HCO₃⁻ 상승은 만성 고탄산혈증의 신장 보상이고, 그 위에 pH 가 7.35 아래로 떨어져 있으니 만성 위의 급성 호흡성 산증(급성 고탄산 호흡부전)이다."
  - q: "NIPPV 금기 다섯 가지 이상을 대라."
    a: "심혈관 불안정, 의식 저하, 협조 불가, 다량 분비물·배출 불가, 안면 기형·외상, 극도 비만, 심한 화상."
  - q: "NIPPV 를 시작했는데 1시간 뒤 GCS 가 9로 떨어지고 PaCO₂ 가 더 올랐다. 다음은?"
    a: "NIPPV 실패 — 지체 없이 기관삽관한다."
variants:
  - id: v1
    of: kmle-2026-0966
    flip: true
    changed: "졸리나 부르면 깨고 가래를 뱉음·혈역학 안정 → 통증 자극에만 반응(GCS 8)·가래를 뱉지 못해 그르렁거림 → NIPPV 금기가 되어 정답이 비침습적 양압환기에서 기관삽관으로 바뀐다"
    context: "같은 고탄산 호흡부전, 의식·기도 보호만 바꿈"
    stem: "74세 남자가 나흘 전부터 기침과 누런 가래가 늘고 숨이 차더니 오늘 아침부터 깨워도 잘 일어나지 않는다며 가족이 데려왔다. 만성폐쇄성폐질환으로 흡입기를 쓰고 있다. 통증 자극에만 눈을 뜨고 목에서 가래 끓는 소리가 나지만 스스로 뱉지 못한다. 보조 호흡근을 쓰고 양쪽 폐에서 호기 천명이 들린다. 혈압 146/88 mmHg, 맥박 116회/분, 호흡 28회/분, 체온 37.9 ℃. 기관지확장제 분무·전신 스테로이드·항생제를 투여하고 벤투리 마스크로 산소를 주고 있다. 동맥혈 pH 7.22, PaCO₂ 78 mmHg, PaO₂ 56 mmHg, 중탄산염 32 mmol/L, 글래스고 혼수척도 8점이다. 가장 적절한 호흡 보조는?"
    choices: ["A. 비침습적 양압환기", "B. 고유량 비강 산소", "C. 기관삽관 후 기계환기", "D. 비재호흡마스크 15 L/분", "E. 헬리옥스 흡입"]
    answer: "C"
    explanation: "급성 고탄산 호흡부전은 같지만, 뚜렷한 의식 저하(GCS 8)와 분비물을 스스로 뱉지 못하는 것은 NIPPV 금기다. 마스크 환기로는 기도를 지킬 수 없고 흡인 위험이 크므로 기관삽관·침습적 환기가 답이다. 고유량 비강 산소·고농도 산소·헬리옥스는 환기부전과 기도 보호 문제를 풀지 못한다."
    kind: application
  - id: v2
    of: kmle-2026-0966
    flip: false
    changed: "나이·성별(66세 여자)·악화 계기(감기 뒤)·제시 순서를 바꿈, 산혈증 + 고탄산혈증 + 협조·기도 보호·혈역학 유지는 그대로 → 답은 여전히 비침습적 양압환기"
    context: "겉모습만 바꿈 — 상기도 감염 뒤 악화"
    stem: "66세 여자가 일주일 전 감기를 앓은 뒤 숨찬 것이 심해져 왔다. 40갑년 흡연력의 만성폐쇄성폐질환 환자다. 문장을 끝까지 말하지 못하고 목과 어깨 근육을 쓰며 숨을 쉰다. 질문에 느리지만 정확히 답하고 기침해 가래를 뱉는다. 혈압 138/84 mmHg, 맥박 108회/분, 호흡 32회/분. 흉부 X선에서 과팽창 외 새 병변은 없다. 분무 기관지확장제·전신 스테로이드를 주고 벤투리 마스크로 산소포화도 90 % 를 유지하는 상태에서 동맥혈 pH 7.29, PaCO₂ 66 mmHg, PaO₂ 60 mmHg, 중탄산염 30 mmol/L 이다. 다음으로 가장 적절한 처치는?"
    choices: ["A. 기관삽관 후 기계환기", "B. 비침습적 양압환기", "C. 고유량 비강 산소", "D. 산소를 끊고 경과 관찰", "E. 비재호흡마스크 15 L/분"]
    answer: "B"
    explanation: "계기·나이·성별이 달라도 결정적 단서는 같다 — pH < 7.35 와 PaCO₂ > 45 의 급성 고탄산 호흡부전이고, 의식·협조·가래 배출·혈역학이 유지돼 금기가 없으니 NIPPV 가 1차다. 삽관은 금기·실패 때이고, 산소를 끊으면 저산소혈증이 위험하며, 고유량 비강 산소는 환기 보조 근거가 NIV 에 못 미친다."
    kind: application
---

## 정의
**COPD 급성 악화**는 호흡곤란·기침·가래가 평소 변동을 넘어 악화되어 치료를 바꿔야 하는 상태다. 이 정리본의 목표는 악화 가운데 **급성 고탄산 호흡부전** — PaCO₂ > 45 mmHg 의 환기부전에 산혈증이 동반된 상태 [[harrison-21: 292장 p.2186]] — 에서 어떤 호흡 보조를 고르는가다.

## 병태생리
정상 호흡에서는 호흡근이 적은 일로 충분한 폐포 환기를 만들어 PaCO₂ 를 40 mmHg 근처로 유지한다.
1. **악화 → 기도 저항·과팽창 증가**: 감염 등으로 기도 염증·분비물이 늘면 호기 시간 안에 숨을 다 내쉬지 못해 공기가 갇힌다(동적 과팽창, 내인성 PEEP).
2. **호흡근 부담 증가**: 흡기를 시작하려면 내인성 PEEP 를 먼저 이겨야 하고, 편평해진 횡격막은 효율이 떨어진다.
3. **환기 부족 → PaCO₂ 상승**: 호흡근이 지치면 얕고 빠른 호흡이 되어 사강 비율이 커지고 폐포 환기가 줄어 PaCO₂ 가 오른다.
4. **산혈증**: 만성 고탄산혈증 환자는 신장이 HCO₃⁻ 를 올려 pH 를 지켜 왔는데(PaCO₂ 10 mmHg 당 pH 0.03), 급성으로 더 오르면 보상이 따라가지 못해 pH 가 떨어진다(0.08) [[harrison-21: 292장 p.2186]].

NIPPV 는 흡기 압력으로 호흡근 일을 덜어 주고 호기 압력으로 내인성 PEEP 를 상쇄해, 폐포 환기를 늘려 PaCO₂ 를 낮춘다.

## 기전에서 소견으로
- **보조 호흡근 사용·입술 오므리기·말을 잇지 못함**: 호흡 일의 증가.
- **졸림·혼돈**: 고탄산혈증의 CO₂ 마취 효과. 의식 수준은 NIPPV 가능 여부를 가르는 소견이기도 하다.
- **pH ↓ · PaCO₂ ↑ · HCO₃⁻ ↑**: 만성 위의 급성 호흡성 산증.
- **흉부 X선 과팽창, 새 침윤 없음**: 폐렴·기흉·심부전 같은 다른 원인·동반 질환을 배제하는 근거. 폐색전증도 악화 중 늘어나므로 고려한다 [[harrison-21: 292장 p.2189]].

## 감별
- **고탄산성 vs 저산소성 호흡부전**: PaCO₂ 가 오르고 pH 가 떨어졌으면 환기 문제 → 환기 보조(NIPPV). PaCO₂ 가 정상·낮고 산소화만 나쁘면(폐렴 등) 산소화 도구(고유량 비강 산소 등)가 먼저다.
- **NIPPV 가능 vs 삽관 필요**: 금기 목록(요약·기준표)이 가른다 [[harrison-21: 292장 p.2189]].
- **고탄산혈증 있지만 산혈증 없음**: 만성 보상 상태 — NIV 적응이 아니다 [[?ers-ats-niv-2017]].

## 검사
- **동맥혈 가스**: 진행된 COPD, 고탄산 병력, 의식 변화(혼돈·졸림), 심한 고통이 있으면 필수 [[harrison-21: 292장 p.2189]]. NIPPV 1–2시간 뒤 다시 잰다.
- **흉부 X선**: 중등도 이상 고통이나 국소 소견이 있으면 — 약 25 % 에서 이상(폐렴·심부전이 흔함) [[harrison-21: 292장 p.2189]].
- **폐기능 검사**: 악화의 진단·치료에는 도움이 안 된다 [[harrison-21: 292장 p.2189]].
- **입원 적응**: 호흡성 산증·고탄산혈증, 새롭거나 악화된 저산소혈증, 중증 기저 질환, 집에서 관찰이 어려운 경우 [[harrison-21: 292장 p.2189]].

## 치료 — 환기를 돕는 도구 고르기
1. **바탕 치료**: 흡입 베타 작용제·항무스카린제, 전신 스테로이드(프레드니솔론 30–40 mg 5–10일 수준), 적응 시 항생제 [[harrison-21: 292장 p.2189]].
2. **산소**: 저산소혈증을 교정할 만큼. 해리슨은 포화도 ≥ 90 % 를 적고, 산소가 분당 환기를 줄이지는 않지만 V/Q 변화로 PaCO₂ 를 약간 올릴 수 있으며 그래도 필요한 산소를 주저하지 말라고 한다 [[harrison-21: 292장 p.2189]].
3. **NIPPV**: PaCO₂ > 45 mmHg 의 호흡부전에서 사망·삽관·합병증·재원을 줄인다 [[harrison-21: 292장 p.2189]]. 지침은 pH ≤ 7.35 를 함께 요구한다 [[?ers-ats-niv-2017]].
4. **삽관**: NIPPV 금기, 또는 초기 치료에도 심한 호흡곤란·생명 위협 저산소혈증·심한 고탄산혈증/산혈증·뚜렷한 의식 저하·호흡정지·혈역학 불안정 [[harrison-21: 292장 p.2189]].

재평가: NIPPV 1–2시간 뒤 pH·PaCO₂·호흡수·의식이 좋아지지 않으면 삽관을 미루지 않는다 [[?ers-ats-niv-2017]].

## 권고와 예외
- NIPPV 는 협조와 기도 보호를 전제로 한다. 졸림 자체는 금기가 아니지만 뚜렷한 의식 저하·협조 불가는 금기다 [[harrison-21: 292장 p.2189]].
- 헬리옥스·고유량 비강 산소는 NIPPV 를 대신하지 않는다 [[?gold-2024]].
- 한국 급여 기준·기기 설정 세부는 대조하지 않았다.

## 시험 쟁점 — 충돌·맥락·새 근거
- **Z1 충돌 · 악화 중 목표 산소포화도** — 시험 기준: 88–92 %(조절 산소) [[?gold-2024]] / 다른 기준: 해리슨은 악화 중 포화도 ≥ 90 % 유지를 적고, 급·만성 고탄산혈증 모두에서 산소가 분당 환기를 줄이지 않으며 PaCO₂ 상승은 주로 V/Q 변화 때문이라고 쓴다 [[harrison-21: 292장 p.2189]] / 왜 다른가: 지침은 과량 산소의 고탄산 위험을 줄이려 상한을 두고, 교과서는 저산소 교정을 우선한다 — 두 값은 90 % 근처에서 겹친다 / 시험에서는: KMLE 는 88–92 % 를 고른다. 「산소가 호흡 구동을 없애 CO₂ 가 오른다」는 설명은 해리슨과 어긋나니 V/Q 변화(저산소성 폐혈관수축 해제)·홀데인 효과를 기전으로 쓴다. USMLE 도 88–92 % 가 흔한 답이다.
- **Z2 맥락 · NIV 적응의 pH 기준** — 시험 기준: pH ≤ 7.35 + PaCO₂ > 45 [[?ers-ats-niv-2017]] / 다른 기준: 해리슨은 「PaCO₂ > 45 mmHg 의 호흡부전」으로만 적는다 [[harrison-21: 292장 p.2189]] / 왜 다른가: 해리슨의 「호흡부전」 정의에 급성은 산혈증 동반이 들어 있다 [[harrison-21: 292장 p.2186]] / 시험에서는: 산혈증 + 고탄산혈증을 함께 확인한다.

## (심화) 왜 NIPPV 가 사망을 줄이나
삽관을 피하면 인공호흡기 관련 폐렴·진정·이탈 실패 같은 침습적 환기의 합병증이 줄어든다. 해리슨이 NIPPV 의 이득으로 사망률·삽관 필요와 함께 「치료 합병증」·「재원 기간」 감소를 드는 이유다 [[harrison-21: 292장 p.2189]]. 그 대신 실패를 늦게 알아차리면 이득이 사라지므로, 짧은 간격의 재평가가 치료의 일부다.
