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

The implementation exists (`mit-bih/q5e_prep_p1_p2_asset_identity.py`) and
passed Codex implementation acceptance on 2026-08-12.  The user granted a
separate **read-only execution approval** on 2026-08-12; the terminal stop in
`run_prep()` is now open, and it opens by consulting
`EXECUTION_APPROVAL_RECORD` rather than by having been deleted.  Its position
is unchanged: still after the switch, the token and the folder id, and still
before authentication, the Drive service and every reader.

**A second read-only approval was granted on 2026-08-14**, for a rerun with P2
pointed at the EXP-2026-009 corrective candidate.  It is recorded as its own
entry rather than by editing the first: the two approvals cover **different
folders**, so re-using the earlier record would describe a permission that was
never given.  The superseded 2026-08-12 record is kept in
`PRIOR_EXECUTION_APPROVAL_RECORDS`, because it is what explains why the
20260812 stop bundle exists.  Nothing withheld by the first approval has been
released by the second; the second withholds two further things — overwriting
the 20260812 stop bundle, and promoting the corrective folder to a canonical
Q5-E input.

**One run has completed (2026-08-12) and its bundle exists.**  P1 passed and
produced the full MIT-BIH tree aggregate; P2 stopped at the directory contract.
The bundle is committed and structurally verified — see the Decision log for
the values, the stop and its cause.

This contract is **not** `MEASURED`, `PASS` or `COMPLETE`, and it does not
become so by a run having happened.  The combined verdict is a stop, no value
is eligible for registration, and acceptance was Codex's to give against the
saved notebook output.

**Codex has now given it** (2026-08-12, see the Decision log): the bundle is
`BUNDLE_ACCEPTED_AS_AUTHENTIC_STOP_RECORD`, P1's aggregate is
`P1_OBSERVATION_ACCEPTED` with `REGISTRATION_DEFERRED_UNTIL_COMBINED_PASS`, and
P2's stop is judged `P2_PRODUCER_ARTIFACT_OMISSION` rather than a stale
contract.  An accepted run is not a passed gate: the stop stands, the
twelve-file contract stands, and nothing here is promoted.

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

# P2 — Q5-D bundle identity

**Target (from 2026-08-14):** the EXP-2026-009 corrective candidate, run
`20260813T000000_EXP-2026-009_q5d_null_artifact_repair_corrective`, Drive
folder id `1JzRW_Xdes4Ywp4-VYVvksFFih_RQVbhH`.

**Not the target:** the original canonical run
`20260811T035108_EXP-2026-007_q5d_beat_join_DS1_GATE`, folder id
`1JjwBhU8BXf8lRrYPcM2UjFNdIKxE9Ghd`.  The 2026-08-12 run read it and stopped at
`P2_DIRECTORY_CONTRACT_FAILED` with `missing: ['negative_control_null.npz']`,
judged `P2_PRODUCER_ARTIFACT_OMISSION`.  That folder holds eleven files, it is
immutable, and this rerun does not read it.  `run_prep()` refuses it **by name
and with its own reason**, separately from the generic "not the target"
refusal: re-reading it would reproduce a stop that is already recorded, where a
reader could mistake it for a fresh finding.

**Pointing P2 at the candidate does not register the candidate.**  It is a
*preregistered corrective candidate* — a folder P2 judges.  Q5-E's
`SOURCE_BUNDLE_FOLDER_ID`, `SOURCE_BUNDLE_RUN`, `MITDB_TREE_AGGREGATE` and
`SOURCE_BUNDLE_FILE_SHA256` are imported by the PREP module and left exactly as
they are.  Only a separate registration PR, after a combined PASS **and** a
Codex result acceptance, moves them — and it must move the folder id, the run
name and the five digests **together**, because a bundle identified by one run's
id and another run's digests is identified by neither.

Every P2 result reports the folder actually read, the candidate and the
original canonical folder under **separate keys**
(`folder_id`, `candidate_folder_id`, `original_canonical_folder_id`), plus
`target_is_corrective_candidate`, `target_is_original_canonical` and
`candidate_is_registered_as_canonical: false`.  A single `folder_id` field was
readable as any of the three, and the substitution this preflight exists to
catch is exactly the one where a reader believes a result describes a folder it
does not.

**The bundle is chosen by folder id, never by folder name.**  A folder that
merely has the right name is not evidence, and that substitution is easy to
make and impossible to notice afterwards.  `run_prep()` refuses every folder id
other than the target — including one that differs only in case or by a
trailing space.

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
6. **`manifest_identity`** — read from the schema `BJ.build_manifest()`
   actually writes, or `P2_MANIFEST_IDENTITY_MISMATCH`.

   | field | where it lives | required value |
   |---|---|---|
   | producing code digest | `manifest['code']['sha256']` — **nested**, the mapping `assert_implementation_only()` returns | exactly `6b098c67df3c8e2c8c070b093e6e2d801566f548a3173626745c4a126a97f226` |
   | rule fingerprint | `manifest['rule_fingerprint']` — top level | exactly `31c4be9f44582a68c301fe6cc6572f4db6ff0b3de694af68f6ac6a0f48c2b40e` |
   | freeze fingerprint | `manifest['preflight']['rule_fingerprint']`, when the freeze carries one | equal to the top-level value |

   **The flat `manifest['code_sha256']` this gate used to read has never been
   written by any producer.**  Against the real bundle it resolved to `""`, and
   the gate then failed for a reason that had nothing to do with the bundle.
   The synthetic fixture agreed with it only because the fixture was a
   hand-written flat dict authored from the same belief as the code, so the
   tests could confirm the belief and never test it.  Fixtures are now built by
   `BJ.build_manifest()` itself, and a regression test pins that the old flat
   shape does **not** pass.

   **Exactly one digest is accepted**, not a family of them.  There is no
   raw/LF alternative and no case-insensitive match: a shard and a manifest
   store whatever the producing checkout stored, so accepting a second spelling
   and returning the registered one would hand the caller an identity the
   artifact does not carry.

   A missing, null, wrongly typed or malformed field — including a `code` that
   is a string rather than a mapping, and a freeze fingerprint that disagrees
   with the top-level one — is a **structured problem** carried into
   `P2_MANIFEST_IDENTITY_MISMATCH` with the offending field named.  It is never
   raised.  The reader calls nothing in the frozen module and catches nothing
   at all, so a `RuntimeError` or an `AssertionError` from elsewhere can never
   be relabelled as a manifest defect.  `preflight: null` is the producer's own
   shape when no freeze was supplied and is not a defect: P2 reads identity,
   not the input contract.
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

**One read is the observation.**  A file's authoritative
`(name, bytes, sha256)` is whatever P1's single read produced, and nothing may
revise it.  Explaining *why* a digest differs needs the bytes themselves, and
re-reading is a different moment — on a live tree the file may have changed —
so anything derived from a later read is reported under
`second_read_non_authoritative` and never merged into the observation.  Its
content-derived fields (line endings, BOM, excerpts) appear **only** when the
second read hashes to the same value as the first; when the two disagree, that
instability is the finding and no excerpt is offered, because it would describe
bytes the gate never judged.

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
`source_inventory.json` · `summary.md` · `manifest.json` · `COMMITTED.json`

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

# Publication: a commit marker, not an atomic rename

**The atomic-directory-publication claim is withdrawn.**  An earlier version
staged the bundle elsewhere and published it with `rmdir(directory)` followed
by `rename(staging, directory)`.  Those are two operations, and a directory
that appears at the target between them is *replaced* by POSIX `rename` — the
kernel does this silently as long as the directory is empty, which a regression
test pins as a platform fact.  Claiming the name with `mkdir` closed the
earlier `lexists`-then-rename window but not this one, because the claim was
given back immediately before the rename took it.

Linux offers `renameat2(RENAME_NOREPLACE)`, which genuinely is atomic and
no-replace, and it works on this container's filesystem.  It is **not** used:
the production output path is a Google Drive FUSE mount, where the flag is not
dependable, and a fallback that quietly degrades to plain `rename` would be the
same defect wearing a safer name.

So the directory is written in place and its **completeness** is what is made
indivisible instead:

1. `os.mkdir(directory)` — one operation that either creates the name or
   fails.  It never replaces and never follows: an existing file, empty
   directory, non-empty directory, symlink or junction all raise, and the run
   stops.  A symlinked or reparse-point parent is refused for the same reason.
2. every payload file, then `manifest.json`, written inside the claim — each
   one an **exclusive create** (`O_CREAT | O_EXCL | O_BINARY`), never
   `open(..., "w")`.  Claiming the directory says nothing about the names
   inside it: a writer that got to `config.json` first must keep its bytes,
   and a truncating write would replace them silently and commit on top.
   `O_BINARY` (absent, and therefore 0, on POSIX) is what keeps the file equal
   to the bytes handed in: a Windows text-mode descriptor rewrites every `\n`
   as `\r\n` on the way out, so the digest the writer records — taken from
   what it passed — would describe bytes that never reached the disk, and a
   normal run would fail its own consumer check.  The write loop retries a
   short `os.write`, because a partial write leaves a truncated file that
   still hashes to something, and refuses a write that returns 0 rather than
   spinning forever.
3. `COMMITTED.json` created last, the same way, recording the bundle file set,
   the payload file list and `prep_payload_sha256`.

**A directory without `COMMITTED.json` is not a bundle.**  It is an incomplete
or failed write, and `verify_published_bundle()` refuses it.  This is stronger
than atomic appearance, not weaker: it survives a crash, and it also catches
truncation and post-hoc editing, which a rename never could.

`COMMITTED.json` deliberately does **not** record its own digest or the
manifest's.  The manifest's SHA-256 stays outside the bundle exactly as before
— a digest stored inside the artifact it describes is rewritten by whoever
edits that artifact, so it would look like a freeze record without being one.

**Consumer validation: the marker is checked, not trusted.**  Any reader of a
PREP bundle — including the run itself, immediately after writing, so a run
that cannot validate its own output fails rather than reporting success — must
call `verify_published_bundle(directory, expected_manifest_sha256=...)`.

Taking the file list and the fold *out of the marker* would make the marker
self-certifying: editing a payload file and rewriting the marker's own fold
would produce a bundle that verifies.  So every set and every duplicated field
is checked against the **fixed code contract** and cross-checked between the
two records the run writes:

- the directory's file set equals `bundle_files(synthetic)` — the code
  contract, not the marker's `bundle_files`
- `payload_files` in *both* the marker and the manifest equals
  `payload_files(synthetic)`
- the payload fold is **recomputed** over the contracted payload list and must
  equal the marker's *and* the manifest's recorded value, and those two must
  equal each other
- `experiment_id` and `substage` match the module constants in both records;
  `timestamp` matches between them
- `synthetic_fixture` agrees between the two records and `ingestable` is its
  negation in each.  Which contract applies follows from that agreed flag, so
  relabelling a synthetic bundle as ingestable fails on the file set — the
  synthetic marker file is part of the fixed set for one value and absent from
  it for the other.

**Types are checked, not coerced.**  Every contract flag is written as a real
JSON boolean, and the verifier requires exactly that:

- `committed` must be `True` by identity.  It is the claim the marker exists
  to make, so a marker that says `false`, omits the field, or carries `"true"`
  or `1` is a record of a write that did not finish — and no manifest digest,
  however correct, can make that claim on its behalf.
- `synthetic_fixture` and `ingestable` must each be of type `bool` in both
  records, and `ingestable` must be `not synthetic_fixture`.
- `timestamp` must be a string in both records and identical between them.

Truthiness is not accepted anywhere here, because `bool("false")` is `True`:
under coercion, a value that reads as a denial would have been taken as an
assertion, and the more alarming the value looked the more certainly it would
have passed.  A violation is recorded in `problems` with `structure_ok: false`
and `acceptance_eligible: false` — never raised.

A malformed or truncated `COMMITTED.json` or `manifest.json` is a **finding**,
returned as `ok: false` with a problem list.  It never raises: a parse error
escaping to the caller would turn the thing this verifier exists to detect into
a crash.

**Structure is not acceptance, and a digest is not provenance.**
`manifest.json` is outside the payload fold, so nothing inside the bundle can
vouch for it.  The caller therefore supplies both the digest **and where it
came from**, as `manifest_anchor_source`, drawn from a fixed enum:

| source | meaning | external? |
|---|---|---|
| `same_run_self_check` | the value this run just computed | no |
| `saved_notebook_output` | the saved output of the report cell | **yes** |
| `registered_record` | the value in this Decision log / registration | **yes** |
| `none` | no digest supplied | no |

*Matching* and *being anchored* are different facts and are reported
separately, as `manifest_digest_matches_expected` and
`manifest_anchored_externally`.  A run comparing the manifest against the
digest it computed seconds earlier has confirmed that its own two lines of code
agree — worth doing, and not evidence that the file has not been edited since,
because there is no "since" yet.  Only an external source can make a bundle
`acceptance_eligible`.

An unrecognised, empty or missing source is **refused**, not quietly treated as
external; naming a source without supplying a digest is refused too.  Passing a
string is not provenance.

Accordingly, a run's own immediate self-check returns `structure_ok: true`,
`manifest_digest_matches_expected: true`,
`manifest_anchor_source: same_run_self_check`,
`manifest_anchored_externally: false` and `acceptance_eligible: false` — and
its printed lines say the same thing.  A machine verdict that contradicts its
own prose is worse than either alone.

**Nothing is deleted, ever** — not a pre-existing path, and not the writer's
own directory.  A failed run leaves its partial, uncommitted directory exactly
where it is, at a reported path, because that is where a diagnosis will look
for it.

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

Since 2026-08-14 that registration PR carries a fourth and fifth item, and all
five move **together or not at all**:

1. `MITDB_TREE_AGGREGATE`
2. `SOURCE_BUNDLE_FILE_SHA256` — the five digests
3. `SOURCE_BUNDLE_FOLDER_ID` → the corrective candidate id
4. `SOURCE_BUNDLE_RUN` → the corrective run name
5. `research/ASSETS.md`, recording the candidate's promotion to canonical

A bundle identified by one run's folder id and another run's digests is
identified by neither, so a partial move is worse than none.  Until that PR
merges, the corrective folder is a judged candidate and nothing more, and P3,
M0–M4 and the Q5-E analysis proper stay sealed.

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
- the folder actually read, the corrective candidate and the original canonical
  folder reported under separate keys, with
  `target_is_corrective_candidate: true` and
  `candidate_is_registered_as_canonical: false`
- the exact child set the folder id returned
- every ambiguity category zero: duplicate name, duplicate file id, missing
  file id, nameless, subfolder, shortcut, trashed, Google-native, sizeless
- twelve-file directory contract, `missing = 0`, `unexpected = 0`
- `SUPERSEDED.json` absent
- per-file cross-check: file id, inventory size vs observed size, provider
  sha256 and md5 where available, and the download method used
- `code_sha256` and `rule_fingerprint` both matching the registered values,
  read from `manifest['code']['sha256']` and `manifest['rule_fingerprint']`,
  with the field each value came from recorded in the result
- the five Q5-E input files with name, bytes and SHA-256
- the five-file subset fold
- confirmation that the other seven files are not reported as input-unexpected

**Bundle**

- `COMMITTED.json` present with `committed: true` as a JSON boolean — without
  it the directory is not a bundle and the run is not accepted
- `synthetic_fixture`, `ingestable` booleans and a string `timestamp`,
  agreeing across both records
- the actual file set, equal to the contracted set for that run kind and to the
  set recorded in the marker
- `manifest.payload_files` equal to the fold target actually used
- payload fold recomputes to the recorded `prep_payload_sha256`
- the manifest does not contain its own digest, and neither does the marker
- `verify_published_bundle()` returns `acceptance_eligible: true` when given
  the frozen manifest digest **and** an external
  `manifest_anchor_source` (`saved_notebook_output` or `registered_record`).
  `structure_ok` alone is not sufficient, and neither is a digest whose origin
  is the run itself — the run's own self-check is expected to report
  `acceptance_eligible: false`.
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
- the commit and consumer-validation result: `COMMITTED.json` present,
  `structure_ok`, the recomputed payload fold,
  `manifest_digest_matches_expected`, `manifest_anchor_source`,
  `manifest_anchored_externally`, `acceptance_eligible` with its stated
  reason, and the directory path if the run did not commit
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

## 2026-08-12 — the publish was still test-then-act; atomicity claim withdrawn

Codex was right, and the claim I made in the previous entry was wrong. Claiming
the name with `mkdir` closed the `lexists`-then-rename window, but the publish
then did `rmdir(directory)` and `rename(staging, directory)` — two operations
again, with the claim given back before the rename took it. A regression test
now pins the platform fact that made this unsafe: POSIX `rename` replaces a
pre-existing *empty* directory, so a directory created in that window would
have been destroyed without a trace.

`renameat2(RENAME_NOREPLACE)` was measured and does work on this container's
filesystem, but the production output path is a Drive FUSE mount where the flag
is not dependable, and a silent fallback to plain `rename` would reproduce the
defect under a safer-sounding name. So rather than keep a claim that only holds
on some filesystems, the atomic-directory-publication claim is withdrawn and
the design changed: the bundle is written in place inside the `mkdir` claim and
committed with a `COMMITTED.json` marker created last under `O_CREAT | O_EXCL`.
There is now no rename, no `rmdir`, and no deletion of any kind in the writer —
a test asserts that by AST rather than by comment.

What replaces atomic appearance is a consumer contract, and it is stronger:
`verify_published_bundle()` refuses a directory without the marker, checks the
file set against the committed set, and recomputes the payload fold. It catches
truncation and post-hoc editing, which a rename never could. The run calls it
on its own output before reporting success. The manifest is not in the payload
fold and its digest deliberately stays outside the bundle, so it is anchored by
passing the externally frozen value in — a digest stored inside the artifact it
describes is rewritten by whoever edits that artifact.

Second correction: the publisher-mismatch detail re-read the registered file to
explain the difference, which mixes bytes from a second moment into a finding
about the first. The authoritative `(name, bytes, sha256)` now comes only from
the single read, and the explanatory material sits under
`second_read_non_authoritative` — with its content-derived fields suppressed
entirely when the second read disagrees with the first, since they would
describe bytes no gate ever judged.

Both fixes were checked by reverting them and watching the new tests fail.

## 2026-08-12 — the claim covered the directory but not the files in it

Two more real defects, both measured before being fixed, and both cases of the
same mistake: treating an earlier check as if it covered a later action.

**The directory claim did not extend to the file names inside it.**  Having
`mkdir`ed the directory, the writer filled it with `open(..., "w")`, which
truncates.  A writer that reached `config.json` first had its bytes replaced by
ours and the run committed on top — reproduced with the race hook before the
fix.  Every file the writer produces is now an exclusive create, so whoever got
to a name first keeps it and the run refuses to commit; the write loop also
handles a short `os.write`, which would otherwise leave a truncated file that
still hashes to something. Fixtures cover an intruder creating `config.json`,
`log.txt`, `summary.md`, `manifest.json` and the synthetic marker: each keeps
its bytes and the directory is left with no `COMMITTED.json`.

**The verifier trusted the marker it was verifying.**  It read the payload list
and the fold out of `COMMITTED.json`, so editing `summary.md` and rewriting the
marker's fold produced a bundle that returned `ok: true` with
`manifest_anchored_externally: true` even when the correct manifest digest was
supplied — the manifest was hashed but never parsed, so its own record of the
fold went unread. Now both records are parsed, every set and duplicated field
is checked against the fixed code contract, and the recomputed fold must equal
both recorded folds and they each other. Malformed or truncated JSON returns a
structured verdict instead of raising.

## 2026-08-12 — text-mode newlines, and flags read by truthiness

Two more, both measured. Neither changes any gate, threshold or metric.

**The writer's descriptor was not binary.** `os.open` without `O_BINARY` opens
in text mode on Windows and rewrites every `\n` on the way out, so the file on
disk is not the buffer the caller hashed. The recorded manifest digest would
describe bytes that never existed, and a perfectly good synthetic run would
fail its own consumer check with what looks like corruption. Simulating the
translation reproduces exactly that — `manifest digest … != the externally
frozen …` — and the fix is one flag, which `getattr` makes a no-op on POSIX.
The invariant is now held directly by a test: what `_write_new_file` was handed
and what a reader gets back are byte-identical, across unix newlines, CRLF
already present, a lone carriage return, embedded nulls and high bytes, and an
empty file. A write returning 0 is refused rather than retried, since a silent
hang is worse than a named failure; short writes are still retried to the end.

**The verifier read contract flags by truthiness.** `bool("false")` is `True`,
so a marker whose `synthetic_fixture` said `"false"` was read as saying yes —
the more alarming the value, the more certainly it passed. And `committed` was
never checked at all, so a marker that recorded an unfinished write became
`acceptance_eligible` as soon as a correct manifest digest was supplied. Both
are now checked by identity and by type: `committed is True`,
`synthetic_fixture` and `ingestable` of type `bool` with the latter the
negation of the former, `timestamp` a string and equal across both records.
Violations are problems, not exceptions. Missing, `null`, `0`, `1`, `"true"`
and `"false"` are all covered by fixtures.

## 2026-08-12 — a digest handed over is not a digest held elsewhere

Codex's final review found the machine verdict contradicting the code's own
prose, and it was right. `execute_prep()` passed `verify_published_bundle()`
the digest `write_bundle()` had returned seconds earlier, and the verifier —
seeing *a* digest — reported `manifest_anchored_externally: true` and
`acceptance_eligible: true`, while the very next line printed that the saved
notebook output was still needed. Whichever a reader believed, they were
misled.

The mistake was treating the presence of a digest as provenance. Matching a
value the run computed itself confirms that its own two lines of code agree; it
is not evidence the file has not been edited since, because there is no "since"
yet. So the two facts are now separate — `manifest_digest_matches_expected` and
`manifest_anchored_externally` — and the caller must declare where its value
came from, as one of `same_run_self_check`, `saved_notebook_output`,
`registered_record` or `none`. Only the middle two are external, and only they
can carry `acceptance_eligible`. An unrecognised, empty or missing source is
refused rather than assumed external, and naming a source without a value is
refused too.

The run's own check now reports `acceptance_eligible: false` with
`manifest_anchor_source: same_run_self_check`, which is exactly what its
printed lines say. A regression test asserts the returned dict and the emitted
words agree, because the failure here was not a wrong flag but a disagreement
between two things the same function said.

Related, and worth stating rather than leaving implicit: structural validity is
now reported separately from `acceptance_eligible`. `manifest.json` sits
outside the payload fold, so a bundle whose manifest was never anchored against
the external freeze value cannot be promoted to an acceptance pass, and the
verifier says so in words rather than only in a flag. The run's own call checks
self-consistency against the digest it just computed; the external anchor
remains the saved notebook output.

## 2026-08-12 — separate user read-only execution approval (recorded)

The user granted a **separate read-only execution approval** for EXP-2026-008
Q5-E PREP P1 and P2, distinct from the implementation approval and distinct
from any Q5-E audit approval.

**Approved**

- P1 byte-identity over the registered MIT-BIH publisher tree
  (`research/ASSETS.md :: data-mitdb-raw-100`)
- P2 byte-identity over the canonical Q5-D bundle at the registered folder id
  `1JjwBhU8BXf8lRrYPcM2UjFNdIKxE9Ghd`
- Drive API reads under exactly the `drive.readonly` scope
- writing the P1/P2 result bundle, and saving the notebook with its outputs

**Not approved**

P3 implementation or execution · `detect_r()` · re-running the beat join ·
M0-M4 aggregation · DS2 per-beat labels · V10 probabilities · association or
S PR-AUC · model training or retraining · moving, deleting or overwriting any
Drive file · automatic registration of any observed value.

**What changed in the code.**  One thing.  `_terminal_execution_guard()` used
to raise unconditionally; it now raises unless `EXECUTION_APPROVAL_RECORD`
says the approval was granted, and returns that record when it was.  The
approval is written down rather than implied by a deleted line: an absent
check reads the same whether the approval happened or someone removed an
inconvenience, and a record keeps who approved what, when, and what was
withheld. Setting `granted: False` restores the previous refusal exactly, with
no other edit anywhere — a regression test asserts precisely that.

Everything else is untouched: the gates, their order, the registered folder id,
the digest rules, the 147/147 definition, the fold convention, the publish
contract and the anchor-provenance rules are all unchanged. Authentication
still happens inside `run_prep()` **below** where the stop sits, so the
notebook still calls `run_prep(..., adapter=None)` and holds no credential
logic of its own.

The notebook's two opt-in switches are now on (`APPROVAL =
P.EXECUTION_APPROVAL_TOKEN`, `OPEN_REGISTERED_DATA = True`) and its mount paths
point at the registered asset rather than a blank to be filled in. The module
constant `OPEN_REGISTERED_DATA` stays `False`, so opting in remains something a
call site does explicitly and a stray import still reaches nothing.

**Nothing was executed in this PR.** No authentication was performed, no Drive
API call was made, no registered asset was opened, and no digest was computed
against real bytes. This change makes a run possible; it does not make one
happen, and the three Q5-E stops remain closed.

## 2026-08-12 — first execution attempt: P1 passed, P2 stopped, bundle refused

The first real run under the read-only approval reached both gates and then
failed to write, for a reason that was a defect in this code rather than
anything about the assets.

**What was measured.** Authentication succeeded with the scope proven exactly
read-only. P1 returned `P1_MITDB_IDENTITY_PASS` — the registered MIT-BIH
publisher tree is byte-identical to its registration. P2 returned
`P2_DIRECTORY_CONTRACT_FAILED`: the folder at the registered id did not hold
exactly the twelve contracted files. That is a real stop and is **not** to be
resolved by relaxing the directory contract; which files are missing or
unexpected is recorded by the run, and this attempt lost that detail to the
defect below.

**The defect.** `assert_no_credentials()` scanned the serialised JSON text for
`"credentials"`. The auth audit records `credential_type`, as this contract
requires, and its value in Colab is the class name `Credentials` — so the scan
read a value as a field and refused to write a run that had already completed
both gates. The guard fired on the word rather than the thing, and the cost was
an entire execution.

It now walks the structure and matches **keys** exactly, at any depth,
including inside lists. `credential_type` is accepted; `credentials`,
`access_token`, `authorization` and the rest are refused with the path to the
offending field. Reverting to the text scan, or stopping the walk at lists or
at nested mappings, each fails a test.

Nothing was written to Drive by the failed attempt: the guard runs before the
output directory is created, so no partial bundle exists. The run must be
repeated to capture P2's missing/unexpected lists. No value was registered and
the three Q5-E stops remain closed.

## 2026-08-12 — first completed run: P1 measured, P2 stopped

Run `20260812T123035_EXP-2026-008_q5e_prep_p1_p2_asset_identity`, written to
`MyDrive/MedKOS/ecg-model/runs/`.  Read-only throughout: the credential was
acquired with exactly `https://www.googleapis.com/auth/drive.readonly`,
observed as exactly that one scope, and `exact_readonly_scope_proven` is true.
No Drive file was moved, deleted or overwritten.

**Runtime.**  Colab, Python 3.12.13, Linux-6.6.122+-x86_64-with-glibc2.35,
`google-api-python-client` 2.198.0, `google-auth` 2.49.0, `google-colab` 1.0.0.

### P1 — passed, and the value Q5-E was blocked on now exists

All four gates PASS.  `SHA256SUMS.txt` read exactly once, its own digest equal
to the registered `b61158a9…`; publisher list `checked/matched 146/146`, zero
mismatched, zero unlisted; 147 per-file observations.

    MITDB_TREE_AGGREGATE (observed)
      0b46a411c1882fc5e09e2e60c2613ca441574c78a62f84272ad3ff4a2179ade8

It extends the registered prefix `0b46a411`.  This is the full 64-hex that
`INPUT_IDENTITY_REGISTRATION_REQUIRED` was waiting for.  It is an
**observation, not a registration**: `gate_passed: true` but
`eligible_for_registration: false`, because the combined gate did not open.

### P2 — stopped at `directory_contract`

The registered folder id returned **11 children**, all unambiguous.  The
twelve-file contract reports `missing: ['negative_control_null.npz']`,
`unexpected: []`.  Gates 4-7 were never reached, so `input_identity` is null
and `SOURCE_BUNDLE_FILE_SHA256` was not computed.

**The file was never produced.**  Established from the code, not inferred:
`negative_control_null` appears exactly once in the 4,951-line frozen producer
— inside the `BUNDLE_FILES` tuple — and the module contains **no `savez` call
at all**.  The shard folder carries the producer's code hash `6b098c67df3c`,
which is the frozen module's own SHA-256, so the version that made this bundle
is the version just read.  Two runs on different code hashes each produced the
same eleven files.

**No data is missing.**  `null_summary()` returns `"j_null_max": list(maxima)`
— the complete 10,000-replicate vector, inlined — and the per-family values are
preserved in the 100 shard files.  What is absent is a file, not a measurement.

**Open question for the design owner.**  Two readings fit the evidence and this
document does not choose between them:

1. the contract is stale — the design moved the null distribution into
   `null_summary.json`, making the `.npz` redundant, and `BUNDLE_FILES` was not
   updated; the twelve-file contract should become eleven; or
2. the producer never met its approved spec — EXP-2026-007 lists
   `negative_control_null.npz` under Required outputs, so the bundle is
   genuinely short of what was approved and the producer is what needs fixing.

`BUNDLE_FILES` lives in the **frozen** Q5-D module, whose SHA-256
`6b098c67…` is a registered identity used across Q5-E and embedded in the shard
folder name.  It is not edited here under either reading.  Shrinking the
contract to make P2 pass would be resolving a failure by relaxing a rule, which
this contract forbids.

### Bundle

    prep_payload_sha256               41114110ce08708592e73d096e1c697cb68492de19c6e59f98f082adae7fe0d3
    manifest_sha256_freeze_externally 31f6086962e529cc2184028096fdde3edbdece12dfe959305f724708a3ea0973

`COMMITTED.json` present, `structure_ok: true`, recomputed payload fold equal to
both recorded folds, no problems.  `synthetic_fixture: false`,
`ingestable: true`.  `acceptance_eligible: false` with
`manifest_anchor_source: same_run_self_check` — as designed: the run compared
the manifest against a digest it had just computed, which is self-consistency,
not an external anchor.  Acceptance requires a reviewer to supply the digest
above from the saved notebook output.

The saved report cell did not print `missing`/`unexpected`, so the whole point
of the stop had to be recovered from `decision.json` afterwards.  The cell now
prints them; that gap was in the report, not in the bundle.

### The run record and the template are separate files

Colab pushes an executed notebook over the file it was opened from.  That would
overwrite the unexecuted template, and the two must both exist: the template so
a reader cannot mistake stale output for a result, the executed copy because
its saved output **is** the external freeze record for the manifest digest.

- `notebooks/quest56_q5e_prep_p1_p2_asset_identity.ipynb` — template, always
  committed with zero outputs and null `execution_count`.
- `notebooks/executed/quest56_q5e_prep_p1_p2_asset_identity_<timestamp>.ipynb`
  — the run record, committed **with** its output.

The first record is `…_20260812T123035.ipynb`.  Its output carries both
digests, the P1 aggregate, the P2 stop and the missing filename.  A test
asserts each side of the split.

## 2026-08-12 — Codex result acceptance: the run is accepted, the stop stands

Codex returned its verdict on the completed run.  Four decisions, recorded here
as given.  None of them changes a gate, a threshold, the directory contract, a
null value or a registered identity, and none of them makes this contract
`MEASURED`, `PASS` or `COMPLETE`.

### D1 — P1: the observation is accepted, registration is deferred

The full aggregate

    MITDB_TREE_AGGREGATE (observed, accepted as an observation)
      0b46a411c1882fc5e09e2e60c2613ca441574c78a62f84272ad3ff4a2179ade8

is **accepted as a valid observation**.  It is *not* written into the
`MITDB_TREE_AGGREGATE` constant, because the preregistered combined gate
permits registration only when P1 **and** P2 pass, and P2 stopped.

    P1_OBSERVATION_ACCEPTED
    REGISTRATION_DEFERRED_UNTIL_COMBINED_PASS

This is what the *Independence* section prescribes rather than an exception to
it: the passing gate's observation is reported, its eligibility is withheld.
`INPUT_IDENTITY_REGISTRATION_REQUIRED` therefore remains closed, and the value
above stays a candidate carrying `applied_automatically: false`.

### D2 — P2: `P2_PRODUCER_ARTIFACT_OMISSION`

`P2_DIRECTORY_CONTRACT_FAILED` is **not** grounds for correcting the contract.
Of the two readings the result handoff put to the design owner, the first — a
stale contract — is rejected and the second is adopted.

`negative_control_null.npz` is registered in **both** places that define the
bundle:

- EXP-2026-007 *Required outputs*
  (`experiments/specs/EXP-2026-007-q5d-order-preserving-beat-join-gate.md`,
  under "Future Drive run directory"); and
- `BUNDLE_FILES` in `mit-bih/q5d_order_preserving_beat_join.py`.

No approved Decision log entry removed it from either.  The twelve-file
directory contract is therefore **not** reduced to eleven.

    P2_PRODUCER_ARTIFACT_OMISSION

The defect is in the producer's **output packaging**.  It is not a failed
scientific computation and not a loss of null values: `null_summary()` inlines
the complete 10,000-replicate `j_null_max` vector, and the per-family values
are preserved in the 100 shards.  What was never written is a file.

### D3 — Recovery: deterministic reconstruction, never a re-run

The EXP-2026-007 beat join and the 10,000 × 3 null are **not** re-run.  The
adopted direction is to reconstruct `negative_control_null.npz` deterministically
from the existing 100 validated shards through the **frozen**
`finalize_null_shards()` path.

- The existing Drive bundle and the existing null shards are not modified, not
  deleted and not overwritten.
- A **new corrective bundle folder** is created.  The existing eleven files are
  copied **byte-identically** into it, and the reconstructed NPZ is added, so the
  folder holds exactly the twelve `BUNDLE_FILES` names.
- Nothing outside `BUNDLE_FILES` is placed in the corrective folder.
- The corrective provenance is recorded in this repository's Decision log and in
  `research/ASSETS.md` / `research/PROJECT_STATE.md`.

**The NPZ contract is fixed in a specification before any implementation**, so
that a serialisation cannot be chosen after seeing which one verifies:

- `wrong_record`: float64, shape `(10000,)`
- `order_shuffle`: float64, shape `(10000,)`
- `circular_shift`: float64, shape `(10000,)`
- `j_null_max`: float64, shape `(10000,)`
- readable with `allow_pickle=False`
- every value finite
- for every replicate `b`, `j_null_max[b]` **exactly equal** to the maximum of
  the three families at `b`
- exactly equal to the `j_null_max` already recorded in the existing
  `null_summary.json`
- the existing 100 shards verified for identity, digest, `code_sha256`,
  `rule_fingerprint`, `input_digest`, replicate coverage `0..9999`, and no
  overlap and no gap

If any one of these fails, the repair stops with `REPAIR_INPUT_UNQUALIFIED` and
publishes neither the NPZ nor a new bundle.  Several schemas or serialisations
are **not** produced so that one can be picked afterwards.

### D4 — This run's bundle: an authentic stop record

Recomputed from the actual Drive bytes:

    manifest SHA-256  31f6086962e529cc2184028096fdde3edbdece12dfe959305f724708a3ea0973
    payload fold      41114110ce08708592e73d096e1c697cb68492de19c6e59f98f082adae7fe0d3

Both equal the external freeze values printed in the saved executed notebook
`notebooks/executed/quest56_q5e_prep_p1_p2_asset_identity_20260812T123035.ipynb`,
which is the external anchor this contract requires — not the run's own
self-check.

    BUNDLE_ACCEPTED_AS_AUTHENTIC_STOP_RECORD

The bundle is accepted as a faithful record of what happened.  **The combined
verdict is still a P2 stop**, so nothing is promoted to `PREP_P1_P2_PASS` and
nothing becomes registration eligible.  Accepting a stop record and passing a
gate are different claims and are not conflated here.

### What this entry does not do

It does not edit `BUNDLE_FILES`, the frozen Q5-D module or its SHA-256; it does
not touch a null value, a gate, a threshold or a decision; it does not register
the P1 aggregate or any `SOURCE_BUNDLE_FILE_SHA256`; it does not create,
copy or read a Drive folder; it does not reconstruct an NPZ; and it does not
raise this contract's `status`, which stays `approved_for_implementation`.

### Position in the Order

Step 5 (Codex result acceptance) is complete, with the outcome *accepted run,
upheld stop*.  Step 6 (the registration PR) does **not** follow from it: it
waits on a combined pass, which waits in turn on the corrective bundle and on a
separate user approval to execute the repair.

## 2026-08-14 — rerun enable: the corrective candidate becomes P2's target

The corrective bundle exists (EXP-2026-009, `REPAIR_COMPLETE`, 2026-08-13), and
the user granted a second **read-only execution approval** for a P1/P2 rerun
against it.  This entry records the code change that makes such a run possible,
and its boundaries.  **No run has happened under it.**

### D5 — `P2_TARGET_REPOINTED_TO_CORRECTIVE_CANDIDATE`

`run_prep()` now accepts exactly `1JzRW_Xdes4Ywp4-VYVvksFFih_RQVbhH`
(`20260813T000000_EXP-2026-009_q5d_null_artifact_repair_corrective`) and
refuses everything else — including a case-folded or space-padded spelling of
the target itself.

The **original canonical folder id is refused separately, by name, with its own
reason**.  It is not a stray id: it is the eleven-file folder whose stop is
already recorded, and a generic "not the target" message would have said the
same words for a typo and for the one folder a reader might most plausibly
re-point at.  Both refusals happen before the terminal guard, so neither is
reachable by flipping the approval record.

### D6 — `CANDIDATE_IS_NOT_A_REGISTRATION`

Q5-E's `SOURCE_BUNDLE_FOLDER_ID`, `SOURCE_BUNDLE_RUN`, `MITDB_TREE_AGGREGATE`
and `SOURCE_BUNDLE_FILE_SHA256` are **unchanged**.  The corrective folder id
appears nowhere in `q5e_leg2_failure_mechanism_audit.py`, and a regression test
asserts that.  Every P2 result reports the candidate and the original under
separate keys with `candidate_is_registered_as_canonical: false`.

Promotion is a separate PR after a combined PASS and a Codex result acceptance,
and it moves the folder id, the run name and the five digests **together**.

### D7 — `MANIFEST_SCHEMA_CORRECTED_TO_THE_PRODUCER`

Gate 6 read a flat `manifest['code_sha256']`.  No producer has ever written
that key.  `BJ.build_manifest()` nests the digest at `manifest['code']['sha256']`
— `code` being the mapping `assert_implementation_only()` returns — and puts
the fingerprint at the top level.

**Why the tests did not catch it.**  The synthetic fixture was a hand-written
flat dict, authored from the same belief as the gate.  A suite built that way
can only confirm the belief; it cannot test it.  The fixture is now produced by
`BJ.build_manifest()` itself, with the digest pinned to the registered LF
identity so a CRLF checkout cannot make the fixture impersonate the machine
running it, and a regression test pins that the old flat shape **stops**.

The match is exact — one digest, no raw/LF alternative, no case folding.
Malformed, missing, null and wrongly typed fields become structured problems
under `P2_MANIFEST_IDENTITY_MISMATCH` with the field named; the reader calls
nothing in the frozen module and catches nothing at all, so no `RuntimeError`
or `AssertionError` can be relabelled as a manifest defect.

### D8 — `RERUN_APPROVAL_RECORDED_SEPARATELY`

The 2026-08-14 approval is a new record, not an edit of the 2026-08-12 one.
The two cover different folders, and a record rewritten in place records only
the latest thing.  `NOT_APPROVED` is written once and shared, so the two
records cannot drift into a boundary that looks like it moved when nobody moved
it.  The new record withholds two further things: overwriting the 20260812 stop
bundle, and promoting the corrective folder to a canonical input.

`OPEN_REGISTERED_DATA` remains `False` at module level.  Authentication and
Drive-adapter construction remain below the terminal guard; the scope must
still be exactly `drive.readonly`.

### What this entry does not do

It does not run anything, authenticate, call the Drive API, create a folder or
write a bundle.  It does not modify `q5d_order_preserving_beat_join.py`, the
twelve-file contract, a null value, a family, a seed, a replicate count, a
gate, a threshold or a decision rule.  It does not overwrite the 20260812 stop
bundle or its executed notebook, and it does not touch the original eleven-file
Drive folder or the null shards.  It registers no value, and it does not raise
this contract's `status`, which stays `approved_for_implementation`.

### Position in the Order

Step 4 is re-entered with a new target: a P1+P2 run against the corrective
candidate, bundle preserved at a **new timestamp** — the 20260812 bundle is not
overwritten.  Step 5 (Codex result acceptance) and step 6 (the registration PR,
now carrying five items) follow only from that run's outcome.  Steps 7 and 8 —
P3 and any Q5-E execution approval — remain sealed.

## 2026-08-14 — result accepted, and the values registered by a separate PR

The rerun ran once from merged `main`, against the corrective candidate.

    P1       P1_MITDB_IDENTITY_PASS            first_failure null
    P2       P2_SOURCE_BUNDLE_IDENTITY_PASS    first_failure null
    combined PREP_P1_P2_PASS

Run `20260814T104835_EXP-2026-008_q5e_prep_p1_p2_asset_identity`, Drive folder
id `1805OG3ovOf3TJU_0xmzGIR9Nz51qrn2L`.  The 20260812 stop bundle was not
overwritten; it stands at folder id `1yKw7zH4ElQFVcIx0ckFRDxNZVREQcZMU`, a gap
this entry also closes — that run's row previously said "folder id 미기록", and
its **STOP verdict is unchanged**.

### Codex result acceptance

    PREP_P1_P2_RESULT_ACCEPTED
    CORRECTIVE_PROMOTION_APPROVED

**The external anchor was verified by Codex, not by the run.**  This is the
distinction the contract has insisted on throughout, and it was honoured:
Codex re-fetched the Drive bundle read-only and called

    verify_published_bundle(
        <bundle>,
        expected_manifest_sha256=
            "f23d90180cbc43f5805c8c04216bfdd2f3479a6fe9af655a884cfd17b8446f9e",
        manifest_anchor_source=saved_notebook_output)

obtaining `structure_ok: true`, `manifest_digest_matches_expected: true`,
`manifest_anchored_externally: true`, `acceptance_eligible: true`,
`problems: []`, `prep_payload_sha256:
4b77dbeed73124d56914e5cba99de94a370f59ba9020d908b642a85b83ed5ee7`.

The run's own self-check reported `acceptance_eligible: false` under
`same_run_self_check`, exactly as designed.  A run comparing a digest against
the value it computed seconds earlier has confirmed its own arithmetic, not
that the file has not been edited since — and the two verdicts differing is
the mechanism working, not a contradiction.

### What was registered, and where

Four categories, moved **together** by a separate registration PR into
`mit-bih/q5e_leg2_failure_mechanism_audit.py`:

| category | value |
|---|---|
| `MITDB_TREE_AGGREGATE` | `0b46a411c1882fc5e09e2e60c2613ca441574c78a62f84272ad3ff4a2179ade8` |
| `SOURCE_BUNDLE_FOLDER_ID` | `1JzRW_Xdes4Ywp4-VYVvksFFih_RQVbhH` |
| `SOURCE_BUNDLE_RUN` | `20260813T000000_EXP-2026-009_q5d_null_artifact_repair_corrective` |
| `SOURCE_BUNDLE_FILE_SHA256` | the five below |

    decision.json                d464a4059e6cad39de1018b3eaecb0b7713c9fd0839fbed94ffa4be2b2d7e8e5
    join_map.parquet             dad93d340f2ca0db30b4c8c77e13f847e612b342b1e31c47a1b411fa8fd62971
    manifest.json                4bd7b4d8bb2ce9a3461b85ecdf65761ce1ad625bd6c6adc1d39c6c12029fbb4c
    record_class_coverage.csv    e786c203ffe23c67ba7d412c64703813b5cb22ecbe7d17f53679ee94d982ccec
    unmatched_and_ambiguous.csv  b6134468493b32fa5b56cfff9c35aee4d4059d6d8f321c6678a06acdf250459f

`SOURCE_BUNDLE_RUN` names the **corrective bundle**, not the PREP run.  The
PREP run measured these values; the corrective bundle supplies the inputs.
Writing `20260814T104835…` there would name the measuring instrument as the
material.

`p1_p2_registration_state()` refuses any partial fill: a bundle identified by
one run's folder id and another run's digests is identified by neither, and the
half-registered state is worse than the unregistered one because both gates
would report a pass built on a mismatch nobody looked for.

### Audit values that are deliberately **not** registered as constants

| value | where it lives | why not a constant |
|---|---|---|
| five-file subset fold `2c98aebb…` | `research/ASSETS.md` | derivable from the five registered digests; a second copy could drift |
| twelve-file full fold `4c9c9cec…` | `research/ASSETS.md` | provenance/audit identity of the *whole* bundle.  Q5-E reads five files; a gate over the other seven would fail a bundle for a reason the science does not depend on |
| `prep_payload_sha256` `4b77dbee…` | `research/ASSETS.md` | identity of the PREP bundle, not of any Q5-E input |
| PREP manifest freeze `f23d9018…` | `research/ASSETS.md`, this log | the acceptance anchor, not a science gate |

None of these appears in `q5e_leg2_failure_mechanism_audit.py`, and a
regression test asserts their absence there and their presence in `ASSETS.md`.

### Corrective provenance — the statement that must survive

The registered bundle is a **corrective packaging-derived canonical Q5-E
input**.  Precisely:

- The eleven files other than `negative_control_null.npz` are **byte-identical
  copies** of what the original EXP-2026-007 run produced.
- `negative_control_null.npz` is **not** a file that run wrote.  The original
  producer never wrote it — `P2_PRODUCER_ARTIFACT_OMISSION` — and it was
  reconstructed a day later by `q5d_null_artifact_repair.py` from the 100
  preregistered null shards.
- Replicate coverage exactly `10000/10000`, no gap, no overlap.
- The reconstructed `j_null_max` is **element-wise identical** to the vector
  already in `null_summary.json` — two vectors written by different code paths
  in the original run, so their agreement is evidence rather than
  self-confirmation.
- No scientific rule, null value, seed, family or replicate count changed.
  This is a deterministic repackaging of a missing artifact.

**It must never be written that the original EXP-2026-007 run produced a
twelve-file bundle.**  It did not.

### What this entry does not do

It does not run anything, authenticate, call the Drive API or write a bundle.
It does not modify `q5d_order_preserving_beat_join.py`, any scientific gate,
threshold, hypothesis or multiplicity correction.  It does not touch the
template notebook, the executed records, the Drive bundles, the original
eleven-file folder or the null shards.  It does not raise this contract's
`status`, which stays `approved_for_implementation`, and it does not promote
Q5-E to `approved_for_execution`, `RUNNING`, `MEASURED` or `COMPLETE`.

### Position in the Order

Steps 5 (Codex result acceptance) and 6 (the registration PR) are complete.
Step 7 — P3 approval, implementation, execution and acceptance — is **not**
changed by this: registering P1 and P2 did not alter P3's conditions, and
`SOURCE_MATCH_ORACLE_RECORD` is still `None`, so `verify_source_match_equivalence()`
still stops M4 before the detector replay is reached.  Step 8, a Q5-E execution
approval, remains after that.
