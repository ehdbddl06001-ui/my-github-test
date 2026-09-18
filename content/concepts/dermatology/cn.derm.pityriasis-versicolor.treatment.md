---
id: cn.derm.pityriasis-versicolor.treatment
type: concept
topic: Dermatology
see_also: [Infectious Disease]
date: 2026-09-18
updated: 2026-09-18
version: 2
confidence: medium
review_status: unreviewed
title: "어루러기 — 진단 단서에서 치료 수준(국소 vs 경구 아졸)으로"
objective: "어루러기를 KOH 소견으로 확인한 뒤, 범위·재발·국소 치료 실패에 따라 국소 항진균제와 경구 아졸 중 치료를 고른다"
objective_kind: 치료
condition: 어루러기(전풍)
exams: [kmle, usmle]
summary:
  - "진단 단서: 몸통 위쪽의 비늘 있는 저·과색소 반점 + KOH 에서 짧은 균사와 둥근 포자 무리(말라세지아)."
  - "치료는 「진단」이 아니라 「범위·재발」로 갈린다: 국한·첫 발병 → 국소 항진균제, 광범위·재발·국소 실패 → 경구 이트라코나졸·플루코나졸."
  - "경구 테르비나핀·그리세오풀빈은 효과가 없다(피부사상균 약). 경구 케토코나졸은 간독성으로 쓰지 않는다."
  - "스테로이드·타크로리무스는 곰팡이를 돕거나 무관 — 습진·백반증으로 오인했을 때의 선택이다."
  - "색은 균이 없어진 뒤 수개월에 걸쳐 돌아온다 — 치료 실패가 아니다."
criteria:
  - id: pv-first-line
    name: 1차 치료
    kind: 치료 권고
    population: "국한된 어루러기"
    statement: "국소 항진균제(케토코나졸 등 아졸, 징크 피리치온, 테르비나핀 국소제)가 1차"
    exceptions: "광범위·재발·국소 치료 실패는 경구 아졸 고려"
    source: gupta-2015
    basis: current
    exams: [kmle, usmle]
  - id: pv-oral
    name: 경구 치료
    kind: 치료 권고
    population: "중증·난치 어루러기"
    statement: "경구 이트라코나졸 또는 플루코나졸. 경구 테르비나핀은 효과가 없고 경구 케토코나졸은 더 이상 처방하지 않는다"
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
    - {id: koh, kind: decision, text: "KOH 검경에서 짧은 균사와 둥근 포자 무리가 보이는가?"}
    - {id: kohdo, kind: info, text: "KOH 검경을 한다 — 우드등 형광은 보조일 뿐 음성이어도 배제하지 않는다"}
    - {id: other, kind: alert, text: "다른 진단 — 백반증(비늘 없음·완전 탈색)·염증 후 저색소·장미색 비강진 등"}
    - {id: extent, kind: decision, text: "국한되고 첫 발병인가? 범위 · 재발 횟수 · 이전 국소 치료 결과"}
    - {id: extask, kind: info, text: "범위와 이전 발병·치료 이력을 확인한다"}
    - {id: topical, kind: end, text: "국소 항진균제 — 케토코나졸 크림·샴푸 등 아졸, 셀레늄 설파이드, 징크 피리치온"}
    - {id: oral, kind: end, text: "경구 이트라코나졸 또는 플루코나졸 (경구 테르비나핀·그리세오풀빈 무효, 경구 케토코나졸은 쓰지 않음)"}
  edges:
    - {from: start, to: koh}
    - {from: koh, to: extent, label: "있음"}
    - {from: koh, to: other, label: "없음"}
    - {from: koh, to: kohdo, label: "미시행"}
    - {from: kohdo, to: extent, label: "있으면"}
    - {from: kohdo, to: other, label: "없으면"}
    - {from: extent, to: topical, label: "예"}
    - {from: extent, to: extask, label: "정보 없음"}
    - {from: extent, to: oral, label: "광범위·재발·국소 실패"}
    - {from: extask, to: topical, label: "국한·첫 발병"}
    - {from: extask, to: oral, label: "광범위·재발"}
diagram_notes:
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

## 정의
어루러기(전풍)는 피부 상재 효모 **말라세지아**가 균사형으로 늘어나 생기는 표재성 감염이다. 피지가 많은 몸통 위쪽·목·위팔에 비늘 있는 저색소 또는 과색소 반점을 만든다.

## 병태생리
덥고 습한 환경, 땀, 기름진 피부에서 효모형이 균사형으로 바뀐다. 상재균이라 **재발이 흔하다** — 균을 없애도 다시 늘어날 조건이 남는다. 말라세지아는 지질을 요구해 일반 배양에서 잘 자라지 않는다.

## 기전에서 소견으로
- 균이 만드는 아젤라산이 멜라닌 합성을 억제 → 햇볕에 타도 그 부위만 하얗게 남는다(저색소).
- 각질층의 균 → 긁으면 미세한 비늘이 두드러진다.
- KOH 에서 짧은 균사와 둥근 포자 무리(「스파게티와 미트볼」). 우드등 형광은 일부에서만 보이는 보조 소견이다.

## 감별
- **백반증**: 비늘 없음, 완전 탈색, KOH 음성. 국소 타크로리무스가 쓰이는 쪽은 이것이다.
- **염증 후 저색소·백색 비강진·장미색 비강진·지루 피부염**: 분포·비늘·KOH 로 가른다.
- **체부백선**: 가장자리가 활동성인 고리 모양, 피부사상균 — 그리세오풀빈·테르비나핀이 듣는 쪽.

## 검사
KOH 검경이 핵심이다. 배양은 일상적으로 필요 없고, 일반 배지 음성은 오히려 합당하다.

## 치료
- **국한·첫 발병** → 국소 항진균제(아졸 크림·샴푸, 셀레늄 설파이드, 징크 피리치온).
- **광범위·재발·국소 실패** → 경구 이트라코나졸 또는 플루코나졸.
- 무효·금기: 경구 테르비나핀·그리세오풀빈(무효), 경구 케토코나졸(간독성으로 쓰지 않음), 국소 스테로이드(악화).
- 색 회복에 수개월 걸린다는 것을 미리 설명한다. 재발이 잦으면 예방적 국소제.

## 권고와 예외
- 국소제 사이의 상대 효과는 근거가 약하다 — 「가장 좋은 국소제」를 외울 필요는 없다.
- 경구 아졸의 용량·기간은 이 정리본에서 대조하지 않았다(검토 항목).
- 국내 교과서의 권고 문구는 대조하지 않았다(검토 항목).

## (심화) 치료 문항이 진단 문항처럼 보이는 이유
보기에 경쟁하는 치료(국소 vs 경구 아졸)가 없으면 문항은 사실상 「어루러기인가」만 묻게 된다. 이 정리본의 목표는 진단 다음 단계 — **범위·재발이 치료 수준을 바꾼다** — 이다.
