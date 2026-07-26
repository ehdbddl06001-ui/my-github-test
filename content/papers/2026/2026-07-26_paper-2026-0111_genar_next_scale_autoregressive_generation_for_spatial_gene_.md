---
id: paper-2026-0111
type: paper
topic: Pathology
source: "PubMed / Medical image analysis"
journal: "Medical image analysis"
pmid: "42503259"
doi: "10.1016/j.media.2026.104232"
authors: ["Ouyang Jiarui", "Wang Yihui", "Gao Yihang", "Xu Yingxue", "Yang Shu", "Chen Hao"]
url: "https://pubmed.ncbi.nlm.nih.gov/42503259/"
pubdate: "2026-07-25"
confidence: medium
date: 2026-07-26
tags: [scraped, pubmed]
related: []
---

## Title
GenAR: Next-scale autoregressive generation for spatial gene expression prediction

## Authors
Ouyang Jiarui, Wang Yihui, Gao Yihang, Xu Yingxue, Yang Shu, Chen Hao

## Journal / DOI
Medical image analysis · DOI: 10.1016/j.media.2026.104232 · PMID: 42503259
https://pubmed.ncbi.nlm.nih.gov/42503259/

## Abstract
Spatial Transcriptomics (ST) offers spatially resolved gene expression but remains costly. Predicting expression directly from widely available Hematoxylin and Eosin (H&E) stained images presents a cost-effective alternative. However, most computational approaches (i) predict each gene independently, overlooking co-expression structure, and (ii) cast the task as continuous regression despite expression being discrete counts. This mismatch can yield biologically implausible outputs and complicate downstream analyses. We introduce GenAR, a multi-scale autoregressive framework that refines predictions from coarse to fine. GenAR (a) clusters genes into hierarchical groups to expose cross-gene dependencies, (b) models expression as discrete token generation over a fixed vocabulary of integer count tokens to directly predict raw counts, and (c) conditions decoding on fused histological and spatial embeddings. By modeling expression on the physical count scale, GenAR avoids the limitations of continuous regression, while its coarse-to-fine factorization ensures a principled conditional decomposition. Extensive experimental results on five ST datasets across different tissue types demonstrate that GenAR achieves state-of-the-art performance, offering potential implications for precision medicine and cost-effective molecular profiling. Code is publicly available at https://github.com/oyjr/genar.

## Summary
<!-- TODO: /gen-paper 로 핵심을 자기 언어로 요약 -->

## Clinical Impact
<!-- TODO: 이 연구가 왜 practice-changing인가 -->

## Guideline 변화
<!-- TODO: 이전 가이드라인과 무엇이 달라졌나 -->

## My Ideas
<!-- TODO: 후속 아이디어/연구 메모 -->
