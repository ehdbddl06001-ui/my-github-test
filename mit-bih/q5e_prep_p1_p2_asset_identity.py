#!/usr/bin/env python3
"""EXP-2026-008 / Q5-E — PREP P1 and P2: registered asset identity.

Two of the three items that currently stop a Q5-E run are asset identities
that have never been frozen:

* **P1** — the MIT-BIH publisher tree's full 64-hex aggregate.  The spec pins
  it only in truncated form (`0b46a411…`), and a truncated digest is not an
  execution contract.
* **P2** — the per-file SHA-256 of the five canonical Q5-D bundle files Q5-E
  reads, established from a **Drive folder id** rather than from a folder that
  merely has the right name.

Which folder P2 reads (2026-08-14)
----------------------------------
The 2026-08-12 run read the original canonical folder and stopped: the bundle
held eleven of the twelve contracted files, because the producer never wrote
`negative_control_null.npz`.  EXP-2026-009 then built a **corrective
candidate** — the eleven original bytes copied unchanged plus the twelfth
reconstructed from the 100 preregistered null shards.

P2 now targets that candidate, `1JzRW_Xdes4Ywp4-VYVvksFFih_RQVbhH`, and
`run_prep()` refuses every other id — including the original, by name and for
a stated reason, because re-reading it would reproduce a stop that is already
recorded.

Pointing P2 at the candidate does **not** register it.  Q5-E's
`SOURCE_BUNDLE_FOLDER_ID` and `SOURCE_BUNDLE_RUN` are imported here and left
exactly as they are; the candidate becomes a canonical input only through a
separate registration PR, after a combined PASS and a Codex result acceptance.

This module implements those two read-only preflights.  It does **not**
register anything: a run produces `registration_candidates.json`, and the
values enter `q5e_leg2_failure_mechanism_audit.py` and the spec only through a
separate result-acceptance PR after Codex reviews the run.

What this file may never do
---------------------------
Run `detect_r()`, aggregate M0-M4, re-run the beat join, open a DS2 per-beat
label or a V10 probability, compute an association or S PR-AUC, train
anything, or modify, move or delete any Drive artifact.  Every entry point
that touches a registered asset is behind an execution token *and* a terminal
guard, and the guard is not removed by the implementation PR.

P1 and P2 are scientifically independent
----------------------------------------
Neither overwrites the other's verdict.  Each keeps its own status and its own
first failing gate, and the combined verdict is `PREP_P1_P2_PASS` only when
both pass.  A failure is never resolved by relaxing a rule.
"""

from __future__ import annotations

import hashlib
import json
import os
from typing import (Any, Callable, Dict, List, Mapping, Optional, Sequence,
                    Tuple)

try:                                                        # pragma: no cover
    import q5d_order_preserving_beat_join as BJ
    import q5e_leg2_failure_mechanism_audit as Q5E
except ImportError:                                         # pragma: no cover
    import sys
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import q5d_order_preserving_beat_join as BJ
    import q5e_leg2_failure_mechanism_audit as Q5E


EXPERIMENT_ID = "EXP-2026-008"
SUBSTAGE = "Q5E_PREP_P1_P2_ASSET_IDENTITY"
RUN_SLUG = "EXP-2026-008_q5e_prep_p1_p2_asset_identity"
MODULE_VERSION = 1
SPEC_PATH = ("experiments/specs/"
             "EXP-2026-008-q5e-leg2-failure-mechanism-audit.md")
CONTRACT_PATH = ("experiments/specs/"
                 "EXP-2026-008-q5e-prep-p1-p2-execution-contract.md")

# ─────────────────────────────────────────────────────────────────────────────
# P2 — registered targets
#
# Two folders are named here and they are **not** interchangeable.
#
# `ORIGINAL_CANONICAL_*` is what Q5-E registers today: the run that produced
# the DS1 gate bundle.  The 2026-08-12 P2 run read it by folder id and stopped
# at `P2_DIRECTORY_CONTRACT_FAILED` with `missing:
# ['negative_control_null.npz']` — judged `P2_PRODUCER_ARTIFACT_OMISSION`, a
# packaging defect in the producer rather than a stale contract.  That folder
# still holds eleven files, it is immutable, and nothing here touches it.
#
# `CORRECTIVE_*` is the twelve-file folder EXP-2026-009 built on 2026-08-13 by
# copying those eleven bytes unchanged and reconstructing the twelfth from the
# 100 preregistered null shards.  It is a **preregistered corrective
# candidate**: a folder P2 is now pointed at so that it can be judged.  It is
# not yet a canonical Q5-E input, and this module does not make it one — the
# constants in `q5e_leg2_failure_mechanism_audit.py` are deliberately left
# exactly as they are.  Only a separate registration PR, after a combined PASS
# and a Codex result acceptance, may move `SOURCE_BUNDLE_FOLDER_ID` and
# `SOURCE_BUNDLE_RUN` across.
# ─────────────────────────────────────────────────────────────────────────────
#: Q5-E's registered constants, imported and **not modified** by this module.
#: Since the 2026-08-14 registration PR these name the corrective bundle.
SOURCE_BUNDLE_RUN = Q5E.SOURCE_BUNDLE_RUN
SOURCE_BUNDLE_FOLDER_ID = Q5E.SOURCE_BUNDLE_FOLDER_ID
#: The **original eleven-file producer folder**, read by the 2026-08-12 run.
#:
#: These used to alias the registration above, because before 2026-08-14 the
#: registration *was* the original folder.  Aliasing them now would be wrong
#: twice over: `run_prep()` refuses `ORIGINAL_CANONICAL_FOLDER_ID` by name, so
#: the alias would make it refuse the folder it targets; and every report would
#: print the same id under both "candidate" and "original", which is exactly
#: the substitution this preflight exists to catch.  They are therefore read
#: from Q5-E's own lineage constants, which is where that folder still lives.
ORIGINAL_CANONICAL_RUN = Q5E.ORIGINAL_PRODUCER_RUN
ORIGINAL_CANONICAL_FOLDER_ID = Q5E.ORIGINAL_PRODUCER_FOLDER_ID
#: `research/ASSETS.md :: run-20260813-q5d-null-corrective`.
CORRECTIVE_BUNDLE_RUN = ("20260813T000000_EXP-2026-009_q5d_null_artifact_"
                         "repair_corrective")
CORRECTIVE_BUNDLE_FOLDER_ID = "1JzRW_Xdes4Ywp4-VYVvksFFih_RQVbhH"
CORRECTIVE_BUNDLE_SPEC = ("experiments/specs/"
                          "EXP-2026-009-q5d-null-artifact-repair.md")
#: The single folder id the production route accepts.  Named separately from
#: both of the above so that changing what P2 targets is one visible edit and
#: not a silent consequence of editing a registration.
P2_TARGET_FOLDER_ID = CORRECTIVE_BUNDLE_FOLDER_ID
P2_TARGET_RUN = CORRECTIVE_BUNDLE_RUN

PRODUCING_CODE_SHA256 = Q5E.PRODUCING_CODE_SHA256
REGISTERED_RULE_FINGERPRINT = Q5E.REGISTERED_RULE_FINGERPRINT
SUPERSEDED_MARKER = Q5E.SUPERSEDED_MARKER
BUNDLE_INPUT_FILES = Q5E.BUNDLE_INPUT_FILES

# ─────────────────────────────────────────────────────────────────────────────
# Approval.  Separate from the Q5-E audit token: approving this read-only
# preflight is not approving the audit, and the two must not be
# interchangeable.
# ─────────────────────────────────────────────────────────────────────────────
EXECUTION_APPROVAL_TOKEN = "q5e-prep-p1-p2-read-only-execution-approved-by-user"
EXECUTION_APPROVAL_FLAG = "--i-have-separate-prep-execution-approval"
#: Default closed.  A stray import or notebook run cannot reach an asset, even
#: now that execution is approved: the notebook opts in explicitly at its call
#: site, so nothing reaches a registered byte by merely importing this module.
OPEN_REGISTERED_DATA = False

#: What was **not** approved.  Identical across both approvals, and written
#: once so the two records cannot drift apart into a boundary that looks like
#: it moved when nobody moved it.
NOT_APPROVED: Tuple[str, ...] = (
    "P3 implementation or execution",
    "running detect_r()",
    "re-running the beat join",
    "re-running the 10,000 x 3 null replicates",
    "M0-M4 aggregation",
    "opening DS2 per-beat labels",
    "opening V10 probabilities",
    "computing association or S PR-AUC",
    "training or retraining any model",
    "moving, deleting or overwriting any Drive file",
    "automatic registration of any observed value",
)

#: The user's separate read-only execution approvals, written down rather than
#: implied by a deleted line.  A guard that opens because someone edited it
#: records no decision; these record who approved what, when, and — just as
#: importantly — what was *not* approved, so the boundary is readable from the
#: code and not only from a spec.
#:
#: There are two entries because there were two approvals, and they are **not**
#: the same approval.  The 2026-08-12 one covered P2 against the original
#: canonical folder; that run happened and stopped.  The 2026-08-14 one covers
#: P2 against the corrective candidate folder — a different target, so
#: re-using the earlier record for it would describe a permission that was
#: never given.  The superseded entry is kept rather than edited: a record that
#: gets rewritten each time is a record of only the latest thing.
PRIOR_EXECUTION_APPROVAL_RECORDS: Tuple[Dict[str, object], ...] = ({
    "granted": True,
    "superseded": True,
    "granted_on": "2026-08-12",
    "granted_by": "user",
    "kind": "read-only execution of EXP-2026-008 Q5-E PREP P1 and P2",
    "p2_target_folder_id": ORIGINAL_CANONICAL_FOLDER_ID,
    "p2_target_run": ORIGINAL_CANONICAL_RUN,
    "outcome": ("run 20260812T123035 completed; P1 PASS, P2 stopped at "
                "P2_DIRECTORY_CONTRACT_FAILED (missing "
                "negative_control_null.npz).  Bundle preserved and accepted "
                "as an authentic stop record."),
    "approved": (
        "P1 byte-identity over the registered MIT-BIH publisher tree",
        "P2 byte-identity over the canonical Q5-D bundle at the registered "
        "folder id",
        "Drive API reads under exactly the drive.readonly scope",
        "writing the P1/P2 result bundle and saving the notebook with its "
        "outputs",
    ),
    "not_approved": NOT_APPROVED,
    "recorded_in": ("experiments/specs/"
                    "EXP-2026-008-q5e-prep-p1-p2-execution-contract.md"),
},)

#: The **current** approval.  This is the one `_terminal_execution_guard()`
#: consults; setting `granted` back to False restores the previous refusal
#: exactly, with no other change anywhere.
EXECUTION_APPROVAL_RECORD: Dict[str, object] = {
    "granted": True,
    "superseded": False,
    "granted_on": "2026-08-14",
    "granted_by": "user",
    "kind": ("read-only re-execution of EXP-2026-008 Q5-E PREP P1 and P2, "
             "with P2 pointed at the EXP-2026-009 corrective candidate"),
    "supersedes": "2026-08-12",
    "p2_target_folder_id": CORRECTIVE_BUNDLE_FOLDER_ID,
    "p2_target_run": CORRECTIVE_BUNDLE_RUN,
    "approved": (
        "P1 byte-identity re-check over the registered MIT-BIH publisher tree",
        "P2 byte-identity over the corrective candidate Q5-D bundle at folder "
        f"id {CORRECTIVE_BUNDLE_FOLDER_ID}",
        "Drive API reads under exactly the drive.readonly scope",
        "writing a NEW versioned P1/P2 result bundle and saving the executed "
        "notebook with its outputs",
    ),
    "not_approved": NOT_APPROVED + (
        "overwriting the 20260812 P2 stop bundle",
        "promoting the corrective folder to a canonical Q5-E input",
    ),
    "recorded_in": ("experiments/specs/"
                    "EXP-2026-008-q5e-prep-p1-p2-execution-contract.md"),
}
APPROVAL_NOTE = (
    "Approved (2026-08-14): read-only re-execution of P1 and P2 — re-checking "
    "the registered MIT-BIH tree, reading the EXP-2026-009 corrective "
    f"candidate bundle at folder id {CORRECTIVE_BUNDLE_FOLDER_ID} under "
    "exactly the drive.readonly scope, writing a NEW versioned result bundle, "
    "and saving the executed notebook with its outputs.  NOT approved: P3, "
    "detect_r(), re-running the beat join or the null replicates, M0-M4 "
    "aggregation, DS2 labels, V10 probabilities, association or S PR-AUC, any "
    "training, moving or deleting any Drive file, overwriting the 20260812 "
    "stop bundle, registering any observed value, or promoting the corrective "
    "folder to a canonical Q5-E input.  Registration remains a separate "
    "result-acceptance PR after Codex review.")

# ─────────────────────────────────────────────────────────────────────────────
# P1 — registered targets
# ─────────────────────────────────────────────────────────────────────────────
#: `research/ASSETS.md :: data-mitdb-raw-100`.  `SHA256SUMS.txt` cannot appear
#: in its own list, so the publisher list covers the other 146 files and this
#: digest covers the list itself.  Together they are 147/147.
MITDB_CHECKSUM_FILE_SHA256 = Q5E.MITDB_CHECKSUM_FILE_SHA256
MITDB_PUBLISHER_LISTED_FILES = Q5E.MITDB_PUBLISHER_LISTED_FILES
#: The truncated aggregate the spec already records.  Used only as a *prefix*
#: check on an observed value; it is never expanded, reconstructed or guessed.
MITDB_REGISTERED_AGGREGATE_PREFIX = "0b46a411"

P1_PASS = "P1_MITDB_IDENTITY_PASS"
P1_REGISTRATION_REQUIRED = "P1_INPUT_IDENTITY_REGISTRATION_REQUIRED"
P1_FILE_SET_MISMATCH = "P1_MITDB_FILE_SET_MISMATCH"
P1_CHECKSUM_FILE_MISMATCH = "P1_MITDB_CHECKSUM_FILE_MISMATCH"
P1_PUBLISHER_MISMATCH = "P1_MITDB_PUBLISHER_CHECKSUM_MISMATCH"
MITDB_IDENTITY_DIVERGED = "MITDB_IDENTITY_DIVERGED"
#: Ordered P1 gates.  The aggregate is computed only after every one of the
#: preceding gates has passed, so a failing tree never yields a number that
#: could be mistaken for a registration candidate.
P1_GATE_ORDER: Tuple[str, ...] = (
    "expected_file_set", "checksum_file_digest", "publisher_checksums",
    "tree_aggregate")

# ─────────────────────────────────────────────────────────────────────────────
# P2 — verdicts and gate order
# ─────────────────────────────────────────────────────────────────────────────
P2_PASS = "P2_SOURCE_BUNDLE_IDENTITY_PASS"
P2_DIGEST_FREEZE_REQUIRED = "P2_SOURCE_BUNDLE_DIGEST_FREEZE_REQUIRED"
P2_FOLDER_ID_BRIDGE_UNRESOLVED = "P2_FOLDER_ID_BRIDGE_UNRESOLVED"
P2_DIRECTORY_CONTRACT_FAILED = "P2_DIRECTORY_CONTRACT_FAILED"
P2_INVENTORY_AMBIGUOUS = "P2_INVENTORY_AMBIGUOUS"
P2_SUPERSEDED_PRESENT = "P2_SUPERSEDED_BUNDLE"
P2_MANIFEST_MISMATCH = "P2_MANIFEST_IDENTITY_MISMATCH"
#: Ordered P2 gates.  The folder id is resolved first: choosing the bundle by
#: folder *name* is exactly the mistake this preflight exists to prevent.
P2_GATE_ORDER: Tuple[str, ...] = (
    "folder_id_inventory", "inventory_unambiguous", "directory_contract",
    "superseded_absent", "canonical_bytes_bridge", "manifest_identity",
    "input_identity")

#: Drive `mimeType` values that make a child ambiguous rather than a plain
#: file.  A shortcut can point anywhere; a folder is not a bundle member.
DRIVE_FOLDER_MIME = "application/vnd.google-apps.folder"
DRIVE_SHORTCUT_MIME = "application/vnd.google-apps.shortcut"

# ─────────────────────────────────────────────────────────────────────────────
# Combined verdicts
# ─────────────────────────────────────────────────────────────────────────────
PREP_PASS = "PREP_P1_P2_PASS"
PREP_MULTIPLE_FAILURES = "MULTIPLE_PREP_FAILURES"
PREP_STATUSES: Tuple[str, ...] = (
    PREP_PASS, PREP_MULTIPLE_FAILURES, P1_REGISTRATION_REQUIRED,
    P1_FILE_SET_MISMATCH, P1_CHECKSUM_FILE_MISMATCH, P1_PUBLISHER_MISMATCH,
    MITDB_IDENTITY_DIVERGED, P2_DIGEST_FREEZE_REQUIRED,
    P2_FOLDER_ID_BRIDGE_UNRESOLVED, P2_DIRECTORY_CONTRACT_FAILED,
    P2_INVENTORY_AMBIGUOUS, P2_SUPERSEDED_PRESENT, P2_MANIFEST_MISMATCH)

# ─────────────────────────────────────────────────────────────────────────────
# Bundle contract
# ─────────────────────────────────────────────────────────────────────────────
#: The payload identity of a **P1/P2** bundle.  Defined here rather than
#: inherited from Q5-E's list: that list belongs to P3 and carries oracle
#: files this preflight has no business writing.  Only the fold algorithm and
#: the canonical-JSON convention are reused.  `manifest.json` is excluded — it
#: records the fold, so including it would be circular by construction.
P1_P2_PREP_PAYLOAD_FILES: Tuple[str, ...] = (
    "config.json", "decision.json", "log.txt",
    "registration_candidates.json", "source_inventory.json", "summary.md")
PREP_MANIFEST_FILE = "manifest.json"
#: Written last, with `O_EXCL`.  Its presence is what makes a directory a
#: bundle; publication is not a rename, so nothing else can say so.  Excluded
#: from the payload fold for the same reason as the manifest: it records the
#: fold, so folding it in would be circular.
COMMIT_MARKER = "COMMITTED.json"

# ─────────────────────────────────────────────────────────────────────────────
# Where a manifest digest came from
#
# `manifest.json` is outside the payload fold, so the only thing that can vouch
# for it is a digest held somewhere else.  *Somewhere else* is the whole point:
# a run comparing the manifest against the digest it computed itself, seconds
# earlier, has checked that its own two lines of code agree — which is worth
# doing, and is not evidence that the file has not been edited since.  So a
# caller does not merely hand over a digest string, it says where the string
# came from, and only a genuinely external origin can support acceptance.
# ─────────────────────────────────────────────────────────────────────────────
#: The run checking its own freshly computed value.  Catches a broken write;
#: proves nothing about later editing, because there is no "later" yet.
ANCHOR_SAME_RUN = "same_run_self_check"
#: The saved output of the notebook's report cell — the primary freeze record.
ANCHOR_SAVED_NOTEBOOK = "saved_notebook_output"
#: The value written into the execution contract's Decision log / registration.
ANCHOR_REGISTERED_RECORD = "registered_record"
#: No digest was supplied at all.
ANCHOR_NONE = "none"
MANIFEST_ANCHOR_SOURCES: Tuple[str, ...] = (
    ANCHOR_SAME_RUN, ANCHOR_SAVED_NOTEBOOK, ANCHOR_REGISTERED_RECORD,
    ANCHOR_NONE)
#: The two origins that are external to the run being verified.  Only these
#: can make a bundle acceptance-eligible.
EXTERNAL_MANIFEST_ANCHORS: Tuple[str, ...] = (
    ANCHOR_SAVED_NOTEBOOK, ANCHOR_REGISTERED_RECORD)


def payload_files(synthetic: bool) -> Tuple[str, ...]:
    """The exact fold target for this kind of run.

    A synthetic run's marker is part of the payload identity, not an extra
    sitting outside it: deleting or editing the marker must break the fold,
    otherwise "no file outside the payload identity" would not be true.
    """
    names = set(P1_P2_PREP_PAYLOAD_FILES)
    if synthetic:
        names.add(SYNTHETIC_MARKER)
    return tuple(sorted(names))


def bundle_files(synthetic: bool) -> Tuple[str, ...]:
    """Exactly what a committed run holds: payload, manifest, commit marker."""
    return tuple(sorted(set(payload_files(synthetic))
                        | {PREP_MANIFEST_FILE, COMMIT_MARKER}))


SYNTHETIC_MARKER = "SYNTHETIC_FIXTURE.json"
SYNTHETIC_NOTE = ("Produced from synthetic fixtures. NOT a Q5-E result and "
                  "NOT an asset identity. Never an ingest candidate.")
#: Keys that must never reach a bundle.  Credentials and local paths are not
#: evidence and do not belong in an artifact that gets shared.
CREDENTIAL_KEYS: Tuple[str, ...] = (
    "token", "access_token", "refresh_token", "client_secret", "client_id",
    "credentials", "api_key", "authorization", "private_key", "password")


class PrepError(RuntimeError):
    """Any refusal from this module."""


class PrepNotApprovedError(PrepError):
    """Reached a registered asset without the separate execution approval."""


def require_execution_approval(approval: Optional[str], what: str) -> None:
    """Permission before capability.  Checked before any read or API call."""
    if approval != EXECUTION_APPROVAL_TOKEN:
        raise PrepNotApprovedError(
            f"refusing to reach {what}: this read-only PREP needs its own "
            f"separate execution approval.  {APPROVAL_NOTE}")


def execution_is_approved(approval: Optional[str]) -> bool:
    return approval == EXECUTION_APPROVAL_TOKEN


def _terminal_execution_guard() -> Dict[str, object]:
    """The single stop a separately approved execution PR opens.

    It sits after every check and before the first registered read, so an
    approved run reaches a complete route and an unapproved one reaches
    nothing.  **This PR opens it** — and opens it by consulting
    :data:`EXECUTION_APPROVAL_RECORD` rather than by deleting the check.

    That difference is the point.  Deleting the line would leave the repository
    with no statement of who approved what: the only evidence would be the
    absence of code, which reads identically whether the approval happened or
    someone simply removed an inconvenience.  Consulting a record keeps the
    decision legible, keeps `granted: False` as an exact one-value revert, and
    keeps this function as the single place the boundary moves.

    Nothing else about the route changed: the switch, the approval token and
    the folder id are still checked *before* this point, and authentication,
    the Drive service and every reader still happen *after* it.
    """
    if not EXECUTION_APPROVAL_RECORD.get("granted"):
        raise PrepError(
            "P1/P2 are implemented but not approved for execution: reading the "
            "registered MIT-BIH tree or calling the Drive API needs a separate "
            f"read-only execution approval.  {APPROVAL_NOTE}")
    return dict(EXECUTION_APPROVAL_RECORD)


def _canonical_json(obj: object) -> str:
    return Q5E._canonical_json(obj)


def _sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _is_sha256(value: object) -> bool:
    return Q5E._is_sha256(value)


def fold_file_triples(files: Sequence[Mapping[str, object]]) -> str:
    """The registered `(name, bytes, sha256)` fold, reused not reinvented.

    Identical to what `BJ.hash_file_set` folds internally and to what
    `Q5E.subset_file_fold` uses; a regression test asserts the agreement on a
    real directory rather than taking it on trust.
    """
    ordered = sorted((dict(f) for f in files), key=lambda f: str(f["name"]))
    return _sha256_bytes(_canonical_json(
        [[f["name"], f["bytes"], f["sha256"]] for f in ordered]
    ).encode("utf-8"))


# ─────────────────────────────────────────────────────────────────────────────
# Filesystem and Drive seams.
#
# Every byte this module reads goes through one of these two interfaces, so a
# synthetic test can exercise the whole route while proving that no real file
# was opened and no real API was called.
# ─────────────────────────────────────────────────────────────────────────────
class LocalTreeReader(object):
    """Reads a mounted directory.  Approval is checked before every read."""

    __slots__ = ("approval",)

    def __init__(self, approval: Optional[str]) -> None:
        self.approval = approval

    def listdir(self, directory: str) -> List[str]:
        require_execution_approval(self.approval, f"listing {directory!r}")
        if not os.path.isdir(directory):
            return []
        return sorted(name for name in os.listdir(directory)
                      if os.path.isfile(os.path.join(directory, name)))

    def stat_and_hash(self, directory: str, name: str) -> Dict[str, object]:
        path = os.path.join(directory, name)
        require_execution_approval(self.approval, f"reading {path!r}")
        digest = hashlib.sha256()
        with open(path, "rb") as handle:
            for chunk in iter(lambda: handle.read(1 << 20), b""):
                digest.update(chunk)
        return {"name": name, "bytes": os.path.getsize(path),
                "sha256": digest.hexdigest()}

    def read_bytes(self, directory: str, name: str,
                   limit: Optional[int] = None) -> bytes:
        """One read, returning the bytes themselves.

        P1 needs the checksum file's digest *and* its contents.  Reading it
        twice would leave a window in which the file changes between the two
        reads, so the caller takes a single snapshot through here and works
        from that.
        """
        path = os.path.join(directory, name)
        require_execution_approval(self.approval, f"reading {path!r}")
        with open(path, "rb") as handle:
            return handle.read() if limit is None else handle.read(limit)

    def read_text(self, directory: str, name: str) -> str:
        path = os.path.join(directory, name)
        require_execution_approval(self.approval, f"reading {path!r}")
        with open(path, encoding="utf-8", errors="replace") as handle:
            return handle.read()


class DriveFolderAdapter(object):
    """The Drive seam.  Production subclasses this; tests inject a fake.

    Only two operations are ever needed, and both are read-only: enumerate a
    folder's direct children by **folder id**, and fetch one file's bytes by
    **file id**.  Nothing here can create, move, trash or modify anything.
    """

    def list_children(self, folder_id: str) -> List[Dict[str, object]]:
        raise NotImplementedError

    def download(self, file_id: str) -> bytes:
        raise NotImplementedError

    def describe(self) -> Dict[str, object]:
        return {"adapter": type(self).__name__, "read_only": True}


class GoogleDriveFolderAdapter(DriveFolderAdapter):     # pragma: no cover
    """Production adapter.  Never constructed by a test, never at import.

    The service is **injected**, never built here.  An earlier draft fell back
    to ``build("drive", "v3")`` when none was supplied, which quietly picks up
    whatever ambient default credential the runtime happens to hold — a
    credential whose scope nobody checked and which may well be able to write.
    That is exactly the thing :func:`audit_credential_scopes` exists to
    prevent, so the fallback is gone: no service means no adapter.
    """

    __slots__ = ("approval", "_service")

    def __init__(self, approval: Optional[str], service=None) -> None:
        require_execution_approval(approval, "the Google Drive API")
        if service is None:
            raise PrepError(
                "refusing to build a Drive adapter without a service: this "
                "adapter never constructs its own client, because a default "
                "client silently adopts an ambient credential whose scope has "
                "not been proven read-only.  Use build_drive_adapter(), which "
                "acquires a credential scoped to "
                f"{DRIVE_READONLY_SCOPE} and proves it before this point.")
        self.approval = approval
        self._service = service

    def _client(self):
        require_execution_approval(self.approval, "the Google Drive API")
        return self._service

    def list_children(self, folder_id: str) -> List[Dict[str, object]]:
        require_execution_approval(self.approval, f"Drive folder {folder_id!r}")
        fields = ("nextPageToken, files(id, name, size, mimeType, "
                  "modifiedTime, sha256Checksum, md5Checksum, trashed, "
                  "shortcutDetails)")
        out: List[Dict[str, object]] = []
        token = None
        while True:
            response = self._client().files().list(
                q=f"'{folder_id}' in parents",
                fields=fields, pageToken=token,
                includeItemsFromAllDrives=True,
                supportsAllDrives=True).execute()
            out.extend(response.get("files", []))
            token = response.get("nextPageToken")
            if not token:
                break
        return out

    def download(self, file_id: str) -> bytes:
        require_execution_approval(self.approval, f"Drive file {file_id!r}")
        return self._client().files().get_media(
            fileId=file_id, supportsAllDrives=True).execute()


#: Packages an approved run needs.  Named and reported rather than installed:
#: a silent `pip install latest` would change the runtime under a preflight
#: whose whole purpose is to pin identity.
RUNTIME_DEPENDENCIES: Dict[str, str] = {
    "google.colab": "Colab read-only Drive authentication",
    "googleapiclient": "Drive v3 client (google-api-python-client)",
    "google.auth": "credential objects and scope inspection",
}
#: Distributions whose versions are pinned into the result for provenance.
RUNTIME_DISTRIBUTIONS: Tuple[str, ...] = (
    "google-auth", "google-api-python-client", "google-colab")
#: The only scope this preflight may hold.  Declared *and* requested *and*
#: verified — a constant nobody passes to an API call proves nothing.
DRIVE_READONLY_SCOPE = "https://www.googleapis.com/auth/drive.readonly"
READONLY_SCOPE_UNPROVEN = "P2_READONLY_SCOPE_UNPROVEN"


def check_runtime_dependencies() -> Dict[str, object]:
    """Report what an approved run needs.  Never installs anything."""
    missing = []
    for name in sorted(RUNTIME_DEPENDENCIES):
        try:
            __import__(name)
        except ImportError:
            missing.append(name)
    return {"required": sorted(RUNTIME_DEPENDENCIES), "missing": missing,
            "ok": not missing,
            "note": ("install these deliberately and pin them; this preflight "
                     "never installs a package for you, because a silent "
                     "upgrade would change the runtime under an identity "
                     "check")}


def runtime_identity() -> Dict[str, object]:
    """The environment this run actually happened in.

    Provenance, not behaviour: the digest algorithm does not change with the
    interpreter, but "which environment produced this identity" has to be
    answerable later.  A version that cannot be determined is reported as
    `unavailable` rather than guessed.
    """
    import platform                                       # noqa: PLC0415
    versions: Dict[str, str] = {}
    for dist in RUNTIME_DISTRIBUTIONS:
        try:
            from importlib import metadata               # noqa: PLC0415
            versions[dist] = metadata.version(dist)
        except Exception:                    # noqa: BLE001 - absence is data
            versions[dist] = "unavailable"
    return {
        "python_version": platform.python_version(),
        "platform": platform.platform(),
        "distributions": versions,
        "requested_drive_scope": DRIVE_READONLY_SCOPE,
        "prep_module_sha256": Q5E.sha256_file(os.path.abspath(__file__)),
        "q5e_module_sha256": Q5E.sha256_file(os.path.abspath(Q5E.__file__)),
        "frozen_q5d_module_sha256": Q5E.sha256_file(
            os.path.abspath(BJ.__file__)),
        "note": ("no package was installed by this run; an unavailable "
                 "version is reported as such and never inferred"),
    }


def audit_credential_scopes(credential) -> Dict[str, object]:
    """Prove the credential is read-only, or refuse to claim that it is.

    Having no write method on the adapter shows the *adapter* cannot write.
    It says nothing about the credential, which is what actually bounds what
    the API will do.  So the scopes are inspected: exactly the read-only scope
    proves it; a broader scope does not, even though it "includes" what we
    need; and scopes that cannot be observed at all prove nothing either.
    """
    scopes = getattr(credential, "scopes", None)
    observed = sorted(str(s) for s in scopes) if scopes else []
    exact = observed == [DRIVE_READONLY_SCOPE]
    if not observed:
        reason = ("the credential exposes no scopes, so read-only cannot be "
                  "proven; it is not assumed")
    elif not exact:
        reason = ("the credential carries scopes beyond the read-only one; a "
                  "broader credential is not accepted merely because it "
                  "includes what is needed")
    else:
        reason = None
    return {
        "requested_scopes": [DRIVE_READONLY_SCOPE],
        "observed_scopes": observed,
        "exact_readonly_scope_proven": exact,
        "credential_type": type(credential).__name__,
        "service_api": "drive", "service_version": "v3",
        "no_write_adapter_methods": True,
        "reason": reason,
        # The credential object itself is never recorded — only these facts.
        "credential_recorded": False,
    }


def authenticate_drive_readonly(approval: Optional[str],
                                credential_provider=None,
                                service_factory=None
                                ) -> Tuple[object, Dict[str, object]]:
    """Acquire a read-only credential and build the Drive v3 service from it.

    Returns `(service, auth_audit)`.  Approval is checked before either step,
    so an unapproved run performs **zero** authentication calls — not a failed
    one, none at all.  Both seams are injectable so the path is testable
    without a real credential; production passes neither.

    If the credential cannot be shown to hold exactly the read-only scope, this
    raises rather than proceeding.  Calling a broader credential "read-only"
    because it happens to include the scope we want would be a claim the code
    cannot support.
    """
    require_execution_approval(approval, "Google Drive authentication")
    report = check_runtime_dependencies()
    if credential_provider is None and report["missing"]:
        raise PrepError(
            f"refusing to authenticate: {report['missing']} are not "
            f"importable.  {report['note']}")
    if credential_provider is None:                      # pragma: no cover
        credential_provider = _colab_readonly_credential
    credential = credential_provider()
    audit = audit_credential_scopes(credential)
    if not audit["exact_readonly_scope_proven"]:
        raise PrepError(
            f"{READONLY_SCOPE_UNPROVEN}: {audit['reason']}.  observed="
            f"{audit['observed_scopes']}.  This preflight does not run under a "
            f"credential whose read-only bound it cannot demonstrate.")
    if service_factory is None:                          # pragma: no cover
        from googleapiclient.discovery import build      # noqa: PLC0415

        def service_factory(credentials):
            return build("drive", "v3", credentials=credentials)
    # The credential is passed explicitly; the client never picks up an
    # ambient default whose scope nobody checked.
    return service_factory(credential), audit


def _colab_readonly_credential():                        # pragma: no cover
    """Colab auth, down-scoped to read-only where the platform allows it.

    Colab's `authenticate_user()` mints a broad user credential.  Where the
    credential supports `with_scopes`, it is narrowed to the read-only scope
    here; where it does not, `audit_credential_scopes` will refuse rather than
    let a broad credential be described as read-only.
    """
    from google.colab import auth                        # noqa: PLC0415
    auth.authenticate_user()
    import google.auth                                   # noqa: PLC0415
    credential, _project = google.auth.default(
        scopes=[DRIVE_READONLY_SCOPE])
    if hasattr(credential, "with_scopes") and \
            getattr(credential, "requires_scopes", False):
        credential = credential.with_scopes([DRIVE_READONLY_SCOPE])
    return credential


def build_drive_adapter(approval: Optional[str], credential_provider=None,
                        service_factory=None
                        ) -> Tuple["GoogleDriveFolderAdapter",
                                   Dict[str, object]]:
    """Authenticate, prove the scope, then hand the service to the adapter.

    This is the whole production auth path, complete here.  The execution
    approval PR removes the terminal guard and changes the notebook switches;
    it does not write authentication logic for the first time.
    """
    service, audit = authenticate_drive_readonly(
        approval, credential_provider=credential_provider,
        service_factory=service_factory)
    return GoogleDriveFolderAdapter(approval, service=service), audit


def normalise_child(child: Mapping[str, object]) -> Dict[str, object]:
    """One inventory row, with credentials and local paths left out.

    Drive returns more than this; only the identity-bearing fields are kept,
    so a bundle cannot accidentally carry an access token or a mount path.
    """
    size = child.get("size")
    return {
        "file_id": str(child.get("id") or ""),
        "name": str(child.get("name") or ""),
        "bytes": int(size) if size not in (None, "") else None,
        "mime_type": str(child.get("mimeType") or ""),
        "modified_time": str(child.get("modifiedTime") or ""),
        "provider_sha256": str(child.get("sha256Checksum") or "") or None,
        "provider_md5": str(child.get("md5Checksum") or "") or None,
        "trashed": bool(child.get("trashed")),
        "is_shortcut": (str(child.get("mimeType") or "") == DRIVE_SHORTCUT_MIME
                        or bool(child.get("shortcutDetails"))),
        "is_folder": str(child.get("mimeType") or "") == DRIVE_FOLDER_MIME,
    }


def assert_no_credentials(payload: object, where: str = "bundle") -> None:
    """Refuse to write a bundle file that carries a credential-bearing field.

    Checked on **keys**, walking the structure, rather than by scanning the
    serialised text.  The text scan could not tell a field from a value, and
    that is not a hypothetical: the auth audit records `credential_type`, whose
    value in Colab is the class name `Credentials`, and the scan read that as a
    `"credentials"` field and refused to write a run that had already completed
    both gates.  A guard that fires on the word rather than the thing costs a
    real run and teaches people to route around it.

    What it is for is unchanged — a field named `access_token` or `password`
    must never reach a bundle, at any depth — and that is now checked exactly,
    so `credential_type` is fine and `credentials` is not.
    """
    banned = {k.lower() for k in CREDENTIAL_KEYS}

    def walk(node: object, path: str) -> None:
        if isinstance(node, Mapping):
            for key, value in node.items():
                name = str(key)
                where_key = f"{path}.{name}" if path else name
                if name.lower() in banned:
                    raise PrepError(
                        f"refusing to write {where}: it carries a {name!r} "
                        f"field at {where_key!r}.  Credentials are not "
                        f"evidence and never enter a bundle.")
                walk(value, where_key)
        elif isinstance(node, (list, tuple)):
            for index, value in enumerate(node):
                walk(value, f"{path}[{index}]")

    walk(payload, "")


# ─────────────────────────────────────────────────────────────────────────────
# The publisher checksum list, parsed from a byte snapshot
#
# `BJ.parse_sha256sums` takes a *path* and opens it.  P1 has to verify the
# checksum file's own digest before trusting its contents, so using the frozen
# function for the second step would mean opening the same registered path
# twice — and a file that changes between those two reads would be verified in
# one state and parsed in another.  The parse is therefore done here, from the
# same immutable bytes the digest was taken over.  The frozen module is not
# modified; the conventions below are held to `BJ.parse_sha256sums` by
# differential equivalence tests over the same inputs.
# ─────────────────────────────────────────────────────────────────────────────
def parse_sha256sums_text(text: str) -> Dict[str, str]:
    """`BJ.parse_sha256sums`, reading a string instead of a path.

    Same conventions, deliberately line for line: strip, skip blank and `#`
    lines, split on the first run of whitespace, drop a leading `*` (binary
    marker) and a leading `./`, keep the listed path rather than collapsing it
    to a basename, accept only 64-character digests, and lowercase them.
    """
    out: Dict[str, str] = {}
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split(None, 1)
        if len(parts) != 2:
            continue
        digest, name = parts[0].strip(), parts[1].strip()
        name = name.lstrip("*")
        if name.startswith("./"):
            name = name[2:]
        if len(digest) == 64:
            out[name] = digest.lower()
    return out


def _second_read_detail(reader: "LocalTreeReader", directory: str, name: str,
                        authoritative_sha256: str) -> Dict[str, object]:
    """Cheap explanations for a digest mismatch, from a **second** read.

    The authoritative observation of a file is the `(name, bytes, sha256)`
    taken by the single read in P1's gate 3.  Explaining *why* a digest
    differs needs the bytes themselves, and re-reading is a different moment:
    on a live tree the file may have changed in between, so anything derived
    from the second read describes a state the gate never judged.

    So it is reported under its own key, never merged into the observation,
    and the content-derived fields appear **only** when the second read hashes
    to the same value as the first.  When it does not, that instability is
    itself the finding, and no line counts or excerpts are offered — they would
    describe bytes that were never the ones measured.
    """
    out: Dict[str, object] = {
        "why": ("a second read taken to explain the mismatch; the "
                "authoritative observation is the single read in gate 3 and "
                "is not affected by anything here"),
        "authoritative": False,
    }
    try:
        body = reader.read_bytes(directory, name)
    except OSError as error:                              # pragma: no cover
        out["error"] = str(error)
        return out
    second = _sha256_bytes(body)
    out["sha256"] = second
    out["stable"] = second == authoritative_sha256
    if not out["stable"]:
        out["note"] = ("the file changed between the authoritative read and "
                       "this one; no content-derived detail is reported, "
                       "because it would describe bytes the gate never judged")
        return out
    out.update({
        "bytes_read": len(body),
        "starts_with_bom": body.startswith(b"\xef\xbb\xbf"),
        "has_crlf": b"\r\n" in body,
        "ends_with_newline": body.endswith(b"\n"),
    })
    if len(body) > 8192:
        return out
    try:
        text = body.decode("utf-8")
    except UnicodeDecodeError:
        out["binary"] = True
        return out
    lines = [ln for ln in text.splitlines() if ln.strip()]
    out["non_empty_lines"] = len(lines)
    out["first_lines"] = lines[:5]
    out["last_lines"] = lines[-5:]
    out["sha256_without_trailing_newlines"] = _sha256_bytes(
        text.rstrip("\n").encode("utf-8"))
    return out


def compare_against_publisher_list(files: Sequence[Mapping[str, object]],
                                   checksum_text: str,
                                   reader: "LocalTreeReader",
                                   directory: str) -> Dict[str, object]:
    """`BJ.verify_against_publisher_checksums` over a snapshot, not a path.

    Same comparison and the same reported fields, with two differences that
    matter here: the publisher list comes from bytes already verified rather
    than from a fresh `open()`, and the mismatch detail is read back through
    the approval-checked reader instead of by opening the registered path
    directly.
    """
    published = parse_sha256sums_text(checksum_text)
    problems: List[str] = []
    checked = matched = 0
    mismatched: List[Dict[str, object]] = []
    unlisted: List[str] = []
    for entry in files:
        name = str(entry["name"])
        if name == BJ.MITDB_CHECKSUM_FILE:
            continue                    # a checksum file cannot list itself
        want = published.get(name)      # exact listed key, never a basename
        if want is None:
            unlisted.append(name)
            continue
        checked += 1
        observed = str(entry["sha256"]).lower()
        if observed == want:
            matched += 1
            continue
        problems.append(f"{name}: sha256 differs from the publisher list")
        # Authoritative: straight from the single read this gate already took.
        detail: Dict[str, object] = {
            "name": name, "published_sha256": want,
            "observed_sha256": observed, "bytes": entry.get("bytes"),
            "read_by_the_join": BJ._is_read_by_the_join(name),
            "observation_from_single_read": True,
            # Kept strictly beside the observation, never merged into it.
            "second_read_non_authoritative": _second_read_detail(
                reader, directory, name, observed),
        }
        mismatched.append(detail)
    considered = sum(1 for e in files
                     if str(e["name"]) != BJ.MITDB_CHECKSUM_FILE)
    if considered and not checked:
        problems.append(
            f"the publisher list has {len(published)} entries but none of the "
            f"{considered} files in {directory} matched a top-level name; "
            f"nothing was actually verified")
    return {"available": True, "ok": not problems, "problems": problems,
            "checked": checked, "matched": matched, "considered": considered,
            "mismatched": mismatched, "unlisted": sorted(unlisted),
            "published_entries": len(published),
            "read_by_the_join": sorted(
                n for n in (m["name"] for m in mismatched)
                if BJ._is_read_by_the_join(str(n)))}


# ─────────────────────────────────────────────────────────────────────────────
# P1 — MIT-BIH publisher tree identity
# ─────────────────────────────────────────────────────────────────────────────
def run_p1(mitdb_dir: str, approval: Optional[str],
           reader: Optional[LocalTreeReader] = None) -> Dict[str, object]:
    """P1, in the registered order, stopping at the first failing gate.

    The **I/O** follows the gate order, not just the report.  Only
    `SHA256SUMS.txt` is read for gate 2; the other 146 files are not touched
    until that gate passes, and the aggregate is folded only after the
    publisher list has passed too.  A tree that fails an early gate therefore
    never yields per-file digests or an aggregate that could be mistaken for a
    registration candidate.
    """
    reader = reader or LocalTreeReader(approval)
    expected = list(BJ.mitdb_expected_files())
    gates: List[Dict[str, object]] = []

    def stop(reason: str, **extra) -> Dict[str, object]:
        # `per_file` empty means "not measured yet", not "measured and hidden".
        # Gates that stop before anything is hashed leave it empty; gates that
        # stop after the tree was hashed pass the observations back in.
        out = {"prep": "P1", "ok": False, "status": reason,
               "first_failure": reason, "gates": gates,
               "gate_order": list(P1_GATE_ORDER),
               "tree_aggregate": None, "per_file": [],
               "gate_passed": False, "eligible_for_registration": False,
               "observation_only": False, "blocked_by": reason,
               "seals": _p1_seals()}
        out.update(extra)
        return out

    # ---- gate 1: the exact expected file set ------------------------------
    present = reader.listdir(mitdb_dir)
    missing = [n for n in expected if n not in present]
    unexpected = [n for n in present if n not in expected]
    gates.append({"gate": "expected_file_set",
                  "ok": not missing and not unexpected,
                  "n_expected": len(expected), "n_observed": len(present),
                  "missing": missing, "unexpected": unexpected})
    if missing or unexpected:
        return stop(P1_FILE_SET_MISMATCH)

    # ---- gate 2: the checksum file's own digest, reading ONLY that file ---
    # One read.  The digest below and the publisher list parsed at gate 3 come
    # from the *same* bytes, so there is no window in which the file could be
    # replaced between "this is the registered list" and "here is what the
    # list says".  Verifying one state and then parsing another would make the
    # verification decorative.
    checksum_blob = reader.read_bytes(mitdb_dir, BJ.MITDB_CHECKSUM_FILE)
    checksum_entry = {"name": BJ.MITDB_CHECKSUM_FILE,
                      "bytes": len(checksum_blob),
                      "sha256": _sha256_bytes(checksum_blob)}
    observed_checksum = str(checksum_entry["sha256"])
    checksum_ok = observed_checksum == MITDB_CHECKSUM_FILE_SHA256
    gates.append({"gate": "checksum_file_digest", "ok": checksum_ok,
                  "file": BJ.MITDB_CHECKSUM_FILE,
                  "observed": observed_checksum,
                  "registered": MITDB_CHECKSUM_FILE_SHA256,
                  "files_read_so_far": 1,
                  "reads_of_checksum_file": 1,
                  "snapshot_note": ("the digest and the parsed list come from "
                                    "one immutable read of this file")})
    if not checksum_ok:
        # Nothing else is read.  A list that is not the registered list
        # verifies nothing, so hashing the other 146 files would be work done
        # in support of a conclusion that cannot be reached.
        return stop(P1_CHECKSUM_FILE_MISMATCH)

    # ---- gate 3: the publisher list over the other 146 files --------------
    others = [reader.stat_and_hash(mitdb_dir, name) for name in expected
              if name != BJ.MITDB_CHECKSUM_FILE]
    files = sorted([checksum_entry] + others, key=lambda f: str(f["name"]))
    published = compare_against_publisher_list(
        files, checksum_blob.decode("utf-8", "replace"), reader, mitdb_dir)
    checked = int(published.get("checked") or 0)
    matched = int(published.get("matched") or 0)
    mismatched = list(published.get("mismatched") or ())
    unlisted = list(published.get("unlisted") or ())
    publisher_ok = bool(
        published.get("available") and not published.get("problems")
        and checked == MITDB_PUBLISHER_LISTED_FILES
        and matched == MITDB_PUBLISHER_LISTED_FILES
        and not mismatched and not unlisted)
    gates.append({"gate": "publisher_checksums", "ok": publisher_ok,
                  "available": bool(published.get("available")),
                  "checked": checked, "matched": matched,
                  "expected_checked": MITDB_PUBLISHER_LISTED_FILES,
                  "n_mismatched": len(mismatched),
                  "n_unlisted": len(unlisted),
                  "mismatched": mismatched, "unlisted": unlisted,
                  "published_entries": published.get("published_entries"),
                  "problems": list(published.get("problems", ()))})
    if not publisher_ok:
        # The 147 per-file digests were genuinely computed before this gate
        # could be decided, and they are the whole diagnostic value of a
        # failing tree — which files differ, and by how much.  Blanking them
        # would discard measured evidence.  What is withheld is the
        # *aggregate*, because folding an unverified tree produces a number
        # that looks exactly like a registration candidate.
        return stop(P1_PUBLISHER_MISMATCH,
                    per_file=files, tree_aggregate=None,
                    publisher=published,
                    observation_only=True,
                    observation_note=(
                        "per-file observations from a FAILED gate: they "
                        "describe what was measured and are not a "
                        "registration candidate.  No aggregate was folded."))

    # ---- gate 4: the full 147-file aggregate ------------------------------
    aggregate = fold_file_triples(files)
    prefix_ok = aggregate.startswith(MITDB_REGISTERED_AGGREGATE_PREFIX)
    gates.append({"gate": "tree_aggregate", "ok": prefix_ok,
                  "aggregate": aggregate,
                  "registered_prefix": MITDB_REGISTERED_AGGREGATE_PREFIX,
                  "prefix_matches": prefix_ok})
    if not prefix_ok:
        # The observed value is kept as a *diagnostic observation* so the
        # divergence can be investigated.  It is explicitly not a registration
        # candidate: this gate did not pass.
        return stop(MITDB_IDENTITY_DIVERGED,
                    tree_aggregate=aggregate, per_file=files,
                    observation_only=True,
                    observation_note=(
                        "diagnostic observation from a FAILED gate; not a "
                        "registration candidate"))

    return {
        "prep": "P1", "ok": True, "status": P1_PASS, "first_failure": None,
        "gates": gates, "gate_order": list(P1_GATE_ORDER),
        "n_expected_files": len(expected), "n_observed_files": len(present),
        "missing": [], "unexpected": [],
        "checksum_file": {"name": BJ.MITDB_CHECKSUM_FILE,
                          "observed": observed_checksum,
                          "registered": MITDB_CHECKSUM_FILE_SHA256},
        "publisher": {"checked": checked, "matched": matched,
                      "mismatch": len(mismatched), "unlisted": len(unlisted)},
        "published_tree_integrity": {
            "publisher_listed": MITDB_PUBLISHER_LISTED_FILES,
            "checksum_file_self": 1,
            "total": MITDB_PUBLISHER_LISTED_FILES + 1,
            "note": ("147/147 is 146 publisher-listed files plus the "
                     "separately registered digest of the list itself; a "
                     "checksum file cannot verify itself")},
        "tree_aggregate": aggregate,
        "registered_prefix_matches": True,
        "per_file": files,
        "gate_passed": True, "observation_only": False, "blocked_by": None,
        "seals": _p1_seals(),
    }


def _p1_seals() -> Dict[str, bool]:
    return {"detector_executed": False, "m0_m4_aggregated": False,
            "beat_join_executed": False, "model_scored": False,
            "probability_opened": False, "labels_opened": False,
            "training_performed": False, "bytes_hashed_only": True}


# ─────────────────────────────────────────────────────────────────────────────
# P2 — Q5-D bundle identity, from a folder id
# ─────────────────────────────────────────────────────────────────────────────
def _folder_identity(folder_id: str) -> Dict[str, object]:
    """Which folder was read, reported so it cannot be confused with another.

    Three ids are in play — the one actually queried, the corrective candidate
    P2 is pointed at, and the original canonical folder Q5-E still registers —
    and they are reported under **separate keys**.  A single `folder_id` field
    next to the word "registered" was exactly readable as any of them, and the
    one substitution this preflight exists to catch is the one where a reader
    believes a result describes a folder it does not.
    """
    return {
        "folder_id": folder_id,
        "candidate_folder_id": CORRECTIVE_BUNDLE_FOLDER_ID,
        "candidate_run": CORRECTIVE_BUNDLE_RUN,
        "candidate_spec": CORRECTIVE_BUNDLE_SPEC,
        "original_canonical_folder_id": ORIGINAL_CANONICAL_FOLDER_ID,
        "original_canonical_run": ORIGINAL_CANONICAL_RUN,
        "target_is_corrective_candidate":
            folder_id == CORRECTIVE_BUNDLE_FOLDER_ID,
        "target_is_original_canonical":
            folder_id == ORIGINAL_CANONICAL_FOLDER_ID,
        # Derived, never asserted.  Before 2026-08-14 this was a hard `False`
        # and saying so was the whole point; after the registration PR a hard
        # `False` would be a false statement, and a report that keeps insisting
        # a folder is unregistered after it was registered is worse than one
        # that never claimed anything.  So it reads Q5-E's registration.
        "candidate_is_registered_as_canonical":
            CORRECTIVE_BUNDLE_FOLDER_ID == Q5E.SOURCE_BUNDLE_FOLDER_ID,
        "note": ("the corrective folder was a preregistered candidate P2 "
                 "judged; it became the canonical Q5-E input through the "
                 "separate 2026-08-14 registration PR, after the combined "
                 "PASS and the Codex result acceptance"),
    }


def run_p2(folder_id: str, adapter: DriveFolderAdapter,
           approval: Optional[str], mount_dir: Optional[str] = None,
           reader: Optional[LocalTreeReader] = None) -> Dict[str, object]:
    """P2, in the registered order, stopping at the first failing gate.

    The bundle is identified by **folder id**.  A folder that merely has the
    right name is not evidence, and this preflight exists precisely because
    that substitution is easy to make and impossible to notice afterwards.
    """
    require_execution_approval(approval, f"Drive folder {folder_id!r}")
    reader = reader or LocalTreeReader(approval)
    gates: List[Dict[str, object]] = []
    inventory: List[Dict[str, object]] = []

    def stop(reason: str, **extra) -> Dict[str, object]:
        out = {"prep": "P2", "ok": False, "status": reason,
               "first_failure": reason, "gates": gates,
               "gate_order": list(P2_GATE_ORDER),
               **_folder_identity(folder_id),
               "inventory": inventory, "input_identity": None,
               "gate_passed": False, "eligible_for_registration": False,
               "observation_only": False, "blocked_by": reason,
               "seals": _p2_seals()}
        out.update(extra)
        return out

    # ---- gate 1: direct children of the registered folder id --------------
    inventory = [normalise_child(c) for c in adapter.list_children(folder_id)]
    gates.append({"gate": "folder_id_inventory", "ok": bool(inventory),
                  "folder_id": folder_id, "n_children": len(inventory)})
    if not inventory:
        return stop(P2_FOLDER_ID_BRIDGE_UNRESOLVED)

    # ---- gate 2: the inventory is unambiguous -----------------------------
    # P2's identity key is the Drive file id.  A row without one cannot be
    # used at all, and a duplicated one makes "which file" unanswerable.
    names = [row["name"] for row in inventory]
    ids = [row["file_id"] for row in inventory]
    expected_names = set(BJ.BUNDLE_FILES) | {SUPERSEDED_MARKER}
    ambiguity = {
        "duplicate_names": sorted({n for n in names if names.count(n) > 1}),
        "subfolders": [r["name"] for r in inventory if r["is_folder"]],
        "shortcuts": [r["name"] for r in inventory if r["is_shortcut"]],
        "trashed": [r["name"] for r in inventory if r["trashed"]],
        "nameless": [r["file_id"] for r in inventory if not r["name"]],
        "missing_file_id": [r["name"] for r in inventory if not r["file_id"]],
        "duplicate_file_ids": sorted(
            {i for i in ids if i and ids.count(i) > 1}),
        # A Google-native document has no plain bytes to hash, so one wearing
        # a bundle file's name is a substitution, not a bundle member.
        "google_native": [
            r["name"] for r in inventory
            if str(r["mime_type"]).startswith("application/vnd.google-apps.")
            and not r["is_folder"] and not r["is_shortcut"]],
        # A regular file must report a size; without one the inventory cannot
        # be cross-checked against the bytes.
        "sizeless": [
            r["name"] for r in inventory
            if r["bytes"] is None and not r["is_folder"]
            and not r["is_shortcut"]
            and not str(r["mime_type"]).startswith(
                "application/vnd.google-apps.")],
    }
    unambiguous = not any(ambiguity.values())
    gates.append({"gate": "inventory_unambiguous", "ok": unambiguous,
                  "expected_names": sorted(expected_names), **ambiguity})
    if not unambiguous:
        return stop(P2_INVENTORY_AMBIGUOUS, ambiguity=ambiguity)

    live = [r for r in inventory if not r["trashed"]]
    live_names = sorted(r["name"] for r in live)

    # ---- gate 3: the whole twelve-file directory contract -----------------
    expected = list(BJ.BUNDLE_FILES)
    missing = [n for n in expected if n not in live_names]
    unexpected = [n for n in live_names
                  if n not in expected and n != SUPERSEDED_MARKER]
    directory_ok = not missing and not unexpected
    gates.append({"gate": "directory_contract", "ok": directory_ok,
                  "n_expected": len(expected), "n_observed": len(live_names),
                  "missing": missing, "unexpected": unexpected})
    if not directory_ok:
        return stop(P2_DIRECTORY_CONTRACT_FAILED)

    # ---- gate 4: no SUPERSEDED marker -------------------------------------
    superseded = SUPERSEDED_MARKER in live_names
    gates.append({"gate": "superseded_absent", "ok": not superseded,
                  "marker": SUPERSEDED_MARKER})
    if superseded:
        return stop(P2_SUPERSEDED_PRESENT)

    # ---- gate 5: canonical bytes, by file id or a proven mount bridge -----
    bytes_by_name, bridge = _canonical_bytes(
        inventory, adapter, mount_dir, reader)
    gates.append(bridge)
    if not bridge["ok"]:
        return stop(P2_FOLDER_ID_BRIDGE_UNRESOLVED, bridge=bridge)

    # The bridge really did cross-check every file against the inventory, and
    # that observation stands on its own: it is what a later manifest failure
    # gets diagnosed against.  It is preserved on every stop from here on, and
    # it is explicitly not an identity — `input_identity` stays None because
    # that gate was never reached.
    bridged = {"bridge": bridge, "observation_only": True,
               "observation_note": (
                   "the canonical-bytes bridge passed and its cross-checks are "
                   "preserved as observations; they are not an input identity, "
                   "which is only produced by the final P2 gate")}

    # ---- gate 6: manifest identity ----------------------------------------
    try:
        manifest = json.loads(bytes_by_name["manifest.json"].decode("utf-8"))
    except (KeyError, UnicodeDecodeError, ValueError) as error:
        gates.append({"gate": "manifest_identity", "ok": False,
                      "problems": [f"manifest.json unreadable: {error}"]})
        return stop(P2_MANIFEST_MISMATCH, **bridged)
    identity, problems = manifest_identity(manifest)
    gates.append({"gate": "manifest_identity", "ok": not problems,
                  **identity, "problems": problems})
    if problems:
        return stop(P2_MANIFEST_MISMATCH,
                    manifest_identity={**identity, "problems": problems},
                    **bridged)

    # ---- gate 7: the five-file scientific input identity ------------------
    # Only the files Q5-E reads.  The other seven are part of the directory
    # contract above and are NOT unexpected here.
    input_files = [
        {"name": name, "bytes": len(bytes_by_name[name]),
         "sha256": _sha256_bytes(bytes_by_name[name])}
        for name in sorted(BUNDLE_INPUT_FILES)]
    subset_fold = fold_file_triples(input_files)
    gates.append({"gate": "input_identity", "ok": True,
                  "n_files": len(input_files), "subset_fold": subset_fold,
                  "not_unexpected": sorted(set(BJ.BUNDLE_FILES)
                                           - set(BUNDLE_INPUT_FILES))})

    full_files = [
        {"name": name, "bytes": len(bytes_by_name[name]),
         "sha256": _sha256_bytes(bytes_by_name[name])}
        for name in sorted(BJ.BUNDLE_FILES)]
    return {
        "prep": "P2", "ok": True, "status": P2_PASS, "first_failure": None,
        "gates": gates, "gate_order": list(P2_GATE_ORDER),
        **_folder_identity(folder_id),
        "inventory": inventory,
        "directory_contract": {"n_expected": len(expected),
                               "missing": [], "unexpected": [],
                               "full_fold": fold_file_triples(full_files)},
        "manifest_identity": dict(identity),
        "input_identity": {"files": input_files, "subset_fold": subset_fold},
        "bridge": bridge,
        "gate_passed": True, "observation_only": False, "blocked_by": None,
        "seals": _p2_seals(),
    }


def _cross_check(row: Mapping[str, object], body: bytes,
                 method: str) -> Dict[str, object]:
    """Compare fetched bytes against everything the inventory claims.

    Length is always checked.  `sha256Checksum` is the identity check;
    `md5Checksum` is a **provider transfer cross-check**, not a security
    identity — MD5 is not collision-resistant and is never treated as one.
    A checksum the provider did not supply is recorded as unavailable rather
    than guessed at.
    """
    observed_sha = _sha256_bytes(body)
    observed_md5 = hashlib.md5(body).hexdigest()      # noqa: S324 - see above
    provider_sha = row.get("provider_sha256")
    provider_md5 = row.get("provider_md5")
    inventory_bytes = row.get("bytes")
    problems: List[str] = []
    if inventory_bytes is not None and int(inventory_bytes) != len(body):
        problems.append(
            f"{row['name']}: inventory says {inventory_bytes} bytes, fetched "
            f"{len(body)}")
    if provider_sha and str(provider_sha).lower() != observed_sha:
        problems.append(
            f"{row['name']}: provider sha256 disagrees with the fetched bytes")
    if provider_md5 and str(provider_md5).lower() != observed_md5:
        problems.append(
            f"{row['name']}: provider md5 disagrees with the fetched bytes")
    return {
        "file_id": row.get("file_id"), "name": row.get("name"),
        "download_method": method,
        "inventory_bytes": inventory_bytes, "observed_bytes": len(body),
        "bytes_match": (inventory_bytes is None
                        or int(inventory_bytes) == len(body)),
        "provider_sha256": provider_sha, "observed_sha256": observed_sha,
        "sha256_available": bool(provider_sha),
        "sha256_match": (bool(provider_sha)
                         and str(provider_sha).lower() == observed_sha),
        "provider_md5": provider_md5, "observed_md5": observed_md5,
        "md5_available": bool(provider_md5),
        "md5_match": (bool(provider_md5)
                      and str(provider_md5).lower() == observed_md5),
        "md5_note": "provider transfer cross-check, not a security identity",
        "checksum_available": bool(provider_sha or provider_md5),
        "problems": problems,
        "ok": not problems,
    }


def _canonical_bytes(inventory: Sequence[Mapping[str, object]],
                     adapter: DriveFolderAdapter, mount_dir: Optional[str],
                     reader: LocalTreeReader
                     ) -> Tuple[Dict[str, bytes], Dict[str, object]]:
    """Fetch the bundle's bytes and cross-check every one against the inventory.

    Preferred: stream each file **by file id**, which needs no bridge because
    the bytes come from the registered folder directly.  Either way the fetched
    bytes are re-checked against the inventory's size and any provider
    checksum; a fetch that merely *succeeded* proves nothing about what came
    back.  A missing provider checksum does not fail a direct stream — the
    file id already ties the bytes to the folder — but it is recorded as
    unavailable rather than passed over.
    """
    audit: List[Dict[str, object]] = []
    by_name: Dict[str, bytes] = {}
    streamed = True
    try:
        for row in inventory:
            body = adapter.download(str(row["file_id"]))
            by_name[str(row["name"])] = body
            audit.append(_cross_check(row, body, "drive_file_id_stream"))
    except NotImplementedError:
        streamed = False
        by_name, audit = {}, []

    if streamed:
        problems = [p for entry in audit for p in entry["problems"]]
        if problems:
            # Do not hand these bytes downstream: a manifest or input identity
            # computed from unverified bytes would look like evidence.
            return {}, {"gate": "canonical_bytes_bridge", "ok": False,
                        "method": None, "attempted": "drive_file_id_stream",
                        "n_files": len(audit), "cross_check": audit,
                        "problems": problems}
        return by_name, {
            "gate": "canonical_bytes_bridge", "ok": True,
            "method": "drive_file_id_stream", "n_files": len(audit),
            "cross_check": audit,
            "n_without_checksum": sum(1 for e in audit
                                      if not e["checksum_available"]),
            "note": ("bytes came from the registered folder id directly and "
                     "were re-checked against the inventory; no mount bridge "
                     "was needed")}

    if not mount_dir:
        return {}, {"gate": "canonical_bytes_bridge", "ok": False,
                    "method": None, "attempted": "mount",
                    "cross_check": [],
                    "problems": ["the adapter cannot stream by file id and no "
                                 "mount was supplied, so the folder id cannot "
                                 "be linked to any bytes"]}

    present = reader.listdir(mount_dir)
    inventory_names = sorted(str(r["name"]) for r in inventory)
    problems: List[str] = []
    if sorted(present) != inventory_names:
        problems.append(
            f"mount holds {sorted(present)} but the folder id lists "
            f"{inventory_names}; the two are not the same file set")
    if not problems:
        for row in inventory:
            name = str(row["name"])
            with open(os.path.join(mount_dir, name), "rb") as handle:
                body = handle.read()
            entry = _cross_check(row, body, "mount_bridged_to_folder_id")
            audit.append(entry)
            problems.extend(entry["problems"])
            by_name[name] = body
    if problems:
        return {}, {"gate": "canonical_bytes_bridge", "ok": False,
                    "method": None, "attempted": "mount",
                    "n_files": len(audit), "cross_check": audit,
                    "problems": problems,
                    "note": ("a matching folder *name* is never accepted as "
                             "the bridge")}
    return by_name, {
        "gate": "canonical_bytes_bridge", "ok": True,
        "method": "mount_bridged_to_folder_id", "n_files": len(audit),
        "cross_check": audit,
        "n_without_checksum": sum(1 for e in audit
                                  if not e["checksum_available"]),
        "note": ("the mount was tied to the folder-id inventory by exact "
                 "name, size and every available provider checksum; a "
                 "matching folder name is never accepted as the bridge")}


#: Where each identity field actually lives in `BJ.build_manifest()`'s output.
#: Recorded in the result so a reader can see which field was consulted rather
#: than infer it — the previous version read a `code_sha256` key that the
#: producer has never written, and the report gave no way to notice.
MANIFEST_IDENTITY_SOURCES: Dict[str, str] = {
    "code_sha256": "manifest['code']['sha256'] (nested, from "
                   "assert_implementation_only())",
    "rule_fingerprint": "manifest['rule_fingerprint'] (top level)",
    "preflight_rule_fingerprint": "manifest['preflight']['rule_fingerprint'] "
                                  "(cross-checked against the top level when "
                                  "the freeze carries one)",
}


def manifest_identity(manifest: Mapping[str, object]
                      ) -> Tuple[Dict[str, object], List[str]]:
    """Read the producing identity from where the producer actually writes it.

    `BJ.build_manifest()` records the module digest **nested**, as
    ``manifest['code']['sha256']`` — `code` is the mapping
    `assert_implementation_only()` returns — and the rule fingerprint at the
    top level.  An earlier version of this gate read a flat
    ``manifest['code_sha256']``, which no producer has ever written; against
    the real bundle it resolved to `""`, and the gate then failed for a reason
    that had nothing to do with the bundle.  The synthetic fixture agreed with
    it only because the fixture was a hand-written flat dict authored from the
    same belief as the code, so the tests could confirm the belief and never
    test it.  The fixtures now come from `BJ.build_manifest()` itself.

    Both fields are matched **exactly** against the registered constants.
    There is no raw/LF alternative: a shard and a manifest store whatever the
    producing checkout stored, and accepting one digest while returning
    another would hand the caller an identity the artifact does not carry.

    Malformed, missing, null or wrongly typed fields are returned as
    `problems`, never raised, and the caller turns them into
    `P2_MANIFEST_IDENTITY_MISMATCH`.  Nothing here calls into the frozen
    module, so there is no exception to catch and no room for a `RuntimeError`
    or an `AssertionError` from elsewhere to be relabelled as a manifest
    defect.
    """
    problems: List[str] = []
    observed: Dict[str, object] = {
        "code_sha256": None, "rule_fingerprint": None,
        "preflight_rule_fingerprint": None,
        "read_from": dict(MANIFEST_IDENTITY_SOURCES),
    }

    fingerprint = manifest.get("rule_fingerprint")
    if not isinstance(fingerprint, str) or not _is_sha256(fingerprint):
        problems.append(
            f"rule_fingerprint: {fingerprint!r} is not a 64-hex string at the "
            f"manifest's top level")
    else:
        observed["rule_fingerprint"] = fingerprint
        if fingerprint != REGISTERED_RULE_FINGERPRINT:
            problems.append(
                f"rule_fingerprint {fingerprint} != the registered "
                f"{REGISTERED_RULE_FINGERPRINT}")

    code = manifest.get("code")
    if not isinstance(code, Mapping):
        problems.append(
            f"code: {type(code).__name__}, not the mapping the producer writes "
            f"under manifest['code']; the module digest lives at "
            f"manifest['code']['sha256'] and a flat manifest['code_sha256'] is "
            f"not this schema")
    else:
        code_sha = code.get("sha256")
        if not isinstance(code_sha, str) or not _is_sha256(code_sha):
            problems.append(
                f"code.sha256: {code_sha!r} is not a 64-hex string")
        else:
            observed["code_sha256"] = code_sha
            if code_sha != PRODUCING_CODE_SHA256:
                problems.append(
                    f"code.sha256 {code_sha} != the registered "
                    f"{PRODUCING_CODE_SHA256}")

    # The freeze is optional in the schema — `build_manifest()` writes `None`
    # when no preflight was supplied — but when it is there it must not
    # disagree with the manifest it sits inside.  Two fingerprints in one file
    # that differ mean the file was assembled from two runs.
    preflight = manifest.get("preflight")
    if preflight is None:
        observed["preflight_present"] = False
    elif not isinstance(preflight, Mapping):
        observed["preflight_present"] = True
        problems.append(
            f"preflight: {type(preflight).__name__}, not the frozen input "
            f"freeze mapping or null")
    else:
        observed["preflight_present"] = True
        frozen = preflight.get("rule_fingerprint")
        if frozen is not None:
            observed["preflight_rule_fingerprint"] = frozen
            if frozen != fingerprint:
                problems.append(
                    f"preflight.rule_fingerprint {frozen!r} disagrees with the "
                    f"manifest's own {fingerprint!r}")
    return observed, problems


def _p2_seals() -> Dict[str, bool]:
    return {"bytes_hashed_only": True, "file_contents_aggregated": False,
            "parquet_parsed": False, "probability_opened": False,
            "labels_opened": False, "model_scored": False,
            "training_performed": False, "drive_modified": False}


# ─────────────────────────────────────────────────────────────────────────────
# Combined decision.  Independent gates, preserved independently.
# ─────────────────────────────────────────────────────────────────────────────
def combine(p1: Mapping[str, object], p2: Mapping[str, object]
            ) -> Dict[str, object]:
    """One verdict over two independent gates; neither overwrites the other."""
    failures = [dict(r) for r in (p1, p2) if not r.get("ok")]
    if not failures:
        status = PREP_PASS
    elif len(failures) > 1:
        status = PREP_MULTIPLE_FAILURES
    else:
        status = str(failures[0].get("first_failure") or "")
    return {
        "status": status,
        "p1": {"status": p1.get("status"), "ok": bool(p1.get("ok")),
               "first_failure": p1.get("first_failure")},
        "p2": {"status": p2.get("status"), "ok": bool(p2.get("ok")),
               "first_failure": p2.get("first_failure")},
        "both_passed": not failures,
        "failed_preps": [str(f.get("prep")) for f in failures],
        "registration_allowed": not failures,
        "note": ("P1 and P2 are scientifically independent; a failure in one "
                 "does not overwrite the other's verdict, and no value is "
                 "registered unless both pass"),
    }


def registration_candidates(p1: Mapping[str, object], p2: Mapping[str, object],
                            combined: Mapping[str, object]
                            ) -> Dict[str, object]:
    """Observations and eligibility, kept as **separate** facts.

    An earlier draft blanked a passing gate's observation when the other gate
    failed.  That destroyed audit evidence: P1 really did compute an
    aggregate, and erasing it makes the run harder to diagnose, not safer.
    What must be withheld is *eligibility to register*, not the observation.

    So each entry reports what was measured, whether its own gate passed, and
    whether the combined gate opened registration.  A value that was never
    computed — because its gate stopped earlier — stays `None`, because there
    is nothing to report.
    """
    both = bool(combined.get("registration_allowed"))
    blocked_by = sorted({str(r.get("first_failure")) for r in (p1, p2)
                         if r.get("first_failure")})

    def entry(target: str, observed: object, gate: Mapping[str, object],
              **extra) -> Dict[str, object]:
        passed = bool(gate.get("ok"))
        return {
            "target": target,
            # Preserved regardless of the other gate's verdict.
            "observed": observed,
            "gate_passed": passed,
            "combined_registration_allowed": both,
            "eligible_for_registration": bool(passed and both),
            "applied_automatically": False,
            "blocked_by": blocked_by,
            **extra}

    # P1's aggregate exists only when gate 4 was reached.  On
    # MITDB_IDENTITY_DIVERGED it was computed but the gate failed, so it is a
    # diagnostic observation and explicitly not a candidate.
    p1_observed = p1.get("tree_aggregate")
    p1_entry = entry(
        "q5e_leg2_failure_mechanism_audit.MITDB_TREE_AGGREGATE",
        p1_observed, p1,
        # True only when this *target* was actually measured under a failed
        # gate.  A publisher-checksum failure preserves 147 per-file digests
        # but folds no aggregate, so the target is genuinely absent while the
        # observations it would have been folded from are not.
        observation_only=bool(p1.get("observation_only")
                              and p1_observed is not None),
        per_file_observations=len(p1.get("per_file") or ()),
        observation_note=(
            p1.get("observation_note")
            or ("computed after every P1 gate passed" if p1.get("ok")
                else "not computed: P1 stopped before the aggregate gate")))

    identity = dict(p2.get("input_identity") or {})
    p2_observed = ({f["name"]: f["sha256"] for f in identity.get("files", ())}
                   or None)
    p2_entry = entry(
        "q5e_leg2_failure_mechanism_audit.SOURCE_BUNDLE_FILE_SHA256",
        p2_observed, p2,
        subset_fold=identity.get("subset_fold"),
        # Preserved even when a later gate failed: the bridge really did
        # cross-check these files, and that is diagnostic evidence.
        bridge_cross_checks=len(
            (p2.get("bridge") or {}).get("cross_check") or ()),
        bridge_method=(p2.get("bridge") or {}).get("method"),
        observation_note=(
            "computed after every P2 gate passed" if p2.get("ok")
            else str(p2.get("observation_note")
                     or "not computed: P2 stopped before the input-identity "
                        "gate")))

    return {
        "registration_allowed": both,
        "applied_automatically": False,
        "blocked_by": blocked_by,
        "note": ("observations are preserved even when the other gate failed; "
                 "only eligibility is withheld.  Nothing here modifies "
                 "q5e_leg2_failure_mechanism_audit.py or the spec — a separate "
                 "result-acceptance PR registers eligible values after "
                 "review."),
        "MITDB_TREE_AGGREGATE": p1_entry,
        "SOURCE_BUNDLE_FILE_SHA256": p2_entry,
    }


# ─────────────────────────────────────────────────────────────────────────────
# Bundle
# ─────────────────────────────────────────────────────────────────────────────
#: Test seam.  Called once between claiming the directory and filling it —
#: the only window the publish still has, and one in which the name cannot be
#: taken, only written into.  Production never sets it; it exists so the
#: remaining window can be exercised rather than argued about.
_PUBLISH_RACE_HOOK = None


def _write_new_file(path: str, body: bytes) -> None:
    """Create a file that must not already exist, and write all of it.

    `open(path, "w")` truncates whatever is there.  Inside a directory this
    call just claimed, another writer's file should be impossible — but
    "should be impossible" is exactly what the withdrawn atomicity claim
    asserted and got wrong, and a truncating write turns someone else's bytes
    into ours with no error and no trace.  `O_EXCL` makes the creation itself
    the check, so there is no window between deciding the name is free and
    taking it.

    `O_BINARY` matters and is not Windows boilerplate.  Without it Windows
    opens the descriptor in text mode and rewrites every `\\n` on the way out,
    so the file on disk is not the bytes that were handed in — and since the
    caller hashes what it *passed*, the recorded digest would describe bytes
    that never existed.  A synthetic run would then fail its own consumer
    check, and the failure would look like corruption rather than a translated
    newline.  The flag is absent on POSIX, where `getattr` supplies 0.

    The write loop is not decoration: `os.write` is allowed to write fewer
    bytes than it was handed, and a short write would produce a truncated file
    that still hashes to *something* and would be committed as a bundle.  A
    return of 0 makes no progress, so it is refused rather than retried
    forever — a silent hang is worse than a named failure.
    """
    flags = (os.O_CREAT | os.O_EXCL | os.O_WRONLY
             | getattr(os, "O_BINARY", 0))
    try:
        handle = os.open(path, flags, 0o644)
    except FileExistsError as error:
        raise PrepError(
            f"refusing to write {os.path.basename(path)!r}: it already exists "
            f"in this run's own directory.  Something else created it after "
            f"the directory was claimed; its bytes are left untouched and "
            f"this bundle is not committed.") from error
    try:
        written = 0
        while written < len(body):
            chunk = os.write(handle, body[written:])
            if chunk <= 0:
                raise PrepError(
                    f"refusing to continue writing {os.path.basename(path)!r}:"
                    f" os.write made no progress at byte {written} of "
                    f"{len(body)}.  Retrying would spin forever, and the file "
                    f"as it stands is truncated.")
            written += chunk
    finally:
        os.close(handle)


def _write_new_json(path: str, value: object) -> bytes:
    """Exclusive-create a canonical JSON file and return the bytes written."""
    body = json.dumps(value, indent=1, sort_keys=True).encode("utf-8")
    _write_new_file(path, body)
    return body


def _is_link_like(path: str) -> bool:
    """Symlink, or a Windows junction / reparse point where detectable.

    A junction is not a symlink as far as `os.path.islink` is concerned on
    older interpreters, and writing through one lands somewhere other than
    where the path says.  `os.path.isjunction` exists from 3.12; where it does
    not, this reports what it can rather than claiming a check it did not make.
    """
    if os.path.islink(path):
        return True
    isjunction = getattr(os.path, "isjunction", None)
    if isjunction is not None:
        try:
            return bool(isjunction(path))
        except OSError:                                    # pragma: no cover
            return False
    return False
def build_config(timestamp: str, synthetic: bool,
                 auth_audit: Optional[Mapping[str, object]] = None
                 ) -> Dict[str, object]:
    """The run's own description, including the environment it happened in.

    A digest is only as interpretable as the run that produced it: "which
    interpreter, which client library version, under which Drive scope" has to
    be answerable months later, and it cannot be reconstructed after the fact.
    Versions that cannot be determined are reported as `unavailable` rather
    than guessed, and nothing here is installed or upgraded to make the record
    look tidier.
    """
    return {"experiment_id": EXPERIMENT_ID, "substage": SUBSTAGE,
            "run_slug": RUN_SLUG, "module_version": MODULE_VERSION,
            "timestamp": timestamp, "spec": SPEC_PATH,
            "contract": CONTRACT_PATH,
            "runtime": runtime_identity(),
            "dependencies": check_runtime_dependencies(),
            # Present only on a route that authenticated.  A synthetic run
            # never authenticates, so it records that plainly rather than
            # leaving the field ambiguous.
            "drive_authentication": (dict(auth_audit) if auth_audit else {
                "performed": False,
                "requested_scopes": [DRIVE_READONLY_SCOPE],
                "exact_readonly_scope_proven": False,
                "reason": ("no Drive authentication was performed on this "
                           "route; nothing was proven and nothing is claimed"),
            }),
            "scope": ["P1", "P2"], "p3_in_scope": False,
            "synthetic_fixture": bool(synthetic),
            "ingestable": not synthetic,
            "registered_targets": {
                "mitdb_checksum_file_sha256": MITDB_CHECKSUM_FILE_SHA256,
                "mitdb_publisher_listed_files": MITDB_PUBLISHER_LISTED_FILES,
                "mitdb_registered_aggregate_prefix":
                    MITDB_REGISTERED_AGGREGATE_PREFIX,
                # The two folders, under separate keys.  Q5-E's registered
                # constants are recorded unchanged; the corrective folder is
                # recorded as the candidate this run judged.
                "source_bundle_run": SOURCE_BUNDLE_RUN,
                "source_bundle_folder_id": SOURCE_BUNDLE_FOLDER_ID,
                "original_canonical_run": ORIGINAL_CANONICAL_RUN,
                "original_canonical_folder_id": ORIGINAL_CANONICAL_FOLDER_ID,
                "corrective_candidate_run": CORRECTIVE_BUNDLE_RUN,
                "corrective_candidate_folder_id": CORRECTIVE_BUNDLE_FOLDER_ID,
                "corrective_candidate_spec": CORRECTIVE_BUNDLE_SPEC,
                "p2_target_folder_id": P2_TARGET_FOLDER_ID,
                "candidate_is_registered_as_canonical": False,
                "producing_code_sha256": PRODUCING_CODE_SHA256,
                "rule_fingerprint": REGISTERED_RULE_FINGERPRINT,
                "manifest_identity_sources": dict(MANIFEST_IDENTITY_SOURCES)},
            "approval_note": APPROVAL_NOTE,
            "prior_approvals": [dict(r)
                                for r in PRIOR_EXECUTION_APPROVAL_RECORDS]}


def summary_markdown(combined: Mapping[str, object], p1: Mapping[str, object],
                     p2: Mapping[str, object], synthetic: bool) -> str:
    lines = [f"# {EXPERIMENT_ID} / Q5-E PREP P1+P2 - asset identity", ""]
    if synthetic:
        lines += ["> **SYNTHETIC FIXTURE - NOT A Q5-E RESULT.**  Produced from",
                  "> synthetic fixtures. It is not an asset identity and is",
                  "> never an ingest candidate.", ""]
    lines += [
        f"- combined status: `{combined.get('status')}`",
        f"- P1: `{p1.get('status')}` (first failure: "
        f"`{p1.get('first_failure')}`)",
        f"- P2: `{p2.get('status')}` (first failure: "
        f"`{p2.get('first_failure')}`)",
        f"- registration allowed: {combined.get('registration_allowed')}",
        "",
        "P1 and P2 are independent gates. A failure in one does not overwrite",
        "the other's verdict, and no value is registered unless both pass.",
        "",
        "This is an asset-identity preflight. It is not a Q5-E measurement,",
        "no detector ran, and no M0-M4 aggregation was performed.",
    ]
    return "\n".join(lines) + "\n"


def write_bundle(directory: str, config: Mapping[str, object],
                 p1: Mapping[str, object], p2: Mapping[str, object],
                 combined: Mapping[str, object], log_lines: Sequence[str],
                 synthetic: bool = False) -> Dict[str, object]:
    """Claim the output directory, write into it, and commit it with a marker.

    **There is no rename here, and the atomic-directory-publication claim an
    earlier version made is withdrawn.**  That version staged elsewhere and
    published with `rmdir(directory)` followed by `rename(staging, directory)`.
    Those are two operations, and between them a new directory can appear at
    the target — POSIX `rename` then *replaces* it, silently, as long as it is
    empty.  Claiming the name with `mkdir` closed the earlier `lexists`-then-
    rename window but not this one: the claim was given back before the rename
    took it.  Linux offers `renameat2(RENAME_NOREPLACE)`, which really is
    atomic, but the production output path is a Drive FUSE mount where that
    flag is not dependable, and a fallback that silently degrades to plain
    `rename` would be the same defect wearing a safer name.

    So the directory is published in place and its **completeness** is what is
    made atomic instead:

    1. `os.mkdir(directory)` — one operation that creates the name or fails.
       It never replaces or follows anything: a file, an empty directory, a
       non-empty directory, a symlink or a junction all raise.
    2. every payload file, then `manifest.json`, written inside the claim.
    3. `COMMITTED.json` created last with `O_CREAT | O_EXCL`.

    A directory without that marker is **not a bundle** — it is an incomplete
    or failed write, and :func:`verify_published_bundle` refuses it.  That is
    the consumer's contract, and it is stronger than atomic appearance: it
    survives a crash, and it also catches truncation and later editing, which
    an atomic rename never could.

    Nothing pre-existing is ever deleted or replaced, and nothing is deleted at
    all — a failed run leaves its partial, uncommitted directory exactly where
    it is, because that is where a diagnosis will look for it.
    """
    payload_names = payload_files(synthetic)
    candidates = registration_candidates(p1, p2, combined)
    payload: Dict[str, object] = {
        "config.json": config,
        "source_inventory.json": {"p1_per_file": p1.get("per_file", []),
                                  "p2_folder_inventory": p2.get("inventory",
                                                                [])},
        "decision.json": {"combined": dict(combined), "p1": dict(p1),
                          "p2": dict(p2)},
        "registration_candidates.json": candidates,
    }
    for name, value in payload.items():
        assert_no_credentials(value, name)

    parent = os.path.dirname(os.path.abspath(directory)) or "."
    os.makedirs(parent, exist_ok=True)
    if _is_link_like(parent):
        raise PrepError(
            f"refusing to publish under {parent!r}: it is a symlink or "
            f"reparse point, and this function does not follow links when "
            f"writing or renaming")

    # Claim the name atomically.  `mkdir` fails if anything at all is there,
    # and it does not follow a symlink sitting at the path, so an existing
    # file, empty directory, non-empty directory, symlink or junction is
    # preserved untouched rather than overwritten.
    try:
        os.mkdir(directory)
    except FileExistsError as error:
        raise PrepError(
            f"refusing to publish to {directory!r}: something is already "
            f"there.  A PREP bundle is new, never an overwrite, and this "
            f"function does not delete or replace anything that already "
            f"exists — not a file, not an empty directory, not a symlink."
        ) from error
    try:
        if _PUBLISH_RACE_HOOK is not None:
            # The only window left: between claiming the name and filling it.
            # Nothing here can take the name away, but something *can* write
            # into it, and the file-set check below is what catches that.
            _PUBLISH_RACE_HOOK(directory)

        # Every file below is created exclusively.  Not one of them may
        # replace something that is already at its name.
        for name, value in payload.items():
            _write_new_json(os.path.join(directory, name), value)
        _write_new_file(
            os.path.join(directory, "log.txt"),
            ("\n".join(str(line) for line in log_lines) + "\n")
            .encode("utf-8"))
        summary = summary_markdown(combined, p1, p2, synthetic)
        _write_new_file(os.path.join(directory, "summary.md"),
                        summary.encode("utf-8"))
        if synthetic:
            _write_new_json(
                os.path.join(directory, SYNTHETIC_MARKER),
                {"synthetic_fixture": True, "ingestable": False,
                 "reason": SYNTHETIC_NOTE})

        written = sorted(os.listdir(directory))
        if written != sorted(payload_names):
            raise PrepError(
                f"refusing to commit: the written file set {written} is not "
                f"the contracted set {sorted(payload_names)}.  A file outside "
                f"the payload identity would be unaccounted for.")

        triples = []
        for name in written:
            path = os.path.join(directory, name)
            with open(path, "rb") as handle:
                body = handle.read()
            triples.append({"name": name, "bytes": len(body),
                            "sha256": _sha256_bytes(body)})
        fold = fold_file_triples(triples)
        manifest = {
            "experiment_id": EXPERIMENT_ID, "substage": SUBSTAGE,
            "timestamp": config.get("timestamp"),
            "prep_payload_sha256": fold,
            # The actual fold target for this kind of run, not a static list.
            "payload_files": list(payload_names),
            "excluded_from_payload_fold": [PREP_MANIFEST_FILE],
            "manifest_self_digest_recorded_here": False,
            "manifest_self_digest_frozen_externally": True,
            "synthetic_fixture": bool(synthetic),
            "ingestable": not synthetic,
            "module_sha256": Q5E.sha256_file(os.path.abspath(__file__)),
            "frozen_module_sha256": Q5E.sha256_file(
                os.path.abspath(BJ.__file__)),
            # Which environment produced this identity, and under which scope.
            "runtime": config.get("runtime"),
            "drive_authentication": config.get("drive_authentication"),
            "note": ("manifest.json is excluded from the fold it records; its "
                     "own SHA-256 is frozen outside this bundle, in the "
                     "execution-contract Decision log and the registration "
                     "record"),
        }
        assert_no_credentials(manifest, PREP_MANIFEST_FILE)
        manifest_digest = _sha256_bytes(_write_new_json(
            os.path.join(directory, PREP_MANIFEST_FILE), manifest))

        before_commit = sorted(os.listdir(directory))
        expected_before = sorted(set(bundle_files(synthetic)) - {COMMIT_MARKER})
        if before_commit != expected_before:
            raise PrepError(
                f"refusing to commit: file set {before_commit} != "
                f"{expected_before}")

        # The commit.  `O_EXCL` means this either creates the marker or fails;
        # it can never overwrite one, so a directory cannot be committed twice
        # or have its commit record rewritten by a second run.
        marker = {
            "committed": True,
            "experiment_id": EXPERIMENT_ID, "substage": SUBSTAGE,
            "timestamp": config.get("timestamp"),
            "bundle_files": sorted(bundle_files(synthetic)),
            "payload_files": list(payload_names),
            "prep_payload_sha256": fold,
            # The manifest's own SHA-256 is deliberately NOT here.  It stays
            # outside the bundle entirely, exactly as before; a consumer
            # anchors the manifest by passing the externally frozen value to
            # verify_published_bundle().  A digest recorded inside the artifact
            # it describes is rewritten by whoever edits that artifact, so it
            # would look like a freeze record without being one.
            "manifest_sha256_recorded_here": False,
            "manifest_sha256_frozen_externally": True,
            "synthetic_fixture": bool(synthetic),
            "ingestable": not synthetic,
            "note": ("a bundle directory without this marker is an incomplete "
                     "or failed write, not a bundle; verify_published_bundle() "
                     "refuses it.  This replaces an atomic-rename publish, "
                     "which could not be made no-replace on the Drive FUSE "
                     "mount this writes to"),
        }
        assert_no_credentials(marker, COMMIT_MARKER)
        _write_new_json(os.path.join(directory, COMMIT_MARKER), marker)

        final_set = sorted(os.listdir(directory))
        if final_set != sorted(bundle_files(synthetic)):   # pragma: no cover
            raise PrepError(
                f"refusing to report a publish: final file set {final_set} != "
                f"{sorted(bundle_files(synthetic))}")
    except Exception as error:
        # Keep the evidence exactly where it is.  The directory stays,
        # uncommitted, which is precisely what marks it as a failed write —
        # and deleting it is how a diagnosis gets lost.  Nothing is removed.
        raise PrepError(
            f"PREP bundle was not committed: {error}.  The partial directory "
            f"is preserved at {directory!r} for inspection.  It carries no "
            f"{COMMIT_MARKER}, so it is not a bundle and no consumer will "
            f"accept it.  Nothing was deleted or replaced.") from error
    return {"directory": directory, "written": final_set,
            "payload_files": list(payload_names),
            "prep_payload_sha256": fold,
            # Returned for external freezing; deliberately NOT inside the
            # manifest.  `COMMITTED.json` records it too, which is not a
            # self-reference — the marker does not record its own digest — and
            # is a completeness check, not the external freeze record.
            "manifest_sha256_freeze_externally": manifest_digest,
            "committed": True,
            "registration_allowed": bool(combined.get("registration_allowed"))}


def _load_json(path: str, label: str) -> Tuple[object, Optional[str]]:
    """Read a JSON file without ever letting a parse error escape.

    A truncated or hand-edited bundle file is one of the things this verifier
    exists to detect, so raising `JSONDecodeError` at the caller would turn a
    finding into a crash — and a crash is not a verdict a reviewer can act on.
    """
    try:
        with open(path, "rb") as handle:
            body = handle.read()
    except OSError as error:
        return None, f"{label} could not be read: {error}"
    try:
        value = json.loads(body.decode("utf-8"))
    except (UnicodeDecodeError, ValueError) as error:
        return None, (f"{label} is not readable JSON ({error}); a truncated or "
                      f"edited file is not a bundle member")
    if not isinstance(value, dict):
        return None, f"{label} is a {type(value).__name__}, not an object"
    return value, None


def verify_published_bundle(directory: str,
                            expected_manifest_sha256: Optional[str] = None,
                            manifest_anchor_source: Optional[str] = None
                            ) -> Dict[str, object]:
    """The consumer's contract: is this directory a committed PREP bundle?

    Called by the run itself immediately after writing, so a run that cannot
    validate its own output fails loudly rather than reporting a success.  It
    is also what any later reader must use: since publication is no longer a
    rename, "the directory exists" says nothing.

    **The marker is checked, not trusted.**  An earlier version took the file
    list and the fold straight out of `COMMITTED.json`, which made the marker
    self-certifying: editing a payload file and rewriting the marker's fold
    produced a bundle that verified.  Every set and every duplicated field is
    therefore checked against the **fixed code contract** — `payload_files()`,
    `bundle_files()`, `EXPERIMENT_ID`, `SUBSTAGE` — and cross-checked between
    the marker and the manifest, which are written from the same run and must
    agree.  Only the recomputed fold counts, and it must equal both recorded
    folds.

    `manifest.json` is outside the payload fold, so the fold cannot detect an
    edited manifest, and its digest is deliberately absent from the bundle — a
    digest stored inside the artifact it describes is rewritten by whoever
    edits that artifact.  So it is anchored from outside, and the caller must
    say **where the anchor came from**: `manifest_anchor_source` is one of
    :data:`MANIFEST_ANCHOR_SOURCES`, not free text and not optional once a
    digest is supplied.

    That distinction is the whole point.  *Matching a digest* and *being
    anchored* are different facts, reported separately as
    `manifest_digest_matches_expected` and `manifest_anchored_externally`: a
    run comparing the manifest against the value it computed itself moments
    earlier has confirmed its own two lines of code agree, which is worth
    doing and is not evidence that nothing has been edited since — there is no
    "since" yet.  Only a digest from the saved notebook output or the
    registration record is external, and only that can carry
    `acceptance_eligible`.  Passing a string is not provenance.
    """
    problems: List[str] = []

    source = manifest_anchor_source
    if expected_manifest_sha256 is None:
        # No digest: the only honest source is "none".  A caller naming an
        # origin without a value has described evidence it did not bring.
        if source not in (None, ANCHOR_NONE):
            problems.append(
                f"manifest_anchor_source is {source!r} but no "
                f"expected_manifest_sha256 was supplied; an anchor origin "
                f"without a value is not an anchor")
        source = ANCHOR_NONE
    elif source is None or source == "":
        problems.append(
            "a manifest digest was supplied without a manifest_anchor_source; "
            "where a digest came from is what decides whether it anchors "
            f"anything, so it must be one of {list(MANIFEST_ANCHOR_SOURCES)}")
        source = None
    elif source not in MANIFEST_ANCHOR_SOURCES:
        problems.append(
            f"manifest_anchor_source {source!r} is not one of "
            f"{list(MANIFEST_ANCHOR_SOURCES)}; an unrecognised origin is "
            f"refused rather than treated as external")
        source = None
    elif source == ANCHOR_NONE:
        problems.append(
            f"manifest_anchor_source is {ANCHOR_NONE!r} but a digest was "
            f"supplied; say where it came from or do not pass it")
        source = None

    def verdict(**extra) -> Dict[str, object]:
        structure_ok = not problems
        matches = extra.get("manifest_digest_matches_expected")
        external = bool(source in EXTERNAL_MANIFEST_ANCHORS
                        and matches is True and structure_ok)
        if structure_ok and external:
            note = (f"structurally valid and the manifest matches a digest "
                    f"held outside this bundle ({source})")
        elif structure_ok and source == ANCHOR_SAME_RUN:
            note = ("structurally valid, and the manifest matches the digest "
                    "this same run computed — a self-check, not an external "
                    "anchor.  Acceptance needs the digest from the saved "
                    "notebook output or the registration record, so this is "
                    "NOT an acceptance pass")
        elif structure_ok:
            note = ("structurally valid, but manifest.json is outside the "
                    "payload fold and no external digest anchors it, so it is "
                    "unchecked and this is NOT an acceptance pass")
        else:
            note = "not structurally valid; acceptance is not in question"
        out: Dict[str, object] = {
            "directory": directory,
            "problems": problems,
            # Structural validity: is this a complete, self-consistent bundle?
            "ok": structure_ok,
            "structure_ok": structure_ok,
            # Where the caller says the comparison value came from, and
            # whether that origin is outside the run being verified.
            "manifest_anchor_source": source,
            "manifest_anchored_externally": external,
            # Acceptance is a stricter question than structure, and an
            # unanchored manifest can never answer it: the one file the fold
            # does not cover would be unchecked.
            "acceptance_eligible": structure_ok and external,
            "acceptance_note": note,
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
                       manifest_sha256=None, synthetic_fixture=None,
                       ingestable=None)

    marker, error = _load_json(marker_path, COMMIT_MARKER)
    if error:
        problems.append(error)
        return verdict(committed=False, prep_payload_sha256=None,
                       manifest_sha256=None, synthetic_fixture=None,
                       ingestable=None)

    manifest_path = os.path.join(directory, PREP_MANIFEST_FILE)
    manifest, error = _load_json(manifest_path, PREP_MANIFEST_FILE)
    if error:
        problems.append(error)
        manifest = {}

    manifest_digest = None
    if os.path.isfile(manifest_path):
        with open(manifest_path, "rb") as handle:
            manifest_digest = _sha256_bytes(handle.read())
    else:
        problems.append(f"{PREP_MANIFEST_FILE} is missing")

    # ---- the commit itself -------------------------------------------------
    # `committed` is the claim the whole marker exists to make, so it is
    # checked by identity rather than truthiness.  A marker that says
    # `committed: false`, or omits the field, is a record of a write that did
    # not finish; accepting it because a manifest digest happened to match
    # would let an abandoned directory pass as a bundle.
    if marker.get("committed") is not True:
        problems.append(
            f"{COMMIT_MARKER}: committed is {marker.get('committed')!r}, not "
            f"True.  This directory does not claim to be a finished bundle, "
            f"and nothing else can make that claim on its behalf.")

    # ---- which contract applies -------------------------------------------
    # `synthetic` decides the expected file sets, so it cannot be taken from
    # one file's say-so.  Both records must agree, and `ingestable` must be
    # its negation; flipping the flag then fails the file-set check, because
    # the synthetic marker file is part of the fixed contract for one value
    # and absent from it for the other.
    #
    # The types are checked by identity, not by truthiness.  `bool("false")`
    # is True, so a string that reads as a denial would have been taken as an
    # assertion — the more alarming the value looks, the more certainly it
    # would have passed.  `0`/`1` are likewise not booleans here, however
    # readable they are, because the contract writes real JSON booleans and
    # anything else means the file was not written by this code.
    def _strict_bool(label: str, record: Mapping[str, object],
                     field: str) -> Optional[bool]:
        if field not in record:
            problems.append(f"{label}: {field} is missing")
            return None
        value = record[field]
        if type(value) is not bool:                       # noqa: E721
            problems.append(
                f"{label}: {field} is {value!r} ({type(value).__name__}), not "
                f"a JSON boolean; truthiness is not accepted here")
            return None
        return value

    flags: Dict[str, Dict[str, Optional[bool]]] = {}
    for label, record in ((COMMIT_MARKER, marker),
                          (PREP_MANIFEST_FILE, manifest)):
        flags[label] = {
            "synthetic_fixture": _strict_bool(label, record,
                                              "synthetic_fixture"),
            "ingestable": _strict_bool(label, record, "ingestable"),
        }
        synth = flags[label]["synthetic_fixture"]
        ingest = flags[label]["ingestable"]
        if synth is not None and ingest is not None and ingest is not (
                not synth):
            problems.append(
                f"{label}: ingestable {ingest!r} is not the negation of "
                f"synthetic_fixture {synth!r}")

    marker_synth = flags[COMMIT_MARKER]["synthetic_fixture"]
    manifest_synth = flags[PREP_MANIFEST_FILE]["synthetic_fixture"]
    if (marker_synth is not None and manifest_synth is not None
            and marker_synth is not manifest_synth):
        problems.append(
            f"synthetic_fixture disagrees: {COMMIT_MARKER} says "
            f"{marker_synth!r}, {PREP_MANIFEST_FILE} says {manifest_synth!r}")

    # When the flag is unusable, fall back to what is on disk rather than
    # guessing a contract — otherwise one bad field cascades into a file-set
    # complaint that hides the real one.
    if marker_synth is not None:
        synthetic = marker_synth
    else:
        synthetic = os.path.isfile(os.path.join(directory, SYNTHETIC_MARKER))

    expected_bundle = sorted(bundle_files(synthetic))
    expected_payload = sorted(payload_files(synthetic))

    # ---- the fixed code contract, not the marker's word --------------------
    observed = sorted(os.listdir(directory))
    if observed != expected_bundle:
        problems.append(
            f"file set {observed} != the contracted set {expected_bundle}")
    for label, record in ((COMMIT_MARKER, marker),
                          (PREP_MANIFEST_FILE, manifest)):
        declared = sorted(str(n) for n in record.get("payload_files") or ())
        if declared != expected_payload:
            problems.append(
                f"{label}: payload_files {declared} != the contracted "
                f"{expected_payload}")
    marker_bundle = sorted(str(n) for n in marker.get("bundle_files") or ())
    if marker_bundle != expected_bundle:
        problems.append(
            f"{COMMIT_MARKER}: bundle_files {marker_bundle} != the contracted "
            f"{expected_bundle}")

    # ---- fields both records carry, and the constants they came from -------
    for field, constant in (("experiment_id", EXPERIMENT_ID),
                            ("substage", SUBSTAGE)):
        for label, record in ((COMMIT_MARKER, marker),
                              (PREP_MANIFEST_FILE, manifest)):
            if record.get(field) != constant:
                problems.append(
                    f"{label}: {field} {record.get(field)!r} != {constant!r}")
    stamps = {}
    for label, record in ((COMMIT_MARKER, marker),
                          (PREP_MANIFEST_FILE, manifest)):
        value = record.get("timestamp")
        if type(value) is not str:                        # noqa: E721
            problems.append(
                f"{label}: timestamp is {value!r} ({type(value).__name__}), "
                f"not the contracted string")
        else:
            stamps[label] = value
    if len(stamps) == 2 and len(set(stamps.values())) != 1:
        problems.append(
            f"timestamp disagrees: {COMMIT_MARKER} says "
            f"{stamps[COMMIT_MARKER]!r}, {PREP_MANIFEST_FILE} says "
            f"{stamps[PREP_MANIFEST_FILE]!r}")

    # ---- the only digest that counts is the recomputed one -----------------
    triples = []
    for name in expected_payload:
        path = os.path.join(directory, name)
        if not os.path.isfile(path):
            problems.append(f"payload file {name!r} is missing")
            continue
        with open(path, "rb") as handle:
            body = handle.read()
        triples.append({"name": name, "bytes": len(body),
                        "sha256": _sha256_bytes(body)})
    fold = fold_file_triples(triples) if triples else None
    for label, record in ((COMMIT_MARKER, marker),
                          (PREP_MANIFEST_FILE, manifest)):
        recorded = record.get("prep_payload_sha256")
        if fold != recorded:
            problems.append(
                f"recomputed payload fold {fold} != {label}'s {recorded}")
    if (marker.get("prep_payload_sha256")
            != manifest.get("prep_payload_sha256")):
        problems.append(
            f"{COMMIT_MARKER} and {PREP_MANIFEST_FILE} record different "
            f"payload folds; one of them was rewritten")

    if PREP_MANIFEST_FILE in expected_payload:              # pragma: no cover
        problems.append(
            f"{PREP_MANIFEST_FILE} must not be inside the fold it records")

    matches: Optional[bool] = None
    if expected_manifest_sha256 is not None:
        matches = (manifest_digest is not None
                   and manifest_digest == expected_manifest_sha256)
        if not matches:
            problems.append(
                f"manifest digest {manifest_digest} != the {source or 'given'}"
                f" digest {expected_manifest_sha256}")

    return verdict(committed=marker.get("committed") is True,
                   prep_payload_sha256=fold,
                   manifest_sha256=manifest_digest,
                   expected_manifest_sha256=expected_manifest_sha256,
                   manifest_digest_matches_expected=matches,
                   synthetic_fixture=synthetic,
                   ingestable=flags[COMMIT_MARKER]["ingestable"])


# ─────────────────────────────────────────────────────────────────────────────
# Production entry point
# ─────────────────────────────────────────────────────────────────────────────
def run_prep(mitdb_dir: str, folder_id: str, out_dir: str,
             adapter: Optional[DriveFolderAdapter] = None,
             mount_dir: Optional[str] = None,
             approval: Optional[str] = None,
             open_registered_data: bool = OPEN_REGISTERED_DATA,
             timestamp: str = "", emit=print) -> Dict[str, object]:
    """The single production route for P1 and P2.

    Refuses without the separate read-only execution approval, and refuses
    again at the terminal guard.  Permission is checked before capability, so
    an unauthorised call is refused as unauthorised whatever happens to be
    installed and whatever credentials happen to exist.

    The order is fixed and it is the point of the function: switch, approval,
    folder id, **terminal guard**, then — and only then — dependencies,
    credential, Drive service, and finally any reader or API call.  Everything
    that could touch a credential or a registered byte sits below the guard, so
    an unapproved call performs zero authentication attempts rather than a
    failed one.  The notebook therefore has no auth code of its own to run: it
    calls this with ``adapter=None``.
    """
    if not open_registered_data:
        raise PrepNotApprovedError(
            f"OPEN_REGISTERED_DATA is False.  This is the default: a stray "
            f"import or notebook run cannot reach a registered asset.  "
            f"{APPROVAL_NOTE}")
    require_execution_approval(approval, f"the P1/P2 preflight over {out_dir!r}")
    if folder_id == ORIGINAL_CANONICAL_FOLDER_ID:
        # Named separately from the general refusal below.  This id is not a
        # typo or a stray folder — it is the eleven-file original, and it is
        # refused *because* P2 already read it on 2026-08-12 and stopped at
        # P2_DIRECTORY_CONTRACT_FAILED.  Re-running against it would reproduce
        # that stop and could be mistaken for a fresh finding, and it is not
        # what this rerun was approved for.  The folder stays untouched.
        raise PrepError(
            f"refusing to run: {folder_id!r} is the ORIGINAL canonical folder "
            f"{ORIGINAL_CANONICAL_RUN!r}, which holds eleven files and whose "
            f"P2 stop (P2_DIRECTORY_CONTRACT_FAILED, missing "
            f"'negative_control_null.npz') is already recorded and preserved.  "
            f"This rerun targets the corrective candidate "
            f"{CORRECTIVE_BUNDLE_FOLDER_ID!r} ({CORRECTIVE_BUNDLE_RUN}).  "
            f"Neither folder is modified by pointing at the other.")
    if folder_id != P2_TARGET_FOLDER_ID:
        raise PrepError(
            f"refusing to run: {folder_id!r} is not the corrective candidate "
            f"folder id {P2_TARGET_FOLDER_ID!r}.  The bundle is chosen by id, "
            f"never by name, by proximity or by size, and this is not a "
            f"general-purpose folder inspector.")
    emit("Q5-E PREP P1+P2: approval present; nothing has been opened yet.")
    emit(f"P2 target: {P2_TARGET_FOLDER_ID} ({P2_TARGET_RUN}) — the "
         f"preregistered corrective candidate, NOT the original canonical "
         f"{ORIGINAL_CANONICAL_FOLDER_ID}.")

    granted = _terminal_execution_guard()
    emit(f"read-only execution approval: granted {granted['granted_on']} by "
         f"{granted['granted_by']} — {granted['kind']}.")
    emit(f"not approved by it: {', '.join(granted['not_approved'])}.")

    # ---- Everything below is the complete, already-implemented preflight. --
    # It is unchanged by the execution-enable PR: opening the guard above is
    # the only thing that moved.
    auth_audit = None                                   # pragma: no cover
    if adapter is None:                                 # pragma: no cover
        adapter, auth_audit = build_drive_adapter(approval)
        emit(f"Drive scope proven read-only: "
             f"{auth_audit['exact_readonly_scope_proven']}")
    return execute_prep(                                # pragma: no cover
        mitdb_dir, folder_id, out_dir, adapter,
        mount_dir=mount_dir, approval=approval, timestamp=timestamp,
        emit=emit, synthetic=False, auth_audit=auth_audit)


def execute_prep(mitdb_dir: str, folder_id: str, out_dir: str,
                 adapter: DriveFolderAdapter, mount_dir: Optional[str] = None,
                 approval: Optional[str] = None, timestamp: str = "",
                 emit=print, synthetic: bool = False,
                 reader: Optional[LocalTreeReader] = None,
                 auth_audit: Optional[Mapping[str, object]] = None
                 ) -> Dict[str, object]:
    """Run both gates and write the bundle.  Shared by production and fixtures.

    A synthetic run must set ``synthetic=True``; the bundle is then stamped and
    is never an ingest candidate.
    """
    reader = reader or LocalTreeReader(approval)
    log: List[str] = [f"scope=P1+P2 synthetic={bool(synthetic)}"]

    p1 = run_p1(mitdb_dir, approval, reader=reader)
    log.append(f"P1 {p1['status']} first_failure={p1['first_failure']}")
    emit(f"P1: {p1['status']}")

    # P2 runs whatever P1 did: they are independent gates.
    p2 = run_p2(folder_id, adapter, approval, mount_dir=mount_dir,
                reader=reader)
    log.append(f"P2 {p2['status']} first_failure={p2['first_failure']}")
    emit(f"P2: {p2['status']}")

    combined = combine(p1, p2)
    log.append(f"combined {combined['status']}")
    emit(f"combined: {combined['status']}")

    directory = os.path.join(out_dir, f"{timestamp}_{RUN_SLUG}")
    written = write_bundle(
        directory, build_config(timestamp, synthetic, auth_audit),
        p1, p2, combined, log, synthetic=synthetic)

    # Validate the bundle the same way any later consumer must.  A run that
    # cannot verify its own output must not report a success: publication is
    # no longer an atomic rename, so "the directory is there" is not evidence
    # that it is complete.
    # The digest handed in is the one this run just computed, so the origin is
    # declared as exactly that.  The verifier then reports
    # `manifest_anchored_externally: False` and `acceptance_eligible: False`,
    # which is what the emitted lines below say too — an earlier version
    # returned True for both while printing that the external anchor was still
    # needed, and a machine verdict that contradicts its own prose is worse
    # than either alone.
    verified = verify_published_bundle(
        written["directory"],
        expected_manifest_sha256=written["manifest_sha256_freeze_externally"],
        manifest_anchor_source=ANCHOR_SAME_RUN)
    if not verified["ok"]:
        raise PrepError(
            f"the bundle at {written['directory']!r} does not pass the "
            f"consumer contract: {verified['problems']}.  It is left in place "
            f"for inspection and nothing was deleted.")
    emit(f"bundle committed, structure verified: "
         f"{verified['prep_payload_sha256']}")
    emit(f"manifest digest self-check: "
         f"{verified['manifest_digest_matches_expected']} "
         f"(source={verified['manifest_anchor_source']}, "
         f"externally anchored={verified['manifest_anchored_externally']})")
    emit(f"acceptance_eligible={verified['acceptance_eligible']}: it needs the "
         f"manifest digest from the saved report cell "
         f"({ANCHOR_SAVED_NOTEBOOK}) or the registration record "
         f"({ANCHOR_REGISTERED_RECORD}).")
    return {"p1": p1, "p2": p2, "combined": combined, "bundle": written,
            "verified": verified}


def module_capabilities() -> Tuple[str, ...]:
    """Names a notebook asserts before use, so a stale clone cannot masquerade."""
    return ("run_prep", "execute_prep", "run_p1", "run_p2", "combine",
            "registration_candidates", "write_bundle",
            "verify_published_bundle", "COMMIT_MARKER",
            "MANIFEST_ANCHOR_SOURCES", "EXTERNAL_MANIFEST_ANCHORS",
            "ANCHOR_SAME_RUN", "ANCHOR_SAVED_NOTEBOOK",
            "ANCHOR_REGISTERED_RECORD", "ANCHOR_NONE", "fold_file_triples",
            "DriveFolderAdapter", "GoogleDriveFolderAdapter",
            "LocalTreeReader", "normalise_child", "assert_no_credentials",
            "authenticate_drive_readonly", "build_drive_adapter",
            "audit_credential_scopes", "runtime_identity",
            "check_runtime_dependencies", "parse_sha256sums_text",
            "compare_against_publisher_list", "payload_files", "bundle_files",
            "design_card", "EXECUTION_APPROVAL_TOKEN", "DRIVE_READONLY_SCOPE",
            "EXECUTION_APPROVAL_RECORD", "PRIOR_EXECUTION_APPROVAL_RECORDS",
            "manifest_identity", "MANIFEST_IDENTITY_SOURCES",
            "CORRECTIVE_BUNDLE_FOLDER_ID", "CORRECTIVE_BUNDLE_RUN",
            "ORIGINAL_CANONICAL_FOLDER_ID", "ORIGINAL_CANONICAL_RUN",
            "P2_TARGET_FOLDER_ID", "P2_TARGET_RUN")


def _approval_line() -> str:
    if not EXECUTION_APPROVAL_RECORD.get("granted"):
        return "NOT APPROVED"
    return (f"APPROVED {EXECUTION_APPROVAL_RECORD['granted_on']} by "
            f"{EXECUTION_APPROVAL_RECORD['granted_by']} (read-only)")


def design_card() -> str:
    """A constants card that opens nothing.  Safe to print anywhere."""
    return "\n".join([
        f"{EXPERIMENT_ID} / {SUBSTAGE} - read-only preflight, not a result",
        f"  parent spec          : {SPEC_PATH}",
        f"  execution contract   : {CONTRACT_PATH}",
        f"  scope                : P1 + P2 (P3 is NOT in scope)",
        f"  P1 expected files    : {len(BJ.mitdb_expected_files())}",
        f"  P1 publisher-listed  : {MITDB_PUBLISHER_LISTED_FILES} "
        f"(+1 for the list itself = 147)",
        f"  P1 aggregate prefix  : {MITDB_REGISTERED_AGGREGATE_PREFIX}",
        f"  P2 target folder id  : {P2_TARGET_FOLDER_ID}  (corrective "
        f"candidate)",
        f"  P2 target run        : {P2_TARGET_RUN}",
        f"  original canonical   : {ORIGINAL_CANONICAL_FOLDER_ID}  "
        f"(11 files; refused as a target, untouched)",
        f"  candidate registered : False — registration is a separate PR",
        f"  P2 directory files   : {len(BJ.BUNDLE_FILES)}",
        f"  P2 Q5-E input files  : {len(BUNDLE_INPUT_FILES)}",
        f"  read-only execution  : {_approval_line()}",
        f"  token still required : {not execution_is_approved(None)}",
        "",
        "  This preflight registers nothing.  It emits candidate values; a",
        "  separate result-acceptance PR registers them after Codex review.",
        "",
        f"  {APPROVAL_NOTE}",
    ])


def main(argv: Optional[Sequence[str]] = None) -> int:    # pragma: no cover
    import argparse
    parser = argparse.ArgumentParser(
        description=f"{EXPERIMENT_ID} Q5-E PREP P1+P2")
    parser.add_argument(EXECUTION_APPROVAL_FLAG, action="store_true",
                        dest="approved")
    args = parser.parse_args(argv)
    print(design_card())
    if not args.approved:
        print(f"\nSKIP: {APPROVAL_NOTE}")
        return 2
    print("\nApproval flag present.  This CLI still runs nothing: the "
          "preflight is executed from the notebook, which supplies the "
          "mount paths and the output directory.")
    return 2


if __name__ == "__main__":                                # pragma: no cover
    raise SystemExit(main())
