---
id: paper-2026-0847
type: paper
topic: Hematology-Oncology
source: "PubMed / JMIR medical informatics"
journal: "JMIR medical informatics"
pmid: "42932875"
doi: "10.2196/86639"
authors: ["Wang Lixiuyun", "Tang Yafei", "Ma Jun", "Wang Shuqi", "Yang Guoqiang", "Huang Jin", "Li Qiuhong", "Feng Yonghong"]
url: "https://pubmed.ncbi.nlm.nih.gov/42932875/"
pubdate: "2026-10-26"
confidence: medium
date: 2026-10-26
tags: [scraped, pubmed]
related: []
---

## Title
Differential Diagnosis of Early-Stage Pulmonary Sarcoidosis With Normal Serum Angiotensin-Converting Enzyme Activity Using Peripheral Blood Indicators: Machine Learning Models Development and Validation

## Authors
Wang Lixiuyun, Tang Yafei, Ma Jun, Wang Shuqi, Yang Guoqiang, Huang Jin, Li Qiuhong, Feng Yonghong

## Journal / DOI
JMIR medical informatics · DOI: 10.2196/86639 · PMID: 42932875
https://pubmed.ncbi.nlm.nih.gov/42932875/

## Abstract
**BACKGROUND:** Early-stage pulmonary sarcoidosis with serum angiotensin-converting enzyme (sACE) activity within the normal range is difficult to distinguish from other pulmonary diseases with similar radiographic characteristics.

**OBJECTIVE:** This study aimed to develop and validate machine learning (ML)-based diagnostic models for differentiating early-stage pulmonary sarcoidosis using indices from routine peripheral blood tests.

**METHODS:** From May 2014 to May 2021, a total of 1142 patients with atypical initial pulmonary imaging findings were enrolled. After applying strict inclusion and exclusion criteria, 420 cases were divided into sarcoidosis and nonsarcoidosis groups (including mediastinal lymph node tuberculosis [MLNT], lung cancer, lymphoma, and pneumoconiosis), then stratified by sex and randomly split (7:3) into training and validation sets. Features were selected via univariate analysis (P<.10), the Boruta algorithm, and least absolute shrinkage and selection operator regression. Six ML algorithms-logistic regression (LR), random forest, support vector machine (SVM), extreme gradient boosting, k‑nearest neighbor, and naïve Bayes-were compared using area under the curve (AUC), accuracy, sensitivity, specificity, F1-score, Brier score, calibration assessment, and decision curve analysis. Shapley Additive Explanations was used for interpretability. The selected models were deployed as an interactive Shiny web application.

**RESULTS:** After stratification, the male group comprised 224 cases (sarcoidosis n=42; MLNT: n=39; lung cancer: n=106; lymphoma: n=9; pneumoconiosis: n=28), and the female group comprised 196 cases (sarcoidosis: n=100; MLNT: n=39; lung cancer: n=49; lymphoma: n=4; pneumoconiosis: n=4). Models were selected based on comprehensive evaluation of multiple performance metrics, including AUC, accuracy, specificity, F1-score, and Brier score. The selected model for the male group was SVM, incorporating the following indices: age, lymphocyte count (Lym#), red cell distribution width standard deviation, D-dimer, sACE, cluster of differentiation 4-positive T cells to cluster of differentiation 8-positive T cells ratio (CD4+/CD8+), erythrocyte sedimentation rate, triglyceride to high-density lipoprotein cholesterol ratio (TG/HDLC), basophil count, and total protein. The selected model for the female group was LR, using Lym#, sACE, total cholesterol, TG/HDLC, glucose, CD3+%, and CD8+%. The validation set results showed AUCs of 0.896 (95% CI 0.746-1.000) and 0.762 (95% CI 0.632-0.892), sensitivities of 0.700 (95% CI 0.397-0.892) and 0.679 (95% CI 0.493-0.821), and specificities of 0.942 (95% CI 0.844-0.980) and 0.815 (95% CI 0.633-0.918), respectively.

**CONCLUSIONS:** Based on sex‑stratified strategies, the models demonstrated preliminary discriminative ability for differentiating early‑stage pulmonary sarcoidosis with normal sACE from other pulmonary diseases. However, the wide CIs preclude definitive conclusions about clinical performance, and external validation in larger cohorts is needed.

## Summary
<!-- TODO: /gen-paper 로 핵심을 자기 언어로 요약 -->

## Clinical Impact
<!-- TODO: 이 연구가 왜 practice-changing인가 -->

## Guideline 변화
<!-- TODO: 이전 가이드라인과 무엇이 달라졌나 -->

## My Ideas
<!-- TODO: 후속 아이디어/연구 메모 -->
