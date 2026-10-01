---
id: cn.em.ventricular-fibrillation.immediate-defibrillation
type: concept
topic: Emergency Medicine
see_also: [Cardiology]
date: 2026-09-23
updated: 2026-10-02
version: 3
outline: h306            # 기본틀 슬롯(content/outline/subjects.yaml)
confidence: medium
review_status: unreviewed
note_form: 2            # 판형 2(2026-09-25) — 결론·시험 단서·왜 → 혼동 → 표·도식 → 목표에 맞춘 본문
title: "심실세동 — 무맥 세동파에는 즉시 비동기 제세동"
objective: "심실세동에서 조직된 수축이 사라져 심박출이 멎는 기전을 설명하고, 무반응·무맥·무호흡 환자에서 제세동 가능 리듬(심실세동·무맥 심실빈맥)을 알아본 뒤 가슴압박과 함께 즉시 비동기 제세동을 첫 처치로 고르며, 동기화 율동전환·약물·서맥 처치와의 적응 차이를 판단한다"
objective_kind: 다음 처치
condition: 심실세동(심정지)
exams: [kmle, usmle]
summary:
  - "결론: 무반응·무맥에 QRS 없는 세동파면 가슴압박과 함께 즉시 비동기 제세동(이상성 200 J)."
  - "시험 단서: 쓰러짐·무맥·헐떡임 + 제각각인 세동파 = 심실세동(ventricular fibrillation), 제세동 가능 리듬."
  - "왜: 세동파엔 인식할 R파가 없어 동기화가 안 되고, 제세동이 빠를수록 결과가 좋다 [[harrison-21: 306장 p.2262–2263]]."
  - "에피네프린 1 mg(3–5분마다)·아미오다론 300 mg(충격 뒤 반복 시)은 충격 사이의 보조, 아트로핀·조율은 서맥 처치."
  - "무맥성 전기활동·무수축은 제세동 불가 리듬 — 압박·에피네프린·가역 원인 교정 [[harrison-21: 306장 p.2263]]."
pitfalls:
  - contrast: "동기화 율동전환 vs 비동기 제세동"
    point: "둘 다 전기충격이지만 동기화는 기계가 R파를 인식해 그 위에 쏜다(재분극 취약기에 쏘아 세동을 만들지 않으려고). 세동파에는 인식할 R파가 없어 동기화 모드로는 충격이 나가지 않거나 늦어진다. 무맥 리듬 — 심실세동·다형 심실빈맥 — 은 비동기다."
    exception: "맥박이 있는 불안정 단형 심실빈맥·상심실성 빈맥은 동기화 율동전환이 맞다. 무맥이면 단형 심실빈맥도 제세동한다."
    cites: ["harrison-21"]
    covers: ["kmle-2026-0554:C"]
  - contrast: "항부정맥제를 먼저 vs 충격을 먼저"
    point: "아미오다론은 한 번 이상 충격을 줬는데도 세동·빈맥이 반복될 때 다음 충격 뒤 재발을 줄이려는 보조다. 약이 도는 동안 제세동을 미루면 성공 가능성이 시간에 따라 떨어진다."
    cites: ["harrison-21"]
    covers: ["kmle-2026-0554:B"]
  - contrast: "서맥 처치(아트로핀·조율)를 심정지에"
    point: "아트로핀·경피/경정맥 조율은 맥박이 느린 리듬(증상성 서맥·방실차단)에서 박동수를 올리는 처치다. 세동은 박동이 느린 것이 아니라 조직된 박동이 없는 것이라 올릴 박동이 없다."
    cites: ["harrison-21"]
    covers: ["kmle-2026-0554:D", "kmle-2026-0554:E"]
  - contrast: "무수축(평탄선)에 충격"
    point: "무수축·무맥성 전기활동은 제세동 불가 리듬이다. 가슴압박·에피네프린과 가역 원인 탐색(저산소·저혈량·산증·고칼륨·저체온·독물·압전·긴장성 기흉·폐색전·심근경색)이 치료다."
    cites: ["harrison-21"]
criteria:
  - id: vf-shock-harrison
    name: 제세동 가능 리듬의 처치(해리슨)
    kind: 치료 기준
    population: "심실세동·무맥 심실빈맥 심정지"
    statement: "진단 즉시 이상성 200 J 충격 → 곧바로 가슴압박 2분 → 리듬 확인, 남아 있으면 최대 에너지로 반복. 에피네프린 1 mg IV/IO 3–5분마다, 충격 뒤 반복되면 아미오다론 300 mg(재발 시 150 mg), 실패 시 리도카인"
    exceptions: "단형 심실빈맥은 동기화, 다형 심실빈맥·심실세동은 비동기 충격"
    source: harrison-21
    locator: "306장 p.2262–2263, 그림 306-3"
    basis: current
    exams: [kmle, usmle]
sources:
  - id: harrison-21
    org: "McGraw Hill"
    title: "Harrison's Principles of Internal Medicine, 21st ed. — Chapter 306: Cardiovascular Collapse, Cardiac Arrest, and Sudden Cardiac Death"
    kind: textbook
    year: 2022
    citation: "Loscalzo J, Kasper DL, Longo DL, et al (eds). Harrison's Principles of Internal Medicine, 21e. 306장 p.2257–2266"
    checked_at: 2026-09-23
    checked: "본문 대조(드라이브 문서, 306장 p.2260–2263) — 생존 사슬(인지·가슴압박 중심 CPR·가능한 한 빠른 제세동·전문소생술), 제세동 속도가 결과의 중요한 예측 인자, VF/VT 진단 즉시 이상성 200 J 충격 뒤 곧바로 압박 2분·리듬 확인, 에피네프린 1 mg 3–5분마다, 단형 VT 는 QRS 동기화·다형 VT 와 VF 는 비동기 충격, 반복 시 아미오다론 300 mg 뒤 150 mg·실패 시 리도카인, 재발 원인(허혈·QT 연장→마그네슘·고칼륨→칼슘), PEA/무수축은 CPR·에피네프린·가역 원인, 서맥 리듬에 아트로핀 1 mg·조율(그림 306-3)을 확인했다"
    verified: text
  - id: aha-acls-2020
    org: "American Heart Association"
    title: "Part 3: Adult Basic and Advanced Life Support: 2020 American Heart Association Guidelines for Cardiopulmonary Resuscitation and Emergency Cardiovascular Care"
    kind: guideline
    year: 2020
    citation: "Panchal AR, Bartos JA, Cabañas JG, et al. Circulation 2020;142(16 Suppl 2):S366–S468"
    doi: "10.1161/CIR.0000000000000916"
    pmid: "33081529"   # 2026-09-25 PubMed esearch 로 DOI 확인·제목 일치
    checked_at: 2026-09-23
    checked: "서지만 — 루틴 컨테이너에서 ahajournals·PubMed 접근이 막혀 본문을 대조하지 못했다(문항 해설의 출처)"
    verified: citation
tables:
  - id: rhythms
    section: "가르는 소견 — 리듬이 처치를 정한다"
    title: "심정지·불안정 리듬별 첫 전기·약물 처치"
    role: treatment
    span: full
    columns: ["리듬", "맥박", "첫 처치", "왜 그런가", "근거"]
    rows:
      - ["심실세동", "없음", "비동기 제세동 + 가슴압박", "조직된 QRS 가 없어 동기화 불가, 시간이 곧 생존", "[[harrison-21: 306장 p.2262–2263]]"]
      - ["다형 심실빈맥(무맥)", "없음", "비동기 제세동", "QRS 모양이 계속 바뀌어 동기화가 믿을 수 없다", "[[harrison-21: 306장 p.2263]]"]
      - ["단형 심실빈맥", "있음·불안정", "동기화 율동전환", "R파에 맞춰 쏘아 취약기 충격을 피한다", "[[harrison-21: 306장 p.2263]]"]
      - ["무맥성 전기활동·무수축", "없음", "가슴압박 + 에피네프린, 가역 원인 치료", "제세동할 세동이 없다", "[[harrison-21: 306장 p.2263]]"]
      - ["증상성 서맥", "있음", "아트로핀 1 mg, 경피·경정맥 조율", "박동이 느린 것이 문제 — 박동수를 올린다", "[[harrison-21: 306장 p.2262]]"]
    note: "에너지는 이상성 200 J(첫 충격), 이후 최대 에너지 — 제세동기 종류에 따라 다르다 [[harrison-21: 306장 p.2262]]."
diagram:
  title: "쓰러진 환자 — 리듬 확인에서 첫 전기충격까지"
  nodes:
    - {id: start, kind: start, text: "무반응·무맥·정상 호흡 없음 → 가슴압박 시작"}
    - {id: pads, kind: step, text: "제세동기 부착 — 압박을 잠깐 멈추고 리듬 확인"}
    - {id: rhythm, kind: decision, text: "제세동 가능 리듬(심실세동·무맥 심실빈맥)인가?"}
    - {id: shock, kind: step, text: "즉시 비동기 충격(이상성 200 J) → 곧바로 가슴압박 2분"}
    - {id: persist, kind: decision, text: "2분 뒤 리듬 확인 — 세동·빈맥이 남아 있는가?"}
    - {id: acls, kind: step, text: "충격 반복 + 에피네프린, 반복되면 아미오다론"}
    - {id: cause, kind: info, text: "재발 원인 탐색 — 허혈·QT 연장·고칼륨"}
    - {id: rosc, kind: end, text: "자발순환 회복 — 소생 후 치료, 원인 평가"}
    - {id: nonshock, kind: end, text: "무맥성 전기활동·무수축 — 압박·에피네프린·가역 원인(충격 없음)"}
  edges:
    - {from: start, to: pads}
    - {from: pads, to: rhythm}
    - {from: rhythm, to: shock, label: "예"}
    - {from: rhythm, to: nonshock, label: "아니오"}
    - {from: shock, to: persist}
    - {from: persist, to: acls, label: "남아 있음"}
    - {from: persist, to: rosc, label: "순환 회복"}
    - {from: acls, to: cause}
    - {from: cause, to: rosc}
diagram_notes:
  - "도움 요청을 먼저 하고 압박을 시작한다(생존 사슬의 앞 두 고리) [[harrison-21: 306장 p.2260]]."
  - "용량: 에피네프린 1 mg IV/IO 3–5분마다, 아미오다론 300 mg(재발 시 150 mg), 실패하면 리도카인 [[harrison-21: 306장 p.2263]]."
  - "재발 원인별 처치: 허혈 → 응급 관동맥조영, QT 연장(토르사드) → 마그네슘, 고칼륨 → 칼슘 [[harrison-21: 306장 p.2263]]."
  - "맥박이 있는 빈맥은 이 도식 밖이다 — 불안정한 단형 빈맥은 동기화 율동전환, 안정하면 약물·전문가 상담."
  - "충전하는 동안에도 압박을 계속하고, 충격 직후 리듬·맥박을 보지 말고 곧바로 압박을 재개한다 [[harrison-21: 306장 p.2262]]."
  - "약물 용량·간격은 해리슨 서술이다. 2020 AHA 지침 본문은 미대조(†)."
checks:
  - q: "심실세동에서 동기화 모드로는 충격을 줄 수 없는 이유는?"
    a: "동기화는 제세동기가 R파를 인식해 그 순간에 쏘는 방식인데, 세동파에는 인식할 QRS 가 없다. 그래서 충격이 지연되거나 나가지 않는다 — 비동기로 즉시 쏜다."
  - q: "아미오다론은 심실세동 소생에서 언제 들어가는가?"
    a: "한 번 이상 충격을 줬는데도 세동·무맥 빈맥이 반복될 때, 다음 충격 뒤 재발을 줄이려고 300 mg(재발 시 150 mg)을 준다. 첫 처치가 아니다."
  - q: "맥박이 있고 혈압이 떨어진 단형 심실빈맥의 전기 처치는? 그 환자가 맥박을 잃으면?"
    a: "맥박이 있으면 동기화 율동전환, 맥박을 잃으면 무맥 심실빈맥으로 보고 비동기 제세동을 한다."
variants:
  - id: v1
    of: kmle-2026-0554
    flip: true
    changed: "무맥·무호흡·QRS 없는 세동파 → 맥박이 있고 의식이 흐린 저혈압 환자의 규칙적인 넓은 QRS 빈맥(단형 심실빈맥) ⇒ 정답이 비동기 제세동에서 동기화 율동전환으로"
    context: "같은 전기충격, 맥박이 있는 조직된 리듬"
    stem: "58세 남자가 30분 전부터 가슴이 두근거리고 어지러워 응급실에 왔다. 2년 전 전벽 심근경색을 앓았다. 도착 시 묻는 말에 늦게 대답하고 식은땀을 흘린다. 혈압 74/46 mmHg, 맥박 184회/분(목동맥에서 약하게 촉지), 호흡 24회/분, 체온 36.6 ℃. 심전도에서 모양이 일정하고 규칙적인 넓은 QRS 빈맥이 계속된다. 칼륨은 4.2 mmol/L 이다. 가장 먼저 시행할 처치는?"
    choices: ["A. 즉시 비동기 전기충격을 시행한다", "B. 정맥 아미오다론을 투여하고 관찰한다", "C. 동기화 심장율동전환을 시행한다", "D. 정맥 아트로핀을 투여한다", "E. 경피 인공심장박동조율을 시작한다"]
    answer: "C"
    explanation: "맥박이 있고 저혈압·의식 저하가 동반된 불안정 단형 심실빈맥이다. QRS 가 일정해 제세동기가 R파를 인식할 수 있으므로 동기화 율동전환으로 취약기 충격을 피한다. 원 문항과 달리 맥박이 있고 조직된 QRS 가 있다는 단서가 답을 바꿨다 — 맥박을 잃거나 다형으로 바뀌면 비동기 제세동이다."
    kind: application
  - id: v2
    of: kmle-2026-0554
    flip: false
    changed: "나이·성별·쓰러진 장소(수영장)·발견 경위와 감시 방법(자동제세동기)을 바꾸고, 무반응·무맥·세동파는 남김 ⇒ 답은 그대로 즉시 비동기 제세동"
    context: "겉모습만 다른 심정지 — 병원 밖 수영장"
    stem: "34세 여자가 수영장 탈의실에서 쓰러졌다. 출동한 구급대원이 도착했을 때 불러도 반응이 없고 목동맥 맥박이 없으며 헐떡이는 숨만 가끔 있다. 가슴압박을 시작하고 제세동기 패드를 붙였다. 리듬 화면에는 크기와 모양이 제각각인 불규칙한 파형만 보이고 QRS 를 구분할 수 없다. 체온 36.2 ℃, 혈당 112 mg/dL. 다음으로 할 처치는?"
    choices: ["A. 정맥로를 잡고 에피네프린을 먼저 투여한다", "B. 동기화 모드로 전기충격을 시행한다", "C. 즉시 비동기 전기충격을 시행한다", "D. 정맥 아트로핀을 투여한다", "E. 경피 인공심장박동조율을 시작한다"]
    answer: "C"
    explanation: "환자·장소·발견 경위는 달라도 무반응·무맥·비정상 호흡에 QRS 없는 세동파는 심실세동, 곧 제세동 가능 리듬이다. 즉시 비동기 충격 뒤 곧바로 압박 2분을 한다. 헐떡이는 숨은 정상 호흡이 아니다. 동기화는 인식할 R파가 없어 불가능하고, 에피네프린은 충격 사이의 보조, 아트로핀·조율은 서맥 처치다."
    kind: application
figures:
- id: f1
  file: docs/assets/figures/pmc-pmc13303025_figure3-0-0-322-362.png
  kind: ecg
  at: 기전 — 질서 있는 수축에서 세동으로
  shows: 심실세동 — 사지유도에서 모양·간격이 일정하지 않은 무질서한 파형
  look_for:
  - QRS·T 를 구별할 수 없고 진폭·주기가 제각각
  - 등전위선 없이 이어지는 파형
  label: '「Ventricular fibrillation recorded on telemetry and implantable cardioverter-defibrillator (ICD) imaging. (A) Limb-lead electrocardiogram captured during an episode of ventricular fibrillation. (B) Post-procedural imaging showing the implanted ICD.」 — Case Report: Recurrent ventricular fibrillation induced by multivessel coronary artery spasm: a case supporting ICD for secondary prevention'
  label_basis: published_figure
  reference: 동료 심사 논문의 그림 설명(저자가 그 소견이라고 쓴 그림)
  paper: 'Case Report: Recurrent ventricular fibrillation induced by multivessel coronary artery spasm: a case supporting ICD for secondary prevention. Frontiers in Physiology'
  doi: 10.3389/fphys.2026.1808973
  credit: 'Case Report: Recurrent ventricular fibrillation induced by multivessel coronary artery spasm: a case supporting ICD for secondary prevention. Front Physiol. 2026 Jun 12;17:1808973. doi: 10.3389/fphys.2026.1808973 (CC BY) — Figure 3'
  license: CC BY
  url: https://pmc.ncbi.nlm.nih.gov/articles/PMC13303025/
  asset: PMC-PMC13303025_Figure3
  privacy_check: 심전도 — 환자 정보 문자 없음
  crop: 0,0,322,362
---

## 판단 — 왜 즉시 비동기 제세동이 먼저인가
- 심정지 처치는 **리듬**이 가른다. 심실세동·무맥 심실빈맥은 제세동 가능 리듬(shockable rhythm)이라 충격이 치료다 [[harrison-21: 306장 p.2262]].
- 제세동이 얼마나 빨리 되느냐가 결과의 중요한 예측 인자다 — 약물이 도는 동안 충격을 미루면 성공 가능성이 떨어진다 [[harrison-21: 306장 p.2262]].
- 세동파에는 인식할 R파가 없다. 동기화 율동전환(synchronized cardioversion)은 충격이 나가지 않거나 늦어지므로 **비동기**로 쏜다 [[harrison-21: 306장 p.2263]].
- 에피네프린·아미오다론은 충격 사이의 보조이고, 아트로핀·조율은 박동이 느린 리듬의 처치라 올릴 박동이 없는 세동에는 쓸 곳이 없다.

## 기전 — 질서 있는 수축에서 세동으로
정상에서는 동결절의 흥분이 전도계를 따라 심실 전체로 빠르게 퍼져 심근이 거의 동시에 수축하고, 탈분극한 심근은 불응기에 들어가 한 박동 = 한 번의 박출이 된다. 허혈·경색 흉터·심근병증·QT 연장·전해질 이상은 부위마다 불응기를 다르게 만들고, 여기에 조기 박동이 들어오면 여러 회귀 파면이 쪼개지며 떠돌아 심근이 제각각 떨기만 한다. 박출이 0 이 되어 몇 초 안에 의식을 잃는다.
- 전기충격은 심근 대부분을 한꺼번에 탈분극시켜 모든 파면을 불응기로 만들고, 먼저 회복하는 동결절이 리듬을 되찾을 기회를 얻는다. 시간이 지날수록 심근 에너지가 고갈되어 성공률이 떨어진다.
- 소견: 무반응·무맥·무호흡 또는 헐떡임(정상 호흡이 아니다), 심전도에는 크기·모양·간격이 제각각인 세동파만 있고 QRS 를 구분할 수 없다. 급성 관동맥 허혈이 가장 흔한 배경이다 [[harrison-21: 306장 p.2263]].

## 가르는 소견 — 리듬이 처치를 정한다
- 무맥 심실빈맥은 넓은 QRS 가 빠르게 이어지지만 맥박이 없다. 무수축은 평탄선, 무맥성 전기활동은 리듬은 있으나 맥박이 없다.
- **동기화 율동전환**: R파를 인식해 그 위에 쏜다 — T파(취약기) 충격으로 세동을 유발하지 않으려는 것. 조직된 QRS 가 있는 리듬(맥박 있는 단형 심실빈맥·상심실성 빈맥).
- **비동기 제세동(defibrillation)**: 시점을 가리지 않고 즉시 쏜다. 인식할 R파가 없는 심실세동, QRS 모양이 계속 바뀌는 다형 심실빈맥 [[harrison-21: 306장 p.2263]].
- 심정지 중의 검사는 리듬 확인이 전부다. 자동제세동기의 첫 리듬은 원인 추정에 쓰이므로 보관하고, 재발하는 세동은 허혈 평가·전해질·QT 를 본다 [[harrison-21: 306장 p.2262–2263]].

## 선택 — 소생 순서
1. 인지와 가슴압박 — 무반응·무맥·비정상 호흡이면 도움 요청, 압박 시작 [[harrison-21: 306장 p.2260]].
2. 심실세동·심실빈맥으로 진단되면 즉시 이상성 200 J 충격. 충전 중에도 압박을 계속한다 [[harrison-21: 306장 p.2262]].
3. 충격 직후 맥박을 찾지 말고 곧바로 압박 2분 → 리듬 확인. 남아 있으면 최대 에너지로 다시 충격.
4. 충격 사이에 에피네프린, 한 번 이상 충격 뒤에도 반복되면 아미오다론, 실패하면 리도카인(용량은 도식 아래 메모) [[harrison-21: 306장 p.2263]].
5. 원인 치료 — 허혈·토르사드·고칼륨 [[harrison-21: 306장 p.2263]].

## 권고와 예외
- 무맥 단형 심실빈맥도 제세동(비동기)한다 — 「단형이면 동기화」는 맥박이 있을 때의 규칙이다.
- 대사성 산증이 제세동과 충분한 환기 뒤에도 남으면 중탄산나트륨 1 mEq/kg 을 줄 수 있다 [[harrison-21: 306장 p.2263]].
- 일시적·가역 원인으로 설명되지 않고 기대여명이 합리적인 심실세동·심실빈맥 심정지 생존자는 2차 예방으로 ICD 를 넣는다. 급성 심근경색 첫 48시간 안의 세동은 대개 여기에 해당하지 않는다 [[harrison-21: 306장 p.2263]].

## 시험 쟁점 — 충돌·맥락·새 근거
- 해당 없음(대조: 해리슨 306장 p.2260~2263) — 즉시 비동기 제세동·동기화의 적응·아미오다론의 자리는 문항 해설과 맞는다. 문항이 인용한 2020 AHA 지침 본문은 미대조(†).

## (심화) 왜 동기화가 세동을 만들 수 있는가
T파의 정점 부근은 심근 일부는 회복했고 일부는 아직 불응기인 「취약기」다. 조직된 리듬에서 이 순간에 충격이 떨어지면 불균일한 회복 상태에 회귀가 생겨 심실세동이 유발될 수 있다(R-on-T). 그래서 맥박이 있는 리듬은 R파에 맞춰 쏜다. 심실세동에서는 이미 전체가 무질서하므로 이 위험을 따질 이유가 없고, 기다리는 시간만 생존을 깎는다.
