---
id: paper-2026-0063
type: paper
topic: Pathology
source: "PubMed / Frontiers in oncology"
journal: "Frontiers in oncology"
pmid: "42434758"
doi: "10.3389/fonc.2026.1808098"
authors: ["Al-Mohtaseb Alia", "Alotaibi Fahad T", "Alhatamleh Salem", "Malkawi Hatem", "Alishwait Amal", "Aljehani Ala Meshal", "Madain Rola", "Amin Mohammad"]
url: "https://pubmed.ncbi.nlm.nih.gov/42434758/"
pubdate: "2026"
confidence: medium
date: 2026-07-11
tags: [scraped, pubmed]
related: []
---

## Title
An interpretable deep learning framework for intestinal metaplasia detection in gastric histopathology images

## Authors
Al-Mohtaseb Alia, Alotaibi Fahad T, Alhatamleh Salem, Malkawi Hatem, Alishwait Amal, Aljehani Ala Meshal, Madain Rola, Amin Mohammad

## Journal / DOI
Frontiers in oncology · DOI: 10.3389/fonc.2026.1808098 · PMID: 42434758
https://pubmed.ncbi.nlm.nih.gov/42434758/

## Abstract
**BACKGROUND:** Intestinal metaplasia (IM) is a precancerous gastric lesion that commonly develops in the setting of chronic gastric inflammation and represents a key step in gastric carcinogenesis. Delayed or inaccurate identification of IM may delay appropriate surveillance and clinical management, potentially increasing the risk of progression to gastric cancer.

**METHODS:** In this study, we propose a deep learning-based framework, termed CNXTGeM, for the automated detection of intestinal metaplasia in hematoxylin and eosin (H&E)-stained gastric histopathology images. The model integrates a ConvNeXt-Tiny backbone with Generalized Mean (GeM) pooling and Efficient Channel Attention (ECA) to enhance feature representation and discrimination of histopathological patterns associated with intestinal metaplasia. The framework was evaluated using 1,037 H&E-stained gastric biopsy samples (516 IM and 521 controls) obtained from Elazığ Fethi Sekin City Hospital, with an 80/10/10 stratified patient-level train/validation/test split to prevent data leakage. External validation was further performed using the publicly available GasHisSDB dataset (33,284 image patches). Model interpretability was assessed using three complementary gradient-based visualization techniques: Grad-CAM, Grad-CAM++, and XGrad-CAM.

**RESULTS:** CNXTGeM outperformed the evaluated baseline deep learning models, including VGG16, VGG19, DenseNet121, and MobileNetV2, achieving an accuracy of 99.04%, precision of 98.08%, specificity of 98.11%, and an F1-score of 99.03%. Notably, the proposed framework achieved 100% sensitivity, representing an 8.51% improvement in recall over the baseline ConvNeXt model, which may help reduce missed IM cases in computer-assisted histopathological assessment. On the external GasHisSDB dataset, CNXTGeM maintained robust performance (accuracy = 99.34%, F1-score = 99.31%), suggesting good generalization to an independent external dataset. Gradient-based visualization analyses (Grad-CAM, Grad-CAM++, and XGrad-CAM) indicated that the model consistently focused on histopathological regions relevant to inflammation-related mucosal alterations.

**CONCLUSION:** The proposed CNXTGeM framework demonstrates the potential to provide a reliable, efficient, and interpretable artificial intelligence-based approach for computer-assisted detection of intestinal metaplasia. By accurately identifying inflammation-associated histopathological features, the model supports computer-assisted histopathological assessment, reduces inter-observer variability, and may facilitate digital pathology workflows for the assessment of intestinal metaplasia.

## Summary
<!-- TODO: /gen-paper 로 핵심을 자기 언어로 요약 -->

## Clinical Impact
<!-- TODO: 이 연구가 왜 practice-changing인가 -->

## Guideline 변화
<!-- TODO: 이전 가이드라인과 무엇이 달라졌나 -->

## My Ideas
<!-- TODO: 후속 아이디어/연구 메모 -->
