---
experiment_id: EXP-2026-007
title: Q5-D expert-validated P-wave timing association audit
status: approved_for_implementation
design_owner: codex
implementation_owner: claude
dataset: MIT-BIH
split: DS1_to_DS2_inter_patient
primary_metric: S_PR_AUC
created: 2026-08-09
---

# Fixed question

In MIT-BIH DS2 beats whose RR timing is normal-like, is correctly aligned,
independently validated P-to-R timing discordance associated with lower frozen
V10 `pwave` S PR-AUC than an otherwise identical within-record sham alignment?

This is the only scientific question in EXP-2026-007.  The only manipulated
variable is `P_ALIGNMENT`:

- `TRUE`: the detected P-wave timing scalar stays attached to its own beat.
- `SHAM`: the same scalar is permuted within record and within the frozen RR bin,
  preserving record, RR distribution, missingness, class prevalence, model
  probabilities, and sample count.

No ECG sample, label, split, model probability, or model parameter is changed.
The permitted language is **failure-associated P-wave timing**.  This experiment
cannot establish a physiological cause or a model mechanism because it does not
intervene on model input.

# Hypothesis

After a frozen P-wave delineation rule passes an independent expert-annotation
qualification gate, the difference in frozen V10 `pwave` S PR-AUC between
P-timing-concordant and P-timing-discordant normal-like-RR beats will exceed the
same difference under `SHAM` alignment by at least 0.015, with a record-clustered
95% confidence interval above zero.

The null is not merely `effect = 0`.  It is the empirical distribution generated
by rerunning the complete selection-and-scoring procedure after `P_ALIGNMENT`
is broken under the same eligibility and matching rules.

# Why now

- Q5-A found no qualified patient, quality, RR, or fixed-window atrial-proxy
  block.  The existing `B_ATRIAL` proxies were weak and directionally
  inconsistent; widening that proxy family is closed.
- Q5-C found a reproducible shared error core, but its classifier was driven
  chiefly by `pre_rr` and `coupling_ratio`.  Timing-normal S beats therefore
  remain the relevant unresolved group, while RR reliance itself is not a new
  explanation.
- A previously unregistered external asset provides expert P-wave annotations
  for 12 MIT-BIH records.  The annotations were made by one expert and checked
  by a second expert.  This is an independent atrial landmark, not another
  fixed pre-QRS proxy:
  `https://physionet.org/content/pwave/1.0.0/` (DOI `10.13026/C2108F`).
- The reference records split cleanly into six DS1 records
  (`101, 106, 119, 122, 207, 223`) and six untouched DS2 records
  (`100, 103, 117, 214, 222, 231`).  No DS2 record may be used to change the
  delineation method, lead, window, RR rule, discordance rule, or gate.

This does not reopen residual CNN, subtype recovery, patient-CVaR/GroupDRO,
alarm-threshold, SMOTE/oversampling, FiLM/patient embedding, metric learning,
multi-beat context, 2D-DTW, INCART rescue, or proxy-widening directions.

# Alternative-design screen and current answerability

## Alternative A — frozen-model atrial-window intervention

This would be the more direct model-mechanism experiment, but it is not currently
executable.  The registered Drive V10 package contains saved per-seed
probabilities and metrics, but no exact V10 `pwave` checkpoints, model source,
or replay preprocessing package.  Drive-wide searches for `v10_ECG`, `v10.zip`,
`state_dict`, and model checkpoint extensions did not locate that replay bundle.
Do not retrain to fill this gap inside EXP-2026-007; retraining needs a new spec
and explicit user approval.

## Alternative B — use the public expert annotations directly

This is useful for qualification, but cannot by itself answer the Q5-C hard-core
question robustly.  Of the seven Q5-C core records
(`100, 200, 202, 210, 213, 232, 234`), only record `100` has a public expert
P-wave annotation file.  Q5-C contains only 10 shared-core S beats out of 33 S
beats in record 100.  A one-record result is not patient-independent evidence.

## Selected design — qualify one frozen delineator, then extend measurement

Use the public expert annotations solely to qualify a single deterministic
P-wave delineation rule.  Only if it passes the frozen DS2 qualification gate
may that rule be applied to the full MIT-BIH DS2 and the Q5-C core records.

**Answerability now:** the scientific question cannot be answered with the
files currently registered in Drive.  Raw full-record MIT-BIH waveforms and the
PhysioNet `pwave` v1.0.0 annotations are absent.  Acquiring, checksumming,
joining, and qualifying those inputs is the first and potentially terminal part
of this experiment.  `INPUT_ABSENT` or `MEASUREMENT_UNQUALIFIED` is a complete,
valid result: **지금은 답할 수 없다**.

# Controlled comparison

- Baseline: frozen V10 `pwave` probability files for seeds
  `1000, 1001, 1002, 1003, 1004`; use the mean of five per-seed metrics, not the
  post-hoc probability ensemble.
- Single changed variable: `P_ALIGNMENT = TRUE | SHAM`.
- P-wave rule: one frozen implementation of NeuroKit2
  `ecg_delineate(method="dwt")`, channel 0 only, using reference R locations
  rather than redetecting R peaks.  Pin and record the exact package version and
  source hash before reading any DS1 waveform.  Defaults are fixed; no method or
  parameter sweep is allowed.
- P-to-R scalar: for each valid beat, `PR_ms = R_sample - P_peak_sample` and
  `PR_discordance = abs(PR_ms - record_median_PR) / record_MAD_PR`.  The record
  median and MAD are label-free and use all valid beats in that record.
- Normal-like RR rule: derive the central interquartile interval of
  `coupling_ratio` from DS1 N beats only; freeze its two numeric endpoints before
  opening any DS2 outcome.  This deterministic rule is not model training.
- Discordance rule: the DS1 75th percentile of valid `PR_discordance`, frozen
  before opening DS2 outcomes.  Do not optimize this threshold for S PR-AUC.
- `SHAM`: within each record and frozen RR quartile, permute the complete
  `(PR_discordance, valid/missing)` assignment across eligible beats.  Use a
  seeded permutation and preserve counts exactly.
- Fixed components: DS1/DS2 membership, beat join, labels, model probabilities,
  preprocessing, R locations, lead, delineator, RR band, threshold, bootstrap,
  and all decision thresholds.
- Patient split: MIT-BIH DS1 -> DS2 inter-patient.  DS2 remains sealed until the
  code, tests, manifest, DS1-derived constants, and qualification rules are
  written.
- Seeds: model seeds `1000..1004`; permutation seed master `2026007`; bootstrap
  seed master `2026008`.
- Determinism/environment: save Python, OS, package versions, NeuroKit source
  hash, WFDB version, input SHA-256, and all RNG states in `manifest.json`.

# Negative control and what it falsifies

`SHAM` is the mandatory negative control.  It preserves record identity, RR bin,
P-measurement distribution, missingness, S prevalence, V10 probabilities, and
sample size while destroying only beat-specific P timing alignment.

If `SHAM` produces the same separation as `TRUE`, it falsifies the claim that
beat-specific atrial timing carries additional failure-associated information.
The observed separation would instead be compatible with record composition,
RR structure, missingness, prevalence, or a permissive matching rule.

# Inputs and outputs

## Present in Drive

- V10 per-arm/per-seed saved probabilities and metrics:
  `MyDrive/MedKOS/ecg-model/baseline_pkgs/v10pkg/`.
- Q5-C measured bundle, including `core_membership.csv`, `result.json`, and
  `manifest.json`:
  `MyDrive/MedKOS/ecg-model/runs/20260809T134523_EXP-2026-006/`.
- Registered processed MIT-BIH arrays (`mamba_data.npz` and related baseline
  assets) referenced by `research/ASSETS.md`.

## Absent from Drive at design time

- PhysioNet `pwave` v1.0.0 expert annotation files and published
  `SHA256SUMS.txt`.
- Complete raw MIT-BIH `.dat/.hea/.atr` files required to run and validate the
  delineator on all DS1/DS2 records.
- Exact V10 checkpoints/source/replay package.  These are not needed for this
  association audit because frozen saved probabilities are used, but their
  absence blocks a future input-intervention experiment.

## PREP_DATA acquisition gate

Execution is staged.  The currently authorized substage is **PREP_DATA-A
ACQUIRE_ONLY**: perform items 1-2, build the immutable inventory, verify that
every required file can be opened by WFDB, save the acquisition report, and
stop.  Do not perform item 3, delineation qualification, or any association
analysis until the PREP_DATA-A bundle has been reviewed.  An acquisition-only
run is not a scientific result and must not change this spec to `MEASURED`.

1. Download only from the versioned PhysioNet sources:
   `pwave/1.0.0` and `mitdb/1.0.0` (or the canonical version resolved before
   execution).  Record final URLs, versions, licenses, file sizes, and SHA-256.
2. Verify the `pwave` files against the publisher's `SHA256SUMS.txt`.
3. Join raw `atr` R samples to the registered processed beat identity using
   `(record, sample)` and the already-audited beat filtering semantics.  No
   nearest-neighbor many-to-one join is allowed.
4. Save the acquired immutable input bundle under a new Drive asset directory
   and add it to `research/ASSETS.md` only during measured-result intake.
5. If acquisition, checksum, record identity, lead order, sampling frequency, or
   unique join fails, emit `INPUT_ABSENT_OR_MISMATCH` and stop before scientific
   analysis.

## Files allowed to change during implementation

- `experiments/specs/EXP-2026-007-q5d-expert-validated-pwave-timing-audit.md`
- `mit-bih/q5d_expert_validated_pwave_timing.py`
- `mit-bih/test_q5d_expert_validated_pwave_timing.py`
- `notebooks/quest47_q5d_expert_validated_pwave_timing.ipynb`

Result intake into `research/ASSETS.md` and `research/PROJECT_STATE.md` is a
separate, reviewable commit after the full run; it must not alter notebook
outputs.

- Colab notebook: `notebooks/quest47_q5d_expert_validated_pwave_timing.ipynb`
- Drive run directory:
  `MyDrive/MedKOS/ecg-model/runs/<timestamp>_EXP-2026-007/`
- Required outputs: `config.json`, `manifest.json`, `result.json`,
  `decision.json`, `log.txt`, `input_inventory.csv`,
  `pwave_qualification.csv`, `beat_measurements.parquet`,
  `stratum_metrics.csv`, `null_distribution.csv`, figures, and an executed
  notebook with all displayed tables/plots saved.

# Measurement qualification gate

1. Run the frozen delineator on the six DS1 expert-annotated records.  This is a
   dry qualification report only; do not tune parameters or change the lead.
2. Freeze code, package hash, P matching tolerance (`+-50 ms`), physiological
   P-before-R search interval (`40..300 ms`), DS1-derived RR interval, and
   discordance threshold.  Save them before opening DS2 labels or V10 outcomes.
3. Run once on the six expert-annotated DS2 records.  Match detections to expert
   P annotations one-to-one within `+-50 ms`.
4. Qualification passes only if all are true:
   - DS2 record-macro P-peak sensitivity >= 0.80;
   - DS2 record-macro positive predictive value >= 0.80;
   - at least 5 of 6 DS2 reference records have sensitivity and PPV >= 0.70;
   - no record has a many-to-one or cross-beat annotation join;
   - the true P-match rate exceeds the within-record circular-shift chance rate
     by at least 4x, and its record-bootstrap 95% CI lower bound exceeds 1x.
5. The public resource warns that not every P wave is guaranteed to be labelled.
   Report this limitation.  Do not weaken the thresholds after seeing DS2.
6. If any item fails, emit `MEASUREMENT_UNQUALIFIED` and stop.  Do not continue
   with a broadened window, another delineator, a better-looking lead, or manual
   exclusions inside this experiment.

# Evaluation

- Primary metric: S-beat PR-AUC from each frozen V10 `pwave` seed, averaged over
  seeds.  The primary statistic is
  `DiD = [PRAUC_concordant - PRAUC_discordant]_TRUE -
  median([PRAUC_concordant - PRAUC_discordant]_SHAM)`
  among DS2 normal-like-RR beats.
- Secondary:
  - pooled and record-macro S PR-AUC in each stratum;
  - five seed-specific DiD values;
  - record-specific direction and S/non-S support;
  - the same frozen analysis restricted to the seven Q5-C core records;
  - association between `PR_discordance` and frozen V10 S score/error as a
    continuous, descriptive effect with no threshold promotion;
  - measurement missingness by record and class.
- Patient-level lower-tail analysis: report record-macro and worst-record
  S PR-AUC only as secondary diagnostics.  Do not reopen CVaR/GroupDRO.
- Bootstrap: 2,000 record-cluster bootstrap replicates; sample records first and
  carry all five seed predictions and all beats of a sampled record together.
- Null/permutation: 10,000 `SHAM` permutations.  Recompute eligibility, strata,
  S PR-AUC, and DiD from the beginning in every replicate.
- Leakage checks:
  - assert disjoint DS1 and DS2 patients/records;
  - assert no DS2-derived rule or threshold is serialized before code freeze;
  - assert labels never enter delineation, P matching, record median/MAD, or
    `SHAM` construction;
  - assert per-seed arrays join one-to-one to the same beat identities;
  - assert the model probability arrays are byte-identical before and after the
    run.

# Chance baseline and rule-relaxation rule

The chance baseline must be recomputed under the exact rule being evaluated.
The primary rule is fixed to one P-search interval, one RR band, one
discordance threshold, and one delineator.  Its empirical null is the 10,000
within-record, within-RR-bin `SHAM` permutations above.

Any wider P-search interval, wider RR-normal band, alternate matching tolerance,
alternate lead, alternate delineator, alternate threshold, or subgroup scan is
exploratory.  If such a sensitivity analysis is shown:

1. rerun the null with the relaxed rule itself;
2. take the maximum absolute statistic across the full allowed candidate set in
   each permutation (`maxT`);
3. compare the observed maximum only with that expanded max-null distribution;
4. never reuse the stricter rule's lower null cutoff.

Relaxing a rule creates more eligible matches or more opportunities to select a
large statistic, so its effective null/chance baseline can only stay the same or
rise.  A relaxed analysis cannot inherit or improve the primary gate merely by
using more candidates.

# Acceptance and stopping criteria

## Success: `P_TIMING_FAILURE_ASSOCIATION`

All conditions must hold:

- PREP_DATA and measurement qualification pass without deviation;
- primary DiD >= 0.015 S PR-AUC;
- record-cluster bootstrap 95% CI lower bound for DiD > 0;
- observed TRUE statistic exceeds the primary permutation-null 95th percentile;
- at least 4 of 5 model seeds have positive DiD;
- at least 5 eligible DS2 records have positive record-level direction;
- no single record contributes >50% of all eligible S beats;
- both discordance strata contain at least 100 S and 500 non-S beats overall,
  and at least five records contain both S and non-S support.

This permits only: “expert-validated P-wave timing discordance is associated
with the frozen V10 failure pattern after RR-restricted comparison.”

## Decision tree

1. **`INPUT_ABSENT_OR_MISMATCH`** — required public inputs cannot be acquired,
   checksummed, or joined.  Stop: **지금은 답할 수 없다**.
2. **`MEASUREMENT_UNQUALIFIED`** — the fixed delineator fails expert-reference
   qualification.  Stop: **지금은 답할 수 없다**.  The next candidate is a
   separately approved expert-annotation acquisition study, not a broader proxy.
3. **`INSUFFICIENT_PATIENT_SUPPORT`** — qualification passes but the preregistered
   stratum/record support gate fails.  Stop with no association claim; do not
   pool away the patient-independence problem.
4. **`GENERIC_RR_OR_RECORD_EFFECT`** — TRUE does not exceed the matched SHAM/max
   null, or the sham effect is of comparable size.  The negative control has
   falsified P-timing specificity.
5. **`NO_DETECTABLE_P_TIMING_ASSOCIATION` — “아무것도 없다.”**  Inputs,
   qualification, support, and control pass, but DiD is <0.015, its CI includes
   zero, or seed/record direction gates fail.  Conclude that this measurement
   found no robust additional failure-associated atrial-timing signal.  Do not
   widen the rule until it fits.
6. **`P_TIMING_FAILURE_ASSOCIATION`** — every success gate passes.  Promote only
   the failure-association statement above.  A causal/mechanistic claim still
   requires a later single-input intervention with an exact frozen model replay
   package and negative control.

## Terminate early if

- DS2 is opened before the DS1 constants and code hash are frozen;
- any implementation step trains, fine-tunes, calibrates, or selects a model;
- the implementation changes the standard DS1/DS2 patient split;
- the team proposes changing a method/window/lead/threshold after viewing DS2;
- a required output, provenance hash, or negative-control result is missing.

## Minimum effect worth interpreting

Primary DiD of 0.015 S PR-AUC.  Effects below this are reported numerically but
enter the explicit “nothing there” branch even if a nominal p-value is small.

# Visualization and report requirements

The executed notebook must begin with a one-screen decision card containing:
decision code, input gate, qualification gate, support counts, primary TRUE
contrast, SHAM null q95, DiD with 95% CI, seed direction, record direction, and
the exact permitted interpretation sentence.

It must also display:

- expert-vs-detected P timing Bland-Altman/scatter and per-record sensitivity/PPV;
- TRUE and SHAM PR-discordance distributions;
- S PR-AUC by stratum for all five seeds with uncertainty;
- the full permutation-null histogram with observed statistic and q95 marked;
- record-level support and effects, with record 232 domination visible;
- a table of every failed/passed gate and the first stopping reason;
- examples of valid, missing, and mismatched P delineations selected by a fixed
  seed, never cherry-picked after outcome inspection.

# Learning boundary

EXP-2026-007 is analysis-only.  It downloads public data, runs one frozen signal
processing rule, and evaluates already-saved predictions.  It performs no model
training.  Any learned P-wave detector, V10 replay retraining, score fusion,
rescue classifier, or new neural experiment requires a new preregistration and
separate explicit user approval before execution.

# Implementation checklist

- [ ] Read `AGENTS.md`, `CLAUDE.md`, `docs/AI_COLLABORATION.md`, and the Q5 handoff
- [ ] Obtain user approval and set `status: approved_for_implementation`
- [ ] Acquire and checksum the missing public inputs before analysis
- [ ] Freeze DS1 constants, code hash, and environment before opening DS2
- [ ] Add synthetic join, permutation, leakage, and max-null tests
- [ ] Preserve MIT-BIH DS1 -> DS2 patient independence
- [ ] Use the five frozen V10 seed arrays; do not substitute the ensemble metric
- [ ] Save the complete executed notebook and auditable Drive run bundle
- [ ] Ingest the measured result without changing notebook outputs
- [ ] Open a PR with exact commands, input URLs/hashes, and all deviations

# References

- PhysioNet MIT-BIH Arrhythmia Database P-Wave Annotations v1.0.0:
  `https://physionet.org/content/pwave/1.0.0/`
- Martinez JP, Almeida R, Olmos S, Rocha AP, Laguna P. A wavelet-based ECG
  delineator: evaluation on standard databases. IEEE Trans Biomed Eng.
  2004;51(4):570-581. DOI `10.1109/TBME.2003.821031`.
- NeuroKit2 ECG delineation documentation:
  `https://neuropsychology.github.io/NeuroKit/functions/ecg.html`

# Decision log

- 2026-08-09 — Codex draft.  Selected expert-qualified P-to-R timing audit over
  frozen-model occlusion because exact V10 replay assets are absent.  Registered
  acquisition and qualification as terminal gates, preserved a literal
  “nothing there” branch, and forbade proxy widening or DS2-driven rule changes.
- 2026-08-09 — User approved the direction.  Execution is staged: implement and
  run `PREP_DATA` first, acquiring and verifying the versioned PhysioNet inputs.
  Do not open the measurement-qualification or association-analysis stages until
  the acquisition bundle is reviewed and accepted.
