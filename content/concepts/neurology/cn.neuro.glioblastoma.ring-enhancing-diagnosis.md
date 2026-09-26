---
id: cn.neuro.glioblastoma.ring-enhancing-diagnosis
type: concept
topic: Hematology-Oncology
see_also: [Neurology, Radiology]
date: 2026-09-26
updated: 2026-09-26
version: 1
outline: h90            # 해리슨 21판 90장 Primary and Metastatic Tumors of the Nervous System(혈액종양내과 책)
confidence: medium
review_status: unreviewed
note_form: 2            # 판형 2(2026-09-25)
title: "교모세포종 — 축내 종괴 + 두꺼운 고리 조영"
objective: "수주에 걸쳐 진행하는 편측 결손의 고령 환자에서 축내 종괴 효과와 두꺼운 불규칙 고리 조영을 읽어 교모세포종으로 진단한다"
objective_kind: 진단
condition: 교모세포종(glioblastoma, IDH-wildtype) vs 만성 경막밑혈종·뇌경색·뇌농양·중추신경계 림프종
exams: [usmle, kmle]
summary:
  - "결론: 수주 진행 결손 + 뇌 실질 안 종괴 효과 + 두꺼운 불규칙 고리 조영·중심 괴사 = 교모세포종."
  - "시험 단서: 60~70대, 두통·경련·편마비가 수주에 걸쳐 악화, 발열 없음, 몸통 CT 원발암 없음(ring-enhancing mass)."
  - "왜: 빠르게 자라는 종양의 가장자리는 새는 신생혈관으로 조영되고 가운데는 산소가 모자라 괴사한다."
  - "먼저 병변 자리를 가른다 — 뇌 겉 초승달 저류는 경막밑혈종, 실질 안에서 고랑·뇌실을 누르면 종괴다."
  - "림프종은 뇌실 주위 균질 조영, 농양은 얇은 매끈한 벽 + 발열 — 스테로이드는 림프종 의심 시 생검 뒤로."
pitfalls:
  - contrast: "만성 경막밑혈종 vs 축내 종괴"
    point: "둘 다 고령에서 수주 진행 편마비·인지 저하를 낸다. 경막밑혈종은 머리뼈 안쪽을 따라가는 초승달 모양의 축외 저류이고, 종양은 뇌 실질 안에서 고랑을 지우고 같은 쪽 뇌실을 누른다."
    exception: "영상에 초승달 저류가 보이면 병력과 무관하게 경막밑혈종이 먼저다."
    cites: ["harrison-21: 90장 p.701", "?osborn-brain"]
    covers: ["imaging-2026-0115:D"]
  - contrast: "편마비 + 중대뇌동맥 영역 병변 = 뇌경색?"
    point: "뇌경색은 분~시간 만에 결손이 최대가 된다. 수주에 걸쳐 진행하고 뇌실을 누르며 고리로 조영되면 종괴다."
  - contrast: "고리 조영 = 농양?"
    point: "농양도 고리로 조영되지만 벽이 얇고 매끈하며 중심이 확산 제한을 보이고 발열·감염원이 있다. 두꺼운 불규칙 고리 + 발열 없음은 종양 쪽이다."
  - contrast: "고령의 악성 축내 종괴 = 림프종?"
    point: "면역이 정상인 원발 중추신경계 림프종은 뇌실 주위·뇌량·바닥핵에서 조밀하게 균질 조영된다. 중심 괴사를 둘러싼 고리는 교모세포종 쪽이다."
    cites: ["harrison-21: 90장 p.705"]
tables:
  - id: ddx
    section: "가르는 소견 — 자리·시간·조영 모양"
    title: "진행성 편측 결손 고령 환자의 뇌 병변 감별"
    role: differential
    span: column
    columns: ["질환", "가르는 소견", "임상 맥락"]
    rows:
      - ["교모세포종(glioblastoma)", "축내, 두꺼운 불규칙 고리 조영 + 중심 괴사 + 주위 부종, T2/FLAIR 고신호에 침윤 세포 [[harrison-21: 90장 p.704]]", "60~70대, 두통·경련·국소 결손 [[harrison-21: 90장 p.704]]"]
      - ["만성 경막밑혈종(chronic subdural hematoma)", "초승달 모양 축외 저류, 머리뼈 안쪽을 따라감 [[?osborn-brain]]", "고령, 가벼운 머리 외상 뒤 수주 진행"]
      - ["뇌경색(ischemic infarction)", "동맥 영역에 맞음, 아급성기 이랑 모양 조영 [[?osborn-brain]]", "분~시간 만에 최대 결손"]
      - ["뇌농양(pyogenic abscess)", "얇고 매끈한 고리, 중심 확산 제한 [[?osborn-brain]]", "발열, 부비동·치아 감염, 심내막염"]
      - ["원발 중추신경계 림프종(PCNSL)", "조밀한 균질 조영, 뇌실 주위·뇌량·바닥핵 [[harrison-21: 90장 p.705]]", "면역 정상은 고령(중앙 60세), 면역저하에서 다발 [[harrison-21: 90장 p.705]]"]
      - ["뇌 전이(brain metastasis)", "회백질 경계, 경계 뚜렷, 고리 또는 균질 조영, 영상만으로는 비특이적 [[harrison-21: 90장 p.708]]", "원발암(폐가 가장 흔함) — 몸통 영상으로 찾는다"]
criteria:
  - id: gbm-imaging
    name: 악성 뇌종양의 MRI 모양
    kind: 진단 소견
    population: "뇌종양이 의심되는 환자"
    statement: "MRI(가돌리늄 조영)가 우선 검사다. 악성 뇌종양은 원발·전이 모두 조영되고 중심 괴사와 주위 백질 부종을 보이며, 교모세포종은 중심 괴사와 부종을 동반한 고리 조영 종괴로 나타난다 [[harrison-21: 90장 p.701]] [[harrison-21: 90장 p.704]]"
    exceptions: "저등급 교종은 대개 조영되지 않는다 — FLAIR 에서 본다 [[harrison-21: 90장 p.701]]"
    source: harrison-21
    basis: current
    exams: [usmle, kmle]
sources:
  - id: harrison-21
    org: "McGraw Hill"
    title: "Harrison's Principles of Internal Medicine, 21st ed. — Chapter 90: Primary and Metastatic Tumors of the Nervous System"
    kind: textbook
    year: 2022
    citation: "Loscalzo J, Kasper DL, Longo DL, et al (eds). Harrison's Principles of Internal Medicine, 21e. 90장 p.701–708"
    checked_at: 2026-09-26
    checked: "본문 대조(드라이브 장별 문서 90장) — p.701: 편측 증상은 아급성·진행성, 악성 교종의 ~25% 경련, MRI 우선, 악성 뇌종양은 조영·중심 괴사·주위 부종, 수막종은 경막 기반 · p.702: 덱사메타손이 부종을 줄임, 경련이 있었던 환자만 항경련제(장기 예방 없음) · p.704: 교모세포종은 60~70대 두통·경련·국소 결손, 중심 괴사·부종을 동반한 고리 조영 종괴, T2/FLAIR 고신호에 침윤 세포, ~10% IDH 돌연변이, 다음 WHO 개정에서 IDH-wildtype 으로 한정 예정, 최대 안전 절제 뒤 RT 60 Gy/30회 + 테모졸로마이드 → 보조 6개월, 중앙 생존 14.6–18개월 · p.705: 원발 CNS 림프종은 조밀한 조영·뇌실 주위/뇌량/바닥핵, 면역 정상 환자 중앙 60세, 생검 전 스테로이드 보류 · p.708: 전이는 회백질 경계, 고리 또는 균질 조영, 영상은 비특이적(농양 등과 비슷). 농양의 벽 두께·확산 제한, 경막밑혈종 모양, 뇌경색 조영 양상은 이 장에 없다"
    verified: text
  - id: osborn-brain
    org: "Osborn AG"
    title: "Osborn's Brain: Imaging, Pathology, and Anatomy, 2nd ed."
    kind: textbook
    year: 2017
    citation: "Osborn AG. Osborn's Brain: Imaging, Pathology, and Anatomy. 2nd ed. Elsevier; 2017"
    checked_at: 2026-09-26
    checked: "원문 미확인 — 문항 해설의 근거 목록에 있는 서지만 옮김(농양·경막밑혈종·뇌경색 영상 소견의 출처 후보)"
    verified: citation
  - id: louis-2021
    org: "Louis DN et al (WHO CNS5)"
    title: "The 2021 WHO Classification of Tumors of the Central Nervous System: a summary"
    kind: guideline
    year: 2021
    citation: "Neuro Oncol 2021;23(8):1231-1251"
    doi: "10.1093/neuonc/noab106"
    pmid: "34185076"
    checked_at: 2026-09-26
    checked: "원문 미확인 — 컨테이너가 PubMed·doi.org 를 막음. 서지·DOI·PMID 는 기억으로 적었다(학습서 워크플로가 확인)"
    verified: citation
diagram:
  title: "진행성 편측 결손 — 자리·시간·조영으로 가른다"
  nodes:
    - {id: start, kind: start, text: "고령, 수주 진행 편마비·두통·경련"}
    - {id: loc, kind: decision, text: "병변이 뇌 실질 안(축내)인가?"}
    - {id: locinfo, kind: info, text: "MRI 로 축외 저류·종괴 효과 확인"}
    - {id: sdh, kind: end, text: "만성 경막밑혈종 — 초승달 축외 저류"}
    - {id: onset, kind: decision, text: "분~시간 만에 결손이 최대였나?"}
    - {id: infarct, kind: end, text: "뇌경색 — 동맥 영역에 맞는 병변"}
    - {id: enh, kind: decision, text: "조영 양상은?"}
    - {id: enhinfo, kind: info, text: "조영 T1·확산강조영상(DWI) 추가"}
    - {id: abscess, kind: alert, text: "뇌농양 — 얇은 벽·중심 확산 제한·발열"}
    - {id: pcnsl, kind: end, text: "원발 CNS 림프종 — 생검 전 스테로이드 보류"}
    - {id: gbm, kind: end, text: "교모세포종 — 두꺼운 불규칙 고리·중심 괴사"}
  edges:
    - {from: start, to: loc}
    - {from: loc, to: sdh, label: "축외 초승달"}
    - {from: loc, to: locinfo, label: "영상 없음"}
    - {from: loc, to: onset, label: "축내 종괴 효과"}
    - {from: locinfo, to: sdh, label: "축외 저류"}
    - {from: locinfo, to: onset, label: "축내 병변"}
    - {from: onset, to: infarct, label: "예"}
    - {from: onset, to: enh, label: "수주 진행"}
    - {from: enh, to: abscess, label: "얇은 고리·발열"}
    - {from: enh, to: pcnsl, label: "균질·뇌실 주위"}
    - {from: enh, to: gbm, label: "두꺼운 고리"}
    - {from: enh, to: enhinfo, label: "미시행"}
    - {from: enhinfo, to: gbm, label: "두꺼운 고리"}
    - {from: enhinfo, to: abscess, label: "중심 확산 제한"}
diagram_notes:
  - "고리 조영은 전이·농양·탈수초 병변·방사선 괴사에서도 보인다 — 몸통 CT 로 원발암을 찾아 전이를 줄이고, 발열·감염원으로 농양을 줄인다 [[harrison-21: 90장 p.708]]."
  - "림프종이 의심되면 정위 생검 전에 스테로이드를 보류한다 — 림프종 세포를 녹여 진단 조직이 안 나올 수 있다 [[harrison-21: 90장 p.705]]."
  - "뇌경색도 아급성기에 조영되지만 이랑 모양이고 동맥 영역에 맞는다 — 수주 동안 뇌실을 누르는 두꺼운 고리는 아니다."
checks:
  - q: "고령 환자의 수주 진행 편마비에서 영상으로 가장 먼저 가를 것은?"
    a: "병변이 축외(초승달 저류 = 경막밑혈종)인지 축내(고랑·뇌실을 누르는 실질 종괴)인지."
  - q: "교모세포종의 두꺼운 고리와 중심 비조영 부위는 각각 무엇인가?"
    a: "고리 = 새는 신생혈관을 가진 살아 있는 종양, 가운데 = 산소 부족으로 생긴 괴사."
  - q: "고리 조영 종괴에서 농양 쪽으로 기우는 소견은?"
    a: "얇고 매끈한 벽, 중심 확산 제한, 발열이나 감염원(부비동·치아·심내막염)."
variants:
  - id: v1
    of: imaging-2026-0115
    flip: true
    changed: "발열·최근 치아 감염을 더하고 고리를 「두꺼운 불규칙」에서 「얇고 매끈, 중심 확산 제한」으로 바꿈 → 답이 교모세포종에서 화농성 뇌농양으로"
    context: "Changed clue flips the answer — thin smooth ring, fever, dental source"
    stem: "A 58-year-old man is brought to the emergency department because of worsening headache and weakness of his right arm over the past 10 days. Three weeks ago he had a lower molar extracted for a painful abscess. He has not been immunosuppressed. His temperature is 38.4°C. Examination shows mild right hemiparesis. Chest, abdomen, and pelvic CT shows no mass. MRI of the brain shows a left frontal intra-axial lesion with surrounding edema and effacement of the adjacent sulci. After gadolinium, the lesion has a thin, smooth rim of enhancement that is thinnest on its ventricular side, and the center shows marked restricted diffusion. Which of the following is the most likely diagnosis?"
    choices: ["A. Glioblastoma", "B. Pyogenic brain abscess", "C. Primary CNS lymphoma", "D. Chronic subdural hematoma", "E. Acute ischemic infarction"]
    answer: "B"
    explanation: "The lesion is still intra-axial with mass effect, but three findings now point to infection: fever after a recent dental abscess, a thin smooth rim (thinnest toward the ventricle), and restricted diffusion in the center, which reflects viscous pus [[?osborn-brain]]. Ring enhancement alone does not separate tumor from abscess — Harrison notes that similar-appearing lesions occur with brain abscesses [[harrison-21: 90장 p.708]]. In the original item the ring was thick and irregular around necrosis in an afebrile older man, which favors glioblastoma. Lymphoma enhances densely and homogeneously, and a subdural hematoma is an extra-axial crescent."
    kind: application
  - id: v2
    of: imaging-2026-0115
    flip: false
    changed: "성별(여자)·나이(66세)·주증상(언어장애·오른쪽 약화, 가족이 성격 변화를 알아챔)·병변 쪽(왼쪽 측두엽)·제시 순서를 바꾸고 「수주 진행, 발열 없음, 축내 종괴 효과, 두꺼운 불규칙 고리 + 중심 괴사, 원발암 없음」은 유지 → 답은 여전히 교모세포종"
    context: "Surface details change, answer stays — aphasia and personality change in an older woman"
    stem: "A 66-year-old woman is brought to the physician by her daughter, who has noticed over the past 6 weeks that she has become irritable, has trouble finding words, and drops objects from her right hand. She has had headaches on waking for a month. She has no fever and takes no immunosuppressive drugs. Examination shows a nonfluent aphasia and mild right hand weakness. Mammography and CT of the chest, abdomen, and pelvis are normal. MRI of the brain shows a left temporal intra-axial mass with surrounding T2/FLAIR hyperintensity and compression of the left lateral ventricle; there is no extra-axial collection. After gadolinium, the mass has a thick, irregular rim of enhancement around a central nonenhancing area. Which of the following is the most likely diagnosis?"
    choices: ["A. Chronic subdural hematoma", "B. Primary CNS lymphoma", "C. Glioblastoma", "D. Pyogenic brain abscess", "E. Acute ischemic infarction"]
    answer: "C"
    explanation: "The deciding clues are unchanged from the original item: weeks of progressive deficit in an older adult, an intra-axial mass with mass effect, a thick irregular ring around central necrosis, no fever, and no primary cancer on body imaging. Glioblastoma typically presents in the sixth and seventh decades with headache, seizures, or focal deficits and appears as a ring-enhancing mass with central necrosis and surrounding edema [[harrison-21: 90장 p.704]]. Aphasia and personality change replace hemiparesis only because the lesion is in the dominant temporal lobe. There is no extra-axial crescent, the course is too slow for infarction, lymphoma would enhance homogeneously, and there is no infectious setting for abscess."
    kind: application
---

## 판단 — 왜 교모세포종이 먼저인가
- **자리**: 뇌 실질 안에서 고랑을 지우고 같은 쪽 측뇌실을 누른다 → 축내 종괴. 머리뼈 안쪽을 따라가는 초승달 저류가 없으므로 경막밑혈종이 아니다.
- **시간**: 편측 증상이 아급성으로 진행한다 — 뇌종양의 전형적 경과다 [[harrison-21: 90장 p.701]]. 분~시간 만에 최대가 되는 뇌경색과 다르다.
- **조영 모양**: 중심 괴사를 둘러싼 고리 조영 + 주위 부종은 교모세포종의 전형 [[harrison-21: 90장 p.704]]. 두껍고 불규칙한 벽, 발열 없음은 농양보다 종양 쪽이다.
- **나머지 배제**: 몸통 CT 에 원발암이 없어 단발 전이 가능성이 낮고, 면역이 정상이며 조영이 균질하지 않아 림프종보다 교모세포종이다.

## 기전 — 새는 신생혈관과 중심 괴사
교모세포종은 혈액 공급을 앞질러 자란다. 종양이 만든 비정상 신생혈관은 혈액뇌장벽이 깨져 있어 가돌리늄이 새어 나오므로 살아 있는 종양 가장자리가 두껍고 울퉁불퉁한 고리로 조영된다. 가운데는 산소가 모자라 괴사하므로 조영되지 않는다. 종양은 주변 백질로 침윤하고 혈관성 부종이 겹쳐 T1 저신호·T2/FLAIR 고신호가 넓게 퍼지며, 이 고신호 부위에도 침윤한 종양 세포가 있다 [[harrison-21: 90장 p.704]]. 이 부피가 고랑을 지우고 뇌실을 눌러 두통(아침에 심한 경우가 있음)·경련·국소 결손을 만든다 [[harrison-21: 90장 p.701]].

## 가르는 소견 — 자리·시간·조영 모양
- 조영 전 T1 한 장만으로도 **축내 vs 축외**와 **종괴 효과**는 읽을 수 있다. 조영 모양·확산강조영상(diffusion-weighted imaging, DWI)은 축내 병변 사이를 가른다.
- 고리 조영은 비특이적이다 — 전이·농양·탈수초·방사선 괴사도 비슷하게 보일 수 있어 임상 맥락(발열, 원발암, 면역 상태)과 함께 읽는다 [[harrison-21: 90장 p.708]].
- 수막종은 경막에 붙어 조영되고 뇌를 누르지만 침윤하지 않는다 — 축외 종괴다 [[harrison-21: 90장 p.701]].

## 권고와 예외
- 조영 MRI 가 우선이고 CT 는 MRI 를 못 하는 환자에게 남긴다 [[harrison-21: 90장 p.701]].
- 부종으로 인한 증상은 덱사메타손이 빠르게 줄인다. 다만 림프종이 의심되면 생검 전에는 보류한다 [[harrison-21: 90장 p.702]] [[harrison-21: 90장 p.705]].
- 경련이 있었던 환자는 항경련제를 쓰고, 경련이 없던 환자에게 장기 예방 투여는 하지 않는다 [[harrison-21: 90장 p.702]].
- 확진은 조직 검사다. 치료는 최대 안전 절제 뒤 방사선(60 Gy/30회)과 테모졸로마이드 병용, 이어서 보조 테모졸로마이드 6개월이고, 중앙 생존은 14.6~18개월이다 [[harrison-21: 90장 p.704]]. 65~70세 넘는 고령은 40 Gy/3주 단기 분할 + 테모졸로마이드도 쓴다 [[harrison-21: 90장 p.704]].

## 시험 쟁점 — 충돌·맥락·새 근거
- **Z1 새 근거 · 「교모세포종」의 정의** — 시험 기준: 교모세포종은 IDH 돌연변이가 없는(IDH-wildtype) 등급 4 성상세포 종양으로 한정된다 — 해리슨 21판은 「다음 WHO 개정에서 그렇게 바뀐다」고 적는다 [[harrison-21: 90장 p.704]] / 다른 기준: 2021 WHO 분류(CNS5)가 이를 시행 — IDH 돌연변이 등급 4 는 「성상세포종, IDH-mutant, 등급 4」 [[?louis-2021]] / 왜 다른가: 해리슨 21판 집필이 WHO 2021 발표 전후라 예고형으로 서술 / 시험에서는: KMLE·USMLE 모두 영상·임상 진단은 「glioblastoma」, 분자 분류를 물으면 IDH-wildtype 이 교모세포종이다.
- 농양·경막밑혈종·뇌경색의 영상 소견(벽 두께, 확산 제한, 초승달 모양, 이랑 조영)은 해리슨 90장에 없어 대조하지 못했다 — [[?osborn-brain]] 로 남긴다.
