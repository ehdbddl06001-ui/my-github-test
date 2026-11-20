---
id: cn.obgyn.aneuploidy-screening.positive-screen-diagnostic-test
type: concept
topic: Obstetrics & Gynecology
see_also: [Genetics]
date: 2026-11-20
updated: 2026-11-20
version: 1
outline: ob.prenatal-dx   # 기본틀 슬롯(content/outline/subjects.yaml) — 산부인과 손 슬롯 「산전 진단과 태아 안녕 평가」
confidence: medium
review_status: unreviewed
note_form: 2            # 판형 2(2026-09-25) — 기본틀 [gap] 으로 쓴 정리본(오답 연결 없음)
title: "이수성 선별 양성 — 확진은 주수에 맞는 침습 검사로"
objective: "염색체 이수성 선별검사(cfDNA·혈청 선별)가 고위험으로 나온 임신부에게, 선별과 진단을 구분하고 임신 주수와 태반 모자이크 가능성에 맞춰 융모막융모생검과 양수천자 중 확진검사를 고른다"
objective_kind: 검사 선택
condition: 태아 염색체 이수성 선별검사 고위험(positive aneuploidy screen)
exams: [kmle, usmle]
summary:
  - "결론: 선별 고위험은 진단이 아니다 — 14주 전이면 융모막융모생검, 14주 이후면 양수천자로 확진한다."
  - "시험 단서: cfDNA(NIPT)·쿼드·통합검사 「고위험」 + 「다음 처치는?」 → 침습 진단검사(diagnostic testing)."
  - "왜: cfDNA는 태반에서 온 DNA라 위양성이 있고, 혈청 선별은 위험도 계산일 뿐 태아 핵형을 보지 않는다."
  - "양수천자는 14주 전에 하지 않는다(유산·내반족↑), 융모막융모생검은 9주 전에 하지 않는다(유산·사지 결손↑)."
  - "CVS가 모자이크면 태반 국한 모자이크일 수 있어 양수천자로 태아 핵형을 다시 본다."
pitfalls:
  - contrast: "cfDNA 고위험 = 다운증후군 확진?"
    point: "cfDNA 는 선별검사다. 큰 코호트에서 trisomy 21 양성예측도도 90.9 % 였다 — 침습 검사 없이 결론 내리거나 임신 종결 같은 되돌릴 수 없는 처치를 하지 않는다 [[ksmfm-screening-2021: cfDNA KQ7]]."
  - contrast: "cfDNA 저위험 = 염색체 정상?"
    point: "흔한 세 삼염색체(21·18·13)의 위험이 낮다는 뜻일 뿐이다. 침습 검사로 찾은 이상의 16.9 % 는 지금의 cfDNA 로 잡을 수 없는 종류였다 [[ksmfm-screening-2021: cfDNA KQ3·KQ4]]."
  - contrast: "1삼분기 확진 — 이른 양수천자?"
    point: "14주 전 양수천자는 중기 양수천자보다 태아 소실(7.6 % vs 5.9 %)·내반족·양수 누출이 많다. 1삼분기에는 9주 이후 융모막융모생검을 고른다 [[ksmfm-invasive-2021: KQ2·KQ8]]."
  - contrast: "CVS 모자이크 = 태아 모자이크?"
    point: "CVS 모자이크(약 1.3 %)는 대개 태반 세포영양막에 국한되고, 뒤이은 양수천자의 약 90 % 가 정상이었다 — 양수천자로 태아 핵형을 확인한다 [[ksmfm-invasive-2021: KQ3]]."
  - contrast: "혈청 선별 고위험 → 다른 혈청 선별로 재확인?"
    point: "고위험 뒤 혈청 선별을 다시 하는 것은 권하지 않는다. 진단을 원하면 침습 검사, 침습을 피하고 싶으면 cfDNA 를 상담한다 [[ksmfm-screening-2021: 혈청 KQ5]]."
tables:
  - id: screen-performance
    title: "선별검사 — 시기와 성능(단태 임신)"
    role: tests
    span: column
    section: "가르는 소견 — 선별 결과의 무게"
    columns: ["검사", "시기", "대상", "성능"]
    rows:
      - ["cfDNA(NIPT)", "10주 이후 [[ksmfm-screening-2021: cfDNA KQ5]]", "삼염색체 21·18·13, 성염색체 이수성 [[ksmfm-screening-2021: cfDNA KQ2]]", "T21 민감도 99.3 %·특이도 99.8 %, T13·monosomy X 민감도 91 % [[ksmfm-screening-2021: cfDNA KQ2]]"]
      - ["1삼분기 선별(PAPP-A·free β-hCG + NT)", "11–13주 [[ksmfm-screening-2021: 혈청 KQ1]]", "다운증후군 등", "검출률 80–84 %(위양성 5 %), 양성예측도 3–4 % [[ksmfm-screening-2021: 혈청 KQ1]]"]
      - ["쿼드 선별(AFP·hCG·uE3·inhibin A)", "2삼분기(통합검사에서 15–21주) [[ksmfm-screening-2021: 혈청 KQ1]]", "다운증후군·삼염색체 18", "검출률 81 %(위양성 5 %) [[ksmfm-screening-2021: 혈청 KQ1]]"]
      - ["통합검사(NT·PAPP-A + 쿼드)", "11–13주 + 15–21주 [[ksmfm-screening-2021: 혈청 KQ1]]", "다운증후군 등", "검출률 94–96 %(위양성 5 %), 양성예측도 5 % [[ksmfm-screening-2021: 혈청 KQ1]]"]
    note: "혈청 선별의 고위험 기준은 1:270(35세 여성의 다운증후군 위험) [[ksmfm-screening-2021: 혈청 KQ1]]."
  - id: invasive-choice
    title: "확진검사 — 융모막융모생검 vs 양수천자"
    role: comparison
    span: column
    section: "선택 — 주수와 검체가 검사를 정한다"
    columns: ["항목", "융모막융모생검(CVS)", "양수천자(amniocentesis)"]
    rows:
      - ["시기", "9주 이후 ~ 14주 전 [[ksmfm-invasive-2021: KQ2·KQ9]] [[ksmfm-screening-2021: 혈청 KQ5]]", "14주 이후(중기 양수천자) [[ksmfm-invasive-2021: KQ8]] [[ksmfm-screening-2021: 혈청 KQ5]]"]
      - ["검체", "융모(태반)", "양수(태아 세포)"]
      - ["정확도·한계", "검출 98–99 %, 모자이크 <1 %, 모체 세포 오염 <1 % [[ksmfm-screening-2021: 혈청 KQ5]]", "정확도 99.8–99.9 % [[ksmfm-screening-2021: 혈청 KQ5]]"]
      - ["너무 이르면", "9주 전: 유산·사지 결손·얼굴 기형↑ [[ksmfm-invasive-2021: KQ9]]", "14주 전: 유산·내반족·양수 누출↑ [[ksmfm-invasive-2021: KQ8]]"]
diagram:
  title: "이수성 선별 고위험 — 확진검사 고르기"
  nodes:
    - {id: start, kind: start, text: "cfDNA·혈청 선별 결과 고위험"}
    - {id: couns, kind: step, text: "상담 — 선별일 뿐, 확진 전 비가역 처치 ✗"}
    - {id: cpm, kind: decision, text: "태반 국한 모자이크가 의심되나?"}
    - {id: ga, kind: decision, text: "지금 임신 주수는?"}
    - {id: early, kind: info, text: "9주 전 — 주수 재확인, 9주 이후로 미룸"}
    - {id: cvs, kind: step, text: "융모막융모생검(CVS)"}
    - {id: mos, kind: decision, text: "CVS 결과가 모자이크인가?"}
    - {id: cvsdx, kind: end, text: "CVS 핵형으로 확진"}
    - {id: amnio, kind: end, text: "14주 이후 양수천자로 태아 핵형 확진"}
  edges:
    - {from: start, to: couns}
    - {from: couns, to: cpm}
    - {from: cpm, to: ga, label: "아님"}
    - {from: cpm, to: amnio, label: "의심"}
    - {from: ga, to: early, label: "9주 전"}
    - {from: ga, to: cvs, label: "9–13주"}
    - {from: ga, to: amnio, label: "14주 이후"}
    - {from: early, to: cvs, label: "9–13주"}
    - {from: early, to: amnio, label: "14주 이후"}
    - {from: cvs, to: mos}
    - {from: mos, to: cvsdx, label: "아님"}
    - {from: mos, to: amnio, label: "모자이크"}
diagram_notes:
  - "태반 국한 모자이크를 의심할 때 — cfDNA 결과와 초음파 등 다른 소견이 어긋나거나, 희귀 상염색체 이수성처럼 양성예측도가 낮은 결과. 이때는 양수천자가 태아 핵형을 더 직접 본다. 그 밖의 대다수 cfDNA 고위험은 CVS 로 충분하다 [[poulton-hui-2025: Confined placental mosaicism]]."
  - "cfDNA 「결과 없음(no call)」은 태아 이수성(특히 18·13) 가능성이 높아지는 신호다 — 재검 대신 침습 검사를 권하는 지침과, 재검·다른 선별도 선택지로 두는 자료가 갈린다(시험 쟁점 Z2) [[ksmfm-screening-2021: cfDNA KQ3]] [[poulton-hui-2025: Test failures]]."
  - "초음파에서 구조 이상·NT ≥3 mm·낭성 림프관종이 보이면 선별을 거치지 않고 침습 검사와 정밀 초음파로 간다 [[ksmfm-screening-2021: 혈청 KQ8]]."
  - "Rh 음성 임신부는 침습 검사 뒤 72시간 안에 항D 면역글로불린을 준다. 예방적 항생제는 권하지 않는다 [[ksmfm-invasive-2021: KQ4·KQ6]]."
checks:
  - q: "임신 11주, cfDNA 에서 trisomy 21 고위험. 다음 검사는?"
    a: "융모막융모생검으로 확진한다. cfDNA 는 선별이라 확진 전에 결론 내리지 않고, 14주 전 양수천자는 유산·내반족이 늘어 고르지 않는다."
  - q: "CVS 에서 trisomy 모자이크가 나왔다. 왜 양수천자를 하나?"
    a: "CVS 는 태반(세포영양막)을 보므로 태반 국한 모자이크일 수 있다 — 양수천자로 태아 자신의 핵형을 확인한다. CVS 모자이크의 약 90 % 는 양수천자가 정상이었다."
  - q: "cfDNA 가 태반 국한 모자이크에 흔들리는 이유는?"
    a: "모체 혈액의 태아 cfDNA 는 태반에서 나온다. 태반과 태아의 핵형이 다르면 cfDNA 결과가 태아 핵형과 어긋난다."
sources:
  - id: ksmfm-screening-2021
    org: "Korean Society of Maternal-Fetal Medicine (Choe SA, Seol HJ, Kwon JY, et al)"
    title: "Clinical Practice Guidelines for Prenatal Aneuploidy Screening and Diagnostic Testing from Korean Society of Maternal-Fetal Medicine: (1) Prenatal Aneuploidy Screening"
    kind: guideline
    year: 2021
    citation: "J Korean Med Sci 2021;36(4):e27"
    doi: "10.3346/jkms.2021.36.e27"
    pmid: "33496086"
    url: "https://pmc.ncbi.nlm.nih.gov/articles/PMC7834900/"
    checked_at: 2026-11-20
    checked: "PMC 전문 대조(PMC7834900). 혈청 KQ1 — 고위험 기준 1:270, 1삼분기 선별(PAPP-A·free β-hCG·NT, 11–13주) 검출률 80–84 %·위양성 5 %·양성예측도 3–4 %, 트리플 69 %, 쿼드 81 %, 통합검사(11–13주 + 15–21주) 94–96 %·양성예측도 5 %, 양수천자(15–22주) 소실 0.13 %·1삼분기 CVS 약 1.2 %. 혈청 KQ4 — 저위험 뒤 독립 재선별 ✗(위양성↑). 혈청 KQ5 — 고위험은 확진 아님, 침습 검사 먼저 권고, CVS 14주 전·양수천자 14주 후, CVS 검출 98–99 %·모자이크 <1 %·모체 오염 <1 %·시술 소실 0.5–1.2 %, 양수천자 정확도 99.8–99.9 %·최근 소실 0.06–0.13 %, 1삼분기 양수천자 ✗(누출·내반족), 혈청 재검 ✗, cfDNA 는 대안이나 진단 아님(진짜 양성이면 진단 지연). 혈청 KQ8 — NT ≥3 mm·낭성 림프관종이면 선별 없이 침습 검사. cfDNA KQ1 — 모두에게 정보 제공 가능, 우선은 고위험군. KQ2 — T21 민감도 99.3 %·특이도 99.8 %, T18 97.4 %·99.8 %, T13·monosomy X 91 %·>99 %, 위양성에 태반 모자이크·소실 쌍태·모체 CNV·모체 악성종양, 미세결실 ✗. KQ3 — 저위험 ≠ 정상, no call 은 재검 대신 침습 검사(이수성 가능성↑, 재검 성공 45–90 %), 비만에서 no call 흔함. KQ4 — 저위험군 전원 1차로는 비용효과 ✗, 침습 검사로 찾은 이상의 16.9 % 는 cfDNA 로 못 찾음. KQ5 — 10주 이후. KQ6 — 다태 ✗. KQ7 — 고위험이면 침습 검사 제안, 확진 전 비가역 처치 ✗, PPV 전체 삼염색체 82.9 %·T21 90.9 %. 서론 — 태아 cfDNA 는 태반 기원"
    verified: text
  - id: ksmfm-invasive-2021
    org: "Korean Society of Maternal-Fetal Medicine"
    title: "Clinical Practice Guidelines for Prenatal Aneuploidy Screening and Diagnostic Testing from Korean Society of Maternal-Fetal Medicine: (2) Invasive Diagnostic Testing for Fetal Chromosomal Abnormalities"
    kind: guideline
    year: 2021
    citation: "J Korean Med Sci 2021;36(4):e26"
    doi: "10.3346/jkms.2021.36.e26"
    pmid: "33496085"
    url: "https://pmc.ncbi.nlm.nih.gov/articles/PMC7834898/"
    checked_at: 2026-11-20
    checked: "PMC 전문 대조(PMC7834898). KQ1 — 35세 이상 전원 침습 검사 ✗. KQ2 — 1삼분기 진단은 CVS(14주 전 양수천자는 소실·기형↑), CVS 는 9주 이후(Level 1+, A), WHO 자료: 10주 이후 CVS 는 소실·기형을 늘리지 않음, 조기 양수천자 소실 7.6 % vs 중기 5.9 %·내반족·막 파열↑. KQ3 — 진짜 태아 모자이크와 태반 국한 모자이크 구별에 양수천자, CVS 모자이크 1.3 %(세포영양막 국한)·뒤이은 양수천자 약 90 % 정상, 태반 국한 모자이크는 태아 성장 제한 등과 관련, 6·7·11·14·15번 염색체는 UPD 검사 고려. KQ4 — Rh 음성은 72시간 안 항D 면역글로불린. KQ6 — 예방 항생제 ✗. KQ7 — CMA 를 모든 침습 검사의 대체로 ✗, 구조 이상 태아에는 이점. KQ8 — 14주 전 양수천자 ✗(Level 1++, A). KQ9 — 9주 전 CVS ✗(유산·사지 결손·얼굴 기형, 6–7주 CVS 소실 7.2 % vs 2.5 %). KQ10 — 쌍태에서 소실 위험 더 큼. 이 문서의 「검사 뒤 2주 안 소실 약 3 %」·메타분석 3.07 %/3.84 % 는 시술 기여분이 아닌 전체 소실률이다"
    verified: text
  - id: poulton-hui-2025
    org: "Poulton A, Hui L (종설)"
    title: "Noninvasive prenatal testing: an overview"
    kind: review
    year: 2025
    citation: "Aust Prescr 2025;48(2):47-53"
    doi: "10.18773/austprescr.2025.019"
    pmid: "40343140"
    url: "https://pmc.ncbi.nlm.nih.gov/articles/PMC12055489/"
    checked_at: 2026-11-20
    checked: "PMC 전문 대조(PMC12055489). 「What does the NIPT result mean?」 — 선별이지 진단 아님, 고위험이면 유전 상담과 CVS·양수천자 확진을 강하게 권고. 「Confined placental mosaicism」 — 임신의 약 1 %, cfDNA 는 태반 기원이라 태아 핵형과 어긋날 수 있음, 의심되면(NIPT 와 초음파 등 불일치) 양수천자가 더 직접적, 대다수 고위험에는 CVS 가 적절. 「Test failures」 — no call 은 낮은 태아 분획이 흔한 원인이고 이수성과 관련, 선택지는 재검(성공 약 60 %)·침습 검사·CFTS. 「Multiple gestations」 — 쌍태에서도 단태와 비슷한 성능, 권장 방법. Table 1 — NIPT 10주 이후. 호주(RANZCOG) 맥락"
    verified: text
  - id: acmg-nips-2022
    org: "American College of Medical Genetics and Genomics (Dungan JS, Klugman S, et al)"
    title: "Noninvasive prenatal screening (NIPS) for fetal chromosome abnormalities in a general-risk population: an evidence-based clinical guideline of the ACMG"
    kind: guideline
    year: 2023
    citation: "Genet Med 2023;25(2):100336 (온라인 2022-12-16)"
    doi: "10.1016/j.gim.2022.11.004"
    pmid: "36524989"
    url: "https://doi.org/10.1016/j.gim.2022.11.004"
    checked_at: 2026-11-20
    checked: "PubMed 초록만(PMC 전문 없음). ACMG 는 모든 단태·쌍태 임신부에게 trisomy 21·18·13 선별로 기존 선별보다 NIPS 를 강하게 권고, 성염색체 이수성 선별도 제안하도록 강하게 권고"
    verified: abstract
  - id: cherry-acmg-2017
    org: "American College of Medical Genetics and Genomics (Cherry AM, Akkari YM, et al)"
    title: "Diagnostic cytogenetic testing following positive noninvasive prenatal screening results: a clinical laboratory practice resource of the ACMG"
    kind: guideline
    year: 2017
    citation: "Genet Med 2017;19(8):845-850"
    doi: "10.1038/gim.2017.91"
    pmid: "28726804"
    url: "https://doi.org/10.1038/gim.2017.91"
    checked_at: 2026-11-20
    checked: "PubMed 초록만. NIPS 는 선별검사이므로 모든 선별 양성은 진단검사로 확인할 것을 권고, 알고리즘은 CVS 또는 양수천자 검체로 염색체 분석·FISH·CMA"
    verified: abstract
  - id: salomon-2019
    org: "Salomon LJ, Sotiriadis A, Wulff CB, Odibo A, Akolekar R (체계적 문헌고찰·메타분석)"
    title: "Risk of miscarriage following amniocentesis or chorionic villus sampling: systematic review of literature and updated meta-analysis"
    kind: review
    year: 2019
    citation: "Ultrasound Obstet Gynecol 2019;54(4):442-451"
    doi: "10.1002/uog.20353"
    pmid: "31124209"
    url: "https://doi.org/10.1002/uog.20353"
    checked_at: 2026-11-20
    checked: "PubMed 초록만(PMC 전문 없음). 24주 전 소실 — 양수천자 0.91 % vs 대조 0.58 %, 시술 관련 위험 0.30 %(95 % CI 0.11–0.49), CVS 1.39 % vs 1.23 %, 시술 관련 0.20 %(−0.13–0.52). 위험도가 비슷한 대조군만 보면 양수천자 0.12 %, CVS −0.11 % — 지금 설명하는 수치보다 낮다"
    verified: abstract
figures_none: 검사 선택 목표 — 선별 결과·임신 주수·CVS 핵형으로 가르고 영상 소견이 시험 단서가 아니다
---

## 판단 — 왜 고위험 결과 다음은 진단검사인가
- 선별검사는 **위험도**를 낸다. 혈청 선별은 나이에 따른 위험에 혈청 결과의 우도비를 곱한 값이고, 고위험(기준 1:270)이라도 태아 이상을 확정하지 않는다 [[ksmfm-screening-2021: 혈청 KQ1·KQ5]].
- cfDNA 도 선별이다. 위양성·위음성이 있어 고위험이면 침습 검사를 제안하고, 확진 전에는 되돌릴 수 없는 산과 처치를 하지 않는다 [[ksmfm-screening-2021: cfDNA KQ7]] [[cherry-acmg-2017]].
- 핵형을 직접 보는 것은 침습 검사(융모막융모생검·양수천자)뿐이다 — 모든 염색체의 수·구조 이상을 보지만 유산 위험이 따른다 [[ksmfm-screening-2021: 혈청 KQ1]].
- 침습 검사를 피하려는 임신부에게 혈청 고위험 뒤 cfDNA 는 합리적 대안이지만, 진짜 양성이면 결국 침습 검사가 필요해 진단이 늦어진다는 점을 알린다 [[ksmfm-screening-2021: 혈청 KQ5]].

## 기전 — cfDNA는 태반을 본다
모체 혈장의 태아 cfDNA 는 **태반에서 나온** 조각이다. 태아가 다운증후군이면 21번 염색체 조각이 조금 더 많아지고, 이 차이로 위험을 계산한다 [[ksmfm-screening-2021: 서론]]. 그래서 태반과 태아의 핵형이 다르면(태반 국한 모자이크, 임신의 약 1 %) 태아가 정상이어도 고위험이 나온다 [[poulton-hui-2025: Confined placental mosaicism]]. 소실된 쌍태아·모체 복제수 변이·모체 악성종양도 결과를 흔든다 [[ksmfm-screening-2021: cfDNA KQ2]]. 융모막융모생검도 같은 태반 조직(세포영양막)을 보므로 모자이크가 나오면 태아 자신의 세포가 있는 양수로 다시 확인한다 [[ksmfm-invasive-2021: KQ3]].

## 가르는 소견 — 선별 결과의 무게
- 표처럼 cfDNA 의 민감도·특이도가 가장 높다. 그래도 양성예측도는 대상의 사전 위험에 따라 달라 저위험군에서 낮다 [[ksmfm-screening-2021: cfDNA KQ1·KQ4]].
- 음성 결과의 한계: 혈청 저위험은 「잡을 수 있는 이수성의 위험이 낮다」는 뜻이고, cfDNA 저위험도 모든 염색체 이상을 배제하지 않는다 [[ksmfm-screening-2021: 혈청 KQ1]] [[ksmfm-screening-2021: cfDNA KQ3]].
- 성염색체 이수성·희귀 상염색체 이수성은 양성예측도가 낮다(monosomy X 48.4 %) — 태반 모자이크가 한 원인이다 [[ksmfm-screening-2021: cfDNA KQ2]] [[poulton-hui-2025: Sex chromosome aneuploidies]].

## 선택 — 주수와 검체가 검사를 정한다
- 14주 전 → 융모막융모생검, 14주 이후 → 양수천자 [[ksmfm-screening-2021: 혈청 KQ5]].
- 너무 이른 시술이 문제다: 9주 전 CVS 는 유산·사지 결손이, 14주 전 양수천자는 유산·내반족·양수 누출이 늘었다 [[ksmfm-invasive-2021: KQ8·KQ9]].
- 태반 국한 모자이크가 의심되면(cfDNA 와 초음파가 어긋남 등) 양수천자가 태아 핵형을 더 직접 본다. 대다수 cfDNA 고위험에는 CVS 가 적절하다 [[poulton-hui-2025: Confined placental mosaicism]].
- 모자이크가 6·7·11·14·15번 염색체의 삼염색체면 양수천자 때 단친 이염색체(UPD) 검사를 고려한다 [[ksmfm-invasive-2021: KQ3]].

## 권고와 예외
- 나이(35세 이상)만으로 침습 검사를 권하지 않는다 — 먼저 선별로 위험을 평가한다 [[ksmfm-invasive-2021: KQ1]].
- 구조 이상·NT ≥3 mm·낭성 림프관종이면 선별 없이 침습 검사와 정밀 초음파로 간다 [[ksmfm-screening-2021: 혈청 KQ8]].
- 쌍태에서는 침습 검사의 소실 위험이 단태보다 높다 [[ksmfm-invasive-2021: KQ10]].
- 염색체 마이크로어레이를 모든 침습 검사에서 핵형 분석 대신 쓰지는 않는다(구조 이상 태아에서 이점) [[ksmfm-invasive-2021: KQ7]].

## 시험 쟁점 — 충돌·맥락·새 근거
- **Z1 맥락 · cfDNA를 모든 임신부의 1차 선별로?** — 시험 기준: 확진은 어느 경우든 침습 검사(이 정리본의 판단은 여기에 달려 있지 않다) / 다른 기준: 한국 지침(2019 승인)은 비용효과 때문에 모든 임신부 1차로는 권하지 않고 다태에는 권하지 않는다 [[ksmfm-screening-2021: cfDNA KQ4·KQ6]]. ACMG 2022 는 모든 단태·쌍태에게 기존 선별보다 NIPS 를 강하게 권고한다 [[acmg-nips-2022]]. 호주 종설도 쌍태 성능이 단태와 비슷하다고 적는다 [[poulton-hui-2025: Multiple gestations]] / 왜 다른가: 나라별 보험·비용 맥락과 지침 시점(2019 vs 2022) / 시험에서는: KMLE — 국내 지침 문구(고위험군 우선, 다태 ✗)가 나올 수 있다 · USMLE — cfDNA 를 모든 임신부에게 제안할 수 있는 선별로 본다.
- **Z2 충돌 · cfDNA 「결과 없음(no call)」 다음** — 시험 기준: 이수성 가능성이 높아지는 신호로 보고 침습 검사를 제안한다 [[ksmfm-screening-2021: cfDNA KQ3]] / 다른 기준: 재검(성공 약 60 %)·침습 검사·다른 선별을 상담으로 고르게 한다 [[poulton-hui-2025: Test failures]] / 왜 다른가: 한국 지침은 재검 성공률이 낮고 기다리는 동안의 불안을 이유로 재검을 권하지 않는다 / 시험에서는: KMLE · USMLE 모두 「침습 검사 제안」이 가장 안전한 답이다 — 「재검만」은 피한다.
- **Z3 충돌 · 시술 관련 유산 위험의 숫자** — 시험 기준: 수치보다 「CVS·양수천자 모두 작은 유산 위험이 있다」를 쓴다 / 다른 기준: 한국 지침은 양수천자 0.06–0.13 %, CVS 0.5–1.2 % 를 적는다 [[ksmfm-screening-2021: 혈청 KQ5]]. 메타분석은 시술 관련 위험을 양수천자 0.30 %, CVS 0.20 % 로, 위험도가 비슷한 대조군만 보면 둘 다 거의 0 으로 낸다 [[salomon-2019]] / 왜 다른가: 대조군 선택(위험도 맞춤 여부)과 「전체 소실」 vs 「시술 기여분」의 차이 — 한국 지침 (2)의 약 3 % 는 전체 소실률이다 [[ksmfm-invasive-2021: KQ10]] / 시험에서는: 특정 숫자를 정답 근거로 삼는 보기는 출처를 확인한다.
