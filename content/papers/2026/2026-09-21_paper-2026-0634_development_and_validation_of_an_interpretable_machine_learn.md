---
id: paper-2026-0634
type: paper
topic: Infectious Disease
source: "PubMed / JMIR medical informatics"
journal: "JMIR medical informatics"
pmid: "42766803"
doi: "10.2196/90285"
authors: ["Sun Jiaxuan", "Wang Jingyuan", "Dong Yuxin", "Liu Jieyu", "Ding Yiyun", "Fan Shilin", "Chen Dongyue", "Shou Songtao"]
url: "https://pubmed.ncbi.nlm.nih.gov/42766803/"
pubdate: "2026-09-21"
confidence: medium
date: 2026-09-21
tags: [scraped, pubmed]
related: []
---

## Title
Development and Validation of an Interpretable Machine Learning Model to Predict Mortality in Patients With Sepsis-Induced Coagulopathy: Multicenter Cohort Study

## Authors
Sun Jiaxuan, Wang Jingyuan, Dong Yuxin, Liu Jieyu, Ding Yiyun, Fan Shilin, Chen Dongyue, Shou Songtao

## Journal / DOI
JMIR medical informatics · DOI: 10.2196/90285 · PMID: 42766803
https://pubmed.ncbi.nlm.nih.gov/42766803/

## Abstract
**BACKGROUND:** Sepsis-induced coagulopathy (SIC) is a common and severe complication in patients with sepsis, characterized by microvascular thrombosis, systemic endothelial damage, and markedly increased short-term mortality. Existing traditional clinical risk scoring systems demonstrate limited accuracy and fail to capture complex, nonlinear physiological interactions, underscoring the urgent need for advanced prognostic tools.

**OBJECTIVE:** The objective of this study was to develop and validate an interpretable machine learning (ML) model using large-scale, multicenter databases to predict early mortality in intensive care unit (ICU) patients with SIC and to evaluate its predictive performance and clinical utility compared with traditional clinical risk scores.

**METHODS:** The study retrospectively analyzed clinical data of patients with SIC from the Medical Information Mart for Intensive Care IV (MIMIC-IV), the eICU Collaborative Research Database (eICU-CRD), and Tianjin Medical University General Hospital. Feature selection was performed using LASSO (least absolute shrinkage and selection operator) regression, the Boruta algorithm, and recursive feature elimination with cross-validation, combined with multivariable logistic regression. Twelve ML algorithms were trained and compared with 4 traditional clinical scoring systems (Sequential Organ Failure Assessment, Acute Physiology and Chronic Health Evaluation II, Simplified Acute Physiology Score II, and Oxford Acute Severity of Illness Score) to predict 28-day mortality after ICU admission. Model discrimination, calibration, and clinical utility were assessed using the area under the curve (AUC), calibration curves, and decision curve analysis. Furthermore, Shapley additive explanations (SHAP) values were used to ensure model interpretability and to identify individual pathophysiological drivers.

**RESULTS:** A total of 7980 (66.3%) patients with SIC from the MIMIC-IV database, 3815 (31.7%) from the eICU-CRD database, and 235 (2.0%) from Tianjin Medical University General Hospital were included in the study. Ten independent predictors were identified to construct the model. The XGBoost (extreme gradient boosting) model performed the best, with an AUC of 0.899 (95% CI 0.889-0.909) in the internal validation set and 0.882 and 0.904 in the 2 external validation sets, significantly outperforming traditional scoring systems and demonstrating higher clinical net benefit. SHAP analysis identified that the top 5 critical features were anion gap, red blood cell distribution width, lactate, total bilirubin, and age. Furthermore, an easy-to-use online tool, SIC Predict Streamlit, was developed based on this model to enable clinicians to quickly assess patient risk.

**CONCLUSIONS:** The ML model developed in this study demonstrated superior accuracy, robustness, and generalizability in predicting early mortality in patients with SIC. The model outperformed traditional clinical scoring tools, and the findings provide valuable insights for prognostic assessment and the individualized management of patients with SIC.

## Summary
<!-- TODO: /gen-paper 로 핵심을 자기 언어로 요약 -->

## Clinical Impact
<!-- TODO: 이 연구가 왜 practice-changing인가 -->

## Guideline 변화
<!-- TODO: 이전 가이드라인과 무엇이 달라졌나 -->

## My Ideas
<!-- TODO: 후속 아이디어/연구 메모 -->
