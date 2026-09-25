---
id: cn.gs.diverticular-abscess.percutaneous-drainage
type: concept
topic: Gastroenterology
see_also: [General Surgery]
date: 2026-09-25
updated: 2026-09-25
version: 1
outline: h328            # 기본틀 슬롯(content/outline/subjects.yaml) — 해리슨 328장 Diverticular Disease
confidence: medium
review_status: unreviewed
note_form: 2            # 판형 2(2026-09-25)
title: "게실 농양 — 큰 농양·안정이면 경피 배농"
objective: "농양을 동반한 급성 게실염에서 농양 크기·혈역학·복막염 범위로 경피 배농·항생제 단독·응급 절제 중 다음 처치를 고른다"
objective_kind: 다음 처치
condition: 농양 동반 급성 게실염(diverticular abscess, Hinchey Ib~II)
exams: [usmle, kmle]
summary:
  - "결론: 안정된 환자의 3 cm 넘는 벽이 뚜렷한 게실 농양은 항생제에 CT 유도 경피 배농을 더한다."
  - "시험 단서: 좌하복부 통증·발열 + CT 결장 옆 테두리 조영 증강 액체(rim-enhancing collection), 유리 공기 없음."
  - "왜: 고름 덩어리엔 항생제가 잘 닿지 않는다 — 배농이 패혈 원인을 줄이고 응급 장루 수술을 피하게 한다."
  - "수술로 가는 조건: 배농 실패 뒤 범발성 복막염, 분변성 복막염·유리 공기(경피 배농의 금기), 쇼크."
  - "대장내시경(colonoscopy)은 급성기가 아니라 회복 약 6주 뒤 — 대장암 배제용."
pitfalls:
  - contrast: "IV 항생제 단독 vs 배농 추가"
    point: "작은 농양은 항생제만으로 흔히 낫지만, 3 cm 를 넘고 벽이 뚜렷한 농양은 배농을 더한다. 크기가 가른다 — 5 cm 를 넘으면 두 기준 어디서도 단독 항생제 쪽이 아니다."
    exception: "해리슨은 5 cm 미만도 항생제 단독으로 풀릴 수 있다고 적어 3~5 cm 는 겹친다(시험 쟁점 Z1)."
    cites: ["harrison-21: 328장 p.2500"]
    covers: ["usmle-2026-0173:B"]
  - contrast: "구불결장 절제 + 끝 결장루(Hartmann) vs 경피 배농"
    point: "하트만 수술은 배농 실패 뒤 범발성 복막염, 분변성 복막염(Hinchey IV)·쇼크의 처치다. 안정·국소 압통·유리 공기 없음이면 먼저 배농한다."
    cites: ["harrison-21: 328장 p.2500"]
    covers: ["usmle-2026-0173:C"]
  - contrast: "대장내시경으로 암 배제 — 지금?"
    point: "대장암 배제는 필요하지만 시기는 급발작 약 6주 뒤다. 활동성 감염·농양이 있는 지금의 다음 처치는 배농이다."
    cites: ["harrison-21: 328장 p.2498"]
    covers: ["usmle-2026-0173:D"]
  - contrast: "복강경 세척·배액 vs 경피 배농"
    point: "복강경 세척은 복강 전체로 퍼진 화농성 복막염(Hinchey III)에서 논의되는 선택지이고 재수술 위험이 높다. 결장 옆에 국한된 농양은 경피로 뺀다."
    cites: ["harrison-21: 328장 p.2500"]
    covers: ["usmle-2026-0173:E"]
tables:
  - id: level
    section: "선택 — 크기·상태로 가르는 처치"
    title: "게실염 — CT 소견 × 상태 → 처치"
    role: treatment
    span: column
    columns: ["상황", "처치", "주의"]
    rows:
      - ["염증덩이·작은 농양(Hinchey Ia, 작은 Ib)", "IV 항생제 단독 [[harrison-21: 328장 p.2500]]", "5 cm 미만은 항생제로 풀릴 수 있다"]
      - ["3 cm 넘고 벽이 뚜렷한 농양, 안정(Ib·II)", "IV 항생제 + CT 유도 경피 배농 [[harrison-21: 328장 p.2500]]", "배농 실패 20~25%"]
      - ["경피 접근 경로 없음·기복증·분변성 복막염", "경피 배농 금기 → 수술 [[harrison-21: 328장 p.2500]]", "—"]
      - ["배농 실패 + 범발성 복막염", "응급 수술, 대개 하트만 수술 [[harrison-21: 328장 p.2500]]", "구불결장 절제 + 끝 결장루 + 직장 끝(rectal stump)"]
      - ["화농성 복막염(III)", "절제 ± 우회 장루, 선택적 복강경 세척 [[harrison-21: 328장 p.2500]]", "세척 단독은 재수술 위험 ↑"]
      - ["분변성 복막염(IV)", "하트만 수술 또는 세척 + 우회 장루 — 문합 금지 [[harrison-21: 328장 p.2500]]", "—"]
criteria:
  - id: dvabs-drain
    name: 경피 배농 적응
    kind: 치료 권고
    population: "농양 동반 급성 게실염, 혈역학적으로 안정"
    statement: "항생제에 더해 3 cm 를 넘고 벽이 뚜렷한 게실 농양은 CT 유도 경피 배농(해리슨이 인용한 ASCRS 권고) [[harrison-21: 328장 p.2500]]"
    exceptions: "경피 접근 경로 없음·기복증·분변성 복막염은 금기. 5 cm 미만은 항생제 단독으로 풀릴 수 있다"
    source: harrison-21
    basis: current
    exams: [usmle, kmle]
  - id: dvabs-surgery
    name: 응급 수술 전환
    kind: 치료 권고
    population: "경피 배농 뒤 게실 농양"
    statement: "배농이 실패하고 범발성 복막염이 생기면 응급 수술 — 대부분 하트만 수술(구불결장 절제·끝 결장루·직장 끝(rectal stump)) [[harrison-21: 328장 p.2500]]"
    exceptions: "분변성 복막염(Hinchey IV)에서는 어떤 문합도 하지 않는다"
    source: harrison-21
    basis: current
    exams: [usmle, kmle]
  - id: dvabs-colonoscopy
    name: 대장내시경 시기
    kind: 검사 시기
    population: "게실염 급발작 뒤"
    statement: "대장암 배제를 위해 급발작 약 6주 뒤 대장내시경 [[harrison-21: 328장 p.2498]]"
    exceptions: "지침 문헌은 6~8주로 적기도 한다[[?ascrs-2020]]"
    source: harrison-21
    basis: current
    exams: [usmle, kmle]
sources:
  - id: harrison-21
    org: "McGraw Hill"
    title: "Harrison's Principles of Internal Medicine, 21st ed. — Chapter 328: Diverticular Disease and Common Anorectal Disorders"
    kind: textbook
    year: 2022
    citation: "Loscalzo J, Kasper DL, Longo DL, et al (eds). Harrison's Principles of Internal Medicine, 21e. 328장 p.2498–2500 (Fig. 328-2 · Table 328-1 · Table 328-4)"
    checked_at: 2026-09-25
    checked: "본문 대조(드라이브 장별 문서 h328) — p.2498: CT 진단 기준(벽 > 4 mm·결장 주위 지방 염증), 농양 최대 20%, Table 328-1(합병 25%, 농양 16%), Hinchey 분류·Ia 염증덩이/Ib 결장 주위 농양, 급발작 약 6주 뒤 대장내시경(대장암 배제·수술 전). p.2499: 입원 게실염 ~75% 비수술 치료 반응, 3세대 세팔로스포린 또는 시프로플록사신+메트로니다졸, 단독 piperacillin, 합병 게실염의 수술 위험 낮은 환자에서 수술 적응. p.2500: Table 328-4(Ib·II = 경피 배농 후 절제), ASCRS 인용 — 3 cm 초과·벽 뚜렷한 농양은 항생제 + CT 유도 경피 배농, 5 cm 미만은 항생제 단독으로 풀릴 수 있음, 금기(경로 없음·기복증·분변성 복막염), 실패율 20–25%, 실패 + 범발성 복막염 → 대개 하트만 수술, Hinchey III 복강경 세척(재수술 위험 ↑), IV 문합 금지. 해리슨에 없는 것: 급성기 대장내시경의 천공 위험 설명, 4 cm 기준, 배농 뒤 선택적 절제의 개별화, 면역저하 환자의 수술 문턱."
    verified: text
  - id: ascrs-2020
    org: "American Society of Colon and Rectal Surgeons (Hall J et al.)"
    title: "The American Society of Colon and Rectal Surgeons Clinical Practice Guidelines for the Management of Left-Sided Colonic Diverticulitis"
    kind: guideline
    year: 2020
    citation: "Dis Colon Rectum 2020;63(6):728-747"
    doi: "10.1097/DCR.0000000000001679"
    url: "https://doi.org/10.1097/DCR.0000000000001679"
    checked_at: 2026-09-25
    checked: "서지만(기억·문항 참고문헌 기준, 컨테이너가 PubMed·doi.org 를 막아 원문·PMID 미대조). 본문 권고는 해리슨 328장이 인용한 부분만 해리슨 쪽으로 확인했다."
    verified: citation
  - id: wses-2020
    org: "World Society of Emergency Surgery (Sartelli M et al.)"
    title: "2020 update of the WSES guidelines for the management of acute colonic diverticulitis in the emergency setting"
    kind: guideline
    year: 2020
    citation: "World J Emerg Surg 2020;15:32"
    doi: "10.1186/s13017-020-00313-4"
    url: "https://doi.org/10.1186/s13017-020-00313-4"
    checked_at: 2026-09-25
    checked: "서지만(기억·문항 참고문헌 기준, 원문·PMID 미대조). 4 cm 기준 등은 원문을 보지 않아 [[?wses-2020]] 로만 단다."
    verified: citation
diagram:
  title: "게실염 — 농양이 있을 때의 다음 처치"
  nodes:
    - {id: start, kind: start, text: "좌하복부 통증·발열 + CT 급성 게실염"}
    - {id: shock, kind: decision, text: "쇼크·범발성 복막염·유리 공기?"}
    - {id: hartmann, kind: end, text: "응급 절제 — 하트만 수술(Hartmann)"}
    - {id: abscess, kind: decision, text: "벽 뚜렷한 농양 > 3 cm?"}
    - {id: ctinfo, kind: info, text: "조영 CT 로 농양 크기·벽·위치 확인"}
    - {id: abx, kind: end, text: "IV 항생제 단독 + 경과 관찰"}
    - {id: route, kind: decision, text: "경피 접근 경로가 있는가?"}
    - {id: pcd, kind: end, text: "CT 유도 경피 배농 + IV 항생제"}
    - {id: opdrain, kind: alert, text: "수술적 배농·절제"}
  edges:
    - {from: start, to: shock}
    - {from: shock, to: hartmann, label: "있음"}
    - {from: shock, to: abscess, label: "없음·안정"}
    - {from: abscess, to: route, label: "예"}
    - {from: abscess, to: abx, label: "작음·없음"}
    - {from: abscess, to: ctinfo, label: "영상 없음"}
    - {from: ctinfo, to: route, label: "큰 농양"}
    - {from: ctinfo, to: abx, label: "작은 농양"}
    - {from: route, to: pcd, label: "있음"}
    - {from: route, to: opdrain, label: "없음"}
diagram_notes:
  - "3~5 cm 는 겹친다 — 해리슨은 3 cm 초과 배농, 5 cm 미만은 항생제로도 풀릴 수 있다고 함께 적는다. 5 cm 를 넘으면 배농 쪽이다."
  - "경피 배농의 금기: 접근 경로 없음, 기복증(pneumoperitoneum), 분변성 복막염."
  - "배농이 실패하고(20~25%) 범발성 복막염이 생기면 응급 수술 — 대개 하트만 수술."
  - "대장내시경은 급발작 약 6주 뒤, 대장암 배제용이다 — 도식의 어느 끝에서도 지금 하는 처치가 아니다."
checks:
  - q: "안정된 환자의 5.5 cm 게실 농양 — 항생제만으로 부족한 이유와 다음 처치는?"
    a: "3 cm 를 넘는 벽 뚜렷한 농양은 항생제만으로는 실패가 많다. IV 항생제에 CT 유도 경피 배농을 더한다."
  - q: "경피 배농 대신 수술로 가는 조건 셋은?"
    a: "경피 접근 경로가 없음, 기복증·분변성 복막염(배농 금기), 배농 실패 뒤 범발성 복막염·쇼크."
  - q: "게실염 뒤 대장내시경은 언제·왜?"
    a: "급발작 약 6주 뒤, 대장암을 배제하려고(특히 수술 전). 급성기의 다음 처치가 아니다."
variants:
  - id: v1
    of: usmle-2026-0173
    flip: true
    changed: "혈압 132/80·국소 압통·유리 공기 없음 → 혈압 84/50·젖산 4.6·복부 전체 반발통·강직·CT 유리 공기와 복강 내 분변성 액체 → 경피 배농 금기가 되어 답이 「CT 유도 경피 배농」에서 「구불결장 절제 + 끝 결장루(하트만)」로 바뀜"
    context: "단서를 바꿔 답이 바뀌는 변형 — 유리 공기·분변성 복막염·쇼크"
    stem: "A 66-year-old woman is brought to the emergency department with 3 days of left lower abdominal pain that became severe and generalized 6 hours ago. She has known sigmoid diverticulosis. Temperature is 38.9°C, pulse 124/min, respirations 26/min, and blood pressure 84/50 mm Hg despite 2 L of intravenous crystalloid. The abdomen is distended and rigid with diffuse rebound tenderness. Leukocyte count is 21,400/mm³ and serum lactate is 4.6 mmol/L. CT scan of the abdomen and pelvis shows sigmoid wall thickening with inflamed diverticula, free intraperitoneal air, and extraluminal fluid with fecal material throughout the pelvis and both paracolic gutters. Intravenous piperacillin-tazobactam is started. Which of the following is the most appropriate next step in management?"
    choices: ["A. CT-guided percutaneous drainage of the pelvic fluid", "B. Continuation of intravenous antibiotics with serial abdominal examinations", "C. Laparoscopic peritoneal lavage without resection", "D. Emergency sigmoid resection with end colostomy", "E. Colonoscopy to evaluate the sigmoid colon"]
    answer: "D"
    explanation: "유리 공기와 분변성 복막염(Hinchey IV)에 쇼크가 겹쳤다. 기복증·분변성 복막염은 경피 배농의 금기이고 항생제만으로는 원인을 없앨 수 없으며, 분변성 복막염에서는 문합을 하지 않는다 — 응급 하트만 수술(구불결장 절제·끝 결장루)이 답이다. 세척 단독은 화농성(III)에서나 논의되고 재수술 위험이 높다. 원래 문항은 안정·국소 농양이라 배농이 먼저였다."
    kind: application
  - id: v2
    of: usmle-2026-0173
    flip: false
    changed: "나이·성별(58세 남자), 병력(고혈압·과거 대장내시경 → 이상지질혈증), 배뇨 증상 추가, 농양 위치·크기(결장 옆 5.5 cm → 골반 쪽 6 cm), 검사 제시 순서를 바꾸고 「활력 안정·국소 압통·유리 공기 없음·3 cm 넘는 벽 뚜렷한 농양」은 그대로 → 답은 여전히 CT 유도 경피 배농"
    context: "겉모습만 바꾸고 답은 같은 변형 — 골반 쪽 6 cm 농양의 중년 남자"
    stem: "A 58-year-old man comes to the emergency department because of 5 days of lower abdominal pain, fever, and increasing urinary frequency. He has hyperlipidemia treated with atorvastatin and takes no other medications. CT scan of the abdomen and pelvis with intravenous contrast shows sigmoid diverticula with wall thickening and fat stranding and a 6-cm thick-walled fluid collection in the pelvis between the sigmoid colon and the bladder; there is no free intraperitoneal air. Temperature is 38.4°C, pulse 96/min, and blood pressure 138/84 mm Hg. The abdomen is tender with guarding in the suprapubic region and left lower quadrant but is otherwise soft without rebound. Leukocyte count is 16,900/mm³ and serum lactate is 1.2 mmol/L. Intravenous ceftriaxone and metronidazole are started. Which of the following is the most appropriate next step in management?"
    choices: ["A. Continuation of intravenous antibiotics alone for 10 days", "B. Emergency sigmoid resection with end colostomy", "C. Colonoscopy to exclude sigmoid carcinoma", "D. CT-guided percutaneous drainage of the collection", "E. Laparoscopic peritoneal lavage and drain placement"]
    answer: "D"
    explanation: "겉모습(남자·골반 위치·배뇨 증상·다른 항생제)이 바뀌어도 결정적 단서는 같다 — 안정된 활력, 국소 압통, 유리 공기 없음, 3 cm 를 넘는 벽 뚜렷한 농양. 그래서 항생제에 CT 유도 경피 배농을 더한다. 방광 쪽 증상은 인접 염증으로 설명되고 누공 확인은 급성기 결정이 아니다. 대장내시경은 약 6주 뒤, 응급 절제·세척은 범발성 복막염에서."
    kind: application
---

## 판단 — 왜 경피 배농이 먼저인가
- 게실염이 **결장 옆 농양**을 만들었고 환자가 **안정**하면, 할 일은 「고름을 빼되 장은 아직 자르지 않는 것」이다 — 그 도구가 CT 유도 경피 배농(percutaneous drainage)이다 [[harrison-21: 328장 p.2500]].
- 크기가 항생제 단독과 배농을 가른다: 3 cm 를 넘고 벽이 뚜렷한 농양은 항생제에 배농을 더한다 [[harrison-21: 328장 p.2500]].
- 안정·국소 복막염·유리 공기 없음이 응급 수술을 가른다: 하트만 수술은 배농 실패 뒤 범발성 복막염이나 분변성 복막염의 처치다 [[harrison-21: 328장 p.2500]].
- 배농은 급성 패혈 원인을 줄여, 필요한 절제를 나중에 문합과 함께 하게 해 준다(Table 328-4: Ib·II = 배농 뒤 절제) [[harrison-21: 328장 p.2500]].

## 기전 — 미세 천공에서 농양까지
게실은 근육층이 약한 곳(혈관이 뚫고 들어가는 자리)으로 점막이 빠져나온 주머니다. 목이 막히고 내압이 오르면 벽에 염증과 미세 천공이 생긴다. 새어 나온 것이 결장 주위 지방·장간막에 갇히면 염증덩이(phlegmon, Ia)나 결장 주위 농양(Ib)이, 멀리 골반에 고이면 원격 농양(II)이 된다. 천공이 막히지 않고 복강에 퍼지면 화농성(III)·분변성(IV) 복막염이다 [[harrison-21: 328장 p.2498]].
- 농양은 벽으로 둘러싸인 무혈관 고름이라 **항생제가 안쪽까지 잘 닿지 않는다** — 크면 원인을 물리적으로 빼야 한다. CT 에서 「테두리 조영 증강」은 이 벽을 보여 주는 소견이다.
- 압통이 좌하복부에 머물고 반발통이 없으면 염증이 아직 결장 주위에 갇혀 있다는 뜻이다. 유리 공기·복강 전체 액체는 갇히지 않았다는 신호다.
- 정상 소견의 한계: 유리 공기가 없다고 천공이 없던 것은 아니다(농양 자체가 막힌 천공이다). 가르는 것은 「갇혔는가」다.

## 선택 — 크기·상태로 가르는 처치
- 경피 배농은 항생제와 **함께** 한다 — 배농이 항생제를 대신하지 않는다. 항생제는 그람음성 막대균·혐기균을 덮는다(3세대 세팔로스포린 또는 시프로플록사신 + 메트로니다졸, 단독 피페라실린) [[harrison-21: 328장 p.2499]].
- 재평가: 배농 실패는 20~25% 다. 열·통증·백혈구가 좋아지지 않거나 범발성 복막염이 생기면 수술로 넘어간다 [[harrison-21: 328장 p.2500]].
- 금기: 경피 경로 없음, 기복증, 분변성 복막염 [[harrison-21: 328장 p.2500]].

## 권고와 예외
- 대장내시경은 급발작 **약 6주 뒤** 대장암 배제·수술 전 평가로 한다 [[harrison-21: 328장 p.2498]]. 급성기에 하지 않는 이유(공기 주입에 의한 천공 위험)는 해리슨에 적혀 있지 않다 [[?ascrs-2020]].
- 배농 기준 크기를 4 cm 로 쓰는 문헌도 있다 [[?wses-2020]]. 어느 쪽이든 5 cm 를 넘으면 배농이다.
- 면역저하 환자에서 수술 문턱을 낮추는 문제는 이 정리본에서 대조하지 않았다(검토 항목).

## 시험 쟁점 — 충돌·맥락·새 근거
- **Z1 맥락 · 배농 크기 기준 3 cm, 4 cm, 5 cm** — 시험 기준: 안정 + 3 cm 넘는 벽 뚜렷한 농양 → 항생제 + 경피 배농 [[harrison-21: 328장 p.2500]] / 다른 기준: 같은 쪽에서 해리슨은 「5 cm 미만 농양은 항생제만으로 풀릴 수 있다」고도 적고, 4 cm 를 쓰는 지침도 있다 [[?wses-2020]] / 왜 다른가: 3~5 cm 는 어느 쪽도 성공할 수 있는 회색 지대라 기관마다 선을 달리 긋는다 / 시험에서는: USMLE·KMLE 모두 5 cm 를 넘으면 배농, 2 cm 안팎이면 항생제 단독으로 출제하는 것이 안전하다 — 회색 지대 크기가 나오면 다른 단서(악화·반응)를 찾는다.
- **Z2 충돌 · 배농 뒤 절제는 늘 하는가** — 시험 기준: 급성기의 다음 처치는 배농이고, 배농 뒤 선택적 절제는 이 목표의 답이 아니다 / 다른 기준: 해리슨은 Ib·II 를 「배농 뒤 약 6주에 절제·문합」으로, 합병 게실염은 수술 위험이 낮으면 모두 수술 적응으로 적는다 [[harrison-21: 328장 p.2499–2500]]. 최근 지침은 재발 위험·환자 상태로 개별화한다고 알려져 있다 [[?ascrs-2020]] / 왜 다른가: 배농 뒤 재발률 자료가 쌓이며 일률적 절제에서 개별화로 옮겨 가는 중이다 / 시험에서는: 「배농 후 다음 단계」를 물으면 USMLE 는 회복 뒤 대장내시경 + 선택적 절제 논의, KMLE 는 교과서형으로 선택적 절제를 답으로 둘 수 있다.
- **Z3 맥락 · Hinchey III 의 정의** — 시험 기준: III = 화농성 범발성 복막염, IV = 분변성 복막염 / 다른 기준: 해리슨 그림 328-2 설명은 III 을 「비교통 천공 + 분변성 복막염」으로 적지만, 같은 장 본문은 III 에 분변성 복막염이 없다고 적는다 [[harrison-21: 328장 p.2498·p.2500]] / 왜 다른가: 그림 설명 문구의 불일치 / 시험에서는: 본문 쪽 정의(III 화농성, IV 분변성)로 푼다.
