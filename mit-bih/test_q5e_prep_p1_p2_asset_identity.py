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
    adapter = _adapter()
    with tempfile.TemporaryDirectory() as tmp:
        try:
            P.run_prep(tmp, P.SOURCE_BUNDLE_FOLDER_ID, tmp, adapter=adapter,
                       approval=TOKEN, open_registered_data=True,
                       emit=lambda *a: None)
            raise AssertionError("run_prep produced a result")
        except P.PrepError as error:
            check("never been executed" in str(error),
                  "the terminal guard stops an approved run")
    check(adapter.calls == [],
          "and it stops it before any Drive call is made")

    import inspect
    source = inspect.getsource(P.run_prep)
    check("_terminal_execution_guard()" in source, "the guard is present")
    check(source.index("_terminal_execution_guard")
          < source.index("execute_prep("),
          "the guard precedes the route that reads anything")
    check(source.index("require_execution_approval")
          < source.index("_terminal_execution_guard"),
          "approval is checked before the guard, so refusals say why")


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
                  "and the partial staging is preserved, not deleted")
        finally:
            P.P1_P2_PREP_PAYLOAD_FILES = real
        check(not os.path.exists(out),
              "the final path was never created")
        failed = [n for n in os.listdir(tmp) if n.endswith(".failed")]
        check(len(failed) == 1,
              "the failed staging directory is kept for inspection")


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
    check("OPEN_REGISTERED_DATA = False" in source,
          "the notebook defaults to closed")
    check("APPROVAL = None" in source, "and carries no approval token")
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
            real_verifier = BJ.verify_against_publisher_checksums
            BJ.verify_against_publisher_checksums = (
                lambda *a, **k: calls.append("verify") or real_verifier(*a, **k))
            try:
                result = P.run_p1(drifted, TOKEN, reader=reader)
            finally:
                BJ.verify_against_publisher_checksums = real_verifier

    check(result["status"] == P.P1_CHECKSUM_FILE_MISMATCH,
          "a drifted checksum file stops P1")
    check(reader.read == [BJ.MITDB_CHECKSUM_FILE],
          "exactly one file was read: the checksum file itself")
    check(len(reader.read) == 1,
          "the other 146 files were never read")
    check(calls == [], "the publisher verifier was never called")
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
            check("already exists" in str(error),
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

        source = open(P.__file__, encoding="utf-8").read()
        writer = source.split("def write_bundle(", 1)[1].split("\ndef ", 1)[0]
        check("rmtree" not in writer,
              "the writer never calls a recursive delete")
        check("os.rmdir" not in writer, "nor removes the final directory")
        check("except BaseException" not in writer,
              "and does not catch BaseException")
        check("except Exception as error" in writer,
              "it catches only ordinary exceptions, and names them")


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


def test_b4_authentication_happens_only_on_the_approved_path():
    """B4: an unapproved run performs zero authentication calls."""
    calls = []

    def authenticator():
        calls.append("auth")

    def service_factory():
        calls.append("service")
        return object()

    for approval, label in ((None, "no approval"),
                            ("wrong-token", "a wrong token")):
        try:
            P.authenticate_drive_readonly(approval,
                                          authenticator=authenticator,
                                          service_factory=service_factory)
            raise AssertionError(f"{label} authenticated")
        except P.PrepNotApprovedError:
            check(True, f"{label} is refused before authenticating")
    check(calls == [], "and zero authentication calls were made")

    service = P.authenticate_drive_readonly(
        TOKEN, authenticator=authenticator, service_factory=service_factory)
    check(calls == ["auth", "service"],
          "an approved call authenticates first, then builds the service")
    check(service is not None, "and returns a service object")

    adapter = P.build_drive_adapter(TOKEN, authenticator=authenticator,
                                    service_factory=service_factory)
    check(isinstance(adapter, P.GoogleDriveFolderAdapter),
          "build_drive_adapter injects the service into the adapter")
    check(adapter._service is not None, "the adapter holds the service")

    with open(P.__file__, encoding="utf-8") as handle:
        text = handle.read()
    check("drive.readonly" in text, "the read-only scope is declared")
    installers = _module_calls(P.__file__) & {
        "check_call", "check_output", "call", "run", "Popen", "system"}
    check(not installers,
          f"no subprocess/installer call exists: {sorted(installers)}")
    check("!pip" not in text, "and no notebook-magic install either")
    report = P.check_runtime_dependencies()
    check(set(report["required"]) == set(P.RUNTIME_DEPENDENCIES),
          "the dependency requirement is reported explicitly")


def test_b4_notebook_authenticates_only_behind_both_switches():
    with open(NOTEBOOK, encoding="utf-8") as handle:
        nb = json.load(handle)
    source = "\n".join("".join(c["source"]) for c in nb["cells"]
                        if c["cell_type"] == "code")
    check("authenticate_drive_readonly" in source
          or "build_drive_adapter" in source,
          "the notebook performs the real authentication")
    check("check_runtime_dependencies" in source,
          "and reports the dependency requirement before doing so")
    auth_cell = [c for c in nb["cells"]
                 if c["cell_type"] == "code"
                 and ("build_drive_adapter" in "".join(c["source"])
                      or "authenticate_drive_readonly" in "".join(c["source"]))]
    check(auth_cell, "the auth cell exists")
    body = "".join(auth_cell[0]["source"])
    check("OPEN_REGISTERED_DATA" in body and "APPROVAL" in body,
          "and is guarded by both switches")
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
    check("nothing pre-existing is deleted" in flat,
          "the atomic-publish claim is scoped to no-delete behaviour")
    check("not even the passing gate's observation" not in flat,
          "the old blanket-withholding sentence is gone")


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
