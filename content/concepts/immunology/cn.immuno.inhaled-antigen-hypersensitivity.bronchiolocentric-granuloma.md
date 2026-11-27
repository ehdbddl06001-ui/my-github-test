---
id: cn.immuno.inhaled-antigen-hypersensitivity.bronchiolocentric-granuloma
type: concept
topic: Immunology
see_also: [Pulmonology, Occupational Medicine]
date: 2026-11-27
updated: 2026-11-27
version: 1
outline: immuno.hypersensitivity   # 면역학 책 「과민반응」
layer: basic            # 기초 정리본 — 임상 정리본의 roots 가 가리키는 기전 단위
discipline: immunology
system: respiratory
objective_kind: 기전
textbook_check: unavailable
confidence: medium
review_status: unreviewed
note_form: 2
title: "흡입 항원 과민반응 — 작은 기도에 림프구 · 느슨한 육아종"
objective: "말단 기도까지 내려앉는 작은 항원 입자가 감작된 사람에서 Th1 · Th17 반응과 특이 IgG · 선천 면역을 일으켜 세기관지 중심의 림프구 침윤과 느슨한 비건락 육아종을 만드는 과정을 설명하고, 이것이 세척액 림프구 증가 · 공기 걸림 · 노출 4~8시간 뒤 증상으로 나타나는 이유와 사르코이드증 · 유기 분진 독성 증후군과의 차이를 가른다"
condition: 흡입 항원 과민반응 — 과민성 폐렴(hypersensitivity pneumonitis, extrinsic allergic alveolitis)
exams: [usmle, kmle]
summary:
  - "결론: 과민성 폐렴은 말단 기도에 내려앉은 흡입 항원에 대한 Th1 · Th17 면역 반응 — 세기관지 둘레의 림프구와 느슨한 육아종이 병변이다."
  - "시험 단서: 새 · 곰팡이 건초 노출 + 노출 4~8시간 뒤 열 · 기침 + 세척액 림프구 증가 — BAL lymphocytosis, loose granulomas."
  - "왜: 항원이 작은 기도 · 폐포에 닿아 감작된 림프구가 모이므로, 작은 기도가 좁아져 공기가 갇히고 세척액에 림프구가 늘어난다."
  - "특이 IgG 는 노출만으로도 생긴다 — 무증상 농부 · 비둘기 사육자에게도 있어 그것만으로 진단하지 않는다."
pitfalls:
  - contrast: "비건락 육아종이면 사르코이드증?"
    point: "과민성 폐렴의 육아종은 작은 기도 근처에 느슨하고 경계가 흐리다. 사르코이드증의 비건락 육아종은 잘 짜여 있고, 폐문 림프절 비대와 폐 밖 장기 침범이 흔하다 [[harrison-22: 299장 p.2230]]."
  - contrast: "특이 IgG(침강소) 양성 = 과민성 폐렴?"
    point: "고노출 무증상자도 특이 IgG 를 가져 면역 반응만으로는 진단이 아니다. 여러 항원 패널은 실제 원인 항원의 일부만 담아 거짓 음성도 흔하다 [[harrison-22: 299장 p.2229]]."
  - contrast: "곡물 · 곰팡이 분진 뒤 열이면 모두 과민성 폐렴?"
    point: "유기 분진 독성 증후군도 같은 분진으로 생기지만 미리 감작될 필요가 없고 특이 IgG 도 없다 — 면역 감작이 없는 독성 반응이다 [[harrison-22: 299장 p.2230]]."
tables:
  - id: granulomas
    title: "비건락 육아종 — 과민성 폐렴과 사르코이드증"
    role: comparison
    span: column
    section: "소견으로 — 림프구 · 공기 걸림 · 육아종"
    columns: ["", "과민성 폐렴", "사르코이드증"]
    rows:
      - ["원인", "흡입 항원에 대한 감작 [[harrison-22: 299장 p.2229]]", "원인 항원 불명"]
      - ["육아종", "느슨 · 경계 흐림, 작은 기도 근처 [[harrison-22: 299장 p.2230]]", "잘 짜임 [[harrison-22: 299장 p.2230]]"]
      - ["폐문 림프절 · 폐 밖", "드묾", "폐문 림프절 비대 · 다른 장기 침범 [[harrison-22: 299장 p.2230]]"]
checks:
  - q: "과민성 폐렴에서 날숨 CT 에 공기 걸림이 보이는 이유는?"
    a: "항원이 말단 기도에 내려앉아 세기관지 중심 염증이 작은 기도를 좁히기 때문이다."
  - q: "특이 IgG 양성만으로 과민성 폐렴을 진단하지 않는 이유는?"
    a: "고노출 무증상자(농부 · 비둘기 사육자)도 특이 IgG 를 가지며, 노출의 증거일 뿐 병의 증거가 아니기 때문이다."
variants:
  - id: v1
    flip: false
    changed: "핵심 변형 — 조직 소견에서 면역 기전(세기관지 중심 림프구 · 느슨한 육아종)을 묻는다"
    context: "곰팡이 건초를 다루는 농부의 반복 발열 · 기침"
    stem: "A 49-year-old dairy farmer has had recurrent episodes of fever, chills, cough, and dyspnea that begin several hours after he forks moldy hay and subside over 1–2 days. He has never smoked. Expiratory high-resolution CT shows centrilobular nodules, ground-glass opacities, and patchy air trapping. Bronchoalveolar lavage shows 55% lymphocytes. A transbronchial cryobiopsy is performed. Which of the following findings is most likely?"
    choices: ["A. Well-formed noncaseating granulomas along lymphatics with hilar node involvement", "B. Loose, poorly formed noncaseating granulomas near small airways with lymphocytic infiltrates", "C. Caseating granulomas containing acid-fast bacilli", "D. Eosinophil-filled alveoli with Charcot-Leyden crystals", "E. Temporally heterogeneous fibroblastic foci with basal honeycombing"]
    answer: "B"
    explanation: "Repeated inhalation of small antigen particles (thermophilic actinomycetes in moldy hay) drives a TH1/TH17 response in sensitized individuals, producing bronchiolocentric lymphocytic inflammation with loose, poorly defined noncaseating granulomas; small-airway inflammation explains the air trapping and BAL lymphocytosis. Well-formed granulomas with hilar adenopathy suggest sarcoidosis; fibroblastic foci with basal honeycombing suggest idiopathic pulmonary fibrosis."
    kind: application
figures_none: 면역 기전 — 영상 · 조직 사진은 임상 정리본(cn.pulm.hypersensitivity-pneumonitis.exposure-bal-diagnosis)의 몫이다
sources:
  - id: harrison-22
    org: "McGraw Hill"
    title: "Harrison's Principles of Internal Medicine, 22nd ed."
    kind: textbook
    year: 2025
    citation: "Harrison's Principles of Internal Medicine, 22e. 299장 Hypersensitivity Pneumonitis and Pulmonary Infiltrates with Eosinophilia p.2228–2230"
    checked_at: 2026-11-27
    checked: "본문 대조(드라이브 22판 장별 문서 H22_299) — p.2229 원인 항원(진균 · 세균 · 마이코박테리아 · 새 · 화학물질), 농부 폐(곰팡이 건초의 호열성 방선균 · 아스페르길루스) · 조류 사육자 폐(깃털 · 배설물 · 혈청 단백), 병태생리: 말단 기도 · 폐포에 내려앉는 작은 흡입 항원에 대한 면역 매개 질환, 조절 안 된 TH1 · TH17, 특이 IgG(적응 면역)와 TLR · MyD88 → 호중구(선천 면역), 만성형은 섬유세포 · MUC5B 다형성이 IPF 와 겹침, HRCT 간유리 · 소엽 중심 결절 · 날숨 공기 걸림(작은 기도 침범), 특이 IgG 는 무증상 고노출자에게도 · 패널 거짓 음성 · p.2230 세척액 림프구 증가(비특이) · CD4/CD8 < 1 흔함, 작은 기도 근처의 느슨하고 경계 흐린 비건락 육아종과 림프구 위주 침윤 · 세기관지염(사르코이드증은 잘 짜인 육아종 · 폐문 림프절 · 폐 밖 침범), 예측 인자에 노출 4~8시간 뒤 증상, 유기 분진 독성 증후군은 감작 불필요 · 특이 IgG 없음. 과민반응 형(Ⅲ · Ⅳ형) 분류 용어는 이 장에 없어 쓰지 않았다(전공 교과서 미대조)"
    verified: text
---

## 정상 — 작은 입자는 말단 기도까지 내려간다
흡입한 입자 가운데 충분히 작은 것은 큰 기도에서 걸러지지 않고 말단 기도와 폐포에 내려앉는다. 과민성 폐렴의 원인 항원 — 곰팡이 건초의 호열성 방선균 · 아스페르길루스, 새의 깃털 · 배설물 · 혈청 단백, 이소시안산 같은 화학물질, 온수 욕조의 마이코박테리아 — 이 바로 이런 입자다 [[harrison-22: 299장 p.2229]].

## 고장 — 감작된 사람의 Th1 · Th17 반응
- 과민성 폐렴은 흡입 항원에 대한 면역 매개 질환이고, 조절되지 않은 Th1 · Th17 반응이 중심이다 [[harrison-22: 299장 p.2229]].
- 특이 IgG(침강소)는 적응 면역이 관여함을 보여 주고, 톨유사수용체 · MyD88 신호가 호중구를 부르는 선천 면역도 함께 작동한다 [[harrison-22: 299장 p.2229]].
- 노출이 오래 이어지면 섬유세포가 염증 · 섬유화에 더해지고, 만성형은 특발성 폐섬유증과 유전적 바탕(MUC5B)을 일부 나눈다 [[harrison-22: 299장 p.2229]].

## 소견으로 — 림프구 · 공기 걸림 · 육아종
- 세기관지 중심 염증이 작은 기도를 좁혀 날숨 CT 에 공기 걸림이, 폐포 침윤이 간유리 음영 · 소엽 중심 결절로 보인다 [[harrison-22: 299장 p.2229]].
- 모인 림프구는 세척액 림프구 증가로 나타나고, 대개 CD4/CD8 비가 1 보다 낮다 — 둘 다 특이하지는 않다 [[harrison-22: 299장 p.2230]].
- 조직은 작은 기도 근처의 느슨하고 경계가 흐린 비건락 육아종과 림프구 위주의 침윤, 세기관지염이다 [[harrison-22: 299장 p.2230]].
- 감작된 면역 반응이라 증상은 노출 4~8시간 뒤에 오고, 노출을 끊으면 비섬유형은 대개 가라앉는다 [[harrison-22: 299장 p.2229]] [[harrison-22: 299장 p.2230]].

## 임상 판단으로 — 노출이 먼저, 면역 검사는 보조
- 진단의 첫 축은 증상과 맞물린 노출력이고, 특이 IgG · 세척액 · 조직은 면역 반응을 보여 주는 보조 근거다 — 임상 판단은 `cn.pulm.hypersensitivity-pneumonitis.exposure-bal-diagnosis`.
- 치료의 축이 항원 회피인 것도 같은 이유다 — 반응을 이끄는 항원을 없앤다 [[harrison-22: 299장 p.2230]].

## 시험 쟁점 — 충돌·맥락·새 근거
- 해당 없음(대조: 해리슨 22판 299장 p.2229~2230)
