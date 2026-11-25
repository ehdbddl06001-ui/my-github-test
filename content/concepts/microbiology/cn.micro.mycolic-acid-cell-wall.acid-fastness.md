---
id: cn.micro.mycolic-acid-cell-wall.acid-fastness
type: concept
topic: Microbiology
see_also: [Infectious Disease, Pulmonology]
date: 2026-11-25
updated: 2026-11-25
version: 1
outline: micro.bacteria-basics   # 미생물학 책 「세균 총론 — 구조·독소·내성 기전」
layer: basic            # 기초 정리본 — 임상 정리본의 roots 가 가리키는 기전 단위
discipline: microbiology
system: multisystem
textbook_check: unavailable
confidence: medium
review_status: unreviewed
note_form: 2
title: "미콜산 세포벽 — 사슬 길이가 항산성의 세기를 정한다"
objective: "세포벽의 미콜산이 염색약을 붙잡아 산 탈색을 견디는 원리로, 결핵균은 강한 산-알코올에도 붉게 남고 노카르디아는 약산 탈색에서만 남으며 방선균은 남지 않는 이유를 설명하고 염색 결과로 가지 치는 균을 가른다"
objective_kind: 기전
condition: 미콜산 세포벽과 항산성(mycolic acid, acid-fastness)
exams: [usmle, kmle]
summary:
  - "결론: 항산성은 세포벽 미콜산이 만든다 — 결핵균은 강한 산에도, 노카르디아는 약한 산에서만 붉게 남는다."
  - "시험 단서: 가늘고 염주 모양으로 가지 치는 그람 양성 실 + 약산 탈색(modified Kinyoun) 양성 → 노카르디아(weakly acid-fast)."
  - "왜: 노카르디아의 미콜산은 탄소 45–65 개로 짧아, 염색약을 붙잡는 힘이 결핵균보다 약하다."
  - "미콜산이 없는 방선균(Actinomyces)은 같은 가지 친 그람 양성 실이어도 어떤 산 탈색에서도 남지 않는다."
pitfalls:
  - contrast: "약산 항산성 양성 = 결핵균?"
    point: "약산 탈색은 노카르디아도 남긴다 [[harrison-22: 179장 p.1360]]. 결핵균은 가지를 치지 않는 막대균이고 강한 산-알코올에도 남는다 — 가지 치는 실 + 약산에서만 양성이면 노카르디아다."
  - contrast: "가지 치는 그람 양성 실이면 다 노카르디아?"
    point: "방선균도 가지 치는 그람 양성 실이지만 미콜산이 없어 항산 염색에서 남지 않는다. 노카르디아는 호기성이고 약산 탈색에서 남는다 [[harrison-22: 179장 p.1358]] [[harrison-22: 179장 p.1360]]."
  - contrast: "결핵 검체 처리면 노카르디아도 잡힌다?"
    point: "결핵균 배양을 위한 오염 제거 처리는 노카르디아를 죽일 수 있어, 노카르디아를 의심하면 쓰지 않는다 — 검사실에 알려 오래 배양한다 [[harrison-22: 179장 p.1360]]."
tables:
  - id: acid-fast-spectrum
    title: "미콜산과 염색 — 가지 치는 균과 결핵균"
    role: comparison
    span: column
    section: "소견으로 — 염색이 갈리는 이유"
    columns: ["균", "미콜산", "강한 산 탈색", "약산 탈색"]
    rows:
      - ["결핵균(Mycobacterium)", "길다", "남는다(붉음)", "남는다"]
      - ["노카르디아(Nocardia)", "짧다(탄소 45–65)", "빠진다", "남는다(붉음)"]
      - ["방선균(Actinomyces)", "없다", "빠진다", "빠진다"]
    note: "노카르디아 행 [[harrison-22: 179장 p.1358]] [[harrison-22: 179장 p.1360]]. 결핵균 · 방선균 행과 사슬 길이의 비교는 표준 미생물학(전공 교과서 미대조)."
checks:
  - q: "노카르디아가 「약한」 항산성인 이유는?"
    a: "세포벽에 미콜산이 있지만 사슬이 짧아(탄소 45–65) 강한 산-알코올에는 염색약이 빠지고, 약산 탈색에서만 붉게 남는다."
  - q: "가지 치는 그람 양성 실이 약산 항산 염색에서 음성이면 무엇을 생각하는가?"
    a: "미콜산이 없는 방선균 — 혐기성이고 입안 상재균이며, 얼굴·목의 굳은 덩이와 누공을 만든다."
variants:
  - id: v1
    flip: false
    changed: "핵심 변형 — 약산 탈색에서만 붉게 남는 염색 결과의 세포벽 기전을 묻는다"
    context: "장기이식 환자의 공동 폐 결절에서 나온 가지 치는 균"
    stem: "A 54-year-old man who received a kidney transplant 8 months ago has had fever and a productive cough for 3 weeks. Chest CT shows a cavitating nodule in the right upper lobe. Bronchoalveolar lavage fluid shows thin, beaded, branching gram-positive filaments. The filaments retain carbol fuchsin when decolorized with 1% sulfuric acid but lose it with acid-alcohol. Which of the following cell wall features best explains this staining pattern?"
    choices: ["A. A thick peptidoglycan layer without lipid", "B. Mycolic acids with shorter carbon chains than those of mycobacteria", "C. A polysaccharide capsule that excludes the dye", "D. An outer membrane containing lipopolysaccharide", "E. Absence of a cell wall"]
    answer: "B"
    explanation: "Nocardia has mycolic acids in its cell wall, but they are shorter (45–65 carbons) than those of mycobacteria, so the organism holds the dye only when a weak acid is used for decolorization (weakly acid-fast). Mycobacteria resist strong acid-alcohol; Actinomyces has peptidoglycan without mycolic acids and is not acid-fast; a capsule, LPS outer membrane, or absent cell wall does not produce acid-fastness."
    kind: application
figures_none: 세포벽 기전 — 염색 사진은 임상 정리본(cn.id.disseminated-nocardiosis.partial-acid-fast-identification)이 맡는다
sources:
  - id: harrison-22
    org: "McGraw Hill"
    title: "Harrison's Principles of Internal Medicine, 22nd ed."
    kind: textbook
    year: 2025
    citation: "Harrison's Principles of Internal Medicine, 22e. 179장 Nocardiosis p.1358–1362"
    checked_at: 2026-11-25
    checked: "본문 대조(드라이브 22판 장별 문서 H22_179) — p.1358 노카르디아는 그람 양성·약한 항산성·카탈라아제 양성, Mycobacteriales 목으로 세포벽에 미콜산(탄소 45–65)과 트레할로스, 호기성, 식세포 안에서 산화물 중화·포식소체-리소좀 융합 차단 · p.1360 폭 1 μm·최대 50 μm 의 염주 모양 가지 치는 그람 양성 실, 약산 탈색(modified Kinyoun·Ziehl-Neelsen·Fite-Faraco)에서 항산성, 은 염색에 물듦, 결핵균 배양용 오염 제거 처리는 노카르디아를 죽일 수 있음. 결핵균의 강한 산-알코올 저항, 방선균의 미콜산 부재, 사슬 길이와 염색 세기의 관계는 이 장에 없어 표준 미생물학으로 두었다(전공 교과서 미대조)"
    verified: text
---

## 정상 — 미콜산이 세포벽을 기름 막으로 감싼다
결핵균과 노카르디아는 같은 Mycobacteriales 목으로, 펩티도글리칸 바깥에 긴 지방산인 미콜산과 트레할로스가 붙은 세포벽을 가진다 [[harrison-22: 179장 p.1358]]. 이 지질 막은 물에 잘 젖지 않아 그람 염색은 고르게 먹지 않지만, 가열·페놀로 밀어 넣은 카볼 푹신은 한 번 들어가면 쉽게 빠지지 않는다. 산으로 탈색해도 붉은색이 남는 성질이 항산성이다.

## 고장 — 사슬이 짧으면 약한 산에서만 버틴다
- 결핵균의 미콜산은 길어 강한 산-알코올에도 염색약을 붙잡는다.
- 노카르디아의 미콜산은 탄소 45–65 개로 짧아 [[harrison-22: 179장 p.1358]], 강한 산에는 빠지고 약한 산으로 탈색할 때만 남는다 — 「약한 항산성」이다 [[harrison-22: 179장 p.1360]].
- 방선균은 미콜산이 없어 어떤 산 탈색에서도 남지 않는다.

## 소견으로 — 염색이 갈리는 이유
- 노카르디아는 폭 약 1 μm 의 가늘고 염주 모양으로 가지 치는 그람 양성 실이다 — 쉽게 끊겨 알균·짧은 막대처럼 보이기도 한다 [[harrison-22: 179장 p.1360]].
- 같은 모양에서 약산 탈색 양성이면 노카르디아, 음성이면 방선균을 생각한다. 은 염색은 노카르디아도 물들여 둘을 가르지 못한다 [[harrison-22: 179장 p.1360]].

## 임상 판단으로 — 염색이 다음 검사를 정한다
- 면역억제 환자의 공동 폐 결절에서 가지 치는 약산 항산성 실이 나오면 노카르디아증으로 보고 뇌 영상으로 파종을 찾는다 — 임상 판단은 `cn.id.disseminated-nocardiosis.partial-acid-fast-identification`.
- 결핵균 배양용 오염 제거 처리는 노카르디아를 죽이므로, 의심하면 검사실에 알리고 오래 배양한다 [[harrison-22: 179장 p.1360]].

## 시험 쟁점 — 충돌·맥락·새 근거
- 해당 없음(대조: 해리슨 22판 179장 p.1358~1360)
