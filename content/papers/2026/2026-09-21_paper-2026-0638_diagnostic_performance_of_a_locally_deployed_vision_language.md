---
id: paper-2026-0638
type: paper
topic: Laboratory Medicine
source: "PubMed / JMIR AI"
journal: "JMIR AI"
pmid: "42766848"
doi: "10.2196/99757"
authors: ["Shi Yin", "Tong Zhi-Chao"]
url: "https://pubmed.ncbi.nlm.nih.gov/42766848/"
pubdate: "2026-09-21"
confidence: medium
date: 2026-09-21
tags: [scraped, pubmed]
related: []
---

## Title
Diagnostic Performance of a Locally Deployed Vision Language Model for Bone Tumor Diagnosis Using Smartphone-Captured Images: Exploratory Retrospective Study

## Authors
Shi Yin, Tong Zhi-Chao

## Journal / DOI
JMIR AI · DOI: 10.2196/99757 · PMID: 42766848
https://pubmed.ncbi.nlm.nih.gov/42766848/

## Abstract
**BACKGROUND:** Vision language models (VLMs) show promise in medical imaging, yet their performance on high-noise smartphone-captured images-common in primary care referrals-remains untested. Furthermore, it remains controversial whether retrieval-augmented generation (RAG) using external expert guidelines actually improves diagnostic accuracy for rare bone tumors.

**OBJECTIVE:** This study aims to evaluate the diagnostic efficacy of a locally deployed, open-source VLM (Qwen3-VL) on high-noise bone tumor images. Specifically, we investigated how clinical persona prompts and RAG integration were associated with diagnostic performance and observed error patterns during multimodal reasoning.

**METHODS:** This retrospective study included 42 patients with biopsy-proven primary bone tumors and tumor-like lesions. To simulate real-world conditions, we captured the original DICOM (Digital Imaging and Communications in Medicine) images from a monitor using a handheld smartphone without stabilization, organically capturing ambient glare and Moiré patterns typical of real-world teleconsultations. Using a 2×2 factorial design, we compared the diagnostic performance of the base model versus the RAG-integrated model under 2 distinct system personas: "radiologist" and "orthopedic oncologist." Primary outcomes were top-1 and top-3 diagnostic accuracy. We used the McNemar test for paired comparisons of diagnostic correctness before and after RAG integration, and conducted an exploratory analysis of AI hallucinations using model-generated reasoning traces.

**RESULTS:** Without RAG, the top-3 accuracy showed no significant difference between the radiologist and orthopedic oncologist personas (15/42, 36% vs 14/42, 33%; P=.76). After RAG integration, top-1 accuracy in the radiologist persona decreased from 12 (29%, 95% CI 16%-45%) to 6 (14%, 95% CI 5%-29%; P=.03). In the orthopedic oncologist persona, no significant change was observed in top-1 or top-3 accuracy (P=.65 and P>.99, respectively). Exploratory review of model-generated reasoning traces identified several text-associated diagnostic error patterns, including demographic anchoring, trauma-related masking, and shifts toward rare diagnoses following RAG retrieval.

**CONCLUSIONS:** In this exploratory study, adding the evaluated RAG configuration did not improve diagnostic accuracy and was associated with text-related diagnostic errors under smartphone-captured degraded imaging conditions. The findings suggest that persona design may influence the robustness of VLM responses to retrieved information, but this observation requires validation in larger, multimodel studies. Future studies should evaluate whether targeted visual fine-tuning on representative real-world degraded medical images can improve robustness under such conditions.

## Summary
<!-- TODO: /gen-paper 로 핵심을 자기 언어로 요약 -->

## Clinical Impact
<!-- TODO: 이 연구가 왜 practice-changing인가 -->

## Guideline 변화
<!-- TODO: 이전 가이드라인과 무엇이 달라졌나 -->

## My Ideas
<!-- TODO: 후속 아이디어/연구 메모 -->
