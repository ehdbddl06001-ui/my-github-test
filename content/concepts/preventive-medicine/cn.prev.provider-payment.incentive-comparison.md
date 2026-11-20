---
id: cn.prev.provider-payment.incentive-comparison
type: concept
topic: Preventive Medicine
date: 2026-11-20
updated: 2026-11-20
version: 1
outline: prev.health-system   # 기본틀 슬롯(content/outline/subjects.yaml) — 예방의학 손 슬롯 「보건의료체계와 의료법규」
confidence: medium
review_status: unreviewed
note_form: 2            # 판형 2 — 기본틀 빈 슬롯으로 쓴 정리본(오답 연결 없음)
title: "진료비 지불 제도 — 무엇에 돈을 주면 무엇이 느나"
objective: "진료비 지불 제도(행위별 수가·포괄수가·인두제·총액계약·봉급)의 유인과 부작용을 비교해, 제시된 문제(과잉 진료·과소 진료·의뢰 증가·재원 일수·총비용 증가)에 맞는 제도를 고른다"
objective_kind: 감별
condition: 진료비 지불 제도(provider payment mechanisms) — 행위별 수가(fee-for-service) · 포괄수가(case-based/DRG) · 인두제(capitation) · 총액계약·총액예산(global budget) · 봉급(salary)
exams: [kmle, usmle]
summary:
  - "결론: 행위별 수가는 진료량을 늘리고, 인두제·봉급·총액은 비용을 줄이려 진료를 덜 하며, 포괄수가는 재원일수를 줄인다."
  - "시험 단서: 「과잉 진료·검사 남용」은 행위별 수가, 「의뢰 증가·환자 선별」은 인두제, 「입원 건수·상향 코딩」은 포괄수가."
  - "왜: 사후에 단위마다 주면 재정 위험을 지불자가, 사전에 정액으로 주면 공급자가 진다 — 위험을 진 쪽이 아낀다."
  - "포괄수가는 사례당 정액이라 재원일수는 줄지만 입원 건수가 늘 수 있어, 도입국은 모두 지출 상한을 둔다."
  - "단일 제도의 부작용을 막으려 사전 정액에 행위·성과 요소를 섞는 혼합 지불을 권한다."
pitfalls:
  - contrast: "인두제로 바꾸면 전문의·병원 의뢰가 준다?"
    point: "반대다. 인두제는 등록 인원당 정액이라 진료를 덜 하는 쪽이 이익이고, 인두제에서 전문의·병원 의뢰가 더 많았다 [[kazungu-2018: Results — capitation]] [[gosden-2000: 초록]]."
  - contrast: "포괄수가(DRG)는 입원 건수도 줄인다?"
    point: "포괄수가는 재원일수를 줄여 효율을 높이지만 사례(입원) 수를 늘릴 수 있다 — 사례당 돈을 받기 때문이다. 상향 코딩과 필요한 서비스의 과소 제공도 생긴다 [[mathauer-2013: Introduction · Methods]]."
  - contrast: "행위별 수가에서 환자 선별(크림 스키밍)이 문제?"
    point: "행위별 수가는 제공한 단위마다 모두 보상받아 환자 선별의 동기가 없다. 선별은 사전 정액(인두제·총액·봉급) 쪽 부작용이다 [[waitzberg-2022: 4.1]]."
  - contrast: "봉급제 = 생산성을 높이는 제도?"
    point: "봉급은 진료량과 무관해 생산성 유인이 없다 — 실험 연구에서 산출이 가장 적었다 [[kazungu-2018: Results]] [[waitzberg-2022: 4.1]]."
  - contrast: "총액계약이면 공급자가 진료를 늘려 총액을 넘긴다?"
    point: "총액이 미리 정해져 있다. 독일 외래는 분기 총액을 전체 점수로 나눠 점당 가치를 정해 — 모두가 진료량을 늘리면 점당 가치가 떨어진다 [[harrison-21: 7장 p.45]]."
  - contrast: "지불 방식의 효과는 근거가 탄탄하다?"
    point: "일차의료 의사의 지불 방식을 비교한 체계적 고찰에 들어간 연구는 4편뿐이었고 일반화 가능성은 알 수 없다 [[gosden-2000: 초록]]."
tables:
  - id: ppm
    section: "가르는 소견 — 제도별 유인과 부작용"
    title: "진료비 지불 제도 비교"
    role: comparison
    span: full
    columns: ["제도", "지불 단위·시점", "재정 위험", "늘어나는 것", "부작용·단점"]
    rows:
      - ["행위별 수가(fee-for-service)", "개별 서비스마다 · 사후 [[kazungu-2018: Table 1]]", "지불자 [[waitzberg-2022: 4.1]]", "환자 수·서비스 수 — 방문·연속성·권고 방문 준수가 높다 [[waitzberg-2022: 4.1]] [[gosden-2000: 초록]]", "과잉 진료 · 비용 억제·효율 유인 없음 [[waitzberg-2022: 4.1]]"]
      - ["포괄수가(case-based · DRG)", "사례(진단·입원·퇴원)당 정액 = 기준 단가 × DRG 상대 가중치 [[kazungu-2018: Table 1]] [[mathauer-2013: Introduction]]", "공급자(사례 안의 비용) [[kazungu-2018: Results]]", "사례(입원) 수 · 재원일수는 준다 [[mathauer-2013: Introduction]] [[waitzberg-2022: 4.2]]", "불필요한 입원 · 상향 코딩 · 과소 제공 [[mathauer-2013: Methods]]"]
      - ["인두제(capitation)", "등록 1인당 일정 기간 정액 · 사전 [[kazungu-2018: Table 1]]", "공급자 [[waitzberg-2022: 4.1]]", "전문의·병원 의뢰 [[kazungu-2018: Results]] [[gosden-2000: 초록]]", "과소 진료 · 저위험 환자 선별 · 생산성 유인 없음 [[waitzberg-2022: 4.1]]"]
      - ["총액예산·총액계약(global budget)", "합의한 서비스 묶음에 일괄 정액 · 사전 · 쓰임은 자유 [[kazungu-2018: Table 1]]", "공급자 [[waitzberg-2022: 4.1]]", "비용 억제 [[waitzberg-2022: 4.1]]", "과소 진료 · 환자 선별 · 생산성 유인 없음 [[waitzberg-2022: 4.1]]"]
      - ["봉급(salary)", "근무에 대해 고정 급여 · 진료량과 무관", "고용 기관 [[waitzberg-2022: 4.1]]", "환자가 느끼는 접근 만족(행위별 대비) [[gosden-2000: 초록]]", "산출이 가장 적다 · 생산성 유인 없음 [[kazungu-2018: Results]] [[waitzberg-2022: 4.1]]"]
      - ["성과 지불(pay for performance)", "미리 정한 성과 기준 달성에 지불(다른 제도에 얹는다) [[kazungu-2018: Table 1]]", "—", "기준이 가리키는 진료 · 영국 QOF 도입 뒤 GP 소득 평균 25 % 증가 [[harrison-21: 7장 p.45]]", "지표 조작(gaming)·과다 지급 → 감시 필요 [[kazungu-2018: Results]]"]
    note: "봉급의 「재정 위험」은 waitzberg-2022 가 봉급·인두제·총액을 묶어 「공급자에 위험」이라고 쓴 것을, 개인 의사가 아니라 고용 기관이 지는 것으로 읽은 내 판단이다(검토 항목). 일당제(per diem — 하루 정액)는 정의만 확인했고 유인 근거는 읽지 못해 표에서 뺐다 [[kazungu-2018: Table 1]]."
sources:
  - id: kazungu-2018
    org: "Kazungu JS, Barasa EW, Obadha M, Chuma J"
    title: "What characteristics of provider payment mechanisms influence health care providers' behaviour? A literature review"
    kind: review
    year: 2018
    citation: "Int J Health Plann Manage 2018;33(4):e892-e905"
    doi: "10.1002/hpm.2565"
    pmid: "29984422"
    url: "https://pmc.ncbi.nlm.nih.gov/articles/PMC7611391/"
    checked_at: 2026-11-20
    checked: "PMC7611391 본문(WebFetch, 2026-11-20) — 표 1 의 지불 제도 정의(총액예산·항목별 예산·행위별·인두제·일당·사례당(DRG)·성과 지불·혼합): 단위와 사전/사후 · 결과 절: 행위별 수가에서 산출 최대·봉급 최소(실험 연구), 행위별 대비 인두제에서 서비스 양 감소·전문의·병원 의뢰 증가, 인두제·봉급에서 질 높음, 묶음(사례당) 지불은 공급자 재정 위험이 크고 수입이 비용을 못 따라갈 우려, 성과 지불은 조작·과다 지급 위험, 영국 GP 는 인두제 + 성과 지불. 위험 선별·과잉 제공은 이 문헌이 다루지 않음"
    verified: text
  - id: waitzberg-2022
    org: "Waitzberg R, Gerkens S, Dimova A, et al."
    title: "Balancing financial incentives during COVID-19: A comparison of provider payment adjustments across 20 countries"
    kind: review
    year: 2022
    citation: "Health Policy 2022;126(5):398-407"
    doi: "10.1016/j.healthpol.2021.09.015"
    pmid: "34711443"
    url: "https://pmc.ncbi.nlm.nih.gov/articles/PMC8492384/"
    checked_at: 2026-11-20
    checked: "PMC8492384 본문(WebFetch, 2026-11-20) 4.1 · 4.2 · 결론 — 총액예산·봉급·인두제는 사전·포괄 지불로 공급자에 재정 위험, 비용 억제 유인 → 최적 이하 진료, 생산성 유인 없음, 저위험 환자 선별 유인; 행위별 수가는 지불자에 위험, 환자·서비스 수 증가 유인 → 과잉 제공, 단위마다 보상돼 선별 걱정 없음, 비용 억제·효율 유인 없음; DRG·일당 신설 수가는 「더 많은 환자를 치료하되 환자당 비용을 줄이는」 유인; 사전 포괄 지불에 활동 기반 요소를 섞는 혼합 지불 권고. 분석 틀 그림(그림 4)은 이미지라 읽지 못함"
    verified: text
  - id: mathauer-2013
    org: "Mathauer I, Wittenbecher F (WHO)"
    title: "Hospital payment systems based on diagnosis-related groups: experiences in low- and middle-income countries"
    kind: review
    year: 2013
    citation: "Bull World Health Organ 2013;91(10):746-756A"
    doi: "10.2471/BLT.12.115931"
    pmid: "24115798"
    url: "https://pmc.ncbi.nlm.nih.gov/articles/PMC3791650/"
    checked_at: 2026-11-20
    checked: "PMC3791650 본문 앞 100,000자(WebFetch, 2026-11-20 — 남은 약 15,000자는 참고문헌 쪽으로 읽지 않음) — 서론: DRG 분류 변수(주·부진단·나이·성·동반질환·합병증·시술), 지불 = 기준 단가 × DRG 상대 가중치, Street 등 인용 「재원일수를 줄여 효율을 높이지만 사례 수도 늘린다」; 방법: 입원 증가·상향 코딩·필요 서비스 과소 제공이라는 원치 않는 유인; 결과: 자료가 있는 모든 나라가 지출 상한을 둠, 몽골의 물량 상한이 상한까지 채우려는 유인, 코딩 감사 필요; 고찰: Moreno-Serra·Wagstaff — 사례당 지불에서 재원일수 감소·입원 증가 없음·사례당 입원 지출 증가, 크로아티아 재원일수 감소·물량 영향 적음·질 저하 없음; 결론: 지출·물량 상한 권고. 한국은 언급 없음"
    verified: text
  - id: gosden-2000
    org: "Gosden T, Forland F, Kristiansen IS, et al. (Cochrane EPOC)"
    title: "Capitation, salary, fee-for-service and mixed systems of payment: effects on the behaviour of primary care physicians"
    kind: review
    year: 2000
    citation: "Cochrane Database Syst Rev 2000;(3):CD002215"
    doi: "10.1002/14651858.CD002215"
    pmid: "10908531"
    url: "https://pmc.ncbi.nlm.nih.gov/articles/PMC9879313/"
    checked_at: 2026-11-20
    checked: "PubMed MCP 로 PMC9879313 을 열었으나 본문이 비어 초록·쉬운 말 요약만 읽음 — 4개 연구(일차의료 의사 640명·환자 6,400명 이상); 인두제 대비 행위별 수가에서 일차의료 방문·전문의 방문·진단·치료 서비스가 많고 병원 의뢰·반복 처방은 적음, 권고 방문 횟수 준수 높음; 봉급 대비 행위별 수가에서 방문·연속성·권고 방문 준수가 높고 환자의 접근 만족은 낮음; 연구가 적어 일반화 가능성 불명"
    verified: abstract
  - id: harrison-21
    org: "McGraw Hill"
    title: "Harrison's Principles of Internal Medicine, 21st ed. — Chapter 7: Global Diversity of Health System Financing and Delivery"
    kind: textbook
    year: 2022
    citation: "Harrison's Principles of Internal Medicine, 21e. 7장 p.42–49 (22판에 이 장이 없어 21판으로 대조)"
    checked_at: 2026-11-20
    checked: "드라이브 21판 장별 문서(7장) 본문 대조 — 조세 기반 체계의 병원 의사는 협상된 봉급을 받는 공무원(p.44) · 독일 외래 의사는 점수제 행위별 수가: 의사회와 질병금고 연합의 전국 합의로 행위별 점수, 질병금고 연합이 분기 총액을 정하고 분기 끝에 총액 ÷ 전체 점수 = 점당 가치, 의사 점수 × 점당 가치 = 지불(p.45) · 독일·네덜란드 일차의료 접근이 좋은 이유로 흔히 꼽는 것이 수정 행위별 수가(p.45) · 영국 QOF(2004)는 질 연동 추가 소득, GP 소득 평균 25 % 증가(p.45) · 한국 2003년 의약분업(p.48). 지불 제도별 유인을 비교하는 서술은 이 장에 없음"
    verified: text
figures_none: "지불 제도의 유인 비교 — 판독할 영상 소견이 없는 보건 정책 목표다"
diagram:
  title: "지불 제도 상황 문항 — 문제에서 제도로"
  nodes:
    - {id: start, kind: start, text: "의료 이용·비용 문제를 제시한 상황 문항"}
    - {id: info, kind: info, text: "지불 단위·사전/사후·재정 위험을 누가 지나 확인"}
    - {id: q, kind: decision, text: "발문이 말하는 문제는?"}
    - {id: over, kind: end, text: "과잉 진료 → 행위별 수가 탓 · 사전·묶음 지불로"}
    - {id: under, kind: end, text: "과소 진료·의뢰↑·선별 → 인두제·봉급·총액 탓"}
    - {id: los, kind: end, text: "긴 재원일수 → 포괄수가(사례당 정액)"}
    - {id: cap, kind: end, text: "총진료비 증가 → 총액계약·지출 상한"}
    - {id: drg, kind: end, text: "입원 건수↑·상향 코딩 → 포괄수가 부작용"}
  edges:
    - {from: start, to: info}
    - {from: info, to: q}
    - {from: q, to: over, label: "과잉 진료"}
    - {from: q, to: under, label: "과소·의뢰 증가"}
    - {from: q, to: los, label: "재원일수"}
    - {from: q, to: cap, label: "총비용 증가"}
    - {from: q, to: drg, label: "DRG 뒤 문제"}
diagram_notes:
  - "한 제도의 부작용을 다른 제도로 옮기면 반대쪽 부작용이 생긴다 — 그래서 사전 포괄 지불에 활동 기반 요소를 섞는 혼합 지불을 권한다 [[waitzberg-2022: Conclusions]]."
  - "포괄수가를 쓰는 나라는 자료가 있는 모든 곳에서 지출 상한을 두었다. 다만 물량 상한은 상한까지 채우려는 유인을 만들 수 있다(몽골) [[mathauer-2013: Findings — Ceilings]]."
  - "성과 지불은 단독 제도가 아니라 다른 제도에 얹는 요소다 — 영국 GP 는 인두제 + 성과 지불 [[kazungu-2018: Results]]."
checks:
  - q: "검사·처치 건수가 급증해 보험 재정이 악화됐다. 원인으로 가장 의심할 지불 제도와 그 이유는?"
    a: "행위별 수가. 제공한 서비스마다 사후에 보상받아 재정 위험을 지불자가 지고, 공급자에게 진료량을 늘릴 유인이 있다."
  - q: "인두제를 도입한 뒤 늘어날 것으로 예상되는 것 둘은?"
    a: "전문의·병원 의뢰와 저위험 환자 선별. 등록 인원당 정액이라 진료를 덜 할수록 이익이다."
  - q: "포괄수가(DRG) 도입의 기대 효과와 대표 부작용은?"
    a: "재원일수 감소·효율 향상이 기대 효과이고, 입원 건수 증가·상향 코딩·필요 서비스 과소 제공이 부작용이다."
---

## 판단 — 왜 「무엇에 돈을 주나」가 먼저인가
- 지불 제도는 공급자에게 신호(유인)를 준다 — 단위가 무엇이고(서비스·사례·사람·기간), 언제 주며(사전·사후), 재정 위험을 누가 지는지가 행동을 정한다 [[kazungu-2018: Abstract]] [[waitzberg-2022: 4.1]].
- 사후에 단위마다 주면(행위별 수가) 위험은 지불자에게 있고 공급자는 양을 늘린다. 사전에 정액으로 주면(인두제·총액·봉급) 위험은 공급자에게 가고 공급자는 비용을 줄인다 [[waitzberg-2022: 4.1]].
- 그래서 상황 문항은 「문제(과잉·과소·의뢰·재원일수·총비용)」에서 거꾸로 제도를 찾는다 — 도식이 그 길이다.

## 기전 — 지불 단위에서 행동으로
- **행위별 수가(fee-for-service)**: 서비스 하나가 곧 수입이다. 각 단위가 모두 보상되므로 환자를 고를 이유는 없지만, 비용을 아끼거나 효율을 높일 이유도 없다 [[waitzberg-2022: 4.1]]. 일차의료 비교 연구에서 방문·연속성은 높았다 [[gosden-2000: 초록]].
- **포괄수가(case-based · diagnosis-related group, DRG)**: 진단·나이·동반질환·시술로 사례를 묶어, 기준 단가 × 상대 가중치만큼 사례당 준다 [[mathauer-2013: Introduction]]. 사례 안에서 쓰는 비용은 공급자 몫이라 재원일수를 줄이고, 사례 수 자체는 늘릴 유인이 생긴다 [[waitzberg-2022: 4.2]].
- **인두제(capitation)**: 등록한 사람 수에 정액을 미리 준다 [[kazungu-2018: Table 1]]. 진료를 덜 하거나 다른 곳으로 보낼수록 남으므로 의뢰가 늘고, 저위험 환자를 고를 유인이 있다 [[kazungu-2018: Results]] [[waitzberg-2022: 4.1]].
- **총액예산·총액계약(global budget)**: 서비스 묶음 전체에 일괄 정액을 미리 정한다 [[kazungu-2018: Table 1]]. 독일 외래는 의사회·질병금고 연합이 행위 점수와 분기 총액을 합의하고, 분기 끝에 총액을 전체 점수로 나눠 점당 가치를 정한다 — 행위별 수가의 양 증가를 총액이 상쇄한다 [[harrison-21: 7장 p.45]].
- **봉급(salary)**: 진료량과 무관한 고정 급여 — 조세 기반 체계의 병원 의사가 대표다 [[harrison-21: 7장 p.44]]. 생산성 유인이 없다 [[waitzberg-2022: 4.1]].

## 가르는 소견 — 제도별 유인과 부작용
- 표가 다섯 제도와 성과 지불의 단위·위험·늘어나는 것·부작용을 나란히 놓는다.
- **의뢰 증가**는 인두제의 표지다 — 인두제에서 전문의·병원 의뢰가 행위별 수가보다 많았다 [[kazungu-2018: Results]] [[gosden-2000: 초록]].
- **해석 한계**: 일차의료 의사의 지불 방식 비교 고찰에 든 연구는 4편뿐이고 일반화 가능성은 알 수 없다 [[gosden-2000: 초록]]. 같은 제도라도 단가 수준·지급 시기·성과 요구 같은 설계 특성이 행동을 바꾼다 [[kazungu-2018: Results]].

## 선택 — 문제에 맞는 제도
- 과잉 진료·검사 남용 → 사전·묶음 지불(인두제·포괄수가·총액)로 옮긴다. 과소 진료·의뢰 증가 → 행위별·성과 요소를 섞는다 [[waitzberg-2022: Conclusions]].
- 입원이 길다 → 포괄수가. 다만 입원 건수·상향 코딩을 감시하는 코딩 감사와 지출 상한을 함께 둔다 [[mathauer-2013: Findings — Ceilings]].
- 총진료비 자체를 묶어야 한다 → 총액계약(점수제처럼 양이 늘면 단가가 내려가는 구조) [[harrison-21: 7장 p.45]].
- 질 향상이 목표 → 다른 제도에 성과 지불을 얹는다(영국 QOF). 조작을 막을 감시가 필요하다 [[harrison-21: 7장 p.45]] [[kazungu-2018: Results]].

## 권고와 예외
- 한 제도만으로는 반대쪽 부작용이 따른다 — 사전 포괄 지불을 뼈대로 활동 기반 요소를 섞는 혼합(blended) 지불을 권한다 [[waitzberg-2022: Conclusions]].
- 포괄수가에서 물량 상한은 상한까지 채우려는 불필요한 입원을 부를 수 있고, 물량을 줄이면 대기가 길어질 수 있다 [[mathauer-2013: Findings — Ceilings]].
- 한국의 지불 제도(국민건강보험의 행위별 수가·질병군 포괄수가의 범위·연도)와 의료법 조문은 보건복지부·건강보험심사평가원·국가법령정보센터 원문을 읽지 못해 싣지 않았다(검토 항목). 의료법규는 이 정리본의 목표 밖이다.

## 시험 쟁점 — 충돌·맥락·새 근거
- **Z1 충돌 · 포괄수가는 입원 건수를 늘리나** — 시험 기준: 포괄수가는 재원일수를 줄여 효율을 높이지만 사례 수를 늘린다(Street 등) [[mathauer-2013: Introduction]] / 다른 기준: 여러 나라의 사례당 지불 도입을 본 연구는 재원일수 감소·입원 증가 없음·사례당 입원 지출 증가를 보고했다(Moreno-Serra·Wagstaff) [[mathauer-2013: Discussion]] / 왜 다른가: 지출·물량 상한, 코딩 감사, 나라별 설계가 달라 입원 증가 유인이 실제로 드러나는 정도가 다르다 [[mathauer-2013: Findings — Ceilings]] / 시험에서는: KMLE·USMLE 모두 「유인」을 묻는 문항이면 입원 건수 증가·상향 코딩을 포괄수가의 부작용으로 답한다(내 판단 — 국내 교과서와 대조하지 않았다).
- **Z2 맥락 · 「총액계약」과 「총액예산」** — 시험 기준: 총액예산(global budget)은 합의한 서비스 묶음에 미리 정한 일괄 정액 [[kazungu-2018: Table 1]] / 다른 기준: 독일 외래는 의사회와 질병금고 연합이 총액을 정하고 행위별 점수로 나누는 점수제 — 국내 교과서가 「총액계약제」의 예로 드는 형태로 보인다 [[harrison-21: 7장 p.45]] / 왜 다른가: 병원 한 곳에 주는 예산이냐, 공급자 단체와 지불자가 진료비 총액을 계약하느냐의 차이다 / 시험에서는: KMLE 의 「총액계약제」 정의는 국내 교과서와 대조하지 않았다(검토 항목) · USMLE 는 global budget 을 「사전 정액 · 공급자 위험 · 비용 억제」로 답한다.
