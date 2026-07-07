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
    "v": "BNP는 neprilysin의 기질이므로 약물로 분해가 줄면 혈중 BNP가 상승한다. 반면 NT-proBNP는 neprilysin이 자르지 않으므로 심부전이 호전되면 감소한다. 그래서 ARNI 치료 중에는 반드시 NT-proBNP로 반응을 모니터링한다(BNP로 판단하면 악화로 오해)."
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
    "v": "아급성 심내막염 + E. faecalis 균혈증. 대장 신생물과 enterococcal/ *Streptococcus gallolyticus*(구 bovis) 균혈증의 연관은 고전적 단서다."
   },
   {
    "k": "정답근거",
    "v": "전통적 상승 요법은 ampicillin + aminoglycoside지만, 본 균주는 HLGR이라 gentamicin 상승효과를 기대할 수 없고 독성만 남는다. 이때 ampicillin + ceftriaxone(이중 베타락탐)이 표준이다. 두 약이 서로 다른 penicillin-binding protein을 포화시켜(ampicillin→PBP4/5, ceftriaxone→ PBP2/3) 상승적 살균효과를 낸다. 신독성·이독성도 피할 수 있다."
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
    "v": "(A) AG 상승·HCO3 저하를 설명 못 함. (B) 보상이라기엔 PaCO2가 과도하게 낮음(Winter 벗어남). (D) pH·HCO3 방향상 대사성 알칼리증 근거 없음. (E) 과호흡·저PaCO2와 반대."
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
    "v": "전형적 HIT type II. 노출 5–10일 후 혈소판 >50% 감소 + 새로운 혈전(DVT) + heparin-PF4 항체·SRA 양성 (4T score 高)."
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
    "v": "(A) heparin 지속은 절대 금기. (B) 즉시 warfarin은 괴사 위험. (D) 혈소판 수혈은 연료 공급. (E) LMWH도 HIT 항체와 교차반응."
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
    "v": "호중구 NADPH oxidase가 산소를 O2−(superoxide)로 환원하는 호흡 폭발(respiratory burst)을 못 한다. 그래서 자신의 H2O2를 분해해버리는 catalase-양성 미생물(S. aureus, Serratia, Burkholderia cepacia, Nocardia, Aspergillus)을 죽이지 못한다(catalase-음성균은 자기 H2O2를 남겨 호중구가 이용 → 상대적으로 문제 적음)."
   },
   {
    "k": "검사",
    "v": "DHR 유세포검사(활성산소 있으면 형광↑; CGD는 감소) 또는 고전적 nitroblue tetrazolium(NBT) 검사 음성."
   },
   {
    "k": "오답감별",
    "v": "(B) LAD-1은 CD18 integrin 결손 → 지연된 탯줄 탈락, 농(pus) 형성 안 됨, 백혈구 증가. (C) XLA는 B세포·면역글로불린 부재 → 협막균 재발. (D) WAS는 습진·혈소판감소·감염 3징(X-연관). (E) IL-12R 결핍은 파종성 mycobacteria/Salmonella."
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
    "v": "(A) MG는 postsynaptic AChR 항체 → 사용할수록 악화(decremental), 안구·연수 증상 먼저, 반사 정상, 자율신경 정상. (C) MuSK 항체는 seronegative MG의 일부. (D) VGKC는 신경근긴장(neuromyotonia)/변연계뇌염. (E) 항-GM1은 다초점운동신경병/GBS 변형."
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
    "v": "Ornithine transcarbamylase(OTC) 결핍 — 가장 흔한 요소회로 장애, 유일한 X-연관(남아에서 중증). 신생아 초기 정상 → 단백 부하(수유) 후 급성 고암모니아혈증 뇌증."
   },
   {
    "k": "기전(왜 orotic acid가 오르나)",
    "v": "OTC는 미토콘드리아에서 carbamoyl phosphate + ornithine → citrulline을 만든다. 결핍되면 carbamoyl phosphate가 축적 → 세포질 피리미딘 합성 경로로 유입 → orotic acid ↑. citrulline은 만들지 못해 낮다. 암모니아가 요소로 처리되지 못해 BUN은 낮고, 암모니아가 호흡 중추를 자극해 호흡성 알칼리증(신생아 고암모니아혈증의 단서)."
   },
   {
    "k": "오답감별(감별의 핵심)",
    "v": "- (B) CPS1 결핍: carbamoyl phosphate 자체를 못 만들어 상류가 비므로 orotic acid는 정상/낮음 — 본 증례처럼 orotic acid↑와 맞지 않음. - (C) UMP synthase 결핍(유전성 orotic aciduria): orotic aciduria는 같지만 거대적혈모구빈혈(+)이고 고암모니아혈증은 없다 — 본 증례와 반대. - (D) MCAD 결핍: 금식 시 저케톤성 저혈당, 고암모니아혈증·orotic aciduria 아님. - (E) PKU: 발달지연·musty odor, 요소회로와 무관."
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
    "v": "(B) C3 결핍이면 C3 낮고 화농균·협막균 중증 감염 + 옵소닌화 장애. (C) C1 INH 결핍은 유전성 혈관부종(감염 아님). (D) XLA는 협막균 재발·면역 글로불린 저하. (E) 선택적 IgA는 대개 경미, 점막감염/아나필락시스(수혈)."
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
    "v": "(B) ferrochelatase → erythropoietic protoporphyria(광과민성). (C) uroporphyrinogen decarboxylase → porphyria cutanea tarda(광과민·수포, 가장 흔함). (D) ALA dehydratase 결핍/납중독은 드묾. (E) G6PD는 heme 합성과 무관 (용혈)."
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
    "v": "Vancomycin은 펩티도글리칸 전구체의 말단 D-Ala-D-Ala에 수소결합해 transglycosylation/가교를 막는다. VanA형 VRE는 van 오페론(ligase)이 말단을 D-Ala-D-Lactate로 바꿔 수소결합 하나를 잃게 만들어 친화도를 약 1000배 떨어뜨린다 → 내성."
   },
   {
    "k": "오답감별",
    "v": "(B) β-lactamase는 페니실린/세팔로스포린을 가수분해(반코마이신과 무관). (C) mecA→PBP2a는 MRSA의 β-lactam 내성 기전. (D) efflux는 tetracycline 등. (E) erm 메틸화(23S rRNA)는 macrolide(MLSb) 내성."
   },
   {
    "k": "임상핵심",
    "v": "\"VRE(VanA) = D-Ala-D-Lac.\" 치료는 linezolid 또는 daptomycin(중증 균혈증). MRSA와 혼동 금지(그건 PBP2a)."
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
    "v": "- (B) Gs ADP-ribosylation → cAMP↑: 콜레라 독소, ETEC 이열성독소(LT), 백일해는 Gi 억제로 cAMP↑. - (C) 28S rRNA에서 아데닌 제거(60S 불활성): Shiga / Shiga-like(EHEC) 독소 → HUS. - (D) SNARE 절단: 보툴리눔(ACh 방출 차단→이완마비), 파상풍(glycine/ GABA 방출 차단→경직마비). - (E) 초항원(superantigen): TSST-1, 연쇄상구균 발열외독소 → 다량 사이토카인."
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
    "v": "- (B) tPA 적격자에게 aspirin으로 대체하면 안 됨(항혈소판은 tPA 후 24시간 뒤). - (C) 급성기 permissive hypertension — tPA 줄 때만 <185/110로 조절하고, tPA 안 주면 대개 <220/120까지 허용. <120/80로 급강하하면 penumbra 관류 악화. - (D) 급성 허혈성 뇌졸중에 즉시 전량 헤파린은 이득 없고 출혈 위험. - (E) tPA를 늦추려 MRI를 기다리는 것은 부적절(비조영 CT로 출혈만 배제되면 투여)."
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
    "v": "비후성 유문협착(hypertrophic pyloric stenosis) — 생후 3~6주 남아, 비담즙성 사출성 구토, 수유 후에도 배고파함, 올리브 종괴, 초음파에서 유문 비후."
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
    "v": "(B) AA는 만성 염증(류마티스관절염·만성감염·가족성지중해열)의 serum amyloid A 유래. (C) ATTR는 transthyretin(노인성 심장/유전성 신경). (D) β2-microglobulin은 장기 투석 관련(손목터널). (E) Aβ는 알츠하이머·뇌 아밀로이드혈관병."
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
    "v": "- (B) 저환기: A-a 정상, PaCO2 상승, 산소에 잘 반응. - (C) 저흡입산소(고지대): A-a 정상, 산소로 교정. - (D) V/Q 부조화: A-a 증가하지만 100% 산소에 대체로 교정(저 V/Q 폐포도 결국 산소 도달) — 션트와의 핵심 감별점. - (E) 확산장애: A-a 증가하나 보충 산소에 반응(운동 시 악화)."
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
    "v": "- (B) 신성 요붕증: 신장이 ADH에 저항 → desmopressin에도 반응 없음(핵심 감별점). 원인: lithium, 고칼슘혈증, 유전성 V2/AQP2. - (C) SIADH: ADH 과다 → 농축뇨·저나트륨혈증, 다뇨가 아니라 수분저류. - (D) 원발성 다음증: 수분제한만으로도 어느 정도 농축(기저 ADH 억제 상태), desmopressin에 과반응 안 함. - (E) 삼투성 이뇨(고혈당): 소변 삼투압이 낮지 않고 포도당 존재."
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
    "v": "정맥 황산마그네슘(MgSO4)이 경련 예방·치료의 1차. 동시에 항고혈압제(labetalol·hydralazine·경구 nifedipine)로 중증 고혈압을 조절하고, 근치는 분만(≥34주 중증이면 분만)."
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
    "v": "리튬은 대사되지 않고 신장으로만 배설되며 치료지수가 매우 좁다. Thiazide는 용적을 줄여 근위세뇨관에서 Na⁺(과 함께 Li⁺) 재흡수 를 늘리고, NSAID(ibuprofen)는 신전 prostaglandin을 줄여 신혈류·GFR을 낮춘다 → 리튬 청소율 감소 → 농도 상승 → 독성(조대 진전·실조·혼돈·구토, 중증엔 경련· 신부전)."
   },
   {
    "k": "오답감별",
    "v": "(B) 리튬은 단백결합을 하지 않는 이온이라 displacement 무관. (C) 리튬은 간대사 안 됨 → 효소유도 무관. (D) 독성은 저나트륨/용적감소가 핵심 이지 고칼륨이 아님(thiazide는 오히려 저칼륨 경향). (E) CYP 대사 산물 없음."
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
    "v": "치료용량 acetaminophen은 대부분 glucuronidation/ sulfation(phase II)으로 무독화된다. 과량에서 이 경로가 포화되면 여분이 CYP2E1을 통해 반응성 친전자성 대사물 NAPQI로 전환된다. NAPQI는 평소 glutathione(GSH)과 포합돼 해독되지만, GSH가 고갈되면 간세포 단백에 공유결합해 중심소엽(zone 3) 괴사를 일으킨다."
   },
   {
    "k": "antidote 기전",
    "v": "N-acetylcysteine(NAC)은 cysteine을 공급해 GSH를 재합성 (및 직접 NAPQI 결합)함으로써 간독성을 예방한다 → 정답 A."
   },
   {
    "k": "오답감별",
    "v": "(B) NAC는 CYP2E1 억제제가 아니며 모약을 미변화 배설시키지 않는다. (C) 흡착·킬레이트는 activated charcoal 역할이지 NAC가 아니다. (D) UGT 유도로 작용하지 않는다. (E) naloxone식 수용체 길항 기전이 아니다."
   },
   {
    "k": "임상핵심",
    "v": "시간축이 있어도 nomogram(4시간 이후 레벨)으로 판단하며, 초기엔 AST/ALT가 정상일 수 있다(괴사는 24–72시간에 최고조). NAC는 8–10시간 이내 투여 시 거의 완전 예방, 늦어도 투여 이득이 있다."
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
    "v": "CO는 Hb에 대한 친화도가 O2보다 ~200–250배 높아 carboxyhemoglobin을 형성 → O2 content(운반능) 감소. 게다가 남은 자리의 O2 방출을 방해해 곡선을 좌측 이동(조직에서 O2를 못 놓음) → 조직 저산소 악화."
   },
   {
    "k": "왜 지표가 정상처럼 보이나",
    "v": "용존 O2(PaO2)는 정상이고, 표준 pulse oximeter는 두 파장만 읽어 COHb를 oxyHb로 오인 → SpO2 거짓 정상. 실제 포화도·COHb는 co-oximetry로 측정해야 한다."
   },
   {
    "k": "오답감별",
    "v": "(A) PaO2는 정상이고 곡선은 좌측(우측 아님) 이동. (B) methemoglobin은 별개 기전(산화 스트레스, 초콜릿색 혈액, methylene blue 치료). (D)(E) dead space·확산장벽은 PaO2를 낮추는데 여기선 PaO2가 정상이라 배제."
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
    "v": "Aspergillus는 격벽성(septate) 균사가 예각 (~45°)으로 분지하며 혈관을 침습(angioinvasion) → 혈전·출혈성 경색 → 객혈과 CT의 halo sign(초기)·이후 air-crescent/공동을 만든다. 장기 호중구감소가 결정적 위험인자이고 galactomannan(세포벽 성분)이 진단 보조."
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
    "v": "DKA는 삼투성 이뇨·구토·산증에 의한 세포 내→외 이동 으로 전신 총칼륨이 심하게 고갈돼 있다. 측정 혈청 K가 정상이어도 실제 부족이며, 여기선 이미 3.2 mEq/L로 낮다. Insulin은 K⁺를 세포 내로 이동시켜 급격한 저칼륨혈증 → 치명적 부정맥을 유발할 수 있다."
   },
   {
    "k": "원칙",
    "v": "K < 3.3 mEq/L면 insulin을 보류하고 먼저 K를 정주 보충한다. K가 3.3–5.2면 insulin과 함께 K를 보충, K > 5.2면 K 없이 insulin 시작하며 추적."
   },
   {
    "k": "오답감별",
    "v": "(A) 총칼륨은 높지 않고 오히려 고갈 → 즉시 insulin은 위험. (B) bicarbonate는 대개 불필요(pH < 6.9에서만 고려)하고 저칼륨·역설적 CNS 산증 위험. (C) K 2.5까지 방치하면 부정맥 위험이 이미 크다. (E) calcium은 고칼륨의 심근 안정화용으로 상황이 반대다."
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
    "v": "통증이 홍반에 비해 과도(pain out of proportion), 어두운 변색·긴장성 수포, 염발음(crepitus, 가스형성), 분 단위로 번지는 경계, 전신 독성 → necrotizing fasciitis. 이는 외과적 응급으로 즉각적 광범위 debridement가 예후를 결정하고, 광범위 항생제(예: vancomycin + piperacillin-tazobactam ± clindamycin)는 보조다."
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
    "v": "혈성 설사 후 미세혈관병성 용혈성 빈혈(schistocyte) + 혈소판감소 + 급성 신손상 = Shiga toxin 생성 대장균(STEC, O157:H7)에 의한 전형적 HUS. 치료의 핵심은 지지요법(신중한 수액·전해질, 필요 시 투석)."
   },
   {
    "k": "왜 항생제 금기",
    "v": "항생제와 지사제(loperamide)는 균 사멸·정체로 Shiga toxin 방출·흡수를 늘려 HUS를 유발·악화시킬 수 있어 피한다 → 정답 E."
   },
   {
    "k": "오답감별",
    "v": "(A)(B) 위 이유로 금기(항생제·loperamide). (C) 예방적 혈소판 수혈은 피함(활동성 출혈·침습적 시술 시에만). (D) plasma exchange는 비전형(complement) HUS나 TTP의 치료로, 전형적 소아 STEC-HUS의 1차가 아니다."
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
    "v": "BP 170/110(중증 범위) + 두통 + 요 단백 4+ + 혈소판 90,000(감소) → 중증 전자간증(severe preeclampsia). 38주 이고 CTG가 기저 140·중등도 변이·만기감속 없음(reassuring) → 알고리즘상 \"중증 · 태아 안정\" 분기. 여기에 추정체중 <10 백분위 + 양수과소(AFI 3 cm) 로 IUGR 동반. → MgSO₄ 발작예방 + 혈압조절 후 분만, 자궁경부 양호 (3 cm/90%/-2)·두위·태아안정이므로 유도분만 우선."
   },
   {
    "k": "일반 프레임워크",
    "v": "아래 부록의 결정표(중증도 × 재태주수 × 태아상태)를 통째로 익혀 두면 재태주수·태아상태만 바꿔도 바로 적용된다."
   },
   {
    "k": "오답감별",
    "v": "(A) 38주 중증 전자간증에 expectant/외래관찰은 부적절(분만이 근치). (B) tocolysis는 중증 전자간증에서 금기(임신 연장 위험). (D) betamethasone은 <34주 폐성숙 목적 — 38주엔 불필요하고 분만 지연은 해롭다. (E) 태아가 안정적이면 제왕절개가 필수는 아니며, 무엇보다 MgSO₄·혈압조절을 생략하는 선택은 안전하지 않다."
   },
   {
    "k": "임상핵심",
    "v": "중증 혈압 기준 ≥160/110, 발작예방 MgSO₄, 급성 중증 고혈압 labetalol·hydralazine·nifedipine. 분만 방식은 중증도가 아니라 태아상태· 자궁경부·산과 적응으로 결정한다."
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
    "v": "리듬 스트립에서 뚜렷한 P파가 없고, 기저가 잔물결(f파)처럼 흔들리며 RR 간격이 불규칙하게 불규칙(irregularly irregular) → 심방세동(atrial fibrillation). 진찰의 불규칙한 맥박과 일치."
   },
   {
    "k": "오답감별",
    "v": "(B) 심방조동은 톱니(sawtooth) F파에 흔히 규칙적 전도. (C) MAT는 P파가 3가지 이상 형태 + 불규칙(흔히 COPD). (D) 동성부정맥은 정상 P파가 있고 호흡에 따라 RR이 변동. (E) 심실빈맥은 넓은 QRS가 규칙적으로 빠르게 — 형태가 명확히 다르다."
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
  "figureSvg": "<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 900 198\" width=\"900\" height=\"198\" role=\"img\" aria-label=\"ECG 리듬 스트립 · 25 mm/s, 10 mm/mV\"><style>.bg{fill:#fff}.gmin{stroke:#f4c9c9;stroke-width:0.5}.gmaj{stroke:#e59a9a;stroke-width:1}.trace{fill:none;stroke:#111;stroke-width:1.6;stroke-linejoin:round;stroke-linecap:round}.cap{font:11px -apple-system,Segoe UI,sans-serif;fill:#555}</style><rect class=\"bg\" x=\"0\" y=\"0\" width=\"900\" height=\"180\"/><line x1=\"0\" y1=\"0\" x2=\"0\" y2=\"180\" class=\"gmaj\"/><line x1=\"6\" y1=\"0\" x2=\"6\" y2=\"180\" class=\"gmin\"/><line x1=\"12\" y1=\"0\" x2=\"12\" y2=\"180\" class=\"gmin\"/><line x1=\"18\" y1=\"0\" x2=\"18\" y2=\"180\" class=\"gmin\"/><line x1=\"24\" y1=\"0\" x2=\"24\" y2=\"180\" class=\"gmin\"/><line x1=\"30\" y1=\"0\" x2=\"30\" y2=\"180\" class=\"gmaj\"/><line x1=\"36\" y1=\"0\" x2=\"36\" y2=\"180\" class=\"gmin\"/><line x1=\"42\" y1=\"0\" x2=\"42\" y2=\"180\" class=\"gmin\"/><line x1=\"48\" y1=\"0\" x2=\"48\" y2=\"180\" class=\"gmin\"/><line x1=\"54\" y1=\"0\" x2=\"54\" y2=\"180\" class=\"gmin\"/><line x1=\"60\" y1=\"0\" x2=\"60\" y2=\"180\" class=\"gmaj\"/><line x1=\"66\" y1=\"0\" x2=\"66\" y2=\"180\" class=\"gmin\"/><line x1=\"72\" y1=\"0\" x2=\"72\" y2=\"180\" class=\"gmin\"/><line x1=\"78\" y1=\"0\" x2=\"78\" y2=\"180\" class=\"gmin\"/><line x1=\"84\" y1=\"0\" x2=\"84\" y2=\"180\" class=\"gmin\"/><line x1=\"90\" y1=\"0\" x2=\"90\" y2=\"180\" class=\"gmaj\"/><line x1=\"96\" y1=\"0\" x2=\"96\" y2=\"180\" class=\"gmin\"/><line x1=\"102\" y1=\"0\" x2=\"102\" y2=\"180\" class=\"gmin\"/><line x1=\"108\" y1=\"0\" x2=\"108\" y2=\"180\" class=\"gmin\"/><line x1=\"114\" y1=\"0\" x2=\"114\" y2=\"180\" class=\"gmin\"/><line x1=\"120\" y1=\"0\" x2=\"120\" y2=\"180\" class=\"gmaj\"/><line x1=\"126\" y1=\"0\" x2=\"126\" y2=\"180\" class=\"gmin\"/><line x1=\"132\" y1=\"0\" x2=\"132\" y2=\"180\" class=\"gmin\"/><line x1=\"138\" y1=\"0\" x2=\"138\" y2=\"180\" class=\"gmin\"/><line x1=\"144\" y1=\"0\" x2=\"144\" y2=\"180\" class=\"gmin\"/><line x1=\"150\" y1=\"0\" x2=\"150\" y2=\"180\" class=\"gmaj\"/><line x1=\"156\" y1=\"0\" x2=\"156\" y2=\"180\" class=\"gmin\"/><line x1=\"162\" y1=\"0\" x2=\"162\" y2=\"180\" class=\"gmin\"/><line x1=\"168\" y1=\"0\" x2=\"168\" y2=\"180\" class=\"gmin\"/><line x1=\"174\" y1=\"0\" x2=\"174\" y2=\"180\" class=\"gmin\"/><line x1=\"180\" y1=\"0\" x2=\"180\" y2=\"180\" class=\"gmaj\"/><line x1=\"186\" y1=\"0\" x2=\"186\" y2=\"180\" class=\"gmin\"/><line x1=\"192\" y1=\"0\" x2=\"192\" y2=\"180\" class=\"gmin\"/><line x1=\"198\" y1=\"0\" x2=\"198\" y2=\"180\" class=\"gmin\"/><line x1=\"204\" y1=\"0\" x2=\"204\" y2=\"180\" class=\"gmin\"/><line x1=\"210\" y1=\"0\" x2=\"210\" y2=\"180\" class=\"gmaj\"/><line x1=\"216\" y1=\"0\" x2=\"216\" y2=\"180\" class=\"gmin\"/><line x1=\"222\" y1=\"0\" x2=\"222\" y2=\"180\" class=\"gmin\"/><line x1=\"228\" y1=\"0\" x2=\"228\" y2=\"180\" class=\"gmin\"/><line x1=\"234\" y1=\"0\" x2=\"234\" y2=\"180\" class=\"gmin\"/><line x1=\"240\" y1=\"0\" x2=\"240\" y2=\"180\" class=\"gmaj\"/><line x1=\"246\" y1=\"0\" x2=\"246\" y2=\"180\" class=\"gmin\"/><line x1=\"252\" y1=\"0\" x2=\"252\" y2=\"180\" class=\"gmin\"/><line x1=\"258\" y1=\"0\" x2=\"258\" y2=\"180\" class=\"gmin\"/><line x1=\"264\" y1=\"0\" x2=\"264\" y2=\"180\" class=\"gmin\"/><line x1=\"270\" y1=\"0\" x2=\"270\" y2=\"180\" class=\"gmaj\"/><line x1=\"276\" y1=\"0\" x2=\"276\" y2=\"180\" class=\"gmin\"/><line x1=\"282\" y1=\"0\" x2=\"282\" y2=\"180\" class=\"gmin\"/><line x1=\"288\" y1=\"0\" x2=\"288\" y2=\"180\" class=\"gmin\"/><line x1=\"294\" y1=\"0\" x2=\"294\" y2=\"180\" class=\"gmin\"/><line x1=\"300\" y1=\"0\" x2=\"300\" y2=\"180\" class=\"gmaj\"/><line x1=\"306\" y1=\"0\" x2=\"306\" y2=\"180\" class=\"gmin\"/><line x1=\"312\" y1=\"0\" x2=\"312\" y2=\"180\" class=\"gmin\"/><line x1=\"318\" y1=\"0\" x2=\"318\" y2=\"180\" class=\"gmin\"/><line x1=\"324\" y1=\"0\" x2=\"324\" y2=\"180\" class=\"gmin\"/><line x1=\"330\" y1=\"0\" x2=\"330\" y2=\"180\" class=\"gmaj\"/><line x1=\"336\" y1=\"0\" x2=\"336\" y2=\"180\" class=\"gmin\"/><line x1=\"342\" y1=\"0\" x2=\"342\" y2=\"180\" class=\"gmin\"/><line x1=\"348\" y1=\"0\" x2=\"348\" y2=\"180\" class=\"gmin\"/><line x1=\"354\" y1=\"0\" x2=\"354\" y2=\"180\" class=\"gmin\"/><line x1=\"360\" y1=\"0\" x2=\"360\" y2=\"180\" class=\"gmaj\"/><line x1=\"366\" y1=\"0\" x2=\"366\" y2=\"180\" class=\"gmin\"/><line x1=\"372\" y1=\"0\" x2=\"372\" y2=\"180\" class=\"gmin\"/><line x1=\"378\" y1=\"0\" x2=\"378\" y2=\"180\" class=\"gmin\"/><line x1=\"384\" y1=\"0\" x2=\"384\" y2=\"180\" class=\"gmin\"/><line x1=\"390\" y1=\"0\" x2=\"390\" y2=\"180\" class=\"gmaj\"/><line x1=\"396\" y1=\"0\" x2=\"396\" y2=\"180\" class=\"gmin\"/><line x1=\"402\" y1=\"0\" x2=\"402\" y2=\"180\" class=\"gmin\"/><line x1=\"408\" y1=\"0\" x2=\"408\" y2=\"180\" class=\"gmin\"/><line x1=\"414\" y1=\"0\" x2=\"414\" y2=\"180\" class=\"gmin\"/><line x1=\"420\" y1=\"0\" x2=\"420\" y2=\"180\" class=\"gmaj\"/><line x1=\"426\" y1=\"0\" x2=\"426\" y2=\"180\" class=\"gmin\"/><line x1=\"432\" y1=\"0\" x2=\"432\" y2=\"180\" class=\"gmin\"/><line x1=\"438\" y1=\"0\" x2=\"438\" y2=\"180\" class=\"gmin\"/><line x1=\"444\" y1=\"0\" x2=\"444\" y2=\"180\" class=\"gmin\"/><line x1=\"450\" y1=\"0\" x2=\"450\" y2=\"180\" class=\"gmaj\"/><line x1=\"456\" y1=\"0\" x2=\"456\" y2=\"180\" class=\"gmin\"/><line x1=\"462\" y1=\"0\" x2=\"462\" y2=\"180\" class=\"gmin\"/><line x1=\"468\" y1=\"0\" x2=\"468\" y2=\"180\" class=\"gmin\"/><line x1=\"474\" y1=\"0\" x2=\"474\" y2=\"180\" class=\"gmin\"/><line x1=\"480\" y1=\"0\" x2=\"480\" y2=\"180\" class=\"gmaj\"/><line x1=\"486\" y1=\"0\" x2=\"486\" y2=\"180\" class=\"gmin\"/><line x1=\"492\" y1=\"0\" x2=\"492\" y2=\"180\" class=\"gmin\"/><line x1=\"498\" y1=\"0\" x2=\"498\" y2=\"180\" class=\"gmin\"/><line x1=\"504\" y1=\"0\" x2=\"504\" y2=\"180\" class=\"gmin\"/><line x1=\"510\" y1=\"0\" x2=\"510\" y2=\"180\" class=\"gmaj\"/><line x1=\"516\" y1=\"0\" x2=\"516\" y2=\"180\" class=\"gmin\"/><line x1=\"522\" y1=\"0\" x2=\"522\" y2=\"180\" class=\"gmin\"/><line x1=\"528\" y1=\"0\" x2=\"528\" y2=\"180\" class=\"gmin\"/><line x1=\"534\" y1=\"0\" x2=\"534\" y2=\"180\" class=\"gmin\"/><line x1=\"540\" y1=\"0\" x2=\"540\" y2=\"180\" class=\"gmaj\"/><line x1=\"546\" y1=\"0\" x2=\"546\" y2=\"180\" class=\"gmin\"/><line x1=\"552\" y1=\"0\" x2=\"552\" y2=\"180\" class=\"gmin\"/><line x1=\"558\" y1=\"0\" x2=\"558\" y2=\"180\" class=\"gmin\"/><line x1=\"564\" y1=\"0\" x2=\"564\" y2=\"180\" class=\"gmin\"/><line x1=\"570\" y1=\"0\" x2=\"570\" y2=\"180\" class=\"gmaj\"/><line x1=\"576\" y1=\"0\" x2=\"576\" y2=\"180\" class=\"gmin\"/><line x1=\"582\" y1=\"0\" x2=\"582\" y2=\"180\" class=\"gmin\"/><line x1=\"588\" y1=\"0\" x2=\"588\" y2=\"180\" class=\"gmin\"/><line x1=\"594\" y1=\"0\" x2=\"594\" y2=\"180\" class=\"gmin\"/><line x1=\"600\" y1=\"0\" x2=\"600\" y2=\"180\" class=\"gmaj\"/><line x1=\"606\" y1=\"0\" x2=\"606\" y2=\"180\" class=\"gmin\"/><line x1=\"612\" y1=\"0\" x2=\"612\" y2=\"180\" class=\"gmin\"/><line x1=\"618\" y1=\"0\" x2=\"618\" y2=\"180\" class=\"gmin\"/><line x1=\"624\" y1=\"0\" x2=\"624\" y2=\"180\" class=\"gmin\"/><line x1=\"630\" y1=\"0\" x2=\"630\" y2=\"180\" class=\"gmaj\"/><line x1=\"636\" y1=\"0\" x2=\"636\" y2=\"180\" class=\"gmin\"/><line x1=\"642\" y1=\"0\" x2=\"642\" y2=\"180\" class=\"gmin\"/><line x1=\"648\" y1=\"0\" x2=\"648\" y2=\"180\" class=\"gmin\"/><line x1=\"654\" y1=\"0\" x2=\"654\" y2=\"180\" class=\"gmin\"/><line x1=\"660\" y1=\"0\" x2=\"660\" y2=\"180\" class=\"gmaj\"/><line x1=\"666\" y1=\"0\" x2=\"666\" y2=\"180\" class=\"gmin\"/><line x1=\"672\" y1=\"0\" x2=\"672\" y2=\"180\" class=\"gmin\"/><line x1=\"678\" y1=\"0\" x2=\"678\" y2=\"180\" class=\"gmin\"/><line x1=\"684\" y1=\"0\" x2=\"684\" y2=\"180\" class=\"gmin\"/><line x1=\"690\" y1=\"0\" x2=\"690\" y2=\"180\" class=\"gmaj\"/><line x1=\"696\" y1=\"0\" x2=\"696\" y2=\"180\" class=\"gmin\"/><line x1=\"702\" y1=\"0\" x2=\"702\" y2=\"180\" class=\"gmin\"/><line x1=\"708\" y1=\"0\" x2=\"708\" y2=\"180\" class=\"gmin\"/><line x1=\"714\" y1=\"0\" x2=\"714\" y2=\"180\" class=\"gmin\"/><line x1=\"720\" y1=\"0\" x2=\"720\" y2=\"180\" class=\"gmaj\"/><line x1=\"726\" y1=\"0\" x2=\"726\" y2=\"180\" class=\"gmin\"/><line x1=\"732\" y1=\"0\" x2=\"732\" y2=\"180\" class=\"gmin\"/><line x1=\"738\" y1=\"0\" x2=\"738\" y2=\"180\" class=\"gmin\"/><line x1=\"744\" y1=\"0\" x2=\"744\" y2=\"180\" class=\"gmin\"/><line x1=\"750\" y1=\"0\" x2=\"750\" y2=\"180\" class=\"gmaj\"/><line x1=\"756\" y1=\"0\" x2=\"756\" y2=\"180\" class=\"gmin\"/><line x1=\"762\" y1=\"0\" x2=\"762\" y2=\"180\" class=\"gmin\"/><line x1=\"768\" y1=\"0\" x2=\"768\" y2=\"180\" class=\"gmin\"/><line x1=\"774\" y1=\"0\" x2=\"774\" y2=\"180\" class=\"gmin\"/><line x1=\"780\" y1=\"0\" x2=\"780\" y2=\"180\" class=\"gmaj\"/><line x1=\"786\" y1=\"0\" x2=\"786\" y2=\"180\" class=\"gmin\"/><line x1=\"792\" y1=\"0\" x2=\"792\" y2=\"180\" class=\"gmin\"/><line x1=\"798\" y1=\"0\" x2=\"798\" y2=\"180\" class=\"gmin\"/><line x1=\"804\" y1=\"0\" x2=\"804\" y2=\"180\" class=\"gmin\"/><line x1=\"810\" y1=\"0\" x2=\"810\" y2=\"180\" class=\"gmaj\"/><line x1=\"816\" y1=\"0\" x2=\"816\" y2=\"180\" class=\"gmin\"/><line x1=\"822\" y1=\"0\" x2=\"822\" y2=\"180\" class=\"gmin\"/><line x1=\"828\" y1=\"0\" x2=\"828\" y2=\"180\" class=\"gmin\"/><line x1=\"834\" y1=\"0\" x2=\"834\" y2=\"180\" class=\"gmin\"/><line x1=\"840\" y1=\"0\" x2=\"840\" y2=\"180\" class=\"gmaj\"/><line x1=\"846\" y1=\"0\" x2=\"846\" y2=\"180\" class=\"gmin\"/><line x1=\"852\" y1=\"0\" x2=\"852\" y2=\"180\" class=\"gmin\"/><line x1=\"858\" y1=\"0\" x2=\"858\" y2=\"180\" class=\"gmin\"/><line x1=\"864\" y1=\"0\" x2=\"864\" y2=\"180\" class=\"gmin\"/><line x1=\"870\" y1=\"0\" x2=\"870\" y2=\"180\" class=\"gmaj\"/><line x1=\"876\" y1=\"0\" x2=\"876\" y2=\"180\" class=\"gmin\"/><line x1=\"882\" y1=\"0\" x2=\"882\" y2=\"180\" class=\"gmin\"/><line x1=\"888\" y1=\"0\" x2=\"888\" y2=\"180\" class=\"gmin\"/><line x1=\"894\" y1=\"0\" x2=\"894\" y2=\"180\" class=\"gmin\"/><line x1=\"900\" y1=\"0\" x2=\"900\" y2=\"180\" class=\"gmaj\"/><line x1=\"0\" y1=\"0\" x2=\"900\" y2=\"0\" class=\"gmaj\"/><line x1=\"0\" y1=\"6\" x2=\"900\" y2=\"6\" class=\"gmin\"/><line x1=\"0\" y1=\"12\" x2=\"900\" y2=\"12\" class=\"gmin\"/><line x1=\"0\" y1=\"18\" x2=\"900\" y2=\"18\" class=\"gmin\"/><line x1=\"0\" y1=\"24\" x2=\"900\" y2=\"24\" class=\"gmin\"/><line x1=\"0\" y1=\"30\" x2=\"900\" y2=\"30\" class=\"gmaj\"/><line x1=\"0\" y1=\"36\" x2=\"900\" y2=\"36\" class=\"gmin\"/><line x1=\"0\" y1=\"42\" x2=\"900\" y2=\"42\" class=\"gmin\"/><line x1=\"0\" y1=\"48\" x2=\"900\" y2=\"48\" class=\"gmin\"/><line x1=\"0\" y1=\"54\" x2=\"900\" y2=\"54\" class=\"gmin\"/><line x1=\"0\" y1=\"60\" x2=\"900\" y2=\"60\" class=\"gmaj\"/><line x1=\"0\" y1=\"66\" x2=\"900\" y2=\"66\" class=\"gmin\"/><line x1=\"0\" y1=\"72\" x2=\"900\" y2=\"72\" class=\"gmin\"/><line x1=\"0\" y1=\"78\" x2=\"900\" y2=\"78\" class=\"gmin\"/><line x1=\"0\" y1=\"84\" x2=\"900\" y2=\"84\" class=\"gmin\"/><line x1=\"0\" y1=\"90\" x2=\"900\" y2=\"90\" class=\"gmaj\"/><line x1=\"0\" y1=\"96\" x2=\"900\" y2=\"96\" class=\"gmin\"/><line x1=\"0\" y1=\"102\" x2=\"900\" y2=\"102\" class=\"gmin\"/><line x1=\"0\" y1=\"108\" x2=\"900\" y2=\"108\" class=\"gmin\"/><line x1=\"0\" y1=\"114\" x2=\"900\" y2=\"114\" class=\"gmin\"/><line x1=\"0\" y1=\"120\" x2=\"900\" y2=\"120\" class=\"gmaj\"/><line x1=\"0\" y1=\"126\" x2=\"900\" y2=\"126\" class=\"gmin\"/><line x1=\"0\" y1=\"132\" x2=\"900\" y2=\"132\" class=\"gmin\"/><line x1=\"0\" y1=\"138\" x2=\"900\" y2=\"138\" class=\"gmin\"/><line x1=\"0\" y1=\"144\" x2=\"900\" y2=\"144\" class=\"gmin\"/><line x1=\"0\" y1=\"150\" x2=\"900\" y2=\"150\" class=\"gmaj\"/><line x1=\"0\" y1=\"156\" x2=\"900\" y2=\"156\" class=\"gmin\"/><line x1=\"0\" y1=\"162\" x2=\"900\" y2=\"162\" class=\"gmin\"/><line x1=\"0\" y1=\"168\" x2=\"900\" y2=\"168\" class=\"gmin\"/><line x1=\"0\" y1=\"174\" x2=\"900\" y2=\"174\" class=\"gmin\"/><line x1=\"0\" y1=\"180\" x2=\"900\" y2=\"180\" class=\"gmaj\"/><polyline class=\"trace\" points=\"0.0,88.8 0.6,88.5 1.2,88.2 1.8,88.0 2.4,88.0 3.0,88.1 3.6,88.2 4.2,88.4 4.8,88.7 5.4,89.0 6.0,89.2 6.6,89.5 7.2,89.7 7.8,89.9 8.4,90.1 9.0,90.2 9.6,90.2 10.2,90.2 10.8,90.2 11.4,90.2 12.0,90.2 12.6,90.3 13.2,90.3 13.8,90.4 14.4,90.5 15.0,90.7 15.6,90.9 16.2,91.1 16.8,91.3 17.4,91.4 18.0,91.6 18.6,91.6 19.2,91.6 19.8,91.5 20.4,91.3 21.0,90.9 21.6,90.6 22.2,90.1 22.8,89.6 23.4,89.1 24.0,88.6 24.6,88.1 25.2,87.7 25.8,87.4 26.4,87.2 27.0,87.2 27.6,87.3 28.2,87.6 28.8,87.9 29.4,88.4 30.0,89.0 30.6,89.7 31.2,90.3 31.8,91.0 32.4,91.6 33.0,92.1 33.6,92.5 34.2,92.7 34.8,92.9 35.4,92.8 36.0,92.7 36.6,92.4 37.2,92.0 37.8,91.5 38.4,91.0 39.0,90.4 39.6,89.9 40.2,89.4 40.8,89.0 41.4,88.8 42.0,88.9 42.6,89.5 43.2,90.3 43.8,90.1 44.4,87.4 45.0,81.5 45.6,72.0 46.2,59.6 46.8,45.8 47.4,33.8 48.0,27.4 48.6,29.0 49.2,38.3 49.8,52.5 50.4,67.8 51.0,81.1 51.6,90.9 52.2,96.8 52.8,99.4 53.4,99.5 54.0,98.0 54.6,95.9 55.2,94.0 55.8,92.6 56.4,91.9 57.0,91.6 57.6,91.6 58.2,91.7 58.8,91.8 59.4,91.9 60.0,91.8 60.6,91.7 61.2,91.4 61.8,91.1 62.4,90.7 63.0,90.2 63.6,89.6 64.2,89.0 64.8,88.5 65.4,88.0 66.0,87.6 66.6,87.3 67.2,87.1 67.8,87.1 68.4,87.2 69.0,87.5 69.6,87.9 70.2,88.4 70.8,88.9 71.4,89.6 72.0,90.2 72.6,90.8 73.2,91.3 73.8,91.8 74.4,92.1 75.0,92.2 75.6,92.2 76.2,92.0 76.8,91.7 77.4,91.2 78.0,90.6 78.6,89.8 79.2,89.0 79.8,88.1 80.4,87.2 81.0,86.2 81.6,85.3 82.2,84.4 82.8,83.5 83.4,82.7 84.0,81.9 84.6,81.1 85.2,80.4 85.8,79.6 86.4,78.9 87.0,78.2 87.6,77.4 88.2,76.7 88.8,76.0 89.4,75.3 90.0,74.7 90.6,74.1 91.2,73.6 91.8,73.2 92.4,73.0 93.0,72.9 93.6,72.9 94.2,73.2 94.8,73.7 95.4,74.3 96.0,75.0 96.6,76.0 97.2,77.0 97.8,78.0 98.4,79.2 99.0,80.2 99.6,81.3 100.2,82.3 100.8,83.1 101.4,83.8 102.0,84.4 102.6,84.8 103.2,85.1 103.8,85.3 104.4,85.4 105.0,85.4 105.6,85.3 106.2,85.3 106.8,85.3 107.4,85.4 108.0,85.5 108.6,85.8 109.2,86.2 109.8,86.6 110.4,87.2 111.0,87.9 111.6,88.6 112.2,89.3 112.8,90.0 113.4,90.7 114.0,91.3 114.6,91.8 115.2,92.2 115.8,92.5 116.4,92.6 117.0,92.6 117.6,92.4 118.2,92.1 118.8,91.8 119.4,91.4 120.0,90.9 120.6,90.4 121.2,90.0 121.8,89.6 122.4,89.3 123.0,89.0 123.6,88.9 124.2,88.8 124.8,88.8 125.4,88.8 126.0,88.9 126.6,89.0 127.2,89.1 127.8,89.3 128.4,89.4 129.0,89.4 129.6,89.5 130.2,89.5 130.8,89.6 131.4,90.0 132.0,90.7 132.6,91.4 133.2,90.9 133.8,87.8 134.4,81.3 135.0,71.3 135.6,58.5 136.2,44.8 136.8,33.5 137.4,28.2 138.0,31.2 138.6,41.6 139.2,56.5 139.8,71.9 140.4,84.9 141.0,94.2 141.6,99.6 142.2,101.6 142.8,101.1 143.4,98.9 144.0,96.1 144.6,93.5 145.2,91.3 145.8,89.8 146.4,88.8 147.0,88.0 147.6,87.5 148.2,87.2 148.8,87.0 149.4,87.0 150.0,87.2 150.6,87.5 151.2,87.9 151.8,88.4 152.4,89.0 153.0,89.6 153.6,90.3 154.2,90.9 154.8,91.4 155.4,91.8 156.0,92.2 156.6,92.4 157.2,92.5 157.8,92.4 158.4,92.2 159.0,92.0 159.6,91.6 160.2,91.2 160.8,90.8 161.4,90.3 162.0,89.9 162.6,89.5 163.2,89.2 163.8,88.9 164.4,88.7 165.0,88.5 165.6,88.3 166.2,88.2 166.8,88.0 167.4,87.9 168.0,87.7 168.6,87.4 169.2,87.0 169.8,86.6 170.4,86.0 171.0,85.4 171.6,84.7 172.2,83.9 172.8,83.1 173.4,82.3 174.0,81.5 174.6,80.7 175.2,79.9 175.8,79.2 176.4,78.6 177.0,78.0 177.6,77.6 178.2,77.2 178.8,76.8 179.4,76.6 180.0,76.4 180.6,76.3 181.2,76.5 181.8,77.1 182.4,77.7 183.0,77.1 183.6,73.9 184.2,67.2 184.8,57.1 185.4,44.1 186.0,30.1 186.6,18.4 187.2,12.7 187.8,15.3 188.4,25.6 189.0,40.6 189.6,56.5 190.2,70.5 190.8,80.9 191.4,87.6 192.0,91.2 192.6,92.2 193.2,91.8 193.8,90.8 194.4,89.9 195.0,89.5 195.6,89.5 196.2,89.9 196.8,90.4 197.4,90.8 198.0,91.1 198.6,91.2 199.2,91.3 199.8,91.2 200.4,91.0 201.0,90.8 201.6,90.5 202.2,90.2 202.8,90.0 203.4,89.7 204.0,89.5 204.6,89.4 205.2,89.4 205.8,89.3 206.4,89.3 207.0,89.4 207.6,89.4 208.2,89.4 208.8,89.4 209.4,89.4 210.0,89.4 210.6,89.3 211.2,89.1 211.8,89.0 212.4,88.8 213.0,88.6 213.6,88.4 214.2,88.3 214.8,88.2 215.4,88.1 216.0,88.1 216.6,88.2 217.2,88.2 217.8,88.3 218.4,88.4 219.0,88.5 219.6,88.5 220.2,88.5 220.8,88.3 221.4,87.9 222.0,87.4 222.6,86.7 223.2,85.9 223.8,84.8 224.4,83.6 225.0,82.2 225.6,80.8 226.2,79.2 226.8,77.7 227.4,76.2 228.0,74.8 228.6,73.5 229.2,72.4 229.8,71.6 230.4,70.9 231.0,70.6 231.6,70.5 232.2,70.7 232.8,71.2 233.4,71.8 234.0,72.7 234.6,73.7 235.2,74.8 235.8,76.0 236.4,77.2 237.0,78.3 237.6,79.4 238.2,80.5 238.8,81.4 239.4,82.3 240.0,83.0 240.6,83.7 241.2,84.3 241.8,84.8 242.4,85.2 243.0,85.6 243.6,86.0 244.2,86.4 244.8,86.8 245.4,87.2 246.0,87.5 246.6,88.1 247.2,88.8 247.8,89.9 248.4,90.8 249.0,90.2 249.6,86.7 250.2,79.6 250.8,69.1 251.4,55.7 252.0,41.8 252.6,30.6 253.2,25.9 253.8,29.5 254.4,40.4 255.0,55.2 255.6,70.2 256.2,82.8 256.8,91.7 257.4,97.0 258.0,99.2 258.6,99.1 259.2,97.7 259.8,95.9 260.4,94.4 261.0,93.4 261.6,93.0 262.2,92.8 262.8,92.8 263.4,92.8 264.0,92.7 264.6,92.4 265.2,92.0 265.8,91.6 266.4,91.0 267.0,90.3 267.6,89.7 268.2,89.0 268.8,88.4 269.4,87.9 270.0,87.5 270.6,87.2 271.2,87.1 271.8,87.1 272.4,87.3 273.0,87.6 273.6,88.0 274.2,88.5 274.8,89.0 275.4,89.5 276.0,90.1 276.6,90.5 277.2,90.9 277.8,91.2 278.4,91.4 279.0,91.5 279.6,91.5 280.2,91.3 280.8,91.1 281.4,90.7 282.0,90.3 282.6,89.8 283.2,89.3 283.8,88.8 284.4,88.3 285.0,87.7 285.6,87.2 286.2,86.6 286.8,86.0 287.4,85.3 288.0,84.7 288.6,83.9 289.2,83.1 289.8,82.2 290.4,81.3 291.0,80.2 291.6,79.2 292.2,78.0 292.8,76.9 293.4,75.8 294.0,74.8 294.6,73.9 295.2,73.1 295.8,72.5 296.4,72.1 297.0,71.9 297.6,71.9 298.2,72.2 298.8,72.6 299.4,73.3 300.0,74.1 300.6,75.1 301.2,76.2 301.8,77.3 302.4,78.5 303.0,79.6 303.6,80.6 304.2,81.5 304.8,82.3 305.4,82.9 306.0,83.4 306.6,83.8 307.2,84.0 307.8,84.2 308.4,84.3 309.0,84.5 309.6,84.9 310.2,85.7 310.8,86.6 311.4,86.6 312.0,84.1 312.6,78.4 313.2,69.2 313.8,57.0 314.4,43.6 315.0,32.1 315.6,26.2 316.2,28.3 316.8,38.1 317.4,52.8 318.0,68.5 318.6,82.2 319.2,92.2 319.8,98.3 320.4,101.0 321.0,101.0 321.6,99.3 322.2,96.9 322.8,94.5 323.4,92.8 324.0,91.6 324.6,90.9 325.2,90.5 325.8,90.4 326.4,90.3 327.0,90.3 327.6,90.3 328.2,90.3 328.8,90.3 329.4,90.2 330.0,90.2 330.6,90.1 331.2,90.0 331.8,89.8 332.4,89.5 333.0,89.2 333.6,88.9 334.2,88.7 334.8,88.4 335.4,88.2 336.0,88.0 336.6,88.0 337.2,88.0 337.8,88.1 338.4,88.4 339.0,88.7 339.6,89.2 340.2,89.7 340.8,90.2 341.4,90.7 342.0,91.2 342.6,91.6 343.2,91.9 343.8,92.0 344.4,92.0 345.0,91.9 345.6,91.5 346.2,90.9 346.8,90.2 347.4,89.3 348.0,88.2 348.6,87.1 349.2,85.9 349.8,84.6 350.4,83.4 351.0,82.2 351.6,81.0 352.2,80.0 352.8,79.0 353.4,78.2 354.0,77.4 354.6,76.8 355.2,76.3 355.8,75.9 356.4,75.5 357.0,75.2 357.6,75.0 358.2,74.8 358.8,74.7 359.4,74.6 360.0,74.5 360.6,74.5 361.2,74.6 361.8,74.7 362.4,74.8 363.0,75.1 363.6,75.5 364.2,76.0 364.8,76.5 365.4,77.2 366.0,78.0 366.6,78.8 367.2,79.7 367.8,80.7 368.4,81.6 369.0,82.5 369.6,83.4 370.2,84.1 370.8,84.8 371.4,85.4 372.0,85.8 372.6,86.2 373.2,86.4 373.8,86.6 374.4,86.6 375.0,86.7 375.6,86.7 376.2,86.7 376.8,86.8 377.4,86.9 378.0,87.2 378.6,87.5 379.2,87.9 379.8,88.4 380.4,89.0 381.0,89.6 381.6,90.2 382.2,90.9 382.8,91.5 383.4,92.1 384.0,92.5 384.6,92.8 385.2,93.0 385.8,93.0 386.4,92.8 387.0,92.5 387.6,92.1 388.2,91.6 388.8,91.0 389.4,90.4 390.0,89.7 390.6,89.1 391.2,88.6 391.8,88.1 392.4,87.8 393.0,87.6 393.6,87.5 394.2,87.5 394.8,87.7 395.4,88.0 396.0,88.3 396.6,88.7 397.2,89.1 397.8,89.6 398.4,90.0 399.0,90.3 399.6,90.6 400.2,90.8 400.8,91.0 401.4,91.0 402.0,91.0 402.6,91.0 403.2,90.9 403.8,90.9 404.4,90.8 405.0,91.1 405.6,91.6 406.2,92.5 406.8,92.6 407.4,90.7 408.0,85.6 408.6,76.9 409.2,64.9 409.8,51.1 410.4,38.0 411.0,29.5 411.6,28.7 412.2,35.8 412.8,48.8 413.4,63.8 414.0,77.5 414.6,87.9 415.2,94.4 415.8,97.5 416.4,97.7 417.0,96.2 417.6,93.8 418.2,91.6 418.8,89.9 419.4,88.9 420.0,88.6 420.6,88.8 421.2,89.2 421.8,89.8 422.4,90.4 423.0,91.0 423.6,91.6 424.2,92.1 424.8,92.5 425.4,92.8 426.0,93.0 426.6,93.0 427.2,92.8 427.8,92.5 428.4,92.1 429.0,91.6 429.6,91.0 430.2,90.4 430.8,89.8 431.4,89.2 432.0,88.6 432.6,88.2 433.2,87.9 433.8,87.7 434.4,87.6 435.0,87.6 435.6,87.7 436.2,87.9 436.8,88.2 437.4,88.5 438.0,88.8 438.6,89.0 439.2,89.2 439.8,89.4 440.4,89.4 441.0,89.3 441.6,89.2 442.2,88.9 442.8,88.5 443.4,88.1 444.0,87.5 444.6,86.9 445.2,86.3 445.8,85.6 446.4,84.9 447.0,84.2 447.6,83.5 448.2,82.7 448.8,82.0 449.4,81.2 450.0,80.4 450.6,79.5 451.2,78.6 451.8,77.7 452.4,76.8 453.0,75.8 453.6,74.9 454.2,74.0 454.8,73.2 455.4,72.5 456.0,71.9 456.6,71.5 457.2,71.2 457.8,71.2 458.4,71.4 459.0,71.8 459.6,72.5 460.2,73.4 460.8,74.5 461.4,75.8 462.0,77.2 462.6,78.7 463.2,80.3 463.8,81.8 464.4,83.3 465.0,84.7 465.6,85.9 466.2,87.0 466.8,87.9 467.4,88.5 468.0,89.0 468.6,89.2 469.2,89.3 469.8,89.2 470.4,89.1 471.0,88.8 471.6,88.5 472.2,88.2 472.8,87.9 473.4,87.7 474.0,87.5 474.6,87.5 475.2,87.5 475.8,87.6 476.4,87.8 477.0,88.1 477.6,88.4 478.2,88.8 478.8,89.1 479.4,89.5 480.0,89.8 480.6,90.0 481.2,90.2 481.8,90.3 482.4,90.4 483.0,90.4 483.6,90.4 484.2,90.4 484.8,90.4 485.4,90.4 486.0,90.4 486.6,90.5 487.2,90.5 487.8,90.7 488.4,90.8 489.0,91.0 489.6,91.1 490.2,91.3 490.8,91.4 491.4,91.4 492.0,91.4 492.6,91.3 493.2,91.1 493.8,90.8 494.4,90.5 495.0,90.1 495.6,89.6 496.2,89.2 496.8,89.1 497.4,89.3 498.0,89.7 498.6,89.4 499.2,86.8 499.8,81.1 500.4,72.0 501.0,59.8 501.6,46.2 502.2,34.1 502.8,27.2 503.4,28.2 504.0,37.2 504.6,51.6 505.2,67.5 505.8,81.7 506.4,92.4 507.0,99.1 507.6,102.2 508.2,102.5 508.8,100.8 509.4,98.3 510.0,95.7 510.6,93.6 511.2,92.0 511.8,90.8 512.4,90.0 513.0,89.4 513.6,88.9 514.2,88.5 514.8,88.3 515.4,88.1 516.0,88.1 516.6,88.1 517.2,88.3 517.8,88.5 518.4,88.7 519.0,89.0 519.6,89.2 520.2,89.5 520.8,89.7 521.4,89.9 522.0,90.0 522.6,90.1 523.2,90.1 523.8,90.1 524.4,90.1 525.0,90.1 525.6,90.1 526.2,90.1 526.8,90.1 527.4,90.2 528.0,90.3 528.6,90.4 529.2,90.6 529.8,90.7 530.4,90.8 531.0,90.8 531.6,90.8 532.2,90.6 532.8,90.4 533.4,90.0 534.0,89.4 534.6,88.7 535.2,87.9 535.8,86.9 536.4,85.9 537.0,84.7 537.6,83.5 538.2,82.3 538.8,81.1 539.4,80.0 540.0,79.0 540.6,78.1 541.2,77.3 541.8,76.6 542.4,76.1 543.0,75.8 543.6,75.5 544.2,75.4 544.8,75.4 545.4,75.4 546.0,75.5 546.6,75.7 547.2,75.8 547.8,75.9 548.4,76.1 549.0,76.2 549.6,76.3 550.2,76.3 550.8,76.4 551.4,76.6 552.0,76.7 552.6,77.0 553.2,77.3 553.8,77.7 554.4,78.2 555.0,78.8 555.6,79.4 556.2,80.2 556.8,81.0 557.4,81.9 558.0,82.8 558.6,83.7 559.2,84.5 559.8,85.4 560.4,86.1 561.0,86.8 561.6,87.4 562.2,87.8 562.8,88.2 563.4,88.6 564.0,88.8 564.6,89.0 565.2,89.2 565.8,89.3 566.4,89.5 567.0,89.6 567.6,89.8 568.2,90.1 568.8,90.3 569.4,90.6 570.0,90.9 570.6,91.3 571.2,91.5 571.8,91.7 572.4,91.9 573.0,91.9 573.6,91.9 574.2,91.8 574.8,91.5 575.4,91.1 576.0,90.7 576.6,90.2 577.2,89.6 577.8,89.0 578.4,88.5 579.0,88.0 579.6,87.6 580.2,87.3 580.8,87.1 581.4,87.1 582.0,87.2 582.6,87.5 583.2,87.9 583.8,88.4 584.4,89.0 585.0,89.6 585.6,90.3 586.2,90.9 586.8,91.5 587.4,92.0 588.0,92.4 588.6,92.6 589.2,92.7 589.8,92.7 590.4,92.5 591.0,92.2 591.6,91.9 592.2,91.4 592.8,90.9 593.4,90.4 594.0,90.0 594.6,89.5 595.2,89.2 595.8,88.9 596.4,88.7 597.0,88.6 597.6,88.6 598.2,88.6 598.8,88.7 599.4,88.9 600.0,89.0 600.6,89.2 601.2,89.4 601.8,89.6 602.4,90.0 603.0,90.8 603.6,91.6 604.2,91.4 604.8,88.9 605.4,83.0 606.0,73.6 606.6,61.1 607.2,47.2 607.8,34.8 608.4,27.9 609.0,29.0 609.6,38.0 610.2,52.2 610.8,67.9 611.4,81.7 612.0,92.1 612.6,98.5 613.2,101.5 613.8,101.7 614.4,100.1 615.0,97.7 615.6,95.3 616.2,93.2 616.8,91.7 617.4,90.6 618.0,89.8 618.6,89.1 619.2,88.5 619.8,87.9 620.4,87.5 621.0,87.2 621.6,87.0 622.2,87.0 622.8,87.2 623.4,87.5 624.0,87.9 624.6,88.4 625.2,89.0 625.8,89.6 626.4,90.3 627.0,90.9 627.6,91.4 628.2,91.9 628.8,92.3 629.4,92.5 630.0,92.5 630.6,92.5 631.2,92.3 631.8,92.0 632.4,91.6 633.0,91.2 633.6,90.7 634.2,90.2 634.8,89.7 635.4,89.2 636.0,88.8 636.6,88.4 637.2,88.1 637.8,87.8 638.4,87.6 639.0,87.3 639.6,87.1 640.2,86.8 640.8,86.5 641.4,86.1 642.0,85.6 642.6,85.0 643.2,84.4 643.8,83.6 644.4,82.8 645.0,81.9 645.6,81.0 646.2,80.1 646.8,79.2 647.4,78.4 648.0,77.6 648.6,76.9 649.2,76.3 649.8,75.8 650.4,75.5 651.0,75.3 651.6,75.2 652.2,75.2 652.8,75.2 653.4,75.4 654.0,75.5 654.6,75.7 655.2,76.0 655.8,76.3 656.4,77.0 657.0,78.0 657.6,78.8 658.2,78.2 658.8,74.9 659.4,68.1 660.0,57.8 660.6,45.0 661.2,31.6 661.8,21.0 662.4,17.0 663.0,21.4 663.6,33.2 664.2,49.0 664.8,65.1 665.4,78.7 666.0,88.6 666.6,94.8 667.2,97.7 667.8,98.1 668.4,97.1 669.0,95.6 669.6,94.1 670.2,93.1 670.8,92.5 671.4,92.1 672.0,91.9 672.6,91.6 673.2,91.4 673.8,91.0 674.4,90.7 675.0,90.3 675.6,90.0 676.2,89.8 676.8,89.5 677.4,89.3 678.0,89.2 678.6,89.2 679.2,89.2 679.8,89.2 680.4,89.2 681.0,89.3 681.6,89.4 682.2,89.4 682.8,89.4 683.4,89.4 684.0,89.3 684.6,89.2 685.2,89.1 685.8,89.0 686.4,88.9 687.0,88.8 687.6,88.7 688.2,88.7 688.8,88.8 689.4,88.9 690.0,89.1 690.6,89.3 691.2,89.5 691.8,89.7 692.4,89.9 693.0,90.0 693.6,90.0 694.2,89.9 694.8,89.6 695.4,89.1 696.0,88.5 696.6,87.6 697.2,86.6 697.8,85.4 698.4,84.1 699.0,82.6 699.6,81.1 700.2,79.6 700.8,78.1 701.4,76.7 702.0,75.4 702.6,74.2 703.2,73.3 703.8,72.5 704.4,72.0 705.0,71.8 705.6,71.7 706.2,71.9 706.8,72.3 707.4,72.8 708.0,73.5 708.6,74.2 709.2,75.0 709.8,75.9 710.4,76.7 711.0,77.5 711.6,78.3 712.2,79.0 712.8,79.7 713.4,80.4 714.0,81.0 714.6,81.5 715.2,82.1 715.8,82.6 716.4,83.2 717.0,83.7 717.6,84.3 718.2,84.8 718.8,85.4 719.4,85.9 720.0,86.5 720.6,86.9 721.2,87.4 721.8,87.8 722.4,88.1 723.0,88.3 723.6,88.5 724.2,88.6 724.8,88.6 725.4,88.6 726.0,88.6 726.6,88.5 727.2,88.5 727.8,88.5 728.4,88.5 729.0,88.7 729.6,88.9 730.2,89.2 730.8,89.6 731.4,90.3 732.0,91.4 732.6,92.7 733.2,93.4 733.8,92.0 734.4,87.3 735.0,79.0 735.6,67.3 736.2,53.5 736.8,40.2 737.4,31.3 738.0,29.8 738.6,36.4 739.2,48.8 739.8,63.5 740.4,77.0 741.0,87.3 741.6,93.8 742.2,96.9 742.8,97.2 743.4,95.6 744.0,93.4 744.6,91.2 745.2,89.5 745.8,88.7 746.4,88.4 747.0,88.6 747.6,89.1 748.2,89.6 748.8,90.2 749.4,90.7 750.0,91.2 750.6,91.5 751.2,91.8 751.8,92.0 752.4,92.0 753.0,91.9 753.6,91.8 754.2,91.6 754.8,91.3 755.4,91.0 756.0,90.8 756.6,90.5 757.2,90.2 757.8,90.0 758.4,89.9 759.0,89.8 759.6,89.7 760.2,89.7 760.8,89.7 761.4,89.7 762.0,89.6 762.6,89.6 763.2,89.4 763.8,89.3 764.4,89.1 765.0,88.8 765.6,88.5 766.2,88.1 766.8,87.7 767.4,87.3 768.0,86.9 768.6,86.6 769.2,86.2 769.8,85.9 770.4,85.6 771.0,85.4 771.6,85.2 772.2,85.0 772.8,84.8 773.4,84.6 774.0,84.3 774.6,83.9 775.2,83.4 775.8,82.8 776.4,82.1 777.0,81.2 777.6,80.2 778.2,79.1 778.8,78.0 779.4,76.8 780.0,75.6 780.6,74.4 781.2,73.5 781.8,73.0 782.4,73.0 783.0,73.2 783.6,72.4 784.2,69.2 784.8,62.8 785.4,53.1 786.0,40.9 786.6,27.9 787.2,17.4 787.8,13.1 788.4,17.2 789.0,28.8 789.6,44.7 790.2,61.3 790.8,75.5 791.4,85.9 792.0,92.4 792.6,95.5 793.2,95.9 793.8,94.8 794.4,93.0 795.0,91.3 795.6,90.1 796.2,89.4 796.8,89.1 797.4,89.0 798.0,89.1 798.6,89.1 799.2,89.3 799.8,89.4 800.4,89.5 801.0,89.6 801.6,89.7 802.2,89.8 802.8,89.8 803.4,89.8 804.0,89.7 804.6,89.6 805.2,89.4 805.8,89.3 806.4,89.0 807.0,88.8 807.6,88.5 808.2,88.3 808.8,88.2 809.4,88.1 810.0,88.1 810.6,88.2 811.2,88.5 811.8,88.8 812.4,89.2 813.0,89.6 813.6,90.1 814.2,90.6 814.8,91.0 815.4,91.4 816.0,91.7 816.6,91.8 817.2,91.8 817.8,91.5 818.4,91.1 819.0,90.5 819.6,89.7 820.2,88.8 820.8,87.7 821.4,86.4 822.0,85.2 822.6,83.8 823.2,82.5 823.8,81.2 824.4,80.0 825.0,78.9 825.6,77.9 826.2,77.1 826.8,76.3 827.4,75.7 828.0,75.2 828.6,74.9 829.2,74.6 829.8,74.5 830.4,74.4 831.0,74.4 831.6,74.4 832.2,74.5 832.8,74.6 833.4,74.7 834.0,74.9 834.6,75.2 835.2,75.5 835.8,75.8 836.4,76.3 837.0,76.8 837.6,77.5 838.2,78.2 838.8,78.9 839.4,79.8 840.0,80.6 840.6,81.5 841.2,82.4 841.8,83.3 842.4,84.1 843.0,84.9 843.6,85.7 844.2,86.7 844.8,88.0 845.4,88.9 846.0,88.1 846.6,84.3 847.2,76.9 847.8,66.1 848.4,52.6 849.0,38.8 849.6,28.3 850.2,24.5 850.8,29.2 851.4,40.8 852.0,56.2 852.6,71.5 853.2,84.2 853.8,93.1 854.4,98.4 855.0,100.6 855.6,100.5 856.2,99.1 856.8,97.3 857.4,95.6 858.0,94.4 858.6,93.6 859.2,93.1 859.8,92.6 860.4,92.2 861.0,91.6 861.6,91.0 862.2,90.4 862.8,89.7 863.4,89.1 864.0,88.5 864.6,88.1 865.2,87.7 865.8,87.5 866.4,87.4 867.0,87.4 867.6,87.6 868.2,87.9 868.8,88.2 869.4,88.6 870.0,89.1 870.6,89.5 871.2,90.0 871.8,90.3 872.4,90.7 873.0,90.9 873.6,91.0 874.2,91.1 874.8,91.1 875.4,91.0 876.0,90.8 876.6,90.6 877.2,90.4 877.8,90.1 878.4,89.9 879.0,89.6 879.6,89.4 880.2,89.1 880.8,88.8 881.4,88.5 882.0,88.2 882.6,87.7 883.2,87.2 883.8,86.6 884.4,85.9 885.0,85.0 885.6,84.0 886.2,83.0 886.8,81.8 887.4,80.6 888.0,79.3 888.6,78.1 889.2,76.8 889.8,75.7 890.4,74.7 891.0,73.9 891.6,73.2 892.2,72.7 892.8,72.5 893.4,72.5 894.0,72.6 894.6,73.0 895.2,73.6 895.8,74.3 896.4,75.0 897.0,75.9 897.6,76.7 898.2,77.6 898.8,78.4 899.4,79.1 900.0,79.8\"/><text class=\"cap\" x=\"4\" y=\"193\">리듬 스트립 · 25 mm/s, 10 mm/mV</text></svg>"
 }
];
