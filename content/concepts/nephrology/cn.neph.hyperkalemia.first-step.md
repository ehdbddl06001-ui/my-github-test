---
id: cn.neph.hyperkalemia.first-step
type: concept
topic: Nephrology
see_also: [Cardiology, Emergency Medicine]
date: 2026-09-18
updated: 2026-09-18
version: 1
confidence: medium
review_status: unreviewed
title: "고칼륨혈증 — 가장 먼저 할 처치를 심전도로 고른다"
objective: "고칼륨혈증 환자에서 심전도 변화 유무로 첫 처치(심근막 안정화 → 세포 내 이동 → 제거)의 순서를 고른다"
objective_kind: 다음 처치
condition: 고칼륨혈증
exams: [kmle, usmle]
summary:
  - "진단(칼륨 상승)은 쉽다. 갈리는 곳은 「무엇을 먼저」다."
  - "심전도 변화(뾰족한 T파·PR 연장·P파 소실·QRS 확장·서맥)가 있으면 첫 처치는 정맥 칼슘 — 칼륨을 낮추지 않고 심근막을 안정화해 시간을 번다."
  - "그다음 칼륨을 세포 안으로(정맥 인슐린+포도당, 보조로 살부타몰), 그다음 몸 밖으로(결합제·이뇨제·투석)."
  - "심전도 변화가 없으면 칼슘은 첫 처치가 아니다 — 수치와 원인에 따라 이동·제거부터."
  - "투석 환자의 최종 제거는 투석이지만, 준비되는 동안 심장을 먼저 보호한다."
criteria:
  - id: hk-calcium
    name: 정맥 칼슘의 적응
    kind: 치료 권고(순서)
    population: "고칼륨혈증 성인"
    statement: "고칼륨혈증에 의한 심전도 변화가 있으면 정맥 칼슘으로 심근막을 안정화한다. 칼슘은 혈청 칼륨을 낮추지 않는다"
    exceptions: "심전도 변화가 없으면 일상적 적응이 아니다. 디곡신 복용 환자의 칼슘 투여는 논란이 있어 이 정리본에서 다루지 않는다(검토 항목)"
    source: kdigo-2020
    basis: current
    exams: [kmle, usmle]
  - id: hk-shift
    name: 세포 내 이동
    kind: 치료 권고
    population: "중증 또는 심전도 변화가 있는 고칼륨혈증"
    statement: "정맥 인슐린과 포도당(저혈당 감시), 보조로 흡입 베타2 작용제"
    exceptions: "효과는 일시적 — 제거 치료와 함께"
    source: kdigo-2020
    basis: current
    exams: [kmle, usmle]
  - id: hk-remove
    name: 제거
    kind: 치료 권고
    population: "고칼륨혈증"
    statement: "칼륨 결합제, 소변이 나오면 루프 이뇨제, 말기 신부전·불응이면 투석"
    exceptions: "결합제는 작용이 느려 응급의 첫 처치가 아니다. 약제 종류(폴리스티렌설폰산·파티로머·지르코늄)는 국가별 사용 가능 여부가 다르다 — 국내 사용 여부 미대조"
    source: kdigo-2020
    basis: current
    exams: [kmle, usmle]
sources:
  - id: kdigo-2020
    org: "KDIGO (Kidney Disease: Improving Global Outcomes) Controversies Conference"
    title: "Potassium homeostasis and management of dyskalemia in kidney diseases"
    kind: consensus
    year: 2020
    citation: "Clase CM et al. Kidney Int 2020;97(1):42-61"
    doi: "10.1016/j.kint.2019.09.018"
    pmid: "31706619"
    url: "https://doi.org/10.1016/j.kint.2019.09.018"
    checked_at: 2026-09-18
    checked: "PubMed 로 서지·주제 확인. 응급 처치 순서의 세부 문구는 본문 대조 전(검토 항목)"
  - id: ukka-2020
    org: "UK Kidney Association"
    title: "Treatment of acute hyperkalaemia in adults"
    kind: guideline
    year: 2020
    citation: "UK Kidney Association, 2020 (2022 갱신, 현재 보관 문서)"
    url: "https://www.ukkidney.org/health-professionals/guidelines/treatment-acute-hyperkalaemia-adults"
    checked_at: 2026-09-18
    checked: "제목·발행 기관·연도만 확인. 권고 본문(PDF) 미대조"
    watch: {pattern: "(HYPERKALAEMIA GUIDELINE[^<>]{0,40}?\\.pdf)"}   # 쪽에 걸린 PDF 파일 이름(판·날짜)이 바뀌면 개정 신호
diagram:
  title: "고칼륨혈증 — 가장 먼저 할 처치"
  nodes:
    - {id: start, kind: start, text: "혈청 칼륨 상승이 확인된 환자"}
    - {id: monitor, kind: step, text: "심장 감시를 걸고 12유도 심전도·활력징후 확인"}
    - {id: ecg, kind: decision, text: "고칼륨혈증에 의한 심전도 변화가 있는가? 뾰족한 T · PR 연장 · P 소실 · QRS 확장 · 서맥"}
    - {id: noecg, kind: info, text: "심전도 판독 전 — 판독을 서두른다. 수치만으로 칼슘 여부를 정하지 않는다"}
    - {id: calcium, kind: step, text: "① 정맥 칼슘 — 심근막 안정화(칼륨은 그대로). 심전도 재확인"}
    - {id: shift, kind: step, text: "② 세포 안으로 이동 — 정맥 인슐린+포도당(혈당 감시), 보조로 살부타몰 흡입"}
    - {id: remove, kind: step, text: "③ 몸 밖으로 제거 — 결합제 · 소변이 나오면 이뇨제 · 말기 신부전·불응이면 투석"}
    - {id: cause, kind: end, text: "원인 교정(약물·식이·용혈 표본 여부) · 칼륨 반복 측정"}
  edges:
    - {from: start, to: monitor}
    - {from: monitor, to: ecg}
    - {from: ecg, to: calcium, label: "있음"}
    - {from: ecg, to: noecg, label: "아직 판독 전"}
    - {from: ecg, to: shift, label: "없음 · 중증 수치"}
    - {from: noecg, to: calcium, label: "변화 있으면"}
    - {from: noecg, to: shift, label: "없으면"}
    - {from: calcium, to: shift}
    - {from: shift, to: remove}
    - {from: remove, to: cause}
checks:
  - q: "심전도 변화가 있는 고칼륨혈증에서 칼슘을 먼저 주는 이유는? 칼슘이 칼륨 수치를 낮추는가?"
    a: "심근막의 흥분성을 곧바로 안정화해 치명적 부정맥을 막기 때문이다. 칼륨 수치는 낮추지 않는다 — 그래서 이동·제거가 뒤따라야 한다."
  - q: "안정화 → 이동 → 제거 순서에서 각 단계의 대표 약·처치는?"
    a: "안정화: 정맥 칼슘. 이동: 정맥 인슐린+포도당, 살부타몰. 제거: 결합제·이뇨제·투석."
  - q: "칼륨 6.8 인데 심전도가 정상이다. 칼슘이 첫 처치인가?"
    a: "아니다. 칼슘의 적응은 심전도 변화다. 중증 수치면 인슐린+포도당으로 이동부터, 원인 약물 중단·제거를 함께."
variants:
  - id: v1
    context: "같은 목표, 다른 맥락 — 심전도 변화가 없는 중증 고칼륨혈증"
    stem: "58세 여자가 정기 혈액검사에서 칼륨이 높다는 연락을 받고 왔다. 당뇨병성 콩팥병으로 안지오텐신 수용체 차단제와 스피로놀락톤을 먹고 있다. 증상은 없다. 혈압 134/80 mmHg, 맥박 78회/분. 혈청 칼륨 6.7 mEq/L(용혈 없음), 크레아티닌 2.1 mg/dL, 소변량은 정상이다. 12유도 심전도는 정상 동리듬이며 T파·PR·QRS 변화가 없다. 가장 먼저 할 처치는?"
    choices: ["A. 정맥 칼슘글루콘산", "B. 정맥 인슐린과 포도당", "C. 응급 혈액투석", "D. 1주 뒤 재검", "E. 생리식염수 대량 투여"]
    answer: "B"
    explanation: "칼륨은 중증 범위지만 심전도 변화가 없어 막 안정화(칼슘)의 적응이 아니다. 먼저 세포 안으로 옮기고(인슐린+포도당), 원인 약물(스피로놀락톤 등)을 멈추고 제거를 이어 간다. 투석은 신기능이 남아 소변이 나오는 지금의 첫 처치가 아니고, 1주 뒤 재검은 중증 수치를 방치한다."
    kind: application
---

## 정의
혈청 칼륨이 기준 상한을 넘는 상태다. 시험에서 중요한 축은 **수치**보다 **심장 독성의 증거(심전도 변화)** 다 — 같은 수치라도 심전도가 바뀌었으면 즉시 심장을 보호한다.

## 병태생리
세포 밖 칼륨이 오르면 안정막전위가 덜 음전하가 되어 처음에는 흥분성이 오르고, 더 오르면 나트륨 통로가 불활성화되어 전도가 느려진다. 그래서 뾰족한 T파(재분극 가속) → PR 연장·P파 소실 → QRS 확장 → 사인파·심실세동·무수축 순으로 진행한다.

## 기전에서 소견으로
- 근력 약화·두근거림·서맥은 막전위 이상의 결과다.
- 칼슘은 역치 전위를 올려 안정막전위와의 간격을 되돌린다 — 칼륨을 옮기거나 빼는 게 아니라 **막의 반응성**을 바꾼다. 그래서 효과가 빠르지만 칼륨 수치는 그대로다.
- 인슐린은 Na⁺/K⁺-ATPase 를 활성화해 칼륨을 세포 안으로 넣는다(포도당을 함께 줘 저혈당을 막는다). 베타2 작용제도 같은 펌프를 돕는다.

## 감별
- **가성 고칼륨혈증**: 용혈 표본·혈소판·백혈구 급증. 심전도가 정상이고 임상과 맞지 않으면 재측정. 다만 심전도 변화가 있으면 재측정을 기다리지 않는다.
- **원인 감별**: 신기능 저하, RAAS 억제제·칼륨 보존 이뇨제, 조직 파괴(횡문근융해·종양용해), 대사성 산증, 부신 기능 저하.

## 검사
- 12유도 심전도와 심장 감시가 첫 검사다 — 처치 순서를 이것이 정한다.
- 혈청 칼륨 재측정(용혈 확인), 크레아티닌, 혈당, 산염기, 약물 목록.

## 치료
1. **안정화** — 심전도 변화가 있으면 정맥 칼슘. 몇 분 안에 작용, 효과는 일시적이라 심전도를 다시 보고 필요하면 반복.
2. **이동** — 정맥 인슐린+포도당, 보조로 살부타몰 흡입.
3. **제거** — 칼륨 결합제(느리다), 소변이 나오면 루프 이뇨제, 말기 신부전·불응이면 투석.
4. **원인** — 원인 약물 중단, 식이 검토, 반복 측정.

## 권고와 예외
- 칼슘의 적응은 **심전도 변화**다. 수치만 높고 심전도가 정상이면 이동·제거부터.
- 투석 환자에서 최종 해결은 투석이지만, 준비 시간 동안 안정화가 먼저다.
- 생리식염수 대량 투여·이뇨제는 소변이 나오는 환자에서만 의미가 있고, 투석 환자에서는 용적 과부하를 부른다.
- 이 정리본의 권고는 KDIGO 2020 회의 결론을 서지 수준으로만 대조했다. 국내 지침·약제 사용 가능 여부는 대조하지 않았다(검토 항목).

## (심화) 「가장 먼저」 문항에서 인슐린이 매력적인 이유
인슐린+포도당은 **수치를 실제로 낮추는** 첫 약이라 「치료」처럼 느껴진다. 하지만 심전도가 바뀐 환자에서 급한 것은 수치가 아니라 **다음 몇 분의 부정맥**이다. 문항이 「가장 먼저」를 물으면 시간 축(분 단위 위험 → 시간 단위 교정)으로 보기를 줄 세운다.
