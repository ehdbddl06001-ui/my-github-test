---
id: paper-2026-0495
type: paper
topic: Pathology
source: "PubMed / IEEE journal of biomedical and health informatics"
journal: "IEEE journal of biomedical and health informatics"
pmid: "42647704"
doi: "10.1109/JBHI.2026.3727613"
authors: ["Shu Chang", "Tang Qiling", "Yue Jianchi", "Chen Pengzhou", "Liu Rong", "Wang Shuai"]
url: "https://pubmed.ncbi.nlm.nih.gov/42647704/"
pubdate: "2026-08-26"
confidence: medium
date: 2026-08-26
tags: [scraped, pubmed]
related: []
---

## Title
Dirichlet Process-Guided Dynamic Filtering for Mitosis Detection with Single Point Supervision

## Authors
Shu Chang, Tang Qiling, Yue Jianchi, Chen Pengzhou, Liu Rong, Wang Shuai

## Journal / DOI
IEEE journal of biomedical and health informatics · DOI: 10.1109/JBHI.2026.3727613 · PMID: 42647704
https://pubmed.ncbi.nlm.nih.gov/42647704/

## Abstract
Accurate detection of mitotic figures in breast histopathology images is central to tumor grading and prognostic assessment. Precise bounding-box annotation remains labor-intensive and variable because mitotic figures are small, morphologically diverse, and boundary-ambiguous. Point-level supervision reduces annotation cost but lacks scale information, making reliable pseudo-box generation essential. Existing point-supervised pipelines often use static or heuristic thresholds that may become unstable as teacher predictions and proposal-score distributions evolve. We propose DDFMitos-Net, a point-supervised teacher-student framework for distribution-aware proposal filtering. The framework learns initial scale priors from point-guided simulated masks, refines teacher-generated pseudo-boxes through Adaptive Multiple Instance Learning, and uses Distribution-based Dynamic Filtering to integrate classification confidence with point-centered spatial information. Adaptive thresholds are estimated with a truncated Dirichlet Process Mixture Model. Transformation-Scale Learning improves geometric consistency, and Center-Aware Domain Adaptation provides auxiliary scanner-aware feature alignment. On MITOS12, MITOS14, TUPAC16, and MIDOG21, DDFMitos-Net achieved repeated-run F1 scores of 0.837 ± 0.004, 0.716 ± 0.006, 0.785 ± 0.005, and 0.806 ± 0.004, respectively. These results indicate stable and competitive point-supervised mitosis detection using low-cost point-level annotations.

## Summary
<!-- TODO: /gen-paper 로 핵심을 자기 언어로 요약 -->

## Clinical Impact
<!-- TODO: 이 연구가 왜 practice-changing인가 -->

## Guideline 변화
<!-- TODO: 이전 가이드라인과 무엇이 달라졌나 -->

## My Ideas
<!-- TODO: 후속 아이디어/연구 메모 -->
