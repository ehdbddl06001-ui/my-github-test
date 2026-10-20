---
id: paper-2026-0806
type: paper
topic: Infectious Disease
source: "PubMed / Journal of the American Medical Informatics Association : JAMIA"
journal: "Journal of the American Medical Informatics Association : JAMIA"
pmid: "42900705"
doi: "10.1093/jamia/ocag144"
authors: ["Meyer-Eschenbach Falk", "Schmiedler René", "von Stoephasius Johannes", "Zhang Camille", "Kronfli Luis", "Frey Nicolas", "Näher Anatol-Fiete", "Ehret Jacques", "et al."]
url: "https://pubmed.ncbi.nlm.nih.gov/42900705/"
pubdate: "2026-10-20"
confidence: medium
date: 2026-10-20
tags: [scraped, pubmed]
related: []
---

## Title
Variability in automated sepsis case detection: a systematic analysis of implementation methods in clinical data repositories

## Authors
Meyer-Eschenbach Falk, Schmiedler René, von Stoephasius Johannes, Zhang Camille, Kronfli Luis, Frey Nicolas, Näher Anatol-Fiete, Ehret Jacques, et al.

## Journal / DOI
Journal of the American Medical Informatics Association : JAMIA · DOI: 10.1093/jamia/ocag144 · PMID: 42900705
https://pubmed.ncbi.nlm.nih.gov/42900705/

## Abstract
**OBJECTIVE:** To systematically review and characterize methodological heterogeneity in sepsis case detection using the Medical Information Mart for Intensive Care III (MIMIC-III) and eICU-CRD databases.

**MATERIALS AND METHODS:** We conducted a PRISMA-guided systematic review of PubMed and Web of Science (publication years 2016-2024). Studies were eligible if they applied the SOFA-based Sepsis-3 definition to MIMIC-III or eICU-CRD, provided at least one explicit label-calculation detail, reported a traceable detection rate, and met further criteria detailed in the PRISMA flow diagram. We classified each study by study type and unit of analysis (patients, admissions, or ICU stays) and extracted methodological details on sepsis case detection across 6 domains. For studies with available source code, we additionally examined code structure and repository dependencies to identify methodological decisions across these domains.

**RESULTS:** Of 396 publications screened, 64 met inclusion criteria and 12 provided source code. Sepsis detection rates ranged from 3.4% to 65.2% in MIMIC-III and from 9.8% to 47.9% in eICU-CRD. Substantial variability persisted among studies using identical cohort definitions within both databases (MIMIC-III: 16.9%-42.2%; eICU-CRD: 13.9%-31.4%). In a generalized linear mixed model, between-study heterogeneity was extreme (overall τ²≈0.79; 95% prediction interval for a new study's detection rate 5%-63%), and study-level characteristics-including database, study type, infection detection method, code availability, and unit of analysis-explained only a small proportion of this variance (≈9%), with no characteristic reaching statistical significance. The overall proportion of studies reporting methodological details varied by domain: SOFA calculation (53.1%), infection detection methods (42.2%), temporal windows (37.5%), aggregation methods (26.6%), and missing-data handling (17.2%). Source code analysis identified 321 implementation decisions, revealing heterogeneity in baseline SOFA definitions (SOFA = 0 vs dynamic baseline), temporal windows (infection-centered vs ICU-admission-centered) and infection detection methods (antibiotic-culture matching vs APACHE-based diagnosis). Dependencies among several MIMIC-III repositories suggested propagation of implementation decisions across studies.

**DISCUSSION:** Clinically validated sepsis definitions yield substantially different detection rates across studies using identical datasets. Statistical modeling showed that this variability is driven almost entirely by between-study implementation differences rather than sampling error or study characteristics.

**CONCLUSION:** To improve reproducibility in sepsis research and the robustness of sepsis prediction models, we recommend standardized reporting of sepsis case detection methodology and the publication of version-controlled source code.

## Summary
<!-- TODO: /gen-paper 로 핵심을 자기 언어로 요약 -->

## Clinical Impact
<!-- TODO: 이 연구가 왜 practice-changing인가 -->

## Guideline 변화
<!-- TODO: 이전 가이드라인과 무엇이 달라졌나 -->

## My Ideas
<!-- TODO: 후속 아이디어/연구 메모 -->
