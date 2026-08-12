"""Synthetic and contract tests for EXP-2026-009, the null artifact repair.

Every fixture is invented.  Shard payloads are built from the frozen module's
own `shard_digest()` over `J` values this file makes up, so no test can pass by
recognising a real number, and no test opens a registered artifact: the guard
is closed for the whole file except where a test deliberately opens it against
temp directories, and a final test asserts it is closed again at the end.

Run: `python mit-bih/test_q5d_null_artifact_repair.py`
"""

from __future__ import annotations

import contextlib
import hashlib
import io
import json
import os
import struct
import sys
import tempfile
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import q5d_order_preserving_beat_join as BJ              # noqa: E402
import q5d_null_artifact_repair as R                     # noqa: E402

PASSED = 0
TOTAL = 20                       # replicates in the synthetic null
SHARD_SIZE = 5                   # → four shards
FAMILIES = list(R.REGISTERED_FAMILIES)
EXPECTED = {BJ.shard_filename(s, min(s + SHARD_SIZE, TOTAL)):
            (s, min(s + SHARD_SIZE, TOTAL))
            for s in range(0, TOTAL, SHARD_SIZE)}


def check(condition: bool, label: str) -> None:
    global PASSED
    if not condition:
        raise AssertionError(label)
    PASSED += 1


# ─────────────────────────────────────────────────────────────────────────────
# Fixtures
# ─────────────────────────────────────────────────────────────────────────────
def _identity(code_sha256=None, input_digest="d" * 64, split=None):
    """The four identity fields a manifest carries, defaulting to registered."""
    return {"split": split or R.REGISTERED_SPLIT,
            "code_sha256": code_sha256 or R.FROZEN_Q5D_SHA256_LF,
            "input_digest": input_digest,
            "rule_fingerprint": R.REGISTERED_RULE_FINGERPRINT}


def _j_value(family: str, replicate: int) -> float:
    """A distinct, ordered value per (family, replicate).

    Arranged so the winning family varies with the replicate — a maximum check
    that only ever sees one winner would not notice a reconstruction that took
    the wrong array.
    """
    base = 0.1 + 0.001 * replicate
    offset = {"wrong_record": 0.0, "order_shuffle": 0.02,
              "circular_shift": 0.04}[family]
    if replicate % 3 == 0:
        offset = 0.06 - offset
    return round(base + offset, 12)


def _shard_payload(identity, start, end, families=None, maxima=None,
                   overrides=None):
    """One shard, digested by the frozen module's own function."""
    values = {f: [_j_value(f, b) for b in range(start, end)] for f in FAMILIES}
    if families is not None:
        values.update(families)
    payload = {
        "null_runner_version": R.REGISTERED_NULL_RUNNER_VERSION,
        "split": identity["split"], "families": list(R.REGISTERED_FAMILIES),
        "master_seed": R.REGISTERED_MASTER_SEED,
        "rule_fingerprint": identity["rule_fingerprint"],
        "code_sha256": identity["code_sha256"],
        "input_digest": identity["input_digest"],
        "replicate_start": start, "replicate_end": end,
        "j": {f: list(values[f]) for f in FAMILIES},
        "j_null_max": list(maxima) if maxima is not None else [
            max(values[f][k] for f in FAMILIES) for k in range(end - start)],
        "worker_count": 1, "git_commit": None,
    }
    payload.update(overrides or {})
    payload["digest"] = BJ.shard_digest(payload)
    return payload


def _write_shards(directory, identity, skip=(), payloads=None, raw=None):
    os.makedirs(directory, exist_ok=True)
    for name, (start, end) in EXPECTED.items():
        if (start, end) in skip:
            continue
        path = os.path.join(directory, name)
        if raw and name in raw:
            with open(path, "w", encoding="utf-8") as handle:
                handle.write(raw[name])
            continue
        payload = (payloads or {}).get((start, end)) \
            or _shard_payload(identity, start, end)
        with open(path, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, sort_keys=True, ensure_ascii=False)


def _expected_arrays(total=TOTAL):
    arrays = {R.MEMBER_NAME_BY_FAMILY[f]: [_j_value(f, b) for b in range(total)]
              for f in FAMILIES}
    arrays[R.MAX_MEMBER_NAME] = [
        max(_j_value(f, b) for f in FAMILIES) for b in range(total)]
    return arrays


def _write_source_bundle(directory, identity, summary=None, omit=(), extra=(),
                         manifest_extra=None):
    """The eleven files.  Content is filler except manifest and null_summary."""
    os.makedirs(directory, exist_ok=True)
    arrays = _expected_arrays()
    manifest = dict(identity)
    manifest.update({"experiment_id": "EXP-2026-007", "stage": "DS1_GATE"})
    manifest.update(manifest_extra or {})
    if summary is None:
        summary = {"replicates": TOTAL, "families": list(R.REGISTERED_FAMILIES),
                   "master_seed": R.REGISTERED_MASTER_SEED,
                   "rule_fingerprint": identity["rule_fingerprint"],
                   "j_null_max": list(arrays[R.MAX_MEMBER_NAME])}
    for name in R.SOURCE_BUNDLE_FILES:
        if name in omit:
            continue
        if name == R.MANIFEST_FILE:
            body = json.dumps(manifest, sort_keys=True).encode("utf-8")
        elif name == R.SUMMARY_FILE:
            body = json.dumps(summary, sort_keys=True).encode("utf-8")
        else:
            body = f"filler for {name}\n".encode("utf-8")
        with open(os.path.join(directory, name), "wb") as handle:
            handle.write(body)
    for name in extra:
        with open(os.path.join(directory, name), "wb") as handle:
            handle.write(b"unexpected\n")
    return {"manifest": manifest, "summary": summary, "arrays": arrays}


class FakeDrive(R.FolderInventoryAdapter):
    """A folder-id inventory built from a directory on disk.

    It answers only for ids it was given, so a test that asks for the wrong id
    gets nothing back — which is the behaviour a real folder id has and the
    reason names are never used to find a folder.
    """

    def __init__(self, folders=None, calls=None):
        self.folders = dict(folders or {})
        self.calls = calls if calls is not None else []

    def add_directory(self, folder_id, directory, provider_sha=True,
                      provider_md5=False, mutate=None):
        children = []
        for index, name in enumerate(sorted(os.listdir(directory))):
            path = os.path.join(directory, name)
            if not os.path.isfile(path):
                continue
            with open(path, "rb") as handle:
                body = handle.read()
            child = {"id": f"{folder_id}-file-{index:03d}", "name": name,
                     "size": str(len(body)), "mimeType": "application/json",
                     "trashed": False}
            if provider_sha:
                child["sha256Checksum"] = hashlib.sha256(body).hexdigest()
            if provider_md5:
                child["md5Checksum"] = hashlib.md5(body).hexdigest()
            children.append(child)
        if mutate:
            children = mutate(children)
        self.folders[folder_id] = children
        return self

    def list_children(self, folder_id):
        self.calls.append(folder_id)
        return list(self.folders.get(folder_id, []))


@contextlib.contextmanager
def approved():
    """Open the terminal guard for one test, then close it again.

    The module ships with `granted: False` and must still be closed when this
    file finishes — a test that left execution enabled would hand the next
    reader a module whose guard is open for reasons nothing records.
    """
    R.EXECUTION_APPROVAL_RECORD["granted"] = True
    try:
        yield R.EXECUTION_APPROVAL_TOKEN
    finally:
        R.EXECUTION_APPROVAL_RECORD["granted"] = False


@contextlib.contextmanager
def _repair_world(identity=None, provider_sha=True, bridge=True, **kwargs):
    """A shard folder, a source bundle, a runs parent and a fake Drive."""
    identity = identity or _identity()
    with tempfile.TemporaryDirectory() as tmp:
        runs = os.path.join(tmp, "runs")
        os.makedirs(runs)
        shard_dir = os.path.join(tmp, "shards")
        source = os.path.join(runs, R.SOURCE_BUNDLE_RUN)
        target = os.path.join(runs, "20260813T000000_corrective")
        _write_shards(shard_dir, identity, **kwargs)
        built = _write_source_bundle(source, identity)
        drive = None
        if bridge:
            drive = (FakeDrive()
                     .add_directory(R.SHARD_FOLDER_ID, shard_dir,
                                    provider_sha=provider_sha)
                     .add_directory(R.SOURCE_BUNDLE_FOLDER_ID, source,
                                    provider_sha=provider_sha))
            drive.folders[R.RUNS_PARENT_FOLDER_ID] = []
        yield {"tmp": tmp, "runs": runs, "shards": shard_dir,
               "source": source, "target": target, "drive": drive,
               "identity": identity, "built": built}


# ─────────────────────────────────────────────────────────────────────────────
# The guard
# ─────────────────────────────────────────────────────────────────────────────
def test_the_module_ships_unapproved_and_refuses_everything():
    check(R.EXECUTION_APPROVAL_RECORD["granted"] is False,
          "the shipped approval record is closed")
    check(R.EXECUTION_APPROVAL_RECORD["granted_on"] is None
          and R.EXECUTION_APPROVAL_RECORD["granted_by"] is None
          and R.EXECUTION_APPROVAL_RECORD["pinned_commit"] is None,
          "and records no approver and no pinned commit, because there is none")
    check("execution approved: False" in R.design_card(),
          "the design card says so out loud")

    with tempfile.TemporaryDirectory() as tmp:
        for call in (
            lambda: R.qualify_shards(tmp, _identity(),
                                     R.EXECUTION_APPROVAL_TOKEN),
            lambda: R.read_source_snapshot(tmp, R.EXECUTION_APPROVAL_TOKEN),
            lambda: R.bridge_mount_to_folder_id(FakeDrive(), "x", tmp, (),
                                                R.EXECUTION_APPROVAL_TOKEN),
            lambda: R.confirm_folder_id_of_child(FakeDrive(), "x", "y",
                                                 R.EXECUTION_APPROVAL_TOKEN),
            lambda: R.run_repair(tmp, tmp, os.path.join(tmp, "out"),
                                 R.EXECUTION_APPROVAL_TOKEN),
        ):
            try:
                call()
                raise AssertionError("ran with the guard closed")
            except R.RepairNotApprovedError as error:
                check(error.reason == R.NOT_APPROVED,
                      "the terminal guard refuses even with a valid token")
        check(not os.listdir(tmp), "and nothing was created on the way")


def test_a_wrong_token_is_refused_before_the_guard_is_reached():
    with tempfile.TemporaryDirectory() as tmp, approved():
        for token in (None, "",
                      "q5e-prep-p1-p2-read-only-execution-approved-by-user"):
            try:
                R.qualify_shards(tmp, _identity(), token)
                raise AssertionError(f"accepted {token!r}")
            except R.RepairNotApprovedError:
                check(True, f"{token!r} is refused")
        check(R.EXECUTION_APPROVAL_TOKEN
              != "q5e-prep-p1-p2-read-only-execution-approved-by-user",
              "and the PREP's token is not this module's token")


# ─────────────────────────────────────────────────────────────────────────────
# A — the newline convention behind the registered SHA
# ─────────────────────────────────────────────────────────────────────────────
def test_lf_and_crlf_share_a_registered_identity_but_not_a_raw_digest():
    """The whole reason the convention has to be stated.

    The same file checked out on Windows is different bytes.  If identity were
    the raw digest, a Windows checkout of the frozen module would look like a
    different module; if the raw digest were not also reported, a reader could
    not tell a checkout difference from a genuine one.
    """
    lf = b"line one\nline two\nline three\n"
    crlf = b"line one\r\nline two\r\nline three\r\n"
    left, right = R.digest_pair(lf), R.digest_pair(crlf)
    check(left["lf_normalized_sha256"] == right["lf_normalized_sha256"],
          "LF and CRLF normalise to one registered identity")
    check(left["raw_sha256"] != right["raw_sha256"],
          "while the raw digests stay distinct")
    check(left["had_crlf"] is False and right["had_crlf"] is True,
          "and each says which it was")
    check(left["registered_identity_uses"] == "lf_normalized_sha256",
          "the report names the convention rather than leaving it implicit")
    check(right["raw_bytes"] > right["lf_normalized_bytes"],
          "the CRLF file is longer raw than normalised")


def test_a_lone_cr_is_refused_rather_than_folded():
    """Folding it would let two different files share one identity."""
    for payload in (b"a\rb\n", b"trailing\r", b"\r"):
        try:
            R.normalise_newlines(payload, "fixture")
            raise AssertionError(f"folded {payload!r}")
        except R.RepairError as error:
            check(error.reason == R.UNDEFINED_NEWLINE,
                  f"{payload!r} is refused as an undefined newline")
    check(R.normalise_newlines(b"a\r\nb\n") == b"a\nb\n",
          "CRLF is still folded")
    check(R.normalise_newlines(b"") == b"", "and an empty file is fine")


def test_the_frozen_module_identity_is_asserted_on_the_normalised_digest():
    digests = R.frozen_q5d_digests()
    check(digests["lf_normalized_sha256"] == R.FROZEN_Q5D_SHA256_LF,
          "the imported frozen module normalises to the registered value")
    check(R.FROZEN_Q5D_SHA256_LF.startswith("6b098c67df3c"),
          "which is the hash embedded in the shard folder's name")
    check("raw_sha256" in digests and len(str(digests["raw_sha256"])) == 64,
          "and the raw digest is reported alongside")
    frozen = R.assert_frozen_q5d_unchanged()
    check(frozen["rule_fingerprint"] == R.REGISTERED_RULE_FINGERPRINT,
          "the live rule fingerprint is checked in the same place")

    original = R.FROZEN_Q5D_SHA256_LF
    R.FROZEN_Q5D_SHA256_LF = "0" * 64
    try:
        R.assert_frozen_q5d_unchanged()
        raise AssertionError("a moved module was accepted")
    except R.RepairError as error:
        check(error.reason == R.FROZEN_MODULE_MOVED,
              "a module that is not the registered one is a stop")
        check("raw bytes" in str(error),
              "and the stop reports both digests, so a CRLF checkout is "
              "distinguishable from a real change")
    finally:
        R.FROZEN_Q5D_SHA256_LF = original


def test_artifact_identities_cover_module_spec_and_notebook():
    """H — after a pinned checkout, the files on disk are re-checked."""
    identities = R.artifact_identities(ROOT)
    check(sorted(identities) == ["module", "notebook", "spec"],
          "all three artifacts are identified")
    for label, entry in identities.items():
        check(len(str(entry["lf_normalized_sha256"])) == 64
              and len(str(entry["raw_sha256"])) == 64,
              f"{label} carries both digests")
        check(os.path.exists(os.path.join(ROOT, str(entry["path"]))),
              f"{label} points at a file that exists")


# ─────────────────────────────────────────────────────────────────────────────
# B — the Drive folder-id bridge
# ─────────────────────────────────────────────────────────────────────────────
def test_the_bridge_ties_a_mount_to_a_folder_id_by_content():
    with _repair_world() as world, approved() as token:
        bridge = R.bridge_mount_to_folder_id(
            world["drive"], R.SOURCE_BUNDLE_FOLDER_ID, world["source"],
            R.SOURCE_BUNDLE_FILES, token)
        check(bridge["bridged"] is True, "the mount is tied to the folder id")
        check(bridge["folder_id"] == R.SOURCE_BUNDLE_FOLDER_ID,
              "by id, not by name")
        check("folder id" in bridge["method"]
              and "not a name search" in bridge["method"],
              "and the method says so")
        check(len(bridge["files"]) == len(R.SOURCE_BUNDLE_FILES),
              "every expected file was bridged")
        check(all("provider_sha256" in row["matched_on"]
                  for row in bridge["files"]),
              "each matched on its provider checksum where one exists")
        check(bridge["checksum_coverage"]["provider_sha256"]
              == len(R.SOURCE_BUNDLE_FILES),
              "and the coverage is reported rather than assumed")
        check(world["drive"].calls == [R.SOURCE_BUNDLE_FOLDER_ID],
              "exactly one folder-id query was made")


def test_a_same_named_folder_is_never_accepted_as_a_substitute():
    """The substitution the folder-id rule exists to prevent."""
    with _repair_world() as world, approved() as token:
        impostor = os.path.join(world["tmp"], "impostor")
        _write_source_bundle(impostor, world["identity"])
        with open(os.path.join(impostor, "summary.md"), "ab") as handle:
            handle.write(b"different content\n")
        try:
            R.bridge_mount_to_folder_id(
                world["drive"], R.SOURCE_BUNDLE_FOLDER_ID, impostor,
                R.SOURCE_BUNDLE_FILES, token)
            raise AssertionError("a different folder bridged to the id")
        except R.RepairError as error:
            check(error.reason == R.INPUT_UNQUALIFIED,
                  "content that does not match the folder id is refused")
            check("substitute" in str(error),
                  "and the message names the failure mode")


def test_the_bridge_refuses_every_ambiguity_category():
    with _repair_world() as world, approved() as token:
        source = world["source"]
        cases = {
            "duplicate_name": lambda c: c + [dict(c[0])],
            "subfolder": lambda c: c + [{"id": "sub", "name": "extra",
                                         "mimeType": R.DRIVE_FOLDER_MIME}],
            "shortcut": lambda c: c + [{"id": "sc", "name": "link",
                                        "mimeType": R.DRIVE_SHORTCUT_MIME,
                                        "size": "1"}],
            "trashed": lambda c: c + [{"id": "tr", "name": "gone",
                                       "size": "1", "trashed": True}],
            "nameless": lambda c: c + [{"id": "nn", "name": "", "size": "1"}],
            "sizeless": lambda c: c + [{"id": "sz", "name": "unsized"}],
        }
        for label, mutate in cases.items():
            drive = FakeDrive().add_directory(R.SOURCE_BUNDLE_FOLDER_ID,
                                              source, mutate=mutate)
            try:
                R.bridge_mount_to_folder_id(
                    drive, R.SOURCE_BUNDLE_FOLDER_ID, source,
                    R.SOURCE_BUNDLE_FILES, token)
                raise AssertionError(f"{label} was accepted")
            except R.RepairError as error:
                check(error.reason == R.INPUT_UNQUALIFIED,
                      f"{label} makes the inventory ambiguous and stops")


def test_a_provider_checksum_mismatch_stops_the_bridge():
    with _repair_world() as world, approved() as token:
        def corrupt(children):
            for child in children:
                if child["name"] == R.MANIFEST_FILE:
                    child["sha256Checksum"] = "0" * 64
            return children
        drive = FakeDrive().add_directory(R.SOURCE_BUNDLE_FOLDER_ID,
                                          world["source"], mutate=corrupt)
        try:
            R.bridge_mount_to_folder_id(drive, R.SOURCE_BUNDLE_FOLDER_ID,
                                        world["source"],
                                        R.SOURCE_BUNDLE_FILES, token)
            raise AssertionError("a checksum mismatch bridged")
        except R.RepairError as error:
            check(error.reason == R.INPUT_UNQUALIFIED,
                  "a provider sha256 that disagrees with the mount stops it")


def test_an_absent_provider_checksum_is_recorded_not_invented():
    with _repair_world(provider_sha=False) as world, approved() as token:
        bridge = R.bridge_mount_to_folder_id(
            world["drive"], R.SOURCE_BUNDLE_FOLDER_ID, world["source"],
            R.SOURCE_BUNDLE_FILES, token)
        check(all(row["provider_sha256"] == "unavailable"
                  for row in bridge["files"]),
              "an absent checksum is 'unavailable', never a guess")
        check(bridge["checksum_coverage"]["size_and_name_only"]
              == len(R.SOURCE_BUNDLE_FILES),
              "and the weaker match is counted, so a reviewer sees it")


def test_an_unknown_folder_id_returns_nothing_and_stops():
    with _repair_world() as world, approved() as token:
        try:
            R.bridge_mount_to_folder_id(world["drive"], "not-a-real-id",
                                        world["source"],
                                        R.SOURCE_BUNDLE_FILES, token)
            raise AssertionError("an unknown folder id bridged")
        except R.RepairError as error:
            check(error.reason == R.INPUT_UNQUALIFIED,
                  "an id with no children cannot be bridged to a full mount")


def test_the_new_folder_id_is_read_back_rather_than_assumed():
    """H — a result must be identifiable by id, not picked later by name."""
    with _repair_world() as world, approved() as token:
        world["drive"].folders[R.RUNS_PARENT_FOLDER_ID] = [
            {"id": "new-folder-id", "name": "20260813T000000_corrective",
             "mimeType": R.DRIVE_FOLDER_MIME, "trashed": False}]
        confirmed = R.confirm_folder_id_of_child(
            world["drive"], R.RUNS_PARENT_FOLDER_ID,
            "20260813T000000_corrective", token)
        check(confirmed["folder_id"] == "new-folder-id",
              "the corrective folder's own id comes back from Drive")

        world["drive"].folders[R.RUNS_PARENT_FOLDER_ID].append(
            {"id": "second", "name": "20260813T000000_corrective",
             "mimeType": R.DRIVE_FOLDER_MIME, "trashed": False})
        try:
            R.confirm_folder_id_of_child(world["drive"],
                                         R.RUNS_PARENT_FOLDER_ID,
                                         "20260813T000000_corrective", token)
            raise AssertionError("two folders of one name were resolved")
        except R.RepairError as error:
            check(error.reason == R.INPUT_UNQUALIFIED,
                  "two folders sharing a name cannot identify a result")


# ─────────────────────────────────────────────────────────────────────────────
# C — the exact shard contract
# ─────────────────────────────────────────────────────────────────────────────
def test_the_production_shard_set_is_exactly_the_preregistered_hundred():
    check(R.EXPECTED_SHARD_COUNT == 100, "exactly 100 shards")
    check(R.EXPECTED_SHARD_FILENAMES[0] == "null_shard_00000_00100.json",
          "the first is null_shard_00000_00100.json")
    check(R.EXPECTED_SHARD_FILENAMES[-1] == "null_shard_09900_10000.json",
          "the last is null_shard_09900_10000.json")
    check(len(set(R.EXPECTED_SHARD_FILENAMES)) == 100, "with no duplicates")
    check(all(end - start == 100 for start, end in R.EXPECTED_SHARD_RANGES),
          "each covering exactly 100 replicates")
    check(R.EXPECTED_SHARD_RANGES[-1][1] == R.N_REPLICATES,
          "and together exactly the registered 10,000")
    check(R.expected_shard_set()[R.EXPECTED_SHARD_FILENAMES[0]] == (0, 100),
          "the filename→range map agrees with the plan")


def test_a_complete_consistent_shard_set_qualifies():
    with _repair_world() as world, approved() as token:
        out = R.qualify_shards(world["shards"], world["identity"], token,
                               world["drive"], R.SHARD_FOLDER_ID,
                               total=TOTAL, expected=EXPECTED)
        report = out["report"]
        check(report["qualified"] is True, "a clean set qualifies")
        check(report["observed_file_count"] == len(EXPECTED),
              "every shard was read")
        check(report["missing_files"] == [] and report["extra_files"] == []
              and report["subdirectories"] == [],
              "nothing missing, extra or nested")
        check(report["coverage"]["ok"] is True
              and report["coverage"]["covered"] == TOTAL,
              "coverage is exactly 0..n-1")
        check(report["folder_id_bridge"]["bridged"] is True,
              "and the shard folder was tied to its registered folder id")
        check(report["identity_anchor"]
              == "folder-id-verified bundle manifest.json",
              "the report says what identity was checked against")
        check(report["registered_input_digest"] is None
              and "no repo-side registered value"
              in str(report["input_digest_registration"]),
              "and it states plainly that input_digest has no registered "
              "counterpart yet, rather than pretending to check one")


def test_missing_extra_duplicate_and_nested_shards_are_all_refused():
    identity = _identity()
    with approved() as token:
        with _repair_world(identity, skip=((5, 10),)) as world:
            try:
                R.qualify_shards(world["shards"], identity, token, None,
                                 total=TOTAL, expected=EXPECTED)
                raise AssertionError("a missing shard qualified")
            except R.RepairError as error:
                check(error.reason == R.INPUT_UNQUALIFIED,
                      "a missing preregistered shard file is refused")
                check("missing" in str(error), "and is named as missing")

        with _repair_world(identity) as world:
            with open(os.path.join(world["shards"], "null_shard_extra.json"),
                      "w", encoding="utf-8") as handle:
                handle.write("{}")
            try:
                R.qualify_shards(world["shards"], identity, token, None,
                                 total=TOTAL, expected=EXPECTED)
                raise AssertionError("an extra shard qualified")
            except R.RepairError as error:
                check(error.reason == R.INPUT_UNQUALIFIED,
                      "an unexpected file in the shard folder is refused")

        with _repair_world(identity) as world:
            os.makedirs(os.path.join(world["shards"], "nested"))
            try:
                R.qualify_shards(world["shards"], identity, token, None,
                                 total=TOTAL, expected=EXPECTED)
                raise AssertionError("a subfolder qualified")
            except R.RepairError as error:
                check(error.reason == R.INPUT_UNQUALIFIED,
                      "a subdirectory in the shard folder is refused")


def test_malformed_json_becomes_a_structured_stop_not_a_raw_exception():
    """The thing this function exists to detect must not arrive as a crash."""
    identity = _identity()
    broken = {"null_shard_00000_00005.json": "{not json at all",
              }
    with _repair_world(identity, raw=broken) as world, approved() as token:
        try:
            R.qualify_shards(world["shards"], identity, token, None,
                             total=TOTAL, expected=EXPECTED)
            raise AssertionError("malformed JSON qualified")
        except R.RepairError as error:
            check(error.reason == R.INPUT_UNQUALIFIED,
                  "malformed JSON is REPAIR_INPUT_UNQUALIFIED")
            check("malformed" in str(error),
                  "and is described rather than re-raised")
        except ValueError:
            raise AssertionError("a raw JSONDecodeError escaped")


def test_shard_fields_are_checked_for_type_and_format_not_truthiness():
    """`str(None)` is a non-empty string; a presence check would pass it."""
    identity = _identity()
    bad_values = {
        "code_sha256": "not-a-digest",
        "rule_fingerprint": None,
        "input_digest": 12345,
        "split": "DS2",
        "master_seed": "2026017",
        "null_runner_version": "1",
        "families": ["wrong_record"],
    }
    for field, value in bad_values.items():
        payload = _shard_payload(identity, 0, SHARD_SIZE,
                                 overrides={field: value})
        problems = R.validate_shard_schema(payload, "fixture.json", identity,
                                           (0, SHARD_SIZE))
        check(any(field in p for p in problems),
              f"{field}={value!r} is caught by the schema check")
    check(R.validate_shard_schema([], "fixture.json", identity, (0, 5)),
          "a JSON array where an object belongs is caught")
    check(not R.validate_shard_schema(
        _shard_payload(identity, 0, SHARD_SIZE), "fixture.json", identity,
        (0, SHARD_SIZE)),
        "and a well-formed shard produces no problems")


def test_is_hex64_rejects_what_a_truthiness_check_would_accept():
    for value in ("None", "", None, 0, True, "g" * 64, "a" * 63, "A" * 64,
                  ["a" * 64]):
        check(not R.is_hex64(value), f"{value!r} is not a 64-hex digest")
    check(R.is_hex64("a" * 64) and R.is_hex64(R.FROZEN_Q5D_SHA256_LF),
          "and a real digest is")


def test_a_shard_from_another_run_or_another_rule_is_refused():
    with approved() as token:
        foreign = _identity(code_sha256="e" * 64)
        with _repair_world(foreign) as world:
            try:
                R.qualify_shards(world["shards"], foreign, token, None,
                                 total=TOTAL, expected=EXPECTED)
                raise AssertionError("another run's shards qualified")
            except R.RepairError as error:
                check(error.reason == R.INPUT_UNQUALIFIED,
                      "a shard set whose code_sha256 is not the registered "
                      "one is refused even when it is self-consistent")


def test_an_edited_shard_fails_its_own_digest():
    identity = _identity()
    with _repair_world(identity) as world, approved() as token:
        path = os.path.join(world["shards"], "null_shard_00000_00005.json")
        payload = json.load(open(path, encoding="utf-8"))
        payload["j"]["wrong_record"][0] += 0.5          # digest not updated
        with open(path, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, sort_keys=True)
        try:
            R.qualify_shards(world["shards"], identity, token, None,
                             total=TOTAL, expected=EXPECTED)
            raise AssertionError("an edited shard qualified")
        except R.RepairError as error:
            check(error.reason == R.INPUT_UNQUALIFIED,
                  "an edited shard fails its own digest")


def test_a_shard_whose_max_is_wrong_is_refused():
    identity = _identity()
    wrong = _shard_payload(identity, 0, SHARD_SIZE, maxima=[0.0] * SHARD_SIZE)
    with _repair_world(identity, payloads={(0, SHARD_SIZE): wrong}) as world, \
            approved() as token:
        try:
            R.qualify_shards(world["shards"], identity, token, None,
                             total=TOTAL, expected=EXPECTED)
            raise AssertionError("a wrong maximum qualified")
        except R.RepairError as error:
            check(error.reason == R.INPUT_UNQUALIFIED,
                  "a shard whose maximum is not the family maximum is refused")


def test_the_manifest_must_carry_registered_values_not_just_strings():
    for field, value in (("split", "DS2"),
                         ("code_sha256", "a" * 64),
                         ("rule_fingerprint", "b" * 64),
                         ("input_digest", "short")):
        manifest = _identity()
        manifest[field] = value
        try:
            R.identity_from_manifest(manifest)
            raise AssertionError(f"accepted {field}={value!r}")
        except R.RepairError as error:
            check(error.reason == R.INPUT_UNQUALIFIED,
                  f"the manifest's {field} is checked against the registered "
                  f"value, not merely for being a string")
    check(R.identity_from_manifest(_identity()) == _identity(),
          "and a registered manifest passes")


# ─────────────────────────────────────────────────────────────────────────────
# The identity-only context (Codex decision 1)
# ─────────────────────────────────────────────────────────────────────────────
def test_finalisation_never_reads_the_join_inputs():
    """The runtime invariant that makes an identity-only context legitimate."""
    identity = _identity()
    context = R.identity_only_context(identity)
    check(isinstance(context, BJ.NullContext),
          "it is a real NullContext, not a stand-in")
    for name in ("mamba_by_record", "cache_by_record", "processed_classes",
                 "mamba_classes"):
        book = getattr(context, name)
        check(isinstance(book, R._UnreadMapping) and len(book) == 0,
              f"{name} is empty and refuses to be read")
        try:
            book["100"]
            raise AssertionError(f"{name} did not refuse")
        except AssertionError as error:
            check("read join input" in str(error),
                  f"and {name} says so when something tries")

    shards = {(s, e): _shard_payload(identity, s, e)
              for s, e in EXPECTED.values()}
    families = BJ.finalize_null_shards(shards, context, total=TOTAL)
    check(sorted(families) == sorted(FAMILIES),
          "the frozen finaliser assembles every family from identity alone")
    check(all(len(families[f]) == TOTAL for f in FAMILIES),
          "with every replicate present")


def test_a_moved_rule_fingerprint_stops_the_context():
    identity = _identity()
    identity["rule_fingerprint"] = "f" * 64
    try:
        R.identity_only_context(identity)
        raise AssertionError("a foreign rule fingerprint was accepted")
    except R.RepairError as error:
        check(error.reason == R.INPUT_UNQUALIFIED,
              "the live fingerprint must equal the bundle's")


# ─────────────────────────────────────────────────────────────────────────────
# Reconstruction
# ─────────────────────────────────────────────────────────────────────────────
def test_reconstruction_returns_the_four_arrays_in_canonical_order():
    identity = _identity()
    shards = {(s, e): _shard_payload(identity, s, e)
              for s, e in EXPECTED.values()}
    arrays = R.reconstruct_arrays(shards, R.identity_only_context(identity),
                                  total=TOTAL)
    expected = _expected_arrays()
    check(sorted(arrays) == sorted(R.NPZ_ARRAYS),
          "exactly the four contracted names")
    for name in R.NPZ_ARRAYS:
        check(arrays[name] == expected[name],
              f"{name} is assembled in replicate order")
    members = [R.MEMBER_NAME_BY_FAMILY[f] for f in FAMILIES]
    check(all(arrays[R.MAX_MEMBER_NAME][b]
              == max(arrays[m][b] for m in members) for b in range(TOTAL)),
          "and the maximum is the per-replicate family maximum")
    winners = {max(members, key=lambda m: arrays[m][b]) for b in range(TOTAL)}
    check(len(winners) > 1,
          "the fixture is not degenerate: the winning family varies")


def test_the_member_naming_conflict_is_recorded_and_not_guessed():
    """Codex's review named members that exist nowhere in the frozen module.

    Which frozen family each proposed name denotes is not recorded anywhere, so
    adopting them would mean guessing a scientific label — and a wrong guess
    would pass every structural clause while mislabelling a published artifact.
    The proposal is therefore carried unresolved, and the mapping is one table.
    """
    check(R.MEMBER_NAMING_UNRESOLVED is True,
          "the conflict is flagged in the module, not silently resolved")
    check(sorted(R.MEMBER_NAME_BY_FAMILY) == sorted(R.REGISTERED_FAMILIES),
          "the mapping covers exactly the frozen families")
    check(len(set(R.MEMBER_NAME_BY_FAMILY.values()))
          == len(R.REGISTERED_FAMILIES),
          "and is a bijection, so two families cannot share a member name")
    check(R.MAX_MEMBER_NAME not in R.MEMBER_NAME_BY_FAMILY.values(),
          "the maximum's name is not also a family's name")
    for proposed in R.PROPOSED_MEMBER_NAMES:
        check(isinstance(proposed, str) and proposed,
              f"the proposed name {proposed!r} is recorded verbatim")
    unmapped = [n for n in R.PROPOSED_MEMBER_NAMES
                if n != R.MAX_MEMBER_NAME
                and n not in R.MEMBER_NAME_BY_FAMILY.values()]
    check(len(unmapped) == 3,
          "three of the four proposed names have no family mapping yet")
    check("guess" in R.MEMBER_NAMING_NOTE and "mapping" in R.MEMBER_NAMING_NOTE,
          "and the note says what is needed to resolve it")


def test_the_summary_cross_check_is_exact_and_locates_the_first_difference():
    arrays = _expected_arrays()
    good = {"j_null_max": list(arrays[R.MAX_MEMBER_NAME])}
    agreement = R.compare_to_summary(arrays, good)
    check(agreement["identical"] is True, "an identical vector agrees")
    check(agreement["first_difference"] is None, "with nothing to report")

    drifted = {"j_null_max": list(arrays[R.MAX_MEMBER_NAME])}
    drifted["j_null_max"][7] += 1e-15                    # a float64 tick
    off = R.compare_to_summary(arrays, drifted)
    check(off["identical"] is False,
          "a one-tick difference is a disagreement, not a rounding matter")
    check(off["first_difference"]["index"] == 7,
          "and the first differing index is reported")

    short = {"j_null_max": list(arrays[R.MAX_MEMBER_NAME])[:-1]}
    check(R.compare_to_summary(arrays, short)["identical"] is False,
          "a truncated summary is a disagreement too")
    check(R.compare_to_summary(arrays, {})["identical"] is False,
          "and so is a summary with no vector at all")
    check(R.compare_to_summary(arrays, {"j_null_max": "nope"})["identical"]
          is False,
          "and one whose vector is not a list")


# ─────────────────────────────────────────────────────────────────────────────
# G — the NPZ contract and its two independent readers
# ─────────────────────────────────────────────────────────────────────────────
def test_npy_round_trips_and_declares_float64():
    values = [0.0, -1.5, 3.25, 1e-300, 1e300]
    blob = R.npy_bytes(values)
    check(blob.startswith(b"\x93NUMPY\x01\x00"), "NPY v1.0 magic and version")
    (header_length,) = struct.unpack("<H", blob[8:10])
    check((10 + header_length) % 64 == 0,
          "the header is padded to a 64-byte boundary")
    check(blob[10:10 + header_length].endswith(b"\n"),
          "and terminated with a newline, as the format requires")
    descr, dims, back = R.read_npy_bytes(blob)
    check(descr == "<f8", "the dtype is little-endian float64")
    check(dims == (len(values),), "the shape is one-dimensional")
    check(back == values, "and every value survives exactly")


def test_the_npz_holds_exactly_the_four_arrays_deterministically():
    arrays = _expected_arrays()
    blob = R.npz_bytes(arrays)
    check(sorted(R.read_npz_bytes(blob)) == sorted(R.NPZ_ARRAYS),
          "four members, named as the contract fixes")
    with zipfile.ZipFile(io.BytesIO(blob)) as archive:
        check(all(i.compress_type == zipfile.ZIP_STORED
                  for i in archive.infolist()), "stored, not deflated")
        check({i.date_time for i in archive.infolist()} == {R.ZIP_TIMESTAMP},
              "with a pinned timestamp, so the bytes are deterministic")
    check(R.npz_bytes(arrays) == blob,
          "the same arrays produce byte-identical output twice")
    for bad in ({k: v for k, v in arrays.items() if k != R.MAX_MEMBER_NAME},
                dict(arrays, extra=[0.0])):
        try:
            R.npz_bytes(bad)
            raise AssertionError("an off-contract array set was serialised")
        except R.RepairError as error:
            check(error.reason == R.NPZ_CONTRACT_FAILED,
                  "the writer refuses anything but the four")


def test_duplicate_zip_member_names_are_detected():
    """A dict-based reader silently keeps one of them; the name list does not."""
    arrays = _expected_arrays()
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_STORED) as archive:
        for name in R.NPZ_ARRAYS:
            archive.writestr(zipfile.ZipInfo(f"{name}.npy",
                                             date_time=R.ZIP_TIMESTAMP),
                             R.npy_bytes(arrays[name]))
        archive.writestr(zipfile.ZipInfo(f"{R.MAX_MEMBER_NAME}.npy",
                                         date_time=R.ZIP_TIMESTAMP),
                         R.npy_bytes(arrays[R.MAX_MEMBER_NAME]))
    blob = buffer.getvalue()
    names = R.npz_member_names(blob)
    check(len(names) == 5, "the raw member list keeps the duplicate")
    verdict = R.verify_npz_contract(blob, total=TOTAL)
    check(verdict["ok"] is False, "and the contract refuses it")
    check(verdict["duplicate_members"] == [f"{R.MAX_MEMBER_NAME}.npy"],
          "naming the duplicated member")


def test_the_npz_contract_is_verified_by_reading_the_bytes_back():
    arrays = _expected_arrays()
    blob = R.npz_bytes(arrays)
    verdict = R.verify_npz_contract(blob, arrays[R.MAX_MEMBER_NAME],
                                    total=TOTAL, reconstructed=arrays)
    check(verdict["ok"] is True, f"a correct NPZ passes: {verdict['problems']}")
    check(verdict["sha256"] == hashlib.sha256(blob).hexdigest(),
          "the digest is of the produced bytes")
    check(verdict["duplicate_members"] == [], "no duplicate members")
    for name in R.NPZ_ARRAYS:
        entry = verdict["arrays"][name]
        check(entry["dtype"] == "<f8" and entry["shape"] == [TOTAL]
              and entry["finite"] is True,
              f"{name}: float64, right shape, finite")
    check(verdict["arrays"]["max_is_family_max"] is True,
          "and the internal maximum relation holds")


def test_the_npz_contract_catches_every_way_it_can_be_wrong():
    arrays = _expected_arrays()

    wrong_shape = dict(arrays)
    first_member = R.MEMBER_NAME_BY_FAMILY[FAMILIES[0]]
    wrong_shape[first_member] = arrays[first_member][:-1]
    check(not R.verify_npz_contract(R.npz_bytes(wrong_shape),
                                    total=TOTAL)["ok"],
          "a short array fails the shape clause")

    members = [R.MEMBER_NAME_BY_FAMILY[f] for f in FAMILIES]
    for bad_value in (float("nan"), float("inf"), float("-inf")):
        broken = {k: list(v) for k, v in arrays.items()}
        broken[members[1]][2] = bad_value
        broken[R.MAX_MEMBER_NAME] = [max(broken[m][b] for m in members)
                                     for b in range(TOTAL)]
        verdict = R.verify_npz_contract(R.npz_bytes(broken), total=TOTAL)
        check(not verdict["ok"] and any("non-finite" in str(p)
                                        for p in verdict["problems"]),
              f"{bad_value} is refused")

    detached = {k: list(v) for k, v in arrays.items()}
    detached[R.MAX_MEMBER_NAME] = [0.0] * TOTAL
    verdict = R.verify_npz_contract(R.npz_bytes(detached), total=TOTAL)
    check(not verdict["ok"]
          and any("family maximum" in str(p) for p in verdict["problems"]),
          "a maximum that is not the family maximum is refused")

    verdict = R.verify_npz_contract(
        R.npz_bytes(arrays),
        [v + 1e-15 for v in arrays[R.MAX_MEMBER_NAME]], total=TOTAL)
    check(not verdict["ok"],
          "and disagreement with the expected vector is refused")


def test_a_pickled_member_cannot_be_read_at_all():
    """`allow_pickle=False` exists to reject object arrays; so does this reader."""
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_STORED) as archive:
        header = ("{'descr': '|O', 'fortran_order': False, 'shape': (1,), }"
                  .ljust(54) + "\n")
        body = (b"\x93NUMPY\x01\x00" + struct.pack("<H", len(header))
                + header.encode("latin-1") + b"\x80\x04pickled")
        archive.writestr(zipfile.ZipInfo("wrong_record.npy",
                                         date_time=R.ZIP_TIMESTAMP), body)
    try:
        R.read_npz_bytes(buffer.getvalue())
        raise AssertionError("an object-dtype member was accepted")
    except R.RepairError as error:
        check(error.reason == R.NPZ_CONTRACT_FAILED,
              "an object dtype is refused outright")


def test_numpy_verification_is_a_call_not_a_declared_constant():
    """The earlier version reported a hard-coded True; that is not a check."""
    import ast
    source = open(R.__file__, encoding="utf-8").read()
    # By AST, not by substring: the module still *explains* why the old flag
    # was removed, and prose about a mistake is not the mistake.
    keys = [node.value for tree_node in ast.walk(ast.parse(source))
            if isinstance(tree_node, ast.Dict)
            for node in tree_node.keys
            if isinstance(node, ast.Constant) and isinstance(node.value, str)]
    check("allow_pickle_false_readable" not in keys,
          "the constant-dressed-as-a-measurement is gone from every dict")
    check("numpy.load(" in source and "allow_pickle=False" in source,
          "and the module really calls numpy.load with pickling off")

    arrays = _expected_arrays()
    blob = R.npz_bytes(arrays)
    try:
        import numpy                                     # noqa: F401
        have_numpy = True
    except ImportError:
        have_numpy = False

    result = R.numpy_verify_npz(blob, arrays, required=False)
    check(result["ran"] is have_numpy,
          "the verification runs exactly when numpy is importable")
    if have_numpy:                                       # pragma: no cover
        check(result["ok"] is True,
              f"and numpy agrees with the bytes: {result.get('problems')}")
        check(result["allow_pickle"] is False, "with pickling off")
        for name in R.NPZ_ARRAYS:
            check(result["arrays"][name]["dtype"] == "float64",
                  f"numpy reads {name} as float64")
            check(result["arrays"][name]["shape"] == [TOTAL],
                  f"and {name} with the right shape")
    else:
        check(result["available"] is False,
              "and when numpy is absent it says so instead of claiming a pass")


def test_production_refuses_to_publish_without_numpy():
    """G — 'probably loadable' is not a standard for a published artifact."""
    arrays = _expected_arrays()
    blob = R.npz_bytes(arrays)
    try:
        import numpy                                     # noqa: F401
        have_numpy = True
    except ImportError:
        have_numpy = False

    if have_numpy:                                       # pragma: no cover
        verdict = R.verify_npz_contract(blob, total=TOTAL,
                                        reconstructed=arrays,
                                        require_numpy=True)
        check(verdict["numpy_verification"]["ran"] is True,
              "with numpy present the required verification runs")
        return
    try:
        R.numpy_verify_npz(blob, arrays, required=True)
        raise AssertionError("published without the numpy cross-check")
    except R.RepairError as error:
        check(error.reason == R.NUMPY_UNAVAILABLE,
              "a required numpy check that cannot run is a stop")
        check("not a substitute" in str(error),
              "and the message says the independent reader does not stand in")


# ─────────────────────────────────────────────────────────────────────────────
# D — the immutable source snapshot
# ─────────────────────────────────────────────────────────────────────────────
def test_the_source_is_read_once_and_both_uses_share_those_bytes():
    """The TOCTOU window: judge one manifest, copy another."""
    with _repair_world() as world, approved() as token:
        snapshot, inventory = R.read_source_snapshot(
            world["source"], token, world["drive"])
        check(inventory["count"] == 11, "eleven files inventoried")
        check(inventory["folder_id_bridge"]["bridged"] is True,
              "tied to the registered folder id")
        judged = snapshot.json(R.MANIFEST_FILE)

        # Something rewrites the manifest after it was judged.
        with open(os.path.join(world["source"], R.MANIFEST_FILE), "wb") as h:
            h.write(json.dumps({"split": "DS2"}).encode("utf-8"))

        check(snapshot.json(R.MANIFEST_FILE) == judged,
              "the snapshot still returns the bytes that were judged")
        R.assemble_corrective_bundle(snapshot, world["target"],
                                     R.npz_bytes(world["built"]["arrays"]),
                                     token, world["shards"], world["runs"])
        with open(os.path.join(world["target"], R.MANIFEST_FILE), "rb") as h:
            copied = h.read()
        check(hashlib.sha256(copied).hexdigest()
              == snapshot.digest(R.MANIFEST_FILE),
              "and the copy is the judged bytes, not the rewritten ones")

        recheck = snapshot.recheck()
        check(recheck["ok"] is False,
              "the end-of-run re-hash notices the source moved")
        check(any(R.MANIFEST_FILE in p for p in recheck["problems"]),
              "and names the file that changed")


def test_the_source_bundle_must_be_exactly_the_eleven():
    identity = _identity()
    with tempfile.TemporaryDirectory() as tmp, approved() as token:
        short = os.path.join(tmp, "short")
        _write_source_bundle(short, identity, omit=("log.txt",))
        try:
            R.read_source_snapshot(short, token)
            raise AssertionError("a ten-file source was accepted")
        except R.RepairError as error:
            check(error.reason == R.SOURCE_BUNDLE_UNEXPECTED,
                  "a missing file is a stop")

        wide = os.path.join(tmp, "wide")
        _write_source_bundle(wide, identity, extra=("SUPERSEDED.json",))
        try:
            R.read_source_snapshot(wide, token)
            raise AssertionError("an unexpected file was accepted")
        except R.RepairError as error:
            check(error.reason == R.SOURCE_BUNDLE_UNEXPECTED,
                  "and so is an unexpected one")

        nested = os.path.join(tmp, "nested")
        _write_source_bundle(nested, identity)
        os.makedirs(os.path.join(nested, "figures"))
        try:
            R.read_source_snapshot(nested, token)
            raise AssertionError("a subdirectory was accepted")
        except R.RepairError as error:
            check(error.reason == R.SOURCE_BUNDLE_UNEXPECTED,
                  "and so is a subdirectory")


def test_unparseable_bundle_json_is_a_structured_stop():
    identity = _identity()
    with tempfile.TemporaryDirectory() as tmp, approved() as token:
        source = os.path.join(tmp, "source")
        _write_source_bundle(source, identity)
        with open(os.path.join(source, R.SUMMARY_FILE), "wb") as handle:
            handle.write(b"{not json")
        snapshot, _ = R.read_source_snapshot(source, token)
        try:
            snapshot.json(R.SUMMARY_FILE)
            raise AssertionError("unparseable JSON was returned")
        except R.RepairError as error:
            check(error.reason == R.SOURCE_BUNDLE_UNEXPECTED,
                  "a bundle file that is not JSON is a structured stop")


# ─────────────────────────────────────────────────────────────────────────────
# E — target safety
# ─────────────────────────────────────────────────────────────────────────────
def test_a_target_inside_the_inputs_or_outside_the_runs_parent_is_refused():
    with _repair_world() as world:
        runs, source, shards = world["runs"], world["source"], world["shards"]
        unsafe = {
            "the source itself": source,
            "inside the source": os.path.join(source, "sub"),
            "the shard folder": shards,
            "inside the shard folder": os.path.join(shards, "sub"),
            "outside the runs parent": os.path.join(world["tmp"], "elsewhere"),
        }
        for label, target in unsafe.items():
            try:
                R.assert_target_safe(target, source, shards, runs)
                raise AssertionError(f"accepted a target that is {label}")
            except R.RepairError as error:
                check(error.reason in (R.TARGET_UNSAFE, R.TARGET_EXISTS),
                      f"a target that is {label} is refused")
        safe = R.assert_target_safe(world["target"], source, shards, runs)
        check(safe["parent_is_approved_runs_parent"] is True,
              "and a fresh name under the approved runs parent is allowed")


def test_a_symlinked_component_and_an_existing_target_are_refused():
    with _repair_world() as world:
        runs, source, shards = world["runs"], world["source"], world["shards"]
        existing = os.path.join(runs, "already_there")
        os.makedirs(existing)
        try:
            R.assert_target_safe(existing, source, shards, runs)
            raise AssertionError("accepted an existing target")
        except R.RepairError as error:
            check(error.reason == R.TARGET_EXISTS,
                  "an existing target name is refused")
            check("new unique name" in str(error),
                  "and the message says a retry uses another name")

        try:
            os.symlink(runs, os.path.join(world["tmp"], "link_runs"))
        except (OSError, NotImplementedError, AttributeError):
            check(True, "symlinks unavailable here; the link clause is "
                        "exercised where the platform allows it")
            return
        linked = os.path.join(world["tmp"], "link_runs", "target")
        try:
            R.assert_target_safe(linked, source, shards,
                                 os.path.join(world["tmp"], "link_runs"))
            raise AssertionError("accepted a symlinked parent")
        except R.RepairError as error:
            check(error.reason == R.TARGET_UNSAFE,
                  "a symlinked path component is refused")


# ─────────────────────────────────────────────────────────────────────────────
# F — the failure publication contract
# ─────────────────────────────────────────────────────────────────────────────
def test_a_stop_before_the_claim_leaves_no_directory():
    identity = _identity()
    with _repair_world(identity, skip=((15, 20),)) as world, \
            approved() as token:
        try:
            R.run_repair(world["shards"], world["source"], world["target"],
                         token, world["drive"], world["runs"], total=TOTAL,
                         expected_shards=EXPECTED, require_numpy=False)
            raise AssertionError("published from an incomplete null")
        except R.RepairError as error:
            check(error.reason == R.INPUT_UNQUALIFIED,
                  "an incomplete null stops the run")
            check(error.incomplete_directory is None,
                  "with no directory to preserve")
            check(error.as_record()["target_state"] is None,
                  "and the record says there is no target state")
        check(not os.path.exists(world["target"]),
              "nothing was created")


def test_a_stop_after_the_claim_preserves_the_directory_and_reports_it():
    """The claim the earlier version got wrong: 'any failure leaves no folder'."""
    identity = _identity()
    with _repair_world(identity) as world, approved() as token:
        snapshot, _ = R.read_source_snapshot(world["source"], token)
        # An intruder takes one of the names inside the claimed directory, so
        # the exclusive create fails after the mkdir has happened.
        original = R._write_new_file

        def fail_on_summary(path, body):
            if os.path.basename(path) == "summary.md":
                raise R.RepairError(R.COPY_NOT_BYTE_IDENTICAL,
                                    "simulated mid-write failure")
            return original(path, body)

        R._write_new_file = fail_on_summary
        try:
            R.assemble_corrective_bundle(
                snapshot, world["target"],
                R.npz_bytes(world["built"]["arrays"]), token,
                world["shards"], world["runs"])
            raise AssertionError("assembled despite a mid-write failure")
        except R.RepairError as error:
            check(error.reason == R.COPY_NOT_BYTE_IDENTICAL,
                  "the failure keeps its own reason")
            check(error.incomplete_directory == world["target"],
                  "and carries the exact path of the partial directory")
            check(error.target_state == R.INCOMPLETE_PRESERVED,
                  "marked as preserved, not committed")
            record = error.as_record()
            check(record["committed"] is False and record["accepted"] is False,
                  "the record refuses both committed and accepted")
            check(len(record["incomplete_listing"]) > 0,
                  "and lists what the directory actually holds")
        finally:
            R._write_new_file = original
        check(os.path.isdir(world["target"]),
              "the partial directory is left exactly where it is")
        check(sorted(os.listdir(world["target"])) == \
              sorted(record["incomplete_listing"]),
              "and the reported listing is the real one")
        check(R.MISSING_ARTIFACT not in os.listdir(world["target"]),
              "the NPZ was never written into an unfinished bundle")


def test_the_module_never_deletes_renames_or_overwrites():
    """By AST, not by comment: no delete or rename call exists at all."""
    import ast
    source = open(R.__file__, encoding="utf-8").read()
    tree = ast.parse(source)
    banned = {"remove", "unlink", "rmdir", "removedirs", "rename", "replace",
              "renames", "rmtree", "copy", "copy2", "copyfile", "move"}
    found = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            if node.func.attr in banned and not isinstance(node.func.value,
                                                           ast.Str):
                owner = getattr(node.func.value, "id", None) or \
                    getattr(getattr(node.func.value, "value", None), "id", None)
                if owner in ("os", "shutil", "pathlib"):
                    found.append(node.func.attr)
    check(not found, f"no destructive filesystem call exists: {found}")
    check("shutil" not in source, "and shutil is never imported")
    check(R.FAILURE_PUBLICATION_CONTRACT.count("never") >= 2
          and "new unique target path" in R.FAILURE_PUBLICATION_CONTRACT,
          "the contract states preservation and a new path for a retry")


def test_the_spec_and_notebook_state_the_same_failure_contract():
    spec = open(os.path.join(ROOT, R.SPEC_PATH), encoding="utf-8").read()
    nb = json.load(open(os.path.join(ROOT, R.NOTEBOOK_PATH), encoding="utf-8"))
    body = "\n".join("".join(c["source"]) for c in nb["cells"])
    check(R.INCOMPLETE_PRESERVED in spec,
          "the spec names the preserved-directory state")
    check("new unique" in spec.lower(),
          "and says a retry uses a new unique path")
    check("보존" in body or "preserved" in body.lower(),
          "the notebook says the partial directory is preserved")
    check("삭제" in body or "delete" in body.lower(),
          "and that nothing is deleted")


# ─────────────────────────────────────────────────────────────────────────────
# The whole route
# ─────────────────────────────────────────────────────────────────────────────
def test_the_route_completes_on_a_clean_synthetic_repair():
    with _repair_world() as world, approved() as token:
        world["drive"].folders[R.RUNS_PARENT_FOLDER_ID] = [
            {"id": "corrective-folder-id",
             "name": os.path.basename(world["target"]),
             "mimeType": R.DRIVE_FOLDER_MIME, "trashed": False}]
        decision = R.run_repair(
            world["shards"], world["source"], world["target"], token,
            world["drive"], world["runs"], total=TOTAL,
            expected_shards=EXPECTED, require_numpy=False, repo_root=ROOT)
        check(decision["status"] == R.REPAIR_COMPLETE, "the route completes")
        check(decision["first_stopping_reason"] is None, "with no stop")
        check(decision["qualification"]["qualified"] is True,
              "the shards qualified")
        check(decision["summary_agreement"]["identical"] is True,
              "the summary agreed exactly")
        check(decision["npz"]["ok"] is True, "the NPZ met its contract")
        check(decision["verification"]["ok"] is True,
              "the finished folder verified")
        check(decision["source_recheck"]["ok"] is True,
              "and the source was unchanged at the end")
        check(decision["corrective_folder_id"]["folder_id"]
              == "corrective-folder-id",
              "the new folder's Drive id was read back")
        check(decision["frozen_q5d"]["lf_normalized_sha256"]
              == R.FROZEN_Q5D_SHA256_LF,
              "the frozen module identity is in the record")
        check(decision["artifact_identities"]["module"]["path"]
              == R.MODULE_PATH,
              "and so are the module, spec and notebook identities")
        for flag in ("training_performed", "join_rerun", "null_recomputed",
                     "ds2_outcome_opened", "v10_probability_opened",
                     "registered_anything"):
            check(decision[flag] is False, f"{flag} is false")
        check(sorted(os.listdir(world["target"])) == sorted(R.BUNDLE_FILES),
              "twelve files on disk")
        check(decision["corrective_bundle"]["committed_marker_written"]
              is False,
              "and no COMMITTED marker was written")

        report = R.report_markdown(decision)
        for fragment in (R.REPAIR_COMPLETE, decision["npz"]["sha256"],
                         "corrective-folder-id", R.FROZEN_Q5D_SHA256_LF,
                         "No J value was computed"):
            check(fragment in report, f"the report carries {fragment[:24]}")


def test_a_disagreeing_summary_stops_before_anything_is_written():
    identity = _identity()
    with _repair_world(identity) as world, approved() as token:
        arrays = _expected_arrays()
        drifted = list(arrays[R.MAX_MEMBER_NAME])
        drifted[3] += 1e-15
        _write_source_bundle(world["source"], identity, summary={
            "replicates": TOTAL,
            "rule_fingerprint": R.REGISTERED_RULE_FINGERPRINT,
            "j_null_max": drifted})
        try:
            R.run_repair(world["shards"], world["source"], world["target"],
                         token, None, world["runs"], total=TOTAL,
                         expected_shards=EXPECTED, require_numpy=False)
            raise AssertionError("published despite a disagreeing summary")
        except R.RepairError as error:
            check(error.reason == R.SUMMARY_DISAGREES,
                  "a summary that disagrees is a stop")
            check(error.incomplete_directory is None,
                  "and it happens before the claim")
        check(not os.path.exists(world["target"]),
              "so no corrective folder was created")


def test_every_stop_reason_is_reachable_and_named():
    check(len(set(R.STOP_REASONS)) == len(R.STOP_REASONS),
          "the stop reasons are distinct")
    source = open(R.__file__, encoding="utf-8").read()
    for reason in R.STOP_REASONS:
        constant = [name for name, value in vars(R).items()
                    if value == reason and name.isupper()]
        check(constant, f"{reason} has a named constant")
        check(source.count(constant[0]) >= 2,
              f"{constant[0]} is raised somewhere, not only declared")
    check(R.REPAIR_COMPLETE not in R.STOP_REASONS,
          "completion is not a stop reason")
    check(R.INCOMPLETE_PRESERVED not in R.STOP_REASONS,
          "and neither is the preserved-directory state")


def test_the_repair_never_writes_to_the_frozen_module_or_its_contract():
    source = open(R.__file__, encoding="utf-8").read()
    check("BJ.BUNDLE_FILES" in source,
          "BUNDLE_FILES is read from the frozen module")
    for forbidden in ("BJ.BUNDLE_FILES =", "BJ.BUNDLE_FILES=", "setattr(BJ",
                      "BJ.write_null_shard", "BJ.compute_null_shard",
                      "BJ.run_null_shards"):
        check(forbidden not in source, f"the repair never does {forbidden!r}")
    check(len(R.BUNDLE_FILES) == 12, "the contract is still twelve")
    check(len(R.SOURCE_BUNDLE_FILES) == 11,
          "and the source is those twelve minus the one being rebuilt")
    check(set(R.SOURCE_BUNDLE_FILES) | {R.MISSING_ARTIFACT}
          == set(R.BUNDLE_FILES),
          "differing by exactly negative_control_null.npz")


# ─────────────────────────────────────────────────────────────────────────────
# Contract with the notebook and the spec
# ─────────────────────────────────────────────────────────────────────────────
NOTEBOOK = os.path.join(ROOT, "notebooks",
                        "quest57_q5d_null_artifact_repair.ipynb")


def test_the_notebook_is_committed_unexecuted():
    nb = json.load(open(NOTEBOOK, encoding="utf-8"))
    code = [c for c in nb["cells"] if c["cell_type"] == "code"]
    check(code, "the notebook has code cells")
    check(all(c.get("outputs") == [] for c in code),
          "and not one of them carries output")
    check(all(c.get("execution_count") is None for c in code),
          "nor an execution count")
    body = "\n".join("".join(c["source"]) for c in code)
    check("q5d_null_artifact_repair" in body, "it imports this module")
    check("module_capabilities" in body,
          "and asserts them, so a stale clone cannot masquerade")
    missing = [n for n in R.module_capabilities() if not hasattr(R, n)]
    check(not missing, f"every advertised capability exists: {missing}")


def test_the_notebook_pins_a_commit_and_rechecks_the_files():
    """H — a moving branch is not a pin, and a commit is not a working tree."""
    nb = json.load(open(NOTEBOOK, encoding="utf-8"))
    body = "\n".join("".join(c["source"]) for c in nb["cells"]
                     if c["cell_type"] == "code")
    check("PINNED_COMMIT" in body, "the notebook takes an exact commit")
    check("git checkout" in body or "--branch" not in body,
          "and checks that commit out rather than tracking a branch")
    check("artifact_identities" in body,
          "then re-checks the module, spec and notebook digests on disk")
    check("REPO_BRANCH = 'main'" not in body,
          "it does not silently follow main")


def test_the_notebook_uses_folder_ids_and_holds_no_approval_of_its_own():
    nb = json.load(open(NOTEBOOK, encoding="utf-8"))
    body = "\n".join("".join(c["source"]) for c in nb["cells"]
                     if c["cell_type"] == "code")
    check("EXECUTION_APPROVAL_RECORD['granted'] = True" not in body
          and 'EXECUTION_APPROVAL_RECORD["granted"] = True' not in body,
          "the notebook never flips the approval record")
    check(R.EXECUTION_APPROVAL_TOKEN not in body,
          "and does not carry the token as a literal")
    for folder_id in (R.SOURCE_BUNDLE_FOLDER_ID, R.SHARD_FOLDER_ID,
                      R.RUNS_PARENT_FOLDER_ID):
        check(folder_id in body,
              f"the notebook names folder id {folder_id[:12]}…")
    check("GoogleDriveFolderInventory" in body,
          "and builds a read-only folder-id inventory rather than trusting "
          "a path name")


def test_the_spec_fixes_the_contract_this_module_implements():
    spec = open(os.path.join(ROOT, R.SPEC_PATH), encoding="utf-8").read()
    check("status: draft_awaiting_approval" in spec,
          "the spec is not yet approved for implementation")
    for name in R.NPZ_ARRAYS:
        check(f"`{name}`" in spec, f"the spec names {name}")
    check("allow_pickle=False" in spec, "and fixes the pickle clause")
    check("(10000,)" in spec, "and the shape")
    check("float64" in spec, "and the dtype")
    for reason in R.STOP_REASONS:
        check(reason in spec, f"the spec lists {reason}")
    for folder_id in (R.SOURCE_BUNDLE_FOLDER_ID, R.SHARD_FOLDER_ID,
                      R.RUNS_PARENT_FOLDER_ID):
        check(folder_id in spec, f"and registers folder id {folder_id[:12]}…")
    check(str(R.N_REPLICATES) == "10000",
          "production is the registered 10,000 replicates")
    check("null_shard_00000_00100.json" in spec
          and "null_shard_09900_10000.json" in spec,
          "and the spec pins the preregistered shard filenames")
    for proposed in ("j_null_cross_record", "j_null_within_record",
                     "j_null_rr_mismatch"):
        check(proposed in spec,
              f"the unresolved proposed name {proposed} is recorded in the spec")


def test_nothing_in_this_file_left_the_guard_open():
    """The last word: the module is as closed as it shipped."""
    check(R.EXECUTION_APPROVAL_RECORD["granted"] is False,
          "execution is still not approved")
    check(R.EXECUTION_APPROVAL_RECORD["pinned_commit"] is None,
          "and no commit was pinned by a test")


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
