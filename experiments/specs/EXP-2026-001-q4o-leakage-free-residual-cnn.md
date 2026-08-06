---
experiment_id: EXP-2026-001
title: Q4-O — leakage-free residual CNN on top of the morphology baseline
status: completed_no_go
design_owner: codex
implementation_owner: claude
dataset: svdb_data5.npz (MIT-BIH family, 78 records / 184,499 beats, AAMI 3-class)
split: frozen record-grouped 5-fold CV (outer 5, inner 5 for offset cross-fitting)
primary_metric: record_level_k_sweep_achievement_mean
created: 2026-08-06
---

# Hypothesis

Adding a raw-waveform CNN **residual** on top of the frozen morphology offset raises the
record-level k-sweep achievement mean by at least +0.015 over the morphology baseline,
and does so by more than a control whose beat waveforms carry no label information.

Falsified by this run. Measured `C − A = +0.0009` (95% CI −0.0021 … +0.0042).

# Why now

Q4-N reported `boost_fix = 0.8631` against `cpu_comb = 0.8445`, which looked like a large
residual gain. That comparison was contaminated: the boost arm was trained against a
morphology-offset array that was roughly 80% in-sample, and it was scored against a value
computed on the same contaminated array. Q4-O reopens the residual direction **once**, with
the offset cross-fitted, to establish whether any of that apparent gain survives
de-contamination.

This does not reopen a closed direction: the closed list covers SMOTE, FiLM, patient
embedding, metric learning, multi-beat context, 2D-DTW and alarm-rate dials. A cross-fitted
residual on a frozen morphology offset had not been tested leakage-free before.

# Controlled comparison

- **Baseline:** Arm A `morph_baseline` — logistic regression on the 17-column morphology
  feature set, fit on the outer-train split only. Seed-independent by construction.
- **Single changed variable:** Arm C `morph_plus_raw_residual` adds a 2-channel raw-waveform
  CNN residual, weighted by a learned `alpha`, on top of the *same* offset Arm A produces.
  Nothing else differs.
- **Fixed components:** morphology windows, fractions, template bounds, rhythm k and `fs`
  are frozen from Q4-N (`config.json` → `frozen_from_q4n`); feature dims base 9 / morph 17 /
  comb 28; 12 epochs, batch 1024, lr 1e-3, weight decay 1e-4, embed 16, patience 3,
  dev evaluated every 4 epochs.
- **Patient split:** frozen record-grouped 5-fold CV, record == patient, recorded in
  `fold_map.json`. Scorable records require ≥25 S beats and ≥25 N beats → 56 of 78.
- **Seeds:** 20260806, 20260807, 20260808, 20260809, 20260810 (5).
- **Determinism/environment:** `manifest.json` pins the data SHA-256, the git commit,
  package versions (torch 2.11.0+cu128, numpy 2.0.2, sklearn 1.6.1) and the GPU (Tesla T4).

## Arms

| Arm | key | What it is | Role |
|---|---|---|---|
| A | `morph_baseline` | morphology 17-col logistic, outer-train fit only | **baseline** |
| B | `raw_current_cnn` | raw 2-channel CNN, no morphology | reference |
| C | `morph_plus_raw_residual` | A's offset + CNN residual | **hypothesis** |
| D | `shuffled_waveform_control` | C with beat waveforms permuted within record | **negative control** |
| E | `corrected_q4n_diagnostic` | 28-col comb offset, cross-fitted, + residual | diagnostic |
| F | `comb_baseline_diagnostic` | 28-col comb logistic | E's comparator |

Arm D's permutation moved 99.96% of beats and preserves labels, RR, record ids and the
morphology offset — it removes waveform information and nothing else. **Arm E is compared
against F, never against A**: E's offset is the 28-column comb set while A's is the
17-column morph set, so `E − A` mixes a feature change with the residual.

# Inputs and outputs

- GitHub inputs: `mit-bih/q4o_leakage_free_residual.py`,
  `notebooks/quest47_q4o_leakage_free_residual_cnn.ipynb`
- Files allowed to change (this revision):
  - `experiments/specs/EXP-2026-001-q4o-leakage-free-residual-cnn.md`
  - `mit-bih/q4o_leakage_free_residual.py`
  - `mit-bih/test_q4o_leakage_free_residual.py`
  - `notebooks/quest47_q4o_leakage_free_residual_cnn.ipynb`
- Colab notebook: `notebooks/quest47_q4o_leakage_free_residual_cnn.ipynb`
- Drive run directory:
  `MyDrive/MedKOS/ecg-model/runs/20260806T0923_EXP-2026-001_q4o_leakage_free_residual_cnn/`
- Required outputs: `config.json`, `manifest.json`, `result.json`, `fold_map.json`,
  `log.txt`, `figures/`, `predictions.npz`, `arms/<arm>/probs.npy` — all present.

# Evaluation

- **Primary:** `record_level_k_sweep_achievement_mean` — per record, rank that record's
  beats by S-probability and take achievement@k = hits@k / min(k, n_S); average over
  k ∈ {50, 100, 200, 300}, then average over the 56 scorable records.
- **Secondary:** per-record PR-AUC and AUROC; achievement at operating points k ∈ {30, 50}.
- **Patient-level lower-tail analysis:** p10, median, worst record per arm.
- **Bootstrap:** 2000 draws, record-level and hierarchical (record × seed).
- **Threshold selection:** none — the metric is a ranking metric at a fixed alarm budget.
- **Leakage checks:** morphology offset cross-fitted with 5 inner folds inside each outer
  train split; an invariant assertion that Arm A test scores equal the Arm C/D outer-test
  offsets; a porting-fidelity check re-scoring Arm A features under Q4-N's LORO
  (measured 0.83608 vs Q4-N 0.8361, within the 0.005 tolerance).

# Acceptance and stopping criteria

Gate thresholds: `min_gain = 0.015`, `min_seed_agreement = 4`, `lower_tail_max_drop = 0.01`.

| # | Gate | Result | Evidence |
|---|---|---|---|
| 1 | mean gain ≥ +0.015 | **FAIL** | `C − A = +0.0009` |
| 2 | CI lower bound > 0 | **FAIL** | CI low `−0.0021` |
| 3 | beats the shuffle control | **FAIL** | `C − D = +0.0013`, CI `−0.0016 … +0.0046` |
| 4 | seed direction stable | PASS | 4/5 seeds positive |
| 5 | lower tail not worse | PASS | p10 0.5577 → 0.5764 |
| 6 | leakage and reproducibility | PASS | cross-fitting, invariant, port check |

- **Success:** all six gates pass.
- **No-go:** any of gates 1–3 fails. → **verdict NO-GO.**
- **Minimum effect worth interpreting:** +0.015. With 56 records the record bootstrap has
  no power to resolve anything smaller, so a sub-gate positive mean is not evidence.

Recorded next step: *"Keep the morphology baseline. Return to failure-record and lower-tail
analysis. Do NOT build a Transformer or a larger fusion model."*

# Results as measured

Seed-averaged k-sweep achievement mean:

| Arm | value | Δ vs A | p10 | worst (record) | seed SD |
|---|---|---|---|---|---|
| A `morph_baseline` | 0.8310 | — | 0.5577 | 0.3798 (#61) | 0.00000 |
| B `raw_current_cnn` | 0.2437 | −0.5873 | 0.0446 | 0.0063 (#34) | 0.01701 |
| C `morph_plus_raw_residual` | 0.8318 | +0.0009 | 0.5764 | 0.3963 (#61) | 0.00096 |
| D `shuffled_waveform_control` | 0.8305 | −0.0004 | 0.5578 | 0.3806 (#61) | 0.00089 |
| E `corrected_q4n_diagnostic` | 0.8335 | +0.0026 | 0.5429 | 0.3731 (#9) | 0.00355 |
| F `comb_baseline_diagnostic` | 0.8298 | −0.0012 | 0.5313 | 0.3763 (#9) | 0.00000 |

Contrasts (record bootstrap, 2000 draws):

| Contrast | mean | 95% CI | seeds positive |
|---|---|---|---|
| C − A | +0.0009 | −0.0021 … +0.0042 | 4/5 |
| C − D | +0.0013 | −0.0016 … +0.0046 | 4/5 |
| E − cleanComb | +0.0037 | −0.0035 … +0.0118 | 5/5 |
| B − A | −0.5873 | −0.6489 … −0.5251 | 0/5 |
| E − A | +0.0026 | −0.0103 … +0.0148 | 4/5 |
| D − A | −0.0004 | −0.0012 … +0.0004 | 2/5 |

**Training diagnostic.** Arm C reports `best_epoch = 0` in 25 of 25 seed×fold fits: early
stopping selected the pre-training checkpoint every time, so the residual never improved dev
loss. The learned `alpha` also flips sign across folds (≈ ±0.09). Both are consistent with a
residual that carries no usable signal, and both are why `C − A` sits on zero.

**Why Q4-N's 0.8631 is not a baseline.** It was produced against a ~80% in-sample offset
array and scored against `cpu_comb = 0.8445` computed on that same array, so it measures
contamination rather than performance. Q4-N's CPU arms also used LORO while this run uses
record-grouped 5-fold CV, so the absolute values are not on a common scale. The
de-contaminated analogue is `E − cleanComb = +0.0037` (CI −0.0035 … +0.0118). Cite 0.8631
as a contamination example, never as a comparator.

# Implementation checklist

- [x] Read AGENTS.md and CLAUDE.md
- [x] Reproduce baseline (porting-fidelity check vs Q4-N LORO, within tolerance)
- [x] Add tests/assertions
- [x] Preserve split and preprocessing
- [x] Save executed notebook and run bundle
- [x] Ingest measured result
- [x] Open PR with exact commands and deviations

# Decision log

**2026-08-06 — design (codex).** Reopen the residual direction exactly once, with the
morphology offset cross-fitted, and put a within-record waveform permutation arm (D) in the
gate so that "C beats A" cannot pass on anything other than waveform information.

**2026-08-06 — execution.** Run written to
`MyDrive/MedKOS/ecg-model/runs/20260806T0923_EXP-2026-001_q4o_leakage_free_residual_cnn/`.
Verdict NO-GO on gates 1, 2 and 3. Gate 3 is the decisive one: Arm C is not distinguishable
from the shuffled-waveform control.

**2026-08-06 — presentation-only revision (claude).**
This revision adds a result-reporting layer and **changes no scientific result.**
Specifically unchanged: the existing predictions and `arms/<arm>/probs.npy`; the arm
definitions A–F; the folds and the five seeds; the metric; the bootstrap; the gates and the
NO-GO verdict; and every measured value in `result.json`. No model was trained, re-fit or
re-scored, and no bootstrap was re-drawn.

What it adds:

1. `ANALYZE_EXISTING_RUN` mode in the notebook — given only `OUT_DIR`, it reads
   `result.json`, `manifest.json`, `predictions.npz` and the per-arm `probs.npy` and
   produces the whole report without retraining.
2. A Korean Executive Summary as the first output: verdict, morphology baseline, C−A and
   C−D with 95% CI, gates passed and failed, what the result means, what it does **not**
   prove, and the recommended next action.
3. Tables and figures written to `figures/`: `arm_summary_table.png` + `arm_metrics.csv`,
   `primary_contrasts_zoom.png`, `reference_gap_separate.png`, `achievement_by_k.png`,
   `seed_effects.png`, `fold_training_diagnostics.png`, `patient_delta_waterfall.png` +
   `patient_delta.csv`, `metric_distribution.png`, and `report_summary.md`.
4. `TrainingHistoryRecorder` for **future** runs, plus `learning_curves.png` when a history
   exists.

Decisions taken while implementing, and why:

- **Authority.** Every headline number — arm means, contrasts, confidence intervals, gate
  verdicts — is read verbatim from `result.json`. The reporting layer never recomputes a CI
  and never re-decides a gate.
- **Derived per-record views are gated.** `result.json` stores record-level values only in
  aggregate, so the waterfall and the distribution plot recompute them from `probs.npy` +
  the labels in `predictions.npz`. That recomputation is first checked against the stored
  per-seed `ach@k` means; if it does not reproduce them it is discarded and the two figures
  are **skipped with an explicit note** rather than drawn from unverified numbers.
- **The waterfall averages all five seeds**, not one, and its record mean therefore equals
  the run's own `C − A` point estimate. A test asserts that identity.
- **`contrasts.png` axis defect.** The existing figure plots `B − A ≈ −0.587` on the same
  axis as the primary contrasts (≈ +0.001), which flattens them to a point. The fix is a
  split: `primary_contrasts_zoom.png` carries only C−A, C−D and E−cleanComb with the zero
  line, the +0.015 gate and a PASS/FAIL label per point; `reference_gap_separate.png`
  carries B−A on its own axis. The original `contrasts.png` is **not overwritten** — it is a
  measured artifact of the run, and overwriting it would violate the constraint this
  revision is under. `report_summary.md` records that it is superseded.
- **No fabricated training history.** This run has none. The report says so, skips
  `learning_curves.png`, and points at the fold-level `alpha` / `best_epoch` / `dev_loss`
  values that *were* recorded. `TrainingHistoryRecorder` is observational: it holds no
  optimiser state, returns nothing a training loop can consume, and records `None` for
  epochs without a dev evaluation instead of carrying a value forward — so attaching it
  cannot change training arithmetic or checkpoint selection.
- **Figure axis labels are in English** to avoid Colab's missing-CJK-font problem; all
  interpretation, the summary and `report_summary.md` are Korean.
- **Interpretation text is computed from the run**, not hardcoded, so a sentence cannot
  outlive the number it describes. A test tampers with a contrast and asserts the sentence
  changes.

Tests (`python -m pytest mit-bih/test_q4o_leakage_free_residual.py`) cover: the report
reproduces `result.json`; C−A/C−D values and CIs match the source exactly; per-record views
use five seeds rather than one; no training history is invented when none exists; and
`result.json` — with every other measured artifact — has an identical SHA-256 before and
after the report runs. The suite is hermetic against a synthetic bundle whose `result.json`
is generated by an independent implementation of the metric; set
`MEDKOS_Q4O_RUN_DIR=<run dir>` to additionally check the real Drive run.

Exact commands:

```bash
python -m pytest mit-bih/test_q4o_leakage_free_residual.py -v
python mit-bih/q4o_leakage_free_residual.py --out-dir \
  /content/drive/MyDrive/MedKOS/ecg-model/runs/20260806T0923_EXP-2026-001_q4o_leakage_free_residual_cnn
```

The CLI exits non-zero if any measured artifact's checksum changed.
