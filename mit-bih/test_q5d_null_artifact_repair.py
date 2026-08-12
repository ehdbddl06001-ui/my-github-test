"""Synthetic and contract tests for EXP-2026-009, the null artifact repair.

Every fixture is invented.  Shard payloads are built from the frozen module's
own `shard_digest()` over `J` values this file makes up, so no test can pass by
recognising a real number, and no test opens a registered artifact: the guard
is closed for the whole file except where a test deliberately opens it to
exercise the route, and even then only against temp directories.

Run: `python mit-bih/test_q5d_null_artifact_repair.py`
"""

from __future__ import annotations

import contextlib
import hashlib
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
FAMILIES = sorted(BJ.CONTROL_FAMILIES)


def check(condition: bool, label: str) -> None:
    global PASSED
    if not condition:
        raise AssertionError(label)
    PASSED += 1


# ─────────────────────────────────────────────────────────────────────────────
# Fixtures
# ─────────────────────────────────────────────────────────────────────────────
def _identity(code_sha256: str = "c" * 64, input_digest: str = "d" * 64,
              split: str = "DS1") -> dict:
    """The four identity fields a manifest carries."""
    return {"split": split, "code_sha256": code_sha256,
            "input_digest": input_digest,
            "rule_fingerprint": BJ.rule_fingerprint()}


def _j_value(family: str, replicate: int) -> float:
    """A distinct, ordered value per (family, replicate).

    Deliberately arranged so the family maximum is not always the same family
    — a `j_null_max` check that only ever sees one winner would not notice a
    reconstruction that took the wrong one.
    """
    base = 0.1 + 0.001 * replicate
    offset = {"wrong_record": 0.0, "order_shuffle": 0.02,
              "circular_shift": 0.04}[family]
    if replicate % 3 == 0:
        offset = 0.06 - offset
    return round(base + offset, 12)


def _shard_payload(identity: dict, start: int, end: int,
                   families=None, maxima=None) -> dict:
    """One shard, digested by the frozen module's own function."""
    values = {f: [_j_value(f, b) for b in range(start, end)]
              for f in FAMILIES}
    if families is not None:
        values.update(families)
    payload = {
        "null_runner_version": BJ.NULL_RUNNER_VERSION,
        "split": identity["split"], "families": list(BJ.CONTROL_FAMILIES),
        "master_seed": BJ.MASTER_SEED,
        "rule_fingerprint": identity["rule_fingerprint"],
        "code_sha256": identity["code_sha256"],
        "input_digest": identity["input_digest"],
        "replicate_start": start, "replicate_end": end,
        "j": {f: list(values[f]) for f in FAMILIES},
        "j_null_max": list(maxima) if maxima is not None else [
            max(values[f][k] for f in FAMILIES) for k in range(end - start)],
        "worker_count": 1, "git_commit": None,
    }
    payload["digest"] = BJ.shard_digest(payload)
    return payload


def _write_shards(directory: str, identity: dict, total: int = TOTAL,
                  size: int = SHARD_SIZE, skip=(), payloads=None) -> None:
    os.makedirs(directory, exist_ok=True)
    for start in range(0, total, size):
        end = min(start + size, total)
        if (start, end) in skip:
            continue
        payload = (payloads or {}).get((start, end)) \
            or _shard_payload(identity, start, end)
        with open(os.path.join(directory,
                               BJ.shard_filename(start, end)),
                  "w", encoding="utf-8") as handle:
            json.dump(payload, handle, sort_keys=True, ensure_ascii=False)


def _expected_arrays(total: int = TOTAL) -> dict:
    arrays = {f: [_j_value(f, b) for b in range(total)] for f in FAMILIES}
    arrays["j_null_max"] = [max(arrays[f][b] for f in FAMILIES)
                            for b in range(total)]
    return arrays


def _write_source_bundle(directory: str, identity: dict,
                         total: int = TOTAL, summary=None,
                         omit=(), extra=()) -> dict:
    """The eleven files.  Content is filler except manifest and null_summary."""
    os.makedirs(directory, exist_ok=True)
    arrays = _expected_arrays(total)
    manifest = dict(identity)
    manifest.update({"experiment_id": "EXP-2026-007", "stage": "DS1_GATE"})
    if summary is None:
        summary = {"replicates": total, "families": list(BJ.CONTROL_FAMILIES),
                   "master_seed": BJ.MASTER_SEED,
                   "rule_fingerprint": identity["rule_fingerprint"],
                   "j_null_max": list(arrays["j_null_max"])}
    for name in R.SOURCE_BUNDLE_FILES:
        if name in omit:
            continue
        path = os.path.join(directory, name)
        if name == R.MANIFEST_FILE:
            body = json.dumps(manifest, sort_keys=True).encode("utf-8")
        elif name == R.SUMMARY_FILE:
            body = json.dumps(summary, sort_keys=True).encode("utf-8")
        else:
            body = f"filler for {name}\n".encode("utf-8")
        with open(path, "wb") as handle:
            handle.write(body)
    for name in extra:
        with open(os.path.join(directory, name), "wb") as handle:
            handle.write(b"unexpected\n")
    return {"manifest": manifest, "summary": summary, "arrays": arrays}


@contextlib.contextmanager
def approved():
    """Open the terminal guard for the length of one test, then close it.

    The module ships with `granted: False`, and it must still be False when
    this file finishes — a test that left execution enabled would hand the
    next reader a module whose guard is open for reasons nothing records.
    """
    R.EXECUTION_APPROVAL_RECORD["granted"] = True
    try:
        yield R.EXECUTION_APPROVAL_TOKEN
    finally:
        R.EXECUTION_APPROVAL_RECORD["granted"] = False


# ─────────────────────────────────────────────────────────────────────────────
# The guard and the frozen module
# ─────────────────────────────────────────────────────────────────────────────
def test_the_module_ships_unapproved_and_refuses_everything():
    """Nothing here is approved for execution, and the code says so."""
    check(R.EXECUTION_APPROVAL_RECORD["granted"] is False,
          "the shipped approval record is closed")
    check(R.EXECUTION_APPROVAL_RECORD["granted_on"] is None
          and R.EXECUTION_APPROVAL_RECORD["granted_by"] is None,
          "and records no approver, because there is none")
    check("not approved for execution" in R.design_card()
          or "execution approved: False" in R.design_card(),
          "the design card says so out loud")

    with tempfile.TemporaryDirectory() as tmp:
        for call in (
            lambda: R.qualify_shards(tmp, _identity(),
                                     R.EXECUTION_APPROVAL_TOKEN),
            lambda: R.inspect_source_bundle(tmp, R.EXECUTION_APPROVAL_TOKEN),
            lambda: R.assemble_corrective_bundle(
                tmp, os.path.join(tmp, "out"), b"", R.EXECUTION_APPROVAL_TOKEN),
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
    """Permission before capability: the token is checked first."""
    with tempfile.TemporaryDirectory() as tmp, approved():
        for token in (None, "", "q5e-prep-p1-p2-read-only-execution-approved-by-user"):
            try:
                R.qualify_shards(tmp, _identity(), token)
                raise AssertionError(f"accepted {token!r}")
            except R.RepairNotApprovedError:
                check(True, f"{token!r} is refused")
        check(R.EXECUTION_APPROVAL_TOKEN
              != "q5e-prep-p1-p2-read-only-execution-approved-by-user",
              "and the PREP's token is not this module's token")


def test_the_frozen_q5d_module_is_the_registered_one():
    """The shards were produced by the registered version; so must the reader."""
    check(R.frozen_q5d_sha256() == R.FROZEN_Q5D_SHA256,
          "the imported frozen module hashes to the registered value")
    check(R.assert_frozen_q5d_unchanged() == R.FROZEN_Q5D_SHA256,
          "and the assertion returns it")
    check(R.FROZEN_Q5D_SHA256.startswith("6b098c67df3c"),
          "which is the hash embedded in the shard folder's name")

    original = R.FROZEN_Q5D_SHA256
    R.FROZEN_Q5D_SHA256 = "0" * 64
    try:
        R.assert_frozen_q5d_unchanged()
        raise AssertionError("a moved module was accepted")
    except R.RepairError as error:
        check(error.reason == R.FROZEN_MODULE_MOVED,
              "a module that is not the registered one is a stop")
    finally:
        R.FROZEN_Q5D_SHA256 = original


def test_the_repair_never_writes_to_the_frozen_module_or_its_contract():
    """The twelve-file contract is read, never edited."""
    source = open(R.__file__, encoding="utf-8").read()
    check("BJ.BUNDLE_FILES" in source,
          "BUNDLE_FILES is read from the frozen module")
    for forbidden in ("BJ.BUNDLE_FILES =", "BJ.BUNDLE_FILES=",
                      "setattr(BJ", "BJ.write_null_shard",
                      "BJ.compute_null_shard", "BJ.run_null_shards"):
        check(forbidden not in source,
              f"the repair never does {forbidden!r}")
    check(len(R.BUNDLE_FILES) == 12, "the contract is still twelve")
    check(len(R.SOURCE_BUNDLE_FILES) == 11,
          "and the source is those twelve minus the one being rebuilt")
    check(R.MISSING_ARTIFACT not in R.SOURCE_BUNDLE_FILES,
          "which is negative_control_null.npz")
    check(set(R.SOURCE_BUNDLE_FILES) | {R.MISSING_ARTIFACT}
          == set(R.BUNDLE_FILES),
          "and the two sets differ by exactly that name")


# ─────────────────────────────────────────────────────────────────────────────
# Identity and the identity-only context
# ─────────────────────────────────────────────────────────────────────────────
def test_the_identity_anchor_is_the_manifest_not_the_shards():
    """A shard set that agrees with itself is not evidence of anything."""
    identity = _identity()
    check(R.identity_from_manifest(identity) == identity,
          "the four fields come out of the manifest")
    for field in R.IDENTITY_FIELDS:
        broken = dict(identity)
        broken.pop(field)
        try:
            R.identity_from_manifest(broken)
            raise AssertionError(f"accepted a manifest with no {field}")
        except R.RepairError as error:
            check(error.reason == R.INPUT_UNQUALIFIED,
                  f"a manifest with no {field} cannot anchor anything")


def test_finalisation_never_reads_the_join_inputs():
    """The invariant that makes an identity-only context legitimate.

    If anything on the finalisation path reached for a record, the mapping
    below would raise rather than quietly returning nothing — so this passing
    is the evidence, not the docstring.
    """
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

    shards = {(s, min(s + SHARD_SIZE, TOTAL)):
              _shard_payload(identity, s, min(s + SHARD_SIZE, TOTAL))
              for s in range(0, TOTAL, SHARD_SIZE)}
    families = BJ.finalize_null_shards(shards, context, total=TOTAL)
    check(sorted(families) == FAMILIES,
          "the frozen finaliser assembles all three families from identity "
          "alone")
    check(all(len(families[f]) == TOTAL for f in FAMILIES),
          "with every replicate present")


def test_a_moved_rule_fingerprint_stops_the_context():
    """A null may not be finalised under a rule other than its own."""
    identity = _identity()
    identity["rule_fingerprint"] = "f" * 64
    try:
        R.identity_only_context(identity)
        raise AssertionError("a foreign rule fingerprint was accepted")
    except R.RepairError as error:
        check(error.reason == R.INPUT_UNQUALIFIED,
              "the live fingerprint must equal the bundle's")


# ─────────────────────────────────────────────────────────────────────────────
# Shard qualification
# ─────────────────────────────────────────────────────────────────────────────
def test_a_complete_consistent_shard_set_qualifies():
    identity = _identity()
    with tempfile.TemporaryDirectory() as tmp, approved() as token:
        shard_dir = os.path.join(tmp, "shards")
        _write_shards(shard_dir, identity)
        out = R.qualify_shards(shard_dir, identity, token, total=TOTAL)
        report = out["report"]
        check(report["qualified"] is True, "a clean set qualifies")
        check(report["shard_count"] == TOTAL // SHARD_SIZE,
              "every shard was read")
        check(report["coverage"]["ok"] is True
              and report["coverage"]["covered"] == TOTAL,
              "coverage is exactly 0..n-1")
        check(report["coverage"]["missing_count"] == 0
              and report["coverage"]["overlap_count"] == 0,
              "no gap and no overlap")
        check(report["identity_anchor"] == "bundle manifest.json",
              "and the report says what it was checked against")
        check(len(report["per_shard"]) == TOTAL // SHARD_SIZE
              and all(row["digest_verified"] for row in report["per_shard"]),
              "each shard's own digest was verified")


def test_a_gap_a_duplicate_and_an_overlap_are_all_unqualified():
    identity = _identity()
    cases = {
        "gap": dict(skip=((5, 10),)),
        "overlap": dict(payloads={(10, 15): None}),
    }
    with tempfile.TemporaryDirectory() as tmp, approved() as token:
        shard_dir = os.path.join(tmp, "gap")
        _write_shards(shard_dir, identity, skip=((5, 10),))
        try:
            R.qualify_shards(shard_dir, identity, token, total=TOTAL)
            raise AssertionError("a gap qualified")
        except R.RepairError as error:
            check(error.reason == R.INPUT_UNQUALIFIED,
                  "a missing replicate range is unqualified")

        overlapping = os.path.join(tmp, "overlap")
        _write_shards(overlapping, identity)
        extra = _shard_payload(identity, 3, 8)
        with open(os.path.join(overlapping, BJ.shard_filename(3, 8)),
                  "w", encoding="utf-8") as handle:
            json.dump(extra, handle, sort_keys=True)
        try:
            R.qualify_shards(overlapping, identity, token, total=TOTAL)
            raise AssertionError("an overlap qualified")
        except R.RepairError as error:
            check(error.reason == R.INPUT_UNQUALIFIED,
                  "an overlapping replicate is unqualified")
    check(sorted(cases) == ["gap", "overlap"], "both shapes were exercised")


def test_an_edited_shard_fails_its_own_digest():
    """The frozen reader catches it; the repair does not re-derive the digest."""
    identity = _identity()
    with tempfile.TemporaryDirectory() as tmp, approved() as token:
        shard_dir = os.path.join(tmp, "shards")
        _write_shards(shard_dir, identity)
        path = os.path.join(shard_dir, BJ.shard_filename(0, SHARD_SIZE))
        payload = json.load(open(path, encoding="utf-8"))
        payload["j"]["wrong_record"][0] += 0.5          # digest not updated
        with open(path, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, sort_keys=True)
        try:
            R.qualify_shards(shard_dir, identity, token, total=TOTAL)
            raise AssertionError("an edited shard qualified")
        except R.RepairError as error:
            check(error.reason == R.INPUT_UNQUALIFIED,
                  "an edited shard is unqualified")


def test_a_foreign_shard_set_is_refused_by_identity():
    """Internally consistent is not the same as belonging to this run."""
    ours, theirs = _identity(), _identity(code_sha256="e" * 64)
    with tempfile.TemporaryDirectory() as tmp, approved() as token:
        shard_dir = os.path.join(tmp, "shards")
        _write_shards(shard_dir, theirs)
        try:
            R.qualify_shards(shard_dir, ours, token, total=TOTAL)
            raise AssertionError("another run's shards qualified")
        except R.RepairError as error:
            check(error.reason == R.INPUT_UNQUALIFIED,
                  "a shard set from another code_sha256 is refused")
            check("code_sha256" in str(error),
                  "and the report names the field that disagreed")


def test_a_shard_whose_max_is_wrong_is_refused():
    """`j_null_max` inside a shard must be the family maximum."""
    identity = _identity()
    with tempfile.TemporaryDirectory() as tmp, approved() as token:
        shard_dir = os.path.join(tmp, "shards")
        wrong = _shard_payload(identity, 0, SHARD_SIZE,
                               maxima=[0.0] * SHARD_SIZE)
        _write_shards(shard_dir, identity,
                      payloads={(0, SHARD_SIZE): wrong})
        try:
            R.qualify_shards(shard_dir, identity, token, total=TOTAL)
            raise AssertionError("a wrong maximum qualified")
        except R.RepairError as error:
            check(error.reason == R.INPUT_UNQUALIFIED,
                  "a shard whose maximum is not the family maximum is refused")


# ─────────────────────────────────────────────────────────────────────────────
# Reconstruction and the cross-check against null_summary.json
# ─────────────────────────────────────────────────────────────────────────────
def test_reconstruction_returns_the_four_arrays_in_canonical_order():
    identity = _identity()
    shards = {(s, min(s + SHARD_SIZE, TOTAL)):
              _shard_payload(identity, s, min(s + SHARD_SIZE, TOTAL))
              for s in range(0, TOTAL, SHARD_SIZE)}
    arrays = R.reconstruct_arrays(shards, R.identity_only_context(identity),
                                  total=TOTAL)
    expected = _expected_arrays()
    check(sorted(arrays) == sorted(R.NPZ_ARRAYS),
          "exactly the four contracted names")
    for name in R.NPZ_ARRAYS:
        check(arrays[name] == expected[name],
              f"{name} is assembled in replicate order")
    check(all(arrays["j_null_max"][b]
              == max(arrays[f][b] for f in FAMILIES)
              for b in range(TOTAL)),
          "and j_null_max is the per-replicate family maximum")
    winners = {max(FAMILIES, key=lambda f: arrays[f][b]) for b in range(TOTAL)}
    check(len(winners) > 1,
          "the fixture is not degenerate: the winning family varies")


def test_the_summary_cross_check_is_exact_and_locates_the_first_difference():
    identity = _identity()
    arrays = _expected_arrays()
    good = {"j_null_max": list(arrays["j_null_max"])}
    agreement = R.compare_to_summary(arrays, good)
    check(agreement["identical"] is True, "an identical vector agrees")
    check(agreement["first_difference"] is None, "with nothing to report")

    drifted = {"j_null_max": list(arrays["j_null_max"])}
    drifted["j_null_max"][7] += 1e-15                    # a float64 tick
    off = R.compare_to_summary(arrays, drifted)
    check(off["identical"] is False,
          "a one-tick difference is a disagreement, not a rounding matter")
    check(off["first_difference"]["index"] == 7,
          "and the first differing index is reported")

    short = {"j_null_max": list(arrays["j_null_max"])[:-1]}
    check(R.compare_to_summary(arrays, short)["identical"] is False,
          "a truncated summary is a disagreement too")
    check(R.compare_to_summary(arrays, {})["identical"] is False,
          "and so is a summary with no vector at all")


# ─────────────────────────────────────────────────────────────────────────────
# The NPZ contract
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


def test_the_npz_holds_exactly_the_four_arrays():
    arrays = _expected_arrays()
    blob = R.npz_bytes(arrays)
    members = R.read_npz_bytes(blob)
    check(sorted(members) == sorted(R.NPZ_ARRAYS),
          "four members, named as the contract fixes")
    with zipfile.ZipFile(__import__("io").BytesIO(blob)) as archive:
        check(all(i.compress_type == zipfile.ZIP_STORED
                  for i in archive.infolist()),
              "stored, not deflated")
        check({i.date_time for i in archive.infolist()} == {R.ZIP_TIMESTAMP},
              "with a pinned timestamp, so the bytes are deterministic")
    check(R.npz_bytes(arrays) == blob,
          "the same arrays produce byte-identical output twice")

    for bad in ({k: v for k, v in arrays.items() if k != "j_null_max"},
                dict(arrays, extra=[0.0])):
        try:
            R.npz_bytes(bad)
            raise AssertionError("an off-contract array set was serialised")
        except R.RepairError as error:
            check(error.reason == R.NPZ_CONTRACT_FAILED,
                  "the writer refuses anything but the four")


def test_the_npz_contract_is_verified_by_reading_the_bytes_back():
    arrays = _expected_arrays()
    blob = R.npz_bytes(arrays)
    verdict = R.verify_npz_contract(blob, arrays["j_null_max"], total=TOTAL)
    check(verdict["ok"] is True, f"a correct NPZ passes: {verdict['problems']}")
    check(verdict["sha256"] == hashlib.sha256(blob).hexdigest(),
          "the digest is of the produced bytes")
    for name in R.NPZ_ARRAYS:
        entry = verdict["arrays"][name]
        check(entry["dtype"] == "<f8" and entry["shape"] == [TOTAL]
              and entry["finite"] is True,
              f"{name}: float64, right shape, finite")
    check(verdict["arrays"]["j_null_max_is_family_max"] is True,
          "and the internal maximum relation holds")


def test_the_npz_contract_catches_every_way_it_can_be_wrong():
    arrays = _expected_arrays()

    wrong_shape = dict(arrays)
    wrong_shape["wrong_record"] = arrays["wrong_record"][:-1]
    check(not R.verify_npz_contract(R.npz_bytes(wrong_shape),
                                    total=TOTAL)["ok"],
          "a short array fails the shape clause")

    for bad_value in (float("nan"), float("inf"), float("-inf")):
        broken = {k: list(v) for k, v in arrays.items()}
        broken["order_shuffle"][2] = bad_value
        broken["j_null_max"] = [max(broken[f][b] for f in FAMILIES)
                                for b in range(TOTAL)]
        verdict = R.verify_npz_contract(R.npz_bytes(broken), total=TOTAL)
        check(not verdict["ok"] and any("non-finite" in str(p)
                                        for p in verdict["problems"]),
              f"{bad_value} is refused")

    detached = {k: list(v) for k, v in arrays.items()}
    detached["j_null_max"] = [0.0] * TOTAL
    verdict = R.verify_npz_contract(R.npz_bytes(detached), total=TOTAL)
    check(not verdict["ok"]
          and any("family maximum" in str(p) for p in verdict["problems"]),
          "a j_null_max that is not the family maximum is refused")

    verdict = R.verify_npz_contract(
        R.npz_bytes(arrays),
        [v + 1e-15 for v in arrays["j_null_max"]], total=TOTAL)
    check(not verdict["ok"],
          "and disagreement with the expected vector is refused")


def test_a_pickled_member_cannot_be_read_at_all():
    """`allow_pickle=False` exists to reject object arrays; so does this reader."""
    import io
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


def test_numpy_can_load_the_bytes_when_numpy_is_present():
    """Measured where possible rather than asserted everywhere.

    This container has no numpy, so the claim "numpy reads this with
    `allow_pickle=False`" would otherwise be a promise.  Where numpy exists —
    Colab, and any machine a repair would actually run on — it is checked.
    """
    arrays = _expected_arrays()
    blob = R.npz_bytes(arrays)
    try:
        import numpy                                     # noqa: F401
    except ImportError:
        check(R.read_npz_bytes(blob).keys() is not None,
              "no numpy here: the independent reader stands in, and the "
              "numpy cross-check runs wherever numpy exists")
        return
    import io                                            # pragma: no cover
    with numpy.load(io.BytesIO(blob), allow_pickle=False) as loaded:
        check(sorted(loaded.files) == sorted(R.NPZ_ARRAYS),
              "numpy sees the four arrays")
        for name in R.NPZ_ARRAYS:
            check(str(loaded[name].dtype) == "float64",
                  f"numpy reads {name} as float64")
            check(loaded[name].tolist() == arrays[name],
                  f"and every {name} value matches exactly")


# ─────────────────────────────────────────────────────────────────────────────
# The corrective bundle
# ─────────────────────────────────────────────────────────────────────────────
def test_the_source_bundle_must_be_exactly_the_eleven():
    identity = _identity()
    with tempfile.TemporaryDirectory() as tmp, approved() as token:
        good = os.path.join(tmp, "good")
        _write_source_bundle(good, identity)
        inventory = R.inspect_source_bundle(good, token)
        check(inventory["count"] == 11, "eleven files inventoried")
        check([row["name"] for row in inventory["files"]]
              == list(R.SOURCE_BUNDLE_FILES),
              "in the contract's order")
        check(all(len(row["sha256"]) == 64 for row in inventory["files"]),
              "each with its digest")

        short = os.path.join(tmp, "short")
        _write_source_bundle(short, identity, omit=("log.txt",))
        try:
            R.inspect_source_bundle(short, token)
            raise AssertionError("a ten-file source was accepted")
        except R.RepairError as error:
            check(error.reason == R.SOURCE_BUNDLE_UNEXPECTED,
                  "a missing file is a stop")

        wide = os.path.join(tmp, "wide")
        _write_source_bundle(wide, identity, extra=("SUPERSEDED.json",))
        try:
            R.inspect_source_bundle(wide, token)
            raise AssertionError("an unexpected file was accepted")
        except R.RepairError as error:
            check(error.reason == R.SOURCE_BUNDLE_UNEXPECTED,
                  "and so is an unexpected one")


def test_the_corrective_bundle_is_twelve_and_byte_identical():
    identity = _identity()
    with tempfile.TemporaryDirectory() as tmp, approved() as token:
        source = os.path.join(tmp, "source")
        built = _write_source_bundle(source, identity)
        target = os.path.join(tmp, "corrective")
        blob = R.npz_bytes(built["arrays"])

        before = {name: hashlib.sha256(
            open(os.path.join(source, name), "rb").read()).hexdigest()
            for name in sorted(os.listdir(source))}

        assembled = R.assemble_corrective_bundle(source, target, blob, token)
        check(assembled["listing"] == sorted(R.BUNDLE_FILES),
              "the folder holds exactly the twelve")
        check(assembled["missing"] == [] and assembled["unexpected"] == [],
              "nothing missing, nothing extra")
        check(all(row["byte_identical"] for row in assembled["files"]
                  if row["name"] != R.MISSING_ARTIFACT),
              "every copied file is byte-identical")

        after = {name: hashlib.sha256(
            open(os.path.join(source, name), "rb").read()).hexdigest()
            for name in sorted(os.listdir(source))}
        check(after == before,
              "and the source bundle is untouched, byte for byte")
        check(sorted(os.listdir(source)) == sorted(R.SOURCE_BUNDLE_FILES),
              "with nothing added to it")

        inventory = R.inspect_source_bundle(source, token)
        verdict = R.verify_corrective_bundle(
            target, inventory, hashlib.sha256(blob).hexdigest())
        check(verdict["ok"] is True, f"and it verifies: {verdict['problems']}")
        check(verdict["observed"][R.MISSING_ARTIFACT]
              == hashlib.sha256(blob).hexdigest(),
              "the NPZ landed with the digest that was verified")


def test_an_existing_target_is_never_written_over():
    identity = _identity()
    with tempfile.TemporaryDirectory() as tmp, approved() as token:
        source = os.path.join(tmp, "source")
        built = _write_source_bundle(source, identity)
        target = os.path.join(tmp, "corrective")
        os.makedirs(target)
        with open(os.path.join(target, "precious.txt"), "w",
                  encoding="utf-8") as handle:
            handle.write("keep me")
        try:
            R.assemble_corrective_bundle(source, target,
                                         R.npz_bytes(built["arrays"]), token)
            raise AssertionError("wrote into an existing directory")
        except R.RepairError as error:
            check(error.reason == R.TARGET_EXISTS,
                  "an existing target name is a stop")
        check(sorted(os.listdir(target)) == ["precious.txt"],
              "and what was there is still there")


def test_the_verifier_reopens_the_files_rather_than_trusting_the_writer():
    identity = _identity()
    with tempfile.TemporaryDirectory() as tmp, approved() as token:
        source = os.path.join(tmp, "source")
        built = _write_source_bundle(source, identity)
        target = os.path.join(tmp, "corrective")
        blob = R.npz_bytes(built["arrays"])
        R.assemble_corrective_bundle(source, target, blob, token)
        inventory = R.inspect_source_bundle(source, token)

        with open(os.path.join(target, "summary.md"), "ab") as handle:
            handle.write(b"edited after the fact\n")
        verdict = R.verify_corrective_bundle(
            target, inventory, hashlib.sha256(blob).hexdigest())
        check(verdict["ok"] is False, "post-hoc editing is caught")
        check(any("summary.md" in str(p) for p in verdict["problems"]),
              "and the edited file is named")


# ─────────────────────────────────────────────────────────────────────────────
# The whole route
# ─────────────────────────────────────────────────────────────────────────────
def test_the_route_completes_on_a_clean_synthetic_repair():
    identity = _identity()
    with tempfile.TemporaryDirectory() as tmp, approved() as token:
        shard_dir = os.path.join(tmp, "shards")
        source = os.path.join(tmp, "source")
        target = os.path.join(tmp, "corrective")
        _write_shards(shard_dir, identity)
        _write_source_bundle(source, identity)

        decision = R.run_repair(shard_dir, source, target, token, total=TOTAL)
        check(decision["status"] == R.REPAIR_COMPLETE, "the route completes")
        check(decision["first_stopping_reason"] is None, "with no stop")
        check(decision["qualification"]["qualified"] is True,
              "the shards qualified")
        check(decision["summary_agreement"]["identical"] is True,
              "the summary agreed exactly")
        check(decision["npz"]["ok"] is True, "the NPZ met its contract")
        check(decision["verification"]["ok"] is True,
              "and the finished folder verified")
        for flag in ("training_performed", "join_rerun", "null_recomputed",
                     "ds2_outcome_opened", "v10_probability_opened",
                     "registered_anything"):
            check(decision[flag] is False, f"{flag} is false")
        check(sorted(os.listdir(target)) == sorted(R.BUNDLE_FILES),
              "twelve files on disk")

        report = R.report_markdown(decision)
        check(R.REPAIR_COMPLETE in report and decision["npz"]["sha256"] in report,
              "the report carries the status and the NPZ digest")
        check("No J value was computed" in report,
              "and says plainly that nothing scientific happened")


def test_a_disagreeing_summary_stops_before_anything_is_written():
    """The order is the safety: nothing exists on disk when a run stops."""
    identity = _identity()
    with tempfile.TemporaryDirectory() as tmp, approved() as token:
        shard_dir = os.path.join(tmp, "shards")
        source = os.path.join(tmp, "source")
        target = os.path.join(tmp, "corrective")
        _write_shards(shard_dir, identity)
        arrays = _expected_arrays()
        drifted = list(arrays["j_null_max"])
        drifted[3] += 1e-15
        _write_source_bundle(source, identity, summary={
            "replicates": TOTAL, "rule_fingerprint": BJ.rule_fingerprint(),
            "j_null_max": drifted})
        try:
            R.run_repair(shard_dir, source, target, token, total=TOTAL)
            raise AssertionError("published despite a disagreeing summary")
        except R.RepairError as error:
            check(error.reason == R.SUMMARY_DISAGREES,
                  "a summary that disagrees is a stop")
        check(not os.path.exists(target),
              "and no corrective folder was created")


def test_an_unqualified_input_stops_before_anything_is_written():
    identity = _identity()
    with tempfile.TemporaryDirectory() as tmp, approved() as token:
        shard_dir = os.path.join(tmp, "shards")
        source = os.path.join(tmp, "source")
        target = os.path.join(tmp, "corrective")
        _write_shards(shard_dir, identity, skip=((15, 20),))
        _write_source_bundle(source, identity)
        try:
            R.run_repair(shard_dir, source, target, token, total=TOTAL)
            raise AssertionError("published from an incomplete null")
        except R.RepairError as error:
            check(error.reason == R.INPUT_UNQUALIFIED,
                  "an incomplete null is REPAIR_INPUT_UNQUALIFIED")
        check(not os.path.exists(target), "and nothing was written")


def test_every_stop_reason_is_reachable_and_named():
    """A stop nobody can reach is decoration."""
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
          "and completion is not a stop reason")


# ─────────────────────────────────────────────────────────────────────────────
# Contract with the notebook and the spec
# ─────────────────────────────────────────────────────────────────────────────
NOTEBOOK = os.path.join(ROOT, "notebooks",
                        "quest57_q5d_null_artifact_repair.ipynb")


def test_the_notebook_is_committed_unexecuted():
    """A template with saved output invites a reader to mistake it for a result."""
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


def test_the_notebook_holds_no_approval_of_its_own():
    """The guard is in the module; a notebook must not be able to open it."""
    nb = json.load(open(NOTEBOOK, encoding="utf-8"))
    body = "\n".join("".join(c["source"]) for c in nb["cells"]
                     if c["cell_type"] == "code")
    check("EXECUTION_APPROVAL_RECORD['granted'] = True" not in body
          and 'EXECUTION_APPROVAL_RECORD["granted"] = True' not in body,
          "the notebook never flips the approval record")
    check(R.EXECUTION_APPROVAL_TOKEN not in body,
          "and does not carry the token as a literal")


def test_the_spec_fixes_the_contract_this_module_implements():
    """The NPZ contract is in the spec, and the module matches it."""
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
    check(str(R.N_REPLICATES) == "10000",
          "and production is the registered 10,000 replicates")


def test_nothing_in_this_file_left_the_guard_open():
    """The last word: the module is as closed as it shipped."""
    check(R.EXECUTION_APPROVAL_RECORD["granted"] is False,
          "execution is still not approved")


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
