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
- `alpha` is initialised at exactly `0.0`, so the model's *initial output* equals
  the morphology baseline's. This is an initialisation property only — it does not
  guarantee that the checkpoint selected after training performs at least as well as
  the baseline (see the 2026-08-08 Decision-log entry on `best_epoch = 0` semantics).
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

Found during the CPU smoke run. `alpha` starts at exactly `0`, so the model's
*initial output* equals the offset's. With a bare patience counter, an arm whose
residual is not immediately helpful can end training after very few epochs, before
`alpha` has moved far from zero — which risks leaving a real effect under-trained
rather than measured.

Fix: early stopping cannot fire before epoch `DL_MIN_EPOCH = 4`, i.e. at least four
full training epochs always run. Best-checkpoint selection is unchanged. Decided a
priori from the gradient structure, not from any measured contrast.

*Corrected 2026-08-08*: this entry originally claimed "epoch 0's dev loss *is* the
morphology baseline's loss". That is wrong for this implementation — dev loss is
first computed **after** the first epoch's minibatch updates (~77–79 optimizer steps
at batch 1024 on the real cohort), so epoch 0 is a post-update checkpoint, and the
pre-training state (epoch −1) is never a dev candidate (`best_loss` starts at `inf`,
so the epoch-0 checkpoint always replaces the initial `best_state`). `DL_MIN_EPOCH`
guarantees a minimum number of epochs are *run*; it does not prevent the best
checkpoint from being epoch 0. Consequently there is no "guaranteed lower bound" on
the selected checkpoint's performance; `alpha = 0` at init gives initial output
equality only.

## 2026-08-06 — `comb_baseline_diagnostic` added so Arm E is interpretable

Found during the CPU smoke run. Arm E's offset is the 28-column `comb` set while Arm
A's is the 17-column `morph` set, so `E − A` mixes the feature change with the
residual and cannot answer "did the residual do anything?".

The runner therefore also scores a plain cross-fitted `comb` logistic —
`comb_baseline_diagnostic`, the clean analogue of Q4-N's `cpu_comb` — and reports
`E − comb_baseline` as the isolated residual effect. It is a diagnostic, not a sixth
arm: it gets no `arms/` directory, its logit goes into `predictions.npz`, and it
enters no gate. The primary comparison `C − A` is untouched.

## 2026-08-06 — Morphology port CONFIRMED against Q4-N on real SVDB

The first GPU attempt reached the porting-fidelity check before failing (below), and
it reported:

```text
measured LORO k-sweep 0.8361 vs Q4-N 0.8361 (delta -0.0000, within tolerance: True)
```

The ported morphology feature pipeline reproduces Q4-N's `morph` arm **to four decimal
places** under Q4-N's own LORO protocol. The freeze is verified, not merely asserted.

Cohort as loaded: 184,397 beats, 78 records, **56 scorable** under `MIN_S = MIN_N = 25`,
138,898 scored beats. Feature dims `{base: 9, morph: 17, comb: 28}`, as expected.

## 2026-08-06 — Bug in my own OOF audit (first GPU attempt aborted)

The first GPU run aborted in `cross_fitted_offsets` with:

```text
Q4OError: outer fold 0: 45499 samples have an OOF assignment count != 1
(min 0, max 1). This is exactly the Q4-N overwrite failure mode.
```

The message was wrong on both counts. `min 0, max 1` means **nothing was assigned
twice** — the Q4-N failure mode is `max > 1`. And 45,499 is exactly
184,397 − 138,898: the beats belonging to the 22 records that fall below
`MIN_S`/`MIN_N`. Those records are correctly absent from the fold map and are
legitimately never scored; my audit compared the assignment count over the **whole
cohort** instead of over the **scored subset**, so it fired on beats that were never
supposed to be scored at all.

The all-scorable synthetic fixture could not catch this, which is the real lesson: the
fixture did not have the same shape as the data.

Fixes:

- the OOF audit runs over the scored subset, and separately asserts that no beat
  outside the scorable cohort received an offset;
- the error message distinguishes "scored more than once" (the Q4-N mode) from
  "never scored", instead of blaming both on the overwrite bug;
- `assert_finite` on the offsets is likewise restricted to scored beats;
- unscored beats are `NaN` in `probs.npy`, `fold = -1` and `scored_mask = False` in
  `predictions.npz` — never a fabricated probability. `verify_bundle` now enforces
  that every beat the run *claims* to have scored is finite;
- `synthetic_cohort` gained `n_unscorable`, and both the unit tests and the end-to-end
  smoke run now use a cohort containing unscorable records.

No scientific quantity is affected: the fold map, the arms, the metric, and the gates
are unchanged. This was an assertion-scope bug, not a modelling one.

## 2026-08-06 — Second GPU attempt failed on a stale import, not on the code

The second attempt raised the *same* error after the fix was pushed. It was not a
second bug — the kernel was executing the old module. Two tells in the traceback:

- it displayed line 825 as `full = _fit_logit(X[tr], cohort.y[tr])`, which is that
  line in the **fixed** file, while raising the **old** message
  (`"This is exactly the Q4-N overwrite failure mode"`) that no longer exists on disk.
  Tracebacks take line numbers from the loaded code object but read source text from
  the current file, so new source rendered at old line numbers means a stale module.
- the kernel id was `ipykernel_433` in both attempts — no restart between them.

Cause: `import q4o_leakage_free_residual` is a no-op once the module is in
`sys.modules`. `git reset --hard` updated the file, not the running kernel. The test
cell made this worse rather than catching it: it runs the test script as a
**subprocess**, which reads the new file and passes, while the kernel keeps running
the old code.

Fixes (in the code, not in the instructions):

- `MODULE_VERSION` / `MODULE_BUILD` stamps in the module, bumped on behaviour changes;
- `self_check()` runs the exact path that a stale import gets wrong — a cohort
  containing records below `MIN_S`/`MIN_N` — **in the caller's interpreter**, and
  raises naming the stale-import cause;
- the notebook's import cell purges every `q4o_leakage_free_residual*` entry from
  `sys.modules` and calls `importlib.invalidate_caches()` before importing, then
  asserts the version and runs `self_check()`;
- the test cell re-asserts the in-kernel version after the subprocess run, because a
  passing subprocess says nothing about the loaded module.

A stale import now fails at cell 1 in about a second, instead of surviving to minute
one of the run.

## 2026-08-06 — Fit-split normalisation computed in chunks

Found while auditing what lay downstream of the abort. `float(X[fit_idx].mean())`
materialises a ~1.4 GB temporary for Arm E's 8-channel 3-beat input, and again for the
std, on top of ~2.7 GB of persistent waveform arrays. Replaced with a chunked
accumulator that also accumulates in float64, so it matches the exact float64 mean/std
and is *more* accurate than the float32 reduction it replaces. Verified in tests to be
exact and independent of chunk size.

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

## 2026-08-06 — Presentation-only revision: reporting layer added

**This revision changes no scientific result.** No arm definition, fold map, seed,
metric, bootstrap, gate, or NO-GO rule was touched, and no value in any existing
`result.json` was recomputed or overwritten. What was added is a reporting layer that
reads a finished run bundle and renders it for a human.

Target run: `20260806T0923_EXP-2026-001_q4o_leakage_free_residual_cnn`.

What was added:

- `ANALYZE_EXISTING_RUN` mode in the notebook. Set the flag and a run directory, and
  the notebook reads `result.json`, `manifest.json`, `predictions.npz`, and each
  arm's `probs.npy` and produces the whole report with **no retraining**. The
  cohort-loading, training, and registry-append cells are all skipped in this mode —
  in particular the registry is never re-appended for a run that is already in it.
- `generate_report()`: a Korean executive summary, ten figures/tables, and
  `report_summary.md`, all written into the run's `figures/`.
- Per-record values, which `result.json` stores only as summaries, are recomputed
  from the stored logits with the same `achievement_at()` the run used.

Two self-checks make the "presentation only" claim testable rather than asserted:

1. **Reconciliation** — the recomputed per-arm, per-seed k-sweep means are compared
   against `result.json`. Measured max absolute difference: **0.0**. If it ever
   exceeds `1e-9`, `generate_report()` raises instead of emitting a report, because a
   report that disagrees with the run is worse than no report.
2. **Immutability** — `config.json`, `manifest.json`, `result.json`, `fold_map.json`,
   `predictions.npz`, and every `arms/*/probs.npy` are SHA256-fingerprinted before and
   after reporting, and any change raises. A test asserts the fingerprints are equal.
   *(2026-08-08)* `training_history.json` is included in the fingerprint **when it
   exists** — i.e. for runs executed after history recording was added. Runs without
   one (such as `20260806T0923`) are unaffected; the file is never created
   retroactively, and a test asserts both directions.

Interpretive choices worth recording, because they shape how the run reads:

- **The waterfall averages all five seeds**, not one. A single-seed waterfall would
  be a different quantity, and the CSV records `n_seed_averaged` so this cannot be
  misread later.
- **Δ vs A** in the arm table is the *paired contrast* from `result.json` wherever one
  was measured. For an arm with no paired contrast (`comb_baseline_diagnostic`) the
  plain difference of means is reported and explicitly labelled `mean_difference`, so
  it is never mistaken for a paired result.
- **The report states what the NO-GO does not prove.** In this run Arm C selected
  `best_epoch = 0` in every (seed × fold) combination: the checkpoint after the
  **first completed training epoch** (~77–79 optimizer steps at batch 1024) was
  selected, and no later epoch improved dev BCE loss. Epoch 0 is a post-update
  state, not the pre-training initialisation — the selected checkpoints' `alpha`
  values are mostly `|0.078–0.101|`, not 0. Because the pre-training checkpoint
  (epoch −1) was never evaluated as a dev candidate, this run cannot decide whether
  epoch 0 improved on the exact morphology baseline. The report says so, in the
  executive summary, on the diagnostics figure, and in `report_summary.md`. That
  does **not** license a Transformer — the pre-registered stopping rule still
  forbids it — but it makes the cause of `best_epoch = 0` (schedule, first-epoch
  overfitting, or checkpoint-selector definition) the first thing a follow-up spec
  should separate. `alpha`'s sign can flip together with the head's sign, so the
  sign alone is not seed instability; interpret `alpha × residual` instead.

## 2026-08-06 — Axis fix: primary and reference contrasts were sharing a scale

`contrasts.png` plotted every contrast on one axis. `B − A` is roughly two orders of
magnitude larger than `C − A`, so the primary contrast, the negative control, and the
gate line all collapsed into one indistinguishable dot at zero — the figure was
unreadable exactly where the decision is made.

`_write_figures` now emits `contrasts_primary.png` and `contrasts_reference.png` on
separate axes, and the report adds `primary_contrasts_zoom.png` (auto-scaled to the
primary CIs, with the value and PASS/FAIL beside each point) and
`reference_gap_separate.png`. Presentation only — no measured value changed.

## 2026-08-06 — Training history recorded for future runs only

`_train_one_fold` now returns a per-epoch history (train BCE loss, dev BCE loss, dev
PR-AUC, `alpha`), written to `training_history.json`, and `learning_curves.png` is
drawn from it.

Constraints honoured:

- **Checkpoint selection is unchanged.** It is still `argmin` of dev BCE loss. Dev
  PR-AUC is recorded for the curves and never consulted for selection; a test asserts
  `best_epoch == argmin(recorded dev_loss)` for every (arm, seed, fold).
- **Training computation is unchanged.** Train loss is accumulated from the loss
  already computed for the backward pass, and dev PR-AUC reuses the dev logits from
  the forward pass that already runs for dev loss. No extra optimiser step, no extra
  RNG draw.
- **Nothing is back-filled.** The `20260806T0923` run predates this and has no
  history. The report says so plainly, draws no learning curves, and writes no
  history file of its own. A test copies a bundle, deletes its history, and asserts
  exactly that.

## 2026-08-08 — Presentation/semantics correction (no measured value changed)

Phase A of the post-run review corrected the *description* of `best_epoch = 0`
everywhere it appears (this spec, the module's report prose, the diagnostics-figure
caption, the notebook): epoch 0 is the checkpoint after the first **completed**
training epoch, not a reversion to the pre-training initialisation, and the run
never evaluated the pre-training checkpoint (epoch −1) as a dev candidate. All
"guaranteed lower bound"-type claims, pre-training-reversion claims, and
"residual never turned on" phrasings were removed or replaced. The Q4-O training loop, checkpoint selection, and every measured
artifact (`config.json`, `manifest.json`, `result.json`, `fold_map.json`,
`predictions.npz`, `arms/*/probs.npy`) are unchanged — tests fingerprint them
before/after reporting. The test runner also hardens stdout so Windows CP949
consoles do not die on non-ASCII characters (em dashes, box-drawing rules) in test
output.

## 2026-08-06 — Result status *(superseded — see 2026-08-08 update below)*

At the time this entry was written, no GPU run had been executed. `registry.jsonl`
append is implemented but only ever writes values that came out of an actual run.

## 2026-08-08 — Result status update: the GPU run has been executed — verdict NO-GO

The pre-registered GPU run was executed on 2026-08-06 (Colab, Tesla T4) at repo
commit `624e987b917ec021c9fc2130f37f6f35e720601c`. The run bundle is
`runs/20260806T0923_EXP-2026-001_q4o_leakage_free_residual_cnn` on Drive
(`MedKOS/ecg-model/runs/`). Measured values, read from that bundle's `result.json`
(the authoritative record — nothing here re-measures anything):

- Arm A (morph baseline) k-sweep mean `0.830955`; Arm C (primary) `0.831821`
- `C − A` `+0.000866`, 95% CI `[-0.002083, +0.004206]`
- `C − D` `+0.001302`, 95% CI `[-0.001642, +0.004600]`
- `E − cleanComb` `+0.003743`, 95% CI `[-0.003532, +0.011847]`
- Gates: 3/6 passed → final verdict **NO-GO**

Arm C selected `best_epoch = 0` (the first-completed-epoch checkpoint — see the
2026-08-08 semantics correction above) in all 25 seed×fold combinations. The run
predates training-history recording, so it has no `training_history.json`, and none
is created retroactively. Follow-up: EXP-2026-002 / Q4-P separates the candidate
causes of `best_epoch = 0` without re-running or modifying this experiment.
