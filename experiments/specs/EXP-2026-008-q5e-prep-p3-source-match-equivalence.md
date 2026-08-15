---
experiment_id: EXP-2026-008
substage: Q5E_PREP_P3_SOURCE_MATCH_EQUIVALENCE
title: Q5-E PREP P3 source-match equivalence differential
status: approved_for_implementation
design_owner: codex
implementation_owner: claude
analysis_only: true
training_required: false
dataset: none_synthetic_fixtures_only
split: none_no_record_is_opened
parent_experiment: EXP-2026-008
parent_spec: experiments/specs/EXP-2026-008-q5e-leg2-failure-mechanism-audit.md
sibling_spec: experiments/specs/EXP-2026-008-q5e-prep-p1-p2-execution-contract.md
primary_metric: none_source_equivalence_only
parent_primary_metric: none_diagnostic_association_only
created: 2026-08-14
---

# Status boundary

Five states are separated here on purpose, because collapsing any two of them
would turn a piece of code into a claim it has not earned:

- **implementation approved and accepted** — the user approved the design and
  the implementation on 2026-08-14; Codex returned `P3_IMPLEMENTATION_ACCEPTED`
  at commit `40b1642` on 2026-08-15, and PR #140 merged as `e35e733`.
- **execution approved, read-only** — on 2026-08-15 the user granted a
  separate approval to read the registered `data.py` by file id under exactly
  `drive.readonly`, run the six registered fixtures under injection, and write
  the PREP bundle.  It approves nothing else; the list in `NOT_APPROVED` is
  what it withholds.
- **result not run** — the differential has still never been executed against
  the registered source.  There is no measured outcome anywhere in this
  repository, and none may be inferred from the fact that the code exists or
  that execution is now permitted.
- **`SOURCE_MATCH_ORACLE_RECORD` registration not approved** — a PASS, if one
  is ever measured, does not register itself.  Registration is a separate PR
  after Codex accepts the run.
- **Q5-E scientific execution not approved** — P3 is one of three preflights.
  Completing it approves nothing about the audit itself.

No statement below may be read as `P3_PASS`,
`SOURCE_MATCH_EQUIVALENT_TO_REGISTERED_SOURCE`, a measured result, or an
approval to register anything.  The state after the execution-enable change is
**`P3_EXECUTION_APPROVED_NOT_YET_RUN`**: the route is open, and it has not been
walked.

`status:` in the frontmatter stays `approved_for_implementation`.  It moves
only when a measured result has been accepted, exactly as it did for P1/P2 —
an execution approval is permission to run, not an outcome.

# Why P3 exists

`Q5E.match_peaks_to_annotations()` is a **candidate** adapter written from
prose: "greedy nearest with a `used` set", plus a tolerance, an AAMI selection
and a boundary cut.  That prose admits several inequivalent implementations,
and the fourth Codex review made the consequence a terminal gate — the adapter
is what M4's replay counts are produced *through*, so
`verify_source_match_equivalence()` stops M4 before the detector runs while
`SOURCE_MATCH_ORACLE_RECORD is None`.

Two things this PREP is explicitly **not** allowed to treat as evidence:

- **Reproducing 22/22 per-record counts is not a proof of equivalence**, and
  may not be used to choose between candidate implementations.  Counts are a
  necessary condition; two different matching rules can produce the same
  count with different rows.
- **A second reimplementation is not an oracle.**  Transcribing the same prose
  twice can reproduce the same misreading twice, and the agreement would be an
  artefact of one reader rather than evidence about the source.

# Design

## The oracle is the registered source, executed

`mit-bih/q5e_prep_p3_source_match_equivalence.py` loads the digest-verified
registered `data.py` into an isolated namespace and calls its `build_record`
under synthetic dependency injection:

| injected | stands in for | what it returns |
|---|---|---|
| `sig`, `ann_sample`, `ann_symbol` **as arguments** | the caller's reading | the fixture's ramp signal and its annotations, in the fixture's own order — the registered `build_record` is handed its inputs rather than reading them |
| `wfdb.rdrecord` / `rdann` / `rdsamp` | the WFDB reader | the same ramp signal and the same annotations, so either route sees one world |
| `frontend.detect_r` | the registered detector | the fixture's peaks, in the fixture's order.  **The real detector is never called.** |
| `frontend.rr_features`, `pwave.pwave_features` | the feature producers | rows whose first column is the peak the row was built for |
| `frontend.FS` | the registered sampling rate | `360`, so the source's own `int(0.15 * fs)` lands on the registered 54-sample tolerance the fixtures are built around |
| `frontend._z` | the source's own helper | the identity — and **probed** every run by re-observing each fixture with it negated, so its neutrality is shown rather than assumed |

The stub surface is **declared, not permissive**.  A name it does not carry is
recorded and refused, and the run stops at `P3_STUB_SURFACE_INCOMPLETE` naming
the module and the attribute; returning a mock would let an undeclared
dependency into the run wearing a stub's name.

**The injection spans the call, not only the load.**  `ProducerSession` holds
the stub modules installed in `sys.modules` from compile through exec and
through **every** `build_record()` call, and `load_source_under_injection()`
refuses to execute anything when they are not installed.  An injection that
ended with the load would cover module-level imports only: a `build_record`
containing `import wfdb` or `from .frontend import detect_r` in its own body
resolves those names when it runs, and would then reach the real package — or
the real detector — inside a run whose whole claim is that it reached neither.

Nothing real is read: no ECG signal, no `.atr` file, no V9/V10 cache, no
per-record count.  The ramp signal and the peak-carrying feature rows are what
make the producer's output *self-identifying* — a returned window says which
peak it was cut around, and a returned feature row says which peak it belongs
to — so "which rows did it keep" is an observation rather than an inference.

## What is captured, and how it stays mechanical

Three channels, none of which restates a matching rule:

1. **A line trace of the producer's own frame**, scoped by code-object
   identity, recording what each local did at each step.
2. **The stub call log** — every call the producer made into an injected
   dependency, with what it was handed.
3. **The returned object**, canonicalised.

The projection then reads decisions out of structure rather than out of names:
a container that gained exactly one member, having existed before, is a
consumption; a boolean flag list in which one position turned true is the same
event in a different data structure; a container that gave one member back is a
release.  The integer consumed identifies an annotation by its sample, or by an
index whose two readings — list position and sample rank — agree, or, when
those disagree, by the label the produced row carries, learned from fixtures
this producer resolved unaided.

Every candidate container is projected and the implied mappings are merged.
Agreement between containers is corroboration.  A disagreement is put to the
producer's own output; only one its own output cannot settle is a stop.

**Fixture construction rules** the projection depends on, enforced by
`assert_fixture_contract()` before anything is loaded: every sample is at least
100, so no sample can be mistaken for an index or a distance; peak samples and
annotation samples are disjoint, so an integer seen in a frame says which side
it came from; peaks are distinct and annotation samples are distinct.

## What is compared

One canonical observation per fixture per side, digested with the registered
canonical-JSON convention:

- `peak_to_annotation` — the mapping, with the peak that consumed each one;
- `kept_rows` — the kept set **and its order**;
- `consumed_annotations` — with `consumed_at_peak_index`, i.e. the timing;
- `released_annotations` — annotations handed back, with when;
- `unmatched_annotations`, `unmatched_peaks`;
- `stages` — state before AAMI selection, after AAMI selection and before the
  boundary cut, after the boundary cut, and whether the producer's own kept
  rows are what that description predicts.

The stage decomposition applies the frozen AAMI map and the frozen 150-sample
window identically to each side's own observed matching.  It cannot manufacture
an agreement, because the matching itself comes from each producer, and the
`kept_equals_post_boundary` field records any divergence rather than
normalising it away.

## The six required fixtures

The names are imported from `Q5E.SOURCE_MATCH_REQUIRED_FIXTURES` and are never
retyped.  No fixture records an expected answer — writing one would be a third
transcription of the rule this PREP exists because we cannot trust ourselves to
transcribe.

| fixture | what it refutes |
|---|---|
| `test_source_match_nearest_already_used_falls_through` | that a peak whose nearest annotation is already consumed is dropped rather than falling through to the next-nearest |
| `test_source_match_distance_tie_goes_to_the_earlier_annotation` | that an exact distance tie goes to the later annotation |
| `test_source_match_non_aami_symbol_consumes_its_match` | that a non-AAMI annotation is filtered out of the pool before matching instead of consuming its match and only then being dropped |
| `test_source_match_boundary_cut_consumes_its_match` | that a peak cut by the `p-150` boundary releases its annotation back into the pool |
| `test_source_match_annotation_order_differing_from_sample_order` | that annotations are traversed in the order the reader returned them |
| `test_source_match_peak_order_change_is_visible` | that peaks may be sorted before matching |

**Independent necessity is demonstrated, not asserted.**  The regression suite
builds six synthetic producers, each differing from a faithful one in exactly
one decision, and requires that **exactly one** fixture notices each — so
removing any fixture would let one variant through.  The fixture list may not
be trimmed, renamed, duplicated or extended after seeing a result; a violation
is `P3_FIXTURE_CONTRACT_VIOLATION` and stops the run before anything is
compared.  An additional fixture may only be added by naming it and its
refutation target in this Decision log **before** the source result is seen.

# Registered source identity

The registered `data.py` is `research/ASSETS.md :: baseline-v10-source`,
`MyDrive/mitbih/v9~v13/v10pkg/kinkmap/data.py`:

- Drive file id `1a8mfNbCz5_vPaOWajsX15l93rgEaO_UK`
- parent folder id `1czXZdgSrGttrhOFlNvOHQ3l16ZfluOPX`
- 7,744 bytes
- SHA-256 `20cde66b01d1172926aa1b84cbb70b70ea28bb20c2e958a2c26bd01d03497ada`
  (the same digest `Q5E.M4_SOURCE_MAP_HASHES["data.py"]` already carries; it is
  imported, not copied)

Both are required.  A file id without a digest identifies a name; a digest
without a file id would licence a name search across Drive, which is the
substitution this PREP exists to prevent.  If the file id were absent or
ambiguous in `ASSETS.md`, the run stops with
**`P3_SOURCE_FILE_ID_UNREGISTERED`** and does not fall back to a search.  It is
not absent: the id above is registered, and the implementation pins it as a
constant with the assets row named beside it.

**Order of verification at execution time**, enforced by
`fetch_registered_source()`: direct lookup by file id → provider inventory
(name, size, parents, trashed, shortcut, provider checksum) → read the bytes →
SHA-256 of the bytes read → **only then** compile and execute.  A wrong size,
a trashed file, a shortcut, a folder, a foreign parent or a mismatching
provider checksum stops the run **before anything is downloaded**; a digest
mismatch stops it before anything is compiled.

# Execution barriers

Two, independent.  The implementation PR committed both closed; the
execution-enable PR opened the second one and left the first at its default:

| barrier | value | opened by |
|---|---|---|
| `OPEN_REGISTERED_DATA` | `False` — **still the module default** | an explicit opt-in at the call site, which the notebook now makes |
| `EXECUTION_APPROVAL_RECORD["granted"]` | `True` since 2026-08-15 | the user's separate read-only execution approval, recorded in the field rather than by deleting a check |

The switch stays `False` deliberately: an import, a copied cell or another
module's call still reaches nothing, and the approval is not a standing
permission for the process.  `granted: False` remains an exact one-value
revert that shuts every route again, and the regression suite runs both
states rather than only the one it happens to be committed in.

Neither the Q5-E audit token nor the P1/P2 PREP token opens P3: both are listed
in `REFUSED_TOKENS` and refused **by name**, with a stated reason.  P1/P2
approved reading registered bytes for identity; P3 loads and executes a
registered source file, which is a separate decision.

**A token is not an entry point, and neither is a permit-shaped object.**
Producer bytes are compiled only through `SourcePermit`, which is a **sealed
snapshot of exactly two types**: the base class cannot be instantiated, no
third kind can be defined, no field can be set or deleted after minting, and
the inventory is handed out read-only.  Execution compares `type(permit)` by
identity — never `isinstance`, which a subclass satisfies — and
`validate_permit_for_execution()` re-derives every claim **from the permit's
own bytes on the last line before the compiler**: the recomputed digest must
equal the permit's, and the `kind`/`synthetic`/`approval` combination must be
exactly one of two.  A registered permit additionally re-runs the token, the
guard and — through `assert_registered_provenance()` — the **whole file-id
gate**: the requested and resolved file ids, the name, both byte counts, both
digests, `digest_matches_registered` and `read` exactly `True`, `trashed`,
`is_shortcut` and `is_folder` exactly `False`, an empty problem list, the
registered folder among the parents, and the permit's own label.  A synthetic
permit requires a digest that is not the registered file's.  Matching the
digest alone would say the bytes are the right bytes and nothing about where
they came from, and an arbitrary copy of the same content is not the
registered asset.  An object that skipped its constructor, a
look-alike, and a permit edited after minting all fail there.

The two kinds are not interchangeable:

- `RegisteredSourcePermit` is minted **only** inside
  `fetch_registered_source()`, with a module-private key, after the terminal
  guard, the file-id gate and the digest gate.  Its constructor re-checks the
  key, the approval token, the guard and the digest, so a caller holding the
  key still gets nothing while a barrier is closed.
- `SyntheticSourcePermit` covers a fixture's own producer and **refuses bytes
  whose digest is the registered `data.py`** — so the synthetic route cannot
  be turned into a way to execute the registered source, whatever arguments it
  is given.

There is exactly one place in the module that compiles or executes producer
bytes (`_compile_and_exec`), one public production entry point (`run_p3()`,
which reaches the registered file only through the guard) and one public
synthetic entry point (`execute_synthetic_p3()`, which cannot reach it at
all).  The private executor takes a permit, never a body plus an inventory
plus a token.

While a barrier is closed, an attempted run performs **zero** of each of:
credential acquisition, Drive service construction, Drive API call, registered
file read, import or exec of `data.py`, source `build_record` call, adapter
differential, and output directory creation.  The dependency check runs before
any credential is acquired, so a run that would fail for a missing package
never mints a token first.  The Drive credential must prove **exactly**
`drive.readonly`; a broader scope is refused rather than accepted because it
"includes" what is needed, and a credential that exposes no scopes proves
nothing.

# Mismatch policy

If any fixture disagrees:

- the verdict stays `SOURCE_MATCH_EQUIVALENCE_REQUIRED`;
- no real-record count is opened or consulted;
- `detect_r()` is not run;
- the adapter is **not** modified by this PREP — `describe_difference()`
  preserves the differing fields, both full observations, the injected call
  log, the source digest and the adapter fingerprint in the bundle;
- no candidate record is produced at all, so there is nothing to register,
  trim or argue about;
- a corrected adapter is a separate PR, subject to its own review, and it
  re-runs **every** fixture from the beginning.

There is deliberately no facility for running several candidate rules and
keeping whichever scores best, and the regression suite asserts that no such
facility exists in the module.

## Harness stops are not equivalence failures

`P3_SOURCE_FILE_ID_UNREGISTERED`, `P3_SOURCE_IDENTITY_MISMATCH`,
`P3_SOURCE_UNLOADABLE`, `P3_SOURCE_SIGNATURE_UNBINDABLE`,
`P3_SOURCE_RUNTIME_ERROR`, `P3_SOURCE_TRACE_UNPROJECTABLE`,
`P3_KEPT_ROWS_UNOBSERVABLE` and `P3_FIXTURE_CONTRACT_VIOLATION` each report
themselves.  A run that stopped this way compared nothing; reporting it as a
disagreement between the adapter and the source — in either direction — would
be a fabrication, and `decide()` reports no fixture score for such a run rather
than a zero that would read as six failures.

# PASS record contract

Only when **every** fixture compares equal is a candidate produced, in exactly
the shape `Q5E.verify_source_match_equivalence()` enforces:

```json
{
  "verdict": "SOURCE_MATCH_EQUIVALENT_TO_REGISTERED_SOURCE",
  "registered_file_sha256": "<lowercase 64-hex>",
  "adapter_fingerprint": "<lowercase 64-hex>",
  "prep_bundle_sha256": "<lowercase 64-hex payload fold>",
  "oracle_harness_sha256": "<lowercase 64-hex>",
  "fixtures": [{"name": "…", "source_result_sha256": "…",
                "adapter_result_sha256": "…", "equal": true}],
  "fixtures_passed": "<every fixture>"
}
```

The candidate is put through the registered gate as an **argument**;
`SOURCE_MATCH_ORACLE_RECORD` is not written by this module or by anything it
calls, and the constant stays `None` in this PR.  Registration happens in a
separate PR after Codex accepts the run.

`oracle_harness_sha256` covers the capture and projection functions' own text,
the fixtures, the binding plan and the tolerances — so a PASS recorded under an
older harness cannot be reused for a newer one, just as it cannot be reused
across a changed adapter fingerprint or a changed `data.py` digest.

# PREP bundle

Nine files: the seven-file payload `config.json`, `source_inventory.json`,
`oracle_harness_identity.json`, `fixture_results.json`, `decision.json`,
`log.txt`, `summary.md`, plus `manifest.json` and `COMMITTED.json`.

`prep_payload_sha256` folds exactly those **seven**, using
`Q5E.prep_payload_fold()` — the registered convention, reused rather than
reinvented.  `manifest.json` and `COMMITTED.json` are excluded because each
records the fold, and a file recording its own digest is a circular contract.
The manifest's own SHA-256 is frozen **outside** the bundle: in the saved
output of the notebook's report cell, and later in the registration record.

A synthetic run is stamped inside the folded payload rather than beside it in a
marker file, because the payload list is Q5-E's registered seven and may not
grow — so editing the stamp out breaks the fold.

Publication reuses the P1/P2 contract exactly: `mkdir` claims the directory and
fails rather than replacing anything; every file is created with
`O_CREAT | O_EXCL`; there is no delete, no rename and no fallback path;
`COMMITTED.json` is written last, and a directory without it is an incomplete
write rather than a bundle.  A failed run leaves its partial directory in
place, because that is where a diagnosis will look for it.  No credential,
token or local absolute path is ever written into a bundle file.

`prep_bundle_sha256` in the candidate is the **payload fold**, never the
manifest's own digest.  Because that fold covers `decision.json`, the candidate
record cannot live inside the bundle it would have to describe: the run reports
it, the notebook's saved output freezes it, and `decision.json` carries a
structural pre-check of the same candidate with a placeholder fold, explicitly
flagged as a placeholder.

# Not in scope, and not performed

`detect_r()` or any real detector; any real ECG signal, `.atr` file, V9/V10
cache or real-record count; M0–M4 aggregation; DS2 per-beat labels; V10
probabilities; association or S PR-AUC; any training; any modification, move or
deletion of a Drive artifact; any change to a scientific gate, threshold, null,
seed, family or multiplicity; any change to the P1/P2 registered values or to
the frozen Q5-D module; any registration.

# Acceptance criteria for this implementation PR

1. Both barriers committed closed, and every other stage's token refused by
   name.
2. A closed barrier yields zero credential, API, source-read, source-exec,
   differential and mkdir calls — asserted by counting, not by inspection —
   including for direct calls to the executor, the session factory and the
   loader, which are the routes that would bypass `run_p3()`.
2a. The injection covers the call: a producer that imports its dependencies
   inside `build_record` still reaches only stubs, asserted with decoys
   standing where the real modules would be.
3. File id and digest both checked, in the registered order, before import; a
   file with the right name and a different identity refused in every shape
   tested.
4. The oracle executes the producer itself, and the module contains no second
   matching implementation and no fixture-level expected answer.
5. Each of the six fixtures is shown to be the unique detector of one changed
   decision.
6. Fixture omission, duplication, trimming, `equal=false` and digest
   mismatches all rejected by the registered gate.
7. A changed adapter fingerprint or `data.py` digest invalidates a candidate.
8. Malformed, unloadable, unbindable, unrunnable and unreadable producers all
   report harness stops, never an equivalence failure.
9. Observation digests deterministic; the payload fold self-reference-free.
10. Bundle no-overwrite and commit-marker contracts verified from a consumer's
    position; synthetic bundles stamped as not a result.
11. The notebook is committed unexecuted, with zero outputs and null execution
    counts.
12. `SOURCE_MATCH_ORACLE_RECORD` still `None`; P1/P2 registrations and the
    frozen Q5-D module unchanged; the existing Q5-E, PREP and Q5-D suites still
    pass.

# Decision log

**D1 (2026-08-14) — the registered `build_record` is now called directly.**
The 2026-08-12 third-review ruling (B1 in the parent spec) kept the adapter
independent and declined to call `data.py :: build_record` wholesale, because
it also performs feature computation and file access that are not part of the
matching contract.  P3 reverses that for the differential only, under the
user's 2026-08-14 instruction: the parts that made a wholesale call
objectionable are exactly the parts dependency injection replaces, and the
alternative — a second transcription used as an oracle — is the failure mode
this stop exists to prevent.  The adapter itself is unchanged and is still the
thing under test.

**D2 (2026-08-14) — argument binding is a declared plan, not a guess.**
`data.py` is a registered asset this PR may not open, so `build_record`'s
signature is unknown here.  Parameters are bound by a declared name plan
recorded in the bundle; a required parameter the plan does not cover stops the
run with `P3_SOURCE_SIGNATURE_UNBINDABLE` rather than being filled in.
Extending the plan is a deliberate, re-reviewed edit.

**D3 (2026-08-14) — a conflict between trace containers is settled by the
producer's own output, or it stops.**  A producer keeps several small-integer
collections, and in a fixture where an annotation index and a peak index
coincide, a list of kept row positions reads like a consumption.  Preferring a
container by name would make the projection an interpretation; instead the
conflict is put to the label the producer's own kept row carries, learned from
fixtures it resolved unaided.  An unsettled conflict is
`P3_SOURCE_TRACE_UNPROJECTABLE` — a stop, never a disagreement.

**D4 (2026-08-14) — the candidate record is not stored in the bundle.**  Its
`prep_bundle_sha256` is the bundle's payload fold, which covers
`decision.json`; storing the candidate inside would be the same circularity the
manifest rule already forbids.  `decision.json` carries a placeholder-fold
structural pre-check, flagged as such, and the real candidate is reported by
the run and frozen in the notebook's saved output.

**D5 (2026-08-14) — fixture inputs were adjusted so that each fixture is
uniquely necessary, before any source result was seen.**  Three inputs moved
while the six registered names and their refutation targets stayed fixed: the
non-AAMI fixture's second peak was placed so that its own nearest annotation is
the surviving one (isolating the filter from the fall-through), the peak-order
fixture was given untied distances (isolating traversal order from the tie
rule), and one peak sample was moved off an annotation sample (satisfying the
disjointness rule the projection depends on).  This is a property of the
synthetic inputs only; nothing about the registered source was consulted,
because nothing about it has been read.

**D6 (2026-08-14) — status is `P3_IMPLEMENTATION_AWAITING_CODEX_REVIEW`.**  No
execution approval is requested by this document.  Points Codex is asked to
approve or withdraw explicitly are listed in the implementation PR as B1, B2, …

**D7 (2026-08-14) — Codex review blocker 1 closed: the executor no longer
takes raw bytes.**  The first review found that `execute_p3()` checked neither
`OPEN_REGISTERED_DATA` nor `EXECUTION_APPROVAL_RECORD`, so a caller with the
public token string could compile and execute the registered source, and write
a bundle, with the terminal guard shut — the guard lived in `run_p3()` and
nothing below re-checked it.  The finding is accepted in full.  The public
`execute_p3()` is **removed**; production runs go through `run_p3()` →
`_execute_registered_p3()`, which accepts only a `RegisteredSourcePermit`;
fixtures go through `execute_synthetic_p3()`, whose permit refuses the
registered digest by construction.  The permit type is the typed snapshot the
review asked for: it can only be minted past the guard and the id/digest
gates, and it re-checks the key, the token, the guard and the digest when it
is built and again immediately before execution.  Regression:
`test_producer_bytes_are_executed_only_through_a_permit`,
`test_the_synthetic_route_cannot_execute_the_registered_source`, and
`test_a_closed_guard_reaches_no_compile_exec_or_mkdir_on_the_registered_path`,
which counts calls to the single compile choke point and to `os.mkdir` across
seven direct-call routes and requires zero of each.

**D19 (2026-08-16) — a column selected row by row is still one column; the
synthetic suite failed in Colab and passed here.**  With D17 merged and
execution re-approved, cell 3 stopped before any registered asset was touched:
`'rr' is not a two-dimensional numeric block`, on the *synthetic* `FAITHFUL`
producer.  The cause is a shape the container this repo runs in cannot produce.
A producer that selects rows by index writes `[rr_all[i] for i in keep]` — a
**list of one-dimensional rows** rather than one two-dimensional block — and
where numpy is installed those rows are arrays, not lists.  The width reader
recognised a row only when it was a `list`/`tuple`, so the column read as 1-D
and the carrier as unreadable.

`_row_width()` now asks the row itself: a one-element `shape`, or `len()` for a
`list`/`tuple`, or `len()` for anything that offers `tolist()` — which covers a
numpy row, a stdlib `array.array` row (no `shape` at all) and a plain list
alike.  `_sequence_dtype` and `_flat_tokens` go through the same reading, so a
column of rows is never mistaken for a column of per-row labels.  Ragged rows
are still not a block and are still refused rather than padded.

This is the second time a difference between the two environments has cost a
round trip, and it is worth naming: **numpy is installed where the run happens
and absent where the tests run.**  D17 already moved array reading onto
`shape`/`dtype`/`tolist()` for that reason; the regressions now exercise all
three row kinds, including `array.array`, which is a real array type from the
standard library rather than an imitation of one.  Regression:
`test_a_column_selected_row_by_row_is_still_one_column`.

The execution approval was re-recorded for the new harness digest
`251f6e35d59a6c6949710c70990d57d3ef25c7e5b04a27e072ab4227fe3dd1d7`, with the
reason stated in the record: the fix is inside the same observation seam and
changes nothing the approval was about.  The renewal is in the diff the
approver merges rather than assumed — which is the guard working, not the guard
being worked around.

**D18 (2026-08-16) — execution re-approved, bound to the harness digest.**
The user reviewed D17, merged it, and re-granted read-only execution.  The
approval is recorded **against `oracle_harness_sha256`
`a90d1d2a7dd272d930f64fa4657e91df3f54f8b79c9f968c6b351aa4bc5679e7`** and
`_terminal_execution_guard()` refuses when the module's harness is not that
one, naming both digests.

The reason is the shape of this PREP so far: four of the five rounds were
harness changes, each producing a different oracle.  An approval that applied
to whatever the file says today would be an approval of something nobody read,
and "remember to re-ask" is not a control.  The binding makes renewal
mechanical, and it is a refusal — so the failure direction is always "ask
again", never "run anyway".  `OPEN_REGISTERED_DATA` stays `False`: the switch
was not re-opened, only the approval, and the notebook still opts in at its own
call site.  Regression:
`test_the_approval_is_bound_to_the_harness_it_was_given_for`.

**D17 (2026-08-16) — the return is read by the registered schema, not by
trial; execution approval withdrawn with the harness change.**  D16 widened the
general reader, and Codex's review pointed at the thing that widening does not
fix: the registered `build_record()` returns a **columnar record** — a mapping
of one array per field (`beat`/`ref`/`rr`/`sim`/`pw`/`ctx`/`y`), all row-aligned
— and a reader that recognises rows by trying channels until one works is not a
basis for a statement about the registered source.  Which channel it lands on
depends on what happens to be readable.

The manipulated variable is exactly one thing: **return value → kept-row
identity**.  The fixtures, the adapter, the matching rule, the tolerance and
the verdict criteria are all fixed.

*The record schema is registered, not retyped.*  `COLUMNAR_RECORD_KEYS` is
`BJ.CACHE_KEYS` from the frozen Q5-D module — the cache schema the registered
`prepare()` writes — so this list cannot drift from the thing it describes.

*The identity carrier is fixed in advance and for a structural reason.*
`rr[:, 0]`: the injected `rr_features` stub builds row `j` as `[peak_j, j, 0…]`,
so its first column is the peak the row was built for **by the injection
contract**, not by decoding what the source means by "rr".  It is also the one
channel the `_z` probe cannot move, because the stub never sees `_z`.

*Cross-checks can refuse but never decide.*  `pw[:, 0]` must equal the carrier
exactly where it is readable; the beat window's centre column must equal it
after the declared transform for the active variant (identity under the primary
injection, elementwise negation under the probe — decided from the *variant*,
which is an input, before any value is read).  A contradiction is
`P3_COLUMNAR_RETURN_UNPROJECTABLE`; an unavailable channel is recorded as
unavailable.  Neither can change which rows are read, so no run can end up
reporting the channel that gave the nicest answer.

*The reader is chosen by schema alone*, before a single value is looked at, and
there is **no fallback** from the columnar reader to the general one: falling
back after a contradiction is exactly the after-the-fact selection this removes.
A mapping carrying record columns *without* the carrier is its own stop rather
than a rescue by another channel.

*Nothing is repaired.*  A first column that is NaN, infinite, non-integral, an
unknown sample, or a duplicate is a stop; there is no rounding and no snapping
to a closest peak.  Row **order** is deliberately not a validity rule: one of
the six fixtures exists to catch a producer that reorders its rows, and a rule
that stopped there would turn the difference it was built to detect into "the
harness could not read this".  The order is read, reported, and compared.

*Arrays are read through `shape`/`dtype`/`tolist()`* rather than through
`isinstance(value, numpy.ndarray)`.  numpy is installed where the run happens
and absent where the tests run, so a numpy-typed branch would be exercised only
in the place that cannot test it.

*Diagnosis survives the stop.*  `SourceHarnessError` now carries a structured
`context`, and every fixture records the return's type, keys, per-column shape,
dtype and row-alignment, the channels detected, the per-channel peak sequences,
and per-stub call counts and input row counts — into the existing
`fixture_results.json` (no new bundle file, payload fold unchanged), and onto
the exception when a stop discards the differential.  Shapes and reasons only;
never array contents.

*The approval does not carry over.*  The harness changed, so
`oracle_harness_sha256` changed, and an approval given for a harness the
approver did not see is not an approval of this one.
`EXECUTION_APPROVAL_RECORD.granted` is back to `False` with the withdrawal
recorded beside it, `OPEN_REGISTERED_DATA` stays `False`, and this PR performs
zero registered-source reads, zero Drive API calls, zero P3 runs, zero bundles
and zero registrations.  The order from here is: review this change → merge →
a separate execution-enable approval → one fresh run of all six fixtures from
the first.

New regressions (13): the columnar producer read end to end on all six
fixtures under both injection variants; the reader chosen by schema and never
by result; every way the carrier can fail to identify its rows (width, dtype,
dimensionality, NaN, non-integral, unknown peak, duplicate); cross-checks that
refuse (`pw` moved, beat centre moved) and one that is merely unavailable;
row-count disagreement across columns; a record without its carrier that never
falls back; order read rather than required; the record read through an
array-shaped stand-in with `shape`/`dtype`/`tolist()`; the mutation showing the
general reader *does* read a carrier-less record and so would have chosen a
channel where this one refuses; a stop carrying its diagnosis out to the
bundle; and the diagnosis containing no column values.  Suite: 93 functions,
835 assertions.

**What this does not claim.**  It does not claim to have identified the cause
of the `20260816T000714` stop.  That run predates the shape-describing message,
so its bundle does not say what came back, and a columnar mapping of plain
lists is in fact readable by the old general reader — which means the evidence
is equally consistent with a return the old reader could not name at all.  What
this change does is make the columnar case explicit and checked, and make the
*next* stop say what it saw.  The `20260816T000714` bundle (fold `c0cea7ac…`,
manifest `d0cc9a05…`, Drive folder `1G7ju5VJjKdb6oTM-6n-_nPsM1fb1vRLI`) is a
valid harness-stop audit record and is preserved unmodified.

**D16 (2026-08-16) — fourth attempt stopped at `P3_KEPT_ROWS_UNOBSERVABLE`;
the reader now opens whatever container came back.**  Run `20260816T000714`
ran the registered `build_record` to completion on the first fixture and then
could not read its result: *"the producer returned no row container at all."*
That message was true about the reader, not about the producer.  Row discovery
canonicalised the return with the ordinary container limit, then scanned only
the **top level** of it — so a return that is a tuple of arrays rather than a
mapping of them, or an object carrying them as attributes, looked empty.  An
unread container is not an absent one, and the difference matters because the
first reading would have been recorded as a finding about the registered
source.

Three widenings, each of them still "read what came back" rather than a guess
about what it means: the return is canonicalised with its own larger limit
(`RETURN_MAX_CONTAINER`) so a real beat matrix is not truncated into
unreadability; a return whose canonical form is nothing but a type name is
re-read through its **public, non-callable attributes**, which is how a record
object hands its rows over; and both the row scan and the label-vector scan
recurse into nested containers instead of stopping at the first level they
cannot name.  None of this decodes meaning — the peak-valued field, the
first-column and the window-centre channels are unchanged, and they still have
to agree with each other.

The stop that remains is now actionable.  `P3_KEPT_ROWS_UNOBSERVABLE` prints
the **shape** of what did come back — type, keys, lengths, element kinds via
`describe_returned()` — and no value inside it, so the next extension is
deliberate and the message can never carry something that would pass for a
measurement.  "It kept nothing" and "its output cannot be read" stay separate:
empty containers are still reported as an observation, not a failure.

New regressions: `test_rows_handed_back_in_a_tuple_are_still_read`,
`test_rows_handed_back_as_object_attributes_are_still_read`,
`test_a_return_that_holds_no_rows_stops_and_describes_its_shape` (a producer
returning a count still stops, and the stop names the shape),
`test_the_shape_description_carries_no_measurable_value`, and
`test_an_empty_result_is_reported_as_kept_nothing_not_as_unreadable`.  The
notebook also generates its run stamp in KST rather than having it retyped
each attempt, keeping the hand-written override and the `\d{8}T\d{6}` check.
Bundle `c0cea7ac…` / manifest `d0cc9a05…` is preserved; the adapter, the
fixtures, `SOURCE_MATCH_ORACLE_RECORD = None` and every scientific rule are
untouched.

**D15 (2026-08-15) — third attempt stopped at `frontend._z`; injected
helpers are now probed rather than trusted.**  Run `20260815T235627` got past
the signature and stopped while running: `build_record` calls `frontend._z`.
That is a **function**, and the justification that worked for `FS` does not
transfer — `FS = 360` is right because the source's own `int(0.15 * fs)` then
lands on the registered tolerance, but no arithmetic says what a normaliser
should be.

So `_z` is injected as the identity, the least-interfering stand-in there is,
and its neutrality is **demonstrated on every fixture of every run** instead of
asserted: each fixture is observed a second time with `_z` replaced by an
elementwise negation, and every compared field must be identical.  A field that
moves stops the run at `P3_INJECTED_VALUE_STEERS_MATCHING` — because an
injected value that can move a matching decision is not standing out of the way
of the thing being compared, and a verdict produced through it would be partly
the harness's own. A probe that cannot run (the producer refuses the perturbed
values) is recorded as `untested`, never as passed, and the probe carries its
own label dictionary accumulated in fixture order so a late fixture is not
reported untested for a reason unrelated to `_z`.

`FRONTEND_STUB_FUNCTIONS` is the declared function surface; the invariance
summary is written into `fixture_results.json` and printed by the notebook's
report cell. New regressions:
`test_a_producer_that_normalises_through_the_injected_helper_is_observed`,
`test_an_injected_helper_that_steers_the_matching_is_caught` (a producer whose
matching branches on `_z` is caught, not reported), and
`test_the_probe_reports_untested_rather_than_passed`.  Bundle `31f98c19…` /
manifest `75338583…` is preserved; the adapter, the fixtures and every
scientific rule are untouched.

**D14 (2026-08-15) — second attempt stopped at
`P3_SOURCE_SIGNATURE_UNBINDABLE`; the registered producer is handed its
inputs.**  With `FS` declared, run `20260815T233808` got past the import and
stopped on the signature: `build_record` has required parameters `sig`,
`ann_sample` and `ann_symbol`.  So the registered producer does **not** read
its own signal and annotations — it receives them, and the caller (`prepare()`)
does the reading.  That is a fact about the source obtained by observing a
refusal, and it makes the injection *more* direct rather than less: the
fixture's data now arrives as arguments.

The binding plan is extended to cover those three names, and
`binding_values(fixture)` is fixture-dependent by necessity — a producer that
receives this fixture's signal must receive *this* fixture's.  The values are
built exactly as the reader stubs build theirs, so a producer using either
route sees one world, and a regression asserts that equality fixture by
fixture.  `BINDING_RATIONALE` states, per key, why the value cannot change the
behaviour under test, and it is folded into `oracle_harness_sha256` so editing
a reason invalidates a PASS recorded under the old one.

Two diagnosis improvements, because the first two stops each cost a round
trip: `P3_SOURCE_SIGNATURE_UNBINDABLE` now prints the **whole observed
signature** and what the plan did bind, and the notebook's report cells print
`decision['detail']` for any harness stop — previously that string lived only
in the bundle, so the operator had to open Drive to learn what was missing.

New regressions: `test_a_producer_handed_its_inputs_as_arguments_runs_and_is
_observed` (an argument-shaped producer agrees on all six fixtures),
`test_the_injected_arguments_match_what_the_reader_stubs_return`,
`test_every_injected_argument_carries_a_stated_reason`, and
`test_an_unbindable_signature_reports_the_whole_signature`.  Bundle
`bac0b881…` / manifest `c37172a1…` is preserved, and the adapter, the
fixtures and every scientific rule are untouched.

**D13 (2026-08-15) — first execution attempt stopped at
`P3_STUB_SURFACE_INCOMPLETE`; the injected surface now declares `FS`.**  The
approved run `20260815T232546` reached the registered file and verified it:
file id `1a8mfNbCz5_vPaOWajsX15l93rgEaO_UK`, provider checksum and read bytes
both `20cde66b…`, scope proven exactly `drive.readonly`.  Loading it then
raised `AttributeError: module 'frontend' has no attribute 'FS'` — the
registered `data.py` reads `frontend.FS` at import time, and the injected stub
declared no constants at all.  **This is not a disagreement with the adapter
and not a defect in the source**: it is this harness's injection surface being
incomplete, and the run reported it as its own stop, produced no candidate,
opened no record count and preserved its bundle (payload fold
`dda8e3d2…`, manifest `cc997af2…`).

The fix is deliberately narrow.  `FRONTEND_STUB_CONSTANTS` declares `FS = 360`
— pinned by arithmetic rather than by taste: the static source map records
that `data.py` computes `int(0.15 * fs)`, and `int(0.15 * 360) == 54 ==
M4_PEAK_MATCH_TOLERANCE_SAMPLES`, the registered tolerance the six fixtures
are built around.  Any other value would silently change the behaviour under
test, which is the one thing an injection may never do; a regression asserts
the arithmetic, not the number.  Undeclared names are no longer a bare
`AttributeError`: each stub records the request in the call log and raises
`StubAttributeMissing`, which the harness converts into
`P3_STUB_SURFACE_INCOMPLETE` naming the module and the attribute, so a further
gap is diagnosed in one run instead of guessed.  Returning a mock for unknown
names was rejected: it would let an undeclared dependency into the run wearing
a stub's name.  `WFDB_STUB_CONSTANTS` and `PWAVE_STUB_CONSTANTS` stay empty
until a run demonstrates a need — the surface is what the source is shown to
require, never what it might plausibly want.  New regressions:
`test_a_producer_that_reads_a_declared_constant_loads_and_runs`,
`test_an_undeclared_stub_attribute_is_its_own_stop`, and
`test_an_undeclared_attribute_is_recorded_before_it_is_refused`.

The stop bundle is kept as an authentic record of an attempted run, exactly as
the 2026-08-12 P2 stop bundle was, and the re-run writes a new timestamped
folder rather than replacing it.  Nothing about the adapter, the fixtures or
any scientific rule changed, and no equivalence verdict was produced.

**D12 (2026-08-15) — read-only execution approved; the record moved, nothing
else did.**  Codex accepted the implementation at `40b1642`
(`P3_IMPLEMENTATION_ACCEPTED`), PR #140 merged as `e35e733`, and the user
granted a separate read-only execution approval.  The execution-enable change
touches three things and no others: `EXECUTION_APPROVAL_RECORD` (`granted`,
`granted_on`, `granted_by`, and the `would_approve` list renamed to `approved`
now that it is one), the notebook's call-site opt-in with a Drive mount for
the output bundle and a refusal to run with an empty `TIMESTAMP`, and the
regression suite's guard helper, which now holds the record at either value
and restores it — so the refusals that protect an unapproved run are still
exercised, from the approved state, rather than becoming untested.  No
fixture, no adapter, no scientific gate, threshold, null, seed, family or
multiplicity is touched; `OPEN_REGISTERED_DATA` stays `False`;
`SOURCE_MATCH_ORACLE_RECORD` stays `None`.  New regressions:
`test_the_execution_approval_is_recorded_rather_than_implied`,
`test_the_switch_default_still_refuses_a_stray_import`, and
`test_reverting_the_approval_restores_every_refusal`.  The Drive mount is for
**writing the bundle only** — the registered `data.py` is still read through
the API by file id, never through a mount path, because picking a file by path
is the substitution this PREP exists to prevent.

**D11 (2026-08-14) — fourth-review items closed: the parent gate runs before
the download, and an empty problem list means exactly that.**  Two narrow
exactness defects.  First, the parent comparison in
`fetch_registered_source()` was guarded by the parents being non-empty, so a
provider that returned none at all skipped the check and the bytes were
transferred; the permit's provenance check would still have refused
afterwards, but the contract is that an unconfirmed parent stops the run
**before** the download, and "the provider told us nothing" is not "the
provider confirmed the registered folder".  The guard is removed, so a
missing, empty or foreign parent all stop at the same place.  Second,
`assert_registered_provenance()` coerced the problem list before comparing it,
which accepted a missing key, a `None` and an empty tuple as a clean read —
exactly the fields a hand-assembled inventory would leave unwritten.  It now
requires `problems` to be exactly `[]`.  Regressions:
`test_a_file_with_no_confirmable_parent_is_refused_before_the_download`
(empty, omitted and foreign parents; `P3_SOURCE_IDENTITY_MISMATCH`, one
`get_metadata` call and zero downloads) and
`test_an_empty_problem_list_means_exactly_an_empty_list` (missing, `None`,
empty tuple, empty string and empty dict all refused, with a genuine
inventory still passing).

**D10 (2026-08-14) — third-review blocker closed: a registered permit must
show its file-id provenance, not only its digest.**  D9's re-validation
checked the type, the recomputed digest, the token and the guard, but of the
inventory it checked only `observed_sha256`.  With the guard open, a permit
assembled around the right bytes with a two-field inventory therefore passed —
and that breaks this PREP's actual contract, because an arbitrary copy of the
same content would be indistinguishable from a read of the registered Drive
file.  Matching the digest says the bytes are the right bytes; it does not say
where they came from.  The finding is accepted in full.
`assert_registered_provenance()` now re-derives the whole file-id gate from
the inventory — `requested_file_id`, `file_id`, `name`, `bytes` and
`observed_bytes` against the registered byte count and the permit's own body
length, `registered_sha256` and `observed_sha256` against the recomputed
digest, `digest_matches_registered` and `read` exactly `True`, `trashed`,
`is_shortcut` and `is_folder` exactly `False`, an empty `problems` list, the
registered folder among the parents, and the permit's own label — with
booleans compared by identity so a truthy string cannot stand in for one.  It
runs when the permit is minted **and** on the last line before the compiler.
Regressions: `test_a_registered_permit_must_show_it_came_from_the_registered
_file_id` (the reported bypass verbatim, through the factory, the loader, the
registered executor and the validator, with compiles and mkdirs counted at
zero) and `test_each_provenance_field_of_a_registered_permit_is_re_checked`
(sixteen single-field mutations of a genuine permit's inventory plus a
relabelled permit, all refused, and the genuine permit still passing).

**D9 (2026-08-14) — second-review blocker closed: permits are sealed, and
re-validated before the compiler.**  D7 introduced the permit but left it a
plain object: the base class was constructible, its slots were writable, and
callers checked `isinstance`.  A third kind of permit could therefore be
assembled by hand — claiming `synthetic`, carrying the registered bytes — and
it skipped both the guard re-check (it was not a `RegisteredSourcePermit`) and
the digest refusal (no constructor ran); a legitimately minted synthetic
permit could be edited to the same effect.  The finding is accepted in full.
`SourcePermit` now refuses direct construction, refuses any further subclass
at class-creation time, refuses attribute assignment and deletion after
minting, and exposes its inventory as a read-only mapping.  Execution compares
the type by identity, and `validate_permit_for_execution()` re-derives the
digest from the permit's own bytes and re-checks the whole
`kind`/`synthetic`/`approval` combination — plus the token, the guard and the
inventory identity for a registered permit — immediately before
`_compile_and_exec()`, on every route.  Regressions:
`test_a_hand_built_permit_cannot_execute_the_registered_bytes` (the reported
bypass verbatim, plus a constructor-skipping forgery, with compiles and mkdirs
counted at zero), `test_a_permit_subclass_is_not_a_permit`,
`test_a_minted_permit_cannot_be_edited_afterwards`,
`test_validation_runs_again_immediately_before_the_compiler` (asserts every
compile is immediately preceded by a validation) and
`test_a_registered_permit_is_refused_once_the_guard_closes_again`.

**D8 (2026-08-14) — Codex review blocker 2 closed: the injection now spans the
call.**  The first version closed the `InjectedModules` context as soon as the
source module had executed, so a `build_record` importing `wfdb` or
`.frontend` **inside its own body** would have resolved those names after
`sys.modules` was restored, reaching the real package and the real detector
mid-run.  The finding is accepted in full.  `ProducerSession` now holds the
injection open across compile, exec and every call, `observe_source()` is
called inside that `with` block, and `load_source_under_injection()` refuses
to execute anything unless the stub modules are the ones installed.
Regression: `test_a_producer_that_imports_inside_the_function_still_gets_the
_stubs` runs a late-importing producer with decoys installed where the real
modules would be — verified to fail against the previous lifetime with "the
REAL wfdb.rdrecord was reached" — plus
`test_the_producer_session_holds_the_injection_across_the_call`.
