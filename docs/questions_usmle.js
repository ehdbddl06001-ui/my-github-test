// 자동 생성 파일 — 수정하지 마세요.
// 원본: content/usmle/*.md  →  `python pipelines/export_usmle_web.py`로 재생성
window.USMLE_QUESTIONS = [
 {
  "id": "usmle-2026-0001",
  "exam": "usmle",
  "step": "Step 1",
  "subject": "Pharmacology",
  "subject_file": "Pharmacology",
  "subtopic": "Heart Failure Pharmacology",
  "type": "Heart Failure Pharmacology",
  "difficulty": 5,
  "created": "2026-07-02",
  "vignette": "A 58-year-old man with HFrEF (LVEF 30%) on lisinopril, carvedilol, and spironolactone is transitioned to sacubitril/valsartan after a 36-hour washout of lisinopril. Two weeks later his exertional dyspnea has improved and he has lost 2 kg, but a repeat serum B-type natriuretic peptide (BNP) is higher than his pretreatment value. His NT-proBNP is lower than baseline.",
  "question": "Which statement best explains this biomarker discordance?",
  "options": [
   "The rise in BNP indicates worsening congestion and the drug should be stopped",
   "Neprilysin inhibition reduces degradation of BNP, so BNP rises while NT-proBNP (not a neprilysin substrate) better reflects clinical response",
   "The valsartan component causes aldosterone escape, secondarily raising BNP",
   "Sacubitril cross-reacts with the BNP immunoassay, producing a falsely high value",
   "Anti-drug antibodies to sacubitril have formed, elevating BNP"
  ],
  "answer": 2,
  "explanationText": "- 핵심 기전: Sacubitril의 활성 대사체(sacubitrilat, LBQ657)는 neprilysin을\n  억제한다. Neprilysin은 natriuretic peptide(ANP·BNP·CNP), bradykinin,\n  adrenomedullin, substance P를 분해하는 효소다. 억제하면 natriuretic peptide가\n  올라가 이뇨·혈관확장·RAAS/교감신경 억제 효과를 낸다.\n- 정답근거(biomarker discordance): BNP는 neprilysin의 기질이므로 약물로\n  분해가 줄면 혈중 BNP가 상승한다. 반면 NT-proBNP는 neprilysin이 자르지\n  않으므로 심부전이 호전되면 감소한다. 그래서 ARNI 치료 중에는 반드시\n  NT-proBNP로 반응을 모니터링한다(BNP로 판단하면 악화로 오해).\n- 오답감별: (A) 증상·체중이 호전됐으므로 울혈 악화가 아니다. (C) 아니며\n  기전이 다르다. (D)(E) 실제 임상 현상이 아니다.\n- 임상핵심: ARNI 시작 전 ACEi는 36시간 washout(bradykinin 축적 →\n  angioedema 위험으로 ACEi와 병용 금기). 혈관부종 병력이 있으면 금기.\n- 출처: PARADIGM-HF (NEJM 2014); 2022 AHA/ACC/HFSA Heart Failure Guideline.",
  "explanationItems": [
   {
    "k": "핵심 기전",
    "v": "Sacubitril의 활성 대사체(sacubitrilat, LBQ657)는 neprilysin을 억제한다. Neprilysin은 natriuretic peptide(ANP·BNP·CNP), bradykinin, adrenomedullin, substance P를 분해하는 효소다. 억제하면 natriuretic peptide가 올라가 이뇨·혈관확장·RAAS/교감신경 억제 효과를 낸다."
   },
   {
    "k": "정답근거(biomarker discordance)",
    "v": "BNP는 neprilysin의 기질이므로 약물로 분해가 줄면 혈중 BNP가 상승한다. 반면 NT-proBNP는 neprilysin이 자르지 않으므로 심부전이 호전되면 감소한다. 그래서 ARNI 치료 중에는 반드시 *NT-proBNP로 반응을 모니터링한다(BNP로 판단하면 악화로 오해)."
   },
   {
    "k": "오답감별",
    "v": "(A) 증상·체중이 호전됐으므로 울혈 악화가 아니다. (C) 아니며 기전이 다르다. (D)(E) 실제 임상 현상이 아니다."
   },
   {
    "k": "임상핵심",
    "v": "ARNI 시작 전 ACEi는 36시간 washout(bradykinin 축적 → angioedema 위험으로 ACEi와 병용 금기). 혈관부종 병력이 있으면 금기."
   },
   {
    "k": "출처",
    "v": "PARADIGM-HF (NEJM 2014); 2022 AHA/ACC/HFSA Heart Failure Guideline."
   }
  ],
  "source": "USMLE-style / MedKOS (PARADIGM-HF, 2022 AHA/ACC/HFSA HF guideline)",
  "vitals": [],
  "labs": [],
  "appendix": null,
  "figureSvg": ""
 },
 {
  "id": "usmle-2026-0002",
  "exam": "usmle",
  "step": "Step 2",
  "subject": "Internal Medicine",
  "subject_file": "Internal Medicine",
  "subtopic": "Infective Endocarditis",
  "type": "Infective Endocarditis",
  "difficulty": 5,
  "created": "2026-07-02",
  "vignette": "A 72-year-old man has 3 weeks of low-grade fever, fatigue, and weight loss. He underwent screening colonoscopy 6 weeks ago that revealed an invasive colonic adenocarcinoma. Examination reveals a new murmur of aortic regurgitation; TEE shows a 9-mm aortic valve vegetation. Three sets of blood cultures grow Enterococcus faecalis that is susceptible to ampicillin and vancomycin but demonstrates high-level gentamicin resistance (HLGR). Renal function is normal.",
  "question": "Which antibiotic regimen is most appropriate?",
  "options": [
   "Ampicillin plus gentamicin",
   "Ampicillin plus ceftriaxone",
   "Vancomycin monotherapy",
   "Ceftriaxone monotherapy",
   "Daptomycin plus rifampin"
  ],
  "answer": 2,
  "explanationText": "- 진단: 아급성 심내막염 + E. faecalis 균혈증. 대장 신생물과 enterococcal/\n  *Streptococcus gallolyticus*(구 bovis) 균혈증의 연관은 고전적 단서다.\n- 정답근거: 전통적 상승 요법은 ampicillin + aminoglycoside지만, 본 균주는\n  HLGR이라 gentamicin 상승효과를 기대할 수 없고 독성만 남는다. 이때\n  ampicillin + ceftriaxone(이중 베타락탐)이 표준이다. 두 약이 서로 다른\n  penicillin-binding protein을 포화시켜(ampicillin→PBP4/5, ceftriaxone→\n  PBP2/3) 상승적 살균효과를 낸다. 신독성·이독성도 피할 수 있다.\n- 오답감별: (A) HLGR이라 gentamicin 무의미. (C) vancomycin 단독은 살균력이\n  약해 심내막염에 열등. (D) enterococcus는 저친화도 PBP5 때문에 cephalosporin\n  단독에 본질적 내성 → ceftriaxone 단독 무효. (E) daptomycin+rifampin은 이\n  적응증의 1차가 아니다.\n- 임상핵심: \"Enterococcus 심내막염 + HLGR → ampicillin + ceftriaxone.\"\n  Enterococcus에 cephalosporin 단독은 절대 쓰지 않는다.\n- 출처: AHA/IDSA Infective Endocarditis Guideline; Gavaldà et al. (Ann Intern Med).",
  "explanationItems": [
   {
    "k": "진단",
    "v": "아급성 심내막염 + E. faecalis 균혈증. 대장 신생물과 enterococcal/ Streptococcus gallolyticus*(구 bovis) 균혈증의 연관은 고전적 단서다."
   },
   {
    "k": "정답근거",
    "v": "전통적 상승 요법은 ampicillin + aminoglycoside지만, 본 균주는 *HLGR이라 gentamicin 상승효과를 기대할 수 없고 독성만 남는다. 이때 *ampicillin + ceftriaxone(이중 베타락탐)이 표준이다. 두 약이 서로 다른 *penicillin-binding protein을 포화시켜(ampicillin→PBP4/5, ceftriaxone→ PBP2/3) 상승적 살균효과를 낸다. 신독성·이독성도 피할 수 있다."
   },
   {
    "k": "오답감별",
    "v": "(A) HLGR이라 gentamicin 무의미. (C) vancomycin 단독은 살균력이 약해 심내막염에 열등. (D) enterococcus는 저친화도 PBP5 때문에 cephalosporin 단독에 본질적 내성 → ceftriaxone 단독 무효. (E) daptomycin+rifampin은 이 적응증의 1차가 아니다."
   },
   {
    "k": "임상핵심",
    "v": "\"Enterococcus 심내막염 + HLGR → ampicillin + ceftriaxone.\" Enterococcus에 cephalosporin 단독은 절대 쓰지 않는다."
   },
   {
    "k": "출처",
    "v": "AHA/IDSA Infective Endocarditis Guideline; Gavaldà et al. (Ann Intern Med)."
   }
  ],
  "source": "USMLE-style / MedKOS (AHA/IDSA infective endocarditis guideline)",
  "vitals": [],
  "labs": [],
  "appendix": null,
  "figureSvg": ""
 },
 {
  "id": "usmle-2026-0003",
  "exam": "usmle",
  "step": "Step 1",
  "subject": "Pharmacology",
  "subject_file": "Pharmacology",
  "subtopic": "Acid-Base (Mixed Disorder)",
  "type": "Acid-Base (Mixed Disorder)",
  "difficulty": 5,
  "created": "2026-07-02",
  "vignette": "A 19-year-old woman is brought in 4 hours after ingesting an unknown quantity of aspirin. She is tachypneic and reports tinnitus. Arterial blood gas on room air: pH 7.44, PaCO2 18 mmHg, HCO3- 12 mEq/L. Serum electrolytes: Na+ 140, Cl- 101, HCO3- 12 (anion gap 27).",
  "question": "Which of the following best characterizes her acid-base disorder?",
  "options": [
   "Acute respiratory alkalosis alone",
   "High anion gap metabolic acidosis with appropriate respiratory compensation",
   "Mixed high anion gap metabolic acidosis and primary respiratory alkalosis",
   "High anion gap metabolic acidosis with a superimposed metabolic alkalosis",
   "Primary respiratory acidosis"
  ],
  "answer": 3,
  "explanationText": "- 1단계 – 원발 장애: HCO3- 12로 낮고 AG 27로 높다 → 고음이온차 대사성 산증\n  이 존재.\n- 2단계 – 보상 적절성(Winter 공식): 예측 PaCO2 = 1.5×HCO3 + 8 ± 2 =\n  1.5×12 + 8 = 26 ± 2 (24–28). 실제 PaCO2 = 18로 예측보다 훨씬 낮다 →\n  단순 보상이 아니라 원발성 호흡성 알칼리증이 동반된 혼합장애. (그래서 pH가\n  7.44로 오히려 정상~약알칼리)\n- 정답근거(기전): Salicylate는 ① 연수 호흡중추를 직접 자극 → 호흡성 알칼리증,\n  ② 산화적 인산화 탈공역 + Krebs 회로 억제 → 젖산·케톤 축적으로 고AG 대사성\n  산증. 두 원발 장애가 동시에 나타난다.\n- 오답감별: (A) AG 상승·HCO3 저하를 설명 못 함. (B) 보상이라기엔 PaCO2가\n  과도하게 낮음(Winter 벗어남). (D) pH·HCO3 방향상 대사성 알칼리증 근거 없음.\n  (E) 과호흡·저PaCO2와 반대.\n- 임상핵심: 성인 salicylate 중독 = 고AG 대사성 산증 + 호흡성 알칼리증 혼합.\n  치료는 소변 알칼리화(NaHCO3, ion trapping), 중증(정신상태 변화·신부전·수치\n  매우 높음)이면 혈액투석. 산증 교정 실패 시 CNS로 salicylate 이동 → 삽관 시\n  과호흡 유지 못하면 악화되므로 주의.\n- 출처: Winter's formula; Goldfrank's Toxicologic Emergencies.",
  "explanationItems": [
   {
    "k": "1단계 – 원발 장애",
    "v": "HCO3- 12로 낮고 AG 27로 높다 → 고음이온차 대사성 산증 이 존재."
   },
   {
    "k": "2단계 – 보상 적절성(Winter 공식)",
    "v": "예측 PaCO2 = 1.5×HCO3 + 8 ± 2 = 1.5×12 + 8 = 26 ± 2 (24–28). 실제 PaCO2 = 18로 예측보다 훨씬 낮다 → 단순 보상이 아니라 원발성 호흡성 알칼리증이 동반된 혼합장애. (그래서 pH가 7.44로 오히려 정상~약알칼리)"
   },
   {
    "k": "정답근거(기전)",
    "v": "Salicylate는 ① 연수 호흡중추를 직접 자극 → 호흡성 알칼리증, ② 산화적 인산화 탈공역 + Krebs 회로 억제 → 젖산·케톤 축적으로 고AG 대사성 산증. 두 원발 장애가 동시에 나타난다."
   },
   {
    "k": "오답감별",
    "v": "(A) AG 상승·HCO3 저하를 설명 못 함. (B) 보상이라기엔 PaCO2가 과도하게 낮음(Winter 벗어남). (D) pH·HCO3 방향상 대사성 알칼리증 근거 없음.\n(E) 과호흡·저PaCO2와 반대."
   },
   {
    "k": "임상핵심",
    "v": "성인 salicylate 중독 = 고AG 대사성 산증 + 호흡성 알칼리증 혼합. 치료는 소변 알칼리화(NaHCO3, ion trapping), 중증(정신상태 변화·신부전·수치 매우 높음)이면 혈액투석. 산증 교정 실패 시 CNS로 salicylate 이동 → 삽관 시 과호흡 유지 못하면 악화되므로 주의."
   },
   {
    "k": "출처",
    "v": "Winter's formula; Goldfrank's Toxicologic Emergencies."
   }
  ],
  "source": "USMLE-style / MedKOS (Winter's formula; salicylate toxicology)",
  "vitals": [],
  "labs": [],
  "appendix": null,
  "figureSvg": ""
 },
 {
  "id": "usmle-2026-0004",
  "exam": "usmle",
  "step": "Step 2",
  "subject": "Surgery",
  "subject_file": "Surgery",
  "subtopic": "Pheochromocytoma",
  "type": "Pheochromocytoma",
  "difficulty": 4,
  "created": "2026-07-02",
  "vignette": "A 45-year-old woman has 6 months of episodic pounding headaches, palpitations, and diaphoresis. BP is 190/112 mmHg. Plasma free metanephrines are markedly elevated and abdominal CT shows a 4-cm right adrenal mass. Adrenalectomy is planned.",
  "question": "Which of the following is the most appropriate preoperative pharmacologic preparation?",
  "options": [
   "Start propranolol first, then add phenoxybenzamine once heart rate is controlled",
   "Start phenoxybenzamine (alpha-blockade) with volume expansion, then add a beta-blocker after adequate alpha-blockade",
   "Start metoprolol alone",
   "Proceed directly to surgery without medical preparation",
   "Start lisinopril alone"
  ],
  "answer": 2,
  "explanationText": "- 진단: 발작성 두통·심계항진·발한의 3징 + 고혈압 + 혈장 유리 metanephrine\n  상승 + 부신 종괴 → 갈색세포종(pheochromocytoma). 가장 민감한 검사가 혈장 유리\n  metanephrine이다.\n- 정답근거(순서가 핵심): alpha 차단을 먼저(phenoxybenzamine, 비가역적\n  비선택적 α; 또는 doxazosin) 10–14일 + 염분·수액으로 용적 보충. 충분한 α\n  차단 뒤 잔여/반사 빈맥에 beta 차단을 나중에 추가한다.\n- 오답감별(왜 beta 먼저는 금기인가): β를 먼저 주면 β2 매개 혈관확장이 사라지고\n  카테콜아민의 α 매개 혈관수축이 무저항(unopposed alpha)으로 작용해 고혈압\n  위기를 유발한다. 그래서 (A)(C)는 위험. (D) 무준비 수술은 술중 카테콜아민\n  급증으로 치명적. (E) ACEi 단독은 부적절.\n- 임상핵심: \"Alpha before beta, and never beta alone.\" 유전 연관: MEN2A/2B\n  (RET), von Hippel–Lindau, NF1, SDHx — 젊거나 양측/가족력이면 유전자 검사.\n- 출처: Endocrine Society Clinical Practice Guideline, Pheochromocytoma & Paraganglioma.",
  "explanationItems": [
   {
    "k": "진단",
    "v": "발작성 두통·심계항진·발한의 3징 + 고혈압 + 혈장 유리 metanephrine 상승 + 부신 종괴 → 갈색세포종(pheochromocytoma). 가장 민감한 검사가 혈장 유리 metanephrine이다."
   },
   {
    "k": "정답근거(순서가 핵심)",
    "v": "alpha 차단을 먼저(phenoxybenzamine, 비가역적 비선택적 α; 또는 doxazosin) 10–14일 + 염분·수액으로 용적 보충. 충분한 α 차단 뒤 잔여/반사 빈맥에 beta 차단을 나중에 추가한다."
   },
   {
    "k": "오답감별(왜 beta 먼저는 금기인가)",
    "v": "β를 먼저 주면 β2 매개 혈관확장이 사라지고 카테콜아민의 α 매개 혈관수축이 무저항(unopposed alpha)으로 작용해 고혈압 위기를 유발한다. 그래서 (A)(C)는 위험. (D) 무준비 수술은 술중 카테콜아민 급증으로 치명적. (E) ACEi 단독은 부적절."
   },
   {
    "k": "임상핵심",
    "v": "\"Alpha before beta, and never beta alone.\" 유전 연관: MEN2A/2B (RET), von Hippel–Lindau, NF1, SDHx — 젊거나 양측/가족력이면 유전자 검사."
   },
   {
    "k": "출처",
    "v": "Endocrine Society Clinical Practice Guideline, Pheochromocytoma & Paraganglioma."
   }
  ],
  "source": "USMLE-style / MedKOS (Endocrine Society pheochromocytoma guideline)",
  "vitals": [],
  "labs": [],
  "appendix": null,
  "figureSvg": ""
 },
 {
  "id": "usmle-2026-0005",
  "exam": "usmle",
  "step": "Step 2",
  "subject": "Internal Medicine",
  "subject_file": "Internal Medicine",
  "subtopic": "Heparin-Induced Thrombocytopenia",
  "type": "Heparin-Induced Thrombocytopenia",
  "difficulty": 5,
  "created": "2026-07-02",
  "vignette": "A 64-year-old man is on prophylactic unfractionated heparin after coronary artery bypass grafting. On postoperative day 6 his platelet count falls from 245,000 to 90,000/uL and he develops a new right lower-extremity deep vein thrombosis. A heparin-PF4 antibody ELISA is positive and a serotonin release assay confirms the diagnosis.",
  "question": "Which of the following is the most appropriate next step?",
  "options": [
   "Continue unfractionated heparin at a reduced dose",
   "Stop heparin and start warfarin immediately",
   "Stop all heparin and start argatroban; avoid platelet transfusion and defer warfarin until platelet recovery",
   "Transfuse platelets to correct the thrombocytopenia",
   "Switch from unfractionated heparin to low-molecular-weight heparin"
  ],
  "answer": 3,
  "explanationText": "- 진단: 전형적 HIT type II. 노출 5–10일 후 혈소판 >50% 감소 +\n  새로운 혈전(DVT) + heparin-PF4 항체·SRA 양성 (4T score 高).\n- 기전: heparin과 혈소판 α과립의 PF4가 복합체를 이루고, 이에 대한 IgG가\n  혈소판 Fc수용체를 교차결합 → 혈소판 활성화·응집 → 트롬빈 폭발. 혈소판은\n  줄지만 역설적으로 혈전이 생기는 친혈전성 상태.\n- 정답근거(관리 4원칙): ① 모든 heparin 중단(LMWH도 교차반응 → E 오답).\n  ② 비-heparin 항응고제 시작: argatroban·bivalirudin(직접 트롬빈 억제제) 또는\n  fondaparinux. ③ warfarin은 혈소판 회복(대개 >150k)까지 보류 — 급성기 단독\n  warfarin은 protein C 급감으로 정맥사지괴저·피부괴사 유발. ④ 혈소판 수혈\n  금지 — 혈전 악화(D 오답).\n- 오답감별: (A) heparin 지속은 절대 금기. (B) 즉시 warfarin은 괴사 위험.\n  (D) 혈소판 수혈은 연료 공급. (E) LMWH도 HIT 항체와 교차반응.\n- 임상핵심: \"HIT = clotting disorder, not just low platelets.\" heparin 끊고\n  DTI로 bridge, warfarin은 겹쳐서(overlap) 혈소판 회복 후.\n- 출처: ASH 2018 Guidelines on Management of VTE / HIT.",
  "explanationItems": [
   {
    "k": "진단",
    "v": "전형적 HIT type II. 노출 5–10일 후 혈소판 >50% 감소 + *새로운 혈전(DVT) + heparin-PF4 항체·SRA 양성 (4T score 高)."
   },
   {
    "k": "기전",
    "v": "heparin과 혈소판 α과립의 PF4가 복합체를 이루고, 이에 대한 IgG가 혈소판 Fc수용체를 교차결합 → 혈소판 활성화·응집 → 트롬빈 폭발. 혈소판은 줄지만 역설적으로 혈전이 생기는 친혈전성 상태."
   },
   {
    "k": "정답근거(관리 4원칙)",
    "v": "① 모든 heparin 중단(LMWH도 교차반응 → E 오답). ② 비-heparin 항응고제 시작: argatroban·bivalirudin(직접 트롬빈 억제제) 또는 fondaparinux. ③ warfarin은 혈소판 회복(대개 >150k)까지 보류 — 급성기 단독 warfarin은 protein C 급감으로 정맥사지괴저·피부괴사 유발. ④ 혈소판 수혈 금지 — 혈전 악화(D 오답)."
   },
   {
    "k": "오답감별",
    "v": "(A) heparin 지속은 절대 금기. (B) 즉시 warfarin은 괴사 위험.\n(D) 혈소판 수혈은 연료 공급. (E) LMWH도 HIT 항체와 교차반응."
   },
   {
    "k": "임상핵심",
    "v": "\"HIT = clotting disorder, not just low platelets.\" heparin 끊고 DTI로 bridge, warfarin은 겹쳐서(overlap) 혈소판 회복 후."
   },
   {
    "k": "출처",
    "v": "ASH 2018 Guidelines on Management of VTE / HIT."
   }
  ],
  "source": "USMLE-style / MedKOS (ASH 2018 VTE/HIT guideline)",
  "vitals": [],
  "labs": [],
  "appendix": null,
  "figureSvg": ""
 },
 {
  "id": "usmle-2026-0006",
  "exam": "usmle",
  "step": "Step 1",
  "subject": "Immunology",
  "subject_file": "Immunology",
  "subtopic": "Chronic Granulomatous Disease",
  "type": "Chronic Granulomatous Disease",
  "difficulty": 4,
  "created": "2026-07-02",
  "vignette": "A 2-year-old boy has had recurrent Staphylococcus aureus lymphadenitis, a Serratia marcescens skin abscess, and an Aspergillus pneumonia, plus a hepatic abscess. Neutrophil count is normal. A dihydrorhodamine (DHR) flow-cytometry oxidative-burst assay shows markedly reduced fluorescence after stimulation.",
  "question": "Which of the following underlying defects best explains this presentation?",
  "options": [
   "Defective NADPH oxidase (chronic granulomatous disease)",
   "Defective CD18/beta-2 integrin (leukocyte adhesion deficiency type 1)",
   "Defective Bruton tyrosine kinase (X-linked agammaglobulinemia)",
   "WAS gene mutation (Wiskott-Aldrich syndrome)",
   "IL-12 receptor deficiency"
  ],
  "answer": 1,
  "explanationText": "- 진단: 만성 육아종병(CGD). 가장 흔한 형태는 X-연관 gp91phox 결손.\n- 기전: 호중구 NADPH oxidase가 산소를 O2−(superoxide)로 환원하는 호흡\n  폭발(respiratory burst)을 못 한다. 그래서 자신의 H2O2를 분해해버리는\n  catalase-양성 미생물(S. aureus, Serratia, Burkholderia cepacia,\n  Nocardia, Aspergillus)을 죽이지 못한다(catalase-음성균은 자기 H2O2를 남겨\n  호중구가 이용 → 상대적으로 문제 적음).\n- 검사: DHR 유세포검사(활성산소 있으면 형광↑; CGD는 감소) 또는 고전적\n  nitroblue tetrazolium(NBT) 검사 음성.\n- 오답감별: (B) LAD-1은 CD18 integrin 결손 → 지연된 탯줄 탈락, 농(pus)\n  형성 안 됨, 백혈구 증가. (C) XLA는 B세포·면역글로불린 부재 → 협막균 재발.\n  (D) WAS는 습진·혈소판감소·감염 3징(X-연관). (E) IL-12R 결핍은 파종성\n  mycobacteria/Salmonella.\n- 임상핵심: 재발 catalase-양성 감염 + 육아종/농양 → CGD. 예방: TMP-SMX +\n  itraconazole + IFN-γ.\n- 출처: Janeway's Immunobiology; primary immunodeficiency reviews.",
  "explanationItems": [
   {
    "k": "진단",
    "v": "만성 육아종병(CGD). 가장 흔한 형태는 X-연관 gp91phox 결손."
   },
   {
    "k": "기전",
    "v": "호중구 NADPH oxidase가 산소를 O2−(superoxide)로 환원하는 호흡 폭발(respiratory burst)을 못 한다. 그래서 자신의 H2O2를 분해해버리는 *catalase-양성 미생물(S. aureus, Serratia, Burkholderia cepacia, Nocardia, Aspergillus)을 죽이지 못한다(catalase-음성균은 자기 H2O2를 남겨 호중구가 이용 → 상대적으로 문제 적음)."
   },
   {
    "k": "검사",
    "v": "DHR 유세포검사(활성산소 있으면 형광↑; CGD는 감소) 또는 고전적 *nitroblue tetrazolium(NBT) 검사 음성."
   },
   {
    "k": "오답감별",
    "v": "(B) LAD-1은 CD18 integrin 결손 → 지연된 탯줄 탈락, 농(pus) 형성 안 됨, 백혈구 증가. (C) XLA는 B세포·면역글로불린 부재 → 협막균 재발.\n(D) WAS는 습진·혈소판감소·감염 3징(X-연관). (E) IL-12R 결핍은 파종성 *mycobacteria/Salmonella."
   },
   {
    "k": "임상핵심",
    "v": "재발 catalase-양성 감염 + 육아종/농양 → CGD. 예방: TMP-SMX + itraconazole + IFN-γ."
   },
   {
    "k": "출처",
    "v": "Janeway's Immunobiology; primary immunodeficiency reviews."
   }
  ],
  "source": "USMLE-style / MedKOS (primary immunodeficiency)",
  "vitals": [],
  "labs": [],
  "appendix": null,
  "figureSvg": ""
 },
 {
  "id": "usmle-2026-0007",
  "exam": "usmle",
  "step": "Step 2",
  "subject": "Neurology",
  "subject_file": "Neurology",
  "subtopic": "Lambert-Eaton Myasthenic Syndrome",
  "type": "Lambert-Eaton Myasthenic Syndrome",
  "difficulty": 5,
  "created": "2026-07-02",
  "vignette": "A 62-year-old man with a 40-pack-year smoking history reports several months of proximal lower-limb weakness and difficulty rising from a chair. He notes that grip strength briefly improves after sustained effort. He also has dry mouth and reduced knee reflexes that become detectable after brief exercise. Repetitive nerve stimulation shows a low baseline compound muscle action potential that increases by >100% at high frequency (or after exercise).",
  "question": "Which of the following is the most likely pathophysiologic mechanism?",
  "options": [
   "Autoantibodies against postsynaptic nicotinic acetylcholine receptors",
   "Autoantibodies against presynaptic P/Q-type voltage-gated calcium channels",
   "Autoantibodies against muscle-specific kinase (MuSK)",
   "Autoantibodies against voltage-gated potassium channels",
   "Autoantibodies against the ganglioside GM1"
  ],
  "answer": 2,
  "explanationText": "- 진단: Lambert-Eaton 근무력증후군(LEMS). 근위부 위약 + 노력 시 일시적\n  호전(facilitation) + 자율신경 증상(구강건조·변비) + 반사 저하 +\n  고빈도 반복신경자극에서 incremental 반응(진폭 증가) + 강한 흡연력.\n- 기전: presynaptic P/Q형 전압의존성 칼슘통로(VGCC)에 대한 자가항체 →\n  신경말단으로 Ca²⁺ 유입 감소 → ACh 방출 감소. 반복 자극·운동으로 말단에\n  Ca²⁺이 축적되면 방출이 늘어 일시 호전(MG와 반대).\n- 부종양 연관: 약 50%에서 소세포폐암(SCLC) — 종양 항원이 VGCC와 교차반응.\n  진단 시 흉부 영상으로 반드시 악성 조사.\n- 오답감별(MG와 대조): (A) MG는 postsynaptic AChR 항체 → 사용할수록\n  악화(decremental), 안구·연수 증상 먼저, 반사 정상, 자율신경 정상. (C) MuSK\n  항체는 seronegative MG의 일부. (D) VGKC는 신경근긴장(neuromyotonia)/변연계뇌염.\n  (E) 항-GM1은 다초점운동신경병/GBS 변형.\n- 임상핵심: LEMS = presynaptic VGCC, 노력 시 호전, incremental RNS, SCLC\n  탐색. 치료: 기저 종양 치료 + 3,4-diaminopyridine(칼륨통로 차단으로 ACh 방출↑).\n- 출처: Adams & Victor's Principles of Neurology; paraneoplastic syndrome reviews.",
  "explanationItems": [
   {
    "k": "진단",
    "v": "Lambert-Eaton 근무력증후군(LEMS). 근위부 위약 + 노력 시 일시적 호전(facilitation) + 자율신경 증상(구강건조·변비) + 반사 저하 + 고빈도 반복신경자극에서 incremental 반응(진폭 증가) + 강한 흡연력."
   },
   {
    "k": "기전",
    "v": "presynaptic P/Q형 전압의존성 칼슘통로(VGCC)에 대한 자가항체 → 신경말단으로 Ca²⁺ 유입 감소 → ACh 방출 감소. 반복 자극·운동으로 말단에 Ca²⁺이 축적되면 방출이 늘어 일시 호전(MG와 반대)."
   },
   {
    "k": "부종양 연관",
    "v": "약 50%에서 소세포폐암(SCLC) — 종양 항원이 VGCC와 교차반응. 진단 시 흉부 영상으로 반드시 악성 조사."
   },
   {
    "k": "오답감별(MG와 대조)",
    "v": "(A) MG는 postsynaptic AChR 항체 → 사용할수록 악화(decremental), 안구·연수 증상 먼저, 반사 정상, 자율신경 정상. (C) MuSK 항체는 seronegative MG의 일부. (D) VGKC는 신경근긴장(neuromyotonia)/변연계뇌염.\n(E) 항-GM1은 다초점운동신경병/GBS 변형."
   },
   {
    "k": "임상핵심",
    "v": "LEMS = presynaptic VGCC, 노력 시 호전, incremental RNS, SCLC 탐색. 치료: 기저 종양 치료 + 3,4-diaminopyridine(칼륨통로 차단으로 ACh 방출↑)."
   },
   {
    "k": "출처",
    "v": "Adams & Victor's Principles of Neurology; paraneoplastic syndrome reviews."
   }
  ],
  "source": "USMLE-style / MedKOS (paraneoplastic neurology)",
  "vitals": [],
  "labs": [],
  "appendix": null,
  "figureSvg": ""
 },
 {
  "id": "usmle-2026-0008",
  "exam": "usmle",
  "step": "Step 1",
  "subject": "Biochemistry",
  "subject_file": "Biochemistry",
  "subtopic": "Urea Cycle (Ornithine Transcarbamylase Deficiency)",
  "type": "Urea Cycle (Ornithine Transcarbamylase Deficiency)",
  "difficulty": 5,
  "created": "2026-07-02",
  "vignette": "A male neonate is normal at birth but on day 3 of life becomes lethargic and feeds poorly, then develops tachypnea and seizures. Laboratory studies show a markedly elevated plasma ammonia, a low BUN, and a respiratory alkalosis. Urine orotic acid is elevated, and there is no megaloblastic anemia. Plasma citrulline is low.",
  "question": "Which enzyme deficiency best explains these findings?",
  "options": [
   "Ornithine transcarbamylase",
   "Carbamoyl phosphate synthetase I",
   "UMP synthase (hereditary orotic aciduria)",
   "Medium-chain acyl-CoA dehydrogenase",
   "Phenylalanine hydroxylase"
  ],
  "answer": 1,
  "explanationText": "- 진단: Ornithine transcarbamylase(OTC) 결핍 — 가장 흔한 요소회로 장애,\n  유일한 X-연관(남아에서 중증). 신생아 초기 정상 → 단백 부하(수유) 후 급성\n  고암모니아혈증 뇌증.\n- 기전(왜 orotic acid가 오르나): OTC는 미토콘드리아에서 carbamoyl phosphate\n  + ornithine → citrulline을 만든다. 결핍되면 carbamoyl phosphate가 축적 →\n  세포질 피리미딘 합성 경로로 유입 → orotic acid ↑. citrulline은 만들지\n  못해 낮다. 암모니아가 요소로 처리되지 못해 BUN은 낮고, 암모니아가 호흡\n  중추를 자극해 호흡성 알칼리증(신생아 고암모니아혈증의 단서).\n- 오답감별(감별의 핵심):\n  - (B) CPS1 결핍: carbamoyl phosphate 자체를 못 만들어 상류가 비므로\n    orotic acid는 정상/낮음 — 본 증례처럼 orotic acid↑와 맞지 않음.\n  - (C) UMP synthase 결핍(유전성 orotic aciduria): orotic aciduria는 같지만\n    거대적혈모구빈혈(+)이고 고암모니아혈증은 없다 — 본 증례와 반대.\n  - (D) MCAD 결핍: 금식 시 저케톤성 저혈당, 고암모니아혈증·orotic aciduria\n    아님.\n  - (E) PKU: 발달지연·musty odor, 요소회로와 무관.\n- 임상핵심: \"고암모니아혈증 + orotic aciduria + 거대적혈모구빈혈 없음 →\n  OTC.\" 있으면 UMP synthase. 급성치료: 단백 제한, sodium benzoate/\n  phenylbutyrate(질소 우회 배설), arginine 보충, 중증이면 혈액투석.\n- 출처: Lippincott Biochemistry; inborn errors of metabolism references.",
  "explanationItems": [
   {
    "k": "진단",
    "v": "Ornithine transcarbamylase(OTC) 결핍 — 가장 흔한 요소회로 장애, 유일한 X-연관(남아에서 중증). 신생아 초기 정상 → 단백 부하(수유) 후 급성 *고암모니아혈증 뇌증."
   },
   {
    "k": "기전(왜 orotic acid가 오르나)",
    "v": "OTC는 미토콘드리아에서 carbamoyl phosphate + ornithine → citrulline을 만든다. 결핍되면 carbamoyl phosphate가 축적 → 세포질 피리미딘 합성 경로로 유입 → orotic acid ↑. citrulline은 만들지 못해 낮다. 암모니아가 요소로 처리되지 못해 BUN은 낮고, 암모니아가 호흡 중추를 자극해 호흡성 알칼리증(신생아 고암모니아혈증의 단서)."
   },
   {
    "k": "오답감별(감별의 핵심)",
    "v": "(B) CPS1 결핍: carbamoyl phosphate 자체를 못 만들어 상류가 비므로 *orotic acid는 정상/낮음 — 본 증례처럼 orotic acid↑와 맞지 않음.\n(C) UMP synthase 결핍(유전성 orotic aciduria): orotic aciduria는 같지만 *거대적혈모구빈혈(+)이고 고암모니아혈증은 없다 — 본 증례와 반대.\n(D) MCAD 결핍: 금식 시 저케톤성 저혈당, 고암모니아혈증·orotic aciduria 아님.\n(E) PKU: 발달지연·musty odor, 요소회로와 무관."
   },
   {
    "k": "임상핵심",
    "v": "\"고암모니아혈증 + orotic aciduria + 거대적혈모구빈혈 없음 → OTC.\" 있으면 UMP synthase. 급성치료: 단백 제한, sodium benzoate/ phenylbutyrate(질소 우회 배설), arginine 보충, 중증이면 혈액투석."
   },
   {
    "k": "출처",
    "v": "Lippincott Biochemistry; inborn errors of metabolism references."
   }
  ],
  "source": "USMLE-style / MedKOS (inborn errors of metabolism)",
  "vitals": [],
  "labs": [],
  "appendix": null,
  "figureSvg": ""
 },
 {
  "id": "usmle-2026-0009",
  "exam": "usmle",
  "step": "Step 1",
  "subject": "Immunology",
  "subject_file": "Immunology",
  "subtopic": "Terminal Complement Deficiency",
  "type": "Terminal Complement Deficiency",
  "difficulty": 4,
  "created": "2026-07-02",
  "vignette": "An 18-year-old college student is admitted with his second lifetime episode of Neisseria meningitidis meningitis; he had a documented meningococcal bacteremia at age 12. Immunoglobulin levels and T- and B-cell counts are normal. Total hemolytic complement activity (CH50) is undetectable, while C3 is normal.",
  "question": "Which of the following best explains his susceptibility?",
  "options": [
   "Deficiency of a terminal complement component (C5-C9), impairing formation of the membrane attack complex",
   "C3 deficiency",
   "C1 esterase inhibitor deficiency",
   "Bruton tyrosine kinase deficiency (X-linked agammaglobulinemia)",
   "Selective IgA deficiency"
  ],
  "answer": 1,
  "explanationText": "- 진단: 말단 보체(terminal complement) 결핍 — C5, C6, C7, C8, C9 중 하나.\n- 정답근거: CH50은 고전경로 + 말단경로(C1–C9) 전체 기능을 본다. 말단 성분이\n  없으면 CH50이 0이지만 C3는 정상이다. 완성된 MAC(막공격복합체)은\n  세포벽이 얇은 Neisseria를 직접 용해하는 유일한 방어라, 결핍 시 수막알균·\n  임균 감염이 재발한다.\n- 오답감별: (B) C3 결핍이면 C3 낮고 화농균·협막균 중증 감염 + 옵소닌화 장애.\n  (C) C1 INH 결핍은 유전성 혈관부종(감염 아님). (D) XLA는 협막균 재발·면역\n  글로불린 저하. (E) 선택적 IgA는 대개 경미, 점막감염/아나필락시스(수혈).\n- 임상핵심: \"재발성 Neisseria → 말단 보체(또는 properdin) 결핍 의심, CH50\n  확인.\" 예방: 수막알균 백신(혈청군 ACWY + B). Properdin 결핍은 X-연관으로\n  전격성 수막알균혈증.\n- 출처: Janeway's Immunobiology; complement deficiency reviews.",
  "explanationItems": [
   {
    "k": "진단",
    "v": "말단 보체(terminal complement) 결핍 — C5, C6, C7, C8, C9 중 하나."
   },
   {
    "k": "정답근거",
    "v": "CH50은 고전경로 + 말단경로(C1–C9) 전체 기능을 본다. 말단 성분이 없으면 CH50이 0이지만 C3는 정상이다. 완성된 MAC(막공격복합체)은 세포벽이 얇은 Neisseria를 직접 용해하는 유일한 방어라, 결핍 시 수막알균· 임균 감염이 재발한다."
   },
   {
    "k": "오답감별",
    "v": "(B) C3 결핍이면 C3 낮고 화농균·협막균 중증 감염 + 옵소닌화 장애.\n(C) C1 INH 결핍은 유전성 혈관부종(감염 아님). (D) XLA는 협막균 재발·면역 글로불린 저하. (E) 선택적 IgA는 대개 경미, 점막감염/아나필락시스(수혈)."
   },
   {
    "k": "임상핵심",
    "v": "\"재발성 Neisseria → 말단 보체(또는 properdin) 결핍 의심, CH50 확인.\" 예방: 수막알균 백신(혈청군 ACWY + B). Properdin 결핍은 X-연관으로 전격성 수막알균혈증."
   },
   {
    "k": "출처",
    "v": "Janeway's Immunobiology; complement deficiency reviews."
   }
  ],
  "source": "USMLE-style / MedKOS (complement immunodeficiency)",
  "vitals": [],
  "labs": [],
  "appendix": null,
  "figureSvg": ""
 },
 {
  "id": "usmle-2026-0010",
  "exam": "usmle",
  "step": "Step 1",
  "subject": "Biochemistry",
  "subject_file": "Biochemistry",
  "subtopic": "Acute Intermittent Porphyria",
  "type": "Acute Intermittent Porphyria",
  "difficulty": 5,
  "created": "2026-07-02",
  "vignette": "A 28-year-old woman has recurrent attacks of severe, poorly localized abdominal pain with no peritoneal signs, accompanied by tachycardia, hyponatremia, anxiety, and a symmetric motor neuropathy. Attacks are triggered by fasting and by starting phenobarbital; her urine darkens on standing. There is no photosensitivity. Urinary delta-aminolevulinic acid (ALA) and porphobilinogen (PBG) are markedly elevated.",
  "question": "Which enzyme is deficient?",
  "options": [
   "Porphobilinogen deaminase (hydroxymethylbilane synthase)",
   "Ferrochelatase",
   "Uroporphyrinogen decarboxylase",
   "ALA dehydratase",
   "Glucose-6-phosphate dehydrogenase"
  ],
  "answer": 1,
  "explanationText": "- 진단: 급성 간헐성 포르피린증(AIP) — 상염색체 우성, porphobilinogen\n  deaminase(=hydroxymethylbilane synthase) 결핍.\n- 정답근거(왜 이 증상/검사인가): 결핍 지점의 상류 대사물 ALA·PBG가 축적 →\n  신경독성으로 복통(자율신경)·신경정신·운동신경병. 결손이 uroporphyrinogen\n  생성 이전이라 광과민성 색소가 안 쌓여 광과민성이 없다(5P: Painful abdomen,\n  Polyneuropathy, Psychological, Port-wine urine, Precipitated by drugs).\n- 유발기전: CYP 유도제(barbiturate, rifampin, phenytoin), 금식, 흡연,\n  황체기가 ALA synthase(율속효소)를 유도 → 발작 악화.\n- 오답감별: (B) ferrochelatase → erythropoietic protoporphyria(광과민성).\n  (C) uroporphyrinogen decarboxylase → porphyria cutanea tarda(광과민·수포,\n  가장 흔함). (D) ALA dehydratase 결핍/납중독은 드묾. (E) G6PD는 heme 합성과 무관\n  (용혈).\n- 임상핵심: 급성 발작 치료 = 정맥 hemin + 포도당(glucose loading) →\n  ALA synthase 음성되먹임 억제. 유발약물 회피.\n- 출처: Lippincott Biochemistry; porphyria reviews.",
  "explanationItems": [
   {
    "k": "진단",
    "v": "급성 간헐성 포르피린증(AIP) — 상염색체 우성, porphobilinogen deaminase(=hydroxymethylbilane synthase) 결핍."
   },
   {
    "k": "정답근거(왜 이 증상/검사인가)",
    "v": "결핍 지점의 상류 대사물 ALA·PBG가 축적 → 신경독성으로 복통(자율신경)·신경정신·운동신경병. 결손이 uroporphyrinogen 생성 이전이라 광과민성 색소가 안 쌓여 광과민성이 없다(5P: Painful abdomen, Polyneuropathy, Psychological, Port-wine urine, Precipitated by drugs)."
   },
   {
    "k": "유발기전",
    "v": "CYP 유도제(barbiturate, rifampin, phenytoin), 금식, 흡연, 황체기가 ALA synthase(율속효소)를 유도 → 발작 악화."
   },
   {
    "k": "오답감별",
    "v": "(B) ferrochelatase → erythropoietic protoporphyria(광과민성).\n(C) uroporphyrinogen decarboxylase → porphyria cutanea tarda(광과민·수포, 가장 흔함). (D) ALA dehydratase 결핍/납중독은 드묾. (E) G6PD는 heme 합성과 무관 (용혈)."
   },
   {
    "k": "임상핵심",
    "v": "급성 발작 치료 = 정맥 hemin + 포도당(glucose loading) → ALA synthase 음성되먹임 억제. 유발약물 회피."
   },
   {
    "k": "출처",
    "v": "Lippincott Biochemistry; porphyria reviews."
   }
  ],
  "source": "USMLE-style / MedKOS (heme synthesis, porphyrias)",
  "vitals": [],
  "labs": [],
  "appendix": null,
  "figureSvg": ""
 },
 {
  "id": "usmle-2026-0011",
  "exam": "usmle",
  "step": "Step 1",
  "subject": "Microbiology",
  "subject_file": "Microbiology",
  "subtopic": "Vancomycin Resistance (VRE)",
  "type": "Vancomycin Resistance (VRE)",
  "difficulty": 4,
  "created": "2026-07-02",
  "vignette": "A hospitalized patient develops bacteremia with Enterococcus faecium that is resistant to vancomycin. The resistance is mediated by an acquired operon carried on a transposon.",
  "question": "Which molecular change most directly accounts for the vancomycin resistance?",
  "options": [
   "Substitution of the peptidoglycan precursor terminus from D-Ala-D-Ala to D-Ala-D-Lactate",
   "Production of an extended-spectrum beta-lactamase",
   "Acquisition of mecA encoding an altered penicillin-binding protein 2a",
   "Upregulation of a multidrug efflux pump",
   "Methylation of the 23S ribosomal RNA target"
  ],
  "answer": 1,
  "explanationText": "- 기전: Vancomycin은 펩티도글리칸 전구체의 말단 D-Ala-D-Ala에 수소결합해\n  transglycosylation/가교를 막는다. VanA형 VRE는 van 오페론(ligase)이 말단을\n  D-Ala-D-Lactate로 바꿔 수소결합 하나를 잃게 만들어 친화도를 약 1000배\n  떨어뜨린다 → 내성.\n- 오답감별: (B) β-lactamase는 페니실린/세팔로스포린을 가수분해(반코마이신과\n  무관). (C) mecA→PBP2a는 MRSA의 β-lactam 내성 기전. (D) efflux는\n  tetracycline 등. (E) erm 메틸화(23S rRNA)는 macrolide(MLSb) 내성.\n- 임상핵심: \"VRE(VanA) = D-Ala-D-Lac.\" 치료는 linezolid 또는\n  daptomycin(중증 균혈증). MRSA와 혼동 금지(그건 PBP2a).\n- 출처: Murray Medical Microbiology; antimicrobial resistance reviews.",
  "explanationItems": [
   {
    "k": "기전",
    "v": "Vancomycin은 펩티도글리칸 전구체의 말단 D-Ala-D-Ala에 수소결합해 transglycosylation/가교를 막는다. VanA형 VRE는 van 오페론(ligase)이 말단을 *D-Ala-D-Lactate로 바꿔 수소결합 하나를 잃게 만들어 친화도를 약 1000배 떨어뜨린다 → 내성."
   },
   {
    "k": "오답감별",
    "v": "(B) β-lactamase는 페니실린/세팔로스포린을 가수분해(반코마이신과 무관). (C) mecA→PBP2a는 MRSA의 β-lactam 내성 기전. (D) efflux는 tetracycline 등. (E) erm 메틸화(23S rRNA)는 macrolide(MLSb) 내성."
   },
   {
    "k": "임상핵심",
    "v": "\"VRE(VanA) = D-Ala-D-Lac.\" 치료는 linezolid 또는 *daptomycin(중증 균혈증). MRSA와 혼동 금지(그건 PBP2a)."
   },
   {
    "k": "출처",
    "v": "Murray Medical Microbiology; antimicrobial resistance reviews."
   }
  ],
  "source": "USMLE-style / MedKOS (antimicrobial resistance)",
  "vitals": [],
  "labs": [],
  "appendix": null,
  "figureSvg": ""
 },
 {
  "id": "usmle-2026-0012",
  "exam": "usmle",
  "step": "Step 1",
  "subject": "Microbiology",
  "subject_file": "Microbiology",
  "subtopic": "Exotoxin Mechanism (EF-2 ADP-ribosylation)",
  "type": "Exotoxin Mechanism (EF-2 ADP-ribosylation)",
  "difficulty": 5,
  "created": "2026-07-02",
  "vignette": "A 6-year-old unvaccinated child develops a gray pseudomembrane over the tonsils, a bull neck, and, one week later, myocarditis with heart block. The responsible toxin halts host protein synthesis. This toxin shares its precise molecular mechanism with the exotoxin A of Pseudomonas aeruginosa.",
  "question": "Which mechanism is it?",
  "options": [
   "ADP-ribosylation of elongation factor 2 (EF-2), inactivating it and arresting translation",
   "ADP-ribosylation of the Gs-alpha subunit, persistently raising cAMP",
   "Removal of an adenine from 28S rRNA of the 60S ribosomal subunit",
   "Cleavage of SNARE proteins, blocking neurotransmitter release",
   "Cross-linking of MHC class II and the T-cell receptor as a superantigen"
  ],
  "answer": 1,
  "explanationText": "- 기전: Corynebacterium diphtheriae 독소와 Pseudomonas exotoxin A는\n  모두 EF-2를 ADP-ribosylation하여 불활성화 → 단백질 합성 정지 → 세포\n  사멸. 임상: 인두 위막, 심근염(전도장애), 뇌신경/말초 신경병.\n- 오답감별(독소 기전 비교):\n  - (B) Gs ADP-ribosylation → cAMP↑: 콜레라 독소, ETEC 이열성독소(LT),\n    백일해는 Gi 억제로 cAMP↑.\n  - (C) 28S rRNA에서 아데닌 제거(60S 불활성): Shiga / Shiga-like(EHEC)\n    독소 → HUS.\n  - (D) SNARE 절단: 보툴리눔(ACh 방출 차단→이완마비), 파상풍(glycine/\n    GABA 방출 차단→경직마비).\n  - (E) 초항원(superantigen): TSST-1, 연쇄상구균 발열외독소 → 다량\n    사이토카인.\n- 임상핵심: \"EF-2 ADP-ribosylation = 디프테리아 + Pseudomonas exotoxin A.\"\n  치료/예방: 디프테리아 항독소 + 백신(toxoid).\n- 출처: Murray Medical Microbiology.",
  "explanationItems": [
   {
    "k": "기전",
    "v": "Corynebacterium diphtheriae 독소와 Pseudomonas exotoxin A는 모두 EF-2를 ADP-ribosylation하여 불활성화 → 단백질 합성 정지 → 세포 사멸. 임상: 인두 위막, 심근염(전도장애), 뇌신경/말초 신경병."
   },
   {
    "k": "오답감별(독소 기전 비교)",
    "v": "(B) Gs ADP-ribosylation → cAMP↑: 콜레라 독소, ETEC 이열성독소(LT), 백일해는 Gi 억제로 cAMP↑.\n(C) 28S rRNA에서 아데닌 제거(60S 불활성): Shiga / Shiga-like(EHEC) 독소 → HUS.\n(D) SNARE 절단: 보툴리눔(ACh 방출 차단→이완마비), 파상풍(glycine/ GABA 방출 차단→경직마비).\n(E) 초항원(superantigen): TSST-1, 연쇄상구균 발열외독소 → 다량 사이토카인."
   },
   {
    "k": "임상핵심",
    "v": "\"EF-2 ADP-ribosylation = 디프테리아 + Pseudomonas exotoxin A.\" 치료/예방: 디프테리아 항독소 + 백신(toxoid)."
   },
   {
    "k": "출처",
    "v": "Murray Medical Microbiology."
   }
  ],
  "source": "USMLE-style / MedKOS (bacterial toxins)",
  "vitals": [],
  "labs": [],
  "appendix": null,
  "figureSvg": ""
 },
 {
  "id": "usmle-2026-0013",
  "exam": "usmle",
  "step": "Step 2",
  "subject": "Surgery",
  "subject_file": "Surgery",
  "subtopic": "Acute Mesenteric Ischemia",
  "type": "Acute Mesenteric Ischemia",
  "difficulty": 5,
  "created": "2026-07-02",
  "vignette": "A 74-year-old man with atrial fibrillation who is not on anticoagulation develops sudden severe periumbilical pain. On examination the abdomen is soft with pain that is strikingly out of proportion to the benign findings. Two hours later he passes bloody stool; lactate is elevated with a metabolic acidosis. CT angiography shows an abrupt cutoff of the superior mesenteric artery.",
  "question": "Which of the following is the most appropriate management?",
  "options": [
   "Emergent revascularization (embolectomy or endovascular therapy) with systemic anticoagulation and resection of any nonviable bowel",
   "Intravenous antibiotics and bowel rest for presumed diverticulitis",
   "Outpatient workup for chronic mesenteric ischemia",
   "Reassurance and antispasmodics for irritable bowel syndrome",
   "Supportive care alone for ischemic colitis"
  ],
  "answer": 1,
  "explanationText": "- 진단: 급성 장간막 허혈 — SMA 색전. 심방세동(비항응고)에서 좌심방\n  혈전이 SMA(대개 middle colic 분지 직후)로 색전. 특징: 진찰 소견에 비해 과도한\n  통증(pain out of proportion) → 늦으면 혈변·복막염·젖산성 산증(장괴사 신호).\n- 정답근거: 장 생존이 시간에 달려 있어 즉시 혈관재개통(외과적 색전제거 또는\n  endovascular) + heparin 항응고 + 괴사 부위 절제. 지연 = 사망.\n- 오답감별: (B) 게실염은 좌하복부·발열·국소압통. (C) 만성 장간막 허혈은\n  식후 복통·체중감소(intestinal angina)로 경과가 다름. (D) IBS는 급성 복증·젖산\n  산증과 무관. (E) 허혈성 대장염(분수계, IMA 영역, 고령·저혈압 후)은 대개\n  보존적이지만, 본 증례는 SMA 급성 색전으로 외과적 응급.\n- 임상핵심: \"AF + pain out of proportion + lactate↑ → 급성 SMA 허혈, 응급\n  재개통.\" 정상 젖산·연성 복부라도 배제 못 함(초기엔 정상일 수 있음).\n- 출처: Sabiston/Schwartz Surgery; ACG/SVS guidance.",
  "explanationItems": [
   {
    "k": "진단",
    "v": "급성 장간막 허혈 — SMA 색전. 심방세동(비항응고)에서 좌심방 혈전이 SMA(대개 middle colic 분지 직후)로 색전. 특징: 진찰 소견에 비해 과도한 통증(pain out of proportion) → 늦으면 혈변·복막염·젖산성 산증(장괴사 신호)."
   },
   {
    "k": "정답근거",
    "v": "장 생존이 시간에 달려 있어 즉시 혈관재개통(외과적 색전제거 또는 endovascular) + heparin 항응고 + 괴사 부위 절제. 지연 = 사망."
   },
   {
    "k": "오답감별",
    "v": "(B) 게실염은 좌하복부·발열·국소압통. (C) 만성 장간막 허혈은 식후 복통·체중감소(intestinal angina)로 경과가 다름. (D) IBS는 급성 복증·젖산 산증과 무관. (E) 허혈성 대장염(분수계, IMA 영역, 고령·저혈압 후)은 대개 보존적이지만, 본 증례는 SMA 급성 색전으로 외과적 응급."
   },
   {
    "k": "임상핵심",
    "v": "\"AF + pain out of proportion + lactate↑ → 급성 SMA 허혈, 응급 재개통.\" 정상 젖산·연성 복부라도 배제 못 함(초기엔 정상일 수 있음)."
   },
   {
    "k": "출처",
    "v": "Sabiston/Schwartz Surgery; ACG/SVS guidance."
   }
  ],
  "source": "USMLE-style / MedKOS (acute abdomen)",
  "vitals": [],
  "labs": [],
  "appendix": null,
  "figureSvg": ""
 },
 {
  "id": "usmle-2026-0014",
  "exam": "usmle",
  "step": "Step 2",
  "subject": "Neurology",
  "subject_file": "Neurology",
  "subtopic": "Acute Ischemic Stroke (Thrombolysis)",
  "type": "Acute Ischemic Stroke (Thrombolysis)",
  "difficulty": 4,
  "created": "2026-07-02",
  "vignette": "A 68-year-old man has sudden left hemiparesis, facial droop, and aphasia that began 2 hours ago. Blood pressure is 170/95 mmHg, fingerstick glucose is normal, and he takes no anticoagulants and has had no recent surgery or bleeding. Noncontrast head CT shows no hemorrhage and no large established infarct.",
  "question": "Which of the following is the most appropriate next step?",
  "options": [
   "Administer intravenous alteplase now, as he is within the 4.5-hour window with no hemorrhage and no contraindication",
   "Give aspirin 325 mg and admit, without thrombolysis",
   "Rapidly lower blood pressure to below 120/80 before any therapy",
   "Start full-dose intravenous heparin",
   "Withhold all treatment until MRI is obtained"
  ],
  "answer": 1,
  "explanationText": "- 정답근거: 발병 2시간(≤4.5시간), CT 출혈 없음, 출혈/수술 등 금기\n  없음, 혈압 170/95 < 185/110(tPA 투여 임계) → 정맥 alteplase(tPA) 적응증.\n  시간이 뇌(time is brain)이므로 지체 없이 투여.\n- 오답감별:\n  - (B) tPA 적격자에게 aspirin으로 대체하면 안 됨(항혈소판은 tPA 후 24시간 뒤).\n  - (C) 급성기 permissive hypertension — tPA 줄 때만 <185/110로 조절하고,\n    tPA 안 주면 대개 <220/120까지 허용. <120/80로 급강하하면 penumbra 관류 악화.\n  - (D) 급성 허혈성 뇌졸중에 즉시 전량 헤파린은 이득 없고 출혈 위험.\n  - (E) tPA를 늦추려 MRI를 기다리는 것은 부적절(비조영 CT로 출혈만 배제되면 투여).\n- 임상핵심: \"≤4.5h + 출혈 없음 + 금기 없음 + BP<185/110 → IV tPA.\" 대혈관\n  폐색(LVO)은 선별 기준 충족 시 기계적 혈전제거술을 최대 24시간까지 고려.\n- 출처: AHA/ASA Guidelines for Early Management of Acute Ischemic Stroke.",
  "explanationItems": [
   {
    "k": "정답근거",
    "v": "발병 2시간(≤4.5시간), CT 출혈 없음, 출혈/수술 등 금기 없음, 혈압 170/95 < 185/110(tPA 투여 임계) → 정맥 alteplase(tPA) 적응증. 시간이 뇌(time is brain)이므로 지체 없이 투여."
   },
   {
    "k": "오답감별",
    "v": "(B) tPA 적격자에게 aspirin으로 대체하면 안 됨(항혈소판은 tPA 후 24시간 뒤).\n(C) 급성기 permissive hypertension — tPA 줄 때만 <185/110로 조절하고, tPA 안 주면 대개 <220/120까지 허용. <120/80로 급강하하면 penumbra 관류 악화.\n(D) 급성 허혈성 뇌졸중에 즉시 전량 헤파린은 이득 없고 출혈 위험.\n(E) tPA를 늦추려 MRI를 기다리는 것은 부적절(비조영 CT로 출혈만 배제되면 투여)."
   },
   {
    "k": "임상핵심",
    "v": "\"≤4.5h + 출혈 없음 + 금기 없음 + BP<185/110 → IV tPA.\" 대혈관 폐색(LVO)은 선별 기준 충족 시 기계적 혈전제거술을 최대 24시간까지 고려."
   },
   {
    "k": "출처",
    "v": "AHA/ASA Guidelines for Early Management of Acute Ischemic Stroke."
   }
  ],
  "source": "USMLE-style / MedKOS (AHA/ASA acute stroke guideline)",
  "vitals": [],
  "labs": [],
  "appendix": null,
  "figureSvg": ""
 },
 {
  "id": "usmle-2026-0015",
  "exam": "usmle",
  "step": "Step 2",
  "subject": "Pediatrics",
  "subject_file": "Pediatrics",
  "subtopic": "Ductal-Dependent Cyanotic CHD",
  "type": "Ductal-Dependent Cyanotic CHD",
  "difficulty": 4,
  "created": "2026-07-02",
  "vignette": "A term neonate becomes profoundly cyanotic on the second day of life. The cyanosis does not improve with 100% oxygen (a failed hyperoxia test), the second heart sound is single, and a chest radiograph shows an 'egg-on-a-string' cardiac silhouette. The infant deteriorates as the ductus arteriosus begins to close.",
  "question": "Which of the following is the most appropriate immediate intervention?",
  "options": [
   "Start a prostaglandin E1 infusion to maintain ductal patency",
   "Give indomethacin to close the ductus arteriosus",
   "Provide high-flow oxygen alone, which is sufficient",
   "Begin aggressive diuresis",
   "Start a beta-blocker"
  ],
  "answer": 1,
  "explanationText": "- 진단: 관상동맥관 의존성 청색성 선천심질환 — 여기선 대혈관전위(TGA)\n  (egg-on-a-string, 단일 S2). hyperoxia test 실패(100% 산소로도 PaO2가 크게\n  오르지 않음)가 폐질환과의 감별 단서.\n- 정답근거: TGA·폐동맥폐쇄·중증 대동맥축착·좌심형성부전 등은 동맥관(PDA)을\n  통한 혼합/전신·폐혈류에 의존한다. 동맥관이 닫히면 급격히 악화 → prostaglandin\n  E1(alprostadil) 지속주입으로 동맥관을 열어 유지하는 것이 응급 처치(무호흡\n  부작용 주의). 이후 근본 교정(예: arterial switch).\n- 오답감별: (B) indomethacin은 동맥관을 닫는다 — 미숙아 PDA 치료용으로,\n  여기서는 치명적. (C) 관상동맥관 의존 병변은 산소만으로 해결 안 됨(오히려 산소가\n  동맥관 수축 유발 가능). (D)(E) 병태생리와 무관.\n- 임상핵심: \"산소 무반응 신생아 청색증 → 관상동맥관 의존 CHD, PGE1로 동맥관\n  유지.\" PDA 유지 = PGE1, PDA 폐쇄 = indomethacin/ibuprofen(반대 개념).\n- 출처: Nelson Textbook of Pediatrics; neonatal cardiology.",
  "explanationItems": [
   {
    "k": "진단",
    "v": "관상동맥관 의존성 청색성 선천심질환 — 여기선 대혈관전위(TGA) (egg-on-a-string, 단일 S2). hyperoxia test 실패(100% 산소로도 PaO2가 크게 오르지 않음)가 폐질환과의 감별 단서."
   },
   {
    "k": "정답근거",
    "v": "TGA·폐동맥폐쇄·중증 대동맥축착·좌심형성부전 등은 동맥관(PDA)을 통한 혼합/전신·폐혈류에 의존한다. 동맥관이 닫히면 급격히 악화 → prostaglandin E1(alprostadil) 지속주입으로 동맥관을 열어 유지하는 것이 응급 처치(무호흡 부작용 주의). 이후 근본 교정(예: arterial switch)."
   },
   {
    "k": "오답감별",
    "v": "(B) indomethacin은 동맥관을 닫는다 — 미숙아 PDA 치료용으로, 여기서는 치명적. (C) 관상동맥관 의존 병변은 산소만으로 해결 안 됨(오히려 산소가 동맥관 수축 유발 가능). (D)(E) 병태생리와 무관."
   },
   {
    "k": "임상핵심",
    "v": "\"산소 무반응 신생아 청색증 → 관상동맥관 의존 CHD, PGE1로 동맥관 유지.\" PDA 유지 = PGE1, PDA 폐쇄 = indomethacin/ibuprofen(반대 개념)."
   },
   {
    "k": "출처",
    "v": "Nelson Textbook of Pediatrics; neonatal cardiology."
   }
  ],
  "source": "USMLE-style / MedKOS (neonatal cardiology)",
  "vitals": [],
  "labs": [],
  "appendix": null,
  "figureSvg": ""
 },
 {
  "id": "usmle-2026-0016",
  "exam": "usmle",
  "step": "Step 2",
  "subject": "Pediatrics",
  "subject_file": "Pediatrics",
  "subtopic": "Hypertrophic Pyloric Stenosis",
  "type": "Hypertrophic Pyloric Stenosis",
  "difficulty": 4,
  "created": "2026-07-02",
  "vignette": "A 4-week-old firstborn boy has 1 week of progressive nonbilious projectile vomiting and remains hungry after emesis. Examination reveals visible gastric peristalsis and a firm 'olive-like' mass in the epigastrium. Laboratory studies show a hypochloremic, hypokalemic metabolic alkalosis with paradoxically acidic urine; ultrasound confirms a thickened, elongated pylorus.",
  "question": "Which of the following is the most appropriate next step?",
  "options": [
   "Correct the fluid and electrolyte abnormalities with IV normal saline plus potassium, then perform pyloromyotomy",
   "Proceed to emergent pyloromyotomy before fluid resuscitation",
   "Start a prokinetic agent and discharge home",
   "Obtain a barium enema",
   "Begin broad-spectrum intravenous antibiotics"
  ],
  "answer": 1,
  "explanationText": "- 진단: 비후성 유문협착(hypertrophic pyloric stenosis) — 생후 3~6주 남아,\n  비담즙성 사출성 구토, 수유 후에도 배고파함, 올리브 종괴, 초음파에서\n  유문 비후.\n- 정답근거(산-염기 기전): 위산(HCl) 소실 → 저염소·저칼륨 대사성\n  알칼리증. 신장은 혈장량 유지를 위해 Na⁺을 재흡수하며 H⁺을 배설(그리고\n  저칼륨혈증이 H⁺ 배설을 촉진) → 역설적 산성뇨(paradoxical aciduria).\n  유문협착은 내과적 응급이 아니라 대사 이상이 문제이므로 먼저 생리식염수 +\n  KCl로 교정(소변량 회복 후 K 보충) → 안정되면 Ramstedt 유문근절개술.\n- 오답감별: (B) 알칼리증·저칼륨 상태에서 마취/수술은 무호흡·부정맥 위험 →\n  반드시 교정 선행. (C) 자연 호전 안 됨. (D) 담즙성 구토(장폐색/malrotation) 감별\n  시 상부위장관 조영이지 barium enema 아님. (E) 감염질환 아님.\n- 임상핵심: \"유문협착 = 저Cl·저K 대사성 알칼리증 + 역설적 산성뇨. 수액 교정\n  먼저, 수술은 그다음.\" 담즙성 구토면 유문협착이 아니라 malrotation/volvulus를\n  먼저 배제.\n- 출처: Nelson Textbook of Pediatrics; pediatric surgery references.",
  "explanationItems": [
   {
    "k": "진단",
    "v": "비후성 유문협착(hypertrophic pyloric stenosis) — 생후 3~6주 남아, *비담즙성 사출성 구토, 수유 후에도 배고파함, 올리브 종괴, 초음파에서 유문 비후."
   },
   {
    "k": "정답근거(산-염기 기전)",
    "v": "위산(HCl) 소실 → 저염소·저칼륨 대사성 알칼리증. 신장은 혈장량 유지를 위해 Na⁺을 재흡수하며 H⁺을 배설(그리고 저칼륨혈증이 H⁺ 배설을 촉진) → 역설적 산성뇨(paradoxical aciduria). 유문협착은 내과적 응급이 아니라 대사 이상이 문제이므로 먼저 생리식염수 + KCl로 교정(소변량 회복 후 K 보충) → 안정되면 Ramstedt 유문근절개술."
   },
   {
    "k": "오답감별",
    "v": "(B) 알칼리증·저칼륨 상태에서 마취/수술은 무호흡·부정맥 위험 → 반드시 교정 선행. (C) 자연 호전 안 됨. (D) 담즙성 구토(장폐색/malrotation) 감별 시 상부위장관 조영이지 barium enema 아님. (E) 감염질환 아님."
   },
   {
    "k": "임상핵심",
    "v": "\"유문협착 = 저Cl·저K 대사성 알칼리증 + 역설적 산성뇨. 수액 교정 먼저, 수술은 그다음.\" 담즙성 구토면 유문협착이 아니라 malrotation/volvulus를 먼저 배제."
   },
   {
    "k": "출처",
    "v": "Nelson Textbook of Pediatrics; pediatric surgery references."
   }
  ],
  "source": "USMLE-style / MedKOS (pediatric surgery)",
  "vitals": [],
  "labs": [],
  "appendix": null,
  "figureSvg": ""
 },
 {
  "id": "usmle-2026-0017",
  "exam": "usmle",
  "step": "Step 1",
  "subject": "Pathology",
  "subject_file": "Pathology",
  "subtopic": "Retinoblastoma (Two-Hit Hypothesis)",
  "type": "Retinoblastoma (Two-Hit Hypothesis)",
  "difficulty": 4,
  "created": "2026-07-02",
  "vignette": "A 14-month-old girl is found to have bilateral retinoblastomas, and her father was treated for a similar eye tumor in childhood. Genetic testing shows a germline loss-of-function mutation in one RB1 allele.",
  "question": "Which additional event is required within a retinal cell for a tumor to develop, and what is the mechanism?",
  "options": [
   "Somatic inactivation of the second RB1 allele, because RB1 is a tumor suppressor requiring loss of both copies (Knudson two-hit)",
   "A single activating point mutation in RB1, because RB1 is a proto-oncogene",
   "Amplification of RB1 leading to overexpression",
   "A gain-of-function mutation that constitutively activates RB1",
   "Methylation that increases RB1 transcription"
  ],
  "answer": 1,
  "explanationText": "- 개념: RB1은 종양억제유전자 — Knudson two-hit 가설을 따른다. 종양이\n  생기려면 두 대립유전자가 모두 불활성화되어야 한다.\n- 정답근거(유전성): 유전성(양측성) 망막모세포종은 생식세포에 first hit(한쪽\n  결손)을 이미 갖고 태어나, 망막세포에서 second hit(체세포 변이·LOH)만 추가되면\n  발병 → 양측성·조기·다발성, 그리고 나중에 골육종 위험 증가. 산발성(단측성)은\n  한 세포에서 두 hit가 모두 체세포로 일어나야 해 드물고 늦다.\n- 기전: pRB는 저인산화 상태에서 E2F를 억제해 G1→S 진행을 막는다. 소실되면\n  E2F가 풀려 세포주기가 통제 없이 진행.\n- 오답감별: (B)(D) proto-oncogene/gain-of-function은 종양유전자(예: RAS, MYC)의\n  기전 — RB1과 반대. (C) 증폭·과발현은 oncogene 활성화 방식. (E) 전사 증가는 억제\n  유전자 소실과 반대.\n- 임상핵심: \"종양억제유전자 = two-hit(둘 다 잃어야). 유전성은 first hit를 물려\n  받아 조기·양측성.\" Rb·p53·APC·VHL·NF1/2·BRCA가 대표.\n- 출처: Robbins Pathologic Basis of Disease; Knudson.",
  "explanationItems": [
   {
    "k": "개념",
    "v": "RB1은 종양억제유전자 — Knudson two-hit 가설을 따른다. 종양이 생기려면 두 대립유전자가 모두 불활성화되어야 한다."
   },
   {
    "k": "정답근거(유전성)",
    "v": "유전성(양측성) 망막모세포종은 생식세포에 first hit(한쪽 결손)을 이미 갖고 태어나, 망막세포에서 second hit(체세포 변이·LOH)만 추가되면 발병 → 양측성·조기·다발성, 그리고 나중에 골육종 위험 증가. 산발성(단측성)은 한 세포에서 두 hit가 모두 체세포로 일어나야 해 드물고 늦다."
   },
   {
    "k": "기전",
    "v": "pRB는 저인산화 상태에서 E2F를 억제해 G1→S 진행을 막는다. 소실되면 E2F가 풀려 세포주기가 통제 없이 진행."
   },
   {
    "k": "오답감별",
    "v": "(B)(D) proto-oncogene/gain-of-function은 종양유전자(예: RAS, MYC)의 기전 — RB1과 반대. (C) 증폭·과발현은 oncogene 활성화 방식. (E) 전사 증가는 억제 유전자 소실과 반대."
   },
   {
    "k": "임상핵심",
    "v": "\"종양억제유전자 = two-hit(둘 다 잃어야). 유전성은 first hit를 물려 받아 조기·양측성.\" Rb·p53·APC·VHL·NF1/2·BRCA가 대표."
   },
   {
    "k": "출처",
    "v": "Robbins Pathologic Basis of Disease; Knudson."
   }
  ],
  "source": "USMLE-style / MedKOS (neoplasia, tumor suppressors)",
  "vitals": [],
  "labs": [],
  "appendix": null,
  "figureSvg": ""
 },
 {
  "id": "usmle-2026-0018",
  "exam": "usmle",
  "step": "Step 1",
  "subject": "Pathology",
  "subject_file": "Pathology",
  "subtopic": "Amyloidosis",
  "type": "Amyloidosis",
  "difficulty": 4,
  "created": "2026-07-02",
  "vignette": "A 63-year-old man has nephrotic-range proteinuria, hepatomegaly, macroglossia, and echocardiographic findings of a restrictive cardiomyopathy with low-voltage QRS. A fat-pad biopsy stained with Congo red shows deposits that display apple-green birefringence under polarized light. Serum and urine studies reveal a monoclonal lambda light chain.",
  "question": "Which protein most likely composes the deposits?",
  "options": [
   "Immunoglobulin light chains (AL amyloid)",
   "Serum amyloid A protein (AA amyloid)",
   "Transthyretin (ATTR)",
   "Beta-2 microglobulin",
   "Beta-amyloid (A-beta)"
  ],
  "answer": 1,
  "explanationText": "- 진단: AL 아밀로이드증(원발성). Congo red에서 편광하 사과녹색 복굴절은\n  아밀로이드의 공통 소견(β-병풍 구조), 단클론 경쇄(λ)가 원인 단백을 특정한다.\n- 정답근거: AL은 형질세포 클론(다발골수종·MGUS)이 만든 면역글로불린\n  경쇄가 침착. 임상: 거대혀(macroglossia), 제한성 심근병증(저전압 QRS),\n  신증후군, 간비대, 손목터널 — 다장기 침착.\n- 오답감별: (B) AA는 만성 염증(류마티스관절염·만성감염·가족성지중해열)의\n  serum amyloid A 유래. (C) ATTR는 transthyretin(노인성 심장/유전성 신경).\n  (D) β2-microglobulin은 장기 투석 관련(손목터널). (E) Aβ는 알츠하이머·뇌\n  아밀로이드혈관병.\n- 임상핵심: \"사과녹색 복굴절 = 아밀로이드. 경쇄면 AL(형질세포), SAA면 AA(만성\n  염증).\" 조직형 확인이 치료를 좌우.\n- 출처: Robbins Pathologic Basis of Disease.",
  "explanationItems": [
   {
    "k": "진단",
    "v": "AL 아밀로이드증(원발성). Congo red에서 편광하 사과녹색 복굴절은 아밀로이드의 공통 소견(β-병풍 구조), 단클론 경쇄(λ)가 원인 단백을 특정한다."
   },
   {
    "k": "정답근거",
    "v": "AL은 형질세포 클론(다발골수종·MGUS)이 만든 면역글로불린 경쇄가 침착. 임상: 거대혀(macroglossia), 제한성 심근병증(저전압 QRS), 신증후군, 간비대, 손목터널 — 다장기 침착."
   },
   {
    "k": "오답감별",
    "v": "(B) AA는 만성 염증(류마티스관절염·만성감염·가족성지중해열)의 *serum amyloid A 유래. (C) ATTR는 transthyretin(노인성 심장/유전성 신경).\n(D) β2-microglobulin은 장기 투석 관련(손목터널). (E) Aβ는 알츠하이머·뇌 아밀로이드혈관병."
   },
   {
    "k": "임상핵심",
    "v": "\"사과녹색 복굴절 = 아밀로이드. 경쇄면 AL(형질세포), SAA면 AA(만성 염증).\" 조직형 확인이 치료를 좌우."
   },
   {
    "k": "출처",
    "v": "Robbins Pathologic Basis of Disease."
   }
  ],
  "source": "USMLE-style / MedKOS (deposition diseases)",
  "vitals": [],
  "labs": [],
  "appendix": null,
  "figureSvg": ""
 },
 {
  "id": "usmle-2026-0019",
  "exam": "usmle",
  "step": "Step 1",
  "subject": "Physiology",
  "subject_file": "Physiology",
  "subtopic": "Hypoxemia (A-a Gradient)",
  "type": "Hypoxemia (A-a Gradient)",
  "difficulty": 5,
  "created": "2026-07-02",
  "vignette": "A 40-year-old man with lobar pneumonia is hypoxemic. On 100% inspired oxygen his PaO2 rises only minimally, and the calculated alveolar-arterial (A-a) oxygen gradient is markedly elevated.",
  "question": "Which mechanism of hypoxemia does this pattern most specifically indicate?",
  "options": [
   "Right-to-left shunt (perfusion of non-ventilated alveoli), which does not correct with 100% oxygen",
   "Hypoventilation, which has a normal A-a gradient",
   "Low inspired oxygen (high altitude), with a normal A-a gradient",
   "Ventilation-perfusion mismatch that fully corrects with 100% oxygen and has a normal A-a gradient",
   "Impaired diffusion with a normal A-a gradient"
  ],
  "answer": 1,
  "explanationText": "- 정답근거: 우-좌 션트의 특징은 ① A-a 차이 증가, ② 100% 산소에 반응\n  없음(교정 안 됨). 폐렴에서 폐포가 액체로 차 환기되지 않는 폐포를 혈류가 통과\n  (shunt) → 그 혈액은 산소에 노출되지 않으므로 흡입 산소를 올려도 개선이 미미하다.\n- 오답감별(저산소증 5기전 감별):\n  - (B) 저환기: A-a 정상, PaCO2 상승, 산소에 잘 반응.\n  - (C) 저흡입산소(고지대): A-a 정상, 산소로 교정.\n  - (D) V/Q 부조화: A-a 증가하지만 100% 산소에 대체로 교정(저 V/Q 폐포도\n    결국 산소 도달) — 션트와의 핵심 감별점.\n  - (E) 확산장애: A-a 증가하나 보충 산소에 반응(운동 시 악화).\n- 임상핵심: \"A-a↑ + 100% O2 무반응 = 션트.\" A-a↑ + 산소반응 = V/Q/확산.\n  A-a 정상 = 저환기 또는 저흡입산소.\n- 출처: West Respiratory Physiology; Guyton & Hall.",
  "explanationItems": [
   {
    "k": "정답근거",
    "v": "우-좌 션트의 특징은 ① A-a 차이 증가, ② 100% 산소에 반응 없음(교정 안 됨). 폐렴에서 폐포가 액체로 차 환기되지 않는 폐포를 혈류가 통과 (shunt) → 그 혈액은 산소에 노출되지 않으므로 흡입 산소를 올려도 개선이 미미하다."
   },
   {
    "k": "오답감별(저산소증 5기전 감별)",
    "v": "(B) 저환기: A-a 정상, PaCO2 상승, 산소에 잘 반응.\n(C) 저흡입산소(고지대): A-a 정상, 산소로 교정.\n(D) V/Q 부조화: A-a 증가하지만 100% 산소에 대체로 교정(저 V/Q 폐포도 결국 산소 도달) — 션트와의 핵심 감별점.\n(E) 확산장애: A-a 증가하나 보충 산소에 반응(운동 시 악화)."
   },
   {
    "k": "임상핵심",
    "v": "\"A-a↑ + 100% O2 무반응 = 션트.\" A-a↑ + 산소반응 = V/Q/확산. A-a 정상 = 저환기 또는 저흡입산소."
   },
   {
    "k": "출처",
    "v": "West Respiratory Physiology; Guyton & Hall."
   }
  ],
  "source": "USMLE-style / MedKOS (respiratory physiology)",
  "vitals": [],
  "labs": [],
  "appendix": null,
  "figureSvg": ""
 },
 {
  "id": "usmle-2026-0020",
  "exam": "usmle",
  "step": "Step 1",
  "subject": "Physiology",
  "subject_file": "Physiology",
  "subtopic": "Polyuria (SIADH vs Diabetes Insipidus)",
  "type": "Polyuria (SIADH vs Diabetes Insipidus)",
  "difficulty": 4,
  "created": "2026-07-02",
  "vignette": "A 35-year-old man has polyuria and polydipsia. A water-deprivation test fails to concentrate his urine (urine osmolality remains low despite rising serum osmolality). After administration of desmopressin (a vasopressin analog), his urine osmolality rises by more than 50%.",
  "question": "Which mechanism best explains his condition?",
  "options": [
   "Deficient ADH secretion from the posterior pituitary (central diabetes insipidus)",
   "Renal collecting-duct resistance to ADH (nephrogenic diabetes insipidus)",
   "Excess ADH secretion (SIADH)",
   "Primary polydipsia with normal ADH axis",
   "Osmotic diuresis from glucosuria"
  ],
  "answer": 1,
  "explanationText": "- 정답근거: 중추성 요붕증. 수분제한에도 소변을 농축 못 하지만(내인성 ADH\n  부족), 외인성 desmopressin에는 반응(소변 삼투압 >50% 증가)한다 — 신장의\n  V2 수용체·aquaporin-2 경로는 정상이기 때문.\n- 오답감별:\n  - (B) 신성 요붕증: 신장이 ADH에 저항 → desmopressin에도 반응 없음(핵심\n    감별점). 원인: lithium, 고칼슘혈증, 유전성 V2/AQP2.\n  - (C) SIADH: ADH 과다 → 농축뇨·저나트륨혈증, 다뇨가 아니라 수분저류.\n  - (D) 원발성 다음증: 수분제한만으로도 어느 정도 농축(기저 ADH 억제 상태),\n    desmopressin에 과반응 안 함.\n  - (E) 삼투성 이뇨(고혈당): 소변 삼투압이 낮지 않고 포도당 존재.\n- 임상핵심: \"수분제한 후 desmopressin 반응 O = 중추성, 반응 X = 신성.\" 중추성\n  치료는 desmopressin, 신성은 유발인자 제거 + thiazide/저염식.\n- 출처: Guyton & Hall Physiology; endocrinology references.",
  "explanationItems": [
   {
    "k": "정답근거",
    "v": "중추성 요붕증. 수분제한에도 소변을 농축 못 하지만(내인성 ADH 부족), 외인성 desmopressin에는 반응(소변 삼투압 >50% 증가)한다 — 신장의 V2 수용체·aquaporin-2 경로는 정상이기 때문."
   },
   {
    "k": "오답감별",
    "v": "(B) 신성 요붕증: 신장이 ADH에 저항 → desmopressin에도 반응 없음(핵심 감별점). 원인: lithium, 고칼슘혈증, 유전성 V2/AQP2.\n(C) SIADH: ADH 과다 → 농축뇨·저나트륨혈증, 다뇨가 아니라 수분저류.\n(D) 원발성 다음증: 수분제한만으로도 어느 정도 농축(기저 ADH 억제 상태), desmopressin에 과반응 안 함.\n(E) 삼투성 이뇨(고혈당): 소변 삼투압이 낮지 않고 포도당 존재."
   },
   {
    "k": "임상핵심",
    "v": "\"수분제한 후 desmopressin 반응 O = 중추성, 반응 X = 신성.\" 중추성 치료는 desmopressin, 신성은 유발인자 제거 + thiazide/저염식."
   },
   {
    "k": "출처",
    "v": "Guyton & Hall Physiology; endocrinology references."
   }
  ],
  "source": "USMLE-style / MedKOS (renal/endocrine physiology)",
  "vitals": [],
  "labs": [],
  "appendix": null,
  "figureSvg": ""
 },
 {
  "id": "usmle-2026-0021",
  "exam": "usmle",
  "step": "Step 2",
  "subject": "Obstetrics & Gynecology",
  "subject_file": "Obstetrics & Gynecology",
  "subtopic": "Preeclampsia with Severe Features",
  "type": "Preeclampsia with Severe Features",
  "difficulty": 4,
  "created": "2026-07-02",
  "vignette": "A 29-year-old woman at 34 weeks gestation presents with blood pressure 168/112 mmHg on two readings, a severe headache with visual scotomata, and 3+ proteinuria. Deep tendon reflexes are brisk.",
  "question": "Which of the following is the most appropriate immediate pharmacologic management to prevent the major acute neurologic complication?",
  "options": [
   "Intravenous magnesium sulfate for seizure prophylaxis, plus antihypertensive therapy, with planning for delivery",
   "Phenytoin loading as first-line seizure prophylaxis",
   "Immediate diuresis with furosemide to lower blood pressure",
   "Expectant outpatient management with bed rest until term",
   "Low-dose aspirin to treat the acute episode"
  ],
  "answer": 1,
  "explanationText": "- 진단: 중증 특징 동반 자간전증(BP ≥160/110, 신경학적 증상, 단백뇨). 막아야\n  할 급성 합병증은 자간증(eclamptic seizure).\n- 정답근거: 정맥 황산마그네슘(MgSO4)이 경련 예방·치료의 1차. 동시에\n  항고혈압제(labetalol·hydralazine·경구 nifedipine)로 중증 고혈압을 조절하고,\n  근치는 분만(≥34주 중증이면 분만).\n- 오답감별: (B) phenytoin은 MgSO4보다 열등(MgSO4가 표준). (C) 이뇨제는\n  자간전증의 혈관내 용적 감소를 악화시켜 1차 아님. (D) 중증은 기대요법·외래 관찰\n  대상이 아니다. (E) 아스피린은 예방(고위험군에서 조기 시작)이지 급성 치료가\n  아님.\n- 임상핵심: MgSO4 투여 중 독성 감시(심부건반사 소실 → 호흡억제 → 심정지\n  순), 해독제 calcium gluconate. 신부전 시 용량 감량.\n- 출처: ACOG — Gestational Hypertension and Preeclampsia.",
  "explanationItems": [
   {
    "k": "진단",
    "v": "중증 특징 동반 자간전증(BP ≥160/110, 신경학적 증상, 단백뇨). 막아야 할 급성 합병증은 자간증(eclamptic seizure)."
   },
   {
    "k": "정답근거",
    "v": "정맥 황산마그네슘(MgSO4)이 경련 예방·치료의 1차. 동시에 *항고혈압제(labetalol·hydralazine·경구 nifedipine)로 중증 고혈압을 조절하고, 근치는 분만(≥34주 중증이면 분만)."
   },
   {
    "k": "오답감별",
    "v": "(B) phenytoin은 MgSO4보다 열등(MgSO4가 표준). (C) 이뇨제는 자간전증의 혈관내 용적 감소를 악화시켜 1차 아님. (D) 중증은 기대요법·외래 관찰 대상이 아니다. (E) 아스피린은 예방(고위험군에서 조기 시작)이지 급성 치료가 아님."
   },
   {
    "k": "임상핵심",
    "v": "MgSO4 투여 중 독성 감시(심부건반사 소실 → 호흡억제 → 심정지 순), 해독제 calcium gluconate. 신부전 시 용량 감량."
   },
   {
    "k": "출처",
    "v": "ACOG — Gestational Hypertension and Preeclampsia."
   }
  ],
  "source": "USMLE-style / MedKOS (ACOG hypertension in pregnancy)",
  "vitals": [],
  "labs": [],
  "appendix": null,
  "figureSvg": ""
 },
 {
  "id": "usmle-2026-0022",
  "exam": "usmle",
  "step": "Step 2",
  "subject": "Obstetrics & Gynecology",
  "subject_file": "Obstetrics & Gynecology",
  "subtopic": "Ectopic Pregnancy",
  "type": "Ectopic Pregnancy",
  "difficulty": 4,
  "created": "2026-07-02",
  "vignette": "A 26-year-old woman with a prior chlamydial pelvic infection presents at 6 weeks by dates with mild left lower-quadrant pain and minimal vaginal spotting. She is hemodynamically stable. Serum beta-hCG is 1,800 mIU/mL; transvaginal ultrasound shows no intrauterine gestational sac but a small 2-cm adnexal mass without free fluid.",
  "question": "Which of the following is the most appropriate management?",
  "options": [
   "Medical therapy with intramuscular methotrexate, since she is stable with a small unruptured ectopic and no contraindications",
   "Immediate exploratory laparotomy",
   "Reassurance and repeat testing in 4 weeks with no intervention",
   "Dilation and curettage to remove the pregnancy",
   "High-dose oxytocin infusion"
  ],
  "answer": 1,
  "explanationText": "- 진단: 자궁외임신(난관). 위험인자(과거 클라미디아 PID), β-hCG 1,800\n  인데도 자궁내 임신낭 없음(판별역치 ~1,500–2,000 초과에서 자궁내 낭이 보여야\n  정상) + 부속기 종괴 → 자궁외임신.\n- 정답근거: 혈역학적 안정 + 미파열 + 작은 종괴(<3.5cm) + 심박동 없음 + 금기\n  없음이면 근주 methotrexate(엽산길항 → 영양막 증식 억제)로 내과 치료. 이후\n  β-hCG 추적(4·7일).\n- 오답감별: (B) 개복술은 불안정/파열/자궁외파열 징후일 때. (C) 방치는 파열\n  위험으로 부적절. (D) D&C는 자궁내 임신을 다루는 술기(자궁외에는 부적절). (E)\n  oxytocin은 무관.\n- 임상핵심: MTX 금기(간·신장애, 혈액이상, 모유수유, 활동성 폐질환, 큰 종괴·\n  심박동·높은 β-hCG, 순응도 불량)면 수술. 불안정하면 즉시 수술.\n- 출처: ACOG — Tubal Ectopic Pregnancy.",
  "explanationItems": [
   {
    "k": "진단",
    "v": "자궁외임신(난관). 위험인자(과거 클라미디아 PID), β-hCG 1,800 인데도 자궁내 임신낭 없음(판별역치 ~1,500–2,000 초과에서 자궁내 낭이 보여야 정상) + 부속기 종괴 → 자궁외임신."
   },
   {
    "k": "정답근거",
    "v": "혈역학적 안정 + 미파열 + 작은 종괴(<3.5cm) + 심박동 없음 + 금기 없음이면 근주 methotrexate(엽산길항 → 영양막 증식 억제)로 내과 치료. 이후 β-hCG 추적(4·7일)."
   },
   {
    "k": "오답감별",
    "v": "(B) 개복술은 불안정/파열/자궁외파열 징후일 때. (C) 방치는 파열 위험으로 부적절. (D) D&C는 자궁내 임신을 다루는 술기(자궁외에는 부적절). (E) oxytocin은 무관."
   },
   {
    "k": "임상핵심",
    "v": "MTX 금기(간·신장애, 혈액이상, 모유수유, 활동성 폐질환, 큰 종괴· 심박동·높은 β-hCG, 순응도 불량)면 수술. 불안정하면 즉시 수술."
   },
   {
    "k": "출처",
    "v": "ACOG — Tubal Ectopic Pregnancy."
   }
  ],
  "source": "USMLE-style / MedKOS (early pregnancy complications)",
  "vitals": [],
  "labs": [],
  "appendix": null,
  "figureSvg": ""
 },
 {
  "id": "usmle-2026-0023",
  "exam": "usmle",
  "step": "Step 2",
  "subject": "Psychiatry",
  "subject_file": "Psychiatry",
  "subtopic": "Serotonin Syndrome",
  "type": "Serotonin Syndrome",
  "difficulty": 5,
  "created": "2026-07-02",
  "vignette": "A 24-year-old man on fluoxetine is given tramadol for back pain. Within hours he becomes agitated and diaphoretic with a temperature of 39.4 C, tachycardia, dilated pupils, and prominent lower-extremity clonus with hyperreflexia.",
  "question": "Which diagnosis best fits, and what neuromuscular finding most distinguishes it from its main mimic?",
  "options": [
   "Serotonin syndrome, distinguished by hyperreflexia and clonus (rapid onset after a serotonergic drug)",
   "Neuroleptic malignant syndrome, distinguished by hyperreflexia and clonus",
   "Malignant hyperthermia from an inhaled anesthetic",
   "Anticholinergic toxicity, distinguished by clonus",
   "Thyroid storm, distinguished by lead-pipe rigidity"
  ],
  "answer": 1,
  "explanationText": "- 진단: 세로토닌 증후군. 두 세로토닌성 약물 병용(SSRI fluoxetine +\n  tramadol; 그 외 MAOI·linezolid·triptan·dextromethorphan·MDMA)로 수시간 내\n  급성 발병. 3징: 정신상태 변화 + 자율신경 항진 + 신경근 항진.\n- 정답근거(핵심 감별): 반사항진·간대성 경련(clonus), 특히 하지에서 두드러짐\n  → NMS와의 결정적 차이. NMS는 항정신병약(도파민 차단) 후 수일에 걸쳐 납관\n  경직(lead-pipe rigidity)·반사저하·서맥성 진행.\n- 오답감별: (B) NMS는 clonus/반사항진이 아니라 경직·반사저하. (C) 악성\n  고열은 흡입마취제/succinylcholine 후 마취 중 발생(RYR1). (D) 항콜린성은 건조한\n  피부·장음 감소(발한 없음)로 감별(세로토닌은 발한+). (E) 갑상선폭풍은 clonus/\n  경직이 특징이 아님.\n- 임상핵심: 치료 = 유발약 중단, 지지요법·냉각·벤조디아제핀, 중증엔 cyproheptadine\n  (5-HT2A 길항). NMS 치료(dantrolene·bromocriptine)와 구분.\n- 출처: DSM-5-TR 관련 임상, Hunter criteria; psychopharmacology references.",
  "explanationItems": [
   {
    "k": "진단",
    "v": "세로토닌 증후군. 두 세로토닌성 약물 병용(SSRI fluoxetine + tramadol; 그 외 MAOI·linezolid·triptan·dextromethorphan·MDMA)로 수시간 내 급성 발병. 3징: 정신상태 변화 + 자율신경 항진 + 신경근 항진."
   },
   {
    "k": "정답근거(핵심 감별)",
    "v": "반사항진·간대성 경련(clonus), 특히 하지에서 두드러짐 → NMS와의 결정적 차이. NMS는 항정신병약(도파민 차단) 후 수일에 걸쳐 납관 경직(lead-pipe rigidity)·반사저하·서맥성 진행."
   },
   {
    "k": "오답감별",
    "v": "(B) NMS는 clonus/반사항진이 아니라 경직·반사저하. (C) 악성 고열은 흡입마취제/succinylcholine 후 마취 중 발생(RYR1). (D) 항콜린성은 건조한 피부·장음 감소(발한 없음)로 감별(세로토닌은 발한+). (E) 갑상선폭풍은 clonus/ 경직이 특징이 아님."
   },
   {
    "k": "임상핵심",
    "v": "치료 = 유발약 중단, 지지요법·냉각·벤조디아제핀, 중증엔 cyproheptadine (5-HT2A 길항). NMS 치료(dantrolene·bromocriptine)와 구분."
   },
   {
    "k": "출처",
    "v": "DSM-5-TR 관련 임상, Hunter criteria; psychopharmacology references."
   }
  ],
  "source": "USMLE-style / MedKOS (psychopharmacology emergencies)",
  "vitals": [],
  "labs": [],
  "appendix": null,
  "figureSvg": ""
 },
 {
  "id": "usmle-2026-0024",
  "exam": "usmle",
  "step": "Step 2",
  "subject": "Psychiatry",
  "subject_file": "Psychiatry",
  "subtopic": "Lithium Toxicity",
  "type": "Lithium Toxicity",
  "difficulty": 4,
  "created": "2026-07-02",
  "vignette": "A 52-year-old woman with bipolar I disorder maintained on lithium develops a coarse tremor, ataxia, confusion, and vomiting one week after starting a thiazide diuretic and ibuprofen for a new diagnosis of hypertension and joint pain.",
  "question": "Which mechanism best explains her acute deterioration?",
  "options": [
   "Reduced renal lithium clearance from thiazide-induced volume depletion and NSAID effects, raising lithium to toxic levels",
   "Displacement of lithium from plasma protein binding by ibuprofen",
   "Induction of hepatic metabolism of lithium by the thiazide",
   "Thiazide-induced hyperkalemia potentiating lithium",
   "Formation of a toxic lithium metabolite by CYP3A4"
  ],
  "answer": 1,
  "explanationText": "- 정답근거(약동학): 리튬은 대사되지 않고 신장으로만 배설되며 치료지수가\n  매우 좁다. Thiazide는 용적을 줄여 근위세뇨관에서 Na⁺(과 함께 Li⁺) 재흡수\n  를 늘리고, NSAID(ibuprofen)는 신전 prostaglandin을 줄여 신혈류·GFR을 낮춘다 →\n  리튬 청소율 감소 → 농도 상승 → 독성(조대 진전·실조·혼돈·구토, 중증엔 경련·\n  신부전).\n- 오답감별: (B) 리튬은 단백결합을 하지 않는 이온이라 displacement 무관.\n  (C) 리튬은 간대사 안 됨 → 효소유도 무관. (D) 독성은 저나트륨/용적감소가 핵심\n  이지 고칼륨이 아님(thiazide는 오히려 저칼륨 경향). (E) CYP 대사 산물 없음.\n- 임상핵심: 리튬 농도를 올리는 약: thiazide, ACEi/ARB, NSAID, 탈수. 리튬\n  부작용: 신성 요붕증, 갑상선저하, 진전, 기형(Ebstein). 중증 독성은 혈액투석.\n- 출처: psychopharmacology references; clinical toxicology.",
  "explanationItems": [
   {
    "k": "정답근거(약동학)",
    "v": "리튬은 대사되지 않고 신장으로만 배설되며 치료지수가 매우 좁다. Thiazide는 용적을 줄여 근위세뇨관에서 Na⁺(과 함께 Li⁺) 재흡수 를 늘리고, NSAID(ibuprofen)는 신전 prostaglandin을 줄여 신혈류·GFR을 낮춘다 → *리튬 청소율 감소 → 농도 상승 → 독성(조대 진전·실조·혼돈·구토, 중증엔 경련· 신부전)."
   },
   {
    "k": "오답감별",
    "v": "(B) 리튬은 단백결합을 하지 않는 이온이라 displacement 무관.\n(C) 리튬은 간대사 안 됨 → 효소유도 무관. (D) 독성은 저나트륨/용적감소가 핵심 이지 고칼륨이 아님(thiazide는 오히려 저칼륨 경향). (E) CYP 대사 산물 없음."
   },
   {
    "k": "임상핵심",
    "v": "리튬 농도를 올리는 약: thiazide, ACEi/ARB, NSAID, 탈수. 리튬 부작용: 신성 요붕증, 갑상선저하, 진전, 기형(Ebstein). 중증 독성은 혈액투석."
   },
   {
    "k": "출처",
    "v": "psychopharmacology references; clinical toxicology."
   }
  ],
  "source": "USMLE-style / MedKOS (mood stabilizer safety)",
  "vitals": [],
  "labs": [],
  "appendix": null,
  "figureSvg": ""
 },
 {
  "id": "usmle-2026-0025",
  "exam": "usmle",
  "step": "Step 1",
  "subject": "Pharmacology",
  "subject_file": "Pharmacology",
  "subtopic": "Acetaminophen Toxicity (NAPQI / N-acetylcysteine)",
  "type": "Acetaminophen Toxicity (NAPQI / N-acetylcysteine)",
  "difficulty": 4,
  "created": "2026-07-07",
  "vignette": "A 19-year-old woman is brought to the emergency department 10 hours after ingesting a large number of tablets in a suicide attempt. She is nauseated but alert, with a normal examination and normal aminotransferases. A serum level of the ingested drug plots above the treatment line on the Rumack-Matthew nomogram, and the recommended antidote is started.",
  "question": "The antidote's protective effect against hepatocellular necrosis is best explained by which of the following mechanisms?",
  "options": [
   "Replenishing hepatic glutathione stores used to conjugate a reactive electrophilic metabolite",
   "Competitively inhibiting CYP2E1 so the parent drug is excreted unchanged",
   "Chelating the parent drug within the gut lumen to block absorption",
   "Inducing glucuronosyltransferase to accelerate phase II conjugation of the parent drug",
   "Acting as a receptor antagonist that reverses the drug's central effects"
  ],
  "answer": 1,
  "explanationText": "- 정답근거(대사 경로): 치료용량 acetaminophen은 대부분 glucuronidation/\n  sulfation(phase II)으로 무독화된다. 과량에서 이 경로가 포화되면 여분이\n  CYP2E1을 통해 반응성 친전자성 대사물 NAPQI로 전환된다. NAPQI는 평소\n  glutathione(GSH)과 포합돼 해독되지만, GSH가 고갈되면 간세포 단백에\n  공유결합해 중심소엽(zone 3) 괴사를 일으킨다.\n- antidote 기전: N-acetylcysteine(NAC)은 cysteine을 공급해 GSH를 재합성\n  (및 직접 NAPQI 결합)함으로써 간독성을 예방한다 → 정답 A.\n- 오답감별: (B) NAC는 CYP2E1 억제제가 아니며 모약을 미변화 배설시키지 않는다.\n  (C) 흡착·킬레이트는 activated charcoal 역할이지 NAC가 아니다. (D) UGT 유도로\n  작용하지 않는다. (E) naloxone식 수용체 길항 기전이 아니다.\n- 임상핵심: 시간축이 있어도 nomogram(4시간 이후 레벨)으로 판단하며, 초기엔\n  AST/ALT가 정상일 수 있다(괴사는 24–72시간에 최고조). NAC는 8–10시간 이내\n  투여 시 거의 완전 예방, 늦어도 투여 이득이 있다.\n- 출처: clinical toxicology; pharmacology (phase II metabolism, NAPQI–GSH).",
  "explanationItems": [
   {
    "k": "정답근거(대사 경로)",
    "v": "치료용량 acetaminophen은 대부분 glucuronidation/ sulfation(phase II)으로 무독화된다. 과량에서 이 경로가 포화되면 여분이 *CYP2E1을 통해 반응성 친전자성 대사물 NAPQI로 전환된다. NAPQI는 평소 *glutathione(GSH)과 포합돼 해독되지만, GSH가 고갈되면 간세포 단백에 공유결합해 중심소엽(zone 3) 괴사를 일으킨다."
   },
   {
    "k": "antidote 기전",
    "v": "N-acetylcysteine(NAC)은 cysteine을 공급해 GSH를 재합성 (및 직접 NAPQI 결합)함으로써 간독성을 예방한다 → 정답 A."
   },
   {
    "k": "오답감별",
    "v": "(B) NAC는 CYP2E1 억제제가 아니며 모약을 미변화 배설시키지 않는다.\n(C) 흡착·킬레이트는 activated charcoal 역할이지 NAC가 아니다. (D) UGT 유도로 작용하지 않는다. (E) naloxone식 수용체 길항 기전이 아니다."
   },
   {
    "k": "임상핵심",
    "v": "시간축이 있어도 nomogram(4시간 이후 레벨)으로 판단하며, 초기엔 *AST/ALT가 정상일 수 있다(괴사는 24–72시간에 최고조). NAC는 8–10시간 이내 투여 시 거의 완전 예방, 늦어도 투여 이득이 있다."
   },
   {
    "k": "출처",
    "v": "clinical toxicology; pharmacology (phase II metabolism, NAPQI–GSH)."
   }
  ],
  "source": "USMLE-style / MedKOS (toxicology · phase II metabolism)",
  "vitals": [],
  "labs": [],
  "appendix": null,
  "figureSvg": ""
 },
 {
  "id": "usmle-2026-0026",
  "exam": "usmle",
  "step": "Step 1",
  "subject": "Physiology",
  "subject_file": "Physiology",
  "subtopic": "Carbon Monoxide Poisoning (O2-Hb dissociation curve)",
  "type": "Carbon Monoxide Poisoning (O2-Hb dissociation curve)",
  "difficulty": 4,
  "created": "2026-07-07",
  "vignette": "A 30-year-old man is rescued from a house fire and brought in with headache, dizziness, and confusion. He is breathing spontaneously. Pulse oximetry reads 99%, and arterial blood gas shows a normal PaO2. Despite these values his tissues are hypoxic.",
  "question": "Which set of changes best explains his impaired oxygen delivery?",
  "options": [
   "Reduced dissolved PaO2 with a compensatory right shift of the oxyhemoglobin curve",
   "Increased methemoglobin with a normal oxygen-carrying capacity",
   "Reduced oxygen-carrying capacity plus a left shift of the oxyhemoglobin curve, with preserved dissolved PaO2",
   "Increased alveolar dead space lowering arterial oxygen content",
   "A diffusion barrier at the alveolar membrane lowering PaO2"
  ],
  "answer": 3,
  "explanationText": "- 정답근거(산소 운반): CO는 Hb에 대한 친화도가 O2보다 ~200–250배 높아\n  carboxyhemoglobin을 형성 → O2 content(운반능) 감소. 게다가 남은 자리의\n  O2 방출을 방해해 곡선을 좌측 이동(조직에서 O2를 못 놓음) → 조직 저산소 악화.\n- 왜 지표가 정상처럼 보이나: 용존 O2(PaO2)는 정상이고, 표준 pulse\n  oximeter는 두 파장만 읽어 COHb를 oxyHb로 오인 → SpO2 거짓 정상. 실제\n  포화도·COHb는 co-oximetry로 측정해야 한다.\n- 오답감별: (A) PaO2는 정상이고 곡선은 좌측(우측 아님) 이동. (B)\n  methemoglobin은 별개 기전(산화 스트레스, 초콜릿색 혈액, methylene blue 치료).\n  (D)(E) dead space·확산장벽은 PaO2를 낮추는데 여기선 PaO2가 정상이라 배제.\n- 임상핵심: 화재/난방기 노출 + 두통·혼돈 + 정상 SpO2/PaO2 = CO 중독을 의심.\n  치료 100% O2(반감기 단축), 중증(신경학적 증상·심근허혈·임신)엔 고압산소.\n- 출처: respiratory physiology; toxicology (COHb, co-oximetry).",
  "explanationItems": [
   {
    "k": "정답근거(산소 운반)",
    "v": "CO는 Hb에 대한 친화도가 O2보다 ~200–250배 높아 *carboxyhemoglobin을 형성 → O2 content(운반능) 감소. 게다가 남은 자리의 O2 방출을 방해해 곡선을 좌측 이동(조직에서 O2를 못 놓음) → 조직 저산소 악화."
   },
   {
    "k": "왜 지표가 정상처럼 보이나",
    "v": "용존 O2(PaO2)는 정상이고, 표준 pulse oximeter는 두 파장만 읽어 COHb를 oxyHb로 오인 → SpO2 거짓 정상. 실제 포화도·COHb는 co-oximetry로 측정해야 한다."
   },
   {
    "k": "오답감별",
    "v": "(A) PaO2는 정상이고 곡선은 좌측(우측 아님) 이동. (B) *methemoglobin은 별개 기전(산화 스트레스, 초콜릿색 혈액, methylene blue 치료).\n(D)(E) dead space·확산장벽은 PaO2를 낮추는데 여기선 PaO2가 정상이라 배제."
   },
   {
    "k": "임상핵심",
    "v": "화재/난방기 노출 + 두통·혼돈 + 정상 SpO2/PaO2 = CO 중독을 의심. 치료 100% O2(반감기 단축), 중증(신경학적 증상·심근허혈·임신)엔 고압산소."
   },
   {
    "k": "출처",
    "v": "respiratory physiology; toxicology (COHb, co-oximetry)."
   }
  ],
  "source": "USMLE-style / MedKOS (respiratory · O2 transport)",
  "vitals": [],
  "labs": [],
  "appendix": null,
  "figureSvg": ""
 },
 {
  "id": "usmle-2026-0027",
  "exam": "usmle",
  "step": "Step 1",
  "subject": "Microbiology",
  "subject_file": "Microbiology",
  "subtopic": "Invasive Aspergillosis in prolonged neutropenia",
  "type": "Invasive Aspergillosis in prolonged neutropenia",
  "difficulty": 4,
  "created": "2026-07-07",
  "vignette": "A 46-year-old man receiving induction chemotherapy for acute myeloid leukemia has had a neutrophil count near zero for 3 weeks. He develops fever, pleuritic chest pain, and hemoptysis despite broad-spectrum antibacterial therapy. CT of the chest shows nodules with surrounding ground-glass halos, and a serum galactomannan assay is positive.",
  "question": "Which characteristic of the responsible organism most directly accounts for his hemoptysis and the CT findings?",
  "options": [
   "Broad, ribbon-like nonseptate hyphae with wide-angle branching",
   "Angioinvasion by septate hyphae that branch at acute angles, causing vascular thrombosis and hemorrhagic infarction",
   "A polysaccharide capsule that blocks phagocytosis",
   "Germ-tube-forming yeast that invades along mucosal surfaces",
   "Dimorphic yeast surviving within macrophages after inhalation"
  ],
  "answer": 2,
  "explanationText": "- 정답근거(형태·병리): Aspergillus는 격벽성(septate) 균사가 예각\n  (~45°)으로 분지하며 혈관을 침습(angioinvasion) → 혈전·출혈성 경색 →\n  객혈과 CT의 halo sign(초기)·이후 air-crescent/공동을 만든다. 장기\n  호중구감소가 결정적 위험인자이고 galactomannan(세포벽 성분)이 진단 보조.\n- 오답감별: (A) 넓은 무격벽·직각 분지 = Mucorales(당뇨 케토산증·철과부하,\n  비대뇌형). (C) 협막 효모 = Cryptococcus(India ink, 뇌수막염). (D) germ\n  tube 형성 효모 = Candida albicans. (E) 대식세포 내 이형성 효모 =\n  Histoplasma.\n- 임상핵심: 침습성 aspergillosis 1차 치료는 voriconazole(또는\n  isavuconazole). 예방은 호중구 회복. Mucor와의 감별이 치료(amphotericin B +\n  수술적 절제)를 좌우하므로 균사 형태·숙주 배경을 함께 본다.\n- 출처: medical mycology; immunocompromised host infections.",
  "explanationItems": [
   {
    "k": "정답근거(형태·병리)",
    "v": "Aspergillus는 격벽성(septate) 균사가 예각 (~45°)으로 분지하며 혈관을 침습(angioinvasion) → 혈전·출혈성 경색 → *객혈과 CT의 halo sign(초기)·이후 air-crescent/공동을 만든다. 장기 *호중구감소가 결정적 위험인자이고 galactomannan(세포벽 성분)이 진단 보조."
   },
   {
    "k": "오답감별",
    "v": "(A) 넓은 무격벽·직각 분지 = Mucorales(당뇨 케토산증·철과부하, 비대뇌형). (C) 협막 효모 = Cryptococcus(India ink, 뇌수막염). (D) germ tube 형성 효모 = Candida albicans. (E) 대식세포 내 이형성 효모 = Histoplasma."
   },
   {
    "k": "임상핵심",
    "v": "침습성 aspergillosis 1차 치료는 voriconazole(또는 isavuconazole). 예방은 호중구 회복. Mucor와의 감별이 치료(amphotericin B + 수술적 절제)를 좌우하므로 균사 형태·숙주 배경을 함께 본다."
   },
   {
    "k": "출처",
    "v": "medical mycology; immunocompromised host infections."
   }
  ],
  "source": "USMLE-style / MedKOS (mycology · immunocompromised host)",
  "vitals": [],
  "labs": [],
  "appendix": null,
  "figureSvg": ""
 },
 {
  "id": "usmle-2026-0028",
  "exam": "usmle",
  "step": "Step 2",
  "subject": "Internal Medicine",
  "subject_file": "Internal Medicine",
  "subtopic": "DKA Potassium Management",
  "type": "DKA Potassium Management",
  "difficulty": 4,
  "created": "2026-07-07",
  "vignette": "A 24-year-old man with type 1 diabetes presents with vomiting and deep rapid breathing. Glucose is 540 mg/dL, arterial pH 7.08, bicarbonate 8 mEq/L, and large serum and urine ketones. He has received 2 L of isotonic saline. His initial serum potassium is 3.2 mEq/L.",
  "question": "Which of the following is the most appropriate next step?",
  "options": [
   "Start an insulin infusion immediately without potassium because total-body potassium is high",
   "Give intravenous sodium bicarbonate to correct the acidemia first",
   "Start insulin and add potassium only once potassium falls below 2.5 mEq/L",
   "Give intravenous potassium and hold insulin until potassium is above 3.3 mEq/L",
   "Administer intravenous calcium gluconate to stabilize the myocardium"
  ],
  "answer": 4,
  "explanationText": "- 정답근거(칼륨 동태): DKA는 삼투성 이뇨·구토·산증에 의한 세포 내→외 이동\n  으로 전신 총칼륨이 심하게 고갈돼 있다. 측정 혈청 K가 정상이어도 실제 부족이며,\n  여기선 이미 3.2 mEq/L로 낮다. Insulin은 K⁺를 세포 내로 이동시켜 급격한\n  저칼륨혈증 → 치명적 부정맥을 유발할 수 있다.\n- 원칙: K < 3.3 mEq/L면 insulin을 보류하고 먼저 K를 정주 보충한다. K가\n  3.3–5.2면 insulin과 함께 K를 보충, K > 5.2면 K 없이 insulin 시작하며 추적.\n- 오답감별: (A) 총칼륨은 높지 않고 오히려 고갈 → 즉시 insulin은 위험. (B)\n  bicarbonate는 대개 불필요(pH < 6.9에서만 고려)하고 저칼륨·역설적 CNS 산증\n  위험. (C) K 2.5까지 방치하면 부정맥 위험이 이미 크다. (E) calcium은 고칼륨의\n  심근 안정화용으로 상황이 반대다.\n- 임상핵심: DKA 3축 = 수액 → 칼륨 확인 → insulin, 그리고 glucose ~200\n  에서 포도당 병용·insulin 유지로 ketone을 마저 제거(anion gap 정상화까지).\n- 출처: ADA DKA guidance; internal medicine.",
  "explanationItems": [
   {
    "k": "정답근거(칼륨 동태)",
    "v": "DKA는 삼투성 이뇨·구토·산증에 의한 세포 내→외 이동 으로 전신 총칼륨이 심하게 고갈돼 있다. 측정 혈청 K가 정상이어도 실제 부족이며, 여기선 이미 3.2 mEq/L로 낮다. Insulin은 K⁺를 세포 내로 이동시켜 급격한 *저칼륨혈증 → 치명적 부정맥을 유발할 수 있다."
   },
   {
    "k": "원칙",
    "v": "K < 3.3 mEq/L면 insulin을 보류하고 먼저 K를 정주 보충한다. K가 3.3–5.2면 insulin과 함께 K를 보충, K > 5.2면 K 없이 insulin 시작하며 추적."
   },
   {
    "k": "오답감별",
    "v": "(A) 총칼륨은 높지 않고 오히려 고갈 → 즉시 insulin은 위험. (B) *bicarbonate는 대개 불필요(pH < 6.9에서만 고려)하고 저칼륨·역설적 CNS 산증 위험. (C) K 2.5까지 방치하면 부정맥 위험이 이미 크다. (E) calcium은 고칼륨의 심근 안정화용으로 상황이 반대다."
   },
   {
    "k": "임상핵심",
    "v": "DKA 3축 = 수액 → 칼륨 확인 → insulin, 그리고 glucose ~200 에서 포도당 병용·insulin 유지로 ketone을 마저 제거(anion gap 정상화까지)."
   },
   {
    "k": "출처",
    "v": "ADA DKA guidance; internal medicine."
   }
  ],
  "source": "USMLE-style / MedKOS (endocrine emergency · electrolytes)",
  "vitals": [],
  "labs": [],
  "appendix": null,
  "figureSvg": ""
 },
 {
  "id": "usmle-2026-0029",
  "exam": "usmle",
  "step": "Step 2",
  "subject": "Surgery",
  "subject_file": "Surgery",
  "subtopic": "Necrotizing Fasciitis",
  "type": "Necrotizing Fasciitis",
  "difficulty": 4,
  "created": "2026-07-07",
  "vignette": "A 58-year-old man with diabetes presents with 1 day of rapidly worsening pain in the left leg after a minor scratch. He is febrile and tachycardic. The skin shows a dusky discoloration with a few tense bullae, and pain is far greater than the modest overlying erythema suggests. There is crepitus on palpation, and the margin of erythema is advancing over minutes.",
  "question": "Which of the following is the most appropriate next step in management?",
  "options": [
   "Outpatient oral antibiotics and elevation with next-day wound check",
   "Urgent surgical exploration and debridement, with broad-spectrum antibiotics as an adjunct",
   "MRI of the leg before any surgical decision is made",
   "Incision and drainage at the bedside with packing",
   "Compression bandaging and empiric anticoagulation for suspected DVT"
  ],
  "answer": 2,
  "explanationText": "- 정답근거(임상 인지): 통증이 홍반에 비해 과도(pain out of proportion),\n  어두운 변색·긴장성 수포, 염발음(crepitus, 가스형성), 분 단위로 번지는\n  경계, 전신 독성 → necrotizing fasciitis. 이는 외과적 응급으로 즉각적\n  광범위 debridement가 예후를 결정하고, 광범위 항생제(예: vancomycin +\n  piperacillin-tazobactam ± clindamycin)는 보조다.\n- 오답감별: (A) 외래 경구 치료는 치명적 지연. (C) MRI로 수술을 지연시키면\n  안 된다—진단이 임상적으로 뚜렷하면 곧장 수술(진단 겸 치료). (D) 침상 I&D로는\n  근막 괴사 범위를 못 다룬다. (E) DVT로 오인해 압박·항응고하면 악화.\n- 임상핵심: 보조지표 LRINEC score, 수술장 소견 회백색 무출혈 근막·\n  \"dishwater\" 삼출. clindamycin은 독소 생성 억제 목적 추가. 조기 수술 지연\n  1시간마다 사망률 상승.\n- 출처: surgical infections; emergency general surgery.",
  "explanationItems": [
   {
    "k": "정답근거(임상 인지)",
    "v": "통증이 홍반에 비해 과도(pain out of proportion), *어두운 변색·긴장성 수포, 염발음(crepitus, 가스형성), 분 단위로 번지는 경계, 전신 독성 → necrotizing fasciitis. 이는 외과적 응급으로 즉각적 광범위 debridement가 예후를 결정하고, 광범위 항생제(예: vancomycin + piperacillin-tazobactam ± clindamycin)는 보조다."
   },
   {
    "k": "오답감별",
    "v": "(A) 외래 경구 치료는 치명적 지연. (C) MRI로 수술을 지연시키면 안 된다—진단이 임상적으로 뚜렷하면 곧장 수술(진단 겸 치료). (D) 침상 I&D로는 근막 괴사 범위를 못 다룬다. (E) DVT로 오인해 압박·항응고하면 악화."
   },
   {
    "k": "임상핵심",
    "v": "보조지표 LRINEC score, 수술장 소견 회백색 무출혈 근막· \"dishwater\" 삼출. clindamycin은 독소 생성 억제 목적 추가. 조기 수술 지연 1시간마다 사망률 상승."
   },
   {
    "k": "출처",
    "v": "surgical infections; emergency general surgery."
   }
  ],
  "source": "USMLE-style / MedKOS (surgical emergency · soft-tissue infection)",
  "vitals": [],
  "labs": [],
  "appendix": null,
  "figureSvg": ""
 },
 {
  "id": "usmle-2026-0030",
  "exam": "usmle",
  "step": "Step 2",
  "subject": "Pediatrics",
  "subject_file": "Pediatrics",
  "subtopic": "STEC-Hemolytic Uremic Syndrome (antibiotics contraindicated)",
  "type": "STEC-Hemolytic Uremic Syndrome (antibiotics contraindicated)",
  "difficulty": 5,
  "created": "2026-07-07",
  "vignette": "A 4-year-old girl develops bloody diarrhea after eating an undercooked hamburger at a picnic. Five days later she is pale and lethargic with reduced urine output. Laboratory studies show anemia with schistocytes, a platelet count of 40,000/microL, and a creatinine three times her baseline. Stool testing identifies a Shiga-toxin-producing organism.",
  "question": "Which of the following is the most appropriate management?",
  "options": [
   "Empiric antibiotics to eradicate the organism and shorten the illness",
   "Loperamide to reduce stool frequency and fluid losses",
   "Prophylactic platelet transfusion to prevent bleeding",
   "Immediate plasma exchange as first-line therapy",
   "Supportive care with careful fluid and electrolyte management, avoiding antibiotics and antimotility agents"
  ],
  "answer": 5,
  "explanationText": "- 정답근거(삼징 인지): 혈성 설사 후 미세혈관병성 용혈성 빈혈(schistocyte) +\n  혈소판감소 + 급성 신손상 = Shiga toxin 생성 대장균(STEC, O157:H7)에\n  의한 전형적 HUS. 치료의 핵심은 지지요법(신중한 수액·전해질, 필요 시 투석).\n- 왜 항생제 금기: 항생제와 지사제(loperamide)는 균 사멸·정체로 Shiga\n  toxin 방출·흡수를 늘려 HUS를 유발·악화시킬 수 있어 피한다 → 정답 E.\n- 오답감별: (A)(B) 위 이유로 금기(항생제·loperamide). (C) 예방적 혈소판\n  수혈은 피함(활동성 출혈·침습적 시술 시에만). (D) plasma exchange는\n  비전형(complement) HUS나 TTP의 치료로, 전형적 소아 STEC-HUS의 1차가 아니다.\n- 임상핵심: 성인 TTP는 ADAMTS13 결핍(신경증상 우세)로 혈장교환이 1차 —\n  소아 STEC-HUS와 구분. 비전형 HUS는 보체 조절이상 → eculizumab.\n- 출처: pediatric nephrology; STEC-HUS management.",
  "explanationItems": [
   {
    "k": "정답근거(삼징 인지)",
    "v": "혈성 설사 후 미세혈관병성 용혈성 빈혈(schistocyte) + *혈소판감소 + 급성 신손상 = Shiga toxin 생성 대장균(STEC, O157:H7)에 의한 전형적 HUS. 치료의 핵심은 지지요법(신중한 수액·전해질, 필요 시 투석)."
   },
   {
    "k": "왜 항생제 금기",
    "v": "항생제와 지사제(loperamide)는 균 사멸·정체로 Shiga toxin 방출·흡수를 늘려 HUS를 유발·악화시킬 수 있어 피한다 → 정답 E."
   },
   {
    "k": "오답감별",
    "v": "(A)(B) 위 이유로 금기(항생제·loperamide). (C) 예방적 혈소판 수혈은 피함(활동성 출혈·침습적 시술 시에만). (D) plasma exchange는 *비전형(complement) HUS나 TTP의 치료로, 전형적 소아 STEC-HUS의 1차가 아니다."
   },
   {
    "k": "임상핵심",
    "v": "성인 TTP는 ADAMTS13 결핍(신경증상 우세)로 혈장교환이 1차 — 소아 STEC-HUS와 구분. 비전형 HUS는 보체 조절이상 → eculizumab."
   },
   {
    "k": "출처",
    "v": "pediatric nephrology; STEC-HUS management."
   }
  ],
  "source": "USMLE-style / MedKOS (pediatric nephrology · infectious diarrhea)",
  "vitals": [],
  "labs": [],
  "appendix": null,
  "figureSvg": ""
 },
 {
  "id": "usmle-2026-0031",
  "exam": "usmle",
  "step": "Step 2",
  "subject": "Obstetrics & Gynecology",
  "subject_file": "Obstetrics & Gynecology",
  "subtopic": "Severe Preeclampsia Management (delivery timing, IUGR/oligohydramnios)",
  "type": "Severe Preeclampsia Management (delivery timing, IUGR/oligohydramnios)",
  "difficulty": 5,
  "created": "2026-07-07",
  "vignette": "A 25-year-old primigravida at 38 weeks of gestation presents with 2 days of hand swelling and headache. On examination the cervix is 3 cm dilated, 90% effaced, with the vertex at -2 station. Ultrasound shows a cephalic fetus with an estimated weight of 2,000 g (below the 10th percentile) and an amniotic fluid index of 3 cm. Continuous fetal heart rate monitoring shows a baseline of 140/min with moderate variability and no late decelerations. Her vital signs and laboratory findings are shown.",
  "question": "Which of the following is the most appropriate next step in management?",
  "options": [
   "Expectant management with outpatient blood pressure monitoring until 40 weeks",
   "Tocolysis to prolong the pregnancy and lower the blood pressure",
   "Intravenous magnesium sulfate and an antihypertensive, then proceed with delivery",
   "Betamethasone for fetal lung maturity and delay delivery for 48 hours",
   "Immediate cesarean delivery without magnesium sulfate or antihypertensive therapy"
  ],
  "answer": 3,
  "explanationText": "- 적용(소견 → 진단 → 분기): BP 170/110(중증 범위) + 두통 + 요 단백\n  4+ + 혈소판 90,000(감소) → 중증 전자간증(severe preeclampsia). 38주\n  이고 CTG가 기저 140·중등도 변이·만기감속 없음(reassuring) → 알고리즘상\n  \"중증 · 태아 안정\" 분기. 여기에 추정체중 <10 백분위 + 양수과소(AFI 3 cm)\n  로 IUGR 동반. → MgSO₄ 발작예방 + 혈압조절 후 분만, 자궁경부 양호\n  (3 cm/90%/-2)·두위·태아안정이므로 유도분만 우선.\n- 일반 프레임워크: 아래 부록의 결정표(중증도 × 재태주수 × 태아상태)를 통째로\n  익혀 두면 재태주수·태아상태만 바꿔도 바로 적용된다.\n- 오답감별: (A) 38주 중증 전자간증에 expectant/외래관찰은 부적절(분만이\n  근치). (B) tocolysis는 중증 전자간증에서 금기(임신 연장 위험). (D)\n  betamethasone은 <34주 폐성숙 목적 — 38주엔 불필요하고 분만 지연은 해롭다.\n  (E) 태아가 안정적이면 제왕절개가 필수는 아니며, 무엇보다 MgSO₄·혈압조절을\n  생략하는 선택은 안전하지 않다.\n- 임상핵심: 중증 혈압 기준 ≥160/110, 발작예방 MgSO₄, 급성 중증 고혈압\n  labetalol·hydralazine·nifedipine. 분만 방식은 중증도가 아니라 태아상태·\n  자궁경부·산과 적응으로 결정한다.\n- 자료 관련 한계: 실제 KMLE는 CTG·흉부 X선 이미지를 함께 제시한다. 본\n  문항은 이미지 없이 CTG 소견을 텍스트로 기술했다(영상 판독은 별도 자료 필요).\n- 출처: ACOG preeclampsia guidance; Williams Obstetrics.",
  "explanationItems": [
   {
    "k": "적용(소견 → 진단 → 분기)",
    "v": "BP 170/110(중증 범위) + 두통 + 요 단백 4+ + 혈소판 90,000(감소) → 중증 전자간증(severe preeclampsia). 38주 이고 CTG가 기저 140·중등도 변이·만기감속 없음(reassuring) → 알고리즘상 *\"중증 · 태아 안정\" 분기. 여기에 추정체중 <10 백분위 + 양수과소(AFI 3 cm) 로 IUGR 동반. → MgSO₄ 발작예방 + 혈압조절 후 분만, 자궁경부 양호 (3 cm/90%/-2)·두위·태아안정이므로 유도분만 우선."
   },
   {
    "k": "일반 프레임워크",
    "v": "아래 부록의 결정표(중증도 × 재태주수 × 태아상태)를 통째로 익혀 두면 재태주수·태아상태만 바꿔도 바로 적용된다."
   },
   {
    "k": "오답감별",
    "v": "(A) 38주 중증 전자간증에 expectant/외래관찰은 부적절(분만이 근치). (B) tocolysis는 중증 전자간증에서 금기(임신 연장 위험). (D) *betamethasone은 <34주 폐성숙 목적 — 38주엔 불필요하고 분만 지연은 해롭다.\n(E) 태아가 안정적이면 제왕절개가 필수는 아니며, 무엇보다 MgSO₄·혈압조절을 생략하는 선택은 안전하지 않다."
   },
   {
    "k": "임상핵심",
    "v": "중증 혈압 기준 ≥160/110, 발작예방 MgSO₄, 급성 중증 고혈압 *labetalol·hydralazine·nifedipine. 분만 방식은 중증도가 아니라 태아상태· 자궁경부·산과 적응으로 결정한다."
   },
   {
    "k": "자료 관련 한계",
    "v": "실제 KMLE는 CTG·흉부 X선 이미지를 함께 제시한다. 본 문항은 이미지 없이 CTG 소견을 텍스트로 기술했다(영상 판독은 별도 자료 필요)."
   },
   {
    "k": "출처",
    "v": "ACOG preeclampsia guidance; Williams Obstetrics."
   }
  ],
  "source": "USMLE-style / MedKOS (obstetric emergency · hypertensive disorders)",
  "vitals": [
   {
    "name": "혈압",
    "value": "170/110 mmHg"
   },
   {
    "name": "맥박",
    "value": "82회/분"
   },
   {
    "name": "호흡",
    "value": "20회/분"
   },
   {
    "name": "체온",
    "value": "36.5 °C"
   }
  ],
  "labs": [
   {
    "name": "백혈구",
    "value": "9,000 /mm³",
    "ref": "4,000–10,000"
   },
   {
    "name": "혈색소",
    "value": "11.5 g/dL",
    "ref": "12–16"
   },
   {
    "name": "혈소판",
    "value": "90,000 /mm³",
    "ref": "150,000–400,000"
   },
   {
    "name": "AST",
    "value": "35 U/L",
    "ref": "< 40"
   },
   {
    "name": "ALT",
    "value": "40 U/L",
    "ref": "< 40"
   },
   {
    "name": "크레아티닌",
    "value": "1.1 mg/dL",
    "ref": "0.6–1.2"
   },
   {
    "name": "요 단백",
    "value": "4+",
    "ref": "음성"
   }
  ],
  "appendix": {
   "가이드라인": "전자간증·자간증 처치 (중증도 × 재태주수 × 태아상태)\n─────────────────────────────────────────────\n비중증  <34주        : 혈압조절† ± 발작예방‡, 밀착 추적관찰\n비중증  ≥34주        : (산과 합병증 동반) 유도분만 or 제왕절개\n                       (그 외) ≥37주 유도분만\n중증/자간증 · 태아안정 : 발작예방‡ + 혈압조절† + 유도분만 or 제왕절개\n중증/자간증 · 태아가사 : 발작예방‡ + 혈압조절† + 제왕절개\n─────────────────────────────────────────────\n† 혈압조절 : labetalol · hydralazine · nifedipine\n‡ 발작예방 : magnesium sulfate (MgSO₄)\n※ <34주 응급분만 시 betamethasone 고려. 단 이 때문에 급성기 대응(혈압·발작·태아가사)을 늦추지 말 것.\n",
   "최신지견": "중증 전자간증은 재태 ≥34주면 안정화 후 분만이 원칙이며, expectant management는 <34주에서만 선택적으로 고려한다.",
   "참고문헌": [
    "ACOG Practice Bulletin: Gestational Hypertension and Preeclampsia",
    "Williams Obstetrics — Hypertensive Disorders"
   ]
  },
  "figureSvg": ""
 },
 {
  "id": "usmle-2026-0032",
  "exam": "usmle",
  "step": "Step 2",
  "subject": "Internal Medicine",
  "subject_file": "Internal Medicine",
  "subtopic": "Atrial Fibrillation (ECG rhythm recognition)",
  "type": "Atrial Fibrillation (ECG rhythm recognition)",
  "difficulty": 3,
  "created": "2026-07-07",
  "vignette": "A 68-year-old woman presents with 3 hours of palpitations and mild dyspnea. Her pulse is irregularly irregular. She has no chest pain and is hemodynamically stable. A rhythm strip is shown.",
  "question": "Which of the following best describes the rhythm?",
  "options": [
   "Atrial fibrillation",
   "Atrial flutter",
   "Multifocal atrial tachycardia",
   "Sinus arrhythmia",
   "Ventricular tachycardia"
  ],
  "answer": 1,
  "explanationText": "- 적용(심전도 판독 → 진단): 리듬 스트립에서 뚜렷한 P파가 없고, 기저가\n  잔물결(f파)처럼 흔들리며 RR 간격이 불규칙하게 불규칙(irregularly\n  irregular) → 심방세동(atrial fibrillation). 진찰의 불규칙한 맥박과 일치.\n- 오답감별: (B) 심방조동은 톱니(sawtooth) F파에 흔히 규칙적 전도.\n  (C) MAT는 P파가 3가지 이상 형태 + 불규칙(흔히 COPD). (D) 동성부정맥은\n  정상 P파가 있고 호흡에 따라 RR이 변동. (E) 심실빈맥은 넓은 QRS가\n  규칙적으로 빠르게 — 형태가 명확히 다르다.\n- 임상핵심: AF의 심전도 3요소 = P파 소실 · f파 기저 · RR 불규칙하게 불규칙.\n  확인 후 CHA₂DS₂-VASc로 항응고를 결정하고 심박수/리듬 조절을 함께 본다.\n- 자료 관련 한계: 이 심전도는 별도 이미지가 아니라 수식 기반 결정론 SVG로\n  생성했다(리듬·심박수를 통제). 실제 판독 감각과 유사하나 도식화된 파형이다.\n- 출처: AHA/ACC/HRS AF guideline; clinical electrocardiography.",
  "explanationItems": [
   {
    "k": "적용(심전도 판독 → 진단)",
    "v": "리듬 스트립에서 뚜렷한 P파가 없고, 기저가 *잔물결(f파)처럼 흔들리며 RR 간격이 불규칙하게 불규칙(irregularly irregular) → 심방세동(atrial fibrillation). 진찰의 불규칙한 맥박과 일치."
   },
   {
    "k": "오답감별",
    "v": "(B) 심방조동은 톱니(sawtooth) F파에 흔히 규칙적 전도.\n(C) MAT는 P파가 3가지 이상 형태 + 불규칙(흔히 COPD). (D) 동성부정맥은 *정상 P파가 있고 호흡에 따라 RR이 변동. (E) 심실빈맥은 넓은 QRS가 규칙적으로 빠르게 — 형태가 명확히 다르다."
   },
   {
    "k": "임상핵심",
    "v": "AF의 심전도 3요소 = P파 소실 · f파 기저 · RR 불규칙하게 불규칙. 확인 후 CHA₂DS₂-VASc로 항응고를 결정하고 심박수/리듬 조절을 함께 본다."
   },
   {
    "k": "자료 관련 한계",
    "v": "이 심전도는 별도 이미지가 아니라 수식 기반 결정론 SVG로 생성했다(리듬·심박수를 통제). 실제 판독 감각과 유사하나 도식화된 파형이다."
   },
   {
    "k": "출처",
    "v": "AHA/ACC/HRS AF guideline; clinical electrocardiography."
   }
  ],
  "source": "USMLE-style / MedKOS (cardiology · ECG)",
  "vitals": [
   {
    "name": "혈압",
    "value": "128/78 mmHg"
   },
   {
    "name": "맥박",
    "value": "약 110회/분, 불규칙"
   }
  ],
  "labs": [],
  "appendix": {
   "가이드라인": "불규칙/빠른 리듬 감별 (심전도)\n─────────────────────────────────\n심방세동(AF)      : P파 소실, 기저 f파, RR '불규칙하게 불규칙'\n심방조동(Aflutter) : 톱니 F파(~300/분), 흔히 규칙적 전도(2:1·4:1)\n다소성심방빈맥(MAT): P파 ≥3형태, 불규칙, 흔히 COPD\n동성부정맥          : 정상 P파, 호흡 따라 RR 변동\n심실빈맥(VT)       : 넓은 QRS, 규칙적, 빠름 → 혈역학 불안정 시 제세동\n",
   "최신지견": "AF 확인 후엔 색전예방(CHA₂DS₂-VASc로 항응고 결정)과 심박수/리듬 조절을 함께 판단한다.",
   "참고문헌": [
    "AHA/ACC/HRS Atrial Fibrillation Guideline"
   ]
  },
  "figureSvg": "<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 900 198\" width=\"900\" height=\"198\" role=\"img\" aria-label=\"ECG 리듬 스트립 · 25 mm/s, 10 mm/mV\"><style>.bg{fill:#fff}.gmin{stroke:#f4c9c9;stroke-width:0.5}.gmaj{stroke:#e59a9a;stroke-width:1}.trace{fill:none;stroke:#111;stroke-width:1.6;stroke-linejoin:round;stroke-linecap:round}.cap{font:11px -apple-system,Segoe UI,sans-serif;fill:#555}</style><rect class=\"bg\" x=\"0\" y=\"0\" width=\"900\" height=\"180\"/><line x1=\"0\" y1=\"0\" x2=\"0\" y2=\"180\" class=\"gmaj\"/><line x1=\"6\" y1=\"0\" x2=\"6\" y2=\"180\" class=\"gmin\"/><line x1=\"12\" y1=\"0\" x2=\"12\" y2=\"180\" class=\"gmin\"/><line x1=\"18\" y1=\"0\" x2=\"18\" y2=\"180\" class=\"gmin\"/><line x1=\"24\" y1=\"0\" x2=\"24\" y2=\"180\" class=\"gmin\"/><line x1=\"30\" y1=\"0\" x2=\"30\" y2=\"180\" class=\"gmaj\"/><line x1=\"36\" y1=\"0\" x2=\"36\" y2=\"180\" class=\"gmin\"/><line x1=\"42\" y1=\"0\" x2=\"42\" y2=\"180\" class=\"gmin\"/><line x1=\"48\" y1=\"0\" x2=\"48\" y2=\"180\" class=\"gmin\"/><line x1=\"54\" y1=\"0\" x2=\"54\" y2=\"180\" class=\"gmin\"/><line x1=\"60\" y1=\"0\" x2=\"60\" y2=\"180\" class=\"gmaj\"/><line x1=\"66\" y1=\"0\" x2=\"66\" y2=\"180\" class=\"gmin\"/><line x1=\"72\" y1=\"0\" x2=\"72\" y2=\"180\" class=\"gmin\"/><line x1=\"78\" y1=\"0\" x2=\"78\" y2=\"180\" class=\"gmin\"/><line x1=\"84\" y1=\"0\" x2=\"84\" y2=\"180\" class=\"gmin\"/><line x1=\"90\" y1=\"0\" x2=\"90\" y2=\"180\" class=\"gmaj\"/><line x1=\"96\" y1=\"0\" x2=\"96\" y2=\"180\" class=\"gmin\"/><line x1=\"102\" y1=\"0\" x2=\"102\" y2=\"180\" class=\"gmin\"/><line x1=\"108\" y1=\"0\" x2=\"108\" y2=\"180\" class=\"gmin\"/><line x1=\"114\" y1=\"0\" x2=\"114\" y2=\"180\" class=\"gmin\"/><line x1=\"120\" y1=\"0\" x2=\"120\" y2=\"180\" class=\"gmaj\"/><line x1=\"126\" y1=\"0\" x2=\"126\" y2=\"180\" class=\"gmin\"/><line x1=\"132\" y1=\"0\" x2=\"132\" y2=\"180\" class=\"gmin\"/><line x1=\"138\" y1=\"0\" x2=\"138\" y2=\"180\" class=\"gmin\"/><line x1=\"144\" y1=\"0\" x2=\"144\" y2=\"180\" class=\"gmin\"/><line x1=\"150\" y1=\"0\" x2=\"150\" y2=\"180\" class=\"gmaj\"/><line x1=\"156\" y1=\"0\" x2=\"156\" y2=\"180\" class=\"gmin\"/><line x1=\"162\" y1=\"0\" x2=\"162\" y2=\"180\" class=\"gmin\"/><line x1=\"168\" y1=\"0\" x2=\"168\" y2=\"180\" class=\"gmin\"/><line x1=\"174\" y1=\"0\" x2=\"174\" y2=\"180\" class=\"gmin\"/><line x1=\"180\" y1=\"0\" x2=\"180\" y2=\"180\" class=\"gmaj\"/><line x1=\"186\" y1=\"0\" x2=\"186\" y2=\"180\" class=\"gmin\"/><line x1=\"192\" y1=\"0\" x2=\"192\" y2=\"180\" class=\"gmin\"/><line x1=\"198\" y1=\"0\" x2=\"198\" y2=\"180\" class=\"gmin\"/><line x1=\"204\" y1=\"0\" x2=\"204\" y2=\"180\" class=\"gmin\"/><line x1=\"210\" y1=\"0\" x2=\"210\" y2=\"180\" class=\"gmaj\"/><line x1=\"216\" y1=\"0\" x2=\"216\" y2=\"180\" class=\"gmin\"/><line x1=\"222\" y1=\"0\" x2=\"222\" y2=\"180\" class=\"gmin\"/><line x1=\"228\" y1=\"0\" x2=\"228\" y2=\"180\" class=\"gmin\"/><line x1=\"234\" y1=\"0\" x2=\"234\" y2=\"180\" class=\"gmin\"/><line x1=\"240\" y1=\"0\" x2=\"240\" y2=\"180\" class=\"gmaj\"/><line x1=\"246\" y1=\"0\" x2=\"246\" y2=\"180\" class=\"gmin\"/><line x1=\"252\" y1=\"0\" x2=\"252\" y2=\"180\" class=\"gmin\"/><line x1=\"258\" y1=\"0\" x2=\"258\" y2=\"180\" class=\"gmin\"/><line x1=\"264\" y1=\"0\" x2=\"264\" y2=\"180\" class=\"gmin\"/><line x1=\"270\" y1=\"0\" x2=\"270\" y2=\"180\" class=\"gmaj\"/><line x1=\"276\" y1=\"0\" x2=\"276\" y2=\"180\" class=\"gmin\"/><line x1=\"282\" y1=\"0\" x2=\"282\" y2=\"180\" class=\"gmin\"/><line x1=\"288\" y1=\"0\" x2=\"288\" y2=\"180\" class=\"gmin\"/><line x1=\"294\" y1=\"0\" x2=\"294\" y2=\"180\" class=\"gmin\"/><line x1=\"300\" y1=\"0\" x2=\"300\" y2=\"180\" class=\"gmaj\"/><line x1=\"306\" y1=\"0\" x2=\"306\" y2=\"180\" class=\"gmin\"/><line x1=\"312\" y1=\"0\" x2=\"312\" y2=\"180\" class=\"gmin\"/><line x1=\"318\" y1=\"0\" x2=\"318\" y2=\"180\" class=\"gmin\"/><line x1=\"324\" y1=\"0\" x2=\"324\" y2=\"180\" class=\"gmin\"/><line x1=\"330\" y1=\"0\" x2=\"330\" y2=\"180\" class=\"gmaj\"/><line x1=\"336\" y1=\"0\" x2=\"336\" y2=\"180\" class=\"gmin\"/><line x1=\"342\" y1=\"0\" x2=\"342\" y2=\"180\" class=\"gmin\"/><line x1=\"348\" y1=\"0\" x2=\"348\" y2=\"180\" class=\"gmin\"/><line x1=\"354\" y1=\"0\" x2=\"354\" y2=\"180\" class=\"gmin\"/><line x1=\"360\" y1=\"0\" x2=\"360\" y2=\"180\" class=\"gmaj\"/><line x1=\"366\" y1=\"0\" x2=\"366\" y2=\"180\" class=\"gmin\"/><line x1=\"372\" y1=\"0\" x2=\"372\" y2=\"180\" class=\"gmin\"/><line x1=\"378\" y1=\"0\" x2=\"378\" y2=\"180\" class=\"gmin\"/><line x1=\"384\" y1=\"0\" x2=\"384\" y2=\"180\" class=\"gmin\"/><line x1=\"390\" y1=\"0\" x2=\"390\" y2=\"180\" class=\"gmaj\"/><line x1=\"396\" y1=\"0\" x2=\"396\" y2=\"180\" class=\"gmin\"/><line x1=\"402\" y1=\"0\" x2=\"402\" y2=\"180\" class=\"gmin\"/><line x1=\"408\" y1=\"0\" x2=\"408\" y2=\"180\" class=\"gmin\"/><line x1=\"414\" y1=\"0\" x2=\"414\" y2=\"180\" class=\"gmin\"/><line x1=\"420\" y1=\"0\" x2=\"420\" y2=\"180\" class=\"gmaj\"/><line x1=\"426\" y1=\"0\" x2=\"426\" y2=\"180\" class=\"gmin\"/><line x1=\"432\" y1=\"0\" x2=\"432\" y2=\"180\" class=\"gmin\"/><line x1=\"438\" y1=\"0\" x2=\"438\" y2=\"180\" class=\"gmin\"/><line x1=\"444\" y1=\"0\" x2=\"444\" y2=\"180\" class=\"gmin\"/><line x1=\"450\" y1=\"0\" x2=\"450\" y2=\"180\" class=\"gmaj\"/><line x1=\"456\" y1=\"0\" x2=\"456\" y2=\"180\" class=\"gmin\"/><line x1=\"462\" y1=\"0\" x2=\"462\" y2=\"180\" class=\"gmin\"/><line x1=\"468\" y1=\"0\" x2=\"468\" y2=\"180\" class=\"gmin\"/><line x1=\"474\" y1=\"0\" x2=\"474\" y2=\"180\" class=\"gmin\"/><line x1=\"480\" y1=\"0\" x2=\"480\" y2=\"180\" class=\"gmaj\"/><line x1=\"486\" y1=\"0\" x2=\"486\" y2=\"180\" class=\"gmin\"/><line x1=\"492\" y1=\"0\" x2=\"492\" y2=\"180\" class=\"gmin\"/><line x1=\"498\" y1=\"0\" x2=\"498\" y2=\"180\" class=\"gmin\"/><line x1=\"504\" y1=\"0\" x2=\"504\" y2=\"180\" class=\"gmin\"/><line x1=\"510\" y1=\"0\" x2=\"510\" y2=\"180\" class=\"gmaj\"/><line x1=\"516\" y1=\"0\" x2=\"516\" y2=\"180\" class=\"gmin\"/><line x1=\"522\" y1=\"0\" x2=\"522\" y2=\"180\" class=\"gmin\"/><line x1=\"528\" y1=\"0\" x2=\"528\" y2=\"180\" class=\"gmin\"/><line x1=\"534\" y1=\"0\" x2=\"534\" y2=\"180\" class=\"gmin\"/><line x1=\"540\" y1=\"0\" x2=\"540\" y2=\"180\" class=\"gmaj\"/><line x1=\"546\" y1=\"0\" x2=\"546\" y2=\"180\" class=\"gmin\"/><line x1=\"552\" y1=\"0\" x2=\"552\" y2=\"180\" class=\"gmin\"/><line x1=\"558\" y1=\"0\" x2=\"558\" y2=\"180\" class=\"gmin\"/><line x1=\"564\" y1=\"0\" x2=\"564\" y2=\"180\" class=\"gmin\"/><line x1=\"570\" y1=\"0\" x2=\"570\" y2=\"180\" class=\"gmaj\"/><line x1=\"576\" y1=\"0\" x2=\"576\" y2=\"180\" class=\"gmin\"/><line x1=\"582\" y1=\"0\" x2=\"582\" y2=\"180\" class=\"gmin\"/><line x1=\"588\" y1=\"0\" x2=\"588\" y2=\"180\" class=\"gmin\"/><line x1=\"594\" y1=\"0\" x2=\"594\" y2=\"180\" class=\"gmin\"/><line x1=\"600\" y1=\"0\" x2=\"600\" y2=\"180\" class=\"gmaj\"/><line x1=\"606\" y1=\"0\" x2=\"606\" y2=\"180\" class=\"gmin\"/><line x1=\"612\" y1=\"0\" x2=\"612\" y2=\"180\" class=\"gmin\"/><line x1=\"618\" y1=\"0\" x2=\"618\" y2=\"180\" class=\"gmin\"/><line x1=\"624\" y1=\"0\" x2=\"624\" y2=\"180\" class=\"gmin\"/><line x1=\"630\" y1=\"0\" x2=\"630\" y2=\"180\" class=\"gmaj\"/><line x1=\"636\" y1=\"0\" x2=\"636\" y2=\"180\" class=\"gmin\"/><line x1=\"642\" y1=\"0\" x2=\"642\" y2=\"180\" class=\"gmin\"/><line x1=\"648\" y1=\"0\" x2=\"648\" y2=\"180\" class=\"gmin\"/><line x1=\"654\" y1=\"0\" x2=\"654\" y2=\"180\" class=\"gmin\"/><line x1=\"660\" y1=\"0\" x2=\"660\" y2=\"180\" class=\"gmaj\"/><line x1=\"666\" y1=\"0\" x2=\"666\" y2=\"180\" class=\"gmin\"/><line x1=\"672\" y1=\"0\" x2=\"672\" y2=\"180\" class=\"gmin\"/><line x1=\"678\" y1=\"0\" x2=\"678\" y2=\"180\" class=\"gmin\"/><line x1=\"684\" y1=\"0\" x2=\"684\" y2=\"180\" class=\"gmin\"/><line x1=\"690\" y1=\"0\" x2=\"690\" y2=\"180\" class=\"gmaj\"/><line x1=\"696\" y1=\"0\" x2=\"696\" y2=\"180\" class=\"gmin\"/><line x1=\"702\" y1=\"0\" x2=\"702\" y2=\"180\" class=\"gmin\"/><line x1=\"708\" y1=\"0\" x2=\"708\" y2=\"180\" class=\"gmin\"/><line x1=\"714\" y1=\"0\" x2=\"714\" y2=\"180\" class=\"gmin\"/><line x1=\"720\" y1=\"0\" x2=\"720\" y2=\"180\" class=\"gmaj\"/><line x1=\"726\" y1=\"0\" x2=\"726\" y2=\"180\" class=\"gmin\"/><line x1=\"732\" y1=\"0\" x2=\"732\" y2=\"180\" class=\"gmin\"/><line x1=\"738\" y1=\"0\" x2=\"738\" y2=\"180\" class=\"gmin\"/><line x1=\"744\" y1=\"0\" x2=\"744\" y2=\"180\" class=\"gmin\"/><line x1=\"750\" y1=\"0\" x2=\"750\" y2=\"180\" class=\"gmaj\"/><line x1=\"756\" y1=\"0\" x2=\"756\" y2=\"180\" class=\"gmin\"/><line x1=\"762\" y1=\"0\" x2=\"762\" y2=\"180\" class=\"gmin\"/><line x1=\"768\" y1=\"0\" x2=\"768\" y2=\"180\" class=\"gmin\"/><line x1=\"774\" y1=\"0\" x2=\"774\" y2=\"180\" class=\"gmin\"/><line x1=\"780\" y1=\"0\" x2=\"780\" y2=\"180\" class=\"gmaj\"/><line x1=\"786\" y1=\"0\" x2=\"786\" y2=\"180\" class=\"gmin\"/><line x1=\"792\" y1=\"0\" x2=\"792\" y2=\"180\" class=\"gmin\"/><line x1=\"798\" y1=\"0\" x2=\"798\" y2=\"180\" class=\"gmin\"/><line x1=\"804\" y1=\"0\" x2=\"804\" y2=\"180\" class=\"gmin\"/><line x1=\"810\" y1=\"0\" x2=\"810\" y2=\"180\" class=\"gmaj\"/><line x1=\"816\" y1=\"0\" x2=\"816\" y2=\"180\" class=\"gmin\"/><line x1=\"822\" y1=\"0\" x2=\"822\" y2=\"180\" class=\"gmin\"/><line x1=\"828\" y1=\"0\" x2=\"828\" y2=\"180\" class=\"gmin\"/><line x1=\"834\" y1=\"0\" x2=\"834\" y2=\"180\" class=\"gmin\"/><line x1=\"840\" y1=\"0\" x2=\"840\" y2=\"180\" class=\"gmaj\"/><line x1=\"846\" y1=\"0\" x2=\"846\" y2=\"180\" class=\"gmin\"/><line x1=\"852\" y1=\"0\" x2=\"852\" y2=\"180\" class=\"gmin\"/><line x1=\"858\" y1=\"0\" x2=\"858\" y2=\"180\" class=\"gmin\"/><line x1=\"864\" y1=\"0\" x2=\"864\" y2=\"180\" class=\"gmin\"/><line x1=\"870\" y1=\"0\" x2=\"870\" y2=\"180\" class=\"gmaj\"/><line x1=\"876\" y1=\"0\" x2=\"876\" y2=\"180\" class=\"gmin\"/><line x1=\"882\" y1=\"0\" x2=\"882\" y2=\"180\" class=\"gmin\"/><line x1=\"888\" y1=\"0\" x2=\"888\" y2=\"180\" class=\"gmin\"/><line x1=\"894\" y1=\"0\" x2=\"894\" y2=\"180\" class=\"gmin\"/><line x1=\"900\" y1=\"0\" x2=\"900\" y2=\"180\" class=\"gmaj\"/><line x1=\"0\" y1=\"0\" x2=\"900\" y2=\"0\" class=\"gmaj\"/><line x1=\"0\" y1=\"6\" x2=\"900\" y2=\"6\" class=\"gmin\"/><line x1=\"0\" y1=\"12\" x2=\"900\" y2=\"12\" class=\"gmin\"/><line x1=\"0\" y1=\"18\" x2=\"900\" y2=\"18\" class=\"gmin\"/><line x1=\"0\" y1=\"24\" x2=\"900\" y2=\"24\" class=\"gmin\"/><line x1=\"0\" y1=\"30\" x2=\"900\" y2=\"30\" class=\"gmaj\"/><line x1=\"0\" y1=\"36\" x2=\"900\" y2=\"36\" class=\"gmin\"/><line x1=\"0\" y1=\"42\" x2=\"900\" y2=\"42\" class=\"gmin\"/><line x1=\"0\" y1=\"48\" x2=\"900\" y2=\"48\" class=\"gmin\"/><line x1=\"0\" y1=\"54\" x2=\"900\" y2=\"54\" class=\"gmin\"/><line x1=\"0\" y1=\"60\" x2=\"900\" y2=\"60\" class=\"gmaj\"/><line x1=\"0\" y1=\"66\" x2=\"900\" y2=\"66\" class=\"gmin\"/><line x1=\"0\" y1=\"72\" x2=\"900\" y2=\"72\" class=\"gmin\"/><line x1=\"0\" y1=\"78\" x2=\"900\" y2=\"78\" class=\"gmin\"/><line x1=\"0\" y1=\"84\" x2=\"900\" y2=\"84\" class=\"gmin\"/><line x1=\"0\" y1=\"90\" x2=\"900\" y2=\"90\" class=\"gmaj\"/><line x1=\"0\" y1=\"96\" x2=\"900\" y2=\"96\" class=\"gmin\"/><line x1=\"0\" y1=\"102\" x2=\"900\" y2=\"102\" class=\"gmin\"/><line x1=\"0\" y1=\"108\" x2=\"900\" y2=\"108\" class=\"gmin\"/><line x1=\"0\" y1=\"114\" x2=\"900\" y2=\"114\" class=\"gmin\"/><line x1=\"0\" y1=\"120\" x2=\"900\" y2=\"120\" class=\"gmaj\"/><line x1=\"0\" y1=\"126\" x2=\"900\" y2=\"126\" class=\"gmin\"/><line x1=\"0\" y1=\"132\" x2=\"900\" y2=\"132\" class=\"gmin\"/><line x1=\"0\" y1=\"138\" x2=\"900\" y2=\"138\" class=\"gmin\"/><line x1=\"0\" y1=\"144\" x2=\"900\" y2=\"144\" class=\"gmin\"/><line x1=\"0\" y1=\"150\" x2=\"900\" y2=\"150\" class=\"gmaj\"/><line x1=\"0\" y1=\"156\" x2=\"900\" y2=\"156\" class=\"gmin\"/><line x1=\"0\" y1=\"162\" x2=\"900\" y2=\"162\" class=\"gmin\"/><line x1=\"0\" y1=\"168\" x2=\"900\" y2=\"168\" class=\"gmin\"/><line x1=\"0\" y1=\"174\" x2=\"900\" y2=\"174\" class=\"gmin\"/><line x1=\"0\" y1=\"180\" x2=\"900\" y2=\"180\" class=\"gmaj\"/><polyline class=\"trace\" points=\"0.0,88.8 0.6,88.5 1.2,88.2 1.8,88.0 2.4,88.0 3.0,88.1 3.6,88.2 4.2,88.4 4.8,88.7 5.4,89.0 6.0,89.2 6.6,89.5 7.2,89.7 7.8,89.9 8.4,90.1 9.0,90.2 9.6,90.2 10.2,90.2 10.8,90.2 11.4,90.2 12.0,90.2 12.6,90.3 13.2,90.3 13.8,90.4 14.4,90.5 15.0,90.7 15.6,90.9 16.2,91.1 16.8,91.3 17.4,91.4 18.0,91.6 18.6,91.6 19.2,91.6 19.8,91.5 20.4,91.3 21.0,90.9 21.6,90.6 22.2,90.1 22.8,89.6 23.4,89.1 24.0,88.6 24.6,88.1 25.2,87.7 25.8,87.4 26.4,87.2 27.0,87.2 27.6,87.3 28.2,87.6 28.8,87.9 29.4,88.4 30.0,89.0 30.6,89.7 31.2,90.3 31.8,91.0 32.4,91.6 33.0,92.1 33.6,92.5 34.2,92.7 34.8,92.9 35.4,92.8 36.0,92.7 36.6,92.4 37.2,92.0 37.8,91.5 38.4,91.0 39.0,90.4 39.6,89.9 40.2,89.4 40.8,89.0 41.4,88.8 42.0,88.9 42.6,89.5 43.2,90.3 43.8,90.1 44.4,87.4 45.0,81.5 45.6,72.0 46.2,59.6 46.8,45.8 47.4,33.8 48.0,27.4 48.6,29.0 49.2,38.3 49.8,52.5 50.4,67.8 51.0,81.1 51.6,90.9 52.2,96.8 52.8,99.4 53.4,99.5 54.0,98.0 54.6,95.9 55.2,94.0 55.8,92.6 56.4,91.9 57.0,91.6 57.6,91.6 58.2,91.7 58.8,91.8 59.4,91.9 60.0,91.8 60.6,91.7 61.2,91.4 61.8,91.1 62.4,90.7 63.0,90.2 63.6,89.6 64.2,89.0 64.8,88.5 65.4,88.0 66.0,87.6 66.6,87.3 67.2,87.1 67.8,87.1 68.4,87.2 69.0,87.5 69.6,87.9 70.2,88.4 70.8,88.9 71.4,89.6 72.0,90.2 72.6,90.8 73.2,91.3 73.8,91.8 74.4,92.1 75.0,92.2 75.6,92.2 76.2,92.0 76.8,91.7 77.4,91.2 78.0,90.6 78.6,89.8 79.2,89.0 79.8,88.1 80.4,87.2 81.0,86.2 81.6,85.3 82.2,84.4 82.8,83.5 83.4,82.7 84.0,81.9 84.6,81.1 85.2,80.4 85.8,79.6 86.4,78.9 87.0,78.2 87.6,77.4 88.2,76.7 88.8,76.0 89.4,75.3 90.0,74.7 90.6,74.1 91.2,73.6 91.8,73.2 92.4,73.0 93.0,72.9 93.6,72.9 94.2,73.2 94.8,73.7 95.4,74.3 96.0,75.0 96.6,76.0 97.2,77.0 97.8,78.0 98.4,79.2 99.0,80.2 99.6,81.3 100.2,82.3 100.8,83.1 101.4,83.8 102.0,84.4 102.6,84.8 103.2,85.1 103.8,85.3 104.4,85.4 105.0,85.4 105.6,85.3 106.2,85.3 106.8,85.3 107.4,85.4 108.0,85.5 108.6,85.8 109.2,86.2 109.8,86.6 110.4,87.2 111.0,87.9 111.6,88.6 112.2,89.3 112.8,90.0 113.4,90.7 114.0,91.3 114.6,91.8 115.2,92.2 115.8,92.5 116.4,92.6 117.0,92.6 117.6,92.4 118.2,92.1 118.8,91.8 119.4,91.4 120.0,90.9 120.6,90.4 121.2,90.0 121.8,89.6 122.4,89.3 123.0,89.0 123.6,88.9 124.2,88.8 124.8,88.8 125.4,88.8 126.0,88.9 126.6,89.0 127.2,89.1 127.8,89.3 128.4,89.4 129.0,89.4 129.6,89.5 130.2,89.5 130.8,89.4 131.4,89.4 132.0,89.4 132.6,89.3 133.2,89.3 133.8,89.4 134.4,89.5 135.0,89.6 135.6,89.9 136.2,90.1 136.8,90.5 137.4,90.8 138.0,91.2 138.6,91.5 139.2,91.8 139.8,92.1 140.4,92.2 141.0,92.3 141.6,92.2 142.2,92.1 142.8,91.7 143.4,91.3 144.0,90.8 144.6,90.2 145.2,89.6 145.8,89.0 146.4,88.4 147.0,87.9 147.6,87.5 148.2,87.2 148.8,87.0 149.4,87.0 150.0,87.2 150.6,87.5 151.2,87.9 151.8,88.6 152.4,89.6 153.0,91.0 153.6,92.3 154.2,92.5 154.8,90.0 155.4,84.0 156.0,74.3 156.6,61.6 157.2,47.7 157.8,35.8 158.4,29.8 159.0,31.7 159.6,41.3 160.2,55.3 160.8,70.1 161.4,82.7 162.0,91.7 162.6,97.0 163.2,99.0 163.8,98.6 164.4,96.8 165.0,94.4 165.6,92.3 166.2,90.9 166.8,90.0 167.4,89.6 168.0,89.4 168.6,89.4 169.2,89.4 169.8,89.4 170.4,89.4 171.0,89.3 171.6,89.2 172.2,89.1 172.8,89.1 173.4,89.0 174.0,89.0 174.6,89.1 175.2,89.2 175.8,89.4 176.4,89.7 177.0,90.0 177.6,90.4 178.2,90.8 178.8,91.2 179.4,91.6 180.0,92.0 180.6,92.2 181.2,92.4 181.8,92.4 182.4,92.3 183.0,92.0 183.6,91.7 184.2,91.1 184.8,90.5 185.4,89.8 186.0,89.1 186.6,88.3 187.2,87.5 187.8,86.8 188.4,86.1 189.0,85.5 189.6,85.0 190.2,84.7 190.8,84.4 191.4,84.2 192.0,84.0 192.6,83.9 193.2,83.8 193.8,83.7 194.4,83.5 195.0,83.3 195.6,82.9 196.2,82.5 196.8,81.9 197.4,81.1 198.0,80.3 198.6,79.4 199.2,78.4 199.8,77.4 200.4,76.5 201.0,75.5 201.6,74.7 202.2,74.0 202.8,73.5 203.4,73.1 204.0,72.9 204.6,72.9 205.2,73.1 205.8,73.5 206.4,74.0 207.0,74.6 207.6,75.4 208.2,76.2 208.8,77.0 209.4,77.9 210.0,78.8 210.6,79.6 211.2,80.4 211.8,81.2 212.4,81.9 213.0,82.6 213.6,83.2 214.2,83.9 214.8,84.6 215.4,85.2 216.0,85.9 216.6,86.7 217.2,87.4 217.8,88.2 218.4,88.9 219.0,89.7 219.6,90.3 220.2,91.0 220.8,91.5 221.4,91.9 222.0,92.2 222.6,92.3 223.2,92.3 223.8,92.1 224.4,91.8 225.0,91.4 225.6,90.9 226.2,90.3 226.8,89.7 227.4,89.0 228.0,88.5 228.6,88.2 229.2,88.3 229.8,88.9 230.4,89.2 231.0,87.8 231.6,83.5 232.2,75.8 232.8,64.9 233.4,51.7 234.0,38.7 234.6,29.6 235.2,27.6 235.8,33.8 236.4,46.5 237.0,62.1 237.6,76.9 238.2,88.7 238.8,96.5 239.4,100.6 240.0,101.6 240.6,100.4 241.2,98.1 241.8,95.5 242.4,93.3 243.0,91.8 243.6,90.8 244.2,90.2 244.8,89.9 245.4,89.8 246.0,89.7 246.6,89.7 247.2,89.7 247.8,89.7 248.4,89.7 249.0,89.7 249.6,89.6 250.2,89.6 250.8,89.5 251.4,89.3 252.0,89.2 252.6,89.0 253.2,88.8 253.8,88.6 254.4,88.5 255.0,88.5 255.6,88.5 256.2,88.6 256.8,88.8 257.4,89.0 258.0,89.4 258.6,89.8 259.2,90.3 259.8,90.7 260.4,91.2 261.0,91.6 261.6,91.9 262.2,92.1 262.8,92.1 263.4,92.0 264.0,91.7 264.6,91.2 265.2,90.6 265.8,89.8 266.4,88.8 267.0,87.8 267.6,86.6 268.2,85.5 268.8,84.3 269.4,83.1 270.0,82.0 270.6,81.0 271.2,80.1 271.8,79.3 272.4,78.5 273.0,77.9 273.6,77.4 274.2,77.0 274.8,76.7 275.4,76.4 276.0,76.2 276.6,76.0 277.2,76.0 277.8,76.3 278.4,77.0 279.0,77.4 279.6,76.2 280.2,72.2 280.8,64.8 281.4,53.9 282.0,40.6 282.6,27.0 283.2,16.8 283.8,13.3 284.4,18.3 285.0,30.3 285.6,46.1 286.2,61.7 286.8,74.8 287.4,84.1 288.0,89.6 288.6,92.1 289.2,92.2 289.8,91.0 290.4,89.3 291.0,87.9 291.6,87.0 292.2,86.6 292.8,86.5 293.4,86.5 294.0,86.6 294.6,86.7 295.2,86.9 295.8,87.1 296.4,87.3 297.0,87.7 297.6,88.0 298.2,88.5 298.8,89.0 299.4,89.6 300.0,90.2 300.6,90.8 301.2,91.3 301.8,91.9 302.4,92.3 303.0,92.7 303.6,92.8 304.2,92.8 304.8,92.7 305.4,92.5 306.0,92.0 306.6,91.5 307.2,90.9 307.8,90.2 308.4,89.5 309.0,88.8 309.6,88.2 310.2,87.6 310.8,87.1 311.4,86.7 312.0,86.4 312.6,86.3 313.2,86.2 313.8,86.3 314.4,86.4 315.0,86.5 315.6,86.6 316.2,86.6 316.8,86.6 317.4,86.5 318.0,86.3 318.6,85.9 319.2,85.3 319.8,84.7 320.4,83.8 321.0,82.9 321.6,81.9 322.2,80.8 322.8,79.8 323.4,78.7 324.0,77.6 324.6,76.7 325.2,75.8 325.8,75.1 326.4,74.5 327.0,74.0 327.6,73.7 328.2,73.5 328.8,73.5 329.4,73.5 330.0,73.7 330.6,73.9 331.2,74.2 331.8,74.5 332.4,74.9 333.0,75.4 333.6,75.9 334.2,76.5 334.8,77.1 335.4,77.8 336.0,78.5 336.6,79.4 337.2,80.3 337.8,81.3 338.4,82.3 339.0,83.5 339.6,84.6 340.2,85.8 340.8,86.9 341.4,88.0 342.0,89.0 342.6,90.0 343.2,90.7 343.8,91.3 344.4,91.8 345.0,92.0 345.6,92.1 346.2,91.9 346.8,91.6 347.4,91.2 348.0,90.7 348.6,90.1 349.2,89.5 349.8,88.9 350.4,88.4 351.0,87.9 351.6,87.7 352.2,87.4 352.8,87.3 353.4,87.4 354.0,87.5 354.6,87.8 355.2,88.2 355.8,88.6 356.4,89.1 357.0,89.6 357.6,90.0 358.2,90.4 358.8,90.8 359.4,91.0 360.0,91.2 360.6,91.3 361.2,91.3 361.8,91.3 362.4,91.2 363.0,91.1 363.6,90.9 364.2,90.8 364.8,90.7 365.4,90.6 366.0,90.5 366.6,90.5 367.2,90.5 367.8,90.5 368.4,90.5 369.0,90.6 369.6,90.6 370.2,90.5 370.8,90.4 371.4,90.3 372.0,90.1 372.6,89.8 373.2,89.5 373.8,89.2 374.4,88.9 375.0,88.5 375.6,88.2 376.2,88.0 376.8,87.8 377.4,87.8 378.0,87.8 378.6,88.0 379.2,88.3 379.8,88.7 380.4,89.2 381.0,89.8 381.6,90.4 382.2,91.0 382.8,91.6 383.4,92.1 384.0,92.8 384.6,93.6 385.2,94.6 385.8,95.1 386.4,93.9 387.0,89.6 387.6,81.6 388.2,70.1 388.8,56.0 389.4,41.6 390.0,30.6 390.6,26.4 391.2,30.6 391.8,41.7 392.4,56.4 393.0,71.0 393.6,82.9 394.2,91.2 394.8,95.9 395.4,97.7 396.0,97.3 396.6,95.7 397.2,93.8 397.8,92.3 398.4,91.4 399.0,90.9 399.6,90.8 400.2,90.9 400.8,91.0 401.4,91.0 402.0,91.0 402.6,91.0 403.2,90.9 403.8,90.8 404.4,90.7 405.0,90.7 405.6,90.6 406.2,90.6 406.8,90.6 407.4,90.6 408.0,90.7 408.6,90.8 409.2,90.8 409.8,90.9 410.4,90.8 411.0,90.8 411.6,90.7 412.2,90.5 412.8,90.2 413.4,89.8 414.0,89.5 414.6,89.0 415.2,88.6 415.8,88.2 416.4,87.8 417.0,87.4 417.6,87.1 418.2,87.0 418.8,86.9 419.4,86.9 420.0,87.0 420.6,87.2 421.2,87.4 421.8,87.6 422.4,87.9 423.0,88.0 423.6,88.1 424.2,88.1 424.8,87.8 425.4,87.4 426.0,86.8 426.6,86.0 427.2,85.1 427.8,83.9 428.4,82.6 429.0,81.1 429.6,79.7 430.2,78.2 430.8,76.7 431.4,75.3 432.0,74.1 432.6,73.0 433.2,72.1 433.8,71.5 434.4,71.1 435.0,71.0 435.6,71.1 436.2,71.4 436.8,71.9 437.4,72.6 438.0,73.4 438.6,74.3 439.2,75.3 439.8,76.4 440.4,77.4 441.0,78.4 441.6,79.4 442.2,80.4 442.8,81.3 443.4,82.1 444.0,83.0 444.6,83.7 445.2,84.5 445.8,85.2 446.4,85.9 447.0,86.6 447.6,87.3 448.2,87.9 448.8,88.5 449.4,89.0 450.0,89.4 450.6,89.7 451.2,90.0 451.8,90.1 452.4,90.2 453.0,90.1 453.6,89.9 454.2,89.6 454.8,89.3 455.4,88.9 456.0,88.5 456.6,88.1 457.2,87.8 457.8,87.6 458.4,87.5 459.0,87.4 459.6,87.5 460.2,87.7 460.8,88.1 461.4,88.5 462.0,89.1 462.6,89.7 463.2,90.4 463.8,91.0 464.4,91.6 465.0,92.1 465.6,92.5 466.2,92.8 466.8,93.0 467.4,93.0 468.0,92.8 468.6,92.5 469.2,92.1 469.8,91.6 470.4,91.0 471.0,90.4 471.6,89.8 472.2,89.3 472.8,88.8 473.4,88.4 474.0,88.1 474.6,87.9 475.2,87.9 475.8,87.9 476.4,88.1 477.0,88.3 477.6,88.6 478.2,88.9 478.8,89.2 479.4,89.5 480.0,89.8 480.6,90.0 481.2,90.2 481.8,90.3 482.4,90.4 483.0,90.4 483.6,90.4 484.2,90.4 484.8,90.4 485.4,90.4 486.0,90.4 486.6,90.5 487.2,90.5 487.8,90.7 488.4,90.8 489.0,91.0 489.6,91.1 490.2,91.3 490.8,91.4 491.4,91.4 492.0,91.5 492.6,91.6 493.2,91.9 493.8,92.5 494.4,92.6 495.0,91.1 495.6,86.6 496.2,78.5 496.8,67.0 497.4,53.1 498.0,38.9 498.6,28.3 499.2,24.6 499.8,29.3 500.4,41.1 501.0,56.4 501.6,71.5 502.2,84.0 502.8,92.8 503.4,98.0 504.0,100.1 504.6,99.9 505.2,98.5 505.8,96.8 506.4,95.3 507.0,94.2 507.6,93.6 508.2,93.1 508.8,92.8 509.4,92.5 510.0,92.0 510.6,91.5 511.2,91.0 511.8,90.4 512.4,89.9 513.0,89.3 513.6,88.9 514.2,88.5 514.8,88.3 515.4,88.1 516.0,88.1 516.6,88.1 517.2,88.3 517.8,88.5 518.4,88.7 519.0,89.0 519.6,89.2 520.2,89.5 520.8,89.7 521.4,89.8 522.0,89.9 522.6,90.0 523.2,90.0 523.8,90.0 524.4,89.9 525.0,89.8 525.6,89.8 526.2,89.7 526.8,89.6 527.4,89.6 528.0,89.6 528.6,89.5 529.2,89.5 529.8,89.4 530.4,89.2 531.0,89.0 531.6,88.7 532.2,88.2 532.8,87.6 533.4,86.8 534.0,85.9 534.6,84.9 535.2,83.7 535.8,82.3 536.4,80.9 537.0,79.5 537.6,78.1 538.2,76.7 538.8,75.4 539.4,74.3 540.0,73.3 540.6,72.6 541.2,72.0 541.8,71.7 542.4,71.7 543.0,71.9 543.6,72.3 544.2,72.9 544.8,73.6 545.4,74.4 546.0,75.4 546.6,76.3 547.2,77.3 547.8,78.2 548.4,79.0 549.0,79.8 549.6,80.5 550.2,81.1 550.8,81.6 551.4,82.0 552.0,82.4 552.6,82.7 553.2,83.0 553.8,83.4 554.4,83.7 555.0,84.1 555.6,84.5 556.2,84.9 556.8,85.4 557.4,85.9 558.0,86.4 558.6,87.0 559.2,87.5 559.8,87.9 560.4,88.4 561.0,88.7 561.6,89.0 562.2,89.3 562.8,89.4 563.4,89.5 564.0,89.6 564.6,89.7 565.2,89.7 565.8,89.7 566.4,89.8 567.0,90.0 567.6,90.1 568.2,90.3 568.8,90.5 569.4,90.7 570.0,91.0 570.6,91.3 571.2,91.5 571.8,91.7 572.4,91.9 573.0,91.9 573.6,91.9 574.2,91.8 574.8,91.5 575.4,91.1 576.0,90.7 576.6,90.2 577.2,89.6 577.8,89.1 578.4,88.8 579.0,89.0 579.6,89.4 580.2,89.3 580.8,87.4 581.4,82.4 582.0,74.0 582.6,62.5 583.2,49.1 583.8,36.4 584.4,28.1 585.0,27.4 585.6,34.9 586.2,48.4 586.8,64.3 587.4,79.0 588.0,90.4 588.6,97.9 589.2,101.6 589.8,102.4 590.4,101.0 591.0,98.6 591.6,96.0 592.2,93.7 592.8,92.1 593.4,90.9 594.0,90.2 594.6,89.6 595.2,89.2 595.8,88.9 596.4,88.7 597.0,88.6 597.6,88.6 598.2,88.6 598.8,88.7 599.4,88.9 600.0,89.0 600.6,89.2 601.2,89.3 601.8,89.4 602.4,89.5 603.0,89.6 603.6,89.6 604.2,89.6 604.8,89.5 605.4,89.5 606.0,89.5 606.6,89.5 607.2,89.6 607.8,89.7 608.4,89.8 609.0,90.0 609.6,90.3 610.2,90.5 610.8,90.8 611.4,91.0 612.0,91.2 612.6,91.3 613.2,91.3 613.8,91.2 614.4,90.9 615.0,90.4 615.6,89.8 616.2,89.1 616.8,88.2 617.4,87.1 618.0,86.0 618.6,84.8 619.2,83.6 619.8,82.3 620.4,81.2 621.0,80.1 621.6,79.0 622.2,78.1 622.8,77.4 623.4,76.8 624.0,76.3 624.6,75.9 625.2,75.7 625.8,75.6 626.4,75.5 627.0,75.5 627.6,75.5 628.2,75.6 628.8,75.7 629.4,75.7 630.0,75.8 630.6,75.9 631.2,75.9 631.8,76.0 632.4,76.1 633.0,76.3 633.6,76.5 634.2,76.8 634.8,77.2 635.4,77.7 636.0,78.3 636.6,79.0 637.2,79.7 637.8,80.5 638.4,81.4 639.0,82.2 639.6,83.1 640.2,83.9 640.8,84.7 641.4,85.4 642.0,86.1 642.6,86.6 643.2,87.1 643.8,87.4 644.4,87.7 645.0,88.0 645.6,88.2 646.2,88.4 646.8,88.5 647.4,88.7 648.0,88.9 648.6,89.2 649.2,89.5 649.8,89.9 650.4,90.3 651.0,90.7 651.6,91.1 652.2,91.5 652.8,91.9 653.4,92.1 654.0,92.3 654.6,92.4 655.2,92.3 655.8,92.1 656.4,91.8 657.0,91.4 657.6,90.8 658.2,90.3 658.8,89.6 659.4,89.0 660.0,88.4 660.6,87.9 661.2,87.5 661.8,87.2 662.4,87.0 663.0,87.0 663.6,87.2 664.2,87.5 664.8,87.9 665.4,88.4 666.0,89.0 666.6,89.6 667.2,90.2 667.8,90.8 668.4,91.4 669.0,91.9 669.6,92.4 670.2,93.1 670.8,94.0 671.4,94.5 672.0,93.3 672.6,89.2 673.2,81.5 673.8,70.3 674.4,56.4 675.0,42.2 675.6,31.3 676.2,27.0 676.8,31.2 677.4,42.4 678.0,57.2 678.6,72.0 679.2,84.2 679.8,92.6 680.4,97.4 681.0,99.0 681.6,98.4 682.2,96.5 682.8,94.2 683.4,92.2 684.0,90.8 684.6,89.9 685.2,89.4 685.8,89.2 686.4,89.0 687.0,88.9 687.6,89.0 688.2,89.0 688.8,89.2 689.4,89.4 690.0,89.7 690.6,90.0 691.2,90.4 691.8,90.9 692.4,91.3 693.0,91.7 693.6,92.0 694.2,92.3 694.8,92.5 695.4,92.5 696.0,92.4 696.6,92.2 697.2,91.9 697.8,91.4 698.4,90.8 699.0,90.2 699.6,89.5 700.2,88.9 700.8,88.2 701.4,87.7 702.0,87.2 702.6,86.8 703.2,86.5 703.8,86.4 704.4,86.4 705.0,86.5 705.6,86.7 706.2,87.0 706.8,87.3 707.4,87.5 708.0,87.7 708.6,87.8 709.2,87.8 709.8,87.6 710.4,87.3 711.0,86.8 711.6,86.1 712.2,85.3 712.8,84.3 713.4,83.2 714.0,82.0 714.6,80.7 715.2,79.5 715.8,78.3 716.4,77.1 717.0,76.1 717.6,75.1 718.2,74.4 718.8,73.7 719.4,73.2 720.0,72.9 720.6,72.7 721.2,72.7 721.8,72.8 722.4,73.0 723.0,73.4 723.6,74.2 724.2,75.4 724.8,76.7 725.4,77.0 726.0,74.9 726.6,69.5 727.2,60.6 727.8,48.7 728.4,35.6 729.0,24.4 729.6,18.9 730.2,21.5 730.8,31.9 731.4,47.2 732.0,63.6 732.6,78.0 733.2,88.8 733.8,95.8 734.4,99.2 735.0,99.8 735.6,98.8 736.2,96.8 736.8,94.9 737.4,93.3 738.0,92.1 738.6,91.3 739.2,90.6 739.8,90.0 740.4,89.4 741.0,88.8 741.6,88.2 742.2,87.8 742.8,87.4 743.4,87.1 744.0,87.1 744.6,87.1 745.2,87.2 745.8,87.5 746.4,88.0 747.0,88.5 747.6,89.0 748.2,89.6 748.8,90.2 749.4,90.7 750.0,91.1 750.6,91.5 751.2,91.8 751.8,91.9 752.4,91.9 753.0,91.9 753.6,91.7 754.2,91.4 754.8,91.1 755.4,90.8 756.0,90.4 756.6,90.1 757.2,89.7 757.8,89.4 758.4,89.0 759.0,88.7 759.6,88.4 760.2,88.1 760.8,87.8 761.4,87.4 762.0,87.0 762.6,86.5 763.2,85.9 763.8,85.2 764.4,84.4 765.0,83.5 765.6,82.5 766.2,81.5 766.8,80.4 767.4,79.4 768.0,78.4 768.6,77.4 769.2,76.5 769.8,75.8 770.4,75.2 771.0,74.7 771.6,74.4 772.2,74.3 772.8,74.3 773.4,74.5 774.0,74.8 774.6,75.1 775.2,75.5 775.8,76.0 776.4,76.4 777.0,76.9 777.6,77.3 778.2,77.6 778.8,78.0 779.4,78.2 780.0,78.5 780.6,78.7 781.2,78.9 781.8,79.2 782.4,79.5 783.0,79.9 783.6,80.3 784.2,80.9 784.8,81.5 785.4,82.3 786.0,83.1 786.6,84.0 787.2,84.9 787.8,85.9 788.4,86.8 789.0,87.7 789.6,88.6 790.2,89.4 790.8,90.0 791.4,90.5 792.0,90.9 792.6,91.2 793.2,91.4 793.8,91.4 794.4,91.3 795.0,91.2 795.6,91.0 796.2,90.8 796.8,90.6 797.4,90.5 798.0,90.3 798.6,90.2 799.2,90.1 799.8,90.1 800.4,90.1 801.0,90.1 801.6,90.1 802.2,90.1 802.8,90.0 803.4,90.0 804.0,89.9 804.6,89.7 805.2,89.5 805.8,89.3 806.4,89.0 807.0,88.8 807.6,88.5 808.2,88.3 808.8,88.2 809.4,88.1 810.0,88.2 810.6,88.3 811.2,88.6 811.8,88.9 812.4,89.3 813.0,89.8 813.6,90.4 814.2,91.0 814.8,91.5 815.4,92.0 816.0,92.4 816.6,92.7 817.2,92.9 817.8,92.9 818.4,92.8 819.0,92.5 819.6,92.1 820.2,91.7 820.8,91.3 821.4,91.2 822.0,91.4 822.6,91.2 823.2,89.2 823.8,84.2 824.4,75.8 825.0,64.2 825.6,50.4 826.2,36.9 826.8,27.4 827.4,25.2 828.0,31.3 828.6,44.0 829.2,59.7 829.8,74.7 830.4,86.8 831.0,95.0 831.6,99.5 832.2,100.9 832.8,100.1 833.4,98.2 834.0,95.9 834.6,94.0 835.2,92.6 835.8,91.8 836.4,91.2 837.0,90.9 837.6,90.7 838.2,90.5 838.8,90.4 839.4,90.4 840.0,90.3 840.6,90.3 841.2,90.3 841.8,90.4 842.4,90.4 843.0,90.3 843.6,90.3 844.2,90.2 844.8,90.0 845.4,89.8 846.0,89.5 846.6,89.2 847.2,88.9 847.8,88.6 848.4,88.3 849.0,88.1 849.6,87.9 850.2,87.8 850.8,87.9 851.4,88.0 852.0,88.2 852.6,88.5 853.2,88.9 853.8,89.4 854.4,89.9 855.0,90.3 855.6,90.8 856.2,91.1 856.8,91.3 857.4,91.3 858.0,91.2 858.6,90.8 859.2,90.3 859.8,89.5 860.4,88.6 861.0,87.5 861.6,86.2 862.2,84.9 862.8,83.5 863.4,82.0 864.0,80.6 864.6,79.3 865.2,78.0 865.8,76.9 866.4,75.9 867.0,75.1 867.6,74.4 868.2,73.9 868.8,73.5 869.4,73.3 870.0,73.3 870.6,73.3 871.2,73.4 871.8,73.6 872.4,73.9 873.0,74.3 873.6,74.6 874.2,75.1 874.8,75.5 875.4,76.1 876.0,76.6 876.6,77.3 877.2,77.9 877.8,78.7 878.4,79.5 879.0,80.3 879.6,81.2 880.2,82.1 880.8,83.0 881.4,83.8 882.0,84.7 882.6,85.4 883.2,86.1 883.8,86.8 884.4,87.6 885.0,88.6 885.6,89.7 886.2,89.8 886.8,87.7 887.4,82.3 888.0,73.2 888.6,60.9 889.2,46.8 889.8,33.8 890.4,25.8 891.0,25.5 891.6,33.4 892.2,47.1 892.8,62.8 893.4,77.2 894.0,88.3 894.6,95.6 895.2,99.5 895.8,100.6 896.4,99.8 897.0,98.2 897.6,96.4 898.2,95.0 898.8,94.0 899.4,93.4 900.0,93.0\"/><text class=\"cap\" x=\"4\" y=\"193\">리듬 스트립 · 25 mm/s, 10 mm/mV</text></svg>"
 },
 {
  "id": "usmle-2026-0033",
  "exam": "usmle",
  "step": "Step 2",
  "subject": "Internal Medicine",
  "subject_file": "Internal Medicine",
  "subtopic": "Normal Sinus Rhythm (real ECG from open DB)",
  "type": "Normal Sinus Rhythm (real ECG from open DB)",
  "difficulty": 2,
  "created": "2026-07-07",
  "vignette": "A 45-year-old man has a routine preoperative electrocardiogram. He is asymptomatic and hemodynamically stable. The rhythm strip shown is recorded.",
  "question": "Which of the following best describes the underlying rhythm?",
  "options": [
   "Atrial fibrillation",
   "Normal sinus rhythm",
   "Atrial flutter",
   "Junctional rhythm",
   "Third-degree atrioventricular block"
  ],
  "answer": 2,
  "explanationText": "- 적용(심전도 판독 → 진단): RR 간격이 규칙적이고, 각 QRS 앞에 일정한\n  형태의 P파가 선행하며, QRS 폭이 좁다 → 정상 동율동(normal sinus rhythm).\n- 오답감별: (A) 심방세동은 P파 소실 + RR 불규칙. (C) 심방조동은 톱니\n  (sawtooth) F파. (D) 접합부율동은 P파 소실 또는 역행성 P. (E) 완전방실차단\n  은 P파와 QRS가 서로 무관하게 행진(방실 해리).\n- 임상핵심: NSR 정의 = 모든 QRS 앞 정상 P파 · 규칙적 · 60–100회/분. 판독은\n  ①리듬 규칙성 ②P파 유무·관계 ③QRS 폭 순으로 본다.\n- 자료 관련: 이 심전도는 수식 합성이 아니라 오픈 신호 DB(MIT-BIH, ODC-BY)의\n  실제 파형을 렌더한 것이다(`assets/ecg/*.json` → `render_signal_svg`).\n- 출처: clinical electrocardiography; MIT-BIH Arrhythmia DB.",
  "explanationItems": [
   {
    "k": "적용(심전도 판독 → 진단)",
    "v": "RR 간격이 규칙적이고, 각 QRS 앞에 일정한 형태의 P파가 선행하며, QRS 폭이 좁다 → 정상 동율동(normal sinus rhythm)."
   },
   {
    "k": "오답감별",
    "v": "(A) 심방세동은 P파 소실 + RR 불규칙. (C) 심방조동은 톱니 (sawtooth) F파. (D) 접합부율동은 P파 소실 또는 역행성 P. (E) 완전방실차단 은 P파와 QRS가 서로 무관하게 행진(방실 해리)."
   },
   {
    "k": "임상핵심",
    "v": "NSR 정의 = 모든 QRS 앞 정상 P파 · 규칙적 · 60–100회/분. 판독은 ①리듬 규칙성 ②P파 유무·관계 ③QRS 폭 순으로 본다."
   },
   {
    "k": "자료 관련",
    "v": "이 심전도는 수식 합성이 아니라 오픈 신호 DB(MIT-BIH, ODC-BY)의 실제 파형을 렌더한 것이다(`assets/ecg/*.json` → `render_signal_svg`)."
   },
   {
    "k": "출처",
    "v": "clinical electrocardiography; MIT-BIH Arrhythmia DB."
   }
  ],
  "source": "USMLE-style / MedKOS · ECG: MIT-BIH Arrhythmia DB (ODC-BY)",
  "vitals": [],
  "labs": [],
  "appendix": {
   "최신지견": "정상 동율동의 정의 = 모든 QRS 앞에 정상 P파 · 규칙적 · 심박수 60–100회/분.",
   "참고문헌": [
    "MIT-BIH Arrhythmia Database (PhysioNet, ODC-BY 1.0)"
   ]
  },
  "figureSvg": "<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 900 198\" width=\"900\" height=\"198\" role=\"img\" aria-label=\"ECG 실제 심전도(오픈 DB) · MIT-BIH #100 · MLII · 25 mm/s, 10 mm/mV\"><style>.bg{fill:#fff}.gmin{stroke:#f4c9c9;stroke-width:0.5}.gmaj{stroke:#e59a9a;stroke-width:1}.trace{fill:none;stroke:#111;stroke-width:1.4;stroke-linejoin:round}.cap{font:11px -apple-system,Segoe UI,sans-serif;fill:#555}</style><rect class=\"bg\" x=\"0\" y=\"0\" width=\"900\" height=\"180\"/><line x1=\"0\" y1=\"0\" x2=\"0\" y2=\"180\" class=\"gmaj\"/><line x1=\"6\" y1=\"0\" x2=\"6\" y2=\"180\" class=\"gmin\"/><line x1=\"12\" y1=\"0\" x2=\"12\" y2=\"180\" class=\"gmin\"/><line x1=\"18\" y1=\"0\" x2=\"18\" y2=\"180\" class=\"gmin\"/><line x1=\"24\" y1=\"0\" x2=\"24\" y2=\"180\" class=\"gmin\"/><line x1=\"30\" y1=\"0\" x2=\"30\" y2=\"180\" class=\"gmaj\"/><line x1=\"36\" y1=\"0\" x2=\"36\" y2=\"180\" class=\"gmin\"/><line x1=\"42\" y1=\"0\" x2=\"42\" y2=\"180\" class=\"gmin\"/><line x1=\"48\" y1=\"0\" x2=\"48\" y2=\"180\" class=\"gmin\"/><line x1=\"54\" y1=\"0\" x2=\"54\" y2=\"180\" class=\"gmin\"/><line x1=\"60\" y1=\"0\" x2=\"60\" y2=\"180\" class=\"gmaj\"/><line x1=\"66\" y1=\"0\" x2=\"66\" y2=\"180\" class=\"gmin\"/><line x1=\"72\" y1=\"0\" x2=\"72\" y2=\"180\" class=\"gmin\"/><line x1=\"78\" y1=\"0\" x2=\"78\" y2=\"180\" class=\"gmin\"/><line x1=\"84\" y1=\"0\" x2=\"84\" y2=\"180\" class=\"gmin\"/><line x1=\"90\" y1=\"0\" x2=\"90\" y2=\"180\" class=\"gmaj\"/><line x1=\"96\" y1=\"0\" x2=\"96\" y2=\"180\" class=\"gmin\"/><line x1=\"102\" y1=\"0\" x2=\"102\" y2=\"180\" class=\"gmin\"/><line x1=\"108\" y1=\"0\" x2=\"108\" y2=\"180\" class=\"gmin\"/><line x1=\"114\" y1=\"0\" x2=\"114\" y2=\"180\" class=\"gmin\"/><line x1=\"120\" y1=\"0\" x2=\"120\" y2=\"180\" class=\"gmaj\"/><line x1=\"126\" y1=\"0\" x2=\"126\" y2=\"180\" class=\"gmin\"/><line x1=\"132\" y1=\"0\" x2=\"132\" y2=\"180\" class=\"gmin\"/><line x1=\"138\" y1=\"0\" x2=\"138\" y2=\"180\" class=\"gmin\"/><line x1=\"144\" y1=\"0\" x2=\"144\" y2=\"180\" class=\"gmin\"/><line x1=\"150\" y1=\"0\" x2=\"150\" y2=\"180\" class=\"gmaj\"/><line x1=\"156\" y1=\"0\" x2=\"156\" y2=\"180\" class=\"gmin\"/><line x1=\"162\" y1=\"0\" x2=\"162\" y2=\"180\" class=\"gmin\"/><line x1=\"168\" y1=\"0\" x2=\"168\" y2=\"180\" class=\"gmin\"/><line x1=\"174\" y1=\"0\" x2=\"174\" y2=\"180\" class=\"gmin\"/><line x1=\"180\" y1=\"0\" x2=\"180\" y2=\"180\" class=\"gmaj\"/><line x1=\"186\" y1=\"0\" x2=\"186\" y2=\"180\" class=\"gmin\"/><line x1=\"192\" y1=\"0\" x2=\"192\" y2=\"180\" class=\"gmin\"/><line x1=\"198\" y1=\"0\" x2=\"198\" y2=\"180\" class=\"gmin\"/><line x1=\"204\" y1=\"0\" x2=\"204\" y2=\"180\" class=\"gmin\"/><line x1=\"210\" y1=\"0\" x2=\"210\" y2=\"180\" class=\"gmaj\"/><line x1=\"216\" y1=\"0\" x2=\"216\" y2=\"180\" class=\"gmin\"/><line x1=\"222\" y1=\"0\" x2=\"222\" y2=\"180\" class=\"gmin\"/><line x1=\"228\" y1=\"0\" x2=\"228\" y2=\"180\" class=\"gmin\"/><line x1=\"234\" y1=\"0\" x2=\"234\" y2=\"180\" class=\"gmin\"/><line x1=\"240\" y1=\"0\" x2=\"240\" y2=\"180\" class=\"gmaj\"/><line x1=\"246\" y1=\"0\" x2=\"246\" y2=\"180\" class=\"gmin\"/><line x1=\"252\" y1=\"0\" x2=\"252\" y2=\"180\" class=\"gmin\"/><line x1=\"258\" y1=\"0\" x2=\"258\" y2=\"180\" class=\"gmin\"/><line x1=\"264\" y1=\"0\" x2=\"264\" y2=\"180\" class=\"gmin\"/><line x1=\"270\" y1=\"0\" x2=\"270\" y2=\"180\" class=\"gmaj\"/><line x1=\"276\" y1=\"0\" x2=\"276\" y2=\"180\" class=\"gmin\"/><line x1=\"282\" y1=\"0\" x2=\"282\" y2=\"180\" class=\"gmin\"/><line x1=\"288\" y1=\"0\" x2=\"288\" y2=\"180\" class=\"gmin\"/><line x1=\"294\" y1=\"0\" x2=\"294\" y2=\"180\" class=\"gmin\"/><line x1=\"300\" y1=\"0\" x2=\"300\" y2=\"180\" class=\"gmaj\"/><line x1=\"306\" y1=\"0\" x2=\"306\" y2=\"180\" class=\"gmin\"/><line x1=\"312\" y1=\"0\" x2=\"312\" y2=\"180\" class=\"gmin\"/><line x1=\"318\" y1=\"0\" x2=\"318\" y2=\"180\" class=\"gmin\"/><line x1=\"324\" y1=\"0\" x2=\"324\" y2=\"180\" class=\"gmin\"/><line x1=\"330\" y1=\"0\" x2=\"330\" y2=\"180\" class=\"gmaj\"/><line x1=\"336\" y1=\"0\" x2=\"336\" y2=\"180\" class=\"gmin\"/><line x1=\"342\" y1=\"0\" x2=\"342\" y2=\"180\" class=\"gmin\"/><line x1=\"348\" y1=\"0\" x2=\"348\" y2=\"180\" class=\"gmin\"/><line x1=\"354\" y1=\"0\" x2=\"354\" y2=\"180\" class=\"gmin\"/><line x1=\"360\" y1=\"0\" x2=\"360\" y2=\"180\" class=\"gmaj\"/><line x1=\"366\" y1=\"0\" x2=\"366\" y2=\"180\" class=\"gmin\"/><line x1=\"372\" y1=\"0\" x2=\"372\" y2=\"180\" class=\"gmin\"/><line x1=\"378\" y1=\"0\" x2=\"378\" y2=\"180\" class=\"gmin\"/><line x1=\"384\" y1=\"0\" x2=\"384\" y2=\"180\" class=\"gmin\"/><line x1=\"390\" y1=\"0\" x2=\"390\" y2=\"180\" class=\"gmaj\"/><line x1=\"396\" y1=\"0\" x2=\"396\" y2=\"180\" class=\"gmin\"/><line x1=\"402\" y1=\"0\" x2=\"402\" y2=\"180\" class=\"gmin\"/><line x1=\"408\" y1=\"0\" x2=\"408\" y2=\"180\" class=\"gmin\"/><line x1=\"414\" y1=\"0\" x2=\"414\" y2=\"180\" class=\"gmin\"/><line x1=\"420\" y1=\"0\" x2=\"420\" y2=\"180\" class=\"gmaj\"/><line x1=\"426\" y1=\"0\" x2=\"426\" y2=\"180\" class=\"gmin\"/><line x1=\"432\" y1=\"0\" x2=\"432\" y2=\"180\" class=\"gmin\"/><line x1=\"438\" y1=\"0\" x2=\"438\" y2=\"180\" class=\"gmin\"/><line x1=\"444\" y1=\"0\" x2=\"444\" y2=\"180\" class=\"gmin\"/><line x1=\"450\" y1=\"0\" x2=\"450\" y2=\"180\" class=\"gmaj\"/><line x1=\"456\" y1=\"0\" x2=\"456\" y2=\"180\" class=\"gmin\"/><line x1=\"462\" y1=\"0\" x2=\"462\" y2=\"180\" class=\"gmin\"/><line x1=\"468\" y1=\"0\" x2=\"468\" y2=\"180\" class=\"gmin\"/><line x1=\"474\" y1=\"0\" x2=\"474\" y2=\"180\" class=\"gmin\"/><line x1=\"480\" y1=\"0\" x2=\"480\" y2=\"180\" class=\"gmaj\"/><line x1=\"486\" y1=\"0\" x2=\"486\" y2=\"180\" class=\"gmin\"/><line x1=\"492\" y1=\"0\" x2=\"492\" y2=\"180\" class=\"gmin\"/><line x1=\"498\" y1=\"0\" x2=\"498\" y2=\"180\" class=\"gmin\"/><line x1=\"504\" y1=\"0\" x2=\"504\" y2=\"180\" class=\"gmin\"/><line x1=\"510\" y1=\"0\" x2=\"510\" y2=\"180\" class=\"gmaj\"/><line x1=\"516\" y1=\"0\" x2=\"516\" y2=\"180\" class=\"gmin\"/><line x1=\"522\" y1=\"0\" x2=\"522\" y2=\"180\" class=\"gmin\"/><line x1=\"528\" y1=\"0\" x2=\"528\" y2=\"180\" class=\"gmin\"/><line x1=\"534\" y1=\"0\" x2=\"534\" y2=\"180\" class=\"gmin\"/><line x1=\"540\" y1=\"0\" x2=\"540\" y2=\"180\" class=\"gmaj\"/><line x1=\"546\" y1=\"0\" x2=\"546\" y2=\"180\" class=\"gmin\"/><line x1=\"552\" y1=\"0\" x2=\"552\" y2=\"180\" class=\"gmin\"/><line x1=\"558\" y1=\"0\" x2=\"558\" y2=\"180\" class=\"gmin\"/><line x1=\"564\" y1=\"0\" x2=\"564\" y2=\"180\" class=\"gmin\"/><line x1=\"570\" y1=\"0\" x2=\"570\" y2=\"180\" class=\"gmaj\"/><line x1=\"576\" y1=\"0\" x2=\"576\" y2=\"180\" class=\"gmin\"/><line x1=\"582\" y1=\"0\" x2=\"582\" y2=\"180\" class=\"gmin\"/><line x1=\"588\" y1=\"0\" x2=\"588\" y2=\"180\" class=\"gmin\"/><line x1=\"594\" y1=\"0\" x2=\"594\" y2=\"180\" class=\"gmin\"/><line x1=\"600\" y1=\"0\" x2=\"600\" y2=\"180\" class=\"gmaj\"/><line x1=\"606\" y1=\"0\" x2=\"606\" y2=\"180\" class=\"gmin\"/><line x1=\"612\" y1=\"0\" x2=\"612\" y2=\"180\" class=\"gmin\"/><line x1=\"618\" y1=\"0\" x2=\"618\" y2=\"180\" class=\"gmin\"/><line x1=\"624\" y1=\"0\" x2=\"624\" y2=\"180\" class=\"gmin\"/><line x1=\"630\" y1=\"0\" x2=\"630\" y2=\"180\" class=\"gmaj\"/><line x1=\"636\" y1=\"0\" x2=\"636\" y2=\"180\" class=\"gmin\"/><line x1=\"642\" y1=\"0\" x2=\"642\" y2=\"180\" class=\"gmin\"/><line x1=\"648\" y1=\"0\" x2=\"648\" y2=\"180\" class=\"gmin\"/><line x1=\"654\" y1=\"0\" x2=\"654\" y2=\"180\" class=\"gmin\"/><line x1=\"660\" y1=\"0\" x2=\"660\" y2=\"180\" class=\"gmaj\"/><line x1=\"666\" y1=\"0\" x2=\"666\" y2=\"180\" class=\"gmin\"/><line x1=\"672\" y1=\"0\" x2=\"672\" y2=\"180\" class=\"gmin\"/><line x1=\"678\" y1=\"0\" x2=\"678\" y2=\"180\" class=\"gmin\"/><line x1=\"684\" y1=\"0\" x2=\"684\" y2=\"180\" class=\"gmin\"/><line x1=\"690\" y1=\"0\" x2=\"690\" y2=\"180\" class=\"gmaj\"/><line x1=\"696\" y1=\"0\" x2=\"696\" y2=\"180\" class=\"gmin\"/><line x1=\"702\" y1=\"0\" x2=\"702\" y2=\"180\" class=\"gmin\"/><line x1=\"708\" y1=\"0\" x2=\"708\" y2=\"180\" class=\"gmin\"/><line x1=\"714\" y1=\"0\" x2=\"714\" y2=\"180\" class=\"gmin\"/><line x1=\"720\" y1=\"0\" x2=\"720\" y2=\"180\" class=\"gmaj\"/><line x1=\"726\" y1=\"0\" x2=\"726\" y2=\"180\" class=\"gmin\"/><line x1=\"732\" y1=\"0\" x2=\"732\" y2=\"180\" class=\"gmin\"/><line x1=\"738\" y1=\"0\" x2=\"738\" y2=\"180\" class=\"gmin\"/><line x1=\"744\" y1=\"0\" x2=\"744\" y2=\"180\" class=\"gmin\"/><line x1=\"750\" y1=\"0\" x2=\"750\" y2=\"180\" class=\"gmaj\"/><line x1=\"756\" y1=\"0\" x2=\"756\" y2=\"180\" class=\"gmin\"/><line x1=\"762\" y1=\"0\" x2=\"762\" y2=\"180\" class=\"gmin\"/><line x1=\"768\" y1=\"0\" x2=\"768\" y2=\"180\" class=\"gmin\"/><line x1=\"774\" y1=\"0\" x2=\"774\" y2=\"180\" class=\"gmin\"/><line x1=\"780\" y1=\"0\" x2=\"780\" y2=\"180\" class=\"gmaj\"/><line x1=\"786\" y1=\"0\" x2=\"786\" y2=\"180\" class=\"gmin\"/><line x1=\"792\" y1=\"0\" x2=\"792\" y2=\"180\" class=\"gmin\"/><line x1=\"798\" y1=\"0\" x2=\"798\" y2=\"180\" class=\"gmin\"/><line x1=\"804\" y1=\"0\" x2=\"804\" y2=\"180\" class=\"gmin\"/><line x1=\"810\" y1=\"0\" x2=\"810\" y2=\"180\" class=\"gmaj\"/><line x1=\"816\" y1=\"0\" x2=\"816\" y2=\"180\" class=\"gmin\"/><line x1=\"822\" y1=\"0\" x2=\"822\" y2=\"180\" class=\"gmin\"/><line x1=\"828\" y1=\"0\" x2=\"828\" y2=\"180\" class=\"gmin\"/><line x1=\"834\" y1=\"0\" x2=\"834\" y2=\"180\" class=\"gmin\"/><line x1=\"840\" y1=\"0\" x2=\"840\" y2=\"180\" class=\"gmaj\"/><line x1=\"846\" y1=\"0\" x2=\"846\" y2=\"180\" class=\"gmin\"/><line x1=\"852\" y1=\"0\" x2=\"852\" y2=\"180\" class=\"gmin\"/><line x1=\"858\" y1=\"0\" x2=\"858\" y2=\"180\" class=\"gmin\"/><line x1=\"864\" y1=\"0\" x2=\"864\" y2=\"180\" class=\"gmin\"/><line x1=\"870\" y1=\"0\" x2=\"870\" y2=\"180\" class=\"gmaj\"/><line x1=\"876\" y1=\"0\" x2=\"876\" y2=\"180\" class=\"gmin\"/><line x1=\"882\" y1=\"0\" x2=\"882\" y2=\"180\" class=\"gmin\"/><line x1=\"888\" y1=\"0\" x2=\"888\" y2=\"180\" class=\"gmin\"/><line x1=\"894\" y1=\"0\" x2=\"894\" y2=\"180\" class=\"gmin\"/><line x1=\"900\" y1=\"0\" x2=\"900\" y2=\"180\" class=\"gmaj\"/><line x1=\"0\" y1=\"0\" x2=\"900\" y2=\"0\" class=\"gmaj\"/><line x1=\"0\" y1=\"6\" x2=\"900\" y2=\"6\" class=\"gmin\"/><line x1=\"0\" y1=\"12\" x2=\"900\" y2=\"12\" class=\"gmin\"/><line x1=\"0\" y1=\"18\" x2=\"900\" y2=\"18\" class=\"gmin\"/><line x1=\"0\" y1=\"24\" x2=\"900\" y2=\"24\" class=\"gmin\"/><line x1=\"0\" y1=\"30\" x2=\"900\" y2=\"30\" class=\"gmaj\"/><line x1=\"0\" y1=\"36\" x2=\"900\" y2=\"36\" class=\"gmin\"/><line x1=\"0\" y1=\"42\" x2=\"900\" y2=\"42\" class=\"gmin\"/><line x1=\"0\" y1=\"48\" x2=\"900\" y2=\"48\" class=\"gmin\"/><line x1=\"0\" y1=\"54\" x2=\"900\" y2=\"54\" class=\"gmin\"/><line x1=\"0\" y1=\"60\" x2=\"900\" y2=\"60\" class=\"gmaj\"/><line x1=\"0\" y1=\"66\" x2=\"900\" y2=\"66\" class=\"gmin\"/><line x1=\"0\" y1=\"72\" x2=\"900\" y2=\"72\" class=\"gmin\"/><line x1=\"0\" y1=\"78\" x2=\"900\" y2=\"78\" class=\"gmin\"/><line x1=\"0\" y1=\"84\" x2=\"900\" y2=\"84\" class=\"gmin\"/><line x1=\"0\" y1=\"90\" x2=\"900\" y2=\"90\" class=\"gmaj\"/><line x1=\"0\" y1=\"96\" x2=\"900\" y2=\"96\" class=\"gmin\"/><line x1=\"0\" y1=\"102\" x2=\"900\" y2=\"102\" class=\"gmin\"/><line x1=\"0\" y1=\"108\" x2=\"900\" y2=\"108\" class=\"gmin\"/><line x1=\"0\" y1=\"114\" x2=\"900\" y2=\"114\" class=\"gmin\"/><line x1=\"0\" y1=\"120\" x2=\"900\" y2=\"120\" class=\"gmaj\"/><line x1=\"0\" y1=\"126\" x2=\"900\" y2=\"126\" class=\"gmin\"/><line x1=\"0\" y1=\"132\" x2=\"900\" y2=\"132\" class=\"gmin\"/><line x1=\"0\" y1=\"138\" x2=\"900\" y2=\"138\" class=\"gmin\"/><line x1=\"0\" y1=\"144\" x2=\"900\" y2=\"144\" class=\"gmin\"/><line x1=\"0\" y1=\"150\" x2=\"900\" y2=\"150\" class=\"gmaj\"/><line x1=\"0\" y1=\"156\" x2=\"900\" y2=\"156\" class=\"gmin\"/><line x1=\"0\" y1=\"162\" x2=\"900\" y2=\"162\" class=\"gmin\"/><line x1=\"0\" y1=\"168\" x2=\"900\" y2=\"168\" class=\"gmin\"/><line x1=\"0\" y1=\"174\" x2=\"900\" y2=\"174\" class=\"gmin\"/><line x1=\"0\" y1=\"180\" x2=\"900\" y2=\"180\" class=\"gmaj\"/><polyline class=\"trace\" points=\"0.0,78.0 0.4,78.0 0.8,78.0 1.2,78.0 1.7,78.0 2.1,78.0 2.5,78.0 2.9,78.0 3.3,76.5 3.8,77.4 4.2,78.0 4.6,78.3 5.0,78.9 5.4,78.6 5.8,78.9 6.2,79.8 6.7,80.1 7.1,80.4 7.5,79.5 7.9,78.6 8.3,79.8 8.8,80.1 9.2,80.7 9.6,80.1 10.0,78.6 10.4,77.4 10.8,78.6 11.2,80.7 11.7,81.6 12.1,83.4 12.5,82.8 12.9,84.0 13.3,84.3 13.7,84.9 14.2,85.8 14.6,85.8 15.0,85.8 15.4,85.2 15.8,84.6 16.2,85.2 16.7,85.8 17.1,86.7 17.5,86.7 17.9,86.7 18.3,86.7 18.8,86.4 19.2,87.0 19.6,87.6 20.0,86.4 20.4,85.8 20.8,85.8 21.2,86.1 21.7,86.4 22.1,87.6 22.5,86.7 22.9,87.3 23.3,86.1 23.8,86.7 24.2,87.3 24.6,88.2 25.0,88.5 25.4,89.4 25.8,90.9 26.2,92.4 26.7,92.4 27.1,93.6 27.5,96.6 27.9,98.4 28.3,98.4 28.8,94.8 29.2,89.1 29.6,82.5 30.0,73.5 30.4,62.1 30.8,46.8 31.2,32.1 31.7,22.5 32.1,18.9 32.5,23.4 32.9,38.1 33.3,59.1 33.8,79.2 34.2,91.2 34.6,95.4 35.0,94.8 35.4,91.5 35.8,89.1 36.2,88.8 36.7,89.4 37.1,90.0 37.5,89.1 37.9,88.8 38.3,88.2 38.8,87.9 39.2,88.5 39.6,89.4 40.0,89.7 40.4,88.8 40.8,90.0 41.2,89.4 41.7,89.1 42.1,89.4 42.5,89.1 42.9,88.8 43.3,89.1 43.8,89.1 44.2,90.0 44.6,90.6 45.0,89.4 45.4,88.8 45.8,87.6 46.2,88.5 46.7,88.5 47.1,89.1 47.5,89.7 47.9,89.4 48.3,89.7 48.8,90.0 49.2,90.6 49.6,90.6 50.0,89.7 50.4,89.1 50.8,89.1 51.2,89.1 51.7,89.7 52.1,90.3 52.5,88.8 52.9,88.8 53.3,89.1 53.8,89.1 54.2,89.4 54.6,89.4 55.0,89.7 55.4,89.1 55.8,89.7 56.2,90.3 56.7,90.6 57.1,90.3 57.5,90.0 57.9,89.1 58.3,88.5 58.8,89.4 59.2,89.1 59.6,90.0 60.0,89.1 60.4,89.4 60.8,89.4 61.2,90.0 61.7,90.0 62.1,90.6 62.5,89.7 62.9,89.7 63.3,89.4 63.8,89.1 64.2,90.3 64.6,90.3 65.0,90.0 65.4,89.4 65.8,89.4 66.2,89.4 66.7,90.3 67.1,90.6 67.5,90.6 67.9,90.0 68.3,90.0 68.8,89.4 69.2,90.3 69.6,90.9 70.0,90.9 70.4,90.9 70.8,91.2 71.2,90.9 71.7,91.5 72.1,92.4 72.5,91.5 72.9,90.9 73.3,90.6 73.8,90.9 74.2,91.8 74.6,91.8 75.0,91.2 75.4,91.2 75.8,90.9 76.2,90.9 76.7,91.2 77.1,91.5 77.5,90.6 77.9,89.1 78.3,88.8 78.8,88.8 79.2,89.4 79.6,89.7 80.0,88.2 80.4,87.3 80.8,87.3 81.2,86.7 81.7,87.0 82.1,86.7 82.5,86.4 82.9,85.8 83.3,84.6 83.8,84.3 84.2,84.3 84.6,85.2 85.0,84.6 85.4,84.0 85.8,83.1 86.2,84.0 86.7,84.0 87.1,84.6 87.5,84.6 87.9,83.7 88.3,84.3 88.8,84.6 89.2,84.0 89.6,84.6 90.0,84.3 90.4,84.3 90.8,85.2 91.2,84.9 91.7,84.9 92.1,85.2 92.5,85.5 92.9,85.2 93.3,84.9 93.8,85.8 94.2,86.1 94.6,86.7 95.0,85.8 95.4,85.5 95.8,84.9 96.3,86.1 96.7,86.1 97.1,86.4 97.5,85.8 97.9,85.8 98.3,85.2 98.8,85.5 99.2,86.4 99.6,86.7 100.0,86.1 100.4,85.8 100.8,86.4 101.2,86.1 101.7,87.3 102.1,87.3 102.5,87.6 102.9,87.0 103.3,87.3 103.8,87.9 104.2,87.9 104.6,87.6 105.0,87.0 105.4,86.4 105.8,86.4 106.2,86.7 106.7,87.0 107.1,87.9 107.5,86.7 107.9,87.0 108.3,87.3 108.8,87.6 109.2,87.9 109.6,88.8 110.0,87.9 110.4,87.3 110.8,86.7 111.2,87.9 111.7,88.8 112.1,89.1 112.5,88.2 112.9,87.3 113.3,87.6 113.8,87.9 114.2,88.5 114.6,89.1 115.0,88.8 115.4,88.2 115.8,87.9 116.2,87.6 116.7,87.6 117.1,87.9 117.5,87.3 117.9,87.6 118.3,86.7 118.8,87.3 119.2,87.3 119.6,87.6 120.0,87.6 120.4,86.7 120.8,86.1 121.2,87.0 121.7,87.6 122.1,88.2 122.5,87.6 122.9,87.0 123.3,86.7 123.8,86.1 124.2,85.5 124.6,85.8 125.0,85.8 125.4,85.5 125.8,84.3 126.2,84.3 126.7,84.6 127.1,82.8 127.5,82.5 127.9,81.6 128.3,81.3 128.8,81.6 129.2,82.2 129.6,83.1 130.0,82.5 130.4,82.8 130.8,82.8 131.2,82.8 131.7,83.1 132.1,83.4 132.5,83.7 132.9,83.4 133.3,82.5 133.8,81.9 134.2,81.6 134.6,84.0 135.0,86.4 135.4,86.4 135.8,87.3 136.2,87.9 136.7,89.1 137.1,89.1 137.5,88.8 137.9,88.2 138.3,88.5 138.8,88.2 139.2,88.8 139.6,89.7 140.0,90.0 140.4,89.7 140.8,89.7 141.2,90.3 141.7,90.0 142.1,90.6 142.5,89.1 142.9,89.4 143.3,89.1 143.8,88.5 144.2,90.0 144.6,90.6 145.0,89.7 145.4,89.1 145.8,88.8 146.2,89.1 146.7,90.3 147.1,91.2 147.5,90.9 147.9,92.1 148.3,94.8 148.8,96.0 149.2,97.8 149.6,99.9 150.0,101.4 150.4,99.6 150.8,94.2 151.2,87.3 151.7,78.9 152.1,70.2 152.5,55.2 152.9,39.9 153.3,26.1 153.8,16.8 154.2,12.9 154.6,15.0 155.0,24.0 155.4,39.9 155.8,59.4 156.2,75.9 156.7,85.5 157.1,92.7 157.5,96.3 157.9,97.8 158.3,96.6 158.8,94.8 159.2,92.7 159.6,92.7 160.0,92.4 160.4,92.7 160.8,92.1 161.2,92.1 161.7,92.1 162.1,93.0 162.5,92.4 162.9,92.4 163.3,92.4 163.7,91.8 164.2,93.0 164.6,93.9 165.0,93.9 165.4,93.3 165.8,93.0 166.2,92.7 166.7,93.6 167.1,93.0 167.5,92.4 167.9,91.8 168.3,92.7 168.8,92.7 169.2,93.6 169.6,93.9 170.0,93.9 170.4,92.7 170.8,92.7 171.2,93.0 171.7,93.6 172.1,94.2 172.5,93.3 172.9,93.9 173.3,93.6 173.8,93.9 174.2,94.2 174.6,93.9 175.0,93.3 175.4,93.3 175.8,93.0 176.2,92.7 176.7,93.6 177.1,93.9 177.5,92.7 177.9,92.7 178.3,92.4 178.8,92.4 179.2,93.9 179.6,93.6 180.0,93.0 180.4,92.7 180.8,91.8 181.2,92.7 181.7,93.0 182.1,93.9 182.5,93.3 182.9,92.7 183.3,92.7 183.8,92.4 184.2,93.6 184.6,94.2 185.0,94.2 185.4,93.3 185.8,93.0 186.2,93.6 186.7,94.2 187.1,94.5 187.5,94.5 187.9,93.9 188.3,94.2 188.8,94.8 189.2,94.5 189.6,95.4 190.0,95.1 190.4,95.1 190.8,94.5 191.2,95.1 191.7,96.3 192.1,96.6 192.5,96.3 192.9,95.4 193.3,96.0 193.8,96.3 194.2,96.6 194.6,97.5 195.0,96.9 195.4,96.6 195.8,96.3 196.2,96.6 196.7,97.5 197.1,97.8 197.5,96.9 197.9,96.3 198.3,96.0 198.8,95.7 199.2,95.4 199.6,95.7 200.0,93.9 200.4,93.0 200.8,91.5 201.2,91.2 201.7,90.9 202.1,91.2 202.5,89.7 202.9,88.8 203.3,88.2 203.8,88.5 204.2,89.1 204.6,89.1 205.0,88.5 205.4,87.9 205.8,87.3 206.2,87.3 206.7,88.5 207.1,88.5 207.5,88.2 207.9,87.6 208.3,87.6 208.8,87.0 209.2,88.5 209.6,89.1 210.0,87.6 210.4,87.9 210.8,87.3 211.3,87.3 211.7,88.5 212.1,88.8 212.5,87.9 212.9,87.6 213.3,88.2 213.8,87.6 214.2,88.2 214.6,88.2 215.0,87.9 215.4,87.0 215.8,86.7 216.2,87.6 216.7,87.9 217.1,88.5 217.5,88.2 217.9,87.3 218.3,88.2 218.8,88.2 219.2,88.2 219.6,89.1 220.0,88.2 220.4,88.5 220.8,88.2 221.2,88.8 221.7,89.4 222.1,89.7 222.5,89.4 222.9,89.4 223.3,89.1 223.8,88.8 224.2,90.0 224.6,90.3 225.0,90.0 225.4,89.4 225.8,89.1 226.2,89.1 226.7,90.0 227.1,90.0 227.5,90.0 227.9,88.5 228.3,89.1 228.8,89.4 229.2,89.7 229.6,90.6 230.0,89.4 230.4,89.1 230.8,89.1 231.2,89.4 231.7,90.6 232.1,90.9 232.5,90.6 232.9,90.3 233.3,89.7 233.8,90.0 234.2,90.0 234.6,90.0 235.0,90.0 235.4,89.1 235.8,89.1 236.2,89.4 236.7,90.0 237.1,90.3 237.5,90.3 237.9,89.7 238.3,89.1 238.7,90.0 239.2,90.0 239.6,90.6 240.0,90.3 240.4,89.7 240.8,89.1 241.2,89.7 241.7,89.7 242.1,89.7 242.5,89.1 242.9,89.4 243.3,89.1 243.8,89.4 244.2,90.0 244.6,90.0 245.0,89.7 245.4,89.1 245.8,88.2 246.2,87.0 246.7,87.3 247.1,87.0 247.5,86.4 247.9,85.8 248.3,85.2 248.8,85.2 249.2,85.2 249.6,84.6 250.0,84.3 250.4,83.7 250.8,82.8 251.2,82.2 251.7,83.7 252.1,84.0 252.5,83.7 252.9,84.0 253.3,83.4 253.8,84.0 254.2,84.3 254.6,85.8 255.0,85.8 255.4,85.2 255.8,84.3 256.2,82.8 256.7,82.5 257.1,83.1 257.5,85.2 257.9,85.5 258.3,86.1 258.8,86.4 259.2,87.6 259.6,88.5 260.0,89.7 260.4,89.1 260.8,89.4 261.2,89.4 261.7,90.6 262.1,91.5 262.5,90.9 262.9,90.0 263.3,90.3 263.8,90.6 264.2,91.2 264.6,91.8 265.0,92.1 265.4,91.5 265.8,91.2 266.2,91.2 266.7,92.1 267.1,92.4 267.5,92.1 267.9,91.8 268.3,90.6 268.8,91.5 269.2,92.7 269.6,93.6 270.0,93.9 270.4,95.4 270.8,97.2 271.2,98.7 271.7,100.5 272.1,102.6 272.5,103.5 272.9,100.8 273.3,93.6 273.8,84.3 274.2,74.7 274.6,62.1 275.0,44.7 275.4,27.9 275.8,16.2 276.2,11.7 276.7,18.3 277.1,38.1 277.5,66.3 277.9,88.5 278.3,99.3 278.8,99.6 279.2,96.0 279.6,94.2 280.0,93.0 280.4,92.7 280.8,93.0 281.2,92.7 281.7,93.0 282.1,93.6 282.5,93.0 282.9,93.6 283.3,92.7 283.8,93.0 284.2,93.0 284.6,93.9 285.0,93.6 285.4,93.3 285.8,93.3 286.2,94.2 286.7,93.6 287.1,94.5 287.5,94.2 287.9,93.6 288.3,93.6 288.8,94.5 289.2,94.5 289.6,95.4 290.0,94.5 290.4,93.9 290.8,93.9 291.2,93.6 291.7,94.8 292.1,95.1 292.5,94.5 292.9,94.2 293.3,93.9 293.8,93.9 294.2,94.8 294.6,94.5 295.0,93.3 295.4,93.0 295.8,93.3 296.2,93.3 296.7,93.0 297.1,94.2 297.5,93.6 297.9,92.7 298.3,93.3 298.8,93.3 299.2,94.2 299.6,94.8 300.0,94.8 300.4,94.2 300.8,94.2 301.2,93.9 301.7,94.8 302.1,94.8 302.5,94.5 302.9,94.2 303.3,93.3 303.8,93.3 304.2,93.9 304.6,94.8 305.0,93.9 305.4,93.6 305.8,93.0 306.2,93.3 306.7,93.3 307.1,93.6 307.5,92.4 307.9,93.3 308.3,92.7 308.7,92.7 309.2,93.3 309.6,94.2 310.0,93.6 310.4,93.6 310.8,93.9 311.2,94.2 311.7,94.5 312.1,94.5 312.5,94.8 312.9,94.2 313.3,94.2 313.8,93.9 314.2,95.4 314.6,95.1 315.0,95.4 315.4,94.5 315.8,94.5 316.2,94.5 316.7,94.5 317.1,94.8 317.5,94.8 317.9,94.2 318.3,93.0 318.8,93.0 319.2,92.7 319.6,91.8 320.0,90.9 320.4,89.7 320.8,89.4 321.2,89.1 321.7,89.4 322.1,89.4 322.5,88.8 322.9,88.5 323.3,87.6 323.8,87.6 324.2,88.2 324.6,87.9 325.0,87.6 325.4,87.3 325.8,87.3 326.2,87.3 326.7,87.9 327.1,87.9 327.5,87.9 327.9,88.2 328.3,87.3 328.8,87.6 329.2,88.2 329.6,88.5 330.0,88.8 330.4,87.9 330.8,87.6 331.2,87.6 331.7,88.5 332.1,88.8 332.5,87.6 332.9,87.9 333.3,87.0 333.8,87.9 334.2,88.8 334.6,89.1 335.0,88.5 335.4,88.5 335.8,88.5 336.2,88.8 336.7,90.3 337.1,90.3 337.5,89.7 337.9,89.4 338.3,89.1 338.8,89.4 339.2,89.7 339.6,90.9 340.0,90.3 340.4,90.3 340.8,90.6 341.2,90.9 341.7,90.6 342.1,91.2 342.5,90.6 342.9,90.3 343.3,89.7 343.8,90.6 344.2,90.3 344.6,91.2 345.0,91.2 345.4,90.3 345.8,90.6 346.2,90.3 346.7,91.5 347.1,92.1 347.5,91.5 347.9,90.9 348.3,91.2 348.8,90.9 349.2,91.2 349.6,92.1 350.0,91.5 350.4,91.2 350.8,90.3 351.2,90.3 351.7,90.3 352.1,91.5 352.5,91.2 352.9,90.0 353.3,90.0 353.8,89.7 354.2,90.6 354.6,91.2 355.0,90.9 355.4,90.6 355.8,90.6 356.2,90.6 356.7,91.8 357.1,92.4 357.5,90.6 357.9,90.9 358.3,90.6 358.8,90.9 359.2,90.9 359.6,91.5 360.0,90.9 360.4,90.0 360.8,90.6 361.2,90.0 361.7,90.0 362.1,90.0 362.5,89.7 362.9,87.9 363.3,87.6 363.8,87.6 364.2,87.9 364.6,87.6 365.0,86.7 365.4,86.4 365.8,85.8 366.3,86.1 366.7,86.1 367.1,85.8 367.5,85.2 367.9,84.6 368.3,84.0 368.8,84.9 369.2,85.2 369.6,85.8 370.0,86.1 370.4,85.2 370.8,85.5 371.2,85.8 371.7,86.1 372.1,85.8 372.5,86.1 372.9,85.8 373.3,85.2 373.8,84.6 374.2,83.7 374.6,84.9 375.0,86.1 375.4,87.9 375.8,87.9 376.2,90.0 376.7,90.9 377.1,92.1 377.5,92.4 377.9,92.1 378.3,91.5 378.8,91.8 379.2,92.4 379.6,92.7 380.0,93.0 380.4,92.4 380.8,92.4 381.2,92.4 381.7,93.0 382.1,93.6 382.5,93.3 382.9,91.8 383.3,91.8 383.7,92.7 384.2,93.0 384.6,94.2 385.0,93.6 385.4,93.3 385.8,92.7 386.2,93.6 386.7,94.8 387.1,96.9 387.5,97.8 387.9,99.6 388.3,99.9 388.8,100.8 389.2,101.7 389.6,105.3 390.0,108.0 390.4,107.1 390.8,103.8 391.2,99.0 391.7,92.4 392.1,85.5 392.5,76.2 392.9,63.9 393.3,47.1 393.8,31.2 394.2,20.7 394.6,17.7 395.0,23.1 395.4,40.8 395.8,65.4 396.2,87.6 396.7,99.3 397.1,100.5 397.5,97.8 397.9,93.9 398.3,92.7 398.8,92.7 399.2,93.3 399.6,93.9 400.0,93.6 400.4,92.4 400.8,92.7 401.2,93.0 401.7,93.6 402.1,93.9 402.5,93.6 402.9,93.3 403.3,92.7 403.8,93.0 404.2,93.9 404.6,94.2 405.0,93.9 405.4,93.0 405.8,93.6 406.2,93.9 406.7,93.6 407.1,93.6 407.5,93.9 407.9,92.7 408.3,92.4 408.8,92.7 409.2,93.0 409.6,93.3 410.0,93.3 410.4,93.3 410.8,93.0 411.2,93.0 411.7,93.6 412.1,93.6 412.5,93.3 412.9,93.0 413.3,92.4 413.8,91.8 414.2,92.4 414.6,93.0 415.0,92.7 415.4,92.4 415.8,91.8 416.2,92.4 416.7,93.0 417.1,93.0 417.5,92.4 417.9,91.8 418.3,91.8 418.8,92.4 419.2,93.0 419.6,92.7 420.0,92.7 420.4,91.2 420.8,91.8 421.2,92.4 421.7,93.0 422.1,92.1 422.5,92.4 422.9,91.8 423.3,92.1 423.8,92.7 424.2,92.1 424.6,91.8 425.0,91.8 425.4,91.8 425.8,91.8 426.2,92.1 426.7,92.7 427.1,92.7 427.5,91.2 427.9,91.5 428.3,91.8 428.8,92.4 429.2,92.7 429.6,92.7 430.0,91.8 430.4,91.2 430.8,92.4 431.2,92.1 431.7,92.7 432.1,91.8 432.5,91.8 432.9,91.2 433.3,91.5 433.8,92.4 434.2,93.0 434.6,92.4 435.0,92.4 435.4,91.5 435.8,91.2 436.2,91.5 436.7,91.8 437.1,90.3 437.5,89.4 437.9,88.5 438.3,88.2 438.8,88.5 439.2,88.8 439.6,88.2 440.0,87.0 440.4,86.4 440.8,87.3 441.3,87.0 441.7,86.4 442.1,86.4 442.5,86.1 442.9,85.5 443.3,86.1 443.8,86.7 444.2,87.0 444.6,87.0 445.0,86.7 445.4,86.1 445.8,86.7 446.2,87.0 446.7,87.9 447.1,87.0 447.5,86.4 447.9,86.1 448.3,85.8 448.8,87.0 449.2,87.6 449.6,87.3 450.0,87.0 450.4,87.0 450.8,86.4 451.2,87.3 451.7,87.6 452.1,87.3 452.5,87.0 452.9,87.3 453.3,87.6 453.8,88.2 454.2,87.9 454.6,88.2 455.0,87.0 455.4,87.3 455.8,87.9 456.2,89.1 456.7,89.7 457.1,89.1 457.5,88.5 457.9,88.5 458.3,88.2 458.7,88.8 459.2,89.4 459.6,89.1 460.0,88.2 460.4,88.5 460.8,88.5 461.2,89.1 461.7,90.0 462.1,89.7 462.5,89.4 462.9,89.1 463.3,89.4 463.8,90.0 464.2,90.3 464.6,90.0 465.0,89.7 465.4,89.4 465.8,89.4 466.2,89.1 466.7,89.4 467.1,89.7 467.5,89.4 467.9,88.5 468.3,89.7 468.8,89.7 469.2,90.3 469.6,91.2 470.0,90.9 470.4,90.0 470.8,90.0 471.2,90.3 471.7,90.3 472.1,90.3 472.5,89.7 472.9,89.7 473.3,90.0 473.8,90.0 474.2,92.1 474.6,90.9 475.0,90.9 475.4,90.0 475.8,90.0 476.2,90.3 476.7,90.6 477.1,90.0 477.5,89.1 477.9,89.1 478.3,89.4 478.8,89.4 479.2,89.7 479.6,89.1 480.0,88.5 480.4,86.7 480.8,86.7 481.2,87.3 481.7,87.6 482.1,86.4 482.5,86.1 482.9,85.8 483.3,86.1 483.8,85.8 484.2,85.5 484.6,85.2 485.0,84.3 485.4,83.1 485.8,84.0 486.2,83.7 486.7,84.6 487.1,84.6 487.5,84.0 487.9,83.4 488.3,84.6 488.8,85.2 489.2,84.9 489.6,84.6 490.0,85.5 490.4,85.2 490.8,86.1 491.2,84.6 491.7,84.3 492.1,84.0 492.5,85.2 492.9,86.1 493.3,87.3 493.8,88.2 494.2,88.8 494.6,89.4 495.0,90.0 495.4,89.1 495.8,89.4 496.2,90.0 496.7,90.9 497.1,90.3 497.5,89.7 497.9,89.4 498.3,90.0 498.8,90.9 499.2,91.2 499.6,91.8 500.0,91.5 500.4,91.2 500.8,91.2 501.2,92.1 501.7,91.8 502.1,91.8 502.5,91.2 502.9,91.5 503.3,90.9 503.8,91.5 504.2,92.1 504.6,91.2 505.0,90.9 505.4,90.3 505.8,90.6 506.2,91.5 506.7,92.4 507.1,93.0 507.5,95.1 507.9,96.0 508.3,98.4 508.8,100.2 509.2,103.2 509.6,102.6 510.0,97.8 510.4,90.6 510.8,82.5 511.2,72.6 511.7,58.2 512.1,40.8 512.5,27.0 512.9,20.1 513.3,22.5 513.8,37.2 514.2,60.6 514.6,81.3 515.0,94.5 515.4,99.3 515.8,98.1 516.2,96.3 516.7,93.9 517.1,93.3 517.5,92.7 517.9,92.7 518.3,93.3 518.8,93.6 519.2,94.8 519.6,94.8 520.0,93.6 520.4,93.0 520.8,93.6 521.2,93.6 521.7,94.2 522.1,93.6 522.5,92.4 522.9,92.7 523.3,93.0 523.8,93.0 524.2,93.0 524.6,93.0 525.0,92.4 525.4,92.7 525.8,92.7 526.2,93.3 526.7,94.8 527.1,93.9 527.5,93.3 527.9,93.0 528.3,93.3 528.8,93.6 529.2,94.8 529.6,94.2 530.0,93.6 530.4,93.6 530.8,93.6 531.2,93.9 531.7,94.2 532.1,93.6 532.5,94.5 532.9,93.6 533.3,93.9 533.8,93.9 534.2,94.5 534.6,94.2 535.0,93.6 535.4,93.0 535.8,93.0 536.2,93.0 536.7,93.3 537.1,93.0 537.5,93.0 537.9,93.6 538.3,93.6 538.8,94.5 539.2,95.4 539.6,94.2 540.0,93.6 540.4,93.0 540.8,92.7 541.2,94.2 541.7,93.6 542.1,93.6 542.5,93.3 542.9,93.0 543.3,93.0 543.8,93.6 544.2,94.5 544.6,94.2 545.0,93.3 545.4,93.0 545.8,93.3 546.2,93.6 546.7,94.8 547.1,94.8 547.5,94.8 547.9,94.5 548.3,94.8 548.8,96.3 549.2,96.0 549.6,96.3 550.0,95.4 550.4,96.0 550.8,97.5 551.2,96.6 551.7,96.9 552.1,95.7 552.5,95.4 552.9,94.8 553.3,95.1 553.8,96.0 554.2,96.3 554.6,96.0 555.0,95.1 555.4,94.5 555.8,93.9 556.2,94.8 556.7,94.5 557.1,93.6 557.5,92.1 557.9,91.5 558.3,91.2 558.8,91.2 559.2,91.2 559.6,90.0 560.0,89.1 560.4,88.2 560.8,87.6 561.2,87.6 561.7,88.5 562.1,87.9 562.5,87.9 562.9,87.6 563.3,87.9 563.8,88.2 564.2,88.5 564.6,88.2 565.0,87.6 565.4,87.6 565.8,87.0 566.2,87.9 566.7,88.5 567.1,87.9 567.5,88.2 567.9,87.0 568.3,87.3 568.8,87.6 569.2,87.3 569.6,86.4 570.0,86.1 570.4,86.7 570.8,87.0 571.2,87.6 571.7,88.8 572.1,87.6 572.5,87.3 572.9,87.3 573.3,88.2 573.8,88.8 574.2,89.4 574.6,88.8 575.0,88.2 575.4,88.5 575.8,89.4 576.2,89.1 576.7,89.7 577.1,88.8 577.5,88.8 577.9,88.5 578.3,88.2 578.8,89.4 579.2,89.4 579.6,90.0 580.0,89.4 580.4,88.8 580.8,89.1 581.2,88.2 581.7,89.4 582.1,89.1 582.5,89.1 582.9,89.1 583.3,89.1 583.8,89.4 584.2,89.7 584.6,89.1 585.0,88.5 585.4,88.2 585.8,88.8 586.2,89.4 586.7,90.6 587.1,90.0 587.5,89.7 587.9,89.4 588.3,88.5 588.8,88.8 589.2,90.3 589.6,89.1 590.0,88.2 590.4,88.2 590.8,89.1 591.2,89.1 591.7,89.4 592.1,89.4 592.5,89.1 592.9,89.1 593.3,89.1 593.8,89.7 594.2,89.7 594.6,89.7 595.0,88.8 595.4,88.8 595.8,88.8 596.2,90.0 596.7,90.3 597.1,89.7 597.5,89.1 597.9,88.5 598.3,87.9 598.8,87.6 599.2,87.6 599.6,85.8 600.0,85.5 600.4,84.6 600.8,84.9 601.3,85.2 601.7,84.9 602.1,84.3 602.5,83.4 602.9,83.4 603.3,82.5 603.8,83.4 604.2,83.4 604.6,82.5 605.0,83.1 605.4,82.8 605.8,83.4 606.2,84.0 606.7,84.6 607.1,83.7 607.5,83.1 607.9,83.1 608.3,84.3 608.8,84.6 609.2,84.3 609.6,83.1 610.0,81.6 610.4,81.0 610.8,81.9 611.2,83.1 611.7,85.5 612.1,85.5 612.5,86.4 612.9,86.4 613.3,87.9 613.8,89.1 614.2,89.7 614.6,89.7 615.0,90.0 615.4,90.3 615.8,90.3 616.2,89.7 616.7,90.6 617.1,90.0 617.5,89.7 617.9,89.7 618.3,90.0 618.8,90.6 619.2,91.5 619.6,90.6 620.0,91.5 620.4,90.0 620.8,89.7 621.2,90.9 621.7,92.1 622.1,90.9 622.5,90.0 622.9,90.3 623.3,90.3 623.8,90.6 624.2,92.1 624.6,92.7 625.0,93.0 625.4,94.8 625.8,96.6 626.2,97.8 626.7,99.9 627.1,102.0 627.5,101.7 627.9,99.0 628.3,93.6 628.8,87.0 629.2,78.9 629.6,66.9 630.0,50.4 630.4,33.6 630.8,21.3 631.2,16.2 631.7,21.6 632.1,38.1 632.5,61.5 632.9,82.2 633.3,94.8 633.8,99.3 634.2,98.7 634.6,96.3 635.0,93.3 635.4,92.7 635.8,93.0 636.2,93.0 636.7,93.3 637.1,92.7 637.5,92.1 637.9,92.4 638.3,92.4 638.8,93.3 639.2,93.9 639.6,93.9 640.0,92.7 640.4,92.7 640.8,93.6 641.2,93.6 641.7,94.2 642.1,93.9 642.5,93.0 642.9,93.0 643.3,93.3 643.8,94.2 644.2,94.2 644.6,94.2 645.0,93.3 645.4,92.7 645.8,92.7 646.2,93.9 646.7,94.2 647.1,93.6 647.5,93.0 647.9,93.0 648.3,93.0 648.8,93.6 649.2,93.9 649.6,93.9 650.0,93.3 650.4,92.7 650.8,93.0 651.2,93.9 651.7,94.8 652.1,94.2 652.5,93.6 652.9,93.9 653.3,93.6 653.8,94.2 654.2,94.8 654.6,94.8 655.0,93.9 655.4,93.0 655.8,92.7 656.2,93.3 656.7,93.9 657.1,93.9 657.5,93.3 657.9,92.7 658.3,93.9 658.8,94.5 659.2,94.5 659.6,94.2 660.0,94.2 660.4,93.6 660.8,94.5 661.2,94.2 661.7,94.8 662.1,93.9 662.5,93.3 662.9,93.6 663.3,93.3 663.8,93.3 664.2,93.9 664.6,93.3 665.0,93.0 665.4,93.0 665.8,93.6 666.2,93.9 666.7,94.8 667.1,94.8 667.5,93.9 667.9,93.9 668.3,94.5 668.8,95.1 669.2,96.0 669.6,95.7 670.0,95.4 670.4,95.1 670.8,95.1 671.2,96.3 671.7,96.0 672.1,96.0 672.5,95.4 672.9,95.4 673.3,96.0 673.7,95.7 674.2,96.3 674.6,95.1 675.0,95.1 675.4,94.2 675.8,93.3 676.3,93.3 676.7,92.4 677.1,91.2 677.5,89.4 677.9,89.1 678.3,88.8 678.8,89.1 679.2,89.1 679.6,87.9 680.0,87.0 680.4,86.4 680.8,86.7 681.2,86.7 681.7,87.9 682.1,87.0 682.5,86.4 682.9,86.1 683.3,87.3 683.8,86.7 684.2,87.0 684.6,86.7 685.0,86.1 685.4,85.8 685.8,85.8 686.2,86.7 686.7,86.7 687.1,86.4 687.5,85.5 687.9,85.5 688.3,85.5 688.8,85.8 689.2,86.7 689.6,86.4 690.0,85.8 690.4,85.8 690.8,86.7 691.2,87.0 691.7,87.6 692.1,87.0 692.5,87.0 692.9,86.4 693.3,86.7 693.8,87.3 694.2,87.6 694.6,87.9 695.0,87.0 695.4,87.3 695.8,87.6 696.2,87.9 696.7,88.8 697.1,88.8 697.5,88.2 697.9,87.9 698.3,88.2 698.8,88.2 699.2,88.8 699.6,88.5 700.0,87.9 700.4,88.5 700.8,88.2 701.2,89.1 701.7,89.1 702.1,88.5 702.5,87.9 702.9,87.9 703.3,87.9 703.8,89.1 704.2,89.4 704.6,89.1 705.0,88.5 705.4,88.8 705.8,88.8 706.2,89.1 706.7,89.4 707.1,89.1 707.5,88.8 707.9,88.8 708.3,88.5 708.8,88.8 709.2,89.1 709.6,88.8 710.0,88.2 710.4,87.6 710.8,88.8 711.2,88.2 711.7,89.4 712.1,89.1 712.5,87.9 712.9,88.5 713.3,89.1 713.8,89.1 714.2,89.4 714.6,89.1 715.0,89.1 715.4,88.5 715.8,88.5 716.2,89.1 716.7,89.1 717.1,88.8 717.5,88.2 717.9,88.2 718.3,88.2 718.8,89.1 719.2,89.1 719.6,88.5 720.0,88.2 720.4,87.6 720.8,87.6 721.2,87.0 721.7,88.2 722.1,87.3 722.5,85.8 722.9,84.6 723.3,84.6 723.8,84.9 724.2,85.2 724.6,84.6 725.0,83.4 725.4,83.1 725.8,82.8 726.2,82.5 726.7,82.5 727.1,82.2 727.5,81.3 727.9,81.6 728.3,81.6 728.8,82.8 729.2,83.4 729.6,83.7 730.0,83.1 730.4,82.2 730.8,83.7 731.2,83.7 731.7,84.3 732.1,83.4 732.5,81.9 732.9,81.3 733.3,82.5 733.8,84.6 734.2,85.8 734.6,86.4 735.0,87.3 735.4,87.6 735.8,88.5 736.2,89.1 736.7,88.8 737.1,88.5 737.5,89.1 737.9,89.1 738.3,89.4 738.8,89.7 739.2,90.0 739.6,89.7 740.0,89.4 740.4,88.5 740.8,88.8 741.2,89.4 741.7,90.0 742.1,90.0 742.5,90.0 742.9,89.4 743.3,89.7 743.8,90.0 744.2,90.6 744.6,89.7 745.0,89.7 745.4,89.7 745.8,89.7 746.2,90.0 746.7,90.6 747.1,91.2 747.5,91.5 747.9,93.6 748.3,96.0 748.7,98.1 749.2,99.0 749.6,100.5 750.0,101.4 750.4,99.6 750.8,94.2 751.3,86.1 751.7,77.4 752.1,65.4 752.5,51.3 752.9,34.5 753.3,20.7 753.8,12.6 754.2,14.1 754.6,22.8 755.0,42.6 755.4,68.1 755.8,87.0 756.2,96.0 756.7,97.5 757.1,94.8 757.5,92.1 757.9,90.9 758.3,90.9 758.8,91.5 759.2,92.1 759.6,92.1 760.0,91.8 760.4,91.5 760.8,91.2 761.2,91.5 761.7,92.4 762.1,92.4 762.5,91.8 762.9,91.5 763.3,91.5 763.8,92.4 764.2,93.0 764.6,92.4 765.0,92.4 765.4,92.7 765.8,92.4 766.2,93.0 766.7,93.9 767.1,93.3 767.5,93.0 767.9,92.1 768.3,93.0 768.8,93.0 769.2,93.3 769.6,93.3 770.0,93.0 770.4,92.7 770.8,92.7 771.2,93.0 771.7,93.6 772.1,92.7 772.5,92.4 772.9,91.8 773.3,91.8 773.8,92.1 774.2,92.7 774.6,92.4 775.0,91.5 775.4,91.5 775.8,91.5 776.2,91.8 776.7,92.4 777.1,91.5 777.5,92.7 777.9,91.8 778.3,91.5 778.8,92.1 779.2,92.7 779.6,92.7 780.0,92.4 780.4,91.8 780.8,91.8 781.2,92.4 781.7,93.0 782.1,92.7 782.5,92.4 782.9,91.8 783.3,92.1 783.8,92.4 784.2,92.7 784.6,92.1 785.0,92.1 785.4,91.5 785.8,91.5 786.2,91.2 786.7,92.7 787.1,91.2 787.5,91.2 787.9,90.9 788.3,91.8 788.8,92.1 789.2,93.3 789.6,92.7 790.0,91.8 790.4,91.8 790.8,91.5 791.2,92.4 791.7,92.7 792.1,92.7 792.5,92.7 792.9,92.7 793.3,91.8 793.8,92.4 794.2,93.0 794.6,92.1 795.0,91.5 795.4,91.8 795.8,91.8 796.2,92.7 796.7,93.6 797.1,91.8 797.5,91.5 797.9,90.9 798.3,91.8 798.8,92.4 799.2,92.1 799.6,91.5 800.0,90.9 800.4,90.0 800.8,90.0 801.2,89.1 801.7,89.1 802.1,88.2 802.5,87.9 802.9,87.0 803.3,86.4 803.8,86.4 804.2,87.0 804.6,86.1 805.0,85.5 805.4,86.1 805.8,86.1 806.2,86.1 806.7,86.7 807.1,86.7 807.5,86.1 807.9,85.8 808.3,86.1 808.8,86.4 809.2,86.7 809.6,86.7 810.0,86.1 810.4,86.1 810.8,86.4 811.2,86.7 811.7,87.3 812.1,87.0 812.5,86.4 812.9,86.1 813.3,86.4 813.8,86.4 814.2,87.0 814.6,86.4 815.0,86.1 815.4,85.8 815.8,86.1 816.2,86.7 816.7,87.9 817.1,87.6 817.5,86.4 817.9,85.5 818.3,85.5 818.8,85.8 819.2,86.4 819.6,86.4 820.0,85.5 820.4,85.2 820.8,85.2 821.2,85.2 821.7,86.1 822.1,85.2 822.5,84.0 822.9,83.4 823.3,83.4 823.7,84.3 824.2,84.3 824.6,84.0 825.0,82.2 825.4,82.5 825.8,84.0 826.3,84.6 826.7,83.1 827.1,81.6 827.5,81.9 827.9,82.5 828.3,83.1 828.8,83.7 829.2,83.7 829.6,84.0 830.0,84.3 830.4,85.5 830.8,86.4 831.2,88.2 831.7,88.5 832.1,88.5 832.5,87.9 832.9,89.1 833.3,89.7 833.8,90.0 834.2,90.9 834.6,91.2 835.0,90.9 835.4,90.3 835.8,90.6 836.2,91.8 836.7,92.4 837.1,91.8 837.5,91.5 837.9,91.2 838.3,91.2 838.8,91.5 839.2,92.1 839.6,90.9 840.0,90.3 840.4,90.6 840.8,90.6 841.2,90.3 841.7,91.2 842.1,90.3 842.5,90.3 842.9,89.7 843.3,90.6 843.8,90.3 844.2,91.8 844.6,91.2 845.0,91.8 845.4,93.3 845.8,95.1 846.2,97.8 846.7,100.5 847.1,100.5 847.5,102.3 847.9,103.5 848.3,101.7 848.8,96.0 849.2,87.6 849.6,77.7 850.0,67.8 850.4,53.7 850.8,38.7 851.2,25.2 851.7,18.6 852.1,16.8 852.5,25.2 852.9,45.3 853.3,70.8 853.8,89.4 854.2,98.1 854.6,97.5 855.0,94.2 855.4,91.8 855.8,91.2 856.2,92.4 856.7,93.3 857.1,92.1 857.5,92.7 857.9,91.8 858.3,92.4 858.8,93.0 859.2,93.6 859.6,92.7 860.0,92.1 860.4,92.4 860.8,92.4 861.2,93.0 861.7,93.3 862.1,93.6 862.5,93.3 862.9,92.7 863.3,92.7 863.8,93.0 864.2,93.3 864.6,92.7 865.0,92.4 865.4,92.7 865.8,92.4 866.2,93.9 866.7,94.5 867.1,93.6 867.5,93.9 867.9,92.7 868.3,92.7 868.8,92.7 869.2,93.3 869.6,93.3 870.0,92.7 870.4,91.8 870.8,92.1 871.2,93.0 871.7,93.3 872.1,92.7 872.5,93.3 872.9,92.7 873.3,93.0 873.8,93.9 874.2,94.2 874.6,93.6 875.0,92.4 875.4,92.4 875.8,92.1 876.2,93.3 876.7,93.3 877.1,93.0 877.5,92.7 877.9,92.1 878.3,91.8 878.8,93.0 879.2,93.0 879.6,92.4 880.0,92.1 880.4,91.8 880.8,92.4 881.2,92.7 881.7,93.3 882.1,93.3 882.5,92.4 882.9,92.1 883.3,93.0 883.8,92.7 884.2,93.3 884.6,93.0 885.0,92.4 885.4,92.1 885.8,92.4 886.2,93.0 886.7,93.6 887.1,93.3 887.5,92.7 887.9,92.1 888.3,92.1 888.8,92.4 889.2,93.6 889.6,93.0 890.0,93.3 890.4,92.7 890.8,93.3 891.2,93.6 891.7,94.8 892.1,94.5 892.5,93.6 892.9,93.3 893.3,93.6 893.8,93.6 894.2,94.2 894.6,93.3 895.0,92.7 895.4,92.1 895.8,92.4 896.2,93.0 896.7,93.6 897.1,92.7 897.5,91.5 897.9,91.5 898.3,91.5 898.7,92.4 899.2,91.5 899.6,90.6\"/><text class=\"cap\" x=\"4\" y=\"193\">실제 심전도(오픈 DB) · MIT-BIH #100 · MLII · 25 mm/s, 10 mm/mV</text></svg>"
 },
 {
  "id": "usmle-2026-0034",
  "exam": "usmle",
  "step": "Step 2",
  "subject": "Internal Medicine",
  "subject_file": "Internal Medicine",
  "subtopic": "Complete Right Bundle Branch Block (12-lead, real ECG)",
  "type": "Complete Right Bundle Branch Block (12-lead, real ECG)",
  "difficulty": 4,
  "created": "2026-07-07",
  "vignette": "A 62-year-old man has a 12-lead electrocardiogram performed before elective surgery. He is asymptomatic. The tracing is shown.",
  "question": "Which of the following best accounts for the widened QRS complex?",
  "options": [
   "Complete right bundle branch block",
   "Complete left bundle branch block",
   "Wolff-Parkinson-White pattern",
   "Left anterior fascicular block",
   "Left ventricular hypertrophy"
  ],
  "answer": 1,
  "explanationText": "- 적용(12유도 판독 → 진단): QRS 폭 ≥120 ms + V1–V2의 rSR′(\"토끼귀\" M자)\n  + I·V6의 넓고 뭉툭한 S파 → 완전우각차단(CRBBB). 우각 차단으로 우심실\n  탈분극이 지연돼 우흉부에서 늦은 R′가 생긴다.\n- 오답감별(낚시 주의): (B) 좌각차단(CLBBB)도 넓은 QRS지만 정반대로 I·V6에\n  넓은 단일 R파, V1에 QS/rS이고 rSR′가 없다 — \"넓은 QRS = LBBB\"로 넘겨짚기\n  쉬운 함정. (C) WPW는 짧은 PR + 델타파로 넓어진다(형태가 다름). (D)\n  좌전섬유속차단(LAFB)은 좌축편위를 만들지만 QRS를 넓히지 않는다(이 심전도\n  질문의 핵심: 폭 확장의 원인이 아님) — 이 기록에 LAFB가 동반돼 있어 특히 매력적인\n  오답. (E) LVH는 전압 증가가 특징이지 폭 확장의 주원인이 아니다.\n- 임상핵심: 넓은 QRS는 ① 폭(≥120 ms) → ② V1 형태(rSR′=RBBB / 단일 R=LBBB)\n  → ③ PR·델타(WPW) 순으로 접근. 새 CLBBB + 흉통은 STEMI-equivalent로 취급.\n- 자료 관련: 이 12유도는 합성이 아니라 오픈 DB(PTB-XL, CC-BY)의 실제 기록을\n  렌더한 것(`assets/ecg/*.json` → `render_signal_svg.twelve_lead_svg`). 모양이 본질인\n  진단이라 합성 대신 실데이터를 쓴다.\n- 출처: PTB-XL (PhysioNet); AHA/ACCF/HRS ECG interpretation.",
  "explanationItems": [
   {
    "k": "적용(12유도 판독 → 진단)",
    "v": "QRS 폭 ≥120 ms + V1–V2의 rSR′(\"토끼귀\" M자) + I·V6의 넓고 뭉툭한 S파 → 완전우각차단(CRBBB). 우각 차단으로 우심실 탈분극이 지연돼 우흉부에서 늦은 R′가 생긴다."
   },
   {
    "k": "오답감별(낚시 주의)",
    "v": "(B) 좌각차단(CLBBB)도 넓은 QRS지만 정반대로 I·V6에 *넓은 단일 R파, V1에 QS/rS이고 rSR′가 없다 — \"넓은 QRS = LBBB\"로 넘겨짚기 쉬운 함정. (C) WPW는 짧은 PR + 델타파로 넓어진다(형태가 다름). (D) *좌전섬유속차단(LAFB)은 좌축편위를 만들지만 QRS를 넓히지 않는다(이 심전도 질문의 핵심: 폭 확장의 원인이 아님) — 이 기록에 LAFB가 동반돼 있어 특히 매력적인 오답. (E) LVH는 전압 증가가 특징이지 폭 확장의 주원인이 아니다."
   },
   {
    "k": "임상핵심",
    "v": "넓은 QRS는 ① 폭(≥120 ms) → ② V1 형태(rSR′=RBBB / 단일 R=LBBB) → ③ PR·델타(WPW) 순으로 접근. 새 CLBBB + 흉통은 STEMI-equivalent로 취급."
   },
   {
    "k": "자료 관련",
    "v": "이 12유도는 합성이 아니라 오픈 DB(PTB-XL, CC-BY)의 실제 기록을 렌더한 것(`assets/ecg/*.json` → `render_signal_svg.twelve_lead_svg`). 모양이 본질인 진단이라 합성 대신 실데이터를 쓴다."
   },
   {
    "k": "출처",
    "v": "PTB-XL (PhysioNet); AHA/ACCF/HRS ECG interpretation."
   }
  ],
  "source": "USMLE-style / MedKOS · ECG: PTB-XL 1.0.3 (PhysioNet, CC-BY 4.0)",
  "vitals": [],
  "labs": [],
  "appendix": {
   "가이드라인": "넓은 QRS(≥120 ms) 감별 — 12유도 형태\n─────────────────────────────────────\nCRBBB : V1–V2 rSR′(M) · I·V6 넓은 S · 우흉부에서 뒤늦은 R\nCLBBB : I·V6 넓은 단일 R(노치) · V1 QS/rS · 중격 q 소실\nWPW   : PR 단축(<120 ms) + 델타파(QRS 시작부 뭉툭)\n심실 기원/고칼륨 : P 없음/사인파 등 맥락으로 감별\n(LAFB·LPFB 단독은 축은 바꿔도 QRS를 넓히지 않는다)\n",
   "최신지견": "새 CLBBB + 흉통은 STEMI-equivalent로 다룰 수 있으나, 무증상 우연 발견 CRBBB는 대개 양성이다.",
   "참고문헌": [
    "PTB-XL: a large publicly available ECG dataset (PhysioNet, CC-BY 4.0)",
    "AHA/ACCF/HRS Recommendations for Interpretation of the ECG (Intraventricular Conduction)"
   ]
  },
  "figureSvg": "<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 1500 456\" width=\"1500\" height=\"456\" role=\"img\" aria-label=\"12-lead ECG 12유도 · 실데이터(PTB-XL, CC-BY) · 25 mm/s, 10 mm/mV\"><style>.bg{fill:#fff}.gmin{stroke:#f4c9c9;stroke-width:0.5}.gmaj{stroke:#e59a9a;stroke-width:1}.trace{fill:none;stroke:#111;stroke-width:1.2;stroke-linejoin:round}.lead{font:bold 11px sans-serif;fill:#333}.cap{font:11px sans-serif;fill:#555}</style><rect class=\"bg\" x=\"0\" y=\"0\" width=\"1500\" height=\"440\"/><line x1=\"0\" y1=\"0\" x2=\"0\" y2=\"440\" class=\"gmaj\"/><line x1=\"6\" y1=\"0\" x2=\"6\" y2=\"440\" class=\"gmin\"/><line x1=\"12\" y1=\"0\" x2=\"12\" y2=\"440\" class=\"gmin\"/><line x1=\"18\" y1=\"0\" x2=\"18\" y2=\"440\" class=\"gmin\"/><line x1=\"24\" y1=\"0\" x2=\"24\" y2=\"440\" class=\"gmin\"/><line x1=\"30\" y1=\"0\" x2=\"30\" y2=\"440\" class=\"gmaj\"/><line x1=\"36\" y1=\"0\" x2=\"36\" y2=\"440\" class=\"gmin\"/><line x1=\"42\" y1=\"0\" x2=\"42\" y2=\"440\" class=\"gmin\"/><line x1=\"48\" y1=\"0\" x2=\"48\" y2=\"440\" class=\"gmin\"/><line x1=\"54\" y1=\"0\" x2=\"54\" y2=\"440\" class=\"gmin\"/><line x1=\"60\" y1=\"0\" x2=\"60\" y2=\"440\" class=\"gmaj\"/><line x1=\"66\" y1=\"0\" x2=\"66\" y2=\"440\" class=\"gmin\"/><line x1=\"72\" y1=\"0\" x2=\"72\" y2=\"440\" class=\"gmin\"/><line x1=\"78\" y1=\"0\" x2=\"78\" y2=\"440\" class=\"gmin\"/><line x1=\"84\" y1=\"0\" x2=\"84\" y2=\"440\" class=\"gmin\"/><line x1=\"90\" y1=\"0\" x2=\"90\" y2=\"440\" class=\"gmaj\"/><line x1=\"96\" y1=\"0\" x2=\"96\" y2=\"440\" class=\"gmin\"/><line x1=\"102\" y1=\"0\" x2=\"102\" y2=\"440\" class=\"gmin\"/><line x1=\"108\" y1=\"0\" x2=\"108\" y2=\"440\" class=\"gmin\"/><line x1=\"114\" y1=\"0\" x2=\"114\" y2=\"440\" class=\"gmin\"/><line x1=\"120\" y1=\"0\" x2=\"120\" y2=\"440\" class=\"gmaj\"/><line x1=\"126\" y1=\"0\" x2=\"126\" y2=\"440\" class=\"gmin\"/><line x1=\"132\" y1=\"0\" x2=\"132\" y2=\"440\" class=\"gmin\"/><line x1=\"138\" y1=\"0\" x2=\"138\" y2=\"440\" class=\"gmin\"/><line x1=\"144\" y1=\"0\" x2=\"144\" y2=\"440\" class=\"gmin\"/><line x1=\"150\" y1=\"0\" x2=\"150\" y2=\"440\" class=\"gmaj\"/><line x1=\"156\" y1=\"0\" x2=\"156\" y2=\"440\" class=\"gmin\"/><line x1=\"162\" y1=\"0\" x2=\"162\" y2=\"440\" class=\"gmin\"/><line x1=\"168\" y1=\"0\" x2=\"168\" y2=\"440\" class=\"gmin\"/><line x1=\"174\" y1=\"0\" x2=\"174\" y2=\"440\" class=\"gmin\"/><line x1=\"180\" y1=\"0\" x2=\"180\" y2=\"440\" class=\"gmaj\"/><line x1=\"186\" y1=\"0\" x2=\"186\" y2=\"440\" class=\"gmin\"/><line x1=\"192\" y1=\"0\" x2=\"192\" y2=\"440\" class=\"gmin\"/><line x1=\"198\" y1=\"0\" x2=\"198\" y2=\"440\" class=\"gmin\"/><line x1=\"204\" y1=\"0\" x2=\"204\" y2=\"440\" class=\"gmin\"/><line x1=\"210\" y1=\"0\" x2=\"210\" y2=\"440\" class=\"gmaj\"/><line x1=\"216\" y1=\"0\" x2=\"216\" y2=\"440\" class=\"gmin\"/><line x1=\"222\" y1=\"0\" x2=\"222\" y2=\"440\" class=\"gmin\"/><line x1=\"228\" y1=\"0\" x2=\"228\" y2=\"440\" class=\"gmin\"/><line x1=\"234\" y1=\"0\" x2=\"234\" y2=\"440\" class=\"gmin\"/><line x1=\"240\" y1=\"0\" x2=\"240\" y2=\"440\" class=\"gmaj\"/><line x1=\"246\" y1=\"0\" x2=\"246\" y2=\"440\" class=\"gmin\"/><line x1=\"252\" y1=\"0\" x2=\"252\" y2=\"440\" class=\"gmin\"/><line x1=\"258\" y1=\"0\" x2=\"258\" y2=\"440\" class=\"gmin\"/><line x1=\"264\" y1=\"0\" x2=\"264\" y2=\"440\" class=\"gmin\"/><line x1=\"270\" y1=\"0\" x2=\"270\" y2=\"440\" class=\"gmaj\"/><line x1=\"276\" y1=\"0\" x2=\"276\" y2=\"440\" class=\"gmin\"/><line x1=\"282\" y1=\"0\" x2=\"282\" y2=\"440\" class=\"gmin\"/><line x1=\"288\" y1=\"0\" x2=\"288\" y2=\"440\" class=\"gmin\"/><line x1=\"294\" y1=\"0\" x2=\"294\" y2=\"440\" class=\"gmin\"/><line x1=\"300\" y1=\"0\" x2=\"300\" y2=\"440\" class=\"gmaj\"/><line x1=\"306\" y1=\"0\" x2=\"306\" y2=\"440\" class=\"gmin\"/><line x1=\"312\" y1=\"0\" x2=\"312\" y2=\"440\" class=\"gmin\"/><line x1=\"318\" y1=\"0\" x2=\"318\" y2=\"440\" class=\"gmin\"/><line x1=\"324\" y1=\"0\" x2=\"324\" y2=\"440\" class=\"gmin\"/><line x1=\"330\" y1=\"0\" x2=\"330\" y2=\"440\" class=\"gmaj\"/><line x1=\"336\" y1=\"0\" x2=\"336\" y2=\"440\" class=\"gmin\"/><line x1=\"342\" y1=\"0\" x2=\"342\" y2=\"440\" class=\"gmin\"/><line x1=\"348\" y1=\"0\" x2=\"348\" y2=\"440\" class=\"gmin\"/><line x1=\"354\" y1=\"0\" x2=\"354\" y2=\"440\" class=\"gmin\"/><line x1=\"360\" y1=\"0\" x2=\"360\" y2=\"440\" class=\"gmaj\"/><line x1=\"366\" y1=\"0\" x2=\"366\" y2=\"440\" class=\"gmin\"/><line x1=\"372\" y1=\"0\" x2=\"372\" y2=\"440\" class=\"gmin\"/><line x1=\"378\" y1=\"0\" x2=\"378\" y2=\"440\" class=\"gmin\"/><line x1=\"384\" y1=\"0\" x2=\"384\" y2=\"440\" class=\"gmin\"/><line x1=\"390\" y1=\"0\" x2=\"390\" y2=\"440\" class=\"gmaj\"/><line x1=\"396\" y1=\"0\" x2=\"396\" y2=\"440\" class=\"gmin\"/><line x1=\"402\" y1=\"0\" x2=\"402\" y2=\"440\" class=\"gmin\"/><line x1=\"408\" y1=\"0\" x2=\"408\" y2=\"440\" class=\"gmin\"/><line x1=\"414\" y1=\"0\" x2=\"414\" y2=\"440\" class=\"gmin\"/><line x1=\"420\" y1=\"0\" x2=\"420\" y2=\"440\" class=\"gmaj\"/><line x1=\"426\" y1=\"0\" x2=\"426\" y2=\"440\" class=\"gmin\"/><line x1=\"432\" y1=\"0\" x2=\"432\" y2=\"440\" class=\"gmin\"/><line x1=\"438\" y1=\"0\" x2=\"438\" y2=\"440\" class=\"gmin\"/><line x1=\"444\" y1=\"0\" x2=\"444\" y2=\"440\" class=\"gmin\"/><line x1=\"450\" y1=\"0\" x2=\"450\" y2=\"440\" class=\"gmaj\"/><line x1=\"456\" y1=\"0\" x2=\"456\" y2=\"440\" class=\"gmin\"/><line x1=\"462\" y1=\"0\" x2=\"462\" y2=\"440\" class=\"gmin\"/><line x1=\"468\" y1=\"0\" x2=\"468\" y2=\"440\" class=\"gmin\"/><line x1=\"474\" y1=\"0\" x2=\"474\" y2=\"440\" class=\"gmin\"/><line x1=\"480\" y1=\"0\" x2=\"480\" y2=\"440\" class=\"gmaj\"/><line x1=\"486\" y1=\"0\" x2=\"486\" y2=\"440\" class=\"gmin\"/><line x1=\"492\" y1=\"0\" x2=\"492\" y2=\"440\" class=\"gmin\"/><line x1=\"498\" y1=\"0\" x2=\"498\" y2=\"440\" class=\"gmin\"/><line x1=\"504\" y1=\"0\" x2=\"504\" y2=\"440\" class=\"gmin\"/><line x1=\"510\" y1=\"0\" x2=\"510\" y2=\"440\" class=\"gmaj\"/><line x1=\"516\" y1=\"0\" x2=\"516\" y2=\"440\" class=\"gmin\"/><line x1=\"522\" y1=\"0\" x2=\"522\" y2=\"440\" class=\"gmin\"/><line x1=\"528\" y1=\"0\" x2=\"528\" y2=\"440\" class=\"gmin\"/><line x1=\"534\" y1=\"0\" x2=\"534\" y2=\"440\" class=\"gmin\"/><line x1=\"540\" y1=\"0\" x2=\"540\" y2=\"440\" class=\"gmaj\"/><line x1=\"546\" y1=\"0\" x2=\"546\" y2=\"440\" class=\"gmin\"/><line x1=\"552\" y1=\"0\" x2=\"552\" y2=\"440\" class=\"gmin\"/><line x1=\"558\" y1=\"0\" x2=\"558\" y2=\"440\" class=\"gmin\"/><line x1=\"564\" y1=\"0\" x2=\"564\" y2=\"440\" class=\"gmin\"/><line x1=\"570\" y1=\"0\" x2=\"570\" y2=\"440\" class=\"gmaj\"/><line x1=\"576\" y1=\"0\" x2=\"576\" y2=\"440\" class=\"gmin\"/><line x1=\"582\" y1=\"0\" x2=\"582\" y2=\"440\" class=\"gmin\"/><line x1=\"588\" y1=\"0\" x2=\"588\" y2=\"440\" class=\"gmin\"/><line x1=\"594\" y1=\"0\" x2=\"594\" y2=\"440\" class=\"gmin\"/><line x1=\"600\" y1=\"0\" x2=\"600\" y2=\"440\" class=\"gmaj\"/><line x1=\"606\" y1=\"0\" x2=\"606\" y2=\"440\" class=\"gmin\"/><line x1=\"612\" y1=\"0\" x2=\"612\" y2=\"440\" class=\"gmin\"/><line x1=\"618\" y1=\"0\" x2=\"618\" y2=\"440\" class=\"gmin\"/><line x1=\"624\" y1=\"0\" x2=\"624\" y2=\"440\" class=\"gmin\"/><line x1=\"630\" y1=\"0\" x2=\"630\" y2=\"440\" class=\"gmaj\"/><line x1=\"636\" y1=\"0\" x2=\"636\" y2=\"440\" class=\"gmin\"/><line x1=\"642\" y1=\"0\" x2=\"642\" y2=\"440\" class=\"gmin\"/><line x1=\"648\" y1=\"0\" x2=\"648\" y2=\"440\" class=\"gmin\"/><line x1=\"654\" y1=\"0\" x2=\"654\" y2=\"440\" class=\"gmin\"/><line x1=\"660\" y1=\"0\" x2=\"660\" y2=\"440\" class=\"gmaj\"/><line x1=\"666\" y1=\"0\" x2=\"666\" y2=\"440\" class=\"gmin\"/><line x1=\"672\" y1=\"0\" x2=\"672\" y2=\"440\" class=\"gmin\"/><line x1=\"678\" y1=\"0\" x2=\"678\" y2=\"440\" class=\"gmin\"/><line x1=\"684\" y1=\"0\" x2=\"684\" y2=\"440\" class=\"gmin\"/><line x1=\"690\" y1=\"0\" x2=\"690\" y2=\"440\" class=\"gmaj\"/><line x1=\"696\" y1=\"0\" x2=\"696\" y2=\"440\" class=\"gmin\"/><line x1=\"702\" y1=\"0\" x2=\"702\" y2=\"440\" class=\"gmin\"/><line x1=\"708\" y1=\"0\" x2=\"708\" y2=\"440\" class=\"gmin\"/><line x1=\"714\" y1=\"0\" x2=\"714\" y2=\"440\" class=\"gmin\"/><line x1=\"720\" y1=\"0\" x2=\"720\" y2=\"440\" class=\"gmaj\"/><line x1=\"726\" y1=\"0\" x2=\"726\" y2=\"440\" class=\"gmin\"/><line x1=\"732\" y1=\"0\" x2=\"732\" y2=\"440\" class=\"gmin\"/><line x1=\"738\" y1=\"0\" x2=\"738\" y2=\"440\" class=\"gmin\"/><line x1=\"744\" y1=\"0\" x2=\"744\" y2=\"440\" class=\"gmin\"/><line x1=\"750\" y1=\"0\" x2=\"750\" y2=\"440\" class=\"gmaj\"/><line x1=\"756\" y1=\"0\" x2=\"756\" y2=\"440\" class=\"gmin\"/><line x1=\"762\" y1=\"0\" x2=\"762\" y2=\"440\" class=\"gmin\"/><line x1=\"768\" y1=\"0\" x2=\"768\" y2=\"440\" class=\"gmin\"/><line x1=\"774\" y1=\"0\" x2=\"774\" y2=\"440\" class=\"gmin\"/><line x1=\"780\" y1=\"0\" x2=\"780\" y2=\"440\" class=\"gmaj\"/><line x1=\"786\" y1=\"0\" x2=\"786\" y2=\"440\" class=\"gmin\"/><line x1=\"792\" y1=\"0\" x2=\"792\" y2=\"440\" class=\"gmin\"/><line x1=\"798\" y1=\"0\" x2=\"798\" y2=\"440\" class=\"gmin\"/><line x1=\"804\" y1=\"0\" x2=\"804\" y2=\"440\" class=\"gmin\"/><line x1=\"810\" y1=\"0\" x2=\"810\" y2=\"440\" class=\"gmaj\"/><line x1=\"816\" y1=\"0\" x2=\"816\" y2=\"440\" class=\"gmin\"/><line x1=\"822\" y1=\"0\" x2=\"822\" y2=\"440\" class=\"gmin\"/><line x1=\"828\" y1=\"0\" x2=\"828\" y2=\"440\" class=\"gmin\"/><line x1=\"834\" y1=\"0\" x2=\"834\" y2=\"440\" class=\"gmin\"/><line x1=\"840\" y1=\"0\" x2=\"840\" y2=\"440\" class=\"gmaj\"/><line x1=\"846\" y1=\"0\" x2=\"846\" y2=\"440\" class=\"gmin\"/><line x1=\"852\" y1=\"0\" x2=\"852\" y2=\"440\" class=\"gmin\"/><line x1=\"858\" y1=\"0\" x2=\"858\" y2=\"440\" class=\"gmin\"/><line x1=\"864\" y1=\"0\" x2=\"864\" y2=\"440\" class=\"gmin\"/><line x1=\"870\" y1=\"0\" x2=\"870\" y2=\"440\" class=\"gmaj\"/><line x1=\"876\" y1=\"0\" x2=\"876\" y2=\"440\" class=\"gmin\"/><line x1=\"882\" y1=\"0\" x2=\"882\" y2=\"440\" class=\"gmin\"/><line x1=\"888\" y1=\"0\" x2=\"888\" y2=\"440\" class=\"gmin\"/><line x1=\"894\" y1=\"0\" x2=\"894\" y2=\"440\" class=\"gmin\"/><line x1=\"900\" y1=\"0\" x2=\"900\" y2=\"440\" class=\"gmaj\"/><line x1=\"906\" y1=\"0\" x2=\"906\" y2=\"440\" class=\"gmin\"/><line x1=\"912\" y1=\"0\" x2=\"912\" y2=\"440\" class=\"gmin\"/><line x1=\"918\" y1=\"0\" x2=\"918\" y2=\"440\" class=\"gmin\"/><line x1=\"924\" y1=\"0\" x2=\"924\" y2=\"440\" class=\"gmin\"/><line x1=\"930\" y1=\"0\" x2=\"930\" y2=\"440\" class=\"gmaj\"/><line x1=\"936\" y1=\"0\" x2=\"936\" y2=\"440\" class=\"gmin\"/><line x1=\"942\" y1=\"0\" x2=\"942\" y2=\"440\" class=\"gmin\"/><line x1=\"948\" y1=\"0\" x2=\"948\" y2=\"440\" class=\"gmin\"/><line x1=\"954\" y1=\"0\" x2=\"954\" y2=\"440\" class=\"gmin\"/><line x1=\"960\" y1=\"0\" x2=\"960\" y2=\"440\" class=\"gmaj\"/><line x1=\"966\" y1=\"0\" x2=\"966\" y2=\"440\" class=\"gmin\"/><line x1=\"972\" y1=\"0\" x2=\"972\" y2=\"440\" class=\"gmin\"/><line x1=\"978\" y1=\"0\" x2=\"978\" y2=\"440\" class=\"gmin\"/><line x1=\"984\" y1=\"0\" x2=\"984\" y2=\"440\" class=\"gmin\"/><line x1=\"990\" y1=\"0\" x2=\"990\" y2=\"440\" class=\"gmaj\"/><line x1=\"996\" y1=\"0\" x2=\"996\" y2=\"440\" class=\"gmin\"/><line x1=\"1002\" y1=\"0\" x2=\"1002\" y2=\"440\" class=\"gmin\"/><line x1=\"1008\" y1=\"0\" x2=\"1008\" y2=\"440\" class=\"gmin\"/><line x1=\"1014\" y1=\"0\" x2=\"1014\" y2=\"440\" class=\"gmin\"/><line x1=\"1020\" y1=\"0\" x2=\"1020\" y2=\"440\" class=\"gmaj\"/><line x1=\"1026\" y1=\"0\" x2=\"1026\" y2=\"440\" class=\"gmin\"/><line x1=\"1032\" y1=\"0\" x2=\"1032\" y2=\"440\" class=\"gmin\"/><line x1=\"1038\" y1=\"0\" x2=\"1038\" y2=\"440\" class=\"gmin\"/><line x1=\"1044\" y1=\"0\" x2=\"1044\" y2=\"440\" class=\"gmin\"/><line x1=\"1050\" y1=\"0\" x2=\"1050\" y2=\"440\" class=\"gmaj\"/><line x1=\"1056\" y1=\"0\" x2=\"1056\" y2=\"440\" class=\"gmin\"/><line x1=\"1062\" y1=\"0\" x2=\"1062\" y2=\"440\" class=\"gmin\"/><line x1=\"1068\" y1=\"0\" x2=\"1068\" y2=\"440\" class=\"gmin\"/><line x1=\"1074\" y1=\"0\" x2=\"1074\" y2=\"440\" class=\"gmin\"/><line x1=\"1080\" y1=\"0\" x2=\"1080\" y2=\"440\" class=\"gmaj\"/><line x1=\"1086\" y1=\"0\" x2=\"1086\" y2=\"440\" class=\"gmin\"/><line x1=\"1092\" y1=\"0\" x2=\"1092\" y2=\"440\" class=\"gmin\"/><line x1=\"1098\" y1=\"0\" x2=\"1098\" y2=\"440\" class=\"gmin\"/><line x1=\"1104\" y1=\"0\" x2=\"1104\" y2=\"440\" class=\"gmin\"/><line x1=\"1110\" y1=\"0\" x2=\"1110\" y2=\"440\" class=\"gmaj\"/><line x1=\"1116\" y1=\"0\" x2=\"1116\" y2=\"440\" class=\"gmin\"/><line x1=\"1122\" y1=\"0\" x2=\"1122\" y2=\"440\" class=\"gmin\"/><line x1=\"1128\" y1=\"0\" x2=\"1128\" y2=\"440\" class=\"gmin\"/><line x1=\"1134\" y1=\"0\" x2=\"1134\" y2=\"440\" class=\"gmin\"/><line x1=\"1140\" y1=\"0\" x2=\"1140\" y2=\"440\" class=\"gmaj\"/><line x1=\"1146\" y1=\"0\" x2=\"1146\" y2=\"440\" class=\"gmin\"/><line x1=\"1152\" y1=\"0\" x2=\"1152\" y2=\"440\" class=\"gmin\"/><line x1=\"1158\" y1=\"0\" x2=\"1158\" y2=\"440\" class=\"gmin\"/><line x1=\"1164\" y1=\"0\" x2=\"1164\" y2=\"440\" class=\"gmin\"/><line x1=\"1170\" y1=\"0\" x2=\"1170\" y2=\"440\" class=\"gmaj\"/><line x1=\"1176\" y1=\"0\" x2=\"1176\" y2=\"440\" class=\"gmin\"/><line x1=\"1182\" y1=\"0\" x2=\"1182\" y2=\"440\" class=\"gmin\"/><line x1=\"1188\" y1=\"0\" x2=\"1188\" y2=\"440\" class=\"gmin\"/><line x1=\"1194\" y1=\"0\" x2=\"1194\" y2=\"440\" class=\"gmin\"/><line x1=\"1200\" y1=\"0\" x2=\"1200\" y2=\"440\" class=\"gmaj\"/><line x1=\"1206\" y1=\"0\" x2=\"1206\" y2=\"440\" class=\"gmin\"/><line x1=\"1212\" y1=\"0\" x2=\"1212\" y2=\"440\" class=\"gmin\"/><line x1=\"1218\" y1=\"0\" x2=\"1218\" y2=\"440\" class=\"gmin\"/><line x1=\"1224\" y1=\"0\" x2=\"1224\" y2=\"440\" class=\"gmin\"/><line x1=\"1230\" y1=\"0\" x2=\"1230\" y2=\"440\" class=\"gmaj\"/><line x1=\"1236\" y1=\"0\" x2=\"1236\" y2=\"440\" class=\"gmin\"/><line x1=\"1242\" y1=\"0\" x2=\"1242\" y2=\"440\" class=\"gmin\"/><line x1=\"1248\" y1=\"0\" x2=\"1248\" y2=\"440\" class=\"gmin\"/><line x1=\"1254\" y1=\"0\" x2=\"1254\" y2=\"440\" class=\"gmin\"/><line x1=\"1260\" y1=\"0\" x2=\"1260\" y2=\"440\" class=\"gmaj\"/><line x1=\"1266\" y1=\"0\" x2=\"1266\" y2=\"440\" class=\"gmin\"/><line x1=\"1272\" y1=\"0\" x2=\"1272\" y2=\"440\" class=\"gmin\"/><line x1=\"1278\" y1=\"0\" x2=\"1278\" y2=\"440\" class=\"gmin\"/><line x1=\"1284\" y1=\"0\" x2=\"1284\" y2=\"440\" class=\"gmin\"/><line x1=\"1290\" y1=\"0\" x2=\"1290\" y2=\"440\" class=\"gmaj\"/><line x1=\"1296\" y1=\"0\" x2=\"1296\" y2=\"440\" class=\"gmin\"/><line x1=\"1302\" y1=\"0\" x2=\"1302\" y2=\"440\" class=\"gmin\"/><line x1=\"1308\" y1=\"0\" x2=\"1308\" y2=\"440\" class=\"gmin\"/><line x1=\"1314\" y1=\"0\" x2=\"1314\" y2=\"440\" class=\"gmin\"/><line x1=\"1320\" y1=\"0\" x2=\"1320\" y2=\"440\" class=\"gmaj\"/><line x1=\"1326\" y1=\"0\" x2=\"1326\" y2=\"440\" class=\"gmin\"/><line x1=\"1332\" y1=\"0\" x2=\"1332\" y2=\"440\" class=\"gmin\"/><line x1=\"1338\" y1=\"0\" x2=\"1338\" y2=\"440\" class=\"gmin\"/><line x1=\"1344\" y1=\"0\" x2=\"1344\" y2=\"440\" class=\"gmin\"/><line x1=\"1350\" y1=\"0\" x2=\"1350\" y2=\"440\" class=\"gmaj\"/><line x1=\"1356\" y1=\"0\" x2=\"1356\" y2=\"440\" class=\"gmin\"/><line x1=\"1362\" y1=\"0\" x2=\"1362\" y2=\"440\" class=\"gmin\"/><line x1=\"1368\" y1=\"0\" x2=\"1368\" y2=\"440\" class=\"gmin\"/><line x1=\"1374\" y1=\"0\" x2=\"1374\" y2=\"440\" class=\"gmin\"/><line x1=\"1380\" y1=\"0\" x2=\"1380\" y2=\"440\" class=\"gmaj\"/><line x1=\"1386\" y1=\"0\" x2=\"1386\" y2=\"440\" class=\"gmin\"/><line x1=\"1392\" y1=\"0\" x2=\"1392\" y2=\"440\" class=\"gmin\"/><line x1=\"1398\" y1=\"0\" x2=\"1398\" y2=\"440\" class=\"gmin\"/><line x1=\"1404\" y1=\"0\" x2=\"1404\" y2=\"440\" class=\"gmin\"/><line x1=\"1410\" y1=\"0\" x2=\"1410\" y2=\"440\" class=\"gmaj\"/><line x1=\"1416\" y1=\"0\" x2=\"1416\" y2=\"440\" class=\"gmin\"/><line x1=\"1422\" y1=\"0\" x2=\"1422\" y2=\"440\" class=\"gmin\"/><line x1=\"1428\" y1=\"0\" x2=\"1428\" y2=\"440\" class=\"gmin\"/><line x1=\"1434\" y1=\"0\" x2=\"1434\" y2=\"440\" class=\"gmin\"/><line x1=\"1440\" y1=\"0\" x2=\"1440\" y2=\"440\" class=\"gmaj\"/><line x1=\"1446\" y1=\"0\" x2=\"1446\" y2=\"440\" class=\"gmin\"/><line x1=\"1452\" y1=\"0\" x2=\"1452\" y2=\"440\" class=\"gmin\"/><line x1=\"1458\" y1=\"0\" x2=\"1458\" y2=\"440\" class=\"gmin\"/><line x1=\"1464\" y1=\"0\" x2=\"1464\" y2=\"440\" class=\"gmin\"/><line x1=\"1470\" y1=\"0\" x2=\"1470\" y2=\"440\" class=\"gmaj\"/><line x1=\"1476\" y1=\"0\" x2=\"1476\" y2=\"440\" class=\"gmin\"/><line x1=\"1482\" y1=\"0\" x2=\"1482\" y2=\"440\" class=\"gmin\"/><line x1=\"1488\" y1=\"0\" x2=\"1488\" y2=\"440\" class=\"gmin\"/><line x1=\"1494\" y1=\"0\" x2=\"1494\" y2=\"440\" class=\"gmin\"/><line x1=\"1500\" y1=\"0\" x2=\"1500\" y2=\"440\" class=\"gmaj\"/><line x1=\"0\" y1=\"0\" x2=\"1500\" y2=\"0\" class=\"gmaj\"/><line x1=\"0\" y1=\"6\" x2=\"1500\" y2=\"6\" class=\"gmin\"/><line x1=\"0\" y1=\"12\" x2=\"1500\" y2=\"12\" class=\"gmin\"/><line x1=\"0\" y1=\"18\" x2=\"1500\" y2=\"18\" class=\"gmin\"/><line x1=\"0\" y1=\"24\" x2=\"1500\" y2=\"24\" class=\"gmin\"/><line x1=\"0\" y1=\"30\" x2=\"1500\" y2=\"30\" class=\"gmaj\"/><line x1=\"0\" y1=\"36\" x2=\"1500\" y2=\"36\" class=\"gmin\"/><line x1=\"0\" y1=\"42\" x2=\"1500\" y2=\"42\" class=\"gmin\"/><line x1=\"0\" y1=\"48\" x2=\"1500\" y2=\"48\" class=\"gmin\"/><line x1=\"0\" y1=\"54\" x2=\"1500\" y2=\"54\" class=\"gmin\"/><line x1=\"0\" y1=\"60\" x2=\"1500\" y2=\"60\" class=\"gmaj\"/><line x1=\"0\" y1=\"66\" x2=\"1500\" y2=\"66\" class=\"gmin\"/><line x1=\"0\" y1=\"72\" x2=\"1500\" y2=\"72\" class=\"gmin\"/><line x1=\"0\" y1=\"78\" x2=\"1500\" y2=\"78\" class=\"gmin\"/><line x1=\"0\" y1=\"84\" x2=\"1500\" y2=\"84\" class=\"gmin\"/><line x1=\"0\" y1=\"90\" x2=\"1500\" y2=\"90\" class=\"gmaj\"/><line x1=\"0\" y1=\"96\" x2=\"1500\" y2=\"96\" class=\"gmin\"/><line x1=\"0\" y1=\"102\" x2=\"1500\" y2=\"102\" class=\"gmin\"/><line x1=\"0\" y1=\"108\" x2=\"1500\" y2=\"108\" class=\"gmin\"/><line x1=\"0\" y1=\"114\" x2=\"1500\" y2=\"114\" class=\"gmin\"/><line x1=\"0\" y1=\"120\" x2=\"1500\" y2=\"120\" class=\"gmaj\"/><line x1=\"0\" y1=\"126\" x2=\"1500\" y2=\"126\" class=\"gmin\"/><line x1=\"0\" y1=\"132\" x2=\"1500\" y2=\"132\" class=\"gmin\"/><line x1=\"0\" y1=\"138\" x2=\"1500\" y2=\"138\" class=\"gmin\"/><line x1=\"0\" y1=\"144\" x2=\"1500\" y2=\"144\" class=\"gmin\"/><line x1=\"0\" y1=\"150\" x2=\"1500\" y2=\"150\" class=\"gmaj\"/><line x1=\"0\" y1=\"156\" x2=\"1500\" y2=\"156\" class=\"gmin\"/><line x1=\"0\" y1=\"162\" x2=\"1500\" y2=\"162\" class=\"gmin\"/><line x1=\"0\" y1=\"168\" x2=\"1500\" y2=\"168\" class=\"gmin\"/><line x1=\"0\" y1=\"174\" x2=\"1500\" y2=\"174\" class=\"gmin\"/><line x1=\"0\" y1=\"180\" x2=\"1500\" y2=\"180\" class=\"gmaj\"/><line x1=\"0\" y1=\"186\" x2=\"1500\" y2=\"186\" class=\"gmin\"/><line x1=\"0\" y1=\"192\" x2=\"1500\" y2=\"192\" class=\"gmin\"/><line x1=\"0\" y1=\"198\" x2=\"1500\" y2=\"198\" class=\"gmin\"/><line x1=\"0\" y1=\"204\" x2=\"1500\" y2=\"204\" class=\"gmin\"/><line x1=\"0\" y1=\"210\" x2=\"1500\" y2=\"210\" class=\"gmaj\"/><line x1=\"0\" y1=\"216\" x2=\"1500\" y2=\"216\" class=\"gmin\"/><line x1=\"0\" y1=\"222\" x2=\"1500\" y2=\"222\" class=\"gmin\"/><line x1=\"0\" y1=\"228\" x2=\"1500\" y2=\"228\" class=\"gmin\"/><line x1=\"0\" y1=\"234\" x2=\"1500\" y2=\"234\" class=\"gmin\"/><line x1=\"0\" y1=\"240\" x2=\"1500\" y2=\"240\" class=\"gmaj\"/><line x1=\"0\" y1=\"246\" x2=\"1500\" y2=\"246\" class=\"gmin\"/><line x1=\"0\" y1=\"252\" x2=\"1500\" y2=\"252\" class=\"gmin\"/><line x1=\"0\" y1=\"258\" x2=\"1500\" y2=\"258\" class=\"gmin\"/><line x1=\"0\" y1=\"264\" x2=\"1500\" y2=\"264\" class=\"gmin\"/><line x1=\"0\" y1=\"270\" x2=\"1500\" y2=\"270\" class=\"gmaj\"/><line x1=\"0\" y1=\"276\" x2=\"1500\" y2=\"276\" class=\"gmin\"/><line x1=\"0\" y1=\"282\" x2=\"1500\" y2=\"282\" class=\"gmin\"/><line x1=\"0\" y1=\"288\" x2=\"1500\" y2=\"288\" class=\"gmin\"/><line x1=\"0\" y1=\"294\" x2=\"1500\" y2=\"294\" class=\"gmin\"/><line x1=\"0\" y1=\"300\" x2=\"1500\" y2=\"300\" class=\"gmaj\"/><line x1=\"0\" y1=\"306\" x2=\"1500\" y2=\"306\" class=\"gmin\"/><line x1=\"0\" y1=\"312\" x2=\"1500\" y2=\"312\" class=\"gmin\"/><line x1=\"0\" y1=\"318\" x2=\"1500\" y2=\"318\" class=\"gmin\"/><line x1=\"0\" y1=\"324\" x2=\"1500\" y2=\"324\" class=\"gmin\"/><line x1=\"0\" y1=\"330\" x2=\"1500\" y2=\"330\" class=\"gmaj\"/><line x1=\"0\" y1=\"336\" x2=\"1500\" y2=\"336\" class=\"gmin\"/><line x1=\"0\" y1=\"342\" x2=\"1500\" y2=\"342\" class=\"gmin\"/><line x1=\"0\" y1=\"348\" x2=\"1500\" y2=\"348\" class=\"gmin\"/><line x1=\"0\" y1=\"354\" x2=\"1500\" y2=\"354\" class=\"gmin\"/><line x1=\"0\" y1=\"360\" x2=\"1500\" y2=\"360\" class=\"gmaj\"/><line x1=\"0\" y1=\"366\" x2=\"1500\" y2=\"366\" class=\"gmin\"/><line x1=\"0\" y1=\"372\" x2=\"1500\" y2=\"372\" class=\"gmin\"/><line x1=\"0\" y1=\"378\" x2=\"1500\" y2=\"378\" class=\"gmin\"/><line x1=\"0\" y1=\"384\" x2=\"1500\" y2=\"384\" class=\"gmin\"/><line x1=\"0\" y1=\"390\" x2=\"1500\" y2=\"390\" class=\"gmaj\"/><line x1=\"0\" y1=\"396\" x2=\"1500\" y2=\"396\" class=\"gmin\"/><line x1=\"0\" y1=\"402\" x2=\"1500\" y2=\"402\" class=\"gmin\"/><line x1=\"0\" y1=\"408\" x2=\"1500\" y2=\"408\" class=\"gmin\"/><line x1=\"0\" y1=\"414\" x2=\"1500\" y2=\"414\" class=\"gmin\"/><line x1=\"0\" y1=\"420\" x2=\"1500\" y2=\"420\" class=\"gmaj\"/><line x1=\"0\" y1=\"426\" x2=\"1500\" y2=\"426\" class=\"gmin\"/><line x1=\"0\" y1=\"432\" x2=\"1500\" y2=\"432\" class=\"gmin\"/><line x1=\"0\" y1=\"438\" x2=\"1500\" y2=\"438\" class=\"gmin\"/><polyline class=\"trace\" points=\"0.0,68.7 1.5,69.1 3.0,69.3 4.5,69.0 6.0,69.3 7.5,69.6 9.0,70.1 10.5,69.4 12.0,66.9 13.5,66.2 15.0,64.6 16.5,63.3 18.0,63.5 19.5,63.3 21.0,63.4 22.5,63.4 24.0,63.4 25.5,63.9 27.0,64.2 28.5,64.3 30.0,64.6 31.5,64.8 33.0,64.8 34.5,64.8 36.0,64.7 37.5,65.1 39.0,65.4 40.5,65.0 42.0,65.7 43.5,66.1 45.0,65.8 46.5,65.7 48.0,65.5 49.5,65.4 51.0,65.5 52.5,65.2 54.0,65.1 55.5,64.8 57.0,64.9 58.5,65.8 60.0,65.3 61.5,65.2 63.0,64.1 64.5,61.8 66.0,62.0 67.5,61.8 69.0,60.4 70.5,60.4 72.0,61.6 73.5,63.7 75.0,65.2 76.5,65.2 78.0,65.1 79.5,65.0 81.0,65.5 82.5,65.0 84.0,64.4 85.5,55.7 87.0,42.3 88.5,49.3 90.0,60.5 91.5,64.5 93.0,68.7 94.5,72.3 96.0,76.6 97.5,75.6 99.0,72.4 100.5,69.3 102.0,67.3 103.5,67.3 105.0,66.9 106.5,66.8 108.0,66.6 109.5,66.6 111.0,66.6 112.5,66.7 114.0,67.3 115.5,67.9 117.0,67.6 118.5,68.1 120.0,68.5 121.5,68.2 123.0,68.4 124.5,66.9 126.0,65.2 127.5,63.4 129.0,61.9 130.5,61.9 132.0,61.7 133.5,61.5 135.0,61.5 136.5,61.2 138.0,61.3 139.5,61.0 141.0,60.9 142.5,61.2 144.0,61.2 145.5,61.3 147.0,61.5 148.5,62.2 150.0,62.5 151.5,62.0 153.0,61.8 154.5,61.4 156.0,61.1 157.5,61.4 159.0,61.8 160.5,62.0 162.0,62.4 163.5,62.8 165.0,62.5 166.5,61.8 168.0,61.8 169.5,61.8 171.0,61.9 172.5,61.5 174.0,60.6 175.5,60.3 177.0,58.8 178.5,58.0 180.0,57.6 181.5,56.1 183.0,57.1 184.5,59.1 186.0,60.7 187.5,62.4 189.0,62.7 190.5,62.2 192.0,63.0 193.5,62.0 195.0,62.5 196.5,55.6 198.0,40.0 199.5,44.4 201.0,57.5 202.5,63.0 204.0,66.3 205.5,69.3 207.0,73.9 208.5,74.2 210.0,71.7 211.5,68.7 213.0,65.7 214.5,64.8 216.0,64.5 217.5,64.1 219.0,63.9 220.5,63.9 222.0,63.9 223.5,63.9 225.0,64.1 226.5,64.6 228.0,65.0 229.5,65.5 231.0,66.0 232.5,66.0 234.0,65.7 235.5,63.9 237.0,61.6 238.5,60.3 240.0,59.2 241.5,58.9 243.0,58.8 244.5,58.5 246.0,58.4 247.5,57.9 249.0,57.7 250.5,57.9 252.0,57.9 253.5,58.6 255.0,59.2 256.5,59.2 258.0,59.7 259.5,59.4 261.0,59.0 262.5,59.2 264.0,58.6 265.5,58.7 267.0,59.2 268.5,59.6 270.0,60.0 271.5,60.1 273.0,60.0 274.5,60.0 276.0,60.3 277.5,60.2 279.0,60.4 280.5,61.3 282.0,60.3 283.5,58.9 285.0,57.7 286.5,56.8 288.0,56.3 289.5,55.6 291.0,55.0 292.5,54.0 294.0,55.4 295.5,57.1 297.0,57.6 298.5,57.6 300.0,58.3 301.5,58.0 303.0,59.1 304.5,60.6 306.0,60.3 307.5,53.5 309.0,38.0 310.5,41.3 312.0,54.7 313.5,59.9 315.0,62.6 316.5,64.8 318.0,69.0 319.5,69.3 321.0,67.5 322.5,65.1 324.0,63.4 325.5,61.8 327.0,60.3 328.5,60.6 330.0,60.3 331.5,60.3 333.0,60.4 334.5,60.9 336.0,61.5 337.5,62.0 339.0,62.5 340.5,63.0 342.0,63.3 343.5,63.0 345.0,63.4 346.5,62.3 348.0,60.4 349.5,58.5 351.0,56.4 352.5,55.3 354.0,54.6 355.5,54.9 357.0,55.8 358.5,56.4 360.0,56.1 361.5,56.2 363.0,56.6 364.5,57.0 366.0,57.4 367.5,57.3 369.0,57.5 370.5,57.1 372.0,56.6 373.5,56.9\"/><polyline class=\"trace\" points=\"375.0,56.4 376.5,56.1 378.0,56.2 379.5,56.5 381.0,56.4 382.5,56.5 384.0,56.1 385.5,56.7 387.0,58.9 388.5,59.4 390.0,60.7 391.5,61.9 393.0,61.6 394.5,61.6 396.0,61.4 397.5,61.5 399.0,61.4 400.5,61.0 402.0,60.7 403.5,60.6 405.0,60.3 406.5,60.1 408.0,60.1 409.5,60.1 411.0,60.2 412.5,59.8 414.0,59.5 415.5,59.6 417.0,59.1 418.5,58.8 420.0,59.0 421.5,59.1 423.0,59.2 424.5,59.2 426.0,59.2 427.5,59.4 429.0,59.5 430.5,59.7 432.0,59.8 433.5,59.2 435.0,59.4 436.5,59.9 438.0,61.4 439.5,63.7 441.0,64.2 442.5,64.5 444.0,65.0 445.5,64.3 447.0,62.8 448.5,60.6 450.0,58.9 451.5,58.9 453.0,58.9 454.5,59.2 456.0,58.9 457.5,60.2 459.0,61.9 460.5,66.4 462.0,73.7 463.5,66.3 465.0,57.0 466.5,56.8 468.0,55.8 469.5,52.8 471.0,49.0 472.5,49.9 474.0,52.9 475.5,56.0 477.0,57.7 478.5,57.7 480.0,58.0 481.5,58.1 483.0,58.3 484.5,58.3 486.0,58.3 487.5,58.3 489.0,58.0 490.5,57.6 492.0,57.8 493.5,57.7 495.0,57.9 496.5,58.2 498.0,58.3 499.5,59.5 501.0,60.9 502.5,62.5 504.0,63.7 505.5,63.5 507.0,63.5 508.5,63.5 510.0,63.3 511.5,63.4 513.0,63.3 514.5,63.6 516.0,63.7 517.5,63.4 519.0,63.3 520.5,63.1 522.0,63.0 523.5,62.6 525.0,62.5 526.5,62.7 528.0,62.8 529.5,63.0 531.0,63.1 532.5,62.8 534.0,62.5 535.5,62.3 537.0,62.0 538.5,61.7 540.0,61.9 541.5,62.5 543.0,62.4 544.5,62.5 546.0,62.4 547.5,62.9 549.0,64.3 550.5,64.9 552.0,66.3 553.5,66.9 555.0,66.8 556.5,67.7 558.0,66.0 559.5,63.9 561.0,62.4 562.5,60.7 564.0,60.7 565.5,61.1 567.0,60.8 568.5,62.0 570.0,63.2 571.5,67.3 573.0,75.4 574.5,69.9 576.0,58.5 577.5,57.4 579.0,57.7 580.5,55.2 582.0,51.3 583.5,51.1 585.0,53.5 586.5,56.4 588.0,59.2 589.5,60.0 591.0,60.1 592.5,60.4 594.0,60.6 595.5,60.6 597.0,60.6 598.5,60.6 600.0,60.4 601.5,60.2 603.0,60.0 604.5,59.7 606.0,59.8 607.5,59.7 609.0,60.1 610.5,61.9 612.0,63.6 613.5,64.6 615.0,65.5 616.5,65.5 618.0,65.5 619.5,65.5 621.0,65.4 622.5,65.6 624.0,65.5 625.5,65.2 627.0,65.2 628.5,64.6 630.0,64.3 631.5,64.3 633.0,64.2 634.5,64.3 636.0,64.4 637.5,64.2 639.0,64.5 640.5,64.3 642.0,63.9 643.5,63.6 645.0,63.2 646.5,63.0 648.0,63.1 649.5,63.1 651.0,62.8 652.5,62.7 654.0,62.5 655.5,61.8 657.0,63.0 658.5,64.5 660.0,65.9 661.5,66.9 663.0,67.6 664.5,68.5 666.0,68.4 667.5,68.6 669.0,66.9 670.5,64.9 672.0,64.5 673.5,64.4 675.0,63.9 676.5,63.9 678.0,63.2 679.5,62.5 681.0,64.4 682.5,68.2 684.0,76.0 685.5,71.6 687.0,60.7 688.5,59.4 690.0,59.7 691.5,57.8 693.0,54.0 694.5,53.7 696.0,55.6 697.5,58.1 699.0,60.1 700.5,61.3 702.0,62.2 703.5,62.1 705.0,62.4 706.5,62.6 708.0,62.5 709.5,62.1 711.0,61.9 712.5,61.6 714.0,61.4 715.5,61.1 717.0,61.1 718.5,61.6 720.0,61.4 721.5,62.4 723.0,63.8 724.5,65.4 726.0,66.8 727.5,67.5 729.0,68.1 730.5,67.6 732.0,66.7 733.5,66.1 735.0,66.1 736.5,66.0 738.0,65.6 739.5,65.3 741.0,64.9 742.5,65.1 744.0,65.1 745.5,65.2 747.0,65.5 748.5,65.4\"/><polyline class=\"trace\" points=\"750.0,74.2 751.5,75.0 753.0,76.2 754.5,77.4 756.0,78.9 757.5,79.8 759.0,81.4 760.5,82.8 762.0,84.1 763.5,85.6 765.0,85.7 766.5,85.0 768.0,83.8 769.5,81.1 771.0,77.7 772.5,74.7 774.0,71.6 775.5,69.1 777.0,67.7 778.5,67.0 780.0,66.6 781.5,66.2 783.0,65.8 784.5,65.4 786.0,65.1 787.5,64.9 789.0,64.9 790.5,64.9 792.0,64.9 793.5,64.9 795.0,64.6 796.5,64.4 798.0,64.2 799.5,64.0 801.0,63.7 802.5,63.6 804.0,63.4 805.5,63.3 807.0,63.1 808.5,62.9 810.0,62.8 811.5,62.2 813.0,60.9 814.5,60.3 816.0,59.9 817.5,59.2 819.0,60.7 820.5,62.9 822.0,64.0 823.5,63.4 825.0,60.6 826.5,60.1 828.0,60.7 829.5,61.3 831.0,60.9 832.5,59.4 834.0,56.8 835.5,57.4 837.0,59.4 838.5,51.4 840.0,48.3 841.5,45.7 843.0,33.6 844.5,18.3 846.0,8.2 847.5,9.2 849.0,21.4 850.5,43.2 852.0,55.6 853.5,59.9 855.0,63.1 856.5,63.6 858.0,64.3 859.5,64.6 861.0,65.2 862.5,65.8 864.0,66.7 865.5,67.8 867.0,69.4 868.5,70.6 870.0,71.5 871.5,72.8 873.0,74.4 874.5,76.1 876.0,78.1 877.5,79.1 879.0,78.7 880.5,78.2 882.0,76.5 883.5,73.6 885.0,70.5 886.5,66.9 888.0,64.3 889.5,62.3 891.0,60.9 892.5,60.5 894.0,60.2 895.5,59.9 897.0,59.5 898.5,59.2 900.0,59.2 901.5,59.2 903.0,59.2 904.5,59.2 906.0,59.2 907.5,59.1 909.0,58.9 910.5,58.9 912.0,58.7 913.5,58.6 915.0,58.6 916.5,58.4 918.0,58.3 919.5,58.3 921.0,58.3 922.5,57.9 924.0,56.7 925.5,55.2 927.0,55.3 928.5,55.8 930.0,57.5 931.5,60.3 933.0,62.3 934.5,62.0 936.0,59.4 937.5,59.5 939.0,60.1 940.5,60.6 942.0,61.3 943.5,59.9 945.0,56.8 946.5,57.3 948.0,59.2 949.5,52.5 951.0,49.3 952.5,46.6 954.0,35.6 955.5,20.2 957.0,9.2 958.5,8.7 960.0,18.6 961.5,40.1 963.0,54.9 964.5,60.6 966.0,63.0 967.5,63.5 969.0,64.8 970.5,64.6 972.0,64.7 973.5,65.4 975.0,66.3 976.5,66.9 978.0,67.8 979.5,69.0 981.0,70.5 982.5,71.6 984.0,72.6 985.5,74.5 987.0,76.6 988.5,77.7 990.0,77.7 991.5,76.5 993.0,74.3 994.5,71.8 996.0,68.8 997.5,65.6 999.0,62.5 1000.5,60.0 1002.0,58.3 1003.5,57.4 1005.0,57.1 1006.5,56.9 1008.0,56.8 1009.5,56.8 1011.0,56.8 1012.5,56.8 1014.0,56.7 1015.5,56.5 1017.0,56.5 1018.5,56.5 1020.0,56.5 1021.5,56.6 1023.0,55.9 1024.5,55.6 1026.0,55.6 1027.5,55.6 1029.0,55.6 1030.5,55.7 1032.0,55.6 1033.5,55.5 1035.0,54.5 1036.5,52.9 1038.0,53.5 1039.5,53.8 1041.0,54.6 1042.5,57.3 1044.0,59.8 1045.5,59.7 1047.0,56.9 1048.5,57.0 1050.0,57.3 1051.5,57.8 1053.0,58.3 1054.5,57.4 1056.0,54.9 1057.5,53.6 1059.0,56.3 1060.5,50.4 1062.0,46.6 1063.5,45.3 1065.0,35.1 1066.5,20.2 1068.0,8.8 1069.5,7.0 1071.0,14.6 1072.5,36.0 1074.0,52.6 1075.5,58.9 1077.0,62.2 1078.5,63.1 1080.0,64.8 1081.5,64.7 1083.0,64.9 1084.5,65.6 1086.0,66.9 1087.5,68.1 1089.0,69.0 1090.5,70.4 1092.0,72.1 1093.5,73.5 1095.0,75.2 1096.5,77.1 1098.0,78.6 1099.5,80.3 1101.0,80.5 1102.5,79.7 1104.0,78.5 1105.5,75.9 1107.0,72.3 1108.5,69.0 1110.0,66.1 1111.5,63.7 1113.0,62.8 1114.5,62.8 1116.0,62.5 1117.5,62.4 1119.0,62.2 1120.5,62.4 1122.0,62.6 1123.5,62.5\"/><polyline class=\"trace\" points=\"1125.0,75.2 1126.5,76.6 1128.0,78.9 1129.5,81.1 1131.0,83.2 1132.5,84.9 1134.0,86.6 1135.5,86.6 1137.0,85.7 1138.5,84.3 1140.0,81.3 1141.5,77.5 1143.0,73.3 1144.5,68.8 1146.0,64.8 1147.5,61.2 1149.0,58.9 1150.5,58.6 1152.0,58.6 1153.5,58.7 1155.0,58.9 1156.5,58.9 1158.0,59.1 1159.5,59.4 1161.0,59.5 1162.5,59.8 1164.0,60.0 1165.5,60.2 1167.0,60.1 1168.5,59.8 1170.0,60.1 1171.5,60.4 1173.0,60.8 1174.5,61.1 1176.0,61.4 1177.5,61.6 1179.0,61.6 1180.5,61.6 1182.0,61.6 1183.5,61.6 1185.0,61.5 1186.5,60.8 1188.0,59.5 1189.5,58.9 1191.0,58.2 1192.5,57.4 1194.0,57.3 1195.5,57.5 1197.0,59.3 1198.5,62.4 1200.0,63.3 1201.5,63.3 1203.0,63.8 1204.5,63.6 1206.0,64.5 1207.5,62.8 1209.0,60.5 1210.5,47.4 1212.0,34.6 1213.5,58.8 1215.0,80.2 1216.5,69.1 1218.0,53.5 1219.5,48.8 1221.0,57.8 1222.5,66.3 1224.0,69.4 1225.5,71.1 1227.0,70.6 1228.5,70.4 1230.0,70.2 1231.5,69.7 1233.0,69.9 1234.5,70.7 1236.0,71.5 1237.5,73.2 1239.0,75.2 1240.5,76.8 1242.0,79.6 1243.5,81.7 1245.0,83.4 1246.5,85.2 1248.0,85.2 1249.5,84.4 1251.0,84.0 1252.5,82.2 1254.0,78.9 1255.5,75.0 1257.0,70.8 1258.5,66.6 1260.0,62.9 1261.5,60.4 1263.0,59.2 1264.5,58.5 1266.0,58.6 1267.5,59.2 1269.0,59.7 1270.5,60.3 1272.0,60.6 1273.5,60.8 1275.0,61.0 1276.5,61.2 1278.0,61.3 1279.5,61.4 1281.0,61.6 1282.5,61.6 1284.0,61.8 1285.5,62.0 1287.0,61.9 1288.5,62.2 1290.0,62.4 1291.5,62.7 1293.0,62.8 1294.5,63.1 1296.0,62.9 1297.5,61.6 1299.0,61.0 1300.5,60.2 1302.0,58.8 1303.5,58.1 1305.0,58.4 1306.5,59.1 1308.0,60.7 1309.5,62.7 1311.0,63.9 1312.5,64.5 1314.0,65.8 1315.5,65.8 1317.0,66.6 1318.5,64.5 1320.0,60.9 1321.5,50.4 1323.0,35.2 1324.5,55.0 1326.0,80.4 1327.5,71.4 1329.0,54.8 1330.5,48.0 1332.0,55.4 1333.5,65.1 1335.0,68.8 1336.5,71.3 1338.0,71.0 1339.5,70.7 1341.0,70.5 1342.5,70.1 1344.0,70.2 1345.5,70.3 1347.0,71.2 1348.5,72.5 1350.0,74.3 1351.5,76.2 1353.0,78.4 1354.5,80.7 1356.0,82.8 1357.5,84.1 1359.0,83.8 1360.5,83.2 1362.0,82.2 1363.5,80.0 1365.0,77.1 1366.5,73.5 1368.0,69.4 1369.5,65.2 1371.0,61.8 1372.5,59.3 1374.0,57.7 1375.5,57.4 1377.0,57.8 1378.5,58.2 1380.0,58.6 1381.5,59.0 1383.0,59.3 1384.5,59.7 1386.0,60.0 1387.5,60.3 1389.0,60.7 1390.5,61.0 1392.0,61.3 1393.5,61.3 1395.0,61.3 1396.5,61.3 1398.0,61.3 1399.5,61.3 1401.0,61.0 1402.5,61.0 1404.0,61.0 1405.5,61.1 1407.0,61.0 1408.5,61.0 1410.0,59.7 1411.5,58.6 1413.0,58.2 1414.5,57.2 1416.0,57.4 1417.5,58.0 1419.0,59.5 1420.5,62.4 1422.0,63.6 1423.5,63.9 1425.0,64.9 1426.5,64.9 1428.0,66.0 1429.5,64.2 1431.0,61.3 1432.5,51.2 1434.0,35.8 1435.5,53.8 1437.0,79.9 1438.5,72.4 1440.0,54.9 1441.5,46.8 1443.0,53.8 1444.5,64.2 1446.0,68.4 1447.5,70.8 1449.0,71.0 1450.5,70.9 1452.0,70.9 1453.5,70.9 1455.0,70.9 1456.5,71.1 1458.0,71.7 1459.5,72.9 1461.0,75.0 1462.5,76.9 1464.0,79.3 1465.5,81.7 1467.0,83.8 1468.5,85.0 1470.0,86.1 1471.5,85.9 1473.0,84.3 1474.5,82.1 1476.0,79.2 1477.5,76.2 1479.0,71.8 1480.5,67.2 1482.0,63.7 1483.5,60.9 1485.0,59.2 1486.5,58.7 1488.0,59.1 1489.5,59.5 1491.0,60.0 1492.5,60.4 1494.0,60.8 1495.5,61.1 1497.0,61.4 1498.5,61.6\"/><polyline class=\"trace\" points=\"0.0,174.4 1.5,174.7 3.0,174.4 4.5,174.0 6.0,174.0 7.5,173.4 9.0,173.7 10.5,173.3 12.0,171.3 13.5,171.0 15.0,169.9 16.5,169.0 18.0,169.4 19.5,169.4 21.0,169.7 22.5,169.8 24.0,169.9 25.5,170.2 27.0,170.4 28.5,170.5 30.0,170.8 31.5,171.0 33.0,171.0 34.5,171.0 36.0,170.9 37.5,171.3 39.0,171.6 40.5,171.7 42.0,172.1 43.5,172.2 45.0,172.2 46.5,172.2 48.0,172.2 49.5,172.2 51.0,172.2 52.5,172.0 54.0,171.9 55.5,171.7 57.0,171.4 58.5,171.7 60.0,172.0 61.5,171.1 63.0,169.2 64.5,166.9 66.0,165.6 67.5,165.4 69.0,165.6 70.5,167.2 72.0,168.9 73.5,171.0 75.0,172.9 76.5,173.0 78.0,173.2 79.5,172.5 81.0,172.7 82.5,170.7 84.0,167.8 85.5,167.5 87.0,166.2 88.5,174.1 90.0,181.5 91.5,177.8 93.0,175.7 94.5,178.2 96.0,181.3 97.5,180.5 99.0,177.7 100.5,174.8 102.0,173.3 103.5,173.4 105.0,173.1 106.5,173.0 108.0,172.8 109.5,172.8 111.0,172.8 112.5,172.8 114.0,172.8 115.5,172.8 117.0,172.8 118.5,172.4 120.0,171.9 121.5,171.4 123.0,171.0 124.5,170.2 126.0,169.0 127.5,167.7 129.0,166.7 130.5,167.1 132.0,167.4 133.5,167.5 135.0,167.9 136.5,168.0 138.0,168.1 139.5,167.8 141.0,167.7 142.5,168.0 144.0,168.1 145.5,168.4 147.0,168.6 148.5,168.6 150.0,168.6 151.5,168.6 153.0,168.6 154.5,168.6 156.0,168.7 157.5,169.0 159.0,169.2 160.5,169.4 162.0,169.6 163.5,169.9 165.0,169.6 166.5,169.2 168.0,169.3 169.5,169.2 171.0,169.3 172.5,168.7 174.0,166.8 175.5,165.8 177.0,164.5 178.5,164.3 180.0,164.8 181.5,164.5 183.0,166.9 184.5,169.2 186.0,170.5 187.5,172.0 189.0,171.8 190.5,171.5 192.0,171.3 193.5,170.0 195.0,167.1 196.5,165.9 198.0,165.1 199.5,171.9 201.0,181.6 202.5,178.3 204.0,174.1 205.5,176.2 207.0,179.4 208.5,179.6 210.0,177.2 211.5,174.5 213.0,171.9 214.5,171.3 216.0,171.4 217.5,171.1 219.0,171.0 220.5,171.0 222.0,171.1 223.5,171.0 225.0,171.1 226.5,171.0 228.0,171.1 229.5,171.0 231.0,170.5 232.5,170.8 234.0,170.1 235.5,168.4 237.0,167.2 238.5,166.5 240.0,165.9 241.5,166.0 243.0,166.3 244.5,166.5 246.0,166.8 247.5,166.9 249.0,167.2 250.5,167.5 252.0,167.7 253.5,168.0 255.0,168.3 256.5,168.1 258.0,168.0 259.5,168.0 261.0,168.2 262.5,168.3 264.0,168.3 265.5,168.6 267.0,168.9 268.5,169.2 270.0,169.5 271.5,169.8 273.0,169.8 274.5,169.8 276.0,170.1 277.5,170.3 279.0,170.4 280.5,171.0 282.0,169.8 283.5,168.0 285.0,166.6 286.5,165.4 288.0,164.5 289.5,163.5 291.0,164.2 292.5,164.8 294.0,166.8 295.5,168.9 297.0,169.5 298.5,169.6 300.0,170.0 301.5,170.1 303.0,170.5 304.5,170.4 306.0,166.9 307.5,166.0 309.0,165.9 310.5,171.4 312.0,179.8 313.5,177.3 315.0,174.0 316.5,175.6 318.0,178.9 319.5,179.3 321.0,177.1 322.5,174.6 324.0,172.3 325.5,171.7 327.0,171.3 328.5,171.1 330.0,170.8 331.5,170.5 333.0,170.5 334.5,170.8 336.0,170.7 337.5,170.8 339.0,170.7 340.5,170.8 342.0,170.5 343.5,169.8 345.0,169.7 346.5,168.9 348.0,168.0 349.5,166.8 351.0,165.9 352.5,165.7 354.0,165.3 355.5,165.9 357.0,166.7 358.5,167.2 360.0,167.6 361.5,167.8 363.0,168.1 364.5,168.3 366.0,168.7 367.5,168.6 369.0,168.3 370.5,168.3 372.0,168.3 373.5,168.3\"/><polyline class=\"trace\" points=\"375.0,174.3 376.5,174.4 378.0,174.8 379.5,174.7 381.0,175.0 382.5,175.5 384.0,175.9 385.5,175.4 387.0,174.0 388.5,173.4 390.0,172.4 391.5,171.6 393.0,171.6 394.5,171.3 396.0,171.3 397.5,171.2 399.0,171.1 400.5,171.5 402.0,171.7 403.5,171.8 405.0,171.9 406.5,172.0 408.0,172.0 409.5,172.0 411.0,171.9 412.5,172.2 414.0,172.2 415.5,171.8 417.0,172.4 418.5,172.7 420.0,172.3 421.5,172.3 423.0,172.0 424.5,171.9 426.0,172.0 427.5,171.9 429.0,171.9 430.5,171.7 432.0,171.9 433.5,172.7 435.0,171.9 436.5,172.3 438.0,172.3 439.5,171.1 441.0,171.9 442.5,171.8 444.0,170.3 445.5,169.5 447.0,169.9 448.5,170.9 450.0,171.4 451.5,171.4 453.0,171.3 454.5,171.4 456.0,171.9 457.5,172.3 459.0,173.2 460.5,164.7 462.0,151.9 463.5,155.0 465.0,162.5 466.5,168.3 468.0,173.5 469.5,175.8 471.0,178.6 472.5,178.0 474.0,176.3 475.5,174.6 477.0,173.4 478.5,173.2 480.0,173.0 481.5,173.0 483.0,172.9 484.5,172.9 486.0,172.9 487.5,172.9 489.0,173.5 490.5,174.2 492.0,173.9 493.5,174.6 495.0,175.2 496.5,175.2 498.0,175.6 499.5,174.5 501.0,173.4 502.5,172.3 504.0,171.3 505.5,171.1 507.0,170.8 508.5,170.5 510.0,170.2 511.5,169.9 513.0,169.9 514.5,169.8 516.0,169.8 517.5,169.9 519.0,169.8 520.5,169.8 522.0,169.9 523.5,170.7 525.0,170.9 526.5,170.4 528.0,170.2 529.5,169.8 531.0,169.5 532.5,169.6 534.0,169.9 535.5,170.0 537.0,170.3 538.5,170.6 540.0,170.4 541.5,169.9 543.0,169.9 544.5,169.9 546.0,169.9 547.5,169.9 549.0,169.8 550.5,170.1 552.0,169.3 553.5,168.6 555.0,167.9 556.5,166.5 558.0,166.3 559.5,167.2 561.0,168.1 562.5,169.1 564.0,169.5 565.5,169.2 567.0,170.0 568.5,169.6 570.0,171.7 571.5,165.4 573.0,150.2 574.5,151.0 576.0,159.4 577.5,166.5 579.0,171.9 580.5,173.9 582.0,177.0 583.5,177.1 585.0,175.8 586.5,174.1 588.0,172.5 589.5,171.9 591.0,171.5 592.5,171.3 594.0,171.1 595.5,171.1 597.0,171.1 598.5,171.1 600.0,171.3 601.5,171.9 603.0,172.2 604.5,172.8 606.0,173.4 607.5,173.3 609.0,173.3 610.5,172.5 612.0,170.8 613.5,169.7 615.0,168.9 616.5,168.6 618.0,168.3 619.5,168.0 621.0,167.8 622.5,167.1 624.0,166.9 625.5,166.8 627.0,166.8 628.5,167.3 630.0,167.7 631.5,167.9 633.0,168.4 634.5,168.0 636.0,167.6 637.5,167.7 639.0,167.2 640.5,167.1 642.0,167.5 643.5,167.7 645.0,168.0 646.5,168.0 648.0,167.8 649.5,167.8 651.0,168.0 652.5,167.8 654.0,168.0 655.5,168.6 657.0,168.1 658.5,167.7 660.0,167.1 661.5,166.9 663.0,166.8 664.5,166.6 666.0,165.7 667.5,164.3 669.0,164.7 670.5,165.4 672.0,165.6 673.5,165.6 675.0,166.0 676.5,165.6 678.0,166.6 679.5,168.1 681.0,169.6 682.5,163.2 684.0,147.8 685.5,148.3 687.0,157.5 688.5,163.9 690.0,168.3 691.5,169.6 693.0,172.2 694.5,172.3 696.0,171.7 697.5,170.5 699.0,169.9 700.5,168.6 702.0,167.4 703.5,167.8 705.0,167.7 706.5,167.8 708.0,167.9 709.5,168.3 711.0,168.8 712.5,169.3 714.0,169.8 715.5,170.3 717.0,170.7 718.5,170.8 720.0,171.3 721.5,170.5 723.0,169.2 724.5,167.8 726.0,166.2 727.5,165.2 729.0,164.7 730.5,164.7 732.0,165.2 733.5,165.5 735.0,165.0 736.5,165.0 738.0,165.3 739.5,165.6 741.0,165.8 742.5,165.7 744.0,166.0 745.5,165.6 747.0,165.1 748.5,165.4\"/><polyline class=\"trace\" points=\"750.0,182.8 751.5,184.0 753.0,185.9 754.5,188.1 756.0,190.2 757.5,192.3 759.0,194.2 760.5,195.8 762.0,196.6 763.5,195.8 765.0,194.8 766.5,193.0 768.0,189.9 769.5,184.9 771.0,179.1 772.5,173.7 774.0,168.6 775.5,165.4 777.0,163.9 778.5,163.7 780.0,163.3 781.5,163.2 783.0,163.6 784.5,163.8 786.0,164.1 787.5,164.3 789.0,164.6 790.5,164.7 792.0,164.6 793.5,164.7 795.0,164.6 796.5,164.7 798.0,165.0 799.5,165.3 801.0,165.4 802.5,165.7 804.0,165.9 805.5,165.6 807.0,165.6 808.5,165.5 810.0,165.8 811.5,165.1 813.0,163.5 814.5,163.5 816.0,163.5 817.5,163.5 819.0,163.4 820.5,164.1 822.0,165.3 823.5,165.9 825.0,166.4 826.5,167.2 828.0,167.7 829.5,168.6 831.0,169.3 832.5,168.1 834.0,164.5 835.5,158.8 837.0,148.0 838.5,141.0 840.0,148.5 841.5,145.8 843.0,126.7 844.5,112.2 846.0,113.1 847.5,124.0 849.0,144.0 850.5,166.0 852.0,172.6 853.5,174.6 855.0,175.8 856.5,175.6 858.0,176.5 859.5,176.9 861.0,178.3 862.5,179.5 864.0,181.3 865.5,183.1 867.0,186.0 868.5,188.7 870.0,190.9 871.5,193.2 873.0,195.0 874.5,196.8 876.0,197.4 877.5,197.5 879.0,196.8 880.5,194.1 882.0,189.7 883.5,184.6 885.0,178.8 886.5,173.4 888.0,169.1 889.5,166.2 891.0,165.5 892.5,165.3 894.0,165.6 895.5,166.3 897.0,166.7 898.5,167.4 900.0,167.6 901.5,167.8 903.0,168.0 904.5,168.3 906.0,168.5 907.5,168.7 909.0,169.0 910.5,169.2 912.0,169.3 913.5,169.6 915.0,169.8 916.5,169.5 918.0,169.5 919.5,169.5 921.0,169.3 922.5,169.1 924.0,168.4 925.5,167.5 927.0,167.6 928.5,168.0 930.0,168.4 931.5,168.7 933.0,170.7 934.5,172.5 936.0,171.3 937.5,171.6 939.0,172.2 940.5,172.6 942.0,173.8 943.5,172.7 945.0,169.6 946.5,163.8 948.0,154.0 949.5,145.0 951.0,148.7 952.5,150.1 954.0,134.0 955.5,117.0 957.0,116.2 958.5,125.2 960.0,143.5 961.5,167.1 963.0,175.7 964.5,178.2 966.0,179.1 967.5,179.0 969.0,180.3 970.5,180.4 972.0,181.9 973.5,183.2 975.0,185.3 976.5,187.4 978.0,189.6 979.5,192.4 981.0,194.5 982.5,196.8 984.0,198.6 985.5,200.2 987.0,201.4 988.5,200.8 990.0,199.3 991.5,196.7 993.0,192.4 994.5,187.1 996.0,181.6 997.5,176.4 999.0,172.0 1000.5,169.2 1002.0,167.9 1003.5,167.6 1005.0,168.1 1006.5,168.3 1008.0,168.6 1009.5,168.9 1011.0,169.0 1012.5,169.3 1014.0,169.5 1015.5,169.7 1017.0,170.0 1018.5,170.1 1020.0,170.1 1021.5,170.1 1023.0,170.1 1024.5,170.1 1026.0,170.0 1027.5,170.3 1029.0,170.4 1030.5,170.4 1032.0,170.2 1033.5,169.6 1035.0,169.0 1036.5,168.1 1038.0,168.0 1039.5,167.7 1041.0,167.7 1042.5,169.2 1044.0,171.0 1045.5,171.9 1047.0,172.1 1048.5,172.8 1050.0,172.9 1051.5,173.4 1053.0,173.5 1054.5,173.5 1056.0,171.6 1057.5,165.6 1059.0,156.7 1060.5,147.1 1062.0,151.5 1063.5,154.5 1065.0,137.8 1066.5,120.6 1068.0,118.4 1069.5,126.5 1071.0,143.1 1072.5,166.9 1074.0,178.3 1075.5,181.0 1077.0,181.5 1078.5,181.3 1080.0,183.1 1081.5,183.4 1083.0,184.8 1084.5,186.1 1086.0,187.9 1087.5,190.1 1089.0,192.3 1090.5,194.9 1092.0,197.5 1093.5,199.9 1095.0,201.9 1096.5,203.9 1098.0,204.2 1099.5,203.7 1101.0,202.8 1102.5,200.5 1104.0,196.8 1105.5,191.8 1107.0,185.8 1108.5,180.4 1110.0,176.1 1111.5,172.9 1113.0,172.4 1114.5,172.7 1116.0,172.9 1117.5,173.2 1119.0,173.5 1120.5,173.8 1122.0,174.0 1123.5,174.4\"/><polyline class=\"trace\" points=\"1125.0,185.1 1126.5,186.0 1128.0,186.6 1129.5,187.7 1131.0,188.4 1132.5,188.4 1134.0,187.3 1135.5,185.6 1137.0,183.3 1138.5,179.6 1140.0,175.5 1141.5,172.5 1143.0,171.1 1144.5,170.3 1146.0,170.1 1147.5,170.4 1149.0,170.2 1150.5,170.5 1152.0,170.7 1153.5,170.5 1155.0,170.7 1156.5,170.2 1158.0,169.6 1159.5,169.7 1161.0,169.5 1162.5,169.1 1164.0,169.1 1165.5,169.3 1167.0,169.5 1168.5,169.6 1170.0,169.8 1171.5,170.0 1173.0,170.0 1174.5,170.0 1176.0,170.0 1177.5,170.0 1179.0,170.0 1180.5,169.8 1182.0,169.7 1183.5,169.6 1185.0,169.8 1186.5,169.0 1188.0,167.8 1189.5,167.4 1191.0,166.0 1192.5,165.0 1194.0,164.2 1195.5,163.9 1197.0,165.1 1198.5,167.5 1200.0,168.7 1201.5,168.4 1203.0,169.9 1204.5,168.9 1206.0,171.2 1207.5,169.0 1209.0,168.2 1210.5,143.4 1212.0,116.8 1213.5,176.4 1215.0,221.4 1216.5,203.1 1218.0,190.2 1219.5,183.4 1221.0,183.7 1222.5,182.0 1224.0,178.8 1225.5,174.6 1227.0,171.4 1228.5,171.8 1230.0,171.4 1231.5,172.1 1233.0,172.2 1234.5,172.5 1236.0,172.8 1237.5,173.3 1239.0,174.5 1240.5,175.3 1242.0,176.2 1243.5,177.3 1245.0,177.2 1246.5,176.5 1248.0,176.1 1249.5,174.1 1251.0,171.1 1252.5,167.7 1254.0,164.4 1255.5,162.1 1257.0,161.0 1258.5,161.2 1260.0,161.7 1261.5,162.0 1263.0,162.5 1264.5,162.8 1266.0,163.1 1267.5,163.1 1269.0,163.2 1270.5,163.4 1272.0,163.5 1273.5,163.0 1275.0,162.4 1276.5,162.7 1278.0,163.0 1279.5,163.2 1281.0,163.6 1282.5,163.8 1284.0,164.1 1285.5,164.4 1287.0,164.6 1288.5,164.9 1290.0,165.2 1291.5,164.8 1293.0,164.5 1294.5,164.8 1296.0,165.0 1297.5,163.9 1299.0,163.3 1300.5,163.0 1302.0,161.8 1303.5,160.9 1305.0,159.9 1306.5,160.8 1308.0,162.2 1309.5,163.9 1311.0,166.0 1312.5,166.0 1314.0,168.0 1315.5,166.9 1317.0,168.4 1318.5,166.9 1320.0,166.3 1321.5,147.4 1323.0,115.4 1324.5,165.5 1326.0,220.2 1327.5,206.2 1329.0,190.2 1330.5,182.7 1332.0,182.7 1333.5,181.9 1335.0,178.9 1336.5,175.1 1338.0,172.0 1339.5,172.4 1341.0,172.0 1342.5,172.7 1344.0,172.8 1345.5,173.1 1347.0,173.4 1348.5,174.0 1350.0,175.0 1351.5,176.1 1353.0,177.4 1354.5,178.6 1356.0,179.2 1357.5,178.8 1359.0,177.9 1360.5,176.2 1362.0,173.4 1363.5,169.7 1365.0,166.5 1366.5,164.2 1368.0,163.2 1369.5,163.3 1371.0,163.6 1372.5,164.2 1374.0,164.7 1375.5,165.3 1377.0,165.6 1378.5,165.9 1380.0,166.2 1381.5,166.4 1383.0,166.7 1384.5,166.9 1386.0,167.2 1387.5,167.5 1389.0,167.7 1390.5,168.1 1392.0,168.1 1393.5,167.8 1395.0,168.1 1396.5,168.3 1398.0,168.6 1399.5,168.7 1401.0,169.0 1402.5,169.2 1404.0,169.1 1405.5,169.1 1407.0,169.0 1408.5,169.2 1410.0,168.4 1411.5,167.8 1413.0,167.3 1414.5,166.3 1416.0,166.0 1417.5,166.0 1419.0,167.2 1420.5,169.6 1422.0,171.3 1423.5,171.5 1425.0,172.8 1426.5,171.4 1428.0,172.8 1429.5,171.4 1431.0,172.4 1432.5,156.1 1434.0,122.4 1435.5,168.9 1437.0,225.7 1438.5,212.9 1440.0,196.0 1441.5,188.2 1443.0,189.2 1444.5,189.6 1446.0,185.7 1447.5,182.5 1449.0,179.4 1450.5,179.1 1452.0,178.5 1453.5,179.1 1455.0,179.9 1456.5,180.3 1458.0,180.1 1459.5,181.0 1461.0,182.7 1462.5,183.7 1464.0,184.9 1465.5,186.6 1467.0,187.1 1468.5,186.2 1470.0,185.9 1471.5,184.6 1473.0,181.4 1474.5,178.2 1476.0,175.7 1477.5,173.4 1479.0,171.9 1480.5,172.1 1482.0,172.6 1483.5,172.9 1485.0,173.5 1486.5,173.8 1488.0,174.2 1489.5,174.5 1491.0,174.8 1492.5,175.0 1494.0,175.3 1495.5,175.6 1497.0,176.0 1498.5,176.0\"/><polyline class=\"trace\" points=\"0.0,276.6 1.5,276.5 3.0,276.0 4.5,275.9 6.0,275.5 7.5,274.8 9.0,274.5 10.5,274.8 12.0,275.2 13.5,275.7 15.0,276.1 16.5,276.6 18.0,276.8 19.5,277.0 21.0,277.1 22.5,277.3 24.0,277.5 25.5,277.2 27.0,277.1 28.5,277.1 30.0,277.1 31.5,277.1 33.0,277.1 34.5,277.1 36.0,277.2 37.5,277.1 39.0,277.1 40.5,277.6 42.0,277.2 43.5,277.0 45.0,277.3 46.5,277.4 48.0,277.6 49.5,277.8 51.0,277.6 52.5,277.8 54.0,277.6 55.5,277.8 57.0,277.5 58.5,276.7 60.0,277.6 61.5,276.8 63.0,275.9 64.5,276.0 66.0,274.5 67.5,274.5 69.0,276.1 70.5,277.7 72.0,278.2 73.5,278.2 75.0,278.5 76.5,278.7 78.0,279.0 79.5,278.5 81.0,278.1 82.5,276.6 84.0,274.3 85.5,282.6 87.0,294.8 88.5,295.6 90.0,291.9 91.5,284.2 93.0,277.9 94.5,276.9 96.0,275.6 97.5,275.8 99.0,276.1 100.5,276.4 102.0,276.9 103.5,277.0 105.0,277.2 106.5,277.1 108.0,277.1 109.5,277.1 111.0,277.1 112.5,277.0 114.0,276.4 115.5,275.8 117.0,276.1 118.5,275.2 120.0,274.3 121.5,274.1 123.0,273.6 124.5,274.2 126.0,274.7 127.5,275.2 129.0,275.7 130.5,276.0 132.0,276.5 133.5,276.9 135.0,277.3 136.5,277.7 138.0,277.7 139.5,277.7 141.0,277.7 142.5,277.7 144.0,277.8 145.5,278.0 147.0,278.0 148.5,277.3 150.0,277.0 151.5,277.5 153.0,277.8 154.5,278.1 156.0,278.5 157.5,278.5 159.0,278.3 160.5,278.3 162.0,278.1 163.5,277.9 165.0,278.1 166.5,278.2 168.0,278.3 169.5,278.2 171.0,278.4 172.5,278.1 174.0,277.2 175.5,276.4 177.0,276.6 178.5,277.2 180.0,278.1 181.5,279.3 183.0,280.8 184.5,281.0 186.0,280.7 187.5,280.5 189.0,280.0 190.5,280.1 192.0,279.3 193.5,279.0 195.0,275.4 196.5,281.2 198.0,296.0 199.5,298.5 201.0,295.0 202.5,286.3 204.0,278.8 205.5,277.8 207.0,276.4 208.5,276.3 210.0,276.4 211.5,276.7 213.0,277.1 214.5,277.3 216.0,277.8 217.5,277.9 219.0,278.1 220.5,278.0 222.0,278.0 223.5,278.0 225.0,277.9 226.5,277.3 228.0,277.0 229.5,276.3 231.0,275.5 232.5,275.7 234.0,275.4 235.5,275.3 237.0,276.4 238.5,277.2 240.0,277.7 241.5,278.0 243.0,278.5 244.5,278.8 246.0,279.2 247.5,280.0 249.0,280.3 250.5,280.6 252.0,280.7 253.5,280.3 255.0,280.0 256.5,279.7 258.0,279.2 259.5,279.6 261.0,280.2 262.5,280.0 264.0,280.6 265.5,280.8 267.0,280.6 268.5,280.5 270.0,280.3 271.5,280.5 273.0,280.7 274.5,280.7 276.0,280.7 277.5,281.0 279.0,280.9 280.5,280.5 282.0,280.3 283.5,280.0 285.0,279.8 286.5,279.4 288.0,279.1 289.5,278.8 291.0,280.0 292.5,281.7 294.0,282.3 295.5,282.7 297.0,282.8 298.5,282.9 300.0,282.6 301.5,283.0 303.0,282.3 304.5,280.8 306.0,277.5 307.5,283.5 309.0,298.7 310.5,301.0 312.0,296.0 313.5,288.3 315.0,282.3 316.5,281.8 318.0,280.8 319.5,280.9 321.0,280.5 322.5,280.3 324.0,279.9 325.5,280.8 327.0,281.8 328.5,281.3 330.0,281.4 331.5,281.1 333.0,281.0 334.5,280.7 336.0,280.2 337.5,279.7 339.0,279.1 340.5,278.7 342.0,278.2 343.5,277.7 345.0,277.2 346.5,277.5 348.0,278.4 349.5,279.3 351.0,280.4 352.5,281.2 354.0,281.6 355.5,282.0 357.0,281.8 358.5,281.7 360.0,282.4 361.5,282.6 363.0,282.4 364.5,282.3 366.0,282.2 367.5,282.2 369.0,281.7 370.5,282.1 372.0,282.6 373.5,282.4\"/><polyline class=\"trace\" points=\"375.0,279.1 376.5,279.2 378.0,278.8 379.5,278.5 381.0,278.4 382.5,277.7 384.0,277.7 385.5,277.7 387.0,276.9 388.5,277.0 390.0,276.7 391.5,276.4 393.0,276.7 394.5,276.8 396.0,277.0 397.5,277.2 399.0,277.3 400.5,277.3 402.0,277.3 403.5,277.5 405.0,277.6 406.5,277.7 408.0,277.7 409.5,277.6 411.0,277.6 412.5,277.8 414.0,277.9 415.5,278.3 417.0,278.3 418.5,278.2 420.0,278.4 421.5,278.4 423.0,278.5 424.5,278.5 426.0,278.5 427.5,278.5 429.0,278.4 430.5,278.4 432.0,278.1 433.5,277.8 435.0,278.5 436.5,277.6 438.0,276.1 439.5,275.1 441.0,273.7 442.5,273.6 444.0,274.5 445.5,276.1 447.0,277.2 448.5,278.2 450.0,279.3 451.5,279.5 453.0,279.6 454.5,279.1 456.0,279.0 457.5,277.3 459.0,274.7 460.5,278.7 462.0,284.1 463.5,288.4 465.0,290.2 466.5,284.6 468.0,280.4 469.5,281.1 471.0,282.0 472.5,281.8 474.0,280.5 475.5,279.2 477.0,278.7 478.5,278.8 480.0,278.7 481.5,278.7 483.0,278.5 484.5,278.5 486.0,278.5 487.5,278.5 489.0,278.2 490.5,277.9 492.0,278.1 493.5,277.4 495.0,276.7 496.5,276.4 498.0,276.0 499.5,275.8 501.0,275.5 502.5,275.1 504.0,274.8 505.5,275.2 507.0,275.5 508.5,275.8 510.0,276.3 511.5,276.5 513.0,276.5 514.5,276.4 516.0,276.3 517.5,276.5 519.0,276.6 520.5,276.9 522.0,276.9 523.5,276.6 525.0,276.5 526.5,276.7 528.0,276.8 529.5,277.0 531.0,277.2 532.5,277.3 534.0,277.3 535.5,277.5 537.0,277.5 538.5,277.5 540.0,277.5 541.5,277.3 543.0,277.5 544.5,277.3 546.0,277.5 547.5,277.0 549.0,275.7 550.5,274.8 552.0,274.2 553.5,274.4 555.0,275.1 556.5,275.5 558.0,277.5 559.5,278.7 561.0,279.2 562.5,279.9 564.0,279.5 565.5,279.4 567.0,278.9 568.5,278.1 570.0,274.9 571.5,277.2 573.0,284.1 574.5,288.8 576.0,291.9 577.5,285.9 579.0,280.1 580.5,280.6 582.0,281.5 583.5,281.5 585.0,280.3 586.5,279.2 588.0,278.1 589.5,277.9 591.0,278.2 592.5,278.2 594.0,278.1 595.5,278.1 597.0,278.1 598.5,278.1 600.0,278.1 601.5,277.8 603.0,277.6 604.5,277.3 606.0,276.6 607.5,276.9 609.0,276.3 610.5,275.5 612.0,275.5 613.5,275.5 615.0,275.4 616.5,275.7 618.0,276.0 619.5,276.3 621.0,276.6 622.5,277.0 624.0,277.4 625.5,277.6 627.0,277.8 628.5,277.8 630.0,277.8 631.5,277.5 633.0,277.2 634.5,277.5 636.0,277.8 637.5,277.8 639.0,278.1 640.5,278.3 642.0,278.4 643.5,278.4 645.0,278.5 646.5,278.7 648.0,278.8 649.5,278.8 651.0,279.0 652.5,279.3 654.0,279.3 655.5,279.3 657.0,278.7 658.5,277.6 660.0,276.8 661.5,276.0 663.0,275.4 664.5,274.8 666.0,275.7 667.5,276.9 669.0,278.2 670.5,279.4 672.0,279.7 673.5,279.8 675.0,279.9 676.5,280.2 678.0,280.0 679.5,279.1 681.0,275.8 682.5,278.4 684.0,285.9 685.5,289.8 687.0,291.5 688.5,286.4 690.0,281.7 691.5,282.3 693.0,283.5 694.5,283.7 696.0,282.4 697.5,281.0 699.0,279.7 700.5,279.8 702.0,280.2 703.5,279.8 705.0,279.7 706.5,279.4 708.0,279.4 709.5,279.3 711.0,279.0 712.5,278.8 714.0,278.5 715.5,278.4 717.0,278.0 718.5,277.4 720.0,277.0 721.5,276.9 723.0,276.8 724.5,276.6 726.0,276.8 727.5,277.1 729.0,277.0 730.5,277.6 732.0,277.9 733.5,278.1 735.0,278.7 736.5,278.8 738.0,278.9 739.5,278.9 741.0,279.1 742.5,279.0 744.0,278.5 745.5,278.8 747.0,279.1 748.5,279.0\"/><polyline class=\"trace\" points=\"750.0,279.7 751.5,281.3 753.0,284.2 754.5,286.8 756.0,289.7 757.5,292.2 759.0,294.5 760.5,295.9 762.0,296.4 763.5,295.5 765.0,293.3 766.5,291.2 768.0,287.5 769.5,282.1 771.0,276.7 772.5,271.6 774.0,267.9 775.5,266.3 777.0,266.5 778.5,266.9 780.0,267.2 781.5,267.6 783.0,267.8 784.5,268.2 786.0,268.5 787.5,268.8 789.0,269.2 790.5,269.5 792.0,269.8 793.5,270.4 795.0,270.9 796.5,271.5 798.0,272.0 799.5,272.4 801.0,272.7 802.5,273.0 804.0,273.4 805.5,273.7 807.0,273.9 808.5,273.9 810.0,273.9 811.5,273.7 813.0,273.3 814.5,272.7 816.0,272.1 817.5,272.5 819.0,273.0 820.5,273.6 822.0,276.1 823.5,278.6 825.0,278.5 826.5,279.2 828.0,279.9 829.5,280.2 831.0,280.0 832.5,278.0 834.0,275.7 835.5,267.4 837.0,255.7 838.5,257.7 840.0,268.2 841.5,263.3 843.0,245.2 844.5,236.9 846.0,247.7 847.5,261.5 849.0,273.6 850.5,284.4 852.0,287.2 853.5,288.1 855.0,288.5 856.5,289.0 858.0,290.0 859.5,291.3 861.0,292.6 862.5,294.4 864.0,296.5 865.5,298.6 867.0,301.9 868.5,304.4 870.0,306.8 871.5,309.3 873.0,311.1 874.5,311.5 876.0,311.2 877.5,310.5 879.0,308.4 880.5,304.9 882.0,300.0 883.5,294.7 885.0,289.8 886.5,285.3 888.0,282.9 889.5,282.6 891.0,282.3 892.5,281.9 894.0,281.6 895.5,281.2 897.0,281.1 898.5,281.0 900.0,281.5 901.5,281.7 903.0,281.6 904.5,281.7 906.0,281.7 907.5,281.7 909.0,281.7 910.5,281.7 912.0,281.7 913.5,281.7 915.0,281.7 916.5,281.9 918.0,281.7 919.5,281.3 921.0,280.9 922.5,279.7 924.0,278.5 925.5,277.6 927.0,276.9 928.5,276.3 930.0,275.5 931.5,276.4 933.0,279.2 934.5,281.9 936.0,282.3 937.5,282.2 939.0,282.4 940.5,282.1 942.0,282.6 943.5,280.9 945.0,277.2 946.5,270.1 948.0,258.3 949.5,257.3 951.0,268.6 952.5,265.6 954.0,246.9 955.5,236.4 957.0,244.2 958.5,257.8 960.0,270.6 961.5,282.3 963.0,285.7 964.5,287.0 966.0,287.6 967.5,287.2 969.0,287.8 970.5,288.7 972.0,290.4 973.5,291.5 975.0,293.7 976.5,296.1 978.0,298.5 979.5,301.3 981.0,303.7 982.5,306.2 984.0,307.7 985.5,308.5 987.0,308.7 988.5,307.5 990.0,305.1 991.5,301.6 993.0,296.5 994.5,291.3 996.0,285.9 997.5,281.0 999.0,278.3 1000.5,276.9 1002.0,276.9 1003.5,276.9 1005.0,276.6 1006.5,276.6 1008.0,276.5 1009.5,276.7 1011.0,276.9 1012.5,276.9 1014.0,276.7 1015.5,276.6 1017.0,276.6 1018.5,276.4 1020.0,276.2 1021.5,276.1 1023.0,275.9 1024.5,275.7 1026.0,275.6 1027.5,275.4 1029.0,274.9 1030.5,274.5 1032.0,274.1 1033.5,273.8 1035.0,272.5 1036.5,271.5 1038.0,270.9 1039.5,269.4 1041.0,269.7 1042.5,270.1 1044.0,271.7 1045.5,274.2 1047.0,273.6 1048.5,273.7 1050.0,274.3 1051.5,274.6 1053.0,275.5 1054.5,273.9 1056.0,270.6 1057.5,263.1 1059.0,251.7 1060.5,249.6 1062.0,261.2 1063.5,259.8 1065.0,240.5 1066.5,228.7 1068.0,234.6 1069.5,249.2 1071.0,261.1 1072.5,272.2 1074.0,277.5 1075.5,278.3 1077.0,278.8 1078.5,278.7 1080.0,279.7 1081.5,280.4 1083.0,281.1 1084.5,282.4 1086.0,284.5 1087.5,286.5 1089.0,289.0 1090.5,291.7 1092.0,294.3 1093.5,296.1 1095.0,298.3 1096.5,299.7 1098.0,299.4 1099.5,298.2 1101.0,295.8 1102.5,292.8 1104.0,288.0 1105.5,282.2 1107.0,276.9 1108.5,271.9 1110.0,268.5 1111.5,267.1 1113.0,267.3 1114.5,267.7 1116.0,267.9 1117.5,268.2 1119.0,268.5 1120.5,268.7 1122.0,269.1 1123.5,269.3\"/><polyline class=\"trace\" points=\"1125.0,288.6 1126.5,288.9 1128.0,289.2 1129.5,288.7 1131.0,288.3 1132.5,287.8 1134.0,287.6 1135.5,286.9 1137.0,284.7 1138.5,282.2 1140.0,280.1 1141.5,279.0 1143.0,278.3 1144.5,278.3 1146.0,278.7 1147.5,278.9 1149.0,279.2 1150.5,279.5 1152.0,279.7 1153.5,280.0 1155.0,280.5 1156.5,280.3 1158.0,279.9 1159.5,279.7 1161.0,279.3 1162.5,279.4 1164.0,279.6 1165.5,279.5 1167.0,279.9 1168.5,280.2 1170.0,280.2 1171.5,280.1 1173.0,279.9 1174.5,279.9 1176.0,279.7 1177.5,279.5 1179.0,279.6 1180.5,279.6 1182.0,279.6 1183.5,279.6 1185.0,279.2 1186.5,278.8 1188.0,278.4 1189.5,278.1 1191.0,277.3 1192.5,276.0 1194.0,274.9 1195.5,275.0 1197.0,276.1 1198.5,277.9 1200.0,279.8 1201.5,279.9 1203.0,280.6 1204.5,280.0 1206.0,280.9 1207.5,279.3 1209.0,277.9 1210.5,265.1 1212.0,246.7 1213.5,270.9 1215.0,294.6 1216.5,290.7 1218.0,290.0 1219.5,290.7 1221.0,292.3 1222.5,290.3 1224.0,287.4 1225.5,284.4 1227.0,282.1 1228.5,282.2 1230.0,281.6 1231.5,281.6 1233.0,281.1 1234.5,281.1 1236.0,281.4 1237.5,281.3 1239.0,281.6 1240.5,282.0 1242.0,282.7 1243.5,283.3 1245.0,282.9 1246.5,282.0 1248.0,281.1 1249.5,279.3 1251.0,276.6 1252.5,274.0 1254.0,271.9 1255.5,270.4 1257.0,270.5 1258.5,271.2 1260.0,271.9 1261.5,272.5 1263.0,272.8 1264.5,273.1 1266.0,273.3 1267.5,273.6 1269.0,273.9 1270.5,273.9 1272.0,273.9 1273.5,273.9 1275.0,273.9 1276.5,273.9 1278.0,273.9 1279.5,273.9 1281.0,273.9 1282.5,273.9 1284.0,273.9 1285.5,273.9 1287.0,273.9 1288.5,273.9 1290.0,273.9 1291.5,273.9 1293.0,273.9 1294.5,273.9 1296.0,273.9 1297.5,273.0 1299.0,272.5 1300.5,272.3 1302.0,271.0 1303.5,269.8 1305.0,268.9 1306.5,269.0 1308.0,270.1 1309.5,272.1 1311.0,273.7 1312.5,273.4 1314.0,274.2 1315.5,273.8 1317.0,274.7 1318.5,274.4 1320.0,273.2 1321.5,262.9 1323.0,243.0 1324.5,261.7 1326.0,289.3 1327.5,287.4 1329.0,284.7 1330.5,285.8 1332.0,288.3 1333.5,286.8 1335.0,283.5 1336.5,281.1 1338.0,278.1 1339.5,276.8 1341.0,276.6 1342.5,277.2 1344.0,277.5 1345.5,277.9 1347.0,278.3 1348.5,278.7 1350.0,279.3 1351.5,279.7 1353.0,280.3 1354.5,280.8 1356.0,280.3 1357.5,280.0 1359.0,279.1 1360.5,277.2 1362.0,275.3 1363.5,272.7 1365.0,270.4 1366.5,269.5 1368.0,269.7 1369.5,270.3 1371.0,270.8 1372.5,271.5 1374.0,272.1 1375.5,272.8 1377.0,273.4 1378.5,273.8 1380.0,274.1 1381.5,274.4 1383.0,274.8 1384.5,275.1 1386.0,275.4 1387.5,275.4 1389.0,275.4 1390.5,275.7 1392.0,275.7 1393.5,275.8 1395.0,276.0 1396.5,276.1 1398.0,276.3 1399.5,276.5 1401.0,276.6 1402.5,276.3 1404.0,276.3 1405.5,276.3 1407.0,276.2 1408.5,276.4 1410.0,275.9 1411.5,275.4 1413.0,274.5 1414.5,273.7 1416.0,273.2 1417.5,272.8 1419.0,274.1 1420.5,276.0 1422.0,277.1 1423.5,276.8 1425.0,277.6 1426.5,277.5 1428.0,278.2 1429.5,278.4 1431.0,277.6 1432.5,268.0 1434.0,247.8 1435.5,264.7 1437.0,292.3 1438.5,291.0 1440.0,289.2 1441.5,289.8 1443.0,292.0 1444.5,291.4 1446.0,288.3 1447.5,286.2 1449.0,283.6 1450.5,283.0 1452.0,282.8 1453.5,282.9 1455.0,282.9 1456.5,282.8 1458.0,282.9 1459.5,283.0 1461.0,283.8 1462.5,284.8 1464.0,284.9 1465.5,285.4 1467.0,285.7 1468.5,284.8 1470.0,284.0 1471.5,282.0 1473.0,280.0 1474.5,278.0 1476.0,275.7 1477.5,274.6 1479.0,274.5 1480.5,275.0 1482.0,275.7 1483.5,276.3 1485.0,276.7 1486.5,277.1 1488.0,277.5 1489.5,277.9 1491.0,278.2 1492.5,278.7 1494.0,278.8 1495.5,279.3 1497.0,280.2 1498.5,280.2\"/><polyline class=\"trace\" points=\"0.0,389.7 1.5,390.0 3.0,389.8 4.5,389.4 6.0,389.3 7.5,388.8 9.0,389.0 10.5,388.6 12.0,386.6 13.5,386.4 15.0,385.3 16.5,384.3 18.0,384.7 19.5,384.7 21.0,385.0 22.5,385.1 24.0,385.2 25.5,385.5 27.0,385.7 28.5,385.9 30.0,386.2 31.5,386.4 33.0,386.4 34.5,386.3 36.0,386.2 37.5,386.6 39.0,386.9 40.5,387.1 42.0,387.4 43.5,387.6 45.0,387.6 46.5,387.6 48.0,387.6 49.5,387.6 51.0,387.6 52.5,387.4 54.0,387.2 55.5,387.0 57.0,386.8 58.5,387.0 60.0,387.4 61.5,386.4 63.0,384.5 64.5,382.2 66.0,380.9 67.5,380.7 69.0,381.0 70.5,382.5 72.0,384.2 73.5,386.4 75.0,388.2 76.5,388.3 78.0,388.5 79.5,387.9 81.0,388.0 82.5,386.1 84.0,383.2 85.5,382.8 87.0,381.6 88.5,389.4 90.0,396.8 91.5,393.1 93.0,391.0 94.5,393.6 96.0,396.6 97.5,395.8 99.0,393.0 100.5,390.1 102.0,388.6 103.5,388.8 105.0,388.4 106.5,388.3 108.0,388.1 109.5,388.2 111.0,388.2 112.5,388.2 114.0,388.2 115.5,388.2 117.0,388.2 118.5,387.7 120.0,387.3 121.5,386.7 123.0,386.4 124.5,385.5 126.0,384.3 127.5,383.0 129.0,382.0 130.5,382.4 132.0,382.7 133.5,382.9 135.0,383.2 136.5,383.4 138.0,383.4 139.5,383.1 141.0,383.1 142.5,383.4 144.0,383.5 145.5,383.8 147.0,384.0 148.5,384.0 150.0,384.0 151.5,384.0 153.0,384.0 154.5,384.0 156.0,384.0 157.5,384.3 159.0,384.5 160.5,384.7 162.0,384.9 163.5,385.2 165.0,385.0 166.5,384.5 168.0,384.6 169.5,384.5 171.0,384.7 172.5,384.0 174.0,382.2 175.5,381.1 177.0,379.9 178.5,379.6 180.0,380.1 181.5,379.9 183.0,382.3 184.5,384.6 186.0,385.8 187.5,387.4 189.0,387.1 190.5,386.8 192.0,386.7 193.5,385.3 195.0,382.4 196.5,381.2 198.0,380.4 199.5,387.3 201.0,396.9 202.5,393.6 204.0,389.5 205.5,391.6 207.0,394.8 208.5,394.9 210.0,392.5 211.5,389.8 213.0,387.2 214.5,386.6 216.0,386.7 217.5,386.5 219.0,386.4 220.5,386.4 222.0,386.4 223.5,386.3 225.0,386.4 226.5,386.3 228.0,386.4 229.5,386.3 231.0,385.9 232.5,386.1 234.0,385.4 235.5,383.7 237.0,382.6 238.5,381.9 240.0,381.3 241.5,381.4 243.0,381.6 244.5,381.8 246.0,382.1 247.5,382.2 249.0,382.5 250.5,382.9 252.0,383.1 253.5,383.4 255.0,383.6 256.5,383.4 258.0,383.4 259.5,383.4 261.0,383.5 262.5,383.7 264.0,383.7 265.5,384.0 267.0,384.3 268.5,384.5 270.0,384.8 271.5,385.1 273.0,385.1 274.5,385.2 276.0,385.4 277.5,385.6 279.0,385.8 280.5,386.3 282.0,385.1 283.5,383.4 285.0,381.9 286.5,380.7 288.0,379.8 289.5,378.8 291.0,379.5 292.5,380.2 294.0,382.2 295.5,384.3 297.0,384.8 298.5,384.9 300.0,385.3 301.5,385.5 303.0,385.8 304.5,385.8 306.0,382.2 307.5,381.4 309.0,381.2 310.5,386.8 312.0,395.1 313.5,392.7 315.0,389.3 316.5,391.0 318.0,394.3 319.5,394.6 321.0,392.4 322.5,389.9 324.0,387.7 325.5,387.0 327.0,386.6 328.5,386.4 330.0,386.1 331.5,385.8 333.0,385.9 334.5,386.1 336.0,386.0 337.5,386.1 339.0,386.0 340.5,386.1 342.0,385.9 343.5,385.2 345.0,385.0 346.5,384.3 348.0,383.3 349.5,382.2 351.0,381.3 352.5,381.0 354.0,380.6 355.5,381.3 357.0,382.0 358.5,382.6 360.0,382.9 361.5,383.2 363.0,383.5 364.5,383.7 366.0,384.1 367.5,384.0 369.0,383.6 370.5,383.7 372.0,383.7 373.5,383.7 375.0,383.7 376.5,383.8 378.0,384.1 379.5,384.4 381.0,384.7 382.5,384.9 384.0,385.2 385.5,384.7 387.0,384.5 388.5,384.7 390.0,384.9 391.5,385.2 393.0,385.1 394.5,385.1 396.0,383.7 397.5,382.8 399.0,382.3 400.5,379.3 402.0,378.6 403.5,379.3 405.0,380.2 406.5,383.1 408.0,384.6 409.5,385.2 411.0,385.9 412.5,386.5 414.0,386.7 415.5,387.0 417.0,385.9 418.5,383.9 420.0,383.1 421.5,382.9 423.0,389.9 424.5,395.7 426.0,393.0 427.5,391.5 429.0,393.0 430.5,396.9 432.0,397.2 433.5,394.1 435.0,390.9 436.5,387.8 438.0,387.2 439.5,387.3 441.0,387.3 442.5,387.6 444.0,387.6 445.5,387.5 447.0,387.1 448.5,387.7 450.0,388.2 451.5,387.7 453.0,387.3 454.5,386.9 456.0,386.5 457.5,386.2 459.0,385.9 460.5,384.3 462.0,382.8 463.5,383.1 465.0,382.9 466.5,381.9 468.0,382.0 469.5,382.5 471.0,382.8 472.5,383.2 474.0,383.6 475.5,383.9 477.0,384.1 478.5,384.3 480.0,384.5 481.5,384.7 483.0,385.0 484.5,385.2 486.0,385.3 487.5,385.5 489.0,385.6 490.5,385.8 492.0,385.9 493.5,386.1 495.0,386.0 496.5,386.1 498.0,386.1 499.5,386.1 501.0,386.4 502.5,386.3 504.0,386.5 505.5,386.7 507.0,386.7 508.5,385.9 510.0,384.1 511.5,383.2 513.0,381.5 514.5,380.7 516.0,381.5 517.5,382.0 519.0,382.9 520.5,384.7 522.0,387.0 523.5,388.1 525.0,388.8 526.5,388.9 528.0,388.3 529.5,387.2 531.0,384.3 532.5,384.3 534.0,382.8 535.5,384.9 537.0,395.2 538.5,396.6 540.0,391.6 541.5,392.2 543.0,396.3 544.5,397.9 546.0,395.7 547.5,392.6 549.0,390.3 550.5,389.3 552.0,389.0 553.5,389.1 555.0,388.8 556.5,388.7 558.0,388.8 559.5,388.8 561.0,388.8 562.5,388.8 564.0,388.8 565.5,388.8 567.0,388.6 568.5,388.0 570.0,387.5 571.5,387.0 573.0,386.2 574.5,384.9 576.0,383.5 577.5,383.1 579.0,383.4 580.5,383.7 582.0,384.0 583.5,384.3 585.0,384.6 586.5,384.9 588.0,384.9 589.5,384.9 591.0,384.9 592.5,384.9 594.0,385.1 595.5,385.5 597.0,385.8 598.5,386.1 600.0,386.5 601.5,386.5 603.0,386.3 604.5,386.5 606.0,386.8 607.5,387.0 609.0,387.3 610.5,387.1 612.0,387.0 613.5,387.0 615.0,386.7 616.5,386.7 618.0,386.7 619.5,387.6 621.0,386.4 622.5,383.8 624.0,383.0 625.5,381.8 627.0,382.0 628.5,383.0 630.0,383.4 631.5,385.2 633.0,387.0 634.5,387.8 636.0,388.1 637.5,388.9 639.0,389.2 640.5,388.8 642.0,387.2 643.5,384.9 645.0,384.0 646.5,383.9 648.0,392.0 649.5,399.2 651.0,395.2 652.5,392.4 654.0,395.2 655.5,398.5 657.0,397.9 658.5,395.5 660.0,393.1 661.5,391.0 663.0,390.6 664.5,390.6 666.0,390.6 667.5,390.6 669.0,390.6 670.5,390.3 672.0,390.3 673.5,390.3 675.0,390.0 676.5,390.0 678.0,389.9 679.5,389.4 681.0,388.7 682.5,388.2 684.0,387.4 685.5,386.7 687.0,385.5 688.5,384.6 690.0,384.2 691.5,383.5 693.0,384.1 694.5,384.9 696.0,385.5 697.5,385.9 699.0,386.1 700.5,386.4 702.0,386.6 703.5,387.0 705.0,387.1 706.5,387.3 708.0,387.5 709.5,387.6 711.0,387.9 712.5,387.7 714.0,387.6 715.5,387.4 717.0,387.7 718.5,388.8 720.0,388.8 721.5,388.8 723.0,388.8 724.5,388.8 726.0,388.6 727.5,388.1 729.0,387.6 730.5,387.1 732.0,386.7 733.5,385.3 735.0,384.5 736.5,382.9 738.0,381.7 739.5,382.0 741.0,382.2 742.5,385.0 744.0,388.1 745.5,388.9 747.0,388.9 748.5,390.0\"/><text class=\"lead\" x=\"4\" y=\"21\">I</text><text class=\"lead\" x=\"379\" y=\"21\">AVR</text><text class=\"lead\" x=\"754\" y=\"21\">V1</text><text class=\"lead\" x=\"1129\" y=\"21\">V4</text><text class=\"lead\" x=\"4\" y=\"129\">II</text><text class=\"lead\" x=\"379\" y=\"129\">AVL</text><text class=\"lead\" x=\"754\" y=\"129\">V2</text><text class=\"lead\" x=\"1129\" y=\"129\">V5</text><text class=\"lead\" x=\"4\" y=\"237\">III</text><text class=\"lead\" x=\"379\" y=\"237\">AVF</text><text class=\"lead\" x=\"754\" y=\"237\">V3</text><text class=\"lead\" x=\"1129\" y=\"237\">V6</text><text class=\"lead\" x=\"4\" y=\"346\">II (rhythm)</text><text class=\"cap\" x=\"4\" y=\"452\">12유도 · 실데이터(PTB-XL, CC-BY) · 25 mm/s, 10 mm/mV</text></svg>"
 },
 {
  "id": "usmle-2026-0035",
  "exam": "usmle",
  "step": "Step 2",
  "subject": "Internal Medicine",
  "subject_file": "Internal Medicine",
  "subtopic": "Acute STEMI management (12-lead, real ECG)",
  "type": "Acute STEMI management (12-lead, real ECG)",
  "difficulty": 4,
  "created": "2026-07-07",
  "vignette": "A 58-year-old man arrives 60 minutes after the onset of severe crushing chest pain with diaphoresis. He is hemodynamically stable. His 12-lead electrocardiogram is shown and a high-sensitivity troponin is elevated. A cardiac catheterization laboratory is available on site.",
  "question": "Which of the following is the most appropriate next step?",
  "options": [
   "Immediate reperfusion with primary percutaneous coronary intervention",
   "High-dose NSAIDs and observation for pericarditis",
   "Repeat the ECG and troponin in 6 hours before deciding",
   "Outpatient exercise stress test after discharge",
   "Anticoagulation alone without reperfusion"
  ],
  "answer": 1,
  "explanationText": "- 정답근거: 허혈성 흉통 + 12유도 급성 ST 상승 + 트로포닌 상승 = 급성\n  STEMI. 근치는 막힌 관동맥을 최대한 빨리 여는 재관류이며, PCI 시설이 있으니\n  일차적 PCI가 최우선(door-to-balloon 최소화).\n- 오답감별(낚시 주의): (B) 심막염은 광범위 오목형 ST상승·PR하강 — 국소\n  ST상승·허혈흉통과 다르며 NSAID로 흘리면 위험. (C) 6시간 후 재검은 재관류를\n  지연시키는 대표 함정(시간=심근). (D) 급성기 외래 스트레스검사는 금기. (E)\n  항응고만으로는 폐색을 열지 못한다.\n- 임상핵심: STEMI = 즉시 재관류(PCI 가능 → 일차적 PCI, 불가·지연 시\n  섬유소용해). aspirin·P2Y12·항응고·통증조절 병행. 재관류를 늦추는 선택은 오답.\n- 자료 관련: 12유도는 오픈 DB(PTB-XL, CC-BY)의 실제 급성 MI 기록을 렌더한\n  것(도식화 레이아웃). 모양 기반 진단이라 합성 대신 실데이터 사용.\n- 출처: PTB-XL (PhysioNet); ACC/AHA STEMI guideline.",
  "explanationItems": [
   {
    "k": "정답근거",
    "v": "허혈성 흉통 + 12유도 급성 ST 상승 + 트로포닌 상승 = 급성 STEMI. 근치는 막힌 관동맥을 최대한 빨리 여는 재관류이며, PCI 시설이 있으니 일차적 PCI가 최우선(door-to-balloon 최소화)."
   },
   {
    "k": "오답감별(낚시 주의)",
    "v": "(B) 심막염은 광범위 오목형 ST상승·PR하강 — 국소 ST상승·허혈흉통과 다르며 NSAID로 흘리면 위험. (C) 6시간 후 재검은 재관류를 지연시키는 대표 함정(시간=심근). (D) 급성기 외래 스트레스검사는 금기. (E) 항응고만으로는 폐색을 열지 못한다."
   },
   {
    "k": "임상핵심",
    "v": "STEMI = 즉시 재관류(PCI 가능 → 일차적 PCI, 불가·지연 시 섬유소용해). aspirin·P2Y12·항응고·통증조절 병행. 재관류를 늦추는 선택은 오답."
   },
   {
    "k": "자료 관련",
    "v": "12유도는 오픈 DB(PTB-XL, CC-BY)의 실제 급성 MI 기록을 렌더한 것(도식화 레이아웃). 모양 기반 진단이라 합성 대신 실데이터 사용."
   },
   {
    "k": "출처",
    "v": "PTB-XL (PhysioNet); ACC/AHA STEMI guideline."
   }
  ],
  "source": "USMLE-style / MedKOS · ECG: PTB-XL 1.0.3 (PhysioNet, CC-BY 4.0)",
  "vitals": [],
  "labs": [],
  "appendix": {
   "가이드라인": "급성 흉통 + ST 상승 접근\n─────────────────────────────\nSTEMI 확진(허혈흉통 + 국소 ST상승 ± 트로포닌↑)\n  → 재관류: PCI 가능 → 일차적 PCI(최우선)\n            PCI 불가/지연(>120분) → 섬유소용해제\n  + 보조: aspirin·P2Y12·항응고·통증조절\n감별: 심막염(광범위 오목 ST상승·PR하강), 조기재분극, 대동맥박리(재관류 금기)\n※ 재관류를 지연시키는 선택(추적 후 결정·외래검사)은 오답.\n",
   "최신지견": "door-to-balloon ≤90분 목표. 새 CLBBB + 허혈흉통도 STEMI-equivalent로 재관류 고려.",
   "참고문헌": [
    "PTB-XL (PhysioNet, CC-BY 4.0)",
    "ACC/AHA STEMI Guideline"
   ]
  },
  "figureSvg": "<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 1500 456\" width=\"1500\" height=\"456\" role=\"img\" aria-label=\"12-lead ECG 12유도 · 실데이터(PTB-XL, CC-BY) · 급성 심근경색\"><style>.bg{fill:#fff}.gmin{stroke:#f4c9c9;stroke-width:0.5}.gmaj{stroke:#e59a9a;stroke-width:1}.trace{fill:none;stroke:#111;stroke-width:1.2;stroke-linejoin:round}.lead{font:bold 11px sans-serif;fill:#333}.cap{font:11px sans-serif;fill:#555}</style><rect class=\"bg\" x=\"0\" y=\"0\" width=\"1500\" height=\"440\"/><line x1=\"0\" y1=\"0\" x2=\"0\" y2=\"440\" class=\"gmaj\"/><line x1=\"6\" y1=\"0\" x2=\"6\" y2=\"440\" class=\"gmin\"/><line x1=\"12\" y1=\"0\" x2=\"12\" y2=\"440\" class=\"gmin\"/><line x1=\"18\" y1=\"0\" x2=\"18\" y2=\"440\" class=\"gmin\"/><line x1=\"24\" y1=\"0\" x2=\"24\" y2=\"440\" class=\"gmin\"/><line x1=\"30\" y1=\"0\" x2=\"30\" y2=\"440\" class=\"gmaj\"/><line x1=\"36\" y1=\"0\" x2=\"36\" y2=\"440\" class=\"gmin\"/><line x1=\"42\" y1=\"0\" x2=\"42\" y2=\"440\" class=\"gmin\"/><line x1=\"48\" y1=\"0\" x2=\"48\" y2=\"440\" class=\"gmin\"/><line x1=\"54\" y1=\"0\" x2=\"54\" y2=\"440\" class=\"gmin\"/><line x1=\"60\" y1=\"0\" x2=\"60\" y2=\"440\" class=\"gmaj\"/><line x1=\"66\" y1=\"0\" x2=\"66\" y2=\"440\" class=\"gmin\"/><line x1=\"72\" y1=\"0\" x2=\"72\" y2=\"440\" class=\"gmin\"/><line x1=\"78\" y1=\"0\" x2=\"78\" y2=\"440\" class=\"gmin\"/><line x1=\"84\" y1=\"0\" x2=\"84\" y2=\"440\" class=\"gmin\"/><line x1=\"90\" y1=\"0\" x2=\"90\" y2=\"440\" class=\"gmaj\"/><line x1=\"96\" y1=\"0\" x2=\"96\" y2=\"440\" class=\"gmin\"/><line x1=\"102\" y1=\"0\" x2=\"102\" y2=\"440\" class=\"gmin\"/><line x1=\"108\" y1=\"0\" x2=\"108\" y2=\"440\" class=\"gmin\"/><line x1=\"114\" y1=\"0\" x2=\"114\" y2=\"440\" class=\"gmin\"/><line x1=\"120\" y1=\"0\" x2=\"120\" y2=\"440\" class=\"gmaj\"/><line x1=\"126\" y1=\"0\" x2=\"126\" y2=\"440\" class=\"gmin\"/><line x1=\"132\" y1=\"0\" x2=\"132\" y2=\"440\" class=\"gmin\"/><line x1=\"138\" y1=\"0\" x2=\"138\" y2=\"440\" class=\"gmin\"/><line x1=\"144\" y1=\"0\" x2=\"144\" y2=\"440\" class=\"gmin\"/><line x1=\"150\" y1=\"0\" x2=\"150\" y2=\"440\" class=\"gmaj\"/><line x1=\"156\" y1=\"0\" x2=\"156\" y2=\"440\" class=\"gmin\"/><line x1=\"162\" y1=\"0\" x2=\"162\" y2=\"440\" class=\"gmin\"/><line x1=\"168\" y1=\"0\" x2=\"168\" y2=\"440\" class=\"gmin\"/><line x1=\"174\" y1=\"0\" x2=\"174\" y2=\"440\" class=\"gmin\"/><line x1=\"180\" y1=\"0\" x2=\"180\" y2=\"440\" class=\"gmaj\"/><line x1=\"186\" y1=\"0\" x2=\"186\" y2=\"440\" class=\"gmin\"/><line x1=\"192\" y1=\"0\" x2=\"192\" y2=\"440\" class=\"gmin\"/><line x1=\"198\" y1=\"0\" x2=\"198\" y2=\"440\" class=\"gmin\"/><line x1=\"204\" y1=\"0\" x2=\"204\" y2=\"440\" class=\"gmin\"/><line x1=\"210\" y1=\"0\" x2=\"210\" y2=\"440\" class=\"gmaj\"/><line x1=\"216\" y1=\"0\" x2=\"216\" y2=\"440\" class=\"gmin\"/><line x1=\"222\" y1=\"0\" x2=\"222\" y2=\"440\" class=\"gmin\"/><line x1=\"228\" y1=\"0\" x2=\"228\" y2=\"440\" class=\"gmin\"/><line x1=\"234\" y1=\"0\" x2=\"234\" y2=\"440\" class=\"gmin\"/><line x1=\"240\" y1=\"0\" x2=\"240\" y2=\"440\" class=\"gmaj\"/><line x1=\"246\" y1=\"0\" x2=\"246\" y2=\"440\" class=\"gmin\"/><line x1=\"252\" y1=\"0\" x2=\"252\" y2=\"440\" class=\"gmin\"/><line x1=\"258\" y1=\"0\" x2=\"258\" y2=\"440\" class=\"gmin\"/><line x1=\"264\" y1=\"0\" x2=\"264\" y2=\"440\" class=\"gmin\"/><line x1=\"270\" y1=\"0\" x2=\"270\" y2=\"440\" class=\"gmaj\"/><line x1=\"276\" y1=\"0\" x2=\"276\" y2=\"440\" class=\"gmin\"/><line x1=\"282\" y1=\"0\" x2=\"282\" y2=\"440\" class=\"gmin\"/><line x1=\"288\" y1=\"0\" x2=\"288\" y2=\"440\" class=\"gmin\"/><line x1=\"294\" y1=\"0\" x2=\"294\" y2=\"440\" class=\"gmin\"/><line x1=\"300\" y1=\"0\" x2=\"300\" y2=\"440\" class=\"gmaj\"/><line x1=\"306\" y1=\"0\" x2=\"306\" y2=\"440\" class=\"gmin\"/><line x1=\"312\" y1=\"0\" x2=\"312\" y2=\"440\" class=\"gmin\"/><line x1=\"318\" y1=\"0\" x2=\"318\" y2=\"440\" class=\"gmin\"/><line x1=\"324\" y1=\"0\" x2=\"324\" y2=\"440\" class=\"gmin\"/><line x1=\"330\" y1=\"0\" x2=\"330\" y2=\"440\" class=\"gmaj\"/><line x1=\"336\" y1=\"0\" x2=\"336\" y2=\"440\" class=\"gmin\"/><line x1=\"342\" y1=\"0\" x2=\"342\" y2=\"440\" class=\"gmin\"/><line x1=\"348\" y1=\"0\" x2=\"348\" y2=\"440\" class=\"gmin\"/><line x1=\"354\" y1=\"0\" x2=\"354\" y2=\"440\" class=\"gmin\"/><line x1=\"360\" y1=\"0\" x2=\"360\" y2=\"440\" class=\"gmaj\"/><line x1=\"366\" y1=\"0\" x2=\"366\" y2=\"440\" class=\"gmin\"/><line x1=\"372\" y1=\"0\" x2=\"372\" y2=\"440\" class=\"gmin\"/><line x1=\"378\" y1=\"0\" x2=\"378\" y2=\"440\" class=\"gmin\"/><line x1=\"384\" y1=\"0\" x2=\"384\" y2=\"440\" class=\"gmin\"/><line x1=\"390\" y1=\"0\" x2=\"390\" y2=\"440\" class=\"gmaj\"/><line x1=\"396\" y1=\"0\" x2=\"396\" y2=\"440\" class=\"gmin\"/><line x1=\"402\" y1=\"0\" x2=\"402\" y2=\"440\" class=\"gmin\"/><line x1=\"408\" y1=\"0\" x2=\"408\" y2=\"440\" class=\"gmin\"/><line x1=\"414\" y1=\"0\" x2=\"414\" y2=\"440\" class=\"gmin\"/><line x1=\"420\" y1=\"0\" x2=\"420\" y2=\"440\" class=\"gmaj\"/><line x1=\"426\" y1=\"0\" x2=\"426\" y2=\"440\" class=\"gmin\"/><line x1=\"432\" y1=\"0\" x2=\"432\" y2=\"440\" class=\"gmin\"/><line x1=\"438\" y1=\"0\" x2=\"438\" y2=\"440\" class=\"gmin\"/><line x1=\"444\" y1=\"0\" x2=\"444\" y2=\"440\" class=\"gmin\"/><line x1=\"450\" y1=\"0\" x2=\"450\" y2=\"440\" class=\"gmaj\"/><line x1=\"456\" y1=\"0\" x2=\"456\" y2=\"440\" class=\"gmin\"/><line x1=\"462\" y1=\"0\" x2=\"462\" y2=\"440\" class=\"gmin\"/><line x1=\"468\" y1=\"0\" x2=\"468\" y2=\"440\" class=\"gmin\"/><line x1=\"474\" y1=\"0\" x2=\"474\" y2=\"440\" class=\"gmin\"/><line x1=\"480\" y1=\"0\" x2=\"480\" y2=\"440\" class=\"gmaj\"/><line x1=\"486\" y1=\"0\" x2=\"486\" y2=\"440\" class=\"gmin\"/><line x1=\"492\" y1=\"0\" x2=\"492\" y2=\"440\" class=\"gmin\"/><line x1=\"498\" y1=\"0\" x2=\"498\" y2=\"440\" class=\"gmin\"/><line x1=\"504\" y1=\"0\" x2=\"504\" y2=\"440\" class=\"gmin\"/><line x1=\"510\" y1=\"0\" x2=\"510\" y2=\"440\" class=\"gmaj\"/><line x1=\"516\" y1=\"0\" x2=\"516\" y2=\"440\" class=\"gmin\"/><line x1=\"522\" y1=\"0\" x2=\"522\" y2=\"440\" class=\"gmin\"/><line x1=\"528\" y1=\"0\" x2=\"528\" y2=\"440\" class=\"gmin\"/><line x1=\"534\" y1=\"0\" x2=\"534\" y2=\"440\" class=\"gmin\"/><line x1=\"540\" y1=\"0\" x2=\"540\" y2=\"440\" class=\"gmaj\"/><line x1=\"546\" y1=\"0\" x2=\"546\" y2=\"440\" class=\"gmin\"/><line x1=\"552\" y1=\"0\" x2=\"552\" y2=\"440\" class=\"gmin\"/><line x1=\"558\" y1=\"0\" x2=\"558\" y2=\"440\" class=\"gmin\"/><line x1=\"564\" y1=\"0\" x2=\"564\" y2=\"440\" class=\"gmin\"/><line x1=\"570\" y1=\"0\" x2=\"570\" y2=\"440\" class=\"gmaj\"/><line x1=\"576\" y1=\"0\" x2=\"576\" y2=\"440\" class=\"gmin\"/><line x1=\"582\" y1=\"0\" x2=\"582\" y2=\"440\" class=\"gmin\"/><line x1=\"588\" y1=\"0\" x2=\"588\" y2=\"440\" class=\"gmin\"/><line x1=\"594\" y1=\"0\" x2=\"594\" y2=\"440\" class=\"gmin\"/><line x1=\"600\" y1=\"0\" x2=\"600\" y2=\"440\" class=\"gmaj\"/><line x1=\"606\" y1=\"0\" x2=\"606\" y2=\"440\" class=\"gmin\"/><line x1=\"612\" y1=\"0\" x2=\"612\" y2=\"440\" class=\"gmin\"/><line x1=\"618\" y1=\"0\" x2=\"618\" y2=\"440\" class=\"gmin\"/><line x1=\"624\" y1=\"0\" x2=\"624\" y2=\"440\" class=\"gmin\"/><line x1=\"630\" y1=\"0\" x2=\"630\" y2=\"440\" class=\"gmaj\"/><line x1=\"636\" y1=\"0\" x2=\"636\" y2=\"440\" class=\"gmin\"/><line x1=\"642\" y1=\"0\" x2=\"642\" y2=\"440\" class=\"gmin\"/><line x1=\"648\" y1=\"0\" x2=\"648\" y2=\"440\" class=\"gmin\"/><line x1=\"654\" y1=\"0\" x2=\"654\" y2=\"440\" class=\"gmin\"/><line x1=\"660\" y1=\"0\" x2=\"660\" y2=\"440\" class=\"gmaj\"/><line x1=\"666\" y1=\"0\" x2=\"666\" y2=\"440\" class=\"gmin\"/><line x1=\"672\" y1=\"0\" x2=\"672\" y2=\"440\" class=\"gmin\"/><line x1=\"678\" y1=\"0\" x2=\"678\" y2=\"440\" class=\"gmin\"/><line x1=\"684\" y1=\"0\" x2=\"684\" y2=\"440\" class=\"gmin\"/><line x1=\"690\" y1=\"0\" x2=\"690\" y2=\"440\" class=\"gmaj\"/><line x1=\"696\" y1=\"0\" x2=\"696\" y2=\"440\" class=\"gmin\"/><line x1=\"702\" y1=\"0\" x2=\"702\" y2=\"440\" class=\"gmin\"/><line x1=\"708\" y1=\"0\" x2=\"708\" y2=\"440\" class=\"gmin\"/><line x1=\"714\" y1=\"0\" x2=\"714\" y2=\"440\" class=\"gmin\"/><line x1=\"720\" y1=\"0\" x2=\"720\" y2=\"440\" class=\"gmaj\"/><line x1=\"726\" y1=\"0\" x2=\"726\" y2=\"440\" class=\"gmin\"/><line x1=\"732\" y1=\"0\" x2=\"732\" y2=\"440\" class=\"gmin\"/><line x1=\"738\" y1=\"0\" x2=\"738\" y2=\"440\" class=\"gmin\"/><line x1=\"744\" y1=\"0\" x2=\"744\" y2=\"440\" class=\"gmin\"/><line x1=\"750\" y1=\"0\" x2=\"750\" y2=\"440\" class=\"gmaj\"/><line x1=\"756\" y1=\"0\" x2=\"756\" y2=\"440\" class=\"gmin\"/><line x1=\"762\" y1=\"0\" x2=\"762\" y2=\"440\" class=\"gmin\"/><line x1=\"768\" y1=\"0\" x2=\"768\" y2=\"440\" class=\"gmin\"/><line x1=\"774\" y1=\"0\" x2=\"774\" y2=\"440\" class=\"gmin\"/><line x1=\"780\" y1=\"0\" x2=\"780\" y2=\"440\" class=\"gmaj\"/><line x1=\"786\" y1=\"0\" x2=\"786\" y2=\"440\" class=\"gmin\"/><line x1=\"792\" y1=\"0\" x2=\"792\" y2=\"440\" class=\"gmin\"/><line x1=\"798\" y1=\"0\" x2=\"798\" y2=\"440\" class=\"gmin\"/><line x1=\"804\" y1=\"0\" x2=\"804\" y2=\"440\" class=\"gmin\"/><line x1=\"810\" y1=\"0\" x2=\"810\" y2=\"440\" class=\"gmaj\"/><line x1=\"816\" y1=\"0\" x2=\"816\" y2=\"440\" class=\"gmin\"/><line x1=\"822\" y1=\"0\" x2=\"822\" y2=\"440\" class=\"gmin\"/><line x1=\"828\" y1=\"0\" x2=\"828\" y2=\"440\" class=\"gmin\"/><line x1=\"834\" y1=\"0\" x2=\"834\" y2=\"440\" class=\"gmin\"/><line x1=\"840\" y1=\"0\" x2=\"840\" y2=\"440\" class=\"gmaj\"/><line x1=\"846\" y1=\"0\" x2=\"846\" y2=\"440\" class=\"gmin\"/><line x1=\"852\" y1=\"0\" x2=\"852\" y2=\"440\" class=\"gmin\"/><line x1=\"858\" y1=\"0\" x2=\"858\" y2=\"440\" class=\"gmin\"/><line x1=\"864\" y1=\"0\" x2=\"864\" y2=\"440\" class=\"gmin\"/><line x1=\"870\" y1=\"0\" x2=\"870\" y2=\"440\" class=\"gmaj\"/><line x1=\"876\" y1=\"0\" x2=\"876\" y2=\"440\" class=\"gmin\"/><line x1=\"882\" y1=\"0\" x2=\"882\" y2=\"440\" class=\"gmin\"/><line x1=\"888\" y1=\"0\" x2=\"888\" y2=\"440\" class=\"gmin\"/><line x1=\"894\" y1=\"0\" x2=\"894\" y2=\"440\" class=\"gmin\"/><line x1=\"900\" y1=\"0\" x2=\"900\" y2=\"440\" class=\"gmaj\"/><line x1=\"906\" y1=\"0\" x2=\"906\" y2=\"440\" class=\"gmin\"/><line x1=\"912\" y1=\"0\" x2=\"912\" y2=\"440\" class=\"gmin\"/><line x1=\"918\" y1=\"0\" x2=\"918\" y2=\"440\" class=\"gmin\"/><line x1=\"924\" y1=\"0\" x2=\"924\" y2=\"440\" class=\"gmin\"/><line x1=\"930\" y1=\"0\" x2=\"930\" y2=\"440\" class=\"gmaj\"/><line x1=\"936\" y1=\"0\" x2=\"936\" y2=\"440\" class=\"gmin\"/><line x1=\"942\" y1=\"0\" x2=\"942\" y2=\"440\" class=\"gmin\"/><line x1=\"948\" y1=\"0\" x2=\"948\" y2=\"440\" class=\"gmin\"/><line x1=\"954\" y1=\"0\" x2=\"954\" y2=\"440\" class=\"gmin\"/><line x1=\"960\" y1=\"0\" x2=\"960\" y2=\"440\" class=\"gmaj\"/><line x1=\"966\" y1=\"0\" x2=\"966\" y2=\"440\" class=\"gmin\"/><line x1=\"972\" y1=\"0\" x2=\"972\" y2=\"440\" class=\"gmin\"/><line x1=\"978\" y1=\"0\" x2=\"978\" y2=\"440\" class=\"gmin\"/><line x1=\"984\" y1=\"0\" x2=\"984\" y2=\"440\" class=\"gmin\"/><line x1=\"990\" y1=\"0\" x2=\"990\" y2=\"440\" class=\"gmaj\"/><line x1=\"996\" y1=\"0\" x2=\"996\" y2=\"440\" class=\"gmin\"/><line x1=\"1002\" y1=\"0\" x2=\"1002\" y2=\"440\" class=\"gmin\"/><line x1=\"1008\" y1=\"0\" x2=\"1008\" y2=\"440\" class=\"gmin\"/><line x1=\"1014\" y1=\"0\" x2=\"1014\" y2=\"440\" class=\"gmin\"/><line x1=\"1020\" y1=\"0\" x2=\"1020\" y2=\"440\" class=\"gmaj\"/><line x1=\"1026\" y1=\"0\" x2=\"1026\" y2=\"440\" class=\"gmin\"/><line x1=\"1032\" y1=\"0\" x2=\"1032\" y2=\"440\" class=\"gmin\"/><line x1=\"1038\" y1=\"0\" x2=\"1038\" y2=\"440\" class=\"gmin\"/><line x1=\"1044\" y1=\"0\" x2=\"1044\" y2=\"440\" class=\"gmin\"/><line x1=\"1050\" y1=\"0\" x2=\"1050\" y2=\"440\" class=\"gmaj\"/><line x1=\"1056\" y1=\"0\" x2=\"1056\" y2=\"440\" class=\"gmin\"/><line x1=\"1062\" y1=\"0\" x2=\"1062\" y2=\"440\" class=\"gmin\"/><line x1=\"1068\" y1=\"0\" x2=\"1068\" y2=\"440\" class=\"gmin\"/><line x1=\"1074\" y1=\"0\" x2=\"1074\" y2=\"440\" class=\"gmin\"/><line x1=\"1080\" y1=\"0\" x2=\"1080\" y2=\"440\" class=\"gmaj\"/><line x1=\"1086\" y1=\"0\" x2=\"1086\" y2=\"440\" class=\"gmin\"/><line x1=\"1092\" y1=\"0\" x2=\"1092\" y2=\"440\" class=\"gmin\"/><line x1=\"1098\" y1=\"0\" x2=\"1098\" y2=\"440\" class=\"gmin\"/><line x1=\"1104\" y1=\"0\" x2=\"1104\" y2=\"440\" class=\"gmin\"/><line x1=\"1110\" y1=\"0\" x2=\"1110\" y2=\"440\" class=\"gmaj\"/><line x1=\"1116\" y1=\"0\" x2=\"1116\" y2=\"440\" class=\"gmin\"/><line x1=\"1122\" y1=\"0\" x2=\"1122\" y2=\"440\" class=\"gmin\"/><line x1=\"1128\" y1=\"0\" x2=\"1128\" y2=\"440\" class=\"gmin\"/><line x1=\"1134\" y1=\"0\" x2=\"1134\" y2=\"440\" class=\"gmin\"/><line x1=\"1140\" y1=\"0\" x2=\"1140\" y2=\"440\" class=\"gmaj\"/><line x1=\"1146\" y1=\"0\" x2=\"1146\" y2=\"440\" class=\"gmin\"/><line x1=\"1152\" y1=\"0\" x2=\"1152\" y2=\"440\" class=\"gmin\"/><line x1=\"1158\" y1=\"0\" x2=\"1158\" y2=\"440\" class=\"gmin\"/><line x1=\"1164\" y1=\"0\" x2=\"1164\" y2=\"440\" class=\"gmin\"/><line x1=\"1170\" y1=\"0\" x2=\"1170\" y2=\"440\" class=\"gmaj\"/><line x1=\"1176\" y1=\"0\" x2=\"1176\" y2=\"440\" class=\"gmin\"/><line x1=\"1182\" y1=\"0\" x2=\"1182\" y2=\"440\" class=\"gmin\"/><line x1=\"1188\" y1=\"0\" x2=\"1188\" y2=\"440\" class=\"gmin\"/><line x1=\"1194\" y1=\"0\" x2=\"1194\" y2=\"440\" class=\"gmin\"/><line x1=\"1200\" y1=\"0\" x2=\"1200\" y2=\"440\" class=\"gmaj\"/><line x1=\"1206\" y1=\"0\" x2=\"1206\" y2=\"440\" class=\"gmin\"/><line x1=\"1212\" y1=\"0\" x2=\"1212\" y2=\"440\" class=\"gmin\"/><line x1=\"1218\" y1=\"0\" x2=\"1218\" y2=\"440\" class=\"gmin\"/><line x1=\"1224\" y1=\"0\" x2=\"1224\" y2=\"440\" class=\"gmin\"/><line x1=\"1230\" y1=\"0\" x2=\"1230\" y2=\"440\" class=\"gmaj\"/><line x1=\"1236\" y1=\"0\" x2=\"1236\" y2=\"440\" class=\"gmin\"/><line x1=\"1242\" y1=\"0\" x2=\"1242\" y2=\"440\" class=\"gmin\"/><line x1=\"1248\" y1=\"0\" x2=\"1248\" y2=\"440\" class=\"gmin\"/><line x1=\"1254\" y1=\"0\" x2=\"1254\" y2=\"440\" class=\"gmin\"/><line x1=\"1260\" y1=\"0\" x2=\"1260\" y2=\"440\" class=\"gmaj\"/><line x1=\"1266\" y1=\"0\" x2=\"1266\" y2=\"440\" class=\"gmin\"/><line x1=\"1272\" y1=\"0\" x2=\"1272\" y2=\"440\" class=\"gmin\"/><line x1=\"1278\" y1=\"0\" x2=\"1278\" y2=\"440\" class=\"gmin\"/><line x1=\"1284\" y1=\"0\" x2=\"1284\" y2=\"440\" class=\"gmin\"/><line x1=\"1290\" y1=\"0\" x2=\"1290\" y2=\"440\" class=\"gmaj\"/><line x1=\"1296\" y1=\"0\" x2=\"1296\" y2=\"440\" class=\"gmin\"/><line x1=\"1302\" y1=\"0\" x2=\"1302\" y2=\"440\" class=\"gmin\"/><line x1=\"1308\" y1=\"0\" x2=\"1308\" y2=\"440\" class=\"gmin\"/><line x1=\"1314\" y1=\"0\" x2=\"1314\" y2=\"440\" class=\"gmin\"/><line x1=\"1320\" y1=\"0\" x2=\"1320\" y2=\"440\" class=\"gmaj\"/><line x1=\"1326\" y1=\"0\" x2=\"1326\" y2=\"440\" class=\"gmin\"/><line x1=\"1332\" y1=\"0\" x2=\"1332\" y2=\"440\" class=\"gmin\"/><line x1=\"1338\" y1=\"0\" x2=\"1338\" y2=\"440\" class=\"gmin\"/><line x1=\"1344\" y1=\"0\" x2=\"1344\" y2=\"440\" class=\"gmin\"/><line x1=\"1350\" y1=\"0\" x2=\"1350\" y2=\"440\" class=\"gmaj\"/><line x1=\"1356\" y1=\"0\" x2=\"1356\" y2=\"440\" class=\"gmin\"/><line x1=\"1362\" y1=\"0\" x2=\"1362\" y2=\"440\" class=\"gmin\"/><line x1=\"1368\" y1=\"0\" x2=\"1368\" y2=\"440\" class=\"gmin\"/><line x1=\"1374\" y1=\"0\" x2=\"1374\" y2=\"440\" class=\"gmin\"/><line x1=\"1380\" y1=\"0\" x2=\"1380\" y2=\"440\" class=\"gmaj\"/><line x1=\"1386\" y1=\"0\" x2=\"1386\" y2=\"440\" class=\"gmin\"/><line x1=\"1392\" y1=\"0\" x2=\"1392\" y2=\"440\" class=\"gmin\"/><line x1=\"1398\" y1=\"0\" x2=\"1398\" y2=\"440\" class=\"gmin\"/><line x1=\"1404\" y1=\"0\" x2=\"1404\" y2=\"440\" class=\"gmin\"/><line x1=\"1410\" y1=\"0\" x2=\"1410\" y2=\"440\" class=\"gmaj\"/><line x1=\"1416\" y1=\"0\" x2=\"1416\" y2=\"440\" class=\"gmin\"/><line x1=\"1422\" y1=\"0\" x2=\"1422\" y2=\"440\" class=\"gmin\"/><line x1=\"1428\" y1=\"0\" x2=\"1428\" y2=\"440\" class=\"gmin\"/><line x1=\"1434\" y1=\"0\" x2=\"1434\" y2=\"440\" class=\"gmin\"/><line x1=\"1440\" y1=\"0\" x2=\"1440\" y2=\"440\" class=\"gmaj\"/><line x1=\"1446\" y1=\"0\" x2=\"1446\" y2=\"440\" class=\"gmin\"/><line x1=\"1452\" y1=\"0\" x2=\"1452\" y2=\"440\" class=\"gmin\"/><line x1=\"1458\" y1=\"0\" x2=\"1458\" y2=\"440\" class=\"gmin\"/><line x1=\"1464\" y1=\"0\" x2=\"1464\" y2=\"440\" class=\"gmin\"/><line x1=\"1470\" y1=\"0\" x2=\"1470\" y2=\"440\" class=\"gmaj\"/><line x1=\"1476\" y1=\"0\" x2=\"1476\" y2=\"440\" class=\"gmin\"/><line x1=\"1482\" y1=\"0\" x2=\"1482\" y2=\"440\" class=\"gmin\"/><line x1=\"1488\" y1=\"0\" x2=\"1488\" y2=\"440\" class=\"gmin\"/><line x1=\"1494\" y1=\"0\" x2=\"1494\" y2=\"440\" class=\"gmin\"/><line x1=\"1500\" y1=\"0\" x2=\"1500\" y2=\"440\" class=\"gmaj\"/><line x1=\"0\" y1=\"0\" x2=\"1500\" y2=\"0\" class=\"gmaj\"/><line x1=\"0\" y1=\"6\" x2=\"1500\" y2=\"6\" class=\"gmin\"/><line x1=\"0\" y1=\"12\" x2=\"1500\" y2=\"12\" class=\"gmin\"/><line x1=\"0\" y1=\"18\" x2=\"1500\" y2=\"18\" class=\"gmin\"/><line x1=\"0\" y1=\"24\" x2=\"1500\" y2=\"24\" class=\"gmin\"/><line x1=\"0\" y1=\"30\" x2=\"1500\" y2=\"30\" class=\"gmaj\"/><line x1=\"0\" y1=\"36\" x2=\"1500\" y2=\"36\" class=\"gmin\"/><line x1=\"0\" y1=\"42\" x2=\"1500\" y2=\"42\" class=\"gmin\"/><line x1=\"0\" y1=\"48\" x2=\"1500\" y2=\"48\" class=\"gmin\"/><line x1=\"0\" y1=\"54\" x2=\"1500\" y2=\"54\" class=\"gmin\"/><line x1=\"0\" y1=\"60\" x2=\"1500\" y2=\"60\" class=\"gmaj\"/><line x1=\"0\" y1=\"66\" x2=\"1500\" y2=\"66\" class=\"gmin\"/><line x1=\"0\" y1=\"72\" x2=\"1500\" y2=\"72\" class=\"gmin\"/><line x1=\"0\" y1=\"78\" x2=\"1500\" y2=\"78\" class=\"gmin\"/><line x1=\"0\" y1=\"84\" x2=\"1500\" y2=\"84\" class=\"gmin\"/><line x1=\"0\" y1=\"90\" x2=\"1500\" y2=\"90\" class=\"gmaj\"/><line x1=\"0\" y1=\"96\" x2=\"1500\" y2=\"96\" class=\"gmin\"/><line x1=\"0\" y1=\"102\" x2=\"1500\" y2=\"102\" class=\"gmin\"/><line x1=\"0\" y1=\"108\" x2=\"1500\" y2=\"108\" class=\"gmin\"/><line x1=\"0\" y1=\"114\" x2=\"1500\" y2=\"114\" class=\"gmin\"/><line x1=\"0\" y1=\"120\" x2=\"1500\" y2=\"120\" class=\"gmaj\"/><line x1=\"0\" y1=\"126\" x2=\"1500\" y2=\"126\" class=\"gmin\"/><line x1=\"0\" y1=\"132\" x2=\"1500\" y2=\"132\" class=\"gmin\"/><line x1=\"0\" y1=\"138\" x2=\"1500\" y2=\"138\" class=\"gmin\"/><line x1=\"0\" y1=\"144\" x2=\"1500\" y2=\"144\" class=\"gmin\"/><line x1=\"0\" y1=\"150\" x2=\"1500\" y2=\"150\" class=\"gmaj\"/><line x1=\"0\" y1=\"156\" x2=\"1500\" y2=\"156\" class=\"gmin\"/><line x1=\"0\" y1=\"162\" x2=\"1500\" y2=\"162\" class=\"gmin\"/><line x1=\"0\" y1=\"168\" x2=\"1500\" y2=\"168\" class=\"gmin\"/><line x1=\"0\" y1=\"174\" x2=\"1500\" y2=\"174\" class=\"gmin\"/><line x1=\"0\" y1=\"180\" x2=\"1500\" y2=\"180\" class=\"gmaj\"/><line x1=\"0\" y1=\"186\" x2=\"1500\" y2=\"186\" class=\"gmin\"/><line x1=\"0\" y1=\"192\" x2=\"1500\" y2=\"192\" class=\"gmin\"/><line x1=\"0\" y1=\"198\" x2=\"1500\" y2=\"198\" class=\"gmin\"/><line x1=\"0\" y1=\"204\" x2=\"1500\" y2=\"204\" class=\"gmin\"/><line x1=\"0\" y1=\"210\" x2=\"1500\" y2=\"210\" class=\"gmaj\"/><line x1=\"0\" y1=\"216\" x2=\"1500\" y2=\"216\" class=\"gmin\"/><line x1=\"0\" y1=\"222\" x2=\"1500\" y2=\"222\" class=\"gmin\"/><line x1=\"0\" y1=\"228\" x2=\"1500\" y2=\"228\" class=\"gmin\"/><line x1=\"0\" y1=\"234\" x2=\"1500\" y2=\"234\" class=\"gmin\"/><line x1=\"0\" y1=\"240\" x2=\"1500\" y2=\"240\" class=\"gmaj\"/><line x1=\"0\" y1=\"246\" x2=\"1500\" y2=\"246\" class=\"gmin\"/><line x1=\"0\" y1=\"252\" x2=\"1500\" y2=\"252\" class=\"gmin\"/><line x1=\"0\" y1=\"258\" x2=\"1500\" y2=\"258\" class=\"gmin\"/><line x1=\"0\" y1=\"264\" x2=\"1500\" y2=\"264\" class=\"gmin\"/><line x1=\"0\" y1=\"270\" x2=\"1500\" y2=\"270\" class=\"gmaj\"/><line x1=\"0\" y1=\"276\" x2=\"1500\" y2=\"276\" class=\"gmin\"/><line x1=\"0\" y1=\"282\" x2=\"1500\" y2=\"282\" class=\"gmin\"/><line x1=\"0\" y1=\"288\" x2=\"1500\" y2=\"288\" class=\"gmin\"/><line x1=\"0\" y1=\"294\" x2=\"1500\" y2=\"294\" class=\"gmin\"/><line x1=\"0\" y1=\"300\" x2=\"1500\" y2=\"300\" class=\"gmaj\"/><line x1=\"0\" y1=\"306\" x2=\"1500\" y2=\"306\" class=\"gmin\"/><line x1=\"0\" y1=\"312\" x2=\"1500\" y2=\"312\" class=\"gmin\"/><line x1=\"0\" y1=\"318\" x2=\"1500\" y2=\"318\" class=\"gmin\"/><line x1=\"0\" y1=\"324\" x2=\"1500\" y2=\"324\" class=\"gmin\"/><line x1=\"0\" y1=\"330\" x2=\"1500\" y2=\"330\" class=\"gmaj\"/><line x1=\"0\" y1=\"336\" x2=\"1500\" y2=\"336\" class=\"gmin\"/><line x1=\"0\" y1=\"342\" x2=\"1500\" y2=\"342\" class=\"gmin\"/><line x1=\"0\" y1=\"348\" x2=\"1500\" y2=\"348\" class=\"gmin\"/><line x1=\"0\" y1=\"354\" x2=\"1500\" y2=\"354\" class=\"gmin\"/><line x1=\"0\" y1=\"360\" x2=\"1500\" y2=\"360\" class=\"gmaj\"/><line x1=\"0\" y1=\"366\" x2=\"1500\" y2=\"366\" class=\"gmin\"/><line x1=\"0\" y1=\"372\" x2=\"1500\" y2=\"372\" class=\"gmin\"/><line x1=\"0\" y1=\"378\" x2=\"1500\" y2=\"378\" class=\"gmin\"/><line x1=\"0\" y1=\"384\" x2=\"1500\" y2=\"384\" class=\"gmin\"/><line x1=\"0\" y1=\"390\" x2=\"1500\" y2=\"390\" class=\"gmaj\"/><line x1=\"0\" y1=\"396\" x2=\"1500\" y2=\"396\" class=\"gmin\"/><line x1=\"0\" y1=\"402\" x2=\"1500\" y2=\"402\" class=\"gmin\"/><line x1=\"0\" y1=\"408\" x2=\"1500\" y2=\"408\" class=\"gmin\"/><line x1=\"0\" y1=\"414\" x2=\"1500\" y2=\"414\" class=\"gmin\"/><line x1=\"0\" y1=\"420\" x2=\"1500\" y2=\"420\" class=\"gmaj\"/><line x1=\"0\" y1=\"426\" x2=\"1500\" y2=\"426\" class=\"gmin\"/><line x1=\"0\" y1=\"432\" x2=\"1500\" y2=\"432\" class=\"gmin\"/><line x1=\"0\" y1=\"438\" x2=\"1500\" y2=\"438\" class=\"gmin\"/><polyline class=\"trace\" points=\"0.0,58.2 1.5,59.5 3.0,62.7 4.5,56.8 6.0,60.7 7.5,59.7 9.0,62.7 10.5,64.0 12.0,59.1 13.5,62.0 15.0,65.1 16.5,64.2 18.0,61.9 19.5,63.7 21.0,65.1 22.5,65.3 24.0,61.7 25.5,64.9 27.0,66.7 28.5,59.9 30.0,61.5 31.5,61.5 33.0,64.0 34.5,62.0 36.0,60.2 37.5,63.4 39.0,59.2 40.5,59.4 42.0,57.0 43.5,57.9 45.0,62.1 46.5,60.0 48.0,59.2 49.5,58.8 51.0,61.5 52.5,60.7 54.0,60.3 55.5,61.8 57.0,55.7 58.5,43.9 60.0,45.1 61.5,55.3 63.0,55.0 64.5,62.2 66.0,62.6 67.5,59.5 69.0,63.4 70.5,60.3 72.0,62.7 73.5,60.5 75.0,57.9 76.5,61.5 78.0,61.7 79.5,59.1 81.0,62.1 82.5,61.8 84.0,58.3 85.5,61.0 87.0,56.1 88.5,53.5 90.0,58.3 91.5,59.8 93.0,58.8 94.5,60.4 96.0,61.2 97.5,61.4 99.0,62.1 100.5,63.1 102.0,61.5 103.5,57.0 105.0,60.4 106.5,60.7 108.0,61.3 109.5,63.8 111.0,62.0 112.5,61.9 114.0,62.1 115.5,62.7 117.0,59.1 118.5,56.0 120.0,55.7 121.5,53.7 123.0,53.2 124.5,53.3 126.0,57.1 127.5,61.1 129.0,57.9 130.5,56.6 132.0,60.4 133.5,63.2 135.0,64.8 136.5,54.0 138.0,40.0 139.5,42.6 141.0,51.9 142.5,56.4 144.0,58.3 145.5,59.4 147.0,60.0 148.5,63.3 150.0,62.5 151.5,59.8 153.0,60.9 154.5,58.9 156.0,59.5 157.5,64.4 159.0,64.3 160.5,64.7 162.0,63.8 163.5,59.4 165.0,62.8 166.5,61.2 168.0,62.5 169.5,64.9 171.0,59.1 172.5,61.3 174.0,66.3 175.5,68.5 177.0,61.9 178.5,61.9 180.0,67.5 181.5,66.7 183.0,64.6 184.5,64.2 186.0,65.5 187.5,60.1 189.0,59.5 190.5,60.0 192.0,62.1 193.5,65.2 195.0,59.3 196.5,56.9 198.0,57.3 199.5,58.6 201.0,57.4 202.5,57.1 204.0,59.8 205.5,59.8 207.0,60.1 208.5,62.3 210.0,64.2 211.5,63.9 213.0,66.7 214.5,66.8 216.0,57.3 217.5,40.3 219.0,41.4 220.5,53.8 222.0,56.1 223.5,62.4 225.0,62.7 226.5,61.4 228.0,64.0 229.5,64.2 231.0,63.6 232.5,59.7 234.0,58.3 235.5,61.5 237.0,62.7 238.5,59.4 240.0,60.0 241.5,60.4 243.0,60.1 244.5,61.9 246.0,61.2 247.5,64.1 249.0,65.2 250.5,63.0 252.0,64.0 253.5,66.7 255.0,70.2 256.5,68.2 258.0,66.2 259.5,69.9 261.0,69.7 262.5,66.5 264.0,66.8 265.5,65.3 267.0,64.0 268.5,65.7 270.0,65.3 271.5,67.4 273.0,64.8 274.5,61.4 276.0,59.8 277.5,57.3 279.0,60.5 280.5,61.8 282.0,62.8 283.5,64.8 285.0,64.8 286.5,65.9 288.0,69.3 289.5,62.1 291.0,58.6 292.5,66.8 294.0,62.6 295.5,49.3 297.0,44.8 298.5,54.7 300.0,61.0 301.5,61.6 303.0,64.2 304.5,65.9 306.0,63.4 307.5,63.1 309.0,65.1 310.5,64.6 312.0,60.0 313.5,58.9 315.0,66.3 316.5,65.4 318.0,63.4 319.5,62.4 321.0,63.3 322.5,66.9 324.0,63.4 325.5,66.0 327.0,66.6 328.5,63.0 330.0,65.9 331.5,64.9 333.0,67.3 334.5,68.3 336.0,68.1 337.5,68.7 339.0,64.8 340.5,66.5 342.0,66.8 343.5,66.2 345.0,67.1 346.5,67.8 348.0,64.1 349.5,62.5 351.0,63.8 352.5,66.4 354.0,68.0 355.5,62.7 357.0,63.3 358.5,62.1 360.0,59.4 361.5,60.4 363.0,63.6 364.5,68.2 366.0,69.1 367.5,66.7 369.0,62.4 370.5,66.1 372.0,68.0 373.5,59.5\"/><polyline class=\"trace\" points=\"375.0,62.7 376.5,63.1 378.0,60.3 379.5,66.3 381.0,63.3 382.5,63.0 384.0,62.1 385.5,62.3 387.0,66.3 388.5,66.1 390.0,62.8 391.5,63.1 393.0,65.5 394.5,63.3 396.0,62.5 397.5,60.1 399.0,62.8 400.5,61.6 402.0,60.0 403.5,64.8 405.0,63.0 406.5,63.4 408.0,61.4 409.5,63.8 411.0,66.4 412.5,63.7 414.0,67.5 415.5,66.7 417.0,66.1 418.5,66.6 420.0,64.3 421.5,64.8 423.0,63.4 424.5,64.2 426.0,63.0 427.5,61.8 429.0,60.8 430.5,59.1 432.0,74.8 433.5,94.5 435.0,92.0 436.5,78.0 438.0,70.6 439.5,61.5 441.0,59.2 442.5,60.7 444.0,57.4 445.5,58.7 447.0,57.1 448.5,59.5 450.0,62.3 451.5,59.4 453.0,59.1 454.5,62.0 456.0,59.3 457.5,59.9 459.0,63.7 460.5,60.9 462.0,65.8 463.5,68.7 465.0,64.7 466.5,63.7 468.0,65.4 469.5,64.5 471.0,62.8 472.5,61.5 474.0,60.9 475.5,61.3 477.0,62.1 478.5,65.2 480.0,62.6 481.5,62.1 483.0,61.9 484.5,60.5 486.0,61.9 487.5,61.0 489.0,63.6 490.5,64.3 492.0,65.6 493.5,68.1 495.0,67.0 496.5,67.6 498.0,68.5 499.5,68.5 501.0,65.4 502.5,61.1 504.0,63.2 505.5,64.3 507.0,62.7 508.5,59.6 510.0,57.1 511.5,80.4 513.0,101.2 514.5,93.3 516.0,79.8 517.5,69.9 519.0,64.3 520.5,61.5 522.0,60.7 523.5,57.8 525.0,58.6 526.5,60.9 528.0,60.0 529.5,62.8 531.0,61.0 532.5,58.2 534.0,58.7 535.5,56.8 537.0,59.1 538.5,63.5 540.0,61.9 541.5,62.8 543.0,61.3 544.5,59.9 546.0,65.1 547.5,63.4 549.0,59.3 550.5,58.2 552.0,63.1 553.5,62.8 555.0,56.8 556.5,58.0 558.0,60.0 559.5,59.7 561.0,60.0 562.5,62.7 564.0,63.6 565.5,64.5 567.0,61.8 568.5,60.6 570.0,68.3 571.5,68.8 573.0,65.9 574.5,64.9 576.0,65.5 577.5,65.7 579.0,63.9 580.5,64.2 582.0,63.1 583.5,62.1 585.0,61.2 586.5,61.9 588.0,61.2 589.5,59.2 591.0,76.1 592.5,99.2 594.0,94.2 595.5,79.1 597.0,71.6 598.5,63.4 600.0,60.6 601.5,59.9 603.0,59.0 604.5,59.0 606.0,58.8 607.5,61.3 609.0,63.8 610.5,62.2 612.0,60.3 613.5,63.7 615.0,63.8 616.5,63.6 618.0,63.9 619.5,62.6 621.0,64.8 622.5,63.1 624.0,62.2 625.5,64.8 627.0,64.2 628.5,61.6 630.0,58.3 631.5,60.3 633.0,61.5 634.5,57.4 636.0,58.5 637.5,61.0 639.0,59.4 640.5,61.8 642.0,63.2 643.5,60.4 645.0,61.2 646.5,60.2 648.0,63.7 649.5,66.6 651.0,66.7 652.5,68.4 654.0,63.6 655.5,63.5 657.0,64.1 658.5,61.8 660.0,61.5 661.5,60.3 663.0,56.3 664.5,60.9 666.0,65.4 667.5,56.2 669.0,64.1 670.5,88.8 672.0,98.4 673.5,84.2 675.0,70.0 676.5,65.3 678.0,59.0 679.5,57.1 681.0,59.7 682.5,58.4 684.0,57.3 685.5,58.2 687.0,60.5 688.5,62.5 690.0,57.6 691.5,56.8 693.0,59.8 694.5,61.3 696.0,59.4 697.5,57.7 699.0,62.4 700.5,60.5 702.0,60.1 703.5,63.4 705.0,60.7 706.5,61.0 708.0,59.8 709.5,58.5 711.0,57.4 712.5,57.4 714.0,59.7 715.5,58.2 717.0,58.0 718.5,58.0 720.0,56.8 721.5,56.2 723.0,59.7 724.5,60.4 726.0,60.9 727.5,60.0 729.0,58.7 730.5,62.9 732.0,60.2 733.5,60.9 735.0,63.6 736.5,61.9 738.0,59.2 739.5,54.7 741.0,54.5 742.5,55.6 744.0,59.2 745.5,56.1 747.0,52.6 748.5,71.0\"/><polyline class=\"trace\" points=\"750.0,56.0 751.5,55.7 753.0,55.8 754.5,55.5 756.0,54.6 757.5,55.2 759.0,56.7 760.5,59.7 762.0,62.0 763.5,62.5 765.0,62.9 766.5,64.4 768.0,66.6 769.5,66.7 771.0,67.7 772.5,67.2 774.0,66.4 775.5,67.9 777.0,66.3 778.5,65.3 780.0,64.9 781.5,63.4 783.0,62.8 784.5,59.5 786.0,55.8 787.5,56.6 789.0,63.7 790.5,70.6 792.0,69.5 793.5,67.1 795.0,66.6 796.5,65.6 798.0,64.0 799.5,62.5 801.0,61.8 802.5,62.2 804.0,61.5 805.5,63.1 807.0,95.0 808.5,147.6 810.0,145.4 811.5,97.8 813.0,71.7 814.5,60.9 816.0,54.8 817.5,53.9 819.0,52.8 820.5,52.2 822.0,50.4 823.5,49.3 825.0,49.0 826.5,48.9 828.0,48.7 829.5,48.9 831.0,48.7 832.5,47.6 834.0,47.5 835.5,49.5 837.0,51.6 838.5,52.0 840.0,53.2 841.5,55.6 843.0,57.1 844.5,57.4 846.0,59.6 847.5,60.9 849.0,58.8 850.5,58.5 852.0,58.2 853.5,57.8 855.0,57.6 856.5,57.0 858.0,57.4 859.5,58.0 861.0,57.4 862.5,56.4 864.0,54.4 865.5,51.0 867.0,52.4 868.5,58.8 870.0,62.8 871.5,63.1 873.0,62.4 874.5,60.6 876.0,59.2 877.5,59.2 879.0,59.7 880.5,59.4 882.0,60.1 883.5,57.5 885.0,53.5 886.5,100.6 888.0,158.0 889.5,141.4 891.0,93.9 892.5,71.1 894.0,57.6 895.5,52.3 897.0,50.5 898.5,50.9 900.0,49.6 901.5,48.9 903.0,49.2 904.5,48.0 906.0,47.4 907.5,45.6 909.0,45.4 910.5,45.6 912.0,45.4 913.5,45.6 915.0,45.6 916.5,48.4 918.0,51.1 919.5,53.2 921.0,55.7 922.5,58.9 924.0,60.7 925.5,60.3 927.0,61.0 928.5,61.9 930.0,62.1 931.5,62.7 933.0,62.8 934.5,62.4 936.0,62.3 937.5,63.1 939.0,61.9 940.5,61.0 942.0,62.1 943.5,58.8 945.0,55.5 946.5,56.2 948.0,63.1 949.5,69.9 951.0,69.3 952.5,69.4 954.0,68.4 955.5,65.7 957.0,64.7 958.5,65.0 960.0,65.5 961.5,65.8 963.0,65.8 964.5,61.6 966.0,96.6 967.5,158.0 969.0,156.8 970.5,104.5 972.0,79.2 973.5,66.4 975.0,59.5 976.5,58.2 978.0,59.4 979.5,57.8 981.0,55.3 982.5,55.9 984.0,55.3 985.5,55.5 987.0,55.2 988.5,55.0 990.0,55.2 991.5,55.1 993.0,56.9 994.5,57.6 996.0,56.1 997.5,60.3 999.0,65.4 1000.5,64.6 1002.0,68.0 1003.5,72.1 1005.0,73.3 1006.5,73.6 1008.0,73.1 1009.5,73.8 1011.0,74.2 1012.5,74.7 1014.0,72.3 1015.5,73.0 1017.0,75.6 1018.5,74.1 1020.0,73.9 1021.5,70.6 1023.0,69.0 1024.5,68.4 1026.0,70.1 1027.5,78.7 1029.0,81.5 1030.5,80.6 1032.0,80.4 1033.5,78.5 1035.0,75.4 1036.5,76.0 1038.0,78.6 1039.5,77.8 1041.0,78.9 1042.5,74.8 1044.0,87.1 1045.5,140.8 1047.0,158.0 1048.5,125.1 1050.0,91.4 1051.5,76.3 1053.0,69.0 1054.5,67.1 1056.0,63.8 1057.5,63.0 1059.0,61.1 1060.5,61.3 1062.0,60.0 1063.5,58.5 1065.0,59.1 1066.5,58.2 1068.0,57.4 1069.5,57.6 1071.0,56.3 1072.5,56.2 1074.0,58.0 1075.5,59.1 1077.0,61.9 1078.5,63.0 1080.0,64.3 1081.5,65.5 1083.0,65.5 1084.5,66.4 1086.0,64.6 1087.5,64.7 1089.0,63.7 1090.5,61.5 1092.0,62.3 1093.5,61.8 1095.0,62.1 1096.5,61.9 1098.0,62.2 1099.5,62.5 1101.0,59.3 1102.5,57.5 1104.0,57.2 1105.5,61.7 1107.0,67.4 1108.5,68.8 1110.0,69.7 1111.5,67.7 1113.0,65.1 1114.5,64.4 1116.0,64.9 1117.5,65.5 1119.0,64.8 1120.5,63.4 1122.0,63.4 1123.5,95.8\"/><polyline class=\"trace\" points=\"1125.0,63.3 1126.5,65.0 1128.0,67.5 1129.5,64.8 1131.0,64.7 1132.5,64.3 1134.0,63.9 1135.5,64.3 1137.0,63.9 1138.5,62.5 1140.0,64.8 1141.5,66.8 1143.0,67.0 1144.5,67.1 1146.0,65.9 1147.5,66.7 1149.0,66.7 1150.5,66.7 1152.0,66.7 1153.5,66.7 1155.0,65.8 1156.5,64.2 1158.0,64.4 1159.5,61.6 1161.0,59.4 1162.5,58.6 1164.0,57.6 1165.5,61.3 1167.0,63.0 1168.5,62.2 1170.0,62.8 1171.5,61.0 1173.0,62.4 1174.5,59.8 1176.0,62.5 1177.5,61.8 1179.0,61.6 1180.5,50.8 1182.0,-8.6 1183.5,4.5 1185.0,68.3 1186.5,70.8 1188.0,65.3 1189.5,63.4 1191.0,63.8 1192.5,63.7 1194.0,61.1 1195.5,62.8 1197.0,60.7 1198.5,61.6 1200.0,61.6 1201.5,59.8 1203.0,60.3 1204.5,59.8 1206.0,58.6 1207.5,57.0 1209.0,54.7 1210.5,53.3 1212.0,53.2 1213.5,54.8 1215.0,57.1 1216.5,58.5 1218.0,60.3 1219.5,62.2 1221.0,62.9 1222.5,64.2 1224.0,64.9 1225.5,64.4 1227.0,64.2 1228.5,63.6 1230.0,62.8 1231.5,63.4 1233.0,64.0 1234.5,62.8 1236.0,62.7 1237.5,62.8 1239.0,59.8 1240.5,58.6 1242.0,57.4 1243.5,58.1 1245.0,62.5 1246.5,62.2 1248.0,60.3 1249.5,59.7 1251.0,59.2 1252.5,64.1 1254.0,61.2 1255.5,62.2 1257.0,60.4 1258.5,59.7 1260.0,51.1 1261.5,-24.2 1263.0,-22.5 1264.5,56.9 1266.0,66.9 1267.5,63.7 1269.0,63.6 1270.5,61.1 1272.0,63.6 1273.5,63.1 1275.0,63.9 1276.5,62.7 1278.0,63.2 1279.5,61.9 1281.0,60.0 1282.5,60.9 1284.0,61.6 1285.5,59.5 1287.0,58.6 1288.5,57.6 1290.0,55.3 1291.5,55.4 1293.0,55.6 1294.5,56.6 1296.0,59.4 1297.5,61.0 1299.0,62.7 1300.5,63.5 1302.0,63.3 1303.5,63.9 1305.0,63.4 1306.5,63.0 1308.0,62.4 1309.5,62.5 1311.0,62.4 1312.5,62.1 1314.0,63.4 1315.5,63.6 1317.0,62.6 1318.5,59.1 1320.0,56.9 1321.5,56.7 1323.0,57.5 1324.5,61.2 1326.0,62.7 1327.5,61.3 1329.0,61.8 1330.5,59.9 1332.0,62.8 1333.5,61.0 1335.0,58.4 1336.5,56.6 1338.0,56.9 1339.5,54.0 1341.0,-16.4 1342.5,-26.5 1344.0,55.0 1345.5,70.1 1347.0,62.3 1348.5,63.6 1350.0,61.0 1351.5,62.4 1353.0,60.6 1354.5,61.5 1356.0,60.5 1357.5,60.4 1359.0,61.8 1360.5,62.5 1362.0,61.8 1363.5,61.6 1365.0,60.8 1366.5,59.9 1368.0,58.8 1369.5,56.2 1371.0,56.1 1372.5,56.1 1374.0,57.4 1375.5,59.2 1377.0,61.0 1378.5,64.5 1380.0,65.4 1381.5,64.6 1383.0,64.7 1384.5,64.1 1386.0,64.1 1387.5,63.7 1389.0,64.0 1390.5,65.8 1392.0,65.2 1393.5,65.8 1395.0,64.9 1396.5,63.8 1398.0,64.1 1399.5,61.8 1401.0,60.0 1402.5,60.7 1404.0,64.9 1405.5,65.0 1407.0,65.0 1408.5,63.4 1410.0,65.2 1411.5,66.2 1413.0,66.6 1414.5,67.3 1416.0,63.4 1417.5,65.5 1419.0,13.9 1420.5,-10.5 1422.0,50.1 1423.5,71.7 1425.0,68.8 1426.5,69.3 1428.0,66.8 1429.5,67.5 1431.0,65.7 1432.5,65.5 1434.0,64.1 1435.5,65.9 1437.0,65.2 1438.5,64.9 1440.0,65.1 1441.5,62.9 1443.0,60.1 1444.5,57.8 1446.0,56.7 1447.5,55.6 1449.0,55.1 1450.5,54.6 1452.0,56.2 1453.5,57.3 1455.0,58.0 1456.5,60.0 1458.0,62.6 1459.5,63.5 1461.0,63.0 1462.5,62.4 1464.0,61.3 1465.5,62.4 1467.0,62.4 1468.5,61.9 1470.0,62.0 1471.5,61.1 1473.0,61.6 1474.5,60.6 1476.0,57.9 1477.5,58.0 1479.0,57.1 1480.5,56.8 1482.0,59.4 1483.5,61.6 1485.0,62.2 1486.5,60.4 1488.0,58.8 1489.5,62.3 1491.0,61.1 1492.5,61.9 1494.0,61.8 1495.5,60.4 1497.0,54.6 1498.5,-10.5\"/><polyline class=\"trace\" points=\"0.0,173.1 1.5,171.0 3.0,173.4 4.5,167.2 6.0,169.3 7.5,170.8 9.0,169.8 10.5,168.0 12.0,165.0 13.5,162.6 15.0,166.0 16.5,166.3 18.0,163.9 19.5,166.3 21.0,166.6 22.5,171.2 24.0,169.4 25.5,168.4 27.0,170.1 28.5,167.2 30.0,169.1 31.5,168.3 33.0,169.8 34.5,167.1 36.0,163.6 37.5,165.8 39.0,162.4 40.5,163.9 42.0,167.4 43.5,165.6 45.0,166.0 46.5,167.1 48.0,170.4 49.5,169.5 51.0,169.2 52.5,172.3 54.0,174.8 55.5,176.6 57.0,151.5 58.5,123.7 60.0,127.5 61.5,145.5 63.0,160.5 64.5,171.6 66.0,175.8 67.5,175.8 69.0,178.5 70.5,178.9 72.0,179.8 73.5,177.1 75.0,174.1 76.5,176.4 78.0,176.6 79.5,173.5 81.0,176.1 82.5,175.0 84.0,171.0 85.5,173.9 87.0,169.0 88.5,165.9 90.0,169.0 91.5,169.3 93.0,167.1 94.5,167.3 96.0,169.9 97.5,172.2 99.0,172.6 100.5,170.8 102.0,171.0 103.5,169.2 105.0,170.9 106.5,171.9 108.0,171.7 109.5,171.9 111.0,170.8 112.5,172.6 114.0,167.3 115.5,165.3 117.0,166.4 118.5,164.5 120.0,166.9 121.5,167.7 123.0,166.5 124.5,166.3 126.0,168.7 127.5,173.4 129.0,172.3 130.5,171.4 132.0,170.9 133.5,174.2 135.0,177.5 136.5,141.9 138.0,114.3 139.5,127.6 141.0,145.1 142.5,160.6 144.0,169.6 145.5,174.4 147.0,175.1 148.5,177.7 150.0,177.0 151.5,175.0 153.0,175.8 154.5,172.2 156.0,175.0 157.5,175.8 159.0,174.9 160.5,178.3 162.0,174.8 163.5,170.2 165.0,169.9 166.5,169.8 168.0,171.6 169.5,172.0 171.0,167.5 172.5,168.4 174.0,171.7 175.5,171.7 177.0,168.6 178.5,169.2 180.0,175.5 181.5,174.0 183.0,172.0 184.5,173.1 186.0,171.2 187.5,171.1 189.0,170.0 190.5,167.6 192.0,170.9 193.5,170.1 195.0,160.9 196.5,162.0 198.0,167.5 199.5,168.1 201.0,168.1 202.5,168.1 204.0,169.0 205.5,168.4 207.0,170.2 208.5,170.1 210.0,170.2 211.5,169.1 213.0,167.7 214.5,171.4 216.0,147.1 217.5,117.9 219.0,126.8 220.5,144.7 222.0,157.4 223.5,167.5 225.0,172.9 226.5,175.3 228.0,174.6 229.5,174.4 231.0,175.4 232.5,174.4 234.0,170.7 235.5,170.9 237.0,173.3 238.5,169.9 240.0,169.0 241.5,169.2 243.0,168.6 244.5,169.5 246.0,165.9 247.5,166.3 249.0,167.2 250.5,164.1 252.0,164.4 253.5,166.8 255.0,169.9 256.5,168.0 258.0,167.4 259.5,172.0 261.0,169.9 262.5,168.2 264.0,171.1 265.5,167.8 267.0,166.2 268.5,170.0 270.0,169.0 271.5,168.9 273.0,164.6 274.5,162.1 276.0,163.5 277.5,162.6 279.0,168.9 280.5,167.9 282.0,165.7 283.5,168.4 285.0,169.0 286.5,170.1 288.0,174.8 289.5,172.9 291.0,167.3 292.5,177.4 294.0,165.9 295.5,129.8 297.0,115.2 298.5,133.7 300.0,155.6 301.5,164.5 303.0,174.4 304.5,176.5 306.0,173.8 307.5,176.7 309.0,176.9 310.5,175.6 312.0,175.6 313.5,172.7 315.0,175.0 316.5,177.6 318.0,173.5 319.5,171.7 321.0,174.6 322.5,174.4 324.0,168.4 325.5,169.6 327.0,169.9 328.5,166.8 330.0,169.4 331.5,169.7 333.0,169.9 334.5,171.5 336.0,173.8 337.5,173.3 339.0,172.5 340.5,173.7 342.0,173.7 343.5,174.3 345.0,175.9 346.5,176.5 348.0,173.1 349.5,173.2 351.0,171.1 352.5,170.3 354.0,171.3 355.5,168.1 357.0,172.9 358.5,172.8 360.0,170.1 361.5,172.3 363.0,174.7 364.5,179.1 366.0,178.5 367.5,178.6 369.0,175.8 370.5,178.2 372.0,183.5 373.5,155.1\"/><polyline class=\"trace\" points=\"375.0,164.8 376.5,167.2 378.0,169.1 379.5,166.3 381.0,169.2 382.5,167.5 384.0,170.8 385.5,173.2 387.0,169.8 388.5,173.9 390.0,175.3 391.5,174.2 393.0,173.1 394.5,173.7 396.0,174.9 397.5,172.9 399.0,170.2 400.5,173.8 402.0,174.9 403.5,169.5 405.0,170.1 406.5,170.5 408.0,172.3 409.5,171.6 411.0,171.6 412.5,173.7 414.0,171.2 415.5,170.7 417.0,166.5 418.5,168.3 420.0,172.2 421.5,169.6 423.0,167.2 424.5,167.3 426.0,170.1 427.5,167.8 429.0,166.0 430.5,166.6 432.0,173.1 433.5,175.2 435.0,174.5 436.5,175.7 438.0,168.0 439.5,169.6 441.0,167.8 442.5,164.7 444.0,167.3 445.5,164.0 447.0,165.9 448.5,165.1 450.0,163.9 451.5,166.4 453.0,166.5 454.5,165.5 456.0,167.2 457.5,167.4 459.0,165.9 460.5,167.2 462.0,164.7 463.5,163.7 465.0,166.9 466.5,168.3 468.0,168.4 469.5,169.9 471.0,169.3 472.5,168.5 474.0,169.0 475.5,170.9 477.0,169.1 478.5,165.6 480.0,168.2 481.5,168.0 483.0,168.6 484.5,171.0 486.0,169.8 487.5,168.8 489.0,171.6 490.5,173.2 492.0,169.0 493.5,166.9 495.0,165.4 496.5,163.0 498.0,163.2 499.5,163.3 501.0,165.9 502.5,167.6 504.0,164.8 505.5,164.1 507.0,168.1 508.5,169.2 510.0,169.2 511.5,176.2 513.0,176.1 514.5,172.0 516.0,172.6 517.5,169.3 519.0,166.6 520.5,165.3 522.0,165.6 523.5,167.5 525.0,167.1 526.5,165.5 528.0,166.2 529.5,165.9 531.0,165.1 532.5,169.6 534.0,169.9 535.5,168.6 537.0,169.5 538.5,167.5 540.0,171.0 541.5,169.5 543.0,169.8 544.5,172.0 546.0,168.4 547.5,170.3 549.0,173.6 550.5,175.8 552.0,170.8 553.5,170.5 555.0,172.8 556.5,172.9 558.0,171.7 559.5,170.7 561.0,173.1 562.5,167.6 564.0,167.7 565.5,169.3 567.0,169.8 568.5,173.4 570.0,172.0 571.5,169.0 573.0,166.8 574.5,167.8 576.0,166.5 577.5,166.2 579.0,168.5 580.5,168.9 582.0,168.1 583.5,170.4 585.0,172.3 586.5,172.5 588.0,176.1 589.5,174.3 591.0,176.9 592.5,174.5 594.0,171.1 595.5,174.6 597.0,170.5 598.5,171.8 600.0,169.3 601.5,166.8 603.0,169.9 604.5,170.2 606.0,169.0 607.5,165.7 609.0,166.2 610.5,169.2 612.0,169.2 613.5,167.7 615.0,168.6 616.5,169.0 618.0,168.9 619.5,170.2 621.0,171.4 622.5,174.1 624.0,174.8 625.5,174.1 627.0,175.0 628.5,176.5 630.0,178.4 631.5,177.4 633.0,175.6 634.5,177.1 636.0,177.9 637.5,175.6 639.0,174.4 640.5,174.6 642.0,174.1 643.5,173.9 645.0,174.0 646.5,176.1 648.0,175.6 649.5,173.5 651.0,171.1 652.5,169.2 654.0,169.2 655.5,171.0 657.0,173.1 658.5,173.7 660.0,173.4 661.5,174.0 663.0,175.0 664.5,168.8 666.0,168.1 667.5,171.2 669.0,172.9 670.5,177.5 672.0,180.4 673.5,181.0 675.0,176.4 676.5,172.5 678.0,170.1 679.5,170.8 681.0,169.6 682.5,167.9 684.0,169.8 685.5,169.9 687.0,165.3 688.5,165.7 690.0,172.0 691.5,169.7 693.0,169.8 694.5,169.8 696.0,169.1 697.5,172.8 699.0,172.4 700.5,174.3 702.0,174.7 703.5,172.8 705.0,174.4 706.5,173.2 708.0,175.5 709.5,175.7 711.0,174.4 712.5,175.1 714.0,171.6 715.5,172.8 717.0,173.1 718.5,172.2 720.0,172.3 721.5,172.6 723.0,170.7 724.5,169.0 726.0,171.4 727.5,174.4 729.0,175.5 730.5,171.7 732.0,170.0 733.5,168.8 735.0,167.6 736.5,167.4 738.0,169.3 739.5,171.7 741.0,172.9 742.5,170.5 744.0,167.6 745.5,170.2 747.0,169.3 748.5,175.2\"/><polyline class=\"trace\" points=\"750.0,159.7 751.5,159.7 753.0,159.7 754.5,159.6 756.0,160.2 757.5,161.9 759.0,165.5 760.5,168.5 762.0,172.8 763.5,177.7 765.0,180.6 766.5,182.5 768.0,183.8 769.5,184.6 771.0,182.8 772.5,181.5 774.0,181.0 775.5,180.0 777.0,178.5 778.5,176.3 780.0,175.6 781.5,176.3 783.0,175.2 784.5,170.5 786.0,168.5 787.5,168.0 789.0,171.4 790.5,177.4 792.0,176.2 793.5,173.4 795.0,173.1 796.5,172.9 798.0,170.5 799.5,169.8 801.0,167.7 802.5,169.3 804.0,166.6 805.5,172.6 807.0,217.2 808.5,255.4 810.0,247.5 811.5,203.5 813.0,170.2 814.5,160.7 816.0,153.7 817.5,153.0 819.0,152.1 820.5,151.2 822.0,150.1 823.5,149.4 825.0,150.1 826.5,148.9 828.0,148.6 829.5,149.2 831.0,149.5 832.5,148.1 834.0,148.9 835.5,151.6 837.0,154.6 838.5,158.2 840.0,162.4 841.5,168.3 843.0,171.9 844.5,174.4 846.0,176.7 847.5,176.9 849.0,176.4 850.5,175.8 852.0,172.5 853.5,169.9 855.0,169.5 856.5,168.6 858.0,169.2 859.5,169.4 861.0,170.1 862.5,169.5 864.0,165.4 865.5,162.6 867.0,162.8 868.5,167.2 870.0,172.7 871.5,174.3 873.0,172.8 874.5,170.4 876.0,169.4 877.5,169.2 879.0,170.3 880.5,169.2 882.0,171.3 883.5,167.4 885.0,171.3 886.5,224.3 888.0,264.6 889.5,243.5 891.0,202.6 892.5,174.4 894.0,162.4 895.5,155.9 897.0,155.3 898.5,153.9 900.0,152.5 901.5,152.5 903.0,150.6 904.5,151.2 906.0,150.7 907.5,150.9 909.0,151.1 910.5,149.1 912.0,149.7 913.5,150.9 915.0,153.9 916.5,158.1 918.0,158.9 919.5,163.6 921.0,170.0 922.5,173.1 924.0,176.9 925.5,178.2 927.0,177.8 928.5,177.3 930.0,176.6 931.5,176.9 933.0,176.2 934.5,175.2 936.0,173.4 937.5,171.9 939.0,172.3 940.5,171.9 942.0,170.5 943.5,168.0 945.0,165.4 946.5,165.1 948.0,169.1 949.5,173.7 951.0,175.3 952.5,175.6 954.0,175.2 955.5,173.8 957.0,172.6 958.5,173.1 960.0,170.0 961.5,173.1 963.0,171.4 964.5,168.7 966.0,214.2 967.5,262.6 969.0,251.9 970.5,209.0 972.0,177.7 973.5,164.9 975.0,157.5 976.5,155.3 978.0,156.3 979.5,154.7 981.0,152.6 982.5,152.7 984.0,152.6 985.5,152.3 987.0,152.9 988.5,153.2 990.0,153.6 991.5,154.2 993.0,154.2 994.5,155.9 996.0,158.1 997.5,163.2 999.0,167.9 1000.5,171.7 1002.0,178.5 1003.5,180.8 1005.0,182.7 1006.5,183.8 1008.0,182.9 1009.5,183.0 1011.0,181.9 1012.5,181.2 1014.0,180.8 1015.5,181.2 1017.0,178.7 1018.5,178.9 1020.0,181.9 1021.5,178.0 1023.0,176.7 1024.5,175.7 1026.0,175.3 1027.5,182.2 1029.0,184.9 1030.5,184.4 1032.0,183.0 1033.5,182.1 1035.0,181.6 1036.5,182.5 1038.0,182.8 1039.5,181.7 1041.0,182.4 1042.5,180.2 1044.0,203.2 1045.5,247.3 1047.0,262.9 1048.5,232.0 1050.0,191.4 1051.5,175.7 1053.0,168.0 1054.5,165.5 1056.0,164.7 1057.5,161.5 1059.0,162.0 1060.5,161.2 1062.0,159.3 1063.5,157.6 1065.0,158.1 1066.5,157.6 1068.0,157.0 1069.5,157.6 1071.0,156.3 1072.5,157.1 1074.0,160.4 1075.5,162.9 1077.0,166.5 1078.5,171.0 1080.0,174.5 1081.5,176.8 1083.0,177.6 1084.5,178.2 1086.0,177.4 1087.5,174.7 1089.0,173.5 1090.5,173.2 1092.0,170.5 1093.5,167.8 1095.0,168.3 1096.5,167.1 1098.0,166.6 1099.5,167.2 1101.0,164.2 1102.5,163.3 1104.0,162.4 1105.5,164.8 1107.0,169.8 1108.5,170.7 1110.0,171.1 1111.5,169.5 1113.0,168.4 1114.5,166.9 1116.0,168.3 1117.5,168.3 1119.0,168.0 1120.5,165.7 1122.0,169.6 1123.5,215.5\"/><polyline class=\"trace\" points=\"1125.0,164.7 1126.5,164.1 1128.0,164.5 1129.5,165.1 1131.0,164.1 1132.5,164.2 1134.0,164.1 1135.5,164.2 1137.0,164.1 1138.5,163.2 1140.0,164.0 1141.5,164.5 1143.0,166.8 1144.5,166.3 1146.0,165.2 1147.5,165.0 1149.0,162.5 1150.5,163.9 1152.0,164.6 1153.5,163.2 1155.0,162.6 1156.5,162.5 1158.0,162.9 1159.5,161.6 1161.0,161.0 1162.5,160.7 1164.0,159.4 1165.5,160.0 1167.0,160.0 1168.5,159.7 1170.0,160.6 1171.5,162.2 1173.0,164.6 1174.5,163.5 1176.0,165.4 1177.5,164.2 1179.0,167.5 1180.5,162.9 1182.0,123.4 1183.5,114.9 1185.0,140.2 1186.5,153.3 1188.0,162.6 1189.5,167.1 1191.0,168.9 1192.5,169.3 1194.0,169.2 1195.5,169.3 1197.0,169.0 1198.5,169.3 1200.0,169.5 1201.5,170.0 1203.0,170.1 1204.5,170.8 1206.0,169.9 1207.5,168.4 1209.0,168.1 1210.5,166.5 1212.0,167.2 1213.5,167.3 1215.0,166.1 1216.5,167.7 1218.0,168.9 1219.5,169.3 1221.0,171.1 1222.5,173.5 1224.0,173.6 1225.5,172.9 1227.0,172.9 1228.5,173.1 1230.0,173.8 1231.5,173.1 1233.0,173.1 1234.5,172.4 1236.0,172.3 1237.5,172.3 1239.0,169.4 1240.5,169.5 1242.0,169.3 1243.5,168.3 1245.0,168.9 1246.5,170.1 1248.0,169.5 1249.5,169.2 1251.0,172.2 1252.5,175.3 1254.0,172.2 1255.5,173.9 1257.0,173.1 1258.5,174.1 1260.0,172.5 1261.5,124.0 1263.0,103.5 1264.5,132.0 1266.0,152.2 1267.5,167.1 1269.0,170.5 1270.5,174.3 1272.0,177.6 1273.5,177.6 1275.0,178.0 1276.5,177.3 1278.0,177.4 1279.5,177.0 1281.0,177.1 1282.5,178.0 1284.0,178.1 1285.5,175.9 1287.0,176.2 1288.5,176.1 1290.0,175.6 1291.5,174.8 1293.0,174.6 1294.5,176.5 1296.0,176.3 1297.5,176.7 1299.0,177.1 1300.5,177.4 1302.0,177.1 1303.5,177.4 1305.0,177.1 1306.5,176.7 1308.0,177.6 1309.5,175.8 1311.0,174.6 1312.5,175.9 1314.0,176.9 1315.5,176.2 1317.0,175.5 1318.5,172.9 1320.0,171.5 1321.5,171.6 1323.0,169.8 1324.5,171.6 1326.0,173.7 1327.5,171.5 1329.0,169.5 1330.5,171.3 1332.0,175.8 1333.5,175.0 1335.0,175.1 1336.5,173.1 1338.0,175.9 1339.5,178.4 1341.0,132.3 1342.5,103.6 1344.0,130.1 1345.5,150.2 1347.0,165.0 1348.5,173.7 1350.0,175.7 1351.5,178.3 1353.0,178.7 1354.5,178.8 1356.0,177.9 1357.5,178.8 1359.0,180.9 1360.5,179.7 1362.0,179.0 1363.5,180.7 1365.0,180.7 1366.5,180.1 1368.0,177.3 1369.5,177.6 1371.0,177.2 1372.5,176.2 1374.0,176.8 1375.5,174.4 1377.0,176.4 1378.5,176.1 1380.0,175.7 1381.5,176.1 1383.0,174.7 1384.5,174.7 1386.0,171.1 1387.5,169.8 1389.0,171.9 1390.5,171.7 1392.0,171.7 1393.5,174.7 1395.0,174.7 1396.5,173.3 1398.0,170.1 1399.5,168.3 1401.0,168.0 1402.5,166.0 1404.0,167.6 1405.5,166.7 1407.0,167.4 1408.5,167.2 1410.0,167.4 1411.5,168.7 1413.0,168.7 1414.5,168.6 1416.0,168.9 1417.5,173.0 1419.0,143.5 1420.5,110.4 1422.0,122.2 1423.5,141.4 1425.0,157.9 1426.5,167.8 1428.0,168.2 1429.5,170.6 1431.0,172.2 1432.5,170.8 1434.0,170.5 1435.5,171.2 1437.0,170.8 1438.5,169.5 1440.0,167.9 1441.5,168.1 1443.0,168.0 1444.5,168.2 1446.0,166.9 1447.5,165.7 1449.0,165.9 1450.5,164.9 1452.0,166.1 1453.5,166.9 1455.0,167.4 1456.5,168.0 1458.0,168.0 1459.5,168.3 1461.0,168.3 1462.5,169.0 1464.0,169.5 1465.5,170.2 1467.0,170.3 1468.5,168.9 1470.0,170.2 1471.5,170.0 1473.0,169.7 1474.5,171.7 1476.0,170.4 1477.5,169.7 1479.0,169.6 1480.5,169.2 1482.0,170.6 1483.5,172.5 1485.0,172.9 1486.5,170.5 1488.0,170.2 1489.5,174.1 1491.0,174.0 1492.5,174.6 1494.0,172.8 1495.5,175.8 1497.0,174.9 1498.5,131.6\"/><polyline class=\"trace\" points=\"0.0,284.5 1.5,281.1 3.0,280.3 4.5,280.0 6.0,278.2 7.5,280.7 9.0,276.8 10.5,273.6 12.0,275.4 13.5,270.1 15.0,270.4 16.5,271.7 18.0,271.6 19.5,272.2 21.0,271.2 22.5,275.4 24.0,277.3 25.5,273.1 27.0,272.9 28.5,276.9 30.0,277.2 31.5,276.4 33.0,275.4 34.5,274.6 36.0,273.0 37.5,271.9 39.0,272.7 40.5,274.0 42.0,280.0 43.5,277.3 45.0,273.5 46.5,276.7 48.0,280.8 49.5,280.2 51.0,277.3 52.5,281.1 54.0,284.1 55.5,284.4 57.0,265.3 58.5,249.4 60.0,252.0 61.5,259.8 63.0,275.0 64.5,278.9 66.0,282.7 67.5,285.9 69.0,284.7 70.5,288.1 72.0,286.8 73.5,286.2 75.0,285.9 76.5,284.5 78.0,284.5 79.5,284.0 81.0,283.6 82.5,282.8 84.0,282.4 85.5,282.5 87.0,282.6 88.5,282.0 90.0,280.3 91.5,279.1 93.0,277.9 94.5,276.6 96.0,278.4 97.5,280.3 99.0,280.0 100.5,277.2 102.0,279.1 103.5,281.8 105.0,280.0 106.5,280.7 108.0,280.0 109.5,277.6 111.0,278.4 112.5,280.3 114.0,274.9 115.5,272.2 117.0,277.0 118.5,278.1 120.0,280.8 121.5,283.5 123.0,282.8 124.5,282.6 126.0,281.2 127.5,281.8 129.0,284.1 130.5,284.4 132.0,280.1 133.5,280.6 135.0,282.3 136.5,257.4 138.0,243.9 139.5,254.5 141.0,262.8 142.5,273.7 144.0,280.9 145.5,284.6 147.0,284.7 148.5,284.1 150.0,284.2 151.5,284.7 153.0,284.5 154.5,282.9 156.0,285.1 157.5,281.0 159.0,280.2 160.5,283.3 162.0,280.6 163.5,280.3 165.0,276.7 166.5,278.2 168.0,278.7 169.5,276.7 171.0,278.1 172.5,276.6 174.0,274.9 175.5,272.7 177.0,276.3 178.5,276.9 180.0,277.6 181.5,276.8 183.0,277.0 184.5,278.6 186.0,275.3 187.5,280.6 189.0,280.1 190.5,277.2 192.0,278.4 193.5,274.5 195.0,271.2 196.5,274.7 198.0,279.7 199.5,279.1 201.0,280.3 202.5,280.5 204.0,278.7 205.5,278.1 207.0,279.7 208.5,277.5 210.0,275.5 211.5,274.8 213.0,270.6 214.5,274.2 216.0,259.4 217.5,247.2 219.0,255.0 220.5,260.5 222.0,270.9 223.5,274.6 225.0,279.8 226.5,283.6 228.0,280.2 229.5,279.8 231.0,281.4 232.5,284.2 234.0,281.9 235.5,279.0 237.0,280.1 238.5,280.0 240.0,278.7 241.5,278.3 243.0,278.1 244.5,277.3 246.0,274.3 247.5,271.8 249.0,271.5 250.5,270.7 252.0,269.9 253.5,269.7 255.0,269.4 256.5,269.4 258.0,270.8 259.5,271.6 261.0,269.8 262.5,271.3 264.0,273.9 265.5,272.1 267.0,271.8 268.5,273.9 270.0,273.3 271.5,271.0 273.0,269.4 274.5,270.3 276.0,273.3 277.5,274.8 279.0,278.0 280.5,275.7 282.0,272.4 283.5,273.2 285.0,273.9 286.5,273.9 288.0,275.1 289.5,280.4 291.0,278.2 292.5,280.2 294.0,272.8 295.5,250.1 297.0,239.8 298.5,248.6 300.0,264.1 301.5,272.5 303.0,279.9 304.5,280.2 306.0,280.0 307.5,283.2 309.0,281.4 310.5,280.6 312.0,285.3 313.5,283.4 315.0,278.2 316.5,281.8 318.0,279.7 319.5,278.8 321.0,280.9 322.5,277.1 324.0,274.5 325.5,273.3 327.0,273.0 328.5,273.3 330.0,273.0 331.5,274.4 333.0,272.2 334.5,272.8 336.0,275.2 337.5,274.2 339.0,277.3 340.5,276.7 342.0,276.5 343.5,277.8 345.0,278.4 346.5,278.3 348.0,278.6 349.5,280.3 351.0,276.9 352.5,273.4 354.0,272.8 355.5,275.1 357.0,279.2 358.5,280.3 360.0,280.2 361.5,281.4 363.0,280.8 364.5,280.5 366.0,279.0 367.5,281.5 369.0,283.0 370.5,281.7 372.0,285.1 373.5,265.2\"/><polyline class=\"trace\" points=\"375.0,282.9 376.5,280.1 378.0,280.9 379.5,277.7 381.0,277.8 382.5,279.9 384.0,277.4 385.5,274.9 387.0,274.3 388.5,270.4 390.0,272.3 391.5,273.1 393.0,271.8 394.5,273.4 396.0,273.0 397.5,277.4 399.0,277.5 400.5,274.9 402.0,275.6 403.5,276.1 405.0,277.3 406.5,276.5 408.0,276.7 409.5,275.0 411.0,272.4 412.5,273.0 414.0,271.6 415.5,273.1 417.0,277.8 418.5,275.5 420.0,273.8 421.5,276.0 423.0,279.7 424.5,278.9 426.0,277.3 427.5,280.8 429.0,283.5 430.5,284.5 432.0,262.5 433.5,240.7 435.0,243.9 436.5,256.7 438.0,271.8 439.5,279.3 441.0,283.3 442.5,284.9 444.0,285.6 445.5,287.6 447.0,287.4 448.5,285.7 450.0,284.1 451.5,284.5 453.0,284.6 454.5,282.9 456.0,283.9 457.5,283.0 459.0,280.8 460.5,282.3 462.0,279.9 463.5,278.0 465.0,278.7 466.5,278.3 468.0,276.6 469.5,276.0 471.0,278.2 472.5,280.3 474.0,280.4 475.5,278.1 477.0,279.1 478.5,279.6 480.0,279.6 481.5,280.3 483.0,279.9 484.5,278.8 486.0,278.7 487.5,280.5 489.0,275.2 490.5,272.9 492.0,275.8 493.5,275.4 495.0,277.9 496.5,279.7 498.0,278.7 499.5,278.5 501.0,279.0 502.5,281.7 504.0,282.3 505.5,282.0 507.0,279.6 508.5,281.5 510.0,283.9 511.5,253.8 513.0,233.2 514.5,245.2 516.0,258.0 517.5,271.2 519.0,279.4 520.5,283.6 522.0,283.9 523.5,285.0 525.0,284.7 526.5,283.9 528.0,284.2 529.5,281.6 531.0,284.2 532.5,282.5 534.0,281.7 535.5,284.9 537.0,281.8 538.5,279.3 540.0,277.5 541.5,278.1 543.0,279.2 544.5,278.4 546.0,276.9 547.5,276.6 549.0,277.4 550.5,276.3 552.0,276.5 553.5,277.1 555.0,280.7 556.5,279.4 558.0,278.6 559.5,279.9 561.0,277.3 562.5,280.0 564.0,279.1 565.5,276.5 567.0,278.7 568.5,276.4 570.0,270.1 571.5,272.5 573.0,277.7 574.5,277.7 576.0,278.3 577.5,278.4 579.0,277.9 580.5,277.3 582.0,279.0 583.5,277.9 585.0,276.9 586.5,276.0 588.0,273.2 589.5,276.9 591.0,257.4 592.5,236.7 594.0,245.0 595.5,256.8 597.0,268.2 598.5,275.2 600.0,280.4 601.5,283.5 603.0,281.5 604.5,281.2 606.0,282.4 607.5,283.4 609.0,280.4 610.5,279.1 612.0,280.8 613.5,279.0 615.0,278.0 616.5,277.8 618.0,277.5 619.5,277.5 621.0,274.2 622.5,273.1 624.0,273.4 625.5,271.5 627.0,271.2 628.5,272.4 630.0,273.7 631.5,272.8 633.0,273.3 634.5,276.0 636.0,274.0 637.5,273.9 639.0,276.6 640.5,274.0 642.0,273.1 643.5,276.1 645.0,275.2 646.5,274.0 648.0,271.1 649.5,270.3 651.0,272.5 652.5,272.8 654.0,277.5 655.5,275.9 657.0,273.1 658.5,274.9 660.0,275.5 661.5,276.1 663.0,279.0 664.5,280.7 666.0,276.9 667.5,282.9 669.0,273.4 670.5,244.0 672.0,231.6 673.5,245.2 675.0,264.0 676.5,272.7 678.0,281.2 679.5,282.4 681.0,281.0 682.5,284.0 684.0,283.2 685.5,282.2 687.0,284.5 688.5,282.1 690.0,280.7 691.5,283.8 693.0,280.7 694.5,279.4 696.0,281.8 697.5,279.9 699.0,275.5 700.5,275.5 702.0,275.5 703.5,274.2 705.0,275.3 706.5,276.1 708.0,275.1 709.5,276.3 711.0,278.6 712.5,277.8 714.0,279.0 715.5,279.3 717.0,279.2 718.5,280.1 720.0,281.2 721.5,281.5 723.0,279.9 724.5,280.8 726.0,278.1 727.5,276.0 729.0,276.2 730.5,275.7 732.0,280.2 733.5,280.6 735.0,279.2 736.5,280.9 738.0,281.8 739.5,283.9 741.0,282.9 742.5,284.1 744.0,283.5 745.5,284.0 747.0,288.4 748.5,264.2\"/><polyline class=\"trace\" points=\"750.0,282.1 751.5,281.7 753.0,284.5 754.5,280.0 756.0,275.7 757.5,276.3 759.0,276.6 760.5,277.3 762.0,277.7 763.5,278.7 765.0,282.6 766.5,284.2 768.0,285.3 769.5,285.8 771.0,284.2 772.5,284.7 774.0,284.0 775.5,284.9 777.0,283.0 778.5,280.9 780.0,283.0 781.5,282.2 783.0,281.5 784.5,277.1 786.0,274.8 787.5,273.9 789.0,274.3 790.5,280.8 792.0,280.8 793.5,279.5 795.0,278.8 796.5,275.5 798.0,276.1 799.5,275.8 801.0,276.4 802.5,276.3 804.0,276.7 805.5,272.4 807.0,244.8 808.5,254.2 810.0,299.9 811.5,298.5 813.0,281.4 814.5,277.9 816.0,274.4 817.5,275.5 819.0,274.4 820.5,273.5 822.0,272.7 823.5,272.1 825.0,272.6 826.5,271.4 828.0,270.5 829.5,269.8 831.0,269.1 832.5,267.4 834.0,265.3 835.5,264.9 837.0,267.2 838.5,268.5 840.0,268.5 841.5,271.5 843.0,274.5 844.5,277.1 846.0,278.2 847.5,277.7 849.0,277.8 850.5,277.6 852.0,277.5 853.5,277.2 855.0,277.2 856.5,277.6 858.0,278.1 859.5,278.5 861.0,279.1 862.5,278.9 864.0,275.3 865.5,273.7 867.0,274.0 868.5,275.8 870.0,279.1 871.5,280.3 873.0,280.5 874.5,278.1 876.0,277.9 877.5,280.6 879.0,278.8 880.5,279.4 882.0,279.4 883.5,278.1 885.0,270.2 886.5,233.5 888.0,245.2 889.5,299.6 891.0,299.5 892.5,285.7 894.0,280.7 895.5,276.3 897.0,278.3 898.5,276.0 900.0,275.2 901.5,275.5 903.0,275.1 904.5,274.8 906.0,273.5 907.5,272.2 909.0,272.4 910.5,269.4 912.0,267.8 913.5,268.4 915.0,267.4 916.5,268.2 918.0,268.6 919.5,270.3 921.0,272.7 922.5,275.8 924.0,278.4 925.5,279.7 927.0,281.2 928.5,280.5 930.0,280.4 931.5,281.2 933.0,281.7 934.5,282.1 936.0,281.7 937.5,281.5 939.0,281.2 940.5,280.8 942.0,279.3 943.5,276.9 945.0,275.5 946.5,275.1 948.0,277.3 949.5,280.8 951.0,283.5 952.5,283.7 954.0,282.8 955.5,282.3 957.0,282.3 958.5,280.4 960.0,278.8 961.5,277.3 963.0,277.2 964.5,273.2 966.0,239.8 967.5,247.6 969.0,302.9 970.5,306.1 972.0,288.7 973.5,285.7 975.0,281.4 976.5,280.3 978.0,282.1 979.5,282.4 981.0,281.5 982.5,281.9 984.0,281.8 985.5,280.8 987.0,277.9 988.5,276.7 990.0,276.0 991.5,275.5 993.0,276.6 994.5,274.6 996.0,274.1 997.5,275.8 999.0,275.8 1000.5,280.0 1002.0,284.6 1003.5,286.5 1005.0,288.7 1006.5,289.3 1008.0,291.0 1009.5,291.7 1011.0,291.1 1012.5,291.6 1014.0,291.5 1015.5,291.6 1017.0,291.4 1018.5,291.1 1020.0,290.7 1021.5,290.4 1023.0,288.4 1024.5,285.2 1026.0,286.6 1027.5,289.6 1029.0,293.7 1030.5,295.5 1032.0,292.5 1033.5,292.1 1035.0,291.9 1036.5,292.9 1038.0,294.7 1039.5,292.2 1041.0,292.2 1042.5,292.1 1044.0,264.7 1045.5,250.7 1047.0,293.6 1048.5,313.3 1050.0,297.6 1051.5,294.3 1053.0,290.5 1054.5,287.2 1056.0,287.4 1057.5,285.5 1059.0,283.8 1060.5,284.4 1062.0,282.9 1063.5,281.1 1065.0,283.2 1066.5,280.2 1068.0,276.3 1069.5,275.4 1071.0,272.5 1072.5,270.7 1074.0,270.6 1075.5,270.1 1077.0,271.2 1078.5,273.5 1080.0,275.7 1081.5,276.7 1083.0,277.1 1084.5,277.3 1086.0,277.6 1087.5,278.1 1089.0,276.5 1090.5,275.8 1092.0,276.9 1093.5,277.3 1095.0,278.0 1096.5,275.9 1098.0,275.4 1099.5,276.1 1101.0,273.6 1102.5,273.0 1104.0,271.8 1105.5,272.9 1107.0,277.3 1108.5,278.1 1110.0,277.9 1111.5,277.8 1113.0,276.7 1114.5,277.5 1116.0,277.7 1117.5,278.0 1119.0,278.8 1120.5,278.6 1122.0,275.4 1123.5,244.2\"/><polyline class=\"trace\" points=\"1125.0,289.4 1126.5,291.6 1128.0,292.5 1129.5,289.8 1131.0,289.5 1132.5,288.1 1134.0,287.2 1135.5,287.0 1137.0,286.6 1138.5,286.6 1140.0,285.0 1141.5,285.3 1143.0,284.4 1144.5,284.2 1146.0,286.3 1147.5,284.8 1149.0,283.8 1150.5,283.5 1152.0,283.5 1153.5,283.8 1155.0,283.6 1156.5,282.7 1158.0,280.5 1159.5,279.3 1161.0,278.6 1162.5,277.0 1164.0,275.1 1165.5,275.9 1167.0,275.9 1168.5,274.4 1170.0,274.7 1171.5,273.3 1173.0,274.0 1174.5,274.5 1176.0,275.5 1177.5,275.8 1179.0,276.8 1180.5,276.0 1182.0,255.4 1183.5,238.8 1185.0,242.4 1186.5,254.9 1188.0,268.7 1189.5,276.3 1191.0,280.6 1192.5,281.9 1194.0,282.9 1195.5,283.5 1197.0,282.7 1198.5,282.5 1200.0,281.8 1201.5,281.6 1203.0,281.4 1204.5,281.5 1206.0,281.4 1207.5,279.8 1209.0,279.0 1210.5,279.7 1212.0,279.8 1213.5,277.6 1215.0,276.0 1216.5,276.2 1218.0,277.0 1219.5,278.0 1221.0,279.3 1222.5,280.9 1224.0,281.1 1225.5,282.2 1227.0,282.3 1228.5,281.5 1230.0,282.4 1231.5,281.8 1233.0,281.6 1234.5,280.7 1236.0,281.1 1237.5,282.4 1239.0,280.8 1240.5,279.6 1242.0,278.9 1243.5,276.7 1245.0,275.6 1246.5,275.7 1248.0,273.9 1249.5,274.5 1251.0,276.7 1252.5,276.6 1254.0,275.4 1255.5,276.3 1257.0,274.9 1258.5,276.7 1260.0,277.5 1261.5,251.7 1263.0,228.7 1264.5,233.0 1266.0,248.8 1267.5,264.6 1269.0,272.4 1270.5,277.0 1272.0,278.7 1273.5,279.3 1275.0,279.6 1276.5,278.0 1278.0,278.0 1279.5,278.7 1281.0,278.5 1282.5,281.1 1284.0,281.3 1285.5,277.5 1287.0,277.3 1288.5,277.2 1290.0,276.9 1291.5,277.0 1293.0,275.5 1294.5,275.4 1296.0,275.8 1297.5,276.0 1299.0,276.4 1300.5,276.6 1302.0,277.2 1303.5,277.7 1305.0,278.1 1306.5,278.2 1308.0,278.7 1309.5,278.5 1311.0,277.9 1312.5,278.1 1314.0,279.4 1315.5,278.8 1317.0,276.9 1318.5,278.1 1320.0,276.8 1321.5,275.4 1323.0,276.0 1324.5,275.4 1326.0,275.7 1327.5,275.2 1329.0,275.1 1330.5,277.6 1332.0,281.5 1333.5,280.5 1335.0,279.9 1336.5,282.0 1338.0,285.5 1339.5,287.4 1341.0,261.9 1342.5,232.8 1344.0,233.5 1345.5,248.2 1347.0,263.4 1348.5,273.7 1350.0,277.5 1351.5,277.8 1353.0,277.8 1354.5,278.1 1356.0,278.1 1357.5,276.3 1359.0,276.0 1360.5,277.0 1362.0,276.3 1363.5,274.9 1365.0,276.4 1366.5,277.6 1368.0,273.6 1369.5,273.6 1371.0,274.9 1372.5,274.3 1374.0,276.4 1375.5,274.3 1377.0,276.8 1378.5,278.7 1380.0,277.1 1381.5,282.9 1383.0,280.8 1384.5,280.8 1386.0,283.0 1387.5,281.5 1389.0,283.7 1390.5,281.4 1392.0,283.5 1393.5,282.6 1395.0,280.8 1396.5,282.3 1398.0,278.9 1399.5,279.4 1401.0,278.6 1402.5,278.8 1404.0,277.4 1405.5,277.6 1407.0,280.9 1408.5,279.9 1410.0,282.8 1411.5,286.1 1413.0,284.5 1414.5,282.1 1416.0,284.7 1417.5,285.7 1419.0,273.2 1420.5,248.4 1422.0,241.1 1423.5,253.6 1425.0,268.3 1426.5,278.2 1428.0,279.7 1429.5,284.2 1431.0,287.1 1432.5,286.0 1434.0,286.6 1435.5,286.6 1437.0,283.5 1438.5,282.9 1440.0,284.7 1441.5,283.0 1443.0,280.3 1444.5,279.7 1446.0,279.8 1447.5,279.3 1449.0,277.9 1450.5,275.4 1452.0,276.9 1453.5,277.3 1455.0,275.2 1456.5,275.8 1458.0,276.8 1459.5,277.3 1461.0,275.7 1462.5,277.2 1464.0,277.1 1465.5,277.4 1467.0,277.4 1468.5,274.3 1470.0,275.6 1471.5,274.9 1473.0,274.8 1474.5,275.7 1476.0,275.6 1477.5,276.7 1479.0,275.8 1480.5,274.3 1482.0,274.8 1483.5,275.5 1485.0,275.7 1486.5,276.7 1488.0,277.4 1489.5,280.4 1491.0,281.3 1492.5,281.7 1494.0,281.8 1495.5,282.9 1497.0,282.4 1498.5,260.7\"/><polyline class=\"trace\" points=\"0.0,384.7 1.5,382.7 3.0,385.0 4.5,378.9 6.0,381.0 7.5,382.5 9.0,381.5 10.5,379.7 12.0,376.6 13.5,374.2 15.0,377.7 16.5,378.0 18.0,375.6 19.5,378.0 21.0,378.3 22.5,382.9 24.0,381.1 25.5,380.1 27.0,381.7 28.5,378.9 30.0,380.8 31.5,380.0 33.0,381.5 34.5,378.7 36.0,375.3 37.5,377.5 39.0,374.1 40.5,375.6 42.0,379.0 43.5,377.3 45.0,377.7 46.5,378.8 48.0,382.1 49.5,381.1 51.0,380.8 52.5,384.0 54.0,386.5 55.5,388.3 57.0,363.1 58.5,335.4 60.0,339.2 61.5,357.1 63.0,372.1 64.5,383.2 66.0,387.4 67.5,387.5 69.0,390.1 70.5,390.6 72.0,391.5 73.5,388.8 75.0,385.8 76.5,388.1 78.0,388.3 79.5,385.2 81.0,387.7 82.5,386.7 84.0,382.7 85.5,385.6 87.0,380.7 88.5,377.5 90.0,380.7 91.5,381.0 93.0,378.7 94.5,379.0 96.0,381.6 97.5,383.8 99.0,384.3 100.5,382.5 102.0,382.7 103.5,380.9 105.0,382.6 106.5,383.5 108.0,383.4 109.5,383.5 111.0,382.5 112.5,384.3 114.0,379.0 115.5,377.0 117.0,378.1 118.5,376.2 120.0,378.6 121.5,379.3 123.0,378.1 124.5,378.0 126.0,380.4 127.5,385.0 129.0,384.0 130.5,383.1 132.0,382.6 133.5,385.9 135.0,389.2 136.5,353.5 138.0,326.0 139.5,339.3 141.0,356.8 142.5,372.3 144.0,381.3 145.5,386.1 147.0,386.8 148.5,389.4 150.0,388.7 151.5,386.7 153.0,387.5 154.5,383.8 156.0,386.7 157.5,387.5 159.0,386.6 160.5,390.0 162.0,386.5 163.5,381.9 165.0,381.6 166.5,381.4 168.0,383.2 169.5,383.7 171.0,379.2 172.5,380.1 174.0,383.4 175.5,383.4 177.0,380.3 178.5,380.8 180.0,387.2 181.5,385.6 183.0,383.7 184.5,384.8 186.0,382.9 187.5,382.8 189.0,381.7 190.5,379.3 192.0,382.6 193.5,381.8 195.0,372.6 196.5,373.7 198.0,379.2 199.5,379.8 201.0,379.8 202.5,379.8 204.0,380.7 205.5,380.1 207.0,381.9 208.5,381.8 210.0,381.9 211.5,380.8 213.0,379.3 214.5,383.1 216.0,358.8 217.5,329.6 219.0,338.5 220.5,356.4 222.0,369.1 223.5,379.2 225.0,384.6 226.5,387.0 228.0,386.3 229.5,386.1 231.0,387.1 232.5,386.1 234.0,382.3 235.5,382.6 237.0,385.0 238.5,381.6 240.0,380.7 241.5,380.8 243.0,380.3 244.5,381.2 246.0,377.5 247.5,378.0 249.0,378.9 250.5,375.8 252.0,376.0 253.5,378.5 255.0,381.6 256.5,379.6 258.0,379.1 259.5,383.7 261.0,381.6 262.5,379.9 264.0,382.8 265.5,379.5 267.0,377.9 268.5,381.7 270.0,380.7 271.5,380.5 273.0,376.3 274.5,373.8 276.0,375.2 277.5,374.2 279.0,380.6 280.5,379.6 282.0,377.4 283.5,380.1 285.0,380.7 286.5,381.8 288.0,386.5 289.5,384.6 291.0,379.0 292.5,389.1 294.0,377.5 295.5,341.5 297.0,326.8 298.5,345.4 300.0,367.3 301.5,376.2 303.0,386.1 304.5,388.2 306.0,385.5 307.5,388.3 309.0,388.6 310.5,387.3 312.0,387.3 313.5,384.4 315.0,386.7 316.5,389.3 318.0,385.2 319.5,383.4 321.0,386.2 322.5,386.1 324.0,380.1 325.5,381.3 327.0,381.6 328.5,378.5 330.0,381.1 331.5,381.4 333.0,381.6 334.5,383.2 336.0,385.5 337.5,385.0 339.0,384.2 340.5,385.4 342.0,385.4 343.5,386.0 345.0,387.6 346.5,388.2 348.0,384.8 349.5,384.9 351.0,382.8 352.5,382.0 354.0,382.9 355.5,379.8 357.0,384.6 358.5,384.4 360.0,381.7 361.5,384.0 363.0,386.4 364.5,390.8 366.0,390.2 367.5,390.3 369.0,387.4 370.5,389.9 372.0,395.2 373.5,366.8 375.0,337.5 376.5,342.5 378.0,360.0 379.5,376.2 381.0,388.0 382.5,393.6 384.0,394.6 385.5,393.1 387.0,391.8 388.5,395.3 390.0,396.1 391.5,393.9 393.0,392.6 394.5,391.6 396.0,393.5 397.5,391.6 399.0,390.7 400.5,392.8 402.0,388.5 403.5,387.8 405.0,388.0 406.5,386.7 408.0,388.0 409.5,388.2 411.0,393.4 412.5,391.6 414.0,387.1 415.5,389.9 417.0,392.1 418.5,392.8 420.0,389.4 421.5,390.7 423.0,392.2 424.5,390.0 426.0,390.8 427.5,390.0 429.0,390.1 430.5,387.6 432.0,384.3 433.5,387.7 435.0,385.4 436.5,383.8 438.0,388.9 439.5,386.4 441.0,386.0 442.5,388.3 444.0,392.0 445.5,390.3 447.0,387.7 448.5,392.5 450.0,393.9 451.5,398.2 453.0,370.6 454.5,334.1 456.0,341.4 457.5,360.1 459.0,376.2 460.5,387.6 462.0,391.7 463.5,392.1 465.0,394.9 466.5,399.9 468.0,397.5 469.5,396.4 471.0,396.0 472.5,395.7 474.0,395.9 475.5,394.1 477.0,396.1 478.5,395.8 480.0,392.4 481.5,391.4 483.0,389.8 484.5,390.8 486.0,390.4 487.5,387.6 489.0,390.6 490.5,393.0 492.0,392.1 493.5,393.3 495.0,393.8 496.5,392.0 498.0,391.3 499.5,391.9 501.0,392.5 502.5,394.4 504.0,392.8 505.5,391.2 507.0,392.5 508.5,389.6 510.0,385.4 511.5,382.5 513.0,384.8 514.5,385.9 516.0,385.6 517.5,387.2 519.0,387.3 520.5,390.2 522.0,388.8 523.5,392.7 525.0,391.0 526.5,388.5 528.0,393.2 529.5,387.6 531.0,396.1 532.5,383.6 534.0,348.0 535.5,347.4 537.0,361.4 538.5,375.1 540.0,386.0 541.5,391.1 543.0,395.3 544.5,394.4 546.0,394.4 547.5,394.5 549.0,392.3 550.5,394.3 552.0,398.0 553.5,394.5 555.0,395.2 556.5,396.0 558.0,392.1 559.5,393.7 561.0,391.8 562.5,388.0 564.0,385.2 565.5,385.9 567.0,384.6 568.5,383.7 570.0,389.9 571.5,388.4 573.0,387.9 574.5,387.6 576.0,389.4 577.5,392.1 579.0,387.3 580.5,389.7 582.0,391.9 583.5,389.6 585.0,389.5 586.5,389.4 588.0,386.0 589.5,386.4 591.0,386.5 592.5,383.2 594.0,384.6 595.5,384.1 597.0,385.4 598.5,389.6 600.0,389.7 601.5,388.0 603.0,391.7 604.5,392.5 606.0,386.8 607.5,392.4 609.0,396.9 610.5,371.7 612.0,341.5 613.5,337.8 615.0,357.6 616.5,376.0 618.0,383.7 619.5,393.4 621.0,394.0 622.5,392.4 624.0,398.5 625.5,395.1 627.0,392.8 628.5,394.0 630.0,391.4 631.5,392.7 633.0,393.1 634.5,394.3 636.0,388.3 637.5,387.9 639.0,390.9 640.5,385.5 642.0,386.8 643.5,386.7 645.0,387.0 646.5,388.8 648.0,389.7 649.5,390.1 651.0,390.4 652.5,392.8 654.0,392.2 655.5,389.5 657.0,389.5 658.5,389.4 660.0,390.7 661.5,392.5 663.0,389.2 664.5,389.8 666.0,391.3 667.5,386.1 669.0,388.0 670.5,389.2 672.0,383.2 673.5,385.0 675.0,386.4 676.5,387.9 678.0,385.7 679.5,383.4 681.0,390.3 682.5,391.5 684.0,392.2 685.5,392.4 687.0,390.4 688.5,397.4 690.0,378.4 691.5,340.2 693.0,339.7 694.5,355.3 696.0,372.1 697.5,388.6 699.0,390.6 700.5,392.6 702.0,392.7 703.5,394.2 705.0,395.2 706.5,393.1 708.0,395.2 709.5,394.9 711.0,395.1 712.5,393.1 714.0,391.0 715.5,393.4 717.0,390.6 718.5,388.0 720.0,390.3 721.5,389.4 723.0,385.5 724.5,386.1 726.0,387.3 727.5,385.1 729.0,387.7 730.5,391.5 732.0,389.8 733.5,390.1 735.0,394.5 736.5,392.3 738.0,387.3 739.5,388.2 741.0,390.6 742.5,390.2 744.0,391.5 745.5,391.1 747.0,386.9 748.5,387.6\"/><text class=\"lead\" x=\"4\" y=\"21\">I</text><text class=\"lead\" x=\"379\" y=\"21\">AVR</text><text class=\"lead\" x=\"754\" y=\"21\">V1</text><text class=\"lead\" x=\"1129\" y=\"21\">V4</text><text class=\"lead\" x=\"4\" y=\"129\">II</text><text class=\"lead\" x=\"379\" y=\"129\">AVL</text><text class=\"lead\" x=\"754\" y=\"129\">V2</text><text class=\"lead\" x=\"1129\" y=\"129\">V5</text><text class=\"lead\" x=\"4\" y=\"237\">III</text><text class=\"lead\" x=\"379\" y=\"237\">AVF</text><text class=\"lead\" x=\"754\" y=\"237\">V3</text><text class=\"lead\" x=\"1129\" y=\"237\">V6</text><text class=\"lead\" x=\"4\" y=\"346\">II (rhythm)</text><text class=\"cap\" x=\"4\" y=\"452\">12유도 · 실데이터(PTB-XL, CC-BY) · 급성 심근경색</text></svg>"
 },
 {
  "id": "usmle-2026-0036",
  "exam": "usmle",
  "step": "Step 2",
  "subject": "Internal Medicine",
  "subject_file": "Internal Medicine",
  "subtopic": "Complete Left Bundle Branch Block (12-lead, real ECG)",
  "type": "Complete Left Bundle Branch Block (12-lead, real ECG)",
  "difficulty": 4,
  "created": "2026-07-07",
  "vignette": "A 70-year-old woman has a 12-lead electrocardiogram during an outpatient visit. The QRS duration is prolonged. There is a broad, notched, monophasic R wave in leads I and V6 and a predominantly negative QRS (QS/rS) in V1, with loss of the normal septal q waves.",
  "question": "Which of the following is the most likely diagnosis?",
  "options": [
   "Complete left bundle branch block",
   "Complete right bundle branch block",
   "Wolff-Parkinson-White pattern",
   "Left ventricular hypertrophy without conduction delay",
   "Hyperkalemia"
  ],
  "answer": 1,
  "explanationText": "- 정답근거: 넓은 QRS(≥120 ms) + I·V6의 넓고 노치된 단일 R파 + V1의\n  QS/rS + 중격 q파 소실 → 완전좌각차단(CLBBB).\n- 오답감별(낚시 주의): (B) 우각차단(CRBBB)은 정반대 — V1의 rSR′(M)와\n  I·V6의 넓은 S파. \"넓은 QRS면 다 RBBB\"로 넘겨짚기 쉬운 함정. (C) WPW는 짧은\n  PR+델타파. (D) LVH 단독은 전압 증가가 핵심이지 QRS를 크게 넓히지 않는다. (E)\n  고칼륨은 뾰족T·사인파 등 전해질 맥락을 동반.\n- 임상핵심: V1 형태로 좌우 각차단을 가른다(단일 R=LBBB / rSR′=RBBB). 새 CLBBB\n  + 허혈흉통 = STEMI-equivalent, CLBBB에서 MI는 Sgarbossa 기준으로 판단.\n- 자료 관련: 12유도는 오픈 DB(PTB-XL, CC-BY)의 실제 CLBBB 기록을 렌더(도식화).\n- 출처: PTB-XL (PhysioNet); AHA/ACCF/HRS ECG interpretation.",
  "explanationItems": [
   {
    "k": "정답근거",
    "v": "넓은 QRS(≥120 ms) + I·V6의 넓고 노치된 단일 R파 + V1의 QS/rS + 중격 q파 소실 → 완전좌각차단(CLBBB)."
   },
   {
    "k": "오답감별(낚시 주의)",
    "v": "(B) 우각차단(CRBBB)은 정반대 — V1의 rSR′(M)와 I·V6의 넓은 S파. \"넓은 QRS면 다 RBBB\"로 넘겨짚기 쉬운 함정. (C) WPW는 짧은 PR+델타파. (D) LVH 단독은 전압 증가가 핵심이지 QRS를 크게 넓히지 않는다. (E) *고칼륨은 뾰족T·사인파 등 전해질 맥락을 동반."
   },
   {
    "k": "임상핵심",
    "v": "V1 형태로 좌우 각차단을 가른다(단일 R=LBBB / rSR′=RBBB). 새 CLBBB + 허혈흉통 = STEMI-equivalent, CLBBB에서 MI는 Sgarbossa 기준으로 판단."
   },
   {
    "k": "자료 관련",
    "v": "12유도는 오픈 DB(PTB-XL, CC-BY)의 실제 CLBBB 기록을 렌더(도식화)."
   },
   {
    "k": "출처",
    "v": "PTB-XL (PhysioNet); AHA/ACCF/HRS ECG interpretation."
   }
  ],
  "source": "USMLE-style / MedKOS · ECG: PTB-XL 1.0.3 (PhysioNet, CC-BY 4.0)",
  "vitals": [],
  "labs": [],
  "appendix": {
   "가이드라인": "넓은 QRS(≥120 ms) 감별 — 12유도 형태\n─────────────────────────────────────\nCLBBB : I·V6 넓은 단일 R(노치) · V1 QS/rS · 중격 q 소실\nCRBBB : V1–V2 rSR′(M) · I·V6 넓은 S\nWPW   : PR 단축 + 델타파\n고칼륨 : 뾰족 T → QRS 확대 → 사인파(전해질 맥락)\n",
   "최신지견": "새 CLBBB + 허혈흉통 = STEMI-equivalent(재관류 고려). CLBBB에서는 통상 ST 기준으로 MI를 읽기 어려워 Sgarbossa 기준을 쓴다.",
   "참고문헌": [
    "PTB-XL (PhysioNet, CC-BY 4.0)",
    "AHA/ACCF/HRS ECG Interpretation (Intraventricular Conduction)"
   ]
  },
  "figureSvg": "<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 1500 456\" width=\"1500\" height=\"456\" role=\"img\" aria-label=\"12-lead ECG 12유도 · 실데이터(PTB-XL, CC-BY) · 완전좌각차단\"><style>.bg{fill:#fff}.gmin{stroke:#f4c9c9;stroke-width:0.5}.gmaj{stroke:#e59a9a;stroke-width:1}.trace{fill:none;stroke:#111;stroke-width:1.2;stroke-linejoin:round}.lead{font:bold 11px sans-serif;fill:#333}.cap{font:11px sans-serif;fill:#555}</style><rect class=\"bg\" x=\"0\" y=\"0\" width=\"1500\" height=\"440\"/><line x1=\"0\" y1=\"0\" x2=\"0\" y2=\"440\" class=\"gmaj\"/><line x1=\"6\" y1=\"0\" x2=\"6\" y2=\"440\" class=\"gmin\"/><line x1=\"12\" y1=\"0\" x2=\"12\" y2=\"440\" class=\"gmin\"/><line x1=\"18\" y1=\"0\" x2=\"18\" y2=\"440\" class=\"gmin\"/><line x1=\"24\" y1=\"0\" x2=\"24\" y2=\"440\" class=\"gmin\"/><line x1=\"30\" y1=\"0\" x2=\"30\" y2=\"440\" class=\"gmaj\"/><line x1=\"36\" y1=\"0\" x2=\"36\" y2=\"440\" class=\"gmin\"/><line x1=\"42\" y1=\"0\" x2=\"42\" y2=\"440\" class=\"gmin\"/><line x1=\"48\" y1=\"0\" x2=\"48\" y2=\"440\" class=\"gmin\"/><line x1=\"54\" y1=\"0\" x2=\"54\" y2=\"440\" class=\"gmin\"/><line x1=\"60\" y1=\"0\" x2=\"60\" y2=\"440\" class=\"gmaj\"/><line x1=\"66\" y1=\"0\" x2=\"66\" y2=\"440\" class=\"gmin\"/><line x1=\"72\" y1=\"0\" x2=\"72\" y2=\"440\" class=\"gmin\"/><line x1=\"78\" y1=\"0\" x2=\"78\" y2=\"440\" class=\"gmin\"/><line x1=\"84\" y1=\"0\" x2=\"84\" y2=\"440\" class=\"gmin\"/><line x1=\"90\" y1=\"0\" x2=\"90\" y2=\"440\" class=\"gmaj\"/><line x1=\"96\" y1=\"0\" x2=\"96\" y2=\"440\" class=\"gmin\"/><line x1=\"102\" y1=\"0\" x2=\"102\" y2=\"440\" class=\"gmin\"/><line x1=\"108\" y1=\"0\" x2=\"108\" y2=\"440\" class=\"gmin\"/><line x1=\"114\" y1=\"0\" x2=\"114\" y2=\"440\" class=\"gmin\"/><line x1=\"120\" y1=\"0\" x2=\"120\" y2=\"440\" class=\"gmaj\"/><line x1=\"126\" y1=\"0\" x2=\"126\" y2=\"440\" class=\"gmin\"/><line x1=\"132\" y1=\"0\" x2=\"132\" y2=\"440\" class=\"gmin\"/><line x1=\"138\" y1=\"0\" x2=\"138\" y2=\"440\" class=\"gmin\"/><line x1=\"144\" y1=\"0\" x2=\"144\" y2=\"440\" class=\"gmin\"/><line x1=\"150\" y1=\"0\" x2=\"150\" y2=\"440\" class=\"gmaj\"/><line x1=\"156\" y1=\"0\" x2=\"156\" y2=\"440\" class=\"gmin\"/><line x1=\"162\" y1=\"0\" x2=\"162\" y2=\"440\" class=\"gmin\"/><line x1=\"168\" y1=\"0\" x2=\"168\" y2=\"440\" class=\"gmin\"/><line x1=\"174\" y1=\"0\" x2=\"174\" y2=\"440\" class=\"gmin\"/><line x1=\"180\" y1=\"0\" x2=\"180\" y2=\"440\" class=\"gmaj\"/><line x1=\"186\" y1=\"0\" x2=\"186\" y2=\"440\" class=\"gmin\"/><line x1=\"192\" y1=\"0\" x2=\"192\" y2=\"440\" class=\"gmin\"/><line x1=\"198\" y1=\"0\" x2=\"198\" y2=\"440\" class=\"gmin\"/><line x1=\"204\" y1=\"0\" x2=\"204\" y2=\"440\" class=\"gmin\"/><line x1=\"210\" y1=\"0\" x2=\"210\" y2=\"440\" class=\"gmaj\"/><line x1=\"216\" y1=\"0\" x2=\"216\" y2=\"440\" class=\"gmin\"/><line x1=\"222\" y1=\"0\" x2=\"222\" y2=\"440\" class=\"gmin\"/><line x1=\"228\" y1=\"0\" x2=\"228\" y2=\"440\" class=\"gmin\"/><line x1=\"234\" y1=\"0\" x2=\"234\" y2=\"440\" class=\"gmin\"/><line x1=\"240\" y1=\"0\" x2=\"240\" y2=\"440\" class=\"gmaj\"/><line x1=\"246\" y1=\"0\" x2=\"246\" y2=\"440\" class=\"gmin\"/><line x1=\"252\" y1=\"0\" x2=\"252\" y2=\"440\" class=\"gmin\"/><line x1=\"258\" y1=\"0\" x2=\"258\" y2=\"440\" class=\"gmin\"/><line x1=\"264\" y1=\"0\" x2=\"264\" y2=\"440\" class=\"gmin\"/><line x1=\"270\" y1=\"0\" x2=\"270\" y2=\"440\" class=\"gmaj\"/><line x1=\"276\" y1=\"0\" x2=\"276\" y2=\"440\" class=\"gmin\"/><line x1=\"282\" y1=\"0\" x2=\"282\" y2=\"440\" class=\"gmin\"/><line x1=\"288\" y1=\"0\" x2=\"288\" y2=\"440\" class=\"gmin\"/><line x1=\"294\" y1=\"0\" x2=\"294\" y2=\"440\" class=\"gmin\"/><line x1=\"300\" y1=\"0\" x2=\"300\" y2=\"440\" class=\"gmaj\"/><line x1=\"306\" y1=\"0\" x2=\"306\" y2=\"440\" class=\"gmin\"/><line x1=\"312\" y1=\"0\" x2=\"312\" y2=\"440\" class=\"gmin\"/><line x1=\"318\" y1=\"0\" x2=\"318\" y2=\"440\" class=\"gmin\"/><line x1=\"324\" y1=\"0\" x2=\"324\" y2=\"440\" class=\"gmin\"/><line x1=\"330\" y1=\"0\" x2=\"330\" y2=\"440\" class=\"gmaj\"/><line x1=\"336\" y1=\"0\" x2=\"336\" y2=\"440\" class=\"gmin\"/><line x1=\"342\" y1=\"0\" x2=\"342\" y2=\"440\" class=\"gmin\"/><line x1=\"348\" y1=\"0\" x2=\"348\" y2=\"440\" class=\"gmin\"/><line x1=\"354\" y1=\"0\" x2=\"354\" y2=\"440\" class=\"gmin\"/><line x1=\"360\" y1=\"0\" x2=\"360\" y2=\"440\" class=\"gmaj\"/><line x1=\"366\" y1=\"0\" x2=\"366\" y2=\"440\" class=\"gmin\"/><line x1=\"372\" y1=\"0\" x2=\"372\" y2=\"440\" class=\"gmin\"/><line x1=\"378\" y1=\"0\" x2=\"378\" y2=\"440\" class=\"gmin\"/><line x1=\"384\" y1=\"0\" x2=\"384\" y2=\"440\" class=\"gmin\"/><line x1=\"390\" y1=\"0\" x2=\"390\" y2=\"440\" class=\"gmaj\"/><line x1=\"396\" y1=\"0\" x2=\"396\" y2=\"440\" class=\"gmin\"/><line x1=\"402\" y1=\"0\" x2=\"402\" y2=\"440\" class=\"gmin\"/><line x1=\"408\" y1=\"0\" x2=\"408\" y2=\"440\" class=\"gmin\"/><line x1=\"414\" y1=\"0\" x2=\"414\" y2=\"440\" class=\"gmin\"/><line x1=\"420\" y1=\"0\" x2=\"420\" y2=\"440\" class=\"gmaj\"/><line x1=\"426\" y1=\"0\" x2=\"426\" y2=\"440\" class=\"gmin\"/><line x1=\"432\" y1=\"0\" x2=\"432\" y2=\"440\" class=\"gmin\"/><line x1=\"438\" y1=\"0\" x2=\"438\" y2=\"440\" class=\"gmin\"/><line x1=\"444\" y1=\"0\" x2=\"444\" y2=\"440\" class=\"gmin\"/><line x1=\"450\" y1=\"0\" x2=\"450\" y2=\"440\" class=\"gmaj\"/><line x1=\"456\" y1=\"0\" x2=\"456\" y2=\"440\" class=\"gmin\"/><line x1=\"462\" y1=\"0\" x2=\"462\" y2=\"440\" class=\"gmin\"/><line x1=\"468\" y1=\"0\" x2=\"468\" y2=\"440\" class=\"gmin\"/><line x1=\"474\" y1=\"0\" x2=\"474\" y2=\"440\" class=\"gmin\"/><line x1=\"480\" y1=\"0\" x2=\"480\" y2=\"440\" class=\"gmaj\"/><line x1=\"486\" y1=\"0\" x2=\"486\" y2=\"440\" class=\"gmin\"/><line x1=\"492\" y1=\"0\" x2=\"492\" y2=\"440\" class=\"gmin\"/><line x1=\"498\" y1=\"0\" x2=\"498\" y2=\"440\" class=\"gmin\"/><line x1=\"504\" y1=\"0\" x2=\"504\" y2=\"440\" class=\"gmin\"/><line x1=\"510\" y1=\"0\" x2=\"510\" y2=\"440\" class=\"gmaj\"/><line x1=\"516\" y1=\"0\" x2=\"516\" y2=\"440\" class=\"gmin\"/><line x1=\"522\" y1=\"0\" x2=\"522\" y2=\"440\" class=\"gmin\"/><line x1=\"528\" y1=\"0\" x2=\"528\" y2=\"440\" class=\"gmin\"/><line x1=\"534\" y1=\"0\" x2=\"534\" y2=\"440\" class=\"gmin\"/><line x1=\"540\" y1=\"0\" x2=\"540\" y2=\"440\" class=\"gmaj\"/><line x1=\"546\" y1=\"0\" x2=\"546\" y2=\"440\" class=\"gmin\"/><line x1=\"552\" y1=\"0\" x2=\"552\" y2=\"440\" class=\"gmin\"/><line x1=\"558\" y1=\"0\" x2=\"558\" y2=\"440\" class=\"gmin\"/><line x1=\"564\" y1=\"0\" x2=\"564\" y2=\"440\" class=\"gmin\"/><line x1=\"570\" y1=\"0\" x2=\"570\" y2=\"440\" class=\"gmaj\"/><line x1=\"576\" y1=\"0\" x2=\"576\" y2=\"440\" class=\"gmin\"/><line x1=\"582\" y1=\"0\" x2=\"582\" y2=\"440\" class=\"gmin\"/><line x1=\"588\" y1=\"0\" x2=\"588\" y2=\"440\" class=\"gmin\"/><line x1=\"594\" y1=\"0\" x2=\"594\" y2=\"440\" class=\"gmin\"/><line x1=\"600\" y1=\"0\" x2=\"600\" y2=\"440\" class=\"gmaj\"/><line x1=\"606\" y1=\"0\" x2=\"606\" y2=\"440\" class=\"gmin\"/><line x1=\"612\" y1=\"0\" x2=\"612\" y2=\"440\" class=\"gmin\"/><line x1=\"618\" y1=\"0\" x2=\"618\" y2=\"440\" class=\"gmin\"/><line x1=\"624\" y1=\"0\" x2=\"624\" y2=\"440\" class=\"gmin\"/><line x1=\"630\" y1=\"0\" x2=\"630\" y2=\"440\" class=\"gmaj\"/><line x1=\"636\" y1=\"0\" x2=\"636\" y2=\"440\" class=\"gmin\"/><line x1=\"642\" y1=\"0\" x2=\"642\" y2=\"440\" class=\"gmin\"/><line x1=\"648\" y1=\"0\" x2=\"648\" y2=\"440\" class=\"gmin\"/><line x1=\"654\" y1=\"0\" x2=\"654\" y2=\"440\" class=\"gmin\"/><line x1=\"660\" y1=\"0\" x2=\"660\" y2=\"440\" class=\"gmaj\"/><line x1=\"666\" y1=\"0\" x2=\"666\" y2=\"440\" class=\"gmin\"/><line x1=\"672\" y1=\"0\" x2=\"672\" y2=\"440\" class=\"gmin\"/><line x1=\"678\" y1=\"0\" x2=\"678\" y2=\"440\" class=\"gmin\"/><line x1=\"684\" y1=\"0\" x2=\"684\" y2=\"440\" class=\"gmin\"/><line x1=\"690\" y1=\"0\" x2=\"690\" y2=\"440\" class=\"gmaj\"/><line x1=\"696\" y1=\"0\" x2=\"696\" y2=\"440\" class=\"gmin\"/><line x1=\"702\" y1=\"0\" x2=\"702\" y2=\"440\" class=\"gmin\"/><line x1=\"708\" y1=\"0\" x2=\"708\" y2=\"440\" class=\"gmin\"/><line x1=\"714\" y1=\"0\" x2=\"714\" y2=\"440\" class=\"gmin\"/><line x1=\"720\" y1=\"0\" x2=\"720\" y2=\"440\" class=\"gmaj\"/><line x1=\"726\" y1=\"0\" x2=\"726\" y2=\"440\" class=\"gmin\"/><line x1=\"732\" y1=\"0\" x2=\"732\" y2=\"440\" class=\"gmin\"/><line x1=\"738\" y1=\"0\" x2=\"738\" y2=\"440\" class=\"gmin\"/><line x1=\"744\" y1=\"0\" x2=\"744\" y2=\"440\" class=\"gmin\"/><line x1=\"750\" y1=\"0\" x2=\"750\" y2=\"440\" class=\"gmaj\"/><line x1=\"756\" y1=\"0\" x2=\"756\" y2=\"440\" class=\"gmin\"/><line x1=\"762\" y1=\"0\" x2=\"762\" y2=\"440\" class=\"gmin\"/><line x1=\"768\" y1=\"0\" x2=\"768\" y2=\"440\" class=\"gmin\"/><line x1=\"774\" y1=\"0\" x2=\"774\" y2=\"440\" class=\"gmin\"/><line x1=\"780\" y1=\"0\" x2=\"780\" y2=\"440\" class=\"gmaj\"/><line x1=\"786\" y1=\"0\" x2=\"786\" y2=\"440\" class=\"gmin\"/><line x1=\"792\" y1=\"0\" x2=\"792\" y2=\"440\" class=\"gmin\"/><line x1=\"798\" y1=\"0\" x2=\"798\" y2=\"440\" class=\"gmin\"/><line x1=\"804\" y1=\"0\" x2=\"804\" y2=\"440\" class=\"gmin\"/><line x1=\"810\" y1=\"0\" x2=\"810\" y2=\"440\" class=\"gmaj\"/><line x1=\"816\" y1=\"0\" x2=\"816\" y2=\"440\" class=\"gmin\"/><line x1=\"822\" y1=\"0\" x2=\"822\" y2=\"440\" class=\"gmin\"/><line x1=\"828\" y1=\"0\" x2=\"828\" y2=\"440\" class=\"gmin\"/><line x1=\"834\" y1=\"0\" x2=\"834\" y2=\"440\" class=\"gmin\"/><line x1=\"840\" y1=\"0\" x2=\"840\" y2=\"440\" class=\"gmaj\"/><line x1=\"846\" y1=\"0\" x2=\"846\" y2=\"440\" class=\"gmin\"/><line x1=\"852\" y1=\"0\" x2=\"852\" y2=\"440\" class=\"gmin\"/><line x1=\"858\" y1=\"0\" x2=\"858\" y2=\"440\" class=\"gmin\"/><line x1=\"864\" y1=\"0\" x2=\"864\" y2=\"440\" class=\"gmin\"/><line x1=\"870\" y1=\"0\" x2=\"870\" y2=\"440\" class=\"gmaj\"/><line x1=\"876\" y1=\"0\" x2=\"876\" y2=\"440\" class=\"gmin\"/><line x1=\"882\" y1=\"0\" x2=\"882\" y2=\"440\" class=\"gmin\"/><line x1=\"888\" y1=\"0\" x2=\"888\" y2=\"440\" class=\"gmin\"/><line x1=\"894\" y1=\"0\" x2=\"894\" y2=\"440\" class=\"gmin\"/><line x1=\"900\" y1=\"0\" x2=\"900\" y2=\"440\" class=\"gmaj\"/><line x1=\"906\" y1=\"0\" x2=\"906\" y2=\"440\" class=\"gmin\"/><line x1=\"912\" y1=\"0\" x2=\"912\" y2=\"440\" class=\"gmin\"/><line x1=\"918\" y1=\"0\" x2=\"918\" y2=\"440\" class=\"gmin\"/><line x1=\"924\" y1=\"0\" x2=\"924\" y2=\"440\" class=\"gmin\"/><line x1=\"930\" y1=\"0\" x2=\"930\" y2=\"440\" class=\"gmaj\"/><line x1=\"936\" y1=\"0\" x2=\"936\" y2=\"440\" class=\"gmin\"/><line x1=\"942\" y1=\"0\" x2=\"942\" y2=\"440\" class=\"gmin\"/><line x1=\"948\" y1=\"0\" x2=\"948\" y2=\"440\" class=\"gmin\"/><line x1=\"954\" y1=\"0\" x2=\"954\" y2=\"440\" class=\"gmin\"/><line x1=\"960\" y1=\"0\" x2=\"960\" y2=\"440\" class=\"gmaj\"/><line x1=\"966\" y1=\"0\" x2=\"966\" y2=\"440\" class=\"gmin\"/><line x1=\"972\" y1=\"0\" x2=\"972\" y2=\"440\" class=\"gmin\"/><line x1=\"978\" y1=\"0\" x2=\"978\" y2=\"440\" class=\"gmin\"/><line x1=\"984\" y1=\"0\" x2=\"984\" y2=\"440\" class=\"gmin\"/><line x1=\"990\" y1=\"0\" x2=\"990\" y2=\"440\" class=\"gmaj\"/><line x1=\"996\" y1=\"0\" x2=\"996\" y2=\"440\" class=\"gmin\"/><line x1=\"1002\" y1=\"0\" x2=\"1002\" y2=\"440\" class=\"gmin\"/><line x1=\"1008\" y1=\"0\" x2=\"1008\" y2=\"440\" class=\"gmin\"/><line x1=\"1014\" y1=\"0\" x2=\"1014\" y2=\"440\" class=\"gmin\"/><line x1=\"1020\" y1=\"0\" x2=\"1020\" y2=\"440\" class=\"gmaj\"/><line x1=\"1026\" y1=\"0\" x2=\"1026\" y2=\"440\" class=\"gmin\"/><line x1=\"1032\" y1=\"0\" x2=\"1032\" y2=\"440\" class=\"gmin\"/><line x1=\"1038\" y1=\"0\" x2=\"1038\" y2=\"440\" class=\"gmin\"/><line x1=\"1044\" y1=\"0\" x2=\"1044\" y2=\"440\" class=\"gmin\"/><line x1=\"1050\" y1=\"0\" x2=\"1050\" y2=\"440\" class=\"gmaj\"/><line x1=\"1056\" y1=\"0\" x2=\"1056\" y2=\"440\" class=\"gmin\"/><line x1=\"1062\" y1=\"0\" x2=\"1062\" y2=\"440\" class=\"gmin\"/><line x1=\"1068\" y1=\"0\" x2=\"1068\" y2=\"440\" class=\"gmin\"/><line x1=\"1074\" y1=\"0\" x2=\"1074\" y2=\"440\" class=\"gmin\"/><line x1=\"1080\" y1=\"0\" x2=\"1080\" y2=\"440\" class=\"gmaj\"/><line x1=\"1086\" y1=\"0\" x2=\"1086\" y2=\"440\" class=\"gmin\"/><line x1=\"1092\" y1=\"0\" x2=\"1092\" y2=\"440\" class=\"gmin\"/><line x1=\"1098\" y1=\"0\" x2=\"1098\" y2=\"440\" class=\"gmin\"/><line x1=\"1104\" y1=\"0\" x2=\"1104\" y2=\"440\" class=\"gmin\"/><line x1=\"1110\" y1=\"0\" x2=\"1110\" y2=\"440\" class=\"gmaj\"/><line x1=\"1116\" y1=\"0\" x2=\"1116\" y2=\"440\" class=\"gmin\"/><line x1=\"1122\" y1=\"0\" x2=\"1122\" y2=\"440\" class=\"gmin\"/><line x1=\"1128\" y1=\"0\" x2=\"1128\" y2=\"440\" class=\"gmin\"/><line x1=\"1134\" y1=\"0\" x2=\"1134\" y2=\"440\" class=\"gmin\"/><line x1=\"1140\" y1=\"0\" x2=\"1140\" y2=\"440\" class=\"gmaj\"/><line x1=\"1146\" y1=\"0\" x2=\"1146\" y2=\"440\" class=\"gmin\"/><line x1=\"1152\" y1=\"0\" x2=\"1152\" y2=\"440\" class=\"gmin\"/><line x1=\"1158\" y1=\"0\" x2=\"1158\" y2=\"440\" class=\"gmin\"/><line x1=\"1164\" y1=\"0\" x2=\"1164\" y2=\"440\" class=\"gmin\"/><line x1=\"1170\" y1=\"0\" x2=\"1170\" y2=\"440\" class=\"gmaj\"/><line x1=\"1176\" y1=\"0\" x2=\"1176\" y2=\"440\" class=\"gmin\"/><line x1=\"1182\" y1=\"0\" x2=\"1182\" y2=\"440\" class=\"gmin\"/><line x1=\"1188\" y1=\"0\" x2=\"1188\" y2=\"440\" class=\"gmin\"/><line x1=\"1194\" y1=\"0\" x2=\"1194\" y2=\"440\" class=\"gmin\"/><line x1=\"1200\" y1=\"0\" x2=\"1200\" y2=\"440\" class=\"gmaj\"/><line x1=\"1206\" y1=\"0\" x2=\"1206\" y2=\"440\" class=\"gmin\"/><line x1=\"1212\" y1=\"0\" x2=\"1212\" y2=\"440\" class=\"gmin\"/><line x1=\"1218\" y1=\"0\" x2=\"1218\" y2=\"440\" class=\"gmin\"/><line x1=\"1224\" y1=\"0\" x2=\"1224\" y2=\"440\" class=\"gmin\"/><line x1=\"1230\" y1=\"0\" x2=\"1230\" y2=\"440\" class=\"gmaj\"/><line x1=\"1236\" y1=\"0\" x2=\"1236\" y2=\"440\" class=\"gmin\"/><line x1=\"1242\" y1=\"0\" x2=\"1242\" y2=\"440\" class=\"gmin\"/><line x1=\"1248\" y1=\"0\" x2=\"1248\" y2=\"440\" class=\"gmin\"/><line x1=\"1254\" y1=\"0\" x2=\"1254\" y2=\"440\" class=\"gmin\"/><line x1=\"1260\" y1=\"0\" x2=\"1260\" y2=\"440\" class=\"gmaj\"/><line x1=\"1266\" y1=\"0\" x2=\"1266\" y2=\"440\" class=\"gmin\"/><line x1=\"1272\" y1=\"0\" x2=\"1272\" y2=\"440\" class=\"gmin\"/><line x1=\"1278\" y1=\"0\" x2=\"1278\" y2=\"440\" class=\"gmin\"/><line x1=\"1284\" y1=\"0\" x2=\"1284\" y2=\"440\" class=\"gmin\"/><line x1=\"1290\" y1=\"0\" x2=\"1290\" y2=\"440\" class=\"gmaj\"/><line x1=\"1296\" y1=\"0\" x2=\"1296\" y2=\"440\" class=\"gmin\"/><line x1=\"1302\" y1=\"0\" x2=\"1302\" y2=\"440\" class=\"gmin\"/><line x1=\"1308\" y1=\"0\" x2=\"1308\" y2=\"440\" class=\"gmin\"/><line x1=\"1314\" y1=\"0\" x2=\"1314\" y2=\"440\" class=\"gmin\"/><line x1=\"1320\" y1=\"0\" x2=\"1320\" y2=\"440\" class=\"gmaj\"/><line x1=\"1326\" y1=\"0\" x2=\"1326\" y2=\"440\" class=\"gmin\"/><line x1=\"1332\" y1=\"0\" x2=\"1332\" y2=\"440\" class=\"gmin\"/><line x1=\"1338\" y1=\"0\" x2=\"1338\" y2=\"440\" class=\"gmin\"/><line x1=\"1344\" y1=\"0\" x2=\"1344\" y2=\"440\" class=\"gmin\"/><line x1=\"1350\" y1=\"0\" x2=\"1350\" y2=\"440\" class=\"gmaj\"/><line x1=\"1356\" y1=\"0\" x2=\"1356\" y2=\"440\" class=\"gmin\"/><line x1=\"1362\" y1=\"0\" x2=\"1362\" y2=\"440\" class=\"gmin\"/><line x1=\"1368\" y1=\"0\" x2=\"1368\" y2=\"440\" class=\"gmin\"/><line x1=\"1374\" y1=\"0\" x2=\"1374\" y2=\"440\" class=\"gmin\"/><line x1=\"1380\" y1=\"0\" x2=\"1380\" y2=\"440\" class=\"gmaj\"/><line x1=\"1386\" y1=\"0\" x2=\"1386\" y2=\"440\" class=\"gmin\"/><line x1=\"1392\" y1=\"0\" x2=\"1392\" y2=\"440\" class=\"gmin\"/><line x1=\"1398\" y1=\"0\" x2=\"1398\" y2=\"440\" class=\"gmin\"/><line x1=\"1404\" y1=\"0\" x2=\"1404\" y2=\"440\" class=\"gmin\"/><line x1=\"1410\" y1=\"0\" x2=\"1410\" y2=\"440\" class=\"gmaj\"/><line x1=\"1416\" y1=\"0\" x2=\"1416\" y2=\"440\" class=\"gmin\"/><line x1=\"1422\" y1=\"0\" x2=\"1422\" y2=\"440\" class=\"gmin\"/><line x1=\"1428\" y1=\"0\" x2=\"1428\" y2=\"440\" class=\"gmin\"/><line x1=\"1434\" y1=\"0\" x2=\"1434\" y2=\"440\" class=\"gmin\"/><line x1=\"1440\" y1=\"0\" x2=\"1440\" y2=\"440\" class=\"gmaj\"/><line x1=\"1446\" y1=\"0\" x2=\"1446\" y2=\"440\" class=\"gmin\"/><line x1=\"1452\" y1=\"0\" x2=\"1452\" y2=\"440\" class=\"gmin\"/><line x1=\"1458\" y1=\"0\" x2=\"1458\" y2=\"440\" class=\"gmin\"/><line x1=\"1464\" y1=\"0\" x2=\"1464\" y2=\"440\" class=\"gmin\"/><line x1=\"1470\" y1=\"0\" x2=\"1470\" y2=\"440\" class=\"gmaj\"/><line x1=\"1476\" y1=\"0\" x2=\"1476\" y2=\"440\" class=\"gmin\"/><line x1=\"1482\" y1=\"0\" x2=\"1482\" y2=\"440\" class=\"gmin\"/><line x1=\"1488\" y1=\"0\" x2=\"1488\" y2=\"440\" class=\"gmin\"/><line x1=\"1494\" y1=\"0\" x2=\"1494\" y2=\"440\" class=\"gmin\"/><line x1=\"1500\" y1=\"0\" x2=\"1500\" y2=\"440\" class=\"gmaj\"/><line x1=\"0\" y1=\"0\" x2=\"1500\" y2=\"0\" class=\"gmaj\"/><line x1=\"0\" y1=\"6\" x2=\"1500\" y2=\"6\" class=\"gmin\"/><line x1=\"0\" y1=\"12\" x2=\"1500\" y2=\"12\" class=\"gmin\"/><line x1=\"0\" y1=\"18\" x2=\"1500\" y2=\"18\" class=\"gmin\"/><line x1=\"0\" y1=\"24\" x2=\"1500\" y2=\"24\" class=\"gmin\"/><line x1=\"0\" y1=\"30\" x2=\"1500\" y2=\"30\" class=\"gmaj\"/><line x1=\"0\" y1=\"36\" x2=\"1500\" y2=\"36\" class=\"gmin\"/><line x1=\"0\" y1=\"42\" x2=\"1500\" y2=\"42\" class=\"gmin\"/><line x1=\"0\" y1=\"48\" x2=\"1500\" y2=\"48\" class=\"gmin\"/><line x1=\"0\" y1=\"54\" x2=\"1500\" y2=\"54\" class=\"gmin\"/><line x1=\"0\" y1=\"60\" x2=\"1500\" y2=\"60\" class=\"gmaj\"/><line x1=\"0\" y1=\"66\" x2=\"1500\" y2=\"66\" class=\"gmin\"/><line x1=\"0\" y1=\"72\" x2=\"1500\" y2=\"72\" class=\"gmin\"/><line x1=\"0\" y1=\"78\" x2=\"1500\" y2=\"78\" class=\"gmin\"/><line x1=\"0\" y1=\"84\" x2=\"1500\" y2=\"84\" class=\"gmin\"/><line x1=\"0\" y1=\"90\" x2=\"1500\" y2=\"90\" class=\"gmaj\"/><line x1=\"0\" y1=\"96\" x2=\"1500\" y2=\"96\" class=\"gmin\"/><line x1=\"0\" y1=\"102\" x2=\"1500\" y2=\"102\" class=\"gmin\"/><line x1=\"0\" y1=\"108\" x2=\"1500\" y2=\"108\" class=\"gmin\"/><line x1=\"0\" y1=\"114\" x2=\"1500\" y2=\"114\" class=\"gmin\"/><line x1=\"0\" y1=\"120\" x2=\"1500\" y2=\"120\" class=\"gmaj\"/><line x1=\"0\" y1=\"126\" x2=\"1500\" y2=\"126\" class=\"gmin\"/><line x1=\"0\" y1=\"132\" x2=\"1500\" y2=\"132\" class=\"gmin\"/><line x1=\"0\" y1=\"138\" x2=\"1500\" y2=\"138\" class=\"gmin\"/><line x1=\"0\" y1=\"144\" x2=\"1500\" y2=\"144\" class=\"gmin\"/><line x1=\"0\" y1=\"150\" x2=\"1500\" y2=\"150\" class=\"gmaj\"/><line x1=\"0\" y1=\"156\" x2=\"1500\" y2=\"156\" class=\"gmin\"/><line x1=\"0\" y1=\"162\" x2=\"1500\" y2=\"162\" class=\"gmin\"/><line x1=\"0\" y1=\"168\" x2=\"1500\" y2=\"168\" class=\"gmin\"/><line x1=\"0\" y1=\"174\" x2=\"1500\" y2=\"174\" class=\"gmin\"/><line x1=\"0\" y1=\"180\" x2=\"1500\" y2=\"180\" class=\"gmaj\"/><line x1=\"0\" y1=\"186\" x2=\"1500\" y2=\"186\" class=\"gmin\"/><line x1=\"0\" y1=\"192\" x2=\"1500\" y2=\"192\" class=\"gmin\"/><line x1=\"0\" y1=\"198\" x2=\"1500\" y2=\"198\" class=\"gmin\"/><line x1=\"0\" y1=\"204\" x2=\"1500\" y2=\"204\" class=\"gmin\"/><line x1=\"0\" y1=\"210\" x2=\"1500\" y2=\"210\" class=\"gmaj\"/><line x1=\"0\" y1=\"216\" x2=\"1500\" y2=\"216\" class=\"gmin\"/><line x1=\"0\" y1=\"222\" x2=\"1500\" y2=\"222\" class=\"gmin\"/><line x1=\"0\" y1=\"228\" x2=\"1500\" y2=\"228\" class=\"gmin\"/><line x1=\"0\" y1=\"234\" x2=\"1500\" y2=\"234\" class=\"gmin\"/><line x1=\"0\" y1=\"240\" x2=\"1500\" y2=\"240\" class=\"gmaj\"/><line x1=\"0\" y1=\"246\" x2=\"1500\" y2=\"246\" class=\"gmin\"/><line x1=\"0\" y1=\"252\" x2=\"1500\" y2=\"252\" class=\"gmin\"/><line x1=\"0\" y1=\"258\" x2=\"1500\" y2=\"258\" class=\"gmin\"/><line x1=\"0\" y1=\"264\" x2=\"1500\" y2=\"264\" class=\"gmin\"/><line x1=\"0\" y1=\"270\" x2=\"1500\" y2=\"270\" class=\"gmaj\"/><line x1=\"0\" y1=\"276\" x2=\"1500\" y2=\"276\" class=\"gmin\"/><line x1=\"0\" y1=\"282\" x2=\"1500\" y2=\"282\" class=\"gmin\"/><line x1=\"0\" y1=\"288\" x2=\"1500\" y2=\"288\" class=\"gmin\"/><line x1=\"0\" y1=\"294\" x2=\"1500\" y2=\"294\" class=\"gmin\"/><line x1=\"0\" y1=\"300\" x2=\"1500\" y2=\"300\" class=\"gmaj\"/><line x1=\"0\" y1=\"306\" x2=\"1500\" y2=\"306\" class=\"gmin\"/><line x1=\"0\" y1=\"312\" x2=\"1500\" y2=\"312\" class=\"gmin\"/><line x1=\"0\" y1=\"318\" x2=\"1500\" y2=\"318\" class=\"gmin\"/><line x1=\"0\" y1=\"324\" x2=\"1500\" y2=\"324\" class=\"gmin\"/><line x1=\"0\" y1=\"330\" x2=\"1500\" y2=\"330\" class=\"gmaj\"/><line x1=\"0\" y1=\"336\" x2=\"1500\" y2=\"336\" class=\"gmin\"/><line x1=\"0\" y1=\"342\" x2=\"1500\" y2=\"342\" class=\"gmin\"/><line x1=\"0\" y1=\"348\" x2=\"1500\" y2=\"348\" class=\"gmin\"/><line x1=\"0\" y1=\"354\" x2=\"1500\" y2=\"354\" class=\"gmin\"/><line x1=\"0\" y1=\"360\" x2=\"1500\" y2=\"360\" class=\"gmaj\"/><line x1=\"0\" y1=\"366\" x2=\"1500\" y2=\"366\" class=\"gmin\"/><line x1=\"0\" y1=\"372\" x2=\"1500\" y2=\"372\" class=\"gmin\"/><line x1=\"0\" y1=\"378\" x2=\"1500\" y2=\"378\" class=\"gmin\"/><line x1=\"0\" y1=\"384\" x2=\"1500\" y2=\"384\" class=\"gmin\"/><line x1=\"0\" y1=\"390\" x2=\"1500\" y2=\"390\" class=\"gmaj\"/><line x1=\"0\" y1=\"396\" x2=\"1500\" y2=\"396\" class=\"gmin\"/><line x1=\"0\" y1=\"402\" x2=\"1500\" y2=\"402\" class=\"gmin\"/><line x1=\"0\" y1=\"408\" x2=\"1500\" y2=\"408\" class=\"gmin\"/><line x1=\"0\" y1=\"414\" x2=\"1500\" y2=\"414\" class=\"gmin\"/><line x1=\"0\" y1=\"420\" x2=\"1500\" y2=\"420\" class=\"gmaj\"/><line x1=\"0\" y1=\"426\" x2=\"1500\" y2=\"426\" class=\"gmin\"/><line x1=\"0\" y1=\"432\" x2=\"1500\" y2=\"432\" class=\"gmin\"/><line x1=\"0\" y1=\"438\" x2=\"1500\" y2=\"438\" class=\"gmin\"/><polyline class=\"trace\" points=\"0.0,87.6 1.5,92.5 3.0,93.1 4.5,91.6 6.0,90.4 7.5,89.1 9.0,85.7 10.5,81.5 12.0,76.9 13.5,72.3 15.0,68.6 16.5,65.1 18.0,62.4 19.5,60.7 21.0,60.9 22.5,60.4 24.0,59.7 25.5,58.9 27.0,57.3 28.5,60.6 30.0,62.0 31.5,60.9 33.0,60.9 34.5,61.0 36.0,61.8 37.5,59.4 39.0,61.0 40.5,62.2 42.0,60.6 43.5,59.5 45.0,58.2 46.5,60.4 48.0,60.8 49.5,59.3 51.0,60.3 52.5,62.1 54.0,62.1 55.5,61.8 57.0,60.6 58.5,60.9 60.0,61.1 61.5,57.2 63.0,57.6 64.5,57.3 66.0,46.6 67.5,25.6 69.0,2.4 70.5,-13.6 72.0,-16.2 73.5,-12.4 75.0,-9.8 76.5,-0.4 78.0,11.8 79.5,20.8 81.0,33.7 82.5,50.1 84.0,62.2 85.5,71.1 87.0,78.4 88.5,79.5 90.0,81.4 91.5,83.7 93.0,84.1 94.5,88.8 96.0,90.2 97.5,90.8 99.0,93.5 100.5,92.8 102.0,92.1 103.5,90.7 105.0,87.4 106.5,84.7 108.0,81.3 109.5,75.9 111.0,71.4 112.5,68.8 114.0,64.5 115.5,60.8 117.0,59.4 118.5,58.9 120.0,60.5 121.5,60.0 123.0,57.0 124.5,56.9 126.0,59.6 127.5,62.6 129.0,62.5 130.5,60.2 132.0,60.3 133.5,60.1 135.0,60.8 136.5,63.3 138.0,62.3 139.5,61.5 141.0,59.4 142.5,54.9 144.0,60.1 145.5,64.1 147.0,60.4 148.5,60.6 150.0,61.0 151.5,60.4 153.0,62.4 154.5,63.4 156.0,62.7 157.5,60.9 159.0,58.5 160.5,57.3 162.0,53.8 163.5,43.5 165.0,20.8 166.5,-6.6 168.0,-17.6 169.5,-14.3 171.0,-13.5 172.5,-7.2 174.0,5.8 175.5,11.7 177.0,25.5 178.5,40.2 180.0,51.4 181.5,67.3 183.0,74.7 184.5,78.7 186.0,81.5 187.5,81.3 189.0,83.2 190.5,84.7 192.0,86.8 193.5,89.5 195.0,90.2 196.5,94.3 198.0,96.6 199.5,93.5 201.0,90.6 202.5,88.0 204.0,84.1 205.5,80.0 207.0,75.4 208.5,69.4 210.0,66.0 211.5,63.6 213.0,61.9 214.5,61.2 216.0,61.3 217.5,60.3 219.0,58.2 220.5,59.5 222.0,61.6 223.5,62.0 225.0,62.2 226.5,61.8 228.0,61.8 229.5,62.2 231.0,62.5 232.5,62.7 234.0,63.1 235.5,64.0 237.0,62.7 238.5,61.2 240.0,58.8 241.5,59.5 243.0,62.2 244.5,62.5 246.0,63.0 247.5,62.1 249.0,63.6 250.5,63.6 252.0,62.0 253.5,62.4 255.0,60.9 256.5,58.5 258.0,58.0 259.5,55.2 261.0,43.2 262.5,19.8 264.0,-5.1 265.5,-13.6 267.0,-12.3 268.5,-13.1 270.0,-6.5 271.5,6.7 273.0,13.9 274.5,26.3 276.0,41.5 277.5,53.8 279.0,67.9 280.5,76.0 282.0,79.9 283.5,81.3 285.0,83.6 286.5,86.2 288.0,88.0 289.5,88.9 291.0,91.0 292.5,93.2 294.0,92.2 295.5,93.8 297.0,93.8 298.5,92.9 300.0,90.0 301.5,85.6 303.0,82.2 304.5,75.3 306.0,70.8 307.5,68.8 309.0,65.9 310.5,65.7 312.0,63.1 313.5,60.7 315.0,62.8 316.5,63.2 318.0,63.7 319.5,62.8 321.0,61.8 322.5,61.6 324.0,61.2 325.5,61.9 327.0,62.8 328.5,63.9 330.0,64.3 331.5,65.8 333.0,65.5 334.5,63.9 336.0,62.1 337.5,59.4 339.0,60.7 340.5,63.7 342.0,64.9 343.5,64.2 345.0,62.5 346.5,62.8 348.0,63.9 349.5,64.6 351.0,65.9 352.5,65.2 354.0,63.1 355.5,60.8 357.0,59.9 358.5,51.9 360.0,31.2 361.5,8.2 363.0,-10.1 364.5,-15.3 366.0,-11.6 367.5,-8.3 369.0,-0.2 370.5,8.8 372.0,18.8 373.5,33.4\"/><polyline class=\"trace\" points=\"375.0,44.7 376.5,42.3 378.0,42.7 379.5,44.4 381.0,46.5 382.5,47.8 384.0,50.5 385.5,54.0 387.0,57.2 388.5,60.3 390.0,62.6 391.5,64.5 393.0,65.8 394.5,65.9 396.0,64.8 397.5,64.8 399.0,64.3 400.5,64.5 402.0,65.1 403.5,63.0 405.0,63.1 406.5,63.7 408.0,63.4 409.5,63.1 411.0,62.8 412.5,65.4 414.0,65.2 415.5,63.7 417.0,64.6 418.5,65.5 420.0,65.5 421.5,63.7 423.0,62.5 424.5,62.6 426.0,61.8 427.5,60.4 429.0,60.3 430.5,60.1 432.0,60.4 433.5,60.4 435.0,60.4 436.5,63.2 438.0,64.0 439.5,67.1 441.0,76.4 442.5,86.7 444.0,98.2 445.5,108.2 447.0,108.5 448.5,101.8 450.0,96.5 451.5,89.4 453.0,80.9 454.5,76.1 456.0,70.0 457.5,61.3 459.0,55.5 460.5,52.2 462.0,48.8 463.5,48.4 465.0,47.5 466.5,46.5 468.0,46.5 469.5,43.9 471.0,43.3 472.5,43.3 474.0,42.2 475.5,43.3 477.0,44.2 478.5,46.1 480.0,49.3 481.5,51.9 483.0,54.5 484.5,57.7 486.0,60.6 487.5,62.0 489.0,64.5 490.5,66.4 492.0,66.7 493.5,66.1 495.0,64.2 496.5,64.2 498.0,65.5 499.5,64.8 501.0,63.1 502.5,61.2 504.0,61.8 505.5,63.4 507.0,63.7 508.5,64.8 510.0,64.9 511.5,64.1 513.0,64.6 514.5,64.7 516.0,65.7 517.5,67.5 519.0,63.4 520.5,60.3 522.0,62.6 523.5,62.1 525.0,61.0 526.5,61.2 528.0,59.8 529.5,59.7 531.0,60.3 532.5,60.5 534.0,62.7 535.5,65.1 537.0,70.8 538.5,77.2 540.0,87.1 541.5,103.2 543.0,111.0 544.5,106.3 546.0,100.2 547.5,94.2 549.0,85.5 550.5,81.2 552.0,73.9 553.5,66.4 555.0,60.4 556.5,52.1 558.0,50.3 559.5,48.9 561.0,47.6 562.5,47.9 564.0,46.9 565.5,46.5 567.0,45.3 568.5,44.4 570.0,43.6 571.5,41.1 573.0,41.1 574.5,43.8 576.0,46.9 577.5,49.2 579.0,51.6 580.5,54.6 582.0,57.7 583.5,61.5 585.0,63.0 586.5,63.8 588.0,64.4 589.5,64.1 591.0,63.6 592.5,63.6 594.0,64.5 595.5,63.4 597.0,62.1 598.5,61.5 600.0,61.2 601.5,61.3 603.0,61.2 604.5,62.0 606.0,62.5 607.5,63.5 609.0,63.7 610.5,62.7 612.0,63.2 613.5,63.7 615.0,64.3 616.5,63.1 618.0,60.4 619.5,59.5 621.0,59.2 622.5,58.6 624.0,57.7 625.5,58.1 627.0,59.0 628.5,59.1 630.0,60.4 631.5,63.0 633.0,63.8 634.5,69.3 636.0,77.6 637.5,86.9 639.0,101.8 640.5,107.7 642.0,103.9 643.5,99.9 645.0,93.8 646.5,85.1 648.0,79.3 649.5,72.6 651.0,64.9 652.5,59.1 654.0,52.0 655.5,48.9 657.0,47.7 658.5,46.9 660.0,45.9 661.5,43.9 663.0,43.5 664.5,43.5 666.0,41.6 667.5,41.4 669.0,43.0 670.5,42.4 672.0,43.1 673.5,44.3 675.0,47.5 676.5,51.0 678.0,53.1 679.5,58.3 681.0,60.5 682.5,60.8 684.0,62.4 685.5,61.3 687.0,62.6 688.5,64.0 690.0,61.9 691.5,61.3 693.0,60.6 694.5,61.3 696.0,62.1 697.5,62.0 699.0,62.2 700.5,61.7 702.0,61.3 703.5,60.7 705.0,61.2 706.5,61.2 708.0,60.5 709.5,61.6 711.0,63.6 712.5,64.6 714.0,62.9 715.5,60.4 717.0,59.1 718.5,59.1 720.0,59.4 721.5,58.9 723.0,58.6 724.5,57.9 726.0,57.3 727.5,57.4 729.0,58.2 730.5,61.4 732.0,64.5 733.5,72.4 735.0,83.5 736.5,93.6 738.0,105.6 739.5,108.5 741.0,102.2 742.5,96.1 744.0,89.2 745.5,83.1 747.0,77.5 748.5,70.0\"/><polyline class=\"trace\" points=\"750.0,4.8 751.5,4.7 753.0,5.4 754.5,6.1 756.0,6.7 757.5,9.6 759.0,15.6 760.5,22.4 762.0,30.3 763.5,38.1 765.0,45.7 766.5,51.8 768.0,55.9 769.5,59.5 771.0,61.7 772.5,62.0 774.0,61.9 775.5,61.9 777.0,61.9 778.5,61.9 780.0,61.9 781.5,61.9 783.0,61.1 784.5,60.3 786.0,58.0 787.5,56.1 789.0,57.9 790.5,61.2 792.0,64.0 793.5,65.2 795.0,65.8 796.5,64.2 798.0,61.6 799.5,61.2 801.0,60.5 802.5,60.1 804.0,60.7 805.5,60.7 807.0,61.2 808.5,61.3 810.0,61.0 811.5,58.8 813.0,56.4 814.5,73.4 816.0,120.0 817.5,158.0 819.0,158.0 820.5,158.0 822.0,158.0 823.5,158.0 825.0,158.0 826.5,142.3 828.0,118.3 829.5,96.5 831.0,76.3 832.5,59.8 834.0,44.5 835.5,34.2 837.0,27.9 838.5,24.4 840.0,21.4 841.5,17.8 843.0,14.8 844.5,11.2 846.0,8.8 847.5,6.7 849.0,5.2 850.5,6.0 852.0,8.0 853.5,11.4 855.0,15.7 856.5,22.2 858.0,30.3 859.5,38.0 861.0,45.3 862.5,52.0 864.0,57.5 865.5,61.0 867.0,63.3 868.5,64.4 870.0,64.8 871.5,65.5 873.0,65.7 874.5,66.0 876.0,66.0 877.5,64.2 879.0,63.0 880.5,63.1 882.0,61.9 883.5,59.6 885.0,58.2 886.5,60.2 888.0,63.5 889.5,65.5 891.0,66.6 892.5,67.7 894.0,66.0 895.5,63.4 897.0,63.3 898.5,62.7 900.0,62.7 901.5,63.4 903.0,63.5 904.5,62.4 906.0,61.5 907.5,62.2 909.0,58.9 910.5,61.6 912.0,89.4 913.5,143.5 915.0,158.0 916.5,158.0 918.0,158.0 919.5,158.0 921.0,158.0 922.5,158.0 924.0,134.8 925.5,112.3 927.0,90.7 928.5,72.1 930.0,56.1 931.5,41.6 933.0,33.3 934.5,28.3 936.0,24.9 937.5,21.6 939.0,18.8 940.5,15.0 942.0,12.0 943.5,9.7 945.0,6.7 946.5,7.0 948.0,8.0 949.5,9.4 951.0,14.1 952.5,19.5 954.0,26.1 955.5,34.1 957.0,41.6 958.5,49.3 960.0,55.3 961.5,58.6 963.0,62.0 964.5,64.6 966.0,65.9 967.5,66.7 969.0,67.6 970.5,68.1 972.0,67.4 973.5,66.9 975.0,66.1 976.5,65.3 978.0,64.3 979.5,62.0 981.0,60.5 982.5,59.4 984.0,60.2 985.5,64.5 987.0,67.3 988.5,68.4 990.0,69.4 991.5,67.2 993.0,64.9 994.5,64.0 996.0,63.7 997.5,63.9 999.0,62.9 1000.5,62.7 1002.0,63.0 1003.5,62.5 1005.0,63.1 1006.5,60.3 1008.0,62.3 1009.5,91.0 1011.0,145.6 1012.5,158.0 1014.0,158.0 1015.5,158.0 1017.0,158.0 1018.5,158.0 1020.0,158.0 1021.5,134.6 1023.0,112.5 1024.5,91.6 1026.0,72.4 1027.5,56.7 1029.0,42.3 1030.5,33.5 1032.0,28.4 1033.5,25.2 1035.0,21.9 1036.5,18.4 1038.0,15.1 1039.5,12.0 1041.0,9.4 1042.5,7.6 1044.0,6.9 1045.5,7.6 1047.0,10.2 1048.5,14.4 1050.0,19.6 1051.5,26.1 1053.0,34.0 1054.5,42.1 1056.0,49.4 1057.5,55.2 1059.0,60.0 1060.5,63.4 1062.0,65.7 1063.5,66.9 1065.0,67.5 1066.5,68.3 1068.0,68.1 1069.5,66.8 1071.0,66.1 1072.5,65.5 1074.0,64.9 1075.5,64.4 1077.0,62.1 1078.5,60.7 1080.0,58.8 1081.5,57.9 1083.0,62.0 1084.5,64.5 1086.0,66.4 1087.5,68.4 1089.0,66.4 1090.5,64.8 1092.0,64.2 1093.5,62.8 1095.0,63.0 1096.5,63.4 1098.0,62.1 1099.5,61.9 1101.0,62.8 1102.5,63.4 1104.0,61.7 1105.5,57.5 1107.0,69.0 1108.5,110.3 1110.0,158.0 1111.5,158.0 1113.0,158.0 1114.5,158.0 1116.0,158.0 1117.5,158.0 1119.0,148.3 1120.5,122.8 1122.0,101.2 1123.5,79.7\"/><polyline class=\"trace\" points=\"1125.0,25.3 1126.5,24.0 1128.0,21.7 1129.5,19.7 1131.0,17.8 1132.5,17.2 1134.0,18.6 1135.5,21.6 1137.0,25.3 1138.5,29.8 1140.0,36.8 1141.5,43.5 1143.0,49.0 1144.5,54.5 1146.0,59.1 1147.5,62.2 1149.0,64.1 1150.5,65.4 1152.0,66.9 1153.5,67.3 1155.0,66.2 1156.5,66.3 1158.0,66.9 1159.5,66.0 1161.0,63.7 1162.5,61.8 1164.0,61.9 1165.5,62.9 1167.0,63.7 1168.5,64.1 1170.0,64.6 1171.5,65.3 1173.0,65.5 1174.5,66.2 1176.0,66.3 1177.5,67.0 1179.0,67.1 1180.5,67.6 1182.0,68.0 1183.5,67.3 1185.0,67.8 1186.5,61.9 1188.0,59.3 1189.5,66.6 1191.0,111.6 1192.5,158.0 1194.0,158.0 1195.5,158.0 1197.0,158.0 1198.5,158.0 1200.0,158.0 1201.5,158.0 1203.0,133.9 1204.5,111.0 1206.0,91.2 1207.5,77.7 1209.0,64.8 1210.5,50.6 1212.0,42.1 1213.5,39.1 1215.0,36.1 1216.5,33.4 1218.0,30.5 1219.5,28.0 1221.0,25.6 1222.5,23.1 1224.0,20.2 1225.5,18.5 1227.0,16.9 1228.5,16.6 1230.0,17.2 1231.5,18.8 1233.0,22.8 1234.5,27.2 1236.0,33.1 1237.5,38.9 1239.0,45.6 1240.5,52.0 1242.0,56.2 1243.5,59.7 1245.0,61.9 1246.5,64.4 1248.0,65.4 1249.5,65.3 1251.0,65.8 1252.5,64.6 1254.0,64.0 1255.5,65.2 1257.0,64.3 1258.5,61.6 1260.0,60.0 1261.5,60.0 1263.0,60.7 1264.5,61.6 1266.0,62.2 1267.5,63.0 1269.0,63.6 1270.5,64.2 1272.0,64.9 1273.5,65.2 1275.0,66.1 1276.5,66.1 1278.0,66.9 1279.5,66.4 1281.0,67.2 1282.5,64.9 1284.0,57.7 1285.5,58.0 1287.0,74.9 1288.5,134.7 1290.0,158.0 1291.5,158.0 1293.0,158.0 1294.5,158.0 1296.0,158.0 1297.5,158.0 1299.0,148.0 1300.5,123.5 1302.0,101.3 1303.5,84.8 1305.0,72.1 1306.5,58.1 1308.0,45.6 1309.5,39.7 1311.0,36.6 1312.5,33.6 1314.0,31.6 1315.5,28.0 1317.0,27.1 1318.5,27.7 1320.0,27.3 1321.5,27.5 1323.0,27.4 1324.5,27.4 1326.0,25.9 1327.5,23.0 1329.0,20.5 1330.5,18.3 1332.0,17.1 1333.5,16.9 1335.0,17.8 1336.5,20.2 1338.0,23.5 1339.5,28.0 1341.0,34.2 1342.5,41.3 1344.0,47.1 1345.5,52.3 1347.0,57.5 1348.5,60.7 1350.0,62.8 1351.5,63.7 1353.0,64.7 1354.5,65.1 1356.0,64.9 1357.5,65.2 1359.0,65.3 1360.5,65.4 1362.0,64.3 1363.5,62.7 1365.0,61.0 1366.5,59.9 1368.0,60.6 1369.5,61.5 1371.0,62.3 1372.5,63.4 1374.0,64.2 1375.5,64.5 1377.0,64.9 1378.5,64.9 1380.0,65.5 1381.5,65.5 1383.0,65.7 1384.5,65.6 1386.0,65.5 1387.5,65.8 1389.0,60.3 1390.5,58.8 1392.0,67.3 1393.5,114.6 1395.0,158.0 1396.5,158.0 1398.0,158.0 1399.5,158.0 1401.0,158.0 1402.5,158.0 1404.0,151.9 1405.5,125.5 1407.0,104.8 1408.5,86.8 1410.0,74.8 1411.5,61.5 1413.0,47.8 1414.5,40.5 1416.0,37.7 1417.5,34.9 1419.0,32.3 1420.5,29.6 1422.0,26.9 1423.5,24.4 1425.0,22.1 1426.5,19.2 1428.0,16.9 1429.5,16.0 1431.0,15.1 1432.5,16.3 1434.0,18.7 1435.5,21.3 1437.0,25.6 1438.5,31.5 1440.0,38.1 1441.5,44.2 1443.0,49.8 1444.5,54.7 1446.0,57.9 1447.5,59.8 1449.0,60.7 1450.5,61.3 1452.0,62.0 1453.5,62.6 1455.0,62.9 1456.5,63.3 1458.0,63.4 1459.5,61.6 1461.0,60.6 1462.5,59.1 1464.0,57.0 1465.5,58.9 1467.0,59.7 1468.5,59.7 1470.0,60.8 1471.5,60.9 1473.0,61.6 1474.5,62.4 1476.0,62.9 1477.5,63.4 1479.0,64.3 1480.5,64.0 1482.0,64.0 1483.5,63.9 1485.0,66.0 1486.5,62.8 1488.0,56.7 1489.5,57.1 1491.0,80.0 1492.5,144.4 1494.0,158.0 1495.5,158.0 1497.0,158.0 1498.5,158.0\"/><polyline class=\"trace\" points=\"0.0,178.7 1.5,178.6 3.0,177.0 4.5,175.2 6.0,172.3 7.5,170.8 9.0,168.9 10.5,166.1 12.0,164.4 13.5,162.7 15.0,161.8 16.5,161.6 18.0,161.5 19.5,163.0 21.0,165.1 22.5,165.6 24.0,167.3 25.5,167.7 27.0,168.1 28.5,169.0 30.0,167.5 31.5,167.4 33.0,168.0 34.5,168.4 36.0,168.1 37.5,165.4 39.0,164.2 40.5,166.1 42.0,165.7 43.5,165.2 45.0,166.4 46.5,167.7 48.0,169.8 49.5,171.1 51.0,171.9 52.5,172.7 54.0,173.0 55.5,173.7 57.0,174.1 58.5,173.8 60.0,173.7 61.5,171.9 63.0,170.1 64.5,164.1 66.0,156.2 67.5,156.6 69.0,156.8 70.5,152.7 72.0,154.8 73.5,164.4 75.0,172.4 76.5,177.2 78.0,181.9 79.5,182.5 81.0,181.8 82.5,183.0 84.0,182.4 85.5,180.1 87.0,179.5 88.5,179.4 90.0,179.1 91.5,178.9 93.0,178.5 94.5,179.1 96.0,178.9 97.5,178.3 99.0,177.6 100.5,176.3 102.0,175.2 103.5,172.6 105.0,169.6 106.5,167.3 108.0,165.4 109.5,164.2 111.0,163.1 112.5,162.7 114.0,162.1 115.5,162.0 117.0,162.9 118.5,164.4 120.0,166.7 121.5,167.2 123.0,167.7 124.5,169.0 126.0,169.9 127.5,170.7 129.0,169.5 130.5,168.6 132.0,167.9 133.5,166.0 135.0,164.9 136.5,164.1 138.0,164.1 139.5,164.7 141.0,164.8 142.5,165.6 144.0,168.6 145.5,170.8 147.0,170.1 148.5,171.0 150.0,172.5 151.5,172.8 153.0,173.7 154.5,172.8 156.0,172.3 157.5,173.6 159.0,171.6 160.5,168.2 162.0,160.3 163.5,157.8 165.0,160.5 166.5,155.7 168.0,151.2 169.5,157.2 171.0,168.6 172.5,174.3 174.0,178.8 175.5,181.5 177.0,182.3 178.5,182.5 180.0,183.4 181.5,184.0 183.0,180.3 184.5,179.1 186.0,178.8 187.5,178.5 189.0,178.6 190.5,177.9 192.0,178.2 193.5,177.4 195.0,178.2 196.5,179.1 198.0,176.9 199.5,174.6 201.0,171.2 202.5,169.2 204.0,168.3 205.5,166.3 207.0,164.7 208.5,163.3 210.0,163.8 211.5,164.4 213.0,164.8 214.5,166.2 216.0,167.2 217.5,168.1 219.0,168.6 220.5,169.4 222.0,169.8 223.5,170.7 225.0,170.9 226.5,171.1 228.0,171.4 229.5,169.4 231.0,168.1 232.5,166.0 234.0,165.2 235.5,166.2 237.0,166.5 238.5,167.1 240.0,168.3 241.5,170.0 243.0,172.4 244.5,174.0 246.0,174.1 247.5,176.2 249.0,176.7 250.5,175.8 252.0,175.6 253.5,174.9 255.0,173.8 256.5,171.2 258.0,170.1 259.5,161.7 261.0,157.2 262.5,162.0 264.0,157.1 265.5,153.8 267.0,160.2 268.5,168.9 270.0,174.3 271.5,178.6 273.0,183.0 274.5,184.0 276.0,184.3 277.5,183.6 279.0,183.6 280.5,181.8 282.0,180.3 283.5,180.4 285.0,180.1 286.5,181.5 288.0,180.5 289.5,179.7 291.0,181.4 292.5,179.7 294.0,177.3 295.5,177.1 297.0,175.6 298.5,174.1 300.0,170.5 301.5,168.1 303.0,167.4 304.5,163.8 306.0,163.8 307.5,165.2 309.0,165.0 310.5,167.4 312.0,167.3 313.5,166.9 315.0,169.0 316.5,169.8 318.0,170.7 319.5,170.3 321.0,169.7 322.5,170.0 324.0,169.9 325.5,170.2 327.0,170.2 328.5,170.3 330.0,169.0 331.5,167.5 333.0,169.1 334.5,168.6 336.0,166.2 337.5,167.1 339.0,169.1 340.5,171.1 342.0,172.5 343.5,173.3 345.0,174.2 346.5,174.9 348.0,174.5 349.5,175.2 351.0,175.1 352.5,175.6 354.0,176.1 355.5,172.0 357.0,166.8 358.5,158.9 360.0,157.5 361.5,160.2 363.0,154.6 364.5,153.8 366.0,162.7 367.5,171.6 369.0,177.4 370.5,180.6 372.0,181.6 373.5,182.1\"/><polyline class=\"trace\" points=\"375.0,191.2 376.5,196.2 378.0,197.7 379.5,197.1 381.0,197.2 382.5,196.8 384.0,194.4 385.5,191.5 387.0,187.7 388.5,184.0 390.0,180.8 391.5,177.4 393.0,174.7 394.5,172.3 396.0,171.4 397.5,170.7 399.0,169.1 400.5,168.2 402.0,166.3 403.5,169.2 405.0,171.3 406.5,170.3 408.0,170.0 409.5,169.9 411.0,170.8 412.5,169.8 414.0,171.9 415.5,172.2 417.0,170.8 418.5,169.9 420.0,168.0 421.5,169.6 423.0,169.0 424.5,166.8 426.0,167.4 427.5,168.9 429.0,168.6 430.5,168.0 432.0,166.5 433.5,167.0 435.0,167.4 436.5,164.4 438.0,165.7 439.5,168.3 441.0,161.5 442.5,140.4 444.0,117.0 445.5,103.1 447.0,99.4 448.5,98.5 450.0,97.0 451.5,104.1 453.0,113.9 454.5,122.7 456.0,135.9 457.5,151.6 459.0,164.1 460.5,174.0 462.0,181.7 463.5,182.8 465.0,185.0 466.5,187.3 468.0,187.9 469.5,192.4 471.0,193.8 472.5,194.7 474.0,197.7 475.5,197.7 477.0,197.5 478.5,197.5 480.0,195.7 481.5,194.1 483.0,191.6 484.5,186.9 486.0,183.0 487.5,180.5 489.0,176.5 490.5,172.9 492.0,171.0 493.5,169.8 495.0,170.2 496.5,169.4 498.0,166.3 499.5,165.5 501.0,167.7 502.5,170.4 504.0,170.9 505.5,169.0 507.0,169.3 508.5,170.2 510.0,171.4 511.5,174.4 513.0,173.3 514.5,172.2 516.0,170.0 517.5,165.2 519.0,168.9 520.5,171.8 522.0,168.4 523.5,168.2 525.0,167.8 526.5,167.1 528.0,168.6 529.5,170.1 531.0,169.6 532.5,167.2 534.0,165.7 535.5,166.3 537.0,166.8 538.5,157.8 540.0,133.6 541.5,108.6 543.0,99.9 544.5,100.2 546.0,95.2 547.5,98.8 549.0,109.5 550.5,114.0 552.0,127.4 553.5,141.9 555.0,152.7 556.5,168.3 558.0,177.6 559.5,182.2 561.0,185.1 562.5,185.1 564.0,187.0 565.5,188.7 567.0,190.8 568.5,193.8 570.0,194.2 571.5,197.8 573.0,201.1 574.5,199.3 576.0,198.0 577.5,196.5 579.0,193.0 580.5,189.9 582.0,186.1 583.5,180.8 585.0,177.1 586.5,174.5 588.0,172.5 589.5,171.3 591.0,170.8 592.5,169.3 594.0,166.9 595.5,167.8 597.0,169.9 598.5,169.8 600.0,169.9 601.5,169.3 603.0,169.2 604.5,170.6 606.0,171.5 607.5,172.8 609.0,173.5 610.5,174.0 612.0,172.5 613.5,170.7 615.0,167.7 616.5,167.5 618.0,169.1 619.5,168.6 621.0,169.0 622.5,167.0 624.0,168.3 625.5,168.7 627.0,167.2 628.5,168.0 630.0,167.1 631.5,166.0 633.0,166.0 634.5,167.4 636.0,157.7 637.5,131.9 639.0,109.5 640.5,102.6 642.0,100.7 643.5,95.5 645.0,99.4 646.5,110.5 648.0,115.5 649.5,127.3 651.0,142.4 652.5,155.1 654.0,169.2 655.5,178.1 657.0,182.8 658.5,184.2 660.0,186.6 661.5,188.5 663.0,190.8 664.5,192.1 666.0,193.4 667.5,196.4 669.0,196.6 670.5,198.3 672.0,199.0 673.5,198.9 675.0,197.8 676.5,194.7 678.0,191.5 679.5,186.5 681.0,181.9 682.5,179.3 684.0,176.4 685.5,175.1 687.0,172.6 688.5,170.4 690.0,171.4 691.5,171.3 693.0,171.4 694.5,170.7 696.0,170.0 697.5,169.6 699.0,169.3 700.5,169.9 702.0,170.8 703.5,171.8 705.0,172.8 706.5,175.2 708.0,174.0 709.5,172.6 711.0,172.0 712.5,169.0 714.0,169.3 715.5,171.3 717.0,171.7 718.5,170.6 720.0,168.5 721.5,168.4 723.0,169.7 724.5,170.1 726.0,171.4 727.5,170.5 729.0,168.1 730.5,167.8 732.0,169.6 733.5,165.5 735.0,145.5 736.5,121.3 738.0,105.7 739.5,100.8 741.0,100.2 742.5,99.0 744.0,104.1 745.5,111.6 747.0,121.0 748.5,135.4\"/><polyline class=\"trace\" points=\"750.0,74.0 751.5,74.0 753.0,74.0 754.5,74.0 756.0,74.0 757.5,74.0 759.0,80.4 760.5,92.5 762.0,107.2 763.5,121.0 765.0,135.5 766.5,147.4 768.0,156.3 769.5,162.6 771.0,166.6 772.5,169.1 774.0,169.0 775.5,169.5 777.0,169.9 778.5,170.1 780.0,170.4 781.5,169.9 783.0,168.9 784.5,168.0 786.0,165.2 787.5,162.4 789.0,164.2 790.5,167.7 792.0,169.9 793.5,170.2 795.0,170.1 796.5,170.4 798.0,170.0 799.5,170.6 801.0,169.6 802.5,169.8 804.0,170.1 805.5,170.5 807.0,171.3 808.5,170.9 810.0,172.0 811.5,157.9 813.0,168.6 814.5,253.9 816.0,266.0 817.5,266.0 819.0,266.0 820.5,266.0 822.0,266.0 823.5,266.0 825.0,266.0 826.5,266.0 828.0,261.4 829.5,218.4 831.0,182.1 832.5,155.8 834.0,133.2 835.5,114.5 837.0,103.1 838.5,96.6 840.0,89.9 841.5,83.2 843.0,77.1 844.5,74.0 846.0,74.0 847.5,74.0 849.0,74.0 850.5,74.0 852.0,74.0 853.5,74.0 855.0,78.9 856.5,89.9 858.0,104.0 859.5,118.3 861.0,132.1 862.5,144.9 864.0,155.1 865.5,163.1 867.0,167.2 868.5,169.4 870.0,171.1 871.5,171.6 873.0,171.9 874.5,172.0 876.0,172.6 877.5,170.8 879.0,170.0 880.5,169.9 882.0,168.0 883.5,165.3 885.0,162.8 886.5,165.2 888.0,168.9 889.5,170.5 891.0,170.8 892.5,171.0 894.0,171.2 895.5,171.3 897.0,171.6 898.5,171.5 900.0,172.3 901.5,171.7 903.0,172.9 904.5,172.0 906.0,173.5 907.5,168.7 909.0,154.6 910.5,191.5 912.0,266.0 913.5,266.0 915.0,266.0 916.5,266.0 918.0,266.0 919.5,266.0 921.0,266.0 922.5,266.0 924.0,266.0 925.5,245.4 927.0,203.9 928.5,171.9 930.0,147.6 931.5,125.5 933.0,109.9 934.5,100.9 936.0,94.1 937.5,87.7 939.0,81.6 940.5,74.9 942.0,74.0 943.5,74.0 945.0,74.0 946.5,74.0 948.0,74.0 949.5,74.0 951.0,74.0 952.5,82.7 954.0,95.3 955.5,109.9 957.0,123.6 958.5,137.5 960.0,149.7 961.5,158.9 963.0,164.8 964.5,168.4 966.0,171.1 967.5,171.9 969.0,172.2 970.5,172.5 972.0,172.6 973.5,173.1 975.0,172.3 976.5,171.0 978.0,169.6 979.5,167.8 981.0,165.3 982.5,164.1 984.0,166.9 985.5,170.0 987.0,171.1 988.5,172.6 990.0,173.5 991.5,173.8 993.0,173.4 994.5,172.2 996.0,172.3 997.5,173.2 999.0,173.0 1000.5,174.3 1002.0,173.6 1003.5,175.5 1005.0,170.0 1006.5,156.6 1008.0,193.8 1009.5,266.0 1011.0,266.0 1012.5,266.0 1014.0,266.0 1015.5,266.0 1017.0,266.0 1018.5,266.0 1020.0,266.0 1021.5,266.0 1023.0,246.4 1024.5,205.9 1026.0,174.0 1027.5,150.3 1029.0,128.2 1030.5,112.2 1032.0,103.3 1033.5,97.2 1035.0,90.7 1036.5,84.3 1038.0,78.2 1039.5,74.0 1041.0,74.0 1042.5,74.0 1044.0,74.0 1045.5,74.0 1047.0,74.0 1048.5,77.5 1050.0,86.8 1051.5,98.2 1053.0,111.8 1054.5,126.0 1056.0,139.6 1057.5,150.9 1059.0,160.5 1060.5,167.0 1062.0,171.0 1063.5,173.1 1065.0,173.0 1066.5,172.9 1068.0,173.1 1069.5,172.9 1071.0,173.1 1072.5,172.9 1074.0,172.8 1075.5,171.4 1077.0,169.6 1078.5,168.3 1080.0,166.0 1081.5,167.4 1083.0,169.5 1084.5,170.7 1086.0,173.4 1087.5,174.6 1089.0,175.2 1090.5,174.0 1092.0,173.8 1093.5,173.9 1095.0,174.1 1096.5,174.3 1098.0,174.0 1099.5,175.5 1101.0,175.2 1102.5,176.6 1104.0,162.9 1105.5,162.4 1107.0,232.1 1108.5,266.0 1110.0,266.0 1111.5,266.0 1113.0,266.0 1114.5,266.0 1116.0,266.0 1117.5,266.0 1119.0,266.0 1120.5,266.0 1122.0,229.6 1123.5,191.5\"/><polyline class=\"trace\" points=\"1125.0,217.2 1126.5,218.7 1128.0,218.4 1129.5,216.1 1131.0,212.8 1132.5,207.7 1134.0,201.2 1135.5,193.6 1137.0,185.2 1138.5,177.2 1140.0,170.4 1141.5,164.9 1143.0,162.0 1144.5,161.8 1146.0,163.0 1147.5,164.3 1149.0,165.5 1150.5,166.5 1152.0,167.4 1153.5,168.5 1155.0,169.6 1156.5,170.8 1158.0,171.7 1159.5,172.3 1161.0,173.1 1162.5,173.3 1164.0,173.1 1165.5,173.6 1167.0,174.4 1168.5,174.3 1170.0,174.0 1171.5,174.0 1173.0,173.4 1174.5,173.8 1176.0,174.9 1177.5,174.4 1179.0,173.7 1180.5,173.2 1182.0,172.8 1183.5,172.6 1185.0,171.6 1186.5,168.9 1188.0,168.7 1189.5,163.5 1191.0,148.3 1192.5,125.6 1194.0,93.7 1195.5,78.8 1197.0,86.6 1198.5,93.4 1200.0,91.3 1201.5,90.4 1203.0,99.0 1204.5,122.5 1206.0,156.7 1207.5,184.8 1209.0,201.4 1210.5,204.2 1212.0,203.5 1213.5,203.6 1215.0,203.6 1216.5,205.6 1218.0,207.6 1219.5,210.1 1221.0,212.6 1222.5,213.4 1224.0,212.7 1225.5,212.2 1227.0,209.5 1228.5,205.0 1230.0,199.0 1231.5,191.1 1233.0,183.3 1234.5,175.0 1236.0,167.5 1237.5,161.5 1239.0,158.5 1240.5,157.6 1242.0,157.9 1243.5,159.9 1245.0,160.9 1246.5,162.5 1248.0,164.5 1249.5,165.1 1251.0,166.2 1252.5,166.5 1254.0,166.8 1255.5,167.1 1257.0,167.5 1258.5,167.8 1260.0,168.2 1261.5,168.7 1263.0,169.0 1264.5,169.6 1266.0,169.9 1267.5,170.2 1269.0,170.2 1270.5,170.1 1272.0,170.5 1273.5,170.2 1275.0,169.8 1276.5,169.0 1278.0,168.7 1279.5,167.6 1281.0,167.3 1282.5,167.7 1284.0,165.3 1285.5,165.3 1287.0,155.3 1288.5,137.4 1290.0,111.4 1291.5,81.8 1293.0,78.1 1294.5,87.5 1296.0,90.4 1297.5,87.8 1299.0,88.9 1300.5,103.0 1302.0,132.6 1303.5,166.0 1305.0,190.9 1306.5,201.3 1308.0,201.3 1309.5,201.9 1311.0,201.0 1312.5,202.3 1314.0,205.3 1315.5,206.8 1317.0,209.9 1318.5,211.8 1320.0,212.1 1321.5,211.5 1323.0,210.0 1324.5,207.6 1326.0,202.2 1327.5,195.3 1329.0,187.8 1330.5,179.8 1332.0,171.5 1333.5,165.0 1335.0,161.0 1336.5,157.5 1338.0,157.3 1339.5,158.5 1341.0,159.8 1342.5,162.1 1344.0,162.9 1345.5,163.9 1347.0,165.6 1348.5,166.4 1350.0,167.0 1351.5,168.0 1353.0,168.3 1354.5,168.6 1356.0,168.9 1357.5,169.1 1359.0,169.4 1360.5,169.6 1362.0,170.0 1363.5,170.2 1365.0,170.5 1366.5,170.8 1368.0,170.5 1369.5,170.2 1371.0,171.1 1372.5,171.9 1374.0,171.2 1375.5,171.2 1377.0,170.8 1378.5,170.5 1380.0,170.4 1381.5,168.0 1383.0,167.1 1384.5,156.8 1386.0,138.6 1387.5,112.5 1389.0,83.1 1390.5,79.1 1392.0,87.7 1393.5,89.4 1395.0,87.1 1396.5,87.8 1398.0,101.2 1399.5,132.2 1401.0,166.1 1402.5,192.0 1404.0,203.5 1405.5,201.7 1407.0,202.5 1408.5,204.3 1410.0,206.2 1411.5,208.3 1413.0,210.1 1414.5,213.0 1416.0,215.0 1417.5,215.7 1419.0,214.8 1420.5,214.0 1422.0,211.2 1423.5,205.8 1425.0,198.7 1426.5,190.7 1428.0,183.0 1429.5,174.6 1431.0,168.1 1432.5,163.6 1434.0,160.3 1435.5,160.2 1437.0,162.3 1438.5,162.7 1440.0,163.0 1441.5,166.0 1443.0,167.4 1444.5,167.3 1446.0,168.3 1447.5,169.2 1449.0,169.9 1450.5,170.8 1452.0,171.0 1453.5,171.4 1455.0,172.5 1456.5,172.2 1458.0,172.6 1459.5,173.0 1461.0,172.6 1462.5,172.5 1464.0,172.3 1465.5,172.0 1467.0,172.3 1468.5,173.2 1470.0,173.5 1471.5,173.5 1473.0,173.1 1474.5,173.2 1476.0,172.6 1477.5,172.8 1479.0,170.7 1480.5,169.0 1482.0,164.4 1483.5,149.0 1485.0,129.9 1486.5,99.5 1488.0,78.4 1489.5,82.8 1491.0,89.0 1492.5,88.2 1494.0,85.8 1495.5,92.4 1497.0,114.0 1498.5,146.7\"/><polyline class=\"trace\" points=\"0.0,261.8 1.5,256.8 3.0,254.5 4.5,254.2 6.0,252.7 7.5,252.4 9.0,253.8 10.5,255.3 12.0,258.2 13.5,261.1 15.0,263.8 16.5,267.1 18.0,269.8 19.5,273.0 21.0,274.9 22.5,275.9 24.0,278.3 25.5,279.4 27.0,281.5 28.5,279.0 30.0,276.1 31.5,277.2 33.0,277.8 34.5,278.0 36.0,277.0 37.5,276.7 39.0,273.9 40.5,274.6 42.0,275.8 43.5,276.4 45.0,278.9 46.5,277.9 48.0,279.6 49.5,282.4 51.0,282.2 52.5,281.2 54.0,281.5 55.5,282.5 57.0,284.2 58.5,283.6 60.0,283.2 61.5,285.4 63.0,283.1 64.5,277.5 66.0,280.3 67.5,301.6 69.0,325.1 70.5,337.0 72.0,341.7 73.5,347.5 75.0,352.9 76.5,348.2 78.0,340.8 79.5,332.3 81.0,318.7 82.5,303.6 84.0,290.8 85.5,279.7 87.0,271.8 88.5,270.6 90.0,268.2 91.5,265.8 93.0,265.0 94.5,260.9 96.0,259.3 97.5,258.2 99.0,254.8 100.5,254.2 102.0,253.9 103.5,252.6 105.0,252.9 106.5,253.3 108.0,254.8 109.5,259.0 111.0,262.3 112.5,264.6 114.0,268.3 115.5,271.8 117.0,274.2 118.5,276.1 120.0,276.9 121.5,278.0 123.0,281.3 124.5,282.7 126.0,280.9 127.5,278.7 129.0,277.6 130.5,279.0 132.0,278.4 133.5,276.6 135.0,274.8 136.5,271.4 138.0,272.5 139.5,273.9 141.0,276.1 142.5,281.4 144.0,279.1 145.5,277.3 147.0,280.4 148.5,281.1 150.0,282.1 151.5,283.0 153.0,282.0 154.5,280.0 156.0,280.3 157.5,283.3 159.0,283.9 160.5,281.5 162.0,277.1 163.5,284.8 165.0,310.4 166.5,333.0 168.0,339.4 169.5,342.1 171.0,352.8 172.5,352.1 174.0,343.6 175.5,340.5 177.0,327.5 178.5,313.1 180.0,302.7 181.5,287.4 183.0,276.2 184.5,271.0 186.0,268.0 187.5,267.8 189.0,265.9 190.5,263.9 192.0,262.0 193.5,258.6 195.0,258.6 196.5,255.4 198.0,251.0 199.5,251.8 201.0,251.3 202.5,251.8 204.0,254.9 205.5,257.0 207.0,260.0 208.5,264.6 210.0,268.5 211.5,271.4 213.0,273.6 214.5,275.6 216.0,276.6 217.5,278.5 219.0,281.1 220.5,280.6 222.0,278.8 223.5,279.3 225.0,279.3 226.5,279.9 228.0,280.2 229.5,277.9 231.0,276.3 232.5,274.0 234.0,272.8 235.5,272.8 237.0,274.5 238.5,276.6 240.0,280.2 241.5,281.2 243.0,280.8 244.5,282.1 246.0,281.8 247.5,284.8 249.0,283.7 250.5,282.9 252.0,284.3 253.5,283.1 255.0,283.5 256.5,283.3 258.0,282.7 259.5,277.2 261.0,284.6 262.5,312.8 264.0,332.8 265.5,338.1 267.0,343.1 268.5,352.7 270.0,351.5 271.5,342.5 273.0,339.8 274.5,328.5 276.0,313.5 277.5,300.4 279.0,286.3 280.5,276.4 282.0,271.0 283.5,269.7 285.0,267.2 286.5,266.0 288.0,263.1 289.5,261.5 291.0,261.0 292.5,257.1 294.0,255.7 295.5,253.9 297.0,252.5 298.5,251.8 300.0,251.2 301.5,253.0 303.0,255.9 304.5,259.1 306.0,263.7 307.5,267.0 309.0,269.8 310.5,272.4 312.0,274.8 313.5,276.8 315.0,276.9 316.5,277.3 318.0,277.7 319.5,278.2 321.0,278.5 322.5,279.1 324.0,279.4 325.5,279.0 327.0,278.1 328.5,277.1 330.0,275.4 331.5,272.4 333.0,274.2 334.5,275.4 336.0,274.8 337.5,278.3 339.0,279.0 340.5,278.0 342.0,278.2 343.5,279.7 345.0,282.3 346.5,282.7 348.0,281.3 349.5,281.2 351.0,279.9 352.5,281.0 354.0,283.6 355.5,282.0 357.0,277.6 358.5,277.7 360.0,297.0 361.5,322.6 363.0,335.4 364.5,339.8 366.0,344.9 367.5,350.5 369.0,348.3 370.5,342.4 372.0,333.5 373.5,319.3\"/><polyline class=\"trace\" points=\"375.0,274.6 376.5,272.1 378.0,270.1 379.5,269.1 381.0,266.9 382.5,266.0 384.0,265.7 385.5,265.1 387.0,265.7 388.5,266.3 390.0,267.1 391.5,268.7 393.0,270.0 394.5,272.4 396.0,274.4 397.5,275.2 399.0,277.2 400.5,277.9 402.0,279.1 403.5,278.4 405.0,276.2 406.5,276.6 408.0,277.2 409.5,277.6 411.0,276.9 412.5,275.4 414.0,273.4 415.5,274.8 417.0,275.2 418.5,275.2 420.0,277.0 421.5,277.2 423.0,279.1 424.5,281.1 426.0,281.4 427.5,281.4 429.0,281.7 430.5,282.4 432.0,283.5 433.5,283.0 435.0,282.7 436.5,283.0 438.0,280.9 439.5,275.2 441.0,272.7 442.5,283.5 444.0,295.3 445.5,299.2 447.0,302.6 448.5,310.3 450.0,317.0 451.5,317.1 453.0,315.7 454.5,311.7 456.0,304.6 457.5,297.7 459.0,291.0 460.5,284.2 462.0,280.0 463.5,279.4 465.0,278.0 466.5,276.7 468.0,276.1 469.5,274.3 471.0,273.5 472.5,272.7 474.0,270.6 475.5,269.6 477.0,268.9 478.5,267.0 480.0,265.6 481.5,264.7 483.0,264.5 484.5,266.0 486.0,267.1 487.5,268.0 489.0,269.6 490.5,271.2 492.0,272.9 493.5,274.6 495.0,276.1 496.5,277.0 498.0,278.8 499.5,280.2 501.0,279.8 502.5,279.0 504.0,277.9 505.5,278.2 507.0,277.5 508.5,275.6 510.0,274.2 511.5,272.1 513.0,272.7 514.5,273.7 516.0,274.9 517.5,277.9 519.0,278.3 520.5,278.5 522.0,279.6 523.5,280.4 525.0,281.7 526.5,282.3 528.0,282.1 529.5,280.8 531.0,280.6 532.5,282.8 534.0,282.1 535.5,279.3 537.0,273.1 538.5,275.7 540.0,289.8 541.5,298.7 543.0,299.7 544.5,304.0 546.0,315.1 547.5,317.5 549.0,315.5 550.5,315.3 552.0,309.2 553.5,302.1 555.0,297.4 556.5,290.1 558.0,282.6 559.5,279.4 561.0,277.8 562.5,277.5 564.0,276.6 565.5,275.3 567.0,274.5 568.5,272.4 570.0,272.8 571.5,271.6 573.0,268.3 574.5,267.6 576.0,265.6 577.5,264.9 579.0,266.0 580.5,266.1 582.0,266.7 583.5,268.3 585.0,270.5 586.5,272.2 588.0,273.6 589.5,275.2 591.0,276.3 592.5,277.7 594.0,279.2 595.5,279.4 597.0,278.6 598.5,279.3 600.0,279.5 601.5,279.9 603.0,280.2 604.5,278.0 606.0,276.6 607.5,274.3 609.0,273.3 610.5,273.9 612.0,274.8 613.5,276.3 615.0,278.6 616.5,280.0 618.0,281.0 619.5,282.4 621.0,282.3 622.5,284.9 624.0,284.5 625.5,283.7 627.0,284.2 628.5,283.3 630.0,283.0 631.5,281.6 633.0,280.8 634.5,273.8 636.0,275.2 637.5,291.7 639.0,299.3 640.5,300.3 642.0,306.0 643.5,315.1 645.0,317.2 646.5,314.9 648.0,315.7 649.5,310.6 651.0,303.2 652.5,296.4 654.0,289.3 655.5,283.5 657.0,280.0 658.5,279.4 660.0,278.0 661.5,278.1 663.0,276.2 664.5,275.0 666.0,275.5 667.5,272.8 669.0,270.9 670.5,269.9 672.0,268.4 673.5,267.3 675.0,265.3 676.5,264.9 678.0,266.0 679.5,265.8 681.0,268.2 682.5,270.5 684.0,271.8 685.5,274.3 687.0,275.4 688.5,276.2 690.0,277.3 691.5,277.9 693.0,278.6 694.5,278.6 696.0,278.5 697.5,278.9 699.0,279.0 700.5,279.0 702.0,278.5 703.5,278.1 705.0,276.6 706.5,274.3 708.0,276.1 709.5,276.3 711.0,274.9 712.5,277.1 714.0,278.4 715.5,279.0 717.0,279.7 718.5,280.9 720.0,282.6 721.5,283.2 723.0,282.2 724.5,282.6 726.0,281.8 727.5,282.6 729.0,284.2 730.5,281.4 732.0,276.6 733.5,272.7 735.0,281.6 736.5,295.7 738.0,299.3 739.5,301.2 741.0,308.1 742.5,315.3 744.0,317.2 745.5,315.8 747.0,311.9 748.5,305.0\"/><polyline class=\"trace\" points=\"750.0,193.2 751.5,191.0 753.0,188.1 754.5,186.2 756.0,186.3 757.5,189.4 759.0,194.8 760.5,203.0 762.0,213.2 763.5,224.4 765.0,236.3 766.5,246.5 768.0,255.9 769.5,263.3 771.0,268.3 772.5,271.4 774.0,273.3 775.5,274.7 777.0,274.9 778.5,275.4 780.0,275.5 781.5,276.1 783.0,275.8 784.5,273.9 786.0,271.6 787.5,269.3 789.0,269.9 790.5,271.8 792.0,272.8 793.5,273.8 795.0,274.4 796.5,275.1 798.0,275.5 799.5,276.5 801.0,277.1 802.5,278.2 804.0,278.5 805.5,279.1 807.0,279.5 808.5,279.6 810.0,280.3 811.5,269.8 813.0,272.5 814.5,316.7 816.0,374.0 817.5,374.0 819.0,374.0 820.5,374.0 822.0,374.0 823.5,374.0 825.0,374.0 826.5,374.0 828.0,374.0 829.5,338.7 831.0,306.6 832.5,284.5 834.0,265.4 835.5,247.3 837.0,235.6 838.5,229.8 840.0,223.6 841.5,217.8 843.0,211.9 844.5,205.8 846.0,200.6 847.5,196.0 849.0,192.0 850.5,190.0 852.0,189.9 853.5,192.1 855.0,197.1 856.5,204.3 858.0,214.2 859.5,225.0 861.0,236.3 862.5,246.3 864.0,256.5 865.5,265.7 867.0,270.4 868.5,273.2 870.0,275.5 871.5,277.8 873.0,279.0 874.5,278.8 876.0,279.0 877.5,278.4 879.0,278.1 880.5,278.8 882.0,277.5 883.5,274.8 885.0,273.0 886.5,273.9 888.0,276.3 889.5,278.0 891.0,279.1 892.5,280.2 894.0,281.1 895.5,282.1 897.0,283.2 898.5,283.5 900.0,284.0 901.5,283.6 903.0,284.5 904.5,283.8 906.0,285.0 907.5,281.6 909.0,270.6 910.5,286.6 912.0,347.4 913.5,374.0 915.0,374.0 916.5,374.0 918.0,374.0 919.5,374.0 921.0,374.0 922.5,374.0 924.0,374.0 925.5,363.4 927.0,325.6 928.5,297.7 930.0,278.1 931.5,258.6 933.0,242.4 934.5,233.8 936.0,227.7 937.5,222.0 939.0,216.6 940.5,210.2 942.0,205.1 943.5,199.9 945.0,195.3 946.5,192.2 948.0,190.3 949.5,191.2 951.0,194.2 952.5,200.4 954.0,208.3 955.5,218.1 957.0,229.3 958.5,240.9 960.0,252.6 961.5,260.5 963.0,268.0 964.5,273.6 966.0,275.7 967.5,278.4 969.0,279.2 970.5,279.2 972.0,279.5 973.5,279.6 975.0,279.8 976.5,279.7 978.0,278.9 979.5,277.3 981.0,275.8 982.5,274.9 984.0,276.2 985.5,278.1 987.0,278.8 988.5,280.2 990.0,281.6 991.5,282.1 993.0,282.9 994.5,283.7 996.0,285.1 997.5,286.5 999.0,285.3 1000.5,286.0 1002.0,285.7 1003.5,286.9 1005.0,283.2 1006.5,272.5 1008.0,288.5 1009.5,348.9 1011.0,374.0 1012.5,374.0 1014.0,374.0 1015.5,374.0 1017.0,374.0 1018.5,374.0 1020.0,374.0 1021.5,374.0 1023.0,364.3 1024.5,328.2 1026.0,300.7 1027.5,281.5 1029.0,262.5 1030.5,246.0 1032.0,237.6 1033.5,232.2 1035.0,226.6 1036.5,220.6 1038.0,214.3 1039.5,208.9 1041.0,204.0 1042.5,200.1 1044.0,196.9 1045.5,196.4 1047.0,197.7 1048.5,199.5 1050.0,204.7 1051.5,212.2 1053.0,221.8 1054.5,232.8 1056.0,244.2 1057.5,255.1 1059.0,264.3 1060.5,271.5 1062.0,276.3 1063.5,278.5 1065.0,280.8 1066.5,282.7 1068.0,283.8 1069.5,284.2 1071.0,283.4 1072.5,283.5 1074.0,283.3 1075.5,282.2 1077.0,281.0 1078.5,279.9 1080.0,277.7 1081.5,276.5 1083.0,279.6 1084.5,281.8 1086.0,282.7 1087.5,283.5 1089.0,284.2 1090.5,284.7 1092.0,285.5 1093.5,286.0 1095.0,286.2 1096.5,286.0 1098.0,285.9 1099.5,286.4 1101.0,285.4 1102.5,287.2 1104.0,278.1 1105.5,273.9 1107.0,306.9 1108.5,374.0 1110.0,374.0 1111.5,374.0 1113.0,374.0 1114.5,374.0 1116.0,374.0 1117.5,374.0 1119.0,374.0 1120.5,374.0 1122.0,351.4 1123.5,318.0\"/><polyline class=\"trace\" points=\"1125.0,328.8 1126.5,330.7 1128.0,331.5 1129.5,329.4 1131.0,326.5 1132.5,322.4 1134.0,316.2 1135.5,309.4 1137.0,301.5 1138.5,293.5 1140.0,286.5 1141.5,282.0 1143.0,279.8 1144.5,278.0 1146.0,278.1 1147.5,280.4 1149.0,282.1 1150.5,284.1 1152.0,285.9 1153.5,286.6 1155.0,287.5 1156.5,287.7 1158.0,289.1 1159.5,290.1 1161.0,289.8 1162.5,290.0 1164.0,289.9 1165.5,290.0 1167.0,289.7 1168.5,289.5 1170.0,289.1 1171.5,289.0 1173.0,288.5 1174.5,288.7 1176.0,289.7 1177.5,288.9 1179.0,288.1 1180.5,287.6 1182.0,287.4 1183.5,286.9 1185.0,286.2 1186.5,284.1 1188.0,283.0 1189.5,278.0 1191.0,261.7 1192.5,238.6 1194.0,206.2 1195.5,188.4 1197.0,192.9 1198.5,194.1 1200.0,193.5 1201.5,197.0 1203.0,206.9 1204.5,233.4 1206.0,269.7 1207.5,299.5 1209.0,317.6 1210.5,318.9 1212.0,315.9 1213.5,317.7 1215.0,319.3 1216.5,321.2 1218.0,323.8 1219.5,326.5 1221.0,329.4 1222.5,331.4 1224.0,330.9 1225.5,330.3 1227.0,328.2 1228.5,324.0 1230.0,318.0 1231.5,310.4 1233.0,302.8 1234.5,294.4 1236.0,286.6 1237.5,280.5 1239.0,277.8 1240.5,277.2 1242.0,277.3 1243.5,278.3 1245.0,278.5 1246.5,280.5 1248.0,282.3 1249.5,283.2 1251.0,284.2 1252.5,284.2 1254.0,285.6 1255.5,285.7 1257.0,285.3 1258.5,285.3 1260.0,284.9 1261.5,284.8 1263.0,284.6 1264.5,284.5 1266.0,284.3 1267.5,284.1 1269.0,284.0 1270.5,283.8 1272.0,283.5 1273.5,282.9 1275.0,282.6 1276.5,282.1 1278.0,281.8 1279.5,281.7 1281.0,281.5 1282.5,280.5 1284.0,277.3 1285.5,276.3 1287.0,266.3 1288.5,246.5 1290.0,220.2 1291.5,189.3 1293.0,182.0 1294.5,185.2 1296.0,184.8 1297.5,186.7 1299.0,190.6 1300.5,205.6 1302.0,237.8 1303.5,272.7 1305.0,299.1 1306.5,310.2 1308.0,310.3 1309.5,310.6 1311.0,309.1 1312.5,310.1 1314.0,313.0 1315.5,314.8 1317.0,318.0 1318.5,320.2 1320.0,320.8 1321.5,320.1 1323.0,318.6 1324.5,316.2 1326.0,311.7 1327.5,305.3 1329.0,297.5 1330.5,289.3 1332.0,281.2 1333.5,274.3 1335.0,270.1 1336.5,268.7 1338.0,267.7 1339.5,266.8 1341.0,268.7 1342.5,270.5 1344.0,272.0 1345.5,273.4 1347.0,274.1 1348.5,274.9 1350.0,275.5 1351.5,276.1 1353.0,276.3 1354.5,276.3 1356.0,275.9 1357.5,275.7 1359.0,275.4 1360.5,275.1 1362.0,274.5 1363.5,273.5 1365.0,273.0 1366.5,272.7 1368.0,272.4 1369.5,272.1 1371.0,271.8 1372.5,271.6 1374.0,270.7 1375.5,269.9 1377.0,269.1 1378.5,267.8 1380.0,266.5 1381.5,263.8 1383.0,262.5 1384.5,251.6 1386.0,231.5 1387.5,204.7 1389.0,182.0 1390.5,182.0 1392.0,182.0 1393.5,182.0 1395.0,182.0 1396.5,182.0 1398.0,185.6 1399.5,218.3 1401.0,253.2 1402.5,280.2 1404.0,291.6 1405.5,288.7 1407.0,288.6 1408.5,290.0 1410.0,291.4 1411.5,293.2 1413.0,294.4 1414.5,297.0 1416.0,298.8 1417.5,299.7 1419.0,299.0 1420.5,297.3 1422.0,294.3 1423.5,288.5 1425.0,281.5 1426.5,274.0 1428.0,266.0 1429.5,257.1 1431.0,250.0 1432.5,244.6 1434.0,240.9 1435.5,240.2 1437.0,240.9 1438.5,241.5 1440.0,242.3 1441.5,243.6 1443.0,244.3 1444.5,244.6 1446.0,244.9 1447.5,245.2 1449.0,245.4 1450.5,245.7 1452.0,245.8 1453.5,245.8 1455.0,244.5 1456.5,243.1 1458.0,244.2 1459.5,243.1 1461.0,241.5 1462.5,241.1 1464.0,240.3 1465.5,239.5 1467.0,239.2 1468.5,239.4 1470.0,239.1 1471.5,239.4 1473.0,237.7 1474.5,237.3 1476.0,237.6 1477.5,236.8 1479.0,235.4 1480.5,234.1 1482.0,229.7 1483.5,214.1 1485.0,193.7 1486.5,182.0 1488.0,182.0 1489.5,182.0 1491.0,182.0 1492.5,182.0 1494.0,182.0 1495.5,182.0 1497.0,182.0 1498.5,211.7\"/><polyline class=\"trace\" points=\"0.0,393.3 1.5,393.2 3.0,391.6 4.5,389.8 6.0,387.0 7.5,385.5 9.0,383.5 10.5,380.7 12.0,379.0 13.5,377.4 15.0,376.4 16.5,376.2 18.0,376.2 19.5,377.7 21.0,379.8 22.5,380.2 24.0,381.9 25.5,382.3 27.0,382.8 28.5,383.6 30.0,382.1 31.5,382.0 33.0,382.6 34.5,383.0 36.0,382.7 37.5,380.1 39.0,378.9 40.5,380.7 42.0,380.4 43.5,379.8 45.0,381.0 46.5,382.3 48.0,384.4 49.5,385.7 51.0,386.5 52.5,387.3 54.0,387.6 55.5,388.3 57.0,388.7 58.5,388.5 60.0,388.3 61.5,386.5 63.0,384.7 64.5,378.7 66.0,370.8 67.5,371.2 69.0,371.4 70.5,367.3 72.0,369.4 73.5,379.0 75.0,387.0 76.5,391.8 78.0,396.5 79.5,397.1 81.0,396.4 82.5,397.6 84.0,397.0 85.5,394.7 87.0,394.2 88.5,394.0 90.0,393.7 91.5,393.5 93.0,393.1 94.5,393.7 96.0,393.5 97.5,393.0 99.0,392.2 100.5,390.9 102.0,389.8 103.5,387.3 105.0,384.2 106.5,381.9 108.0,380.1 109.5,378.9 111.0,377.7 112.5,377.4 114.0,376.8 115.5,376.6 117.0,377.5 118.5,379.0 120.0,381.3 121.5,381.9 123.0,382.3 124.5,383.6 126.0,384.5 127.5,385.3 129.0,384.1 130.5,383.2 132.0,382.5 133.5,380.6 135.0,379.5 136.5,378.7 138.0,378.7 139.5,379.3 141.0,379.5 142.5,380.2 144.0,383.2 145.5,385.4 147.0,384.7 148.5,385.6 150.0,387.1 151.5,387.4 153.0,388.3 154.5,387.4 156.0,386.9 157.5,388.2 159.0,386.2 160.5,382.8 162.0,374.9 163.5,372.4 165.0,375.1 166.5,370.3 168.0,365.8 169.5,371.8 171.0,383.2 172.5,388.9 174.0,393.4 175.5,396.1 177.0,396.9 178.5,397.2 180.0,398.1 181.5,398.7 183.0,394.9 184.5,393.7 186.0,393.4 187.5,393.1 189.0,393.2 190.5,392.5 192.0,392.8 193.5,392.1 195.0,392.8 196.5,393.7 198.0,391.5 199.5,389.2 201.0,385.8 202.5,383.8 204.0,382.9 205.5,381.0 207.0,379.3 208.5,378.0 210.0,378.4 211.5,379.0 213.0,379.5 214.5,380.8 216.0,381.9 217.5,382.8 219.0,383.2 220.5,384.0 222.0,384.4 223.5,385.3 225.0,385.5 226.5,385.7 228.0,386.0 229.5,384.0 231.0,382.7 232.5,380.6 234.0,379.8 235.5,380.8 237.0,381.1 238.5,381.7 240.0,382.9 241.5,384.6 243.0,387.0 244.5,388.6 246.0,388.8 247.5,390.9 249.0,391.3 250.5,390.4 252.0,390.2 253.5,389.5 255.0,388.4 256.5,385.8 258.0,384.7 259.5,376.3 261.0,371.8 262.5,376.6 264.0,371.7 265.5,368.4 267.0,374.8 268.5,383.5 270.0,388.9 271.5,393.2 273.0,397.6 274.5,398.7 276.0,398.9 277.5,398.2 279.0,398.2 280.5,396.4 282.0,394.9 283.5,395.0 285.0,394.8 286.5,396.1 288.0,395.1 289.5,394.3 291.0,396.0 292.5,394.3 294.0,391.9 295.5,391.7 297.0,390.2 298.5,388.7 300.0,385.2 301.5,382.7 303.0,382.0 304.5,378.4 306.0,378.4 307.5,379.8 309.0,379.6 310.5,382.0 312.0,381.9 313.5,381.5 315.0,383.6 316.5,384.4 318.0,385.3 319.5,384.9 321.0,384.3 322.5,384.6 324.0,384.6 325.5,384.9 327.0,384.8 328.5,384.9 330.0,383.7 331.5,382.1 333.0,383.7 334.5,383.2 336.0,380.8 337.5,381.7 339.0,383.7 340.5,385.7 342.0,387.1 343.5,387.9 345.0,388.8 346.5,389.5 348.0,389.1 349.5,389.8 351.0,389.7 352.5,390.2 354.0,390.7 355.5,386.7 357.0,381.4 358.5,373.5 360.0,372.1 361.5,374.8 363.0,369.2 364.5,368.4 366.0,377.3 367.5,386.2 369.0,392.1 370.5,395.2 372.0,396.3 373.5,396.7 375.0,398.2 376.5,398.8 378.0,396.3 379.5,395.4 381.0,395.7 382.5,395.4 384.0,395.4 385.5,395.2 387.0,395.9 388.5,394.8 390.0,393.1 391.5,392.7 393.0,392.2 394.5,390.2 396.0,388.6 397.5,387.3 399.0,384.3 400.5,382.3 402.0,380.5 403.5,379.4 405.0,378.7 406.5,378.6 408.0,379.6 409.5,380.1 411.0,381.0 412.5,382.0 414.0,382.8 415.5,383.4 417.0,383.7 418.5,384.1 420.0,385.2 421.5,383.5 423.0,382.0 424.5,382.7 426.0,381.3 427.5,380.2 429.0,380.4 430.5,380.2 432.0,380.6 433.5,380.5 435.0,381.8 436.5,384.4 438.0,385.8 439.5,386.8 441.0,387.6 442.5,388.6 444.0,389.0 445.5,390.6 447.0,390.4 448.5,389.4 450.0,388.9 451.5,386.2 453.0,384.0 454.5,375.1 456.0,373.5 457.5,376.7 459.0,369.6 460.5,367.3 462.0,375.4 463.5,386.1 465.0,391.2 466.5,395.4 468.0,398.1 469.5,398.3 471.0,398.7 472.5,398.8 474.0,398.9 475.5,396.6 477.0,396.0 478.5,396.2 480.0,395.7 481.5,395.8 483.0,395.4 484.5,395.5 486.0,394.5 487.5,393.2 489.0,393.0 490.5,390.9 492.0,389.5 493.5,387.4 495.0,384.3 496.5,383.2 498.0,381.6 499.5,379.8 501.0,378.4 502.5,379.2 504.0,380.4 505.5,381.0 507.0,382.0 508.5,382.9 510.0,385.4 511.5,384.8 513.0,383.3 514.5,384.4 516.0,384.0 517.5,384.3 519.0,384.1 520.5,384.2 522.0,384.2 523.5,381.6 525.0,380.8 526.5,381.5 528.0,381.5 529.5,382.0 531.0,382.0 532.5,383.9 534.0,386.6 535.5,388.0 537.0,389.9 538.5,391.3 540.0,392.1 541.5,392.1 543.0,391.7 544.5,391.1 546.0,391.0 547.5,390.0 549.0,388.7 550.5,382.8 552.0,374.0 553.5,377.4 555.0,377.2 556.5,370.2 558.0,372.1 559.5,381.7 561.0,390.9 562.5,394.5 564.0,398.2 565.5,399.9 567.0,400.8 568.5,401.3 570.0,400.5 571.5,400.3 573.0,399.3 574.5,398.6 576.0,396.8 577.5,395.6 579.0,396.6 580.5,397.2 582.0,397.1 583.5,397.1 585.0,397.2 586.5,394.6 588.0,391.2 589.5,389.5 591.0,388.5 592.5,387.6 594.0,384.1 595.5,381.7 597.0,382.3 598.5,381.7 600.0,381.4 601.5,381.9 603.0,382.6 604.5,383.1 606.0,384.4 607.5,386.2 609.0,386.9 610.5,387.6 612.0,388.2 613.5,389.2 615.0,389.7 616.5,388.9 618.0,389.3 619.5,387.3 621.0,385.3 622.5,384.7 624.0,382.0 625.5,382.5 627.0,383.0 628.5,383.8 630.0,386.8 631.5,388.8 633.0,391.6 634.5,393.3 636.0,392.1 637.5,391.6 639.0,393.8 640.5,393.3 642.0,391.3 643.5,393.6 645.0,392.9 646.5,389.4 648.0,383.2 649.5,375.1 651.0,376.9 652.5,377.5 654.0,370.7 655.5,373.5 657.0,385.1 658.5,391.6 660.0,396.0 661.5,399.7 663.0,399.7 664.5,401.8 666.0,402.7 667.5,402.4 669.0,400.9 670.5,399.2 672.0,399.2 673.5,398.5 675.0,398.3 676.5,397.8 678.0,397.2 679.5,397.8 681.0,399.1 682.5,397.8 684.0,395.0 685.5,393.4 687.0,391.6 688.5,390.0 690.0,387.4 691.5,385.7 693.0,384.7 694.5,382.5 696.0,381.9 697.5,382.7 699.0,383.2 700.5,383.7 702.0,384.8 703.5,387.1 705.0,388.4 706.5,388.9 708.0,389.4 709.5,390.1 711.0,390.6 712.5,390.5 714.0,390.4 715.5,390.7 717.0,389.2 718.5,387.4 720.0,385.8 721.5,384.6 723.0,386.1 724.5,385.6 726.0,386.0 727.5,386.4 729.0,388.3 730.5,390.3 732.0,391.5 733.5,394.8 735.0,394.1 736.5,394.3 738.0,395.6 739.5,394.8 741.0,394.3 742.5,393.6 744.0,391.7 745.5,387.8 747.0,379.0 748.5,375.9\"/><text class=\"lead\" x=\"4\" y=\"21\">I</text><text class=\"lead\" x=\"379\" y=\"21\">AVR</text><text class=\"lead\" x=\"754\" y=\"21\">V1</text><text class=\"lead\" x=\"1129\" y=\"21\">V4</text><text class=\"lead\" x=\"4\" y=\"129\">II</text><text class=\"lead\" x=\"379\" y=\"129\">AVL</text><text class=\"lead\" x=\"754\" y=\"129\">V2</text><text class=\"lead\" x=\"1129\" y=\"129\">V5</text><text class=\"lead\" x=\"4\" y=\"237\">III</text><text class=\"lead\" x=\"379\" y=\"237\">AVF</text><text class=\"lead\" x=\"754\" y=\"237\">V3</text><text class=\"lead\" x=\"1129\" y=\"237\">V6</text><text class=\"lead\" x=\"4\" y=\"346\">II (rhythm)</text><text class=\"cap\" x=\"4\" y=\"452\">12유도 · 실데이터(PTB-XL, CC-BY) · 완전좌각차단</text></svg>"
 },
 {
  "id": "usmle-2026-0037",
  "exam": "usmle",
  "step": "Step 1",
  "subject": "Pathology",
  "subject_file": "Pathology",
  "subtopic": "Chronic Passive Hepatic Congestion (centrilobular / zone 3 necrosis)",
  "type": "Chronic Passive Hepatic Congestion (centrilobular / zone 3 necrosis)",
  "difficulty": 4,
  "created": "2026-07-09",
  "vignette": "A 68-year-old man with longstanding tricuspid regurgitation and progressive right-sided heart failure is found to have a firm, mottled, reddish-brown liver with a mosaic appearance on cut section. Serum aminotransferases are mildly elevated. A liver biopsy shows congestion and hepatocyte necrosis concentrated around the central veins, with relative sparing of hepatocytes near the portal tracts.",
  "question": "Which of the following best explains why this histologic pattern is centered on the central veins rather than the portal tracts?",
  "options": [
   "Kupffer cells are concentrated around the central veins and mediate a localized cytokine-driven injury there",
   "Central-vein hepatocytes are the last in the sinusoidal flow to receive oxygen and are the first to bear the retrograde rise in venous pressure from right heart failure",
   "The central vein carries oxygen-rich hepatic arterial blood directly, so elevated right-sided pressure is transmitted there first",
   "A one-way valve in the sinusoidal capillary bed shields portal-tract hepatocytes from any rise in central venous pressure",
   "Bile canaliculi converge on the central vein, so cholestatic bile acid toxicity accounts for the necrosis seen here"
  ],
  "answer": 2,
  "explanationText": "- 정답근거: 간소엽의 혈류는 문맥삼합(portal triad, 간동맥+문맥)에서 시작해 굴모세혈관(sinusoid)을 거쳐 중심정맥(central vein)으로 모인다. 따라서 zone 3(중심정맥 주변) 간세포는 산소가 이미 상당 부분 소모된 혈액을 가장 늦게 받아 저산소증에 가장 취약하다. 동시에 우심부전으로 상승한 중심정맥압은 간정맥을 통해 역행성으로 전달되는데, 이 압력 상승 역시 중심정맥과 가장 가까운 zone 3 부터 영향을 준다. 저산소증 + 울혈이라는 두 기전이 같은 부위(zone 3)에서 겹쳐 \"nutmeg liver\"의 육안 소견과 중심소엽성 괴사라는 조직 소견을 만든다.\n- 오답감별:\n  - A: Kupffer cell(간 대식세포)은 굴모세혈관 전체에 고르게 분포하며 특정 구역(zone 3)에 국한되지 않는다. 이 문항의 병태생리는 면역·사이토카인 매개가 아니라 저산소증-울혈 매개다.\n  - C: 해부학의 역전 함정이다. 중심정맥은 산소가 풍부한 간동맥혈이 아니라 이미 조직을 거친 간정맥 유출혈(저산소)을 모으는 통로다. 오히려 문맥삼합부가 간동맥의 신선한 산소혈을 먼저 받는다.\n  - D: 그런 \"일방향 밸브\" 구조는 실재하지 않는 가상의 기전이다. 문맥역 간세포는 이중 혈액공급(간동맥+문맥) 덕분에 상대적으로 보호되는 것이지, 밸브 때문이 아니다.\n  - E: 담관은 문맥역(portal tract)으로 모여 담관계를 이루지, 중심정맥으로 모이지 않는다. 이 증례의 생검 소견은 울혈·괴사이지 담즙정체(cholestasis) 패턴이 아니다.\n- 임상핵심: 우심부전 → 간정맥 유출 장애 → \"nutmeg liver\"(중심소엽성 울혈·괴사). 만성화되면 심장성 간경화(cardiac cirrhosis)로 진행할 수 있다. Zone 1(문맥역)은 이중 혈류로 저산소에 강하고, Zone 3(중심정맥)는 저산소·독성물질(예: 아세트아미노펜)에 가장 취약하다는 원칙은 다른 간손상 문제에도 재사용된다.\n- 출처: Robbins Basic Pathology (Liver, hepatic zonation and vascular injury patterns).",
  "explanationItems": [
   {
    "k": "정답근거",
    "v": "간소엽의 혈류는 문맥삼합(portal triad, 간동맥+문맥)에서 시작해 굴모세혈관(sinusoid)을 거쳐 중심정맥(central vein)으로 모인다. 따라서 zone 3(중심정맥 주변) 간세포는 산소가 이미 상당 부분 소모된 혈액을 가장 늦게 받아 저산소증에 가장 취약하다. 동시에 우심부전으로 상승한 중심정맥압은 간정맥을 통해 역행성으로 전달되는데, 이 압력 상승 역시 중심정맥과 가장 가까운 zone 3 부터 영향을 준다. 저산소증 + 울혈이라는 두 기전이 같은 부위(zone 3)에서 겹쳐 \"nutmeg liver\"의 육안 소견과 중심소엽성 괴사라는 조직 소견을 만든다."
   },
   {
    "k": "오답감별",
    "v": "A: Kupffer cell(간 대식세포)은 굴모세혈관 전체에 고르게 분포하며 특정 구역(zone 3)에 국한되지 않는다. 이 문항의 병태생리는 면역·사이토카인 매개가 아니라 저산소증-울혈 매개다.\nC: 해부학의 역전 함정이다. 중심정맥은 산소가 풍부한 간동맥혈이 아니라 이미 조직을 거친 간정맥 유출혈(저산소)을 모으는 통로다. 오히려 문맥삼합부가 간동맥의 신선한 산소혈을 먼저 받는다.\nD: 그런 \"일방향 밸브\" 구조는 실재하지 않는 가상의 기전이다. 문맥역 간세포는 이중 혈액공급(간동맥+문맥) 덕분에 상대적으로 보호되는 것이지, 밸브 때문이 아니다.\nE: 담관은 문맥역(portal tract)으로 모여 담관계를 이루지, 중심정맥으로 모이지 않는다. 이 증례의 생검 소견은 울혈·괴사이지 담즙정체(cholestasis) 패턴이 아니다."
   },
   {
    "k": "임상핵심",
    "v": "우심부전 → 간정맥 유출 장애 → \"nutmeg liver\"(중심소엽성 울혈·괴사). 만성화되면 심장성 간경화(cardiac cirrhosis)로 진행할 수 있다. Zone 1(문맥역)은 이중 혈류로 저산소에 강하고, Zone 3(중심정맥)는 저산소·독성물질(예: 아세트아미노펜)에 가장 취약하다는 원칙은 다른 간손상 문제에도 재사용된다."
   },
   {
    "k": "출처",
    "v": "Robbins Basic Pathology (Liver, hepatic zonation and vascular injury patterns)."
   }
  ],
  "source": "USMLE-style / MedKOS (hepatic pathology · zonal injury)",
  "vitals": [],
  "labs": [],
  "appendix": null,
  "figureSvg": ""
 },
 {
  "id": "usmle-2026-0038",
  "exam": "usmle",
  "step": "Step 1",
  "subject": "Pharmacology",
  "subject_file": "Pharmacology",
  "subtopic": "Beta-Blocker Overdose — Glucagon Rescue Mechanism",
  "type": "Beta-Blocker Overdose — Glucagon Rescue Mechanism",
  "difficulty": 4,
  "created": "2026-07-09",
  "vignette": "A 44-year-old man is brought to the emergency department after intentionally ingesting a large quantity of propranolol. He is bradycardic and hypotensive despite intravenous fluids and atropine. Intravenous glucagon is administered and his heart rate and blood pressure improve.",
  "question": "Which of the following best explains the mechanism by which glucagon reverses this patient's bradycardia and hypotension?",
  "options": [
   "Glucagon inhibits phosphodiesterase in cardiac myocytes, slowing the breakdown of existing cAMP",
   "Glucagon directly opens myocardial L-type calcium channels, raising intracellular calcium independent of any second messenger",
   "Glucagon triggers hepatic glycogenolysis, and the resulting hyperglycemia raises heart rate through an osmotic effect",
   "Glucagon binds its own Gs-coupled receptor on cardiac myocytes, activating adenylate cyclase and raising intracellular cAMP independent of the blocked beta-adrenergic receptor",
   "Glucagon competitively displaces propranolol from the beta-1 adrenergic receptor binding site"
  ],
  "answer": 4,
  "explanationText": "- 정답근거: 프로프라놀롤은 베타-1 수용체를 차단해 Gs 단백질 경로를 통한 아데닐산고리화효소(adenylate cyclase) 활성화를 막는다. 글루카곤은 베타 수용체와는 별개인 자신의 글루카곤 수용체(역시 Gs 결합)를 통해 아데닐산고리화효소를 직접 활성화하므로, 베타 수용체가 막혀 있어도 세포 내 cAMP를 올려 심근 수축력과 심박수를 회복시킬 수 있다. 이것이 베타차단제 과량복용에서 글루카곤이 \"우회 경로(bypass)\" 해독제로 쓰이는 핵심 기전이다.\n- 오답감별:\n  - A: 포스포디에스터라제(PDE) 억제로 cAMP 분해를 늦추는 것은 밀리논(milrinone) 같은 PDE 억제제의 기전이다. 글루카곤의 주작용은 새로운 cAMP를 만드는 수용체-매개 활성화이지, 기존 cAMP 분해를 막는 것이 아니다 — 강심제 기전을 혼동하기 쉬운 함정이다.\n  - B: 글루카곤은 칼슘통로를 직접 여는 것이 아니라 cAMP-단백인산화효소A(PKA) 경로를 통해 간접적으로 칼슘유입을 늘린다. \"직접 통로 개방\"은 기전을 지나치게 단순화한 오개념이다.\n  - C: 글루카곤이 혈당을 올리는 대사 작용은 잘 알려져 있지만, 이는 이 환자의 심박수·혈압 회복과 직접적 인과관계가 없다 — \"글루카곤=혈당호르몬\"이라는 익숙한 지식을 엉뚱한 상황에 끌어오는 전형적 함정이다.\n  - E: 글루카곤은 베타 수용체 결합부위에서 프로프라놀롤과 경쟁하지 않는다. 애초에 별도의 수용체를 쓰기 때문에 \"우회\"라는 표현이 성립한다.\n- 임상핵심: 베타차단제 과량복용으로 아트로핀에 반응하지 않는 서맥·저혈압이 있으면 글루카곤을 우선 고려한다(고용량 인슐린-포도당 요법은 칼슘통로차단제 중독에서 더 중요). \"수용체가 막혀도 다른 수용체로 같은 2차전달자를 올릴 수 있다\"는 원리는 다른 수용체 길항제 해독 문제에도 재사용된다.\n- 출처: Goodman & Gilman's Pharmacological Basis of Therapeutics (Autonomic pharmacology · beta-blocker toxicity).",
  "explanationItems": [
   {
    "k": "정답근거",
    "v": "프로프라놀롤은 베타-1 수용체를 차단해 Gs 단백질 경로를 통한 아데닐산고리화효소(adenylate cyclase) 활성화를 막는다. 글루카곤은 베타 수용체와는 별개인 자신의 글루카곤 수용체(역시 Gs 결합)를 통해 아데닐산고리화효소를 직접 활성화하므로, 베타 수용체가 막혀 있어도 세포 내 cAMP를 올려 심근 수축력과 심박수를 회복시킬 수 있다. 이것이 베타차단제 과량복용에서 글루카곤이 \"우회 경로(bypass)\" 해독제로 쓰이는 핵심 기전이다."
   },
   {
    "k": "오답감별",
    "v": "A: 포스포디에스터라제(PDE) 억제로 cAMP 분해를 늦추는 것은 밀리논(milrinone) 같은 PDE 억제제의 기전이다. 글루카곤의 주작용은 새로운 cAMP를 만드는 수용체-매개 활성화이지, 기존 cAMP 분해를 막는 것이 아니다 — 강심제 기전을 혼동하기 쉬운 함정이다.\nB: 글루카곤은 칼슘통로를 직접 여는 것이 아니라 cAMP-단백인산화효소A(PKA) 경로를 통해 간접적으로 칼슘유입을 늘린다. \"직접 통로 개방\"은 기전을 지나치게 단순화한 오개념이다.\nC: 글루카곤이 혈당을 올리는 대사 작용은 잘 알려져 있지만, 이는 이 환자의 심박수·혈압 회복과 직접적 인과관계가 없다 — \"글루카곤=혈당호르몬\"이라는 익숙한 지식을 엉뚱한 상황에 끌어오는 전형적 함정이다.\nE: 글루카곤은 베타 수용체 결합부위에서 프로프라놀롤과 경쟁하지 않는다. 애초에 별도의 수용체를 쓰기 때문에 \"우회\"라는 표현이 성립한다."
   },
   {
    "k": "임상핵심",
    "v": "베타차단제 과량복용으로 아트로핀에 반응하지 않는 서맥·저혈압이 있으면 글루카곤을 우선 고려한다(고용량 인슐린-포도당 요법은 칼슘통로차단제 중독에서 더 중요). \"수용체가 막혀도 다른 수용체로 같은 2차전달자를 올릴 수 있다\"는 원리는 다른 수용체 길항제 해독 문제에도 재사용된다."
   },
   {
    "k": "출처",
    "v": "Goodman & Gilman's Pharmacological Basis of Therapeutics (Autonomic pharmacology · beta-blocker toxicity)."
   }
  ],
  "source": "USMLE-style / MedKOS (toxicology · receptor pharmacology)",
  "vitals": [],
  "labs": [],
  "appendix": null,
  "figureSvg": ""
 },
 {
  "id": "usmle-2026-0039",
  "exam": "usmle",
  "step": "Step 1",
  "subject": "Physiology",
  "subject_file": "Physiology",
  "subtopic": "ACE Inhibitor-Induced AKI in Bilateral Renal Artery Stenosis",
  "type": "ACE Inhibitor-Induced AKI in Bilateral Renal Artery Stenosis",
  "difficulty": 5,
  "created": "2026-07-09",
  "vignette": "A 74-year-old man with hypertension and known bilateral renal artery stenosis is started on lisinopril. One week later his serum creatinine has risen sharply, as shown in the accompanying labs, while his potassium and sodium remain within the reference range.",
  "question": "Which of the following best explains the mechanism of this acute decline in renal function?",
  "options": [
   "Loss of angiotensin II-mediated efferent arteriolar constriction removes the compensatory mechanism maintaining glomerular filtration pressure distal to the stenoses",
   "Lisinopril directly constricts the afferent arteriole, reducing total renal blood flow independent of angiotensin II",
   "Lisinopril accumulates in proximal tubular cells and causes direct toxic tubular necrosis",
   "Loss of angiotensin II feedback increases renin release, and renin itself is directly toxic to glomerular capillaries at high concentration",
   "Lisinopril precipitates acute thrombosis at the stenotic segment of the renal artery, causing renal infarction"
  ],
  "answer": 1,
  "explanationText": "- 정답근거: 양측 신동맥협착에서는 사구체로 들어가는 관류압 자체가 만성적으로 낮다. 이 상태에서 사구체여과율(GFR)을 유지하는 마지막 보상기전이 바로 안지오텐신II에 의한 수출세동맥(efferent arteriole) 수축이다 — 나가는 길을 좁혀 사구체 내압을 인위적으로 높게 유지하는 것이다. ACE 억제제는 안지오텐신II 생성을 막아 이 수출세동맥 수축을 제거하므로, 이미 관류압이 낮은 상태에서 여과압까지 급격히 떨어져 GFR이 급감하고 크레아티닌이 급상승한다. 이것이 양측(또는 단신) 신동맥협착 환자에서 ACE 억제제/ARB가 금기에 가깝게 다뤄지는 이유다.\n- 오답감별:\n  - B: 수입세동맥(afferent)과 수출세동맥(efferent)을 혼동한 함정이다. ACE 억제제가 문제를 일으키는 부위는 수출세동맥이며, 그것도 직접 수축이 아니라 안지오텐신II 매개 수축을 제거하는 것이다.\n  - C: 세뇨관 직접 독성은 아미노글리코시드 같은 약물의 급성세뇨관괴사(ATN) 기전과 혼동한 것이다. ACE 억제제-신동맥협착 AKI는 혈역학적(hemodynamic) 기전이지 세포독성 기전이 아니다.\n  - D: 레닌 수치는 실제로 상승하지만(음성되먹임 상실), 레닌 자체가 사구체를 직접 손상시킨다는 것은 사실이 아니다 — 되먹임 개념과 가상의 독성 기전을 억지로 결합한 오답이다.\n  - E: 이미 협착이 있다는 사실을 이용한 그럴듯한 함정이지만, ACE 억제제가 혈전증을 유발한다는 기전은 존재하지 않는다. 이 증례처럼 K/Na이 정상 범위인 것도 급성 경색보다는 순수 혈역학적 GFR 저하에 부합한다(참고치로 제시한 정상 K·Na는 신경계 콩팥 손상이 아닌 여과압 저하만 시사하는 미끼값).\n- 임상핵심: 신동맥협착이 의심되면 ACE 억제제/ARB 시작 후 1~2주 내 크레아티닌·칼륨을 재확인한다. 크레아티닌이 기저치 대비 30% 이상 급상승하면 즉시 중단하고 신동맥협착을 재평가한다. \"안지오텐신II는 수출세동맥을 주로 수축시켜 GFR을 지킨다\"는 원리는 NSAID(수입세동맥 확장 차단)와 짝지어 자주 출제된다.\n- 출처: Guyton and Hall Textbook of Medical Physiology (Renal hemodynamics · RAAS autoregulation).",
  "explanationItems": [
   {
    "k": "정답근거",
    "v": "양측 신동맥협착에서는 사구체로 들어가는 관류압 자체가 만성적으로 낮다. 이 상태에서 사구체여과율(GFR)을 유지하는 마지막 보상기전이 바로 안지오텐신II에 의한 수출세동맥(efferent arteriole) 수축이다 — 나가는 길을 좁혀 사구체 내압을 인위적으로 높게 유지하는 것이다. ACE 억제제는 안지오텐신II 생성을 막아 이 수출세동맥 수축을 제거하므로, 이미 관류압이 낮은 상태에서 여과압까지 급격히 떨어져 GFR이 급감하고 크레아티닌이 급상승한다. 이것이 양측(또는 단신) 신동맥협착 환자에서 ACE 억제제/ARB가 금기에 가깝게 다뤄지는 이유다."
   },
   {
    "k": "오답감별",
    "v": "B: 수입세동맥(afferent)과 수출세동맥(efferent)을 혼동한 함정이다. ACE 억제제가 문제를 일으키는 부위는 수출세동맥이며, 그것도 직접 수축이 아니라 안지오텐신II 매개 수축을 제거하는 것이다.\nC: 세뇨관 직접 독성은 아미노글리코시드 같은 약물의 급성세뇨관괴사(ATN) 기전과 혼동한 것이다. ACE 억제제-신동맥협착 AKI는 혈역학적(hemodynamic) 기전이지 세포독성 기전이 아니다.\nD: 레닌 수치는 실제로 상승하지만(음성되먹임 상실), 레닌 자체가 사구체를 직접 손상시킨다는 것은 사실이 아니다 — 되먹임 개념과 가상의 독성 기전을 억지로 결합한 오답이다.\nE: 이미 협착이 있다는 사실을 이용한 그럴듯한 함정이지만, ACE 억제제가 혈전증을 유발한다는 기전은 존재하지 않는다. 이 증례처럼 K/Na이 정상 범위인 것도 급성 경색보다는 순수 혈역학적 GFR 저하에 부합한다(참고치로 제시한 정상 K·Na는 신경계 콩팥 손상이 아닌 여과압 저하만 시사하는 미끼값)."
   },
   {
    "k": "임상핵심",
    "v": "신동맥협착이 의심되면 ACE 억제제/ARB 시작 후 1~2주 내 크레아티닌·칼륨을 재확인한다. 크레아티닌이 기저치 대비 30% 이상 급상승하면 즉시 중단하고 신동맥협착을 재평가한다. \"안지오텐신II는 수출세동맥을 주로 수축시켜 GFR을 지킨다\"는 원리는 NSAID(수입세동맥 확장 차단)와 짝지어 자주 출제된다."
   },
   {
    "k": "출처",
    "v": "Guyton and Hall Textbook of Medical Physiology (Renal hemodynamics · RAAS autoregulation)."
   }
  ],
  "source": "USMLE-style / MedKOS (renal physiology · glomerular hemodynamics)",
  "vitals": [
   {
    "name": "혈압",
    "value": "152/94 mmHg"
   },
   {
    "name": "맥박",
    "value": "78회/분"
   },
   {
    "name": "호흡",
    "value": "16회/분"
   },
   {
    "name": "체온",
    "value": "36.7 °C"
   }
  ],
  "labs": [
   {
    "name": "혈청 크레아티닌 (투약 전)",
    "value": "1.0 mg/dL",
    "ref": "0.7–1.3"
   },
   {
    "name": "혈청 크레아티닌 (투약 1주 후)",
    "value": "2.9 mg/dL",
    "ref": "0.7–1.3"
   },
   {
    "name": "혈청 칼륨",
    "value": "4.6 mEq/L",
    "ref": "3.5–5.0"
   },
   {
    "name": "혈청 나트륨",
    "value": "139 mEq/L",
    "ref": "135–145"
   }
  ],
  "appendix": null,
  "figureSvg": ""
 },
 {
  "id": "usmle-2026-0040",
  "exam": "usmle",
  "step": "Step 2",
  "subject": "Internal Medicine",
  "subject_file": "Internal Medicine",
  "subtopic": "Inferior Wall MI with Suspected Right Ventricular Involvement (12-lead, real ECG)",
  "type": "Inferior Wall MI with Suspected Right Ventricular Involvement (12-lead, real ECG)",
  "difficulty": 5,
  "created": "2026-07-09",
  "vignette": "A 61-year-old man arrives with 90 minutes of crushing substernal chest pain radiating to the jaw and diaphoresis. His blood pressure is 88/56 mmHg and heart rate is 58/min. The 12-lead electrocardiogram shown is obtained. A cardiac catheterization laboratory has already been activated.",
  "question": "Which of the following is the most appropriate immediate next step, given his current vital signs?",
  "options": [
   "Administer sublingual nitroglycerin for chest pain relief before further evaluation",
   "Give intravenous furosemide to reduce preload and relieve presumed pulmonary congestion",
   "Obtain a right-sided ECG (lead V4R) to evaluate for right ventricular infarction before giving nitrates or diuretics",
   "Administer intravenous morphine as first-line analgesia despite the current blood pressure",
   "Start a beta-blocker now to reduce myocardial oxygen demand despite the relative bradycardia"
  ],
  "answer": 3,
  "explanationText": "- 정답근거: 하벽 심근경색(우관상동맥이 흔한 원인혈관)은 우심실경색을 동반하는 경우가 흔하다. 우심실경색이 있으면 심박출량이 전부하(preload)에 극도로 의존하게 되므로, 전부하를 줄이는 어떤 개입(질산염·이뇨제·과도한 아편유사제·베타차단제로 인한 서맥 심화)도 심박출량을 급격히 떨어뜨려 심한 저혈압·쇼크를 유발할 수 있다. 현재 이 환자는 하벽경색 소견 + 저혈압(88/56) + 상대적 서맥(58회/분)이라는 우심실경색 의심 삼징후를 보이므로, 니트로글리세린 등을 주기 전에 우측유도 심전도(V4R) 로 우심실경색 여부(V4R ST분절 상승)를 먼저 확인해야 한다.\n- 오답감별:\n  - A: 하벽경색의 흉통에 반사적으로 니트로글리세린을 주는 것은 우심실경색이 있다면 전부하를 급격히 감소시켜 치명적 저혈압을 유발할 수 있다 — 가장 흔한 함정.\n  - B: 이뇨제 역시 전부하를 줄이는 약제로, 니트로글리세린과 같은 기전으로 우심실경색 환자에서 위험하다. \"폐울혈이 있을 것\"이라는 추정만으로 투여하면 안 된다.\n  - D: 모르핀도 정맥확장을 통해 전부하를 낮춘다. 통증 조절보다 혈역학적 안전 확인이 우선이다.\n  - E: 베타차단제는 서맥을 악화시켜 심박출량을 더 떨어뜨릴 수 있고, 이미 상대적 서맥이 있는 하벽경색에서는 상대적 금기에 가깝다.\n- 임상핵심: 하벽경색 + 저혈압/서맥 조합을 보면 반사적으로 \"우심실경색 감별(V4R) → 전부하 감소 약제 회피 → 수액으로 전부하 유지\"의 순서를 떠올린다. 카테터실 활성화(재관류 준비)는 이 평가와 병행하되, 약물 투여 순서는 혈역학 안전을 우선한다.\n- 출처: ACC/AHA STEMI Guideline (Right ventricular infarction management).",
  "explanationItems": [
   {
    "k": "정답근거",
    "v": "하벽 심근경색(우관상동맥이 흔한 원인혈관)은 우심실경색을 동반하는 경우가 흔하다. 우심실경색이 있으면 심박출량이 전부하(preload)에 극도로 의존하게 되므로, 전부하를 줄이는 어떤 개입(질산염·이뇨제·과도한 아편유사제·베타차단제로 인한 서맥 심화)도 심박출량을 급격히 떨어뜨려 심한 저혈압·쇼크를 유발할 수 있다. 현재 이 환자는 하벽경색 소견 + 저혈압(88/56) + 상대적 서맥(58회/분)이라는 우심실경색 의심 삼징후를 보이므로, 니트로글리세린 등을 주기 전에 우측유도 심전도(V4R) 로 우심실경색 여부(V4R ST분절 상승)를 먼저 확인해야 한다."
   },
   {
    "k": "오답감별",
    "v": "A: 하벽경색의 흉통에 반사적으로 니트로글리세린을 주는 것은 우심실경색이 있다면 전부하를 급격히 감소시켜 치명적 저혈압을 유발할 수 있다 — 가장 흔한 함정.\nB: 이뇨제 역시 전부하를 줄이는 약제로, 니트로글리세린과 같은 기전으로 우심실경색 환자에서 위험하다. \"폐울혈이 있을 것\"이라는 추정만으로 투여하면 안 된다.\nD: 모르핀도 정맥확장을 통해 전부하를 낮춘다. 통증 조절보다 혈역학적 안전 확인이 우선이다.\nE: 베타차단제는 서맥을 악화시켜 심박출량을 더 떨어뜨릴 수 있고, 이미 상대적 서맥이 있는 하벽경색에서는 상대적 금기에 가깝다."
   },
   {
    "k": "임상핵심",
    "v": "하벽경색 + 저혈압/서맥 조합을 보면 반사적으로 \"우심실경색 감별(V4R) → 전부하 감소 약제 회피 → 수액으로 전부하 유지\"의 순서를 떠올린다. 카테터실 활성화(재관류 준비)는 이 평가와 병행하되, 약물 투여 순서는 혈역학 안전을 우선한다."
   },
   {
    "k": "출처",
    "v": "ACC/AHA STEMI Guideline (Right ventricular infarction management)."
   }
  ],
  "source": "USMLE-style / MedKOS · ECG: PTB-XL 1.0.3 (PhysioNet, CC-BY 4.0)",
  "vitals": [
   {
    "name": "혈압",
    "value": "88/56 mmHg"
   },
   {
    "name": "맥박",
    "value": "58회/분"
   },
   {
    "name": "호흡",
    "value": "18회/분"
   },
   {
    "name": "체온",
    "value": "36.6 °C"
   }
  ],
  "labs": [
   {
    "name": "고감도 트로포닌 T",
    "value": "1,850 ng/L",
    "ref": "< 14"
   },
   {
    "name": "혈청 칼륨",
    "value": "4.0 mEq/L",
    "ref": "3.5–5.0"
   },
   {
    "name": "백혈구",
    "value": "10,200 /mm³",
    "ref": "4,000–10,000"
   }
  ],
  "appendix": {
   "가이드라인": "우심실경색 관리 결정표\n─────────────────────────────────────────────\n소견   : 하벽경색 + 저혈압/서맥 + 경정맥압 상승 → V4R ST 상승 확인\n확인 시: 정맥수액으로 전부하 유지, 니트로글리세린·이뇨제·과량 아편유사제·베타차단제 회피\n저혈압 지속 시: 도부타민 등 변력제 고려, 필요시 재관류(1차 PCI) 신속 진행\n─────────────────────────────────────────────\n",
   "최신지견": "우심실경색은 하벽경색 환자의 약 30~50%에서 동반되며 원내 사망률과 밀접하다.",
   "참고문헌": [
    "2013 ACCF/AHA STEMI Guideline",
    "Braunwald's Heart Disease — Right ventricular infarction"
   ]
  },
  "figureSvg": "<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 1500 456\" width=\"1500\" height=\"456\" role=\"img\" aria-label=\"12-lead ECG 12유도 · 실데이터(PTB-XL, CC-BY) · 하벽·전중격 심근경색\"><style>.bg{fill:#fff}.gmin{stroke:#f4c9c9;stroke-width:0.5}.gmaj{stroke:#e59a9a;stroke-width:1}.trace{fill:none;stroke:#111;stroke-width:1.2;stroke-linejoin:round}.lead{font:bold 11px sans-serif;fill:#333}.cap{font:11px sans-serif;fill:#555}</style><rect class=\"bg\" x=\"0\" y=\"0\" width=\"1500\" height=\"440\"/><line x1=\"0\" y1=\"0\" x2=\"0\" y2=\"440\" class=\"gmaj\"/><line x1=\"6\" y1=\"0\" x2=\"6\" y2=\"440\" class=\"gmin\"/><line x1=\"12\" y1=\"0\" x2=\"12\" y2=\"440\" class=\"gmin\"/><line x1=\"18\" y1=\"0\" x2=\"18\" y2=\"440\" class=\"gmin\"/><line x1=\"24\" y1=\"0\" x2=\"24\" y2=\"440\" class=\"gmin\"/><line x1=\"30\" y1=\"0\" x2=\"30\" y2=\"440\" class=\"gmaj\"/><line x1=\"36\" y1=\"0\" x2=\"36\" y2=\"440\" class=\"gmin\"/><line x1=\"42\" y1=\"0\" x2=\"42\" y2=\"440\" class=\"gmin\"/><line x1=\"48\" y1=\"0\" x2=\"48\" y2=\"440\" class=\"gmin\"/><line x1=\"54\" y1=\"0\" x2=\"54\" y2=\"440\" class=\"gmin\"/><line x1=\"60\" y1=\"0\" x2=\"60\" y2=\"440\" class=\"gmaj\"/><line x1=\"66\" y1=\"0\" x2=\"66\" y2=\"440\" class=\"gmin\"/><line x1=\"72\" y1=\"0\" x2=\"72\" y2=\"440\" class=\"gmin\"/><line x1=\"78\" y1=\"0\" x2=\"78\" y2=\"440\" class=\"gmin\"/><line x1=\"84\" y1=\"0\" x2=\"84\" y2=\"440\" class=\"gmin\"/><line x1=\"90\" y1=\"0\" x2=\"90\" y2=\"440\" class=\"gmaj\"/><line x1=\"96\" y1=\"0\" x2=\"96\" y2=\"440\" class=\"gmin\"/><line x1=\"102\" y1=\"0\" x2=\"102\" y2=\"440\" class=\"gmin\"/><line x1=\"108\" y1=\"0\" x2=\"108\" y2=\"440\" class=\"gmin\"/><line x1=\"114\" y1=\"0\" x2=\"114\" y2=\"440\" class=\"gmin\"/><line x1=\"120\" y1=\"0\" x2=\"120\" y2=\"440\" class=\"gmaj\"/><line x1=\"126\" y1=\"0\" x2=\"126\" y2=\"440\" class=\"gmin\"/><line x1=\"132\" y1=\"0\" x2=\"132\" y2=\"440\" class=\"gmin\"/><line x1=\"138\" y1=\"0\" x2=\"138\" y2=\"440\" class=\"gmin\"/><line x1=\"144\" y1=\"0\" x2=\"144\" y2=\"440\" class=\"gmin\"/><line x1=\"150\" y1=\"0\" x2=\"150\" y2=\"440\" class=\"gmaj\"/><line x1=\"156\" y1=\"0\" x2=\"156\" y2=\"440\" class=\"gmin\"/><line x1=\"162\" y1=\"0\" x2=\"162\" y2=\"440\" class=\"gmin\"/><line x1=\"168\" y1=\"0\" x2=\"168\" y2=\"440\" class=\"gmin\"/><line x1=\"174\" y1=\"0\" x2=\"174\" y2=\"440\" class=\"gmin\"/><line x1=\"180\" y1=\"0\" x2=\"180\" y2=\"440\" class=\"gmaj\"/><line x1=\"186\" y1=\"0\" x2=\"186\" y2=\"440\" class=\"gmin\"/><line x1=\"192\" y1=\"0\" x2=\"192\" y2=\"440\" class=\"gmin\"/><line x1=\"198\" y1=\"0\" x2=\"198\" y2=\"440\" class=\"gmin\"/><line x1=\"204\" y1=\"0\" x2=\"204\" y2=\"440\" class=\"gmin\"/><line x1=\"210\" y1=\"0\" x2=\"210\" y2=\"440\" class=\"gmaj\"/><line x1=\"216\" y1=\"0\" x2=\"216\" y2=\"440\" class=\"gmin\"/><line x1=\"222\" y1=\"0\" x2=\"222\" y2=\"440\" class=\"gmin\"/><line x1=\"228\" y1=\"0\" x2=\"228\" y2=\"440\" class=\"gmin\"/><line x1=\"234\" y1=\"0\" x2=\"234\" y2=\"440\" class=\"gmin\"/><line x1=\"240\" y1=\"0\" x2=\"240\" y2=\"440\" class=\"gmaj\"/><line x1=\"246\" y1=\"0\" x2=\"246\" y2=\"440\" class=\"gmin\"/><line x1=\"252\" y1=\"0\" x2=\"252\" y2=\"440\" class=\"gmin\"/><line x1=\"258\" y1=\"0\" x2=\"258\" y2=\"440\" class=\"gmin\"/><line x1=\"264\" y1=\"0\" x2=\"264\" y2=\"440\" class=\"gmin\"/><line x1=\"270\" y1=\"0\" x2=\"270\" y2=\"440\" class=\"gmaj\"/><line x1=\"276\" y1=\"0\" x2=\"276\" y2=\"440\" class=\"gmin\"/><line x1=\"282\" y1=\"0\" x2=\"282\" y2=\"440\" class=\"gmin\"/><line x1=\"288\" y1=\"0\" x2=\"288\" y2=\"440\" class=\"gmin\"/><line x1=\"294\" y1=\"0\" x2=\"294\" y2=\"440\" class=\"gmin\"/><line x1=\"300\" y1=\"0\" x2=\"300\" y2=\"440\" class=\"gmaj\"/><line x1=\"306\" y1=\"0\" x2=\"306\" y2=\"440\" class=\"gmin\"/><line x1=\"312\" y1=\"0\" x2=\"312\" y2=\"440\" class=\"gmin\"/><line x1=\"318\" y1=\"0\" x2=\"318\" y2=\"440\" class=\"gmin\"/><line x1=\"324\" y1=\"0\" x2=\"324\" y2=\"440\" class=\"gmin\"/><line x1=\"330\" y1=\"0\" x2=\"330\" y2=\"440\" class=\"gmaj\"/><line x1=\"336\" y1=\"0\" x2=\"336\" y2=\"440\" class=\"gmin\"/><line x1=\"342\" y1=\"0\" x2=\"342\" y2=\"440\" class=\"gmin\"/><line x1=\"348\" y1=\"0\" x2=\"348\" y2=\"440\" class=\"gmin\"/><line x1=\"354\" y1=\"0\" x2=\"354\" y2=\"440\" class=\"gmin\"/><line x1=\"360\" y1=\"0\" x2=\"360\" y2=\"440\" class=\"gmaj\"/><line x1=\"366\" y1=\"0\" x2=\"366\" y2=\"440\" class=\"gmin\"/><line x1=\"372\" y1=\"0\" x2=\"372\" y2=\"440\" class=\"gmin\"/><line x1=\"378\" y1=\"0\" x2=\"378\" y2=\"440\" class=\"gmin\"/><line x1=\"384\" y1=\"0\" x2=\"384\" y2=\"440\" class=\"gmin\"/><line x1=\"390\" y1=\"0\" x2=\"390\" y2=\"440\" class=\"gmaj\"/><line x1=\"396\" y1=\"0\" x2=\"396\" y2=\"440\" class=\"gmin\"/><line x1=\"402\" y1=\"0\" x2=\"402\" y2=\"440\" class=\"gmin\"/><line x1=\"408\" y1=\"0\" x2=\"408\" y2=\"440\" class=\"gmin\"/><line x1=\"414\" y1=\"0\" x2=\"414\" y2=\"440\" class=\"gmin\"/><line x1=\"420\" y1=\"0\" x2=\"420\" y2=\"440\" class=\"gmaj\"/><line x1=\"426\" y1=\"0\" x2=\"426\" y2=\"440\" class=\"gmin\"/><line x1=\"432\" y1=\"0\" x2=\"432\" y2=\"440\" class=\"gmin\"/><line x1=\"438\" y1=\"0\" x2=\"438\" y2=\"440\" class=\"gmin\"/><line x1=\"444\" y1=\"0\" x2=\"444\" y2=\"440\" class=\"gmin\"/><line x1=\"450\" y1=\"0\" x2=\"450\" y2=\"440\" class=\"gmaj\"/><line x1=\"456\" y1=\"0\" x2=\"456\" y2=\"440\" class=\"gmin\"/><line x1=\"462\" y1=\"0\" x2=\"462\" y2=\"440\" class=\"gmin\"/><line x1=\"468\" y1=\"0\" x2=\"468\" y2=\"440\" class=\"gmin\"/><line x1=\"474\" y1=\"0\" x2=\"474\" y2=\"440\" class=\"gmin\"/><line x1=\"480\" y1=\"0\" x2=\"480\" y2=\"440\" class=\"gmaj\"/><line x1=\"486\" y1=\"0\" x2=\"486\" y2=\"440\" class=\"gmin\"/><line x1=\"492\" y1=\"0\" x2=\"492\" y2=\"440\" class=\"gmin\"/><line x1=\"498\" y1=\"0\" x2=\"498\" y2=\"440\" class=\"gmin\"/><line x1=\"504\" y1=\"0\" x2=\"504\" y2=\"440\" class=\"gmin\"/><line x1=\"510\" y1=\"0\" x2=\"510\" y2=\"440\" class=\"gmaj\"/><line x1=\"516\" y1=\"0\" x2=\"516\" y2=\"440\" class=\"gmin\"/><line x1=\"522\" y1=\"0\" x2=\"522\" y2=\"440\" class=\"gmin\"/><line x1=\"528\" y1=\"0\" x2=\"528\" y2=\"440\" class=\"gmin\"/><line x1=\"534\" y1=\"0\" x2=\"534\" y2=\"440\" class=\"gmin\"/><line x1=\"540\" y1=\"0\" x2=\"540\" y2=\"440\" class=\"gmaj\"/><line x1=\"546\" y1=\"0\" x2=\"546\" y2=\"440\" class=\"gmin\"/><line x1=\"552\" y1=\"0\" x2=\"552\" y2=\"440\" class=\"gmin\"/><line x1=\"558\" y1=\"0\" x2=\"558\" y2=\"440\" class=\"gmin\"/><line x1=\"564\" y1=\"0\" x2=\"564\" y2=\"440\" class=\"gmin\"/><line x1=\"570\" y1=\"0\" x2=\"570\" y2=\"440\" class=\"gmaj\"/><line x1=\"576\" y1=\"0\" x2=\"576\" y2=\"440\" class=\"gmin\"/><line x1=\"582\" y1=\"0\" x2=\"582\" y2=\"440\" class=\"gmin\"/><line x1=\"588\" y1=\"0\" x2=\"588\" y2=\"440\" class=\"gmin\"/><line x1=\"594\" y1=\"0\" x2=\"594\" y2=\"440\" class=\"gmin\"/><line x1=\"600\" y1=\"0\" x2=\"600\" y2=\"440\" class=\"gmaj\"/><line x1=\"606\" y1=\"0\" x2=\"606\" y2=\"440\" class=\"gmin\"/><line x1=\"612\" y1=\"0\" x2=\"612\" y2=\"440\" class=\"gmin\"/><line x1=\"618\" y1=\"0\" x2=\"618\" y2=\"440\" class=\"gmin\"/><line x1=\"624\" y1=\"0\" x2=\"624\" y2=\"440\" class=\"gmin\"/><line x1=\"630\" y1=\"0\" x2=\"630\" y2=\"440\" class=\"gmaj\"/><line x1=\"636\" y1=\"0\" x2=\"636\" y2=\"440\" class=\"gmin\"/><line x1=\"642\" y1=\"0\" x2=\"642\" y2=\"440\" class=\"gmin\"/><line x1=\"648\" y1=\"0\" x2=\"648\" y2=\"440\" class=\"gmin\"/><line x1=\"654\" y1=\"0\" x2=\"654\" y2=\"440\" class=\"gmin\"/><line x1=\"660\" y1=\"0\" x2=\"660\" y2=\"440\" class=\"gmaj\"/><line x1=\"666\" y1=\"0\" x2=\"666\" y2=\"440\" class=\"gmin\"/><line x1=\"672\" y1=\"0\" x2=\"672\" y2=\"440\" class=\"gmin\"/><line x1=\"678\" y1=\"0\" x2=\"678\" y2=\"440\" class=\"gmin\"/><line x1=\"684\" y1=\"0\" x2=\"684\" y2=\"440\" class=\"gmin\"/><line x1=\"690\" y1=\"0\" x2=\"690\" y2=\"440\" class=\"gmaj\"/><line x1=\"696\" y1=\"0\" x2=\"696\" y2=\"440\" class=\"gmin\"/><line x1=\"702\" y1=\"0\" x2=\"702\" y2=\"440\" class=\"gmin\"/><line x1=\"708\" y1=\"0\" x2=\"708\" y2=\"440\" class=\"gmin\"/><line x1=\"714\" y1=\"0\" x2=\"714\" y2=\"440\" class=\"gmin\"/><line x1=\"720\" y1=\"0\" x2=\"720\" y2=\"440\" class=\"gmaj\"/><line x1=\"726\" y1=\"0\" x2=\"726\" y2=\"440\" class=\"gmin\"/><line x1=\"732\" y1=\"0\" x2=\"732\" y2=\"440\" class=\"gmin\"/><line x1=\"738\" y1=\"0\" x2=\"738\" y2=\"440\" class=\"gmin\"/><line x1=\"744\" y1=\"0\" x2=\"744\" y2=\"440\" class=\"gmin\"/><line x1=\"750\" y1=\"0\" x2=\"750\" y2=\"440\" class=\"gmaj\"/><line x1=\"756\" y1=\"0\" x2=\"756\" y2=\"440\" class=\"gmin\"/><line x1=\"762\" y1=\"0\" x2=\"762\" y2=\"440\" class=\"gmin\"/><line x1=\"768\" y1=\"0\" x2=\"768\" y2=\"440\" class=\"gmin\"/><line x1=\"774\" y1=\"0\" x2=\"774\" y2=\"440\" class=\"gmin\"/><line x1=\"780\" y1=\"0\" x2=\"780\" y2=\"440\" class=\"gmaj\"/><line x1=\"786\" y1=\"0\" x2=\"786\" y2=\"440\" class=\"gmin\"/><line x1=\"792\" y1=\"0\" x2=\"792\" y2=\"440\" class=\"gmin\"/><line x1=\"798\" y1=\"0\" x2=\"798\" y2=\"440\" class=\"gmin\"/><line x1=\"804\" y1=\"0\" x2=\"804\" y2=\"440\" class=\"gmin\"/><line x1=\"810\" y1=\"0\" x2=\"810\" y2=\"440\" class=\"gmaj\"/><line x1=\"816\" y1=\"0\" x2=\"816\" y2=\"440\" class=\"gmin\"/><line x1=\"822\" y1=\"0\" x2=\"822\" y2=\"440\" class=\"gmin\"/><line x1=\"828\" y1=\"0\" x2=\"828\" y2=\"440\" class=\"gmin\"/><line x1=\"834\" y1=\"0\" x2=\"834\" y2=\"440\" class=\"gmin\"/><line x1=\"840\" y1=\"0\" x2=\"840\" y2=\"440\" class=\"gmaj\"/><line x1=\"846\" y1=\"0\" x2=\"846\" y2=\"440\" class=\"gmin\"/><line x1=\"852\" y1=\"0\" x2=\"852\" y2=\"440\" class=\"gmin\"/><line x1=\"858\" y1=\"0\" x2=\"858\" y2=\"440\" class=\"gmin\"/><line x1=\"864\" y1=\"0\" x2=\"864\" y2=\"440\" class=\"gmin\"/><line x1=\"870\" y1=\"0\" x2=\"870\" y2=\"440\" class=\"gmaj\"/><line x1=\"876\" y1=\"0\" x2=\"876\" y2=\"440\" class=\"gmin\"/><line x1=\"882\" y1=\"0\" x2=\"882\" y2=\"440\" class=\"gmin\"/><line x1=\"888\" y1=\"0\" x2=\"888\" y2=\"440\" class=\"gmin\"/><line x1=\"894\" y1=\"0\" x2=\"894\" y2=\"440\" class=\"gmin\"/><line x1=\"900\" y1=\"0\" x2=\"900\" y2=\"440\" class=\"gmaj\"/><line x1=\"906\" y1=\"0\" x2=\"906\" y2=\"440\" class=\"gmin\"/><line x1=\"912\" y1=\"0\" x2=\"912\" y2=\"440\" class=\"gmin\"/><line x1=\"918\" y1=\"0\" x2=\"918\" y2=\"440\" class=\"gmin\"/><line x1=\"924\" y1=\"0\" x2=\"924\" y2=\"440\" class=\"gmin\"/><line x1=\"930\" y1=\"0\" x2=\"930\" y2=\"440\" class=\"gmaj\"/><line x1=\"936\" y1=\"0\" x2=\"936\" y2=\"440\" class=\"gmin\"/><line x1=\"942\" y1=\"0\" x2=\"942\" y2=\"440\" class=\"gmin\"/><line x1=\"948\" y1=\"0\" x2=\"948\" y2=\"440\" class=\"gmin\"/><line x1=\"954\" y1=\"0\" x2=\"954\" y2=\"440\" class=\"gmin\"/><line x1=\"960\" y1=\"0\" x2=\"960\" y2=\"440\" class=\"gmaj\"/><line x1=\"966\" y1=\"0\" x2=\"966\" y2=\"440\" class=\"gmin\"/><line x1=\"972\" y1=\"0\" x2=\"972\" y2=\"440\" class=\"gmin\"/><line x1=\"978\" y1=\"0\" x2=\"978\" y2=\"440\" class=\"gmin\"/><line x1=\"984\" y1=\"0\" x2=\"984\" y2=\"440\" class=\"gmin\"/><line x1=\"990\" y1=\"0\" x2=\"990\" y2=\"440\" class=\"gmaj\"/><line x1=\"996\" y1=\"0\" x2=\"996\" y2=\"440\" class=\"gmin\"/><line x1=\"1002\" y1=\"0\" x2=\"1002\" y2=\"440\" class=\"gmin\"/><line x1=\"1008\" y1=\"0\" x2=\"1008\" y2=\"440\" class=\"gmin\"/><line x1=\"1014\" y1=\"0\" x2=\"1014\" y2=\"440\" class=\"gmin\"/><line x1=\"1020\" y1=\"0\" x2=\"1020\" y2=\"440\" class=\"gmaj\"/><line x1=\"1026\" y1=\"0\" x2=\"1026\" y2=\"440\" class=\"gmin\"/><line x1=\"1032\" y1=\"0\" x2=\"1032\" y2=\"440\" class=\"gmin\"/><line x1=\"1038\" y1=\"0\" x2=\"1038\" y2=\"440\" class=\"gmin\"/><line x1=\"1044\" y1=\"0\" x2=\"1044\" y2=\"440\" class=\"gmin\"/><line x1=\"1050\" y1=\"0\" x2=\"1050\" y2=\"440\" class=\"gmaj\"/><line x1=\"1056\" y1=\"0\" x2=\"1056\" y2=\"440\" class=\"gmin\"/><line x1=\"1062\" y1=\"0\" x2=\"1062\" y2=\"440\" class=\"gmin\"/><line x1=\"1068\" y1=\"0\" x2=\"1068\" y2=\"440\" class=\"gmin\"/><line x1=\"1074\" y1=\"0\" x2=\"1074\" y2=\"440\" class=\"gmin\"/><line x1=\"1080\" y1=\"0\" x2=\"1080\" y2=\"440\" class=\"gmaj\"/><line x1=\"1086\" y1=\"0\" x2=\"1086\" y2=\"440\" class=\"gmin\"/><line x1=\"1092\" y1=\"0\" x2=\"1092\" y2=\"440\" class=\"gmin\"/><line x1=\"1098\" y1=\"0\" x2=\"1098\" y2=\"440\" class=\"gmin\"/><line x1=\"1104\" y1=\"0\" x2=\"1104\" y2=\"440\" class=\"gmin\"/><line x1=\"1110\" y1=\"0\" x2=\"1110\" y2=\"440\" class=\"gmaj\"/><line x1=\"1116\" y1=\"0\" x2=\"1116\" y2=\"440\" class=\"gmin\"/><line x1=\"1122\" y1=\"0\" x2=\"1122\" y2=\"440\" class=\"gmin\"/><line x1=\"1128\" y1=\"0\" x2=\"1128\" y2=\"440\" class=\"gmin\"/><line x1=\"1134\" y1=\"0\" x2=\"1134\" y2=\"440\" class=\"gmin\"/><line x1=\"1140\" y1=\"0\" x2=\"1140\" y2=\"440\" class=\"gmaj\"/><line x1=\"1146\" y1=\"0\" x2=\"1146\" y2=\"440\" class=\"gmin\"/><line x1=\"1152\" y1=\"0\" x2=\"1152\" y2=\"440\" class=\"gmin\"/><line x1=\"1158\" y1=\"0\" x2=\"1158\" y2=\"440\" class=\"gmin\"/><line x1=\"1164\" y1=\"0\" x2=\"1164\" y2=\"440\" class=\"gmin\"/><line x1=\"1170\" y1=\"0\" x2=\"1170\" y2=\"440\" class=\"gmaj\"/><line x1=\"1176\" y1=\"0\" x2=\"1176\" y2=\"440\" class=\"gmin\"/><line x1=\"1182\" y1=\"0\" x2=\"1182\" y2=\"440\" class=\"gmin\"/><line x1=\"1188\" y1=\"0\" x2=\"1188\" y2=\"440\" class=\"gmin\"/><line x1=\"1194\" y1=\"0\" x2=\"1194\" y2=\"440\" class=\"gmin\"/><line x1=\"1200\" y1=\"0\" x2=\"1200\" y2=\"440\" class=\"gmaj\"/><line x1=\"1206\" y1=\"0\" x2=\"1206\" y2=\"440\" class=\"gmin\"/><line x1=\"1212\" y1=\"0\" x2=\"1212\" y2=\"440\" class=\"gmin\"/><line x1=\"1218\" y1=\"0\" x2=\"1218\" y2=\"440\" class=\"gmin\"/><line x1=\"1224\" y1=\"0\" x2=\"1224\" y2=\"440\" class=\"gmin\"/><line x1=\"1230\" y1=\"0\" x2=\"1230\" y2=\"440\" class=\"gmaj\"/><line x1=\"1236\" y1=\"0\" x2=\"1236\" y2=\"440\" class=\"gmin\"/><line x1=\"1242\" y1=\"0\" x2=\"1242\" y2=\"440\" class=\"gmin\"/><line x1=\"1248\" y1=\"0\" x2=\"1248\" y2=\"440\" class=\"gmin\"/><line x1=\"1254\" y1=\"0\" x2=\"1254\" y2=\"440\" class=\"gmin\"/><line x1=\"1260\" y1=\"0\" x2=\"1260\" y2=\"440\" class=\"gmaj\"/><line x1=\"1266\" y1=\"0\" x2=\"1266\" y2=\"440\" class=\"gmin\"/><line x1=\"1272\" y1=\"0\" x2=\"1272\" y2=\"440\" class=\"gmin\"/><line x1=\"1278\" y1=\"0\" x2=\"1278\" y2=\"440\" class=\"gmin\"/><line x1=\"1284\" y1=\"0\" x2=\"1284\" y2=\"440\" class=\"gmin\"/><line x1=\"1290\" y1=\"0\" x2=\"1290\" y2=\"440\" class=\"gmaj\"/><line x1=\"1296\" y1=\"0\" x2=\"1296\" y2=\"440\" class=\"gmin\"/><line x1=\"1302\" y1=\"0\" x2=\"1302\" y2=\"440\" class=\"gmin\"/><line x1=\"1308\" y1=\"0\" x2=\"1308\" y2=\"440\" class=\"gmin\"/><line x1=\"1314\" y1=\"0\" x2=\"1314\" y2=\"440\" class=\"gmin\"/><line x1=\"1320\" y1=\"0\" x2=\"1320\" y2=\"440\" class=\"gmaj\"/><line x1=\"1326\" y1=\"0\" x2=\"1326\" y2=\"440\" class=\"gmin\"/><line x1=\"1332\" y1=\"0\" x2=\"1332\" y2=\"440\" class=\"gmin\"/><line x1=\"1338\" y1=\"0\" x2=\"1338\" y2=\"440\" class=\"gmin\"/><line x1=\"1344\" y1=\"0\" x2=\"1344\" y2=\"440\" class=\"gmin\"/><line x1=\"1350\" y1=\"0\" x2=\"1350\" y2=\"440\" class=\"gmaj\"/><line x1=\"1356\" y1=\"0\" x2=\"1356\" y2=\"440\" class=\"gmin\"/><line x1=\"1362\" y1=\"0\" x2=\"1362\" y2=\"440\" class=\"gmin\"/><line x1=\"1368\" y1=\"0\" x2=\"1368\" y2=\"440\" class=\"gmin\"/><line x1=\"1374\" y1=\"0\" x2=\"1374\" y2=\"440\" class=\"gmin\"/><line x1=\"1380\" y1=\"0\" x2=\"1380\" y2=\"440\" class=\"gmaj\"/><line x1=\"1386\" y1=\"0\" x2=\"1386\" y2=\"440\" class=\"gmin\"/><line x1=\"1392\" y1=\"0\" x2=\"1392\" y2=\"440\" class=\"gmin\"/><line x1=\"1398\" y1=\"0\" x2=\"1398\" y2=\"440\" class=\"gmin\"/><line x1=\"1404\" y1=\"0\" x2=\"1404\" y2=\"440\" class=\"gmin\"/><line x1=\"1410\" y1=\"0\" x2=\"1410\" y2=\"440\" class=\"gmaj\"/><line x1=\"1416\" y1=\"0\" x2=\"1416\" y2=\"440\" class=\"gmin\"/><line x1=\"1422\" y1=\"0\" x2=\"1422\" y2=\"440\" class=\"gmin\"/><line x1=\"1428\" y1=\"0\" x2=\"1428\" y2=\"440\" class=\"gmin\"/><line x1=\"1434\" y1=\"0\" x2=\"1434\" y2=\"440\" class=\"gmin\"/><line x1=\"1440\" y1=\"0\" x2=\"1440\" y2=\"440\" class=\"gmaj\"/><line x1=\"1446\" y1=\"0\" x2=\"1446\" y2=\"440\" class=\"gmin\"/><line x1=\"1452\" y1=\"0\" x2=\"1452\" y2=\"440\" class=\"gmin\"/><line x1=\"1458\" y1=\"0\" x2=\"1458\" y2=\"440\" class=\"gmin\"/><line x1=\"1464\" y1=\"0\" x2=\"1464\" y2=\"440\" class=\"gmin\"/><line x1=\"1470\" y1=\"0\" x2=\"1470\" y2=\"440\" class=\"gmaj\"/><line x1=\"1476\" y1=\"0\" x2=\"1476\" y2=\"440\" class=\"gmin\"/><line x1=\"1482\" y1=\"0\" x2=\"1482\" y2=\"440\" class=\"gmin\"/><line x1=\"1488\" y1=\"0\" x2=\"1488\" y2=\"440\" class=\"gmin\"/><line x1=\"1494\" y1=\"0\" x2=\"1494\" y2=\"440\" class=\"gmin\"/><line x1=\"1500\" y1=\"0\" x2=\"1500\" y2=\"440\" class=\"gmaj\"/><line x1=\"0\" y1=\"0\" x2=\"1500\" y2=\"0\" class=\"gmaj\"/><line x1=\"0\" y1=\"6\" x2=\"1500\" y2=\"6\" class=\"gmin\"/><line x1=\"0\" y1=\"12\" x2=\"1500\" y2=\"12\" class=\"gmin\"/><line x1=\"0\" y1=\"18\" x2=\"1500\" y2=\"18\" class=\"gmin\"/><line x1=\"0\" y1=\"24\" x2=\"1500\" y2=\"24\" class=\"gmin\"/><line x1=\"0\" y1=\"30\" x2=\"1500\" y2=\"30\" class=\"gmaj\"/><line x1=\"0\" y1=\"36\" x2=\"1500\" y2=\"36\" class=\"gmin\"/><line x1=\"0\" y1=\"42\" x2=\"1500\" y2=\"42\" class=\"gmin\"/><line x1=\"0\" y1=\"48\" x2=\"1500\" y2=\"48\" class=\"gmin\"/><line x1=\"0\" y1=\"54\" x2=\"1500\" y2=\"54\" class=\"gmin\"/><line x1=\"0\" y1=\"60\" x2=\"1500\" y2=\"60\" class=\"gmaj\"/><line x1=\"0\" y1=\"66\" x2=\"1500\" y2=\"66\" class=\"gmin\"/><line x1=\"0\" y1=\"72\" x2=\"1500\" y2=\"72\" class=\"gmin\"/><line x1=\"0\" y1=\"78\" x2=\"1500\" y2=\"78\" class=\"gmin\"/><line x1=\"0\" y1=\"84\" x2=\"1500\" y2=\"84\" class=\"gmin\"/><line x1=\"0\" y1=\"90\" x2=\"1500\" y2=\"90\" class=\"gmaj\"/><line x1=\"0\" y1=\"96\" x2=\"1500\" y2=\"96\" class=\"gmin\"/><line x1=\"0\" y1=\"102\" x2=\"1500\" y2=\"102\" class=\"gmin\"/><line x1=\"0\" y1=\"108\" x2=\"1500\" y2=\"108\" class=\"gmin\"/><line x1=\"0\" y1=\"114\" x2=\"1500\" y2=\"114\" class=\"gmin\"/><line x1=\"0\" y1=\"120\" x2=\"1500\" y2=\"120\" class=\"gmaj\"/><line x1=\"0\" y1=\"126\" x2=\"1500\" y2=\"126\" class=\"gmin\"/><line x1=\"0\" y1=\"132\" x2=\"1500\" y2=\"132\" class=\"gmin\"/><line x1=\"0\" y1=\"138\" x2=\"1500\" y2=\"138\" class=\"gmin\"/><line x1=\"0\" y1=\"144\" x2=\"1500\" y2=\"144\" class=\"gmin\"/><line x1=\"0\" y1=\"150\" x2=\"1500\" y2=\"150\" class=\"gmaj\"/><line x1=\"0\" y1=\"156\" x2=\"1500\" y2=\"156\" class=\"gmin\"/><line x1=\"0\" y1=\"162\" x2=\"1500\" y2=\"162\" class=\"gmin\"/><line x1=\"0\" y1=\"168\" x2=\"1500\" y2=\"168\" class=\"gmin\"/><line x1=\"0\" y1=\"174\" x2=\"1500\" y2=\"174\" class=\"gmin\"/><line x1=\"0\" y1=\"180\" x2=\"1500\" y2=\"180\" class=\"gmaj\"/><line x1=\"0\" y1=\"186\" x2=\"1500\" y2=\"186\" class=\"gmin\"/><line x1=\"0\" y1=\"192\" x2=\"1500\" y2=\"192\" class=\"gmin\"/><line x1=\"0\" y1=\"198\" x2=\"1500\" y2=\"198\" class=\"gmin\"/><line x1=\"0\" y1=\"204\" x2=\"1500\" y2=\"204\" class=\"gmin\"/><line x1=\"0\" y1=\"210\" x2=\"1500\" y2=\"210\" class=\"gmaj\"/><line x1=\"0\" y1=\"216\" x2=\"1500\" y2=\"216\" class=\"gmin\"/><line x1=\"0\" y1=\"222\" x2=\"1500\" y2=\"222\" class=\"gmin\"/><line x1=\"0\" y1=\"228\" x2=\"1500\" y2=\"228\" class=\"gmin\"/><line x1=\"0\" y1=\"234\" x2=\"1500\" y2=\"234\" class=\"gmin\"/><line x1=\"0\" y1=\"240\" x2=\"1500\" y2=\"240\" class=\"gmaj\"/><line x1=\"0\" y1=\"246\" x2=\"1500\" y2=\"246\" class=\"gmin\"/><line x1=\"0\" y1=\"252\" x2=\"1500\" y2=\"252\" class=\"gmin\"/><line x1=\"0\" y1=\"258\" x2=\"1500\" y2=\"258\" class=\"gmin\"/><line x1=\"0\" y1=\"264\" x2=\"1500\" y2=\"264\" class=\"gmin\"/><line x1=\"0\" y1=\"270\" x2=\"1500\" y2=\"270\" class=\"gmaj\"/><line x1=\"0\" y1=\"276\" x2=\"1500\" y2=\"276\" class=\"gmin\"/><line x1=\"0\" y1=\"282\" x2=\"1500\" y2=\"282\" class=\"gmin\"/><line x1=\"0\" y1=\"288\" x2=\"1500\" y2=\"288\" class=\"gmin\"/><line x1=\"0\" y1=\"294\" x2=\"1500\" y2=\"294\" class=\"gmin\"/><line x1=\"0\" y1=\"300\" x2=\"1500\" y2=\"300\" class=\"gmaj\"/><line x1=\"0\" y1=\"306\" x2=\"1500\" y2=\"306\" class=\"gmin\"/><line x1=\"0\" y1=\"312\" x2=\"1500\" y2=\"312\" class=\"gmin\"/><line x1=\"0\" y1=\"318\" x2=\"1500\" y2=\"318\" class=\"gmin\"/><line x1=\"0\" y1=\"324\" x2=\"1500\" y2=\"324\" class=\"gmin\"/><line x1=\"0\" y1=\"330\" x2=\"1500\" y2=\"330\" class=\"gmaj\"/><line x1=\"0\" y1=\"336\" x2=\"1500\" y2=\"336\" class=\"gmin\"/><line x1=\"0\" y1=\"342\" x2=\"1500\" y2=\"342\" class=\"gmin\"/><line x1=\"0\" y1=\"348\" x2=\"1500\" y2=\"348\" class=\"gmin\"/><line x1=\"0\" y1=\"354\" x2=\"1500\" y2=\"354\" class=\"gmin\"/><line x1=\"0\" y1=\"360\" x2=\"1500\" y2=\"360\" class=\"gmaj\"/><line x1=\"0\" y1=\"366\" x2=\"1500\" y2=\"366\" class=\"gmin\"/><line x1=\"0\" y1=\"372\" x2=\"1500\" y2=\"372\" class=\"gmin\"/><line x1=\"0\" y1=\"378\" x2=\"1500\" y2=\"378\" class=\"gmin\"/><line x1=\"0\" y1=\"384\" x2=\"1500\" y2=\"384\" class=\"gmin\"/><line x1=\"0\" y1=\"390\" x2=\"1500\" y2=\"390\" class=\"gmaj\"/><line x1=\"0\" y1=\"396\" x2=\"1500\" y2=\"396\" class=\"gmin\"/><line x1=\"0\" y1=\"402\" x2=\"1500\" y2=\"402\" class=\"gmin\"/><line x1=\"0\" y1=\"408\" x2=\"1500\" y2=\"408\" class=\"gmin\"/><line x1=\"0\" y1=\"414\" x2=\"1500\" y2=\"414\" class=\"gmin\"/><line x1=\"0\" y1=\"420\" x2=\"1500\" y2=\"420\" class=\"gmaj\"/><line x1=\"0\" y1=\"426\" x2=\"1500\" y2=\"426\" class=\"gmin\"/><line x1=\"0\" y1=\"432\" x2=\"1500\" y2=\"432\" class=\"gmin\"/><line x1=\"0\" y1=\"438\" x2=\"1500\" y2=\"438\" class=\"gmin\"/><polyline class=\"trace\" points=\"0.0,51.9 1.5,50.5 3.0,49.5 4.5,50.7 6.0,52.1 7.5,53.8 9.0,54.8 10.5,55.7 12.0,57.5 13.5,58.6 15.0,59.4 16.5,59.7 18.0,59.8 19.5,60.2 21.0,60.5 22.5,60.6 24.0,60.9 25.5,61.3 27.0,62.0 28.5,62.4 30.0,62.1 31.5,61.2 33.0,59.1 34.5,58.3 36.0,58.5 37.5,58.2 39.0,58.4 40.5,58.0 42.0,58.4 43.5,60.0 45.0,61.4 46.5,62.4 48.0,62.8 49.5,63.0 51.0,63.0 52.5,64.0 54.0,63.5 55.5,65.2 57.0,60.9 58.5,42.2 60.0,10.2 61.5,-0.9 63.0,38.5 64.5,63.2 66.0,63.1 67.5,66.4 69.0,63.4 70.5,63.5 72.0,63.3 73.5,63.0 75.0,62.9 76.5,61.9 78.0,61.8 79.5,61.0 81.0,60.7 82.5,60.1 84.0,60.0 85.5,59.4 87.0,58.7 88.5,57.4 90.0,55.6 91.5,55.6 93.0,56.5 94.5,57.1 96.0,58.1 97.5,58.7 99.0,60.0 100.5,61.7 102.0,62.2 103.5,62.3 105.0,62.6 106.5,62.8 108.0,63.0 109.5,63.1 111.0,63.3 112.5,63.6 114.0,63.8 115.5,64.2 117.0,64.9 118.5,63.7 120.0,62.1 121.5,61.9 123.0,61.6 124.5,61.6 126.0,62.0 127.5,62.5 129.0,63.2 130.5,63.7 132.0,64.3 133.5,64.9 135.0,65.2 136.5,65.9 138.0,66.3 139.5,67.2 141.0,67.2 142.5,66.4 144.0,63.1 145.5,47.0 147.0,11.1 148.5,1.6 150.0,46.4 151.5,69.4 153.0,62.7 154.5,64.4 156.0,63.7 157.5,64.0 159.0,64.0 160.5,63.5 162.0,63.1 163.5,62.0 165.0,61.7 166.5,60.6 168.0,60.2 169.5,59.2 171.0,58.6 172.5,58.3 174.0,56.8 175.5,55.0 177.0,53.9 178.5,54.1 180.0,54.9 181.5,55.5 183.0,56.4 184.5,58.5 186.0,60.5 187.5,61.5 189.0,62.2 190.5,62.9 192.0,63.6 193.5,64.0 195.0,63.7 196.5,63.4 198.0,63.3 199.5,63.0 201.0,62.7 202.5,62.5 204.0,62.1 205.5,61.8 207.0,61.6 208.5,61.5 210.0,60.7 211.5,60.1 213.0,60.3 214.5,60.4 216.0,60.3 217.5,61.5 219.0,63.3 220.5,63.2 222.0,63.7 223.5,63.3 225.0,63.9 226.5,64.0 228.0,64.5 229.5,64.6 231.0,56.2 232.5,31.1 234.0,0.1 235.5,24.5 237.0,66.3 238.5,66.0 240.0,64.8 241.5,64.6 243.0,62.5 244.5,63.4 246.0,62.3 247.5,62.1 249.0,60.8 250.5,60.3 252.0,59.4 253.5,59.1 255.0,58.6 256.5,57.9 258.0,57.7 259.5,56.8 261.0,54.6 262.5,53.6 264.0,53.9 265.5,53.7 267.0,54.1 268.5,54.3 270.0,55.7 271.5,59.7 273.0,61.9 274.5,62.2 276.0,62.5 277.5,62.5 279.0,62.7 280.5,62.8 282.0,63.0 283.5,62.7 285.0,62.1 286.5,61.8 288.0,61.3 289.5,62.2 291.0,63.1 292.5,62.1 294.0,61.7 295.5,61.6 297.0,62.0 298.5,63.1 300.0,62.5 301.5,61.8 303.0,62.8 304.5,64.1 306.0,65.1 307.5,66.4 309.0,66.4 310.5,65.9 312.0,65.5 313.5,64.3 315.0,64.4 316.5,59.4 318.0,35.1 319.5,8.0 321.0,24.0 322.5,60.5 324.0,69.4 325.5,67.7 327.0,67.3 328.5,66.1 330.0,65.8 331.5,65.1 333.0,64.9 334.5,64.5 336.0,64.3 337.5,63.9 339.0,63.3 340.5,63.0 342.0,62.4 343.5,61.9 345.0,60.8 346.5,59.3 348.0,58.1 349.5,57.3 351.0,57.7 352.5,58.6 354.0,59.4 355.5,60.3 357.0,61.2 358.5,62.2 360.0,63.3 361.5,64.2 363.0,64.4 364.5,64.7 366.0,65.1 367.5,64.9 369.0,64.7 370.5,64.2 372.0,64.0 373.5,63.4\"/><polyline class=\"trace\" points=\"375.0,65.8 376.5,67.0 378.0,67.8 379.5,66.9 381.0,66.1 382.5,65.0 384.0,64.4 385.5,63.7 387.0,62.1 388.5,61.2 390.0,60.6 391.5,60.3 393.0,60.1 394.5,59.7 396.0,59.4 397.5,59.3 399.0,59.1 400.5,58.8 402.0,58.3 403.5,58.1 405.0,58.6 406.5,59.7 408.0,61.8 409.5,62.5 411.0,62.3 412.5,62.5 414.0,62.2 415.5,62.4 417.0,62.0 418.5,60.3 420.0,59.0 421.5,58.0 423.0,57.6 424.5,57.4 426.0,57.6 427.5,56.9 429.0,57.3 430.5,56.4 432.0,58.9 433.5,70.7 435.0,90.8 436.5,103.0 438.0,79.7 439.5,57.3 441.0,57.4 442.5,56.7 444.0,57.8 445.5,58.0 447.0,57.7 448.5,57.9 450.0,57.8 451.5,58.5 453.0,58.6 454.5,59.1 456.0,59.4 457.5,59.7 459.0,59.9 460.5,60.6 462.0,61.2 463.5,62.5 465.0,64.3 466.5,64.3 468.0,63.6 469.5,63.1 471.0,62.4 472.5,62.0 474.0,60.9 475.5,59.3 477.0,58.9 478.5,58.9 480.0,58.8 481.5,58.7 483.0,58.5 484.5,58.6 486.0,58.6 487.5,58.4 489.0,58.3 490.5,58.1 492.0,57.8 493.5,59.4 495.0,60.9 496.5,61.1 498.0,61.4 499.5,61.5 501.0,61.0 502.5,60.6 504.0,60.1 505.5,59.6 507.0,59.1 508.5,58.6 510.0,58.4 511.5,57.9 513.0,57.7 514.5,57.0 516.0,57.1 517.5,57.8 519.0,60.3 520.5,70.2 522.0,92.4 523.5,103.6 525.0,77.4 526.5,57.5 528.0,60.4 529.5,59.6 531.0,59.7 532.5,59.7 534.0,59.5 535.5,60.0 537.0,60.3 538.5,61.0 540.0,61.2 541.5,61.9 543.0,62.3 544.5,63.0 546.0,63.5 547.5,63.8 549.0,65.2 550.5,67.0 552.0,68.1 553.5,68.1 555.0,67.6 556.5,67.2 558.0,66.7 559.5,65.5 561.0,63.9 562.5,63.0 564.0,62.3 565.5,61.8 567.0,61.1 568.5,60.8 570.0,61.2 571.5,61.5 573.0,61.7 574.5,62.0 576.0,62.2 577.5,62.7 579.0,63.3 580.5,63.7 582.0,64.1 583.5,64.3 585.0,65.1 586.5,65.6 588.0,65.4 589.5,65.2 591.0,65.1 592.5,63.9 594.0,62.1 595.5,62.0 597.0,61.5 598.5,61.6 600.0,61.3 601.5,61.0 603.0,61.2 604.5,61.1 606.0,67.3 607.5,82.5 609.0,104.8 610.5,95.7 612.0,65.1 613.5,60.7 615.0,62.0 616.5,61.3 618.0,62.5 619.5,61.6 621.0,62.3 622.5,62.7 624.0,63.5 625.5,64.0 627.0,64.6 628.5,65.1 630.0,65.4 631.5,66.1 633.0,66.3 634.5,67.2 636.0,69.5 637.5,70.6 639.0,70.5 640.5,70.8 642.0,70.5 643.5,70.6 645.0,69.6 646.5,66.5 648.0,64.5 649.5,64.0 651.0,63.6 652.5,63.4 654.0,63.1 655.5,62.8 657.0,62.7 658.5,62.9 660.0,63.4 661.5,63.7 663.0,64.1 664.5,63.8 666.0,63.6 667.5,64.8 669.0,65.4 670.5,65.7 672.0,65.4 673.5,64.5 675.0,64.5 676.5,64.5 678.0,63.5 679.5,62.4 681.0,61.4 682.5,60.3 684.0,60.3 685.5,60.7 687.0,60.9 688.5,61.7 690.0,61.6 691.5,66.0 693.0,81.0 694.5,100.7 696.0,96.0 697.5,67.9 699.0,57.5 700.5,59.4 702.0,59.2 703.5,60.3 705.0,60.4 706.5,60.8 708.0,60.9 709.5,61.1 711.0,61.2 712.5,61.5 714.0,62.0 715.5,62.2 717.0,62.7 718.5,63.1 720.0,64.2 721.5,65.7 723.0,66.9 724.5,67.8 726.0,67.5 727.5,66.7 729.0,66.1 730.5,65.4 732.0,64.6 733.5,63.7 735.0,62.7 736.5,62.1 738.0,61.9 739.5,61.7 741.0,61.5 742.5,61.5 744.0,61.6 745.5,62.1 747.0,62.2 748.5,62.6\"/><polyline class=\"trace\" points=\"750.0,18.8 751.5,20.1 753.0,21.9 754.5,23.2 756.0,24.6 757.5,26.4 759.0,28.1 760.5,28.7 762.0,29.1 763.5,29.7 765.0,30.0 766.5,30.6 768.0,31.0 769.5,31.6 771.0,32.1 772.5,32.5 774.0,33.1 775.5,33.5 777.0,34.0 778.5,34.4 780.0,35.1 781.5,35.7 783.0,36.2 784.5,36.9 786.0,37.1 787.5,39.4 789.0,41.8 790.5,41.8 792.0,41.7 793.5,41.7 795.0,41.4 796.5,41.6 798.0,41.7 799.5,41.8 801.0,42.0 802.5,41.5 804.0,42.3 805.5,41.3 807.0,47.5 808.5,62.4 810.0,88.5 811.5,109.3 813.0,91.5 814.5,65.6 816.0,51.9 817.5,44.4 819.0,43.6 820.5,42.7 822.0,42.8 823.5,42.4 825.0,42.2 826.5,42.1 828.0,41.8 829.5,41.8 831.0,41.8 832.5,41.6 834.0,40.5 835.5,40.2 837.0,40.6 838.5,40.7 840.0,41.3 841.5,42.7 843.0,45.1 844.5,47.2 846.0,47.8 847.5,48.1 849.0,48.6 850.5,48.9 852.0,49.4 853.5,49.9 855.0,50.4 856.5,50.8 858.0,51.3 859.5,51.4 861.0,51.4 862.5,51.6 864.0,51.7 865.5,51.7 867.0,52.0 868.5,52.2 870.0,52.5 871.5,52.8 873.0,53.3 874.5,55.3 876.0,56.2 877.5,56.2 879.0,56.2 880.5,56.5 882.0,56.4 883.5,56.7 885.0,57.0 886.5,57.0 888.0,57.6 889.5,57.1 891.0,58.3 892.5,56.5 894.0,60.4 895.5,75.4 897.0,103.0 898.5,123.6 900.0,103.3 901.5,77.8 903.0,65.7 904.5,57.9 906.0,57.0 907.5,55.9 909.0,56.1 910.5,55.8 912.0,55.6 913.5,55.6 915.0,55.2 916.5,55.2 918.0,54.9 919.5,54.7 921.0,54.4 922.5,54.6 924.0,55.1 925.5,55.6 927.0,56.1 928.5,57.3 930.0,58.8 931.5,59.8 933.0,60.7 934.5,61.4 936.0,61.6 937.5,62.0 939.0,62.3 940.5,62.7 942.0,62.7 943.5,62.4 945.0,62.2 946.5,62.0 948.0,61.7 949.5,61.6 951.0,61.9 952.5,61.9 954.0,61.9 955.5,62.2 957.0,62.1 958.5,62.5 960.0,63.9 961.5,64.5 963.0,64.7 964.5,64.9 966.0,65.0 967.5,65.3 969.0,64.9 970.5,65.1 972.0,64.7 973.5,65.1 975.0,64.6 976.5,65.1 978.0,64.3 979.5,63.5 981.0,73.0 982.5,91.9 984.0,120.8 985.5,121.3 987.0,93.4 988.5,77.5 990.0,67.6 991.5,64.7 993.0,64.5 994.5,63.4 996.0,63.6 997.5,63.0 999.0,63.1 1000.5,62.6 1002.0,62.5 1003.5,62.3 1005.0,62.0 1006.5,61.9 1008.0,61.6 1009.5,61.3 1011.0,61.3 1012.5,62.2 1014.0,63.2 1015.5,64.0 1017.0,64.9 1018.5,65.3 1020.0,65.7 1021.5,66.1 1023.0,66.6 1024.5,66.9 1026.0,67.0 1027.5,67.2 1029.0,67.4 1030.5,67.5 1032.0,67.7 1033.5,67.9 1035.0,67.9 1036.5,68.0 1038.0,68.2 1039.5,68.1 1041.0,68.4 1042.5,68.8 1044.0,69.1 1045.5,70.8 1047.0,71.6 1048.5,71.4 1050.0,71.5 1051.5,71.1 1053.0,71.2 1054.5,71.0 1056.0,71.0 1057.5,70.7 1059.0,71.1 1060.5,70.7 1062.0,71.0 1063.5,70.5 1065.0,69.7 1066.5,79.1 1068.0,97.5 1069.5,123.9 1071.0,127.0 1072.5,100.8 1074.0,83.0 1075.5,73.2 1077.0,69.0 1078.5,68.4 1080.0,67.8 1081.5,68.0 1083.0,67.4 1084.5,67.4 1086.0,67.1 1087.5,66.7 1089.0,66.4 1090.5,66.0 1092.0,65.9 1093.5,66.0 1095.0,66.3 1096.5,66.3 1098.0,66.6 1099.5,66.6 1101.0,67.0 1102.5,69.0 1104.0,70.0 1105.5,70.2 1107.0,70.4 1108.5,70.6 1110.0,70.8 1111.5,71.0 1113.0,71.4 1114.5,71.7 1116.0,72.0 1117.5,72.4 1119.0,72.6 1120.5,72.4 1122.0,72.4 1123.5,72.4\"/><polyline class=\"trace\" points=\"1125.0,52.7 1126.5,52.3 1128.0,51.7 1129.5,51.2 1131.0,51.1 1132.5,52.2 1134.0,54.5 1135.5,57.6 1137.0,60.4 1138.5,61.4 1140.0,62.2 1141.5,62.7 1143.0,62.8 1144.5,63.1 1146.0,63.3 1147.5,63.6 1149.0,63.4 1150.5,63.3 1152.0,63.2 1153.5,63.0 1155.0,63.0 1156.5,61.8 1158.0,60.1 1159.5,59.8 1161.0,59.4 1162.5,59.1 1164.0,59.8 1165.5,60.7 1167.0,61.8 1168.5,62.6 1170.0,63.7 1171.5,64.3 1173.0,64.7 1174.5,65.4 1176.0,65.5 1177.5,66.2 1179.0,64.9 1180.5,65.8 1182.0,60.6 1183.5,42.7 1185.0,15.1 1186.5,16.6 1188.0,68.4 1189.5,91.1 1191.0,75.1 1192.5,67.8 1194.0,66.1 1195.5,65.9 1197.0,64.8 1198.5,64.2 1200.0,63.9 1201.5,63.3 1203.0,63.1 1204.5,62.5 1206.0,61.7 1207.5,60.7 1209.0,59.5 1210.5,57.5 1212.0,55.8 1213.5,54.9 1215.0,55.0 1216.5,55.3 1218.0,55.7 1219.5,55.9 1221.0,57.1 1222.5,60.0 1224.0,61.9 1225.5,63.4 1227.0,64.5 1228.5,64.8 1230.0,64.9 1231.5,65.1 1233.0,65.3 1234.5,65.4 1236.0,65.2 1237.5,65.0 1239.0,64.8 1240.5,64.6 1242.0,64.5 1243.5,64.3 1245.0,63.7 1246.5,62.9 1248.0,62.9 1249.5,63.1 1251.0,63.4 1252.5,63.6 1254.0,64.1 1255.5,65.1 1257.0,66.3 1258.5,66.6 1260.0,66.7 1261.5,67.4 1263.0,67.2 1264.5,68.2 1266.0,66.6 1267.5,67.4 1269.0,62.1 1270.5,41.4 1272.0,18.2 1273.5,21.4 1275.0,68.6 1276.5,92.7 1278.0,76.9 1279.5,68.2 1281.0,66.2 1282.5,66.0 1284.0,65.7 1285.5,65.2 1287.0,64.1 1288.5,63.1 1290.0,62.9 1291.5,62.2 1293.0,61.5 1294.5,59.9 1296.0,58.7 1297.5,57.0 1299.0,54.7 1300.5,53.8 1302.0,53.1 1303.5,53.1 1305.0,53.9 1306.5,54.4 1308.0,55.3 1309.5,56.7 1311.0,59.0 1312.5,61.4 1314.0,62.1 1315.5,62.0 1317.0,62.2 1318.5,62.4 1320.0,62.4 1321.5,62.1 1323.0,62.0 1324.5,62.1 1326.0,62.1 1327.5,62.1 1329.0,62.0 1330.5,61.2 1332.0,60.3 1333.5,59.7 1335.0,59.1 1336.5,58.9 1338.0,59.2 1339.5,59.8 1341.0,60.9 1342.5,61.6 1344.0,62.8 1345.5,63.5 1347.0,64.2 1348.5,63.6 1350.0,64.0 1351.5,63.9 1353.0,63.4 1354.5,62.3 1356.0,46.4 1357.5,19.9 1359.0,-1.1 1360.5,31.3 1362.0,81.4 1363.5,79.7 1365.0,67.0 1366.5,62.4 1368.0,61.3 1369.5,61.6 1371.0,60.6 1372.5,61.0 1374.0,60.2 1375.5,60.3 1377.0,59.6 1378.5,59.3 1380.0,58.2 1381.5,55.7 1383.0,53.8 1384.5,52.0 1386.0,50.9 1387.5,51.1 1389.0,51.4 1390.5,51.7 1392.0,52.1 1393.5,52.3 1395.0,53.3 1396.5,55.3 1398.0,58.1 1399.5,60.0 1401.0,60.3 1402.5,60.7 1404.0,61.1 1405.5,61.5 1407.0,61.9 1408.5,62.0 1410.0,62.1 1411.5,62.3 1413.0,62.5 1414.5,61.5 1416.0,59.1 1417.5,58.3 1419.0,58.6 1420.5,58.2 1422.0,58.2 1423.5,58.0 1425.0,59.0 1426.5,61.0 1428.0,61.6 1429.5,62.1 1431.0,62.1 1432.5,62.8 1434.0,62.5 1435.5,63.3 1437.0,63.3 1438.5,63.9 1440.0,62.3 1441.5,44.8 1443.0,18.9 1444.5,-8.0 1446.0,23.5 1447.5,81.0 1449.0,79.9 1450.5,68.5 1452.0,64.5 1453.5,62.5 1455.0,63.2 1456.5,61.9 1458.0,62.4 1459.5,61.4 1461.0,61.6 1462.5,60.4 1464.0,59.2 1465.5,58.5 1467.0,57.4 1468.5,56.1 1470.0,53.5 1471.5,51.5 1473.0,51.2 1474.5,51.3 1476.0,51.6 1477.5,51.5 1479.0,52.6 1480.5,55.2 1482.0,57.5 1483.5,60.0 1485.0,62.2 1486.5,62.8 1488.0,63.0 1489.5,63.3 1491.0,63.5 1492.5,63.9 1494.0,63.6 1495.5,63.4 1497.0,63.1 1498.5,62.8\"/><polyline class=\"trace\" points=\"0.0,173.2 1.5,172.3 3.0,171.7 4.5,172.3 6.0,172.4 7.5,172.9 9.0,173.1 10.5,173.7 12.0,175.0 13.5,175.8 15.0,176.1 16.5,176.4 18.0,176.7 19.5,177.0 21.0,177.4 22.5,177.5 24.0,177.7 25.5,177.8 27.0,178.1 28.5,178.1 30.0,177.4 31.5,176.1 33.0,174.0 34.5,173.4 36.0,173.7 37.5,173.6 39.0,174.0 40.5,173.8 42.0,174.3 43.5,176.0 45.0,177.3 46.5,178.4 48.0,178.8 49.5,178.8 51.0,178.6 52.5,178.8 54.0,178.6 55.5,178.8 57.0,178.1 58.5,173.1 60.0,164.9 61.5,151.5 63.0,158.8 64.5,178.9 66.0,178.8 67.5,176.8 69.0,177.7 70.5,177.3 72.0,178.0 73.5,177.9 75.0,178.2 76.5,177.7 78.0,177.7 79.5,177.5 81.0,177.3 82.5,177.2 84.0,177.0 85.5,176.2 87.0,175.6 88.5,174.2 90.0,172.5 91.5,172.5 93.0,173.0 94.5,173.3 96.0,173.8 97.5,174.0 99.0,174.9 100.5,176.4 102.0,176.7 103.5,176.6 105.0,176.6 106.5,176.6 108.0,176.6 109.5,176.4 111.0,176.2 112.5,176.3 114.0,176.2 115.5,176.3 117.0,176.2 118.5,174.3 120.0,172.6 121.5,172.6 123.0,172.2 124.5,172.2 126.0,172.6 127.5,172.9 129.0,173.4 130.5,173.7 132.0,174.1 133.5,174.4 135.0,174.6 136.5,174.9 138.0,174.9 139.5,175.5 141.0,175.2 142.5,174.7 144.0,173.1 145.5,169.2 147.0,160.7 148.5,147.9 150.0,155.5 151.5,172.3 153.0,173.1 154.5,173.1 156.0,173.5 157.5,173.4 159.0,173.8 160.5,173.1 162.0,173.1 163.5,172.6 165.0,172.5 166.5,172.2 168.0,171.9 169.5,171.4 171.0,171.0 172.5,170.7 174.0,169.4 175.5,167.7 177.0,166.6 178.5,166.3 180.0,166.6 181.5,166.8 183.0,166.9 184.5,167.2 186.0,168.3 187.5,169.3 189.0,169.8 190.5,170.3 192.0,170.9 193.5,171.1 195.0,170.7 196.5,170.4 198.0,170.1 199.5,169.7 201.0,169.4 202.5,168.9 204.0,168.1 205.5,167.4 207.0,166.9 208.5,166.5 210.0,165.7 211.5,165.3 213.0,165.6 214.5,165.9 216.0,166.1 217.5,167.4 219.0,169.3 220.5,169.5 222.0,169.9 223.5,170.1 225.0,170.4 226.5,170.7 228.0,169.9 229.5,169.9 231.0,165.9 232.5,160.6 234.0,147.1 235.5,140.9 237.0,160.3 238.5,169.5 240.0,168.0 241.5,169.5 243.0,169.1 244.5,170.1 246.0,169.8 247.5,169.3 249.0,168.9 250.5,168.3 252.0,168.0 253.5,167.5 255.0,167.2 256.5,166.7 258.0,166.5 259.5,165.6 261.0,163.0 262.5,161.8 264.0,161.9 265.5,161.5 267.0,161.5 268.5,161.2 270.0,161.7 271.5,164.0 273.0,165.7 274.5,166.5 276.0,166.9 277.5,167.4 279.0,167.7 280.5,168.1 282.0,168.4 283.5,168.2 285.0,167.8 286.5,167.5 288.0,167.1 289.5,166.9 291.0,166.3 292.5,165.0 294.0,164.2 295.5,163.8 297.0,163.9 298.5,164.6 300.0,165.3 301.5,166.0 303.0,166.8 304.5,167.9 306.0,168.7 307.5,169.8 309.0,169.8 310.5,169.5 312.0,169.5 313.5,168.9 315.0,169.0 316.5,165.4 318.0,159.7 319.5,147.3 321.0,140.8 322.5,160.3 324.0,172.4 325.5,170.2 327.0,171.0 328.5,170.0 330.0,170.1 331.5,170.0 333.0,169.9 334.5,170.1 336.0,169.9 337.5,169.9 339.0,169.4 340.5,169.3 342.0,168.9 343.5,168.6 345.0,167.5 346.5,166.0 348.0,164.8 349.5,163.9 351.0,164.0 352.5,164.6 354.0,165.1 355.5,165.6 357.0,166.2 358.5,166.9 360.0,167.8 361.5,168.4 363.0,168.5 364.5,168.5 366.0,168.8 367.5,168.8 369.0,168.7 370.5,168.5 372.0,168.3 373.5,168.1\"/><polyline class=\"trace\" points=\"375.0,159.2 376.5,158.4 378.0,157.6 379.5,158.5 381.0,159.9 382.5,161.3 384.0,162.3 385.5,162.9 387.0,163.9 388.5,164.7 390.0,165.3 391.5,165.4 393.0,165.4 394.5,165.6 396.0,165.8 397.5,165.9 399.0,166.0 400.5,166.3 402.0,166.9 403.5,167.3 405.0,167.4 406.5,167.1 408.0,166.1 409.5,165.6 411.0,165.6 412.5,165.3 414.0,165.4 415.5,165.1 417.0,165.3 418.5,165.9 420.0,166.8 421.5,167.1 423.0,167.4 424.5,167.6 426.0,167.7 427.5,168.6 429.0,168.2 430.5,169.9 432.0,165.8 433.5,149.7 435.0,121.8 436.5,117.4 438.0,153.1 439.5,167.7 441.0,167.7 442.5,172.0 444.0,168.5 445.5,168.9 447.0,168.3 448.5,168.0 450.0,167.8 451.5,166.9 453.0,166.9 454.5,166.2 456.0,166.0 457.5,165.4 459.0,165.4 460.5,165.3 462.0,164.9 463.5,164.2 465.0,163.3 466.5,163.4 468.0,163.9 469.5,164.5 471.0,165.1 472.5,165.7 474.0,166.5 475.5,167.5 477.0,167.8 478.5,168.0 480.0,168.3 481.5,168.4 483.0,168.7 484.5,168.9 486.0,169.1 487.5,169.4 489.0,169.6 490.5,170.0 492.0,170.8 493.5,170.6 495.0,169.8 496.5,169.6 498.0,169.5 499.5,169.5 501.0,169.6 502.5,170.0 504.0,170.5 505.5,170.8 507.0,171.3 508.5,171.7 510.0,171.9 511.5,172.4 513.0,172.8 514.5,173.4 516.0,173.6 517.5,173.1 519.0,170.5 520.5,156.4 522.0,124.8 523.5,121.8 525.0,162.6 526.5,177.3 528.0,170.2 529.5,171.9 531.0,171.0 532.5,171.3 534.0,171.0 535.5,170.9 537.0,170.5 538.5,169.7 540.0,169.4 541.5,168.6 543.0,168.2 544.5,167.4 546.0,167.1 547.5,166.9 549.0,166.1 550.5,165.1 552.0,164.7 553.5,165.0 555.0,165.6 556.5,166.2 558.0,167.0 559.5,168.9 561.0,170.3 562.5,170.8 564.0,171.3 565.5,171.7 567.0,172.2 568.5,172.4 570.0,172.3 571.5,172.2 573.0,172.2 574.5,172.2 576.0,172.0 577.5,172.1 579.0,172.0 580.5,172.0 582.0,172.1 583.5,172.3 585.0,171.9 586.5,171.5 588.0,171.4 589.5,171.4 591.0,171.3 592.5,171.8 594.0,172.6 595.5,172.5 597.0,172.8 598.5,172.3 600.0,172.7 601.5,172.5 603.0,173.5 604.5,173.7 606.0,167.3 607.5,144.8 609.0,120.5 610.5,148.1 612.0,180.1 613.5,175.2 615.0,174.7 616.5,173.8 618.0,172.0 619.5,172.3 621.0,171.4 622.5,171.4 624.0,170.3 625.5,170.1 627.0,169.4 628.5,169.3 630.0,169.0 631.5,168.6 633.0,168.4 634.5,168.1 636.0,167.1 637.5,166.6 639.0,166.9 640.5,166.9 642.0,167.3 643.5,167.7 645.0,168.9 646.5,171.7 648.0,173.0 649.5,172.9 651.0,173.0 652.5,172.8 654.0,172.8 655.5,172.7 657.0,172.7 658.5,172.6 660.0,172.2 661.5,172.0 663.0,171.8 664.5,172.8 666.0,173.9 667.5,173.7 669.0,173.5 670.5,173.7 672.0,174.0 673.5,174.8 675.0,173.8 676.5,172.9 678.0,173.5 679.5,174.1 681.0,174.7 682.5,175.5 684.0,175.5 685.5,175.2 687.0,174.7 688.5,173.9 690.0,173.9 691.5,170.8 693.0,149.3 694.5,128.4 696.0,147.6 697.5,174.3 699.0,177.2 700.5,176.5 702.0,175.8 703.5,175.0 705.0,174.7 706.5,174.1 708.0,174.0 709.5,173.4 711.0,173.3 712.5,172.9 714.0,172.6 715.5,172.3 717.0,171.9 718.5,171.6 720.0,171.0 721.5,170.4 723.0,169.7 724.5,169.3 726.0,169.6 727.5,170.3 729.0,170.8 730.5,171.5 732.0,172.0 733.5,172.8 735.0,173.4 736.5,174.0 738.0,174.1 739.5,174.4 741.0,174.7 742.5,174.4 744.0,174.3 745.5,173.9 747.0,173.8 748.5,173.3\"/><polyline class=\"trace\" points=\"750.0,151.3 751.5,151.2 753.0,150.9 754.5,153.8 756.0,158.1 757.5,163.5 759.0,169.7 760.5,174.3 762.0,176.6 763.5,177.6 765.0,178.2 766.5,178.8 768.0,179.2 769.5,179.7 771.0,180.1 772.5,180.6 774.0,180.9 775.5,180.6 777.0,180.1 778.5,179.6 780.0,179.1 781.5,179.0 783.0,179.3 784.5,179.7 786.0,179.8 787.5,180.2 789.0,180.3 790.5,181.6 792.0,183.1 793.5,183.4 795.0,183.4 796.5,183.3 798.0,183.5 799.5,183.2 801.0,183.6 802.5,183.1 804.0,183.7 805.5,183.4 807.0,191.7 808.5,212.2 810.0,230.7 811.5,260.0 813.0,266.0 814.5,228.1 816.0,196.6 817.5,183.8 819.0,179.4 820.5,179.2 822.0,178.5 823.5,176.5 825.0,174.2 826.5,174.5 828.0,174.1 829.5,172.6 831.0,170.1 832.5,168.0 834.0,164.7 835.5,159.8 837.0,157.2 838.5,156.6 840.0,155.9 841.5,157.6 843.0,161.7 844.5,166.3 846.0,173.1 847.5,177.6 849.0,179.7 850.5,182.1 852.0,184.0 853.5,185.1 855.0,184.6 856.5,184.4 858.0,184.1 859.5,183.8 861.0,183.6 862.5,183.4 864.0,183.4 865.5,183.4 867.0,183.4 868.5,183.3 870.0,183.6 871.5,183.9 873.0,184.1 874.5,184.5 876.0,184.6 877.5,185.2 879.0,185.8 880.5,186.4 882.0,186.5 883.5,186.3 885.0,186.2 886.5,185.8 888.0,186.0 889.5,185.5 891.0,186.2 892.5,185.1 894.0,189.7 895.5,207.4 897.0,232.3 898.5,262.0 900.0,265.5 901.5,230.7 903.0,196.5 904.5,181.9 906.0,178.6 907.5,177.7 909.0,176.8 910.5,176.1 912.0,174.6 913.5,173.0 915.0,172.2 916.5,171.3 918.0,168.1 919.5,163.6 921.0,160.5 922.5,156.9 924.0,153.7 925.5,153.1 927.0,152.8 928.5,151.9 930.0,153.4 931.5,159.0 933.0,164.2 934.5,167.8 936.0,171.1 937.5,172.4 939.0,172.2 940.5,172.3 942.0,172.3 943.5,172.3 945.0,172.2 946.5,171.9 948.0,171.6 949.5,171.4 951.0,171.1 952.5,170.8 954.0,170.5 955.5,170.1 957.0,169.8 958.5,169.6 960.0,169.6 961.5,169.3 963.0,169.2 964.5,169.5 966.0,169.6 967.5,169.9 969.0,169.9 970.5,170.3 972.0,170.0 973.5,169.5 975.0,168.7 976.5,168.0 978.0,168.4 979.5,166.9 981.0,176.7 982.5,195.2 984.0,222.6 985.5,244.8 987.0,227.1 988.5,193.5 990.0,170.7 991.5,162.0 993.0,162.0 994.5,160.7 996.0,160.2 997.5,159.5 999.0,158.1 1000.5,156.0 1002.0,153.9 1003.5,152.2 1005.0,150.7 1006.5,148.2 1008.0,145.3 1009.5,142.5 1011.0,140.5 1012.5,140.4 1014.0,140.8 1015.5,141.5 1017.0,144.4 1018.5,150.3 1020.0,154.9 1021.5,158.3 1023.0,161.2 1024.5,162.3 1026.0,162.4 1027.5,162.4 1029.0,162.7 1030.5,162.7 1032.0,162.6 1033.5,162.4 1035.0,162.2 1036.5,162.1 1038.0,161.9 1039.5,161.7 1041.0,162.1 1042.5,162.7 1044.0,163.2 1045.5,163.7 1047.0,164.3 1048.5,164.5 1050.0,165.3 1051.5,166.3 1053.0,166.3 1054.5,165.8 1056.0,165.7 1057.5,165.4 1059.0,165.1 1060.5,165.1 1062.0,165.0 1063.5,165.9 1065.0,166.4 1066.5,174.7 1068.0,193.4 1069.5,218.7 1071.0,239.7 1072.5,225.1 1074.0,190.0 1075.5,170.1 1077.0,163.1 1078.5,161.1 1080.0,160.3 1081.5,159.7 1083.0,159.4 1084.5,158.5 1086.0,157.8 1087.5,156.9 1089.0,154.3 1090.5,151.3 1092.0,148.8 1093.5,146.6 1095.0,143.3 1096.5,140.2 1098.0,139.2 1099.5,138.9 1101.0,143.0 1102.5,147.7 1104.0,151.8 1105.5,157.4 1107.0,161.0 1108.5,164.0 1110.0,165.5 1111.5,166.1 1113.0,166.5 1114.5,166.2 1116.0,166.3 1117.5,166.3 1119.0,166.3 1120.5,166.2 1122.0,165.9 1123.5,165.7\"/><polyline class=\"trace\" points=\"1125.0,165.9 1126.5,165.6 1128.0,164.8 1129.5,165.1 1131.0,165.6 1132.5,166.1 1134.0,166.6 1135.5,167.0 1137.0,168.2 1138.5,169.0 1140.0,169.2 1141.5,169.5 1143.0,169.8 1144.5,170.0 1146.0,170.3 1147.5,170.4 1149.0,170.4 1150.5,170.4 1152.0,170.4 1153.5,170.4 1155.0,170.0 1156.5,169.5 1158.0,168.9 1159.5,168.4 1161.0,167.9 1162.5,167.2 1164.0,167.5 1165.5,168.0 1167.0,168.6 1168.5,169.5 1170.0,170.6 1171.5,171.7 1173.0,171.9 1174.5,172.0 1176.0,171.7 1177.5,172.2 1179.0,171.6 1180.5,171.8 1182.0,167.7 1183.5,149.1 1185.0,115.8 1186.5,104.7 1188.0,147.9 1189.5,181.4 1191.0,177.6 1192.5,174.1 1194.0,173.6 1195.5,173.5 1197.0,173.2 1198.5,172.8 1200.0,173.1 1201.5,173.1 1203.0,173.2 1204.5,173.1 1206.0,173.1 1207.5,173.1 1209.0,172.5 1210.5,171.7 1212.0,170.6 1213.5,168.4 1215.0,167.9 1216.5,168.3 1218.0,168.4 1219.5,168.7 1221.0,168.9 1222.5,169.2 1224.0,170.1 1225.5,170.8 1227.0,171.8 1228.5,172.7 1230.0,172.8 1231.5,173.0 1233.0,173.2 1234.5,173.4 1236.0,173.4 1237.5,173.1 1239.0,172.6 1240.5,172.3 1242.0,171.9 1243.5,171.5 1245.0,171.1 1246.5,170.6 1248.0,170.2 1249.5,170.4 1251.0,170.8 1252.5,170.9 1254.0,171.3 1255.5,171.4 1257.0,172.1 1258.5,174.3 1260.0,175.2 1261.5,175.3 1263.0,175.0 1264.5,175.6 1266.0,174.8 1267.5,175.4 1269.0,169.5 1270.5,148.2 1272.0,117.6 1273.5,107.2 1275.0,149.4 1276.5,185.1 1278.0,180.2 1279.5,174.7 1281.0,174.3 1282.5,174.0 1284.0,173.7 1285.5,173.3 1287.0,173.1 1288.5,172.6 1290.0,172.4 1291.5,172.0 1293.0,171.7 1294.5,171.4 1296.0,170.8 1297.5,169.8 1299.0,168.4 1300.5,167.9 1302.0,168.0 1303.5,165.4 1305.0,164.1 1306.5,165.0 1308.0,165.6 1309.5,167.2 1311.0,169.0 1312.5,170.3 1314.0,170.8 1315.5,170.8 1317.0,171.1 1318.5,171.2 1320.0,171.4 1321.5,171.1 1323.0,171.0 1324.5,171.0 1326.0,170.7 1327.5,170.8 1329.0,170.6 1330.5,169.4 1332.0,168.3 1333.5,167.8 1335.0,167.1 1336.5,166.6 1338.0,167.1 1339.5,167.8 1341.0,168.6 1342.5,169.1 1344.0,170.0 1345.5,170.5 1347.0,171.7 1348.5,172.0 1350.0,172.3 1351.5,172.6 1353.0,172.0 1354.5,170.6 1356.0,156.0 1357.5,126.0 1359.0,94.6 1360.5,113.8 1362.0,168.1 1363.5,180.6 1365.0,173.1 1366.5,170.9 1368.0,169.5 1369.5,170.1 1371.0,169.5 1372.5,169.6 1374.0,169.5 1375.5,169.4 1377.0,169.0 1378.5,168.5 1380.0,168.2 1381.5,167.7 1383.0,167.1 1384.5,166.2 1386.0,165.4 1387.5,164.5 1389.0,163.8 1390.5,163.8 1392.0,163.9 1393.5,164.2 1395.0,164.3 1396.5,164.8 1398.0,166.5 1399.5,167.7 1401.0,168.1 1402.5,168.8 1404.0,169.3 1405.5,169.9 1407.0,169.9 1408.5,169.6 1410.0,169.5 1411.5,169.2 1413.0,169.0 1414.5,168.7 1416.0,167.5 1417.5,166.8 1419.0,166.8 1420.5,166.5 1422.0,166.4 1423.5,166.2 1425.0,166.5 1426.5,168.2 1428.0,168.9 1429.5,169.5 1431.0,169.6 1432.5,170.1 1434.0,170.4 1435.5,170.7 1437.0,171.3 1438.5,169.8 1440.0,169.6 1441.5,154.9 1443.0,125.0 1444.5,94.3 1446.0,109.9 1447.5,165.4 1449.0,178.0 1450.5,172.0 1452.0,173.9 1453.5,171.9 1455.0,172.8 1456.5,171.6 1458.0,171.8 1459.5,171.3 1461.0,171.1 1462.5,171.0 1464.0,170.5 1465.5,170.6 1467.0,170.2 1468.5,169.8 1470.0,168.3 1471.5,166.6 1473.0,165.6 1474.5,164.8 1476.0,164.6 1477.5,165.1 1479.0,165.4 1480.5,165.9 1482.0,166.9 1483.5,168.3 1485.0,170.1 1486.5,171.1 1488.0,171.4 1489.5,171.7 1491.0,172.1 1492.5,172.1 1494.0,171.7 1495.5,171.4 1497.0,171.3 1498.5,170.9\"/><polyline class=\"trace\" points=\"0.0,290.6 1.5,291.0 3.0,291.4 4.5,290.8 6.0,289.5 7.5,288.3 9.0,287.5 10.5,287.2 12.0,286.7 13.5,286.3 15.0,285.9 16.5,285.9 18.0,286.1 19.5,286.1 21.0,286.1 22.5,286.1 24.0,286.1 25.5,285.7 27.0,285.3 28.5,285.0 30.0,284.5 31.5,284.1 33.0,284.1 34.5,284.4 36.0,284.5 37.5,284.7 39.0,284.8 40.5,285.0 42.0,285.1 43.5,285.3 45.0,285.1 46.5,285.3 48.0,285.1 49.5,285.0 51.0,284.8 52.5,284.0 54.0,284.3 55.5,282.7 57.0,286.5 58.5,300.1 60.0,323.9 61.5,321.6 63.0,289.6 64.5,285.0 66.0,284.8 67.5,279.6 69.0,283.5 70.5,283.0 72.0,283.9 73.5,284.1 75.0,284.5 76.5,285.1 78.0,285.1 79.5,285.7 81.0,285.8 82.5,286.3 84.0,286.2 85.5,286.1 87.0,286.1 88.5,286.0 90.0,286.1 91.5,286.0 93.0,285.7 94.5,285.3 96.0,285.0 97.5,284.5 99.0,284.2 100.5,283.9 102.0,283.7 103.5,283.5 105.0,283.2 106.5,283.0 108.0,282.8 109.5,282.5 111.0,282.3 112.5,282.0 114.0,281.7 115.5,281.4 117.0,280.5 118.5,279.7 120.0,279.7 121.5,279.8 123.0,279.8 124.5,279.8 126.0,279.8 127.5,279.7 129.0,279.4 130.5,279.2 132.0,279.0 133.5,278.7 135.0,278.5 136.5,278.2 138.0,277.9 139.5,277.5 141.0,277.2 142.5,277.5 144.0,279.3 145.5,291.4 147.0,318.8 148.5,315.4 150.0,278.3 151.5,272.1 153.0,279.6 154.5,277.9 156.0,279.0 157.5,278.5 159.0,279.1 160.5,278.8 162.0,279.3 163.5,279.9 165.0,280.0 166.5,280.8 168.0,280.9 169.5,281.5 171.0,281.6 172.5,281.6 174.0,281.8 175.5,281.9 177.0,281.8 178.5,281.5 180.0,280.9 181.5,280.5 183.0,279.7 184.5,277.9 186.0,277.0 187.5,277.0 189.0,276.8 190.5,276.6 192.0,276.5 193.5,276.4 195.0,276.2 196.5,276.2 198.0,276.0 199.5,275.8 201.0,275.9 202.5,275.5 204.0,275.2 205.5,274.9 207.0,274.6 208.5,274.2 210.0,274.2 211.5,274.4 213.0,274.6 214.5,274.8 216.0,274.9 217.5,275.1 219.0,275.2 220.5,275.5 222.0,275.4 223.5,276.0 225.0,275.7 226.5,276.0 228.0,274.6 229.5,274.5 231.0,278.8 232.5,298.7 234.0,316.3 235.5,285.6 237.0,263.2 238.5,272.7 240.0,272.4 241.5,274.2 243.0,275.8 244.5,276.0 246.0,276.7 247.5,276.5 249.0,277.3 250.5,277.2 252.0,277.8 253.5,277.6 255.0,277.8 256.5,278.0 258.0,278.0 259.5,277.9 261.0,277.6 262.5,277.5 264.0,277.2 265.5,277.1 267.0,276.7 268.5,276.1 270.0,275.2 271.5,273.5 273.0,273.1 274.5,273.6 276.0,273.7 277.5,274.0 279.0,274.3 280.5,274.6 282.0,274.7 283.5,274.7 285.0,274.9 286.5,275.0 288.0,275.0 289.5,273.9 291.0,272.5 292.5,272.1 294.0,271.8 295.5,271.5 297.0,271.1 298.5,270.7 300.0,272.0 301.5,273.3 303.0,273.1 304.5,273.0 306.0,272.8 307.5,272.6 309.0,272.7 310.5,272.8 312.0,273.2 313.5,273.8 315.0,273.9 316.5,275.1 318.0,293.8 319.5,308.5 321.0,286.0 322.5,269.1 324.0,272.2 325.5,271.8 327.0,272.9 328.5,273.1 330.0,273.5 331.5,274.1 333.0,274.2 334.5,274.8 336.0,274.9 337.5,275.2 339.0,275.3 340.5,275.5 342.0,275.8 343.5,275.9 345.0,275.9 346.5,275.9 348.0,275.9 349.5,275.9 351.0,275.5 352.5,275.2 354.0,274.9 355.5,274.6 357.0,274.3 358.5,273.9 360.0,273.7 361.5,273.5 363.0,273.3 364.5,273.0 366.0,272.9 367.5,273.2 369.0,273.3 370.5,273.5 372.0,273.6 373.5,273.9\"/><polyline class=\"trace\" points=\"375.0,286.3 376.5,286.0 378.0,286.0 379.5,285.9 381.0,285.4 382.5,285.0 384.0,284.7 385.5,284.8 387.0,285.3 388.5,285.4 390.0,285.4 391.5,285.6 393.0,285.9 394.5,286.0 396.0,286.2 397.5,286.2 399.0,286.3 400.5,286.2 402.0,286.1 403.5,285.9 405.0,285.4 406.5,284.5 408.0,283.5 409.5,283.3 411.0,283.5 412.5,283.5 414.0,283.8 415.5,283.8 417.0,284.1 418.5,285.1 420.0,285.6 421.5,286.2 423.0,286.3 424.5,286.3 426.0,286.1 427.5,285.8 429.0,285.9 430.5,285.1 432.0,286.6 433.5,291.0 435.0,298.8 436.5,290.9 438.0,278.6 439.5,286.3 441.0,286.2 442.5,282.6 444.0,285.0 445.5,284.5 447.0,285.3 448.5,285.4 450.0,285.7 451.5,285.8 453.0,285.8 454.5,286.0 456.0,285.9 457.5,286.2 459.0,286.0 460.5,285.6 462.0,285.3 463.5,284.5 465.0,283.6 466.5,283.6 468.0,283.8 469.5,283.7 471.0,283.8 472.5,283.7 474.0,283.9 475.5,284.5 477.0,284.5 478.5,284.4 480.0,284.3 481.5,284.2 483.0,284.1 484.5,283.8 486.0,283.6 487.5,283.6 489.0,283.4 490.5,283.2 492.0,282.7 493.5,281.4 495.0,280.6 496.5,280.6 498.0,280.4 499.5,280.3 501.0,280.6 502.5,280.7 504.0,280.8 505.5,280.9 507.0,280.9 508.5,281.0 510.0,281.0 511.5,281.0 513.0,280.8 514.5,280.9 516.0,280.6 517.5,280.5 519.0,280.6 520.5,284.7 522.0,294.1 523.5,286.0 525.0,271.3 526.5,276.6 528.0,280.8 529.5,279.9 531.0,280.7 532.5,280.3 534.0,280.8 535.5,280.4 537.0,280.6 538.5,280.6 540.0,280.7 541.5,280.9 543.0,280.8 544.5,280.9 546.0,280.7 547.5,280.6 549.0,280.0 550.5,279.3 552.0,278.6 553.5,278.3 555.0,278.1 556.5,278.0 558.0,277.7 559.5,277.0 561.0,277.1 562.5,277.6 564.0,277.7 565.5,277.9 567.0,278.1 568.5,278.1 570.0,277.8 571.5,277.7 573.0,277.4 574.5,277.2 576.0,277.0 577.5,276.6 579.0,276.1 580.5,275.6 582.0,275.1 583.5,274.8 585.0,274.4 586.5,274.3 588.0,274.5 589.5,274.7 591.0,274.9 592.5,275.6 594.0,276.6 595.5,276.9 597.0,277.0 598.5,277.5 600.0,277.4 601.5,277.8 603.0,276.7 604.5,276.6 606.0,276.7 607.5,284.1 609.0,286.1 610.5,267.7 612.0,266.2 613.5,275.5 615.0,274.6 616.5,276.3 618.0,276.9 619.5,277.4 621.0,277.6 622.5,277.3 624.0,277.5 625.5,277.2 627.0,277.3 628.5,277.0 630.0,276.9 631.5,276.7 633.0,276.6 634.5,276.1 636.0,274.7 637.5,274.1 639.0,274.0 640.5,273.8 642.0,273.5 643.5,273.1 645.0,273.0 646.5,273.2 648.0,273.9 649.5,274.5 651.0,274.8 652.5,275.1 654.0,275.4 655.5,275.8 657.0,276.0 658.5,275.8 660.0,275.8 661.5,275.7 663.0,275.5 664.5,274.8 666.0,273.9 667.5,273.0 669.0,272.4 670.5,272.1 672.0,271.9 673.5,272.1 675.0,273.1 676.5,274.1 678.0,274.4 679.5,274.8 681.0,275.2 682.5,275.6 684.0,275.7 685.5,275.5 687.0,275.7 688.5,275.8 690.0,275.8 691.5,274.6 693.0,281.2 694.5,282.3 696.0,267.9 697.5,269.2 699.0,276.7 700.5,275.4 702.0,276.3 703.5,276.0 705.0,276.2 706.5,276.4 708.0,276.5 709.5,276.9 711.0,276.8 712.5,276.9 714.0,276.8 715.5,276.8 717.0,276.7 718.5,276.7 720.0,276.1 721.5,275.4 723.0,274.8 724.5,274.3 726.0,274.2 727.5,274.3 729.0,274.5 730.5,274.5 732.0,274.6 733.5,274.9 735.0,275.2 736.5,275.4 738.0,275.3 739.5,275.2 741.0,275.2 742.5,275.4 744.0,275.4 745.5,275.4 747.0,275.4 748.5,275.4\"/><polyline class=\"trace\" points=\"750.0,253.9 751.5,252.6 753.0,252.9 754.5,255.5 756.0,258.1 757.5,261.0 759.0,266.4 760.5,272.6 762.0,276.0 763.5,278.2 765.0,278.8 766.5,278.5 768.0,278.7 769.5,278.6 771.0,278.6 772.5,278.7 774.0,279.0 775.5,278.9 777.0,278.9 778.5,278.9 780.0,278.9 781.5,278.6 783.0,278.4 784.5,278.0 786.0,276.6 787.5,276.0 789.0,275.7 790.5,276.6 792.0,279.2 793.5,280.0 795.0,280.2 796.5,282.4 798.0,284.7 799.5,284.2 801.0,283.8 802.5,283.4 804.0,282.8 805.5,282.9 807.0,282.3 808.5,283.8 810.0,286.1 811.5,312.4 813.0,345.4 814.5,329.1 816.0,296.6 817.5,282.9 819.0,279.5 820.5,280.4 822.0,278.2 823.5,275.7 825.0,274.0 826.5,273.2 828.0,273.1 829.5,271.8 831.0,268.9 832.5,267.3 834.0,263.9 835.5,259.5 837.0,257.5 838.5,256.4 840.0,256.6 841.5,255.8 843.0,258.3 844.5,264.1 846.0,269.5 847.5,274.6 849.0,277.5 850.5,279.3 852.0,280.9 853.5,283.1 855.0,284.1 856.5,283.5 858.0,283.2 859.5,282.7 861.0,282.4 862.5,282.1 864.0,281.7 865.5,281.4 867.0,281.1 868.5,280.7 870.0,280.1 871.5,279.5 873.0,279.0 874.5,279.5 876.0,280.0 877.5,280.6 879.0,281.1 880.5,282.1 882.0,284.1 883.5,284.7 885.0,284.6 886.5,284.6 888.0,284.5 889.5,284.7 891.0,284.5 892.5,284.8 894.0,285.0 895.5,285.5 897.0,288.7 898.5,313.0 900.0,344.6 901.5,333.9 903.0,298.6 904.5,282.7 906.0,280.4 907.5,278.8 909.0,277.9 910.5,277.2 912.0,276.0 913.5,275.1 915.0,274.3 916.5,273.3 918.0,270.4 919.5,266.8 921.0,264.0 922.5,260.1 924.0,257.7 925.5,257.0 927.0,256.5 928.5,256.8 930.0,256.9 931.5,261.2 933.0,268.0 934.5,271.5 936.0,273.9 937.5,277.5 939.0,278.5 940.5,278.2 942.0,278.4 943.5,278.2 945.0,278.3 946.5,278.0 948.0,278.0 949.5,278.1 951.0,277.9 952.5,278.1 954.0,277.8 955.5,276.9 957.0,276.1 958.5,275.9 960.0,275.8 961.5,276.0 963.0,275.8 964.5,276.3 966.0,278.6 967.5,279.6 969.0,279.6 970.5,280.5 972.0,281.1 973.5,281.0 975.0,281.1 976.5,280.8 978.0,281.0 979.5,277.6 981.0,276.0 982.5,277.0 984.0,288.9 985.5,325.2 987.0,339.7 988.5,312.2 990.0,284.2 991.5,276.0 993.0,276.5 994.5,275.1 996.0,273.5 997.5,273.3 999.0,272.8 1000.5,270.4 1002.0,268.5 1003.5,267.6 1005.0,265.5 1006.5,261.6 1008.0,257.7 1009.5,254.7 1011.0,252.8 1012.5,252.0 1014.0,252.4 1015.5,252.0 1017.0,253.4 1018.5,260.2 1020.0,265.5 1021.5,269.4 1023.0,273.3 1024.5,275.6 1026.0,277.0 1027.5,277.4 1029.0,277.7 1030.5,278.0 1032.0,278.2 1033.5,278.5 1035.0,278.7 1036.5,279.0 1038.0,279.3 1039.5,277.3 1041.0,274.9 1042.5,275.1 1044.0,275.3 1045.5,275.4 1047.0,275.9 1048.5,275.8 1050.0,277.5 1051.5,279.3 1053.0,279.7 1054.5,279.9 1056.0,280.2 1057.5,280.6 1059.0,280.6 1060.5,281.4 1062.0,281.2 1063.5,282.6 1065.0,279.1 1066.5,273.7 1068.0,276.8 1069.5,288.2 1071.0,324.1 1072.5,341.2 1074.0,310.8 1075.5,285.9 1077.0,278.8 1078.5,276.2 1080.0,276.1 1081.5,275.1 1083.0,273.8 1084.5,272.3 1086.0,271.9 1087.5,271.1 1089.0,267.8 1090.5,264.6 1092.0,261.7 1093.5,259.9 1095.0,255.7 1096.5,251.2 1098.0,250.0 1099.5,249.9 1101.0,253.8 1102.5,256.2 1104.0,260.2 1105.5,267.0 1107.0,271.2 1108.5,275.6 1110.0,278.0 1111.5,279.1 1113.0,279.8 1114.5,279.8 1116.0,280.1 1117.5,280.1 1119.0,280.8 1120.5,280.7 1122.0,279.8 1123.5,279.3\"/><polyline class=\"trace\" points=\"1125.0,277.6 1126.5,276.8 1128.0,276.0 1129.5,275.4 1131.0,273.4 1132.5,273.0 1134.0,274.2 1135.5,276.3 1137.0,277.5 1138.5,277.6 1140.0,278.2 1141.5,278.5 1143.0,279.0 1144.5,279.1 1146.0,279.1 1147.5,279.1 1149.0,279.1 1150.5,279.1 1152.0,279.1 1153.5,278.8 1155.0,278.3 1156.5,278.1 1158.0,277.4 1159.5,276.9 1161.0,276.4 1162.5,275.8 1164.0,275.5 1165.5,274.9 1167.0,276.7 1168.5,279.2 1170.0,279.6 1171.5,280.0 1173.0,280.3 1174.5,280.6 1176.0,280.2 1177.5,280.0 1179.0,279.4 1180.5,279.4 1182.0,277.3 1183.5,260.4 1185.0,229.8 1186.5,215.0 1188.0,244.3 1189.5,278.7 1191.0,282.4 1192.5,280.6 1194.0,281.1 1195.5,280.9 1197.0,281.4 1198.5,281.3 1200.0,281.6 1201.5,281.7 1203.0,282.0 1204.5,282.1 1206.0,282.4 1207.5,282.7 1209.0,282.5 1210.5,281.7 1212.0,281.1 1213.5,279.7 1215.0,278.1 1216.5,277.8 1218.0,277.5 1219.5,277.2 1221.0,276.9 1222.5,276.6 1224.0,277.8 1225.5,279.2 1227.0,279.6 1228.5,280.0 1230.0,280.5 1231.5,280.8 1233.0,280.9 1234.5,280.9 1236.0,280.9 1237.5,280.9 1239.0,280.9 1240.5,280.8 1242.0,280.5 1243.5,280.3 1245.0,279.2 1246.5,277.9 1248.0,277.9 1249.5,277.8 1251.0,277.9 1252.5,277.8 1254.0,277.9 1255.5,278.3 1257.0,279.1 1258.5,281.0 1260.0,281.7 1261.5,282.0 1263.0,281.9 1264.5,282.4 1266.0,282.2 1267.5,282.4 1269.0,278.6 1270.5,259.1 1272.0,230.7 1273.5,216.6 1275.0,245.6 1276.5,280.8 1278.0,283.4 1279.5,281.0 1281.0,281.0 1282.5,280.7 1284.0,281.1 1285.5,280.7 1287.0,281.1 1288.5,281.1 1290.0,281.2 1291.5,281.2 1293.0,281.1 1294.5,281.2 1296.0,280.9 1297.5,279.9 1299.0,279.0 1300.5,278.5 1302.0,277.5 1303.5,275.2 1305.0,274.5 1306.5,275.1 1308.0,275.4 1309.5,275.8 1311.0,276.4 1312.5,278.2 1314.0,279.1 1315.5,279.0 1317.0,279.1 1318.5,279.0 1320.0,279.1 1321.5,279.0 1323.0,278.7 1324.5,278.8 1326.0,278.5 1327.5,278.5 1329.0,278.5 1330.5,277.8 1332.0,276.7 1333.5,275.7 1335.0,275.4 1336.5,276.0 1338.0,276.3 1339.5,276.7 1341.0,277.2 1342.5,277.4 1344.0,277.8 1345.5,277.9 1347.0,278.2 1348.5,277.9 1350.0,277.8 1351.5,278.0 1353.0,277.6 1354.5,277.9 1356.0,267.1 1357.5,240.3 1359.0,212.3 1360.5,220.0 1362.0,262.8 1363.5,281.7 1365.0,278.6 1366.5,278.7 1368.0,278.4 1369.5,278.9 1371.0,278.8 1372.5,279.1 1374.0,279.0 1375.5,278.5 1377.0,278.3 1378.5,277.9 1380.0,277.6 1381.5,277.3 1383.0,276.9 1384.5,276.4 1386.0,275.7 1387.5,274.2 1389.0,273.0 1390.5,272.7 1392.0,273.0 1393.5,273.4 1395.0,273.8 1396.5,274.2 1398.0,274.7 1399.5,275.2 1401.0,275.7 1402.5,276.1 1404.0,276.6 1405.5,277.0 1407.0,277.5 1408.5,277.8 1410.0,277.5 1411.5,277.0 1413.0,276.7 1414.5,276.2 1416.0,275.1 1417.5,274.6 1419.0,274.5 1420.5,274.2 1422.0,274.4 1423.5,274.8 1425.0,275.0 1426.5,275.3 1428.0,275.5 1429.5,275.9 1431.0,276.0 1432.5,276.6 1434.0,276.9 1435.5,277.2 1437.0,278.1 1438.5,279.1 1440.0,277.7 1441.5,265.6 1443.0,240.9 1444.5,207.6 1446.0,212.5 1447.5,260.9 1449.0,280.5 1450.5,277.5 1452.0,278.5 1453.5,278.2 1455.0,279.1 1456.5,278.9 1458.0,279.3 1459.5,279.6 1461.0,279.7 1462.5,279.4 1464.0,278.9 1465.5,278.8 1467.0,278.3 1468.5,278.1 1470.0,277.7 1471.5,277.2 1473.0,276.3 1474.5,275.1 1476.0,274.9 1477.5,275.2 1479.0,275.5 1480.5,275.9 1482.0,276.3 1483.5,276.5 1485.0,276.9 1486.5,277.3 1488.0,277.7 1489.5,278.1 1491.0,278.5 1492.5,278.7 1494.0,278.8 1495.5,279.1 1497.0,279.2 1498.5,279.5\"/><polyline class=\"trace\" points=\"0.0,389.4 1.5,388.5 3.0,387.9 4.5,388.5 6.0,388.6 7.5,389.1 9.0,389.3 10.5,389.8 12.0,391.2 13.5,391.9 15.0,392.2 16.5,392.5 18.0,392.9 19.5,393.2 21.0,393.6 22.5,393.7 24.0,393.9 25.5,394.0 27.0,394.3 28.5,394.3 30.0,393.6 31.5,392.3 33.0,390.2 34.5,389.6 36.0,389.8 37.5,389.8 39.0,390.2 40.5,390.0 42.0,390.4 43.5,392.2 45.0,393.4 46.5,394.6 48.0,394.9 49.5,394.9 51.0,394.8 52.5,395.0 54.0,394.8 55.5,394.9 57.0,394.3 58.5,389.3 60.0,381.1 61.5,367.6 63.0,375.0 64.5,395.1 66.0,394.9 67.5,393.0 69.0,393.9 70.5,393.4 72.0,394.2 73.5,394.0 75.0,394.3 76.5,393.9 78.0,393.9 79.5,393.7 81.0,393.4 82.5,393.4 84.0,393.1 85.5,392.4 87.0,391.8 88.5,390.4 90.0,388.6 91.5,388.6 93.0,389.2 94.5,389.5 96.0,390.0 97.5,390.2 99.0,391.1 100.5,392.5 102.0,392.8 103.5,392.8 105.0,392.8 106.5,392.8 108.0,392.8 109.5,392.5 111.0,392.4 112.5,392.5 114.0,392.4 115.5,392.5 117.0,392.4 118.5,390.4 120.0,388.8 121.5,388.8 123.0,388.3 124.5,388.3 126.0,388.8 127.5,389.1 129.0,389.5 130.5,389.9 132.0,390.3 133.5,390.6 135.0,390.8 136.5,391.1 138.0,391.1 139.5,391.6 141.0,391.4 142.5,390.9 144.0,389.3 145.5,385.4 147.0,376.9 148.5,364.0 150.0,371.7 151.5,388.5 153.0,389.2 154.5,389.2 156.0,389.7 157.5,389.5 159.0,390.0 160.5,389.3 162.0,389.3 163.5,388.8 165.0,388.7 166.5,388.3 168.0,388.1 169.5,387.6 171.0,387.2 172.5,386.9 174.0,385.6 175.5,383.9 177.0,382.8 178.5,382.5 180.0,382.8 181.5,382.9 183.0,383.1 184.5,383.4 186.0,384.5 187.5,385.5 189.0,386.0 190.5,386.5 192.0,387.1 193.5,387.3 195.0,386.8 196.5,386.5 198.0,386.2 199.5,385.9 201.0,385.6 202.5,385.0 204.0,384.3 205.5,383.6 207.0,383.1 208.5,382.7 210.0,381.9 211.5,381.5 213.0,381.8 214.5,382.1 216.0,382.3 217.5,383.5 219.0,385.5 220.5,385.6 222.0,386.1 223.5,386.2 225.0,386.5 226.5,386.9 228.0,386.1 229.5,386.1 231.0,382.0 232.5,376.8 234.0,363.3 235.5,357.1 237.0,376.5 238.5,385.6 240.0,384.1 241.5,385.7 243.0,385.3 244.5,386.2 246.0,385.9 247.5,385.5 249.0,385.1 250.5,384.5 252.0,384.2 253.5,383.7 255.0,383.4 256.5,382.9 258.0,382.6 259.5,381.7 261.0,379.2 262.5,378.0 264.0,378.1 265.5,377.7 267.0,377.7 268.5,377.4 270.0,377.9 271.5,380.2 273.0,381.9 274.5,382.7 276.0,383.1 277.5,383.5 279.0,383.9 280.5,384.3 282.0,384.6 283.5,384.4 285.0,384.0 286.5,383.7 288.0,383.3 289.5,383.1 291.0,382.5 292.5,381.2 294.0,380.4 295.5,380.0 297.0,380.1 298.5,380.8 300.0,381.4 301.5,382.2 303.0,383.0 304.5,384.1 306.0,384.9 307.5,385.9 309.0,386.0 310.5,385.6 312.0,385.7 313.5,385.1 315.0,385.2 316.5,381.6 318.0,375.9 319.5,363.5 321.0,357.0 322.5,376.5 324.0,388.6 325.5,386.4 327.0,387.1 328.5,386.2 330.0,386.3 331.5,386.2 333.0,386.1 334.5,386.2 336.0,386.1 337.5,386.1 339.0,385.6 340.5,385.5 342.0,385.1 343.5,384.8 345.0,383.7 346.5,382.2 348.0,381.0 349.5,380.1 351.0,380.2 352.5,380.8 354.0,381.3 355.5,381.8 357.0,382.4 358.5,383.1 360.0,384.0 361.5,384.6 363.0,384.7 364.5,384.7 366.0,385.0 367.5,385.0 369.0,384.9 370.5,384.7 372.0,384.5 373.5,384.3 375.0,384.1 376.5,383.7 378.0,382.4 379.5,381.4 381.0,380.5 382.5,380.4 384.0,381.1 385.5,381.4 387.0,382.2 388.5,382.8 390.0,384.0 391.5,384.6 393.0,384.9 394.5,385.0 396.0,385.1 397.5,385.8 399.0,385.2 400.5,385.2 402.0,381.1 403.5,376.5 405.0,363.1 406.5,356.2 408.0,379.1 409.5,390.2 411.0,386.4 412.5,386.8 414.0,386.3 415.5,387.0 417.0,386.9 418.5,387.4 420.0,387.4 421.5,386.9 423.0,386.8 424.5,386.4 426.0,386.2 427.5,385.8 429.0,384.9 430.5,383.4 432.0,381.3 433.5,379.3 435.0,379.5 436.5,380.0 438.0,380.3 439.5,380.9 441.0,381.1 442.5,381.9 444.0,383.1 445.5,383.5 447.0,383.7 448.5,383.9 450.0,384.2 451.5,384.4 453.0,384.2 454.5,383.9 456.0,383.8 457.5,383.5 459.0,383.3 460.5,383.1 462.0,381.6 463.5,380.1 465.0,379.9 466.5,379.5 468.0,379.3 469.5,379.9 471.0,380.2 472.5,381.0 474.0,382.1 475.5,383.4 477.0,384.1 478.5,384.3 480.0,384.8 481.5,384.8 483.0,385.7 484.5,385.0 486.0,385.2 487.5,382.0 489.0,377.2 490.5,367.1 492.0,356.3 493.5,373.1 495.0,387.4 496.5,385.5 498.0,386.5 499.5,385.7 501.0,385.9 502.5,386.0 504.0,386.1 505.5,386.3 507.0,386.2 508.5,386.6 510.0,386.4 511.5,386.3 513.0,385.8 514.5,385.5 516.0,384.6 517.5,383.3 519.0,381.9 520.5,379.7 522.0,378.9 523.5,379.0 525.0,379.1 526.5,380.6 528.0,382.4 529.5,383.9 531.0,384.9 532.5,385.5 534.0,386.2 535.5,386.7 537.0,386.9 538.5,387.1 540.0,387.3 541.5,387.6 543.0,387.6 544.5,387.2 546.0,386.9 547.5,386.3 549.0,385.3 550.5,383.1 552.0,382.2 553.5,382.3 555.0,382.4 556.5,382.6 558.0,382.7 559.5,383.9 561.0,385.1 562.5,386.4 564.0,386.9 565.5,387.1 567.0,387.5 568.5,387.6 570.0,388.1 571.5,388.0 573.0,388.5 574.5,384.1 576.0,378.3 577.5,368.4 579.0,362.4 580.5,381.7 582.0,392.5 583.5,388.2 585.0,389.2 586.5,388.4 588.0,388.6 589.5,388.3 591.0,388.3 592.5,388.7 594.0,388.5 595.5,388.7 597.0,388.5 598.5,388.7 600.0,388.1 601.5,387.0 603.0,386.3 604.5,385.2 606.0,383.6 607.5,381.9 609.0,381.3 610.5,382.0 612.0,382.4 613.5,383.0 615.0,384.7 616.5,386.4 618.0,387.5 619.5,388.2 621.0,388.5 622.5,388.9 624.0,389.4 625.5,389.7 627.0,389.6 628.5,389.4 630.0,389.3 631.5,389.1 633.0,388.9 634.5,388.8 636.0,387.3 637.5,385.8 639.0,385.6 640.5,385.2 642.0,385.0 643.5,385.6 645.0,386.1 646.5,386.7 648.0,387.2 649.5,387.7 651.0,388.3 652.5,388.8 654.0,389.4 655.5,389.0 657.0,389.4 658.5,388.6 660.0,389.2 661.5,387.3 663.0,382.1 664.5,375.0 666.0,362.6 667.5,371.9 669.0,388.6 670.5,387.9 672.0,388.6 673.5,388.8 675.0,388.9 676.5,389.3 678.0,388.6 679.5,389.1 681.0,388.6 682.5,388.6 684.0,388.5 685.5,388.4 687.0,388.0 688.5,387.8 690.0,387.6 691.5,386.1 693.0,384.4 694.5,383.7 696.0,383.8 697.5,384.2 699.0,384.4 700.5,384.7 702.0,384.9 703.5,385.7 705.0,387.5 706.5,388.1 708.0,388.2 709.5,388.5 711.0,388.6 712.5,388.9 714.0,388.6 715.5,388.5 717.0,388.6 718.5,388.5 720.0,388.6 721.5,388.5 723.0,388.1 724.5,386.8 726.0,384.6 727.5,383.8 729.0,383.4 730.5,383.4 732.0,384.1 733.5,384.5 735.0,385.2 736.5,385.7 738.0,386.9 739.5,388.0 741.0,388.0 742.5,388.7 744.0,388.5 745.5,389.2 747.0,388.9 748.5,388.5\"/><text class=\"lead\" x=\"4\" y=\"21\">I</text><text class=\"lead\" x=\"379\" y=\"21\">AVR</text><text class=\"lead\" x=\"754\" y=\"21\">V1</text><text class=\"lead\" x=\"1129\" y=\"21\">V4</text><text class=\"lead\" x=\"4\" y=\"129\">II</text><text class=\"lead\" x=\"379\" y=\"129\">AVL</text><text class=\"lead\" x=\"754\" y=\"129\">V2</text><text class=\"lead\" x=\"1129\" y=\"129\">V5</text><text class=\"lead\" x=\"4\" y=\"237\">III</text><text class=\"lead\" x=\"379\" y=\"237\">AVF</text><text class=\"lead\" x=\"754\" y=\"237\">V3</text><text class=\"lead\" x=\"1129\" y=\"237\">V6</text><text class=\"lead\" x=\"4\" y=\"346\">II (rhythm)</text><text class=\"cap\" x=\"4\" y=\"452\">12유도 · 실데이터(PTB-XL, CC-BY) · 하벽·전중격 심근경색</text></svg>"
 },
 {
  "id": "usmle-2026-0041",
  "exam": "usmle",
  "step": "Step 2",
  "subject": "Neurology",
  "subject_file": "Neurology",
  "subtopic": "Guillain-Barré Syndrome — Respiratory Monitoring Before Definitive Therapy",
  "type": "Guillain-Barré Syndrome — Respiratory Monitoring Before Definitive Therapy",
  "difficulty": 4,
  "created": "2026-07-09",
  "vignette": "A 34-year-old woman comes to the emergency department because of progressive weakness over the past 3 days, beginning in her feet and now involving her legs and hands. She reports mild difficulty swallowing but no shortness of breath. Two weeks ago she had a bout of bloody diarrhea that resolved without treatment. On examination she has symmetric weakness, absent deep tendon reflexes, and intact sensation. Her vital signs are currently stable.",
  "question": "Which of the following is the most appropriate immediate next step in management?",
  "options": [
   "Begin oral corticosteroids to reduce inflammatory demyelination",
   "Start intravenous immunoglobulin immediately, without further assessment of respiratory status",
   "Reassure the patient and arrange outpatient neurology follow-up in one week given her stable vital signs",
   "Obtain nerve conduction studies to confirm the diagnosis before initiating any monitoring or treatment",
   "Admit for close monitoring of forced vital capacity (FVC) and negative inspiratory force to anticipate respiratory failure"
  ],
  "answer": 5,
  "explanationText": "- 정답근거: 선행 설사(Campylobacter jejuni 의심) 2주 후 발생한 대칭성 상행성 약화 + 심부건반사 소실 + 감각은 보존 + 경도 연하곤란은 길랑-바레 증후군(GBS)의 전형적 모습이다. 현재 활력징후가 안정적이어 보여도, GBS는 호흡근까지 마비가 진행하면 수 시간 내에 호흡부전으로 악화될 수 있으므로 가장 먼저 해야 할 일은 확진이나 면역치료가 아니라 연속적인 FVC·최대흡기압(NIF) 감시를 위한 입원이다.\n- 오답감별:\n  - A: 스테로이드는 GBS에서 효과가 입증되지 않았다(다발성경화증과 혼동하기 쉬운 함정) — 사용하지 않는다.\n  - B: IVIG는 실제 표준 치료이지만, 순서가 틀렸다. 호흡 안전이 확보되지 않은 상태에서 치료만 서두르면 안 되고, 입원·모니터링 체계 안에서 시행해야 한다(\"치료 자체는 맞지만 지금 당장 가장 먼저 할 일은 아니다\"라는 순서 함정).\n  - C: 활력징후가 안정적이라고 외래로 돌려보내는 것은 위험하다. 상행성 마비는 예측 불가능하게 빠르게 진행할 수 있다 — 가장 치명적인 오답.\n  - D: 신경전도검사는 진단을 뒷받침하지만, 결과를 기다리느라 호흡 안전 모니터링을 지연시켜서는 안 된다. 임상적으로 GBS가 강력히 의심되면 확진 검사 결과를 기다리지 않고 모니터링·치료 준비를 시작한다.\n- 임상핵심: GBS 초기 대응의 핵심은 \"확진\"이 아니라 \"호흡부전을 놓치지 않는 것\"이다. FVC 20 mL/kg 미만, 빠른 하강 추세, 연수마비 징후는 조기 삽관을 시사한다(\"20/30/40 규칙\": FVC<20, 최대흡기압>-30, 최대호기압<40 cmH2O).\n- 출처: American Academy of Neurology Guideline — Guillain-Barré Syndrome.",
  "explanationItems": [
   {
    "k": "정답근거",
    "v": "선행 설사(Campylobacter jejuni 의심) 2주 후 발생한 대칭성 상행성 약화 + 심부건반사 소실 + 감각은 보존 + 경도 연하곤란은 길랑-바레 증후군(GBS)의 전형적 모습이다. 현재 활력징후가 안정적이어 보여도, GBS는 호흡근까지 마비가 진행하면 수 시간 내에 호흡부전으로 악화될 수 있으므로 가장 먼저 해야 할 일은 확진이나 면역치료가 아니라 연속적인 FVC·최대흡기압(NIF) 감시를 위한 입원이다."
   },
   {
    "k": "오답감별",
    "v": "A: 스테로이드는 GBS에서 효과가 입증되지 않았다(다발성경화증과 혼동하기 쉬운 함정) — 사용하지 않는다.\nB: IVIG는 실제 표준 치료이지만, 순서가 틀렸다. 호흡 안전이 확보되지 않은 상태에서 치료만 서두르면 안 되고, 입원·모니터링 체계 안에서 시행해야 한다(\"치료 자체는 맞지만 지금 당장 가장 먼저 할 일은 아니다\"라는 순서 함정).\nC: 활력징후가 안정적이라고 외래로 돌려보내는 것은 위험하다. 상행성 마비는 예측 불가능하게 빠르게 진행할 수 있다 — 가장 치명적인 오답.\nD: 신경전도검사는 진단을 뒷받침하지만, 결과를 기다리느라 호흡 안전 모니터링을 지연시켜서는 안 된다. 임상적으로 GBS가 강력히 의심되면 확진 검사 결과를 기다리지 않고 모니터링·치료 준비를 시작한다."
   },
   {
    "k": "임상핵심",
    "v": "GBS 초기 대응의 핵심은 \"확진\"이 아니라 \"호흡부전을 놓치지 않는 것\"이다. FVC 20 mL/kg 미만, 빠른 하강 추세, 연수마비 징후는 조기 삽관을 시사한다(\"20/30/40 규칙\": FVC<20, 최대흡기압>-30, 최대호기압<40 cmH2O)."
   },
   {
    "k": "출처",
    "v": "American Academy of Neurology Guideline — Guillain-Barré Syndrome."
   }
  ],
  "source": "USMLE-style / MedKOS (neurology · acute neuromuscular emergency)",
  "vitals": [
   {
    "name": "혈압",
    "value": "118/74 mmHg"
   },
   {
    "name": "맥박",
    "value": "88회/분"
   },
   {
    "name": "호흡",
    "value": "18회/분"
   },
   {
    "name": "체온",
    "value": "36.8 °C"
   }
  ],
  "labs": [],
  "appendix": {
   "가이드라인": "길랑-바레 증후군(GBS) 초기 대응 결정표\n─────────────────────────────────────────────\n1단계: 호흡 안전 확보 — 연속 FVC·NIF 측정, 구음/연하 관찰, 자율신경 불안정 감시\n       (FVC < 20 mL/kg, 또는 급격히 감소하는 추세면 삽관 고려 — \"20/30/40 규칙\")\n2단계: 확진·중증도 평가 — 신경전도검사·뇌척수액(단백-세포 해리) — 치료 시작을 늦추지 않음\n3단계: 면역치료 — IVIG 또는 혈장교환술(동등 효과, 병용은 권장 안 함)\n       스테로이드 단독은 효과 없음 → 사용하지 않음\n─────────────────────────────────────────────\n",
   "최신지견": "GBS 사망의 주된 원인은 진단 지연이 아니라 호흡부전 인지 지연이다. 활력징후가 안정적이어도 상행성 마비는 수 시간~수일 내 급격히 진행할 수 있다.",
   "참고문헌": [
    "AAN Guideline: Guillain-Barré Syndrome Management",
    "Adams and Victor's Principles of Neurology — Acute inflammatory demyelinating polyneuropathy"
   ]
  },
  "figureSvg": ""
 },
 {
  "id": "usmle-2026-0042",
  "exam": "usmle",
  "step": "Step 2",
  "subject": "Psychiatry",
  "subject_file": "Psychiatry",
  "subtopic": "Neuroleptic Malignant Syndrome vs Serotonin Syndrome (differentiating features)",
  "type": "Neuroleptic Malignant Syndrome vs Serotonin Syndrome (differentiating features)",
  "difficulty": 4,
  "created": "2026-07-09",
  "vignette": "A 45-year-old man with schizophrenia is brought to the emergency department by his group home staff. His haloperidol dose was increased 5 days ago. Over the past 2 days he has become progressively confused with a fever and profuse diaphoresis. On examination he has generalized 'lead-pipe' rigidity without clonus, and deep tendon reflexes are normal rather than increased. His vital signs and CK are shown.",
  "question": "Which of the following clinical features most strongly favors this diagnosis over serotonin syndrome?",
  "options": [
   "Presence of hyperreflexia with inducible clonus in the lower extremities",
   "Rapid symptom onset within hours of the causative drug exposure",
   "Symptom onset over several days after a dopamine-blocking agent was started or increased, with rigidity but no clonus",
   "Gastrointestinal hyperactivity with diarrhea and hyperactive bowel sounds",
   "Dilated pupils and ocular clonus on examination"
  ],
  "answer": 3,
  "explanationText": "- 정답근거: 신경이완제악성증후군(NMS)은 도파민 차단제(대표적으로 항정신병약) 시작·증량 후 수일에 걸쳐 서서히 발생하며, 근육 소견은 간대(clonus) 없는 납관 강직(lead-pipe rigidity)이 특징이다. 이 환자는 할로페리돌 증량 5일 후 서서히 발열·경직·의식변화가 나타났고 간대·과반사가 없다는 점에서 세로토닌증후군보다 NMS에 부합한다.\n- 오답감별:\n  - A: 간대를 동반한 과반사는 오히려 세로토닌증후군의 특징이다. NMS는 반사가 정상이거나 오히려 저하될 수 있다 — 두 질환을 헷갈리기 쉬운 대표적 함정.\n  - B: 수시간 내 급성 발병은 세로토닌증후군의 전형적 시간경과다. NMS는 대개 약제 변경 후 1~3일 이상에 걸쳐 서서히 진행한다 — 시간경과를 반대로 아는 경우가 많다.\n  - D: 설사·장운동 항진은 세로토닌 과잉에 의한 자율신경 증상으로 세로토닌증후군에 가깝다. NMS는 오히려 자율신경 불안정이 있어도 장운동 저하(심하면 마비성 장폐색)로 나타나는 경우가 더 특징적이다.\n  - E: 산동(mydriasis)과 안구간대(ocular clonus)는 세로토닌증후군의 전형적 눈 소견이다. NMS에서는 이런 안구 소견이 특징적이지 않다.\n- 임상핵심: \"며칠에 걸쳐 서서히 + 납관강직 + clonus 없음 = NMS\", \"수시간 내 급격히 + clonus/과반사 + 산동 + 설사 = 세로토닌증후군\"으로 시간경과와 신경학적 진찰(clonus 유무)을 짝지어 암기한다. 두 질환 모두 원인약물 중단이 최우선이며, NMS는 브로모크립틴·단트롤렌, 세로토닌증후군은 사이프로헵타딘을 보조적으로 사용한다.\n- 출처: Kaplan & Sadock's Synopsis of Psychiatry (Drug-induced hyperthermic syndromes).",
  "explanationItems": [
   {
    "k": "정답근거",
    "v": "신경이완제악성증후군(NMS)은 도파민 차단제(대표적으로 항정신병약) 시작·증량 후 수일에 걸쳐 서서히 발생하며, 근육 소견은 간대(clonus) 없는 납관 강직(lead-pipe rigidity)이 특징이다. 이 환자는 할로페리돌 증량 5일 후 서서히 발열·경직·의식변화가 나타났고 간대·과반사가 없다는 점에서 세로토닌증후군보다 NMS에 부합한다."
   },
   {
    "k": "오답감별",
    "v": "A: 간대를 동반한 과반사는 오히려 세로토닌증후군의 특징이다. NMS는 반사가 정상이거나 오히려 저하될 수 있다 — 두 질환을 헷갈리기 쉬운 대표적 함정.\nB: 수시간 내 급성 발병은 세로토닌증후군의 전형적 시간경과다. NMS는 대개 약제 변경 후 1~3일 이상에 걸쳐 서서히 진행한다 — 시간경과를 반대로 아는 경우가 많다.\nD: 설사·장운동 항진은 세로토닌 과잉에 의한 자율신경 증상으로 세로토닌증후군에 가깝다. NMS는 오히려 자율신경 불안정이 있어도 장운동 저하(심하면 마비성 장폐색)로 나타나는 경우가 더 특징적이다.\nE: 산동(mydriasis)과 안구간대(ocular clonus)는 세로토닌증후군의 전형적 눈 소견이다. NMS에서는 이런 안구 소견이 특징적이지 않다."
   },
   {
    "k": "임상핵심",
    "v": "\"며칠에 걸쳐 서서히 + 납관강직 + clonus 없음 = NMS\", \"수시간 내 급격히 + clonus/과반사 + 산동 + 설사 = 세로토닌증후군\"으로 시간경과와 신경학적 진찰(clonus 유무)을 짝지어 암기한다. 두 질환 모두 원인약물 중단이 최우선이며, NMS는 브로모크립틴·단트롤렌, 세로토닌증후군은 사이프로헵타딘을 보조적으로 사용한다."
   },
   {
    "k": "출처",
    "v": "Kaplan & Sadock's Synopsis of Psychiatry (Drug-induced hyperthermic syndromes)."
   }
  ],
  "source": "USMLE-style / MedKOS (psychiatry · drug-induced hyperthermic syndromes)",
  "vitals": [
   {
    "name": "혈압",
    "value": "148/92 mmHg"
   },
   {
    "name": "맥박",
    "value": "112회/분"
   },
   {
    "name": "호흡",
    "value": "22회/분"
   },
   {
    "name": "체온",
    "value": "39.8 °C"
   }
  ],
  "labs": [
   {
    "name": "혈청 크레아틴키나제(CK)",
    "value": "18,400 U/L",
    "ref": "30–200"
   },
   {
    "name": "백혈구",
    "value": "14,200 /mm³",
    "ref": "4,000–10,000"
   },
   {
    "name": "혈청 나트륨",
    "value": "138 mEq/L",
    "ref": "135–145"
   }
  ],
  "appendix": {
   "가이드라인": "NMS vs 세로토닌증후군 감별·처치\n─────────────────────────────────────────────\n항목        NMS                      세로토닌증후군\n유발약물    도파민 차단제(항정신병약) 세로토닌작용제 병용/과량\n발병 속도   수일(용량 변경 후)        수시간 이내\n근긴장      납관 강직(clonus 없음)    간대(clonus)·과반사\n동공        정상                      산동\n장관운동    저하(마비성 장폐색 가능)  항진(설사·과다연동)\n─────────────────────────────────────────────\n공통 처치: 원인약물 즉시 중단, 적극적 냉각·수액\nNMS 특이: 브로모크립틴(도파민효현제) ± 단트롤렌(골격근 이완, ryanodine 수용체 차단)\n세로토닌증후군 특이: 사이프로헵타딘(세로토닌 길항제)\n",
   "최신지견": "두 증후군 모두 원인약물 중단이 가장 중요한 첫 조치이며, 약물치료는 보조적이다.",
   "참고문헌": [
    "APA Practice Guideline — Management of Neuroleptic Malignant Syndrome",
    "Kaplan & Sadock's Synopsis of Psychiatry — Drug-induced hyperthermic syndromes"
   ]
  },
  "figureSvg": ""
 },
 {
  "id": "usmle-2026-0043",
  "exam": "usmle",
  "step": "Step 1",
  "subject": "Immunology",
  "subject_file": "Immunology",
  "subtopic": "X-linked Agammaglobulinemia (Bruton's Disease)",
  "type": "X-linked Agammaglobulinemia (Bruton's Disease)",
  "difficulty": 4,
  "created": "2026-07-14",
  "vignette": "A 5-month-old boy is brought to the emergency department with a 2-day history of fever and productive cough. He was well until about 5 months of age. He has already had two episodes of otitis media and one episode of sinusitis, each treated with oral antibiotics. On examination, the tonsils are absent and no cervical lymph nodes are palpable. Chest x-ray shows a right lower lobe infiltrate, and sputum culture grows Streptococcus pneumoniae. Vital signs and laboratory studies, including flow cytometry, are shown.",
  "question": "Which of the following best describes the mechanism underlying this infant's disease?",
  "options": [
   "Impaired class-switch recombination due to a defective CD40 ligand on activated T cells",
   "Arrest of B-cell maturation at the pre-B stage due to a defective Bruton tyrosine kinase",
   "Global arrest of lymphocyte development due to adenosine deaminase deficiency",
   "Failure of the neutrophil oxidative burst due to defective NADPH oxidase",
   "Failure of membrane attack complex formation due to a terminal complement component deficiency"
  ],
  "answer": 2,
  "explanationText": "- 정답근거: 생후 5~6개월(모체 이행항체 소실 시점) 이후부터 시작된 encapsulated organism(폐렴구균) 반복 감염, 편도·림프절 저형성, 전 클래스(IgG/IgA/IgM) 면역글로불린 저하, 그리고 말초혈 CD19+ B세포가 거의 소실된 소견은 X-linked agammaglobulinemia(XLA)에 합당하다. BTK(Bruton tyrosine kinase) 결함으로 pre-B세포 수용체 신호전달이 차단되어 pre-B세포에서 성숙 B세포로의 분화가 멈춘다.\n- 오답감별:\n  - A: CD40 리간드 결함(Hyper-IgM 증후군)은 클래스스위칭만 안 되므로 B세포 수 자체는 정상이고 IgM은 정상~상승한다. 이 환아는 B세포가 거의 없고 IgM도 낮아 부합하지 않는다.\n  - C: 아데노신탈아미노효소(ADA) 결핍은 SCID를 일으켜 T세포까지 결핍되는데, 이 환아는 절대호중구수는 정상이고 문항에서 T세포 결핍 소견이 제시되지 않았다(B세포 선택적 결핍).\n  - D: NADPH 산화효소 결함(만성육아종병, CGD)은 B세포·면역글로불린은 정상이며 호중구 살균능만 소실된다. 이 환아는 ANC가 정상이고 오히려 체액성 면역(Ig·B세포)이 결핍되어 있어 반대 패턴이다.\n  - E: 말단보체(C5-C9) 결핍은 Neisseria 균종 반복 감염이 특징이며 CH50이 저하되는데, 이 환아는 CH50이 정상이고 폐렴구균 감염·저감마글로불린혈증이 핵심이다.\n- 임상핵심: 남아 + 생후 6개월 전후부터 시작되는 반복적 encapsulated organism 감염 + 편도/림프절 저형성 + 전 클래스 Ig 저하 + CD19+ B세포 부재 → XLA를 우선 의심하고 BTK 결함을 원인 기전으로 연결한다.\n- 출처: First Aid for the USMLE Step 1 — Immunology, Immunodeficiencies; Nelson Textbook of Pediatrics.",
  "explanationItems": [
   {
    "k": "정답근거",
    "v": "생후 5~6개월(모체 이행항체 소실 시점) 이후부터 시작된 encapsulated organism(폐렴구균) 반복 감염, 편도·림프절 저형성, 전 클래스(IgG/IgA/IgM) 면역글로불린 저하, 그리고 말초혈 CD19+ B세포가 거의 소실된 소견은 X-linked agammaglobulinemia(XLA)에 합당하다. BTK(Bruton tyrosine kinase) 결함으로 pre-B세포 수용체 신호전달이 차단되어 pre-B세포에서 성숙 B세포로의 분화가 멈춘다."
   },
   {
    "k": "오답감별",
    "v": "A: CD40 리간드 결함(Hyper-IgM 증후군)은 클래스스위칭만 안 되므로 B세포 수 자체는 정상이고 IgM은 정상~상승한다. 이 환아는 B세포가 거의 없고 IgM도 낮아 부합하지 않는다.\nC: 아데노신탈아미노효소(ADA) 결핍은 SCID를 일으켜 T세포까지 결핍되는데, 이 환아는 절대호중구수는 정상이고 문항에서 T세포 결핍 소견이 제시되지 않았다(B세포 선택적 결핍).\nD: NADPH 산화효소 결함(만성육아종병, CGD)은 B세포·면역글로불린은 정상이며 호중구 살균능만 소실된다. 이 환아는 ANC가 정상이고 오히려 체액성 면역(Ig·B세포)이 결핍되어 있어 반대 패턴이다.\nE: 말단보체(C5-C9) 결핍은 Neisseria 균종 반복 감염이 특징이며 CH50이 저하되는데, 이 환아는 CH50이 정상이고 폐렴구균 감염·저감마글로불린혈증이 핵심이다."
   },
   {
    "k": "임상핵심",
    "v": "남아 + 생후 6개월 전후부터 시작되는 반복적 encapsulated organism 감염 + 편도/림프절 저형성 + 전 클래스 Ig 저하 + CD19+ B세포 부재 → XLA를 우선 의심하고 BTK 결함을 원인 기전으로 연결한다."
   },
   {
    "k": "출처",
    "v": "First Aid for the USMLE Step 1 — Immunology, Immunodeficiencies; Nelson Textbook of Pediatrics."
   }
  ],
  "source": "USMLE-style / MedKOS (immunology · primary humoral immunodeficiency)",
  "vitals": [
   {
    "name": "혈압",
    "value": "88/54 mmHg"
   },
   {
    "name": "맥박",
    "value": "132회/분"
   },
   {
    "name": "호흡",
    "value": "40회/분"
   },
   {
    "name": "체온",
    "value": "38.6 °C"
   }
  ],
  "labs": [
   {
    "name": "혈청 IgG",
    "value": "92 mg/dL",
    "ref": "400–1000"
   },
   {
    "name": "혈청 IgA",
    "value": "<7 mg/dL",
    "ref": "20–100"
   },
   {
    "name": "혈청 IgM",
    "value": "15 mg/dL",
    "ref": "40–160"
   },
   {
    "name": "말초혈 CD19+ B세포",
    "value": "0.2 %",
    "ref": "5–20"
   },
   {
    "name": "절대호중구수(ANC)",
    "value": "3,200 /mm³",
    "ref": "1,500–8,000"
   },
   {
    "name": "총보체활성(CH50)",
    "value": "정상 범위",
    "ref": "정상"
   }
  ],
  "appendix": {
   "가이드라인": "주요 원발성 면역결핍의 감별 (제시된 검사 소견 기준)\n─────────────────────────────────────────────────────\n질환                 B세포        Ig(전체)     T세포     특이 소견\nXLA(BTK 결함)         부재/저하    전 클래스↓   정상      남아, 6개월 이후 발병\nHyper-IgM(CD40L 결함)  정상 수      IgM 정상/↑,  정상      클래스스위칭 안 됨\n                                    IgG/IgA↓\nSCID(ADA 결핍 등)      저하         저하         저하      전반적 림프구 결핍\nCGD(NADPH옥시다제)     정상         정상         정상      호중구 살균능 소실\n말단보체결핍(C5-9)     정상         정상         정상      Neisseria 반복감염\n─────────────────────────────────────────────────────\n",
   "최신지견": "확진은 BTK 유전자 검사 또는 B세포 내 BTK 단백 발현 소실 확인으로 하며, 치료는 정기적 IVIG 대체요법이다.",
   "참고문헌": [
    "First Aid for the USMLE Step 1 — Immunology, Immunodeficiencies",
    "Nelson Textbook of Pediatrics — Primary Humoral Immunodeficiencies"
   ]
  },
  "figureSvg": ""
 },
 {
  "id": "usmle-2026-0044",
  "exam": "usmle",
  "step": "Step 1",
  "subject": "Biochemistry",
  "subject_file": "Biochemistry",
  "subtopic": "Fatty Acid Oxidation Disorder (MCAD Deficiency)",
  "type": "Fatty Acid Oxidation Disorder (MCAD Deficiency)",
  "difficulty": 5,
  "created": "2026-07-14",
  "vignette": "An 18-month-old girl is brought to the emergency department after being found difficult to arouse this morning. She had a low-grade fever and poor oral intake yesterday and missed both dinner and breakfast. On arrival she is lethargic but responds to voice. Vital signs and laboratory studies are shown. Urine ketones are unexpectedly low given the degree of hypoglycemia present.",
  "question": "Which of the following best explains the absence of ketosis in this hypoglycemic child?",
  "options": [
   "Impaired carnitine palmitoyltransferase-1 activity prevents long-chain fatty acids from entering the mitochondria",
   "Deficient glucose-6-phosphatase activity prevents the final step of glycogenolysis and gluconeogenesis",
   "Deficient pyruvate dehydrogenase activity prevents conversion of pyruvate to acetyl-CoA",
   "Deficient medium-chain acyl-CoA dehydrogenase activity blocks beta-oxidation of medium-chain fatty acids, limiting the acetyl-CoA available for ketogenesis",
   "Deficient HMG-CoA lyase activity blocks the terminal step of ketone body synthesis"
  ],
  "answer": 4,
  "explanationText": "- 정답근거: 장시간 공복(저녁·아침 결식) 후 저혈당인데도 소변 케톤이 미량에 그치는 \"저케톤성 저혈당(hypoketotic hypoglycemia)\"과, 유리지방산 상승, 젖산은 정상, 아실카르니틴 profile에서 C8(옥타노일카르니틴)이 뚜렷이 상승한 소견은 MCAD(중쇄 아실-CoA 탈수소효소) 결핍의 전형이다. 중쇄 지방산이 미토콘드리아 베타산화를 거치지 못해 아세틸-CoA 공급이 끊기고, 그 결과 간에서 케톤체 합성 기질이 부족해진다.\n- 오답감별:\n  - A: CPT-1 결핍은 장쇄 지방산이 미토콘드리아로 들어가지 못하는 질환으로 임상상은 유사하나, 이 문항의 핵심 단서인 C8 아실카르니틴 상승은 중쇄(medium-chain) 효소 결함을 가리키며 CPT-1(장쇄 운반체) 결함과는 부합하지 않는다.\n  - B: Von Gierke병(G6Pase 결핍)도 공복 저혈당을 일으키지만, 당신생 경로 전체가 막혀 젖산이 축적되므로 젖산산증을 동반한다. 이 환아는 젖산이 정상 범위(1.4 mmol/L)로, 당원분해 장애를 시사하는 소견과 맞지 않는다.\n  - C: 피루브산탈수소효소 결핍 역시 젖산·피루브산이 함께 상승하는 것이 특징인데, 이 환아의 젖산은 정상이다.\n  - E: HMG-CoA 리아제 결핍도 저케톤성 저혈당을 일으켜 매력적인 오답이지만, 이 경우 케톤생성 \"마지막 단계\"만 막혀 전구체(아세토아세틸-CoA)가 축적되고 아실카르니틴 패턴은 C8이 아닌 다른 패턴(디카르복실산뇨 등)으로 나타난다. 문항에 제시된 C8 상승은 지방산 산화의 중쇄 단계 결함(MCAD)을 특이적으로 가리킨다.\n- 임상핵심: \"공복 유발 저케톤성 저혈당 + 젖산 정상 + 아실카르니틴 C8 상승\" 조합은 MCAD 결핍을 시사하는 대표 패턴으로 암기한다. 급성기에는 공복을 피하고 포도당을 정주하는 것이 핵심 치료다.\n- 출처: First Aid for the USMLE Step 1 — Biochemistry, Fatty Acid Metabolism; Nelson Textbook of Pediatrics.",
  "explanationItems": [
   {
    "k": "정답근거",
    "v": "장시간 공복(저녁·아침 결식) 후 저혈당인데도 소변 케톤이 미량에 그치는 \"저케톤성 저혈당(hypoketotic hypoglycemia)\"과, 유리지방산 상승, 젖산은 정상, 아실카르니틴 profile에서 C8(옥타노일카르니틴)이 뚜렷이 상승한 소견은 MCAD(중쇄 아실-CoA 탈수소효소) 결핍의 전형이다. 중쇄 지방산이 미토콘드리아 베타산화를 거치지 못해 아세틸-CoA 공급이 끊기고, 그 결과 간에서 케톤체 합성 기질이 부족해진다."
   },
   {
    "k": "오답감별",
    "v": "A: CPT-1 결핍은 장쇄 지방산이 미토콘드리아로 들어가지 못하는 질환으로 임상상은 유사하나, 이 문항의 핵심 단서인 C8 아실카르니틴 상승은 중쇄(medium-chain) 효소 결함을 가리키며 CPT-1(장쇄 운반체) 결함과는 부합하지 않는다.\nB: Von Gierke병(G6Pase 결핍)도 공복 저혈당을 일으키지만, 당신생 경로 전체가 막혀 젖산이 축적되므로 젖산산증을 동반한다. 이 환아는 젖산이 정상 범위(1.4 mmol/L)로, 당원분해 장애를 시사하는 소견과 맞지 않는다.\nC: 피루브산탈수소효소 결핍 역시 젖산·피루브산이 함께 상승하는 것이 특징인데, 이 환아의 젖산은 정상이다.\nE: HMG-CoA 리아제 결핍도 저케톤성 저혈당을 일으켜 매력적인 오답이지만, 이 경우 케톤생성 \"마지막 단계\"만 막혀 전구체(아세토아세틸-CoA)가 축적되고 아실카르니틴 패턴은 C8이 아닌 다른 패턴(디카르복실산뇨 등)으로 나타난다. 문항에 제시된 C8 상승은 지방산 산화의 중쇄 단계 결함(MCAD)을 특이적으로 가리킨다."
   },
   {
    "k": "임상핵심",
    "v": "\"공복 유발 저케톤성 저혈당 + 젖산 정상 + 아실카르니틴 C8 상승\" 조합은 MCAD 결핍을 시사하는 대표 패턴으로 암기한다. 급성기에는 공복을 피하고 포도당을 정주하는 것이 핵심 치료다."
   },
   {
    "k": "출처",
    "v": "First Aid for the USMLE Step 1 — Biochemistry, Fatty Acid Metabolism; Nelson Textbook of Pediatrics."
   }
  ],
  "source": "USMLE-style / MedKOS (biochemistry · fatty acid oxidation)",
  "vitals": [
   {
    "name": "혈압",
    "value": "92/58 mmHg"
   },
   {
    "name": "맥박",
    "value": "128회/분"
   },
   {
    "name": "호흡",
    "value": "26회/분"
   },
   {
    "name": "체온",
    "value": "38.3 °C"
   }
  ],
  "labs": [
   {
    "name": "혈당",
    "value": "38 mg/dL",
    "ref": "70–100"
   },
   {
    "name": "소변 케톤",
    "value": "미량",
    "ref": "저혈당 시 강양성 예상"
   },
   {
    "name": "혈청 유리지방산(FFA)",
    "value": "2.1 mmol/L",
    "ref": "0.1–0.6"
   },
   {
    "name": "혈청 젖산",
    "value": "1.4 mmol/L",
    "ref": "0.5–2.2"
   },
   {
    "name": "AST/ALT",
    "value": "88/76 U/L",
    "ref": "< 40"
   },
   {
    "name": "혈장 아실카르니틴 profile",
    "value": "옥타노일카르니틴(C8) 뚜렷한 상승",
    "ref": "정상 대비 증가"
   }
  ],
  "appendix": {
   "가이드라인": "공복 저혈당 감별 — 케톤 유무와 젖산으로 좁히기\n───────────────────────────────────────────────\n기전                      케톤       젖산     핵심 검사 소견\n지방산 산화 장애(MCAD 등)  저/음성    정상     아실카르니틴 이상(C8↑)\n당신생/당원분해 장애(Von   저/음성    상승     젖산산증 동반\n  Gierke, G6Pase 결핍)\n피루브산탈수소효소 결핍    저/음성    상승     피루브산·젖산 동반 상승\n케톤생성 장애(HMG-CoA      저/음성    정상     아세토아세트산 전구체 축적,\n  리아제 결핍)                                  아실카르니틴 패턴 다름\n───────────────────────────────────────────────\n",
   "최신지견": "신생아 선별검사(탠덤매스)로 C8 아실카르니틴 상승을 조기 발견하면 급성 대사위기 전에 진단할 수 있다.",
   "참고문헌": [
    "First Aid for the USMLE Step 1 — Biochemistry, Fatty Acid Metabolism",
    "Nelson Textbook of Pediatrics — Inborn Errors of Fatty Acid Oxidation"
   ]
  },
  "figureSvg": ""
 },
 {
  "id": "usmle-2026-0045",
  "exam": "usmle",
  "step": "Step 1",
  "subject": "Microbiology",
  "subject_file": "Microbiology",
  "subtopic": "Atypical Pneumonia (Legionella pneumophila)",
  "type": "Atypical Pneumonia (Legionella pneumophila)",
  "difficulty": 4,
  "created": "2026-07-14",
  "vignette": "A 58-year-old man returns from a business trip and presents with a 3-day history of high fever, headache, and watery diarrhea followed by a dry cough and worsening dyspnea. He stayed at a hotel with a large decorative fountain and used the hot tub daily. Chest x-ray shows a patchy infiltrate in the right lower lobe. Sputum Gram stain shows many neutrophils but no visible organisms, and a routine sputum culture on standard blood agar shows no growth after 48 hours. Vital signs and laboratory studies are shown.",
  "question": "Which of the following is the most appropriate next diagnostic test to confirm the suspected diagnosis?",
  "options": [
   "Urinary antigen test for Legionella pneumophila serogroup 1",
   "Repeat sputum culture on standard blood agar for an additional 48 hours",
   "Cold agglutinin titer to evaluate for Mycoplasma pneumoniae infection",
   "Sputum acid-fast bacillus smear and culture for suspected tuberculosis",
   "Serum beta-D-glucan assay to evaluate for an invasive fungal infection"
  ],
  "answer": 1,
  "explanationText": "- 정답근거: 온수(핫텁)·분수 노출력, 고열에 비해 상대적으로 낮은 맥박, 설사 등 위장관 증상 동반, 저나트륨혈증, 간효소 상승, 그리고 Gram 염색에서 호중구는 많으나 균이 보이지 않고 표준 혈액한천배지에서 배양이 안 되는 소견은 모두 Legionella pneumophila 폐렴을 시사한다. Legionella는 시스테인·철분이 첨가된 특수배지(BCYE)에서만 자라므로, 신속한 확진에는 소변 항원검사(혈청군 1)가 가장 적합하다.\n- 오답감별:\n  - B: 표준 혈액한천배지는 Legionella가 필요로 하는 시스테인이 없어 배양 기간을 늘려도 자라지 않는다. 반복 배양은 시간만 지연시킨다.\n  - C: 콜드응집소 검사는 Mycoplasma pneumoniae 감염을 시사하는 보조검사로, 이 환자의 수인성 노출력·저나트륨혈증 패턴과는 맞지 않는다.\n  - D: 항산균 도말·배양은 결핵이 의심될 때(만성 기침·객혈·야간발한·고위험 노출력) 시행하며, 이 환자의 급성 경과·수계 노출력과는 부합하지 않는다.\n  - E: 베타-D-글루칸은 아스페르길루스·주폐포자충 등 진균 감염의 표지자로, 세균성 비정형 폐렴인 Legionella 감별에는 사용하지 않는다.\n- 임상핵심: 여행/온수 노출력 + 고열 대비 상대적 서맥 + 위장관 증상 동반 폐렴 + 저나트륨혈증 + 표준배지 배양 음성 → Legionella를 의심하고 소변항원검사로 신속 확진한다(단, 혈청군 1만 검출하는 한계는 기억).\n- 출처: First Aid for the USMLE Step 1 — Microbiology, Atypical Pneumonias; IDSA/ATS CAP Guidelines.",
  "explanationItems": [
   {
    "k": "정답근거",
    "v": "온수(핫텁)·분수 노출력, 고열에 비해 상대적으로 낮은 맥박, 설사 등 위장관 증상 동반, 저나트륨혈증, 간효소 상승, 그리고 Gram 염색에서 호중구는 많으나 균이 보이지 않고 표준 혈액한천배지에서 배양이 안 되는 소견은 모두 Legionella pneumophila 폐렴을 시사한다. Legionella는 시스테인·철분이 첨가된 특수배지(BCYE)에서만 자라므로, 신속한 확진에는 소변 항원검사(혈청군 1)가 가장 적합하다."
   },
   {
    "k": "오답감별",
    "v": "B: 표준 혈액한천배지는 Legionella가 필요로 하는 시스테인이 없어 배양 기간을 늘려도 자라지 않는다. 반복 배양은 시간만 지연시킨다.\nC: 콜드응집소 검사는 Mycoplasma pneumoniae 감염을 시사하는 보조검사로, 이 환자의 수인성 노출력·저나트륨혈증 패턴과는 맞지 않는다.\nD: 항산균 도말·배양은 결핵이 의심될 때(만성 기침·객혈·야간발한·고위험 노출력) 시행하며, 이 환자의 급성 경과·수계 노출력과는 부합하지 않는다.\nE: 베타-D-글루칸은 아스페르길루스·주폐포자충 등 진균 감염의 표지자로, 세균성 비정형 폐렴인 Legionella 감별에는 사용하지 않는다."
   },
   {
    "k": "임상핵심",
    "v": "여행/온수 노출력 + 고열 대비 상대적 서맥 + 위장관 증상 동반 폐렴 + 저나트륨혈증 + 표준배지 배양 음성 → Legionella를 의심하고 소변항원검사로 신속 확진한다(단, 혈청군 1만 검출하는 한계는 기억)."
   },
   {
    "k": "출처",
    "v": "First Aid for the USMLE Step 1 — Microbiology, Atypical Pneumonias; IDSA/ATS CAP Guidelines."
   }
  ],
  "source": "USMLE-style / MedKOS (microbiology · atypical pneumonia)",
  "vitals": [
   {
    "name": "혈압",
    "value": "132/84 mmHg"
   },
   {
    "name": "맥박",
    "value": "82회/분"
   },
   {
    "name": "호흡",
    "value": "24회/분"
   },
   {
    "name": "체온",
    "value": "39.6 °C"
   }
  ],
  "labs": [
   {
    "name": "혈청 나트륨",
    "value": "128 mEq/L",
    "ref": "135–145"
   },
   {
    "name": "AST/ALT",
    "value": "76/68 U/L",
    "ref": "< 40"
   },
   {
    "name": "C-반응단백(CRP)",
    "value": "18 mg/dL",
    "ref": "< 0.5"
   },
   {
    "name": "백혈구",
    "value": "13,200 /mm³",
    "ref": "4,000–10,000"
   },
   {
    "name": "혈소판",
    "value": "210,000 /mm³",
    "ref": "150,000–400,000"
   }
  ],
  "appendix": {
   "가이드라인": "비정형 폐렴 원인균별 확진검사 감별\n───────────────────────────────────────────────\n원인균                  표준 배지 성장   특이 확진검사\nLegionella pneumophila   불가(BCYE 필요)  소변항원(혈청군1), BCYE 배양/PCR\nMycoplasma pneumoniae    불가(특수배지)   콜드응집소, PCR, IgM 혈청검사\nChlamydophila pneumoniae 불가             PCR, 혈청검사\nMycobacterium tuberculosis 불가(특수배지) AFB 도말/배양, NAAT\nAspergillus/Pneumocystis 진균배지 필요    베타-D-글루칸, 갈락토만난\n───────────────────────────────────────────────\n",
   "최신지견": "소변항원검사는 혈청군 1(전체 원인균의 약 80~90%)만 검출하므로 음성이어도 배양·PCR로 배제를 확인해야 한다.",
   "참고문헌": [
    "First Aid for the USMLE Step 1 — Microbiology, Atypical Pneumonias",
    "IDSA/ATS Community-Acquired Pneumonia Guidelines"
   ]
  },
  "figureSvg": ""
 },
 {
  "id": "usmle-2026-0046",
  "exam": "usmle",
  "step": "Step 2",
  "subject": "Internal Medicine",
  "subject_file": "Internal Medicine",
  "subtopic": "Atrial Flutter (ECG rhythm recognition)",
  "type": "Atrial Flutter (ECG rhythm recognition)",
  "difficulty": 4,
  "created": "2026-07-14",
  "vignette": "A 70-year-old man with a history of COPD presents with 6 hours of palpitations and mild dyspnea. He denies chest pain or syncope. He is alert and oriented, and his skin is warm and well-perfused. Vital signs are shown. An ECG (shown) reveals a regular, narrow-complex tachycardia with sawtooth-appearing atrial activity and 2:1 atrioventricular conduction. He is unsure exactly when his symptoms began, saying it may have started sometime yesterday. Thyroid and electrolyte panels are shown and are unremarkable.",
  "question": "Which of the following is the most appropriate next step in management?",
  "options": [
   "Immediate synchronized electrical cardioversion despite stable hemodynamics",
   "Intravenous adenosine to attempt pharmacologic termination of the rhythm",
   "Rate control with an intravenous beta-blocker as the initial step in management",
   "Immediate intravenous amiodarone for pharmacologic cardioversion today",
   "Electrical cardioversion today without prior transesophageal echocardiography"
  ],
  "answer": 3,
  "explanationText": "- 정답근거: 이 환자는 혈역학적으로 안정(정상 혈압, 의식명료, 관류 양호)하고 증상 발생 시점이 불명확한 심방조동이다. 안정형이면서 지속시간이 불확실할 때는 우선 심박수 조절을 시행하고, 이후 뇌졸중 위험(CHA2DS2-VASc)을 평가해 항응고 여부를 결정한 뒤에 리듬조절(동율동전환)을 고려하는 것이 표준 순서다.\n- 오답감별:\n  - A: 즉시 전기적 동율동전환은 저혈압·흉통·의식저하·폐부종 등 혈역학적 불안정 소견이 있을 때만 우선한다. 이 환자는 안정적이므로 응급 동율동전환의 적응증이 아니다.\n  - B: 아데노신은 방실결절 의존 회로(AVNRT/AVRT)의 진단·치료에 쓰인다. 심방조동은 거대 회귀회로가 방실결절에 의존하지 않아 아데노신으로 일시적 방실차단은 되어도 부정맥 자체는 종료되지 않는다.\n  - D: 아미오다론으로 즉시 화학적 동율동전환을 시도하면, 지속시간이 불명확한 상태에서 좌심방이 혈전이 있을 경우 색전증(뇌졸중) 위험이 있다. 항응고 평가 없이 리듬조절을 서두르면 안 된다.\n  - E: TEE 없이 지속시간 불명확한 부정맥을 동율동전환하는 것은 활력징후가 안정적이더라도 색전 위험을 배제하지 못한 채 시행하는 것이라 위험하다.\n- 임상핵심: 안정형 심방조동/세동 신환, 지속시간 불명확 → 심박수 조절이 최우선, 리듬조절(동율동전환)은 항응고 평가·TEE 또는 지속시간 확인 이후에만 시행한다.\n- 출처: 2023 ACC/AHA/ACCP/HRS Atrial Fibrillation Guideline; UpToDate — Atrial Flutter.",
  "explanationItems": [
   {
    "k": "정답근거",
    "v": "이 환자는 혈역학적으로 안정(정상 혈압, 의식명료, 관류 양호)하고 증상 발생 시점이 불명확한 심방조동이다. 안정형이면서 지속시간이 불확실할 때는 우선 심박수 조절을 시행하고, 이후 뇌졸중 위험(CHA2DS2-VASc)을 평가해 항응고 여부를 결정한 뒤에 리듬조절(동율동전환)을 고려하는 것이 표준 순서다."
   },
   {
    "k": "오답감별",
    "v": "A: 즉시 전기적 동율동전환은 저혈압·흉통·의식저하·폐부종 등 혈역학적 불안정 소견이 있을 때만 우선한다. 이 환자는 안정적이므로 응급 동율동전환의 적응증이 아니다.\nB: 아데노신은 방실결절 의존 회로(AVNRT/AVRT)의 진단·치료에 쓰인다. 심방조동은 거대 회귀회로가 방실결절에 의존하지 않아 아데노신으로 일시적 방실차단은 되어도 부정맥 자체는 종료되지 않는다.\nD: 아미오다론으로 즉시 화학적 동율동전환을 시도하면, 지속시간이 불명확한 상태에서 좌심방이 혈전이 있을 경우 색전증(뇌졸중) 위험이 있다. 항응고 평가 없이 리듬조절을 서두르면 안 된다.\nE: TEE 없이 지속시간 불명확한 부정맥을 동율동전환하는 것은 활력징후가 안정적이더라도 색전 위험을 배제하지 못한 채 시행하는 것이라 위험하다."
   },
   {
    "k": "임상핵심",
    "v": "안정형 심방조동/세동 신환, 지속시간 불명확 → 심박수 조절이 최우선, 리듬조절(동율동전환)은 항응고 평가·TEE 또는 지속시간 확인 이후에만 시행한다."
   },
   {
    "k": "출처",
    "v": "2023 ACC/AHA/ACCP/HRS Atrial Fibrillation Guideline; UpToDate — Atrial Flutter."
   }
  ],
  "source": "USMLE-style / MedKOS (cardiology · arrhythmia management)",
  "vitals": [
   {
    "name": "혈압",
    "value": "118/76 mmHg"
   },
   {
    "name": "맥박",
    "value": "148회/분"
   },
   {
    "name": "호흡",
    "value": "22회/분"
   },
   {
    "name": "체온",
    "value": "36.8 °C"
   }
  ],
  "labs": [
   {
    "name": "혈청 TSH",
    "value": "2.1 mIU/L",
    "ref": "0.4–4.0"
   },
   {
    "name": "혈청 칼륨",
    "value": "4.2 mEq/L",
    "ref": "3.5–5.0"
   }
  ],
  "appendix": {
   "가이드라인": "안정형 심방조동/세동 신환 처치 순서\n───────────────────────────────────────────\n1단계  혈역학적 안정성 평가 (저혈압·흉통·의식저하·폐부종 → 불안정 시 즉시 동율동전환)\n2단계  안정 시: 베타차단제/non-DHP 칼슘차단제로 심박수 조절\n3단계  지속시간 확인 → 48시간 미만 확실 / TEE로 좌심방이 혈전 배제 시에만 조기 동율동전환 고려\n4단계  지속시간 불명확 or 48시간 이상 → 최소 3주 항응고 후 선택적 동율동전환(또는 CHA2DS2-VASc 기반 지속 항응고)\n───────────────────────────────────────────\n",
   "최신지견": "심방조동은 심방세동과 달리 방실결절 비의존 거대 회귀회로라 아데노신으로 일시적 방실차단은 되지만 종료되지 않는다.",
   "참고문헌": [
    "2023 ACC/AHA/ACCP/HRS Guideline for the Diagnosis and Management of Atrial Fibrillation",
    "UpToDate — Atrial Flutter: Overview and Management"
   ]
  },
  "figureSvg": "<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 900 198\" width=\"900\" height=\"198\" role=\"img\" aria-label=\"ECG flutter · 148 bpm · 25 mm/s, 10 mm/mV\"><style>.bg{fill:#fff}.gmin{stroke:#f4c9c9;stroke-width:0.5}.gmaj{stroke:#e59a9a;stroke-width:1}.trace{fill:none;stroke:#111;stroke-width:1.6;stroke-linejoin:round;stroke-linecap:round}.cap{font:11px -apple-system,Segoe UI,sans-serif;fill:#555}</style><rect class=\"bg\" x=\"0\" y=\"0\" width=\"900\" height=\"180\"/><line x1=\"0\" y1=\"0\" x2=\"0\" y2=\"180\" class=\"gmaj\"/><line x1=\"6\" y1=\"0\" x2=\"6\" y2=\"180\" class=\"gmin\"/><line x1=\"12\" y1=\"0\" x2=\"12\" y2=\"180\" class=\"gmin\"/><line x1=\"18\" y1=\"0\" x2=\"18\" y2=\"180\" class=\"gmin\"/><line x1=\"24\" y1=\"0\" x2=\"24\" y2=\"180\" class=\"gmin\"/><line x1=\"30\" y1=\"0\" x2=\"30\" y2=\"180\" class=\"gmaj\"/><line x1=\"36\" y1=\"0\" x2=\"36\" y2=\"180\" class=\"gmin\"/><line x1=\"42\" y1=\"0\" x2=\"42\" y2=\"180\" class=\"gmin\"/><line x1=\"48\" y1=\"0\" x2=\"48\" y2=\"180\" class=\"gmin\"/><line x1=\"54\" y1=\"0\" x2=\"54\" y2=\"180\" class=\"gmin\"/><line x1=\"60\" y1=\"0\" x2=\"60\" y2=\"180\" class=\"gmaj\"/><line x1=\"66\" y1=\"0\" x2=\"66\" y2=\"180\" class=\"gmin\"/><line x1=\"72\" y1=\"0\" x2=\"72\" y2=\"180\" class=\"gmin\"/><line x1=\"78\" y1=\"0\" x2=\"78\" y2=\"180\" class=\"gmin\"/><line x1=\"84\" y1=\"0\" x2=\"84\" y2=\"180\" class=\"gmin\"/><line x1=\"90\" y1=\"0\" x2=\"90\" y2=\"180\" class=\"gmaj\"/><line x1=\"96\" y1=\"0\" x2=\"96\" y2=\"180\" class=\"gmin\"/><line x1=\"102\" y1=\"0\" x2=\"102\" y2=\"180\" class=\"gmin\"/><line x1=\"108\" y1=\"0\" x2=\"108\" y2=\"180\" class=\"gmin\"/><line x1=\"114\" y1=\"0\" x2=\"114\" y2=\"180\" class=\"gmin\"/><line x1=\"120\" y1=\"0\" x2=\"120\" y2=\"180\" class=\"gmaj\"/><line x1=\"126\" y1=\"0\" x2=\"126\" y2=\"180\" class=\"gmin\"/><line x1=\"132\" y1=\"0\" x2=\"132\" y2=\"180\" class=\"gmin\"/><line x1=\"138\" y1=\"0\" x2=\"138\" y2=\"180\" class=\"gmin\"/><line x1=\"144\" y1=\"0\" x2=\"144\" y2=\"180\" class=\"gmin\"/><line x1=\"150\" y1=\"0\" x2=\"150\" y2=\"180\" class=\"gmaj\"/><line x1=\"156\" y1=\"0\" x2=\"156\" y2=\"180\" class=\"gmin\"/><line x1=\"162\" y1=\"0\" x2=\"162\" y2=\"180\" class=\"gmin\"/><line x1=\"168\" y1=\"0\" x2=\"168\" y2=\"180\" class=\"gmin\"/><line x1=\"174\" y1=\"0\" x2=\"174\" y2=\"180\" class=\"gmin\"/><line x1=\"180\" y1=\"0\" x2=\"180\" y2=\"180\" class=\"gmaj\"/><line x1=\"186\" y1=\"0\" x2=\"186\" y2=\"180\" class=\"gmin\"/><line x1=\"192\" y1=\"0\" x2=\"192\" y2=\"180\" class=\"gmin\"/><line x1=\"198\" y1=\"0\" x2=\"198\" y2=\"180\" class=\"gmin\"/><line x1=\"204\" y1=\"0\" x2=\"204\" y2=\"180\" class=\"gmin\"/><line x1=\"210\" y1=\"0\" x2=\"210\" y2=\"180\" class=\"gmaj\"/><line x1=\"216\" y1=\"0\" x2=\"216\" y2=\"180\" class=\"gmin\"/><line x1=\"222\" y1=\"0\" x2=\"222\" y2=\"180\" class=\"gmin\"/><line x1=\"228\" y1=\"0\" x2=\"228\" y2=\"180\" class=\"gmin\"/><line x1=\"234\" y1=\"0\" x2=\"234\" y2=\"180\" class=\"gmin\"/><line x1=\"240\" y1=\"0\" x2=\"240\" y2=\"180\" class=\"gmaj\"/><line x1=\"246\" y1=\"0\" x2=\"246\" y2=\"180\" class=\"gmin\"/><line x1=\"252\" y1=\"0\" x2=\"252\" y2=\"180\" class=\"gmin\"/><line x1=\"258\" y1=\"0\" x2=\"258\" y2=\"180\" class=\"gmin\"/><line x1=\"264\" y1=\"0\" x2=\"264\" y2=\"180\" class=\"gmin\"/><line x1=\"270\" y1=\"0\" x2=\"270\" y2=\"180\" class=\"gmaj\"/><line x1=\"276\" y1=\"0\" x2=\"276\" y2=\"180\" class=\"gmin\"/><line x1=\"282\" y1=\"0\" x2=\"282\" y2=\"180\" class=\"gmin\"/><line x1=\"288\" y1=\"0\" x2=\"288\" y2=\"180\" class=\"gmin\"/><line x1=\"294\" y1=\"0\" x2=\"294\" y2=\"180\" class=\"gmin\"/><line x1=\"300\" y1=\"0\" x2=\"300\" y2=\"180\" class=\"gmaj\"/><line x1=\"306\" y1=\"0\" x2=\"306\" y2=\"180\" class=\"gmin\"/><line x1=\"312\" y1=\"0\" x2=\"312\" y2=\"180\" class=\"gmin\"/><line x1=\"318\" y1=\"0\" x2=\"318\" y2=\"180\" class=\"gmin\"/><line x1=\"324\" y1=\"0\" x2=\"324\" y2=\"180\" class=\"gmin\"/><line x1=\"330\" y1=\"0\" x2=\"330\" y2=\"180\" class=\"gmaj\"/><line x1=\"336\" y1=\"0\" x2=\"336\" y2=\"180\" class=\"gmin\"/><line x1=\"342\" y1=\"0\" x2=\"342\" y2=\"180\" class=\"gmin\"/><line x1=\"348\" y1=\"0\" x2=\"348\" y2=\"180\" class=\"gmin\"/><line x1=\"354\" y1=\"0\" x2=\"354\" y2=\"180\" class=\"gmin\"/><line x1=\"360\" y1=\"0\" x2=\"360\" y2=\"180\" class=\"gmaj\"/><line x1=\"366\" y1=\"0\" x2=\"366\" y2=\"180\" class=\"gmin\"/><line x1=\"372\" y1=\"0\" x2=\"372\" y2=\"180\" class=\"gmin\"/><line x1=\"378\" y1=\"0\" x2=\"378\" y2=\"180\" class=\"gmin\"/><line x1=\"384\" y1=\"0\" x2=\"384\" y2=\"180\" class=\"gmin\"/><line x1=\"390\" y1=\"0\" x2=\"390\" y2=\"180\" class=\"gmaj\"/><line x1=\"396\" y1=\"0\" x2=\"396\" y2=\"180\" class=\"gmin\"/><line x1=\"402\" y1=\"0\" x2=\"402\" y2=\"180\" class=\"gmin\"/><line x1=\"408\" y1=\"0\" x2=\"408\" y2=\"180\" class=\"gmin\"/><line x1=\"414\" y1=\"0\" x2=\"414\" y2=\"180\" class=\"gmin\"/><line x1=\"420\" y1=\"0\" x2=\"420\" y2=\"180\" class=\"gmaj\"/><line x1=\"426\" y1=\"0\" x2=\"426\" y2=\"180\" class=\"gmin\"/><line x1=\"432\" y1=\"0\" x2=\"432\" y2=\"180\" class=\"gmin\"/><line x1=\"438\" y1=\"0\" x2=\"438\" y2=\"180\" class=\"gmin\"/><line x1=\"444\" y1=\"0\" x2=\"444\" y2=\"180\" class=\"gmin\"/><line x1=\"450\" y1=\"0\" x2=\"450\" y2=\"180\" class=\"gmaj\"/><line x1=\"456\" y1=\"0\" x2=\"456\" y2=\"180\" class=\"gmin\"/><line x1=\"462\" y1=\"0\" x2=\"462\" y2=\"180\" class=\"gmin\"/><line x1=\"468\" y1=\"0\" x2=\"468\" y2=\"180\" class=\"gmin\"/><line x1=\"474\" y1=\"0\" x2=\"474\" y2=\"180\" class=\"gmin\"/><line x1=\"480\" y1=\"0\" x2=\"480\" y2=\"180\" class=\"gmaj\"/><line x1=\"486\" y1=\"0\" x2=\"486\" y2=\"180\" class=\"gmin\"/><line x1=\"492\" y1=\"0\" x2=\"492\" y2=\"180\" class=\"gmin\"/><line x1=\"498\" y1=\"0\" x2=\"498\" y2=\"180\" class=\"gmin\"/><line x1=\"504\" y1=\"0\" x2=\"504\" y2=\"180\" class=\"gmin\"/><line x1=\"510\" y1=\"0\" x2=\"510\" y2=\"180\" class=\"gmaj\"/><line x1=\"516\" y1=\"0\" x2=\"516\" y2=\"180\" class=\"gmin\"/><line x1=\"522\" y1=\"0\" x2=\"522\" y2=\"180\" class=\"gmin\"/><line x1=\"528\" y1=\"0\" x2=\"528\" y2=\"180\" class=\"gmin\"/><line x1=\"534\" y1=\"0\" x2=\"534\" y2=\"180\" class=\"gmin\"/><line x1=\"540\" y1=\"0\" x2=\"540\" y2=\"180\" class=\"gmaj\"/><line x1=\"546\" y1=\"0\" x2=\"546\" y2=\"180\" class=\"gmin\"/><line x1=\"552\" y1=\"0\" x2=\"552\" y2=\"180\" class=\"gmin\"/><line x1=\"558\" y1=\"0\" x2=\"558\" y2=\"180\" class=\"gmin\"/><line x1=\"564\" y1=\"0\" x2=\"564\" y2=\"180\" class=\"gmin\"/><line x1=\"570\" y1=\"0\" x2=\"570\" y2=\"180\" class=\"gmaj\"/><line x1=\"576\" y1=\"0\" x2=\"576\" y2=\"180\" class=\"gmin\"/><line x1=\"582\" y1=\"0\" x2=\"582\" y2=\"180\" class=\"gmin\"/><line x1=\"588\" y1=\"0\" x2=\"588\" y2=\"180\" class=\"gmin\"/><line x1=\"594\" y1=\"0\" x2=\"594\" y2=\"180\" class=\"gmin\"/><line x1=\"600\" y1=\"0\" x2=\"600\" y2=\"180\" class=\"gmaj\"/><line x1=\"606\" y1=\"0\" x2=\"606\" y2=\"180\" class=\"gmin\"/><line x1=\"612\" y1=\"0\" x2=\"612\" y2=\"180\" class=\"gmin\"/><line x1=\"618\" y1=\"0\" x2=\"618\" y2=\"180\" class=\"gmin\"/><line x1=\"624\" y1=\"0\" x2=\"624\" y2=\"180\" class=\"gmin\"/><line x1=\"630\" y1=\"0\" x2=\"630\" y2=\"180\" class=\"gmaj\"/><line x1=\"636\" y1=\"0\" x2=\"636\" y2=\"180\" class=\"gmin\"/><line x1=\"642\" y1=\"0\" x2=\"642\" y2=\"180\" class=\"gmin\"/><line x1=\"648\" y1=\"0\" x2=\"648\" y2=\"180\" class=\"gmin\"/><line x1=\"654\" y1=\"0\" x2=\"654\" y2=\"180\" class=\"gmin\"/><line x1=\"660\" y1=\"0\" x2=\"660\" y2=\"180\" class=\"gmaj\"/><line x1=\"666\" y1=\"0\" x2=\"666\" y2=\"180\" class=\"gmin\"/><line x1=\"672\" y1=\"0\" x2=\"672\" y2=\"180\" class=\"gmin\"/><line x1=\"678\" y1=\"0\" x2=\"678\" y2=\"180\" class=\"gmin\"/><line x1=\"684\" y1=\"0\" x2=\"684\" y2=\"180\" class=\"gmin\"/><line x1=\"690\" y1=\"0\" x2=\"690\" y2=\"180\" class=\"gmaj\"/><line x1=\"696\" y1=\"0\" x2=\"696\" y2=\"180\" class=\"gmin\"/><line x1=\"702\" y1=\"0\" x2=\"702\" y2=\"180\" class=\"gmin\"/><line x1=\"708\" y1=\"0\" x2=\"708\" y2=\"180\" class=\"gmin\"/><line x1=\"714\" y1=\"0\" x2=\"714\" y2=\"180\" class=\"gmin\"/><line x1=\"720\" y1=\"0\" x2=\"720\" y2=\"180\" class=\"gmaj\"/><line x1=\"726\" y1=\"0\" x2=\"726\" y2=\"180\" class=\"gmin\"/><line x1=\"732\" y1=\"0\" x2=\"732\" y2=\"180\" class=\"gmin\"/><line x1=\"738\" y1=\"0\" x2=\"738\" y2=\"180\" class=\"gmin\"/><line x1=\"744\" y1=\"0\" x2=\"744\" y2=\"180\" class=\"gmin\"/><line x1=\"750\" y1=\"0\" x2=\"750\" y2=\"180\" class=\"gmaj\"/><line x1=\"756\" y1=\"0\" x2=\"756\" y2=\"180\" class=\"gmin\"/><line x1=\"762\" y1=\"0\" x2=\"762\" y2=\"180\" class=\"gmin\"/><line x1=\"768\" y1=\"0\" x2=\"768\" y2=\"180\" class=\"gmin\"/><line x1=\"774\" y1=\"0\" x2=\"774\" y2=\"180\" class=\"gmin\"/><line x1=\"780\" y1=\"0\" x2=\"780\" y2=\"180\" class=\"gmaj\"/><line x1=\"786\" y1=\"0\" x2=\"786\" y2=\"180\" class=\"gmin\"/><line x1=\"792\" y1=\"0\" x2=\"792\" y2=\"180\" class=\"gmin\"/><line x1=\"798\" y1=\"0\" x2=\"798\" y2=\"180\" class=\"gmin\"/><line x1=\"804\" y1=\"0\" x2=\"804\" y2=\"180\" class=\"gmin\"/><line x1=\"810\" y1=\"0\" x2=\"810\" y2=\"180\" class=\"gmaj\"/><line x1=\"816\" y1=\"0\" x2=\"816\" y2=\"180\" class=\"gmin\"/><line x1=\"822\" y1=\"0\" x2=\"822\" y2=\"180\" class=\"gmin\"/><line x1=\"828\" y1=\"0\" x2=\"828\" y2=\"180\" class=\"gmin\"/><line x1=\"834\" y1=\"0\" x2=\"834\" y2=\"180\" class=\"gmin\"/><line x1=\"840\" y1=\"0\" x2=\"840\" y2=\"180\" class=\"gmaj\"/><line x1=\"846\" y1=\"0\" x2=\"846\" y2=\"180\" class=\"gmin\"/><line x1=\"852\" y1=\"0\" x2=\"852\" y2=\"180\" class=\"gmin\"/><line x1=\"858\" y1=\"0\" x2=\"858\" y2=\"180\" class=\"gmin\"/><line x1=\"864\" y1=\"0\" x2=\"864\" y2=\"180\" class=\"gmin\"/><line x1=\"870\" y1=\"0\" x2=\"870\" y2=\"180\" class=\"gmaj\"/><line x1=\"876\" y1=\"0\" x2=\"876\" y2=\"180\" class=\"gmin\"/><line x1=\"882\" y1=\"0\" x2=\"882\" y2=\"180\" class=\"gmin\"/><line x1=\"888\" y1=\"0\" x2=\"888\" y2=\"180\" class=\"gmin\"/><line x1=\"894\" y1=\"0\" x2=\"894\" y2=\"180\" class=\"gmin\"/><line x1=\"900\" y1=\"0\" x2=\"900\" y2=\"180\" class=\"gmaj\"/><line x1=\"0\" y1=\"0\" x2=\"900\" y2=\"0\" class=\"gmaj\"/><line x1=\"0\" y1=\"6\" x2=\"900\" y2=\"6\" class=\"gmin\"/><line x1=\"0\" y1=\"12\" x2=\"900\" y2=\"12\" class=\"gmin\"/><line x1=\"0\" y1=\"18\" x2=\"900\" y2=\"18\" class=\"gmin\"/><line x1=\"0\" y1=\"24\" x2=\"900\" y2=\"24\" class=\"gmin\"/><line x1=\"0\" y1=\"30\" x2=\"900\" y2=\"30\" class=\"gmaj\"/><line x1=\"0\" y1=\"36\" x2=\"900\" y2=\"36\" class=\"gmin\"/><line x1=\"0\" y1=\"42\" x2=\"900\" y2=\"42\" class=\"gmin\"/><line x1=\"0\" y1=\"48\" x2=\"900\" y2=\"48\" class=\"gmin\"/><line x1=\"0\" y1=\"54\" x2=\"900\" y2=\"54\" class=\"gmin\"/><line x1=\"0\" y1=\"60\" x2=\"900\" y2=\"60\" class=\"gmaj\"/><line x1=\"0\" y1=\"66\" x2=\"900\" y2=\"66\" class=\"gmin\"/><line x1=\"0\" y1=\"72\" x2=\"900\" y2=\"72\" class=\"gmin\"/><line x1=\"0\" y1=\"78\" x2=\"900\" y2=\"78\" class=\"gmin\"/><line x1=\"0\" y1=\"84\" x2=\"900\" y2=\"84\" class=\"gmin\"/><line x1=\"0\" y1=\"90\" x2=\"900\" y2=\"90\" class=\"gmaj\"/><line x1=\"0\" y1=\"96\" x2=\"900\" y2=\"96\" class=\"gmin\"/><line x1=\"0\" y1=\"102\" x2=\"900\" y2=\"102\" class=\"gmin\"/><line x1=\"0\" y1=\"108\" x2=\"900\" y2=\"108\" class=\"gmin\"/><line x1=\"0\" y1=\"114\" x2=\"900\" y2=\"114\" class=\"gmin\"/><line x1=\"0\" y1=\"120\" x2=\"900\" y2=\"120\" class=\"gmaj\"/><line x1=\"0\" y1=\"126\" x2=\"900\" y2=\"126\" class=\"gmin\"/><line x1=\"0\" y1=\"132\" x2=\"900\" y2=\"132\" class=\"gmin\"/><line x1=\"0\" y1=\"138\" x2=\"900\" y2=\"138\" class=\"gmin\"/><line x1=\"0\" y1=\"144\" x2=\"900\" y2=\"144\" class=\"gmin\"/><line x1=\"0\" y1=\"150\" x2=\"900\" y2=\"150\" class=\"gmaj\"/><line x1=\"0\" y1=\"156\" x2=\"900\" y2=\"156\" class=\"gmin\"/><line x1=\"0\" y1=\"162\" x2=\"900\" y2=\"162\" class=\"gmin\"/><line x1=\"0\" y1=\"168\" x2=\"900\" y2=\"168\" class=\"gmin\"/><line x1=\"0\" y1=\"174\" x2=\"900\" y2=\"174\" class=\"gmin\"/><line x1=\"0\" y1=\"180\" x2=\"900\" y2=\"180\" class=\"gmaj\"/><polyline class=\"trace\" points=\"0.0,90.0 0.6,90.4 1.2,90.8 1.8,91.2 2.4,91.5 3.0,91.9 3.6,92.3 4.2,92.7 4.8,93.1 5.4,93.5 6.0,93.8 6.6,94.2 7.2,94.6 7.8,95.0 8.4,95.4 9.0,95.8 9.6,96.1 10.2,96.5 10.8,96.9 11.4,97.3 12.0,97.7 12.6,98.1 13.2,98.4 13.8,98.8 14.4,99.2 15.0,80.4 15.6,80.8 16.2,81.2 16.8,81.6 17.4,81.9 18.0,82.3 18.6,82.7 19.2,83.1 19.8,83.5 20.4,83.9 21.0,84.2 21.6,84.6 22.2,85.0 22.8,85.4 23.4,85.8 24.0,86.2 24.6,86.5 25.2,86.9 25.8,87.3 26.4,87.7 27.0,88.1 27.6,88.5 28.2,88.8 28.8,89.2 29.4,89.6 30.0,90.0 30.6,90.4 31.2,90.8 31.8,91.2 32.4,91.5 33.0,91.9 33.6,92.3 34.2,92.7 34.8,93.1 35.4,93.5 36.0,93.8 36.6,94.2 37.2,94.6 37.8,95.0 38.4,95.4 39.0,95.8 39.6,96.1 40.2,96.5 40.8,96.9 41.4,97.3 42.0,97.7 42.6,98.1 43.2,98.4 43.8,98.8 44.4,99.2 45.0,80.4 45.6,80.8 46.2,81.2 46.8,81.6 47.4,81.9 48.0,82.3 48.6,82.7 49.2,83.1 49.8,83.5 50.4,83.9 51.0,84.2 51.6,84.6 52.2,85.0 52.8,85.4 53.4,86.0 54.0,86.9 54.6,88.1 55.2,89.1 55.8,88.4 56.4,84.9 57.0,77.9 57.6,67.4 58.2,54.4 58.8,41.0 59.4,30.7 60.0,27.3 60.6,32.1 61.2,43.9 61.8,59.2 62.4,74.5 63.0,87.0 63.6,95.8 64.2,100.8 64.8,102.8 65.4,102.5 66.0,100.9 66.6,99.0 67.2,97.4 67.8,96.5 68.4,96.0 69.0,96.0 69.6,96.2 70.2,96.6 70.8,96.9 71.4,97.3 72.0,97.7 72.6,98.1 73.2,98.4 73.8,98.8 74.4,99.2 75.0,80.4 75.6,80.8 76.2,81.2 76.8,81.5 77.4,81.9 78.0,82.3 78.6,82.7 79.2,83.1 79.8,83.5 80.4,83.8 81.0,84.2 81.6,84.6 82.2,85.0 82.8,85.3 83.4,85.7 84.0,86.0 84.6,86.4 85.2,86.7 85.8,87.0 86.4,87.3 87.0,87.6 87.6,87.9 88.2,88.1 88.8,88.3 89.4,88.5 90.0,88.6 90.6,88.7 91.2,88.7 91.8,88.7 92.4,88.6 93.0,88.5 93.6,88.3 94.2,88.0 94.8,87.7 95.4,87.3 96.0,86.9 96.6,86.5 97.2,86.0 97.8,85.5 98.4,85.0 99.0,84.4 99.6,83.9 100.2,83.5 100.8,83.1 101.4,82.7 102.0,82.5 102.6,82.3 103.2,82.2 103.8,82.3 104.4,82.5 105.0,63.6 105.6,64.1 106.2,64.6 106.8,65.3 107.4,66.2 108.0,67.1 108.6,68.1 109.2,69.2 109.8,70.4 110.4,71.7 111.0,72.9 111.6,74.2 112.2,75.5 112.8,76.8 113.4,78.1 114.0,79.4 114.6,81.0 115.2,82.8 115.8,84.7 116.4,85.4 117.0,83.6 117.6,78.3 118.2,69.5 118.8,57.6 119.4,44.3 120.0,32.8 120.6,26.9 121.2,29.0 121.8,38.9 122.4,53.6 123.0,69.4 123.6,83.1 124.2,93.4 124.8,99.8 125.4,102.7 126.0,103.2 126.6,101.9 127.2,100.1 127.8,98.4 128.4,97.2 129.0,96.6 129.6,96.5 130.2,96.7 130.8,97.0 131.4,97.3 132.0,97.7 132.6,98.1 133.2,98.4 133.8,98.8 134.4,99.2 135.0,80.4 135.6,80.8 136.2,81.2 136.8,81.6 137.4,81.9 138.0,82.3 138.6,82.7 139.2,83.1 139.8,83.5 140.4,83.8 141.0,84.2 141.6,84.6 142.2,85.0 142.8,85.3 143.4,85.7 144.0,86.1 144.6,86.4 145.2,86.8 145.8,87.1 146.4,87.4 147.0,87.7 147.6,88.0 148.2,88.3 148.8,88.5 149.4,88.7 150.0,88.9 150.6,89.1 151.2,89.2 151.8,89.2 152.4,89.2 153.0,89.1 153.6,89.0 154.2,88.9 154.8,88.6 155.4,88.3 156.0,88.0 156.6,87.6 157.2,87.2 157.8,86.7 158.4,86.2 159.0,85.7 159.6,85.1 160.2,84.6 160.8,84.2 161.4,83.7 162.0,83.4 162.6,83.1 163.2,82.9 163.8,82.8 164.4,82.8 165.0,63.7 165.6,64.0 166.2,64.4 166.8,64.9 167.4,65.6 168.0,66.4 168.6,67.3 169.2,68.3 169.8,69.4 170.4,70.5 171.0,71.7 171.6,73.0 172.2,74.3 172.8,75.6 173.4,76.8 174.0,78.1 174.6,79.4 175.2,80.9 175.8,82.7 176.4,84.6 177.0,85.9 177.6,85.1 178.2,81.1 178.8,73.5 179.4,62.6 180.0,49.5 180.6,36.9 181.2,28.7 181.8,27.9 182.4,35.2 183.0,48.6 183.6,64.4 184.2,79.2 184.8,90.7 185.4,98.4 186.0,102.6 186.6,103.8 187.2,103.0 187.8,101.3 188.4,99.5 189.0,98.1 189.6,97.3 190.2,97.0 190.8,97.1 191.4,97.4 192.0,97.7 192.6,98.1 193.2,98.4 193.8,98.8 194.4,99.2 195.0,80.4 195.6,80.8 196.2,81.2 196.8,81.6 197.4,81.9 198.0,82.3 198.6,82.7 199.2,83.1 199.8,83.5 200.4,83.8 201.0,84.2 201.6,84.6 202.2,85.0 202.8,85.4 203.4,85.7 204.0,86.1 204.6,86.5 205.2,86.8 205.8,87.2 206.4,87.5 207.0,87.8 207.6,88.1 208.2,88.4 208.8,88.7 209.4,89.0 210.0,89.2 210.6,89.4 211.2,89.5 211.8,89.6 212.4,89.7 213.0,89.7 213.6,89.7 214.2,89.6 214.8,89.4 215.4,89.2 216.0,89.0 216.6,88.6 217.2,88.3 217.8,87.8 218.4,87.4 219.0,86.9 219.6,86.4 220.2,85.8 220.8,85.3 221.4,84.8 222.0,84.4 222.6,84.0 223.2,83.7 223.8,83.4 224.4,83.3 225.0,64.1 225.6,64.2 226.2,64.4 226.8,64.8 227.4,65.2 228.0,65.9 228.6,66.6 229.2,67.5 229.8,68.4 230.4,69.5 231.0,70.6 231.6,71.8 232.2,73.1 232.8,74.3 233.4,75.6 234.0,76.9 234.6,78.2 235.2,79.5 235.8,80.9 236.4,82.5 237.0,84.5 237.6,86.1 238.2,86.2 238.8,83.5 239.4,77.1 240.0,67.3 240.6,54.7 241.2,41.6 241.8,31.4 242.4,27.7 243.0,32.3 243.6,44.0 244.2,59.4 244.8,74.8 245.4,87.6 246.0,96.7 246.6,102.0 247.2,104.1 247.8,104.0 248.4,102.5 249.0,100.6 249.6,99.1 250.2,98.0 250.8,97.6 251.4,97.6 252.0,97.8 252.6,98.1 253.2,98.5 253.8,98.8 254.4,99.2 255.0,80.4 255.6,80.8 256.2,81.2 256.8,81.6 257.4,81.9 258.0,82.3 258.6,82.7 259.2,83.1 259.8,83.5 260.4,83.9 261.0,84.2 261.6,84.6 262.2,85.0 262.8,85.4 263.4,85.7 264.0,86.1 264.6,86.5 265.2,86.9 265.8,87.2 266.4,87.6 267.0,87.9 267.6,88.2 268.2,88.6 268.8,88.9 269.4,89.1 270.0,89.4 270.6,89.6 271.2,89.8 271.8,90.0 272.4,90.1 273.0,90.2 273.6,90.2 274.2,90.2 274.8,90.2 275.4,90.0 276.0,89.8 276.6,89.6 277.2,89.3 277.8,88.9 278.4,88.5 279.0,88.1 279.6,87.6 280.2,87.1 280.8,86.5 281.4,86.0 282.0,85.5 282.6,85.1 283.2,84.6 283.8,84.3 284.4,84.0 285.0,64.7 285.6,64.6 286.2,64.6 286.8,64.8 287.4,65.1 288.0,65.6 288.6,66.2 289.2,66.9 289.8,67.7 290.4,68.6 291.0,69.6 291.6,70.7 292.2,71.9 292.8,73.1 293.4,74.4 294.0,75.7 294.6,77.0 295.2,78.3 295.8,79.5 296.4,80.9 297.0,82.4 297.6,84.3 298.2,86.2 298.8,87.0 299.4,85.3 300.0,80.3 300.6,71.6 301.2,59.8 301.8,46.6 302.4,34.9 303.0,28.6 303.6,30.3 304.2,39.7 304.8,54.3 305.4,70.1 306.0,84.0 306.6,94.5 307.2,101.1 307.8,104.2 308.4,104.7 309.0,103.6 309.6,101.8 310.2,100.1 310.8,98.9 311.4,98.2 312.0,98.1 312.6,98.2 313.2,98.5 313.8,98.8 314.4,99.2 315.0,80.4 315.6,80.8 316.2,81.2 316.8,81.6 317.4,81.9 318.0,82.3 318.6,82.7 319.2,83.1 319.8,83.5 320.4,83.9 321.0,84.2 321.6,84.6 322.2,85.0 322.8,85.4 323.4,85.8 324.0,86.1 324.6,86.5 325.2,86.9 325.8,87.2 326.4,87.6 327.0,88.0 327.6,88.3 328.2,88.6 328.8,89.0 329.4,89.3 330.0,89.6 330.6,89.8 331.2,90.1 331.8,90.3 332.4,90.5 333.0,90.6 333.6,90.7 334.2,90.8 334.8,90.8 335.4,90.7 336.0,90.6 336.6,90.4 337.2,90.2 337.8,89.9 338.4,89.6 339.0,89.2 339.6,88.7 340.2,88.3 340.8,87.8 341.4,87.2 342.0,86.7 342.6,86.2 343.2,85.7 343.8,85.3 344.4,84.9 345.0,65.4 345.6,65.2 346.2,65.1 346.8,65.1 347.4,65.3 348.0,65.5 348.6,65.9 349.2,66.5 349.8,67.1 350.4,67.9 351.0,68.8 351.6,69.8 352.2,70.9 352.8,72.0 353.4,73.2 354.0,74.5 354.6,75.8 355.2,77.1 355.8,78.3 356.4,79.6 357.0,80.9 357.6,82.4 358.2,84.1 358.8,86.1 359.4,87.4 360.0,86.8 360.6,83.0 361.2,75.6 361.8,64.8 362.4,51.8 363.0,39.1 363.6,30.5 364.2,29.2 364.8,36.2 365.4,49.4 366.0,65.1 366.6,80.0 367.2,91.8 367.8,99.7 368.4,104.0 369.0,105.3 369.6,104.6 370.2,102.9 370.8,101.2 371.4,99.7 372.0,98.9 372.6,98.6 373.2,98.7 373.8,98.9 374.4,99.2 375.0,80.4 375.6,80.8 376.2,81.2 376.8,81.6 377.4,81.9 378.0,82.3 378.6,82.7 379.2,83.1 379.8,83.5 380.4,83.9 381.0,84.2 381.6,84.6 382.2,85.0 382.8,85.4 383.4,85.8 384.0,86.1 384.6,86.5 385.2,86.9 385.8,87.3 386.4,87.6 387.0,88.0 387.6,88.4 388.2,88.7 388.8,89.0 389.4,89.4 390.0,89.7 390.6,90.0 391.2,90.3 391.8,90.5 392.4,90.7 393.0,90.9 393.6,91.1 394.2,91.2 394.8,91.3 395.4,91.3 396.0,91.3 396.6,91.2 397.2,91.0 397.8,90.8 398.4,90.5 399.0,90.2 399.6,89.8 400.2,89.4 400.8,89.0 401.4,88.5 402.0,87.9 402.6,87.4 403.2,86.9 403.8,86.4 404.4,86.0 405.0,66.4 405.6,66.0 406.2,65.8 406.8,65.7 407.4,65.6 408.0,65.7 408.6,65.9 409.2,66.3 409.8,66.8 410.4,67.4 411.0,68.1 411.6,69.0 412.2,69.9 412.8,71.0 413.4,72.1 414.0,73.3 414.6,74.6 415.2,75.8 415.8,77.1 416.4,78.4 417.0,79.7 417.6,81.0 418.2,82.4 418.8,84.0 419.4,85.9 420.0,87.6 420.6,87.9 421.2,85.3 421.8,79.1 422.4,69.4 423.0,57.0 423.6,43.8 424.2,33.3 424.8,29.3 425.4,33.4 426.0,44.7 426.6,60.1 427.2,75.6 427.8,88.6 428.4,97.9 429.0,103.4 429.6,105.6 430.2,105.6 430.8,104.1 431.4,102.2 432.0,100.7 432.6,99.6 433.2,99.2 433.8,99.1 434.4,99.3 435.0,80.4 435.6,80.8 436.2,81.2 436.8,81.6 437.4,81.9 438.0,82.3 438.6,82.7 439.2,83.1 439.8,83.5 440.4,83.9 441.0,84.2 441.6,84.6 442.2,85.0 442.8,85.4 443.4,85.8 444.0,86.1 444.6,86.5 445.2,86.9 445.8,87.3 446.4,87.7 447.0,88.0 447.6,88.4 448.2,88.8 448.8,89.1 449.4,89.4 450.0,89.8 450.6,90.1 451.2,90.4 451.8,90.7 452.4,90.9 453.0,91.2 453.6,91.4 454.2,91.6 454.8,91.7 455.4,91.8 456.0,91.8 456.6,91.8 457.2,91.7 457.8,91.6 458.4,91.4 459.0,91.2 459.6,90.9 460.2,90.5 460.8,90.1 461.4,89.6 462.0,89.2 462.6,88.7 463.2,88.1 463.8,87.6 464.4,87.1 465.0,67.4 465.6,67.0 466.2,66.7 466.8,66.4 467.4,66.2 468.0,66.1 468.6,66.2 469.2,66.4 469.8,66.7 470.4,67.1 471.0,67.7 471.6,68.4 472.2,69.2 472.8,70.1 473.4,71.1 474.0,72.2 474.6,73.4 475.2,74.6 475.8,75.9 476.4,77.2 477.0,78.5 477.6,79.8 478.2,81.0 478.8,82.4 479.4,83.9 480.0,85.7 480.6,87.6 481.2,88.6 481.8,87.1 482.4,82.2 483.0,73.7 483.6,62.1 484.2,48.8 484.8,37.0 485.4,30.3 486.0,31.5 486.6,40.6 487.2,55.0 487.8,70.8 488.4,84.9 489.0,95.6 489.6,102.3 490.2,105.7 490.8,106.3 491.4,105.2 492.0,103.4 492.6,101.7 493.2,100.5 493.8,99.8 494.4,99.6 495.0,80.6 495.6,80.8 496.2,81.2 496.8,81.6 497.4,81.9 498.0,82.3 498.6,82.7 499.2,83.1 499.8,83.5 500.4,83.9 501.0,84.2 501.6,84.6 502.2,85.0 502.8,85.4 503.4,85.8 504.0,86.2 504.6,86.5 505.2,86.9 505.8,87.3 506.4,87.7 507.0,88.0 507.6,88.4 508.2,88.8 508.8,89.1 509.4,89.5 510.0,89.8 510.6,90.2 511.2,90.5 511.8,90.8 512.4,91.1 513.0,91.4 513.6,91.6 514.2,91.8 514.8,92.0 515.4,92.2 516.0,92.3 516.6,92.3 517.2,92.3 517.8,92.3 518.4,92.2 519.0,92.0 519.6,91.8 520.2,91.5 520.8,91.2 521.4,90.8 522.0,90.3 522.6,89.9 523.2,89.3 523.8,88.8 524.4,88.3 525.0,68.6 525.6,68.1 526.2,67.7 526.8,67.3 527.4,67.0 528.0,66.8 528.6,66.7 529.2,66.7 529.8,66.8 530.4,67.1 531.0,67.5 531.6,68.0 532.2,68.6 532.8,69.4 533.4,70.3 534.0,71.3 534.6,72.4 535.2,73.5 535.8,74.7 536.4,76.0 537.0,77.2 537.6,78.5 538.2,79.8 538.8,81.1 539.4,82.4 540.0,83.8 540.6,85.6 541.2,87.5 541.8,88.9 542.4,88.5 543.0,84.8 543.6,77.6 544.2,67.0 544.8,54.0 545.4,41.3 546.0,32.4 546.6,30.6 547.2,37.2 547.8,50.1 548.4,65.8 549.0,80.8 549.6,92.8 550.2,100.9 550.8,105.4 551.4,106.9 552.0,106.3 552.6,104.6 553.2,102.8 553.8,101.4 554.4,100.5 555.0,81.0 555.6,81.0 556.2,81.2 556.8,81.6 557.4,81.9 558.0,82.3 558.6,82.7 559.2,83.1 559.8,83.5 560.4,83.9 561.0,84.2 561.6,84.6 562.2,85.0 562.8,85.4 563.4,85.8 564.0,86.2 564.6,86.5 565.2,86.9 565.8,87.3 566.4,87.7 567.0,88.1 567.6,88.4 568.2,88.8 568.8,89.2 569.4,89.5 570.0,89.9 570.6,90.2 571.2,90.6 571.8,90.9 572.4,91.2 573.0,91.5 573.6,91.8 574.2,92.1 574.8,92.3 575.4,92.5 576.0,92.6 576.6,92.7 577.2,92.8 577.8,92.8 578.4,92.8 579.0,92.7 579.6,92.6 580.2,92.4 580.8,92.1 581.4,91.8 582.0,91.4 582.6,91.0 583.2,90.5 583.8,90.0 584.4,89.5 585.0,69.8 585.6,69.3 586.2,68.8 586.8,68.4 587.4,67.9 588.0,67.6 588.6,67.4 589.2,67.2 589.8,67.2 590.4,67.3 591.0,67.5 591.6,67.8 592.2,68.3 592.8,68.9 593.4,69.6 594.0,70.5 594.6,71.4 595.2,72.5 595.8,73.6 596.4,74.8 597.0,76.0 597.6,77.3 598.2,78.6 598.8,79.9 599.4,81.2 600.0,82.5 600.6,83.8 601.2,85.4 601.8,87.4 602.4,89.1 603.0,89.5 603.6,87.0 604.2,81.1 604.8,71.6 605.4,59.3 606.0,46.0 606.6,35.3 607.2,30.8 607.8,34.5 608.4,45.6 609.0,60.8 609.6,76.3 610.2,89.5 610.8,99.0 611.4,104.7 612.0,107.1 612.6,107.2 613.2,105.8 613.8,103.9 614.4,102.3 615.0,82.0 615.6,81.5 616.2,81.5 616.8,81.7 617.4,82.0 618.0,82.3 618.6,82.7 619.2,83.1 619.8,83.5 620.4,83.9 621.0,84.2 621.6,84.6 622.2,85.0 622.8,85.4 623.4,85.8 624.0,86.2 624.6,86.5 625.2,86.9 625.8,87.3 626.4,87.7 627.0,88.1 627.6,88.4 628.2,88.8 628.8,89.2 629.4,89.6 630.0,89.9 630.6,90.3 631.2,90.6 631.8,91.0 632.4,91.3 633.0,91.6 633.6,91.9 634.2,92.2 634.8,92.5 635.4,92.7 636.0,92.9 636.6,93.1 637.2,93.2 637.8,93.3 638.4,93.4 639.0,93.3 639.6,93.3 640.2,93.2 640.8,93.0 641.4,92.7 642.0,92.4 642.6,92.1 643.2,91.7 643.8,91.2 644.4,90.7 645.0,71.0 645.6,70.5 646.2,70.0 646.8,69.5 647.4,69.0 648.0,68.6 648.6,68.2 649.2,68.0 649.8,67.8 650.4,67.7 651.0,67.7 651.6,67.9 652.2,68.2 652.8,68.6 653.4,69.2 654.0,69.9 654.6,70.7 655.2,71.6 655.8,72.6 656.4,73.7 657.0,74.9 657.6,76.1 658.2,77.4 658.8,78.7 659.4,80.0 660.0,81.2 660.6,82.5 661.2,83.8 661.8,85.4 662.4,87.2 663.0,89.1 663.6,90.1 664.2,88.8 664.8,84.1 665.4,75.8 666.0,64.3 666.6,51.1 667.2,39.1 667.8,32.0 668.4,32.8 669.0,41.5 669.6,55.7 670.2,71.5 670.8,85.8 671.4,96.6 672.0,103.6 672.6,107.1 673.2,107.9 673.8,106.9 674.4,105.1 675.0,84.2 675.6,82.9 676.2,82.2 676.8,82.0 677.4,82.1 678.0,82.4 678.6,82.7 679.2,83.1 679.8,83.5 680.4,83.9 681.0,84.2 681.6,84.6 682.2,85.0 682.8,85.4 683.4,85.8 684.0,86.2 684.6,86.5 685.2,86.9 685.8,87.3 686.4,87.7 687.0,88.1 687.6,88.5 688.2,88.8 688.8,89.2 689.4,89.6 690.0,90.0 690.6,90.3 691.2,90.7 691.8,91.0 692.4,91.4 693.0,91.7 693.6,92.0 694.2,92.4 694.8,92.6 695.4,92.9 696.0,93.2 696.6,93.4 697.2,93.6 697.8,93.7 698.4,93.8 699.0,93.9 699.6,93.9 700.2,93.8 700.8,93.7 701.4,93.6 702.0,93.3 702.6,93.1 703.2,92.7 703.8,92.3 704.4,91.9 705.0,72.2 705.6,71.7 706.2,71.2 706.8,70.7 707.4,70.2 708.0,69.7 708.6,69.3 709.2,68.9 709.8,68.6 710.4,68.4 711.0,68.2 711.6,68.2 712.2,68.4 712.8,68.6 713.4,69.0 714.0,69.5 714.6,70.1 715.2,70.9 715.8,71.8 716.4,72.8 717.0,73.9 717.6,75.0 718.2,76.2 718.8,77.5 719.4,78.7 720.0,80.0 720.6,81.3 721.2,82.6 721.8,83.9 722.4,85.3 723.0,87.0 723.6,89.0 724.2,90.5 724.8,90.1 725.4,86.7 726.0,79.7 726.6,69.2 727.2,56.3 727.8,43.4 728.4,34.2 729.0,32.1 729.6,38.2 730.2,50.9 730.8,66.5 731.4,81.6 732.0,93.8 732.6,102.1 733.2,106.8 733.8,108.4 734.4,107.9 735.0,87.1 735.6,85.2 736.2,83.8 736.8,82.9 737.4,82.5 738.0,82.5 738.6,82.8 739.2,83.1 739.8,83.5 740.4,83.9 741.0,84.2 741.6,84.6 742.2,85.0 742.8,85.4 743.4,85.8 744.0,86.2 744.6,86.5 745.2,86.9 745.8,87.3 746.4,87.7 747.0,88.1 747.6,88.5 748.2,88.8 748.8,89.2 749.4,89.6 750.0,90.0 750.6,90.3 751.2,90.7 751.8,91.1 752.4,91.4 753.0,91.8 753.6,92.1 754.2,92.5 754.8,92.8 755.4,93.1 756.0,93.3 756.6,93.6 757.2,93.8 757.8,94.0 758.4,94.2 759.0,94.3 759.6,94.4 760.2,94.4 760.8,94.4 761.4,94.3 762.0,94.1 762.6,93.9 763.2,93.7 763.8,93.4 764.4,93.0 765.0,73.4 765.6,72.9 766.2,72.4 766.8,71.9 767.4,71.4 768.0,70.9 768.6,70.4 769.2,69.9 769.8,69.5 770.4,69.2 771.0,68.9 771.6,68.8 772.2,68.7 772.8,68.8 773.4,69.0 774.0,69.4 774.6,69.8 775.2,70.4 775.8,71.2 776.4,72.0 777.0,72.9 777.6,74.0 778.2,75.1 778.8,76.3 779.4,77.5 780.0,78.8 780.6,80.1 781.2,81.4 781.8,82.7 782.4,83.9 783.0,85.3 783.6,86.9 784.2,88.8 784.8,90.6 785.4,91.1 786.0,88.8 786.6,83.1 787.2,73.8 787.8,61.5 788.4,48.3 789.0,37.3 789.6,32.4 790.2,35.7 790.8,46.4 791.4,61.4 792.0,77.1 792.6,90.5 793.2,100.2 793.8,106.0 794.4,108.6 795.0,89.6 795.6,88.2 796.2,86.4 796.8,84.8 797.4,83.6 798.0,83.1 798.6,83.0 799.2,83.2 799.8,83.5 800.4,83.9 801.0,84.2 801.6,84.6 802.2,85.0 802.8,85.4 803.4,85.8 804.0,86.2 804.6,86.5 805.2,86.9 805.8,87.3 806.4,87.7 807.0,88.1 807.6,88.5 808.2,88.8 808.8,89.2 809.4,89.6 810.0,90.0 810.6,90.4 811.2,90.7 811.8,91.1 812.4,91.5 813.0,91.8 813.6,92.2 814.2,92.5 814.8,92.9 815.4,93.2 816.0,93.5 816.6,93.8 817.2,94.0 817.8,94.3 818.4,94.5 819.0,94.6 819.6,94.8 820.2,94.9 820.8,94.9 821.4,94.9 822.0,94.8 822.6,94.7 823.2,94.5 823.8,94.3 824.4,94.0 825.0,74.5 825.6,74.1 826.2,73.6 826.8,73.1 827.4,72.6 828.0,72.1 828.6,71.6 829.2,71.1 829.8,70.6 830.4,70.2 831.0,69.8 831.6,69.5 832.2,69.3 832.8,69.3 833.4,69.3 834.0,69.5 834.6,69.7 835.2,70.2 835.8,70.7 836.4,71.4 837.0,72.2 837.6,73.1 838.2,74.1 838.8,75.2 839.4,76.4 840.0,77.6 840.6,78.9 841.2,80.2 841.8,81.4 842.4,82.7 843.0,84.0 843.6,85.3 844.2,86.8 844.8,88.6 845.4,90.6 846.0,91.7 846.6,90.5 847.2,86.0 847.8,77.9 848.4,66.6 849.0,53.4 849.6,41.2 850.2,33.8 850.8,34.1 851.4,42.4 852.0,56.4 852.6,72.3 853.2,86.7 853.8,97.7 854.4,104.9 855.0,89.4 855.6,90.3 856.2,89.3 856.8,87.5 857.4,85.8 858.0,84.5 858.6,83.8 859.2,83.5 859.8,83.6 860.4,83.9 861.0,84.3 861.6,84.6 862.2,85.0 862.8,85.4 863.4,85.8 864.0,86.2 864.6,86.5 865.2,86.9 865.8,87.3 866.4,87.7 867.0,88.1 867.6,88.5 868.2,88.8 868.8,89.2 869.4,89.6 870.0,90.0 870.6,90.4 871.2,90.7 871.8,91.1 872.4,91.5 873.0,91.9 873.6,92.2 874.2,92.6 874.8,92.9 875.4,93.3 876.0,93.6 876.6,93.9 877.2,94.2 877.8,94.5 878.4,94.7 879.0,94.9 879.6,95.1 880.2,95.3 880.8,95.4 881.4,95.4 882.0,95.4 882.6,95.4 883.2,95.3 883.8,95.1 884.4,94.9 885.0,75.4 885.6,75.1 886.2,74.7 886.8,74.3 887.4,73.8 888.0,73.3 888.6,72.8 889.2,72.3 889.8,71.8 890.4,71.3 891.0,70.8 891.6,70.5 892.2,70.1 892.8,69.9 893.4,69.8 894.0,69.8 894.6,69.9 895.2,70.1 895.8,70.5 896.4,71.0 897.0,71.7 897.6,72.4 898.2,73.3 898.8,74.3 899.4,75.3 900.0,76.5\"/><text class=\"cap\" x=\"4\" y=\"193\">flutter · 148 bpm · 25 mm/s, 10 mm/mV</text></svg>"
 },
 {
  "id": "usmle-2026-0047",
  "exam": "usmle",
  "step": "Step 2",
  "subject": "Surgery",
  "subject_file": "Surgery",
  "subtopic": "Acute Cholangitis (Biliary Sepsis)",
  "type": "Acute Cholangitis (Biliary Sepsis)",
  "difficulty": 4,
  "created": "2026-07-14",
  "vignette": "A 68-year-old woman is brought to the emergency department with 1 day of right upper quadrant pain, fever, and yellowing of her skin. Over the past 2 hours she has become confused, and her family notes she is unusually drowsy. Vital signs and laboratory studies are shown. Abdominal ultrasound shows a dilated common bile duct (12 mm) with an echogenic focus and posterior shadowing within it. Intravenous fluids and empiric broad-spectrum antibiotics are started immediately.",
  "question": "Which of the following is the most appropriate next step in management?",
  "options": [
   "Continue antibiotics alone and reassess clinical status in 24 hours",
   "Emergency open cholecystectomy to address the biliary source of infection",
   "Discharge home with outpatient MRCP scheduled within the next week",
   "Percutaneous transhepatic drainage while withholding antibiotics until cultures return",
   "Urgent ERCP for biliary decompression following resuscitation and antibiotics"
  ],
  "answer": 5,
  "explanationText": "- 정답근거: 우상복부 통증·발열·황달(Charcot triad)에 더해 새로 발생한 저혈압과 의식변화까지 동반된 것은 Reynolds pentad로, 화농성 담관염(suppurative cholangitis)에 의한 패혈성 쇼크를 의미한다. 초기 수액소생과 경험적 항생제 투여 후에는 감염원 조절을 위한 응급 담도감압이 필요하며, ERCP가 1차 선택이다.\n- 오답감별:\n  - A: 항생제만으로는 폐쇄된 담도 내 감염원을 제거할 수 없어 패혈증이 진행할 위험이 크다. 장기부전(쇼크·의식저하)이 있는 중증에서는 반드시 담도감압이 병행되어야 한다.\n  - B: 담낭절제술은 급성 담낭염(담낭 자체 병변)의 처치이며, 총담관 폐쇄로 인한 담관염을 감압하지 못한다. 패혈성 쇼크 상태의 환자에게 즉시 개복 수술을 시행하는 것은 위험도도 지나치게 높다.\n  - C: 장기부전을 동반한 응급 상황에서 외래 재평가로 미루는 것은 치료를 지연시켜 패혈증을 악화시킨다.\n  - D: PTBD는 ERCP가 불가능할 때의 대안이 될 수 있지만, 항생제 투여를 배양결과가 나올 때까지 미루는 것은 패혈증 번들 원칙(경험적 항생제 즉시 시작)에 위배된다.\n- 임상핵심: Charcot triad(발열·황달·우상복부통)에 쇼크·의식저하가 더해진 Reynolds pentad는 담관염 중에서도 응급 담도감압이 필요한 중증 신호다. 수액소생·경험적 항생제를 즉시 시작한 뒤 ERCP(불가 시 PTBD)로 감압한다.\n- 출처: Tokyo Guidelines 2018 (TG18) for Acute Cholangitis; Sabiston Textbook of Surgery.",
  "explanationItems": [
   {
    "k": "정답근거",
    "v": "우상복부 통증·발열·황달(Charcot triad)에 더해 새로 발생한 저혈압과 의식변화까지 동반된 것은 Reynolds pentad로, 화농성 담관염(suppurative cholangitis)에 의한 패혈성 쇼크를 의미한다. 초기 수액소생과 경험적 항생제 투여 후에는 감염원 조절을 위한 응급 담도감압이 필요하며, ERCP가 1차 선택이다."
   },
   {
    "k": "오답감별",
    "v": "A: 항생제만으로는 폐쇄된 담도 내 감염원을 제거할 수 없어 패혈증이 진행할 위험이 크다. 장기부전(쇼크·의식저하)이 있는 중증에서는 반드시 담도감압이 병행되어야 한다.\nB: 담낭절제술은 급성 담낭염(담낭 자체 병변)의 처치이며, 총담관 폐쇄로 인한 담관염을 감압하지 못한다. 패혈성 쇼크 상태의 환자에게 즉시 개복 수술을 시행하는 것은 위험도도 지나치게 높다.\nC: 장기부전을 동반한 응급 상황에서 외래 재평가로 미루는 것은 치료를 지연시켜 패혈증을 악화시킨다.\nD: PTBD는 ERCP가 불가능할 때의 대안이 될 수 있지만, 항생제 투여를 배양결과가 나올 때까지 미루는 것은 패혈증 번들 원칙(경험적 항생제 즉시 시작)에 위배된다."
   },
   {
    "k": "임상핵심",
    "v": "Charcot triad(발열·황달·우상복부통)에 쇼크·의식저하가 더해진 Reynolds pentad는 담관염 중에서도 응급 담도감압이 필요한 중증 신호다. 수액소생·경험적 항생제를 즉시 시작한 뒤 ERCP(불가 시 PTBD)로 감압한다."
   },
   {
    "k": "출처",
    "v": "Tokyo Guidelines 2018 (TG18) for Acute Cholangitis; Sabiston Textbook of Surgery."
   }
  ],
  "source": "USMLE-style / MedKOS (surgery · hepatobiliary emergencies)",
  "vitals": [
   {
    "name": "혈압",
    "value": "84/54 mmHg"
   },
   {
    "name": "맥박",
    "value": "118회/분"
   },
   {
    "name": "호흡",
    "value": "24회/분"
   },
   {
    "name": "체온",
    "value": "39.2 °C"
   }
  ],
  "labs": [
   {
    "name": "총빌리루빈",
    "value": "6.8 mg/dL",
    "ref": "0.2–1.2"
   },
   {
    "name": "직접빌리루빈",
    "value": "5.1 mg/dL",
    "ref": "0–0.3"
   },
   {
    "name": "알칼리인산분해효소(ALP)",
    "value": "420 U/L",
    "ref": "44–147"
   },
   {
    "name": "AST/ALT",
    "value": "98/85 U/L",
    "ref": "< 40"
   },
   {
    "name": "백혈구",
    "value": "19,400 /mm³",
    "ref": "4,000–10,000"
   },
   {
    "name": "혈소판",
    "value": "232,000 /mm³",
    "ref": "150,000–400,000"
   }
  ],
  "appendix": {
   "가이드라인": "급성 담관염 중증도별 처치(Tokyo Guidelines 개념)\n───────────────────────────────────────────────\n중증도               정의                       처치\n경증(Grade I)         전신장기부전 없음           항생제 ± 조기 담도배액\n중등증(Grade II)      백혈구/빌리루빈/연령 등 기준 조기(24~48시간 내) 담도배액\n중증(Grade III,       장기부전 동반(쇼크·의식저하  즉시 수액소생+항생제 →\n  Reynolds pentad)     = 이 환자)                  응급 담도감압(ERCP 우선, 불가시 PTBD)\n───────────────────────────────────────────────\n",
   "최신지견": "ERCP가 기술적으로 불가능하거나 응급실에서 즉시 시행이 어려운 경우 PTBD를 대안으로 시행하되, 항생제 시작을 지연시켜서는 안 된다.",
   "참고문헌": [
    "Tokyo Guidelines 2018 (TG18) for Acute Cholangitis and Cholecystitis",
    "Sabiston Textbook of Surgery — Biliary Tract"
   ]
  },
  "figureSvg": ""
 },
 {
  "id": "usmle-2026-0048",
  "exam": "usmle",
  "step": "Step 2",
  "subject": "Pediatrics",
  "subject_file": "Pediatrics",
  "subtopic": "Kawasaki Disease (Coronary Artery Aneurysm Prevention)",
  "type": "Kawasaki Disease (Coronary Artery Aneurysm Prevention)",
  "difficulty": 4,
  "created": "2026-07-14",
  "vignette": "A 3-year-old boy has had fever ≥39°C for 5 days that has not responded to acetaminophen or ibuprofen. Examination shows bilateral non-exudative conjunctival injection, a diffusely erythematous 'strawberry' tongue, dry cracked lips, a polymorphous truncal rash, and a single tender 1.8-cm right cervical lymph node. His fingertips have begun to peel. Blood cultures obtained on admission are negative at 48 hours. Vital signs and laboratory studies are shown. Echocardiogram shows mild dilation of the left main coronary artery (z-score 2.3).",
  "question": "Which of the following is the most appropriate treatment at this time?",
  "options": [
   "Intravenous ceftriaxone pending further culture results",
   "A single dose of intravenous immunoglobulin (IVIG) plus high-dose aspirin",
   "Systemic corticosteroids as sole initial therapy",
   "Low-dose aspirin alone, without an anti-inflammatory dose",
   "Continued observation and antipyretics, with reassessment in 48 hours"
  ],
  "answer": 2,
  "explanationText": "- 정답근거: 5일 이상 지속되는 고열에 결막충혈·구강점막변화·발진·사지말단변화·경부림프절병증 중 4가지 이상이 동반되고, 무균성 농뇨·혈소판증가증·관상동맥 경도 확장까지 확인되어 가와사키병 진단기준을 충족한다. 발병 10일 이내 IVIG 1회 투여와 고용량(항염증 용량) 아스피린 병용이 관상동맥류 위험을 낮추는 표준 초기 치료다.\n- 오답감별:\n  - A: 48시간 혈액배양이 음성으로 세균감염이 배제된 상태이며, 가와사키병은 항생제에 반응하지 않는 혈관염이다.\n  - C: 전신 스테로이드는 표준 1차 단독요법이 아니며, IVIG에 반응하지 않는 저항성 환자나 관상동맥류 고위험군에서 IVIG에 추가하는 보조요법으로 사용한다.\n  - D: 급성기에는 항혈소판 목적의 저용량이 아니라 항염증 목적의 고용량 아스피린이 필요하며, 해열되고 안정화된 이후에 저용량으로 전환한다.\n  - E: 이미 관상동맥 확장 소견이 나타난 상태에서 치료를 지연시키면 관상동맥류로 진행할 위험이 유의하게 증가한다.\n- 임상핵심: 5일 이상 발열 + 임상기준 4/5 충족 → 발병 10일 이내 IVIG 1회 + 고용량 아스피린이 치료의 핵심이며, 목표는 관상동맥류 예방이다.\n- 출처: AHA Scientific Statement on Kawasaki Disease; Nelson Textbook of Pediatrics.",
  "explanationItems": [
   {
    "k": "정답근거",
    "v": "5일 이상 지속되는 고열에 결막충혈·구강점막변화·발진·사지말단변화·경부림프절병증 중 4가지 이상이 동반되고, 무균성 농뇨·혈소판증가증·관상동맥 경도 확장까지 확인되어 가와사키병 진단기준을 충족한다. 발병 10일 이내 IVIG 1회 투여와 고용량(항염증 용량) 아스피린 병용이 관상동맥류 위험을 낮추는 표준 초기 치료다."
   },
   {
    "k": "오답감별",
    "v": "A: 48시간 혈액배양이 음성으로 세균감염이 배제된 상태이며, 가와사키병은 항생제에 반응하지 않는 혈관염이다.\nC: 전신 스테로이드는 표준 1차 단독요법이 아니며, IVIG에 반응하지 않는 저항성 환자나 관상동맥류 고위험군에서 IVIG에 추가하는 보조요법으로 사용한다.\nD: 급성기에는 항혈소판 목적의 저용량이 아니라 항염증 목적의 고용량 아스피린이 필요하며, 해열되고 안정화된 이후에 저용량으로 전환한다.\nE: 이미 관상동맥 확장 소견이 나타난 상태에서 치료를 지연시키면 관상동맥류로 진행할 위험이 유의하게 증가한다."
   },
   {
    "k": "임상핵심",
    "v": "5일 이상 발열 + 임상기준 4/5 충족 → 발병 10일 이내 IVIG 1회 + 고용량 아스피린이 치료의 핵심이며, 목표는 관상동맥류 예방이다."
   },
   {
    "k": "출처",
    "v": "AHA Scientific Statement on Kawasaki Disease; Nelson Textbook of Pediatrics."
   }
  ],
  "source": "USMLE-style / MedKOS (pediatrics · vasculitis)",
  "vitals": [
   {
    "name": "혈압",
    "value": "96/60 mmHg"
   },
   {
    "name": "맥박",
    "value": "138회/분"
   },
   {
    "name": "호흡",
    "value": "26회/분"
   },
   {
    "name": "체온",
    "value": "39.8 °C"
   }
  ],
  "labs": [
   {
    "name": "적혈구침강속도(ESR)",
    "value": "68 mm/hr",
    "ref": "< 20"
   },
   {
    "name": "C-반응단백(CRP)",
    "value": "9.8 mg/dL",
    "ref": "< 0.5"
   },
   {
    "name": "혈소판",
    "value": "620,000 /mm³",
    "ref": "150,000–450,000"
   },
   {
    "name": "혈청 알부민",
    "value": "2.9 g/dL",
    "ref": "3.5–5.0"
   },
   {
    "name": "소변 백혈구(무균성 농뇨)",
    "value": "30/HPF, 소변배양 음성",
    "ref": "< 5/HPF"
   },
   {
    "name": "혈액배양(48시간)",
    "value": "음성",
    "ref": "음성"
   }
  ],
  "appendix": {
   "가이드라인": "가와사키병 임상기준 및 치료 (관상동맥류 예방)\n───────────────────────────────────────────────\n주요 임상기준(발열≥5일 + 아래 5개 중 ≥4개)\n  · 양측 비삼출성 결막충혈\n  · 구강점막 변화(딸기혀·구순균열)\n  · 다형성 발진\n  · 사지말단 변화(급성기 부종/홍반 → 아급성기 낙설)\n  · 경부 림프절병증(≥1.5cm, 대개 단측)\n치료: 발병 10일 이내 IVIG 2g/kg 1회 + 고용량 아스피린(항염증 용량)\n      → 해열 후 저용량 아스피린(항혈소판 용량)으로 전환\n      IVIG 저항성/고위험군: 추가 IVIG 또는 스테로이드 보조\n───────────────────────────────────────────────\n",
   "최신지견": "치료 지연 시 관상동맥류 발생률이 최대 25%까지 보고되나, 적절한 IVIG 치료로 약 4% 미만으로 감소한다.",
   "참고문헌": [
    "AHA Scientific Statement — Diagnosis, Treatment, and Long-Term Management of Kawasaki Disease",
    "Nelson Textbook of Pediatrics — Kawasaki Disease"
   ]
  },
  "figureSvg": ""
 },
 {
  "id": "usmle-2026-0049",
  "exam": "usmle",
  "step": "Step 1",
  "subject": "Biochemistry",
  "subject_file": "Biochemistry",
  "subtopic": "Ornithine Transcarbamylase (OTC) Deficiency — Urea Cycle Biochemistry",
  "type": "Ornithine Transcarbamylase (OTC) Deficiency — Urea Cycle Biochemistry",
  "difficulty": 5,
  "created": "2026-07-21",
  "vignette": "A 3-day-old male newborn, born after an uncomplicated term vaginal delivery, becomes progressively lethargic and refuses feeds over the past 24 hours. He has had several episodes of non-bilious vomiting without diarrhea or fever. His mother reports that two maternal uncles died in infancy of an undiagnosed illness. Vital signs and laboratory studies are shown.",
  "question": "Which of the following additional findings would most strongly support this infant's specific enzyme defect over other proximal urea cycle disorders?",
  "options": [
   "Elevated urine orotic acid with low plasma citrulline",
   "Markedly elevated plasma citrulline with elevated urine orotic acid",
   "Low or undetectable urine orotic acid with low plasma citrulline",
   "Elevated plasma propionylcarnitine (C3) with normal urine orotic acid",
   "Elevated plasma lysine with low plasma ornithine"
  ],
  "answer": 1,
  "explanationText": "- 정답근거: 신생아기 발병, 수유거부·기면·호흡성 알칼리증을 동반한 고암모니아혈증(암모니아 285 μmol/L)이면서 혈당·젖산·간효소가 정상이고 BUN이 낮아 요소 생성 저하가 시사된다. 모계 삼촌들의 영아기 사망은 X-linked 유전을 암시한다. OTC는 카르바모일인산을 시트룰린으로 전환하는 효소로, 결핍 시 카르바모일인산이 축적되어 세포질 피리미딘 합성경로로 유입되며 요오로트산이 상승하고, 동시에 하류 산물인 시트룰린은 낮아진다.\n- 오답감별:\n  - (B) 시트룰린이 현저히 상승하면 OTC보다 하류 효소인 ASS1 결핍(시트룰린혈증)을 시사한다 — OTC는 시트룰린 생성 단계이므로 결핍 시 시트룰린이 오히려 낮다.\n  - (C) 요오로트산이 낮거나 검출되지 않으면 카르바모일인산 자체가 만들어지지 않는 CPS1 또는 NAGS 결핍을 시사한다 — OTC 결핍에서는 카르바모일인산이 축적되어 오로트산이 오히려 상승한다.\n  - (D) 프로피오닐카르니틴 상승은 유기산혈증(2차성 고암모니아혈증)의 표지자이며, 통상 대사성 산증을 동반한다 — 본 환아는 산증이 아닌 호흡성 알칼리증 소견이라 원발 요소회로 결손에 부합한다.\n  - (E) 리신 상승·오르니틴 저하는 고오르니틴혈증-고암모니아혈증-호모시트룰린뇨증(HHH 증후군, 오르니틴 전위효소 결핍)의 소견이며 요오로트산·시트룰린 패턴이 다르다.\n- 임상핵심: 신생아 고암모니아혈증에서 대사성 산증이 없다면 요소회로 결손을 우선 의심하고, 요오로트산·혈장 시트룰린 조합으로 OTC(오로트산↑·시트룰린↓) vs CPS1/NAGS(오로트산↓·시트룰린↓) vs ASS1(오로트산↑·시트룰린↑↑)을 감별한다.\n- 출처: Nelson Textbook of Pediatrics; Lippincott Biochemistry — Urea Cycle Disorders.",
  "explanationItems": [
   {
    "k": "정답근거",
    "v": "신생아기 발병, 수유거부·기면·호흡성 알칼리증을 동반한 고암모니아혈증(암모니아 285 μmol/L)이면서 혈당·젖산·간효소가 정상이고 BUN이 낮아 요소 생성 저하가 시사된다. 모계 삼촌들의 영아기 사망은 X-linked 유전을 암시한다. OTC는 카르바모일인산을 시트룰린으로 전환하는 효소로, 결핍 시 카르바모일인산이 축적되어 세포질 피리미딘 합성경로로 유입되며 요오로트산이 상승하고, 동시에 하류 산물인 시트룰린은 낮아진다."
   },
   {
    "k": "오답감별",
    "v": "(B) 시트룰린이 현저히 상승하면 OTC보다 하류 효소인 ASS1 결핍(시트룰린혈증)을 시사한다 — OTC는 시트룰린 생성 단계이므로 결핍 시 시트룰린이 오히려 낮다.\n(C) 요오로트산이 낮거나 검출되지 않으면 카르바모일인산 자체가 만들어지지 않는 CPS1 또는 NAGS 결핍을 시사한다 — OTC 결핍에서는 카르바모일인산이 축적되어 오로트산이 오히려 상승한다.\n(D) 프로피오닐카르니틴 상승은 유기산혈증(2차성 고암모니아혈증)의 표지자이며, 통상 대사성 산증을 동반한다 — 본 환아는 산증이 아닌 호흡성 알칼리증 소견이라 원발 요소회로 결손에 부합한다.\n(E) 리신 상승·오르니틴 저하는 고오르니틴혈증-고암모니아혈증-호모시트룰린뇨증(HHH 증후군, 오르니틴 전위효소 결핍)의 소견이며 요오로트산·시트룰린 패턴이 다르다."
   },
   {
    "k": "임상핵심",
    "v": "신생아 고암모니아혈증에서 대사성 산증이 없다면 요소회로 결손을 우선 의심하고, 요오로트산·혈장 시트룰린 조합으로 OTC(오로트산↑·시트룰린↓) vs CPS1/NAGS(오로트산↓·시트룰린↓) vs ASS1(오로트산↑·시트룰린↑↑)을 감별한다."
   },
   {
    "k": "출처",
    "v": "Nelson Textbook of Pediatrics; Lippincott Biochemistry — Urea Cycle Disorders."
   }
  ],
  "source": "USMLE-style / MedKOS (biochemistry · urea cycle)",
  "vitals": [
   {
    "name": "체온",
    "value": "36.8 °C"
   },
   {
    "name": "맥박",
    "value": "168회/분"
   },
   {
    "name": "호흡",
    "value": "68회/분"
   },
   {
    "name": "혈압",
    "value": "68/40 mmHg"
   }
  ],
  "labs": [
   {
    "name": "혈장 암모니아",
    "value": "285 μmol/L",
    "ref": "< 50"
   },
   {
    "name": "혈당",
    "value": "82 mg/dL",
    "ref": "70–100"
   },
   {
    "name": "정맥혈 pH",
    "value": "7.48",
    "ref": "7.35–7.45"
   },
   {
    "name": "혈청 젖산",
    "value": "1.3 mmol/L",
    "ref": "0.5–2.2"
   },
   {
    "name": "혈중요소질소(BUN)",
    "value": "3 mg/dL",
    "ref": "7–20"
   },
   {
    "name": "AST/ALT",
    "value": "28/24 U/L",
    "ref": "< 40"
   }
  ],
  "appendix": {
   "가이드라인": "신생아 고암모니아혈증 감별 (요소회로 결손 vs 유기산혈증)\n───────────────────────────────────────────────\n소견 패턴 → 추정 진단\n  · 요오로트산↑ + 혈장 시트룰린↓  → OTC 결핍(X-linked, 가장 흔함)\n  · 요오로트산↓/미검출 + 시트룰린↓ → CPS1 또는 NAGS 결핍(상염색체 열성)\n  · 요오로트산↑ + 시트룰린 현저↑  → 시트룰린혈증(ASS1 결핍)\n  · 프로피오닐카르니틴(C3)↑, 대사성 산증 동반 → 유기산혈증(2차성 고암모니아혈증)\n공통 초기처치: 단백질 섭취 중단, 정맥 포도당으로 이화작용 억제, 암모니아 제거\n(투석/스캐빈저제) — 효소별 확진은 소변 유기산·혈장 아미노산 분석으로.\n",
   "최신지견": "OTC 결핍은 X-linked이나 여성 보인자도 이화작용 스트레스(감염·분만 후)로 발현될 수 있다.",
   "참고문헌": [
    "Nelson Textbook of Pediatrics — Inborn Errors of Urea Cycle Metabolism",
    "Lippincott Biochemistry — Urea Cycle Disorders"
   ]
  },
  "figureSvg": ""
 },
 {
  "id": "usmle-2026-0050",
  "exam": "usmle",
  "step": "Step 1",
  "subject": "Immunology",
  "subject_file": "Immunology",
  "subtopic": "Chronic Granulomatous Disease — Phagocyte NADPH Oxidase Defect",
  "type": "Chronic Granulomatous Disease — Phagocyte NADPH Oxidase Defect",
  "difficulty": 5,
  "created": "2026-07-21",
  "vignette": "An 18-month-old boy is brought to the hospital with a 4-day history of fever and a painful, fluctuant perianal mass. This is his third hospitalization for a deep soft-tissue abscess in the past year; a prior admission was for pneumonia with a right-upper-lobe nodule on chest imaging that grew Aspergillus species on culture. His maternal uncle had a similar history of recurrent infections in childhood. Vital signs and laboratory studies are shown.",
  "question": "Which of the following is the most likely underlying defect?",
  "options": [
   "Defect in myeloperoxidase (MPO) within neutrophil phagolysosomes",
   "Deficiency of terminal complement components C5 through C9",
   "Deficiency of the IL-12/IFN-γ signaling axis",
   "Defect in the phagocyte NADPH oxidase complex (gp91-phox)",
   "Mutation in the Wiskott–Aldrich syndrome protein (WASP) gene"
  ],
  "answer": 4,
  "explanationText": "- 정답근거: 카탈라아제양성균(Serratia marcescens)에 의한 반복 심부농양과 침습성 아스페르길루스 폐렴이라는 조합은 호중구·대식세포의 산화폭발(respiratory burst) 결함을 강하게 시사한다. IgG·보체(CH50)가 정상이라 체액성·보체 경로는 정상이고, 모계 삼촌의 유사 병력은 X-linked 유전(NADPH oxidase의 gp91-phox 소단위 유전자는 X염색체에 위치)과 부합해 만성육아종병(CGD)이 가장 가능성 높다.\n- 오답감별:\n  - (A) MPO 결핍은 대개 무증상이거나 경미한 임상경과를 보이며, 카탈라아제양성균에 의한 반복 침습성 감염 양상과는 거리가 있다.\n  - (B) 말단보체(C5–C9) 결핍은 주로 나이세리아균(수막구균·임균) 반복 감염으로 나타나며 CH50이 저하되어야 하는데 본 환아는 CH50이 정상이다.\n  - (C) IL-12/IFN-γ축 결핍은 비결핵항산균·살모넬라 등 세포내 병원체에 취약하게 만들며, 카탈라아제양성균·진균 조합과는 전형적 패턴이 다르다.\n  - (E) WAS는 습진과 미세혈소판을 동반한 혈소판감소증이 특징적으로 동반되는데 본 증례에는 그런 소견이 없다.\n- 임상핵심: 카탈라아제양성균+진균 반복 침습감염이면서 IgG·보체가 정상이면 NADPH oxidase 결핍(만성육아종병)을 우선 의심하고 DHR 유세포검사로 확진한다.\n- 출처: Nelson Textbook of Pediatrics; Janeway's Immunobiology.",
  "explanationItems": [
   {
    "k": "정답근거",
    "v": "카탈라아제양성균(Serratia marcescens)에 의한 반복 심부농양과 침습성 아스페르길루스 폐렴이라는 조합은 호중구·대식세포의 산화폭발(respiratory burst) 결함을 강하게 시사한다. IgG·보체(CH50)가 정상이라 체액성·보체 경로는 정상이고, 모계 삼촌의 유사 병력은 X-linked 유전(NADPH oxidase의 gp91-phox 소단위 유전자는 X염색체에 위치)과 부합해 만성육아종병(CGD)이 가장 가능성 높다."
   },
   {
    "k": "오답감별",
    "v": "(A) MPO 결핍은 대개 무증상이거나 경미한 임상경과를 보이며, 카탈라아제양성균에 의한 반복 침습성 감염 양상과는 거리가 있다.\n(B) 말단보체(C5–C9) 결핍은 주로 나이세리아균(수막구균·임균) 반복 감염으로 나타나며 CH50이 저하되어야 하는데 본 환아는 CH50이 정상이다.\n(C) IL-12/IFN-γ축 결핍은 비결핵항산균·살모넬라 등 세포내 병원체에 취약하게 만들며, 카탈라아제양성균·진균 조합과는 전형적 패턴이 다르다.\n(E) WAS는 습진과 미세혈소판을 동반한 혈소판감소증이 특징적으로 동반되는데 본 증례에는 그런 소견이 없다."
   },
   {
    "k": "임상핵심",
    "v": "카탈라아제양성균+진균 반복 침습감염이면서 IgG·보체가 정상이면 NADPH oxidase 결핍(만성육아종병)을 우선 의심하고 DHR 유세포검사로 확진한다."
   },
   {
    "k": "출처",
    "v": "Nelson Textbook of Pediatrics; Janeway's Immunobiology."
   }
  ],
  "source": "USMLE-style / MedKOS (immunology · phagocyte disorders)",
  "vitals": [
   {
    "name": "혈압",
    "value": "92/58 mmHg"
   },
   {
    "name": "맥박",
    "value": "128회/분"
   },
   {
    "name": "호흡",
    "value": "26회/분"
   },
   {
    "name": "체온",
    "value": "39.2 °C"
   }
  ],
  "labs": [
   {
    "name": "백혈구(WBC)",
    "value": "18,200 /mm³",
    "ref": "5,000–15,000"
   },
   {
    "name": "호중구 절대수(ANC)",
    "value": "6,100 /mm³",
    "ref": "1,500–8,000"
   },
   {
    "name": "혈청 IgG",
    "value": "980 mg/dL",
    "ref": "700–1,600"
   },
   {
    "name": "보체 CH50",
    "value": "48 U/mL",
    "ref": "41–90"
   },
   {
    "name": "C-반응단백(CRP)",
    "value": "11.8 mg/dL",
    "ref": "< 0.5"
   },
   {
    "name": "혈액배양",
    "value": "Serratia marcescens 동정",
    "ref": "무성장"
   }
  ],
  "appendix": {
   "가이드라인": "반복 감염 소아 — 면역결핍 유형별 특징 감별\n───────────────────────────────────────────────\n임상 단서 → 의심 진단\n  · 카탈라아제양성균(Serratia·Staph·Burkholderia)+진균(Aspergillus) 반복감염, IgG·보체 정상\n    → 만성육아종병(NADPH oxidase 결핍)\n  · 나이세리아균 반복 수막염/균혈증 → 말단보체(C5–C9) 결핍\n  · 비결핵항산균·살모넬라 반복감염 → IL-12/IFN-γ축 결핍\n  · 습진+혈소판감소증(작은 혈소판)+반복감염 → Wiskott–Aldrich 증후군\n  · 화농성 세균 반복감염+제대탈락 지연 → 백혈구부착결핍(LAD)\n확진: 디하이드로로다민(DHR) 유세포검사로 호중구 산화폭발 감소 확인.\n",
   "최신지견": "DHR 검사가 과거 NBT 검사보다 민감도가 높아 현재 1차 선별검사로 표준화되어 있다.",
   "참고문헌": [
    "Nelson Textbook of Pediatrics — Chronic Granulomatous Disease",
    "Janeway's Immunobiology — Phagocyte Deficiencies"
   ]
  },
  "figureSvg": ""
 },
 {
  "id": "usmle-2026-0051",
  "exam": "usmle",
  "step": "Step 1",
  "subject": "Pathology",
  "subject_file": "Pathology",
  "subtopic": "AL (Primary) Amyloidosis — Source of Amyloidogenic Protein",
  "type": "AL (Primary) Amyloidosis — Source of Amyloidogenic Protein",
  "difficulty": 4,
  "created": "2026-07-21",
  "vignette": "A 58-year-old man presents with 6 months of progressive lower-extremity edema, fatigue, and foamy urine. He has no history of diabetes, chronic infection, autoimmune disease, or dialysis. On examination he has macroglossia and easy bruising around the eyes after routine phlebotomy. Serum protein electrophoresis shows a monoclonal spike in the gamma region. A renal biopsy demonstrates extracellular deposits that stain with Congo red and show apple-green birefringence under polarized light. Vital signs and laboratory studies are shown.",
  "question": "Which of the following is the most likely underlying source of the amyloidogenic protein in this patient?",
  "options": [
   "Serum amyloid A protein produced during chronic inflammation",
   "Clonal plasma cells producing misfolded immunoglobulin light chains",
   "Mutant transthyretin protein synthesized by the liver",
   "β2-microglobulin accumulation from long-term dialysis",
   "Islet amyloid polypeptide deposition in pancreatic islets"
  ],
  "answer": 2,
  "explanationText": "- 정답근거: 단클론감마글로불린증(혈청단백전기영동 gamma 스파이크), 유리경쇄비의 뚜렷한 편향(0.08, 정상 0.26–1.65), 신증후군, 대설증, 경미한 외상 후 안와주위 자반은 모두 클론성 형질세포가 만든 오접힘 면역글로불린 경쇄가 조직에 침착하는 AL 아밀로이드증을 시사한다. 만성염증질환·투석·당뇨·가족력이 모두 없어 다른 유형이 배제된다.\n- 오답감별:\n  - (A) SAA 유래 AA 아밀로이드증은 류마티스관절염 등 만성염증질환을 기저로 하는데 본 환자는 그런 병력이 없다.\n  - (C) 변이 트랜스티레틴(ATTR)에 의한 아밀로이드증은 보통 가족력과 말초신경병증·심근병증을 동반하는데 제시된 소견과 맞지 않는다.\n  - (D) β2-마이크로글로불린 아밀로이드증은 수년 이상 장기 혈액투석 환자에서 발생하는데 본 환자는 투석력이 없다.\n  - (E) 췌도 아밀린 침착은 제2형 당뇨병 환자의 췌도에 국한되며 전신 신증후군을 설명하지 못하고 공복혈당도 정상이다.\n- 임상핵심: 단클론감마글로불린증 + 유리경쇄비 편향 + 신증후군/대설증/자반 조합이면 AL 아밀로이드증(형질세포 이상질환)을 우선 의심한다.\n- 출처: Robbins Basic Pathology; UpToDate — Diagnosis of AL Amyloidosis.",
  "explanationItems": [
   {
    "k": "정답근거",
    "v": "단클론감마글로불린증(혈청단백전기영동 gamma 스파이크), 유리경쇄비의 뚜렷한 편향(0.08, 정상 0.26–1.65), 신증후군, 대설증, 경미한 외상 후 안와주위 자반은 모두 클론성 형질세포가 만든 오접힘 면역글로불린 경쇄가 조직에 침착하는 AL 아밀로이드증을 시사한다. 만성염증질환·투석·당뇨·가족력이 모두 없어 다른 유형이 배제된다."
   },
   {
    "k": "오답감별",
    "v": "(A) SAA 유래 AA 아밀로이드증은 류마티스관절염 등 만성염증질환을 기저로 하는데 본 환자는 그런 병력이 없다.\n(C) 변이 트랜스티레틴(ATTR)에 의한 아밀로이드증은 보통 가족력과 말초신경병증·심근병증을 동반하는데 제시된 소견과 맞지 않는다.\n(D) β2-마이크로글로불린 아밀로이드증은 수년 이상 장기 혈액투석 환자에서 발생하는데 본 환자는 투석력이 없다.\n(E) 췌도 아밀린 침착은 제2형 당뇨병 환자의 췌도에 국한되며 전신 신증후군을 설명하지 못하고 공복혈당도 정상이다."
   },
   {
    "k": "임상핵심",
    "v": "단클론감마글로불린증 + 유리경쇄비 편향 + 신증후군/대설증/자반 조합이면 AL 아밀로이드증(형질세포 이상질환)을 우선 의심한다."
   },
   {
    "k": "출처",
    "v": "Robbins Basic Pathology; UpToDate — Diagnosis of AL Amyloidosis."
   }
  ],
  "source": "USMLE-style / MedKOS (pathology · amyloidosis)",
  "vitals": [
   {
    "name": "혈압",
    "value": "118/76 mmHg"
   },
   {
    "name": "맥박",
    "value": "88회/분"
   },
   {
    "name": "호흡",
    "value": "16회/분"
   },
   {
    "name": "체온",
    "value": "36.5 °C"
   }
  ],
  "labs": [
   {
    "name": "혈청 알부민",
    "value": "2.1 g/dL",
    "ref": "3.5–5.0"
   },
   {
    "name": "24시간 요단백",
    "value": "6.2 g/day",
    "ref": "< 0.15"
   },
   {
    "name": "혈청 크레아티닌",
    "value": "1.3 mg/dL",
    "ref": "0.7–1.3"
   },
   {
    "name": "혈청 유리경쇄비(κ/λ)",
    "value": "0.08",
    "ref": "0.26–1.65"
   },
   {
    "name": "공복혈당",
    "value": "94 mg/dL",
    "ref": "70–100"
   },
   {
    "name": "혈청 칼슘",
    "value": "9.4 mg/dL",
    "ref": "8.5–10.5"
   }
  ],
  "appendix": {
   "가이드라인": "아밀로이드 유형별 원인 단백질 감별\n───────────────────────────────────────────────\n임상 맥락 → 아밀로이드 유형(원인 단백질)\n  · 단클론감마글로불린증, 유리경쇄비 편향, 대설증/안와주위 자반 → AL(경쇄)\n  · 만성염증질환(류마티스관절염·만성감염) 병력 → AA(혈청아밀로이드A)\n  · 가족력, 말초신경병증/심근병증 → ATTR(유전변이 또는 야생형 트랜스티레틴)\n  · 장기 혈액투석(수년 이상) → Aβ2M(베타2-마이크로글로불린)\n  · 제2형 당뇨병, 췌도 침착 → islet amyloid polypeptide(아밀린)\n확진: Congo red 염색 + 편광현미경 사과-녹색 복굴절, 유형 확인은 면역조직화학/질량분석.\n",
   "최신지견": "질량분석 기반 아밀로이드 유형분류(laser microdissection-MS)가 면역조직화학보다 정확도가 높아 표준으로 자리잡고 있다.",
   "참고문헌": [
    "Robbins Basic Pathology — Amyloidosis",
    "UpToDate — Diagnosis of Immunoglobulin Light Chain Amyloidosis"
   ]
  },
  "figureSvg": ""
 },
 {
  "id": "usmle-2026-0052",
  "exam": "usmle",
  "step": "Step 2",
  "subject": "Internal Medicine",
  "subject_file": "Internal Medicine",
  "subtopic": "Unstable Wide-Complex Tachycardia — Synchronized Cardioversion",
  "type": "Unstable Wide-Complex Tachycardia — Synchronized Cardioversion",
  "difficulty": 4,
  "created": "2026-07-21",
  "vignette": "A 62-year-old man with a history of myocardial infarction 3 years ago presents with sudden palpitations and near-syncope. He is diaphoretic, pale, and mildly confused but has a palpable pulse. The rhythm strip is shown. Vital signs and laboratory studies are shown.",
  "question": "Which of the following is the most appropriate immediate management?",
  "options": [
   "Immediate unsynchronized defibrillation",
   "Intravenous amiodarone loading infusion over 10 minutes",
   "Immediate synchronized cardioversion",
   "Vagal maneuvers followed by adenosine if unsuccessful",
   "Intravenous metoprolol bolus"
  ],
  "answer": 3,
  "explanationText": "- 정답근거: 이전 심근경색 병력이 있는 환자에서 광QRS빈맥(QRS 152ms)과 함께 저혈압(78/50)·의식수준 저하(GCS 14)라는 불안정 징후가 동반되었으나 맥박은 촉지된다. ACLS 알고리즘상 맥박이 있으면서 불안정한 빈맥은 즉시 동기화 심율동전환이 표준 처치다.\n- 오답감별:\n  - (A) 비동기 제세동은 무맥성 리듬(심실세동/무맥성 심실빈맥)에 사용하며, 맥박이 있는 환자에게 시행하면 R-on-T로 심실세동을 유발할 위험이 있다.\n  - (B) 아미오다론 정맥 부하는 혈역학적으로 안정한 광QRS빈맥에 고려하는 처치이며, 불안정한 환자에서 우선순위가 아니다.\n  - (D) 미주신경수기·아데노신은 좁은QRS의 방실결절 의존성 빈맥(SVT)에 사용하는 처치로, 허혈성 심질환 병력이 있는 광QRS빈맥에는 적절하지 않고 지연으로 악화 위험이 있다.\n  - (E) 베타차단제 볼루스는 급성 불안정 빈맥의 즉시 처치가 아니며, 저혈압을 더 악화시킬 수 있다.\n- 임상핵심: 광QRS빈맥에서는 진단(원인) 확인보다 먼저 \"맥박 유무 → 안정성\"을 판단해 무맥이면 제세동, 맥박 있고 불안정하면 동기화 심율동전환을 즉시 시행한다.\n- 출처: AHA ACLS Guidelines; Braunwald's Heart Disease.",
  "explanationItems": [
   {
    "k": "정답근거",
    "v": "이전 심근경색 병력이 있는 환자에서 광QRS빈맥(QRS 152ms)과 함께 저혈압(78/50)·의식수준 저하(GCS 14)라는 불안정 징후가 동반되었으나 맥박은 촉지된다. ACLS 알고리즘상 맥박이 있으면서 불안정한 빈맥은 즉시 동기화 심율동전환이 표준 처치다."
   },
   {
    "k": "오답감별",
    "v": "(A) 비동기 제세동은 무맥성 리듬(심실세동/무맥성 심실빈맥)에 사용하며, 맥박이 있는 환자에게 시행하면 R-on-T로 심실세동을 유발할 위험이 있다.\n(B) 아미오다론 정맥 부하는 혈역학적으로 안정한 광QRS빈맥에 고려하는 처치이며, 불안정한 환자에서 우선순위가 아니다.\n(D) 미주신경수기·아데노신은 좁은QRS의 방실결절 의존성 빈맥(SVT)에 사용하는 처치로, 허혈성 심질환 병력이 있는 광QRS빈맥에는 적절하지 않고 지연으로 악화 위험이 있다.\n(E) 베타차단제 볼루스는 급성 불안정 빈맥의 즉시 처치가 아니며, 저혈압을 더 악화시킬 수 있다."
   },
   {
    "k": "임상핵심",
    "v": "광QRS빈맥에서는 진단(원인) 확인보다 먼저 \"맥박 유무 → 안정성\"을 판단해 무맥이면 제세동, 맥박 있고 불안정하면 동기화 심율동전환을 즉시 시행한다."
   },
   {
    "k": "출처",
    "v": "AHA ACLS Guidelines; Braunwald's Heart Disease."
   }
  ],
  "source": "USMLE-style / MedKOS (internal medicine · arrhythmia, synthetic ECG)",
  "vitals": [
   {
    "name": "혈압",
    "value": "78/50 mmHg"
   },
   {
    "name": "맥박",
    "value": "192회/분"
   },
   {
    "name": "호흡",
    "value": "24회/분"
   },
   {
    "name": "체온",
    "value": "36.9 °C"
   }
  ],
  "labs": [
   {
    "name": "트로포닌I",
    "value": "0.18 ng/mL",
    "ref": "< 0.04"
   },
   {
    "name": "혈청 칼륨",
    "value": "4.1 mEq/L",
    "ref": "3.5–5.0"
   },
   {
    "name": "혈청 마그네슘",
    "value": "2.0 mg/dL",
    "ref": "1.7–2.2"
   },
   {
    "name": "산소포화도",
    "value": "94%",
    "ref": "≥ 95%"
   },
   {
    "name": "심전도 QRS폭",
    "value": "152 ms",
    "ref": "< 120"
   },
   {
    "name": "의식수준(GCS)",
    "value": "14점",
    "ref": "15점"
   }
  ],
  "appendix": {
   "가이드라인": "광QRS빈맥 안정성에 따른 처치 (ACLS)\n───────────────────────────────────────────────\n맥박 유무 → 처치\n  · 무맥(pulseless) → 심폐소생술 + 비동기 제세동(defibrillation)\n  · 맥박 있음 + 불안정(저혈압·의식저하·흉통·쇼크) → 동기화 심율동전환\n  · 맥박 있음 + 안정 → 항부정맥제(아미오다론 등) 정맥 투여, 순환기 자문\n주의: 동기화 여부를 반드시 확인 — R파에 동기화하지 않으면 T파에 충격이 가해져\n심실세동을 유발할 수 있다(R-on-T 위험).\n",
   "최신지견": "저혈압·의식저하가 동반된 광QRS빈맥은 원인 감별보다 즉시 심율동전환이 우선이다.",
   "참고문헌": [
    "AHA ACLS Guidelines — Tachycardia with a Pulse Algorithm",
    "Braunwald's Heart Disease — Ventricular Arrhythmias"
   ]
  },
  "figureSvg": "<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 900 198\" width=\"900\" height=\"198\" role=\"img\" aria-label=\"ECG vtach · 188 bpm · 25 mm/s, 10 mm/mV\"><style>.bg{fill:#fff}.gmin{stroke:#f4c9c9;stroke-width:0.5}.gmaj{stroke:#e59a9a;stroke-width:1}.trace{fill:none;stroke:#111;stroke-width:1.6;stroke-linejoin:round;stroke-linecap:round}.cap{font:11px -apple-system,Segoe UI,sans-serif;fill:#555}</style><rect class=\"bg\" x=\"0\" y=\"0\" width=\"900\" height=\"180\"/><line x1=\"0\" y1=\"0\" x2=\"0\" y2=\"180\" class=\"gmaj\"/><line x1=\"6\" y1=\"0\" x2=\"6\" y2=\"180\" class=\"gmin\"/><line x1=\"12\" y1=\"0\" x2=\"12\" y2=\"180\" class=\"gmin\"/><line x1=\"18\" y1=\"0\" x2=\"18\" y2=\"180\" class=\"gmin\"/><line x1=\"24\" y1=\"0\" x2=\"24\" y2=\"180\" class=\"gmin\"/><line x1=\"30\" y1=\"0\" x2=\"30\" y2=\"180\" class=\"gmaj\"/><line x1=\"36\" y1=\"0\" x2=\"36\" y2=\"180\" class=\"gmin\"/><line x1=\"42\" y1=\"0\" x2=\"42\" y2=\"180\" class=\"gmin\"/><line x1=\"48\" y1=\"0\" x2=\"48\" y2=\"180\" class=\"gmin\"/><line x1=\"54\" y1=\"0\" x2=\"54\" y2=\"180\" class=\"gmin\"/><line x1=\"60\" y1=\"0\" x2=\"60\" y2=\"180\" class=\"gmaj\"/><line x1=\"66\" y1=\"0\" x2=\"66\" y2=\"180\" class=\"gmin\"/><line x1=\"72\" y1=\"0\" x2=\"72\" y2=\"180\" class=\"gmin\"/><line x1=\"78\" y1=\"0\" x2=\"78\" y2=\"180\" class=\"gmin\"/><line x1=\"84\" y1=\"0\" x2=\"84\" y2=\"180\" class=\"gmin\"/><line x1=\"90\" y1=\"0\" x2=\"90\" y2=\"180\" class=\"gmaj\"/><line x1=\"96\" y1=\"0\" x2=\"96\" y2=\"180\" class=\"gmin\"/><line x1=\"102\" y1=\"0\" x2=\"102\" y2=\"180\" class=\"gmin\"/><line x1=\"108\" y1=\"0\" x2=\"108\" y2=\"180\" class=\"gmin\"/><line x1=\"114\" y1=\"0\" x2=\"114\" y2=\"180\" class=\"gmin\"/><line x1=\"120\" y1=\"0\" x2=\"120\" y2=\"180\" class=\"gmaj\"/><line x1=\"126\" y1=\"0\" x2=\"126\" y2=\"180\" class=\"gmin\"/><line x1=\"132\" y1=\"0\" x2=\"132\" y2=\"180\" class=\"gmin\"/><line x1=\"138\" y1=\"0\" x2=\"138\" y2=\"180\" class=\"gmin\"/><line x1=\"144\" y1=\"0\" x2=\"144\" y2=\"180\" class=\"gmin\"/><line x1=\"150\" y1=\"0\" x2=\"150\" y2=\"180\" class=\"gmaj\"/><line x1=\"156\" y1=\"0\" x2=\"156\" y2=\"180\" class=\"gmin\"/><line x1=\"162\" y1=\"0\" x2=\"162\" y2=\"180\" class=\"gmin\"/><line x1=\"168\" y1=\"0\" x2=\"168\" y2=\"180\" class=\"gmin\"/><line x1=\"174\" y1=\"0\" x2=\"174\" y2=\"180\" class=\"gmin\"/><line x1=\"180\" y1=\"0\" x2=\"180\" y2=\"180\" class=\"gmaj\"/><line x1=\"186\" y1=\"0\" x2=\"186\" y2=\"180\" class=\"gmin\"/><line x1=\"192\" y1=\"0\" x2=\"192\" y2=\"180\" class=\"gmin\"/><line x1=\"198\" y1=\"0\" x2=\"198\" y2=\"180\" class=\"gmin\"/><line x1=\"204\" y1=\"0\" x2=\"204\" y2=\"180\" class=\"gmin\"/><line x1=\"210\" y1=\"0\" x2=\"210\" y2=\"180\" class=\"gmaj\"/><line x1=\"216\" y1=\"0\" x2=\"216\" y2=\"180\" class=\"gmin\"/><line x1=\"222\" y1=\"0\" x2=\"222\" y2=\"180\" class=\"gmin\"/><line x1=\"228\" y1=\"0\" x2=\"228\" y2=\"180\" class=\"gmin\"/><line x1=\"234\" y1=\"0\" x2=\"234\" y2=\"180\" class=\"gmin\"/><line x1=\"240\" y1=\"0\" x2=\"240\" y2=\"180\" class=\"gmaj\"/><line x1=\"246\" y1=\"0\" x2=\"246\" y2=\"180\" class=\"gmin\"/><line x1=\"252\" y1=\"0\" x2=\"252\" y2=\"180\" class=\"gmin\"/><line x1=\"258\" y1=\"0\" x2=\"258\" y2=\"180\" class=\"gmin\"/><line x1=\"264\" y1=\"0\" x2=\"264\" y2=\"180\" class=\"gmin\"/><line x1=\"270\" y1=\"0\" x2=\"270\" y2=\"180\" class=\"gmaj\"/><line x1=\"276\" y1=\"0\" x2=\"276\" y2=\"180\" class=\"gmin\"/><line x1=\"282\" y1=\"0\" x2=\"282\" y2=\"180\" class=\"gmin\"/><line x1=\"288\" y1=\"0\" x2=\"288\" y2=\"180\" class=\"gmin\"/><line x1=\"294\" y1=\"0\" x2=\"294\" y2=\"180\" class=\"gmin\"/><line x1=\"300\" y1=\"0\" x2=\"300\" y2=\"180\" class=\"gmaj\"/><line x1=\"306\" y1=\"0\" x2=\"306\" y2=\"180\" class=\"gmin\"/><line x1=\"312\" y1=\"0\" x2=\"312\" y2=\"180\" class=\"gmin\"/><line x1=\"318\" y1=\"0\" x2=\"318\" y2=\"180\" class=\"gmin\"/><line x1=\"324\" y1=\"0\" x2=\"324\" y2=\"180\" class=\"gmin\"/><line x1=\"330\" y1=\"0\" x2=\"330\" y2=\"180\" class=\"gmaj\"/><line x1=\"336\" y1=\"0\" x2=\"336\" y2=\"180\" class=\"gmin\"/><line x1=\"342\" y1=\"0\" x2=\"342\" y2=\"180\" class=\"gmin\"/><line x1=\"348\" y1=\"0\" x2=\"348\" y2=\"180\" class=\"gmin\"/><line x1=\"354\" y1=\"0\" x2=\"354\" y2=\"180\" class=\"gmin\"/><line x1=\"360\" y1=\"0\" x2=\"360\" y2=\"180\" class=\"gmaj\"/><line x1=\"366\" y1=\"0\" x2=\"366\" y2=\"180\" class=\"gmin\"/><line x1=\"372\" y1=\"0\" x2=\"372\" y2=\"180\" class=\"gmin\"/><line x1=\"378\" y1=\"0\" x2=\"378\" y2=\"180\" class=\"gmin\"/><line x1=\"384\" y1=\"0\" x2=\"384\" y2=\"180\" class=\"gmin\"/><line x1=\"390\" y1=\"0\" x2=\"390\" y2=\"180\" class=\"gmaj\"/><line x1=\"396\" y1=\"0\" x2=\"396\" y2=\"180\" class=\"gmin\"/><line x1=\"402\" y1=\"0\" x2=\"402\" y2=\"180\" class=\"gmin\"/><line x1=\"408\" y1=\"0\" x2=\"408\" y2=\"180\" class=\"gmin\"/><line x1=\"414\" y1=\"0\" x2=\"414\" y2=\"180\" class=\"gmin\"/><line x1=\"420\" y1=\"0\" x2=\"420\" y2=\"180\" class=\"gmaj\"/><line x1=\"426\" y1=\"0\" x2=\"426\" y2=\"180\" class=\"gmin\"/><line x1=\"432\" y1=\"0\" x2=\"432\" y2=\"180\" class=\"gmin\"/><line x1=\"438\" y1=\"0\" x2=\"438\" y2=\"180\" class=\"gmin\"/><line x1=\"444\" y1=\"0\" x2=\"444\" y2=\"180\" class=\"gmin\"/><line x1=\"450\" y1=\"0\" x2=\"450\" y2=\"180\" class=\"gmaj\"/><line x1=\"456\" y1=\"0\" x2=\"456\" y2=\"180\" class=\"gmin\"/><line x1=\"462\" y1=\"0\" x2=\"462\" y2=\"180\" class=\"gmin\"/><line x1=\"468\" y1=\"0\" x2=\"468\" y2=\"180\" class=\"gmin\"/><line x1=\"474\" y1=\"0\" x2=\"474\" y2=\"180\" class=\"gmin\"/><line x1=\"480\" y1=\"0\" x2=\"480\" y2=\"180\" class=\"gmaj\"/><line x1=\"486\" y1=\"0\" x2=\"486\" y2=\"180\" class=\"gmin\"/><line x1=\"492\" y1=\"0\" x2=\"492\" y2=\"180\" class=\"gmin\"/><line x1=\"498\" y1=\"0\" x2=\"498\" y2=\"180\" class=\"gmin\"/><line x1=\"504\" y1=\"0\" x2=\"504\" y2=\"180\" class=\"gmin\"/><line x1=\"510\" y1=\"0\" x2=\"510\" y2=\"180\" class=\"gmaj\"/><line x1=\"516\" y1=\"0\" x2=\"516\" y2=\"180\" class=\"gmin\"/><line x1=\"522\" y1=\"0\" x2=\"522\" y2=\"180\" class=\"gmin\"/><line x1=\"528\" y1=\"0\" x2=\"528\" y2=\"180\" class=\"gmin\"/><line x1=\"534\" y1=\"0\" x2=\"534\" y2=\"180\" class=\"gmin\"/><line x1=\"540\" y1=\"0\" x2=\"540\" y2=\"180\" class=\"gmaj\"/><line x1=\"546\" y1=\"0\" x2=\"546\" y2=\"180\" class=\"gmin\"/><line x1=\"552\" y1=\"0\" x2=\"552\" y2=\"180\" class=\"gmin\"/><line x1=\"558\" y1=\"0\" x2=\"558\" y2=\"180\" class=\"gmin\"/><line x1=\"564\" y1=\"0\" x2=\"564\" y2=\"180\" class=\"gmin\"/><line x1=\"570\" y1=\"0\" x2=\"570\" y2=\"180\" class=\"gmaj\"/><line x1=\"576\" y1=\"0\" x2=\"576\" y2=\"180\" class=\"gmin\"/><line x1=\"582\" y1=\"0\" x2=\"582\" y2=\"180\" class=\"gmin\"/><line x1=\"588\" y1=\"0\" x2=\"588\" y2=\"180\" class=\"gmin\"/><line x1=\"594\" y1=\"0\" x2=\"594\" y2=\"180\" class=\"gmin\"/><line x1=\"600\" y1=\"0\" x2=\"600\" y2=\"180\" class=\"gmaj\"/><line x1=\"606\" y1=\"0\" x2=\"606\" y2=\"180\" class=\"gmin\"/><line x1=\"612\" y1=\"0\" x2=\"612\" y2=\"180\" class=\"gmin\"/><line x1=\"618\" y1=\"0\" x2=\"618\" y2=\"180\" class=\"gmin\"/><line x1=\"624\" y1=\"0\" x2=\"624\" y2=\"180\" class=\"gmin\"/><line x1=\"630\" y1=\"0\" x2=\"630\" y2=\"180\" class=\"gmaj\"/><line x1=\"636\" y1=\"0\" x2=\"636\" y2=\"180\" class=\"gmin\"/><line x1=\"642\" y1=\"0\" x2=\"642\" y2=\"180\" class=\"gmin\"/><line x1=\"648\" y1=\"0\" x2=\"648\" y2=\"180\" class=\"gmin\"/><line x1=\"654\" y1=\"0\" x2=\"654\" y2=\"180\" class=\"gmin\"/><line x1=\"660\" y1=\"0\" x2=\"660\" y2=\"180\" class=\"gmaj\"/><line x1=\"666\" y1=\"0\" x2=\"666\" y2=\"180\" class=\"gmin\"/><line x1=\"672\" y1=\"0\" x2=\"672\" y2=\"180\" class=\"gmin\"/><line x1=\"678\" y1=\"0\" x2=\"678\" y2=\"180\" class=\"gmin\"/><line x1=\"684\" y1=\"0\" x2=\"684\" y2=\"180\" class=\"gmin\"/><line x1=\"690\" y1=\"0\" x2=\"690\" y2=\"180\" class=\"gmaj\"/><line x1=\"696\" y1=\"0\" x2=\"696\" y2=\"180\" class=\"gmin\"/><line x1=\"702\" y1=\"0\" x2=\"702\" y2=\"180\" class=\"gmin\"/><line x1=\"708\" y1=\"0\" x2=\"708\" y2=\"180\" class=\"gmin\"/><line x1=\"714\" y1=\"0\" x2=\"714\" y2=\"180\" class=\"gmin\"/><line x1=\"720\" y1=\"0\" x2=\"720\" y2=\"180\" class=\"gmaj\"/><line x1=\"726\" y1=\"0\" x2=\"726\" y2=\"180\" class=\"gmin\"/><line x1=\"732\" y1=\"0\" x2=\"732\" y2=\"180\" class=\"gmin\"/><line x1=\"738\" y1=\"0\" x2=\"738\" y2=\"180\" class=\"gmin\"/><line x1=\"744\" y1=\"0\" x2=\"744\" y2=\"180\" class=\"gmin\"/><line x1=\"750\" y1=\"0\" x2=\"750\" y2=\"180\" class=\"gmaj\"/><line x1=\"756\" y1=\"0\" x2=\"756\" y2=\"180\" class=\"gmin\"/><line x1=\"762\" y1=\"0\" x2=\"762\" y2=\"180\" class=\"gmin\"/><line x1=\"768\" y1=\"0\" x2=\"768\" y2=\"180\" class=\"gmin\"/><line x1=\"774\" y1=\"0\" x2=\"774\" y2=\"180\" class=\"gmin\"/><line x1=\"780\" y1=\"0\" x2=\"780\" y2=\"180\" class=\"gmaj\"/><line x1=\"786\" y1=\"0\" x2=\"786\" y2=\"180\" class=\"gmin\"/><line x1=\"792\" y1=\"0\" x2=\"792\" y2=\"180\" class=\"gmin\"/><line x1=\"798\" y1=\"0\" x2=\"798\" y2=\"180\" class=\"gmin\"/><line x1=\"804\" y1=\"0\" x2=\"804\" y2=\"180\" class=\"gmin\"/><line x1=\"810\" y1=\"0\" x2=\"810\" y2=\"180\" class=\"gmaj\"/><line x1=\"816\" y1=\"0\" x2=\"816\" y2=\"180\" class=\"gmin\"/><line x1=\"822\" y1=\"0\" x2=\"822\" y2=\"180\" class=\"gmin\"/><line x1=\"828\" y1=\"0\" x2=\"828\" y2=\"180\" class=\"gmin\"/><line x1=\"834\" y1=\"0\" x2=\"834\" y2=\"180\" class=\"gmin\"/><line x1=\"840\" y1=\"0\" x2=\"840\" y2=\"180\" class=\"gmaj\"/><line x1=\"846\" y1=\"0\" x2=\"846\" y2=\"180\" class=\"gmin\"/><line x1=\"852\" y1=\"0\" x2=\"852\" y2=\"180\" class=\"gmin\"/><line x1=\"858\" y1=\"0\" x2=\"858\" y2=\"180\" class=\"gmin\"/><line x1=\"864\" y1=\"0\" x2=\"864\" y2=\"180\" class=\"gmin\"/><line x1=\"870\" y1=\"0\" x2=\"870\" y2=\"180\" class=\"gmaj\"/><line x1=\"876\" y1=\"0\" x2=\"876\" y2=\"180\" class=\"gmin\"/><line x1=\"882\" y1=\"0\" x2=\"882\" y2=\"180\" class=\"gmin\"/><line x1=\"888\" y1=\"0\" x2=\"888\" y2=\"180\" class=\"gmin\"/><line x1=\"894\" y1=\"0\" x2=\"894\" y2=\"180\" class=\"gmin\"/><line x1=\"900\" y1=\"0\" x2=\"900\" y2=\"180\" class=\"gmaj\"/><line x1=\"0\" y1=\"0\" x2=\"900\" y2=\"0\" class=\"gmaj\"/><line x1=\"0\" y1=\"6\" x2=\"900\" y2=\"6\" class=\"gmin\"/><line x1=\"0\" y1=\"12\" x2=\"900\" y2=\"12\" class=\"gmin\"/><line x1=\"0\" y1=\"18\" x2=\"900\" y2=\"18\" class=\"gmin\"/><line x1=\"0\" y1=\"24\" x2=\"900\" y2=\"24\" class=\"gmin\"/><line x1=\"0\" y1=\"30\" x2=\"900\" y2=\"30\" class=\"gmaj\"/><line x1=\"0\" y1=\"36\" x2=\"900\" y2=\"36\" class=\"gmin\"/><line x1=\"0\" y1=\"42\" x2=\"900\" y2=\"42\" class=\"gmin\"/><line x1=\"0\" y1=\"48\" x2=\"900\" y2=\"48\" class=\"gmin\"/><line x1=\"0\" y1=\"54\" x2=\"900\" y2=\"54\" class=\"gmin\"/><line x1=\"0\" y1=\"60\" x2=\"900\" y2=\"60\" class=\"gmaj\"/><line x1=\"0\" y1=\"66\" x2=\"900\" y2=\"66\" class=\"gmin\"/><line x1=\"0\" y1=\"72\" x2=\"900\" y2=\"72\" class=\"gmin\"/><line x1=\"0\" y1=\"78\" x2=\"900\" y2=\"78\" class=\"gmin\"/><line x1=\"0\" y1=\"84\" x2=\"900\" y2=\"84\" class=\"gmin\"/><line x1=\"0\" y1=\"90\" x2=\"900\" y2=\"90\" class=\"gmaj\"/><line x1=\"0\" y1=\"96\" x2=\"900\" y2=\"96\" class=\"gmin\"/><line x1=\"0\" y1=\"102\" x2=\"900\" y2=\"102\" class=\"gmin\"/><line x1=\"0\" y1=\"108\" x2=\"900\" y2=\"108\" class=\"gmin\"/><line x1=\"0\" y1=\"114\" x2=\"900\" y2=\"114\" class=\"gmin\"/><line x1=\"0\" y1=\"120\" x2=\"900\" y2=\"120\" class=\"gmaj\"/><line x1=\"0\" y1=\"126\" x2=\"900\" y2=\"126\" class=\"gmin\"/><line x1=\"0\" y1=\"132\" x2=\"900\" y2=\"132\" class=\"gmin\"/><line x1=\"0\" y1=\"138\" x2=\"900\" y2=\"138\" class=\"gmin\"/><line x1=\"0\" y1=\"144\" x2=\"900\" y2=\"144\" class=\"gmin\"/><line x1=\"0\" y1=\"150\" x2=\"900\" y2=\"150\" class=\"gmaj\"/><line x1=\"0\" y1=\"156\" x2=\"900\" y2=\"156\" class=\"gmin\"/><line x1=\"0\" y1=\"162\" x2=\"900\" y2=\"162\" class=\"gmin\"/><line x1=\"0\" y1=\"168\" x2=\"900\" y2=\"168\" class=\"gmin\"/><line x1=\"0\" y1=\"174\" x2=\"900\" y2=\"174\" class=\"gmin\"/><line x1=\"0\" y1=\"180\" x2=\"900\" y2=\"180\" class=\"gmaj\"/><polyline class=\"trace\" points=\"0.0,90.0 0.6,90.0 1.2,90.0 1.8,90.0 2.4,90.0 3.0,90.0 3.6,90.0 4.2,90.0 4.8,90.0 5.4,90.0 6.0,90.0 6.6,90.0 7.2,90.0 7.8,90.0 8.4,90.0 9.0,90.0 9.6,90.0 10.2,90.0 10.8,90.0 11.4,90.0 12.0,90.0 12.6,90.0 13.2,90.0 13.8,90.0 14.4,90.0 15.0,90.0 15.6,90.0 16.2,90.0 16.8,90.0 17.4,90.0 18.0,90.0 18.6,90.0 19.2,90.0 19.8,90.0 20.4,90.0 21.0,90.0 21.6,90.0 22.2,90.0 22.8,89.9 23.4,89.9 24.0,89.9 24.6,89.8 25.2,89.7 25.8,89.6 26.4,89.5 27.0,89.3 27.6,89.1 28.2,88.8 28.8,88.4 29.4,88.0 30.0,87.4 30.6,86.6 31.2,85.7 31.8,84.7 32.4,83.4 33.0,81.9 33.6,80.1 34.2,78.1 34.8,75.9 35.4,73.3 36.0,70.5 36.6,67.5 37.2,64.2 37.8,60.8 38.4,57.3 39.0,53.6 39.6,50.0 40.2,46.5 40.8,43.1 41.4,39.9 42.0,37.1 42.6,34.7 43.2,32.8 43.8,31.3 44.4,30.5 45.0,30.2 45.6,30.5 46.2,31.5 46.8,33.0 47.4,35.0 48.0,37.5 48.6,40.4 49.2,43.7 49.8,47.2 50.4,50.8 51.0,54.6 51.6,58.4 52.2,62.1 52.8,65.7 53.4,69.2 54.0,72.5 54.6,75.6 55.2,78.4 55.8,81.0 56.4,83.4 57.0,85.5 57.6,87.5 58.2,89.2 58.8,90.8 59.4,92.3 60.0,93.6 60.6,94.8 61.2,95.9 61.8,97.0 62.4,98.1 63.0,99.1 63.6,100.1 64.2,101.0 64.8,102.0 65.4,103.0 66.0,103.9 66.6,104.9 67.2,105.8 67.8,106.8 68.4,107.7 69.0,108.7 69.6,109.6 70.2,110.4 70.8,111.3 71.4,112.1 72.0,112.8 72.6,113.5 73.2,114.0 73.8,114.5 74.4,114.9 75.0,115.2 75.6,115.4 76.2,115.3 76.8,115.2 77.4,114.8 78.0,114.2 78.6,113.4 79.2,112.4 79.8,111.0 80.4,109.4 81.0,107.5 81.6,105.2 82.2,102.6 82.8,99.7 83.4,96.4 84.0,92.8 84.6,89.0 85.2,84.9 85.8,80.6 86.4,76.1 87.0,71.6 87.6,67.0 88.2,62.6 88.8,58.3 89.4,54.3 90.0,50.6 90.6,47.4 91.2,44.7 91.8,42.5 92.4,40.9 93.0,39.9 93.6,39.6 94.2,39.9 94.8,40.9 95.4,42.3 96.0,44.3 96.6,46.7 97.2,49.5 97.8,52.5 98.4,55.7 99.0,59.1 99.6,62.4 100.2,65.8 100.8,69.1 101.4,72.2 102.0,75.2 102.6,77.9 103.2,80.5 103.8,82.9 104.4,85.0 105.0,87.0 105.6,88.7 106.2,90.3 106.8,91.8 107.4,93.1 108.0,94.3 108.6,95.4 109.2,96.5 109.8,97.5 110.4,98.5 111.0,99.5 111.6,100.4 112.2,101.4 112.8,102.2 113.4,103.2 114.0,104.1 114.6,105.1 115.2,106.0 115.8,107.0 116.4,107.9 117.0,108.9 117.6,109.7 118.2,110.6 118.8,111.4 119.4,112.2 120.0,112.9 120.6,113.6 121.2,114.2 121.8,114.6 122.4,115.0 123.0,115.3 123.6,115.4 124.2,115.3 124.8,115.1 125.4,114.7 126.0,114.1 126.6,113.2 127.2,112.1 127.8,110.7 128.4,109.0 129.0,107.0 129.6,104.7 130.2,102.0 130.8,99.0 131.4,95.7 132.0,92.0 132.6,88.1 133.2,84.0 133.8,79.6 134.4,75.1 135.0,70.6 135.6,66.1 136.2,61.7 136.8,57.4 137.4,53.5 138.0,49.9 138.6,46.8 139.2,44.1 139.8,42.1 140.4,40.6 141.0,39.8 141.6,39.6 142.2,40.1 142.8,41.1 143.4,42.7 144.0,44.8 144.6,47.3 145.2,50.1 145.8,53.2 146.4,56.4 147.0,59.8 147.6,63.2 148.2,66.5 148.8,69.7 149.4,72.8 150.0,75.8 150.6,78.5 151.2,81.0 151.8,83.3 152.4,85.4 153.0,87.3 153.6,89.1 154.2,90.6 154.8,92.0 155.4,93.3 156.0,94.5 156.6,95.7 157.2,96.7 157.8,97.7 158.4,98.7 159.0,99.7 159.6,100.6 160.2,101.6 160.8,102.4 161.4,103.4 162.0,104.3 162.6,105.3 163.2,106.2 163.8,107.2 164.4,108.1 165.0,109.0 165.6,109.9 166.2,110.8 166.8,111.6 167.4,112.4 168.0,113.1 168.6,113.7 169.2,114.3 169.8,114.7 170.4,115.1 171.0,115.3 171.6,115.4 172.2,115.3 172.8,115.0 173.4,114.6 174.0,113.9 174.6,113.0 175.2,111.8 175.8,110.4 176.4,108.6 177.0,106.5 177.6,104.1 178.2,101.4 178.8,98.3 179.4,94.9 180.0,91.2 180.6,87.3 181.2,83.1 181.8,78.7 182.4,74.2 183.0,69.6 183.6,65.1 184.2,60.7 184.8,56.6 185.4,52.7 186.0,49.2 186.6,46.2 187.2,43.7 187.8,41.7 188.4,40.4 189.0,39.7 189.6,39.7 190.2,40.3 190.8,41.4 191.4,43.1 192.0,45.3 192.6,47.8 193.2,50.7 193.8,53.8 194.4,57.1 195.0,60.5 195.6,63.9 196.2,67.2 196.8,70.4 197.4,73.5 198.0,76.4 198.6,79.0 199.2,81.5 199.8,83.8 200.4,85.9 201.0,87.7 201.6,89.4 202.2,90.9 202.8,92.3 203.4,93.6 204.0,94.8 204.6,95.9 205.2,96.9 205.8,97.9 206.4,98.9 207.0,99.9 207.6,100.8 208.2,101.8 208.8,102.6 209.4,103.6 210.0,104.5 210.6,105.5 211.2,106.4 211.8,107.4 212.4,108.3 213.0,109.2 213.6,110.1 214.2,111.0 214.8,111.8 215.4,112.5 216.0,113.2 216.6,113.8 217.2,114.4 217.8,114.8 218.4,115.1 219.0,115.3 219.6,115.4 220.2,115.3 220.8,115.0 221.4,114.5 222.0,113.7 222.6,112.8 223.2,111.5 223.8,110.0 224.4,108.2 225.0,106.0 225.6,103.6 226.2,100.8 226.8,97.6 227.4,94.2 228.0,90.4 228.6,86.4 229.2,82.1 229.8,77.7 230.4,73.2 231.0,68.7 231.6,64.2 232.2,59.8 232.8,55.7 233.4,51.9 234.0,48.5 234.6,45.6 235.2,43.2 235.8,41.4 236.4,40.2 237.0,39.7 237.6,39.8 238.2,40.5 238.8,41.7 239.4,43.5 240.0,45.8 240.6,48.4 241.2,51.4 241.8,54.5 242.4,57.8 243.0,61.2 243.6,64.6 244.2,67.9 244.8,71.1 245.4,74.1 246.0,76.9 246.6,79.6 247.2,82.0 247.8,84.3 248.4,86.3 249.0,88.1 249.6,89.8 250.2,91.3 250.8,92.6 251.4,93.9 252.0,95.0 252.6,96.1 253.2,97.2 253.8,98.2 254.4,99.1 255.0,100.1 255.6,101.0 256.2,101.8 256.8,102.8 257.4,103.8 258.0,104.7 258.6,105.7 259.2,106.6 259.8,107.6 260.4,108.5 261.0,109.4 261.6,110.3 262.2,111.1 262.8,111.9 263.4,112.7 264.0,113.4 264.6,114.0 265.2,114.5 265.8,114.9 266.4,115.2 267.0,115.3 267.6,115.4 268.2,115.2 268.8,114.9 269.4,114.3 270.0,113.5 270.6,112.5 271.2,111.2 271.8,109.7 272.4,107.8 273.0,105.5 273.6,103.0 274.2,100.1 274.8,96.9 275.4,93.4 276.0,89.6 276.6,85.5 277.2,81.2 277.8,76.8 278.4,72.2 279.0,67.7 279.6,63.2 280.2,58.9 280.8,54.9 281.4,51.1 282.0,47.8 282.6,45.0 283.2,42.8 283.8,41.1 284.4,40.0 285.0,39.6 285.6,39.9 286.2,40.7 286.8,42.1 287.4,44.0 288.0,46.3 288.6,49.0 289.2,52.0 289.8,55.2 290.4,58.6 291.0,61.9 291.6,65.3 292.2,68.6 292.8,71.7 293.4,74.7 294.0,77.5 294.6,80.1 295.2,82.5 295.8,84.7 296.4,86.7 297.0,88.5 297.6,90.1 298.2,91.6 298.8,92.9 299.4,94.1 300.0,95.3 300.6,96.3 301.2,97.4 301.8,98.4 302.4,99.3 303.0,100.3 303.6,101.2 304.2,102.1 304.8,103.0 305.4,104.0 306.0,104.9 306.6,105.9 307.2,106.9 307.8,107.8 308.4,108.7 309.0,109.6 309.6,110.5 310.2,111.3 310.8,112.1 311.4,112.8 312.0,113.5 312.6,114.1 313.2,114.6 313.8,115.0 314.4,115.2 315.0,115.4 315.6,115.3 316.2,115.1 316.8,114.8 317.4,114.2 318.0,113.4 318.6,112.3 319.2,110.9 319.8,109.3 320.4,107.3 321.0,105.0 321.6,102.4 322.2,99.5 322.8,96.2 323.4,92.6 324.0,88.7 324.6,84.6 325.2,80.3 325.8,75.8 326.4,71.3 327.0,66.7 327.6,62.3 328.2,58.0 328.8,54.0 329.4,50.4 330.0,47.2 330.6,44.5 331.2,42.4 331.8,40.8 332.4,39.9 333.0,39.6 333.6,40.0 334.2,40.9 334.8,42.4 335.4,44.4 336.0,46.9 336.6,49.7 337.2,52.7 337.8,55.9 338.4,59.3 339.0,62.7 339.6,66.0 340.2,69.3 340.8,72.4 341.4,75.3 342.0,78.1 342.6,80.7 343.2,83.0 343.8,85.1 344.4,87.1 345.0,88.8 345.6,90.4 346.2,91.8 346.8,93.2 347.4,94.4 348.0,95.5 348.6,96.6 349.2,97.6 349.8,98.6 350.4,99.5 351.0,100.5 351.6,101.4 352.2,102.3 352.8,103.2 353.4,104.2 354.0,105.1 354.6,106.1 355.2,107.1 355.8,108.0 356.4,108.9 357.0,109.8 357.6,110.7 358.2,111.5 358.8,112.3 359.4,113.0 360.0,113.6 360.6,114.2 361.2,114.7 361.8,115.0 362.4,115.3 363.0,115.4 363.6,115.3 364.2,115.1 364.8,114.7 365.4,114.0 366.0,113.1 366.6,112.0 367.2,110.6 367.8,108.9 368.4,106.9 369.0,104.5 369.6,101.8 370.2,98.8 370.8,95.4 371.4,91.8 372.0,87.9 372.6,83.7 373.2,79.3 373.8,74.8 374.4,70.3 375.0,65.8 375.6,61.4 376.2,57.2 376.8,53.2 377.4,49.7 378.0,46.6 378.6,44.0 379.2,42.0 379.8,40.6 380.4,39.8 381.0,39.7 381.6,40.1 382.2,41.2 382.8,42.8 383.4,44.9 384.0,47.4 384.6,50.3 385.2,53.4 385.8,56.6 386.4,60.0 387.0,63.4 387.6,66.7 388.2,69.9 388.8,73.0 389.4,75.9 390.0,78.7 390.6,81.2 391.2,83.5 391.8,85.6 392.4,87.5 393.0,89.2 393.6,90.7 394.2,92.1 394.8,93.4 395.4,94.6 396.0,95.7 396.6,96.8 397.2,97.8 397.8,98.8 398.4,99.7 399.0,100.7 399.6,101.6 400.2,102.5 400.8,103.4 401.4,104.4 402.0,105.3 402.6,106.3 403.2,107.3 403.8,108.2 404.4,109.1 405.0,110.0 405.6,110.8 406.2,111.7 406.8,112.4 407.4,113.1 408.0,113.8 408.6,114.3 409.2,114.7 409.8,115.1 410.4,115.3 411.0,115.4 411.6,115.3 412.2,115.0 412.8,114.5 413.4,113.9 414.0,112.9 414.6,111.7 415.2,110.3 415.8,108.5 416.4,106.4 417.0,104.0 417.6,101.2 418.2,98.1 418.8,94.7 419.4,91.0 420.0,87.0 420.6,82.8 421.2,78.4 421.8,73.9 422.4,69.3 423.0,64.8 423.6,60.5 424.2,56.3 424.8,52.4 425.4,49.0 426.0,46.0 426.6,43.5 427.2,41.6 427.8,40.4 428.4,39.7 429.0,39.7 429.6,40.3 430.2,41.5 430.8,43.2 431.4,45.4 432.0,48.0 432.6,50.9 433.2,54.1 433.8,57.3 434.4,60.7 435.0,64.1 435.6,67.4 436.2,70.6 436.8,73.7 437.4,76.5 438.0,79.2 438.6,81.7 439.2,83.9 439.8,86.0 440.4,87.8 441.0,89.5 441.6,91.0 442.2,92.4 442.8,93.7 443.4,94.9 444.0,96.0 444.6,97.0 445.2,98.0 445.8,99.0 446.4,99.9 447.0,100.9 447.6,101.8 448.2,102.7 448.8,103.6 449.4,104.6 450.0,105.6 450.6,106.5 451.2,107.5 451.8,108.4 452.4,109.3 453.0,110.2 453.6,111.0 454.2,111.8 454.8,112.6 455.4,113.3 456.0,113.9 456.6,114.4 457.2,114.8 457.8,115.1 458.4,115.3 459.0,115.4 459.6,115.2 460.2,114.9 460.8,114.4 461.4,113.7 462.0,112.7 462.6,111.4 463.2,109.9 463.8,108.1 464.4,105.9 465.0,103.4 465.6,100.6 466.2,97.4 466.8,93.9 467.4,90.2 468.0,86.1 468.6,81.9 469.2,77.4 469.8,72.9 470.4,68.4 471.0,63.9 471.6,59.6 472.2,55.5 472.8,51.7 473.4,48.3 474.0,45.4 474.6,43.1 475.2,41.3 475.8,40.2 476.4,39.7 477.0,39.8 477.6,40.5 478.2,41.8 478.8,43.7 479.4,46.0 480.0,48.6 480.6,51.6 481.2,54.7 481.8,58.1 482.4,61.4 483.0,64.8 483.6,68.1 484.2,71.3 484.8,74.3 485.4,77.1 486.0,79.8 486.6,82.2 487.2,84.4 487.8,86.4 488.4,88.2 489.0,89.9 489.6,91.3 490.2,92.7 490.8,93.9 491.4,95.1 492.0,96.2 492.6,97.2 493.2,98.2 493.8,99.2 494.4,100.1 495.0,101.1 495.6,101.9 496.2,102.9 496.8,103.8 497.4,104.8 498.0,105.8 498.6,106.7 499.2,107.7 499.8,108.6 500.4,109.5 501.0,110.4 501.6,111.2 502.2,112.0 502.8,112.7 503.4,113.4 504.0,114.0 504.6,114.5 505.2,114.9 505.8,115.2 506.4,115.3 507.0,115.4 507.6,115.2 508.2,114.8 508.8,114.3 509.4,113.5 510.0,112.5 510.6,111.1 511.2,109.5 511.8,107.6 512.4,105.4 513.0,102.8 513.6,99.9 514.2,96.7 514.8,93.2 515.4,89.3 516.0,85.2 516.6,80.9 517.2,76.5 517.8,71.9 518.4,67.4 519.0,63.0 519.6,58.7 520.2,54.6 520.8,50.9 521.4,47.6 522.0,44.9 522.6,42.6 523.2,41.0 523.8,40.0 524.4,39.6 525.0,39.9 525.6,40.8 526.2,42.2 526.8,44.1 527.4,46.5 528.0,49.2 528.6,52.2 529.2,55.4 529.8,58.8 530.4,62.1 531.0,65.5 531.6,68.8 532.2,71.9 532.8,74.9 533.4,77.7 534.0,80.3 534.6,82.7 535.2,84.8 535.8,86.8 536.4,88.6 537.0,90.2 537.6,91.6 538.2,93.0 538.8,94.2 539.4,95.3 540.0,96.4 540.6,97.4 541.2,98.4 541.8,99.4 542.4,100.3 543.0,101.3 543.6,102.1 544.2,103.1 544.8,104.0 545.4,105.0 546.0,106.0 546.6,106.9 547.2,107.9 547.8,108.8 548.4,109.7 549.0,110.5 549.6,111.4 550.2,112.2 550.8,112.9 551.4,113.5 552.0,114.1 552.6,114.6 553.2,115.0 553.8,115.2 554.4,115.4 555.0,115.3 555.6,115.1 556.2,114.7 556.8,114.1 557.4,113.3 558.0,112.2 558.6,110.8 559.2,109.2 559.8,107.2 560.4,104.9 561.0,102.2 561.6,99.3 562.2,96.0 562.8,92.4 563.4,88.5 564.0,84.3 564.6,80.0 565.2,75.5 565.8,71.0 566.4,66.5 567.0,62.0 567.6,57.8 568.2,53.8 568.8,50.2 569.4,47.0 570.0,44.3 570.6,42.2 571.2,40.7 571.8,39.9 572.4,39.6 573.0,40.0 573.6,41.0 574.2,42.6 574.8,44.6 575.4,47.0 576.0,49.8 576.6,52.9 577.2,56.1 577.8,59.5 578.4,62.9 579.0,66.2 579.6,69.5 580.2,72.6 580.8,75.5 581.4,78.3 582.0,80.8 582.6,83.1 583.2,85.3 583.8,87.2 584.4,88.9 585.0,90.5 585.6,91.9 586.2,93.2 586.8,94.4 587.4,95.6 588.0,96.6 588.6,97.6 589.2,98.6 589.8,99.6 590.4,100.5 591.0,101.5 591.6,102.3 592.2,103.3 592.8,104.2 593.4,105.2 594.0,106.2 594.6,107.1 595.2,108.0 595.8,109.0 596.4,109.9 597.0,110.7 597.6,111.5 598.2,112.3 598.8,113.0 599.4,113.7 600.0,114.2 600.6,114.7 601.2,115.0 601.8,115.3 602.4,115.4 603.0,115.3 603.6,115.1 604.2,114.6 604.8,114.0 605.4,113.1 606.0,111.9 606.6,110.5 607.2,108.8 607.8,106.7 608.4,104.3 609.0,101.6 609.6,98.6 610.2,95.2 610.8,91.6 611.4,87.6 612.0,83.4 612.6,79.0 613.2,74.6 613.8,70.0 614.4,65.5 615.0,61.1 615.6,56.9 616.2,53.0 616.8,49.5 617.4,46.4 618.0,43.8 618.6,41.9 619.2,40.5 619.8,39.8 620.4,39.7 621.0,40.2 621.6,41.3 622.2,43.0 622.8,45.1 623.4,47.6 624.0,50.5 624.6,53.6 625.2,56.8 625.8,60.2 626.4,63.6 627.0,66.9 627.6,70.1 628.2,73.2 628.8,76.1 629.4,78.8 630.0,81.3 630.6,83.6 631.2,85.7 631.8,87.6 632.4,89.3 633.0,90.8 633.6,92.2 634.2,93.5 634.8,94.7 635.4,95.8 636.0,96.9 636.6,97.9 637.2,98.8 637.8,99.8 638.4,100.7 639.0,101.7 639.6,102.5 640.2,103.5 640.8,104.5 641.4,105.4 642.0,106.4 642.6,107.3 643.2,108.2 643.8,109.2 644.4,110.0 645.0,110.9 645.6,111.7 646.2,112.5 646.8,113.2 647.4,113.8 648.0,114.3 648.6,114.8 649.2,115.1 649.8,115.3 650.4,115.4 651.0,115.3 651.6,115.0 652.2,114.5 652.8,113.8 653.4,112.9 654.0,111.6 654.6,110.2 655.2,108.4 655.8,106.2 656.4,103.8 657.0,101.0 657.6,97.9 658.2,94.5 658.8,90.7 659.4,86.7 660.0,82.5 660.6,78.1 661.2,73.6 661.8,69.0 662.4,64.6 663.0,60.2 663.6,56.0 664.2,52.2 664.8,48.8 665.4,45.8 666.0,43.4 666.6,41.5 667.2,40.3 667.8,39.7 668.4,39.7 669.0,40.4 669.6,41.6 670.2,43.4 670.8,45.6 671.4,48.2 672.0,51.1 672.6,54.3 673.2,57.6 673.8,60.9 674.4,64.3 675.0,67.6 675.6,70.8 676.2,73.9 676.8,76.7 677.4,79.4 678.0,81.8 678.6,84.1 679.2,86.1 679.8,88.0 680.4,89.6 681.0,91.1 681.6,92.5 682.2,93.8 682.8,94.9 683.4,96.0 684.0,97.1 684.6,98.1 685.2,99.0 685.8,100.0 686.4,100.9 687.0,101.8 687.6,102.7 688.2,103.7 688.8,104.7 689.4,105.6 690.0,106.6 690.6,107.5 691.2,108.4 691.8,109.4 692.4,110.2 693.0,111.1 693.6,111.9 694.2,112.6 694.8,113.3 695.4,113.9 696.0,114.4 696.6,114.9 697.2,115.2 697.8,115.3 698.4,115.4 699.0,115.2 699.6,114.9 700.2,114.4 700.8,113.6 701.4,112.6 702.0,111.4 702.6,109.8 703.2,107.9 703.8,105.7 704.4,103.2 705.0,100.4 705.6,97.2 706.2,93.7 706.8,89.9 707.4,85.8 708.0,81.6 708.6,77.1 709.2,72.6 709.8,68.1 710.4,63.6 711.0,59.3 711.6,55.2 712.2,51.4 712.8,48.1 713.4,45.2 714.0,42.9 714.6,41.2 715.2,40.1 715.8,39.7 716.4,39.8 717.0,40.6 717.6,41.9 718.2,43.8 718.8,46.1 719.4,48.8 720.0,51.8 720.6,55.0 721.2,58.3 721.8,61.6 722.4,65.0 723.0,68.3 723.6,71.5 724.2,74.5 724.8,77.3 725.4,79.9 726.0,82.3 726.6,84.5 727.2,86.5 727.8,88.3 728.4,90.0 729.0,91.4 729.6,92.8 730.2,94.0 730.8,95.2 731.4,96.3 732.0,97.3 732.6,98.3 733.2,99.2 733.8,100.2 734.4,101.1 735.0,102.0 735.6,102.9 736.2,103.9 736.8,104.9 737.4,105.8 738.0,106.8 738.6,107.7 739.2,108.6 739.8,109.5 740.4,110.4 741.0,111.3 741.6,112.0 742.2,112.8 742.8,113.4 743.4,114.0 744.0,114.5 744.6,114.9 745.2,115.2 745.8,115.4 746.4,115.3 747.0,115.2 747.6,114.8 748.2,114.2 748.8,113.4 749.4,112.4 750.0,111.0 750.6,109.4 751.2,107.5 751.8,105.2 752.4,102.7 753.0,99.7 753.6,96.5 754.2,92.9 754.8,89.1 755.4,85.0 756.0,80.6 756.6,76.2 757.2,71.7 757.8,67.1 758.4,62.7 759.0,58.4 759.6,54.4 760.2,50.7 760.8,47.5 761.4,44.7 762.0,42.5 762.6,40.9 763.2,40.0 763.8,39.6 764.4,39.9 765.0,40.8 765.6,42.3 766.2,44.3 766.8,46.7 767.4,49.4 768.0,52.4 768.6,55.6 769.2,59.0 769.8,62.4 770.4,65.7 771.0,69.0 771.6,72.1 772.2,75.1 772.8,77.9 773.4,80.4 774.0,82.8 774.6,85.0 775.2,86.9 775.8,88.7 776.4,90.3 777.0,91.7 777.6,93.1 778.2,94.3 778.8,95.4 779.4,96.5 780.0,97.5 780.6,98.5 781.2,99.4 781.8,100.4 782.4,101.3 783.0,102.2 783.6,103.1 784.2,104.1 784.8,105.1 785.4,106.0 786.0,107.0 786.6,107.9 787.2,108.8 787.8,109.7 788.4,110.6 789.0,111.4 789.6,112.2 790.2,112.9 790.8,113.6 791.4,114.1 792.0,114.6 792.6,115.0 793.2,115.2 793.8,115.4 794.4,115.3 795.0,115.1 795.6,114.7 796.2,114.1 796.8,113.2 797.4,112.1 798.0,110.7 798.6,109.0 799.2,107.0 799.8,104.7 800.4,102.1 801.0,99.1 801.6,95.7 802.2,92.1 802.8,88.2 803.4,84.1 804.0,79.7 804.6,75.2 805.2,70.7 805.8,66.2 806.4,61.7 807.0,57.5 807.6,53.6 808.2,50.0 808.8,46.8 809.4,44.2 810.0,42.1 810.6,40.7 811.2,39.8 811.8,39.6 812.4,40.1 813.0,41.1 813.6,42.7 814.2,44.7 814.8,47.2 815.4,50.0 816.0,53.1 816.6,56.4 817.2,59.7 817.8,63.1 818.4,66.4 819.0,69.7 819.6,72.8 820.2,75.7 820.8,78.4 821.4,81.0 822.0,83.3 822.6,85.4 823.2,87.3 823.8,89.0 824.4,90.6 825.0,92.0 825.6,93.3 826.2,94.5 826.8,95.6 827.4,96.7 828.0,97.7 828.6,98.7 829.2,99.7 829.8,100.6 830.4,101.5 831.0,102.4 831.6,103.3 832.2,104.3 832.8,105.3 833.4,106.2 834.0,107.2 834.6,108.1 835.2,109.0 835.8,109.9 836.4,110.8 837.0,111.6 837.6,112.4 838.2,113.1 838.8,113.7 839.4,114.3 840.0,114.7 840.6,115.1 841.2,115.3 841.8,115.4 842.4,115.3 843.0,115.0 843.6,114.6 844.2,113.9 844.8,113.0 845.4,111.8 846.0,110.4 846.6,108.6 847.2,106.6 847.8,104.2 848.4,101.5 849.0,98.4 849.6,95.0 850.2,91.3 850.8,87.3 851.4,83.1 852.0,78.8 852.6,74.3 853.2,69.7 853.8,65.2 854.4,60.8 855.0,56.6 855.6,52.8 856.2,49.3 856.8,46.2 857.4,43.7 858.0,41.8 858.6,40.4 859.2,39.7 859.8,39.7 860.4,40.2 861.0,41.4 861.6,43.1 862.2,45.2 862.8,47.8 863.4,50.7 864.0,53.8 864.6,57.1 865.2,60.4 865.8,63.8 866.4,67.1 867.0,70.3 867.6,73.4 868.2,76.3 868.8,79.0 869.4,81.5 870.0,83.8 870.6,85.8 871.2,87.7 871.8,89.4 872.4,90.9 873.0,92.3 873.6,93.6 874.2,94.8 874.8,95.9 875.4,96.9 876.0,97.9 876.6,98.9 877.2,99.9 877.8,100.8 878.4,101.7 879.0,102.6 879.6,103.6 880.2,104.5 880.8,105.5 881.4,106.4 882.0,107.4 882.6,108.3 883.2,109.2 883.8,110.1 884.4,111.0 885.0,111.8 885.6,112.6 886.2,113.4 886.8,114.1 887.4,114.7 888.0,115.3 888.6,115.8 889.2,116.2 889.8,116.5 890.4,116.8 891.0,116.9 891.6,117.0 892.2,117.0 892.8,116.9 893.4,116.7 894.0,116.4 894.6,116.1 895.2,115.6 895.8,115.1 896.4,114.6 897.0,113.9 897.6,113.2 898.2,112.5 898.8,111.7 899.4,110.8 900.0,109.9\"/><text class=\"cap\" x=\"4\" y=\"193\">vtach · 188 bpm · 25 mm/s, 10 mm/mV</text></svg>"
 },
 {
  "id": "usmle-2026-0053",
  "exam": "usmle",
  "step": "Step 2",
  "subject": "Neurology",
  "subject_file": "Neurology",
  "subtopic": "Cholinergic Crisis vs Myasthenic Crisis — Pyridostigmine Overdose",
  "type": "Cholinergic Crisis vs Myasthenic Crisis — Pyridostigmine Overdose",
  "difficulty": 5,
  "created": "2026-07-21",
  "vignette": "A 23-year-old woman with myasthenia gravis on home pyridostigmine develops a upper respiratory infection and, over the past 2 days, self-increases her pyridostigmine dose because her weakness feels worse. She now presents with worsening generalized weakness, excessive salivation, watery diarrhea, and abdominal cramping. On examination she has diffuse muscle fasciculations, bilateral ptosis, and diaphoresis. Vital signs and laboratory studies are shown.",
  "question": "Which of the following is the most appropriate immediate step in management?",
  "options": [
   "Increase the pyridostigmine dose to overcome receptor blockade",
   "Administer edrophonium to confirm the diagnosis before treatment",
   "Begin plasmapheresis emergently before addressing muscarinic symptoms",
   "Administer neostigmine to reverse the muscle weakness",
   "Discontinue pyridostigmine with atropine for muscarinic symptom control"
  ],
  "answer": 5,
  "explanationText": "- 정답근거: 피리도스티그민 자가증량 후 근력저하와 함께 축동(2mm)·서맥(52회/분)·침흘림·설사·복통·발한·근속경련이라는 무스카린 및 니코틴 과잉자극 소견이 나타났으며, PaCO2가 경도 상승해 초기 호흡부전 소견도 보인다. 이는 근무력 자체보다 항콜린에스테라제 과다에 의한 콜린작동위기를 시사하므로 원인 약물을 중단하고 무스카린 증상에 아트로핀을 투여하며 호흡상태를 면밀히 관찰하는 것이 우선이다.\n- 오답감별:\n  - (A) 이미 과다복용으로 위기가 발생한 상황에서 피리도스티그민을 더 늘리면 콜린작동 증상과 호흡부전을 악화시킨다.\n  - (B) 에드로포민(텐실론) 검사는 근무력위기와 콜린작동위기가 모호할 때 쓰는 진단 보조 수단인데, 이미 서맥·축동·침흘림 등 무스카린 과잉 소견이 명확하고 검사 자체가 서맥·기관지경련을 악화시킬 위험이 있어 우선순위가 아니다.\n  - (C) 혈장교환은 근무력위기의 치료 옵션이지만, 콜린작동 증상을 그대로 둔 채 시행하면 서맥·기도분비물 증가로 상태가 악화될 수 있어 원인 조치가 먼저다.\n  - (D) 네오스티그민은 피리도스티그민과 같은 항콜린에스테라제 계열로, 이미 과다상태인 환자에게 투여하면 콜린작동위기를 더 심화시킨다.\n- 임상핵심: 항콜린에스테라제 복용 중 축동·서맥·침흘림·설사 등 무스카린 증상이 근력저하와 함께 나타나면 콜린작동위기를 우선 의심해 약물을 중단하고 아트로핀 및 호흡 모니터링을 시행한다.\n- 출처: Adams and Victor's Principles of Neurology; UpToDate — Myasthenic and Cholinergic Crisis.",
  "explanationItems": [
   {
    "k": "정답근거",
    "v": "피리도스티그민 자가증량 후 근력저하와 함께 축동(2mm)·서맥(52회/분)·침흘림·설사·복통·발한·근속경련이라는 무스카린 및 니코틴 과잉자극 소견이 나타났으며, PaCO2가 경도 상승해 초기 호흡부전 소견도 보인다. 이는 근무력 자체보다 항콜린에스테라제 과다에 의한 콜린작동위기를 시사하므로 원인 약물을 중단하고 무스카린 증상에 아트로핀을 투여하며 호흡상태를 면밀히 관찰하는 것이 우선이다."
   },
   {
    "k": "오답감별",
    "v": "(A) 이미 과다복용으로 위기가 발생한 상황에서 피리도스티그민을 더 늘리면 콜린작동 증상과 호흡부전을 악화시킨다.\n(B) 에드로포민(텐실론) 검사는 근무력위기와 콜린작동위기가 모호할 때 쓰는 진단 보조 수단인데, 이미 서맥·축동·침흘림 등 무스카린 과잉 소견이 명확하고 검사 자체가 서맥·기관지경련을 악화시킬 위험이 있어 우선순위가 아니다.\n(C) 혈장교환은 근무력위기의 치료 옵션이지만, 콜린작동 증상을 그대로 둔 채 시행하면 서맥·기도분비물 증가로 상태가 악화될 수 있어 원인 조치가 먼저다.\n(D) 네오스티그민은 피리도스티그민과 같은 항콜린에스테라제 계열로, 이미 과다상태인 환자에게 투여하면 콜린작동위기를 더 심화시킨다."
   },
   {
    "k": "임상핵심",
    "v": "항콜린에스테라제 복용 중 축동·서맥·침흘림·설사 등 무스카린 증상이 근력저하와 함께 나타나면 콜린작동위기를 우선 의심해 약물을 중단하고 아트로핀 및 호흡 모니터링을 시행한다."
   },
   {
    "k": "출처",
    "v": "Adams and Victor's Principles of Neurology; UpToDate — Myasthenic and Cholinergic Crisis."
   }
  ],
  "source": "USMLE-style / MedKOS (neurology · neuromuscular junction disorders)",
  "vitals": [
   {
    "name": "혈압",
    "value": "98/62 mmHg"
   },
   {
    "name": "맥박",
    "value": "52회/분"
   },
   {
    "name": "호흡",
    "value": "26회/분"
   },
   {
    "name": "체온",
    "value": "36.4 °C"
   }
  ],
  "labs": [
   {
    "name": "동공 크기",
    "value": "양측 2mm",
    "ref": "3–5mm"
   },
   {
    "name": "동맥혈가스 PaCO2",
    "value": "47 mmHg",
    "ref": "35–45"
   },
   {
    "name": "혈당",
    "value": "88 mg/dL",
    "ref": "70–100"
   },
   {
    "name": "혈청 나트륨",
    "value": "138 mEq/L",
    "ref": "135–145"
   },
   {
    "name": "혈청 칼륨",
    "value": "4.0 mEq/L",
    "ref": "3.5–5.0"
   }
  ],
  "appendix": {
   "가이드라인": "근무력위기 vs 콜린작동위기 감별 및 처치\n───────────────────────────────────────────────\n구분 → 소견 → 처치\n  · 근무력위기(항콜린에스테라제 부족) → 동공 정상/산동, 서맥 없음, 근력저하 우세\n    → 피리도스티그민 용량 유지/증량, 필요시 IVIG·혈장교환\n  · 콜린작동위기(항콜린에스테라제 과다) → 축동, 서맥, 침흘림·설사·발한(무스카린 증상),\n    근속경련 → 즉시 약물 중단 + 아트로핀(무스카린 증상 조절) + 호흡 모니터링\n공통: 두 경우 모두 호흡부전 위험 — 노력성폐활량(FVC)·최대흡기압(NIF)으로 조기\n삽관 여부를 판단하며, 애매하면 약물을 보류하고 지지치료를 우선한다(에드로포늄\n검사는 서맥·기관지경련 악화 위험이 있어 진단이 이미 명확한 경우 피한다).\n",
   "최신지견": "임상 소견이 명확한 콜린작동위기에서는 진단 확인을 위한 약물 챌린지보다 즉시 원인 약물 중단이 우선된다.",
   "참고문헌": [
    "Adams and Victor's Principles of Neurology — Myasthenia Gravis",
    "UpToDate — Myasthenic Crisis and Cholinergic Crisis"
   ]
  },
  "figureSvg": ""
 },
 {
  "id": "usmle-2026-0054",
  "exam": "usmle",
  "step": "Step 2",
  "subject": "Psychiatry",
  "subject_file": "Psychiatry",
  "subtopic": "Severe Lithium Toxicity — Thiazide- and Dehydration-Precipitated",
  "type": "Severe Lithium Toxicity — Thiazide- and Dehydration-Precipitated",
  "difficulty": 5,
  "created": "2026-07-21",
  "vignette": "A 54-year-old woman with bipolar I disorder maintained on chronic lithium started hydrochlorothiazide for hypertension 2 weeks ago and then had a week of viral gastroenteritis with vomiting and diarrhea. She now presents with coarse tremor, ataxia, confusion, and myoclonic jerks. She is normothermic and has no muscular rigidity. Vital signs and laboratory studies are shown.",
  "question": "Which of the following is the most appropriate next step in management?",
  "options": [
   "Initiate emergent hemodialysis",
   "Administer sodium polystyrene sulfonate",
   "Start IV normal saline and reassess in 24 hours",
   "Administer IV sodium bicarbonate to alkalinize the urine",
   "Begin oral whole bowel irrigation with polyethylene glycol"
  ],
  "answer": 1,
  "explanationText": "- 정답근거: 티아지드 병용과 위장관염으로 인한 탈수가 리튬 신장 청소율을 낮춰 만성치료 중 급성-만성 리튬 중독이 발생했다(농도 3.2 mEq/L, 급성신손상 동반). 실조·의식변화·근간대경련 같은 중증 신경계 증상과 신부전이 동반되면 농도와 무관하게 혈액투석이 표준 처치다. 정상 체온·근강직 없음은 세로토닌증후군/NMS를 배제하는 데도 도움이 된다.\n- 오답감별:\n  - (B) 나트륨폴리스티렌설포네이트는 고칼륨혈증 치료제로 리튬 제거와 무관하다.\n  - (C) 생리식염수 단독은 경증 중독에 적합하나, 급성신손상으로 청소율이 저하된 중증 신경독성에서는 불충분하며 지연 시 신경학적 손상이 악화될 수 있다.\n  - (D) 중탄산나트륨을 통한 요알칼리화는 살리실산 중독에 효과적인 전략이며, 리튬은 신세뇨관에서 나트륨처럼 재흡수되므로 이 방법으로 제거되지 않는다.\n  - (E) 전장관세척은 급성 정제 다량섭취 직후 위장관 내 미흡수 약물을 배출하기 위한 처치로, 본 환자는 만성 치료 중 축적성 중독이라 흡수할 약물이 남아있지 않아 효과가 없다.\n- 임상핵심: 만성 리튬치료 중 신기능저하를 동반한 중증 신경계 증상(실조·의식변화·근간대경련)이 있으면 농도 수치에만 의존하지 말고 혈액투석 적응증으로 판단한다.\n- 출처: EXTRIP Workgroup Recommendations; Kaplan & Sadock's Synopsis of Psychiatry.",
  "explanationItems": [
   {
    "k": "정답근거",
    "v": "티아지드 병용과 위장관염으로 인한 탈수가 리튬 신장 청소율을 낮춰 만성치료 중 급성-만성 리튬 중독이 발생했다(농도 3.2 mEq/L, 급성신손상 동반). 실조·의식변화·근간대경련 같은 중증 신경계 증상과 신부전이 동반되면 농도와 무관하게 혈액투석이 표준 처치다. 정상 체온·근강직 없음은 세로토닌증후군/NMS를 배제하는 데도 도움이 된다."
   },
   {
    "k": "오답감별",
    "v": "(B) 나트륨폴리스티렌설포네이트는 고칼륨혈증 치료제로 리튬 제거와 무관하다.\n(C) 생리식염수 단독은 경증 중독에 적합하나, 급성신손상으로 청소율이 저하된 중증 신경독성에서는 불충분하며 지연 시 신경학적 손상이 악화될 수 있다.\n(D) 중탄산나트륨을 통한 요알칼리화는 살리실산 중독에 효과적인 전략이며, 리튬은 신세뇨관에서 나트륨처럼 재흡수되므로 이 방법으로 제거되지 않는다.\n(E) 전장관세척은 급성 정제 다량섭취 직후 위장관 내 미흡수 약물을 배출하기 위한 처치로, 본 환자는 만성 치료 중 축적성 중독이라 흡수할 약물이 남아있지 않아 효과가 없다."
   },
   {
    "k": "임상핵심",
    "v": "만성 리튬치료 중 신기능저하를 동반한 중증 신경계 증상(실조·의식변화·근간대경련)이 있으면 농도 수치에만 의존하지 말고 혈액투석 적응증으로 판단한다."
   },
   {
    "k": "출처",
    "v": "EXTRIP Workgroup Recommendations; Kaplan & Sadock's Synopsis of Psychiatry."
   }
  ],
  "source": "USMLE-style / MedKOS (psychiatry · lithium toxicity)",
  "vitals": [
   {
    "name": "혈압",
    "value": "108/70 mmHg"
   },
   {
    "name": "맥박",
    "value": "104회/분"
   },
   {
    "name": "호흡",
    "value": "20회/분"
   },
   {
    "name": "체온",
    "value": "36.6 °C"
   }
  ],
  "labs": [
   {
    "name": "혈청 리튬 농도",
    "value": "3.2 mEq/L",
    "ref": "0.6–1.2"
   },
   {
    "name": "혈청 크레아티닌",
    "value": "2.4 mg/dL",
    "ref": "0.6–1.1"
   },
   {
    "name": "혈청 나트륨",
    "value": "134 mEq/L",
    "ref": "135–145"
   },
   {
    "name": "크레아틴키나아제(CK)",
    "value": "180 U/L",
    "ref": "30–200"
   },
   {
    "name": "백혈구(WBC)",
    "value": "8,200 /mm³",
    "ref": "4,000–10,000"
   }
  ],
  "appendix": {
   "가이드라인": "리튬 중독 중증도별 처치\n───────────────────────────────────────────────\n소견 → 처치\n  · 경증(진전·오심, 신기능 정상, 농도 <2.5) → 원인약물 중단 + 등장성 수액\n  · 중등증~중증(운동실조·의식변화·근간대경련, 신부전 동반 또는 농도 ≥2.5)\n    → 혈액투석(신기능 저하 시 리튬 청소율이 크게 떨어져 수액만으로 부족)\n  · 급성 정제 과량복용(만성치료 중 아님, 섭취 직후) → 전장관세척 고려\n주의: 나트륨폴리스티렌설포네이트·중탄산나트륨 요알칼리화는 리튬 제거에 효과가\n없다(리튬은 신장에서 나트륨과 유사하게 재흡수되어 서방형 킬레이트·산성화 전략이\n작동하지 않음) — 살리실산 중독과 혼동하지 않는다.\n",
   "최신지견": "EXTRIP 권고: 신중증 증상 동반 시 리튬 농도와 무관하게 혈액투석을 고려한다.",
   "참고문헌": [
    "EXTRIP Workgroup — Extracorporeal Treatment for Lithium Poisoning",
    "Kaplan & Sadock's Synopsis of Psychiatry — Lithium Toxicity"
   ]
  },
  "figureSvg": ""
 }
];
