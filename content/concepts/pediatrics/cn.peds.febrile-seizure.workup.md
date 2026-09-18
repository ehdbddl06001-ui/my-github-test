---
id: cn.peds.febrile-seizure.workup
type: concept
topic: Pediatrics
see_also: [Neurology]
date: 2026-09-18
updated: 2026-09-18
version: 1
confidence: medium
review_status: unreviewed
title: "열성경련 뒤 — 추가 검사가 필요한 경우와 필요 없는 경우"
objective: "열과 함께 발작한 6~60개월 소아에서, 단순 열성경련의 조건과 수막염 위험 배경을 근거로 요추천자·뇌파·영상·항경련제가 필요한지 가른다"
objective_kind: 검사 선택
condition: 단순 열성경련
exams: [kmle, usmle]
summary:
  - "먼저 안정화와 발작 종료를 확인한다. 5분 넘게 이어지면 이 도식이 아니라 경련 지속 처치다."
  - "단순형 = 6~60개월, 15분 미만의 전신발작, 24시간 내 1회, 두개내 감염·대사 이상·무열성 경련 병력 없음."
  - "단순형이고 수막 자극·의식 저하·국소 이상이 없으면 뇌파·혈액검사·영상은 일상적으로 하지 않는다. 할 일은 발열 원인 평가·해열·보호자 교육."
  - "요추천자가 「선택지(option)」로 올라오는 배경: 6~12개월의 Hib·폐렴구균 접종 미완료·불명, 항생제 선행 투여. 문항에 이 정보가 없으면 「없음」으로 채우지 말고 확인할 항목으로 남긴다."
  - "정상 진찰(목경직 없음·대천문 편평·빠른 회복)은 수막염 가능성을 낮추는 의미 있는 음성 소견이다 — 정보를 버리는 게 아니다."
criteria:
  - id: sfs-definition
    name: 단순 열성경련의 정의
    kind: 정의(진단 범주)
    population: "생후 6~60개월 발열 소아"
    statement: "15분 미만의 전신발작이 24시간 동안 1회, 두개내 감염·대사 이상·무열성 경련 병력이 없을 것"
    exceptions: "초점 발작·15분 이상·24시간 내 재발 중 하나라도 있으면 복합 열성경련 — 이 기준을 적용하지 않는다"
    source: aap-2008
    basis: current
    exams: [kmle, usmle]
  - id: sfs-lp
    name: 요추천자 적응
    kind: 검사 권고(강도 구분)
    population: "단순 열성경련으로 온 6~60개월 소아"
    statement: "수막염을 시사하는 임상 징후·증상이 있으면 시행한다. 6~12개월에서 Hib·폐렴구균 접종이 부족하거나 확인할 수 없을 때, 그리고 항생제를 먼저 쓴 소아에서는 「선택지(option)」다"
    exceptions: "option 은 「해도 되고 안 해도 되는」 가장 약한 권고 — 일률적 시행 기준이 아니다"
    source: aap-2011
    basis: current
    exams: [kmle, usmle]
  - id: sfs-no-routine
    name: 일상적 검사 비권고
    kind: 검사 권고
    population: "단순 열성경련"
    statement: "뇌파·혈액검사·신경영상은 일상적으로 필요하지 않다. 발열의 원인을 찾는 데 주의를 둔다"
    exceptions: "복합형·국소 이상·의식 회복 지연은 이 권고의 대상이 아니다"
    source: aap-2011
    basis: current
    exams: [kmle, usmle]
  - id: sfs-no-prophylaxis
    name: 예방적 항경련제
    kind: 치료 권고
    population: "단순 열성경련을 한 번 이상 겪은 소아"
    statement: "지속적·간헐적 항경련제 예방 투여를 권하지 않는다(이득보다 부작용). 해열제는 재발을 막지 못한다"
    exceptions: "이 문서는 요약만 확인 — 세부 문구는 본문 대조 전"
    source: aap-2008
    basis: current
    exams: [kmle, usmle]
sources:
  - id: aap-2011
    org: "American Academy of Pediatrics, Subcommittee on Febrile Seizures"
    title: "Neurodiagnostic evaluation of the child with a simple febrile seizure"
    kind: guideline
    year: 2011
    citation: "Pediatrics 2011;127(2):389-394"
    doi: "10.1542/peds.2010-3318"
    pmid: "21285335"
    url: "https://doi.org/10.1542/peds.2010-3318"
    checked_at: 2026-09-18
    checked: "PubMed 초록의 권고 문구와 대조(요추천자 option 조건·일상 검사 비권고)"
  - id: aap-2008
    org: "American Academy of Pediatrics, Steering Committee on Quality Improvement and Management, Subcommittee on Febrile Seizures"
    title: "Febrile seizures: clinical practice guideline for the long-term management of the child with simple febrile seizures"
    kind: guideline
    year: 2008
    citation: "Pediatrics 2008;121(6):1281-1286"
    doi: "10.1542/peds.2008-0939"
    pmid: "18519501"
    url: "https://doi.org/10.1542/peds.2008-0939"
    checked_at: 2026-09-18
    checked: "PubMed 초록으로 정의 대조. 항경련제 권고 세부는 본문 대조 전"
diagram:
  title: "열과 함께 발작한 6~60개월 소아 — 추가 검사가 필요한가"
  nodes:
    - {id: start, kind: start, text: "열과 함께 발작한 6~60개월 소아"}
    - {id: abc, kind: decision, text: "기도·호흡·순환 확인. 발작이 멈췄는가?"}
    - {id: status, kind: alert, text: "5분 넘게 지속 — 경련 지속 처치(벤조디아제핀 등). 이 도식 범위 밖"}
    - {id: cns, kind: decision, text: "의식이 빨리 돌아오고 수막 자극 징후·국소 신경학적 이상이 없는가?"}
    - {id: cnswork, kind: end, text: "중추신경계 감염·구조적 원인 평가 — 요추천자·영상 등"}
    - {id: simple, kind: decision, text: "단순형인가? 전신발작 · 15분 미만 · 24시간 내 1회"}
    - {id: complex, kind: alert, text: "복합 열성경련 — 개별 평가(이 도식은 단순형만 다룬다)"}
    - {id: risk, kind: decision, text: "요추천자를 고려하게 하는 배경이 있는가? 6~12개월 Hib·폐렴구균 접종 미완료·불명 / 항생제 선행 투여"}
    - {id: ask, kind: info, text: "보호자에게 접종력·최근 항생제를 확인한다 — 확인 전에는 「없음」으로 단정하지 않는다"}
    - {id: lp, kind: end, text: "요추천자는 선택지(option)로 고려"}
    - {id: home, kind: end, text: "추가 검사 없이 발열 원인 평가·해열·보호자 교육. 뇌파·혈액검사·영상·예방적 항경련제는 일상적으로 하지 않는다"}
  edges:
    - {from: start, to: abc}
    - {from: abc, to: status, label: "5분 넘게 지속"}
    - {from: abc, to: cns, label: "멈춤"}
    - {from: cns, to: cnswork, label: "아니오"}
    - {from: cns, to: simple, label: "예"}
    - {from: simple, to: complex, label: "아니오"}
    - {from: simple, to: risk, label: "예"}
    - {from: risk, to: lp, label: "해당"}
    - {from: risk, to: ask, label: "정보 없음"}
    - {from: risk, to: home, label: "해당 없음 확인"}
    - {from: ask, to: lp, label: "해당하면"}
    - {from: ask, to: home, label: "해당 없으면"}
checks:
  - q: "단순 열성경련의 네 조건은?"
    a: "6~60개월, 15분 미만, 전신발작, 24시간 내 1회(+ 두개내 감염·대사 이상·무열성 경련 병력 없음)."
  - q: "단순 열성경련에서 요추천자가 「선택지」가 되는 두 배경은?"
    a: "6~12개월에서 Hib·폐렴구균 접종 미완료 또는 확인 불가, 그리고 항생제 선행 투여. 수막염 징후가 있으면 선택지가 아니라 시행한다."
  - q: "문항에 접종력이 적혀 있지 않다. 「접종 완료」로 보고 풀어도 되는가?"
    a: "아니다. 정보 없음은 음성이 아니다. 다만 18개월처럼 6~12개월 범위 밖이면 접종 항목은 요추천자 고려 조건 자체에 해당하지 않는다 — 나이부터 본다."
variants:
  - id: v1
    context: "같은 목표, 다른 맥락 — 접종력 불명·항생제 선행 투여가 있는 10개월 영아"
    stem: "10개월 남아가 39.2 ℃ 발열과 함께 1분간 온몸을 떠는 발작을 한 뒤 응급실에 왔다. 발작은 저절로 멈췄고 지금은 깨어 엄마를 알아본다. 해외에서 태어나 예방접종 기록을 확인할 수 없다. 이틀 전부터 다른 병원에서 받은 경구 아목시실린을 먹고 있다. 목경직은 없고 국소 신경학적 이상은 없다. 다음 중 고려해야 할 검사로 가장 적절한 것은?"
    choices: ["A. 추가 검사 없이 귀가", "B. 요추천자", "C. 뇌 자기공명영상", "D. 뇌파검사", "E. 혈청 칼슘·마그네슘 검사"]
    answer: "B"
    explanation: "단순 열성경련의 형태지만 6~12개월에 접종력을 확인할 수 없고 항생제를 먼저 먹었다. 항생제는 수막염의 징후를 가릴 수 있어, 두 배경 모두 요추천자를 「선택지」로 올린다(AAP 2011). 뇌파·영상·전해질은 여전히 일상 검사가 아니다."
    kind: application
---

## 정의
열성경련은 생후 6~60개월 소아가 발열 중에 두개내 감염·대사 이상 없이 겪는 발작이다. **단순형**은 15분 미만의 전신발작이 24시간 동안 한 번이고, 하나라도 벗어나면(초점성·15분 이상·24시간 내 재발) **복합형**이다. 단순형이라는 판정은 「검사를 덜 해도 되는 집단」이라는 뜻이라, 조건을 하나씩 확인하는 과정이 곧 검사 결정이다.

## 병태생리
발달 중인 뇌는 체온 상승에 대한 발작 역치가 낮다. 유전 소인이 있어 가족력이 흔하다. 단순형은 뇌 손상을 남기지 않고 지능·행동 발달에 영향이 없으며, 이후 뇌전증 위험은 일반 인구보다 약간 높은 정도다.

## 기전에서 소견으로
- 열이 오르는 초기에 짧은 전신발작 → 곧 멈추고 의식이 빠르게 돌아온다.
- 발작의 원인이 뇌 자체가 아니므로 발작 뒤 신경학적 진찰은 정상이다. **국소 결손이 남거나 의식 회복이 늦으면** 원인이 뇌에 있을 가능성(감염·구조 이상)을 먼저 본다.
- 수막염도 열과 발작을 함께 일으킨다. 그래서 목경직·대천문 팽창·처짐 같은 수막 징후의 **유무**가 결정적이다 — 없다는 확인도 판단 근거다.

## 감별
- **세균성 수막염·뇌염**: 수막 자극 징후, 의식 회복 지연, 처짐·보챔 지속. 항생제를 먼저 먹었으면 징후가 가려질 수 있다.
- **복합 열성경련**: 초점성·15분 이상·24시간 내 재발 — 개별 평가.
- **오한(rigor)·열성 섬망**: 의식이 유지되고 리듬 있는 강직·간대가 아니다.
- **전해질 이상·저혈당에 의한 발작**: 구토·설사·섭취 부족의 병력, 회복이 더딤.

## 검사
- 단순형이면서 수막 징후·국소 이상이 없으면 **뇌파·혈액검사·신경영상은 일상적으로 하지 않는다**. 재발이나 뇌전증 예측에 도움이 되지 않는다.
- 혈액·소변 검사는 **발열 원인**을 찾기 위해 필요할 때만 한다(경련 때문이 아니다).
- 요추천자: 수막염 징후가 있으면 시행. 6~12개월의 접종 미완료·불명, 항생제 선행 투여에서는 선택지.

## 치료
- 발작이 멈췄으면 발열 원인 치료, 해열·수분, 보호자 교육(재발 가능성, 발작 시 옆으로 눕히기, 5분 넘으면 119).
- **예방적 항경련제는 권하지 않는다**. 해열제는 편안함을 위한 것이고 재발을 막지는 못한다.
- 발작이 5분 넘게 이어지면 경련 지속으로 보고 벤조디아제핀 처치 — 이 정리본의 범위 밖.

## 권고와 예외
- 이 정리본의 권고는 **단순형**에만 해당한다. 복합형은 영상·뇌파 결정이 달라질 수 있다.
- 요추천자의 「option」은 가장 약한 권고 강도다. 시험 문항이 「가장 적절한」을 물을 때는 보기 안의 다른 선택지와 비교해 판단한다.
- 국내 교과서·국시에서도 같은 정의(6개월~5세, 15분, 전신, 24시간 1회)를 쓴다. 국내 지침 원문은 이 정리본에서 대조하지 않았다(검토 항목).

## (심화) 왜 「정보 없음」을 음성으로 채우면 안 되는가
접종력·항생제 복용이 문항에 없을 때 「없음」으로 채우면 요추천자 판단의 한 갈래를 조용히 지운다. 시험 문항은 대개 그 정보를 주지 않아 단순형 원칙대로 답하게 설계되지만, 실제 진료에서는 **확인할 항목**이다. 이 구분이 도식의 「추가 정보 필요」 경로다. 18개월 이상이면 접종 항목은 요추천자 고려 조건 자체에 해당하지 않는다 — 나이 조건을 먼저 본다.
