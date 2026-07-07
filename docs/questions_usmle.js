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
 }
];
