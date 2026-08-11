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

1. Codex fixes this design; Claude transcribes it into this file and opens a PR.
   **← this step.**
2. The user approves the design; `status` becomes `approved_for_implementation`.
3. Claude implements the frozen design on `claude/<task>` **without executing
   it**.
4. The user separately approves execution on the registered artifacts.
5. Only then may M0-M4 run, write a new timestamped Drive bundle, and be
   reviewed.

Steps 2 and 4 are independent approvals.  Neither authorizes DS2 per-beat
labels, V10 probabilities, the association analysis, or any training.  Those
seals are unchanged by this document.

**No aggregation of `unmatched_and_ambiguous.csv` or `join_map.parquet` may be
computed before step 4** — including the zero-execution-cost M0.  A diagnostic
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
   interpretation rule of M1-M4.  If a definition proves unimplementable, the
   spec is amended and re-approved through the Decision log, in the open, before
   the affected measurement runs — never adjusted after its own result.
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
   - M2's run construction over `raw_atr_ordinal` is a **mamba-side**
     measurement.  Cache-side rows are excluded and are **never** imputed into a
     run by time adjacency or by neighbour class.
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

**M0.4 — consecutive failure runs over `raw_atr_ordinal`.**
Mamba side only (§What the bundle contains, item 2).  A run is a maximal set of
mamba-side failed rows whose `raw_atr_ordinal` values are **exactly
consecutive integers** within one record.  Report:

- counts in run-length buckets `1`, `2`, `3-9`, `>=10`;
- median, p90 and maximum run length;
- `share_in_long_runs = (failed rows in runs of length >= 3) / (all mamba-side
  failed rows)`.

Runs never cross a record boundary.  A gap in `raw_atr_ordinal` ends the run;
missing ordinals are never bridged by time adjacency.

**M0.5 — conditional failure after a failed V beat.**
```text
numerator   = mamba-side rows where the beat at raw_atr_ordinal + 1 in the same
              record exists and is failed, given the row at raw_atr_ordinal is
              failed and has mamba_aami == V
denominator = mamba-side failed rows with mamba_aami == V whose
              raw_atr_ordinal + 1 exists in the same record
```
Report the same quantity for N and S as the comparison, and the unconditional
mamba-side failure rate as the reference level.

**M0.6 — strata always separated.**
Every M0 table is reported for the 17 equal-count DS1 records and the 5
mismatched-count DS1 records separately, in addition to pooled.  The strata are
reporting strata: neither may be excluded, re-matched, or used to rescue
anything.

## M1 — nearest-candidate distance

Inputs: frozen mamba RR (Leg 1 replay under the frozen module) and frozen cache
RR, both converted by the frozen integer-sample contract.  **No new RR
representation is introduced.**

Population: **non-certified cache rows**, DS1.

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

**M1 is not a tolerance experiment.**  It is forbidden to report, or to compute,
coverage or match counts under any tolerance other than the frozen 1 sample.

## M2 — failure adjacency and runs

Inputs: `unmatched_and_ambiguous.csv` and `join_map.parquet`, mamba side.

- adjacency is defined **only** on exactly consecutive `raw_atr_ordinal` within
  one record (same definition as M0.4);
- runs never cross a record boundary;
- rows with a missing ordinal — which is every cache-side row — are excluded,
  never repaired by time adjacency;
- for every failed mamba-side V beat, report the failure topology of the
  `+/-1 beat` neighbourhood and of the `+/-10 beat` neighbourhood: number of
  neighbours present, number failed, failure share, and the same three for N and
  S as comparison.

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
| `local_rr_sd` | population standard deviation of `pre` over rows `[row-10, row+10]` clipped to the record, in integer samples at 360 Hz |

Compared across the four groups `CERTIFIED`, `NO_EDGE`, `NOT_OPTIMAL`,
`AMBIGUOUS`.  Report median, p25, p75, and the full ECDF per group.

**Nothing is selected.**  No new matching is chosen, no arbitrary maximum path
is promoted to truth, no edge is re-certified.  This measurement observes the
graph the frozen rule already built.

## M4 — detector / source discordance anchors

Inputs: the registered DS1 raw MIT-BIH tree and the frozen lineage source only.

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
3. the source version and hash are frozen.  **As registered today they are
   not**: `research/ASSETS.md :: baseline-v10-source` and `baseline-v9-source`
   both record "hash 미계산", and the cache record NPZs likewise have no
   computed hash.  Freezing them is a prerequisite of M4, and computing those
   hashes is itself part of the implementation, not a result-dependent choice.

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

For each anchor, measure the failure topology of the 10 beats before and the 10
beats after, on the mamba side over `raw_atr_ordinal`.  Report failure share per
offset `-10 … +10`, and the share of all failures that lie within 10 beats after
some anchor.

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

# Negative controls and null computation

Three controls, each **10,000 replicates**, master seed **`2026019`**, drawn per
`(control, replicate)` so replicate `b` is the same value on any machine, in any
order, on any worker count.  Each replicate recomputes the **complete statistic**
of its family from the permuted arrangement; nothing is approximated and no
family is omitted.

| control | what is permuted | what is preserved | what it falsifies |
|---|---|---|---|
| **A** — within-record class circular shift | the per-record class sequence is circularly shifted by a non-zero offset drawn uniformly from `1 … n-1` | per-record class composition, per-record failure count, the entire failure run structure | "the V association is only record composition plus record 208's weight" |
| **B** — within-record failure-position permutation | the ordinal positions of failures are permuted within `record x side x failure-reason` | per-record, per-side, per-reason failure counts | "the observed long runs arose by chance within the same record" |
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
first failure.

A p-value alone never promotes a mechanism.  A flag fires only when its
Holm-adjusted family p-value is significant **and** every effect-size condition
below holds.

# Preregistered association flags

Each flag is evaluated **independently**.  All conditions of a flag must hold.

**`H1_ASSOCIATED`** — all of:
- among uncensored failed V rows with reason `NO_EDGE`, the share with
  `d_inf` in `2-5` samples is `>= 0.50`;
- the V-by-distance-bucket association exceeds Control A's `q99`;
- the majority of the relevant run-length mass is at length `<= 2`;
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
- `>= 0.50` of the explained failures lie in runs of length `>= 3`;
- the distance distribution places more mass in `21-100` or `>100` samples than
  in `2-5` samples;
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

1. **`DIAGNOSTIC_INPUT_MISMATCH`** — any QA reproduction target in §QA fails, or
   canonical and superseded bundles cannot be told apart, or an input hash is
   unknown.  **STOP.**  No measurement is reported.
2. **`MECHANISM_UNRESOLVED_INPUT_ABSENT`** — QA passes but M4.0 fails, so H2 and
   H3 cannot be evaluated.  M0-M3 are reported as **diagnostic partial results**;
   `H1_ASSOCIATED` and `H4_ASSOCIATED` may be computed and reported but are
   **not** promoted to a terminal mechanism verdict.
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
- a source hash is unknown or unverifiable;
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
| 3 | record 208 failure raster | x = `raw_atr_ordinal`, one row per class, mark = failed beat |
| 4 | run-length distribution | histogram over buckets `1`, `2`, `3-9`, `>=10`, plus median/p90/max |
| 5 | nearest-distance histogram | fixed bins `0-1`, `2-5`, `6-20`, `21-100`, `>100`; censored rows in their own bar |
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
         "record_208": {}, "runs": {}, "post_v_failure": {}, "strata": {}},
  "m1": {"bins": {}, "censored": 0, "window_half_width": 15},
  "m2": {"runs": {}, "v_neighbourhood_pm1": {}, "v_neighbourhood_pm10": {}},
  "m3": {"by_group": {}},
  "m4": {"status": "OK | DIAGNOSTIC_INPUT_ABSENT", "feasibility": {},
         "anchors": 0, "offset_curve": {}},
  "m5": {"strata_present": ["class", "reason", "record",
                            "count_stratum", "record_116", "record_208",
                            "pooled"]},
  "null": {"replicates": 10000, "master_seed": 2026019,
           "controls": {"A": {}, "B": {}, "C": {}}},
  "tests": {"H1": {"statistic": 0.0, "p": 0.0, "p_holm": 0.0, "q99": 0.0,
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
- `m0_runs.csv` — `record, run_start_ordinal, run_length, classes, reasons`
- `m1_distance.csv` — `record, cache_record_row, processed_class, reason, d_inf, bin, censored`
- `m3_graph.csv` — `record, side, row, group, candidate_degree, usable_edges, has_forced_rank, rr_pair_multiplicity, local_rr_sd`
- `m4_anchors.csv` — `record, anchor_ordinal, anchor_kind, offset, failed` (absent when M4 stops)
- `null_summary.json` — per control, per statistic: full quantiles, `q95`, `q99`, seed, replicate count

# Inputs and outputs contract for a future approved implementation

## Files allowed to change

During the current design task, **only this file**.

After the design approval (step 2), implementation is limited to:

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

1. user approves the spec;
2. Claude Code opens an implementation PR (code only, not executed);
3. user approves execution;
4. M0-M4 run;
5. a new timestamped Drive bundle is written;
6. the executed notebook is committed and the run ingested;
7. Codex performs result acceptance.

# Implementation checklist

- [ ] User approves this draft; `status` becomes `approved_for_implementation`
- [ ] Claude implements the frozen design without executing it
- [ ] User separately approves execution on the registered artifacts
- [ ] Bundle file IDs, byte sizes and SHA-256 recorded before any measurement
- [ ] QA reproduction targets all match, or `DIAGNOSTIC_INPUT_MISMATCH`
- [ ] M3 graph reconstruction reproduces the bundle partition exactly
- [ ] M4 feasibility gate evaluated before any anchor is used
- [ ] The complete M0-M4 plan is unchanged from this document at run time
- [ ] All three controls run at 10,000 replicates under seed `2026019`
- [ ] Holm correction applied across exactly the four families
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
