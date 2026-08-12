---
experiment_id: EXP-2026-009
substage: Q5D_NULL_ARTIFACT_REPAIR
title: Q5-D negative-control null artifact repair
status: draft_awaiting_approval
design_owner: codex
implementation_owner: claude
analysis_only: true
training_required: false
dataset: none_artifact_repair_only
split: none_artifact_repair_only
parent_experiment: EXP-2026-007
parent_spec: experiments/specs/EXP-2026-007-q5d-order-preserving-beat-join-gate.md
originating_decision: experiments/specs/EXP-2026-008-q5e-prep-p1-p2-execution-contract.md
primary_metric: none_artifact_repair_only
created: 2026-08-12
---

# Status boundary

This is a **packaging repair**, not an experiment.  It produces no scientific
result, answers no scientific question, and no outcome of a repair run may be
cited as a Q5-D or Q5-E finding.  Nothing here re-runs the beat join, the
10,000 × 3 null, or any part of `EXP-2026-007`; nothing here recomputes a `J`
value.  Every number it emits already exists in an artifact that has been
sitting on Drive since 2026-08-11 — this moves bytes and checks them.

`status` is `draft_awaiting_approval`.  The implementation lands **unexecuted**
behind a terminal guard, exactly as the P1/P2 PREP did: `granted: False` in
`EXECUTION_APPROVAL_RECORD`, so an import, a notebook run or a stray call
reaches nothing.  Opening it is a separate user decision and a separate PR.

# Why this exists

`EXP-2026-008` Q5-E PREP P2 read the canonical Q5-D bundle at the registered
folder id and found **eleven** files where the contract names twelve.  The
missing one is `negative_control_null.npz`.

Codex's verdict, recorded in the
[P1/P2 execution contract](EXP-2026-008-q5e-prep-p1-p2-execution-contract.md)
Decision log on 2026-08-12:

    P2_PRODUCER_ARTIFACT_OMISSION

`negative_control_null.npz` is registered in **both** `EXP-2026-007`'s Required
outputs and `BUNDLE_FILES` in `mit-bih/q5d_order_preserving_beat_join.py`, and
no approved Decision log removed it from either.  So the twelve-file contract
is not reduced to eleven, and the producer's output packaging is what is short.

**No measurement was lost.**  `null_summary()` returns
`"j_null_max": list(maxima)` — the complete 10,000-replicate vector, inlined
into `null_summary.json` — and the per-family values are preserved in the 100
shards.  What is absent is a file.

# What this repair does, in one sentence

Reconstruct `negative_control_null.npz` deterministically from the 100 existing
validated shards through the **frozen** `finalize_null_shards()` path, and
place it in a **new** corrective bundle folder alongside byte-identical copies
of the existing eleven files.

# What it may not do

- Re-run the beat join or any null replicate.  No `J` value is computed here.
- Modify, delete, overwrite, move or re-timestamp the existing Drive bundle,
  the existing null shards, or anything else already on Drive.
- Edit `mit-bih/q5d_order_preserving_beat_join.py`.  Its SHA-256
  `6b098c67df3c8e2c8c070b093e6e2d801566f548a3173626745c4a126a97f226` is a
  registered identity across Q5-E and is embedded in the shard folder name; the
  repair module **imports it read-only** and asserts that digest before doing
  anything.
- Change any gate, threshold, rule fingerprint, decision, registered constant,
  or `BUNDLE_FILES`.
- Put anything in the corrective folder that is not one of the twelve
  `BUNDLE_FILES` names.
- Open a DS2 per-beat label or a V10 probability, run `detect_r()`, aggregate
  M0–M4, compute an association or S PR-AUC, or train anything.
- Register a value.  Registration stays a separate PR after a combined pass.

# The NPZ contract

**Fixed here, before the implementation exists**, so that a serialisation
cannot be chosen after seeing which one verifies.  A repair run produces
exactly one NPZ, by one route, and either it satisfies every clause below or
nothing is published.

| Array | dtype | shape |
|---|---|---|
| `wrong_record` | float64 | `(10000,)` |
| `order_shuffle` | float64 | `(10000,)` |
| `circular_shift` | float64 | `(10000,)` |
| `j_null_max` | float64 | `(10000,)` |

- Exactly those four names.  No extra array, no metadata array.
- Readable with `allow_pickle=False`.
- Every value finite — no NaN, no infinity.
- For every replicate `b`, `j_null_max[b]` is **exactly equal** to
  `max(wrong_record[b], order_shuffle[b], circular_shift[b])`.  Exact equality,
  not a tolerance: these are the same float64 values that already exist in the
  shards, so anything but equality means something was transformed on the way
  through.
- `j_null_max` is **exactly equal**, element by element, to the `j_null_max`
  already recorded in the existing bundle's `null_summary.json`.  This is the
  independent cross-check: the shards and the summary were written by different
  code paths in the original run, and the repair is only correct if they agree.
- The three family arrays are in `finalize_null_shards()`'s canonical order —
  family name sorted, replicate ascending within each — which is the order the
  frozen module already guarantees is independent of execution order and worker
  count.

## Qualification of the repair input

Before a single byte of NPZ is produced, all of the following must hold over
the 100 shards.  Any failure stops the run with

    REPAIR_INPUT_UNQUALIFIED

and publishes **neither the NPZ nor a new bundle**:

- every shard passes its own recorded digest (`BJ.read_null_shard`);
- every shard's identity fields match: `null_runner_version`, `split`,
  `families`, `master_seed`, `rule_fingerprint`, `code_sha256`, `input_digest`;
- `code_sha256`, `rule_fingerprint` and `input_digest` match the **existing
  bundle's `manifest.json`**, not merely each other;
- replicate coverage is exactly `0..9999`, with no gap and no overlap;
- each shard's own `j_null_max` equals the per-replicate family maximum;
- the live `rule_fingerprint()` of the frozen module equals the shards'.

The identity anchor is deliberately the bundle manifest rather than the shards
themselves.  Deriving the expected identity from the shards and then checking
the shards against it would accept any internally consistent set, including one
belonging to a different run.

## How the frozen finaliser is reached

`finalize_null_shards(shards, context, total)` is the only sanctioned route to
the arrays, and it takes a `NullContext`.  Constructing a full context would
mean rebuilding the entire run's join inputs — which is exactly the re-run this
repair exists to avoid.

It does not need them.  `finalize_null_shards()` and `verify_null_shard()`
touch only `context.identity()`: `null_runner_version`, `split`, `families`,
`master_seed`, `rule_fingerprint`, `code_sha256`, `input_digest`.  The heavy
maps (`mamba_by_record`, `cache_by_record`, `processed_classes`,
`mamba_classes`) are read by `compute_null_shard()` alone, which this repair
never calls.

So the repair builds an **identity-only context**: the real identity fields,
and empty record maps.  A contract test pins the invariant that makes this
legitimate — finalisation succeeds with the maps empty, which it could not do
if anything on the path read them.  If that ever stops being true, the test
fails rather than the repair silently reconstructing from nothing.

**Flagged for design review:** this is the one place the repair uses a frozen
function in a way its author did not have in mind.  It preserves every check
that bears on correctness and skips only data that is provably unread, but a
reviewer should agree with that before execution is approved.

## Serialisation

The NPY/NPZ bytes are written by a small, explicit writer in the repair module
rather than by `numpy.savez`, and read back by a matching explicit reader.
Three reasons, stated so a reviewer can reject them:

1. **The verifier must not be the writer's own library.** Reading the file back
   through the same dependency that produced it checks that numpy agrees with
   numpy.  An independent reader checks the bytes.
2. **Deterministic bytes.** A ZIP records a timestamp per member; the writer
   pins it, so the same arrays always produce the same file. "Deterministic
   reconstruction" should mean the bytes too, not only the numbers.
3. **The contract is testable where there is no numpy.** The repository's test
   environment has none, and a critical path that cannot be exercised in CI is
   not really covered.

The format is NPY v1.0, `'<f8'`, `fortran_order: False`, stored (uncompressed)
in the ZIP — the same thing `numpy.savez` writes for these arrays. Where numpy
**is** available, a test additionally loads the produced bytes with
`numpy.load(..., allow_pickle=False)` and asserts the values match exactly, so
the claim "numpy can read this" is measured rather than asserted.  If Codex
prefers `numpy.savez`, it is a one-function substitution and the contract above
is unchanged.

# The corrective bundle

Target: a **new** folder.  Nothing is written into, beside, or over the
existing run folder.

1. The source bundle must hold exactly the **eleven** names — the twelve
   `BUNDLE_FILES` minus `negative_control_null.npz` — with nothing missing and
   nothing unexpected.  Otherwise `REPAIR_SOURCE_BUNDLE_UNEXPECTED`: a source
   that is not the bundle P2 measured is not the thing this repair was
   authorised for.
2. The target folder must not already exist.  It is claimed with a single
   `os.mkdir`, which never replaces and never follows.
3. Each of the eleven is copied **byte-identically**: its SHA-256 is taken from
   the source bytes, the bytes are written to the target as an exclusive create
   (`O_CREAT | O_EXCL | O_BINARY`), and the target is then re-read and hashed.
   A mismatch is `REPAIR_COPY_NOT_BYTE_IDENTICAL`.  Metadata-copying helpers
   are not used: the contract is over content.
4. The NPZ is written the same way, as the twelfth file.
5. The final directory listing must equal `BJ.BUNDLE_FILES` exactly — twelve
   names, `missing = 0`, `unexpected = 0`.
6. Nothing else is written into the folder.  In particular **no provenance
   sidecar**: the corrective folder is the twelve files and nothing more.

The repair's own record therefore lives outside the folder.  A run returns a
decision structure and prints a report; that **saved notebook output is the
external record**, the same anchor rule the P1/P2 PREP uses, and the digests
are copied from it into this document's Decision log, `research/ASSETS.md` and
`research/PROJECT_STATE.md` by a separate PR.  No new bundle writer is
introduced — an extra artifact would need its own location, atomicity and
identity contract before it could carry evidence.

# Stop reasons

Each is terminal.  A repair that stops publishes nothing.

| Reason | Meaning |
|---|---|
| `REPAIR_NOT_APPROVED` | reached without the separate execution approval |
| `REPAIR_FROZEN_MODULE_MOVED` | the imported Q5-D module is not the registered SHA-256 |
| `REPAIR_INPUT_UNQUALIFIED` | the shards failed any qualification clause above |
| `REPAIR_SUMMARY_DISAGREES` | reconstructed `j_null_max` ≠ `null_summary.json`'s |
| `REPAIR_NPZ_CONTRACT_FAILED` | the produced bytes fail any NPZ clause above |
| `REPAIR_SOURCE_BUNDLE_UNEXPECTED` | the source folder is not the eleven |
| `REPAIR_TARGET_EXISTS` | the corrective folder name is already taken |
| `REPAIR_COPY_NOT_BYTE_IDENTICAL` | a copied file's digest moved |

# Acceptance criteria

Fixed before any measurement exists.

- the frozen Q5-D SHA-256 asserted at import and recorded in the report
- the 100 shards' qualification report: per-clause result, the shared identity,
  and the coverage check as ranges rather than a claim
- the manifest-anchored identity, shown next to the shards' own
- the reconstructed arrays' lengths, and the `j_null_max` agreement with
  `null_summary.json` reported as an exact element-wise comparison with the
  index of the first difference if any
- the NPZ's four names, dtypes, shapes, finiteness, and the two exact-equality
  checks, verified by **reading the produced bytes back**, not from the values
  that were written
- the SHA-256 of the produced NPZ
- the eleven source digests and the eleven target digests, side by side
- the final twelve-name directory listing, with `missing = 0`, `unexpected = 0`
- an explicit statement that the source bundle and the shard folder were opened
  read-only and that nothing was written outside the new folder
- `training_performed`, `join_rerun`, `null_recomputed`, `ds2_outcome_opened`,
  `v10_probability_opened` all false

# Order

1. Codex design acceptance of this spec and of the flagged context decision
2. user approval, `status` → `approved_for_implementation`
3. separate user **execution** approval, which opens the terminal guard
4. repair run: reconstruct, assemble, verify — read-only over the source
5. registration PR fixes the new folder id, the NPZ digest and the lineage
6. separate user approval to re-run Q5-E PREP P1/P2 against the corrective
   bundle
7. P1/P2 re-run; only on a **combined pass** do the P1 aggregate and the five
   P2 digests become registration eligible
8. only then, P3 source-equivalence PREP

Nothing in steps 4–8 follows automatically from the step before it.

# Decision log

## 2026-08-12 — specified and implemented, never executed

The implementation lands with the terminal guard closed (`granted: False`), so
no shard has been opened, no NPZ has been produced, no Drive folder has been
created or copied, and no digest has been computed against a real artifact.
Every test is synthetic: shard fixtures are built from the frozen module's own
`shard_digest()` over invented `J` values, so no test can pass by recognising a
real number.

The NPZ contract above was written before the serialiser, and the serialiser
was written to it.  Only one is implemented; there is no second candidate to
choose between after seeing results.

Two decisions a reviewer should weigh rather than inherit: the identity-only
`NullContext`, and the explicit NPY/NPZ writer instead of `numpy.savez`. Both
are argued above with what they buy and what they cost, and both are
substitutable without touching the contract.
