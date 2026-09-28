---
id: cn.cardio.aortic-dissection.impulse-control-first
type: concept
topic: Cardiology
see_also: [Emergency Medicine, Thoracic Surgery]
date: 2026-09-23
updated: 2026-09-28
version: 3
outline: h280            # 기본틀 슬롯(content/outline/subjects.yaml)
confidence: medium
review_status: unreviewed
note_form: 2            # 판형 2(2026-09-25) — 결론·시험 단서·왜 → 혼동 → 표·도식 → 목표에 맞춘 본문
title: "급성 대동맥박리 — 혈압보다 심박수·수축력을 먼저"
objective: "급성 대동맥박리에서 저혈압이 없으면 정맥 베타차단제로 심박수·수축력(dP/dt)을 먼저 낮추고, 혈관확장제는 그 뒤에 더하며, 혈전용해·항혈전제는 피하는 순서를 판단한다"
objective_kind: 치료
condition: 급성 대동맥박리(acute aortic dissection)
exams: [kmle, usmle]
summary:
  - "결론: 저혈압 없는 급성 대동맥박리의 첫 약물은 정맥 베타차단제(심박 약 60회/분) — 혈관확장제는 그 뒤에 더한다."
  - "시험 단서: 찢어지는 흉통이 등으로 이동 + 양팔 혈압차·새 이완기 잡음 = 급성 대동맥박리(acute aortic dissection)."
  - "왜: 박리를 넓히는 힘은 혈압 숫자보다 dP/dt·심박수다 — 혈관확장제 단독은 반사 빈맥으로 그 힘을 키운다."
  - "쓰지 않는다: 혈전용해·항혈소판·항응고(벽 안 출혈·파열), 고혈압 박리의 수액 부하, 하이드랄라진 단독."
  - "확정 치료는 Stanford 분류가 정한다 — A형 응급 수술, 합병증 없는 B형 약물, 합병증 있는 B형 스텐트그라프트."
pitfalls:
  - contrast: "「급성 흉통 = 관동맥 재관류(혈전용해·항혈소판)」 반사 vs 대동맥박리"
    point: "혈전용해제·이중 항혈소판제·항응고제는 관동맥 혈전이 원인일 때의 치료다. 박리에서는 가짜 내강·벽 안으로의 출혈을 키우고 파열·심낭 혈종을 조장한다. 흉통 환자에서 재관류 치료 전에 박리 단서(통증의 이동·맥박/혈압 비대칭·이완기 잡음·종격동 확장)를 먼저 걸러야 하는 이유다."
    exception: "박리가 관상동맥 입구(주로 우관상동맥)를 침범해 ST 상승이 함께 나올 수 있다 — 이때도 혈전용해가 아니라 수술이 답이다."
    cites: ["harrison-21", "?acc-aha-aortic-2022"]
    covers: ["kmle-2026-0555:C", "kmle-2026-0555:D"]
  - contrast: "니트로프루시드(혈관확장제)를 먼저 vs 베타차단제를 먼저"
    point: "혈관확장제만 먼저 주면 압력은 내려가도 반사 교감 흥분으로 심박수·수축력이 올라 dP/dt 가 커진다. 순서는 「베타차단 → 필요하면 혈관확장」이다."
    exception: "베타차단제 금기(심한 천식·고도 방실차단 등)면 정맥 딜티아젬·베라파밀이 심박 조절을 대신할 수 있다 [[harrison-21: 280장 p.2106]]."
    cites: ["harrison-21"]
    covers: ["kmle-2026-0555:A"]
  - contrast: "「혈압을 지키려고」 수액 부하"
    point: "혈압이 높거나 정상인 박리 환자에게 수액을 빠르게 주면 박동압과 전단응력을 키운다. 수액·승압은 저혈압(심낭압전·파열·심한 대동맥판 역류)을 동반한 경우의 소생 처치이고, 그때는 약물 조절보다 응급 수술이 우선이다."
    cites: ["harrison-21"]
    covers: ["kmle-2026-0555:E"]
criteria:
  - id: ad-targets-harrison
    name: 초기 약물 목표(해리슨)
    kind: 치료 기준
    population: "저혈압이 없는 급성 대동맥박리"
    statement: "정맥 베타차단제로 심박 약 60회/분, 이어 니트로프루시드로 수축기압 ≤120 mmHg. 라베탈롤 단독도 가능"
    exceptions: "저혈압이면 적용하지 않는다. 베타차단제를 쓸 수 없으면 정맥 베라파밀·딜티아젬"
    source: harrison-21
    locator: "280장 p.2105–2106 Treatment: Aortic Dissection"
    basis: current
    exams: [kmle, usmle]
  - id: ad-surgery-harrison
    name: 확정 치료(해리슨)
    kind: 치료 기준
    population: "급성 대동맥박리·벽내 혈종"
    statement: "A형(상행 침범)은 응급·긴급 수술. 합병증 없는 B형은 약물 치료, 합병증 있는 B형은 흉부 혈관내 스텐트그라프트(불가능하면 수술)"
    exceptions: "B형의 합병증 = 진행, 주요 분지 혈류 장애, 파열 임박, 지속 통증"
    source: harrison-21
    locator: "280장 p.2106"
    basis: current
    exams: [kmle, usmle]
sources:
  - id: harrison-21
    org: "McGraw Hill"
    title: "Harrison's Principles of Internal Medicine, 21st ed. — Chapter 280: Diseases of the Aorta"
    kind: textbook
    year: 2022
    citation: "Loscalzo J, Kasper DL, Longo DL, et al (eds). Harrison's Principles of Internal Medicine, 21e. 280장 p.2101–2106"
    checked_at: 2026-09-23
    checked: "본문 대조(드라이브 문서, 280장 p.2104–2106) — 박리 기전(내막 파열·가짜 내강, 박동 흐름이 층을 따라 박리), Stanford A/B 분류, 고혈압 동반 70 %, 찢어지는 이동성 통증·맥박 소실·대동맥판 역류(근위 박리의 50 % 이상)·신경 결손, 허혈 없는 심전도가 심근경색 감별에 도움, 경식도 심초음파·CT·MRI 의 정확도, 치료(저혈압이 없으면 정맥 베타차단제로 심박 ~60, 니트로프루시드로 수축기 ≤120, 라베탈롤 가능, 베타차단제 불가 시 베라파밀·딜티아젬, 직접 혈관확장제 단독 금기), A형 수술·B형 약물/합병증 시 TEVAR 서술을 확인했다"
    verified: text
  - id: acc-aha-aortic-2022
    org: "American College of Cardiology / American Heart Association"
    title: "2022 ACC/AHA Guideline for the Diagnosis and Management of Aortic Disease"
    kind: guideline
    year: 2022
    citation: "Isselbacher EM, Preventza O, Hamilton Black J 3rd, et al. Circulation 2022;146(24):e334–e482"
    doi: "10.1161/CIR.0000000000001106"
    pmid: "36322642"   # 2026-09-25 PubMed esearch 로 DOI 확인·제목 일치
    checked_at: 2026-09-23
    checked: "서지만 — 루틴 컨테이너의 네트워크 정책이 ahajournals·PubMed 접근을 막아 권고 본문·수치 목표를 대조하지 못했다"
    verified: citation
tables:
  - id: ddx
    section: "가르는 소견 — 재관류 치료 전에 박리를 거른다"
    title: "급성 흉통에서 박리를 가리키는 소견과 그 이유"
    role: differential
    span: full
    columns: ["소견", "생기는 이유", "박리 외에 흔한 원인", "근거"]
    rows:
      - ["갑작스러운 찢어지는 통증, 등·어깨뼈 사이로 이동", "박리가 벽을 따라 진행하는 만큼 통증 위치가 옮겨 간다", "심근경색은 점차 심해지고 이동하지 않는 압박감", "[[harrison-21: 280장 p.2105]]"]
      - ["양팔 혈압차·맥박 소실", "가짜 내강·박리막이 분지(쇄골하·경동맥) 입구를 막는다", "쇄골하동맥 협착, 대동맥 축착", "[[harrison-21: 280장 p.2105]]"]
      - ["새 이완기 잡음(대동맥판 역류)", "근위 박리가 판륜을 넓히거나 판엽 지지를 무너뜨린다(근위 박리의 50 % 이상)", "만성 대동맥판 역류, 감염심내막염", "[[harrison-21: 280장 p.2105]]"]
      - ["편마비·하반신마비·장 허혈·혈뇨", "경동맥·척수·내장 분지의 혈류 차단", "뇌졸중·장간막 허혈 단독", "[[harrison-21: 280장 p.2105]]"]
      - ["허혈 소견 없는 심전도, 정상 트로포닌", "관상동맥을 침범하지 않은 박리", "허혈 없는 흉통(폐색전증·심낭염 등)", "[[harrison-21: 280장 p.2105]]"]
    note: "드물게 박리가 관상동맥 입구를 침범해 심근경색이 동반된다 — ST 상승이 있어도 박리 단서가 있으면 영상으로 먼저 확인한다 [[harrison-21: 280장 p.2105]]."
  - id: drugs
    section: "선택 — 무엇을 어떤 순서로"
    title: "급성 박리의 약물 — 역할과 순서"
    role: treatment
    span: full
    columns: ["약물", "순서·역할", "목표·주의", "근거"]
    rows:
      - ["정맥 베타차단제(에스몰롤·메토프롤롤·프로프라놀롤)", "첫 약물 — 심박수·수축력을 낮춰 dP/dt 감소", "심박 약 60회/분. 저혈압이면 쓰지 않는다", "[[harrison-21: 280장 p.2106]]"]
      - ["라베탈롤", "α·β 차단을 한 약으로 — 첫 약물로 가능", "베타차단 효과가 먼저 확보되는지 확인", "[[harrison-21: 280장 p.2106]]"]
      - ["니트로프루시드", "베타차단 뒤 추가 — 압력을 더 낮춘다", "수축기 ≤120 mmHg. 단독 투여 금지", "[[harrison-21: 280장 p.2106]]"]
      - ["정맥 베라파밀·딜티아젬", "베타차단제를 쓸 수 없을 때 심박 조절 대안", "음성 변력 작용 확인", "[[harrison-21: 280장 p.2106]]"]
      - ["하이드랄라진 등 직접 혈관확장제 단독", "금기", "반사 빈맥으로 전단응력 증가 → 박리 확장", "[[harrison-21: 280장 p.2106]]"]
      - ["혈전용해제·이중 항혈소판·항응고", "쓰지 않는다", "벽 안 출혈·파열·심낭 혈종 위험", "[[?acc-aha-aortic-2022]]"]
    note: "통증 조절(마약성 진통제)도 교감 흥분을 줄여 같은 목표에 기여한다 [[?acc-aha-aortic-2022]]."
diagram:
  title: "급성 흉통에서 박리 의심 — 첫 약물에서 확정 치료까지"
  nodes:
    - {id: start, kind: start, text: "갑작스러운 심한 흉·배부 통증 → 양팔 혈압·맥박·잡음·신경, 심전도"}
    - {id: suspect, kind: decision, text: "박리 단서(이동성 통증·혈압차·잡음·신경 결손)?"}
    - {id: acs, kind: end, text: "박리 단서 없음 + 허혈 심전도 — 급성 관동맥증후군 경로"}
    - {id: hypo, kind: decision, text: "저혈압·쇼크가 있는가?"}
    - {id: shock, kind: alert, text: "소생 + 응급 수술 — 강압 약물 조절은 하지 않는다"}
    - {id: bb, kind: step, text: "정맥 베타차단제 먼저(심박 약 60회/분) + 통증 조절"}
    - {id: vd, kind: step, text: "수축기 >120 mmHg 남으면 니트로프루시드 추가"}
    - {id: info, kind: info, text: "영상 확인·분류 — CT 혈관조영 또는 경식도 심초음파"}
    - {id: type, kind: decision, text: "상행대동맥 침범(Stanford A)?"}
    - {id: surgery, kind: end, text: "A형 — 응급·긴급 수술(인조혈관 치환, 필요 시 판막)"}
    - {id: comp, kind: decision, text: "B형 — 합병증이 있는가?"}
    - {id: tevar, kind: end, text: "합병증 있는 B형 — 혈관내 스텐트그라프트(불가하면 수술)"}
    - {id: medical, kind: end, text: "합병증 없는 B형 — 약물 유지, 6–12개월마다 CT·MRI"}
  edges:
    - {from: start, to: suspect}
    - {from: suspect, to: acs, label: "없음"}
    - {from: suspect, to: hypo, label: "있음"}
    - {from: hypo, to: shock, label: "저혈압"}
    - {from: hypo, to: bb, label: "정상·고혈압"}
    - {from: bb, to: vd}
    - {from: vd, to: info}
    - {from: info, to: type}
    - {from: type, to: surgery, label: "침범"}
    - {from: type, to: comp, label: "비침범"}
    - {from: comp, to: tevar, label: "있음"}
    - {from: comp, to: medical, label: "없음"}
diagram_notes:
  - "약물 조절은 영상 확인을 기다리지 않는다 — 진단을 의심하는 순간 시작한다 [[harrison-21: 280장 p.2105]]. 중환자실에서 혈역학을 감시한다."
  - "박리 단서 = 이동하는 찢어지는 통증 · 맥박/혈압 비대칭 · 새 이완기 잡음 · 신경 결손(가르는 소견 표)."
  - "「박리 단서 없음」 갈래에서도 관상동맥 입구를 침범한 박리가 ST 상승으로 보일 수 있다 — 단서가 하나라도 있으면 재관류 전에 영상을 먼저 본다."
  - "저혈압·쇼크는 심낭압전·파열·심한 대동맥판 역류를 뜻할 수 있다 — 그래서 심박·수축력을 낮추는 약을 쓰지 않는다."
  - "니트로프루시드는 베타차단 뒤에만 — 단독 투여 금지(선택 표)."
  - "영상 선택 — 안정 시 CT 혈관조영, 불안정 시 경식도 심초음파."
  - "B형의 합병증 = 진행 · 분지 폐쇄 · 파열 임박 · 지속 통증."
  - "목표 수치(심박 약 60·수축기 ≤120)는 해리슨 기준이다. 지침의 세부 목표는 본문 미대조(†)."
checks:
  - q: "혈압이 높은 급성 박리에서 니트로프루시드를 먼저 쓰지 않고 베타차단제를 먼저 쓰는 이유는?"
    a: "혈관확장만 하면 반사 교감 흥분으로 심박수·수축력이 올라 압력 상승 속도(dP/dt)와 전단응력이 커진다. 베타차단으로 그 반사를 먼저 막아야 혈관확장이 안전해진다."
  - q: "박리 환자에게 혈전용해제가 해로운 이유를 기전으로 설명하라."
    a: "박리는 혈전이 아니라 벽이 갈라진 병이다. 혈전용해는 가짜 내강·벽 안으로의 출혈을 키워 파열·심낭 혈종·압전을 부른다."
  - q: "박리 환자가 혈압 78/40 mmHg 로 왔다. 베타차단제를 먼저 주지 않는 이유와 할 일은?"
    a: "저혈압은 심낭압전·파열·심한 대동맥판 역류를 뜻할 수 있어, 심박·수축력을 낮추는 약은 쇼크를 악화시킨다. 소생과 함께 응급 수술로 간다."
variants:
  - id: v1
    of: kmle-2026-0555
    flip: true
    changed: "양팔 혈압차·이완기 잡음·이동성 통증 → 박리 단서 없이 압박성 흉통과 하벽 ST 상승, 경피적 관동맥중재 불가(이송 2시간 이상) ⇒ 정답이 베타차단제에서 혈전용해제로"
    context: "같은 흉통, 박리 단서가 없고 재관류가 급한 경우"
    stem: "60세 남자가 1시간 전 시작된 가슴을 짓누르는 통증으로 섬 지역 보건의료원에 왔다. 통증은 이동하지 않고 왼팔로 뻗친다. 혈압 오른팔 142/84, 왼팔 138/82 mmHg, 맥박 88회/분, 호흡 20회/분, 체온 36.7 ℃. 심잡음은 없고 사지 맥박은 대칭이다. 심전도에서 Ⅱ·Ⅲ·aVF 에 ST 분절 상승이 있다. 흉부 X선의 종격동 폭은 정상이다. 경피적 관동맥중재가 가능한 병원까지 이송에 2시간 이상 걸리며, 출혈 병력이나 최근 수술은 없다. 가장 적절한 처치는?"
    choices: ["A. 정맥 니트로프루시드를 투여한다", "B. 정맥 베타차단제만 투여하고 관찰한다", "C. 정맥 혈전용해제를 투여한다", "D. 응급 대동맥 치환술을 의뢰한다", "E. 정맥 수액을 빠르게 투여한다"]
    answer: "C"
    explanation: "이동하는 찢어지는 통증·혈압 비대칭·이완기 잡음·종격동 확장 같은 박리 단서가 없고, 허혈 심전도(하벽 ST 상승)가 있으며 제시간에 관동맥중재를 받을 수 없다. 이때는 금기가 없으면 혈전용해가 재관류 수단이다. 원 문항과 같은 흉통이라도 박리 단서가 있으면 혈전용해는 금기이고 베타차단제가 먼저다 — 답을 바꾼 것은 「박리 단서의 유무」다."
    kind: application
  - id: v2
    of: kmle-2026-0555
    flip: false
    changed: "나이·성별·통증 시작 부위(등 먼저)·검사 제시 순서를 바꾸고, 이동성 통증·혈압 비대칭·고혈압은 남김 ⇒ 답은 그대로 정맥 베타차단제"
    context: "겉모습만 다른 박리 — 등에서 시작한 통증"
    stem: "71세 여자가 40분 전 갑자기 어깨뼈 사이가 찢어지는 듯 아프다가 통증이 가슴 앞과 배 쪽으로 번져 응급실에 왔다. 오래된 고혈압이 있다. 혈압 왼팔 184/102, 오른팔 150/88 mmHg, 맥박 104회/분, 호흡 22회/분, 체온 36.6 ℃. 흉부 X선에서 상종격동이 넓어져 있다. 심전도는 동빈맥 외에 허혈 소견이 없고 트로포닌은 정상이다. 영상 검사를 준비하는 동안 가장 먼저 투여할 약물은?"
    choices: ["A. 정맥 하이드랄라진", "B. 정맥 에스몰롤", "C. 정맥 알테플라제", "D. 정맥 헤파린", "E. 정맥 생리식염수 급속 투여"]
    answer: "B"
    explanation: "통증의 시작 부위와 환자 특성은 달라도 이동하는 찢어지는 통증·양팔 혈압차·종격동 확장·허혈 없는 심전도가 박리를 가리키고, 혈압이 높다. 첫 약물은 심박수·수축력을 낮추는 정맥 베타차단제(에스몰롤)이고, 혈관확장제(하이드랄라진) 단독은 반사 빈맥으로 박리를 키운다. 혈전용해·항응고·수액 부하는 모두 해롭다."
    kind: application
figures_rejected:
- asset: PMC-PMC13422630_Figure4
  reason: 의인성 B형 박리에 대동맥내풍선펌프 인공물 — 전형적 박리 소견 교육용으로 혼동을 준다
figures:
- id: f1
  file: docs/assets/figures/pmc-pmc13586086_fig4-0-1000-850-1549.jpg
  kind: ct
  at: 가르는 소견 — 재관류 치료 전에 박리를 거른다
  shows: 대동맥박리 조영 CT(가로면) — 내막판이 참강과 가강을 나눈다
  look_for:
  - 하행 흉부대동맥 안을 가로지르는 얇은 선(내막판)
  - 내막판 양쪽으로 조영 정도가 다른 두 내강
  label: '「a: Post-contrast high-resolution coronal plane of chest CT scan revealing aortic dissection extending from the arch (after the left subclavian artery) to the descending thoracic aorta showing the true lumen (star) and false lumen (big arrow) and the presence of adjoining mural thrombi. b: Post-contrast sagittal chest CT scan of the aortic arch and descending thoracic aorta revealing an intimal flap (small arrow) separating the true (star) and false lumens (big arrow) and the presence of adjoining mural thrombi. c: Post-contrast axial chest CT scan of the descending thoracic aorta revealing an intimal flap (small arrow) separating the true (star) and false lumens (big arrow), and the presence of adjoining mural thrombi. d: Post-contrast axial chest CT of the descending thoracic aorta highlighting the communication ‘entry tear’ (arrow) between the true and false lumens and the presence of adjoining mural thrombi (star)」 — Acute aortic dissection masquerading as large bowel obstruction:
    a case report'
  label_basis: published_figure
  reference: 동료 심사 논문의 그림 설명(저자가 그 소견이라고 쓴 그림)
  paper: 'Acute aortic dissection masquerading as large bowel obstruction: a case report. The Egyptian Heart Journal'
  doi: 10.1186/s43044-026-00775-y
  credit: 'Acute aortic dissection masquerading as large bowel obstruction: a case report. Egypt Heart J. 2026 Sep 17;78:68. doi: 10.1186/s43044-026-00775-y (CC BY) — Fig. 4'
  license: CC BY
  url: https://pmc.ncbi.nlm.nih.gov/articles/PMC13586086/
  asset: PMC-PMC13586086_Fig4
  privacy_check: 가로면 CT 한 패널만 — 얼굴·이름·병원 표지 없음(다른 패널의 날짜 문자는 잘라냄)
  crop: 0,1000,850,1549
---

## 판단 — 왜 베타차단제가 먼저인가
- 박리를 넓히는 힘은 혈압의 크기만이 아니라 **압력이 얼마나 빨리 오르는가(dP/dt)** 와 박동 횟수다 — 수축력이 강하고 심박이 빠를수록 매 박동의 충격이 크다. 그래서 치료는 「혈압 낮추기」보다 「심박수·수축력 낮추기」로 시작한다.
- 저혈압이 없으면 진단을 **의심하는 순간** 정맥 베타차단제로 시작하고, 혈관확장제는 그 뒤에 더한다 — 혈관확장제 단독은 반사 빈맥으로 전단응력을 키운다 [[harrison-21: 280장 p.2105–2106]].
- 박리는 혈전이 아니라 벽이 갈라진 병이다 — 재관류 치료(혈전용해·항혈전제)는 벽 안 출혈을 키워 파열·압전을 부른다.

## 기전 — 탄성 관에서 가짜 내강으로
대동맥 벽은 얇은 내막, 평활근과 탄력판이 층을 이룬 두꺼운 중막, 외막으로 되어 있다. 수축기에 늘어나 일회박출량 일부와 탄성 에너지를 저장했다가 이완기에 되돌아가며 혈류를 이어 준다(완충 기능). 그 대가로 끊임없이 높은 박동압과 **전단응력**을 받고, 라플라스 법칙상 벽 장력은 압력×반지름에 비례한다 [[harrison-21: 280장 p.2101]].

**급성 대동맥박리**는 내막이 찢어지고(또는 중막 출혈이 내막을 뚫고) 박동 혈류가 중막의 탄력판 사이를 파고들어 **가짜 내강**을 만드는 병이다. 발병 14일 이내를 급성으로 보며, 벽내 혈종·관통성 죽상 궤양과 함께 급성 대동맥증후군을 이룬다 [[harrison-21: 280장 p.2104]].
- **벽이 약해지는 조건**: 중막 퇴행(마르판·로이스-디에츠·엘러스-단로스 Ⅳ형·이첨판막·터너), 대동맥염, 축착, 임신 3삼분기, 외상 [[harrison-21: 280장 p.2105]].
- **벽에 힘이 더 걸리는 조건**: 고혈압(환자의 약 70 %), 코카인, 역도 같은 순간적 압력 상승 [[harrison-21: 280장 p.2105]].
- 찢어짐은 전단응력이 큰 **상행대동맥 오른쪽 가쪽 벽**과 **동맥관인대 바로 아래 하행대동맥**에 잘 생긴다. 한 번 생긴 틈은 매 박동마다 혈류가 밀어 넓히며 주로 원위로, 때로 근위로 번진다 [[harrison-21: 280장 p.2104]].

## 가르는 소견 — 재관류 치료 전에 박리를 거른다
급성 흉통의 흔한 「반사」는 급성 관동맥증후군 치료다. 그 전에 표의 박리 단서를 확인하고, 폐색전증·긴장성 기흉·심낭염·식도 파열도 같은 자리에서 감별한다.
- **통증**: 갑자기 시작해 처음부터 가장 심하고 찢어지는 양상이며 발한을 동반한다. 번지는 만큼 앞가슴 → 등·어깨뼈 사이 → 배로 옮겨 간다 [[harrison-21: 280장 p.2105]].
- **대동맥판 역류**: 이완기 잡음은 흉골 오른쪽 가장자리, 넓은 맥압·심부전이 함께 온다 [[harrison-21: 280장 p.2105]]. **심낭 혈종·압전**은 A형이 근위로 역행하면 생기며 저혈압의 가장 위험한 원인이다.
- **흉부 X선**: 상종격동 확장, 왼쪽 흉막 삼출 [[harrison-21: 280장 p.2105]].
- **영상**: CT 혈관조영은 박리막·범위·분지 침범을 보여 주며 민감도·특이도가 90 % 를 넘지만 불안정 환자에게는 덜 적합하다. 경식도 심초음파는 상행·하행 박리에 매우 정확하고(민감도 98 %) 대동맥판 역류·심낭 삼출을 함께 보며 침상에서 할 수 있다. 경흉부 심초음파는 근위 박리에서 민감도 80 % 이상이지만 궁·하행에서는 약하다. MRI 는 정확하지만 시간이 걸려 안정 환자·추적용이다 [[harrison-21: 280장 p.2105]].
- **음성 결과의 한계**: 디이량체는 박리에서 대개 오르지만 확진 검사가 아니다. 정상 트로포닌·허혈 없는 심전도는 관동맥 원인을 낮출 뿐 박리를 확인하지 않는다.

## 선택 — 무엇을 어떤 순서로
- 저혈압이 없으면 목표는 수축력과 동맥압, 곧 전단응력을 낮추는 것 — 중환자실에서 혈역학을 감시한다 [[harrison-21: 280장 p.2105–2106]].
- 순서와 목표 수치는 표대로다(베타차단 → 필요하면 니트로프루시드). 정맥 ACE 억제제(에날라프릴랏)를 더할 수도 있다 [[harrison-21: 280장 p.2106]].
- **Stanford 분류가 확정 치료를 정한다** — 상행대동맥 침범 A형(근위), 궁·하행에 국한된 B형(원위). DeBakey Ⅰ·Ⅱ형은 A형, Ⅲ형은 B형 [[harrison-21: 280장 p.2105]]. A형은 응급·긴급 수술(박리막 절제·가짜 내강 폐쇄·인조혈관 치환, 판막이 망가졌으면 판막 처치). 합병증 없는 B형은 약물, 합병증 있는 B형은 흉부 혈관내 스텐트그라프트(TEVAR), 불가하면 수술 [[harrison-21: 280장 p.2106]].

## 권고와 예외
- **저혈압·쇼크**가 있으면 위의 약물 조절을 하지 않는다 — 압전·파열·심한 역류를 의심하고 소생과 함께 응급 수술로 간다.
- 장기 관리는 베타차단제에 다른 강압제(ACE 억제제·칼슘통로차단제)를 더한 혈압·수축력 조절이며, 만성 B형·벽내 혈종은 6–12개월마다 CT·MRI 로 진행·확장을 추적한다. 수술받은 환자의 원내 사망률은 15–25 %, 약물 치료한 B형은 약 12 % 이다 [[harrison-21: 280장 p.2106]].

## 시험 쟁점 — 충돌·맥락·새 근거
- 해당 없음(대조: 해리슨 280장 p.2104~2106) — 첫 약물(정맥 베타차단제)·혈관확장제 단독 금기·A형 수술/B형 약물의 서술은 문항 해설과 맞는다. 2022 ACC/AHA 지침의 세부 목표 수치는 본문 미대조(†).

## (심화) 벽내 혈종과 관통성 궤양
벽내 혈종은 내막 파열 없이 영양혈관이 터져 벽 안에 피가 고인 상태로 대부분 하행대동맥에 생기고, 박리·파열로 진행할 수 있다. 관통성 죽상 궤양은 죽상판이 중막까지 파고든 것으로 국소적이며, 가성동맥류·파열로 갈 수 있다. 두 경우 모두 A/B 분류와 치료 원칙(A형 수술, 합병증 없는 B형 약물)을 박리와 같이 적용한다 [[harrison-21: 280장 p.2104–2106]].
