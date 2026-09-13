// 자동 생성 파일 — 수정하지 마세요.
// 원본: content/imaging/**/*.md  →  `python pipelines/export_imaging_web.py`로 재생성
window.IMAGING_QUESTIONS = [
 {
  "id": "imaging-2026-0014",
  "exam": "imaging",
  "style": "usmle_style",
  "styleLabel": "USMLE형",
  "subject": "산부인과",
  "subject_file": "산부인과",
  "setSubject": "통합(생식의학·산과 마취·흉부 해부)",
  "subtopic": "산과 — 분만 중 태아감시·산과 마취",
  "type": "산과 — 분만 중 태아감시·산과 마취",
  "modality": "CTG",
  "step": "Step 2",
  "difficulty": 4,
  "difficultyLabel": "상",
  "created": "2026-09-13",
  "vignette": "A 29-year-old primigravid woman at 39 weeks' gestation is in the active phase of labor with continuous electronic fetal monitoring. Her pregnancy has been uncomplicated and membranes are intact. The tracing from minutes 30 to 40 of monitoring is shown.",
  "question": "According to the NICHD three-tier system, which of the following best describes this tracing?",
  "options": [
   "Category II with fetal tachycardia",
   "Category III with absent variability and recurrent late decelerations",
   "Category I (normal tracing)",
   "Category II with minimal baseline variability",
   "Category II with recurrent variable decelerations"
  ],
  "answer": 3,
  "explanationText": "- 정답 핵심: The baseline fetal heart rate is about 140–145/min (normal range 110–160). Peak-to-trough fluctuation within 1-minute windows is about 7–10/min, i.e. moderate variability (6–25/min). There are no decelerations of any type; two brief rises toward 155–160/min are accelerations or short signal artefacts, and a brief gap around minute 36 is signal loss, not a deceleration. Normal baseline, moderate variability and no late or variable decelerations define Category I.\n- 원리: The three-tier NICHD system is built on <b>four elements read in order: baseline, variability, accelerations, decelerations</b>.<br> <b>Baseline</b> is the mean rate rounded to 5/min over a 10-minute window, excluding accelerations, decelerations and segments of marked variability; it must be present for at least 2 minutes. Here the trace sits at 140–145/min, inside 110–160/min.<br> <b>Variability</b> is the peak-to-trough amplitude of the irregular fluctuations in a 1-minute window: absent (undetectable), minimal (≤5), <b>moderate (6–25)</b>, marked (>25). Moderate variability reflects an <b>intact, oxygenated autonomic system</b> — the sympathetic and parasympathetic inputs continuously tugging the sinus node — and is the single most reassuring feature; its presence makes significant metabolic acidemia unlikely at that moment.<br> <b>Category I</b> requires <b>all</b> of: normal baseline, moderate variability, no late or variable decelerations (early decelerations and accelerations may be present or absent). <b>Category III</b> is absent variability plus recurrent late or variable decelerations or bradycardia, or a sinusoidal pattern. <b>Everything else is Category II</b> — an indeterminate group that calls for evaluation and continued surveillance, not immediate delivery.<br> <b>Why decelerations are classified by timing and shape</b> — early (gradual, nadir with contraction peak: head compression), late (gradual, nadir after the peak: uteroplacental insufficiency), variable (abrupt, ≥15/min for ≥15 s and <2 min: cord compression). None of these is present in this window; the short gaps are electrode signal loss.\n- 비교: <table><thead><tr><th style=\"width:28%\">Category</th><th style=\"width:40%\">Defining features</th><th>This tracing</th></tr></thead><tbody> <tr><td><b>Category I (answer)</b></td><td><b>baseline 110–160, moderate variability (6–25), no late/variable decelerations</b></td><td>baseline ≈140–145, variability ≈7–10, no decelerations</td></tr> <tr><td>Category II, minimal variability</td><td>amplitude ≤5/min in a 1-min window, other features normal</td><td>fluctuations are 7–10/min, i.e. above 5</td></tr> <tr><td>Category II, recurrent variable decelerations</td><td>abrupt drops ≥15/min lasting ≥15 s with ≥50 % of contractions</td><td>no drop below baseline; contractions are weak and infrequent</td></tr> <tr><td>Category II, tachycardia</td><td>baseline >160/min</td><td>baseline well under 160</td></tr> <tr><td>Category III</td><td>absent variability + recurrent late/variable decelerations or bradycardia; or sinusoidal</td><td>none of these</td></tr> </tbody></table> The <b>closest wrong answer is Category II with minimal variability</b>: a smoothed or compressed strip can make 7–10/min look flat. The 5/min cut-off is applied to the raw 1-minute peak-to-trough amplitude, and at 3 cm/min the small-square height (5/min) is the ruler.\n- 오답 이유:\n  - (A) Fetal tachycardia is a baseline above 160/min for at least 10 minutes. The baseline here is about 140–145/min. This option would be correct only if the trace ran above 160/min throughout the window.\n  - (B) Category III needs absent variability together with recurrent late or variable decelerations or bradycardia, or a sinusoidal pattern. This trace has moderate variability and no decelerations. This option would be correct only if the line were flat and dipping after each contraction.\n  - (D) Minimal variability means peak-to-trough amplitude of 5/min or less within a 1-minute window. Measured against the 5/min grid this trace fluctuates 7–10/min. This option would be correct only if the line were nearly flat within each minute.\n  - (E) Variable decelerations are abrupt drops of at least 15/min lasting at least 15 seconds, and 'recurrent' means with at least half of the contractions. No drop below baseline occurs in this window and contractions are weak. This option would be correct only if abrupt V-shaped dips accompanied most contractions.\n- 함정: Short gaps in the trace are signal loss, not decelerations — a deceleration is a continuous line that leaves the baseline and returns; a gap has no line at all.\n- 학습목표: 분만 중 태아심박동 기록의 기저선·변이도·감속을 읽어 NICHD 3단계 분류를 적용한다\n- 근거·출처: CTU-UHB raw data (4 Hz) — author measurement (2026-09-14): baseline ≈140–145/min, 1-min peak-to-trough ≈7–10/min, no decelerations, brief signal loss 35.8–36.6 min · Macones GA et al. The 2008 NICHD workshop report on electronic fetal monitoring (Obstet Gynecol 2008) · ACOG Practice Bulletin No. 106\n\n## 출처\n- CTU-UHB Intrapartum Cardiotocography Database (PhysioNet, ODC-BY 1.0) · record 1339 · Open Data Commons Attribution License v1.0 · https://opendatacommons.org/licenses/by/1-0/",
  "explanationItems": [
   {
    "k": "정답 핵심",
    "v": "The baseline fetal heart rate is about 140–145/min (normal range 110–160). Peak-to-trough fluctuation within 1-minute windows is about 7–10/min, i.e. moderate variability (6–25/min). There are no decelerations of any type; two brief rises toward 155–160/min are accelerations or short signal artefacts, and a brief gap around minute 36 is signal loss, not a deceleration. Normal baseline, moderate variability and no late or variable decelerations define Category I."
   },
   {
    "k": "원리",
    "v": "The three-tier NICHD system is built on <b>four elements read in order: baseline, variability, accelerations, decelerations</b>.<br> <b>Baseline</b> is the mean rate rounded to 5/min over a 10-minute window, excluding accelerations, decelerations and segments of marked variability; it must be present for at least 2 minutes. Here the trace sits at 140–145/min, inside 110–160/min.<br> <b>Variability</b> is the peak-to-trough amplitude of the irregular fluctuations in a 1-minute window: absent (undetectable), minimal (≤5), <b>moderate (6–25)</b>, marked (>25). Moderate variability reflects an <b>intact, oxygenated autonomic system</b> — the sympathetic and parasympathetic inputs continuously tugging the sinus node — and is the single most reassuring feature; its presence makes significant metabolic acidemia unlikely at that moment.<br> <b>Category I</b> requires <b>all</b> of: normal baseline, moderate variability, no late or variable decelerations (early decelerations and accelerations may be present or absent). <b>Category III</b> is absent variability plus recurrent late or variable decelerations or bradycardia, or a sinusoidal pattern. <b>Everything else is Category II</b> — an indeterminate group that calls for evaluation and continued surveillance, not immediate delivery.<br> <b>Why decelerations are classified by timing and shape</b> — early (gradual, nadir with contraction peak: head compression), late (gradual, nadir after the peak: uteroplacental insufficiency), variable (abrupt, ≥15/min for ≥15 s and <2 min: cord compression). None of these is present in this window; the short gaps are electrode signal loss."
   },
   {
    "k": "비교",
    "v": "<table><thead><tr><th style=\"width:28%\">Category</th><th style=\"width:40%\">Defining features</th><th>This tracing</th></tr></thead><tbody> <tr><td><b>Category I (answer)</b></td><td><b>baseline 110–160, moderate variability (6–25), no late/variable decelerations</b></td><td>baseline ≈140–145, variability ≈7–10, no decelerations</td></tr> <tr><td>Category II, minimal variability</td><td>amplitude ≤5/min in a 1-min window, other features normal</td><td>fluctuations are 7–10/min, i.e. above 5</td></tr> <tr><td>Category II, recurrent variable decelerations</td><td>abrupt drops ≥15/min lasting ≥15 s with ≥50 % of contractions</td><td>no drop below baseline; contractions are weak and infrequent</td></tr> <tr><td>Category II, tachycardia</td><td>baseline >160/min</td><td>baseline well under 160</td></tr> <tr><td>Category III</td><td>absent variability + recurrent late/variable decelerations or bradycardia; or sinusoidal</td><td>none of these</td></tr> </tbody></table> The <b>closest wrong answer is Category II with minimal variability</b>: a smoothed or compressed strip can make 7–10/min look flat. The 5/min cut-off is applied to the raw 1-minute peak-to-trough amplitude, and at 3 cm/min the small-square height (5/min) is the ruler."
   },
   {
    "k": "오답 이유",
    "v": "(A) Fetal tachycardia is a baseline above 160/min for at least 10 minutes. The baseline here is about 140–145/min. This option would be correct only if the trace ran above 160/min throughout the window.\n(B) Category III needs absent variability together with recurrent late or variable decelerations or bradycardia, or a sinusoidal pattern. This trace has moderate variability and no decelerations. This option would be correct only if the line were flat and dipping after each contraction.\n(D) Minimal variability means peak-to-trough amplitude of 5/min or less within a 1-minute window. Measured against the 5/min grid this trace fluctuates 7–10/min. This option would be correct only if the line were nearly flat within each minute.\n(E) Variable decelerations are abrupt drops of at least 15/min lasting at least 15 seconds, and 'recurrent' means with at least half of the contractions. No drop below baseline occurs in this window and contractions are weak. This option would be correct only if abrupt V-shaped dips accompanied most contractions."
   },
   {
    "k": "함정",
    "v": "Short gaps in the trace are signal loss, not decelerations — a deceleration is a continuous line that leaves the baseline and returns; a gap has no line at all."
   },
   {
    "k": "학습목표",
    "v": "분만 중 태아심박동 기록의 기저선·변이도·감속을 읽어 NICHD 3단계 분류를 적용한다"
   },
   {
    "k": "근거·출처",
    "v": "CTU-UHB raw data (4 Hz) — author measurement (2026-09-14): baseline ≈140–145/min, 1-min peak-to-trough ≈7–10/min, no decelerations, brief signal loss 35.8–36.6 min · Macones GA et al. The 2008 NICHD workshop report on electronic fetal monitoring (Obstet Gynecol 2008) · ACOG Practice Bulletin No. 106 ## 출처 CTU-UHB Intrapartum Cardiotocography Database (PhysioNet, ODC-BY 1.0) · record 1339 · Open Data Commons Attribution License v1.0 · https://opendatacommons.org/licenses/by/1-0/"
   }
  ],
  "source": "의대_시험지_제작 오픈데이터 영상 세트 / 20260913T201606Z_일일영상_2026-09-14_9units_9q_85b9cadf",
  "vitals": [],
  "labs": [],
  "appendix": null,
  "figureImg": {
   "src": "assets/imaging/imaging-2026-0014.png",
   "caption": "Intrapartum fetal heart rate (upper) and uterine activity (lower), minutes 30–40 of monitoring; 3 cm/min, vertical lines = 1 min (CTU-UHB Intrapartum Cardiotocography Database, PhysioNet, ODC-BY 1.0; 4 Hz raw data, no smoothing)",
   "alt": "CTG 영상"
  },
  "attribution": {
   "dataset": "CTU-UHB Intrapartum Cardiotocography Database",
   "license": "Open Data Commons Attribution License v1.0",
   "license_url": "https://opendatacommons.org/licenses/by/1-0/",
   "url": "https://physionet.org/content/ctu-uhb-ctgdb/1.0.0/",
   "asset_id": "CTU-1339_30m",
   "text": "CTU-UHB Intrapartum Cardiotocography Database (PhysioNet, ODC-BY 1.0) · record 1339"
  },
  "run_id": "20260913T201606Z_일일영상_2026-09-14_9units_9q_85b9cadf",
  "qid": "Q0005"
 },
 {
  "id": "imaging-2026-0013",
  "exam": "imaging",
  "style": "usmle_style",
  "styleLabel": "USMLE형",
  "subject": "호흡기",
  "subject_file": "호흡기",
  "setSubject": "통합(생식의학·산과 마취·흉부 해부)",
  "subtopic": "흉부 CT 정상 해부 — 세로칸·가로막",
  "type": "흉부 CT 정상 해부 — 세로칸·가로막",
  "modality": "CT",
  "step": "Step 2",
  "difficulty": 4,
  "difficultyLabel": "상",
  "created": "2026-09-13",
  "vignette": "A 67-year-old woman undergoes CT of the chest as part of a health screening program. She has no cough, fever, dyspnea, or weight loss, and she has never smoked. An axial image of the chest at the level of the lung bases (lung window) is shown.",
  "question": "Which of the following best explains the large, smooth, homogeneous soft-tissue density that occupies the anterior part of the right lower hemithorax?",
  "options": [
   "Dome of the right hemidiaphragm with the liver beneath it",
   "Consolidation of the right lower lobe",
   "Loculated right pleural effusion",
   "Mass arising in the right middle lobe",
   "Atelectasis of the right lower lobe"
  ],
  "answer": 1,
  "explanationText": "- 정답 핵심: The density has a smooth, convex, sharply defined margin, is perfectly homogeneous, and the aerated lung wraps around it posteriorly and laterally without any air bronchograms, volume loss, or septal thickening. At the level of the lung bases the right hemidiaphragm rises higher than the left because of the liver; an axial slice cuts the top of the dome and displays the liver as a round soft-tissue 'mass' surrounded by lung. The normal left lung base and the heart at the same level confirm the level.\n- 원리: An axial CT slice is a <b>3 mm-thick slab</b> through a body whose organs are curved. The right hemidiaphragm is a <b>dome that rises to about the 4th–5th intercostal space</b> in expiration, higher than the left because the liver sits beneath it. A transverse slice through the upper part of that dome therefore contains <b>lung all around and diaphragm-plus-liver in the middle</b>: on the image the liver appears as a round, homogeneous soft-tissue 'mass' surrounded by aerated lung. This is a <b>partial-volume / geometric effect of the dome, not a lesion</b>.<br> <b>How to recognize it</b> — (1) the margin is <b>smooth and convex toward the lung</b> in every direction, because it is a curved surface; (2) the interior is <b>perfectly homogeneous</b> with no air bronchograms, no vessels running into it and no cavity; (3) the lung around it is <b>normal</b>, with no volume loss (fissures, hilum and mediastinum are not displaced) and no septal thickening; (4) on the slice above it becomes smaller and on the slice below it becomes larger, until it merges with the whole liver.<br> <b>Why the alternatives look different</b> — consolidation keeps the shape of the lobe and contains air bronchograms; atelectasis shrinks the lobe and pulls the fissure and hilum toward it; an effusion layers dependently (posteriorly in a supine patient) with a meniscus and would not sit anteriorly; a mass has an irregular or lobulated edge, feeding vessels and no 'grows-into-the-liver' behaviour on adjacent slices.\n- 비교: <table><thead><tr><th style=\"width:30%\">Finding</th><th style=\"width:36%\">Shape and interior</th><th>What the surrounding lung does</th></tr></thead><tbody> <tr><td><b>Diaphragm dome + liver (answer)</b></td><td><b>smooth convex margin, homogeneous, anterior right base</b></td><td>normal lung wraps around, no volume loss, merges with liver on lower slices</td></tr> <tr><td>Lobar consolidation</td><td>lobe-shaped, <b>air bronchograms</b>, heterogeneous</td><td>lobe keeps its volume; fissure is a straight boundary</td></tr> <tr><td>Atelectasis</td><td>wedge/triangular, crowded vessels</td><td><b>volume loss</b>: fissure, hilum, mediastinum pulled toward it</td></tr> <tr><td>Pleural effusion</td><td>crescent along the chest wall, <b>dependent (posterior)</b> in a supine patient</td><td>lung compressed anteriorly, meniscus</td></tr> </tbody></table> The <b>closest wrong answer is right lower lobe consolidation</b>: both are soft-tissue density at the base. The discriminator is the <b>absence of air bronchograms and the perfectly smooth convex edge</b>; pneumonia also does not occur in a patient with no symptoms.\n- 오답 이유:\n  - (B) Consolidation fills alveoli with fluid or pus but leaves the bronchi open, producing air bronchograms inside a lobe-shaped opacity, usually with cough and fever. This option would be correct only if branching air lucencies were visible inside the density and the patient had symptoms.\n  - (C) A pleural effusion collects in the dependent (posterior) pleural space of a supine patient as a crescent with a meniscus against the chest wall; it does not form a round anterior density surrounded by lung. This option would be correct only if the fluid lay posteriorly along the ribs.\n  - (D) A lung mass has an irregular, lobulated or spiculated margin, is rarely this large without symptoms, and does not enlarge smoothly into the liver on adjacent slices. This option would be correct only if the edge were irregular and the density persisted as a separate structure below the diaphragm.\n  - (E) Atelectasis produces volume loss: the fissure, hilum and mediastinum shift toward the collapsed lobe and the remaining lung over-expands. Here the fissures and mediastinum are in normal position. This option would be correct only if the right hilum and heart were pulled toward the density.\n- 함정: At the lung bases the right dome is always cut first — a round 'mass' appearing at the anterior right base on a single slice is the liver until proven otherwise. Scroll up and down before naming a lesion.\n- 학습목표: 폐 바닥 축상 CT 에서 가로막돔의 부분용적 효과로 생기는 균질 음영을 병변과 구분한다\n- 근거·출처: TCIA LIDC-IDRI series (CC BY 3.0) — author reading (2026-09-14): lung-base slice, right hemidiaphragm dome (liver) occupying the anterior right base, both lower lobes normal, no nodule · Webb WR, Higgins CB. Thoracic Imaging — diaphragm and partial-volume artefacts at the lung bases\n\n## 출처\n- LIDC-IDRI, The Cancer Imaging Archive (CC BY 3.0) · series …43069436 · Creative Commons Attribution 3.0 Unported · https://www.cancerimagingarchive.net/data-usage-policies-and-restrictions/",
  "explanationItems": [
   {
    "k": "정답 핵심",
    "v": "The density has a smooth, convex, sharply defined margin, is perfectly homogeneous, and the aerated lung wraps around it posteriorly and laterally without any air bronchograms, volume loss, or septal thickening. At the level of the lung bases the right hemidiaphragm rises higher than the left because of the liver; an axial slice cuts the top of the dome and displays the liver as a round soft-tissue 'mass' surrounded by lung. The normal left lung base and the heart at the same level confirm the level."
   },
   {
    "k": "원리",
    "v": "An axial CT slice is a <b>3 mm-thick slab</b> through a body whose organs are curved. The right hemidiaphragm is a <b>dome that rises to about the 4th–5th intercostal space</b> in expiration, higher than the left because the liver sits beneath it. A transverse slice through the upper part of that dome therefore contains <b>lung all around and diaphragm-plus-liver in the middle</b>: on the image the liver appears as a round, homogeneous soft-tissue 'mass' surrounded by aerated lung. This is a <b>partial-volume / geometric effect of the dome, not a lesion</b>.<br> <b>How to recognize it</b> — (1) the margin is <b>smooth and convex toward the lung</b> in every direction, because it is a curved surface; (2) the interior is <b>perfectly homogeneous</b> with no air bronchograms, no vessels running into it and no cavity; (3) the lung around it is <b>normal</b>, with no volume loss (fissures, hilum and mediastinum are not displaced) and no septal thickening; (4) on the slice above it becomes smaller and on the slice below it becomes larger, until it merges with the whole liver.<br> <b>Why the alternatives look different</b> — consolidation keeps the shape of the lobe and contains air bronchograms; atelectasis shrinks the lobe and pulls the fissure and hilum toward it; an effusion layers dependently (posteriorly in a supine patient) with a meniscus and would not sit anteriorly; a mass has an irregular or lobulated edge, feeding vessels and no 'grows-into-the-liver' behaviour on adjacent slices."
   },
   {
    "k": "비교",
    "v": "<table><thead><tr><th style=\"width:30%\">Finding</th><th style=\"width:36%\">Shape and interior</th><th>What the surrounding lung does</th></tr></thead><tbody> <tr><td><b>Diaphragm dome + liver (answer)</b></td><td><b>smooth convex margin, homogeneous, anterior right base</b></td><td>normal lung wraps around, no volume loss, merges with liver on lower slices</td></tr> <tr><td>Lobar consolidation</td><td>lobe-shaped, <b>air bronchograms</b>, heterogeneous</td><td>lobe keeps its volume; fissure is a straight boundary</td></tr> <tr><td>Atelectasis</td><td>wedge/triangular, crowded vessels</td><td><b>volume loss</b>: fissure, hilum, mediastinum pulled toward it</td></tr> <tr><td>Pleural effusion</td><td>crescent along the chest wall, <b>dependent (posterior)</b> in a supine patient</td><td>lung compressed anteriorly, meniscus</td></tr> </tbody></table> The <b>closest wrong answer is right lower lobe consolidation</b>: both are soft-tissue density at the base. The discriminator is the <b>absence of air bronchograms and the perfectly smooth convex edge</b>; pneumonia also does not occur in a patient with no symptoms."
   },
   {
    "k": "오답 이유",
    "v": "(B) Consolidation fills alveoli with fluid or pus but leaves the bronchi open, producing air bronchograms inside a lobe-shaped opacity, usually with cough and fever. This option would be correct only if branching air lucencies were visible inside the density and the patient had symptoms.\n(C) A pleural effusion collects in the dependent (posterior) pleural space of a supine patient as a crescent with a meniscus against the chest wall; it does not form a round anterior density surrounded by lung. This option would be correct only if the fluid lay posteriorly along the ribs.\n(D) A lung mass has an irregular, lobulated or spiculated margin, is rarely this large without symptoms, and does not enlarge smoothly into the liver on adjacent slices. This option would be correct only if the edge were irregular and the density persisted as a separate structure below the diaphragm.\n(E) Atelectasis produces volume loss: the fissure, hilum and mediastinum shift toward the collapsed lobe and the remaining lung over-expands. Here the fissures and mediastinum are in normal position. This option would be correct only if the right hilum and heart were pulled toward the density."
   },
   {
    "k": "함정",
    "v": "At the lung bases the right dome is always cut first — a round 'mass' appearing at the anterior right base on a single slice is the liver until proven otherwise. Scroll up and down before naming a lesion."
   },
   {
    "k": "학습목표",
    "v": "폐 바닥 축상 CT 에서 가로막돔의 부분용적 효과로 생기는 균질 음영을 병변과 구분한다"
   },
   {
    "k": "근거·출처",
    "v": "TCIA LIDC-IDRI series (CC BY 3.0) — author reading (2026-09-14): lung-base slice, right hemidiaphragm dome (liver) occupying the anterior right base, both lower lobes normal, no nodule · Webb WR, Higgins CB. Thoracic Imaging — diaphragm and partial-volume artefacts at the lung bases ## 출처 LIDC-IDRI, The Cancer Imaging Archive (CC BY 3.0) · series …43069436 · Creative Commons Attribution 3.0 Unported · https://www.cancerimagingarchive.net/data-usage-policies-and-restrictions/"
   }
  ],
  "source": "의대_시험지_제작 오픈데이터 영상 세트 / 20260913T201606Z_일일영상_2026-09-14_9units_9q_85b9cadf",
  "vitals": [],
  "labs": [],
  "appendix": null,
  "figureImg": {
   "src": "assets/imaging/imaging-2026-0013.png",
   "caption": "Axial chest CT, lung window, standard display orientation (patient's right on the viewer's left) (The Cancer Imaging Archive, CC BY 3.0; converted from DICOM with windowing only)",
   "alt": "CT 영상"
  },
  "attribution": {
   "dataset": "TCIA LIDC-IDRI (Lung Image Database Consortium)",
   "license": "Creative Commons Attribution 3.0 Unported",
   "license_url": "https://www.cancerimagingarchive.net/data-usage-policies-and-restrictions/",
   "url": "https://nbia.cancerimagingarchive.net/viewer/?series=1.3.6.1.4.1.14519.5.2.1.6279.6001.140642535005388188316143069436",
   "asset_id": "TCIA-LIDC_IDRI-55416288289725",
   "text": "LIDC-IDRI, The Cancer Imaging Archive (CC BY 3.0) · series …43069436"
  },
  "run_id": "20260913T201606Z_일일영상_2026-09-14_9units_9q_85b9cadf",
  "qid": "Q0004"
 },
 {
  "id": "imaging-2026-0012",
  "exam": "imaging",
  "style": "kmle_style",
  "styleLabel": "국시형",
  "subject": "호흡기",
  "subject_file": "호흡기",
  "setSubject": "통합(생식의학·산과 마취·흉부 해부)",
  "subtopic": "흉부 CT 정상 해부 — 세로칸·가로막",
  "type": "흉부 CT 정상 해부 — 세로칸·가로막",
  "modality": "CT",
  "step": "",
  "difficulty": 4,
  "difficultyLabel": "상",
  "created": "2026-09-13",
  "vignette": "67세 여자가 건강검진으로 흉부 CT를 찍었다. 특별한 증상은 없고 흡연력도 없다. 심실 높이의 흉부 CT 축상면(폐창)은 그림과 같다.",
  "question": "척추체의 왼쪽 앞에 접하여 둥근 단면으로 보이는 관 구조물이 가로막을 통과하는 척추 높이는?",
  "options": [
   "제8등뼈(T8)",
   "제10등뼈(T10)",
   "제1허리뼈(L1)",
   "제3허리뼈(L3)",
   "제12등뼈(T12)"
  ],
  "answer": 5,
  "explanationText": "- 정답 핵심: 심실 높이에서 척추체의 왼쪽 앞에 붙어 있는 지름 2~3 cm 의 둥근 관 구조는 하행 흉부대동맥이다(뒤세로칸). 대동맥은 가로막의 두 다리(crura)와 정중활꼴인대 뒤로 지나는 대동맥구멍을 통해 배로 내려가며 그 높이는 제12등뼈다. 식도구멍은 T10, 대정맥구멍은 T8 이다.\n- 원리: 가로막에는 큰 구멍이 셋 있고 각각의 높이가 다르다. <b>대정맥구멍(T8)</b> 은 가로막의 <b>중심널힘줄 안</b>에 있어 숨을 들이쉴 때 오히려 벌어져 정맥 환류를 돕는다. <b>식도구멍(T10)</b> 은 <b>오른쪽 다리(right crus)의 근육섬유가 감싸는</b> 구멍이라 수축할 때 조여 역류를 막는 「생리적 조임근」 역할을 한다. <b>대동맥구멍(T12)</b> 은 엄밀히는 가로막을 「뚫는」 것이 아니라 <b>두 다리와 정중활꼴인대 뒤, 척추체 앞</b>을 지나므로 가로막이 수축해도 대동맥이 눌리지 않는다 — 함께 가슴림프관과 홀정맥이 지난다.<br> <b>왜 T8·T10·T12 인가</b> — 외우는 요령은 「글자 수」다: vena <b>cava</b>(4자·T8 은 8=4×2), <b>oesophagus</b>(10자→T10), <b>aortic hiatus</b>(12자→T12).<br> <b>영상에서 대동맥을 어떻게 알아보나</b> — 축상면에서 하행대동맥은 <b>척추체의 왼쪽 앞</b>에 붙어 위아래 모든 단면에서 같은 자리에 나타나는 <b>둥근 단면</b>이다. 식도는 그보다 <b>오른쪽 앞·정중 가까이</b> 있고 안에 공기가 있을 수 있으며 둥글지 않다. 홀정맥은 <b>척추체 오른쪽 앞</b>의 작은 구조다. 그래서 「왼쪽 앞 · 둥글고 · 크다」 세 가지로 하행대동맥이 확정된다 — 폐창에서는 세로칸이 모두 희게 뭉쳐 보이므로 위치 관계로 읽는다.\n- 비교: <table><thead><tr><th style=\"width:28%\">구조</th><th style=\"width:30%\">축상 CT 에서의 자리</th><th style=\"width:16%\">가로막 통과 높이</th><th>함께 지나는 것</th></tr></thead><tbody> <tr><td><b>하행대동맥(정답 구조)</b></td><td><b>척추체 왼쪽 앞, 둥근 단면, 지름 2~3 cm</b></td><td><b>T12(대동맥구멍)</b></td><td>가슴림프관, 홀정맥</td></tr> <tr><td>식도</td><td>정중~약간 왼쪽, 대동맥의 오른쪽 앞, 납작·공기 가능</td><td>T10(식도구멍)</td><td>앞·뒤 미주신경줄기</td></tr> <tr><td>아래대정맥</td><td>이 높이에는 없음(간 위 짧은 구간만 흉강)</td><td>T8(대정맥구멍)</td><td>오른가로막신경 가지</td></tr> <tr><td>홀정맥</td><td>척추체 오른쪽 앞, 작은 점</td><td>T12(대동맥구멍 또는 오른다리)</td><td>—</td></tr> </tbody></table> <b>가장 가까운 오답은 T10</b> — 영상에서 「척추체 앞의 둥근 것」을 식도로 잘못 읽으면 T10 을 고른다. 식도는 대동맥의 오른쪽 앞에 있고 둥글게 꽉 찬 단면이 아니라는 점, 그리고 이 구조가 <b>왼쪽</b>에 붙어 있다는 점이 갈림길이다.\n- 오답 이유:\n  - ① T8 은 아래대정맥이 중심널힘줄을 지나는 높이다. 아래대정맥은 척추체 오른쪽 앞에 있고 심실 높이의 흉부 단면에는 나타나지 않는다. 이 선지가 정답이 되려면 그림의 구조가 척추 오른쪽 앞의 정맥이어야 한다.\n  - ② T10 은 식도가 오른쪽 다리 섬유 사이로 지나는 높이다. 식도는 대동맥의 오른쪽 앞, 정중 가까이에 있고 둥근 단면이 아니다. 이 선지가 정답이 되려면 그림의 구조가 척추 왼쪽이 아니라 정중 앞의 납작한 관이어야 한다.\n  - ③ L1 은 위창자간막동맥이 대동맥에서 갈라지는 높이이지 대동맥이 가로막을 지나는 높이가 아니다. 이 선지가 정답이 되려면 「가로막 통과」가 아니라 「첫 가지의 기시 높이」를 물어야 한다.\n  - ④ L3 은 아래창자간막동맥의 기시 높이이고 L4 에서 대동맥이 두 온엉덩동맥으로 갈라진다. 이 선지가 정답이 되려면 「대동맥이 갈라지기 직전의 가지」를 물어야 한다.\n- 함정: 폐창에서는 세로칸 구조가 모두 희게 뭉쳐 보인다 — 「척추체 왼쪽 앞의 둥근 단면」이라는 위치 관계 하나로 하행대동맥을 확정한 뒤 높이를 붙인다.\n- 학습목표: 심실 높이 흉부 CT 에서 하행대동맥을 위치로 식별하고 가로막의 대동맥구멍 높이(T12)에 연결한다\n- 근거·출처: TCIA LIDC-IDRI 시리즈(CC BY 3.0) — 작성자 판독(2026-09-14): 심실 높이, 척추체 왼쪽 앞 둥근 하행대동맥, 폐 실질 정상·결절 없음 · Moore Clinically Oriented Anatomy — 가로막 구멍: 대정맥구멍 T8 · 식도구멍 T10 · 대동맥구멍 T12\n\n## 출처\n- LIDC-IDRI, The Cancer Imaging Archive (CC BY 3.0) · series …43069436 · Creative Commons Attribution 3.0 Unported · https://www.cancerimagingarchive.net/data-usage-policies-and-restrictions/",
  "explanationItems": [
   {
    "k": "정답 핵심",
    "v": "심실 높이에서 척추체의 왼쪽 앞에 붙어 있는 지름 2~3 cm 의 둥근 관 구조는 하행 흉부대동맥이다(뒤세로칸). 대동맥은 가로막의 두 다리(crura)와 정중활꼴인대 뒤로 지나는 대동맥구멍을 통해 배로 내려가며 그 높이는 제12등뼈다. 식도구멍은 T10, 대정맥구멍은 T8 이다."
   },
   {
    "k": "원리",
    "v": "가로막에는 큰 구멍이 셋 있고 각각의 높이가 다르다. <b>대정맥구멍(T8)</b> 은 가로막의 <b>중심널힘줄 안</b>에 있어 숨을 들이쉴 때 오히려 벌어져 정맥 환류를 돕는다. <b>식도구멍(T10)</b> 은 <b>오른쪽 다리(right crus)의 근육섬유가 감싸는</b> 구멍이라 수축할 때 조여 역류를 막는 「생리적 조임근」 역할을 한다. <b>대동맥구멍(T12)</b> 은 엄밀히는 가로막을 「뚫는」 것이 아니라 <b>두 다리와 정중활꼴인대 뒤, 척추체 앞</b>을 지나므로 가로막이 수축해도 대동맥이 눌리지 않는다 — 함께 가슴림프관과 홀정맥이 지난다.<br> <b>왜 T8·T10·T12 인가</b> — 외우는 요령은 「글자 수」다: vena <b>cava</b>(4자·T8 은 8=4×2), <b>oesophagus</b>(10자→T10), <b>aortic hiatus</b>(12자→T12).<br> <b>영상에서 대동맥을 어떻게 알아보나</b> — 축상면에서 하행대동맥은 <b>척추체의 왼쪽 앞</b>에 붙어 위아래 모든 단면에서 같은 자리에 나타나는 <b>둥근 단면</b>이다. 식도는 그보다 <b>오른쪽 앞·정중 가까이</b> 있고 안에 공기가 있을 수 있으며 둥글지 않다. 홀정맥은 <b>척추체 오른쪽 앞</b>의 작은 구조다. 그래서 「왼쪽 앞 · 둥글고 · 크다」 세 가지로 하행대동맥이 확정된다 — 폐창에서는 세로칸이 모두 희게 뭉쳐 보이므로 위치 관계로 읽는다."
   },
   {
    "k": "비교",
    "v": "<table><thead><tr><th style=\"width:28%\">구조</th><th style=\"width:30%\">축상 CT 에서의 자리</th><th style=\"width:16%\">가로막 통과 높이</th><th>함께 지나는 것</th></tr></thead><tbody> <tr><td><b>하행대동맥(정답 구조)</b></td><td><b>척추체 왼쪽 앞, 둥근 단면, 지름 2~3 cm</b></td><td><b>T12(대동맥구멍)</b></td><td>가슴림프관, 홀정맥</td></tr> <tr><td>식도</td><td>정중~약간 왼쪽, 대동맥의 오른쪽 앞, 납작·공기 가능</td><td>T10(식도구멍)</td><td>앞·뒤 미주신경줄기</td></tr> <tr><td>아래대정맥</td><td>이 높이에는 없음(간 위 짧은 구간만 흉강)</td><td>T8(대정맥구멍)</td><td>오른가로막신경 가지</td></tr> <tr><td>홀정맥</td><td>척추체 오른쪽 앞, 작은 점</td><td>T12(대동맥구멍 또는 오른다리)</td><td>—</td></tr> </tbody></table> <b>가장 가까운 오답은 T10</b> — 영상에서 「척추체 앞의 둥근 것」을 식도로 잘못 읽으면 T10 을 고른다. 식도는 대동맥의 오른쪽 앞에 있고 둥글게 꽉 찬 단면이 아니라는 점, 그리고 이 구조가 <b>왼쪽</b>에 붙어 있다는 점이 갈림길이다."
   },
   {
    "k": "오답 이유",
    "v": "① T8 은 아래대정맥이 중심널힘줄을 지나는 높이다. 아래대정맥은 척추체 오른쪽 앞에 있고 심실 높이의 흉부 단면에는 나타나지 않는다. 이 선지가 정답이 되려면 그림의 구조가 척추 오른쪽 앞의 정맥이어야 한다.\n② T10 은 식도가 오른쪽 다리 섬유 사이로 지나는 높이다. 식도는 대동맥의 오른쪽 앞, 정중 가까이에 있고 둥근 단면이 아니다. 이 선지가 정답이 되려면 그림의 구조가 척추 왼쪽이 아니라 정중 앞의 납작한 관이어야 한다.\n③ L1 은 위창자간막동맥이 대동맥에서 갈라지는 높이이지 대동맥이 가로막을 지나는 높이가 아니다. 이 선지가 정답이 되려면 「가로막 통과」가 아니라 「첫 가지의 기시 높이」를 물어야 한다.\n④ L3 은 아래창자간막동맥의 기시 높이이고 L4 에서 대동맥이 두 온엉덩동맥으로 갈라진다. 이 선지가 정답이 되려면 「대동맥이 갈라지기 직전의 가지」를 물어야 한다."
   },
   {
    "k": "함정",
    "v": "폐창에서는 세로칸 구조가 모두 희게 뭉쳐 보인다 — 「척추체 왼쪽 앞의 둥근 단면」이라는 위치 관계 하나로 하행대동맥을 확정한 뒤 높이를 붙인다."
   },
   {
    "k": "학습목표",
    "v": "심실 높이 흉부 CT 에서 하행대동맥을 위치로 식별하고 가로막의 대동맥구멍 높이(T12)에 연결한다"
   },
   {
    "k": "근거·출처",
    "v": "TCIA LIDC-IDRI 시리즈(CC BY 3.0) — 작성자 판독(2026-09-14): 심실 높이, 척추체 왼쪽 앞 둥근 하행대동맥, 폐 실질 정상·결절 없음 · Moore Clinically Oriented Anatomy — 가로막 구멍: 대정맥구멍 T8 · 식도구멍 T10 · 대동맥구멍 T12 ## 출처 LIDC-IDRI, The Cancer Imaging Archive (CC BY 3.0) · series …43069436 · Creative Commons Attribution 3.0 Unported · https://www.cancerimagingarchive.net/data-usage-policies-and-restrictions/"
   }
  ],
  "source": "의대_시험지_제작 오픈데이터 영상 세트 / 20260913T201606Z_일일영상_2026-09-14_9units_9q_85b9cadf",
  "vitals": [],
  "labs": [],
  "appendix": null,
  "figureImg": {
   "src": "assets/imaging/imaging-2026-0012.png",
   "caption": "흉부 CT 축상면, 폐창(lung window) — 표준 표시 방향(환자의 오른쪽이 그림의 왼쪽) (The Cancer Imaging Archive, CC BY 3.0 — DICOM 원본을 창 설정 외 가공 없이 변환)",
   "alt": "CT 영상"
  },
  "attribution": {
   "dataset": "TCIA LIDC-IDRI (Lung Image Database Consortium)",
   "license": "Creative Commons Attribution 3.0 Unported",
   "license_url": "https://www.cancerimagingarchive.net/data-usage-policies-and-restrictions/",
   "url": "https://nbia.cancerimagingarchive.net/viewer/?series=1.3.6.1.4.1.14519.5.2.1.6279.6001.140642535005388188316143069436",
   "asset_id": "TCIA-LIDC_IDRI-80831100765610",
   "text": "LIDC-IDRI, The Cancer Imaging Archive (CC BY 3.0) · series …43069436"
  },
  "run_id": "20260913T201606Z_일일영상_2026-09-14_9units_9q_85b9cadf",
  "qid": "Q0003"
 },
 {
  "id": "imaging-2026-0011",
  "exam": "imaging",
  "style": "usmle_style",
  "styleLabel": "USMLE형",
  "subject": "순환기",
  "subject_file": "순환기",
  "setSubject": "통합(생식의학·산과 마취·흉부 해부)",
  "subtopic": "심전도 판독 — 허혈·전기축",
  "type": "심전도 판독 — 허혈·전기축",
  "modality": "ECG",
  "step": "Step 2",
  "difficulty": 3,
  "difficultyLabel": "중",
  "created": "2026-09-13",
  "vignette": "A 25-year-old man comes to the clinic for a pre-participation sports examination. He has no symptoms and no history of syncope or chest pain. He is tall and thin. Blood pressure is 118/72 mm Hg and pulse is 72/min and regular. A 12-lead electrocardiogram is shown.",
  "question": "Which of the following best describes the mean QRS axis in the frontal plane?",
  "options": [
   "Right axis deviation (+90° to +180°)",
   "Normal axis (−30° to +90°)",
   "Left axis deviation (−30° to −90°)",
   "Extreme (northwest) axis (−90° to −180°)",
   "Indeterminate axis (isoelectric in all limb leads)"
  ],
  "answer": 1,
  "explanationText": "- 정답 핵심: In lead I the QRS is predominantly negative (small r, deep S); in lead aVF and lead III it is predominantly positive (qR). A negative lead I with a positive aVF places the mean QRS vector between +90° and +180° — right axis deviation. The QRS is narrow and the rhythm is sinus, so this is an isolated axis finding.\n- 원리: The frontal-plane axis is the <b>direction of the mean QRS vector</b>, and each limb lead is a <b>projection of that vector onto the lead's own axis</b>: lead I looks from the left (0°), lead aVF from the feet (+90°). A vector pointing toward a lead writes a positive deflection; a vector pointing away writes a negative one.<br> <b>Why two leads are enough</b> — leads I and aVF are perpendicular. Positive in both → the vector lies in the lower-left quadrant (0° to +90°, normal). <b>Negative in I but positive in aVF</b> → the vector points down and to the right, i.e. <b>+90° to +180°: right axis deviation</b>. Positive in I, negative in aVF → left axis (0° to −90°, abnormal beyond −30°). Negative in both → extreme axis.<br> <b>Why it happens</b> — the vector swings toward the mass that depolarizes last or most. Right axis deviation appears with a vertically positioned heart in a tall thin young adult, with right ventricular hypertrophy (pulmonary hypertension, congenital shunts), with lateral wall infarction, and with <b>left posterior fascicular block</b> (the posteroinferior fascicle fails, so the inferior wall depolarizes late and the vector tips inferiorly and rightward — a diagnosis made only after the other causes are excluded).<br> <b>Reading order</b> — decide the polarity of I, then of aVF, then refine with the most isoelectric limb lead (the axis is perpendicular to it).\n- 비교: <table><thead><tr><th style=\"width:30%\">Axis</th><th style=\"width:22%\">Lead I</th><th style=\"width:22%\">Lead aVF</th><th>This tracing</th></tr></thead><tbody> <tr><td><b>Right axis deviation (answer)</b></td><td><b>negative (rS)</b></td><td><b>positive (qR)</b></td><td>I is net negative, III/aVF strongly positive → ≈ +120°</td></tr> <tr><td>Normal axis</td><td>positive</td><td>positive (or aVF negative with II positive, −30° to 0°)</td><td>would need a dominant R in lead I</td></tr> <tr><td>Left axis deviation</td><td>positive</td><td>negative, and lead II negative</td><td>opposite of this tracing</td></tr> <tr><td>Extreme axis</td><td>negative</td><td>negative</td><td>aVF here is clearly positive</td></tr> </tbody></table> The <b>closest wrong answer is the normal axis</b>: in a tall thin 25-year-old a vertical axis near +90° is common, and only the <b>negative net area of lead I</b> pushes this tracing past +90°. Measure the r and S of lead I with a ruler instead of eyeballing.\n- 오답 이유:\n  - (B) A normal axis requires a net positive QRS in lead I. Here lead I is a small r followed by a deep S, so the net area is negative. This option would be correct only if the R wave in lead I exceeded its S wave.\n  - (C) Left axis deviation needs a positive lead I with negative leads II and aVF, the mirror image of this tracing. This option would be correct only if aVF and II were predominantly negative.\n  - (D) An extreme (northwest) axis needs negative deflections in both lead I and lead aVF. Lead aVF here is strongly positive. This option would be correct only if aVF were also net negative.\n  - (E) An indeterminate axis means every limb lead is nearly isoelectric (equal positive and negative area). Leads III and aVF here are clearly positive and lead I clearly negative. This option would be correct only if no limb lead had a dominant deflection.\n- 함정: Do not decide the axis from lead II alone — lead II is positive in both the normal range and in right axis deviation. The discriminating lead is lead I.\n- 학습목표: 사지유도 I·aVF 의 QRS 극성으로 평균 QRS 전기축을 결정한다\n- 근거·출처: PTB-XL record label LPFB (two-cardiologist validated) — implies right axis deviation with narrow QRS · 작성자 판독(2026-09-14): I rS(음성), III·aVF qR(양성), QRS ≈0.09 s → 축 ≈ +120° · AHA/ACCF/HRS Recommendations for the Standardization and Interpretation of the ECG, Part III: Intraventricular Conduction Disturbances (2009)\n\n## 출처\n- PTB-XL ECG dataset v1.0.3 (PhysioNet, CC BY 4.0) · record 16116 · Creative Commons Attribution 4.0 International · https://physionet.org/content/ptb-xl/1.0.3/LICENSE.txt",
  "explanationItems": [
   {
    "k": "정답 핵심",
    "v": "In lead I the QRS is predominantly negative (small r, deep S); in lead aVF and lead III it is predominantly positive (qR). A negative lead I with a positive aVF places the mean QRS vector between +90° and +180° — right axis deviation. The QRS is narrow and the rhythm is sinus, so this is an isolated axis finding."
   },
   {
    "k": "원리",
    "v": "The frontal-plane axis is the <b>direction of the mean QRS vector</b>, and each limb lead is a <b>projection of that vector onto the lead's own axis</b>: lead I looks from the left (0°), lead aVF from the feet (+90°). A vector pointing toward a lead writes a positive deflection; a vector pointing away writes a negative one.<br> <b>Why two leads are enough</b> — leads I and aVF are perpendicular. Positive in both → the vector lies in the lower-left quadrant (0° to +90°, normal). <b>Negative in I but positive in aVF</b> → the vector points down and to the right, i.e. <b>+90° to +180°: right axis deviation</b>. Positive in I, negative in aVF → left axis (0° to −90°, abnormal beyond −30°). Negative in both → extreme axis.<br> <b>Why it happens</b> — the vector swings toward the mass that depolarizes last or most. Right axis deviation appears with a vertically positioned heart in a tall thin young adult, with right ventricular hypertrophy (pulmonary hypertension, congenital shunts), with lateral wall infarction, and with <b>left posterior fascicular block</b> (the posteroinferior fascicle fails, so the inferior wall depolarizes late and the vector tips inferiorly and rightward — a diagnosis made only after the other causes are excluded).<br> <b>Reading order</b> — decide the polarity of I, then of aVF, then refine with the most isoelectric limb lead (the axis is perpendicular to it)."
   },
   {
    "k": "비교",
    "v": "<table><thead><tr><th style=\"width:30%\">Axis</th><th style=\"width:22%\">Lead I</th><th style=\"width:22%\">Lead aVF</th><th>This tracing</th></tr></thead><tbody> <tr><td><b>Right axis deviation (answer)</b></td><td><b>negative (rS)</b></td><td><b>positive (qR)</b></td><td>I is net negative, III/aVF strongly positive → ≈ +120°</td></tr> <tr><td>Normal axis</td><td>positive</td><td>positive (or aVF negative with II positive, −30° to 0°)</td><td>would need a dominant R in lead I</td></tr> <tr><td>Left axis deviation</td><td>positive</td><td>negative, and lead II negative</td><td>opposite of this tracing</td></tr> <tr><td>Extreme axis</td><td>negative</td><td>negative</td><td>aVF here is clearly positive</td></tr> </tbody></table> The <b>closest wrong answer is the normal axis</b>: in a tall thin 25-year-old a vertical axis near +90° is common, and only the <b>negative net area of lead I</b> pushes this tracing past +90°. Measure the r and S of lead I with a ruler instead of eyeballing."
   },
   {
    "k": "오답 이유",
    "v": "(B) A normal axis requires a net positive QRS in lead I. Here lead I is a small r followed by a deep S, so the net area is negative. This option would be correct only if the R wave in lead I exceeded its S wave.\n(C) Left axis deviation needs a positive lead I with negative leads II and aVF, the mirror image of this tracing. This option would be correct only if aVF and II were predominantly negative.\n(D) An extreme (northwest) axis needs negative deflections in both lead I and lead aVF. Lead aVF here is strongly positive. This option would be correct only if aVF were also net negative.\n(E) An indeterminate axis means every limb lead is nearly isoelectric (equal positive and negative area). Leads III and aVF here are clearly positive and lead I clearly negative. This option would be correct only if no limb lead had a dominant deflection."
   },
   {
    "k": "함정",
    "v": "Do not decide the axis from lead II alone — lead II is positive in both the normal range and in right axis deviation. The discriminating lead is lead I."
   },
   {
    "k": "학습목표",
    "v": "사지유도 I·aVF 의 QRS 극성으로 평균 QRS 전기축을 결정한다"
   },
   {
    "k": "근거·출처",
    "v": "PTB-XL record label LPFB (two-cardiologist validated) — implies right axis deviation with narrow QRS · 작성자 판독(2026-09-14): I rS(음성), III·aVF qR(양성), QRS ≈0.09 s → 축 ≈ +120° · AHA/ACCF/HRS Recommendations for the Standardization and Interpretation of the ECG, Part III: Intraventricular Conduction Disturbances (2009) ## 출처 PTB-XL ECG dataset v1.0.3 (PhysioNet, CC BY 4.0) · record 16116 · Creative Commons Attribution 4.0 International · https://physionet.org/content/ptb-xl/1.0.3/LICENSE.txt"
   }
  ],
  "source": "의대_시험지_제작 오픈데이터 영상 세트 / 20260913T201606Z_일일영상_2026-09-14_9units_9q_85b9cadf",
  "vitals": [],
  "labs": [],
  "appendix": null,
  "figureImg": {
   "src": "assets/imaging/imaging-2026-0011.png",
   "caption": "12-lead ECG, 25 mm/s, 10 mm/mV, 3×4 + lead II rhythm strip (PTB-XL, PhysioNet, CC BY 4.0; raw signal, no filtering)",
   "alt": "ECG 영상"
  },
  "attribution": {
   "dataset": "PTB-XL, a large publicly available electrocardiography dataset",
   "license": "Creative Commons Attribution 4.0 International",
   "license_url": "https://physionet.org/content/ptb-xl/1.0.3/LICENSE.txt",
   "url": "https://physionet.org/content/ptb-xl/1.0.3/records500/16000/#files-panel",
   "asset_id": "PTBXL-16116",
   "text": "PTB-XL ECG dataset v1.0.3 (PhysioNet, CC BY 4.0) · record 16116"
  },
  "run_id": "20260913T201606Z_일일영상_2026-09-14_9units_9q_85b9cadf",
  "qid": "Q0002"
 },
 {
  "id": "imaging-2026-0010",
  "exam": "imaging",
  "style": "kmle_style",
  "styleLabel": "국시형",
  "subject": "순환기",
  "subject_file": "순환기",
  "setSubject": "통합(생식의학·산과 마취·흉부 해부)",
  "subtopic": "심전도 판독 — 허혈·전기축",
  "type": "심전도 판독 — 허혈·전기축",
  "modality": "ECG",
  "step": "",
  "difficulty": 3,
  "difficultyLabel": "중",
  "created": "2026-09-13",
  "vignette": "63세 남자가 2주 전부터 계단을 오를 때 가슴이 조이는 느낌이 생겨 왔다. 쉬면 5분 안에 사라지고 지금은 통증이 없다. 고혈압으로 약을 먹고 있다. 혈압 138/86 mmHg, 맥박 분당 66회로 규칙적이다. 안정 시 12유도 심전도는 그림과 같다.",
  "question": "심전도 소견은?",
  "options": [
   "불규칙한 RR 간격과 P파 소실",
   "II·III·aVF·V6 유도의 ST 분절 하강과 III·aVF 유도의 T파 역위",
   "II·III·aVF 유도의 ST 분절 상승과 aVL 유도의 상반성 하강",
   "V1–V3 유도의 ST 분절 상승과 병적 Q파",
   "QRS 폭 0.12초 이상의 우각차단"
  ],
  "answer": 2,
  "explanationText": "- 정답 핵심: 모든 QRS 앞에 P파가 일정한 PR 간격으로 있고 RR 이 규칙적인 동율동(약 66회/분)이다. 하벽 유도(II·III·aVF)와 V6 에서 ST 분절이 기준선 아래로 내려가 있고, III·aVF 의 T파는 뒤집혀 있다. ST 상승·병적 Q파·넓은 QRS 는 없다. 노작성 흉통 병력과 함께 하벽·측벽의 심근허혈이 의심되는 소견이다.\n- 원리: ST 분절은 <b>심실 탈분극이 끝나고 재분극이 시작되기 전의 등전위 구간</b>이다. 심내막하층이 허혈에 빠지면 그 부위 세포의 안정막전위와 활동전위 지속시간이 바뀌어 <b>손상전류(injury current)</b> 가 생기고, 심내막하 허혈에서는 이 전류가 <b>심외막 쪽 전극에서 멀어지는 방향</b>이므로 그 유도에서 <b>ST 분절이 내려간다</b>. 반대로 벽 전층이 허혈이면 손상전류 방향이 전극을 향해 <b>ST 가 올라간다</b> — 그래서 ST 하강은 「심내막하 허혈」, ST 상승은 「전층 손상(STEMI)」로 읽는다.<br> <b>왜 하벽·측벽으로 묶는가</b> — II·III·aVF 는 심장의 아래쪽(가로막면)을, V5·V6 는 왼쪽 옆면을 본다. 이 기록은 II·III·aVF 와 V6 에서 함께 ST 가 내려가고 III·aVF 의 T파가 뒤집혀 있어 <b>하측벽 심내막하 허혈</b>에 합당하다. 다만 <b>ST 하강은 ST 상승만큼 혈관을 정확히 가리키지 못한다</b>(전벽 STEMI 의 상반성 하강, 좌심실비대의 부하 양상과도 겹친다) — 그래서 「소견」을 먼저 정확히 읽고, 진단은 병력(노작 시 흉통, 안정 시 소실)과 함께 붙인다.<br> <b>판독 순서</b> — 율동(P–QRS 관계·RR 규칙성) → 축 → 간격(PR·QRS·QT) → ST·T. 이 기록은 율동·간격이 정상이라 「ST·T 이상」만 남는다.\n- 비교: <table><thead><tr><th style=\"width:28%\">소견</th><th style=\"width:36%\">이 기록에서 확인할 자리</th><th>의미</th></tr></thead><tbody> <tr><td><b>II·III·aVF·V6 ST 하강 + III·aVF T 역위(정답)</b></td><td>하벽 유도 세 개와 V6 의 ST 가 기준선(PR 분절) 아래, III·aVF 의 T 가 아래로</td><td>하측벽 심내막하 허혈 의심 — 안정협심증 병력과 맞음</td></tr> <tr><td>II·III·aVF ST 상승 + aVL 상반성 하강</td><td>ST 가 <b>올라가야</b> 하고 aVL 만 내려가야 함 — 여기선 하벽 ST 가 내려감</td><td>하벽 STEMI(우관상동맥) — 응급 재관류</td></tr> <tr><td>V1–V3 ST 상승 + Q파</td><td>V1–V3 는 깊은 S 뒤 T 가 크게 서 있을 뿐 ST 는 기준선</td><td>전중격 STEMI</td></tr> <tr><td>우각차단</td><td>QRS 폭 ≈0.09 s, V1 rSR′ 없음</td><td>전도장애</td></tr> </tbody></table> <b>가장 가까운 오답은 ②</b> — 같은 하벽 유도를 가리키지만 ST 의 <b>방향</b>이 반대다. 「하강」이면 심내막하 허혈·비STEMI 쪽, 「상승」이면 STEMI 로 처치 자체가 갈리므로 기준선(PR 분절)과 J점을 대고 방향부터 정한다.\n- 오답 이유:\n  - ① 심방세동은 RR 간격이 완전히 불규칙하고 P파 대신 세동파가 보인다. 이 기록은 RR 이 일정하고 모든 QRS 앞에 P파가 있다. 이 선지가 정답이 되려면 리듬 스트립에서 RR 이 제각각이고 P파가 없어야 한다.\n  - ③ 하벽 STEMI 는 II·III·aVF 의 ST 가 기준선 위로 올라가고 aVL 이 거울처럼 내려간다. 이 기록은 하벽 ST 가 아래로 내려가 있어 방향이 반대다. 이 선지가 정답이 되려면 J점이 기준선 위 ≥1 mm 에 있어야 한다.\n  - ④ V1–V3 에는 깊은 S파 뒤에 T파가 크게 서 있을 뿐 ST 상승도 병적 Q파(폭 ≥0.04 s·깊이 R의 1/4)도 없다. 이 선지가 정답이 되려면 V1–V3 의 J점 상승과 Q파가 실제로 보여야 한다.\n  - ⑤ 우각차단은 QRS 폭이 0.12 s 이상이고 V1 에 rSR′, V6 에 넓은 S 가 있어야 한다. 이 기록의 QRS 는 작은 칸 2~2.5칸(≈0.09 s)으로 좁다. 이 선지가 정답이 되려면 QRS 가 큰 칸 3칸 이상으로 넓어야 한다.\n- 함정: V1–V3 의 크고 뾰족한 T파와 깊은 S 에 눈이 가면 「전벽」으로 착각한다 — ST 는 기준선에 있다. 하벽 유도 셋을 한꺼번에 보고 PR 분절과 J점을 대야 하강이 보인다.\n- 학습목표: 노작성 흉통 환자의 안정 시 심전도에서 하벽·측벽 유도의 ST 분절 하강과 T파 역위를 읽는다\n- 근거·출처: PTB-XL 기록 라벨 ISCIN(2인 심장내과 검증) · 판독문: ST depressed II·III·aVF·V6, T inverted III·aVF · 작성자 판독(2026-09-14): 동율동 ≈66/분, QRS ≈0.09 s, 하벽·V6 ST 하강, III·aVF T 역위 · Fourth Universal Definition of Myocardial Infarction (2018) — ST 하강·T 역위의 허혈 판정 기준\n\n## 출처\n- PTB-XL ECG dataset v1.0.3 (PhysioNet, CC BY 4.0) · record 1175 · Creative Commons Attribution 4.0 International · https://physionet.org/content/ptb-xl/1.0.3/LICENSE.txt",
  "explanationItems": [
   {
    "k": "정답 핵심",
    "v": "모든 QRS 앞에 P파가 일정한 PR 간격으로 있고 RR 이 규칙적인 동율동(약 66회/분)이다. 하벽 유도(II·III·aVF)와 V6 에서 ST 분절이 기준선 아래로 내려가 있고, III·aVF 의 T파는 뒤집혀 있다. ST 상승·병적 Q파·넓은 QRS 는 없다. 노작성 흉통 병력과 함께 하벽·측벽의 심근허혈이 의심되는 소견이다."
   },
   {
    "k": "원리",
    "v": "ST 분절은 <b>심실 탈분극이 끝나고 재분극이 시작되기 전의 등전위 구간</b>이다. 심내막하층이 허혈에 빠지면 그 부위 세포의 안정막전위와 활동전위 지속시간이 바뀌어 <b>손상전류(injury current)</b> 가 생기고, 심내막하 허혈에서는 이 전류가 <b>심외막 쪽 전극에서 멀어지는 방향</b>이므로 그 유도에서 <b>ST 분절이 내려간다</b>. 반대로 벽 전층이 허혈이면 손상전류 방향이 전극을 향해 <b>ST 가 올라간다</b> — 그래서 ST 하강은 「심내막하 허혈」, ST 상승은 「전층 손상(STEMI)」로 읽는다.<br> <b>왜 하벽·측벽으로 묶는가</b> — II·III·aVF 는 심장의 아래쪽(가로막면)을, V5·V6 는 왼쪽 옆면을 본다. 이 기록은 II·III·aVF 와 V6 에서 함께 ST 가 내려가고 III·aVF 의 T파가 뒤집혀 있어 <b>하측벽 심내막하 허혈</b>에 합당하다. 다만 <b>ST 하강은 ST 상승만큼 혈관을 정확히 가리키지 못한다</b>(전벽 STEMI 의 상반성 하강, 좌심실비대의 부하 양상과도 겹친다) — 그래서 「소견」을 먼저 정확히 읽고, 진단은 병력(노작 시 흉통, 안정 시 소실)과 함께 붙인다.<br> <b>판독 순서</b> — 율동(P–QRS 관계·RR 규칙성) → 축 → 간격(PR·QRS·QT) → ST·T. 이 기록은 율동·간격이 정상이라 「ST·T 이상」만 남는다."
   },
   {
    "k": "비교",
    "v": "<table><thead><tr><th style=\"width:28%\">소견</th><th style=\"width:36%\">이 기록에서 확인할 자리</th><th>의미</th></tr></thead><tbody> <tr><td><b>II·III·aVF·V6 ST 하강 + III·aVF T 역위(정답)</b></td><td>하벽 유도 세 개와 V6 의 ST 가 기준선(PR 분절) 아래, III·aVF 의 T 가 아래로</td><td>하측벽 심내막하 허혈 의심 — 안정협심증 병력과 맞음</td></tr> <tr><td>II·III·aVF ST 상승 + aVL 상반성 하강</td><td>ST 가 <b>올라가야</b> 하고 aVL 만 내려가야 함 — 여기선 하벽 ST 가 내려감</td><td>하벽 STEMI(우관상동맥) — 응급 재관류</td></tr> <tr><td>V1–V3 ST 상승 + Q파</td><td>V1–V3 는 깊은 S 뒤 T 가 크게 서 있을 뿐 ST 는 기준선</td><td>전중격 STEMI</td></tr> <tr><td>우각차단</td><td>QRS 폭 ≈0.09 s, V1 rSR′ 없음</td><td>전도장애</td></tr> </tbody></table> <b>가장 가까운 오답은 ②</b> — 같은 하벽 유도를 가리키지만 ST 의 <b>방향</b>이 반대다. 「하강」이면 심내막하 허혈·비STEMI 쪽, 「상승」이면 STEMI 로 처치 자체가 갈리므로 기준선(PR 분절)과 J점을 대고 방향부터 정한다."
   },
   {
    "k": "오답 이유",
    "v": "① 심방세동은 RR 간격이 완전히 불규칙하고 P파 대신 세동파가 보인다. 이 기록은 RR 이 일정하고 모든 QRS 앞에 P파가 있다. 이 선지가 정답이 되려면 리듬 스트립에서 RR 이 제각각이고 P파가 없어야 한다.\n③ 하벽 STEMI 는 II·III·aVF 의 ST 가 기준선 위로 올라가고 aVL 이 거울처럼 내려간다. 이 기록은 하벽 ST 가 아래로 내려가 있어 방향이 반대다. 이 선지가 정답이 되려면 J점이 기준선 위 ≥1 mm 에 있어야 한다.\n④ V1–V3 에는 깊은 S파 뒤에 T파가 크게 서 있을 뿐 ST 상승도 병적 Q파(폭 ≥0.04 s·깊이 R의 1/4)도 없다. 이 선지가 정답이 되려면 V1–V3 의 J점 상승과 Q파가 실제로 보여야 한다.\n⑤ 우각차단은 QRS 폭이 0.12 s 이상이고 V1 에 rSR′, V6 에 넓은 S 가 있어야 한다. 이 기록의 QRS 는 작은 칸 2~2.5칸(≈0.09 s)으로 좁다. 이 선지가 정답이 되려면 QRS 가 큰 칸 3칸 이상으로 넓어야 한다."
   },
   {
    "k": "함정",
    "v": "V1–V3 의 크고 뾰족한 T파와 깊은 S 에 눈이 가면 「전벽」으로 착각한다 — ST 는 기준선에 있다. 하벽 유도 셋을 한꺼번에 보고 PR 분절과 J점을 대야 하강이 보인다."
   },
   {
    "k": "학습목표",
    "v": "노작성 흉통 환자의 안정 시 심전도에서 하벽·측벽 유도의 ST 분절 하강과 T파 역위를 읽는다"
   },
   {
    "k": "근거·출처",
    "v": "PTB-XL 기록 라벨 ISCIN(2인 심장내과 검증) · 판독문: ST depressed II·III·aVF·V6, T inverted III·aVF · 작성자 판독(2026-09-14): 동율동 ≈66/분, QRS ≈0.09 s, 하벽·V6 ST 하강, III·aVF T 역위 · Fourth Universal Definition of Myocardial Infarction (2018) — ST 하강·T 역위의 허혈 판정 기준 ## 출처 PTB-XL ECG dataset v1.0.3 (PhysioNet, CC BY 4.0) · record 1175 · Creative Commons Attribution 4.0 International · https://physionet.org/content/ptb-xl/1.0.3/LICENSE.txt"
   }
  ],
  "source": "의대_시험지_제작 오픈데이터 영상 세트 / 20260913T201606Z_일일영상_2026-09-14_9units_9q_85b9cadf",
  "vitals": [],
  "labs": [],
  "appendix": null,
  "figureImg": {
   "src": "assets/imaging/imaging-2026-0010.png",
   "caption": "12유도 심전도, 25 mm/s · 10 mm/mV, 3×4 + II 리듬 스트립 (PTB-XL ECG dataset, PhysioNet, CC BY 4.0 — 원신호 그대로 작도)",
   "alt": "ECG 영상"
  },
  "attribution": {
   "dataset": "PTB-XL, a large publicly available electrocardiography dataset",
   "license": "Creative Commons Attribution 4.0 International",
   "license_url": "https://physionet.org/content/ptb-xl/1.0.3/LICENSE.txt",
   "url": "https://physionet.org/content/ptb-xl/1.0.3/records500/01000/#files-panel",
   "asset_id": "PTBXL-01175",
   "text": "PTB-XL ECG dataset v1.0.3 (PhysioNet, CC BY 4.0) · record 1175"
  },
  "run_id": "20260913T201606Z_일일영상_2026-09-14_9units_9q_85b9cadf",
  "qid": "Q0001"
 },
 {
  "id": "imaging-2026-0006",
  "exam": "imaging",
  "style": "usmle_style",
  "styleLabel": "USMLE형",
  "subject": "산부인과",
  "subject_file": "산부인과",
  "setSubject": "통합(생식의학·응급·마취)",
  "subtopic": "산과 — 분만 중 태아감시·산과 마취",
  "type": "산과 — 분만 중 태아감시·산과 마취",
  "modality": "CTG",
  "step": "Step 2",
  "difficulty": 4,
  "difficultyLabel": "상",
  "created": "2026-09-13",
  "vignette": "A 37-year-old woman, para 1, at 41 weeks' gestation is in labor with continuous electronic fetal monitoring. The tracing from minutes 40 to 50 of monitoring is shown.",
  "question": "Which of the following best describes the change in fetal heart rate between minutes 42 and 44?",
  "options": [
   "Sinusoidal pattern",
   "Prolonged deceleration",
   "Variable deceleration",
   "Late deceleration",
   "Early deceleration"
  ],
  "answer": 2,
  "explanationText": "- 정답 핵심: Baseline is about 150/min (minutes 46–50). The heart rate leaves baseline at about minute 42, falls to a nadir near 75/min, and does not return until about minute 44.3 — a decrease of ≥15/min lasting ≥2 minutes but <10 minutes, which is a prolonged deceleration (NICHD).\n- 원리: NICHD 분류에서 감속의 이름은 <b>모양이 아니라 「기저선을 떠나 돌아올 때까지의 시간」과 「시작 방식(급격/완만)」</b>으로 정한다. <b>기저선</b>은 감속·가속을 뺀 10분 구간에서 가장 흔한 값으로, 이 기록에서는 46~50분의 <b>약 150/min</b> 이다.<br> <b>왜 지속 감속인가</b> — 42.0분에 기저선을 떠나 <b>최저 약 75/min</b> 까지 떨어졌다가 <b>44.3분에야 돌아온다</b>. 감소 폭 ≥15/min 이고 지속시간이 <b>2분 이상 10분 미만</b>이므로 정의상 <b>prolonged deceleration</b> 이다. 10분을 넘으면 「기저선 변화」로 부른다.<br> <b>왜 2분이 경계인가</b> — 변이 감속의 기전은 <b>제대 압박 → 압수용체 반사 → 미주신경 긴장</b>으로, 압박이 풀리면 15초~2분 안에 회복된다. 2분을 넘게 돌아오지 못하면 <b>반사가 아니라 저산소증으로 인한 심근 억제</b>가 의심되는 시간대로 들어간다. 그래서 2분이 이름을 바꾸는 선이다.<br> <b>그다음 판단</b> — 지속 감속은 <b>2군(indeterminate)</b> 이고, 원인(자궁 과자극·저혈압·제대 탈출·태반 조기박리)을 찾아 <b>체위 변경·옥시토신 중단·수액·산소</b>로 소생 조치를 한다. <b>세로 1분선으로 시간을 세는 것</b>이 판독의 시작이다.\n- 비교: <table><thead><tr><th style=\"width:24%\">감속</th><th style=\"width:22%\">시작 방식</th><th style=\"width:22%\">지속</th><th>수축과의 관계 · 기전</th></tr></thead><tbody> <tr><td><b>지속 감속(정답)</b></td><td>급격 또는 완만</td><td><b>≥2분 ~ &lt;10분</b></td><td>수축과 무관해도 됨 · 저산소·제대압박 지속</td></tr> <tr><td>변이 감속</td><td><b>급격</b>(최저까지 &lt;30초)</td><td><b>15초 ~ &lt;2분</b></td><td>수축과 시점 불규칙 · 제대 압박 반사</td></tr> <tr><td>후기 감속</td><td>완만(≥30초)</td><td>수축 길이만큼</td><td><b>최저점이 수축 정점 뒤</b> · 자궁태반 관류 부전</td></tr> <tr><td>조기 감속</td><td>완만</td><td>수축 길이만큼</td><td><b>최저점이 수축 정점과 일치</b> · 아두 압박</td></tr> <tr><td>정현파형</td><td>—</td><td>≥20분</td><td>3~5 cycles/min 매끈한 사인파 · 태아 빈혈</td></tr> </tbody></table> <b>가장 가까운 오답은 ③ 변이 감속</b> — 모양이 급격해 보이면 변이 감속으로 부르기 쉽지만, <b>2.3분</b>이라는 시간이 이름을 바꾼다. 「급격 + 2분 미만 = 변이, 2분 이상 = 지속」이 경계다.\n- 오답 이유:\n  - (A) 정현파형은 3~5 cycles/min 의 매끈한 사인파가 20분 이상 이어지고 기저선 변이도가 사라진 상태로, 태아 빈혈·저산소를 뜻한다. 이 기록은 한 번의 큰 하강이다. 이 선지가 정답이 되려면 규칙적 파동이 20분 넘게 반복돼야 한다.\n  - (C) 변이 감속은 급격히 떨어지지만 15초에서 2분 미만에 회복하는 제대 압박 반사다. 이 감속은 2.3분 이어져 정의를 넘는다. 이 선지가 정답이 되려면 44분 전에 기저선으로 돌아왔어야 한다.\n  - (D) 후기 감속은 30초 이상 완만하게 내려가고 최저점이 수축 정점 뒤에 오며 수축마다 반복된다. 여기서는 하강이 수축 상승보다 먼저 시작하고 반복도 없다. 이 선지가 정답이 되려면 수축 정점 뒤로 밀린 최저점이 여러 수축에서 반복돼야 한다.\n  - (E) 조기 감속은 수축의 거울상처럼 얕고 완만하며 최저점이 수축 정점과 일치하는 아두 압박 소견이다. 75/min 까지 떨어지는 2분 넘는 하강은 그 범주가 아니다. 이 선지가 정답이 되려면 얕은 하강의 최저점이 수축 정점과 겹쳐야 한다.\n- 함정: 감속 이름은 모양보다 「기저선을 떠난 시점부터 돌아온 시점까지」의 시간이 먼저 — 세로 1분선으로 2분을 넘는지 센다.\n- 학습목표: 분만 중 태아심박동 감속의 유형을 지속시간으로 분류\n- 근거·출처: CTU-UHB 원자료(4 Hz) 작성자 계측: 기저 ≈150, 42.0~44.3분 FHR<135, 최저 ≈73 · Macones GA et al. NICHD 2008 workshop report on electronic fetal monitoring (Obstet Gynecol 2008)\n\n## 출처\n- CTU-UHB Intrapartum Cardiotocography Database (PhysioNet, ODC-BY 1.0) · record 1486 · Open Data Commons Attribution License v1.0 · https://opendatacommons.org/licenses/by/1-0/",
  "explanationItems": [
   {
    "k": "정답 핵심",
    "v": "Baseline is about 150/min (minutes 46–50). The heart rate leaves baseline at about minute 42, falls to a nadir near 75/min, and does not return until about minute 44.3 — a decrease of ≥15/min lasting ≥2 minutes but <10 minutes, which is a prolonged deceleration (NICHD)."
   },
   {
    "k": "원리",
    "v": "NICHD 분류에서 감속의 이름은 <b>모양이 아니라 「기저선을 떠나 돌아올 때까지의 시간」과 「시작 방식(급격/완만)」</b>으로 정한다. <b>기저선</b>은 감속·가속을 뺀 10분 구간에서 가장 흔한 값으로, 이 기록에서는 46~50분의 <b>약 150/min</b> 이다.<br> <b>왜 지속 감속인가</b> — 42.0분에 기저선을 떠나 <b>최저 약 75/min</b> 까지 떨어졌다가 <b>44.3분에야 돌아온다</b>. 감소 폭 ≥15/min 이고 지속시간이 <b>2분 이상 10분 미만</b>이므로 정의상 <b>prolonged deceleration</b> 이다. 10분을 넘으면 「기저선 변화」로 부른다.<br> <b>왜 2분이 경계인가</b> — 변이 감속의 기전은 <b>제대 압박 → 압수용체 반사 → 미주신경 긴장</b>으로, 압박이 풀리면 15초~2분 안에 회복된다. 2분을 넘게 돌아오지 못하면 <b>반사가 아니라 저산소증으로 인한 심근 억제</b>가 의심되는 시간대로 들어간다. 그래서 2분이 이름을 바꾸는 선이다.<br> <b>그다음 판단</b> — 지속 감속은 <b>2군(indeterminate)</b> 이고, 원인(자궁 과자극·저혈압·제대 탈출·태반 조기박리)을 찾아 <b>체위 변경·옥시토신 중단·수액·산소</b>로 소생 조치를 한다. <b>세로 1분선으로 시간을 세는 것</b>이 판독의 시작이다."
   },
   {
    "k": "비교",
    "v": "<table><thead><tr><th style=\"width:24%\">감속</th><th style=\"width:22%\">시작 방식</th><th style=\"width:22%\">지속</th><th>수축과의 관계 · 기전</th></tr></thead><tbody> <tr><td><b>지속 감속(정답)</b></td><td>급격 또는 완만</td><td><b>≥2분 ~ &lt;10분</b></td><td>수축과 무관해도 됨 · 저산소·제대압박 지속</td></tr> <tr><td>변이 감속</td><td><b>급격</b>(최저까지 &lt;30초)</td><td><b>15초 ~ &lt;2분</b></td><td>수축과 시점 불규칙 · 제대 압박 반사</td></tr> <tr><td>후기 감속</td><td>완만(≥30초)</td><td>수축 길이만큼</td><td><b>최저점이 수축 정점 뒤</b> · 자궁태반 관류 부전</td></tr> <tr><td>조기 감속</td><td>완만</td><td>수축 길이만큼</td><td><b>최저점이 수축 정점과 일치</b> · 아두 압박</td></tr> <tr><td>정현파형</td><td>—</td><td>≥20분</td><td>3~5 cycles/min 매끈한 사인파 · 태아 빈혈</td></tr> </tbody></table> <b>가장 가까운 오답은 ③ 변이 감속</b> — 모양이 급격해 보이면 변이 감속으로 부르기 쉽지만, <b>2.3분</b>이라는 시간이 이름을 바꾼다. 「급격 + 2분 미만 = 변이, 2분 이상 = 지속」이 경계다."
   },
   {
    "k": "오답 이유",
    "v": "(A) 정현파형은 3~5 cycles/min 의 매끈한 사인파가 20분 이상 이어지고 기저선 변이도가 사라진 상태로, 태아 빈혈·저산소를 뜻한다. 이 기록은 한 번의 큰 하강이다. 이 선지가 정답이 되려면 규칙적 파동이 20분 넘게 반복돼야 한다.\n(C) 변이 감속은 급격히 떨어지지만 15초에서 2분 미만에 회복하는 제대 압박 반사다. 이 감속은 2.3분 이어져 정의를 넘는다. 이 선지가 정답이 되려면 44분 전에 기저선으로 돌아왔어야 한다.\n(D) 후기 감속은 30초 이상 완만하게 내려가고 최저점이 수축 정점 뒤에 오며 수축마다 반복된다. 여기서는 하강이 수축 상승보다 먼저 시작하고 반복도 없다. 이 선지가 정답이 되려면 수축 정점 뒤로 밀린 최저점이 여러 수축에서 반복돼야 한다.\n(E) 조기 감속은 수축의 거울상처럼 얕고 완만하며 최저점이 수축 정점과 일치하는 아두 압박 소견이다. 75/min 까지 떨어지는 2분 넘는 하강은 그 범주가 아니다. 이 선지가 정답이 되려면 얕은 하강의 최저점이 수축 정점과 겹쳐야 한다."
   },
   {
    "k": "함정",
    "v": "감속 이름은 모양보다 「기저선을 떠난 시점부터 돌아온 시점까지」의 시간이 먼저 — 세로 1분선으로 2분을 넘는지 센다."
   },
   {
    "k": "학습목표",
    "v": "분만 중 태아심박동 감속의 유형을 지속시간으로 분류"
   },
   {
    "k": "근거·출처",
    "v": "CTU-UHB 원자료(4 Hz) 작성자 계측: 기저 ≈150, 42.0~44.3분 FHR<135, 최저 ≈73 · Macones GA et al. NICHD 2008 workshop report on electronic fetal monitoring (Obstet Gynecol 2008) ## 출처 CTU-UHB Intrapartum Cardiotocography Database (PhysioNet, ODC-BY 1.0) · record 1486 · Open Data Commons Attribution License v1.0 · https://opendatacommons.org/licenses/by/1-0/"
   }
  ],
  "source": "의대_시험지_제작 오픈데이터 영상 세트 / 20260913T053235Z_일일영상_2026-09-13_10units_9q_7072fb0c",
  "vitals": [],
  "labs": [],
  "appendix": null,
  "figureImg": {
   "src": "assets/imaging/imaging-2026-0006.png",
   "caption": "Intrapartum fetal heart rate (upper) and uterine activity (lower), minutes 40–50 of monitoring; 3 cm/min, vertical lines = 1 min (CTU-UHB Intrapartum Cardiotocography Database, PhysioNet, ODC-BY 1.0; 4 Hz raw data, no smoothing)",
   "alt": "CTG 영상"
  },
  "attribution": {
   "dataset": "CTU-UHB Intrapartum Cardiotocography Database",
   "license": "Open Data Commons Attribution License v1.0",
   "license_url": "https://opendatacommons.org/licenses/by/1-0/",
   "url": "https://physionet.org/content/ctu-uhb-ctgdb/1.0.0/",
   "asset_id": "CTU-1486_40m",
   "text": "CTU-UHB Intrapartum Cardiotocography Database (PhysioNet, ODC-BY 1.0) · record 1486"
  },
  "run_id": "20260913T053235Z_일일영상_2026-09-13_10units_9q_7072fb0c",
  "qid": "Q0006"
 },
 {
  "id": "imaging-2026-0004",
  "exam": "imaging",
  "style": "usmle_style",
  "styleLabel": "USMLE형",
  "subject": "병리·조직학",
  "subject_file": "병리·조직학",
  "setSubject": "통합(생식의학·응급·마취)",
  "subtopic": "생식샘 조직학과 성분화·무월경",
  "type": "생식샘 조직학과 성분화·무월경",
  "modality": "HISTOLOGY_IHC",
  "step": "Step 2",
  "difficulty": 3,
  "difficultyLabel": "중",
  "created": "2026-09-13",
  "vignette": "An 84-year-old man undergoes bilateral orchiectomy as androgen-deprivation therapy for metastatic prostate cancer. A section of the resected testis is stained by immunohistochemistry for a peptide hormone that is produced by only one cell population in this organ; the photomicrograph is shown (brown = positive, blue = hematoxylin counterstain).",
  "question": "The strongly stained cells are the principal target of which of the following hormones?",
  "options": [
   "Anti-Müllerian hormone",
   "Prolactin",
   "Luteinizing hormone",
   "Follicle-stimulating hormone",
   "Inhibin B"
  ],
  "answer": 3,
  "explanationText": "- 정답 핵심: Round tubules lined by germ cells are unstained; the strongly positive cells form clusters in the interstitium between the tubules — Leydig cells. Leydig cells express LH receptors and make testosterone in response to LH.\n- 원리: 이 사진에서 <b>세정관 안은 전부 음성</b>이고 <b>관 사이 결합조직에 무리 지은 세포만 강하게 갈색</b>이다. 위치만으로 <b>간질(Leydig)세포</b>가 정해진다. 염색한 펩타이드 호르몬은 <b>INSL3(insulin-like 3)</b> 로, 간질세포가 특이적으로 만드는 표지자다.<br> <b>왜 LH 인가</b> — 뇌하수체 성선자극호르몬은 <b>표적 세포가 다르다</b>. <b>LH 수용체(LHCGR)는 간질세포</b>에, <b>FSH 수용체는 세르톨리세포</b>에 있다. LH 가 LHCGR 에 결합하면 <b>cAMP↑ → StAR 단백 → 콜레스테롤이 미토콘드리아 안으로</b> 들어가고 <b>CYP11A1·17α-hydroxylase·17,20-lyase·17β-HSD</b> 를 거쳐 테스토스테론이 된다.<br> <b>외우는 틀</b> — <b>「L 은 L」</b>: LH → Leydig → 테스토스테론. <b>「F 는 S」</b>: FSH → Sertoli → 정자형성 지원·인히빈 B·ABP. 태아기에는 LH 대신 <b>태반 hCG</b> 가 같은 LHCGR 을 자극해 남성화에 필요한 테스토스테론을 만들게 한다는 점도 이 틀의 연장이다.<br> <b>임상으로 이어지면</b> — 간질세포 기능이 떨어지면 <b>LH 가 올라가고 테스토스테론이 낮은</b> 일차 성선기능저하증(클라인펠터 등)이 되고, 세르톨리 기능이 떨어지면 <b>인히빈 B 가 떨어져 FSH 가 오른다</b>. 사진 → 수용체 → 호르몬 축 해석까지가 한 묶음이다.\n- 비교: <table><thead><tr><th style=\"width:20%\">호르몬</th><th style=\"width:26%\">표적 세포 · 위치</th><th style=\"width:26%\">세포가 만드는 것</th><th>이 사진에서</th></tr></thead><tbody> <tr><td><b>LH(정답)</b></td><td><b>간질(Leydig)세포 · 관 사이</b></td><td>테스토스테론 · INSL3</td><td><b>강양성 무리 = 표적</b></td></tr> <tr><td>FSH</td><td>세르톨리세포 · 관 안 기저막</td><td>인히빈 B · ABP · 정자형성 지원</td><td>관 안이 음성 → 표적 아님</td></tr> <tr><td>AMH</td><td>뮐러관 중간엽(태아)</td><td>세르톨리가 분비하는 쪽</td><td>고환 안에 표적 없음</td></tr> <tr><td>인히빈 B</td><td>뇌하수체 FSH 세포</td><td>세르톨리가 분비하는 쪽</td><td>고환 안에 표적 없음</td></tr> <tr><td>프롤락틴</td><td>유선 · 시상하부</td><td>—</td><td>고환 스테로이드 합성의 영양호르몬 아님</td></tr> </tbody></table> <b>가장 가까운 오답은 ④ FSH</b> — 같은 성선자극호르몬이지만 <b>표적이 관 안(세르톨리)</b>이다. 사진에서 <b>관 안이 비어 있다</b>는 것이 결정적 근거다.\n- 오답 이유:\n  - (A) AMH 는 세르톨리세포가 분비해 태아 뮐러관에 작용하는 호르몬이라 간질세포는 표적이 아니라 오히려 무관한 쪽이다. 이 선지가 정답이 되려면 「이 세포가 분비하는 호르몬」을 물었고 염색된 세포가 관 안 세르톨리세포여야 한다.\n  - (B) 프롤락틴은 유선과 시상하부에 작용하며 고환 스테로이드 합성의 영양호르몬이 아니다. 고프롤락틴혈증은 GnRH 를 눌러 간접적으로 테스토스테론을 낮출 뿐이다. 이 선지가 정답이 되려면 유선 조직 사진이어야 한다.\n  - (D) FSH 의 수용체는 세정관 안의 세르톨리세포에 있다. 이 사진은 관 안이 전부 음성이라 세르톨리를 표적으로 물은 것이 아니다. 이 선지가 정답이 되려면 갈색 세포가 관 안 기저막에 한 줄로 늘어서 있어야 한다.\n  - (E) 인히빈 B 는 세르톨리세포가 만들어 뇌하수체 FSH 를 억제하는 쪽이지 간질세포가 표적이 되는 호르몬이 아니다. 이 선지가 정답이 되려면 「이 세포가 분비하는 것」을 물었고 세포가 세르톨리세포여야 한다.\n- 함정: LH = Leydig(간질), FSH = Sertoli(관 안) — 위치로 먼저 세포를 정하고 수용체를 붙인다.\n- 학습목표: 간질 Leydig 세포 식별과 LH 표적 연결\n- 근거·출처: HPA INSL3/testis 주석: Leydig cells high · 세정관 세포 not detected · 작성자 육안 판독(2026-09-13)\n\n## 출처\n- Human Protein Atlas, INSL3 / Testis (CC BY 4.0), https://images.proteinatlas.org/28615/59764_A_5_6.jpg · Creative Commons Attribution 4.0 International · https://www.proteinatlas.org/about/licence",
  "explanationItems": [
   {
    "k": "정답 핵심",
    "v": "Round tubules lined by germ cells are unstained; the strongly positive cells form clusters in the interstitium between the tubules — Leydig cells. Leydig cells express LH receptors and make testosterone in response to LH."
   },
   {
    "k": "원리",
    "v": "이 사진에서 <b>세정관 안은 전부 음성</b>이고 <b>관 사이 결합조직에 무리 지은 세포만 강하게 갈색</b>이다. 위치만으로 <b>간질(Leydig)세포</b>가 정해진다. 염색한 펩타이드 호르몬은 <b>INSL3(insulin-like 3)</b> 로, 간질세포가 특이적으로 만드는 표지자다.<br> <b>왜 LH 인가</b> — 뇌하수체 성선자극호르몬은 <b>표적 세포가 다르다</b>. <b>LH 수용체(LHCGR)는 간질세포</b>에, <b>FSH 수용체는 세르톨리세포</b>에 있다. LH 가 LHCGR 에 결합하면 <b>cAMP↑ → StAR 단백 → 콜레스테롤이 미토콘드리아 안으로</b> 들어가고 <b>CYP11A1·17α-hydroxylase·17,20-lyase·17β-HSD</b> 를 거쳐 테스토스테론이 된다.<br> <b>외우는 틀</b> — <b>「L 은 L」</b>: LH → Leydig → 테스토스테론. <b>「F 는 S」</b>: FSH → Sertoli → 정자형성 지원·인히빈 B·ABP. 태아기에는 LH 대신 <b>태반 hCG</b> 가 같은 LHCGR 을 자극해 남성화에 필요한 테스토스테론을 만들게 한다는 점도 이 틀의 연장이다.<br> <b>임상으로 이어지면</b> — 간질세포 기능이 떨어지면 <b>LH 가 올라가고 테스토스테론이 낮은</b> 일차 성선기능저하증(클라인펠터 등)이 되고, 세르톨리 기능이 떨어지면 <b>인히빈 B 가 떨어져 FSH 가 오른다</b>. 사진 → 수용체 → 호르몬 축 해석까지가 한 묶음이다."
   },
   {
    "k": "비교",
    "v": "<table><thead><tr><th style=\"width:20%\">호르몬</th><th style=\"width:26%\">표적 세포 · 위치</th><th style=\"width:26%\">세포가 만드는 것</th><th>이 사진에서</th></tr></thead><tbody> <tr><td><b>LH(정답)</b></td><td><b>간질(Leydig)세포 · 관 사이</b></td><td>테스토스테론 · INSL3</td><td><b>강양성 무리 = 표적</b></td></tr> <tr><td>FSH</td><td>세르톨리세포 · 관 안 기저막</td><td>인히빈 B · ABP · 정자형성 지원</td><td>관 안이 음성 → 표적 아님</td></tr> <tr><td>AMH</td><td>뮐러관 중간엽(태아)</td><td>세르톨리가 분비하는 쪽</td><td>고환 안에 표적 없음</td></tr> <tr><td>인히빈 B</td><td>뇌하수체 FSH 세포</td><td>세르톨리가 분비하는 쪽</td><td>고환 안에 표적 없음</td></tr> <tr><td>프롤락틴</td><td>유선 · 시상하부</td><td>—</td><td>고환 스테로이드 합성의 영양호르몬 아님</td></tr> </tbody></table> <b>가장 가까운 오답은 ④ FSH</b> — 같은 성선자극호르몬이지만 <b>표적이 관 안(세르톨리)</b>이다. 사진에서 <b>관 안이 비어 있다</b>는 것이 결정적 근거다."
   },
   {
    "k": "오답 이유",
    "v": "(A) AMH 는 세르톨리세포가 분비해 태아 뮐러관에 작용하는 호르몬이라 간질세포는 표적이 아니라 오히려 무관한 쪽이다. 이 선지가 정답이 되려면 「이 세포가 분비하는 호르몬」을 물었고 염색된 세포가 관 안 세르톨리세포여야 한다.\n(B) 프롤락틴은 유선과 시상하부에 작용하며 고환 스테로이드 합성의 영양호르몬이 아니다. 고프롤락틴혈증은 GnRH 를 눌러 간접적으로 테스토스테론을 낮출 뿐이다. 이 선지가 정답이 되려면 유선 조직 사진이어야 한다.\n(D) FSH 의 수용체는 세정관 안의 세르톨리세포에 있다. 이 사진은 관 안이 전부 음성이라 세르톨리를 표적으로 물은 것이 아니다. 이 선지가 정답이 되려면 갈색 세포가 관 안 기저막에 한 줄로 늘어서 있어야 한다.\n(E) 인히빈 B 는 세르톨리세포가 만들어 뇌하수체 FSH 를 억제하는 쪽이지 간질세포가 표적이 되는 호르몬이 아니다. 이 선지가 정답이 되려면 「이 세포가 분비하는 것」을 물었고 세포가 세르톨리세포여야 한다."
   },
   {
    "k": "함정",
    "v": "LH = Leydig(간질), FSH = Sertoli(관 안) — 위치로 먼저 세포를 정하고 수용체를 붙인다."
   },
   {
    "k": "학습목표",
    "v": "간질 Leydig 세포 식별과 LH 표적 연결"
   },
   {
    "k": "근거·출처",
    "v": "HPA INSL3/testis 주석: Leydig cells high · 세정관 세포 not detected · 작성자 육안 판독(2026-09-13) ## 출처 Human Protein Atlas, INSL3 / Testis (CC BY 4.0), https://images.proteinatlas.org/28615/59764_A_5_6.jpg · Creative Commons Attribution 4.0 International · https://www.proteinatlas.org/about/licence"
   }
  ],
  "source": "의대_시험지_제작 오픈데이터 영상 세트 / 20260913T053235Z_일일영상_2026-09-13_10units_9q_7072fb0c",
  "vitals": [],
  "labs": [],
  "appendix": null,
  "figureImg": {
   "src": "assets/imaging/imaging-2026-0004.jpg",
   "caption": "Human tissue section, immunohistochemistry (brown = positive, blue = hematoxylin counterstain) (Human Protein Atlas, CC BY 4.0; original image, resized only)",
   "alt": "HISTOLOGY_IHC 영상"
  },
  "attribution": {
   "dataset": "Human Protein Atlas (tissue IHC)",
   "license": "Creative Commons Attribution 4.0 International",
   "license_url": "https://www.proteinatlas.org/about/licence",
   "url": "https://www.proteinatlas.org/ENSG00000248099-INSL3/tissue/Testis",
   "asset_id": "HPA-INSL3_59764_A_5_6",
   "text": "Human Protein Atlas, INSL3 / Testis (CC BY 4.0), https://images.proteinatlas.org/28615/59764_A_5_6.jpg"
  },
  "run_id": "20260913T053235Z_일일영상_2026-09-13_10units_9q_7072fb0c",
  "qid": "Q0004"
 },
 {
  "id": "imaging-2026-0003",
  "exam": "imaging",
  "style": "kmle_style",
  "styleLabel": "국시형",
  "subject": "병리·조직학",
  "subject_file": "병리·조직학",
  "setSubject": "통합(생식의학·응급·마취)",
  "subtopic": "생식샘 조직학과 성분화·무월경",
  "type": "생식샘 조직학과 성분화·무월경",
  "modality": "HISTOLOGY_IHC",
  "step": "",
  "difficulty": 4,
  "difficultyLabel": "상",
  "created": "2026-09-13",
  "vignette": "65세 남자가 전이 전립선암의 호르몬 치료로 양측 고환절제술을 받았다. 절제한 고환 조직 절편에 어떤 전사인자에 대한 면역조직화학염색(갈색 = 양성, 청색 = 대조염색)을 하였더니 그림과 같았다.",
  "question": "짙은 갈색 핵으로 강하게 염색된 세포가 태아기에 분비하는 물질의 작용으로 옳은 것은?",
  "options": [
   "외부생식기의 남성화",
   "고환 하강의 경복부 단계 유도",
   "태반의 hCG 분비 촉진",
   "중신옆관(뮐러관)의 퇴화 유도",
   "중신관(볼프관)의 분화 유지"
  ],
  "answer": 4,
  "explanationText": "- 정답 핵심: 둥근 관(세정관) 안에 생식세포가 층을 이루고, 짙은 갈색 핵은 관의 기저막에 붙어 한 줄로 늘어서 있다 — 세르톨리세포. 관 사이 간질세포는 음성이다. 태아 세르톨리세포는 항뮐러관호르몬(AMH)을 분비해 뮐러관을 퇴화시킨다.\n- 원리: 고환의 조직 구조는 <b>「관 안」과 「관 사이」</b> 두 구획으로 읽는다. 세정관 안에는 <b>생식세포가 층을 이루고</b>, 그 <b>기저막에 발을 붙인 큰 세포가 세르톨리세포</b>다. 관 사이 성긴 결합조직에 <b>무리 지어 있는 세포가 간질(Leydig)세포</b>다. 이 사진의 짙은 갈색 핵은 <b>관 안, 기저막 쪽에 한 줄로</b> 늘어서 있으므로 세르톨리세포다.<br> <b>왜 SOX9 인가</b> — SOX9 는 <b>SRY 아래에서 세르톨리세포 운명을 정하는 전사인자</b>로, 태아기부터 성인까지 세르톨리 핵에 발현한다. 그래서 IHC 에서 핵이 갈색으로 물든다.<br> <b>태아기 세르톨리세포의 일</b> — <b>항뮐러관호르몬(AMH, TGF-β 계열 당단백)</b> 을 분비한다. AMH 는 <b>중신옆관(뮐러관) 주변 중간엽의 AMHR2</b> 에 결합해 세포자멸사를 유도하고, 그 결과 <b>자궁·난관·질 상부가 만들어지지 않는다</b>. 임신 8주 무렵부터 작동하며, 이것이 46,XY 태아에 여성 내부생식기가 없는 이유다.<br> <b>남성화의 나머지 절반</b>은 <b>간질세포의 테스토스테론(볼프관 유지)과 DHT(외부생식기·전립선)</b> 이 맡는다. 즉 「없애는 일은 세르톨리(AMH), 만드는 일은 간질(안드로겐)」로 나뉜다.\n- 비교: <table><thead><tr><th style=\"width:22%\">세포</th><th style=\"width:22%\">사진에서의 위치</th><th style=\"width:24%\">태아기 분비물</th><th>작용</th></tr></thead><tbody> <tr><td><b>세르톨리세포(정답)</b></td><td><b>세정관 안 · 기저막에 한 줄</b></td><td><b>AMH</b></td><td><b>뮐러관 퇴화</b> → 자궁·난관 없음</td></tr> <tr><td>간질(Leydig)세포</td><td>관 사이 결합조직에 무리</td><td>테스토스테론 · INSL3</td><td>볼프관 유지 · 경복부 고환하강</td></tr> <tr><td>표적 조직(5α-환원효소)</td><td>—</td><td>DHT</td><td>외부생식기 남성화 · 전립선</td></tr> <tr><td>태반 합체영양막</td><td>—</td><td>hCG</td><td>초기 간질세포 자극(태아 고환이 촉진하지 않음)</td></tr> </tbody></table> <b>가장 가까운 오답은 ⑤</b> — 같은 고환 세포의 태아기 기능이지만 <b>볼프관 유지는 간질세포의 테스토스테론</b>이다. 사진에서 <b>관 사이가 음성</b>인 것이 결정적 근거다.\n- 오답 이유:\n  - ① 외부생식기 남성화는 테스토스테론이 표적 조직의 5α-환원효소로 DHT 가 되어 일으킨다. 세르톨리세포는 안드로겐을 만들지 않는다. 이 선지가 정답이 되려면 갈색 세포가 관 사이 간질세포여야 하고, 그래도 「DHT 작용」으로 한 단계 더 가야 한다.\n  - ② 고환의 경복부 하강은 간질세포가 분비하는 INSL3 가 고환도대를 두껍게 해 이끈다. 이 선지가 정답이 되려면 염색된 세포가 관 사이에 무리 지은 간질세포여야 한다.\n  - ③ hCG 는 태반 합체영양막이 분비하며 태아 고환 세포가 그 분비를 촉진하는 경로는 없다. 오히려 hCG 가 간질세포를 자극하는 방향이다. 이 선지가 정답이 되려면 분비 주체와 표적이 뒤바뀌어야 하므로 어떤 사진에서도 성립하지 않는다.\n  - ⑤ 볼프관을 부고환·정관·정낭으로 분화·유지하는 것은 간질세포의 테스토스테론이다. 이 사진에서는 관 사이가 음성이라 간질세포를 물은 것이 아니다. 이 선지가 정답이 되려면 갈색 세포가 관 사이에 있어야 한다.\n- 함정: 갈색 세포가 「관 안」인지 「관 사이」인지가 세르톨리(AMH)와 간질세포(테스토스테론)를 가르는 첫 갈림길이다.\n- 학습목표: 세정관 기저부 세르톨리세포를 식별하고 태아기 기능(AMH)에 연결\n- 근거·출처: HPA SOX9/testis 주석: Sertoli cells high · 나머지 not detected · 작성자 육안 판독(2026-09-13)\n\n## 출처\n- Human Protein Atlas, SOX9 / Testis (CC BY 4.0), https://images.proteinatlas.org/68240/159895_A_5_6.jpg · Creative Commons Attribution 4.0 International · https://www.proteinatlas.org/about/licence",
  "explanationItems": [
   {
    "k": "정답 핵심",
    "v": "둥근 관(세정관) 안에 생식세포가 층을 이루고, 짙은 갈색 핵은 관의 기저막에 붙어 한 줄로 늘어서 있다 — 세르톨리세포. 관 사이 간질세포는 음성이다. 태아 세르톨리세포는 항뮐러관호르몬(AMH)을 분비해 뮐러관을 퇴화시킨다."
   },
   {
    "k": "원리",
    "v": "고환의 조직 구조는 <b>「관 안」과 「관 사이」</b> 두 구획으로 읽는다. 세정관 안에는 <b>생식세포가 층을 이루고</b>, 그 <b>기저막에 발을 붙인 큰 세포가 세르톨리세포</b>다. 관 사이 성긴 결합조직에 <b>무리 지어 있는 세포가 간질(Leydig)세포</b>다. 이 사진의 짙은 갈색 핵은 <b>관 안, 기저막 쪽에 한 줄로</b> 늘어서 있으므로 세르톨리세포다.<br> <b>왜 SOX9 인가</b> — SOX9 는 <b>SRY 아래에서 세르톨리세포 운명을 정하는 전사인자</b>로, 태아기부터 성인까지 세르톨리 핵에 발현한다. 그래서 IHC 에서 핵이 갈색으로 물든다.<br> <b>태아기 세르톨리세포의 일</b> — <b>항뮐러관호르몬(AMH, TGF-β 계열 당단백)</b> 을 분비한다. AMH 는 <b>중신옆관(뮐러관) 주변 중간엽의 AMHR2</b> 에 결합해 세포자멸사를 유도하고, 그 결과 <b>자궁·난관·질 상부가 만들어지지 않는다</b>. 임신 8주 무렵부터 작동하며, 이것이 46,XY 태아에 여성 내부생식기가 없는 이유다.<br> <b>남성화의 나머지 절반</b>은 <b>간질세포의 테스토스테론(볼프관 유지)과 DHT(외부생식기·전립선)</b> 이 맡는다. 즉 「없애는 일은 세르톨리(AMH), 만드는 일은 간질(안드로겐)」로 나뉜다."
   },
   {
    "k": "비교",
    "v": "<table><thead><tr><th style=\"width:22%\">세포</th><th style=\"width:22%\">사진에서의 위치</th><th style=\"width:24%\">태아기 분비물</th><th>작용</th></tr></thead><tbody> <tr><td><b>세르톨리세포(정답)</b></td><td><b>세정관 안 · 기저막에 한 줄</b></td><td><b>AMH</b></td><td><b>뮐러관 퇴화</b> → 자궁·난관 없음</td></tr> <tr><td>간질(Leydig)세포</td><td>관 사이 결합조직에 무리</td><td>테스토스테론 · INSL3</td><td>볼프관 유지 · 경복부 고환하강</td></tr> <tr><td>표적 조직(5α-환원효소)</td><td>—</td><td>DHT</td><td>외부생식기 남성화 · 전립선</td></tr> <tr><td>태반 합체영양막</td><td>—</td><td>hCG</td><td>초기 간질세포 자극(태아 고환이 촉진하지 않음)</td></tr> </tbody></table> <b>가장 가까운 오답은 ⑤</b> — 같은 고환 세포의 태아기 기능이지만 <b>볼프관 유지는 간질세포의 테스토스테론</b>이다. 사진에서 <b>관 사이가 음성</b>인 것이 결정적 근거다."
   },
   {
    "k": "오답 이유",
    "v": "① 외부생식기 남성화는 테스토스테론이 표적 조직의 5α-환원효소로 DHT 가 되어 일으킨다. 세르톨리세포는 안드로겐을 만들지 않는다. 이 선지가 정답이 되려면 갈색 세포가 관 사이 간질세포여야 하고, 그래도 「DHT 작용」으로 한 단계 더 가야 한다.\n② 고환의 경복부 하강은 간질세포가 분비하는 INSL3 가 고환도대를 두껍게 해 이끈다. 이 선지가 정답이 되려면 염색된 세포가 관 사이에 무리 지은 간질세포여야 한다.\n③ hCG 는 태반 합체영양막이 분비하며 태아 고환 세포가 그 분비를 촉진하는 경로는 없다. 오히려 hCG 가 간질세포를 자극하는 방향이다. 이 선지가 정답이 되려면 분비 주체와 표적이 뒤바뀌어야 하므로 어떤 사진에서도 성립하지 않는다.\n⑤ 볼프관을 부고환·정관·정낭으로 분화·유지하는 것은 간질세포의 테스토스테론이다. 이 사진에서는 관 사이가 음성이라 간질세포를 물은 것이 아니다. 이 선지가 정답이 되려면 갈색 세포가 관 사이에 있어야 한다."
   },
   {
    "k": "함정",
    "v": "갈색 세포가 「관 안」인지 「관 사이」인지가 세르톨리(AMH)와 간질세포(테스토스테론)를 가르는 첫 갈림길이다."
   },
   {
    "k": "학습목표",
    "v": "세정관 기저부 세르톨리세포를 식별하고 태아기 기능(AMH)에 연결"
   },
   {
    "k": "근거·출처",
    "v": "HPA SOX9/testis 주석: Sertoli cells high · 나머지 not detected · 작성자 육안 판독(2026-09-13) ## 출처 Human Protein Atlas, SOX9 / Testis (CC BY 4.0), https://images.proteinatlas.org/68240/159895_A_5_6.jpg · Creative Commons Attribution 4.0 International · https://www.proteinatlas.org/about/licence"
   }
  ],
  "source": "의대_시험지_제작 오픈데이터 영상 세트 / 20260913T053235Z_일일영상_2026-09-13_10units_9q_7072fb0c",
  "vitals": [],
  "labs": [],
  "appendix": null,
  "figureImg": {
   "src": "assets/imaging/imaging-2026-0003.jpg",
   "caption": "사람 장기 조직 절편, 면역조직화학염색(양성 = 갈색, 핵 대조염색 = 청색) (Human Protein Atlas, CC BY 4.0 — 원본 그대로, 크기 조정만)",
   "alt": "HISTOLOGY_IHC 영상"
  },
  "attribution": {
   "dataset": "Human Protein Atlas (tissue IHC)",
   "license": "Creative Commons Attribution 4.0 International",
   "license_url": "https://www.proteinatlas.org/about/licence",
   "url": "https://www.proteinatlas.org/ENSG00000125398-SOX9/tissue/Testis",
   "asset_id": "HPA-SOX9_159895_A_5_6",
   "text": "Human Protein Atlas, SOX9 / Testis (CC BY 4.0), https://images.proteinatlas.org/68240/159895_A_5_6.jpg"
  },
  "run_id": "20260913T053235Z_일일영상_2026-09-13_10units_9q_7072fb0c",
  "qid": "Q0003"
 },
 {
  "id": "imaging-2026-0002",
  "exam": "imaging",
  "style": "kmle_style",
  "styleLabel": "국시형",
  "subject": "순환기",
  "subject_file": "순환기",
  "setSubject": "통합(생식의학·응급·마취)",
  "subtopic": "심전도 판독 — 응급·마취 전 평가",
  "type": "심전도 판독 — 응급·마취 전 평가",
  "modality": "ECG",
  "step": "",
  "difficulty": 3,
  "difficultyLabel": "중",
  "created": "2026-09-13",
  "vignette": "79세 여자가 1시간 전 갑자기 시작된 두근거림으로 응급실에 왔다. 의식은 명료하고 흉통·호흡곤란은 없다. 혈압 128/80 mmHg 이다. 심전도는 그림과 같다.",
  "question": "가장 먼저 할 처치는?",
  "options": [
   "변형 발살바 수기(미주신경자극)",
   "아데노신 6 mg 급속 정맥주사",
   "동기화 심장율동전환",
   "아미오다론 정맥주사",
   "경구 디곡신"
  ],
  "answer": 1,
  "explanationText": "- 정답 핵심: QRS 가 좁고 RR 이 완전히 규칙적인 분당 약 175회 빈맥이며 QRS 앞에 뚜렷한 P파가 없다 — 발작성 상심실빈맥. 혈역학적으로 안정되어 있으므로 미주신경자극(변형 발살바)이 첫 단계이고, 실패하면 아데노신을 쓴다.\n- 원리: 좁은 QRS 의 규칙적 빈맥이 <b>갑자기 시작</b>했다면 대부분 <b>방실결절을 회로의 일부로 쓰는 회귀빈맥(AVNRT·AVRT)</b> 이다. 회귀는 <b>느린 길과 빠른 길이 방실결절 안팎에서 고리를 이루어 흥분이 맴도는 것</b>이므로, <b>고리의 한 지점(방실결절)의 전도를 잠깐 끊으면 빈맥이 멈춘다</b>.<br> <b>왜 미주신경자극이 첫 단계인가</b> — 발살바 수기는 <b>흉강내압 상승 → 압반사 → 미주신경 긴장 증가 → 방실결절 전도 지연·차단</b> 을 일으킨다. 약물 없이, 부작용 없이 회로를 끊을 수 있고, <b>변형 발살바(숨 참기 후 즉시 눕혀 다리 올리기)는 종료율이 약 17 % → 43 %</b> 로 오른다(REVERT).<br> <b>왜 아데노신이 그다음인가</b> — 아데노신은 <b>방실결절의 A1 수용체로 K⁺ 통로를 열어 수 초간 전도를 차단</b>하는 「약으로 하는 미주신경자극」이다. 효과는 확실하지만 안면홍조·흉부 압박감·일시 무수축이 따르므로 <b>비침습 수기가 실패한 뒤</b>에 쓴다.<br> <b>순서를 정하는 축은 혈역학</b> — 저혈압·의식저하·허혈성 흉통·급성 심부전이 있으면 이 순서를 건너뛰고 <b>동기화 율동전환</b>으로 간다. 이 환자는 혈압 128/80, 의식 명료라 안정군이다.\n- 비교: <table><thead><tr><th style=\"width:24%\">상황</th><th style=\"width:34%\">첫 처치</th><th>왜</th></tr></thead><tbody> <tr><td><b>안정 · 좁은 QRS · 규칙적(정답)</b></td><td><b>변형 발살바(미주신경자극)</b></td><td>약 없이 방실결절 전도를 끊어 회로 종료 · 실패 시 아데노신</td></tr> <tr><td>안정 · 발살바 실패</td><td><b>아데노신 6 → 12 mg 급속 IV</b></td><td>A1 수용체로 방실결절 일시 차단</td></tr> <tr><td><b>불안정</b>(저혈압·의식저하·흉통·폐부종)</td><td><b>동기화 율동전환</b></td><td>회로를 전기로 한 번에 재설정</td></tr> <tr><td>넓은 QRS · 규칙적</td><td>심실빈맥으로 간주 — 아미오다론/프로카인아마이드 또는 율동전환</td><td>아데노신은 진단적 보조에 그침</td></tr> </tbody></table> <b>가장 가까운 오답은 ②</b> — 같은 안정군 PSVT 의 처치지만 <b>순서가 두 번째</b>다. 「가장 먼저」를 물으면 수기, 「수기가 실패했다」면 아데노신. <b>75세 이상에서는 경동맥동 마사지를 피하지만</b> 발살바는 나이와 무관하게 첫 단계다.\n- 오답 이유:\n  - ② 아데노신은 방실결절을 수 초간 차단해 회로를 끊는 확실한 약이지만 홍조·흉부 압박감·일시 무수축이 따라 비침습 수기 뒤에 쓴다. 이 선지가 정답이 되려면 발문에 「발살바 수기를 시행했으나 종료되지 않았다」가 있어야 한다.\n  - ③ 동기화 율동전환은 저혈압·의식저하·허혈성 흉통·급성 심부전 같은 불안정 징후가 있을 때의 첫 처치다. 혈압 128/80 에 의식 명료인 이 환자에서는 순서가 맨 뒤다. 이 선지가 정답이 되려면 불안정 징후 하나가 발문에 있어야 한다.\n  - ④ 아미오다론은 넓은 QRS 빈맥이나 심기능이 나쁜 환자의 심방세동 조절에 쓰는 약이지 좁은 QRS 규칙적 빈맥의 1차 종료 약이 아니다. 이 선지가 정답이 되려면 QRS 가 넓고 심실빈맥이 의심되는 기록이어야 한다.\n  - ⑤ 디곡신은 방실결절 전도를 늦추지만 효과 발현이 느려 급성 종료 목적에 쓰지 않는다. 이 선지가 정답이 되려면 「심방세동의 장기 심박수 조절」처럼 시간 축이 다른 상황이어야 한다.\n- 함정: 75세 이상이라 경동맥동 마사지는 피하지만(경동맥 협착·색전 위험), 발살바 수기는 그대로 첫 단계다.\n- 학습목표: 혈역학적으로 안정된 좁은 QRS 규칙적 빈맥의 첫 처치\n- 근거·출처: PTB-XL 기록 라벨 PSVT(2인 심장내과 검증) · 작성자 원신호 계측: RR 0.34 s(sd 5 ms), HR 176 · 2015 ACC/AHA/HRS SVT 가이드라인 · REVERT 시험(Lancet 2015)\n\n## 출처\n- PTB-XL ECG dataset v1.0.3 (PhysioNet, CC BY 4.0) · record 16229 · Creative Commons Attribution 4.0 International · https://physionet.org/content/ptb-xl/1.0.3/LICENSE.txt",
  "explanationItems": [
   {
    "k": "정답 핵심",
    "v": "QRS 가 좁고 RR 이 완전히 규칙적인 분당 약 175회 빈맥이며 QRS 앞에 뚜렷한 P파가 없다 — 발작성 상심실빈맥. 혈역학적으로 안정되어 있으므로 미주신경자극(변형 발살바)이 첫 단계이고, 실패하면 아데노신을 쓴다."
   },
   {
    "k": "원리",
    "v": "좁은 QRS 의 규칙적 빈맥이 <b>갑자기 시작</b>했다면 대부분 <b>방실결절을 회로의 일부로 쓰는 회귀빈맥(AVNRT·AVRT)</b> 이다. 회귀는 <b>느린 길과 빠른 길이 방실결절 안팎에서 고리를 이루어 흥분이 맴도는 것</b>이므로, <b>고리의 한 지점(방실결절)의 전도를 잠깐 끊으면 빈맥이 멈춘다</b>.<br> <b>왜 미주신경자극이 첫 단계인가</b> — 발살바 수기는 <b>흉강내압 상승 → 압반사 → 미주신경 긴장 증가 → 방실결절 전도 지연·차단</b> 을 일으킨다. 약물 없이, 부작용 없이 회로를 끊을 수 있고, <b>변형 발살바(숨 참기 후 즉시 눕혀 다리 올리기)는 종료율이 약 17 % → 43 %</b> 로 오른다(REVERT).<br> <b>왜 아데노신이 그다음인가</b> — 아데노신은 <b>방실결절의 A1 수용체로 K⁺ 통로를 열어 수 초간 전도를 차단</b>하는 「약으로 하는 미주신경자극」이다. 효과는 확실하지만 안면홍조·흉부 압박감·일시 무수축이 따르므로 <b>비침습 수기가 실패한 뒤</b>에 쓴다.<br> <b>순서를 정하는 축은 혈역학</b> — 저혈압·의식저하·허혈성 흉통·급성 심부전이 있으면 이 순서를 건너뛰고 <b>동기화 율동전환</b>으로 간다. 이 환자는 혈압 128/80, 의식 명료라 안정군이다."
   },
   {
    "k": "비교",
    "v": "<table><thead><tr><th style=\"width:24%\">상황</th><th style=\"width:34%\">첫 처치</th><th>왜</th></tr></thead><tbody> <tr><td><b>안정 · 좁은 QRS · 규칙적(정답)</b></td><td><b>변형 발살바(미주신경자극)</b></td><td>약 없이 방실결절 전도를 끊어 회로 종료 · 실패 시 아데노신</td></tr> <tr><td>안정 · 발살바 실패</td><td><b>아데노신 6 → 12 mg 급속 IV</b></td><td>A1 수용체로 방실결절 일시 차단</td></tr> <tr><td><b>불안정</b>(저혈압·의식저하·흉통·폐부종)</td><td><b>동기화 율동전환</b></td><td>회로를 전기로 한 번에 재설정</td></tr> <tr><td>넓은 QRS · 규칙적</td><td>심실빈맥으로 간주 — 아미오다론/프로카인아마이드 또는 율동전환</td><td>아데노신은 진단적 보조에 그침</td></tr> </tbody></table> <b>가장 가까운 오답은 ②</b> — 같은 안정군 PSVT 의 처치지만 <b>순서가 두 번째</b>다. 「가장 먼저」를 물으면 수기, 「수기가 실패했다」면 아데노신. <b>75세 이상에서는 경동맥동 마사지를 피하지만</b> 발살바는 나이와 무관하게 첫 단계다."
   },
   {
    "k": "오답 이유",
    "v": "② 아데노신은 방실결절을 수 초간 차단해 회로를 끊는 확실한 약이지만 홍조·흉부 압박감·일시 무수축이 따라 비침습 수기 뒤에 쓴다. 이 선지가 정답이 되려면 발문에 「발살바 수기를 시행했으나 종료되지 않았다」가 있어야 한다.\n③ 동기화 율동전환은 저혈압·의식저하·허혈성 흉통·급성 심부전 같은 불안정 징후가 있을 때의 첫 처치다. 혈압 128/80 에 의식 명료인 이 환자에서는 순서가 맨 뒤다. 이 선지가 정답이 되려면 불안정 징후 하나가 발문에 있어야 한다.\n④ 아미오다론은 넓은 QRS 빈맥이나 심기능이 나쁜 환자의 심방세동 조절에 쓰는 약이지 좁은 QRS 규칙적 빈맥의 1차 종료 약이 아니다. 이 선지가 정답이 되려면 QRS 가 넓고 심실빈맥이 의심되는 기록이어야 한다.\n⑤ 디곡신은 방실결절 전도를 늦추지만 효과 발현이 느려 급성 종료 목적에 쓰지 않는다. 이 선지가 정답이 되려면 「심방세동의 장기 심박수 조절」처럼 시간 축이 다른 상황이어야 한다."
   },
   {
    "k": "함정",
    "v": "75세 이상이라 경동맥동 마사지는 피하지만(경동맥 협착·색전 위험), 발살바 수기는 그대로 첫 단계다."
   },
   {
    "k": "학습목표",
    "v": "혈역학적으로 안정된 좁은 QRS 규칙적 빈맥의 첫 처치"
   },
   {
    "k": "근거·출처",
    "v": "PTB-XL 기록 라벨 PSVT(2인 심장내과 검증) · 작성자 원신호 계측: RR 0.34 s(sd 5 ms), HR 176 · 2015 ACC/AHA/HRS SVT 가이드라인 · REVERT 시험(Lancet 2015) ## 출처 PTB-XL ECG dataset v1.0.3 (PhysioNet, CC BY 4.0) · record 16229 · Creative Commons Attribution 4.0 International · https://physionet.org/content/ptb-xl/1.0.3/LICENSE.txt"
   }
  ],
  "source": "의대_시험지_제작 오픈데이터 영상 세트 / 20260913T053235Z_일일영상_2026-09-13_10units_9q_7072fb0c",
  "vitals": [],
  "labs": [],
  "appendix": null,
  "figureImg": {
   "src": "assets/imaging/imaging-2026-0002.png",
   "caption": "12유도 심전도, 25 mm/s · 10 mm/mV, 3×4 + II 리듬 스트립 (PTB-XL ECG dataset, PhysioNet, CC BY 4.0 — 원신호 그대로 작도)",
   "alt": "ECG 영상"
  },
  "attribution": {
   "dataset": "PTB-XL, a large publicly available electrocardiography dataset",
   "license": "Creative Commons Attribution 4.0 International",
   "license_url": "https://physionet.org/content/ptb-xl/1.0.3/LICENSE.txt",
   "url": "https://physionet.org/content/ptb-xl/1.0.3/records500/16000/#files-panel",
   "asset_id": "PTBXL-16229",
   "text": "PTB-XL ECG dataset v1.0.3 (PhysioNet, CC BY 4.0) · record 16229"
  },
  "run_id": "20260913T053235Z_일일영상_2026-09-13_10units_9q_7072fb0c",
  "qid": "Q0002"
 },
 {
  "id": "imaging-2026-0001",
  "exam": "imaging",
  "style": "kmle_style",
  "styleLabel": "국시형",
  "subject": "순환기",
  "subject_file": "순환기",
  "setSubject": "통합(생식의학·응급·마취)",
  "subtopic": "심전도 판독 — 응급·마취 전 평가",
  "type": "심전도 판독 — 응급·마취 전 평가",
  "modality": "ECG",
  "step": "",
  "difficulty": 4,
  "difficultyLabel": "상",
  "created": "2026-09-13",
  "vignette": "79세 남자가 예정 수술 전 검사로 심전도를 찍었다. 증상은 없고 맥박은 분당 55회로 규칙적이다. 심전도는 그림과 같다.",
  "question": "심전도 소견과 수술 후 오심·구토 예방 계획을 옳게 짝지은 것은?",
  "options": [
   "좌심실비대 — 예방약 선택에 제한이 없다",
   "고칼륨혈증(뾰족한 T파) — 칼슘을 투여한 뒤 수술을 진행한다",
   "QT 간격 연장 — 온단세트론 투여를 피한다",
   "QT 간격 연장 — 드로페리돌을 우선 투여한다",
   "완전방실차단 — 수술 전 임시 심박조율기를 삽입한다"
  ],
  "answer": 3,
  "explanationText": "- 정답 핵심: 서맥(RR ≈1.1 s)에서 QRS 시작부터 느리고 낮은 T파 끝까지 ≈0.52 s(II·V5, 큰 칸 2.5칸 이상) — Bazett 보정 QTc ≈0.50 s 로 뚜렷한 QT 연장이다. 모든 P 뒤에 QRS 가 따르고 T파는 뾰족하지 않다. QT 연장 환자는 비틀림 심실빈맥(torsades) 위험이 커서 5-HT3 길항제(온단세트론)·드로페리돌 같은 QT 연장 제제를 피하고 덱사메타손·아프레피탄트 등으로 대체하며 K·Mg 를 교정한다.\n- 원리: QT 간격은 <b>심실의 탈분극 시작부터 재분극이 끝날 때까지</b>다. 재분극은 <b>K⁺ 이 세포 밖으로 나가는 전류(주로 IKr)</b>가 만들고, 이 전류가 약물·전해질·선천 이온통로 이상으로 <b>느려지면 T파가 늦게 끝나 QT 가 길어진다</b>.<br> <b>왜 심박수로 보정하는가</b> — 재분극 시간은 심박수가 느릴수록 생리적으로 길어진다. 그래서 <b>QTc = QT/√RR(Bazett)</b> 로 60회/분 기준에 맞춘다. 이 환자는 RR 1.10 s(55회/분)이므로 <b>√RR≈1.05, QTc≈0.52/1.05≈0.50 s</b> — 남자 기준 <b>0.45 s 를 훌쩍 넘는</b> 뚜렷한 연장이다.<br> <b>왜 위험한가</b> — 재분극이 길어지면 <b>조기후탈분극(EAD)</b> 이 생기고, 이것이 <b>비틀림 심실빈맥(torsades de pointes)</b> 의 방아쇠가 된다. QT 를 더 늘리는 약(5-HT3 길항제·드로페리돌·할로페리돌·일부 항생제)과 <b>저K·저Mg</b> 는 위험을 곱한다.<br> <b>그래서 주술기 계획</b> — PONV 예방에서 <b>온단세트론·드로페리돌을 빼고 덱사메타손·아프레피탄트로 대체</b>하며, K·Mg 를 정상 상단으로 교정하고 수술 중 QT 를 감시한다. 「심전도 판독 → 약물 선택」이 한 줄로 이어지는 문항이다.\n- 비교: <table><thead><tr><th style=\"width:26%\">심전도 소견</th><th style=\"width:30%\">이 기록에서의 근거</th><th>주술기 대응</th></tr></thead><tbody> <tr><td><b>QT 연장(정답)</b></td><td><b>QT≈0.52 s · RR 1.10 s → QTc≈0.50 s</b>, T파 낮고 넓음</td><td><b>온단세트론·드로페리돌 회피</b>, K·Mg 교정, QT 감시</td></tr> <tr><td>고칼륨혈증</td><td>T파가 <b>뾰족·좁은 텐트형</b>이어야 함 — 여기선 낮고 넓음</td><td>칼슘·인슐린-포도당 후 수술</td></tr> <tr><td>좌심실비대</td><td>SV1+RV5 ≥3.5 mV 등 전압 기준 — 여기선 ≈2.2 mV</td><td>PONV 약 제한 없음</td></tr> <tr><td>완전방실차단</td><td>P–QRS 해리 · 심실 이탈율동 — 여기선 매 P 뒤 QRS</td><td>임시 조율기</td></tr> </tbody></table> <b>가장 가까운 오답은 ④</b> — 같은 「QT 연장」 판독이지만 <b>드로페리돌은 온단세트론보다 QT 경고가 더 강한 약(블랙박스)</b> 이라 「우선 투여」는 판독을 맞히고도 처치에서 틀리는 자리다.\n- 오답 이유:\n  - ① 좌심실비대는 SV1+RV5 ≥3.5 mV 또는 RaVL ≥1.1 mV 같은 전압 기준을 채워야 하고, 설령 비대가 있어도 QT 연장이 함께 있으면 예방약 제한이 생긴다. 이 선지가 정답이 되려면 QT 가 정상이고 전압 기준을 넘어야 한다.\n  - ② 고칼륨혈증은 T파가 좁고 뾰족한 텐트형으로 서고 QRS 가 넓어진다. 이 기록은 T파가 낮고 넓어 정반대다. 이 선지가 정답이 되려면 뾰족한 T파와 함께 K⁺ 상승의 임상 배경이 있어야 한다.\n  - ④ 판독(QT 연장)은 맞지만 드로페리돌은 QT 연장 경고가 더 강한 약이라 QT 연장 환자에게는 온단세트론보다 먼저 쓸 이유가 없다. 이 선지가 정답이 되려면 QT 가 정상이고 5-HT3 길항제를 못 쓰는 별도 사유가 있어야 한다.\n  - ⑤ 완전방실차단은 P파와 QRS 가 서로 무관하게 각자 규칙적으로 뛴다(방실해리). 여기서는 모든 P 뒤에 일정한 간격으로 QRS 가 따른다. 이 선지가 정답이 되려면 P–QRS 해리와 느린 이탈율동이 보여야 한다.\n- 함정: 서맥에서는 「QT < RR 의 절반」 눈대중이 틀어진다. 반드시 QT 를 재서 √RR 로 보정한다 — 55회/분에서 0.52 s 는 QTc ≈0.50 s.\n- 학습목표: 수술 전 심전도에서 QT 연장을 읽고 주술기 약물 선택에 연결\n- 근거·출처: PTB-XL 기록 라벨 LNGQT(2인 심장내과 검증) · 작성자 원신호 계측: QT≈520 ms, RR 1.096 s, QTcB≈497 ms · Fourth Consensus Guidelines for the Management of PONV (Anesth Analg 2020) — QT 연장 환자에서 5-HT3 길항제·드로페리돌 주의\n\n## 출처\n- PTB-XL ECG dataset v1.0.3 (PhysioNet, CC BY 4.0) · record 320 · Creative Commons Attribution 4.0 International · https://physionet.org/content/ptb-xl/1.0.3/LICENSE.txt",
  "explanationItems": [
   {
    "k": "정답 핵심",
    "v": "서맥(RR ≈1.1 s)에서 QRS 시작부터 느리고 낮은 T파 끝까지 ≈0.52 s(II·V5, 큰 칸 2.5칸 이상) — Bazett 보정 QTc ≈0.50 s 로 뚜렷한 QT 연장이다. 모든 P 뒤에 QRS 가 따르고 T파는 뾰족하지 않다. QT 연장 환자는 비틀림 심실빈맥(torsades) 위험이 커서 5-HT3 길항제(온단세트론)·드로페리돌 같은 QT 연장 제제를 피하고 덱사메타손·아프레피탄트 등으로 대체하며 K·Mg 를 교정한다."
   },
   {
    "k": "원리",
    "v": "QT 간격은 <b>심실의 탈분극 시작부터 재분극이 끝날 때까지</b>다. 재분극은 <b>K⁺ 이 세포 밖으로 나가는 전류(주로 IKr)</b>가 만들고, 이 전류가 약물·전해질·선천 이온통로 이상으로 <b>느려지면 T파가 늦게 끝나 QT 가 길어진다</b>.<br> <b>왜 심박수로 보정하는가</b> — 재분극 시간은 심박수가 느릴수록 생리적으로 길어진다. 그래서 <b>QTc = QT/√RR(Bazett)</b> 로 60회/분 기준에 맞춘다. 이 환자는 RR 1.10 s(55회/분)이므로 <b>√RR≈1.05, QTc≈0.52/1.05≈0.50 s</b> — 남자 기준 <b>0.45 s 를 훌쩍 넘는</b> 뚜렷한 연장이다.<br> <b>왜 위험한가</b> — 재분극이 길어지면 <b>조기후탈분극(EAD)</b> 이 생기고, 이것이 <b>비틀림 심실빈맥(torsades de pointes)</b> 의 방아쇠가 된다. QT 를 더 늘리는 약(5-HT3 길항제·드로페리돌·할로페리돌·일부 항생제)과 <b>저K·저Mg</b> 는 위험을 곱한다.<br> <b>그래서 주술기 계획</b> — PONV 예방에서 <b>온단세트론·드로페리돌을 빼고 덱사메타손·아프레피탄트로 대체</b>하며, K·Mg 를 정상 상단으로 교정하고 수술 중 QT 를 감시한다. 「심전도 판독 → 약물 선택」이 한 줄로 이어지는 문항이다."
   },
   {
    "k": "비교",
    "v": "<table><thead><tr><th style=\"width:26%\">심전도 소견</th><th style=\"width:30%\">이 기록에서의 근거</th><th>주술기 대응</th></tr></thead><tbody> <tr><td><b>QT 연장(정답)</b></td><td><b>QT≈0.52 s · RR 1.10 s → QTc≈0.50 s</b>, T파 낮고 넓음</td><td><b>온단세트론·드로페리돌 회피</b>, K·Mg 교정, QT 감시</td></tr> <tr><td>고칼륨혈증</td><td>T파가 <b>뾰족·좁은 텐트형</b>이어야 함 — 여기선 낮고 넓음</td><td>칼슘·인슐린-포도당 후 수술</td></tr> <tr><td>좌심실비대</td><td>SV1+RV5 ≥3.5 mV 등 전압 기준 — 여기선 ≈2.2 mV</td><td>PONV 약 제한 없음</td></tr> <tr><td>완전방실차단</td><td>P–QRS 해리 · 심실 이탈율동 — 여기선 매 P 뒤 QRS</td><td>임시 조율기</td></tr> </tbody></table> <b>가장 가까운 오답은 ④</b> — 같은 「QT 연장」 판독이지만 <b>드로페리돌은 온단세트론보다 QT 경고가 더 강한 약(블랙박스)</b> 이라 「우선 투여」는 판독을 맞히고도 처치에서 틀리는 자리다."
   },
   {
    "k": "오답 이유",
    "v": "① 좌심실비대는 SV1+RV5 ≥3.5 mV 또는 RaVL ≥1.1 mV 같은 전압 기준을 채워야 하고, 설령 비대가 있어도 QT 연장이 함께 있으면 예방약 제한이 생긴다. 이 선지가 정답이 되려면 QT 가 정상이고 전압 기준을 넘어야 한다.\n② 고칼륨혈증은 T파가 좁고 뾰족한 텐트형으로 서고 QRS 가 넓어진다. 이 기록은 T파가 낮고 넓어 정반대다. 이 선지가 정답이 되려면 뾰족한 T파와 함께 K⁺ 상승의 임상 배경이 있어야 한다.\n④ 판독(QT 연장)은 맞지만 드로페리돌은 QT 연장 경고가 더 강한 약이라 QT 연장 환자에게는 온단세트론보다 먼저 쓸 이유가 없다. 이 선지가 정답이 되려면 QT 가 정상이고 5-HT3 길항제를 못 쓰는 별도 사유가 있어야 한다.\n⑤ 완전방실차단은 P파와 QRS 가 서로 무관하게 각자 규칙적으로 뛴다(방실해리). 여기서는 모든 P 뒤에 일정한 간격으로 QRS 가 따른다. 이 선지가 정답이 되려면 P–QRS 해리와 느린 이탈율동이 보여야 한다."
   },
   {
    "k": "함정",
    "v": "서맥에서는 「QT < RR 의 절반」 눈대중이 틀어진다. 반드시 QT 를 재서 √RR 로 보정한다 — 55회/분에서 0.52 s 는 QTc ≈0.50 s."
   },
   {
    "k": "학습목표",
    "v": "수술 전 심전도에서 QT 연장을 읽고 주술기 약물 선택에 연결"
   },
   {
    "k": "근거·출처",
    "v": "PTB-XL 기록 라벨 LNGQT(2인 심장내과 검증) · 작성자 원신호 계측: QT≈520 ms, RR 1.096 s, QTcB≈497 ms · Fourth Consensus Guidelines for the Management of PONV (Anesth Analg 2020) — QT 연장 환자에서 5-HT3 길항제·드로페리돌 주의 ## 출처 PTB-XL ECG dataset v1.0.3 (PhysioNet, CC BY 4.0) · record 320 · Creative Commons Attribution 4.0 International · https://physionet.org/content/ptb-xl/1.0.3/LICENSE.txt"
   }
  ],
  "source": "의대_시험지_제작 오픈데이터 영상 세트 / 20260913T053235Z_일일영상_2026-09-13_10units_9q_7072fb0c",
  "vitals": [],
  "labs": [],
  "appendix": null,
  "figureImg": {
   "src": "assets/imaging/imaging-2026-0001.png",
   "caption": "12유도 심전도, 25 mm/s · 10 mm/mV, 3×4 + II 리듬 스트립 (PTB-XL ECG dataset, PhysioNet, CC BY 4.0 — 원신호 그대로 작도)",
   "alt": "ECG 영상"
  },
  "attribution": {
   "dataset": "PTB-XL, a large publicly available electrocardiography dataset",
   "license": "Creative Commons Attribution 4.0 International",
   "license_url": "https://physionet.org/content/ptb-xl/1.0.3/LICENSE.txt",
   "url": "https://physionet.org/content/ptb-xl/1.0.3/records500/00000/#files-panel",
   "asset_id": "PTBXL-00320",
   "text": "PTB-XL ECG dataset v1.0.3 (PhysioNet, CC BY 4.0) · record 320"
  },
  "run_id": "20260913T053235Z_일일영상_2026-09-13_10units_9q_7072fb0c",
  "qid": "Q0001"
 },
 {
  "id": "imaging-2026-0018",
  "exam": "imaging",
  "style": "usmle_style",
  "styleLabel": "USMLE형",
  "subject": "산부인과",
  "subject_file": "산부인과",
  "setSubject": "통합(생식의학·산과 마취·흉부 해부)",
  "subtopic": "부인과 — 골반통·부인과 해부·자궁외임신",
  "type": "부인과 — 골반통·부인과 해부·자궁외임신",
  "modality": "",
  "step": "Step 2",
  "difficulty": 5,
  "difficultyLabel": "최상",
  "created": "2026-09-13",
  "vignette": "A 26-year-old woman, gravida 1, comes to the emergency department because of mild left lower abdominal pain for 1 day. Her last menstrual period was 6 weeks ago and a home pregnancy test was positive. She has no vaginal bleeding. Her pulse is 78/min and blood pressure is 116/74 mm Hg. The abdomen is soft without rebound or guarding. Transvaginal ultrasonography shows no intrauterine gestational sac, no adnexal mass, and no free fluid. Serum β-hCG concentration is 900 mIU/mL and hemoglobin is 12.8 g/dL.",
  "question": "Which of the following is the most appropriate next step in management?",
  "options": [
   "Diagnostic laparoscopy",
   "Uterine aspiration with histologic examination",
   "Oral misoprostol",
   "Repeat serum β-hCG measurement in 48 hours",
   "Single-dose intramuscular methotrexate"
  ],
  "answer": 4,
  "explanationText": "- 정답 핵심: This is a pregnancy of unknown location: a positive pregnancy test with neither an intrauterine nor an ectopic pregnancy seen. At a β-hCG of 900 mIU/mL — below the discriminatory level (about 1500–3500 mIU/mL) — a normal early intrauterine pregnancy can still be invisible, so the diagnosis cannot be made from one measurement. Because she is hemodynamically stable with no peritoneal signs, no mass and no free fluid, the correct step is to follow the trend with a repeat β-hCG in 48 hours (and repeat ultrasonography once the level reaches the discriminatory zone).\n- 원리: The <b>discriminatory level</b> is the β-hCG concentration above which a viable intrauterine pregnancy should be seen on transvaginal ultrasonography — about <b>1500–2000 mIU/mL</b>, and conservatively as high as <b>3500 mIU/mL</b> to avoid misdiagnosing a wanted pregnancy. <b>Below</b> that level an empty uterus proves nothing: the pregnancy may simply be too small to see. That is why a single value of 900 mIU/mL cannot separate (a) an early normal intrauterine pregnancy, (b) a failing intrauterine pregnancy, and (c) an ectopic pregnancy.<br> <b>Why the 48-hour rise separates them</b> — a viable intrauterine pregnancy at this level rises by at least <b>about 49 % in 48 hours</b> (the minimum rise is lower at higher starting levels); a fall of at least 21 % suggests a failing pregnancy; a slower rise or a plateau suggests ectopic or non-viable pregnancy. Interpreting the trend then guides the next test: repeat ultrasonography once the level crosses the discriminatory zone, or uterine aspiration to prove or exclude chorionic villi when the pregnancy is non-viable.<br> <b>Why nothing is treated yet</b> — methotrexate given to a woman with an unrecognized early intrauterine pregnancy is teratogenic and abortifacient; laparoscopy without a mass or free fluid has a low yield and its own risks; aspiration or misoprostol interrupt a possibly normal pregnancy. Expectant surveillance is safe only because she is <b>stable</b>: normal pulse and blood pressure, soft abdomen, no free fluid, normal hemoglobin — the moment any of these changes, the pathway becomes surgical.\n- 비교: <table><thead><tr><th style=\"width:32%\">Scenario</th><th style=\"width:34%\">Key numbers / findings</th><th>Correct step</th></tr></thead><tbody> <tr><td><b>PUL, stable, β-hCG below discriminatory level (this patient)</b></td><td><b>900 mIU/mL, no mass, no free fluid, normal vitals</b></td><td><b>repeat β-hCG in 48 h</b>, ultrasound again when ≥ discriminatory level</td></tr> <tr><td>PUL, stable, β-hCG above discriminatory level</td><td>e.g. ≥3500 mIU/mL and empty uterus, or abnormal rise</td><td>non-viable: uterine aspiration to look for villi; if none, treat as ectopic (methotrexate)</td></tr> <tr><td>Ectopic confirmed, stable, unruptured</td><td>adnexal mass with yolk sac/embryo, hCG <5000, no cardiac activity, no contraindication</td><td>methotrexate</td></tr> <tr><td>Any ectopic, unstable or ruptured</td><td>hypotension, peritoneal signs, free fluid, falling hemoglobin</td><td>immediate laparoscopy/laparotomy</td></tr> </tbody></table> The <b>closest wrong answer is methotrexate</b>: the reflex 'no intrauterine pregnancy → ectopic' ignores the discriminatory level. Methotrexate is justified only once an intrauterine pregnancy has been excluded — by a level above the discriminatory zone with an empty uterus, an abnormal trend, or aspiration showing no villi.\n- 오답 이유:\n  - (A) Diagnostic laparoscopy is the step for a hemodynamically unstable patient or one with peritoneal signs or free fluid suggesting rupture. This patient is stable with a soft abdomen and no fluid. This option would be correct only if she had hypotension, rebound tenderness, or hemoperitoneum on ultrasonography.\n  - (B) Uterine aspiration to look for chorionic villi is used once the pregnancy is known to be non-viable (abnormal β-hCG trend or empty uterus above the discriminatory level) to distinguish failed intrauterine from ectopic pregnancy. This option would be correct only after a non-viable trend had been documented.\n  - (C) Misoprostol is a treatment for a confirmed failed intrauterine pregnancy (early pregnancy loss). Nothing here proves the pregnancy is intrauterine or non-viable. This option would be correct only if ultrasonography had shown an intrauterine sac with an embryo without cardiac activity.\n  - (E) Methotrexate is given only after an intrauterine pregnancy has been excluded, because it is teratogenic and abortifacient. At 900 mIU/mL an early normal intrauterine pregnancy can still be invisible. This option would be correct only if an adnexal ectopic mass were seen or the β-hCG trend were abnormal with an empty uterus above the discriminatory level.\n- 함정: 'No intrauterine pregnancy' on ultrasound is only meaningful above the discriminatory β-hCG level. Below it, the empty uterus is uninformative and the trend is the test.\n- 학습목표: 식별기준치 아래의 위치미상 임신에서 혈역학적 안정 시 48시간 β-hCG 추적을 고른다\n- 근거·출처: ACOG Practice Bulletin No. 193: Tubal Ectopic Pregnancy (2018) — pregnancy of unknown location, discriminatory level, serial β-hCG · Barnhart KT et al. Symptomatic patients with an early viable intrauterine pregnancy: hCG curves redefined (Obstet Gynecol 2004) — minimum 48-h rise",
  "explanationItems": [
   {
    "k": "정답 핵심",
    "v": "This is a pregnancy of unknown location: a positive pregnancy test with neither an intrauterine nor an ectopic pregnancy seen. At a β-hCG of 900 mIU/mL — below the discriminatory level (about 1500–3500 mIU/mL) — a normal early intrauterine pregnancy can still be invisible, so the diagnosis cannot be made from one measurement. Because she is hemodynamically stable with no peritoneal signs, no mass and no free fluid, the correct step is to follow the trend with a repeat β-hCG in 48 hours (and repeat ultrasonography once the level reaches the discriminatory zone)."
   },
   {
    "k": "원리",
    "v": "The <b>discriminatory level</b> is the β-hCG concentration above which a viable intrauterine pregnancy should be seen on transvaginal ultrasonography — about <b>1500–2000 mIU/mL</b>, and conservatively as high as <b>3500 mIU/mL</b> to avoid misdiagnosing a wanted pregnancy. <b>Below</b> that level an empty uterus proves nothing: the pregnancy may simply be too small to see. That is why a single value of 900 mIU/mL cannot separate (a) an early normal intrauterine pregnancy, (b) a failing intrauterine pregnancy, and (c) an ectopic pregnancy.<br> <b>Why the 48-hour rise separates them</b> — a viable intrauterine pregnancy at this level rises by at least <b>about 49 % in 48 hours</b> (the minimum rise is lower at higher starting levels); a fall of at least 21 % suggests a failing pregnancy; a slower rise or a plateau suggests ectopic or non-viable pregnancy. Interpreting the trend then guides the next test: repeat ultrasonography once the level crosses the discriminatory zone, or uterine aspiration to prove or exclude chorionic villi when the pregnancy is non-viable.<br> <b>Why nothing is treated yet</b> — methotrexate given to a woman with an unrecognized early intrauterine pregnancy is teratogenic and abortifacient; laparoscopy without a mass or free fluid has a low yield and its own risks; aspiration or misoprostol interrupt a possibly normal pregnancy. Expectant surveillance is safe only because she is <b>stable</b>: normal pulse and blood pressure, soft abdomen, no free fluid, normal hemoglobin — the moment any of these changes, the pathway becomes surgical."
   },
   {
    "k": "비교",
    "v": "<table><thead><tr><th style=\"width:32%\">Scenario</th><th style=\"width:34%\">Key numbers / findings</th><th>Correct step</th></tr></thead><tbody> <tr><td><b>PUL, stable, β-hCG below discriminatory level (this patient)</b></td><td><b>900 mIU/mL, no mass, no free fluid, normal vitals</b></td><td><b>repeat β-hCG in 48 h</b>, ultrasound again when ≥ discriminatory level</td></tr> <tr><td>PUL, stable, β-hCG above discriminatory level</td><td>e.g. ≥3500 mIU/mL and empty uterus, or abnormal rise</td><td>non-viable: uterine aspiration to look for villi; if none, treat as ectopic (methotrexate)</td></tr> <tr><td>Ectopic confirmed, stable, unruptured</td><td>adnexal mass with yolk sac/embryo, hCG <5000, no cardiac activity, no contraindication</td><td>methotrexate</td></tr> <tr><td>Any ectopic, unstable or ruptured</td><td>hypotension, peritoneal signs, free fluid, falling hemoglobin</td><td>immediate laparoscopy/laparotomy</td></tr> </tbody></table> The <b>closest wrong answer is methotrexate</b>: the reflex 'no intrauterine pregnancy → ectopic' ignores the discriminatory level. Methotrexate is justified only once an intrauterine pregnancy has been excluded — by a level above the discriminatory zone with an empty uterus, an abnormal trend, or aspiration showing no villi."
   },
   {
    "k": "오답 이유",
    "v": "(A) Diagnostic laparoscopy is the step for a hemodynamically unstable patient or one with peritoneal signs or free fluid suggesting rupture. This patient is stable with a soft abdomen and no fluid. This option would be correct only if she had hypotension, rebound tenderness, or hemoperitoneum on ultrasonography.\n(B) Uterine aspiration to look for chorionic villi is used once the pregnancy is known to be non-viable (abnormal β-hCG trend or empty uterus above the discriminatory level) to distinguish failed intrauterine from ectopic pregnancy. This option would be correct only after a non-viable trend had been documented.\n(C) Misoprostol is a treatment for a confirmed failed intrauterine pregnancy (early pregnancy loss). Nothing here proves the pregnancy is intrauterine or non-viable. This option would be correct only if ultrasonography had shown an intrauterine sac with an embryo without cardiac activity.\n(E) Methotrexate is given only after an intrauterine pregnancy has been excluded, because it is teratogenic and abortifacient. At 900 mIU/mL an early normal intrauterine pregnancy can still be invisible. This option would be correct only if an adnexal ectopic mass were seen or the β-hCG trend were abnormal with an empty uterus above the discriminatory level."
   },
   {
    "k": "함정",
    "v": "'No intrauterine pregnancy' on ultrasound is only meaningful above the discriminatory β-hCG level. Below it, the empty uterus is uninformative and the trend is the test."
   },
   {
    "k": "학습목표",
    "v": "식별기준치 아래의 위치미상 임신에서 혈역학적 안정 시 48시간 β-hCG 추적을 고른다"
   },
   {
    "k": "근거·출처",
    "v": "ACOG Practice Bulletin No. 193: Tubal Ectopic Pregnancy (2018) — pregnancy of unknown location, discriminatory level, serial β-hCG · Barnhart KT et al. Symptomatic patients with an early viable intrauterine pregnancy: hCG curves redefined (Obstet Gynecol 2004) — minimum 48-h rise"
   }
  ],
  "source": "의대_시험지_제작 오픈데이터 영상 세트 / 20260913T201606Z_일일영상_2026-09-14_9units_9q_85b9cadf",
  "vitals": [],
  "labs": [],
  "appendix": null,
  "figureImg": null,
  "attribution": {
   "dataset": "",
   "license": "",
   "license_url": "",
   "url": "",
   "asset_id": "",
   "text": ""
  },
  "run_id": "20260913T201606Z_일일영상_2026-09-14_9units_9q_85b9cadf",
  "qid": "Q0009"
 },
 {
  "id": "imaging-2026-0017",
  "exam": "imaging",
  "style": "kmle_style",
  "styleLabel": "국시형",
  "subject": "산부인과",
  "subject_file": "산부인과",
  "setSubject": "통합(생식의학·산과 마취·흉부 해부)",
  "subtopic": "부인과 — 골반통·부인과 해부·자궁외임신",
  "type": "부인과 — 골반통·부인과 해부·자궁외임신",
  "modality": "",
  "step": "",
  "difficulty": 4,
  "difficultyLabel": "상",
  "created": "2026-09-13",
  "vignette": "45세 여자가 자궁근종으로 복식 전자궁절제술을 받았다. 수술 3일째부터 왼쪽 옆구리 통증과 38.2 ℃ 발열이 생겼다. 조영증강 CT에서 왼쪽 수신증이 있고 자궁목이 있던 자리의 왼쪽 옆에서 조영제가 새어 나온다.",
  "question": "손상된 구조물이 이 부위에서 바로 아래로 지나가는 혈관은?",
  "options": [
   "속엉덩동맥",
   "폐쇄동맥",
   "아래방광동맥",
   "자궁동맥",
   "난소동맥"
  ],
  "answer": 4,
  "explanationText": "- 정답 핵심: 자궁목 옆의 조영제 누출과 같은 쪽 수신증은 요관 손상이다. 요관은 골반에서 넓은인대 바닥의 자궁목 외측 약 1.5~2 cm 지점에서 자궁동맥 바로 아래를 지나 방광으로 들어가며(「다리 아래 물」), 자궁동맥을 결찰·절단하는 이 단계가 요관 손상이 가장 잦은 지점이다.\n- 원리: 요관은 콩팥에서 방광까지 <b>복막 뒤</b>를 내려오며 골반에서 세 번 다른 구조와 만난다. ① <b>골반 가장자리</b>에서 온엉덩동맥 갈림 앞을 지나며 <b>난소걸이인대(난소혈관)</b> 와 나란히 가까이 놓인다. ② 골반 옆벽을 따라 내려와 <b>넓은인대 바닥(자궁목 외측 약 1.5~2 cm, 질천장 높이)</b>에서 <b>속엉덩동맥에서 온 자궁동맥이 요관 위를 앞으로 가로지른다</b> — 「다리(자궁동맥) 아래로 물(요관)이 흐른다」. ③ 마지막으로 방광 뒤벽을 비스듬히 뚫고 들어간다.<br> <b>왜 자궁절제술의 요관 손상은 ②에서 가장 많은가</b> — 자궁동맥을 결찰하려면 자궁목 옆의 조직을 겸자로 잡는데, 이때 요관이 자궁동맥에서 <b>1~2 cm 아래·뒤</b>에 있어 근종으로 자궁이 커지거나 출혈로 시야가 나쁘면 함께 잡히거나 잘리며, 결찰 시 열이 닿아 <b>지연 괴사 → 누출·요종(urinoma)</b> 이 된다. 그래서 수술 직후가 아니라 <b>수일 뒤 옆구리 통증·발열· 수신증</b>으로 나타난다.<br> <b>①과 ②를 어떻게 가르나</b> — 난소걸이인대를 자를 때(양쪽 난소·난관 절제)는 골반 가장자리(①)가 위험하고, 자궁동맥을 자를 때는 자궁목 옆(②)이 위험하다. 발문의 「자궁목이 있던 자리의 옆」이 ②를 가리키고, 그 자리에서 요관 <b>위</b>를 지나는 혈관은 자궁동맥뿐이다.\n- 비교: <table><thead><tr><th style=\"width:26%\">교차 부위</th><th style=\"width:30%\">요관 위를 지나는 구조</th><th>손상되는 수술 단계 · 표지</th></tr></thead><tbody> <tr><td><b>넓은인대 바닥, 자궁목 외측 1.5~2 cm(정답 자리)</b></td><td><b>자궁동맥</b>(요관 위를 앞으로 가로지름)</td><td><b>자궁동맥 결찰</b> — 자궁목 옆 누출·수신증</td></tr> <tr><td>골반 가장자리</td><td>난소걸이인대 속 <b>난소동·정맥</b>(요관과 나란히)</td><td>난소걸이인대 결찰(난소 절제) — 더 위쪽 누출</td></tr> <tr><td>방광 진입부</td><td>—(방광벽 안 터널)</td><td>방광 박리·질천장 봉합 — 요관질누공</td></tr> </tbody></table> <b>가장 가까운 오답은 난소동맥</b> — 역시 요관과 만나는 혈관이지만 자리가 <b>골반 가장자리(위)</b>이고 요관 위를 가로지르지 않고 나란히 간다. 발문의 「자궁목 옆」이라는 위치가 자궁동맥을 고르게 한다.\n- 오답 이유:\n  - ① 속엉덩동맥은 골반 옆벽에서 요관의 뒤·바깥쪽을 내려가며 요관 위를 가로지르지 않는다. 자궁동맥은 그 앞가지일 뿐이다. 이 선지가 정답이 되려면 「요관 위를 가로지르는 혈관」이 아니라 「그 혈관의 기원」을 물어야 한다.\n  - ② 폐쇄동맥은 골반 옆벽을 따라 폐쇄구멍으로 나가며 요관보다 바깥·아래에 있어 자궁절제술의 요관 손상과 무관하다. 이 선지가 정답이 되려면 림프절 절제 중 폐쇄오목의 손상을 물어야 한다.\n  - ③ 아래방광동맥은 방광 바닥과 요관 아래 끝에 가지를 주지만 요관 위를 가로질러 자궁목 옆을 지나지 않는다. 이 선지가 정답이 되려면 방광 진입부 근처의 혈액 공급을 물어야 한다.\n  - ⑤ 난소동맥은 난소걸이인대 속에서 골반 가장자리의 요관과 나란히 지나므로 난소·난관을 함께 뗄 때 위험한 자리다. 이 선지가 정답이 되려면 누출 부위가 자궁목 옆이 아니라 골반 가장자리 높이여야 한다.\n- 함정: 「요관 손상 = 난소혈관」으로 외우면 틀린다. 어느 인대를 자르는 단계인지(난소걸이인대 vs 자궁동맥)로 부위가 갈린다.\n- 학습목표: 자궁절제술 중 요관 손상 호발 부위와 자궁동맥의 교차 관계\n- 근거·출처: Moore Clinically Oriented Anatomy — 골반 요관의 주행과 자궁동맥 교차(water under the bridge) · Te Linde's Operative Gynecology — 자궁절제술 중 요관 손상 호발 부위(자궁동맥 결찰부·난소걸이인대·질천장)",
  "explanationItems": [
   {
    "k": "정답 핵심",
    "v": "자궁목 옆의 조영제 누출과 같은 쪽 수신증은 요관 손상이다. 요관은 골반에서 넓은인대 바닥의 자궁목 외측 약 1.5~2 cm 지점에서 자궁동맥 바로 아래를 지나 방광으로 들어가며(「다리 아래 물」), 자궁동맥을 결찰·절단하는 이 단계가 요관 손상이 가장 잦은 지점이다."
   },
   {
    "k": "원리",
    "v": "요관은 콩팥에서 방광까지 <b>복막 뒤</b>를 내려오며 골반에서 세 번 다른 구조와 만난다. ① <b>골반 가장자리</b>에서 온엉덩동맥 갈림 앞을 지나며 <b>난소걸이인대(난소혈관)</b> 와 나란히 가까이 놓인다. ② 골반 옆벽을 따라 내려와 <b>넓은인대 바닥(자궁목 외측 약 1.5~2 cm, 질천장 높이)</b>에서 <b>속엉덩동맥에서 온 자궁동맥이 요관 위를 앞으로 가로지른다</b> — 「다리(자궁동맥) 아래로 물(요관)이 흐른다」. ③ 마지막으로 방광 뒤벽을 비스듬히 뚫고 들어간다.<br> <b>왜 자궁절제술의 요관 손상은 ②에서 가장 많은가</b> — 자궁동맥을 결찰하려면 자궁목 옆의 조직을 겸자로 잡는데, 이때 요관이 자궁동맥에서 <b>1~2 cm 아래·뒤</b>에 있어 근종으로 자궁이 커지거나 출혈로 시야가 나쁘면 함께 잡히거나 잘리며, 결찰 시 열이 닿아 <b>지연 괴사 → 누출·요종(urinoma)</b> 이 된다. 그래서 수술 직후가 아니라 <b>수일 뒤 옆구리 통증·발열· 수신증</b>으로 나타난다.<br> <b>①과 ②를 어떻게 가르나</b> — 난소걸이인대를 자를 때(양쪽 난소·난관 절제)는 골반 가장자리(①)가 위험하고, 자궁동맥을 자를 때는 자궁목 옆(②)이 위험하다. 발문의 「자궁목이 있던 자리의 옆」이 ②를 가리키고, 그 자리에서 요관 <b>위</b>를 지나는 혈관은 자궁동맥뿐이다."
   },
   {
    "k": "비교",
    "v": "<table><thead><tr><th style=\"width:26%\">교차 부위</th><th style=\"width:30%\">요관 위를 지나는 구조</th><th>손상되는 수술 단계 · 표지</th></tr></thead><tbody> <tr><td><b>넓은인대 바닥, 자궁목 외측 1.5~2 cm(정답 자리)</b></td><td><b>자궁동맥</b>(요관 위를 앞으로 가로지름)</td><td><b>자궁동맥 결찰</b> — 자궁목 옆 누출·수신증</td></tr> <tr><td>골반 가장자리</td><td>난소걸이인대 속 <b>난소동·정맥</b>(요관과 나란히)</td><td>난소걸이인대 결찰(난소 절제) — 더 위쪽 누출</td></tr> <tr><td>방광 진입부</td><td>—(방광벽 안 터널)</td><td>방광 박리·질천장 봉합 — 요관질누공</td></tr> </tbody></table> <b>가장 가까운 오답은 난소동맥</b> — 역시 요관과 만나는 혈관이지만 자리가 <b>골반 가장자리(위)</b>이고 요관 위를 가로지르지 않고 나란히 간다. 발문의 「자궁목 옆」이라는 위치가 자궁동맥을 고르게 한다."
   },
   {
    "k": "오답 이유",
    "v": "① 속엉덩동맥은 골반 옆벽에서 요관의 뒤·바깥쪽을 내려가며 요관 위를 가로지르지 않는다. 자궁동맥은 그 앞가지일 뿐이다. 이 선지가 정답이 되려면 「요관 위를 가로지르는 혈관」이 아니라 「그 혈관의 기원」을 물어야 한다.\n② 폐쇄동맥은 골반 옆벽을 따라 폐쇄구멍으로 나가며 요관보다 바깥·아래에 있어 자궁절제술의 요관 손상과 무관하다. 이 선지가 정답이 되려면 림프절 절제 중 폐쇄오목의 손상을 물어야 한다.\n③ 아래방광동맥은 방광 바닥과 요관 아래 끝에 가지를 주지만 요관 위를 가로질러 자궁목 옆을 지나지 않는다. 이 선지가 정답이 되려면 방광 진입부 근처의 혈액 공급을 물어야 한다.\n⑤ 난소동맥은 난소걸이인대 속에서 골반 가장자리의 요관과 나란히 지나므로 난소·난관을 함께 뗄 때 위험한 자리다. 이 선지가 정답이 되려면 누출 부위가 자궁목 옆이 아니라 골반 가장자리 높이여야 한다."
   },
   {
    "k": "함정",
    "v": "「요관 손상 = 난소혈관」으로 외우면 틀린다. 어느 인대를 자르는 단계인지(난소걸이인대 vs 자궁동맥)로 부위가 갈린다."
   },
   {
    "k": "학습목표",
    "v": "자궁절제술 중 요관 손상 호발 부위와 자궁동맥의 교차 관계"
   },
   {
    "k": "근거·출처",
    "v": "Moore Clinically Oriented Anatomy — 골반 요관의 주행과 자궁동맥 교차(water under the bridge) · Te Linde's Operative Gynecology — 자궁절제술 중 요관 손상 호발 부위(자궁동맥 결찰부·난소걸이인대·질천장)"
   }
  ],
  "source": "의대_시험지_제작 오픈데이터 영상 세트 / 20260913T201606Z_일일영상_2026-09-14_9units_9q_85b9cadf",
  "vitals": [],
  "labs": [],
  "appendix": null,
  "figureImg": null,
  "attribution": {
   "dataset": "",
   "license": "",
   "license_url": "",
   "url": "",
   "asset_id": "",
   "text": ""
  },
  "run_id": "20260913T201606Z_일일영상_2026-09-14_9units_9q_85b9cadf",
  "qid": "Q0008"
 },
 {
  "id": "imaging-2026-0016",
  "exam": "imaging",
  "style": "kmle_style",
  "styleLabel": "국시형",
  "subject": "산부인과",
  "subject_file": "산부인과",
  "setSubject": "통합(생식의학·산과 마취·흉부 해부)",
  "subtopic": "부인과 — 골반통·부인과 해부·자궁외임신",
  "type": "부인과 — 골반통·부인과 해부·자궁외임신",
  "modality": "",
  "step": "",
  "difficulty": 3,
  "difficultyLabel": "중",
  "created": "2026-09-13",
  "vignette": "17세 여자가 6개월 전부터 월경 첫 1~2일에 아랫배가 쥐어짜듯 아파 왔다. 통증은 허리와 허벅지로 뻗치고 메스꺼움이 함께 있다. 초경은 13세였고 월경주기는 28일로 규칙적이며 성경험은 없다. 진찰과 골반 초음파에서 이상이 없다.",
  "question": "가장 적절한 치료는?",
  "options": [
   "진단 복강경검사",
   "경험적 항생제 투여",
   "비스테로이드소염제를 월경 시작과 함께 복용",
   "복합 경구피임약을 주기적으로 복용",
   "GnRH 작용제를 3개월 투여"
  ],
  "answer": 3,
  "explanationText": "- 정답 핵심: 초경 후 배란주기가 확립된 뒤 시작되어 월경 시작과 함께 나타나고 1~2일 안에 잦아드는 쥐어짜는 아랫배 통증, 허리·허벅지 방사통과 위장 증상, 정상 골반 소견은 일차 월경곤란증의 전형이다. 원인은 자궁내막에서 만들어지는 프로스타글란딘 F2α 의 과다이므로 프로스타글란딘 합성을 막는 NSAID 가 첫 치료다.\n- 원리: 일차 월경곤란증의 통증은 <b>자궁내막이 떨어져 나갈 때 만들어지는 프로스타글란딘(PGF2α · PGE2)</b> 이 자궁근을 <b>세게, 자주, 기저긴장이 높은 상태로 수축</b>시키고 자궁 혈류를 줄여 <b>허혈성 통증</b>을 만드는 것이다. 배란 후 황체가 만든 프로게스테론이 떨어지면 내막 세포막의 인지질에서 <b>아라키돈산이 풀려 나오고, COX-2 가 이를 프로스타글란딘으로 바꾼다</b> — 그래서 통증은 <b>배란주기가 확립된 초경 1~2년 뒤</b>에 시작되고, <b>월경 시작 직전~첫 1~2일</b>(내막 붕괴·PG 농도 최고)에 가장 심하며, PG 가 장으로 들어가 <b>메스꺼움·설사</b>를 만든다.<br> <b>왜 NSAID 인가</b> — NSAID 는 COX 를 막아 <b>프로스타글란딘 생성 자체를 줄인다</b>. 그래서 통증을 덮는 것이 아니라 원인을 줄이며, 효과를 보려면 <b>월경 시작(또는 통증 시작)과 동시에</b> 먹기 시작해 2~3일 규칙적으로 복용해야 한다 — PG 가 이미 많이 만들어진 뒤에 먹으면 효과가 떨어진다.<br> <b>왜 피임약이 두 번째인가</b> — 복합 경구피임약은 <b>배란을 막고 내막을 얇게 만들어</b> PG 원료 자체를 줄이므로 역시 효과적이지만, 피임이 필요 없고 NSAID 를 아직 써 보지 않은 청소년에서는 <b>NSAID 가 먼저</b>다. 두 약을 <b>충분히 3~6개월</b> 써도 반응이 없을 때 비로소 <b>이차 월경곤란증(자궁내막증 등)</b> 을 의심해 복강경을 고려한다.\n- 비교: <table><thead><tr><th style=\"width:28%\">치료</th><th style=\"width:34%\">기전</th><th>이 환자에서의 자리</th></tr></thead><tbody> <tr><td><b>NSAID(정답)</b></td><td><b>COX 억제 → 프로스타글란딘 생성 감소</b></td><td><b>1차</b> — 월경 시작과 함께 2~3일 규칙 복용</td></tr> <tr><td>복합 경구피임약</td><td>배란 억제·내막 위축 → PG 원료 감소</td><td>피임을 원하거나 NSAID 무효·금기일 때</td></tr> <tr><td>GnRH 작용제</td><td>저에스트로겐 상태로 내막·병변 억제</td><td>확진된 자궁내막증의 2차 치료 — 골밀도 손실로 청소년 1차 아님</td></tr> <tr><td>복강경</td><td>이차 원인(자궁내막증) 확인</td><td>1차·2차 약물에 3~6개월 반응 없을 때</td></tr> </tbody></table> <b>가장 가까운 오답은 복합 경구피임약</b> — 둘 다 1차 약으로 인정되지만 「성경험 없음 · 피임 필요 없음 · 약물 미시도」라는 조건이 NSAID 를 앞세운다. 발문에 「피임을 원한다」 또는 「NSAID 로 조절되지 않는다」가 있으면 피임약이 정답이 된다.\n- 오답 이유:\n  - ① 진단 복강경은 NSAID 와 호르몬 치료에 3~6개월 반응하지 않아 이차 월경곤란증(자궁내막증)이 의심될 때의 단계다. 이 선지가 정답이 되려면 약물치료 실패나 비정상 골반 소견이 발문에 있어야 한다.\n  - ② 항생제는 골반염증질환처럼 감염이 통증의 원인일 때 쓴다. 이 환자는 성경험이 없고 발열·분비물·자궁목 압통이 없다. 이 선지가 정답이 되려면 성경험과 함께 발열·자궁목 움직임 압통이 있어야 한다.\n  - ④ 복합 경구피임약도 일차 월경곤란증에 효과적이지만 피임이 필요 없고 NSAID 를 써 보지 않은 청소년에서는 두 번째다. 이 선지가 정답이 되려면 환자가 피임을 원하거나 NSAID 로 3개월 이상 조절되지 않았어야 한다.\n  - ⑤ GnRH 작용제는 확진된 자궁내막증의 2차 치료이며 저에스트로겐으로 골밀도를 떨어뜨려 청소년의 1차 치료로 쓰지 않는다. 이 선지가 정답이 되려면 복강경으로 자궁내막증이 확진되고 1차 약이 실패했어야 한다.\n- 함정: 「초음파 정상 → 검사 더 하기」로 가지 않는다. 일차 월경곤란증은 진찰이 정상인 것이 진단이고, 치료 반응이 곧 확인이다.\n- 학습목표: 골반 이상이 없는 청소년의 일차 월경곤란증에서 첫 치료로 프로스타글란딘 합성 억제(NSAID)를 고른다\n- 근거·출처: ACOG Committee Opinion No. 760: Dysmenorrhea and Endometriosis in the Adolescent (2018) · 표준 부인과 지식 — 일차 월경곤란증의 프로스타글란딘 기전(Berek & Novak's Gynecology)",
  "explanationItems": [
   {
    "k": "정답 핵심",
    "v": "초경 후 배란주기가 확립된 뒤 시작되어 월경 시작과 함께 나타나고 1~2일 안에 잦아드는 쥐어짜는 아랫배 통증, 허리·허벅지 방사통과 위장 증상, 정상 골반 소견은 일차 월경곤란증의 전형이다. 원인은 자궁내막에서 만들어지는 프로스타글란딘 F2α 의 과다이므로 프로스타글란딘 합성을 막는 NSAID 가 첫 치료다."
   },
   {
    "k": "원리",
    "v": "일차 월경곤란증의 통증은 <b>자궁내막이 떨어져 나갈 때 만들어지는 프로스타글란딘(PGF2α · PGE2)</b> 이 자궁근을 <b>세게, 자주, 기저긴장이 높은 상태로 수축</b>시키고 자궁 혈류를 줄여 <b>허혈성 통증</b>을 만드는 것이다. 배란 후 황체가 만든 프로게스테론이 떨어지면 내막 세포막의 인지질에서 <b>아라키돈산이 풀려 나오고, COX-2 가 이를 프로스타글란딘으로 바꾼다</b> — 그래서 통증은 <b>배란주기가 확립된 초경 1~2년 뒤</b>에 시작되고, <b>월경 시작 직전~첫 1~2일</b>(내막 붕괴·PG 농도 최고)에 가장 심하며, PG 가 장으로 들어가 <b>메스꺼움·설사</b>를 만든다.<br> <b>왜 NSAID 인가</b> — NSAID 는 COX 를 막아 <b>프로스타글란딘 생성 자체를 줄인다</b>. 그래서 통증을 덮는 것이 아니라 원인을 줄이며, 효과를 보려면 <b>월경 시작(또는 통증 시작)과 동시에</b> 먹기 시작해 2~3일 규칙적으로 복용해야 한다 — PG 가 이미 많이 만들어진 뒤에 먹으면 효과가 떨어진다.<br> <b>왜 피임약이 두 번째인가</b> — 복합 경구피임약은 <b>배란을 막고 내막을 얇게 만들어</b> PG 원료 자체를 줄이므로 역시 효과적이지만, 피임이 필요 없고 NSAID 를 아직 써 보지 않은 청소년에서는 <b>NSAID 가 먼저</b>다. 두 약을 <b>충분히 3~6개월</b> 써도 반응이 없을 때 비로소 <b>이차 월경곤란증(자궁내막증 등)</b> 을 의심해 복강경을 고려한다."
   },
   {
    "k": "비교",
    "v": "<table><thead><tr><th style=\"width:28%\">치료</th><th style=\"width:34%\">기전</th><th>이 환자에서의 자리</th></tr></thead><tbody> <tr><td><b>NSAID(정답)</b></td><td><b>COX 억제 → 프로스타글란딘 생성 감소</b></td><td><b>1차</b> — 월경 시작과 함께 2~3일 규칙 복용</td></tr> <tr><td>복합 경구피임약</td><td>배란 억제·내막 위축 → PG 원료 감소</td><td>피임을 원하거나 NSAID 무효·금기일 때</td></tr> <tr><td>GnRH 작용제</td><td>저에스트로겐 상태로 내막·병변 억제</td><td>확진된 자궁내막증의 2차 치료 — 골밀도 손실로 청소년 1차 아님</td></tr> <tr><td>복강경</td><td>이차 원인(자궁내막증) 확인</td><td>1차·2차 약물에 3~6개월 반응 없을 때</td></tr> </tbody></table> <b>가장 가까운 오답은 복합 경구피임약</b> — 둘 다 1차 약으로 인정되지만 「성경험 없음 · 피임 필요 없음 · 약물 미시도」라는 조건이 NSAID 를 앞세운다. 발문에 「피임을 원한다」 또는 「NSAID 로 조절되지 않는다」가 있으면 피임약이 정답이 된다."
   },
   {
    "k": "오답 이유",
    "v": "① 진단 복강경은 NSAID 와 호르몬 치료에 3~6개월 반응하지 않아 이차 월경곤란증(자궁내막증)이 의심될 때의 단계다. 이 선지가 정답이 되려면 약물치료 실패나 비정상 골반 소견이 발문에 있어야 한다.\n② 항생제는 골반염증질환처럼 감염이 통증의 원인일 때 쓴다. 이 환자는 성경험이 없고 발열·분비물·자궁목 압통이 없다. 이 선지가 정답이 되려면 성경험과 함께 발열·자궁목 움직임 압통이 있어야 한다.\n④ 복합 경구피임약도 일차 월경곤란증에 효과적이지만 피임이 필요 없고 NSAID 를 써 보지 않은 청소년에서는 두 번째다. 이 선지가 정답이 되려면 환자가 피임을 원하거나 NSAID 로 3개월 이상 조절되지 않았어야 한다.\n⑤ GnRH 작용제는 확진된 자궁내막증의 2차 치료이며 저에스트로겐으로 골밀도를 떨어뜨려 청소년의 1차 치료로 쓰지 않는다. 이 선지가 정답이 되려면 복강경으로 자궁내막증이 확진되고 1차 약이 실패했어야 한다."
   },
   {
    "k": "함정",
    "v": "「초음파 정상 → 검사 더 하기」로 가지 않는다. 일차 월경곤란증은 진찰이 정상인 것이 진단이고, 치료 반응이 곧 확인이다."
   },
   {
    "k": "학습목표",
    "v": "골반 이상이 없는 청소년의 일차 월경곤란증에서 첫 치료로 프로스타글란딘 합성 억제(NSAID)를 고른다"
   },
   {
    "k": "근거·출처",
    "v": "ACOG Committee Opinion No. 760: Dysmenorrhea and Endometriosis in the Adolescent (2018) · 표준 부인과 지식 — 일차 월경곤란증의 프로스타글란딘 기전(Berek & Novak's Gynecology)"
   }
  ],
  "source": "의대_시험지_제작 오픈데이터 영상 세트 / 20260913T201606Z_일일영상_2026-09-14_9units_9q_85b9cadf",
  "vitals": [],
  "labs": [],
  "appendix": null,
  "figureImg": null,
  "attribution": {
   "dataset": "",
   "license": "",
   "license_url": "",
   "url": "",
   "asset_id": "",
   "text": ""
  },
  "run_id": "20260913T201606Z_일일영상_2026-09-14_9units_9q_85b9cadf",
  "qid": "Q0007"
 },
 {
  "id": "imaging-2026-0015",
  "exam": "imaging",
  "style": "usmle_style",
  "styleLabel": "USMLE형",
  "subject": "산부인과",
  "subject_file": "산부인과",
  "setSubject": "통합(생식의학·산과 마취·흉부 해부)",
  "subtopic": "산과 — 분만 중 태아감시·산과 마취",
  "type": "산과 — 분만 중 태아감시·산과 마취",
  "modality": "",
  "step": "Step 2",
  "difficulty": 3,
  "difficultyLabel": "중",
  "created": "2026-09-13",
  "vignette": "A 32-year-old woman, gravida 2, para 1, at 38 weeks' gestation is brought to the operating room for emergency cesarean delivery under general anesthesia because of umbilical cord prolapse. She ate a full meal 2 hours ago. Rapid-sequence induction with cricoid pressure is planned.",
  "question": "Which of the following medications is most appropriate to administer immediately before induction to reduce the severity of pneumonitis if aspiration occurs?",
  "options": [
   "Intravenous dexamethasone",
   "Oral sodium citrate",
   "Intravenous ondansetron",
   "Intravenous midazolam",
   "Intravenous glycopyrrolate"
  ],
  "answer": 2,
  "explanationText": "- 정답 핵심: Pregnant women at term are treated as having a full stomach (progesterone-mediated slowing of gastric emptying, raised intragastric pressure, reduced lower esophageal sphincter tone), and this patient has also eaten recently. Aspiration pneumonitis severity depends on gastric pH below about 2.5 and volume above about 25 mL. A non-particulate antacid such as 0.3 M sodium citrate raises gastric pH within minutes and is the one agent that works in the time available before an emergency induction; H2 blockers and metoclopramide are useful adjuncts when there is more time.\n- 원리: Aspiration pneumonitis (Mendelson syndrome) is a <b>chemical burn of the airway by acid</b>, and its severity rises steeply when the aspirated fluid has <b>pH below about 2.5</b> and a volume above about 25 mL (0.4 mL/kg). Pregnancy makes aspiration more likely for anatomical and hormonal reasons: <b>progesterone lowers the tone of the lower esophageal sphincter</b>, the enlarging uterus <b>raises intragastric pressure</b>, and labor, pain and opioids <b>delay gastric emptying</b>. Every laboring woman undergoing general anesthesia is therefore treated as a full-stomach patient — rapid-sequence induction, cricoid pressure, and <b>pharmacologic prophylaxis</b>.<br> <b>Why sodium citrate</b> — a non-particulate (clear) antacid neutralizes the acid already in the stomach, raising pH above 2.5 <b>within minutes</b> and for about 30–60 minutes; it is the only agent whose onset fits an emergency. It must be non-particulate because particulate antacids (aluminium hydroxide, magnesium trisilicate) themselves cause a granulomatous pneumonitis if aspirated.<br> <b>Why the others are second-line here</b> — H2-receptor antagonists (famotidine, ranitidine) and proton-pump inhibitors reduce <b>secretion of new acid</b> and need 30–60 minutes or more; metoclopramide increases gastric emptying and LES tone but also takes time. In an elective case these are given the night before and the morning of surgery, often together with citrate. Antiemetics, sedatives, anticholinergics and steroids <b>do not change the pH or volume of gastric contents</b>.\n- 비교: <table><thead><tr><th style=\"width:28%\">Agent</th><th style=\"width:36%\">Mechanism</th><th>Time to effect · role before an emergency induction</th></tr></thead><tbody> <tr><td><b>Sodium citrate 0.3 M (answer)</b></td><td><b>neutralizes acid already present</b> (non-particulate)</td><td><b>minutes</b> — the only one that works in this window</td></tr> <tr><td>Famotidine / ranitidine IV</td><td>blocks H2 receptors, less new acid</td><td>30–60 min — adjunct if time allows</td></tr> <tr><td>Metoclopramide IV</td><td>faster emptying, higher LES tone</td><td>15–30 min — adjunct</td></tr> <tr><td>Ondansetron / glycopyrrolate / dexamethasone</td><td>antiemetic / antisialagogue / anti-inflammatory</td><td>no effect on gastric pH or volume</td></tr> </tbody></table> The <b>closest wrong answer is glycopyrrolate</b>: it dries secretions and is sometimes given before airway management, but it does not raise gastric pH and may even lower LES tone. The question asks what reduces the <b>severity</b> of pneumonitis — that is a pH question, and pH is changed only by the antacid.\n- 오답 이유:\n  - (A) Dexamethasone reduces postoperative nausea and airway edema but has no effect on gastric acidity or volume before induction. This option would be correct only as part of multimodal nausea prophylaxis, not for aspiration.\n  - (C) Ondansetron prevents nausea and vomiting after surgery but does not alter gastric pH or volume, so it does not reduce the injury if aspiration occurs. This option would be correct only if the question asked about prophylaxis of postoperative nausea and vomiting.\n  - (D) Midazolam causes sedation and amnesia, crosses the placenta, depresses the neonate and blunts airway reflexes, which increases rather than reduces aspiration risk. This option would be correct only for anxiolysis in a non-pregnant patient with no aspiration risk.\n  - (E) Glycopyrrolate reduces airway secretions and vagal bradycardia but does not neutralize gastric acid and may reduce lower esophageal sphincter tone. This option would be correct only if the goal were to dry secretions before ketamine or awake intubation.\n- 함정: Cricoid pressure and rapid-sequence induction address the volume that reaches the airway; the antacid addresses what that volume does when it gets there. Both are given — the drug that changes severity is the antacid.\n- 학습목표: 응급 제왕절개 전신마취 전 흡인성 폐렴 예방을 위한 비입자성 제산제 투여\n- 근거·출처: ASA Practice Guidelines for Obstetric Anesthesia (Anesthesiology 2016) — timely administration of non-particulate antacids, H2 antagonists and/or metoclopramide before cesarean delivery · Mendelson CL. Am J Obstet Gynecol 1946 — aspiration of stomach contents into the lungs during obstetric anesthesia",
  "explanationItems": [
   {
    "k": "정답 핵심",
    "v": "Pregnant women at term are treated as having a full stomach (progesterone-mediated slowing of gastric emptying, raised intragastric pressure, reduced lower esophageal sphincter tone), and this patient has also eaten recently. Aspiration pneumonitis severity depends on gastric pH below about 2.5 and volume above about 25 mL. A non-particulate antacid such as 0.3 M sodium citrate raises gastric pH within minutes and is the one agent that works in the time available before an emergency induction; H2 blockers and metoclopramide are useful adjuncts when there is more time."
   },
   {
    "k": "원리",
    "v": "Aspiration pneumonitis (Mendelson syndrome) is a <b>chemical burn of the airway by acid</b>, and its severity rises steeply when the aspirated fluid has <b>pH below about 2.5</b> and a volume above about 25 mL (0.4 mL/kg). Pregnancy makes aspiration more likely for anatomical and hormonal reasons: <b>progesterone lowers the tone of the lower esophageal sphincter</b>, the enlarging uterus <b>raises intragastric pressure</b>, and labor, pain and opioids <b>delay gastric emptying</b>. Every laboring woman undergoing general anesthesia is therefore treated as a full-stomach patient — rapid-sequence induction, cricoid pressure, and <b>pharmacologic prophylaxis</b>.<br> <b>Why sodium citrate</b> — a non-particulate (clear) antacid neutralizes the acid already in the stomach, raising pH above 2.5 <b>within minutes</b> and for about 30–60 minutes; it is the only agent whose onset fits an emergency. It must be non-particulate because particulate antacids (aluminium hydroxide, magnesium trisilicate) themselves cause a granulomatous pneumonitis if aspirated.<br> <b>Why the others are second-line here</b> — H2-receptor antagonists (famotidine, ranitidine) and proton-pump inhibitors reduce <b>secretion of new acid</b> and need 30–60 minutes or more; metoclopramide increases gastric emptying and LES tone but also takes time. In an elective case these are given the night before and the morning of surgery, often together with citrate. Antiemetics, sedatives, anticholinergics and steroids <b>do not change the pH or volume of gastric contents</b>."
   },
   {
    "k": "비교",
    "v": "<table><thead><tr><th style=\"width:28%\">Agent</th><th style=\"width:36%\">Mechanism</th><th>Time to effect · role before an emergency induction</th></tr></thead><tbody> <tr><td><b>Sodium citrate 0.3 M (answer)</b></td><td><b>neutralizes acid already present</b> (non-particulate)</td><td><b>minutes</b> — the only one that works in this window</td></tr> <tr><td>Famotidine / ranitidine IV</td><td>blocks H2 receptors, less new acid</td><td>30–60 min — adjunct if time allows</td></tr> <tr><td>Metoclopramide IV</td><td>faster emptying, higher LES tone</td><td>15–30 min — adjunct</td></tr> <tr><td>Ondansetron / glycopyrrolate / dexamethasone</td><td>antiemetic / antisialagogue / anti-inflammatory</td><td>no effect on gastric pH or volume</td></tr> </tbody></table> The <b>closest wrong answer is glycopyrrolate</b>: it dries secretions and is sometimes given before airway management, but it does not raise gastric pH and may even lower LES tone. The question asks what reduces the <b>severity</b> of pneumonitis — that is a pH question, and pH is changed only by the antacid."
   },
   {
    "k": "오답 이유",
    "v": "(A) Dexamethasone reduces postoperative nausea and airway edema but has no effect on gastric acidity or volume before induction. This option would be correct only as part of multimodal nausea prophylaxis, not for aspiration.\n(C) Ondansetron prevents nausea and vomiting after surgery but does not alter gastric pH or volume, so it does not reduce the injury if aspiration occurs. This option would be correct only if the question asked about prophylaxis of postoperative nausea and vomiting.\n(D) Midazolam causes sedation and amnesia, crosses the placenta, depresses the neonate and blunts airway reflexes, which increases rather than reduces aspiration risk. This option would be correct only for anxiolysis in a non-pregnant patient with no aspiration risk.\n(E) Glycopyrrolate reduces airway secretions and vagal bradycardia but does not neutralize gastric acid and may reduce lower esophageal sphincter tone. This option would be correct only if the goal were to dry secretions before ketamine or awake intubation."
   },
   {
    "k": "함정",
    "v": "Cricoid pressure and rapid-sequence induction address the volume that reaches the airway; the antacid addresses what that volume does when it gets there. Both are given — the drug that changes severity is the antacid."
   },
   {
    "k": "학습목표",
    "v": "응급 제왕절개 전신마취 전 흡인성 폐렴 예방을 위한 비입자성 제산제 투여"
   },
   {
    "k": "근거·출처",
    "v": "ASA Practice Guidelines for Obstetric Anesthesia (Anesthesiology 2016) — timely administration of non-particulate antacids, H2 antagonists and/or metoclopramide before cesarean delivery · Mendelson CL. Am J Obstet Gynecol 1946 — aspiration of stomach contents into the lungs during obstetric anesthesia"
   }
  ],
  "source": "의대_시험지_제작 오픈데이터 영상 세트 / 20260913T201606Z_일일영상_2026-09-14_9units_9q_85b9cadf",
  "vitals": [],
  "labs": [],
  "appendix": null,
  "figureImg": null,
  "attribution": {
   "dataset": "",
   "license": "",
   "license_url": "",
   "url": "",
   "asset_id": "",
   "text": ""
  },
  "run_id": "20260913T201606Z_일일영상_2026-09-14_9units_9q_85b9cadf",
  "qid": "Q0006"
 },
 {
  "id": "imaging-2026-0009",
  "exam": "imaging",
  "style": "usmle_style",
  "styleLabel": "USMLE형",
  "subject": "산부인과",
  "subject_file": "산부인과",
  "setSubject": "통합(생식의학·응급·마취)",
  "subtopic": "부인과 — 자궁외임신·기능성 무월경",
  "type": "부인과 — 자궁외임신·기능성 무월경",
  "modality": "",
  "step": "Step 2",
  "difficulty": 5,
  "difficultyLabel": "최상",
  "created": "2026-09-13",
  "vignette": "A 22-year-old woman who is a collegiate long-distance runner comes to the physician because she has not had a menstrual period for 8 months. Her BMI is 17.5 kg/m2. Urine hCG is negative. Serum TSH and prolactin concentrations are within the reference ranges. She has no withdrawal bleeding after a 10-day course of oral medroxyprogesterone. Serum FSH and LH concentrations are low-normal.",
  "question": "This patient is at greatest risk for which of the following?",
  "options": [
   "Decreased bone mineral density",
   "Endometrial hyperplasia",
   "Hirsutism",
   "Galactorrhea",
   "Venous thromboembolism"
  ],
  "answer": 1,
  "explanationText": "- 정답 핵심: No withdrawal bleeding means the endometrium was not estrogen-primed; low-normal gonadotropins place the defect in the hypothalamus (energy deficit suppresses GnRH pulsatility). The resulting hypoestrogenism causes bone loss — the female athlete triad.\n- 원리: 무월경 검사는 <b>「에스트로겐이 있는가」</b>를 먼저 묻는다. <b>프로게스틴 소퇴 출혈</b>은 자궁내막이 에스트로겐으로 두꺼워져 있을 때만 나온다. 이 환자는 출혈이 <b>없으므로 저에스트로겐 상태</b>다. 그다음 <b>FSH·LH 가 낮은-정상</b>이면 난소가 아니라 <b>시상하부-뇌하수체</b>가 원인이다.<br> <b>왜 시상하부가 꺼지는가</b> — 장거리 달리기의 <b>에너지 결핍(BMI 17.5)</b> 은 <b>렙틴 감소·코르티솔 증가</b>로 이어지고, 이것이 <b>GnRH 박동 발생기(kisspeptin 뉴런)</b> 를 억제한다. GnRH 박동이 사라지면 LH 박동이 사라지고 난포가 자라지 못해 에스트라디올이 바닥으로 떨어진다 — <b>기능성 시상하부 무월경(FHA)</b>.<br> <b>왜 뼈가 가장 위험한가</b> — 에스트로겐은 <b>파골세포의 수명을 줄이고 RANKL 을 억제</b>해 뼈흡수를 막는다. 20대 초반은 <b>최대 골량이 완성되는 마지막 시기</b>인데, 이때 에스트로겐이 없으면 <b>얻어야 할 뼈를 못 얻고 있는 뼈도 잃는다</b>. 여기에 <b>에너지 결핍 자체의 IGF-1 저하</b>와 코르티솔이 더해져 골밀도 저하와 피로골절이 온다 — <b>여성 운동선수 삼주징</b>(에너지 결핍·무월경·골밀도 저하).<br> <b>치료의 순서</b>도 여기서 나온다 — 피임약으로 월경을 만드는 것이 아니라 <b>에너지 균형 회복</b>이 먼저이고, 그래도 안 되면 경피 에스트라디올을 고려한다.\n- 비교: <table><thead><tr><th style=\"width:24%\">무월경의 원인</th><th style=\"width:22%\">소퇴 출혈</th><th style=\"width:22%\">FSH · LH</th><th>가장 큰 위험</th></tr></thead><tbody> <tr><td><b>기능성 시상하부 무월경(정답)</b></td><td><b>없음</b>(저에스트로겐)</td><td><b>낮음~낮은 정상</b></td><td><b>골밀도 저하 · 피로골절</b></td></tr> <tr><td>다낭난소증후군</td><td><b>있음</b>(에스트로겐 있음)</td><td>LH/FSH 상승 경향</td><td><b>자궁내막증식·다모증</b></td></tr> <tr><td>일차 난소부전</td><td>없음</td><td><b>FSH 높음</b></td><td>골밀도 저하 · 심혈관</td></tr> <tr><td>고프롤락틴혈증</td><td>없음~있음</td><td>낮음</td><td>유루증 · 시야결손</td></tr> </tbody></table> <b>가장 가까운 오답은 ② 자궁내막증식</b> — 「무월경 = 내막이 쌓인다」는 직관은 <b>에스트로겐이 있을 때(PCOS)</b>만 맞다. <b>소퇴 출혈 음성</b>이 그 직관을 끊는 열쇠다.\n- 오답 이유:\n  - (B) 자궁내막증식은 배란은 없지만 에스트로겐은 충분한 상태(다낭난소증후군)에서 내막이 대항 없이 쌓일 때 생기며, 그때는 프로게스틴에 소퇴 출혈이 나온다. 이 환자는 출혈이 없다. 이 선지가 정답이 되려면 소퇴 출혈이 양성이고 LH/FSH 가 높은 PCOS 소견이어야 한다.\n  - (C) 다모증은 안드로겐 과다(PCOS·선천부신과형성)의 표현이지 시상하부 억제의 결과가 아니다. 이 선지가 정답이 되려면 여드름·다모증과 함께 테스토스테론 상승이 있어야 한다.\n  - (D) 유루증은 고프롤락틴혈증의 징후인데 이 환자의 프롤락틴은 정상이다. 이 선지가 정답이 되려면 프롤락틴 상승과 시야결손·두통 같은 뇌하수체 종양 단서가 있어야 한다.\n  - (E) 정맥혈전색전증 위험은 에스트로겐 과다나 외인성 에스트로겐(경구피임약·임신)에서 오르지 에스트로겐 결핍에서는 오르지 않는다. 이 선지가 정답이 되려면 고용량 에스트로겐 치료 중이거나 임신 상태여야 한다.\n- 함정: 무월경이면 무조건 「자궁내막증식 위험」이 아니다 — 소퇴 출혈 여부로 에스트로겐이 있는지를 먼저 가른다.\n- 학습목표: 프로게스틴 소퇴 출혈 음성 + 낮은 성선자극호르몬 → 저에스트로겐 → 골밀도 저하\n- 근거·출처: Endocrine Society Clinical Practice Guideline: Functional Hypothalamic Amenorrhea (J Clin Endocrinol Metab 2017)",
  "explanationItems": [
   {
    "k": "정답 핵심",
    "v": "No withdrawal bleeding means the endometrium was not estrogen-primed; low-normal gonadotropins place the defect in the hypothalamus (energy deficit suppresses GnRH pulsatility). The resulting hypoestrogenism causes bone loss — the female athlete triad."
   },
   {
    "k": "원리",
    "v": "무월경 검사는 <b>「에스트로겐이 있는가」</b>를 먼저 묻는다. <b>프로게스틴 소퇴 출혈</b>은 자궁내막이 에스트로겐으로 두꺼워져 있을 때만 나온다. 이 환자는 출혈이 <b>없으므로 저에스트로겐 상태</b>다. 그다음 <b>FSH·LH 가 낮은-정상</b>이면 난소가 아니라 <b>시상하부-뇌하수체</b>가 원인이다.<br> <b>왜 시상하부가 꺼지는가</b> — 장거리 달리기의 <b>에너지 결핍(BMI 17.5)</b> 은 <b>렙틴 감소·코르티솔 증가</b>로 이어지고, 이것이 <b>GnRH 박동 발생기(kisspeptin 뉴런)</b> 를 억제한다. GnRH 박동이 사라지면 LH 박동이 사라지고 난포가 자라지 못해 에스트라디올이 바닥으로 떨어진다 — <b>기능성 시상하부 무월경(FHA)</b>.<br> <b>왜 뼈가 가장 위험한가</b> — 에스트로겐은 <b>파골세포의 수명을 줄이고 RANKL 을 억제</b>해 뼈흡수를 막는다. 20대 초반은 <b>최대 골량이 완성되는 마지막 시기</b>인데, 이때 에스트로겐이 없으면 <b>얻어야 할 뼈를 못 얻고 있는 뼈도 잃는다</b>. 여기에 <b>에너지 결핍 자체의 IGF-1 저하</b>와 코르티솔이 더해져 골밀도 저하와 피로골절이 온다 — <b>여성 운동선수 삼주징</b>(에너지 결핍·무월경·골밀도 저하).<br> <b>치료의 순서</b>도 여기서 나온다 — 피임약으로 월경을 만드는 것이 아니라 <b>에너지 균형 회복</b>이 먼저이고, 그래도 안 되면 경피 에스트라디올을 고려한다."
   },
   {
    "k": "비교",
    "v": "<table><thead><tr><th style=\"width:24%\">무월경의 원인</th><th style=\"width:22%\">소퇴 출혈</th><th style=\"width:22%\">FSH · LH</th><th>가장 큰 위험</th></tr></thead><tbody> <tr><td><b>기능성 시상하부 무월경(정답)</b></td><td><b>없음</b>(저에스트로겐)</td><td><b>낮음~낮은 정상</b></td><td><b>골밀도 저하 · 피로골절</b></td></tr> <tr><td>다낭난소증후군</td><td><b>있음</b>(에스트로겐 있음)</td><td>LH/FSH 상승 경향</td><td><b>자궁내막증식·다모증</b></td></tr> <tr><td>일차 난소부전</td><td>없음</td><td><b>FSH 높음</b></td><td>골밀도 저하 · 심혈관</td></tr> <tr><td>고프롤락틴혈증</td><td>없음~있음</td><td>낮음</td><td>유루증 · 시야결손</td></tr> </tbody></table> <b>가장 가까운 오답은 ② 자궁내막증식</b> — 「무월경 = 내막이 쌓인다」는 직관은 <b>에스트로겐이 있을 때(PCOS)</b>만 맞다. <b>소퇴 출혈 음성</b>이 그 직관을 끊는 열쇠다."
   },
   {
    "k": "오답 이유",
    "v": "(B) 자궁내막증식은 배란은 없지만 에스트로겐은 충분한 상태(다낭난소증후군)에서 내막이 대항 없이 쌓일 때 생기며, 그때는 프로게스틴에 소퇴 출혈이 나온다. 이 환자는 출혈이 없다. 이 선지가 정답이 되려면 소퇴 출혈이 양성이고 LH/FSH 가 높은 PCOS 소견이어야 한다.\n(C) 다모증은 안드로겐 과다(PCOS·선천부신과형성)의 표현이지 시상하부 억제의 결과가 아니다. 이 선지가 정답이 되려면 여드름·다모증과 함께 테스토스테론 상승이 있어야 한다.\n(D) 유루증은 고프롤락틴혈증의 징후인데 이 환자의 프롤락틴은 정상이다. 이 선지가 정답이 되려면 프롤락틴 상승과 시야결손·두통 같은 뇌하수체 종양 단서가 있어야 한다.\n(E) 정맥혈전색전증 위험은 에스트로겐 과다나 외인성 에스트로겐(경구피임약·임신)에서 오르지 에스트로겐 결핍에서는 오르지 않는다. 이 선지가 정답이 되려면 고용량 에스트로겐 치료 중이거나 임신 상태여야 한다."
   },
   {
    "k": "함정",
    "v": "무월경이면 무조건 「자궁내막증식 위험」이 아니다 — 소퇴 출혈 여부로 에스트로겐이 있는지를 먼저 가른다."
   },
   {
    "k": "학습목표",
    "v": "프로게스틴 소퇴 출혈 음성 + 낮은 성선자극호르몬 → 저에스트로겐 → 골밀도 저하"
   },
   {
    "k": "근거·출처",
    "v": "Endocrine Society Clinical Practice Guideline: Functional Hypothalamic Amenorrhea (J Clin Endocrinol Metab 2017)"
   }
  ],
  "source": "의대_시험지_제작 오픈데이터 영상 세트 / 20260913T053235Z_일일영상_2026-09-13_10units_9q_7072fb0c",
  "vitals": [],
  "labs": [],
  "appendix": null,
  "figureImg": null,
  "attribution": {
   "dataset": "",
   "license": "",
   "license_url": "",
   "url": "",
   "asset_id": "",
   "text": ""
  },
  "run_id": "20260913T053235Z_일일영상_2026-09-13_10units_9q_7072fb0c",
  "qid": "Q0009"
 },
 {
  "id": "imaging-2026-0008",
  "exam": "imaging",
  "style": "usmle_style",
  "styleLabel": "USMLE형",
  "subject": "산부인과",
  "subject_file": "산부인과",
  "setSubject": "통합(생식의학·응급·마취)",
  "subtopic": "부인과 — 자궁외임신·기능성 무월경",
  "type": "부인과 — 자궁외임신·기능성 무월경",
  "modality": "",
  "step": "Step 2",
  "difficulty": 4,
  "difficultyLabel": "상",
  "created": "2026-09-13",
  "vignette": "A 29-year-old woman has vaginal spotting 7 weeks after her last menstrual period. She is hemodynamically stable. Transvaginal ultrasonography shows no intrauterine pregnancy and a 2.5-cm left adnexal mass without cardiac activity. Serum β-hCG concentration is 2800 mIU/mL. Methotrexate therapy is being considered.",
  "question": "Which of the following additional findings is an absolute contraindication to this treatment?",
  "options": [
   "She desires future pregnancy",
   "She is breastfeeding her 8-month-old son",
   "Her blood type is Rh-negative",
   "She had a previous ectopic pregnancy treated with salpingostomy",
   "Her serum β-hCG concentration rose 20% over 48 hours"
  ],
  "answer": 2,
  "explanationText": "- 정답 핵심: Methotrexate is excreted in breast milk and is toxic to the infant; breastfeeding is an absolute contraindication (with immunodeficiency, liver/renal/pulmonary disease, blood dyscrasias, peptic ulcer, intrauterine pregnancy, and rupture/instability).\n- 원리: 메토트렉세이트(MTX)는 <b>디하이드로엽산환원효소(DHFR) 억제제</b>로, <b>빠르게 분열하는 세포의 DNA 합성을 막아</b> 영양막을 죽인다. 같은 이유로 <b>골수·점막·간·신장·폐</b>가 손상될 수 있고, <b>모유로 배설</b>되어 젖먹이의 골수와 점막에 닿는다. 그래서 <b>수유는 절대 금기</b>다.<br> <b>절대 금기의 논리</b> — (1) <b>약이 환자에게 위험한 경우</b>: 면역결핍, 활동성 간·신장·폐질환, 혈액이상, 소화성궤양, 알코올 남용, MTX 과민. (2) <b>제3자에게 위험한 경우</b>: 수유(영아), 자궁내 임신(정상 태아). (3) <b>약이 상황을 감당 못 하는 경우</b>: 파열·혈역학 불안정 → 수술.<br> <b>상대 금기(실패 위험 요인)</b>는 다른 층이다 — <b>hCG &gt;5,000, 태아 심박 있음, 종괴 &gt;4 cm</b>, 추적 불가. 이들은 「효과가 떨어진다」는 뜻이지 「써서는 안 된다」가 아니다. 이 환자는 hCG 2,800·2.5 cm·심박 없음이라 오히려 <b>좋은 후보</b>다.<br> <b>Rh 음성은 금기가 아니라 추가 처치</b>(anti-D)이고, <b>향후 임신 희망</b>은 내과적 치료를 <b>선호하게 만드는</b> 요인이다. 「절대 금기」와 「실패 요인」과 「부수 처치」를 세 층으로 나누어 두면 어떤 선지가 와도 자리를 찾는다.\n- 비교: <table><thead><tr><th style=\"width:26%\">층</th><th style=\"width:44%\">항목</th><th>의미</th></tr></thead><tbody> <tr><td><b>절대 금기(정답 층)</b></td><td><b>수유</b> · 자궁내 임신 · 면역결핍 · 간·신·폐질환 · 혈액이상 · 소화성궤양 · 파열/불안정</td><td><b>MTX 를 쓰지 않는다</b> → 수술 또는 분만 후</td></tr> <tr><td>상대 금기 = 실패 위험</td><td>hCG &gt;5,000 · 태아 심박 · 종괴 &gt;4 cm · 추적 곤란</td><td>써도 되나 실패·파열 위험 설명</td></tr> <tr><td>부수 처치</td><td>Rh 음성 → anti-D</td><td>MTX 여부와 무관하게 시행</td></tr> <tr><td>선호 요인</td><td>향후 임신 희망 · 과거 자궁외임신</td><td>난관 보존 → 내과적 치료를 더 고려</td></tr> </tbody></table> <b>가장 가까운 오답은 ⑤</b> — 「48시간 hCG 20 % 상승」은 <b>비정상 임신을 진단하는 기준(정상은 ≥49 % 상승)</b>이지 MTX 의 금기가 아니다. 진단 기준과 치료 금기를 섞는 자리다.\n- 오답 이유:\n  - (A) 향후 임신을 원하는 것은 난관을 보존하는 내과적 치료를 더 선호하게 만드는 요인이지 금기가 아니다. 이 선지가 정답이 되려면 「임신을 원하므로 MTX 를 피한다」는 근거가 있어야 하는데 그런 근거는 없다.\n  - (C) Rh 음성은 자궁외임신 치료 방식과 무관하게 anti-D 면역글로불린을 주면 되는 부수 처치다. 이 선지가 정답이 되려면 Rh 상태가 MTX 독성이나 효과에 영향을 주어야 하는데 그렇지 않다.\n  - (D) 과거 자궁외임신과 난관절개술 병력은 재발 위험을 높일 뿐 MTX 사용을 막지 않으며, 오히려 남은 난관을 아끼려 내과적 치료를 고른다. 이 선지가 정답이 되려면 「이전 MTX 과민반응」 같은 약물 자체의 병력이어야 한다.\n  - (E) 48시간에 20 % 상승은 정상 임신의 최소 상승(약 49 %)에 못 미쳐 비정상 임신을 진단하는 기준이다. 진단이 되었다는 뜻이지 치료 금기가 아니다. 이 선지가 정답이 되려면 hCG 가 5,000 을 넘는 「실패 위험」이었더라도 상대 금기에 그친다.\n- 함정: 「절대 금기」와 「실패 위험 요인(hCG 고값·태아심박·큰 종괴)」을 섞지 않는다.\n- 학습목표: 자궁외임신 메토트렉세이트의 절대 금기 구분\n- 근거·출처: ACOG Practice Bulletin No. 193: Tubal Ectopic Pregnancy (2018)",
  "explanationItems": [
   {
    "k": "정답 핵심",
    "v": "Methotrexate is excreted in breast milk and is toxic to the infant; breastfeeding is an absolute contraindication (with immunodeficiency, liver/renal/pulmonary disease, blood dyscrasias, peptic ulcer, intrauterine pregnancy, and rupture/instability)."
   },
   {
    "k": "원리",
    "v": "메토트렉세이트(MTX)는 <b>디하이드로엽산환원효소(DHFR) 억제제</b>로, <b>빠르게 분열하는 세포의 DNA 합성을 막아</b> 영양막을 죽인다. 같은 이유로 <b>골수·점막·간·신장·폐</b>가 손상될 수 있고, <b>모유로 배설</b>되어 젖먹이의 골수와 점막에 닿는다. 그래서 <b>수유는 절대 금기</b>다.<br> <b>절대 금기의 논리</b> — (1) <b>약이 환자에게 위험한 경우</b>: 면역결핍, 활동성 간·신장·폐질환, 혈액이상, 소화성궤양, 알코올 남용, MTX 과민. (2) <b>제3자에게 위험한 경우</b>: 수유(영아), 자궁내 임신(정상 태아). (3) <b>약이 상황을 감당 못 하는 경우</b>: 파열·혈역학 불안정 → 수술.<br> <b>상대 금기(실패 위험 요인)</b>는 다른 층이다 — <b>hCG &gt;5,000, 태아 심박 있음, 종괴 &gt;4 cm</b>, 추적 불가. 이들은 「효과가 떨어진다」는 뜻이지 「써서는 안 된다」가 아니다. 이 환자는 hCG 2,800·2.5 cm·심박 없음이라 오히려 <b>좋은 후보</b>다.<br> <b>Rh 음성은 금기가 아니라 추가 처치</b>(anti-D)이고, <b>향후 임신 희망</b>은 내과적 치료를 <b>선호하게 만드는</b> 요인이다. 「절대 금기」와 「실패 요인」과 「부수 처치」를 세 층으로 나누어 두면 어떤 선지가 와도 자리를 찾는다."
   },
   {
    "k": "비교",
    "v": "<table><thead><tr><th style=\"width:26%\">층</th><th style=\"width:44%\">항목</th><th>의미</th></tr></thead><tbody> <tr><td><b>절대 금기(정답 층)</b></td><td><b>수유</b> · 자궁내 임신 · 면역결핍 · 간·신·폐질환 · 혈액이상 · 소화성궤양 · 파열/불안정</td><td><b>MTX 를 쓰지 않는다</b> → 수술 또는 분만 후</td></tr> <tr><td>상대 금기 = 실패 위험</td><td>hCG &gt;5,000 · 태아 심박 · 종괴 &gt;4 cm · 추적 곤란</td><td>써도 되나 실패·파열 위험 설명</td></tr> <tr><td>부수 처치</td><td>Rh 음성 → anti-D</td><td>MTX 여부와 무관하게 시행</td></tr> <tr><td>선호 요인</td><td>향후 임신 희망 · 과거 자궁외임신</td><td>난관 보존 → 내과적 치료를 더 고려</td></tr> </tbody></table> <b>가장 가까운 오답은 ⑤</b> — 「48시간 hCG 20 % 상승」은 <b>비정상 임신을 진단하는 기준(정상은 ≥49 % 상승)</b>이지 MTX 의 금기가 아니다. 진단 기준과 치료 금기를 섞는 자리다."
   },
   {
    "k": "오답 이유",
    "v": "(A) 향후 임신을 원하는 것은 난관을 보존하는 내과적 치료를 더 선호하게 만드는 요인이지 금기가 아니다. 이 선지가 정답이 되려면 「임신을 원하므로 MTX 를 피한다」는 근거가 있어야 하는데 그런 근거는 없다.\n(C) Rh 음성은 자궁외임신 치료 방식과 무관하게 anti-D 면역글로불린을 주면 되는 부수 처치다. 이 선지가 정답이 되려면 Rh 상태가 MTX 독성이나 효과에 영향을 주어야 하는데 그렇지 않다.\n(D) 과거 자궁외임신과 난관절개술 병력은 재발 위험을 높일 뿐 MTX 사용을 막지 않으며, 오히려 남은 난관을 아끼려 내과적 치료를 고른다. 이 선지가 정답이 되려면 「이전 MTX 과민반응」 같은 약물 자체의 병력이어야 한다.\n(E) 48시간에 20 % 상승은 정상 임신의 최소 상승(약 49 %)에 못 미쳐 비정상 임신을 진단하는 기준이다. 진단이 되었다는 뜻이지 치료 금기가 아니다. 이 선지가 정답이 되려면 hCG 가 5,000 을 넘는 「실패 위험」이었더라도 상대 금기에 그친다."
   },
   {
    "k": "함정",
    "v": "「절대 금기」와 「실패 위험 요인(hCG 고값·태아심박·큰 종괴)」을 섞지 않는다."
   },
   {
    "k": "학습목표",
    "v": "자궁외임신 메토트렉세이트의 절대 금기 구분"
   },
   {
    "k": "근거·출처",
    "v": "ACOG Practice Bulletin No. 193: Tubal Ectopic Pregnancy (2018)"
   }
  ],
  "source": "의대_시험지_제작 오픈데이터 영상 세트 / 20260913T053235Z_일일영상_2026-09-13_10units_9q_7072fb0c",
  "vitals": [],
  "labs": [],
  "appendix": null,
  "figureImg": null,
  "attribution": {
   "dataset": "",
   "license": "",
   "license_url": "",
   "url": "",
   "asset_id": "",
   "text": ""
  },
  "run_id": "20260913T053235Z_일일영상_2026-09-13_10units_9q_7072fb0c",
  "qid": "Q0008"
 },
 {
  "id": "imaging-2026-0007",
  "exam": "imaging",
  "style": "kmle_style",
  "styleLabel": "국시형",
  "subject": "산부인과",
  "subject_file": "산부인과",
  "setSubject": "통합(생식의학·응급·마취)",
  "subtopic": "산과 — 분만 중 태아감시·산과 마취",
  "type": "산과 — 분만 중 태아감시·산과 마취",
  "modality": "",
  "step": "",
  "difficulty": 3,
  "difficultyLabel": "중",
  "created": "2026-09-13",
  "vignette": "39주 초산부가 제왕절개술을 위해 척추마취를 받았다. 마취 5분 뒤 혈압이 80/45 mmHg(마취 전 120/75 mmHg), 맥박이 분당 112회로 오르고 오심을 호소한다.",
  "question": "자궁을 왼쪽으로 밀고 수액을 주면서 투여할 승압제로 가장 적절한 것은?",
  "options": [
   "에페드린",
   "도파민",
   "바소프레신",
   "에피네프린",
   "페닐에프린"
  ],
  "answer": 5,
  "explanationText": "- 정답 핵심: 척추마취의 교감신경 차단으로 혈관이 확장된 저혈압이다. 순수 α1 작용제인 페닐에프린이 1차 선택이다 — 태아 산증이 에페드린보다 적고, 반사 서맥으로 이미 빠른 모체 맥박을 오히려 낮춘다.\n- 원리: 척추마취 저혈압의 기전은 <b>교감신경 절전섬유 차단 → 세동맥·정맥 확장 → 전신혈관저항과 정맥환류 감소</b>다. 임신부는 <b>자궁이 하대정맥을 눌러 정맥환류가 이미 줄어 있고</b>, 자궁태반 순환은 자가조절이 없어 <b>모체 혈압이 곧 태아 관류</b>다. 그래서 빠르고 정확한 승압이 필요하다.<br> <b>왜 페닐에프린인가</b> — 순수 <b>α1 작용제</b>라 <b>확장된 혈관을 직접 조여</b> 저혈압의 원인을 그대로 되돌린다. 심장 β 자극이 없어 <b>모체 빈맥을 악화시키지 않고</b>, 혈압이 오르면 <b>압반사로 심박수가 떨어져</b> 이 환자처럼 맥박 112회인 상황에 오히려 알맞다. 여러 무작위 연구에서 <b>제대동맥 pH 가 에페드린보다 높았다</b>.<br> <b>왜 에페드린이 밀려났는가</b> — 에페드린은 <b>β1 자극 + 노르에피네프린 방출</b>로 혈압을 올리는데, <b>태반을 잘 통과해 태아 대사율과 카테콜아민을 올려</b> 제대혈 산증을 늘린다. 발현도 느리고 빈맥을 더한다. 옛 교과서의 「자궁혈류 보존」 논리는 동물실험에 근거했고, 임상 결과는 페닐에프린 쪽이 좋았다.<br> <b>따라서 현재 권고</b>(2018 국제 합의) — <b>페닐에프린 예방적 지속주입이 표준</b>, <b>모체 서맥이 동반된 저혈압에서만 에페드린</b>을 고른다.\n- 비교: <table><thead><tr><th style=\"width:20%\">승압제</th><th style=\"width:24%\">수용체</th><th style=\"width:26%\">모체 심박수</th><th>태아 산-염기</th></tr></thead><tbody> <tr><td><b>페닐에프린(정답)</b></td><td><b>α1 순수</b></td><td><b>↓(압반사)</b> — 빈맥 환자에 적합</td><td><b>제대동맥 pH 높음</b></td></tr> <tr><td>에페드린</td><td>β1 &gt; α · 간접 NE 방출</td><td>↑ — 빈맥 악화</td><td>태반 통과 → 태아 산증↑</td></tr> <tr><td>에피네프린</td><td>α+β 강력</td><td>↑↑</td><td>자궁혈류 감소 위험 · 심정지·아나필락시스용</td></tr> <tr><td>바소프레신</td><td>V1</td><td>—</td><td>난치성 혈관확장성 쇼크의 보조약</td></tr> <tr><td>도파민</td><td>용량 의존 D1/β/α</td><td>↑</td><td>산과 표준 아님</td></tr> </tbody></table> <b>가장 가까운 오답은 ① 에페드린</b> — 같은 척추마취 저혈압의 승압제지만, <b>모체 심박수가 갈림길</b>이다. 맥박이 느리면 에페드린, 빠르거나 정상이면 페닐에프린.\n- 오답 이유:\n  - ① 에페드린은 태반을 통과해 태아 대사와 카테콜아민을 올려 제대혈 산증을 늘리고 β1 자극으로 빈맥을 더한다. 이 환자는 이미 112회다. 이 선지가 정답이 되려면 저혈압에 모체 서맥이 동반되어 있어야 한다.\n  - ② 도파민은 용량에 따라 수용체가 바뀌는 불안정한 승압제로 산과 척추마취 저혈압의 표준이 아니다. 이 선지가 정답이 되려면 「심인성 쇼크에 강심 효과가 필요한」 전혀 다른 상황이어야 한다.\n  - ③ 바소프레신은 카테콜아민에 반응하지 않는 난치성 혈관확장성 쇼크에서 보조로 쓰는 약이다. 첫 승압제로 고를 근거가 없다. 이 선지가 정답이 되려면 페닐에프린·에페드린에 반응하지 않는 패혈성 쇼크 배경이어야 한다.\n  - ④ 에피네프린은 α·β 를 모두 강하게 자극해 자궁혈류를 줄일 수 있고 심정지·아나필락시스에 쓰는 약이다. 이 선지가 정답이 되려면 아나필락시스나 심정지 상황이어야 한다.\n- 함정: 에페드린이 「자궁혈류 보존」으로 배웠던 옛 선택이지만, 현재 권고는 페닐에프린 — 특히 모체 빈맥이면 에페드린은 오답.\n- 학습목표: 제왕절개 척추마취 후 저혈압의 승압제 선택\n- 근거·출처: International consensus statement on the management of hypotension with vasopressors during caesarean section under spinal anaesthesia (Anaesthesia 2018)",
  "explanationItems": [
   {
    "k": "정답 핵심",
    "v": "척추마취의 교감신경 차단으로 혈관이 확장된 저혈압이다. 순수 α1 작용제인 페닐에프린이 1차 선택이다 — 태아 산증이 에페드린보다 적고, 반사 서맥으로 이미 빠른 모체 맥박을 오히려 낮춘다."
   },
   {
    "k": "원리",
    "v": "척추마취 저혈압의 기전은 <b>교감신경 절전섬유 차단 → 세동맥·정맥 확장 → 전신혈관저항과 정맥환류 감소</b>다. 임신부는 <b>자궁이 하대정맥을 눌러 정맥환류가 이미 줄어 있고</b>, 자궁태반 순환은 자가조절이 없어 <b>모체 혈압이 곧 태아 관류</b>다. 그래서 빠르고 정확한 승압이 필요하다.<br> <b>왜 페닐에프린인가</b> — 순수 <b>α1 작용제</b>라 <b>확장된 혈관을 직접 조여</b> 저혈압의 원인을 그대로 되돌린다. 심장 β 자극이 없어 <b>모체 빈맥을 악화시키지 않고</b>, 혈압이 오르면 <b>압반사로 심박수가 떨어져</b> 이 환자처럼 맥박 112회인 상황에 오히려 알맞다. 여러 무작위 연구에서 <b>제대동맥 pH 가 에페드린보다 높았다</b>.<br> <b>왜 에페드린이 밀려났는가</b> — 에페드린은 <b>β1 자극 + 노르에피네프린 방출</b>로 혈압을 올리는데, <b>태반을 잘 통과해 태아 대사율과 카테콜아민을 올려</b> 제대혈 산증을 늘린다. 발현도 느리고 빈맥을 더한다. 옛 교과서의 「자궁혈류 보존」 논리는 동물실험에 근거했고, 임상 결과는 페닐에프린 쪽이 좋았다.<br> <b>따라서 현재 권고</b>(2018 국제 합의) — <b>페닐에프린 예방적 지속주입이 표준</b>, <b>모체 서맥이 동반된 저혈압에서만 에페드린</b>을 고른다."
   },
   {
    "k": "비교",
    "v": "<table><thead><tr><th style=\"width:20%\">승압제</th><th style=\"width:24%\">수용체</th><th style=\"width:26%\">모체 심박수</th><th>태아 산-염기</th></tr></thead><tbody> <tr><td><b>페닐에프린(정답)</b></td><td><b>α1 순수</b></td><td><b>↓(압반사)</b> — 빈맥 환자에 적합</td><td><b>제대동맥 pH 높음</b></td></tr> <tr><td>에페드린</td><td>β1 &gt; α · 간접 NE 방출</td><td>↑ — 빈맥 악화</td><td>태반 통과 → 태아 산증↑</td></tr> <tr><td>에피네프린</td><td>α+β 강력</td><td>↑↑</td><td>자궁혈류 감소 위험 · 심정지·아나필락시스용</td></tr> <tr><td>바소프레신</td><td>V1</td><td>—</td><td>난치성 혈관확장성 쇼크의 보조약</td></tr> <tr><td>도파민</td><td>용량 의존 D1/β/α</td><td>↑</td><td>산과 표준 아님</td></tr> </tbody></table> <b>가장 가까운 오답은 ① 에페드린</b> — 같은 척추마취 저혈압의 승압제지만, <b>모체 심박수가 갈림길</b>이다. 맥박이 느리면 에페드린, 빠르거나 정상이면 페닐에프린."
   },
   {
    "k": "오답 이유",
    "v": "① 에페드린은 태반을 통과해 태아 대사와 카테콜아민을 올려 제대혈 산증을 늘리고 β1 자극으로 빈맥을 더한다. 이 환자는 이미 112회다. 이 선지가 정답이 되려면 저혈압에 모체 서맥이 동반되어 있어야 한다.\n② 도파민은 용량에 따라 수용체가 바뀌는 불안정한 승압제로 산과 척추마취 저혈압의 표준이 아니다. 이 선지가 정답이 되려면 「심인성 쇼크에 강심 효과가 필요한」 전혀 다른 상황이어야 한다.\n③ 바소프레신은 카테콜아민에 반응하지 않는 난치성 혈관확장성 쇼크에서 보조로 쓰는 약이다. 첫 승압제로 고를 근거가 없다. 이 선지가 정답이 되려면 페닐에프린·에페드린에 반응하지 않는 패혈성 쇼크 배경이어야 한다.\n④ 에피네프린은 α·β 를 모두 강하게 자극해 자궁혈류를 줄일 수 있고 심정지·아나필락시스에 쓰는 약이다. 이 선지가 정답이 되려면 아나필락시스나 심정지 상황이어야 한다."
   },
   {
    "k": "함정",
    "v": "에페드린이 「자궁혈류 보존」으로 배웠던 옛 선택이지만, 현재 권고는 페닐에프린 — 특히 모체 빈맥이면 에페드린은 오답."
   },
   {
    "k": "학습목표",
    "v": "제왕절개 척추마취 후 저혈압의 승압제 선택"
   },
   {
    "k": "근거·출처",
    "v": "International consensus statement on the management of hypotension with vasopressors during caesarean section under spinal anaesthesia (Anaesthesia 2018)"
   }
  ],
  "source": "의대_시험지_제작 오픈데이터 영상 세트 / 20260913T053235Z_일일영상_2026-09-13_10units_9q_7072fb0c",
  "vitals": [],
  "labs": [],
  "appendix": null,
  "figureImg": null,
  "attribution": {
   "dataset": "",
   "license": "",
   "license_url": "",
   "url": "",
   "asset_id": "",
   "text": ""
  },
  "run_id": "20260913T053235Z_일일영상_2026-09-13_10units_9q_7072fb0c",
  "qid": "Q0007"
 },
 {
  "id": "imaging-2026-0005",
  "exam": "imaging",
  "style": "kmle_style",
  "styleLabel": "국시형",
  "subject": "산부인과",
  "subject_file": "산부인과",
  "setSubject": "통합(생식의학·응급·마취)",
  "subtopic": "생식샘 조직학과 성분화·무월경",
  "type": "생식샘 조직학과 성분화·무월경",
  "modality": "",
  "step": "",
  "difficulty": 4,
  "difficultyLabel": "상",
  "created": "2026-09-13",
  "vignette": "17세 여자가 월경을 한 번도 하지 않아 왔다. 키 170 cm, 유방 발달은 성숙 단계이나 음모와 겨드랑이털이 거의 없다. 외부생식기는 여성형이고 질은 짧은 맹낭으로 끝나며 골반 초음파에서 자궁이 보이지 않는다. 혈청 테스토스테론은 성인 남성 정상 범위다.",
  "question": "진단은?",
  "options": [
   "터너증후군",
   "5α-환원효소 결핍증",
   "칼만증후군",
   "완전 안드로겐무감응증후군",
   "뮐러관무형성(MRKH 증후군)"
  ],
  "answer": 4,
  "explanationText": "- 정답 핵심: 46,XY 에서 고환의 세르톨리세포가 AMH 를 내어 자궁·질 상부가 없고, 안드로겐 수용체가 작동하지 않아 음모·액모가 없으며, 테스토스테론이 방향화된 에스트라디올로 유방은 발달한다.\n- 원리: 원발무월경 감별은 <b>「유방(에스트로겐 노출)」·「자궁」·「음모(안드로겐 작용)」</b> 세 축으로 푼다. 이 환자는 <b>유방 ○ · 자궁 × · 음모 ×</b> 이고 테스토스테론이 남성 범위다.<br> <b>왜 자궁이 없는가</b> — 핵형이 46,XY 이면 <b>고환의 세르톨리세포가 AMH</b> 를 내어 뮐러관을 퇴화시키므로 <b>자궁·난관·질 상부가 생기지 않는다</b>(질이 짧은 맹낭으로 끝나는 이유).<br> <b>왜 음모가 없는가</b> — 안드로겐 수용체(AR) 유전자 결손으로 <b>테스토스테론도 DHT 도 세포에 신호를 못 넣는다</b>. 그래서 외부생식기는 여성형으로 남고 사춘기 음모·액모도 나지 않는다. <b>혈중 테스토스테론은 오히려 높다</b> — 수용체가 없어 되먹임이 안 걸려 LH 가 오르고 고환이 계속 만들기 때문이다.<br> <b>왜 유방은 발달하는가</b> — 높은 테스토스테론이 말초 <b>아로마타제로 에스트라디올</b>이 되고, 에스트로겐 수용체는 정상이므로 유방은 성숙 단계까지 자란다. <b>키가 큰 것</b>도 Y 염색체와 늦게 닫히는 성장판의 결과다.<br> 즉 <b>「안드로겐은 못 쓰고 에스트로겐은 쓴다」</b>가 이 질환의 표현형 전체를 설명한다. 진단 후에는 <b>성선종양 위험 때문에 사춘기 완료 뒤 고환 절제</b>와 에스트로겐 보충이 따른다.\n- 비교: <table><thead><tr><th style=\"width:24%\">진단</th><th>핵형</th><th>유방</th><th>자궁</th><th>음모</th><th>테스토스테론</th></tr></thead><tbody> <tr><td><b>완전 안드로겐무감응(정답)</b></td><td>46,XY</td><td><b>○</b></td><td><b>×</b></td><td><b>×</b></td><td><b>남성 범위</b></td></tr> <tr><td>뮐러관무형성(MRKH)</td><td>46,XX</td><td>○</td><td>×</td><td><b>○</b></td><td>여성 범위</td></tr> <tr><td>터너증후군</td><td>45,X</td><td><b>×</b></td><td>○</td><td>○(약함)</td><td>낮음 · FSH 높음</td></tr> <tr><td>칼만증후군</td><td>46,XX</td><td>×</td><td>○</td><td>×~약함</td><td>낮음 · FSH·LH 낮음</td></tr> <tr><td>5α-환원효소 결핍</td><td>46,XY</td><td>×</td><td>×</td><td>○</td><td>남성 범위 · 사춘기 남성화</td></tr> </tbody></table> <b>가장 가까운 오답은 ⑤ MRKH</b> — 「유방 ○ · 자궁 ×」까지 같다. <b>음모 유무와 테스토스테론 수치</b>가 두 진단을 가른다. 음모가 정상이면 MRKH, 없으면 CAIS.\n- 오답 이유:\n  - ① 터너증후군은 난소부전이라 에스트로겐이 없어 유방이 발달하지 않고 키가 작으며 뮐러관은 정상이라 자궁이 있다. 이 환자와 세 축이 모두 반대다. 이 선지가 정답이 되려면 「유방 미발달·저신장·자궁 있음·FSH 상승」이어야 한다.\n  - ② 5α-환원효소 결핍은 테스토스테론은 정상이라 사춘기에 음경 성장·근육 발달 같은 남성화가 일어나고 음모도 난다. 유방은 두드러지지 않는다. 이 선지가 정답이 되려면 사춘기 남성화와 모호한 외부생식기 병력이 있어야 한다.\n  - ③ 칼만증후군은 GnRH 결핍으로 FSH·LH 가 낮아 에스트로겐이 없고 유방이 발달하지 않으며, 46,XX 라 자궁은 정상이고 후각 저하가 동반된다. 이 선지가 정답이 되려면 유방 미발달·자궁 있음·무후각이어야 한다.\n  - ⑤ MRKH 는 46,XX 에서 뮐러관만 형성되지 않은 것이라 자궁은 없지만 난소가 정상이어서 음모·액모가 정상이고 테스토스테론은 여성 범위다. 이 선지가 정답이 되려면 음모가 정상이고 테스토스테론이 낮아야 한다.\n- 함정: 「자궁 없음」만 보고 MRKH 로 가지 않는다 — 음모 유무와 테스토스테론 수치가 두 질환을 가른다.\n- 학습목표: 원발무월경에서 음모 결여 + 남성 수준 테스토스테론으로 완전 안드로겐무감응 감별\n- 근거·출처: 표준 부인과 내분비 지식 — 원발무월경 감별(Speroff 9판 11장)",
  "explanationItems": [
   {
    "k": "정답 핵심",
    "v": "46,XY 에서 고환의 세르톨리세포가 AMH 를 내어 자궁·질 상부가 없고, 안드로겐 수용체가 작동하지 않아 음모·액모가 없으며, 테스토스테론이 방향화된 에스트라디올로 유방은 발달한다."
   },
   {
    "k": "원리",
    "v": "원발무월경 감별은 <b>「유방(에스트로겐 노출)」·「자궁」·「음모(안드로겐 작용)」</b> 세 축으로 푼다. 이 환자는 <b>유방 ○ · 자궁 × · 음모 ×</b> 이고 테스토스테론이 남성 범위다.<br> <b>왜 자궁이 없는가</b> — 핵형이 46,XY 이면 <b>고환의 세르톨리세포가 AMH</b> 를 내어 뮐러관을 퇴화시키므로 <b>자궁·난관·질 상부가 생기지 않는다</b>(질이 짧은 맹낭으로 끝나는 이유).<br> <b>왜 음모가 없는가</b> — 안드로겐 수용체(AR) 유전자 결손으로 <b>테스토스테론도 DHT 도 세포에 신호를 못 넣는다</b>. 그래서 외부생식기는 여성형으로 남고 사춘기 음모·액모도 나지 않는다. <b>혈중 테스토스테론은 오히려 높다</b> — 수용체가 없어 되먹임이 안 걸려 LH 가 오르고 고환이 계속 만들기 때문이다.<br> <b>왜 유방은 발달하는가</b> — 높은 테스토스테론이 말초 <b>아로마타제로 에스트라디올</b>이 되고, 에스트로겐 수용체는 정상이므로 유방은 성숙 단계까지 자란다. <b>키가 큰 것</b>도 Y 염색체와 늦게 닫히는 성장판의 결과다.<br> 즉 <b>「안드로겐은 못 쓰고 에스트로겐은 쓴다」</b>가 이 질환의 표현형 전체를 설명한다. 진단 후에는 <b>성선종양 위험 때문에 사춘기 완료 뒤 고환 절제</b>와 에스트로겐 보충이 따른다."
   },
   {
    "k": "비교",
    "v": "<table><thead><tr><th style=\"width:24%\">진단</th><th>핵형</th><th>유방</th><th>자궁</th><th>음모</th><th>테스토스테론</th></tr></thead><tbody> <tr><td><b>완전 안드로겐무감응(정답)</b></td><td>46,XY</td><td><b>○</b></td><td><b>×</b></td><td><b>×</b></td><td><b>남성 범위</b></td></tr> <tr><td>뮐러관무형성(MRKH)</td><td>46,XX</td><td>○</td><td>×</td><td><b>○</b></td><td>여성 범위</td></tr> <tr><td>터너증후군</td><td>45,X</td><td><b>×</b></td><td>○</td><td>○(약함)</td><td>낮음 · FSH 높음</td></tr> <tr><td>칼만증후군</td><td>46,XX</td><td>×</td><td>○</td><td>×~약함</td><td>낮음 · FSH·LH 낮음</td></tr> <tr><td>5α-환원효소 결핍</td><td>46,XY</td><td>×</td><td>×</td><td>○</td><td>남성 범위 · 사춘기 남성화</td></tr> </tbody></table> <b>가장 가까운 오답은 ⑤ MRKH</b> — 「유방 ○ · 자궁 ×」까지 같다. <b>음모 유무와 테스토스테론 수치</b>가 두 진단을 가른다. 음모가 정상이면 MRKH, 없으면 CAIS."
   },
   {
    "k": "오답 이유",
    "v": "① 터너증후군은 난소부전이라 에스트로겐이 없어 유방이 발달하지 않고 키가 작으며 뮐러관은 정상이라 자궁이 있다. 이 환자와 세 축이 모두 반대다. 이 선지가 정답이 되려면 「유방 미발달·저신장·자궁 있음·FSH 상승」이어야 한다.\n② 5α-환원효소 결핍은 테스토스테론은 정상이라 사춘기에 음경 성장·근육 발달 같은 남성화가 일어나고 음모도 난다. 유방은 두드러지지 않는다. 이 선지가 정답이 되려면 사춘기 남성화와 모호한 외부생식기 병력이 있어야 한다.\n③ 칼만증후군은 GnRH 결핍으로 FSH·LH 가 낮아 에스트로겐이 없고 유방이 발달하지 않으며, 46,XX 라 자궁은 정상이고 후각 저하가 동반된다. 이 선지가 정답이 되려면 유방 미발달·자궁 있음·무후각이어야 한다.\n⑤ MRKH 는 46,XX 에서 뮐러관만 형성되지 않은 것이라 자궁은 없지만 난소가 정상이어서 음모·액모가 정상이고 테스토스테론은 여성 범위다. 이 선지가 정답이 되려면 음모가 정상이고 테스토스테론이 낮아야 한다."
   },
   {
    "k": "함정",
    "v": "「자궁 없음」만 보고 MRKH 로 가지 않는다 — 음모 유무와 테스토스테론 수치가 두 질환을 가른다."
   },
   {
    "k": "학습목표",
    "v": "원발무월경에서 음모 결여 + 남성 수준 테스토스테론으로 완전 안드로겐무감응 감별"
   },
   {
    "k": "근거·출처",
    "v": "표준 부인과 내분비 지식 — 원발무월경 감별(Speroff 9판 11장)"
   }
  ],
  "source": "의대_시험지_제작 오픈데이터 영상 세트 / 20260913T053235Z_일일영상_2026-09-13_10units_9q_7072fb0c",
  "vitals": [],
  "labs": [],
  "appendix": null,
  "figureImg": null,
  "attribution": {
   "dataset": "",
   "license": "",
   "license_url": "",
   "url": "",
   "asset_id": "",
   "text": ""
  },
  "run_id": "20260913T053235Z_일일영상_2026-09-13_10units_9q_7072fb0c",
  "qid": "Q0005"
 }
];
