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

1. The user approved `PREP_M4_ASSET_FREEZE`; Claude completed it read-only and
   recorded `PREP_M4_ASSET_FREEZE_PASS`, with no M0-M4 aggregation.
2. Codex accepts that preflight, fixes decisions A-E in this file and opens a
   PR.  **This step.**
3. The user separately approves `PREP_M4_RR_EQUIVALENCE`; Claude runs only that
   read-only value-identity preflight and records its result.
4. Codex accepts that result; the user approves the completed design and
   `status` becomes `approved_for_implementation`.
5. Claude implements the frozen design on `claude/<task>` **without executing
   it**.
6. The user separately approves execution on the registered artifacts.
7. Only then may M0-M4 run, write a new timestamped Drive bundle, and be
   reviewed.

Steps 1, 3, 4 and 6 are separate approvals: asset freeze, RR value-equivalence
preflight, implementation design, and scientific execution respectively.  None authorizes DS2 per-beat
labels, V10 probabilities, the association analysis, or any training.  Those
seals are unchanged by this document.

The frontmatter `split` reads `DS1_only_diagnostic`.  That is the **scope of
this diagnostic**, forced by the DS2 seal, and it is not a change to the
project's principal benchmark: `AGENTS.md`'s DS1 -> DS2 inter-patient evaluation
and the parent's `S_PR_AUC` primary remain exactly as registered.

**No aggregation of `unmatched_and_ambiguous.csv` or `join_map.parquet` may be
computed before step 7** — including the zero-execution-cost M0.  A diagnostic
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
- registered **V10** preprocessing cache, aggregate `82b9a593…` over 45
  files, as the M4/Leg 2 input; the V9 cache aggregate `25cd7952…` is a
  corroborating rebuild and is not a substitute input;
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
3. verify, without detector replay, that `rr.shape[0]` and `meta.json[n]` equal
   the registered row count for every one of the 44 cache records in both V9
   and V10 (44/44 per version), reading neither `y` nor any probability array;
   without opening V10 probability values or DS2 per-beat class labels; and
4. record the resulting identities in `research/ASSETS.md` and this Decision log
   before implementation approval.

If the canonical producer cannot be identified uniquely, a required hash is
unverifiable, or the cache-shape/meta ledger does not verify all 44 counts, the
preflight ends `M4_INPUT_FREEZE_FAILED`.  The spec stays `draft`; no detector,
version, tolerance or source is substituted.  This preflight performs no M0-M4
aggregation and does not itself authorize implementation or execution.

`PREP_M4_ASSET_FREEZE_PASS` was accepted by Codex on 2026-08-12.  The
connector/mounted-filesystem split is valid identity evidence because all 90
cache file sizes bound the two views 90/90 and the four reported aggregates
were independently reproduced from their `(name, bytes, sha256)` triples 4/4.
This establishes byte identity, not runtime reproducibility or detector-output
reproducibility.

### Frozen M4 identity constants

These constants are in the operative body rather than only the Decision log so
an implementation cannot choose an identity by path, filename or whichever
copy happens to be available.

| role | asset | Drive ID | files / bytes | registered aggregate SHA-256 |
|---|---|---|---|---|
| **M4 input contract** | V10 source `kinkmap/` | `1czXZdgSrGttrhOFlNvOHQ3l16ZfluOPX` | 7 `.py` / 39,761 B | `1a0c66c8116745bf83f836fd267931b83f0179cc5e62fd1ba5b055ec236452ce` |
| **M4 input contract** | V10 cache | `1I6iugsrHwJjjpLVS8TVp-aDkVwpdmJxF` | 45 / 167,868,618 B | `82b9a593dcf23fa4ffc60b44c2fe7da02313dfe7d69dfbe64d85c38b4aa78b14` |
| corroborating rebuild | V9 source `kinkmap/` | `1oYHJi38hir2JqZl9s_SyuSxq3Hxw25sK` | 7 `.py` / 79,329 B | `ffb5679cdfd6b9cc5d46a1071f1fac374d0bb428c360d9a2be80edb111bfb296` |
| corroborating rebuild | V9 cache | `1TXLX14RHA5u1dIUiYt36k2dcT5lpm5RY` | 45 / 167,064,378 B | `25cd7952329fc6f04273046c80d5b0d7b3ee74baf10d2dba4036f9ea7f94fbe8` |

The V10 source expected set is fixed as
`{__init__,data,evaluate,frontend,model,pwave,train}.py`; the V9 corroborating
set is `{__init__,data,evaluate,frontend,model,train,v15b_local}.py`.  Future
verification uses these exact names and fails on either a missing or an extra
file.  The five V9 zip archives are recorded historical neighbours, not loaded
producer inputs, and remain outside this contract.  They become inputs only if
a later, separately preregistered procedure reads them.

The decisive source-map files are V10 `frontend.py`, SHA-256
`d2635e05c2e0b26f68ae022c0997970c5d3a3d0828e3e943c7c78b260a78a217`,
and V10 `data.py`, SHA-256
`20cde66b01d1172926aa1b84cbb70b70ea28bb20c2e958a2c26bd01d03497ada`.
The former is byte-identical in V9 and V10.  `v15b_local.py` belongs to the
mamba/Leg 1 lineage and must never be treated as the V10 cache producer.

The V9 constants are corroborating evidence only for M4.  Their mismatch may
not be silently ignored, but it is reported as `CORROBORATION_MISMATCH` rather
than repaired by substituting V9 for V10.  The separate RR-equivalence preflight
below uses both cache trees as its own inputs.

### PREP_M4_RR_EQUIVALENCE — separate approval blocker

Before implementation approval, and only after separate user approval, compare
the stored V9 and V10 `rr` arrays for all 44 records.  This is a read-only asset
preflight, not part of M4 implementation and not an M0-M4 measurement.  It must:

1. re-verify the two cache constants above, including their exact expected sets;
2. open only the `rr` member with `allow_pickle=False`, never `y`, probabilities
   or DS2 per-beat labels;
3. require identical record names, `(n, 7)` shapes and `float32` dtypes; and
4. require value identity for every element, treating paired NaNs as equal, and
   report `RR_VALUE_IDENTICAL_44_OF_44` only when all 44 records pass.

On any mismatch it reports `V9_V10_RR_LINEAGE_DIVERGED`, preserves the mismatch
record/row/column and value pair for audit, leaves this spec `draft`, and returns
to Codex.  It does not average, tolerate, repair or select a lineage.  A PASS
strengthens the same-row-set premise at value level; it is not evidence that
detector peaks or the registered runtime have been reproduced.

### M4.0 — feasibility gate, evaluated first

All three must hold:

1. a read-only static source-map verification, performed against the two exact
   V10 file hashes above before any detector call, confirms the original run's
   `detect_r()`/`rr_features()` producer in `frontend.py` and the annotation
   matching, AAMI selection, reused `idx`, and boundary selection in `data.py`:
   `tol = int(0.15 * fs)`, greedy nearest `used`-set matching, and the
   `p-150 >= 0` / `p+150 <= len` cut.  Keyword presence alone is insufficient;
   the checklist records function and call-site mappings.  A mismatch yields
   `M4_SOURCE_MAP_UNVERIFIED` and condition 1 fails;
2. the required detector peak positions are obtainable **deterministically** —
   note that neither lineage stores them (§What the bundle contains, item 6), so
   this requires re-running the detector under the registered runtime
   (`numpy 2.5.1`, `scipy 1.18.0`, `wfdb 4.3.1`, CPython 3.12.3), whose output
   must be shown to reproduce the registered per-record cache counts for all 22
   DS1 records before any anchor is used;
3. the V10 source and V10 cache equal the two **M4 input-contract** identities
   above and `PREP_M4_RR_EQUIVALENCE` has passed.  A path or filename without
   its registered digest is insufficient.  V9 is never substituted for V10.

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

## Dual-attestation identity standard

When a registered Drive asset is too large for the connector to stream, a
connector listing and a user-mounted read-only hash run may jointly establish
byte identity only when all of the following are recorded and pass: canonical
Drive IDs; an exact preregistered expected-name set; connector and mounted-view
byte sizes agreeing for every file; mounted-view per-file SHA-256; and an
independent recomputation of the registered canonical-JSON aggregate from every
`(name, bytes, sha256)` triple.  Each later verification re-enumerates the
registered folder ID and repeats the full name/size crosswalk; an old listing,
mtime or path alone is never inherited as proof.  Any missing, extra, size or
digest mismatch stops the consuming stage.

This protocol attests file identity only.  `PREP_M4_ASSET_FREEZE` links the
registered runtime identity to the frozen generation lineage, so its PASS is
accepted despite the hash run using Colab CPython 3.12.13 / numpy 2.0.2.  It
does **not** establish that the registered CPython 3.12.3 / numpy 2.5.1 / scipy
1.18.0 / wfdb 4.3.1 runtime can be installed or will reproduce detector peaks.
That separate claim is tested only by M4.0 condition 2, with no fallback
runtime or approximate count match.

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
the original producer/cache lineage and verify all 44 cache record counts from
`rr` shape and metadata in each version is
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
2. **`MECHANISM_UNRESOLVED_INPUT_ABSENT`** — QA passes but M4.0 fails, including
   `M4_SOURCE_MAP_UNVERIFIED`, an unavailable exact registered runtime, or a
   22/22 detector-count reproduction failure, so H2 and H3 cannot be evaluated.
   M0-M3 are reported as **diagnostic partial results**;
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

1. user approves the read-only `PREP_M4_RR_EQUIVALENCE` preflight;
2. Claude performs only that preflight and records its result;
3. Codex accepts the result and the user approves the completed spec;
4. `status` becomes `approved_for_implementation`;
5. Claude Code opens an implementation PR (code only, not executed);
6. user separately approves execution;
7. M0-M4 run;
8. a new timestamped Drive bundle is written;
9. the executed notebook is committed and the run ingested;
10. Codex performs result acceptance.

# Implementation checklist

- [x] Codex resolves the five open design questions (Q1-Q5)
- [x] User approves the read-only `PREP_M4_ASSET_FREEZE` scope
- [x] `PREP_M4_ASSET_FREEZE` uniquely freezes source/cache identities and
      verifies all 44 cache `rr` shape/meta counts in each version before status promotion
      — **`PREP_M4_ASSET_FREEZE_PASS`, 2026-08-11** (Decision log below)
- [x] Codex accepts `PREP_M4_ASSET_FREEZE` and resolves A-E without executing
      any diagnostic measurement
- [x] User separately approves `PREP_M4_RR_EQUIVALENCE`
- [x] The value-level RR preflight returns `RR_VALUE_IDENTICAL_44_OF_44`, or
      `V9_V10_RR_LINEAGE_DIVERGED` returns the draft to Codex
      — **`RR_VALUE_IDENTICAL_44_OF_44`, 2026-08-12** (Decision log below)
- [ ] User approves this draft; `status` becomes `approved_for_implementation`
- [ ] Claude implements the frozen design without executing it
- [ ] User separately approves execution on the registered artifacts
- [ ] Bundle file IDs, byte sizes and SHA-256 recorded before any measurement
- [ ] QA reproduction targets all match, or `DIAGNOSTIC_INPUT_MISMATCH`
- [ ] M3 graph reconstruction reproduces the bundle partition exactly
- [ ] Static source-map verification passes against the frozen V10
      `frontend.py` and `data.py` hashes before any detector call
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
  and cache lineage and verify all 44 cache `rr` shape/meta counts in each version.
  Failure leaves
  the spec draft as `M4_INPUT_FREEZE_FAILED`; it does not license a substitute
  detector, version, tolerance or source.

  **Transferred values.**  Null seed `2026019`, the cache-side V/`NO_EDGE` H1
  population reading, and `local_rr_sd` over clipped `[row-10,row+10]` are
  accepted.  The latter is now explicit population SD (`ddof=0`) in integer
  samples, with SD 0 for a one-row window.

- 2026-08-11 — **`PREP_M4_ASSET_FREEZE_PASS`.  Read-only asset freeze; no
  detector replay, no M0-M4 aggregation, no implementation.**

  *Scope and authority.*  The user approved the read-only
  `PREP_M4_ASSET_FREEZE` scope only.  This entry records measured identities.
  It is **not** implementation approval and **not** M0-M4 execution approval;
  `status` stays `draft`.

  *Preflight run.*  Branch `claude/q5e-m4-asset-freeze`.  Gate checked first:
  PR #101 merged to `main` at `7964270`, and the required §"Resolved design
  decisions", §"PREP_M4_ASSET_FREEZE", `mamba_record_row` primary and
  `raw_atr_ordinal` non-decisional text all present before any measurement.

  *Where the numbers come from — stated plainly.*  Drive file/folder IDs, file
  counts, per-file byte sizes and mtimes were measured **by Claude Code through
  the Drive connector in this session**.  The SHA-256 values, tree digests and
  `rr` shapes were computed **by the user in Colab with Drive mounted**, because
  this container cannot stream the 334,932,996 B of cache bytes (the connector
  returns file content into the model context; the smallest npz is 2,543,011 B).
  A first attempt therefore ended `PREP_ENVIRONMENT_BLOCKED` with no repository
  change.  The two sources are bound together by measurement, not by assertion:
  **all 90 cache file byte sizes agree exactly between the connector listing and
  the mounted filesystem (90/90)**, so the registered Drive IDs and the hashed
  bytes are the same files.  Every reported aggregate was independently
  recomputed here from its own `(name, bytes, sha256)` triples through
  `hash_file_set()`'s canonical-JSON fold and matched, 4/4.

  *Digest contract.*  `PREP_DIGEST_CONTRACT_UNRESOLVED` did not fire.  The
  registered convention `q5d_order_preserving_beat_join.hash_file_set()` was
  reused unchanged, with `cache_expected_files()` (= `meta.json` + 44 record
  npz = 45 names) as the cache expected set.  No new digest algorithm was
  invented.

  *Frozen identities.*

  | asset | Drive ID | files | bytes | aggregate / tree SHA-256 |
  |---|---|---|---|---|
  | V9 source `kinkmap/` | `1oYHJi38hir2JqZl9s_SyuSxq3Hxw25sK` (pkg root) | 7 `.py` | 79,329 | `ffb5679cdfd6b9cc5d46a1071f1fac374d0bb428c360d9a2be80edb111bfb296` |
  | V10 source `kinkmap/` | `1czXZdgSrGttrhOFlNvOHQ3l16ZfluOPX` (pkg root `18Zb55_VUYfuSwjTPpVMUGvTG1L7snOB_`) | 7 `.py` | 39,761 | `1a0c66c8116745bf83f836fd267931b83f0179cc5e62fd1ba5b055ec236452ce` |
  | V9 cache | `1TXLX14RHA5u1dIUiYt36k2dcT5lpm5RY` | 45 | 167,064,378 | `25cd7952329fc6f04273046c80d5b0d7b3ee74baf10d2dba4036f9ea7f94fbe8` |
  | V10 cache | `1I6iugsrHwJjjpLVS8TVp-aDkVwpdmJxF` | 45 | 167,868,618 | `82b9a593dcf23fa4ffc60b44c2fe7da02313dfe7d69dfbe64d85c38b4aa78b14` |

  *Cache structure, both versions.*  45/45 files, **missing 0, unexpected 0**.
  All 44 records: `rr.shape[0] == meta.json[n]`, `rr` is `(n, 7) float32`, and
  `cache_n`/`split` match the frozen ledger 44/44.  **Shape mismatches: 0.**
  Split totals **DS1 50,551 · DS2 49,289 · total 99,840** in each version, equal
  to the registered values.  V9 and V10 agree on all 44 record counts.

  *Three findings worth more than the freeze itself.*

  1. **The V10 cache tree digest is `82b9a593dcf2…`, which equals the input
     identity the canonical `EXP-2026-007` DS1_GATE run registered
     (`82b9a593…`).**  The cache frozen here is byte-for-byte the cache that
     produced `JOIN_UNRESOLVED` — established by digest, not by path or
     filename.  The V9 cache digest `25cd7952…` differs, which is the correct
     result: Leg 2 consumes V10 positional rows.
  2. **`frontend.py` is byte-identical across V9 and V10** (`d2635e05…`,
     8,434 B), as are `evaluate.py`, `train.py` and `__init__.py`.  `detect_r()`
     and `rr_features()` live in `frontend.py`, so the detector and the RR
     producer are now proven to be the *same file* in both lineages at hash
     level, not merely "identical at string level" as previously argued.
     `data.py` differs (6,972 -> 7,744 B) and `pwave.py` is V10-only, exactly
     the shape the `pw` add-on predicts.  The artifacts agree independently:
     every V10 cache npz carries members `beat ref rr sim pw ctx y` against V9's
     `beat ref rr sim ctx y` — one added key, same row counts, same `rr` shape.
  3. **`v15b_local.py` on Drive hashes to `cd4320e5…`, identical to the
     committed `mit-bih/lineage/v15b_local.py` and to the value recorded in
     `research/PROVENANCE_2026-08-10_mamba_data_lineage.md`.**  That document's
     open gap — "no means to confirm the committed copy is byte-identical to the
     original" — is now closed for this path.  Note it is the **mamba (Leg 1)**
     producer and lives only on the V9 side; it is not the V9/V10 cache
     producer.

  *Seals.*  `y` was never read — only NPZ member *names* were listed, and only
  `rr` was materialised.  No DS2 per-beat class label, no V10 probability, no
  association, no S PR-AUC, no training.  `detector_replay_performed: false`,
  `training_performed: false`, `association_performed: false`.  No Drive file
  was modified, moved, deleted or overwritten; the run only read.

  *Three residuals, recorded rather than papered over.*

  1. **The source expected-set was discovered, then registered.**  The Colab
     step passed a `*.py` glob as `hash_file_set`'s expected names, so its
     aggregate was a snapshot, not a contract — and a glob cannot notice an
     absent file, the exact failure this spec already rejects for the V10 result
     grid.  Closed by **registering the name lists now**: V9 =
     `{__init__, data, evaluate, frontend, model, train, v15b_local}.py`, V10 =
     `{__init__, data, evaluate, frontend, model, pwave, train}.py`.  Future
     verification recomputes over these fixed names, so a deletion is
     detectable.  The five archives present in the V9 folder
     (`cache_v15b.zip`, `v11.zip`, `v12.zip`, `v13.zip`, `v13pkg.zip`) are
     recorded as present and **outside the frozen contract**; bringing them
     under contract needs a separate decision.
  2. **The rule-to-file mapping is carried, not re-measured.**  Which file holds
     `detect_r()`, `tol = int(0.15 * fs)`, the greedy `used`-set matching, the
     +/-150 boundary cut, the AAMI filter, `rr_features` and the `nan -> 0.0`
     endpoint is recorded in the `EXP-2026-007` Decision log and in
     `research/ASSETS.md :: baseline-v10-source` from an earlier reading of these
     same files.  Those readings were not hash-pinned at the time.  The hashes
     above pin the bytes from now on, and M4 must confirm the mapping against
     these frozen digests before using any anchor.
  3. **The measurement environment is not the registered runtime.**  The freeze
     ran on Colab `python 3.12.13 / numpy 2.0.2`; the registered runtime is
     `CPython 3.12.3 / numpy 2.5.1 / scipy 1.18.0 / wfdb 4.3.1 /
     tensorflow 2.21.0 / keras 3.15.0`.  This is irrelevant to SHA-256 and to
     reading a stored `rr` shape, and the registered runtime is recorded and
     linked to these identities as §E requires.  It is **not** evidence that the
     registered runtime is reproducible here.

  *What this PASS does and does not unblock.*  M4.0 condition 3 (source,
  cache and hashes equal to the frozen identities) is now satisfiable, and
  condition 1's source is identified and pinned.  **Condition 2 is not
  satisfied**: detector peak positions are stored in neither lineage, so M4
  still requires re-running `detect_r()` under the registered runtime and
  showing it reproduces the registered per-record counts for all 22 DS1 records.
  Nothing here performed that.

  **PREP 통과는 EXP-2026-008 구현 승인 또는 M0-M4 실행 승인이 아니다.**

  *Freeze manifest — per-file SHA-256 (the record a tree digest alone cannot
  replace: it says something changed, not what).*

```text
# sources/v9  files=7  bytes=79329  aggregate=ffb5679cdfd6b9cc5d46a1071f1fac374d0bb428c360d9a2be80edb111bfb296
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855          0  __init__.py
e178c51ebf1e526e3296d5e81476652cadf4f4b87a25526ef6ac199f52f3632c       6972  data.py
62910d3b16d1834743c91509f69051d9b03e0ce46a1684347eb8a29c5f071bd2       6898  evaluate.py
d2635e05c2e0b26f68ae022c0997970c5d3a3d0828e3e943c7c78b260a78a217       8434  frontend.py
feae1eef46976928f9fde3be872929074f22a7ea14cd3f8585b33fb08f8370ac       5133  model.py
57c336a9668465ee8eb0a832a4af78ec8383137db6150822b9d0f1e36e220eae       4697  train.py
cd4320e50068a93f460238ff28a2c22f80da42b0002b1a192d79ea2e17721421      47195  v15b_local.py

# sources/v10  files=7  bytes=39761  aggregate=1a0c66c8116745bf83f836fd267931b83f0179cc5e62fd1ba5b055ec236452ce
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855          0  __init__.py
20cde66b01d1172926aa1b84cbb70b70ea28bb20c2e958a2c26bd01d03497ada       7744  data.py
62910d3b16d1834743c91509f69051d9b03e0ce46a1684347eb8a29c5f071bd2       6898  evaluate.py
d2635e05c2e0b26f68ae022c0997970c5d3a3d0828e3e943c7c78b260a78a217       8434  frontend.py
10c80659f48f9f81809f7d6a1a82748ce4380f74b7bd38404aef35af659bf156       5861  model.py
addfecb0613f19a12d22c9d73e22da0be2b3bd1f9da0188a20e4bb9e7878aee8       6127  pwave.py
57c336a9668465ee8eb0a832a4af78ec8383137db6150822b9d0f1e36e220eae       4697  train.py

# caches/v9  files=45  bytes=167064378  aggregate=25cd7952329fc6f04273046c80d5b0d7b3ee74baf10d2dba4036f9ea7f94fbe8
efa2233881409e739d5245d4ca7fab9f1b0cb46fc6b2541b9e03c30e577af1a7    3659122  100.npz
c782e16309b4c5bc672e92a031cd06270af67bb8f4afb0fcd48ff3a0603c92ec    3055976  101.npz
5973995c6ac5f610150b9b7e0c66461c444fa9faf468d6b3aa4a52264c657c46    3432247  103.npz
b209ba0c1abc205327909bea38d240326b301659dbc310ce83d64417872203eb    4291133  105.npz
ad2befe31948c8e5a4f4fbd220ba099b35cb0187d364b6b2c57d2efb3391a333    3466362  106.npz
fb406dab622c318527d39454fcff4139675fb54b7890a9ff50dea0a7b20d8397    2962708  108.npz
4f7c37e9a8e6a8d94509699e26fda966c0935a62960e73d8d42097141a0fbbda    4231247  109.npz
c9bd518420a3f7fc8e7a55257637c681e27ad2fe2394b487b7ae590d6051a2d8    3555970  111.npz
550295e085c4e8c2fcf38536dcc99c8a4b90a548cc3dddb2ddbc7ded420dd2f0    4134230  112.npz
a6ff5e97edf63ae8f4a410a505feb5dc2ddffb931d73fc0aa84e7ee9472dea14    3043636  113.npz
6cb43a4c63e39315840b5ea6e288b1cedd803d6d0a22d59516d8e56d0e9c922f    3130543  114.npz
94819731680cb6c905969130deb7f470b305f202da41dc2a4f54e3993195b905    3238333  115.npz
65892707d076941ef92598b874eba8baefbac9c1da1fbb3df243ba700f5cd55b    4094120  116.npz
8724803d033a629d094cf7adf9241ac8ed931a47198847a10e93276c4e7c5a88    2556519  117.npz
bc388644034ba3c34b7750e53e6fb6ad1459cb1e3767790a0a307c8f8d71349d    3881323  118.npz
16b2b4315dd5d6acd5d3966d331089088fcdf4ddf973c1432298eebb611a2fb4    3416313  119.npz
f4386222753458c9f42a1d2d66dd887b49f8c8d4f7e3da9174b11c55a214011f    3056954  121.npz
556447e09ff9716902497099d5976d590e8640bdca282b263221250176467c27    4078204  122.npz
ea1cef353b75b27ef2c7c8a52cfa438ce616231c1e1e2319c49bc4e59fb354a4    2543011  123.npz
2f516f41d15a698d35f31f8ca1b1f323698aeb1a1b8c36b78a7ffc51511589ff    2724033  124.npz
4ac8588158957995e215c266e6153e611b8db61c4894450b4d4b166819f1de33    4417055  200.npz
ef2ac06a64eeb4f24667008d08c1d17d6a12f643cb7e85c7fb6dc7f50d8609c2    3189711  201.npz
4a777d5c9575b7e84359167f1d1a3b1fd135eac1c0950a398a659cb957895910    3525271  202.npz
79edcd36bba17e53b0d77098f68ba01ba24cde43f47cee362ed28c6f9149aafa    5124065  203.npz
2bf3552bc8238c50f957976b69ed44464a240cc3ebb9bcf693698dd3511da640    4212661  205.npz
67acaaf79f4f1e3fc3791871280bebeb7d6e0eabaf78170c84a9f33cdd9c2526    3107920  207.npz
21d7a1043b2a155a35bbd4d10c4db7b16070e0520bde0a5fb10c5fc8049caa5d    4400900  208.npz
dd11a422ae430fbf3e18aea54e0fe1eb427bd39c8e56472ca5b7cd9accf2ce40    4995349  209.npz
8193546a1f53bce60417cca11c0fb753215b0e2fa142a69d028c5e783a638791    4331033  210.npz
746b2c699e8f69342ddaf4b33c9dee15bb00078d6703a95ea42d48e62265a298    4639359  212.npz
dbb57412e8bd2129affe41cb9d048516322d423dbeb28f74094ffefed08dc7ec    5073180  213.npz
195c576f92fdec550c64fd1fe33dd1a75f754a090463242f185d7878662940f6    3815925  214.npz
51fa489a6cf6d50ff2c23ec569069f6ff9e2fbf7d03c6e65003fbbc812de9474    5597947  215.npz
b3587a607d29ede7e9c82c8f1e0b75c557a77a5dc5f08c9dc404674d30e6f3a5    3686848  219.npz
952040a63b4bb6c7abfad7e956ccf5ba89641255d500ed5ae519a70158305178    3372982  220.npz
e12a8f388bb00222a115d23a6011e195ad33c199245abc5e72a73f23faec72e3    4044528  221.npz
0a30471d24dd89aab71a385bfb97a78e0e20707e73c0ef6e32dce2a955e841fd    4089083  222.npz
b9bc3297f03645ae4350bbf7fff90869a1b18d6b56305449f85dd00b0a1889b0    4296026  223.npz
073ef63c9c383023c6b31ad255cf354bb86698c519394b91ab10cd37c0307513    3494566  228.npz
76d88f060be18a75dd4ce94a32a1c8dd14a6c616dc74cd718e5a4253bc5709f2    3778217  230.npz
cb43c8dc76ed830dfec79bcc253d7b67c39ef923425832878ca4f5b89422019f    2613271  231.npz
c72eebc2e3ac4423b1dd24be27bed6c21c64fa94b9488a3fccf21697671e5c95    2909866  232.npz
07574ef78aed9d2ab5be411bfeb9c9fdf51e7d24aee7d89130c781cdd2e1f4fc    5283071  233.npz
89c35bc501acfa88e058f393310f6411a68a9a44f1bdebb3084069104b4ab932    4511622  234.npz
ec5efe7ba37aebe3c0772dd22ef9c101cbf3607db27aa2a56654c255b80021e3       1938  meta.json

# caches/v10  files=45  bytes=167868618  aggregate=82b9a593dcf23fa4ffc60b44c2fe7da02313dfe7d69dfbe64d85c38b4aa78b14
a9676b8d1ce997854363db63fb7e570581ea4fbbcfafc697b405a5284d4bbe63    3676956  100.npz
12a919051498a5f060c93d15640e64eedbc3d0a47b6d05f8dc5546d528d50150    3070898  101.npz
3e7da1c8fa2315d5cd45d0bdbebbb9239142fb548f1beb6ffbd093aaf068735e    3449110  103.npz
c6372d5392294a9d7bf4f1734108f0571dd3aceb5523e9c00bf18aea2484414e    4311976  105.npz
ad8fb7695f7a87a67b0e5fe0d3a04ca6b4f423cbd276ac4dfe73b29bdac2eb60    3483268  106.npz
73fa45dfea19d935443a20d13d5b0bd2320ce4199aa9c4426d5a4646a84bc427    2977421  108.npz
3221a9f2f56513e88e84c20cbc5a85ddcc54e8e3b9356d0f51da9fe32684ace8    4251100  109.npz
c88cd18ada5edfe76896ad39290d2425bf5fa917d362123ad67a43de0726e4ec    3572783  111.npz
31a49adcdb6c667a27a052ebd85527b4df792496adabd08623e5fdb515bfed98    4154372  112.npz
5e619970acd484e73d96aee64364f53cbe3f5f9328dc61a205d51035c1a26e9e    3058268  113.npz
b1ee3d902b083a348cb587e6f5d6a3704bf7834d0dff99b87c252f2a36b103ab    3145532  114.npz
ae30735f157c8a31ccaa3d4cd5b763529fed097d7a8a069e1b73c43d4e33a718    3254111  115.npz
3f9e34fe6d98070681ac5afc64f631d07ca331b707e746c2bf9418b6b29e3d29    4113767  116.npz
09f04dd02a75dc5cb29ebc9c86b2fe44e97cb63afb966eeffb2757b1fbc8752a    2569082  117.npz
b5d58f61b49287bd473d20f4947425f5ab6fb9dab92a164473906895c218c2e2    3899949  118.npz
9d899113f9a37ac58357867f6e6b91e555367e8f4c6b55cc45b1059b5b0fff73    3432480  119.npz
0ced156d4ba5e844ee53526cae814f5e40e1889627d793e238ad7e900f0683bd    3072018  121.npz
ec346e6bcd3a01807783a1b3a5452bf72e766766350b06902f1d625a0dbafeff    4098285  122.npz
2ad4d9311461aaa662da8abb38c146a6bb72eed04782daf3e26f9d5b79d7f474    2554996  123.npz
de1268a4da38c48de5e52b3d3a4045d7993d5df0b1db01f92cc7e2e85fb3fc64    2737560  124.npz
601bf56d31e4ee04b833f502c334346343dcaa9e648144c7182b2065ea2de3fd    4438800  200.npz
a67a5dd0a13647bb05b7c426aaceaa808bafa97869524bf76c5aa54c5438e75a    3205220  201.npz
80b04c41e2458625ce45af0355dccf43b673a04ded9657a58aa4a52ceaed8c82    3541585  202.npz
f0c1a8957071fa00dd031a3e8a46de42690dbfdc86c7720de390778942e60843    5148723  203.npz
86096346a94045c0475b73e86a86c55b3a88b4e412597af5b9ece07e739f8e5b    4232454  205.npz
073dc5c3e562ed47439f8d181e6b36d5d02f681a6d23b4197924d4945c165c43    3123019  207.npz
0e5e6fe4796aeec86afee5699835424bc84324704ffe50d5ce107e763fc113ac    4422372  208.npz
22ad2689795462998b2ed8fc92b287e05f04250c66e3bdd18146d0758c67705b    5019006  209.npz
4302fd3268343e99ef7bf330b8b072d2b0933ef501e704bf0df4ef4cebaa40e5    4351950  210.npz
23c5c9e120f434825f599d150362cd42b615bf26e548d63940567e78ee335f47    4661337  212.npz
a89cb8e2be7afb4d3042828d0c7e06a9369cba9fe8103b21f607c840b5f46218    5096012  213.npz
d2d3fd5da9df201d98f8c0a4ed4990059e091292106f3cbdacea8c5484fab485    3834828  214.npz
606e961abf277c19184400910c5a22f8d6febfa05e3f35533f7babf59576a334    5625169  215.npz
1300d3402afcd69898fcb75ca7f3746a6471f49001fa8fdce6802a2abc91d43a    3704351  219.npz
3fcd3fd8d93f680b52e6a073bd2262f727765f957733bf53da37b06edb568a06    3389237  220.npz
f68de04ed657ce2261510b1ad72a139784da464b19a7ddd411ff47faea03817a    4063829  221.npz
4c86f0e7ef382a6b5b5c0b2f651cecff4c512bcde55e479efdde21014b59c677    4109349  222.npz
eff617ddebd604a543d9b8097ce82560eb2c4886deee5b8dcc5b3fb71d1c0d11    4317024  223.npz
9493d7081634819bb5621778e877aad6d0797868c0e8f2ea0924b723ffe925e1    3511600  228.npz
a4c683cbf7228f7cd76149d561626f3326b8223f66e156a96877b2364ae6bd07    3796600  230.npz
0b4a4e19aa87b61558282b342d1a53682ff3a43cb1d0349d862a16dc2a22e8e8    2625937  231.npz
2c47316dd2f822d3deefc6564440f454944c4c4e2ac001a27110f162e1a10a36    2923934  232.npz
abe0b62d097aa8824d55d904d5eb79e828d6410ee56796d6626a0e653bf8b9dd    5308309  233.npz
dfc6ecd29ceeab19800d3bc5ce49eb9d4820c18a5841c9b9560175693574bda5    4532103  234.npz
ec5efe7ba37aebe3c0772dd22ef9c101cbf3607db27aa2a56654c255b80021e3       1938  meta.json
```

- 2026-08-12 — **Codex acceptance of `PREP_M4_ASSET_FREEZE_PASS` and decisions
  A-E.  Design only; no M0-M4 aggregation, detector replay, join replay or
  sealed-value access.  Status remains `draft`.**

  **Acceptance.**  The frozen result is accepted.  Its four aggregates, 104
  per-file hashes and 44/44 shape/count checks are inherited unchanged.  This
  acceptance says that the named bytes and stored structure are identified; it
  does not say that detector peaks, the generation runtime or M4 are already
  reproducible.

  **A — accept dual-source identity evidence, with a strict reusable
  protocol.**  The connector and mounted filesystem are adequately bound here
  by the complete 90/90 size crosswalk plus 4/4 independent aggregate
  recomputations.  The runtime contract now registers the only circumstances
  under which this split-source method may be reused: exact folder ID and
  expected set, fresh full re-enumeration, complete size crosswalk, per-file
  SHA-256 and independent canonical fold.  It is an identity attestation only;
  it cannot attest runtime or semantic reproducibility.

  **B1 — accept this source snapshot once, but do not treat measurement-after-
  registration as the future standard.**  No M0-M4 result had been opened when
  the names were frozen, so the exact seven-name lists may serve as the
  historical snapshot's contract.  This differs from the corrected MIT-BIH
  expected set: publisher `RECORDS` supplied an external authority there,
  whereas directory contents supplied the source names here.  Consequently all
  future checks use today's exact name lists prospectively and fail on missing
  or extra files.  The five V9 zip archives remain outside the active producer
  contract because no registered step imports or reads them; presence is
  recorded, and use would require a new explicit contract rather than silent
  expansion.

  **B2 — source identification is hash-complete but semantic mapping still
  receives a static pre-execution check.**  Before `detect_r()` is called, the
  implementation must verify the registered function/call-site map against the
  exact frozen V10 `frontend.py` and `data.py` hashes.  This is read-only source
  inspection, not detector execution.  Failure is
  `M4_SOURCE_MAP_UNVERIFIED`, makes M4.0 condition 1 false and reaches the
  already-registered input-absent branch; no source is substituted.

  **B3 — accept the runtime lineage link, not runtime reproducibility.**
  SHA-256 and stored shape reads do not depend on the Colab numpy version, so
  using CPython 3.12.13 / numpy 2.0.2 for the freeze does not invalidate its
  PASS.  The historical identity link to the registered runtime is sufficient
  for the asset-freeze gate.  Whether CPython 3.12.3 / numpy 2.5.1 / scipy
  1.18.0 / wfdb 4.3.1 can stand and reproduce all 22 DS1 counts remains M4.0
  condition 2 and has not passed.

  **C — retain M4 (option a).**  Missing stored peaks make detector replay
  necessary; they do not establish that replay is impossible.  More
  importantly, Q3 fixed Holm at H1-H4 precisely to prevent the family from
  changing after M4 feasibility became known.  Removing H2/H3 now would be the
  structurally conditional change Q3 forbids and would require a cascading
  rewrite of the question, three earlier Codex decisions, controls, gates,
  schema and decision tree.  The registered design already has the honest
  failure path: exact-runtime installation and 22/22 count reproduction are an
  implementation-stage feasibility gate; failure makes H2/H3 `UNEVALUABLE`,
  assigns p=1 only inside four-family Holm and terminates as
  `MECHANISM_UNRESOLVED_INPUT_ABSENT`.  No hypothesis, gate or multiplicity
  family changes.

  **D — promote and classify the constants.**  V10 source `1a0c66c8…` and V10
  cache `82b9a593…` are the M4 input contract because Leg 2 consumes the V10
  positional rows.  V9 source `ffb5679c…` and cache `25cd7952…` are
  corroborating rebuild evidence, not substitute inputs.  The operative M4
  body now carries full digests, Drive IDs, counts/bytes, fixed source-name sets
  and the exact V10 `frontend.py`/`data.py` hashes.  `v15b_local.py` remains a
  Leg 1 producer only.

  **E — approve a separate `PREP_M4_RR_EQUIVALENCE`, not M4 implementation.**
  After its own user approval and before implementation approval, a read-only
  preflight will compare only the stored V9/V10 `rr` values for all 44 records,
  after both cache identities reverify.  It never opens `y`, DS2 per-beat
  labels or probabilities.  Exact value equality (paired NaNs equal) must pass
  44/44.  `V9_V10_RR_LINEAGE_DIVERGED` leaves the spec draft and returns to
  Codex; there is no tolerance, averaging or preferred-lineage selection.
  Keeping this independent prevents an additional lineage measurement from
  being hidden inside M4 implementation and closes the count-only inference at
  negligible cost.

  **Next step.**  Merge this design PR only after review.  Then obtain separate
  user approval for `PREP_M4_RR_EQUIVALENCE`; Claude runs and records only that
  preflight.  Codex accepts its result before the user may promote this spec.
  Implementation approval, M0-M4 execution approval and every sealed analysis
  remain later, separate decisions.

- 2026-08-12 — **`RR_VALUE_IDENTICAL_44_OF_44`.  Read-only value-level RR
  equivalence; no detector replay, no M0-M4 aggregation, no implementation.**

  *Scope and authority.*  The user separately approved the read-only
  `PREP_M4_RR_EQUIVALENCE` scope only.  This is not implementation approval and
  not M0-M4 execution approval; `status` stays `draft`.  Gate checked first:
  PR #105 merged to `main` at `7c664ab`, carrying the frozen M4 identity
  constants, the `PREP_M4_RR_EQUIVALENCE` section and the dual-attestation
  standard this run follows.

  *Measurement split, per the registered dual-attestation standard.*  Drive
  folder IDs, expected-set membership and per-file byte sizes were **re-enumerated
  fresh** by Claude Code through the connector on 2026-08-12; the 2026-08-11
  listing was **not** inherited, as the standard requires.  Per-file SHA-256,
  aggregates and the `rr` arrays were read by the user in Colab with Drive
  mounted, because this container still cannot stream 334,932,996 B.  The two
  halves are bound by measurement: **45/45 byte sizes agree in each cache
  (90/90 overall)**, and both aggregates were **independently recomputed here**
  from their own `(name, bytes, sha256)` triples through `hash_file_set()`'s
  canonical fold.

  *Gate 1 — cache identity, re-verified before any array was read.*

  | cache | Drive ID | files | missing / extra | bytes | aggregate |
  |---|---|---|---|---|---|
  | V9 | `1TXLX14RHA5u1dIUiYt36k2dcT5lpm5RY` | 45/45 | 0 / 0 | 167,064,378 | `25cd7952…` **= registered** |
  | V10 | `1I6iugsrHwJjjpLVS8TVp-aDkVwpdmJxF` | 45/45 | 0 / 0 | 167,868,618 | `82b9a593…` **= registered** |

  Both equal the constants in §"Frozen M4 identity constants".  Because the
  aggregate is a canonical fold over **every** `(name, bytes, sha256)` triple,
  this equality also proves that **all 90 per-file digests are unchanged since
  the 2026-08-11 freeze manifest** — no file needed re-listing to establish it.

  *Gate 2 — `rr` value comparison, 44 records.*  Each record NPZ was opened with
  `allow_pickle=False` and **only the `rr` member was materialised**; `y` was
  never indexed.  Record name sets are identical, every array is `(n, 7)`
  `float32`, and every `n` equals both `meta.json[n]` and the frozen ledger's
  `cache_n`.  Value comparison was exact — `(a == b) | (isnan(a) & isnan(b))` —
  with no tolerance, rounding, averaging, repair or lineage selection anywhere.

  **Result: 44 of 44 records value-identical.  `first_mismatch` is null.**
  Split totals from the compared records reproduce DS1 50,551 · DS2 49,289 ·
  total 99,840.

  *Two facts stronger than the registered criterion, recorded but not used to
  decide.*

  1. **All 44 records are byte-identical at the `rr` array level**, not merely
     value-identical.  The registered verdict rests on value identity; byte
     identity is reported as a strictly stronger observation.
  2. **No NaN appears in any `rr` array in either lineage** (0/0 in all 44
     records), so the paired-NaN clause never fired.  This is consistent with
     `rr_features` applying `nan_to_num`: the endpoint "no neighbour" marker is
     a stored literal `0.0`, not a NaN — the same reading already registered in
     §"What the canonical bundle does and does not contain" item 7 and in Q5.

  *What this establishes.*  The lineage claim that V10 is a pure `pw` add-on
  over V9's row selection is now supported **at value level**, not only by
  counts and structure.  Previously the evidence was byte-identical `meta.json`,
  44/44 `rr.shape`, a single added NPZ member, and a byte-identical
  `frontend.py`.  Two independently rebuilt caches now carry bit-for-bit
  identical RR content for all 99,840 rows, which is what a shared row selection
  predicts and what a divergent one could not produce.

  *What it does not establish.*  It is not evidence that detector peaks were
  reproduced, that the registered runtime can be installed, or that M4 is
  feasible.  **M4.0 condition 2 remains unsatisfied** and is untouched by this
  preflight.  The measurement environment was Colab `python 3.12.13 /
  numpy 2.0.2`, again **not** the registered `CPython 3.12.3 / numpy 2.5.1 /
  scipy 1.18.0 / wfdb 4.3.1`; that is irrelevant to SHA-256 and to reading
  stored arrays, and the runtime contract already says so.

  *Seals.*  `y` never read, DS2 per-beat labels never opened, no V10
  probability, no association, no S PR-AUC, no training, `detect_r()` not
  called, beat join not re-run, no Drive file created, modified, moved or
  deleted, and `mit-bih/q5d_order_preserving_beat_join.py` imported read-only
  and unmodified.

  **PREP 통과는 EXP-2026-008 구현 승인 또는 M0-M4 실행 승인이 아니다.**

  *Per-record result (44/44).*

```text
record  split     n  shape      dtype     value_identical  byte_identical  nan
   100  DS2   2271  (n, 7)     float32   True             True            0/0
   101  DS1   1862  (n, 7)     float32   True             True            0/0
   103  DS2   2083  (n, 7)     float32   True             True            0/0
   105  DS2   2566  (n, 7)     float32   True             True            0/0
   106  DS1   2027  (n, 7)     float32   True             True            0/0
   108  DS1   1759  (n, 7)     float32   True             True            0/0
   109  DS1   2528  (n, 7)     float32   True             True            0/0
   111  DS2   2123  (n, 7)     float32   True             True            0/0
   112  DS1   2537  (n, 7)     float32   True             True            0/0
   113  DS2   1794  (n, 7)     float32   True             True            0/0
   114  DS1   1875  (n, 7)     float32   True             True            0/0
   115  DS1   1952  (n, 7)     float32   True             True            0/0
   116  DS1   2397  (n, 7)     float32   True             True            0/0
   117  DS2   1534  (n, 7)     float32   True             True            0/0
   118  DS1   2277  (n, 7)     float32   True             True            0/0
   119  DS1   1987  (n, 7)     float32   True             True            0/0
   121  DS2   1862  (n, 7)     float32   True             True            0/0
   122  DS1   2474  (n, 7)     float32   True             True            0/0
   123  DS2   1517  (n, 7)     float32   True             True            0/0
   124  DS1   1613  (n, 7)     float32   True             True            0/0
   200  DS2   2598  (n, 7)     float32   True             True            0/0
   201  DS1   1961  (n, 7)     float32   True             True            0/0
   202  DS2   2134  (n, 7)     float32   True             True            0/0
   203  DS1   2972  (n, 7)     float32   True             True            0/0
   205  DS1   2644  (n, 7)     float32   True             True            0/0
   207  DS1   1859  (n, 7)     float32   True             True            0/0
   208  DS1   2572  (n, 7)     float32   True             True            0/0
   209  DS1   3004  (n, 7)     float32   True             True            0/0
   210  DS2   2638  (n, 7)     float32   True             True            0/0
   212  DS2   2747  (n, 7)     float32   True             True            0/0
   213  DS2   2887  (n, 7)     float32   True             True            0/0
   214  DS2   2257  (n, 7)     float32   True             True            0/0
   215  DS1   3360  (n, 7)     float32   True             True            0/0
   219  DS2   2153  (n, 7)     float32   True             True            0/0
   220  DS1   2046  (n, 7)     float32   True             True            0/0
   221  DS2   2427  (n, 7)     float32   True             True            0/0
   222  DS2   2477  (n, 7)     float32   True             True            0/0
   223  DS1   2590  (n, 7)     float32   True             True            0/0
   228  DS2   2053  (n, 7)     float32   True             True            0/0
   230  DS1   2255  (n, 7)     float32   True             True            0/0
   231  DS2   1570  (n, 7)     float32   True             True            0/0
   232  DS2   1780  (n, 7)     float32   True             True            0/0
   233  DS2   3066  (n, 7)     float32   True             True            0/0
   234  DS2   2752  (n, 7)     float32   True             True            0/0

44/44 value_identical · 44/44 byte_identical · NaN 0 · DS1 50,551 · DS2 49,289 · total 99,840
```
