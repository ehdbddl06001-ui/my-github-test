---
id: cn.ortho.axial-spondyloarthritis.sacroiliac-mri
type: concept
topic: Rheumatology
see_also: [Orthopedics]
date: 2026-11-01
updated: 2026-11-01
version: 1
outline: h362
confidence: medium
review_status: unreviewed
note_form: 2
title: "축성 척추관절염 — X선 정상이면 엉치엉덩관절 MRI"
objective: "염증성 허리통증에 척추관절염 소견이 있는데 골반 X선이 정상이면 엉치엉덩관절 MRI로 활동성 염증을 찾는 검사를 고른다"
objective_kind: 검사 선택
condition: 축성 척추관절염(axial spondyloarthritis) · 방사선 비진행형(nonradiographic axSpA)
exams: [kmle, usmle]
summary:
  - "결론: 염증성 허리통증 + 척추관절염 소견 + 골반 X선 정상 → 다음 검사는 엉치엉덩관절 MRI(STIR 골수 부종)."
  - "시험 단서: 45세 전 시작, 새벽 통증·30분 넘는 아침 강직, 운동에 호전, 진통소염제(NSAID) 48시간 반응, 앞포도막염(anterior uveitis)·HLA-B27."
  - "왜: 초기 염증(osteitis)은 MRI에만 보이고, X선 변화(경화·미란)는 수년 뒤에야 생긴다 — 기다리면 진단이 늦는다."
  - "CT 는 구조 변화만 보고 방사선이 많다. 뼈스캔은 민감도·특이도가 낮다. 척추 X선은 만성 허리통증에서 피한다."
  - "MRI 는 민감해 운동선수·출산 뒤·40세 넘은 사람도 골수 부종이 보일 수 있다 — 임상 소견 없이 찍으면 과잉 진단."
pitfalls:
  - contrast: "요추 CT vs 엉치엉덩관절 MRI"
    point: "CT 는 미란·경화·강직 같은 구조 변화를 보지만 활동성 염증(골수 부종)은 보지 못하고 방사선 노출이 크다. X선이 정상인 초기 단계에서 찾을 것은 염증이라 MRI다. 게다가 병변은 요추가 아니라 엉치엉덩관절에 먼저 온다."
    exception: "MRI 를 찍을 수 없을 때 저선량 엉치엉덩관절 CT 가 X선 대안으로 쓰인다(구조 평가용)."
    cites: ["harrison-22: 374장 p.2885", "harrison-22: 374장 p.2888"]
    covers: ["kmle-2026-1658:A"]
  - contrast: "6개월 뒤 X선 재촬영 — 기다리면?"
    point: "방사선 변화가 생기기까지 수년이 걸리고, 진단 지연이 이미 5–14년으로 보고된다. 지금 MRI 로 염증을 볼 수 있다."
    cites: ["harrison-22: 374장 p.2884"]
  - contrast: "뼈스캔 — 온몸의 염증을 찾는다?"
    point: "엉치엉덩관절은 원래 섭취가 많아 뼈스캔으로 염증을 가르기 어렵다(민감도·특이도 낮음). 축성 척추관절염 진단 검사가 아니다."
tables:
  - id: imaging
    section: "가르는 소견 — 검사마다 보는 것"
    title: "엉치엉덩관절을 보는 검사 — 무엇을 보나"
    role: differential
    span: column
    columns: ["검사", "보는 것", "언제"]
    rows:
      - ["골반 X선(AP·Ferguson)", "경화·미란·관절 간격 변화·강직(구조)", "첫 검사 — 양성이면 방사선 진행형(강직척추염) [[harrison-22: 374장 p.2884]]"]
      - ["엉치엉덩관절 MRI", "STIR 골수 부종(활동성 염증) + 지방 변성·미란(구조)", "X선 정상인데 임상 소견이 뚜렷할 때 [[harrison-22: 374장 p.2885]]"]
      - ["저선량 CT", "구조 변화(미란·강직) — 염증은 못 본다", "MRI 불가 시, X선 대안 [[harrison-22: 374장 p.2885]]"]
      - ["뼈스캔", "뼈 대사 증가 — 엉치엉덩관절에서 비특이", "진단에 쓰지 않는다"]
criteria:
  - id: ibp
    name: 염증성 허리통증
    kind: 임상 소견
    population: "3개월 넘는 만성 허리통증"
    statement: "45세 전 서서히 시작, 30분 넘는 아침 강직, 자정 뒤 야간 통증, 운동에 호전·쉬면 악화, 충분한 NSAID 에 48시간 안에 50 % 넘게 호전 [[harrison-22: 374장 p.2883]]"
    exceptions: "모든 항목이 있어야 하는 것은 아니다 [[harrison-22: 374장 p.2883]]"
    source: harrison-22
    basis: current
    exams: [kmle, usmle]
  - id: nraxspa
    name: 방사선 비진행형 진단
    kind: 진단 흐름
    population: "엉치엉덩관절 X선이 확실한 엉치엉덩관절염이 아닌 만성 허리통증"
    statement: "척추관절염 소견이 있으면 엉치엉덩관절 MRI — 양성이면 방사선 비진행형 축성 척추관절염. MRI 음성이면 임상 소견이 뚜렷하고 HLA-B27 양성일 때만 진단을 유지한다 [[harrison-22: 374장 p.2884]]"
    exceptions: "MRI 소견은 기계적 부하로도 생긴다 — 임상 소견과 함께 판단 [[harrison-22: 374장 p.2885]]"
    source: harrison-22
    basis: current
    exams: [kmle, usmle]
sources:
  - id: harrison-22
    org: "McGraw Hill"
    title: "Harrison's Principles of Internal Medicine, 22nd ed. — Chapter 374: Spondyloarthritis"
    kind: textbook
    year: 2025
    citation: "Harrison's Principles of Internal Medicine, 22e. 374장 p.2883–2885, 2887–2888"
    checked_at: 2026-11-01
    checked: "드라이브 22판 장별 문서 H22_374 본문 대조 — Table 374-4 염증성 vs 기계적 허리통증(p.2883) · 진단 지연 5–14년, Fig. 374-2 진단 흐름(X선 → 척추관절염 소견 → 엉치엉덩관절 MRI → HLA-B27), CRP·ESR 민감도 30–40 %, 척추 X선은 피함(p.2884) · 저선량 CT 는 X선 대안, MRI 초기 염증(osteitis)이 유일한 이상일 수 있음, STIR 골수 부종, 기계적 부하·40세 이후 과잉 진단 주의(p.2885) · 뼈스캔은 PsA 진단에 민감·특이하지 않음, CT 방사선 부담(p.2888, PsA 절) · Table 374-5 최대 용량 NSAID 4주 뒤 활동성이면 TNFi·IL-17i, 전통 DMARD 는 축성 병변에 무효(p.2887)"
    verified: text
diagram:
  title: "만성 허리통증 — 엉치엉덩관절 MRI 까지"
  nodes:
    - {id: start, kind: start, text: "3개월 넘는 허리·엉덩이 통증, 45세 전 시작"}
    - {id: ibp, kind: decision, text: "염증성 양상(아침 강직·운동에 호전)?"}
    - {id: ask, kind: info, text: "강직 시간·야간 통증·NSAID 반응을 묻는다"}
    - {id: mech, kind: end, text: "기계적 허리통증 쪽으로 평가"}
    - {id: xray, kind: decision, text: "골반 X선에 확실한 엉치엉덩관절염?"}
    - {id: ras, kind: end, text: "방사선 진행형(강직척추염)"}
    - {id: mri, kind: decision, text: "엉치엉덩관절 MRI 골수 부종?"}
    - {id: nras, kind: end, text: "방사선 비진행형 축성 척추관절염"}
    - {id: b27, kind: alert, text: "임상 소견 뚜렷 + HLA-B27 양성일 때만 진단"}
  edges:
    - {from: start, to: ibp}
    - {from: ibp, to: xray, label: "예"}
    - {from: ibp, to: mech, label: "아니오"}
    - {from: ibp, to: ask, label: "정보 없음"}
    - {from: ask, to: xray, label: "염증성"}
    - {from: ask, to: mech, label: "기계적"}
    - {from: xray, to: ras, label: "있음"}
    - {from: xray, to: mri, label: "정상"}
    - {from: mri, to: nras, label: "있음"}
    - {from: mri, to: b27, label: "없음"}
diagram_notes:
  - "척추관절염 소견 — 염증성 허리통증, 말초 관절염, 앞포도막염, 손발가락염, 부착부염, 건선, 염증성 장질환, 가족력, NSAID 반응, CRP 상승 [[harrison-22: 374장 p.2884]]."
  - "CRP·ESR 은 활동성 환자의 30–40 % 에서만 올라 정상이어도 배제하지 못한다 [[harrison-22: 374장 p.2884]]."
  - "MRI 는 기계적 부하(운동선수·출산 뒤)·40세 이후에도 골수 부종을 보일 수 있다 — 임상 소견 없이 찍지 않는다."
checks:
  - q: "염증성 허리통증·HLA-B27 양성인데 골반 X선이 정상이다. 다음 검사는?"
    a: "엉치엉덩관절 MRI(STIR) — 초기 활동성 염증(골수 부종)은 MRI에만 보인다."
  - q: "CT 가 이 단계에서 답이 아닌 이유는?"
    a: "구조 변화만 보고 염증을 못 보며 방사선이 많다. MRI 를 못 찍을 때의 X선 대안이다."
variants:
  - id: v1
    of: kmle-2026-1658
    flip: true
    changed: "골반 X선 정상 → 양쪽 엉치엉덩관절의 경화·미란(확실한 엉치엉덩관절염), 물음을 다음 처치로 ⇒ 진단이 X선으로 끝나 MRI가 필요 없고, 정답이 엉치엉덩관절 MRI에서 최대 용량 진통소염제로"
    context: "같은 염증성 허리통증, X선이 이미 엉치엉덩관절염을 보여 주는 변형"
    stem: "27세 남자가 2년 전부터 허리와 엉덩이가 아파 왔다. 새벽에 아파서 깨고 아침에 1시간 넘게 허리가 뻣뻣하며 움직이면 나아진다. 진찰에서 허리 앞굽힘이 제한되고 양쪽 엉치엉덩관절을 누르면 아프다. 다리 근력과 감각은 정상이다. CRP 2.1 mg/dL, HLA-B27 양성이다. 골반 X선에서 양쪽 엉치엉덩관절 가장자리에 경화와 미란이 있다. 지금까지 약을 먹은 적은 없다. 가장 적절한 처치는?"
    choices: ["A. 엉치엉덩관절 MRI 촬영 후 치료 결정", "B. 최대 용량 진통소염제 지속 투여와 운동 치료", "C. 경구 글루코코르티코이드 장기 투여", "D. 메토트렉세이트 단독 투여", "E. 요추 유합술"]
    answer: "B"
    explanation: "원래 문항과 달리 X선에서 확실한 엉치엉덩관절염(경화·미란)이 보여 방사선 진행형 축성 척추관절염(강직척추염)으로 진단이 끝난다 — MRI 는 X선이 정상일 때 염증을 찾는 검사라 여기서는 필요 없다. 첫 치료는 운동·물리치료와 최대 용량 진통소염제이고, 4주 뒤에도 활동성이면 TNF 억제제나 IL-17 억제제로 올린다. 메토트렉세이트 같은 전통 항류마티스제는 축성 병변에 효과가 없다."
    kind: application
  - id: v2
    of: kmle-2026-1658
    flip: false
    changed: "26세 남자·앞포도막염 → 31세 여자·발뒤꿈치 부착부염과 궤양성 대장염, 검사 순서와 표현을 바꿈 ⇒ 염증성 허리통증 + 척추관절염 소견 + 골반 X선 정상이라는 결정 단서는 같아 답은 그대로 엉치엉덩관절 MRI"
    context: "겉모습만 바꾼 변형 — 여자, 다른 척추관절염 소견"
    stem: "31세 여자가 8개월째 엉덩이 깊은 곳과 허리가 아파 왔다. 밤 2시쯤 아파서 깨고 아침 강직이 40분 가며, 오래 앉아 있으면 심해지고 걸으면 나아진다. 3년 전 궤양성 대장염을 진단받았고 왼쪽 발뒤꿈치 아킬레스힘줄 부착부가 붓고 아팠던 적이 있다. 진찰에서 양쪽 엉치엉덩관절 부위에 압통이 있고 신경학적 이상은 없다. HLA-B27 은 양성이고 CRP 는 정상이다. 골반 X선에서 엉치엉덩관절은 정상이다. 다음으로 가장 적절한 검사는?"
    choices: ["A. 1년 뒤 골반 X선 재촬영", "B. 엉치엉덩관절 MRI", "C. 요추 CT", "D. 전신 뼈스캔", "E. 류마티스인자 검사"]
    answer: "B"
    explanation: "나이·성별·동반 소견이 바뀌었지만 결정 단서는 같다 — 45세 전 시작한 염증성 허리통증(야간 통증·아침 강직·움직이면 호전)에 척추관절염 소견(염증성 장질환·부착부염·HLA-B27)이 있고 X선은 정상이다. 초기 염증은 MRI 에만 보이므로 엉치엉덩관절 MRI 를 찍는다. CRP 정상은 활동성 환자의 60–70 % 에서 볼 수 있어 배제 근거가 아니고, 여자라는 점은 진단을 늦추는 흔한 이유일 뿐이다."
    kind: application
figures_wanted:
- source: PMC_OA
  shows: 엉치엉덩관절 MRI STIR 의 골수 부종 — 축성 척추관절염의 활동성 염증
  at: 가르는 소견 — 검사마다 보는 것
  query: '"sacroiliitis" AND "bone marrow edema" AND "STIR" AND "spondyloarthritis"'
  caption_terms:
  - bone marrow
  - STIR
  modality: MR
---

## 판단 — 왜 X선이 정상이면 MRI 인가
- 엉치엉덩관절 X선의 경화·미란은 **구조 손상**이 쌓인 뒤에야 보인다 — 진단 지연이 5–14년으로 보고된다 [[harrison-22: 374장 p.2884]].
- 초기에는 MRI 의 활동성 염증(osteitis)이 **유일한 이상**일 수 있다 [[harrison-22: 374장 p.2885]]. 그래서 X선이 정상이고 임상 소견이 뚜렷하면 다음은 MRI 다.
- 기다리는 것(재촬영)은 진단·치료만 늦추고, CT·뼈스캔은 지금 찾으려는 염증을 보지 못한다.

## 기전 — 부착부 염증에서 골수 부종, 그리고 뼈로
척추관절염은 힘줄·인대가 뼈에 붙는 자리(부착부)와 엉치엉덩관절의 면역 염증으로 시작한다. 염증이 관절 밑 뼈속질로 번지면 물이 늘어 MRI STIR 영상에서 밝은 골수 부종으로 보인다. 시간이 지나면 염증 자리가 지방 변성으로 바뀌고, 다시 새 뼈가 생겨 미란·경화·강직이 된다 [[harrison-22: 374장 p.2885]]. X선은 이 마지막 구조 단계만 잡아내므로 초기에 정상이다.

## 가르는 소견 — 검사마다 보는 것
- 첫 검사는 골반 AP(또는 Ferguson) 한 장이고, 척추 X선은 만성 허리통증에서 피한다 [[harrison-22: 374장 p.2884]].
- STIR 골수 부종이 활동성 염증, T1 의 지방 변성·미란이 구조 변화다. 여러 종류의 병변이 함께 있을수록 확신이 커진다 [[harrison-22: 374장 p.2885]].
- **음성·양성의 한계**: CRP·ESR 은 활동성 환자의 30–40 % 에서만 오른다 [[harrison-22: 374장 p.2884]]. MRI 골수 부종은 운동선수·출산 뒤·40세 넘은 사람에게도 보일 수 있다 [[harrison-22: 374장 p.2885]].

## 권고와 예외
- MRI 가 음성이어도 임상 소견이 뚜렷하고 HLA-B27 이 양성이면 방사선 비진행형으로 진단할 수 있다 [[harrison-22: 374장 p.2884]].
- MRI 를 찍을 수 없으면 저선량 엉치엉덩관절 CT 가 X선의 대안이다 — 염증이 아니라 구조를 본다 [[harrison-22: 374장 p.2885]].
- 진단 뒤 첫 치료(운동·최대 용량 NSAID → 생물학제제)는 이 정리본의 목표가 아니다.

## 시험 쟁점 — 충돌·맥락·새 근거
- 해당 없음(대조: 해리슨 22판 374장 p.2883–2885)
