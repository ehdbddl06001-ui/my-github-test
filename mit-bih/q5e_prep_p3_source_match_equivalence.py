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
#: Stops that say the harness could not make the comparison.  A candidate
#: record is never produced from one of these, and none of them may be
#: reported as a disagreement between the adapter and the registered source.
HARNESS_STOPS: Tuple[str, ...] = (
    P3_SOURCE_FILE_ID_UNREGISTERED, P3_SOURCE_IDENTITY_MISMATCH,
    P3_SOURCE_UNLOADABLE, P3_SOURCE_SIGNATURE_UNBINDABLE,
    P3_SOURCE_RUNTIME_ERROR, P3_SOURCE_TRACE_UNPROJECTABLE,
    P3_KEPT_ROWS_UNOBSERVABLE, P3_FIXTURE_CONTRACT_VIOLATION)
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

#: Barrier 2.  `granted: False` is the committed state.  An execution PR flips
#: this one field and changes nothing else; the value records who approved
#: what, so an opened barrier still says why it is open.
EXECUTION_APPROVAL_RECORD: Dict[str, object] = {
    "granted": False,
    "granted_on": None,
    "granted_by": None,
    "kind": ("read-only execution of EXP-2026-008 Q5-E PREP P3: the candidate "
             "adapter against the registered data.py under synthetic "
             "dependency injection"),
    "would_approve": (
        f"reading the registered {REGISTERED_SOURCE_NAME} by file id "
        f"{REGISTERED_SOURCE_FILE_ID} under exactly the drive.readonly scope",
        "loading it into an isolated namespace with synthetic stubs injected",
        "calling its build_record on the six registered synthetic fixtures",
        "writing the P3 PREP result bundle",
    ),
    "not_approved": NOT_APPROVED,
    "recorded_in": SPEC_PATH,
}
APPROVAL_NOTE = (
    "P3 is implemented but NOT approved for execution.  Reaching the "
    f"registered {REGISTERED_SOURCE_NAME} needs both OPEN_REGISTERED_DATA and "
    "a separate read-only execution approval recorded in "
    "EXECUTION_APPROVAL_RECORD, and neither the Q5-E audit token nor the "
    "P1/P2 PREP token may be reused for it.  Not approved by any P3 "
    "approval: " + ", ".join(NOT_APPROVED) + ".")

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

    def __init__(self, status: str, message: str) -> None:
        if status not in HARNESS_STOPS:
            raise P3Error(f"{status!r} is not a registered harness stop; the "
                          f"harness does not invent verdicts")
        super().__init__(f"{status}: {message}")
        self.status = status
        self.detail = message


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
    """The stop a separately approved execution PR opens, by one field.

    It sits after the switch, the token and the fixture contract, and before
    dependencies, credentials, the Drive service and every read — so an
    unapproved call performs zero authentication attempts rather than a failed
    one.
    """
    if not EXECUTION_APPROVAL_RECORD.get("granted"):
        raise P3NotApprovedError(
            "P3 is implemented but not approved for execution: reading and "
            f"executing the registered {REGISTERED_SOURCE_NAME} needs a "
            f"separate read-only execution approval.  {APPROVAL_NOTE}")
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

FIXTURES: Tuple[Dict[str, object], ...] = (
    {
        "name": "test_source_match_nearest_already_used_falls_through",
        "refutes": ("that a peak whose nearest annotation is already consumed "
                    "is dropped.  Peak 1012's nearest is 1001, taken by peak "
                    "1000; falling through keeps it against 1042, dropping "
                    "loses the row entirely"),
        "peaks": (1000, 1012),
        "annotations": ((1001, "N"), (1042, "V")),
        "signal_length": 3000,
    },
    {
        "name": "test_source_match_distance_tie_goes_to_the_earlier_annotation",
        "refutes": ("that an exact distance tie goes to the later annotation.  "
                    "Peak 1030 is 30 samples from both 1000 and 1060, and the "
                    "two carry different AAMI classes, so the tie rule is "
                    "visible in the kept row and not only in an index"),
        "peaks": (1030,),
        "annotations": ((1000, "N"), (1060, "V")),
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
        "peaks": (1000, 1044),
        "annotations": ((1001, "+"), (1042, "N")),
        "signal_length": 3000,
    },
    {
        "name": "test_source_match_boundary_cut_consumes_its_match",
        "refutes": ("that a peak cut by the p-150 boundary releases its "
                    "annotation.  Peak 140 matches 141 and is cut; peak 190 is "
                    "49 samples from 141 and is not cut, so releasing gives it "
                    "that row and consuming leaves it unmatched"),
        "peaks": (140, 190),
        "annotations": ((141, "N"), (251, "V")),
        "signal_length": 3000,
    },
    {
        "name": "test_source_match_annotation_order_differing_from_sample_order",
        "refutes": ("that annotations are traversed in the order the reader "
                    "returned them.  Listed as [1060, 1000] with peak 1030 "
                    "equidistant, list order takes 1060 and sample order takes "
                    "1000 — different AAMI classes, so the kept row shows it"),
        "peaks": (1030,),
        "annotations": ((1060, "V"), (1000, "N")),
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
        "peaks": (1035, 1001),
        "annotations": ((1000, "N"), (1060, "V")),
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


def build_injection(fixture: Mapping[str, object],
                    log: Optional[StubCallLog] = None
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
        given = _peak_argument(args)
        log.record("pwave.pwave_features", given=list(given), n_args=len(args),
                   kwargs=sorted(kwargs))
        rows = [[float(p)] + [0.0] * 4 for p in given]
        numpy = _numpy()
        return (numpy.array(rows, dtype="float64") if numpy is not None
                else rows)

    return ({"rdrecord": rdrecord, "rdann": rdann, "rdsamp": rdsamp,
             "dl_database": dl_database, "detect_r": detect_r,
             "rr_features": rr_features, "pwave_features": pwave_features},
            log)


#: Module-global names a producer might hold its injected dependencies under.
#: Rebound after execution as well as before, so `import wfdb` and `from
#: .frontend import detect_r` are both covered.
INJECTED_GLOBALS: Tuple[str, ...] = (
    "detect_r", "rr_features", "pwave_features")
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

    def __enter__(self) -> "InjectedModules":
        wfdb = self._module("wfdb", {
            k: self.stubs[k]
            for k in ("rdrecord", "rdann", "rdsamp", "dl_database")})
        frontend = self._module("frontend", {
            "detect_r": self.stubs["detect_r"],
            "rr_features": self.stubs["rr_features"]})
        pwave = self._module("pwave",
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
    if list(inventory.get("problems") or ()) != []:
        problems.append(
            f"the inventory records unresolved problems: "
            f"{inventory.get('problems')!r}")
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

    __slots__ = ("permit", "fixture", "stubs", "log", "_injection", "_module")

    def __init__(self, permit: SourcePermit,
                 fixture: Mapping[str, object]) -> None:
        self.permit = permit
        self.fixture = fixture
        self.stubs: Dict[str, object] = {}
        self.log = StubCallLog()
        self._injection: Optional[InjectedModules] = None
        self._module: Optional[types.ModuleType] = None

    def __enter__(self) -> Tuple[Callable, StubCallLog]:
        self.stubs, self.log = build_injection(self.fixture)
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

    def open_producer(fixture: Mapping[str, object]) -> ProducerSession:
        return ProducerSession(permit, fixture)

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
    (("use_detected", "detected", "use_detect"), "use_detected"),
    (("split", "which"), "split"),
    (("win_before", "before"), "win_before"),
    (("win_after", "after"), "win_after"),
)
BINDING_VALUES: Dict[str, object] = {
    "record_name": "SYNTHETIC",
    "data_dir": "<synthetic>",
    "fs": FIXTURE_FS,
    "use_detected": True,
    "split": "DS1",
    "win_before": BJ.WIN_BEFORE,
    "win_after": BJ.WIN_AFTER,
}


def bind_source_arguments(function: Callable) -> Dict[str, object]:
    """Bind the producer's parameters from the declared plan, or stop.

    Nothing is invented: a parameter is bound when its name matches the plan or
    when it has a default of its own, and anything else raises
    `P3_SOURCE_SIGNATURE_UNBINDABLE` — a harness stop, never a verdict about
    the adapter.
    """
    import inspect                                           # noqa: PLC0415
    try:
        signature = inspect.signature(function)
    except (TypeError, ValueError) as error:                 # pragma: no cover
        raise SourceHarnessError(
            P3_SOURCE_SIGNATURE_UNBINDABLE,
            f"the signature of {getattr(function, '__name__', '?')} could not "
            f"be read: {error}") from error
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
            bound[name] = BINDING_VALUES[key]
            plan.append({"parameter": name, "bound_from": "plan",
                         "value": repr(BINDING_VALUES[key])})
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
            f"binding plan does not cover: {unbound}.  The plan is extended "
            f"deliberately and re-reviewed; a parameter is never filled with a "
            f"guess.")
    return {"kwargs": bound, "plan": plan,
            "parameters": list(signature.parameters)}


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
MAX_DEPTH = 3


def canonical_value(value: object, depth: int = 0) -> object:
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
        oversized = len(value) > MAX_CONTAINER                # type: ignore[arg-type]
    except TypeError:
        oversized = False
    if oversized:
        # Checked before any conversion: `tolist()` on a large array would
        # materialise the whole thing only to have it summarised anyway.
        return {"__type__": type(value).__name__, "__len__": len(value)}  # type: ignore[arg-type]
    tolist = getattr(value, "tolist", None)
    if callable(tolist) and not isinstance(value, (list, tuple, set, dict)):
        try:
            return canonical_value(tolist(), depth)
        except Exception:                                    # noqa: BLE001
            return {"__type__": type(value).__name__}
    if isinstance(value, Mapping):
        if len(value) > MAX_CONTAINER:                       # pragma: no cover
            return {"__type__": "mapping", "__len__": len(value)}
        try:
            items = sorted(value.items(), key=lambda kv: repr(kv[0]))
        except Exception:                                    # noqa: BLE001
            items = list(value.items())                      # pragma: no cover
        return {"__map__": [[canonical_value(k, depth + 1),
                             canonical_value(v, depth + 1)] for k, v in items]}
    if isinstance(value, (set, frozenset)):
        if len(value) > MAX_CONTAINER:                       # pragma: no cover
            return {"__type__": "set", "__len__": len(value)}
        try:
            members = sorted(value, key=repr)
        except Exception:                                    # noqa: BLE001
            members = list(value)                            # pragma: no cover
        return {"__set__": [canonical_value(m, depth + 1) for m in members]}
    if isinstance(value, (list, tuple)):
        if len(value) > MAX_CONTAINER:
            return {"__type__": type(value).__name__, "__len__": len(value)}
        return [canonical_value(m, depth + 1) for m in value]
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


def discover_kept_rows(returned: object, fixture: Mapping[str, object]
                       ) -> Dict[str, object]:
    """Read the kept rows out of whatever the producer returned.

    Three independent channels, and they must agree where more than one is
    present:

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
    peaks = [int(p) for p in fixture["peaks"]]
    peak_set = set(peaks)
    canonical = canonical_value(returned)
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
        return

    scan(canonical, "")
    if not channels:
        if rejected:
            raise SourceHarnessError(
                P3_KEPT_ROWS_UNOBSERVABLE,
                f"the producer returned row-like structures this projection "
                f"could not read: {rejected}.  The comparison was not made.")
        if not empty_lists:
            # Nothing that could hold rows came back at all.  "It kept
            # nothing" and "its output cannot be read" are different findings,
            # and only the second one is true here.
            raise SourceHarnessError(
                P3_KEPT_ROWS_UNOBSERVABLE,
                "the producer returned no row container at all: not an empty "
                "one, which would say it kept nothing, and not a readable one. "
                " The comparison was not made.")
        # Every row container that came back was empty: the producer kept no
        # rows, and that is an observation rather than a failure.
        return {"rows": [], "channels": ["empty_result"],
                "channel_sequences": {"empty_result": []},
                "empty_containers": sorted(empty_lists)}
    sequences = {name: [row["peak_sample"] for row in rows]
                 for name, rows in channels.items()}
    if len({tuple(v) for v in sequences.values()}) != 1:
        raise SourceHarnessError(
            P3_KEPT_ROWS_UNOBSERVABLE,
            f"the producer's own output channels disagree about which rows it "
            f"kept: {sequences}.  A comparison built on a channel chosen after "
            f"seeing the answers would be worthless.")
    rows = channels[sorted(channels)[0]]
    for name in sorted(channels):
        for index, row in enumerate(channels[name]):
            for token in row["tokens"]:
                if token not in rows[index]["tokens"]:
                    rows[index]["tokens"].append(token)
    for index, vector in enumerate(label_vectors(canonical, len(rows),
                                                 peak_set)):
        for position, row in enumerate(rows):
            row["tokens"].append([f"vector_{index}", vector[position]])
    return {"rows": rows, "channels": sorted(channels),
            "channel_sequences": {k: list(v) for k, v in sequences.items()}}


def label_vectors(canonical: object, n_rows: int, peak_set: Set[int]
                  ) -> List[List[str]]:
    """Flat per-row vectors a producer returned, as opaque tokens.

    What the values *mean* is never decoded.  They are tokens, compared only
    with other tokens from the same producer, which is all the projection needs
    in order to tell two annotations apart.  Every candidate vector is kept:
    one that turns out to be row-unique simply never matches anything and
    contributes nothing, while a class-like one generalises across fixtures.
    """
    found: List[List[str]] = []

    def scan(node: object) -> None:
        if isinstance(node, dict):
            if "__map__" in node:
                for _key, value in node["__map__"]:
                    scan(value)
                return
            for key, value in node.items():
                if not str(key).startswith("__"):
                    scan(value)
            return
        if isinstance(node, list) and n_rows and len(node) == n_rows:
            if all(isinstance(v, (int, float, str)) and not isinstance(v, bool)
                   for v in node):
                if all(isinstance(v, int) and v in peak_set for v in node):
                    return
                found.append([_canonical_json(v) for v in node])
            return

    scan(canonical)
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
                        side: str) -> Dict[str, object]:
    """One producer's decisions on one fixture, in the canonical schema.

    The same function runs over the registered source and over the candidate
    adapter.  It compares nothing; it says what each of them did, and stops
    when the trace does not say.
    """
    annotations = _annotation_table(fixture)
    peaks = _peak_table(fixture)
    name = str(fixture["name"])
    discovered = discover_kept_rows(returned, fixture)
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
            f"{side}/{name}: " + "; ".join(sorted(set(unresolved))))

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
                f"to {symbol!r}")

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
                   dictionary: LabelDictionary
                   ) -> Tuple[Dict[str, object], Dict[str, object]]:
    """Run the registered producer on one fixture and read what it did."""
    binding = bind_source_arguments(build_record)
    returned, trace = trace_call(build_record, build_record.__code__,
                                 binding["kwargs"])
    observation = project_observation(fixture, trace, returned, dictionary,
                                      side="source")
    return observation, {"binding": binding["plan"], **trace.as_dict()}


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
    observation = project_observation(fixture, trace, returned, dictionary,
                                      side="adapter")
    return observation, dict(trace.as_dict())


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
    results: List[Dict[str, object]] = []
    detail: List[Dict[str, object]] = []
    for name in fixture_names():
        fixture = FIXTURES_BY_NAME[name]
        # The producer is observed **inside** its session, so the stubs are
        # still installed while `build_record` runs.  A dependency imported in
        # the function body resolves to the injected module, not a real one.
        with open_source(fixture) as (build_record, call_log):
            source_observation, source_meta = observe_source(
                build_record, fixture, source_dictionary)
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
                       "equal": equal,
                       "source": source_observation,
                       "adapter": adapter_observation,
                       "source_meta": source_meta,
                       "adapter_meta": adapter_meta,
                       "injected_calls": call_log.as_list(),
                       "difference": (None if equal else describe_difference(
                           source_observation, adapter_observation))})
        emit(f"fixture {name}: equal={equal}")
    return {"gate": gate, "fixtures": results, "detail": detail,
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
    "discover_kept_rows", "label_vectors", "project_observation",
    "stage_decomposition", "observe_source", "observe_adapter",
    "differential_over_fixtures")


def oracle_harness_identity() -> Dict[str, object]:
    """What the harness *is*, as a digest over its own text and its fixtures."""
    import inspect                                           # noqa: PLC0415
    payload = {"functions": {name: inspect.getsource(globals()[name])
                             for name in ORACLE_HARNESS_FUNCTIONS},
               "fixtures": [fixture_card(n) for n in fixture_names()],
               "binding_plan": [[list(a), k] for a, k in BINDING_PLAN],
               "binding_values": {k: repr(v)
                                  for k, v in sorted(BINDING_VALUES.items())},
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
    if (inventory["parents"]
            and REGISTERED_SOURCE_FOLDER_ID not in inventory["parents"]):
        problems.append(f"the file's parents {inventory['parents']} do not "
                        f"include the registered folder id "
                        f"{REGISTERED_SOURCE_FOLDER_ID}")
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
    differential: Optional[Dict[str, object]] = None
    try:
        differential = differential_over_fixtures(
            source_factory(permit), adapter=adapter, emit=record)
    except SourceHarnessError as error:
        stop, detail = error.status, error.detail
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
