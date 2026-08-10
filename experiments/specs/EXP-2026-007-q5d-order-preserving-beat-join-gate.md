---
experiment_id: EXP-2026-007
substage: Q5D_BEAT_JOIN_IDENTIFIABILITY_GATE
title: Q5-D deletion-aware order-preserving beat identity join gate
status: draft
design_owner: codex
implementation_owner: claude
dataset: MIT-BIH
split: DS1_to_DS2_inter_patient
primary_metric: join_min_class_recall
parent_primary_metric: S_PR_AUC
created: 2026-08-10
---

# Status boundary

This document specifies one beat-identity join and its falsification gates.  It
does not authorize implementation or execution.  EXP-2026-007 remains
scientifically **NOT RUN**, and its parent spec remains
`approved_for_implementation` only for the separately authorized stages.

The measurement-qualification track and this design track were separated
because they used different files and evidence.  Qualification has now finished
as `MEASUREMENT_QUALIFIED` (canonical run `20260810T005802`, 5/5 gates).  That
result establishes only that the frozen measurement tool passed its registered
gate.  It does not authorize the join or association.

1. Codex may finish this `draft` join design without reading DS2 outcomes.
2. The join still requires design review, explicit user approval, and promotion
   of this file to `approved_for_implementation` before implementation or
   execution.
3. V10 probabilities and the association analysis remain sealed until the
   frozen join passes its own gates and receive their own explicit approval.

# Fixed question

Can one fixed, deletion-aware, order-preserving alignment of raw MIT-BIH
`.atr` R-beat order to the registered processed-beat row order recover a unique,
one-to-one, class-balanced beat identity map strongly enough to support the
parent EXP-2026-007 association analysis?

This is an identifiability question, not the parent scientific association
question.  The only controlled variable in validation is
`SEQUENCE_RELATIONSHIP`:

- `TRUE_ORDER`: the raw RR sequence remains paired with its own record and in
  its original order.
- `BROKEN_ORDER`: the same inputs pass through one preregistered negative-control
  transform that destroys record identity or order.

The join rule does not use P-wave timing, PR discordance, beat class, V10
probability, or any outcome.  Class labels may be used only after matching to
audit DS1 and, after all freezes and approvals, to apply the fixed DS2 support
gate.

# Why now

- Q5-A measured that the stored `t` is not an annotation sample index: direct
  `t` to `.atr` matching recovered only 1.9%, at chance level, with median
  nearest distance `0.222 x RR`.
- Q5-B-0 recovered 25.9% with strict RR keys and 90.5% with a relaxed tie-set
  rule, but failed because `subtype_coverage_balance = 0.368 < 0.80`.  The
  missing 10% was not ignorable.
- Q5-B-0 diagnosis showed that unmatched beats were usually close: p50 nearest
  distance was 0.10 ms and 93.8% lay within twice the tolerance.  Rejection was
  driven by the 5 ms local margin, not by a lack of nearby candidates.
- The audited drop map contains 818 raw beats absent from the processed cohort:
  N 1, S 0, V 0, F 802, Q 15; 92% occur in records 208 and 213.  Therefore a
  valid rule must allow deletions but must not silently accept class-selective
  recovery.
- Raw MIT-BIH and expert P-wave assets now exist and passed PREP_DATA-A, but a
  stable raw-to-processed beat UID has not been demonstrated.
- The frozen measurement qualification passed at the exact preregistered
  per-record floor: 5 of 6 reference records passed, leaving zero record-level
  margin.  DS2 record-macro sensitivity was 0.9476, macro PPV 0.8860,
  many-to-one and cross-beat errors were zero, and the true/chance ratio was
  8.283 [7.460, 9.548].  This is a measured qualification result, not an
  association result.

This design does not reopen `B_SUBTYPE`.  Q5-B-0 used RR keys to recover S
subtype information; this gate asks only whether raw and processed rows have an
identifiable one-to-one identity for the already-fixed parent analysis.

# Inputs

## Available and allowed for rule design or validation

- Synthetic fixtures with known raw-to-processed truth.
- MIT-BIH DS1 raw `.atr` R samples and RR intervals.
- DS1 processed rows, record identity, stored pre/post RR values, and DS1 class
  labels for audit only.
- The already-measured 44-record fingerprint map and the four paced leftovers.
- Q5-B-0 `record_mapping.csv` and its frozen aggregate drop facts.
- Qualification run `20260810T005802`, its frozen manifest, and its
  record-level measurement-quality report.  It may define prespecified
  quality-confound diagnostics but may not change the beat join.
- `ecg_multi.npz` RR provenance: samples, median approximately 268.
- Processed-array RR provenance, but only if its units and conversion contract
  are explicitly documented.  Unit scale must never be estimated by choosing
  the value that creates the most matches.

## Available only after the join rule and code are frozen and execution is approved

- DS2 processed beat class labels, solely for the fixed coverage, class-balance,
  and label-agreement gates.
- DS2 raw `.atr` symbols, solely for the same frozen audit.

DS2 labels must not be used to select the join rule, tolerance, eligibility,
record exclusions, or thresholds.  If a DS2 gate fails, the rule is not revised.

## Forbidden in this substage

- V10 probabilities and all `v10pkg_results/` outcomes.
- DS2 S PR-AUC or any DS2 association statistic.
- P-wave delineation, PR-discordance strata, model training, calibration, or
  checkpoint access.
- Downloads, Drive mutation, or overwriting any existing run bundle.

## Missing or unverified at design time

- A processed-row `beat_uid` linked to the source `.atr` ordinal and R sample.
- A demonstrated contract that processed rows preserve chronological order
  within each record after every filter and concatenation.
- A per-beat keep/drop ledger with the exact source ordinal and drop reason.
- A saved row-permutation map from preprocessing output back to raw input.

The first implementation gate is a provenance-only audit of these items.  If
chronological row order cannot be proven from frozen source code, manifests, or
an already-saved row map, do not infer it from favorable DS1 matching.  Emit
`JOIN_INPUT_ABSENT`.

# One fixed join rule

## 1. Record and order contract

Use only the existing frozen record fingerprint map.  Do not remap records from
DS2 outcomes.  Within each mapped record:

- raw beats are ordered by `.atr` R sample;
- processed beats are ordered by their documented, stable within-record row
  order;
- the first or last beat is ineligible when either pre-RR or post-RR is absent;
- gaps are permitted only on the raw side, representing raw beats removed by
  preprocessing;
- a processed beat may never be mapped twice, and a raw beat may never be mapped
  twice;
- mappings must be strictly monotone in both sequences.

If a processed-side gap is required, stop for that record.  The registered
processed cohort is supposed to be derived from raw beats, so inventing an
unobserved raw source is not allowed.

## 2. Unit conversion and candidate edges

Convert both raw and processed pre/post RR values to integer samples at 360 Hz
using only the declared artifact units and round-half-to-even.  No fitted scale
or record-specific scale search is permitted.

Before conversion, freeze from preprocessing source and manifest whether stored
processed RR was computed before beat filtering or recomputed after filtering.
Reproduce exactly that one semantic on the raw side.  Do not try both and retain
the one with higher coverage.  If the stored semantic cannot be established, or
if reproducing a post-filter RR requires an unavailable per-beat keep/drop
ledger, emit `JOIN_INPUT_ABSENT`.

A raw beat `i` and processed beat `j` form a candidate edge iff both conditions
hold:

```text
abs(raw_pre_samples[i]  - processed_pre_samples[j])  <= 1
abs(raw_post_samples[i] - processed_post_samples[j]) <= 1
```

The one-sample tolerance is fixed because both artifacts ultimately refer to a
360 Hz discrete signal.  It replaces the rejected 5 ms local margin; it is not
widened when RR patterns repeat.

Beat symbols and labels do not enter candidate construction.

## 3. Maximum-cardinality monotone matching

Among candidate edges, find a strictly monotone one-to-one matching with the
maximum number of matched processed beats.  There is no secondary score, margin,
distance preference, label preference, or record-specific penalty.

An edge is **certified** only when it appears in every maximum-cardinality
monotone matching.  An implementation may identify such forced edges with
prefix/suffix dynamic-programming counts; it must not select one arbitrary
optimal path.  Edges that change across equally optimal paths are `AMBIGUOUS`
and remain unmatched.

This is the complete primary rule.  Q5-B-0's aggregate drop map is used to
audit the resulting gaps and to construct synthetic fixtures, not to choose
among ambiguous pairings.

# Synthetic fixtures

All fixtures are fixed before DS1 audit and have known true identities.  The
rule must recover 100% of identifiable true pairs, create zero false pairs, and
mark every deliberately non-identifiable repeated segment `AMBIGUOUS` in:

1. identity/no-drop sequence;
2. one isolated raw deletion;
3. consecutive deletions;
4. Q5-B-0-like F/Q deletion counts, including concentration in two records;
5. repeated coupling intervals with one unique flanking context;
6. a perfectly repeated segment with two equally optimal alignments;
7. +/-1-sample quantization on either RR component;
8. a declared seconds-to-samples conversion;
9. an intentionally wrong unit declaration, which must stop rather than fit a
   scale;
10. row-order corruption, which must fail the monotonicity/provenance gate.

Any synthetic false match terminates the rule as `JOIN_RULE_FALSIFIED` before
DS1 is inspected.

# Negative controls

Each control reruns the full candidate construction, maximum matching,
certification, and all audit statistics.  Nothing except
`SEQUENCE_RELATIONSHIP` changes.

1. **Wrong record:** derange raw records among processed records within frozen
   record-length quintiles.  This falsifies the possibility that common RR
   distributions alone create an apparently successful join.
2. **Order shuffle:** permute complete raw-beat RR pairs within record while
   carrying their audit symbols together.  This falsifies the possibility that
   the multiset of RR pairs, without chronology, is sufficient.
3. **Circular shift:** apply a non-zero within-record circular shift to the raw
   beat sequence.  Allowed offsets are all offsets from 1 through `n-1`; draw
   uniformly.  This preserves local autocorrelation more strongly than a full
   shuffle and falsifies a join driven by repetitive rhythm rather than exact
   beat position.

The wrong-record control is skipped only for a length bin containing fewer than
two records; the binning is then coarsened deterministically until derangement
is possible.  Records are never dropped to improve a control.

# Primary validation statistic and empirical null

On DS1, after matching, map raw symbols to the frozen parent AAMI classes.  For
each processed class `c in {N, S, V}` define:

```text
correct_recall_c = certified pairs with agreeing class c /
                   all processed DS1 beats of class c
J_min            = min(correct_recall_N, correct_recall_S, correct_recall_V)
```

Class agreement is an audit target and never an input to the join.  `J_min` is
chosen instead of pooled accuracy so a dominant N class cannot hide loss of S
or V beats.

Generate 10,000 replicates for each negative-control family with master seed
`2026017`.  At replicate `b`, define the family-wise null statistic as:

```text
J_null_max[b] = max(J_wrong[b], J_shuffle[b], J_shift[b])
```

Report the full distribution, median, q95, q99, and
`signal_to_null = J_min_TRUE / max(q95(J_null_max), 1 / n_processed_DS1)`.
The finite-sample floor prevents division by zero from creating an infinite
claim.

Use 2,000 record-cluster bootstrap replicates, seed `2026018`, carrying all
beats of a sampled record together.  Report the 95% CI of
`J_min_TRUE - q95(J_null_max)`.  The null is generated once under the frozen
rule; bootstrap uncertainty applies to the true record sample and is not a
license to retune the rule.

# Fixed acceptance and stopping gates

The DS1 rule qualifies only if every gate passes:

1. synthetic exact recovery and ambiguity fixtures pass with zero false pairs;
2. record/order provenance is documented, and all mappings are monotone and
   one-to-one;
3. overall certified coverage is at least 0.95;
4. certified S-beat coverage is at least 0.95;
5. each of N, S, and V certified coverage is at least 0.90;
6. `class_coverage_balance = min(class coverage) / overall coverage >= 0.80`;
7. every eligible DS1 record has coverage at least 0.80 and
   `record_coverage_balance = p10(record coverage) / macro(record coverage) >= 0.80`;
8. class agreement among certified pairs is at least 0.995 overall and at least
   0.98 in each of N, S, and V;
9. `J_min_TRUE > q99(J_null_max)`;
10. `signal_to_null >= 5.0`;
11. the record-bootstrap 95% CI lower bound for
    `J_min_TRUE - q95(J_null_max)` is greater than zero;
12. for every record with processed S support,
    `S_share_inflation = (record share of certified S) /
    (record share of all processed S) <= 1.25`.

These thresholds preserve the Q5-B-0 principle that 90% pooled coverage is not
enough when missingness is class- or record-selective.

This last gate detects join-induced concentration without rejecting a record
merely because the unjoined source cohort genuinely contains many S beats.

After the rule, source hash, tests, environment, thresholds, and DS1 report are
frozen, the same support gates 2-8 and 12 apply once to DS2.  DS2 does not rerun
the null and cannot change any constant.  If a DS2 gate fails, emit
`JOIN_SELECTION_BIASED` and stop before opening V10 probabilities.

# Rule relaxation and multiplicity

There is no confirmatory relaxation path inside this substage.  In particular,
do not widen the one-sample RR tolerance, accept one arbitrary optimal path,
remove hard records, change record bins, or lower a class/record gate after DS1
or DS2 results are seen.

If a sensitivity appendix is requested later, preregister its complete finite
candidate set first.  For each candidate, regenerate all three null families
under that candidate.  Within every replicate take `maxT` over both the control
families and all candidate rules.  Compare the observed best rule only with
that expanded max-null.  A relaxed rule may not inherit the primary rule's
lower cutoff and may not rescue EXP-2026-007 without a new approved spec.

# Decision tree

1. **`JOIN_INPUT_ABSENT`**: stable processed row order, unit provenance, record
   identity, or another required identity artifact is missing.  Stop: the
   mapping is not presently answerable.
2. **`JOIN_RULE_FALSIFIED`**: any synthetic false match occurs, TRUE fails to
   exceed the max-null, or the signal/null gates fail.  Stop; ordinary RR
   repetition can explain the apparent mapping.
3. **`JOIN_SELECTION_BIASED`**: pooled recovery looks high but a class, record,
   concentration, or agreement gate fails.  Stop; do not analyze the selected
   subset.
4. **`JOIN_UNRESOLVED`**: all inputs exist but repeated RR patterns leave too
   many pairs ambiguous to pass coverage.  This is the explicit valid
   "nothing identifiable" result.
5. **`JOIN_IDENTIFIABLE`**: all frozen DS1 and DS2 join gates pass.  This permits
   creation of a beat identity map only.  It is not a P-timing association and
   does not authorize opening V10 probabilities without the parent's next
   explicit approval.

# If the join is impossible in principle

If multiple raw beat histories produce the same stored processed RR sequence
and different beat maps, and no stored field distinguishes them, the map is not
identifiable from current artifacts.  Do not promote a convenient optimal path.

The preprocessing stage would have made the join deterministic by saving one
ledger row per raw beat with:

- dataset and version;
- record ID;
- raw `.atr` ordinal;
- raw R sample;
- raw annotation symbol;
- `kept` boolean and exact drop reason;
- processed row index after every concatenation or permutation;
- preprocessing source commit and configuration hash;
- `beat_uid = SHA256(dataset_version | record | atr_ordinal | r_sample)`.

The same `beat_uid` should have been carried into every per-seed probability
file.  If `JOIN_INPUT_ABSENT` or `JOIN_UNRESOLVED` fires, acquiring or
reconstructing this ledger from a verified historical preprocessing replay is
the only valid next route.  Guessing a UID from `t`, RR rank, class, or model
score is not.

# Parallel-work contract

| Track | Owner | May do now | Must not do |
|---|---|---|---|
| Q: measurement qualification | Claude | Complete: `MEASUREMENT_QUALIFIED`, run `20260810T005802` | Reinterpret qualification as join or association approval; change the frozen gates |
| J: beat-join design | Codex | Maintain this draft; specify rule, controls, null, and stops | Write/run join code; inspect DS2 labels/probabilities |
| J implementation | Claude, only after approval | Implement exactly the approved join spec | Touch qualification files or revise scientific rules silently |
| Association | none yet | Nothing | Open V10 outcomes or calculate S PR-AUC |

Qualification passed with exactly 5 of 6 reference records above the
preregistered per-record floor.  This zero-margin pass must be reported as such;
the join cannot promote it to evidence of uniform measurement quality.

# Qualification-derived constraints for later association

These constraints use only the completed outcome-blind qualification report and
are frozen before V10 probabilities or DS2 class outcomes are opened.  They do
not change the join rule or its gates.

## Record 222: unresolved annotation-density interpretation

Record 222 had sensitivity 0.9602, PPV 0.4873, 1,257 expert annotations, and
2,477 detections.  Its annotation-density PPV ceiling is 0.5075, so the observed
PPV is close to that ceiling.  Qualification cannot distinguish whether the
unannotated detections are valid but unpublished P waves or detections in beats
without a true P wave.

Therefore:

1. record 222 remains in the primary join and later primary association because
   the frozen qualification decision passed with one per-record failure allowed;
2. do not call unannotated detections false positives, true positives, or
   missing expert labels without additional expert evidence;
3. do not exclude, down-weight, impute, or retune record 222 in the primary
   analysis;
4. report its join coverage, P-measurement availability, eligible S/non-S
   support, and record-specific association direction separately;
5. preregister one leave-222-out sensitivity using the unchanged join, strata,
   SHAM, and statistic.  It is diagnostic and cannot replace the primary result;
6. if a positive primary association changes sign when 222 is removed, or if
   record 222 supplies more than the parent's fixed 50% ceiling of eligible S
   beats, attach the flag
   `ANNOTATION_DENSITY_SENSITIVE`.  Do not promote a general P-timing statement
   from that result even if the pooled primary threshold passes.

The beat join for 222 is judged only by raw-to-processed identity.  Its low
expert-reference PPV must not be allowed to make a correct beat join fail, and a
good beat join must not be used to resolve the biological meaning of its
unannotated P detections.

## Record 231: measurement-quality/model-failure covariance

Record 231 had the lowest qualification sensitivity, 0.7859, while its PPV was
0.997.  Independently, Q5-A placed it in the worst quartile for all four models,
with S PR-AUC approximately 0.001-0.002.  Measurement quality and model failure
are therefore known in advance to be poor in the same record.  A later
association could partly reflect this covariance rather than beat-specific
P-timing information.

The parent's within-record, within-RR-bin `SHAM` remains the primary negative
control because it preserves record membership, missingness count, model-score
distribution, and record-level measurement quality while breaking beat-specific
P-timing alignment.  In addition, the later association report must include:

1. a fixed leave-231-out diagnostic using the unchanged primary procedure;
2. record 231's measurement-valid/missing counts by the frozen RR and
   concordance strata;
3. the single outcome-blind measurement-availability indicator already defined
   by the frozen delineator: `P_VALID = 1` iff it returned a P peak inside the
   frozen 40-300 ms window and the existing physiological validity checks
   passed; no new confidence score or threshold is created;
4. a comparison of the primary P-timing statistic with the measurement-quality
   control statistic, without selecting the larger one;
5. the flag `MEASUREMENT_QUALITY_CONFOUNDED` when both conditions hold:
   - the leave-231-out P-timing DiD changes sign or falls below 0.015; and
   - the measurement-quality control reaches or exceeds the absolute primary
     P-timing statistic under its own recomputed null.

If that flag fires, report the numerical association but do not claim robust
failure-associated P timing.  The valid conclusion is that the present design
cannot separate P timing from measurement-quality covariance.  No alternative
quality threshold, record exclusion, or detector is tried inside EXP-2026-007.

The measurement-quality control statistic is fixed as
`DiD_quality = [PRAUC_P_VALID - PRAUC_P_INVALID]_TRUE -
median([PRAUC_P_VALID - PRAUC_P_INVALID]_QUALITY_SHAM)`, where
`QUALITY_SHAM` permutes the complete `P_VALID` assignment within record and the
same frozen RR bin.  Its 10,000-permutation null is recomputed separately; it
cannot reuse the P-alignment SHAM cutoff.  If either validity stratum lacks the
parent's minimum support, report `QUALITY_CONTROL_UNDERPOWERED` rather than
changing the indicator or pooling records.

The leave-222-out and leave-231-out diagnostics are prespecified sensitivity
analyses, not a two-record search.  They are never used to choose a favorable
subset, and no other record-deletion result is promoted.

Likewise, the measured PR-discordance threshold `2.000` is sample-quantized and
has mass at the boundary.  This join does not use that threshold.  Before any
association execution, the parent spec must separately freeze whether equality
belongs to the concordant group, discordant group, or a boundary stratum.  No
choice may be made after viewing DS2 outcomes.

# Inputs and outputs contract for a future approved implementation

## GitHub inputs

- `experiments/specs/EXP-2026-007-q5d-expert-validated-pwave-timing-audit.md`
- `research/HANDOFF_2026-08-10_Q5D_beat_join_to_codex.md`
- the approved qualification freeze manifest and decision only;
- Q5-B-0 `record_mapping.csv` registered through `research/ASSETS.md`.

## Files allowed to change

During the current design task, only this spec may change.

After separate approval, implementation is limited to:

- this spec's Decision log and status;
- `mit-bih/q5d_order_preserving_beat_join.py`;
- `mit-bih/test_q5d_order_preserving_beat_join.py`;
- `notebooks/quest54_q5d_order_preserving_beat_join.ipynb`.

Do not modify Claude's qualification files:
`mit-bih/q5d_qualify_*`, `notebooks/quest53_*`, or
`research/PLAN_2026-08-10_*`.

## Future Drive run directory

`MyDrive/MedKOS/ecg-model/runs/<timestamp>_EXP-2026-007_q5d_beat_join/`

Required outputs:

- `config.json` and `manifest.json` with code, input, unit, and environment
  hashes;
- `decision.json` with the first stopping reason;
- `synthetic_fixture_results.csv`;
- `join_map.parquet` containing only stable IDs and join audit fields, no V10
  probability;
- `unmatched_and_ambiguous.csv`;
- `record_class_coverage.csv`;
- `negative_control_null.npz` and `null_summary.json`;
- `bootstrap.json`;
- `log.txt` and a human-readable `summary.md`;
- figures showing per-record coverage, per-class coverage, ambiguity, and the
  full max-null distribution.

# Implementation checklist

- [ ] User approves this draft and status changes to `approved_for_implementation`
- [ ] Qualification passes before any join execution
- [ ] Provenance/order audit passes before DS1 matching
- [ ] Synthetic fixtures run before DS1 audit
- [ ] DS1 rule and all hashes freeze before DS2 class audit
- [ ] No DS2 outcome or V10 probability is opened during rule selection
- [ ] All negative controls rerun the complete matching rule
- [ ] DS2 support failure stops before V10 access
- [ ] Complete run bundle is saved without overwriting prior assets
- [ ] Executed notebook and measured join decision are reviewed separately

# Decision log

- 2026-08-10 — Codex draft.  Chose one deletion-aware monotone rule based on
  integer-sample pre/post RR candidate edges.  Replaced Q5-B-0's local 5 ms
  margin with a global identifiability criterion: retain only edges common to
  every maximum-cardinality monotone matching.  Registered wrong-record,
  order-shuffle, and circular-shift max-null controls; class and record lower-tail
  coverage gates; an explicit `JOIN_UNRESOLVED` branch; and the historical
  `beat_uid` ledger required if current artifacts are non-identifiable.  This
  document is design-only and does not change EXP-2026-007 from NOT RUN.
- 2026-08-10 — Incorporated the completed outcome-blind qualification
  (`MEASUREMENT_QUALIFIED`, canonical run `20260810T005802`).  Prespecified
  record 222 as annotation-density-uncertain without excluding or weighting it,
  and record 231 as a measurement-quality/model-failure covariance risk with
  fixed leave-one-record-out and `P_VALID`/`QUALITY_SHAM` diagnostics.  Replaced
  an absolute per-record S-share gate with source-relative share inflation so
  the join is tested for selection bias rather than natural patient prevalence.
