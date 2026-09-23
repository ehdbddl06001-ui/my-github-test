---
id: paper-2026-0651
type: paper
topic: Surgery
source: "PubMed / JMIR medical informatics"
journal: "JMIR medical informatics"
pmid: "42777233"
doi: "10.2196/82145"
authors: ["Lee Chaewoo", "Park Seoyoung", "Hwang Jiyoung", "Woo Selin", "Park Youn Chan", "Seo Jae Won", "Lee Sun Ho", "Ahn Jae Hyun", "et al."]
url: "https://pubmed.ncbi.nlm.nih.gov/42777233/"
pubdate: "2026-09-23"
confidence: medium
date: 2026-09-23
tags: [scraped, pubmed]
related: []
---

## Title
Multioutput Machine Learning Model for Predicting Postoperative Outcomes After Liposuction: Algorithm Development and Validation Study in a Multicenter Cohort

## Authors
Lee Chaewoo, Park Seoyoung, Hwang Jiyoung, Woo Selin, Park Youn Chan, Seo Jae Won, Lee Sun Ho, Ahn Jae Hyun, et al.

## Journal / DOI
JMIR medical informatics · DOI: 10.2196/82145 · PMID: 42777233
https://pubmed.ncbi.nlm.nih.gov/42777233/

## Abstract
**BACKGROUND:** Liposuction is widely performed to remove localized fat deposits and improve body contour, yet individualized prediction of postoperative outcomes remains challenging. Existing machine learning (ML) studies have largely focused on single-outcome prediction, with limited attention to the interdependence between postoperative body weight and circumferential size.

**OBJECTIVE:** This study aimed to develop and validate a chained multioutput ML framework to jointly predict postoperative body weight and circumferential size after liposuction using a large multicenter cohort from the 365mc network.

**METHODS:** We analyzed a multicenter cohort of 7804 individuals who underwent liposuction in 2024 at 20 obesity specialty clinics in the 365mc network across South Korea. Using 15 predictors, we compared 8 individual ML models, an automated ML approach, 2 ensemble approaches, and chained multioutput regression models for predicting postoperative body weight and circumferential size. Models were developed using 5-fold cross-validation and evaluated on an independent test set. Performance was assessed using the coefficient of determination (R2), root mean square error (RMSE), mean absolute error (MAE), and mean absolute percentage error (MAPE), and feature importance was evaluated using Shapley additive explanation (SHAP) values. The selected model was integrated into a web-based clinical decision support system (CDSS).

**RESULTS:** A total of 7804 individuals who underwent liposuction were included; of these, 7612 (97.54%) were female. The chained extra trees regressor model with a weight-to-size prediction order achieved an R2 of 0.98, an RMSE of 2.36, an MAE of 1.24, and a MAPE of 2.19. The SHAP analysis identified preoperative weight as the main predictor of postoperative body weight and preoperative size and liposuction-related factors as key predictors of postoperative circumferential size. The final model was integrated into a web-based CDSS (365mc AI platform).

**CONCLUSIONS:** We developed and validated a chained multioutput regression model to predict postoperative body weight and circumferential size after liposuction. Integrated into a web-based CDSS, the model may support patient-specific preoperative counseling and surgical planning.

## Summary
<!-- TODO: /gen-paper 로 핵심을 자기 언어로 요약 -->

## Clinical Impact
<!-- TODO: 이 연구가 왜 practice-changing인가 -->

## Guideline 변화
<!-- TODO: 이전 가이드라인과 무엇이 달라졌나 -->

## My Ideas
<!-- TODO: 후속 아이디어/연구 메모 -->
