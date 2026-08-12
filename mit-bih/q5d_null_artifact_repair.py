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

The frozen Q5-D module is imported **read-only**; its LF-normalised SHA-256 is
asserted before anything else happens.  This module never writes to it and
never calls any of its writers.
"""

from __future__ import annotations

import hashlib
import io
import json
import os
import struct
import zipfile
from typing import Dict, List, Mapping, Optional, Sequence, Tuple

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in os.sys.path:                              # pragma: no cover
    os.sys.path.insert(0, HERE)

import q5d_order_preserving_beat_join as BJ              # noqa: E402
import q5e_leg2_failure_mechanism_audit as Q5E           # noqa: E402

EXPERIMENT_ID = "EXP-2026-009"
SUBSTAGE = "Q5D_NULL_ARTIFACT_REPAIR"
RUN_SLUG = "EXP-2026-009_q5d_null_artifact_repair"
MODULE_VERSION = 2
SPEC_PATH = "experiments/specs/EXP-2026-009-q5d-null-artifact-repair.md"
NOTEBOOK_PATH = "notebooks/quest57_q5d_null_artifact_repair.ipynb"
MODULE_PATH = "mit-bih/q5d_null_artifact_repair.py"
#: Where the repository root is, when a caller did not say.  A run should pass
#: `repo_root` explicitly; this is only so the identity check has something to
#: fail against rather than crashing on `None`.
ROOT_GUESS = os.path.dirname(HERE)
ORIGINATING_DECISION = ("experiments/specs/"
                        "EXP-2026-008-q5e-prep-p1-p2-execution-contract.md")

# ─── APPROVAL BLOCK START ────────────────────────────────────────────────────
# Everything between these markers is approval metadata and the guard.  It is
# excluded from `module_science_digest()`, which is what makes an
# execution-enable PR verifiable: that PR may change this block and nothing
# else, and the science digest proves it.  Do not put logic here.
#
# Its own token: approving this repair is not approving the Q5-E PREP, the
# Q5-E audit, or a P1/P2 re-run, and none of those approves this.  The Q5-E
# PREP token is never translated or reused.
# ─────────────────────────────────────────────────────────────────────────────
EXECUTION_APPROVAL_TOKEN = "q5d-null-artifact-repair-execution-approved-by-user"

#: The commit Codex reviewed, recorded **by a later commit**.  This is how the
#: pin avoids being self-referential: a commit SHA written into the very commit
#: it names cannot exist, and a 40-hex string typed into a notebook is not an
#: approval — it is an assertion by whoever typed it.  So the approved
#: implementation is named here, in the enable PR, pointing *backwards*; the
#: notebook measures the actual `HEAD` it is running and the two are checked
#: against each other.
APPROVED_IMPLEMENTATION_COMMIT: Optional[str] = None

#: LF-normalised digests of what the review actually covered.  The repair
#: module is **not** in this table: a record inside a file cannot certify that
#: file.  What covers the module is `module_science_digest()` — the module with
#: this approval block removed — so an enable PR that only flips the guard
#: leaves it unchanged and a science change is visible.
APPROVED_ARTIFACT_DIGESTS: Dict[str, Optional[str]] = {
    "spec_lf_sha256": None,
    "notebook_lf_sha256": None,
    "frozen_q5d_lf_sha256": None,
    "module_science_lf_sha256": None,
}

#: Closed.  The record is written down rather than implied by an absent check:
#: a deleted guard reads identically whether an approval happened or someone
#: removed an inconvenience.  Flipping `granted` to True, with the rest filled
#: in, is the whole of what an execution-approval PR does here.
EXECUTION_APPROVAL_RECORD: Dict[str, object] = {
    "granted": False,
    "granted_on": None,
    "granted_by": None,
    "pinned_commit": None,
    "kind": ("reconstruct negative_control_null.npz from the existing "
             "EXP-2026-007 null shards and assemble a new corrective bundle "
             "folder"),
    "would_approve": (
        "reading the 100 existing null shards, read-only",
        "reading the existing canonical Q5-D bundle's eleven files, read-only",
        "read-only Drive folder-id inventories of the registered folder ids",
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
# ─── APPROVAL BLOCK END ──────────────────────────────────────────────────────
APPROVAL_NOTE = (
    "This repair is implemented but NOT approved for execution.  An approval "
    "would cover: reading the existing shards and the existing eleven bundle "
    "files read-only, read-only folder-id inventories, and writing one new "
    "corrective folder holding exactly the twelve BUNDLE_FILES names.  It "
    "would NOT cover re-running the beat join or the null, touching the "
    "existing bundle or shards, editing the frozen module, relaxing the "
    "twelve-file contract, or registering anything.")

# ─────────────────────────────────────────────────────────────────────────────
# Registered identities.  Read from where each is owned; never re-declared
# here when another module already holds it.
# ─────────────────────────────────────────────────────────────────────────────
#: `research/ASSETS.md :: run-20260811-q5d-ds1-gate`, and its first twelve
#: characters are embedded in the shard folder's name.  **This is the
#: LF-normalised digest** — see `NEWLINE_CONVENTION` below.
FROZEN_Q5D_SHA256_LF = (
    "6b098c67df3c8e2c8c070b093e6e2d801566f548a3173626745c4a126a97f226")
REGISTERED_RULE_FINGERPRINT = Q5E.REGISTERED_RULE_FINGERPRINT
REGISTERED_SPLIT = "DS1"
REGISTERED_MASTER_SEED = BJ.MASTER_SEED
REGISTERED_NULL_RUNNER_VERSION = BJ.NULL_RUNNER_VERSION
REGISTERED_FAMILIES: Tuple[str, ...] = tuple(BJ.CONTROL_FAMILIES)

#: Drive folder ids, confirmed by the user on 2026-08-12.  A folder is chosen
#: by id and never by name: a folder that merely has the right name is not
#: evidence, and that substitution is easy to make and impossible to notice
#: afterwards.
SOURCE_BUNDLE_FOLDER_ID = Q5E.SOURCE_BUNDLE_FOLDER_ID
SOURCE_BUNDLE_RUN = Q5E.SOURCE_BUNDLE_RUN
SHARD_FOLDER_ID = "1c0AbOwwu1UoZ_8Wz60fhzjDcgCkLHMG9"
RUNS_PARENT_FOLDER_ID = "1YbNX4IeWUph3VFwgpCHGFiibzihF6gXh"

#: No full `input_digest` is registered anywhere in this repository — only the
#: field name appears, in the specs.  So it is checked for **type and format**
#: and for agreement between the shards and the folder-id-anchored manifest,
#: and `None` here says truthfully that there is no third, independent value to
#: compare against yet.  A registration PR should add one; inventing a constant
#: to compare with would be a check that always passes.
REGISTERED_INPUT_DIGEST: Optional[str] = None

MISSING_ARTIFACT = "negative_control_null.npz"
BUNDLE_FILES: Tuple[str, ...] = tuple(BJ.BUNDLE_FILES)
#: What the source bundle must hold: the twelve minus the one being rebuilt.
SOURCE_BUNDLE_FILES: Tuple[str, ...] = tuple(
    name for name in BUNDLE_FILES if name != MISSING_ARTIFACT)
SUMMARY_FILE = "null_summary.json"
MANIFEST_FILE = "manifest.json"

N_REPLICATES = BJ.N_NULL_REPLICATES
SHARD_WIDTH = BJ.DEFAULT_SHARD_SIZE
#: The preregistered shard set, generated from the frozen plan rather than
#: retyped: exactly 100 ranges of 100, `null_shard_00000_00100.json` through
#: `null_shard_09900_10000.json`.
EXPECTED_SHARD_RANGES: Tuple[Tuple[int, int], ...] = BJ.shard_plan(
    total=N_REPLICATES, shard_size=SHARD_WIDTH)
EXPECTED_SHARD_FILENAMES: Tuple[str, ...] = tuple(
    BJ.shard_filename(start, end) for start, end in EXPECTED_SHARD_RANGES)
EXPECTED_SHARD_COUNT = len(EXPECTED_SHARD_RANGES)

# ─────────────────────────────────────────────────────────────────────────────
# NPZ member names.
#
# `MEMBER_NAME_BY_FAMILY` maps a frozen control family to its NPZ member name
# and is the *only* place that mapping lives, so the family maximum is always
# computed over families and a rename cannot silently break the relation.
# ─────────────────────────────────────────────────────────────────────────────
MEMBER_NAME_BY_FAMILY: Dict[str, str] = {f: f for f in REGISTERED_FAMILIES}
MAX_MEMBER_NAME = "j_null_max"
NPZ_ARRAYS: Tuple[str, ...] = tuple(
    sorted(MEMBER_NAME_BY_FAMILY[f] for f in REGISTERED_FAMILIES)
) + (MAX_MEMBER_NAME,)

#: **Resolved (N1, 2026-08-12).**  The native frozen family names are retained
#: and the proposed aliases are rejected — not deferred.  The reason is
#: substantive rather than procedural: `order_shuffle` and `circular_shift` are
#: *both* within-record manipulations, so no bijection exists between the three
#: families and the proposed
#: `j_null_cross_record` / `j_null_within_record` / `j_null_rr_mismatch`, and
#: nothing uniquely corresponds to `rr_mismatch`.  Any mapping would be a
#: guess, and a wrong one would mislabel a published artifact while passing
#: every structural clause.
#:
#: Kept as an audit trail only.  Nothing reads it.
REJECTED_PROPOSAL: Dict[str, object] = {
    "proposed_names": ("j_null_max", "j_null_cross_record",
                       "j_null_within_record", "j_null_rr_mismatch"),
    "decision": "rejected",
    "decided_on": "2026-08-12",
    "reason": ("no bijective semantic mapping exists: order_shuffle and "
               "circular_shift are both within-record manipulations and "
               "nothing uniquely corresponds to rr_mismatch"),
    "recorded_in": SPEC_PATH,
}
MEMBER_NAMING_UNRESOLVED = False
MEMBER_NAMING_NOTE = (
    "The NPZ member names are the native frozen control family names plus "
    "j_null_max, as fixed by D3 and confirmed by N1.  The proposed aliases "
    "j_null_cross_record / j_null_within_record / j_null_rr_mismatch were "
    "rejected because no bijective semantic mapping exists — order_shuffle and "
    "circular_shift are both within-record manipulations and nothing uniquely "
    "corresponds to rr_mismatch.  Computed values and array order are "
    "unchanged by this decision.")

# ─────────────────────────────────────────────────────────────────────────────
# Newline convention
# ─────────────────────────────────────────────────────────────────────────────
NEWLINE_CONVENTION = (
    "Registered source identities are SHA-256 over LF-normalised bytes: CRLF "
    "is folded to LF before hashing, so the same file checked out on Windows "
    "and on Linux carries the same registered identity.  The raw-byte digest "
    "is reported alongside and is deliberately different on a CRLF checkout — "
    "it identifies the bytes on this disk, not the registered artifact.  A "
    "lone CR is refused rather than folded: it is not a newline convention "
    "this repository uses, and treating it as one would make two genuinely "
    "different files share an identity.")

# ─────────────────────────────────────────────────────────────────────────────
# Stop reasons.  Each is terminal; a repair that stops publishes nothing that
# is marked accepted.
# ─────────────────────────────────────────────────────────────────────────────
NOT_APPROVED = "REPAIR_NOT_APPROVED"
FROZEN_MODULE_MOVED = "REPAIR_FROZEN_MODULE_MOVED"
EXECUTION_IDENTITY_UNVERIFIED = "REPAIR_EXECUTION_IDENTITY_UNVERIFIED"
READONLY_SCOPE_UNPROVEN = "REPAIR_READONLY_SCOPE_UNPROVEN"
BYTES_MOVED_AFTER_BRIDGE = "REPAIR_BYTES_MOVED_AFTER_BRIDGE"
OUTPUT_FOLDER_ID_UNRESOLVED = "REPAIR_OUTPUT_FOLDER_ID_UNRESOLVED"
UNDEFINED_NEWLINE = "REPAIR_UNDEFINED_NEWLINE"
INPUT_UNQUALIFIED = "REPAIR_INPUT_UNQUALIFIED"
SUMMARY_DISAGREES = "REPAIR_SUMMARY_DISAGREES"
NPZ_CONTRACT_FAILED = "REPAIR_NPZ_CONTRACT_FAILED"
NUMPY_UNAVAILABLE = "REPAIR_NUMPY_UNAVAILABLE"
SOURCE_BUNDLE_UNEXPECTED = "REPAIR_SOURCE_BUNDLE_UNEXPECTED"
SOURCE_CHANGED_DURING_RUN = "REPAIR_SOURCE_CHANGED_DURING_RUN"
TARGET_EXISTS = "REPAIR_TARGET_EXISTS"
TARGET_UNSAFE = "REPAIR_TARGET_UNSAFE"
COPY_NOT_BYTE_IDENTICAL = "REPAIR_COPY_NOT_BYTE_IDENTICAL"
REPAIR_COMPLETE = "REPAIR_COMPLETE"
#: Not a stop reason — the state of a folder a stop left behind.  It is never
#: `COMMITTED`, never accepted, and never deleted or overwritten.
INCOMPLETE_PRESERVED = "REPAIR_INCOMPLETE_TARGET_PRESERVED"

STOP_REASONS: Tuple[str, ...] = (
    NOT_APPROVED, FROZEN_MODULE_MOVED, EXECUTION_IDENTITY_UNVERIFIED,
    READONLY_SCOPE_UNPROVEN, UNDEFINED_NEWLINE, INPUT_UNQUALIFIED,
    BYTES_MOVED_AFTER_BRIDGE, SUMMARY_DISAGREES, NPZ_CONTRACT_FAILED,
    NUMPY_UNAVAILABLE, SOURCE_BUNDLE_UNEXPECTED, SOURCE_CHANGED_DURING_RUN,
    TARGET_EXISTS, TARGET_UNSAFE, COPY_NOT_BYTE_IDENTICAL,
    OUTPUT_FOLDER_ID_UNRESOLVED,
)

#: The one seam a synthetic fixture may use to skip Drive.  Production never
#: accepts it: `run_repair()` requires a real adapter route, and the
#: synthetic-only entry point requires this marker explicitly, so "no adapter"
#: can never be reached by forgetting an argument.
SYNTHETIC_FIXTURE_MARKER = "q5d-null-repair-synthetic-fixture-not-a-result"
MODE_PRODUCTION = "production"
MODE_SYNTHETIC = "synthetic_fixture"
#: A synthetic run's terminal status.  Deliberately not `REPAIR_COMPLETE`: a
#: fixture result must not be mistakable for a publishable one, and this is what
#: makes "REPAIR_COMPLETE with no resolved folder id" structurally impossible.
SYNTHETIC_COMPLETE = "REPAIR_COMPLETE_SYNTHETIC_FIXTURE"

FAILURE_PUBLICATION_CONTRACT = (
    "A stop before the target directory is created leaves no directory at all. "
    "A stop after it is created leaves the partial directory exactly where it "
    "is, at the reported path and with its file list reported, marked "
    "REPAIR_INCOMPLETE_TARGET_PRESERVED: it is never committed, never "
    "accepted, never registered, and never deleted, overwritten or renamed by "
    "this module.  A retry uses a new unique target path; it does not reuse, "
    "clean or resume the preserved one.")


class RepairError(RuntimeError):
    """Any refusal from this module.

    Carries the preserved-directory detail when a stop happened after the
    target was claimed, because "where is the half-written folder" is the first
    thing a diagnosis needs and reconstructing it from a message is guesswork.
    """

    def __init__(self, reason: str, message: str,
                 incomplete_directory: Optional[str] = None,
                 listing: Sequence[str] = ()) -> None:
        super().__init__(f"{reason}: {message}")
        self.reason = reason
        self.incomplete_directory = incomplete_directory
        self.listing = tuple(listing)
        self.target_state = (INCOMPLETE_PRESERVED if incomplete_directory
                             else None)

    def as_record(self) -> Dict[str, object]:
        """What the notebook prints and a Decision log copies."""
        return {
            "first_stopping_reason": self.reason,
            "message": str(self),
            "target_state": self.target_state,
            "incomplete_directory": self.incomplete_directory,
            "incomplete_listing": list(self.listing),
            "committed": False,
            "accepted": False,
            "registered_anything": False,
            "retry_guidance": FAILURE_PUBLICATION_CONTRACT,
        }


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
# Digests, and the newline convention the registered identities use
# ─────────────────────────────────────────────────────────────────────────────
def _sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def normalise_newlines(payload: bytes, where: str = "input") -> bytes:
    """CRLF folded to LF.  A lone CR is refused, not folded.

    Folding a lone CR would let two genuinely different files share one
    registered identity, and this repository has no artifact that uses CR line
    endings — so the safe reading of an unexpected CR is "something is wrong",
    not "probably a Mac Classic file".
    """
    folded = payload.replace(b"\r\n", b"\n")
    if b"\r" in folded:
        index = folded.index(b"\r")
        raise RepairError(
            UNDEFINED_NEWLINE,
            f"{where} contains a lone CR at byte {index}; LF and CRLF are the "
            f"only newline conventions with a defined registered identity, and "
            f"a CR is refused rather than folded into one")
    return folded


def digest_pair(payload: bytes, where: str = "input") -> Dict[str, object]:
    """Both digests, and which convention the registered identity uses.

    Reporting only one of these is what made the convention ambiguous in the
    first place: a reader could not tell whether a mismatch meant a different
    artifact or a different checkout.
    """
    folded = normalise_newlines(payload, where)
    return {
        "raw_sha256": _sha256(payload),
        "lf_normalized_sha256": _sha256(folded),
        "raw_bytes": len(payload),
        "lf_normalized_bytes": len(folded),
        "had_crlf": payload != folded,
        "registered_identity_uses": "lf_normalized_sha256",
    }


def file_digest_pair(path: str) -> Dict[str, object]:
    with open(path, "rb") as handle:
        return digest_pair(handle.read(), os.path.basename(path))


def frozen_q5d_digests() -> Dict[str, object]:
    """Both digests of the Q5-D module this process actually imported."""
    return file_digest_pair(BJ.__file__)


def assert_frozen_q5d_unchanged() -> Dict[str, object]:
    """The repair is only meaningful against the version that made the bundle.

    The shard folder's name carries `6b098c67df3c`, the first twelve characters
    of the **LF-normalised** digest, so identity is asserted on that and the raw
    digest is reported beside it.  On a CRLF checkout the raw digest differs and
    the registered one does not, which is the whole point of the convention.
    """
    digests = frozen_q5d_digests()
    if digests["lf_normalized_sha256"] != FROZEN_Q5D_SHA256_LF:
        raise RepairError(
            FROZEN_MODULE_MOVED,
            f"the imported Q5-D module normalises to "
            f"{digests['lf_normalized_sha256']}, not the registered "
            f"{FROZEN_Q5D_SHA256_LF} (raw bytes {digests['raw_sha256']}).  The "
            f"null shards were produced by the registered version and may not "
            f"be finalised by another.")
    live = BJ.rule_fingerprint()
    if live != REGISTERED_RULE_FINGERPRINT:
        raise RepairError(
            FROZEN_MODULE_MOVED,
            f"the live rule fingerprint {live!r} is not the registered "
            f"{REGISTERED_RULE_FINGERPRINT!r}")
    return dict(digests, rule_fingerprint=live,
                newline_convention=NEWLINE_CONVENTION)


APPROVAL_BLOCK_START = "# ─── APPROVAL BLOCK START"
APPROVAL_BLOCK_END = "# ─── APPROVAL BLOCK END"


def module_science_digest(path: Optional[str] = None) -> Dict[str, object]:
    """This module's digest with the approval block removed.

    A record inside a file cannot certify that file — so the approval metadata
    is fenced off and everything *else* is hashed.  An execution-enable PR may
    change the fenced block and nothing more, and this digest proves it: it is
    identical before and after such a PR, and it moves the moment any logic
    changes.  That is what lets "the approval only flipped a flag" be a checked
    claim rather than a promise in a commit message.
    """
    with open(path or os.path.abspath(__file__), "rb") as handle:
        text = normalise_newlines(handle.read(), "repair module")
    lines = text.split(b"\n")
    kept: List[bytes] = []
    inside = False
    starts = ends = 0
    for line in lines:
        if line.startswith(APPROVAL_BLOCK_START.encode("utf-8")):
            inside, starts = True, starts + 1
            continue
        if line.startswith(APPROVAL_BLOCK_END.encode("utf-8")):
            inside, ends = False, ends + 1
            continue
        if not inside:
            kept.append(line)
    if starts != 1 or ends != 1:
        raise RepairError(
            EXECUTION_IDENTITY_UNVERIFIED,
            f"the approval block is not delimited exactly once "
            f"({starts} start, {ends} end markers); the science digest would "
            f"not mean what it claims")
    return {"module_science_lf_sha256": _sha256(b"\n".join(kept)),
             "excluded_lines": len(lines) - len(kept),
             "convention": ("LF-normalised digest of the module with the "
                            "approval block excluded, so an enable PR that "
                            "touches only approval metadata leaves it equal")}


def verify_execution_identity(repo_root: str, execution_head: Optional[str],
                             ) -> Dict[str, object]:
    """Is the code on disk the implementation that was approved, and which
    commit is actually running?

    Two separate facts, deliberately not collapsed:

    * **approved implementation** — named by `APPROVED_IMPLEMENTATION_COMMIT`
      and `APPROVED_ARTIFACT_DIGESTS`, both written by a *later* enable PR so
      the record points backwards and is never self-referential;
    * **execution head** — the commit actually checked out, measured from git by
      the notebook and passed in.  A 40-hex string typed into a cell is an
      assertion by whoever typed it, so it is recorded as an observation and
      then checked against the approved digests rather than believed.

    Every clause must hold before any registered asset is opened.
    """
    problems: List[str] = []
    if not APPROVED_IMPLEMENTATION_COMMIT:
        problems.append(
            "no approved implementation commit is recorded; an execution "
            "approval PR records the reviewed commit before a run is possible")
    elif not (isinstance(APPROVED_IMPLEMENTATION_COMMIT, str)
              and len(APPROVED_IMPLEMENTATION_COMMIT) == 40
              and all(c in _HEX for c in APPROVED_IMPLEMENTATION_COMMIT)):
        problems.append(
            f"the approved implementation commit "
            f"{APPROVED_IMPLEMENTATION_COMMIT!r} is not a 40-hex sha")

    if not (isinstance(execution_head, str) and len(execution_head) == 40
            and all(c in _HEX for c in execution_head)):
        problems.append(
            f"execution_head {execution_head!r} is not a 40-hex sha measured "
            f"from git; the module carries no commit of its own to fall back on")

    observed = artifact_identities(repo_root)
    science = module_science_digest(os.path.join(repo_root, MODULE_PATH))
    measured = {
        "spec_lf_sha256": observed["spec"]["lf_normalized_sha256"],
        "notebook_lf_sha256": observed["notebook"]["lf_normalized_sha256"],
        "frozen_q5d_lf_sha256": frozen_q5d_digests()["lf_normalized_sha256"],
        "module_science_lf_sha256": science["module_science_lf_sha256"],
    }
    for field, expected in APPROVED_ARTIFACT_DIGESTS.items():
        if not expected:
            problems.append(f"{field} is not recorded in the approved "
                            f"implementation")
        elif measured.get(field) != expected:
            problems.append(f"{field}: on disk {measured.get(field)} != "
                            f"approved {expected}")
    if problems:
        raise RepairError(
            EXECUTION_IDENTITY_UNVERIFIED,
            "the running code is not verifiably the approved implementation:\n"
            "  " + "\n  ".join(problems))
    return {
        "approved_implementation_commit": APPROVED_IMPLEMENTATION_COMMIT,
        "execution_head": execution_head,
        "head_equals_approved_commit": (
            execution_head == APPROVED_IMPLEMENTATION_COMMIT),
        "approved_artifact_digests": dict(APPROVED_ARTIFACT_DIGESTS),
        "measured_artifact_digests": measured,
        "artifact_identities": observed,
        "module_science_digest": science,
        "self_referential": False,
    }


def artifact_identities(repo_root: str) -> Dict[str, object]:
    """LF-normalised and raw digests of the module, spec and notebook.

    Re-checked after a pinned checkout: knowing the commit is not the same as
    knowing the three files on disk are the ones that commit contains, and a
    dirty working tree is exactly the case a commit pin cannot see.
    """
    out: Dict[str, object] = {}
    for label, relative in (("module", MODULE_PATH), ("spec", SPEC_PATH),
                            ("notebook", NOTEBOOK_PATH)):
        path = os.path.join(repo_root, relative)
        out[label] = dict(file_digest_pair(path), path=relative)
    return out


# ─────────────────────────────────────────────────────────────────────────────
# Type and format checks.  A non-empty string coerced with `str()` is not a
# validated field: `str(None)` is `"None"`, which is truthy and 64 characters
# away from being a digest.
# ─────────────────────────────────────────────────────────────────────────────
_HEX = set("0123456789abcdef")


def is_hex64(value: object) -> bool:
    return (isinstance(value, str) and len(value) == 64
            and all(c in _HEX for c in value))


def is_finite_float(value: object) -> bool:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return False
    return value == value and value not in (float("inf"), float("-inf"))


# ─────────────────────────────────────────────────────────────────────────────
# Drive folder-id bridge.  Every registered artifact is addressed by folder id;
# a mount path is accepted only when it is tied to that id file by file.
# ─────────────────────────────────────────────────────────────────────────────
DRIVE_FOLDER_MIME = "application/vnd.google-apps.folder"
DRIVE_SHORTCUT_MIME = "application/vnd.google-apps.shortcut"
AMBIGUITY_CATEGORIES: Tuple[str, ...] = (
    "duplicate_name", "duplicate_file_id", "missing_file_id", "nameless",
    "subfolder", "shortcut", "trashed", "google_native", "sizeless",
)


class FolderInventoryAdapter(object):
    """The one seam every Drive read goes through.

    A synthetic test can exercise the whole route through this while proving no
    real API was called, and a production implementation is the only thing that
    ever talks to Drive.
    """

    def list_children(self, folder_id: str
                      ) -> Sequence[Mapping[str, object]]:  # pragma: no cover
        raise NotImplementedError


#: Exactly one scope.  A broader credential is not accepted merely because it
#: includes this one: "read-only" would then be a claim the code cannot support.
DRIVE_READONLY_SCOPE = "https://www.googleapis.com/auth/drive.readonly"
#: What the adapter can do, recorded so a reviewer does not have to read it to
#: find out.  `files.list` is the whole surface.
ADAPTER_OPERATIONS: Tuple[str, ...] = ("files.list",)
RUNTIME_DEPENDENCIES: Dict[str, str] = {
    "googleapiclient": "google-api-python-client",
    "google.auth": "google-auth",
}


def check_runtime_dependencies() -> Dict[str, object]:
    """What is importable, before a credential is minted.

    Nothing is installed or upgraded to tidy the record: a version that cannot
    be determined is written as `unavailable`, never guessed.
    """
    import importlib
    out: Dict[str, object] = {}
    for module_name, distribution in RUNTIME_DEPENDENCIES.items():
        try:
            importlib.import_module(module_name)
            present = True
        except Exception:                                # pragma: no cover
            present = False
        version = "unavailable"
        try:                                             # pragma: no cover
            from importlib import metadata
            version = metadata.version(distribution)
        except Exception:
            pass
        out[distribution] = {"importable": present, "version": version}
    return out


class DriveAuthenticator(object):
    """The one seam a credential comes from.

    Authentication lives here rather than in a notebook cell: a cell that built
    its own service would mint a credential the terminal guard never saw, which
    is the guard defeated by convenience.
    """

    def credential(self, scopes: Sequence[str]):         # pragma: no cover
        raise NotImplementedError


class ColabReadOnlyAuthenticator(DriveAuthenticator):    # pragma: no cover
    """Colab's user credential, requested with exactly the read-only scope."""

    def credential(self, scopes: Sequence[str]):
        from google.colab import auth as colab_auth
        import google.auth
        colab_auth.authenticate_user()
        credential, _project = google.auth.default(scopes=list(scopes))
        return credential


def default_service_factory(credential):                 # pragma: no cover
    """A Drive v3 client built on an explicit credential.

    Never a default client: a default client silently adopts an ambient
    credential whose scope nobody checked.
    """
    from googleapiclient.discovery import build
    return build("drive", "v3", credentials=credential,
                 cache_discovery=False)


def audit_credential_scopes(credential) -> Dict[str, object]:
    """What was asked for, what came back, and whether that is exactly one scope.

    A credential whose scopes cannot be observed is not accepted as read-only:
    "read-only" would be an unverifiable claim.  Nothing here records a token,
    a credential body or an authorization header.
    """
    observed = getattr(credential, "scopes", None)
    if observed is None:
        observed_list: List[str] = []
        observable = False
    else:
        observed_list = sorted(str(s) for s in observed)
        observable = True
    return {
        "requested_scopes": [DRIVE_READONLY_SCOPE],
        "observed_scopes": observed_list,
        "scopes_observable": observable,
        "exact_readonly_scope_proven": (observable
                                        and observed_list
                                        == [DRIVE_READONLY_SCOPE]),
        "credential_type": type(credential).__name__,
        "credential_recorded": False,
    }


def build_drive_adapter(approval: Optional[str],
                        authenticator: Optional[DriveAuthenticator] = None,
                        service_factory=None) -> Tuple[FolderInventoryAdapter,
                                                       Dict[str, object]]:
    """Mint a credential, prove its scope, then build the read-only adapter.

    Called **below** the terminal guard and after the dependency check, so an
    unapproved run never reaches an authenticator, a service factory or the
    Drive API.  Order inside is the same principle: the scope is proven before
    a service exists, because a service built on an unaudited credential has
    already had the access this check exists to bound.
    """
    require_execution_approval(approval, "a Drive credential")
    _terminal_execution_guard()
    dependencies = check_runtime_dependencies()
    authenticator = authenticator or ColabReadOnlyAuthenticator()
    factory = service_factory or default_service_factory

    credential = authenticator.credential([DRIVE_READONLY_SCOPE])
    audit = audit_credential_scopes(credential)
    if not audit["exact_readonly_scope_proven"]:
        raise RepairError(
            READONLY_SCOPE_UNPROVEN,
            f"the credential does not carry exactly "
            f"{DRIVE_READONLY_SCOPE!r}: observed {audit['observed_scopes']} "
            f"(observable: {audit['scopes_observable']}).  A broader "
            f"credential is not accepted merely because it includes the scope "
            f"this repair needs.")
    service = factory(credential)
    adapter = GoogleDriveFolderInventory(service)
    audit.update({
        "service_api": "drive", "service_version": "v3",
        "adapter_operations": list(ADAPTER_OPERATIONS),
        "no_write_adapter_methods": True,
        "runtime_dependencies": dependencies,
        "authenticated_below_terminal_guard": True,
    })
    return adapter, audit


class GoogleDriveFolderInventory(FolderInventoryAdapter):   # pragma: no cover
    """Read-only `files.list` over a folder id.  Never a name search.

    Constructed with an explicit service; it does not build a default client,
    because a default client silently adopts an ambient credential whose scope
    nobody checked.
    """

    FIELDS = ("nextPageToken, files(id, name, size, mimeType, trashed, "
              "sha256Checksum, md5Checksum, modifiedTime, shortcutDetails)")

    def __init__(self, service) -> None:
        self._service = service

    def list_children(self, folder_id: str) -> Sequence[Mapping[str, object]]:
        out: List[Mapping[str, object]] = []
        token = None
        while True:
            response = self._service.files().list(
                q=f"'{folder_id}' in parents",
                fields=self.FIELDS, pageSize=1000, pageToken=token,
                includeItemsFromAllDrives=True,
                supportsAllDrives=True).execute()
            out.extend(response.get("files") or [])
            token = response.get("nextPageToken")
            if not token:
                break
        return out


def normalise_child(child: Mapping[str, object]) -> Dict[str, object]:
    """One Drive child, with its size as an int or None — never a guess."""
    size = child.get("size")
    try:
        size_int: Optional[int] = int(size) if size is not None else None
    except (TypeError, ValueError):
        size_int = None
    return {
        "file_id": child.get("id"), "name": child.get("name"),
        "bytes": size_int, "mime_type": child.get("mimeType"),
        "trashed": bool(child.get("trashed")),
        "provider_sha256": child.get("sha256Checksum"),
        "provider_md5": child.get("md5Checksum"),
        "is_shortcut": child.get("mimeType") == DRIVE_SHORTCUT_MIME
        or bool(child.get("shortcutDetails")),
        "is_folder": child.get("mimeType") == DRIVE_FOLDER_MIME,
    }


def inventory_folder(adapter: FolderInventoryAdapter, folder_id: str
                     ) -> Dict[str, object]:
    """Direct children of a folder id, with every ambiguity category counted."""
    children = [normalise_child(c) for c in adapter.list_children(folder_id)]
    names: Dict[str, int] = {}
    ids: Dict[object, int] = {}
    for child in children:
        names[str(child["name"])] = names.get(str(child["name"]), 0) + 1
        ids[child["file_id"]] = ids.get(child["file_id"], 0) + 1
    ambiguity = {
        "duplicate_name": sorted(n for n, c in names.items() if c > 1),
        "duplicate_file_id": sorted(str(i) for i, c in ids.items() if c > 1),
        "missing_file_id": sorted(str(c["name"]) for c in children
                                  if not c["file_id"]),
        "nameless": [str(c["file_id"]) for c in children if not c["name"]],
        "subfolder": sorted(str(c["name"]) for c in children if c["is_folder"]),
        "shortcut": sorted(str(c["name"]) for c in children
                           if c["is_shortcut"]),
        "trashed": sorted(str(c["name"]) for c in children if c["trashed"]),
        "google_native": sorted(
            str(c["name"]) for c in children
            if str(c["mime_type"] or "").startswith("application/vnd.google-apps")
            and not c["is_folder"] and not c["is_shortcut"]),
        "sizeless": sorted(str(c["name"]) for c in children
                           if c["bytes"] is None and not c["is_folder"]),
    }
    return {
        "folder_id": folder_id,
        "method": "files.list by folder id (not a name search)",
        "children": children,
        "child_count": len(children),
        "ambiguity": ambiguity,
        "unambiguous": not any(ambiguity[k] for k in AMBIGUITY_CATEGORIES),
    }


def bridge_mount_to_folder_id(adapter: FolderInventoryAdapter, folder_id: str,
                              mount_dir: str, expected_names: Sequence[str],
                              approval: Optional[str]) -> Dict[str, object]:
    """Tie a mount path to a folder id, file by file, or refuse it.

    A matching folder *name* is never accepted: the whole failure mode this
    guards against is a same-named folder standing in for the registered one.
    So every expected name must be present in the folder-id inventory and on
    the mount with the same size, and with every provider checksum the API
    actually supplied — a checksum it did not supply is recorded as
    unavailable, never guessed, and never treated as a match.
    """
    require_execution_approval(approval, f"folder id {folder_id}")
    _terminal_execution_guard()

    inventory = inventory_folder(adapter, folder_id)
    if not inventory["unambiguous"]:
        raise RepairError(
            INPUT_UNQUALIFIED,
            f"the inventory of folder id {folder_id} is ambiguous: "
            f"{ {k: v for k, v in dict(inventory['ambiguity']).items() if v} }")
    if not os.path.isdir(mount_dir):
        raise RepairError(
            INPUT_UNQUALIFIED,
            f"no mounted directory at {mount_dir!r} to bridge to folder id "
            f"{folder_id}")

    by_name = {str(c["name"]): c for c in inventory["children"]}
    rows: List[Dict[str, object]] = []
    problems: List[str] = []
    #: The bytes the bridge itself read.  Everything downstream judges *these*
    #: — a later read is a different moment, and on a Drive mount that is not
    #: hypothetical.  A re-read still happens, to detect the substitution
    #: rather than merely avoid it.
    bridged_bytes: Dict[str, bytes] = {}
    for name in expected_names:
        row: Dict[str, object] = {"name": name}
        child = by_name.get(name)
        path = os.path.join(mount_dir, name)
        if child is None:
            problems.append(f"{name}: not a child of folder id {folder_id}")
            rows.append(dict(row, in_inventory=False))
            continue
        if not os.path.isfile(path):
            problems.append(f"{name}: in the inventory but not on the mount")
            rows.append(dict(row, in_inventory=True, on_mount=False))
            continue
        with open(path, "rb") as handle:
            body = handle.read()
        observed = _sha256(body)
        matched_on: List[str] = ["name"]
        row.update({
            "in_inventory": True, "on_mount": True,
            "file_id": child["file_id"],
            "inventory_bytes": child["bytes"], "mount_bytes": len(body),
            "mount_sha256": observed,
            "provider_sha256": child["provider_sha256"] or "unavailable",
            "provider_md5": child["provider_md5"] or "unavailable",
        })
        if child["bytes"] != len(body):
            problems.append(
                f"{name}: inventory says {child['bytes']} B, mount has "
                f"{len(body)} B")
        else:
            matched_on.append("size")
        if child["provider_sha256"]:
            if str(child["provider_sha256"]).lower() != observed:
                problems.append(
                    f"{name}: provider sha256 {child['provider_sha256']} != "
                    f"mount {observed}")
            else:
                matched_on.append("provider_sha256")
        if child["provider_md5"]:
            observed_md5 = hashlib.md5(body).hexdigest()
            if str(child["provider_md5"]).lower() != observed_md5:
                problems.append(
                    f"{name}: provider md5 {child['provider_md5']} != mount "
                    f"{observed_md5}")
            else:
                matched_on.append("provider_md5")
        row["matched_on"] = matched_on
        rows.append(row)

        bridged_bytes[name] = body

    unexpected = sorted(set(by_name) - set(expected_names))
    if unexpected:
        problems.append(
            f"folder id {folder_id} holds {len(unexpected)} unexpected "
            f"children: {unexpected[:5]}")
    if problems:
        raise RepairError(
            INPUT_UNQUALIFIED,
            f"the mount at {mount_dir!r} could not be tied to folder id "
            f"{folder_id}; a same-named folder is never accepted as a "
            f"substitute:\n  " + "\n  ".join(problems[:10]))
    return {
        "folder_id": folder_id,
        "mount": os.path.basename(os.path.normpath(mount_dir)),
        "method": inventory["method"],
        "child_count": inventory["child_count"],
        "ambiguity": inventory["ambiguity"],
        "files": rows,
        "checksum_coverage": {
            "provider_sha256": sum(1 for r in rows
                                   if "provider_sha256" in (r.get("matched_on")
                                                            or [])),
            "provider_md5": sum(1 for r in rows
                                if "provider_md5" in (r.get("matched_on")
                                                      or [])),
            "size_and_name_only": sum(
                1 for r in rows
                if set(r.get("matched_on") or []) == {"name", "size"}),
        },
        "bridged": True,
        "bytes_captured": len(bridged_bytes),
    }, bridged_bytes


def assert_bytes_unmoved_since_bridge(mount_dir: str, names: Sequence[str],
                                      bridged: Mapping[str, bytes]
                                      ) -> Dict[str, object]:
    """Re-read and compare against what the bridge captured.

    Using the bridged bytes downstream already prevents judging one file and
    publishing another.  This *detects* the substitution as well, because a
    file that changed between the folder-id bridge and the judgement is a
    finding — a same-size replacement would otherwise pass silently, and
    silence is exactly what makes it dangerous.
    """
    problems: List[str] = []
    for name in names:
        path = os.path.join(mount_dir, name)
        try:
            with open(path, "rb") as handle:
                now = handle.read()
        except OSError as error:
            problems.append(f"{name}: unreadable after the bridge ({error})")
            continue
        if _sha256(now) != _sha256(bridged[name]):
            problems.append(
                f"{name}: {_sha256(now)} now, {_sha256(bridged[name])} when "
                f"the folder id was bridged "
                f"({len(now)} B vs {len(bridged[name])} B)")
    if problems:
        raise RepairError(
            BYTES_MOVED_AFTER_BRIDGE,
            f"bytes under {mount_dir!r} changed after they were tied to their "
            f"folder id:\n  " + "\n  ".join(problems[:10]))
    return {"checked": len(names), "ok": True}


def bridge_runs_parent(adapter: FolderInventoryAdapter, runs_parent_dir: str,
                       source_dir: str, target_dir: str,
                       approval: Optional[str],
                       parent_folder_id: str = "",
                       source_folder_id: str = "") -> Dict[str, object]:
    """Prove the write destination is the registered parent, before any mkdir.

    A mount path is a name, and a name is exactly what this module refuses to
    treat as identity everywhere else — so the parent gets the same treatment
    as the inputs.  The link between the two worlds is the source bundle: it
    has a registered folder id *and* a mount path, so if the registered source
    id is a direct child of the registered parent id, and the source mount's
    parent directory is the runs-parent mount, then the runs-parent mount is
    the registered parent's mount.  Injecting some other directory under the
    same `RUNS_PARENT_DIR` string breaks the second half.
    """
    require_execution_approval(approval, f"runs parent {runs_parent_dir!r}")
    _terminal_execution_guard()
    parent_folder_id = parent_folder_id or RUNS_PARENT_FOLDER_ID
    source_folder_id = source_folder_id or SOURCE_BUNDLE_FOLDER_ID

    problems: List[str] = []
    inventory = inventory_folder(adapter, parent_folder_id)
    children = [c for c in inventory["children"]
                if str(c["file_id"]) == source_folder_id]
    if len(children) != 1:
        problems.append(
            f"the registered source folder id {source_folder_id} is not a "
            f"single direct child of the registered parent id "
            f"{parent_folder_id} (found {len(children)})")
    elif not children[0]["is_folder"] or children[0]["trashed"] \
            or children[0]["is_shortcut"]:
        problems.append(
            f"the source child of {parent_folder_id} is not a live folder "
            f"(folder={children[0]['is_folder']} "
            f"trashed={children[0]['trashed']} "
            f"shortcut={children[0]['is_shortcut']})")

    if not runs_parent_dir or not os.path.isdir(runs_parent_dir):
        problems.append(f"the runs parent mount {runs_parent_dir!r} is not a "
                        f"directory")
    else:
        source_parent = os.path.dirname(_real(os.path.normpath(source_dir)))
        if source_parent != _real(runs_parent_dir):
            problems.append(
                f"the source bundle's mount parent {source_parent!r} is not "
                f"the runs parent mount {_real(runs_parent_dir)!r}; the path "
                f"given cannot be the registered parent id's mount")
        target_parent = os.path.dirname(_real(os.path.normpath(target_dir)))
        if target_parent != _real(runs_parent_dir):
            problems.append(
                f"the target's parent {target_parent!r} is not the runs "
                f"parent mount")
        walk = os.path.normpath(runs_parent_dir)
        while True:
            if os.path.lexists(walk) and _is_link_like(walk):
                problems.append(f"{walk!r} is a symlink or reparse point")
            nxt = os.path.dirname(walk)
            if nxt == walk:
                break
            walk = nxt

    if problems:
        raise RepairError(
            TARGET_UNSAFE,
            "the runs parent could not be tied to its registered folder id:\n"
            "  " + "\n  ".join(problems))
    return {
        "parent_folder_id": parent_folder_id,
        "source_folder_id": source_folder_id,
        "source_is_direct_child": True,
        "runs_parent_mount": os.path.basename(
            os.path.normpath(runs_parent_dir)),
        "source_mount_parent_matches": True,
        "target_parent_matches": True,
        "link_like_component": False,
    }


def resolve_output_folder_id(adapter: FolderInventoryAdapter,
                             parent_folder_id: str, name: str,
                             approval: Optional[str],
                             attempts: int = 5, sleeper=None,
                             delay_seconds: float = 2.0) -> Dict[str, object]:
    """The new folder's own Drive id, with a bounded read-only retry.

    Drive is eventually consistent: a folder that exists on the mount can be
    briefly invisible to `files.list`.  That is not a reason to give the run a
    pass, and it is not a reason to create a second folder either — so this
    retries a few times, read-only, and then stops.

    Every attempt is a list call and nothing else.  Nothing is created, renamed
    or deleted here under any outcome.
    """
    require_execution_approval(approval, f"folder id {parent_folder_id}")
    _terminal_execution_guard()
    import time
    sleeper = sleeper or time.sleep
    seen: List[Dict[str, object]] = []
    for attempt in range(1, max(1, int(attempts)) + 1):
        inventory = inventory_folder(adapter, parent_folder_id)
        matches = [c for c in inventory["children"]
                   if str(c["name"]) == name and c["is_folder"]
                   and not c["trashed"] and not c["is_shortcut"]]
        seen.append({"attempt": attempt, "matches": len(matches)})
        if len(matches) == 1:
            return {"folder_id": matches[0]["file_id"], "name": name,
                    "parent_folder_id": parent_folder_id,
                    "attempts": attempt, "history": seen,
                    "method": inventory["method"], "resolved": True}
        if len(matches) > 1:
            raise RepairError(
                OUTPUT_FOLDER_ID_UNRESOLVED,
                f"{len(matches)} folders named {name!r} under parent id "
                f"{parent_folder_id}; a result that cannot be named by one id "
                f"cannot be accepted")
        if attempt < max(1, int(attempts)):
            sleeper(delay_seconds)
    raise RepairError(
        OUTPUT_FOLDER_ID_UNRESOLVED,
        f"the corrective folder {name!r} was written and verified but its "
        f"Drive folder id did not become visible under parent id "
        f"{parent_folder_id} within {attempts} read-only attempts.  The output "
        f"is preserved and unregistered; re-resolve it with "
        f"reconcile_output_folder_id() rather than writing another folder.")


def reconcile_output_folder_id(adapter: FolderInventoryAdapter,
                               target_dir: str, snapshot_digests:
                               Mapping[str, str], npz_sha256: str,
                               approval: Optional[str],
                               parent_folder_id: str = "",
                               attempts: int = 5, sleeper=None
                               ) -> Dict[str, object]:
    """Re-resolve a preserved output's folder id, read-only, changing nothing.

    For the case `resolve_output_folder_id()` gave up on.  It re-checks the
    parent folder id, the exact folder name, the exact twelve-file listing and
    every digest before returning an id, because an id attached to a folder
    nobody re-verified would be worse than no id at all.  It never writes,
    never creates a second folder, and never edits the existing one.
    """
    require_execution_approval(approval, f"reconciling {target_dir!r}")
    _terminal_execution_guard()
    name = os.path.basename(os.path.normpath(target_dir))
    listing = _listing(target_dir)
    problems: List[str] = []
    if listing != sorted(BUNDLE_FILES):
        problems.append(f"listing {listing} != the twelve "
                        f"{sorted(BUNDLE_FILES)}")
    expected = dict(snapshot_digests)
    expected[MISSING_ARTIFACT] = npz_sha256
    observed: Dict[str, str] = {}
    for entry in listing:
        try:
            with open(os.path.join(target_dir, entry), "rb") as handle:
                observed[entry] = _sha256(handle.read())
        except OSError as error:                         # pragma: no cover
            problems.append(f"{entry}: unreadable ({error})")
            continue
        if entry in expected and observed[entry] != expected[entry]:
            problems.append(f"{entry}: {observed[entry]} != expected "
                            f"{expected[entry]}")
    if problems:
        raise RepairError(
            OUTPUT_FOLDER_ID_UNRESOLVED,
            "the preserved output no longer matches what was written, so its "
            "folder id may not be resolved:\n  " + "\n  ".join(problems[:10]),
            incomplete_directory=target_dir, listing=listing)
    resolved = resolve_output_folder_id(
        adapter, parent_folder_id or RUNS_PARENT_FOLDER_ID, name, approval,
        attempts=attempts, sleeper=sleeper)
    return {"reconciled": True, "folder_id": resolved["folder_id"],
            "name": name, "listing": listing, "observed": observed,
            "attempts": resolved["attempts"],
            "wrote_nothing": True}


def confirm_folder_id_of_child(adapter: FolderInventoryAdapter,
                               parent_folder_id: str, name: str,
                               approval: Optional[str]) -> Dict[str, object]:
    """The new corrective folder's own Drive id, read back read-only.

    A result must be identifiable afterwards by id.  Picking it later by folder
    name is the same substitution risk this module refuses everywhere else.
    """
    require_execution_approval(approval, f"folder id {parent_folder_id}")
    _terminal_execution_guard()
    inventory = inventory_folder(adapter, parent_folder_id)
    matches = [c for c in inventory["children"]
               if str(c["name"]) == name and c["is_folder"]
               and not c["trashed"] and not c["is_shortcut"]]
    if len(matches) != 1:
        raise RepairError(
            INPUT_UNQUALIFIED,
            f"expected exactly one folder named {name!r} under parent id "
            f"{parent_folder_id}, found {len(matches)}")
    return {"folder_id": matches[0]["file_id"], "name": name,
            "parent_folder_id": parent_folder_id,
            "method": inventory["method"]}


# ─────────────────────────────────────────────────────────────────────────────
# Identity, anchored on the folder-id-verified bundle manifest
# ─────────────────────────────────────────────────────────────────────────────
IDENTITY_FIELDS: Tuple[str, ...] = ("split", "code_sha256",
                                    "rule_fingerprint", "input_digest")


def identity_from_manifest(manifest: Mapping[str, object]) -> Dict[str, str]:
    """What the shards must match — validated, not merely non-empty.

    The manifest is trusted only because the bytes it was parsed from are tied
    to the registered folder id by :func:`bridge_mount_to_folder_id`, and only
    for fields that also agree with a registered constant.  `input_digest` has
    no registered counterpart in this repository, so it is checked for format
    and for shard agreement and that limit is recorded rather than papered over.
    """
    problems: List[str] = []
    values: Dict[str, str] = {}
    for field in IDENTITY_FIELDS:
        value = manifest.get(field)
        if not isinstance(value, str) or not value:
            problems.append(f"{field}: {value!r} is not a non-empty string")
            continue
        values[field] = value
    if values.get("split") != REGISTERED_SPLIT:
        problems.append(
            f"split: {values.get('split')!r} is not the registered "
            f"{REGISTERED_SPLIT!r}")
    for field in ("code_sha256", "rule_fingerprint", "input_digest"):
        if field in values and not is_hex64(values[field]):
            problems.append(f"{field}: {values[field]!r} is not 64 hex digits")
    if values.get("code_sha256") not in (None, FROZEN_Q5D_SHA256_LF):
        problems.append(
            f"code_sha256: {values.get('code_sha256')} is not the registered "
            f"{FROZEN_Q5D_SHA256_LF}")
    if values.get("rule_fingerprint") not in (None,
                                              REGISTERED_RULE_FINGERPRINT):
        problems.append(
            f"rule_fingerprint: {values.get('rule_fingerprint')} is not the "
            f"registered {REGISTERED_RULE_FINGERPRINT}")
    if (REGISTERED_INPUT_DIGEST is not None
            and values.get("input_digest") != REGISTERED_INPUT_DIGEST):
        problems.append(
            f"input_digest: {values.get('input_digest')} is not the registered "
            f"{REGISTERED_INPUT_DIGEST}")
    if problems:
        raise RepairError(
            INPUT_UNQUALIFIED,
            "the bundle manifest cannot anchor this repair:\n  "
            + "\n  ".join(problems))
    return values


class _UnreadMapping(dict):
    """An empty mapping that refuses to be read.

    It makes "the finaliser never touches the join inputs" a fact the tests
    observe rather than a claim in a comment: if anything on the path reaches
    for a record, this raises instead of quietly returning nothing.
    """

    def __getitem__(self, key):
        raise AssertionError(
            f"the repair path read join input {key!r}; finalisation is "
            f"supposed to need only the shard identity")

    def get(self, key, default=None):
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
    module, so a rule that had moved is caught here rather than being read out
    of the manifest and agreeing with itself.
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
# Shard qualification — exact set, exact schema, structured failures
# ─────────────────────────────────────────────────────────────────────────────
def validate_shard_schema(payload: object, name: str,
                          identity: Mapping[str, str],
                          expected_range: Tuple[int, int]) -> List[str]:
    """Types, formats and full digests — not "is it truthy".

    `str(x)` on a missing field yields `"None"`, which is a non-empty string and
    would pass a presence check while carrying no identity at all.  Every field
    is therefore checked for its type and its shape.
    """
    problems: List[str] = []
    if not isinstance(payload, dict):
        return [f"{name}: top level is {type(payload).__name__}, not an object"]

    start, end = expected_range
    for field, want in (("replicate_start", start), ("replicate_end", end)):
        value = payload.get(field)
        if isinstance(value, bool) or not isinstance(value, int):
            problems.append(f"{name}: {field} is {value!r}, not an int")
        elif value != want:
            problems.append(f"{name}: {field} is {value}, expected {want}")

    version = payload.get("null_runner_version")
    if isinstance(version, bool) or not isinstance(version, int):
        problems.append(f"{name}: null_runner_version is {version!r}, not an int")
    elif version != REGISTERED_NULL_RUNNER_VERSION:
        problems.append(
            f"{name}: null_runner_version {version} != registered "
            f"{REGISTERED_NULL_RUNNER_VERSION}")

    seed = payload.get("master_seed")
    if isinstance(seed, bool) or not isinstance(seed, int):
        problems.append(f"{name}: master_seed is {seed!r}, not an int")
    elif seed != REGISTERED_MASTER_SEED:
        problems.append(f"{name}: master_seed {seed} != registered "
                        f"{REGISTERED_MASTER_SEED}")

    if payload.get("split") != REGISTERED_SPLIT:
        problems.append(f"{name}: split {payload.get('split')!r} != registered "
                        f"{REGISTERED_SPLIT!r}")

    families = payload.get("families")
    if not isinstance(families, list) or [str(f) for f in families] != \
            list(REGISTERED_FAMILIES):
        problems.append(f"{name}: families {families!r} != registered "
                        f"{list(REGISTERED_FAMILIES)}")

    for field, registered in (("code_sha256", FROZEN_Q5D_SHA256_LF),
                              ("rule_fingerprint",
                               REGISTERED_RULE_FINGERPRINT),
                              ("input_digest", REGISTERED_INPUT_DIGEST)):
        value = payload.get(field)
        if not is_hex64(value):
            problems.append(f"{name}: {field} {value!r} is not 64 hex digits")
            continue
        if registered is not None and value != registered:
            problems.append(f"{name}: {field} {value} != registered "
                            f"{registered}")
        if identity.get(field) and value != identity[field]:
            problems.append(
                f"{name}: {field} {value} != the manifest's {identity[field]}")

    if not is_hex64(payload.get("digest")):
        problems.append(f"{name}: digest {payload.get('digest')!r} is not "
                        f"64 hex digits")

    span = end - start
    arrays = payload.get("j")
    if not isinstance(arrays, dict):
        problems.append(f"{name}: 'j' is {type(arrays).__name__}, not an object")
    else:
        if sorted(arrays) != sorted(REGISTERED_FAMILIES):
            problems.append(f"{name}: 'j' has {sorted(arrays)}, expected "
                            f"{sorted(REGISTERED_FAMILIES)}")
        for family in REGISTERED_FAMILIES:
            values = arrays.get(family)
            if not isinstance(values, list):
                problems.append(f"{name}: j[{family!r}] is not a list")
            elif len(values) != span:
                problems.append(f"{name}: j[{family!r}] has {len(values)} "
                                f"values for a {span}-replicate shard")
            elif not all(is_finite_float(v) for v in values):
                problems.append(f"{name}: j[{family!r}] holds a non-finite or "
                                f"non-numeric value")
    maxima = payload.get("j_null_max")
    if not isinstance(maxima, list):
        problems.append(f"{name}: j_null_max is not a list")
    elif len(maxima) != span:
        problems.append(f"{name}: j_null_max has {len(maxima)} values for a "
                        f"{span}-replicate shard")
    elif not all(is_finite_float(v) for v in maxima):
        problems.append(f"{name}: j_null_max holds a non-finite value")
    return problems


def expected_shard_set() -> Dict[str, Tuple[int, int]]:
    """Filename → range, for exactly the preregistered 100 shards."""
    return {BJ.shard_filename(start, end): (start, end)
            for start, end in EXPECTED_SHARD_RANGES}


def coverage_report(ranges: Sequence[Tuple[int, int]], total: int
                    ) -> Dict[str, object]:
    """Gaps and overlaps as ranges, not as a yes/no."""
    seen: Dict[int, Tuple[int, int]] = {}
    overlaps: List[Dict[str, object]] = []
    for start, end in sorted(ranges):
        for replicate in range(start, end):
            if replicate in seen:
                overlaps.append({"replicate": replicate,
                                 "in": [list(seen[replicate]), [start, end]]})
            else:
                seen[replicate] = (start, end)
    missing = [b for b in range(int(total)) if b not in seen]
    beyond = sorted(b for b in seen if b >= int(total))
    return {
        "ranges": [list(r) for r in sorted(ranges)],
        "covered": len(seen), "expected": int(total),
        "missing_count": len(missing), "missing_first": missing[:5],
        "overlap_count": len(overlaps), "overlap_first": overlaps[:5],
        "beyond_total": beyond[:5],
        "ok": (not missing and not overlaps and not beyond
               and len(seen) == int(total)),
    }


def qualify_shards(shard_dir: str, manifest: Mapping[str, object],
                   approval: Optional[str],
                   adapter: Optional[FolderInventoryAdapter] = None,
                   folder_id: str = SHARD_FOLDER_ID,
                   total: int = N_REPLICATES,
                   expected: Optional[Mapping[str, Tuple[int, int]]] = None
                   ) -> Dict[str, object]:
    """Read the shards and prove they may be finalised, or stop.

    Every clause the spec fixes, each reported with what it observed rather
    than a bare pass — a qualification whose evidence is a boolean cannot be
    audited afterwards.  A malformed or unparseable shard becomes a problem in
    this report, never a raw `JSONDecodeError` escaping to the caller: the
    thing this function exists to detect must not arrive as a crash.
    """
    require_execution_approval(approval, f"the null shards at {shard_dir!r}")
    _terminal_execution_guard()

    identity = identity_from_manifest(manifest)
    context = identity_only_context(identity)
    wanted = dict(expected if expected is not None else expected_shard_set())

    bridge: Optional[Dict[str, object]] = None
    bridged: Dict[str, bytes] = {}
    if adapter is not None:
        bridge, bridged = bridge_mount_to_folder_id(
            adapter, folder_id, shard_dir, sorted(wanted), approval)
        # Detect a substitution as well as avoid it: the judgement below reads
        # the bridged bytes, and this proves nothing moved underneath them.
        assert_bytes_unmoved_since_bridge(shard_dir, sorted(wanted), bridged)

    if not os.path.isdir(shard_dir):
        raise RepairError(INPUT_UNQUALIFIED,
                          f"no shard directory at {shard_dir!r}")
    entries = sorted(os.listdir(shard_dir))
    on_disk = sorted(n for n in entries
                     if os.path.isfile(os.path.join(shard_dir, n)))
    subdirs = sorted(n for n in entries if n not in on_disk)

    problems: List[str] = []
    if subdirs:
        problems.append(f"the shard folder holds {len(subdirs)} "
                        f"subdirectories or non-files: {subdirs[:5]}")
    missing_files = [n for n in sorted(wanted) if n not in on_disk]
    extra_files = [n for n in on_disk if n not in wanted]
    if missing_files:
        problems.append(f"{len(missing_files)} preregistered shard files are "
                        f"missing: {missing_files[:5]}")
    if extra_files:
        problems.append(f"{len(extra_files)} unexpected files in the shard "
                        f"folder: {extra_files[:5]}")
    if len(on_disk) != len(wanted):
        problems.append(f"{len(on_disk)} files where the preregistered set is "
                        f"exactly {len(wanted)}")

    shards: Dict[Tuple[int, int], Dict[str, object]] = {}
    per_shard: List[Dict[str, object]] = []
    for name in sorted(set(wanted) & set(on_disk)):
        path = os.path.join(shard_dir, name)
        expected_range = wanted[name]
        try:
            if name in bridged:
                # The bridged bytes are the authoritative ones; parsing them
                # rather than re-opening keeps judgement and folder-id identity
                # over the same snapshot.
                raw = json.loads(bridged[name].decode("utf-8"))
            else:
                with open(path, encoding="utf-8") as handle:
                    raw = json.load(handle)
        except (ValueError, UnicodeDecodeError, OSError) as error:
            problems.append(f"{name}: unreadable or malformed JSON ({error})")
            per_shard.append({"file": name, "readable": False})
            continue

        schema_problems = validate_shard_schema(raw, name, identity,
                                                expected_range)
        problems.extend(schema_problems)
        if schema_problems:
            per_shard.append({"file": name, "readable": True,
                              "schema_problems": schema_problems})
            continue

        try:
            recomputed = BJ.shard_digest(raw)
        except BJ.NullShardError as error:
            problems.append(f"{name}: cannot digest ({error})")
            continue
        if recomputed != raw.get("digest"):
            problems.append(f"{name}: fails its own digest "
                            f"({str(raw.get('digest'))[:16]}... != "
                            f"{recomputed[:16]}...)")
            per_shard.append({"file": name, "readable": True,
                              "digest_verified": False})
            continue

        identity_problems = BJ.verify_null_shard(raw, context)
        problems.extend(f"{name}: {p}" for p in identity_problems)
        key = (int(raw["replicate_start"]), int(raw["replicate_end"]))
        if key in shards:
            problems.append(f"{name}: a second shard claims {list(key)}")
        shards[key] = raw
        per_shard.append({
            "file": name, "readable": True, "digest_verified": True,
            "replicate_start": key[0], "replicate_end": key[1],
            "digest": raw["digest"], "schema_problems": [],
            "identity_problems": list(identity_problems),
        })

    coverage = coverage_report(list(shards), total)
    if not coverage["ok"]:
        problems.append(
            f"replicate coverage is not exactly 0..{int(total) - 1}: "
            f"{coverage['missing_count']} missing, "
            f"{coverage['overlap_count']} overlapping")

    report: Dict[str, object] = {
        "shard_dir": os.path.basename(os.path.normpath(shard_dir)),
        "folder_id": folder_id,
        "folder_id_bridge": bridge,
        "expected_count": len(wanted),
        "observed_file_count": len(on_disk),
        "expected_first": sorted(wanted)[0] if wanted else None,
        "expected_last": sorted(wanted)[-1] if wanted else None,
        "missing_files": missing_files, "extra_files": extra_files,
        "subdirectories": subdirs,
        "identity_anchor": "folder-id-verified bundle manifest.json",
        "identity": dict(identity),
        "registered_input_digest": REGISTERED_INPUT_DIGEST,
        "input_digest_registration": (
            "no repo-side registered value; checked for 64-hex format and for "
            "agreement between shards and the folder-id-verified manifest"),
        "live_rule_fingerprint": context.rule_fingerprint,
        "coverage": coverage,
        "per_shard": per_shard,
        "problems": problems,
        "qualified": not problems,
    }
    if problems:
        raise RepairError(
            INPUT_UNQUALIFIED,
            f"{len(problems)} problem(s) over {len(on_disk)} files; the first "
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

    The maximum is taken over **families**, then written under whichever member
    name `MEMBER_NAME_BY_FAMILY` gives, so renaming a member cannot change
    which numbers the relation is computed from.
    """
    families = BJ.finalize_null_shards(shards, context, total=total)
    arrays: Dict[str, List[float]] = {}
    for family in REGISTERED_FAMILIES:
        arrays[MEMBER_NAME_BY_FAMILY[family]] = list(families[family])
    arrays[MAX_MEMBER_NAME] = [
        max(families[f][b] for f in REGISTERED_FAMILIES)
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
    ours = list(arrays[MAX_MEMBER_NAME])
    theirs = null_summary.get("j_null_max")
    if not isinstance(theirs, list):
        return {"n_reconstructed": len(ours), "n_summary": 0,
                "identical": False,
                "first_difference": {"detail": f"summary j_null_max is "
                                               f"{type(theirs).__name__}"},
                "summary_replicates": null_summary.get("replicates"),
                "summary_rule_fingerprint": null_summary.get(
                    "rule_fingerprint")}
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
# NPY / NPZ.  Written explicitly, then verified twice: once by an independent
# reader and once — mandatorily, in production — by numpy itself.
# ─────────────────────────────────────────────────────────────────────────────
NPY_MAGIC = b"\x93NUMPY"
NPY_VERSION = (1, 0)
NPY_DTYPE = "<f8"
#: A fixed ZIP timestamp, so the same arrays always produce the same bytes.
ZIP_TIMESTAMP = (1980, 1, 1, 0, 0, 0)


def npy_bytes(values: Sequence[float]) -> bytes:
    """One 1-D float64 array in NPY v1.0 — the format `numpy.save` writes."""
    header = ("{'descr': '%s', 'fortran_order': False, 'shape': (%d,), }"
              % (NPY_DTYPE, len(values)))
    prefix = len(NPY_MAGIC) + 2 + 2
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

    Deliberately strict: an object array is exactly what `allow_pickle=False`
    exists to reject, and this reader cannot represent one at all.
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
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_STORED) as archive:
        for name in names:
            info = zipfile.ZipInfo(f"{name}.npy", date_time=ZIP_TIMESTAMP)
            info.compress_type = zipfile.ZIP_STORED
            archive.writestr(info, npy_bytes(arrays[name]))
    return buffer.getvalue()


def npz_member_names(blob: bytes) -> List[str]:
    """Raw ZIP member names, duplicates included.

    A ZIP can legally carry two entries with the same name, and a mapping-based
    reader silently keeps one of them — so duplicates have to be detected here,
    on the list, before anything collapses it into a dict.
    """
    with zipfile.ZipFile(io.BytesIO(blob)) as archive:
        return list(archive.namelist())


def read_npz_bytes(blob: bytes) -> Dict[str, Tuple[str, Tuple[int, ...],
                                                   List[float]]]:
    """Every member of an NPZ, parsed without numpy."""
    out: Dict[str, Tuple[str, Tuple[int, ...], List[float]]] = {}
    with zipfile.ZipFile(io.BytesIO(blob)) as archive:
        for name in archive.namelist():
            if not name.endswith(".npy"):
                raise RepairError(
                    NPZ_CONTRACT_FAILED,
                    f"the NPZ holds a non-array member {name!r}")
            out[name[:-4]] = read_npy_bytes(archive.read(name))
    return out


def numpy_verify_npz(blob: bytes,
                     expected: Mapping[str, Sequence[float]],
                     required: bool) -> Dict[str, object]:
    """Load the produced bytes with numpy and `allow_pickle=False`, for real.

    This is a call, not a claim.  An earlier version of this module reported a
    hard-coded `allow_pickle_false_readable: True`, which is a constant dressed
    as a measurement: it would have kept saying True for a file numpy could not
    open.  In production `required` is True and a missing numpy is a stop,
    because the artifact is about to be published and "probably loadable" is
    not a standard.
    """
    try:
        import numpy
    except ImportError as error:
        if required:
            raise RepairError(
                NUMPY_UNAVAILABLE,
                f"numpy is required to verify the NPZ before publishing it "
                f"({error}); the independent reader is a cross-check, not a "
                f"substitute")
        return {"ran": False, "available": False,
                "reason": "numpy is absent and this call did not require it"}
    problems: List[str] = []
    with numpy.load(io.BytesIO(blob), allow_pickle=False) as loaded:
        names = sorted(loaded.files)
        if names != sorted(NPZ_ARRAYS):
            problems.append(f"numpy sees {names}, expected "
                            f"{sorted(NPZ_ARRAYS)}")
        per_array: Dict[str, object] = {}
        for name in sorted(set(NPZ_ARRAYS) & set(loaded.files)):
            array = loaded[name]
            dtype = str(array.dtype)
            shape = list(array.shape)
            finite = bool(numpy.isfinite(array).all())
            values = array.tolist()
            if dtype != "float64":
                problems.append(f"{name}: numpy dtype {dtype}")
            if not finite:
                problems.append(f"{name}: numpy found a non-finite value")
            if name in expected and values != list(expected[name]):
                problems.append(f"{name}: numpy values differ from the "
                                f"reconstructed array")
            per_array[name] = {"dtype": dtype, "shape": shape,
                               "finite": finite}
    return {"ran": True, "available": True, "numpy_version": numpy.__version__,
            "allow_pickle": False, "arrays": per_array,
            "problems": problems, "ok": not problems}


def verify_npz_contract(blob: bytes,
                        expected_j_null_max: Optional[Sequence[float]] = None,
                        total: int = N_REPLICATES,
                        reconstructed: Optional[
                            Mapping[str, Sequence[float]]] = None,
                        require_numpy: bool = False) -> Dict[str, object]:
    """Every clause of the spec's NPZ contract, checked by reading the bytes.

    Two independent readers: this module's parser, and numpy itself with
    `allow_pickle=False`.  Reading the bytes back matters — verifying the values
    that were *passed in* checks the caller's variables, not the file that will
    be published.
    """
    problems: List[str] = []

    raw_names = npz_member_names(blob)
    duplicates = sorted({n for n in raw_names if raw_names.count(n) > 1})
    if duplicates:
        problems.append(f"the NPZ has duplicate member names: {duplicates}")
    expected_members = sorted(f"{n}.npy" for n in NPZ_ARRAYS)
    if sorted(raw_names) != expected_members:
        problems.append(f"members {sorted(raw_names)}, expected "
                        f"{expected_members}")

    members = read_npz_bytes(blob)
    per_array: Dict[str, object] = {}
    for name in sorted(set(NPZ_ARRAYS) & set(members)):
        descr, dims, values = members[name]
        finite = all(is_finite_float(v) for v in values)
        if descr != NPY_DTYPE:
            problems.append(f"{name}: dtype {descr!r}")
        if dims != (int(total),):
            problems.append(f"{name}: shape {dims}, expected ({int(total)},)")
        if not finite:
            problems.append(f"{name}: holds a non-finite value")
        per_array[name] = {"dtype": descr, "shape": list(dims),
                           "finite": finite, "n": len(values)}

    family_members = [MEMBER_NAME_BY_FAMILY[f] for f in REGISTERED_FAMILIES]
    if all(n in members for n in family_members + [MAX_MEMBER_NAME]):
        maxima = members[MAX_MEMBER_NAME][2]
        shortest = min(len(members[n][2]) for n in family_members)
        mismatched = [b for b in range(min(len(maxima), shortest))
                      if maxima[b] != max(members[n][2][b]
                                          for n in family_members)]
        if mismatched:
            problems.append(
                f"{MAX_MEMBER_NAME} is not the family maximum at "
                f"{len(mismatched)} replicates (first: {mismatched[:5]})")
        per_array["max_is_family_max"] = not mismatched

    if expected_j_null_max is not None and MAX_MEMBER_NAME in members:
        ours = members[MAX_MEMBER_NAME][2]
        theirs = list(expected_j_null_max)
        differing = [b for b in range(min(len(ours), len(theirs)))
                     if ours[b] != theirs[b]]
        if differing or len(ours) != len(theirs):
            problems.append(
                f"{MAX_MEMBER_NAME} differs from the expected vector at "
                f"{len(differing)} replicates (first: {differing[:5]}); "
                f"lengths {len(ours)} vs {len(theirs)}")

    numpy_check = numpy_verify_npz(blob, reconstructed or {}, require_numpy)
    if numpy_check.get("ran") and not numpy_check.get("ok"):
        problems.extend(f"numpy: {p}" for p in numpy_check["problems"])

    return {
        "ok": not problems,
        "sha256": _sha256(blob),
        "bytes": len(blob),
        "members": sorted(raw_names),
        "duplicate_members": duplicates,
        "arrays": per_array,
        "independent_reader_ok": True,
        "numpy_verification": numpy_check,
        "problems": problems,
    }


# ─────────────────────────────────────────────────────────────────────────────
# Immutable source snapshot
# ─────────────────────────────────────────────────────────────────────────────
class SourceSnapshot(object):
    """The eleven files, read **once**, then never re-read for a decision.

    Reading the manifest to judge it and reading it again to copy it is a
    TOCTOU window: the run would verify one state and publish another, and on a
    Drive mount that is not hypothetical.  So one read produces the bytes, and
    both the judging and the copying use these bytes.
    """

    def __init__(self, directory: str, blobs: Mapping[str, bytes]) -> None:
        self.directory = directory
        self._blobs = {name: bytes(body) for name, body in blobs.items()}
        self._digests = {name: _sha256(body)
                         for name, body in self._blobs.items()}

    def names(self) -> Tuple[str, ...]:
        return tuple(sorted(self._blobs))

    def blob(self, name: str) -> bytes:
        return self._blobs[name]

    def digest(self, name: str) -> str:
        return self._digests[name]

    def json(self, name: str) -> Dict[str, object]:
        try:
            return json.loads(self._blobs[name].decode("utf-8"))
        except (ValueError, UnicodeDecodeError) as error:
            raise RepairError(
                SOURCE_BUNDLE_UNEXPECTED,
                f"{name} in the source bundle is not readable JSON ({error})")

    def inventory(self) -> Dict[str, object]:
        return {"directory": os.path.basename(os.path.normpath(self.directory)),
                "count": len(self._blobs),
                "files": [{"name": name, "bytes": len(self._blobs[name]),
                           "sha256": self._digests[name]}
                          for name in self.names()]}

    def recheck(self) -> Dict[str, object]:
        """Re-hash the source on disk against this snapshot.

        The criterion is fixed before the run: every one of the eleven must
        still hash to what the snapshot holds.  Deciding afterwards which
        differences were acceptable is how a check becomes a formality.
        """
        problems: List[str] = []
        for name in self.names():
            path = os.path.join(self.directory, name)
            try:
                with open(path, "rb") as handle:
                    now = _sha256(handle.read())
            except OSError as error:
                problems.append(f"{name}: unreadable at the end of the run "
                                f"({error})")
                continue
            if now != self._digests[name]:
                problems.append(f"{name}: {now} now, {self._digests[name]} "
                                f"when the snapshot was taken")
        return {"ok": not problems, "checked": len(self.names()),
                "problems": problems}


def read_source_snapshot(source_dir: str, approval: Optional[str],
                         adapter: Optional[FolderInventoryAdapter] = None,
                         folder_id: str = SOURCE_BUNDLE_FOLDER_ID
                         ) -> Tuple[SourceSnapshot, Dict[str, object]]:
    """Validate the source folder, then read the eleven exactly once.

    A source that is not the bundle P2 measured is not the thing this repair was
    authorised for, so an unexpected name is a stop rather than something to
    copy along.
    """
    require_execution_approval(approval, f"the source bundle at {source_dir!r}")
    _terminal_execution_guard()
    if not os.path.isdir(source_dir):
        raise RepairError(SOURCE_BUNDLE_UNEXPECTED,
                          f"no source bundle directory at {source_dir!r}")
    entries = sorted(os.listdir(source_dir))
    present = sorted(n for n in entries
                     if os.path.isfile(os.path.join(source_dir, n)))
    subdirs = sorted(n for n in entries if n not in present)
    missing = [n for n in SOURCE_BUNDLE_FILES if n not in present]
    unexpected = [n for n in present if n not in SOURCE_BUNDLE_FILES]
    if missing or unexpected or subdirs:
        raise RepairError(
            SOURCE_BUNDLE_UNEXPECTED,
            f"the source bundle must hold exactly the eleven "
            f"{list(SOURCE_BUNDLE_FILES)}; missing={missing} "
            f"unexpected={unexpected} subdirectories={subdirs}")

    bridge: Optional[Dict[str, object]] = None
    blobs: Dict[str, bytes] = {}
    if adapter is not None:
        bridge, blobs = bridge_mount_to_folder_id(
            adapter, folder_id, source_dir, SOURCE_BUNDLE_FILES, approval)
        # The snapshot *is* the bridged bytes — one read, tied to the folder
        # id — and the re-read below turns a substitution into a finding
        # instead of something that merely could not take effect.
        assert_bytes_unmoved_since_bridge(source_dir, SOURCE_BUNDLE_FILES,
                                          blobs)
    else:
        for name in SOURCE_BUNDLE_FILES:
            with open(os.path.join(source_dir, name), "rb") as handle:
                blobs[name] = handle.read()
    snapshot = SourceSnapshot(source_dir, blobs)
    return snapshot, {"folder_id": folder_id, "folder_id_bridge": bridge,
                      "bytes_from": ("folder-id bridge" if adapter is not None
                                     else "mount (synthetic fixture only)"),
                      **snapshot.inventory()}


# ─────────────────────────────────────────────────────────────────────────────
# Target safety
# ─────────────────────────────────────────────────────────────────────────────
def _real(path: str) -> str:
    return os.path.normcase(os.path.realpath(path))


def _is_link_like(path: str) -> bool:
    if os.path.islink(path):
        return True
    checker = getattr(os.path, "isjunction", None)     # Windows reparse points
    return bool(checker(path)) if checker else False


def _within(child: str, parent: str) -> bool:
    child_real, parent_real = _real(child), _real(parent)
    if child_real == parent_real:
        return True
    return child_real.startswith(parent_real.rstrip(os.sep) + os.sep)


def assert_target_safe(target_dir: str, source_dir: str, shard_dir: str,
                       runs_parent_dir: str) -> Dict[str, object]:
    """Refuse a target that could damage an input, before anything is created.

    Every clause here is about a path that would have looked plausible: the
    source folder itself, a subdirectory of the shard folder, somewhere outside
    the approved runs parent, or a name reached through a symlink whose target
    is elsewhere entirely.
    """
    problems: List[str] = []
    if not target_dir:
        problems.append("no target directory was given")
        raise RepairError(TARGET_UNSAFE, "; ".join(problems))

    for label, other in (("the source bundle", source_dir),
                         ("the shard folder", shard_dir)):
        if not other:
            continue
        if _within(target_dir, other):
            problems.append(f"the target is {label} or inside it")
        if _within(other, target_dir):
            problems.append(f"{label} is inside the target")

    parent = os.path.dirname(os.path.normpath(target_dir))
    if runs_parent_dir:
        if _real(parent) != _real(runs_parent_dir):
            problems.append(
                f"the target's parent is not the approved runs parent "
                f"({parent!r} != {runs_parent_dir!r})")
        if not os.path.isdir(runs_parent_dir):
            problems.append(f"the approved runs parent {runs_parent_dir!r} is "
                            f"not a directory")

    walk = os.path.normpath(target_dir)
    while True:
        if os.path.lexists(walk) and _is_link_like(walk):
            problems.append(f"{walk!r} is a symlink or reparse point")
        nxt = os.path.dirname(walk)
        if nxt == walk:
            break
        walk = nxt

    if problems:
        raise RepairError(TARGET_UNSAFE, "; ".join(problems))
    if os.path.lexists(target_dir):
        raise RepairError(
            TARGET_EXISTS,
            f"{target_dir!r} already exists; a corrective bundle is written to "
            f"a new unique name and never on top of anything.  A retry uses "
            f"another new name — it does not clean or resume this one.")
    return {"target": os.path.basename(os.path.normpath(target_dir)),
            "parent_is_approved_runs_parent": True,
            "inside_source_or_shards": False,
            "link_like_component": False,
            "pre_existing": False}


# ─────────────────────────────────────────────────────────────────────────────
# The corrective bundle
# ─────────────────────────────────────────────────────────────────────────────
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


def _listing(directory: str) -> List[str]:
    try:
        return sorted(os.listdir(directory))
    except OSError:                                      # pragma: no cover
        return []


def assemble_corrective_bundle(snapshot: SourceSnapshot, target_dir: str,
                               npz: bytes, approval: Optional[str],
                               shard_dir: str = "",
                               runs_parent_dir: str = "") -> Dict[str, object]:
    """Copy the eleven from the snapshot, add the NPZ, verify the twelve.

    Nothing is written into, beside or over the source.  The target name is
    claimed with a single `os.mkdir`, which never replaces and never follows.
    **A stop after the claim leaves the partial directory exactly where it is**,
    reported by path and listing, never committed and never deleted — see
    :data:`FAILURE_PUBLICATION_CONTRACT`.
    """
    require_execution_approval(approval,
                               f"a corrective folder at {target_dir!r}")
    _terminal_execution_guard()
    safety = assert_target_safe(target_dir, snapshot.directory, shard_dir,
                                runs_parent_dir)

    os.mkdir(target_dir)
    # From here on every failure must carry the preserved path, because from
    # here on there is a directory a diagnosis will want to look at.
    try:
        copied: List[Dict[str, object]] = []
        for name in SOURCE_BUNDLE_FILES:
            body = snapshot.blob(name)
            _write_new_file(os.path.join(target_dir, name), body)
            with open(os.path.join(target_dir, name), "rb") as handle:
                back = handle.read()
            digest = _sha256(back)
            if digest != snapshot.digest(name) or len(back) != len(body):
                raise RepairError(
                    COPY_NOT_BYTE_IDENTICAL,
                    f"{name} landed as {digest} / {len(back)} B, not "
                    f"{snapshot.digest(name)} / {len(body)} B")
            copied.append({"name": name, "bytes": len(back), "sha256": digest,
                           "byte_identical": True,
                           "from": "immutable source snapshot"})

        _write_new_file(os.path.join(target_dir, MISSING_ARTIFACT), npz)
        with open(os.path.join(target_dir, MISSING_ARTIFACT), "rb") as handle:
            written = handle.read()
        if written != npz:
            raise RepairError(
                COPY_NOT_BYTE_IDENTICAL,
                f"{MISSING_ARTIFACT} on disk is not the bytes that were "
                f"verified")
        copied.append({"name": MISSING_ARTIFACT, "bytes": len(written),
                       "sha256": _sha256(written), "byte_identical": None,
                       "from": "reconstructed and contract-verified NPZ"})

        listing = _listing(target_dir)
        missing = [n for n in BUNDLE_FILES if n not in listing]
        unexpected = [n for n in listing if n not in BUNDLE_FILES]
        if missing or unexpected:
            raise RepairError(
                SOURCE_BUNDLE_UNEXPECTED,
                f"the corrective folder must hold exactly the twelve "
                f"BUNDLE_FILES; missing={missing} unexpected={unexpected}")
    except RepairError as error:
        raise RepairError(error.reason, str(error).split(": ", 1)[-1],
                          incomplete_directory=target_dir,
                          listing=_listing(target_dir)) from error

    return {"directory": os.path.basename(os.path.normpath(target_dir)),
            "path": target_dir, "target_safety": safety,
            "files": copied, "listing": listing,
            "missing": missing, "unexpected": unexpected,
            "contract_files": list(BUNDLE_FILES),
            "committed_marker_written": False}


def verify_corrective_bundle(target_dir: str, snapshot: SourceSnapshot,
                             npz_sha256: str) -> Dict[str, object]:
    """Re-read the finished folder and compare it to what it should be.

    Separate from the assembly on purpose: a writer that certifies its own
    output is checking its variables.  This one opens the files again.
    """
    listing = _listing(target_dir)
    problems: List[str] = []
    if listing != sorted(BUNDLE_FILES):
        problems.append(f"listing {listing} != the twelve "
                        f"{sorted(BUNDLE_FILES)}")
    expected = {name: snapshot.digest(name) for name in snapshot.names()}
    expected[MISSING_ARTIFACT] = npz_sha256
    observed: Dict[str, str] = {}
    for name in listing:
        try:
            with open(os.path.join(target_dir, name), "rb") as handle:
                digest = _sha256(handle.read())
        except OSError as error:                         # pragma: no cover
            problems.append(f"{name}: unreadable ({error})")
            continue
        observed[name] = digest
        if name in expected and digest != expected[name]:
            problems.append(f"{name}: {digest} != expected {expected[name]}")
    return {"ok": not problems, "listing": listing, "observed": observed,
            "expected": expected, "problems": problems}


# ─────────────────────────────────────────────────────────────────────────────
# The whole route
# ─────────────────────────────────────────────────────────────────────────────
def _route(shard_dir: str, source_dir: str, target_dir: str,
           approval: Optional[str], adapter: Optional[FolderInventoryAdapter],
           runs_parent_dir: str, total: int,
           expected_shards: Optional[Mapping[str, Tuple[int, int]]],
           require_numpy: bool, repo_root: Optional[str], mode: str,
           auth_audit: Optional[Dict[str, object]],
           execution_identity: Optional[Dict[str, object]],
           resolve_attempts: int, sleeper) -> Dict[str, object]:
    """The shared body.  Callers decide production or synthetic, never this.

    Order is the safety: nothing is created on disk until the shards have
    qualified, the arrays have been reconstructed, the summary has agreed and
    the NPZ bytes have passed their contract under both readers.  A stop before
    the claim leaves no directory; **every** stop after it preserves the
    partial one and reports its path and listing — which is why the tail of
    this function runs inside one boundary rather than each step remembering to
    attach that detail.
    """
    frozen = assert_frozen_q5d_unchanged()

    parent_bridge = None
    if adapter is not None:
        parent_bridge = bridge_runs_parent(adapter, runs_parent_dir,
                                           source_dir, target_dir, approval)

    snapshot, source = read_source_snapshot(source_dir, approval, adapter)
    manifest = snapshot.json(MANIFEST_FILE)
    summary = snapshot.json(SUMMARY_FILE)

    qualified = qualify_shards(shard_dir, manifest, approval, adapter,
                              SHARD_FOLDER_ID, total=total,
                              expected=expected_shards)
    arrays = reconstruct_arrays(qualified["shards"], qualified["context"],
                               total=total)

    agreement = compare_to_summary(arrays, summary)
    if not agreement["identical"]:
        raise RepairError(
            SUMMARY_DISAGREES,
            f"the reconstructed {MAX_MEMBER_NAME} does not equal the one in "
            f"{SUMMARY_FILE}: {agreement['first_difference']}")

    blob = npz_bytes(arrays)
    contract = verify_npz_contract(blob, summary.get("j_null_max"),
                                   total=total, reconstructed=arrays,
                                   require_numpy=require_numpy)
    if not contract["ok"]:
        raise RepairError(NPZ_CONTRACT_FAILED,
                          "; ".join(str(p) for p in contract["problems"]))

    assembled = assemble_corrective_bundle(snapshot, target_dir, blob,
                                           approval, shard_dir,
                                           runs_parent_dir)
    # ── Everything below has a directory on disk.  One boundary attaches the
    #    preserved path and listing to whatever comes out, so no later step can
    #    forget to and leave a reader unable to find the folder.
    try:
        verified = verify_corrective_bundle(target_dir, snapshot,
                                            contract["sha256"])
        if not verified["ok"]:
            raise RepairError(COPY_NOT_BYTE_IDENTICAL,
                              "; ".join(str(p) for p in verified["problems"]))

        recheck = snapshot.recheck()
        if not recheck["ok"]:
            raise RepairError(
                SOURCE_CHANGED_DURING_RUN,
                f"the source bundle changed while the repair ran: "
                f"{recheck['problems']}")

        folder = None
        if adapter is not None:
            folder = resolve_output_folder_id(
                adapter, RUNS_PARENT_FOLDER_ID,
                os.path.basename(os.path.normpath(target_dir)), approval,
                attempts=resolve_attempts, sleeper=sleeper)
    except RepairError as error:
        raise RepairError(error.reason, str(error).split(": ", 1)[-1],
                          incomplete_directory=(error.incomplete_directory
                                                or target_dir),
                          listing=(error.listing or _listing(target_dir))
                          ) from error

    if mode == MODE_PRODUCTION and not (folder and folder.get("folder_id")):
        # Unreachable by construction — production always has an adapter and
        # `resolve_output_folder_id` either returns an id or raises — and
        # asserted here so it stays that way.
        raise RepairError(                               # pragma: no cover
            OUTPUT_FOLDER_ID_UNRESOLVED,
            "a production run may not complete without a resolved corrective "
            "folder id", incomplete_directory=target_dir,
            listing=_listing(target_dir))

    return {
        "experiment_id": EXPERIMENT_ID, "substage": SUBSTAGE,
        "module_version": MODULE_VERSION, "spec": SPEC_PATH,
        "mode": mode,
        "status": (REPAIR_COMPLETE if mode == MODE_PRODUCTION
                   else SYNTHETIC_COMPLETE),
        "ingestable": mode == MODE_PRODUCTION,
        "first_stopping_reason": None,
        "frozen_q5d": frozen,
        "execution_identity": execution_identity,
        "drive_authentication": auth_audit,
        "runs_parent_bridge": parent_bridge,
        "artifact_identities": (artifact_identities(repo_root)
                                if repo_root else None),
        "pinned_commit": (execution_identity or {}).get("execution_head"),
        "member_naming_unresolved": MEMBER_NAMING_UNRESOLVED,
        "member_naming_note": MEMBER_NAMING_NOTE,
        "qualification": qualified["report"],
        "summary_agreement": agreement,
        "npz": contract,
        "source_bundle": source,
        "source_recheck": recheck,
        "corrective_bundle": assembled,
        "corrective_folder_id": folder,
        "verification": verified,
        "training_performed": False,
        "join_rerun": False,
        "null_recomputed": False,
        "ds2_outcome_opened": False,
        "v10_probability_opened": False,
        "registered_anything": False,
    }


def run_repair(shard_dir: str, source_dir: str, target_dir: str,
               approval: Optional[str] = None,
               authenticator: Optional[DriveAuthenticator] = None,
               service_factory=None,
               runs_parent_dir: str = "",
               execution_head: Optional[str] = None,
               repo_root: Optional[str] = None,
               total: int = N_REPLICATES,
               expected_shards: Optional[Mapping[str, Tuple[int, int]]] = None,
               resolve_attempts: int = 5, sleeper=None) -> Dict[str, object]:
    """The production route.  Drive access is mandatory and built here.

    In order, and the order is the contract:

    1. the approval token
    2. `EXECUTION_APPROVAL_RECORD.granted`
    3. the approved implementation identity, against the code on disk
    4. the exact registered folder ids
    5. the terminal execution guard
    6. the dependency check
    7. credential acquisition
    8. proof of exactly the read-only scope
    9. the Drive service and the adapter
    10. folder-id inventories, including the runs parent
    11. the first byte read, and only then any byte written

    There is no `adapter` parameter and no way to pass `None` through: a
    production run that could skip Drive would be a run whose provenance rests
    on a typed path.  A fixture that needs to skip it uses
    :func:`run_repair_synthetic_fixture`, which cannot produce a
    `REPAIR_COMPLETE`.
    """
    require_execution_approval(approval, "the repair route")
    if not EXECUTION_APPROVAL_RECORD.get("granted"):
        _terminal_execution_guard()                      # raises
    identity = verify_execution_identity(repo_root or ROOT_GUESS,
                                         execution_head)
    for folder_id in (SOURCE_BUNDLE_FOLDER_ID, SHARD_FOLDER_ID,
                      RUNS_PARENT_FOLDER_ID):
        if not folder_id:                                # pragma: no cover
            raise RepairError(INPUT_UNQUALIFIED,
                              "a registered folder id is missing")
    _terminal_execution_guard()

    adapter, auth_audit = build_drive_adapter(approval, authenticator,
                                              service_factory)
    if adapter is None:                                  # pragma: no cover
        raise RepairError(
            INPUT_UNQUALIFIED,
            "the production route requires a Drive adapter; without one the "
            "registered folder ids cannot be checked and identity would rest "
            "on a typed path")
    return _route(shard_dir, source_dir, target_dir, approval, adapter,
                  runs_parent_dir, total, expected_shards, True,
                  repo_root, MODE_PRODUCTION, auth_audit, identity,
                  resolve_attempts, sleeper)


def run_repair_synthetic_fixture(shard_dir: str, source_dir: str,
                                 target_dir: str,
                                 approval: Optional[str] = None,
                                 synthetic_marker: Optional[str] = None,
                                 adapter: Optional[FolderInventoryAdapter]
                                 = None,
                                 runs_parent_dir: str = "",
                                 total: int = N_REPLICATES,
                                 expected_shards: Optional[
                                     Mapping[str, Tuple[int, int]]] = None,
                                 require_numpy: bool = False,
                                 repo_root: Optional[str] = None,
                                 resolve_attempts: int = 1,
                                 sleeper=None) -> Dict[str, object]:
    """The synthetic-only seam.  It cannot produce a publishable result.

    It exists because lower-level fixtures need to exercise the route without
    Drive, and because the alternative — letting the production entry point
    accept `adapter=None` — would make "no provenance" reachable by omitting an
    argument.  Here it takes an explicit marker, and the terminal status is
    `REPAIR_COMPLETE_SYNTHETIC_FIXTURE`, which nothing downstream accepts.

    The notebook never calls this; a test asserts that.
    """
    if synthetic_marker != SYNTHETIC_FIXTURE_MARKER:
        raise RepairError(
            INPUT_UNQUALIFIED,
            "the synthetic fixture seam requires its explicit marker; "
            "production runs go through run_repair(), which requires Drive")
    require_execution_approval(approval, "the synthetic repair route")
    _terminal_execution_guard()
    return _route(shard_dir, source_dir, target_dir, approval, adapter,
                  runs_parent_dir, total, expected_shards, require_numpy,
                  repo_root, MODE_SYNTHETIC, None, None, resolve_attempts,
                  sleeper)


def report_markdown(decision: Mapping[str, object]) -> str:
    """The human-readable record.  Its saved notebook output is the anchor.

    No sidecar file is written into the corrective folder, so this printed
    report — copied into the Decision log by a separate PR — is where the
    digests, the folder id and the provenance live.
    """
    qualification = dict(decision.get("qualification") or {})
    coverage = dict(qualification.get("coverage") or {})
    npz = dict(decision.get("npz") or {})
    numpy_check = dict(npz.get("numpy_verification") or {})
    agreement = dict(decision.get("summary_agreement") or {})
    source = dict(decision.get("source_bundle") or {})
    corrective = dict(decision.get("corrective_bundle") or {})
    folder = dict(decision.get("corrective_folder_id") or {})
    frozen = dict(decision.get("frozen_q5d") or {})
    lines = [
        f"# {EXPERIMENT_ID} — {SUBSTAGE}",
        "",
        f"status: **{decision.get('status')}** · first stopping reason: "
        f"{decision.get('first_stopping_reason')}",
        "",
        "A packaging repair. No J value was computed, no replicate was "
        "re-run, and no scientific question was answered.",
        "",
        "## Identity",
        f"- frozen Q5-D LF-normalised SHA-256 "
        f"`{frozen.get('lf_normalized_sha256')}` (registered convention)",
        f"- frozen Q5-D raw-byte SHA-256 `{frozen.get('raw_sha256')}` "
        f"(had CRLF: {frozen.get('had_crlf')})",
        f"- rule fingerprint `{frozen.get('rule_fingerprint')}`",
        f"- pinned commit: {decision.get('pinned_commit')}",
        f"- identity anchor: {qualification.get('identity_anchor')}",
        "",
        "## Folder ids (chosen by id, never by name)",
        f"- source bundle `{source.get('folder_id')}`",
        f"- shard folder `{qualification.get('folder_id')}`",
        f"- corrective folder `{folder.get('folder_id')}`",
        "",
        "## Shards",
        f"- {qualification.get('observed_file_count')} files against a "
        f"preregistered {qualification.get('expected_count')} "
        f"({qualification.get('expected_first')} … "
        f"{qualification.get('expected_last')})",
        f"- missing {qualification.get('missing_files')} · extra "
        f"{qualification.get('extra_files')} · subdirectories "
        f"{qualification.get('subdirectories')}",
        f"- coverage {coverage.get('covered')}/{coverage.get('expected')} · "
        f"missing {coverage.get('missing_count')} · overlapping "
        f"{coverage.get('overlap_count')}",
        "",
        "## Reconstruction",
        f"- {MAX_MEMBER_NAME} identical to {SUMMARY_FILE}: "
        f"{agreement.get('identical')} "
        f"({agreement.get('n_reconstructed')} vs {agreement.get('n_summary')})",
        f"- NPZ SHA-256 `{npz.get('sha256')}` ({npz.get('bytes')} B), "
        f"contract ok: {npz.get('ok')}",
        f"- members {npz.get('members')} · duplicates "
        f"{npz.get('duplicate_members')}",
        f"- numpy verification ran: {numpy_check.get('ran')} · "
        f"allow_pickle=False · ok: {numpy_check.get('ok')} · numpy "
        f"{numpy_check.get('numpy_version')}",
        f"- member naming unresolved: "
        f"{decision.get('member_naming_unresolved')}",
        "",
        "## Corrective bundle",
        f"- source: {source.get('count')} files, re-hash after the run ok: "
        f"{dict(decision.get('source_recheck') or {}).get('ok')}",
        f"- target: {len(list(corrective.get('listing') or []))} files, "
        f"missing {corrective.get('missing')} unexpected "
        f"{corrective.get('unexpected')}",
        f"- no COMMITTED marker written: "
        f"{corrective.get('committed_marker_written') is False}",
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
            "read_npz_bytes", "npz_member_names", "verify_npz_contract",
            "numpy_verify_npz", "read_source_snapshot", "SourceSnapshot",
            "assemble_corrective_bundle", "verify_corrective_bundle",
            "run_repair_synthetic_fixture", "bridge_runs_parent",
            "resolve_output_folder_id", "reconcile_output_folder_id",
            "assert_bytes_unmoved_since_bridge", "build_drive_adapter",
            "DriveAuthenticator", "ColabReadOnlyAuthenticator",
            "audit_credential_scopes", "check_runtime_dependencies",
            "verify_execution_identity", "module_science_digest",
            "SYNTHETIC_FIXTURE_MARKER", "DRIVE_READONLY_SCOPE",
            "ADAPTER_OPERATIONS", "REJECTED_PROPOSAL",
            "assert_target_safe", "identity_from_manifest",
            "identity_only_context", "coverage_report",
            "assert_frozen_q5d_unchanged", "frozen_q5d_digests",
            "digest_pair", "normalise_newlines", "artifact_identities",
            "FolderInventoryAdapter", "GoogleDriveFolderInventory",
            "inventory_folder", "bridge_mount_to_folder_id",
            "confirm_folder_id_of_child", "report_markdown",
            "EXECUTION_APPROVAL_TOKEN", "EXECUTION_APPROVAL_RECORD",
            "NPZ_ARRAYS", "MEMBER_NAME_BY_FAMILY", "BUNDLE_FILES",
            "SOURCE_BUNDLE_FILES", "EXPECTED_SHARD_FILENAMES", "STOP_REASONS",
            "FAILURE_PUBLICATION_CONTRACT", "NEWLINE_CONVENTION")


def design_card() -> str:
    """What this module is and is not, printed before anything runs."""
    return "\n".join([
        f"{EXPERIMENT_ID} / {SUBSTAGE} — module v{MODULE_VERSION}",
        f"spec: {SPEC_PATH}",
        f"originating decision: {ORIGINATING_DECISION}",
        "",
        "A packaging repair: reconstruct negative_control_null.npz from the",
        f"{EXPECTED_SHARD_COUNT} existing null shards and place it in a NEW",
        "corrective folder beside byte-identical copies of the existing",
        "eleven files.",
        "",
        "It does NOT re-run the beat join, re-run the null, compute any J",
        "value, modify the existing bundle or shards, edit the frozen module,",
        "relax the twelve-file contract, or register anything.",
        "",
        f"execution approved: {bool(EXECUTION_APPROVAL_RECORD.get('granted'))}",
        APPROVAL_NOTE,
        "",
        FAILURE_PUBLICATION_CONTRACT,
        "",
        MEMBER_NAMING_NOTE,
    ])
