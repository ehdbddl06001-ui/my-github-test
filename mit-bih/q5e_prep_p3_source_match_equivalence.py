#!/usr/bin/env python3
"""EXP-2026-008 / Q5-E — PREP P3: source-match equivalence differential.

The last of the three registrations that stop a Q5-E run is the one that
cannot be settled by hashing a file.  `Q5E.match_peaks_to_annotations()` is a
**candidate** adapter written from prose, and `SOURCE_MATCH_ORACLE_RECORD is
None` stops M4 before the detector runs precisely because nobody has compared
it against the registered `data.py`.

What an oracle may be
---------------------
Not a second reimplementation.  Transcribing "greedy nearest with a `used`
set" twice can reproduce the same misreading twice and call the agreement a
proof.  So the oracle here **is the registered source itself**: the
digest-verified `data.py` is loaded into an isolated namespace, its
`build_record` is called under synthetic dependency injection — stub WFDB
reader, stub `detect_r`, stub RR/feature producer — and what it did is
captured **mechanically**: a line trace of its own frame, the arguments it
handed to the injected stubs, and the object it returned.  No sentence of
`data.py` is re-expressed as a rule anywhere in this file, and no expected
answer is written down for any fixture.

What is compared
----------------
Both sides are projected into one canonical observation — peak to annotation
mapping, kept rows and their order, the consumed annotations and *when* each
was consumed, the unmatched annotations, the unmatched peaks, and the state
either side of AAMI selection and of the boundary cut.  Digest equality of
that record, on every one of the six required fixtures, is the only thing
that can produce a PASS.  The projection is the same code for both sides, so
it cannot be tuned to make one of them look like the other.

Reproducing 22/22 per-record counts is **not** evidence of equivalence and is
not consulted here.  There is deliberately no facility for running several
candidate rules and keeping whichever scores best: this module compares one
adapter against one registered source and reports what it found.

What this file may never do
---------------------------
Open a real ECG signal, call the real `detect_r()`, read a V9/V10 cache, look
at a real-record count, aggregate M0-M4, open a DS2 per-beat label or a V10
probability, compute an association or S PR-AUC, train anything, or modify,
move or delete any Drive artifact.  Reaching the registered `data.py` at all
needs **two independent barriers** open: `OPEN_REGISTERED_DATA` and this
PREP's own execution-approval record.  Neither is open in this implementation
PR, and neither may be opened by reusing the Q5-E audit token or the P1/P2
PREP token — both are refused by name.

Bytes are executed only through a `SourcePermit`, never from a raw body and a
token string, and there are exactly two kinds: one minted solely inside
`fetch_registered_source()` after the guard and the id and digest gates, and
one for fixture bytes that **refuses the registered digest outright**.  The
stub modules stay installed for the whole `ProducerSession` — the load *and*
every call — so a dependency imported inside `build_record` reaches the
injection too, rather than the real package a moment after the load finished.

Failure is not equivalence failure
----------------------------------
A malformed source, an import error, an unbindable signature, an unreadable
trace: each is reported as its own harness stop.  None of them may wear the
costume of "the adapter disagrees with the source", and none of them produces
a candidate record.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import sys
import types
from typing import (Callable, Dict, List, Mapping, Optional, Sequence, Set,
                    Tuple)

try:                                                        # pragma: no cover
    import q5d_order_preserving_beat_join as BJ
    import q5e_leg2_failure_mechanism_audit as Q5E
    import q5e_prep_p1_p2_asset_identity as P12
except ImportError:                                         # pragma: no cover
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import q5d_order_preserving_beat_join as BJ
    import q5e_leg2_failure_mechanism_audit as Q5E
    import q5e_prep_p1_p2_asset_identity as P12


EXPERIMENT_ID = "EXP-2026-008"
SUBSTAGE = "Q5E_PREP_P3_SOURCE_MATCH_EQUIVALENCE"
RUN_SLUG = "EXP-2026-008_q5e_prep_p3_source_match_equivalence"
MODULE_VERSION = 1
SPEC_PATH = ("experiments/specs/"
             "EXP-2026-008-q5e-prep-p3-source-match-equivalence.md")
PARENT_SPEC_PATH = ("experiments/specs/"
                    "EXP-2026-008-q5e-leg2-failure-mechanism-audit.md")
P1_P2_CONTRACT_PATH = ("experiments/specs/"
                       "EXP-2026-008-q5e-prep-p1-p2-execution-contract.md")

# ─────────────────────────────────────────────────────────────────────────────
# The registered source, by **file id and digest**.
#
# `research/ASSETS.md :: baseline-v10-source` registers the V10 producer
# package and gives `kinkmap/data.py` its own Drive file id and byte count; the
# digest is the one EXP-2026-008 froze on 2026-08-11 and the one
# `Q5E.M4_SOURCE_MAP_HASHES` already carries.  Both are required: a file id
# without a digest identifies a name, and a digest without a file id would
# licence a name search across Drive — which is exactly the substitution this
# PREP exists to prevent.
# ─────────────────────────────────────────────────────────────────────────────
REGISTERED_SOURCE_NAME = Q5E.SOURCE_MATCH_REGISTERED_FILE          # data.py
REGISTERED_SOURCE_FUNCTION = Q5E.SOURCE_MATCH_REGISTERED_FUNCTION  # build_record
REGISTERED_SOURCE_SHA256 = Q5E.M4_SOURCE_MAP_HASHES[REGISTERED_SOURCE_NAME]
#: `MyDrive/mitbih/v9~v13/v10pkg/kinkmap/data.py`, 7,744 B.
REGISTERED_SOURCE_FILE_ID = "1a8mfNbCz5_vPaOWajsX15l93rgEaO_UK"
REGISTERED_SOURCE_FOLDER_ID = "1czXZdgSrGttrhOFlNvOHQ3l16ZfluOPX"
REGISTERED_SOURCE_BYTES = 7744
REGISTERED_SOURCE_ASSET_ROW = "baseline-v10-source"
#: The package `data.py` lives in.  It is loaded as `<package>.data` so that a
#: relative `from .frontend import detect_r` resolves to an injected stub
#: rather than to whatever happens to sit on `sys.path`.
REGISTERED_SOURCE_PACKAGE = "kinkmap"

# ─────────────────────────────────────────────────────────────────────────────
# Verdicts.
#
# Exactly two of these are equivalence verdicts in the Q5-E sense; the rest are
# harness stops, and they are kept apart deliberately.  "The source could not
# be loaded" and "the adapter disagrees with the source" are different
# findings, and collapsing them would let a broken run be read as a scientific
# one — in either direction.
# ─────────────────────────────────────────────────────────────────────────────
P3_PASS = Q5E.SOURCE_MATCH_ORACLE_PASS
P3_EQUIVALENCE_REQUIRED = Q5E.SOURCE_MATCH_EQUIVALENCE_REQUIRED
P3_SOURCE_FILE_ID_UNREGISTERED = "P3_SOURCE_FILE_ID_UNREGISTERED"
P3_SOURCE_IDENTITY_MISMATCH = "P3_SOURCE_IDENTITY_MISMATCH"
P3_SOURCE_UNLOADABLE = "P3_SOURCE_UNLOADABLE"
P3_SOURCE_SIGNATURE_UNBINDABLE = "P3_SOURCE_SIGNATURE_UNBINDABLE"
P3_SOURCE_RUNTIME_ERROR = "P3_SOURCE_RUNTIME_ERROR"
P3_SOURCE_TRACE_UNPROJECTABLE = "P3_SOURCE_TRACE_UNPROJECTABLE"
P3_KEPT_ROWS_UNOBSERVABLE = "P3_KEPT_ROWS_UNOBSERVABLE"
P3_FIXTURE_CONTRACT_VIOLATION = "P3_FIXTURE_CONTRACT_VIOLATION"
#: The producer asked an injected stub for a name the declared surface does
#: not carry.  Its own stop, because "the injection is incomplete" and "the
#: source is broken" are different findings and only the first one is ours to
#: fix.  The 20260815T232546 run stopped here: the registered `data.py` reads
#: `frontend.FS` at import time, and the stub declared no constants at all.
P3_STUB_SURFACE_INCOMPLETE = "P3_STUB_SURFACE_INCOMPLETE"
#: An injected value was shown to change the matching decisions.  A constant
#: can be justified by arithmetic — `FS = 360` reproduces the registered
#: tolerance — but a *function* cannot, so the neutrality of one is not
#: asserted, it is probed: the same fixture is run again under a deliberately
#: different implementation, and the observation must be identical.  When it is
#: not, the injection is steering the thing it was supposed to stand out of the
#: way of, and that is a stop rather than a verdict.
P3_INJECTED_VALUE_STEERS_MATCHING = "P3_INJECTED_VALUE_STEERS_MATCHING"
#: The producer returned the registered **columnar** record — a mapping of
#: per-row columns — and its own channels do not agree about which rows it
#: kept.  Its own stop, kept apart from the generic one: here the return *was*
#: recognised and read, and what failed is a contradiction inside it.  Reading
#: this as `SOURCE_MATCH_EQUIVALENCE_REQUIRED` would be wrong in the worst
#: direction, because no comparison was made.
P3_COLUMNAR_RETURN_UNPROJECTABLE = "P3_COLUMNAR_RETURN_UNPROJECTABLE"
#: The producer ran to completion and returned **nothing** — `None`, not an
#: empty record.  Its own stop, because it is a different finding again: the
#: run reached the registered source, executed it, and the source declined to
#: build a record for this input.  Reading that as "the reader could not see
#: the rows" would send the next round to the wrong place, and reading it as a
#: disagreement would be a fabrication — no rows were compared.  Whether the
#: cause is the fixture or the producer is answered by the trace, not here.
P3_SOURCE_RETURNED_NO_RECORD = "P3_SOURCE_RETURNED_NO_RECORD"
#: Stops that say the harness could not make the comparison.  A candidate
#: record is never produced from one of these, and none of them may be
#: reported as a disagreement between the adapter and the registered source.
HARNESS_STOPS: Tuple[str, ...] = (
    P3_SOURCE_FILE_ID_UNREGISTERED, P3_SOURCE_IDENTITY_MISMATCH,
    P3_SOURCE_UNLOADABLE, P3_SOURCE_SIGNATURE_UNBINDABLE,
    P3_SOURCE_RUNTIME_ERROR, P3_SOURCE_TRACE_UNPROJECTABLE,
    P3_KEPT_ROWS_UNOBSERVABLE, P3_FIXTURE_CONTRACT_VIOLATION,
    P3_STUB_SURFACE_INCOMPLETE, P3_INJECTED_VALUE_STEERS_MATCHING,
    P3_COLUMNAR_RETURN_UNPROJECTABLE, P3_SOURCE_RETURNED_NO_RECORD)
P3_STATUSES: Tuple[str, ...] = (
    (P3_PASS, P3_EQUIVALENCE_REQUIRED) + HARNESS_STOPS)
#: Ordered P3 gates.  The source is never imported before its identity has
#: been established, and no differential is attempted before the fixture set
#: has been checked against the registered required-fixture list.
P3_GATE_ORDER: Tuple[str, ...] = (
    "fixture_contract", "source_file_id_registered", "source_inventory",
    "source_bytes_digest", "source_loaded", "fixture_differential",
    "candidate_structure")

# ─────────────────────────────────────────────────────────────────────────────
# Approval.  Two barriers, and neither is opened by another stage's token.
# ─────────────────────────────────────────────────────────────────────────────
EXECUTION_APPROVAL_TOKEN = (
    "q5e-prep-p3-source-match-differential-read-only-execution-approved-by-user")
EXECUTION_APPROVAL_FLAG = "--i-have-separate-p3-execution-approval"
#: Barrier 1.  Default closed, and left closed by this implementation PR: a
#: stray import, a notebook run or a copied cell cannot reach `data.py`.
OPEN_REGISTERED_DATA = False

#: Tokens that are **not** this approval, refused by name so that reuse is a
#: named failure rather than a silent one.  P1/P2 approved reading registered
#: bytes for identity; the Q5-E token approves the audit itself.  Neither
#: approves loading and executing a registered source file.
REFUSED_TOKENS: Dict[str, str] = {
    Q5E.EXECUTION_APPROVAL_TOKEN: (
        "the Q5-E audit execution token.  Approving the audit is not "
        "approving this PREP, and this PREP running does not approve the "
        "audit"),
    P12.EXECUTION_APPROVAL_TOKEN: (
        "the P1/P2 PREP token.  P1/P2 approved reading registered bytes for "
        "identity; P3 loads and executes a registered source file, which is a "
        "separate decision"),
}

#: What a P3 approval would and would not cover.  Written down rather than
#: implied, so the boundary is readable from the code and not only from a spec.
NOT_APPROVED: Tuple[str, ...] = (
    "the Q5-E scientific execution",
    "running detect_r() or any real detector",
    "opening a real ECG signal, a V9/V10 cache or any real-record count",
    "M0-M4 aggregation",
    "opening DS2 per-beat labels",
    "opening V10 probabilities",
    "computing association or S PR-AUC",
    "training or retraining any model",
    "registering SOURCE_MATCH_ORACLE_RECORD",
    "modifying, moving or deleting any Drive artifact",
    "correcting the candidate adapter inside this PREP",
)

#: Barrier 2.  The user's separate read-only execution approval, written down
#: rather than implied by a deleted line.  A guard that opens because someone
#: edited it records no decision; this records who approved what, when, and —
#: just as importantly — what was **not** approved, so the boundary is
#: readable from the code and not only from a spec.  Setting `granted` back to
#: `False` restores every refusal exactly, with no other change anywhere.
#:
#: **Re-granted on 2026-08-16**, for the columnar-reader harness and no other.
#: The approval of 2026-08-15 was withdrawn when that reader changed the
#: harness digest; this one names the digest it was given for, and
#: :func:`_terminal_execution_guard` refuses when the module's harness is not
#: that one.  Renewal is mechanical rather than remembered, and the failure
#: direction is "ask again".
EXECUTION_APPROVAL_RECORD: Dict[str, object] = {
    "granted": True,
    "granted_on": "2026-08-16",
    "for_oracle_harness_sha256": (
        "ae0b12f8365ccf6fbb3433d9d6d85670c1d0fe9cb563576aaebdaa2ac52d6487"),
    "renewed_for_this_harness_because": (
        "run 20260816T131241 reported two more helpers at once "
        "(frontend.stack_ctx, frontend.slope_channel), which are declared as "
        "probed identities, and showed compare_features being called without "
        "the peaks - so the row producers now recover their rows from the "
        "beat windows, which name their own centre under the injected ramp.  "
        "Injection surface only; the fixtures (as revised in D21, which the "
        "spec owner should still review), the rule, the tolerance and the "
        "verdict criteria are unchanged"),
    "supersedes": {
        "granted_on": "2026-08-15",
        "withdrawn_on": "2026-08-16",
        "withdrawn_because": (
            "the kept-row observation seam changed, so oracle_harness_sha256 "
            "changed; the 2026-08-15 execution approval and the "
            "P3_IMPLEMENTATION_ACCEPTED that came with it were given for the "
            "previous harness and did not carry over"),
    },
    "granted_by": "user",
    "kind": ("read-only execution of EXP-2026-008 Q5-E PREP P3: the candidate "
             "adapter against the registered data.py under synthetic "
             "dependency injection"),
    "approved": (
        f"reading the registered {REGISTERED_SOURCE_NAME} by file id "
        f"{REGISTERED_SOURCE_FILE_ID} under exactly the drive.readonly scope",
        "loading it into an isolated namespace with synthetic stubs injected",
        "calling its build_record on the six registered synthetic fixtures",
        "writing the P3 PREP result bundle and saving the executed notebook "
        "with its outputs",
    ),
    "not_approved": NOT_APPROVED,
    "implementation_accepted": "P3_IMPLEMENTATION_ACCEPTED (Codex, 2026-08-15, "
                               "commit 40b1642)",
    "recorded_in": SPEC_PATH,
}
APPROVAL_NOTE = (
    "Approved (2026-08-16) by the user, for oracle harness a90d1d2a… and no "
    "other: the 2026-08-15 approval was withdrawn when the kept-row reader "
    "changed the harness digest, and this one is bound to the digest so the "
    "next harness change closes the door again rather than inheriting an "
    "approval nobody gave.  The run starts again from the first of the six "
    "fixtures.  What is approved: **read-only** execution of P3 — "
    f"reading the registered {REGISTERED_SOURCE_NAME} by file id "
    f"{REGISTERED_SOURCE_FILE_ID} under exactly the drive.readonly scope, "
    "loading it under synthetic dependency injection, running the six "
    "registered fixtures, and writing the PREP bundle.  OPEN_REGISTERED_DATA "
    "is still False by default, so a stray import reaches nothing; the "
    "notebook opts in explicitly at its call site.  Neither the Q5-E audit "
    "token nor the P1/P2 PREP token opens this stage.  NOT approved by it: "
    + ", ".join(NOT_APPROVED) + ".")

# ─────────────────────────────────────────────────────────────────────────────
# Bundle contract.  The payload fold is Q5-E's registered seven-file list and
# the fold function is Q5-E's, reused rather than reinvented; `manifest.json`
# and `COMMITTED.json` sit outside it for the reason the fold exists.
# ─────────────────────────────────────────────────────────────────────────────
PREP_PAYLOAD_FILES: Tuple[str, ...] = Q5E.PREP_PAYLOAD_FILES
PREP_MANIFEST_FILE = Q5E.PREP_MANIFEST_FILE
COMMIT_MARKER = P12.COMMIT_MARKER
BUNDLE_FILES: Tuple[str, ...] = tuple(sorted(
    set(PREP_PAYLOAD_FILES) | {PREP_MANIFEST_FILE, COMMIT_MARKER}))
#: A synthetic run is stamped **inside** the folded payload rather than beside
#: it in a marker file.  P1/P2 puts its marker in its own payload list; here
#: the payload list is Q5-E's registered seven and may not grow, so the stamp
#: goes where the fold already covers it — editing it out breaks the fold.
SYNTHETIC_NOTE = ("SYNTHETIC FIXTURE - NOT A Q5-E RESULT and NOT A P3 RESULT. "
                  "Produced against a synthetic producer module, not against "
                  "the registered data.py.  Never an ingest candidate and "
                  "never a SOURCE_MATCH_ORACLE_RECORD candidate.")
ANCHOR_SAME_RUN = P12.ANCHOR_SAME_RUN
ANCHOR_SAVED_NOTEBOOK = P12.ANCHOR_SAVED_NOTEBOOK
ANCHOR_REGISTERED_RECORD = P12.ANCHOR_REGISTERED_RECORD
ANCHOR_NONE = P12.ANCHOR_NONE
MANIFEST_ANCHOR_SOURCES = P12.MANIFEST_ANCHOR_SOURCES
EXTERNAL_MANIFEST_ANCHORS = P12.EXTERNAL_MANIFEST_ANCHORS

DRIVE_READONLY_SCOPE = P12.DRIVE_READONLY_SCOPE
DRIVE_FOLDER_MIME = P12.DRIVE_FOLDER_MIME
DRIVE_SHORTCUT_MIME = P12.DRIVE_SHORTCUT_MIME
READONLY_SCOPE_UNPROVEN = "P3_READONLY_SCOPE_UNPROVEN"


class P3Error(RuntimeError):
    """Any refusal from this module."""


class P3NotApprovedError(P3Error):
    """Reached a registered asset without this PREP's own approval."""


class SourceHarnessError(P3Error):
    """The harness could not make the comparison.

    Deliberately distinct from a disagreement: a caller catching this must not
    report `SOURCE_MATCH_EQUIVALENCE_REQUIRED` "because the fixtures differed",
    because they were never compared.
    """

    def __init__(self, status: str, message: str,
                 context: Optional[Mapping[str, object]] = None) -> None:
        if status not in HARNESS_STOPS:
            raise P3Error(f"{status!r} is not a registered harness stop; the "
                          f"harness does not invent verdicts")
        super().__init__(f"{status}: {message}")
        self.status = status
        self.detail = message
        #: Structured diagnosis, carried on the exception so that it survives
        #: to the bundle.  A stop discards the differential, so anything only
        #: reachable through the returned result is lost exactly when it is
        #: most needed — which is how the 20260816T000714 run cost a round
        #: trip.  Shapes and reasons only: never array contents.
        self.context: Dict[str, object] = dict(context or {})


def require_execution_approval(approval: Optional[str], what: str) -> None:
    """Permission before capability, checked before any read or API call."""
    if approval is not None and approval in REFUSED_TOKENS:
        raise P3NotApprovedError(
            f"refusing to reach {what}: the token supplied is "
            f"{REFUSED_TOKENS[approval]}.  P3 has its own approval and does "
            f"not accept another stage's.  {APPROVAL_NOTE}")
    if approval != EXECUTION_APPROVAL_TOKEN:
        raise P3NotApprovedError(
            f"refusing to reach {what}: this read-only differential needs its "
            f"own separate execution approval.  {APPROVAL_NOTE}")


def execution_is_approved(approval: Optional[str]) -> bool:
    return approval == EXECUTION_APPROVAL_TOKEN


def _terminal_execution_guard() -> Dict[str, object]:
    """The single stop a separately approved execution PR opens.

    It sits after the switch, the token and the fixture contract, and before
    dependencies, credentials, the Drive service and every read — so an
    unapproved call performs zero authentication attempts rather than a failed
    one.  **The execution PR opens it** by consulting
    :data:`EXECUTION_APPROVAL_RECORD` rather than by deleting the check: a
    removed line reads identically whether the approval happened or somebody
    removed an inconvenience, while a consulted record keeps the decision
    legible, keeps `granted: False` as an exact one-value revert, and keeps
    this function as the only place the boundary moves.
    """
    if not EXECUTION_APPROVAL_RECORD.get("granted"):
        raise P3NotApprovedError(
            "P3 is implemented but not approved for execution: reading and "
            f"executing the registered {REGISTERED_SOURCE_NAME} needs a "
            f"separate read-only execution approval.  {APPROVAL_NOTE}")
    # The approval is for the harness it was given for.  Four rounds of this
    # PREP were harness changes, and each one produced a different oracle; an
    # approval that carried over to whatever the file says today would be an
    # approval of something nobody read.  Binding it to the digest makes the
    # renewal mechanical instead of remembered — and this is a *refusal*, so
    # the failure direction is "ask again", never "run anyway".
    bound = EXECUTION_APPROVAL_RECORD.get("for_oracle_harness_sha256")
    current = str(oracle_harness_identity()["oracle_harness_sha256"])
    if bound != current:
        raise P3NotApprovedError(
            f"the execution approval on record is for oracle harness "
            f"{bound}, and this module's harness is {current}.  The harness "
            f"decides what the run observes, so an approval given for a "
            f"different one is not an approval of this run.  Re-approve "
            f"against the current digest before executing.")
    return dict(EXECUTION_APPROVAL_RECORD)


def _canonical_json(obj: object) -> str:
    return Q5E._canonical_json(obj)


def _sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _is_sha256(value: object) -> bool:
    return Q5E._is_sha256(value)


def canonical_digest(obj: object) -> str:
    """The one digest convention used for every observation in this module."""
    return _sha256_bytes(_canonical_json(obj).encode("utf-8"))


# ─────────────────────────────────────────────────────────────────────────────
# The six registered fixtures.
#
# Names are **imported** from `Q5E.SOURCE_MATCH_REQUIRED_FIXTURES`, never
# retyped, so this list cannot drift from the one the M4.0 sub-gate enforces.
# Each fixture exists to refute one reading of the prose, and the refutation
# target is written beside it: a fixture nobody can say what it would catch is
# decoration.
#
# No fixture records an expected answer.  What the correct answer *is* comes
# from the registered source; writing it here would be the third transcription
# of a rule this PREP exists because we cannot trust ourselves to transcribe.
#
# Construction rules every fixture obeys, checked by `assert_fixture_contract`
# because the trace projection depends on them:
#
#   * every sample — peak or annotation — is >= 100, so no sample can be
#     mistaken for a container index or for a distance;
#   * peak samples and annotation samples are disjoint, so an integer seen in
#     a producer's frame says which side it came from;
#   * peak samples are distinct, and annotation samples are distinct.
# ─────────────────────────────────────────────────────────────────────────────
MIN_FIXTURE_SAMPLE = 100
TOLERANCE = Q5E.M4_PEAK_MATCH_TOLERANCE_SAMPLES              # 54
FIXTURE_FS = 360

# ─────────────────────────────────────────────────────────────────────────────
# Filler beats (added 2026-08-16, D21).
#
# Run `20260816T022702` showed the registered producer running to completion and
# returning `None` while holding one kept beat (`kp == [1000]`), having never
# called the RR stub: it declines to build a record when too few beats survive.
# An RR interval needs two beats, so a producer that computes one has to.  Four
# of the six fixtures, built to isolate a single decision with as few peaks as
# possible, keep fewer than two rows — so as they stood they could not reach
# the comparison at all, whatever the adapter did.
#
# The fix is additive and identical across all six: a run of clean beats, far
# from every decision under test and well inside the boundary, matched at
# distance 1 by an unambiguous AAMI-N annotation.  What each fixture isolates
# is untouched — no filler beat is within `TOLERANCE` of any decision peak or
# annotation, so it cannot become anyone's nearest, be consumed by anyone else,
# or change a tie.  Both sides keep the same filler rows in the same order, so
# the filler adds identical rows to both observations and can only be a
# difference if the two sides genuinely differ on it.
#
# Six of them, spaced 240 samples (a plausible interval at 360 Hz): enough that
# an interior beat has neighbours on both sides for an RR feature, and enough
# margin over a small minimum.  If the registered guard turns out to want more,
# this is the one number to change — and changing it changes the fixture
# digests, so a PASS recorded under the old ones cannot be reused.
# ─────────────────────────────────────────────────────────────────────────────
#: Filler symbols alternate between AAMI classes, and that is load-bearing
#: rather than decorative.  The trace projection reads a consumed integer as
#: either a list position or a sample rank; with filler present those two
#: readings differ by a constant offset, so every peak has two candidate
#: annotations and the producer's own kept row has to settle which.  A row
#: carries its **class**, not its symbol — so six distinct N-class symbols
#: would settle nothing.  Neighbouring filler annotations therefore carry
#: different classes, and the first one is S so that it differs from whichever
#: decision annotation precedes it in every fixture (those are all N or V).
#: All six map to an AAMI class, so every filler beat is kept by both sides.
FILLER_PEAKS: Tuple[int, ...] = (1500, 1740, 1980, 2220, 2460, 2700)
FILLER_SYMBOLS: Tuple[str, ...] = ("A", "L", "J", "R", "a", "e")
FILLER_ANNOTATIONS: Tuple[Tuple[int, str], ...] = tuple(
    (peak + 1, symbol) for peak, symbol in zip(FILLER_PEAKS, FILLER_SYMBOLS))
FILLER_NOTE = (
    "the last six peaks of every fixture are filler: clean AAMI-N beats, "
    "further than the tolerance from every decision peak and annotation, "
    "present because the registered producer declines to build a record from "
    "too few beats.  They are identical in all six fixtures and are kept by "
    "both sides, so they carry no decision of their own")


def _with_filler(peaks: Tuple[int, ...],
                 annotations: Tuple[Tuple[int, str], ...]
                 ) -> Tuple[Tuple[int, ...], Tuple[Tuple[int, str], ...]]:
    """A fixture's own peaks and annotations, followed by the shared filler.

    Appended rather than interleaved: the decision under test stays first in
    traversal order, so a fixture that depends on the order it is traversed in
    still depends on exactly what it did before.
    """
    return tuple(peaks) + tuple(FILLER_PEAKS), \
        tuple(annotations) + tuple(FILLER_ANNOTATIONS)


FIXTURES: Tuple[Dict[str, object], ...] = (
    {
        "name": "test_source_match_nearest_already_used_falls_through",
        "refutes": ("that a peak whose nearest annotation is already consumed "
                    "is dropped.  Peak 1012's nearest is 1001, taken by peak "
                    "1000; falling through keeps it against 1042, dropping "
                    "loses the row entirely"),
        "peaks": _with_filler((1000, 1012), ((1001, "N"), (1042, "V")))[0],
        "annotations": _with_filler((1000, 1012), ((1001, "N"), (1042, "V")))[1],
        "signal_length": 3000,
    },
    {
        "name": "test_source_match_distance_tie_goes_to_the_earlier_annotation",
        "refutes": ("that an exact distance tie goes to the later annotation.  "
                    "Peak 1030 is 30 samples from both 1000 and 1060, and the "
                    "two carry different AAMI classes, so the tie rule is "
                    "visible in the kept row and not only in an index"),
        "peaks": _with_filler((1030,), ((1000, "N"), (1060, "V")))[0],
        "annotations": _with_filler((1030,), ((1000, "N"), (1060, "V")))[1],
        "signal_length": 3000,
    },
    {
        "name": "test_source_match_non_aami_symbol_consumes_its_match",
        "refutes": ("that a non-AAMI annotation is removed from the candidate "
                    "pool before matching.  If '+' at 1001 is filtered out "
                    "first, peak 1000 takes 1042 and peak 1044 is left "
                    "unmatched; if it is consumed and only then dropped, peak "
                    "1044 keeps 1042.  Peak 1044's nearest annotation is 1042 "
                    "either way, so this fixture isolates the filter and does "
                    "not also depend on falling through"),
        "peaks": _with_filler((1000, 1044), ((1001, "+"), (1042, "N")))[0],
        "annotations": _with_filler((1000, 1044), ((1001, "+"), (1042, "N")))[1],
        "signal_length": 3000,
    },
    {
        "name": "test_source_match_boundary_cut_consumes_its_match",
        "refutes": ("that a peak cut by the p-150 boundary releases its "
                    "annotation.  Peak 140 matches 141 and is cut; peak 190 is "
                    "49 samples from 141 and is not cut, so releasing gives it "
                    "that row and consuming leaves it unmatched"),
        "peaks": _with_filler((140, 190), ((141, "N"), (251, "V")))[0],
        "annotations": _with_filler((140, 190), ((141, "N"), (251, "V")))[1],
        "signal_length": 3000,
    },
    {
        "name": "test_source_match_annotation_order_differing_from_sample_order",
        "refutes": ("that annotations are traversed in the order the reader "
                    "returned them.  Listed as [1060, 1000] with peak 1030 "
                    "equidistant, list order takes 1060 and sample order takes "
                    "1000 — different AAMI classes, so the kept row shows it"),
        "peaks": _with_filler((1030,), ((1060, "V"), (1000, "N")))[0],
        "annotations": _with_filler((1030,), ((1060, "V"), (1000, "N")))[1],
        "signal_length": 3000,
    },
    {
        "name": "test_source_match_peak_order_change_is_visible",
        "refutes": ("that peaks may be sorted before matching.  Both peaks "
                    "keep a row either way, so the only thing that moves is "
                    "the order they are written in: detector order gives "
                    "[1035, 1001] and sorting first gives [1001, 1035].  No "
                    "distance here is tied, so this fixture depends on the "
                    "traversal order alone"),
        "peaks": _with_filler((1035, 1001), ((1000, "N"), (1060, "V")))[0],
        "annotations": _with_filler((1035, 1001), ((1000, "N"), (1060, "V")))[1],
        "signal_length": 3000,
    },
)
FIXTURES_BY_NAME: Dict[str, Dict[str, object]] = {
    str(f["name"]): f for f in FIXTURES}
REQUIRED_FIXTURES: Tuple[str, ...] = Q5E.SOURCE_MATCH_REQUIRED_FIXTURES


def fixture_names() -> Tuple[str, ...]:
    return tuple(str(f["name"]) for f in FIXTURES)


def assert_fixture_contract() -> Dict[str, object]:
    """The fixture set is exactly the registered one, and it is well formed.

    Reducing the list, renaming an entry, or adding one after seeing a result
    are the same failure — a differential whose coverage was chosen by its own
    outcome — so the set is pinned against
    `Q5E.SOURCE_MATCH_REQUIRED_FIXTURES` here, before anything is loaded or
    compared, and a violation stops the run rather than shrinking it.
    """
    problems: List[str] = []
    names = fixture_names()
    if list(names) != list(REQUIRED_FIXTURES):
        problems.append(
            f"the fixture set {list(names)} is not the registered required set "
            f"{list(REQUIRED_FIXTURES)}")
    if len(set(names)) != len(names):
        problems.append(f"duplicate fixture names: {sorted(names)}")
    for fixture in FIXTURES:
        name = str(fixture["name"])
        peaks = [int(p) for p in fixture["peaks"]]
        annotations = [(int(s), str(y)) for s, y in fixture["annotations"]]
        samples = [s for s, _ in annotations]
        length = int(fixture["signal_length"])
        if not str(fixture.get("refutes") or "").strip():
            problems.append(f"{name}: no refutation target is recorded")
        if not peaks:
            problems.append(f"{name}: no peaks")
        if not annotations:
            problems.append(f"{name}: no annotations")
        if len(set(peaks)) != len(peaks):
            problems.append(f"{name}: repeated peak samples {peaks}")
        if len(set(samples)) != len(samples):
            problems.append(f"{name}: repeated annotation samples {samples}")
        if set(peaks) & set(samples):
            problems.append(
                f"{name}: a peak sample equals an annotation sample "
                f"{sorted(set(peaks) & set(samples))}; the trace projection "
                f"could not then tell which side an integer came from")
        for value in peaks + samples:
            if value < MIN_FIXTURE_SAMPLE:
                problems.append(
                    f"{name}: sample {value} is below {MIN_FIXTURE_SAMPLE}, so "
                    f"it could be mistaken for an index or a distance")
            if value >= length:
                problems.append(f"{name}: sample {value} is outside the signal")
    if problems:
        raise SourceHarnessError(P3_FIXTURE_CONTRACT_VIOLATION,
                                 "; ".join(problems))
    return {"gate": "fixture_contract", "ok": True, "reason": None,
            "fixtures": list(names),
            "required_fixtures": list(REQUIRED_FIXTURES),
            "n_fixtures": len(names)}


def fixture_card(name: str) -> Dict[str, object]:
    """A fixture as reported: inputs and refutation target, no expectations."""
    fixture = FIXTURES_BY_NAME[name]
    return {"name": name, "refutes": fixture["refutes"],
            "peaks": [int(p) for p in fixture["peaks"]],
            "annotations": [[int(s), str(y)] for s, y in
                            fixture["annotations"]],
            "signal_length": int(fixture["signal_length"]),
            "tolerance": TOLERANCE, "fs": FIXTURE_FS,
            "win_before": BJ.WIN_BEFORE, "win_after": BJ.WIN_AFTER}


# ─────────────────────────────────────────────────────────────────────────────
# Synthetic dependency injection.
#
# Nothing real is read.  The signal is a ramp whose sample *value* equals its
# sample *index*, so any window a producer returns says which peak it was cut
# around; `detect_r` returns the fixture's peaks in the fixture's order; the
# RR/feature producer returns rows whose first column is the peak it was given,
# so returned rows say which peaks survived.  Every stub records what it was
# handed, because those arguments are the producer's own decisions.
# ─────────────────────────────────────────────────────────────────────────────
#: Constants the injected `frontend` stub declares, because the registered
#: source reads them at import time.  The 20260815T232546 run established that
#: `data.py` reads `frontend.FS`; it stopped there rather than guessing, which
#: is what `P3_STUB_SURFACE_INCOMPLETE` is for.
#:
#: `FS` **must** be the registered 360 Hz and not an arbitrary number.  The
#: static source map records that `data.py` computes its tolerance as
#: `int(0.15 * fs)`, and `int(0.15 * 360) == 54 ==
#: M4_PEAK_MATCH_TOLERANCE_SAMPLES` — the registered tolerance the fixtures are
#: built around.  Injecting anything else would silently change the behaviour
#: under test, which is the one thing an injection may never do.  A regression
#: pins the arithmetic rather than the number.
#:
#: `WIN_BEFORE` and `WIN_AFTER` are the beat window, and the 20260816T121935
#: run established that `build_record` reads the first of them from `frontend`
#: rather than defining it.  They are pinned to the frozen Q5-D module's
#: `WIN_BEFORE`/`WIN_AFTER`, which are the registered v10 lineage constants —
#: the same 150/150 the boundary rule `p - 150 >= 0 and p + 150 <= len(x)` is
#: written from, the same pair `stage_decomposition` describes both sides with,
#: and the same pair the candidate adapter applies.  One fixture exists solely
#: to pin that boundary (peak 140 is cut by it), so injecting any other value
#: would move the line the fixture was built to test.
#:
#: Only `WIN_BEFORE` was observed being read.  `WIN_AFTER` is declared beside
#: it because they are one constant in two halves — a window with a start and
#: no end is not a window — and because they carry the *same* justification;
#: declaring the pair costs nothing and a missing half costs a whole run.  The
#: discovery pass cannot settle this on its own: a permissive stand-in answers
#: `WIN_BEFORE`, and what a producer does next with a stand-in is not
#: necessarily what it does with 150.
FRONTEND_STUB_CONSTANTS: Dict[str, object] = {"FS": FIXTURE_FS,
                                              "WIN_BEFORE": BJ.WIN_BEFORE,
                                              "WIN_AFTER": BJ.WIN_AFTER}
#: Helper functions the registered source reaches for, beyond the two the
#: source map names.  The 20260815T235627 run established that `build_record`
#: calls `frontend._z` while running.
#:
#: A constant can be justified by arithmetic; a **function cannot**, and this
#: PREP does not accept "it looked harmless".  So `_z` is injected as the
#: identity — the least-interfering stand-in there is — and its neutrality is
#: **probed on every fixture of every run**: the same fixture is observed again
#: with `_z` replaced by an elementwise negation, and the two observations must
#: be identical.  If a matching decision ever moved with `_z`, the run stops at
#: `P3_INJECTED_VALUE_STEERS_MATCHING` instead of reporting a comparison the
#: injection had a hand in.
#: Helpers the registered producer reaches for whose *shape* this PREP has no
#: registered claim about.  Each is injected as the identity — it hands its
#: argument straight back — and each is probed on every fixture of every run
#: by re-running under an elementwise negation.  `_z` came from the
#: 20260815T235627 run; `stack_ctx` and `slope_channel` from 20260816T131241,
#: where the discovery pass reported both at once.
#:
#: Identity is the only stand-in that needs no claim about what the helper
#: computes, and it keeps the property the whole projection rests on: a window
#: that passes through it still names its own centre sample.
FRONTEND_STUB_FUNCTIONS: Tuple[str, ...] = ("_z", "stack_ctx",
                                            "slope_channel")
STUB_VARIANT_PRIMARY = "identity"
STUB_VARIANT_PROBE = "negated"
STUB_VARIANTS: Tuple[str, ...] = (STUB_VARIANT_PRIMARY, STUB_VARIANT_PROBE)
#: Constants the other stub modules declare.  Empty until a run shows that the
#: registered source reads one, for the same reason: the surface is what the
#: source demonstrably needs, never what it might plausibly want.
WFDB_STUB_CONSTANTS: Dict[str, object] = {}
PWAVE_STUB_CONSTANTS: Dict[str, object] = {}


class StubAttributeMissing(AttributeError):
    """A producer asked an injected stub for an undeclared name.

    An `AttributeError` subclass on purpose: a producer that guards with
    `hasattr()` must see a plain missing attribute, exactly as it would with a
    real module that lacks the name.  A bare access propagates and the harness
    turns it into `P3_STUB_SURFACE_INCOMPLETE`, naming the module and the
    attribute so the next run needs no guesswork.
    """

    def __init__(self, module_name: str, attribute: str) -> None:
        super().__init__(
            f"the injected {module_name!r} stub declares no {attribute!r}")
        self.module_name = module_name
        self.attribute = attribute


class StubCallLog(object):
    """Every call a producer made into an injected dependency, in order."""

    __slots__ = ("calls",)

    def __init__(self) -> None:
        self.calls: List[Dict[str, object]] = []

    def record(self, target: str, **detail: object) -> None:
        self.calls.append({"seq": len(self.calls), "target": target, **detail})

    def by_target(self, target: str) -> List[Dict[str, object]]:
        return [dict(c) for c in self.calls if c["target"] == target]

    def as_list(self) -> List[Dict[str, object]]:
        return [dict(c) for c in self.calls]


def stub_call_summary(log: StubCallLog) -> Dict[str, object]:
    """How often each injected dependency was called, and with how many rows.

    Counts and row counts only — never the values a stub was handed.  It
    belongs beside the return schema for the same reason: when a run stops,
    "the producer asked for peaks twice and never called the RR stub" is the
    difference between one more round trip and none.
    """
    counts: Dict[str, int] = {}
    rows: Dict[str, List[int]] = {}
    for call in log.as_list():
        target = str(call["target"])
        counts[target] = counts.get(target, 0) + 1
        for key in ("given", "returned"):
            value = call.get(key)
            if isinstance(value, (list, tuple)):
                rows.setdefault(f"{target}.{key}", []).append(len(value))
    return {"counts": dict(sorted(counts.items())),
            "input_rows": {k: v for k, v in sorted(rows.items())}}


def _numpy():
    """numpy if it is importable, else None.  Never installed by this module."""
    try:
        import numpy                                         # noqa: PLC0415
        return numpy
    except ImportError:                                      # pragma: no cover
        return None


def make_ramp_signal(length: int, channels: int = 2):
    """`signal[i][c] = i`, so a returned window reveals its own centre.

    A real waveform is never used: this PREP compares control flow, and a
    self-identifying ramp turns "which peak is this row" into an observation
    instead of an inference.
    """
    numpy = _numpy()
    if numpy is not None:
        column = numpy.arange(int(length), dtype="float64")
        return numpy.stack([column] * int(channels), axis=1)
    return [[float(i)] * int(channels) for i in range(int(length))]


class _RecordStub(object):
    """What a WFDB record reader returns, reduced to what a producer reads."""

    def __init__(self, fixture: Mapping[str, object]) -> None:
        length = int(fixture["signal_length"])
        self.p_signal = make_ramp_signal(length)
        self.d_signal = self.p_signal
        self.fs = FIXTURE_FS
        self.sig_len = length
        self.n_sig = 2
        self.sig_name = ["MLII", "V1"]
        self.units = ["mV", "mV"]
        self.record_name = "SYNTHETIC"


class _AnnotationStub(object):
    """What an annotation reader returns, in the fixture's own order."""

    def __init__(self, fixture: Mapping[str, object]) -> None:
        annotations = [(int(s), str(y)) for s, y in fixture["annotations"]]
        numpy = _numpy()
        samples = [s for s, _ in annotations]
        self.sample = (numpy.array(samples, dtype="int64")
                       if numpy is not None else list(samples))
        self.symbol = [y for _, y in annotations]
        self.aux_note = ["" for _ in annotations]
        self.fs = FIXTURE_FS
        self.ann_len = len(annotations)
        self.record_name = "SYNTHETIC"


def _elementwise(value: object, transform):
    """Apply `transform` to every number in a signal-shaped value.

    Works on a numpy array, a list of rows or a flat list, and returns the
    value unchanged when it is none of those — a probe that cannot perturb an
    input reports that it could not, rather than pretending it did.
    """
    numpy = _numpy()
    if numpy is not None and isinstance(value, numpy.ndarray):
        return transform(value)
    if isinstance(value, (list, tuple)):
        out = []
        for item in value:
            if isinstance(item, (list, tuple)):
                out.append([transform(v) for v in item])
            elif isinstance(item, (int, float)) and not isinstance(item, bool):
                out.append(transform(item))
            else:
                return value
        return out
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return transform(value)
    return value


def build_injection(fixture: Mapping[str, object],
                    log: Optional[StubCallLog] = None,
                    variant: str = STUB_VARIANT_PRIMARY,
                    permissive: bool = False,
                    unpack_arity: int = 0
                    ) -> Tuple[Dict[str, object], StubCallLog]:
    """The stub surface a producer may reach, and the log of what it reached.

    Returned as a mapping from *name* to object rather than as a module, so the
    same stubs can be installed as `sys.modules` entries and patched over
    module globals — a producer may write `import wfdb`, `from .frontend
    import detect_r` or `import frontend as FE`, and none of those forms may
    reach a real dependency.
    """
    log = log if log is not None else StubCallLog()
    peaks = [int(p) for p in fixture["peaks"]]

    def rdrecord(*args: object, **kwargs: object):
        log.record("wfdb.rdrecord", n_args=len(args), kwargs=sorted(kwargs))
        return _RecordStub(fixture)

    def rdann(*args: object, **kwargs: object):
        log.record("wfdb.rdann", n_args=len(args), kwargs=sorted(kwargs))
        return _AnnotationStub(fixture)

    def rdsamp(*args: object, **kwargs: object):
        log.record("wfdb.rdsamp", n_args=len(args), kwargs=sorted(kwargs))
        stub = _RecordStub(fixture)
        return stub.p_signal, {"fs": FIXTURE_FS, "sig_len": stub.sig_len}

    def dl_database(*args: object, **kwargs: object):
        raise P3Error(
            "refusing to download a database: this PREP runs entirely on "
            "synthetic fixtures and never fetches a dataset")

    def detect_r(*args: object, **kwargs: object):
        """The stub standing in for the registered detector.

        The real `detect_r()` is never called — not here and not on any code
        path in this module.  The fixture's peaks come back in the fixture's
        own order, because that order is one of the things under test.
        """
        log.record("frontend.detect_r", n_args=len(args), kwargs=sorted(kwargs),
                   returned=list(peaks))
        numpy = _numpy()
        return (numpy.array(peaks, dtype="int64") if numpy is not None
                else list(peaks))

    def _peak_argument(args: Sequence[object]) -> List[int]:
        for argument in args:
            try:
                values = [int(v) for v in argument]          # type: ignore[arg-type]
            except (TypeError, ValueError):
                continue
            if values and all(v in set(peaks) for v in values):
                return values
        return []

    def _peaks_from_windows(args: Sequence[object]) -> List[int]:
        """Peaks recovered from a block of beat windows, or `[]`.

        A producer does not have to hand a helper the peaks: the
        20260816T131241 run showed `compare_features` being called without
        them, and a stub that answers such a call with **no rows** puts a
        column of a different length into the record — which the reader would
        then, correctly, refuse.

        The windows say it themselves.  The injected signal is a ramp, so
        `signal[i] == i` and a stored window's centre sample *is* the peak it
        was cut around; that is the same declared property the beat
        cross-check channel reads.  Either sign is accepted because the
        declared helpers (`_z` and the identity helpers beside it) may be
        applied to a window more than once, and a sign cannot change which row
        is which.
        """
        for argument in args:
            rows = _numeric_rows(argument)
            if not rows or len(rows[0]) != BJ.WIN_BEFORE + BJ.WIN_AFTER:
                continue
            centres = [row[BJ.WIN_BEFORE] for row in rows]
            for sign in (1.0, -1.0):
                values = [sign * c for c in centres]
                if all(float(v) == int(v) and int(v) in set(peaks)
                       for v in values):
                    return [int(v) for v in values]
        return []

    def rr_features(*args: object, **kwargs: object):
        """RR/feature producer stub.  Row `j` is `[peak_j, j, 0, 0, 0, 0, 0]`.

        The first column carries the peak the row was built for, so the rows a
        producer keeps say which peaks it kept — an observation, not an
        inference from counts.
        """
        given = _peak_argument(args)
        log.record("frontend.rr_features", given=list(given), n_args=len(args),
                   kwargs=sorted(kwargs))
        rows = [[float(p), float(j)] + [0.0] * (BJ.CACHE_RR_DIM - 2)
                for j, p in enumerate(given)]
        numpy = _numpy()
        return (numpy.array(rows, dtype="float64") if numpy is not None
                else rows)

    def pwave_features(*args: object, **kwargs: object):
        """V10's P-wave add-on.  Same row convention, so it is observable too."""
        given = _peak_argument(args) or _peaks_from_windows(args)
        log.record("pwave.pwave_features", given=list(given), n_args=len(args),
                   kwargs=sorted(kwargs))
        rows = [[float(p)] + [0.0] * 4 for p in given]
        numpy = _numpy()
        return (numpy.array(rows, dtype="float64") if numpy is not None
                else rows)

    def compare_features(*args: object, **kwargs: object):
        """The producer of the record's `ref` and `sim` columns.

        Run `20260816T125027` established two things at once: `build_record`
        reads `frontend.compare_features`, and it **unpacks the result into
        two** — the discovery pass got `ValueError: not enough values to
        unpack (expected 2, got 0)`.  Two blocks beside `beat`, and V10's
        registered `ARMS` carries a `compare` arm, so this is the pair the
        cache calls `ref` and `sim`.

        Both come back under the same row convention as every other feature
        producer: one row per peak handed in, that peak in the first column.
        The arity is not a guess — it is what the producer itself demanded.
        """
        given = _peak_argument(args) or _peaks_from_windows(args)
        log.record("frontend.compare_features", given=list(given),
                   n_args=len(args), kwargs=sorted(kwargs))
        rows = [[float(p)] + [0.0] * 4 for p in given]
        numpy = _numpy()
        block = (numpy.array(rows, dtype="float64") if numpy is not None
                 else rows)
        second = (numpy.array(rows, dtype="float64") if numpy is not None
                  else [list(row) for row in rows])
        return block, second

    def beat_ctx(*args: object, **kwargs: object):
        """The producer of the record's `ctx` column.

        Run `20260816T031420` got past the beat-count guard and stopped here:
        `build_record` reads `frontend.beat_ctx` while running.  It is declared
        under the **same row convention** as the other feature producers — one
        row per peak it was handed, that peak in the first column — for the
        same two reasons: the rows stay row-aligned with `rr`, which the
        columnar reader requires of every registered column, and each row says
        which peak it was built for, so nothing has to be inferred from counts.
        Like every injected function its neutrality is probed rather than
        asserted; a matching decision that moved with it would stop the run.
        """
        given = _peak_argument(args) or _peaks_from_windows(args)
        log.record("frontend.beat_ctx", given=list(given), n_args=len(args),
                   kwargs=sorted(kwargs))
        rows = [[float(p)] + [0.0] * 4 for p in given]
        numpy = _numpy()
        return (numpy.array(rows, dtype="float64") if numpy is not None
                else rows)

    if variant not in STUB_VARIANTS:
        raise P3Error(
            f"{variant!r} is not one of the declared stub variants "
            f"{list(STUB_VARIANTS)}; a run may not invent a third injection")

    def _identity_helper(name: str):
        """A declared helper stand-in, and the probe that tests it.

        `identity` hands the value straight back — the least-interfering thing
        a stand-in can do, and the only one that needs no claim about what the
        helper computes.  `negated` returns it elementwise negated, and exists
        so a run can *demonstrate* that no matching decision moved with the
        helper rather than assume so.

        Echoing the argument also preserves the one property this PREP relies
        on: the injected signal is a ramp, so a window that passes through an
        identity helper still names its own centre sample.
        """
        def helper(value: object = None, *args: object, **kwargs: object):
            log.record(f"frontend.{name}", variant=variant,
                       n_args=1 + len(args), kwargs=sorted(kwargs))
            if variant == STUB_VARIANT_PROBE:
                return _elementwise(value, lambda v: -v)
            return value

        helper.__name__ = name
        return helper

    def missing_attribute(module_name: str):
        """What an injected module does when asked for an undeclared name.

        It records the request — so the bundle says exactly what the producer
        wanted — and then refuses.  Returning a mock instead would let an
        unknown dependency slip into the run wearing a stub's name, which is
        the whole thing the injection exists to prevent.

        The one exception is a **surface discovery** pass (`permissive`), which
        exists only to list the names a producer would go on to ask for and
        whose result may never become an observation.  It is built as its own
        injection, is never used by `differential_over_fixtures` for a
        comparison, and :func:`discover_stub_surface` is the only caller.
        """
        def __getattr__(name: str):
            log.record(f"{module_name}.__getattr__", requested=name,
                       declared=False, permissive=permissive)
            if permissive:
                import unittest.mock                          # noqa: PLC0415
                stand_in = unittest.mock.MagicMock(
                    name=f"undeclared:{module_name}.{name}")
                if unpack_arity:
                    # A producer that writes `a, b = helper(...)` refuses a
                    # stand-in that unpacks into nothing, and the pass stops
                    # one name early.  The arity is not guessed: it is read
                    # back from the producer's own ValueError and fed in here
                    # on a retry, which is why this is a parameter.
                    stand_in.return_value = tuple(
                        unittest.mock.MagicMock(
                            name=f"undeclared:{module_name}.{name}[{i}]")
                        for i in range(unpack_arity))
                return stand_in
            raise StubAttributeMissing(module_name, name)

        return __getattr__

    return ({"rdrecord": rdrecord, "rdann": rdann, "rdsamp": rdsamp,
             "dl_database": dl_database, "detect_r": detect_r,
             "rr_features": rr_features, "pwave_features": pwave_features,
             "beat_ctx": beat_ctx, "compare_features": compare_features,
             "_variant": variant,
             "_missing_attribute": missing_attribute,
             **{name: _identity_helper(name)
                for name in FRONTEND_STUB_FUNCTIONS},
             "_constants": {"wfdb": dict(WFDB_STUB_CONSTANTS),
                            "frontend": dict(FRONTEND_STUB_CONSTANTS),
                            "pwave": dict(PWAVE_STUB_CONSTANTS)}},
            log)


#: Module-global names a producer might hold its injected dependencies under.
#: Rebound after execution as well as before, so `import wfdb` and `from
#: .frontend import detect_r` are both covered.
INJECTED_GLOBALS: Tuple[str, ...] = (
    ("detect_r", "rr_features", "pwave_features", "beat_ctx",
     "compare_features") + FRONTEND_STUB_FUNCTIONS)
INJECTED_MODULE_NAMES: Tuple[str, ...] = (
    "wfdb", "frontend", "pwave", REGISTERED_SOURCE_PACKAGE,
    f"{REGISTERED_SOURCE_PACKAGE}.frontend",
    f"{REGISTERED_SOURCE_PACKAGE}.pwave")


class InjectedModules(object):
    """Install stub modules for the load, and put `sys.modules` back after.

    The stubs live only for the duration of the load; nothing is left behind
    that could make a later import silently resolve to a fake.
    """

    __slots__ = ("stubs", "_saved")

    def __init__(self, stubs: Mapping[str, object]) -> None:
        self.stubs = dict(stubs)
        self._saved: Dict[str, object] = {}

    @staticmethod
    def _module(name: str, attributes: Mapping[str, object]
                ) -> types.ModuleType:
        module = types.ModuleType(name)
        for key, value in attributes.items():
            setattr(module, key, value)
        return module

    def _surface(self, name: str, attributes: Mapping[str, object]
                 ) -> types.ModuleType:
        """One stub module: its declared surface, and a refusal for the rest.

        The declared constants come from the module-level plan, and anything
        else raises :class:`StubAttributeMissing` through PEP 562's module
        `__getattr__` — recorded first, so a stop names what was wanted.
        """
        declared = dict(attributes)
        declared.update(self.stubs["_constants"].get(name, {}))
        module = self._module(name, declared)
        module.__getattr__ = self.stubs["_missing_attribute"](name)
        return module

    def __enter__(self) -> "InjectedModules":
        wfdb = self._surface("wfdb", {
            k: self.stubs[k]
            for k in ("rdrecord", "rdann", "rdsamp", "dl_database")})
        frontend_surface = {"detect_r": self.stubs["detect_r"],
                            "rr_features": self.stubs["rr_features"],
                            "beat_ctx": self.stubs["beat_ctx"],
                            "compare_features":
                                self.stubs["compare_features"]}
        frontend_surface.update({name: self.stubs[name]
                                 for name in FRONTEND_STUB_FUNCTIONS})
        frontend = self._surface("frontend", frontend_surface)
        pwave = self._surface("pwave",
                              {"pwave_features": self.stubs["pwave_features"]})
        package = self._module(REGISTERED_SOURCE_PACKAGE, {})
        package.__path__ = []                                # type: ignore[attr-defined]
        setattr(package, "frontend", frontend)
        setattr(package, "pwave", pwave)
        modules = {
            "wfdb": wfdb, "frontend": frontend, "pwave": pwave,
            REGISTERED_SOURCE_PACKAGE: package,
            f"{REGISTERED_SOURCE_PACKAGE}.frontend": frontend,
            f"{REGISTERED_SOURCE_PACKAGE}.pwave": pwave,
        }
        for name, module in modules.items():
            if name in sys.modules:
                self._saved[name] = sys.modules[name]
            sys.modules[name] = module
        return self

    def __exit__(self, *exc: object) -> None:
        for name in INJECTED_MODULE_NAMES:
            if name in self._saved:
                sys.modules[name] = self._saved[name]        # type: ignore[assignment]
            else:
                sys.modules.pop(name, None)
        self._saved.clear()


# ─────────────────────────────────────────────────────────────────────────────
# Permits: who may execute which bytes.
#
# An earlier version took `(body, expected_sha256, approval)` and executed
# whatever it was handed.  A public token string was then the only thing
# between a caller and compiling the registered source with both barriers
# closed, because the guard lived in `run_p3()` and nothing below re-checked
# it.  Bytes are now executed only through a **permit**, and there are exactly
# two kinds:
#
# * `RegisteredSourcePermit` — minted only inside `fetch_registered_source()`,
#   with a module-private key, after the terminal guard, the file-id gate and
#   the digest gate.  Its constructor re-checks the approval and the guard, so
#   even a caller holding the key gets nothing while a barrier is closed.
# * `SyntheticSourcePermit` — for a producer written by a test or a notebook
#   fixture.  It **refuses bytes whose digest is the registered `data.py`**, so
#   the synthetic route is structurally incapable of running the registered
#   source, whatever approval the caller has.
#
# Nothing else can produce a permit, and nothing without one is compiled.
# ─────────────────────────────────────────────────────────────────────────────
# Sealing, and why a permit is not just a record
# ---------------------------------------------
# A first version of this made the permit a plain object: the base class was
# constructible, its slots were writable, and the callers checked
# `isinstance`.  That left a third kind of permit anyone could build — hand
# construct the base class, set `kind = "synthetic"` and `body` to the
# registered bytes, and both the guard re-check (skipped, because the object
# is not a `RegisteredSourcePermit`) and the digest refusal (skipped, because
# no constructor ran) were simply absent.  A legitimately minted synthetic
# permit could be edited afterwards to the same effect.
#
# So a permit is now a **sealed snapshot of exactly two types**:
#
# * the base class cannot be instantiated and cannot be subclassed further;
# * fields cannot be set or deleted after minting, and the inventory is handed
#   out as a read-only mapping;
# * execution accepts `type(permit)` being one of the two, by identity, never
#   `isinstance` — a subclass is not one of them;
# * and every claim the permit makes is **re-derived from its own bytes
#   immediately before the compiler is reached**, not merely checked when it
#   was minted.  A permit is evidence, not an assertion.
_REGISTERED_PERMIT_KEY = object()
_PERMIT_CONSTRUCTION_KEY = object()
PERMIT_KIND_REGISTERED = "registered"
PERMIT_KIND_SYNTHETIC = "synthetic"


class SourcePermit(object):
    """Permission to execute one producer's bytes, and the rules it carries.

    Not constructible, not subclassable beyond the two kinds below, and not
    editable once minted.
    """

    __slots__ = ("kind", "sha256", "body", "inventory", "synthetic", "label",
                 "approval", "_sealed")
    #: Filled once, immediately after the two concrete permits are defined.
    #: While it is empty the module is still defining them; afterwards, any
    #: further subclass is refused at class-creation time.
    _PERMIT_TYPES: Tuple[type, ...] = ()

    def __init_subclass__(cls, **kwargs: object) -> None:
        super().__init_subclass__(**kwargs)
        if SourcePermit._PERMIT_TYPES:
            raise P3NotApprovedError(
                f"refusing to define {cls.__name__}: there are exactly two "
                f"kinds of source permit, and a third would be a rule nobody "
                f"reviewed.  {APPROVAL_NOTE}")

    def __init__(self, construction_key: object = None, kind: str = "",
                 body: bytes = b"", inventory: Mapping[str, object] = (),
                 synthetic: bool = False, label: str = "",
                 approval: Optional[str] = None) -> None:
        # Every parameter has a default so that `SourcePermit()` reaches the
        # refusal below and says *why*, rather than dying on a signature and
        # leaving the reader to guess whether the rule exists.
        if construction_key is not _PERMIT_CONSTRUCTION_KEY:
            raise P3NotApprovedError(
                "a SourcePermit is not constructible: it is minted by "
                "fetch_registered_source() or by synthetic_permit(), which are "
                "where the gates live.  Building one directly would be a third "
                f"kind of permit that skipped both.  {APPROVAL_NOTE}")
        if type(self) not in SourcePermit._PERMIT_TYPES:
            raise P3NotApprovedError(
                f"{type(self).__name__} is not one of the two permit types; a "
                f"subclass inherits the name and none of the checks.  "
                f"{APPROVAL_NOTE}")
        object.__setattr__(self, "kind", str(kind))
        object.__setattr__(self, "sha256", _sha256_bytes(body))
        object.__setattr__(self, "body", bytes(body))
        object.__setattr__(self, "inventory",
                           types.MappingProxyType(dict(inventory)))
        object.__setattr__(self, "synthetic", bool(synthetic))
        object.__setattr__(self, "label", str(label))
        object.__setattr__(self, "approval", approval)
        object.__setattr__(self, "_sealed", True)

    def __setattr__(self, name: str, value: object) -> None:
        if getattr(self, "_sealed", False):
            raise P3NotApprovedError(
                f"a source permit is a sealed snapshot; {name!r} cannot be "
                f"changed after it is minted.  Editing one is how a fixture "
                f"permit would become permission to run the registered "
                f"source.  {APPROVAL_NOTE}")
        object.__setattr__(self, name, value)                # pragma: no cover

    def __delattr__(self, name: str) -> None:
        raise P3NotApprovedError(
            f"a source permit is a sealed snapshot; {name!r} cannot be "
            f"removed from it.  {APPROVAL_NOTE}")

    def describe(self) -> Dict[str, object]:
        return {"kind": self.kind, "sha256": self.sha256,
                "synthetic": self.synthetic, "label": self.label,
                "bytes": len(self.body), "sealed": True}


class RegisteredSourcePermit(SourcePermit):
    """Bytes that came from the registered file id and matched its digest.

    Minting one is a privileged act, so it re-runs every check rather than
    trusting the caller that got here: the module-private key, this PREP's own
    approval token, the terminal execution guard, and the digest.  Every one
    of them is checked again before the bytes reach a compiler.
    """

    __slots__ = ()

    def __init__(self, key: object, body: bytes,
                 inventory: Mapping[str, object],
                 approval: Optional[str]) -> None:
        if key is not _REGISTERED_PERMIT_KEY:
            raise P3NotApprovedError(
                "a registered-source permit is minted only by "
                "fetch_registered_source(), after the terminal guard and the "
                "file-id and digest gates.  Constructing one directly is how a "
                f"caller would route around those gates.  {APPROVAL_NOTE}")
        require_execution_approval(
            approval, f"executing the registered {REGISTERED_SOURCE_NAME}")
        _terminal_execution_guard()
        digest = _sha256_bytes(body)
        if digest != REGISTERED_SOURCE_SHA256:
            raise SourceHarnessError(
                P3_SOURCE_IDENTITY_MISMATCH,
                f"a registered permit was asked for over bytes hashing to "
                f"{digest}, not the registered {REGISTERED_SOURCE_SHA256}")
        if str(inventory.get("observed_sha256") or "") != digest:
            raise SourceHarnessError(
                P3_SOURCE_IDENTITY_MISMATCH,
                "the inventory does not describe the bytes it was handed")
        assert_registered_provenance(REGISTERED_SOURCE_NAME, inventory, digest,
                                     len(body))
        SourcePermit.__init__(self, _PERMIT_CONSTRUCTION_KEY,
                              PERMIT_KIND_REGISTERED, body, inventory, False,
                              REGISTERED_SOURCE_NAME, approval)


class SyntheticSourcePermit(SourcePermit):
    """Bytes written by a fixture, which are provably not the registered file.

    No approval is required, because nothing registered is reachable through
    it — and that is enforced rather than asserted: bytes whose digest is the
    registered `data.py` are refused here **and again** before execution, so
    this route cannot become a way to run the registered source, by editing
    the permit or by any other means.
    """

    __slots__ = ()

    def __init__(self, body: bytes, label: str = "synthetic.py") -> None:
        digest = _sha256_bytes(body)
        if digest == REGISTERED_SOURCE_SHA256:
            raise P3NotApprovedError(
                "the synthetic route refuses bytes whose digest is the "
                f"registered {REGISTERED_SOURCE_NAME}.  Executing those needs "
                f"the production route, both barriers and the id gate.  "
                f"{APPROVAL_NOTE}")
        SourcePermit.__init__(
            self, _PERMIT_CONSTRUCTION_KEY, PERMIT_KIND_SYNTHETIC, body,
            {"requested_file_id": "<synthetic>", "file_id": "<synthetic>",
             "name": label, "bytes": len(body), "observed_bytes": len(body),
             "observed_sha256": digest,
             "registered_sha256": REGISTERED_SOURCE_SHA256,
             "digest_matches_registered": False, "read": True,
             "synthetic_fixture": True, "problems": [],
             "note": SYNTHETIC_NOTE},
            True, label, None)


#: Closes the type set.  Any further subclass now fails at class creation, and
#: `__init__` refuses anything whose exact type is not one of these two.
SourcePermit._PERMIT_TYPES = (RegisteredSourcePermit, SyntheticSourcePermit)


def synthetic_permit(body: bytes, label: str = "synthetic.py"
                     ) -> SyntheticSourcePermit:
    """The only way to get a permit for bytes that are not the registered file."""
    return SyntheticSourcePermit(body, label=label)


def assert_registered_provenance(label: object,
                                 inventory: Mapping[str, object],
                                 digest: str, observed_bytes: int) -> None:
    """The file-id gate, re-derived from the inventory a permit carries.

    Matching the registered **digest** says the bytes are the right bytes.  It
    does not say where they came from, and this PREP's contract is that the
    oracle runs a file that passed the **file id** gate as well: an arbitrary
    copy of the same content, handed over with a two-field inventory, would
    otherwise be indistinguishable from a read of the registered Drive file.
    That is the difference between "these bytes hash correctly" and "this is
    the registered asset", and P3 exists because the second one is the claim
    that matters.

    So every field `fetch_registered_source()` established is checked again
    here, exactly, on the last line before the compiler.  Booleans are
    compared by identity: `bool("false")` is `True`, and a string that reads
    as a denial must not be taken as an assertion.
    """
    problems: List[str] = []
    if label != REGISTERED_SOURCE_NAME:
        problems.append(f"label {label!r} != {REGISTERED_SOURCE_NAME!r}")
    for field, expected in (("requested_file_id", REGISTERED_SOURCE_FILE_ID),
                            ("file_id", REGISTERED_SOURCE_FILE_ID),
                            ("name", REGISTERED_SOURCE_NAME),
                            ("registered_sha256", digest),
                            ("observed_sha256", digest)):
        if inventory.get(field) != expected:
            problems.append(
                f"{field} {inventory.get(field)!r} != {expected!r}")
    for field in ("bytes", "observed_bytes"):
        if inventory.get(field) != REGISTERED_SOURCE_BYTES:
            problems.append(
                f"{field} {inventory.get(field)!r} != "
                f"{REGISTERED_SOURCE_BYTES}")
    if observed_bytes != REGISTERED_SOURCE_BYTES:
        problems.append(
            f"the permit holds {observed_bytes} bytes where "
            f"{REGISTERED_SOURCE_BYTES} are registered")
    for field, expected in (("digest_matches_registered", True),
                            ("read", True), ("trashed", False),
                            ("is_shortcut", False), ("is_folder", False)):
        if inventory.get(field) is not expected:
            problems.append(
                f"{field} is {inventory.get(field)!r}, not {expected!r}")
    # Exactly an empty list.  Coercing first would have accepted a missing
    # key, a `None` and an empty tuple as "no problems", and those say that
    # the field was never written rather than that the read was clean — a
    # hand-assembled inventory is precisely where that difference matters.
    if inventory.get("problems") != []:
        problems.append(
            f"problems is {inventory.get('problems')!r}, not an empty list; a "
            f"missing or unset field is not a clean read")
    parents = [str(p) for p in (inventory.get("parents") or ())]
    if REGISTERED_SOURCE_FOLDER_ID not in parents:
        problems.append(
            f"parents {parents} do not include the registered folder "
            f"{REGISTERED_SOURCE_FOLDER_ID}")
    if problems:
        raise SourceHarnessError(
            P3_SOURCE_IDENTITY_MISMATCH,
            "the permit's inventory does not show a read of the registered "
            "file id: " + "; ".join(problems) + ".  Bytes with the right "
            "digest are not the registered asset unless they came from the "
            "registered file, and this PREP runs only the registered asset.")


def validate_permit_for_execution(permit: object) -> Dict[str, object]:
    """Re-derive every claim a permit makes, from the bytes it actually holds.

    Called immediately before the compiler, on every route, because "it was
    checked when it was minted" is a statement about the past.  An object that
    never ran a constructor, one whose type merely resembles a permit, or one
    that was edited afterwards all fail here — the digest is recomputed from
    `body`, and the kind, the synthetic flag and the approval must form one of
    exactly two combinations:

    * `registered` — not synthetic, this PREP's own approval token, the
      registered digest, an inventory that describes those same bytes, and the
      terminal guard still open;
    * `synthetic` — synthetic, no approval, and a digest that is **not** the
      registered one.

    Anything else is refused, and refused as an approval failure rather than as
    something about the adapter.
    """
    kind = type(permit)
    if kind not in SourcePermit._PERMIT_TYPES:
        raise P3NotApprovedError(
            f"{getattr(kind, '__name__', kind)!r} is not one of the two source "
            f"permits.  A look-alike, a subclass or a hand-built object is not "
            f"a permit, and this is checked by type identity for exactly that "
            f"reason.  {APPROVAL_NOTE}")
    body = getattr(permit, "body", None)
    if not isinstance(body, bytes):
        raise P3NotApprovedError(
            "the permit carries no bytes to execute; it never completed a "
            f"mint.  {APPROVAL_NOTE}")
    digest = _sha256_bytes(body)
    if digest != getattr(permit, "sha256", None):
        raise P3NotApprovedError(
            f"the permit says its bytes hash to {getattr(permit, 'sha256', None)!r} "
            f"and they hash to {digest}: the body or the digest was changed "
            f"after it was minted.  {APPROVAL_NOTE}")
    inventory = dict(getattr(permit, "inventory", {}) or {})
    approval = getattr(permit, "approval", None)
    if kind is RegisteredSourcePermit:
        if (getattr(permit, "kind", None) != PERMIT_KIND_REGISTERED
                or getattr(permit, "synthetic", None) is not False):
            raise P3NotApprovedError(
                "a registered permit must say so in every field; this one "
                f"does not.  {APPROVAL_NOTE}")
        require_execution_approval(
            approval, f"executing the registered {REGISTERED_SOURCE_NAME}")
        _terminal_execution_guard()
        if digest != REGISTERED_SOURCE_SHA256:
            raise SourceHarnessError(
                P3_SOURCE_IDENTITY_MISMATCH,
                f"a registered permit holds bytes hashing to {digest}, not the "
                f"registered {REGISTERED_SOURCE_SHA256}")
        assert_registered_provenance(getattr(permit, "label", None), inventory,
                                     digest, len(body))
    else:
        if (getattr(permit, "kind", None) != PERMIT_KIND_SYNTHETIC
                or getattr(permit, "synthetic", None) is not True):
            raise P3NotApprovedError(
                "a synthetic permit must say so in every field; this one does "
                f"not.  {APPROVAL_NOTE}")
        if approval is not None:
            raise P3NotApprovedError(
                "a synthetic permit carries no approval, because it opens "
                f"nothing that needs one.  {APPROVAL_NOTE}")
        if digest == REGISTERED_SOURCE_SHA256:
            raise P3NotApprovedError(
                "a synthetic permit holds the registered "
                f"{REGISTERED_SOURCE_NAME} bytes.  The synthetic route never "
                f"executes those, however the permit was obtained.  "
                f"{APPROVAL_NOTE}")
        if inventory.get("digest_matches_registered") is not False:
            raise P3NotApprovedError(
                "a synthetic permit's inventory claims to describe the "
                f"registered file.  {APPROVAL_NOTE}")
    return {"kind": permit.kind, "sha256": digest,
            "synthetic": bool(permit.synthetic), "revalidated": True}


def _compile_and_exec(body: bytes, label: str,
                      namespace: Dict[str, object]) -> None:
    """The single place this module compiles or executes producer bytes.

    One choke point on purpose: a test can count calls to it and show that a
    refused route reached zero of them, which "we checked the arguments" could
    never demonstrate.
    """
    try:
        code = compile(body, label, "exec")
    except SyntaxError as error:
        raise SourceHarnessError(
            P3_SOURCE_UNLOADABLE,
            f"the source did not compile: {error!r}.  That is a load failure, "
            f"not a disagreement with the adapter.") from error
    try:
        exec(code, namespace)                                # noqa: S102
    except StubAttributeMissing as error:
        raise SourceHarnessError(
            P3_STUB_SURFACE_INCOMPLETE,
            f"at import time the source read {error.attribute!r} from the "
            f"injected {error.module_name!r} stub, which does not declare it.  "
            f"That is this harness's injection surface being incomplete, not "
            f"the source being broken and not a disagreement with the "
            f"adapter: declare the name deliberately, with a value that "
            f"cannot change the behaviour under test, and re-run every "
            f"fixture.") from error
    except Exception as error:                               # noqa: BLE001
        raise SourceHarnessError(
            P3_SOURCE_UNLOADABLE,
            f"the source raised while executing at import time: "
            f"{type(error).__name__}: {error}.  That is a load failure, not a "
            f"disagreement with the adapter.") from error


def load_source_under_injection(permit: SourcePermit,
                                stubs: Mapping[str, object]
                                ) -> types.ModuleType:
    """Execute a permitted producer in an isolated namespace.

    **Must be called with the stub modules already installed** — see
    :class:`ProducerSession`, which is the only caller.  The module is built by
    hand rather than imported from a path: it never joins `sys.modules` under
    its own name, so nothing else in the process can pick it up, and the stub
    package is what a relative import resolves through.
    """
    # Everything the permit claims is re-derived here, from the bytes it
    # actually holds, on the last line before the compiler.  Checking at mint
    # time only says what was true then; this is what is true now.
    validate_permit_for_execution(permit)
    installed = sys.modules.get("wfdb")
    frontend = sys.modules.get(f"{REGISTERED_SOURCE_PACKAGE}.frontend")
    if (getattr(installed, "rdrecord", None) is not stubs["rdrecord"]
            or getattr(frontend, "detect_r", None) is not stubs["detect_r"]):
        raise P3Error(
            "refusing to execute a producer without its injected dependencies "
            "installed in sys.modules: a module-level or function-level import "
            "would then reach a real package, or the real detector.  Use "
            "ProducerSession, which holds the injection open across the load "
            "*and* every call.")
    module = types.ModuleType(f"{REGISTERED_SOURCE_PACKAGE}.data")
    module.__file__ = permit.label
    module.__package__ = REGISTERED_SOURCE_PACKAGE
    _compile_and_exec(permit.body, permit.label, module.__dict__)
    # Module-level `import wfdb` already bound the stub; this covers the
    # `from ... import detect_r` forms, where the name is a module global.
    for attribute in INJECTED_GLOBALS:
        if attribute in module.__dict__:
            module.__dict__[attribute] = stubs[attribute]
    if not hasattr(module, REGISTERED_SOURCE_FUNCTION):
        raise SourceHarnessError(
            P3_SOURCE_UNLOADABLE,
            f"the loaded source has no {REGISTERED_SOURCE_FUNCTION}(); the "
            f"file whose digest matched is not the producer this PREP "
            f"compares against")
    return module


class ProducerSession(object):
    """A loaded producer, held **with its stub modules still installed**.

    The injection has to outlive the load.  An earlier version closed it as
    soon as the module had been executed, which covered module-level imports
    and nothing else: a `build_record` containing `import wfdb` or `from
    .frontend import detect_r` in its own body would have resolved those names
    at call time, when `sys.modules` had already been put back — and reached
    the real package, or the real detector, in the middle of a run whose whole
    claim is that it reached neither.

    So the session spans compile, exec, **and every call**, and the caller can
    only get the producer inside a `with` block.
    """

    __slots__ = ("permit", "fixture", "variant", "permissive", "unpack_arity",
                 "stubs", "log", "_injection", "_module")

    def __init__(self, permit: SourcePermit,
                 fixture: Mapping[str, object],
                 variant: str = STUB_VARIANT_PRIMARY,
                 permissive: bool = False,
                 unpack_arity: int = 0) -> None:
        self.permit = permit
        self.fixture = fixture
        self.variant = variant
        self.permissive = permissive
        self.unpack_arity = unpack_arity
        self.stubs: Dict[str, object] = {}
        self.log = StubCallLog()
        self._injection: Optional[InjectedModules] = None
        self._module: Optional[types.ModuleType] = None

    def __enter__(self) -> Tuple[Callable, StubCallLog]:
        self.stubs, self.log = build_injection(self.fixture,
                                               variant=self.variant,
                                               permissive=self.permissive,
                                               unpack_arity=self.unpack_arity)
        self._injection = InjectedModules(self.stubs)
        self._injection.__enter__()
        try:
            self._module = load_source_under_injection(self.permit, self.stubs)
        except BaseException:
            self._injection.__exit__(None, None, None)
            self._injection = None
            raise
        return (getattr(self._module, REGISTERED_SOURCE_FUNCTION), self.log)

    def __exit__(self, *exc: object) -> None:
        if self._injection is not None:
            self._injection.__exit__(*exc)
            self._injection = None
        self._module = None


def source_factory(permit: SourcePermit) -> Callable:
    """A per-fixture session opener: fresh namespace, fresh stubs, every time.

    The stubs *are* the fixture, so each fixture needs its own load.  Doing it
    this way also means module-level state in the producer cannot leak from one
    fixture into the next, which would make a later observation depend on an
    earlier one.
    """
    # Validated here as well as before the compiler: a caller that cannot open
    # a session at all is a clearer failure than one that opens six and is
    # refused inside each.  Neither check replaces the other.
    validate_permit_for_execution(permit)

    def open_producer(fixture: Mapping[str, object],
                      variant: str = STUB_VARIANT_PRIMARY,
                      permissive: bool = False,
                      unpack_arity: int = 0) -> ProducerSession:
        return ProducerSession(permit, fixture, variant=variant,
                               permissive=permissive,
                               unpack_arity=unpack_arity)

    return open_producer


# ─────────────────────────────────────────────────────────────────────────────
# Argument binding.
#
# `build_record`'s signature is not known to this repository — `data.py` is a
# registered Drive asset this PR may not open — so the call is bound by a
# declared plan over parameter *names*, and a parameter the plan cannot bind
# stops the run instead of being guessed.  The plan is recorded in the bundle,
# so a reviewer sees exactly what each parameter received.
# ─────────────────────────────────────────────────────────────────────────────
BINDING_PLAN: Tuple[Tuple[Tuple[str, ...], str], ...] = (
    (("rec", "record", "record_name", "name", "r"), "record_name"),
    (("ddir", "dir", "data_dir", "datadir", "path", "root", "db_dir"),
     "data_dir"),
    (("fs", "sampling_rate", "rate"), "fs"),
    # The 20260815T233808 run established that the registered `build_record`
    # is handed its inputs rather than reading them: its required parameters
    # are `sig`, `ann_sample` and `ann_symbol`.  That makes the fixture's data
    # an **argument**, which is a more direct injection than a reader stub —
    # and the values below are the very same objects the stub readers hand
    # back, so a producer that uses either route sees one world.
    (("sig", "signal", "x", "p_signal", "record_signal"), "signal"),
    (("ann_sample", "ann_samples", "samples", "sample", "ann_idx"),
     "annotation_samples"),
    (("ann_symbol", "ann_symbols", "symbols", "symbol", "sym"),
     "annotation_symbols"),
    (("use_detected", "detected", "use_detect"), "use_detected"),
    (("split", "which"), "split"),
    (("win_before", "before"), "win_before"),
    (("win_after", "after"), "win_after"),
)
#: What each plan key is worth, and why it cannot change the behaviour under
#: test.  Recorded rather than only computed, because a reviewer's question
#: about an injected argument is always "why that value".
BINDING_RATIONALE: Dict[str, str] = {
    "record_name": "a name, never a path to anything real",
    "data_dir": "a placeholder; nothing is read from a directory",
    "fs": (f"the registered {FIXTURE_FS} Hz, so the source's own "
           f"int(0.15 * fs) lands on the registered "
           f"{Q5E.M4_PEAK_MATCH_TOLERANCE_SAMPLES}-sample tolerance"),
    "signal": ("the fixture's ramp signal, identical to what the injected "
               "reader returns; its length is the boundary the cut uses"),
    "annotation_samples": ("the fixture's annotation samples, in the "
                           "fixture's own order — the order is under test"),
    "annotation_symbols": ("the fixture's symbols, in the same order as the "
                           "samples"),
    "use_detected": ("True: the registered rows come from detector order, "
                     "which is what the fixtures pin"),
    "split": "a label; no split is opened",
    "win_before": f"the frozen {BJ.WIN_BEFORE}-sample window",
    "win_after": f"the frozen {BJ.WIN_AFTER}-sample window",
}


def binding_values(fixture: Mapping[str, object]) -> Dict[str, object]:
    """The value each plan key takes for one fixture.

    Fixture-dependent by necessity: a producer that receives its signal and
    annotations as arguments must receive *this* fixture's, and they are built
    the same way the injected readers build theirs so the two routes cannot
    disagree.
    """
    annotations = [(int(s), str(y)) for s, y in fixture["annotations"]]
    numpy = _numpy()
    samples = [s for s, _ in annotations]
    return {
        "record_name": "SYNTHETIC",
        "data_dir": "<synthetic>",
        "fs": FIXTURE_FS,
        "signal": make_ramp_signal(int(fixture["signal_length"])),
        "annotation_samples": (numpy.array(samples, dtype="int64")
                               if numpy is not None else list(samples)),
        "annotation_symbols": [y for _, y in annotations],
        "use_detected": True,
        "split": "DS1",
        "win_before": BJ.WIN_BEFORE,
        "win_after": BJ.WIN_AFTER,
    }


def _describe_binding(key: str, value: object) -> str:
    """A short description of an injected argument, for the bundle.

    The signal is three thousand samples long; its `repr` in a result file
    would bury the plan it is meant to document.
    """
    length = getattr(value, "shape", None) or (
        len(value) if isinstance(value, (list, tuple)) else None)
    if length is not None:
        return f"{key}: {type(value).__name__} of {length}"
    return f"{key}: {value!r}"


def bind_source_arguments(function: Callable,
                          fixture: Mapping[str, object]) -> Dict[str, object]:
    """Bind the producer's parameters from the declared plan, or stop.

    Nothing is invented: a parameter is bound when its name matches the plan or
    when it has a default of its own, and anything else raises
    `P3_SOURCE_SIGNATURE_UNBINDABLE` — a harness stop, never a verdict about
    the adapter.

    The stop names the **whole signature**, not only what went unbound.  The
    20260815T233808 run had to be reopened to find out what `build_record`
    actually takes; a stop that says what it saw makes the next gap a single
    run rather than a round trip.
    """
    import inspect                                           # noqa: PLC0415
    try:
        signature = inspect.signature(function)
    except (TypeError, ValueError) as error:                 # pragma: no cover
        raise SourceHarnessError(
            P3_SOURCE_SIGNATURE_UNBINDABLE,
            f"the signature of {getattr(function, '__name__', '?')} could not "
            f"be read: {error}") from error
    values = binding_values(fixture)
    bound: Dict[str, object] = {}
    plan: List[Dict[str, object]] = []
    unbound: List[str] = []
    for name, parameter in signature.parameters.items():
        if parameter.kind in (parameter.VAR_POSITIONAL, parameter.VAR_KEYWORD):
            plan.append({"parameter": name, "bound_from": "variadic_skipped"})
            continue
        key = None
        for aliases, value_key in BINDING_PLAN:
            if name.lower() in aliases:
                key = value_key
                break
        if key is not None:
            bound[name] = values[key]
            plan.append({"parameter": name, "bound_from": "plan",
                         "plan_key": key,
                         "value": _describe_binding(key, values[key]),
                         "why": BINDING_RATIONALE[key]})
        elif parameter.default is not parameter.empty:
            plan.append({"parameter": name, "bound_from": "producer_default",
                         "value": repr(parameter.default)})
        else:
            unbound.append(name)
            plan.append({"parameter": name, "bound_from": None})
    if unbound:
        raise SourceHarnessError(
            P3_SOURCE_SIGNATURE_UNBINDABLE,
            f"the producer has required parameters this PREP's declared "
            f"binding plan does not cover: {unbound}.  Its full signature is "
            f"({', '.join(str(p) for p in signature.parameters.values())}), "
            f"and the plan bound {sorted(bound)}.  The plan is extended "
            f"deliberately and re-reviewed, with a stated reason why the value "
            f"cannot change the behaviour under test; a parameter is never "
            f"filled with a guess.")
    return {"kwargs": bound, "plan": plan,
            "parameters": [str(p) for p in signature.parameters.values()]}


# ─────────────────────────────────────────────────────────────────────────────
# Mechanical capture: a line trace over exactly one code object.
#
# Nothing here knows what a variable means, and no name from the registered
# source is special-cased.  The projection below works from structure.
# ─────────────────────────────────────────────────────────────────────────────
MAX_TRACE_STEPS = 200000
#: Containers longer than this are summarised rather than expanded.  A
#: producer holds the whole signal in a local, and canonicalising a
#: hundred-thousand-sample array at every line event would make the trace cost
#: more than the run — while a decision this projection can read is always a
#: handful of members.
MAX_CONTAINER = 512
#: The returned object is canonicalised **once** per fixture, not at every
#: line event, so it can be read whole.  A producer that hands back long rows
#: must still be readable: summarising its output would turn "we could not
#: read it" into a fact about the harness rather than about the producer.
RETURN_MAX_CONTAINER = 65536
MAX_DEPTH = 4


def canonical_value(value: object, depth: int = 0,
                    limit: int = MAX_CONTAINER) -> object:
    """A JSON-safe view of one local, or a description of why it is not one.

    Values that cannot be represented are summarised by type and length rather
    than coerced: an unrepresentable local must not silently become `null` and
    then compare equal to a different unrepresentable local.
    """
    if value is None or isinstance(value, (bool, int, str)):
        return value
    if isinstance(value, float):
        return round(value, 9)
    if depth >= MAX_DEPTH:
        return {"__type__": type(value).__name__, "__elided__": True}
    try:
        oversized = len(value) > limit                        # type: ignore[arg-type]
    except TypeError:
        oversized = False
    if oversized:
        # Checked before any conversion: `tolist()` on a large array would
        # materialise the whole thing only to have it summarised anyway.
        return {"__type__": type(value).__name__, "__len__": len(value)}  # type: ignore[arg-type]
    tolist = getattr(value, "tolist", None)
    if callable(tolist) and not isinstance(value, (list, tuple, set, dict)):
        try:
            return canonical_value(tolist(), depth, limit)
        except Exception:                                    # noqa: BLE001
            return {"__type__": type(value).__name__}
    if isinstance(value, Mapping):
        if len(value) > limit:                               # pragma: no cover
            return {"__type__": "mapping", "__len__": len(value)}
        try:
            items = sorted(value.items(), key=lambda kv: repr(kv[0]))
        except Exception:                                    # noqa: BLE001
            items = list(value.items())                      # pragma: no cover
        return {"__map__": [[canonical_value(k, depth + 1, limit),
                             canonical_value(v, depth + 1, limit)]
                            for k, v in items]}
    if isinstance(value, (set, frozenset)):
        if len(value) > limit:                               # pragma: no cover
            return {"__type__": "set", "__len__": len(value)}
        try:
            members = sorted(value, key=repr)
        except Exception:                                    # noqa: BLE001
            members = list(value)                            # pragma: no cover
        return {"__set__": [canonical_value(m, depth + 1, limit)
                            for m in members]}
    if isinstance(value, (list, tuple)):
        if len(value) > limit:
            return {"__type__": type(value).__name__, "__len__": len(value)}
        return [canonical_value(m, depth + 1, limit) for m in value]
    return {"__type__": type(value).__name__}


class FrameTrace(object):
    """The record of one call: what its locals did, and what it returned."""

    __slots__ = ("steps", "returned", "truncated", "code_name", "n_steps")

    def __init__(self) -> None:
        self.steps: List[Dict[str, object]] = []
        self.returned: object = None
        self.truncated = False
        self.code_name = ""
        self.n_steps = 0

    def as_dict(self) -> Dict[str, object]:
        return {"code_name": self.code_name, "n_steps": self.n_steps,
                "truncated": self.truncated}


def trace_call(function: Callable, code, kwargs: Mapping[str, object],
               status_on_error: str = P3_SOURCE_RUNTIME_ERROR
               ) -> Tuple[object, FrameTrace]:
    """Call `function`, tracing only frames whose code object is `code`.

    The tracer is scoped by **code object identity**, not by function name, so
    a same-named helper elsewhere is never traced and cannot contribute to the
    observation.  Whatever was tracing before is restored afterwards, including
    when the call raises.
    """
    trace = FrameTrace()
    trace.code_name = getattr(code, "co_name", "")
    previous: Dict[str, object] = {}
    state = {"steps": 0}

    def local_tracer(frame, event, arg):
        if state["steps"] >= MAX_TRACE_STEPS:                # pragma: no cover
            trace.truncated = True
            return None
        if event not in ("line", "return"):
            return local_tracer
        state["steps"] += 1
        changed: Dict[str, object] = {}
        for name, value in list(frame.f_locals.items()):
            canonical = canonical_value(value)
            if name not in previous or previous[name] != canonical:
                previous[name] = canonical
                changed[name] = canonical
        trace.steps.append({"step": state["steps"], "line": frame.f_lineno,
                            "event": event, "changed": changed})
        return local_tracer

    def global_tracer(frame, event, arg):
        if event == "call" and frame.f_code is code:
            return local_tracer
        return None

    saved = sys.gettrace()
    sys.settrace(global_tracer)
    try:
        returned = function(**dict(kwargs))
    except StubAttributeMissing as error:
        raise SourceHarnessError(
            P3_STUB_SURFACE_INCOMPLETE,
            f"while running, the producer read {error.attribute!r} from the "
            f"injected {error.module_name!r} stub, which does not declare it.  "
            f"The injection surface is incomplete; that is not a "
            f"disagreement with the adapter.") from error
    except Exception as error:                               # noqa: BLE001
        raise SourceHarnessError(
            status_on_error,
            f"{getattr(code, 'co_name', '?')} raised {type(error).__name__}: "
            f"{error}.  A producer that fails to run has not disagreed with "
            f"anything.") from error
    finally:
        sys.settrace(saved)
    trace.returned = returned
    trace.n_steps = state["steps"]
    return returned, trace


# ─────────────────────────────────────────────────────────────────────────────
# Projection: turning a trace into decisions.
#
# This is where the two sides are made comparable, and it is deliberately the
# *same* code for both.  Nothing here re-derives the matching rule; it reads
# what happened:
#
#   * a container local that gained exactly one member, having existed before,
#     is a consumption — a container assigned wholesale is not, because a
#     summary computed at the end of a function records no decision;
#   * a list of flags in which exactly one position turned true is the same
#     event under a different data structure;
#   * the integer consumed identifies an annotation by its sample, or by an
#     index whose two readings (list position and sample rank) agree, or — when
#     those readings disagree — by the label the produced row carries;
#   * the peak in scope is the one a scalar local was holding at that step.
#
# Every candidate container is projected, and the implied mappings are merged.
# Agreement is evidence; a contradiction is `P3_SOURCE_TRACE_UNPROJECTABLE`.
# Nothing is guessed, and an unreadable trace is never reported as a
# disagreement.
# ─────────────────────────────────────────────────────────────────────────────
def _annotation_table(fixture: Mapping[str, object]) -> List[Dict[str, object]]:
    annotations = [(int(s), str(y)) for s, y in fixture["annotations"]]
    order = sorted(range(len(annotations)),
                   key=lambda k: (annotations[k][0], k))
    rank_of = {index: rank for rank, index in enumerate(order)}
    return [{"index": index, "sample": sample, "symbol": symbol,
             "aami": BJ.AAMI_SYMBOL_MAP.get(symbol, ""), "rank": rank_of[index]}
            for index, (sample, symbol) in enumerate(annotations)]


def _peak_table(fixture: Mapping[str, object]) -> List[Dict[str, object]]:
    return [{"peak_index": i, "peak_sample": int(p)}
            for i, p in enumerate(fixture["peaks"])]


def _members(value: object) -> Optional[List[object]]:
    """Container members in canonical form, or `None` if it is not a container."""
    if isinstance(value, dict):
        if "__set__" in value:
            return list(value["__set__"])
        if "__map__" in value:
            return [tuple(pair) if isinstance(pair, list) else pair
                    for pair in value["__map__"]]
        return None
    if isinstance(value, list):
        return list(value)
    return None


def _added_once(previous: object, current: object) -> List[object]:
    """The single member a container gained, or `[]`.

    Only an **incremental** gain counts.  A container that appears for the
    first time already populated, or that grows by several members at once, is
    a summary rather than a decision — `unmatched = all - used` at the end of a
    function is exactly that, and reading it as a consumption would invent
    events that never happened.
    """
    if previous is None:
        return []
    before = _members(previous)
    after = _members(current)
    if before is None or after is None:
        return []
    if len(after) != len(before) + 1:
        return []
    remaining = list(before)
    added: List[object] = []
    for item in after:
        key = json.dumps(item, sort_keys=True, default=repr)
        position = next((i for i, candidate in enumerate(remaining)
                         if json.dumps(candidate, sort_keys=True,
                                       default=repr) == key), None)
        if position is None:
            added.append(item)
        else:
            remaining.pop(position)
    return added if len(added) == 1 else []


def _flipped_once(previous: object, current: object) -> List[object]:
    """The single position of a boolean flag list that turned true, or `[]`.

    `taken[j] = True` consumes an annotation exactly as `used.add(j)` does; it
    just does not change the container's length, so the growth rule alone would
    miss it.  Only genuine booleans count: a numeric row being filled in also
    changes one position from zero to non-zero, and reading that as a
    consumption would invent decisions out of arithmetic.
    """
    if previous is None or not isinstance(previous, list) or \
            not isinstance(current, list) or len(previous) != len(current):
        return []
    changed = [index for index, (before, after)
               in enumerate(zip(previous, current)) if before != after]
    if len(changed) != 1:
        return []
    index = changed[0]
    if previous[index] is False and current[index] is True:
        return [index]
    return []


def _removed_once(previous: object, current: object) -> List[object]:
    """The single member a container gave back, or `[]`.

    Releasing is a decision too, and it is exactly the one the boundary-cut
    fixture exists to pin: a producer that puts an annotation back after
    dropping the peak behaves differently from one that does not, and the
    difference is invisible unless the release is recorded.
    """
    if previous is None:
        return []
    before = _members(previous)
    after = _members(current)
    if before is None or after is None:
        return []
    if len(after) != len(before) - 1:
        return []
    remaining = list(after)
    removed: List[object] = []
    for item in before:
        key = json.dumps(item, sort_keys=True, default=repr)
        position = next((i for i, candidate in enumerate(remaining)
                         if json.dumps(candidate, sort_keys=True,
                                       default=repr) == key), None)
        if position is None:
            removed.append(item)
        else:
            remaining.pop(position)
    return removed if len(removed) == 1 else []


#: How many named locals a stop is allowed to describe.  A cap, not a filter:
#: the names are sorted, so which ones survive does not depend on the run.
STOP_LOCALS_LIMIT = 48
#: How long a list inside one of those locals may be before it is described
#: instead of shown.  A local holding one number per row is the diagnosis —
#: `keep` and `used` are the whole answer — while a local holding a beat window
#: is array contents wearing a local's name, and this file does not publish
#: those.  The bound is on the value, not on which locals are read.
STOP_LOCAL_ITEMS = 16


def _summarise_local(value: object, depth: int = 0) -> object:
    """A canonicalised local, with anything row-shaped left and anything
    signal-shaped described.

    The trace canonicalises locals as it goes, which already turns a numpy
    array into a type and a length.  This is the second bound, for the case the
    first one lets through: a list of windows is short enough to survive
    canonicalisation and long enough, once multiplied out, to put a few
    thousand numbers into a bundle.
    """
    if isinstance(value, list):
        if len(value) > STOP_LOCAL_ITEMS or depth >= 2:
            return {"__type__": "list", "__len__": len(value)}
        return [_summarise_local(item, depth + 1) for item in value]
    if isinstance(value, dict):
        if "__map__" in value:
            pairs = value["__map__"]
            if len(pairs) > STOP_LOCAL_ITEMS or depth >= 2:
                return {"__type__": "mapping", "__len__": len(pairs)}
            return {"__map__": [[k, _summarise_local(v, depth + 1)]
                                for k, v in pairs]}
        if "__set__" in value:
            members = value["__set__"]
            if len(members) > STOP_LOCAL_ITEMS:
                return {"__type__": "set", "__len__": len(members)}
        return value
    return value


def trace_summary(trace: FrameTrace) -> Dict[str, object]:
    """What the traced call did, for a stop that has no comparison to report.

    A stop throws the differential away, and the trace with it — which is
    precisely when the trace is the only thing that can say *why*.  This is the
    reading of it: which line returned, which lines ran, and what each local
    was holding at the end.

    The locals are canonicalised exactly as they are during tracing, so a
    signal or a beat matrix comes out as its type and length rather than as
    numbers.  That is what makes this publishable in a bundle: it says
    `len(keep) == 0`, never what was in the arrays.
    """
    lines: List[int] = []
    finals: Dict[str, object] = {}
    for step in trace.steps:
        lines.append(int(step["line"]))
        finals.update(step["changed"])           # type: ignore[arg-type]
    returns = [int(s["line"]) for s in trace.steps if s["event"] == "return"]
    names = sorted(finals)
    return {
        "code_name": trace.code_name,
        "n_steps": trace.n_steps,
        "truncated": trace.truncated,
        "returned": describe_returned(trace.returned),
        "returned_from_line": (returns[-1] if returns else None),
        "last_line": (lines[-1] if lines else None),
        "distinct_lines_executed": sorted(set(lines)),
        "line_sequence_tail": lines[-40:],
        "n_locals": len(names),
        "final_locals": {name: _summarise_local(finals[name])
                         for name in names[:STOP_LOCALS_LIMIT]},
        "final_locals_truncated": len(names) > STOP_LOCALS_LIMIT,
    }


def growth_events(trace: FrameTrace) -> List[Dict[str, object]]:
    """Every moment a container local recorded one decision, with its scalars."""
    seen: Dict[str, object] = {}
    scalars: Dict[str, int] = {}
    events: List[Dict[str, object]] = []
    for entry in trace.steps:
        changed = dict(entry.get("changed") or {})
        for name, value in changed.items():
            if isinstance(value, int) and not isinstance(value, bool):
                scalars[name] = value
            elif name in scalars:
                scalars.pop(name)
        for name, value in changed.items():
            previous = seen.get(name)
            gained = _added_once(previous, value) or _flipped_once(previous,
                                                                   value)
            released = [] if gained else _removed_once(previous, value)
            seen[name] = value
            for kind, tokens in (("gain", gained), ("release", released)):
                if tokens:
                    events.append({"step": entry["step"],
                                   "line": entry["line"], "container": name,
                                   "kind": kind, "token": tokens[0],
                                   "scalars": dict(scalars)})
    return events


def _resolve_annotation_token(token: object,
                              annotations: Sequence[Mapping[str, object]]
                              ) -> Dict[str, object]:
    """One integer from a trace, read as an annotation — or reported ambiguous.

    Three readings are possible and they are tried in that order: the
    annotation's sample, its position in the reader's list, and its rank in
    sample order.  Fixture construction rules out a sample/index collision, so
    only the last two can disagree — and when they do, this says so rather than
    choosing one.
    """
    if isinstance(token, (list, tuple)) and len(token) == 2:
        token = token[1]
    if not isinstance(token, int) or isinstance(token, bool):
        return {"resolved": None, "ambiguous": False, "candidates": [],
                "reading": "not_an_integer"}
    by_sample = [a for a in annotations if a["sample"] == token]
    if len(by_sample) == 1:
        return {"resolved": by_sample[0]["index"], "ambiguous": False,
                "candidates": [by_sample[0]["index"]], "reading": "sample"}
    by_index = [a for a in annotations if a["index"] == token]
    by_rank = [a for a in annotations if a["rank"] == token]
    if by_index and by_rank:
        if by_index[0]["index"] == by_rank[0]["index"]:
            return {"resolved": by_index[0]["index"], "ambiguous": False,
                    "candidates": [by_index[0]["index"]],
                    "reading": "index_and_rank_agree"}
        return {"resolved": None, "ambiguous": True,
                "candidates": sorted({by_index[0]["index"],
                                      by_rank[0]["index"]}),
                "reading": "index_and_rank_disagree"}
    return {"resolved": None, "ambiguous": False, "candidates": [],
            "reading": "outside_the_annotation_domain"}


def _resolve_peak_in_scope(event: Mapping[str, object],
                           peaks: Sequence[Mapping[str, object]]
                           ) -> Dict[str, object]:
    """Which peak the frame was working on when a container recorded a decision."""
    scalars = dict(event.get("scalars") or {})
    token = event.get("token")
    by_sample = sorted({p["peak_index"] for p in peaks
                        for value in scalars.values()
                        if value == p["peak_sample"]})
    if len(by_sample) == 1:
        return {"peak_index": by_sample[0], "ambiguous": False,
                "reading": "a_scalar_held_this_peak's_sample"}
    if (isinstance(token, (list, tuple)) and len(token) == 2
            and isinstance(token[0], int) and not isinstance(token[0], bool)
            and 0 <= token[0] < len(peaks)):
        return {"peak_index": int(token[0]), "ambiguous": False,
                "reading": "the_mapping_key_is_the_peak_index"}
    by_index = sorted({p["peak_index"] for p in peaks
                       for value in scalars.values()
                       if value == p["peak_index"]})
    if len(by_index) == 1:
        return {"peak_index": by_index[0], "ambiguous": False,
                "reading": "a_scalar_held_this_peak's_index"}
    return {"peak_index": None, "ambiguous": True,
            "candidates": sorted(set(by_sample) | set(by_index)),
            "reading": "no_single_peak_was_in_scope"}


def implied_mappings(trace: FrameTrace, fixture: Mapping[str, object]
                     ) -> Dict[str, object]:
    """One implied peak-to-annotation mapping per candidate container.

    Containers are not filtered by name.  A producer may consume into `used`,
    into a dict, into a flag list or into something nobody anticipated, and the
    projection cannot know which — so every container that behaves like one is
    projected and the results are reconciled afterwards.
    """
    annotations = _annotation_table(fixture)
    peaks = _peak_table(fixture)
    by_container: Dict[str, Dict[str, object]] = {}
    skipped: List[Dict[str, object]] = []
    for event in growth_events(trace):
        annotation = _resolve_annotation_token(event["token"], annotations)
        if annotation["reading"] in ("not_an_integer",
                                     "outside_the_annotation_domain"):
            skipped.append({"container": event["container"],
                            "line": event["line"], "kind": event["kind"],
                            "why": annotation["reading"]})
            continue
        peak = _resolve_peak_in_scope(event, peaks)
        if peak["peak_index"] is None:
            skipped.append({"container": event["container"],
                            "line": event["line"], "kind": event["kind"],
                            "why": peak["reading"]})
            continue
        record = by_container.setdefault(
            event["container"], {"pairs": {}, "releases": [], "problems": []})
        entry = {"peak_index": peak["peak_index"], "step": event["step"],
                 "line": event["line"], "container": event["container"],
                 "reading": annotation["reading"],
                 "annotation_index": annotation["resolved"],
                 "candidates": list(annotation["candidates"])}
        if event["kind"] == "release":
            record["releases"].append(entry)
            continue
        previous = record["pairs"].get(peak["peak_index"])
        if previous is not None and (previous["annotation_index"]
                                     != entry["annotation_index"]
                                     or previous["candidates"]
                                     != entry["candidates"]):
            record["problems"].append(
                f"peak {peak['peak_index']} recorded twice in "
                f"{event['container']!r}")
            continue
        record["pairs"][peak["peak_index"]] = entry
    # A container that never recorded a consumption is not a pool, so its
    # shrinking is somebody else's bookkeeping rather than a release.
    for name, record in by_container.items():
        if not record["pairs"]:
            record["releases"] = []
    return {"by_container": by_container, "skipped": skipped}


def merge_implied(by_container: Mapping[str, Mapping[str, object]],
                  side: str, fixture_name: str, settle=None
                  ) -> Tuple[Dict[int, Dict[str, object]],
                             List[Dict[str, object]]]:
    """Reconcile the containers into one mapping and its releases, or stop.

    Containers that agree corroborate each other.  A disagreement is real work:
    a producer keeps several small-integer collections — an annotation pool, a
    list of kept row positions — and in a fixture where an annotation index and
    a peak index happen to coincide, the row list reads like a consumption.
    That is why a conflict is not resolved by preferring a container: it is put
    to the producer's **own output**, through `settle`, which asks what label
    the row for that peak actually carries.  Only a conflict its own output
    cannot settle is a stop, and a stop is never a disagreement between the two
    sides.
    """
    merged: Dict[int, Dict[str, object]] = {}
    conflicts: Dict[int, Set[int]] = {}
    problems: List[str] = []
    releases: List[Dict[str, object]] = []
    for name in sorted(by_container):
        record = by_container[name]
        problems.extend(str(p) for p in record["problems"])
        releases.extend(dict(entry) for entry in record["releases"])
        for peak_index, entry in sorted(record["pairs"].items()):
            existing = merged.get(peak_index)
            if existing is None:
                merged[peak_index] = dict(entry)
                continue
            if (existing["annotation_index"] is not None
                    and entry["annotation_index"] is not None):
                if existing["annotation_index"] != entry["annotation_index"]:
                    conflicts.setdefault(peak_index, set()).update(
                        {int(existing["annotation_index"]),
                         int(entry["annotation_index"])})
                continue
            if existing["annotation_index"] is None and \
                    entry["annotation_index"] is not None:
                merged[peak_index] = dict(entry)
    for peak_index, candidates in sorted(conflicts.items()):
        chosen = settle(peak_index, sorted(candidates)) if settle else None
        if chosen is None:
            problems.append(
                f"peak {peak_index}: the containers disagree between "
                f"annotations {sorted(candidates)} and the row this producer "
                f"kept for that peak does not settle which it consumed")
            continue
        merged[peak_index] = {**merged[peak_index], "annotation_index": chosen,
                              "candidates": sorted(candidates),
                              "reading": "container_conflict_settled_by_row_label"}
    if problems:
        raise SourceHarnessError(
            P3_SOURCE_TRACE_UNPROJECTABLE,
            f"{side}/{fixture_name}: the execution trace does not read as one "
            f"set of decisions: " + "; ".join(sorted(set(problems))))
    return merged, releases


#: Row fields that name a peak, tried in order.  A row carrying none of them is
#: read through the ramp signal or the RR stub instead.
PEAK_ROW_FIELDS: Tuple[str, ...] = ("r_sample", "peak", "sample", "peak_index")


# ─────────────────────────────────────────────────────────────────────────────
# The registered producer's own return shape: a columnar record.
#
# `build_record()` does not hand back a list of row objects.  It hands back a
# mapping of **columns** — one array per field, all of them row-aligned — which
# is what `prepare()` saves as the record cache.  The generic reader below can
# stumble into such a mapping, but it recognises it by trying things until one
# works, and "whatever channel turned out to be readable" is not a basis for a
# statement about the registered source.  So this schema is read explicitly:
# the keys are checked first, the identity carrier is fixed in advance, and the
# other channels can only refuse the reading — never choose it.
# ─────────────────────────────────────────────────────────────────────────────
#: The columns a built record carries.  Taken from the frozen Q5-D module
#: rather than retyped here: `BJ.CACHE_KEYS` is the registered cache schema and
#: the registered `build_record()` is what writes it, so this list cannot drift
#: away from the thing it claims to describe.
COLUMNAR_RECORD_KEYS: Tuple[str, ...] = tuple(BJ.CACHE_KEYS)

#: The row-identity carrier, fixed **before** any run and for a structural
#: reason rather than a hopeful one: `rr` is built by the injected
#: `rr_features` stub, whose row `j` is `[peak_j, j, 0 …]`.  Its first column is
#: therefore the peak each row was built for *by the injection contract* — not
#: by decoding what the registered source means by "rr".  It is also the one
#: channel that does not move with the `_z` probe, since the stub never sees it.
COLUMNAR_IDENTITY_KEY = "rr"
COLUMNAR_IDENTITY_WIDTH = BJ.CACHE_RR_DIM

#: Independent channels checked **against** the carrier.  `pw` comes from the
#: P-wave stub under the same row convention; `beat` is a window over the ramp
#: signal, whose centre sample is its own index.  Neither can select rows: they
#: can only agree, refuse, or be unavailable, and the last case is recorded.
COLUMNAR_CROSSCHECK_KEYS: Tuple[str, ...] = ("pw", "beat")


def _as_lists(value: object) -> object:
    """An array-like as plain lists, via its own `tolist()`.

    Structural rather than numpy-specific on purpose: this module never
    imports numpy to do its work, the run happens where numpy is installed and
    the tests run where it is not, and an `isinstance(value, ndarray)` branch
    would be exercised in exactly the wrong one of those two places.
    """
    tolist = getattr(value, "tolist", None)
    if callable(tolist) and not isinstance(value, (list, tuple, dict, str,
                                                   bytes)):
        try:
            return tolist()
        except Exception:                                    # noqa: BLE001
            return None
    return value


def _row_width(item: object) -> Optional[int]:
    """How wide one row is, whatever kind of row it is.

    A column can arrive as one two-dimensional block *or* as a list of
    one-dimensional rows — `[rr_all[i] for i in keep]` is the second, and it is
    what the producer writes when it selects rows by index.  Both are the same
    record; a reader that recognised only the first would report a producer
    that plainly returned rows as having returned none.
    """
    shape = getattr(item, "shape", None)
    if isinstance(shape, tuple) and len(shape) == 1:
        return int(shape[0])
    if isinstance(item, (list, tuple)):
        return len(item)
    if isinstance(item, (str, bytes)) or isinstance(item, Mapping):
        return None
    if callable(getattr(item, "tolist", None)) and hasattr(item, "__len__"):
        return len(item)                                     # type: ignore[arg-type]
    return None


def _sequence_shape(value: object) -> Optional[Tuple[int, ...]]:
    """`(rows[, columns])` for an array-like value, or `None`."""
    shape = getattr(value, "shape", None)
    if isinstance(shape, tuple) and all(isinstance(v, int) for v in shape):
        return tuple(int(v) for v in shape)
    value = _as_lists(value)
    if isinstance(value, (list, tuple)):
        widths = [_row_width(item) for item in value]
        if value and all(w is not None for w in widths) \
                and len(set(widths)) == 1:
            return (len(value), int(widths[0]))              # type: ignore[arg-type]
        return (len(value),)
    return None


def _sequence_dtype(value: object) -> Optional[str]:
    """The element type of an array-like, by name.  Never its contents."""
    dtype = getattr(value, "dtype", None)
    if dtype is not None:
        return str(dtype)
    value = _as_lists(value)
    if not isinstance(value, (list, tuple)):
        return None
    kinds = set()
    for item in list(value)[:MAX_CONTAINER]:
        row = _as_lists(item)
        if isinstance(row, (list, tuple)):
            kinds.update(type(v).__name__ for v in list(row)[:8])
        else:
            kinds.add(type(row).__name__)
    return "/".join(sorted(kinds)[:4]) if kinds else "empty"


def _numeric_rows(value: object) -> Optional[List[List[float]]]:
    """A two-dimensional numeric block as plain floats, or `None`.

    `None` means "this is not a numeric block" — a different thing from "this
    block says something unexpected", which is a stop.
    """
    shape = _sequence_shape(value)
    if shape is not None and shape[0] == 0:
        # A column with no rows is a numeric block with no rows.  Reading it as
        # "not a numeric block" would turn a producer that kept nothing into a
        # producer that cannot be read, which are different findings.
        return []
    if shape is None or len(shape) != 2:
        return None
    value = _as_lists(value)
    if not isinstance(value, (list, tuple)):
        return None
    rows: List[List[float]] = []
    for row in value:
        row = _as_lists(row)
        if not isinstance(row, (list, tuple)):
            return None
        out: List[float] = []
        for item in row:
            if isinstance(item, bool) or not isinstance(item, (int, float)):
                return None
            out.append(float(item))
        rows.append(out)
    return rows


def _flat_tokens(value: object, n_rows: int) -> List[str]:
    """A flat per-row column read as opaque tokens, or `[]`.

    What a token *means* is never decoded; it is compared only with tokens from
    the same producer.  This is how a label column can help settle an ambiguous
    trace without the harness ever deciding what a class is called.
    """
    value = _as_lists(value)
    if not isinstance(value, (list, tuple)) or len(value) != n_rows:
        return []
    if any(_row_width(item) is not None or isinstance(item, Mapping)
           for item in value):
        return []                       # rows, not per-row tokens
    return [repr(item) for item in value]


def columnar_keys_present(returned: object) -> List[str]:
    """Which registered record columns a returned mapping carries, by name."""
    if not isinstance(returned, Mapping):
        return []
    keys = {str(k) for k in returned.keys()}
    return [key for key in COLUMNAR_RECORD_KEYS if key in keys]


def is_columnar_return(returned: object) -> bool:
    """Is this the registered columnar record schema?

    Decided from the **schema alone** — the type and the key names — and never
    from the values inside it.  That matters more than it looks: a dispatcher
    that peeked at the numbers could pick whichever reader produced a tidier
    answer, and the answer is the thing under test.

    Recognition needs the identity carrier and at least one other registered
    column.  Requiring all seven would be stricter in appearance only: a record
    missing one of them would then be handed to the general reader, which is
    the fallback this design exists to remove.  The carrier is the column that
    decides anything, so it is the one that must be there — and a mapping that
    carries record columns *without* it is a stop, not a fallback.
    """
    present = columnar_keys_present(returned)
    return COLUMNAR_IDENTITY_KEY in present and len(present) >= 2


def is_incomplete_columnar_return(returned: object) -> bool:
    """Record columns came back, but not the one that identifies the rows."""
    present = columnar_keys_present(returned)
    return len(present) >= 2 and COLUMNAR_IDENTITY_KEY not in present


def return_schema_report(returned: object,
                         n_rows: Optional[int] = None) -> Dict[str, object]:
    """What came back, described by shape.  Recorded on every fixture.

    Type, keys, shapes, dtypes, row-alignment — enough that the next stop is
    diagnosable from the bundle alone, and nothing that could be read as a
    measurement.  No array contents and no source locals.
    """
    report: Dict[str, object] = {
        "type": type(returned).__name__,
        "is_mapping": isinstance(returned, Mapping),
        "is_columnar_record": is_columnar_return(returned),
        "shape_summary": describe_returned(returned),
        "keys": None,
        "columns": {},
    }
    if isinstance(returned, Mapping):
        keys = sorted(str(k) for k in returned.keys())
        report["keys"] = keys
        report["missing_registered_keys"] = [
            key for key in COLUMNAR_RECORD_KEYS if key not in keys]
        columns: Dict[str, object] = {}
        for key in keys[:32]:
            value = returned[key]
            shape = _sequence_shape(value)
            columns[key] = {
                "type": type(value).__name__,
                "shape": (None if shape is None else list(shape)),
                "dtype": _sequence_dtype(value),
                "row_aligned": (None if shape is None or n_rows is None
                                else shape[0] == n_rows)}
        report["columns"] = columns
    return report


def project_columnar_rows(returned: Mapping[str, object],
                          fixture: Mapping[str, object],
                          variant: str = STUB_VARIANT_PRIMARY
                          ) -> Dict[str, object]:
    """Read kept-row identity out of the registered columnar record.

    One decisional carrier, fixed in advance: `rr[:, 0]`, which the injected
    stub wrote the peak into.  Everything else is a check on it.  A cross-check
    that disagrees stops the run; a cross-check that is unavailable is recorded
    as unavailable.  Neither can change which rows are read, so there is no way
    for this function to end up reporting "the channel that gave the nicest
    answer".

    Nothing here rounds, snaps to a closest peak, or tolerates a near miss:
    a first column that is not exactly a fixture peak sample is a stop.
    """
    peaks = [int(p) for p in fixture["peaks"]]
    peak_set = set(peaks)
    position_of = {p: i for i, p in enumerate(peaks)}
    schema = return_schema_report(returned)

    def stop(reason: str, **extra: object) -> None:
        raise SourceHarnessError(
            P3_COLUMNAR_RETURN_UNPROJECTABLE,
            f"{fixture['name']}: {reason}.  The registered columnar record was "
            f"recognised, so this is a contradiction inside what the producer "
            f"returned, not a disagreement with the adapter, and no comparison "
            f"was made.",
            context={"fixture": str(fixture["name"]), "parser": "columnar",
                     "variant": variant, "return_schema": schema,
                     "reason": reason, **extra})

    identity_column = returned.get(COLUMNAR_IDENTITY_KEY)
    rows2d = _numeric_rows(identity_column)
    if rows2d is None:
        stop(f"{COLUMNAR_IDENTITY_KEY!r} is not a two-dimensional numeric "
             f"block, so the registered row-identity carrier cannot be read")
    if rows2d and len(rows2d[0]) != COLUMNAR_IDENTITY_WIDTH:
        stop(f"{COLUMNAR_IDENTITY_KEY!r} is {len(rows2d)} x "
             f"{len(rows2d[0])} where the registered width is "
             f"{COLUMNAR_IDENTITY_WIDTH}")
    identity: List[int] = []
    for index, row in enumerate(rows2d):
        value = row[0]
        if value != value or value in (float("inf"), float("-inf")):
            stop(f"row {index} of {COLUMNAR_IDENTITY_KEY!r} carries "
                 f"{'NaN' if value != value else 'an infinity'} where a sample "
                 f"index belongs")
        if float(value) != int(value):
            stop(f"row {index} of {COLUMNAR_IDENTITY_KEY!r} carries a "
                 f"non-integral value where a sample index belongs; this "
                 f"projection does not round")
        sample = int(value)
        if sample not in peak_set:
            stop(f"row {index} of {COLUMNAR_IDENTITY_KEY!r} names sample "
                 f"{sample}, which is not one of the fixture's peaks; this "
                 f"projection does not fall back to the closest one")
        identity.append(sample)
    if len(set(identity)) != len(identity):
        stop(f"{COLUMNAR_IDENTITY_KEY!r} names the same peak more than once, "
             f"so its rows do not identify themselves")
    # Row **order** is deliberately not a validity condition.  One of the six
    # registered fixtures exists to catch a producer that emits its rows in a
    # different order, and a rule that stopped on that would turn the
    # difference it was built to detect into "the harness could not read this".
    # The order is read and reported; comparing it is the differential's job.
    positions = [position_of[s] for s in identity]
    n_rows = len(identity)

    # Every registered column is a column of the same record: a differing row
    # count means the record does not describe one set of rows, and picking the
    # majority would be inventing an answer.
    notes: Dict[str, str] = {}
    for key in COLUMNAR_RECORD_KEYS:
        shape = _sequence_shape(returned.get(key))
        if shape is None:
            notes[key] = "not array-like; no row count to check"
            continue
        if shape[0] != n_rows:
            stop(f"{key!r} has {shape[0]} rows where "
                 f"{COLUMNAR_IDENTITY_KEY!r} has {n_rows}",
                 row_counts={k: (_sequence_shape(returned.get(k)) or [None])[0]
                             for k in COLUMNAR_RECORD_KEYS})

    channels: Dict[str, List[int]] = {f"{COLUMNAR_IDENTITY_KEY}[:, 0]": identity}

    pw_rows = _numeric_rows(returned.get("pw"))
    if pw_rows is None:
        notes["pw"] = "not a two-dimensional numeric block; not used"
    elif not pw_rows:
        notes["pw"] = "no rows; nothing to cross-check"
    else:
        observed = [row[0] for row in pw_rows]
        if [float(v) for v in observed] != [float(v) for v in identity]:
            stop(f"'pw' first column and {COLUMNAR_IDENTITY_KEY!r} first "
                 f"column name different rows",
                 rr_first_column=list(identity),
                 pw_first_column=[(int(v) if float(v) == int(v) else v)
                                  for v in observed])
        channels["pw[:, 0]"] = identity

    # The beat window carries sample identity only while the injection contract
    # holds: the ramp signal makes `signal[i] == i`, and the declared `_z`
    # stand-in is the identity under the primary variant and an elementwise
    # negation under the probe.  The expected centre is therefore known from
    # the *variant*, which is an input, before any value is looked at.
    sign = -1.0 if variant == STUB_VARIANT_PROBE else 1.0
    beat_rows = _numeric_rows(returned.get("beat"))
    window = BJ.WIN_BEFORE + BJ.WIN_AFTER
    if beat_rows is None:
        notes["beat"] = "not a two-dimensional numeric block; not used"
    elif not beat_rows:
        notes["beat"] = "no rows; nothing to cross-check"
    elif len(beat_rows[0]) != window:
        notes["beat"] = (f"width {len(beat_rows[0])} is not the registered "
                         f"window {window}; not used")
    else:
        centres = [row[BJ.WIN_BEFORE] for row in beat_rows]
        # Either sign: the declared helpers are the identity in the primary
        # variant and an elementwise negation in the probe, and there is more
        # than one of them, so a window may pass through the transform more
        # than once.  A sign cannot change *which* row is which, and the rows
        # still come from `rr` either way — so accepting both costs nothing
        # and refusing one would manufacture a stop out of bookkeeping.
        expected = [sign * float(s) for s in identity]
        expected_twice = [float(s) for s in identity]
        recovered = [c * sign for c in centres]
        if centres == expected or centres == expected_twice:
            channels[f"beat[:, {BJ.WIN_BEFORE}]"] = identity
        elif all(float(v) == int(v) and int(v) in peak_set for v in recovered):
            stop(f"the beat window centres name rows "
                 f"{[int(v) for v in recovered]} where "
                 f"{COLUMNAR_IDENTITY_KEY!r} names {identity}",
                 beat_centres=[int(v) for v in recovered],
                 rr_first_column=list(identity))
        else:
            notes["beat"] = ("the stored window does not carry sample identity "
                             "under this injection; not used")

    labels = _flat_tokens(returned.get("y"), n_rows)
    rows = [{"row": index, "peak_sample": sample,
             "tokens": ([["columnar_y", labels[index]]] if labels else [])}
            for index, sample in enumerate(identity)]
    return {"rows": rows,
            "channels": sorted(channels),
            "channel_sequences": {k: list(v) for k, v in channels.items()},
            "parser": "columnar",
            "identity_channel": f"{COLUMNAR_IDENTITY_KEY}[:, 0]",
            "row_order_follows_fixture": positions == sorted(positions),
            "channel_notes": notes,
            "return_schema": return_schema_report(returned, n_rows)}


def _unreadable(canonical: object) -> bool:
    """Did canonicalisation come back with nothing but a type name?"""
    return (isinstance(canonical, dict) and "__type__" in canonical
            and "__map__" not in canonical and "__set__" not in canonical)


def _public_attributes(value: object) -> Dict[str, object]:
    """A returned object's public, non-callable attributes.

    Bounded and dull on purpose: `__dict__` first, then a `__slots__`-style
    sweep, skipping anything private or callable.  A producer that returns a
    record hands its rows over this way.
    """
    out: Dict[str, object] = {}
    holder = getattr(value, "__dict__", None)
    names = (sorted(holder) if isinstance(holder, dict)
             else [n for n in dir(value) if not n.startswith("_")])
    for name in names[:MAX_CONTAINER]:
        if name.startswith("_"):
            continue
        try:
            attribute = getattr(value, name)
        except Exception:                                    # noqa: BLE001
            continue
        if callable(attribute):
            continue
        out[name] = attribute
    return out


def describe_returned(value: object, depth: int = 0) -> str:
    """The shape of what a producer returned, without its contents.

    Type, keys, lengths and element kinds — enough to extend the reader
    deliberately next time, and nothing that could pass for a measurement.
    """
    numpy = _numpy()
    if numpy is not None and isinstance(value, numpy.ndarray):
        return f"ndarray{tuple(value.shape)} of {value.dtype}"
    if value is None or isinstance(value, (bool, int, float, str, bytes)):
        return type(value).__name__
    if isinstance(value, Mapping):
        if depth >= 2:
            return f"mapping of {len(value)}"
        inner = ", ".join(
            f"{k!r}: {describe_returned(v, depth + 1)}"
            for k, v in list(value.items())[:12])
        return f"mapping({len(value)}) {{{inner}}}"
    if isinstance(value, (list, tuple, set, frozenset)):
        kind = type(value).__name__
        items = list(value)[:3]
        if depth >= 2:
            return f"{kind} of {len(value)}"
        inner = ", ".join(describe_returned(v, depth + 1) for v in items)
        return f"{kind}({len(value)}) [{inner}{', …' if len(value) > 3 else ''}]"
    attributes = _public_attributes(value)
    if attributes:
        inner = ", ".join(
            f"{k}: {describe_returned(v, depth + 1)}"
            for k, v in list(attributes.items())[:12])
        return f"{type(value).__name__} object with {{{inner}}}"
    return f"{type(value).__name__} object with no readable public attributes"


def _canonical_mapping(node: object) -> Optional[Dict[str, object]]:
    """A canonicalised mapping read back as a plain dict, or `None`.

    `canonical_value` renders every mapping as `{"__map__": [[key, value], …]}`
    so that non-string keys survive; row discovery wants the ordinary view of
    it back, and only string keys can be field names.
    """
    if not isinstance(node, dict) or "__map__" not in node:
        return None
    out: Dict[str, object] = {}
    for pair in node["__map__"]:
        if isinstance(pair, (list, tuple)) and len(pair) == 2 and \
                isinstance(pair[0], str):
            out[pair[0]] = pair[1]
    return out


def discover_kept_rows(returned: object, fixture: Mapping[str, object],
                       variant: str = STUB_VARIANT_PRIMARY
                       ) -> Dict[str, object]:
    """Read the kept rows out of whatever the producer returned.

    The registered columnar record is read by :func:`project_columnar_rows`,
    and the choice between the two readers is made from the **return schema
    alone** — before a single value is looked at — so a run can never end up
    reporting whichever reader produced the tidier answer.  There is
    deliberately no fallback from the columnar reader to this one: falling back
    after a contradiction would be exactly that choice, made after seeing it.

    What follows is the general reader, for the candidate adapter and for any
    producer that hands rows back as rows.  Three independent channels, and
    they must agree where more than one is present:

    * rows that are mappings and all carry a peak-valued field;
    * two-dimensional numeric blocks whose first column is a peak — the RR and
      P-wave stubs put the peak there on purpose;
    * two-dimensional blocks as wide as the beat window, whose centre column is
      a peak — the ramp signal makes a window say its own centre.

    Label tokens are collected beside the rows: a row's string fields, and any
    flat per-row vector that is not simply the peaks again.  They are compared
    only against other tokens from the **same** producer, so the two sides
    never have to agree about how a class is spelled.
    """
    if returned is None:
        # It ran, and it declined to build a record.  That is an observation of
        # the producer, not a failure of the reader, and the two must not be
        # reported as one thing: widening a reader that was never the problem
        # is how a run loses another round.  Why it declined is in the trace
        # the caller attaches, never guessed at here.
        raise SourceHarnessError(
            P3_SOURCE_RETURNED_NO_RECORD,
            f"{fixture['name']}: the producer ran to completion and returned "
            f"None — not an empty record, which would say it kept no rows, but "
            f"no record at all.  It declined to build one for this input.  No "
            f"rows were compared, so this is not a disagreement with the "
            f"adapter; the trace beside this stop says which line returned and "
            f"what its locals were holding.",
            context={"fixture": str(fixture["name"]), "variant": variant,
                     "reason": "the producer returned None",
                     "return_schema": return_schema_report(returned)})
    if is_columnar_return(returned):
        return project_columnar_rows(returned, fixture, variant)
    if is_incomplete_columnar_return(returned):
        raise SourceHarnessError(
            P3_COLUMNAR_RETURN_UNPROJECTABLE,
            f"{fixture['name']}: the producer returned the registered record "
            f"columns {columnar_keys_present(returned)} without "
            f"{COLUMNAR_IDENTITY_KEY!r}, the column that says which peak each "
            f"row was built for.  Reading the remaining columns with the "
            f"general reader would be choosing a channel because the "
            f"registered one is missing, so the comparison is not made.",
            context={"fixture": str(fixture["name"]), "parser": "columnar",
                     "variant": variant,
                     "return_schema": return_schema_report(returned),
                     "reason": "the row-identity carrier is missing"})
    peaks = [int(p) for p in fixture["peaks"]]
    peak_set = set(peaks)
    schema = return_schema_report(returned)
    canonical = canonical_value(returned, limit=RETURN_MAX_CONTAINER)
    if _unreadable(canonical):
        # A producer may hand back a record object rather than a mapping or a
        # tuple.  Its public attributes are what it returned, so they are read
        # the same way — this is still "read what came back", not a guess about
        # what it means.
        attributes = _public_attributes(returned)
        if attributes:
            canonical = canonical_value(attributes,
                                        limit=RETURN_MAX_CONTAINER)
    channels: Dict[str, List[Dict[str, object]]] = {}
    rejected: List[str] = []
    empty_lists: List[str] = []

    def scan(node: object, path: str) -> None:
        if isinstance(node, dict):
            if "__map__" in node:
                for key, value in node["__map__"]:
                    scan(value, f"{path}.{key}")
                return
            if "__set__" in node:
                return
            for key, value in node.items():
                if not str(key).startswith("__"):
                    scan(value, f"{path}.{key}")
            return
        if isinstance(node, list) and not node:
            empty_lists.append(path)
            return
        if not isinstance(node, list):
            return
        as_mappings = [_canonical_mapping(item) for item in node]
        if all(item is not None for item in as_mappings):
            rows = []
            with_peak = 0
            for position, item in enumerate(as_mappings):
                sample = None
                for field in PEAK_ROW_FIELDS:
                    value = item.get(field)
                    if isinstance(value, int) and value in peak_set:
                        sample = value
                        break
                    if (field == "peak_index" and isinstance(value, int)
                            and 0 <= value < len(peaks)):
                        sample = peaks[value]
                        break
                if sample is None:
                    continue
                with_peak += 1
                strings = {k: v for k, v in sorted(item.items())
                           if isinstance(v, str)}
                rows.append({"row": position, "peak_sample": sample,
                             "tokens": ([["row_strings",
                                          _canonical_json(strings)]]
                                        if strings else [])})
            if with_peak == 0:
                return                     # not a row channel at all; ignore
            if with_peak != len(node):
                rejected.append(
                    f"{path}: {with_peak} of {len(node)} rows carry a peak")
                return
            channels[f"rows{path}"] = rows
            return
        if all(isinstance(item, list) and item
               and all(isinstance(v, (int, float)) and not isinstance(v, bool)
                       for v in item) for item in node):
            widths = {len(item) for item in node}
            if len(widths) != 1:
                return
            width = widths.pop()
            first = [int(item[0]) for item in node]
            if all(v in peak_set for v in first):
                channels[f"first_column{path}"] = [
                    {"row": i, "peak_sample": v, "tokens": []}
                    for i, v in enumerate(first)]
                return
            if width == BJ.WIN_BEFORE + BJ.WIN_AFTER:
                centres = [int(item[BJ.WIN_BEFORE]) for item in node]
                if all(v in peak_set for v in centres):
                    channels[f"window_centre{path}"] = [
                        {"row": i, "peak_sample": v, "tokens": []}
                        for i, v in enumerate(centres)]
            return
        # Not a row channel itself: look inside.  A producer may return a
        # tuple of arrays rather than a mapping of them, and the rows are then
        # one level further in — an unread container is not an absent one.
        for index, item in enumerate(node[:MAX_CONTAINER]):
            if isinstance(item, (list, dict)):
                scan(item, f"{path}[{index}]")
        return

    scan(canonical, "")
    if not channels:
        if rejected:
            raise SourceHarnessError(
                P3_KEPT_ROWS_UNOBSERVABLE,
                f"the producer returned row-like structures this projection "
                f"could not read: {rejected}.  The comparison was not made.",
                context={"fixture": str(fixture["name"]), "parser": "generic",
                         "variant": variant, "return_schema": schema,
                         "rejected": list(rejected)})
        if not empty_lists:
            # Nothing that could hold rows came back at all.  "It kept
            # nothing" and "its output cannot be read" are different findings,
            # and only the second one is true here.  The stop describes the
            # **shape** of what did come back — type, keys, lengths — because
            # otherwise the next step is a guess about a value nobody may look
            # at directly.
            raise SourceHarnessError(
                P3_KEPT_ROWS_UNOBSERVABLE,
                f"the producer returned no row container at all: not an empty "
                f"one, which would say it kept nothing, and not a readable "
                f"one.  What it did return: {describe_returned(returned)}.  "
                f"The comparison was not made.",
                context={"fixture": str(fixture["name"]), "parser": "generic",
                         "variant": variant, "return_schema": schema,
                         "reason": "no row container at all"})
        # Every row container that came back was empty: the producer kept no
        # rows, and that is an observation rather than a failure.
        return {"rows": [], "channels": ["empty_result"],
                "channel_sequences": {"empty_result": []},
                "parser": "generic", "return_schema": schema,
                "empty_containers": sorted(empty_lists)}
    sequences = {name: [row["peak_sample"] for row in rows]
                 for name, rows in channels.items()}
    if len({tuple(v) for v in sequences.values()}) != 1:
        raise SourceHarnessError(
            P3_KEPT_ROWS_UNOBSERVABLE,
            f"the producer's own output channels disagree about which rows it "
            f"kept: {sequences}.  A comparison built on a channel chosen after "
            f"seeing the answers would be worthless.",
            context={"fixture": str(fixture["name"]), "parser": "generic",
                     "variant": variant, "return_schema": schema,
                     "channel_sequences": {k: list(v)
                                           for k, v in sequences.items()}})
    rows = channels[sorted(channels)[0]]
    for name in sorted(channels):
        for index, row in enumerate(channels[name]):
            for token in row["tokens"]:
                if token not in rows[index]["tokens"]:
                    rows[index]["tokens"].append(token)
    for path, vector in label_vectors(canonical, len(rows), peak_set):
        for position, row in enumerate(rows):
            row["tokens"].append([f"vector_at{path}", vector[position]])
    return {"rows": rows, "channels": sorted(channels),
            "channel_sequences": {k: list(v) for k, v in sequences.items()},
            "parser": "generic",
            "return_schema": return_schema_report(returned, len(rows))}


def label_vectors(canonical: object, n_rows: int, peak_set: Set[int]
                  ) -> List[Tuple[str, List[str]]]:
    """Flat per-row vectors a producer returned, as opaque tokens.

    What the values *mean* is never decoded.  They are tokens, compared only
    with other tokens from the same producer, which is all the projection needs
    in order to tell two annotations apart.  Every candidate vector is kept:
    one that turns out to be row-unique simply never matches anything and
    contributes nothing, while a class-like one generalises across fixtures.

    Each vector is returned with the **path it was found at**, and that path is
    what names its channel.  Naming channels by the order they were discovered
    in instead would make the same output channel a different channel from one
    fixture to the next whenever the number of candidates changed — so a label
    learned where a mapping was unambiguous could not settle the fixture that
    needed it, and the run would stop as unprojectable for a reason that has
    nothing to do with the producer.
    """
    found: List[Tuple[str, List[str]]] = []

    def scan(node: object, path: str) -> None:
        if isinstance(node, dict):
            if "__map__" in node:
                for key, value in node["__map__"]:
                    scan(value, f"{path}.{key}")
                return
            for key, value in node.items():
                if not str(key).startswith("__"):
                    scan(value, f"{path}.{key}")
            return
        if isinstance(node, list):
            if n_rows and len(node) == n_rows and all(
                    isinstance(v, (int, float, str)) and not isinstance(v, bool)
                    for v in node):
                if all(isinstance(v, int) and v in peak_set for v in node):
                    return
                found.append((path, [_canonical_json(v) for v in node]))
                return
            for index, item in enumerate(node[:MAX_CONTAINER]):
                if isinstance(item, (list, dict)):
                    scan(item, f"{path}[{index}]")
            return

    scan(canonical, "")
    return found


class LabelDictionary(object):
    """Observed correspondence between a producer's row labels and annotations.

    Learned only from fixtures whose consumption events resolved on their own,
    and used only to settle the ones that did not.  It is an observation of a
    producer's own output, not a decoding of it: nothing here knows or needs to
    know what the producer calls an AAMI class.  Each channel is kept apart, so
    a row-unique channel cannot poison a class-like one.
    """

    __slots__ = ("by_token", "by_symbol")

    def __init__(self) -> None:
        self.by_token: Dict[str, Set[str]] = {}
        self.by_symbol: Dict[Tuple[str, str], Set[str]] = {}

    @staticmethod
    def _key(token: Sequence[object]) -> str:
        return _canonical_json(list(token))

    def learn(self, tokens: Sequence[Sequence[object]], symbol: str) -> None:
        for token in tokens:
            self.by_token.setdefault(self._key(token), set()).add(symbol)
            channel = str(token[0]) if token else ""
            value = _canonical_json(token[1]) if len(token) > 1 else ""
            self.by_symbol.setdefault((channel, symbol), set()).add(value)

    def symbols_for(self, tokens: Sequence[Sequence[object]]) -> Set[str]:
        """Symbols consistent with every channel that has an opinion."""
        known = [set(self.by_token[self._key(t)]) for t in tokens
                 if self._key(t) in self.by_token]
        if not known:
            return set()
        out = set(known[0])
        for other in known[1:]:
            out &= other
        return out

    def excluded_symbols(self, tokens: Sequence[Sequence[object]]) -> Set[str]:
        """Symbols this row cannot carry, from what the channel already showed.

        Negative evidence, and it is the useful kind on a first sighting: a
        label never seen before says nothing on its own, but if this producer
        has only ever written one label for class `N` and this row's label is a
        different one, then whatever this row is, it is not `N`.  Only channels
        that have been single-valued for a symbol so far are read this way.
        """
        out: Set[str] = set()
        for token in tokens:
            channel = str(token[0]) if token else ""
            value = _canonical_json(token[1]) if len(token) > 1 else ""
            for (known_channel, symbol), values in self.by_symbol.items():
                if known_channel != channel or len(values) != 1:
                    continue
                if value not in values:
                    out.add(symbol)
        return out

    def as_dict(self) -> Dict[str, List[str]]:
        return {token: sorted(symbols)
                for token, symbols in sorted(self.by_token.items())}


def project_observation(fixture: Mapping[str, object], trace: FrameTrace,
                        returned: object, dictionary: LabelDictionary,
                        side: str,
                        variant: str = STUB_VARIANT_PRIMARY,
                        discovery: Optional[Dict[str, object]] = None
                        ) -> Dict[str, object]:
    """One producer's decisions on one fixture, in the canonical schema.

    The same function runs over the registered source and over the candidate
    adapter.  It compares nothing; it says what each of them did, and stops
    when the trace does not say.
    """
    annotations = _annotation_table(fixture)
    peaks = _peak_table(fixture)
    name = str(fixture["name"])
    discovered = discover_kept_rows(returned, fixture, variant)
    if discovery is not None:
        # Handed back to the caller by reference, so that the reading of the
        # return survives a stop raised further down.  It is deliberately not
        # part of the returned observation: the observation is what gets
        # compared, and how a producer *shapes* its output is not a decision
        # this PREP compares.
        discovery.clear()
        discovery.update({k: v for k, v in discovered.items() if k != "rows"})
        discovery["n_rows"] = len(discovered["rows"])
    kept = discovered["rows"]
    peak_index_of = {p["peak_sample"]: p["peak_index"] for p in peaks}

    def settle_by_row_label(peak_index: int,
                            candidates: Sequence[int]) -> Optional[int]:
        """Ask the producer's own output which of two readings is the one.

        The label a kept row carries was learned from fixtures this producer
        resolved unaided, so this is still an observation of the producer
        rather than a rule imposed on it.  A peak with no kept row, or a label
        nobody has seen before, settles nothing and says so.
        """
        row = next((r for r in kept
                    if peak_index_of.get(r["peak_sample"]) == peak_index), None)
        if row is None:
            return None
        options = sorted(set(candidates))
        symbols = dictionary.symbols_for(row["tokens"])
        if symbols:
            matched = [index for index in options
                       if annotations[index]["symbol"] in symbols]
        else:
            excluded = dictionary.excluded_symbols(row["tokens"])
            matched = [index for index in options
                       if annotations[index]["symbol"] not in excluded]
            if len(matched) == len(options):
                return None          # nothing was ruled out; nothing is settled
        return matched[0] if len(matched) == 1 else None

    implied = implied_mappings(trace, fixture)
    merged, releases = merge_implied(implied["by_container"], side, name,
                                     settle=settle_by_row_label)

    # Rows whose annotation is already known teach the dictionary; the
    # dictionary then settles the events that two readings left open.
    for row in kept:
        pair = merged.get(peak_index_of.get(row["peak_sample"]))
        if pair is not None and pair["annotation_index"] is not None:
            dictionary.learn(row["tokens"],
                             annotations[pair["annotation_index"]]["symbol"])
    unresolved: List[str] = []
    for peak_index, entry in sorted(merged.items()):
        if entry["annotation_index"] is not None:
            continue
        chosen = settle_by_row_label(peak_index, entry["candidates"])
        if chosen is not None:
            entry["annotation_index"] = chosen
            entry["reading"] = entry["reading"] + "_settled_by_row_label"
            continue
        unresolved.append(
            f"peak {peak_index} consumed an annotation the trace identifies "
            f"only as one of {entry['candidates']}, and the row it produced "
            f"does not settle it")

    # A kept row for a peak the trace never matched means the projection missed
    # a decision.  That is a stop, not a hole quietly left in the comparison.
    for row in kept:
        peak_index = peak_index_of.get(row["peak_sample"])
        if peak_index is None or peak_index not in merged:
            unresolved.append(
                f"a row was kept for peak sample {row['peak_sample']} that the "
                f"trace never matched to an annotation")
    if unresolved:
        raise SourceHarnessError(
            P3_SOURCE_TRACE_UNPROJECTABLE,
            f"{side}/{name}: " + "; ".join(sorted(set(unresolved))),
            context={"fixture": name, "side": side, "variant": variant,
                     "unresolved": sorted(set(unresolved)),
                     "return_schema": discovered.get("return_schema"),
                     "parser": discovered.get("parser")})

    # What the dictionary already knows must agree with what the trace says.
    # A row whose label contradicts its mapped annotation means one of the two
    # channels is being misread, and reporting that as a disagreement between
    # the two sides would be a fabrication.
    for row in kept:
        pair = merged[peak_index_of[row["peak_sample"]]]
        symbols = dictionary.symbols_for(row["tokens"])
        symbol = annotations[pair["annotation_index"]]["symbol"]
        if symbols and symbol not in symbols:
            raise SourceHarnessError(
                P3_SOURCE_TRACE_UNPROJECTABLE,
                f"{side}/{name}: the row kept for peak sample "
                f"{row['peak_sample']} carries a label this producer has "
                f"elsewhere used for {sorted(symbols)}, but the trace maps it "
                f"to {symbol!r}",
                context={"fixture": name, "side": side, "variant": variant,
                         "return_schema": discovered.get("return_schema"),
                         "parser": discovered.get("parser")})

    mapping = []
    for peak in peaks:
        pair = merged.get(peak["peak_index"])
        annotation = (annotations[pair["annotation_index"]] if pair else None)
        mapping.append({
            "peak_index": peak["peak_index"],
            "peak_sample": peak["peak_sample"],
            "annotation": (None if annotation is None else
                           {"index": annotation["index"],
                            "sample": annotation["sample"],
                            "symbol": annotation["symbol"]}),
            "consumed_at_peak_index": (None if pair is None
                                       else peak["peak_index"])})
    consumed = sorted(
        ({"index": annotations[pair["annotation_index"]]["index"],
          "sample": annotations[pair["annotation_index"]]["sample"],
          "symbol": annotations[pair["annotation_index"]]["symbol"],
          "consumed_at_peak_index": peak_index}
         for peak_index, pair in merged.items()),
        key=lambda a: a["index"])
    consumed_indices = {a["index"] for a in consumed}
    kept_rows = []
    for row in kept:
        peak_index = peak_index_of[row["peak_sample"]]
        annotation = annotations[merged[peak_index]["annotation_index"]]
        kept_rows.append({"row": row["row"], "peak_index": peak_index,
                          "peak_sample": row["peak_sample"],
                          "annotation_index": annotation["index"],
                          "annotation_sample": annotation["sample"],
                          "symbol": annotation["symbol"],
                          "aami": annotation["aami"]})
    return {
        "fixture": name,
        "n_peaks": len(peaks), "n_annotations": len(annotations),
        "signal_length": int(fixture["signal_length"]),
        "tolerance": TOLERANCE,
        "peak_to_annotation": mapping,
        "kept_rows": kept_rows,
        "consumed_annotations": consumed,
        # Releasing is a decision of its own: a producer that hands an
        # annotation back after dropping its peak is not the one that keeps it
        # consumed, and only this field can tell them apart.
        "released_annotations": sorted(
            ({"index": annotations[entry["annotation_index"]]["index"],
              "sample": annotations[entry["annotation_index"]]["sample"],
              "symbol": annotations[entry["annotation_index"]]["symbol"],
              "released_at_peak_index": entry["peak_index"]}
             for entry in releases
             if entry["annotation_index"] is not None),
            key=lambda a: (a["index"], a["released_at_peak_index"])),
        "unmatched_annotations": [
            {"index": a["index"], "sample": a["sample"], "symbol": a["symbol"]}
            for a in annotations if a["index"] not in consumed_indices],
        "unmatched_peaks": [
            {"peak_index": p["peak_index"], "peak_sample": p["peak_sample"]}
            for p in peaks if p["peak_index"] not in merged],
        "stages": stage_decomposition(fixture, mapping, kept_rows),
    }


def stage_decomposition(fixture: Mapping[str, object],
                        mapping: Sequence[Mapping[str, object]],
                        kept_rows: Sequence[Mapping[str, object]]
                        ) -> Dict[str, object]:
    """State either side of AAMI selection and of the boundary cut.

    Both stages are described with the **registered** constants — the frozen
    AAMI map and the frozen 150-sample window — applied identically to each
    side's own observed matching.  That cannot manufacture an agreement,
    because the matching itself comes from each producer, and the last field
    records whether the producer's own kept rows are what this description
    predicts.  A producer whose selection works differently shows up there as a
    difference rather than being normalised away.
    """
    length = int(fixture["signal_length"])
    matched = [m for m in mapping if m["annotation"] is not None]
    post_aami = [m for m in matched
                 if BJ.AAMI_SYMBOL_MAP.get(m["annotation"]["symbol"], "")]
    post_boundary = [m for m in post_aami
                     if m["peak_sample"] - BJ.WIN_BEFORE >= 0
                     and m["peak_sample"] + BJ.WIN_AFTER <= length]
    observed = [row["peak_index"] for row in kept_rows]
    predicted = [m["peak_index"] for m in post_boundary]
    return {"matched_pre_aami": [m["peak_index"] for m in matched],
            "post_aami_pre_boundary": [m["peak_index"] for m in post_aami],
            "post_boundary": predicted,
            "observed_kept": observed,
            "kept_equals_post_boundary": observed == predicted,
            "window": [BJ.WIN_BEFORE, BJ.WIN_AFTER]}


def observation_digest(observation: Mapping[str, object]) -> str:
    """The digest a fixture result reports.  Same schema, same convention."""
    return canonical_digest(observation)


# ─────────────────────────────────────────────────────────────────────────────
# The two sides.
# ─────────────────────────────────────────────────────────────────────────────
def observe_source(build_record: Callable, fixture: Mapping[str, object],
                   dictionary: LabelDictionary,
                   variant: str = STUB_VARIANT_PRIMARY,
                   discovery: Optional[Dict[str, object]] = None
                   ) -> Tuple[Dict[str, object], Dict[str, object]]:
    """Run the registered producer on one fixture and read what it did."""
    binding = bind_source_arguments(build_record, fixture)
    returned, trace = trace_call(build_record, build_record.__code__,
                                 binding["kwargs"])
    reading: Dict[str, object] = {} if discovery is None else discovery
    try:
        observation = project_observation(fixture, trace, returned, dictionary,
                                          side="source", variant=variant,
                                          discovery=reading)
    except SourceHarnessError as error:
        # The reading of the return is the diagnosis, so it is attached before
        # the stop leaves this frame rather than recomputed by a caller that no
        # longer has the value.  The trace goes with it: when the producer ran
        # to completion and still gave nothing readable, which line it returned
        # from and what its locals were holding is the whole question.
        error.context.setdefault("return_schema",
                                 return_schema_report(returned))
        error.context.setdefault("trace", trace_summary(trace))
        error.context.setdefault("binding", list(binding["plan"]))
        raise
    return observation, {"binding": binding["plan"], "variant": variant,
                         "return_reading": dict(reading), **trace.as_dict()}


def observe_adapter(fixture: Mapping[str, object], dictionary: LabelDictionary,
                    adapter: Optional[Callable] = None
                    ) -> Tuple[Dict[str, object], Dict[str, object]]:
    """Run the candidate adapter on the same fixture, through the same lens."""
    adapter = adapter or Q5E.match_peaks_to_annotations
    kwargs = {"peaks": [int(p) for p in fixture["peaks"]],
              "annotations": [(int(s), str(y))
                              for s, y in fixture["annotations"]],
              "signal_length": int(fixture["signal_length"])}
    returned, trace = trace_call(adapter, adapter.__code__, kwargs)
    reading: Dict[str, object] = {}
    observation = project_observation(fixture, trace, returned, dictionary,
                                      side="adapter", discovery=reading)
    return observation, {"return_reading": dict(reading), **trace.as_dict()}


#: What a discovery pass is and is not, carried beside its result so that no
#: reader can mistake one for the other.
SURFACE_DISCOVERY_NOTE = (
    "SURFACE DISCOVERY - NOT AN OBSERVATION.  Run only after a run has already "
    "stopped at P3_STUB_SURFACE_INCOMPLETE, on the fixture that stopped it, "
    "with undeclared names answered by a permissive stand-in instead of a "
    "refusal.  Its only output is the list of names the producer went on to "
    "ask for, so that one round declares all of them instead of one per round. "
    "Nothing it computed is read: not a return value, not a trace, not a row. "
    "The refusal itself is unchanged - a real run still stops at the first "
    "undeclared name.  Read the list as a LOWER BOUND: a stand-in answers "
    "where the real value would, and a producer that branches on what it got "
    "back may take a different path than it will once the name is declared "
    "for real.")


#: How many times a discovery pass may retry with an arity read back from the
#: producer's own unpacking error.  A bound, not a search: each retry must be
#: driven by a *new* number the producer named, so a loop cannot invent one.
MAX_DISCOVERY_ATTEMPTS = 4


def discover_stub_surface(open_source: Callable,
                          fixture: Mapping[str, object]) -> Dict[str, object]:
    """List every undeclared name a producer would ask for, in one pass.

    Four of this PREP's stops have been "the injected surface is missing one
    more name", each costing a full round trip to learn a single name.  The
    refusal is right — an unknown dependency must never slip into a run wearing
    a stub's name — but learning them one at a time is not.

    So after a run has already stopped for that reason, the same fixture is run
    once more with undeclared names answered permissively, purely to enumerate
    them.  The result is a list of names and nothing else: no value it produced
    is read, and the caller writes it into the stop's context, never into an
    observation.
    """
    names: List[str] = []
    error: Optional[str] = None
    completed = False
    arity = 0
    attempts: List[Dict[str, object]] = []

    def collect(log: StubCallLog) -> None:
        for call in log.as_list():
            requested = str(call.get("requested") or "")
            if requested.startswith("__"):
                continue         # import machinery, not a dependency
            if call.get("declared") is False and requested:
                name = f"{str(call['target']).split('.')[0]}.{requested}"
                if name not in names:
                    names.append(name)

    for _attempt in range(MAX_DISCOVERY_ATTEMPTS):
        error, completed = None, False
        try:
            with open_source(fixture, STUB_VARIANT_PRIMARY, permissive=True,
                             unpack_arity=arity) as (build_record, log):
                try:
                    binding = bind_source_arguments(build_record, fixture)
                    build_record(**dict(binding["kwargs"]))
                    completed = True
                except BaseException as problem:             # noqa: BLE001
                    error = f"{type(problem).__name__}: {problem}"[:400]
                collect(log)
        except BaseException as problem:                     # noqa: BLE001
            error = f"{type(problem).__name__}: {problem}"[:400]
        attempts.append({"unpack_arity": arity, "reached_the_end": completed,
                         "stopped_with": error})
        if completed or error is None:
            break
        # A producer that writes `a, b = helper(...)` refuses a stand-in that
        # unpacks into nothing, and the pass would stop one name early.  The
        # arity comes from the producer's own message, not from a guess, so
        # retrying with it is reading the refusal rather than working around
        # it.  Anything else ends the pass.
        wanted = re.search(r"unpack \(expected (\d+)", error or "")
        if not wanted or int(wanted.group(1)) == arity:
            break
        arity = int(wanted.group(1))
    return {"note": SURFACE_DISCOVERY_NOTE,
            "fixture": str(fixture["name"]),
            "undeclared_names": names,
            "reached_the_end": completed,
            "stopped_with": error,
            "unpack_arity_used": arity,
            "attempts": attempts,
            "is_an_observation": False}


def probe_injection_invariance(open_source: Callable,
                               fixture: Mapping[str, object],
                               observation: Mapping[str, object],
                               dictionary: LabelDictionary
                               ) -> Dict[str, object]:
    """Run one fixture again under a different injected helper, and compare.

    The claim being tested is narrow and important: that replacing `_z` with
    something that behaves differently does not move a single decision this
    PREP compares.  If it holds, the injected helper is standing out of the
    way, and that is *shown* rather than argued.  If the probe cannot run —
    because the producer refuses the perturbed values, say — the result is
    reported as untested, never as passed.
    """
    try:
        with open_source(fixture, STUB_VARIANT_PROBE) as (build_record, _log):
            # The probe carries its own dictionary, accumulated across the
            # fixtures in the same order as the primary run's.  A fresh one per
            # fixture would leave the later fixtures with nothing to settle an
            # ambiguous trace against, and they would report "untested" for a
            # reason that has nothing to do with the injected helper.
            probed, _meta = observe_source(build_record, fixture, dictionary,
                                           variant=STUB_VARIANT_PROBE)
    except SourceHarnessError as error:
        return {"status": "untested", "variant": STUB_VARIANT_PROBE,
                "reason": f"the producer stopped under the probe: "
                          f"{error.status}",
                "fields": []}
    except Exception as error:                               # noqa: BLE001
        return {"status": "untested", "variant": STUB_VARIANT_PROBE,
                "reason": f"the probe run raised "
                          f"{type(error).__name__}: {error}",
                "fields": []}
    differing = [d["field"] for d in describe_difference(observation, probed)]
    if differing:
        return {"status": "violated", "variant": STUB_VARIANT_PROBE,
                "reason": "a compared field moved with the injected helper",
                "fields": differing}
    return {"status": "invariant", "variant": STUB_VARIANT_PROBE,
            "reason": ("every compared field is identical under both injected "
                       "implementations"),
            "fields": []}


def differential_over_fixtures(open_source: Callable,
                               adapter: Optional[Callable] = None,
                               emit=None) -> Dict[str, object]:
    """Compare the registered producer with the candidate adapter, fixture by fixture.

    Every registered fixture is run — the list is fixed before anything is
    executed and is never trimmed after seeing a result — and a disagreement is
    recorded rather than repaired.  There is deliberately no branch here that
    adjusts the adapter, tries another rule, or keeps the better-scoring of two
    candidates.
    """
    emit = emit or (lambda _message: None)
    gate = assert_fixture_contract()
    # One dictionary per side.  A label is only ever compared with labels from
    # the same producer, and separate dictionaries make that structural rather
    # than a property of how the tokens happen to be spelled.
    source_dictionary = LabelDictionary()
    adapter_dictionary = LabelDictionary()
    probe_dictionary = LabelDictionary()
    results: List[Dict[str, object]] = []
    detail: List[Dict[str, object]] = []
    for name in fixture_names():
        fixture = FIXTURES_BY_NAME[name]
        reading: Dict[str, object] = {}
        call_log = StubCallLog()
        try:
            # The producer is observed **inside** its session, so the stubs are
            # still installed while `build_record` runs.  A dependency imported
            # in the function body resolves to the injected module, not a real
            # one.
            with open_source(fixture) as (build_record, call_log):
                source_observation, source_meta = observe_source(
                    build_record, fixture, source_dictionary,
                    discovery=reading)
        except SourceHarnessError as error:
            # Everything learned up to the stop goes onto the exception, where
            # `_execute_with_permit` can put it in the bundle.  A stop discards
            # the differential, so a diagnosis reachable only through the
            # result is lost exactly when it is the only thing worth having.
            error.context.setdefault("fixture", name)
            error.context["fixtures_completed"] = [e["name"] for e in detail]
            error.context["stub_calls"] = stub_call_summary(call_log)
            error.context.setdefault("return_reading", dict(reading))
            if error.status == P3_STUB_SURFACE_INCOMPLETE:
                # One more pass over the same fixture, with undeclared names
                # answered instead of refused, purely to list them.  Nothing it
                # produces is read; only the names reach the bundle.
                error.context["surface_discovery"] = discover_stub_surface(
                    open_source, fixture)
            raise
        # Neutrality of the injected helpers is probed, not assumed: the same
        # fixture is observed again with `_z` negated, and the decisions must
        # not move.  A difference means the injection is steering the
        # comparison, which is a stop rather than a result.
        invariance = probe_injection_invariance(
            open_source, fixture, source_observation, probe_dictionary)
        if invariance["status"] == "violated":
            raise SourceHarnessError(
                P3_INJECTED_VALUE_STEERS_MATCHING,
                f"{name}: the observation changed when an injected helper was "
                f"replaced by a different implementation "
                f"({STUB_VARIANT_PRIMARY} vs {STUB_VARIANT_PROBE}): "
                f"{invariance['fields']}.  The injected value is not standing "
                f"out of the way of the decisions this PREP compares, so the "
                f"comparison is not made.")
        adapter_observation, adapter_meta = observe_adapter(
            fixture, adapter_dictionary, adapter)
        source_digest = observation_digest(source_observation)
        adapter_digest = observation_digest(adapter_observation)
        equal = source_digest == adapter_digest
        results.append({"name": name,
                        "source_result_sha256": source_digest,
                        "adapter_result_sha256": adapter_digest,
                        "equal": equal})
        detail.append({"name": name, "refutes": fixture["refutes"],
                       "equal": equal, "stub_invariance": invariance,
                       "source": source_observation,
                       "adapter": adapter_observation,
                       "source_meta": source_meta,
                       "adapter_meta": adapter_meta,
                       # Recorded on every fixture, not only on a stop: the
                       # shape of what the producer returned and how much the
                       # stubs were asked for is what makes the *next* stop
                       # diagnosable from the bundle alone.
                       "return_reading": dict(reading),
                       "stub_calls": stub_call_summary(call_log),
                       "injected_calls": call_log.as_list(),
                       "difference": (None if equal else describe_difference(
                           source_observation, adapter_observation))})
        emit(f"fixture {name}: equal={equal}")
    invariance_summary = {
        entry["name"]: entry["stub_invariance"]["status"] for entry in detail}
    return {"gate": gate, "fixtures": results, "detail": detail,
            "stub_invariance": invariance_summary,
            "stub_invariance_probed": sorted(
                {s for s in invariance_summary.values()}),
            "fixtures_passed": sum(1 for r in results if r["equal"]),
            "fixtures_total": len(results),
            "all_equal": all(r["equal"] for r in results),
            "first_failing_fixture": next(
                (r["name"] for r in results if not r["equal"]), None),
            "label_dictionary": {"source": source_dictionary.as_dict(),
                                 "adapter": adapter_dictionary.as_dict()}}


def describe_difference(source: Mapping[str, object],
                        adapter: Mapping[str, object]
                        ) -> List[Dict[str, object]]:
    """Which fields of the observation differ, preserved for the bundle."""
    fields = ("peak_to_annotation", "kept_rows", "consumed_annotations",
              "released_annotations", "unmatched_annotations",
              "unmatched_peaks", "stages")
    return [{"field": field, "source": source.get(field),
             "adapter": adapter.get(field)}
            for field in fields if source.get(field) != adapter.get(field)]


# ─────────────────────────────────────────────────────────────────────────────
# Harness identity and the candidate record.
# ─────────────────────────────────────────────────────────────────────────────
#: The functions whose text *is* the oracle harness.  Editing any of them
#: changes `oracle_harness_sha256`, so a PASS recorded under an older harness
#: cannot be reused for a newer one.
ORACLE_HARNESS_FUNCTIONS: Tuple[str, ...] = (
    "build_injection", "InjectedModules", "load_source_under_injection",
    "ProducerSession", "source_factory",
    "bind_source_arguments", "trace_call", "canonical_value", "growth_events",
    "_added_once", "_flipped_once", "_resolve_annotation_token",
    "_resolve_peak_in_scope", "implied_mappings", "merge_implied",
    "probe_injection_invariance", "_elementwise",
    "discover_stub_surface",
    "discover_kept_rows", "_unreadable", "_public_attributes",
    "trace_summary", "_summarise_local",
    "is_columnar_return", "is_incomplete_columnar_return",
    "columnar_keys_present", "project_columnar_rows", "return_schema_report",
    "_sequence_shape", "_row_width", "_numeric_rows", "_flat_tokens",
    "_as_lists", "_sequence_dtype",
    "stub_call_summary", "columnar_keys_present",
    "describe_returned", "label_vectors", "project_observation",
    "stage_decomposition", "observe_source", "observe_adapter",
    "differential_over_fixtures")


def oracle_harness_identity() -> Dict[str, object]:
    """What the harness *is*, as a digest over its own text and its fixtures."""
    import inspect                                           # noqa: PLC0415
    payload = {"functions": {name: inspect.getsource(globals()[name])
                             for name in ORACLE_HARNESS_FUNCTIONS},
               "fixtures": [fixture_card(n) for n in fixture_names()],
               "binding_plan": [[list(a), k] for a, k in BINDING_PLAN],
               "binding_rationale": dict(sorted(BINDING_RATIONALE.items())),
               # The injected surface *is* part of the oracle: a producer that
               # reads `frontend.WIN_BEFORE` behaves according to the value it
               # was handed, so a run under a different declared surface is a
               # run of a different oracle.  Folding it in was missing until
               # 2026-08-16 and the gap was masked by every earlier surface
               # change having also edited a function's text — a declared
               # constant added on its own would have left the digest, and so
               # the recorded execution approval, unmoved.
               "injected_constants": {
                   "wfdb": dict(sorted(WFDB_STUB_CONSTANTS.items())),
                   "frontend": dict(sorted(FRONTEND_STUB_CONSTANTS.items())),
                   "pwave": dict(sorted(PWAVE_STUB_CONSTANTS.items()))},
               "injected_functions": sorted(INJECTED_GLOBALS),
               "stub_variants": list(STUB_VARIANTS),
               "tolerance": TOLERANCE, "win_before": BJ.WIN_BEFORE,
               "win_after": BJ.WIN_AFTER, "module_version": MODULE_VERSION}
    return {"oracle_harness_sha256": canonical_digest(payload),
            "functions": list(ORACLE_HARNESS_FUNCTIONS),
            "module_sha256": Q5E.sha256_file(os.path.abspath(__file__)),
            "q5e_module_sha256": Q5E.sha256_file(os.path.abspath(Q5E.__file__)),
            "frozen_q5d_module_sha256": Q5E.sha256_file(
                os.path.abspath(BJ.__file__)),
            "oracle_is_the_registered_source": True,
            "second_reimplementation_used_as_oracle": False,
            "note": ("the oracle is the digest-verified registered "
                     f"{REGISTERED_SOURCE_NAME} executed under dependency "
                     "injection; this digest covers the capture and "
                     "projection harness around it, which re-expresses none "
                     "of its matching rules and records no expected answer")}


#: Stands in for the payload fold while the bundle that produces it is still
#: being written.  Structurally a digest so the registered gate can be
#: exercised, and obviously not one, so it can never be mistaken for a result.
PLACEHOLDER_FOLD = "0" * 64


def candidate_record(differential: Mapping[str, object], source_sha256: str,
                     prep_payload_sha256: str, harness_sha256: str,
                     adapter_fingerprint: Optional[str] = None
                     ) -> Optional[Dict[str, object]]:
    """The `SOURCE_MATCH_ORACLE_RECORD` candidate — only when every fixture agreed.

    Returns `None` otherwise, and that is the whole of the mismatch policy: a
    partial differential produces no record, so there is nothing to register,
    trim or argue about.  Producing a candidate does not register it: the
    module constant stays `None`, and registration is a separate PR after
    Codex accepts the run.
    """
    if not differential.get("all_equal"):
        return None
    return {
        "verdict": P3_PASS,
        "registered_file_sha256": source_sha256,
        "adapter_fingerprint": (adapter_fingerprint
                                or Q5E.source_match_adapter_fingerprint()),
        "prep_bundle_sha256": prep_payload_sha256,
        "oracle_harness_sha256": harness_sha256,
        "fixtures": [dict(entry) for entry in differential["fixtures"]],
        "fixtures_passed": int(differential["fixtures_passed"]),
    }


def check_candidate_against_gate(candidate: Optional[Mapping[str, object]]
                                 ) -> Dict[str, object]:
    """Put the candidate through the **registered** gate, without registering it.

    `Q5E.verify_source_match_equivalence()` is the function M4.0 will call, so
    running the candidate through it here finds a record that would be rejected
    at execution time.  It is called with the candidate passed **as an
    argument**: `SOURCE_MATCH_ORACLE_RECORD` is not written, by this module or
    by anything it calls.
    """
    if candidate is None:
        return {"checked": False, "ok": False,
                "reason": P3_EQUIVALENCE_REQUIRED,
                "problems": [],
                "registered_constant_written": False,
                "note": ("no candidate was produced, so there is nothing to "
                         "check and the M4.0 sub-gate stays closed")}
    gate = Q5E.verify_source_match_equivalence(candidate)
    return {"checked": True, "ok": bool(gate["ok"]),
            "reason": gate.get("reason"),
            "problems": list(gate.get("problems", ())),
            "registered_constant_written": False,
            "note": ("structural acceptance by the registered gate only.  It "
                     "is not a registration and not a Codex acceptance")}


# ─────────────────────────────────────────────────────────────────────────────
# Drive: one file, by id, read-only.
# ─────────────────────────────────────────────────────────────────────────────
class DriveFileAdapter(object):
    """The Drive seam for P3: metadata by file id, then bytes by file id.

    Two read verbs and nothing else.  There is no name search anywhere: a file
    is identified by its id, and the id is the registered one or the run stops.
    """

    def get_metadata(self, file_id: str) -> Dict[str, object]:
        raise NotImplementedError

    def download(self, file_id: str) -> bytes:
        raise NotImplementedError

    def describe(self) -> Dict[str, object]:
        return {"adapter": type(self).__name__, "read_only": True}


class GoogleDriveFileAdapter(DriveFileAdapter):          # pragma: no cover
    """Production adapter.  The service is injected, never built here."""

    __slots__ = ("approval", "_service")

    def __init__(self, approval: Optional[str], service=None) -> None:
        require_execution_approval(approval, "the Google Drive API")
        if service is None:
            raise P3Error(
                "refusing to build a Drive adapter without a service: a "
                "default client silently adopts an ambient credential whose "
                "scope nobody proved.  Use build_drive_adapter(), which "
                f"acquires a credential scoped to {DRIVE_READONLY_SCOPE} and "
                f"proves it first.")
        self.approval = approval
        self._service = service

    def get_metadata(self, file_id: str) -> Dict[str, object]:
        require_execution_approval(self.approval, f"Drive file {file_id!r}")
        fields = ("id, name, size, mimeType, modifiedTime, sha256Checksum, "
                  "md5Checksum, trashed, parents, shortcutDetails")
        return self._service.files().get(
            fileId=file_id, fields=fields, supportsAllDrives=True).execute()

    def download(self, file_id: str) -> bytes:
        require_execution_approval(self.approval, f"Drive file {file_id!r}")
        return self._service.files().get_media(
            fileId=file_id, supportsAllDrives=True).execute()


def authenticate_drive_readonly(approval: Optional[str],
                                credential_provider=None, service_factory=None
                                ) -> Tuple[object, Dict[str, object]]:
    """Acquire a read-only credential and build the Drive service from it.

    P1/P2's credential machinery is reused — its Colab provider, its scope
    audit and its refusal to proceed under a credential whose exact
    `drive.readonly` scope cannot be demonstrated — but the **approval check is
    P3's own**.  P1/P2's token is never passed to anything on this route, which
    is the point: reusing a stage's credential path must not reuse its
    permission.
    """
    require_execution_approval(approval, "Google Drive authentication")
    report = P12.check_runtime_dependencies()
    if credential_provider is None and report["missing"]:
        raise P3Error(
            f"refusing to authenticate: {report['missing']} are not "
            f"importable.  {report['note']}")
    if credential_provider is None:                          # pragma: no cover
        credential_provider = P12._colab_readonly_credential
    credential = credential_provider()
    audit = P12.audit_credential_scopes(credential)
    if not audit["exact_readonly_scope_proven"]:
        raise P3Error(
            f"{READONLY_SCOPE_UNPROVEN}: {audit['reason']}.  observed="
            f"{audit['observed_scopes']}.  This PREP does not run under a "
            f"credential whose read-only bound it cannot demonstrate.")
    if service_factory is None:                              # pragma: no cover
        from googleapiclient.discovery import build          # noqa: PLC0415

        def service_factory(credentials):
            return build("drive", "v3", credentials=credentials)
    return service_factory(credential), audit


def build_drive_adapter(approval: Optional[str], credential_provider=None,
                        service_factory=None
                        ) -> Tuple["GoogleDriveFileAdapter", Dict[str, object]]:
    """Authenticate read-only, prove the scope, then hand over the service."""
    service, audit = authenticate_drive_readonly(
        approval, credential_provider=credential_provider,
        service_factory=service_factory)
    return GoogleDriveFileAdapter(approval, service=service), audit


def fetch_registered_source(adapter: DriveFileAdapter, approval: Optional[str],
                            file_id: str = REGISTERED_SOURCE_FILE_ID
                            ) -> RegisteredSourcePermit:
    """File id, then provider inventory, then bytes, then digest — in that order.

    Every step can stop the run and each stop has its own reason.  The
    inventory is taken *before* the download, so a wrong size, a trashed file,
    a shortcut or a folder is refused without transferring anything; the digest
    is checked *before* anything is compiled.

    Returns a :class:`RegisteredSourcePermit` rather than raw bytes: this
    function is the **only** place a permit over the registered source is
    minted, so "these bytes may be executed" cannot be asserted by a caller
    that skipped the gates above.
    """
    require_execution_approval(approval,
                               f"the registered {REGISTERED_SOURCE_NAME}")
    _terminal_execution_guard()
    if file_id != REGISTERED_SOURCE_FILE_ID:
        raise SourceHarnessError(
            P3_SOURCE_FILE_ID_UNREGISTERED,
            f"{file_id!r} is not the registered file id "
            f"{REGISTERED_SOURCE_FILE_ID!r} from ASSETS.md :: "
            f"{REGISTERED_SOURCE_ASSET_ROW}.  A file with the right name is "
            f"not the registered file, and this PREP never searches by name.")
    metadata = adapter.get_metadata(file_id)
    inventory: Dict[str, object] = {
        "file_id": str(metadata.get("id") or ""),
        "requested_file_id": file_id,
        "name": str(metadata.get("name") or ""),
        "bytes": (int(metadata["size"]) if str(metadata.get("size") or "")
                  else None),
        "mime_type": str(metadata.get("mimeType") or ""),
        "modified_time": str(metadata.get("modifiedTime") or ""),
        "provider_sha256": str(metadata.get("sha256Checksum") or "") or None,
        "provider_md5": str(metadata.get("md5Checksum") or "") or None,
        "trashed": bool(metadata.get("trashed")),
        "parents": [str(p) for p in (metadata.get("parents") or ())],
        "is_shortcut": (str(metadata.get("mimeType") or "")
                        == DRIVE_SHORTCUT_MIME
                        or bool(metadata.get("shortcutDetails"))),
        "is_folder": str(metadata.get("mimeType") or "") == DRIVE_FOLDER_MIME,
        "registered_folder_id": REGISTERED_SOURCE_FOLDER_ID,
        "registered_bytes": REGISTERED_SOURCE_BYTES,
        "registered_sha256": REGISTERED_SOURCE_SHA256,
        "asset_row": REGISTERED_SOURCE_ASSET_ROW,
        "read": False,
    }
    problems: List[str] = []
    if inventory["file_id"] != file_id:
        problems.append(f"the provider returned id {inventory['file_id']!r} "
                        f"for a request for {file_id!r}")
    if inventory["trashed"]:
        problems.append("the file at the registered id is in the trash")
    if inventory["is_shortcut"]:
        problems.append("the id resolves to a shortcut, which can point "
                        "anywhere; a shortcut is never the registered file")
    if inventory["is_folder"]:
        problems.append("the id resolves to a folder, not a file")
    if inventory["name"] != REGISTERED_SOURCE_NAME:
        problems.append(f"the file at the registered id is named "
                        f"{inventory['name']!r}, not "
                        f"{REGISTERED_SOURCE_NAME!r}")
    if inventory["bytes"] != REGISTERED_SOURCE_BYTES:
        problems.append(f"the provider reports {inventory['bytes']} bytes and "
                        f"ASSETS registers {REGISTERED_SOURCE_BYTES}")
    # No truthiness guard.  An earlier version only compared the parents when
    # the provider returned some, so a file with **no** observable parent
    # passed this gate and was downloaded — and the contract is that a parent
    # which cannot be confirmed stops the run *before* the transfer, not after
    # it.  "The provider told us nothing" is not the same as "the provider
    # confirmed the registered folder", and only the second one may proceed.
    if REGISTERED_SOURCE_FOLDER_ID not in inventory["parents"]:
        problems.append(f"the file's parents {inventory['parents']} do not "
                        f"include the registered folder id "
                        f"{REGISTERED_SOURCE_FOLDER_ID}; an unconfirmed parent "
                        f"is not a confirmed one")
    if (inventory["provider_sha256"]
            and inventory["provider_sha256"] != REGISTERED_SOURCE_SHA256):
        problems.append(f"the provider checksum {inventory['provider_sha256']} "
                        f"is not the registered {REGISTERED_SOURCE_SHA256}")
    if problems:
        inventory["problems"] = problems
        raise SourceHarnessError(
            P3_SOURCE_IDENTITY_MISMATCH,
            "the registered file id did not resolve to the registered file: "
            + "; ".join(problems) + ".  Nothing was downloaded or executed.")
    body = adapter.download(file_id)
    observed = _sha256_bytes(body)
    inventory.update({"observed_bytes": len(body), "observed_sha256": observed,
                      "read": True, "problems": [],
                      "digest_matches_registered":
                          observed == REGISTERED_SOURCE_SHA256})
    if observed != REGISTERED_SOURCE_SHA256:
        raise SourceHarnessError(
            P3_SOURCE_IDENTITY_MISMATCH,
            f"the bytes read at the registered file id hash to {observed}, "
            f"not the registered {REGISTERED_SOURCE_SHA256}.  They were not "
            f"compiled or executed.")
    if len(body) != REGISTERED_SOURCE_BYTES:                 # pragma: no cover
        raise SourceHarnessError(
            P3_SOURCE_IDENTITY_MISMATCH,
            f"read {len(body)} bytes where {REGISTERED_SOURCE_BYTES} are "
            f"registered")
    return RegisteredSourcePermit(_REGISTERED_PERMIT_KEY, body, inventory,
                                  approval)


# ─────────────────────────────────────────────────────────────────────────────
# Bundle.  Publication reuses the P1/P2 contract: exclusive creation, no
# overwrite, no delete, no rename, and a commit marker written last.
# ─────────────────────────────────────────────────────────────────────────────
def build_config(timestamp: str, synthetic: bool,
                 auth_audit: Optional[Mapping[str, object]] = None
                 ) -> Dict[str, object]:
    """The run's own description, including the environment it happened in."""
    return {
        "experiment_id": EXPERIMENT_ID, "substage": SUBSTAGE,
        "run_slug": RUN_SLUG, "module_version": MODULE_VERSION,
        "timestamp": timestamp, "spec": SPEC_PATH,
        "parent_spec": PARENT_SPEC_PATH, "p1_p2_contract": P1_P2_CONTRACT_PATH,
        "scope": ["P3"], "p1_p2_in_scope": False,
        "runtime": P12.runtime_identity(),
        "dependencies": P12.check_runtime_dependencies(),
        "drive_authentication": (dict(auth_audit) if auth_audit else {
            "performed": False,
            "requested_scopes": [DRIVE_READONLY_SCOPE],
            "exact_readonly_scope_proven": False,
            "reason": ("no Drive authentication was performed on this route; "
                       "nothing was proven and nothing is claimed")}),
        "synthetic_fixture": bool(synthetic),
        "ingestable": not synthetic,
        "synthetic_note": (SYNTHETIC_NOTE if synthetic else None),
        "registered_targets": {
            "source_name": REGISTERED_SOURCE_NAME,
            "source_function": REGISTERED_SOURCE_FUNCTION,
            "source_file_id": REGISTERED_SOURCE_FILE_ID,
            "source_folder_id": REGISTERED_SOURCE_FOLDER_ID,
            "source_bytes": REGISTERED_SOURCE_BYTES,
            "source_sha256": REGISTERED_SOURCE_SHA256,
            "asset_row": REGISTERED_SOURCE_ASSET_ROW,
            "adapter_fingerprint": Q5E.source_match_adapter_fingerprint(),
            "oracle_record_registered":
                Q5E.SOURCE_MATCH_ORACLE_RECORD is not None,
            "required_fixtures": list(REQUIRED_FIXTURES)},
        "not_performed": [
            "detect_r() or any real detector",
            "any real ECG signal, V9/V10 cache or real-record count",
            "M0-M4 aggregation", "DS2 per-beat labels", "V10 probabilities",
            "association or S PR-AUC", "training of any kind",
            "registration of SOURCE_MATCH_ORACLE_RECORD",
            "any correction of the candidate adapter"],
        "approval_note": APPROVAL_NOTE,
        "approval_record": dict(EXECUTION_APPROVAL_RECORD),
    }


def summary_markdown(decision: Mapping[str, object], synthetic: bool) -> str:
    lines = [f"# {EXPERIMENT_ID} / Q5-E PREP P3 - source-match equivalence", ""]
    if synthetic:
        lines += [f"> **{SYNTHETIC_NOTE}**", ""]
    lines += [
        f"- status: `{decision.get('status')}`",
        f"- first failure: `{decision.get('first_failure')}`",
        f"- fixtures passed: {decision.get('fixtures_passed')} of "
        f"{decision.get('fixtures_total')}",
        f"- harness stop: {decision.get('harness_stop')}",
        f"- candidate derivable from this bundle: "
        f"{decision.get('candidate_derivable')}",
        "",
        "The oracle is the registered `data.py :: build_record` itself, run",
        "under synthetic dependency injection and observed mechanically. No",
        "second reimplementation of the matching rule was used as an oracle,",
        "and per-record counts were neither opened nor consulted.",
        "",
        "This is a read-only PREP. No detector ran, no real ECG signal, cache,",
        "label or probability was opened, and nothing was registered:",
        "`SOURCE_MATCH_ORACLE_RECORD` is unchanged. Any candidate becomes a",
        "registration only through a separate PR after Codex accepts the run.",
        "",
        "The candidate's `prep_bundle_sha256` is this bundle's payload fold,",
        "so the candidate itself is not stored inside the bundle it would",
        "have to describe. It is reported by the run and frozen outside.",
    ]
    return "\n".join(lines) + "\n"


def write_bundle(directory: str, config: Mapping[str, object],
                 source_inventory: Mapping[str, object],
                 harness: Mapping[str, object],
                 fixture_results: Mapping[str, object],
                 decision: Mapping[str, object], log_lines: Sequence[str],
                 synthetic: bool = False) -> Dict[str, object]:
    """Claim the directory, fill it, commit it with a marker written last.

    The publication contract is P1/P2's, deliberately and by reuse: exclusive
    creation for every file, `mkdir` to claim the name so nothing pre-existing
    is replaced, no delete and no rename anywhere, and `COMMITTED.json` last —
    a directory without it is a failed write, not a bundle.  A failed run
    leaves its partial directory exactly where it is, because that is where a
    diagnosis will look for it.
    """
    payload: Dict[str, object] = {
        "config.json": dict(config),
        "source_inventory.json": dict(source_inventory),
        "oracle_harness_identity.json": dict(harness),
        "fixture_results.json": dict(fixture_results),
        "decision.json": dict(decision),
    }
    for name, value in payload.items():
        P12.assert_no_credentials(value, name)

    parent = os.path.dirname(os.path.abspath(directory)) or "."
    os.makedirs(parent, exist_ok=True)
    if P12._is_link_like(parent):
        raise P3Error(
            f"refusing to publish under {parent!r}: it is a symlink or "
            f"reparse point, and this function does not follow links")
    try:
        os.mkdir(directory)
    except FileExistsError as error:
        raise P3Error(
            f"refusing to publish to {directory!r}: something is already "
            f"there.  A PREP bundle is new, never an overwrite, and nothing "
            f"pre-existing is deleted, renamed or replaced.") from error
    try:
        for name, value in payload.items():
            P12._write_new_json(os.path.join(directory, name), value)
        P12._write_new_file(
            os.path.join(directory, "log.txt"),
            ("\n".join(str(line) for line in log_lines) + "\n").encode("utf-8"))
        P12._write_new_file(
            os.path.join(directory, "summary.md"),
            summary_markdown(decision, synthetic).encode("utf-8"))

        written = sorted(os.listdir(directory))
        if written != sorted(PREP_PAYLOAD_FILES):
            raise P3Error(
                f"refusing to commit: the written file set {written} is not "
                f"the contracted payload {sorted(PREP_PAYLOAD_FILES)}.  A file "
                f"outside the payload identity would be unaccounted for.")
        triples = []
        for name in written:
            with open(os.path.join(directory, name), "rb") as handle:
                body = handle.read()
            triples.append({"name": name, "bytes": len(body),
                            "sha256": _sha256_bytes(body)})
        fold = Q5E.prep_payload_fold(triples)
        if not fold["complete"]:                             # pragma: no cover
            raise P3Error(f"the payload fold is incomplete: {fold}")
        manifest = {
            "experiment_id": EXPERIMENT_ID, "substage": SUBSTAGE,
            "timestamp": config.get("timestamp"),
            "prep_payload_sha256": fold["prep_payload_sha256"],
            "payload_files": list(PREP_PAYLOAD_FILES),
            "excluded_from_payload_fold": [PREP_MANIFEST_FILE, COMMIT_MARKER],
            "manifest_self_digest_recorded_here": False,
            "manifest_self_digest_frozen_externally": True,
            "synthetic_fixture": bool(synthetic),
            "ingestable": not synthetic,
            "status": decision.get("status"),
            "oracle_harness_sha256": harness.get("oracle_harness_sha256"),
            "module_sha256": Q5E.sha256_file(os.path.abspath(__file__)),
            "frozen_module_sha256": Q5E.sha256_file(
                os.path.abspath(BJ.__file__)),
            "runtime": config.get("runtime"),
            "drive_authentication": config.get("drive_authentication"),
            "note": ("manifest.json is excluded from the fold it records; its "
                     "own SHA-256 is frozen outside this bundle, in the saved "
                     "report cell and the registration record"),
        }
        P12.assert_no_credentials(manifest, PREP_MANIFEST_FILE)
        manifest_digest = _sha256_bytes(P12._write_new_json(
            os.path.join(directory, PREP_MANIFEST_FILE), manifest))

        before_commit = sorted(os.listdir(directory))
        expected_before = sorted(set(BUNDLE_FILES) - {COMMIT_MARKER})
        if before_commit != expected_before:                 # pragma: no cover
            raise P3Error(f"refusing to commit: file set {before_commit} != "
                          f"{expected_before}")
        marker = {
            "committed": True,
            "experiment_id": EXPERIMENT_ID, "substage": SUBSTAGE,
            "timestamp": config.get("timestamp"),
            "bundle_files": sorted(BUNDLE_FILES),
            "payload_files": list(PREP_PAYLOAD_FILES),
            "prep_payload_sha256": fold["prep_payload_sha256"],
            "manifest_sha256_recorded_here": False,
            "manifest_sha256_frozen_externally": True,
            "synthetic_fixture": bool(synthetic),
            "ingestable": not synthetic,
            "status": decision.get("status"),
            "note": ("a bundle directory without this marker is an incomplete "
                     "or failed write, not a bundle; verify_published_bundle() "
                     "refuses it"),
        }
        P12.assert_no_credentials(marker, COMMIT_MARKER)
        P12._write_new_json(os.path.join(directory, COMMIT_MARKER), marker)
        final_set = sorted(os.listdir(directory))
        if final_set != sorted(BUNDLE_FILES):                # pragma: no cover
            raise P3Error(f"refusing to report a publish: final file set "
                          f"{final_set} != {sorted(BUNDLE_FILES)}")
    except Exception as error:
        raise P3Error(
            f"the P3 PREP bundle was not committed: {error}.  The partial "
            f"directory is preserved at {directory!r}; it carries no "
            f"{COMMIT_MARKER}, so no consumer will accept it, and nothing was "
            f"deleted or replaced.") from error
    return {"directory": directory, "written": final_set,
            "payload_files": list(PREP_PAYLOAD_FILES),
            "prep_payload_sha256": fold["prep_payload_sha256"],
            "manifest_sha256_freeze_externally": manifest_digest,
            "committed": True}


def verify_published_bundle(directory: str,
                            expected_manifest_sha256: Optional[str] = None,
                            manifest_anchor_source: Optional[str] = None
                            ) -> Dict[str, object]:
    """The consumer's contract: is this directory a committed P3 bundle?

    The marker is checked rather than trusted — every set is compared with the
    fixed code contract and cross-checked between the marker and the manifest,
    and only the recomputed fold counts.  `manifest.json` is outside the fold,
    so it is anchored only by a digest whose origin the caller states; a run
    checking its own freshly computed value is a self-check, not an anchor.
    """
    problems: List[str] = []
    source = manifest_anchor_source
    if expected_manifest_sha256 is None:
        if source not in (None, ANCHOR_NONE):
            problems.append(
                f"manifest_anchor_source is {source!r} but no "
                f"expected_manifest_sha256 was supplied; an origin without a "
                f"value is not an anchor")
        source = ANCHOR_NONE
    elif source is None or source == "":
        problems.append(
            "a manifest digest was supplied without a manifest_anchor_source; "
            f"it must be one of {list(MANIFEST_ANCHOR_SOURCES)}")
        source = None
    elif source not in MANIFEST_ANCHOR_SOURCES:
        problems.append(f"manifest_anchor_source {source!r} is not one of "
                        f"{list(MANIFEST_ANCHOR_SOURCES)}")
        source = None
    elif source == ANCHOR_NONE:
        problems.append(f"manifest_anchor_source is {ANCHOR_NONE!r} but a "
                        f"digest was supplied; say where it came from or do "
                        f"not pass it")
        source = None

    def verdict(**extra) -> Dict[str, object]:
        structure_ok = not problems
        matches = extra.get("manifest_digest_matches_expected")
        external = bool(source in EXTERNAL_MANIFEST_ANCHORS
                        and matches is True and structure_ok)
        out: Dict[str, object] = {
            "directory": directory, "problems": problems,
            "ok": structure_ok, "structure_ok": structure_ok,
            "manifest_anchor_source": source,
            "manifest_anchored_externally": external,
            "acceptance_eligible": structure_ok and external,
        }
        out.setdefault("manifest_digest_matches_expected", None)
        out.update(extra)
        return out

    marker_path = os.path.join(directory, COMMIT_MARKER)
    if not os.path.isfile(marker_path):
        problems.append(
            f"{COMMIT_MARKER} is absent: this is an incomplete or failed "
            f"write, not a bundle.  It is not accepted, and it is not deleted "
            f"either.")
        return verdict(committed=False, prep_payload_sha256=None,
                       manifest_sha256=None, synthetic_fixture=None)
    marker, error = P12._load_json(marker_path, COMMIT_MARKER)
    if error:
        problems.append(error)
        return verdict(committed=False, prep_payload_sha256=None,
                       manifest_sha256=None, synthetic_fixture=None)
    manifest_path = os.path.join(directory, PREP_MANIFEST_FILE)
    manifest, error = P12._load_json(manifest_path, PREP_MANIFEST_FILE)
    if error:
        problems.append(error)
        manifest = {}
    manifest_digest = None
    if os.path.isfile(manifest_path):
        with open(manifest_path, "rb") as handle:
            manifest_digest = _sha256_bytes(handle.read())
    else:
        problems.append(f"{PREP_MANIFEST_FILE} is missing")

    if marker.get("committed") is not True:
        problems.append(
            f"{COMMIT_MARKER}: committed is {marker.get('committed')!r}, not "
            f"True.  This directory does not claim to be a finished bundle.")

    def _strict_bool(label: str, record: Mapping[str, object],
                     field: str) -> Optional[bool]:
        if field not in record:
            problems.append(f"{label}: {field} is missing")
            return None
        value = record[field]
        if type(value) is not bool:                          # noqa: E721
            problems.append(
                f"{label}: {field} is {value!r} ({type(value).__name__}), not "
                f"a JSON boolean; truthiness is not accepted here")
            return None
        return value

    flags: Dict[str, Optional[bool]] = {}
    for label, record in ((COMMIT_MARKER, marker),
                          (PREP_MANIFEST_FILE, manifest)):
        synth = _strict_bool(label, record, "synthetic_fixture")
        ingest = _strict_bool(label, record, "ingestable")
        if synth is not None and ingest is not None and ingest is not (
                not synth):
            problems.append(
                f"{label}: ingestable {ingest!r} is not the negation of "
                f"synthetic_fixture {synth!r}")
        flags[label] = synth
    if (flags[COMMIT_MARKER] is not None
            and flags[PREP_MANIFEST_FILE] is not None
            and flags[COMMIT_MARKER] is not flags[PREP_MANIFEST_FILE]):
        problems.append(
            f"synthetic_fixture disagrees: {COMMIT_MARKER} says "
            f"{flags[COMMIT_MARKER]!r}, {PREP_MANIFEST_FILE} says "
            f"{flags[PREP_MANIFEST_FILE]!r}")

    observed = sorted(os.listdir(directory))
    if observed != sorted(BUNDLE_FILES):
        problems.append(f"file set {observed} != the contracted set "
                        f"{sorted(BUNDLE_FILES)}")
    for label, record in ((COMMIT_MARKER, marker),
                          (PREP_MANIFEST_FILE, manifest)):
        declared = sorted(str(n) for n in record.get("payload_files") or ())
        if declared != sorted(PREP_PAYLOAD_FILES):
            problems.append(f"{label}: payload_files {declared} != the "
                            f"contracted {sorted(PREP_PAYLOAD_FILES)}")
    marker_bundle = sorted(str(n) for n in marker.get("bundle_files") or ())
    if marker_bundle != sorted(BUNDLE_FILES):
        problems.append(f"{COMMIT_MARKER}: bundle_files {marker_bundle} != the "
                        f"contracted {sorted(BUNDLE_FILES)}")
    for field, constant in (("experiment_id", EXPERIMENT_ID),
                            ("substage", SUBSTAGE)):
        for label, record in ((COMMIT_MARKER, marker),
                              (PREP_MANIFEST_FILE, manifest)):
            if record.get(field) != constant:
                problems.append(f"{label}: {field} {record.get(field)!r} != "
                                f"{constant!r}")
    stamps = {}
    for label, record in ((COMMIT_MARKER, marker),
                          (PREP_MANIFEST_FILE, manifest)):
        value = record.get("timestamp")
        if type(value) is not str:                           # noqa: E721
            problems.append(f"{label}: timestamp is {value!r} "
                            f"({type(value).__name__}), not the contracted "
                            f"string")
        else:
            stamps[label] = value
    if len(stamps) == 2 and len(set(stamps.values())) != 1:
        problems.append(f"timestamp disagrees: {COMMIT_MARKER} says "
                        f"{stamps[COMMIT_MARKER]!r}, {PREP_MANIFEST_FILE} says "
                        f"{stamps[PREP_MANIFEST_FILE]!r}")

    triples = []
    for name in sorted(PREP_PAYLOAD_FILES):
        path = os.path.join(directory, name)
        if not os.path.isfile(path):
            problems.append(f"payload file {name!r} is missing")
            continue
        with open(path, "rb") as handle:
            body = handle.read()
        triples.append({"name": name, "bytes": len(body),
                        "sha256": _sha256_bytes(body)})
    fold = (Q5E.prep_payload_fold(triples)["prep_payload_sha256"]
            if len(triples) == len(PREP_PAYLOAD_FILES) else None)
    for label, record in ((COMMIT_MARKER, marker),
                          (PREP_MANIFEST_FILE, manifest)):
        if fold != record.get("prep_payload_sha256"):
            problems.append(f"recomputed payload fold {fold} != {label}'s "
                            f"{record.get('prep_payload_sha256')}")
    if PREP_MANIFEST_FILE in PREP_PAYLOAD_FILES:             # pragma: no cover
        problems.append(f"{PREP_MANIFEST_FILE} must not be inside the fold it "
                        f"records")

    matches = None
    if expected_manifest_sha256 is not None:
        matches = (manifest_digest is not None
                   and manifest_digest == expected_manifest_sha256)
        if not matches:
            problems.append(f"manifest digest {manifest_digest} != the "
                            f"{source or 'given'} digest "
                            f"{expected_manifest_sha256}")
    return verdict(committed=marker.get("committed") is True,
                   prep_payload_sha256=fold, manifest_sha256=manifest_digest,
                   expected_manifest_sha256=expected_manifest_sha256,
                   manifest_digest_matches_expected=matches,
                   synthetic_fixture=flags[COMMIT_MARKER])


# ─────────────────────────────────────────────────────────────────────────────
# Decision and entry points.
# ─────────────────────────────────────────────────────────────────────────────
def decide(differential: Optional[Mapping[str, object]],
           harness_stop: Optional[str] = None,
           harness_detail: Optional[str] = None,
           precheck: Optional[Mapping[str, object]] = None
           ) -> Dict[str, object]:
    """The run's verdict, keeping harness failures out of the science.

    A harness stop is reported as itself.  Only a completed differential can
    say `SOURCE_MATCH_EQUIVALENCE_REQUIRED`, and only one in which every
    fixture agreed *and* whose candidate the registered gate accepts
    structurally can say `SOURCE_MATCH_EQUIVALENT_TO_REGISTERED_SOURCE`.
    """
    if harness_stop is not None:
        return {
            "status": harness_stop, "first_failure": harness_stop,
            "harness_stop": True, "detail": harness_detail,
            "fixtures_passed": None, "fixtures_total": len(REQUIRED_FIXTURES),
            "candidate_derivable": False, "candidate_gate_ok": False,
            "equivalence_claimed": False,
            "adapter_modified_by_this_run": False,
            "real_record_counts_opened": False,
            "note": ("the comparison was not made.  This is not a "
                     "disagreement between the adapter and the registered "
                     "source and must not be reported as one"),
            "next_step": "resolve the harness stop and re-run the full fixture "
                         "set from the beginning",
        }
    differential = differential or {}
    all_equal = bool(differential.get("all_equal"))
    gate_ok = bool((precheck or {}).get("ok"))
    status = P3_PASS if (all_equal and gate_ok) else P3_EQUIVALENCE_REQUIRED
    return {
        "status": status,
        "first_failure": (None if status == P3_PASS
                          else (differential.get("first_failing_fixture")
                                or P3_EQUIVALENCE_REQUIRED)),
        "harness_stop": False, "detail": None,
        "fixtures_passed": differential.get("fixtures_passed"),
        "fixtures_total": differential.get("fixtures_total"),
        "candidate_derivable": all_equal and gate_ok,
        "candidate_gate_ok": gate_ok,
        "candidate_structure_precheck": dict(precheck or {}),
        "equivalence_claimed": status == P3_PASS,
        "adapter_modified_by_this_run": False,
        "real_record_counts_opened": False,
        "candidate_recorded_in_this_bundle": False,
        "note": ("a PASS here is the structural result of this differential; "
                 "it is not a registration and not a Codex acceptance.  On any "
                 "disagreement the adapter is left exactly as it is and a "
                 "correction is a separate PR.  The candidate record is not "
                 "stored in this bundle because its prep_bundle_sha256 is this "
                 "bundle's own payload fold"),
        "next_step": ("hand the bundle and the reported candidate to Codex for "
                      "a separate registration PR" if status == P3_PASS else
                      "preserve the mismatch trace; a corrected adapter is a "
                      "separate PR and a full re-run"),
    }


def _execute_with_permit(out_dir: str, permit: SourcePermit,
                         timestamp: str = "", emit=print,
                         adapter: Optional[Callable] = None,
                         auth_audit: Optional[Mapping[str, object]] = None
                         ) -> Dict[str, object]:
    """Load, compare, decide, publish, then derive the candidate.

    **Private on purpose.**  An earlier version was a public entry point
    taking raw bytes, an arbitrary inventory and a token string, and it
    checked neither barrier — so a caller with the public token could compile
    and execute the registered source, and write a bundle, while the terminal
    guard was closed.  It now takes a :class:`SourcePermit`, which cannot
    exist over the registered bytes unless both barriers were open and the
    file-id and digest gates passed, and the two public entry points are
    :func:`run_p3` (registered, guarded) and :func:`execute_synthetic_p3`
    (fixture bytes, provably not the registered file).

    The candidate's `prep_bundle_sha256` is the bundle's payload fold, so the
    candidate cannot live inside the bundle it describes.  The order here is
    the consequence: the differential is checked against the registered gate
    with a placeholder fold *before* publication, the bundle records that
    pre-check, and the real candidate is assembled from the published fold
    afterwards and reported for external freezing.
    """
    validate_permit_for_execution(permit)
    synthetic = bool(permit.synthetic)
    source_inventory = dict(permit.inventory)
    log: List[str] = [
        f"scope=P3 synthetic={synthetic}",
        f"permit={permit.kind} source={permit.label} "
        f"file_id={source_inventory.get('requested_file_id')}",
        f"registered_sha256={source_inventory.get('registered_sha256')}",
        f"observed_sha256={source_inventory.get('observed_sha256')}"]

    def record(message: str) -> None:
        log.append(str(message))
        emit(message)

    harness = oracle_harness_identity()
    expected_digest = permit.sha256
    stop: Optional[str] = None
    detail: Optional[str] = None
    stop_context: Dict[str, object] = {}
    differential: Optional[Dict[str, object]] = None
    try:
        differential = differential_over_fixtures(
            source_factory(permit), adapter=adapter, emit=record)
    except SourceHarnessError as error:
        stop, detail = error.status, error.detail
        stop_context = dict(error.context)
        record(f"harness stop: {stop}: {detail}")

    precheck = check_candidate_against_gate(candidate_record(
        differential or {}, expected_digest, PLACEHOLDER_FOLD,
        str(harness["oracle_harness_sha256"])))
    precheck["placeholder_prep_bundle_sha256"] = True
    decision = decide(differential, stop, detail, precheck)
    fixture_results = {
        "required_fixtures": list(REQUIRED_FIXTURES),
        "fixtures": (list(differential["fixtures"]) if differential else []),
        "detail": (list(differential["detail"]) if differential else []),
        "label_dictionary": (differential.get("label_dictionary")
                             if differential else {}),
        "stub_invariance": (differential.get("stub_invariance")
                            if differential else {}),
        # A stop leaves `detail` empty, and the reading of the return is then
        # the only thing that says why.  It is preserved inside the existing
        # contracted file rather than in a new one, so the payload fold is
        # unchanged and the diagnosis is still covered by it.
        "harness_stop_context": dict(stop_context),
        "synthetic_fixture": bool(synthetic),
        "note": (SYNTHETIC_NOTE if synthetic else
                 "the fixture inputs are synthetic by design; the producer "
                 "under test is the registered source"),
    }
    directory = os.path.join(out_dir, f"{timestamp}_{RUN_SLUG}")
    written = write_bundle(directory,
                           build_config(timestamp, synthetic, auth_audit),
                           source_inventory, harness, fixture_results, decision,
                           log, synthetic=synthetic)
    verified = verify_published_bundle(
        written["directory"],
        expected_manifest_sha256=written["manifest_sha256_freeze_externally"],
        manifest_anchor_source=ANCHOR_SAME_RUN)
    if not verified["ok"]:                                   # pragma: no cover
        raise P3Error(
            f"the bundle at {written['directory']!r} does not pass the "
            f"consumer contract: {verified['problems']}.  It is left in place "
            f"and nothing was deleted.")
    candidate = (None if synthetic else candidate_record(
        differential or {}, expected_digest, written["prep_payload_sha256"],
        str(harness["oracle_harness_sha256"])))
    gate = check_candidate_against_gate(candidate)
    if candidate is not None and gate["ok"] is not precheck["ok"]:
        # The published decision was written from the pre-check, so the two
        # must agree.  If they ever did not, the bundle would state a verdict
        # the finished candidate does not support.
        raise P3Error(                                       # pragma: no cover
            f"the candidate built from the published fold is judged "
            f"{gate['ok']} where the pre-check said {precheck['ok']}: "
            f"{gate['problems']}.  The bundle at {written['directory']!r} is "
            f"left in place and nothing was registered.")
    if synthetic and differential and differential.get("all_equal"):
        gate["note"] = ("a synthetic run produces no candidate at all: it "
                        "compared a synthetic producer, not the registered "
                        "data.py, and must never yield something registrable")
    emit(f"status: {decision['status']}")
    emit(f"bundle committed, payload fold: {written['prep_payload_sha256']}")
    emit(f"SOURCE_MATCH_ORACLE_RECORD is still "
         f"{Q5E.SOURCE_MATCH_ORACLE_RECORD!r}: this run registers nothing.")
    return {"decision": decision, "differential": differential,
            "candidate": candidate, "candidate_gate": gate,
            "candidate_precheck": precheck, "harness": harness,
            # Returned as well as published: on a stop this is the only thing
            # that says why, and making the caller open the bundle to read it
            # is what turned each of the last four stops into a round trip.
            "fixture_results": fixture_results,
            "bundle": written, "verified": verified,
            "permit": permit.describe(),
            "source_inventory": dict(source_inventory)}


def execute_synthetic_p3(out_dir: str, producer_body: bytes,
                         timestamp: str = "", emit=print,
                         adapter: Optional[Callable] = None,
                         source_label: str = "synthetic.py"
                         ) -> Dict[str, object]:
    """Run the whole route over a **fixture's own** producer bytes.

    This is how the harness is exercised without the registered source, and it
    cannot become a way to reach the registered source: the permit it builds
    refuses bytes whose digest is the registered `data.py`, so no argument to
    this function can make it execute that file.  Every bundle it writes is
    stamped synthetic inside the folded payload, is never ingestable, and
    never produces a `SOURCE_MATCH_ORACLE_RECORD` candidate.
    """
    permit = synthetic_permit(producer_body, label=source_label)
    return _execute_with_permit(out_dir, permit, timestamp=timestamp,
                                emit=emit, adapter=adapter)


def _execute_registered_p3(out_dir: str, permit: RegisteredSourcePermit,
                           timestamp: str = "", emit=print,
                           auth_audit: Optional[Mapping[str, object]] = None
                           ) -> Dict[str, object]:   # pragma: no cover
    """The production run, reachable only from `run_p3()` past the guard."""
    if type(permit) is not RegisteredSourcePermit:            # noqa: E721
        raise P3NotApprovedError(
            "the registered route runs only from a RegisteredSourcePermit, "
            "which fetch_registered_source() mints after the guard and the id "
            "and digest gates.  The type is compared by identity: a subclass "
            f"inherits the name and none of the checks.  {APPROVAL_NOTE}")
    validate_permit_for_execution(permit)
    return _execute_with_permit(out_dir, permit, timestamp=timestamp,
                                emit=emit, auth_audit=auth_audit)


def run_p3(out_dir: str, timestamp: str = "",
           adapter_source: Optional[DriveFileAdapter] = None,
           approval: Optional[str] = None,
           open_registered_data: bool = OPEN_REGISTERED_DATA,
           file_id: str = REGISTERED_SOURCE_FILE_ID,
           emit=print) -> Dict[str, object]:
    """The single production route.  Two barriers, then identity, then the read.

    The order is fixed and it is the point of the function: the switch, this
    PREP's own token (another stage's token is refused by name), the file id,
    the fixture contract, the **terminal guard**, then dependencies, then a
    credential, then the Drive service, and only then the metadata lookup, the
    download, the digest check and the load.  An unapproved call performs zero
    authentication attempts, makes zero API calls, reads zero registered bytes
    and creates no output directory.
    """
    if not open_registered_data:
        raise P3NotApprovedError(
            f"OPEN_REGISTERED_DATA is False.  This is the committed default: a "
            f"stray import or notebook run cannot reach the registered "
            f"{REGISTERED_SOURCE_NAME}.  {APPROVAL_NOTE}")
    require_execution_approval(approval,
                              f"the P3 differential over {out_dir!r}")
    if file_id != REGISTERED_SOURCE_FILE_ID:
        raise SourceHarnessError(
            P3_SOURCE_FILE_ID_UNREGISTERED,
            f"{file_id!r} is not the registered file id "
            f"{REGISTERED_SOURCE_FILE_ID!r}.  This is not a general-purpose "
            f"file reader and it never falls back to a name search.")
    gate = assert_fixture_contract()
    emit(f"Q5-E PREP P3: approval present; {gate['n_fixtures']} registered "
         f"fixtures; nothing has been opened yet.")

    # Everything below runs only once the guard is open, which it is not in
    # this PR.  It is complete all the same: the execution PR changes one
    # field in EXECUTION_APPROVAL_RECORD and writes no new route.
    granted = _terminal_execution_guard()
    return _run_p3_after_the_guard(                           # pragma: no cover
        out_dir, timestamp, adapter_source, approval, file_id, granted, emit)


def _run_p3_after_the_guard(out_dir: str, timestamp: str,
                            adapter_source: Optional[DriveFileAdapter],
                            approval: Optional[str], file_id: str,
                            granted: Mapping[str, object],
                            emit) -> Dict[str, object]:   # pragma: no cover
    """The approved route: authenticate, fetch by id, verify, then compare."""
    emit(f"read-only execution approval: granted {granted.get('granted_on')} "
         f"by {granted.get('granted_by')} — {granted.get('kind')}.")
    emit(f"not approved by it: {', '.join(granted['not_approved'])}.")
    auth_audit = None
    if adapter_source is None:
        adapter_source, auth_audit = build_drive_adapter(approval)
        emit(f"Drive scope proven read-only: "
             f"{auth_audit['exact_readonly_scope_proven']}")
    permit = fetch_registered_source(adapter_source, approval, file_id)
    emit(f"registered {REGISTERED_SOURCE_NAME} verified by id and digest: "
         f"{permit.sha256}")
    return _execute_registered_p3(out_dir, permit, timestamp=timestamp,
                                  emit=emit, auth_audit=auth_audit)


def module_capabilities() -> Tuple[str, ...]:
    """Names a notebook asserts before use, so a stale clone cannot masquerade."""
    return ("run_p3", "execute_synthetic_p3", "differential_over_fixtures",
            "observe_source", "observe_adapter", "project_observation",
            "trace_call", "growth_events", "implied_mappings", "merge_implied",
            "discover_kept_rows", "build_injection", "InjectedModules",
            "load_source_under_injection", "ProducerSession", "SourcePermit",
            "RegisteredSourcePermit", "SyntheticSourcePermit",
            "synthetic_permit", "validate_permit_for_execution",
            "binding_values", "BINDING_PLAN", "BINDING_RATIONALE",
            "probe_injection_invariance", "describe_returned",
            "FRONTEND_STUB_FUNCTIONS",
            "STUB_VARIANTS",
            "assert_registered_provenance",
            "source_factory", "bind_source_arguments",
            "fetch_registered_source", "oracle_harness_identity",
            "candidate_record", "check_candidate_against_gate",
            "assert_fixture_contract", "fixture_card", "decide", "write_bundle",
            "verify_published_bundle", "build_drive_adapter",
            "authenticate_drive_readonly", "DriveFileAdapter",
            "GoogleDriveFileAdapter", "design_card", "FIXTURES",
            "REQUIRED_FIXTURES", "P3_GATE_ORDER", "P3_STATUSES",
            "HARNESS_STOPS", "EXECUTION_APPROVAL_TOKEN",
            "EXECUTION_APPROVAL_RECORD", "REFUSED_TOKENS",
            "OPEN_REGISTERED_DATA", "REGISTERED_SOURCE_FILE_ID",
            "REGISTERED_SOURCE_SHA256", "COMMIT_MARKER", "PREP_PAYLOAD_FILES",
            "BUNDLE_FILES")


def _approval_line() -> str:
    if not EXECUTION_APPROVAL_RECORD.get("granted"):
        withdrawn = EXECUTION_APPROVAL_RECORD.get("withdrawn_on")
        if withdrawn:
            return (f"WITHDRAWN {withdrawn} - the approval of "
                    f"{EXECUTION_APPROVAL_RECORD.get('granted_on')} was for a "
                    f"different oracle harness and does not carry over")
        return "NOT APPROVED (implementation only)"
    return (f"APPROVED {EXECUTION_APPROVAL_RECORD['granted_on']} by "
            f"{EXECUTION_APPROVAL_RECORD['granted_by']} (read-only)")


def design_card() -> str:
    """A constants card that opens nothing.  Safe to print anywhere."""
    lines = [
        f"{EXPERIMENT_ID} / {SUBSTAGE} - read-only differential, not a result",
        f"  spec                 : {SPEC_PATH}",
        f"  parent spec          : {PARENT_SPEC_PATH}",
        f"  registered source    : {REGISTERED_SOURCE_NAME} :: "
        f"{REGISTERED_SOURCE_FUNCTION}",
        f"  source file id       : {REGISTERED_SOURCE_FILE_ID}",
        f"  source folder id     : {REGISTERED_SOURCE_FOLDER_ID}",
        f"  source sha256        : {REGISTERED_SOURCE_SHA256}",
        f"  source bytes         : {REGISTERED_SOURCE_BYTES}",
        f"  adapter fingerprint  : {Q5E.source_match_adapter_fingerprint()}",
        f"  oracle harness sha256: "
        f"{oracle_harness_identity()['oracle_harness_sha256']}",
        "  oracle               : the registered source itself, executed "
        "under injection",
        f"  required fixtures    : {len(REQUIRED_FIXTURES)}",
        f"  OPEN_REGISTERED_DATA : {OPEN_REGISTERED_DATA}",
        f"  execution approval   : {_approval_line()}",
        f"  approval bound to    : "
        f"{EXECUTION_APPROVAL_RECORD.get('for_oracle_harness_sha256')}",
        f"  ORACLE_RECORD        : {Q5E.SOURCE_MATCH_ORACLE_RECORD!r} "
        f"(unchanged by this module)",
        "",
        "  Fixtures and what each one refutes:",
    ]
    for name in fixture_names():
        lines.append(f"   - {name}")
        lines.append(f"     {FIXTURES_BY_NAME[name]['refutes']}")
    lines += ["", f"  {APPROVAL_NOTE}"]
    return "\n".join(lines)


def main(argv: Optional[Sequence[str]] = None) -> int:        # pragma: no cover
    import argparse
    parser = argparse.ArgumentParser(
        description=f"{EXPERIMENT_ID} Q5-E PREP P3")
    parser.add_argument(EXECUTION_APPROVAL_FLAG, action="store_true",
                        dest="approved")
    args = parser.parse_args(argv)
    print(design_card())
    if not args.approved:
        print(f"\nSKIP: {APPROVAL_NOTE}")
        return 2
    print("\nApproval flag present.  This CLI still runs nothing: the "
          "differential is executed from the notebook, which supplies the "
          "output directory, and the terminal guard is still closed.")
    return 2


if __name__ == "__main__":                                    # pragma: no cover
    raise SystemExit(main())
