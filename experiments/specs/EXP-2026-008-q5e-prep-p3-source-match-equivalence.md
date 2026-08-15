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

- **implementation approved** — the user approved the design and the
  implementation of P3 on 2026-08-14, and this document is promoted to
  `approved_for_implementation` on that basis.
- **execution not approved** — no approval exists to read the registered
  `data.py`, to authenticate to Drive, or to run the differential.  Both
  barriers in the module are closed and this PR does not open them.
- **result not run** — the differential has never been executed against the
  registered source.  There is no measured outcome anywhere in this
  repository, and none may be inferred from the fact that the code exists.
- **`SOURCE_MATCH_ORACLE_RECORD` registration not approved** — a PASS, if one
  is ever measured, does not register itself.  Registration is a separate PR
  after Codex accepts the run.
- **Q5-E scientific execution not approved** — P3 is one of three preflights.
  Completing it approves nothing about the audit itself.

No statement below may be read as `PREP_IMPLEMENTATION_ACCEPTED`, `P3_PASS`,
`SOURCE_MATCH_EQUIVALENT_TO_REGISTERED_SOURCE`, or an execution approval.  The
state this PR ends in is **`P3_IMPLEMENTATION_AWAITING_CODEX_REVIEW`**.

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
| `wfdb.rdrecord` / `rdann` / `rdsamp` | the WFDB reader | a ramp signal where `signal[i] == i`, and the fixture's annotations in the fixture's own order |
| `frontend.detect_r` | the registered detector | the fixture's peaks, in the fixture's order.  **The real detector is never called.** |
| `frontend.rr_features`, `pwave.pwave_features` | the feature producers | rows whose first column is the peak the row was built for |

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

Two, independent, and both closed in the implementation PR:

| barrier | value | opened by |
|---|---|---|
| `OPEN_REGISTERED_DATA` | `False` | an explicit opt-in at the call site |
| `EXECUTION_APPROVAL_RECORD["granted"]` | `False` | a separate approval PR changing one field |

Neither the Q5-E audit token nor the P1/P2 PREP token opens P3: both are listed
in `REFUSED_TOKENS` and refused **by name**, with a stated reason.  P1/P2
approved reading registered bytes for identity; P3 loads and executes a
registered source file, which is a separate decision.

**A token is not an entry point.**  Producer bytes are compiled only through
`SourcePermit`, and the two kinds are not interchangeable:

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
