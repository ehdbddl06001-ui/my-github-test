---
id: cn.heme.apl.immediate-atra
type: concept
topic: Hematology
see_also: [Oncology]
date: 2026-11-24
updated: 2026-11-25
version: 2
outline: h104            # 해리슨 21판 104장 Acute Myeloid Leukemia → 22판 109장
confidence: medium
review_status: unreviewed
note_form: 2
title: "급성 전골수구 백혈병 — 의심되면 확진 전 ATRA"
objective: "출혈·범혈구감소에 아우어 소체 다발을 가진 비정상 전골수구와 섬유소원 저하 DIC 가 보이면 급성 전골수구 백혈병을 의심하고, 융합 유전자 확진을 기다리지 않고 올-트랜스 레티노산을 즉시 시작한다"
objective_kind: 치료
condition: 급성 전골수구 백혈병(acute promyelocytic leukemia, APL)
exams: [kmle, usmle]
summary:
  - "결론: 급성 전골수구 백혈병이 의심되면 PML-RARA 확진 전에 올-트랜스 레티노산(ATRA)을 바로 시작한다."
  - "시험 단서: 잇몸 출혈·멍 + 범혈구감소, 아우어 소체 다발(faggot cell)의 전골수구, 섬유소원 저하·D-이합체 상승."
  - "왜: 조기 사망은 백혈병이 아니라 DIC 출혈이고, ATRA 가 전골수구를 분화시켜 DIC 를 줄인다."
  - "쓰지 않는 약: 세포독성 항암제만 먼저(과립 방출로 DIC 악화), 헤파린·트라넥삼산 일상 사용, 첫 관해 이식."
  - "백혈구 > 10,000/μL 고위험이면 ATRA 에 세포독성 항암제를 곧바로 더한다 — 분화 증후군·백혈구 급증 때문."
pitfalls:
  - contrast: "「백혈병 = 이식」 vs 응급은 응고병증"
    point: "동종 조혈모세포이식은 관해 뒤 재발 위험이 높은 다른 급성 골수성 백혈병의 공고 치료다. 급성 전골수구 백혈병은 ATRA·비소 삼산화물로 약 85 % 가 장기 생존하는 가장 잘 낫는 아형이라 첫 관해 이식의 자리가 없고, 지금 사람을 죽이는 것은 DIC 출혈이다."
    exception: "재발해 두 번째 관해를 얻은 환자에서는 이식을 검토한다 [[?eln-apl-2019]]."
    cites: ["harrison-22", "?eln-apl-2019"]
    covers: ["kmle-2026-1968:E"]
  - contrast: "시타라빈·다우노루비신 유도 vs 분화 유도"
    point: "급성 전골수구 백혈병도 두 약에 반응하지만, 세포독성 약만 쓰던 시절에는 죽는 백혈병 세포가 과립 성분을 쏟아 DIC 로 많이 사망했다. ATRA 가 DIC 를 줄인 뒤 예후가 바뀌었다."
    exception: "백혈구 > 10,000/μL 고위험군은 ATRA 와 함께 세포독성 항암제로 즉시 세포를 줄인다."
    cites: ["harrison-22"]
    covers: ["kmle-2026-1968:B"]
  - contrast: "출혈이니 트라넥삼산 · 응고가 문제니 헤파린?"
    point: "급성 전골수구 백혈병의 DIC 는 응고와 섬유소용해가 함께 항진된 상태로, 혈전도 생긴다. 항섬유소용해제는 이득이 증명되지 않았고 혈전 위험을 늘리며, 헤파린은 활동성 출혈을 키운다. 원인 치료(ATRA)와 혈소판·동결침전제제 보충이 축이다."
    cites: ["harrison-22", "?eln-apl-2019"]
    covers: ["kmle-2026-1968:A", "kmle-2026-1968:D"]
tables:
  - id: risk
    section: "선택 — 위험도가 유도 요법을 정한다"
    title: "급성 전골수구 백혈병의 유도 요법"
    role: treatment
    span: full
    columns: ["구분", "기준", "유도", "근거"]
    rows:
      - ["의심 단계", "형태 + DIC, 유전자 결과 대기", "ATRA 즉시 + 혈소판·동결침전제제", "[[harrison-22: 109장 p.834]] [[?eln-apl-2019]]"]
      - ["저위험", "백혈구 ≤ 10,000/μL", "ATRA + 비소 삼산화물(항암제 없이)", "[[harrison-22: 109장 p.834]]"]
      - ["고위험", "백혈구 > 10,000/μL", "ATRA + 세포독성 항암제로 즉시 세포 감소", "[[harrison-22: 109장 p.834]]"]
    note: "치료 뒤에는 PML-RARA PCR 로 잔존 질환을 본다 — 신호가 남거나 다시 나오면 재발을 예고한다 [[harrison-22: 109장 p.834]]."
diagram:
  title: "출혈 + 비정상 전골수구 — 급성 전골수구 백혈병의 첫 처치"
  nodes:
    - {id: start, kind: start, text: "출혈·멍 + 범혈구감소"}
    - {id: info, kind: info, text: "말초 도말, PT·aPTT·섬유소원·D-이합체"}
    - {id: apl, kind: decision, text: "아우어 소체 다발 전골수구 + DIC?"}
    - {id: aml, kind: end, text: "다른 급성 백혈병 — 골수·유전 검사로 유도"}
    - {id: atra, kind: step, text: "ATRA 즉시 + 혈소판·동결침전제제"}
    - {id: wbc, kind: decision, text: "백혈구 > 10,000/μL 인가?"}
    - {id: low, kind: end, text: "저위험 — ATRA + 비소 삼산화물"}
    - {id: high, kind: end, text: "고위험 — ATRA + 세포독성 항암제"}
  edges:
    - {from: start, to: info}
    - {from: info, to: apl}
    - {from: apl, to: aml, label: "아니다"}
    - {from: apl, to: atra, label: "그렇다"}
    - {from: atra, to: wbc}
    - {from: wbc, to: low, label: "아니다"}
    - {from: wbc, to: high, label: "그렇다"}
diagram_notes:
  - "PML-RARA 결과(수일)를 기다리지 않는다 — 형태와 DIC 로 의심되면 ATRA 부터 [[?eln-apl-2019]]."
  - "보충 목표(지침): 혈소판 > 30,000–50,000/μL, 섬유소원 > 100–150 mg/dL [[?eln-apl-2019]]."
  - "ATRA 시작 뒤 3주 안의 발열·호흡곤란·폐침윤·체액 저류는 분화 증후군 — 스테로이드, 중증이면 ATRA 를 잠시 멈춘다."
checks:
  - q: "급성 전골수구 백혈병에서 확진 전에 ATRA 를 시작하는 이유는?"
    a: "조기 사망의 주원인이 DIC 출혈이고, ATRA 가 PML-RARA 로 멈춘 분화를 풀어 DIC 를 빠르게 줄이기 때문이다. 다른 아형으로 밝혀져도 며칠의 ATRA 는 해가 적다."
  - q: "ATRA 시작 2주 뒤 발열·호흡곤란·양쪽 폐침윤·체중 증가가 생겼다. 무엇이고 어떻게 하는가?"
    a: "분화 증후군(APL syndrome)이다. 분화한 세포가 폐혈관 내피에 붙어 생긴다 — 스테로이드를 주고, 신부전·중환자실 수준이면 ATRA 를 잠시 멈춘다."
variants:
  - id: v1
    of: kmle-2026-1968
    flip: true
    changed: "도말이 단조로운 모세포(아우어 소체 없음)·섬유소원 정상, 유세포 CD19·CD10·TdT 양성 → 급성 림프모구 백혈병이라 ATRA 의 자리가 없고, 정답이 ATRA 에서 다제 관해 유도 항암 치료로 바뀐다"
    context: "같은 출혈·범혈구감소, 그러나 DIC 가 없고 림프모구인 경우"
    stem: "24세 남자가 2주 전부터 피곤하고 팔다리에 멍이 잘 들어서 왔다. 체온 37.8 ℃, 맥박 98회/분. 목에 1–2 cm 림프절이 여러 개 만져지고 비장이 늑골 아래 2 cm 만져진다. 백혈구 38,000/μL(모세포 80 %), 혈색소 8.6 g/dL, 혈소판 31,000/μL, PT(INR) 1.1, aPTT 31초, 섬유소원 290 mg/dL. 말초혈액 도말에서 세포질이 적고 과립과 아우어 소체가 없는 모세포가 대부분이다. 유세포 분석에서 CD19·CD10·TdT 양성, MPO 음성이다. 가장 적절한 치료는?"
    choices: ["A. 올-트랜스 레티노산 경구", "B. 비소 삼산화물 정맥 주사", "C. 스테로이드를 포함한 다제 관해 유도 항암 치료", "D. 동결침전제제 투여", "E. 동종 조혈모세포이식 의뢰"]
    answer: "C"
    explanation: "원 문항과 달리 아우어 소체가 없고 CD19·CD10·TdT 양성·MPO 음성이라 B세포 급성 림프모구 백혈병이며, 섬유소원·PT 가 정상이라 DIC 도 없다. ATRA·비소 삼산화물은 PML-RARA 를 겨누는 약이라 자리가 없고, 스테로이드를 포함한 다제 관해 유도가 답이다. 섬유소원이 정상이라 동결침전제제가 필요 없고, 이식은 관해 뒤 위험도에 따라 정한다."
    kind: application
  - id: v2
    of: kmle-2026-1968
    flip: false
    changed: "42세 여자의 잇몸 출혈 → 산후가 아닌 35세 남자의 코피·혈뇨, 검사 제시 순서·수치를 바꿈 — 아우어 소체 다발 전골수구 + 섬유소원 저하 DIC + 유전자 결과 대기라는 결정적 단서는 그대로라 답은 ATRA 즉시"
    context: "코피·혈뇨로 온 남자, 같은 형태·DIC 단서"
    stem: "35세 남자가 3일 동안 멎지 않는 코피와 붉은 소변으로 응급실에 왔다. 몸통에 반상 출혈이 흩어져 있다. 혈압 118/74 mmHg, 맥박 108회/분, 체온 37.2 ℃. 섬유소원 70 mg/dL, D-이합체 15 μg/mL FEU, PT(INR) 1.9, 백혈구 3,200/μL, 혈색소 7.9 g/dL, 혈소판 18,000/μL. 말초혈액 도말에서 거친 과립이 가득하고 핵이 두 엽으로 접힌 세포가 많으며, 일부 세포에 아우어 소체가 다발로 모여 있다. 골수 검사와 PML-RARA 검사 결과는 4일 뒤에 나온다. 혈소판과 동결침전제제를 주고 있다. 지금 함께 시작할 치료로 가장 적절한 것은?"
    choices: ["A. 트라넥삼산 정맥 주사", "B. 올-트랜스 레티노산 경구", "C. 저분자량 헤파린 피하 주사", "D. 결과 확인 뒤 치료 결정", "E. 시타라빈 단독 투여"]
    answer: "B"
    explanation: "환자와 출혈 부위는 달라도 아우어 소체 다발을 가진 비정상 전골수구, 섬유소원 70 mg/dL 의 DIC, 유전자 결과 대기라는 단서는 같다. 조기 사망은 DIC 출혈이므로 확진을 기다리지 않고 ATRA 를 시작한다. 백혈구 3,200/μL 라 저위험군이며, 트라넥삼산·헤파린은 이득이 증명되지 않았고 세포독성 약만 먼저 쓰면 DIC 가 악화한다."
    kind: application
sources:
  - id: harrison-22
    org: "McGraw Hill"
    title: "Harrison's Principles of Internal Medicine, 22nd ed."
    kind: textbook
    year: 2025
    citation: "Harrison's Principles of Internal Medicine, 22e. 109장 Acute Myeloid Leukemia p.825–834"
    checked_at: 2026-11-24
    checked: "본문 대조(드라이브 장별 문서 H22_109) — p.826 t(15;17)·PML-RARA 는 APL 과 늘 짝, DIC 는 t(15;17) 과 연관 · p.828 출혈 합병증은 APL 에서 가장 흔하고 DIC 관련 위장관·폐·두개내 출혈, 혈전도 생긴다, 아우어 소체가 있으면 AML · p.833–834 APL 은 약 85 % 장기 생존, 시타라빈·다우노루비신만 쓰던 시절 과립 방출로 인한 DIC 로 사망, ATRA 는 분화를 유도해 DIC 를 줄이고 3주 안 분화 증후군(스테로이드, 중증이면 ATRA 일시 중단, 놓치면 사망 약 10 %), 저위험 ATRA+ATO 가 표준, 백혈구 > 10,000/μL 고위험은 항암제로 즉시 세포 감소, PML-RARA PCR 추적을 확인했다. 확진 전 즉시 시작·수혈 목표·트라넥삼산·이식 서술은 이 장에 없다"
    verified: text
  - id: eln-apl-2019
    org: "European LeukemiaNet"
    title: "Management of acute promyelocytic leukemia: updated recommendations from an expert panel of the European LeukemiaNet"
    kind: guideline
    year: 2019
    citation: "Sanz MA, Fenaux P, Tallman MS, et al. Blood 2019;133(15):1630–1643"
    doi: "10.1182/blood-2019-01-894980"
    checked_at: 2026-11-24
    checked: "서지만 — 루틴 컨테이너가 PubMed·저널 사이트를 막아 원문 미대조. 의심 즉시 ATRA 시작, 혈소판·섬유소원 보충 목표, 항섬유소용해제·헤파린 비권고, 첫 관해 이식 비적응은 기억에 근거하며 사람 대조가 필요하다. 서지·권호·DOI 도 기억이다(학습서 워크플로가 DOI 로 PMID 를 찾는다)"
    verified: citation
figures:
- id: f1
  file: docs/assets/figures/pmc-pmc13722898_figure1.jpg
  kind: histology
  at: 가르는 소견 — 급성 전골수구 백혈병인가
  shows: 급성 전골수구 백혈병의 말초혈액 도말 — 거친 과립의 전골수구와 아우어 소체 다발(faggot cell)
  look_for:
  - 세포질에 바늘 모양 아우어 소체가 여러 개 모인 세포
  - 세포질을 가득 채운 거친 보라색 과립
  label: '「Peripheral blood smear (Wright–Giemsa stain, ×1000 magnification) demonstrating hypergranular promyelocytes. Arrows labeled “Auer rods” indicate characteristic needle‐shaped azurophilic cytoplasmic inclusions. The arrow labeled “Faggot cell” identifies a hypergranular promyelocyte containing numerous bundled Auer rods, a classic morphologic feature of acute promyelocytic leukemia.」 — Acute Promyelocytic Leukemia With PML‐RARA Rearrangement: Clinical and Morphologic Features'
  label_basis: published_figure
  reference: 동료 심사 논문의 그림 설명(저자가 그 소견이라고 쓴 그림)
  paper: 'Acute Promyelocytic Leukemia With PML‐RARA Rearrangement: Clinical and Morphologic Features. Clinical Case Reports'
  doi: 10.1002/ccr3.73830
  credit: 'Acute Promyelocytic Leukemia With PML‐RARA Rearrangement: Clinical and Morphologic Features. Clin Case Rep. 2026 Oct 30;14(11):e73830. doi: 10.1002/ccr3.73830 (CC BY) — FIGURE 1'
  license: CC BY
  url: https://pmc.ncbi.nlm.nih.gov/articles/PMC13722898/
  asset: PMC-PMC13722898_FIGURE1
  privacy_check: 그림 전체를 보았다 — 혈액 도말 현미경 사진뿐이고 얼굴·문신·이름·병원 표지 없음
---

## 판단 — 왜 확진 전에 ATRA 인가
- 급성 전골수구 백혈병(APL)의 출혈 합병증은 DIC 에서 오고, 위장관·폐·두개내 출혈로 죽을 수 있다 [[harrison-22: 109장 p.828]]. 그래서 응급은 백혈병 세포 수가 아니라 응고병증이다.
- ATRA 는 PML-RARA 로 멈춘 분화를 풀어 DIC 를 줄인다 [[harrison-22: 109장 p.834]]. 유전자 결과는 며칠 걸리므로 형태와 DIC 로 의심되면 먼저 시작한다 [[?eln-apl-2019]].
- 혈소판·동결침전제제 보충은 「대신」이 아니라 「함께」다 — 원인을 끄는 약과 빠진 재료를 채우는 처치가 짝을 이룬다.

## 기전 — 분화가 멈춘 전골수구가 응고를 켠다
t(15;17) 이 만드는 PML-RARA 는 레티노산 수용체(RARA)를 망가뜨려 골수구가 전골수구 단계에서 멈추게 한다 [[harrison-22: 109장 p.826, p.834]]. 멈춘 전골수구의 거친 과립에는 응고를 켜고 섬유소를 녹이는 물질이 가득해, 응고와 섬유소용해가 함께 항진된다 — 섬유소원이 떨어지고 D-이합체가 오르며, 출혈이 앞서지만 혈전도 생긴다 [[harrison-22: 109장 p.828]].
- 세포독성 항암제만 쓰면 죽는 세포가 과립을 한꺼번에 쏟아 DIC 가 악화한다 [[harrison-22: 109장 p.834]].
- 약리 용량의 ATRA 는 멈춘 분화를 다시 진행시켜 과립 세포를 성숙 호중구로 바꾼다 — DIC 가 줄어든다.

## 가르는 소견 — 급성 전골수구 백혈병인가
- 아우어 소체가 보이면 급성 골수성 백혈병이 확실하다 [[harrison-22: 109장 p.828]]. 아우어 소체가 다발로 모인 세포(faggot cell)와 두 엽으로 접힌 핵, 거친 과립은 전골수구형을 가리킨다.
- 백혈구는 대개 낮다(저위험) — 높으면 고위험이다. 간비종대·림프절 비대는 흔하지 않다.
- DIC 지표(섬유소원 저하·D-이합체 상승·PT 연장)가 함께 있으면 의심을 굳힌다. 확진은 t(15;17)·PML-RARA 다 [[harrison-22: 109장 p.826]].

## 선택 — 위험도가 유도 요법을 정한다
- 저위험은 ATRA + 비소 삼산화물이 ATRA + 이다루비신보다 나아 표준이 되었고 관해율은 100 % 에 가깝다 [[harrison-22: 109장 p.834]].
- 고위험(백혈구 > 10,000/μL)은 ATRA 뒤 백혈구가 빠르게 오르고 분화 증후군이 생명을 위협하므로 항암제로 즉시 세포를 줄인다 [[harrison-22: 109장 p.834]].
- 분화 증후군: 3주 안 발열·체액 저류·호흡곤란·폐침윤·흉막/심낭 삼출·저산소증 — 스테로이드, 중증(신부전·중환자실)이면 ATRA 일시 중단, 놓치면 사망 약 10 % [[harrison-22: 109장 p.834]].

## 권고와 예외
- 치료 뒤 PML-RARA PCR 로 추적한다 — 신호가 사라지면 장기 무병 생존, 남거나 다시 나오면 재발을 예고한다 [[harrison-22: 109장 p.834]].
- 첫 관해에서 동종 이식의 자리는 없다 — 다른 AML 의 위험도별 공고 치료와 다르다 [[?eln-apl-2019]].

## 시험 쟁점 — 충돌·맥락·새 근거
- 해당 없음(대조: 해리슨 22판 109장 p.826~834 — 해리슨과 어긋난 서술 없음. 확진 전 시작·수혈 목표·항섬유소용해제는 해리슨이 다루지 않아 ELN 지침 서지만, 원문 미대조)
