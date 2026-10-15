---
id: cn.uro.testis-histology.leydig-lh-target
type: concept
topic: Urology
see_also: [Endocrinology, Pathology]
date: 2026-09-23
updated: 2026-10-15
version: 3
outline: uro.male-repro        # 비뇨의학과 「남성 생식계와 고환 질환」 = 해리슨 21판 391장
confidence: medium
review_status: unreviewed
note_form: 2            # 판형 2(2026-09-25)
title: "고환 조직 — 관 사이 간질세포는 LH, 관 안 세르톨리는 FSH"
objective: "고환 조직 사진에서 양성 세포를 위치로 간질세포·세르톨리세포로 가르고, 그 세포가 표적인 호르몬(LH·FSH)을 분비 산물과 구분해 연결한다"
objective_kind: 기전
condition: 고환 간질세포·세르톨리세포와 성선자극호르몬 축
exams: [usmle, kmle]
summary:
  - "결론: 세정관 사이 간질의 양성 세포 = 간질(Leydig)세포 = LH 의 표적, 관 안 기저막 위 = 세르톨리세포 = FSH 의 표적."
  - "시험 단서: 고환 면역염색에서 관 안은 음성, 관 사이 다각형 세포 무리만 양성(Leydig cell) + 「주된 표적 호르몬은?」."
  - "왜: LH 는 주로 간질세포에, FSH 는 세르톨리세포에 작용한다 — 위치가 세포를, 세포가 표적 호르몬을 정한다."
  - "AMH(MIS)·인히빈 B 는 세르톨리세포가 「분비하는」 호르몬이지 간질세포의 「표적」 호르몬이 아니다."
  - "테스토스테론↓ + LH↑ = 고환(일차), LH↓·부적절하게 정상 = 시상하부·뇌하수체(이차). 세정관만 다치면 FSH 만 오른다."
criteria:
  - id: lh-level-primary-secondary
    name: 테스토스테론 저하에서 LH 로 병변 위치 가르기
    kind: 진단 기준
    population: "혈청 테스토스테론이 낮은 남성"
    statement: "LH 가 높으면 고환 수준의 일차 결함, LH 가 낮거나 「부적절하게 정상」이면 시상하부·뇌하수체 수준의 이차 결함이다 [[harrison-21: 391장 p.3010]]"
    exceptions: "LH 는 1–3시간마다 박동성으로 분비돼 값이 출렁인다 — 여러 번 채혈해 합치거나 반복 측정한다 [[harrison-21: 391장 p.3010]]"
    source: harrison-21
    locator: "391장 p.3010 Gonadotropin and inhibin measurements"
    basis: current
    exams: [usmle, kmle]
sources:
  - id: harrison-21
    org: "McGraw Hill"
    title: "Harrison's Principles of Internal Medicine, 21st ed. — Chapter 391: Disorders of the Testes and Male Reproductive System"
    kind: textbook
    year: 2022
    citation: "Loscalzo J, Kasper DL, Longo DL, et al (eds). Harrison's Principles of Internal Medicine, 21e. 391장 p.3006–3026"
    checked_at: 2026-09-23
    checked: "드라이브 391장 문서 대조 — p.3006(LH·FSH 통제 아래 간질세포 테스토스테론·세르톨리세포의 생식세포 지지, 간질세포 INSL3·세르톨리세포 MIS, 태아 간질세포), p.3007(LH 는 주로 간질세포, FSH 는 세르톨리세포·인히빈 B 의 FSH 선택 억제, LH 수용체 G 단백·cAMP·StAR, 콜레스테롤 미토콘드리아 내막 수송이 속도제한, CYP11A1·CYP17A1), p.3009(FSH 수용체 변이·세정관 손상 시 FSH 선택 상승·고환 내 고농도 테스토스테론), p.3010(LH 로 일차·이차 구분, 박동 분비), p.3012(고프롤락틴혈증 = 성선자극호르몬이 낮은 시상하부·뇌하수체 원인), p.3020(고환절제 = 일차 고환 부전·LH 상승)"
    verified: text
  - id: hpa-insl3
    org: "Human Protein Atlas"
    title: "INSL3 — tissue expression, Testis"
    kind: other
    year: 2026
    url: "https://www.proteinatlas.org/ENSG00000248099-INSL3/tissue/Testis"
    checked_at: 2026-09-23
    checked: "문항 영상의 출처 페이지. 이 컨테이너에서 접속이 막혀 주석(간질세포 강양성·세정관 세포 음성)을 직접 대조하지 못했다 — 문항 해설의 인용만 확인"
    verified: citation
tables:
  - id: testis-hormone-targets
    title: "고환의 두 세포 — 어디에 있고, 무엇의 표적이며, 무엇을 내보내나"
    role: comparison
    span: full
    section: "판단 — 위치가 세포를, 세포가 호르몬을 정한다"
    columns: ["세포", "위치(사진에서)", "표적이 되는 호르몬", "세포가 만드는 것", "기능이 떨어지면"]
    rows:
      - ["간질(Leydig)세포", "세정관 **사이** 결합조직에 무리 지음", "LH(수용체: G 단백 결합, cAMP) [[harrison-21: 391장 p.3007]]", "테스토스테론, INSL3 [[harrison-21: 391장 p.3006]]", "테스토스테론↓ · LH↑(일차 성선기능저하증) [[harrison-21: 391장 p.3010]]"]
      - ["세르톨리세포", "세정관 **안** 기저막 위, 생식세포를 둘러쌈", "FSH (+ 고환 내 고농도 테스토스테론) [[harrison-21: 391장 p.3007]]", "인히빈 B, AMH(MIS) [[harrison-21: 391장 p.3006]]", "인히빈 B↓ → FSH 선택 상승 [[harrison-21: 391장 p.3009]]"]
      - ["생식세포", "세정관 안, 기저막에서 내강 쪽으로 성숙", "직접 표적 아님 — 세르톨리세포·테스토스테론을 거쳐 조절", "정자", "정자형성 저하(FSH·고환 내 테스토스테론 모두 필요) [[harrison-21: 391장 p.3009]]"]
    note: "사진 문항의 순서: ① 위치로 세포를 정한다 ② 그 세포의 수용체(표적 호르몬)를 붙인다 ③ 질문이 표적을 묻는지 분비 산물을 묻는지 확인한다."
  - id: gonadotropin-pattern
    title: "호르몬 양상으로 병변 위치 읽기"
    role: differential
    span: column
    section: "가르는 소견 — 사진의 위치와 호르몬 양상"
    columns: ["상황", "테스토스테론", "LH", "FSH"]
    rows:
      - ["간질세포·고환 전체 부전(고환절제·클라인펠터)", "↓", "↑ [[harrison-21: 391장 p.3020]]", "↑"]
      - ["세정관만 손상(방사선 등)", "대개 유지", "정상", "선택적 ↑ [[harrison-21: 391장 p.3009]]"]
      - ["시상하부·뇌하수체(고프롤락틴혈증 포함)", "↓", "↓ 또는 부적절하게 정상 [[harrison-21: 391장 p.3012]]", "↓ 또는 정상"]
    note: "LH 는 간질세포 쪽, FSH 는 세르톨리세포 쪽의 되먹임을 읽는 창이다 [[harrison-21: 391장 p.3007]]."
pitfalls:
  - contrast: "LH vs FSH — 「둘 다 성선자극호르몬이니 고환 세포면 아무거나」"
    point: "두 호르몬은 같은 뇌하수체 세포에서 나오지만 고환 안의 표적이 다르다. LH 는 세정관 사이의 간질세포, FSH 는 세정관 안의 세르톨리세포다 [[harrison-21: 391장 p.3007]]. 사진에서 관 안이 음성이고 관 사이 무리만 양성이면 FSH 의 표적은 염색되지 않은 것이다 — 위치가 호르몬을 정한다."
    exception: "양성 세포가 세정관 안 기저막 위에 한 줄로 서서 생식세포를 둘러싸면 세르톨리세포이고, 그때는 FSH 가 답이다."
    covers: ["imaging-2026-0004:D"]
  - contrast: "표적 호르몬 vs 분비 호르몬 — AMH·인히빈 B"
    point: "AMH(MIS)와 인히빈 B 는 세르톨리세포가 만들어 내보내는 호르몬이다. AMH 는 태아 뮐러관을 퇴행시키고, 인히빈 B 는 뇌하수체 FSH 를 선택적으로 누른다 [[harrison-21: 391장 p.3006]] [[harrison-21: 391장 p.3007]]. 어느 쪽도 간질세포를 표적으로 삼지 않는다 — 「이 세포에 작용하는 것」과 「이 세포가 내는 것」을 섞지 않는다."
    exception: "질문이 「이 세포가 분비하는 것」을 묻고 염색 세포가 세르톨리세포라면 AMH·인히빈 B 가 답이 된다."
    covers: ["imaging-2026-0004:A", "imaging-2026-0004:E"]
  - contrast: "프롤락틴 — 테스토스테론을 낮출 수는 있지만 간질세포의 영양호르몬은 아니다"
    point: "고프롤락틴혈증은 성선자극호르몬을 낮추는 시상하부·뇌하수체 원인으로 분류된다 [[harrison-21: 391장 p.3012]] — 테스토스테론 저하는 GnRH·LH 를 거친 간접 효과다. 간질세포를 직접 움직이는 호르몬은 LH 다 [[harrison-21: 391장 p.3007]]."
    covers: ["imaging-2026-0004:B"]
diagram:
  title: "고환 조직 사진 — 염색된 세포와 호르몬 연결"
  nodes:
    - {id: start, kind: start, text: "고환 조직 사진에서 양성(갈색) 세포를 본다"}
    - {id: loc, kind: decision, text: "양성 세포는 어디에 있나?"}
    - {id: info, kind: info, text: "세정관 기저막·생식세포층을 먼저 찾아 위치를 다시 본다"}
    - {id: leydig, kind: step, text: "세정관 사이 간질의 무리 → 간질(Leydig)세포"}
    - {id: sertoli, kind: step, text: "세정관 안 기저막 위 → 세르톨리세포"}
    - {id: askl, kind: decision, text: "질문이 묻는 것은?"}
    - {id: asks, kind: decision, text: "질문이 묻는 것은?"}
    - {id: lh, kind: end, text: "표적 = LH(수용체 → cAMP → StAR)"}
    - {id: testo, kind: end, text: "분비 = 테스토스테론 · INSL3"}
    - {id: fsh, kind: end, text: "표적 = FSH (정자형성 지원)"}
    - {id: inh, kind: end, text: "분비 = 인히빈 B · AMH(MIS)"}
  edges:
    - {from: start, to: loc}
    - {from: loc, to: leydig, label: "관 사이(간질)"}
    - {from: loc, to: sertoli, label: "관 안(기저막 위)"}
    - {from: loc, to: info, label: "판단 어려움"}
    - {from: info, to: leydig, label: "관 사이로 확인"}
    - {from: info, to: sertoli, label: "관 안으로 확인"}
    - {from: leydig, to: askl}
    - {from: sertoli, to: asks}
    - {from: askl, to: lh, label: "표적 호르몬"}
    - {from: askl, to: testo, label: "분비 산물"}
    - {from: asks, to: fsh, label: "표적 호르몬"}
    - {from: asks, to: inh, label: "분비 산물"}
diagram_notes:
  - "위치가 애매하면 세정관 윤곽(기저막)과 생식세포층을 먼저 찾고, 양성 세포가 관 안인지 관 사이인지 다시 본다. 세르톨리세포는 기저막 위에 서서 생식세포를 둘러싼다."
  - "LH 는 G 단백 결합 수용체 → cAMP → StAR(콜레스테롤의 미토콘드리아 내막 수송, 속도제한) → 테스토스테론 합성으로 간다 [[harrison-21: 391장 p.3007]]."
  - "간질세포 표지(INSL3 등)로 염색한 사진은 관 안이 전부 음성이다 — 「관 안이 비었다」는 음성 소견 자체가 세르톨리세포를 배제하는 근거다."
  - "정자형성에는 FSH 와 함께 고환 안의 고농도 테스토스테론(LH → 간질세포)이 필요하다 — 두 축은 따로 그려도 기능은 이어져 있다 [[harrison-21: 391장 p.3009]]."
  - "hCG·재조합 LH 는 LH 수용체를 통해 성인기 발병 성선자극호르몬 결핍에서 정자형성을 다시 시작시킬 수 있다 [[harrison-21: 391장 p.3009]]."
checks:
  - q: "고환 사진에서 세정관 안은 음성이고 관 사이 세포 무리만 강양성이다. 이 세포의 주된 표적 호르몬은?"
    a: "LH — 관 사이의 간질(Leydig)세포이며 LH 수용체를 통해 테스토스테론을 만든다."
  - q: "FSH 의 고환 표적 세포와 그 세포가 내는 FSH 되먹임 호르몬은?"
    a: "세르톨리세포, 인히빈 B(FSH 를 선택적으로 억제)."
  - q: "간질세포에서 테스토스테론 합성의 속도제한 단계는?"
    a: "StAR 단백에 의한 콜레스테롤의 미토콘드리아 내막 수송."
  - q: "테스토스테론이 낮고 LH 가 높다. 병변 위치는?"
    a: "고환(일차 성선기능저하증). LH 가 낮거나 부적절하게 정상이면 시상하부·뇌하수체(이차)."
  - q: "AMH 가 간질세포의 표적 호르몬이 아닌 이유는?"
    a: "AMH 는 세르톨리세포가 분비해 태아 뮐러관을 퇴행시키는 호르몬이다 — 분비 산물이지 간질세포에 작용하는 호르몬이 아니다."
variants:
  - id: v1
    of: imaging-2026-0004
    flip: true
    changed: "양성 세포의 위치를 「세정관 사이 간질의 무리」에서 「세정관 안 기저막 위에서 생식세포를 둘러싸는 키 큰 세포」로 바꿈 → 표적 호르몬이 LH 에서 FSH 로 바뀜"
    context: "단서를 바꿔 답이 바뀌는 변형 — 양성 세포가 세정관 안에 있다"
    stem: "A 34-year-old man with 2 years of infertility undergoes testicular biopsy. Semen analysis showed reduced sperm concentration. The section is stained by immunohistochemistry for a protein expressed by a single testicular cell type. The positive cells are tall, irregular cells that rest on the basement membrane of the seminiferous tubules and extend cytoplasmic processes toward the lumen, surrounding developing germ cells; the interstitial tissue between the tubules is negative. The positive cells are the principal target of which of the following hormones?"
    choices: ["A. Luteinizing hormone", "B. Follicle-stimulating hormone", "C. Prolactin", "D. Gonadotropin-releasing hormone", "E. Anti-Müllerian hormone"]
    answer: "B"
    explanation: "Cells that sit on the tubular basement membrane and surround germ cells inside the seminiferous tubules are Sertoli cells, and FSH acts on the Sertoli cell to regulate spermatogenesis and inhibin B production [[harrison-21: 391장 p.3007]]. In the original item the positive cells lay between the tubules (Leydig cells), so the answer was LH; moving the positive cells into the tubule is the single change that switches the answer. LH acts primarily on Leydig cells, GnRH acts on the pituitary, and AMH is secreted by Sertoli cells rather than acting on them [[harrison-21: 391장 p.3006]]."
    kind: application
  - id: v2
    of: imaging-2026-0004
    flip: false
    changed: "나이·수술 이유(전립선암 고환절제 → 정계정맥류 수술 중 생검)·염색 대상(펩타이드 호르몬 → 스테로이드 합성 효소)·제시 순서를 바꾸고 「관 안 음성, 관 사이 무리 양성」은 그대로 → 답은 여전히 LH"
    context: "겉모습만 바꾸고 답은 같은 변형 — 다른 표지로 염색한 간질세포"
    stem: "During varicocele repair, a small testicular biopsy is taken from a 27-year-old man. The specimen is stained by immunohistochemistry for the side-chain cleavage enzyme (CYP11A1) that converts cholesterol to pregnenolone. Germ cells and all cells inside the seminiferous tubules are unstained. Strong cytoplasmic staining is present in clusters of polygonal cells in the connective tissue between the tubules. Which of the following hormones is the principal physiologic stimulus of the stained cells?"
    choices: ["A. Follicle-stimulating hormone", "B. Inhibin B", "C. Luteinizing hormone", "D. Prolactin", "E. Anti-Müllerian hormone"]
    answer: "C"
    explanation: "Clusters of cells between the tubules with the tubules themselves negative are Leydig cells — the location decides the cell, whatever the marker. In Leydig cells, CYP11A1 forms pregnenolone within the mitochondrion as part of testosterone synthesis, and LH acting on its G protein–coupled receptor drives this pathway through cAMP and StAR [[harrison-21: 391장 p.3007]]. FSH targets Sertoli cells inside the tubules; inhibin B and AMH are Sertoli-cell products, not hormones acting on Leydig cells; prolactin lowers testosterone only indirectly through suppression of gonadotropins [[harrison-21: 391장 p.3012]]."
    kind: application
figures:
- id: f1
  file: docs/assets/figures/hpa-insl3_59764_a_5_6.jpg
  kind: histology
  at: 가르는 소견 — 사진의 위치와 호르몬 양상
  shows: 고환 INSL3 면역염색 — 세정관 사이 라이디히세포가 갈색
  look_for:
  - 세정관 밖 간질에 무리 지은 큰 세포가 양성
  - 세정관 안 생식세포·세르톨리세포는 음성
  label: 'Testis, INSL3 면역조직화학 — 병리의사 주석(항체·조직 요약) Elongated or late spermatids: not detected; Leydig cells: high; Pachytene spermatocytes: not detected; Peritubular cells: not detected; Preleptotene spermatocytes: not detected; Round or early spermatids: not detected; Sertoli cells: not detected; Spermatogonia cells: not detected'
  label_basis: dataset_expert
  reference: 조직 종류·표본 진단 = 표본 기록(병리의사 SNOMED 주석), 세포별 염색 강도 = HPA 병리의사 주석(이 항체·조직의 요약 — 사진 한 장 단위가 아님)
  paper: Uhlén M 외. Tissue-based map of the human proteome. Science 2015;347:1260419
  doi: 10.1126/science.1260419
  credit: Human Protein Atlas, INSL3 / Testis (CC BY 4.0), https://images.proteinatlas.org/28615/59764_A_5_6.jpg
  license: Creative Commons Attribution 4.0 International
  url: https://www.proteinatlas.org/ENSG00000248099-INSL3/tissue/Testis
  asset: HPA-INSL3_59764_A_5_6
  paper_cited_by: 14435
  from_question: imaging-2026-0004
---

## 판단 — 위치가 세포를, 세포가 호르몬을 정한다
- 고환은 두 구획이다. **세정관 안**에서는 세르톨리세포가 생식세포를 둘러싸 분열·분화·성숙을 돕고, **세정관 사이 간질**에서는 간질(Leydig)세포가 테스토스테론을 만든다. 두 세포는 뇌하수체 LH·FSH 의 통제를 받는다 [[harrison-21: 391장 p.3006]].
- LH 는 주로 간질세포, FSH 는 세르톨리세포에 작용한다 [[harrison-21: 391장 p.3007]] — 사진 문항은 ① 위치로 세포를 정하고 ② 그 세포의 표적 호르몬을 붙이고 ③ 질문이 표적을 묻는지 분비 산물을 묻는지 확인한다.
- 「표적」과 「분비」를 섞지 않는다: 세르톨리세포는 FSH 의 표적이면서 인히빈 B·AMH 를 분비한다 [[harrison-21: 391장 p.3006]].

## 기전 — GnRH 박동에서 두 세포의 두 고리로
시상하부 GnRH 는 약 2시간마다 박동으로 나와 LH·FSH 의 박동을 만든다. LH 는 간질세포의 테스토스테론 합성을, FSH 는 세르톨리세포의 정자형성 지원과 인히빈 B 생산을 조절하고, 인히빈 B 는 FSH 를 선택적으로 누른다. 테스토스테론·에스트라디올은 시상하부·뇌하수체에 음성 되먹임을 건다 [[harrison-21: 391장 p.3007]].
- **간질세포 안**: LH 가 7회 막관통 G 단백 결합 수용체 → cAMP → StAR·스테로이드 합성 효소 유도. 속도제한 단계는 StAR 의 콜레스테롤 미토콘드리아 내막 수송이고, CYP11A1(프레그네놀론) → CYP17A1(17α-수산화효소·17,20-분해효소)을 거친다. LH 수용체 변이는 간질세포 형성저하·무형성을 일으킨다 [[harrison-21: 391장 p.3007]].
- **두 구획은 이어져 있다**: 고환 안 고농도 테스토스테론은 정자형성에 필수이고, FSH 와 함께 감수분열과 정자 방출을 진행시킨다 [[harrison-21: 391장 p.3009]].
- **태아기**: SRY 가 세르톨리세포 분화를 유도하고, 세르톨리세포는 뮐러관을 퇴행시키는 MIS(=AMH)를 만든다. 태아 간질세포는 테스토스테론으로 볼프관·외생식기를 남성화하고, INSL3 로 고환의 복강 내 하강을 돕는다 [[harrison-21: 391장 p.3006]].

## 가르는 소견 — 사진의 위치와 호르몬 양상
- **간질세포 표지(INSL3·스테로이드 합성 효소)로 염색한 사진**: 세정관 안(생식세포·세르톨리세포)은 음성, 관 사이 결합조직의 다각형 세포 무리만 양성이다. INSL3 는 간질세포가 만드는 펩타이드라 이 양상이 나온다 [[harrison-21: 391장 p.3006]] [[?hpa-insl3]]. 「관 안이 비었다」는 음성 소견도 세르톨리세포를 배제하는 근거다.
- **세르톨리세포를 보는 사진**: 양성 세포가 세정관 기저막 위에 서서 생식세포 사이로 뻗고, 간질은 음성이다.
- **프롤락틴**: 고프롤락틴혈증은 성선자극호르몬이 낮은 시상하부·뇌하수체 원인이다 [[harrison-21: 391장 p.3012]] — 간질세포를 직접 자극하는 영양호르몬이 아니다.
- **호르몬 검사**: 테스토스테론이 낮을 때 LH 가 높으면 일차(고환), 낮거나 부적절하게 정상이면 이차 [[harrison-21: 391장 p.3010]]. 세정관만 다치면 인히빈 B 가 줄어 FSH 만 선택적으로 오른다 [[harrison-21: 391장 p.3009]]. 양측 고환절제는 일차 고환 부전의 원인이다 — 원래 문항의 환자는 수술 뒤 LH 가 오른다 [[harrison-21: 391장 p.3020]].
- **정상·한 번 값의 한계**: LH 는 1–3시간마다 박동하므로 한 번 값에 기대지 말고 반복 측정한다 [[harrison-21: 391장 p.3010]].

## 권고와 예외
- 「위치 → 세포 → 수용체」 순서로 읽는다: 관 사이 = 간질세포 = LH, 관 안 = 세르톨리세포 = FSH.
- 축을 알면 치료가 따라온다: 성인기에 생긴 성선자극호르몬 결핍에서는 hCG 나 재조합 LH 가 LH 수용체를 통해 간질세포를 자극해 FSH 없이도 정자형성을 다시 시작시킬 수 있다 [[harrison-21: 391장 p.3009]].
- 전립선암의 안드로겐 차단을 위한 양측 고환절제는 테스토스테론의 주된 공급원(순환 테스토스테론의 95 % 가 고환 유래)을 없앤다 [[harrison-21: 391장 p.3007]]. 치료·수술 뒤에는 테스토스테론과 LH 를 함께 보아 결함 위치를 다시 확인한다.
- INSL3 의 조직 분포(간질세포 강양성·세정관 음성)는 Human Protein Atlas 주석을 직접 열지 못해 문항 해설의 인용만 남겼다(검토 항목).

## 시험 쟁점 — 충돌·맥락·새 근거
- 해당 없음(대조: 해리슨 391장 p.3006~3010, p.3012, p.3020)

## (심화) 왜 두 세포에 두 호르몬인가
LH 와 FSH 는 같은 GnRH 박동에 반응하지만, 고환은 두 결과물 — 전신으로 나가는 테스토스테론과 관 안에서 쓰이는 정자 — 을 따로 조절해야 한다. 간질세포–LH–테스토스테론 고리는 테스토스테론·에스트라디올의 되먹임으로, 세르톨리세포–FSH–인히빈 B 고리는 인히빈 B 의 선택적 FSH 억제로 닫힌다 [[harrison-21: 391장 p.3007]]. 그래서 세정관만 다친 환자는 테스토스테론과 LH 가 정상인데 FSH 만 오르는 「분리된」 양상을 보인다 [[harrison-21: 391장 p.3009]]. 시험은 이 분리를 사진(어느 구획이 양성인가)과 호르몬 수치(어느 되먹임이 끊겼나) 두 방향에서 묻는다.
