---
id: cn.allergy.x-linked-agammaglobulinemia.btk-pre-b-arrest
type: concept
topic: Allergy
see_also: [Immunology, Pediatrics]
date: 2026-09-23
updated: 2026-09-23
version: 1
outline: h351            # 기본틀 슬롯(content/outline/subjects.yaml)
confidence: medium
review_status: unreviewed
title: "X연관 무감마글로불린혈증 — B세포 성숙 정지에서 감염 양상과 감별까지"
objective: "BTK 결함이 pre-B 단계에서 B세포 성숙을 멈추는 기전으로 X연관 무감마글로불린혈증의 발병 시기·피막 세균 감염·B세포 부재를 설명하고, 면역글로불린 양상과 T세포·호중구·보체 소견으로 Hyper-IgM·SCID·CGD·말단 보체결핍과 가른다"
objective_kind: 기전
condition: X연관 무감마글로불린혈증(Bruton 병)
exams: [usmle, kmle]
summary:
  - "B세포는 골수에서 pre-B 세포 → 미성숙 B → 성숙 B 로 자라며, pre-B 세포 수용체 신호가 다음 단계로 넘어가는 문이다. BTK 는 그 신호를 전하는 키나아제라, 결함이 있으면 pre-B 에서 B 로 넘어가지 못한다(새는 차단) [[harrison-21: 351장 p.2716]]."
  - "결과는 말초 B세포 거의 부재(<1%)와 모든 클래스의 면역글로불린 저하다. 림프절 배중심·편도 같은 B세포 구역이 자라지 않는다. T세포·호중구·보체는 정상이다."
  - "항체가 없으면 옵소닌화가 안 되어 피막 세균(폐렴구균·헤모필루스·모락셀라)의 부비동·폐 감염이 반복되고, 장 편모충·장바이러스 감염도 생긴다 [[harrison-21: 351장 p.2716]]."
  - "태반을 건넌 모체 IgG 가 몇 달 동안 지켜 주므로 감염은 대개 6개월 무렵부터 시작된다 [[harrison-21: 351장 p.2716]]. X연관이라 남아다."
  - "치료는 평생 면역글로불린 대체(IV 또는 피하) [[harrison-21: 351장 p.2716–2717]]. 확진은 BTK 유전자 또는 단핵구 안 BTK 단백 소실 [[harrison-21: 351장 p.2716]]."
pitfalls:
  - contrast: "XLA vs SCID(ADA 결핍 등) — 둘 다 영아의 반복 감염·림프 조직 빈약"
    point: "SCID 는 T세포 발달이 멈춰 T·B(ADA 결핍은 NK 까지) 모두 없다 [[harrison-21: 351장 p.2713]]. T세포가 없으면 세포 매개 면역이 빠져 주폐포자충·지속 아구창·바이러스 같은 기회감염과 성장부진이 앞에 선다. XLA 는 B세포만 없어 감염이 피막 세균에 몰린다 — 호중구·보체·T세포가 정상이면 결함은 B세포 쪽이다."
    exception: "SCID 는 모체 T세포 생착으로 T세포 수가 가려질 수 있다 — 기회감염이 보이면 T세포 기능·아형을 더 본다 [[harrison-21: 351장 p.2713]]."
    cites: ["harrison-21"]
    covers: ["usmle-2026-0043:C"]
  - contrast: "XLA vs Hyper-IgM(CD40L 결핍)"
    point: "Hyper-IgM 은 B세포 수는 정상이고 클래스 전환만 안 된다 — IgG·IgA 는 낮고 IgM 은 정상이거나 높다 [[harrison-21: 351장 p.2717]]. CD40L 결핍은 T세포 도움도 빠져 주폐포자충 같은 기회감염이 생길 수 있다. XLA 는 IgM 까지 모두 낮고 B세포 자체가 없다."
    cites: ["harrison-21"]
  - contrast: "B세포 결핍 vs 호중구(CGD)·말단 보체결핍"
    point: "CGD 는 면역글로불린·B세포 정상에 카탈라아제 양성균·아스페르길루스의 농양, 말단 보체(C5–C9) 결핍은 CH50 저하에 나이세리아 반복 감염이다. 면역글로불린이 모두 낮으면 이 둘이 먼저가 아니다."
criteria:
  - id: xla-dx
    name: 무감마글로불린혈증 진단 단서
    kind: 진단 기준
    population: "반복 세균 감염 영아·소아"
    statement: "말초 B세포 <1%(정상 대비)와 모든 클래스 면역글로불린 저하. 85% 가 X 염색체의 BTK 변이, 약 10% 가 pre-B 세포 수용체 구성 요소의 상염색체 열성 결함 [[harrison-21: 351장 p.2716]]"
    exceptions: "일부 BTK 변이는 B세포가 낮게 남는 가벼운 저감마글로불린혈증으로 나타난다 — CVID 와 혼동하지 않는다 [[harrison-21: 351장 p.2716]]"
    source: harrison-21
    basis: current
    exams: [usmle, kmle]
  - id: xla-tx
    name: 치료
    kind: 치료 기준
    population: "무감마글로불린혈증"
    statement: "평생 면역글로불린 대체(IV 또는 피하, 환자 선호로 선택). 만성 폐질환이 있으면 흉부 물리요법과 항생제를 더한다 [[harrison-21: 351장 p.2716–2717]]"
    exceptions: "용량·간격·목표 최저 IgG 는 이 정리본에서 대조하지 않았다(검토 항목)"
    source: harrison-21
    basis: current
    exams: [usmle, kmle]
sources:
  - id: harrison-21
    org: "McGraw Hill"
    title: "Harrison's Principles of Internal Medicine, 21st ed. — Chapter 351: Primary Immune Deficiency Diseases"
    kind: textbook
    year: 2022
    citation: "Loscalzo J, Kasper DL, Longo DL, et al (eds). Harrison's Principles of Internal Medicine, 21e. 351장 p.2709–2718"
    checked_at: 2026-09-23
    checked: "본문 대조(드라이브 351장 문서) — p.2713: ADA 결핍이 SCID 의 10–20%, T·B·NK 모두 부재, 모체 T세포가 림프구 감소를 가릴 수 있음 · p.2716: B세포 결핍이 PID 의 60–70%, 폐렴구균·헤모필루스·모락셀라의 부비동·폐 감염, 지아르디아·장바이러스, 모체 Ig 로 6개월 전 감염 드묾, 무감마글로불린혈증 B세포 <1%·85% BTK(X 연관)·pre-B→B 단계의 새는 차단·단핵구 BTK 면역형광 진단, 치료는 Ig 대체 · p.2717: Hyper-IgM 은 클래스 전환 결함으로 IgG·IgA 매우 낮고 IgM 정상/상승, CD40L(X 연관)·CD40 결핍은 B·T 모두 침범, Ig 대체는 평생. 편도·림프절 부재 서술은 이 장에서 확인하지 못했다"
    verified: text
diagram:
  title: "영아 반복 세균 감염 — 결함이 어느 칸에 있나"
  nodes:
    - {id: start, kind: start, text: "생후 6개월 무렵부터 반복되는 피막 세균 감염(중이염·부비동염·폐렴)"}
    - {id: igs, kind: decision, text: "혈청 IgG·IgA·IgM 이 어떤가?"}
    - {id: igdo, kind: info, text: "면역글로불린 정량 · 호중구 수 · CH50 을 함께 잰다"}
    - {id: other, kind: alert, text: "Ig 정상 — 호중구 기능(CGD)·보체(CH50) 쪽을 본다(이 도식 범위 밖)"}
    - {id: higm, kind: end, text: "IgG·IgA 저하 + IgM 정상/상승 — Hyper-IgM(CD40L 등 클래스 전환 결함)"}
    - {id: bcell, kind: decision, text: "말초 CD19+ B세포가 거의 없는가?"}
    - {id: cvid, kind: alert, text: "B세포는 있는데 Ig 저하 — CVID 등(이 도식 범위 밖, 대개 더 늦게 발병)"}
    - {id: tcell, kind: decision, text: "T·NK 세포와 기회감염은? 주폐포자충·지속 아구창·성장부진"}
    - {id: xla, kind: end, text: "T세포 정상·피막 세균만 — XLA(BTK 결함, pre-B 단계 정지) → 평생 면역글로불린 대체"}
    - {id: scid, kind: end, text: "T·B(·NK) 모두 감소 + 기회감염 — SCID(ADA 결핍 등) → 격리·조혈모세포이식"}
  edges:
    - {from: start, to: igs}
    - {from: igs, to: igdo, label: "미측정"}
    - {from: igdo, to: bcell, label: "모두 저하로 나오면"}
    - {from: igdo, to: other, label: "정상으로 나오면"}
    - {from: igs, to: other, label: "모두 정상"}
    - {from: igs, to: higm, label: "IgM 만 정상/상승"}
    - {from: igs, to: bcell, label: "모두 저하"}
    - {from: bcell, to: tcell, label: "거의 없음(<1–2%)"}
    - {from: bcell, to: cvid, label: "정상 수"}
    - {from: tcell, to: xla, label: "T 정상 · 기회감염 없음"}
    - {from: tcell, to: scid, label: "T·NK 감소 · 기회감염"}
diagram_notes:
  - "6개월 전의 면역글로불린 수치는 모체 IgG 가 섞여 해석이 어렵다 — 발병 시기 자체가 단서다."
  - "SCID 에서는 모체 T세포가 남아 T세포 수를 정상처럼 보이게 할 수 있다 — 기회감염이 있으면 T세포 수만 믿지 않는다."
  - "BTK 변이 일부는 B세포가 낮게 남는다 — B세포가 「조금 있다」고 XLA 를 배제하지 않는다."
checks:
  - q: "XLA 에서 감염이 생후 6개월 무렵에야 시작되는 이유는?"
    a: "임신 후반에 태반을 건넌 모체 IgG 가 몇 달 동안 보호하다가 그 무렵 소진되기 때문이다."
  - q: "XLA 와 ADA 결핍 SCID 를 가르는 가장 직접적인 소견은?"
    a: "T세포(와 NK). XLA 는 B세포만 없고 T세포가 정상이라 피막 세균 감염에 몰리고, SCID 는 T세포가 없어 기회감염·성장부진이 생긴다."
  - q: "B세포 수가 정상인데 IgG·IgA 만 낮고 IgM 이 높다. 결함 자리는?"
    a: "클래스 전환(CD40L–CD40 또는 AID) — Hyper-IgM 증후군."
variants:
  - id: v1
    of: usmle-2026-0043
    flip: true
    changed: "T세포 정상·피막 세균 감염만 → CD3+ T세포·NK 세포 모두 감소, 주폐포자충 폐렴·지속 아구창·만성 설사·성장부진, 늑연골 접합부 이상 ⇒ 정답이 BTK 결함(pre-B 정지)에서 ADA 결핍에 의한 림프구 발달 전반 정지로"
    context: "단서를 바꿔 답이 바뀌는 변형 — T세포까지 없는 영아"
    stem: "A 4-month-old boy is evaluated for failure to thrive, chronic diarrhea, and persistent oral thrush since 2 months of age. He is now tachypneic and hypoxemic, and bronchoalveolar lavage shows Pneumocystis jirovecii. Chest x-ray shows diffuse interstitial infiltrates, no thymic shadow, and flaring of the costochondral junctions. Laboratory studies show an absolute lymphocyte count of 300/mm3; CD3+ T cells, CD19+ B cells, and CD56+ NK cells are all markedly reduced. Serum IgG, IgA, and IgM are low. The neutrophil count and total complement activity are normal. Which of the following best describes the mechanism underlying this infant's disease?"
    choices: ["A. Accumulation of toxic purine metabolites that kills lymphocyte precursors", "B. Arrest of B-cell maturation at the pre-B stage from a defective tyrosine kinase", "C. Defective CD40 ligand preventing immunoglobulin class switching", "D. Absent NADPH oxidase activity in phagocytes", "E. Deficiency of the terminal complement components C5 through C9"]
    answer: "A"
    explanation: "The changed clue is the loss of T and NK cells with opportunistic infection (Pneumocystis, thrush), failure to thrive, and skeletal changes at the costochondral junctions. Adenosine deaminase deficiency lets adenosine and deoxyadenosine metabolites accumulate and kill lymphocyte progenitors, removing T, B, and NK cells, and can cause bone dysplasia [[harrison-21: 351장 p.2713]]. A BTK defect removes only B cells, so T-cell-dependent opportunistic infections would not be expected. CD40L deficiency preserves B-cell numbers, and NADPH oxidase or terminal complement defects leave lymphocytes and immunoglobulins normal."
    kind: application
  - id: v2
    of: usmle-2026-0043
    flip: false
    changed: "나이(14개월)·첫 감염(헤모필루스 폐렴 뒤 폐렴구균 균혈증)·내원 경위(외래 면역 평가)·제시 순서를 바꾸고, 남아·6개월 이후 발병·피막 세균·전 클래스 Ig 저하·B세포 부재·T세포 정상은 유지 ⇒ 답은 그대로 BTK 결함"
    context: "겉모습만 바꾸고 답은 같은 변형 — 외래 면역 평가로 온 걸음마기 남아"
    stem: "A 14-month-old boy is referred for immunologic evaluation after his third serious bacterial infection. He was healthy until 7 months of age and has since had Haemophilus influenzae pneumonia and Streptococcus pneumoniae bacteremia, each responding to antibiotics. His maternal uncle died of recurrent pneumonia in childhood. Growth is normal and there has been no thrush or diarrhea. Serum IgG, IgA, and IgM are all markedly decreased. Flow cytometry shows CD19+ B cells below 1% with normal CD3+, CD4+, and CD8+ T-cell counts. Neutrophil count and CH50 are normal. Which of the following best describes the mechanism of this child's immunodeficiency?"
    choices: ["A. Failure of lymphocyte precursors due to purine metabolite toxicity", "B. Absent CD40 ligand on activated helper T cells", "C. Block in B-cell development at the pre-B stage due to a defective kinase", "D. Defective phagocyte respiratory burst", "E. Impaired assembly of the membrane attack complex"]
    answer: "C"
    explanation: "The deciding clues are unchanged: a boy with an affected maternal uncle (X-linked pattern), onset after maternal IgG waned, infections limited to encapsulated bacteria, all immunoglobulin classes low, B cells below 1%, and normal T cells. This is X-linked agammaglobulinemia, in which defective BTK blocks the pre-B to B transition [[harrison-21: 351장 p.2716]]. Normal T cells and no opportunistic infections argue against SCID; low IgM argues against CD40L deficiency; normal neutrophil and complement studies argue against CGD and terminal complement deficiency."
    kind: application
---

## 정의
X연관 무감마글로불린혈증(XLA, Bruton 병)은 X 염색체의 **BTK** 유전자 결함으로 B세포가 성숙하지 못해 항체가 거의 만들어지지 않는 원발 면역결핍이다. 무감마글로불린혈증의 85% 가 BTK 변이다 [[harrison-21: 351장 p.2716]].

## 병태생리
정상에서 B세포는 골수에서 중쇄를 재배열한 pre-B 세포가 대리 경쇄와 함께 **pre-B 세포 수용체**를 표면에 내고, 그 신호를 받아야 경쇄 재배열과 증식을 거쳐 미성숙·성숙 B세포로 넘어간다. BTK 는 이 수용체 신호를 전하는 키나아제다. BTK 가 없으면 pre-B → B 단계에서 (새면서) 멈춘다 [[harrison-21: 351장 p.2716]]. 나머지 약 10% 는 같은 수용체의 다른 부품(μ 중쇄·λ5·Igα/β·BLNK 등) 결함이다.

## 기전에서 소견으로
- 성숙 B세포가 없음 → 말초 CD19+ B세포 <1%, **IgG·IgA·IgM 모두** 저하.
- B세포 구역(배중심·여포)이 자라지 않음 → 편도가 작거나 없고 림프절이 거의 만져지지 않는다(해리슨 351장에서 이 서술은 확인하지 못했다 — 검토 항목).
- 옵소닌 항체가 없음 → 폐렴구균·헤모필루스·모락셀라의 중이염·부비동염·폐렴이 반복되고, 치료하지 않으면 기관지확장증으로 간다. 장 편모충·장바이러스(수막뇌염) 감염도 생긴다 [[harrison-21: 351장 p.2716]].
- 모체 IgG 가 소진되는 생후 6개월 무렵부터 감염 시작 [[harrison-21: 351장 p.2716]].
- T세포·호중구·보체는 정상 → 세포 내 병원체·진균 기회감염은 두드러지지 않는다.

## 감별
- **SCID(ADA 결핍 등)**: T·B·NK 모두 감소, 기회감염·성장부진, ADA 결핍은 뼈 이형성 동반 가능 [[harrison-21: 351장 p.2713]].
- **Hyper-IgM**: B세포 수 정상, IgM 정상/상승, IgG·IgA 매우 낮음 [[harrison-21: 351장 p.2717]].
- **CVID**: B세포는 있으나 항체 생산 저하, 대개 더 늦게 발병.
- **CGD·말단 보체결핍**: 면역글로불린 정상 — 호중구 기능 검사(DHR)·CH50 으로.

## 검사
면역글로불린 정량 → 림프구 아형(CD19·CD3·CD56) → BTK 단백(단핵구 면역형광) 또는 BTK 유전자 [[harrison-21: 351장 p.2716]]. 백신 항체 반응 측정은 더 미묘한 결핍에서 쓴다.

## 치료
- 평생 면역글로불린 대체(IV 또는 피하 — 둘 다 효과적이라 환자 선호로) [[harrison-21: 351장 p.2716–2717]].
- 급성 감염은 적극적으로 항생제. 만성 폐질환이 생겼으면 흉부 물리요법과 항생제 병행.
- 재평가: 감염 빈도, 폐 기능·영상(기관지확장증), 최저 IgG. 생백신은 피한다(이 정리본에서는 원문 미대조 — 검토 항목).

## 권고와 예외
- BTK 변이라도 B세포가 낮게 남는 가벼운 형이 있다 — CVID 로 부르지 않는다 [[harrison-21: 351장 p.2716]].
- 면역글로불린 제제에는 IgA 가 조금 들어 있어, 잔존 항체 생산이 있으면서 IgA 가 완전 결핍인 환자는 항 IgA 항체로 과민반응이 날 수 있다 — XLA 보다는 IgA 결핍·CVID 의 문제다 [[harrison-21: 351장 p.2717]].

## 시험 쟁점 — 충돌·맥락·새 근거
- 해당 없음(대조: 해리슨 351장 p.2713–2717)

## (심화) 「기전」 문항의 보기 읽기
보기 다섯은 모두 면역계의 서로 다른 칸(B세포 발달·클래스 전환·림프구 전체·호중구·보체)에 하나씩 대응한다. 제시된 검사(B세포·Ig 세 종류·호중구·CH50·T세포 소견)가 칸을 하나씩 지우도록 짜여 있다 — 정상 소견이 오답을 지우는 정보다.
