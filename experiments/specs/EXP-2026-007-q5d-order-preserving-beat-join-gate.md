---
experiment_id: EXP-2026-007
substage: Q5D_BEAT_JOIN_IDENTIFIABILITY_GATE
title: Q5-D deletion-aware order-preserving beat identity join gate
status: approved_for_implementation
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

> **2026-08-10 status note (process only; no scientific content changed).** The
> user has since taken step 2 below: the design is approved and `status` is now
> `approved_for_implementation`.  The paragraph above is Codex's draft-era text
> and is kept verbatim as the record of what was registered.  Read it with this
> correction: **implementation is now authorized; execution is not.**  Step 4 —
> a second, explicit user approval before the implemented join is run on the
> registered data — is still outstanding, and so is the further association
> approval.  EXP-2026-007 remains scientifically **NOT RUN**.

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

Two clarifications added 2026-08-10 after implementation review, neither of
which widens the branch:

- **Byte-identical duplicates are not an ambiguity.**  Several copies of
  `mamba_data.npz` may match the registered SHA-256; being byte-identical to
  the canonical asset is exactly what verification means.  The registered copy
  is preferred, the others are recorded as `byte_identical_duplicate`, and the
  manifest names the physical file used.  Only *zero* matches fire
  `JOIN_INPUT_ABSENT`; a same-size copy whose hash differs is excluded.
- **A missing Drive copy of `cache_v15b/mitdb/meta.json` does not, by itself,
  stop the run.**  When the canonical mamba hash verifies and the stored `pid`
  yields 44 contiguous blocks whose record counts match the committed lineage
  meta in the repository, the separate Drive copy is redundant corroboration,
  not an independent contract item.  Its absence is recorded, not escalated.

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
`203:2974`, `208:2579`, `223:2591`, `105:2567`, `111:2124`, and `222:2481`.
No observed alignment may alter either ledger.

**Two mamba coordinates, kept apart** (corrected 2026-08-10 after
implementation measured the artifact):

- `mamba_split_start` — the registered *logical* split-local coordinate,
  recomputed only by cumulative addition in the frozen split order.  It is an
  audit coordinate and stays exactly as registered.
- `mamba_file_start` — the *physical* global offset inside `mamba_data.npz`,
  measured from the stored `pid` array.  `build_penult.py` and
  `make_colab_data.py` both enumerate `sorted(glob(cache/*.npz))` over all 44
  records at once, so the physical order is `100, 101, 103, 105, …` with DS1
  and DS2 interleaved — it is *not* DS1-block-then-DS2-block.

These two coordinates are different enumerations of the same rows and must not
be conflated.  The V9/V10 cache and result starts are unaffected, because
`data.py::load_split` sorts within a split, which is the ledger's order.

**The matcher uses neither coordinate.**  It matches on record-local rows
only, inside a record slice, so this distinction changes no scientific rule.
Both coordinates are reported for audit; only the per-record mamba *counts*,
which this ledger does fix, act as a gate.

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

- [x] User approves this draft and status changes to `approved_for_implementation`
- [x] Claude implements the approved spec without executing it
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
- 2026-08-10 — **Implementation approval and implementation** (Claude Code).

  *What the user approved.* The user approved implementing this frozen design.
  **That approval is for writing code only.**  It is explicitly **not** approval
  to run the beat join on the registered data.  This PR therefore does not
  execute the join: no MIT-BIH `.atr`, `mamba_data.npz`, V9/V10 cache or result
  NPZ was opened, no DS1 or DS2 join performance was computed, no DS2 per-beat
  class label was read, no V10 probability was opened, no association was run,
  no model was trained, and no Drive file was created, moved or overwritten.
  **Executing on the registered data requires a second, explicit user
  approval** («Status boundary» step 4), which does not exist yet.

  *The barrier is code, not a promise.*  `MODES_NEEDING_EXECUTION_APPROVAL`
  (`LEG1_REPLAY_AUDIT`, `LEG2_RECORD_JOIN`, `DS1_GATE`, `DS2_GATE`) refuse to
  start without an explicit approval token; `open_registered_input()` checks the
  token *before* calling `open()`, so an unapproved run cannot even learn
  whether an artifact exists.  `read_result_npz()` refuses the `prob` key in
  every stage, with or without approval, and gates DS2 `y` behind a second
  post-freeze release token.  The token appears nowhere in this repository
  outside its own definition and the tests that prove the refusal.  Default CLI
  mode is `DESIGN`; the data modes exit 2 with `JOIN_RESULT_NOT_RUN`.

  *Implemented as specified.*  Leg 1 replays the three frozen mamba rules from
  raw `.atr` (registered N/S/V map, 150-sample boundary test on `pos`, the
  fewer-than-five-valid-beats record rule), preserves `.atr` sample order,
  recomputes post-filter RR with the first pre-RR and last post-RR duplicated so
  first and last beats are eligible, and audits count/order/RR against the
  committed ledger — failing as `JOIN_RULE_FALSIFIED` / `LEG1_SOURCE_REPLAY`,
  distinct from the material-contract `JOIN_INPUT_ABSENT`.  Leg 2 matches
  strictly inside each ledger-cut record slice on the single fixed candidate
  rule (`|Δpre| ≤ 1` and `|Δpost| ≤ 1` integer samples at 360 Hz,
  round-half-to-even), with no secondary score, distance/label preference or
  record-specific penalty.  The 44-record ledger, the 36/8 strata and the eight
  registered deltas (`108 −1`, `116 −14`, `203 −2`, `208 −7`, `223 −1`,
  `105 −1`, `111 −1`, `222 −4`) are constants verified against the registered
  starts and totals, never recomputed from join performance.  `t` is refused as
  a join key.  Equal count is a reporting stratum only, and `V9/V10 ⊆ mamba` is
  not used as an identity axiom.

  *Forced edges without enumeration.*  `CERTIFIED` means "in every
  maximum-cardinality monotone matching".  The implementation uses prefix/suffix
  chain-length DP: an edge lies in some maximum matching iff `L(e)+R(e)−1 = M`,
  its rank inside any such matching is forced to `L(e)`, so an edge is in
  *every* maximum matching iff no other usable edge shares its rank.  Singleton
  rank class → `CERTIFIED`; otherwise `AMBIGUOUS`, left unmatched.  Nothing is
  imputed and no arbitrary optimal path is promoted.  This equivalence is
  checked in `test_forced_edges_match_brute_force`, which enumerates *all*
  maximum matchings on 220 random small records (72 of them with multiple
  optima) and agrees with the fast path on every one.

  *Deviation worth recording.*  §«Negative controls» says the wrong-record
  control is skipped for a length bin with fewer than two records.  The first
  implementation mapped such a record to itself, which would have put a copy of
  TRUE into the null; a test caught it.  `derange_within_bins()` now omits those
  records, `wrong_record_skipped()` reports them, and building the control for a
  split where no derangement exists raises rather than degrading to identity.
  No threshold, tolerance, gate, statistic or stopping rule was changed.

  *Null reuse.*  `rule_fingerprint()` hashes the tolerance, symbol map, ledger,
  matcher description, seeds and all gate constants.  `null_summary()` stores
  it and `assert_null_matches_rule()` refuses a null generated under a different
  rule, so a relaxed rule structurally cannot inherit the primary rule's cutoff.

  *Verification.*  357 assertions pass with no registered artifact opened; the
  21 synthetic fixtures produce **zero false certified pairs**.  The 10,000-
  replicate null and 2,000-replicate bootstrap were **not** run — only small
  synthetic replicates, to test reproducibility and format.

  *Record 232, unchanged.*  Record 232's 1,382/1,837 (75.2%) DS2 S share is
  carried as a source-cohort constant.  Gate 12 remains source-relative
  (inflation ≤ 1.25) and does not relax or replace the parent spec's absolute
  50% ceiling, so a successful identity join may still leave the parent
  association blocked by the parent's own preregistered gate.  This spec makes
  no parent amendment.

  *Files changed.*  Only the four this spec allows: this file's `status`,
  checklist and Decision log; `mit-bih/q5d_order_preserving_beat_join.py`;
  `mit-bih/test_q5d_order_preserving_beat_join.py`; and
  `notebooks/quest54_q5d_order_preserving_beat_join.ipynb` (committed
  unexecuted, every output cell empty, no fabricated result).  Claude's
  qualification files (`mit-bih/q5d_qualify_*`, `notebooks/quest53_*`,
  `research/PLAN_2026-08-10_*`) were not touched.
- 2026-08-10 — **Execution approval, artifact loaders and hash preflight**
  (Claude Code).

  *Approval.* The user gave «Status boundary» step 4: executing the join on
  the registered data is approved, and asked that the Colab notebook run
  **hash preflight → STOP/PASS → join** in that order.  Still **not** approved
  and still sealed: V10 probability values, the association analysis, S PR-AUC
  and any model training.  DS2 per-beat class labels remain behind the
  separate post-freeze support-gate release.  Opening a registered artifact
  stays an explicit opt-in in code (`OPEN_REGISTERED_DATA`, default `False`)
  so no stray run touches the data, and `assert_preflight_passed()` blocks
  matching until the material contract closes.

  *Two RR semantics, frozen from source rather than assumed.*  The spec
  requires both sides' units and semantics to be frozen from source before any
  match.  `mit-bih/lineage/build_penult.py` fixes the mamba side:
  `Z(26D) = psa_rel(4) + rr(7) + pw(3) + rhy(5) + ptf2_rel(7)` with
  `RR_PRE_COL = 0`, so pre/post RR are Z columns **4 and 5**, in seconds.  The
  V9/V10 side was **not** in this repository, so `kinkmap/data.py` and
  `kinkmap/frontend.py` were read from the registered source package: the
  cache stores `rr` as `rr_features(peaks)[idx]`, 7 columns,
  `[pre, post, pre/local, post/local, pre/avg, post-pre, lvar]`, in seconds,
  so pre/post are columns **0 and 1**.

  Two differences between the lineages are now recorded as constants rather
  than discovered later:

  1. **Endpoint semantics differ.**  mamba *duplicates* the first pre-RR and
     last post-RR (so first/last beats are eligible).  `rr_features` sets them
     to `np.nan` and then `nan_to_num`s them to **`0.0`** — not duplicated.  A
     stored `0.0` is therefore real data meaning "no neighbour", and such a
     row simply forms no candidate edge and stays `UNMATCHED`.  That is the
     honest outcome; nothing is imputed to close the gap.
  2. **RR is computed at different stages.**  mamba computes RR *after* the
     symbol and boundary filters, on annotation positions.  V9/V10 computes
     `Fr = rr_features(peaks)` on the **full** matched-peak array and only
     then selects `Fr[idx]` with the boundary-valid rows, so a cache row can
     carry an RR whose neighbour was boundary-cut.  The record rules also
     differ (`len(peaks) < 2` for the cache versus mamba's five valid beats).

  This also makes explicit what the frozen one-sample tolerance absorbs: a
  cache RR differs from a mamba RR by `e_j - e_{j-1}`, the *change* in
  detector offset between neighbouring beats, not the offset itself.  The
  tolerance is not widened on this basis; if the offsets move faster than one
  sample, coverage falls and the registered answer is `JOIN_UNRESOLVED`.

  *Deviation recorded — the ledger's `mamba_start` is a different enumeration.*
  The spec builds `mamba_start` "by cumulative addition in the same frozen
  split order".  `build_penult.py` and `make_colab_data.py` both enumerate
  `sorted(glob(cache/*.npz))` over **all 44 records at once**, so the actual
  global row order inside `mamba_data.npz` is `100, 101, 103, 105, …` with DS1
  and DS2 **interleaved**, not DS1-block-then-DS2-block.  The cache and result
  starts are unaffected — `data.py::load_split` sorts *within* a split, which
  is exactly the registered ledger order.  So only the mamba audit offset is
  involved.  The implementation therefore measures mamba record slices from
  the stored `pid` array (contiguity is checked, non-contiguity is an error),
  gates on the ledger's per-record **counts**, which the ledger does fix, and
  reports both the observed file offset and the ledger's split-order start.
  No scientific rule, tolerance, gate, statistic or stopping rule changed;
  this is an audit-field discrepancy in the spec's ledger construction and is
  flagged here for Codex.

  *Three material-contract gaps the preflight now decides.*  `mamba_data.npz`
  had never been compared against its registered SHA-256 `b1c16106…`, and
  Drive holds **three same-size copies** (two created 2026-08-10), so size
  proves nothing; `resolve_canonical_mamba()` accepts exactly one byte-match
  and stops on zero or on ambiguity.  The V9/V10 cache hashes were never
  computed, and the Drive copy of `cache_v15b/mitdb/meta.json` was never
  confirmed.  All of this is `JOIN_INPUT_ABSENT` territory — a failed input
  contract, never a disappointing join — and it is decided *before* matching.

  *Verification.*  446 assertions pass with no registered artifact opened.
  The 21 synthetic fixtures still produce zero false certified pairs, and the
  brute-force forced-edge oracle still agrees on every random record.
- 2026-08-10 — **Codex review of the preflight; five corrections before any
  Colab run** (Codex review, implemented by Claude Code).

  Codex accepted the three artifact findings (cache `0.0` endpoints left
  `UNMATCHED`, the two RR computation stages preserved, mamba's physical order
  measured from `pid`) and confirmed they change no scientific rule, because
  the matcher is record-local.  It then found that **the preflight was weaker
  than it was described as being**, and blocked execution until five things
  were fixed.  All five are now implemented; the review was right on each.

  1. **The directory hash did not hash content.**  `hash_file_set()` replaces
     it: every expected file's bytes are SHA-256'd and folded, with size, into
     one aggregate digest, and extra/missing entries fail the set.  The cache
     set is `meta.json` + 44 record npz; the MIT-BIH set is `.dat/.hea/.atr`
     for all 44 records.  A tampered file with an unchanged name now moves the
     aggregate — the exact case a listing hash misses, and now a test.
  2. **"Two matches -> STOP" was a logic error.**  Two files that both match
     the registered SHA-256 are byte-identical verified copies, not an
     identity ambiguity.  Corrected: zero matches -> `JOIN_INPUT_ABSENT`; one
     or more -> prefer the registered copy, record the rest as
     `byte_identical_duplicate`, and name the physical file used in the
     manifest; a same-size copy whose hash differs is excluded.  The notebook
     now compares all three Drive copies rather than only the registered path.
  3. **The preflight was bypassable.**  `run_join()` took no freeze, so the
     approval token alone could reach matching.  A PASSing freeze from
     `build_preflight()` is now a **required** argument, and
     `verify_preflight_freeze()` re-hashes the canonical mamba asset and both
     aggregates against the files on disk, refuses a freeze made under a
     different rule fingerprint, and refuses one whose result positional
     contract is unproven.
  4. **The result `pid` contract was never called.**
     `verify_result_positional_contract()` is now part of `build_preflight()`
     for both splits, so cache-row -> result-row is proven before Leg 1.
  5. **DS2 could run standalone.**  The notebook minted the release from
     `MODE`.  `release_ds2_support_gate()` now reads the frozen DS1 bundle and
     mints the token only when the DS1 decision, manifest and null agree with
     this run on rule fingerprint, input hashes, code hash and the registered
     null seed, and only when DS1 actually qualified; `run_join()` refuses a
     DS2 split without that token.

  Also on Codex's reading: the absent Drive copy of `cache_v15b/mitdb/meta.json`
  is redundant corroboration once the mamba hash verifies and `pid` yields 44
  contiguous blocks matching the committed lineage meta, so it is recorded
  rather than escalated.  The `JOIN_INPUT_ABSENT` section and the mamba
  coordinate contract in the body were corrected accordingly —
  `mamba_split_start` (registered, logical, split-local) and `mamba_file_start`
  (measured, physical, global) are now named separately, with the matcher
  explicitly using neither.  Both appear in the join map as
  `mamba_global_row` and `mamba_file_row`.

  No threshold, tolerance, gate, statistic, seed or stopping rule changed.
  494 assertions pass, still with no registered artifact opened; the preflight
  bundle is now preserved for a STOP as well as a PASS.
- 2026-08-10 — **Result-NPZ contract corrected: DS1/DS2 separated, V10 grid
  checked exhaustively** (Codex review, implemented by Claude Code).

  *The bug.*  The previous preflight demanded a result-NPZ row contract for
  **both** splits and the notebook pointed both at the same file.  One `pid`
  array cannot satisfy the DS1 50,551-row ledger and the DS2 49,289-row ledger
  at once, and V9/V10 result packages are DS2 prediction outputs, so a correct
  asset would have been STOPped on the DS1 check.  Running the preflight in
  that state would have produced a `JOIN_INPUT_ABSENT` that said nothing about
  the data.  Corrected before any Colab run.

  *The corrected contract.*

  - **DS1** does not require a result NPZ at all.  Its record boundaries are
    proven from the cache `meta.json` against the frozen ledger
    (`verify_cache_ledger_contract`), which is where DS1's row order actually
    lives.
  - **DS2** requires the `pid` contract of **every** file in the registered
    grid — `{arm}_s{seed}.npz` over the five V10 arms (`base`, `full`,
    `pwave`, `pwave_noc`, `v8base`) and seeds 1000-1004, 25 files.  Each must
    independently satisfy the registered ledger: 49,289 rows, the 22 records
    in registered order, contiguous per-record blocks, and each record's
    registered `n` and start.
  - Only `pid` is read.  `prob` stays sealed and `y` is untouched here, so
    this is a cheap material check that opens no outcome.
  - Each file's `pid` digest is recorded, and **all 25 must be identical**.
  - A missing file, a contract failure, or any disagreeing `pid` is
    `JOIN_INPUT_ABSENT` for the **whole set**.  Proceeding with the files that
    happened to pass is explicitly refused, in `verify_preflight_freeze` as
    well as in the report — that would be selecting inputs on the basis of
    which ones passed.
  - The file set is **preregistered by name**, not discovered with a glob: a
    glob cannot notice a file that is absent.

  *Scope.*  V9 arms (`kink`, `kink_noctx`, `kink_noproto`, `v8_noc`,
  `v8base`) are registered in the module so the same check is available, but
  the join consumes V10 positional rows only, so the V10 grid is what the
  preflight checks.  If a later stage consumes V9 results, that stage must run
  the same 25-file check and additionally require the V9 and V10 `pid` digests
  to agree; the scope is not widened pre-emptively here.

  *Why exhaustive rather than representative.*  One representative file only
  shows that the producer was *written* to store the same `pid`.  It cannot
  detect a file mis-copied, mixed in from another run, or truncated — all
  file-level accidents, not source-level ones.  A test now reproduces exactly
  that case: 25 files where one carries a different `pid`, which a
  representative check passes and the exhaustive check fails.

  No threshold, tolerance, gate, statistic, seed or stopping rule changed.
  531 assertions pass with no registered artifact opened.
- 2026-08-10 — **First preflight executed on the registered data.  Three
  contract gaps closed; one false STOP found and fixed.**

  Run `20260810T114347_EXP-2026-007_q5d_beat_join_preflight`.  This is the
  first stage of Q5-D that opened registered artifacts, under the user's
  execution approval.  It hashed only; no join ran, no probability was opened,
  no DS2 label was read, nothing was trained, and no existing Drive asset was
  modified (the run wrote one new timestamped preflight folder).

  **Closed — the three gaps recorded above are now settled by measurement:**

  1. `mamba_data.npz` verifies against the registered SHA-256
     `b1c16106…`, and the **registered copy** is the one present.  One
     byte-identical duplicate was found at
     `mitbih/v9pkg/kinkmap/v13pkg/mamba_data.npz` and recorded as such; a
     third candidate path did not exist, which is not a failure under the
     corrected rule (only *zero* matches are).  The long-standing
     "hash never compared" gap is closed.
  2. The V9/V10 cache aggregate is `82b9a593…` over 45 files with no missing
     and no unexpected entries.  Its hash had never been computed before.
  3. The DS1/DS2 cache-ledger contract passes 22/22, and the DS2 result
     contract passes **25/25 files sharing one `pid` digest** `b8e45b6e…` —
     the exhaustive check Codex required, on its first real run.

  **The single STOP was an error in this spec's implementation, not in the
  data.**  `mitdb-1.0.0` is the publisher's complete MIT-BIH tree — **48**
  records — while the expected set had been built from the **44** the join
  reads.  Records `102`, `104`, `107`, `217` (the paced records the de Chazal
  split excludes) and the publisher metadata `ANNOTATORS`, `RECORDS`,
  `SHA256SUMS.txt` were therefore reported as "unexpected", and a correct,
  immutable, publisher-checksum-verified directory failed.  `ASSETS.md`
  (`data-mitdb-raw-100`) had it right all along: 48 x 3 + 3 = **147** files.

  Corrected: `mitdb_expected_files()` now expects the published tree.  This
  changes the *integrity contract over the directory*; it does not change
  which records the join reads, which is decided by the 44-record ledger and
  by nothing else.  The paced records are expected to **exist** and are never
  opened.

  The correction was also used to strengthen the contract rather than merely
  loosen it: because `SHA256SUMS.txt` ships inside the tree, the preflight now
  cross-checks every hashed file against the **publisher's own digests**
  (`verify_against_publisher_checksums`), reusing the digests already computed
  so it costs no extra I/O.  "These are the bytes that were there" became
  "these are the published bytes".

  No threshold, tolerance, gate, statistic, seed or stopping rule changed.
  564 assertions pass.  Both failure directions stay covered: a genuinely
  missing published file and a tampered byte are still caught, and the STOP
  that occurred is now a regression test.
- 2026-08-10 — **`RECORDS` checksum STOP resolved: the data was pristine, the
  parser was wrong.**

  The third preflight reached the publisher-checksum stage with everything
  else green — mamba verified, cache aggregate clean, DS1/DS2 ledger 22/22,
  DS2 result 25/25 sharing one `pid` digest, MIT-BIH 147 files with no
  missing and no extra — and STOPped on a single line: `RECORDS: sha256
  differs from the publisher list`.

  Diagnosed by reading both artifacts directly.  The registered `RECORDS` is
  192 bytes, 48 lines, LF, terminated with a newline, containing all 48
  published records including the four paced ones, and hashing to
  `fcdca7ea…`.  It is intact.

  The MIT-BIH `SHA256SUMS.txt` (704 entries, itself hashing to the registered
  `b61158a9…`) covers a **wider tree** than the directory being verified, and
  lists two different files whose names collide once paths are stripped:

  ```text
  fcdca7ead9fc93f6…  RECORDS
  215c6f7042da70f9…  x_mitdb/RECORDS
  ```

  `parse_sha256sums` keyed the map on `os.path.basename(name)`, so the nested
  entry overwrote the top-level one and the pristine `RECORDS` was compared
  against a different file's digest.  `ANNOTATORS` has the same collision but
  identical digests on both sides, which is why exactly one file failed and
  the bug looked like a data problem.

  Fixed: the checksum map is keyed on the path **as listed**, and lookup uses
  the exact top-level name, so a nested entry can never answer for a
  top-level file.  A regression test reproduces the precise shape — top-level
  and nested `RECORDS` with different digests, plus the identical-digest
  `ANNOTATORS` case that hid it.

  Two related weaknesses fixed at the same time, both found by looking rather
  than by failing:

  - "nothing matched" could read as "everything passed".  If the publisher
    listed every file under a prefix this directory does not use, `checked`
    would be zero and the stage would report `ok`.  Zero matches against a
    non-empty file set is now a failure that says nothing was verified.
  - the counter reported as `verified` actually counted *files with a
    published entry*, not files that agreed — the run that printed
    `verified=146` was really 145 matched and 1 mismatched.  `checked`,
    `matched`, `mismatched`, `considered` are now separate.

  Nothing about the gate was relaxed to make this pass.  The publisher
  cross-check still fails on a changed byte, a missing published file, and an
  unverifiable list.  No threshold, tolerance, gate, statistic, seed or
  stopping rule changed.  602 assertions pass.

  *Process note.*  Three Colab runs were consumed by stale modules: the
  notebook was newer than the clone twice (fixes pushed after a merge, and
  `import` returning the `sys.modules` cache).  A version assertion was added
  and then defeated by the author forgetting to bump it.  The notebook now
  additionally asserts the **names it actually uses** (`NEED_ATTRS`), which
  cannot be defeated by forgetting a version number, and prints
  `BJ.__file__`.  `MODULE_VERSION` is 3.
- 2026-08-10 — **`PREFLIGHT PASS`.  The material-input contract is closed.**

  Run `20260810T122603_EXP-2026-007_q5d_beat_join_preflight`.  All five
  contracts verified against the registered data, with nothing relaxed:

  | contract | frozen identity |
  |---|---|
  | canonical mamba | `b1c16106…` (registered copy present; one byte-identical duplicate recorded) |
  | V9/V10 cache aggregate | `82b9a593…` — 45 files, 0 missing, 0 extra |
  | MIT-BIH tree aggregate | `0b46a411…` — 147 files, 0 missing, 0 extra, publisher checksums 146/146 |
  | DS1/DS2 cache ledger | 22 / 22 records |
  | DS2 result `pid` | `b8e45b6e…`, shared by all 25 registered files |

  These four digests are the run's **input identity**.  `run_join()` re-checks
  them against the files on disk before Leg 1, and a null or a DS2 release
  generated under a different rule fingerprint cannot be inherited.

  What this does and does not establish: the registered artifacts are the
  ones the lineage says they are, and their row boundaries are internally
  consistent.  It establishes **nothing** about whether the beat identity map
  exists — that is Leg 1 and Leg 2, and `JOIN_UNRESOLVED` remains an entirely
  possible and valid outcome.  No probability was opened, no DS2 label was
  read, nothing was trained, and no registered asset was modified.

  Leg 1 was additionally gated: the audit cell now asserts the preflight
  passed under the current rule fingerprint before replaying any `.atr`, and
  writes its own bundle whether it passes or emits `JOIN_RULE_FALSIFIED`.  607
  assertions pass.
- 2026-08-10 — **Runtime dependencies declared per stage and checked before
  the work.**

  The first Leg 1 attempt died on `ModuleNotFoundError: wfdb` — the run
  environment never installed it — and it surfaced only once the replay
  reached its first `.atr`.  The same class of failure was waiting in a worse
  place: `pyarrow` is imported only when `join_map.parquet` is written, at the
  *end* of a completed join, so a missing `pyarrow` would have discarded a
  full DS1 run including its 10,000-replicate null.

  Fixed structurally rather than by adding one import:

  - `RUNTIME_DEPENDENCIES` records each third-party module, what it is for,
    and its version in the registered runtime (`numpy` 2.5.1, `wfdb` 4.3.1).
  - `STAGE_REQUIREMENTS` maps every mode to what it actually needs.  The
    offline stages need nothing; the preflight needs `numpy`; Leg 1 adds
    `wfdb`; the join stages add `pyarrow` **up front**, not at bundle-writing
    time.
  - `assert_runtime_ready()` refuses to start a stage whose imports are
    absent, naming the exact `pip install` line, before anything is read.
    Each entry point calls it.
  - `build_env_pin()` records the versions actually loaded alongside the
    registered ones, and `build_manifest()` embeds it, so a run says which
    environment produced it.  A version difference is a recorded fact, not a
    new stopping rule — this stage does not invent stops the spec did not
    register.
  - The notebook installs `wfdb==4.3.1` and `pyarrow` in its setup cell and
    prints the per-stage dependency table there.

  One ordering rule was made explicit while doing this: **permission before
  capability**.  A call that was never authorised is refused as unauthorised
  whatever the environment happens to have installed, so
  `require_execution_approval` and the DS2 release check precede the runtime
  check in all three entry points; the expensive freeze re-hashing comes last.
  A test pins that order.

  No threshold, tolerance, gate, statistic, seed or stopping rule changed.
  639 assertions pass.
- 2026-08-10 — **A skipped stage may no longer look like a passed stage.**

  The first Leg 1 attempt after the dependency fix printed the Leg 1 rule
  table and then produced nothing further: `MODE` was still `HASH_PREFLIGHT`,
  so `if MODE in ("LEG1_REPLAY_AUDIT",) and APPROVAL:` was false and the whole
  block was skipped in silence.  The cell's output was **indistinguishable
  from a clean run** — the constants printed, no error appeared.

  That is the most dangerous failure mode this pipeline can have.  Every other
  guard here is designed so a problem stops the run loudly; a stage that
  quietly does nothing inverts that, and could be read as "Leg 1 ran and was
  fine".  Nothing was executed and no wrong result was produced, but the
  output invited a wrong conclusion.

  Fixed: one `stage_should_run()` helper decides whether a stage runs and
  **always announces the outcome** — `RUN` with the mode, or `SKIP` with the
  reason, the exact setting to change, and an explicit warning that the
  constants printed above it are not results.  Both data stages and the
  preflight go through it; no cell uses a bare
  `MODE in (...) and APPROVAL` guard any more.  A test asserts that every cell
  which opens registered data is behind the announcing helper.

  No threshold, tolerance, gate, statistic, seed or stopping rule changed.
  650 assertions pass.
- 2026-08-10 — **Leg 1 passes on DS1.  Null runtime measured and flagged.**

  `LEG1_REPLAY_AUDIT` on DS1: **`ok=True`, replayed 50,576 / 50,576**, and the
  mamba `pid` blocks match the ledger for every record.  Because
  `audit_leg1_against_ledger` reported no problems, all four of its checks
  held: per-record counts, `.atr` ordinal order, strictly increasing R samples
  after filtering, and — with the stored mamba RR supplied at
  `rr_atol_samples = 0` — **every pre- and post-RR value matching exactly** in
  integer samples across all 50,576 rows.

  This is the deterministic leg holding.  The three frozen rules and the RR
  semantic read out of `v15b_local.py` (post-filter, seconds, duplicated
  endpoints) are confirmed against the registered artifact rather than
  assumed, and `JOIN_RULE_FALSIFIED` / `LEG1_SOURCE_REPLAY` did not fire.  It
  says nothing yet about Leg 2 identifiability.

  DS2 Leg 1 is deliberately not run yet: DS2 raw `.atr` symbols are available
  "only after the join rule and code are frozen", which is after the DS1 gate.

  **Feasibility finding, raised before it costs a run.**  A single complete
  DS1 Leg 2 join over the 22 records measures at ~1.7 s (22 records, ~2,300
  rows each, realistic RR density; ~317k candidate edges).  The registered
  null is 3 families x 10,000 replicates, each rerunning the *complete* Leg 2
  — 30,000 joins, about **14 hours**.  A profile puts 85% of that in
  `match_record` (the prefix/suffix Fenwick DP, ~635k tree operations per
  join); row construction and schema validation are only ~15%, so trimming
  those does not change the picture.

  `N_NULL_REPLICATES` is registered and enters the rule fingerprint, so a
  shorter null is **a different rule, not a faster run**.  It has not been
  touched.  The legitimate options are execution strategy — optimise the
  matcher without changing what it computes, or checkpoint the null across
  sessions — and the choice belongs to Codex, not to whoever is impatient at
  the console.  `estimate_null_runtime()` reports the cost, and says so.

  One defect fixed on the way: `run_join` runs the null whenever the split is
  DS1, and the notebook selected DS1 for `LEG2_RECORD_JOIN` — so choosing
  "look at the join" would have silently started the 14-hour null.  The stages
  now mean what their names say: `LEG2_RECORD_JOIN` does the record-wise join
  and coverage with no null (seconds); `DS1_GATE` runs the registered null and
  prints its expected cost first.

  No threshold, tolerance, gate, statistic, seed or stopping rule changed.
  663 assertions pass.
- 2026-08-10 — **Null shard runner.  Science unchanged; execution scheduling
  only.**

  The registered null is 3 families x 10,000 replicates, each rerunning the
  complete Leg 2 — measured at ~14 hours, longer than a Colab session.  Codex
  directed that it be scheduled, not shortened: no reduction, no early stop,
  no approximation, no omitted family.  This entry records that nothing
  scientific moved.

  **Unchanged and asserted by test**: `N_NULL_REPLICATES = 10000`, the three
  `CONTROL_FAMILIES` in order, `MASTER_SEED = 2026017`,
  `BOOTSTRAP_SEED = 2026018`, 2,000 bootstrap replicates, the matcher, the
  candidate rule, the one-sample tolerance, the certification definition,
  `J_null_max[b]` as the per-replicate maximum over the three families, every
  gate and stopping rule, `rule_fingerprint`, `MODULE_VERSION = 3`, and the
  preflight and Leg 1 contracts.  A test also asserts that changing the shard
  size does **not** move `rule_fingerprint`: scheduling is not part of the
  rule.

  **What was added.**  Replicates are cut into *null shards* of 100, each
  holding the same replicate range for **all three families**, so
  `J_null_max` never straddles a boundary.  `apply_control` is already seeded
  per `(family, replicate)`, so replicate `b` is the same value whoever
  computes it and whenever — sharding decides only who computes it.  Shards
  are immutable resume artifacts (never model checkpoints; no trained state
  exists here) and an existing file is never overwritten.  A shard is reused
  only after its own digest verifies *and* its identity matches: runner
  version, split, families, master seed, rule fingerprint, code SHA-256 and a
  preflight-derived input digest.  Each shard also records replicate range,
  worker count and git commit; `worker_count` is deliberately outside the
  digest so one worker and two produce byte-identical shards.  Execution uses
  `ProcessPoolExecutor` with a default of two workers, and the final arrays
  are assembled sorted by `(family, replicate)`, so neither completion order
  nor worker count can reach the numbers.

  `finalize_null_shards()` is the only route to the arrays and STOPs on a
  missing, duplicated or overlapping replicate, a failed digest, a wrong
  `j_null_max`, or any mixture of fingerprint, code hash or input digest.
  **Nothing downstream — `null_summary`, the gate decision, the DS2 release —
  can be built from an incomplete null.**

  **Equivalence, all tested**: sharded equals serial bitwise on a fixed
  replicate count; one worker equals two, with identical shard digests; shard
  sizes 1/4/5/12/100 give the same arrays; shards completed in reverse order
  give the same arrays; an interrupted run resumed gives exactly the
  uninterrupted arrays; and corrupt, missing, duplicate, overlapping and
  mixed-identity shards are all refused.  The existing fixtures and the
  brute-force forced-edge oracle continue to pass.

  Matcher optimisation was explicitly excluded from this work and none was
  done.  763 assertions pass.  No registered data was executed.
- 2026-08-10 — **DS1_GATE production integration.  Science unchanged;
  execution scheduling only.**

  Codex directed that the three stages be separated and that production have
  exactly one route to a DS1 decision.  Nothing scientific moved:
  `rule_fingerprint` is byte-identical to the previous `main`, and so are
  `MODULE_VERSION` (3), `N_NULL_REPLICATES` (10,000), the three families and
  their order, both seeds, the tolerance, the matcher and every gate.

  **The defect this closes.**  `evaluate_gates` skips gates 9-11 when the null
  is absent, so the previous `LEG2_RECORD_JOIN` path evaluated **10 of 12**
  gates and, with the coverage gates passing, returned `JOIN_IDENTIFIABLE` —
  the terminal "the join qualifies" verdict — and wrote it into a Drive run
  bundle as `decision.json` and `summary.md`.  A verdict reached without the
  null, preserved in an immutable-by-convention artifact that could later be
  cited.  Measured and confirmed before the stage was ever run on the
  registered data.

  **Three stages now.**
  `run_true_join()` computes Leg 1, Leg 2, coverage, inflation and `J_min`
  only.  It does not call `evaluate_gates`, does not touch `apply_control`,
  has no `null_replicates` parameter, and reports `TRUE_JOIN_MEASURED` /
  `DS1_GATE_NOT_RUN` instead of a decision.  `run_null_shards()` is unchanged
  from the previous entry.  `finalize_ds1_gate()` verifies the three families
  are complete at the registered size and then runs the registered order —
  `null_summary` -> 2,000 record-cluster bootstrap -> `evaluate_gates` — and
  is the only route to a DS1 decision.  `run_ds1_gate_sharded()` orchestrates
  the three.

  The in-line null loop is gone from the public path.  `run_join()` survives
  only as a shim that **refuses** a non-zero `null_replicates` and names the
  production route; the straight-line computation is kept privately as
  `_serial_null_reference()` and is used solely as the test oracle the sharded
  runner must reproduce.

  **Artifacts.**  `LEG2_RECORD_JOIN` writes a diagnostic `true_join.json` and
  the join map, explicitly *not* a canonical bundle and with no
  `decision.json`.  Only `DS1_GATE`, after combining the TRUE result with a
  complete null, creates the canonical timestamped run directory carrying
  `decision.json`, `null_summary.json` and `bootstrap.json` together.  Shards
  live in a stable, un-timestamped directory so resuming does not litter
  provisional bundles.  `release_ds2_support_gate()` now additionally requires
  exactly 10,000 null replicates and exactly 2,000 bootstrap replicates, so
  only that canonical bundle can release DS2.

  **Tested**: the serial oracle and the sharded production path agree on the
  family arrays, the null summary and its quantiles, the bootstrap, and every
  gate value of the final decision — not merely the verdict; an incomplete,
  short or family-missing null cannot produce a decision or a DS2 release;
  `LEG2_RECORD_JOIN` starts no null and claims no verdict; `run_join` cannot
  start an in-line null; and the fixtures and brute-force oracle still pass.
  823 assertions.  No registered data was executed.

  One incidental robustness fix: `fixture_record_boundary_corruption` named
  record `108` literally, so it depended on that record existing in whatever
  ledger was registered.  It now corrupts the ledger's first record.  The
  fixture's meaning — a corrupted boundary must fail — is unchanged.

  *Short-null bypass closed (Codex review, before merge).*  `finalize_ds1_gate`
  and `run_ds1_gate_sharded` no longer take a `total` argument: a public
  production function that can be asked for a shorter null **is** a short-null
  bypass, whatever its default.  Both now accept exactly
  `N_NULL_REPLICATES = 10000` in each of the three families and refuse 9,999
  and 10,001 alike.  The size-parameterised computation survives only as the
  private `_finalize_ds1_gate_reference()`, used by the equivalence tests so
  they can compare the serial oracle against the sharded runner at an
  affordable size; production cannot reach it.  Tests assert that neither
  public signature carries `total` or any other replicate-count knob.

  Codex also confirmed the two design judgments raised at the previous FROZEN
  point: `TRUE_JOIN_MEASURED` / `DS1_GATE_NOT_RUN` stay in `STAGE_STATUSES`
  and out of the registered `DECISIONS`, and `run_join` stays as an explicit
  refusing shim rather than being deleted.

  *No-early-stop, restated.*  The implementer suggested deciding whether to
  run the null after seeing the TRUE join's coverage.  That is a
  result-dependent execution choice and is not permitted: the null runs to 3
  families x 10,000 replicates regardless of what the TRUE join shows.  A weak
  TRUE result is a reason to expect `JOIN_UNRESOLVED`, never a reason to skip
  the control that would establish it.

  834 assertions pass.  `rule_fingerprint` remains byte-identical to `main`.
- 2026-08-10 — **TRUE join measured on DS1; two control defects found and
  fixed before the null.**

  *Measured TRUE join* (`20260810T142308_…_true_join_DS1`, stage
  `TRUE_JOIN_MEASURED` / `DS1_GATE_NOT_RUN`, no verdict written):

  | quantity | value | registered gate |
  |---|---|---|
  | overall coverage | 0.7595 | ≥ 0.95 — fails |
  | N / S / V coverage | 0.8097 / 0.7341 / **0.1578** | each ≥ 0.90 — fails |
  | `class_coverage_balance` | 0.2077 | ≥ 0.80 — fails |
  | `record_coverage_balance` | 0.4238 | ≥ 0.80 — fails |
  | class agreement | 0.99990 | ≥ 0.995 — passes |
  | `J_min` TRUE | 0.1575 | — |
  | ambiguous fraction | 0.0118 | — |

  First failure is gate 3, whose registered decision is `JOIN_UNRESOLVED`.
  The null enters only gates 9-11, so the decision does not depend on it.
  This is recorded, and it does **not** license skipping the null: the run
  goes to 3 x 10,000 regardless, because choosing on the strength of the TRUE
  result is the result-dependent choice the design forbids.

  The shape repeats Q5-B-0 exactly — high precision, insufficient and
  class-selective recall.  Agreement of 0.99990 says what *is* certified is
  almost certainly right; `class_coverage_balance` of 0.2077 says the
  missingness is concentrated, which is what the Q5-B-0-derived gates exist to
  catch.  V coverage of 0.1578 against N 0.8097 is structured, not noise.  A
  mechanism consistent with it — not measured, and not acted on: the frozen
  tolerance absorbs `e_j - e_{j-1}`, the change in detector offset between
  neighbours, and a PVC's wide abnormal QRS shifts `detect_r()`'s position
  relative to the annotation, moving both its pre- and post-RR and also
  perturbing its neighbours' RR.  The tolerance is not widened; that would be
  relaxation after seeing results.

  *Two defects in the controls, found when DS1_GATE was started.*

  1. **The wrong-record control could not execute at all.**  It deliberately
     pairs one record's raw sequence with another record's processed rows, so
     its mamba slice is a different record's length — but `join_split`
     enforced the registered mamba count unconditionally and raised
     `DS1 101: mamba slice 1613 != registered 1862`.  A registered control was
     impossible to run.  Fixed by registering, per family, whether it
     preserves record length (`CONTROL_PRESERVES_RECORD_LENGTH`) and relaxing
     the **mamba-side** ledger check for the wrong-record family alone.  The
     TRUE join still enforces both sides, and the **cache side is enforced
     always**, including in controls.
  2. **The Leg 1 class did not travel with the beat.**  `j_min` and
     `coverage_report` resolved the carried class as
     `mamba_classes[(record, position)]` — the class of whatever beat
     *originally* occupied that position.  Under order-shuffle,
     circular-shift and wrong-record the beat at a position is a different
     beat, so agreement was scored against the wrong class.  The spec requires
     the audit symbols to travel with the permuted RR pairs.  The error made
     the null **lower than it should be** — anti-conservative, the direction
     that makes TRUE easier to beat.  Fixed by carrying `mamba_aami` on each
     join-map row (added to the minimum audit fields, so the run bundle now
     records it) and scoring on the carried class, with the positional lookup
     kept only as a fallback for callers that supply none.

  Both were invisible to the existing tests because every synthetic record had
  the same length and the same class profile.  Regression tests now use
  records of differing length and a permutation whose carried classes all
  disagree with the positional ones — the second test would score 1.0 under
  the old code and 0.0 under the corrected one.

  No threshold, tolerance, gate, statistic, seed or stopping rule changed;
  `rule_fingerprint` remains byte-identical to `main`.  849 assertions pass.
  **The registered null has not been run**: the first DS1_GATE attempt aborted
  on defect 1 before completing any shard.

  *Worker count follows the machine (scheduling only).*

  The second DS1_GATE attempt ran healthily but slowly.  Measured on the
  runtime, not estimated: `nproc` 2, both worker processes in state `R` at
  87.5% and 75% CPU, `%Cpu` idle 0.0, load average 3.11, per-worker RSS
  0.46 GB, swap 0, and no shard file written after ~17 minutes.  Since a shard
  is 100 replicates x 3 families = 300 joins and progress prints only on shard
  completion, that silence is the expected signature of ~3.4 s per join — the
  1.7 s measured during the TRUE join, halved in throughput by two workers
  sharing two vCPUs.  Extrapolated wall-clock ~14 h, which exceeds the
  session's lifetime and guarantees at least one resume.

  The registered default `DEFAULT_MAX_WORKERS = 2` was chosen for a small
  Colab CPU allowance.  The notebook now takes
  `max(DEFAULT_MAX_WORKERS, os.cpu_count() or 1)` so a larger runtime is used
  when one is present, and never fewer workers than the registered default.

  This is scheduling, not science, and the design already says so: the shard
  digest covers `SHARD_DIGEST_FIELDS`, from which `worker_count` is
  deliberately excluded, precisely so that "a shard computed on one worker and
  the same shard computed on two must be identical where it matters".
  `test_worker_count_does_not_change_the_result` verifies that for 1 vs 2
  workers on identical arrays and identical digests, and `worker_count` is
  still recorded in the shard for provenance.  Nothing else moves: no
  threshold, tolerance, gate, statistic, seed, family, replicate count or
  stopping rule, and `rule_fingerprint` is unchanged from `main`.  The
  module itself is untouched by this change; only the notebook cell and its
  contract tests differ.

  Timing is the reason, but timing may never shrink a null.  `N_NULL_REPLICATES`
  stays 10,000 across all three families: a faster machine finishes the same
  null sooner, whereas a shorter null would be a different rule.  Changing the
  worker count at this moment is also the cheapest it will ever be — no shard
  had completed, so the resume directory did not yet exist and no computed
  artifact is discarded.

  *Gate 11 measured the wrong statistic; the first DS1 null is superseded.*

  The registered null completed — 3 families x 10,000, all 100 shards — and
  the decision was `JOIN_UNRESOLVED`, first stopping reason `3_overall_coverage`,
  failed leg `LEG2_POSITIONAL_JOIN`, 6 of 13 gates passed.  Reading the
  bootstrap line exposed a defect in gate 11.

  `J_min_TRUE - q95` is `0.15751 - 0.1517 = 0.0058`, but the reported 95% CI
  was `[0.48239, 0.71952]`.  **The point estimate lay outside its own
  interval**, which a correctly specified bootstrap cannot produce.  Adding
  `q95` back gives `[0.634, 0.871]`, an interval around overall coverage
  `0.75949` — gate 3's value — rather than around `J_min`.

  `record_cluster_bootstrap` resampled records and computed
  `_ratio(hits, total)` from `per_record_certified`, a per-record
  **certification rate**.  The spec registers the statistic as
  `J_min_TRUE - q95(J_null_max)`, and `J_min` is the **minimum over the three
  per-class correct recalls**.  Pooling is precisely what `J_min` exists to
  defeat: it hides class-selective loss, so the interval was built on the one
  quantity the statistic was designed not to be.  The direction is
  anti-conservative — gate 11 passed on a quantity the spec never defines.

  The decision does not move: gate 3 fails first and first-failure-wins, so
  `JOIN_UNRESOLVED` stands whatever gate 11 says.  That does not make a false
  pass acceptable in an immutable bundle.

  Fixed by computing the registered statistic.  `per_record_class_recall`
  emits `j_min`'s numerators and denominators split by record — pooling them
  over all records reproduces `j_min` exactly, which is the property that makes
  them a legitimate bootstrap input — and each replicate now recomputes the
  three per-class recalls over the resampled records and takes their minimum.
  The record draws are unchanged: same seed, same `randrange` order, so only
  the statistic computed from each resample differs.  `finalize_ds1_gate`
  refuses a true-join result that carries no per-record per-class recall, so
  the pooled shape cannot reach gate 11 again.  `bootstrap.json` now records
  `statistic`, so no reader has to infer the quantity from its interval.

  *Why the existing test did not catch it.*  `test_bootstrap_is_reproducible`
  passed `pooled` as `j_true` — it constructed the point estimate to match the
  wrong statistic, so "the point lies inside the interval" was satisfied by
  construction.  A test that adapts its expectation to the implementation
  tests nothing.  The replacement is an **independent reference**: a
  beat-level implementation written from the spec sentence, sharing no code
  with the module beyond the seed, compared **per replicate** across all 200
  replicates rather than at the interval.  An interval-level check cannot see
  a wrong per-replicate statistic, which is exactly how this survived.  Two
  further tests pin it: pooling the per-record per-class counts reproduces
  `j_min` to 1e-12, and on a fixture where pooled coverage is 0.907 while
  `J_min` is 0.158 — the DS1 shape — the whole interval must sit below the
  value the defective implementation produced.

  *What is not relaxed.*  `code_sha256` enters shard identity, so correcting
  the module invalidates every completed shard and the null must be rerun in
  full.  That cost is the provenance rule working, not a reason to weaken it,
  and scoping the hash to "null-relevant code" after seeing results would be
  the same relaxation-after-the-fact the design forbids.  `rule_fingerprint`
  is deliberately **unchanged**: the frozen rule's constants did not move, and
  `MODULE_VERSION` is not bumped for the same reason — the rule was right and
  the implementation was wrong.  A stale clone is caught instead by the
  notebook's `NEED_ATTRS` capability guard, extended with the new names.

  *What is preserved.*  The superseded shard directory and run bundle are
  **not deleted and not rewritten**.  `mark_superseded` adds one immutable
  `SUPERSEDED.json` carrying `SUPERSEDED_GATE11_IMPLEMENTATION_DEFECT`, the
  reason, and the producing module's hash
  `4a3de5e861d9d371439247924a19e81acb3762e065017d6adb1f062a95e054d7`.  The
  rerun writes to a shard directory keyed by the module hash, so shards from
  two code versions can never mix.

  *What the rerun must measure, not assume.*  The bootstrap is not on the null
  generation path, so the family arrays and `J_null_max` **should** reproduce
  bit for bit.  That is a hypothesis, and `compare_null_shard_sets` is the
  measurement: per-family exact comparison plus digests and a first-difference
  index.  If anything differs the result is not accepted and the cause is
  investigated.  `compare_decisions` builds the before/after gate table from
  the two stored `decision.json` files.  No expected CI, and no expected
  decision, is recorded in advance — the decision tree is reapplied to the new
  run and whatever it returns is the result.  DS2, V10 probabilities and any
  association analysis remain sealed throughout.
