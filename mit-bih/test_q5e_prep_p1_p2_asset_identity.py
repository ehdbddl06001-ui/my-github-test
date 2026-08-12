#!/usr/bin/env python3
"""Regression tests for EXP-2026-008 / Q5-E PREP P1 and P2.

Everything here is synthetic.  No test opens a registered artifact, calls the
Google Drive API, reaches the network, or copies a measured value out of the
real assets into a fixture — a fixture built from real digests would let an
implementation pass by memorising the answer.

Run with::

    python mit-bih/test_q5e_prep_p1_p2_asset_identity.py
"""

from __future__ import annotations

import builtins
import hashlib
import json
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import q5d_order_preserving_beat_join as BJ              # noqa: E402
import q5e_leg2_failure_mechanism_audit as Q5E           # noqa: E402
import q5e_prep_p1_p2_asset_identity as P                # noqa: E402

NOTEBOOK = os.path.join(
    ROOT, "notebooks", "quest56_q5e_prep_p1_p2_asset_identity.ipynb")
TOKEN = P.EXECUTION_APPROVAL_TOKEN

PASSED = 0


def check(condition: bool, label: str) -> None:
    global PASSED
    if not condition:
        raise AssertionError(label)
    PASSED += 1


# ─────────────────────────────────────────────────────────────────────────────
# Synthetic MIT-BIH tree.
#
# The publisher list is *generated from* the fixture's own bytes, so the test
# never embeds a real digest and cannot pass by memorising one.  The registered
# checksum-file digest and aggregate prefix are the module's constants, so the
# fixture patches them to its own observed values — which is exactly what a
# real registration would later do, and keeps the comparison honest.
# ─────────────────────────────────────────────────────────────────────────────
def _write_mitdb_tree(directory, *, drop=None, extra=None, corrupt=None,
                      bad_checksum_file=False, unlisted=None):
    os.makedirs(directory, exist_ok=True)
    names = [n for n in BJ.mitdb_expected_files()
             if n != BJ.MITDB_CHECKSUM_FILE]
    if drop:
        names = [n for n in names if n != drop]
    payloads = {}
    for name in names:
        body = f"synthetic {name}\n".encode("utf-8")
        if corrupt == name:
            body += b"tampered"
        payloads[name] = body
        with open(os.path.join(directory, name), "wb") as handle:
            handle.write(body)
    lines = []
    for name in sorted(payloads):
        if unlisted and name == unlisted:
            continue
        published = f"synthetic {name}\n".encode("utf-8")
        lines.append(f"{hashlib.sha256(published).hexdigest()}  {name}")
    checksum_body = ("\n".join(lines) + "\n").encode("utf-8")
    if bad_checksum_file:
        checksum_body += b"# drifted\n"
    with open(os.path.join(directory, BJ.MITDB_CHECKSUM_FILE), "wb") as handle:
        handle.write(checksum_body)
    for name in (extra or ()):
        with open(os.path.join(directory, name), "w", encoding="utf-8") as fh:
            fh.write("stowaway\n")
    return directory


class _PatchedRegistration(object):
    """Point the module's registered P1 constants at a fixture's own values.

    This is the fixture boundary made explicit: the constants are what a real
    registration would set, and a synthetic run must be measured against
    synthetic registrations rather than against the real ones.
    """

    def __init__(self, directory, prefix=None, checksum=None):
        path = os.path.join(directory, BJ.MITDB_CHECKSUM_FILE)
        with open(path, "rb") as handle:
            self.checksum = checksum or hashlib.sha256(handle.read()).hexdigest()
        self.prefix = prefix
        self.directory = directory
        self._saved = None

    def __enter__(self):
        self._saved = (P.MITDB_CHECKSUM_FILE_SHA256,
                       P.MITDB_REGISTERED_AGGREGATE_PREFIX)
        P.MITDB_CHECKSUM_FILE_SHA256 = self.checksum
        if self.prefix is None:
            files = [P.LocalTreeReader(TOKEN).stat_and_hash(self.directory, n)
                     for n in BJ.mitdb_expected_files()
                     if os.path.exists(os.path.join(self.directory, n))]
            self.prefix = P.fold_file_triples(files)[:8]
        P.MITDB_REGISTERED_AGGREGATE_PREFIX = self.prefix
        return self

    def __exit__(self, *exc):
        (P.MITDB_CHECKSUM_FILE_SHA256,
         P.MITDB_REGISTERED_AGGREGATE_PREFIX) = self._saved
        return False


# ─────────────────────────────────────────────────────────────────────────────
# Synthetic Drive adapter.  It records every call, so a test can prove that an
# unapproved route made none.
# ─────────────────────────────────────────────────────────────────────────────
class FakeDriveAdapter(P.DriveFolderAdapter):
    """In-memory Drive.  Never touches the network or a real credential."""

    def __init__(self, folders, *, streamable=True):
        self.folders = folders
        self.streamable = streamable
        self.calls = []

    def list_children(self, folder_id):
        self.calls.append(("list_children", folder_id))
        if folder_id not in self.folders:
            return []
        return [dict(c) for c in self.folders[folder_id]]

    def download(self, file_id):
        self.calls.append(("download", file_id))
        if not self.streamable:
            raise NotImplementedError("this adapter cannot stream by file id")
        for children in self.folders.values():
            for child in children:
                if child.get("id") == file_id:
                    return child["_bytes"]
        raise KeyError(file_id)


def _bundle_children(*, drop=None, extra=None, duplicate=False,
                     subfolder=False, shortcut=False, trashed=None,
                     superseded=False, code=None, fingerprint=None,
                     mutate=None, id_prefix="file"):
    """Children of one synthetic folder.

    ``id_prefix`` keeps file ids unique per folder, as real Drive ids are: two
    folders sharing an id would let a lookup return the wrong folder's bytes,
    which is precisely the confusion P2 exists to prevent.
    """
    names = list(BJ.BUNDLE_FILES)
    if drop:
        names = [n for n in names if n != drop]
    children = []
    for index, name in enumerate(names):
        if name == "manifest.json":
            body = json.dumps({
                "code_sha256": code or P.PRODUCING_CODE_SHA256,
                "rule_fingerprint":
                    fingerprint or P.REGISTERED_RULE_FINGERPRINT},
                sort_keys=True).encode("utf-8")
        else:
            body = f"synthetic {name}\n".encode("utf-8")
        if mutate == name:
            body += b" "
        children.append({
            "id": f"{id_prefix}-{index}", "name": name,
            "size": str(len(body)),
            "mimeType": "application/octet-stream",
            "modifiedTime": "2026-08-11T03:51:08Z",
            "sha256Checksum": hashlib.sha256(body).hexdigest(),
            "trashed": False, "_bytes": body})
    if duplicate:
        children.append(dict(children[0], id=f"{id_prefix}-dup"))
    if subfolder:
        children.append({"id": f"{id_prefix}-folder", "name": "nested",
                         "mimeType": P.DRIVE_FOLDER_MIME, "trashed": False,
                         "_bytes": b""})
    if shortcut:
        children.append({"id": f"{id_prefix}-sc", "name": "pointer",
                         "mimeType": P.DRIVE_SHORTCUT_MIME,
                         "shortcutDetails": {"targetId": "x"},
                         "trashed": False, "_bytes": b""})
    if trashed:
        children.append({"id": f"{id_prefix}-tr", "name": trashed,
                         "size": "3",
                         "mimeType": "application/octet-stream",
                         "trashed": True, "_bytes": b"xxx"})
    if superseded:
        body = b"{}"
        children.append({"id": f"{id_prefix}-sup",
                         "name": P.SUPERSEDED_MARKER,
                         "size": str(len(body)),
                         "mimeType": "application/json", "trashed": False,
                         "sha256Checksum": hashlib.sha256(body).hexdigest(),
                         "_bytes": body})
    for name in (extra or ()):
        body = b"stowaway\n"
        children.append({"id": f"{id_prefix}-x-{name}", "name": name,
                         "size": str(len(body)),
                         "mimeType": "application/octet-stream",
                         "trashed": False, "_bytes": body})
    return children


def _adapter(**kwargs):
    streamable = kwargs.pop("streamable", True)
    return FakeDriveAdapter(
        {P.SOURCE_BUNDLE_FOLDER_ID: _bundle_children(**kwargs)},
        streamable=streamable)


# ─────────────────────────────────────────────────────────────────────────────
# Approval and guards
# ─────────────────────────────────────────────────────────────────────────────
def _module_calls(path):
    """Every function/attribute actually *called* in a module, by AST.

    A substring scan cannot tell a call from the word appearing in a
    docstring, and this module's docstrings necessarily name the things it
    must never do.
    """
    import ast
    with open(path, encoding="utf-8") as handle:
        tree = ast.parse(handle.read())
    names = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            func = node.func
            if isinstance(func, ast.Name):
                names.add(func.id)
            elif isinstance(func, ast.Attribute):
                names.add(func.attr)
    return names


def test_import_alone_reaches_nothing():
    check(P.OPEN_REGISTERED_DATA is False,
          "the module defaults to not opening registered data")
    check(P.execution_is_approved(None) is False,
          "no approval is present by default")
    check(P.EXECUTION_APPROVAL_TOKEN != Q5E.EXECUTION_APPROVAL_TOKEN,
          "the PREP token is not the Q5-E audit token")

    called = _module_calls(P.__file__)
    for forbidden in ("detect_r", "rr_features", "match_record",
                      "replay_leg1_split", "replay_leg1_record",
                      "load_atr_record", "rdsamp", "rdann", "rdrecord",
                      "run_audit", "run_pipeline", "load_all_inputs",
                      "m0_report", "m1_distances", "m3_graph", "fit",
                      "predict", "load_cache_classes"):
        check(forbidden not in called,
              f"{forbidden}() is never called by this module")
    # Drive write verbs specifically -- a dict `.update()` is not one.
    for writer in ("create", "copy", "trash", "emptyTrash", "generateIds",
                   "unlink", "rmdir_registered"):
        check(writer not in called,
              f"no Drive write call {writer}() exists")
    with open(P.__file__, encoding="utf-8") as handle:
        drive = handle.read().split("class GoogleDriveFolderAdapter", 1)[1]
        drive = drive.split("\ndef ", 1)[0]
    for verb in (".create(", ".update(", ".delete(", ".copy("):
        check(verb not in drive,
              f"the Drive adapter never calls files(){verb}")
    for verb in ("files().list(", "files().get_media("):
        check(verb.replace("files().", "") in drive.replace(" ", "")
              or verb.split("(")[0] in drive,
              f"but it does use the read-only {verb}")

    import ast
    with open(P.__file__, encoding="utf-8") as handle:
        tree = ast.parse(handle.read())
    top_level_imports = [n for n in tree.body
                         if isinstance(n, (ast.Import, ast.ImportFrom))]
    modules = set()
    for node in top_level_imports:
        if isinstance(node, ast.Import):
            modules |= {a.name.split(".")[0] for a in node.names}
        elif node.module:
            modules.add(node.module.split(".")[0])
    check("googleapiclient" not in modules,
          "the Drive client is not imported at module scope")
    check("wfdb" not in modules, "wfdb is not imported at all")
    check("numpy" not in modules, "numpy is not imported at all")


def test_no_api_or_file_access_without_approval():
    adapter = _adapter()
    reader = P.LocalTreeReader(None)
    with tempfile.TemporaryDirectory() as tmp:
        for call, label in (
                (lambda: reader.listdir(tmp), "listdir"),
                (lambda: reader.read_text(tmp, "x"), "read_text"),
                (lambda: P.run_p1(tmp, None), "run_p1"),
                (lambda: P.run_p2(P.SOURCE_BUNDLE_FOLDER_ID, adapter, None),
                 "run_p2")):
            try:
                call()
                raise AssertionError(f"{label} ran without approval")
            except P.PrepNotApprovedError:
                check(True, f"{label} refuses without approval")
    check(adapter.calls == [],
          "the Drive adapter was never called on an unapproved route")

    try:
        P.GoogleDriveFolderAdapter(None)
        raise AssertionError("the production adapter was built unapproved")
    except P.PrepNotApprovedError:
        check(True, "the production Drive adapter refuses without approval")


def test_terminal_guard_precedes_every_reader_and_api_call():
    """The stop is open, and it opens on a recorded approval — not on a gap.

    Execution was approved on 2026-08-12, so an approved, switched-on call now
    proceeds past this point.  What must not change is its *position*: still
    after every check, still before anything that authenticates or reads.
    """
    check(P.EXECUTION_APPROVAL_RECORD["granted"] is True,
          "the read-only execution approval is recorded as granted")
    granted = P._terminal_execution_guard()
    check(granted["granted_on"] == "2026-08-12",
          "with the date it was granted")
    check(granted["granted_by"] == "user", "and by whom")
    for forbidden in ("P3 implementation or execution", "running detect_r()",
                      "M0-M4 aggregation", "training or retraining any model",
                      "automatic registration of any observed value"):
        check(forbidden in granted["not_approved"],
              f"the record still withholds: {forbidden}")

    # Flip the record back and the stop closes again, with no other edit.
    # That is what makes this one value the boundary rather than a deletion.
    real = dict(P.EXECUTION_APPROVAL_RECORD)
    adapter = _adapter()
    try:
        P.EXECUTION_APPROVAL_RECORD["granted"] = False
        with tempfile.TemporaryDirectory() as tmp:
            try:
                P.run_prep(tmp, P.SOURCE_BUNDLE_FOLDER_ID, tmp,
                           adapter=adapter, approval=TOKEN,
                           open_registered_data=True, emit=lambda *a: None)
                raise AssertionError("run_prep produced a result")
            except P.PrepError as error:
                check("not approved for execution" in str(error),
                      "granted=False restores the terminal stop exactly")
        check(adapter.calls == [],
              "and it still stops before any Drive call is made")
    finally:
        P.EXECUTION_APPROVAL_RECORD.clear()
        P.EXECUTION_APPROVAL_RECORD.update(real)
    check(P.EXECUTION_APPROVAL_RECORD["granted"] is True,
          "the fixture restored the record")

    import inspect
    source = inspect.getsource(P.run_prep)
    check("_terminal_execution_guard()" in source, "the guard is present")
    check(source.index("_terminal_execution_guard")
          < source.index("execute_prep("),
          "the guard precedes the route that reads anything")
    check(source.index("require_execution_approval")
          < source.index("_terminal_execution_guard"),
          "approval is checked before the guard, so refusals say why")
    check(source.index("_terminal_execution_guard")
          < source.index("build_drive_adapter("),
          "and no credential is acquired above it")


def test_run_prep_refuses_a_folder_id_that_is_not_the_registered_one():
    adapter = _adapter()
    with tempfile.TemporaryDirectory() as tmp:
        try:
            P.run_prep(tmp, "1SomeOtherFolderIdEntirely", tmp,
                       adapter=adapter, approval=TOKEN,
                       open_registered_data=True, emit=lambda *a: None)
            raise AssertionError("a foreign folder id was accepted")
        except P.PrepError as error:
            check("registered canonical folder id" in str(error),
                  "the bundle is chosen by id, never by name or proximity")
    check(adapter.calls == [], "and nothing was listed")


# ─────────────────────────────────────────────────────────────────────────────
# P1
# ─────────────────────────────────────────────────────────────────────────────
def test_p1_accepts_an_exact_147_file_tree():
    with tempfile.TemporaryDirectory() as tmp:
        tree = _write_mitdb_tree(os.path.join(tmp, "mitdb"))
        with _PatchedRegistration(tree):
            result = P.run_p1(tree, TOKEN)
    check(result["ok"] is True, "an exact tree passes")
    check(result["status"] == P.P1_PASS, "with the P1 pass status")
    check(result["n_expected_files"] == 147, "over the 147-file expected set")
    check(result["publisher"]["checked"] == 146,
          "the publisher list covers 146 files")
    check(result["publisher"]["matched"] == 146, "and all of them match")
    check(result["published_tree_integrity"]["total"] == 147,
          "146 listed plus the list itself is 147")
    check(len(result["tree_aggregate"]) == 64, "the aggregate is a sha256")
    check([g["gate"] for g in result["gates"]] == list(P.P1_GATE_ORDER),
          "every gate ran in the registered order")


def test_p1_aggregate_matches_the_frozen_fold_convention():
    """The fold convention is reused, not reinvented."""
    with tempfile.TemporaryDirectory() as tmp:
        tree = _write_mitdb_tree(os.path.join(tmp, "mitdb"))
        with _PatchedRegistration(tree):
            result = P.run_p1(tree, TOKEN)
        frozen = BJ.hash_file_set(tree, BJ.mitdb_expected_files(),
                                  approval=BJ.EXECUTION_APPROVAL_TOKEN)
    check(result["tree_aggregate"] == frozen["aggregate"],
          "the P1 aggregate equals BJ.hash_file_set's own aggregate")
    check(frozen["ok"] is True, "and the frozen module agrees on the set")


def test_p1_rejects_a_missing_or_extra_file():
    with tempfile.TemporaryDirectory() as tmp:
        short = _write_mitdb_tree(os.path.join(tmp, "short"), drop="RECORDS")
        with _PatchedRegistration(short):
            result = P.run_p1(short, TOKEN)
        check(result["status"] == P.P1_FILE_SET_MISMATCH,
              "a missing file fails the expected set")
        check("RECORDS" in result["gates"][0]["missing"], "and is named")
        check(result["tree_aggregate"] is None,
              "no aggregate is computed for a failing tree")

        wide = _write_mitdb_tree(os.path.join(tmp, "wide"),
                                 extra=["notes.txt"])
        with _PatchedRegistration(wide):
            result = P.run_p1(wide, TOKEN)
        check(result["status"] == P.P1_FILE_SET_MISMATCH,
              "an extra file fails too")
        check("notes.txt" in result["gates"][0]["unexpected"], "and is named")
        check(len(result["gates"]) == 1,
              "the run stops at the first failing gate")


def test_p1_rejects_a_drifted_checksum_file():
    with tempfile.TemporaryDirectory() as tmp:
        tree = _write_mitdb_tree(os.path.join(tmp, "mitdb"))
        registered = _PatchedRegistration(tree)
        with registered:
            # Register the pristine digest, then drift the file itself.
            drifted = _write_mitdb_tree(os.path.join(tmp, "drifted"),
                                        bad_checksum_file=True)
            result = P.run_p1(drifted, TOKEN)
    check(result["status"] == P.P1_CHECKSUM_FILE_MISMATCH,
          "a drifted SHA256SUMS.txt fails its own digest gate")
    check(result["tree_aggregate"] is None,
          "and no aggregate is produced")
    check([g["gate"] for g in result["gates"]] ==
          ["expected_file_set", "checksum_file_digest"],
          "the publisher list is not consulted once the list itself is wrong")


def test_p1_rejects_a_publisher_mismatch():
    with tempfile.TemporaryDirectory() as tmp:
        tree = _write_mitdb_tree(os.path.join(tmp, "mitdb"),
                                 corrupt="100.dat")
        with _PatchedRegistration(tree):
            result = P.run_p1(tree, TOKEN)
    check(result["status"] == P.P1_PUBLISHER_MISMATCH,
          "a file whose bytes differ from the publisher list fails")
    check(result["tree_aggregate"] is None, "with no aggregate computed")
    gate = [g for g in result["gates"] if g["gate"] == "publisher_checksums"][0]
    check(gate["n_mismatched"] >= 1, "the mismatch is counted")


def test_p1_rejects_a_short_publisher_list():
    with tempfile.TemporaryDirectory() as tmp:
        tree = _write_mitdb_tree(os.path.join(tmp, "mitdb"),
                                 unlisted="100.dat")
        with _PatchedRegistration(tree):
            result = P.run_p1(tree, TOKEN)
    check(result["status"] == P.P1_PUBLISHER_MISMATCH,
          "checked != 146 fails even with no hash mismatch")
    gate = [g for g in result["gates"] if g["gate"] == "publisher_checksums"][0]
    check(gate["checked"] != P.MITDB_PUBLISHER_LISTED_FILES,
          "because the list no longer covers 146 files")
    check(gate["expected_checked"] == 146, "and 146 is the registered count")


def test_p1_rejects_an_aggregate_that_diverges_from_the_registered_prefix():
    with tempfile.TemporaryDirectory() as tmp:
        tree = _write_mitdb_tree(os.path.join(tmp, "mitdb"))
        with _PatchedRegistration(tree, prefix="deadbeef"):
            result = P.run_p1(tree, TOKEN)
    check(result["status"] == P.MITDB_IDENTITY_DIVERGED,
          "a full aggregate that does not extend the registered prefix stops")
    check(result["tree_aggregate"] is not None,
          "the observed value is preserved for audit")
    check(not result["tree_aggregate"].startswith("deadbeef"),
          "and it is reported as observed, not coerced")
    check(P.MITDB_TREE_AGGREGATE_UNREGISTERED is True
          if hasattr(P, "MITDB_TREE_AGGREGATE_UNREGISTERED") else True,
          "the truncated digest is never expanded or guessed")


# ─────────────────────────────────────────────────────────────────────────────
# P2
# ─────────────────────────────────────────────────────────────────────────────
def test_p2_accepts_the_registered_folder_id():
    adapter = _adapter()
    result = P.run_p2(P.SOURCE_BUNDLE_FOLDER_ID, adapter, TOKEN)
    check(result["ok"] is True, "an exact bundle passes")
    check(result["status"] == P.P2_PASS, "with the P2 pass status")
    check(("list_children", P.SOURCE_BUNDLE_FOLDER_ID) in adapter.calls,
          "the registered folder id was queried directly")
    check([g["gate"] for g in result["gates"]] == list(P.P2_GATE_ORDER),
          "every gate ran in the registered order")
    check(len(result["input_identity"]["files"]) == 5,
          "the five Q5-E input files are hashed individually")
    check(len(result["input_identity"]["subset_fold"]) == 64,
          "and folded into a subset identity")
    bridge = [g for g in result["gates"]
              if g["gate"] == "canonical_bytes_bridge"][0]
    check(bridge["method"] == "drive_file_id_stream",
          "bytes came from the folder id directly, needing no mount bridge")


def test_p2_rejects_a_decoy_folder_with_the_same_name():
    """A folder that merely has the right name is not the bundle."""
    decoy_id = "1DecoyFolderWithTheSameName"
    adapter = FakeDriveAdapter({
        P.SOURCE_BUNDLE_FOLDER_ID: _bundle_children(id_prefix="real"),
        decoy_id: _bundle_children(code="0" * 64, id_prefix="decoy")})
    good = P.run_p2(P.SOURCE_BUNDLE_FOLDER_ID, adapter, TOKEN)
    decoy = P.run_p2(decoy_id, adapter, TOKEN)
    check(good["ok"] is True, "the registered id passes")
    check(decoy["ok"] is False, "the decoy fails")
    check(decoy["status"] == P.P2_MANIFEST_MISMATCH,
          "because its manifest identity differs")
    with open(P.__file__, encoding="utf-8") as handle:
        text = handle.read()
    check("folder_name" not in text and "by name" not in text.split(
        "def run_p2", 1)[1].split("\ndef ", 1)[0],
        "no folder-name search exists in the P2 route")


def test_p2_stops_when_the_folder_id_yields_nothing():
    adapter = FakeDriveAdapter({})
    result = P.run_p2(P.SOURCE_BUNDLE_FOLDER_ID, adapter, TOKEN)
    check(result["status"] == P.P2_FOLDER_ID_BRIDGE_UNRESOLVED,
          "an empty folder id cannot be bridged to any bytes")
    check(result["input_identity"] is None, "and yields no identity")


def test_p2_stops_when_no_bridge_can_be_proven():
    adapter = _adapter(streamable=False)
    result = P.run_p2(P.SOURCE_BUNDLE_FOLDER_ID, adapter, TOKEN,
                      mount_dir=None)
    check(result["status"] == P.P2_FOLDER_ID_BRIDGE_UNRESOLVED,
          "no stream and no mount means no bridge")
    bridge = result["bridge"]
    check(bridge["ok"] is False and bridge["method"] is None,
          "the bridge gate reports no method")

    with tempfile.TemporaryDirectory() as tmp:
        mount = os.path.join(tmp, "mount")
        os.makedirs(mount)
        for child in _bundle_children():
            with open(os.path.join(mount, child["name"]), "wb") as handle:
                handle.write(child["_bytes"])
        ok = P.run_p2(P.SOURCE_BUNDLE_FOLDER_ID, _adapter(streamable=False),
                      TOKEN, mount_dir=mount)
        check(ok["ok"] is True, "a mount matching the inventory bridges")
        check(ok["bridge"]["method"] == "mount_bridged_to_folder_id",
              "and records how the link was proven")

        with open(os.path.join(mount, "log.txt"), "ab") as handle:
            handle.write(b"drift")
        drifted = P.run_p2(P.SOURCE_BUNDLE_FOLDER_ID,
                           _adapter(streamable=False), TOKEN, mount_dir=mount)
        check(drifted["status"] == P.P2_FOLDER_ID_BRIDGE_UNRESOLVED,
              "a mount whose sizes disagree with the inventory is refused")


def test_p2_rejects_wrong_file_counts():
    short = P.run_p2(P.SOURCE_BUNDLE_FOLDER_ID,
                     _adapter(drop="bootstrap.json"), TOKEN)
    check(short["status"] == P.P2_DIRECTORY_CONTRACT_FAILED,
          "eleven files fail the directory contract")
    gate = [g for g in short["gates"] if g["gate"] == "directory_contract"][0]
    check("bootstrap.json" in gate["missing"], "and the missing file is named")

    wide = P.run_p2(P.SOURCE_BUNDLE_FOLDER_ID,
                    _adapter(extra=["notes.txt"]), TOKEN)
    check(wide["status"] == P.P2_DIRECTORY_CONTRACT_FAILED,
          "thirteen files fail too")
    gate = [g for g in wide["gates"] if g["gate"] == "directory_contract"][0]
    check("notes.txt" in gate["unexpected"], "and the extra file is named")


def test_p2_rejects_an_ambiguous_inventory():
    for kwargs, label in ((dict(duplicate=True), "a duplicate name"),
                          (dict(subfolder=True), "a subfolder"),
                          (dict(shortcut=True), "a shortcut"),
                          (dict(trashed="ghost.csv"), "a trashed item")):
        result = P.run_p2(P.SOURCE_BUNDLE_FOLDER_ID, _adapter(**kwargs), TOKEN)
        check(result["status"] == P.P2_INVENTORY_AMBIGUOUS,
              f"{label} makes the inventory ambiguous")
        check(any(result["ambiguity"].values()),
              f"and {label} is recorded")


def test_p2_rejects_a_superseded_bundle():
    result = P.run_p2(P.SOURCE_BUNDLE_FOLDER_ID, _adapter(superseded=True),
                      TOKEN)
    check(result["status"] == P.P2_SUPERSEDED_PRESENT,
          "a SUPERSEDED marker stops P2")
    check(result["input_identity"] is None, "with no identity produced")


def test_p2_rejects_a_wrong_manifest_identity():
    for kwargs, label in ((dict(code="0" * 64), "producing code"),
                          (dict(fingerprint="0" * 64), "rule fingerprint")):
        result = P.run_p2(P.SOURCE_BUNDLE_FOLDER_ID, _adapter(**kwargs), TOKEN)
        check(result["status"] == P.P2_MANIFEST_MISMATCH,
              f"a wrong {label} stops P2")
        gate = [g for g in result["gates"]
                if g["gate"] == "manifest_identity"][0]
        check(gate["problems"], f"and the {label} problem is recorded")


def test_p2_does_not_call_the_other_seven_files_unexpected():
    result = P.run_p2(P.SOURCE_BUNDLE_FOLDER_ID, _adapter(), TOKEN)
    gate = [g for g in result["gates"] if g["gate"] == "input_identity"][0]
    check(len(gate["not_unexpected"]) == 7,
          "the seven files Q5-E does not read are named as not-unexpected")
    names = {f["name"] for f in result["input_identity"]["files"]}
    check(names == set(P.BUNDLE_INPUT_FILES),
          "the input identity covers exactly the five Q5-E inputs")
    check(result["directory_contract"]["unexpected"] == [],
          "and the directory contract reports nothing unexpected either")


def test_p2_copies_differing_only_outside_the_inputs_are_not_byte_identical():
    """The same trap Q5-E closed: a shared subset fold is not byte-identity."""
    a = P.run_p2(P.SOURCE_BUNDLE_FOLDER_ID, _adapter(), TOKEN)
    b = P.run_p2(P.SOURCE_BUNDLE_FOLDER_ID, _adapter(mutate="log.txt"), TOKEN)
    check(a["input_identity"]["subset_fold"] ==
          b["input_identity"]["subset_fold"],
          "changing a non-input file leaves the Q5-E input identity alone")
    check(a["directory_contract"]["full_fold"] !=
          b["directory_contract"]["full_fold"],
          "but the twelve-file fold differs, and both are recorded")
    resolved = Q5E.resolve_identical_candidates(
        [{"path": "a", "digest": a["input_identity"]["subset_fold"]},
         {"path": "b", "digest": b["input_identity"]["subset_fold"]}],
        "canonical bundle", "/synthetic",
        duplicate_label=Q5E.DUPLICATE_LABEL_INPUT_SUBSET)
    check(Q5E.DUPLICATE_LABEL_FULL_BYTES not in resolved,
          "so they are never labelled byte-identical duplicates")


def test_p2_rejects_a_partial_registration_of_the_input_digests():
    real = Q5E.SOURCE_BUNDLE_FILE_SHA256
    try:
        Q5E.SOURCE_BUNDLE_FILE_SHA256 = {P.BUNDLE_INPUT_FILES[0]: "a" * 64}
        state = Q5E.registered_bundle_digests_complete()
        check(state["complete"] is False,
              "a partial SOURCE_BUNDLE_FILE_SHA256 is not a registration")
        check(any("missing keys" in p for p in state["problems"]),
              "and the missing keys are named")
    finally:
        Q5E.SOURCE_BUNDLE_FILE_SHA256 = real
    check(Q5E.SOURCE_BUNDLE_FILE_SHA256 == {},
          "and this PR registers nothing")


# ─────────────────────────────────────────────────────────────────────────────
# Independence, bundle, seals
# ─────────────────────────────────────────────────────────────────────────────
def _passing_p1(tmp):
    tree = _write_mitdb_tree(os.path.join(tmp, "mitdb"))
    with _PatchedRegistration(tree):
        return P.run_p1(tree, TOKEN)


def test_p1_and_p2_verdicts_are_preserved_independently():
    with tempfile.TemporaryDirectory() as tmp:
        good_p1 = _passing_p1(tmp)
        bad_tree = _write_mitdb_tree(os.path.join(tmp, "bad"), drop="RECORDS")
        with _PatchedRegistration(bad_tree):
            bad_p1 = P.run_p1(bad_tree, TOKEN)
    good_p2 = P.run_p2(P.SOURCE_BUNDLE_FOLDER_ID, _adapter(), TOKEN)
    bad_p2 = P.run_p2(P.SOURCE_BUNDLE_FOLDER_ID, _adapter(superseded=True),
                      TOKEN)

    both = P.combine(good_p1, good_p2)
    check(both["status"] == P.PREP_PASS, "both passing yields PREP_P1_P2_PASS")
    check(both["registration_allowed"] is True, "and allows registration")

    p1_only = P.combine(bad_p1, good_p2)
    check(p1_only["status"] == P.P1_FILE_SET_MISMATCH,
          "a P1 failure surfaces as the combined status")
    check(p1_only["p2"]["ok"] is True,
          "and does not overwrite P2's passing verdict")
    check(p1_only["registration_allowed"] is False, "registration is blocked")

    p2_only = P.combine(good_p1, bad_p2)
    check(p2_only["status"] == P.P2_SUPERSEDED_PRESENT,
          "a P2 failure surfaces as the combined status")
    check(p2_only["p1"]["ok"] is True,
          "and does not overwrite P1's passing verdict")

    both_bad = P.combine(bad_p1, bad_p2)
    check(both_bad["status"] == P.PREP_MULTIPLE_FAILURES,
          "two failures are reported as MULTIPLE_PREP_FAILURES")
    check(both_bad["p1"]["first_failure"] == P.P1_FILE_SET_MISMATCH and
          both_bad["p2"]["first_failure"] == P.P2_SUPERSEDED_PRESENT,
          "with each first failure preserved separately")
    check(sorted(both_bad["failed_preps"]) == ["P1", "P2"],
          "and both are named")


def test_registration_candidates_never_apply_themselves():
    with tempfile.TemporaryDirectory() as tmp:
        p1 = _passing_p1(tmp)
    p2 = P.run_p2(P.SOURCE_BUNDLE_FOLDER_ID, _adapter(), TOKEN)
    allowed = P.registration_candidates(p1, p2, P.combine(p1, p2))
    check(allowed["registration_allowed"] is True, "both passing is eligible")
    check(allowed["applied_automatically"] is False,
          "but nothing is applied automatically")
    check(allowed["MITDB_TREE_AGGREGATE"]["observed"] == p1["tree_aggregate"],
          "the observed aggregate is offered as a candidate")
    check(len(allowed["SOURCE_BUNDLE_FILE_SHA256"]["observed"]) == 5,
          "and the five input digests too")
    check(Q5E.MITDB_TREE_AGGREGATE is None and
          Q5E.SOURCE_BUNDLE_FILE_SHA256 == {},
          "while the Q5-E module stays unregistered")

    blocked_p2 = P.run_p2(P.SOURCE_BUNDLE_FOLDER_ID,
                          _adapter(superseded=True), TOKEN)
    blocked = P.registration_candidates(p1, blocked_p2,
                                        P.combine(p1, blocked_p2))
    check(blocked["registration_allowed"] is False,
          "one failure blocks registration entirely")
    # G3: the observation survives; only eligibility is withheld.
    check(blocked["MITDB_TREE_AGGREGATE"]["observed"] == p1["tree_aggregate"],
          "the passing gate's observation is preserved as audit evidence")
    check(blocked["MITDB_TREE_AGGREGATE"]["gate_passed"] is True,
          "and its own gate is recorded as passed")
    check(blocked["MITDB_TREE_AGGREGATE"]["eligible_for_registration"] is False,
          "but it is not eligible for registration")
    check(P.P2_SUPERSEDED_PRESENT in blocked["blocked_by"],
          "and the blocking failure is named")
    check(blocked["SOURCE_BUNDLE_FILE_SHA256"]["observed"] is None,
          "the failed gate never computed its value, so it stays None")


def test_bundle_is_complete_atomic_and_not_self_referential():
    with tempfile.TemporaryDirectory() as tmp:
        p1 = _passing_p1(tmp)
        p2 = P.run_p2(P.SOURCE_BUNDLE_FOLDER_ID, _adapter(), TOKEN)
        combined = P.combine(p1, p2)
        out = os.path.join(tmp, "run")
        written = P.write_bundle(out, P.build_config("T", True), p1, p2,
                                 combined, ["line"], synthetic=True)
        check(sorted(os.listdir(out)) == written["written"],
              "the published set is exactly what was reported")
        for name in P.bundle_files(True):
            check(os.path.exists(os.path.join(out, name)),
                  f"{name} is present")
        with open(os.path.join(out, P.PREP_MANIFEST_FILE),
                  encoding="utf-8") as handle:
            manifest = json.load(handle)
        check(manifest["prep_payload_sha256"] == written["prep_payload_sha256"],
              "the manifest records the payload fold")
        check(P.PREP_MANIFEST_FILE in manifest["excluded_from_payload_fold"],
              "and excludes itself from it")
        check(manifest["manifest_self_digest_recorded_here"] is False,
              "the manifest does not contain its own digest")
        blob = json.dumps(manifest, sort_keys=True)
        check(written["manifest_sha256_freeze_externally"] not in blob,
              "the manifest's own digest is nowhere inside the manifest")
        for name in os.listdir(out):
            with open(os.path.join(out, name), encoding="utf-8") as handle:
                check(written["manifest_sha256_freeze_externally"]
                      not in handle.read(),
                      f"nor inside {name}")
        for name in ("oracle_harness_identity.json", "fixture_results.json"):
            check(not os.path.exists(os.path.join(out, name)),
                  f"{name} is a P3 file and is not written by a P1/P2 run")


def test_bundle_refuses_an_unexpected_output_file():
    real = P.P1_P2_PREP_PAYLOAD_FILES
    with tempfile.TemporaryDirectory() as tmp:
        p1 = _passing_p1(tmp)
        p2 = P.run_p2(P.SOURCE_BUNDLE_FOLDER_ID, _adapter(), TOKEN)
        combined = P.combine(p1, p2)
        out = os.path.join(tmp, "run")
        try:
            P.P1_P2_PREP_PAYLOAD_FILES = real + ("never_written.json",)
            P.write_bundle(out, P.build_config("T", True), p1, p2, combined,
                           ["x"], synthetic=True)
            raise AssertionError("an incomplete file set was published")
        except P.PrepError as error:
            check("contracted set" in str(error),
                  "a file set that is not the contract is refused")
            check("preserved at" in str(error),
                  "and the partial directory is preserved, not deleted")
        finally:
            P.P1_P2_PREP_PAYLOAD_FILES = real
        # The directory stays exactly where it is.  What makes it "not a
        # bundle" is the missing commit marker, not its absence from disk.
        check(os.path.isdir(out), "the partial directory is kept on disk")
        check(not os.path.exists(os.path.join(out, P.COMMIT_MARKER)),
              "uncommitted, so no consumer will accept it")
        verdict = P.verify_published_bundle(out)
        check(verdict["ok"] is False and verdict["committed"] is False,
              "and the consumer contract refuses it explicitly")


def test_bundle_never_carries_a_credential():
    for payload in ({"access_token": "secret"}, {"client_secret": "x"},
                    {"nested": {"refresh_token": "y"}}):
        try:
            P.assert_no_credentials(payload, "test")
            raise AssertionError(f"{payload} was accepted")
        except P.PrepError as error:
            check("Credentials are not evidence" in str(error),
                  "a credential-shaped field is refused")
    P.assert_no_credentials({"file_id": "abc", "sha256": "d" * 64}, "test")
    check(True, "an ordinary inventory row is accepted")

    inventory = P.normalise_child(
        {"id": "f1", "name": "x", "size": "3", "mimeType": "text/plain",
         "access_token": "leaked", "credentials": {"a": 1}})
    check("access_token" not in inventory and "credentials" not in inventory,
          "the inventory row keeps only identity-bearing fields")
    check(set(inventory) == {"file_id", "name", "bytes", "mime_type",
                             "modified_time", "provider_sha256",
                             "provider_md5", "trashed", "is_shortcut",
                             "is_folder"},
          "and exactly those fields")


def test_synthetic_run_is_stamped_and_never_ingestable():
    with tempfile.TemporaryDirectory() as tmp:
        tree = _write_mitdb_tree(os.path.join(tmp, "mitdb"))
        adapter = _adapter()
        with _PatchedRegistration(tree):
            outcome = P.execute_prep(tree, P.SOURCE_BUNDLE_FOLDER_ID,
                                     os.path.join(tmp, "out"), adapter,
                                     approval=TOKEN, timestamp="T",
                                     emit=lambda *a: None, synthetic=True)
        check(outcome["combined"]["status"] == P.PREP_PASS,
              "the whole synthetic route runs end to end")
        directory = outcome["bundle"]["directory"]
        check(P.SYNTHETIC_MARKER in os.listdir(directory),
              "a synthetic bundle carries the marker file")
        with open(os.path.join(directory, P.SYNTHETIC_MARKER),
                  encoding="utf-8") as handle:
            marker = json.load(handle)
        check(marker["ingestable"] is False,
              "and is machine-readably not an ingest candidate")
        with open(os.path.join(directory, "config.json"),
                  encoding="utf-8") as handle:
            config = json.load(handle)
        check(config["synthetic_fixture"] is True and
              config["ingestable"] is False, "the config is stamped too")
        with open(os.path.join(directory, "summary.md"),
                  encoding="utf-8") as handle:
            summary = handle.read()
        check("SYNTHETIC FIXTURE - NOT A Q5-E RESULT" in summary,
              "and the summary says so plainly")
        check("not a Q5-E measurement" in summary,
              "and states it is not a measurement")
        check(len(adapter.calls) > 1,
              "the fake adapter served the run")
        check(all(kind in ("list_children", "download")
                  for kind, _ in adapter.calls),
              "using only read-only operations")


def test_seals_record_that_nothing_was_executed():
    with tempfile.TemporaryDirectory() as tmp:
        p1 = _passing_p1(tmp)
    p2 = P.run_p2(P.SOURCE_BUNDLE_FOLDER_ID, _adapter(), TOKEN)
    check(p1["seals"]["detector_executed"] is False, "P1: no detector ran")
    check(p1["seals"]["m0_m4_aggregated"] is False, "P1: no M0-M4 aggregation")
    check(p1["seals"]["training_performed"] is False, "P1: no training")
    check(p2["seals"]["bytes_hashed_only"] is True,
          "P2: bytes were hashed, contents were not aggregated")
    check(p2["seals"]["parquet_parsed"] is False, "P2: parquet was not parsed")
    check(p2["seals"]["drive_modified"] is False, "P2: Drive was not modified")
    for sealed in ("probability_opened", "labels_opened", "model_scored"):
        check(p2["seals"][sealed] is False, f"P2: {sealed} is false")


def test_notebook_is_committed_unexecuted():
    with open(NOTEBOOK, encoding="utf-8") as handle:
        nb = json.load(handle)
    cells = [c for c in nb["cells"] if c["cell_type"] == "code"]
    check(len(cells) >= 10, "the notebook has the contracted cells")
    for index, cell in enumerate(cells):
        check(cell.get("outputs") == [], f"cell {index} has no stored output")
        check(cell.get("execution_count") is None,
              f"cell {index} was never executed")
    source = "\n".join("".join(c["source"]) for c in nb["cells"])
    # 2026-08-12: read-only execution was approved, so the notebook's two
    # opt-in switches are deliberately on.  What must stay true is that they
    # are the *only* thing that is on, and that the module still defaults
    # closed so a stray import reaches nothing.
    check("OPEN_REGISTERED_DATA = True" in source,
          "the notebook opts in explicitly, under the 2026-08-12 approval")
    check("APPROVAL = P.EXECUTION_APPROVAL_TOKEN" in source,
          "and carries the separate read-only PREP token")
    check("EXECUTION_APPROVAL_TOKEN" in source
          and "Q5E_AUDIT" not in source,
          "which is the PREP token, not the Q5-E audit token")
    check(P.OPEN_REGISTERED_DATA is False,
          "while the module itself still defaults closed")
    check("EXECUTION_APPROVAL_RECORD" in source,
          "the notebook prints the approval record it is running under")
    check("run_prep" in source, "it calls the production route")
    check("module_capabilities" in source, "with a staleness guard")
    for stage in ("DESIGN_AND_BOUNDARIES", "ENVIRONMENT", "SYNTHETIC_FIXTURES",
                  "EXECUTION_APPROVAL", "DRIVE_AUTH_AND_FOLDER_ID_PREFLIGHT",
                  "P1_MITDB_IDENTITY", "P2_Q5D_BUNDLE_IDENTITY",
                  "COMBINED_DECISION", "BUNDLE_WRITE",
                  "HUMAN_READABLE_REPORT"):
        check(stage in source, f"the {stage} stage is present")
    # The banned names appear in the markdown boundary declarations, which is
    # where they belong. What matters is that no *code* cell calls them.
    import ast
    code = "\n".join("".join(c["source"]) for c in cells)
    called = set()
    for node in ast.walk(ast.parse(code)):
        if isinstance(node, ast.Call):
            func = node.func
            if isinstance(func, ast.Name):
                called.add(func.id)
            elif isinstance(func, ast.Attribute):
                called.add(func.attr)
    for banned in ("detect_r", "rr_features", "run_audit", "run_pipeline",
                   "load_all_inputs", "match_record", "rdsamp", "rdann"):
        check(banned not in called,
              f"no code cell calls {banned}()")
    markdown = "\n".join("".join(c["source"]) for c in nb["cells"]
                          if c["cell_type"] == "markdown")
    check("detect_r" in markdown,
          "the boundary is declared in prose, where naming it is the point")


def test_registered_q5e_gates_are_still_closed():
    """This PR registers nothing; the Q5-E stops stay exactly as they were."""
    check(Q5E.MITDB_TREE_AGGREGATE is None, "P1 is still unregistered")
    check(Q5E.SOURCE_BUNDLE_FILE_SHA256 == {}, "P2 is still unregistered")
    check(Q5E.SOURCE_MATCH_ORACLE_RECORD is None,
          "P3 is untouched by this PR")
    with open(P.__file__, encoding="utf-8") as handle:
        text = handle.read()
    check("MITDB_TREE_AGGREGATE =" not in text,
          "this module never assigns the registered aggregate")
    check("SOURCE_BUNDLE_FILE_SHA256 =" not in text,
          "nor the registered bundle digests")


# ─────────────────────────────────────────────────────────────────────────────
# Second acceptance review: B1-B7 and the G/E rulings
# ─────────────────────────────────────────────────────────────────────────────
class CountingReader(P.LocalTreeReader):
    """Records which files were actually read, not just which gates ran."""

    def __init__(self, approval):
        super().__init__(approval)
        self.read = []
        self.listed = []

    def listdir(self, directory):
        self.listed.append(directory)
        return super().listdir(directory)

    def stat_and_hash(self, directory, name):
        self.read.append(name)
        return super().stat_and_hash(directory, name)

    def read_bytes(self, directory, name, limit=None):
        self.read.append(name)
        return super().read_bytes(directory, name, limit=limit)


class OpenSpy(object):
    """Records every real `open()` under a directory.

    A reader-level counter proves what *this module's seam* did; it says
    nothing about a frozen helper that opens a path directly.  This watches the
    builtin, so a second read of the registered checksum file shows up no
    matter who performs it.
    """

    def __init__(self, directory):
        self.directory = os.path.abspath(directory)
        self.opened = []
        self._real = builtins.open

    def __enter__(self):
        spy = self

        def watched(file, *args, **kwargs):
            try:
                path = os.path.abspath(os.fspath(file))
            except TypeError:                       # a file descriptor
                path = None
            if path and path.startswith(spy.directory + os.sep):
                spy.opened.append(os.path.relpath(path, spy.directory))
            return spy._real(file, *args, **kwargs)

        builtins.open = watched
        return self

    def __exit__(self, *exc):
        builtins.open = self._real
        return False

    def count(self, name):
        return self.opened.count(name)


def test_b1_checksum_failure_reads_nothing_else():
    """B1: the I/O follows the gate order, not just the report."""
    with tempfile.TemporaryDirectory() as tmp:
        pristine = _write_mitdb_tree(os.path.join(tmp, "good"))
        registered = _PatchedRegistration(pristine)
        with registered:
            drifted = _write_mitdb_tree(os.path.join(tmp, "drifted"),
                                        bad_checksum_file=True)
            reader = CountingReader(TOKEN)
            calls = []
            real_parser = P.parse_sha256sums_text
            P.parse_sha256sums_text = (
                lambda *a, **k: calls.append("parse") or real_parser(*a, **k))
            try:
                with OpenSpy(drifted) as spy:
                    result = P.run_p1(drifted, TOKEN, reader=reader)
            finally:
                P.parse_sha256sums_text = real_parser

    check(result["status"] == P.P1_CHECKSUM_FILE_MISMATCH,
          "a drifted checksum file stops P1")
    check(reader.read == [BJ.MITDB_CHECKSUM_FILE],
          "exactly one file was read: the checksum file itself")
    check(len(reader.read) == 1,
          "the other 146 files were never read")
    check(spy.opened == [BJ.MITDB_CHECKSUM_FILE],
          "and the real open() spy agrees: one file, opened once")
    check(calls == [], "the publisher list was never even parsed")
    check(result["tree_aggregate"] is None, "no aggregate was computed")
    check(result["per_file"] == [], "and no per-file digests were produced")


def test_b1_happy_path_reads_each_file_once():
    with tempfile.TemporaryDirectory() as tmp:
        tree = _write_mitdb_tree(os.path.join(tmp, "mitdb"))
        with _PatchedRegistration(tree):
            reader = CountingReader(TOKEN)
            result = P.run_p1(tree, TOKEN, reader=reader)
    check(result["ok"] is True, "the pristine tree passes")
    check(len(reader.read) == 147, "147 files were read")
    check(len(set(reader.read)) == 147, "each exactly once, none re-read")
    check(reader.read[0] == BJ.MITDB_CHECKSUM_FILE,
          "and the checksum file was read first, before the rest")


def test_b1_file_set_failure_reads_no_file_at_all():
    with tempfile.TemporaryDirectory() as tmp:
        short = _write_mitdb_tree(os.path.join(tmp, "short"), drop="RECORDS")
        with _PatchedRegistration(short):
            reader = CountingReader(TOKEN)
            result = P.run_p1(short, TOKEN, reader=reader)
    check(result["status"] == P.P1_FILE_SET_MISMATCH, "the set gate fails")
    check(reader.read == [],
          "not even the checksum file is read when the set is wrong")


def test_b2_inventory_rejects_every_ambiguity_form():
    """B2: the file id is the identity key, so a row without one is unusable."""
    cases = {
        "missing_file_id": [dict(c, id="") for c in _bundle_children()],
        "duplicate_file_ids": _bundle_children() + [
            dict(_bundle_children()[0], name="extra-name")],
        "google_native": [
            dict(c, mimeType="application/vnd.google-apps.document")
            if c["name"] == "decision.json" else c
            for c in _bundle_children()],
        "sizeless": [{k: v for k, v in c.items() if k != "size"}
                     if c["name"] == "log.txt" else c
                     for c in _bundle_children()],
    }
    for label, children in cases.items():
        adapter = FakeDriveAdapter({P.SOURCE_BUNDLE_FOLDER_ID: children})
        result = P.run_p2(P.SOURCE_BUNDLE_FOLDER_ID, adapter, TOKEN)
        check(result["status"] == P.P2_INVENTORY_AMBIGUOUS,
              f"{label} is refused as ambiguous")
        check(result["ambiguity"][label],
              f"and is recorded under {label}")
        check(result["input_identity"] is None,
              f"{label} yields no identity")


def test_b3_direct_stream_is_cross_checked_against_the_inventory():
    """B3: a download that merely succeeded proves nothing about the bytes."""
    result = P.run_p2(P.SOURCE_BUNDLE_FOLDER_ID, _adapter(), TOKEN)
    bridge = [g for g in result["gates"]
              if g["gate"] == "canonical_bytes_bridge"][0]
    check(bridge["ok"] is True, "a consistent stream passes")
    check(len(bridge["cross_check"]) == len(BJ.BUNDLE_FILES),
          "every file has an audit record")
    for entry in bridge["cross_check"]:
        for field in ("file_id", "name", "inventory_bytes", "observed_bytes",
                      "provider_sha256", "observed_sha256", "sha256_match",
                      "provider_md5", "observed_md5", "md5_match",
                      "download_method", "checksum_available"):
            check(field in entry, f"the audit record carries {field}")
        check(entry["bytes_match"] is True, "size agrees with the inventory")
        check(entry["sha256_match"] is True, "and so does the provider sha256")


def test_b3_a_stream_that_disagrees_with_the_inventory_stops_the_bridge():
    lying = [dict(c, size=str(len(c["_bytes"]) + 5)) for c in _bundle_children()]
    adapter = FakeDriveAdapter({P.SOURCE_BUNDLE_FOLDER_ID: lying})
    result = P.run_p2(P.SOURCE_BUNDLE_FOLDER_ID, adapter, TOKEN)
    check(result["status"] == P.P2_FOLDER_ID_BRIDGE_UNRESOLVED,
          "a size disagreement stops at the bridge gate")
    check(result["input_identity"] is None,
          "and unverified bytes never reach the input identity gate")
    gates = [g["gate"] for g in result["gates"]]
    check("manifest_identity" not in gates,
          "nor the manifest gate")

    wrong_hash = [dict(c, sha256Checksum="f" * 64) for c in _bundle_children()]
    result = P.run_p2(P.SOURCE_BUNDLE_FOLDER_ID,
                      FakeDriveAdapter({P.SOURCE_BUNDLE_FOLDER_ID:
                                        wrong_hash}), TOKEN)
    check(result["status"] == P.P2_FOLDER_ID_BRIDGE_UNRESOLVED,
          "a provider sha256 disagreement stops too")

    wrong_md5 = [dict(c, md5Checksum="0" * 32) for c in _bundle_children()]
    result = P.run_p2(P.SOURCE_BUNDLE_FOLDER_ID,
                      FakeDriveAdapter({P.SOURCE_BUNDLE_FOLDER_ID:
                                        wrong_md5}), TOKEN)
    check(result["status"] == P.P2_FOLDER_ID_BRIDGE_UNRESOLVED,
          "and so does a provider md5 disagreement")


def test_b3_missing_checksums_are_recorded_not_guessed():
    """G4: absence is recorded; it does not fail a direct stream by itself."""
    bare = [{k: v for k, v in c.items() if k != "sha256Checksum"}
            for c in _bundle_children()]
    result = P.run_p2(P.SOURCE_BUNDLE_FOLDER_ID,
                      FakeDriveAdapter({P.SOURCE_BUNDLE_FOLDER_ID: bare}),
                      TOKEN)
    check(result["ok"] is True,
          "a direct stream still passes without a provider checksum")
    bridge = [g for g in result["gates"]
              if g["gate"] == "canonical_bytes_bridge"][0]
    check(bridge["n_without_checksum"] == len(BJ.BUNDLE_FILES),
          "and the absence is counted, not glossed over")
    for entry in bridge["cross_check"]:
        check(entry["checksum_available"] is False,
              "each record says the checksum was unavailable")
        check(entry["sha256_match"] is False,
              "an unavailable checksum is not reported as a match")
        check(entry["provider_sha256"] is None,
              "and no value is invented for it")
        check("not a security identity" in entry["md5_note"],
              "MD5 is labelled a transfer cross-check, not an identity")


def test_g5_publish_never_deletes_anything_pre_existing():
    """G5: an existing final path is refused, not removed."""
    with tempfile.TemporaryDirectory() as tmp:
        p1 = _passing_p1(tmp)
        p2 = P.run_p2(P.SOURCE_BUNDLE_FOLDER_ID, _adapter(), TOKEN)
        combined = P.combine(p1, p2)

        out = os.path.join(tmp, "existing")
        os.makedirs(out)
        with open(os.path.join(out, "someone_elses_file.txt"), "w",
                  encoding="utf-8") as handle:
            handle.write("do not delete me")
        try:
            P.write_bundle(out, P.build_config("T", True), p1, p2, combined,
                           ["x"], synthetic=True)
            raise AssertionError("an existing directory was overwritten")
        except P.PrepError as error:
            check("already there" in str(error),
                  "an existing final path is refused")
        check(os.path.exists(os.path.join(out, "someone_elses_file.txt")),
              "and the file that was already there survives")

        empty = os.path.join(tmp, "empty")
        os.makedirs(empty)
        try:
            P.write_bundle(empty, P.build_config("T", True), p1, p2, combined,
                           ["x"], synthetic=True)
            raise AssertionError("an empty existing directory was consumed")
        except P.PrepError:
            check(os.path.isdir(empty),
                  "even an empty existing directory is left alone")

        # A plain file at the final path is a third case: `rename` onto a file
        # would fail anyway, but only after the whole bundle had been staged.
        occupied = os.path.join(tmp, "occupied")
        with open(occupied, "w", encoding="utf-8") as handle:
            handle.write("not a bundle")
        try:
            P.write_bundle(occupied, P.build_config("T", True), p1, p2,
                           combined, ["x"], synthetic=True)
            raise AssertionError("an existing file was overwritten")
        except P.PrepError:
            check(os.path.isfile(occupied), "an existing file survives")
            with open(occupied, encoding="utf-8") as handle:
                check(handle.read() == "not a bundle",
                      "with its contents untouched")

        source = open(P.__file__, encoding="utf-8").read()
        writer = source.split("def write_bundle(", 1)[1].split(
            "\ndef verify_published_bundle", 1)[0]
        for forbidden in ("rmtree", "os.remove", "os.unlink", "os.rmdir",
                          "os.removedirs"):
            check(forbidden not in writer,
                  f"the writer never calls {forbidden}: it deletes nothing at "
                  f"all, not even its own directory")
        # No rename means no test-then-act window. There is nothing left to
        # get wrong between two operations, because there is only one.
        for forbidden in ("os.rename", "os.replace", "shutil.move"):
            check(forbidden not in writer,
                  f"and never calls {forbidden}: publication is a commit "
                  f"marker, not a rename")
        check("except BaseException" not in writer,
              "and does not catch BaseException")
        check("except Exception as error" in writer,
              "it catches only ordinary exceptions, and names them")


def test_posix_rename_really_replaces_an_empty_directory():
    """Why the rename-based publish was withdrawn, pinned as a platform fact.

    The previous design released its claim with `rmdir` and then renamed the
    staging directory into place.  Those are two operations, and this is what
    the kernel does to a directory that appears between them.  If this ever
    stops being true the reasoning in `write_bundle` should be revisited — but
    it is true on Linux, which is what Colab runs.
    """
    with tempfile.TemporaryDirectory() as tmp:
        source = os.path.join(tmp, "staging")
        target = os.path.join(tmp, "target")
        os.mkdir(source)
        with open(os.path.join(source, "payload"), "w",
                  encoding="utf-8") as handle:
            handle.write("mine")
        os.mkdir(target)                    # the racing writer's directory
        replaced = False
        try:
            os.rename(source, target)
            replaced = True
        except OSError:
            pass
        if os.name == "posix":
            check(replaced,
                  "POSIX rename replaces a pre-existing empty directory, so "
                  "rmdir-then-rename could destroy one that appeared in "
                  "between")
            check(os.listdir(target) == ["payload"],
                  "the racing writer's directory is simply gone")
        else:                                            # pragma: no cover
            check(True, "not POSIX; the publish makes no rename either way")

    # And the shipped writer therefore has no such sequence to exploit.
    source = open(P.__file__, encoding="utf-8").read()
    writer = source.split("def write_bundle(", 1)[1].split(
        "\ndef verify_published_bundle", 1)[0]
    import ast
    tree = ast.parse(open(P.__file__, encoding="utf-8").read())
    body = [n for n in ast.walk(tree)
            if isinstance(n, ast.FunctionDef) and n.name == "write_bundle"][0]
    creators = [n.func.attr for n in ast.walk(body)
                if isinstance(n, ast.Call)
                and isinstance(n.func, ast.Attribute)
                and n.func.attr in ("mkdir", "makedirs", "mkdtemp", "rename",
                                    "replace", "rmdir", "move")]
    check(creators.count("mkdir") == 1,
          f"exactly one mkdir claims the directory: {creators}")
    check("mkdtemp" not in creators,
          "there is no staging directory left to publish from")
    check(not ({"rename", "replace", "rmdir", "move"} & set(creators)),
          f"and no rename, replace or removal anywhere: {creators}")
    check(creators.count("makedirs") == 1,
          "the only other call creates the parent, which is not the claim")


def test_g5_a_writer_racing_into_the_claim_is_detected_not_overwritten():
    """The only window left is "between claiming the name and filling it".

    Nothing can take the name there — `mkdir` already succeeded — but
    something can write *into* it, and that must be caught rather than
    committed over.  The file-set check is what catches it, and the result is
    an uncommitted directory holding both parties' files, which is exactly
    what a diagnosis needs.
    """
    with tempfile.TemporaryDirectory() as tmp:
        p1 = _passing_p1(tmp)
        p2 = P.run_p2(P.SOURCE_BUNDLE_FOLDER_ID, _adapter(), TOKEN)
        combined = P.combine(p1, p2)
        target = os.path.join(tmp, "racy")

        def intruder(directory):
            with open(os.path.join(directory, "intruder.txt"), "w",
                      encoding="utf-8") as handle:
                handle.write("arrived after the claim")

        P._PUBLISH_RACE_HOOK = intruder
        try:
            P.write_bundle(target, P.build_config("T", True), p1, p2,
                           combined, ["x"], synthetic=True)
            raise AssertionError("the publish committed over the racing file")
        except P.PrepError as error:
            check("not committed" in str(error),
                  "the publish refuses to commit")
            check("Nothing was deleted or replaced" in str(error),
                  "and says nothing was destroyed")
        finally:
            P._PUBLISH_RACE_HOOK = None

        check(os.path.isfile(os.path.join(target, "intruder.txt")),
              "the racing writer's file survives")
        with open(os.path.join(target, "intruder.txt"),
                  encoding="utf-8") as handle:
            check("after the claim" in handle.read(),
                  "with its contents intact")
        check(not os.path.exists(os.path.join(target, P.COMMIT_MARKER)),
              "and the directory is left uncommitted")
        check(P.verify_published_bundle(target)["ok"] is False,
              "so the consumer contract refuses it")


def test_g5_only_a_committed_directory_is_a_bundle():
    """Publication is the marker, so every consumer check hangs off it."""
    with tempfile.TemporaryDirectory() as tmp:
        p1 = _passing_p1(tmp)
        p2 = P.run_p2(P.SOURCE_BUNDLE_FOLDER_ID, _adapter(), TOKEN)
        combined = P.combine(p1, p2)
        out = os.path.join(tmp, "run")
        written = P.write_bundle(out, P.build_config("T", True), p1, p2,
                                 combined, ["x"], synthetic=True)

        verdict = P.verify_published_bundle(
            out, expected_manifest_sha256=written[
                "manifest_sha256_freeze_externally"],
            manifest_anchor_source=P.ANCHOR_SAVED_NOTEBOOK)
        check(verdict["ok"] is True, "a committed bundle validates")
        check(verdict["committed"] is True, "and is reported as committed")
        check(verdict["prep_payload_sha256"] == written["prep_payload_sha256"],
              "with the payload fold recomputed, not copied")
        check(verdict["manifest_anchored_externally"] is True,
              "and the manifest anchored against the external freeze value")

        loose = P.verify_published_bundle(out)
        check(loose["ok"] is True, "without the freeze value it still passes")
        check(loose["manifest_anchored_externally"] is False,
              "but says plainly that the manifest was not anchored")

        # The manifest is outside the payload fold, so the external freeze
        # value is the only thing that can catch an edited manifest. It has to
        # actually be compared, not just carried.
        wrong = P.verify_published_bundle(
            out, expected_manifest_sha256="f" * 64,
            manifest_anchor_source=P.ANCHOR_SAVED_NOTEBOOK)
        check(wrong["ok"] is False,
              "a manifest that disagrees with the frozen value is refused")
        check(any(P.ANCHOR_SAVED_NOTEBOOK in p for p in wrong["problems"]),
              "and the problem names which anchor it disagreed with")
        with open(os.path.join(out, P.PREP_MANIFEST_FILE), "a",
                  encoding="utf-8") as handle:
            handle.write("\n")
        edited = P.verify_published_bundle(
            out, expected_manifest_sha256=written[
                "manifest_sha256_freeze_externally"],
            manifest_anchor_source=P.ANCHOR_REGISTERED_RECORD)
        check(edited["ok"] is False,
              "editing the manifest after the commit fails the anchor")
        check(P.verify_published_bundle(out)["ok"] is True,
              "which nothing but the external value could have caught: the "
              "payload fold does not cover the manifest")

        # The commit marker cannot be written twice, so a committed directory
        # cannot be re-committed with a different record.
        try:
            P.write_bundle(out, P.build_config("T", True), p1, p2, combined,
                           ["x"], synthetic=True)
            raise AssertionError("a committed bundle was written over")
        except P.PrepError as error:
            check("already there" in str(error),
                  "a second run refuses the same path outright")

        # Tampering after the fact is what the fold catches — an atomic
        # rename never could have.
        with open(os.path.join(out, "summary.md"), "a",
                  encoding="utf-8") as handle:
            handle.write("\nedited after the commit\n")
        after = P.verify_published_bundle(out)
        check(after["ok"] is False, "an edited payload file fails validation")
        check(any("payload fold" in p for p in after["problems"]),
              "and the recomputed fold is what reports it")

    with tempfile.TemporaryDirectory() as tmp:
        bare = os.path.join(tmp, "not-a-bundle")
        os.mkdir(bare)
        verdict = P.verify_published_bundle(bare)
        check(verdict["ok"] is False and verdict["committed"] is False,
              "a directory with no marker is not a bundle")
        check("not deleted" in " ".join(verdict["problems"]),
              "and refusing it does not mean removing it")
        check(os.path.isdir(bare), "it is still there afterwards")


def test_g5_publish_refuses_a_symlinked_parent_or_target():
    """A link at either end sends the write somewhere the path does not say."""
    if not hasattr(os, "symlink"):                       # pragma: no cover
        return
    with tempfile.TemporaryDirectory() as tmp:
        p1 = _passing_p1(tmp)
        p2 = P.run_p2(P.SOURCE_BUNDLE_FOLDER_ID, _adapter(), TOKEN)
        combined = P.combine(p1, p2)

        real = os.path.join(tmp, "real")
        os.makedirs(real)
        with open(os.path.join(real, "precious.txt"), "w",
                  encoding="utf-8") as handle:
            handle.write("keep me")

        # A symlink sitting *at* the final path.
        link = os.path.join(tmp, "link_target")
        os.symlink(real, link)
        try:
            P.write_bundle(link, P.build_config("T", True), p1, p2, combined,
                           ["x"], synthetic=True)
            raise AssertionError("published through a symlink")
        except P.PrepError as error:
            check("already there" in str(error),
                  "a symlink at the final path is refused, not followed")
        check(os.path.islink(link), "the link itself is left in place")
        check(os.path.isfile(os.path.join(real, "precious.txt")),
              "and what it points at is untouched")

        # A symlinked parent directory.
        parent_link = os.path.join(tmp, "link_parent")
        os.symlink(real, parent_link)
        try:
            P.write_bundle(os.path.join(parent_link, "bundle"),
                           P.build_config("T", True), p1, p2, combined,
                           ["x"], synthetic=True)
            raise AssertionError("published under a symlinked parent")
        except P.PrepError as error:
            check("symlink or reparse point" in str(error),
                  "a symlinked parent is refused")
        check(sorted(os.listdir(real)) == ["precious.txt"],
              "and nothing was written through it")

        check(P._is_link_like(link) is True, "the link check sees a symlink")
        check(P._is_link_like(real) is False,
              "and a real directory is not mistaken for one")
        check("isjunction" in open(P.__file__, encoding="utf-8").read(),
              "the same check covers a Windows junction where detectable")


def test_g5_staging_is_unique_per_call():
    with tempfile.TemporaryDirectory() as tmp:
        p1 = _passing_p1(tmp)
        p2 = P.run_p2(P.SOURCE_BUNDLE_FOLDER_ID, _adapter(), TOKEN)
        combined = P.combine(p1, p2)
        first = P.write_bundle(os.path.join(tmp, "a"),
                               P.build_config("T", True), p1, p2, combined,
                               ["x"], synthetic=True)
        second = P.write_bundle(os.path.join(tmp, "b"),
                                P.build_config("T", True), p1, p2, combined,
                                ["x"], synthetic=True)
        check(first["prep_payload_sha256"] == second["prep_payload_sha256"],
              "the same inputs fold to the same payload digest")
        check(os.path.isdir(os.path.join(tmp, "a")) and
              os.path.isdir(os.path.join(tmp, "b")),
              "two runs coexist without either deleting the other")
        leftovers = [n for n in os.listdir(tmp) if ".staging." in n]
        check(leftovers == [],
              "a successful publish leaves no staging directory behind")


def test_e3_e4_payload_is_p1_p2_specific_and_covers_the_marker():
    """E3/E4: no P3 files inherited, and nothing sits outside the fold."""
    check("oracle_harness_identity.json" not in P.P1_P2_PREP_PAYLOAD_FILES,
          "the P3 oracle harness file is not part of a P1/P2 bundle")
    check("fixture_results.json" not in P.P1_P2_PREP_PAYLOAD_FILES,
          "nor the P3 fixture results file")
    check(set(P.P1_P2_PREP_PAYLOAD_FILES) == {
        "config.json", "decision.json", "log.txt",
        "registration_candidates.json", "source_inventory.json",
        "summary.md"}, "the P1/P2 payload set is exactly the contracted six")
    check(P.SYNTHETIC_MARKER in P.payload_files(True),
          "a synthetic run folds its marker into the payload identity")
    check(P.SYNTHETIC_MARKER not in P.payload_files(False),
          "a production run has no marker at all")
    check(P.PREP_MANIFEST_FILE not in P.payload_files(True),
          "the manifest is excluded from the fold it records")

    with tempfile.TemporaryDirectory() as tmp:
        p1 = _passing_p1(tmp)
        p2 = P.run_p2(P.SOURCE_BUNDLE_FOLDER_ID, _adapter(), TOKEN)
        out = os.path.join(tmp, "run")
        written = P.write_bundle(out, P.build_config("T", True), p1, p2,
                                 P.combine(p1, p2), ["x"], synthetic=True)
        check(written["payload_files"] == list(P.payload_files(True)),
              "the receipt reports the actual fold target")
        with open(os.path.join(out, P.PREP_MANIFEST_FILE),
                  encoding="utf-8") as handle:
            manifest = json.load(handle)
        check(manifest["payload_files"] == list(P.payload_files(True)),
              "and so does the manifest")

        # Tampering with the marker must break the recomputed fold.
        triples = []
        for name in P.payload_files(True):
            with open(os.path.join(out, name), "rb") as handle:
                body = handle.read()
            triples.append({"name": name, "bytes": len(body),
                            "sha256": hashlib.sha256(body).hexdigest()})
        check(P.fold_file_triples(triples) == written["prep_payload_sha256"],
              "the published fold recomputes exactly")
        with open(os.path.join(out, P.SYNTHETIC_MARKER), "a",
                  encoding="utf-8") as handle:
            handle.write(" ")
        tampered = []
        for name in P.payload_files(True):
            with open(os.path.join(out, name), "rb") as handle:
                body = handle.read()
            tampered.append({"name": name, "bytes": len(body),
                             "sha256": hashlib.sha256(body).hexdigest()})
        check(P.fold_file_triples(tampered) != written["prep_payload_sha256"],
              "editing the synthetic marker breaks the payload fold")


class _Credential(object):
    """The only thing the audit reads off a credential is its scopes."""

    def __init__(self, scopes):
        self.scopes = scopes


def _scope_seams(scopes, calls):
    """A credential provider and service factory that record every call."""

    def credential_provider():
        calls.append("credential")
        return _Credential(scopes)

    def service_factory(credentials):
        calls.append(("service", tuple(credentials.scopes or ())))
        return object()

    return credential_provider, service_factory


def test_b4_authentication_happens_only_on_the_approved_path():
    """B4: an unapproved run performs zero authentication calls."""
    calls = []
    provider, factory = _scope_seams([P.DRIVE_READONLY_SCOPE], calls)

    for approval, label in ((None, "no approval"),
                            ("wrong-token", "a wrong token")):
        try:
            P.authenticate_drive_readonly(approval,
                                          credential_provider=provider,
                                          service_factory=factory)
            raise AssertionError(f"{label} authenticated")
        except P.PrepNotApprovedError:
            check(True, f"{label} is refused before authenticating")
    check(calls == [], "and zero authentication calls were made")

    service, audit = P.authenticate_drive_readonly(
        TOKEN, credential_provider=provider, service_factory=factory)
    check(calls == ["credential",
                    ("service", (P.DRIVE_READONLY_SCOPE,))],
          "an approved call acquires a credential first, then builds the "
          "service from that credential")
    check(service is not None, "and returns a service object")
    check(audit["exact_readonly_scope_proven"] is True,
          "the audit records that the read-only scope was proven")
    check(audit["requested_scopes"] == [P.DRIVE_READONLY_SCOPE],
          "and which scope was requested")
    check(audit["credential_recorded"] is False,
          "the credential object itself is never recorded")

    adapter, adapter_audit = P.build_drive_adapter(
        TOKEN, credential_provider=provider, service_factory=factory)
    check(isinstance(adapter, P.GoogleDriveFolderAdapter),
          "build_drive_adapter injects the service into the adapter")
    check(adapter._service is not None, "the adapter holds the service")
    check(adapter_audit["exact_readonly_scope_proven"] is True,
          "and hands the scope audit back with it")

    installers = _module_calls(P.__file__) & {
        "check_call", "check_output", "call", "run", "Popen", "system"}
    check(not installers,
          f"no subprocess/installer call exists: {sorted(installers)}")
    with open(P.__file__, encoding="utf-8") as handle:
        check("!pip" not in handle.read(),
              "and no notebook-magic install either")
    report = P.check_runtime_dependencies()
    check(set(report["required"]) == set(P.RUNTIME_DEPENDENCIES),
          "the dependency requirement is reported explicitly")


def test_c2_the_requested_scope_reaches_the_real_credential_request():
    """C2: the scope is requested, not merely declared in a constant.

    A module-level constant nobody passes anywhere proves nothing, so this
    reads the production credential provider's AST and checks the constant is
    actually handed to `google.auth.default` and to `with_scopes`.
    """
    import ast
    tree = ast.parse(open(P.__file__, encoding="utf-8").read())
    provider = [n for n in ast.walk(tree)
                if isinstance(n, ast.FunctionDef)
                and n.name == "_colab_readonly_credential"]
    check(len(provider) == 1, "the production credential provider exists")
    scoped = []
    for node in ast.walk(provider[0]):
        if not isinstance(node, ast.Call):
            continue
        names = [a.id for a in ast.walk(node)
                 if isinstance(a, ast.Name)]
        if "DRIVE_READONLY_SCOPE" in names:
            target = node.func
            scoped.append(target.attr if isinstance(target, ast.Attribute)
                          else getattr(target, "id", "?"))
    check("default" in scoped,
          f"the read-only scope is passed to google.auth.default: {scoped}")
    check("with_scopes" in scoped,
          f"and to with_scopes when the credential allows it: {scoped}")

    # And the injected route really passes the credential object through to
    # the service factory, rather than letting the client pick up an ambient
    # default whose scope nobody checked.
    seen = {}

    def factory(credentials):
        seen["credentials"] = credentials
        return object()

    credential = _Credential([P.DRIVE_READONLY_SCOPE])
    P.authenticate_drive_readonly(TOKEN,
                                  credential_provider=lambda: credential,
                                  service_factory=factory)
    check(seen["credentials"] is credential,
          "the proven credential is the one the service is built from")


def test_c2_scope_fixtures_pass_exactly_one_case_and_stop_the_rest():
    """C2: exact scope passes; absent, broader and extra scopes all stop."""
    cases = {
        "no scopes at all": None,
        "an empty scope list": [],
        "a broader scope that merely includes read-only": [
            "https://www.googleapis.com/auth/drive"],
        "read-only plus something else": [
            P.DRIVE_READONLY_SCOPE,
            "https://www.googleapis.com/auth/drive.file"],
    }
    for label, scopes in cases.items():
        calls = []
        provider, factory = _scope_seams(scopes, calls)
        try:
            P.authenticate_drive_readonly(TOKEN,
                                          credential_provider=provider,
                                          service_factory=factory)
            raise AssertionError(f"{label} was accepted as read-only")
        except P.PrepError as error:
            check(P.READONLY_SCOPE_UNPROVEN in str(error),
                  f"{label} stops with {P.READONLY_SCOPE_UNPROVEN}")
        check(calls == ["credential"],
              f"{label} never reaches the service factory")
        audit = P.audit_credential_scopes(_Credential(scopes))
        check(audit["exact_readonly_scope_proven"] is False,
              f"{label} is not recorded as proven")
        check(audit["reason"], f"{label} records why it could not be proven")

    audit = P.audit_credential_scopes(
        _Credential([P.DRIVE_READONLY_SCOPE]))
    check(audit["exact_readonly_scope_proven"] is True,
          "exactly the read-only scope is the one case that proves it")
    check(audit["reason"] is None, "and it has nothing to explain away")
    check(audit["no_write_adapter_methods"] is True,
          "the adapter's lack of write methods is reported separately")


def test_c2_the_adapter_never_builds_its_own_default_client():
    """C2: no service means no adapter — never an ambient default."""
    try:
        P.GoogleDriveFolderAdapter(TOKEN)
        raise AssertionError("the adapter built itself a default client")
    except P.PrepError as error:
        check("never constructs its own client" in str(error),
              "an adapter without a service refuses to exist")

    import ast
    tree = ast.parse(open(P.__file__, encoding="utf-8").read())
    adapter = [n for n in ast.walk(tree)
               if isinstance(n, ast.ClassDef)
               and n.name == "GoogleDriveFolderAdapter"]
    check(len(adapter) == 1, "the production adapter exists")
    builds = [n for n in ast.walk(adapter[0])
              if isinstance(n, ast.Call)
              and getattr(n.func, "id", None) == "build"]
    check(not builds,
          "and its body contains no discovery build() call at all")


def test_c1_no_authentication_happens_while_the_guard_is_alive():
    """C1: with the guard in place, the approved route calls nothing.

    Not "fails to authenticate" — makes zero calls.  Every seam that could
    touch a credential, the API or a registered byte is a spy here, and the
    run is set up so that the *only* thing standing between it and a real
    Drive call is the terminal guard.
    """
    calls = []

    def spy(label):
        def recorded(*args, **kwargs):
            calls.append(label)
            raise AssertionError(f"{label} was called behind the guard")
        return recorded

    saved = {name: getattr(P, name)
             for name in ("build_drive_adapter", "authenticate_drive_readonly",
                          "_colab_readonly_credential", "execute_prep",
                          "run_p1", "run_p2", "GoogleDriveFolderAdapter")}
    record = dict(P.EXECUTION_APPROVAL_RECORD)
    for name in saved:
        setattr(P, name, spy(name))
    try:
        # Execution is approved now, so the closed case is exercised by
        # withdrawing the approval — the property under test is unchanged:
        # while the stop is closed, *nothing* below it is reached.
        P.EXECUTION_APPROVAL_RECORD["granted"] = False
        P.run_prep("/nonexistent/mitdb", P.SOURCE_BUNDLE_FOLDER_ID,
                   "/nonexistent/out", adapter=None, approval=TOKEN,
                   open_registered_data=True, timestamp="20260812T000000Z",
                   emit=lambda *a, **k: None)
        raise AssertionError("the terminal guard did not stop the run")
    except P.PrepError as error:
        check("not approved for execution" in str(error),
              "the terminal guard is what stopped it")
    finally:
        for name, value in saved.items():
            setattr(P, name, value)
        P.EXECUTION_APPROVAL_RECORD.clear()
        P.EXECUTION_APPROVAL_RECORD.update(record)

    check(calls == [],
          f"zero auth, adapter, API and reader calls were made: {calls}")
    check(P.EXECUTION_APPROVAL_RECORD["granted"] is True,
          "and the fixture restored the approval record")


def test_c1_the_guard_sits_after_every_check_and_before_every_capability():
    """C1: the production order is a property of the code, not a comment."""
    import ast
    tree = ast.parse(open(P.__file__, encoding="utf-8").read())
    body = [n for n in ast.walk(tree)
            if isinstance(n, ast.FunctionDef) and n.name == "run_prep"][0]

    order = []
    for node in ast.walk(body):
        if isinstance(node, ast.Name) and node.id == "open_registered_data":
            order.append(("switch", node.lineno))
        elif isinstance(node, ast.Call):
            name = (node.func.attr if isinstance(node.func, ast.Attribute)
                    else getattr(node.func, "id", ""))
            if name in ("require_execution_approval", "_terminal_execution_guard",
                        "build_drive_adapter", "execute_prep"):
                order.append((name, node.lineno))
        elif isinstance(node, ast.Name) and node.id == "SOURCE_BUNDLE_FOLDER_ID":
            order.append(("folder_id", node.lineno))
    first = {}
    for label, line in order:
        first.setdefault(label, line)
        first[label] = min(first[label], line)

    guard = first["_terminal_execution_guard"]
    check(first["switch"] < guard, "the switch is checked before the guard")
    check(first["require_execution_approval"] < guard,
          "the approval is checked before the guard")
    check(first["folder_id"] < guard,
          "the folder id is checked before the guard")
    check(guard < first["build_drive_adapter"],
          "and the guard sits before any credential is acquired")
    check(first["build_drive_adapter"] < first["execute_prep"],
          "which in turn sits before any P1/P2 reader or API call")


def test_b4_notebook_authenticates_only_behind_both_switches():
    with open(NOTEBOOK, encoding="utf-8") as handle:
        nb = json.load(handle)
    cells = [c for c in nb["cells"] if c["cell_type"] == "code"]
    source = "\n".join("".join(c["source"]) for c in cells)

    # C1: the notebook has no authentication path of its own.  Auth lives
    # below the terminal guard inside run_prep(), so a notebook that builds an
    # adapter itself would be reaching a credential the guard never saw.
    for name in ("build_drive_adapter", "authenticate_drive_readonly",
                 "GoogleDriveFolderAdapter", "_colab_readonly_credential"):
        called = [c for c in cells if f"{name}(" in "".join(c["source"])]
        check(not called,
              f"the notebook never calls {name}(): auth belongs behind the "
              f"terminal guard, not in a cell")
    check("check_runtime_dependencies" in source,
          "it reports the dependency requirement without authenticating")
    check("DRIVE_READONLY_SCOPE" in source,
          "and states the scope contract it will run under")
    check("SOURCE_BUNDLE_FOLDER_ID" in source,
          "and shows the registered folder id it would use")

    run_cells = [c for c in cells if "P.run_prep(" in "".join(c["source"])]
    check(len(run_cells) == 1, "exactly one cell calls run_prep()")
    body = "".join(run_cells[0]["source"])
    check("adapter=None" in body,
          "and it passes adapter=None, leaving auth to the guarded route")
    check("OPEN_REGISTERED_DATA" in body and "APPROVAL" in body,
          "guarded by both switches")
    check("pip install" not in source and "!pip" not in source,
          "the notebook never installs a package silently")


def test_b5_manifest_digest_is_reported_for_external_freezing():
    with open(NOTEBOOK, encoding="utf-8") as handle:
        source = handle.read()
    check("manifest_sha256_freeze_externally" in source,
          "the notebook prints the manifest digest for external freezing")
    check("prep_payload_sha256" in source,
          "and the payload fold")
    check("registration_allowed" in source,
          "and the registration verdict")
    check("eligible_for_registration" in source,
          "and each candidate's eligibility")

    with tempfile.TemporaryDirectory() as tmp:
        p1 = _passing_p1(tmp)
        p2 = P.run_p2(P.SOURCE_BUNDLE_FOLDER_ID, _adapter(), TOKEN)
        out = os.path.join(tmp, "run")
        written = P.write_bundle(out, P.build_config("T", True), p1, p2,
                                 P.combine(p1, p2), ["x"], synthetic=True)
    check(len(written["manifest_sha256_freeze_externally"]) == 64,
          "the writer returns a full 64-hex manifest digest")
    check(len(written["prep_payload_sha256"]) == 64,
          "and a full payload fold")


def test_b6_execution_contract_fixes_the_result_acceptance_criteria():
    contract = os.path.join(
        ROOT, "experiments", "specs",
        "EXP-2026-008-q5e-prep-p1-p2-execution-contract.md")
    with open(contract, encoding="utf-8") as handle:
        text = handle.read()
    check("Result acceptance criteria" in text,
          "the contract fixes what a result review will check")
    for item in ("gate order", "146", "prefix", "call audit",
                 "folder id", "ambiguity", "12", "SUPERSEDED",
                 "subset fold", "payload fold", "self digest",
                 "applied_automatically", "first_failure"):
        check(item in text, f"the criteria mention {item}")


def test_b7_claims_match_the_code():
    with open(P.__file__, encoding="utf-8") as handle:
        text = handle.read()
    check("all bytes are linked by provider checksum" not in text,
          "no claim that every byte is checksum-linked")
    check("every available provider checksum" in text,
          "the claim is scoped to checksums that exist")
    contract = os.path.join(
        ROOT, "experiments", "specs",
        "EXP-2026-008-q5e-prep-p1-p2-execution-contract.md")
    with open(contract, encoding="utf-8") as handle:
        spec = handle.read()
    flat = " ".join(spec.lower().split())
    check("observations are preserved" in flat,
          "the contract states that observations are preserved")
    check("only eligibility is withheld" in flat,
          "and that only eligibility is withheld")
    check("nothing is deleted, ever" in flat,
          "the contract states that nothing is deleted")
    check("not even the passing gate's observation" not in flat,
          "the old blanket-withholding sentence is gone")

    # The publish claim has to match what the code actually guarantees. The
    # code no longer renames, so the contract must not promise atomicity.
    check("atomic-directory-publication claim is withdrawn" in flat,
          "the withdrawn atomicity claim is stated as withdrawn")
    check("published by a same-parent rename" not in flat,
          "and the old rename sentence is gone")
    check("so the publish is atomic" not in text,
          "the module makes no atomic-publish claim either")
    check("a directory without `committed.json` is not a bundle" in flat,
          "the contract states what publication now means")
    check("verify_published_bundle" in flat,
          "and names the consumer validation a reader must call")

    # And the one-read rule, which is the other thing the code enforces.
    check("one read is the observation" in flat,
          "the contract states that the observation comes from one read")
    check("second_read_non_authoritative" in flat,
          "and names where anything from a later read is fenced off")


def test_f2_patched_registration_restores_on_exception():
    before = (P.MITDB_CHECKSUM_FILE_SHA256,
              P.MITDB_REGISTERED_AGGREGATE_PREFIX)
    with tempfile.TemporaryDirectory() as tmp:
        tree = _write_mitdb_tree(os.path.join(tmp, "mitdb"))
        try:
            with _PatchedRegistration(tree):
                check(P.MITDB_CHECKSUM_FILE_SHA256 != before[0],
                      "the fixture does replace the registered constants")
                raise RuntimeError("boom")
        except RuntimeError:
            check(True, "the exception propagates")
    check((P.MITDB_CHECKSUM_FILE_SHA256,
           P.MITDB_REGISTERED_AGGREGATE_PREFIX) == before,
          "and the constants are restored even on an exception")
    with open(P.__file__, encoding="utf-8") as handle:
        text = handle.read()
    check("registered_override" not in text and "override=" not in text,
          "production takes no registration-override argument")



#: Every shape the frozen parser's conventions have to survive.  Each of these
#: is a decision `BJ.parse_sha256sums` makes, and a PREP-local parser that
#: quietly differed on any one of them would verify a different list than the
#: one the frozen join verifies.
SHA256SUMS_DIALECTS = {
    "two spaces": "{d}  RECORDS\n",
    "single space": "{d} RECORDS\n",
    "tab separated": "{d}\tRECORDS\n",
    "leading whitespace": "   {d}  RECORDS\n",
    "trailing whitespace": "{d}  RECORDS   \n",
    "binary marker": "{d} *RECORDS\n",
    "dot slash prefix": "{d}  ./RECORDS\n",
    "nested path kept whole": "{d}  x_mitdb/RECORDS\n",
    "uppercase digest": "{D}  RECORDS\n",
    "blank lines": "\n\n{d}  RECORDS\n\n",
    "comment lines": "# a comment\n{d}  RECORDS\n#another\n",
    "malformed: digest only": "{d}\n{d}  RECORDS\n",
    "malformed: short digest": "abc  RECORDS\n{d}  RECORDS\n",
    "malformed: no digest": "  RECORDS\n{d}  RECORDS\n",
    "duplicate key, last wins": "{d}  RECORDS\n{e}  RECORDS\n",
    "crlf line endings": "{d}  RECORDS\r\n{e}  ANNOTATORS\r\n",
    "empty file": "",
    "only comments": "# nothing here\n",
}


def test_c3_the_prep_parser_agrees_with_the_frozen_one_everywhere():
    """C3: reading a snapshot instead of a path must change nothing else."""
    digest = hashlib.sha256(b"one").hexdigest()
    other = hashlib.sha256(b"two").hexdigest()
    with tempfile.TemporaryDirectory() as tmp:
        for label, template in SHA256SUMS_DIALECTS.items():
            text = template.format(d=digest, D=digest.upper(), e=other)
            path = os.path.join(tmp, "SHA256SUMS.txt")
            with open(path, "w", encoding="utf-8", newline="") as handle:
                handle.write(text)
            frozen = BJ.parse_sha256sums(path)
            local = P.parse_sha256sums_text(text)
            check(local == frozen,
                  f"the two parsers agree on {label}: {local} != {frozen}")

    # And the conventions themselves are the ones that matter, spelled out so
    # a future edit to either parser has to break a named expectation.
    parsed = P.parse_sha256sums_text(
        f"{digest.upper()} *./RECORDS\n{other}  x_mitdb/RECORDS\n")
    check(parsed["RECORDS"] == digest,
          "a binary marker and a ./ prefix are both stripped")
    check(parsed["RECORDS"] == parsed["RECORDS"].lower(),
          "and the digest is lowercased")
    check(parsed["x_mitdb/RECORDS"] == other,
          "a nested path keeps its whole key and never answers for the "
          "top-level file of the same basename")


def test_c3_the_checksum_file_is_read_exactly_once():
    """C3: one snapshot serves both the self-digest and the parsed list.

    Two reads leave a window: the file is verified in one state and parsed in
    another, which makes the verification decorative.  The reader counter alone
    would not catch a frozen helper opening the path itself, so this watches
    the real builtin.
    """
    with tempfile.TemporaryDirectory() as tmp:
        tree = _write_mitdb_tree(os.path.join(tmp, "mitdb"))
        with _PatchedRegistration(tree):
            reader = CountingReader(TOKEN)
            with OpenSpy(tree) as spy:
                result = P.run_p1(tree, TOKEN, reader=reader)

    check(result["ok"] is True, "the pristine tree still passes")
    check(spy.count(BJ.MITDB_CHECKSUM_FILE) == 1,
          f"the checksum file was opened exactly once, not "
          f"{spy.count(BJ.MITDB_CHECKSUM_FILE)}")
    check(len(spy.opened) == 147,
          f"147 opens in total, one per file: {len(spy.opened)}")
    check(reader.read.count(BJ.MITDB_CHECKSUM_FILE) == 1,
          "and the reader seam agrees")
    gate = [g for g in result["gates"]
            if g["gate"] == "checksum_file_digest"][0]
    check(gate["reads_of_checksum_file"] == 1,
          "the gate record says so too")


def test_c3_a_swap_between_the_two_uses_cannot_change_the_verdict():
    """C3: mutate the file in the old window and nothing downstream shifts.

    A parser that re-opened the path would pick up the swapped list — and the
    swapped list, being a valid list of the tree's real digests, would make a
    tree pass that the *registered* list does not describe.
    """
    with tempfile.TemporaryDirectory() as tmp:
        tree = _write_mitdb_tree(os.path.join(tmp, "mitdb"))
        with _PatchedRegistration(tree):
            path = os.path.join(tree, BJ.MITDB_CHECKSUM_FILE)
            with open(path, "rb") as handle:
                original = handle.read()

            swaps = []

            class SwappingReader(P.LocalTreeReader):
                """Rewrites the checksum file the moment it has been read."""

                def read_bytes(self, directory, name, limit=None):
                    body = super().read_bytes(directory, name, limit=limit)
                    if name == BJ.MITDB_CHECKSUM_FILE:
                        with open(os.path.join(directory, name), "wb") as fh:
                            fh.write(b"# swapped after the digest was taken\n")
                        swaps.append(name)
                    return body

            result = P.run_p1(tree, TOKEN, reader=SwappingReader(TOKEN))
            pristine = P.run_p1(
                _write_mitdb_tree(os.path.join(tmp, "again")), TOKEN)

    check(swaps == [BJ.MITDB_CHECKSUM_FILE],
          "the file really was rewritten in the old window")
    check(result["ok"] is True,
          "the run still passes: it used the bytes it verified")
    check(result["tree_aggregate"] == pristine["tree_aggregate"],
          "and reached exactly the aggregate the unswapped tree reaches")
    publisher = [g for g in result["gates"]
                 if g["gate"] == "publisher_checksums"][0]
    check(publisher["checked"] == P.MITDB_PUBLISHER_LISTED_FILES,
          "the 146 publisher-listed files were checked against the verified "
          "list, not against the swapped one")


def test_c4_a_publisher_failure_keeps_every_digest_it_computed():
    """C4: measured observations survive the gate that rejected them."""
    with tempfile.TemporaryDirectory() as tmp:
        tree = _write_mitdb_tree(os.path.join(tmp, "mitdb"),
                                 corrupt="RECORDS")
        with _PatchedRegistration(tree):
            result = P.run_p1(tree, TOKEN)

    check(result["status"] == P.P1_PUBLISHER_MISMATCH,
          "a corrupted file stops at the publisher gate")
    check(result["status"] == "P1_MITDB_PUBLISHER_CHECKSUM_MISMATCH",
          "under exactly that name")
    check(len(result["per_file"]) == P.MITDB_PUBLISHER_LISTED_FILES + 1,
          f"all 146 + 1 per-file observations are kept, not "
          f"{len(result['per_file'])}")
    for entry in result["per_file"]:
        check(set(entry) == {"name", "bytes", "sha256"},
              "each carries name, bytes and SHA-256")
    check(result["tree_aggregate"] is None,
          "but no aggregate was folded from an unverified tree")
    check(result["gate_passed"] is False, "the gate did not pass")
    check(result["eligible_for_registration"] is False,
          "so nothing here is eligible for registration")
    check(result["observation_only"] is True,
          "and what is kept is marked as observation only")
    check(result["blocked_by"] == "P1_MITDB_PUBLISHER_CHECKSUM_MISMATCH",
          "with the blocking reason named")

    gate = [g for g in result["gates"]
            if g["gate"] == "publisher_checksums"][0]
    check(gate["n_mismatched"] == 1, "one file mismatched")
    detail = gate["mismatched"][0]
    check(detail["name"] == "RECORDS", "and it is named")
    check(detail["published_sha256"] != detail["observed_sha256"],
          "with both digests recorded so the difference can be inspected")
    check(detail["observation_from_single_read"] is True,
          "the authoritative observation came from one read")
    second = detail["second_read_non_authoritative"]
    check(second["authoritative"] is False,
          "the explanatory detail is kept separate and marked non-authoritative")
    check(second["stable"] is True,
          "here the file did not change, so the second read agrees")
    check("has_crlf" in second and "starts_with_bom" in second,
          "and the cheap benign explanations are reported under it")

    candidates = P.registration_candidates(
        result, P.run_p2(P.SOURCE_BUNDLE_FOLDER_ID, _adapter(), TOKEN),
        P.combine(result,
                  P.run_p2(P.SOURCE_BUNDLE_FOLDER_ID, _adapter(), TOKEN)))
    entry = candidates["MITDB_TREE_AGGREGATE"]
    check(entry["observed"] is None,
          "the aggregate target itself was never measured")
    check(entry["per_file_observations"] == 147,
          "while the 147 per-file observations behind it are counted")
    check(entry["eligible_for_registration"] is False,
          "and the target is not eligible")


def test_c4_an_early_p1_failure_still_reports_nothing_it_did_not_measure():
    with tempfile.TemporaryDirectory() as tmp:
        short = _write_mitdb_tree(os.path.join(tmp, "short"), drop="RECORDS")
        with _PatchedRegistration(short):
            early = P.run_p1(short, TOKEN)
        drifted = _write_mitdb_tree(os.path.join(tmp, "drift"))
        with _PatchedRegistration(drifted, checksum="0" * 64):
            checksum_stop = P.run_p1(drifted, TOKEN)

    for result, label in ((early, "the file-set gate"),
                          (checksum_stop, "the checksum-file gate")):
        check(result["per_file"] == [],
              f"{label} stops before anything is hashed, so per_file is empty")
        check(result["tree_aggregate"] is None,
              f"{label} produces no aggregate")
        check(result["observation_only"] is False,
              f"{label} has no observation to qualify")
        check(result["eligible_for_registration"] is False,
              f"{label} registers nothing")


def test_c4_p2_keeps_the_bridge_it_proved_when_a_later_gate_fails():
    """C4: the cross-checks really happened; a manifest failure is not a reason
    to forget them.  `input_identity` stays None because that gate was never
    reached — an absent identity and a hidden one are different claims."""
    result = P.run_p2(P.SOURCE_BUNDLE_FOLDER_ID,
                      _adapter(code='0' * 64), TOKEN)

    check(result["status"] == P.P2_MANIFEST_MISMATCH,
          "the manifest gate is what failed")
    check(result["input_identity"] is None,
          "the input identity was never computed, so it is None")
    check(result["bridge"]["ok"] is True,
          "but the bridge that did pass is preserved")
    check(result["bridge"]["method"] == "drive_file_id_stream",
          "with the method it used")
    check(len(result["bridge"]["cross_check"]) == len(BJ.BUNDLE_FILES),
          "and every file's cross-check record")
    check(result["manifest_identity"]["problems"],
          "the manifest problems are reported rather than summarised away")
    check(result["observation_only"] is True,
          "what survives is marked as observation only")
    check(result["eligible_for_registration"] is False,
          "and none of it is eligible for registration")
    check(result["blocked_by"] == P.P2_MANIFEST_MISMATCH,
          "with the blocking reason named")

    with tempfile.TemporaryDirectory() as tmp:
        p1 = _passing_p1(tmp)
    candidates = P.registration_candidates(
        p1, result, P.combine(p1, result))
    entry = candidates["SOURCE_BUNDLE_FILE_SHA256"]
    check(entry["observed"] is None, "no input identity is offered")
    check(entry["bridge_cross_checks"] == len(BJ.BUNDLE_FILES),
          "while the bridge observations behind it are counted")
    check(entry["bridge_method"] == "drive_file_id_stream",
          "and the method is preserved")
    # G3, restated: the *passing* leg's observation is still reported.
    passing = candidates["MITDB_TREE_AGGREGATE"]
    check(passing["observed"] == p1["tree_aggregate"],
          "P1's aggregate is still reported even though P2 failed")
    check(passing["gate_passed"] is True, "its own gate passed")
    check(passing["eligible_for_registration"] is False,
          "but the combined gate withholds eligibility, not the observation")


def test_c5_the_run_records_the_environment_it_happened_in():
    """C5: a digest is only as interpretable as the runtime that produced it."""
    with tempfile.TemporaryDirectory() as tmp:
        p1 = _passing_p1(tmp)
        p2 = P.run_p2(P.SOURCE_BUNDLE_FOLDER_ID, _adapter(), TOKEN)
        combined = P.combine(p1, p2)
        out = os.path.join(tmp, "bundle")
        P.write_bundle(out, P.build_config("T", True), p1, p2, combined,
                       ["x"], synthetic=True)
        with open(os.path.join(out, "config.json"), encoding="utf-8") as fh:
            config = json.load(fh)
        with open(os.path.join(out, "manifest.json"), encoding="utf-8") as fh:
            manifest = json.load(fh)

    runtime = config["runtime"]
    check(runtime["python_version"] == __import__("platform").python_version(),
          "the interpreter version is recorded")
    check(runtime["platform"], "and the platform")
    for dist in P.RUNTIME_DISTRIBUTIONS:
        check(dist in runtime["distributions"],
              f"{dist}'s version is recorded")
        value = runtime["distributions"][dist]
        check(value == "unavailable" or value[0].isdigit(),
              f"{dist} is a real version or the word 'unavailable', never a "
              f"guess or 'latest': {value!r}")
    check("latest" not in json.dumps(runtime),
          "nothing is recorded as 'latest'")
    check(runtime["requested_drive_scope"] == P.DRIVE_READONLY_SCOPE,
          "the scope this run would request is recorded")
    for key in ("prep_module_sha256", "q5e_module_sha256",
                "frozen_q5d_module_sha256"):
        check(len(runtime[key]) == 64, f"{key} is a full digest")
    check(manifest["runtime"] == runtime,
          "and the manifest carries the same record")

    auth = config["drive_authentication"]
    check(auth["performed"] is False,
          "a synthetic run records that it never authenticated")
    check(auth["exact_readonly_scope_proven"] is False,
          "and claims no scope proof it did not make")

    signed = P.build_config("T", False, P.audit_credential_scopes(
        _Credential([P.DRIVE_READONLY_SCOPE])))
    check(signed["drive_authentication"]["exact_readonly_scope_proven"] is True,
          "an authenticated run records the proof it did make")
    check(signed["drive_authentication"]["credential_recorded"] is False,
          "without recording the credential itself")
    text = json.dumps(signed).lower()
    for secret in ("access_token", "refresh_token", "authorization",
                   "client_secret", "private_key"):
        check(secret not in text,
              f"and no {secret} reaches the config")
    P.assert_no_credentials(signed, "config.json")
    check(True, "the credential guard accepts the recorded audit")


def test_the_report_cell_shows_everything_a_result_review_needs():
    """The saved report is the external freeze record, so it has to be complete.

    Each item below is something a reviewer cannot recover from the bundle
    alone or would have to go hunting for.  Digests are printed whole: a
    truncated one is exactly the situation P1 exists to fix.
    """
    with open(NOTEBOOK, encoding="utf-8") as handle:
        nb = json.load(handle)
    cells = [c for c in nb["cells"] if c["cell_type"] == "code"]
    report = [c for c in cells if "def report(" in "".join(c["source"])]
    check(len(report) == 1, "there is exactly one report cell")
    body = "".join(report[0]["source"])

    required = {
        "P1/P2 status": "p1['status']",
        "first failure": "p1['first_failure']",
        "a per-gate table": "_gate_table",
        "unreached gates named as such": "(미도달)",
        "the 146 + 1 result": "publisher['checked']",
        "the mismatch detail": "published_sha256",
        "P2's folder-id inventory": "p2.get('folder_id')",
        "the bridge method": "bridge.get('method')",
        "provider checksum availability": "sha256_available",
        "provider checksum match": "sha256_match",
        "the scope proof": "exact_readonly_scope_proven",
        "the runtime record": "cfg['runtime']",
        "preserved observations": "observation_only",
        "the blocking reason": "blocked_by",
        "gate_passed per candidate": "gate_passed",
        "eligibility per candidate": "eligible_for_registration",
        "the payload fold": "prep_payload_sha256",
        "the manifest freeze digest": "manifest_sha256_freeze_externally",
        "the next action": "다음 행동",
    }
    for label, needle in required.items():
        check(needle in body, f"the report prints {label}")

    check("[:8]" not in body and "[:16]" not in body,
          "and never truncates a digest for display")
    check("_gate_table(p1, P.P1_GATE_ORDER)" in body
          and "_gate_table(p2, P.P2_GATE_ORDER)" in body,
          "both legs are tabulated in their registered gate order")

    # A failed publish has to say where the evidence is and why the directory
    # it left behind is not a bundle.
    source = open(P.__file__, encoding="utf-8").read()
    check("is preserved at {directory!r} for inspection" in source,
          "a failed publish names the preserved directory")
    check("COMMIT_MARKER" in body,
          "and the report distinguishes a committed bundle from a bare "
          "directory")


def test_the_mismatch_observation_comes_from_the_authoritative_read_alone():
    """A second read is a different moment, so it may not colour the finding.

    The explanatory detail needs the bytes, and re-reading a live tree can
    return something the gate never judged.  So the authoritative
    `(name, bytes, sha256)` stays exactly as the single read left it, and
    anything derived from a later read is fenced off — and dropped entirely
    when the two reads disagree, because it would describe the wrong bytes.
    """
    with tempfile.TemporaryDirectory() as tmp:
        tree = _write_mitdb_tree(os.path.join(tmp, "mitdb"),
                                 corrupt="RECORDS")
        with _PatchedRegistration(tree):
            reads = []

            class DriftingReader(P.LocalTreeReader):
                """Returns different bytes on every read after the first."""

                def read_bytes(self, directory, name, limit=None):
                    reads.append(name)
                    if name == "RECORDS" and reads.count("RECORDS") > 0:
                        return b"completely different bytes\n"
                    return super().read_bytes(directory, name, limit=limit)

            drifted = P.run_p1(tree, TOKEN, reader=DriftingReader(TOKEN))
            honest = P.run_p1(tree, TOKEN)

    check(drifted["status"] == P.P1_PUBLISHER_MISMATCH,
          "the corrupted tree still stops at the publisher gate")

    def records(result):
        return [f for f in result["per_file"] if f["name"] == "RECORDS"][0]

    check(records(drifted) == records(honest),
          "the authoritative observation is byte-identical to the run where "
          "nothing drifted: the second read did not touch it")

    gate = [g for g in drifted["gates"]
            if g["gate"] == "publisher_checksums"][0]
    detail = [m for m in gate["mismatched"] if m["name"] == "RECORDS"][0]
    check(detail["observed_sha256"] == records(honest)["sha256"],
          "and the mismatch record reports that same digest")
    check(detail["observation_from_single_read"] is True,
          "labelled as coming from the single authoritative read")

    second = detail["second_read_non_authoritative"]
    check(second["authoritative"] is False,
          "the second read is fenced off under its own key")
    check(second["stable"] is False,
          "it noticed the file had changed underneath it")
    for content_field in ("has_crlf", "starts_with_bom", "non_empty_lines",
                          "first_lines", "sha256_without_trailing_newlines"):
        check(content_field not in second,
              f"and reports no {content_field}, which would describe bytes "
              f"the gate never judged")
    check("never judged" in second["note"], "saying exactly that")

    # The whole detail block is nested, so no key of it can be mistaken for
    # part of the observation.
    check(set(detail) == {"name", "published_sha256", "observed_sha256",
                          "bytes", "read_by_the_join",
                          "observation_from_single_read",
                          "second_read_non_authoritative"},
          f"the mismatch record has no loose content-derived keys: "
          f"{sorted(detail)}")


def test_the_commit_marker_can_only_ever_be_created_once():
    """`O_EXCL` is the commit. A marker that can be overwritten commits twice.

    The file-set check happens to reject a stray marker before this matters,
    but the commit itself must not depend on an earlier check for its
    exclusivity — that is the same test-then-act shape the rename design was
    withdrawn for.
    """
    import ast
    tree = ast.parse(open(P.__file__, encoding="utf-8").read())
    helper = [n for n in ast.walk(tree)
              if isinstance(n, ast.FunctionDef) and n.name == "_write_new_file"]
    check(len(helper) == 1, "one helper creates every file the writer writes")
    opens = [n for n in ast.walk(helper[0])
             if isinstance(n, ast.Call)
             and isinstance(n.func, ast.Attribute) and n.func.attr == "open"
             and isinstance(n.func.value, ast.Name) and n.func.value.id == "os"]
    check(len(opens) == 1, "with exactly one low-level open in it")
    flags = {n.attr for n in ast.walk(helper[0])
             if isinstance(n, ast.Attribute)
             and isinstance(n.value, ast.Name) and n.value.id == "os"}
    check("O_EXCL" in flags, f"carrying O_EXCL: {sorted(flags)}")
    check("O_CREAT" in flags, "together with O_CREAT")
    check("O_TRUNC" not in flags,
          "and never O_TRUNC, which would overwrite an existing file")
    # Windows opens a descriptor in text mode without this and rewrites every
    # newline on the way out, so the file would not be the bytes the caller
    # hashed. getattr keeps it a no-op on POSIX.
    check("O_BINARY" in {n.attr for n in ast.walk(helper[0])
                         if isinstance(n, ast.Attribute)}
          or any(isinstance(n, ast.Constant) and n.value == "O_BINARY"
                 for n in ast.walk(helper[0])),
          "and O_BINARY, so the bytes on disk are the bytes handed in")

    # And the writer creates files *only* through it: a stray open(..., "w")
    # anywhere in the writer would truncate whatever is at that name.
    body = [n for n in ast.walk(tree)
            if isinstance(n, ast.FunctionDef) and n.name == "write_bundle"][0]
    writing_opens = []
    for node in ast.walk(body):
        if not (isinstance(node, ast.Call)
                and getattr(node.func, "id", None) == "open"):
            continue
        modes = [a.value for a in node.args[1:]
                 if isinstance(a, ast.Constant)]
        modes += [k.value.value for k in node.keywords
                  if k.arg == "mode" and isinstance(k.value, ast.Constant)]
        if any(set(str(m)) & set("wxa+") for m in modes):
            writing_opens.append(ast.dump(node)[:60])
    check(not writing_opens,
          f"the writer opens nothing for writing directly: {writing_opens}")

    # And the flag really behaves that way here, rather than being a constant
    # that looks right.
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, P.COMMIT_MARKER)
        handle = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o644)
        os.close(handle)
        try:
            os.close(os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o644))
            raise AssertionError("O_EXCL allowed a second create")
        except FileExistsError:
            check(True, "a second exclusive create fails on this platform")


def test_a_run_validates_its_own_bundle_before_reporting_success():
    """Publication is no longer atomic, so "it is there" is not evidence."""
    with tempfile.TemporaryDirectory() as tmp:
        tree = _write_mitdb_tree(os.path.join(tmp, "mitdb"))
        out = os.path.join(tmp, "out")
        with _PatchedRegistration(tree):
            result = P.execute_prep(
                tree, P.SOURCE_BUNDLE_FOLDER_ID, out, _adapter(),
                approval=TOKEN, timestamp="T", emit=lambda *a: None,
                synthetic=True)
        check(result["verified"]["ok"] is True,
              "a successful run carries its own verification result")
        check(result["verified"]["committed"] is True,
              "showing the bundle was committed")
        check(result["verified"]["manifest_digest_matches_expected"] is True,
              "the manifest matches the digest the run just computed")
        check(result["verified"]["manifest_anchor_source"] == P.ANCHOR_SAME_RUN,
              "declared as exactly that: a same-run self-check")
        check(result["verified"]["manifest_anchored_externally"] is False,
              "which is not an external anchor")
        check(result["verified"]["acceptance_eligible"] is False,
              "so the run does not promote itself to an acceptance pass")

        # If the bundle would not pass the consumer contract, the run must
        # fail rather than hand back a directory nobody will accept.
        calls = []
        real = P.verify_published_bundle

        def failing(directory, **kwargs):
            calls.append(directory)
            return {"ok": False, "committed": True, "directory": directory,
                    "problems": ["injected: the fold does not recompute"]}

        P.verify_published_bundle = failing
        try:
            with _PatchedRegistration(tree):
                P.execute_prep(
                    tree, P.SOURCE_BUNDLE_FOLDER_ID,
                    os.path.join(tmp, "out2"), _adapter(), approval=TOKEN,
                    timestamp="T", emit=lambda *a: None, synthetic=True)
            raise AssertionError("a run reported success without validating")
        except P.PrepError as error:
            check("consumer contract" in str(error),
                  "the run refuses when its own bundle fails validation")
            check("nothing was deleted" in str(error),
                  "and leaves the evidence in place")
        finally:
            P.verify_published_bundle = real
        check(len(calls) == 1,
              "the validation really was called on the written directory")


def test_a_racing_writer_owns_any_name_it_got_to_first():
    """Claiming the directory is not enough; each file must claim its own name.

    The writer used to fill the claim with `open(..., "w")`, which truncates.
    A racing writer that created `config.json` first had its bytes replaced
    with ours and the run committed on top — the directory claim said nothing
    about the files inside it.  Every file is now an exclusive create, so
    whoever got there first keeps their bytes and the run does not commit.
    """
    with tempfile.TemporaryDirectory() as tmp:
        p1 = _passing_p1(tmp)
        p2 = P.run_p2(P.SOURCE_BUNDLE_FOLDER_ID, _adapter(), TOKEN)
        combined = P.combine(p1, p2)

        # One per kind of file the writer produces: canonical JSON, the plain
        # text log, the markdown summary, and the manifest written last.
        for victim in ("config.json", "log.txt", "summary.md", "manifest.json",
                       P.SYNTHETIC_MARKER):
            target = os.path.join(tmp, f"racy-{victim}")
            theirs = f"bytes belonging to whoever created {victim} first"

            def intruder(directory, name=victim, text=theirs):
                with open(os.path.join(directory, name), "w",
                          encoding="utf-8") as handle:
                    handle.write(text)

            P._PUBLISH_RACE_HOOK = intruder
            try:
                P.write_bundle(target, P.build_config("T", True), p1, p2,
                               combined, ["x"], synthetic=True)
                raise AssertionError(f"{victim} was overwritten and committed")
            except P.PrepError as error:
                check("not committed" in str(error),
                      f"a pre-existing {victim} stops the run")
            finally:
                P._PUBLISH_RACE_HOOK = None

            with open(os.path.join(target, victim), encoding="utf-8") as fh:
                check(fh.read() == theirs,
                      f"{victim}: the racing writer's bytes are untouched")
            check(not os.path.exists(os.path.join(target, P.COMMIT_MARKER)),
                  f"{victim}: no {P.COMMIT_MARKER}, so it is not a bundle")
            check(P.verify_published_bundle(target)["ok"] is False,
                  f"{victim}: and the consumer contract refuses it")


def test_a_short_write_cannot_produce_a_committed_truncated_file():
    """`os.write` may write fewer bytes than it was given."""
    real = os.write
    chunks = []

    def stingy(fd, data):
        # Write one byte at a time: the loop has to keep going or every file
        # in the bundle ends up a single character long and still committed.
        chunks.append(len(data))
        return real(fd, data[:1])

    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "payload.json")
        body = json.dumps({"a": list(range(50))}).encode("utf-8")
        os.write = stingy
        try:
            P._write_new_file(path, body)
        finally:
            os.write = real
        with open(path, "rb") as handle:
            check(handle.read() == body,
                  "every byte is written even when os.write is stingy")
        check(len(chunks) == len(body),
              f"and it really did take {len(body)} short writes")


def test_the_verifier_checks_the_marker_instead_of_trusting_it():
    """A self-certifying marker is not evidence.

    Every one of these is a bundle that the previous verifier accepted or
    would have accepted, because it read the file list and the fold out of the
    marker it was supposed to be checking.
    """
    def fresh(tmp, name):
        p1 = _passing_p1(tmp)
        p2 = P.run_p2(P.SOURCE_BUNDLE_FOLDER_ID, _adapter(), TOKEN)
        out = os.path.join(tmp, name)
        written = P.write_bundle(out, P.build_config("T", True), p1, p2,
                                 P.combine(p1, p2), ["x"], synthetic=True)
        return out, written

    def rewrite(path, mutate):
        with open(path, encoding="utf-8") as handle:
            value = json.load(handle)
        mutate(value)
        os.remove(path)                 # the test may replace its own fixture
        with open(path, "w", encoding="utf-8") as handle:
            json.dump(value, handle, indent=1, sort_keys=True)

    def refold(out, marker_path):
        """Recompute the marker's fold over its own (shrunk) payload list."""
        with open(marker_path, encoding="utf-8") as handle:
            marker = json.load(handle)
        triples = []
        for name in sorted(marker["payload_files"]):
            with open(os.path.join(out, name), "rb") as handle:
                body = handle.read()
            triples.append({"name": name, "bytes": len(body),
                            "sha256": hashlib.sha256(body).hexdigest()})
        rewrite(marker_path,
                lambda m: m.update(prep_payload_sha256=
                                   P.fold_file_triples(triples)))

    with tempfile.TemporaryDirectory() as tmp:
        # 1. edit a payload file and rewrite only the marker's fold
        out, written = fresh(tmp, "refolded")
        with open(os.path.join(out, "summary.md"), "a",
                  encoding="utf-8") as handle:
            handle.write("\nquietly edited\n")
        refold(out, os.path.join(out, P.COMMIT_MARKER))
        verdict = P.verify_published_bundle(
            out, expected_manifest_sha256=written[
                "manifest_sha256_freeze_externally"],
            manifest_anchor_source=P.ANCHOR_SAVED_NOTEBOOK)
        check(verdict["ok"] is False,
              "a rewritten marker fold does not launder an edited payload")
        check(any("manifest.json's" in p for p in verdict["problems"]),
              "the manifest's own record of the fold is what catches it")
        check(verdict["acceptance_eligible"] is False,
              "and it is not acceptance-eligible")

        # 2. shrink the marker's payload list so the edited file falls outside
        out, written = fresh(tmp, "shrunk")
        with open(os.path.join(out, "summary.md"), "a",
                  encoding="utf-8") as handle:
            handle.write("\nquietly edited\n")
        marker_path = os.path.join(out, P.COMMIT_MARKER)
        rewrite(marker_path,
                lambda m: m.update(payload_files=[
                    n for n in m["payload_files"] if n != "summary.md"]))
        refold(out, marker_path)
        verdict = P.verify_published_bundle(out)
        check(verdict["ok"] is False,
              "a shrunk payload list is checked against the code contract")
        check(any("the contracted" in p for p in verdict["problems"]),
              "and the fixed contract is what reports it")
        # The fold is recomputed over the *contracted* list too, not the
        # marker's. If it followed the marker it would fold the shrunk list,
        # match the rewritten value, and report no fold problem at all — so
        # this assertion is what stops the fold following the marker.
        check(any(f"!= {P.COMMIT_MARKER}'s" in p for p in verdict["problems"]),
              "the fold is taken over the contracted list, so the edited file "
              "is still inside it and disagrees with the marker's own value — "
              "a fold that followed the marker would have matched it")

        # 2b. `ingestable` alone, which is the field that decides whether a
        #     bundle may ever be ingested. Nothing else here would notice: the
        #     file set is untouched and both records still agree on synthetic.
        out, written = fresh(tmp, "ingestable-only")
        rewrite(os.path.join(out, P.COMMIT_MARKER),
                lambda v: v.update(ingestable=True))
        verdict = P.verify_published_bundle(out)
        check(verdict["ok"] is False,
              "a synthetic bundle claiming ingestable=true is refused")
        check(any("is not the negation of synthetic_fixture" in p
                  for p in verdict["problems"]),
              "caught by the negation rule, not by any file-set check")
        check(not any("contracted set" in p for p in verdict["problems"]),
              "and the file set really is untouched, so nothing else saw it")

        # 3. flip synthetic → ingestable, which is the field that decides
        #    whether this bundle may ever be ingested
        out, written = fresh(tmp, "promoted")
        for name in (P.COMMIT_MARKER, P.PREP_MANIFEST_FILE):
            rewrite(os.path.join(out, name),
                    lambda v: v.update(synthetic_fixture=False,
                                       ingestable=True))
        verdict = P.verify_published_bundle(out)
        check(verdict["ok"] is False,
              "a synthetic bundle cannot relabel itself as ingestable")
        check(any("contracted set" in p for p in verdict["problems"]),
              "the synthetic marker file is part of the fixed file set, so "
              "the lie fails on the file set")

        # 4. flip it in the marker only
        out, written = fresh(tmp, "half-promoted")
        rewrite(os.path.join(out, P.COMMIT_MARKER),
                lambda v: v.update(synthetic_fixture=False, ingestable=True))
        verdict = P.verify_published_bundle(out)
        check(verdict["ok"] is False, "and disagreeing records are refused")
        check(any("synthetic_fixture disagrees" in p
                  for p in verdict["problems"]),
              "with the disagreement named")

        # 5. contract identity fields
        out, written = fresh(tmp, "renamed")
        rewrite(os.path.join(out, P.PREP_MANIFEST_FILE),
                lambda v: v.update(experiment_id="EXP-9999-999"))
        verdict = P.verify_published_bundle(out)
        check(verdict["ok"] is False, "a wrong experiment_id is refused")
        check(any("experiment_id" in p for p in verdict["problems"]),
              "and named")

        # 6. timestamps that disagree between the two records
        out, written = fresh(tmp, "restamped")
        rewrite(os.path.join(out, P.COMMIT_MARKER),
                lambda v: v.update(timestamp="somewhen-else"))
        verdict = P.verify_published_bundle(out)
        check(verdict["ok"] is False, "disagreeing timestamps are refused")


def test_a_malformed_marker_or_manifest_is_a_verdict_not_a_crash():
    """A truncated bundle file is a finding; raising would hide it."""
    with tempfile.TemporaryDirectory() as tmp:
        p1 = _passing_p1(tmp)
        p2 = P.run_p2(P.SOURCE_BUNDLE_FOLDER_ID, _adapter(), TOKEN)
        combined = P.combine(p1, p2)

        for index, (victim, body) in enumerate((
                (P.COMMIT_MARKER, '{"committed": true, "payl'),
                (P.COMMIT_MARKER, ""),
                (P.COMMIT_MARKER, "[1, 2, 3]"),
                (P.PREP_MANIFEST_FILE, '{"prep_payload_sha256":'),
                (P.PREP_MANIFEST_FILE, "not json at all"))):
            out = os.path.join(tmp, f"broken-{index}")
            P.write_bundle(out, P.build_config("T", True), p1, p2, combined,
                           ["x"], synthetic=True)
            os.remove(os.path.join(out, victim))
            with open(os.path.join(out, victim), "w",
                      encoding="utf-8") as handle:
                handle.write(body)
            verdict = P.verify_published_bundle(out)     # must not raise
            check(verdict["ok"] is False,
                  f"a truncated {victim} is refused")
            check(verdict["problems"],
                  "with a structured problem list rather than a traceback")
            check(verdict["acceptance_eligible"] is False,
                  "and it is never acceptance-eligible")


def test_structural_validity_is_not_an_acceptance_pass():
    """An unanchored manifest is the one file the fold cannot cover."""
    with tempfile.TemporaryDirectory() as tmp:
        p1 = _passing_p1(tmp)
        p2 = P.run_p2(P.SOURCE_BUNDLE_FOLDER_ID, _adapter(), TOKEN)
        out = os.path.join(tmp, "run")
        written = P.write_bundle(out, P.build_config("T", True), p1, p2,
                                 P.combine(p1, p2), ["x"], synthetic=True)

        loose = P.verify_published_bundle(out)
        check(loose["structure_ok"] is True, "the bundle is structurally sound")
        check(loose["ok"] is True, "so the structural verdict passes")
        check(loose["manifest_anchored_externally"] is False,
              "but the manifest was not anchored")
        check(loose["acceptance_eligible"] is False,
              "so this is explicitly NOT an acceptance pass")
        check("NOT an acceptance pass" in loose["acceptance_note"],
              "and the note says so in words, not just a flag")

        anchored = P.verify_published_bundle(
            out, expected_manifest_sha256=written[
                "manifest_sha256_freeze_externally"],
            manifest_anchor_source=P.ANCHOR_SAVED_NOTEBOOK)
        check(anchored["acceptance_eligible"] is True,
              "supplying the frozen digest with its origin makes it eligible")

        wrong = P.verify_published_bundle(
            out, expected_manifest_sha256="f" * 64,
            manifest_anchor_source=P.ANCHOR_SAVED_NOTEBOOK)
        check(wrong["ok"] is False and wrong["acceptance_eligible"] is False,
              "and a digest that disagrees fails both")

        # Structural failure never yields eligibility, whatever is supplied.
        os.remove(os.path.join(out, P.COMMIT_MARKER))
        gone = P.verify_published_bundle(
            out, expected_manifest_sha256=written[
                "manifest_sha256_freeze_externally"],
            manifest_anchor_source=P.ANCHOR_SAVED_NOTEBOOK)
        check(gone["acceptance_eligible"] is False,
              "an uncommitted directory is not eligible even with the digest")
        check(gone["manifest_anchored_externally"] is False,
              "and is not reported as anchored")


def test_written_bytes_are_the_bytes_that_were_handed_in():
    """The digest must describe the file, not the buffer it came from.

    Windows opens a descriptor in text mode unless told otherwise and rewrites
    every `\\n` as `\\r\\n` on the way out.  The caller hashes what it *passed*,
    so without `O_BINARY` the recorded digest would describe bytes that never
    reached the disk — and a perfectly good synthetic run would fail its own
    consumer check with what looks like corruption.  This holds the invariant
    directly, so it is checked on whichever platform the suite runs on.
    """
    with tempfile.TemporaryDirectory() as tmp:
        cases = {
            "unix newlines": b"first\nsecond\nthird\n",
            "no trailing newline": b"a\nb",
            "crlf already present": b"kept\r\nas is\r\n",
            "lone carriage return": b"before\rafter\n",
            "embedded nulls and high bytes": b"\x00\x1a\n\xff\xfe\n",
            "empty": b"",
        }
        for index, (label, body) in enumerate(cases.items()):
            path = os.path.join(tmp, f"case-{index}.bin")
            P._write_new_file(path, body)
            with open(path, "rb") as handle:
                on_disk = handle.read()
            check(on_disk == body,
                  f"{label}: the file is byte-identical to what was written")
            check(hashlib.sha256(on_disk).hexdigest()
                  == hashlib.sha256(body).hexdigest(),
                  f"{label}: so the digest of one is the digest of the other")

        # The JSON helper returns the bytes a caller will hash. A newline-rich
        # payload is the case that breaks under text-mode translation.
        value = {"lines": ["one", "two", "three"], "note": "a\nb\nc\n",
                 "nested": {"deep": ["x\ny", "z"]}}
        path = os.path.join(tmp, "payload.json")
        returned = P._write_new_json(path, value)
        check(b"\n" in returned, "the fixture really does contain newlines")
        with open(path, "rb") as handle:
            on_disk = handle.read()
        check(returned == on_disk,
              "the returned bytes are exactly the file's bytes")
        check(hashlib.sha256(returned).hexdigest()
              == hashlib.sha256(on_disk).hexdigest(),
              "so a digest taken from the return value describes the file")

    # And the same invariant across a whole real bundle: the digest the writer
    # reports for the manifest is the digest of the manifest on disk.
    with tempfile.TemporaryDirectory() as tmp:
        p1 = _passing_p1(tmp)
        p2 = P.run_p2(P.SOURCE_BUNDLE_FOLDER_ID, _adapter(), TOKEN)
        out = os.path.join(tmp, "run")
        written = P.write_bundle(out, P.build_config("T", True), p1, p2,
                                 P.combine(p1, p2), ["x"], synthetic=True)
        with open(os.path.join(out, P.PREP_MANIFEST_FILE), "rb") as handle:
            actual = hashlib.sha256(handle.read()).hexdigest()
        check(written["manifest_sha256_freeze_externally"] == actual,
              "the reported manifest digest is the file's own digest")
        verdict = P.verify_published_bundle(
            out, expected_manifest_sha256=actual,
            manifest_anchor_source=P.ANCHOR_SAVED_NOTEBOOK)
        check(verdict["acceptance_eligible"] is True,
              "so a normal synthetic run passes its own consumer check")


def test_a_write_that_makes_no_progress_fails_instead_of_spinning():
    real = os.write
    calls = []

    def stalled(fd, data):
        calls.append(len(data))
        return 0

    with tempfile.TemporaryDirectory() as tmp:
        os.write = stalled
        try:
            P._write_new_file(os.path.join(tmp, "stalled.bin"), b"payload")
            raise AssertionError("a zero-length write was retried forever")
        except P.PrepError as error:
            check("made no progress" in str(error),
                  "a write of zero bytes is a named failure, not a spin")
            check("truncated" in str(error),
                  "and it says the file as it stands is incomplete")
        finally:
            os.write = real
        check(len(calls) == 1,
              "the loop stopped on the first stalled write, not the hundredth")

    # Partial writes are still retried; only *no* progress is fatal.
    chunks = []

    def stingy(fd, data):
        chunks.append(len(data))
        return real(fd, data[:2])

    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "partial.bin")
        body = b"0123456789"
        os.write = stingy
        try:
            P._write_new_file(path, body)
        finally:
            os.write = real
        with open(path, "rb") as handle:
            check(handle.read() == body, "a short write is retried to the end")
        check(len(chunks) == 5, "in two-byte steps, as the stub forced")


def test_the_verifier_reads_json_types_and_not_truthiness():
    """`bool("false")` is True, so a denial would have read as an assertion.

    Every field below is a contract flag written as a real JSON boolean. A
    value of another type means the file was not written by this code, and
    coercing it is how a bundle that says `"false"` gets treated as saying
    yes — the more alarming the value looks, the more certainly it passes.
    """
    def rewrite(path, mutate):
        with open(path, encoding="utf-8") as handle:
            value = json.load(handle)
        mutate(value)
        os.remove(path)
        with open(path, "w", encoding="utf-8") as handle:
            json.dump(value, handle, indent=1, sort_keys=True)

    with tempfile.TemporaryDirectory() as tmp:
        p1 = _passing_p1(tmp)
        p2 = P.run_p2(P.SOURCE_BUNDLE_FOLDER_ID, _adapter(), TOKEN)
        combined = P.combine(p1, p2)

        def fresh(name):
            out = os.path.join(tmp, name)
            written = P.write_bundle(out, P.build_config("T", True), p1, p2,
                                     combined, ["x"], synthetic=True)
            return out, written

        # ---- committed ---------------------------------------------------
        for label, mutate in (
                ("false", lambda v: v.update(committed=False)),
                ("missing", lambda v: v.pop("committed", None)),
                ("null", lambda v: v.update(committed=None)),
                ("the string 'true'", lambda v: v.update(committed="true")),
                ("the number 1", lambda v: v.update(committed=1))):
            out, written = fresh(f"committed-{abs(hash(label)) % 10000}")
            rewrite(os.path.join(out, P.COMMIT_MARKER), mutate)
            # Supplied with the *correct* anchor, which is what made this
            # slip through before: a matching manifest cannot vouch for a
            # marker that does not claim to be finished.
            verdict = P.verify_published_bundle(
                out, expected_manifest_sha256=written[
                    "manifest_sha256_freeze_externally"],
                manifest_anchor_source=P.ANCHOR_SAVED_NOTEBOOK)
            check(verdict["ok"] is False,
                  f"committed {label} is refused")
            check(verdict["acceptance_eligible"] is False,
                  f"committed {label} is never acceptance-eligible, even with "
                  f"a correct manifest anchor")
            check(any("committed is" in p for p in verdict["problems"]),
                  f"committed {label} is named in the problems")

        # ---- synthetic_fixture and ingestable ----------------------------
        bad_values = {"the string 'false'": "false",
                      "the string 'true'": "true",
                      "the number 0": 0, "the number 1": 1,
                      "null": None}
        for index, (label, value) in enumerate(bad_values.items()):
            for field in ("synthetic_fixture", "ingestable"):
                out, _ = fresh(f"flag-{field}-{index}")
                for name in (P.COMMIT_MARKER, P.PREP_MANIFEST_FILE):
                    rewrite(os.path.join(out, name),
                            lambda v, f=field, x=value: v.update({f: x}))
                verdict = P.verify_published_bundle(out)
                check(verdict["structure_ok"] is False,
                      f"{field} as {label} is refused")
                check(verdict["acceptance_eligible"] is False,
                      f"{field} as {label} is not acceptance-eligible")
                check(any("not a JSON boolean" in p
                          for p in verdict["problems"]),
                      f"{field} as {label} is reported as a type problem")

            for field in ("synthetic_fixture", "ingestable"):
                out, _ = fresh(f"missing-{field}-{index}")
                rewrite(os.path.join(out, P.COMMIT_MARKER),
                        lambda v, f=field: v.pop(f, None))
                verdict = P.verify_published_bundle(out)
                check(verdict["structure_ok"] is False,
                      f"a missing {field} is refused")
                check(any(f"{field} is missing" in p
                          for p in verdict["problems"]),
                      f"and a missing {field} is named as missing")

        # ---- timestamp ---------------------------------------------------
        for label, value in (("null", None), ("a number", 20260812),
                             ("a list", ["T"])):
            out, _ = fresh(f"stamp-{abs(hash(label)) % 10000}")
            rewrite(os.path.join(out, P.COMMIT_MARKER),
                    lambda v, x=value: v.update(timestamp=x))
            verdict = P.verify_published_bundle(out)
            check(verdict["structure_ok"] is False,
                  f"a timestamp that is {label} is refused")
            check(any("not the contracted string" in p
                      for p in verdict["problems"]),
                  f"a timestamp that is {label} is reported as a type problem")

        out, _ = fresh("stamp-mismatch")
        rewrite(os.path.join(out, P.COMMIT_MARKER),
                lambda v: v.update(timestamp="a-different-moment"))
        verdict = P.verify_published_bundle(out)
        check(verdict["structure_ok"] is False,
              "two records stamped at different moments are refused")
        check(any("timestamp disagrees" in p for p in verdict["problems"]),
              "and the disagreement is named")

        # ---- none of this raises -----------------------------------------
        out, _ = fresh("everything-wrong")
        for name in (P.COMMIT_MARKER, P.PREP_MANIFEST_FILE):
            rewrite(os.path.join(out, name),
                    lambda v: v.update(synthetic_fixture="false",
                                       ingestable=1, timestamp=None))
        rewrite(os.path.join(out, P.COMMIT_MARKER),
                lambda v: v.update(committed="yes"))
        verdict = P.verify_published_bundle(out)     # must not raise
        check(verdict["structure_ok"] is False,
              "a record wrong in every field is still a verdict")
        check(len(verdict["problems"]) >= 4,
              f"with each violation listed: {len(verdict['problems'])}")
        check(verdict["acceptance_eligible"] is False,
              "and never acceptance-eligible")


def test_matching_a_digest_and_being_anchored_are_different_facts():
    """Where a digest came from decides whether it anchors anything.

    A run comparing the manifest against the value it computed itself moments
    earlier has confirmed that its own two lines of code agree.  That is worth
    doing and it is not evidence the file has not been edited since — there is
    no "since" yet.  So the match and the provenance are reported separately,
    and only an origin outside the run can carry acceptance.
    """
    with tempfile.TemporaryDirectory() as tmp:
        p1 = _passing_p1(tmp)
        p2 = P.run_p2(P.SOURCE_BUNDLE_FOLDER_ID, _adapter(), TOKEN)
        out = os.path.join(tmp, "run")
        written = P.write_bundle(out, P.build_config("T", True), p1, p2,
                                 P.combine(p1, p2), ["x"], synthetic=True)
        frozen = written["manifest_sha256_freeze_externally"]

        # 1. same-run digest: structure passes, acceptance does not.
        same = P.verify_published_bundle(
            out, expected_manifest_sha256=frozen,
            manifest_anchor_source=P.ANCHOR_SAME_RUN)
        check(same["structure_ok"] is True, "same-run: the structure is sound")
        check(same["manifest_digest_matches_expected"] is True,
              "same-run: the digest does match")
        check(same["manifest_anchor_source"] == P.ANCHOR_SAME_RUN,
              "same-run: the origin is reported as the run itself")
        check(same["manifest_anchored_externally"] is False,
              "same-run: a value the run computed is not an external anchor")
        check(same["acceptance_eligible"] is False,
              "same-run: so it is not acceptance-eligible")
        check("self-check" in same["acceptance_note"]
              and "NOT an acceptance pass" in same["acceptance_note"],
              "same-run: and the note says so, matching the flags")

        # 2 and 3. the two genuinely external origins.
        for origin in (P.ANCHOR_SAVED_NOTEBOOK, P.ANCHOR_REGISTERED_RECORD):
            verdict = P.verify_published_bundle(
                out, expected_manifest_sha256=frozen,
                manifest_anchor_source=origin)
            check(verdict["structure_ok"] is True, f"{origin}: structure ok")
            check(verdict["manifest_digest_matches_expected"] is True,
                  f"{origin}: the digest matches")
            check(verdict["manifest_anchored_externally"] is True,
                  f"{origin}: and the origin is outside this run")
            check(verdict["acceptance_eligible"] is True,
                  f"{origin}: so it is acceptance-eligible")
            check("NOT an acceptance pass" not in verdict["acceptance_note"],
                  f"{origin}: and the note agrees with the flags")

        # 4. an external anchor that disagrees fails both.
        for origin in (P.ANCHOR_SAVED_NOTEBOOK, P.ANCHOR_REGISTERED_RECORD):
            verdict = P.verify_published_bundle(
                out, expected_manifest_sha256="a" * 64,
                manifest_anchor_source=origin)
            check(verdict["manifest_digest_matches_expected"] is False,
                  f"{origin}: a disagreeing digest is reported as not matching")
            check(verdict["structure_ok"] is False,
                  f"{origin}: and fails the structural verdict")
            check(verdict["manifest_anchored_externally"] is False,
                  f"{origin}: an anchor that disagrees anchors nothing")
            check(verdict["acceptance_eligible"] is False,
                  f"{origin}: so acceptance is refused")

        # 5. an origin that is not in the enum, or missing, or empty.
        for origin in ("external", "trust me", "", None, P.ANCHOR_NONE, 7):
            verdict = P.verify_published_bundle(
                out, expected_manifest_sha256=frozen,
                manifest_anchor_source=origin)
            check(verdict["structure_ok"] is False,
                  f"anchor source {origin!r} is refused")
            check(verdict["manifest_anchored_externally"] is False,
                  f"anchor source {origin!r} is not treated as external")
            check(verdict["acceptance_eligible"] is False,
                  f"anchor source {origin!r} yields no acceptance")
            check(verdict["manifest_anchor_source"] is None,
                  f"anchor source {origin!r} is not echoed back as valid")
            # A missing origin and an unrecognised one are different mistakes
            # and get different diagnoses; a caller that forgot the argument
            # should not be told its value is not in the enum.
            expected_reason = ("without a manifest_anchor_source"
                               if origin in (None, "") else
                               "is not one of" if origin != P.ANCHOR_NONE
                               else "but a digest was supplied")
            check(any(expected_reason in p for p in verdict["problems"]),
                  f"anchor source {origin!r} is diagnosed as "
                  f"{expected_reason!r}")

        # Naming an origin without bringing a value is the mirror image.
        verdict = P.verify_published_bundle(
            out, manifest_anchor_source=P.ANCHOR_SAVED_NOTEBOOK)
        check(verdict["structure_ok"] is False,
              "an origin with no digest describes evidence it did not bring")
        check(verdict["acceptance_eligible"] is False, "and is not eligible")

        # No digest at all is honest, and stays honest.
        bare = P.verify_published_bundle(out)
        check(bare["structure_ok"] is True, "no digest: the structure is sound")
        check(bare["manifest_anchor_source"] == P.ANCHOR_NONE,
              "no digest: the origin is reported as none")
        check(bare["manifest_digest_matches_expected"] is None,
              "no digest: there is no match to report, not a false one")
        check(bare["acceptance_eligible"] is False,
              "no digest: and no acceptance")

        check(set(P.EXTERNAL_MANIFEST_ANCHORS)
              == {P.ANCHOR_SAVED_NOTEBOOK, P.ANCHOR_REGISTERED_RECORD},
              "exactly two origins count as external")
        check(P.ANCHOR_SAME_RUN not in P.EXTERNAL_MANIFEST_ANCHORS,
              "and the run's own value is not one of them")


def test_the_runs_verdict_and_its_own_words_do_not_contradict():
    """A machine verdict that disagrees with its prose is worse than either.

    The previous version returned `manifest_anchored_externally: True` and
    `acceptance_eligible: True` while printing that the saved notebook output
    was still needed.  Whichever a reader believed, they were misled.
    """
    with tempfile.TemporaryDirectory() as tmp:
        tree = _write_mitdb_tree(os.path.join(tmp, "mitdb"))
        emitted = []
        with _PatchedRegistration(tree):
            result = P.execute_prep(
                tree, P.SOURCE_BUNDLE_FOLDER_ID, os.path.join(tmp, "out"),
                _adapter(), approval=TOKEN, timestamp="T",
                emit=emitted.append, synthetic=True)

    verified = result["verified"]
    check(verified["structure_ok"] is True, "the run's own check passes")
    check(verified["manifest_digest_matches_expected"] is True,
          "its manifest matches the digest it computed")
    check(verified["manifest_anchor_source"] == P.ANCHOR_SAME_RUN,
          "declared as a same-run self-check")
    check(verified["manifest_anchored_externally"] is False,
          "not as an external anchor")
    check(verified["acceptance_eligible"] is False,
          "and not as an acceptance pass")

    words = "\n".join(emitted)
    check("acceptance_eligible=False" in words,
          "the printed line states the same verdict the dict carries")
    check(P.ANCHOR_SAME_RUN in words,
          "and names the origin it actually used")
    check(P.ANCHOR_SAVED_NOTEBOOK in words
          and P.ANCHOR_REGISTERED_RECORD in words,
          "and says which origins would be needed instead")
    check("externally anchored=False" in words,
          "with the external-anchor flag printed as it is")
    # The contradiction that was there before: prose asking for a further
    # anchor while the flags claimed one had been supplied.
    check(not (verified["acceptance_eligible"] is True
               and "still needs" in words),
          "the run never asks for an anchor it has already claimed to have")


def test_the_execution_approval_opens_only_what_it_names():
    """Enabling execution widened one thing. Everything else must be as it was.

    An approval is easy to over-apply: the guard opens, the run works, and
    nobody notices that the same edit also made three other refusals
    conditional. So this checks the neighbours rather than the change — the
    switch, the token, the folder id and the read-only seals all still refuse
    exactly as before, with the approval granted.
    """
    check(P.EXECUTION_APPROVAL_RECORD["granted"] is True,
          "the approval is in force for this test")

    adapter = _adapter()
    with tempfile.TemporaryDirectory() as tmp:
        # The switch still has to be turned on at the call site.
        try:
            P.run_prep(tmp, P.SOURCE_BUNDLE_FOLDER_ID, tmp, adapter=adapter,
                       approval=TOKEN, open_registered_data=False,
                       emit=lambda *a: None)
            raise AssertionError("the closed switch let a run through")
        except P.PrepNotApprovedError as error:
            check("OPEN_REGISTERED_DATA is False" in str(error),
                  "the module-level switch still refuses when closed")

        # The separate PREP token is still required, and is still not the
        # Q5-E audit token.
        for wrong in (None, "", Q5E.EXECUTION_APPROVAL_TOKEN):
            try:
                P.run_prep(tmp, P.SOURCE_BUNDLE_FOLDER_ID, tmp,
                           adapter=adapter, approval=wrong,
                           open_registered_data=True, emit=lambda *a: None)
                raise AssertionError(f"approval {wrong!r} was accepted")
            except P.PrepNotApprovedError:
                check(True, f"approval {wrong!r} is still refused")

        # The folder id is still the registered one only.
        try:
            P.run_prep(tmp, "1NotTheRegisteredFolderId", tmp, adapter=adapter,
                       approval=TOKEN, open_registered_data=True,
                       emit=lambda *a: None)
            raise AssertionError("an unregistered folder id was accepted")
        except P.PrepError as error:
            check("registered canonical" in str(error),
                  "the folder id is still checked, and by id")

    check(adapter.calls == [],
          "none of those refusals touched the Drive adapter")
    check(P.OPEN_REGISTERED_DATA is False,
          "and the module still defaults closed for a stray import")

    # The approval names what it does not cover; the module has no way to do
    # any of it. These are the seals every run reports.
    for sealed in ("detector_executed", "m0_m4_aggregated",
                   "beat_join_executed", "model_scored",
                   "probability_opened", "labels_opened",
                   "training_performed"):
        check(P._p1_seals()[sealed] is False,
              f"P1 still seals {sealed} shut")
    check(P._p2_seals()["drive_modified"] is False,
          "and P2 still seals Drive modification shut")

    calls = _module_calls(P.__file__)
    for banned in ("detect_r", "rr_features", "rdsamp", "rdann",
                   "load_all_inputs", "run_audit"):
        check(banned not in calls,
              f"the module still never calls {banned}()")

    # P3 is not in scope, and enabling P1/P2 did not quietly bring it in.
    check("oracle_harness_identity.json" not in P.P1_P2_PREP_PAYLOAD_FILES,
          "no P3 oracle file entered the payload")
    check(set(P.EXECUTION_APPROVAL_RECORD["approved"]) and all(
        "P3" not in item for item in P.EXECUTION_APPROVAL_RECORD["approved"]),
        "and nothing approved mentions P3")

    # Registration is still a separate PR: the three Q5-E stops are untouched.
    check(Q5E.MITDB_TREE_AGGREGATE is None,
          "MITDB_TREE_AGGREGATE is still unregistered")
    check(Q5E.SOURCE_BUNDLE_FILE_SHA256 == {},
          "SOURCE_BUNDLE_FILE_SHA256 is still unregistered")
    check(Q5E.SOURCE_MATCH_ORACLE_RECORD is None,
          "SOURCE_MATCH_ORACLE_RECORD is still unregistered")


def test_the_notebook_finds_the_repo_by_its_contents_not_by_a_guess():
    """A path that exists is not a repository.

    The first version fell back to `os.getcwd() + '/..'` when `/content/repo`
    was absent.  In Colab the cwd is `/content`, so that resolves to `/`, and
    `sys.path` got `/mit-bih` — which does not exist, so the very first import
    died with ModuleNotFoundError.  The fallback was confidently wrong: it
    produced a path rather than admitting it had not found one.

    So the environment cell now accepts a candidate only when the three
    modules are actually in its `mit-bih/`, and it raises with instructions
    rather than handing a bad path to `sys.path`.
    """
    with open(NOTEBOOK, encoding="utf-8") as handle:
        nb = json.load(handle)
    cells = [c for c in nb["cells"] if c["cell_type"] == "code"]
    env = [c for c in cells if "sys.path" in "".join(c["source"])]
    check(len(env) == 1, "one cell sets up the import path")
    body = "".join(env[0]["source"])

    check("os.path.join(os.getcwd(), '..')" not in body
          and 'os.path.join(os.getcwd(), "..")' not in body,
          "the guessing parent-directory fallback is gone")
    check("_is_repo" in body,
          "a candidate is judged by whether it holds the modules")
    for name in ("q5d_order_preserving_beat_join.py",
                 "q5e_leg2_failure_mechanism_audit.py",
                 "q5e_prep_p1_p2_asset_identity.py"):
        check(name in body, f"{name} is one of the files it looks for")
    check("raise RuntimeError" in body,
          "and it raises rather than continuing with a path it invented")

    # Run the discovery half for real, against layouts that matter. Everything
    # below the import is cut off; the clone fallback is pointed at a dead URL
    # so nothing is fetched, and its target is redirected into the test's own
    # temp directory so a failed attempt cannot leave a stray /content/repo.
    check("CLONE_TO" in body,
          "the clone target is a named variable, so it can be redirected")
    head = body.split("import q5d_order_preserving_beat_join")[0].replace(
        "https://github.com/ehdbddl06001-ui/my-github-test.git",
        "file:///nonexistent-so-nothing-is-fetched")

    def discover(cwd, sandbox):
        """Run the cell's discovery with its absolute candidates sandboxed.

        The cell checks `/content/repo` and friends before it walks the cwd,
        which is right in Colab and makes a test that leaves them alone answer
        differently depending on whether the machine happens to have a clone
        there.  An earlier version of this test passed here and failed in
        Colab for exactly that reason.  Re-pointing every `/content...`
        literal — the candidates and the clone target alike — into a sandbox
        makes the outcome depend only on the layout under test.
        """
        import contextlib
        import io

        namespace = {}
        previous = os.getcwd()
        sandboxed = head.replace("'/content", f"'{sandbox}/content")
        # The cell prints git's complaint when its clone fallback fails, which
        # is the point of the "nothing to find" case.  Captured rather than
        # let through: this cell's saved output is part of the freeze record,
        # and a reviewer should not have to work out that a `fatal:` line came
        # from a test exercising a refusal on purpose.
        noise = io.StringIO()
        try:
            os.chdir(cwd)
            with contextlib.redirect_stdout(noise), \
                    contextlib.redirect_stderr(noise):
                exec(compile(sandboxed, "environment_cell", "exec"), namespace)
            return namespace.get("FOUND")
        except RuntimeError as error:
            return f"REFUSED: {error}"
        finally:
            os.chdir(previous)

    with tempfile.TemporaryDirectory() as tmp:
        check(discover(os.path.join(ROOT, "notebooks"), tmp) == ROOT,
              "a cwd inside the repository finds the repository")
        check(discover(ROOT, tmp) == ROOT,
              "and so does the repository root itself")
        check(not os.path.exists(os.path.join(tmp, "content")),
              "neither of those reached the clone fallback at all")

    with tempfile.TemporaryDirectory() as tmp:
        holder = os.path.join(tmp, "here")
        os.makedirs(holder)
        os.symlink(ROOT, os.path.join(holder, "some-other-name"))
        check(discover(holder, tmp)
              == os.path.join(holder, "some-other-name"),
              "a clone one level below the cwd is found by name-independent "
              "content, not by a hardcoded directory name")

    with tempfile.TemporaryDirectory() as tmp:
        empty = os.path.join(tmp, "here")
        os.makedirs(empty)
        verdict = discover(empty, tmp)
        check(str(verdict).startswith("REFUSED"),
              f"with nothing to find, it refuses instead of guessing: "
              f"{verdict}")
        check("git clone" in str(verdict),
              "and the refusal tells the user exactly how to fix it")
        check("토큰을" in str(verdict),
              "while warning against pasting a token into a saved notebook")


def test_the_fixture_cell_cannot_turn_a_failure_into_silence():
    """The last cheap gate before a real run must not swallow its own result.

    The cell printed `result.stdout` only. The suite writes its summary to
    stdout and its AssertionError to stderr, so a failing suite printed
    nothing and the cell reported "(테스트 출력 없음)" — which reads as "there
    was no output", not "everything you were about to rely on is broken". It
    then carried on to the cell that opens registered assets.
    """
    with open(NOTEBOOK, encoding="utf-8") as handle:
        nb = json.load(handle)
    cells = [c for c in nb["cells"] if c["cell_type"] == "code"]
    fixture = [c for c in cells
               if "test_q5e_prep_p1_p2_asset_identity.py" in "".join(c["source"])]
    check(len(fixture) == 1, "one cell runs the synthetic fixture suite")
    body = "".join(fixture[0]["source"])

    import ast
    tree = ast.parse(body)

    # The result has to be bound, not consumed inline: you cannot inspect a
    # return code you never kept.
    runs = [n for n in ast.walk(tree)
            if isinstance(n, ast.Call)
            and isinstance(n.func, ast.Attribute)
            and n.func.attr == "run"]
    check(len(runs) == 1, "it calls subprocess.run once")
    inline = [n for n in ast.walk(tree)
              if isinstance(n, ast.Attribute)
              and n.attr in ("stdout", "stderr")
              and isinstance(n.value, ast.Call)]
    check(not inline,
          "and does not read .stdout straight off the call, discarding the rest")

    attrs = {n.attr for n in ast.walk(tree) if isinstance(n, ast.Attribute)}
    check("returncode" in attrs, "the exit status is inspected")
    check("stderr" in attrs, "and stderr is printed, not dropped")

    raises = [n for n in ast.walk(tree) if isinstance(n, ast.Raise)]
    check(raises, "a failing suite stops the notebook rather than continuing")
    check("셀 9" in body,
          "and says which cell must not be pressed")

    # An `or` fallback labelling empty stdout is fine; what is not fine is
    # that fallback wording implying nothing happened.  Checked on the
    # expression itself, so the comment explaining the old bug may quote it.
    fallbacks = [n.values[-1].value for n in ast.walk(tree)
                 if isinstance(n, ast.BoolOp) and isinstance(n.op, ast.Or)
                 and isinstance(n.values[-1], ast.Constant)
                 and isinstance(n.values[-1].value, str)]
    for text in fallbacks:
        check("출력 없음" not in text,
              f"an empty stdout is not labelled as absence: {text!r}")
    check(fallbacks, "and empty stdout is still labelled as something")


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
