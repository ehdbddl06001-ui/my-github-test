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
- If either fails, nothing becomes eligible for registration.  The passing
  gate's **observation is still reported** — erasing measured evidence makes a
  run harder to diagnose, not safer — but its
  `eligible_for_registration` is false.
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

**One read of `SHA256SUMS.txt`, not two.**  Gate 2's digest and gate 3's parsed
list come from the *same* byte snapshot.  Verifying the file through one read
and then re-opening the registered path to parse it leaves a window in which
the file changes between the two — the run would then verify one state and act
on another, which makes the verification decorative.  Gate 3 therefore never
re-opens the path; the list is parsed from the verified bytes by a PREP-local
parser held to `BJ.parse_sha256sums`'s conventions (whitespace forms, blank and
comment lines, `*name`, `./name`, nested paths kept whole, 64-character digests
only, lowercased) by differential tests over the same inputs.  The frozen
module is not modified.
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
   **file id** needs no bridge at all.  Either way the fetched bytes are
   re-checked against the inventory: length always, `sha256Checksum` when the
   provider supplies one, `md5Checksum` when it supplies one — and both when
   both exist. A checksum the provider did not supply is recorded as
   unavailable, never guessed, and its absence alone does not fail a direct
   stream, because the file id already ties the bytes to the folder. MD5 is a
   provider **transfer cross-check**, not a security identity. A mount is
   accepted only when tied to the inventory by exact name, size and every
   available provider checksum; a matching folder name is never accepted.  Otherwise
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

# Preserved observations

A gate that fails after doing work keeps what it measured.  Blanking it would
destroy the only evidence that explains the failure, and it protects nothing:
what has to be withheld is *eligibility*, not the observation.

- A `P1_MITDB_PUBLISHER_CHECKSUM_MISMATCH` keeps all 147 per-file
  `(name, bytes, sha256)` observations and the mismatched/unlisted detail, with
  `tree_aggregate: null`, `gate_passed: false`,
  `eligible_for_registration: false`, `observation_only: true` and
  `blocked_by: P1_MITDB_PUBLISHER_CHECKSUM_MISMATCH`.  The aggregate is
  withheld because folding an unverified tree produces a number indistinguishable
  in form from a registration candidate.
- A gate that stops before anything is hashed reports an empty `per_file`,
  because nothing was measured.  An empty observation and a withheld one are
  different claims and are not conflated.
- A P2 failure after `canonical_bytes_bridge` keeps the bridge and its per-file
  cross-checks, with `input_identity: null` — that gate was never reached.

# Authentication and scope

Authentication is part of the guarded route, not of the notebook.  A notebook
cell that built an adapter would mint a credential the terminal guard never
saw, which is the guard defeated by convenience.  `run_prep()` therefore runs
in exactly this order, and the notebook calls it with `adapter=None`:

1. `OPEN_REGISTERED_DATA` switch
2. PREP execution approval token
3. registered folder id
4. **terminal execution guard**  ← the one line an execution-approval PR removes
5. runtime dependency check
6. credential acquisition and read-only scope proof
7. Drive v3 service and adapter construction
8. P1/P2 readers and Drive API calls

The credential is requested with exactly
`https://www.googleapis.com/auth/drive.readonly` and is passed explicitly to
the client; the adapter never constructs a default client, because a default
client silently adopts an ambient credential whose scope nobody checked.  The
run records a machine-readable audit — `requested_scopes`, `observed_scopes`,
`exact_readonly_scope_proven`, `credential_type`, `service_api`/`service_version`,
`no_write_adapter_methods` — and never a token, credential or authorization
header.

A credential whose scopes cannot be observed, or which carries anything beyond
the read-only scope, stops the run with `P2_READONLY_SCOPE_UNPROVEN`.  A
broader credential is **not** accepted merely because it includes the scope we
need: "read-only" would then be a claim the code cannot support.  Having no
write method on the adapter bounds the *adapter*, not the credential, and is
reported separately rather than offered as the proof.  If the platform cannot
produce an exactly read-only credential, that is reported and production
execution is blocked rather than described loosely.

# Runtime identity

Each bundle's `config.json` and `manifest.json` record the environment the run
happened in: Python version, platform, the `google-auth`,
`google-api-python-client` and `google-colab` versions, the requested Drive
scope and whether it was proven, and the SHA-256 of the PREP module, the Q5-E
module and the frozen Q5-D module.  A digest is only as interpretable as the
run that produced it, and this cannot be reconstructed afterwards.

Nothing is installed or upgraded to make the record tidier: a version that
cannot be determined is written as `unavailable`, never as `latest` and never
guessed.  No credential, token or local path is recorded.

# What a run may not do

Open a DS2 per-beat label or a V10 probability, run `detect_r()`, aggregate
M0-M4, re-run the beat join, compute an association or S PR-AUC, train
anything, or modify, move, delete or overwrite any Drive artifact.  Credentials
and local paths never enter a bundle.

# Bundle and identity

A production run writes exactly:

`config.json` · `decision.json` · `log.txt` · `registration_candidates.json` ·
`source_inventory.json` · `summary.md` · `manifest.json`

The payload set is **P1/P2-specific** (`P1_P2_PREP_PAYLOAD_FILES`) and is not
inherited from P3's list: the oracle harness and fixture-result files belong to
the differential and have no business in an asset-identity bundle, not even as
sealed placeholders.  Only the fold algorithm and the canonical-JSON
convention are shared with Q5-E.

A synthetic run additionally writes `SYNTHETIC_FIXTURE.json`, and that marker
is **inside** the payload fold — deleting or editing it breaks the recomputed
digest, which is what "no file outside the payload identity" has to mean.
`manifest.payload_files` records the actual fold target for the run's kind, so
a reader never has to guess which set was folded.

**Non-self-referential identity.**  `prep_payload_sha256` folds every payload
file and **excludes `manifest.json`**, which is the file that records it — a
manifest containing its own digest is circular by construction.  The
manifest's own SHA-256 is returned by the writer for freezing **outside** the
bundle and is deliberately absent from every file inside it.  The primary
external record is the saved notebook output of the final report cell, which
prints the full 64-hex value together with `prep_payload_sha256`; the result
acceptance PR copies both into this document's Decision log and the
registration record.  No sidecar file is introduced — an extra artifact would
need its own location, atomicity and identity contract before it could carry
evidence.

The bundle is staged in a directory unique to the call, verified against the
exact expected file set, and only then published by a same-parent rename, so
the output path never holds a partial run.  **Nothing pre-existing is
deleted**: an existing final path is refused rather than removed, no earlier
staging directory is cleaned up, and a failed run's partial staging is
preserved at a reported `.failed` path rather than discarded — a diagnosis is
worth more than a tidy directory.

The final path is **claimed** with a single `mkdir` before any staging work,
rather than tested with `lexists` and renamed onto much later.  POSIX `rename`
replaces an empty directory, so the test-then-act form could destroy a
directory that appeared in the window between the two; `mkdir` is atomic and
fails if anything at all is at the path — a file, an empty directory, a
non-empty directory, a symlink or a junction — so from the claim onward the
name is ours.  Publishing releases that claim with `rmdir`, which removes only
an empty directory and therefore only ever the writer's own claim; if anything
found its way inside, the run refuses to publish and preserves its staging
instead.  A symlinked or reparse-point parent is refused outright, because
writing through a link lands somewhere other than where the path says.

# Registration

A run produces **candidates**, not registrations.  `registration_candidates.json`
records the observed `MITDB_TREE_AGGREGATE` and the five
`SOURCE_BUNDLE_FILE_SHA256` values with `applied_automatically: false`.

**Observations are preserved; only eligibility is withheld.**  When one gate
fails, the other gate's measurement is still reported — erasing it would
destroy audit evidence and make the run harder to diagnose, not safer.  Each
entry carries `observed`, its own `gate_passed`, the shared
`combined_registration_allowed`, and `eligible_for_registration`, which is true
only when both hold.  A value that was never computed, because its gate stopped
earlier, stays `None` because there is nothing to report.  The aggregate
preserved on `MITDB_IDENTITY_DIVERGED` is marked `observation_only` — a
diagnostic observation from a failed gate, explicitly not a candidate.

Nothing in `mit-bih/q5e_leg2_failure_mechanism_audit.py` or in the Q5-E spec is
edited by a run.  The values enter the codebase only through a **separate
result-acceptance PR** after Codex reviews the run, and both must be written
into the spec and the module together.

# Result acceptance criteria

Fixed **before** any measurement exists, so a result review cannot be argued
into a looser standard afterwards.  A run is accepted only when every item
below is present and correct in the bundle.

**P1**

- gate order as emitted, matching `P1_GATE_ORDER`
- expected file count 147, `missing = 0`, `unexpected = 0`
- `SHA256SUMS.txt` self digest equal to the registered value
- publisher `checked = 146`, `matched = 146`
- `mismatch = 0`, `unlisted = 0`
- full aggregate present, 64-hex, prefix matching `0b46a411`
- a **call audit** showing the aggregate was computed only after gates 1–3
  passed, and that a checksum-file failure would have read no other file

**P2**

- evidence of a direct **folder id** query, not a name search
- the exact child set the folder id returned
- every ambiguity category zero: duplicate name, duplicate file id, missing
  file id, nameless, subfolder, shortcut, trashed, Google-native, sizeless
- twelve-file directory contract, `missing = 0`, `unexpected = 0`
- `SUPERSEDED.json` absent
- per-file cross-check: file id, inventory size vs observed size, provider
  sha256 and md5 where available, and the download method used
- `code_sha256` and `rule_fingerprint` both matching the registered values
- the five Q5-E input files with name, bytes and SHA-256
- the five-file subset fold
- confirmation that the other seven files are not reported as input-unexpected

**Bundle**

- the actual file set, equal to the contracted set for that run kind
- `manifest.payload_files` equal to the fold target actually used
- payload fold recomputes to the recorded `prep_payload_sha256`
- the manifest does not contain its own digest
- the manifest's SHA-256 present in the notebook output or ingest log as the
  external freeze record
- `synthetic_fixture: false` and `ingestable: true` for a production run
- no credential field and no local path anywhere in the bundle
- P1 and P2 verdicts and `first_failure` values recorded independently
- observations preserved even where the other gate failed
- `eligible_for_registration` per candidate, and `applied_automatically: false`
- `config.runtime` present with a real Python version, platform, and a version
  or the literal `unavailable` for each recorded distribution — never `latest`
- `config.drive_authentication.exact_readonly_scope_proven` true for a
  production run, with `observed_scopes` equal to the single read-only scope
- no token, credential or authorization field anywhere in the bundle

**Notebook output** (the saved report cell, which is also the external freeze
record):

- P1 and P2 status and `first_failure`
- a per-gate PASS / STOP table for both legs, with unreached gates shown as
  unreached rather than as passes
- P1's 146 + 1 result, spelled out
- P2's inventory method (folder id, not name search) and bridge method
- the scope proof result
- provider checksum availability and match per file
- preserved observations, `gate_passed`, `eligible_for_registration` and
  `blocked_by`
- the full 64-hex `prep_payload_sha256` and `manifest_sha256_freeze_externally`
- the `.failed` staging path if the publish did not complete
- the next action

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

## 2026-08-12 — second acceptance round: guard, scope, snapshot, observations

Five corrections, all to the implementation and none to the science.  The
scientific question, split, metrics and stopping conditions are unchanged.

**The notebook was authenticating above the guard.**  Cell 5 built the Drive
adapter itself and handed it to `run_prep()`, so a credential was minted before
the terminal guard was ever reached — the guard was intact and irrelevant.
Authentication now lives inside `run_prep()`, below the guard; the notebook
passes `adapter=None` and its preflight cell reports the folder id, the
dependency list and the scope contract while making zero auth, service and API
calls.  A spy test makes every one of those seams raise if touched, and runs
the approved route with the guard alive to show the count really is zero rather
than "refused".

**The read-only scope was declared but not applied.**  A constant nobody passes
to a call proves nothing.  The credential is now acquired explicitly, requested
with exactly the read-only scope, audited, and passed to the client; anything
short of exactly that scope stops with `P2_READONLY_SCOPE_UNPROVEN`, including
a broader credential that happens to include it.  The production adapter no
longer builds a default client, which was the remaining path to an unaudited
ambient credential.

**`SHA256SUMS.txt` was read twice.**  Gate 2 hashed it and gate 3 re-opened it
through the frozen verifier, so a file swapped in between would be verified in
one state and parsed in another.  Both steps now work from one byte snapshot,
with a PREP-local parser held to the frozen parser's conventions by
differential tests across eighteen list dialects.  A reader that rewrites the
file the moment it has been read leaves the verdict unchanged; before the fix
the same fixture changed which list the 146 files were checked against.

**Failing gates were discarding what they had measured.**  A publisher-checksum
failure now keeps all 147 per-file digests and the mismatch detail with the
aggregate withheld, and a P2 manifest failure keeps the bridge cross-checks
with `input_identity` null.  This is the same principle already applied to the
passing leg's observation: withhold eligibility, never evidence.

**The runtime was unrecorded.**  Interpreter, platform, client library
versions, requested scope and the three module digests now go into
`config.json` and `manifest.json`.  Nothing is installed to fill a gap — an
undeterminable version is written as `unavailable`.

Also hardened, following the same reasoning as the earlier publish work: the
final path is claimed atomically with `mkdir` instead of being tested and
renamed onto later, and symlink and reparse-point targets and parents are
refused.  Every one of these fixes was checked by reverting it and watching the
new test fail.

Still true, and still deliberately so: nothing has been executed, no registered
asset has been opened, no digest computed against real bytes, no value
registered, and the terminal guard is untouched.
