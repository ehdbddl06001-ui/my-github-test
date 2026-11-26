---
id: cn.cardio.rv-infarction.avoid-preload-reduction
type: concept
topic: Cardiology
date: 2026-11-26
updated: 2026-11-26
version: 1
outline: h275
confidence: medium
review_status: unreviewed
note_form: 2
title: "우심실 경색 — 전부하에 기대니 질산염을 피한다"
objective: "하벽 ST 분절 상승 심근경색에 동반된 우심실 경색을 알아보고, 전부하를 떨어뜨리는 질산염을 피해야 할 약으로 골라 수액 · 항혈전제 · 재관류와 가른다"
objective_kind: 금기
condition: 우심실 경색(right ventricular infarction)
exams: [kmle, usmle]
summary:
  - "결론: 하벽 경색 + 저혈압 + 목정맥 확장 + 맑은 폐면 우심실 경색 — 니트로글리세린을 피하고 수액으로 전부하를 지킨다."
  - "시험 단서: II · III · aVF ST 상승에 V4R ST 상승, 폐 수포음 · 폐울혈 없음 — RV infarction with inferior STEMI."
  - "왜: 다친 우심실은 들어온 피만큼만 내보내므로 정맥을 넓혀 전부하를 줄이면 좌심 충만과 혈압이 함께 떨어진다."
  - "쓰지 않는 약: 질산염 · 이뇨제, 수축기 혈압 < 90 mmHg 면 질산염 금기."
pitfalls:
  - contrast: "클로피도그렐 부하 용량 — 저혈압이니 항혈소판제도 피해야?"
    point: "P2Y12 억제제는 혈압 · 전부하에 영향을 주지 않고 아스피린에 더해 사망 · 재경색을 줄이는 ST 분절 상승 심근경색의 기본 치료다 [[harrison-22: 286장 p.2121]]. 피할 것은 혈관을 넓혀 전부하를 줄이는 약이다."
    cites: ["harrison-22: 286장 p.2121"]
    covers: ["kmle-2026-1957:C"]
  - contrast: "목정맥 확장 = 수액 과다?"
    point: "우심실 경색의 목정맥 확장은 우심실이 피를 앞으로 보내지 못해 생긴 것이고 폐는 맑다. 치료는 오히려 수액으로 우심실 전부하를 유지하는 것이다 [[harrison-22: 286장 p.2123]]."
    exception: "폐 수포음 · 폐울혈이 뚜렷한 좌심부전이 저혈압의 원인이면 수액을 조심한다."
    cites: ["harrison-22: 286장 p.2123"]
tables:
  - id: hypotension
    section: "가르는 소견 — 하벽 경색 저혈압의 원인"
    title: "목정맥 · 폐 소견으로 저혈압 원인을 가른다"
    role: comparison
    span: full
    columns: ["원인", "목정맥 · 폐", "처치"]
    rows:
      - ["우심실 경색", "목정맥 확장 · 폐 맑음 · V4R ST 상승", "수액 · 재관류, 질산염 금기"]
      - ["좌심부전 · 심인성 쇼크", "폐 수포음 · 폐울혈", "수액 조심 · 재관류 · 순환 보조"]
      - ["저혈량", "목정맥 납작 · 폐 맑음", "조심스러운 수액"]
      - ["미주신경 항진(서맥)", "서맥 · 저혈압, 다리 올리면 회복", "아트로핀"]
    note: "하벽 경색은 부교감 항진으로 서맥 · 저혈압을 보일 수 있다 [[harrison-22: 286장 p.2115]]."
diagram:
  title: "하벽 경색의 저혈압 — 피할 약 고르기"
  nodes:
    - {id: start, kind: start, text: "하벽 ST 분절 상승 심근경색"}
    - {id: info, kind: info, text: "혈압 · 목정맥 · 폐 소리 · 흉부 X선 · V4R"}
    - {id: sbp, kind: decision, text: "수축기 혈압 < 90 mmHg?"}
    - {id: rv, kind: decision, text: "목정맥 확장 + 맑은 폐 + V4R ST 상승?"}
    - {id: rvtx, kind: end, text: "우심실 경색 — 수액 · 재관류, 질산염 금기"}
    - {id: lung, kind: decision, text: "폐 수포음 · 폐울혈?"}
    - {id: lvtx, kind: end, text: "좌심부전 — 수액 조심 · 재관류"}
    - {id: hypo, kind: end, text: "저혈량 · 미주 항진 — 수액 · 아트로핀"}
    - {id: ntg, kind: end, text: "흉통에 질산염 가능 · 재관류"}
  edges:
    - {from: start, to: info}
    - {from: info, to: sbp}
    - {from: sbp, to: ntg, label: "아니오"}
    - {from: sbp, to: rv, label: "예"}
    - {from: rv, to: rvtx, label: "예"}
    - {from: rv, to: lung, label: "아니오"}
    - {from: lung, to: lvtx, label: "있음"}
    - {from: lung, to: hypo, label: "없음"}
diagram_notes:
  - "혈압이 정상이어도 우심실 경색이 의심되면(하벽 경색 · 목정맥 확장 · 맑은 폐) 질산염을 피한다."
  - "24시간 안에 PDE-5 억제제를 먹었으면 질산염을 주지 않는다."
  - "모르핀도 정맥 고임으로 혈압을 떨어뜨리고 하벽 경색에서 서맥 · 방실차단을 부를 수 있다."
checks:
  - q: "우심실 경색에서 질산염이 혈압을 떨어뜨리는 이유는?"
    a: "정맥을 넓혀 우심실로 돌아오는 피(전부하)를 줄인다. 수축이 약해진 우심실은 들어온 만큼만 보내므로 좌심 충만 · 심박출 · 혈압이 함께 떨어진다."
  - q: "하벽 경색에서 우심실 경색을 의심하게 하는 진찰 · 심전도 소견은?"
    a: "목정맥 확장(쿠스마울 징후) · 맑은 폐 · 저혈압, 오른쪽 가슴 유도 V4R 의 ST 상승."
sources:
  - id: harrison-22
    org: "McGraw Hill"
    title: "Harrison's Principles of Internal Medicine, 22nd ed."
    kind: textbook
    year: 2025
    citation: "Loscalzo J, Fauci AS, Kasper DL, et al (eds). Harrison's Principles of Internal Medicine, 22e. 286장 ST-Segment Elevation Myocardial Infarction p.2113–2126"
    checked_at: 2026-11-26
    checked: "본문 대조(드라이브 문서 H22_286) — p.2115 하벽 경색의 부교감 항진(서맥 · 저혈압); p.2118 수축기 < 90 mmHg 또는 우심실 경색 의심(하벽 경색 · 목정맥 압력 상승 · 맑은 폐 · 저혈압)이면 질산염을 피함, 24시간 내 PDE-5 억제제면 금기, 모르핀의 정맥 고임 · 하벽 경색 서맥; p.2121 아스피린에 클로피도그렐을 더하면 사망 · 재경색 · 뇌졸중 감소, 일차 PCI 에 미분획 헤파린; p.2123 하벽 경색의 약 1/3 에 우심실 괴사, 목정맥 확장 · 쿠스마울 징후, V4R ST 상승, 치료는 우심실 전부하 유지를 위한 수액"
    verified: text
kr_diffs_skip: [diff.cardio.acs.dapt-12-months, diff.cardio.acs.ace-inhibitor-indication, diff.cardio.acs.mra-indication, diff.cardio.acs.beta-blocker-preserved-ef]
variants:
  - id: v1
    of: kmle-2026-1957
    flip: true
    changed: "목정맥 확장 · 맑은 폐 · V4R ST 상승 → 양쪽 폐 수포음 · 흉부 X선 폐부종, V4R 정상 — 좌심부전 쪽 저혈압이라 피할 것이 생리식염수 대량 주입이 된다"
    context: "하벽 경색 저혈압이지만 폐울혈이 뚜렷한 경우"
    stem: "71세 여자가 2시간 전 시작된 가슴 통증과 숨참으로 응급실에 왔다. 혈압 86/54 mmHg, 맥박 108회/분, 호흡 28회/분, 산소포화도 88 %(실내 공기). 목정맥은 확장되어 있지 않고 양쪽 폐 아래 절반에서 수포음이 들린다. 12유도 심전도에서 II · III · aVF ST 분절이 상승했고 V4R 은 정상이다. 흉부 X선에서 양쪽 폐부종이 보인다. 심도자실을 준비하고 있다. 이 환자에게 피해야 하는 것은?"
    choices: ["A. 생리식염수 2 L 급속 정맥 주입", "B. 아스피린 씹어 먹기", "C. 클로피도그렐 부하 용량", "D. 미분획 헤파린 정맥 주사", "E. 일차 경피적 관상동맥 중재술"]
    answer: "A"
    explanation: "원 문항은 목정맥 확장 · 맑은 폐 · V4R ST 상승으로 우심실 경색이어서 수액이 치료이고 질산염이 금기였다. 여기서는 폐 수포음 · 폐부종 · 저산소증이 좌심 기능 저하를 말하므로 대량 수액은 폐부종을 악화시킨다. 항혈소판제 · 헤파린 · 일차 중재술은 그대로 필요하다."
    kind: application
  - id: v2
    of: kmle-2026-1957
    flip: false
    changed: "67세 남자 → 59세 여자, 흡연력, 검사 제시 순서를 바꿈 — 하벽 경색 + V4R ST 상승 + 목정맥 확장 + 맑은 폐 + 저혈압은 그대로라 피할 약은 니트로글리세린"
    context: "하벽 경색 + 우심실 경색 양상의 59세 여자"
    stem: "59세 여자가 40분 전부터 명치가 짓눌리고 메스꺼워 119로 왔다. 30년 동안 하루 한 갑씩 담배를 피웠다. 혈압 82/50 mmHg, 맥박 54회/분, 호흡 18회/분, 산소포화도 97 %(실내 공기). 오른쪽 가슴 유도 심전도에서 V4R ST 분절이 1.5 mm 상승했고, 12유도 심전도에서는 II · III · aVF ST 분절이 상승했다. 목정맥이 숨을 들이쉴 때 더 부풀고 폐 소리는 깨끗하다. 흉부 X선에 폐울혈이 없다. 아스피린을 먹게 했다. 이 환자에게 투여를 피해야 하는 것은?"
    choices: ["A. 생리식염수 정맥 주입", "B. 클로피도그렐 부하 용량", "C. 니트로글리세린 설하 투여", "D. 미분획 헤파린 정맥 주사", "E. 일차 경피적 관상동맥 중재술"]
    answer: "C"
    explanation: "나이 · 성별 · 제시 순서가 달라도 하벽 경색에 V4R ST 상승 · 목정맥 확장(쿠스마울 징후) · 맑은 폐 · 저혈압이 겹친 우심실 경색이다. 우심실 박출이 전부하에 기대므로 정맥을 넓히는 니트로글리세린을 피하고 수액으로 전부하를 지키며 재관류한다."
    kind: application
figures_none: "금기 약 고르기 — 시험 단서는 진찰(목정맥 · 폐)과 V4R 이고, 그림이 판단을 더하지 않는다"
---

## 판단 — 왜 니트로글리세린을 피하는가
- 수축기 혈압 < 90 mmHg 이거나 우심실 경색이 의심되면(하벽 경색 · 목정맥 압력 상승 · 맑은 폐 · 저혈압) 질산염을 피한다 [[harrison-22: 286장 p.2118]].
- 우심실 경색의 치료는 우심실 전부하를 지키는 수액이다 — 목정맥 확장은 수액을 막을 이유가 아니다 [[harrison-22: 286장 p.2123]].
- 아스피린 · P2Y12 억제제 · 미분획 헤파린 · 일차 중재술은 혈압과 무관하게 그대로 한다 [[harrison-22: 286장 p.2121]].

## 기전 — 다친 우심실은 전부하에 기댄다
우관상동맥 근위부가 막히면 하벽과 함께 우심실이 다친다. 하벽 경색의 약 1/3 에 우심실 괴사가 있다 [[harrison-22: 286장 p.2123]]. 수축이 약해진 우심실은 정맥으로 돌아온 피만큼만 폐로 보낼 수 있어 오른쪽에는 피가 고이고(목정맥 확장 · 쿠스마울 징후 · 간 비대), 왼쪽은 덜 차서 심박출과 혈압이 떨어지며 폐는 맑다. 질산염 · 이뇨제 · 모르핀처럼 정맥을 넓히거나 혈액량을 줄이는 약은 이 전부하를 더 빼앗아 혈압을 무너뜨린다.

## 가르는 소견 — 하벽 경색 저혈압의 원인
- 오른쪽 가슴 유도, 특히 V4R 의 ST 상승은 첫 24시간에 흔하다 — 하벽 경색이면 V4R 을 찍는다 [[harrison-22: 286장 p.2123]].
- 폐 수포음 · 흉부 X선 폐울혈이 있으면 좌심부전 쪽이고, 그때는 수액을 조심한다.
- 하벽 경색 초기의 서맥 · 저혈압은 부교감 항진일 수 있다 [[harrison-22: 286장 p.2115]].

## 권고와 예외
- 24시간 안에 PDE-5 억제제를 먹은 환자에게는 질산염을 주지 않는다 [[harrison-22: 286장 p.2118]].
- 우심실 경색에 완전 방실차단이 오면 심방 수축의 몫을 잃어 심실 조율에 잘 반응하지 않는다 [[harrison-22: 286장 p.2125]].

## 시험 쟁점 — 충돌·맥락·새 근거
- 해당 없음(대조: 해리슨 22판 286장 p.2115~2125)
