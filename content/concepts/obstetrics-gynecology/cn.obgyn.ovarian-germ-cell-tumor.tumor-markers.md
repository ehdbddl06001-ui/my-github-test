---
id: cn.obgyn.ovarian-germ-cell-tumor.tumor-markers
type: concept
topic: Obstetrics & Gynecology
see_also: [Pathology]
date: 2026-11-02
updated: 2026-11-02
version: 1
outline: gyn.oncology            # 산부인과 손 슬롯 「부인암」(outline.py --harrison: 대조 대상 아님) — 같은 주제를 다루는 해리슨 22판 94장(21판 89장, 슬롯 h89)을 따로 읽어 대조했다
confidence: medium
review_status: unreviewed
note_form: 2            # 판형 2(2026-09-25) — 결론·시험 단서·왜 → 혼동 → 표·도식 → 목표에 맞춘 본문
title: "난소 생식세포종양 — 10대 고형 종괴는 AFP·hCG·LDH"
objective: "10대·젊은 여성의 빠르게 커지는 한쪽 고형 난소 종괴에서 수술 전 혈청 표지자로 알파태아단백·β-hCG·LDH 를 고른다"
objective_kind: 검사 선택
condition: 악성 난소 생식세포종양(malignant ovarian germ cell tumor)의 수술 전 표지자
exams: [kmle, usmle]
summary:
  - "결론: 10대의 빠르게 커지는 한쪽 고형 난소 종괴는 수술 전에 알파태아단백(AFP)·β-hCG·LDH 를 잰다."
  - "시험 단서: 사춘기 소녀 + 수주 사이 커진 큰 고형 종괴(germ cell tumor), 호르몬 징후 없음, 임신반응 음성."
  - "왜: 생식세포종양은 사춘기에 가장 흔한 난소 악성종양이고 표지자는 기원 세포가 만드는 물질이다."
  - "CA-125·HE4 는 상피성 암, 인히빈·에스트라디올은 과립막세포종, 테스토스테론은 Sertoli-Leydig 세포종 쪽이다."
pitfalls:
  - contrast: "인히빈 B·에스트라디올 vs AFP·β-hCG·LDH — 젊은 여성의 고형 종괴면 과립막세포종?"
    point: "인히빈·에스트라디올은 에스트로겐을 만드는 성끈-간질 종양의 표지자다. 간질 종양은 대부분 에스트로겐을 만들지 않고, 만들 때는 월경 이상·조기 사춘기·폐경 후 출혈 같은 호르몬 징후로 드러난다 [[harrison-22: 94장 p.710]] [[harrison-22: 94장 p.712]]. 징후가 없는 사춘기 고형 종괴는 생식세포종양 표지자가 먼저다."
    exception: "월경 사이 출혈·조기 사춘기·자궁내막 증식이 함께 있으면 인히빈·에스트라디올을 고른다."
    covers: ["kmle-2026-1690:E"]
  - contrast: "CA-125·HE4 — 난소 종괴면 CA-125?"
    point: "CA-125(MUC16)·HE4 는 상피성 난소암에서 오르는 물질이고 CA-125 는 특이하지 않다 [[harrison-22: 94장 p.710]]. 상피성 암은 복수·복합성 종괴로 나타나는 나이 든 여성의 종양이라 10대의 고형 종괴에 먼저 고를 표지자가 아니다."
    exception: "폐경 전후 여성의 복수를 동반한 양쪽 복합성 종괴면 CA-125·HE4."
  - contrast: "테스토스테론·DHEA-S — 젊은 여성의 난소 종양 = 호르몬 종양?"
    point: "안드로겐 표지자는 여드름·다모·목소리 변화 같은 남성화 징후가 있을 때 고른다(Sertoli-Leydig 세포종·부신 원인). 남성화 징후가 없으면 결과가 계획을 바꾸지 않는다 [[?novak-16]]."
tables:
  - id: germ-markers
    section: "가르는 소견 — 기원 세포가 표지자를 정한다"
    title: "난소 종양 — 기원 세포별 혈청 표지자"
    role: differential
    span: column
    columns: ["기원 세포", "대표 종양", "표지자"]
    rows:
      - ["생식세포", "난황낭종양 · 융모막암종 · 미분화세포종", "AFP · β-hCG · LDH [[harrison-22: 94장 p.712]] [[?novak-16]]"]
      - ["체강 상피", "고등급 장액성 암", "CA-125 · HE4 [[harrison-22: 94장 p.710]]"]
      - ["성끈-간질(과립막세포)", "과립막세포종", "인히빈 · 에스트라디올 [[?novak-16]]"]
      - ["성끈-간질(Sertoli-Leydig)", "Sertoli-Leydig 세포종", "테스토스테론 [[?novak-16]]"]
  - id: germ-subtype
    section: "기전 — 전능 세포에서 여러 표지자로"
    title: "악성 생식세포종양 — 어떤 표지자를 내나"
    role: differential
    span: column
    columns: ["종양", "표지자"]
    rows:
      - ["미분화세포종(dysgerminoma)", "LDH(일부 β-hCG) [[?novak-16]]"]
      - ["난황낭종양(yolk sac tumor)", "AFP [[?novak-16]]"]
      - ["융모막암종(choriocarcinoma)", "β-hCG [[?novak-16]]"]
      - ["미성숙 기형종 · 배아암", "AFP 가 오를 수 있다 [[?novak-16]]"]
diagram:
  title: "젊은 여성의 고형 난소 종괴 — 수술 전 표지자"
  nodes:
    - {id: start, kind: start, text: "10대·20대의 빠르게 커지는 고형 난소 종괴"}
    - {id: preg, kind: decision, text: "임신반응 음성인가?"}
    - {id: pregdo, kind: info, text: "소변·혈청 hCG 로 임신 먼저 확인"}
    - {id: pregyes, kind: alert, text: "임신 관련 종괴 평가"}
    - {id: horm, kind: decision, text: "호르몬 징후가 있는가?"}
    - {id: hormask, kind: info, text: "월경 양상·남성화 징후 확인"}
    - {id: germ, kind: end, text: "생식세포종양 의심 → AFP·β-hCG·LDH"}
    - {id: estro, kind: end, text: "에스트로겐 징후 → 인히빈·에스트라디올"}
    - {id: andro, kind: end, text: "남성화 징후 → 테스토스테론"}
  edges:
    - {from: start, to: preg}
    - {from: preg, to: horm, label: "음성"}
    - {from: preg, to: pregyes, label: "양성"}
    - {from: preg, to: pregdo, label: "미시행"}
    - {from: pregdo, to: horm, label: "음성이면"}
    - {from: pregdo, to: pregyes, label: "양성이면"}
    - {from: horm, to: germ, label: "없음"}
    - {from: horm, to: estro, label: "출혈·조기 사춘기"}
    - {from: horm, to: andro, label: "다모·변성"}
    - {from: horm, to: hormask, label: "정보 없음"}
    - {from: hormask, to: germ, label: "징후 없음"}
    - {from: hormask, to: estro, label: "에스트로겐 징후"}
diagram_notes:
  - "소변 임신반응은 임신을 배제하는 검사이고, 혈청 β-hCG 정량은 종양 표지자로 따로 잰다 — 임신반응 음성이어도 β-hCG 표지자를 뺄 이유가 되지 않는다."
  - "폐경 전후 여성의 복수 동반 양쪽 복합성 종괴는 이 도식 밖이다 — 상피성 암, CA-125·HE4 [[harrison-22: 94장 p.710]]."
  - "수술 전 수치는 진단의 단서이자 수술·항암치료 뒤 추적의 기준값이다 [[?novak-16]]."
  - "석회화·지방이 섞인 낭성 종괴는 양성 기형종(유피낭종) 쪽이다 — 젊은 여성의 가장 흔한 생식세포 종양 [[harrison-22: 94장 p.712]]."
checks:
  - q: "17세, 수주 사이 커진 14 cm 한쪽 고형 난소 종괴, 호르몬 징후 없음. 수술 전 혈액검사는?"
    a: "AFP·β-hCG·LDH — 사춘기 난소 악성종양의 대부분인 생식세포종양의 표지자."
  - q: "AFP·β-hCG·LDH 는 각각 어떤 생식세포종양을 가리키나?"
    a: "AFP = 난황낭종양, β-hCG = 융모막암종, LDH = 미분화세포종."
  - q: "인히빈·에스트라디올을 고르려면 어떤 단서가 있어야 하나?"
    a: "에스트로겐 징후 — 월경 사이 출혈·조기 사춘기·폐경 후 출혈·자궁내막 증식."
variants:
  - id: v1
    of: kmle-2026-1690
    flip: true
    changed: "규칙적 월경 → 석 달째 불규칙한 월경 사이 출혈, 초음파에 자궁내막 비후 추가 → 에스트로겐 분비 성끈-간질 종양(과립막세포종) 의심으로 답이 AFP·β-hCG·LDH 에서 인히빈 B·에스트라디올로 바뀜"
    context: "단서를 바꿔 답이 바뀌는 변형 — 에스트로겐 징후가 있는 고형 종괴"
    stem: "24세 여자가 석 달 전부터 월경과 월경 사이에 질 출혈이 잦고 아랫배가 묵직하다며 왔다. 이전에는 월경이 28일 주기로 규칙적이었다. 여드름·다모·목소리 변화는 없고 성경험은 있으나 소변 임신반응은 음성이다. 진찰에서 골반에 단단하고 압통 없는 종괴가 만져진다. 질초음파에서 오른쪽 난소에서 기원한 9 cm 고형 종괴가 있고 자궁내막 두께는 18 mm이며 복수는 없다. 수술 전 시행할 혈액검사로 가장 적절한 것은?"
    choices: ["A. 알파태아단백·β-hCG·LDH", "B. CA-125·HE4", "C. CEA·CA19-9", "D. 테스토스테론·DHEA-S", "E. 인히빈 B·에스트라디올"]
    answer: "E"
    explanation: "고형 난소 종괴에 월경 사이 출혈과 두꺼운 자궁내막이 겹쳤다 — 종양이 에스트로겐을 만드는 신호다. 에스트로겐을 만드는 성끈-간질 종양(과립막세포종)을 의심해 인히빈 B·에스트라디올을 잰다. 원래 문항은 월경이 규칙적이고 호르몬 징후가 없는 10대의 빠르게 커진 종괴라 생식세포종양 표지자(AFP·β-hCG·LDH)가 답이었다."
    kind: application
  - id: v2
    of: kmle-2026-1690
    flip: false
    changed: "나이 17 → 20세, 내원 경위(배가 불러 옴 → 아랫배 통증으로 응급실), 종괴 쪽 왼쪽 → 오른쪽·크기 14 → 11 cm, 영상 CT 로 — 「젊은 나이 + 빠르게 커진 한쪽 고형 종괴 + 호르몬 징후 없음」은 그대로 → 답은 여전히 AFP·β-hCG·LDH"
    context: "겉모습만 바꾸고 답은 같은 변형 — 응급실에서 발견"
    stem: "20세 여자가 일주일 전부터 아랫배가 뻐근하게 아파 응급실에 왔다. 한 달 사이 배가 부쩍 나왔다고 한다. 월경은 30일 주기로 규칙적이고 마지막 월경은 10일 전이었다. 여드름·다모·목소리 변화는 없다. 소변 임신반응은 음성이다. 복부 CT 에서 오른쪽 난소에서 기원한 11 cm 고형 종괴가 있고 조영 증강이 뚜렷하며 석회화·지방은 없고 복수는 없다. 반대쪽 난소는 정상이다. 수술 전 시행할 혈액검사로 가장 적절한 것은?"
    choices: ["A. CA-125·HE4", "B. 인히빈 B·에스트라디올", "C. 알파태아단백·β-hCG·LDH", "D. CEA·CA19-9", "E. 테스토스테론·DHEA-S"]
    answer: "C"
    explanation: "나이·내원 경위·종괴 쪽과 크기·영상 검사가 바뀌었지만, 젊은 여성의 빠르게 커진 한쪽 고형 종괴이고 호르몬 징후가 없다는 결정적 단서는 그대로다 — 악성 생식세포종양을 먼저 생각해 AFP·β-hCG·LDH 를 잰다. 석회화·지방이 없어 양성 기형종 쪽도 아니다."
    kind: application
sources:
  - id: harrison-22
    org: "McGraw Hill"
    title: "Harrison's Principles of Internal Medicine, 22nd ed. — Chapter 94: Gynecologic Malignancies"
    kind: textbook
    year: 2025
    citation: "Harrison's Principles of Internal Medicine, 22e. 94장 p.710–712"
    checked_at: 2026-11-02
    checked: "드라이브 22판 장별 문서 H22_94 본문 대조 — 난소 종양은 상피·간질·생식세포 계열, 젊은 여성의 종양은 양성이 많음, 간질 종양 대부분은 에스트로겐을 만들지 않음, 생식세포 종양은 고환 종양과 생물학이 비슷(p.710) · CA-125 = MUC16, 난소암과 연관되나 특이하지 않음, CA-125·mesothelin·HE4(p.710) · 간질 종양 약 7 %, 50–60대, 한쪽 고형 종괴, 드물게 에스트로겐 → 유방 압통·조기 사춘기·월경 이상·폐경 후 출혈(p.712) · 생식세포 종양: 양성 기형종이 가장 흔함(젊은 여성), 악성 = 미분화세포종·난황낭종양·미성숙 기형종·배아암·융모막암종, 발생 정점은 청소년, 일부가 hCG·AFP 를 만듦, 양측은 드묾(미분화세포종 10–15 %), 치료는 한쪽 난소(난관)절제+림프절 표본, 진행성은 BEP(p.712). 해리슨에 없는 것: 종양별 표지자 짝(AFP-난황낭, hCG-융모막, LDH-미분화세포종), LDH, 인히빈"
    verified: text
  - id: novak-16
    org: "Wolters Kluwer"
    title: "Berek & Novak's Gynecology, 16th ed. — Nonepithelial Ovarian Cancer"
    kind: textbook
    year: 2019
    citation: "Berek JS (ed). Berek & Novak's Gynecology, 16e. ch. Nonepithelial Ovarian Cancer"
    checked_at: 2026-11-02
    checked: "서지만(문항 kmle-2026-1690 해설 근거 목록에서 옮김, 원문 미대조 — 검토 항목). 종양별 표지자 짝(AFP·β-hCG·LDH), 성끈-간질 종양의 인히빈·테스토스테론에 쓴다"
    verified: citation
  - id: nccn-ovarian
    org: "NCCN"
    title: "NCCN Clinical Practice Guidelines in Oncology — Ovarian Cancer (Less Common Ovarian Cancers: Malignant Germ Cell Tumors)"
    kind: guideline
    year: 2026
    citation: "NCCN Guidelines, Ovarian Cancer — Malignant Germ Cell Tumors"
    url: "https://www.nccn.org/guidelines/category_1"
    checked_at: 2026-11-02
    checked: "서지만(문항 해설 근거 목록에서 옮김, 원문 미대조 — 검토 항목)"
    verified: citation
figures_none: 혈청 표지자를 고르는 검사 선택 목표 — 판독할 영상 소견이 시험 단서가 아니다
---

## 판단 — 왜 AFP·β-hCG·LDH 가 먼저인가
- 나이가 종양 계열을 정한다: 생식세포종양은 발생 정점이 청소년이고, 상피성 암은 나이 든 여성의 종양이다 [[harrison-22: 94장 p.712]].
- 빠르게 커지는 큰 **고형** 종괴는 양성 기형종(유피낭종 — 석회화·지방이 섞인 낭종)보다 악성 생식세포종양을 먼저 생각하게 한다 [[harrison-22: 94장 p.712]].
- 호르몬 징후(월경 사이 출혈·조기 사춘기·남성화)가 없으면 호르몬을 만드는 성끈-간질 종양 가능성이 낮다 — 간질 종양 대부분은 에스트로겐을 만들지 않고, 만들 때는 이 징후로 드러난다 [[harrison-22: 94장 p.710]] [[harrison-22: 94장 p.712]].
- 표지자는 그 세포가 만드는 물질이다 — 생식세포종양 일부가 hCG·AFP 를 만들고 [[harrison-22: 94장 p.712]], 미분화세포종은 LDH 가 오른다 [[?novak-16]]. 수술 전 수치가 추적의 기준값이 된다.

## 기전 — 전능 세포에서 여러 표지자로
생식세포는 거의 모든 조직으로 분화할 수 있는 전능 세포라, 생식세포종양은 양성 기형종부터 미분화세포종·미성숙 기형종·난황낭종양·융모막암종까지 모양이 제각각이다 [[harrison-22: 94장 p.712]]. 어느 쪽으로 분화했는지가 표지자를 정한다 — 난황낭(태아 간·난황낭 성분)은 AFP, 영양막(융모막암종)은 hCG 를 만들고, 원시 생식세포를 닮은 미분화세포종은 특정 단백 대신 LDH 가 오른다 [[?novak-16]]. 고환 종양과 생물학이 비슷해 표지자와 항암 요법(BEP)도 같다 [[harrison-22: 94장 p.710]] [[harrison-22: 94장 p.712]]. 섞인 종양이 흔해 하나만 재지 않고 셋을 함께 잰다 [[?novak-16]].

## 가르는 소견 — 기원 세포가 표지자를 정한다
- 상피·성끈-간질·생식세포 중 어디서 나왔는지를 나이·종괴 모양·호르몬 징후로 먼저 가늠한다(표) [[harrison-22: 94장 p.710]].
- CA-125 는 상피성 암과 연관되지만 특이하지 않아 [[harrison-22: 94장 p.710]], 가임기 여성에서는 월경·자궁내막증·골반염에서도 오른다 — 10대 고형 종괴에서 정상이어도 악성을 배제하지 못한다 [[?novak-16]].
- 소변 임신반응 음성은 임신 관련 종괴를 배제할 뿐이다 — 혈청 β-hCG 정량은 종양 표지자로 따로 본다.

## 권고와 예외
- 생식세포종양은 양측이 드물어(미분화세포종만 10–15 %) 가임력을 보존하는 한쪽 난소(난관)절제와 림프절 표본이 원칙이다 [[harrison-22: 94장 p.712]].
- 진행성 악성 생식세포종양은 고환 종양처럼 BEP(블레오마이신·에토포시드·시스플라틴) 항암치료를 한다. 미분화세포종은 방사선에도 잘 듣지만 불임을 일으켜 BEP 가 같거나 더 낫다 [[harrison-22: 94장 p.712]].
- 수술 전에는 침 생검으로 진단하지 않는다 — 복강 오염 위험 [[harrison-22: 94장 p.711]].

## 시험 쟁점 — 충돌·맥락·새 근거
- **Z1 맥락 · 표지자 짝의 근거** — 시험 기준: AFP = 난황낭종양, β-hCG = 융모막암종, LDH = 미분화세포종 [[?novak-16]] / 다른 기준: 해리슨 22판은 「일부 생식세포 종양이 hCG·AFP 를 만든다」까지만 쓰고 LDH 와 종양별 짝은 적지 않는다 [[harrison-22: 94장 p.712]] / 왜 다른가: 내과 교과서는 부인종양 세부를 다루지 않는다 / 시험에서는: KMLE · USMLE 모두 세 표지자를 함께 고르는 것이 답이다. 짝의 원문 대조가 남은 검토 항목이다.
