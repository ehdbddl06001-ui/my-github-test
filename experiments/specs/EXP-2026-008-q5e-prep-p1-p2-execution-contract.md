---
experiment_id: EXP-2026-008
substage: Q5E_PREP_P1_P2_ASSET_IDENTITY
title: Q5-E PREP P1+P2 asset identity execution contract
status: approved_for_implementation
design_owner: codex
implementation_owner: claude
analysis_only: true
training_required: false
dataset: MIT-BIH
split: none_asset_identity_only
parent_experiment: EXP-2026-008
parent_spec: experiments/specs/EXP-2026-008-q5e-leg2-failure-mechanism-audit.md
primary_metric: none_asset_identity_only
parent_primary_metric: none_diagnostic_association_only
created: 2026-08-12
---

# Status boundary

This document is the **execution contract** for two read-only asset-identity
preflights, P1 and P2.  It is not a scientific design and produces no
scientific result: nothing here measures anything about ECG data, and no
outcome of a P1/P2 run may be cited as a Q5-E finding.

The implementation exists (`mit-bih/q5e_prep_p1_p2_asset_identity.py`) and has
**never been executed**.  Running it against the registered assets needs a
separate read-only user approval that does not exist yet.  A terminal guard in
`run_prep()` sits after every check and before the first registered read; this
implementation PR does not remove it.

P3 — the source-matching differential — is **not** in scope here.

# Why these two preflights exist

Two of the three items that stop a Q5-E run are asset identities that were
never frozen:

| | Item | Current state | Q5-E stop |
|---|---|---|---|
| **P1** | MIT-BIH publisher tree aggregate | recorded only as `0b46a411…` | `INPUT_IDENTITY_REGISTRATION_REQUIRED` |
| **P2** | canonical Q5-D bundle input digests | not recorded anywhere | `SOURCE_BUNDLE_DIGEST_FREEZE_REQUIRED` |

A truncated digest is not an execution contract: it cannot be recomputed from,
and it must not be expanded or guessed.  A bundle whose contents are unpinned
is not identified either — file presence plus a `code_sha256` string in
`manifest.json` would still accept a bundle whose CSVs had been edited.

# Independence

P1 and P2 are scientifically independent gates.

- Neither overwrites the other's verdict.
- Each keeps its own status and its own first failing gate.
- The combined verdict is `PREP_P1_P2_PASS` **only** when both pass.
- If either fails, no value is offered as a registration candidate — not even
  the passing gate's observation.
- A failure is never resolved by relaxing a rule.

# P1 — MIT-BIH publisher tree identity

Gates, in order.  Each must pass before the next runs, and the aggregate is
computed **only** after the first three have passed, so a failing tree never
produces a number that could be mistaken for a registration candidate.

1. **`expected_file_set`** — exactly `BJ.mitdb_expected_files()`, which is 147
   names and already contains `SHA256SUMS.txt`.  `missing = 0` and
   `unexpected = 0`, or `P1_MITDB_FILE_SET_MISMATCH`.
2. **`checksum_file_digest`** — the SHA-256 of `SHA256SUMS.txt` itself against
   the value registered in `research/ASSETS.md :: data-mitdb-raw-100`.  On
   failure, `P1_MITDB_CHECKSUM_FILE_MISMATCH`; the publisher list is **not**
   consulted, because nothing verified by a list that is not the registered
   list would count.
3. **`publisher_checksums`** — the publisher list over the other 146 files:
   `checked = 146`, `matched = 146`, no mismatch, no unlisted entry, or
   `P1_MITDB_PUBLISHER_CHECKSUM_MISMATCH`.
4. **`tree_aggregate`** — the 147-file fold, using the frozen
   `(name, bytes, sha256)` canonical-JSON convention and no other.  If the
   observed full digest does not extend the registered prefix `0b46a411`,
   `MITDB_IDENTITY_DIVERGED`.

**"147/147" means 146 + 1.**  A checksum file cannot appear in its own list,
and the frozen verifier explicitly skips it.  Stating that the publisher list
verified all 147 would be false; the contract is 146 publisher-listed files
plus the separately registered digest of the list itself.

# P2 — canonical Q5-D bundle identity

Target: run `20260811T035108_EXP-2026-007_q5d_beat_join_DS1_GATE`, Drive folder
id `1JjwBhU8BXf8lRrYPcM2UjFNdIKxE9Ghd`.

**The bundle is chosen by folder id, never by folder name.**  A folder that
merely has the right name is not evidence, and that substitution is easy to
make and impossible to notice afterwards.  `run_prep()` refuses any folder id
other than the registered one.

Gates, in order:

1. **`folder_id_inventory`** — direct children of the registered folder id,
   read-only, recording file id, name, bytes, modified time, provider checksum
   and trashed state.
2. **`inventory_unambiguous`** — no duplicate name, no subfolder, no shortcut,
   no trashed item, no nameless child, or `P2_INVENTORY_AMBIGUOUS`.
3. **`directory_contract`** — exactly the frozen `BJ.BUNDLE_FILES` twelve, with
   `missing = 0` and `unexpected = 0`, or `P2_DIRECTORY_CONTRACT_FAILED`.
4. **`superseded_absent`** — `SUPERSEDED.json` present is
   `P2_SUPERSEDED_BUNDLE`.
5. **`canonical_bytes_bridge`** — bytes come from the folder id.  Streaming by
   **file id** needs no bridge at all.  A mount may be used only if it can be
   tied to the folder-id inventory by exact name, size and count, plus any
   provider checksum; a matching folder name is never accepted.  Otherwise
   `P2_FOLDER_ID_BRIDGE_UNRESOLVED`.
6. **`manifest_identity`** — `code_sha256` = `6b098c67…` and
   `rule_fingerprint` = `31c4be9f…`, or `P2_MANIFEST_IDENTITY_MISMATCH`.
7. **`input_identity`** — the five files Q5-E reads: individual SHA-256 plus
   the subset fold.

**Two contracts, kept separate.**  The directory contract is the whole
twelve-file bundle; the scientific input identity is the five files Q5-E
actually reads.  The other seven are part of the directory contract and are
**not** unexpected in the input identity — conflating the two previously
rejected every genuine bundle.

QA count agreement is never used as identity evidence.  Files are hashed at
byte level only; parquet is not parsed and no content is aggregated.

# What a run may not do

Open a DS2 per-beat label or a V10 probability, run `detect_r()`, aggregate
M0-M4, re-run the beat join, compute an association or S PR-AUC, train
anything, or modify, move, delete or overwrite any Drive artifact.  Credentials
and local paths never enter a bundle.

# Bundle and identity

A run writes exactly:

`config.json` · `manifest.json` · `source_inventory.json` · `decision.json` ·
`registration_candidates.json` · `oracle_harness_identity.json` ·
`fixture_results.json` · `log.txt` · `summary.md`

The two oracle files belong to P3 and are written with an explicit
`not_applicable` seal rather than a fabricated value, so the payload set stays
complete and nothing pretends a differential happened here.  A synthetic run
additionally writes `SYNTHETIC_FIXTURE.json` and is stamped `ingestable:
false` in the config, the summary and that marker.

**Non-self-referential identity.**  `prep_payload_sha256` folds every payload
file and **excludes `manifest.json`**, which is the file that records it — a
manifest containing its own digest is circular by construction.  The
manifest's own SHA-256 is returned by the writer for freezing **outside** the
bundle, in this document's Decision log and the registration record, and is
deliberately absent from every file inside the bundle.

The bundle is staged, verified against the exact expected file set, and only
then published by rename, so the output path never holds a partial run and no
file sits outside the payload identity.

# Registration

A run produces **candidates**, not registrations.  `registration_candidates.json`
records the observed `MITDB_TREE_AGGREGATE` and the five
`SOURCE_BUNDLE_FILE_SHA256` values with `applied_automatically: false`, and
withholds them entirely unless both gates passed.

Nothing in `mit-bih/q5e_leg2_failure_mechanism_audit.py` or in the Q5-E spec is
edited by a run.  The values enter the codebase only through a **separate
result-acceptance PR** after Codex reviews the run, and both must be written
into the spec and the module together.

# Order

1. Codex implementation acceptance of this PREP
2. user merge judgement
3. separate user **read-only execution** approval
4. P1 + P2 run, bundle preserved
5. Codex result acceptance
6. separate registration PR writes the two values
7. P3 approval, implementation, execution, acceptance
8. only then is a Q5-E execution approval considered

# Decision log

## 2026-08-12 — P1/P2 implemented; never executed

The implementation lands with both gates complete, the Drive access confined to
one read-only adapter seam, and the terminal guard in place.  No registered
asset was opened, no Drive API was called, no digest was computed against real
bytes, and no value was registered.  Every test is synthetic: the publisher
list in the P1 fixture is generated from the fixture's own bytes rather than
copied from the real tree, so no test can pass by memorising a real digest.

The file name `q5e_prep_p1_p2_asset_identity.py` follows the existing
`mit-bih/q5e_*` convention; the notebook follows `notebooks/questNN_*`.  This
document is a separate execution contract rather than a section of the Q5-E
spec because its status, scope and approval boundary are its own — it is an
asset-identity preflight, not part of the frozen diagnostic design.

The manifest self-digest freeze slot is deliberately empty: it is filled in
this Decision log when a real run is accepted, and never from inside a bundle.
