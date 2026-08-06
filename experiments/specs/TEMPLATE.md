---
experiment_id: EXP-YYYY-NNN
title: Replace with experiment title
status: draft
design_owner: codex
implementation_owner: claude
dataset: MIT-BIH
split: DS1_to_DS2_inter_patient
primary_metric: S_PR_AUC
created: YYYY-MM-DD
---

# Hypothesis

State one falsifiable claim.

# Why now

Link the latest verified baseline and failure pattern. State whether this reopens a closed direction and why.

# Controlled comparison

- Baseline:
- Single changed variable:
- Fixed components:
- Patient split:
- Seeds:
- Determinism/environment:

# Inputs and outputs

- GitHub inputs:
- Files allowed to change:
- Colab notebook:
- Drive run directory: `MyDrive/MedKOS/ecg-model/runs/<timestamp>_<experiment_id>/`
- Required outputs: `config.json`, `manifest.json`, `result.json`, `log.txt`, figures, saved probabilities.

# Evaluation

- Primary: S-beat PR-AUC
- Secondary:
- Patient-level lower-tail analysis:
- Bootstrap:
- Threshold selection:
- Leakage checks:

# Acceptance and stopping criteria

- Success:
- No-go:
- Terminate early if:
- Minimum effect worth interpreting:

# Implementation checklist

- [ ] Read AGENTS.md and CLAUDE.md
- [ ] Reproduce baseline
- [ ] Add tests/assertions
- [ ] Preserve split and preprocessing
- [ ] Save executed notebook and run bundle
- [ ] Ingest measured result
- [ ] Open PR with exact commands and deviations

# Decision log

Append dated design, implementation, and review decisions here. Never silently change the scientific question.
