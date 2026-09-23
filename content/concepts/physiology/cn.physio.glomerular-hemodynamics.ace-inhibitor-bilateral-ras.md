---
id: cn.physio.glomerular-hemodynamics.ace-inhibitor-bilateral-ras
type: concept
topic: Physiology
see_also: [Nephrology, Cardiology]
date: 2026-09-23
updated: 2026-09-23
version: 1
outline: basic.organ-physio   # 기본틀 슬롯(content/outline/subjects.yaml) — 사구체 혈역학(임상 대조는 해리슨 278장)
confidence: medium
review_status: unreviewed
title: "사구체 혈역학 — 양측 신동맥협착에서 ACE억제제가 GFR 을 떨어뜨리는 이유"
objective: "수입·수출세동맥 저항이 사구체 모세혈관압과 GFR 을 정하는 원리로, 관류압이 낮아진 콩팥(양측 신동맥협착·단일 콩팥 협착)이 안지오텐신II 의 수출세동맥 수축에 기대어 GFR 을 지탱함을 설명하고, ACE억제제·ARB 가 이 보상을 없애 급성신손상을 일으키는 기전을 NSAID(수입세동맥 확장 차단) 기전과 구별한다"
objective_kind: 기전
condition: 양측 신동맥협착에서 ACE억제제 유발 급성신손상
exams: [usmle, kmle]
summary:
  - "GFR 은 사구체 모세혈관압에 달려 있고, 이 압력은 앞문(수입세동맥)과 뒷문(수출세동맥)의 저항이 정한다. 수입세동맥이 넓어지거나 수출세동맥이 좁아지면 모세혈관압이 올라 GFR 이 늘고, 반대면 준다."
  - "신동맥이 좁아져 관류압이 떨어지면 레닌-안지오텐신계가 켜진다 [[harrison-21: 278장 p.2088]]. 안지오텐신II 는 수출세동맥을 상대적으로 더 수축시켜, 들어오는 압력이 낮아도 사구체 모세혈관압과 GFR 을 붙잡아 둔다 — 이때 GFR 은 안지오텐신II 에 「의존」한다."
  - "ACE억제제·ARB 는 이 수출세동맥 수축을 없앤다. 협착 뒤의 콩팥은 여과압을 지탱할 수단을 잃어 GFR 이 급격히 떨어지고 크레아티닌이 오른다. 캡토프릴 신장스캔이 협착 쪽 관류 차이를 키워 보여 주는 것도 같은 원리다 [[harrison-21: 278장 p.2089]]."
  - "양측(또는 기능하는 단일 콩팥) 협착이어야 전체 GFR 이 크게 떨어진다. 한쪽 협착이면 반대쪽 콩팥이 메워 혈청 크레아티닌 변화가 작을 수 있다."
  - "ACE억제제·ARB 투여 중 GFR 이 떨어지면 신동맥협착을 의심하는 단서이며, 혈관 재개통을 고려하는 임상 요인으로 꼽힌다 [[harrison-21: 278장 p.2090 표 278-2]]."
pitfalls:
  - contrast: "ACE억제제 AKI vs NSAID AKI — 어느 세동맥인가"
    point: "ACE억제제·ARB 는 수출세동맥의 안지오텐신II 수축을 없애 여과압을 낮춘다. NSAID 는 프로스타글란딘이 유지하던 수입세동맥 확장을 막아 들어오는 혈류를 줄인다. 두 약 모두 「세동맥 톤」을 바꿔 GFR 을 떨어뜨리지만 작용하는 문이 다르고, ACE억제제는 수입세동맥을 직접 수축시키지 않는다."
    exception: "관류가 떨어진 콩팥(심부전·탈수·간경변)에서는 두 기전이 겹쳐 이뇨제+ACE억제제+NSAID 조합이 특히 위험하다."
    covers: ["usmle-2026-0039:B"]
  - contrast: "크레아티닌 상승 = 약물의 직접 세뇨관 독성?"
    point: "혈역학적 GFR 감소는 구조 손상이 아니라 여과압의 변화이므로 약을 끊으면 대개 되돌아간다. 세뇨관 괴사처럼 원주·세뇨관 표지로 시작하는 손상과 구별한다."
  - contrast: "ACE억제제가 협착 부위에 혈전을 만든다?"
    point: "급격한 크레아티닌 상승은 혈전·경색이 아니라 여과압 소실로 설명된다. 신경색은 옆구리 통증·발열·LDH 의 극단적 상승이 동반된다 [[harrison-21: 278장 p.2090]]."
    cites: ["harrison-21: 278장 p.2090"]
tables:
  - id: arteriole-effects
    title: "세동맥 톤과 GFR"
    role: comparison
    span: column
    section: "기전에서 소견으로"
    columns: ["변화", "사구체 모세혈관압", "GFR", "예"]
    rows:
      - ["수입세동맥 확장", "↑", "↑", "프로스타글란딘"]
      - ["수입세동맥 수축", "↓", "↓", "NSAID(확장 차단)·칼시뉴린억제제"]
      - ["수출세동맥 수축", "↑", "↑(유지)", "안지오텐신II"]
      - ["수출세동맥 확장", "↓", "↓", "ACE억제제·ARB"]
    note: "표준 신장 생리. 임상 대조는 harrison-21: 278장 p.2088–2090"
checks:
  - q: "양측 신동맥협착 환자에서 GFR 이 안지오텐신II 에 의존하는 이유는?"
    a: "관류압이 낮아 수출세동맥을 안지오텐신II 로 수축시켜야만 사구체 모세혈관압을 유지할 수 있기 때문이다."
  - q: "NSAID 로 인한 혈역학적 GFR 감소는 어느 세동맥의 변화인가?"
    a: "프로스타글란딘 매개 수입세동맥 확장이 차단된 수입세동맥 쪽 변화다."
sources:
  - id: harrison-21
    org: "McGraw Hill"
    title: "Harrison's Principles of Internal Medicine, 21st ed. — Chapter 278: Renovascular Disease"
    kind: textbook
    year: 2022
    citation: "Loscalzo J, Kasper DL, Longo DL, et al (eds). Harrison's Principles of Internal Medicine, 21e. 278장 p.2088–2090"
    checked_at: 2026-09-23
    checked: "본문 대조(드라이브 문서) — p.2088 관류압 감소 → 레닌-안지오텐신계 활성·나트륨 배설 감소·교감신경 활성, 초기 안지오텐신 의존 고혈압; p.2089 표 278-1 캡토프릴 신장스캔(캡토프릴에 의한 여과압 저하가 관류 차이를 키움); p.2090 표 278-2 혈관재개통 고려 요인에 「ACE억제제·ARB 치료 중 GFR 감소」, 신경색의 옆구리 통증·발열·LDH 상승. 수입·수출세동맥 기전 자체는 이 장에 서술되지 않아 표준 생리로 남긴다"
    verified: text
variants:
  - id: v1
    of: usmle-2026-0039
    flip: true
    changed: "Replaced lisinopril in bilateral renal artery stenosis with high-dose ibuprofen in a patient with volume-contracted heart failure (no ACE inhibitor started) → the GFR fall now comes from loss of prostaglandin-mediated afferent dilation, so the answer moves from 'loss of angiotensin II efferent constriction' to 'afferent arteriolar constriction'"
    context: "Clue changed so the answer changes — NSAID instead of ACE inhibitor"
    stem: "A 76-year-old woman with chronic heart failure on stable doses of furosemide and metoprolol takes ibuprofen 800 mg three times daily for 10 days for knee osteoarthritis. Her serum creatinine rises from 1.1 to 2.6 mg/dL. Urinalysis shows no casts, protein, or blood. Renal ultrasound shows normal-sized kidneys without hydronephrosis, and Doppler shows no renal artery stenosis. Which of the following best explains the decline in her glomerular filtration rate?"
    choices:
      - "A. Loss of angiotensin II-mediated efferent arteriolar constriction"
      - "B. Loss of prostaglandin-mediated afferent arteriolar dilation, reducing glomerular capillary pressure"
      - "C. Immune complex deposition in the glomerular basement membrane"
      - "D. Obstruction of the renal tubules by drug crystals"
      - "E. Acute thrombosis of the main renal artery"
    answer: "B"
    explanation: "In a volume-contracted kidney (heart failure plus loop diuretic), prostaglandins dilate the afferent arteriole to preserve glomerular perfusion. NSAIDs block prostaglandin synthesis, the afferent arteriole narrows, glomerular capillary pressure falls, and GFR drops. No ACE inhibitor or ARB is involved and there is no renal artery stenosis, so the efferent (angiotensin II) mechanism of the original item does not apply. A bland urinalysis argues against glomerulonephritis and crystal nephropathy."
    kind: application
  - id: v2
    of: usmle-2026-0039
    flip: false
    changed: "Changed age/sex (69-year-old woman), drug name (enalapril instead of lisinopril), presentation (routine follow-up after a flash pulmonary edema admission), and order of facts; kept bilateral renal artery stenosis + new ACE inhibitor + sharp creatinine rise with normal potassium → answer is still loss of angiotensin II efferent constriction"
    context: "Surface changed, answer the same — enalapril after flash pulmonary edema"
    stem: "A 69-year-old woman returns for follow-up 10 days after being started on enalapril. She was recently hospitalized for sudden pulmonary edema with a blood pressure of 188/104 mm Hg, and CT angiography during that admission showed 80% stenosis of both renal arteries. Her serum creatinine was 1.2 mg/dL before enalapril and is now 3.1 mg/dL; potassium is 4.8 mEq/L. Urinalysis is bland. Which of the following best explains the change in her renal function?"
    choices:
      - "A. Enalapril-induced acute interstitial nephritis"
      - "B. Direct afferent arteriolar constriction by enalapril"
      - "C. Removal of angiotensin II-mediated efferent arteriolar constriction that had maintained glomerular filtration pressure"
      - "D. Cholesterol emboli released from the stenotic segments"
      - "E. Enalapril-induced thrombosis of both renal arteries"
    answer: "C"
    explanation: "The key facts are unchanged: bilateral renal artery stenosis lowers renal perfusion pressure, so GFR depends on angiotensin II constricting the efferent arteriole. An ACE inhibitor removes that support, glomerular capillary pressure falls, and creatinine rises sharply within days [[harrison-21: 278장 p.2088–2090]]. ACE inhibitors do not constrict the afferent arteriole; a bland urinalysis and the timing argue against interstitial nephritis, and atheroemboli typically follow an angiographic procedure rather than drug initiation."
    kind: application
---

## 정의
**사구체 여과율(GFR)** 은 사구체 모세혈관압에서 보우만주머니압과 혈장 교질삼투압을 뺀 순여과압과 여과 계수로 정해진다. 이 중 급격히 변하는 것은 모세혈관압이며, 모세혈관압은 앞뒤 세동맥 저항으로 조절된다. 이 정리본의 목표는 **양측 신동맥협착(또는 단일 기능 콩팥의 협착)에서 ACE억제제·ARB 가 급성신손상을 일으키는 기전** 이다.

## 병태생리
정상에서 콩팥은 관류압이 넓은 범위에서 변해도 수입세동맥 근원성 반응과 세뇨관-사구체 되먹임으로 GFR 을 일정하게 지킨다(자가조절). 신동맥이 심하게 좁아져 협착 뒤 관류압이 이 범위 아래로 떨어지면, 콩팥은 레닌을 분비해 안지오텐신II 를 만든다 [[harrison-21: 278장 p.2088]]. 안지오텐신II 는 (1) 전신 혈관을 수축시켜 신관류압을 끌어올리고 (2) 수출세동맥을 수입세동맥보다 더 수축시켜 사구체 모세혈관압을 지탱한다. 이 두 번째 효과 때문에 협착 뒤 콩팥의 GFR 은 안지오텐신II 에 의존하게 된다.

## 기전에서 소견으로
ACE억제제는 안지오텐신II 생성을 막고 ARB 는 수용체를 막아, 수출세동맥이 풀린다. 협착 탓에 들어오는 압력은 낮은데 뒷문까지 열리면 사구체 모세혈관압이 떨어지고 GFR 이 급감한다 — 투약 며칠~1주 안의 크레아티닌 급상승. 이것은 혈역학적 변화이므로 소변검사는 대개 깨끗하고, 약을 끊으면 대개 되돌아간다. 한쪽 협착이면 건강한 반대쪽이 메워 크레아티닌 변화가 작다(세동맥 표). 같은 원리로 캡토프릴 신장스캔은 캡토프릴이 여과압을 떨어뜨려 좌우 관류 차이를 키운다 [[harrison-21: 278장 p.2089]].

## 감별
- **NSAID 유발**: 수입세동맥 쪽 — 프로스타글란딘 매개 확장이 막혀 들어오는 혈류가 준다. 탈수·심부전·간경변에서 잘 생긴다.
- **급성 세뇨관 괴사·간질신염**: 원주·백혈구·세뇨관 손상 소견이 있다.
- **신경색·혈전**: 옆구리 통증·발열·백혈구 증가·LDH 극단적 상승 [[harrison-21: 278장 p.2090]].
- **콜레스테롤 색전**: 혈관조영·혈관 수술 뒤 1~14일, 그물울혈반·발가락 괴저·일시적 호산구증가 [[harrison-21: 278장 p.2089–2090]].

## 검사
혈청 크레아티닌·칼륨을 ACE억제제·ARB 시작 전과 시작 뒤 짧은 간격으로 잰다. 신동맥협착 확인은 도플러 초음파(최고 수축기 속도 >200 cm/s 면 의미 있는 협착), CT 혈관조영 등으로 한다 [[harrison-21: 278장 p.2089]].

## 치료
ACE억제제·ARB 로 GFR 이 떨어지면 약을 끊거나 줄이고 다른 강압제로 바꾸며, 크레아티닌 회복을 확인한다. 동맥경화성 신동맥협착의 기본 치료는 레닌-안지오텐신계 차단을 포함한 약물 치료·금연·스타틴·아스피린이지만, 이 약으로 GFR 이 떨어지는 것은 혈관 재개통을 고려하는 요인이다 [[harrison-21: 278장 p.2089–2090]].

## 권고와 예외
혈압이 조절되고 신기능이 안정적이면 약물 치료와 추적이 재개통과 비슷한 성적을 보였다. 반대로 신기능의 빠른·반복 감소, ACE억제제·ARB 중 GFR 감소, 설명되지 않는 반복 심부전은 재개통을 고려하는 요인이다 [[harrison-21: 278장 p.2089–2090 표 278-2]].

## 시험 쟁점 — 충돌·맥락·새 근거
- 해당 없음(대조: 해리슨 278장 p.2088–2090)
