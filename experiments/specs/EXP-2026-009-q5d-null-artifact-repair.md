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

`status` is `draft_awaiting_approval`.  The design direction has been
**conditionally accepted**; implementation acceptance and execution have not.
The implementation lands **unexecuted** behind a terminal guard, exactly as the
P1/P2 PREP did: `granted: False` in `EXECUTION_APPROVAL_RECORD`, so an import,
a notebook run or a stray call reaches nothing.  Opening it is a separate user
decision and a separate PR.

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
  the existing null shards, or anything else already on Drive.  The module
  contains **no** `os.remove`, `os.rmdir`, `rename`, `replace` or `shutil` call
  at all, and a test asserts that by AST.
- Edit `mit-bih/q5d_order_preserving_beat_join.py`.  Its LF-normalised SHA-256
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

# Registered identities

| What | Value |
|---|---|
| frozen Q5-D module, **LF-normalised** SHA-256 | `6b098c67df3c8e2c8c070b093e6e2d801566f548a3173626745c4a126a97f226` |
| rule fingerprint | `31c4be9f44582a68c301fe6cc6572f4db6ff0b3de694af68f6ac6a0f48c2b40e` |
| split | `DS1` |
| canonical Q5-D source bundle, Drive folder id | `1JjwBhU8BXf8lRrYPcM2UjFNdIKxE9Ghd` |
| null shard folder, Drive folder id | `1c0AbOwwu1UoZ_8Wz60fhzjDcgCkLHMG9` |
| registered runs parent, Drive folder id | `1YbNX4IeWUph3VFwgpCHGFiibzihF6gXh` |
| shard set | exactly 100 files, `null_shard_00000_00100.json` … `null_shard_09900_10000.json`, contiguous 100-wide ranges |

**`input_digest` has no registered value anywhere in this repository** — only
the field name appears.  It is therefore checked for type and 64-hex format and
for agreement between the shards and the folder-id-verified manifest, and the
run reports that limit rather than comparing against an invented constant that
would always match.  A registration PR should supply one.

## The SHA convention

Registered source identities are **SHA-256 over LF-normalised bytes**: CRLF is
folded to LF before hashing, so the same file checked out on Windows and on
Linux carries the same registered identity.  The raw-byte digest is reported
**alongside** every normalised one and is deliberately different on a CRLF
checkout — it identifies the bytes on this disk, not the registered artifact.
Reporting only one of the two is what made the convention ambiguous: a reader
could not tell a checkout difference from a genuine change.

A **lone CR is refused**, not folded, with `REPAIR_UNDEFINED_NEWLINE`.  Folding
it would let two genuinely different files share one registered identity, and
no artifact in this repository uses CR line endings — so the safe reading of an
unexpected CR is "something is wrong".

# Drive access is mandatory, and authentication lives below the guard

**There is no production route that skips Drive.** `run_repair()` takes no
`adapter` parameter at all: it takes an authenticator and a service factory and
builds the adapter itself, so a run whose provenance rested on a typed mount
path is not reachable by omitting an argument. The source bridge, the shard
bridge, the runs-parent bridge and the output folder-id resolution are all
required, and a `REPAIR_COMPLETE` with no resolved corrective folder id is
structurally impossible — the only other terminal status a route can reach is
the synthetic one below.

A fixture that must run without Drive uses `run_repair_synthetic_fixture()`,
which is explicit about what it is:

- it demands `SYNTHETIC_FIXTURE_MARKER` and refuses without it;
- production is the default and needs no marker;
- its terminal status is `REPAIR_COMPLETE_SYNTHETIC_FIXTURE`, never
  `REPAIR_COMPLETE`, and it reports `ingestable: false`;
- the notebook never calls it, which a test asserts.

**Authentication is part of the guarded route, not of the notebook.** A cell
that built its own service would mint a credential the terminal guard never
saw. The order is:

1. the approval token
2. `EXECUTION_APPROVAL_RECORD.granted`
3. the approved implementation identity, against the code on disk
4. the exact registered folder ids
5. the terminal execution guard
6. the dependency check
7. credential acquisition
8. proof of exactly `https://www.googleapis.com/auth/drive.readonly`
9. the Drive service and the adapter
10. folder-id inventories, including the runs parent
11. the first byte read, and only then any byte written

The credential is requested with exactly one scope and passed explicitly to the
client; the adapter never constructs a default client, because a default client
silently adopts an ambient credential whose scope nobody checked. A broader
credential is **not** accepted merely because it includes the scope we need,
and a credential whose scopes cannot be observed is not accepted either —
"read-only" would be an unverifiable claim. Failure is
`REPAIR_READONLY_SCOPE_UNPROVEN`.

The run records `requested_scopes`, `observed_scopes`,
`exact_readonly_scope_proven`, `credential_type`, the Drive API and version, and
that the adapter's entire surface is `files.list` — and never a token,
credential or authorization header. This reuses the exact-scope principle from
`mit-bih/q5e_prep_p1_p2_asset_identity.py`; it does **not** reuse or translate
that module's approval token, which belongs to a different decision.

With no approval, a wrong token, or the guard closed, the authenticator, the
service factory and the Drive API are called **zero** times — proven by spies
rather than by reading the call order.

# The Drive folder-id bridge

**A folder is chosen by id and never by name.**  A folder that merely has the
right name is not evidence, and that substitution is easy to make and
impossible to notice afterwards.  A manually typed mount path is a name, so a
path alone never establishes identity either.

Before anything is read for a decision, each mount is **bridged** to its
registered folder id:

1. the folder id is queried directly (`files.list` with the id in `parents`),
   never a name search;
2. the inventory must be unambiguous — no duplicate name, duplicate file id,
   missing file id, nameless child, subfolder, shortcut, trashed item,
   Google-native file or sizeless entry;
3. every expected name must be present in **both** the inventory and the mount,
   with equal size, and with every provider checksum the API actually supplied
   (`sha256Checksum`, `md5Checksum`) matching the mount bytes;
4. a checksum the provider did not supply is recorded as `unavailable`, never
   guessed and never counted as a match — the run reports how many files
   matched on a provider checksum and how many on name and size alone;
5. anything unresolved or ambiguous is `REPAIR_INPUT_UNQUALIFIED`.

**The bridged bytes are the judged bytes.** The bridge returns the bytes it
read, and the source snapshot and the shard parser use exactly those — a later
read is a different moment, and on a Drive mount that is not hypothetical. The
files are then re-read and compared against the bridge's digests, so a
substitution is *detected* rather than merely rendered ineffective:
`REPAIR_BYTES_MOVED_AFTER_BRIDGE`. This applies to the eleven source files and
to all 100 shards, and a same-length replacement — the case a size check would
miss — is what the regression fixture uses.

## The runs parent is bridged too

A mount path is a name, and a name is what this module refuses to treat as
identity everywhere else, so the write destination gets the same treatment.
Before any `mkdir`:

- the registered source folder id `1JjwBhU8BXf8lRrYPcM2UjFNdIKxE9Ghd` must be a
  single live direct child of the registered parent id
  `1YbNX4IeWUph3VFwgpCHGFiibzihF6gXh`, by API inventory;
- `dirname(realpath(SOURCE_DIR))` must equal `realpath(RUNS_PARENT_DIR)`;
- the target's parent must equal `RUNS_PARENT_DIR`;
- no component may be a symlink, junction or reparse point.

The source bundle is what links the two worlds: it has both a registered folder
id and a mount path, so if the id is a child of the parent id and the mount
lives directly under the runs-parent mount, the runs-parent mount is the
registered parent's mount. Injecting a different directory under the same
`RUNS_PARENT_DIR` string breaks the second half and is refused. **A failed
parent bridge means `os.mkdir` is called zero times**, which a spy asserts.

## Output folder-id resolution

On success the new corrective folder's **own** Drive folder id is read back
read-only from the registered runs parent and recorded, so the result is
identifiable by id afterwards rather than by picking a folder name later.

Drive is eventually consistent, so a folder that exists on the mount can be
briefly invisible to `files.list`. That is handled with a **short, bounded,
read-only retry** — list calls and a wait, nothing else. If it never resolves:

- the run stops with `REPAIR_OUTPUT_FOLDER_ID_UNRESOLVED`;
- the written output is reported by exact path and real listing and preserved;
- it is **not** `REPAIR_COMPLETE`, not accepted and not registered;
- **no second corrective folder is created** — that would turn a visibility
  problem into two artifacts;
- `reconcile_output_folder_id()` re-resolves it later, read-only, after
  re-checking the parent folder id, the exact folder name, the exact twelve-file
  listing and every digest. It writes nothing and edits nothing, and it refuses
  to resolve an output that no longer matches what was written.

Result acceptance is impossible until that resolution succeeds.

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

- Exactly those four ZIP members, with **no duplicate member name**.  A ZIP may
  legally carry two entries of one name and a mapping-based reader silently
  keeps one, so duplicates are detected on the raw name list.
- Readable with `allow_pickle=False`.
- Every value finite — no NaN, no infinity.
- For every replicate `b`, `j_null_max[b]` is **exactly equal** to the maximum
  of the three family arrays at `b`.  Exact equality, not a tolerance: these are
  the same float64 values that already exist in the shards.
- `j_null_max` is **exactly equal**, element by element, to the `j_null_max`
  already recorded in the existing bundle's `null_summary.json`.  This is the
  independent cross-check: the shards and the summary were written by different
  code paths in the original run.
- The three family arrays are in `finalize_null_shards()`'s canonical order —
  family name sorted, replicate ascending within each.

## Member names — resolved (N1)

The members are the **native frozen control family names** plus `j_null_max`:
`wrong_record`, `order_shuffle`, `circular_shift`, `j_null_max`.

The proposed aliases `j_null_cross_record`, `j_null_within_record` and
`j_null_rr_mismatch` are **rejected**, not deferred, and the reason is
substantive rather than procedural: `order_shuffle` and `circular_shift` are
*both* within-record manipulations, so there is no bijection from the three
frozen families onto the proposed triple, and nothing uniquely corresponds to
`rr_mismatch`. Any mapping would be a guess, and a wrong guess would pass every
structural clause above while mislabelling a published artifact.

`MEMBER_NAME_BY_FAMILY` stays the identity mapping, `MEMBER_NAMING_UNRESOLVED`
is `False`, and the proposal survives only as `REJECTED_PROPOSAL`, an audit
record nothing reads. Computed values and array order are unchanged by this
decision.

## Qualification of the repair input

Before a single byte of NPZ is produced, all of the following must hold.  Any
failure stops the run with

    REPAIR_INPUT_UNQUALIFIED

and publishes **neither the NPZ nor a new bundle**:

- the shard mount is bridged to folder id `1c0AbOwwu1UoZ_8Wz60fhzjDcgCkLHMG9`;
- the folder holds **exactly** the 100 preregistered filenames — nothing
  missing, nothing extra, no duplicate, no subdirectory, no non-file entry;
- each file parses as JSON; a malformed or unreadable one becomes a **problem in
  the qualification report**, never a raw `JSONDecodeError` escaping to the
  caller — the thing this check exists to detect must not arrive as a crash;
- each shard passes a **schema** check by type and format, not by truthiness:
  `replicate_start`/`replicate_end` real `int`s equal to the preregistered
  range, `null_runner_version` and `master_seed` `int`s equal to the registered
  values, `split == "DS1"`, `families` exactly the registered tuple,
  `code_sha256` / `rule_fingerprint` / `input_digest` / `digest` full 64-hex
  strings, and the `j` arrays and `j_null_max` lists of finite numbers of the
  right length.  (`str(None)` is `"None"` — a non-empty string that a presence
  check would accept and that carries no identity at all.)
- `code_sha256` and `rule_fingerprint` equal the **registered** values, and all
  three identity digests equal the folder-id-verified manifest's;
- each shard passes its own recorded digest (`BJ.shard_digest`);
- replicate coverage is exactly `0..9999`, with no gap and no overlap;
- each shard's own `j_null_max` equals the per-replicate family maximum;
- the live `rule_fingerprint()` of the frozen module equals the registered one.

The identity anchor is the **folder-id-verified bundle manifest**, not the
shards.  Deriving the expected identity from the shards and then checking the
shards against it would accept any internally consistent set, including one
belonging to a different run — and a manifest is only trusted because the bytes
it was parsed from are tied to the registered folder id and because its fields
also agree with registered constants.

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

So the repair builds an **identity-only context**: the real identity fields, and
record maps that **raise if anything reads them**.  The invariant is enforced at
runtime, not asserted in a comment, and a regression test both confirms the maps
refuse reads and finalises a shard set through them.  If that ever stops being
true, the test fails rather than the repair silently reconstructing from
nothing.

## Serialisation

The NPY/NPZ bytes are written by a small, explicit writer in the repair module
and read back by **two** independent readers.  Three reasons, stated so a
reviewer can reject them:

1. **The verifier must not be only the writer's own library.** An independent
   parser checks the bytes rather than checking that numpy agrees with numpy.
2. **Deterministic bytes.** A ZIP records a timestamp per member; the writer
   pins it, so the same arrays always produce the same file. "Deterministic
   reconstruction" should mean the bytes too, not only the numbers.
3. **The contract is testable where there is no numpy.** The repository's test
   environment has none, and a critical path that cannot be exercised in CI is
   not really covered.

The format is NPY v1.0, `'<f8'`, `fortran_order: False`, stored (uncompressed)
in the ZIP — the same thing `numpy.savez` writes for these arrays.

**In production, numpy verification is mandatory.**  `numpy.load(BytesIO(blob),
allow_pickle=False)` is actually called, every array's dtype, shape, finiteness
and values are compared against the reconstructed arrays, and if numpy cannot be
imported the run stops with `REPAIR_NUMPY_UNAVAILABLE` rather than publishing.
The independent parser is a cross-check, not a substitute.  Nothing reports a
readability flag as a declared constant — an earlier draft returned a hard-coded
`allow_pickle_false_readable: True`, which is a constant dressed as a
measurement and would have kept saying `True` for a file numpy could not open.

# The corrective bundle

Target: a **new** folder.  Nothing is written into, beside, or over the
existing run folder.

1. **Source snapshot.** The eleven are validated and then read **once**, into an
   immutable snapshot.  Both the judging (manifest, `null_summary.json`) and the
   copying use those same bytes.  Reading a file to judge it and reading it
   again to copy it is a TOCTOU window — the run would verify one state and
   publish another, which on a Drive mount is not hypothetical.
2. The source must hold exactly the **eleven** names — the twelve
   `BUNDLE_FILES` minus `negative_control_null.npz` — with nothing missing,
   nothing unexpected and no subdirectory.  Otherwise
   `REPAIR_SOURCE_BUNDLE_UNEXPECTED`: a source that is not the bundle P2
   measured is not the thing this repair was authorised for.
3. **Target safety, checked before anything is created.**  The target is
   refused if it is the source or shard directory or inside either, if either is
   inside it, if its parent is not the approved runs parent, if any path
   component is a symlink or reparse point, or if the name already exists.
4. The target name is claimed with a single `os.mkdir`, which never replaces and
   never follows.
5. Each of the eleven is copied **byte-identically** from the snapshot: written
   as an exclusive create (`O_CREAT | O_EXCL | O_BINARY`), then re-read and
   re-hashed.  A mismatch is `REPAIR_COPY_NOT_BYTE_IDENTICAL`.  Metadata-copying
   helpers are not used: the contract is over content.
6. The NPZ is written the same way, as the twelfth file.
7. The final directory listing must equal `BJ.BUNDLE_FILES` exactly — twelve
   names, `missing = 0`, `unexpected = 0` — verified by a **separate** function
   that reopens the files, because a writer that certifies its own output is
   checking its variables.
8. **At the end of the run the source is re-hashed** against the snapshot.  The
   criterion is fixed here, before the run: every one of the eleven must still
   hash to what the snapshot holds, or `REPAIR_SOURCE_CHANGED_DURING_RUN`.
   Deciding afterwards which differences were acceptable is how a check becomes
   a formality.
9. Nothing else is written into the folder.  In particular **no provenance
   sidecar**: the corrective folder is the twelve files and nothing more.

The repair's own record therefore lives outside the folder.  A run returns a
decision structure and prints a report; that **saved notebook output is the
external record**, the same anchor rule the P1/P2 PREP uses, and the digests and
the new folder id are copied from it into this document's Decision log,
`research/ASSETS.md` and `research/PROJECT_STATE.md` by a separate PR.

# Failure publication contract

An earlier draft claimed "any failure leaves no corrective folder at all".  That
was true only of failures before the claim, and stating it unconditionally would
have left a reader unable to account for a directory that does exist.

- **Stop before the target is created** — no directory exists.
- **Stop after the target is created** — the partial directory is left
  **exactly where it is**, at the reported path, with its actual file list
  reported, marked `REPAIR_INCOMPLETE_TARGET_PRESERVED`.  It is never
  committed, never accepted, never registered, and never deleted, overwritten or
  renamed by this module.
- **A retry uses a new unique target path.**  It does not reuse, clean or resume
  a preserved directory.

The module carries this as `FAILURE_PUBLICATION_CONTRACT`, the error object
carries the path and listing, the notebook prints them, and tests assert both
halves.  No `COMMITTED` marker is written by this repair in any case — the
marker is not one of the twelve `BUNDLE_FILES`.

# Execution pinning, without self-reference

A 40-hex string typed into a notebook is not an approval — it is an assertion by
whoever typed it — and a commit SHA cannot be written into the commit it names.
So the pin is two separate facts, and they are never collapsed:

**Approved implementation.** `APPROVED_IMPLEMENTATION_COMMIT` names the commit
Codex reviewed, and `APPROVED_ARTIFACT_DIGESTS` records the LF-normalised
digests of the spec, the notebook, the frozen Q5-D module, and the repair
module's **science digest**. Both are written by a *later* execution-enable PR,
so the record points backwards and never certifies itself.

The repair module is deliberately absent from that digest table: a record inside
a file cannot certify that file. What covers it is `module_science_digest()` —
the module hashed with the fenced approval block removed. An enable PR may change
that block and nothing else, and the science digest proves it: identical before
and after, and different the moment any logic moves. "The approval only flipped a
flag" therefore becomes a checked claim rather than a promise in a commit
message.

**Execution head.** The notebook measures the actual `HEAD` from git after a
detached checkout, refuses a dirty working tree, and passes it in as
`execution_head`. The decision's `pinned_commit` is that measured value — not a
module constant that would read `None`.

Before any registered asset is opened, `verify_execution_identity()` requires
the approved record to exist, the execution head to be a 40-hex value measured
from git, and every digest on disk to equal the approved one. Anything else is
`REPAIR_EXECUTION_IDENTITY_UNVERIFIED`. With nothing approved — the state this
PR ships in — a production run cannot start.

# Stop reasons

Each is terminal.  A repair that stops publishes nothing that is marked
accepted.

| Reason | Meaning |
|---|---|
| `REPAIR_NOT_APPROVED` | reached without the separate execution approval |
| `REPAIR_FROZEN_MODULE_MOVED` | the imported Q5-D module or rule fingerprint is not the registered one |
| `REPAIR_EXECUTION_IDENTITY_UNVERIFIED` | the running code is not verifiably the approved implementation |
| `REPAIR_READONLY_SCOPE_UNPROVEN` | the credential does not carry exactly the read-only scope |
| `REPAIR_BYTES_MOVED_AFTER_BRIDGE` | a file changed between being tied to its folder id and being judged |
| `REPAIR_UNDEFINED_NEWLINE` | a lone CR, which has no defined registered identity |
| `REPAIR_INPUT_UNQUALIFIED` | the folder-id bridge or the shards failed any clause above |
| `REPAIR_SUMMARY_DISAGREES` | reconstructed `j_null_max` ≠ `null_summary.json`'s |
| `REPAIR_NPZ_CONTRACT_FAILED` | the produced bytes fail any NPZ clause above |
| `REPAIR_NUMPY_UNAVAILABLE` | the mandatory numpy verification could not run |
| `REPAIR_SOURCE_BUNDLE_UNEXPECTED` | the source folder is not the eleven |
| `REPAIR_SOURCE_CHANGED_DURING_RUN` | the source moved between snapshot and end |
| `REPAIR_TARGET_EXISTS` | the corrective folder name is already taken |
| `REPAIR_TARGET_UNSAFE` | the target is inside an input, outside the approved parent, or reached through a link |
| `REPAIR_COPY_NOT_BYTE_IDENTICAL` | a copied file's digest moved |
| `REPAIR_OUTPUT_FOLDER_ID_UNRESOLVED` | the written output's Drive folder id did not resolve |

`REPAIR_INCOMPLETE_TARGET_PRESERVED` is **not** a stop reason — it is the state
of a directory a stop left behind.

# Acceptance criteria

Fixed before any measurement exists.

- the approved implementation commit and digests, the measured `execution_head`,
  and the module / spec / notebook digests re-measured after checkout, both
  LF-normalised and raw
- the credential audit: `requested_scopes`, `observed_scopes`,
  `exact_readonly_scope_proven`, `credential_type`, Drive API and version, and
  that the adapter exposes only `files.list`
- the runs-parent bridge, showing the registered source id as a direct child of
  the registered parent id
- the frozen Q5-D LF-normalised **and** raw SHA-256, and the live rule
  fingerprint
- the three registered folder ids, the inventory method (folder id, not name
  search), every ambiguity category at zero, and per-file bridge rows with file
  id, size and provider-checksum availability and match
- the shard qualification: 100 of 100 preregistered filenames, missing / extra /
  duplicate / subdirectory all empty, per-shard schema and digest results, and
  coverage reported as ranges rather than as a claim
- the manifest-anchored identity beside the shards' own, and an explicit
  statement that `input_digest` has no registered counterpart
- the reconstructed arrays' lengths and the `j_null_max` agreement with
  `null_summary.json` as an exact element-wise comparison, with the index of the
  first difference if any
- the NPZ's member list, absence of duplicate members, dtypes, shapes,
  finiteness and the two exact-equality checks, verified by **reading the
  produced bytes back** under both readers, with the numpy verification's
  version and result recorded
- the SHA-256 of the produced NPZ
- the eleven source digests and the eleven target digests, side by side, and the
  end-of-run source re-hash
- the final twelve-name directory listing, with `missing = 0`, `unexpected = 0`
- the corrective folder's **own Drive folder id**, read back read-only
- an explicit statement that the source bundle and the shard folder were opened
  read-only and that nothing was written outside the new folder
- `training_performed`, `join_rerun`, `null_recomputed`, `ds2_outcome_opened`,
  `v10_probability_opened` all false

# Order

1. Codex design acceptance of this spec, of the three conditional decisions, and
   of the member-naming resolution
2. user approval, `status` → `approved_for_implementation`
3. separate user **execution** approval, which opens the terminal guard and
   fixes the pinned commit
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

The NPZ contract above was written before the serialiser, and the serialiser was
written to it.  Only one is implemented; there is no second candidate to choose
between after seeing results.

## 2026-08-12 — Codex conditional acceptance, and the blockers it named

Codex accepted the **design direction** conditionally.  Implementation
acceptance and execution are **not** granted, the PR stays a draft, and the
boundary is unchanged: no shard content read, no NPZ produced, no corrective
Drive folder created, no beat join re-run.

**Decision 1 — the identity-only `NullContext` is conditionally approved**, on
condition that the runtime invariant and its regression test are kept.  They
are: the record maps raise on any read, and a test both proves the refusal and
finalises a shard set through the context.

**Decision 2 — anchoring run identity on the canonical bundle manifest is
approved**, on condition that the manifest and its path are not trusted on their
own assertion.  They are not: the mount is bridged to the registered Drive
folder id file by file, and the manifest's `split`, `code_sha256` and
`rule_fingerprint` must equal registered constants.  `input_digest` has no
registered counterpart in this repository, so the run says so explicitly rather
than comparing against a value invented for the purpose.

**Decision 3 — the deterministic explicit NPY/NPZ writer is conditionally
approved**, on condition that a real execution verifies through
`numpy.load(..., allow_pickle=False)`.  It now does, mandatorily: production
passes `require_numpy=True`, the call is made, every array is compared, and a
missing numpy is `REPAIR_NUMPY_UNAVAILABLE`.  The previous hard-coded
`allow_pickle_false_readable: True` is gone.

### How each blocker was closed

| | Blocker | Resolution |
|---|---|---|
| A | SHA convention | Registered identity is explicitly the **LF-normalised** digest; both digests are reported everywhere; a lone CR is refused with `REPAIR_UNDEFINED_NEWLINE`. |
| B | Drive folder-id bridge | Mounts are tied to the three registered folder ids by inventory, size and every available provider checksum; ambiguity or an unresolved bridge is `REPAIR_INPUT_UNQUALIFIED`; a same-named folder is never a substitute. |
| C | Shard exact contract | Exactly the 100 preregistered filenames and ranges; missing / extra / duplicate / overlap / gap / subdirectory refused; identity checked against registered constants **and** the manifest; full type/format/hex validation; malformed JSON becomes a structured stop. |
| D | Immutable source snapshot | The eleven are read once; judging and copying share those bytes; the source is re-hashed at the end against a criterion fixed in advance. |
| E | Target safety | Target inside an input, an input inside the target, a parent that is not the approved runs parent, a link-like component, or an existing name are all refused before anything is created. |
| F | Failure publication | The unconditional "no folder" claim is withdrawn and replaced by the contract above; the error carries the preserved path and listing; no delete, rename or overwrite exists in the module, asserted by AST; retries use a new unique path; spec, code, notebook and tests all say the same thing. |
| G | Independent NPZ verification | Exactly four members with no duplicate names, float64 `(10000,)`, finite, elementwise maximum and `null_summary.json` equality, verified by an independent parser **and** by a real `numpy.load(..., allow_pickle=False)`; production stops without numpy. **The member *names* remain unresolved — see below.** |
| H | Notebook pinning and result identity | Execution is pinned to an exact commit SHA, `HEAD` and a clean tree are confirmed, module/spec/notebook digests are re-measured after checkout, and the new corrective folder's Drive id is read back read-only and recorded. |

### N1 — member names, resolved

The proposed aliases are **rejected**, not deferred: `order_shuffle` and
`circular_shift` are both within-record manipulations, so no bijective semantic
mapping onto cross-record / within-record / rr-mismatch exists and nothing
uniquely corresponds to `rr_mismatch`.  Native frozen family names are retained;
`MEMBER_NAMING_UNRESOLVED` is `False`; `PROPOSED_MEMBER_NAMES` is gone and only
`REJECTED_PROPOSAL` remains, as an audit record nothing reads.  Computed values
and array order are unchanged.

## 2026-08-12 — the second review round: N1 and R1-R6

Codex accepted the A-H work and confirmed the Windows result (54 functions /
331 assertions there).  The blockers below were all about the **production**
route's provenance and approval, and none of them changed a gate, a null value,
a seed, a family or the replicate count.

| | Blocker | Resolution |
|---|---|---|
| N1 | member names | native frozen family names retained; proposed aliases rejected because no bijective semantic mapping exists |
| R1 | adapter mandatory | `run_repair()` has no `adapter` parameter; it takes an authenticator and a service factory and builds the adapter below the guard.  Drive-free fixtures use `run_repair_synthetic_fixture()`, which requires an explicit marker and can only reach `REPAIR_COMPLETE_SYNTHETIC_FIXTURE`, so `REPAIR_COMPLETE` without a resolved folder id is structurally unreachable |
| R2 | auth below the guard | the notebook calls no authenticator and builds no service; the module mints the credential below the guard, proves exactly `drive.readonly`, and records the audit.  Guard closed or token wrong → zero credential, service and API calls, proven by spies |
| R3 | bridge bytes are judged bytes | the bridge returns its bytes, the snapshot and the shard parser use them, and a re-read against the bridge digests turns a same-length substitution into `REPAIR_BYTES_MOVED_AFTER_BRIDGE` |
| R4 | runs parent bridged | the registered source id must be a live direct child of the registered parent id, and the source mount must sit directly under the runs-parent mount; a failed bridge means `os.mkdir` is never called |
| R5 | post-write folder id | bounded read-only retry; unresolved → `REPAIR_OUTPUT_FOLDER_ID_UNRESOLVED` with the output preserved, never accepted, no second folder, and a read-only `reconcile_output_folder_id()` that re-checks everything and writes nothing.  One boundary in `_route()` attaches the preserved path and listing to **every** post-write failure |
| R6 | non-self-referential pin | approved implementation (commit + spec/notebook/frozen/science digests, recorded by a later PR) and execution head (measured from git by the notebook) are separate; the module's own coverage is `module_science_digest()`, which an approval-only edit leaves unchanged |

Two design decisions still worth weighing rather than inheriting: the
identity-only context, and the explicit writer instead of `numpy.savez`.  Both
are argued above with what they buy and what they cost, and both are
substitutable without touching the contract.

One limitation stated plainly: **production requires numpy and this
repository's test container has none**, so the production-route tests inject a
stub that asserts `numpy.load` was called with `allow_pickle=False`.  Where real
numpy exists the genuine cross-check runs instead.  The stub keeps the route
reachable in CI; it is not evidence that numpy can read the file, and it is not
used by any production path.
