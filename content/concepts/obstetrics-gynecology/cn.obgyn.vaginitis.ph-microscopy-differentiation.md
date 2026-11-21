---
id: cn.obgyn.vaginitis.ph-microscopy-differentiation
type: concept
topic: Obstetrics & Gynecology
see_also: [Infectious Disease]
date: 2026-11-20
updated: 2026-11-20
version: 1
outline: gyn.infection   # 기본틀 슬롯(content/outline/subjects.yaml) — 산부인과 손 슬롯 「생식기 감염과 성매개감염」
confidence: medium
review_status: unreviewed
note_form: 2            # 판형 2(2026-09-25) — 기본틀 빈 슬롯으로 쓴 정리본(오답 연결 없음)
title: "질염 — pH·도말로 가르고 파트너 치료는 원충만"
objective: "질 분비물 환자에서 질 pH·아민 검사·현미경 소견으로 세균질증·칸디다 질염·트리코모나스 질염을 가르고, 각각의 치료와 성 파트너 치료 여부를 고른다"
objective_kind: 감별
condition: 질염(vaginitis) — 세균질증(bacterial vaginosis) · 외음질 칸디다증(vulvovaginal candidiasis) · 트리코모나스증(trichomoniasis)
exams: [kmle, usmle]
summary:
  - "결론: pH >4.5+아민 냄새+단서세포는 세균질증, pH 정상+효모·가성균사는 칸디다, 움직이는 편모충은 트리코모나스."
  - "시험 단서: 생선 냄새 묽은 회백색 분비물(whiff test), 흰 덩어리 분비물+외음 가려움, 황록색 분비물·딸기 자궁경부."
  - "왜: 젖산균이 혐기균으로 바뀌면 pH·아민이 오르고, 칸디다는 pH 를 바꾸지 않으며, 원충은 성 접촉으로 옮는다."
  - "파트너: 트리코모나스만 현재 파트너를 함께 치료한다 — 세균질증·칸디다는 파트너 치료를 권하지 않는다."
  - "도말 음성은 배제가 아니다 — 현미경 민감도는 약 50 %라 증상이 있으면 NAAT·배양으로 확인한다."
pitfalls:
  - contrast: "세균질증도 성 파트너를 함께 치료?"
    point: "세균질증은 성생활과 관련되지만 파트너를 치료해도 여성의 반응·재발이 달라지지 않아 일상적 파트너 치료를 권하지 않는다. 파트너를 함께 치료하는 것은 트리코모나스다 [[cdc-sti-2021: Bacterial Vaginosis — Management of Sex Partners]]."
    cites: ["cdc-sti-2021: Trichomoniasis — Management of Sex Partners"]
  - contrast: "트리코모나스 — 여성도 메트로니다졸 2 g 단회?"
    point: "여성 권고는 메트로니다졸 500 mg 하루 2번 7일이다. 7일 요법이 2 g 단회보다 1개월 뒤 재양성을 절반으로 줄였다. 2 g 단회는 남성 권고다 [[cdc-sti-2021: Trichomoniasis — Treatment]]."
  - contrast: "트리코모나스에 메트로니다졸 질정·젤?"
    point: "질 젤은 요도·질 주위샘에서 치료 농도에 이르지 못해 경구보다 덜 효과적이어서 권하지 않는다 — 경구 니트로이미다졸만 효과가 입증된 약군이다 [[cdc-sti-2021: Trichomoniasis — Treatment]]."
  - contrast: "pH 정상이면 트리코모나스 배제?"
    point: "트리코모나스는 대개 pH 가 오르지만 정상 pH 에서도 있을 수 있다. pH 는 특이도가 낮아 반드시 도말로 이어 본다 [[cdc-sti-2021: Diseases Characterized by Vulvovaginal Itching…]]."
  - contrast: "증상 없는 칸디다 배양 양성 = 치료?"
    point: "여성의 10–20 %가 질에 칸디다를 지니고 있어 증상·징후 없는 배양 양성은 치료 적응이 아니다 [[cdc-sti-2021: Uncomplicated VVC — Diagnostic Considerations]]."
  - contrast: "임신부 칸디다 질염에 플루코나졸 150 mg 단회?"
    point: "임신 중에는 국소 아졸 7일만 권한다. 플루코나졸 150 mg 단회는 자연유산·선천 기형과의 연관이 보고되어 쓰지 않는다 [[cdc-sti-2021: Complicated VVC — Pregnancy]]."
tables:
  - id: ddx
    section: "가르는 소견 — pH·아민·도말"
    title: "질염 셋 — 진료실 검사로 가르기"
    role: differential
    span: column
    columns: ["질환", "pH·아민(KOH)", "현미경", "분비물·진찰"]
    rows:
      - ["세균질증", "pH >4.5 · KOH 넣으면 생선 냄새(whiff)", "식염수: 단서세포(clue cell) — 가장자리가 작은 혐기균으로 가려진 상피세포", "균질하고 묽은 우유 같은 분비물이 질벽을 덮는다"]
      - ["칸디다 질염", "정상 pH(<4.5) · 아민 냄새 없음", "KOH: 싹트는 효모·균사·가성균사", "외음 가려움·부종·균열, 진한 흰 덩어리 분비물, 외부 배뇨통"]
      - ["트리코모나스", "대개 pH 상승(정상일 수도) · 아민 냄새 가능", "식염수: 움직이는 편모충 — 채취 직후 봐야 한다", "퍼지고 냄새나는 황록색 분비물, 딸기 모양 자궁경부(질확대경에서 더 잘 보임)"]
    note: "모두 cdc-sti-2021 의 질염 머리말 · 각 질환 진단 절. 원충·효모 모두 도말 민감도는 NAAT·배양 대비 약 50 % 다."
  - id: tx
    section: "선택 — 치료와 성 파트너"
    title: "치료 · 파트너 · 임신"
    role: treatment
    span: column
    columns: ["질환", "권고 치료(비임신)", "성 파트너", "임신"]
    rows:
      - ["세균질증(증상 있을 때)", "메트로니다졸 500 mg 하루 2번 7일, 또는 메트로니다졸 젤 0.75 % 5일, 또는 클린다마이신 크림 2 % 7일 [[cdc-sti-2021: BV — Recommended Regimens]]", "일상적 치료 권하지 않음 [[cdc-sti-2021: BV — Management of Sex Partners]]", "증상 있으면 모두 치료(권고 요법 어느 것이나). 티니다졸 피함. 무증상 선별 권하지 않음 [[cdc-sti-2021: BV — Pregnancy]]"]
      - ["칸디다 질염(비복잡)", "단기 국소 아졸(1–3일 포함) 또는 플루코나졸 150 mg 경구 단회 [[cdc-sti-2021: VVC — Recommended Regimens]]", "자료 없어 권하지 않음 — 귀두염 있는 남성만 국소 항진균제 [[cdc-sti-2021: Uncomplicated VVC — Management of Sex Partners]]", "국소 아졸 7일만. 플루코나졸 쓰지 않음 [[cdc-sti-2021: Complicated VVC — Pregnancy]]"]
      - ["트리코모나스", "여성: 메트로니다졸 500 mg 하루 2번 7일. 남성: 메트로니다졸 2 g 단회. 대안: 티니다졸 2 g 단회 [[cdc-sti-2021: Trichomoniasis — Recommended Regimens]]", "현재 파트너를 추정 치료로 보낸다. 둘 다 치료를 마칠 때까지 성관계 금지 [[cdc-sti-2021: Trichomoniasis — Management of Sex Partners]]", "증상 있으면 주수와 관계없이 검사·치료. 티니다졸 피함 [[cdc-sti-2021: Trichomoniasis — Pregnancy]]"]
criteria:
  - id: amsel
    name: Amsel 기준(세균질증 임상 진단)
    kind: 진단 기준
    population: "질 증상이 있는 여성"
    statement: "네 가지 중 셋 이상 — ① 균질하고 묽은(우유 같은) 분비물이 질벽을 고르게 덮음 ② 현미경에서 단서세포 ③ 질액 pH >4.5 ④ 10 % KOH 를 넣기 전·후 생선 냄새(whiff test) [[cdc-sti-2021: BV — Diagnostic Considerations]]"
    exceptions: "Nugent 점수(그람 염색) 대비 민감도 37–70 %, 특이도 94–99 %. 그람 염색이 검사실 기준 표준(Nugent 7–10 = 세균질증) [[cdc-sti-2021: BV — Diagnostic Considerations]]"
    source: cdc-sti-2021
    basis: current
    exams: [kmle, usmle]
sources:
  - id: cdc-sti-2021
    org: "CDC (Workowski KA, Bachmann LH, Chan PA, et al.)"
    title: "Sexually Transmitted Infections Treatment Guidelines, 2021"
    kind: guideline
    year: 2021
    citation: "MMWR Recomm Rep 2021;70(4):1-187 — 「Diseases Characterized by Vulvovaginal Itching, Burning, Irritation, Odor, or Discharge」 절(Bacterial Vaginosis · Trichomoniasis · Vulvovaginal Candidiasis)"
    doi: "10.15585/mmwr.rr7004a1"
    pmid: "34292926"
    url: "https://pmc.ncbi.nlm.nih.gov/articles/PMC8344968/"
    checked_at: 2026-11-20
    checked: "PMC8344968 전문(PubMed MCP)에서 질염 머리말 · 세균질증 · 트리코모나스증 · 외음질 칸디다증 절을 처음부터 끝까지 읽음 — pH >4.5 는 세균질증·트리코모나스(트리코모나스는 정상 pH 가능), KOH 아민 냄새 = 세균질증·트리코모나스, 단서세포 정의, 도말 민감도 약 50 %(NAAT·배양 대비), WBC 만 있으면 자궁경부염 가능; Amsel 4개 중 3개 · Nugent 0–3/4–6/7–10 · Amsel 민감도 37–70 %·특이도 94–99 %; 세균질증 파트너 치료 권하지 않음·임신 중 증상 있으면 치료·무증상 선별 안 함·티니다졸 피함·메트로니다졸과 음주 금지 불필요; 트리코모나스 여성 7일 요법 근거(2 g 단회 대비 재양성 절반)·질 젤 비권고·파트너 추정 치료·3개월 내 재검·임신 중 티니다졸 피함; 칸디다 정상 pH(<4.5)·KOH 로 효모·가성균사·증상 없는 배양 양성은 치료 안 함(10–20 % 보유)·파트너 치료 자료 없음·임신 중 국소 아졸 7일만·플루코나졸 150 mg 단회 쓰지 않음·재발(1년 3회 이상) 정의. PMC 텍스트에서 권고 요법 상자의 기울임 약 이름이 빠져 있어, 상자의 약 이름·제형은 같은 지침의 CDC 웹판(cdc.gov/std/treatment-guidelines/bv.htm · trichomoniasis.htm · candidiasis.htm, 2026-11-20 열람)에서 대조했다"
    verified: text
diagram:
  title: "질 분비물 — pH 에서 도말, 치료와 파트너까지"
  nodes:
    - {id: start, kind: start, text: "질 분비물·가려움·냄새"}
    - {id: ph, kind: decision, text: "질 pH >4.5?"}
    - {id: test, kind: info, text: "pH 종이 · 식염수·KOH 도말을 시행"}
    - {id: wet, kind: decision, text: "식염수 도말에 움직이는 편모충?"}
    - {id: tv, kind: end, text: "트리코모나스 — 메트로니다졸 7일 + 파트너 치료"}
    - {id: amsel, kind: decision, text: "Amsel 4개 중 3개 이상?"}
    - {id: bv, kind: end, text: "세균질증 — 메트로니다졸 · 파트너 치료 안 함"}
    - {id: koh, kind: decision, text: "KOH 에 효모·가성균사?"}
    - {id: vvc, kind: end, text: "칸디다 — 아졸 · 파트너 치료 안 함"}
    - {id: more, kind: alert, text: "도말 음성 = 배제 아님 → NAAT·배양 · 자궁경부염"}
  edges:
    - {from: start, to: ph}
    - {from: ph, to: wet, label: ">4.5"}
    - {from: ph, to: koh, label: "≤4.5"}
    - {from: ph, to: test, label: "측정 안 함"}
    - {from: test, to: wet, label: "pH 높음"}
    - {from: test, to: koh, label: "pH 정상"}
    - {from: wet, to: tv, label: "보임"}
    - {from: wet, to: amsel, label: "안 보임"}
    - {from: amsel, to: bv, label: "예"}
    - {from: amsel, to: more, label: "아니오"}
    - {from: koh, to: vvc, label: "보임"}
    - {from: koh, to: more, label: "안 보임"}
diagram_notes:
  - "pH 는 특이도가 낮다 — 트리코모나스는 정상 pH 에서도 있을 수 있어, pH 정상이라도 증상이 맞으면 식염수 도말·NAAT 를 함께 본다 [[cdc-sti-2021: Diseases Characterized by Vulvovaginal Itching…]]."
  - "식염수 도말은 채취 직후 본다 — 편모충 검출 민감도는 1시간 안에 약 20 %까지 떨어진다 [[cdc-sti-2021: Trichomoniasis — Diagnostic Considerations]]."
  - "원충·효모가 없는데 백혈구만 많으면 자궁경부염을 생각한다. 원인균이 없는데 염증 소견만 있으면 기계적·화학적·알레르기 원인도 있다 [[cdc-sti-2021: Diseases Characterized by Vulvovaginal Itching…]]."
  - "칸디다 도말 음성이지만 증상이 있으면 칸디다 배양을 고려한다(배양이 기준 표준) [[cdc-sti-2021: Uncomplicated VVC — Diagnostic Considerations]]."
checks:
  - q: "질 분비물에 10 % KOH 를 떨어뜨리자 생선 냄새가 났다. 가능한 원인 둘은?"
    a: "세균질증과 트리코모나스. 칸디다는 아민 냄새가 없고 pH 도 정상이다."
  - q: "트리코모나스 여성 환자와 그 남성 파트너의 권고 치료는 각각?"
    a: "여성은 메트로니다졸 500 mg 하루 2번 7일, 남성은 메트로니다졸 2 g 단회. 현재 파트너는 추정 치료로 보내고 둘 다 치료를 마칠 때까지 성관계를 피한다."
  - q: "세균질증이 반복되는 여성의 남편을 함께 치료해야 하나?"
    a: "권하지 않는다. 파트너 치료가 여성의 치료 반응·재발을 바꾸지 않았다."
figures_wanted:
- source: PMC_OA
  shows: 세균질증의 단서세포 — 상피세포 가장자리를 작은 균이 덮어 경계가 흐려진다
  at: 가르는 소견 — pH·아민·도말
  query: '"bacterial vaginosis" AND "clue cells" AND (microscopy OR "wet mount" OR "Gram stain")'
  caption_terms:
  - clue cell
  modality: MICROSCOPY
- source: PMC_OA
  shows: 트리코모나스 질염의 생리식염수 도말 — 편모가 있는 원충
  at: 가르는 소견 — pH·아민·도말
  query: '"Trichomonas vaginalis" AND ("wet mount" OR "saline microscopy") AND "case report"'
  caption_terms:
  - trichomona
  modality: MICROSCOPY
figures_rejected:
- asset: PMC-PMC11905427_Fig3
  reason: 그림이 진단 정확도 숲 그림(forest plot)이다 — 트리코모나스 도말 소견이 없다
- asset: PMC-PMC13493514_FIGURE2
  reason: 단서세포 패널이 개당 약 65 px 썸네일 격자 — 진단명 표지를 빼고 자르면 짧은 변 134 px(<250)라 인쇄에서 소견이 안 보인다
---

## 판단 — 왜 pH 다음에 도말인가
- 병력만으로는 질염 원인을 맞히기 어렵고 잘못된 투약으로 이어진다 — 진료실에서는 **pH · KOH 아민 검사 · 생리식염수/KOH 도말** 셋으로 원인을 정한다 [[cdc-sti-2021: Diseases Characterized by Vulvovaginal Itching…]].
- pH 는 둘로 나눌 뿐이다: >4.5 면 세균질증·트리코모나스, 정상이면 칸디다 쪽. 특이도가 낮아 결론은 도말에서 낸다 [[cdc-sti-2021: Diseases Characterized by Vulvovaginal Itching…]].
- 같은 「질염」이라도 **파트너 치료**는 원인에 따라 갈린다 — 성 접촉으로 옮는 트리코모나스만 현재 파트너를 함께 치료한다 [[cdc-sti-2021: Trichomoniasis — Management of Sex Partners]].

## 기전 — 젖산균 질에서 무엇으로 바뀌나
- **세균질증(bacterial vaginosis, BV)**: 과산화수소·젖산을 만드는 정상 젖산균이 고농도 혐기균으로 바뀐 질 세균 불균형(dysbiosis)이다. 상피세포 위에 여러 균의 생물막이 생기고, 이 작은 혐기균이 상피세포 가장자리를 덮은 것이 단서세포다 [[cdc-sti-2021: Bacterial Vaginosis]]. KOH 를 넣으면 아민(트리메틸아민) 냄새가 난다 [[cdc-sti-2021: BV — Diagnostic Considerations]]. 남성 생식기에서도 관련 균이 나오지만 남성 파트너 치료는 재발을 막지 못했다 [[cdc-sti-2021: Bacterial Vaginosis]].
- **칸디다 질염(vulvovaginal candidiasis, VVC)**: 칸디다(*Candida*) 효모가 원인이다. 질 pH 는 정상(<4.5)이고, KOH 가 세포 성분을 녹여 효모·가성균사가 잘 보인다. 대개 성 접촉으로 옮지 않는다 [[cdc-sti-2021: Uncomplicated VVC — Diagnostic Considerations]].
- **트리코모나스증(trichomoniasis)**: 원충 *Trichomonas vaginalis* 의 성매개감염. 70–85 %는 증상이 거의 없고, 치료하지 않으면 수개월~수년 간다 [[cdc-sti-2021: Trichomoniasis]].

## 가르는 소견 — pH·아민·도말
- 표가 세 질환의 pH·아민·도말·진찰 소견을 나란히 놓는다. 세균질증은 Amsel 4개 중 3개로 임상 진단한다(기준 칸) [[cdc-sti-2021: BV — Diagnostic Considerations]].
- **음성 결과의 한계**: 도말의 편모충·효모 검출 민감도는 약 50 %라 음성이어도 배제하지 못한다 — 트리코모나스는 NAAT, 칸디다는 배양으로 확인한다 [[cdc-sti-2021: Diseases Characterized by Vulvovaginal Itching…]].
- 자궁경부 세포검사(Pap)는 세균질증·트리코모나스의 진단 검사가 아니다 — Pap 에서 트리코모나스가 보이면 민감한 검사로 다시 확인한다 [[cdc-sti-2021: BV — Diagnostic Considerations]] [[cdc-sti-2021: Trichomoniasis — Diagnostic Considerations]].

## 선택 — 치료와 성 파트너
- 세균질증은 **증상이 있을 때** 치료한다. 경구와 국소 치료의 효과를 직접 비교한 자료는 없다 [[cdc-sti-2021: BV — Treatment]].
- 트리코모나스는 니트로이미다졸만 효과가 입증되었다. 여성은 7일 요법이 단회보다 낫다. 치료 뒤 성생활하는 여성은 3개월 안에 다시 검사한다(재감염이 많다) [[cdc-sti-2021: Trichomoniasis — Follow-Up]]. HIV·매독·임질·클라미디아 검사도 함께 한다 [[cdc-sti-2021: Trichomoniasis — Other Management Considerations]].
- 칸디다는 단기 국소 아졸로 증상 완화·배양 음성이 80–90 % [[cdc-sti-2021: Uncomplicated VVC — Treatment]].

## 권고와 예외
- 세균질증 진단 여성은 HIV 와 다른 성매개감염 검사를 받는다 [[cdc-sti-2021: BV — Other Management Considerations]]. 클린다마이신 크림은 기름 기반이라 라텍스 콘돔을 약하게 할 수 있다 [[cdc-sti-2021: BV — Treatment]].
- 복잡 칸디다증(1년 3회 이상 재발 · 중증 · 비알비칸스 · 당뇨·면역저하)은 단기 치료가 아니라 긴 치료가 필요하다 — 재발성은 처음 7–14일 국소 또는 플루코나졸 3회(1·4·7일) 뒤 주 1회 6개월 유지 [[cdc-sti-2021: Complicated VVC — Recurrent VVC]].
- 반복되는 트리코모나스는 대부분 재감염이다 — 치료받지 않은 파트너에 다시 노출됐는지 먼저 본다 [[cdc-sti-2021: Trichomoniasis — Recurrent Trichomoniasis]].
- 국내 교과서·KMLE 해설의 권고 문구는 대조하지 않았다(검토 항목).

## 시험 쟁점 — 충돌·맥락·새 근거
- **Z1 새 근거 · 트리코모나스 여성 요법** — 시험 기준: 여성은 메트로니다졸 500 mg 하루 2번 7일 [[cdc-sti-2021: Trichomoniasis — Recommended Regimens]] / 다른 기준: 2 g 단회는 2021 지침에서 남성 권고·남녀 대안(티니다졸)으로 남았다 [[cdc-sti-2021: Trichomoniasis — Recommended Regimens]] / 왜 다른가: 다기관 무작위 시험에서 7일 요법이 1개월 재양성을 절반으로 줄였고, 남성에서는 비교 시험이 없다 [[cdc-sti-2021: Trichomoniasis — Treatment]] / 시험에서는: KMLE 는 국내 교과서·해설과 대조하지 않았다(검토 항목) · USMLE 는 2021 지침 — 여성 7일·남성 단회로 답한다.
- **Z2 새 근거 · 메트로니다졸과 음주** — 시험 기준: 2021 지침은 메트로니다졸·티니다졸 복용 중 금주가 필요 없다고 쓴다(아세트알데하이드 탈수소효소를 억제하지 않는다) [[cdc-sti-2021: BV — Treatment]] / 다른 기준: 예전 경고는 실험실 실험과 개별 증례에 근거했다고 같은 지침이 적는다 [[cdc-sti-2021: BV — Treatment]] / 왜 다른가: 증례의 반응이 알코올 자체나 메트로니다졸 부작용으로도 설명된다 / 시험에서는: KMLE·USMLE 해설이 이 개정을 반영했는지는 대조하지 않았다 — 질염 치료 선택 문항에서는 금주 지시를 정답의 가르는 근거로 삼지 않는다.
