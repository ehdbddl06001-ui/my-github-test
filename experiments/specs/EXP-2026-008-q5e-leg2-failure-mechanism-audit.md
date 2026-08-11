---
experiment_id: EXP-2026-008
substage: Q5E_LEG2_FAILURE_MECHANISM_AUDIT
title: Q5-E Leg 2 join failure mechanism audit
status: draft
design_owner: codex
implementation_owner: claude
analysis_only: true
training_required: false
dataset: MIT-BIH
split: DS1_only_diagnostic
parent_experiment: EXP-2026-007
parent_spec: experiments/specs/EXP-2026-007-q5d-order-preserving-beat-join-gate.md
primary_metric: none_diagnostic_association_only
parent_primary_metric: S_PR_AUC
created: 2026-08-11
---

# Status boundary

This document is a **diagnostic design**.  It authorizes nothing.  It does not
change EXP-2026-007, does not change the frozen Q5-D join rule, and does not
reopen the parent association.

Q5-D finished as `JOIN_UNRESOLVED`: the registered join rule was neither
falsified nor qualified.  This diagnostic asks what the failure is *associated
with*.  It does not ask how to make the join succeed, and no result it produces
can license a new join rule.

The registered approval chain for this substage is:

1. Codex fixes this design in this file and opens a PR.  **This step.**
2. The user approves the read-only `PREP_M4_ASSET_FREEZE` scope; Claude runs
   only that preflight and records its identities, with no M0-M4 aggregation.
3. Codex accepts the preflight; the user approves the completed design and
   `status` becomes `approved_for_implementation`.
4. Claude implements the frozen design on `claude/<task>` **without executing
   it**.
5. The user separately approves execution on the registered artifacts.
6. Only then may M0-M4 run, write a new timestamped Drive bundle, and be
   reviewed.

Steps 2, 3 and 5 are separate approvals: asset-freeze preflight, implementation
design, and scientific execution respectively.  None authorizes DS2 per-beat
labels, V10 probabilities, the association analysis, or any training.  Those
seals are unchanged by this document.

The frontmatter `split` reads `DS1_only_diagnostic`.  That is the **scope of
this diagnostic**, forced by the DS2 seal, and it is not a change to the
project's principal benchmark: `AGENTS.md`'s DS1 -> DS2 inter-patient evaluation
and the parent's `S_PR_AUC` primary remain exactly as registered.

**No aggregation of `unmatched_and_ambiguous.csv` or `join_map.parquet` may be
computed before step 6** — including the zero-execution-cost M0.  A diagnostic
whose measurement plan is fixed after its cheapest measurement is seen is not a
preregistered diagnostic.

# Fixed question

> In the frozen Q5-D DS1 join, is the observed low V-class recovery and the
> record-level coverage collapse **associated with** local RR offset (H1),
> detector counterpart absence (H2), RR-semantics propagation (H3), or
> candidate-graph degeneracy (H4)?

One question, four preregistered competing associations.  This is an
observational audit of an already-measured, immutable run.  Its language
boundary is **"associated mechanism"** or **"failure-associated factor"**.
Nothing in this spec, and nothing an implementation of it may write, calls an
observed association a **cause**.  Observation over a frozen join cannot
establish causation, and the project has already recorded this same boundary
for Q5-A (`research/PROJECT_STATE.md`: "이것은 `원인`이 아니라 **실패 연관
요인**이다").

V is a **preregistered primary stratum** and stays one.  But the question is
not "why did V fail".  Record 208 lost 2,167 of 2,572 cache rows (84.3%), and
no MIT-BIH record is 84% V, so record 208's collapse necessarily includes N
beats.  A V-only framing is arithmetically insufficient and is refused here.

# Audited result: the fixed facts

Everything below is a measured quantity of one immutable run.  This diagnostic
reads them, verifies them, and never recomputes the join that produced them.

## Canonical bundle

| item | value |
|---|---|
| Drive run | `20260811T035108_EXP-2026-007_q5d_beat_join_DS1_GATE` |
| folder id | `1JjwBhU8BXf8lRrYPcM2UjFNdIKxE9Ghd` |
| producing module code SHA-256 | `6b098c67df3c8e2c8c070b093e6e2d801566f548a3173626745c4a126a97f226` |
| `rule_fingerprint` | `31c4be9f44582a68c301fe6cc6572f4db6ff0b3de694af68f6ac6a0f48c2b40e` |

Earlier bundles carrying `SUPERSEDED.json`
(`SUPERSEDED_GATE11_IMPLEMENTATION_DEFECT`, producing module
`4a3de5e861d9d371439247924a19e81acb3762e065017d6adb1f062a95e054d7`) are
**preserved and never read as the result**.  Failure to distinguish canonical
from superseded is a stopping condition (§QA).

## Decision

| item | value |
|---|---|
| `decision` | `JOIN_UNRESOLVED` |
| `first_stopping_reason` | `3_overall_coverage` |
| `failed_leg` | `LEG2_POSITIONAL_JOIN` |
| gates passed | 5 of 13 |
| gate count reconciliation | the spec body lists 12 numbered gates; `evaluate_gates()` records **13** because gate 2 is emitted as `2a_leg1_source_replay` + `2b_leg2_record_boundaries` and `13_ambiguity_reported` is recorded as well.  `5 of 13` is correct and must not be "corrected" to 12 |
| `training_performed` / `model_scored` / `v10_probability_opened` / `association_performed` | all False |

## Coverage and the null-facing gates

| quantity | value |
|---|---|
| overall coverage | `0.7594904156198691` |
| N coverage | `0.8097` |
| S coverage | `0.7341101694915254` |
| V coverage | `0.15776955602537` |
| `J_min` TRUE | `0.15750528541226216` |
| corrected gate 11 95% CI | `[-0.05260925120498404, 0.13225229746939302]` |

The corrected gate 11 interval straddles zero.  The defective implementation
had reported `[0.48239100367683824, 0.7195216751797353]`, an interval that
corroborated gate 9; the registered statistic does not.  The null arrays
(`wrong_record`, `order_shuffle`, `circular_shift`, `j_null_max`) were **bitwise
identical** across the defective and corrected module runs, 10,000/10,000 each,
which is the expected consequence of the bootstrap sitting off the null
generation path and was measured rather than argued.

## Failure composition

| reason | count |
|---|---|
| `LEG2_NO_CANDIDATE_EDGE` | 13,716 |
| `LEG2_EDGE_IN_NO_MAXIMUM_MATCHING` | 9,887 |
| `LEG2_AMBIGUOUS_RANK_CLASS` | 738 |
| total failure rows | 24,341 (mamba side 12,183 + cache side 12,158) |

These are **not one disease**.  `NO_EDGE` (candidate generation produced
nothing) and `NOT_OPTIMAL` (candidates existed but no forced certification) are
analysed as **separate failure processes** throughout, and no measurement pools
them except where §M5 explicitly requires a pooled row alongside the stratified
ones.

# Competing hypotheses and their distinguishing predictions

All four are registered as **equals**.  H1 is not the default: the recorded
Q5-D mechanism note ("a PVC's wide abnormal QRS shifts `detect_r()` relative to
the annotation") is an H1-flavoured hypothesis that cannot by itself produce
record 208's 84.3% loss, nor a 266-fold gap between the mismatched stratum's
registered deficit (-25 rows) and its 6,648 failures.

| | hypothesis | mechanism | distinguishing prediction |
|---|---|---|---|
| **H1** | `LOCAL_RR_OFFSET` | the beat-to-beat change in `detect_r()` position exceeds the frozen +/-1 sample tolerance | failed V / `NO_EDGE` rows have nearest-candidate `d_inf` concentrated at **2-5 samples**; failures are **isolated or in local pairs** (run length 1-2); no post-anchor propagation |
| **H2** | `COUNTERPART_ABSENT` | the corresponding detector beat does not exist at all | source-replay-confirmed **missing detector events explain `NO_EDGE` failures at the position level**; nearest candidate is absent or very far |
| **H3** | `RR_SEMANTICS_PROPAGATION` | mamba computes RR *after* the symbol/boundary filters with duplicated endpoints; the cache computes `rr_features(peaks)` *before* row selection with `nan -> 0.0` endpoints, so one lineage-local discordance shifts a whole RR beat for the neighbours | failure **runs of length >= 3** trail a replay-confirmed discordance anchor; distances sit at **local RR interval scale (21-100 or >100 samples)**, not 2-5 |
| **H4** | `CANDIDATE_GRAPH_DEGENERACY` | integer-quantized, repeated `(pre, post)` pairs raise candidate degree and maximum-chain competition until forced-edge certification certifies almost nothing | `NOT_OPTIMAL` and `AMBIGUOUS` rows have **higher candidate degree** than certified rows; concentrated in **stable-RR** segments; identical-RR-pair multiplicity higher and/or local RR variability lower |

H3 and H4 are the only two that can produce a 266-fold amplification of a small
count deficit.  That is a reason they must be measured, **not** a reason to rank
them in advance.

**No hypothesis is permitted to absorb all failures.**  `NO_EDGE` and
`NOT_OPTIMAL` are reported separately in every measurement, and a flag that
fires on one process makes no claim about the other.

# Preregistration principle

1. The complete M0-M4 plan — definitions, window sizes, bins, denominators,
   controls, thresholds, and the decision tree — is fixed by this document
   **before any of it runs**.
2. Seeing M0 may **not** change the definition, window size, bin edges, or
   interpretation rule of M1-M4.  Once any M0 result has been observed, an
   M1-M4 definition may not be amended at all: if one then proves
   unimplementable, the run **STOPs** and returns to Codex for a new
   preregistration.  An amendment is possible only *before* the first
   measurement of the run produces a number, and only through the Decision log
   in the open.  There is no in-flight repair path.
3. M0's zero execution cost is not an exemption.  §Status boundary forbids
   aggregating the bundle before the execution approval.
4. No measurement in this spec selects, tunes, or tests a tolerance.  It is
   explicitly forbidden to compute "coverage under tolerance k" for any k
   (§What this diagnostic does not license).

# Inputs

## Read (canonical bundle, DS1 only)

| file | what is read |
|---|---|
| `unmatched_and_ambiguous.csv` | all 24,341 non-certified rows, 15 columns |
| `join_map.parquet` | all rows including certified, for denominators and for the certified comparison group |
| `record_class_coverage.csv` | per-record and per-class certified coverage, as a cross-check |
| `decision.json` | decision, first stopping reason, gate table, `rule_fingerprint` |
| `manifest.json` | input identity digests, code SHA-256, environment pin |

Before any measurement, record for **each** of the five files: Drive file ID,
byte size, and SHA-256.  These five digests are this diagnostic's input
identity and are written into its own manifest.

## Read (frozen lineage, M1 / M3 / M4 only)

- registered canonical `mamba_data.npz`, SHA-256
  `b1c16106216522cb21291f990e7ab0e7f8dfd8135406db322f41cda3687f6c05`;
- registered V9/V10 preprocessing cache, aggregate `82b9a593…` over 45 files;
- registered MIT-BIH `mitdb-1.0.0` publisher tree, aggregate `0b46a411…`, 147
  files, publisher checksums verified;
- the frozen module `mit-bih/q5d_order_preserving_beat_join.py` at code SHA-256
  `6b098c67…`, imported **read-only** to replay Leg 1 and to reconstruct the
  candidate graph deterministically.

## Sealed — not opened by this diagnostic

- DS2 per-beat class labels;
- V10 probability values and everything under `v10pkg_results/`;
- S PR-AUC and every association statistic;
- P-wave delineation outputs, model checkpoints, training of any kind.

# What the canonical bundle does and does not contain

These are properties of the frozen implementation
(`mit-bih/q5d_order_preserving_beat_join.py`, code SHA-256 `6b098c67…`).  They
are recorded here because they decide which measurements are free reads of the
bundle and which require a deterministic replay under execution approval.

1. **`join_map` row model.**  `join_record()` emits **one row per mamba beat**
   plus **one row per non-certified cache row**.  A certified pair appears once,
   as the mamba row, carrying `cache_record_row` and `result_global_row`.
   `unmatched_and_ambiguous.csv` is exactly the subset with
   `status != CERTIFIED`, over the same 15 columns.
2. **Cache-side rows carry no class and no ordinal.**  On a cache-side row
   `raw_atr_ordinal`, `raw_r_sample`, `mamba_aami`, `mamba_record_row`,
   `mamba_global_row`, `mamba_file_row` are all `None` **by construction**, not
   by data loss.  Consequences, both binding:
   - M2's primary `mamba_record_row` runs and secondary `raw_atr_ordinal`
     sensitivity runs are both **mamba-side** measurements.  Cache-side rows are
     excluded and are **never** imputed into a run by time adjacency or by
     neighbour class.
   - cache-side class may be supplied **only** from the canonical DS1
     processed-class map (`load_cache_classes()`, cache `y`, DS1 audit use is
     already permitted by the parent spec).  A `mamba_aami` of `None` is never
     estimated, and never filled from a certified neighbour.
3. **RR differences exist only for certified rows.**
   `pre_rr_difference_samples` and `post_rr_difference_samples` are `None`
   whenever `cache_record_row is None`, which is every failed row.  **M1 cannot
   be read out of the bundle.**  It requires recomputing both RR sequences under
   the frozen unit contract, which is an execution.
4. **The candidate graph is not in the bundle.**  `MatchResult.edges` and
   `rank_class_sizes` are computed inside `match_record()` and only aggregate
   counts survive into the artifacts.  **M3 requires a deterministic replay** of
   `candidate_edges()` / `match_record()` under the frozen module and the frozen
   inputs.  That replay recomputes the *same* graph; it selects no matching,
   promotes no optimal path, and changes no constant.
5. **Two different "ambiguous" counts exist and must not be conflated.**
   `stratum_report()` counts ambiguous **edges** (`len(result.ambiguous)`; 157
   equal-count + 305 mismatched-count = 462), while
   `LEG2_AMBIGUOUS_RANK_CLASS = 738` counts ambiguous **rows** across both
   sides.  Every M0-M5 table states which of the two it reports.
6. **Detector peak positions are not materialised anywhere the join reads.**
   `load_cache_sequences()` reads only the cache `rr` block (7 columns, seconds,
   pre/post = columns 0/1) and the ledger; no peak sample array is loaded, and
   the mamba lineage does not store `rpks` either
   (`research/PROVENANCE_2026-08-10_mamba_data_lineage.md` §8).  M4 therefore
   cannot read detector positions — it must reproduce them or stop (§M4).
7. **The frozen unit contract.**  Both sides convert to integer samples at
   `FS = 360` with round-half-to-even (`to_samples`).  mamba: `feats[:,4]`,
   `feats[:,5]`, seconds, post-filter, duplicated endpoints.  cache: `rr[:,0]`,
   `rr[:,1]`, seconds, computed on the full matched-peak array before row
   selection, endpoints `nan -> 0.0`.  M1 and M3 use exactly this contract and
   no other.

# Measurements

Every measurement below reports its numerator, its denominator, and its unit.
Every one is additionally stratified per §M5.

## M0 — failure topology of the existing canonical bundle

Inputs: the five bundle files above.  Execution cost is zero; the approval
requirement is not.

**M0.1 — mamba-side per-class failure rate.**
For `c in {N, S, V}`:

```text
numerator   = mamba-side rows with mamba_aami == c and status != CERTIFIED
denominator = mamba-side rows with mamba_aami == c            (all statuses)
```

Mamba-side rows are identified by `mamba_record_row is not None`.  DS1 mamba
rows total 50,576.

**M0.2 — class x failure-reason contingency table.**
Rows `{N, S, V}` (mamba side) and `{N, S, V}` (cache side, class from the
canonical DS1 processed-class map) x columns
`{LEG2_NO_CANDIDATE_EDGE, LEG2_EDGE_IN_NO_MAXIMUM_MATCHING,
LEG2_AMBIGUOUS_RANK_CLASS}`.  Counts and row-wise shares.  Sides reported
separately, never summed into one class total.

**M0.3 — record 208, per class.**
Denominator, failure count and failure rate for N, S, V on the mamba side
(denominator = mamba rows of that class in record 208; mamba `n` = 2,579) and
on the cache side (denominator = processed rows of that class; cache `n` =
2,572).  This replaces the arithmetic argument in
`research/HANDOFF_2026-08-11_Q5D_v_class_join_failure_to_codex.md` §2(a) with a
direct measurement.

**M0.4 — consecutive failure runs over the processed mamba sequence.**
Mamba side only (§What the bundle contains, item 2).  The registered **primary**
adjacency is `mamba_record_row + 1` within one record: a run is a maximal set of
failed rows with exactly consecutive `mamba_record_row` values.  This is the
literal sequence presented to Leg 2, not inferred time adjacency.  Report:

- counts in run-length buckets `1`, `2`, `3-9`, `>=10`;
- median, p90 and maximum run length;
- `share_in_long_runs = (failed rows in runs of length >= 3) / (all mamba-side
  failed rows)`.

Runs never cross a record boundary.  Repeat the same table using exactly
consecutive `raw_atr_ordinal` as the registered **secondary sensitivity audit**.
A raw-ordinal gap ends that secondary run and is never bridged by time
adjacency.  Only the mamba-row primary enters H1/H3 flags; the raw-ordinal
sensitivity result cannot rescue, veto, or replace a primary flag.  The
difference between the two is reported per record, including record 208.

**M0.5 — conditional failure after a failed V beat.**
```text
numerator   = mamba-side rows where the beat at mamba_record_row + 1 in the same
              record exists and is failed, given the current row is failed and
              has mamba_aami == V
denominator = mamba-side failed rows with mamba_aami == V whose
              mamba_record_row + 1 exists in the same record
```
Report the same quantity for N and S as the comparison, and the unconditional
mamba-side failure rate as the reference level.  Repeat using
`raw_atr_ordinal + 1` only as the same non-decisional secondary sensitivity
audit registered in M0.4.

**M0.6 — strata always separated.**
Every M0 table is reported for the 17 equal-count DS1 records and the 5
mismatched-count DS1 records separately, in addition to pooled.  The strata are
reporting strata: neither may be excluded, re-matched, or used to rescue
anything.

## M1 — nearest-candidate distance

Inputs: frozen mamba RR (Leg 1 replay under the frozen module) and frozen cache
RR, both converted by the frozen integer-sample contract.  **No new RR
representation is introduced.**

Population: **non-certified cache rows**, DS1.  The H1 gate population is fixed
more narrowly as cache-side `LEG2_NO_CANDIDATE_EDGE` rows whose processed class
from the canonical DS1 map is V; no symmetric mamba-side distance is substituted.

For cache row `j` in record `r` with `n_m` mamba rows and `n_c` cache rows,
the rank-proportional mamba centre is

```text
c(j) = round_half_even( j * (n_m - 1) / (n_c - 1) )        if n_c > 1
c(j) = 0                                                    if n_c == 1
```

The fixed window half-width is

```text
W = 1 + max over records of abs(mamba_n_r - cache_n_r) = 1 + 14 = 15 rows
```

(the maximum is record 116, `|2411 - 2397| = 14`), so the window is the mamba
rows `[c(j) - W, c(j) + W]` intersected with `[0, n_m - 1]` — at most 31
candidates.  `W` is fixed by the registered ledger, not by any observed
distance.

Distance, in integer samples at 360 Hz:

```text
d_inf(j, i) = max( abs(mamba_pre[i]  - cache_pre[j]),
                   abs(mamba_post[i] - cache_post[j]) )
d_inf(j)    = min over i in the window of d_inf(j, i)
```

Reported bins: `0-1`, `2-5`, `6-20`, `21-100`, `>100` samples.

A row whose minimising `i` lies at `abs(i - c(j)) == W` is flagged
`CENSORED_AT_WINDOW_BOUNDARY`, reported as its own count, and **excluded from
every H1 and H3 determination**.  Censored rows are never treated as if the
window had been wide enough.

A cache row with `pre == 0` or `post == 0` under the frozen cache contract is
flagged `CACHE_ENDPOINT_ZERO`.  It remains in QA, class/reason denominators and
descriptive tables, but is excluded from the M1 distance distribution used by
every H1/H3 null, p-value and effect gate.  The identical exclusion is applied
inside every replicate.  Its count and failure rate are additionally reported
as `H3_ENDPOINT_COMPONENT`; this descriptive component cannot by itself fire H3
and is never folded into the `>100`-sample evidence gate.

**M1 is not a tolerance experiment.**  It is forbidden to report, or to compute,
coverage or match counts under any tolerance other than the frozen 1 sample.

## M2 — failure adjacency and runs

Inputs: `unmatched_and_ambiguous.csv` and `join_map.parquet`, mamba side.

- primary adjacency is exactly consecutive `mamba_record_row` within one record
  (same definition as M0.4);
- runs never cross a record boundary;
- rows with a missing ordinal — which is every cache-side row — are excluded,
  never repaired by time adjacency;
- for every failed mamba-side V beat, report the failure topology of the
  `+/-1 beat` neighbourhood and of the `+/-10 beat` neighbourhood: number of
  neighbours present, number failed, failure share, and the same three for N and
  S as comparison.

Cache-side rows are excluded from runs and are never repaired by time adjacency.
Repeat M2 with raw-ordinal adjacency as a secondary sensitivity audit.  Only the
mamba-row primary contributes to H1/H3 effect gates.  Disagreement is itself
reported per record and does not permit choosing the more favourable result.

## M3 — frozen candidate graph

Inputs: the frozen module at code SHA-256 `6b098c67…`, the frozen tolerance
(1 sample), the frozen matcher, the frozen certification rule, and the frozen
inputs.  The graph is **reconstructed**, not redesigned: `candidate_edges()` and
`match_record()` are called unchanged and must reproduce the bundle's certified,
ambiguous and unmatched partition exactly (this equality is a QA check, §QA).

Per row (both sides, reported separately):

| quantity | definition |
|---|---|
| `candidate_degree` | mamba row `i`: `#{j : (i,j) in E}`; cache row `j`: `#{i : (i,j) in E}` |
| `usable_edges` | edges incident to the row with `L(e) + R(e) - 1 == M` (i.e. lying in **some** maximum monotone matching) |
| `has_forced_rank` | whether any incident usable edge is the sole member of its rank class |
| `rr_pair_multiplicity` | within the record and the same side, `#{k : (pre[k], post[k]) == (pre[row], post[row])}`, integer samples |
| `local_rr_sd` | population standard deviation (`ddof = 0`) of `pre` over rows `[row-10, row+10]` clipped to the record, in integer samples at 360 Hz; a one-row window has SD 0 |

Compared across the four groups `CERTIFIED`, `NO_EDGE`, `NOT_OPTIMAL`,
`AMBIGUOUS`.  Report median, p25, p75, and the full ECDF per group.

On the cache side, construct `CERTIFIED` from the non-null `cache_record_row` on
each certified mamba row.  Create exactly one cache-side row per certified pair,
attach class only from the frozen DS1 processed-class map, and assert uniqueness
of `(record, cache_record_row)` plus equality with the certified-pair count.
Together, the four cache-side groups must form a disjoint, exhaustive partition
of cache rows.  Any collision, duplicate, omission or count mismatch is
`DIAGNOSTIC_INPUT_MISMATCH`.

**Nothing is selected.**  No new matching is chosen, no arbitrary maximum path
is promoted to truth, no edge is re-certified.  This measurement observes the
graph the frozen rule already built.

## M4 — detector / source discordance anchors

Inputs: the registered DS1 raw MIT-BIH tree and the frozen lineage source only.

### PREP_M4_ASSET_FREEZE — approval blocker, not a measurement

M4 is retained because omitting it would make H2 and H3 structurally
unevaluable and prevent a complete four-hypothesis verdict.  Before this spec
may be promoted from `draft`, a separate read-only preflight must:

1. uniquely identify the canonical V9/V10 source packages and cache trees by
   Drive file/folder ID, path, byte size and SHA-256 (tree digest for a folder);
2. freeze the exact `detect_r()` producer, annotation-matching source and runtime;
3. reproduce the registered row count for every one of the 44 cache records in
   both V9 and V10 (44/44 per version),
   without opening V10 probability values or DS2 per-beat class labels; and
4. record the resulting identities in `research/ASSETS.md` and this Decision log
   before implementation approval.

If the canonical producer cannot be identified uniquely, a required hash is
unverifiable, or deterministic replay does not reproduce all 44 counts, the
preflight ends `M4_INPUT_FREEZE_FAILED`.  The spec stays `draft`; no detector,
version, tolerance or source is substituted.  This preflight performs no M0-M4
aggregation and does not itself authorize implementation or execution.

### M4.0 — feasibility gate, evaluated first

All three must hold:

1. a source exists that reproduces the original run's `detect_r()` and its
   annotation matching **exactly** (the `v10pkg`/`v9pkg` `kinkmap` package: the
   `detect_r()` call, `tol = int(0.15 * fs)`, the greedy nearest `used`-set
   matching, and the `p-150 >= 0` / `p+150 <= len` boundary cut);
2. the required detector peak positions are obtainable **deterministically** —
   note that neither lineage stores them (§What the bundle contains, item 6), so
   this requires re-running the detector under the registered runtime
   (`numpy 2.5.1`, `scipy 1.18.0`, `wfdb 4.3.1`, CPython 3.12.3), whose output
   must be shown to reproduce the registered per-record cache counts before any
   anchor is used;
3. the source version, cache tree and hashes equal the identities frozen by
   `PREP_M4_ASSET_FREEZE`.  A path or filename without its registered digest is
   insufficient.

If any of the three fails:

```text
M4 = DIAGNOSTIC_INPUT_ABSENT
```

and M4 stops.  **Drop positions are then not inferred from row-count
differences.**  A `-25` DS1 total deficit is a count, not a location; treating it
as one is explicitly forbidden.

### M4.1 — anchors and post-anchor topology

If the gate passes, reproduce the source's own rule to identify
detector-annotation **discordance anchors**: annotation positions with no
matched detector peak within the source's own `+/-54 sample` tolerance, and
detector peaks matched to no annotation, each in the source's own order.

For H2 positional explanation, an annotation-without-peak anchor maps to its
exact kept mamba row when the frozen Leg 1 replay kept that annotation; a
detector-without-annotation anchor maps to its exact cache row when the frozen
cache selection kept that peak.  An anchor whose counterpart-side row was not
kept is reported but contributes nothing to the H2 explanatory numerator.

For H3 topology, place each anchor at its unique sample-ordered boundary in the
kept mamba sequence.  An exact kept annotation is offset 0; otherwise offset +1
is the first kept row strictly after the anchor and offset -1 is the last kept
row strictly before it.  Measure 10 kept beats on either side over
`mamba_record_row`.  Report failure share per offset `-10 … +10` (offset 0 is NA
for an inter-row anchor), and the share of all failures within 10 kept beats
after an anchor.  A non-unique placement is reported and excluded, never
imputed.  Repeat raw-ordinal topology as a secondary sensitivity audit, but only
the mamba-row primary enters H2/H3 gates.

**No new detector, no new peak-matching tolerance, and no manual anchor may be
introduced.**  If the original rule cannot be reproduced, the answer is
`DIAGNOSTIC_INPUT_ABSENT`, not an approximation.

## M5 — fixed strata for every result

Every M0-M4 result is reported simultaneously by:

- class `N` / `S` / `V` (side stated);
- failure-reason bucket `NO_EDGE` / `NOT_OPTIMAL` / `AMBIGUOUS`;
- record;
- `equal_count` (17 DS1 records) / `mismatched_count` (5 DS1 records);
- records `116` and `208` individually;
- pooled.

**A mechanism is never declared from the pooled value alone.**  The pooled row
exists so a stratified claim can be compared against it, not so it can stand
alone.

# Runtime and execution-environment contract

Engineering only.  Nothing in this section changes a scientific rule; every
item exists because Q5-D lost runs to exactly these failure modes and closed
them in its own module.  A Q5-E implementation reproduces the same closures
rather than rediscovering them.

## Stage dependencies, declared before the work

Follow `RUNTIME_DEPENDENCIES` / `STAGE_REQUIREMENTS` /
`assert_runtime_ready()` in the frozen module.  A stage refuses to start when
its imports are absent, naming the exact `pip install` line, **before** anything
is read.

| stage | needs | why |
|---|---|---|
| M0 (bundle only) | `numpy`, `pyarrow` | `join_map.parquet` |
| M0 (cache-side class) | + registered cache access | `load_cache_classes()` on DS1 `y` |
| M1, M3 | + `wfdb` | Leg 1 replay from raw `.atr` |
| M4 | + `scipy` at the registered version | `detect_r()` reproduction |

`pyarrow` is declared **up front**, not at write time.  Q5-D recorded the same
rule after finding that a missing `pyarrow` would have discarded a completed
run at the bundle-writing step.

## Registered-input access is opt-in and re-verified

- A Q5-E run opens no registered artifact without an explicit execution
  approval flag, default off, mirroring Q5-D's `OPEN_REGISTERED_DATA` and
  `require_execution_approval()`.
- Before M1, M3 or M4 opens `mamba_data.npz`, the V9/V10 cache or the MIT-BIH
  tree, the run re-verifies their identity by reusing the frozen module's
  `build_preflight()` and `verify_preflight_freeze()` against the registered
  digests (`b1c16106…`, `82b9a593…`, `0b46a411…`).  Analysing a different copy
  of an artifact than the canonical run consumed is a contamination path, and
  a preflight already exists to close it.
- The canonical bundle is additionally checked for the **absence** of
  `SUPERSEDED.json` and for `manifest.json` carrying code SHA-256
  `6b098c67…`.  Path alone never establishes canonicity.

## Staleness and silent-skip guards

- The notebook asserts the **capabilities it actually uses** on both modules
  (the Q5-E module and the frozen Q5-D module) and prints both `__file__`
  paths.  A version integer alone is defeated by forgetting to bump it; Q5-D
  lost three Colab runs to a stale clone and to `import` returning the
  `sys.modules` cache.
- Every stage announces `RUN` or `SKIP` with its reason through a single
  helper, as in Q5-D's `stage_should_run()`.  A stage that quietly does nothing
  must never be indistinguishable from a stage that passed.

## Cost profile

The controls here permute an already-measured 24,341-row failure table; they do
**not** rerun the matcher.  Expected costs, from the frozen module's measured
behaviour:

| stage | expected cost |
|---|---|
| M0 | seconds |
| M1 | seconds — at most 31 candidates per non-certified cache row |
| M3 | ~2 s for the whole DS1 graph replay (one complete Leg 2 join measured at ~1.7 s) |
| M4 | minutes, dominated by re-running `detect_r()` over 22 records |
| controls A/B/C, 3 x 10,000 | minutes |

Peak memory stays small: `load_mamba_sequences()` reads only `feats` (26 columns)
and `pid` from the 204 MB npz, never `beat` or `ref`.

**Therefore no null sharding, no resume directory and no cross-session
checkpointing are required.**  Q5-D needed them because each of its 30,000
replicates reran a complete Leg 2 join; Q5-E's do not.  If an implementation
finds itself rerunning the matcher inside a replicate loop, that is a defect in
the implementation, not a reason to shard.

## Output writing

One new timestamped directory.  Nothing existing is written to, moved or
removed, and a failed or stopped run still preserves its bundle so a STOP is as
inspectable as a PASS.

# Resolved design decisions — Codex, 2026-08-11

These decisions are frozen before any M0-M4 aggregation.  They resolve every
implementation-dependent denominator or statistic surfaced in PR #100.

## Q1 — processed-sequence adjacency is primary

**Decision.**  Use `mamba_record_row` adjacency as primary for M0.4, M0.5, M2
and every H1/H3 run-related gate.  Use `raw_atr_ordinal` only as a registered,
non-decisional secondary sensitivity audit.  Both are reported, but the
secondary cannot rescue, veto or replace a primary flag.

**The fact.**  `replay_leg1_record()` assigns `raw_atr_ordinal` by enumerating
**all** `.atr` annotations, including the ones the three frozen rules then drop.
So two beats that are *adjacent in the processed sequence* have consecutive raw
ordinals only when no annotation was dropped between them.  F and Q symbols are
never in the AAMI map — that is the entire 818-beat Q5-B-0 drop map, `F 802`,
92% of it concentrated in records **208** and 213.

**The consequence of the rejected definition.**  If a run is defined as
exactly consecutive `raw_atr_ordinal`, every dropped F beat between two failed
beats **splits a run in two**.  The suppression is multiplicative in run length and differs by
record: with a drop rate `d` between neighbours, the surviving mass of a
length-`L` run falls as roughly `(1-d)^(L-1)`.  Record 208's raw stream is
F-dense, while a record such as 101 is nearly F-free — so long runs are
suppressed hardest **in the one DS1 record whose 84.3% collapse motivates the
whole diagnostic**, and barely at all elsewhere.

**Why it matters for the verdict, not just for tidiness.**  `share_in_long_runs`
and "the majority of run mass is at length <= 2" are literal inputs to
`H1_ASSOCIATED`, and "`>= 0.50` of explained failures lie in runs of length
`>= 3`" is a literal input to `H3_ASSOCIATED`.  The artifact pushes both in the
same direction: **toward H1 and away from H3**, strongest in record 208.  A
differential, hypothesis-aligned bias in a registered gate input is not an
acceptable unknown.

**Rejected alternative.**  Keeping raw-ordinal adjacency primary and adding
`mamba_record_row` only as secondary would retain a known hypothesis-aligned
bias in the decisive statistic.  `mamba_record_row` is reported as the primary.
`mamba_record_row` is already carried in `join_map` and gives exact
processed-sequence adjacency with no gaps.  Note that this is **not** the
forbidden repair: the ban is on treating a missing ordinal as adjacent *in
time*, whereas `mamba_record_row + 1` is the literal next row of the sequence
the join operates on.  It is also arguably the adjacency the hypotheses are
about — H1's `e_j - e_{j-1}` and H3's endpoint/filter semantics both act between
**consecutive kept beats**, not between consecutive annotations.  Reporting both
makes the size of the artifact measurable instead of invisible.

## Q2 — Control B is one joint categorical permutation

**Decision.**  Within each `record x side`, jointly permute one categorical
label vector with the exact multiset `{NO_EDGE x a, NOT_OPTIMAL x b, AMBIGUOUS
x c, CERTIFIED x rest}`.  Never permute failure reasons independently.

Control B preserves failure counts per `record x side x failure-reason` and
permutes positions.  Applying an independent permutation per reason lets two
reasons land on the same row.  The registered construction is a **single joint
permutation** of the position pool within `record x side`, to
which the multiset of labels (`NO_EDGE` x a, `NOT_OPTIMAL` x b, `AMBIGUOUS` x c,
`CERTIFIED` x rest) is then assigned — which preserves every per-reason count
and cannot collide.  This must be stated, not inferred: it is the difference
between a valid null and an ill-defined one, and an implementer forced to guess
is an implementer contaminating the design.

## Q3 — Holm remains a four-family procedure when M4 is unavailable

**Decision.**  The family is always H1-H4.  When M4 is unavailable, H2 and H3
remain explicitly `UNEVALUABLE`; assign each p=1.0 only inside the Holm
calculation.  Report raw H1/H4 p-values and `p_holm_4family`, never a two-family
adjusted p-value.  The placeholders are not evidence of no association.

This conservative convention prevents the multiplicity family from changing
conditionally after M4 feasibility is known.  Partial results are not promoted
to a verdict, regardless of their adjusted values.

## Q4 — cache-side `CERTIFIED` is derived one-to-one

**Decision.**  Derive exactly one cache-side certified row from each certified
mamba row's non-null `cache_record_row`, subject to the uniqueness, class and
partition assertions in M3.

A certified pair appears in `join_map` **once**, as the mamba row.  There is
therefore no cache-side row carrying `status = CERTIFIED`.  M3 compares four
groups per side, and Control B strata are `record x side`, so the cache-side
certified group is derived from `cache_record_row` on certified mamba rows under
the exact assertions registered in M3.

## Q5 — stored zero endpoints are descriptive, not distance evidence

**Decision.**  Flag them `CACHE_ENDPOINT_ZERO`, retain them in QA and ordinary
denominators, report them as `H3_ENDPOINT_COMPONENT`, and exclude them from all
observed and null H1/H3 distance statistics and effect gates.

`rr_features` writes `nan -> 0.0` at record endpoints, so the first and last
cache row of every record carries a real stored `0.0` — data meaning "no
neighbour", not a missing value.  Their `d_inf` is necessarily on the order of a
full RR interval, which lands them in the `>100 samples` bin: the exact bin H3's
distance condition reads.  The population is small (2 rows x 22 DS1 records = 44
of 12,158 non-certified cache rows, and fewer after certification), so this is
hygiene rather than a threat — they are flagged
`CACHE_ENDPOINT_ZERO`, counted separately, and excluded from the H3 distance
condition, for the same reason censored rows are.

## Additional resolution — M4 retained with a pre-approval asset freeze

Do not intentionally collapse the experiment to H1/H4.  Complete the read-only
`PREP_M4_ASSET_FREEZE` before promoting this spec.  Failure to uniquely freeze
the original producer/cache lineage and reproduce all 44 cache record counts in
each version is
`M4_INPUT_FREEZE_FAILED`; the spec stays `draft` and no substitute source or
relaxed rule is allowed.  If an approved implementation later fails exact peak
replay, decision-tree branch 2 remains the registered result.

The proposed null seed **`2026019`** is accepted.  The proposed `local_rr_sd`
formula is accepted with `ddof = 0`, clipped record boundaries and SD 0 for a
one-row window.  The H1 distance population reading is accepted: non-certified
cache-side `NO_EDGE` rows, V from the frozen DS1 processed-class map, subject to
the registered censoring and endpoint exclusions.

# Negative controls and null computation

Three controls, each **10,000 replicates**, master seed **`2026019`**, drawn per
`(control, replicate)` so replicate `b` is the same value on any machine, in any
order, on any worker count.  Each replicate recomputes the **complete statistic**
of its family from the permuted arrangement; nothing is approximated and no
family is omitted.

| control | what is permuted | what is preserved | what it falsifies |
|---|---|---|---|
| **A** — within-record class circular shift | the per-record class sequence is circularly shifted by a non-zero offset drawn uniformly from `1 … n-1` | per-record class composition, per-record failure count, the entire failure run structure | "the V association is only record composition plus record 208's weight" |
| **B** — within-record joint status permutation | one joint categorical vector `{NO_EDGE, NOT_OPTIMAL, AMBIGUOUS, CERTIFIED}` is permuted within each `record x side`; exactly one status is assigned per row | per-record, per-side and per-reason counts, with no collisions | "the observed long runs and graph-group contrasts arose by chance within the same record and side" |
| **C** — discordance-anchor circular shift | anchor positions are circularly shifted within record | per-record anchor count and the whole failure topology | "post-anchor failure propagation is chance positional overlap" |

Control C is available **only** when M4.0 passes.  When it does not, every
statistic whose null is Control C is reported as unevaluable, not as
non-significant.

Permutation p-value for every registered statistic:

```text
p = (1 + number of replicates whose null statistic >= the observed statistic)
    / (10000 + 1)
```

The `q99` referenced by the effect-size gates is the 99th percentile of the same
10,000-replicate null distribution of that statistic.

# Multiplicity

Four hypothesis families, one family-level p-value each:

| family | statistic | null |
|---|---|---|
| H1 | share of `2-5` sample `d_inf` among uncensored failed V / `NO_EDGE` rows, relative to the same share in non-V | Control A |
| H2 | share of `NO_EDGE` failures positionally explained by replay-confirmed counterpart absence | Control C |
| H3 | share of failures within 10 beats after a replay-confirmed anchor | Control C |
| H4 | `median(candidate_degree \| NOT_OPTIMAL + AMBIGUOUS) - median(candidate_degree \| CERTIFIED)` | Control B |

**Holm** correction across exactly these four, at `alpha = 0.05`: sort the four
p-values ascending and require `p_(k) <= 0.05 / (4 - k + 1)`, stopping at the
first failure.  If M4 is unavailable, H2/H3 are labelled `UNEVALUABLE` and each
is assigned p=1.0 only for this four-family adjustment.  Report the field as
`p_holm_4family`; a two-family adjustment is forbidden.

A p-value alone never promotes a mechanism.  A flag fires only when its
Holm-adjusted family p-value is significant **and** every effect-size condition
below holds.

# Preregistered association flags

Each flag is evaluated **independently**.  All conditions of a flag must hold.

**`H1_ASSOCIATED`** — all of:
- among uncensored, non-`CACHE_ENDPOINT_ZERO`, cache-side failed V rows with
  reason `NO_EDGE`, the share with
  `d_inf` in `2-5` samples is `>= 0.50`;
- the V-by-distance-bucket association exceeds Control A's `q99`;
- the majority of the primary mamba-row run-length mass is at length `<= 2`;
- the M4 propagation gate (H3's post-anchor condition) is **not** met;
- Holm-adjusted H1 p-value significant.

**`H2_ASSOCIATED`** — all of:
- replay-confirmed counterpart absence explains `>= 0.50` of `NO_EDGE`
  failures **at the position level**;
- exceeds Control C's `q99`;
- Holm-adjusted H2 p-value significant.
- Total row-count differences are **excluded from the explanatory numerator**.
  A record's `-7` deficit explains seven positions only if those seven positions
  are identified by replay.

**`H3_ASSOCIATED`** — all of:
- failure concentration within 10 beats after a replay-confirmed discordance
  anchor exceeds Control C's `q99`;
- `>= 0.50` of the explained failures lie in primary mamba-row runs of length
  `>= 3`;
- after excluding censored and `CACHE_ENDPOINT_ZERO` rows, the distance
  distribution places more mass in `21-100` or `>100` samples than in `2-5`
  samples;
- Holm-adjusted H3 p-value significant.

**`H4_ASSOCIATED`** — all of:
- among `NOT_OPTIMAL` and `AMBIGUOUS` rows, the share with
  `candidate_degree >= 2` is `>= 0.50`;
- the candidate-degree effect versus certified rows exceeds Control B's `q99`;
- the direction of `rr_pair_multiplicity` (higher in failed rows) **or**
  `local_rr_sd` (lower in failed rows) agrees;
- Holm-adjusted H4 p-value significant.

# Decision tree

Evaluated in order; exactly one branch is reached.

1. **`DIAGNOSTIC_INPUT_MISMATCH`** — any QA reproduction target in §QA fails,
   canonical and superseded bundles cannot be told apart, or any registered
   canonical-bundle/M0-M3 input hash is unknown.  **STOP.**  No measurement is
   reported.  M4-specific assets are governed first by the pre-approval freeze
   and then by branch 2, not silently reclassified here.
2. **`MECHANISM_UNRESOLVED_INPUT_ABSENT`** — QA passes but M4.0 fails, so H2 and
   H3 cannot be evaluated.  M0-M3 are reported as **diagnostic partial results**;
   `H1_ASSOCIATED` and `H4_ASSOCIATED` may be computed and reported but are
   **not** promoted to a terminal mechanism verdict.  Their reported adjustment
   is the registered four-family Holm value with H2/H3 p=1 placeholders.
3. **`MULTI_MECHANISM_ASSOCIATED`** — all four flags evaluable and **two or more**
   fire.  Report every flag that fired, with its statistics; do not rank them.
4. **`H1_ASSOCIATED` / `H2_ASSOCIATED` / `H3_ASSOCIATED` / `H4_ASSOCIATED`** —
   all four flags evaluable and **exactly one** fires.
5. **`NO_REGISTERED_MECHANISM_ASSOCIATED`** — all four flags evaluable and
   **none** fires.  This is a valid, complete, publishable result: the four
   preregistered mechanisms do not account for the observed failure topology
   under their registered criteria.  It is never rewritten into a weaker version
   of a flag, and no post-hoc mechanism is added to fill it.

Branch 5 is mandatory and must survive into the implementation: an audit with no
"nothing was confirmed" outcome is not an audit.

# QA and stopping conditions

## Reproduction targets, checked before any measurement

| target | required value |
|---|---|
| total failure rows | 24,341 |
| mamba-side failure rows | 12,183 |
| cache-side failure rows | 12,158 |
| `LEG2_NO_CANDIDATE_EDGE` | 13,716 |
| `LEG2_EDGE_IN_NO_MAXIMUM_MATCHING` | 9,887 |
| `LEG2_AMBIGUOUS_RANK_CLASS` | 738 |
| DS1 records | 22 |
| `rule_fingerprint` | `31c4be9f44582a68c301fe6cc6572f4db6ff0b3de694af68f6ac6a0f48c2b40e` |
| producing module code SHA-256 | `6b098c67df3c8e2c8c070b093e6e2d801566f548a3173626745c4a126a97f226` |

Additionally, before M3 is used: the reconstructed candidate graph must
reproduce the bundle's `CERTIFIED` / `AMBIGUOUS` / `UNMATCHED` partition and the
three reason counts **exactly**.

Any single mismatch: `DIAGNOSTIC_INPUT_MISMATCH`, **STOP**.

## Further stopping conditions

- canonical and superseded run bundles cannot be distinguished;
- a registered canonical-bundle or M0-M3 source hash is unknown or unverifiable;
- M4 detector replay is impossible (`DIAGNOSTIC_INPUT_ABSENT`; the diagnostic
  continues into branch 2, it does not guess drop positions);
- progress would require opening DS2 labels or V10 probabilities — **STOP**, the
  seal is not negotiable;
- progress would require changing any join rule constant — **STOP**.  A
  diagnostic that must modify the thing it observes has left its own scope.

# What this diagnostic does not license

Registering an association here authorizes **none** of the following, whatever
the result:

- widening the RR tolerance, or selecting any new tolerance;
- re-optimising join coverage by any means;
- excluding class V;
- excluding record 116, record 208, or the mismatched-count stratum;
- reordering, reweighting or reinterpreting the Q5-D gates;
- approving any new join rule by reusing the existing null.  A new rule requires
  its own preregistration, its own `rule_fingerprint`, its own negative-control
  null, and its own user approval — `assert_null_matches_rule()` enforces the
  first three structurally;
- opening DS2 per-beat labels;
- opening V10 probabilities;
- running the association analysis;
- computing S PR-AUC;
- training or retraining any model;
- modifying, deleting or overwriting any existing Drive bundle, canonical or
  superseded;
- writing the word **cause** about any observed association.

Confirming a mechanism association does **not** rescue Q5-D.  `JOIN_UNRESOLVED`
stands until a separately preregistered rule passes its own gates.

# Visualization plan

Seven figures.  **All titles, axis labels, tick labels and legends are ASCII**;
no Korean, no typographic dashes, no unit glyphs.

| # | figure | content |
|---|---|---|
| 1 | class x failure reason, stacked bar | x = class (N, S, V), stack = reason; one panel per side |
| 2 | per-record class failure-rate heatmap | rows = 22 DS1 records, columns = N/S/V, cell = failure rate; strata annotated |
| 3 | record 208 failure raster | primary x = `mamba_record_row`, one row per class, mark = failed beat; raw-ordinal sensitivity shown separately |
| 4 | run-length distribution | primary mamba-row histogram over buckets `1`, `2`, `3-9`, `>=10`, plus median/p90/max; raw-ordinal sensitivity overlaid or panelled |
| 5 | nearest-distance histogram | fixed bins `0-1`, `2-5`, `6-20`, `21-100`, `>100`; censored and `CACHE_ENDPOINT_ZERO` rows in separate descriptive bars |
| 6 | candidate-degree violin + ECDF | groups CERTIFIED / NO_EDGE / NOT_OPTIMAL / AMBIGUOUS |
| 7 | anchor-aligned failure probability curve | x = beat offset `-10 … +10` from anchor, y = failure share, with the Control C band |

Figure 7 is produced only when M4.0 passes; otherwise the bundle records its
absence and the reason.

# Machine-readable result schema

`q5e_result.json`:

```json
{
  "experiment_id": "EXP-2026-008",
  "substage": "Q5E_LEG2_FAILURE_MECHANISM_AUDIT",
  "analysis_only": true,
  "training_performed": false,
  "model_scored": false,
  "v10_probability_opened": false,
  "ds2_labels_opened": false,
  "association_performed": false,
  "source_bundle": {
    "run": "20260811T035108_EXP-2026-007_q5d_beat_join_DS1_GATE",
    "folder_id": "1JjwBhU8BXf8lRrYPcM2UjFNdIKxE9Ghd",
    "producing_code_sha256": "6b098c67...",
    "rule_fingerprint": "31c4be9f...",
    "files": [{"name": "", "file_id": "", "bytes": 0, "sha256": ""}]
  },
  "qa": {"targets": {"": {"expected": 0, "observed": 0, "ok": true}},
         "graph_partition_reproduced": true, "ok": true},
  "m0": {"class_failure_rate": {}, "class_by_reason": {},
         "record_208": {}, "runs_primary_mamba_row": {},
         "runs_secondary_raw_ordinal": {}, "post_v_failure": {}, "strata": {}},
  "m1": {"bins": {}, "censored": 0, "cache_endpoint_zero": 0,
         "h3_endpoint_component": {}, "window_half_width": 15},
  "m2": {"adjacency_primary": "mamba_record_row",
         "runs": {}, "raw_ordinal_sensitivity": {},
         "v_neighbourhood_pm1": {}, "v_neighbourhood_pm10": {}},
  "m3": {"by_group": {}},
  "m4": {"status": "OK | DIAGNOSTIC_INPUT_ABSENT", "feasibility": {},
         "anchors": 0, "offset_curve": {}},
  "m5": {"strata_present": ["class", "reason", "record",
                            "count_stratum", "record_116", "record_208",
                            "pooled"]},
  "null": {"replicates": 10000, "master_seed": 2026019,
           "controls": {"A": {}, "B": {}, "C": {}}},
  "tests": {"H1": {"statistic": 0.0, "p": 0.0, "p_holm_4family": 0.0, "q99": 0.0,
                   "effect_gates": {}, "flag": false},
            "H2": {}, "H3": {}, "H4": {}},
  "decision": "H1_ASSOCIATED | H2_ASSOCIATED | H3_ASSOCIATED | H4_ASSOCIATED | MULTI_MECHANISM_ASSOCIATED | NO_REGISTERED_MECHANISM_ASSOCIATED | MECHANISM_UNRESOLVED_INPUT_ABSENT | DIAGNOSTIC_INPUT_MISMATCH",
  "first_stopping_reason": null,
  "language_boundary": "association_only_no_causal_claim"
}
```

Accompanying tabular outputs, all with an explicit header row and ASCII column
names:

- `m0_class_by_reason.csv` — `side, class, reason, count, denominator, rate`
- `m0_record_class.csv` — `record, stratum, class, side, denominator, failures, rate`
- `m0_runs.csv` — `record, adjacency_definition, run_start, run_length, classes, reasons, decisional`
- `m1_distance.csv` — `record, cache_record_row, processed_class, reason, d_inf, bin, censored, cache_endpoint_zero, included_in_distance_gate`
- `m3_graph.csv` — `record, side, row, group, candidate_degree, usable_edges, has_forced_rank, rr_pair_multiplicity, local_rr_sd`
- `m4_anchors.csv` — `record, anchor_ordinal, anchor_sample, anchor_kind, adjacency_definition, offset, mapped_mamba_record_row, failed, decisional` (absent when M4 stops)
- `null_summary.json` — per control, per statistic: full quantiles, `q95`, `q99`, seed, replicate count

# Inputs and outputs contract for a future approved implementation

## Files allowed to change

During the current design task, **only this file**.  A later, separately
approved `PREP_M4_ASSET_FREEZE` intake may change only `research/ASSETS.md` and
this spec's checklist/Decision log; it may not add analysis code or outputs.

After the completed design approval (step 3), implementation is limited to:

- this spec's `status`, checklist and Decision log;
- `mit-bih/q5e_leg2_failure_mechanism_audit.py`;
- `mit-bih/test_q5e_leg2_failure_mechanism_audit.py`;
- `notebooks/quest55_q5e_leg2_failure_mechanism_audit.ipynb`.

Explicitly **not** modifiable, at any step:

- `mit-bih/q5d_order_preserving_beat_join.py` and its tests — the frozen module
  is imported read-only;
- any existing null shard;
- any canonical or superseded run bundle;
- `mit-bih/q5d_qualify_*`, `notebooks/quest53_*`, `research/PLAN_2026-08-10_*`.

## Future Drive run directory

`MyDrive/MedKOS/ecg-model/runs/<timestamp>_EXP-2026-008_q5e_leg2_failure_mechanism_audit/`

A new timestamped directory.  No existing bundle is written to, moved, or
removed.

Required outputs: `config.json`, `manifest.json`, `q5e_result.json`, the six
CSVs above, `null_summary.json`, the seven figures, `log.txt`, `summary.md`.

# Approval boundary

**This step:** write this spec and open the PR.  `status` stays `draft`.  No
code, no notebook, no Drive per-beat analysis, no M0 aggregation, no raw ECG or
detector execution.  After the PR, **STOP** and wait for the user.

**Everything after is separate and sequential:**

1. user approves the read-only M4 asset-freeze preflight;
2. Claude performs only that preflight and records its identities;
3. Codex accepts the preflight and the user approves the completed spec;
4. Claude Code opens an implementation PR (code only, not executed);
5. user separately approves execution;
6. M0-M4 run;
7. a new timestamped Drive bundle is written;
8. the executed notebook is committed and the run ingested;
9. Codex performs result acceptance.

# Implementation checklist

- [x] Codex resolves the five open design questions (Q1-Q5)
- [ ] User approves the read-only `PREP_M4_ASSET_FREEZE` scope
- [ ] `PREP_M4_ASSET_FREEZE` uniquely freezes source/cache identities and
      reproduces all 44 cache record counts in each version before status promotion
- [ ] User approves this draft; `status` becomes `approved_for_implementation`
- [ ] Claude implements the frozen design without executing it
- [ ] User separately approves execution on the registered artifacts
- [ ] Bundle file IDs, byte sizes and SHA-256 recorded before any measurement
- [ ] QA reproduction targets all match, or `DIAGNOSTIC_INPUT_MISMATCH`
- [ ] M3 graph reconstruction reproduces the bundle partition exactly
- [ ] M4 feasibility gate evaluated before any anchor is used
- [ ] The complete M0-M4 plan is unchanged from this document at run time
- [ ] All three controls run at 10,000 replicates under seed `2026019`
- [ ] Control B uses one joint categorical permutation per `record x side`
- [ ] Holm correction applied across exactly four families; unavailable H2/H3
      use p=1 only inside `p_holm_4family`
- [ ] Primary runs/neighbourhoods use `mamba_record_row`; raw ordinal is
      non-decisional sensitivity only
- [ ] `CACHE_ENDPOINT_ZERO` excluded identically from observed/null distance gates
- [ ] Cache-side `CERTIFIED` partition assertions pass exactly
- [ ] `NO_REGISTERED_MECHANISM_ASSOCIATED` reachable and tested
- [ ] No DS2 label, V10 probability, association, or training at any point
- [ ] No existing Drive bundle or null shard modified
- [ ] No causal language anywhere in the outputs

# Decision log

- 2026-08-11 — **Transcription (Claude Code).  Codex's design, copied from the
  user's transfer message; Claude changed no scientific rule.**

  The design in this file — the single fixed question, the four competing
  hypotheses and their distinguishing predictions, the M0-M5 measurement plan,
  the window `W = 15`, the distance definition `d_inf`, the censoring rule, the
  reporting bins, the three negative controls with 10,000 replicates, the
  permutation p-value formula, Holm across four families, every effect-size
  gate, the decision tree including the mandatory
  `NO_REGISTERED_MECHANISM_ASSOCIATED` branch, the QA reproduction targets, the
  stopping conditions, the licence exclusions, and the approval boundary — is
  **Codex's**, transcribed from the user's transfer message.  Claude Code did
  not alter the scientific question, any threshold, any window, any denominator,
  any control, the multiplicity handling, or any stopping rule.  The language
  boundary is kept at "associated mechanism" / "failure-associated factor"
  exactly as Codex directed; the word "cause" appears in this file only where it
  is forbidden.

  *ID.*  `EXP-2026-008` was verified free on `main` and in the working tree
  before use; no other number was substituted.

  *Two values the transfer message did not supply, registered here and open to
  Codex correction before approval.*  Neither changes a scientific rule; both
  are values a preregistration cannot omit.

  1. **Null master seed `2026019`.**  The transfer message registers "10,000
     replicates, fixed seed" without a value.  `2026019` continues the repo's
     existing sequence (`MASTER_SEED = 2026017`, `BOOTSTRAP_SEED = 2026018` in
     `mit-bih/q5d_order_preserving_beat_join.py`) and is distinct from both, so
     no Q5-E null can be confused with a Q5-D null.
  2. **`local_rr_sd`.**  M3 registers "local RR variability" without a formula.
     Fixed here as the population standard deviation of `pre` over rows
     `[row-10, row+10]` clipped to the record, in integer samples — the same
     `+/-10 beat` neighbourhood the transfer message already registers for M2
     and M4, so the diagnostic uses one locality scale rather than two.

  *One reading recorded rather than assumed.*  M1 is registered on cache rows
  ("each cache row's rank-proportional mamba centre"), while the `H1_ASSOCIATED`
  gate speaks of "failed V / `NO_EDGE` rows".  Since `d_inf` exists only for the
  M1 population, the gate population is taken to be **non-certified cache rows
  with reason `LEG2_NO_CANDIDATE_EDGE` whose processed class is V**, class
  supplied solely by the canonical DS1 processed-class map as the transfer
  message requires.  The symmetric mamba-side distance is **not** registered and
  must not be substituted.  Codex may correct this reading before approval.

  *Implementation facts folded in, as the user asked, from reading the frozen
  Q5-D module (`mit-bih/q5d_order_preserving_beat_join.py`, code SHA-256
  `6b098c67…`).*  These are properties of the artifact, not design changes, and
  they are what §"What the canonical bundle does and does not contain" records:

  - `join_record()` emits one row per mamba beat plus one row per non-certified
    cache row, so `unmatched_and_ambiguous.csv` is the `status != CERTIFIED`
    subset over the same 15 `JOIN_MAP_FIELDS`;
  - cache-side rows carry `raw_atr_ordinal = None` **by construction**.  M2's
    ordinal-based runs are therefore a mamba-side measurement, which is exactly
    consistent with the instruction not to repair missing ordinals by time
    adjacency — the spec now says so explicitly rather than leaving an
    implementer to discover it;
  - `pre_rr_difference_samples` / `post_rr_difference_samples` are `None` on
    every failed row, so **M1 cannot be read out of the bundle** and needs the
    frozen RR contract recomputed.  M1 is a step-4 measurement, not a free read;
  - `MatchResult.edges` and `rank_class_sizes` never reach the bundle, so **M3
    requires a deterministic replay** of `candidate_edges()` / `match_record()`
    under the frozen module.  A QA equality — the replayed partition must
    reproduce the bundle's certified/ambiguous/unmatched split and the three
    reason counts exactly — is registered so the replay cannot silently drift;
  - `stratum_report()`'s `ambiguous` counts **edges** (157 + 305 = 462) while
    `LEG2_AMBIGUOUS_RANK_CLASS = 738` counts **rows**.  Conflating them would
    have produced a false discrepancy in M0.2, so every table states which it
    reports;
  - neither lineage materialises detector peak positions
    (`load_cache_sequences()` reads only the cache `rr` block; the mamba lineage
    does not store `rpks`), and `research/ASSETS.md` records "hash 미계산" for
    both `baseline-v9-source` and `baseline-v10-source`.  M4's feasibility gate
    is therefore a real gate with a real chance of firing, and freezing those
    hashes is named as its prerequisite.

  *What this transcription did not do.*  No code was written or modified, no
  notebook was created or edited, no Drive artifact was read, downloaded,
  written or analysed, no `unmatched_and_ambiguous.csv` or `join_map.parquet`
  aggregation was computed, no raw ECG or detector was run, no DS2 label or V10
  probability was opened, no association or training occurred, and no join rule
  constant was changed.  `mit-bih/q5d_order_preserving_beat_join.py` was read
  and not modified.  The change set is this one new file.

- 2026-08-11 — **Pre-merge review of the transcription (Claude Code).  Five
  open questions raised for Codex; one self-inflicted loophole closed; the
  execution contract registered.**  Still no code, no notebook, no execution,
  no Drive read, no rule change.

  *A loophole in the transcription's own wording, closed.*  §Preregistration
  principle previously allowed a definition to be "amended and re-approved
  through the Decision log ... before the affected measurement runs".  Read
  literally that permits amending M1-M4 **after** M0 has been seen, as long as
  M1 has not started — which is exactly what the transfer message forbids.
  Corrected: once any M0 result has been observed, an M1-M4 definition may not
  be amended at all; the run STOPs and returns to Codex.  There is no in-flight
  repair path.

  *Five design questions, as originally raised; resolved in the later Codex
  entry and §Resolved design decisions.*  At this historical step they were not
  decided.  Q1 is the substantive one: `raw_atr_ordinal` enumerates **all**
  `.atr` annotations including dropped ones, so every dropped F beat splits a
  run, the suppression is multiplicative in run length, and F beats are
  concentrated in record **208** — biasing `share_in_long_runs` and the
  run-length gate **toward H1 and away from H3**, hardest in the record that
  motivates the diagnostic.  A proposal is recorded (keep raw-ordinal adjacency
  primary, add `mamba_record_row` adjacency as a registered secondary, which is
  sequence adjacency and not the forbidden time-based repair), but the
  registered definition stands unchanged until Codex rules.  Q2-Q5 are
  under-specifications that would otherwise force implementer choices: Control
  B's permutation must be declared joint rather than per-reason; Holm's scope
  when M4 is absent; the derivation of the cache-side `CERTIFIED` group, which
  has no row of its own in `join_map`; and the `CACHE_ENDPOINT_ZERO` rows whose
  stored `0.0` endpoints land them in the very distance bin H3 reads.

  *Execution contract registered (§Runtime and execution-environment
  contract).*  Engineering only, no scientific rule touched.  Per-stage
  dependencies declared up front (`pyarrow` before the run, not at bundle-write
  time); registered-input access opt-in and re-verified through the frozen
  module's own `build_preflight()` / `verify_preflight_freeze()`; the canonical
  bundle checked for the absence of `SUPERSEDED.json` and for code SHA-256
  `6b098c67…` rather than trusted by path; capability assertions and `__file__`
  printing on **both** modules; every stage announcing `RUN`/`SKIP`.  Each of
  these closes a failure mode Q5-D actually hit.

  *Cost, measured rather than assumed.*  Q5-E's controls permute an
  already-measured 24,341-row table instead of rerunning the matcher, so the
  whole diagnostic is minutes, not the ~14 hours that forced Q5-D to shard.
  `load_mamba_sequences()` reads only `feats` and `pid`, never `beat`/`ref`, so
  peak memory is small.  No sharding, resume directory or cross-session
  checkpointing is registered; an implementation that needs them has a defect,
  not a scheduling problem.

  *One inherited number confirmed, not corrected.*  `5 of 13` looked
  inconsistent with the parent spec's 12 numbered gates.  `evaluate_gates()`
  emits 13 — gate 2 splits into `2a_leg1_source_replay` / `2b_leg2_record_
  boundaries`, plus `13_ambiguity_reported`.  The figure is right and is now
  annotated so no one "fixes" it.

- 2026-08-11 — **Codex resolution of PR #100's five open design questions and
  M4 feasibility decision.  Design only; status remains `draft`.**

  **Q1.**  `mamba_record_row` is primary for every run/neighbourhood statistic
  and H1/H3 gate; `raw_atr_ordinal` is a non-decisional secondary sensitivity
  audit.  Raw ordinal was rejected as primary because dropped F/Q annotations
  fragment runs record-dependently, most strongly in record 208, biasing the
  registered gate inputs toward H1 and away from H3.  Processed-row adjacency is
  the literal Leg 2 sequence and introduces neither time imputation nor a new
  join rule.

  **Q2.**  Control B is one joint categorical permutation within each
  `record x side`, preserving all four group counts without collisions.

  **Q3.**  Holm remains four-family in every branch.  When M4 is absent, H2/H3
  are `UNEVALUABLE` and contribute p=1 only to `p_holm_4family`; no conditional
  two-family correction is allowed and H1/H4 partial flags remain nonterminal.

  **Q4.**  Cache-side certified rows are derived one-to-one from certified
  mamba rows' `cache_record_row`, with uniqueness, count-equality, class-lineage
  and exhaustive-partition assertions.

  **Q5.**  `CACHE_ENDPOINT_ZERO` rows remain visible in QA and descriptive
  denominators but are excluded identically from observed and null H1/H3
  distance gates.  Their separate `H3_ENDPOINT_COMPONENT` is descriptive and
  cannot fire H3.

  **M4.**  M4 is retained because intentionally omitting it makes H2/H3
  unevaluable.  A separate read-only `PREP_M4_ASSET_FREEZE` is now a blocker to
  status promotion: it must uniquely hash/freeze the canonical V9/V10 producer
  and cache lineage and reproduce all 44 cache record counts in each version.
  Failure leaves
  the spec draft as `M4_INPUT_FREEZE_FAILED`; it does not license a substitute
  detector, version, tolerance or source.

  **Transferred values.**  Null seed `2026019`, the cache-side V/`NO_EDGE` H1
  population reading, and `local_rr_sd` over clipped `[row-10,row+10]` are
  accepted.  The latter is now explicit population SD (`ddof=0`) in integer
  samples, with SD 0 for a one-row window.
