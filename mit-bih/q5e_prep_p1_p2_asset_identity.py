#!/usr/bin/env python3
"""EXP-2026-008 / Q5-E — PREP P1 and P2: registered asset identity.

Two of the three items that currently stop a Q5-E run are asset identities
that have never been frozen:

* **P1** — the MIT-BIH publisher tree's full 64-hex aggregate.  The spec pins
  it only in truncated form (`0b46a411…`), and a truncated digest is not an
  execution contract.
* **P2** — the per-file SHA-256 of the five canonical Q5-D bundle files Q5-E
  reads, established from the **registered Drive folder id** rather than from
  a folder that merely has the right name.

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
# Approval.  Separate from the Q5-E audit token: approving this read-only
# preflight is not approving the audit, and the two must not be
# interchangeable.
# ─────────────────────────────────────────────────────────────────────────────
EXECUTION_APPROVAL_TOKEN = "q5e-prep-p1-p2-read-only-execution-approved-by-user"
EXECUTION_APPROVAL_FLAG = "--i-have-separate-prep-execution-approval"
#: Default closed.  A stray import or notebook run cannot reach an asset.
OPEN_REGISTERED_DATA = False
APPROVAL_NOTE = (
    "Approved: writing this PREP implementation (2026-08-12).  NOT approved: "
    "reading any registered Drive asset, calling the Drive API, computing any "
    "real digest, running P3, running detect_r(), aggregating M0-M4, or "
    "registering any value.  Read-only PREP execution needs its own separate "
    "user approval.")

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
# P2 — registered targets
# ─────────────────────────────────────────────────────────────────────────────
SOURCE_BUNDLE_RUN = Q5E.SOURCE_BUNDLE_RUN
SOURCE_BUNDLE_FOLDER_ID = Q5E.SOURCE_BUNDLE_FOLDER_ID
PRODUCING_CODE_SHA256 = Q5E.PRODUCING_CODE_SHA256
REGISTERED_RULE_FINGERPRINT = Q5E.REGISTERED_RULE_FINGERPRINT
SUPERSEDED_MARKER = Q5E.SUPERSEDED_MARKER
BUNDLE_INPUT_FILES = Q5E.BUNDLE_INPUT_FILES

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
    """Exactly what a run writes: the payload plus the manifest."""
    return tuple(sorted(set(payload_files(synthetic)) | {PREP_MANIFEST_FILE}))


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


def _terminal_execution_guard() -> None:
    """The single line a separately approved execution PR removes.

    It sits after every check and before the first registered read, so an
    approved run reaches a complete route and an unapproved one reaches
    nothing.  This PR does not remove it.
    """
    raise PrepError(
        "P1/P2 are implemented but have never been executed: reading the "
        "registered MIT-BIH tree or calling the Drive API needs a separate "
        f"read-only execution approval that does not exist yet.  "
        f"{APPROVAL_NOTE}")


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

    The client is built lazily inside the call, so importing this module
    reaches no network and needs no credentials.  The credential object is
    held here and is never written into a result.
    """

    __slots__ = ("approval", "_service")

    def __init__(self, approval: Optional[str], service=None) -> None:
        require_execution_approval(approval, "the Google Drive API")
        self.approval = approval
        self._service = service

    def _client(self):
        if self._service is None:
            require_execution_approval(self.approval, "the Google Drive API")
            from googleapiclient.discovery import build   # noqa: PLC0415
            self._service = build("drive", "v3")
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
}
#: Drive scope.  Read-only by contract: this preflight must be unable to
#: modify, move or delete anything even if a call were miswritten.
DRIVE_READONLY_SCOPE = "https://www.googleapis.com/auth/drive.readonly"


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


def authenticate_drive_readonly(approval: Optional[str],
                                authenticator=None, service_factory=None):
    """Authenticate and build a **read-only** Drive v3 service.

    Approval is checked before either step, so an unapproved notebook run
    performs zero authentication calls — not a failed one, none.  Both steps
    are injectable so the notebook path is testable without a real credential;
    production passes neither and gets Colab auth plus a real client.

    The returned service is handed to :class:`GoogleDriveFolderAdapter` and is
    never written into a result.
    """
    require_execution_approval(approval, "Google Drive authentication")
    report = check_runtime_dependencies()
    if authenticator is None and service_factory is None and report["missing"]:
        raise PrepError(
            f"refusing to authenticate: {report['missing']} are not "
            f"importable.  {report['note']}")
    if authenticator is None:                            # pragma: no cover
        from google.colab import auth                    # noqa: PLC0415
        authenticator = auth.authenticate_user
    authenticator()
    if service_factory is None:                          # pragma: no cover
        from googleapiclient.discovery import build      # noqa: PLC0415

        def service_factory():
            return build("drive", "v3")
    return service_factory()


def build_drive_adapter(approval: Optional[str], authenticator=None,
                        service_factory=None) -> "GoogleDriveFolderAdapter":
    """Authenticate, then hand the service to the adapter.

    This is the whole production auth path, complete now.  The execution
    approval PR removes the terminal guard and nothing else: it does not have
    to write authentication logic for the first time.
    """
    service = authenticate_drive_readonly(
        approval, authenticator=authenticator, service_factory=service_factory)
    return GoogleDriveFolderAdapter(approval, service=service)


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
    """Refuse to write anything that looks like a secret or a local path."""
    text = _canonical_json(payload) if not isinstance(payload, str) else payload
    lowered = text.lower()
    for key in CREDENTIAL_KEYS:
        if f'"{key}"' in lowered:
            raise PrepError(
                f"refusing to write {where}: it carries a {key!r} field.  "
                f"Credentials are not evidence and never enter a bundle.")


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
        out = {"prep": "P1", "ok": False, "status": reason,
               "first_failure": reason, "gates": gates,
               "gate_order": list(P1_GATE_ORDER),
               "tree_aggregate": None, "per_file": [],
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
    checksum_entry = reader.stat_and_hash(mitdb_dir, BJ.MITDB_CHECKSUM_FILE)
    observed_checksum = str(checksum_entry["sha256"])
    checksum_ok = observed_checksum == MITDB_CHECKSUM_FILE_SHA256
    gates.append({"gate": "checksum_file_digest", "ok": checksum_ok,
                  "file": BJ.MITDB_CHECKSUM_FILE,
                  "observed": observed_checksum,
                  "registered": MITDB_CHECKSUM_FILE_SHA256,
                  "files_read_so_far": 1})
    if not checksum_ok:
        # Nothing else is read.  A list that is not the registered list
        # verifies nothing, so hashing the other 146 files would be work done
        # in support of a conclusion that cannot be reached.
        return stop(P1_CHECKSUM_FILE_MISMATCH)

    # ---- gate 3: the publisher list over the other 146 files --------------
    others = [reader.stat_and_hash(mitdb_dir, name) for name in expected
              if name != BJ.MITDB_CHECKSUM_FILE]
    files = sorted([checksum_entry] + others, key=lambda f: str(f["name"]))
    published = BJ.verify_against_publisher_checksums(
        {"files": files}, mitdb_dir)
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
                  "problems": list(published.get("problems", ()))})
    if not publisher_ok:
        return stop(P1_PUBLISHER_MISMATCH)

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
        "seals": _p1_seals(),
    }


def _p1_seals() -> Dict[str, bool]:
    return {"detector_executed": False, "m0_m4_aggregated": False,
            "beat_join_executed": False, "model_scored": False,
            "probability_opened": False, "labels_opened": False,
            "training_performed": False, "bytes_hashed_only": True}


# ─────────────────────────────────────────────────────────────────────────────
# P2 — canonical Q5-D bundle identity, from the registered folder id
# ─────────────────────────────────────────────────────────────────────────────
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
               "folder_id": folder_id, "registered_run": SOURCE_BUNDLE_RUN,
               "inventory": inventory, "input_identity": None,
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

    # ---- gate 6: manifest identity ----------------------------------------
    try:
        manifest = json.loads(bytes_by_name["manifest.json"].decode("utf-8"))
    except (KeyError, UnicodeDecodeError, ValueError) as error:
        gates.append({"gate": "manifest_identity", "ok": False,
                      "problems": [f"manifest.json unreadable: {error}"]})
        return stop(P2_MANIFEST_MISMATCH)
    code = str(manifest.get("code_sha256") or "")
    fingerprint = str(manifest.get("rule_fingerprint") or "")
    problems = []
    if code != PRODUCING_CODE_SHA256:
        problems.append(f"code_sha256 {code!r} != registered")
    if fingerprint != REGISTERED_RULE_FINGERPRINT:
        problems.append(f"rule_fingerprint {fingerprint!r} != registered")
    gates.append({"gate": "manifest_identity", "ok": not problems,
                  "code_sha256": code, "rule_fingerprint": fingerprint,
                  "problems": problems})
    if problems:
        return stop(P2_MANIFEST_MISMATCH)

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
        "folder_id": folder_id, "registered_run": SOURCE_BUNDLE_RUN,
        "inventory": inventory,
        "directory_contract": {"n_expected": len(expected),
                               "missing": [], "unexpected": [],
                               "full_fold": fold_file_triples(full_files)},
        "manifest_identity": {"code_sha256": code,
                              "rule_fingerprint": fingerprint},
        "input_identity": {"files": input_files, "subset_fold": subset_fold},
        "bridge": bridge,
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
        observation_only=bool(p1.get("observation_only")),
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
        observation_note=(
            "computed after every P2 gate passed" if p2.get("ok")
            else "not computed: P2 stopped before the input-identity gate"))

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
def build_config(timestamp: str, synthetic: bool) -> Dict[str, object]:
    return {"experiment_id": EXPERIMENT_ID, "substage": SUBSTAGE,
            "run_slug": RUN_SLUG, "module_version": MODULE_VERSION,
            "timestamp": timestamp, "spec": SPEC_PATH,
            "contract": CONTRACT_PATH,
            "scope": ["P1", "P2"], "p3_in_scope": False,
            "synthetic_fixture": bool(synthetic),
            "ingestable": not synthetic,
            "registered_targets": {
                "mitdb_checksum_file_sha256": MITDB_CHECKSUM_FILE_SHA256,
                "mitdb_publisher_listed_files": MITDB_PUBLISHER_LISTED_FILES,
                "mitdb_registered_aggregate_prefix":
                    MITDB_REGISTERED_AGGREGATE_PREFIX,
                "source_bundle_run": SOURCE_BUNDLE_RUN,
                "source_bundle_folder_id": SOURCE_BUNDLE_FOLDER_ID,
                "producing_code_sha256": PRODUCING_CODE_SHA256,
                "rule_fingerprint": REGISTERED_RULE_FINGERPRINT},
            "approval_note": APPROVAL_NOTE}


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
    """Write the PREP bundle, then publish it by rename.

    Deliberately conservative about deletion.  An earlier draft removed a
    pre-existing staging directory and an empty final directory, and caught
    `BaseException` to clean up — all three could destroy someone else's files
    or a previous run's evidence.  Now: the staging directory is unique to this
    call, an existing final path is refused rather than removed, nothing
    pre-existing is deleted, and a failed run's partial staging is **kept** at
    a reported `.failed` path so it can be inspected.
    """
    if os.path.lexists(directory):
        raise PrepError(
            f"refusing to publish to {directory!r}: it already exists.  A PREP "
            f"bundle is new, never an overwrite, and this function does not "
            f"delete anything that is already there.")
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
    if os.path.islink(parent):
        raise PrepError(
            f"refusing to publish under {parent!r}: it is a symlink, and this "
            f"function does not follow links when writing or renaming")
    import tempfile                                        # noqa: PLC0415
    staging = tempfile.mkdtemp(
        prefix=f".{os.path.basename(os.path.abspath(directory))}.staging.",
        dir=parent)
    try:
        for name, value in payload.items():
            with open(os.path.join(staging, name), "w",
                      encoding="utf-8") as handle:
                json.dump(value, handle, indent=1, sort_keys=True)
        with open(os.path.join(staging, "log.txt"), "w",
                  encoding="utf-8") as handle:
            handle.write("\n".join(str(line) for line in log_lines) + "\n")
        summary = summary_markdown(combined, p1, p2, synthetic)
        with open(os.path.join(staging, "summary.md"), "w",
                  encoding="utf-8") as handle:
            handle.write(summary)
        if synthetic:
            with open(os.path.join(staging, SYNTHETIC_MARKER), "w",
                      encoding="utf-8") as handle:
                json.dump({"synthetic_fixture": True, "ingestable": False,
                           "reason": SYNTHETIC_NOTE}, handle, indent=1,
                          sort_keys=True)

        written = sorted(os.listdir(staging))
        if written != sorted(payload_names):
            raise PrepError(
                f"refusing to publish: the staged file set {written} is not "
                f"the contracted set {sorted(payload_names)}.  A file outside "
                f"the payload identity would be unaccounted for.")

        triples = []
        for name in written:
            path = os.path.join(staging, name)
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
            "note": ("manifest.json is excluded from the fold it records; its "
                     "own SHA-256 is frozen outside this bundle, in the "
                     "execution-contract Decision log and the registration "
                     "record"),
        }
        assert_no_credentials(manifest, PREP_MANIFEST_FILE)
        with open(os.path.join(staging, PREP_MANIFEST_FILE), "w",
                  encoding="utf-8") as handle:
            json.dump(manifest, handle, indent=1, sort_keys=True)

        final_set = sorted(os.listdir(staging))
        if final_set != sorted(bundle_files(synthetic)):
            raise PrepError(
                f"refusing to publish: final file set {final_set} != "
                f"{sorted(bundle_files(synthetic))}")
        with open(os.path.join(staging, PREP_MANIFEST_FILE), "rb") as handle:
            manifest_digest = _sha256_bytes(handle.read())

        # Same-parent rename: same filesystem, so the publish is atomic.
        os.rename(staging, directory)
    except Exception as error:
        # Keep the evidence.  A failed run's partial staging is more useful
        # than a clean directory, and deleting it is how a diagnosis gets
        # lost.  Only this call's own directory is ever touched.
        failed = f"{staging}.failed"
        try:
            os.rename(staging, failed)
        except OSError:                                    # pragma: no cover
            failed = staging
        raise PrepError(
            f"PREP bundle was not published: {error}.  The partial staging "
            f"directory is preserved at {failed!r} for inspection; nothing "
            f"was deleted.") from error
    return {"directory": directory, "written": final_set,
            "payload_files": list(payload_names),
            "prep_payload_sha256": fold,
            # Returned for external freezing; deliberately NOT inside the file.
            "manifest_sha256_freeze_externally": manifest_digest,
            "registration_allowed": bool(combined.get("registration_allowed"))}


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

    When no adapter is supplied, the approved route authenticates and builds a
    read-only Drive service itself — the auth path is complete here, so the
    execution-approval PR removes the guard and nothing else.
    """
    if not open_registered_data:
        raise PrepNotApprovedError(
            f"OPEN_REGISTERED_DATA is False.  This is the default: a stray "
            f"import or notebook run cannot reach a registered asset.  "
            f"{APPROVAL_NOTE}")
    require_execution_approval(approval, f"the P1/P2 preflight over {out_dir!r}")
    if folder_id != SOURCE_BUNDLE_FOLDER_ID:
        raise PrepError(
            f"refusing to run: {folder_id!r} is not the registered canonical "
            f"folder id {SOURCE_BUNDLE_FOLDER_ID!r}.  The bundle is chosen by "
            f"id, never by name or by proximity, and this is not a "
            f"general-purpose folder inspector.")
    emit("Q5-E PREP P1+P2: approval present; nothing has been opened yet.")

    _terminal_execution_guard()

    # ---- Everything below is the complete, already-implemented preflight. --
    # Removing the guard above is the *only* change a separately approved
    # execution PR makes here.
    return execute_prep(                                # pragma: no cover
        mitdb_dir, folder_id, out_dir,
        adapter or build_drive_adapter(approval),
        mount_dir=mount_dir, approval=approval, timestamp=timestamp,
        emit=emit, synthetic=False)


def execute_prep(mitdb_dir: str, folder_id: str, out_dir: str,
                 adapter: DriveFolderAdapter, mount_dir: Optional[str] = None,
                 approval: Optional[str] = None, timestamp: str = "",
                 emit=print, synthetic: bool = False,
                 reader: Optional[LocalTreeReader] = None
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
    written = write_bundle(directory, build_config(timestamp, synthetic),
                           p1, p2, combined, log, synthetic=synthetic)
    return {"p1": p1, "p2": p2, "combined": combined, "bundle": written}


def module_capabilities() -> Tuple[str, ...]:
    """Names a notebook asserts before use, so a stale clone cannot masquerade."""
    return ("run_prep", "execute_prep", "run_p1", "run_p2", "combine",
            "registration_candidates", "write_bundle", "fold_file_triples",
            "DriveFolderAdapter", "GoogleDriveFolderAdapter",
            "LocalTreeReader", "normalise_child", "assert_no_credentials",
            "authenticate_drive_readonly", "build_drive_adapter",
            "check_runtime_dependencies", "payload_files", "bundle_files",
            "design_card", "EXECUTION_APPROVAL_TOKEN")


def design_card() -> str:
    """A constants card that opens nothing.  Safe to print anywhere."""
    return "\n".join([
        f"{EXPERIMENT_ID} / {SUBSTAGE} - read-only preflight, not a result",
        f"  spec                 : {SPEC_PATH}",
        f"  scope                : P1 + P2 (P3 is NOT in scope)",
        f"  P1 expected files    : {len(BJ.mitdb_expected_files())}",
        f"  P1 publisher-listed  : {MITDB_PUBLISHER_LISTED_FILES} "
        f"(+1 for the list itself = 147)",
        f"  P1 aggregate prefix  : {MITDB_REGISTERED_AGGREGATE_PREFIX}",
        f"  P2 folder id         : {SOURCE_BUNDLE_FOLDER_ID}",
        f"  P2 directory files   : {len(BJ.BUNDLE_FILES)}",
        f"  P2 Q5-E input files  : {len(BUNDLE_INPUT_FILES)}",
        f"  execution approved   : {execution_is_approved(None)}",
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
    print("\nApproval flag present, but the terminal guard still refuses.")
    return 2


if __name__ == "__main__":                                # pragma: no cover
    raise SystemExit(main())
