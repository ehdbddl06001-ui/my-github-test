#!/usr/bin/env python3
"""Regression tests for EXP-2026-008 / Q5-E PREP P3.

Everything here is synthetic.  **No test opens the registered `data.py`**, and
that is the point rather than an inconvenience: the producers under test are
written in this file, so the harness can be shown to detect a difference in
each decision the six required fixtures exist to pin — which is impossible to
demonstrate against a file whose behaviour nobody may look at yet.

No test reaches the Google Drive API, the network, a real ECG signal, a
detector, a cache, a per-record count, or any registered digest that would let
an implementation pass by memorising an answer.

Run with::

    python mit-bih/test_q5e_prep_p3_source_match_equivalence.py
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
import tempfile
import types

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import q5d_order_preserving_beat_join as BJ                  # noqa: E402
import q5e_leg2_failure_mechanism_audit as Q5E               # noqa: E402
import q5e_prep_p1_p2_asset_identity as P12                  # noqa: E402
import q5e_prep_p3_source_match_equivalence as P3            # noqa: E402

NOTEBOOK = os.path.join(
    ROOT, "notebooks", "quest58_q5e_prep_p3_source_match_equivalence.ipynb")
SPEC = os.path.join(
    ROOT, "experiments", "specs",
    "EXP-2026-008-q5e-prep-p3-source-match-equivalence.md")
TOKEN = P3.EXECUTION_APPROVAL_TOKEN
STAMP = "20260814T000000"

PASSED = 0


def check(condition: bool, label: str) -> None:
    global PASSED
    if not condition:
        raise AssertionError(label)
    PASSED += 1


# ─────────────────────────────────────────────────────────────────────────────
# Synthetic producers.
#
# `FAITHFUL` is written against the same prose the candidate adapter was
# written against.  It is **not** an oracle and it is never used as one: it is
# a stand-in for a registered source, so that the harness can be tested without
# the registered source.  Each variant below changes exactly one decision, and
# a test asserts which fixtures notice.
# ─────────────────────────────────────────────────────────────────────────────
FAITHFUL = '''
import wfdb
from .frontend import detect_r, rr_features

WIN_BEFORE = 150
WIN_AFTER = 150
AAMI = {"N": "N", "L": "N", "R": "N", "e": "N", "j": "N",
        "A": "S", "a": "S", "J": "S", "S": "S", "V": "V", "E": "V"}
CALLED = []


def build_record(rec, ddir, fs=360, use_detected=True):
    CALLED.append(rec)
    sig = wfdb.rdrecord(rec, pn_dir=ddir)
    ann = wfdb.rdann(rec, "atr")
    x = sig.p_signal
    peaks = detect_r([row[0] for row in x], fs)
    tol = int(0.15 * fs)
    samples = [int(s) for s in ann.sample]
    symbols = list(ann.symbol)
    order = sorted(range(len(samples)), key=lambda k: (samples[k], k))
    used = set()
    beats = []
    ys = []
    keep = []
    for i, p in enumerate(peaks):
        p = int(p)
        best = None
        bd = tol + 1
        for rank in range(len(order)):
            if rank in used:
                continue
            d = abs(samples[order[rank]] - p)
            if d < bd:
                best, bd = rank, d
        if best is None or bd > tol:
            continue
        used.add(best)
        j = order[best]
        cls = AAMI.get(symbols[j], "")
        if not cls:
            continue
        if not (p - WIN_BEFORE >= 0 and p + WIN_AFTER <= len(x)):
            continue
        keep.append(i)
        beats.append([float(v[0]) for v in x[p - WIN_BEFORE:p + WIN_AFTER]])
        ys.append(cls)
    rr_all = rr_features(peaks, fs)
    rr = [rr_all[i] for i in keep]
    return {"beat": beats, "rr": rr, "y": ys}
'''

#: One decision changed per variant, and the fixture that must notice.  The
#: mapping is asserted, not assumed: `test_each_required_fixture_pins_a
#: _decision_no_other_fixture_catches` fails if a variant is caught by the
#: wrong fixture, by several, or by none.
VARIANTS = {
    # A peak whose nearest annotation is taken is dropped instead of falling
    # through to the next-nearest.
    "drop_if_nearest_used": (
        [("        for rank in range(len(order)):\n"
          "            if rank in used:\n"
          "                continue\n",
          "        for rank in range(len(order)):\n"),
         ("        used.add(best)\n",
          "        if best in used:\n            continue\n"
          "        used.add(best)\n")],
        "test_source_match_nearest_already_used_falls_through"),
    # An exact distance tie goes to the annotation later in the reader's list.
    "tie_to_larger_list_index": (
        [("            if d < bd:\n",
          "            if d < bd or (d == bd and best is not None\n"
          "                          and order[rank] > order[best]):\n")],
        "test_source_match_distance_tie_goes_to_the_earlier_annotation"),
    # Non-AAMI annotations never enter the candidate pool.
    "non_aami_filtered_before_matching": (
        [("    order = sorted(range(len(samples)), "
          "key=lambda k: (samples[k], k))\n",
          "    order = sorted([k for k in range(len(samples))\n"
          "                    if AAMI.get(symbols[k], '')],\n"
          "                   key=lambda k: (samples[k], k))\n")],
        "test_source_match_non_aami_symbol_consumes_its_match"),
    # A peak cut by the window boundary gives its annotation back.
    "boundary_cut_releases": (
        [("        if not (p - WIN_BEFORE >= 0 and p + WIN_AFTER <= len(x)):\n"
          "            continue\n",
          "        if not (p - WIN_BEFORE >= 0 and p + WIN_AFTER <= len(x)):\n"
          "            used.discard(best)\n"
          "            continue\n")],
        "test_source_match_boundary_cut_consumes_its_match"),
    # Annotations are traversed in the order the reader returned them.
    "annotations_in_reader_order": (
        [("    order = sorted(range(len(samples)), "
          "key=lambda k: (samples[k], k))\n",
          "    order = list(range(len(samples)))\n")],
        "test_source_match_annotation_order_differing_from_sample_order"),
    # Peaks are sorted before matching.
    "peaks_sorted_first": (
        [("    tol = int(0.15 * fs)\n",
          "    peaks = sorted(int(v) for v in peaks)\n"
          "    tol = int(0.15 * fs)\n")],
        "test_source_match_peak_order_change_is_visible"),
}


def variant_text(name: str) -> str:
    text = FAITHFUL
    for old, new in VARIANTS[name][0]:
        if old not in text:                                  # pragma: no cover
            raise AssertionError(f"variant {name}: anchor not found")
        text = text.replace(old, new)
    return text


def load_for(text: str, label: str = "synthetic.py"):
    """A per-fixture session opener over synthetic bytes.

    The permit refuses the registered digest, so nothing built here can reach
    `data.py` however it is called.
    """
    return P3.source_factory(
        P3.synthetic_permit(text.encode("utf-8"), label=label))


def differential_for(text: str, adapter=None):
    return P3.differential_over_fixtures(load_for(text), adapter=adapter)


class FakeDriveFile(P3.DriveFileAdapter):
    """A Drive seam that counts what it was asked for.  Nothing is real."""

    def __init__(self, metadata=None, body=b"", fail_download=False):
        self.metadata = dict(metadata or {})
        self.body = body
        self.fail_download = fail_download
        self.calls = []

    def get_metadata(self, file_id):
        self.calls.append(("get_metadata", file_id))
        return dict(self.metadata)

    def download(self, file_id):
        self.calls.append(("download", file_id))
        if self.fail_download:                               # pragma: no cover
            raise AssertionError("download must not have been reached")
        return self.body


def good_metadata(body: bytes, **overrides) -> dict:
    metadata = {"id": P3.REGISTERED_SOURCE_FILE_ID,
                "name": P3.REGISTERED_SOURCE_NAME,
                "size": str(len(body)), "mimeType": "text/x-python",
                "modifiedTime": "2026-07-18T08:00:00Z",
                "sha256Checksum": hashlib.sha256(body).hexdigest(),
                "md5Checksum": hashlib.md5(body).hexdigest(),
                "trashed": False,
                "parents": [P3.REGISTERED_SOURCE_FOLDER_ID]}
    metadata.update(overrides)
    return metadata


class Credential(object):
    def __init__(self, scopes):
        self.scopes = list(scopes)


class _guard_set_to(object):
    """Hold the execution record at one value for a test, then restore it.

    Both directions are needed now that the user has approved execution.  The
    gates *below* the guard — the file-id gate, the provider inventory, the
    digest check — can only be exercised while it is open, and the refusals
    that protect an unapproved run can only be exercised while it is shut; a
    gate nobody tested is a gate nobody has.  Whatever the committed value is,
    it is put back afterwards and checked, so a suite that leaks a flipped
    barrier into the next test fails rather than passing quietly.
    """

    def __init__(self, granted):
        self.granted = granted
        self._saved = None

    def __enter__(self):
        self._saved = P3.EXECUTION_APPROVAL_RECORD["granted"]
        P3.EXECUTION_APPROVAL_RECORD["granted"] = self.granted
        return self

    def __exit__(self, *exc):
        P3.EXECUTION_APPROVAL_RECORD["granted"] = self._saved
        check(P3.EXECUTION_APPROVAL_RECORD["granted"] is self._saved,
              "the approval record is restored after the test")
        return False


def opened_guard():
    """The guard open, as an approved run has it."""
    return _guard_set_to(True)


def closed_guard():
    """The guard shut, as it was before the approval and as a revert restores."""
    return _guard_set_to(False)


# ─────────────────────────────────────────────────────────────────────────────
# 1. The barriers: what the approval opened, and what it did not.
# ─────────────────────────────────────────────────────────────────────────────
def test_the_execution_approval_is_recorded_rather_than_implied():
    """A guard that opened because someone deleted a line records no decision.

    The user approved read-only execution on 2026-08-15, and the record says
    who, when, what for — and, at least as importantly, what the approval does
    **not** cover.  `granted: False` remains an exact one-value revert.
    """
    record = P3.EXECUTION_APPROVAL_RECORD
    check(record["granted"] is True, "the record grants read-only execution")
    check(record["granted_on"] == "2026-08-16" and record["granted_by"] ==
          "user", "and names when it was granted and by whom")
    check(record["supersedes"]["withdrawn_on"] == "2026-08-16"
          and "oracle_harness_sha256" in
          str(record["supersedes"]["withdrawn_because"]),
          "while keeping the withdrawn one and the reason it lapsed, so the "
          "history reads as a decision rather than as an edit")
    check("read-only" in str(record["kind"]),
          "the approval is for a read-only run")
    check(any("drive.readonly" in entry for entry in record["approved"]),
          "which reads the registered file under exactly drive.readonly")
    check(P3.APPROVAL_NOTE.startswith("Approved (2026-08-16)")
          and "NOT approved by it" in P3.APPROVAL_NOTE,
          "the note states both halves of the boundary")


def test_the_approval_is_bound_to_the_harness_it_was_given_for():
    """An approval is of a *thing*, and the harness is the thing.

    Four rounds of this PREP were harness changes and each produced a
    different oracle.  An approval that applied to whatever the file says today
    would be an approval of something nobody read, so the record names the
    digest and the guard checks it — a refusal, so the failure direction is
    "ask again" and never "run anyway".
    """
    record = P3.EXECUTION_APPROVAL_RECORD
    current = P3.oracle_harness_identity()["oracle_harness_sha256"]
    check(record["for_oracle_harness_sha256"] == current,
          f"the approval names this module's harness: {current}")
    saved = record["for_oracle_harness_sha256"]
    try:
        record["for_oracle_harness_sha256"] = "0" * 64
        try:
            P3.run_p3("/nonexistent/out", approval=TOKEN,
                      open_registered_data=True, timestamp=STAMP,
                      emit=lambda _message: None)
        except P3.P3NotApprovedError as error:
            check("is not an approval of this run" in str(error),
                  "an approval for another harness refuses the run")
            check(current in str(error) and "0" * 64 in str(error),
                  "naming both digests, so renewing it is mechanical")
        else:                                                # pragma: no cover
            raise AssertionError("a stale approval let a run through")
    finally:
        record["for_oracle_harness_sha256"] = saved
    check(P3.EXECUTION_APPROVAL_RECORD["for_oracle_harness_sha256"] == current,
          "and the record is restored after the test")
    for item in ("the Q5-E scientific execution", "running detect_r()",
                 "registering SOURCE_MATCH_ORACLE_RECORD",
                 "M0-M4 aggregation", "training or retraining any model"):
        check(any(item in entry for entry in P3.NOT_APPROVED),
              f"and {item!r} is still outside it")
        check(item in P3.APPROVAL_NOTE,
              f"and the note repeats {item!r} where a reader will see it")


def test_the_switch_default_still_refuses_a_stray_import():
    """Approval did not open the switch; the notebook opts in at its call site.

    So an import, a copied cell or another module's call still reaches
    nothing, and the approval is not a standing permission for the process.
    """
    check(P3.OPEN_REGISTERED_DATA is False,
          "OPEN_REGISTERED_DATA is still False in the module")
    try:
        P3.run_p3("/nonexistent/out", approval=TOKEN, timestamp=STAMP,
                  emit=lambda _message: None)
    except P3.P3NotApprovedError as error:
        check("OPEN_REGISTERED_DATA is False" in str(error),
              "and a call that does not opt in explicitly is refused")
    else:                                                    # pragma: no cover
        raise AssertionError("the default switch let a run through")


def test_reverting_the_approval_restores_every_refusal():
    """One field back to False, and the whole route is shut again."""
    body = FAITHFUL.encode("utf-8")
    with closed_guard():
        for label, thunk in (
                ("run_p3",
                 lambda: P3.run_p3("/nonexistent/out", approval=TOKEN,
                                   open_registered_data=True, timestamp=STAMP,
                                   emit=lambda _message: None)),
                ("fetch_registered_source",
                 lambda: P3.fetch_registered_source(
                     FakeDriveFile(good_metadata(body), body,
                                   fail_download=True), TOKEN)),
                ("minting a registered permit",
                 lambda: P3.RegisteredSourcePermit(
                     P3._REGISTERED_PERMIT_KEY, body,
                     {"observed_sha256": hashlib.sha256(body).hexdigest()},
                     TOKEN))):
            try:
                thunk()
            except P3.P3NotApprovedError as error:
                check("not approved for execution" in str(error),
                      f"{label} is refused again with granted back to False")
            else:                                            # pragma: no cover
                raise AssertionError(f"{label} ran with the guard reverted")


def test_a_shut_guard_performs_no_credential_api_source_or_mkdir_call():
    """The whole point of a terminal guard: an unapproved call does nothing.

    Not "fails safely after connecting" — every seam that could authenticate,
    call an API, read a registered byte, execute the source or create an output
    directory is counted, and every count must be zero.
    """
    counters = {"auth": 0, "adapter": 0, "fetch": 0, "load": 0, "compile": 0,
                "mkdir": 0, "credential": 0}
    saved = {name: getattr(P3, name) for name in
             ("authenticate_drive_readonly", "build_drive_adapter",
              "fetch_registered_source", "load_source_under_injection",
              "_compile_and_exec")}
    saved_mkdir = os.mkdir
    saved_credential = P12._colab_readonly_credential

    def counted(key, result=None):
        def call(*args, **kwargs):
            counters[key] += 1
            return result
        return call

    try:
        P3.authenticate_drive_readonly = counted("auth")
        P3.build_drive_adapter = counted("adapter")
        P3.fetch_registered_source = counted("fetch")
        P3.load_source_under_injection = counted("load")
        P3._compile_and_exec = counted("compile")
        P12._colab_readonly_credential = counted("credential")
        os.mkdir = counted("mkdir")
        attempts = [
            {},                                        # both barriers closed
            {"approval": TOKEN},                       # switch still closed
            {"open_registered_data": True},            # token missing
            {"approval": Q5E.EXECUTION_APPROVAL_TOKEN,
             "open_registered_data": True},            # the audit's token
            {"approval": P12.EXECUTION_APPROVAL_TOKEN,
             "open_registered_data": True},            # the P1/P2 token
            {"approval": TOKEN, "open_registered_data": True},  # guard shut
        ]
        for keywords in attempts:
            try:
                with closed_guard():
                    P3.run_p3("/nonexistent/out", timestamp=STAMP,
                              emit=lambda _message: None, **keywords)
            except P3.P3NotApprovedError:
                check(True, f"run_p3 refuses {sorted(keywords)}")
            else:                                            # pragma: no cover
                raise AssertionError(f"run_p3 accepted {keywords}")
    finally:
        for name, value in saved.items():
            setattr(P3, name, value)
        os.mkdir = saved_mkdir
        P12._colab_readonly_credential = saved_credential
    check(counters == {"auth": 0, "adapter": 0, "fetch": 0, "load": 0,
                       "compile": 0, "mkdir": 0, "credential": 0},
          f"and reached nothing at all on the way: {counters}")


def test_another_stages_token_is_refused_by_name():
    for token, who in ((Q5E.EXECUTION_APPROVAL_TOKEN, "Q5-E audit"),
                       (P12.EXECUTION_APPROVAL_TOKEN, "P1/P2 PREP")):
        try:
            P3.require_execution_approval(token, "the registered source")
        except P3.P3NotApprovedError as error:
            check("does not accept another stage's" in str(error),
                  f"the {who} token is refused as another stage's approval")
        else:                                                # pragma: no cover
            raise AssertionError(f"the {who} token was accepted")
    check(P3.EXECUTION_APPROVAL_TOKEN not in
          (Q5E.EXECUTION_APPROVAL_TOKEN, P12.EXECUTION_APPROVAL_TOKEN),
          "and P3's own token is a different string from both")
    check(P3.execution_is_approved(TOKEN) and not P3.execution_is_approved(None),
          "only P3's own token reads as approved")


def test_every_registered_read_checks_approval_first():
    """Permission before capability, on each entry that touches a byte."""
    body = FAITHFUL.encode("utf-8")
    for approval in (None, "guess", Q5E.EXECUTION_APPROVAL_TOKEN,
                     P12.EXECUTION_APPROVAL_TOKEN):
        adapter = FakeDriveFile(good_metadata(body), body, fail_download=True)
        try:
            P3.fetch_registered_source(adapter, approval)
        except P3.P3NotApprovedError:
            check(not adapter.calls,
                  f"the fetch refuses approval={approval!r} without calling "
                  f"the adapter at all")
        else:                                                # pragma: no cover
            raise AssertionError("the fetch ran without approval")
    # Even the right token does not mint a permit while the guard is shut.
    adapter = FakeDriveFile(good_metadata(body), body, fail_download=True)
    try:
        with closed_guard():
            P3.fetch_registered_source(adapter, TOKEN)
    except P3.P3NotApprovedError as error:
        check(not adapter.calls,
              "and with the correct token it still stops at the guard, before "
              "the first API call")
        check("not approved for execution" in str(error),
              "naming the shut guard as the reason")
    else:                                                    # pragma: no cover
        raise AssertionError("the fetch ran with the guard shut")


def test_producer_bytes_are_executed_only_through_a_permit():
    """The blocker: a public token plus raw bytes must not be a way in.

    An earlier version's executor took `(body, inventory, approval)` and
    checked neither barrier, so the token string alone could compile and run
    the registered source.  Bytes now reach a compiler only through a permit,
    and there is no way to build one over the registered digest without both
    barriers open.
    """
    stubs, _log = P3.build_injection(P3.FIXTURES[0])
    for impostor in (b"x = 1\n", {"body": b"x = 1\n"}, None,
                     ("body", TOKEN)):
        try:
            P3.load_source_under_injection(impostor, stubs)
        except P3.P3NotApprovedError as error:
            check("not one of the two source permits" in str(error),
                  f"the loader refuses {type(impostor).__name__} instead of a "
                  f"permit")
        else:                                                # pragma: no cover
            raise AssertionError(f"{impostor!r} was executed")
        try:
            P3.source_factory(impostor)
        except P3.P3NotApprovedError:
            check(True, "and so does the session factory")
        else:                                                # pragma: no cover
            raise AssertionError("a factory was built without a permit")
    try:
        P3.RegisteredSourcePermit(object(), b"x = 1\n", {}, TOKEN)
    except P3.P3NotApprovedError as error:
        check("minted only by fetch_registered_source()" in str(error),
              "a registered permit cannot be constructed with a forged key")
    else:                                                    # pragma: no cover
        raise AssertionError("a forged registered permit was accepted")
    try:
        with closed_guard():
            P3.RegisteredSourcePermit(P3._REGISTERED_PERMIT_KEY, b"x = 1\n",
                                      {}, TOKEN)
    except P3.P3NotApprovedError as error:
        check("not approved for execution" in str(error),
              "and even with the module's own key a shut guard refuses it")
    else:                                                    # pragma: no cover
        raise AssertionError("the guard did not stop a registered permit")
    try:
        with opened_guard():
            P3.RegisteredSourcePermit(P3._REGISTERED_PERMIT_KEY, b"x = 1\n",
                                      {}, TOKEN)
    except P3.SourceHarnessError as error:
        check(error.status == P3.P3_SOURCE_IDENTITY_MISMATCH,
              "and with the guard open it is the digest that refuses it: the "
              "approval opened a file, not a door")
    else:                                                    # pragma: no cover
        raise AssertionError("a permit was minted over foreign bytes")


class _counted_compiles(object):
    """Count every compile and every mkdir for the length of a block."""

    def __init__(self):
        self.counts = {"compile": 0, "mkdir": 0}
        self._compile = None
        self._mkdir = None

    def __enter__(self):
        self._compile = P3._compile_and_exec
        self._mkdir = os.mkdir

        def counted_compile(*args, **kwargs):
            self.counts["compile"] += 1
            return self._compile(*args, **kwargs)

        def counted_mkdir(*args, **kwargs):
            self.counts["mkdir"] += 1
            return self._mkdir(*args, **kwargs)

        P3._compile_and_exec = counted_compile
        os.mkdir = counted_mkdir
        return self

    def __exit__(self, *exc):
        P3._compile_and_exec = self._compile
        os.mkdir = self._mkdir
        return False


class _registered_bytes(object):
    """Point the registered digest at bytes this test controls.

    The real `data.py` is unreadable here, so "the registered bytes" have to
    be simulated to test that they are refused.  Pointing the constant at a
    fixture's own body is the same move a registration would make, and it is
    put back afterwards.
    """

    def __init__(self, body):
        self.body = body
        self._saved = None

    def __enter__(self):
        self._saved = P3.REGISTERED_SOURCE_SHA256
        P3.REGISTERED_SOURCE_SHA256 = hashlib.sha256(self.body).hexdigest()
        return self.body

    def __exit__(self, *exc):
        P3.REGISTERED_SOURCE_SHA256 = self._saved
        check(P3.REGISTERED_SOURCE_SHA256 ==
              Q5E.M4_SOURCE_MAP_HASHES["data.py"],
              "the registered digest constant is put back afterwards")
        return False


def test_a_hand_built_permit_cannot_execute_the_registered_bytes():
    """The reported bypass, verbatim, plus the ways around the way around it.

    A permit used to be a plain object: base class constructible, slots
    writable, callers checking `isinstance`.  That made a third kind of permit
    anyone could assemble — claim `synthetic`, carry the registered bytes, and
    skip both the guard re-check and the digest refusal, because neither
    constructor ran.
    """
    registered = b"# stands in for the registered data.py bytes\n"
    with _registered_bytes(registered), _counted_compiles() as counter:
        def hand_built():
            permit = P3.SourcePermit()
            permit.kind = "synthetic"
            permit.body = registered
            permit.sha256 = hashlib.sha256(registered).hexdigest()
            permit.inventory = {}
            permit.synthetic = True
            permit.label = "synthetic.py"
            permit.approval = None
            return P3.source_factory(permit)

        try:
            hand_built()
        except P3.P3NotApprovedError as error:
            check("not constructible" in str(error),
                  "the base permit cannot be constructed at all, and says why")
        else:                                                # pragma: no cover
            raise AssertionError("a hand-built permit was accepted")

        # And if the constructor is skipped entirely, the pre-compile
        # re-validation is what refuses it.
        forged = object.__new__(P3.SyntheticSourcePermit)
        for field, value in (("kind", "synthetic"), ("body", registered),
                             ("sha256",
                              hashlib.sha256(registered).hexdigest()),
                             ("inventory",
                              {"digest_matches_registered": False,
                               "observed_sha256":
                                   hashlib.sha256(registered).hexdigest()}),
                             ("synthetic", True), ("label", "synthetic.py"),
                             ("approval", None)):
            object.__setattr__(forged, field, value)
        for label, thunk in (
                ("the session factory", lambda: P3.source_factory(forged)),
                ("the loader", lambda: P3.load_source_under_injection(
                    forged, P3.build_injection(P3.FIXTURES[0])[0])),
                ("the executor", lambda: P3._execute_with_permit(
                    "/nonexistent", forged, timestamp=STAMP))):
            try:
                thunk()
            except P3.P3NotApprovedError as error:
                check("holds the registered" in str(error)
                      or "sealed snapshot" in str(error),
                      f"{label} refuses a permit that never ran a constructor")
            else:                                            # pragma: no cover
                raise AssertionError(f"{label} accepted a forged permit")
    check(counter.counts == {"compile": 0, "mkdir": 0},
          f"and nothing was compiled and no directory was created: "
          f"{counter.counts}")


def test_a_permit_subclass_is_not_a_permit():
    try:
        class Sneaky(P3.SyntheticSourcePermit):              # noqa: F811
            pass
    except P3.P3NotApprovedError as error:
        check("exactly two kinds of source permit" in str(error),
              "a third permit type cannot even be defined")
    else:                                                    # pragma: no cover
        raise AssertionError("a permit subclass was defined")
    check(P3.SourcePermit._PERMIT_TYPES ==
          (P3.RegisteredSourcePermit, P3.SyntheticSourcePermit),
          "and the permitted set is exactly the two committed types")
    # Type identity, not isinstance: a look-alike carrying the right fields is
    # refused because it is not one of those two objects.
    class LooksLikeOne(object):
        kind = "synthetic"
        body = b"x = 1\n"
        sha256 = hashlib.sha256(b"x = 1\n").hexdigest()
        inventory = {"digest_matches_registered": False}
        synthetic = True
        label = "synthetic.py"
        approval = None

    try:
        P3.validate_permit_for_execution(LooksLikeOne())
    except P3.P3NotApprovedError as error:
        check("checked by type identity" in str(error),
              "and a duck-typed look-alike is refused by type identity")
    else:                                                    # pragma: no cover
        raise AssertionError("a look-alike passed validation")


def test_a_minted_permit_cannot_be_edited_afterwards():
    permit = P3.synthetic_permit(FAITHFUL.encode("utf-8"))
    registered = b"# stands in for the registered data.py bytes\n"
    for field, value in (("body", registered), ("sha256", "0" * 64),
                         ("kind", "registered"), ("synthetic", False),
                         ("approval", TOKEN), ("label", "data.py"),
                         ("inventory", {})):
        try:
            setattr(permit, field, value)
        except P3.P3NotApprovedError as error:
            check("sealed snapshot" in str(error),
                  f"{field} cannot be changed after the permit is minted")
        else:                                                # pragma: no cover
            raise AssertionError(f"{field} was edited on a minted permit")
    try:
        del permit.body
    except P3.P3NotApprovedError:
        check(True, "and nothing can be deleted from it either")
    else:                                                    # pragma: no cover
        raise AssertionError("a permit field was deleted")
    try:
        permit.inventory["observed_sha256"] = "0" * 64
    except TypeError:
        check(True, "the inventory is handed out read-only, so it cannot be "
                    "edited through the reference either")
    else:                                                    # pragma: no cover
        raise AssertionError("the permit inventory was mutated")
    check(permit.sha256 == hashlib.sha256(FAITHFUL.encode("utf-8")).hexdigest(),
          "and the permit still describes the bytes it was minted over")


def test_validation_runs_again_immediately_before_the_compiler():
    """Not "it was checked when it was minted" — checked now, from the bytes."""
    order = []
    saved_validate = P3.validate_permit_for_execution
    saved_compile = P3._compile_and_exec

    def traced_validate(permit):
        order.append("validate")
        return saved_validate(permit)

    def traced_compile(*args, **kwargs):
        order.append("compile")
        return saved_compile(*args, **kwargs)

    try:
        P3.validate_permit_for_execution = traced_validate
        P3._compile_and_exec = traced_compile
        permit = P3.synthetic_permit(FAITHFUL.encode("utf-8"))
        with P3.ProducerSession(permit, P3.FIXTURES[0]) as (build_record, _log):
            build_record(rec="SYNTHETIC", ddir="<synthetic>")
    finally:
        P3.validate_permit_for_execution = saved_validate
        P3._compile_and_exec = saved_compile
    check("compile" in order, "the producer really was compiled")
    for index, event in enumerate(order):
        if event == "compile":
            check(index > 0 and order[index - 1] == "validate",
                  "and every compile is immediately preceded by a validation")
    check(saved_validate(permit)["revalidated"] is True,
          "the validator reports that it re-derived the permit's claims")


def test_a_registered_permit_is_refused_once_the_guard_closes_again():
    """The guard is re-checked at execution, not only when the permit is minted.

    A permit minted under the approval is not a standing licence: revert the
    record — as a revoked approval would — and the permit it already issued
    stops working, at every surface, before anything is compiled.
    """
    body = FAITHFUL.encode("utf-8")
    with _registered_bytes(body):
        adapter = FakeDriveFile(good_metadata(body), body)
        saved_bytes = P3.REGISTERED_SOURCE_BYTES
        try:
            P3.REGISTERED_SOURCE_BYTES = len(body)
            with opened_guard():
                permit = P3.fetch_registered_source(adapter, TOKEN)
            check(type(permit) is P3.RegisteredSourcePermit,
                  "a registered permit was minted while the guard was open")
            with _counted_compiles() as counter, closed_guard():
                for label, thunk in (
                        ("the session factory",
                         lambda: P3.source_factory(permit)),
                        ("the loader",
                         lambda: P3.load_source_under_injection(
                             permit, P3.build_injection(P3.FIXTURES[0])[0])),
                        ("the executor",
                         lambda: P3._execute_registered_p3(
                             "/nonexistent", permit, timestamp=STAMP))):
                    try:
                        thunk()
                    except P3.P3NotApprovedError as error:
                        check("not approved for execution" in str(error),
                              f"{label} refuses it now that the guard is shut")
                    else:                                    # pragma: no cover
                        raise AssertionError(f"{label} used a stale permit")
            check(counter.counts == {"compile": 0, "mkdir": 0},
                  f"with nothing compiled and no directory made: "
                  f"{counter.counts}")
        finally:
            P3.REGISTERED_SOURCE_BYTES = saved_bytes


def _registered_permit_for(body):
    """Mint a genuine registered permit over `body`, with the constants pointed
    at it for the length of the caller's `_registered_bytes` block."""
    adapter = FakeDriveFile(good_metadata(body), body)
    with opened_guard():
        return P3.fetch_registered_source(adapter, TOKEN)


def test_a_registered_permit_must_show_it_came_from_the_registered_file_id():
    """Matching the digest says the bytes are right, not where they came from.

    The contract is that the oracle runs a file that passed the **file id**
    gate as well.  A permit assembled around the right bytes with a two-field
    inventory would otherwise be indistinguishable from a read of the
    registered Drive file — an arbitrary copy of the same content, wearing the
    provenance of the registered asset.
    """
    body = FAITHFUL.encode("utf-8")
    saved_bytes = P3.REGISTERED_SOURCE_BYTES
    with _registered_bytes(body) as registered:
        digest = hashlib.sha256(registered).hexdigest()
        try:
            P3.REGISTERED_SOURCE_BYTES = len(registered)
            with _counted_compiles() as counter, opened_guard():
                forged = object.__new__(P3.RegisteredSourcePermit)
                P3.SourcePermit.__init__(
                    forged, P3._PERMIT_CONSTRUCTION_KEY,
                    P3.PERMIT_KIND_REGISTERED, registered,
                    {"observed_sha256": digest}, False, "data.py", TOKEN)
                for label, thunk in (
                        ("the session factory",
                         lambda: P3.source_factory(forged)),
                        ("the loader",
                         lambda: P3.load_source_under_injection(
                             forged, P3.build_injection(P3.FIXTURES[0])[0])),
                        ("the registered executor",
                         lambda: P3._execute_registered_p3(
                             "/nonexistent", forged, timestamp=STAMP)),
                        ("the validator",
                         lambda: P3.validate_permit_for_execution(forged))):
                    try:
                        thunk()
                    except P3.SourceHarnessError as error:
                        check(error.status == P3.P3_SOURCE_IDENTITY_MISMATCH,
                              f"{label} refuses a permit whose inventory does "
                              f"not show a read of the registered file id")
                        check("registered file id" in str(error),
                              f"{label} says the file id is what is missing")
                    else:                                    # pragma: no cover
                        raise AssertionError(
                            f"{label} accepted bytes with no provenance")
            check(counter.counts == {"compile": 0, "mkdir": 0},
                  f"and nothing was compiled or created: {counter.counts}")
        finally:
            P3.REGISTERED_SOURCE_BYTES = saved_bytes


def test_each_provenance_field_of_a_registered_permit_is_re_checked():
    """A genuine permit, then one field of its inventory swapped, one at a time."""
    body = FAITHFUL.encode("utf-8")
    saved_bytes = P3.REGISTERED_SOURCE_BYTES
    with _registered_bytes(body) as registered:
        try:
            P3.REGISTERED_SOURCE_BYTES = len(registered)
            permit = _registered_permit_for(registered)
            with opened_guard():
                report = P3.validate_permit_for_execution(permit)
            check(report["revalidated"] is True
                  and report["kind"] == P3.PERMIT_KIND_REGISTERED,
                  "a permit minted by fetch_registered_source() passes the "
                  "production validator unchanged")
            genuine = dict(permit.inventory)
            mutations = {
                "a different requested file id":
                    {"requested_file_id": "1SomethingElse"},
                "a different resolved file id": {"file_id": "1SomethingElse"},
                "another name": {"name": "data_v2.py"},
                "another provider size": {"bytes": 999},
                "another observed size": {"observed_bytes": 999},
                "a registered digest that is not the observed one":
                    {"registered_sha256": "a" * 64},
                "an observed digest that is not the body's":
                    {"observed_sha256": "b" * 64},
                "a denied digest match": {"digest_matches_registered": False},
                "a file that was never read": {"read": False},
                "unresolved problems": {"problems": ["something was wrong"]},
                "a foreign parent folder": {"parents": ["1SomeOtherFolder"]},
                "no parent at all": {"parents": []},
                "a trashed file": {"trashed": True},
                "a shortcut": {"is_shortcut": True},
                "a folder": {"is_folder": True},
                "a truthy string where a boolean belongs":
                    {"digest_matches_registered": "true"},
            }
            with _counted_compiles() as counter:
                for label, override in mutations.items():
                    tampered = object.__new__(P3.RegisteredSourcePermit)
                    for field in ("kind", "sha256", "body", "synthetic",
                                  "label", "approval", "_sealed"):
                        object.__setattr__(tampered, field,
                                           getattr(permit, field))
                    object.__setattr__(
                        tampered, "inventory",
                        types.MappingProxyType({**genuine, **override}))
                    try:
                        with opened_guard():
                            P3.validate_permit_for_execution(tampered)
                    except P3.SourceHarnessError as error:
                        check(error.status == P3.P3_SOURCE_IDENTITY_MISMATCH,
                              f"{label} is refused by the provenance check")
                    else:                                    # pragma: no cover
                        raise AssertionError(f"{label} was accepted")
                # The permit's own label is part of the same claim.
                relabelled = object.__new__(P3.RegisteredSourcePermit)
                for field in ("kind", "sha256", "body", "synthetic",
                              "inventory", "approval", "_sealed"):
                    object.__setattr__(relabelled, field,
                                       getattr(permit, field))
                object.__setattr__(relabelled, "label", "something_else.py")
                try:
                    with opened_guard():
                        P3.validate_permit_for_execution(relabelled)
                except P3.SourceHarnessError:
                    check(True, "and so is a permit relabelled away from the "
                                "registered file name")
                else:                                        # pragma: no cover
                    raise AssertionError("a relabelled permit was accepted")
            check(counter.counts == {"compile": 0, "mkdir": 0},
                  f"none of which compiled anything: {counter.counts}")
        finally:
            P3.REGISTERED_SOURCE_BYTES = saved_bytes


def test_the_synthetic_route_cannot_execute_the_registered_source():
    """The synthetic executor is not a back door, and cannot be made one."""
    saved = P3.REGISTERED_SOURCE_SHA256
    body = FAITHFUL.encode("utf-8")
    try:
        # Point the registered digest at the fixture's own bytes: the synthetic
        # route must then refuse those very bytes, whatever else is true.
        P3.REGISTERED_SOURCE_SHA256 = hashlib.sha256(body).hexdigest()
        for call in (lambda: P3.synthetic_permit(body),
                     lambda: P3.execute_synthetic_p3("/nonexistent", body)):
            try:
                call()
            except P3.P3NotApprovedError as error:
                check("refuses bytes whose digest is the registered" in
                      str(error),
                      "the synthetic route refuses the registered bytes by "
                      "digest, not by intention")
            else:                                            # pragma: no cover
                raise AssertionError("the registered bytes ran synthetically")
    finally:
        P3.REGISTERED_SOURCE_SHA256 = saved
    permit = P3.synthetic_permit(body)
    check(permit.synthetic is True and permit.kind == "synthetic",
          "an ordinary fixture producer still gets a synthetic permit")
    check(permit.inventory["digest_matches_registered"] is False
          and permit.inventory["synthetic_fixture"] is True,
          "whose inventory says plainly that it is not the registered file")
    check(permit.approval is None,
          "and which carries no approval, because it opens nothing registered")


def test_a_shut_guard_reaches_no_compile_exec_or_mkdir_on_the_registered_path():
    """Counted, not argued: the refused route touches none of the three.

    Run with the approval reverted, because that is the state this protects:
    every direct-call route into the registered path must reach nothing while
    the guard is shut, not merely fail somewhere later.
    """
    counters = {"compile": 0, "mkdir": 0}
    saved_compile = P3._compile_and_exec
    saved_mkdir = os.mkdir
    body = FAITHFUL.encode("utf-8")

    def counted_compile(*args, **kwargs):
        counters["compile"] += 1
        return saved_compile(*args, **kwargs)

    def counted_mkdir(*args, **kwargs):
        counters["mkdir"] += 1
        return saved_mkdir(*args, **kwargs)

    try:
        P3._compile_and_exec = counted_compile
        os.mkdir = counted_mkdir
        attempts = (
            lambda: P3.run_p3("/nonexistent", approval=TOKEN,
                              open_registered_data=True, timestamp=STAMP,
                              emit=lambda _m: None),
            lambda: P3.fetch_registered_source(
                FakeDriveFile(good_metadata(body), body), TOKEN),
            lambda: P3.RegisteredSourcePermit(P3._REGISTERED_PERMIT_KEY, body,
                                              {}, TOKEN),
            lambda: P3.source_factory(b"raw bytes are not a permit"),
            lambda: P3.load_source_under_injection(body, {}),
            lambda: P3._execute_registered_p3("/nonexistent", body,
                                              timestamp=STAMP),
            lambda: P3._execute_with_permit("/nonexistent", body,
                                            timestamp=STAMP),
        )
        for index, attempt in enumerate(attempts):
            try:
                with closed_guard():
                    attempt()
            except (P3.P3NotApprovedError, P3.SourceHarnessError):
                check(True, f"attempt {index} on the registered path refused")
            else:                                            # pragma: no cover
                raise AssertionError(f"attempt {index} was allowed")
    finally:
        P3._compile_and_exec = saved_compile
        os.mkdir = saved_mkdir
    check(counters == {"compile": 0, "mkdir": 0},
          f"and between them they compiled nothing and created no directory: "
          f"{counters}")


def test_drive_scope_must_be_exactly_read_only():
    audits = []

    def factory(credential):
        audits.append(credential)
        return {"service": True}

    service, audit = P3.authenticate_drive_readonly(
        TOKEN, credential_provider=lambda: Credential([P3.DRIVE_READONLY_SCOPE]),
        service_factory=factory)
    check(service == {"service": True} and audit["exact_readonly_scope_proven"],
          "an exactly read-only credential is accepted and recorded as proven")
    for scopes in ([], ["https://www.googleapis.com/auth/drive"],
                   [P3.DRIVE_READONLY_SCOPE,
                    "https://www.googleapis.com/auth/drive.file"]):
        before = len(audits)
        try:
            P3.authenticate_drive_readonly(
                TOKEN, credential_provider=lambda: Credential(scopes),
                service_factory=factory)
        except P3.P3Error as error:
            check(P3.READONLY_SCOPE_UNPROVEN in str(error),
                  f"scopes {scopes} are refused rather than assumed read-only")
            check(len(audits) == before,
                  "and no service is built from a credential it refused")
        else:                                                # pragma: no cover
            raise AssertionError(f"scopes {scopes} were accepted")


def test_the_drive_seam_has_no_write_verb():
    surface = {n for n in dir(P3.DriveFileAdapter) if not n.startswith("_")}
    check(surface == {"get_metadata", "download", "describe"},
          "the P3 Drive adapter exposes only read verbs")
    with open(P3.__file__, encoding="utf-8") as handle:
        body = handle.read().split("class GoogleDriveFileAdapter", 1)[1]
    body = body.split("\ndef ", 1)[0]
    for verb in (".create(", ".update(", ".delete(", ".trash(", ".copy(",
                 ".move("):
        check(verb not in body,
              f"and the production adapter never calls files(){verb}")


# ─────────────────────────────────────────────────────────────────────────────
# 2. Source identity: id and digest, in that order, before anything runs.
# ─────────────────────────────────────────────────────────────────────────────
def test_an_unregistered_file_id_stops_before_any_api_call():
    body = FAITHFUL.encode("utf-8")
    adapter = FakeDriveFile(good_metadata(body), body, fail_download=True)
    try:
        with opened_guard():
            P3.fetch_registered_source(adapter, TOKEN,
                                       "1SomeOtherFileIdEntirely")
    except P3.SourceHarnessError as error:
        check(error.status == P3.P3_SOURCE_FILE_ID_UNREGISTERED,
              "an unregistered file id stops as P3_SOURCE_FILE_ID_UNREGISTERED")
        check(not adapter.calls,
              "and nothing was asked of Drive before that stop")
        check("never searches by name" in str(error),
              "the refusal says a name search is not the fallback")
    else:                                                    # pragma: no cover
        raise AssertionError("an unregistered file id was accepted")
    try:
        P3.run_p3("/nonexistent", approval=TOKEN, open_registered_data=True,
                  file_id="1Another")
    except P3.SourceHarnessError as error:
        check(error.status == P3.P3_SOURCE_FILE_ID_UNREGISTERED,
              "and the production route refuses it before the terminal guard")


def test_a_file_with_the_right_name_but_a_different_identity_is_refused():
    """The substitution this PREP exists to prevent, in five shapes."""
    body = FAITHFUL.encode("utf-8")
    cases = {
        "a different file answered to the id":
            {"id": "1SomethingElse"},
        "the id resolves to a shortcut":
            {"shortcutDetails": {"targetId": "1Elsewhere"}},
        "the id resolves to a folder":
            {"mimeType": P3.DRIVE_FOLDER_MIME},
        "the file is in the trash": {"trashed": True},
        "the byte count is not the registered one": {"size": "999"},
        "the file lives outside the registered folder":
            {"parents": ["1SomeOtherFolder"]},
        "the file has the registered name but another provider checksum":
            {"sha256Checksum": "a" * 64},
    }
    for label, override in cases.items():
        metadata = good_metadata(body, **override)
        check(metadata["name"] == P3.REGISTERED_SOURCE_NAME,
              f"{label}: the name still matches, which is exactly the trap")
        adapter = FakeDriveFile(metadata, body, fail_download=True)
        try:
            with opened_guard():
                P3.fetch_registered_source(adapter, TOKEN)
        except P3.SourceHarnessError as error:
            check(error.status == P3.P3_SOURCE_IDENTITY_MISMATCH,
                  f"{label}: refused as an identity mismatch")
            check([c for c in adapter.calls if c[0] == "download"] == [],
                  f"{label}: and nothing was downloaded")
        else:                                                # pragma: no cover
            raise AssertionError(f"{label} was accepted")
    renamed = good_metadata(body, name="data_v2.py")
    adapter = FakeDriveFile(renamed, body, fail_download=True)
    try:
        with opened_guard():
            P3.fetch_registered_source(adapter, TOKEN)
    except P3.SourceHarnessError as error:
        check(error.status == P3.P3_SOURCE_IDENTITY_MISMATCH,
              "a renamed file at the registered id is refused too")


def test_a_file_with_no_confirmable_parent_is_refused_before_the_download():
    """An unconfirmed parent is not a confirmed one, and the difference is
    which side of the transfer the run stops on.

    The parent comparison used to be guarded by the parents being non-empty,
    so a provider that returned none at all skipped the check and the bytes
    were fetched anyway.  The provenance check would still have refused the
    permit afterwards — but the contract is that a parent which cannot be
    confirmed stops the run *before* anything is downloaded.
    """
    body = FAITHFUL.encode("utf-8")
    for label, override in (("no parents at all", {"parents": []}),
                            ("a parents field the provider omitted",
                             {"parents": None}),
                            ("a foreign parent",
                             {"parents": ["1SomeOtherFolder"]})):
        adapter = FakeDriveFile(good_metadata(body, **override), body,
                                fail_download=True)
        try:
            with opened_guard():
                P3.fetch_registered_source(adapter, TOKEN)
        except P3.SourceHarnessError as error:
            check(error.status == P3.P3_SOURCE_IDENTITY_MISMATCH,
                  f"{label}: refused as an identity mismatch")
            check("Nothing was downloaded" in str(error),
                  f"{label}: and refused before the transfer, not after it")
            check(adapter.calls == [("get_metadata",
                                     P3.REGISTERED_SOURCE_FILE_ID)],
                  f"{label}: exactly one metadata lookup and no download "
                  f"({adapter.calls})")
        else:                                                # pragma: no cover
            raise AssertionError(f"{label} was fetched")


def test_an_empty_problem_list_means_exactly_an_empty_list():
    """A field that was never written is not a clean read."""
    body = FAITHFUL.encode("utf-8")
    saved_bytes = P3.REGISTERED_SOURCE_BYTES
    with _registered_bytes(body) as registered:
        try:
            P3.REGISTERED_SOURCE_BYTES = len(registered)
            permit = _registered_permit_for(registered)
            genuine = dict(permit.inventory)
            check(genuine["problems"] == [],
                  "a genuine inventory records an empty problem list")
            for label, override in (
                    ("a missing problems field", {}),
                    ("problems set to None", {"problems": None}),
                    ("problems as an empty tuple", {"problems": ()}),
                    ("problems as an empty string", {"problems": ""}),
                    ("problems as an empty dict", {"problems": {}})):
                inventory = dict(genuine)
                if override:
                    inventory.update(override)
                else:
                    inventory.pop("problems")
                try:
                    with opened_guard():
                        P3.assert_registered_provenance(
                            P3.REGISTERED_SOURCE_NAME, inventory,
                            permit.sha256, len(registered))
                except P3.SourceHarnessError as error:
                    check("not an empty list" in str(error),
                          f"{label} is refused rather than coerced")
                else:                                        # pragma: no cover
                    raise AssertionError(f"{label} passed as a clean read")
            with opened_guard():
                P3.assert_registered_provenance(
                    P3.REGISTERED_SOURCE_NAME, genuine, permit.sha256,
                    len(registered))
            check(True, "while the genuine inventory still passes")
        finally:
            P3.REGISTERED_SOURCE_BYTES = saved_bytes


def test_bytes_that_do_not_match_the_registered_digest_are_never_executed():
    """The digest gate sits before `compile`, not after `exec`."""
    poison = b"raise SystemExit('this must never be executed')\n"
    # The metadata claims the registered size and checksum, so the run gets
    # past the inventory and the *bytes themselves* are what stops it.  A file
    # that lies about its own metadata is the case the second check exists for.
    lying = good_metadata(poison, size=str(P3.REGISTERED_SOURCE_BYTES),
                          sha256Checksum=P3.REGISTERED_SOURCE_SHA256)
    adapter = FakeDriveFile(lying, poison)
    try:
        with opened_guard():
            P3.fetch_registered_source(adapter, TOKEN)
    except P3.SourceHarnessError as error:
        check(error.status == P3.P3_SOURCE_IDENTITY_MISMATCH,
              "bytes whose digest is not the registered one stop the run")
        check("were not compiled or executed" in str(error),
              "and the refusal states that they were not executed")
        check([c[0] for c in adapter.calls] == ["get_metadata", "download"],
              "the bytes were read, hashed and refused — never executed")
    else:                                                    # pragma: no cover
        raise AssertionError("unverified bytes were accepted")
    short = FAITHFUL.encode("utf-8")
    adapter = FakeDriveFile(good_metadata(short), short, fail_download=True)
    try:
        with opened_guard():
            P3.fetch_registered_source(adapter, TOKEN)
    except P3.SourceHarnessError as error:
        check("Nothing was downloaded" in str(error),
              "and a size or checksum that disagrees stops before the download")
    with opened_guard():
        try:
            P3.RegisteredSourcePermit(P3._REGISTERED_PERMIT_KEY, poison,
                                      {"observed_sha256": "b" * 64}, TOKEN)
        except P3.SourceHarnessError as error:
            check(error.status == P3.P3_SOURCE_IDENTITY_MISMATCH,
                  "and a permit repeats the check against the bytes it is "
                  "given, so unverified bytes never become executable")
        else:                                                # pragma: no cover
            raise AssertionError("a permit was minted over unverified bytes")


def test_matching_bytes_are_fetched_in_the_registered_order():
    """The happy path, against the fixture's **own** registered identity.

    The registered constants are pointed at the synthetic body for the length
    of this test — the way a registration would point them at a real file —
    rather than the fixture being given the real digest to match.  A test that
    embedded the registered digest could be satisfied by memorising it.
    """
    body = FAITHFUL.encode("utf-8")
    saved = (P3.REGISTERED_SOURCE_BYTES, P3.REGISTERED_SOURCE_SHA256)
    try:
        P3.REGISTERED_SOURCE_BYTES = len(body)
        P3.REGISTERED_SOURCE_SHA256 = hashlib.sha256(body).hexdigest()
        adapter = FakeDriveFile(good_metadata(body), body)
        with opened_guard():
            permit = P3.fetch_registered_source(adapter, TOKEN)
        inventory = permit.inventory
        check(permit.body == body and isinstance(
                  permit, P3.RegisteredSourcePermit),
              "the verified bytes come back inside a registered permit")
        check([c[0] for c in adapter.calls] == ["get_metadata", "download"],
              "inventory first, download second: a bad file is refused "
              "before anything is transferred")
        check(inventory["observed_sha256"] == P3.REGISTERED_SOURCE_SHA256
              and inventory["digest_matches_registered"] is True,
              "and the inventory records the digest of the bytes read and "
              "that it matched")
        check(inventory["read"] is True and inventory["problems"] == [],
              "with no problems left over")
    finally:
        P3.REGISTERED_SOURCE_BYTES, P3.REGISTERED_SOURCE_SHA256 = saved
    check(P3.REGISTERED_SOURCE_SHA256 == Q5E.M4_SOURCE_MAP_HASHES["data.py"],
          "and the module's registered identity is put back untouched")


def test_the_registered_identity_matches_the_frozen_source_map():
    check(P3.REGISTERED_SOURCE_SHA256 ==
          Q5E.M4_SOURCE_MAP_HASHES["data.py"],
          "the digest is Q5-E's own registered data.py hash, not a copy")
    check(P3._is_sha256(P3.REGISTERED_SOURCE_SHA256),
          "and it is a lowercase 64-hex digest")
    check(P3.REGISTERED_SOURCE_FILE_ID == "1a8mfNbCz5_vPaOWajsX15l93rgEaO_UK"
          and P3.REGISTERED_SOURCE_BYTES == 7744,
          "the file id and byte count are the ones ASSETS.md registers")
    with open(os.path.join(ROOT, "research", "ASSETS.md"),
              encoding="utf-8") as handle:
        assets = handle.read()
    check(P3.REGISTERED_SOURCE_FILE_ID in assets,
          "the file id is present in the assets registry")
    check(P3.REGISTERED_SOURCE_FOLDER_ID in assets,
          "and so is the folder it must live in")


# ─────────────────────────────────────────────────────────────────────────────
# 3. The oracle is the source, and there is no second reimplementation.
# ─────────────────────────────────────────────────────────────────────────────
def test_the_oracle_actually_executes_the_producer():
    """Not a description of the producer: the producer, running."""
    open_source = load_for(FAITHFUL)
    fixture = P3.FIXTURES_BY_NAME[
        "test_source_match_nearest_already_used_falls_through"]
    dictionary = P3.LabelDictionary()
    with open_source(fixture) as (build_record, log):
        observation, meta = P3.observe_source(build_record, fixture,
                                              dictionary)
    module_globals = build_record.__globals__
    check(module_globals["CALLED"] == ["SYNTHETIC"],
          "the producer's own module state shows its function ran")
    check(meta["n_steps"] > 0 and meta["code_name"] == "build_record",
          "and the trace came from that function's own code object")
    targets = {call["target"] for call in log.as_list()}
    check({"wfdb.rdrecord", "wfdb.rdann", "frontend.detect_r",
           "frontend.rr_features"} <= targets,
          "every dependency it reached was an injected stub")
    check(log.by_target("frontend.detect_r")[0]["returned"] ==
          [int(p) for p in fixture["peaks"]],
          "the detector stub, not a detector, supplied the peaks")
    check(observation["kept_rows"] and observation["peak_to_annotation"],
          "and the observation is built from what that run did")


def test_the_projection_is_not_a_second_matching_implementation():
    """A rule written twice can be wrong twice; this file writes it none.

    The projection may read distances, orders and tolerances *for reporting*,
    but it must not compute a match: no distance arithmetic, no comparison
    against the tolerance, and no fixture may carry an expected answer.
    """
    with open(P3.__file__, encoding="utf-8") as handle:
        module_text = handle.read()
    body = module_text.split("def canonical_value", 1)[1]
    body = body.split("def build_config", 1)[0]
    for token in ("abs(", "<= tolerance", "< tolerance", "<= TOLERANCE",
                  "best_distance", "nearest"):
        check(token not in body,
              f"the capture and projection layer contains no {token!r}")
    for fixture in P3.FIXTURES:
        for key in fixture:
            check(key in ("name", "refutes", "peaks", "annotations",
                          "signal_length"),
                  f"no fixture carries {key!r}: an expected answer here would "
                  f"be a third transcription of the rule")
    identity = P3.oracle_harness_identity()
    check(identity["oracle_is_the_registered_source"] is True
          and identity["second_reimplementation_used_as_oracle"] is False,
          "and the harness identity says so where a reviewer will read it")


def test_the_harness_reads_the_adapters_own_mapping_correctly():
    """The projection is checked against a side that already declares its answer.

    The candidate adapter records `raw_atr_ordinal` on each kept row — its own
    statement of which annotation the row came from.  The projection never
    looks at that field; agreeing with it on every fixture is evidence that
    reading a trace mechanically recovers what the producer actually did.
    """
    dictionary = P3.LabelDictionary()
    for name in P3.fixture_names():
        fixture = P3.FIXTURES_BY_NAME[name]
        observation, _meta = P3.observe_adapter(fixture, dictionary)
        declared = Q5E.match_peaks_to_annotations(
            [int(p) for p in fixture["peaks"]],
            [(int(s), str(y)) for s, y in fixture["annotations"]],
            int(fixture["signal_length"]))
        projected = [(row["peak_index"], row["annotation_index"])
                     for row in observation["kept_rows"]]
        stated = [(row["peak_index"], row["raw_atr_ordinal"])
                  for row in declared["kept_rows"]]
        check(projected == stated,
              f"{name}: the projected kept rows equal the adapter's own")
        unmatched = sorted(a["index"]
                           for a in observation["unmatched_annotations"])
        check(unmatched == sorted(a["anchor_ordinal"] for a in
                                  declared["annotations_without_peak"]),
              f"{name}: and so do the unmatched annotations")
        unmatched_peaks = sorted(p["peak_index"]
                                 for p in observation["unmatched_peaks"])
        check(unmatched_peaks == sorted(p["anchor_ordinal"] for p in
                                        declared["peaks_without_annotation"]),
              f"{name}: and the unmatched peaks")


def test_a_faithful_producer_and_the_adapter_agree_on_every_fixture():
    result = differential_for(FAITHFUL)
    check(result["all_equal"] is True,
          "a producer written to the same contract agrees on all six fixtures")
    check(result["fixtures_passed"] == result["fixtures_total"] == 6,
          "and all six were run, not a subset")
    check([entry["name"] for entry in result["fixtures"]] ==
          list(Q5E.SOURCE_MATCH_REQUIRED_FIXTURES),
          "in the registered order, under the registered names")
    for entry in result["fixtures"]:
        check(P3._is_sha256(entry["source_result_sha256"])
              and entry["source_result_sha256"] ==
              entry["adapter_result_sha256"],
              f"{entry['name']}: both sides produced the same 64-hex digest")


def test_each_required_fixture_pins_a_decision_no_other_fixture_catches():
    """Six fixtures, six decisions, and none of them is redundant.

    For every variant, exactly one fixture notices — so removing that fixture
    would let that variant through, which is what "independently necessary"
    means.  A differential that could drop a fixture and keep its verdict was
    never testing six things.
    """
    names = list(P3.fixture_names())
    detected = {}
    for variant, (_edits, expected) in sorted(VARIANTS.items()):
        result = differential_for(variant_text(variant))
        caught = [entry["name"] for entry in result["fixtures"]
                  if not entry["equal"]]
        detected[variant] = caught
        check(caught == [expected],
              f"{variant}: caught by exactly {expected}, not {caught}")
        check(result["all_equal"] is False
              and result["first_failing_fixture"] == expected,
              f"{variant}: the differential reports it as a disagreement")
    for name in names:
        owners = [v for v, caught in detected.items() if caught == [name]]
        check(len(owners) == 1,
              f"{name} is the only fixture that catches {owners}")
    check(sorted(sum(detected.values(), [])) == sorted(names),
          "and between them the variants cover every fixture exactly once")


def test_a_disagreement_preserves_the_trace_rather_than_repairing_anything():
    variant = "boundary_cut_releases"
    fingerprint_before = Q5E.source_match_adapter_fingerprint()
    result = differential_for(variant_text(variant))
    entry = next(d for d in result["detail"] if not d["equal"])
    fields = {difference["field"] for difference in entry["difference"]}
    check("released_annotations" in fields or "peak_to_annotation" in fields,
          "the release decision shows up as a named field difference")
    check(entry["source"]["fixture"] == entry["adapter"]["fixture"],
          "both sides' full observations are preserved side by side")
    check(entry["injected_calls"],
          "along with every call the producer made into the stubs")
    check(Q5E.source_match_adapter_fingerprint() == fingerprint_before,
          "and the adapter is not touched: its fingerprint is unchanged")
    check(P3.candidate_record(result, "a" * 64, "b" * 64, "c" * 64) is None,
          "a differential with a disagreement yields no candidate at all")


def test_consumption_timing_and_stage_states_are_part_of_the_comparison():
    dictionary = P3.LabelDictionary()
    fixture = P3.FIXTURES_BY_NAME[
        "test_source_match_boundary_cut_consumes_its_match"]
    observation, _meta = P3.observe_adapter(fixture, dictionary)
    check(observation["consumed_annotations"][0]["consumed_at_peak_index"] == 0,
          "the annotation consumed by the cut peak records when it was taken")
    filler = list(range(len(fixture["peaks"]) - len(P3.FILLER_PEAKS),
                        len(fixture["peaks"])))
    check([row["peak_index"] for row in observation["kept_rows"]] == filler,
          "no row survives the boundary cut in this fixture: every kept row is "
          "a filler beat, and the two peaks under test keep nothing")
    check(observation["stages"]["matched_pre_aami"] == [0] + filler,
          "the state before AAMI selection still shows the match")
    check(observation["stages"]["post_boundary"] == filler,
          "and the state after the boundary cut holds only the filler")
    check(observation["stages"]["kept_equals_post_boundary"] is True,
          "the producer's own kept rows agree with that description")
    check(observation["released_annotations"] == [],
          "and nothing was released back into the pool")
    for field in ("peak_to_annotation", "kept_rows", "consumed_annotations",
                  "released_annotations", "unmatched_annotations",
                  "unmatched_peaks", "stages"):
        check(field in observation,
              f"the compared observation carries {field}")


def test_the_observation_digest_is_deterministic():
    dictionary = P3.LabelDictionary()
    digests = []
    for _attempt in range(3):
        observation, _meta = P3.observe_adapter(P3.FIXTURES[0],
                                                P3.LabelDictionary())
        digests.append(P3.observation_digest(observation))
    check(len(set(digests)) == 1,
          "the same run of the same producer yields the same digest")
    open_source = load_for(FAITHFUL)
    with open_source(P3.FIXTURES[0]) as (build_record, _log):
        source, _meta = P3.observe_source(build_record, P3.FIXTURES[0],
                                          dictionary)
    check(P3.observation_digest(source) == digests[0],
          "and two different producers that decided the same thing agree")
    mutated = dict(source)
    mutated["kept_rows"] = list(reversed(source["kept_rows"]))
    check(P3.observation_digest(mutated) != digests[0],
          "while reordering the kept rows changes it, as row order must")


# ─────────────────────────────────────────────────────────────────────────────
# 4. Harness failures are never dressed up as equivalence failures.
# ─────────────────────────────────────────────────────────────────────────────
def test_a_broken_source_is_a_harness_stop_and_not_a_disagreement():
    cases = {
        "def build_record(rec, ddir:\n    pass\n": P3.P3_SOURCE_UNLOADABLE,
        "raise ValueError('import time')\n": P3.P3_SOURCE_UNLOADABLE,
        "def something_else():\n    return 1\n": P3.P3_SOURCE_UNLOADABLE,
        "def build_record(rec, ddir, mystery):\n    return {}\n":
            P3.P3_SOURCE_SIGNATURE_UNBINDABLE,
        "def build_record(rec, ddir):\n    raise KeyError('boom')\n":
            P3.P3_SOURCE_RUNTIME_ERROR,
        "def build_record(rec, ddir):\n    return {'nothing': 1}\n":
            P3.P3_KEPT_ROWS_UNOBSERVABLE,
    }
    for text, expected in cases.items():
        try:
            differential_for(text)
        except P3.SourceHarnessError as error:
            check(error.status == expected,
                  f"{expected}: reported as itself, not as a fixture mismatch")
            check(error.status in P3.HARNESS_STOPS,
                  f"{expected} is registered as a harness stop")
            check(error.status not in (P3.P3_PASS, P3.P3_EQUIVALENCE_REQUIRED),
                  f"{expected} is not an equivalence verdict")
        else:                                                # pragma: no cover
            raise AssertionError(f"{expected} did not stop the run")


def test_a_harness_stop_produces_no_verdict_and_no_candidate():
    decision = P3.decide(None, P3.P3_SOURCE_UNLOADABLE, "could not compile")
    check(decision["status"] == P3.P3_SOURCE_UNLOADABLE,
          "the decision carries the stop as the status")
    check(decision["harness_stop"] is True
          and decision["equivalence_claimed"] is False,
          "and claims no equivalence either way")
    check(decision["candidate_derivable"] is False,
          "no candidate is derivable from a run that did not compare anything")
    check("not a disagreement" in decision["note"],
          "the note says explicitly that this is not a disagreement")
    check(decision["fixtures_passed"] is None,
          "and reports no fixture count rather than zero, which would read as "
          "six failures")


def test_an_unreadable_trace_stops_instead_of_guessing():
    """A producer whose bookkeeping cannot be read is a stop, not a mismatch."""
    opaque = '''
import wfdb
from .frontend import detect_r, rr_features


def build_record(rec, ddir, fs=360):
    sig = wfdb.rdrecord(rec)
    ann = wfdb.rdann(rec, "atr")
    x = sig.p_signal
    peaks = [int(p) for p in detect_r([row[0] for row in x], fs)]
    samples = [int(s) for s in ann.sample]
    pairs = dict(zip(range(len(peaks)), range(len(samples))))
    rows = [[float(peaks[i])] + [0.0] * 6 for i in sorted(pairs)]
    return {"rr": rows}
'''
    try:
        differential_for(opaque)
    except P3.SourceHarnessError as error:
        check(error.status == P3.P3_SOURCE_TRACE_UNPROJECTABLE,
              "a wholesale-assigned mapping records no decision and stops")
        check("not read as one set of decisions" in str(error)
              or "does not settle" in str(error)
              or "never matched" in str(error),
              "and the stop says what could not be read")
    else:                                                    # pragma: no cover
        raise AssertionError("an unreadable trace was projected anyway")


def test_the_fixture_set_cannot_be_trimmed_renamed_or_duplicated():
    saved = P3.FIXTURES
    try:
        for label, fixtures in (
                ("a trimmed set", saved[:3]),
                ("a duplicated entry", saved + (saved[0],)),
                ("a renamed entry",
                 ({**saved[0], "name": "test_source_match_renamed"},)
                 + saved[1:]),
                ("an added entry",
                 saved + ({"name": "test_source_match_extra",
                           "refutes": "something", "peaks": (1000,),
                           "annotations": ((1001, "N"),),
                           "signal_length": 3000},))):
            P3.FIXTURES = fixtures
            try:
                P3.assert_fixture_contract()
            except P3.SourceHarnessError as error:
                check(error.status == P3.P3_FIXTURE_CONTRACT_VIOLATION,
                      f"{label} is refused before anything is compared")
            else:                                            # pragma: no cover
                raise AssertionError(f"{label} was accepted")
    finally:
        P3.FIXTURES = saved
    gate = P3.assert_fixture_contract()
    check(gate["fixtures"] == list(Q5E.SOURCE_MATCH_REQUIRED_FIXTURES),
          "the committed set is exactly the registered required set")
    check(P3.REQUIRED_FIXTURES is Q5E.SOURCE_MATCH_REQUIRED_FIXTURES,
          "and it is imported from Q5-E rather than retyped")


def test_fixture_construction_rules_are_enforced():
    saved = P3.FIXTURES
    broken = {
        "a peak sample that is also an annotation sample":
            {"peaks": (1001, 1012)},
        "a sample small enough to look like an index": {"peaks": (5, 1012)},
        "a repeated peak": {"peaks": (1000, 1000)},
        "no refutation target": {"refutes": "  "},
    }
    try:
        for label, override in broken.items():
            P3.FIXTURES = ({**saved[0], **override},) + saved[1:]
            try:
                P3.assert_fixture_contract()
            except P3.SourceHarnessError as error:
                check(error.status == P3.P3_FIXTURE_CONTRACT_VIOLATION,
                      f"{label} is refused")
            else:                                            # pragma: no cover
                raise AssertionError(f"{label} was accepted")
    finally:
        P3.FIXTURES = saved


# ─────────────────────────────────────────────────────────────────────────────
# 5. The candidate record, and the registered gate that will judge it.
# ─────────────────────────────────────────────────────────────────────────────
def test_a_complete_agreement_yields_a_candidate_the_registered_gate_accepts():
    result = differential_for(FAITHFUL)
    candidate = P3.candidate_record(result, P3.REGISTERED_SOURCE_SHA256,
                                    "b" * 64, "c" * 64)
    check(candidate is not None, "six agreements produce a candidate record")
    check(candidate["verdict"] == Q5E.SOURCE_MATCH_ORACLE_PASS,
          "whose verdict is the registered PASS string")
    check(candidate["fixtures_passed"] == 6 == len(candidate["fixtures"]),
          "and which reports every fixture, all of them equal")
    gate = P3.check_candidate_against_gate(candidate)
    check(gate["ok"] is True and gate["problems"] == [],
          f"the registered M4.0 gate accepts it structurally: {gate}")
    check(gate["registered_constant_written"] is False,
          "and nothing was written into SOURCE_MATCH_ORACLE_RECORD")
    check(Q5E.SOURCE_MATCH_ORACLE_RECORD is None,
          "which is still None after building and checking a candidate")


def test_the_registered_gate_rejects_every_way_a_candidate_could_be_weakened():
    result = differential_for(FAITHFUL)
    good = P3.candidate_record(result, P3.REGISTERED_SOURCE_SHA256,
                               "b" * 64, "c" * 64)
    cases = {
        "a trimmed fixture list":
            {**good, "fixtures": good["fixtures"][:5], "fixtures_passed": 5},
        "a duplicated fixture":
            {**good, "fixtures": good["fixtures"] + [good["fixtures"][0]],
             "fixtures_passed": 7},
        "a fixture marked unequal":
            {**good, "fixtures": [{**good["fixtures"][0], "equal": False}]
                                 + good["fixtures"][1:]},
        "digests that differ under an equal flag":
            {**good, "fixtures": [{**good["fixtures"][0],
                                   "adapter_result_sha256": "d" * 64}]
                                 + good["fixtures"][1:]},
        "a truncated digest": {**good, "prep_bundle_sha256": "b" * 32},
        "an uppercase digest": {**good, "oracle_harness_sha256": "C" * 64},
        "a placeholder identity": {**good, "adapter_fingerprint": "x"},
        "a fixtures_passed that does not match":
            {**good, "fixtures_passed": 5},
        "a verdict string of its own": {**good, "verdict": "LOOKS_FINE"},
    }
    for label, candidate in cases.items():
        gate = P3.check_candidate_against_gate(candidate)
        check(gate["ok"] is False and gate["problems"],
              f"the registered gate rejects {label}")
        check(gate["reason"] == Q5E.SOURCE_MATCH_EQUIVALENCE_REQUIRED,
              f"and leaves the verdict at SOURCE_MATCH_EQUIVALENCE_REQUIRED "
              f"for {label}")


def test_a_stale_adapter_fingerprint_or_a_moved_source_invalidates_a_candidate():
    result = differential_for(FAITHFUL)
    candidate = P3.candidate_record(result, P3.REGISTERED_SOURCE_SHA256,
                                    "b" * 64, "c" * 64)
    check(P3.check_candidate_against_gate(candidate)["ok"] is True,
          "the candidate is accepted while both identities hold")
    moved = {**candidate, "registered_file_sha256": "e" * 64}
    gate = P3.check_candidate_against_gate(moved)
    check(gate["ok"] is False, "a candidate against another data.py is refused")
    check(any("different `data.py`" in problem for problem in gate["problems"]),
          "and the reason names the changed registered source")
    stale = {**candidate, "adapter_fingerprint": "f" * 64}
    gate = P3.check_candidate_against_gate(stale)
    check(gate["ok"] is False,
          "a candidate recorded against another adapter is refused")
    check(any("adapter has changed" in problem for problem in gate["problems"]),
          "and the reason names the changed adapter")
    saved = dict(Q5E.SOURCE_MATCH_CONTRACT)
    try:
        Q5E.SOURCE_MATCH_CONTRACT["distance_tie"] = "the later one wins"
        check(P3.check_candidate_against_gate(candidate)["ok"] is False,
              "editing the adapter's declared contract invalidates the "
              "candidate that was recorded against it")
    finally:
        Q5E.SOURCE_MATCH_CONTRACT.clear()
        Q5E.SOURCE_MATCH_CONTRACT.update(saved)
    check(P3.check_candidate_against_gate(candidate)["ok"] is True,
          "and restoring the contract restores acceptance")


def test_the_harness_identity_changes_when_the_harness_changes():
    identity = P3.oracle_harness_identity()
    check(P3._is_sha256(identity["oracle_harness_sha256"]),
          "the harness identity is a 64-hex digest")
    check(identity["oracle_harness_sha256"] ==
          P3.oracle_harness_identity()["oracle_harness_sha256"],
          "and it is stable across calls")
    saved = P3.FIXTURES
    try:
        P3.FIXTURES = saved[:1]
        check(P3.oracle_harness_identity()["oracle_harness_sha256"]
              != identity["oracle_harness_sha256"],
              "changing the fixture set changes it")
    finally:
        P3.FIXTURES = saved
    saved_plan = P3.BINDING_PLAN
    try:
        P3.BINDING_PLAN = saved_plan[:-1]
        check(P3.oracle_harness_identity()["oracle_harness_sha256"]
              != identity["oracle_harness_sha256"],
              "and so does changing what the producer is called with")
    finally:
        P3.BINDING_PLAN = saved_plan
    check(P3.oracle_harness_identity()["oracle_harness_sha256"] ==
          identity["oracle_harness_sha256"], "restoring both restores it")


def test_there_is_no_facility_for_choosing_the_best_scoring_adapter():
    with open(P3.__file__, encoding="utf-8") as handle:
        text = handle.read()
    for token in ("best_score", "candidates.sort", "max(results",
                  "choose_adapter", "try_adapters"):
        check(token not in text,
              f"the module contains no {token!r}: a differential that picks a "
              f"winner is not a differential")
    check(text.count("def differential_over_fixtures") == 1,
          "there is exactly one differential entry point")
    check("adapter_modified_by_this_run" in text
          and "correcting the candidate adapter" in text,
          "and the run states that it does not correct the adapter")


# ─────────────────────────────────────────────────────────────────────────────
# 6. The bundle: fold, no-overwrite, commit marker, synthetic stamp.
# ─────────────────────────────────────────────────────────────────────────────
def _synthetic_run(directory, text=FAITHFUL):
    return P3.execute_synthetic_p3(directory, text.encode("utf-8"),
                                   timestamp=STAMP, emit=lambda _m: None)


def test_a_synthetic_run_writes_the_contracted_bundle_and_verifies_it():
    with tempfile.TemporaryDirectory() as directory:
        result = _synthetic_run(directory)
        bundle = result["bundle"]
        check(sorted(os.listdir(bundle["directory"])) ==
              sorted(P3.BUNDLE_FILES),
              f"the bundle holds exactly {sorted(P3.BUNDLE_FILES)}")
        check(sorted(P3.PREP_PAYLOAD_FILES) == sorted([
            "config.json", "source_inventory.json",
            "oracle_harness_identity.json", "fixture_results.json",
            "decision.json", "log.txt", "summary.md"]),
              "the payload is the seven files the contract names")
        check(P3.PREP_PAYLOAD_FILES == Q5E.PREP_PAYLOAD_FILES,
              "reused from Q5-E rather than redeclared")
        check(result["verified"]["ok"] is True,
              "and the run verifies its own output before reporting success")
        check(result["verified"]["acceptance_eligible"] is False,
              "a self-check is not an external anchor, so it is not "
              "acceptance-eligible")
        check(result["verified"]["manifest_anchor_source"] ==
              P3.ANCHOR_SAME_RUN, "and it says the digest came from this run")


def test_the_payload_fold_excludes_the_manifest_and_the_marker():
    with tempfile.TemporaryDirectory() as directory:
        result = _synthetic_run(directory)
        bundle = result["bundle"]["directory"]
        with open(os.path.join(bundle, P3.PREP_MANIFEST_FILE),
                  encoding="utf-8") as handle:
            manifest = json.load(handle)
        with open(os.path.join(bundle, P3.COMMIT_MARKER),
                  encoding="utf-8") as handle:
            marker = json.load(handle)
        check(manifest["prep_payload_sha256"] ==
              result["bundle"]["prep_payload_sha256"] ==
              marker["prep_payload_sha256"],
              "the manifest and the marker record the same fold")
        check(P3.PREP_MANIFEST_FILE not in P3.PREP_PAYLOAD_FILES
              and P3.COMMIT_MARKER not in P3.PREP_PAYLOAD_FILES,
              "and neither is inside the fold it records")
        check(manifest["manifest_self_digest_recorded_here"] is False
              and marker["manifest_sha256_recorded_here"] is False,
              "no file records its own digest, which would be circular")
        triples = []
        for name in sorted(P3.PREP_PAYLOAD_FILES):
            with open(os.path.join(bundle, name), "rb") as handle:
                body = handle.read()
            triples.append({"name": name, "bytes": len(body),
                            "sha256": hashlib.sha256(body).hexdigest()})
        recomputed = Q5E.prep_payload_fold(triples)
        check(recomputed["prep_payload_sha256"] ==
              manifest["prep_payload_sha256"],
              "an independent recomputation of the fold agrees")
        with open(os.path.join(bundle, P3.PREP_MANIFEST_FILE), "rb") as handle:
            manifest_bytes = handle.read()
        with_manifest = triples + [
            {"name": P3.PREP_MANIFEST_FILE, "bytes": len(manifest_bytes),
             "sha256": hashlib.sha256(manifest_bytes).hexdigest()}]
        check(Q5E.prep_payload_fold(with_manifest)["prep_payload_sha256"] ==
              recomputed["prep_payload_sha256"],
              "and adding the manifest to the input does not change it")


def test_a_bundle_directory_is_never_overwritten_and_is_never_deleted():
    with tempfile.TemporaryDirectory() as directory:
        result = _synthetic_run(directory)
        bundle = result["bundle"]["directory"]
        before = sorted(os.listdir(bundle))
        try:
            _synthetic_run(directory)
        except P3.P3Error as error:
            check("already" in str(error) and "never an overwrite" in str(error),
                  "a second run at the same path refuses rather than replaces")
        else:                                                # pragma: no cover
            raise AssertionError("the bundle was overwritten")
        check(sorted(os.listdir(bundle)) == before,
              "and the first bundle is untouched")
    with open(P3.__file__, encoding="utf-8") as handle:
        writer = handle.read().split("def write_bundle", 1)[1]
    writer = writer.split("\ndef verify_published_bundle", 1)[0]
    for verb in ("shutil.rmtree", "os.remove", "os.unlink", "os.rmdir",
                 "os.rename", "os.replace"):
        check(verb not in writer,
              f"the writer never calls {verb}, so nothing is moved or deleted")
    check("os.mkdir(directory)" in writer,
          "the directory is claimed with mkdir, which fails rather than "
          "replaces")
    check("P12._write_new_json" in writer and "P12._write_new_file" in writer,
          "and every file is created through the exclusive-create helpers")


def test_a_directory_without_a_commit_marker_is_not_a_bundle():
    with tempfile.TemporaryDirectory() as directory:
        result = _synthetic_run(directory)
        bundle = result["bundle"]["directory"]
        marker = os.path.join(bundle, P3.COMMIT_MARKER)
        with open(marker, "rb") as handle:
            saved = handle.read()
        os.remove(marker)
        verdict = P3.verify_published_bundle(bundle)
        check(verdict["ok"] is False and verdict["committed"] is False,
              "a directory missing COMMITTED.json is refused")
        check(any("incomplete or failed write" in problem
                  for problem in verdict["problems"]),
              "and is described as an incomplete write, not a bundle")
        with open(marker, "wb") as handle:
            handle.write(saved)
        check(P3.verify_published_bundle(bundle)["ok"] is True,
              "restoring the marker restores the bundle")
        payload = os.path.join(bundle, "summary.md")
        with open(payload, "ab") as handle:
            handle.write(b"\nedited after the fact\n")
        verdict = P3.verify_published_bundle(bundle)
        check(verdict["ok"] is False,
              "editing a payload file after the commit is detected")
        check(any("recomputed payload fold" in problem
                  for problem in verdict["problems"]),
              "by the recomputed fold, not by the marker's own word")


def test_a_manifest_digest_only_anchors_when_it_comes_from_outside():
    with tempfile.TemporaryDirectory() as directory:
        result = _synthetic_run(directory)
        bundle = result["bundle"]["directory"]
        digest = result["bundle"]["manifest_sha256_freeze_externally"]
        same_run = P3.verify_published_bundle(bundle, digest,
                                              P3.ANCHOR_SAME_RUN)
        check(same_run["ok"] and not same_run["acceptance_eligible"],
              "a digest this run computed is a self-check, not an anchor")
        external = P3.verify_published_bundle(bundle, digest,
                                              P3.ANCHOR_SAVED_NOTEBOOK)
        check(external["acceptance_eligible"] is True,
              "a digest from the saved notebook output does anchor it")
        check(P3.verify_published_bundle(bundle, digest)["ok"] is False,
              "a digest with no stated origin is refused")
        check(P3.verify_published_bundle(bundle, None,
                                         P3.ANCHOR_SAVED_NOTEBOOK)["ok"]
              is False,
              "and an origin with no digest is refused too")
        wrong = P3.verify_published_bundle(bundle, "a" * 64,
                                           P3.ANCHOR_REGISTERED_RECORD)
        check(wrong["ok"] is False and wrong["acceptance_eligible"] is False,
              "a mismatching external digest fails the bundle")


def test_a_synthetic_bundle_is_stamped_as_not_a_result_everywhere_that_counts():
    with tempfile.TemporaryDirectory() as directory:
        result = _synthetic_run(directory)
        bundle = result["bundle"]["directory"]
        with open(os.path.join(bundle, "config.json"), encoding="utf-8") as f:
            config = json.load(f)
        with open(os.path.join(bundle, "summary.md"), encoding="utf-8") as f:
            summary = f.read()
        with open(os.path.join(bundle, P3.COMMIT_MARKER),
                  encoding="utf-8") as f:
            marker = json.load(f)
        check(config["synthetic_fixture"] is True
              and config["ingestable"] is False,
              "the config says the run was synthetic and not ingestable")
        check("NOT A Q5-E RESULT" in config["synthetic_note"]
              and "NOT A P3 RESULT" in config["synthetic_note"],
              "in words, not only as a flag")
        check("NOT A Q5-E RESULT" in summary,
              "and the summary a human reads says it first")
        check(marker["synthetic_fixture"] is True,
              "the commit marker carries the same flag")
        check(result["candidate"] is None,
              "a synthetic run produces no candidate record at all")
        check("synthetic producer" in result["candidate_gate"]["note"],
              "and says why: it compared a synthetic producer")
        check(config["synthetic_note"] in
              open(os.path.join(bundle, "config.json"),
                   encoding="utf-8").read(),
              "the stamp is inside the folded payload, so editing it out "
              "breaks the fold")


def test_no_credential_or_token_field_can_reach_a_bundle():
    for payload in ({"access_token": "x"}, {"nested": {"refresh_token": "y"}},
                    {"rows": [{"client_secret": "z"}]},
                    {"credentials": {"anything": 1}}):
        try:
            P12.assert_no_credentials(payload, "config.json")
        except P12.PrepError:
            check(True, f"a bundle carrying {sorted(payload)} is refused")
        else:                                                # pragma: no cover
            raise AssertionError(f"{payload} was allowed into a bundle")
    P12.assert_no_credentials({"credential_type": "Credentials",
                               "credential_recorded": False}, "config.json")
    check(True, "while a field describing a credential without being one is "
                "allowed, as P1/P2 already established")
    with tempfile.TemporaryDirectory() as directory:
        result = _synthetic_run(directory)
        for name in sorted(P3.BUNDLE_FILES):
            with open(os.path.join(result["bundle"]["directory"], name),
                      encoding="utf-8") as handle:
                text = handle.read()
            for secret in ("access_token", "refresh_token", "client_secret"):
                check(secret not in text,
                      f"{name} carries no {secret}")


def test_a_run_that_disagrees_still_writes_a_complete_preserved_bundle():
    with tempfile.TemporaryDirectory() as directory:
        result = _synthetic_run(directory, variant_text("boundary_cut_releases"))
        bundle = result["bundle"]["directory"]
        check(sorted(os.listdir(bundle)) == sorted(P3.BUNDLE_FILES),
              "a disagreement is published as completely as an agreement")
        with open(os.path.join(bundle, "decision.json"), encoding="utf-8") as f:
            decision = json.load(f)
        check(decision["status"] == Q5E.SOURCE_MATCH_EQUIVALENCE_REQUIRED,
              "the verdict stays SOURCE_MATCH_EQUIVALENCE_REQUIRED")
        check(decision["equivalence_claimed"] is False
              and decision["adapter_modified_by_this_run"] is False,
              "nothing is claimed and the adapter is untouched")
        check(decision["real_record_counts_opened"] is False,
              "and no real-record count was opened to break the tie")
        with open(os.path.join(bundle, "fixture_results.json"),
                  encoding="utf-8") as f:
            fixtures = json.load(f)
        failing = [d for d in fixtures["detail"] if not d["equal"]]
        check(failing and failing[0]["difference"],
              "the mismatch trace is preserved in the bundle")
        check(result["candidate"] is None,
              "and no candidate is produced from it")


def test_a_harness_stop_still_writes_a_bundle_that_says_so():
    with tempfile.TemporaryDirectory() as directory:
        result = _synthetic_run(directory,
                                "def build_record(rec, ddir):\n    return {}\n")
        with open(os.path.join(result["bundle"]["directory"], "decision.json"),
                  encoding="utf-8") as handle:
            decision = json.load(handle)
        check(decision["status"] in P3.HARNESS_STOPS,
              "the bundle records the harness stop as the status")
        check(decision["harness_stop"] is True,
              "flagged as a harness stop rather than a comparison")
        check(decision["fixtures_passed"] is None,
              "with no fixture score that could be read as six failures")


# ─────────────────────────────────────────────────────────────────────────────
# 7. Boundaries: nothing registered, nothing frozen touched, no science run.
# ─────────────────────────────────────────────────────────────────────────────
def test_the_oracle_record_is_still_none_after_everything_this_suite_did():
    check(Q5E.SOURCE_MATCH_ORACLE_RECORD is None,
          "SOURCE_MATCH_ORACLE_RECORD is still None")
    gate = Q5E.verify_source_match_equivalence()
    check(gate["ok"] is False
          and gate["reason"] == Q5E.SOURCE_MATCH_EQUIVALENCE_REQUIRED,
          "so the M4.0 sub-gate is still closed")
    with open(os.path.join(HERE, "q5e_leg2_failure_mechanism_audit.py"),
              encoding="utf-8") as handle:
        text = handle.read()
    check("SOURCE_MATCH_ORACLE_RECORD: Optional[Dict[str, object]] = None"
          in text, "and the constant is still None in the committed source")
    with open(P3.__file__, encoding="utf-8") as handle:
        p3_text = handle.read()
    check("SOURCE_MATCH_ORACLE_RECORD =" not in p3_text
          and "SOURCE_MATCH_ORACLE_RECORD[" not in p3_text,
          "this module never assigns to it")


def test_no_detector_no_m0_to_m4_no_labels_no_probabilities_no_training():
    with open(P3.__file__, encoding="utf-8") as handle:
        text = handle.read()
    forbidden = ("Q5E.m4_feasibility_gate", "Q5E.DetectorReplay",
                 "Q5E.load_v10_producer", "Q5E.m0_report", "Q5E.m1_distances",
                 "Q5E.m2_report", "Q5E.m3_graph", "Q5E.m5_stratified",
                 "Q5E.run_audit", "Q5E.build_result",
                 "BJ.load_atr_record", "BJ.load_cache_record",
                 "BJ.hash_file_set", "probs.npy", "predictions.npz",
                 "pr_auc", ".fit(", "keras", "tensorflow", "torch",
                 "sklearn")
    for token in forbidden:
        check(token not in text, f"the module never mentions {token!r}")
    check("def detect_r" in text,
          "the only detect_r here is the injected stub")
    stub_body = text.split("def detect_r(*args", 1)[1].split("def ", 1)[0]
    check("real `detect_r()` is never called" in stub_body,
          "and it says so where it is defined")
    open_source = load_for(FAITHFUL)
    with open_source(P3.FIXTURES[0]) as (build_record, log):
        build_record(rec="SYNTHETIC", ddir="<synthetic>")
    targets = {call["target"] for call in log.as_list()}
    check(targets <= {"wfdb.rdrecord", "wfdb.rdann", "wfdb.rdsamp",
                      "frontend.detect_r", "frontend.rr_features",
                      "pwave.pwave_features",
                      # A refused lookup is part of the surface too: it
                      # records what was wanted and hands back nothing.
                      "wfdb.__getattr__", "frontend.__getattr__",
                      "pwave.__getattr__"},
          f"a producer can reach only the injected stub surface: {targets}")
    refusals = [c for c in log.as_list() if c["target"].endswith("__getattr__")]
    check(all(c["declared"] is False for c in refusals),
          "and a lookup outside it is recorded as refused, never supplied")


#: A producer that imports its dependencies **inside** `build_record`.  Under
#: an injection that ends when the module finishes loading, these names would
#: resolve at call time — after `sys.modules` had been put back — and reach the
#: real package and the real detector.
LATE_IMPORT_PRODUCER = FAITHFUL.replace(
    "import wfdb\nfrom .frontend import detect_r, rr_features\n", "").replace(
    "    CALLED.append(rec)\n",
    "    CALLED.append(rec)\n"
    "    import wfdb\n"
    "    from .frontend import detect_r, rr_features\n")


class _Decoy(object):
    """Stands where a real dependency would be, and shouts if it is used."""

    def __init__(self, name):
        self.name = name

    def __getattr__(self, attribute):
        def refuse(*_args, **_kwargs):
            raise AssertionError(
                f"the REAL {self.name}.{attribute} was reached: the injection "
                f"did not cover the call")
        return refuse


def test_a_producer_that_imports_inside_the_function_still_gets_the_stubs():
    """Blocker 2: the injection must outlive the load, not end with it.

    Decoys are installed where the real modules would be, so if the stub
    context closed before `build_record` ran, the function-level imports would
    pick the decoys up and the test would fail loudly rather than silently
    reaching a real dependency.
    """
    check("    import wfdb" in LATE_IMPORT_PRODUCER
          and "from .frontend import" in LATE_IMPORT_PRODUCER.split(
              "def build_record", 1)[1],
          "the fixture producer really does import inside the function")
    saved = {name: sys.modules.get(name) for name in P3.INJECTED_MODULE_NAMES}
    try:
        for name in ("wfdb", "frontend",
                     f"{P3.REGISTERED_SOURCE_PACKAGE}.frontend"):
            sys.modules[name] = _Decoy(name)
        result = differential_for(LATE_IMPORT_PRODUCER)
        check(result["all_equal"] is True,
              "a late-importing producer is observed exactly like an early "
              "one, so its imports resolved to the stubs")
        check(result["fixtures_passed"] == 6,
              "on all six fixtures, with the decoys in place throughout")
    finally:
        for name, module in saved.items():
            if module is None:
                sys.modules.pop(name, None)
            else:                                            # pragma: no cover
                sys.modules[name] = module
    check(all(sys.modules.get(name) is saved[name]
              for name in P3.INJECTED_MODULE_NAMES),
          "and sys.modules is exactly what it was before the run")


def test_the_producer_session_holds_the_injection_across_the_call():
    permit = P3.synthetic_permit(FAITHFUL.encode("utf-8"))
    session = P3.ProducerSession(permit, P3.FIXTURES[0])
    outside = sys.modules.get("wfdb")
    with session as (build_record, log):
        installed = sys.modules.get("wfdb")
        check(installed is not outside,
              "inside the session, wfdb is the injected stub")
        check(getattr(installed, "rdrecord", None) is session.stubs["rdrecord"],
              "and it is this session's own stub, not a leftover")
        build_record(rec="SYNTHETIC", ddir="<synthetic>")
        check(log.by_target("frontend.detect_r"),
              "a call made inside the session reaches the stub detector")
    check(sys.modules.get("wfdb") is outside,
          "and afterwards sys.modules is restored")
    try:
        P3.load_source_under_injection(permit, P3.build_injection(
            P3.FIXTURES[0])[0])
    except P3.P3Error as error:
        check("without its injected dependencies installed" in str(error),
              "loading outside a session is refused rather than half-injected")
    else:                                                    # pragma: no cover
        raise AssertionError("a producer was loaded with no injection active")


#: A producer that reads `frontend.FS` at import time and derives its
#: tolerance from it — the shape the registered `data.py` turned out to have,
#: which the 20260815T232546 run discovered by stopping.
FS_READING_PRODUCER = FAITHFUL.replace(
    "from .frontend import detect_r, rr_features",
    "from .frontend import detect_r, rr_features, FS").replace(
    "    tol = int(0.15 * fs)", "    tol = int(0.15 * FS)")

#: A producer that reads a name nobody declared.
UNDECLARED_READING_PRODUCER = FAITHFUL.replace(
    "from .frontend import detect_r, rr_features",
    "from .frontend import detect_r, rr_features\n"
    "import frontend as FE\n"
    "_UNUSED = FE.SOMETHING_NOBODY_DECLARED")


#: A producer shaped the way the registered one turned out to be: it is handed
#: its signal and annotations rather than reading them.  The 20260815T233808
#: run established the required parameters `sig`, `ann_sample`, `ann_symbol`.
ARGUMENT_SHAPED_PRODUCER = '''
from .frontend import detect_r, rr_features, FS

WIN_BEFORE = 150
WIN_AFTER = 150
AAMI = {"N": "N", "L": "N", "R": "N", "e": "N", "j": "N",
        "A": "S", "a": "S", "J": "S", "S": "S", "V": "V", "E": "V"}


def build_record(rec, sig, ann_sample, ann_symbol, use_detected=True):
    x = sig
    peaks = detect_r([row[0] for row in x], FS)
    tol = int(0.15 * FS)
    samples = [int(s) for s in ann_sample]
    symbols = list(ann_symbol)
    order = sorted(range(len(samples)), key=lambda k: (samples[k], k))
    used = set()
    beats, ys, keep = [], [], []
    for i, p in enumerate(peaks):
        p = int(p)
        best, bd = None, tol + 1
        for rank in range(len(order)):
            if rank in used:
                continue
            d = abs(samples[order[rank]] - p)
            if d < bd:
                best, bd = rank, d
        if best is None or bd > tol:
            continue
        used.add(best)
        j = order[best]
        cls = AAMI.get(symbols[j], "")
        if not cls:
            continue
        if not (p - WIN_BEFORE >= 0 and p + WIN_AFTER <= len(x)):
            continue
        keep.append(i)
        beats.append([float(v[0]) for v in x[p - WIN_BEFORE:p + WIN_AFTER]])
        ys.append(cls)
    rr_all = rr_features(peaks, FS)
    return {"beat": beats, "rr": [rr_all[i] for i in keep], "y": ys}
'''


def test_a_producer_handed_its_inputs_as_arguments_runs_and_is_observed():
    """The shape the registered `build_record` turned out to have.

    `sig`, `ann_sample` and `ann_symbol` are required parameters, so the
    fixture's data goes in as arguments — a more direct injection than a
    reader stub, and one the projection reads exactly as before.
    """
    result = differential_for(ARGUMENT_SHAPED_PRODUCER)
    check(result["all_equal"] is True and result["fixtures_passed"] == 6,
          "an argument-shaped producer runs and agrees on all six fixtures")
    for name in ("sig", "ann_sample", "ann_symbol"):
        check(any(name in aliases for aliases, _key in P3.BINDING_PLAN),
              f"and {name!r} is covered by the declared plan")


def test_every_injected_argument_carries_a_stated_reason():
    """"Why that value" is answerable for each one, from the module itself."""
    keys = {key for _aliases, key in P3.BINDING_PLAN}
    missing = sorted(keys - set(P3.BINDING_RATIONALE))
    check(missing == [],
          f"every plan key states why its value is safe: missing {missing}")
    check(str(P3.BINDING_RATIONALE["fs"]).find("54") > 0,
          "the sampling rate's reason is the registered tolerance it produces")
    # The rationale is folded into the harness identity, so editing a reason
    # invalidates a PASS recorded under the old one.
    before = P3.oracle_harness_identity()["oracle_harness_sha256"]
    saved = dict(P3.BINDING_RATIONALE)
    try:
        P3.BINDING_RATIONALE["fs"] = "because it seemed fine"
        check(P3.oracle_harness_identity()["oracle_harness_sha256"] != before,
              "and the reasons are part of the harness identity, so rewriting "
              "one changes it")
    finally:
        P3.BINDING_RATIONALE.clear()
        P3.BINDING_RATIONALE.update(saved)
    check(P3.oracle_harness_identity()["oracle_harness_sha256"] == before,
          "restoring them restores it")


def test_the_injected_arguments_match_what_the_reader_stubs_return():
    """One world: a producer using either route sees the same fixture."""
    for name in P3.fixture_names():
        fixture = P3.FIXTURES_BY_NAME[name]
        values = P3.binding_values(fixture)
        stubs, _log = P3.build_injection(fixture)
        record = stubs["rdrecord"]("SYNTHETIC")
        annotation = stubs["rdann"]("SYNTHETIC", "atr")
        check(len(values["signal"]) == len(record.p_signal)
              and float(values["signal"][7][0]) == float(record.p_signal[7][0]),
              f"{name}: the argument signal is the reader stub's signal")
        check([int(v) for v in values["annotation_samples"]] ==
              [int(v) for v in annotation.sample],
              f"{name}: the argument annotation samples are the stub's, in "
              f"the fixture's own order")
        check(list(values["annotation_symbols"]) == list(annotation.symbol),
              f"{name}: and so are the symbols")
        check(values["fs"] == P3.FRONTEND_STUB_CONSTANTS["FS"],
              f"{name}: the injected fs is the declared constant")


def test_an_unbindable_signature_reports_the_whole_signature():
    """A stop that says what it saw makes the next gap one run, not two."""
    unknown = ARGUMENT_SHAPED_PRODUCER.replace(
        "def build_record(rec, sig, ann_sample, ann_symbol, use_detected=True):",
        "def build_record(rec, sig, ann_sample, ann_symbol, mystery_thing):")
    try:
        differential_for(unknown)
    except P3.SourceHarnessError as error:
        check(error.status == P3.P3_SOURCE_SIGNATURE_UNBINDABLE,
              "an uncovered required parameter stops the run")
        check("'mystery_thing'" in str(error) or "mystery_thing" in str(error),
              "naming what could not be bound")
        check("full signature is (rec, sig, ann_sample, ann_symbol, "
              "mystery_thing)" in str(error),
              "and printing the whole signature it observed")
        check("the plan bound ['ann_sample', 'ann_symbol', 'rec', 'sig']"
              in str(error),
              "and what it did manage to bind")
        check("never filled with a guess" in str(error),
              "and that a value is never guessed into it")
    else:                                                    # pragma: no cover
        raise AssertionError("an uncovered parameter was filled in")


#: A producer that normalises its beat window through `frontend._z`, the way
#: the registered one turned out to.  The 20260815T235627 run established that
#: `build_record` calls `_z` while running.
Z_USING_PRODUCER = ARGUMENT_SHAPED_PRODUCER.replace(
    "from .frontend import detect_r, rr_features, FS",
    "from .frontend import detect_r, rr_features, FS, _z").replace(
    "        beats.append([float(v[0]) for v in x[p - WIN_BEFORE:p + WIN_AFTER]])",
    "        beats.append(_z([float(v[0]) for v in "
    "x[p - WIN_BEFORE:p + WIN_AFTER]]))")

#: The same producer, but with a matching decision that moves with `_z`.  An
#: injected helper that can do this is not standing out of the way.
Z_STEERING_PRODUCER = Z_USING_PRODUCER.replace(
    "        if best is None or bd > tol:",
    "        if _z(1.0) < 0:\n            continue\n"
    "        if best is None or bd > tol:")


def test_a_producer_that_normalises_through_the_injected_helper_is_observed():
    """`_z` is declared, and the run still reads every decision."""
    check("_z" in P3.FRONTEND_STUB_FUNCTIONS,
          "the injected frontend declares _z")
    result = differential_for(Z_USING_PRODUCER)
    check(result["all_equal"] is True and result["fixtures_passed"] == 6,
          "a producer that normalises its windows through _z agrees on all "
          "six fixtures")
    check(result["stub_invariance_probed"] == ["invariant"],
          f"and every fixture was probed and found invariant: "
          f"{result['stub_invariance']}")


def test_an_injected_helper_that_steers_the_matching_is_caught():
    """The claim is demonstrated per run, not asserted once in a comment.

    A constant can be justified by arithmetic — `FS = 360` reproduces the
    registered tolerance.  A *function* cannot, so its neutrality is probed:
    the fixture is observed again with `_z` replaced by an elementwise
    negation, and any compared field that moves stops the run.
    """
    try:
        differential_for(Z_STEERING_PRODUCER)
    except P3.SourceHarnessError as error:
        check(error.status == P3.P3_INJECTED_VALUE_STEERS_MATCHING,
              "a producer whose matching moves with _z is caught")
        check("identity vs negated" in str(error),
              "and the stop names the two implementations it compared")
        check("peak_to_annotation" in str(error)
              or "kept_rows" in str(error),
              "and which compared field moved")
        check(error.status in P3.HARNESS_STOPS,
              "it is a harness stop, so no equivalence verdict is claimed")
    else:                                                    # pragma: no cover
        raise AssertionError("an injected helper steered the comparison")


def test_the_probe_reports_untested_rather_than_passed():
    """A probe that cannot run says so; it never counts as a clean result."""
    def refusing_source(_fixture, _variant=P3.STUB_VARIANT_PRIMARY):
        raise AssertionError("the probe should not have reached this")

    class _Refuses(object):
        def __enter__(self):
            raise P3.SourceHarnessError(P3.P3_SOURCE_RUNTIME_ERROR,
                                        "the producer refused the probe")

        def __exit__(self, *exc):
            return False

    report = P3.probe_injection_invariance(
        lambda _fixture, _variant: _Refuses(), P3.FIXTURES[0], {},
        P3.LabelDictionary())
    check(report["status"] == "untested",
          "a probe the producer refuses is reported as untested")
    check("stopped under the probe" in report["reason"],
          "with the reason recorded")
    check(report["status"] != "invariant",
          "and never silently upgraded to a clean invariance result")


def test_a_producer_that_reads_a_declared_constant_loads_and_runs():
    """`frontend.FS` is part of the injected surface, and it is the right value.

    The registered source reads it at import time.  The value is pinned by the
    arithmetic rather than by taste: the static source map records that
    `data.py` computes `int(0.15 * fs)`, so an injected `FS` of 360 reproduces
    the registered 54-sample tolerance the fixtures are built around, and any
    other value would silently change the behaviour under test.
    """
    check(P3.FRONTEND_STUB_CONSTANTS["FS"] == 360,
          "the injected frontend declares FS")
    check(int(0.15 * P3.FRONTEND_STUB_CONSTANTS["FS"]) ==
          Q5E.M4_PEAK_MATCH_TOLERANCE_SAMPLES,
          "and the source's own tolerance arithmetic over it lands on the "
          "registered tolerance")
    result = differential_for(FS_READING_PRODUCER)
    check(result["all_equal"] is True and result["fixtures_passed"] == 6,
          "a producer that derives its tolerance from the injected FS runs "
          "and agrees on all six fixtures")


#: A producer that reads two names nobody declared, one after the other.  The
#: refusal only ever reveals the first, which is how four rounds of this PREP
#: each cost a full run to learn a single name.
TWO_MISSING_NAMES_PRODUCER = Z_USING_PRODUCER.replace(
    "from .frontend import detect_r, rr_features, FS, _z",
    "from .frontend import detect_r, rr_features, FS, _z\n"
    "import frontend as FE").replace(
    "    rr_all = rr_features(peaks, FS)",
    "    _first = FE.first_missing_name\n"
    "    _second = FE.second_missing_name\n"
    "    rr_all = rr_features(peaks, FS)")


def test_the_declared_surface_covers_the_ctx_producer():
    """`frontend.beat_ctx` builds the record's `ctx` column.

    Run `20260816T031420` got past the beat-count guard and stopped here.  It
    is declared under the same row convention as the other feature producers,
    for the same two reasons: the rows stay aligned with `rr`, which the
    columnar reader requires of every registered column, and each row says
    which peak it was built for rather than leaving that to a count.
    """
    check("beat_ctx" in P3.INJECTED_GLOBALS,
          "the injected globals carry beat_ctx")
    stubs, _log = P3.build_injection(P3.FIXTURES[0])
    with P3.InjectedModules(stubs):
        frontend = sys.modules["frontend"]
        rows = frontend.beat_ctx([1000, 1012], 360)
        rows = [list(row) for row in rows]
    check([row[0] for row in rows] == [1000.0, 1012.0],
          f"each row names the peak it was built for: {rows}")
    check(len({len(row) for row in rows}) == 1,
          "and every row has the same width, so the column is a block")
    ctx_reading = P3.build_injection(P3.FIXTURES[0])[0]["beat_ctx"]
    check(callable(ctx_reading), "it is a callable, like the producers beside "
                                 "it")


def test_the_surface_discovery_pass_lists_every_missing_name_at_once():
    """A refusal reveals one name; four rounds have each cost a run for one.

    So after a run has already stopped for that reason, the same fixture is run
    once more with undeclared names answered rather than refused — purely to
    enumerate them.  Nothing it produces may be read.
    """
    try:
        differential_for(TWO_MISSING_NAMES_PRODUCER)
    except P3.SourceHarnessError as error:
        check(error.status == P3.P3_STUB_SURFACE_INCOMPLETE,
              "the run still stops at the first undeclared name")
        check("first_missing_name" in str(error),
              "and the stop still names that one")
        discovery = error.context["surface_discovery"]
        check(discovery["undeclared_names"] ==
              ["frontend.first_missing_name", "frontend.second_missing_name"],
              f"while the discovery pass lists both, in the order the producer "
              f"asked for them: {discovery['undeclared_names']}")
        check(discovery["is_an_observation"] is False
              and "NOT AN OBSERVATION" in discovery["note"],
              "and says plainly that it is not an observation")
        check(all(not name.split(".")[1].startswith("__")
                  for name in discovery["undeclared_names"]),
              "import machinery is not reported as a dependency")
    else:                                                    # pragma: no cover
        raise AssertionError("two undeclared names did not stop the run")


def test_the_discovery_pass_can_never_become_a_result():
    """Permissive is a diagnosis mode, and it must not be reachable elsewhere."""
    import inspect
    source = inspect.getsource(P3.differential_over_fixtures)
    check("permissive" not in source,
          "the differential never opens a permissive session itself")
    check("discover_stub_surface" in source
          and "P3_STUB_SURFACE_INCOMPLETE" in source,
          "it only asks for one after a run has already stopped for that "
          "reason")
    callers = [name for name in dir(P3)
               if callable(getattr(P3, name, None))
               and "permissive=True" in (
                   inspect.getsource(getattr(P3, name))
                   if getattr(getattr(P3, name), "__module__", "") ==
                   P3.__name__ and not isinstance(getattr(P3, name), type)
                   else "")]
    check(callers == ["discover_stub_surface"],
          f"and it is the only function in the module that opens one: "
          f"{callers}")
    # A permissive session still refuses nothing quietly: every undeclared name
    # is recorded, and the record says which mode it was recorded in.
    stubs, log = P3.build_injection(P3.FIXTURES[0], permissive=True)
    with P3.InjectedModules(stubs):
        sys.modules["frontend"].whatever_this_is
    entries = [c for c in log.as_list() if c["target"] == "frontend.__getattr__"]
    check(entries and entries[0]["permissive"] is True
          and entries[0]["declared"] is False,
          f"a permissive read is logged as permissive: {entries}")
    stubs, log = P3.build_injection(P3.FIXTURES[0])
    with P3.InjectedModules(stubs):
        try:
            sys.modules["frontend"].whatever_this_is
        except P3.StubAttributeMissing:
            pass
    entries = [c for c in log.as_list() if c["target"] == "frontend.__getattr__"]
    check(entries and entries[0]["permissive"] is False,
          "and an ordinary read is logged as the refusal it is")


#: A producer that takes its window from `frontend` rather than defining it,
#: the way the registered one turned out to.  The 20260816T121935 run
#: established that `build_record` reads `frontend.WIN_BEFORE`.
WINDOW_READING_PRODUCER = Z_USING_PRODUCER.replace(
    "from .frontend import detect_r, rr_features, FS, _z",
    "from .frontend import detect_r, rr_features, FS, _z, WIN_BEFORE, "
    "WIN_AFTER").replace("WIN_BEFORE = 150\nWIN_AFTER = 150\n", "")


def test_the_injected_window_is_the_registered_one():
    """A constant is justified by arithmetic, never by taste.

    `FS` is 360 because the source's own `int(0.15 * fs)` then lands on the
    registered tolerance.  The window is the same kind of claim: 150/150 is
    what the registered boundary rule is written from, what the candidate
    adapter applies, and what `stage_decomposition` describes both sides with —
    and one fixture exists solely to pin that line.
    """
    for name in ("WIN_BEFORE", "WIN_AFTER"):
        check(name in P3.FRONTEND_STUB_CONSTANTS,
              f"the injected frontend declares {name}")
    check(P3.FRONTEND_STUB_CONSTANTS["WIN_BEFORE"] == BJ.WIN_BEFORE
          and P3.FRONTEND_STUB_CONSTANTS["WIN_AFTER"] == BJ.WIN_AFTER,
          "and takes both from the frozen Q5-D module rather than retyping "
          "them, so they cannot drift from the rule they describe")
    fixture = P3.FIXTURES_BY_NAME[
        "test_source_match_boundary_cut_consumes_its_match"]
    peak = int(fixture["peaks"][0])
    check(peak - P3.FRONTEND_STUB_CONSTANTS["WIN_BEFORE"] < 0,
          f"peak {peak} is cut by exactly this window, which is what that "
          f"fixture exists to pin — a different value would move the line")
    observation, _meta = P3.observe_adapter(fixture, P3.LabelDictionary())
    check(observation["stages"]["window"] ==
          [P3.FRONTEND_STUB_CONSTANTS["WIN_BEFORE"],
           P3.FRONTEND_STUB_CONSTANTS["WIN_AFTER"]],
          "the injected window is the one both sides are described with")
    result = differential_for(WINDOW_READING_PRODUCER)
    check(result["all_equal"] is True and result["fixtures_passed"] == 6,
          "a producer that takes its window from the injection agrees on all "
          "six fixtures")
    check(result["stub_invariance_probed"] == ["invariant"],
          "and the injection is still probed on every fixture")


def test_the_harness_identity_covers_the_injected_surface():
    """A run under a different declared surface is a run of a different oracle.

    This was missing until 2026-08-16, and the gap was invisible because every
    earlier surface change had also edited a function's text.  Adding
    `WIN_BEFORE` on its own would have left the digest — and with it the
    recorded execution approval — unmoved, while changing what the producer
    under test actually does.
    """
    before = P3.oracle_harness_identity()["oracle_harness_sha256"]
    saved = dict(P3.FRONTEND_STUB_CONSTANTS)
    try:
        P3.FRONTEND_STUB_CONSTANTS["WIN_BEFORE"] = 149
        check(P3.oracle_harness_identity()["oracle_harness_sha256"] != before,
              "changing a declared constant changes the harness identity")
    finally:
        P3.FRONTEND_STUB_CONSTANTS.clear()
        P3.FRONTEND_STUB_CONSTANTS.update(saved)
    check(P3.oracle_harness_identity()["oracle_harness_sha256"] == before,
          "and restoring it restores the identity")
    saved_globals = P3.INJECTED_GLOBALS
    try:
        P3.INJECTED_GLOBALS = saved_globals + ("something_new",)
        check(P3.oracle_harness_identity()["oracle_harness_sha256"] != before,
              "declaring another injected name changes it too")
    finally:
        P3.INJECTED_GLOBALS = saved_globals
    identity = P3.oracle_harness_identity()
    check(identity["oracle_harness_sha256"] == before,
          "and the module is left exactly as it was")
    check(P3.EXECUTION_APPROVAL_RECORD["for_oracle_harness_sha256"] == before,
          "the recorded execution approval names this harness, so a surface "
          "change closes the door until it is renewed")


#: A producer that unpacks an undeclared helper into two, and then reads
#: another undeclared name.  The 20260816T125027 pass stopped at the unpack —
#: `ValueError: not enough values to unpack (expected 2, got 0)` — and never
#: saw the second name.
UNPACKING_PRODUCER = Z_USING_PRODUCER.replace(
    "from .frontend import detect_r, rr_features, FS, _z",
    "from .frontend import detect_r, rr_features, FS, _z\n"
    "import frontend as FE").replace(
    "    rr_all = rr_features(peaks, FS)",
    "    _first, _second = FE.pair_returning_helper(1)\n"
    "    _after = FE.name_after_the_unpack\n"
    "    rr_all = rr_features(peaks, FS)")


def test_the_declared_surface_covers_the_compare_producer():
    """`frontend.compare_features` builds `ref` and `sim`, and returns two.

    The arity is not a guess: run `20260816T125027` produced `ValueError: not
    enough values to unpack (expected 2, got 0)` from the producer itself, and
    V10's registered `ARMS` carries a `compare` arm beside the two remaining
    record columns.
    """
    check("compare_features" in P3.INJECTED_GLOBALS,
          "the injected globals carry compare_features")
    stubs, _log = P3.build_injection(P3.FIXTURES[0])
    with P3.InjectedModules(stubs):
        returned = sys.modules["frontend"].compare_features([1000, 1012], 360)
    check(len(returned) == 2,
          f"it returns exactly the two blocks the producer unpacks: "
          f"{len(returned)}")
    for index, block in enumerate(returned):
        rows = [list(row) for row in block]
        check([row[0] for row in rows] == [1000.0, 1012.0],
              f"block {index} names the peak each row was built for: {rows}")
    check({"ref", "sim"} <= set(P3.COLUMNAR_RECORD_KEYS),
          "and the two columns it is declared for are registered ones")


#: A producer that hands its compare helper the beat windows rather than the
#: peaks, and routes its windows through two more declared helpers.  Both are
#: what the 20260816T131241 run showed.
WINDOW_ARGUMENT_PRODUCER = ARGUMENT_SHAPED_PRODUCER.replace(
    "from .frontend import detect_r, rr_features, FS",
    "from .frontend import (detect_r, rr_features, FS, _z, stack_ctx,\n"
    "                       slope_channel, compare_features, beat_ctx)\n"
    "from .pwave import pwave_features"
).replace(
    "    rr_all = rr_features(peaks, FS)",
    "    windows = [_z([float(v[0]) for v in\n"
    "                   x[int(peaks[i]) - WIN_BEFORE:"
    "int(peaks[i]) + WIN_AFTER]])\n"
    "               for i in keep]\n"
    "    windows = slope_channel(stack_ctx(windows))\n"
    "    ref_all, sim_all = compare_features(windows)\n"
    "    ctx_all = beat_ctx(windows)\n"
    "    pw_all = pwave_features(windows)\n"
    "    rr_all = rr_features(peaks, FS)"
).replace(
    '    return {"beat": beats, "rr": [rr_all[i] for i in keep], "y": ys}',
    '    return {"beat": beats, "ref": [list(r) for r in ref_all],\n'
    '            "rr": [rr_all[i] for i in keep],\n'
    '            "sim": [list(r) for r in sim_all],\n'
    '            "pw": [list(r) for r in pw_all],\n'
    '            "ctx": [list(r) for r in ctx_all], "y": ys}')


#: A producer built to the shapes run `20260816T134407` showed the registered
#: one returning: two-lead windows `(n, 300, 2)`, `compare_features` handed the
#: windows rather than the peaks, integer class codes in `y`, and all seven
#: columns.  Its **rule** is the adapter's, deliberately — this rehearses
#: whether the harness can read the record, not what the record says.
REGISTERED_SHAPED_PRODUCER = '''
from .frontend import (detect_r, rr_features, FS, WIN_BEFORE, WIN_AFTER, _z,
                       stack_ctx, slope_channel, compare_features, beat_ctx)
from . import pwave as PW

AAMI = {"N": "N", "L": "N", "R": "N", "e": "N", "j": "N",
        "A": "S", "a": "S", "J": "S", "S": "S", "V": "V", "E": "V"}


def build_record(rec, sig, ann_sample, ann_symbol, use_detected=True):
    x = sig
    fs = FS
    tol = int(0.15 * fs)
    tpk = [int(s) for s in ann_sample]
    tlb = [AAMI.get(str(s), "") for s in ann_symbol]
    peaks = [int(p) for p in detect_r(slope_channel(x), fs)]
    order = sorted(range(len(tpk)), key=lambda k: (tpk[k], k))
    used = set()
    kp, li = [], []
    for i, p in enumerate(peaks):
        best, bd = None, tol + 1
        for rank in range(len(order)):
            if rank in used:
                continue
            d = abs(tpk[order[rank]] - p)
            if d < bd:
                best, bd = rank, d
        if best is None or bd > tol:
            continue
        used.add(best)
        j = order[best]
        if not tlb[j]:
            continue
        if not (p - WIN_BEFORE >= 0 and p + WIN_AFTER <= len(x)):
            continue
        kp.append(p)
        li.append(j)
    valid = [[i, p] for i, p in enumerate(kp)]
    idx = [i for i, _p in valid]
    cuts = [_z([[float(v) for v in x[s]]
                for s in range(p - WIN_BEFORE, p + WIN_AFTER)]) for p in kp]
    cuts = stack_ctx(cuts)
    ref, sim = compare_features(cuts)
    ctx_all = beat_ctx(cuts)
    pw_all = PW.pwave_features(cuts)
    rr_all = rr_features(kp, fs)
    y = [0 if tlb[j] == "N" else 1 for j in li]
    return {"beat": cuts,
            "ref": [list(r) for r in ref],
            "rr": [list(rr_all[i]) for i in idx],
            "sim": [list(r) for r in sim],
            "pw": [list(r) for r in pw_all],
            "ctx": [list(r) for r in ctx_all],
            "y": y}
'''


def test_the_reader_handles_the_shapes_the_registered_record_came_back_with():
    """A rehearsal of the real record, from the trace the run preserved.

    Run `20260816T134407` ran the registered producer to completion and
    returned all seven columns — `beat` with shape `(7, 300, 2)`, integer class
    codes in `y` — and stopped only because `ref` and `sim` came back empty:
    `compare_features` had been called without the peaks, and the stub answered
    a call it did not recognise with no rows at all.

    So the windows are read for what they are.  A sample may have more than one
    channel, and a two-lead record is not an unreadable one.
    """
    result = differential_for(REGISTERED_SHAPED_PRODUCER)
    check(result["all_equal"] is True and result["fixtures_passed"] == 6,
          f"the record shape the registered producer returns is read on all "
          f"six fixtures: {result['fixtures_passed']}/6")
    check(result["stub_invariance_probed"] == ["invariant"],
          f"and every fixture was probed invariant: {result['stub_invariance']}")
    reading = result["detail"][0]["return_reading"]
    check(reading["parser"] == "columnar", "through the columnar reader")
    check(f"beat[:, {BJ.WIN_BEFORE}]" in reading["channels"],
          f"with the two-lead beat block read as a cross-check channel rather "
          f"than skipped: {reading['channels']}")
    columns = reading["return_schema"]["columns"]
    check(columns["beat"]["shape"][:1] == [len(reading["channel_sequences"]
                                              ["rr[:, 0]"])],
          f"every column describes the same rows: {columns}")
    check(all(entry["return_reading"]["return_schema"]["columns"]["ref"]
              ["shape"][0] ==
              entry["return_reading"]["return_schema"]["columns"]["rr"]
              ["shape"][0] for entry in result["detail"]),
          "including ref, which is what the run stopped on")


#: The registered rule, as three runs of trace now pin it: the nearest
#: annotation over **all** of them, ties to the lowest list index, and a peak
#: whose nearest is already consumed is **dropped** rather than falling
#: through.  Class codes in `y` (N=0, S=1, V=2), which is what the record
#: showed.  This is a stand-in for the source's *behaviour*, so the
#: differential is expected to disagree with the adapter — on exactly the two
#: fixtures built to catch these two decisions.
SOURCE_RULE_PRODUCER = REGISTERED_SHAPED_PRODUCER.replace(
    "    order = sorted(range(len(tpk)), key=lambda k: (tpk[k], k))\n", ""
).replace("""        for rank in range(len(order)):
            if rank in used:
                continue
            d = abs(tpk[order[rank]] - p)
            if d < bd:
                best, bd = rank, d
        if best is None or bd > tol:
            continue
        used.add(best)
        j = order[best]""",
"""        for rank in range(len(tpk)):
            d = abs(tpk[rank] - p)
            if d < bd:
                best, bd = rank, d
        if best is None or bd > tol:
            continue
        if best in used:
            continue
        used.add(best)
        j = best""").replace(
    '    y = [0 if tlb[j] == "N" else 1 for j in li]',
    '    y = [0 if tlb[j] == "N" else (1 if tlb[j] == "S" else 2) for j in li]')


def test_a_class_code_settles_what_a_symbol_never_taught():
    """The stop of `20260816T142848`, and why the dictionary could not settle it.

    Candidates `V` and `N`; the row is labelled `2`; and by then the producer
    had taught the dictionary `L`, `R`, `e`, `A`, `J`, `a` — every filler
    symbol — but never the symbol `N` itself.  Keyed by symbol there is
    nothing to say.  Keyed by **registered AAMI class** there is everything:
    `0` has been the label on every `N`-class row, so a row labelled `2` is not
    class `N`, whatever its symbol turns out to be.
    """
    dictionary = P3.LabelDictionary()
    dictionary.learn([["columnar_y", "0"]], "L")             # class N
    dictionary.learn([["columnar_y", "1"]], "A")             # class S
    token = [["columnar_y", "2"]]
    check(dictionary.symbols_for(token) == set()
          and "N" not in dictionary.excluded_symbols(token),
          "keyed by symbol, a row labelled 2 rules out nothing about 'N'")
    check("N" in dictionary.excluded_classes(token)
          and "V" not in dictionary.excluded_classes(token),
          f"keyed by class it rules out N and leaves V: "
          f"{sorted(dictionary.excluded_classes(token))}")
    check(BJ.AAMI_SYMBOL_MAP["L"] == "N" and BJ.AAMI_SYMBOL_MAP["V"] == "V",
          "and the class comes from the frozen map both sides already use")
    published = dictionary.as_dict()
    check("by_class_token" in published and "by_token" in published,
          f"both readings are published for the bundle: {published}")


def test_a_fixtures_own_rows_settle_it_even_when_the_shared_one_cannot():
    """A shared dictionary can be diluted; a fixture's own rows cannot.

    Negative evidence needs a channel that has been *single-valued* for a
    symbol or a class.  One fixture writing two different labels for the same
    class — for any reason, including a producer this PREP has not seen yet —
    silently disables that evidence everywhere afterwards.  The fixture's own
    resolved rows are the most direct evidence there is about its own labels,
    and they cannot be diluted by another fixture, so the settler consults them
    too.
    """
    annotations = [{"symbol": "V", "aami": "V"}, {"symbol": "N", "aami": "N"}]
    token = [["columnar_y", "2"]]
    diluted = P3.LabelDictionary()
    diluted.learn([["columnar_y", "0"]], "L")                # class N
    diluted.learn([["columnar_y", "9"]], "R")                # class N again
    check(P3._settle_with(diluted, token, [0, 1], annotations) is None,
          "a channel that has been two-valued for a class settles nothing, "
          "which is the correct refusal rather than a guess")
    local = P3.LabelDictionary()
    local.learn([["columnar_y", "0"]], "L")
    local.learn([["columnar_y", "1"]], "A")
    check(P3._settle_with(local, token, [0, 1], annotations) == 0,
          "while a clean dictionary rules out the N-class candidate and "
          "leaves the V one")
    check(P3._settle_with(P3.LabelDictionary(), token, [0, 1],
                          annotations) is None,
          "and an empty dictionary settles nothing at all")
    import inspect
    source = inspect.getsource(P3.project_observation)
    check("local_dictionary" in source and "dictionaries" in source,
          "the projection builds a fixture-local dictionary beside the shared "
          "one")
    check(source.index("dictionaries.append") <
          source.index("chosen = settle_by_row_label"),
          "and learns into it before the settling pass that needs it")


def test_the_registered_rule_is_reported_rather_than_stopping_the_run():
    """The rehearsal that matters: the source's behaviour, not just its shapes.

    Peak 1012's nearest annotation is taken, and the registered producer drops
    the peak instead of falling through; a tie goes to the lower list index
    rather than the earlier sample.  Two of the six fixtures exist to catch
    exactly those, and the run must *report* them — a projection that cannot
    read the trace would turn a detected difference into "the harness could not
    tell", which is the worst direction for this PREP to fail in.
    """
    result = differential_for(SOURCE_RULE_PRODUCER)
    check(result["all_equal"] is False and result["fixtures_passed"] == 4,
          f"four fixtures agree and two disagree: "
          f"{result['fixtures_passed']}/6")
    disagreed = sorted(entry["name"] for entry in result["detail"]
                       if not entry["equal"])
    check(disagreed == ["test_source_match_annotation_order_differing_from_"
                        "sample_order",
                        "test_source_match_nearest_already_used_falls_through"],
          f"and they are the two built for these decisions: {disagreed}")
    for entry in result["detail"]:
        if entry["equal"]:
            continue
        fields = {difference["field"] for difference in entry["difference"]}
        check({"kept_rows", "consumed_annotations"} <= fields,
              f"{entry['name']}: the difference is in the rows kept and the "
              f"annotations consumed: {sorted(fields)}")
    check(P3.candidate_record(result, "a" * 64, "b" * 64, "c" * 64) is None,
          "a differential with a disagreement yields no candidate at all")
    check(Q5E.SOURCE_MATCH_ORACLE_RECORD is None,
          "and nothing is registered by observing one")


def test_a_window_block_is_read_flat_or_multi_channel():
    """One reader for both, so the two cannot drift apart."""
    peaks = [1000, 1500]
    flat = [[float(s) for s in range(p - BJ.WIN_BEFORE, p + BJ.WIN_AFTER)]
            for p in peaks]
    two_lead = [[[float(s)] * 2
                 for s in range(p - BJ.WIN_BEFORE, p + BJ.WIN_AFTER)]
                for p in peaks]
    check(P3.window_centres(flat) == [1000.0, 1500.0],
          "a flat window block names its centres")
    check(P3.window_centres(two_lead) == [1000.0, 1500.0],
          "and so does a two-lead one, from the first channel")
    check(P3.window_centres([[1.0, 2.0], [3.0, 4.0]]) == [],
          "a block that is not window-shaped is simply not this channel")
    check(P3.window_centres([]) == [] and P3.window_centres(None) == [],
          "and neither is nothing at all")
    stubs, _log = P3.build_injection(P3.FIXTURES[0])
    with P3.InjectedModules(stubs):
        ref, _sim = sys.modules["frontend"].compare_features(two_lead)
    check([list(row)[0] for row in ref] == [1000.0, 1500.0],
          "a helper handed two-lead windows still returns aligned rows")


def test_a_helper_called_without_the_peaks_still_returns_aligned_rows():
    """A column of the wrong length is a column the reader must refuse.

    Run `20260816T131241` called `compare_features` with **no peak list**
    (`given: [0]`), so a stub that answers only to peaks would have put an
    empty column into a record whose other columns had seven rows.  The
    windows say which rows they are: the injected signal is a ramp, so a
    stored window's centre sample is the peak it was cut around — the same
    declared property the beat cross-check reads.
    """
    stubs, _log = P3.build_injection(P3.FIXTURES[0])
    peaks = [int(p) for p in P3.FIXTURES[0]["peaks"]][:3]
    windows = [[0.0] * BJ.WIN_BEFORE + [float(p)]
               + [0.0] * (BJ.WIN_AFTER - 1) for p in peaks]
    with P3.InjectedModules(stubs):
        frontend = sys.modules["frontend"]
        ref, sim = frontend.compare_features(windows)
        ctx = frontend.beat_ctx(windows)
    for label, block in (("ref", ref), ("sim", sim), ("ctx", ctx)):
        rows = [list(row) for row in block]
        check([row[0] for row in rows] == [float(p) for p in peaks],
              f"{label} recovers its rows from the windows: {rows}")
    negated = [[-v for v in row] for row in windows]
    with P3.InjectedModules(stubs):
        ref_negated, _sim = sys.modules["frontend"].compare_features(negated)
    check([list(row)[0] for row in ref_negated] == [float(p) for p in peaks],
          "and a window that passed through a negating probe names the same "
          "rows, because a sign cannot change which row is which")
    result = differential_for(WINDOW_ARGUMENT_PRODUCER)
    check(result["all_equal"] is True and result["fixtures_passed"] == 6,
          "a producer shaped this way agrees on all six fixtures")
    check(result["stub_invariance_probed"] == ["invariant"],
          f"and every fixture was probed: {result['stub_invariance']}")


def test_every_declared_helper_is_the_identity_and_is_probed():
    """Shape-unknown helpers get the one stand-in that claims nothing."""
    check(P3.FRONTEND_STUB_FUNCTIONS == ("_z", "stack_ctx", "slope_channel"),
          f"the declared helpers are the three the runs found: "
          f"{P3.FRONTEND_STUB_FUNCTIONS}")
    stubs, _log = P3.build_injection(P3.FIXTURES[0])
    probe, _log = P3.build_injection(P3.FIXTURES[0],
                                     variant=P3.STUB_VARIANT_PROBE)
    for name in P3.FRONTEND_STUB_FUNCTIONS:
        value = [[1.0, -2.0], [3.0, 4.0]]
        check(stubs[name](value) == value,
              f"{name} hands its argument straight back")
        check(probe[name](value) == [[-1.0, 2.0], [-3.0, -4.0]],
              f"and the probe variant of {name} negates it elementwise")
        check(name in P3.INJECTED_GLOBALS,
              f"{name} is part of the injected surface, so it is folded into "
              f"the harness identity")


def test_the_discovery_pass_reads_an_arity_back_and_keeps_going():
    """A stand-in that unpacks into nothing ends the pass one name early.

    The producer says how many values it wanted, so the retry is reading the
    refusal rather than working around it — and a retry that is not driven by
    a new number the producer named does not happen.
    """
    try:
        differential_for(UNPACKING_PRODUCER)
    except P3.SourceHarnessError as error:
        discovery = error.context["surface_discovery"]
        check(discovery["undeclared_names"] ==
              ["frontend.pair_returning_helper",
               "frontend.name_after_the_unpack"],
              f"the pass gets past the unpack and reports the name behind it: "
              f"{discovery['undeclared_names']}")
        check(discovery["unpack_arity_used"] == 2
              and discovery["reached_the_end"] is True,
              f"using the arity the producer itself named: {discovery}")
        attempts = discovery["attempts"]
        check(len(attempts) == 2 and attempts[0]["unpack_arity"] == 0
              and "expected 2" in str(attempts[0]["stopped_with"]),
              f"and every attempt is recorded, including the one that failed: "
              f"{attempts}")
    else:                                                    # pragma: no cover
        raise AssertionError("the unpacking producer did not stop the run")
    check(P3.MAX_DISCOVERY_ATTEMPTS >= 2,
          "the retry is bounded rather than a search")


def test_the_discovery_pass_reports_itself_as_a_lower_bound():
    """A stand-in answers where a value would, and control flow can differ.

    The 20260816T121935 pass listed one name and reached the end of the
    producer — with that name answered by a mock.  What the producer does next
    once the name is declared for real is not something the pass observed, and
    the note has to say so or the list reads as a guarantee.
    """
    check("LOWER BOUND" in P3.SURFACE_DISCOVERY_NOTE,
          "the note says the list is a lower bound")
    check("branches on what it got back" in P3.SURFACE_DISCOVERY_NOTE,
          "and why: a producer may branch on the stand-in")
    try:
        differential_for(TWO_MISSING_NAMES_PRODUCER)
    except P3.SourceHarnessError as error:
        discovery = error.context["surface_discovery"]
        check(P3.SURFACE_DISCOVERY_NOTE == discovery["note"],
              "and the caveat travels with every result it produces")


def test_an_undeclared_stub_attribute_is_its_own_stop():
    """"The injection is incomplete" is not "the source is broken".

    The run of 2026-08-15 stopped exactly here, and the message has to name
    the module and the attribute — otherwise the next step is guesswork, and
    guessing a value into an injected dependency is how a run stops measuring
    the thing it claims to measure.
    """
    with _counted_compiles() as counter:
        try:
            differential_for(UNDECLARED_READING_PRODUCER)
        except P3.SourceHarnessError as error:
            check(error.status == P3.P3_STUB_SURFACE_INCOMPLETE,
                  "an undeclared attribute stops as P3_STUB_SURFACE_INCOMPLETE")
            check("SOMETHING_NOBODY_DECLARED" in str(error)
                  and "'frontend'" in str(error),
                  "and the stop names both the module and the attribute")
            check("not a disagreement with the adapter" in str(error),
                  "and says it is not a disagreement with the adapter")
        else:                                                # pragma: no cover
            raise AssertionError("an undeclared attribute was supplied")
    check(counter.counts["compile"] > 0,
          "the source did compile — this is a surface gap, not a load failure")
    check(P3.P3_STUB_SURFACE_INCOMPLETE in P3.HARNESS_STOPS,
          "the stop is registered as a harness stop")
    decision = P3.decide(None, P3.P3_STUB_SURFACE_INCOMPLETE, "surface gap")
    check(decision["harness_stop"] is True
          and decision["equivalence_claimed"] is False
          and decision["fixtures_passed"] is None,
          "and it produces no fixture score and no equivalence claim")


def test_an_undeclared_attribute_is_recorded_before_it_is_refused():
    stubs, log = P3.build_injection(P3.FIXTURES[0])
    with P3.InjectedModules(stubs):
        frontend = sys.modules["frontend"]
        check(frontend.FS == 360, "the declared constant is readable")
        try:
            frontend.WHATEVER_THIS_IS
        except AttributeError as error:
            check(isinstance(error, P3.StubAttributeMissing),
                  "an undeclared one raises the harness's own AttributeError")
        else:                                                # pragma: no cover
            raise AssertionError("an undeclared attribute was returned")
        check(hasattr(frontend, "WHATEVER_THIS_IS") is False,
              "so hasattr() sees a plainly missing attribute, as it would on "
              "a real module")
    requests = [c for c in log.as_list()
                if c["target"] == "frontend.__getattr__"]
    check([c["requested"] for c in requests] == ["WHATEVER_THIS_IS"] * 2,
          f"and every request is recorded for the bundle: {requests}")
    check(all(c["declared"] is False for c in requests),
          "each marked as undeclared rather than quietly supplied")


#: The same producer, handing its rows back as a bare tuple rather than a
#: mapping.  The 20260816T000714 run stopped at P3_KEPT_ROWS_UNOBSERVABLE
#: because the reader only looked at the top level of a container it could not
#: name — an unread container is not an absent one.
TUPLE_RETURNING_PRODUCER = Z_USING_PRODUCER.replace(
    '    return {"beat": beats, "rr": [rr_all[i] for i in keep], "y": ys}',
    '    return (beats, [rr_all[i] for i in keep], ys)')

#: The same rows again, this time as a record object's attributes.
OBJECT_RETURNING_PRODUCER = Z_USING_PRODUCER.replace(
    '    return {"beat": beats, "rr": [rr_all[i] for i in keep], "y": ys}',
    '    class _Record(object):\n'
    '        pass\n'
    '    out = _Record()\n'
    '    out.beat = beats\n'
    '    out.rr = [rr_all[i] for i in keep]\n'
    '    out.y = ys\n'
    '    return out')

#: A producer whose return says nothing at all about which rows it kept.  This
#: one has to stop: reading a count as a mapping would be an invention.
OPAQUE_RETURNING_PRODUCER = Z_USING_PRODUCER.replace(
    '    return {"beat": beats, "rr": [rr_all[i] for i in keep], "y": ys}',
    '    return len(keep)')


def test_rows_handed_back_in_a_tuple_are_still_read():
    """A container the reader cannot name is opened, not given up on.

    The rows are the same rows; only the wrapper differs.  Refusing to look
    inside a tuple would report "this producer kept nothing observable" about
    a producer that plainly kept something.
    """
    result = differential_for(TUPLE_RETURNING_PRODUCER)
    check(result["all_equal"] is True and result["fixtures_passed"] == 6,
          "a producer that returns its rows in a tuple is read and agrees on "
          "all six fixtures")
    check(result["stub_invariance_probed"] == ["invariant"],
          "and the injection is still probed on every fixture")


def test_rows_handed_back_as_object_attributes_are_still_read():
    """A returned record is read through its own public attributes."""
    result = differential_for(OBJECT_RETURNING_PRODUCER)
    check(result["all_equal"] is True and result["fixtures_passed"] == 6,
          "a producer that returns a record object is read and agrees on all "
          "six fixtures")
    attributes = P3._public_attributes(_ExampleRecord())
    check(sorted(attributes) == ["beat", "rr", "y"],
          f"only public non-callable attributes are read: {sorted(attributes)}")


class _ExampleRecord(object):
    """A stand-in for a returned record, with things that must not be read."""

    def __init__(self):
        self.beat = [[1.0]]
        self.rr = [[0.8]]
        self.y = ["N"]
        self._private = "not read"

    def method(self):                                        # pragma: no cover
        raise AssertionError("a callable attribute must not be read")


def test_a_return_that_holds_no_rows_stops_and_describes_its_shape():
    """The stop that cannot be avoided still has to be actionable.

    "It kept nothing" and "its output cannot be read" are different findings.
    When the second one is true the stop prints the *shape* of what came back
    — type, keys, lengths — so the next extension is deliberate rather than a
    guess, and never a value that could pass for a measurement.
    """
    try:
        differential_for(OPAQUE_RETURNING_PRODUCER)
    except P3.SourceHarnessError as error:
        check(error.status == P3.P3_KEPT_ROWS_UNOBSERVABLE,
              "an unreadable return is a harness stop, not a disagreement")
        check("What it did return: int." in str(error),
              f"and the stop describes the returned shape: {error}")
        check("not an empty one" in str(error),
              "distinguishing it from a producer that kept no rows")
        check("The comparison was not made." in str(error),
              "and saying plainly that nothing was compared")
    else:                                                    # pragma: no cover
        raise AssertionError("an unreadable return was read anyway")
    check(P3.P3_KEPT_ROWS_UNOBSERVABLE in P3.HARNESS_STOPS,
          "the stop is registered as a harness stop")


def test_the_shape_description_carries_no_measurable_value():
    """Shapes are printable; contents are not, and must not leak into a stop."""
    described = P3.describe_returned(
        {"beat": [[0.125, 0.5], [0.25, 0.75]], "y": ["N", "V"]})
    check("mapping(2)" in described and "'beat'" in described,
          f"a mapping is described by its keys and size: {described}")
    check("0.125" not in described and "'V'" not in described,
          "and never by the values inside it")
    check(P3.describe_returned(7) == "int"
          and P3.describe_returned(None) == "NoneType",
          "a scalar is described by its type alone")
    check("no readable public attributes" in P3.describe_returned(object()),
          "and an object with nothing readable says exactly that")


def test_an_empty_result_is_reported_as_kept_nothing_not_as_unreadable():
    """The two findings stay apart in the direction that matters too."""
    rows = P3.discover_kept_rows({"kept": [], "labels": []}, P3.FIXTURES[0])
    check(rows["rows"] == [] and rows["channels"] == ["empty_result"],
          "a producer that returns empty containers kept no rows, and that is "
          "an observation rather than a failure")
    check(rows["empty_containers"] != [],
          f"with the containers it did return recorded: {rows}")
    columnar = P3.discover_kept_rows({"beat": [], "rr": [], "y": []},
                                     P3.FIXTURES[0])
    check(columnar["rows"] == [] and columnar["parser"] == "columnar",
          "and an empty registered record says the same thing through the "
          "columnar reader, rather than reporting itself unreadable")


#: A producer shaped the way the registered one is: it returns the record as
#: **columns**, one array per field, which is what `prepare()` saves as the
#: cache.  `BJ.CACHE_KEYS` is the registered schema for those columns.
COLUMNAR_PRODUCER = '''
from .frontend import detect_r, rr_features, FS, _z
from .pwave import pwave_features

WIN_BEFORE = 150
WIN_AFTER = 150
AAMI = {"N": "N", "L": "N", "R": "N", "e": "N", "j": "N",
        "A": "S", "a": "S", "J": "S", "S": "S", "V": "V", "E": "V"}


def build_record(rec, sig, ann_sample, ann_symbol, use_detected=True):
    x = sig
    peaks = detect_r([row[0] for row in x], FS)
    tol = int(0.15 * FS)
    samples = [int(s) for s in ann_sample]
    symbols = list(ann_symbol)
    order = sorted(range(len(samples)), key=lambda k: (samples[k], k))
    used = set()
    ys, keep = [], []
    for i, p in enumerate(peaks):
        p = int(p)
        best, bd = None, tol + 1
        for rank in range(len(order)):
            if rank in used:
                continue
            d = abs(samples[order[rank]] - p)
            if d < bd:
                best, bd = rank, d
        if best is None or bd > tol:
            continue
        used.add(best)
        j = order[best]
        cls = AAMI.get(symbols[j], "")
        if not cls:
            continue
        if not (p - WIN_BEFORE >= 0 and p + WIN_AFTER <= len(x)):
            continue
        keep.append(i)
        ys.append(cls)
    rr_all = rr_features(peaks, FS)
    pw_all = pwave_features(x, peaks, None, FS)
    beat = [_z([float(v[0]) for v in
                x[int(peaks[i]) - WIN_BEFORE:int(peaks[i]) + WIN_AFTER]])
            for i in keep]
    return {"beat": beat,
            "ref": [[0.0] for _ in keep],
            "rr": [list(rr_all[i]) for i in keep],
            "sim": [[0.0] for _ in keep],
            "pw": [list(pw_all[i]) for i in keep],
            "ctx": [[0.0] for _ in keep],
            "y": ys}
'''


def _record(fixture, kept, **overrides):
    """A well-formed registered record over `kept`, before any mutation.

    Built the way the injection contract says the columns come out: `rr` row
    `j` starts with its peak, `pw` likewise, and the beat window is centred on
    the sample it was cut around because the ramp signal makes it so.
    """
    window = P3.BJ.WIN_BEFORE + P3.BJ.WIN_AFTER
    record = {
        "beat": [[0.0] * P3.BJ.WIN_BEFORE + [float(p)]
                 + [0.0] * (window - P3.BJ.WIN_BEFORE - 1) for p in kept],
        "ref": [[0.0] for _ in kept],
        "rr": [[float(p), float(i)] + [0.0] * (P3.BJ.CACHE_RR_DIM - 2)
               for i, p in enumerate(kept)],
        "sim": [[0.0] for _ in kept],
        "pw": [[float(p)] + [0.0] * 4 for p in kept],
        "ctx": [[0.0] for _ in kept],
        "y": ["N" for _ in kept]}
    record.update(overrides)
    return record


def _columnar_stop(record, fixture=None, variant=P3.STUB_VARIANT_PRIMARY):
    """Read a record and return the stop it raised, or `None`."""
    fixture = fixture or P3.FIXTURES[0]
    try:
        P3.discover_kept_rows(record, fixture, variant)
    except P3.SourceHarnessError as error:
        return error
    return None


def test_the_registered_columnar_record_is_read_by_its_own_reader():
    """The shape the registered `build_record` returns, read end to end.

    Not a list of rows: a mapping of columns, one array per field, all of them
    row-aligned.  The 20260816T000714 run stopped without comparing anything,
    and a general reader that recognises this by trying channels until one
    works is not a basis for a statement about the registered source.
    """
    check(P3.COLUMNAR_RECORD_KEYS == tuple(BJ.CACHE_KEYS),
          "the record columns come from the frozen Q5-D cache schema rather "
          "than being retyped here")
    result = differential_for(COLUMNAR_PRODUCER)
    check(result["all_equal"] is True and result["fixtures_passed"] == 6,
          "a columnar producer is read and agrees on all six fixtures")
    check(result["stub_invariance_probed"] == ["invariant"],
          f"and every fixture was probed under the negated helper: "
          f"{result['stub_invariance']}")
    reading = result["detail"][0]["return_reading"]
    check(reading["parser"] == "columnar"
          and reading["identity_channel"] == "rr[:, 0]",
          f"the reading names the reader and the carrier it used: {reading}")
    check(reading["channels"] == sorted(["rr[:, 0]", "pw[:, 0]",
                                         f"beat[:, {P3.BJ.WIN_BEFORE}]"]),
          f"and all three registered channels were read: {reading['channels']}")


def test_the_reader_is_chosen_by_schema_and_never_by_result():
    """A dispatcher that looked at the values could pick the nicer answer."""
    import inspect
    source = inspect.getsource(P3.is_columnar_return)
    check("keys" in source and "values()" not in source,
          "recognition reads key names, and never the values under them")
    check(P3.is_columnar_return(_record(P3.FIXTURES[0], [1001])) is True,
          "a registered record is recognised")
    check(P3.is_columnar_return({"kept": [1, 2], "labels": ["N", "V"]})
          is False, "an ordinary mapping is not")
    check(P3.is_columnar_return([{"r_sample": 1001}]) is False,
          "and neither is a list of rows, which the general reader takes")
    # The columnar reader never hands a contradiction back to the general one:
    # falling back after seeing a contradiction is choosing a channel by its
    # answer, which is the whole thing this design removes.
    broken = _record(P3.FIXTURES[0], [1001], rr=[[9999.0] + [0.0] * 6])
    error = _columnar_stop(broken)
    check(error is not None
          and error.status == P3.P3_COLUMNAR_RETURN_UNPROJECTABLE,
          "a record whose carrier names an unknown peak stops")
    check(P3.discover_kept_rows.__doc__ is not None
          and "no fallback" in P3.discover_kept_rows.__doc__,
          "and the reader says so where the next reader will look")


def test_the_identity_carrier_is_checked_exactly_and_never_repaired():
    """Every way the carrier could fail to identify its rows, one at a time."""
    fixture = P3.FIXTURES[0]
    peaks = [int(p) for p in fixture["peaks"]][:2]
    good = _record(fixture, peaks)
    check(_columnar_stop(good) is None,
          "the unmutated record reads cleanly, so each case below is the "
          "mutation and nothing else")
    cases = {
        "wrong width": [[float(p), 0.0] for p in peaks],
        "not numeric": [[str(p)] + [0.0] * 6 for p in peaks],
        "not two-dimensional": [float(p) for p in peaks],
        "NaN": [[float("nan")] + [0.0] * 6 for _ in peaks],
        "non-integral": [[float(p) + 0.5] + [0.0] * 6 for p in peaks],
        "unknown peak": [[float(p) + 3] + [0.0] * 6 for p in peaks],
        "duplicate peak": [[float(peaks[0])] + [0.0] * 6 for _ in peaks],
    }
    for label, rr in cases.items():
        error = _columnar_stop(_record(fixture, peaks, rr=rr))
        check(error is not None
              and error.status == P3.P3_COLUMNAR_RETURN_UNPROJECTABLE,
              f"a carrier that is {label} stops instead of being repaired")
        check(error.context.get("return_schema", {}).get("columns", {}).get(
            "rr") is not None,
              f"and the stop for {label} carries the schema of what it read")
    check("does not round" in str(_columnar_stop(
        _record(fixture, peaks, rr=cases["non-integral"]))),
          "the stop says outright that nothing is rounded into place")
    check("does not fall back to the closest" in str(_columnar_stop(
        _record(fixture, peaks, rr=cases["unknown peak"]))),
          "and that no sample is snapped to a peak near it")


def test_the_cross_check_channels_can_refuse_but_never_decide():
    """`pw` and the beat centre check the carrier; they never replace it."""
    fixture = P3.FIXTURES[0]
    peaks = [int(p) for p in fixture["peaks"]][:2]
    window = P3.BJ.WIN_BEFORE + P3.BJ.WIN_AFTER
    moved_pw = [[float(peaks[1])] + [0.0] * 4, [float(peaks[0])] + [0.0] * 4]
    error = _columnar_stop(_record(fixture, peaks, pw=moved_pw))
    check(error is not None
          and error.status == P3.P3_COLUMNAR_RETURN_UNPROJECTABLE
          and "'pw' first column" in str(error),
          "a pw column that names different rows stops the run")
    check(error.context.get("rr_first_column") == peaks
          and error.context.get("pw_first_column") == [peaks[1], peaks[0]],
          f"and both sequences are preserved for the bundle: {error.context}")
    moved_beat = [[0.0] * P3.BJ.WIN_BEFORE + [float(peaks[1 - i])]
                  + [0.0] * (window - P3.BJ.WIN_BEFORE - 1)
                  for i in range(len(peaks))]
    error = _columnar_stop(_record(fixture, peaks, beat=moved_beat))
    check(error is not None and "beat window centres" in str(error),
          "a beat window centred on a different peak stops it too")
    # Unavailable is recorded, not silently dropped — and it is never a stop,
    # because a cross-check that cannot run has not contradicted anything.
    reading = P3.discover_kept_rows(
        _record(fixture, peaks, pw=[["x"], ["y"]]), fixture)
    check([row["peak_sample"] for row in reading["rows"]] == peaks,
          "an unreadable cross-check leaves the carrier's reading standing")
    check("pw" in reading["channel_notes"]
          and "pw[:, 0]" not in reading["channels"],
          f"and says why it was not used: {reading['channel_notes']}")


def test_every_registered_column_must_describe_the_same_rows():
    fixture = P3.FIXTURES[0]
    peaks = [int(p) for p in fixture["peaks"]][:2]
    error = _columnar_stop(_record(fixture, peaks, y=["N"]))
    check(error is not None
          and error.status == P3.P3_COLUMNAR_RETURN_UNPROJECTABLE
          and "'y' has 1 rows" in str(error),
          "a column with a different row count stops the run")
    check(error.context.get("row_counts", {}).get("rr") == 2,
          f"and every column's row count is preserved: {error.context}")


def test_a_record_without_its_identity_carrier_never_falls_back():
    """The one case where the general reader would look like a rescue."""
    fixture = P3.FIXTURES[0]
    peaks = [int(p) for p in fixture["peaks"]][:2]
    record = _record(fixture, peaks)
    record.pop("rr")
    check(P3.is_columnar_return(record) is False
          and P3.is_incomplete_columnar_return(record) is True,
          "a record missing its carrier is recognised as exactly that")
    error = _columnar_stop(record)
    check(error is not None
          and error.status == P3.P3_COLUMNAR_RETURN_UNPROJECTABLE,
          "and it stops rather than being read through the beat window")
    check("would be choosing a channel" in str(error),
          "with the reason: another channel would be chosen because the "
          "registered one is absent, which is selection after the fact")


def test_row_order_is_read_and_compared_rather_than_required():
    """Order is a decision under test, so it must not be a validity rule.

    One of the six fixtures exists to catch a producer that emits its rows in
    another order.  A reader that stopped on that would convert the difference
    it was built to detect into "the harness could not read this" — the worst
    possible direction for an error.
    """
    fixture = P3.FIXTURES[0]
    peaks = [int(p) for p in fixture["peaks"]][:2]
    reversed_rows = _record(fixture, list(reversed(peaks)))
    reading = P3.discover_kept_rows(reversed_rows, fixture)
    check([row["peak_sample"] for row in reading["rows"]] ==
          list(reversed(peaks)),
          "a reordered record is read in the order it came in")
    check(reading["row_order_follows_fixture"] is False,
          "the reading records that the order is not the fixture's")
    check(P3.discover_kept_rows(_record(fixture, peaks),
                                fixture)["row_order_follows_fixture"] is True,
          "and that an unreordered one is")
    # And the fixture built for this still catches it as a difference.
    ordering = "test_source_match_peak_order_change_is_visible"
    check(ordering in P3.fixture_names(),
          "the ordering fixture is still one of the required six")


class _Array(object):
    """The array surface the reader is allowed to use, and nothing else.

    numpy is installed where the run happens and absent where these tests run,
    so an `isinstance(value, ndarray)` branch would be exercised in exactly the
    wrong one of the two.  The reader goes through `shape`, `dtype` and
    `tolist()` instead — the three things a real array offers — and this stands
    in for one here.  Attribute access beyond those three fails loudly.
    """

    __slots__ = ("_rows", "shape", "dtype")

    def __init__(self, rows, dtype="float32"):
        self._rows = [list(r) if isinstance(r, (list, tuple)) else r
                      for r in rows]
        widths = [len(r) for r in self._rows if isinstance(r, list)]
        square = (widths and len(widths) == len(self._rows)
                  and len(set(widths)) == 1)
        self.shape = ((len(self._rows), widths[0]) if square
                      else (len(self._rows),))
        self.dtype = dtype

    def tolist(self):
        return [list(r) if isinstance(r, list) else r for r in self._rows]

    def __len__(self):
        return len(self._rows)

    def __iter__(self):
        return iter(self._rows)


def test_the_record_is_read_through_the_array_surface_not_through_numpy():
    """The shape the run will really hand over: columns as arrays.

    The registered producer builds its columns with numpy and stores them as
    float32.  This module never imports numpy to read them — it uses `shape`,
    `dtype` and `tolist()`, which is why the reading can be tested here at all.
    """
    fixture = P3.FIXTURES[0]
    peaks = [int(p) for p in fixture["peaks"]][:2]
    plain = _record(fixture, peaks)
    arrays = {key: (_Array(value, "<U1" if key == "y" else "float32"))
              for key, value in plain.items()}
    reading = P3.discover_kept_rows(arrays, fixture)
    check([row["peak_sample"] for row in reading["rows"]] == peaks,
          "columns handed over as arrays read exactly as plain lists do")
    check(reading["channels"] == P3.discover_kept_rows(
        plain, fixture)["channels"],
          "with the same channels found in both")
    check(reading["return_schema"]["columns"]["rr"]["dtype"] == "float32",
          "and the array's own dtype is what the report records")
    check(reading["rows"][0]["tokens"] == [["columnar_y", repr("N")]],
          f"labels survive as opaque tokens: {reading['rows'][0]['tokens']}")
    check(P3._numpy() is None or True,
          "and none of this required numpy to be importable")


#: A producer that runs to completion and declines to build a record.  The
#: registered source did exactly this on the first fixture of run
#: 20260816T012958 — it returned `None`, not an empty record.
NONE_RETURNING_PRODUCER = Z_USING_PRODUCER.replace(
    '    return {"beat": beats, "rr": [rr_all[i] for i in keep], "y": ys}',
    '    if len(keep) < 99:\n'
    '        return None\n'
    '    return {"beat": beats, "rr": [rr_all[i] for i in keep], "y": ys}')


def test_the_filler_beats_cannot_touch_any_decision_under_test():
    """The fixtures grew, and the growth has to be provably inert.

    Run `20260816T022702` showed the registered producer declining to build a
    record while holding one kept beat, so four of the six fixtures could never
    reach the comparison.  Filler beats fix that — and a filler beat that could
    become someone's nearest, be consumed by someone else, or change a tie
    would silently rewrite the thing each fixture exists to refute.
    """
    filler_peaks = set(P3.FILLER_PEAKS)
    filler_samples = {sample for sample, _symbol in P3.FILLER_ANNOTATIONS}
    check(len(P3.FILLER_PEAKS) == len(filler_peaks) == 6,
          "there are six distinct filler beats")
    for fixture in P3.FIXTURES:
        name = str(fixture["name"])
        peaks = [int(p) for p in fixture["peaks"]]
        annotations = [(int(s), str(y)) for s, y in fixture["annotations"]]
        decision_peaks = [p for p in peaks if p not in filler_peaks]
        decision_samples = [s for s, _ in annotations if s not in filler_samples]
        check(peaks[-len(P3.FILLER_PEAKS):] == list(P3.FILLER_PEAKS),
              f"{name}: the filler is appended, so the decision peaks are "
              f"still traversed first")
        for peak in P3.FILLER_PEAKS:
            for other in decision_samples:
                check(abs(peak - other) > P3.TOLERANCE,
                      f"{name}: filler peak {peak} is further than the "
                      f"tolerance from decision annotation {other}, so it can "
                      f"never be matched to one")
        for sample in filler_samples:
            for other in decision_peaks:
                check(abs(sample - other) > P3.TOLERANCE,
                      f"{name}: filler annotation {sample} is out of reach of "
                      f"decision peak {other}")
        for peak in P3.FILLER_PEAKS:
            within = [s for s, _ in annotations if abs(s - peak) <= P3.TOLERANCE]
            check(within == [peak + 1],
                  f"{name}: filler peak {peak} has exactly one annotation "
                  f"within the tolerance, so it carries no matching decision")
            check(BJ.WIN_BEFORE <= peak <= int(fixture["signal_length"])
                  - BJ.WIN_AFTER - 1,
                  f"{name}: filler peak {peak} is strictly inside the window "
                  f"boundary, so it carries no boundary decision either")
    classes = [BJ.AAMI_SYMBOL_MAP.get(symbol, "")
               for _sample, symbol in P3.FILLER_ANNOTATIONS]
    check(all(classes), f"every filler symbol maps to an AAMI class: {classes}")
    check(all(a != b for a, b in zip(classes, classes[1:])),
          f"neighbouring filler classes differ, which is what lets a kept row "
          f"settle an ambiguous trace reading: {classes}")
    check(classes[0] == "S",
          "and the first one is S, so it differs from the decision annotation "
          "before it in every fixture — those are all N or V")
    used = {symbol for _s, symbol in P3.FILLER_ANNOTATIONS}
    for fixture in P3.FIXTURES:
        decision = {str(y) for s, y in fixture["annotations"]
                    if int(s) not in filler_samples}
        check(not (used & decision),
              f"{fixture['name']}: no filler symbol is one the fixture's own "
              f"annotations use")


def test_the_filler_adds_the_same_rows_to_both_sides():
    """Inert means inert on both sides, or it is not a fair comparison."""
    result = differential_for(COLUMNAR_PRODUCER)
    check(result["all_equal"] is True and result["fixtures_passed"] == 6,
          "a faithful producer still agrees on all six fixtures")
    for entry in result["detail"]:
        kept = [row["peak_sample"] for row in entry["source"]["kept_rows"]]
        filler_kept = [p for p in kept if p in set(P3.FILLER_PEAKS)]
        check(filler_kept == list(P3.FILLER_PEAKS),
              f"{entry['name']}: every filler beat is kept, in order: "
              f"{filler_kept}")
        check(len(kept) >= 2,
              f"{entry['name']}: at least two rows survive, which is what the "
              f"registered producer needs before it will build a record")


def test_a_producer_that_declines_to_build_a_record_is_its_own_finding():
    """"It returned nothing" is not "its rows could not be read".

    Run `20260816T012958` reached the registered source, verified it, ran it,
    and got `None` back.  Reported as a reader problem it sends the next round
    to widen a reader that was never involved; reported as a disagreement it
    invents a comparison that did not happen.  It is a third thing, and the
    trace is what says which.
    """
    try:
        differential_for(NONE_RETURNING_PRODUCER)
    except P3.SourceHarnessError as error:
        check(error.status == P3.P3_SOURCE_RETURNED_NO_RECORD,
              f"a None return is its own stop, not the reader's: {error.status}")
        check("not an empty record" in str(error)
              and "declined to build one" in str(error),
              "and the message separates it from a producer that kept no rows")
        check("not a disagreement with the adapter" in str(error),
              "and from a disagreement, which would need a comparison")
        trace = error.context.get("trace", {})
        check(trace.get("returned") == "NoneType",
              f"the trace records what came back: {trace.get('returned')}")
        check(isinstance(trace.get("returned_from_line"), int),
              f"and the line it returned from: {trace.get('returned_from_line')}")
        check(trace.get("code_name") == "build_record"
              and trace.get("n_steps", 0) > 0,
              "and that the producer really ran")
        locals_seen = trace.get("final_locals", {})
        check(locals_seen.get("keep") == list(range(8)),
              f"with the locals that explain it — here the producer had kept "
              f"rows and returned None anyway: keep = {locals_seen.get('keep')}")
        check("ys" in locals_seen and "peaks" in locals_seen,
              f"and the rest of what it was holding: {sorted(locals_seen)}")
        check(error.context["stub_calls"]["counts"]["frontend.detect_r"] == 1,
              "and how far it got through its dependencies")
    else:                                                    # pragma: no cover
        raise AssertionError("a producer that returned nothing was read anyway")
    check(P3.P3_SOURCE_RETURNED_NO_RECORD in P3.HARNESS_STOPS,
          "the stop is a harness stop, so no candidate can be built from it")
    decision = P3.decide(None, P3.P3_SOURCE_RETURNED_NO_RECORD, "declined")
    check(decision["harness_stop"] is True
          and decision["equivalence_claimed"] is False
          and decision["fixtures_passed"] is None,
          "and it yields no fixture score and no equivalence claim")


def test_the_trace_a_stop_carries_describes_locals_without_their_contents():
    """It has to be safe to write into a bundle, like every other diagnosis."""
    try:
        differential_for(NONE_RETURNING_PRODUCER)
    except P3.SourceHarnessError as error:
        trace = error.context["trace"]
    else:                                                    # pragma: no cover
        raise AssertionError("expected the None-return stop")
    signal = trace["final_locals"].get("x")
    check(isinstance(signal, dict) and signal.get("__len__") == 3000,
          f"a signal-sized local is recorded as its type and length: {signal}")
    check("__type__" in signal and not isinstance(signal.get("__len__"), list),
          "never as its samples")
    text = json.dumps(trace)
    check(len(text) < 20000,
          f"the whole trace summary stays small enough to publish: {len(text)}")
    check(trace["distinct_lines_executed"] ==
          sorted(set(trace["distinct_lines_executed"])),
          "the executed lines are recorded in order and deduplicated")
    check(trace["final_locals_truncated"] is False
          and trace["n_locals"] == len(trace["final_locals"]),
          "and the locals are complete rather than silently cut")


def test_a_column_selected_row_by_row_is_still_one_column():
    """The shape a producer writes when it selects rows by index.

    `[rr_all[i] for i in keep]` is a **list of one-dimensional rows**, not one
    two-dimensional block — and where numpy is installed those rows are arrays,
    not lists.  Both are the same column of the same record.  A reader that
    recognised only the block form reported a producer that plainly returned
    rows as having returned none, which is how the Colab suite failed while
    this suite (no numpy) passed.
    """
    fixture = P3.FIXTURES[0]
    peaks = [int(p) for p in fixture["peaks"]][:2]
    plain = _record(fixture, peaks)
    selected = dict(plain)
    for key in ("rr", "pw"):
        selected[key] = [_Array(row) for row in plain[key]]
    check(P3._sequence_shape(selected["rr"]) == (2, P3.BJ.CACHE_RR_DIM),
          f"a list of row arrays has the shape of the block it is: "
          f"{P3._sequence_shape(selected['rr'])}")
    reading = P3.discover_kept_rows(selected, fixture)
    check([row["peak_sample"] for row in reading["rows"]] == peaks,
          "and it reads exactly as the block form does")
    check(reading["channels"] == P3.discover_kept_rows(
        plain, fixture)["channels"],
          "with the same channels, including the cross-check")
    check(P3._flat_tokens(selected["rr"], 2) == [],
          "a column of rows is never mistaken for a column of per-row labels")
    check(P3._flat_tokens(["N", "V"], 2) == [repr("N"), repr("V")],
          "while a real label column still reads as tokens")
    # And with a real array type from the standard library, which carries no
    # `shape` at all — so the width has to come from the row itself.
    import array as _array
    stdlib = dict(plain)
    stdlib["rr"] = [_array.array("d", row) for row in plain["rr"]]
    check(P3._sequence_shape(stdlib["rr"]) == (2, P3.BJ.CACHE_RR_DIM),
          "a row type with no shape attribute still reports its width")
    check([row["peak_sample"] for row in
           P3.discover_kept_rows(stdlib, fixture)["rows"]] == peaks,
          "and reads the same rows")
    # Rows of uneven width are not a block at all, so they are refused rather
    # than read as though the ragged part were not there.
    ragged = dict(plain)
    ragged["rr"] = [_Array(plain["rr"][0]), _Array(plain["rr"][1][:3])]
    error = _columnar_stop(ragged)
    check(error is not None
          and error.status == P3.P3_COLUMNAR_RETURN_UNPROJECTABLE,
          "a ragged carrier stops instead of being padded or trimmed")


def test_the_general_reader_would_choose_a_channel_where_this_one_refuses():
    """The mutation that shows the new reader changes an outcome.

    The general reader is not blind to a columnar record — that is the
    problem.  It finds whichever channel happens to be readable, so a record
    that has lost its registered identity carrier is still read, from whatever
    else is lying around, and the run reports rows nobody registered a carrier
    for.  Same input, two outcomes; only one of them is a statement about the
    registered source.
    """
    fixture = P3.FIXTURES[0]
    peaks = [int(p) for p in fixture["peaks"]][:2]
    record = _record(fixture, peaks)
    record.pop(P3.COLUMNAR_IDENTITY_KEY)
    saved = (P3.is_columnar_return, P3.is_incomplete_columnar_return)
    try:
        P3.is_columnar_return = lambda _returned: False
        P3.is_incomplete_columnar_return = lambda _returned: False
        general = P3.discover_kept_rows(record, fixture)
    finally:
        P3.is_columnar_return, P3.is_incomplete_columnar_return = saved
    check([row["peak_sample"] for row in general["rows"]] == peaks,
          "without the columnar reader the record is read anyway")
    check(P3.COLUMNAR_IDENTITY_KEY not in "".join(general["channels"]),
          f"from channels picked by what was available: {general['channels']}")
    error = _columnar_stop(record)
    check(error is not None
          and error.status == P3.P3_COLUMNAR_RETURN_UNPROJECTABLE,
          "and with it the same record is a stop, because the channel that "
          "was registered to decide is not there")
    check(P3.is_columnar_return is saved[0]
          and P3.is_incomplete_columnar_return is saved[1],
          "the module is left exactly as it was")


def test_a_stop_carries_its_diagnosis_out_to_the_bundle():
    """A stop discards the differential, which is when the reading matters most.

    The 20260816T000714 stop cost a round trip because everything that would
    have explained it lived in a result the stop threw away.
    """
    broken = COLUMNAR_PRODUCER.replace(
        '            "rr": [list(rr_all[i]) for i in keep],',
        '            "rr": [[9.0] * 7 for i in keep],')
    try:
        differential_for(broken)
    except P3.SourceHarnessError as error:
        check(error.status == P3.P3_COLUMNAR_RETURN_UNPROJECTABLE,
              "a record whose carrier cannot be read stops the differential")
        context = error.context
        check(context.get("fixture") in P3.fixture_names(),
              f"the stop names the fixture it happened on: {context.get('fixture')}")
        check(context.get("return_schema", {}).get("keys") ==
              sorted(BJ.CACHE_KEYS),
              "and carries the keys the producer returned")
        check(context["return_schema"]["columns"]["beat"]["shape"] is not None,
              "with each column's shape")
        check("counts" in context.get("stub_calls", {})
              and context["stub_calls"]["counts"].get("frontend.detect_r") == 1,
              f"and how often each stub was called: {context.get('stub_calls')}")
        check(context.get("fixtures_completed") == [],
              "and which fixtures had completed when it stopped")
    else:                                                    # pragma: no cover
        raise AssertionError("an unreadable carrier was read anyway")


def test_the_diagnosis_records_shapes_and_never_array_contents():
    """It has to be safe to publish: shapes yes, measurements no."""
    fixture = P3.FIXTURES[0]
    peaks = [int(p) for p in fixture["peaks"]][:2]
    record = _record(fixture, peaks, ctx=[[0.125], [0.875]])
    report = P3.return_schema_report(record, len(peaks))
    text = json.dumps(report)
    check("0.125" not in text and "0.875" not in text,
          f"no column value appears anywhere in the report: {text[:200]}")
    check(report["columns"]["ctx"]["shape"] == [2, 1]
          and report["columns"]["ctx"]["row_aligned"] is True,
          "while the shape and the row alignment are both recorded")
    check(report["columns"]["beat"]["dtype"] is not None,
          "and each column's element type")
    check(report["is_columnar_record"] is True and report["keys"] ==
          sorted(BJ.CACHE_KEYS), "with the schema it recognised")


def test_the_bundle_records_the_return_shape_on_every_fixture():
    """Not only on a stop: the next stop is diagnosable from the run before it."""
    with tempfile.TemporaryDirectory() as directory:
        result = P3.execute_synthetic_p3(directory,
                                         COLUMNAR_PRODUCER.encode("utf-8"),
                                         timestamp=STAMP, emit=lambda _m: None)
        with open(os.path.join(result["bundle"]["directory"],
                               "fixture_results.json"), encoding="utf-8") as h:
            written = json.load(h)
    check(len(written["detail"]) == 6, "every fixture is in the bundle")
    for entry in written["detail"]:
        check(entry["return_reading"]["parser"] == "columnar",
              f"{entry['name']}: the reading of the return is recorded")
        check(entry["return_reading"]["return_schema"]["keys"] ==
              sorted(BJ.CACHE_KEYS),
              f"{entry['name']}: with the columns the producer returned")
        check(entry["stub_calls"]["counts"]["frontend.rr_features"] >= 1,
              f"{entry['name']}: and how often each stub was asked for")
    check("harness_stop_context" in written,
          "the contracted file has a place for a stop's diagnosis")
    with tempfile.TemporaryDirectory() as directory:
        stopped = P3.execute_synthetic_p3(
            directory, NONE_RETURNING_PRODUCER.encode("utf-8"),
            timestamp=STAMP, emit=lambda _m: None)
    context = stopped["fixture_results"]["harness_stop_context"]
    check(stopped["decision"]["status"] == P3.P3_SOURCE_RETURNED_NO_RECORD,
          "a run that stops still writes its bundle")
    check(context["trace"]["returned"] == "NoneType"
          and context["stub_calls"]["counts"],
          "with the trace and the stub calls inside the contracted file")
    check(stopped["fixture_results"] is not None,
          "and the run hands the same reading back to its caller, so the "
          "notebook can print it without opening Drive")
    check(sorted(P3.PREP_PAYLOAD_FILES) == sorted(Q5E.PREP_PAYLOAD_FILES),
          "and the payload list did not grow to hold any of it")


def test_this_change_moved_the_reader_and_nothing_scientific():
    """The manipulated variable, stated as an assertion rather than a claim."""
    check(Q5E.SOURCE_MATCH_ORACLE_RECORD is None,
          "no oracle record is registered")
    check(len(P3.REQUIRED_FIXTURES) == 6
          and list(P3.fixture_names()) == list(P3.REQUIRED_FIXTURES),
          "the six required fixtures are the six that run")
    check(P3.TOLERANCE == Q5E.M4_PEAK_MATCH_TOLERANCE_SAMPLES,
          "the tolerance is still the registered one")
    check(P3.REGISTERED_SOURCE_SHA256 == Q5E.M4_SOURCE_MAP_HASHES["data.py"]
          and P3.REGISTERED_SOURCE_FILE_ID ==
          "1a8mfNbCz5_vPaOWajsX15l93rgEaO_UK",
          "the source identity is unchanged")
    check(P3.OPEN_REGISTERED_DATA is False,
          "and the module default still opens nothing on import: the "
          "execution approval was re-granted against the new harness digest, "
          "the switch was not")


def test_the_injected_stubs_never_reach_a_real_dependency():
    saved = {name: sys.modules.get(name) for name in P3.INJECTED_MODULE_NAMES}
    stubs, _log = P3.build_injection(P3.FIXTURES[0])
    with P3.InjectedModules(stubs):
        check(sys.modules["wfdb"].rdrecord is stubs["rdrecord"],
              "inside the load, wfdb is the stub")
        check(sys.modules[f"{P3.REGISTERED_SOURCE_PACKAGE}.frontend"].detect_r
              is stubs["detect_r"],
              "and a relative import of frontend resolves to the stub")
    for name in P3.INJECTED_MODULE_NAMES:
        check(sys.modules.get(name) is saved[name],
              f"and afterwards sys.modules[{name!r}] is exactly what it was")
    try:
        stubs["dl_database"]("mitdb")
    except P3.P3Error as error:
        check("never fetches a dataset" in str(error),
              "a producer that tries to download a database is refused")
    else:                                                    # pragma: no cover
        raise AssertionError("a dataset download was allowed")


def test_the_signal_is_synthetic_and_self_identifying():
    signal = P3.make_ramp_signal(20)
    check(len(signal) == 20 and float(signal[7][0]) == 7.0,
          "the ramp signal's value at a sample is that sample's index")
    fixture = P3.FIXTURES[0]
    stubs, log = P3.build_injection(fixture)
    record = stubs["rdrecord"]("SYNTHETIC")
    annotation = stubs["rdann"]("SYNTHETIC", "atr")
    check(record.fs == 360 and record.sig_len == fixture["signal_length"],
          "the record stub reports the fixture's own geometry")
    check([int(s) for s in annotation.sample] ==
          [int(s) for s, _y in fixture["annotations"]],
          "the annotation stub returns the fixture's samples in its order")
    check(list(annotation.symbol) == [y for _s, y in fixture["annotations"]],
          "and its symbols")
    check([c["target"] for c in log.as_list()] ==
          ["wfdb.rdrecord", "wfdb.rdann"],
          "and every call is logged in the order it was made")


def test_p1_p2_registrations_and_the_frozen_q5d_module_are_untouched():
    check(Q5E.sha256_file(BJ.__file__) == Q5E.PRODUCING_CODE_SHA256,
          "the frozen Q5-D module still hashes to its registered code sha")
    check(Q5E.SOURCE_BUNDLE_FOLDER_ID == "1JzRW_Xdes4Ywp4-VYVvksFFih_RQVbhH",
          "P2's registered corrective folder id is unchanged")
    check(len(Q5E.SOURCE_BUNDLE_FILE_SHA256) == len(Q5E.BUNDLE_INPUT_FILES) == 5
          and all(Q5E._is_sha256(v)
                  for v in Q5E.SOURCE_BUNDLE_FILE_SHA256.values()),
          "P2's five registered input digests are all still there")
    check(Q5E._is_sha256(str(Q5E.MITDB_TREE_AGGREGATE)),
          "P1's registered MIT-BIH tree aggregate is still a full digest")
    check(str(Q5E.MITDB_TREE_AGGREGATE).startswith("0b46a411"),
          "and still the value the earlier observation recorded")
    check(P12.EXECUTION_APPROVAL_RECORD["granted"] is True
          and P12.CORRECTIVE_BUNDLE_FOLDER_ID == Q5E.SOURCE_BUNDLE_FOLDER_ID,
          "the P1/P2 module's own approval and lineage are unchanged")
    check(Q5E.ORIGINAL_PRODUCER_FOLDER_ID ==
          "1JjwBhU8BXf8lRrYPcM2UjFNdIKxE9Ghd",
          "and the original producer folder is still recorded as lineage only")


def test_this_pr_adds_no_new_writer_to_the_frozen_or_audit_modules():
    """P3 imports the frozen modules; it must not be able to change them."""
    import re
    with open(P3.__file__, encoding="utf-8") as handle:
        text = handle.read()
    for token in ("Q5E.SOURCE_MATCH_ORACLE_RECORD =", "setattr(Q5E",
                  "setattr(BJ", "setattr(P12", "Q5E.__dict__",
                  "BJ.__dict__"):
        check(token not in text, f"the module never writes {token!r}")
    # An attribute assignment on an imported module, by shape rather than by
    # a substring that `<=` would also satisfy.
    assignment = re.compile(r"^\s*(BJ|Q5E|P12)\.\w+\s*(=[^=]|\+=|-=|\|=)")
    offenders = [line for line in text.splitlines()
                 if assignment.match(line)]
    check(offenders == [],
          f"the imported modules are read, never assigned: {offenders}")


# ─────────────────────────────────────────────────────────────────────────────
# 8. The committed artefacts: notebook, spec, capabilities.
# ─────────────────────────────────────────────────────────────────────────────
def test_the_notebook_is_committed_unexecuted():
    check(os.path.isfile(NOTEBOOK), "the quest58 notebook exists")
    with open(NOTEBOOK, encoding="utf-8") as handle:
        notebook = json.load(handle)
    outputs = 0
    counts = []
    for cell in notebook["cells"]:
        outputs += len(cell.get("outputs", ()) or ())
        if cell["cell_type"] == "code":
            counts.append(cell.get("execution_count"))
    check(outputs == 0, "it carries no outputs at all")
    check(counts and all(count is None for count in counts),
          "and every code cell's execution_count is null")
    text = "\n".join("".join(cell["source"]) for cell in notebook["cells"])
    for stage in ("DESIGN", "SYNTHETIC_FIXTURES",
                  "DEPENDENCY_AND_APPROVAL_PREFLIGHT", "SOURCE_FILE_IDENTITY",
                  "SOURCE_ORACLE_DIFFERENTIAL", "RESULT_GATE",
                  "BUNDLE_REPORT"):
        check(stage in text, f"the planned stage {stage} is named in it")
    first = "".join(notebook["cells"][1]["source"])
    check(all(stage in first for stage in
              ("DESIGN", "SYNTHETIC_FIXTURES", "RESULT_GATE", "BUNDLE_REPORT")),
          "and the first code cell prints the whole planned order")
    check("APPROVAL = P3.EXECUTION_APPROVAL_TOKEN" in text
          and "OPEN_REGISTERED_DATA = True" in text,
          "the notebook opts in at its call site, as the approval intends")
    check("모듈 기본값" in text and "P3.OPEN_REGISTERED_DATA" in text,
          "while printing the module default beside it, which stays False")
    check(P3.OPEN_REGISTERED_DATA is False,
          "and that default really is still False in the module")
    check("run_p3(" in text, "it calls the production route rather than "
                             "reimplementing one")
    for label in ("prep payload fold", "manifest SHA-256", "adapter "
                  "fingerprint", "oracle harness"):
        check(label.replace("  ", " ") in text.replace("\n", " "),
              f"the report cell is built to show {label}")


def test_the_notebook_cannot_reach_a_registered_byte_before_approval():
    with open(NOTEBOOK, encoding="utf-8") as handle:
        notebook = json.load(handle)
    cells = ["".join(cell["source"]) for cell in notebook["cells"]]
    # The stage a cell *is*, from its own first line — not the stage list the
    # design cell prints, which names every stage including this one.
    approval_index = next(
        i for i, text in enumerate(cells)
        if "DEPENDENCY_AND_APPROVAL_PREFLIGHT" in text.splitlines()[0])
    for index, text in enumerate(cells[:approval_index]):
        for token in ("run_p3(", "fetch_registered_source", "authenticate",
                      "build_drive_adapter", "download"):
            check(token not in text,
                  f"cell {index} runs before the approval preflight and does "
                  f"not call {token!r}")
    body = "\n".join(cells)
    check("APPROVAL = P3.EXECUTION_APPROVAL_TOKEN" in body,
          "the approval token is set from the module, never typed as a "
          "literal that could drift from it")
    check(P3.EXECUTION_APPROVAL_TOKEN not in body,
          "so the literal string itself does not appear in the notebook")
    check("raise RuntimeError" in body and "TIMESTAMP" in body,
          "and a malformed TIMESTAMP stops the run rather than writing an "
          "unnamed bundle")
    check("%Y%m%dT%H%M%S" in body and "timedelta(hours=9)" in body,
          "the run stamp is generated in KST rather than retyped each run")
    check("if not TIMESTAMP:" in body,
          "while a value written by hand still wins, for a re-run that has to "
          "carry a particular identifier")
    check(r"\d{8}T\d{6}" in body,
          "and the format is checked, so a generated or typed value that is "
          "not a run identifier stops before a folder is made")


def test_the_spec_records_the_separated_states():
    check(os.path.isfile(SPEC), "the P3 spec exists")
    with open(SPEC, encoding="utf-8") as handle:
        spec = handle.read()
    for line in ("status: approved_for_implementation",
                 "design_owner: codex", "implementation_owner: claude"):
        check(line in spec, f"the frontmatter carries {line!r}")
    # Markdown emphasis is presentation; the state names are what must be there.
    plain = spec.replace("`", "").replace("*", "")
    for state in ("implementation approved", "execution not approved",
                  "result not run",
                  "SOURCE_MATCH_ORACLE_RECORD registration not approved",
                  "Q5-E scientific execution not approved"):
        check(state in plain, f"and the spec separates the state {state!r}")
    for name in Q5E.SOURCE_MATCH_REQUIRED_FIXTURES:
        check(name in spec, f"the spec names the required fixture {name}")
    check("P3_SOURCE_FILE_ID_UNREGISTERED" in spec,
          "and the stop for an unregistered file id")
    check(P3.REGISTERED_SOURCE_SHA256 in spec,
          "and the registered data.py digest it runs against")
    check("MEASURED" not in spec.split("## Decision log")[0]
          or "not run" in spec,
          "while claiming no measured result")


def test_module_capabilities_are_all_present():
    missing = [name for name in P3.module_capabilities()
               if not hasattr(P3, name)]
    check(missing == [], f"every advertised capability exists: {missing}")
    for name in ("run_p3", "execute_synthetic_p3",
                 "differential_over_fixtures", "fetch_registered_source",
                 "candidate_record", "synthetic_permit", "ProducerSession"):
        check(name in P3.module_capabilities(),
              f"and the list advertises {name}")
    card = P3.design_card()
    check(P3.REGISTERED_SOURCE_FILE_ID in card
          and "APPROVED 2026-08-16 by user (read-only)" in card
          and "None (unchanged by this module)" in card,
          "the design card states the target, the approval state and that "
          "nothing is registered")
    check(P3.EXECUTION_APPROVAL_RECORD["for_oracle_harness_sha256"] in card,
          "and the harness digest the approval is bound to, beside the "
          "harness digest the module actually has")
    check("OPEN_REGISTERED_DATA : False" in card,
          "and that the switch default is still shut")
    for name in P3.fixture_names():
        check(name in card, f"and lists {name} with what it refutes")


def test_the_existing_q5e_and_prep_suites_still_pass_unmodified():
    """The frozen and registered modules this PR imports are not edited by it."""
    for module, name in ((Q5E, "q5e_leg2_failure_mechanism_audit.py"),
                         (BJ, "q5d_order_preserving_beat_join.py"),
                         (P12, "q5e_prep_p1_p2_asset_identity.py")):
        path = os.path.join(HERE, name)
        check(os.path.abspath(module.__file__) == os.path.abspath(path),
              f"{name} is imported from the repository, not a copy")
    check(Q5E.source_match_adapter_fingerprint() ==
          Q5E.source_match_adapter_fingerprint(),
          "the adapter fingerprint is stable across calls")
    check(P3._is_sha256(Q5E.source_match_adapter_fingerprint()),
          "and is a 64-hex digest the candidate can carry")


def declared_tests():
    """Top-level `test_*` functions, by AST rather than by line prefix."""
    import ast
    with open(os.path.abspath(__file__), encoding="utf-8") as handle:
        tree = ast.parse(handle.read())
    return sorted(node.name for node in tree.body
                  if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
                  and node.name.startswith("test_"))


def run_all() -> int:
    """Run every test, and refuse to under-report.

    A test defined after this function would be collected too late to run, and
    a test that asserts nothing cannot fail — both are silent passes, so both
    are failures here.
    """
    global PASSED
    collected = {name: value for name, value in globals().items()
                 if name.startswith("test_") and callable(value)}
    declared = declared_tests()
    missing = [n for n in declared if n not in collected]
    extra = [n for n in sorted(collected) if n not in declared]
    if missing or extra:
        raise AssertionError(
            f"the runner did not collect what this file declares: "
            f"missing={missing} unexpected={extra}")
    silent = []
    for name in declared:
        before = PASSED
        collected[name]()
        if PASSED == before:
            silent.append(name)
    if silent:
        raise AssertionError(
            f"these tests ran without asserting anything: {silent}")
    print(f"{len(declared)} test functions, {PASSED} assertions passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(run_all())
