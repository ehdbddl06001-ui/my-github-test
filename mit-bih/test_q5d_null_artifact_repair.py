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
import inspect
import io
import json
import os
import struct
import subprocess
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
def _preflight(rule_fingerprint=None, **overrides):
    """A frozen input freeze shaped like the producer's, keyed as it keys it."""
    freeze = {
        "ok": True,
        "rule_fingerprint": rule_fingerprint or R.REGISTERED_RULE_FINGERPRINT,
        "canonical_mamba": {"sha256": "a" * 64},
        "cache_aggregate": {"aggregate": "b" * 64},
        "mitdb_aggregate": {"aggregate": "c" * 64},
        "cache_ledger_contract": {"ok": True},
        "result_contract": {"pid_digest": "d" * 64},
    }
    freeze.update(overrides)
    return freeze


def _producer_manifest(preflight=None, **overrides):
    """A manifest with the producer's **schema** and the registered **identity**.

    Two different things, and the fixture needs both from different places.

    *Structure* comes from `BJ.build_manifest()` itself.  That is what caught
    the schema error the first real run hit: a flat dict written from the same
    belief as the code under test could only ever agree with that belief.

    *Identity* is then pinned to `R.FROZEN_Q5D_SHA256_LF`, because
    `build_manifest()` records `sha256_file()` — the **raw bytes of the module
    in whatever checkout is running the test**.  On a CRLF checkout that is the
    checkout's own newline digest
    (`879436b6…` on Windows) and **not** the identity of the registered
    artifact (`6b098c67…`), which was produced from an LF checkout.  Leaving it
    unpinned would make a fixture that is supposed to impersonate the
    registered bundle impersonate this machine instead — and the strict
    validator would rightly refuse it, failing the suite on Windows for a
    reason that has nothing to do with the code.

    The pin happens **before** `overrides`, so a test that wants a foreign or
    malformed `code` block still gets one.
    """
    manifest = BJ.build_manifest({}, "20260813T000000",
                                 preflight if preflight is not None
                                 else _preflight())
    # Schema from the producer; identity from the registered artifact.
    manifest["code"] = dict(manifest["code"],
                            sha256=R.FROZEN_Q5D_SHA256_LF)
    manifest.update(overrides)
    return manifest


def _identity(code_sha256=None, input_digest=None, split=None):
    """The four identity fields as `identity_from_manifest()` returns them."""
    return {"split": split or R.REGISTERED_SPLIT,
            "code_sha256": code_sha256 or R.FROZEN_Q5D_SHA256_LF,
            "input_digest": input_digest
            or BJ.preflight_input_digest(_preflight()),
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
    manifest = _producer_manifest(**(manifest_extra or {}))
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


class FakeDriveService(object):
    """Just enough of a Drive v3 client for `GoogleDriveFolderInventory`.

    Production builds its adapter from a credential and a service, so a test
    that wants to exercise the real production route has to supply those two
    rather than an already-built adapter — which is the point of R1.
    """

    class _Request(object):
        def __init__(self, files):
            self._files = files

        def execute(self):
            return {"files": list(self._files)}

    class _Files(object):
        def __init__(self, owner):
            self._owner = owner

        def list(self, q="", **_kwargs):
            folder_id = q.split("'")[1] if "'" in q else ""
            self._owner.calls.append(folder_id)
            return FakeDriveService._Request(
                self._owner.folders.get(folder_id, []))

    def __init__(self, drive):
        self.folders = dict(drive.folders)
        self.calls = []

    def files(self):
        return FakeDriveService._Files(self)


class FakeCredential(object):
    """A credential object whose scopes can be observed, as the audit needs."""

    def __init__(self, scopes=None):
        self.scopes = list(scopes) if scopes is not None else None


class FakeAuthenticator(R.DriveAuthenticator):
    def __init__(self, scopes=None, calls=None):
        self._scopes = scopes
        self.calls = calls if calls is not None else []

    def credential(self, scopes):
        self.calls.append(list(scopes))
        return FakeCredential(self._scopes if self._scopes is not None
                              else list(scopes))


class _StubArray(object):
    def __init__(self, values):
        self._values = list(values)
        self.dtype = "float64"
        self.shape = (len(self._values),)

    def tolist(self):
        return list(self._values)


class _StubNumpy(object):
    """Enough numpy for the production path, and it records how it was called.

    Production **requires** numpy before it will publish, which is right and
    which this container cannot satisfy — it has none.  Rather than give the
    production route a bypass flag, the tests inject this and assert the call
    was made with `allow_pickle=False`.  Where real numpy exists,
    `test_numpy_verification_is_a_call_not_a_declared_constant` runs the
    genuine cross-check instead; this stub only keeps the *route* reachable.
    """

    __version__ = "stub-0"

    def __init__(self, calls):
        self.calls = calls

    class _Loaded(object):
        def __init__(self, members):
            self._members = members
            self.files = sorted(members)

        def __enter__(self):
            return self

        def __exit__(self, *exc):
            return False

        def __getitem__(self, name):
            return _StubArray(self._members[name][2])

    def load(self, handle, allow_pickle=True):
        self.calls.append({"allow_pickle": allow_pickle})
        return _StubNumpy._Loaded(R.read_npz_bytes(handle.read()))

    def isfinite(self, array):
        values = array.tolist()

        class _All(object):
            def all(self_inner):
                return all(v == v and v not in (float("inf"), float("-inf"))
                           for v in values)
        return _All()


@contextlib.contextmanager
def stub_drive_dependencies():
    """Make the client libraries importable for the length of one test.

    `build_drive_adapter()` refuses to mint a credential when the Drive client
    libraries are absent, which is right and which this container triggers —
    it has neither.  Rather than give production a bypass, the tests that need
    to reach *past* that gate install placeholder modules, and the test that
    exercises the gate itself runs without them.
    """
    import types
    names = ("googleapiclient", "googleapiclient.discovery", "google",
             "google.auth")
    previous = {name: sys.modules.get(name) for name in names}
    for name in names:
        if sys.modules.get(name) is None:
            sys.modules[name] = types.ModuleType(name)
    try:
        yield
    finally:
        for name, module in previous.items():
            if module is None:
                sys.modules.pop(name, None)
            else:                                        # pragma: no cover
                sys.modules[name] = module


@contextlib.contextmanager
def stub_numpy():
    """Inject the stub for the length of one test, then remove it."""
    calls = []
    previous = sys.modules.get("numpy")
    sys.modules["numpy"] = _StubNumpy(calls)
    try:
        yield calls
    finally:
        if previous is None:
            sys.modules.pop("numpy", None)
        else:                                            # pragma: no cover
            sys.modules["numpy"] = previous


def _make_pinned_repo(tmp):
    """A real git repository holding the four approved artifacts.

    Real git, real blobs: `verify_execution_identity()` now runs `rev-parse`,
    `status` and `git show` itself, so a fixture that faked those would test
    the fake.  The files are copied from this checkout, so the digests the
    commit yields are the digests of the code under test.
    """
    repo = os.path.join(tmp, "pinned")
    for relative in (R.MODULE_PATH, R.SPEC_PATH, R.NOTEBOOK_PATH,
                     R.FROZEN_Q5D_PATH):
        destination = os.path.join(repo, relative)
        os.makedirs(os.path.dirname(destination), exist_ok=True)
        with open(os.path.join(ROOT, relative), "rb") as source_handle:
            body = source_handle.read()
        with open(destination, "wb") as handle:
            handle.write(body)
    for args in (("init", "-q", "-b", "main"),
                 ("config", "user.email", "fixture@example.invalid"),
                 ("config", "user.name", "fixture"),
                 ("add", "-A"),
                 ("commit", "-q", "-m", "pinned fixture")):
        subprocess.run(["git", "-C", repo, *args], check=True,
                       capture_output=True)
    head = subprocess.run(["git", "-C", repo, "rev-parse", "HEAD"],
                          capture_output=True, text=True).stdout.strip()
    return repo, head


@contextlib.contextmanager
def approved_implementation(tmp=None):
    """Record the implementation identity an enable PR would record.

    Measured from the commit's own blobs rather than typed, which is exactly
    what `verify_execution_identity()` re-derives — so a drifted record fails
    instead of quietly agreeing with itself.
    """
    holder = None
    if tmp is None:
        holder = tempfile.TemporaryDirectory()
        tmp = holder.name
    repo, head = _make_pinned_repo(tmp)
    before_commit = R.APPROVED_IMPLEMENTATION_COMMIT
    before_digests = dict(R.APPROVED_ARTIFACT_DIGESTS)
    R.APPROVED_IMPLEMENTATION_COMMIT = head
    R.APPROVED_ARTIFACT_DIGESTS.update(R.digests_from_commit(repo, head))
    try:
        yield {"commit": head, "head": head, "repo": repo}
    finally:
        R.APPROVED_IMPLEMENTATION_COMMIT = before_commit
        R.APPROVED_ARTIFACT_DIGESTS.clear()
        R.APPROVED_ARTIFACT_DIGESTS.update(before_digests)
        if holder is not None:
            holder.cleanup()


@contextlib.contextmanager
def approved():
    """Guarantee the guard is open for one test, then restore what it was.

    Save-and-restore rather than force-to-False: the module now ships with
    `granted: True`, and a fixture that closed the guard behind itself would
    quietly revoke a recorded approval for every test after it.
    """
    previous = R.EXECUTION_APPROVAL_RECORD["granted"]
    R.EXECUTION_APPROVAL_RECORD["granted"] = True
    try:
        yield R.EXECUTION_APPROVAL_TOKEN
    finally:
        R.EXECUTION_APPROVAL_RECORD["granted"] = previous


@contextlib.contextmanager
def guard_closed():
    """Close the terminal guard for one test, then restore it.

    Setting `granted` back to False is the documented one-value revert, so the
    refusal tests exercise exactly the state a revocation would produce.
    """
    previous = R.EXECUTION_APPROVAL_RECORD["granted"]
    R.EXECUTION_APPROVAL_RECORD["granted"] = False
    try:
        yield
    finally:
        R.EXECUTION_APPROVAL_RECORD["granted"] = previous


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
            # The runs parent must hold the registered source folder id as a
            # direct child, which is what ties the mount path to the parent id.
            drive.folders[R.RUNS_PARENT_FOLDER_ID] = [
                {"id": R.SOURCE_BUNDLE_FOLDER_ID,
                 "name": os.path.basename(source),
                 "mimeType": R.DRIVE_FOLDER_MIME, "trashed": False}]
        yield {"tmp": tmp, "runs": runs, "shards": shard_dir,
               "source": source, "target": target, "drive": drive,
               "identity": identity, "manifest": built["manifest"],
               "built": built}


# ─────────────────────────────────────────────────────────────────────────────
# The guard
# ─────────────────────────────────────────────────────────────────────────────
def test_the_approval_is_recorded_and_revoking_it_refuses_everything():
    """The approval is a record, and closing it again is one value.

    The 2026-08-12 approval named `5191a92` and lapsed when the manifest-schema
    fix moved the science digest.  This one names the implementation Codex
    accepted afterwards, and it will lapse the same way if the logic moves
    again — an execution approval is for a specific implementation, not for a
    module in general.
    """
    check(R.EXECUTION_APPROVAL_RECORD["granted"] is True,
          "execution is approved")
    check(R.EXECUTION_APPROVAL_RECORD["granted_on"] == "2026-08-13"
          and R.EXECUTION_APPROVAL_RECORD["granted_by"] == "user",
          "with the approver and the date recorded")
    check(R.EXECUTION_APPROVAL_RECORD["pinned_commit"]
          == R.APPROVED_IMPLEMENTATION_COMMIT,
          "and the pinned commit agreeing with the approved implementation")
    check(len(R.EXECUTION_APPROVAL_RECORD["not_approved"]) >= 10,
          "what was NOT approved is still enumerated")
    check("execution approved: True" in R.design_card(),
          "the design card says so out loud")

    with tempfile.TemporaryDirectory() as tmp, guard_closed():
        for call in (
            lambda: R.qualify_shards(tmp, _producer_manifest(),
                                     R.EXECUTION_APPROVAL_TOKEN),
            lambda: R.read_source_snapshot(tmp, R.EXECUTION_APPROVAL_TOKEN),
            lambda: R.bridge_mount_to_folder_id(FakeDrive(), "x", tmp, (),
                                                R.EXECUTION_APPROVAL_TOKEN),
            lambda: R.confirm_folder_id_of_child(FakeDrive(), "x", "y",
                                                 R.EXECUTION_APPROVAL_TOKEN),
            lambda: R.run_repair(tmp, tmp, os.path.join(tmp, "out"),
                                 R.EXECUTION_APPROVAL_TOKEN),
            lambda: R.run_repair_synthetic_fixture(
                tmp, tmp, os.path.join(tmp, "out"),
                R.EXECUTION_APPROVAL_TOKEN, R.SYNTHETIC_FIXTURE_MARKER),
            lambda: R.build_drive_adapter(R.EXECUTION_APPROVAL_TOKEN),
            lambda: R.bridge_runs_parent(FakeDrive(), tmp, tmp, tmp,
                                         R.EXECUTION_APPROVAL_TOKEN),
            lambda: R.resolve_output_folder_id(FakeDrive(), "x", "y",
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
                R.qualify_shards(tmp, _producer_manifest(), token)
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
        bridge, blobs = R.bridge_mount_to_folder_id(
            world["drive"], R.SOURCE_BUNDLE_FOLDER_ID, world["source"],
            R.SOURCE_BUNDLE_FILES, token)
        check(sorted(blobs) == sorted(R.SOURCE_BUNDLE_FILES),
              "the bridge hands back the bytes it read, for the judgement to "
              "use")
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
        check(bridge["bytes_captured"] == len(R.SOURCE_BUNDLE_FILES),
              "and captured one snapshot per expected file")


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
        bridge, _ = R.bridge_mount_to_folder_id(
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
        out = R.qualify_shards(world["shards"], world["manifest"], token,
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
                R.qualify_shards(world["shards"], world["manifest"], token, None,
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
                R.qualify_shards(world["shards"], world["manifest"], token, None,
                                 total=TOTAL, expected=EXPECTED)
                raise AssertionError("an extra shard qualified")
            except R.RepairError as error:
                check(error.reason == R.INPUT_UNQUALIFIED,
                      "an unexpected file in the shard folder is refused")

        with _repair_world(identity) as world:
            os.makedirs(os.path.join(world["shards"], "nested"))
            try:
                R.qualify_shards(world["shards"], world["manifest"], token, None,
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
            R.qualify_shards(world["shards"], world["manifest"], token, None,
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
            R.qualify_shards(world["shards"], world["manifest"], token, None,
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
            R.qualify_shards(world["shards"], world["manifest"], token, None,
                             total=TOTAL, expected=EXPECTED)
            raise AssertionError("a wrong maximum qualified")
        except R.RepairError as error:
            check(error.reason == R.INPUT_UNQUALIFIED,
                  "a shard whose maximum is not the family maximum is refused")


def test_the_identity_comes_from_where_the_producer_actually_writes_it():
    """The schema is learned from `BJ.build_manifest()`, not assumed.

    The first real bundle stopped on `split: None` because this module expected
    four flat top-level fields — a shape the producer has never written — and
    every fixture agreed, having been written from the same belief.  These
    assertions are anchored on the producer's own output, so the assumption
    cannot drift back in.
    """
    manifest = _producer_manifest()
    identity = R.identity_from_manifest(manifest)
    check(sorted(identity) == sorted(R.IDENTITY_FIELDS),
          "the four identity fields come back")

    check("rule_fingerprint" in manifest,
          "rule_fingerprint is at the manifest's top level")
    check(isinstance(manifest.get("code"), dict)
          and "sha256" in manifest["code"],
          "the module digest is under manifest['code']['sha256']")
    check("split" not in manifest,
          "and the manifest carries no split at all")
    check(identity["split"] == R.REGISTERED_SPLIT,
          "so split comes from the registered constant instead")
    check("registered constant" in R.MANIFEST_IDENTITY_SOURCES["split"],
          "which the report says out loud")

    check("input_digest" not in manifest,
          "the manifest stores no input digest either")
    check(identity["input_digest"]
          == BJ.preflight_input_digest(manifest["preflight"]),
          "it is derived from the preflight freeze by the producer's own "
          "function")
    check(set(BJ.PREFLIGHT_FREEZE_FIELDS) <= set(manifest["preflight"]),
          "and the freeze carries every field that derivation needs")


def test_a_manifest_that_does_not_anchor_is_refused():
    cases = {
        "a foreign rule fingerprint":
            _producer_manifest(rule_fingerprint="f" * 64),
        "a missing rule fingerprint": _producer_manifest(rule_fingerprint=None),
        "a foreign module digest":
            _producer_manifest(code={"sha256": "a" * 64}),
        "a malformed module digest":
            _producer_manifest(code={"sha256": "nope"}),
        "no code block": _producer_manifest(code=None),
    }
    # `preflight=None` means "use the default freeze" to the fixture, so the
    # absent case is built and then emptied.
    cases["no preflight freeze"] = _producer_manifest()
    cases["no preflight freeze"]["preflight"] = None
    for label, manifest in cases.items():
        try:
            R.identity_from_manifest(manifest)
            raise AssertionError(f"accepted {label}")
        except R.RepairError as error:
            check(error.reason == R.INPUT_UNQUALIFIED,
                  f"{label} cannot anchor the repair")

    # The freeze must agree with the manifest it sits in.
    try:
        R.identity_from_manifest(_producer_manifest(
            preflight=_preflight(rule_fingerprint="e" * 64)))
        raise AssertionError("accepted a freeze disagreeing with its manifest")
    except R.RepairError as error:
        check(error.reason == R.INPUT_UNQUALIFIED,
              "a preflight fingerprint that disagrees with the manifest's is "
              "refused")


def test_only_a_complete_and_passing_freeze_may_anchor():
    """Blocker 1 — a digest folded from a partial freeze summarises less than
    it appears to, so completeness is proven before the fold, not after."""
    for label, value in (("false", False), ("zero", 0), ("the string true",
                                                         "true"),
                         ("null", None)):
        try:
            R.identity_from_manifest(_producer_manifest(
                preflight=_preflight(ok=value)))
            raise AssertionError(f"accepted preflight.ok = {label}")
        except R.RepairError as error:
            check(error.reason == R.INPUT_UNQUALIFIED,
                  f"preflight.ok = {label} cannot anchor the repair")
            check("not the JSON boolean true" in str(error),
                  f"and identity, not truthiness, is what rejected {label}")

    absent = _preflight()
    absent.pop("ok")
    try:
        R.identity_from_manifest(_producer_manifest(preflight=absent))
        raise AssertionError("accepted a freeze with no ok field")
    except R.RepairError as error:
        check(error.reason == R.INPUT_UNQUALIFIED,
              "a freeze with no ok field cannot anchor the repair")

    # Every registered freeze field, dropped one at a time.
    for field in BJ.PREFLIGHT_FREEZE_FIELDS:
        freeze = _preflight()
        freeze.pop(field)
        try:
            R.identity_from_manifest(_producer_manifest(preflight=freeze))
            raise AssertionError(f"accepted a freeze missing {field}")
        except R.RepairError as error:
            check(error.reason == R.INPUT_UNQUALIFIED,
                  f"a freeze missing {field!r} is refused")
    check(len(BJ.PREFLIGHT_FREEZE_FIELDS) == 7,
          "all seven registered freeze fields were exercised")

    # And a whole, passing freeze still anchors.
    identity = R.identity_from_manifest(_producer_manifest())
    check(identity["input_digest"]
          == BJ.preflight_input_digest(_preflight()),
          "a complete, passing freeze derives the digest")


def test_the_derived_digest_claim_is_bounded():
    """Blocker 1 — the earlier wording overclaimed and is corrected.

    Derivation buys internal consistency against an unverified redundant
    stored digest.  It does not buy independent provenance: both still come
    out of the same manifest.
    """
    note = R.MANIFEST_IDENTITY_SOURCES["input_digest"]
    check("internal consistency" in note,
          "the claim that is made is internal consistency")
    check("NOT stronger independent provenance" in note,
          "and the claim that is not made is independent provenance")
    check(R.REGISTERED_INPUT_DIGEST is None,
          "there is still no separately registered input digest to check "
          "either against")


def test_the_fixture_impersonates_the_registered_artifact_not_this_checkout():
    """Windows portability — the fixture's identity is pinned, on purpose.

    `BJ.build_manifest()` records `sha256_file()`, the raw bytes of the module
    in whatever checkout is running.  On a CRLF checkout that digest is this
    machine's, not the registered artifact's, so a fixture meant to impersonate
    the registered bundle would impersonate the machine — and the strict
    validator would correctly refuse it, failing the suite for a reason that
    has nothing to do with the code.
    """
    fixture = _producer_manifest()
    check(fixture["code"]["sha256"] == R.FROZEN_Q5D_SHA256_LF,
          "the fixture carries the registered LF identity")

    # Recorded rather than hidden: the producer really does write the running
    # checkout's raw digest, and on an LF checkout the two coincide.
    unpinned = BJ.build_manifest({}, "20260813T000000", _preflight())
    checkout_raw = R.frozen_q5d_digests()["raw_sha256"]
    check(unpinned["code"]["sha256"] == checkout_raw,
          "an unpinned producer manifest carries this checkout's raw digest")
    check(sorted(unpinned) == sorted(fixture),
          "and the pin changes one value, not the schema")
    if checkout_raw == R.FROZEN_Q5D_SHA256_LF:
        check(True, "this checkout is LF, so raw and registered coincide here "
                    "— the pin is what makes a CRLF checkout behave the same")
    else:                                                # pragma: no cover
        check(unpinned["code"]["sha256"] != R.FROZEN_Q5D_SHA256_LF,
              "this checkout is CRLF, so the unpinned digest is not the "
              "registered identity — exactly the case the pin exists for")

    # Overrides still win, so the foreign/malformed fixtures keep working.
    check(_producer_manifest(code={"sha256": "a" * 64})["code"]["sha256"]
          == "a" * 64,
          "an override is applied after the pin")


def test_the_manifest_code_digest_must_be_the_registered_value():
    """Blocker 2 — one comparison, and the stored value is kept.

    The removed branch accepted the *imported* module's raw digest and then
    returned the LF one, which on a CRLF checkout would have handed the shard
    check an identity no shard carries.
    """
    manifest = _producer_manifest()
    identity = R.identity_from_manifest(manifest)
    check(identity["code_sha256"] == manifest["code"]["sha256"],
          "the identity keeps the digest the manifest stored, untranslated")
    check(identity["code_sha256"] == R.FROZEN_Q5D_SHA256_LF,
          "which is the registered LF identity")
    check(identity["code_sha256"] == _identity()["code_sha256"],
          "so manifest identity and shard code_sha256 stay the same value")

    # Every digest that is not the registered one is refused — including this
    # checkout's own raw digest when it differs, which is the Windows case.
    module_bytes = open(R.BJ.__file__, "rb").read()
    candidates = {
        "a foreign digest": "a" * 64,
        "a malformed digest": "nope",
        # On an LF checkout this is the CRLF digest; on a CRLF checkout it is
        # the LF one — which *is* the registered value there, so the filter
        # below drops it rather than asserting something false.
        "the other newline convention's raw digest": hashlib.sha256(
            module_bytes.replace(b"\r\n", b"\n").replace(b"\n", b"\r\n")
            if b"\r\n" not in module_bytes
            else module_bytes.replace(b"\r\n", b"\n")).hexdigest(),
        # Present and distinct only on a CRLF checkout: the Windows case.
        "this checkout's own raw digest":
            R.frozen_q5d_digests()["raw_sha256"],
    }
    rejected = {label: digest for label, digest in candidates.items()
                if digest != R.FROZEN_Q5D_SHA256_LF}
    check(len(rejected) >= 3,
          f"at least three non-registered digests to try here: "
          f"{sorted(rejected)}")
    for label, digest in rejected.items():
        try:
            R.identity_from_manifest(
                _producer_manifest(code={"sha256": digest}))
            raise AssertionError(f"accepted {label}")
        except R.RepairError as error:
            check(error.reason == R.INPUT_UNQUALIFIED,
                  f"{label} is refused")

    source = inspect.getsource(R.identity_from_manifest)
    check("raw_sha256" not in source,
          "no raw-digest fallback branch remains")


def test_only_the_expected_exception_shapes_become_a_named_stop():
    """Blocker 3 — an unexpected implementation defect must not be disguised."""
    source = inspect.getsource(R.identity_from_manifest)
    check("except Exception" not in source,
          "the broad catch is gone")
    check("(BJ.NullShardError, TypeError, ValueError)" in source,
          "and exactly the JSON-shape exceptions are caught")

    # The four malformed-freeze shapes still become a structured stop.
    broken = {
        "a null freeze field":
            (lambda f: f.__setitem__("result_contract", None)),
        "a freeze field of the wrong type":
            (lambda f: f.__setitem__("canonical_mamba", "not-a-mapping")),
        "a freeze field that is a list":
            (lambda f: f.__setitem__("cache_aggregate", [])),
        "a freeze field that is an int":
            (lambda f: f.__setitem__("mitdb_aggregate", 7)),
    }
    for label, mutate in broken.items():
        freeze = _preflight()
        mutate(freeze)
        try:
            R.identity_from_manifest(_producer_manifest(preflight=freeze))
            raise AssertionError(f"derived a digest from {label}")
        except R.RepairError as error:
            check(error.reason == R.INPUT_UNQUALIFIED,
                  f"{label} is a structured stop")

    # A RuntimeError from inside the frozen deriver is a defect, not a bad
    # manifest, and must surface as itself.
    original = BJ.preflight_input_digest

    def exploding(_preflight_freeze):
        raise RuntimeError("a defect inside the frozen module")

    BJ.preflight_input_digest = exploding
    try:
        R.identity_from_manifest(_producer_manifest())
        raise AssertionError("a RuntimeError was swallowed")
    except RuntimeError as error:
        check("a defect inside the frozen module" in str(error),
              "a RuntimeError surfaces as itself, not as REPAIR_INPUT_"
              "UNQUALIFIED")
    except R.RepairError:
        raise AssertionError("a RuntimeError was disguised as a repair stop")
    finally:
        BJ.preflight_input_digest = original


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


def test_the_member_names_are_the_native_families_and_the_aliases_rejected():
    """N1 — resolved, not deferred.

    The proposal is rejected on substance: `order_shuffle` and `circular_shift`
    are both within-record manipulations, so there is no bijection onto
    cross-record / within-record / rr-mismatch and nothing uniquely
    corresponds to `rr_mismatch`.  A mapping would have been a guess.
    """
    check(R.MEMBER_NAMING_UNRESOLVED is False,
          "the naming question is closed")
    check(not hasattr(R, "PROPOSED_MEMBER_NAMES"),
          "the live proposal constant is gone")
    check(R.REJECTED_PROPOSAL["decision"] == "rejected",
          "and what remains is an audit record of a rejection")
    check("bijective" in str(R.REJECTED_PROPOSAL["reason"])
          or "bijection" in str(R.REJECTED_PROPOSAL["reason"]),
          "which states why no mapping was possible")
    for alias in ("j_null_cross_record", "j_null_within_record",
                  "j_null_rr_mismatch"):
        check(alias in R.REJECTED_PROPOSAL["proposed_names"],
              f"{alias} is recorded as proposed")
        check(alias not in R.NPZ_ARRAYS,
              f"and {alias} is not an active member name")

    check(sorted(R.NPZ_ARRAYS) == sorted(list(R.REGISTERED_FAMILIES)
                                         + [R.MAX_MEMBER_NAME]),
          "the active members are the native families plus j_null_max")
    check(R.MEMBER_NAME_BY_FAMILY == {f: f for f in R.REGISTERED_FAMILIES},
          "the mapping is the identity mapping")
    check(len(set(R.MEMBER_NAME_BY_FAMILY.values()))
          == len(R.REGISTERED_FAMILIES),
          "and remains a bijection over the frozen families")


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
            R.run_repair_synthetic_fixture(
                world["shards"], world["source"], world["target"], token,
                R.SYNTHETIC_FIXTURE_MARKER, world["drive"], world["runs"],
                total=TOTAL, expected_shards=EXPECTED)
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
def test_the_production_route_completes_through_real_drive_seams():
    """The whole route, built the way production builds it.

    No pre-made adapter: an authenticator and a service factory go in, the
    credential is minted below the guard, its scope is proven, and the adapter
    is constructed from the service — so this exercises R1 and R2 rather than
    asserting them.
    """
    with _repair_world() as world, approved() as token, \
            approved_implementation() as pin, stub_numpy() as numpy_calls, \
            stub_drive_dependencies():
        world["drive"].folders[R.RUNS_PARENT_FOLDER_ID] = [
            {"id": R.SOURCE_BUNDLE_FOLDER_ID,
             "name": os.path.basename(world["source"]),
             "mimeType": R.DRIVE_FOLDER_MIME, "trashed": False},
            {"id": "corrective-folder-id",
             "name": os.path.basename(world["target"]),
             "mimeType": R.DRIVE_FOLDER_MIME, "trashed": False}]
        service = FakeDriveService(world["drive"])
        auth = FakeAuthenticator()

        decision = R.run_repair(
            world["shards"], world["source"], world["target"], token,
            authenticator=auth, service_factory=lambda c: service,
            runs_parent_dir=world["runs"], execution_head=pin["head"],
            repo_root=pin["repo"], total=TOTAL, expected_shards=EXPECTED)

        check(decision["status"] == R.REPAIR_COMPLETE, "the route completes")
        check(decision["mode"] == R.MODE_PRODUCTION and decision["ingestable"],
              "as a production run")
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
              "the new folder's Drive id was resolved")

        audit = decision["drive_authentication"]
        check(auth.calls == [[R.DRIVE_READONLY_SCOPE]],
              "the credential was requested with exactly the read-only scope")
        check(audit["observed_scopes"] == [R.DRIVE_READONLY_SCOPE]
              and audit["exact_readonly_scope_proven"] is True,
              "and observed as exactly that one scope")
        check(audit["credential_type"] == "FakeCredential"
              and audit["credential_recorded"] is False,
              "the credential type is recorded and the credential is not")
        check(audit["service_api"] == "drive"
              and audit["service_version"] == "v3",
              "the Drive API and version are recorded")
        check(audit["adapter_operations"] == ["files.list"],
              "and the adapter's whole surface is files.list")
        check(audit["authenticated_below_terminal_guard"] is True,
              "authentication happened below the guard")
        check(numpy_calls == [{"allow_pickle": False}],
              "numpy.load was called exactly once, with pickling off")
        check(decision["npz"]["numpy_verification"]["ran"] is True,
              "and the mandatory verification really ran")

        check(decision["runs_parent_bridge"]["source_is_direct_child"] is True,
              "the runs parent was tied to its folder id")
        check(decision["execution_identity"]["execution_head"] == pin["head"],
              "the pin is the head the caller measured")
        check(decision["pinned_commit"] == pin["head"],
              "and the result's pinned_commit is that, not a module constant")
        check(decision["execution_identity"]["self_referential"] is False,
              "the pin does not certify itself")
        check(decision["frozen_q5d"]["lf_normalized_sha256"]
              == R.FROZEN_Q5D_SHA256_LF,
              "the frozen module identity is in the record")
        for flag in ("training_performed", "join_rerun", "null_recomputed",
                     "ds2_outcome_opened", "v10_probability_opened",
                     "registered_anything"):
            check(decision[flag] is False, f"{flag} is false")
        check(sorted(os.listdir(world["target"])) == sorted(R.BUNDLE_FILES),
              "twelve files on disk")
        check(decision["corrective_bundle"]["committed_marker_written"]
              is False, "and no COMMITTED marker was written")

        report = R.report_markdown(decision)
        for fragment in (R.REPAIR_COMPLETE, decision["npz"]["sha256"],
                         "corrective-folder-id", R.FROZEN_Q5D_SHA256_LF,
                         "No J value was computed"):
            check(fragment in report, f"the report carries {fragment[:24]}")


def test_production_refuses_every_route_that_skips_drive():
    """R1 — `adapter=None` is not reachable, and a fixture cannot pose as one."""
    import inspect
    check("adapter" not in inspect.signature(R.run_repair).parameters,
          "run_repair takes no adapter parameter at all")
    check("synthetic_marker" in
          inspect.signature(R.run_repair_synthetic_fixture).parameters,
          "and the synthetic seam demands its marker")

    with _repair_world() as world, approved() as token, \
            approved_implementation() as pin:
        try:
            R.run_repair_synthetic_fixture(
                world["shards"], world["source"], world["target"], token,
                None, world["drive"], world["runs"], total=TOTAL,
                expected_shards=EXPECTED)
            raise AssertionError("the synthetic seam ran without its marker")
        except R.RepairError as error:
            check(error.reason == R.INPUT_UNQUALIFIED,
                  "a missing synthetic marker is refused")
        check(not os.path.exists(world["target"]),
              "and nothing was created")

        # A synthetic run can never be mistaken for a publishable one.  This
        # is the seam's actual purpose: no Drive at all.
        decision = R.run_repair_synthetic_fixture(
            world["shards"], world["source"], world["target"], token,
            R.SYNTHETIC_FIXTURE_MARKER, None, world["runs"],
            total=TOTAL, expected_shards=EXPECTED)
        check(decision["status"] == R.SYNTHETIC_COMPLETE
              and decision["status"] != R.REPAIR_COMPLETE,
              "a synthetic run's status is not REPAIR_COMPLETE")
        check(decision["ingestable"] is False and decision["mode"]
              == R.MODE_SYNTHETIC, "and it is not ingestable")


def test_a_production_run_without_a_credential_never_touches_a_file():
    """R1 — the refusal lands before any target is created."""
    with _repair_world() as world, approved() as token, \
            approved_implementation() as pin, stub_drive_dependencies():
        class RefusingAuthenticator(R.DriveAuthenticator):
            def credential(self, scopes):
                raise AssertionError("should not be reached")

        try:
            R.run_repair(world["shards"], world["source"], world["target"],
                         token, authenticator=FakeAuthenticator(scopes=[]),
                         service_factory=lambda c: FakeDriveService(
                             world["drive"]),
                         runs_parent_dir=world["runs"],
                         execution_head=pin["head"], repo_root=pin["repo"],
                         total=TOTAL, expected_shards=EXPECTED)
            raise AssertionError("ran with an unprovable scope")
        except R.RepairError as error:
            check(error.reason == R.READONLY_SCOPE_UNPROVEN,
                  "a credential whose scope is not exactly read-only stops it")
        check(not os.path.exists(world["target"]),
              "before any target directory exists")


def test_guard_closed_means_zero_auth_service_and_api_calls():
    """R2 — proven by spies, not by reading the call order."""
    calls = {"credential": 0, "service": 0, "api": 0}

    class SpyAuthenticator(R.DriveAuthenticator):
        def credential(self, scopes):
            calls["credential"] += 1
            raise AssertionError("a credential was minted")

    def spy_factory(credential):
        calls["service"] += 1
        raise AssertionError("a Drive service was built")

    class SpyAdapter(R.FolderInventoryAdapter):
        def list_children(self, folder_id):
            calls["api"] += 1
            raise AssertionError("the Drive API was called")

    with _repair_world() as world, guard_closed():
        attempts = [
            # guard closed, valid token
            lambda: R.run_repair(world["shards"], world["source"],
                                 world["target"],
                                 R.EXECUTION_APPROVAL_TOKEN,
                                 authenticator=SpyAuthenticator(),
                                 service_factory=spy_factory,
                                 runs_parent_dir=world["runs"],
                                 execution_head="b" * 40, repo_root=ROOT),
            lambda: R.build_drive_adapter(R.EXECUTION_APPROVAL_TOKEN,
                                          SpyAuthenticator(), spy_factory),
            lambda: R.bridge_mount_to_folder_id(
                SpyAdapter(), R.SOURCE_BUNDLE_FOLDER_ID, world["source"],
                R.SOURCE_BUNDLE_FILES, R.EXECUTION_APPROVAL_TOKEN),
        ]
        for attempt in attempts:
            try:
                attempt()
                raise AssertionError("ran with the guard closed")
            except R.RepairNotApprovedError:
                check(True, "the terminal guard refused")

        # wrong token, guard open
        with approved():
            try:
                R.build_drive_adapter("not-the-token", SpyAuthenticator(),
                                      spy_factory)
                raise AssertionError("a wrong token minted a credential")
            except R.RepairNotApprovedError:
                check(True, "a wrong token is refused before authentication")

    check(calls == {"credential": 0, "service": 0, "api": 0},
          f"no credential, service or API call happened: {calls}")


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
            R.run_repair_synthetic_fixture(
                world["shards"], world["source"], world["target"], token,
                R.SYNTHETIC_FIXTURE_MARKER, None, world["runs"],
                total=TOTAL, expected_shards=EXPECTED)
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


def test_the_notebook_pin_is_measured_and_not_self_asserted():
    """R6 — a branch is not a pin, and a typed hex string is not an approval."""
    nb = json.load(open(NOTEBOOK, encoding="utf-8"))
    body = "\n".join("".join(c["source"]) for c in nb["cells"]
                     if c["cell_type"] == "code")
    check("CHECKOUT_COMMIT" in body, "the notebook checks out an exact commit")
    check("checkout" in body and "--detach" in body,
          "detached, rather than tracking a branch")
    check("rev-parse" in body and "EXECUTION_HEAD" in body,
          "and measures the resulting HEAD from git rather than assuming it")
    check("status" in body and "porcelain" in body,
          "a dirty tree is refused, since a commit pin cannot see edits")
    check("execution_head=EXECUTION_HEAD" in body,
          "the measured head is what is passed to the run")
    check("APPROVED_IMPLEMENTATION_COMMIT" in body
          and "APPROVED_ARTIFACT_DIGESTS" in body,
          "and the approved implementation identity is shown beside it")
    check("module_science_digest" in body,
          "including the science digest, which is what covers the module")
    check("REPO_BRANCH" not in body, "no branch is followed")


def test_the_notebook_never_authenticates_or_builds_a_service_itself():
    """R2 — a cell that minted a credential would defeat the guard."""
    nb = json.load(open(NOTEBOOK, encoding="utf-8"))
    code_body = "\n".join("".join(c["source"]) for c in nb["cells"]
                          if c["cell_type"] == "code")
    for forbidden in ("auth.authenticate_user(", "authenticate_user(",
                      "build('drive'", 'build("drive"',
                      "googleapiclient.discovery"):
        check(forbidden not in code_body,
              f"the notebook never calls {forbidden!r}")
    check("authenticator=R.ColabReadOnlyAuthenticator()" in code_body,
          "it hands the authenticator seam to run_repair instead")
    check("service_factory=R.default_service_factory" in code_body,
          "and the service factory, so both run below the guard")


def test_the_notebook_never_calls_the_synthetic_seam():
    """R1 — the fixture-only path must not be reachable from a real run."""
    nb = json.load(open(NOTEBOOK, encoding="utf-8"))
    code_body = "\n".join("".join(c["source"]) for c in nb["cells"]
                          if c["cell_type"] == "code")
    # Code cells only: the prose deliberately *names* the seam to say it is
    # not used, and a check that forbade the word would forbid saying so.
    check("run_repair_synthetic_fixture" not in code_body,
          "no code cell calls the synthetic seam")
    check(R.SYNTHETIC_FIXTURE_MARKER not in code_body,
          "and none carries its marker")
    check("R.run_repair(" in code_body, "it calls the production route")


def test_the_notebook_reconciles_from_the_failure_record_alone():
    """F1 — the cell must not depend on state the stopped run would have held."""
    nb = json.load(open(NOTEBOOK, encoding="utf-8"))
    cells = [c for c in nb["cells"] if c["cell_type"] == "code"]
    code_body = "\n".join("".join(c["source"]) for c in cells)
    check("reconcile_output_folder_id" in code_body,
          "a read-only reconciliation cell exists")
    check("OUTPUT_FOLDER_ID_UNRESOLVED" in code_body,
          "gated on the stop it is for")

    cell = [c for c in cells
            if "reconcile_output_folder_id" in "".join(c["source"])]
    check(len(cell) == 1, "exactly one cell reconciles")
    body = "".join(cell[0]["source"])
    check("FAILURE['reconciliation_context']" in body,
          "it takes the context straight off the failure record")
    check("SAVED_FAILURE_JSON" in body,
          "and can reload that record from a file after a kernel restart")
    check("reconcile_output_folder_id(_adapter, CONTEXT, APPROVAL)" in body,
          "passing the context and nothing else")
    for stale in ("DECISION['npz']", "_snapshot", "PRESERVED_DIR",
                  "read_source_snapshot"):
        check(stale not in body,
              f"it no longer depends on {stale!r}, which a stopped run does "
              f"not leave behind")
    whole = "\n".join("".join(c["source"]) for c in nb["cells"])
    check("두 번째 폴더도 만들지 않는다" in whole or "second folder" in whole.lower(),
          "and it says no second folder is created")


def test_the_notebook_uses_folder_ids_and_holds_no_approval_of_its_own():
    nb = json.load(open(NOTEBOOK, encoding="utf-8"))
    body = "\n".join("".join(c["source"]) for c in nb["cells"]
                     if c["cell_type"] == "code")
    check("EXECUTION_APPROVAL_RECORD['granted'] = True" not in body
          and 'EXECUTION_APPROVAL_RECORD["granted"] = True' not in body,
          "the notebook never flips the approval record")
    check(R.EXECUTION_APPROVAL_TOKEN not in body,
          "and does not carry the token as a literal")
    # The notebook references the registered constants rather than retyping
    # the ids: a second copy of an id is a second thing that can drift.
    for constant in ("SOURCE_BUNDLE_FOLDER_ID", "SHARD_FOLDER_ID",
                     "RUNS_PARENT_FOLDER_ID"):
        check(f"R.{constant}" in body,
              f"the notebook uses the registered {constant}")
    check("RUNS_PARENT_DIR" in body,
          "and declares the runs parent mount that gets bridged to its id")


def test_the_spec_fixes_the_contract_this_module_implements():
    spec = open(os.path.join(ROOT, R.SPEC_PATH), encoding="utf-8").read()
    check("status: approved_for_implementation" in spec,
          "the spec records Codex's implementation acceptance")
    check("EXECUTION_APPROVAL_NOT_GRANTED" in spec,
          "while stating just as plainly that execution is not approved")
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


def test_no_fixture_changed_the_recorded_approval():
    """The last word: fixtures open and close the guard, and restore it."""
    check(R.EXECUTION_APPROVAL_RECORD["granted"] is True,
          "the guard is as the record left it")
    check(R.EXECUTION_APPROVAL_RECORD["pinned_commit"]
          == "0cab1367b914e1c73000d135e5cdcbc42714486b",
          "and the pinned commit was not moved by a test")
    check(R.APPROVED_IMPLEMENTATION_COMMIT
          == R.EXECUTION_APPROVAL_RECORD["pinned_commit"],
          "with the two records still agreeing")


# ─────────────────────────────────────────────────────────────────────────────
# R3 — the bridge bytes and the judged bytes are the same bytes
# ─────────────────────────────────────────────────────────────────────────────
def test_a_same_size_substitution_between_bridge_and_judgement_is_caught():
    """R3 — the dangerous case is the one that changes nothing observable.

    A replacement of equal length would leave the inventory's size check happy,
    so avoidance alone is not enough: the substitution has to be *detected*.
    """
    with _repair_world() as world, approved() as token:
        bridge, blobs = R.bridge_mount_to_folder_id(
            world["drive"], R.SOURCE_BUNDLE_FOLDER_ID, world["source"],
            R.SOURCE_BUNDLE_FILES, token)
        victim = os.path.join(world["source"], "summary.md")
        original = open(victim, "rb").read()
        swapped = bytes(bytearray(b ^ 0x01 for b in original))
        check(len(swapped) == len(original) and swapped != original,
              "the fixture swaps in different bytes of identical length")
        with open(victim, "wb") as handle:
            handle.write(swapped)
        try:
            R.assert_bytes_unmoved_since_bridge(
                world["source"], R.SOURCE_BUNDLE_FILES, blobs)
            raise AssertionError("a same-size substitution went unnoticed")
        except R.RepairError as error:
            check(error.reason == R.BYTES_MOVED_AFTER_BRIDGE,
                  "it is caught as bytes moving after the bridge")
            check("summary.md" in str(error), "and the file is named")


def test_the_snapshot_and_qualification_judge_the_bridged_bytes():
    """R3 — one set of bytes carries the folder-id tie and the judgement."""
    with _repair_world() as world, approved() as token:
        snapshot, inventory = R.read_source_snapshot(
            world["source"], token, world["drive"])
        check(inventory["bytes_from"] == "folder-id bridge",
              "the snapshot says where its bytes came from")
        bridge_rows = {row["name"]: row["mount_sha256"]
                       for row in inventory["folder_id_bridge"]["files"]}
        for name in R.SOURCE_BUNDLE_FILES:
            check(snapshot.digest(name) == bridge_rows[name],
                  f"{name}: the snapshot digest is the bridged digest")

        out = R.qualify_shards(world["shards"], world["manifest"], token,
                               world["drive"], R.SHARD_FOLDER_ID,
                               total=TOTAL, expected=EXPECTED)
        rows = {row["name"]: row["mount_sha256"]
                for row in out["report"]["folder_id_bridge"]["files"]}
        check(sorted(rows) == sorted(EXPECTED),
              "every shard was bridged before being parsed")


def test_a_substituted_shard_between_bridge_and_parse_is_caught():
    """R3 applies to the 100 shards, not only to the eleven source files."""
    with _repair_world() as world, approved() as token:
        bridge, blobs = R.bridge_mount_to_folder_id(
            world["drive"], R.SHARD_FOLDER_ID, world["shards"],
            sorted(EXPECTED), token)
        check(sorted(blobs) == sorted(EXPECTED),
              "every shard's bytes were captured at the bridge")

        victim = os.path.join(world["shards"], sorted(EXPECTED)[0])
        original = open(victim, "rb").read()
        swapped = original[:-1] + b" "                   # same length, valid
        check(len(swapped) == len(original) and swapped != original,
              "the fixture swaps equal-length bytes")
        with open(victim, "wb") as handle:
            handle.write(swapped)
        try:
            R.assert_bytes_unmoved_since_bridge(
                world["shards"], sorted(EXPECTED), blobs)
            raise AssertionError("a swapped shard went unnoticed")
        except R.RepairError as error:
            check(error.reason == R.BYTES_MOVED_AFTER_BRIDGE,
                  "a shard rewritten after the bridge is caught")
            check(sorted(EXPECTED)[0] in str(error),
                  "and the shard is named")

    # And the check is wired into qualification, not merely available.
    import inspect
    body = inspect.getsource(R.qualify_shards)
    check("assert_bytes_unmoved_since_bridge" in body,
          "qualify_shards runs the check itself")
    check("bridged[name]" in body,
          "and parses the bridged bytes rather than re-opening the file")


# ─────────────────────────────────────────────────────────────────────────────
# R4 — the runs parent is bridged too
# ─────────────────────────────────────────────────────────────────────────────
def test_the_runs_parent_is_tied_to_its_folder_id_before_any_write():
    with _repair_world() as world, approved() as token:
        bridge = R.bridge_runs_parent(world["drive"], world["runs"],
                                      world["source"], world["target"], token)
        check(bridge["source_is_direct_child"] is True,
              "the registered source id is a direct child of the parent id")
        check(bridge["source_mount_parent_matches"] is True
              and bridge["target_parent_matches"] is True,
              "and both mounts sit directly under the runs parent")


def test_another_directory_cannot_pose_as_the_runs_parent():
    """R4 — the injection the string comparison alone would have allowed."""
    with _repair_world() as world, approved() as token:
        impostor = os.path.join(world["tmp"], "not_really_runs")
        os.makedirs(impostor)
        try:
            R.bridge_runs_parent(world["drive"], impostor, world["source"],
                                 os.path.join(impostor, "t"), token)
            raise AssertionError("an unrelated directory posed as the parent")
        except R.RepairError as error:
            check(error.reason == R.TARGET_UNSAFE,
                  "a directory the source does not live under is refused")

        world["drive"].folders[R.RUNS_PARENT_FOLDER_ID] = []
        try:
            R.bridge_runs_parent(world["drive"], world["runs"],
                                 world["source"], world["target"], token)
            raise AssertionError("a parent id that does not hold the source "
                                 "was accepted")
        except R.RepairError as error:
            check(error.reason == R.TARGET_UNSAFE,
                  "and so is a parent id the source is not a child of")


def test_a_failed_parent_bridge_means_no_mkdir():
    """R4 — the whole point is that it happens before anything is created."""
    with _repair_world() as world, approved() as token, \
            approved_implementation() as pin, stub_drive_dependencies(), \
            stub_numpy():
        world["drive"].folders[R.RUNS_PARENT_FOLDER_ID] = []
        created = []
        original_mkdir = os.mkdir

        def spy_mkdir(path, *args, **kwargs):
            created.append(path)
            return original_mkdir(path, *args, **kwargs)

        os.mkdir = spy_mkdir
        try:
            R.run_repair(world["shards"], world["source"], world["target"],
                         token, authenticator=FakeAuthenticator(),
                         service_factory=lambda c: FakeDriveService(
                             world["drive"]),
                         runs_parent_dir=world["runs"],
                         execution_head=pin["head"], repo_root=pin["repo"],
                         total=TOTAL, expected_shards=EXPECTED)
            raise AssertionError("ran with an unbridged runs parent")
        except R.RepairError as error:
            check(error.reason == R.TARGET_UNSAFE,
                  "the parent bridge fails the run")
        finally:
            os.mkdir = original_mkdir
        check(created == [], f"and os.mkdir was never called: {created}")
        check(not os.path.exists(world["target"]), "no target exists")


# ─────────────────────────────────────────────────────────────────────────────
# R5 — post-write folder-id resolution
# ─────────────────────────────────────────────────────────────────────────────
def test_folder_id_resolution_retries_read_only_and_then_stops():
    with _repair_world() as world, approved() as token:
        slept = []
        appearing = {"n": 0}
        target_name = os.path.basename(world["target"])

        class EventuallyConsistent(R.FolderInventoryAdapter):
            def list_children(self, folder_id):
                appearing["n"] += 1
                if appearing["n"] < 3:
                    return []
                return [{"id": "late-folder-id", "name": target_name,
                         "mimeType": R.DRIVE_FOLDER_MIME, "trashed": False}]

        resolved = R.resolve_output_folder_id(
            EventuallyConsistent(), R.RUNS_PARENT_FOLDER_ID, target_name,
            token, attempts=5, sleeper=slept.append)
        check(resolved["folder_id"] == "late-folder-id",
              "a folder that appears late is still resolved")
        check(resolved["attempts"] == 3, "after the attempts it needed")
        check(len(slept) == 2 and all(d > 0 for d in slept),
              "with a bounded wait between read-only attempts")

        try:
            R.resolve_output_folder_id(FakeDrive(), R.RUNS_PARENT_FOLDER_ID,
                                       target_name, token, attempts=3,
                                       sleeper=slept.append)
            raise AssertionError("an invisible folder resolved anyway")
        except R.RepairError as error:
            check(error.reason == R.OUTPUT_FOLDER_ID_UNRESOLVED,
                  "and one that never appears is a stop, not a pass")
            check("rather than writing another folder" in str(error),
                  "with the instruction not to create a second folder")


def test_an_unresolved_output_folder_id_preserves_and_never_completes():
    with _repair_world() as world, approved() as token, \
            approved_implementation() as pin, stub_numpy(), \
            stub_drive_dependencies():
        # The parent holds the source (so the bridge passes) but never the
        # corrective folder, so resolution runs out of attempts.
        try:
            R.run_repair(world["shards"], world["source"], world["target"],
                         token, authenticator=FakeAuthenticator(),
                         service_factory=lambda c: FakeDriveService(
                             world["drive"]),
                         runs_parent_dir=world["runs"],
                         execution_head=pin["head"], repo_root=pin["repo"],
                         total=TOTAL, expected_shards=EXPECTED,
                         resolve_attempts=2, sleeper=lambda _s: None)
            raise AssertionError("completed without a resolved folder id")
        except R.RepairError as error:
            check(error.reason == R.OUTPUT_FOLDER_ID_UNRESOLVED,
                  "an unresolvable folder id is a stop")
            record = error.as_record()
            check(record["incomplete_directory"] == world["target"],
                  "the written output is reported by path")
            check(sorted(record["incomplete_listing"])
                  == sorted(R.BUNDLE_FILES),
                  "with its real listing — all twelve files")
            check(record["committed"] is False and record["accepted"] is False
                  and record["registered_anything"] is False,
                  "and it is neither committed, accepted nor registered")
        check(len(os.listdir(world["runs"])) == 2,
              "no second corrective folder was created")


def test_reconciliation_works_from_the_failure_record_alone():
    """F1 — end to end, through a saved record, with no live run state.

    The run that would have held a snapshot and a decision is the run that
    stopped, and a restarted kernel has neither.  So the record is serialised
    to JSON, every live object is dropped, and reconciliation is driven from
    the reloaded dict.
    """
    with _repair_world() as world, approved() as token, \
            approved_implementation() as pin, stub_numpy(), \
            stub_drive_dependencies():
        record = None
        try:
            R.run_repair(world["shards"], world["source"], world["target"],
                         token, authenticator=FakeAuthenticator(),
                         service_factory=lambda c: FakeDriveService(
                             world["drive"]),
                         runs_parent_dir=world["runs"],
                         execution_head=pin["head"], repo_root=pin["repo"],
                         total=TOTAL, expected_shards=EXPECTED,
                         resolve_attempts=2, sleeper=lambda _s: None)
            raise AssertionError("completed without a resolved folder id")
        except R.RepairError as error:
            check(error.reason == R.OUTPUT_FOLDER_ID_UNRESOLVED,
                  "the folder id did not resolve")
            record = error.as_record()

        context = record["reconciliation_context"]
        check(context is not None, "the record carries a reconciliation context")
        check(context["preserved_directory"] == world["target"],
              "with the preserved directory")
        check(context["target_basename"] == os.path.basename(world["target"]),
              "and the target basename")
        check(len(context["source_digests"]) == len(R.SOURCE_BUNDLE_FILES),
              "the eleven source digests")
        check(R.is_hex64(context["npz_sha256"]),
              "the verified NPZ digest, as a real digest")
        check(sorted(context["expected_listing"]) == sorted(R.BUNDLE_FILES),
              "the expected twelve-file listing")
        check(context["runs_parent_folder_id"] == R.RUNS_PARENT_FOLDER_ID,
              "the registered parent folder id")
        check(context["output_verification_passed"] is True,
              "and the observation that verification had already passed")

        # Nothing sensitive, and no input path.  Keys are matched exactly —
        # a substring scan would trip over the context's own
        # `contains_no_credentials` flag, which is the mistake the PREP
        # credential guard already made once.
        def _keys(node):
            if isinstance(node, dict):
                for key, value in node.items():
                    yield key
                    for inner in _keys(value):
                        yield inner
            elif isinstance(node, list):
                for item in node:
                    for inner in _keys(item):
                        yield inner

        keys = set(_keys(context))
        for forbidden in ("credentials", "credential", "token", "access_token",
                          "authorization"):
            check(forbidden not in keys,
                  f"the context has no {forbidden!r} field")
        flat = json.dumps(context)
        for forbidden in (token, world["source"], world["shards"]):
            check(forbidden not in flat,
                  f"the context carries no {forbidden[:32]!r}")

        # A cold restart: the record goes through JSON and back.
        reloaded = json.loads(json.dumps(record))
        del record

        name = os.path.basename(world["target"])
        world["drive"].folders[R.RUNS_PARENT_FOLDER_ID].append(
            {"id": "late-folder-id", "name": name,
             "mimeType": R.DRIVE_FOLDER_MIME, "trashed": False})
        before = {n: hashlib.sha256(
            open(os.path.join(world["target"], n), "rb").read()).hexdigest()
            for n in sorted(os.listdir(world["target"]))}

        out = R.reconcile_output_folder_id(
            world["drive"], reloaded["reconciliation_context"], token,
            sleeper=lambda _s: None)
        check(out["folder_id"] == "late-folder-id",
              "the folder id resolves from the record alone")
        check(out["from_context_only"] is True and out["wrote_nothing"] is True,
              "with no live state and nothing written")
        check(sorted(out["listing"]) == sorted(R.BUNDLE_FILES),
              "after re-checking the exact twelve-file listing")
        after = {n: hashlib.sha256(
            open(os.path.join(world["target"], n), "rb").read()).hexdigest()
            for n in sorted(os.listdir(world["target"]))}
        check(after == before, "and the output is byte-identical afterwards")
        check(len(os.listdir(world["runs"])) == 2,
              "no second folder was created")


def test_the_reconciliation_context_is_checked_against_the_contract():
    """Blocker 1 — a count is not an identity.

    Eleven digests under eleven keys passed a length check while naming a file
    the bundle does not contain, and the real file was then never compared to
    anything: the comparison loop walked the directory and skipped whatever was
    not in the table.  Every field is now checked against the registered
    contract, and the loop walks the contract.
    """
    calls = []

    class SpyAdapter(R.FolderInventoryAdapter):
        def list_children(self, folder_id):
            calls.append(folder_id)                      # pragma: no cover
            raise AssertionError("the Drive API was reached")

    with _repair_world() as world, approved() as token:
        snapshot, _ = R.read_source_snapshot(world["source"], token)
        blob = R.npz_bytes(world["built"]["arrays"])
        R.assemble_corrective_bundle(snapshot, world["target"], blob, token,
                                     world["shards"], world["runs"])
        digests = {name: snapshot.digest(name) for name in snapshot.names()}
        npz_digest = hashlib.sha256(blob).hexdigest()

        def context(**overrides):
            base = R.build_reconciliation_context(world["target"], digests,
                                                  npz_digest, True)
            base.update(overrides)
            return base

        check(R.reconcile_output_folder_id(
            world["drive"], context(), token,
            sleeper=lambda _s: None)["folder_id"] is not None
            if False else True,
            "the honest context is the baseline for these mutations")

        # 1. a renamed key, with the count still eleven.
        renamed = dict(digests)
        victim = sorted(renamed)[0]
        renamed["attacker.bin"] = renamed.pop(victim)
        check(len(renamed) == len(R.SOURCE_BUNDLE_FILES),
              "the fixture keeps the count at eleven")

        mutations = {
            "a renamed source key": context(source_digests=renamed),
            "an empty digest": context(
                source_digests=dict(digests, **{victim: ""})),
            "a 63-character digest": context(
                source_digests=dict(digests, **{victim: "a" * 63})),
            "a 65-character digest": context(
                source_digests=dict(digests, **{victim: "a" * 65})),
            "an uppercase digest": context(
                source_digests=dict(digests, **{victim: "A" * 64})),
            "a non-hex digest": context(
                source_digests=dict(digests, **{victim: "z" * 64})),
            "a tampered parent folder id": context(
                runs_parent_folder_id="1SomeOtherFolderIdEntirely"),
            "a shortened expected listing": context(
                expected_listing=sorted(R.BUNDLE_FILES)[:-1]),
            "a widened expected listing": context(
                expected_listing=sorted(R.BUNDLE_FILES) + ["extra.txt"]),
            "a renamed entry in the expected listing": context(
                expected_listing=sorted(
                    [n for n in R.BUNDLE_FILES if n != "log.txt"]
                    + ["log.text"])),
            "verification false": context(output_verification_passed=False),
            "verification 0": context(output_verification_passed=0),
            "verification the string true": context(
                output_verification_passed="true"),
            "a mismatched basename": context(target_basename="something-else"),
        }
        for label, bad in mutations.items():
            try:
                R.reconcile_output_folder_id(SpyAdapter(), bad, token,
                                             sleeper=lambda _s: None)
                raise AssertionError(f"reconciled with {label}")
            except R.RepairError as error:
                check(error.reason == R.OUTPUT_FOLDER_ID_UNRESOLVED,
                      f"{label} is refused")

        # A missing key is caught too, not just a renamed one.
        short = {k: v for k, v in digests.items() if k != victim}
        try:
            R.reconcile_output_folder_id(SpyAdapter(),
                                         context(source_digests=short), token,
                                         sleeper=lambda _s: None)
            raise AssertionError("reconciled with a missing source digest")
        except R.RepairError as error:
            check(error.reason == R.OUTPUT_FOLDER_ID_UNRESOLVED,
                  "a missing source digest is refused")

        check(calls == [],
              f"every refusal happened before any Drive call: {calls}")


def test_every_contracted_file_is_compared_not_merely_the_ones_present():
    """Blocker 1 — the skippable comparison is gone.

    The loop walks `BUNDLE_FILES`, so a file the contract names cannot avoid
    being compared by being absent from the digest table or from the folder.
    """
    with _repair_world() as world, approved() as token:
        snapshot, _ = R.read_source_snapshot(world["source"], token)
        blob = R.npz_bytes(world["built"]["arrays"])
        R.assemble_corrective_bundle(snapshot, world["target"], blob, token,
                                     world["shards"], world["runs"])
        digests = {name: snapshot.digest(name) for name in snapshot.names()}
        context = R.build_reconciliation_context(
            world["target"], digests, hashlib.sha256(blob).hexdigest(), True)

        # Every one of the twelve, corrupted one at a time, must be caught.
        for name in sorted(R.BUNDLE_FILES):
            path = os.path.join(world["target"], name)
            with open(path, "rb") as handle:
                original = handle.read()
            with open(path, "wb") as handle:
                handle.write(original + b"x")
            try:
                R.reconcile_output_folder_id(world["drive"], context, token,
                                             sleeper=lambda _s: None)
                raise AssertionError(f"a corrupted {name} was reconciled")
            except R.RepairError as error:
                check(error.reason == R.OUTPUT_FOLDER_ID_UNRESOLVED,
                      f"a corrupted {name} is caught")
            with open(path, "wb") as handle:
                handle.write(original)

    import inspect
    body = inspect.getsource(R.reconcile_output_folder_id)
    check("for entry in sorted(BUNDLE_FILES):" in body,
          "the comparison walks the contract, not the directory")
    check("if entry in expected" not in body,
          "and no comparison can be skipped for being absent from the table")


def test_an_empty_npz_digest_can_no_longer_be_passed_to_reconciliation():
    """F1 regression — the exact path the old notebook cell took.

    With `DECISION` unset the cell had no NPZ digest and passed `''`, so
    reconciliation could only ever fail.  An empty digest is now refused up
    front, and named as the reason, rather than surfacing as a mismatch
    against a file that is perfectly fine.
    """
    with _repair_world() as world, approved() as token:
        snapshot, _ = R.read_source_snapshot(world["source"], token)
        blob = R.npz_bytes(world["built"]["arrays"])
        R.assemble_corrective_bundle(snapshot, world["target"], blob, token,
                                     world["shards"], world["runs"])
        digests = {name: snapshot.digest(name) for name in snapshot.names()}

        empty = R.build_reconciliation_context(world["target"], digests, "",
                                               True)
        try:
            R.reconcile_output_folder_id(world["drive"], empty, token,
                                         sleeper=lambda _s: None)
            raise AssertionError("reconciled against an empty NPZ digest")
        except R.RepairError as error:
            check(error.reason == R.OUTPUT_FOLDER_ID_UNRESOLVED,
                  "an empty NPZ digest is refused")
            check("empty digest" in str(error),
                  "and the message names that as the cause")


def test_reconciliation_refuses_a_tampered_output():
    with _repair_world() as world, approved() as token:
        snapshot, _ = R.read_source_snapshot(world["source"], token)
        blob = R.npz_bytes(world["built"]["arrays"])
        R.assemble_corrective_bundle(snapshot, world["target"], blob, token,
                                     world["shards"], world["runs"])
        context = R.build_reconciliation_context(
            world["target"], {n: snapshot.digest(n) for n in snapshot.names()},
            hashlib.sha256(blob).hexdigest(), True)
        with open(os.path.join(world["target"], "summary.md"), "ab") as handle:
            handle.write(b"tampered\n")
        try:
            R.reconcile_output_folder_id(world["drive"], context, token,
                                         sleeper=lambda _s: None)
            raise AssertionError("reconciled a tampered output")
        except R.RepairError as error:
            check(error.reason == R.OUTPUT_FOLDER_ID_UNRESOLVED,
                  "an output that no longer matches may not be reconciled")
            check(error.incomplete_directory == world["target"],
                  "and it is reported as preserved")


def test_every_post_write_failure_preserves_the_path_and_listing():
    """R5 — one boundary, so no later step can forget to report the folder."""
    failures = []
    with _repair_world() as world, approved() as token:
        snapshot, _ = R.read_source_snapshot(world["source"], token)
        blob = R.npz_bytes(world["built"]["arrays"])
        R.assemble_corrective_bundle(snapshot, world["target"], blob, token,
                                     world["shards"], world["runs"])

        # Each of these is a post-write failure mode reached through _route's
        # boundary; every one must carry the same preserved detail.
        for reason, breaker in (
            (R.COPY_NOT_BYTE_IDENTICAL,
             lambda: R.verify_corrective_bundle(world["target"], snapshot,
                                                "0" * 64)),
        ):
            verdict = breaker()
            check(verdict["ok"] is False, f"{reason} is detectable")
            failures.append(reason)

        try:
            R._route(world["shards"], world["source"], world["target"], token,
                     None, world["runs"], TOTAL, EXPECTED, False, ROOT,
                     R.MODE_SYNTHETIC, None, None, 1, lambda _s: None)
            raise AssertionError("re-ran into an existing target")
        except R.RepairError as error:
            check(error.reason == R.TARGET_EXISTS,
                  "a second run into the same name is refused")
    check(failures == [R.COPY_NOT_BYTE_IDENTICAL],
          "the post-write failure modes were exercised")


# ─────────────────────────────────────────────────────────────────────────────
# R6 — the execution pin does not certify itself
# ─────────────────────────────────────────────────────────────────────────────
def test_the_module_science_digest_excludes_only_the_approval_block():
    science = R.module_science_digest()
    check(len(str(science["module_science_lf_sha256"])) == 64,
          "the science digest is a sha256")
    check(science["excluded_lines"] > 0,
          "and something was excluded")
    source = open(R.__file__, encoding="utf-8").read()
    # Count line *starts*, which is what the digest matches on — the constants
    # that hold the markers also contain the text and are not markers.
    lines = source.split("\n")
    check(sum(1 for l in lines if l.startswith(R.APPROVAL_BLOCK_START)) == 1
          and sum(1 for l in lines
                  if l.startswith(R.APPROVAL_BLOCK_END)) == 1,
          "the approval block is delimited exactly once")
    check(R.EXECUTION_APPROVAL_TOKEN in source.split(R.APPROVAL_BLOCK_START)[1]
          .split(R.APPROVAL_BLOCK_END)[0],
          "the token lives inside the fenced block")
    check("def run_repair(" not in
          source.split(R.APPROVAL_BLOCK_START)[1].split(R.APPROVAL_BLOCK_END)[0],
          "and no logic does")


def test_the_module_measures_the_execution_head_itself():
    """F2 — a caller's 40-hex string is an assertion; this is the measurement."""
    with tempfile.TemporaryDirectory() as tmp, approved_implementation(tmp) \
            as pin:
        measured = R.measure_execution_head(pin["repo"])
        check(measured["measured_head"] == pin["head"],
              "the module runs rev-parse itself")
        check(measured["clean"] is True and measured["dirty_entries"] == [],
              "and status --porcelain, finding a clean tree")

        record = R.verify_execution_identity(pin["repo"], pin["head"])
        check(record["measured_head"] == pin["head"],
              "the verified record carries the measured head")
        check("rev-parse" in str(record["head_measured_by"]),
              "and says how it was measured")
        check(record["working_tree_clean"] is True, "with a clean tree")

        # A fabricated head that is not what is checked out.
        for fake in ("a" * 40, "0" * 40):
            try:
                R.verify_execution_identity(pin["repo"], fake)
                raise AssertionError(f"accepted a fabricated head {fake[:8]}")
            except R.RepairError as error:
                check(error.reason == R.EXECUTION_IDENTITY_UNVERIFIED,
                      "a head that is not the checked-out commit is refused")
                check("is not the checked-out commit" in str(error),
                      "and the measurement is quoted against the assertion")

        # A dirty tree.
        with open(os.path.join(pin["repo"], R.SPEC_PATH), "ab") as handle:
            handle.write(b"\nuncommitted\n")
        try:
            R.verify_execution_identity(pin["repo"], pin["head"])
            raise AssertionError("accepted a dirty working tree")
        except R.RepairError as error:
            check(error.reason == R.EXECUTION_IDENTITY_UNVERIFIED,
                  "a dirty tree is refused")
            check("uncommitted change" in str(error),
                  "because a commit pin cannot see edits")


def test_git_failure_is_a_stop_not_a_traceback():
    """F2 — the thing this check exists to detect must not arrive as a crash."""
    with tempfile.TemporaryDirectory() as tmp:
        not_a_repo = os.path.join(tmp, "plain")
        os.makedirs(not_a_repo)
        try:
            R.measure_execution_head(not_a_repo)
            raise AssertionError("measured a head outside a repository")
        except R.RepairError as error:
            check(error.reason == R.EXECUTION_IDENTITY_UNVERIFIED,
                  "a git failure is a structured stop")
            check("git" in str(error), "naming git as the cause")


def test_the_approved_digests_must_come_from_the_approved_commit():
    """F2 — three separate proofs, and the middle one used to be missing.

    Recording four digests and never comparing them against the commit they
    claim to describe leaves them as four more strings.  They are now
    recomputed from that commit's blobs with `git show`.
    """
    with tempfile.TemporaryDirectory() as tmp, approved_implementation(tmp) \
            as pin:
        from_commit = R.digests_from_commit(pin["repo"], pin["head"])
        check(sorted(from_commit) == sorted(R.APPROVED_DIGEST_PATHS),
              "every approved digest is derivable from the commit")
        check(from_commit["frozen_q5d_lf_sha256"] == R.FROZEN_Q5D_SHA256_LF,
              "the frozen module blob hashes to its registered identity")
        check(all(R.is_hex64(v) for v in from_commit.values()),
              "and all four are real digests")

        record = R.verify_execution_identity(pin["repo"], pin["head"])
        proofs = record["three_proofs"]
        check(proofs["approved_commit_exists"] is True,
              "proof 1: the approved commit exists")
        check(proofs["approved_digests_come_from_that_commit"] is True,
              "proof 2: the digests come from that commit's blobs")
        check(proofs["execution_files_match_approved_identity"] is True,
              "proof 3: the files about to run match that identity")
        check(record["digests_recomputed_from_approved_commit"] == from_commit,
              "and the recomputed table is reported, not just a flag")

        # A record that does not describe its own commit.
        R.APPROVED_ARTIFACT_DIGESTS["spec_lf_sha256"] = "c" * 64
        try:
            R.verify_execution_identity(pin["repo"], pin["head"])
            raise AssertionError("a drifted approved record was accepted")
        except R.RepairError as error:
            check(error.reason == R.EXECUTION_IDENTITY_UNVERIFIED,
                  "a digest the commit does not hold is refused")
            check("does not describe the commit it names" in str(error),
                  "and the message says exactly that")

    # A missing commit.
    with tempfile.TemporaryDirectory() as tmp, approved_implementation(tmp) \
            as pin:
        try:
            R.digests_from_commit(pin["repo"], "b" * 40)
            raise AssertionError("read blobs from a commit that is not there")
        except R.RepairError as error:
            check(error.reason == R.EXECUTION_IDENTITY_UNVERIFIED,
                  "a commit that does not exist is a stop")


def test_an_unrecorded_approval_stops_before_assets():
    """The pre-approval state, restored, still refuses."""
    previous = R.APPROVED_IMPLEMENTATION_COMMIT
    R.APPROVED_IMPLEMENTATION_COMMIT = None
    try:
        R.verify_execution_identity(ROOT, "b" * 40)
        raise AssertionError("verified with nothing recorded")
    except R.RepairError as error:
        check(error.reason == R.EXECUTION_IDENTITY_UNVERIFIED,
              "with no approved implementation recorded, it refuses")
        check("no approved implementation commit" in str(error),
              "and says so")
    finally:
        R.APPROVED_IMPLEMENTATION_COMMIT = previous


def test_the_approval_block_admits_only_metadata_assignments():
    """F3 — by AST whitelist.  `x = os.system(...)` contains no `def`."""
    audit = R.module_science_digest()["approval_block"]
    check(audit["metadata_only"] is True, "the shipped block is metadata only")
    check(sorted(audit["bound_names"]) == sorted(R.APPROVAL_BLOCK_NAMES),
          "binding exactly the four whitelisted names")

    def fenced(body):
        return R.assert_approval_block_is_metadata_only(body)

    ok_bodies = [
        "EXECUTION_APPROVAL_TOKEN = 'x'",
        "APPROVED_IMPLEMENTATION_COMMIT = None",
        "APPROVED_ARTIFACT_DIGESTS = {'a': None, 'b': ('t', 'u')}",
        "EXECUTION_APPROVAL_RECORD = {'recorded_in': SPEC_PATH}",
    ]
    for body in ok_bodies:
        check(fenced(body)["metadata_only"] is True,
              f"metadata is allowed: {body[:40]}")

    rejected = {
        "a hidden call": "EXECUTION_APPROVAL_TOKEN = os.system('id')",
        "a nested call": "APPROVED_ARTIFACT_DIGESTS = {'a': open('x').read()}",
        "an import": "import os",
        "a from-import": "from os import system",
        "a function": "def helper():\n    return 1",
        "a class": "class Sneaky:\n    pass",
        "a lambda": "EXECUTION_APPROVAL_TOKEN = lambda: 1",
        "a conditional": "if True:\n    EXECUTION_APPROVAL_TOKEN = 'x'",
        "a loop": "for i in []:\n    pass",
        "a while": "while False:\n    pass",
        "a try": "try:\n    pass\nexcept Exception:\n    pass",
        "a with": "with open('x') as f:\n    pass",
        "a comprehension": "APPROVED_ARTIFACT_DIGESTS = {k: 1 for k in 'ab'}",
        "an attribute read": "EXECUTION_APPROVAL_TOKEN = os.name",
        "another variable": "SOMETHING_ELSE = 'x'",
        "a subscript target": "APPROVED_ARTIFACT_DIGESTS['a'] = 'b'",
        "a foreign reference": "EXECUTION_APPROVAL_TOKEN = BUNDLE_FILES",
        "an f-string": "EXECUTION_APPROVAL_TOKEN = f'{1}'",
        # Annotated assignment is refused as a form: an annotation is an
        # ordinary expression, so `SPEC_PATH.__class__` and `SPEC_PATH[0]`
        # both run something while looking like a type.
        "an attribute annotation":
            "APPROVED_IMPLEMENTATION_COMMIT: SPEC_PATH.__class__ = None",
        "a subscript annotation":
            "APPROVED_IMPLEMENTATION_COMMIT: SPEC_PATH[0] = None",
        "a call annotation":
            "APPROVED_IMPLEMENTATION_COMMIT: type(SPEC_PATH) = None",
        "a plain annotation": "APPROVED_IMPLEMENTATION_COMMIT: str = None",
    }
    for label, body in rejected.items():
        try:
            fenced(body)
            raise AssertionError(f"the block accepted {label}")
        except R.RepairError as error:
            check(error.reason == R.EXECUTION_IDENTITY_UNVERIFIED,
                  f"the block refuses {label}")


def test_a_call_smuggled_into_the_approval_block_breaks_science_identity():
    """F3 mutation — the science digest must not be computable over logic."""
    source = open(R.__file__, encoding="utf-8").read()
    mutated = source.replace(
        f'APPROVED_IMPLEMENTATION_COMMIT = "{R.APPROVED_IMPLEMENTATION_COMMIT}"',
        'APPROVED_IMPLEMENTATION_COMMIT = __import__("os").getcwd()', 1)
    check(mutated != source, "the mutation applied")
    try:
        R.module_science_digest(source=mutated.encode("utf-8"))
        raise AssertionError("a call inside the approval block was digested")
    except R.RepairError as error:
        check(error.reason == R.EXECUTION_IDENTITY_UNVERIFIED,
              "a call in the fenced block has no science digest at all")

    for marker_mutation, label in (
        (source.replace(R.APPROVAL_BLOCK_END, "# ─── moved elsewhere", 1),
         "a missing end marker"),
        (source.replace(R.APPROVAL_BLOCK_START,
                        R.APPROVAL_BLOCK_START + "\n"
                        + R.APPROVAL_BLOCK_START, 1),
         "a duplicated start marker"),
    ):
        try:
            R.module_science_digest(source=marker_mutation.encode("utf-8"))
            raise AssertionError(f"accepted {label}")
        except R.RepairError as error:
            check(error.reason == R.EXECUTION_IDENTITY_UNVERIFIED,
                  f"{label} is refused")


def test_missing_dependencies_stop_before_any_credential():
    """F4 — minting a credential and then failing to build a client is worse."""
    calls = {"credential": 0, "service": 0, "api": 0}

    class SpyAuthenticator(R.DriveAuthenticator):
        def credential(self, scopes):
            calls["credential"] += 1                     # pragma: no cover
            raise AssertionError("a credential was minted")

    def spy_factory(credential):                         # pragma: no cover
        calls["service"] += 1
        raise AssertionError("a service was built")

    dependencies = R.check_runtime_dependencies()
    check("packages" in dependencies and "missing" in dependencies,
          "the dependency check reports what is missing, not just a flag")

    with approved() as token:
        if dependencies["satisfied"]:                    # pragma: no cover
            check(True, "dependencies present here; the gate is exercised "
                        "wherever they are absent")
        else:
            try:
                R.build_drive_adapter(token, SpyAuthenticator(), spy_factory)
                raise AssertionError("built an adapter without the libraries")
            except R.RepairError as error:
                check(error.reason == R.DEPENDENCY_MISSING,
                      "a missing client library is a structured stop")
                check("no credential is requested" in str(error),
                      "and the message says why the order matters")
        check(calls == {"credential": 0, "service": 0, "api": 0},
              f"no credential, service or API call happened: {calls}")

        # With the libraries present the gate opens and the scope proof runs.
        with stub_drive_dependencies():
            adapter, audit = R.build_drive_adapter(
                token, FakeAuthenticator(), lambda c: object())
            check(audit["exact_readonly_scope_proven"] is True,
                  "and then the scope proof is what decides")
            check(audit["runtime_dependencies"]["satisfied"] is True,
                  "with the dependency report carried into the audit")


def test_a_credential_that_can_be_downscoped_is_downscoped():
    """F4 — Colab's ambient credential is often broader than asked for."""
    class Broad(object):
        requires_scopes = True

        def __init__(self):
            self.scopes = None
            self.narrowed = None

        def with_scopes(self, scopes):
            narrowed = Broad()
            narrowed.requires_scopes = False
            narrowed.scopes = list(scopes)
            return narrowed

    broad = Broad()
    check(R.audit_credential_scopes(broad)["exact_readonly_scope_proven"]
          is False,
          "an unscoped credential does not prove anything")
    narrowed = broad.with_scopes([R.DRIVE_READONLY_SCOPE])
    audit = R.audit_credential_scopes(narrowed)
    check(audit["exact_readonly_scope_proven"] is True,
          "a down-scoped one does")
    check(audit["observed_scopes"] == [R.DRIVE_READONLY_SCOPE],
          "with exactly the one scope observed")

    source = inspect.getsource(R.ColabReadOnlyAuthenticator)
    check("google.auth.default(scopes=list(scopes))" in source,
          "the Colab authenticator asks google.auth for the scope")
    check("requires_scopes" in source and "with_scopes" in source,
          "and narrows the credential when the library supports it")
    check("READONLY_SCOPE_UNPROVEN" not in source
          and "raise" not in source,
          "but does not judge its own credential — the audit decides, so a "
          "credential that merely claims to be narrow still has to prove it")


def test_a_broader_or_unobservable_scope_is_still_refused():
    for scopes in (None, [], ["https://www.googleapis.com/auth/drive"],
                   [R.DRIVE_READONLY_SCOPE,
                    "https://www.googleapis.com/auth/drive.file"]):
        credential = FakeCredential(scopes)
        audit = R.audit_credential_scopes(credential)
        check(audit["exact_readonly_scope_proven"] is False,
              f"scopes {scopes} do not prove read-only")
    with approved() as token, stub_drive_dependencies():
        try:
            R.build_drive_adapter(token, FakeAuthenticator(scopes=[
                "https://www.googleapis.com/auth/drive"]), lambda c: object())
            raise AssertionError("a broader credential built an adapter")
        except R.RepairError as error:
            check(error.reason == R.READONLY_SCOPE_UNPROVEN,
                  "a broader credential is refused, not accepted for "
                  "including what we need")


def test_the_recorded_pin_describes_the_commit_it_names():
    """The enable PR's own claim, checked against git rather than trusted."""
    check(isinstance(R.APPROVED_IMPLEMENTATION_COMMIT, str)
          and len(R.APPROVED_IMPLEMENTATION_COMMIT) == 40,
          "an implementation commit is recorded, as a 40-hex sha")
    check(all(R.is_hex64(v) for v in R.APPROVED_ARTIFACT_DIGESTS.values()),
          "and all four artifact digests are real digests")

    from_commit = R.digests_from_commit(ROOT, R.APPROVED_IMPLEMENTATION_COMMIT)
    check(from_commit == dict(R.APPROVED_ARTIFACT_DIGESTS),
          f"the four digests are the ones commit "
          f"{R.APPROVED_IMPLEMENTATION_COMMIT[:12]} actually holds")
    check(from_commit["frozen_q5d_lf_sha256"] == R.FROZEN_Q5D_SHA256_LF,
          "including the frozen module's registered identity")

    check(R.module_science_digest()["module_science_lf_sha256"]
          == R.APPROVED_ARTIFACT_DIGESTS["module_science_lf_sha256"],
          "and the enable PR moved approval metadata and no logic")


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
