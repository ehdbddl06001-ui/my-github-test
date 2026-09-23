---
id: cn.id.legionella-pneumonia.urinary-antigen-diagnosis
type: concept
topic: Infectious Disease
see_also: [Microbiology, Pulmonology]
date: 2026-09-23
updated: 2026-09-23
version: 1
outline: h159            # 기본틀 슬롯(content/outline/subjects.yaml)
confidence: medium
review_status: unreviewed
title: "레지오넬라 폐렴 — 세포 내 세균의 단서에서 확진 검사(소변 항원) 고르기까지"
objective: "레지오넬라가 대식세포 안에서 자라고 일반 배지에서 자라지 않는 성질로 수계 노출·위장관 증상·저나트륨혈증·그람염색 무균 소견을 설명하고, 급성 폐렴에서 이 단서가 모이면 첫 확진 검사로 소변 항원(혈청군 1)을 고르되 음성의 한계와 결핵·마이코플라스마·진균 검사가 맞는 조건을 가른다"
objective_kind: 검사 선택
condition: 레지오넬라 폐렴(재향군인병)
exams: [usmle, kmle]
summary:
  - "레지오넬라는 원래 물속 아메바 안에서 사는 세균이다. 사람은 오염된 물의 에어로졸(냉각탑·분수·온수 욕조·샤워기)을 들이마셔 우연히 감염되고, 폐포 대식세포 안에서 식작용을 피해 증식한다 [[harrison-21: 159장 p.1250–1251]]."
  - "시스테인 같은 특수 영양이 필요해 일반 혈액 한천에서 자라지 않고 BCYE 배지에서 3–5일 걸려 자란다. 객담 그람염색에 호중구는 많은데 균이 안 보이는 것이 이 성질의 결과다 [[harrison-21: 159장 p.1254]]."
  - "폐렴에 신경·위장관 증상(설사·구역)이 같이 오고 저나트륨혈증·간효소 상승·신기능 저하가 흔하다 — 이 조합이 다른 폐렴과 가르는 단서다 [[harrison-21: 159장 p.1253]]."
  - "가장 빠른 확진은 소변 항원검사다. 쉽고 빠르며 특이도가 매우 높지만 L. pneumophila 혈청군 1만 잡는다(민감도 약 70%) — 음성이어도 배제하지 못한다 [[harrison-21: 159장 p.1255]]. 하기도 검체 PCR 은 배양보다 민감하다 [[harrison-21: 159장 p.1255]]."
  - "치료는 세포 안으로 들어가는 약 — 플루오로퀴놀론(레보플록사신) 또는 매크롤라이드(아지스로마이신) [[harrison-21: 159장 p.1256]]. 베타락탐은 세포 안에 닿지 않는다."
pitfalls:
  - contrast: "「일반 배지 음성·그람염색 무균 = 특수 균(결핵)」 vs 급성 레지오넬라"
    point: "일반 배지에서 안 자라는 폐렴균은 여럿이다(레지오넬라·마이코플라스마·결핵·진균). 어느 검사를 할지는 배양 결과가 아니라 **경과와 노출**이 정한다. 며칠 사이의 고열·설사·저나트륨과 수계 노출이면 레지오넬라, 수주의 기침·객혈·야간발한·체중감소와 상엽 공동이면 결핵이다."
    exception: "면역저하자는 전형적 증상 없이 올 수 있고, 두 감염이 겹칠 수도 있다 — 경과가 애매하면 둘 다 검사한다."
    cites: ["harrison-21"]
    covers: ["usmle-2026-0045:D"]
  - contrast: "소변 항원 음성 = 레지오넬라 배제?"
    point: "소변 항원은 혈청군 1만 잡고 민감도도 약 70% 다. 발병 아주 초기에는 음성일 수 있고, 무뇨 환자에게는 쓸 수 없다. 의심이 남으면 하기도 검체 PCR·BCYE 배양을 하고 경험적 치료를 유지한다 [[harrison-21: 159장 p.1255]]."
    cites: ["harrison-21"]
  - contrast: "한랭응집소(마이코플라스마)"
    point: "마이코플라스마는 젊은 사람의 가벼운 「걸어 다니는 폐렴」이 전형이고, 한랭응집소는 비특이적이라 확진 검사가 아니다. 저나트륨·설사·수계 노출·고열의 중증 폐렴은 레지오넬라 쪽이다(마이코플라스마 서술은 해리슨 159장 밖 — 원문 미대조)."
criteria:
  - id: leg-uat
    name: 소변 항원검사
    kind: 검사 기준
    population: "레지오넬라가 의심되는 폐렴"
    statement: "쉽고 빠르며 특이도가 매우 높다. L. pneumophila 혈청군 1만 검출, 민감도 약 70%. 초기에는 음성일 수 있고 감염 뒤 수개월 양성이 남을 수 있으며, 무뇨 환자에서는 쓸 수 없다 [[harrison-21: 159장 p.1255]]"
    exceptions: "혈청군 1 이외·다른 종(면역저하자에서 더 흔함)은 놓친다 [[harrison-21: 159장 p.1250]]"
    source: harrison-21
    basis: current
    exams: [usmle, kmle]
  - id: leg-culture-pcr
    name: 배양·분자 검사
    kind: 검사 기준
    population: "레지오넬라가 의심되는 폐렴"
    statement: "하기도 검체의 BCYE 배양이 표준(역학 조사에 필수), 3–5일 소요. PCR 등 핵산증폭검사는 배양보다 민감하다 [[harrison-21: 159장 p.1254–1255]]"
    exceptions: "항생제 투여 뒤 채취하면 배양 민감도가 떨어진다"
    source: harrison-21
    basis: current
    exams: [usmle, kmle]
  - id: leg-tx
    name: 치료
    kind: 치료 기준
    population: "레지오넬라 폐렴"
    statement: "플루오로퀴놀론(레보플록사신 등) 또는 매크롤라이드(아지스로마이신 등). 면역저하자는 중등증 이상으로 보고 정주로 시작 [[harrison-21: 159장 p.1256]]"
    exceptions: "기간·병용 요법 세부는 이 정리본에서 대조하지 않았다(검토 항목)"
    source: harrison-21
    basis: current
    exams: [usmle, kmle]
sources:
  - id: harrison-21
    org: "McGraw Hill"
    title: "Harrison's Principles of Internal Medicine, 21st ed. — Chapter 159: Legionella Infections"
    kind: textbook
    year: 2022
    citation: "Loscalzo J, Kasper DL, Longo DL, et al (eds). Harrison's Principles of Internal Medicine, 21e. 159장 p.1249–1256"
    checked_at: 2026-09-23
    checked: "본문 대조(드라이브 159장 문서) — p.1250: 아메바 안 증식·사람은 우연 숙주·흡입 뒤 폐포 대식세포 안 증식, 미국 배양 확진의 약 10% 가 혈청군 1 이외 · p.1251: 냉각탑·분수·온수 욕조·샤워기 등 수계 노출원 · p.1253: 신경·위장관 증상이 있으면 레지오넬라 가능성, 백혈구 증가·혈소판 감소·간효소 상승·저나트륨·신기능 저하 흔함, 폰티악열은 폐렴 없는 자기 제한 질환 · p.1254: BCYE 배지·시스테인 요구·3–5일, 배양이 표준 · p.1255: 소변 항원은 혈청군 1만·민감도 약 70%·특이도 매우 높음·초기 음성·수개월 양성·무뇨 불가, PCR 이 배양보다 민감 · p.1256 표: 플루오로퀴놀론 또는 매크롤라이드. 비교맥(상대적 서맥)은 이 장에서 확인하지 못했다"
    verified: text
diagram:
  title: "급성 폐렴에서 레지오넬라 확진 검사 고르기"
  nodes:
    - {id: start, kind: start, text: "고열·기침·새 침윤의 폐렴, 객담 그람염색에 호중구는 많고 균은 안 보임"}
    - {id: course, kind: decision, text: "경과는? 며칠의 급성 vs 수주의 기침·객혈·야간발한·체중감소"}
    - {id: tb, kind: alert, text: "만성 경과·상엽 침윤이나 공동 — 결핵: AFB 도말·배양·핵산증폭검사(이 도식 범위 밖)"}
    - {id: clue, kind: decision, text: "레지오넬라 단서가 있는가? 수계 노출·설사·저나트륨·간효소 상승"}
    - {id: cluedo, kind: info, text: "여행·숙박·온수 욕조 노출과 나트륨·간효소를 확인한다"}
    - {id: cap, kind: alert, text: "단서 없음 — 일반 지역사회 폐렴 평가·경험적 치료(이 도식 범위 밖)"}
    - {id: uat, kind: decision, text: "소변 항원검사(혈청군 1) 결과는?"}
    - {id: confirm, kind: end, text: "확진 — 레보플록사신 또는 아지스로마이신"}
    - {id: more, kind: end, text: "배제되지 않음 — 하기도 검체 PCR·BCYE 배양, 경험적 치료 유지"}
  edges:
    - {from: start, to: course}
    - {from: course, to: tb, label: "수주·만성"}
    - {from: course, to: clue, label: "며칠·급성"}
    - {from: clue, to: uat, label: "있음"}
    - {from: clue, to: cap, label: "없음"}
    - {from: clue, to: cluedo, label: "모름"}
    - {from: cluedo, to: uat, label: "하나라도 있으면"}
    - {from: cluedo, to: cap, label: "모두 없으면"}
    - {from: uat, to: confirm, label: "양성"}
    - {from: uat, to: more, label: "음성"}
diagram_notes:
  - "그람염색에 균이 안 보이는 것은 레지오넬라가 없다는 뜻이 아니라, 일반 염색·배지로 잘 안 보이는 세균이라는 뜻이다."
  - "면역저하자는 발열 없이 올 수 있고 혈청군 1 이외·다른 종이 더 흔해 소변 항원 음성이 더 흔하다 — PCR·배양을 함께 낸다 [[harrison-21: 159장 p.1250, p.1253]]."
  - "소변 항원은 수개월 양성이 남을 수 있다 — 최근 레지오넬라 병력이 있으면 양성의 해석에 주의한다 [[harrison-21: 159장 p.1255]]."
checks:
  - q: "레지오넬라 폐렴에서 객담 그람염색에 균이 잘 보이지 않고 일반 배지에서 자라지 않는 이유는?"
    a: "대식세포 안에서 자라는 세포 내 세균이고 시스테인 같은 특수 영양이 필요해 BCYE 배지에서만 자란다."
  - q: "소변 항원검사가 음성이면 레지오넬라를 배제할 수 있나?"
    a: "아니다. 혈청군 1만 잡고 민감도가 약 70% 라 음성이어도 하기도 PCR·BCYE 배양으로 확인한다."
  - q: "같은 「배양 음성 폐렴」에서 결핵 검사를 먼저 해야 하는 경과는?"
    a: "수주 이상의 기침·객혈·야간발한·체중감소, 상엽 침윤이나 공동, 결핵 노출 위험."
variants:
  - id: v1
    of: usmle-2026-0045
    flip: true
    changed: "3일의 급성 고열·설사·저나트륨·호텔 온수 욕조 노출 → 8주의 기침·객혈·야간발한·체중감소, 교정시설 근무, 우상엽 공동·정상 나트륨 ⇒ 정답이 소변 레지오넬라 항원에서 객담 AFB 도말·배양으로"
    context: "단서를 바꿔 답이 바뀌는 변형 — 수주의 경과와 상엽 공동"
    stem: "A 58-year-old man who works as a guard at a correctional facility presents with an 8-week history of productive cough, two episodes of blood-streaked sputum, drenching night sweats, and a 6-kg weight loss. He has had low-grade evening fevers but no diarrhea. Chest x-ray shows a right upper lobe infiltrate with a thick-walled cavity. Sputum Gram stain shows many neutrophils but no predominant organism, and a routine culture on standard blood agar shows only normal flora after 48 hours. Serum sodium is 139 mEq/L, and liver enzymes are normal. Which of the following is the most appropriate next diagnostic test?"
    choices: ["A. Urinary antigen test for Legionella pneumophila serogroup 1", "B. Sputum acid-fast bacillus smear and mycobacterial culture", "C. Cold agglutinin titer", "D. Serum beta-D-glucan assay", "E. Repeat sputum culture on standard blood agar"]
    answer: "B"
    explanation: "The changed clues are the time course and pattern: weeks of cough with hemoptysis, night sweats, weight loss, an occupational tuberculosis exposure, and an upper-lobe cavity. These point to pulmonary tuberculosis, so sputum AFB smear and mycobacterial culture (with nucleic acid amplification) come first. Legionella causes an acute illness over days with water-source exposure, diarrhea, hyponatremia, and transaminitis — none are present here [[harrison-21: 159장 p.1253]]. Cold agglutinins are nonspecific, beta-D-glucan targets invasive fungal infection in immunocompromised hosts, and repeating a standard culture will not grow mycobacteria."
    kind: application
  - id: v2
    of: usmle-2026-0045
    flip: false
    changed: "나이·성별(67세 여성)·노출원(크루즈선 스파)·동반 증상(혼돈)·제시 순서를 바꾸고, 급성 고열·설사·저나트륨·간효소 상승·그람염색 무균·일반 배지 음성은 유지 ⇒ 답은 그대로 소변 항원"
    context: "겉모습만 바꾸고 답은 같은 변형 — 크루즈 여행 뒤 폐렴과 혼돈"
    stem: "A 67-year-old woman is brought to the emergency department 4 days after returning from a cruise during which she used the ship's spa pool daily. Her husband reports that she has had fever to 40 C, loose stools, and new confusion for 2 days, followed by a cough. She smokes 1 pack per day. Chest x-ray shows a left lower lobe consolidation. Serum sodium is 127 mEq/L, AST is 88 U/L, and ALT is 71 U/L. A sputum Gram stain shows abundant neutrophils without visible bacteria, and a sputum culture on routine media has no growth at 2 days. Which of the following is the most appropriate test to confirm the most likely diagnosis?"
    choices: ["A. Serum galactomannan assay", "B. Sputum acid-fast bacillus smear", "C. Legionella urinary antigen test", "D. Cold agglutinin titer", "E. Rapid streptococcal antigen test of the throat"]
    answer: "C"
    explanation: "The deciding clues are unchanged: an acute pneumonia after aerosolized warm-water exposure, with diarrhea, neurologic symptoms, hyponatremia, elevated transaminases, and neutrophils without organisms on a sputum that does not grow on routine media [[harrison-21: 159장 p.1251, p.1253]]. The urinary antigen test is the fastest confirmatory test, although it detects only serogroup 1 and a negative result should prompt PCR or BCYE culture [[harrison-21: 159장 p.1255]]. The acute course argues against tuberculosis, galactomannan is for invasive aspergillosis, and cold agglutinins are nonspecific."
    kind: application
---

## 정의
레지오넬라 폐렴(재향군인병)은 주로 *Legionella pneumophila*(대개 혈청군 1)가 일으키는 폐렴이다. 폐렴 없이 독감처럼 지나가는 **폰티악열**과 함께 레지오넬라증이라 부른다 [[harrison-21: 159장 p.1249, p.1253]].

## 병태생리
레지오넬라는 물속 아메바·원생동물 안에서 증식하는 세균이고 사람은 우연 숙주다. 냉각탑·분수·온수 욕조·샤워기처럼 따뜻한 물이 고인 건물 배관에서 에어로졸로 흡입되면, 폐포 대식세포에 먹힌 뒤 식포-리소좀 융합을 피해 **대식세포 안에서** 증식한다 [[harrison-21: 159장 p.1250–1251]]. 사람 사이 전파는 거의 없다.

## 기전에서 소견으로
- 세포 내 증식 + 특수 영양 요구 → 그람염색에 호중구는 많은데 균이 거의 안 보이고, 일반 혈액 한천에서 자라지 않는다(BCYE 필요) [[harrison-21: 159장 p.1254]].
- 전신 염증과 다장기 침범 → 고열, 두통·혼돈, 설사·구역, 간효소 상승, 신기능 저하, **저나트륨혈증** [[harrison-21: 159장 p.1253]].
- 흉부 X선은 반점형·대엽성 침윤으로 특이적이지 않다 — 영상으로 원인균을 정할 수 없다.

## 감별
- **결핵**: 수주~수개월 경과, 객혈·야간발한·체중감소, 상엽 침윤·공동 → AFB 도말·배양·핵산증폭.
- **마이코플라스마·클라미도필라**: 대개 가벼운 비정형 폐렴, 저나트륨·설사는 두드러지지 않음.
- **침습성 진균 감염**: 호중구감소·면역저하 숙주 → 베타-D-글루칸·갈락토만난.
- **폐렴구균 폐렴**: 그람양성 쌍구균이 보이고 소변 폐렴구균 항원이 있다.

## 검사
1. **소변 항원(혈청군 1)** — 가장 빠르고 쉬움, 특이도 매우 높음, 민감도 약 70% [[harrison-21: 159장 p.1255]].
2. **하기도 검체 PCR** — 배양보다 민감, 점점 보급 [[harrison-21: 159장 p.1255]].
3. **BCYE 배양** — 표준, 역학 조사(노출원 비교)에 필수, 3–5일 [[harrison-21: 159장 p.1254]].
4. 혈청 항체(4배 상승) — 급성기 진단에는 늦고 민감도가 낮아 역학 조사용.

## 치료
- 레보플록사신 등 플루오로퀴놀론 또는 아지스로마이신 등 매크롤라이드 — 세포 안으로 들어가는 약 [[harrison-21: 159장 p.1256]].
- 면역저하자는 중등증 이상으로 보고 정주로 시작한다 [[harrison-21: 159장 p.1256]].
- 재평가: 발열·산소화·나트륨·신기능의 호전. 음성 소변 항원으로 치료를 끊지 않는다.

## 권고와 예외
- 소변 항원 음성은 혈청군 1 이외 균, 발병 초기, 면역저하자에서 흔하다 — PCR·배양으로 확인.
- 집단 발생이 의심되면 배양 분리주가 노출원 추적에 필요하므로 항생제 전에 하기도 검체를 받는 것이 좋다 [[harrison-21: 159장 p.1254]].

## 시험 쟁점 — 충돌·맥락·새 근거
- **Z1 새 근거 · 「가장 좋은 확진 검사」** — 시험 기준: 빠른 첫 확진 검사는 소변 항원(혈청군 1) [[harrison-21: 159장 p.1255]] / 다른 기준: 해리슨은 하기도 검체 PCR 이 배양보다 2–4배 더 많은 증례를 찾는다며 보급이 늘고 있다고 적는다 [[harrison-21: 159장 p.1255]] / 왜 다른가: 소변 항원은 빠르지만 혈청군 1만 잡고, PCR 은 민감하지만 하기도 검체와 검사실 여건이 필요하다 / 시험에서는: USMLE · 보기에 소변 항원이 있으면 「다음 검사」로 그것, 「표준(gold standard)」을 물으면 BCYE 배양 · KMLE 도 같은 흐름.

## (심화) 음성 결과가 주는 정보
이 문항의 「그람염색 무균 + 일반 배지 48시간 무성장」은 음성 결과지만 진단을 좁히는 정보다. 다만 그것만으로는 결핵·마이코플라스마·레지오넬라가 모두 남는다 — 경과(며칠)와 노출(온수 욕조)이 셋 중 하나를 고른다.
