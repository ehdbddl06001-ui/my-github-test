"""EXP-2026-009 — reconstruct `negative_control_null.npz` from existing shards.

A **packaging repair**, not an experiment.  It computes no `J` value, re-runs
no replicate, and answers no scientific question: every number it emits already
exists in artifacts written on 2026-08-11.  See
`experiments/specs/EXP-2026-009-q5d-null-artifact-repair.md`.

Why it exists: Q5-E PREP P2 found eleven files where `BUNDLE_FILES` names
twelve, and Codex judged that `P2_PRODUCER_ARTIFACT_OMISSION` — a producer
output-packaging defect, not a stale contract and not a lost measurement.  The
per-family values survive in the 100 null shards and `j_null_max` survives
inlined in `null_summary.json`; what is missing is a file.

**Nothing here is approved for execution.**  `EXECUTION_APPROVAL_RECORD` says
`granted: False`, so `_terminal_execution_guard()` refuses, and it sits above
every read of a shard, every byte of NPZ and every directory creation.  A
stray import reaches nothing.

The frozen Q5-D module is imported **read-only** and its SHA-256 is asserted
before anything else happens; this module never writes to it, and never uses
any of its writers.
"""

from __future__ import annotations

import hashlib
import json
import os
import struct
import zipfile
from typing import Dict, Iterable, List, Mapping, Optional, Sequence, Tuple

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in os.sys.path:                              # pragma: no cover
    os.sys.path.insert(0, HERE)

import q5d_order_preserving_beat_join as BJ              # noqa: E402

EXPERIMENT_ID = "EXP-2026-009"
SUBSTAGE = "Q5D_NULL_ARTIFACT_REPAIR"
RUN_SLUG = "EXP-2026-009_q5d_null_artifact_repair"
MODULE_VERSION = 1
SPEC_PATH = "experiments/specs/EXP-2026-009-q5d-null-artifact-repair.md"
ORIGINATING_DECISION = ("experiments/specs/"
                        "EXP-2026-008-q5e-prep-p1-p2-execution-contract.md")

# ─────────────────────────────────────────────────────────────────────────────
# Approval.  Its own token: approving this repair is not approving the Q5-E
# PREP, the Q5-E audit, or a P1/P2 re-run, and none of those approves this.
# ─────────────────────────────────────────────────────────────────────────────
EXECUTION_APPROVAL_TOKEN = "q5d-null-artifact-repair-execution-approved-by-user"

#: Closed.  The record is written down rather than implied by an absent check:
#: a deleted guard reads identically whether an approval happened or someone
#: removed an inconvenience.  Flipping `granted` to True, with the rest filled
#: in, is the whole of what an execution-approval PR does here.
EXECUTION_APPROVAL_RECORD: Dict[str, object] = {
    "granted": False,
    "granted_on": None,
    "granted_by": None,
    "kind": ("reconstruct negative_control_null.npz from the existing "
             "EXP-2026-007 null shards and assemble a new corrective bundle "
             "folder"),
    "would_approve": (
        "reading the 100 existing null shards, read-only",
        "reading the existing canonical Q5-D bundle's eleven files, read-only",
        "writing one new corrective bundle folder containing exactly the "
        "twelve BUNDLE_FILES names",
        "saving the notebook with its outputs as the external record",
    ),
    "not_approved": (
        "re-running the beat join or any null replicate",
        "modifying, deleting, overwriting or moving the existing bundle",
        "modifying, deleting or overwriting any existing null shard",
        "editing q5d_order_preserving_beat_join.py or BUNDLE_FILES",
        "reducing the twelve-file contract to eleven",
        "writing anything into the corrective folder beyond BUNDLE_FILES",
        "opening DS2 per-beat labels or V10 probabilities",
        "running detect_r(), M0-M4 aggregation, association or S PR-AUC",
        "training or retraining any model",
        "registering any value, including the new folder id",
        "re-running Q5-E PREP P1/P2",
    ),
    "recorded_in": SPEC_PATH,
}
APPROVAL_NOTE = (
    "This repair is implemented but NOT approved for execution.  An approval "
    "would cover: reading the existing shards and the existing eleven bundle "
    "files read-only, and writing one new corrective folder holding exactly "
    "the twelve BUNDLE_FILES names.  It would NOT cover re-running the beat "
    "join or the null, touching the existing bundle or shards, editing the "
    "frozen module, relaxing the twelve-file contract, or registering "
    "anything.")

# ─────────────────────────────────────────────────────────────────────────────
# Registered identities.  Read from the frozen module where it owns them.
# ─────────────────────────────────────────────────────────────────────────────
#: `research/ASSETS.md :: run-20260811-q5d-ds1-gate`, and the first twelve
#: characters are embedded in the shard folder's name.
FROZEN_Q5D_SHA256 = (
    "6b098c67df3c8e2c8c070b093e6e2d801566f548a3173626745c4a126a97f226")

MISSING_ARTIFACT = "negative_control_null.npz"
BUNDLE_FILES: Tuple[str, ...] = tuple(BJ.BUNDLE_FILES)
#: What the source bundle must hold: the twelve minus the one being rebuilt.
SOURCE_BUNDLE_FILES: Tuple[str, ...] = tuple(
    name for name in BUNDLE_FILES if name != MISSING_ARTIFACT)
SUMMARY_FILE = "null_summary.json"
MANIFEST_FILE = "manifest.json"

#: The NPZ's four arrays, in the order the spec fixes.  `j_null_max` last
#: because it is derived from the three families before it.
NPZ_ARRAYS: Tuple[str, ...] = tuple(sorted(BJ.CONTROL_FAMILIES)) + \
    ("j_null_max",)
N_REPLICATES = BJ.N_NULL_REPLICATES

# ─────────────────────────────────────────────────────────────────────────────
# Stop reasons.  Each is terminal; a repair that stops publishes nothing.
# ─────────────────────────────────────────────────────────────────────────────
NOT_APPROVED = "REPAIR_NOT_APPROVED"
FROZEN_MODULE_MOVED = "REPAIR_FROZEN_MODULE_MOVED"
INPUT_UNQUALIFIED = "REPAIR_INPUT_UNQUALIFIED"
SUMMARY_DISAGREES = "REPAIR_SUMMARY_DISAGREES"
NPZ_CONTRACT_FAILED = "REPAIR_NPZ_CONTRACT_FAILED"
SOURCE_BUNDLE_UNEXPECTED = "REPAIR_SOURCE_BUNDLE_UNEXPECTED"
TARGET_EXISTS = "REPAIR_TARGET_EXISTS"
COPY_NOT_BYTE_IDENTICAL = "REPAIR_COPY_NOT_BYTE_IDENTICAL"
REPAIR_COMPLETE = "REPAIR_COMPLETE"

STOP_REASONS: Tuple[str, ...] = (
    NOT_APPROVED, FROZEN_MODULE_MOVED, INPUT_UNQUALIFIED, SUMMARY_DISAGREES,
    NPZ_CONTRACT_FAILED, SOURCE_BUNDLE_UNEXPECTED, TARGET_EXISTS,
    COPY_NOT_BYTE_IDENTICAL,
)


class RepairError(RuntimeError):
    """Any refusal from this module."""

    def __init__(self, reason: str, message: str) -> None:
        super().__init__(f"{reason}: {message}")
        self.reason = reason


class RepairNotApprovedError(RepairError):
    """Reached a real artifact without the separate execution approval."""

    def __init__(self, message: str) -> None:
        super().__init__(NOT_APPROVED, message)


def require_execution_approval(approval: Optional[str], what: str) -> None:
    """Permission before capability.  Checked before any read or write."""
    if approval != EXECUTION_APPROVAL_TOKEN:
        raise RepairNotApprovedError(
            f"refusing to reach {what}: this repair needs its own separate "
            f"execution approval.  {APPROVAL_NOTE}")


def execution_is_approved(approval: Optional[str]) -> bool:
    return approval == EXECUTION_APPROVAL_TOKEN


def _terminal_execution_guard() -> Dict[str, object]:
    """The single stop a separate execution-approval PR opens.

    It sits after the approval token and the frozen-module check and before the
    first shard read, the first NPZ byte and the first `mkdir`, so an approved
    run reaches a complete route and an unapproved one reaches nothing.  It
    consults :data:`EXECUTION_APPROVAL_RECORD` rather than being deleted, for
    the reason the P1/P2 PREP gives: an absent check records no decision.
    """
    if not EXECUTION_APPROVAL_RECORD.get("granted"):
        raise RepairNotApprovedError(
            "the repair is implemented but not approved for execution: "
            "reading the registered shards or writing a corrective folder "
            f"needs a separate execution approval.  {APPROVAL_NOTE}")
    return dict(EXECUTION_APPROVAL_RECORD)


# ─────────────────────────────────────────────────────────────────────────────
# The frozen module, and proving it is the registered one
# ─────────────────────────────────────────────────────────────────────────────
def frozen_q5d_sha256() -> str:
    """The SHA-256 of the Q5-D module this process actually imported."""
    with open(BJ.__file__, "rb") as handle:
        return hashlib.sha256(handle.read()).hexdigest()


def assert_frozen_q5d_unchanged() -> str:
    """The repair is only meaningful against the version that made the bundle.

    The shard folder's name carries `6b098c67df3c`, which is this digest's
    first twelve characters, so a moved module means the shards on disk were
    produced by something other than the code about to read them.  That is a
    stop, not a warning.
    """
    observed = frozen_q5d_sha256()
    if observed != FROZEN_Q5D_SHA256:
        raise RepairError(
            FROZEN_MODULE_MOVED,
            f"the imported Q5-D module hashes to {observed}, not the "
            f"registered {FROZEN_Q5D_SHA256}.  The null shards were produced "
            f"by the registered version and may not be finalised by another.")
    return observed


# ─────────────────────────────────────────────────────────────────────────────
# Identity, anchored on the bundle manifest rather than on the shards
# ─────────────────────────────────────────────────────────────────────────────
IDENTITY_FIELDS: Tuple[str, ...] = ("split", "code_sha256",
                                    "rule_fingerprint", "input_digest")


def identity_from_manifest(manifest: Mapping[str, object]) -> Dict[str, str]:
    """What the shards must match, taken from the bundle that is being repaired.

    Deriving the expected identity from the shards and then checking the shards
    against it would accept any internally consistent set — including one
    belonging to a different run.  The manifest is the independent anchor.
    """
    missing = [f for f in IDENTITY_FIELDS if not manifest.get(f)]
    if missing:
        raise RepairError(
            INPUT_UNQUALIFIED,
            f"the bundle manifest carries no {missing}; without it there is "
            f"nothing independent to check the shards against")
    return {field: str(manifest[field]) for field in IDENTITY_FIELDS}


class _UnreadMapping(dict):
    """An empty mapping that refuses to be read.

    It makes "the finaliser never touches the join inputs" a fact the tests
    observe rather than a claim in a comment: if anything on the path reaches
    for a record, this raises instead of quietly returning nothing.  `dict()`
    over an empty instance copies no items, so construction still works.
    """

    def __getitem__(self, key):                          # pragma: no cover
        raise AssertionError(
            f"the repair path read join input {key!r}; finalisation is "
            f"supposed to need only the shard identity")

    def get(self, key, default=None):                    # pragma: no cover
        return self.__getitem__(key)


def identity_only_context(identity: Mapping[str, str]) -> "BJ.NullContext":
    """A `NullContext` carrying identity and no join data.

    `finalize_null_shards()` and `verify_null_shard()` consult
    `context.identity()` only — `null_runner_version`, `split`, `families`,
    `master_seed`, `rule_fingerprint`, `code_sha256`, `input_digest`.  The
    heavy maps are read by `compute_null_shard()`, which this repair never
    calls, so rebuilding them would mean re-running exactly what the repair
    exists to avoid.

    `NullContext.__init__` sets `rule_fingerprint` from the **live** frozen
    module, so a rule that had moved would be caught here rather than being
    read out of the manifest and agreed with itself.  That the manifest's
    fingerprint matches it is checked separately, below.
    """
    context = BJ.NullContext(
        split=str(identity["split"]),
        mamba_by_record={}, cache_by_record={},
        processed_classes={}, mamba_classes={},
        input_digest=str(identity["input_digest"]),
        code_sha256=str(identity["code_sha256"]))
    # `NullContext.__init__` copies each mapping with `dict()`, so passing the
    # refusing mapping in would have been converted straight back to a plain
    # empty dict and guarded nothing.  Installing them afterwards keeps the
    # refusal live for the whole of finalisation.
    context.mamba_by_record = _UnreadMapping()
    context.cache_by_record = _UnreadMapping()
    context.processed_classes = _UnreadMapping()
    context.mamba_classes = _UnreadMapping()
    if context.rule_fingerprint != str(identity["rule_fingerprint"]):
        raise RepairError(
            INPUT_UNQUALIFIED,
            f"the live rule fingerprint {context.rule_fingerprint!r} is not "
            f"the bundle's {identity['rule_fingerprint']!r}; a null may not be "
            f"finalised under a rule other than the one that produced it")
    return context


# ─────────────────────────────────────────────────────────────────────────────
# Qualification of the 100 shards
# ─────────────────────────────────────────────────────────────────────────────
def _shard_paths(shard_dir: str) -> List[str]:
    if not os.path.isdir(shard_dir):
        raise RepairError(
            INPUT_UNQUALIFIED,
            f"no shard directory at {shard_dir!r}")
    return [os.path.join(shard_dir, name)
            for name in sorted(os.listdir(shard_dir))
            if name.startswith("null_shard_") and name.endswith(".json")]


def coverage_report(ranges: Sequence[Tuple[int, int]], total: int
                    ) -> Dict[str, object]:
    """Gaps and overlaps as ranges, not as a yes/no.

    A reviewer reading "coverage ok" learns nothing about what was checked; a
    reviewer reading the ranges can see the null really is `0..total-1` once
    each.
    """
    seen: Dict[int, Tuple[int, int]] = {}
    overlaps: List[Dict[str, object]] = []
    for start, end in sorted(ranges):
        for replicate in range(start, end):
            if replicate in seen:
                overlaps.append({"replicate": replicate,
                                 "in": [list(seen[replicate]),
                                        [start, end]]})
            else:
                seen[replicate] = (start, end)
    missing = [b for b in range(int(total)) if b not in seen]
    beyond = sorted(b for b in seen if b >= int(total))
    return {
        "ranges": [list(r) for r in sorted(ranges)],
        "covered": len(seen),
        "expected": int(total),
        "missing_count": len(missing),
        "missing_first": missing[:5],
        "overlap_count": len(overlaps),
        "overlap_first": overlaps[:5],
        "beyond_total": beyond[:5],
        "ok": (not missing and not overlaps and not beyond
               and len(seen) == int(total)),
    }


def qualify_shards(shard_dir: str, manifest: Mapping[str, object],
                   approval: Optional[str],
                   total: int = N_REPLICATES) -> Dict[str, object]:
    """Read the shards and prove they may be finalised, or stop.

    Every clause the spec fixes, each reported with what it observed rather
    than a bare pass — a qualification whose evidence is a boolean cannot be
    audited afterwards.
    """
    require_execution_approval(approval, f"the null shards at {shard_dir!r}")
    _terminal_execution_guard()

    identity = identity_from_manifest(manifest)
    context = identity_only_context(identity)

    paths = _shard_paths(shard_dir)
    if not paths:
        raise RepairError(
            INPUT_UNQUALIFIED,
            f"{shard_dir!r} holds no null_shard_*.json files")

    problems: List[str] = []
    shards: Dict[Tuple[int, int], Dict[str, object]] = {}
    per_shard: List[Dict[str, object]] = []
    for path in paths:
        name = os.path.basename(path)
        try:
            # Verifies the shard's own recorded digest and refuses a corrupt
            # or edited one; this is the frozen module's reader, not ours.
            payload = BJ.read_null_shard(path)
        except BJ.NullShardError as error:
            problems.append(f"{name}: {error}")
            continue
        shard_problems = BJ.verify_null_shard(payload, context)
        problems.extend(f"{name}: {p}" for p in shard_problems)
        key = (int(payload["replicate_start"]), int(payload["replicate_end"]))
        if key in shards:
            problems.append(f"{name}: a second shard claims {list(key)}")
        shards[key] = payload
        per_shard.append({
            "file": name, "replicate_start": key[0], "replicate_end": key[1],
            "digest": str(payload.get("digest")),
            "digest_verified": True,
            "identity_problems": list(shard_problems),
        })

    coverage = coverage_report(list(shards), total)
    if not coverage["ok"]:
        problems.append(
            f"replicate coverage is not exactly 0..{int(total) - 1}: "
            f"{coverage['missing_count']} missing, "
            f"{coverage['overlap_count']} overlapping")

    report: Dict[str, object] = {
        "shard_dir": os.path.basename(os.path.normpath(shard_dir)),
        "shard_count": len(paths),
        "identity_anchor": "bundle manifest.json",
        "identity": dict(identity),
        "live_rule_fingerprint": context.rule_fingerprint,
        "coverage": coverage,
        "per_shard": per_shard,
        "problems": problems,
        "qualified": not problems,
    }
    if problems:
        raise RepairError(
            INPUT_UNQUALIFIED,
            f"{len(problems)} problem(s) over {len(paths)} shards; the first "
            f"few are:\n  " + "\n  ".join(problems[:10]))
    return {"report": report, "shards": shards, "context": context}


# ─────────────────────────────────────────────────────────────────────────────
# Reconstruction — through the frozen finaliser, never around it
# ─────────────────────────────────────────────────────────────────────────────
def reconstruct_arrays(shards: Mapping[Tuple[int, int], Mapping[str, object]],
                       context: "BJ.NullContext",
                       total: int = N_REPLICATES
                       ) -> Dict[str, List[float]]:
    """The four arrays, assembled by `BJ.finalize_null_shards()`.

    `j_null_max` is recomputed here as the per-replicate maximum of the three
    families rather than concatenated from the shards.  Both are available and
    they must agree — `verify_null_shard()` has already checked each shard's
    own `j_null_max` against its families, and `null_summary.json` is checked
    against this one downstream — so deriving it keeps the NPZ's internal
    consistency true by construction instead of by hope.
    """
    families = BJ.finalize_null_shards(shards, context, total=total)
    ordered = sorted(BJ.CONTROL_FAMILIES)
    arrays: Dict[str, List[float]] = {f: list(families[f]) for f in ordered}
    arrays["j_null_max"] = [max(arrays[f][b] for f in ordered)
                            for b in range(int(total))]
    return arrays


def compare_to_summary(arrays: Mapping[str, Sequence[float]],
                       null_summary: Mapping[str, object]) -> Dict[str, object]:
    """Element-wise exact equality against the summary the original run wrote.

    This is the repair's independent check: the shards and `null_summary.json`
    were written by different code paths in the original run, so agreement
    between them is evidence, while agreement of the shards with themselves is
    not.  Reported with the first differing index, because "they differ" does
    not tell a reader whether one value drifted or the whole vector is offset.
    """
    ours = list(arrays["j_null_max"])
    theirs = list(null_summary.get("j_null_max") or [])
    first: Optional[Dict[str, object]] = None
    for index in range(min(len(ours), len(theirs))):
        if ours[index] != theirs[index]:
            first = {"index": index, "reconstructed": ours[index],
                     "summary": theirs[index]}
            break
    if first is None and len(ours) != len(theirs):
        first = {"index": min(len(ours), len(theirs)),
                 "detail": "length differs"}
    return {
        "n_reconstructed": len(ours), "n_summary": len(theirs),
        "identical": first is None and len(ours) == len(theirs),
        "first_difference": first,
        "summary_replicates": null_summary.get("replicates"),
        "summary_rule_fingerprint": null_summary.get("rule_fingerprint"),
    }


# ─────────────────────────────────────────────────────────────────────────────
# NPY / NPZ.  Written explicitly and read back explicitly — see the spec for
# why the verifier is deliberately not the writer's own library.
# ─────────────────────────────────────────────────────────────────────────────
NPY_MAGIC = b"\x93NUMPY"
NPY_VERSION = (1, 0)
NPY_DTYPE = "<f8"
#: A fixed ZIP timestamp, so the same arrays always produce the same bytes.
#: `zipfile` would otherwise stamp the wall clock and make a deterministic
#: reconstruction produce a different file every time it ran.
ZIP_TIMESTAMP = (1980, 1, 1, 0, 0, 0)


def npy_bytes(values: Sequence[float]) -> bytes:
    """One 1-D float64 array in NPY v1.0 — the format `numpy.save` writes.

    Header is padded so that magic + version + length + header is a multiple of
    64 bytes and ends with a newline, which is what the format requires and
    what makes the data section aligned.
    """
    header = ("{'descr': '%s', 'fortran_order': False, 'shape': (%d,), }"
              % (NPY_DTYPE, len(values)))
    prefix = len(NPY_MAGIC) + 2 + 2                      # magic, version, len
    padding = 64 - ((prefix + len(header) + 1) % 64)
    if padding == 64:
        padding = 0
    header = header + " " * padding + "\n"
    out = bytearray()
    out += NPY_MAGIC
    out += bytes(NPY_VERSION)
    out += struct.pack("<H", len(header))
    out += header.encode("latin-1")
    for value in values:
        out += struct.pack("<d", float(value))
    return bytes(out)


def read_npy_bytes(blob: bytes) -> Tuple[str, Tuple[int, ...], List[float]]:
    """Parse an NPY v1.0 array without numpy.  Refuses anything else.

    Deliberately strict: a pickled object array is exactly what
    `allow_pickle=False` exists to reject, and this reader cannot represent one
    at all, so a file it accepts is a file numpy can load with pickling off.
    """
    if not blob.startswith(NPY_MAGIC):
        raise RepairError(NPZ_CONTRACT_FAILED, "not an NPY file")
    major, minor = blob[6], blob[7]
    if (major, minor) != NPY_VERSION:
        raise RepairError(NPZ_CONTRACT_FAILED,
                          f"NPY version {major}.{minor}, expected 1.0")
    (header_length,) = struct.unpack("<H", blob[8:10])
    header = blob[10:10 + header_length].decode("latin-1")
    body = blob[10 + header_length:]
    if "'descr'" not in header or "'shape'" not in header:
        raise RepairError(NPZ_CONTRACT_FAILED, f"unreadable header {header!r}")
    descr = header.split("'descr':")[1].split(",")[0].strip().strip("'\"")
    fortran = "True" in header.split("'fortran_order':")[1].split(",")[0]
    shape_text = header.split("'shape':")[1].split("(")[1].split(")")[0]
    dims = tuple(int(part) for part in shape_text.split(",") if part.strip())
    if descr != NPY_DTYPE:
        raise RepairError(NPZ_CONTRACT_FAILED,
                          f"dtype {descr!r}, expected {NPY_DTYPE!r}")
    if fortran:
        raise RepairError(NPZ_CONTRACT_FAILED, "fortran_order is True")
    count = 1
    for dim in dims:
        count *= dim
    if len(body) != count * 8:
        raise RepairError(
            NPZ_CONTRACT_FAILED,
            f"{len(body)} data bytes for {count} float64 values")
    values = [struct.unpack("<d", body[i * 8:i * 8 + 8])[0]
              for i in range(count)]
    return descr, dims, values


def npz_bytes(arrays: Mapping[str, Sequence[float]]) -> bytes:
    """The four arrays as an uncompressed NPZ, with deterministic bytes."""
    names = list(NPZ_ARRAYS)
    unexpected = sorted(set(arrays) - set(names))
    missing = [n for n in names if n not in arrays]
    if missing or unexpected:
        raise RepairError(
            NPZ_CONTRACT_FAILED,
            f"the NPZ holds exactly {names}; missing={missing} "
            f"unexpected={unexpected}")
    import io
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_STORED) as archive:
        for name in names:
            info = zipfile.ZipInfo(f"{name}.npy", date_time=ZIP_TIMESTAMP)
            info.compress_type = zipfile.ZIP_STORED
            archive.writestr(info, npy_bytes(arrays[name]))
    return buffer.getvalue()


def read_npz_bytes(blob: bytes) -> Dict[str, Tuple[str, Tuple[int, ...],
                                                   List[float]]]:
    """Every member of an NPZ, parsed without numpy."""
    import io
    out: Dict[str, Tuple[str, Tuple[int, ...], List[float]]] = {}
    with zipfile.ZipFile(io.BytesIO(blob)) as archive:
        for name in archive.namelist():
            if not name.endswith(".npy"):
                raise RepairError(
                    NPZ_CONTRACT_FAILED,
                    f"the NPZ holds a non-array member {name!r}")
            out[name[:-4]] = read_npy_bytes(archive.read(name))
    return out


def _is_finite(value: float) -> bool:
    return value == value and value not in (float("inf"), float("-inf"))


def verify_npz_contract(blob: bytes,
                        expected_j_null_max: Optional[Sequence[float]] = None,
                        total: int = N_REPLICATES) -> Dict[str, object]:
    """Every clause of the spec's NPZ contract, checked by reading the bytes.

    Reading them back matters: verifying the values that were *passed in*
    checks the caller's variables, not the file, and the file is what will be
    published.
    """
    problems: List[str] = []
    members = read_npz_bytes(blob)

    names = sorted(members)
    if names != sorted(NPZ_ARRAYS):
        problems.append(f"arrays {names}, expected {sorted(NPZ_ARRAYS)}")

    per_array: Dict[str, object] = {}
    for name in sorted(set(NPZ_ARRAYS) & set(members)):
        descr, dims, values = members[name]
        finite = all(_is_finite(v) for v in values)
        if descr != NPY_DTYPE:
            problems.append(f"{name}: dtype {descr!r}")
        if dims != (int(total),):
            problems.append(f"{name}: shape {dims}, expected ({int(total)},)")
        if not finite:
            problems.append(f"{name}: holds a non-finite value")
        per_array[name] = {"dtype": descr, "shape": list(dims),
                           "finite": finite, "n": len(values)}

    if all(n in members for n in NPZ_ARRAYS):
        families = sorted(BJ.CONTROL_FAMILIES)
        maxima = members["j_null_max"][2]
        mismatched = [
            b for b in range(min(len(maxima),
                                 min(len(members[f][2]) for f in families)))
            if maxima[b] != max(members[f][2][b] for f in families)]
        if mismatched:
            problems.append(
                f"j_null_max is not the family maximum at {len(mismatched)} "
                f"replicates (first: {mismatched[:5]})")
        per_array["j_null_max_is_family_max"] = not mismatched

    if expected_j_null_max is not None and "j_null_max" in members:
        ours = members["j_null_max"][2]
        theirs = list(expected_j_null_max)
        differing = [b for b in range(min(len(ours), len(theirs)))
                     if ours[b] != theirs[b]]
        if differing or len(ours) != len(theirs):
            problems.append(
                f"j_null_max differs from the expected vector at "
                f"{len(differing)} replicates (first: {differing[:5]}); "
                f"lengths {len(ours)} vs {len(theirs)}")

    return {
        "ok": not problems,
        "sha256": hashlib.sha256(blob).hexdigest(),
        "bytes": len(blob),
        "arrays": per_array,
        "allow_pickle_false_readable": True,
        "problems": problems,
    }


# ─────────────────────────────────────────────────────────────────────────────
# The corrective bundle
# ─────────────────────────────────────────────────────────────────────────────
def _read_file(path: str) -> bytes:
    with open(path, "rb") as handle:
        return handle.read()


def _write_new_file(path: str, body: bytes) -> None:
    """Exclusive create, binary, short-write safe.

    The same discipline the PREP writer uses and for the same reasons: claiming
    a directory says nothing about the names inside it, a truncating open would
    replace another writer's bytes silently, and a text-mode descriptor on
    Windows would rewrite every `\\n` so the file would not equal what was
    hashed.
    """
    flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY | getattr(os, "O_BINARY", 0)
    handle = os.open(path, flags, 0o644)
    try:
        written = 0
        while written < len(body):
            just = os.write(handle, body[written:])
            if just == 0:
                raise RepairError(
                    COPY_NOT_BYTE_IDENTICAL,
                    f"a write to {os.path.basename(path)} returned 0 bytes")
            written += just
    finally:
        os.close(handle)


def inspect_source_bundle(source_dir: str, approval: Optional[str]
                          ) -> Dict[str, object]:
    """The eleven, their sizes and their digests — read-only.

    A source that is not the bundle P2 measured is not the thing this repair
    was authorised for, so an unexpected name is a stop rather than something
    to copy along.
    """
    require_execution_approval(approval, f"the source bundle at {source_dir!r}")
    _terminal_execution_guard()
    if not os.path.isdir(source_dir):
        raise RepairError(SOURCE_BUNDLE_UNEXPECTED,
                          f"no source bundle directory at {source_dir!r}")
    present = sorted(name for name in os.listdir(source_dir)
                     if os.path.isfile(os.path.join(source_dir, name)))
    subdirs = sorted(name for name in os.listdir(source_dir)
                     if not os.path.isfile(os.path.join(source_dir, name)))
    missing = [n for n in SOURCE_BUNDLE_FILES if n not in present]
    unexpected = [n for n in present if n not in SOURCE_BUNDLE_FILES]
    if missing or unexpected or subdirs:
        raise RepairError(
            SOURCE_BUNDLE_UNEXPECTED,
            f"the source bundle must hold exactly the eleven "
            f"{list(SOURCE_BUNDLE_FILES)}; missing={missing} "
            f"unexpected={unexpected} subdirectories={subdirs}")
    files: List[Dict[str, object]] = []
    for name in SOURCE_BUNDLE_FILES:
        body = _read_file(os.path.join(source_dir, name))
        files.append({"name": name, "bytes": len(body),
                      "sha256": hashlib.sha256(body).hexdigest()})
    return {"directory": os.path.basename(os.path.normpath(source_dir)),
            "files": files, "count": len(files),
            "missing": missing, "unexpected": unexpected}


def read_bundle_json(source_dir: str, name: str,
                     approval: Optional[str]) -> Dict[str, object]:
    """One JSON file out of the source bundle, read-only."""
    require_execution_approval(approval, f"{name} in {source_dir!r}")
    _terminal_execution_guard()
    with open(os.path.join(source_dir, name), encoding="utf-8") as handle:
        return json.load(handle)


def assemble_corrective_bundle(source_dir: str, target_dir: str,
                               npz: bytes, approval: Optional[str]
                               ) -> Dict[str, object]:
    """Copy the eleven byte-identically, add the NPZ, verify the twelve.

    Nothing is written into, beside or over the source.  The target name is
    claimed with a single `os.mkdir`, which never replaces and never follows:
    an existing file, directory, symlink or junction all raise.
    """
    require_execution_approval(approval, f"a corrective folder at {target_dir!r}")
    _terminal_execution_guard()

    source = inspect_source_bundle(source_dir, approval)
    if os.path.lexists(target_dir):
        raise RepairError(
            TARGET_EXISTS,
            f"{target_dir!r} already exists; a corrective bundle is written to "
            f"a new name and never on top of anything")
    os.mkdir(target_dir)

    copied: List[Dict[str, object]] = []
    for row in source["files"]:
        name = str(row["name"])
        body = _read_file(os.path.join(source_dir, name))
        if hashlib.sha256(body).hexdigest() != row["sha256"]:
            raise RepairError(
                COPY_NOT_BYTE_IDENTICAL,
                f"{name} changed between being inventoried and being read")
        _write_new_file(os.path.join(target_dir, name), body)
        back = _read_file(os.path.join(target_dir, name))
        digest = hashlib.sha256(back).hexdigest()
        if digest != row["sha256"] or len(back) != row["bytes"]:
            raise RepairError(
                COPY_NOT_BYTE_IDENTICAL,
                f"{name} landed as {digest} / {len(back)} B, not "
                f"{row['sha256']} / {row['bytes']} B")
        copied.append({"name": name, "bytes": len(back), "sha256": digest,
                       "byte_identical": True})

    _write_new_file(os.path.join(target_dir, MISSING_ARTIFACT), npz)
    written = _read_file(os.path.join(target_dir, MISSING_ARTIFACT))
    if written != npz:
        raise RepairError(
            COPY_NOT_BYTE_IDENTICAL,
            f"{MISSING_ARTIFACT} on disk is not the bytes that were verified")
    copied.append({"name": MISSING_ARTIFACT, "bytes": len(written),
                   "sha256": hashlib.sha256(written).hexdigest(),
                   "byte_identical": None})

    listing = sorted(os.listdir(target_dir))
    missing = [n for n in BUNDLE_FILES if n not in listing]
    unexpected = [n for n in listing if n not in BUNDLE_FILES]
    if missing or unexpected:
        raise RepairError(
            SOURCE_BUNDLE_UNEXPECTED,
            f"the corrective folder must hold exactly the twelve "
            f"BUNDLE_FILES; missing={missing} unexpected={unexpected}")
    return {"directory": os.path.basename(os.path.normpath(target_dir)),
            "files": copied, "listing": listing,
            "missing": missing, "unexpected": unexpected,
            "contract_files": list(BUNDLE_FILES)}


def verify_corrective_bundle(target_dir: str,
                             source: Mapping[str, object],
                             npz_sha256: str) -> Dict[str, object]:
    """Re-read the finished folder and compare it to what it should be.

    Separate from the assembly on purpose: a writer that certifies its own
    output is checking its variables.  This one opens the files again.
    """
    listing = sorted(os.listdir(target_dir))
    problems: List[str] = []
    if listing != sorted(BUNDLE_FILES):
        problems.append(f"listing {listing} != the twelve {sorted(BUNDLE_FILES)}")
    expected = {str(row["name"]): str(row["sha256"])
                for row in source["files"]}
    expected[MISSING_ARTIFACT] = npz_sha256
    observed: Dict[str, str] = {}
    for name in listing:
        digest = hashlib.sha256(
            _read_file(os.path.join(target_dir, name))).hexdigest()
        observed[name] = digest
        if name in expected and digest != expected[name]:
            problems.append(f"{name}: {digest} != expected {expected[name]}")
    return {"ok": not problems, "listing": listing, "observed": observed,
            "expected": expected, "problems": problems}


# ─────────────────────────────────────────────────────────────────────────────
# The whole route
# ─────────────────────────────────────────────────────────────────────────────
def run_repair(shard_dir: str, source_dir: str, target_dir: str,
               approval: Optional[str] = None,
               total: int = N_REPLICATES) -> Dict[str, object]:
    """Qualify, reconstruct, cross-check, assemble, verify — or stop.

    Order matters and is not an accident: nothing is created on disk until the
    shards have qualified, the arrays have been reconstructed, the summary has
    agreed and the NPZ bytes have passed their contract.  A run that stops
    leaves no corrective folder at all.
    """
    require_execution_approval(approval, "the repair route")
    frozen = assert_frozen_q5d_unchanged()
    _terminal_execution_guard()

    manifest = read_bundle_json(source_dir, MANIFEST_FILE, approval)
    summary = read_bundle_json(source_dir, SUMMARY_FILE, approval)

    qualified = qualify_shards(shard_dir, manifest, approval, total=total)
    arrays = reconstruct_arrays(qualified["shards"], qualified["context"],
                                total=total)

    agreement = compare_to_summary(arrays, summary)
    if not agreement["identical"]:
        raise RepairError(
            SUMMARY_DISAGREES,
            f"the reconstructed j_null_max does not equal the one in "
            f"{SUMMARY_FILE}: {agreement['first_difference']}")

    blob = npz_bytes(arrays)
    contract = verify_npz_contract(blob, summary.get("j_null_max"),
                                   total=total)
    if not contract["ok"]:
        raise RepairError(NPZ_CONTRACT_FAILED,
                          "; ".join(str(p) for p in contract["problems"]))

    source = inspect_source_bundle(source_dir, approval)
    assembled = assemble_corrective_bundle(source_dir, target_dir, blob,
                                           approval)
    verified = verify_corrective_bundle(target_dir, source,
                                        contract["sha256"])
    if not verified["ok"]:
        raise RepairError(COPY_NOT_BYTE_IDENTICAL,
                          "; ".join(str(p) for p in verified["problems"]))

    return {
        "experiment_id": EXPERIMENT_ID, "substage": SUBSTAGE,
        "module_version": MODULE_VERSION, "spec": SPEC_PATH,
        "status": REPAIR_COMPLETE,
        "first_stopping_reason": None,
        "frozen_q5d_sha256": frozen,
        "qualification": qualified["report"],
        "summary_agreement": agreement,
        "npz": contract,
        "source_bundle": source,
        "corrective_bundle": assembled,
        "verification": verified,
        "training_performed": False,
        "join_rerun": False,
        "null_recomputed": False,
        "ds2_outcome_opened": False,
        "v10_probability_opened": False,
        "registered_anything": False,
    }


def report_markdown(decision: Mapping[str, object]) -> str:
    """The human-readable record.  Its saved notebook output is the anchor.

    No sidecar file is written into the corrective folder, so this printed
    report — copied into the Decision log by a separate PR — is where the
    digests and the provenance live.
    """
    qualification = dict(decision.get("qualification") or {})
    coverage = dict(qualification.get("coverage") or {})
    npz = dict(decision.get("npz") or {})
    agreement = dict(decision.get("summary_agreement") or {})
    source = dict(decision.get("source_bundle") or {})
    corrective = dict(decision.get("corrective_bundle") or {})
    lines = [
        f"# {EXPERIMENT_ID} — {SUBSTAGE}",
        "",
        f"status: **{decision.get('status')}** · first stopping reason: "
        f"{decision.get('first_stopping_reason')}",
        "",
        "A packaging repair. No J value was computed, no replicate was re-run, "
        "and no scientific question was answered.",
        "",
        "## Identity",
        f"- frozen Q5-D SHA-256 `{decision.get('frozen_q5d_sha256')}`",
        f"- identity anchor: {qualification.get('identity_anchor')}",
        f"- live rule fingerprint `{qualification.get('live_rule_fingerprint')}`",
        "",
        "## Shards",
        f"- {qualification.get('shard_count')} shards, qualified: "
        f"{qualification.get('qualified')}",
        f"- coverage {coverage.get('covered')}/{coverage.get('expected')} · "
        f"missing {coverage.get('missing_count')} · overlapping "
        f"{coverage.get('overlap_count')}",
        "",
        "## Reconstruction",
        f"- j_null_max identical to {SUMMARY_FILE}: "
        f"{agreement.get('identical')} "
        f"({agreement.get('n_reconstructed')} vs {agreement.get('n_summary')})",
        f"- NPZ SHA-256 `{npz.get('sha256')}` ({npz.get('bytes')} B), "
        f"contract ok: {npz.get('ok')}",
        "",
        "## Corrective bundle",
        f"- source: {source.get('count')} files",
        f"- target: {len(list(corrective.get('listing') or []))} files, "
        f"missing {corrective.get('missing')} unexpected "
        f"{corrective.get('unexpected')}",
        "",
        "## Not done",
        "- the existing bundle and shards were opened read-only and not "
        "modified, deleted, overwritten or moved",
        "- no file outside the new corrective folder was written",
        "- no value was registered; registration is a separate PR",
    ]
    return "\n".join(lines)


def module_capabilities() -> Tuple[str, ...]:
    """Names a notebook asserts before use, so a stale clone cannot masquerade."""
    return ("run_repair", "qualify_shards", "reconstruct_arrays",
            "compare_to_summary", "npy_bytes", "read_npy_bytes", "npz_bytes",
            "read_npz_bytes", "verify_npz_contract", "inspect_source_bundle",
            "assemble_corrective_bundle", "verify_corrective_bundle",
            "identity_from_manifest", "identity_only_context",
            "coverage_report", "assert_frozen_q5d_unchanged",
            "report_markdown", "EXECUTION_APPROVAL_TOKEN",
            "EXECUTION_APPROVAL_RECORD", "NPZ_ARRAYS", "BUNDLE_FILES",
            "SOURCE_BUNDLE_FILES", "STOP_REASONS")


def design_card() -> str:
    """What this module is and is not, printed before anything runs."""
    return "\n".join([
        f"{EXPERIMENT_ID} / {SUBSTAGE} — module v{MODULE_VERSION}",
        f"spec: {SPEC_PATH}",
        f"originating decision: {ORIGINATING_DECISION}",
        "",
        "A packaging repair: reconstruct negative_control_null.npz from the",
        "100 existing null shards and place it in a NEW corrective folder",
        "beside byte-identical copies of the existing eleven files.",
        "",
        "It does NOT re-run the beat join, re-run the null, compute any J",
        "value, modify the existing bundle or shards, edit the frozen module,",
        "relax the twelve-file contract, or register anything.",
        "",
        f"execution approved: {bool(EXECUTION_APPROVAL_RECORD.get('granted'))}",
        APPROVAL_NOTE,
    ])
