---
id: cn.obgyn.granulosa-cell-tumor.tumor-marker
type: concept
topic: Obstetrics & Gynecology
see_also: [Pathology]
date: 2026-10-23
updated: 2026-10-23
version: 2
outline: gyn.oncology            # 산부인과 손 슬롯 「부인암 — 자궁경부·자궁내막·난소·융모성 질환」(outline.py --harrison: 대조 대상 아님) — 같은 주제를 다루는 해리슨 89장(혈액종양내과 h89)을 따로 읽어 대조했다
confidence: medium
review_status: unreviewed
note_form: 2            # 판형 2(2026-09-25) — 결론·시험 단서·왜 → 혼동 → 표·도식 → 목표에 맞춘 본문
title: "과립막세포종 — 추적 표지자는 기원 세포가 정한다"
objective: "에스트로겐 과다 징후와 조직 소견으로 난소 과립막세포종을 알아보고, 재발 감시 표지자로 인히빈을 고른다"
objective_kind: 검사 선택
condition: 성인형 난소 과립막세포종(adult granulosa cell tumor)의 재발 감시 표지자
exams: [kmle, usmle]
summary:
  - "결론: 성인형 과립막세포종(granulosa cell tumor)의 재발 감시 표지자는 인히빈(inhibin) B 다 — CA-125 가 아니다."
  - "시험 단서: 폐경 후 출혈 + 자궁내막 증식·선암 + 한쪽 고형 난소 종괴, 조직의 Call-Exner 소체·커피콩 핵."
  - "왜: 표지자는 종양이 나온 세포가 만드는 물질이다 — 과립막세포는 에스트라디올과 인히빈을 분비한다."
  - "CA-125 는 상피성(특히 고등급 장액성) 암, AFP·β-hCG 는 생식세포 종양, CEA 는 점액성·위장관 전이 종양의 표지자다."
pitfalls:
  - contrast: "인히빈 B vs CA-125 — 난소암이면 CA-125?"
    point: "CA-125 는 체강 상피에서 나온 상피성 난소암(특히 고등급 장액성)의 표지자다 [[harrison-21: 89장 p.696]]. 과립막세포종은 상피가 아니라 성끈-간질(sex cord-stromal) 종양이라 과립막세포가 분비하는 인히빈이 재발 때 먼저 오른다 [[?novak-16]]."
    exception: "조직이 유두 구조·사종체(psammoma body)를 가진 고등급 장액성 암이면 CA-125 로 추적한다."
    covers: ["imaging-2026-0412:B"]
  - contrast: "AFP·β-hCG — 고형 난소 종괴의 표지자?"
    point: "AFP·hCG 는 생식세포 종양(난황낭종·융모막암종 등)의 표지자이고 주로 젊은 여성에서 쓴다 [[harrison-21: 89장 p.698]]. 폐경 후 에스트로겐 징후가 있는 종괴에는 맞지 않는다."
  - contrast: "자궁내막 선암이 있으니 원발 자궁암만?"
    point: "폐경 후 에스트로겐 공급원이 없는데 자궁내막이 두껍고 선암이 있으면, 에스트로겐을 만드는 난소 종양이 함께 있는지 본다 — 성끈-간질 종양에는 자궁내막암이 동시에 생길 수 있다 [[harrison-21: 89장 p.697]] [[harrison-21: 89장 p.699]]."
tables:
  - id: ovarian-tumor-markers
    section: "가르는 소견 — 기원 세포가 표지자를 정한다"
    title: "난소 종양 — 기원 세포별 혈청 표지자"
    role: differential
    span: column
    columns: ["기원 세포", "대표 종양", "추적 표지자"]
    rows:
      - ["체강 상피", "고등급 장액성 암", "CA-125 [[harrison-21: 89장 p.696]]"]
      - ["성끈-간질(과립막세포)", "성인형 과립막세포종", "인히빈 B(·AMH) [[?novak-16]]"]
      - ["생식세포", "난황낭종·융모막암종", "AFP·β-hCG [[harrison-21: 89장 p.698]]"]
      - ["점액 상피·위장관 전이", "점액성 종양·Krukenberg", "CEA [[?novak-16]]"]
diagram:
  title: "난소 종괴 수술 뒤 — 어떤 표지자로 추적하나"
  nodes:
    - {id: start, kind: start, text: "난소 종괴 절제 — 재발 감시 표지자 선택"}
    - {id: histo, kind: decision, text: "조직의 기원 세포는?"}
    - {id: ask, kind: info, text: "호르몬 증상·자궁내막·나이·종괴 양상 확인"}
    - {id: gct, kind: step, text: "과립막세포종 — 에스트로겐·인히빈 분비"}
    - {id: inhibin, kind: end, text: "인히빈 B(·AMH)로 오래 추적"}
    - {id: ca125, kind: end, text: "상피성 암 → CA-125"}
    - {id: germ, kind: end, text: "생식세포 종양 → AFP·β-hCG"}
    - {id: cea, kind: end, text: "점액성·위장관 전이 → CEA"}
  edges:
    - {from: start, to: histo}
    - {from: histo, to: gct, label: "Call-Exner·핵 홈"}
    - {from: histo, to: ca125, label: "유두·사종체"}
    - {from: histo, to: germ, label: "생식세포"}
    - {from: histo, to: cea, label: "점액 상피"}
    - {from: histo, to: ask, label: "조직 미확정"}
    - {from: ask, to: gct, label: "에스트로겐 과다"}
    - {from: ask, to: ca125, label: "복수·양측 종괴"}
    - {from: gct, to: inhibin}
diagram_notes:
  - "에스트로겐 과다 징후 — 폐경 후 출혈, 자궁내막 증식·자궁내막모양 선암, 유방 압통, 아이의 성조숙증 [[harrison-21: 89장 p.697]]."
  - "과립막세포종은 수술 뒤 오랜 기간이 지나 재발할 수 있어 오래 추적한다 — 재발 시점 수치는 원문 미대조(검토 항목) [[?novak-16]]."
  - "가임기 여성에서는 정상 월경 주기에도 인히빈이 오르내린다 — 폐경 뒤에 해석이 가장 깨끗하다 [[?novak-16]]."
checks:
  - q: "폐경 후 출혈·자궁내막 선암과 고형 난소 종괴가 있고 조직에 Call-Exner 소체가 보인다. 재발 감시 표지자는?"
    a: "인히빈 B(와 AMH) — 과립막세포가 분비하는 물질이다."
  - q: "난소 종양 표지자를 고르는 원칙은?"
    a: "기원 세포 — 상피는 CA-125, 생식세포는 AFP·hCG, 성끈-간질(과립막세포)은 인히빈."
  - q: "과립막세포종이 폐경 후 출혈을 일으키는 이유는?"
    a: "종양이 에스트로겐을 만들어, 맞서는 프로게스테론 없이 자궁내막을 자극하기 때문(증식증·선암)."
variants:
  - id: v1
    of: imaging-2026-0412
    flip: true
    changed: "에스트로겐 징후(폐경 후 출혈·자궁내막 선암) 삭제, 복부 팽만·복수·양쪽 복합 종괴로, 조직을 Call-Exner 소체 → 유두 구조·사종체·심한 핵 이형성으로 → 답이 인히빈 B 에서 CA-125 로 바뀜"
    context: "단서를 바꿔 답이 바뀌는 변형 — 상피성 난소암"
    stem: "63세 여자가 2개월 전부터 배가 불러 오고 조금만 먹어도 배가 부르다며 병원에 왔다. 12년 전 폐경되었고 질 출혈은 없었다. 배가 팽만되어 있고 이동탁음이 있다. 질초음파에서 자궁내막 두께는 3 mm이고 양쪽 난소에 고형 부분이 섞인 복합 종괴가 있으며 복수가 많다. 수술로 떼어 낸 난소 종괴의 조직 절편(H&E 염색)에서 유두 모양 구조, 동심원 층의 석회화 소체, 핵 이형성이 심한 세포가 보인다. 수술과 항암치료 뒤 재발 감시에 가장 유용한 혈청 표지자는?"
    choices: ["A. 인히빈 B", "B. CA-125", "C. α-태아단백", "D. β-hCG", "E. 암배아항원"]
    answer: "B"
    explanation: "유두 구조·사종체·심한 핵 이형성은 체강 상피에서 나온 고등급 장액성 암이다. 복수·양쪽 종괴도 상피성 암의 복막 전파와 맞는다. 상피성 난소암은 CA-125 를 분비하고, 재발 때 CA-125 가 먼저 오른다. 원래 문항은 폐경 후 출혈·자궁내막 선암(에스트로겐 과다)과 Call-Exner 소체가 있는 과립막세포종이라 과립막세포가 분비하는 인히빈 B 가 답이었다."
    kind: application
  - id: v2
    of: imaging-2026-0412
    flip: false
    changed: "나이 65 → 57세, 내원 경위(반복 출혈 → 건강검진 초음파의 자궁내막 비후 뒤 점상 출혈), 왼쪽, 종괴 크기 9 → 6 cm, 자궁내막 생검을 선암 → 비정형 증식증으로 바꾸고 「폐경 후 에스트로겐 과다 + 고형 종괴 + Call-Exner 소체·핵 홈」은 그대로 → 답은 여전히 인히빈 B"
    context: "겉모습만 바꾸고 답은 같은 변형 — 건강검진에서 발견"
    stem: "57세 여자가 건강검진 초음파에서 자궁내막이 두껍다는 말을 듣고 병원에 왔다. 7년 전 폐경되었고 최근 한 달 동안 점상 질 출혈이 두 번 있었다. 호르몬제나 건강보조식품을 먹은 적이 없다. 질초음파에서 자궁내막 두께는 12 mm이고 왼쪽 난소에 6 cm 고형 종괴가 있다. 자궁내막 생검에서 비정형 자궁내막 증식증이 나왔다. 수술로 떼어 낸 난소 종괴의 조직 절편(H&E 염색)에서 작고 균일한 세포가 판상으로 자라고, 호산성 물질을 둘러싼 작은 소포 모양 배열과 세로로 홈이 팬 핵이 보인다. 수술 뒤 재발 감시에 가장 유용한 혈청 표지자는?"
    choices: ["A. CA-125", "B. 암배아항원", "C. 인히빈 B", "D. α-태아단백", "E. β-hCG"]
    answer: "C"
    explanation: "나이·발견 경위·종괴 쪽과 크기·자궁내막 병변의 단계가 바뀌었지만, 외인성 에스트로겐 없이 폐경 후 자궁내막이 자극되고 고형 난소 종괴의 조직에 Call-Exner 소체와 핵 홈이 있다는 결정적 단서는 그대로다 — 성인형 과립막세포종이다. 과립막세포가 분비하는 인히빈 B 로 재발을 감시한다. CA-125 는 상피성 암, AFP·β-hCG 는 생식세포 종양의 표지자다."
    kind: application
sources:
  - id: harrison-21
    org: "McGraw Hill"
    title: "Harrison's Principles of Internal Medicine, 21st ed. — Chapter 89: Gynecologic Malignancies"
    kind: textbook
    year: 2022
    citation: "Loscalzo J, Fauci AS, Kasper DL, et al (eds). Harrison's Principles of Internal Medicine, 21e. 89장 Gynecologic Malignancies(Spriggs D), 인쇄쪽 695–700"
    checked_at: 2026-10-23
    checked: "드라이브 장 문서로 본문 대조. p.695 난소 세포군(상피·간질·생식세포)과 종양 분류, 상피성이 가장 흔함, Krukenberg. p.696 CA-125 = MUC16, 난소암과 연관되나 특이하지 않음. p.697 재발의 첫 신호로 CA-125 상승(상피성); 간질 종양은 난소 종양의 약 7 %, 50–60대, 한쪽 고형 종괴, 드물게 에스트로겐을 만들어 폐경 후 출혈·자궁내막암 동시 발생, Sertoli-Leydig = 안드로겐, 섬유종 = Meigs, 치료는 수술. p.698 생식세포 종양은 hCG·AFP. p.699 에스트로겐 분비 종양은 자궁내막암 위험인자. 해리슨에 없는 것: 인히빈·AMH 표지자, Call-Exner 소체·핵 홈 조직 소견, FOXL2, 늦은 재발"
    verified: text
  - id: novak-16
    org: "Wolters Kluwer"
    title: "Berek & Novak's Gynecology, 16th ed. — Ovarian, Fallopian Tube, and Peritoneal Cancer (sex cord-stromal tumors)"
    kind: textbook
    year: 2019
    citation: "Berek JS (ed). Berek & Novak's Gynecology, 16e. ch. Ovarian, Fallopian Tube, and Peritoneal Cancer — sex cord-stromal tumors"
    checked_at: 2026-10-23
    checked: "서지만(문항 imaging-2026-0412 해설 근거 목록에서 옮김, 원문 미대조 — 검토 항목). 인히빈·AMH 표지자, 늦은 재발과 장기 추적, CEA 의 쓰임에 쓴다"
    verified: citation
  - id: who-5-female
    org: "IARC"
    title: "WHO Classification of Tumours, 5th ed. — Female Genital Tumours: sex cord-stromal tumours (adult granulosa cell tumour)"
    kind: textbook
    year: 2020
    citation: "WHO Classification of Tumours Editorial Board. Female Genital Tumours, 5e. Sex cord-stromal tumours — adult granulosa cell tumour"
    checked_at: 2026-10-23
    checked: "서지만(문항 해설 근거 목록에서 옮김, 원문 미대조 — 검토 항목). Call-Exner 소체·핵 홈·FOXL2 조직·분자 소견 서술에 쓴다"
    verified: citation
  - id: cureus-2022-gct
    org: "Cureus (증례 보고, PMC Open Access)"
    title: "A Rare Case of Granulosa Cell Tumor Associated With Endometrial Carcinoma - A Case Report"
    kind: other
    year: 2022
    citation: "Cureus 2022;14(11):e31122"
    doi: "10.7759/cureus.31122"
    url: "https://pmc.ncbi.nlm.nih.gov/articles/PMC9721141/"
    checked_at: 2026-10-23
    checked: "그림 8(H&E — Call-Exner 소체·핵 홈 화살표)과 그 설명만 확인(문항 imaging-2026-0412·exam-builder 풀 기록). 본문은 열지 않았다"
    verified: citation
figures:
- id: f1
  file: docs/assets/figures/pmc-pmc9721141_figure8.jpg
  kind: histology
  at: 기전 — 과립막세포에서 에스트로겐 징후로
  shows: 난소 과립막세포종 H&E(40배) — Call-Exner 소체와 핵 홈
  look_for:
  - 검은 화살표 — Call-Exner 소체 자리
  - 주황 화살표 — 세로 홈이 팬 핵
  - 작고 균일한 세포가 빽빽한 판상 배열
  label: 「Histopathological cut section of granulosa cell tumor of ovary (Hematoxyline and Eosin stained, 40X), black arrows shows call exner body and orange arrow shows nuclear groove」 — A Rare Case of Granulosa Cell Tumor Associated With Endometrial Carcinoma - A Case Report
  label_basis: published_figure
  reference: 동료 심사 논문의 그림 설명(저자가 그 소견이라고 쓴 그림)
  paper: A Rare Case of Granulosa Cell Tumor Associated With Endometrial Carcinoma - A Case Report
  doi: 10.7759/cureus.31122
  credit: 'A Rare Case of Granulosa Cell Tumor Associated With Endometrial Carcinoma - A Case Report. Cureus. 2022 Nov 5;14(11):e31122. doi: 10.7759/cureus.31122 (CC BY) — Figure 8'
  license: CC BY
  url: https://pmc.ncbi.nlm.nih.gov/articles/PMC9721141/
  asset: PMC-PMC9721141_Figure8
  from_question: imaging-2026-0412
---

## 판단 — 왜 인히빈 B가 먼저인가
- 먼저 종양의 기원 세포를 정한다: 폐경 후 **에스트로겐 과다**(출혈·자궁내막 증식·선암) + **한쪽 고형 난소 종괴**는 호르몬을 만드는 성끈-간질 종양을 떠올리게 한다 [[harrison-21: 89장 p.697]].
- 조직의 Call-Exner 소체와 세로 홈이 팬 「커피콩」 핵이 성인형 과립막세포종을 정한다 [[?who-5-female]].
- 혈청 표지자는 그 세포가 만드는 물질이다 — 과립막세포는 인히빈과 항뮐러관호르몬(anti-Müllerian hormone, AMH)을 분비하므로 수술 뒤 재발 감시는 인히빈 B 로 한다 [[?novak-16]].
- CA-125 는 상피성 난소암의 표지자다 — 「난소 종양 = CA-125」 로 고르면 틀린다 [[harrison-21: 89장 p.696]].

## 기전 — 과립막세포에서 에스트로겐 징후로
정상 난포에서 과립막세포는 난포막세포가 만든 안드로겐을 아로마타제(aromatase)로 에스트라디올로 바꾸고, FSH 를 억제하는 인히빈과 AMH 를 분비한다. 종양이 된 과립막세포도 이 기능을 가진다 [[?novak-16]]. 폐경 뒤에는 에스트로겐 공급원이 거의 없는데 종양이 에스트로겐을 계속 만들면, 맞서는 프로게스테론 없이 자궁내막이 자극되어 증식증·자궁내막모양 선암이 생기고 출혈이 난다 [[harrison-21: 89장 p.699]]. 그래서 이 종양은 폐경 후 출혈로, 아이에서는 성조숙증으로 드러난다 [[harrison-21: 89장 p.697]]. 조직에서는 작고 균일한 세포가 판상·소주상으로 자라고, 호산성 기저막 물질을 둘러싼 소포 모양 배열(Call-Exner 소체)과 세로 홈이 팬 핵이 보인다 [[?who-5-female]].

## 가르는 소견 — 기원 세포가 표지자를 정한다
- 상피·생식세포·성끈-간질 중 어디서 나왔는지가 표지자를 정한다(표) [[harrison-21: 89장 p.695]].
- CA-125(MUC16)는 상피성 난소암과 연관되지만 특이하지 않다 — 자궁내막증·골반염·복수에서도 오른다 [[harrison-21: 89장 p.696]]. 과립막세포종에서는 감시 도구로 쓸모가 적다.
- 가임기 여성은 정상 주기에도 인히빈이 오르내려, 표지자 해석은 폐경 뒤에 가장 깨끗하다 [[?novak-16]].

## 권고와 예외
- 성끈-간질 종양의 치료는 대부분 수술이고, 보조 항암치료 없이 절제한다 — 항암치료(카보플라틴·파클리탁셀)는 절제 불가·여러 번 재발한 종양에 남겨 둔다 [[harrison-21: 89장 p.697]] [[harrison-21: 89장 p.698]].
- 에스트로겐을 만드는 종양에는 자궁내막암·유방암이 동시에 있을 수 있어 함께 평가한다 [[harrison-21: 89장 p.697]].
- 과립막세포종은 수술 뒤 오래 지나 재발할 수 있어 장기 추적한다 — 재발 시점 수치는 원문 미대조(검토 항목) [[?novak-16]].

## 시험 쟁점 — 충돌·맥락·새 근거
- **Z1 맥락 · 간질 종양은 에스트로겐을 만드는가** — 시험 기준: 과립막세포종(성인형)은 에스트로겐을 만드는 대표 난소 종양이다 [[?novak-16]] / 다른 기준: 「대부분의 간질 종양은 에스트로겐을 만들지 않고, 드물게 만들어 폐경 후 출혈·자궁내막암을 일으킨다」 [[harrison-21: 89장 p.695]] [[harrison-21: 89장 p.697]] / 왜 다른가: 해리슨은 섬유종·Sertoli-Leydig 를 포함한 간질 종양 전체를 말하고, 시험은 그중 과립막세포종 하나를 묻는다 / 시험에서는: KMLE · USMLE 모두 「폐경 후 출혈 + 자궁내막 증식·암 + 고형 난소 종괴」 = 과립막세포종, 표지자 인히빈.
- **Z2 새 근거 · 표지자 출처** — 시험 기준: 인히빈 B(·AMH) [[?novak-16]] / 다른 기준: 해리슨 89장은 간질 종양의 표지자를 언급하지 않는다(대조: 89장 p.697) / 왜 다른가: 내과 교과서는 부인종양 세부를 다루지 않는다 / 시험에서는: KMLE · USMLE 모두 인히빈. 원문 대조가 남은 검토 항목이다.
