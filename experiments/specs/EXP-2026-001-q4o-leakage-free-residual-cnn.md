---
experiment_id: EXP-2026-001
arm_id: Q4-O
title: Leakage-free morphology baseline freeze and current-beat raw-CNN complementarity validation
status: approved_for_implementation
design_owner: codex
implementation_owner: claude
dataset: SVDB
data_file: svdb_data5.npz
data_path_expected: /content/drive/MyDrive/mitbih/svdb_data5.npz
split: frozen record-grouped 5-fold CV
inner_split: record-grouped 5-fold cross-fitting inside each outer-train
primary_metric: record_level_k_sweep_achievement_mean
primary_k_sweep: [50, 100, 200, 300]
primary_comparison: arm_C_morph_plus_raw_residual minus arm_A_morph_baseline
negative_control_comparison: arm_C_morph_plus_raw_residual minus arm_D_shuffled_waveform_control
arms:
  - A: morph_baseline
  - B: raw_current_cnn
  - C: morph_plus_raw_residual
  - D: shuffled_waveform_control
  - E: corrected_q4n_diagnostic
training_seeds: [20260806, 20260807, 20260808, 20260809, 20260810]
waveform_permutation_seed: 20261797
fold_map_seed: deterministic_burden_sort_no_rng
expected_drive_run_dir: MyDrive/MedKOS/ecg-model/runs/<timestamp>_EXP-2026-001_q4o_leakage_free_residual_cnn/
acceptance_criteria:
  - mean_C_minus_A >= 0.015
  - paired_record_bootstrap_95CI_lower_C_minus_A > 0
  - mean_C_minus_D > 0 and paired_record_bootstrap_95CI_lower_C_minus_D > 0
  - seed_direction_positive_count >= 4 of 5
  - p10_lower_tail_C >= p10_lower_tail_A - 0.01
  - all leakage and reproducibility assertions pass
stopping_criteria:
  - NO-GO if C-A CI contains 0
  - NO-GO if mean gain < 0.015
  - NO-GO if C does not beat D
  - NO-GO if seed direction unstable
  - NO-GO if lower tail degrades
  - NO-GO if any leakage assertion fails
  - On NO-GO do not build a Transformer or a larger fusion model
allowed_files:
  - experiments/specs/EXP-2026-001-q4o-leakage-free-residual-cnn.md
  - mit-bih/q4o_leakage_free_residual.py
  - mit-bih/test_q4o_leakage_free_residual.py
  - notebooks/quest47_q4o_leakage_free_residual_cnn.ipynb
implementation_command: python mit-bih/q4o_leakage_free_residual.py --smoke --out <dir>
test_command: python mit-bih/test_q4o_leakage_free_residual.py
created: 2026-08-06
---

# Hypothesis

Falsifiable claim under test:

> On SVDB, adding a **current-beat raw-waveform residual** on top of a **leakage-free**
> morphology logistic offset improves the record-level k-sweep achievement mean by
> at least **+0.015** over the morphology baseline alone, and this improvement is
> larger than what the same architecture achieves when the beat-level
> waveform-to-label correspondence is destroyed.

The null this experiment must be able to accept: the raw current beat carries **no**
label-relevant information beyond what the frozen morphology features already encode.

# Why now

Q4-N (`quest46_q4n_scope_rank_vector`, branch
`claude/ai-model-ecg-diagnosis-6v8hof-5v35t1`, commit `acbafb5`) reported a residual
boosting result that **cannot** be used, because the offset that the residual CNN was
trained and evaluated against was partly in-sample. See the Decision log entry
`2026-08-06 / Q4-N OOF overwrite` below for the code-level evidence.

Therefore three things have to happen before any further model complexity:

1. The morphology baseline has to be **re-frozen under a leakage-free protocol**, so
   the project has a trustworthy number to compare against.
2. The residual-CNN complementarity question has to be **re-asked** with a
   cross-fitted offset.
3. The Q4-N residual result has to be **re-run as a diagnostic** to see whether the
   reported `boost_fix = 0.8631` survives removal of the contamination.

This does **not** reopen a closed direction. `research/PROJECT_STATE.md` lists
multi-beat context, patient embedding, SMOTE, and metric learning as closed; none of
them are used here. Arm B/C/D use the **current beat only**.

# Controlled comparison

- **Baseline (Arm A)**: `morph_baseline` — Q4-N's `morph` arm feature matrix
  (`F_BASE` 9 RR columns ⊕ `MORPH` 8 morphology columns = 17 columns), logistic
  regression, `C=1.0`, `max_iter=3000`. Scaler and model are fit on outer-train
  records only. Outer-test predictions come from a model that has never seen any
  outer-test record.
- **Single changed variable (Arm A → Arm C)**: the addition of an `alpha`-scaled
  residual head that reads **only the current beat's two lead waveforms**. Nothing
  else changes — same fold map, same morphology definition, same metric, same
  seeds.
- **Fixed components**: morphology feature definition (frozen verbatim from Q4-N),
  achievement metric and its k-sweep, record cohort rule (`MIN_S = MIN_N = 25`),
  record-burden stratification principle, `SEED0 = 20260806` base.
- **Record split**: frozen record-grouped 5-fold CV. The fold map is generated once
  and shared by every arm and every seed, and saved as `fold_map.json`.
- **Seeds**: five training seeds `20260806..20260810`. The Arm D waveform
  permutation seed (`20261797`) is separate from and never equal to any model seed.
- **Determinism/environment**: `torch.use_deterministic_algorithms(True)` where the
  ops allow it, `cudnn.deterministic = True`, `cudnn.benchmark = False`,
  `CUBLAS_WORKSPACE_CONFIG=:4096:8`. Any op that refuses to run deterministically is
  named in `manifest.json` under `nondeterministic_ops` rather than silently
  tolerated.

## Arms

### Arm A — `morph_baseline`

Q4-N morphology features only, logistic. Every scaler and every model is fit on
outer-train records. Outer-test predictions are produced by a model that saw no
outer-test record.

### Arm B — `raw_current_cnn`

Current beat's two lead waveforms only. **Forbidden here**: previous/next beat, RR,
morphology, P-vector, or any other clinical feature. Small 1D CNN, no offset.

Arm B is a reference point, not a gate. Its role is to show what the raw current beat
alone can do under the identical fold map.

### Arm C — `morph_plus_raw_residual` (primary)

```text
final_logit = morph_offset + alpha * cnn_residual
```

- `morph_offset` is the **cross-fitted** Arm A logit (Section "Leakage-free
  stacking").
- `cnn_residual` reads the current beat's two lead waveforms only.
- `alpha` is initialised at exactly `0.0`, which guarantees the model starts at the
  morphology baseline and therefore has a guaranteed lower bound at initialisation.
- The residual head's last linear layer is initialised **xavier-uniform**, not zeros.
  Initialising `alpha = 0` and the head weights `= 0` at the same time creates the
  gradient deadlock diagnosed in Q4-N (`∂L/∂alpha ∝ h(z) = 0` and
  `∂L/∂h_w ∝ alpha = 0`). The implementation carries a unit test asserting that the
  residual branch receives a non-zero gradient at step 0.

### Arm D — `shuffled_waveform_control` (key negative control)

Identical architecture, identical training schedule, identical offset, identical
folds and seeds as Arm C. The only change: **within each record**, the beat waveform
tensor is permuted across beats, so a beat's label no longer corresponds to its own
waveform. The record's signal distribution is preserved exactly (it is a permutation
of the same rows); the beat-level waveform information is destroyed.

Permutation rule: `beat[idx_of_record] = beat[idx_of_record][rng.permutation(n_rec)]`
with `rng = np.random.RandomState(20261797 + record_id)`. RR channels, labels, record
ids, and the morphology offset all stay attached to the original beat. The permutation
is applied once, before folding, and its seed and rule are written into
`manifest.json`.

### Arm E — `corrected_q4n_diagnostic` (diagnostic only)

Q4-N's `boost_fix` structure kept as close as possible: 3-beat input
(`prev ⊕ current ⊕ next` waveforms plus two RR ratio channels, `3*n_lead + 2`
channels), `comb` feature offset (`F_BASE ⊕ MORPH ⊕ VEC ⊕ PONT2` = 9+8+6+5 = 28 columns),
xavier head init, `alpha = 0` start, BCE loss.

**The only substantive change is that the offset is cross-fitted instead of
overwritten in-sample.**

Arm E must **not** be declared the primary result and must **not** become the new
baseline. Its only job is to answer: does `0.8631` survive de-contamination?

## Forbidden in this experiment

Transformer; prev/next beat in Arms B/C/D; rank loss; P-vector or P-on-T inside
Arms B/C/D; auxiliary physiology loss; patient embedding; SMOTE; any threshold,
early stopping, or feature selection that reads the test fold; and changing the
metric or `k` after seeing results.

# Inputs and outputs

- **GitHub inputs**: this spec; `mit-bih/q4o_leakage_free_residual.py`.
- **Data input**: `svdb_data5.npz`, expected at
  `/content/drive/MyDrive/mitbih/svdb_data5.npz`. This is the exact file Q4-N read
  (`SV5 = os.path.join(MITBIH, "svdb_data5.npz")`, `MITBIH = <DRIVE_ROOT>/mitbih`).
  **`svdb_data.npz` is a different file and must not be substituted.** The runner
  refuses to start if the required keys (`pid`, `y3`, `pre_rr`, `post_rr`, `beat`,
  `sym`) are missing.
- **Files allowed to change**: see `allowed_files` in the frontmatter. No other
  research file and no existing result is touched.
- **Colab notebook**: `notebooks/quest47_q4o_leakage_free_residual_cnn.ipynb`.
- **Drive run directory**:
  `MyDrive/MedKOS/ecg-model/runs/<timestamp>_EXP-2026-001_q4o_leakage_free_residual_cnn/`

Required outputs:

```text
runs/<timestamp>_EXP-2026-001_q4o_leakage_free_residual_cnn/
  config.json
  manifest.json
  result.json
  log.txt
  fold_map.json
  predictions.npz
  figures/
  arms/
    morph_baseline/probs.npy
    raw_current_cnn/probs.npy
    morph_plus_raw_residual/probs.npy
    shuffled_waveform_control/probs.npy
    corrected_q4n_diagnostic/probs.npy
```

Each `probs.npy` is `(n_seed, n_sample)` in the **same sample order** as
`predictions.npz`, which carries `sample_id`, `record_id`, `y_true`, `fold`, and
`seeds`. `sample_id` is the row index into the original `svdb_data5.npz` arrays, so
every probability can be traced back to a specific beat.

`manifest.json` must record: absolute data path, file name, SHA256, array shapes and
dtypes, class count, record/patient counts, per-fold record lists, git commit SHA,
Python and core package versions, and CUDA/GPU information.

# Leakage-free stacking

For each outer fold `f`:

1. Remove the outer-test records of `f` entirely.
2. Run a record-grouped inner cross-fit inside the outer-train records.
3. Every outer-train sample receives a prediction from an inner model that did not
   train on it, **exactly once**.
4. That cross-fitted offset is what the residual CNN trains against.
5. The outer-test offset comes from a single morphology model fit on the **whole**
   outer-train set.
6. Every normalisation, scaler, and feature-selection step is fit inside the
   training scope that owns it and nowhere else.
7. The early-stopping validation records are chosen inside outer-train only
   (burden-sorted, every `DEV_EVERY = 4`-th record, following Q4-N's rule).

Required assertions (implemented, and covered by tests):

- per outer fold, each OOF sample assignment count `== 1`;
- `train_records ∩ test_records == ∅` for every outer fold;
- `inner_train_records ∩ inner_valid_records == ∅` for every inner fold;
- outer-test labels never reach any threshold, scaler, or early-stopping decision;
- number of predictions equals the number of input samples;
- no `NaN` and no `Inf` anywhere in the offsets or the arm scores.

# Evaluation

Protocol preserved from Q4-N so the numbers stay comparable.

**Primary**

- record-level k-sweep achievement mean, `k ∈ {50, 100, 200, 300}`,
  `achievement(r, k) = TP@k / min(S_r, k)`;
- Arm C − Arm A paired difference.

**Key negative control**

- Arm C − Arm D paired difference.

**Secondary**

- `k = 30` and `k = 50` operating-point achievement;
- record/patient macro PR-AUC;
- record/patient macro AUROC;
- lower-tail 10th percentile of the per-record primary metric;
- worst-record result and its record id;
- per-seed results and their standard deviation;
- diagnostic comparison of Arm E against the Q4-N reported numbers
  (`cpu_comb = 0.8445`, `boost_fix = 0.8631`, `boost_rank = 0.8492`), reported as a
  **contaminated-versus-clean** contrast and never as a baseline.

All comparisons are paired on the same fold and the same seed. Record-level paired
bootstrap 95% CIs are reported for every contrast (2000 resamples). A hierarchical
bootstrap that resamples records **and** seeds is reported alongside it.

Note on wording: in SVDB one record is one patient, so "record macro" and "patient
macro" are the same quantity here; the manifest states this explicitly rather than
implying two independent views.

# Acceptance and stopping criteria

**PASS requires all six:**

1. `mean(C − A) >= +0.015`
2. paired record-bootstrap 95% CI lower bound of `C − A` `> 0`
3. `mean(C − D) > 0` **and** its 95% CI lower bound `> 0`
4. at least 4 of 5 seeds show a positive `C − A` direction
5. the lower-tail 10th percentile of C is not worse than A's by more than `0.01`
6. every leakage and reproducibility assertion passes

**NO-GO if any of:** the `C − A` CI contains 0; the mean gain is below `+0.015`;
C does not significantly beat the waveform-shuffle control D; the seed direction is
unstable; the lower tail degrades; a leakage assertion fails.

**On NO-GO**: do not build a Transformer and do not build a larger fusion model.
Keep the morphology baseline and return to failure-record and lower-tail analysis.

**On PASS**: do not go to a Transformer either. The next step is to port the *same*
minimal residual structure to MIT-BIH DS1→DS2 under the primary S PR-AUC protocol.

**Minimum effect worth interpreting**: `+0.015` on the k-sweep achievement mean.
Anything smaller is inside the range this protocol cannot separate from noise, and is
reported but not interpreted.

# Implementation checklist

- [x] Read `AGENTS.md`, `CLAUDE.md`, `docs/AI_COLLABORATION.md`, `research/PROJECT_STATE.md`, `research/ASSETS.md`
- [x] Confirm the Q4-N OOF overwrite at code level
- [x] Freeze the morphology definition verbatim
- [x] Implement leakage assertions
- [x] Add tests, including a test that *detects* the Q4-N overwrite pattern
- [x] CPU smoke run on synthetic grouped fixture data
- [ ] GPU run in Colab (user)
- [ ] Save executed notebook and run bundle
- [ ] Ingest measured result
- [ ] Review by design owner

# Decision log

## 2026-08-06 — Q4-N OOF overwrite (why `0.8631` is excluded from the baseline)

Located in `notebooks/quest46_q4n_scope_rank_vector.ipynb` on branch
`claude/ai-model-ecg-diagnosis-6v8hof-5v35t1` (commit `acbafb5`), section R6:

```python
def cpu_fold(X):
    sc = np.full(len(K), np.nan)
    for f in range(DL_FOLDS):
        te_r = [r for r in REC_OK if FOLD[r] == f]
        tr_r = [r for r in REC_OK if FOLD[r] != f]
        tr = np.concatenate([IDXS[r] for r in tr_r])
        te = np.concatenate([IDXS[r] for r in te_r])
        mu, sd = X[tr].mean(0), X[tr].std(0) + 1e-9
        lr = LogisticRegression(max_iter=3000, C=1.0).fit((X[tr] - mu) / sd,
                                                          TT_[tr].astype(int))
        sc[tr] = lr.decision_function((X[tr] - mu) / sd)   # <-- in-sample, overwrites
        sc[te] = lr.decision_function((X[te] - mu) / sd)
    return sc
OFF = cpu_fold(FEAT["comb"])
```

The function writes **both** the train and the test positions of a single shared
array `sc`. The five folds run in sequence, so each fold's `sc[tr] = ...` overwrites
whatever the earlier folds wrote there. After the final iteration (`f = 4`), the
array holds:

- the 20% of samples belonging to fold 4's **test** records — genuinely
  out-of-sample;
- the remaining ~80%, which are fold 4's **training** records — **in-sample
  predictions from a model fit on those very samples**.

Consequences, all of which this experiment treats as invalidating:

- `cpu_comb = 0.8445` is not a baseline. It is scored on an array that is ~80%
  in-sample, so it is optimistically biased by an unknown amount.
- `boost_fix = 0.8631` and `boost_rank = 0.8492` used that array as the residual
  offset. The CNN trained against an offset that had already memorised the training
  beats, and was evaluated on test beats whose offset came from a clean model. The
  offset therefore has a *different statistical character* on train than on test,
  which corrupts both the learned `alpha` and the reported delta.
- The reported delta `boost_fix − cpu_comb = +0.0186` is a difference between two
  numbers computed on the same contaminated array, so its sign is not interpretable
  either.

**Decision**: `cpu_comb = 0.8445`, `boost_fix = 0.8631`, and `boost_rank = 0.8492`
are excluded from the project's baseline record. They are carried in `REF_Q4N` only
as *contaminated reference values* for the Arm E diagnostic contrast. The Q4-N
initialisation-deadlock diagnosis itself (`alpha` and head both zero-initialised →
mutual zero gradient) is **not** invalidated by this bug — it is an
architecture-level argument, and Q4-O keeps the fix (xavier head, `alpha = 0` start)
and adds a unit test for it.

Note on scope: Q4-N's **CPU arms** (`base`, `morph`, `vec`, `vshuf`, `pont2`,
`p2shuf`, `comb`, e.g. `morph − base = +0.1570`) used the separate `loro()` /
`fit_fold()` path, which holds out one record at a time and fits on the rest. That
path is not affected by this bug. Only the R6 deep-learning section's `cpu_fold()`
offset is.

## 2026-08-06 — Data file confirmed, not substituted

Q4-N reads `SV5 = os.path.join(MITBIH, "svdb_data5.npz")` with
`MITBIH = os.path.join(DRIVE_ROOT, "mitbih")` and `DRIVE_ROOT = "/content/drive/MyDrive"`
under Colab, i.e. `/content/drive/MyDrive/mitbih/svdb_data5.npz`. It requires the keys
`pid`, `y3`, `pre_rr`, `post_rr`, `beat`, `sym`. `svdb_data.npz` (documented in
`mit-bih/HANDOFF.md` §1.2 with keys `beat`, `y`, `pid`, `pre_rr`, `post_rr`) is a
**different, older** file without `y3`/`sym`. Q4-O uses `svdb_data5.npz` and nothing
else. No blocker.

## 2026-08-06 — Morphology definition frozen; two implementation-level notes

The Arm A feature matrix is Q4-N's `morph` arm: `F_BASE` (9 RR-derived columns)
concatenated with `MORPH` (`morph_feats(extended=False)`, 8 columns) = 17 columns.
Windows, fractions, template rule (`TMPL_LO/HI/MIN`), and constants are copied
verbatim. Two implementation-level notes, neither of which changes the definition:

1. Q4-N computes the local RR baseline with
   `pd.Series(pre).groupby(pd.Series(RID)).apply(lambda x: x.shift(1).rolling(k, min_periods=1).median())`
   and then `np.asarray(...)`, which relies on the groups being contiguous and
   ascending for the result to line up with the original row order. Q4-O computes
   the same quantity with an explicit per-record positional loop, which is
   order-exact by construction. The arithmetic is identical.
2. Q4-N's per-record `std`/`mean` columns are record-level constants broadcast to
   the record's beats; Q4-O reproduces that broadcast explicitly.

A **porting-fidelity check** is pre-registered: the runner can optionally re-score
Arm A's feature matrix under Q4-N's original leave-one-record-out protocol and
compare against Q4-N's reported `morph` k-sweep of `0.8361`. Agreement within
`|Δ| <= 0.005` confirms the port. This is a diagnostic on the *port*, not a gate on
the *hypothesis*, and it is reported in `manifest.json` under
`morph_port_check`.

## 2026-08-06 — Split changed from LORO to record-grouped 5-fold, on purpose

Q4-N's CPU arms used leave-one-record-out; its R6 deep-learning section used a
record-grouped 5-fold map. Q4-O uses **record-grouped 5-fold for every arm**, because
the residual CNN cannot be trained ~40 times over without the compute cost dominating
the experiment, and because all five arms must share one fold map for the paired
comparisons to be valid. The stratification principle (sort records by
`(S-burden, record_id)`, assign `i % n_folds`) is Q4-N's, unchanged. Absolute values
are therefore **not** directly comparable to Q4-N's LORO numbers; only the
within-Q4-O paired contrasts are interpreted. This is recorded here rather than
applied silently.

## 2026-08-06 — Early-stopping warmup (`DL_MIN_EPOCH = 4`)

Found during the CPU smoke run. Because `alpha` starts at exactly `0`, epoch 0's dev
loss *is* the morphology baseline's loss. With a bare patience counter, an arm whose
residual is not immediately helpful stops at epoch 0, before `alpha` has left zero —
which makes the arm **untestable** rather than merely unhelpful, and would let a real
effect go unmeasured.

Fix: early stopping cannot fire before epoch `DL_MIN_EPOCH = 4`. Best-checkpoint
selection is unchanged, so the guaranteed lower bound still holds — if the residual
genuinely does not help, the restored checkpoint is still the near-baseline one.
Decided a priori from the gradient structure, not from any measured contrast.

## 2026-08-06 — `comb_baseline_diagnostic` added so Arm E is interpretable

Found during the CPU smoke run. Arm E's offset is the 28-column `comb` set while Arm
A's is the 17-column `morph` set, so `E − A` mixes the feature change with the
residual and cannot answer "did the residual do anything?".

The runner therefore also scores a plain cross-fitted `comb` logistic —
`comb_baseline_diagnostic`, the clean analogue of Q4-N's `cpu_comb` — and reports
`E − comb_baseline` as the isolated residual effect. It is a diagnostic, not a sixth
arm: it gets no `arms/` directory, its logit goes into `predictions.npz`, and it
enters no gate. The primary comparison `C − A` is untouched.

## 2026-08-06 — `requirements.txt` unchanged

The runner needs `numpy`, `scipy`, `scikit-learn`, `pandas`, `torch`, and
`matplotlib`. All of these are pre-installed in Colab, which is where the experiment
actually runs, and the repository's `requirements.txt` describes the MedKOS content
pipeline rather than the ECG experiment environment. No change is proposed. If a
future run needs a pin, the reason goes here first.

## 2026-08-06 — Implementation and test commands

```bash
# unit / leakage / schema tests (no GPU, no real data)
python mit-bih/test_q4o_leakage_free_residual.py

# CPU smoke run on a synthetic grouped fixture, writes a full run bundle
python mit-bih/q4o_leakage_free_residual.py --smoke --out /tmp/q4o_smoke

# real run (Colab, GPU) — driven by the notebook, or directly:
python mit-bih/q4o_leakage_free_residual.py \
    --data /content/drive/MyDrive/mitbih/svdb_data5.npz \
    --out  /content/drive/MyDrive/MedKOS/ecg-model/runs/<timestamp>_EXP-2026-001_q4o_leakage_free_residual_cnn
```

## 2026-08-06 — Result status

**No GPU run has been executed.** No arm value, no delta, and no PASS/NO-GO verdict
exists yet. `registry.jsonl` append is implemented but only ever writes values that
came out of an actual run. Nothing in this spec, in the code, or in the notebook may
be read as a result.
