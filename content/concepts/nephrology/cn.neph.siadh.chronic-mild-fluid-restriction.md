---
id: cn.neph.siadh.chronic-mild-fluid-restriction
type: concept
topic: Nephrology
see_also: [Endocrinology, Oncology]
date: 2026-09-23
updated: 2026-10-05
version: 2
outline: h53            # 기본틀 슬롯(content/outline/subjects.yaml)
confidence: medium
review_status: unreviewed
note_form: 2            # 판형 2(2026-09-25)
title: "SIADH — 경증 만성은 수분제한, 경련엔 고장성식염수"
objective: "SIADH 저나트륨혈증에서 증상의 중증도와 경과(급성·만성)에 따라 첫 치료를 고른다"
objective_kind: 치료
condition: SIADH(부적절 항이뇨 증후군, SIAD)
exams: [kmle, usmle]
summary:
  - "결론: 증상이 가벼운 만성 SIADH 의 첫 치료는 수분제한(원인 교정과 함께) — 경련·혼수일 때만 3% 고장성식염수."
  - "시험 단서: 소세포폐암 + 정상용적 저삼투 저나트륨혈증 + 요삼투 >100·요Na 상승, 갑상선·부신 정상 = SIADH(SIAD)."
  - "왜: 낮은 삼투질농도에서도 AVP(ADH)가 꺼지지 않아 자유수를 못 버린다 — 들어오는 물을 줄이는 것이 기둥이다."
  - "교정 한계: 만성은 24시간 8~10 mM·48시간 18 mM 을 넘기지 않는다 — 넘으면 삼투성 탈수초 증후군(ODS)."
  - "쓰지 않는다: 데스모프레신(ADH 작용을 더함), 생리식염수(농축뇨로 나트륨만 빠짐), 저장성 수액·자유수."
pitfalls:
  - contrast: "데스모프레신 vs 수분제한 — 「ADH·소변 농축 문제」라서?"
    point: "데스모프레신은 V2 작용제로 ADH 가 부족한 중추성 요붕증의 약이다. SIADH 는 이미 ADH 작용이 과잉이라 자유수 저류가 늘어 저나트륨혈증이 악화된다. 필요한 방향은 반대 — 물을 줄이거나(수분제한) V2 를 막는다(바프탄)."
    exception: "과교정이 일어났거나 우려될 때는 데스모프레신과 포도당수로 교정 속도를 되돌리거나, 처음부터 데스모프레신을 고정 투여하며 고장성식염수로 천천히 올리는 전략이 있다 [[harrison-21: 53장 p.346]]."
    cites: ["harrison-21: 53장 p.346"]
    covers: ["kmle-2026-0072:E"]
  - contrast: "저나트륨혈증 = 생리식염수?"
    point: "등장성 식염수는 AVP 가 억제되는 저혈량성 저나트륨혈증에 듣는다. SIADH 에서는 요삼투가 수액의 삼투질농도보다 높으면 나트륨은 소변으로 나가고 물은 남아 나트륨이 더 떨어질 수 있다."
    cites: ["harrison-21: 53장 p.345"]
  - contrast: "수분제한은 모두 같은 양?"
    point: "소변으로 자유수를 못 버리는 환자일수록 강하게 제한한다 — 요/혈장 전해질비로 정한다(표). 갈증도 부적절하게 자극돼 있어 지키기 어렵다."
    cites: ["harrison-21: 53장 p.345"]
tables:
  - id: siadh-ddx
    title: "정상용적 SIADH 를 다른 저나트륨혈증과 가르기"
    role: differential
    span: column
    section: "가르는 소견 — 정상용적·농축뇨·요나트륨"
    columns: ["원인", "가르는 소견", "치료 쪽"]
    rows:
      - ["SIADH", "정상용적, 요삼투 >100, 요Na 상승(>20~30), 요산 저하(<4 mg/dL)", "수분제한"]
      - ["저혈량성", "요Na <20, 요산 상승", "등장성 식염수(AVP 가 억제된다)"]
      - ["과혈량성(심부전·간경변·신증후군)", "부종", "—"]
      - ["갑상선저하·2차 부신부전", "TSH·오전 코르티솔 이상", "먼저 걸러야 SIADH 진단"]
    note: "harrison-21: 53장 p.342–343"
  - id: siadh-treatment
    title: "SIADH — 상황별 치료"
    role: treatment
    span: column
    section: "선택 — 증상·경과·반응에 따라"
    columns: ["상황", "치료", "주의"]
    rows:
      - ["경증·만성, 증상 가볍다", "수분제한(원인 교정과 함께)", "요/혈장 전해질비로 제한량 결정"]
      - ["중증 증상(경련·혼수), 급성", "3% 고장성식염수 4~6 mM", "그 뒤 만성 교정 한계"]
      - ["수분제한에 반응 없음", "경구 요소·푸로세마이드+염분, 톨밥탄", "톨밥탄은 입원 시작, 1~2개월 이내"]
      - ["과교정", "포도당수·데스모프레신", "ODS 예방 목적"]
    note: "harrison-21: 53장 p.345–346"
  - id: fluid-restriction
    title: "수분제한의 강도 — 요/혈장 전해질비"
    role: treatment
    span: column
    section: "선택 — 증상·경과·반응에 따라"
    columns: ["(요Na+요K)/혈장Na", "하루 수분 제한량"]
    rows:
      - ["> 1", "500 mL 미만"]
      - ["약 1", "500~700 mL"]
      - ["< 1", "1 L 미만"]
    note: "harrison-21: 53장 p.345"
diagram:
  title: "SIADH 저나트륨혈증 — 첫 치료 고르기"
  nodes:
    - {id: start, kind: start, text: "정상용적 저삼투 저나트륨혈증 · 요삼투 >100"}
    - {id: excl, kind: decision, text: "갑상선·부신 정상, 이뇨제 없음?"}
    - {id: other, kind: alert, text: "갑상선저하·부신부전 — SIADH 아님"}
    - {id: sx, kind: decision, text: "경련·의식저하 같은 중증 증상?"}
    - {id: sxinfo, kind: info, text: "증상의 정도·발생 시점(48시간)을 확인"}
    - {id: hts, kind: end, text: "3% 고장성식염수 — 4~6 mM 만 올린다"}
    - {id: fr, kind: step, text: "수분제한 + 원인 교정"}
    - {id: resp, kind: decision, text: "수분제한으로 나트륨이 오르나?"}
    - {id: keep, kind: end, text: "수분제한 유지 · 나트륨 자주 재측정"}
    - {id: second, kind: end, text: "경구 요소 · 푸로세마이드+염분 · 톨밥탄"}
  edges:
    - {from: start, to: excl}
    - {from: excl, to: sx, label: "정상"}
    - {from: excl, to: other, label: "이상"}
    - {from: sx, to: hts, label: "있음"}
    - {from: sx, to: fr, label: "가볍다"}
    - {from: sx, to: sxinfo, label: "불명"}
    - {from: sxinfo, to: hts, label: "중증·급성"}
    - {from: sxinfo, to: fr, label: "경증·만성"}
    - {from: fr, to: resp}
    - {from: resp, to: keep, label: "오른다"}
    - {from: resp, to: second, label: "안 오른다"}
diagram_notes:
  - "만성(48시간 넘게 또는 기간 불명)은 24시간 8~10 mM·48시간 18 mM 을 넘겨 올리지 않는다 — 고장성식염수로 증상을 가라앉힌 뒤에도 같다."
  - "수분제한 양은 요/혈장 전해질비로 정한다(표) — 비가 클수록 자유수를 못 버리므로 더 강하게."
  - "톨밥탄은 입원해서 시작하고 수분제한을 풀며, 간독성 때문에 1~2개월 이내로 쓴다."
  - "데스모프레신은 과교정을 되돌리거나 막을 때만 쓴다 — 그 밖에는 SIADH 를 악화시킨다."
  - "생리식염수는 요삼투가 수액보다 높으면 효과가 없거나 나트륨을 더 떨어뜨린다."
checks:
  - q: "SIADH 에서 생리식염수가 오히려 나트륨을 낮출 수 있는 이유는?"
    a: "요삼투가 수액(약 300 mOsm/kg)보다 높으면 투여한 나트륨은 소변으로 나가고 그 물의 일부는 남기 때문이다."
  - q: "만성 저나트륨혈증의 24시간·48시간 교정 상한은?"
    a: "24시간 8~10 mM, 48시간 18 mM."
  - q: "SIADH 치료에서 데스모프레신을 쓰는 자리는?"
    a: "과교정을 되돌리거나 막을 때뿐이다. 그 밖에는 ADH 작용을 더해 저나트륨혈증을 악화시킨다."
criteria:
  - id: hypoNa-correction-limit
    name: 만성 저나트륨혈증 교정 한계(Harrison)
    kind: 치료 기준
    population: "48시간 넘게 지속된(또는 기간 불명) 저나트륨혈증"
    statement: "24시간에 8~10 mM, 48시간에 18 mM 을 넘겨 올리지 않는다 — 넘으면 ODS 위험"
    exceptions: "맥주 포토마니아·저칼륨혈증·알코올·영양실조는 ODS 고위험이라 더 조심한다"
    source: harrison-21
    locator: "53장 p.344–345"
    basis: current
    exams: [kmle, usmle]
  - id: hypoNa-acute-severe
    name: 급성 중증 증상(Harrison)
    kind: 치료 기준
    population: "경련·의식저하 등 중증 증상의 급성 저나트륨혈증"
    statement: "3% 고장성식염수(513 mM)로 1~2 mM/h, 총 4~6 mM 을 올린다. 100 mL 일시 주입이 지속 주입보다 효과적"
    exceptions: "증상이 가라앉으면 만성 교정 한계를 따른다"
    source: harrison-21
    locator: "53장 p.345"
    basis: current
    exams: [kmle, usmle]
sources:
  - id: harrison-21
    org: "McGraw Hill"
    title: "Harrison's Principles of Internal Medicine, 21st ed. — Chapter 53: Fluid and Electrolyte Disturbances"
    kind: textbook
    year: 2022
    citation: "Loscalzo J, Kasper DL, Longo DL, et al (eds). Harrison's Principles of Internal Medicine, 21e. 53장 p.338–355"
    checked_at: 2026-09-23
    checked: "본문 대조(드라이브 문서) — p.339 AVP 삼투 역치 약 285 mOsm/kg·V2 작용; p.342–343 SIAD 가 정상용적 저나트륨혈증의 가장 흔한 원인, 갑상선저하·2차 부신부전 감별, 소세포폐암 75%, 요산 저하; p.344–345 ODS 교정 한계(8–10 mM/24h·18 mM/48h), 수분제한과 요/혈장 전해질비별 제한량, 3% 식염수 4–6 mM, 톨밥탄 적응·기간; p.346 과교정 시 DDAVP·포도당수"
    verified: text
  - id: spasovski-2014
    org: "European Society of Endocrinology / ESICM / ERA-EDTA"
    title: "Clinical practice guideline on diagnosis and treatment of hyponatraemia"
    kind: guideline
    year: 2014
    citation: "Spasovski G, Vanholder R, Allolio B, et al. Eur J Endocrinol 2014;170(3):G1–G47"
    doi: "10.1530/EJE-13-1020"
    pmid: "24569125"   # 2026-09-25 PubMed esearch 로 DOI 확인·제목 일치
    checked_at: 2026-09-23
    checked: "서지만 — 루틴 컨테이너에서 doi·PubMed 접근이 막혀 본문을 대조하지 못했다. 시험 쟁점 절의 증상 분류 서술은 사람 대조가 필요하다"
    verified: citation
variants:
  - id: v1
    of: kmle-2026-0072
    flip: true
    changed: "증상을 가벼운 오심·집중력저하에서 전신 강직간대 경련·의식저하로, 경과를 이틀 사이 급격한 발생으로 바꿈 → 중증 증상 급성 저나트륨혈증이므로 답이 수분제한에서 3% 고장성식염수로 바뀜"
    context: "단서를 바꿔 답이 바뀌는 변형 — 경련을 동반한 급성 저나트륨혈증"
    stem: "66세 남성이 소세포폐암으로 항암치료를 받던 중 이틀 전부터 두통과 구토가 심해지다가 오늘 전신 강직간대 경련을 한 뒤 불러도 눈을 겨우 뜬다. 사흘 전 외래 혈청 나트륨은 134 mmol/L 였다. 부종이나 탈수 소견은 없다. 혈청 나트륨 116 mmol/L, 혈청 삼투질농도 242 mOsm/kg, 소변 삼투질농도 510 mOsm/kg, 소변 나트륨 55 mmol/L 이며 갑상선·부신 기능은 정상이다. 가장 먼저 할 치료는?"
    choices: ["A. 3% 고장성식염수 투여", "B. 수분제한", "C. 데스모프레신 투여", "D. 0.45% 식염수 투여", "E. 경구 톨밥탄 투여"]
    answer: "A"
    explanation: "SIADH 라는 진단은 같지만, 이틀 사이 생긴(급성) 저나트륨혈증이 경련·의식저하를 일으켰으므로 뇌부종을 줄이기 위해 3% 고장성식염수로 4~6 mM 을 빨리 올린다 [[harrison-21: 53장 p.345]]. 수분제한은 며칠에 걸쳐 작용해 중증 증상에는 늦고, 톨밥탄은 반응이 예측하기 어려워 응급 치료가 아니다. 데스모프레신과 저장성 수액은 나트륨을 더 낮춘다. 원래 문항은 증상이 가벼워 수분제한이 먼저였다."
    kind: application
  - id: v2
    of: kmle-2026-0072
    flip: false
    changed: "성별·나이(72세 여성)·내원 경위(정기 채혈에서 발견)·제시 순서를 바꾸고, 소세포폐암·정상용적·농축뇨·요나트륨 상승·갑상선/부신 정상·가벼운 증상은 그대로 → 답은 여전히 수분제한"
    context: "겉모습만 바꾸고 답은 같은 변형 — 정기 채혈에서 발견된 저나트륨혈증"
    stem: "72세 여성이 소세포폐암 2차 항암치료 전 정기 채혈에서 혈청 나트륨 121 mmol/L 로 확인되었다. 최근 한두 주 동안 입맛이 떨어지고 약간 멍한 느낌이 있었다고 한다. 혈압 128/76 mmHg, 누운 자세와 선 자세 혈압 차이가 없고 피부 긴장도와 하지 부종은 정상이다. 이뇨제는 복용하지 않는다. 혈청 삼투질농도 252 mOsm/kg, 소변 삼투질농도 450 mOsm/kg, 소변 나트륨 48 mmol/L, TSH 와 오전 코르티솔은 정상이다. 가장 적절한 초기 치료는?"
    choices: ["A. 데스모프레신 투여", "B. 생리식염수 정주", "C. 3% 고장성식염수 투여", "D. 수분제한", "E. 5% 포도당수 정주"]
    answer: "D"
    explanation: "환자와 발견 경위는 달라도 결정 단서 — 정상용적, 저삼투 저나트륨혈증에 부적절하게 진한 소변과 요나트륨 상승, 갑상선·부신 정상, 소세포폐암, 가벼운 만성 증상 — 가 같으므로 SIADH 의 1차 치료인 수분제한이다 [[harrison-21: 53장 p.343·345]]. 데스모프레신·포도당수는 자유수를 늘려 악화시키고, 생리식염수는 농축뇨로 나트륨이 빠져 효과가 없거나 악화시킬 수 있으며, 고장성식염수는 중증 증상일 때 쓴다."
    kind: application
figures_none: 나트륨·삼투압 수치로 판단하는 문제 — 영상 소견이 없다
---

## 판단 — 왜 수분제한이 먼저인가
- SIADH 는 AVP 가 꺼지지 않아 자유수를 버리지 못하는 상태다 — 들어오는 물을 줄이는 **수분제한**이 만성 저나트륨혈증 치료의 초석이다 [[harrison-21: 53장 p.345]].
- 치료의 급한 정도는 **증상**이 정한다. 경련·의식저하가 있는 급성 저나트륨혈증만 3% 고장성식염수로 4~6 mM 을 빨리 올린다 [[harrison-21: 53장 p.345]].
- 어느 쪽이든 만성은 교정 한계를 넘기지 않고, 개입에 대한 반응을 예측하기 어려워 나트륨을 자주 다시 잰다 [[harrison-21: 53장 p.344–345]].
- ADH 작용을 더하는 데스모프레신, 농축뇨에서 나트륨만 빠지는 생리식염수, 자유수를 더하는 저장성 수액은 방향이 반대다.

## 기전 — AVP 가 꺼지지 않아 자유수를 못 버린다
정상에서 AVP 는 혈장 삼투질농도 약 285 mOsm/kg 부터 분비되어, 집합관 주세포의 V2 수용체 → cAMP → 아쿠아포린-2 삽입으로 물을 재흡수한다. 이 역치 아래로 떨어지면 AVP 가 꺼져 묽은 소변으로 과잉의 물을 버린다 [[harrison-21: 53장 p.339]]. **SIADH(부적절 항이뇨 증후군, SIAD)** 에서는 AVP 분비가 제멋대로이거나, 낮은 삼투질농도에서 억제되지 않거나, 역치가 낮게 재설정되거나, V2 수용체 기능획득으로 AVP 없이도 작용한다 [[harrison-21: 53장 p.342]]. 갈증 역치도 낮아져 물을 계속 마신다.
- 「AVP escape」로 물 저류가 부종이 생길 만큼은 늘지 않는다 — 임상적으로 정상용적(엄밀히는 약간 용적 과다) [[harrison-21: 53장 p.343]].
- 약간 늘어난 용적으로 근위세뇨관 재흡수가 줄어 요나트륨이 오르고 혈청 요산이 낮아진다.
- 증상은 뇌세포 부종에서 온다(두통·오심·구토 → 경련·의식저하). 48시간 넘은 만성은 뇌세포가 삼투질을 내보내 적응하므로 증상이 가볍다 [[harrison-21: 53장 p.345]].

## 가르는 소견 — 정상용적·농축뇨·요나트륨
SIADH 는 정상용적 저나트륨혈증의 가장 흔한 원인이지만 **제외 진단**이다 — 갑상선기능저하, 2차(뇌하수체성) 부신부전(당질코르티코이드 결핍이 AVP 를 풀어놓는다), 이뇨제를 먼저 거른다 [[harrison-21: 53장 p.342]]. 저용질 섭취(맥주 포토마니아)와도 가른다.
- 검사: 혈장 삼투질농도(저삼투 확인 — 고혈당·가성저나트륨혈증 배제), 요삼투, 요나트륨·요칼륨, 용적 평가, TSH·오전 코르티솔, 요산.
- 원인: 폐질환(폐렴·결핵), 중추신경 질환(종양·지주막하출혈·수막염), 악성 종양(소세포폐암이 악성 종양 관련 SIADH 의 75%), 약물(SSRI 가 가장 흔함) [[harrison-21: 53장 p.343]].

## 선택 — 증상·경과·반응에 따라
치료를 정하는 세 가지 — 증상의 유무·중증도, 만성일 때 ODS 위험, 개입 반응의 예측 불가능성 [[harrison-21: 53장 p.345]].
- 원인 교정(약물 중단, 폐렴·종양 치료)은 어느 경우에나 함께 한다.
- 수분제한이 듣지 않으면 경구 요소, 푸로세마이드+염분 정제, 톨밥탄(V2 길항). 톨밥탄은 소세포폐암처럼 지속되는 SIADH 에 가장 알맞다 [[harrison-21: 53장 p.345]].

## 권고와 예외
과교정(24시간 8~10 mM 초과)이 생기면 포도당수와 데스모프레신으로 되돌려 ODS 를 막는다. 중증 저나트륨혈증은 처음부터 데스모프레신을 고정 투여하고 고장성식염수로 천천히 올리는 전략도 있다 [[harrison-21: 53장 p.346]]. 맥주 포토마니아·저칼륨혈증·알코올·영양실조는 ODS 고위험이라 더 조심한다. 이 두 경우를 빼면 데스모프레신은 SIADH 를 악화시키는 약이다.

## 시험 쟁점 — 충돌·맥락·새 근거
- **Z1 맥락 · 「중등도 증상」에 고장성식염수를 쓰는가** — 시험 기준: 해리슨은 급성·중증 증상(경련·의식저하)에 고장성식염수를, 증상이 가벼운 만성에 수분제한을 둔다 [[harrison-21: 53장 p.345]] / 다른 기준: 유럽 지침은 증상을 중등도(오심·혼돈·두통)와 중증(구토·경련·혼수)으로 나눠 중등도에도 고장성식염수 일회 주입을 권한다고 알려져 있으나 원문을 대조하지 못했다 [[?spasovski-2014]] / 왜 다른가: 증상 분류와 「급성·만성」 구분의 무게가 다르다 / 시험에서는: KMLE · USMLE 모두 가벼운 증상의 만성 SIADH 는 수분제한, 경련·혼수는 고장성식염수로 답한다.
