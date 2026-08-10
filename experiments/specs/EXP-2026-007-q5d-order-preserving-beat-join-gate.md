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
2. The user may separately approve the design and promote this file to
   `approved_for_implementation`; that approval means only that Claude may write
   the implementation.
3. Claude may implement the frozen design on a `claude/<task>` branch without
   running it on the registered data.
4. The user must give a second, explicit approval before the implemented beat
   join is executed on the registered data.
5. Only after execution, preservation of the Drive run bundle, notebook commit,
   and run ingestion may the measured join decision be reviewed.

Design approval in step 2 and data-execution approval in step 4 are independent.
Neither one authorizes opening V10 probability values or running the association.
Those remain sealed until the join passes its own gates and the user gives a
further explicit association approval.

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
- Raw MIT-BIH and expert P-wave assets now exist and passed PREP_DATA-A.  The
  subsequent preflight established `SOURCE_REPLAY_PROVEN` for the V9/V10
  preprocessing lineage, but no stable cross-lineage mamba-to-V9/V10 beat UID is
  stored.
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
- The registered V9 and V10 cache `meta.json` ledgers and the fixed 44-record
  counts.  The cache row order is `detect_r()` detection order, not `.atr`
  ordinal order.
- The registered canonical `mamba_data.npz` and its committed lineage metadata.
  An unzipped derivative is not substituted unless it is first hash-linked to
  the canonical asset.

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

## Provenance fixed before implementation

The preflight decision is `SOURCE_REPLAY_PROVEN` (A).  It proves the V9/V10
preprocessing lineage: exact source, environment, MIT-BIH 1.0.0 input,
filtering, row selection, and within-record row order.  V9 and V10 independently
rebuilt caches have identical `n` and split metadata for all 44 records.  Their
rows are materialized, so this design consumes the registered caches rather than
rerunning `detect_r()`.

Here, **replay** means deterministic reconstruction or verification of
preprocessing lineage only.  It does not mean regenerating model probabilities.
`train.py` does not call `keras.utils.enable_op_determinism()`, so GPU learning is
nondeterministic even in the pinned environment.  No model is trained or
retrained in this substage, and no newly generated probability may replace a
registered result.

A does not prove that mamba and V9/V10 contain the same beats.  Eight record
counts differ, by -31 V9/V10 rows in total (DS1 -25; DS2 -6).  It also does not
create a cross-lineage per-beat key: V9/V10 result NPZs store only `prob`, `y`,
and `pid`, so identity remains positional.  The stored `t` is explicitly
ineligible as a key because it restarts at zero per record and accumulates
filtered RR rather than absolute sample time; the observed 1.9% Q5-A join is
consistent with that failure mode.

Under A, `JOIN_INPUT_ABSENT` remains available only for a failed material-input
contract, not for disappointing join performance.  It fires before matching if
any of the following cannot be verified against the registered manifest and
source:

- the canonical mamba asset or its source/meta hashes, 44-record order, counts,
  units, or deterministic drop semantics do not match the registered lineage;
- either V9 or V10 cache/meta asset, its 44 record boundaries, detection-order
  contract, or equality of the V9 and V10 cache ledgers is missing or fails hash
  verification;
- the producer-side positional contract from cache row to result-NPZ row cannot
  be proven, or a result NPZ length/contiguous `pid` block does not equal its
  registered cache boundary, without inspecting probability values; or
- a required artifact has been replaced by an unverified duplicate and cannot
  be linked byte-for-byte to the registered canonical asset.

The absence of a stored cross-lineage `beat_uid` is the identifiability question
answered by the frozen matcher below; it is not, by itself, an A-era
`JOIN_INPUT_ABSENT` condition.

# One fixed join rule

## Leg 1: raw `.atr` to mamba rows

Leg 1 is a deterministic source-replay gate, not a statistical join.  For every
record, order raw annotations by `.atr` sample and replay the three frozen mamba
rules exactly: retain only symbols mapped into the registered N/S/V set; apply
the 150-sample window boundary test using annotation position `pos`; and drop a
whole record only under the source's fewer-than-five-valid-beats rule.  Assign
the resulting kept sequence, in order, to the canonical mamba record slice from
the committed lineage ledger.

After filtering, recompute mamba RR exactly as the source does.  The first
pre-RR is a duplicate of the first available interval, and the last post-RR is a
duplicate of the last available interval; first and last beats are therefore
eligible.  Leg 1 must reproduce every per-record count, split total (DS1 50,576;
DS2 49,295), ordinal order, and stored RR value within the declared numeric
serialization tolerance.  Any mismatch emits `JOIN_RULE_FALSIFIED` with
`failed_leg = LEG1_SOURCE_REPLAY` and stops before Leg 2.  A missing or
hash-inconsistent input instead emits `JOIN_INPUT_ABSENT` as defined above.

## Leg 2: mamba rows to V9/V10 positional rows

Leg 2 is detector-dependent and is not reconstructed from `.atr`.  It consumes
the registered V9/V10 cache rows in their materialized `detect_r()` order and
uses the cache row position as the future result-NPZ position.  It never treats
that position as an `.atr` ordinal and never opens a V10 probability value.

Matching is performed independently inside each frozen record slice.  Global
order-preserving alignment is forbidden: the DS2 deficits in 105, 111, and 222
would shift every later record.  Record boundaries are arithmetic consequences
of the registered ledger, not boundaries inferred from labels or join quality.
The prespecified count strata are:

- equal-count: 36 records;
- mismatched DS1: 108 (-1), 116 (-14), 203 (-2), 208 (-7), 223 (-1);
- mismatched DS2: 105 (-1), 111 (-1), 222 (-4).

The fixed cache ledger is:

| split | V9/V10 records in array order (`record:n@start`) |
|---|---|
| DS1 | `101:1862@0`, `106:2027@1862`, `108:1759@3889`, `109:2528@5648`, `112:2537@8176`, `114:1875@10713`, `115:1952@12588`, `116:2397@14540`, `118:2277@16937`, `119:1987@19214`, `122:2474@21201`, `124:1613@23675`, `201:1961@25288`, `203:2972@27249`, `205:2644@30221`, `207:1859@32865`, `208:2572@34724`, `209:3004@37296`, `215:3360@40300`, `220:2046@43660`, `223:2590@45706`, `230:2255@48296` |
| DS2 | `100:2271@0`, `103:2083@2271`, `105:2566@4354`, `111:2123@6920`, `113:1794@9043`, `117:1534@10837`, `121:1862@12371`, `123:1517@14233`, `200:2598@15750`, `202:2134@18348`, `210:2638@20482`, `212:2747@23120`, `213:2887@25867`, `214:2257@28754`, `219:2153@31011`, `221:2427@33164`, `222:2477@35591`, `228:2053@38068`, `231:1570@40121`, `232:1780@41691`, `233:3066@43471`, `234:2752@46537` |

For the mamba slices, `n` equals the listed cache `n` in the 36 equal-count
records.  The eight exceptions are fixed as `108:1760`, `116:2411`,
`203:2974`, `208:2579`, `223:2591`, `105:2567`, `111:2124`, and `222:2481`;
their mamba starts are recomputed only by cumulative addition in the same frozen
split order.  No observed alignment may alter either ledger.

The tempting hypothesis `V9/V10 rows are a subset of mamba rows` is **not** an
identity axiom.  Mamba applies its boundary rule at annotation position `pos`,
whereas V9/V10 applies it at detector position `p`; an unmatched mamba row and
an unmatched detector row can cancel in the count.  Consequently equal-count
records are not zipped by position or automatically certified.  All 44 records,
including the 36 equal-count records, pass through the same matcher.  A
drop-one/add-one cancellation is falsified whenever the fixed candidate graph
does not uniquely certify the positional mapping; the affected edges remain
`AMBIGUOUS` and the existing coverage, agreement, and selection gates decide the
result.

Within each record, gaps are permitted on either sequence while finding the
maximum-cardinality monotone matching because the two boundary definitions do
not prove set inclusion.  No gap is imputed: every unmatched V9/V10 row remains
unmapped and counts against coverage, while unmatched mamba rows are reported
with their Leg 1 identity.  Each row may be mapped at most once, and certified
mappings must be strictly monotone in both record-local sequences.

### Unit conversion and candidate edges

Convert both mamba and cache pre/post RR values to integer samples at 360 Hz
using only the declared artifact units and round-half-to-even.  No fitted scale
or record-specific scale search is permitted.

The mamba side uses the Leg 1 source-replayed, post-filter RR with its endpoint
duplication semantics.  The V9/V10 side uses the registered cache RR semantic.
Both semantics and units are frozen from source and manifest before any match.
Do not try alternate RR definitions and retain the one with higher coverage.

A mamba beat `i` and V9/V10 cache row `j` in the same record form a candidate
edge iff both conditions
hold:

```text
abs(mamba_pre_samples[i]  - cache_pre_samples[j])  <= 1
abs(mamba_post_samples[i] - cache_post_samples[j]) <= 1
```

The one-sample tolerance is fixed because both artifacts ultimately refer to a
360 Hz discrete signal.  It replaces the rejected 5 ms local margin; it is not
widened when RR patterns repeat.

Beat symbols and labels do not enter candidate construction.

### Maximum-cardinality monotone matching

Among candidate edges, find a strictly monotone one-to-one matching with the
maximum number of matched V9/V10 rows.  There is no secondary score, margin,
distance preference, label preference, or record-specific penalty.

An edge is **certified** only when it appears in every maximum-cardinality
monotone matching.  An implementation may identify such forced edges with
prefix/suffix dynamic-programming counts; it must not select one arbitrary
optimal path.  Edges that change across equally optimal paths are `AMBIGUOUS`
and remain unmatched.

This two-leg chain is the complete primary rule.  Q5-B-0's aggregate drop map is
used to audit the resulting gaps and to construct synthetic fixtures, not to
choose among ambiguous pairings.  Leg 1 is fixed by provenance and Leg 2 has one
record-wise matcher; the equal/mismatched count strata are reporting strata, not
alternative rules.

# Synthetic fixtures

All fixtures are fixed before DS1 audit and have known true identities.  The
rule must recover 100% of identifiable true pairs, create zero false pairs, and
mark every deliberately non-identifiable repeated segment `AMBIGUOUS` in:

1. Leg 1 identity/no-drop replay, including duplicated endpoint RR and eligible
   first/last beats;
2. Leg 1 isolated and consecutive deterministic drops;
3. Leg 1 Q5-B-0-like F/Q deletion counts, including concentration in two
   records;
4. Leg 2 identity/no-drop sequence;
5. one isolated mamba-only or cache-only row and consecutive gaps on either
   side;
6. an equal-count drop-one/add-one cancellation, which must not be positionally
   zipped;
7. repeated coupling intervals with one unique flanking context;
8. a perfectly repeated segment with two equally optimal alignments;
9. +/-1-sample quantization on either RR component;
10. a declared seconds-to-samples conversion;
11. an intentionally wrong unit declaration, which must stop rather than fit a
    scale;
12. record-boundary corruption and within-record row-order corruption, each of
    which must fail without allowing a cross-record match.

Any synthetic false match terminates the rule as `JOIN_RULE_FALSIFIED` before
DS1 is inspected.

# Negative controls

Leg 1 remains fixed and must already have passed its exact replay gate.  Each
control then reruns the complete Leg 2 candidate construction, record-wise
maximum matching, certification, and all audit statistics.  Nothing except
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

On DS1, after matching, carry Leg 1 raw symbols through mamba identity to the
frozen parent AAMI classes.  In the definitions below, `processed` means the
V9/V10 positional row that would index a result NPZ; it never means a mamba row.
For each processed class `c in {N, S, V}` define:

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
2. the two provenance gates both pass: (a) Leg 1 exactly reproduces the frozen
   source/meta count, order, and RR ledger; and (b) Leg 2 verifies all 44 cache
   and result-position record boundaries, with every certified map record-local,
   monotone, and one-to-one;
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

Report all gates for the prespecified 36 equal-count and 8 mismatched-count
strata in addition to the pooled report.  These are diagnostic strata only:
neither stratum can be excluded, assigned a different matcher, or used to rescue
a failed primary gate.

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

1. **`JOIN_INPUT_ABSENT`**: an A-era material-input contract listed above fails
   before matching (canonical hash/source/meta, 44-record cache ledger,
   detection-order contract, or cache-to-result positional contract).  Stop:
   the registered inputs do not support the specified mapping.  Low coverage or
   a missing cross-lineage UID does not enter this branch.
2. **`JOIN_RULE_FALSIFIED`**: Leg 1 fails exact deterministic source replay, any
   synthetic false match occurs, TRUE fails to exceed the max-null, or the
   signal/null gates fail.  Stop; either the lineage contract is contradicted or
   ordinary RR repetition can explain the apparent Leg 2 mapping.
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
recovering this cross-lineage ledger from the original materialized V9/V10 cache
build is the only valid next route.  A fresh detector run or GPU training run is
not an identity-equivalent substitute, and A's deterministic mamba source replay
alone cannot reconstruct detector-dependent V9/V10 identities.  Guessing a UID
from `t`, RR rank, class, or model score is not.

# Parallel-work contract

| Track | Owner | May do now | Must not do |
|---|---|---|---|
| Q: measurement qualification | Claude | Complete: `MEASUREMENT_QUALIFIED`, run `20260810T005802` | Reinterpret qualification as join or association approval; change the frozen gates |
| J: beat-join design | Codex | Maintain this draft; specify rule, controls, null, and stops | Write/run join code; inspect DS2 labels/probabilities |
| J implementation | Claude, only after design approval | Implement exactly the approved join spec without executing it | Touch qualification files, run on registered data without the separate execution approval, or revise scientific rules silently |
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

## Record 232: known source concentration and parent-gate conflict

Before this join, record 232 already supplies 1,382 of 1,837 DS2 S beats
(75.2%).  This exceeds the parent spec's fixed rule that no single record may
contribute more than 50% of all eligible S beats.  The concentration is present
in the source cohort and therefore cannot be repaired by selecting a favorable
join subset.

Join gate 12 remains source-relative: it tests whether certification inflates a
record's existing S share by more than 1.25.  It does not replace, relax, or
reinterpret the parent's absolute 50% rule.  Thus a successful identity join may
still leave the parent association blocked by its own preregistered gate.  Any
resolution requires a separate parent-spec amendment, frozen without viewing
V10 probabilities or DS2 association outcomes; this join design makes no such
amendment.

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
- `research/HANDOFF_2026-08-10_Q5D_preflight_result_to_codex.md`
- `research/PREFLIGHT_2026-08-10_drive_asset_intake.md`
- `research/PROVENANCE_2026-08-10_mamba_data_lineage.md`
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
- [ ] Claude implements the approved spec without executing it
- [ ] User separately approves execution on the registered data
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
- 2026-08-10 — Registration note (Claude Code; process only, no scientific
  content changed).  This file was registered on `main` by Claude Code from a
  branch named `codex/q5d-beat-join-design` (PR #75).  Under `AGENTS.md` a
  Claude Code commit belongs on `claude/<task>`; the `codex/` namespace is
  reserved for Codex-authored branches, so the branch name was wrong.  The
  registered content was Codex's draft copied verbatim — the file as committed
  in `71e1991` hashes to SHA-256
  `5c938158b32dce2b86f39d05730012c6e11cf27e490977aa9d9a67db8778cc68`, identical
  to the source draft, with no rewriting or summarisation.  The merge landed
  before the branch name could be corrected, so the error is recorded here
  rather than by rewriting `main` history.  `design_owner` stays `codex`,
  `status` stays `draft`, and nothing in this spec has been implemented or
  executed.
- 2026-08-10 — Revised after the preflight reached
  `SOURCE_REPLAY_PROVEN` (A), contrary to the earlier B-conditional assumption.
  Redefined `JOIN_INPUT_ABSENT` as a material-contract failure under A and split
  the single join into deterministic Leg 1 (`.atr` to mamba) and
  detector-dependent, record-wise Leg 2 (mamba to V9/V10 positional rows).
  Registered the 44-record boundary ledger, the 36 equal-count and 8
  mismatched-count strata, and separate leg failures.  Rejected count equality
  and the plausible V9/V10-subset relation as identity axioms because the `pos`
  versus `p` boundary rules permit drop/add cancellation; all records therefore
  use the same forced-edge matcher.  Clarified that replay proves preprocessing
  lineage, not nondeterministic GPU probability regeneration; corrected endpoint
  RR to duplicated-and-eligible semantics; separated design approval from data
  execution approval; and documented the pre-existing record-232/parent-50%
  conflict without changing the parent gate.  Status remains `draft`; no join,
  label/probability inspection, training, download, or Drive mutation occurred.
