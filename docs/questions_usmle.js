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
    "v": "(B) 좌각차단(CLBBB)도 넓은 QRS지만 정반대로 I·V6에 넓은 단일 R파, V1에 QS/rS이고 rSR′가 없다 — \"넓은 QRS = LBBB\"로 넘겨짚기 쉬운 함정. (C) WPW는 짧은 PR + 델타파로 넓어진다(형태가 다름). (D) 좌전섬유속차단(LAFB)은 좌축편위를 만들지만 QRS를 넓히지 않는다(이 심전도 질문의 핵심: 폭 확장의 원인이 아님) — 이 기록에 LAFB가 동반돼 있어 특히 매력적인 오답. (E) LVH는 전압 증가가 특징이지 폭 확장의 주원인이 아니다."
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
 }
];
