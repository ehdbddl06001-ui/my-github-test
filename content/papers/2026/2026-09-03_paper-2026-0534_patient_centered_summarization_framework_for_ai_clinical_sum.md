---
id: paper-2026-0534
type: paper
topic: Cardiology
source: "PubMed / Journal of medical Internet research"
journal: "Journal of medical Internet research"
pmid: "42691463"
doi: "10.2196/87061"
authors: ["Lizarazo Jimenez Maria", "Claros Ana Gabriela", "Green Kieran", "Toro-Tobon David", "Larios Felipe", "Asthana Sheena", "Wenczenovicz Camila", "Guevara Maldonado Kerly", "et al."]
url: "https://pubmed.ncbi.nlm.nih.gov/42691463/"
pubdate: "2026-09-03"
confidence: medium
date: 2026-09-03
tags: [scraped, pubmed]
related: []
---

## Title
Patient-Centered Summarization Framework for AI Clinical Summarization: Mixed Methods Study

## Authors
Lizarazo Jimenez Maria, Claros Ana Gabriela, Green Kieran, Toro-Tobon David, Larios Felipe, Asthana Sheena, Wenczenovicz Camila, Guevara Maldonado Kerly, et al.

## Journal / DOI
Journal of medical Internet research · DOI: 10.2196/87061 · PMID: 42691463
https://pubmed.ncbi.nlm.nih.gov/42691463/

## Abstract
**BACKGROUND:** Large language models (LLMs) are increasingly demonstrating the potential to reach human-level performance in generating clinical summaries from patient-clinician conversations. LLMs are usually evaluated against clinical summaries that focus mainly on patients' biology and not on their biography (eg, preferences, values, wishes, and concerns). To achieve patient-centered care, artificial intelligence clinical summarization must incorporate patient-centered domains, implemented through patient-centered summaries (PCSs).

**OBJECTIVE:** This study aimed to develop a framework to generate PCS that capture patients' values, preferences, and wishes while ensuring clinical utility for clinicians, and assess if current open-source LLMs can achieve human-level performance in generating PCS.

**METHODS:** We developed a 4-step mixed methods process to define and evaluate PCS. First, 2 patient and public involvement and engagement groups were convened in the United Kingdom (10 patients and 8 clinicians), who participated in semistructured interviews exploring what personal and contextual information should be included in clinical summaries and how it should be structured for clinical use. Second, findings were translated into an annotation guideline, which was used by 8 clinician annotators to generate gold standard PCS from 88 transcribed patient-clinician consultations about the management of atrial fibrillation. Third, 16 consultations were used to iteratively develop and refine a prompt aligned with the annotation guideline. Finally, 5 LLMs (Llama-3.2-3B [Meta AI], Llama-3.1-8B [Meta AI], Mistral-8B [Mistral AI], Gemma-3-4B [Google DeepMind], and Qwen3-8B [Alibaba]) generated summaries from 72 consultations using zero-shot and few-shot prompting, which were evaluated against gold standard PCS using ROUGE-L (Recall-Oriented Understudy for Gisting Evaluation-Longest Common Subsequence) and BERTScore (Bidirectional Encoder Representations from Transformers Score) and assessed for correctness, completeness, conciseness, patient-centeredness, and fluency.

**RESULTS:** Patients emphasized that summaries should include (1) lifestyle routines and daily functioning as indicators of independence or disruption; (2) the presence and role of social support systems, especially during crises; (3) recent life events or stressors, such as trauma, loss, or caregiving demands; and (4) care preferences, values, and communication styles that provide meaning or reflect autonomy. Clinicians sought summaries that included a concise functional baseline, psychosocial context, and emotional cues, preferably in a structured, clinically digestible format. In the 72 consultations (mean age 70, SD 11 y; 32/72, 44.4% female), the best zero-shot performance was observed with Mistral-8B (ROUGE-L 0.189) and Llama-3.1-8B (BERTScore 0.673). The best few-shot prompting was found with 3 examples using Llama-3.1-8B (ROUGE-L 0.206 and BERTScore 0.683).

**CONCLUSIONS:** The open-source LLMs we evaluated did not achieve human-level performance in generating PCSs. Without task-specific fine-tuning, current open-source LLMs cannot reach human-level performance in this task. Our framework serves as an innovative guideline for developing gold standard PCS for artificial intelligence clinical tasks.

## Summary
<!-- TODO: /gen-paper 로 핵심을 자기 언어로 요약 -->

## Clinical Impact
<!-- TODO: 이 연구가 왜 practice-changing인가 -->

## Guideline 변화
<!-- TODO: 이전 가이드라인과 무엇이 달라졌나 -->

## My Ideas
<!-- TODO: 후속 아이디어/연구 메모 -->
