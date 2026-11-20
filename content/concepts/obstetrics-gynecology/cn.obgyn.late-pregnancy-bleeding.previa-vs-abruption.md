---
id: cn.obgyn.late-pregnancy-bleeding.previa-vs-abruption
type: concept
topic: Obstetrics & Gynecology
see_also: [Emergency Medicine, Hematology/Oncology]
date: 2026-11-20
updated: 2026-11-20
version: 1
outline: ob.bleeding   # 기본틀 슬롯(content/outline/subjects.yaml) — 산부인과 「임신 중 출혈 — 전치태반·태반조기박리·유산」
confidence: medium
review_status: unreviewed
note_form: 2            # 판형 2(2026-09-25) — 기본틀 빈 슬롯으로 쓴 정리본(오답 연결 없음)
title: "임신 후반기 출혈 — 내진 전 초음파, 통증이 가른다"
objective: "임신 후반기 질출혈에서 내진 전에 초음파로 태반 위치를 확인하고, 통증·자궁 긴장·태아 상태로 전치태반과 태반조기박리를 갈라 경과 관찰과 분만 중 처치를 고른다"
objective_kind: 다음 처치
condition: 임신 후반기 질출혈(antepartum hemorrhage) — 전치태반(placenta previa)·태반조기박리(placental abruption)
exams: [kmle, usmle]
summary:
  - "결론: 임신 후반기 출혈은 내진 전에 초음파로 태반 위치를 보고, 통증·자궁 긴장·태아 상태로 전치태반과 박리를 가른다."
  - "시험 단서: 통증 없는 출혈 = 전치태반(placenta previa), 출혈+복통·잦은 수축·태아심박 이상 = 태반조기박리(abruption)."
  - "왜: 전치태반은 태반이 내구를 덮어 손가락이 출혈을 키우고, 박리는 탈락막 출혈의 트롬빈이 수축·DIC를 부른다."
  - "처치: 안정된 전치태반은 36–37주 계획 제왕절개, 34주 이후 급성 박리는 산모 안정화 뒤 분만한다."
  - "초음파 정상은 박리를 배제하지 못하고(민감도 57 %), 질 출혈량은 박리 중증도와 맞지 않는다."
pitfalls:
  - contrast: "출혈 원인을 보려면 내진부터?"
    point: "전치태반이 배제되기 전에는 손가락 내진을 하지 않는다. 출혈의 양과 근원은 초음파와 멸균 질경 검사로 본다 [[sahu-2024: Antenatal Surveillance]]."
  - contrast: "초음파에 태반 뒤 혈종이 없으면 박리가 아니다?"
    point: "3삼분기 초음파는 혈액과 태반의 에코가 비슷해 놓치기 쉽다 — 한 연구에서 민감도 57 %, 음성예측도 14 %. 박리는 임상 진단이다 [[brandt-2023: Diagnosis]]."
  - contrast: "질 출혈이 적으면 가벼운 박리?"
    point: "피가 자궁 안에 고이는 은닉 박리(concealed abruption)는 출혈이 거의 없어도 태아 사망·응고장애로 갈 수 있다. 출혈량 대신 활력징후·소변량·의식으로 중증도를 본다 [[brandt-2023: Diagnosis]] [[brandt-2023: Clinical management of abruption]]."
  - contrast: "2삼분기 초음파의 전치태반 = 제왕절개 확정?"
    point: "중기 초음파에서는 최대 10 %에서 보이지만 분만 때는 0.5–1 % 이다 [[cassardo-2026]]. 하부 자궁 분절이 자라며 태반이 내구에서 멀어지므로 3삼분기에 경질 초음파로 다시 잰다 [[sahu-2024: Antenatal Surveillance]]."
  - contrast: "박리로 태아가 이미 사망 → 제왕절개?"
    point: "응고장애가 동반되기 쉬워 수술 출혈을 피하려고 질식 분만을 우선한다(시도한 15명 중 14명 성공) [[brandt-2023: Fetal death]]."
  - contrast: "34주 이후 박리에서 수축억제제로 시간을 번다?"
    point: "34–36주 박리에는 자궁수축억제제를 쓰지 않고, 스테로이드를 주려고 분만을 늦추지도 않는다 [[brandt-2023: Clinical management of abruption]]."
tables:
  - id: previa-vs-abruption
    title: "전치태반과 태반조기박리 — 가르는 소견"
    role: differential
    span: column
    section: "가르는 소견 — 통증·자궁·태반 위치"
    columns: ["항목", "전치태반", "태반조기박리"]
    rows:
      - ["정의", "태반이 내구를 덮음. 덮지 않고 20 mm 안이면 저위 태반(low-lying placenta) [[jansen-2022: Introduction]]", "분만 전에 태반이 자궁벽에서 일찍 떨어짐 [[brandt-2023: Introduction]]"]
      - ["출혈·통증", "통증 없는 출혈 [[sahu-2024: Hemorrhage]]", "질 출혈+복통, 수축이 흔함 — 출혈이 없을 수도 있다(은닉) [[brandt-2023: Diagnosis]]"]
      - ["자궁", "—(읽은 출처에 자궁 긴장 기술 없음)", "강직성 수축·잦은 저진폭 수축·자연 빈수축(tachysystole) [[brandt-2023: Clinical management of abruption]] [[brandt-2023: Diagnosis]]"]
      - ["태아심박", "—(읽은 출처에 특이 양상 기술 없음)", "변이 소실·서맥·사인파형·후기·변동성 감속 [[brandt-2023: Clinical management of abruption]]"]
      - ["초음파", "진단 기준 검사 — 경질 초음파로 내구까지 거리를 재고 태반유착·전치혈관을 배제 [[cassardo-2026]]", "태반 뒤·가장자리·융모막 아래 혈종 등. 정상이어도 배제 못 함 [[brandt-2023: Diagnosis]]"]
      - ["위험인자", "이전 제왕절개(가장 큼)·보조생식·다태 [[cassardo-2026]], 자궁 수술·고령·다산·흡연 [[sahu-2024: Maternal Morbidity and Mortality]]", "이전 박리·만성 고혈압·전자간증·코카인·친밀한 파트너 폭력이 가장 큼, 흡연·복부 외상 [[brandt-2023: Epidemiology]] [[brandt-2023: Pathophysiology]]"]
      - ["주된 합병증", "산전 출혈 40–60 %, 산후 출혈 20–35 %, 37주 전 분만 >40 % [[cassardo-2026]]", "출혈성 쇼크·파종혈관내응고(DIC)·자궁절제, 주산기 사망 [[brandt-2023: Adverse outcomes among pregnant people]] [[tikkanen-2011]]"]
  - id: manage
    title: "처치 — 경과 관찰인가 분만인가"
    role: treatment
    span: column
    section: "선택 — 경과 관찰인가 분만인가"
    columns: ["상황", "처치", "근거·주의"]
    rows:
      - ["전치태반 + 새 출혈", "입원, 산모 혈역학·태아 상태 우선, 초음파·질경으로 출혈 평가 [[sahu-2024: Antenatal Surveillance]]", "출혈 횟수가 늘수록 예정 전 응급 분만 위험↑ [[jansen-2022: Interpretation and implication]]"]
      - ["전치태반, 출혈 없거나 멎음", "36–37주 계획 제왕절개(앞쪽 태반이면 그 안에서 이르게) [[cassardo-2026]] [[sahu-2024: Timing and Mode of Delivery]]", "출혈 양상·조기 진통이면 더 일찍 [[sahu-2024: Timing and Mode of Delivery]]"]
      - ["저위 태반(내구에서 11–20 mm)", "질식 분만 시도 가능 [[cassardo-2026]]", "35주 뒤 경질 초음파 거리로 분만 방법을 정한다 [[sahu-2024: Timing and Mode of Delivery]]"]
      - ["34주 이후 급성 박리(경·중 모두)", "산모 안정화 → 분만 [[brandt-2023: Clinical management of abruption]]", "굵은 정맥로·정질액, 혈색소·혈소판·PT·피브리노겐·교차시험 [[brandt-2023: Clinical management of abruption]]"]
      - ["만성 박리(조산, 안정)", "입원 관찰 뒤 외래 가능 — 주 1–2회 태아 감시, 36–37주 분만 [[brandt-2023: Clinical management of abruption]]", "저자 의견 수준. 태아심박 이상이 생기면 분만 [[brandt-2023: Clinical management of abruption]]"]
      - ["박리 + 태아 사망", "질식 분만 우선 [[brandt-2023: Fetal death]]", "이전 자궁 수술이 있으면 개별화 [[brandt-2023: Fetal death]]"]
criteria:
  - id: previa-delivery
    name: 전치태반 분만 시기
    kind: 치료 권고
    population: "합병증 없는(무증상) 전치태반"
    statement: "36–37주에 계획 제왕절개 — 산모 출혈 위험과 의인성 조산의 균형 [[cassardo-2026]]. 캐나다 지침(SOGC)도 36–37주를 권한다고 종설이 인용 [[sahu-2024: Timing and Mode of Delivery]]"
    exceptions: "출혈이 반복되거나 조기 진통이면 더 일찍. 저위 태반 11–20 mm 는 질식 분만 시도 가능"
    source: cassardo-2026
    basis: current
    exams: [kmle, usmle]
  - id: abruption-delivery
    name: 34주 이후 급성 태반조기박리
    kind: 치료 권고
    population: "34주 이후 급성 태반조기박리(경·중 모두)"
    statement: "산모 안정화 후 분만. 37주 전이고 7일 안 분만이 예상되면 산전 코르티코스테로이드를 고려하나 34–36주에는 이를 위해 분만을 늦추지 않으며 수축억제제는 쓰지 않는다 [[brandt-2023: Clinical management of abruption]]"
    exceptions: "34주 전 박리의 처치는 이 정리본의 출처에서 대조하지 않았다"
    source: brandt-2023
    basis: current
    exams: [kmle, usmle]
diagram:
  title: "임신 후반기 질출혈 — 태반 위치와 통증으로 가르기"
  nodes:
    - {id: start, kind: start, text: "임신 후반기 질출혈"}
    - {id: unstable, kind: decision, text: "산모 불안정·태아 상태 이상?"}
    - {id: emerg, kind: alert, text: "소생·수혈 준비 → 즉시 분만"}
    - {id: us, kind: decision, text: "태반이 내구를 덮거나 20 mm 안?"}
    - {id: usinfo, kind: info, text: "태반 위치 모름 — 내진 말고 초음파부터"}
    - {id: prev, kind: decision, text: "출혈이 멎고 36주 전인가?"}
    - {id: expect, kind: end, text: "입원 관찰 → 36–37주 계획 제왕절개"}
    - {id: csec, kind: end, text: "제왕절개 분만"}
    - {id: pain, kind: decision, text: "복통·압통·잦은 수축이 있나?"}
    - {id: abr, kind: alert, text: "태반조기박리 — 안정화 후 분만·DIC 검사"}
    - {id: other, kind: end, text: "다른 원인 — 질경으로 확인"}
  edges:
    - {from: start, to: unstable}
    - {from: unstable, to: emerg, label: "예"}
    - {from: unstable, to: us, label: "아니오"}
    - {from: us, to: prev, label: "예"}
    - {from: us, to: pain, label: "아니오"}
    - {from: us, to: usinfo, label: "미확인"}
    - {from: usinfo, to: prev, label: "전치·저위"}
    - {from: usinfo, to: pain, label: "정상 위치"}
    - {from: prev, to: expect, label: "예"}
    - {from: prev, to: csec, label: "아니오"}
    - {from: pain, to: abr, label: "있음"}
    - {from: pain, to: other, label: "없음"}
diagram_notes:
  - "전치태반이 있는데 분만이 필요하면 방법은 제왕절개다(절대 적응) [[cassardo-2026]]. 저위 태반 11–20 mm 만 질식 분만 시도 대상이다 [[cassardo-2026]]."
  - "태반 위치가 정상인데 통증이 없어도 은닉 박리·자연 빈수축이면 박리를 의심한다 — 초음파 정상은 배제 근거가 아니다 [[brandt-2023: Diagnosis]]."
  - "Rh(D) 음성 산모의 출혈에는 클라이하우어-베트케 검사로 Rh(D) 면역글로불린 용량을 정한다(박리 중증도는 알려 주지 않는다) [[brandt-2023: Clinical management of abruption]]."
  - "박리의 「분만」 경로는 34주 이후 근거다. 34주 전 박리의 경과 관찰 기준은 이 정리본에서 대조하지 않았다."
checks:
  - q: "임신 33주, 통증 없는 선홍색 질출혈. 응급실에서 먼저 하지 말아야 할 것과 먼저 할 것은?"
    a: "손가락 내진을 하지 않는다. 산모 혈역학·태아 상태를 보고 초음파로 태반 위치를 확인한다(질경으로 출혈 근원 확인)."
  - q: "태반조기박리가 의심되는데 초음파가 정상이다. 배제할 수 있나?"
    a: "아니다. 3삼분기 초음파는 민감도가 낮아(한 연구 57 %) 박리는 임상 진단이다 — 통증·수축·태아심박으로 판단한다."
  - q: "박리 산모에서 출혈 양이 적다. 중증도를 무엇으로 보나?"
    a: "출혈량은 중증도와 맞지 않는다(은닉 출혈). 활력징후·소변량·의식, 혈소판·PT·피브리노겐(DIC)과 태아심박으로 본다."
sources:
  - id: brandt-2023
    org: "Brandt JS, Ananth CV (종설)"
    title: "Placental abruption at near-term and term gestations: pathophysiology, epidemiology, diagnosis, and management"
    kind: review
    year: 2023
    citation: "Am J Obstet Gynecol 2023;228(5S):S1313-S1329"
    doi: "10.1016/j.ajog.2022.06.059"
    pmid: "37164498"
    url: "https://doi.org/10.1016/j.ajog.2022.06.059"
    checked_at: 2026-11-20
    checked: "PMC10176440 전문(PubMed 도구)을 처음부터 끝까지 읽음. Introduction(정의) · Pathophysiology(탈락막 출혈·트롬빈의 수축 유발·DIC, 복부 외상·양막 절개 후 감압) · Epidemiology(0.6–1.2 %, 최대 위험인자 표 요약 문장) · Diagnosis(질 출혈+복통, 수축은 비특이, 전치태반·이슬 배제가 필요한 임상 진단, 초음파 민감도 57 %·음성예측도 14 %, 은닉 박리, 쿠블레르 자궁) · Clinical management(34주 이후 급성 박리는 안정화 후 분만, 출혈량≠중증도, 정맥로·검사·클라이하우어-베트케, 태아심박 양상, 스테로이드·수축억제제·마그네슘, 만성 박리 36–37주) · Coagulopathy(박리가 임신 중 DIC 의 가장 흔한 원인) · Fetal death(질식 분만 우선, 15명 중 14명). 34주 전 박리 처치는 범위 밖이라 쓰지 않았다"
    verified: text
  - id: sahu-2024
    org: "Sahu SA, Shrivastava D (종설)"
    title: "Maternal and Perinatal Outcomes in Placenta Previa: A Comprehensive Review of Evidence"
    kind: review
    year: 2024
    citation: "Cureus 2024;16(5):e59737"
    doi: "10.7759/cureus.59737"
    pmid: "38841031"
    url: "https://doi.org/10.7759/cureus.59737"
    checked_at: 2026-11-20
    checked: "PMC11151188 전문(PubMed 도구)을 읽음. Hemorrhage(통증 없는 출혈, 3삼분기 출혈의 주요 원인) · Maternal Morbidity and Mortality(위험인자) · Timing and Mode of Delivery(SOGC 인용 36–37주, 출혈 양상·조기 진통이면 더 일찍, 35주 뒤 내구 거리 <2 cm 면 제왕절개율↑) · Antenatal Surveillance(태반 「이동」, 2삼분기 의심례 대부분 해소, 손가락 내진 회피, 새 출혈이면 입원, 초음파·멸균 질경으로 출혈 평가). 같은 절의 「태아 폐 성숙 확인·헤마토크리트 30 % 유지·수축억제제」 나열은 근거가 오래되어 보이고 다른 출처로 대조하지 못해 쓰지 않았다. 학술지 수준이 낮아 핵심 판단은 cassardo-2026·jansen-2022 와 겹치는 것만 썼다"
    verified: text
  - id: jansen-2022
    org: "Jansen CHJR, van Dijk CE, Kleinrouweler CE, et al (체계적 고찰·메타분석)"
    title: "Risk of preterm birth for placenta previa or low-lying placenta and possible preventive interventions: A systematic review and meta-analysis"
    kind: review
    year: 2022
    citation: "Front Endocrinol (Lausanne) 2022;13:921220"
    doi: "10.3389/fendo.2022.921220"
    pmid: "36120450"
    url: "https://doi.org/10.3389/fendo.2022.921220"
    checked_at: 2026-11-20
    checked: "PMC9478860 전문(PubMed 도구)을 읽음. Introduction · Study selection(전치태반 = 내구를 덮음, 저위 태반 = 덮지 않고 20 mm 안 — 현재 권고 정의로 기술) · Synthesized findings(37주 전 조산 전치태반 46 %, 저위 태반 30 %) · Interpretation and implication(산전 출혈 횟수가 예정 전 응급 분만의 독립 예측인자). 예방 중재(황체호르몬·페서리·봉축)는 근거 불충분이라 이 정리본에 넣지 않았다"
    verified: text
  - id: cassardo-2026
    org: "Cassardo O, Orsi M, Ossola MW, et al (종설)"
    title: "Cesarean delivery for placenta previa"
    kind: review
    year: 2026
    citation: "Am J Obstet Gynecol 2026;233(6S):S255-S271"
    doi: "10.1016/j.ajog.2025.09.010"
    pmid: "41485820"
    url: "https://doi.org/10.1016/j.ajog.2025.09.010"
    checked_at: 2026-11-20
    checked: "PubMed 초록만(전문 PMC 없음). 제왕절개 절대 적응, 분만 때 0.5–1 %·중기 초음파 최대 10 %, 이전 제왕절개가 최대 위험, 보조생식 6배, 산전 출혈 40–60 %·산후 출혈 20–35 %, 37주 전 분만 >40 %, 경질 초음파가 진단 기준(내구 거리·태반유착·전치혈관), 무증상 36–37주 계획 제왕절개(앞쪽 태반이면 이르게), 저위 태반 11–20 mm 질식 분만 시도"
    verified: abstract
  - id: tikkanen-2011
    org: "Tikkanen M (종설)"
    title: "Placental abruption: epidemiology, risk factors and consequences"
    kind: review
    year: 2011
    citation: "Acta Obstet Gynecol Scand 2011;90(2):140-149"
    doi: "10.1111/j.1600-0412.2010.01030.x"
    pmid: "21241259"
    url: "https://doi.org/10.1111/j.1600-0412.2010.01030.x"
    checked_at: 2026-11-20
    checked: "PubMed 초록만. 임신 후반기 질출혈의 주요 원인, 0.4–1 %(북유럽 0.38–0.51 %, 미국 0.6–1.0 %), 산모 위험(출혈·수혈·응급 자궁절제·DIC·신부전), 주산기 결과(조산·질식·사산), 선진국 조산의 약 10 %·주산기 사망의 10–20 %"
    verified: abstract
figures_none: "판단 목표 — 통증·자궁 긴장·태아 상태와 태반 위치(거리 수치)로 가르고, 박리의 초음파 소견은 민감도가 낮아 시험 단서가 아니다"
---

## 판단 — 왜 내진 전 초음파, 그다음 통증인가
- 태반조기박리는 전치태반과 이슬(bloody show)을 배제해야 하는 **임상 진단**이다 — 그래서 태반 위치가 먼저다 [[brandt-2023: Diagnosis]].
- 태반 위치를 모르면 손가락 내진을 하지 않는다. 출혈의 양·근원은 초음파와 멸균 질경으로 본다 [[sahu-2024: Antenatal Surveillance]].
- 위치가 정상이면 **통증·수축·태아심박**이 박리를 가리킨다. 전치태반의 전형은 통증 없는 출혈이다 [[sahu-2024: Hemorrhage]] [[brandt-2023: Diagnosis]].
- 처치는 진단보다 **산모·태아 상태와 주수**가 정한다: 불안정하면 즉시 분만, 안정된 전치태반은 조산 위험과 출혈 위험을 저울질해 기다린다 [[cassardo-2026]].

## 기전 — 출혈이 생기는 자리가 다르다
- **전치태반**: 태반이 내구를 덮거나(전치태반) 20 mm 안에 있다(저위 태반) [[jansen-2022: Study selection]]. 3삼분기에 하부 자궁 분절이 늘어나며 혈류가 적은 그 부위에서 태반이 떨어지기 쉬워 출혈 → 수축 → 조산으로 이어진다고 추정된다 [[jansen-2022: Introduction]]. 같은 분절 성장 때문에 2삼분기의 낮은 태반은 대부분 내구에서 멀어진다 [[sahu-2024: Antenatal Surveillance]].
- **태반조기박리**: 만성 탈락막·자궁태반 혈관병증 위에 외상·급한 감압 같은 급성 계기가 겹쳐 탈락막 혈관이 터진다 [[brandt-2023: Pathophysiology]]. 탈락막의 조직인자가 만든 트롬빈이 자궁을 수축시키고, 혈관 안으로 많이 들어가면 소모성 응고장애(DIC)가 된다 [[brandt-2023: Pathophysiology]]. 박리는 임신 중 DIC 의 가장 흔한 원인이다 [[brandt-2023: Coagulopathy]].
- 피가 자궁 안에 고이면 출혈이 거의 없는 은닉 박리가 되고, 자궁근층으로 스미면 쿠블레르 자궁(Couvelaire uterus)이다 — 이것만으로 자궁절제 적응은 아니다 [[brandt-2023: Diagnosis]].

## 가르는 소견 — 통증·자궁·태반 위치
- 표가 두 질환을 나란히 놓는다. 수축 자체는 정상 진통에도 있어 비특이적이고, **자연 빈수축·강직성 수축과 태아심박 이상**이 박리 쪽으로 기울게 한다 [[brandt-2023: Diagnosis]] [[brandt-2023: Clinical management of abruption]].
- 해석 한계: 초음파 정상은 박리를 배제하지 못한다(민감도 57 %, 다른 연구 80 %) [[brandt-2023: Diagnosis]]. 질 출혈량은 박리의 임상 결과와 맞지 않는다 [[brandt-2023: Clinical management of abruption]].
- 전치태반 진단에는 경질 초음파가 기준이며, 같은 검사로 태반유착 스펙트럼(placenta accreta spectrum)·전치혈관(vasa previa)을 배제한다 [[cassardo-2026]].

## 선택 — 경과 관찰인가 분만인가
- **전치태반**: 새 출혈이면 입원해 산모 혈역학과 태아 상태를 먼저 본다 [[sahu-2024: Antenatal Surveillance]]. 안정되면 36–37주 계획 제왕절개, 출혈이 반복되면 더 일찍 [[cassardo-2026]] [[sahu-2024: Timing and Mode of Delivery]]. 37주 전 분만이 46 % 로 흔하다 [[jansen-2022: Synthesized findings]].
- **34주 이후 급성 박리**: 경증이든 중증이든 산모 안정화 → 분만 [[brandt-2023: Clinical management of abruption]]. 태아 상태는 산모 안정화를 시작한 뒤 평가한다 [[brandt-2023: Clinical management of abruption]].
- 37주 전이고 7일 안 분만이 예상되면 산전 코르티코스테로이드를 고려하되, 34–36주 박리에서 이를 위해 분만을 미루지 않는다 [[brandt-2023: Clinical management of abruption]].

## 권고와 예외
- 34–36주 박리에는 자궁수축억제제를 쓰지 않는다. 황산마그네슘은 신경 보호 목적으로 쓰지 않지만 중증 전자간증이면 경련 예방에 쓴다 [[brandt-2023: Clinical management of abruption]].
- 박리 + 태아 사망은 질식 분만 우선, 이전 자궁 수술·자궁파열 위험이 크면 개별화한다 [[brandt-2023: Fetal death]].
- 34주 전 박리의 경과 관찰 기준, 전치태반에서 수축억제제의 역할은 이 정리본에서 대조하지 않았다(검토 항목 — RCOG Green-top 27a 2026 개정판 전문으로 보강).
- 임신 전반기 출혈(유산·자궁외임신)은 판단 축이 달라 이 정리본에 넣지 않았다(같은 슬롯의 별도 정리본 대상).
