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
    check(record["granted_on"] == "2026-08-15" and record["granted_by"] ==
          "user", "and names when it was granted and by whom")
    check("read-only" in str(record["kind"]),
          "the approval is for a read-only run")
    check(any("drive.readonly" in entry for entry in record["approved"]),
          "which reads the registered file under exactly drive.readonly")
    check("Approved (2026-08-15)" in P3.APPROVAL_NOTE
          and "NOT approved by it" in P3.APPROVAL_NOTE,
          "the note states both halves of the boundary")
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
    check(observation["kept_rows"] == [],
          "no row survives the boundary cut in this fixture")
    check(observation["stages"]["matched_pre_aami"] == [0],
          "the state before AAMI selection still shows the match")
    check(observation["stages"]["post_boundary"] == [],
          "and the state after the boundary cut is empty")
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
    saved_values = dict(P3.BINDING_VALUES)
    try:
        P3.BINDING_VALUES["fs"] = 250
        check(P3.oracle_harness_identity()["oracle_harness_sha256"]
              != identity["oracle_harness_sha256"],
              "and so does changing what the producer is called with")
    finally:
        P3.BINDING_VALUES.clear()
        P3.BINDING_VALUES.update(saved_values)
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
                      "pwave.pwave_features"},
          f"a producer can reach only the injected stub surface: {targets}")


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
          "and an empty TIMESTAMP stops the run rather than writing an "
          "unnamed bundle")


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
          and "APPROVED 2026-08-15 by user (read-only)" in card
          and "None (unchanged by this module)" in card,
          "the design card states the target, the approval state and that "
          "nothing is registered")
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
