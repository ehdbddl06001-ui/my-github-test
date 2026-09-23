---
id: cn.em.beta-blocker-overdose.glucagon-mechanism
type: concept
topic: Emergency Medicine
see_also: [Pharmacology, Cardiology]
date: 2026-09-23
updated: 2026-09-23
version: 1
outline: h459            # 기본틀 슬롯(content/outline/subjects.yaml)
confidence: medium
review_status: unreviewed
title: "베타차단제 중독 — 글루카곤이 막힌 수용체를 우회하는 기전"
objective: "심근의 베타1 수용체 → Gs → adenylate cyclase → cAMP → PKA → L형 칼슘통로 인산화로 이어지는 정상 신호를 설명하고, 베타차단제 중독의 서맥·저혈압이 이 사슬의 입구가 막힌 결과임을 이해한 뒤, 글루카곤이 자신의 Gs 결합 수용체로 같은 사슬에 들어가 cAMP 를 올린다는 기전을 PDE 억제·직접 칼슘통로 개방·수용체 경쟁 같은 다른 기전과 구별한다"
objective_kind: 기전
condition: 베타차단제 중독(과량 복용)
exams: [usmle, kmle]
summary:
  - "심근에서 노르에피네프린·에피네프린이 베타1 수용체에 붙으면 Gs 단백이 adenylate cyclase 를 켜 cAMP 가 늘고, PKA 가 L형 칼슘통로 등을 인산화해 칼슘 유입이 늘어난다 → 심박수(변시)와 수축력(변력)이 오른다 [[?goodman-gilman]]."
  - "베타차단제 중독은 이 사슬의 입구(베타 수용체)를 막아 서맥·방실차단·저혈압을 만든다. 해리슨 표 459-4 는 저혈당·고칼륨·경련도 적고, 프로프라놀롤처럼 막 작용(membrane-active)이 있는 약은 따로 위험하다고 적는다 [[harrison-21: 459장 p.3591]]."
  - "글루카곤은 베타 수용체가 아닌 **자신의 글루카곤 수용체**(역시 Gs 결합)에 붙어 같은 adenylate cyclase → cAMP 사슬을 켠다. 입구가 달라서 베타 수용체가 막혀 있어도 작동한다 [[?goodman-gilman]]."
  - "해리슨의 치료 순서: 저혈압·증상성 서맥에 글루카곤. 아트로핀·이소프로테레놀·도파민·도부타민·에피네프린·노르에피네프린은 때때로 효과가 있고, 반응이 없으면 고용량 인슐린(포도당·칼륨으로 정상 혈당·칼륨 유지)·조율·기계적 순환 보조 [[harrison-21: 459장 p.3591]]."
  - "cAMP 를 올리는 다른 길 — PDE 억제(밀리논: 분해를 막음), 칼슘 투여(세포 밖 칼슘을 늘림) — 도 있지만 글루카곤의 기전은 아니다."
tables:
  - id: camp-routes
    title: "심근 cAMP·칼슘을 올리는 길 — 무엇이 어디에 작용하나"
    role: comparison
    span: column
    section: "(심화) cAMP 를 올리는 여러 길"
    columns: ["약", "작용점", "베타 수용체가 막혀도?", "기전"]
    rows:
      - ["베타 작용제(이소프로테레놀 등)", "베타 수용체", "경쟁 — 고용량 필요", "막힌 입구를 경쟁으로 연다"]
      - ["글루카곤", "글루카곤 수용체(Gs)", "작동한다", "다른 입구로 같은 adenylate cyclase"]
      - ["밀리논", "PDE3", "작동한다", "cAMP 분해를 막는다(새로 만들지 않음)"]
      - ["칼슘염", "세포 밖 칼슘", "작동한다", "L형 통로를 지나는 칼슘의 양을 늘린다"]
    note: "해리슨 표 459-4 는 약 이름과 사용 상황만 적고 수용체 수준의 기전은 적지 않는다 [[harrison-21: 459장 p.3591]]. 기전 서술은 약리학 교과서 [[?goodman-gilman]]."
sources:
  - id: harrison-21
    org: "McGraw Hill"
    title: "Harrison's Principles of Internal Medicine, 21st ed. — Chapter 459: Poisoning and Drug Overdose"
    kind: textbook
    year: 2022
    citation: "Loscalzo J, Kasper DL, Longo DL, et al (eds). Harrison's Principles of Internal Medicine, 21e. 459장 p.3587, 3591 (Table 459-4)"
    checked_at: 2026-09-23
    checked: "본문 대조(드라이브 459장 문서) — p.3587 저혈압을 동반한 서맥성 부정맥에서 글루카곤·칼슘·고용량 인슐린+포도당이 베타차단제·칼슘통로차단제 중독에 효과적일 수 있음 · p.3591 표 459-4 β차단제 행(분류: 심장선택·비선택·부분작용제·α1 길항·막 작용 약; 소견: 생리적 억제·방실차단·저혈당·고칼륨·경련, 소탈롤 QT 연장; 치료: 저혈압·증상성 서맥에 글루카곤, 아트로핀·이소프로테레놀·도파민·도부타민·에피네프린·노르에피네프린은 때때로 효과, 난치성은 고용량 인슐린·조율·기계 보조) · 칼슘통로차단제 행(저혈압은 주로 혈관저항 감소, 고혈당, 칼슘·글루카곤). 글루카곤의 수용체·cAMP 기전은 이 장에 없다"
    verified: text
  - id: goodman-gilman
    org: "McGraw Hill"
    title: "Goodman & Gilman's The Pharmacological Basis of Therapeutics — adrenergic receptor signaling · beta-blocker toxicity"
    kind: textbook
    year: 2023
    citation: "Brunton LL, Knollmann BC (eds). Goodman & Gilman's The Pharmacological Basis of Therapeutics, 14e. (장·쪽 미대조)"
    checked_at: 2026-09-23
    checked: "서지만 — 문항 출처로 적힌 교과서. 이 세션에서 원문 미대조(글루카곤 수용체-Gs-cAMP 기전 서술의 근거)"
    verified: citation
diagram:
  title: "베타차단제 중독 — 서맥·저혈압 치료 순서"
  nodes:
    - {id: start, kind: start, text: "베타차단제 과량 복용 · 서맥 · 저혈압"}
    - {id: qrs, kind: decision, text: "QRS 가 넓어졌거나 경련이 있는가? (막 작용 약 — 프로프라놀롤 등)"}
    - {id: qrsdo, kind: info, text: "12유도 심전도 · 혈당 · 칼륨 · 복용 약 이름과 서방형 여부 확인"}
    - {id: na, kind: step, text: "나트륨통로 차단 소견을 함께 치료(해리슨 표의 항정신병약·삼환계 행처럼 QRS 연장에 탄산수소나트륨)"}
    - {id: resp, kind: decision, text: "수액·아트로핀 뒤에도 저혈압·증상성 서맥이 남는가?"}
    - {id: obs, kind: end, text: "관찰 — 서방형·소탈롤은 늦게 나빠질 수 있다"}
    - {id: glu, kind: step, text: "글루카곤 정주 — 자신의 Gs 수용체로 cAMP 를 올린다"}
    - {id: refr, kind: decision, text: "글루카곤에도 반응이 없는가?"}
    - {id: hdi, kind: end, text: "고용량 인슐린(포도당·칼륨 보충) · 카테콜아민 · 조율 · 기계적 순환 보조"}
    - {id: keep, kind: end, text: "글루카곤 지속 · 혈당·칼륨 감시"}
  edges:
    - {from: start, to: qrs}
    - {from: qrs, to: na, label: "예"}
    - {from: qrs, to: resp, label: "아니오"}
    - {from: qrs, to: qrsdo, label: "모름"}
    - {from: qrsdo, to: na, label: "QRS 연장"}
    - {from: qrsdo, to: resp, label: "QRS 정상"}
    - {from: na, to: resp}
    - {from: resp, to: glu, label: "예"}
    - {from: resp, to: obs, label: "아니오"}
    - {from: glu, to: refr}
    - {from: refr, to: hdi, label: "예"}
    - {from: refr, to: keep, label: "아니오"}
diagram_notes:
  - "베타차단제 중독의 저혈당·고칼륨은 표 459-4 에 적힌 소견이다 — 고용량 인슐린을 쓸 때 포도당·칼륨을 함께 보는 이유이기도 하다 [[harrison-21: 459장 p.3591]]."
  - "칼슘통로차단제 중독은 고혈당, 혈관저항 감소에 의한 저혈압이 특징이고 칼슘·글루카곤·고용량 인슐린·지질 유제를 쓴다 — 베타차단제 중독과 해독 도구가 겹친다 [[harrison-21: 459장 p.3591]]."
  - "QRS 연장에 탄산수소나트륨을 쓰는 가지는 해리슨이 나트륨통로 차단 약(항정신병약 등)에 적은 원칙을 옮긴 것이다 — 베타차단제 행 자체에는 적혀 있지 않다(검토 항목)."
pitfalls:
  - contrast: "글루카곤 = 「칼슘통로를 직접 연다」 vs 2차전달자를 거친다"
    point: "글루카곤 효과의 마지막 단계는 실제로 L형 칼슘통로를 통한 칼슘 유입 증가다. 그러나 그 사이에 글루카곤 수용체 → Gs → adenylate cyclase → cAMP → PKA 인산화가 있다. 기전 문항에서 「2차전달자 없이」「직접」 같은 말은 사슬의 중간을 지운 서술이다. 베타 수용체가 막혀도 글루카곤이 듣는 이유는 「다른 입구, 같은 사슬」이다."
    exception: "칼슘염 투여는 통로를 지나는 칼슘의 양을 늘려 수축력을 올린다 — 이것은 글루카곤이 아니라 칼슘의 기전이다."
    cites: ["?goodman-gilman"]
    covers: ["usmle-2026-0038:B"]
  - contrast: "글루카곤 vs 밀리논(PDE 억제)"
    point: "둘 다 베타 수용체를 거치지 않고 cAMP 를 올리지만, 글루카곤은 cAMP 를 새로 만들게 하고(adenylate cyclase 활성) 밀리논은 이미 있는 cAMP 의 분해를 막는다."
    cites: ["?goodman-gilman"]
  - contrast: "글루카곤 = 혈당 호르몬?"
    point: "글루카곤은 간에서 글리코겐 분해로 혈당을 올리지만, 심박·혈압 회복은 심근 수용체-cAMP 작용이다. 혈당 상승은 부수 효과이고(구역·구토도 흔하다) 심장 효과의 원인이 아니다."
    cites: ["?goodman-gilman"]
checks:
  - q: "베타 수용체가 약으로 막혀 있는데 글루카곤이 심박·수축력을 올릴 수 있는 이유는?"
    a: "글루카곤은 베타 수용체가 아닌 자신의 Gs 결합 수용체에 붙어 같은 adenylate cyclase → cAMP → PKA 사슬을 켠다 — 입구가 다르다."
  - q: "글루카곤과 밀리논이 cAMP 를 올리는 방식의 차이는?"
    a: "글루카곤은 adenylate cyclase 를 활성화해 cAMP 를 새로 만들게 하고, 밀리논은 PDE3 를 억제해 cAMP 분해를 막는다."
  - q: "해리슨 표 459-4 가 적은 베타차단제 중독의 대사 소견 두 가지는?"
    a: "저혈당과 고칼륨(칼슘통로차단제 중독은 반대로 고혈당)."
variants:
  - id: v1
    of: usmle-2026-0038
    flip: true
    changed: "rescue drug changed from IV glucagon to IV milrinone (same propranolol overdose, same bradycardia/hypotension) → answer shifts from 'own Gs-coupled receptor activates adenylate cyclase' to 'phosphodiesterase inhibition slows cAMP breakdown'"
    context: "Same patient and poisoning; only the rescue inotrope differs"
    stem: "A 51-year-old woman is brought to the emergency department 3 hours after taking a large number of propranolol tablets. Her pulse is 38/min and blood pressure is 70/40 mm Hg despite intravenous fluids and atropine. Glucagon is unavailable, so the intensivist starts an intravenous infusion of milrinone, and her cardiac output improves. Which of the following best explains how this drug increases myocardial contractility while beta-adrenergic receptors remain blocked?"
    choices:
      - "A. It binds a Gs-coupled receptor distinct from the beta receptor and activates adenylate cyclase"
      - "B. It inhibits phosphodiesterase 3, reducing breakdown of intracellular cAMP"
      - "C. It directly opens L-type calcium channels without any change in second messengers"
      - "D. It displaces propranolol from the beta-1 receptor by competitive agonism"
      - "E. It inhibits the Na+/K+-ATPase, increasing intracellular sodium and calcium"
    answer: "B"
    explanation: "Milrinone inhibits phosphodiesterase 3, so cAMP that is still being produced is broken down more slowly; cAMP-PKA signaling rises without using the blocked beta receptor. The single changed clue — the rescue drug is milrinone, not glucagon — turns the original distractor (PDE inhibition) into the answer. Choice A is glucagon's mechanism, E is digoxin's, and D describes a high-dose beta agonist such as isoproterenol rather than milrinone."
    kind: application
  - id: v2
    of: usmle-2026-0038
    flip: false
    changed: "age, sex, the specific beta blocker (metoprolol), the setting (found at home by family) and answer order changed; glucagon still reverses bradycardia and hypotension → answer unchanged (own Gs-coupled receptor → adenylate cyclase → cAMP)"
    context: "Different patient and beta blocker; same antidote and same question"
    stem: "A 67-year-old man is found confused at home by his daughter next to an empty bottle of his metoprolol tablets. In the emergency department his pulse is 34/min with a junctional rhythm and his blood pressure is 76/44 mm Hg. Fluids and atropine produce no response. An intravenous bolus of glucagon is given, and within minutes his heart rate rises to 58/min and blood pressure to 98/60 mm Hg. Which of the following is the primary mechanism of this improvement?"
    choices:
      - "A. Glucagon raises blood glucose, and hyperglycemia increases sinoatrial node automaticity"
      - "B. Glucagon competes with metoprolol at the beta-1 receptor and displaces it"
      - "C. Glucagon activates its own Gs protein-coupled receptor on cardiac myocytes, stimulating adenylate cyclase and raising cAMP"
      - "D. Glucagon blocks phosphodiesterase, preventing degradation of existing cAMP"
      - "E. Glucagon opens myocardial calcium channels directly, bypassing intracellular signaling"
    answer: "C"
    explanation: "Glucagon binds its own Gs-coupled receptor, activates adenylate cyclase and increases cAMP, so PKA-mediated calcium entry, chronotropy and inotropy recover even though beta-1 receptors remain occupied by metoprolol. Changing the patient, the drug (cardioselective metoprolol instead of propranolol) and the setting does not change the key clue — glucagon reversing beta-blocker-induced bradycardia — so the answer is the same. Calcium-channel opening happens downstream through PKA, not directly."
    kind: application
---

## 정의
베타차단제 중독은 베타 수용체 차단이 과도해 서맥·방실차단·저혈압·심인성 쇼크가 생기는 상태다. 약에 따라 심장선택(아테놀롤·메토프롤롤)·비선택(프로프라놀롤·나돌롤)·부분작용(핀돌롤)·알파 차단 겸비(카르베딜롤·라베탈롤)·막 작용(프로프라놀롤·소탈롤·아세부톨롤) 성질이 달라 중독 양상도 다르다 [[harrison-21: 459장 p.3591]].

## 병태생리
정상 심근: 카테콜아민 → 베타1 수용체 → Gs → adenylate cyclase → cAMP → PKA → L형 칼슘통로·포스포람반 인산화 → 칼슘 유입과 근소포체 칼슘 재흡수 증가 → 수축력과 심박수 증가 [[?goodman-gilman]]. 베타차단제는 이 사슬의 입구를 막는다. 사슬의 뒤쪽(adenylate cyclase 이후)은 멀쩡하므로, 다른 입구로 들어가거나(글루카곤) 뒤쪽을 직접 거드는(PDE 억제, 칼슘) 방법이 해독의 원리가 된다.

## 기전에서 소견으로
- 동결절·방실결절의 cAMP 감소 → 서맥·방실차단(아트로핀은 미주신경만 풀어 반응이 약하다).
- 심근 cAMP 감소 → 수축력 저하 → 저혈압·심인성 쇼크.
- 간 글리코겐 분해·포도당신생의 베타 매개 부분이 막힘 → 저혈당. 세포 안으로의 칼륨 이동 감소 → 고칼륨 [[harrison-21: 459장 p.3591]].
- 막 작용 약(프로프라놀롤) → 나트륨통로 차단으로 QRS 연장·경련. 소탈롤 → QT 연장·심실빈맥. 서방형·소탈롤은 늦게 나타날 수 있다.

## 감별
칼슘통로차단제 중독도 서맥·저혈압이지만 **고혈당**이 흔하고 저혈압이 주로 혈관저항 감소 때문이다. 디곡신 중독(고칼륨·다양한 부정맥), 클로니딘·아편류(축동·의식 저하)도 서맥·저혈압을 만든다 [[harrison-21: 459장 p.3591]].

## 검사
12유도 심전도(PR·QRS·QT), 혈당·칼륨, 복용 약의 이름·제형(서방형 여부)·양. 베타차단제의 혈중 농도는 치료에 쓰지 않는다.

## 치료
1. 기도·호흡·순환 확보, 수액, 아트로핀.
2. 저혈압·증상성 서맥에 **글루카곤** [[harrison-21: 459장 p.3591]].
3. 아트로핀·이소프로테레놀·도파민·도부타민·에피네프린·노르에피네프린은 때때로 효과가 있다.
4. 난치성: 고용량 인슐린(포도당·칼륨으로 정상 혈당·칼륨 유지), 전기 조율, 기계적 순환 보조 [[harrison-21: 459장 p.3587, p.3591]].
5. 반응 확인: 심박·혈압·소변량·의식, 혈당·칼륨 반복 측정.

## 권고와 예외
- 글루카곤은 구역·구토가 흔하다 — 의식이 떨어진 환자에서는 기도 보호를 먼저 생각한다(용량·지속 주입 속도는 이 정리본에서 대조하지 않았다).
- 해리슨은 글루카곤을 먼저 적지만, 약제 간 우선순위는 근거 수준이 낮은 영역이다 — 이 정리본의 목표는 「왜 듣는가」의 기전이다.

## 시험 쟁점 — 충돌·맥락·새 근거
- 해당 없음(대조: 해리슨 459장 p.3587, 3591 — 문항의 해설과 어긋난 곳 없음. 수용체 수준의 기전은 해리슨이 다루지 않아 대조 범위 밖)

## (심화) cAMP 를 올리는 여러 길
표 「심근 cAMP·칼슘을 올리는 길」. 수용체가 막혔을 때의 해독 원리는 세 가지다 — 막힌 입구를 경쟁으로 연다(고용량 작용제), 다른 입구로 같은 사슬에 들어간다(글루카곤), 사슬의 뒤쪽을 거든다(PDE 억제·칼슘). USMLE 기전 문항은 이 셋을 서로의 오답으로 둔다.
