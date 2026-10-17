---
id: cn.path.uterine-smooth-muscle-tumor.leiomyosarcoma-criteria
type: concept
topic: Obstetrics & Gynecology
see_also: [Pathology]
date: 2026-10-18
updated: 2026-10-18
version: 2
outline: gyn.oncology            # 산부인과 손 슬롯 「부인암」(해리슨 대조 대상 아님 — 해리슨 89장은 임상 양상만 참고 대조)
confidence: medium
review_status: unreviewed
note_form: 2            # 판형 2(2026-09-25)
title: "자궁 평활근 종양 — 악성은 괴사·이형성·분열로"
objective: "자궁 방추형 세포 종양에서 종양세포 괴사·핵 이형성·유사분열 세 기준으로 평활근육종을 판정하고 세포성·적색변성 평활근종과 가른다"
objective_kind: 진단
condition: 자궁 평활근육종(uterine leiomyosarcoma)과 평활근종 변이형의 조직 감별
exams: [kmle, usmle]
summary:
  - "결론: 종양세포 괴사·중등도 이상 핵 이형성·유사분열 ≥ 10/10 HPF 중 둘 이상이면 평활근육종(leiomyosarcoma)이다."
  - "시험 단서: 빠르게 커진 자궁 근층 종괴 + 다발 배열 방추형 세포 + 「핵 이형성 뚜렷」「유사분열 18/10 HPF」."
  - "왜: 모양·크기·세포 밀도는 양성과 겹친다 — 악성을 가르는 것은 세포 밀도가 아니라 세 기준의 조합이다."
  - "세포 밀도만 높으면 세포성 평활근종, 이형성 없이 경색형 괴사면 적색변성(임신 중 흔함)이다."
pitfalls:
  - contrast: "세포성 평활근종 vs 평활근육종"
    point: "세포성 평활근종도 세포가 빽빽하지만 핵 이형성·종양세포 괴사가 없고 유사분열이 적다. 세포 밀도는 악성 기준이 아니다 — 이형성과 분열 수가 함께 있으면 세포가 많든 적든 평활근육종이다 [[?who-fgt-5]] [[?bell-1994]]."
    exception: "이형성·괴사가 없고 유사분열도 적은데 세포만 빽빽하면 세포성 평활근종이 맞다."
    covers: ["imaging-2026-0342:E"]
  - contrast: "적색변성 평활근종 — 임신 중이니 괴사는 변성?"
    point: "임신 중 평활근종은 출혈성 경색(적색변성)이 흔하다. 경색형 괴사는 살아 있는 종양과의 사이에 육아조직·유리질화 띠가 끼고 핵 이형성이 없다. 종양세포 괴사는 살아 있는 종양에서 괴사로 갑자기 넘어가고 괴사 안에 이형 핵의 윤곽이 남는다 [[?who-fgt-5]]."
    exception: "이형성이 없고 괴사가 경색형이며 분만 뒤 종괴가 줄면 적색변성이 맞다."
  - contrast: "임신 중 빠른 성장 = 악성?"
    point: "임신 중에는 평활근종도 빨리 자란다. 빠른 성장은 악성의 근거가 아니며, 진단은 조직의 세 기준으로 정한다."
tables:
  - id: usmt-differential
    section: "가르는 소견 — 괴사의 종류와 핵"
    title: "자궁 근층 종양 — 조직으로 가르기"
    role: differential
    span: column
    columns: ["진단", "세포·배열", "괴사", "이형성·분열"]
    rows:
      - ["평활근육종", "다발 배열 방추형", "종양세포 괴사(갑작스러운 경계)", "중등도 이상 · 흔히 ≥ 10/10 HPF [[?who-fgt-5]]"]
      - ["세포성 평활근종", "다발 배열, 세포만 빽빽", "없음", "없음 · 적음 [[?who-fgt-5]]"]
      - ["적색변성 평활근종", "다발 배열 방추형", "출혈성 경색(유리질화 띠)", "없음 · 임신 중 다소 늘 수 있음 [[?who-fgt-5]]"]
      - ["저등급 자궁내막 간질육종", "작은 둥근 세포, 소동맥 주위 소용돌이", "드묾", "경미 · 근층에 혀 모양 침윤 [[?who-fgt-5]]"]
      - ["태반부위 영양막종양", "중간형 영양막세포가 근섬유 사이로", "흔함", "β-hCG 낮게 양성 · hPL 양성 [[?who-fgt-5]]"]
diagram:
  title: "자궁 근층 방추형 세포 종양 — 양성·악성 가르기"
  nodes:
    - {id: start, kind: start, text: "자궁 근층 종괴 — 방추형 세포 종양"}
    - {id: pattern, kind: decision, text: "엇갈리는 다발인가, 둥근 세포인가?"}
    - {id: ess, kind: end, text: "소동맥 주위 둥근 세포 → 자궁내막 간질 종양"}
    - {id: ask, kind: info, text: "괴사 종류·핵 이형성·유사분열 수를 확인"}
    - {id: crit, kind: decision, text: "악성 기준 셋 중 몇 개인가?"}
    - {id: lms, kind: end, text: "둘 이상 → 평활근육종"}
    - {id: benign, kind: decision, text: "괴사가 있다면 어떤 괴사인가?"}
    - {id: red, kind: end, text: "경색형 괴사·이형성 없음 → 적색변성"}
    - {id: cell, kind: end, text: "괴사 없음·세포만 빽빽 → 세포성 평활근종"}
  edges:
    - {from: start, to: pattern}
    - {from: pattern, to: ask, label: "평활근 다발"}
    - {from: pattern, to: ess, label: "둥근 세포"}
    - {from: ask, to: crit}
    - {from: crit, to: lms, label: "둘 이상"}
    - {from: crit, to: benign, label: "하나 이하"}
    - {from: benign, to: red, label: "경색형"}
    - {from: benign, to: cell, label: "괴사 없음"}
diagram_notes:
  - "세 기준 — ① 종양세포(응고) 괴사 ② 미만성 중등도 이상 핵 이형성 ③ 유사분열 ≥ 10/10 HPF. 둘 이상이면 평활근육종이다 [[?who-fgt-5]] [[?bell-1994]]."
  - "기준이 하나만 있거나 경계 값이라 판정이 어려우면 악성 잠재성 불명 평활근 종양(STUMP)으로 보고한다 [[?who-fgt-5]]."
  - "점액성·상피양 평활근 종양은 기준 수치가 더 낮다 — 이 정리본은 방추형(통상형)만 다룬다(검토 항목)."
checks:
  - q: "자궁 평활근 종양에서 평활근육종을 정하는 세 기준과 판정 규칙은?"
    a: "종양세포 괴사, 미만성 중등도 이상 핵 이형성, 유사분열 ≥ 10/10 HPF — 이 중 둘 이상이면 평활근육종."
  - q: "종양세포 괴사와 경색형(유리질화) 괴사를 가르는 소견은?"
    a: "종양세포 괴사는 살아 있는 종양에서 갑자기 넘어가고 이형 핵 윤곽이 남는다. 경색형은 사이에 육아조직·유리질화 띠가 끼고 이형성이 없다."
  - q: "세포성 평활근종이 평활근육종과 다른 점은?"
    a: "세포 밀도만 높고 핵 이형성·종양세포 괴사가 없으며 유사분열이 적다 — 세포 밀도는 악성 기준이 아니다."
variants:
  - id: v1
    of: imaging-2026-0342
    flip: true
    changed: "핵 이형성 뚜렷·유사분열 18/10 HPF·분만 뒤 재성장 → 핵 이형성 없음·유사분열 3/10 HPF·괴사와 종양 사이 유리질화 띠·분만 뒤 크기 감소 → 답이 평활근육종에서 적색변성 평활근종으로 바뀜"
    context: "단서를 바꿔 답이 바뀌는 변형 — 임신 중 아픈 자궁 종괴"
    stem: "31세 임신부가 임신 20주에 시작된 하복부 통증과 미열로 왔다. 체온 37.8 °C 이다. 초음파에서 자궁 근층에 7 cm 종괴가 있고 내부에 낭성 변화가 있다. 진통제로 증상이 가라앉았고, 분만 뒤 6주에 잰 종괴는 5 cm 로 줄었다. 증상이 되풀이되어 종괴절제술을 하였다. 엇갈리는 다발로 배열한 방추형 세포 종양이며, 넓은 출혈·괴사 구역과 살아 있는 종양 사이에 육아조직과 유리질화 띠가 끼어 있다. 핵 이형성은 없고 유사분열은 고배율 10시야당 3개다. 진단은?"
    choices: ["A. 평활근육종", "B. 세포성 평활근종", "C. 적색변성을 동반한 평활근종", "D. 저등급 자궁내막 간질육종", "E. 악성 잠재성 불명 평활근 종양"]
    answer: "C"
    explanation: "괴사가 있어도 그 사이에 육아조직·유리질화 띠가 낀 경색형이고, 핵 이형성이 없으며 유사분열도 적다 — 악성 기준을 하나도 충족하지 않는다. 임신 중 통증·미열과 분만 뒤 크기 감소는 적색변성(출혈성 경색)에 맞는다. 원래 문항은 핵 이형성이 뚜렷하고 유사분열이 18/10 HPF 에 종양세포 괴사까지 있어 기준 셋을 모두 충족한 평활근육종이었다."
    kind: application
  - id: v2
    of: imaging-2026-0342
    flip: false
    changed: "임신 중 성장 → 폐경 전후 과다 월경과 6개월 새 커진 종괴, 나이 35 → 49세, 그림 대신 조직 소견을 글로 — 「종양세포 괴사·핵 이형성 뚜렷·유사분열 ≥ 10/10 HPF」는 그대로 → 답은 여전히 평활근육종"
    context: "겉모습만 바꾸고 답은 같은 변형 — 임신과 무관한 자궁 종괴"
    stem: "49세 여자가 6개월 동안 늘어난 월경량과 하복부 팽만으로 왔다. 1년 전 건강검진 초음파에서 4 cm 였던 자궁 근층 종괴가 이번에는 10 cm 다. 혈색소 9.8 g/dL 이다. 자궁절제술을 하였다. 종괴는 엇갈리는 다발로 배열한 세포 밀도 높은 방추형 세포로 되어 있고, 살아 있는 종양에서 괴사 구역으로 갑자기 넘어가며 괴사 안에 이형 핵의 윤곽이 남아 있다. 핵 이형성이 미만성으로 뚜렷하고 유사분열은 고배율 10시야당 14개다. 진단은?"
    choices: ["A. 세포성 평활근종", "B. 평활근육종", "C. 적색변성을 동반한 평활근종", "D. 저등급 자궁내막 간질육종", "E. 지방평활근종"]
    answer: "B"
    explanation: "나이·증상·임신 여부·제시 방식이 바뀌었지만 결정적 단서는 같다 — 종양세포 괴사, 미만성 뚜렷한 핵 이형성, 유사분열 ≥ 10/10 HPF 로 세 기준을 모두 충족하므로 평활근육종이다. 세포 밀도가 높다는 점에 끌려 세포성 평활근종을 고르면 안 된다 — 세포성 평활근종에는 이형성·종양세포 괴사가 없다."
    kind: application
sources:
  - id: who-fgt-5
    org: "WHO Classification of Tumours Editorial Board / IARC"
    title: "WHO Classification of Tumours: Female Genital Tumours, 5th ed. — Uterine smooth muscle tumours (leiomyoma variants, STUMP, leiomyosarcoma)"
    kind: textbook
    year: 2020
    citation: "WHO Classification of Tumours Editorial Board. Female Genital Tumours. Lyon: IARC; 2020. 5th ed. — uterine leiomyosarcoma, diagnostic criteria"
    checked_at: 2026-10-18
    checked: "서지만(문항 imaging-2026-0342 해설 근거 목록에서 옮김, 원문 미대조 — 검토 항목). 세 악성 기준과 판정 규칙, 괴사 종류, 세포성·적색변성 평활근종, STUMP, 감별 진단 표의 서술에 쓴다"
    verified: citation
  - id: bell-1994
    org: "Bell SW, Kempson RL, Hendrickson MR"
    title: "Problematic uterine smooth muscle neoplasms: a clinicopathologic study of 213 cases"
    kind: other
    year: 1994
    citation: "Am J Surg Pathol 1994;18(6):535-558"
    pmid: "8179071"
    checked_at: 2026-10-18
    checked: "서지만(문항 해설 근거 목록에서 옮김, 원문·초록 미대조 — 컨테이너가 PubMed 를 막음). PMID 는 기억으로 적었다(학습서 워크플로가 확인 — 검토 항목). 괴사·이형성·유사분열 조합 기준(스탠퍼드 기준)의 근거로 쓴다"
    verified: citation
  - id: harrison-21
    org: "McGraw Hill"
    title: "Harrison's Principles of Internal Medicine, 21st ed. — Chapter 89: Gynecologic Malignancies"
    kind: textbook
    year: 2022
    citation: "Loscalzo J, Fauci AS, Kasper DL, et al (eds). Harrison's Principles of Internal Medicine, 21e. 89장 Gynecologic Malignancies, 인쇄쪽 699–700"
    checked_at: 2026-10-18
    checked: "드라이브 장 문서로 본문 대조. p.699 자궁 평활근에서 양성(평활근종)·악성(평활근육종) 종양이 생기며 임상 양상이 매우 다름. p.700 자궁 육종(암육종·평활근육종)은 흔히 증상 있는 큰 골반 종괴로 발견되고 기능성 출혈이 있을 수도 없을 수도, 골반통으로 오기도 함; 암육종 외 자궁 육종 중 평활근육종이 가장 흔하고 재발 시 도세탁셀/젬시타빈, 보조요법 이득은 뚜렷하지 않음. 조직 진단 기준은 이 장에 없다"
    verified: text
  - id: pmc-lms-pregnancy-2026
    org: "Medicine (Baltimore) (증례 보고, PMC Open Access)"
    title: "Leiomyosarcoma of uterus in pregnancy: A case report"
    kind: other
    year: 2026
    citation: "Medicine (Baltimore) 2026;105(19):e48608"
    doi: "10.1097/MD.0000000000048608"
    url: "https://pmc.ncbi.nlm.nih.gov/articles/PMC13166545/"
    checked_at: 2026-10-18
    checked: "문항 imaging-2026-0342 의 그림(Figure 7)과 그 출처 기록만 확인(exam-builder 풀 기록). 본문은 열지 않았다"
    verified: citation
figures:
- id: f1
  file: docs/assets/figures/pmc-pmc13166545_figure7.jpg
  kind: histology
  at: 가르는 소견 — 괴사의 종류와 핵
  shows: 임신 중 자궁 평활근육종 증례의 재수술 조직(H&E 저배율)
  look_for:
  - 오른쪽 — 세포가 빽빽한 방추형 세포 종양
  - 왼쪽 — 호산성 출혈·무구조 구역과 종양 사이의 경계
  label: '「Pathological image after the second surgery.」 — Leiomyosarcoma of uterus in pregnancy: A case report'
  label_basis: published_figure
  reference: 동료 심사 논문의 그림 설명(저자가 그 소견이라고 쓴 그림)
  paper: 'Leiomyosarcoma of uterus in pregnancy: A case report'
  doi: 10.1097/MD.0000000000048608
  credit: 'Leiomyosarcoma of uterus in pregnancy: A case report. Medicine (Baltimore). 2026 May 8;105(19):e48608. doi: 10.1097/MD.0000000000048608 (CC BY) — Figure 7.'
  license: CC BY
  url: https://pmc.ncbi.nlm.nih.gov/articles/PMC13166545/
  asset: PMC-PMC13166545_Figure7
---

## 판단 — 왜 평활근육종이 먼저인가
- 먼저 계열을 정한다: 엇갈리는 **다발**로 배열한 방추형 세포 = 평활근 종양(평활근 분화). 작은 둥근 세포가 소동맥 주위로 소용돌이치면 자궁내막 간질 종양 쪽이다.
- 평활근 종양의 양성·악성은 **세 기준**으로 가른다 — 종양세포 괴사, 미만성 중등도 이상 핵 이형성, 유사분열 ≥ 10/10 HPF. 둘 이상이면 평활근육종이다 [[?who-fgt-5]] [[?bell-1994]].
- 세포 밀도·크기·빠른 성장은 기준이 아니다 — 세포성 평활근종도 세포가 빽빽하고, 임신 중 평활근종도 빨리 자란다.
- 괴사는 **종류**를 본다. 경색형(유리질화) 괴사만 있고 이형성이 없으면 적색변성 같은 양성 변성이다.

## 기전 — 양성 평활근에서 악성 기준으로
자궁 근층의 평활근 세포는 에스트로겐·프로게스테론에 반응해 자라므로, 양성 평활근종도 임신 중에는 유사분열이 늘고 크기가 빨리 커진다. 그래서 「분열이 많다」 하나로는 악성을 말하지 못한다. 악성 종양은 유전체 불안정으로 핵이 커지고 모양·염색이 제각각인 **이형성**을 보이며, 혈관 공급을 앞질러 자라 살아 있는 종양 한가운데가 갑자기 죽는 **종양세포 괴사**를 만든다. 반면 양성 종양이 크게 자라 혈류가 모자라면 허혈성 경색이 생기는데, 이때는 시간이 흘러 괴사와 생존 조직 사이에 육아조직·유리질화 띠가 생기고 세포 이형성은 없다. 임신 중 적색변성(출혈성 경색)이 그 예다. 세 기준을 함께 보는 이유는 각각이 양성 종양에서도 홀로 나타날 수 있기 때문이다 [[?bell-1994]].

## 가르는 소견 — 괴사의 종류와 핵
- 종양세포 괴사: 살아 있는 종양에서 괴사로 **갑작스러운 경계**, 괴사 안에 이형 핵의 유령 윤곽.
- 경색형 괴사: 사이에 육아조직·유리질화 띠, 이형성 없음 — 적색변성의 모양이다.
- 유사분열은 이형성과 함께 볼 때 의미가 크다. 이형성이 없는 「분열 많은 평활근종」은 임신·호르몬 노출에서 생길 수 있다 [[?who-fgt-5]].
- 혈청 β-hCG 가 음성이면 태반부위 영양막종양 가능성은 낮지만, 조직 소견(중간형 영양막세포·hPL)으로 확인한다.

## 권고와 예외
- 임상에서 평활근육종은 대개 증상 있는 큰 골반 종괴로 발견되며 기능성 출혈이 있을 수도 없을 수도 있다 [[harrison-21: 89장 p.700]]. 평활근종과 평활근육종은 같은 평활근에서 생기지만 임상 경과가 매우 다르다 [[harrison-21: 89장 p.699]].
- 재발한 평활근육종에는 도세탁셀/젬시타빈을 쓰며, 보조요법의 이득은 뚜렷하지 않다 [[harrison-21: 89장 p.700]].
- 기준이 하나뿐이거나 경계 값이면 STUMP 로 보고하고 경과를 본다 [[?who-fgt-5]].
- 조직 기준의 근거는 원문 미대조(†)다 — 수치는 사람 검토가 필요하다.

## 시험 쟁점 — 충돌·맥락·새 근거
- 해당 없음(대조: 해리슨 89장 p.699~700 — 임상 양상·치료만 대조, 조직 기준은 해리슨에 없음)
