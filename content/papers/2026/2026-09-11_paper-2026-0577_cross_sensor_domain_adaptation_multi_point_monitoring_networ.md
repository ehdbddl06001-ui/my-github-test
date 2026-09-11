---
id: paper-2026-0577
type: paper
topic: Laboratory Medicine
source: "PubMed / PloS one"
journal: "PloS one"
pmid: "42726803"
doi: "10.1371/journal.pone.0358240"
authors: ["Zhou Zhijie", "Lu Jiao", "Ren Yu", "Li Songbin"]
url: "https://pubmed.ncbi.nlm.nih.gov/42726803/"
pubdate: "2026"
confidence: medium
date: 2026-09-11
tags: [scraped, pubmed]
related: []
---

## Title
Cross-sensor domain adaptation multi-point monitoring network for mechanical fault diagnosis

## Authors
Zhou Zhijie, Lu Jiao, Ren Yu, Li Songbin

## Journal / DOI
PloS one · DOI: 10.1371/journal.pone.0358240 · PMID: 42726803
https://pubmed.ncbi.nlm.nih.gov/42726803/

## Abstract
In recent years, mechanical fault diagnosis systems based on multi-point sensor data fusion have achieved remarkable advancements. However, they still face several critical challenges: substantial data distribution discrepancies across monitoring points, scarcity of labeled fault samples at newly deployed points, and prohibitive costs of training independent models for each sensor. We propose UCTL, an end-to-end unsupervised cross-sensor transfer learning network that enables the transfer and reuse of fault features from labeled source monitoring points to unlabeled target monitoring points with disparate data distributions, thereby achieving cross-sensor domain adaptation in multi-point monitoring systems. UCTL mainly consists of two major components. First, a one-dimensional (1D) Swin Transformer backbone is developed by modifying the original Swin Transformer. It directly accepts 1D vibration inputs without time-frequency map conversion and efficiently extracts multi-scale and temporally correlated features via shifted-window self-attention. Second, we propose a joint distribution alignment method that extends both Maximum Mean Square Discrepancy (MMSD) and Variance Discrepancy Representation (VDR) to their joint forms (Joint MMSD and Joint VDR). A weighted formulation independently controls the alignment strength of the mean-squared and variance-based distribution discrepancies, improving adaptability across diverse cross-sensor scenarios while mitigating class-mismatch risk. Experiments on six cross-sensor transfer tasks across the CWRU bearing dataset and XJTU Spurgear dataset demonstrate that the proposed method achieves an average diagnostic accuracy exceeding 99%. In addition, initialized with pre-trained parameters from a certain monitoring point, UCTL can significantly reduce the number of training epochs and improve the deployment efficiency of the model. Ablation studies further confirm the superiority of the 1D Swin Transformer backbone and the synergistic effect of the hybrid loss, validating the effectiveness of the proposed approach as a robust cross-sensor domain adaptation approach.

## Summary
<!-- TODO: /gen-paper 로 핵심을 자기 언어로 요약 -->

## Clinical Impact
<!-- TODO: 이 연구가 왜 practice-changing인가 -->

## Guideline 변화
<!-- TODO: 이전 가이드라인과 무엇이 달라졌나 -->

## My Ideas
<!-- TODO: 후속 아이디어/연구 메모 -->
