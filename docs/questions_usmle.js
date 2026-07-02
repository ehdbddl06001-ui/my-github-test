// 자동 생성 파일 — 수정하지 마세요.
// 원본: content/usmle/*.md  →  `python pipelines/export_usmle_web.py`로 재생성
window.USMLE_QUESTIONS = [
 {
  "id": "usmle-2026-0001",
  "exam": "usmle",
  "step": "Step 1",
  "subject": "Pharmacology",
  "subtopic": "Heart Failure Pharmacology",
  "type": "Heart Failure Pharmacology",
  "difficulty": 5,
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
  "source": "USMLE-style / MedKOS (PARADIGM-HF, 2022 AHA/ACC/HFSA HF guideline)"
 },
 {
  "id": "usmle-2026-0002",
  "exam": "usmle",
  "step": "Step 2",
  "subject": "Internal Medicine",
  "subtopic": "Infective Endocarditis",
  "type": "Infective Endocarditis",
  "difficulty": 5,
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
  "source": "USMLE-style / MedKOS (AHA/IDSA infective endocarditis guideline)"
 },
 {
  "id": "usmle-2026-0003",
  "exam": "usmle",
  "step": "Step 1",
  "subject": "Pharmacology",
  "subtopic": "Acid-Base (Mixed Disorder)",
  "type": "Acid-Base (Mixed Disorder)",
  "difficulty": 5,
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
  "source": "USMLE-style / MedKOS (Winter's formula; salicylate toxicology)"
 },
 {
  "id": "usmle-2026-0004",
  "exam": "usmle",
  "step": "Step 2",
  "subject": "Surgery",
  "subtopic": "Pheochromocytoma",
  "type": "Pheochromocytoma",
  "difficulty": 4,
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
  "source": "USMLE-style / MedKOS (Endocrine Society pheochromocytoma guideline)"
 },
 {
  "id": "usmle-2026-0005",
  "exam": "usmle",
  "step": "Step 2",
  "subject": "Internal Medicine",
  "subtopic": "Heparin-Induced Thrombocytopenia",
  "type": "Heparin-Induced Thrombocytopenia",
  "difficulty": 5,
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
  "source": "USMLE-style / MedKOS (ASH 2018 VTE/HIT guideline)"
 },
 {
  "id": "usmle-2026-0006",
  "exam": "usmle",
  "step": "Step 1",
  "subject": "Immunology",
  "subtopic": "Chronic Granulomatous Disease",
  "type": "Chronic Granulomatous Disease",
  "difficulty": 4,
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
  "source": "USMLE-style / MedKOS (primary immunodeficiency)"
 },
 {
  "id": "usmle-2026-0007",
  "exam": "usmle",
  "step": "Step 2",
  "subject": "Neurology",
  "subtopic": "Lambert-Eaton Myasthenic Syndrome",
  "type": "Lambert-Eaton Myasthenic Syndrome",
  "difficulty": 5,
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
  "source": "USMLE-style / MedKOS (paraneoplastic neurology)"
 },
 {
  "id": "usmle-2026-0008",
  "exam": "usmle",
  "step": "Step 1",
  "subject": "Biochemistry",
  "subtopic": "Urea Cycle (Ornithine Transcarbamylase Deficiency)",
  "type": "Urea Cycle (Ornithine Transcarbamylase Deficiency)",
  "difficulty": 5,
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
  "source": "USMLE-style / MedKOS (inborn errors of metabolism)"
 },
 {
  "id": "usmle-2026-0009",
  "exam": "usmle",
  "step": "Step 1",
  "subject": "Immunology",
  "subtopic": "Terminal Complement Deficiency",
  "type": "Terminal Complement Deficiency",
  "difficulty": 4,
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
  "source": "USMLE-style / MedKOS (complement immunodeficiency)"
 },
 {
  "id": "usmle-2026-0010",
  "exam": "usmle",
  "step": "Step 1",
  "subject": "Biochemistry",
  "subtopic": "Acute Intermittent Porphyria",
  "type": "Acute Intermittent Porphyria",
  "difficulty": 5,
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
  "source": "USMLE-style / MedKOS (heme synthesis, porphyrias)"
 },
 {
  "id": "usmle-2026-0011",
  "exam": "usmle",
  "step": "Step 1",
  "subject": "Microbiology",
  "subtopic": "Vancomycin Resistance (VRE)",
  "type": "Vancomycin Resistance (VRE)",
  "difficulty": 4,
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
  "source": "USMLE-style / MedKOS (antimicrobial resistance)"
 },
 {
  "id": "usmle-2026-0012",
  "exam": "usmle",
  "step": "Step 1",
  "subject": "Microbiology",
  "subtopic": "Exotoxin Mechanism (EF-2 ADP-ribosylation)",
  "type": "Exotoxin Mechanism (EF-2 ADP-ribosylation)",
  "difficulty": 5,
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
  "source": "USMLE-style / MedKOS (bacterial toxins)"
 },
 {
  "id": "usmle-2026-0013",
  "exam": "usmle",
  "step": "Step 2",
  "subject": "Surgery",
  "subtopic": "Acute Mesenteric Ischemia",
  "type": "Acute Mesenteric Ischemia",
  "difficulty": 5,
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
  "source": "USMLE-style / MedKOS (acute abdomen)"
 },
 {
  "id": "usmle-2026-0014",
  "exam": "usmle",
  "step": "Step 2",
  "subject": "Neurology",
  "subtopic": "Acute Ischemic Stroke (Thrombolysis)",
  "type": "Acute Ischemic Stroke (Thrombolysis)",
  "difficulty": 4,
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
  "source": "USMLE-style / MedKOS (AHA/ASA acute stroke guideline)"
 },
 {
  "id": "usmle-2026-0015",
  "exam": "usmle",
  "step": "Step 2",
  "subject": "Pediatrics",
  "subtopic": "Ductal-Dependent Cyanotic CHD",
  "type": "Ductal-Dependent Cyanotic CHD",
  "difficulty": 4,
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
  "source": "USMLE-style / MedKOS (neonatal cardiology)"
 },
 {
  "id": "usmle-2026-0016",
  "exam": "usmle",
  "step": "Step 2",
  "subject": "Pediatrics",
  "subtopic": "Hypertrophic Pyloric Stenosis",
  "type": "Hypertrophic Pyloric Stenosis",
  "difficulty": 4,
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
  "source": "USMLE-style / MedKOS (pediatric surgery)"
 }
];
