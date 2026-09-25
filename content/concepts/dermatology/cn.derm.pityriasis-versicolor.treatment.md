---
id: cn.derm.pityriasis-versicolor.treatment
type: concept
topic: Dermatology
see_also: [Infectious Disease]
date: 2026-09-18
updated: 2026-09-25
version: 3
outline: h57            # 기본틀 슬롯(content/outline/subjects.yaml)
confidence: medium
review_status: unreviewed
note_form: 2            # 판형 2(2026-09-25) — 결론·시험 단서·왜 → 혼동 → 표·도식 → 목표에 맞춘 본문
title: "어루러기 — 치료 수준은 범위·재발이 정한다"
objective: "어루러기를 KOH 소견으로 확인한 뒤, 범위·재발·국소 치료 실패에 따라 국소 항진균제와 경구 아졸 중 치료를 고른다"
objective_kind: 치료
condition: 어루러기(전풍, pityriasis/tinea versicolor)
exams: [kmle, usmle]
summary:
  - "결론: 국한·첫 발병은 국소 항진균제, 광범위·재발·국소 실패는 경구 이트라코나졸·플루코나졸."
  - "시험 단서: 몸통 위쪽 비늘 있는 저·과색소 반점 + KOH 짧은 균사·둥근 포자 무리 = 말라세지아(Malassezia)."
  - "왜: 진단은 같아도 상재 효모라 재발이 흔하다 — 범위와 재발이 치료 수준을 바꾼다."
  - "쓰지 않는 약: 경구 테르비나핀·그리세오풀빈(피부사상균 약), 경구 케토코나졸(간독성), 스테로이드(악화)."
  - "흰 반점은 균이 없어진 뒤 수개월에 걸쳐 돌아온다 — 남아 있어도 치료 실패가 아니다."
pitfalls:
  - contrast: "경구 그리세오풀빈·테르비나핀 vs 경구 아졸"
    point: "그리세오풀빈·테르비나핀은 피부사상균(백선) 약이라 효모인 말라세지아에 듣지 않는다. 경구로 올릴 때는 이트라코나졸·플루코나졸."
    exception: "경구 케토코나졸도 아졸이지만 간독성으로 1차로 쓰지 않는다."
    cites: ["harrison-21: 57장 p.380–381", "gupta-2015"]
    covers: ["kmle-2026-1063:C"]
  - contrast: "국소 스테로이드 — 가려운 비늘 반점이면?"
    point: "원인이 곰팡이라 스테로이드는 악화시킨다. 비늘 있는 반점에서 먼저 KOH 로 균을 확인한다."
    covers: ["kmle-2026-1063:B"]
  - contrast: "국소 타크로리무스 — 흰 반점이면?"
    point: "타크로리무스는 백반증 쪽 약이다. 백반증은 비늘이 없고 완전 탈색이며 KOH 가 음성이다."
    covers: ["kmle-2026-1063:D"]
  - contrast: "치료 뒤 남은 흰 반점 = 실패?"
    point: "색소 회복은 균이 없어진 뒤 수개월 걸린다. 활동성은 비늘·KOH 로 본다."
tables:
  - id: level
    section: "선택 — 국소에서 경구로 올리는 조건"
    title: "치료 수준 — 무엇이 바꾸나"
    role: treatment
    span: column
    columns: ["상황", "치료", "주의"]
    rows:
      - ["국한·첫 발병", "국소 항진균제 — 아졸 크림·샴푸, 셀레늄 설파이드, 징크 피리치온 [[harrison-21: 57장 p.381]]", "1–2주 매일 뒤 주 1회. 국소제 사이의 우열 근거는 약하다 [[hu-bigby-2010]]"]
      - ["광범위·재발·국소 실패", "경구 이트라코나졸 또는 플루코나졸 [[gupta-2015]]", "효과는 있으나 오래가지 않는다 [[harrison-21: 57장 p.381]]. 용량·기간은 대조하지 않았다"]
      - ["쓰지 않는다", "경구 테르비나핀·그리세오풀빈(무효), 경구 케토코나졸(간독성), 국소 스테로이드(악화)", "타크로리무스는 백반증 약"]
      - ["재발이 잦다", "예방적 국소제", "상재균이라 재발이 흔하다"]
  - id: ddx
    section: "가르는 소견 — 비늘·색·KOH"
    title: "흰 반점·비늘 반점 감별"
    role: differential
    span: column
    columns: ["질환", "가르는 소견", "치료 쪽"]
    rows:
      - ["어루러기", "몸통 위쪽, 미세한 비늘, 저·과색소, KOH 짧은 균사+둥근 포자", "국소·경구 아졸"]
      - ["백반증", "비늘 없음, 완전 탈색, KOH 음성", "국소 타크로리무스 등"]
      - ["체부백선", "가장자리가 활동성인 고리 모양, 피부사상균", "그리세오풀빈·테르비나핀"]
      - ["염증 후 저색소·백색 비강진·장미색 비강진·지루 피부염", "분포·비늘·KOH 로 가른다", "—"]
criteria:
  - id: pv-first-line
    name: 1차 치료
    kind: 치료 권고
    population: "국한된 어루러기"
    statement: "국소 항진균제(케토코나졸 등 아졸, 징크 피리치온, 테르비나핀 국소제)가 1차 — 해리슨도 셀레늄 설파이드·아졸 국소제를 1–2주 매일, 이후 주 1회로 제시한다 [[harrison-21: 57장 p.381]]"
    exceptions: "광범위·재발·국소 치료 실패는 경구 아졸 고려"
    source: gupta-2015
    basis: current
    exams: [kmle, usmle]
  - id: pv-oral
    name: 경구 치료
    kind: 치료 권고
    population: "중증·난치 어루러기"
    statement: "경구 이트라코나졸 또는 플루코나졸. 경구 테르비나핀은 효과가 없고 경구 케토코나졸은 간독성으로 더 이상 1차로 쓰지 않는다 [[harrison-21: 57장 p.380–381]]. 해리슨은 경구제가 효과는 있으나 오래가지 않는다고 적는다 [[harrison-21: 57장 p.381]]"
    exceptions: "용량·기간은 이 정리본에서 대조하지 않았다(검토 항목)"
    source: gupta-2015
    basis: current
    exams: [kmle, usmle]
  - id: pv-evidence
    name: 근거 수준
    kind: 근거 요약
    population: "어루러기 치료 연구"
    statement: "대부분의 국소·전신 치료가 위약보다 효과적이나 시험의 질이 낮고 약제 간 상대 효과는 불확실하다"
    exceptions: "「어느 국소제가 가장 낫다」는 근거로 쓰지 않는다"
    source: hu-bigby-2010
    basis: current
    exams: [kmle, usmle]
sources:
  - id: harrison-21
    org: "McGraw Hill"
    title: "Harrison's Principles of Internal Medicine, 21st ed. — Chapter 57: Eczema, Psoriasis, Cutaneous Infections, Acne, and Other Common Skin Disorders"
    kind: textbook
    year: 2022
    citation: "Loscalzo J, Kasper DL, Longo DL, et al (eds). Harrison's Principles of Internal Medicine, 21e. 57장 p.380–381 (Table 57-5 · Tinea (Pityriasis) Versicolor)"
    checked_at: 2026-09-22
    checked: "본문 대조(PC, 드라이브 원본 PDF 57장 p.380–381) — 원인 Malassezia furfur(피부 상재균, 고온다습에서 발현) · 가슴·어깨·등의 인설 반, 피부색에 따라 저·과색소 · KOH 에서 짧은 균사+둥근 포자(spaghetti and meatballs) · 치료는 국소 셀레늄 설파이드·아졸(유황·살리실산·셀레늄 설파이드 로션/샴푸 1–2주 매일 뒤 주 1회), 10분 넘게 두면 자극 · 경구 항진균제도 효과는 있으나 효과가 오래가지 않고 FDA 적응증이 아니다 · 경구 케토코나졸은 간독성으로 FDA 가 1차 사용을 제한. 색소 회복 기간·경구 이트라코나졸/플루코나졸 용량은 해리슨에 없다"
    verified: text
  - id: gupta-2015
    org: "Gupta AK, Foley KA (체계적 문헌고찰)"
    title: "Antifungal treatment for pityriasis versicolor"
    kind: review
    year: 2015
    citation: "J Fungi (Basel) 2015;1(1):13-29"
    doi: "10.3390/jof1010013"
    pmid: "29376896"
    url: "https://doi.org/10.3390/jof1010013"
    checked_at: 2026-09-18
    checked: "PubMed 초록과 대조(국소 1차, 경구 이트라코나졸·플루코나졸, 경구 테르비나핀 무효, 경구 케토코나졸 중단)"
    verified: abstract
  - id: hu-bigby-2010
    org: "Hu SW, Bigby M (체계적 문헌고찰·메타분석)"
    title: "Pityriasis versicolor: a systematic review of interventions"
    kind: review
    year: 2010
    citation: "Arch Dermatol 2010;146(10):1132-1140"
    doi: "10.1001/archdermatol.2010.259"
    pmid: "20956647"
    url: "https://doi.org/10.1001/archdermatol.2010.259"
    checked_at: 2026-09-18
    checked: "PubMed 초록과 대조(대부분 효과적, 시험 질 낮음)"
    verified: abstract
diagram:
  title: "어루러기 — 진단 확인에서 치료 수준까지"
  nodes:
    - {id: start, kind: start, text: "몸통 위쪽의 비늘 있는 저·과색소 반점"}
    - {id: koh, kind: decision, text: "KOH 에서 짧은 균사·둥근 포자 무리?"}
    - {id: kohdo, kind: info, text: "KOH 검경 — 우드등 음성은 배제 아님"}
    - {id: other, kind: alert, text: "다른 진단 — 백반증·염증 후 저색소 등(표)"}
    - {id: extent, kind: decision, text: "국한되고 첫 발병인가?"}
    - {id: extask, kind: info, text: "범위·이전 발병·국소 치료 결과를 확인"}
    - {id: topical, kind: end, text: "국소 항진균제(아졸·셀레늄 설파이드 등)"}
    - {id: oral, kind: end, text: "경구 이트라코나졸 또는 플루코나졸"}
  edges:
    - {from: start, to: koh}
    - {from: koh, to: extent, label: "있음"}
    - {from: koh, to: other, label: "없음"}
    - {from: koh, to: kohdo, label: "미시행"}
    - {from: kohdo, to: extent, label: "있으면"}
    - {from: kohdo, to: other, label: "없으면"}
    - {from: extent, to: topical, label: "예"}
    - {from: extent, to: extask, label: "정보 없음"}
    - {from: extent, to: oral, label: "광범위·재발·실패"}
    - {from: extask, to: topical, label: "국한·첫 발병"}
    - {from: extask, to: oral, label: "광범위·재발"}
diagram_notes:
  - "경구로 올릴 때도 테르비나핀·그리세오풀빈은 무효, 케토코나졸은 간독성으로 쓰지 않는다 — 아졸 중 이트라코나졸·플루코나졸."
  - "치료 뒤에도 색 회복은 균이 없어진 뒤 수개월 걸린다 — 흰 반점이 남아도 비늘·KOH 로 활동성을 본다."
  - "재발이 잦으면(상재균이라 흔함) 예방적 국소제를 고려한다."
  - "우드등 형광은 일부에서만 보이므로 음성이어도 어루러기를 배제하지 않는다 — KOH 가 기준이다."
checks:
  - q: "어루러기 치료를 국소제와 경구제로 가르는 기준은?"
    a: "범위(광범위), 재발, 국소 치료 실패. 진단 자체가 아니라 이 세 가지가 치료 수준을 정한다."
  - q: "경구 테르비나핀·그리세오풀빈이 어루러기에 쓰이지 않는 이유는?"
    a: "말라세지아(효모)에 효과가 없다 — 피부사상균(백선) 약이다. 경구로는 이트라코나졸·플루코나졸."
  - q: "치료 뒤에도 흰 반점이 남았다. 치료 실패인가?"
    a: "대개 아니다. 색소 회복은 균이 없어진 뒤 수개월 걸린다. 비늘·KOH 로 활동성을 본다."
variants:
  - id: v1
    context: "같은 목표, 다른 맥락 — 광범위·재발·국소 치료 실패"
    stem: "35세 여자가 3년째 여름마다 몸통과 양팔에 번지는 비늘 있는 연갈색 반점으로 왔다. 올해도 케토코나졸 샴푸를 두 차례 발랐지만 2주 만에 다시 번졌다. 병변은 가슴·등 전체와 양쪽 위팔을 덮는다. KOH 검경에서 짧은 균사와 둥근 포자 무리가 보인다. 간기능 검사는 정상이다. 가장 적절한 치료는?"
    choices: ["A. 케토코나졸 샴푸를 같은 방법으로 계속", "B. 경구 이트라코나졸", "C. 경구 테르비나핀", "D. 국소 스테로이드", "E. 경구 그리세오풀빈"]
    answer: "B"
    explanation: "진단은 같지만 범위가 넓고 재발하며 국소 치료에 실패했다 — 치료 수준을 경구 아졸로 올린다. 경구 테르비나핀·그리세오풀빈은 말라세지아에 효과가 없고, 스테로이드는 악화시킨다."
    kind: application
---

## 판단 — 왜 범위·재발이 치료를 바꾸나
- 진단(어루러기)이 같아도 치료 수준은 **범위·재발·국소 치료 결과**가 정한다.
- 원인균이 피부 **상재 효모**라 균을 없애도 다시 늘어날 조건이 남는다 — 그래서 재발이 흔하고, 넓거나 되풀이되면 국소제로는 모자란다.
- 약 선택은 균의 종류에서 나온다: 효모(말라세지아)에는 아졸, 피부사상균(백선)에는 그리세오풀빈·테르비나핀.

## 기전 — 상재 효모에서 반점까지
덥고 습한 환경, 땀, 기름진 피부에서 말라세지아(Malassezia)가 효모형에서 균사형으로 바뀌어 피지가 많은 몸통 위쪽·목·위팔에 퍼진다. 말라세지아는 지질을 요구해 일반 배양에서 잘 자라지 않는다.
- 균이 만드는 아젤라산이 멜라닌 합성을 억제 → 햇볕에 타도 그 부위만 하얗게 남는다(저색소).
- 각질층의 균 → 긁으면 미세한 비늘이 두드러진다.

## 가르는 소견 — 비늘·색·KOH
- **KOH 검경**이 기준이다: 짧은 균사와 둥근 포자 무리(「스파게티와 미트볼」). 배양은 일상적으로 필요 없고, 일반 배지 음성은 오히려 합당하다.
- 우드등 형광은 일부에서만 보이는 보조 소견 — 음성이어도 배제하지 않는다.

## 선택 — 국소에서 경구로 올리는 조건
- 국한·첫 발병 → 국소 항진균제. 광범위·재발·국소 실패 → 경구 이트라코나졸 또는 플루코나졸.
- 색 회복에 수개월 걸린다는 것을 미리 설명한다. 재발이 잦으면 예방적 국소제.

## 권고와 예외
- 국소제 사이의 상대 효과는 근거가 약하다 — 「가장 좋은 국소제」를 외울 필요는 없다.
- 경구 아졸의 용량·기간은 이 정리본에서 대조하지 않았다(검토 항목).
- 국내 교과서의 권고 문구는 대조하지 않았다(검토 항목).
