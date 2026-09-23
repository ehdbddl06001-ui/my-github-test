---
id: cn.cardio.qrs-axis.limb-lead-polarity
type: concept
topic: Cardiology
see_also: [Pulmonology, Pediatrics]
date: 2026-09-23
updated: 2026-09-23
version: 1
outline: h240            # 기본틀 슬롯(content/outline/subjects.yaml) — 해리슨 240장 Electrocardiography
confidence: medium
review_status: unreviewed
title: "평균 QRS 전기축 — 유도 I 과 aVF 의 극성으로 사분면을 정한다"
objective: "사지유도가 평균 QRS 벡터를 각 유도 축에 투영한 값임을 이해하고, 유도 I 과 aVF(필요하면 II)의 QRS 순면적 부호로 정상축·좌축편위·우축편위·극단축·결정 불가를 가르며, 우축편위의 원인(젊고 마른 체형의 정상 변이·전극 뒤바뀜·우심실 부하·측벽경색·좌각후섬유속차단)을 차례로 따진다"
objective_kind: 진단
condition: 12유도 심전도의 전두면 QRS 축 판독
exams: [usmle, kmle]
summary:
  - "사지유도 여섯 개는 같은 심실 탈분극을 전두면의 여섯 방향에서 본다. 탈분극이 유도의 양극 쪽으로 향하면 위로(양성), 음극 쪽으로 향하면 아래로(음성) 그려지고, 유도 축에 수직이면 위아래가 같은 이상성 파형이 된다 [[harrison-21: 240장 p.1825]]."
  - "유도 I(0°)과 aVF(+90°)는 서로 수직이라 두 유도의 부호만으로 평균 QRS 벡터가 어느 사분면에 있는지 정해진다. I 음성 + aVF 양성 = +90°~+180°, 우축편위 [[harrison-21: 240장 p.1825]]."
  - "부호는 R 파 높이가 아니라 **순면적(양성 − 음성)**으로 판단한다. 작은 r 뒤 깊은 S(rS)는 음성이다."
  - "우축편위는 젊은 성인·소아의 정상 변이일 수 있지만, 팔 전극 뒤바뀜·우심실 부하·측벽경색·우흉심·좌측 기흉·좌각후섬유속차단도 만든다. 좌각후섬유속차단은 드물어 다른 원인을 모두 배제한 뒤에만 붙인다 [[harrison-21: 240장 p.1826]] [[harrison-21: 240장 p.1828]]."
  - "정상 범위의 경계값은 자료마다 다르다 — 해리슨은 −30°~+100°, 많은 시험 문항은 −30°~+90° 를 쓴다(아래 시험 쟁점)."
criteria:
  - id: axis-ranges-harrison
    name: 전두면 QRS 축의 범위(해리슨)
    kind: 정의
    population: "성인 12유도 심전도"
    statement: "정상 QRS 축은 약 −30°~+100°. −30° 보다 음이면 좌축편위, +90~+100° 보다 양이면 우축편위 [[harrison-21: 240장 p.1826]]"
    exceptions: "경계값(+90° 대 +100°)은 자료마다 다르다 — 시험 문항은 보기에 적힌 범위를 따른다"
    source: harrison-21
    basis: current
    exams: [usmle, kmle]
  - id: lpfb-harrison
    name: 좌각후섬유속차단의 축 기준
    kind: 진단 기준
    population: "QRS 폭이 거의 정상인 우축편위"
    statement: "QRS 축이 +110~+120° 보다 오른쪽. 단독으로는 매우 드물어 우축편위의 다른 원인을 배제해야 한다 [[harrison-21: 240장 p.1828]]"
    exceptions: "AHA/ACCF/HRS 2009 권고의 세부 형태 기준(I·aVL rS, III·aVF qR)은 원문 미대조 [[?aha-ivcd-2009]]"
    source: harrison-21
    basis: current
    exams: [usmle]
sources:
  - id: harrison-21
    org: "McGraw Hill"
    title: "Harrison's Principles of Internal Medicine, 21st ed. — Chapter 240: Electrocardiography"
    kind: textbook
    year: 2022
    citation: "Loscalzo J, Kasper DL, Longo DL, et al (eds). Harrison's Principles of Internal Medicine, 21e. 240장(Goldberger AL) p.1824-1828, 1830"
    checked_at: 2026-09-23
    checked: "본문 대조(드라이브 240장 문서) — p.1825 유도 극성 규칙(양극 쪽 = 양성, 수직 = 이상성)·육축 도해(그림 240-4, I 0°·aVF +90°·III +120°) · p.1826 정상 QRS 축 <−30°~+100°, 좌축편위 −30° 초과, 우축편위 +90~+100° 초과, 우축편위 원인(소아·젊은 성인 정상 변이, 좌우 팔 전극 뒤바뀜, 급성·만성 우심실 부하, 측벽경색, 우흉심, 좌측 기흉, 좌각후섬유속차단), 우심실비대는 대개 우축편위 동반 · p.1828 섬유속차단은 QRS 폭을 크게 늘리지 않고 축만 옮김, 좌각후섬유속차단 축 +110~+120° 초과·단독은 극히 드물어 다른 원인 배제 필요 · p.1824 전도계(좌다발가지 앞·뒤 섬유속) · p.1827 심전도의 비대 진단 한계·심초음파 · p.1830 판독 14항목(7번째 평균 QRS 축)·이전 심전도 비교"
    verified: text
  - id: aha-ivcd-2009
    org: "American Heart Association / American College of Cardiology Foundation / Heart Rhythm Society"
    title: "Recommendations for the Standardization and Interpretation of the Electrocardiogram, Part III: Intraventricular Conduction Disturbances"
    kind: guideline
    year: 2009
    citation: "Surawicz B, Childers R, Deal BJ, Gettes LS. Circulation 2009;119:e235-e240 (문항 해설에 적힌 권고)"
    url: "https://www.ahajournals.org/journal/circ"
    checked_at: 2026-09-23
    checked: "서지만 — 문항 해설이 근거로 든 권고. 이 컨테이너에서 원문을 열지 못해 섬유속차단 형태 기준 문구를 대조하지 못했다(url 은 학술지 첫 화면, 논문 DOI 미확인)"
    verified: citation
tables:
  - id: axis-quadrants
    title: "유도 I · aVF 극성으로 정하는 축의 사분면"
    role: criteria
    span: column
    section: 감별
    columns: ["축", "유도 I", "유도 aVF", "보탤 확인"]
    rows:
      - ["정상(0°~+90°)", "양성", "양성", "—"]
      - ["정상 또는 좌축(0°~−90°)", "양성", "음성", "II 양성이면 0°~−30° 정상, II 음성이면 −30° 넘은 좌축편위"]
      - ["우축편위(+90°~+180°)", "**음성**", "**양성**", "먼저 팔 전극 뒤바뀜 배제 [[harrison-21: 240장 p.1826]]"]
      - ["극단축(−90°~±180°)", "음성", "음성", "심실 기원 리듬·전극 오류 확인"]
      - ["결정 불가", "등전위", "등전위", "모든 사지유도가 이상성"]
    note: "유도 I 과 aVF 가 서로 수직이라는 점이 이 표의 근거다(그림 240-4) [[harrison-21: 240장 p.1825]]. 우축편위의 상한(+90° 대 +100°)은 시험 쟁점 절 참조."
  - id: rad-causes
    title: "우축편위 — 원인과 가르는 단서"
    role: differential
    span: full
    section: 감별
    columns: ["원인", "기전", "함께 보이는 소견", "판단"]
    rows:
      - ["정상 변이(소아·젊은 성인, 마르고 키 큰 체형)", "심장이 세로로 서 있어 벡터가 아래·오른쪽으로 기움", "QRS 폭·전압·재분극 정상", "다른 원인이 없을 때만 [[harrison-21: 240장 p.1826]]"]
      - ["좌우 팔 전극 뒤바뀜", "유도 I 이 거꾸로 기록됨", "I 에서 P·QRS·T 모두 음성, aVR 양성", "다시 붙여 재기록 [[harrison-21: 240장 p.1826]]"]
      - ["우심실 압력 부하(폐고혈압·폐동맥판 협착)", "두꺼운 우심실이 벡터를 오른쪽으로 당김", "V1 R ≥ S 또는 qR, 우흉부 ST-T 변화", "심초음파로 확인 [[harrison-21: 240장 p.1826]]"]
      - ["급성 폐색전증", "급성 우심실 확장", "동빈맥, S1Q3T3, 우각차단", "임상 맥락으로 [[harrison-21: 240장 p.1826]]"]
      - ["측벽경색", "측벽(왼쪽) 기전력 소실", "I·aVL 의 Q 파", "병력·효소 [[harrison-21: 240장 p.1826]]"]
      - ["좌각후섬유속차단", "하벽이 늦게 탈분극", "QRS 폭 거의 정상, 축 +110~+120° 초과", "위 원인을 모두 배제한 뒤 [[harrison-21: 240장 p.1828]]"]
    note: "해리슨은 이 밖에 우흉심·좌측 기흉도 우축편위 원인으로 적는다 [[harrison-21: 240장 p.1826]]."
pitfalls:
  - contrast: "우축편위 vs 정상축 — 「젊고 마른 사람이니 세로축, 정상」"
    point: "마른 젊은 성인은 축이 +90° 가까이 서는 일이 흔하지만, 축 판정은 체형이 아니라 유도 I 의 QRS 순면적이 정한다. 유도 I 이 rS(작은 r, 깊은 S)로 순면적이 음성이면 벡터가 +90° 를 넘어 오른쪽으로 간 것이다 — 그 뒤에 「이 우축편위가 정상 변이인가」를 따진다 [[harrison-21: 240장 p.1826]]. 순서가 거꾸로면(체형 → 정상) 우심실 부하·섬유속차단을 놓친다."
    exception: "유도 I 이 거의 등전위라면 축은 약 +90° 로 경계선이다 — 보기에 적힌 범위(+90° 또는 +100°)를 확인한다."
    covers: ["imaging-2026-0011:B"]
  - contrast: "유도 II 만 보기 — 「II 가 양성이니 정상」"
    point: "유도 II(+60°)는 정상축과 우축편위(+90°~+150°) 모두에서 양성이다. II 는 좌축편위(−30° 넘음)를 가를 때 쓰는 유도이고, 오른쪽 경계는 유도 I 이 가른다 [[harrison-21: 240장 p.1825]]."
    exception: "I 양성·aVF 음성일 때는 II 가 정상(0°~−30°)과 좌축편위를 가르는 결정 유도가 된다."
  - contrast: "좌각후섬유속차단 vs 우축편위 — 「축이 오른쪽이면 섬유속차단」"
    point: "좌각후섬유속차단은 단독으로 매우 드물고 +110~+120° 를 넘어야 하며, 정상 변이·우심실 부하·측벽경색 같은 흔한 원인을 먼저 배제해야 붙일 수 있는 진단이다 [[harrison-21: 240장 p.1828]]. 우축편위라는 「소견」과 섬유속차단이라는 「원인」을 같은 것으로 쓰지 않는다."
    exception: "보기가 축의 범위만 묻는다면 원인 진단 없이 「우축편위」가 답이다."
diagram:
  title: "전두면 QRS 축 — 유도 I 에서 시작"
  nodes:
    - {id: start, kind: start, text: "12유도 심전도 — 보정(10 mm/mV)·전극 위치 확인 뒤 사지유도를 본다"}
    - {id: lead1, kind: decision, text: "유도 I 의 QRS 순면적(양성 − 음성)은?"}
    - {id: iso, kind: info, text: "가장 등전위인 사지유도를 찾는다 — 축은 그 유도 축에 수직, 그 방향으로 I 부호를 다시 판정"}
    - {id: avf_p, kind: decision, text: "유도 I 양성 — aVF 순면적은?"}
    - {id: avf_n, kind: decision, text: "유도 I 음성 — aVF 순면적은?"}
    - {id: lead2, kind: decision, text: "유도 II 순면적은?"}
    - {id: normal, kind: end, text: "정상축(−30°~+90°)"}
    - {id: lad, kind: end, text: "좌축편위(−30° 넘음) — 좌각전섬유속차단·좌심실비대·하벽경색 평가"}
    - {id: rad, kind: decision, text: "우축편위(+90°~+180°) — I 에서 P·T 도 음성인가(전극 뒤바뀜)?"}
    - {id: redo, kind: end, text: "팔 전극을 바로 붙여 재기록"}
    - {id: cause, kind: step, text: "원인 평가 — 체형·나이, V1 R/S, 우흉부 ST-T, I·aVL Q 파, QRS 폭"}
    - {id: extreme, kind: end, text: "극단축 — 심실 기원 리듬·전극 오류 확인"}
  edges:
    - {from: start, to: lead1}
    - {from: lead1, to: avf_p, label: "양성"}
    - {from: lead1, to: avf_n, label: "음성"}
    - {from: lead1, to: iso, label: "거의 등전위"}
    - {from: iso, to: avf_p, label: "다시 봐도 양성 쪽"}
    - {from: iso, to: avf_n, label: "다시 봐도 음성 쪽"}
    - {from: avf_p, to: normal, label: "양성"}
    - {from: avf_p, to: lead2, label: "음성"}
    - {from: lead2, to: normal, label: "양성(0°~−30°)"}
    - {from: lead2, to: lad, label: "음성"}
    - {from: avf_n, to: rad, label: "양성"}
    - {from: avf_n, to: extreme, label: "음성"}
    - {from: rad, to: redo, label: "예"}
    - {from: rad, to: cause, label: "아니오"}
diagram_notes:
  - "「순면적」은 R 과 S(와 q)의 넓이 차이다. 높은 R 이라도 더 깊은 S 가 따라오면 음성이다."
  - "우축편위의 상한을 +90° 로 둘지 +100° 로 둘지는 자료마다 다르다 — 해리슨은 정상 범위를 +100° 까지 본다 [[harrison-21: 240장 p.1826]]."
  - "원인 평가(cause)에서 다른 이상이 없고 젊고 마른 체형이면 정상 변이로 두고, QRS 폭이 거의 정상인데 +110~+120° 를 넘고 다른 원인이 모두 없을 때만 좌각후섬유속차단을 붙인다 [[harrison-21: 240장 p.1828]]."
  - "축은 판독 14항목 가운데 하나일 뿐이다 — 리듬·간격·Q 파·ST-T 를 함께 본다 [[harrison-21: 240장 p.1830]]."
checks:
  - q: "유도 I 음성, aVF 양성이면 축은?"
    a: "+90°~+180°, 우축편위."
  - q: "유도 I 양성, aVF 음성일 때 정상과 좌축편위를 가르는 유도는?"
    a: "유도 II — 양성이면 0°~−30° 정상, 음성이면 −30° 넘은 좌축편위."
  - q: "유도 I 이 rS 일 때 부호는?"
    a: "순면적이 음성이므로 음성이다. R 이 있다는 것만으로 양성이라 하지 않는다."
  - q: "우축편위를 보면 가장 먼저 배제할 기술적 원인은?"
    a: "좌우 팔 전극 뒤바뀜 — 유도 I 에서 P·QRS·T 가 모두 뒤집힌다."
  - q: "좌각후섬유속차단을 붙이기 전에 필요한 것은?"
    a: "축이 +110~+120° 를 넘고, 정상 변이·우심실 부하·측벽경색 같은 다른 우축편위 원인을 배제하는 것."
variants:
  - id: v1
    of: imaging-2026-0011
    flip: true
    changed: "유도 I 을 rS(순면적 음성)에서 qR(순면적 양성)로 바꾸고 aVF 양성은 유지 → 벡터가 0°~+90° 사분면으로 들어와 답이 「우축편위」에서 「정상축」으로 바뀜"
    context: "Changed clue flips the answer — lead I now net positive"
    stem: "A 23-year-old woman is evaluated before starting college athletics. She has no cardiopulmonary symptoms and takes no medications. She is slender. Blood pressure is 112/70 mm Hg and pulse is 66/min and regular. A 12-lead ECG shows sinus rhythm and a QRS duration of 0.08 s. In lead I the QRS complex is a small q followed by a tall R with a small s (net positive); leads II, III, and aVF each show a dominant R wave. Which of the following best describes the mean QRS axis in the frontal plane?"
    choices: ["A. Right axis deviation (+90° to +180°)", "B. Normal axis (−30° to +90°)", "C. Left axis deviation (−30° to −90°)", "D. Extreme (northwest) axis (−90° to −180°)", "E. Indeterminate axis (isoelectric in all limb leads)"]
    answer: "B"
    explanation: "Lead I (0°) and aVF (+90°) are perpendicular, so their polarities place the mean QRS vector in a quadrant. Both are net positive here, which puts the axis between 0° and +90° — a normal axis [[harrison-21: 240장 p.1825]]. In the original item lead I was rS (net negative) with aVF positive, which moves the vector past +90° into right axis deviation; the lean body habitus is the same in both cases and does not decide the axis. Left axis deviation would need a negative lead II and aVF, and an extreme axis would need both I and aVF negative."
    kind: application
  - id: v2
    of: imaging-2026-0011
    flip: false
    changed: "나이·성별(17세 남자 고교 수영선수)·내원 경위(학교 검진)·제시 순서를 바꾸고 「유도 I rS(순면적 음성) + III·aVF 양성, 좁은 QRS」는 유지 → 답은 여전히 우축편위"
    context: "Surface details change, answer stays — adolescent swimmer at school screening"
    stem: "A 17-year-old boy on his high school swim team has a screening ECG as part of a school sports program. He feels well and has never fainted. Examination shows a lean build and no murmurs. The tracing shows sinus rhythm at 64/min with a QRS duration of 0.08 s. Leads III and aVF show a qR pattern. Lead I shows a small r wave followed by a deeper S wave. Lead II is upright. Which of the following best describes the mean QRS axis in the frontal plane?"
    choices: ["A. Normal axis (−30° to +90°)", "B. Left axis deviation (−30° to −90°)", "C. Right axis deviation (+90° to +180°)", "D. Extreme (northwest) axis (−90° to −180°)", "E. Indeterminate axis (isoelectric in all limb leads)"]
    answer: "C"
    explanation: "Lead I is net negative (r smaller than S) and aVF is net positive, so the mean QRS vector points downward and to the right: +90° to +180°, right axis deviation [[harrison-21: 240장 p.1825]]. The upright lead II does not help, because lead II is positive in both the normal range and right axis deviation. Age, sex, sport, and setting differ from the original item, but the deciding clue — the polarity of leads I and aVF — is the same. Right axis deviation can be a normal variant in young adults, but that is a statement about cause, not about the axis itself [[harrison-21: 240장 p.1826]]."
    kind: application
---

## 정의
평균 QRS 전기축은 심실 탈분극 전체를 하나의 벡터로 합쳤을 때 그 벡터가 전두면에서 가리키는 방향이다. 유도 I 의 양극(왼쪽)을 0° 로 두고, 아래쪽을 양(+), 위쪽을 음(−)으로 잰다 [[harrison-21: 240장 p.1825]]. 이 정리본의 목표는 **사지유도의 극성만으로 축의 사분면을 정하고, 우축편위가 나왔을 때 원인을 어떤 순서로 따지는지**다.

## 병태생리
**정상 기능.** 탈분극은 동결절에서 시작해 방실결절·His 다발을 지나 좌우 다발가지와 Purkinje 섬유로 퍼진다. 좌다발가지는 앞·뒤 섬유속으로 갈라진다 [[harrison-21: 240장 p.1824]]. 좌심실이 더 두꺼워 두 심실이 함께 탈분극할 때의 합 벡터는 왼쪽·뒤로 향하고 [[harrison-21: 240장 p.1825]], 전두면에서는 대개 왼쪽 아래(0°~+90° 부근)를 가리킨다. 해리슨의 정상 심전도 예시는 약 +70° 다 [[harrison-21: 240장 p.1826]].

**유도가 벡터를 「보는」 방식.** 각 사지유도는 같은 사건을 다른 각도에서 찍는 카메라와 같다. 탈분극이 유도의 양극 쪽으로 향하면 위로, 음극 쪽으로 향하면 아래로 그려지며, 유도 축에 수직이면 위아래가 같은 이상성 파형이 된다 [[harrison-21: 240장 p.1825]]. 그래서 각 유도의 QRS 순면적은 평균 벡터를 그 유도 축에 투영한 값이다.

**축이 움직이는 기전.** 평균 벡터는 늦게 또는 더 많이 탈분극하는 쪽으로 기운다. 우심실이 두꺼워지면 오른쪽으로 [[harrison-21: 240장 p.1826]], 한 섬유속이 막히면 그 섬유속이 맡던 부위가 늦게 탈분극해 그쪽으로 기운다 — 좌각전섬유속차단은 왼쪽(위)으로, 좌각후섬유속차단은 오른쪽(아래)으로 [[harrison-21: 240장 p.1828]]. 경색으로 한쪽 벽의 기전력이 없어지면 벡터는 반대쪽으로 밀린다(측벽경색 → 우축). 심장이 세로로 서 있는 마른 체형·젊은 나이에서도 벡터가 아래·오른쪽으로 기운다.

## 기전에서 소견으로
- **유도 I 음성**: 벡터가 유도 I 의 음극(180°) 쪽 반원, 즉 +90° 보다 오른쪽에 있다. 작은 r 뒤 깊은 S(rS)는 순면적 음성이다.
- **aVF 양성**: 벡터가 아래쪽(0°~+180°) 반원에 있다.
- **둘을 합치면**: I 음성 + aVF 양성 = 오른쪽 아래 사분면(+90°~+180°), 우축편위. 유도 III(+120°)과 aVF 가 크게 양성(qR)인 것도 같은 뜻이다.
- **가장 등전위인 유도**: 축은 그 유도에 수직이다 — 사분면을 정한 뒤 각도를 좁힐 때 쓴다 [[harrison-21: 240장 p.1825]].
- **QRS 폭**: 섬유속차단은 QRS 폭을 크게 늘리지 않고 축만 옮긴다. 다발가지 차단은 120 ms 이상으로 넓힌다 [[harrison-21: 240장 p.1828]].

## 감별
사분면은 표 「유도 I · aVF 극성으로 정하는 축의 사분면」으로 정하고, 우축편위가 나오면 표 「우축편위 — 원인과 가르는 단서」 순서로 따진다. 핵심은 순서다.
1. **기술적 원인** — 좌우 팔 전극 뒤바뀜은 유도 I 을 통째로 뒤집는다 [[harrison-21: 240장 p.1826]].
2. **구조적 원인** — 우심실 부하(대개 V1 의 큰 R 과 함께), 급성 폐색전증, 측벽경색, 우흉심, 좌측 기흉 [[harrison-21: 240장 p.1826]].
3. **정상 변이** — 소아·젊은 성인. 다른 이상이 없을 때만 [[harrison-21: 240장 p.1826]].
4. **좌각후섬유속차단** — +110~+120° 를 넘고 위 원인이 모두 없을 때만. 단독으로는 매우 드물다 [[harrison-21: 240장 p.1828]].

## 검사
축 판독은 체계적 판독 14항목(보정·리듬·심박수·PR·QRS·QT·**평균 QRS 축**·P 파·전압·R 파 진행·Q 파·ST·T·U) 가운데 하나다 [[harrison-21: 240장 p.1830]]. 순서는 ① 보정과 전극 위치 확인 → ② 유도 I 순면적 → ③ aVF 순면적 → ④ (I 양성·aVF 음성이면) 유도 II → ⑤ 가장 등전위인 유도로 각도 좁히기. 이전 심전도와 비교하면 새로 생긴 축 변화(섬유속차단·경색)를 가를 수 있다 [[harrison-21: 240장 p.1830]]. 우축편위에 우심실 부하 소견이 함께 있으면 심초음파로 구조를 확인한다 — 심전도는 비대 진단의 민감도·특이도가 제한적이다 [[harrison-21: 240장 p.1827]].

## 치료
축 자체는 치료 대상이 아니다. 판독 뒤의 행동은 원인에 따른다. 전극 뒤바뀜이면 재기록, 증상 없는 젊은 사람의 단독 우축편위이고 다른 판독 항목이 모두 정상이면 추가 검사 없이 기록해 둔다. 우심실 부하 소견·흉통·호흡곤란이 함께 있으면 원인 질환(폐고혈압·폐색전증) 평가로 넘어간다. **재평가**: 이전 심전도와 비교해 축이 새로 오른쪽으로 옮겨 갔다면 정상 변이로 두지 않는다.

## 권고와 예외
- 사분면은 유도 I 과 aVF 두 개로 정한다. II 는 좌축편위 경계(−30°)를 가를 때만 결정 유도다.
- 부호는 순면적으로 — rS 는 음성.
- 우축편위는 「소견」이다. 원인(정상 변이·우심실 부하·섬유속차단)은 전극 확인 → 구조 → 정상 변이 → 섬유속차단 순으로 붙인다.
- 섬유속차단의 형태 기준(AHA/ACCF/HRS 2009)은 원문 미대조다 [[?aha-ivcd-2009]].

## 시험 쟁점 — 충돌·맥락·새 근거
- **Z1 맥락 · 정상축의 오른쪽 경계(+90° 대 +100°)** — 시험 기준: 문항 보기에 적힌 범위(이 문항은 정상 −30°~+90°, 우축편위 +90°~+180°) / 다른 기준: 해리슨은 정상을 −30° 미만~+100° 로, 우축편위를 「+90~+100° 초과」로 적는다 [[harrison-21: 240장 p.1826]] / 왜 다른가: 경계값은 합의된 한 숫자가 아니라 관례이며, 교과서마다 +90° 또는 +100° 를 쓴다 / 시험에서는: USMLE · KMLE 모두 사분면 문항은 대개 +90° 경계를 쓴다 — 축이 +90°~+100° 사이로 애매하면 보기의 정의를 따른다.
- **Z2 맥락 · 좌각후섬유속차단의 축 기준** — 시험 기준: 우축편위 + 좁은 QRS + 다른 원인 배제 [[harrison-21: 240장 p.1828]] / 다른 기준: 해리슨은 축 문턱을 「+110~+120° 초과」로 적는다 [[harrison-21: 240장 p.1828]]. 문항 해설이 든 AHA/ACCF/HRS 2009 의 문턱은 원문을 보지 못했다 [[?aha-ivcd-2009]] / 왜 다른가: 섬유속차단은 배제 진단이라 문턱과 형태 기준이 자료마다 조금씩 다르다 / 시험에서는: USMLE 는 「우축편위 + 다른 원인 없음」, KMLE 는 좌각전섬유속차단(좌축편위) 쪽을 더 자주 묻는다.

## (심화) 왜 두 유도로 충분한가
전두면은 평면이라 벡터 하나는 직교하는 두 성분으로 정해진다. 유도 I 은 좌우 성분을, aVF 는 위아래 성분을 잰다. 부호 두 개로 사분면이, 크기의 비로 각도가 나온다 — 예를 들어 I 의 순면적이 작은 음성이고 aVF 가 크게 양성이면 벡터는 +90° 를 조금 넘은 곳(+100°~+120°)에 있다. 이 문항처럼 유도 III(+120°)이 가장 크게 양성이라면 벡터는 +120° 가까이 있다. 해리슨의 육축 도해가 이 계산의 지도다 [[harrison-21: 240장 p.1825]].
