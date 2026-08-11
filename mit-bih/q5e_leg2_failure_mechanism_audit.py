#!/usr/bin/env python3
"""EXP-2026-008 / Q5-E — Leg 2 join failure mechanism audit (implementation).

This module implements the **frozen** design in
``experiments/specs/EXP-2026-008-q5e-leg2-failure-mechanism-audit.md``.  It
adds no scientific rule of its own.  Every constant, denominator, window,
control, statistic, gate and terminal branch below is a transcription of that
specification, whose `status` is `approved_for_implementation`.

What this file is allowed to do
-------------------------------
Implement the diagnostic.  **Executing it on registered data needs a separate
user approval that does not exist yet.**  Every entry point that would open a
registered artifact refuses without an explicit approval token, and the check
runs *before* :func:`open`, so an unapproved call cannot even learn whether a
file is present.

What it must never do
---------------------
Open a DS2 per-beat class label, a V10 probability, or any association or
S PR-AUC quantity; train anything; run ``detect_r()`` outside the M4.0 gate;
modify the frozen Q5-D module, an existing null shard, or an existing Drive
bundle.  :func:`assert_implementation_only` is the cheapest artifact a reviewer
can re-run against this claim.

Language boundary
-----------------
This diagnostic reports **associated mechanisms** / **failure-associated
factors**.  It never calls an observed association a cause.  The word "cause"
appears in this file only where it is forbidden.
"""

from __future__ import annotations

import hashlib
import json
import math
import os
import random
import statistics
from typing import (Any, Dict, Iterable, List, Mapping, Optional, Sequence,
                    Tuple)

# The frozen Q5-D module is imported **read-only**.  Nothing here writes to it.
try:                                                        # pragma: no cover
    import q5d_order_preserving_beat_join as BJ
except ImportError:                                         # pragma: no cover
    import sys
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import q5d_order_preserving_beat_join as BJ


EXPERIMENT_ID = "EXP-2026-008"
SUBSTAGE = "Q5E_LEG2_FAILURE_MECHANISM_AUDIT"
RUN_SLUG = "EXP-2026-008_q5e_leg2_failure_mechanism_audit"
MODULE_VERSION = 1
SPEC_PATH = ("experiments/specs/"
             "EXP-2026-008-q5e-leg2-failure-mechanism-audit.md")

#: The audited run.  Identity is established by digest, never by path.
SOURCE_BUNDLE_RUN = "20260811T035108_EXP-2026-007_q5d_beat_join_DS1_GATE"
SOURCE_BUNDLE_FOLDER_ID = "1JjwBhU8BXf8lRrYPcM2UjFNdIKxE9Ghd"
PRODUCING_CODE_SHA256 = (
    "6b098c67df3c8e2c8c070b093e6e2d801566f548a3173626745c4a126a97f226")
REGISTERED_RULE_FINGERPRINT = (
    "31c4be9f44582a68c301fe6cc6572f4db6ff0b3de694af68f6ac6a0f48c2b40e")
SUPERSEDED_MARKER = "SUPERSEDED.json"

#: Files read from the canonical bundle.  Preregistered by name: a glob cannot
#: notice a file that is absent.
BUNDLE_INPUT_FILES: Tuple[str, ...] = (
    "unmatched_and_ambiguous.csv", "join_map.parquet",
    "record_class_coverage.csv", "decision.json", "manifest.json",
)

SPLIT = "DS1"
AAMI_CLASSES: Tuple[str, ...] = BJ.AAMI_CLASSES
SIDE_MAMBA = "mamba"
SIDE_CACHE = "cache"
SIDES: Tuple[str, ...] = (SIDE_MAMBA, SIDE_CACHE)

# ─────────────────────────────────────────────────────────────────────────────
# QA reproduction targets.  Checked before any measurement; one mismatch stops.
# ─────────────────────────────────────────────────────────────────────────────
QA_TARGETS: Dict[str, int] = {
    "total_failure_rows": 24341,
    "mamba_side_failure_rows": 12183,
    "cache_side_failure_rows": 12158,
    "LEG2_NO_CANDIDATE_EDGE": 13716,
    "LEG2_EDGE_IN_NO_MAXIMUM_MATCHING": 9887,
    "LEG2_AMBIGUOUS_RANK_CLASS": 738,
    "ds1_records": 22,
}

# ─────────────────────────────────────────────────────────────────────────────
# Frozen M4 identity constants (spec §"Frozen M4 identity constants").
# ─────────────────────────────────────────────────────────────────────────────
M4_INPUT_CONTRACT: Dict[str, Dict[str, object]] = {
    "v10_source": {
        "drive_id": "1czXZdgSrGttrhOFlNvOHQ3l16ZfluOPX",
        "n_files": 7, "bytes": 39761,
        "aggregate": ("1a0c66c8116745bf83f836fd267931b83f"
                      "0179cc5e62fd1ba5b055ec236452ce"),
        "expected": ("__init__.py", "data.py", "evaluate.py", "frontend.py",
                     "model.py", "pwave.py", "train.py"),
    },
    "v10_cache": {
        "drive_id": "1I6iugsrHwJjjpLVS8TVp-aDkVwpdmJxF",
        "n_files": 45, "bytes": 167868618,
        "aggregate": ("82b9a593dcf23fa4ffc60b44c2fe7da02313"
                      "dfe7d69dfbe64d85c38b4aa78b14"),
    },
}
M4_CORROBORATING: Dict[str, Dict[str, object]] = {
    "v9_source": {
        "drive_id": "1oYHJi38hir2JqZl9s_SyuSxq3Hxw25sK",
        "n_files": 7, "bytes": 79329,
        "aggregate": ("ffb5679cdfd6b9cc5d46a1071f1fac374d0b"
                      "b428c360d9a2be80edb111bfb296"),
        "expected": ("__init__.py", "data.py", "evaluate.py", "frontend.py",
                     "model.py", "train.py", "v15b_local.py"),
    },
    "v9_cache": {
        "drive_id": "1TXLX14RHA5u1dIUiYt36k2dcT5lpm5RY",
        "n_files": 45, "bytes": 167064378,
        "aggregate": ("25cd7952329fc6f04273046c80d5b0d7b3ee"
                      "74baf10d2dba4036f9ea7f94fbe8"),
    },
}
#: The two decisive source-map files, by digest.  A path is never sufficient.
M4_SOURCE_MAP_HASHES: Dict[str, str] = {
    "frontend.py":
        "d2635e05c2e0b26f68ae022c0997970c5d3a3d0828e3e943c7c78b260a78a217",
    "data.py":
        "20cde66b01d1172926aa1b84cbb70b70ea28bb20c2e958a2c26bd01d03497ada",
}
#: Call sites the static source map must locate.  Keyword presence alone is
#: explicitly insufficient (spec M4.0 condition 1), so each entry names the
#: file, the enclosing function and the token that must appear inside it.
M4_SOURCE_MAP_CONTRACT: Tuple[Tuple[str, str, str], ...] = (
    ("frontend.py", "detect_r", "def detect_r"),
    ("frontend.py", "rr_features", "def rr_features"),
    ("data.py", "build_record", "detect_r("),
    ("data.py", "build_record", "0.15"),
    ("data.py", "build_record", "used"),
    ("data.py", "build_record", "150"),
    ("data.py", "build_record", "rr_features"),
)
#: The registered production runtime.  M4.0 condition 2 admits no fallback.
M4_REGISTERED_RUNTIME: Dict[str, str] = {
    "python": "3.12.3", "numpy": "2.5.1", "scipy": "1.18.0",
    "wfdb": "4.3.1", "tensorflow": "2.21.0", "keras": "3.15.0",
}
#: Runtime keys M4.0 condition 2 actually requires to be exact.
M4_RUNTIME_REQUIRED: Tuple[str, ...] = ("python", "numpy", "scipy", "wfdb")
#: The detector's own matching tolerance, in samples, from the frozen source.
M4_PEAK_MATCH_TOLERANCE_SAMPLES = 54
M4_ANCHOR_HALF_WINDOW = 10
PREP_M4_RR_EQUIVALENCE_VERDICT = "RR_VALUE_IDENTICAL_44_OF_44"

# ─────────────────────────────────────────────────────────────────────────────
# Measurement constants
# ─────────────────────────────────────────────────────────────────────────────
#: M1 window half-width, fixed by the registered ledger: 1 + max |mamba_n -
#: cache_n| = 1 + 14 (record 116).  Never widened by an observed distance.
M1_WINDOW_HALF_WIDTH = 15
#: Reported distance bins, in integer samples at 360 Hz.
M1_BINS: Tuple[Tuple[str, int, Optional[int]], ...] = (
    ("0-1", 0, 1), ("2-5", 2, 5), ("6-20", 6, 20),
    ("21-100", 21, 100), (">100", 101, None),
)
M1_GATE_BIN = "2-5"
M1_H3_FAR_BINS: Tuple[str, ...] = ("21-100", ">100")
CENSORED_FLAG = "CENSORED_AT_WINDOW_BOUNDARY"
ENDPOINT_ZERO_FLAG = "CACHE_ENDPOINT_ZERO"

#: Run-length report buckets.
RUN_BUCKETS: Tuple[str, ...] = ("1", "2", "3-9", ">=10")
LONG_RUN_MIN = 3
#: Adjacency definitions.  `mamba_record_row` is decisional (Q1); the raw
#: ordinal is a registered, non-decisional sensitivity audit.
ADJ_PRIMARY = "mamba_record_row"
ADJ_SECONDARY = "raw_atr_ordinal"
ADJACENCIES: Tuple[str, ...] = (ADJ_PRIMARY, ADJ_SECONDARY)
NEIGHBOURHOODS: Tuple[int, ...] = (1, 10)
LOCAL_RR_HALF_WINDOW = 10

#: M3 groups.  `CERTIFIED` on the cache side is derived one-to-one (Q4).
GROUP_CERTIFIED = "CERTIFIED"
GROUP_NO_EDGE = "NO_EDGE"
GROUP_NOT_OPTIMAL = "NOT_OPTIMAL"
GROUP_AMBIGUOUS = "AMBIGUOUS"
M3_GROUPS: Tuple[str, ...] = (GROUP_CERTIFIED, GROUP_NO_EDGE,
                              GROUP_NOT_OPTIMAL, GROUP_AMBIGUOUS)
REASON_TO_GROUP: Dict[str, str] = {
    BJ.REASON_NO_EDGE: GROUP_NO_EDGE,
    BJ.REASON_NOT_OPTIMAL: GROUP_NOT_OPTIMAL,
    BJ.REASON_AMBIGUOUS: GROUP_AMBIGUOUS,
}
H4_DEGREE_MIN = 2

#: **Confirmed by Codex, 2026-08-12, before any execution.**  H4 registers one
#: family-level statistic and one p-value, so the side has to be fixed before
#: the run rather than chosen from results.  It is the **cache** side because:
#: in Q5-E's positional failure audit the cache is the detector-row side; Q4
#: defines cache-side `CERTIFIED` one-to-one and requires the four cache-side
#: groups to form a disjoint, exhaustive partition; and fixing it in advance
#: removes any possibility of picking the more favourable of two contrasts
#: after the fact.  The mamba side is still measured and reported, to preserve
#: the symmetric diagnostic picture of the candidate graph, but it is
#: descriptive and never enters a p-value, a q99 comparison, an effect gate,
#: Holm, an association flag or the decision tree.
#:
#: Note this is *not* "every decisional population is cache-side": M2 and H3
#: are decisional on `mamba_record_row`.  The reason is specific to H4.
H4_DECISIONAL_SIDE = SIDE_CACHE

# ─────────────────────────────────────────────────────────────────────────────
# Negative controls and multiplicity
# ─────────────────────────────────────────────────────────────────────────────
N_NULL_REPLICATES = 10000
MASTER_SEED = 2026019
CONTROL_A = "A_within_record_class_circular_shift"
CONTROL_B = "B_within_record_joint_status_permutation"
CONTROL_C = "C_discordance_anchor_circular_shift"
CONTROL_FAMILIES: Tuple[str, ...] = (CONTROL_A, CONTROL_B, CONTROL_C)

HYPOTHESES: Tuple[str, ...] = ("H1", "H2", "H3", "H4")
HYPOTHESIS_CONTROL: Dict[str, str] = {
    "H1": CONTROL_A, "H2": CONTROL_C, "H3": CONTROL_C, "H4": CONTROL_B,
}
HOLM_ALPHA = 0.05
HOLM_FAMILY_SIZE = 4
UNEVALUABLE = "UNEVALUABLE"
#: An unevaluable family enters Holm at p=1.0 and **only** there (Q3).
UNEVALUABLE_P = 1.0
EFFECT_SHARE_MIN = 0.50

# ─────────────────────────────────────────────────────────────────────────────
# Terminal branches and stopping reasons — spec names, verbatim.
# ─────────────────────────────────────────────────────────────────────────────
FLAG_H1 = "H1_ASSOCIATED"
FLAG_H2 = "H2_ASSOCIATED"
FLAG_H3 = "H3_ASSOCIATED"
FLAG_H4 = "H4_ASSOCIATED"
HYPOTHESIS_FLAG: Dict[str, str] = {
    "H1": FLAG_H1, "H2": FLAG_H2, "H3": FLAG_H3, "H4": FLAG_H4}
DECISION_MULTI = "MULTI_MECHANISM_ASSOCIATED"
DECISION_NONE = "NO_REGISTERED_MECHANISM_ASSOCIATED"
DECISION_UNRESOLVED = "MECHANISM_UNRESOLVED_INPUT_ABSENT"
DECISION_MISMATCH = "DIAGNOSTIC_INPUT_MISMATCH"
DECISIONS: Tuple[str, ...] = (
    DECISION_MISMATCH, DECISION_UNRESOLVED, DECISION_MULTI,
    FLAG_H1, FLAG_H2, FLAG_H3, FLAG_H4, DECISION_NONE,
)
M4_OK = "OK"
M4_INPUT_ABSENT = "DIAGNOSTIC_INPUT_ABSENT"
M4_SOURCE_MAP_UNVERIFIED = "M4_SOURCE_MAP_UNVERIFIED"
M4_RUNTIME_UNAVAILABLE = "M4_REGISTERED_RUNTIME_UNAVAILABLE"
M4_COUNT_MISMATCH = "M4_DETECTOR_COUNT_MISMATCH"
M4_RR_MISMATCH = "M4_FROZEN_RR_MISMATCH"
M4_IDENTITY_MISMATCH = "M4_INPUT_IDENTITY_MISMATCH"
#: The ordered M4.0 condition-2 sub-gates.  Order is itself registered: no
#: anchor may be computed before every one of these has passed.
M4_GATE_ORDER: Tuple[str, ...] = (
    "runtime", "source_map", "detector_replay", "record_counts", "rr_equality")

LANGUAGE_BOUNDARY = "association_only_no_causal_claim"

# ─────────────────────────────────────────────────────────────────────────────
# Execution approval.  Permission is checked before capability, and before any
# `open()`, exactly as the frozen Q5-D module does.
# ─────────────────────────────────────────────────────────────────────────────
EXECUTION_APPROVAL_TOKEN = (
    "q5e-execution-on-registered-data-approved-by-user")
EXECUTION_APPROVAL_FLAG = "--i-have-separate-execution-approval"
APPROVAL_NOTE = (
    "EXP-2026-008 is approved for implementation only.  Running it on the "
    "registered artifacts requires a separate, explicit user approval, which "
    "is a different decision from approving this design.")
#: Default OFF.  A stray import or notebook run cannot reach registered data.
OPEN_REGISTERED_DATA = False

MODE_DESIGN = "DESIGN"
MODE_FIXTURES = "FIXTURES"
MODE_QA = "QA"
MODE_AUDIT = "AUDIT"
MODES: Tuple[str, ...] = (MODE_DESIGN, MODE_FIXTURES, MODE_QA, MODE_AUDIT)
MODES_NEEDING_EXECUTION_APPROVAL: Tuple[str, ...] = (MODE_QA, MODE_AUDIT)

RUNTIME_DEPENDENCIES: Dict[str, Tuple[str, str]] = {
    "numpy": ("reading registered arrays and the frozen cache", "2.5.1"),
    "pyarrow": ("reading `join_map.parquet` up front, not at write time", ""),
    "wfdb": ("Leg 1 replay from raw `.atr` (M1, M3)", "4.3.1"),
    "scipy": ("`detect_r()` reproduction (M4 only)", "1.18.0"),
    "matplotlib": ("the seven registered figures", ""),
}
STAGE_REQUIREMENTS: Dict[str, Tuple[str, ...]] = {
    MODE_DESIGN: (),
    MODE_FIXTURES: (),
    MODE_QA: ("numpy", "pyarrow"),
    MODE_AUDIT: ("numpy", "pyarrow", "wfdb", "matplotlib"),
}
#: M4 is the only stage that needs scipy, and only under its own gate.
M4_REQUIREMENTS: Tuple[str, ...] = ("numpy", "wfdb", "scipy")

#: Textual evidence that this file cannot reach a sealed outcome.  Tokens are
#: split so this table does not match itself.
FORBIDDEN_TOKENS: Tuple[str, ...] = (
    '["pro' + 'b"]', "['pro" + "b']", ".f" + "it(", ".back" + "ward(",
    "average_" + "precision", "precision_recall_" + "curve",
    "roc_auc_" + "score", "pr_" + "auc(", "torch." + "optim",
    "state_" + "dict", "model." + "predict(", "keras." + "Model",
    "ds2_" + "labels(", "read_" + "probabilities(",
)

BUNDLE_FILES: Tuple[str, ...] = (
    "config.json", "manifest.json", "q5e_result.json",
    "m0_class_by_reason.csv", "m0_record_class.csv", "m0_runs.csv",
    "m1_distance.csv", "m3_graph.csv", "m4_anchors.csv",
    "null_summary.json", "log.txt", "summary.md",
)
FIGURES: Tuple[str, ...] = (
    "fig1_class_by_reason_stacked.png",
    "fig2_record_class_failure_heatmap.png",
    "fig3_record_208_failure_raster.png",
    "fig4_run_length_distribution.png",
    "fig5_nearest_distance_histogram.png",
    "fig6_candidate_degree_violin_ecdf.png",
    "fig7_anchor_aligned_failure_curve.png",
)
#: Figure 7 exists only when M4.0 passes; its absence is recorded, not hidden.
FIGURE_M4_ONLY = "fig7_anchor_aligned_failure_curve.png"


class Q5EError(RuntimeError):
    """Anything that must stop the substage rather than be worked around."""


class ExecutionNotApprovedError(Q5EError):
    """Raised before a registered artifact is opened without approval."""


class DiagnosticInputMismatch(Q5EError):
    """QA reproduction or partition assertion failed.  No measurement stands."""


# ─────────────────────────────────────────────────────────────────────────────
# Guards
# ─────────────────────────────────────────────────────────────────────────────
def require_execution_approval(approval: Optional[str], what: str) -> None:
    """Gate every path that would open a registered artifact.

    Called *before* the file is opened, so a refusal leaves no trace of having
    touched the data and cannot even reveal whether it exists.
    """
    if approval != EXECUTION_APPROVAL_TOKEN:
        raise ExecutionNotApprovedError(
            f"refusing to open {what}: reaching a registered artifact is an "
            f"explicit opt-in.\n{APPROVAL_NOTE}\n"
            f"Pass {EXECUTION_APPROVAL_FLAG} (CLI) or the execution-approval "
            f"token (API), and clear the identity preflight first.")


def execution_is_approved(approval: Optional[str]) -> bool:
    """Non-raising probe, for cards and notebooks that report their own state."""
    return approval == EXECUTION_APPROVAL_TOKEN


def open_registered_input(path: str, approval: Optional[str], what: str):
    """The single door to a registered file: approval first, existence second."""
    require_execution_approval(approval, what)
    if not os.path.exists(path):
        raise Q5EError(f"{DECISION_MISMATCH}: {what} not found at {path!r}")
    return open(path, "rb")


def resolve_mode(mode: str) -> str:
    value = str(mode).upper()
    if value not in MODES:
        raise Q5EError(f"unknown mode {mode!r}; expected one of {MODES}")
    return value


def check_runtime_dependencies(mode: str = MODE_DESIGN) -> Dict[str, object]:
    """Report which declared imports are present for a stage, without running it."""
    mode = resolve_mode(mode)
    needed = STAGE_REQUIREMENTS[mode]
    present, missing = {}, []
    for name in needed:
        try:
            module = __import__(name)
        except ImportError:
            missing.append(name)
        else:
            present[name] = getattr(module, "__version__", "")
    return {"mode": mode, "required": list(needed), "present": present,
            "missing": missing, "ok": not missing,
            "pip_install": "pip install " + " ".join(missing) if missing else ""}


def assert_runtime_ready(mode: str = MODE_DESIGN) -> Dict[str, object]:
    """Refuse to start a stage whose imports are absent, before anything is read."""
    report = check_runtime_dependencies(mode)
    if not report["ok"]:
        raise Q5EError(
            f"stage {report['mode']} needs {report['missing']} which are not "
            f"importable.  Install them first: {report['pip_install']}")
    return report


def stage_should_run(stage: str, mode: str, approval: Optional[str],
                     emit=print) -> bool:
    """Decide whether a stage runs and **always announce the outcome**.

    A stage that quietly does nothing must never look like a stage that
    passed.  Q5-D lost a run to exactly that, so the announcement is not
    optional and there is no bare ``if MODE == ...`` guard anywhere.
    """
    mode = resolve_mode(mode)
    if mode not in MODES_NEEDING_EXECUTION_APPROVAL:
        emit(f"SKIP {stage}: mode is {mode}; registered data is not opened.  "
             f"Set MODE to one of {MODES_NEEDING_EXECUTION_APPROVAL}.  "
             f"Anything printed above is a constant, not a result.")
        return False
    if not execution_is_approved(approval):
        emit(f"SKIP {stage}: no execution approval token.  {APPROVAL_NOTE}  "
             f"Anything printed above is a constant, not a result.")
        return False
    emit(f"RUN  {stage}: mode {mode}, execution approval present.")
    return True


def module_capabilities() -> Tuple[str, ...]:
    """Names a notebook asserts before use, so a stale clone cannot masquerade.

    A version integer is defeated by forgetting to bump it; a capability list
    is defeated only by actually lacking the capability.
    """
    return ("run_audit", "verify_qa_targets", "m0_report", "m1_distances",
            "m2_report", "m3_graph", "m4_feasibility_gate", "m4_anchors",
            "run_null_family", "h4_evaluate", "h4_descriptive_by_side",
            "holm_4family", "evaluate_flags", "decide",
            "build_result", "write_bundle", "assert_implementation_only",
            "stage_should_run", "EXECUTION_APPROVAL_TOKEN")


def assert_implementation_only(path: Optional[str] = None) -> Dict[str, object]:
    """Textual proof that this file cannot reach a sealed outcome."""
    target = path or os.path.abspath(__file__)
    with open(target, encoding="utf-8") as handle:
        text = handle.read()
    hits = [token for token in FORBIDDEN_TOKENS if token in text]
    if hits:
        raise Q5EError(f"{target}: forbidden tokens present: {hits}")
    return {"path": target, "ok": True, "checked_tokens": len(FORBIDDEN_TOKENS),
            "sha256": sha256_file(target)}


def sha256_file(path: str) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def _canonical_json(obj: object) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False)


def _rng(family: str, replicate: int) -> random.Random:
    """Deterministic per-replicate stream, seeded from a stable string.

    ``random.Random.seed`` hashes a string with SHA-512, so replicate ``b`` is
    the same value on any machine, in any order, on any worker count, and is
    unaffected by ``PYTHONHASHSEED``.
    """
    return random.Random(f"{MASTER_SEED}|{family}|{int(replicate)}")


def _ratio(numerator: float, denominator: float) -> float:
    return float(numerator) / float(denominator) if denominator else 0.0


def percentile(values: Sequence[float], pct: float) -> float:
    """Linear-interpolation percentile, matching ``numpy.percentile`` default."""
    if not values:
        return 0.0
    ordered = sorted(float(v) for v in values)
    if len(ordered) == 1:
        return ordered[0]
    position = (len(ordered) - 1) * (float(pct) / 100.0)
    low = int(position)
    high = min(low + 1, len(ordered) - 1)
    weight = position - low
    return ordered[low] * (1.0 - weight) + ordered[high] * weight


def median(values: Sequence[float]) -> float:
    return float(statistics.median(values)) if values else 0.0


def ecdf(values: Sequence[float]) -> List[Tuple[float, float]]:
    """Empirical CDF as ``(value, cumulative share)`` pairs, ascending."""
    if not values:
        return []
    ordered = sorted(float(v) for v in values)
    total = len(ordered)
    out, seen = [], 0
    for index, value in enumerate(ordered):
        seen = index + 1
        if index + 1 == total or ordered[index + 1] != value:
            out.append((value, seen / total))
    return out


# ─────────────────────────────────────────────────────────────────────────────
# Row model.  A join-map row is a plain mapping with the frozen 15 fields, so
# every measurement below is testable on synthetic rows with no file access.
# ─────────────────────────────────────────────────────────────────────────────
def is_mamba_side(row: Mapping[str, object]) -> bool:
    """Mamba-side rows are identified by a non-null ``mamba_record_row``."""
    return row.get("mamba_record_row") is not None


def is_cache_side(row: Mapping[str, object]) -> bool:
    return not is_mamba_side(row)


def is_failed(row: Mapping[str, object]) -> bool:
    return str(row.get("status")) != BJ.STATUS_CERTIFIED


def row_group(row: Mapping[str, object]) -> str:
    """Map a join-map row to its M3 group."""
    if not is_failed(row):
        return GROUP_CERTIFIED
    reason = str(row.get("drop_or_unmatched_reason") or "")
    if reason not in REASON_TO_GROUP:
        raise Q5EError(f"row has unmappable reason {reason!r}")
    return REASON_TO_GROUP[reason]


def validate_rows(rows: Sequence[Mapping[str, object]]) -> None:
    """Every row must carry the frozen join-map fields and no sealed column."""
    for row in rows:
        missing = [f for f in BJ.JOIN_MAP_FIELDS if f not in row]
        if missing:
            raise Q5EError(f"join-map row missing fields {missing}")
        banned = [f for f in BJ.JOIN_MAP_BANNED_FIELDS if f in row]
        if banned:
            raise Q5EError(f"join-map row carries sealed columns {banned}")
        if str(row["status"]) not in BJ.STATUSES:
            raise Q5EError(f"unknown status {row['status']!r}")


def _by_record(rows: Sequence[Mapping[str, object]]
               ) -> Dict[str, List[Mapping[str, object]]]:
    out: Dict[str, List[Mapping[str, object]]] = {}
    for row in rows:
        out.setdefault(str(row["record"]), []).append(row)
    return out


def record_stratum(record: str) -> str:
    """`equal_count` or `mismatched_count`, from the frozen ledger."""
    return (BJ.STRATUM_MISMATCH if str(record) in BJ.MAMBA_COUNT_DELTA
            else BJ.STRATUM_EQUAL)


# ─────────────────────────────────────────────────────────────────────────────
# QA — reproduction targets, checked before any measurement
# ─────────────────────────────────────────────────────────────────────────────
def observed_qa_counts(rows: Sequence[Mapping[str, object]]) -> Dict[str, int]:
    failed = [r for r in rows if is_failed(r)]
    counts = {
        "total_failure_rows": len(failed),
        "mamba_side_failure_rows": sum(1 for r in failed if is_mamba_side(r)),
        "cache_side_failure_rows": sum(1 for r in failed if is_cache_side(r)),
        "ds1_records": len({str(r["record"]) for r in rows}),
    }
    for reason in (BJ.REASON_NO_EDGE, BJ.REASON_NOT_OPTIMAL,
                   BJ.REASON_AMBIGUOUS):
        counts[reason] = sum(
            1 for r in failed
            if str(r["drop_or_unmatched_reason"]) == reason)
    return counts


def verify_qa_targets(rows: Sequence[Mapping[str, object]],
                      decision: Mapping[str, object],
                      manifest: Mapping[str, object]) -> Dict[str, object]:
    """Reproduce every registered QA target.  One mismatch stops the audit."""
    validate_rows(rows)
    observed = observed_qa_counts(rows)
    targets: Dict[str, Dict[str, object]] = {}
    for name, expected in QA_TARGETS.items():
        got = observed.get(name)
        targets[name] = {"expected": expected, "observed": got,
                         "ok": got == expected}
    fingerprint = str(decision.get("rule_fingerprint")
                      or manifest.get("rule_fingerprint") or "")
    targets["rule_fingerprint"] = {
        "expected": REGISTERED_RULE_FINGERPRINT, "observed": fingerprint,
        "ok": fingerprint == REGISTERED_RULE_FINGERPRINT}
    code = str(manifest.get("code_sha256") or "")
    targets["producing_code_sha256"] = {
        "expected": PRODUCING_CODE_SHA256, "observed": code,
        "ok": code == PRODUCING_CODE_SHA256}
    ok = all(entry["ok"] for entry in targets.values())
    return {"targets": targets, "ok": ok,
            "first_failure": None if ok else
            sorted(k for k, v in targets.items() if not v["ok"])[0]}


def verify_bundle_is_canonical(directory: str, approval: Optional[str]
                               ) -> Dict[str, object]:
    """Canonicity is established by digest and marker absence, never by path."""
    require_execution_approval(approval, f"canonical bundle at {directory!r}")
    superseded = os.path.join(directory, SUPERSEDED_MARKER)
    problems: List[str] = []
    if os.path.exists(superseded):
        problems.append(
            f"{SUPERSEDED_MARKER} present: this is a superseded bundle")
    files: List[Dict[str, object]] = []
    for name in BUNDLE_INPUT_FILES:
        path = os.path.join(directory, name)
        if not os.path.exists(path):
            problems.append(f"missing registered input {name}")
            continue
        files.append({"name": name, "bytes": os.path.getsize(path),
                      "sha256": sha256_file(path)})
    manifest_path = os.path.join(directory, "manifest.json")
    code = ""
    if os.path.exists(manifest_path):
        with open(manifest_path, encoding="utf-8") as handle:
            code = str(json.load(handle).get("code_sha256") or "")
        if code != PRODUCING_CODE_SHA256:
            problems.append(
                f"manifest code_sha256 {code!r} != {PRODUCING_CODE_SHA256}")
    return {"directory": directory, "files": files, "code_sha256": code,
            "problems": problems, "ok": not problems}


# ─────────────────────────────────────────────────────────────────────────────
# M0 — failure topology of the existing canonical bundle
# ─────────────────────────────────────────────────────────────────────────────
def m0_class_failure_rate(rows: Sequence[Mapping[str, object]]
                          ) -> Dict[str, Dict[str, float]]:
    """M0.1 — mamba-side per-class failure rate over all mamba rows of that class."""
    out: Dict[str, Dict[str, float]] = {}
    for cls in AAMI_CLASSES:
        rows_c = [r for r in rows
                  if is_mamba_side(r) and str(r.get("mamba_aami") or "") == cls]
        failures = sum(1 for r in rows_c if is_failed(r))
        out[cls] = {"denominator": len(rows_c), "failures": failures,
                    "rate": _ratio(failures, len(rows_c))}
    return out


def m0_class_by_reason(rows: Sequence[Mapping[str, object]],
                       processed_classes: Mapping[Tuple[str, int], str]
                       ) -> Dict[str, Dict[str, Dict[str, object]]]:
    """M0.2 — class x failure-reason contingency, per side, never summed."""
    out: Dict[str, Dict[str, Dict[str, object]]] = {
        side: {cls: {} for cls in AAMI_CLASSES} for side in SIDES}
    for side in SIDES:
        for cls in AAMI_CLASSES:
            selected = [r for r in rows
                        if (is_mamba_side(r) if side == SIDE_MAMBA
                            else is_cache_side(r))
                        and row_class(r, side, processed_classes) == cls]
            failed = [r for r in selected if is_failed(r)]
            denominator = len(failed)
            for reason in (BJ.REASON_NO_EDGE, BJ.REASON_NOT_OPTIMAL,
                           BJ.REASON_AMBIGUOUS):
                count = sum(1 for r in failed
                            if str(r["drop_or_unmatched_reason"]) == reason)
                out[side][cls][reason] = {
                    "count": count, "denominator": denominator,
                    "share": _ratio(count, denominator)}
            out[side][cls]["_rows"] = len(selected)
    return out


def row_class(row: Mapping[str, object], side: str,
              processed_classes: Mapping[Tuple[str, int], str]) -> str:
    """Class of a row on the stated side.

    A mamba-side row carries its Leg 1 class.  A cache-side row has none by
    construction and may be supplied **only** from the canonical DS1
    processed-class map; it is never estimated and never filled from a
    certified neighbour.
    """
    if side == SIDE_MAMBA:
        return str(row.get("mamba_aami") or "")
    key = row.get("cache_record_row")
    if key is None:
        return ""
    return processed_classes.get((str(row["record"]), int(key)), "")


def _runs_from_positions(positions: Sequence[int]) -> List[Tuple[int, int]]:
    """Maximal runs of exactly consecutive integers as ``(start, length)``."""
    if not positions:
        return []
    ordered = sorted(set(int(p) for p in positions))
    runs: List[Tuple[int, int]] = []
    start = previous = ordered[0]
    for value in ordered[1:]:
        if value == previous + 1:
            previous = value
            continue
        runs.append((start, previous - start + 1))
        start = previous = value
    runs.append((start, previous - start + 1))
    return runs


def failure_runs(rows: Sequence[Mapping[str, object]],
                 adjacency: str = ADJ_PRIMARY
                 ) -> Dict[str, List[Tuple[int, int]]]:
    """Runs of failed mamba-side rows, per record, under one adjacency.

    Cache-side rows have no ordinal by construction and are excluded; a missing
    ordinal is never bridged by time adjacency.  Runs never cross a record
    boundary.
    """
    if adjacency not in ADJACENCIES:
        raise Q5EError(f"unknown adjacency {adjacency!r}")
    out: Dict[str, List[Tuple[int, int]]] = {}
    for record, group in _by_record(rows).items():
        positions = [int(r[adjacency]) for r in group
                     if is_mamba_side(r) and is_failed(r)
                     and r.get(adjacency) is not None]
        out[record] = _runs_from_positions(positions)
    return out


def _run_bucket(length: int) -> str:
    if length == 1:
        return "1"
    if length == 2:
        return "2"
    return "3-9" if length <= 9 else ">=10"


def summarise_runs(runs_by_record: Mapping[str, Sequence[Tuple[int, int]]],
                   total_failed: int) -> Dict[str, object]:
    lengths = [length for runs in runs_by_record.values() for _, length in runs]
    buckets = {name: 0 for name in RUN_BUCKETS}
    for length in lengths:
        buckets[_run_bucket(length)] += 1
    in_long = sum(length for length in lengths if length >= LONG_RUN_MIN)
    return {"buckets": buckets, "n_runs": len(lengths),
            "median": median(lengths), "p90": percentile(lengths, 90.0),
            "max": max(lengths) if lengths else 0,
            "rows_in_long_runs": in_long,
            "share_in_long_runs": _ratio(in_long, total_failed)}


def m0_runs(rows: Sequence[Mapping[str, object]]) -> Dict[str, object]:
    """M0.4 — primary mamba-row runs plus the non-decisional raw-ordinal audit."""
    failed_mamba = sum(1 for r in rows if is_mamba_side(r) and is_failed(r))
    out: Dict[str, object] = {}
    for adjacency in ADJACENCIES:
        runs = failure_runs(rows, adjacency)
        summary = summarise_runs(runs, failed_mamba)
        summary["adjacency_definition"] = adjacency
        summary["decisional"] = adjacency == ADJ_PRIMARY
        summary["per_record"] = {
            record: summarise_runs({record: value}, sum(
                1 for r in rows if str(r["record"]) == record
                and is_mamba_side(r) and is_failed(r)))
            for record, value in runs.items()}
        out[adjacency] = summary
    return out


def m0_post_v_failure(rows: Sequence[Mapping[str, object]],
                      adjacency: str = ADJ_PRIMARY) -> Dict[str, object]:
    """M0.5 — failure share of the next kept beat after a failed beat of class c."""
    out: Dict[str, object] = {"adjacency_definition": adjacency,
                              "decisional": adjacency == ADJ_PRIMARY}
    index: Dict[Tuple[str, int], Mapping[str, object]] = {}
    for row in rows:
        if is_mamba_side(row) and row.get(adjacency) is not None:
            index[(str(row["record"]), int(row[adjacency]))] = row
    for cls in AAMI_CLASSES:
        numerator = denominator = 0
        for row in rows:
            if not (is_mamba_side(row) and is_failed(row)):
                continue
            if str(row.get("mamba_aami") or "") != cls:
                continue
            if row.get(adjacency) is None:
                continue
            nxt = index.get((str(row["record"]), int(row[adjacency]) + 1))
            if nxt is None:
                continue
            denominator += 1
            if is_failed(nxt):
                numerator += 1
        out[cls] = {"numerator": numerator, "denominator": denominator,
                    "share": _ratio(numerator, denominator)}
    mamba_rows = [r for r in rows if is_mamba_side(r)]
    out["reference_unconditional_failure_rate"] = _ratio(
        sum(1 for r in mamba_rows if is_failed(r)), len(mamba_rows))
    return out


def m0_record_class(rows: Sequence[Mapping[str, object]],
                    processed_classes: Mapping[Tuple[str, int], str],
                    record: str) -> Dict[str, Dict[str, Dict[str, float]]]:
    """M0.3 — one record, per class, on both sides."""
    out: Dict[str, Dict[str, Dict[str, float]]] = {}
    subset = [r for r in rows if str(r["record"]) == str(record)]
    for side in SIDES:
        out[side] = {}
        for cls in AAMI_CLASSES:
            selected = [r for r in subset
                        if (is_mamba_side(r) if side == SIDE_MAMBA
                            else is_cache_side(r))
                        and row_class(r, side, processed_classes) == cls]
            failures = sum(1 for r in selected if is_failed(r))
            out[side][cls] = {"denominator": len(selected),
                              "failures": failures,
                              "rate": _ratio(failures, len(selected))}
    return out


def m0_strata(rows: Sequence[Mapping[str, object]]) -> Dict[str, object]:
    """M0.6 — the two count strata, always separated, plus pooled."""
    out: Dict[str, object] = {}
    for stratum in (BJ.STRATUM_EQUAL, BJ.STRATUM_MISMATCH, "pooled"):
        if stratum == "pooled":
            subset = list(rows)
        else:
            subset = [r for r in rows
                      if record_stratum(str(r["record"])) == stratum]
        records = {str(r["record"]) for r in subset}
        failed = [r for r in subset if is_failed(r)]
        out[stratum] = {
            "records": len(records),
            "rows": len(subset),
            "failures": len(failed),
            "rate": _ratio(len(failed), len(subset)),
            "mamba_side_failures": sum(1 for r in failed if is_mamba_side(r)),
            "cache_side_failures": sum(1 for r in failed if is_cache_side(r)),
        }
    return out


def m0_report(rows: Sequence[Mapping[str, object]],
              processed_classes: Mapping[Tuple[str, int], str]
              ) -> Dict[str, object]:
    """The complete M0 block, in the registered schema field names."""
    runs = m0_runs(rows)
    return {
        "class_failure_rate": m0_class_failure_rate(rows),
        "class_by_reason": m0_class_by_reason(rows, processed_classes),
        "record_208": m0_record_class(rows, processed_classes, "208"),
        "record_116": m0_record_class(rows, processed_classes, "116"),
        "runs_primary_mamba_row": runs[ADJ_PRIMARY],
        "runs_secondary_raw_ordinal": runs[ADJ_SECONDARY],
        "post_v_failure": {
            ADJ_PRIMARY: m0_post_v_failure(rows, ADJ_PRIMARY),
            ADJ_SECONDARY: m0_post_v_failure(rows, ADJ_SECONDARY)},
        "strata": m0_strata(rows),
    }


# ─────────────────────────────────────────────────────────────────────────────
# M1 — nearest-candidate distance
# ─────────────────────────────────────────────────────────────────────────────
def rank_proportional_centre(j: int, n_mamba: int, n_cache: int) -> int:
    """Rank-proportional mamba centre for cache row ``j``, round-half-to-even."""
    if n_cache <= 1:
        return 0
    exact = j * (n_mamba - 1) / (n_cache - 1)
    return int(BJ.to_samples(exact, BJ.UNIT_SAMPLES))


def _bin_for(distance: int) -> str:
    for name, low, high in M1_BINS:
        if distance >= low and (high is None or distance <= high):
            return name
    raise Q5EError(f"distance {distance} fell outside the registered bins")


def m1_distances(rows: Sequence[Mapping[str, object]],
                 mamba_rr: Mapping[str, Tuple[Sequence[int], Sequence[int]]],
                 cache_rr: Mapping[str, Tuple[Sequence[int], Sequence[int]]],
                 processed_classes: Mapping[Tuple[str, int], str]
                 ) -> List[Dict[str, object]]:
    """Nearest-candidate `d_inf` for every non-certified cache row.

    The window is the registered fixed half-width; a minimiser sitting on the
    boundary is `CENSORED_AT_WINDOW_BOUNDARY` and never treated as if the
    window had been wide enough.  A stored `0.0` endpoint is
    `CACHE_ENDPOINT_ZERO`: real data meaning "no neighbour", kept in
    descriptive tables and excluded from every H1/H3 distance statistic.
    """
    out: List[Dict[str, object]] = []
    for row in rows:
        if not (is_cache_side(row) and is_failed(row)):
            continue
        record = str(row["record"])
        j = int(row["cache_record_row"])
        m_pre, m_post = mamba_rr[record]
        c_pre, c_post = cache_rr[record]
        n_m, n_c = len(m_pre), len(c_pre)
        centre = rank_proportional_centre(j, n_m, n_c)
        low = max(0, centre - M1_WINDOW_HALF_WIDTH)
        high = min(n_m - 1, centre + M1_WINDOW_HALF_WIDTH)
        best, best_i = None, None
        for i in range(low, high + 1):
            distance = max(abs(m_pre[i] - c_pre[j]), abs(m_post[i] - c_post[j]))
            if best is None or distance < best:
                best, best_i = distance, i
        if best is None:
            raise Q5EError(f"{record}: empty M1 window for cache row {j}")
        censored = abs(best_i - centre) == M1_WINDOW_HALF_WIDTH
        endpoint_zero = (c_pre[j] == 0) or (c_post[j] == 0)
        out.append({
            "record": record, "cache_record_row": j,
            "processed_class": processed_classes.get((record, j), ""),
            "reason": str(row["drop_or_unmatched_reason"]),
            "d_inf": int(best), "bin": _bin_for(int(best)),
            "censored": bool(censored),
            "cache_endpoint_zero": bool(endpoint_zero),
            "included_in_distance_gate": not (censored or endpoint_zero),
        })
    return out


def m1_summary(distances: Sequence[Mapping[str, object]]) -> Dict[str, object]:
    bins = {name: 0 for name, _, _ in M1_BINS}
    gate_bins = {name: 0 for name, _, _ in M1_BINS}
    for entry in distances:
        bins[str(entry["bin"])] += 1
        if entry["included_in_distance_gate"]:
            gate_bins[str(entry["bin"])] += 1
    endpoint = [e for e in distances if e["cache_endpoint_zero"]]
    return {
        "bins": bins, "bins_in_distance_gate": gate_bins,
        "censored": sum(1 for e in distances if e["censored"]),
        "cache_endpoint_zero": len(endpoint),
        "h3_endpoint_component": {
            "count": len(endpoint),
            "share_of_non_certified_cache_rows": _ratio(
                len(endpoint), len(distances)),
            "note": ("descriptive only; cannot fire H3 and is never folded "
                     "into the >100-sample evidence gate")},
        "window_half_width": M1_WINDOW_HALF_WIDTH,
        "n_rows": len(distances),
    }


def distance_gate_rows(distances: Sequence[Mapping[str, object]]
                       ) -> List[Mapping[str, object]]:
    """The exact population every H1/H3 distance statistic and null may use."""
    return [e for e in distances if e["included_in_distance_gate"]]


# ─────────────────────────────────────────────────────────────────────────────
# M2 — failure adjacency and runs
# ─────────────────────────────────────────────────────────────────────────────
def neighbourhood_report(rows: Sequence[Mapping[str, object]],
                         radius: int, adjacency: str = ADJ_PRIMARY
                         ) -> Dict[str, Dict[str, float]]:
    """Failure topology of the +/-radius neighbourhood of each failed beat."""
    index: Dict[Tuple[str, int], Mapping[str, object]] = {}
    for row in rows:
        if is_mamba_side(row) and row.get(adjacency) is not None:
            index[(str(row["record"]), int(row[adjacency]))] = row
    out: Dict[str, Dict[str, float]] = {}
    for cls in AAMI_CLASSES:
        present = failed = anchors = 0
        for row in rows:
            if not (is_mamba_side(row) and is_failed(row)):
                continue
            if str(row.get("mamba_aami") or "") != cls:
                continue
            if row.get(adjacency) is None:
                continue
            anchors += 1
            base = int(row[adjacency])
            for offset in range(-radius, radius + 1):
                if offset == 0:
                    continue
                neighbour = index.get((str(row["record"]), base + offset))
                if neighbour is None:
                    continue
                present += 1
                if is_failed(neighbour):
                    failed += 1
        out[cls] = {"anchors": anchors, "neighbours_present": present,
                    "neighbours_failed": failed,
                    "failure_share": _ratio(failed, present)}
    return out


def m2_report(rows: Sequence[Mapping[str, object]]) -> Dict[str, object]:
    out: Dict[str, object] = {"adjacency_primary": ADJ_PRIMARY}
    runs = m0_runs(rows)
    out["runs"] = runs[ADJ_PRIMARY]
    out["raw_ordinal_sensitivity"] = runs[ADJ_SECONDARY]
    for radius in NEIGHBOURHOODS:
        out[f"v_neighbourhood_pm{radius}"] = {
            adjacency: neighbourhood_report(rows, radius, adjacency)
            for adjacency in ADJACENCIES}
    return out


# ─────────────────────────────────────────────────────────────────────────────
# M3 — frozen candidate graph, reconstructed and never redesigned
# ─────────────────────────────────────────────────────────────────────────────
def _local_rr_sd(pre: Sequence[int], index: int) -> float:
    low = max(0, index - LOCAL_RR_HALF_WINDOW)
    high = min(len(pre) - 1, index + LOCAL_RR_HALF_WINDOW)
    window = [float(pre[k]) for k in range(low, high + 1)]
    if len(window) <= 1:
        return 0.0
    return float(statistics.pstdev(window))


def _pair_multiplicity(pre: Sequence[int], post: Sequence[int]
                       ) -> Dict[int, int]:
    counts: Dict[Tuple[int, int], int] = {}
    for k in range(len(pre)):
        counts[(pre[k], post[k])] = counts.get((pre[k], post[k]), 0) + 1
    return {k: counts[(pre[k], post[k])] for k in range(len(pre))}


def graph_metrics_for_record(mamba: "BJ.RecordSequence",
                             cache: "BJ.RecordSequence"
                             ) -> Dict[str, object]:
    """Reconstruct the frozen candidate graph for one record.

    ``candidate_edges`` and ``match_record`` are called **unchanged**.  Nothing
    is selected: no new matching is chosen, no arbitrary maximum path is
    promoted, no edge is re-certified.
    """
    result = BJ.match_record(mamba, cache)
    edges = result.edges
    degree_m: Dict[int, int] = {}
    degree_c: Dict[int, int] = {}
    for i, j in edges:
        degree_m[i] = degree_m.get(i, 0) + 1
        degree_c[j] = degree_c.get(j, 0) + 1
    usable = set(result.certified) | set(result.ambiguous)
    usable_m: Dict[int, int] = {}
    usable_c: Dict[int, int] = {}
    for i, j in usable:
        usable_m[i] = usable_m.get(i, 0) + 1
        usable_c[j] = usable_c.get(j, 0) + 1
    forced_m = {i for i, _ in result.certified}
    forced_c = {j for _, j in result.certified}
    mult_m = _pair_multiplicity(mamba.pre_samples, mamba.post_samples)
    mult_c = _pair_multiplicity(cache.pre_samples, cache.post_samples)
    return {
        "result": result,
        SIDE_MAMBA: {
            i: {"candidate_degree": degree_m.get(i, 0),
                "usable_edges": usable_m.get(i, 0),
                "has_forced_rank": i in forced_m,
                "rr_pair_multiplicity": mult_m[i],
                "local_rr_sd": _local_rr_sd(mamba.pre_samples, i)}
            for i in range(len(mamba))},
        SIDE_CACHE: {
            j: {"candidate_degree": degree_c.get(j, 0),
                "usable_edges": usable_c.get(j, 0),
                "has_forced_rank": j in forced_c,
                "rr_pair_multiplicity": mult_c[j],
                "local_rr_sd": _local_rr_sd(cache.pre_samples, j)}
            for j in range(len(cache))},
    }


def derive_cache_side_groups(rows: Sequence[Mapping[str, object]],
                             cache_n: Mapping[str, int]
                             ) -> Dict[Tuple[str, int], str]:
    """Q4 — one cache-side `CERTIFIED` row per certified mamba row, asserted.

    Together the four cache-side groups must form a disjoint, exhaustive
    partition of cache rows.  Any collision, duplicate, omission or count
    mismatch is `DIAGNOSTIC_INPUT_MISMATCH`.
    """
    groups: Dict[Tuple[str, int], str] = {}
    certified_pairs = 0
    for row in rows:
        record = str(row["record"])
        if is_mamba_side(row):
            if is_failed(row):
                continue                       # failed mamba rows are not cache rows
            key = row.get("cache_record_row")
            if key is None:
                raise DiagnosticInputMismatch(
                    f"{record}: certified mamba row without cache_record_row")
            pair = (record, int(key))
            if pair in groups:
                raise DiagnosticInputMismatch(
                    f"{record}: duplicate certified cache row {key}")
            groups[pair] = GROUP_CERTIFIED
            certified_pairs += 1
            continue
        pair = (record, int(row["cache_record_row"]))
        if pair in groups:
            raise DiagnosticInputMismatch(
                f"{record}: collision on cache row {pair[1]}")
        groups[pair] = row_group(row)
    for record, n in cache_n.items():
        for j in range(int(n)):
            if (record, j) not in groups:
                raise DiagnosticInputMismatch(
                    f"{record}: cache row {j} belongs to no group")
    if len(groups) != sum(int(n) for n in cache_n.values()):
        raise DiagnosticInputMismatch(
            f"cache-side partition has {len(groups)} rows, ledger says "
            f"{sum(int(n) for n in cache_n.values())}")
    return groups


def m3_graph(rows: Sequence[Mapping[str, object]],
             mamba_by_record: Mapping[str, "BJ.RecordSequence"],
             cache_by_record: Mapping[str, "BJ.RecordSequence"]
             ) -> Dict[str, object]:
    """Per-row graph metrics on both sides, grouped, with the QA partition check."""
    per_row: List[Dict[str, object]] = []
    partition_ok = True
    problems: List[str] = []
    mamba_groups: Dict[Tuple[str, int], str] = {}
    for row in rows:
        if is_mamba_side(row):
            mamba_groups[(str(row["record"]), int(row["mamba_record_row"]))] = \
                row_group(row)
    cache_groups = derive_cache_side_groups(
        rows, {r: len(c) for r, c in cache_by_record.items()})

    for record in sorted(mamba_by_record):
        metrics = graph_metrics_for_record(
            mamba_by_record[record], cache_by_record[record])
        result = metrics["result"]
        observed = {
            GROUP_CERTIFIED: len(result.certified),
            GROUP_AMBIGUOUS: len(result.ambiguous)}
        expected_certified = sum(
            1 for (r, _), g in cache_groups.items()
            if r == record and g == GROUP_CERTIFIED)
        if observed[GROUP_CERTIFIED] != expected_certified:
            partition_ok = False
            problems.append(
                f"{record}: reconstructed certified {observed[GROUP_CERTIFIED]}"
                f" != bundle {expected_certified}")
        for side, table in ((SIDE_MAMBA, metrics[SIDE_MAMBA]),
                            (SIDE_CACHE, metrics[SIDE_CACHE])):
            for index, values in table.items():
                group = (mamba_groups.get((record, index)) if side == SIDE_MAMBA
                         else cache_groups.get((record, index)))
                if group is None:
                    continue
                per_row.append({"record": record, "side": side, "row": index,
                                "group": group,
                                # The mamba side is descriptive: it never
                                # reaches an H4 p-value, q99, effect gate,
                                # Holm value, flag or the decision tree.
                                "decisional": side == H4_DECISIONAL_SIDE,
                                **values})
    by_group = {
        side: {group: _summarise_group(
            [r for r in per_row if r["side"] == side and r["group"] == group])
            for group in M3_GROUPS}
        for side in SIDES}
    return {"rows": per_row, "by_group": by_group,
            "partition_ok": partition_ok, "problems": problems,
            "h4_decisional_side": H4_DECISIONAL_SIDE,
            "non_decisional_sides": [s for s in SIDES
                                     if s != H4_DECISIONAL_SIDE]}


def _summarise_group(entries: Sequence[Mapping[str, object]]
                     ) -> Dict[str, object]:
    degrees = [float(e["candidate_degree"]) for e in entries]
    mult = [float(e["rr_pair_multiplicity"]) for e in entries]
    sds = [float(e["local_rr_sd"]) for e in entries]
    return {
        "n": len(entries),
        "candidate_degree": {"median": median(degrees),
                             "p25": percentile(degrees, 25.0),
                             "p75": percentile(degrees, 75.0),
                             "ecdf": ecdf(degrees)},
        "share_degree_ge_2": _ratio(
            sum(1 for d in degrees if d >= H4_DEGREE_MIN), len(degrees)),
        "rr_pair_multiplicity_median": median(mult),
        "local_rr_sd_median": median(sds),
        "has_forced_rank": sum(1 for e in entries if e["has_forced_rank"]),
        "usable_edges_median": median(
            [float(e["usable_edges"]) for e in entries]),
    }


# ─────────────────────────────────────────────────────────────────────────────
# M4 — feasibility gate first, anchors only afterwards
# ─────────────────────────────────────────────────────────────────────────────
def verify_registered_runtime(observed: Mapping[str, str]) -> Dict[str, object]:
    """M4.0 condition 2, sub-gate 1.  Exact match; no fallback runtime."""
    mismatches = {}
    for key in M4_RUNTIME_REQUIRED:
        want = M4_REGISTERED_RUNTIME[key]
        got = str(observed.get(key, ""))
        if got != want:
            mismatches[key] = {"expected": want, "observed": got}
    return {"gate": "runtime", "required": dict(M4_REGISTERED_RUNTIME),
            "observed": dict(observed), "mismatches": mismatches,
            "ok": not mismatches,
            "reason": None if not mismatches else M4_RUNTIME_UNAVAILABLE}


def verify_source_map(sources: Mapping[str, str],
                      texts: Mapping[str, str]) -> Dict[str, object]:
    """M4.0 condition 1.  Digest first, then function/call-site mapping.

    Keyword presence alone is explicitly insufficient: each contract entry must
    be found **inside** the named function body, not merely somewhere in the
    file.
    """
    problems: List[str] = []
    for name, want in M4_SOURCE_MAP_HASHES.items():
        got = str(sources.get(name, ""))
        if got != want:
            problems.append(f"{name}: sha256 {got!r} != registered {want!r}")
    mapping: List[Dict[str, object]] = []
    for name, function, token in M4_SOURCE_MAP_CONTRACT:
        body = _function_body(texts.get(name, ""), function)
        found = body is not None and token in body
        mapping.append({"file": name, "function": function, "token": token,
                        "found": bool(found)})
        if not found:
            problems.append(f"{name}::{function} does not contain {token!r}")
    return {"gate": "source_map", "mapping": mapping, "problems": problems,
            "ok": not problems,
            "reason": None if not problems else M4_SOURCE_MAP_UNVERIFIED}


def _function_body(text: str, function: str) -> Optional[str]:
    """Body of ``def <function>`` up to the next top-level ``def``/``class``."""
    if not text:
        return None
    lines = text.splitlines()
    start = None
    for index, line in enumerate(lines):
        stripped = line.lstrip()
        if stripped.startswith(f"def {function}(") or \
                stripped.startswith(f"def {function} ("):
            start = index
            indent = len(line) - len(stripped)
            break
    if start is None:
        return None
    body = [lines[start]]
    for line in lines[start + 1:]:
        if line.strip() and (len(line) - len(line.lstrip())) <= indent and \
                line.lstrip().startswith(("def ", "class ")):
            break
        body.append(line)
    return "\n".join(body)


def verify_detector_counts(observed: Mapping[str, int],
                           registered: Mapping[str, int]) -> Dict[str, object]:
    """22/22 DS1 record counts, exactly.  A partial pass is not a pass."""
    mismatches = {r: {"expected": int(registered[r]),
                      "observed": int(observed.get(r, -1))}
                  for r in sorted(registered)
                  if int(observed.get(r, -1)) != int(registered[r])}
    return {"gate": "record_counts", "n_records": len(registered),
            "n_matching": len(registered) - len(mismatches),
            "mismatches": mismatches, "ok": not mismatches,
            "reason": None if not mismatches else M4_COUNT_MISMATCH}


def verify_rr_equality(replayed: Mapping[str, Sequence[Sequence[float]]],
                       frozen: Mapping[str, Sequence[Sequence[float]]]
                       ) -> Dict[str, object]:
    """Exact equality against the frozen V10 RR arrays.

    Paired NaNs count as equal, exactly as `PREP_M4_RR_EQUIVALENCE` registered.
    No tolerance, rounding, repair or lineage selection.
    """
    first = None
    n_ok = 0
    for record in sorted(frozen):
        a, b = replayed.get(record), frozen[record]
        if a is None or len(a) != len(b):
            first = first or {"record": record, "reason": "SHAPE"}
            continue
        ok = True
        for r, (row_a, row_b) in enumerate(zip(a, b)):
            if len(row_a) != len(row_b):
                ok = False
                first = first or {"record": record, "row": r, "reason": "SHAPE"}
                break
            for c, (x, y) in enumerate(zip(row_a, row_b)):
                same = (x == y) or (_isnan(x) and _isnan(y))
                if not same:
                    ok = False
                    first = first or {"record": record, "row": r, "col": c,
                                      "replayed": repr(x), "frozen": repr(y)}
                    break
            if not ok:
                break
        n_ok += 1 if ok else 0
    ok = n_ok == len(frozen)
    return {"gate": "rr_equality", "n_records": len(frozen), "n_identical": n_ok,
            "first_mismatch": first, "ok": ok,
            "reason": None if ok else M4_RR_MISMATCH}


def _isnan(value: object) -> bool:
    try:
        return math.isnan(float(value))
    except (TypeError, ValueError):
        return False


def verify_m4_input_identity(observed: Mapping[str, str],
                             rr_verdict: str) -> Dict[str, object]:
    """M4.0 condition 3.  V9 is never substituted for V10."""
    problems = []
    for key in ("v10_source", "v10_cache"):
        want = str(M4_INPUT_CONTRACT[key]["aggregate"])
        got = str(observed.get(key, ""))
        if got != want:
            problems.append(f"{key}: aggregate {got!r} != registered {want!r}")
    if rr_verdict != PREP_M4_RR_EQUIVALENCE_VERDICT:
        problems.append(
            f"PREP_M4_RR_EQUIVALENCE verdict {rr_verdict!r} != "
            f"{PREP_M4_RR_EQUIVALENCE_VERDICT!r}")
    return {"gate": "input_identity", "problems": problems, "ok": not problems,
            "reason": None if not problems else M4_IDENTITY_MISMATCH}


def m4_feasibility_gate(runtime: Mapping[str, str],
                        sources: Mapping[str, str],
                        texts: Mapping[str, str],
                        detector_counts: Optional[Mapping[str, int]],
                        registered_counts: Mapping[str, int],
                        replayed_rr: Optional[Mapping[str, object]],
                        frozen_rr: Mapping[str, object],
                        input_identity: Mapping[str, str],
                        rr_verdict: str,
                        replay: Optional[object] = None) -> Dict[str, object]:
    """Evaluate M4.0 **in the registered order**, stopping at the first failure.

    The order is itself part of the contract: the runtime and the static source
    map are verified *before* any detector call, and no anchor may be computed
    until every sub-gate has passed.  A failure yields
    `DIAGNOSTIC_INPUT_ABSENT`; there is no fallback runtime, no approximate
    count match, no partial-record pass and no post-hoc repair.
    """
    gates: List[Dict[str, object]] = []
    identity = verify_m4_input_identity(input_identity, rr_verdict)

    step = verify_registered_runtime(runtime)
    gates.append(step)
    if not step["ok"]:
        return _m4_absent(gates, identity, step["reason"])

    step = verify_source_map(sources, texts)
    gates.append(step)
    if not step["ok"]:
        return _m4_absent(gates, identity, step["reason"])

    if not identity["ok"]:
        gates.append(identity)
        return _m4_absent(gates, identity, identity["reason"])

    # Only now may the detector run.  `replay` is injected so the gate is
    # testable without ever calling `detect_r()` in this PR.
    if detector_counts is None and replay is not None:
        detector_counts, replayed_rr = replay()
    if detector_counts is None:
        gates.append({"gate": "detector_replay", "ok": False,
                      "reason": M4_COUNT_MISMATCH,
                      "problems": ["detector replay produced no counts"]})
        return _m4_absent(gates, identity, M4_COUNT_MISMATCH)
    gates.append({"gate": "detector_replay", "ok": True, "reason": None})

    step = verify_detector_counts(detector_counts, registered_counts)
    gates.append(step)
    if not step["ok"]:
        return _m4_absent(gates, identity, step["reason"])

    step = verify_rr_equality(replayed_rr or {}, frozen_rr)
    gates.append(step)
    if not step["ok"]:
        return _m4_absent(gates, identity, step["reason"])

    return {"status": M4_OK, "gates": gates, "identity": identity,
            "order": list(M4_GATE_ORDER), "first_failure": None}


def _m4_absent(gates: Sequence[Mapping[str, object]],
               identity: Mapping[str, object],
               reason: Optional[str]) -> Dict[str, object]:
    return {"status": M4_INPUT_ABSENT, "gates": list(gates),
            "identity": identity, "order": list(M4_GATE_ORDER),
            "first_failure": reason}


def m4_anchors(gate: Mapping[str, object],
               anchors_by_record: Mapping[str, Sequence[Mapping[str, object]]],
               rows: Sequence[Mapping[str, object]]) -> Dict[str, object]:
    """M4.1 — anchor placement and post-anchor topology.

    Refuses to run unless the feasibility gate returned `OK`: no anchor may be
    computed before M4.0 passes, and that ordering is asserted here as well as
    in the caller.
    """
    if str(gate.get("status")) != M4_OK:
        raise Q5EError(
            f"m4_anchors called with gate status {gate.get('status')!r}; "
            f"M4.0 must pass before any anchor is computed")
    index: Dict[Tuple[str, int], Mapping[str, object]] = {}
    for row in rows:
        if is_mamba_side(row):
            index[(str(row["record"]), int(row["mamba_record_row"]))] = row
    offsets = {o: {"present": 0, "failed": 0}
               for o in range(-M4_ANCHOR_HALF_WINDOW, M4_ANCHOR_HALF_WINDOW + 1)}
    detail: List[Dict[str, object]] = []
    explained: set = set()
    n_anchors = excluded = 0
    for record, anchors in sorted(anchors_by_record.items()):
        for anchor in anchors:
            placement = anchor.get("mapped_mamba_record_row")
            if placement is None:
                excluded += 1
                continue
            n_anchors += 1
            base = int(placement)
            if anchor.get("anchor_kind") == "annotation_without_peak" and \
                    anchor.get("counterpart_kept"):
                explained.add((record, base))
            for offset in offsets:
                neighbour = index.get((record, base + offset))
                if neighbour is None:
                    continue
                offsets[offset]["present"] += 1
                failed = is_failed(neighbour)
                offsets[offset]["failed"] += 1 if failed else 0
                detail.append({
                    "record": record,
                    "anchor_ordinal": anchor.get("anchor_ordinal"),
                    "anchor_sample": anchor.get("anchor_sample"),
                    "anchor_kind": anchor.get("anchor_kind"),
                    "adjacency_definition": ADJ_PRIMARY,
                    "offset": offset,
                    "mapped_mamba_record_row": base,
                    "failed": bool(failed), "decisional": True})
    after = set()
    for record, anchors in anchors_by_record.items():
        for anchor in anchors:
            placement = anchor.get("mapped_mamba_record_row")
            if placement is None:
                continue
            for offset in range(1, M4_ANCHOR_HALF_WINDOW + 1):
                key = (record, int(placement) + offset)
                if key in index and is_failed(index[key]):
                    after.add(key)
    total_failed = sum(1 for r in rows if is_mamba_side(r) and is_failed(r))
    return {
        "status": M4_OK, "anchors": n_anchors, "excluded_placements": excluded,
        "offset_curve": {str(o): {**v, "share": _ratio(v["failed"], v["present"])}
                         for o, v in sorted(offsets.items())},
        "share_failures_within_10_after": _ratio(len(after), total_failed),
        "explained_positions": sorted(explained),
        "rows": detail,
    }


# ─────────────────────────────────────────────────────────────────────────────
# Negative controls
# ─────────────────────────────────────────────────────────────────────────────
def control_a_class_shift(classes_by_record: Mapping[str, Sequence[str]],
                          replicate: int) -> Dict[str, List[str]]:
    """Control A — within-record circular shift of the class sequence.

    Preserves per-record class composition, failure count and the entire
    failure run structure; breaks only the class-to-position link.
    """
    rng = _rng(CONTROL_A, replicate)
    out: Dict[str, List[str]] = {}
    for record in sorted(classes_by_record):
        values = list(classes_by_record[record])
        n = len(values)
        if n <= 1:
            out[record] = values
            continue
        shift = rng.randrange(1, n)
        out[record] = values[-shift:] + values[:-shift]
    return out


def control_b_status_permutation(
        statuses_by_key: Mapping[Tuple[str, str], Sequence[str]],
        replicate: int) -> Dict[Tuple[str, str], List[str]]:
    """Control B — one joint categorical permutation per ``record x side``.

    A single permutation of the position pool receives the exact multiset
    ``{NO_EDGE x a, NOT_OPTIMAL x b, AMBIGUOUS x c, CERTIFIED x rest}``.
    Permuting reasons independently would let two land on the same row; this
    construction preserves every per-reason count and cannot collide.
    """
    rng = _rng(CONTROL_B, replicate)
    out: Dict[Tuple[str, str], List[str]] = {}
    for key in sorted(statuses_by_key):
        labels = list(statuses_by_key[key])
        rng.shuffle(labels)
        out[key] = labels
    return out


def control_c_anchor_shift(anchors_by_record: Mapping[str, Sequence[int]],
                           record_lengths: Mapping[str, int],
                           replicate: int) -> Dict[str, List[int]]:
    """Control C — within-record circular shift of anchor positions.

    Preserves the per-record anchor count and the whole failure topology,
    breaking only relative position.  Available **only** when M4.0 passes.
    """
    rng = _rng(CONTROL_C, replicate)
    out: Dict[str, List[int]] = {}
    for record in sorted(anchors_by_record):
        n = int(record_lengths.get(record, 0))
        positions = [int(p) for p in anchors_by_record[record]]
        if n <= 1 or not positions:
            out[record] = positions
            continue
        shift = rng.randrange(1, n)
        out[record] = [(p + shift) % n for p in positions]
    return out


def run_null_family(family: str, statistic, replicates: int = N_NULL_REPLICATES
                    ) -> List[float]:
    """Compute one control family's null distribution.

    ``statistic(replicate)`` returns the complete family statistic recomputed
    from that replicate's permuted arrangement.  Nothing is approximated, no
    family is omitted, and the matcher is never re-run inside the loop.
    """
    if family not in CONTROL_FAMILIES:
        raise Q5EError(f"unknown control family {family!r}")
    return [float(statistic(b)) for b in range(int(replicates))]


def permutation_p(observed: float, null: Sequence[float]) -> float:
    """`p = (1 + #{null >= observed}) / (replicates + 1)`."""
    at_least = sum(1 for value in null if float(value) >= float(observed))
    return (1.0 + at_least) / (len(null) + 1.0)


def null_summary(null: Sequence[float]) -> Dict[str, object]:
    return {"replicates": len(null), "master_seed": MASTER_SEED,
            "median": percentile(null, 50.0),
            "q95": percentile(null, 95.0), "q99": percentile(null, 99.0),
            "min": min(null) if null else 0.0,
            "max": max(null) if null else 0.0}


# ─────────────────────────────────────────────────────────────────────────────
# Family statistics
# ─────────────────────────────────────────────────────────────────────────────
def stat_h1(distances: Sequence[Mapping[str, object]],
            class_of: Optional[Mapping[Tuple[str, int], str]] = None) -> float:
    """H1 — `2-5` share among failed V / `NO_EDGE` rows minus the same in non-V.

    Population: cache-side `LEG2_NO_CANDIDATE_EDGE` rows, uncensored and not
    `CACHE_ENDPOINT_ZERO`.  The identical exclusion is applied inside every
    replicate, which is why `class_of` is injected rather than read from the
    row: Control A moves the class, not the distance.
    """
    rows = [e for e in distance_gate_rows(distances)
            if str(e["reason"]) == BJ.REASON_NO_EDGE]
    def _class(entry: Mapping[str, object]) -> str:
        if class_of is None:
            return str(entry["processed_class"])
        return class_of.get(
            (str(entry["record"]), int(entry["cache_record_row"])), "")
    v_rows = [e for e in rows if _class(e) == "V"]
    other = [e for e in rows if _class(e) in ("N", "S")]
    share_v = _ratio(sum(1 for e in v_rows if e["bin"] == M1_GATE_BIN),
                     len(v_rows))
    share_other = _ratio(sum(1 for e in other if e["bin"] == M1_GATE_BIN),
                         len(other))
    return share_v - share_other


def stat_h2(explained_positions: Sequence[Tuple[str, int]],
            no_edge_positions: Sequence[Tuple[str, int]]) -> float:
    """H2 — share of `NO_EDGE` failures explained **at the position level**.

    A record's total row-count deficit is a count, not a location, and is
    excluded from the numerator: seven positions are explained only if replay
    identifies those seven positions.
    """
    explained = set(explained_positions) & set(no_edge_positions)
    return _ratio(len(explained), len(no_edge_positions))


def stat_h3(failures_after_anchor: Sequence[Tuple[str, int]],
            all_failures: Sequence[Tuple[str, int]]) -> float:
    """H3 — share of failures within 10 kept beats after a confirmed anchor."""
    return _ratio(len(set(failures_after_anchor) & set(all_failures)),
                  len(set(all_failures)))


def _degree_median_contrast(
        rows: Sequence[Mapping[str, object]], side: str,
        group_of: Optional[Mapping[Tuple[str, int], str]] = None) -> float:
    """`median(degree | NOT_OPTIMAL + AMBIGUOUS) - median(degree | CERTIFIED)`.

    Private.  Production never selects the side here: :func:`stat_h4` is the
    only decisional caller and it hard-wires :data:`H4_DECISIONAL_SIDE`.  The
    ``side`` parameter exists so the other side can be *reported*, never so a
    caller can choose which contrast decides.
    """
    selected = [r for r in rows if str(r["side"]) == side]

    def _group(entry: Mapping[str, object]) -> str:
        if group_of is None:
            return str(entry["group"])
        return group_of.get((str(entry["record"]), int(entry["row"])),
                            str(entry["group"]))

    failed = [float(r["candidate_degree"]) for r in selected
              if _group(r) in (GROUP_NOT_OPTIMAL, GROUP_AMBIGUOUS)]
    certified = [float(r["candidate_degree"]) for r in selected
                 if _group(r) == GROUP_CERTIFIED]
    return median(failed) - median(certified)


def stat_h4(rows: Sequence[Mapping[str, object]],
            group_of: Optional[Mapping[Tuple[str, int], str]] = None) -> float:
    """H4 — the registered cache-side median contrast.

    **There is no ``side`` argument by design.**  H4 registers one
    family-level statistic and one p-value, and Codex fixed the side to
    :data:`H4_DECISIONAL_SIDE` before any execution, so a production caller
    must not be able to move it.  ``group_of`` is injected so Control B can
    move the status label without ever touching the degree.
    """
    return _degree_median_contrast(rows, H4_DECISIONAL_SIDE, group_of)


def h4_descriptive_by_side(rows: Sequence[Mapping[str, object]]
                           ) -> Dict[str, Dict[str, object]]:
    """Both sides' contrasts, each explicitly tagged with its decisional status.

    The mamba side is reported to preserve the symmetric diagnostic picture of
    the candidate graph.  It is `decisional: false` and never reaches a
    p-value, a q99 comparison, an effect gate, Holm, a flag or the tree.
    """
    return {side: {"median_contrast": _degree_median_contrast(rows, side),
                   "decisional": side == H4_DECISIONAL_SIDE}
            for side in SIDES}


def h4_effect_gates(rows: Sequence[Mapping[str, object]],
                    q99: float, observed: Optional[float] = None
                    ) -> Dict[str, bool]:
    """The registered `H4_ASSOCIATED` effect conditions, cache-side only."""
    selected = [r for r in rows if str(r["side"]) == H4_DECISIONAL_SIDE]
    failed = [r for r in selected
              if str(r["group"]) in (GROUP_NOT_OPTIMAL, GROUP_AMBIGUOUS)]
    certified = [r for r in selected if str(r["group"]) == GROUP_CERTIFIED]
    share = _ratio(sum(1 for r in failed
                       if float(r["candidate_degree"]) >= H4_DEGREE_MIN),
                   len(failed))
    value = stat_h4(rows) if observed is None else float(observed)
    mult_up = (median([float(r["rr_pair_multiplicity"]) for r in failed]) >
               median([float(r["rr_pair_multiplicity"]) for r in certified]))
    sd_down = (median([float(r["local_rr_sd"]) for r in failed]) <
               median([float(r["local_rr_sd"]) for r in certified]))
    return {
        "share_degree_ge_2_at_least_half": bool(share >= EFFECT_SHARE_MIN),
        "exceeds_control_b_q99": bool(value > float(q99)),
        "direction_multiplicity_or_variability": bool(mult_up or sd_down),
    }


def h4_null_statistic(rows: Sequence[Mapping[str, object]], replicate: int
                      ) -> float:
    """One Control B replicate for H4, permuted on the cache side only.

    Control B is registered per ``record x side``; H4 is decided on the cache
    side, so its null permutes the status vector within each
    ``record x cache-side`` block and leaves every degree where it is.
    """
    blocks: Dict[Tuple[str, str], List[str]] = {}
    order: Dict[Tuple[str, str], List[Tuple[str, int]]] = {}
    for entry in rows:
        if str(entry["side"]) != H4_DECISIONAL_SIDE:
            continue
        key = (str(entry["record"]), H4_DECISIONAL_SIDE)
        blocks.setdefault(key, []).append(str(entry["group"]))
        order.setdefault(key, []).append(
            (str(entry["record"]), int(entry["row"])))
    permuted = control_b_status_permutation(blocks, replicate)
    group_of: Dict[Tuple[str, int], str] = {}
    for key, labels in permuted.items():
        for position, label in zip(order[key], labels):
            group_of[position] = label
    return stat_h4(rows, group_of=group_of)


def h4_evaluate(rows: Sequence[Mapping[str, object]],
                replicates: int = N_NULL_REPLICATES) -> Dict[str, object]:
    """The complete H4 family: observed, null, p, q99 and effect gates.

    One function so the decisional side has exactly one source.  Every value
    here is cache-side; the mamba-side contrast is reported alongside as
    `decisional: false` and is not an input to any of it.
    """
    observed = stat_h4(rows)
    null = run_null_family(CONTROL_B, lambda b: h4_null_statistic(rows, b),
                           replicates=replicates)
    summary = null_summary(null)
    gates = h4_effect_gates(rows, summary["q99"], observed)
    return {"decisional_side": H4_DECISIONAL_SIDE,
            "statistic": observed,
            "p": permutation_p(observed, null),
            "q99": summary["q99"], "null_summary": summary,
            "effect_gates": gates,
            "by_side_descriptive": h4_descriptive_by_side(rows)}


# ─────────────────────────────────────────────────────────────────────────────
# Multiplicity, flags, decision tree
# ─────────────────────────────────────────────────────────────────────────────
def holm_4family(p_values: Mapping[str, Optional[float]],
                 alpha: float = HOLM_ALPHA) -> Dict[str, object]:
    """Holm across exactly four families; a two-family adjustment is forbidden.

    An `UNEVALUABLE` family enters at p=1.0 **only** inside this calculation
    (Q3).  The placeholder is not evidence of no association, and the reported
    field is always `p_holm_4family`.
    """
    used = {}
    for name in HYPOTHESES:
        value = p_values.get(name)
        used[name] = UNEVALUABLE_P if value is None else float(value)
    order = sorted(HYPOTHESES, key=lambda h: used[h])
    adjusted: Dict[str, float] = {}
    running = 0.0
    for rank, name in enumerate(order):
        factor = HOLM_FAMILY_SIZE - rank
        running = max(running, min(1.0, used[name] * factor))
        adjusted[name] = running
    significant = {name: adjusted[name] <= alpha for name in HYPOTHESES}
    return {"family_size": HOLM_FAMILY_SIZE, "alpha": alpha,
            "p_used": used, "p_holm_4family": adjusted,
            "significant": significant,
            "unevaluable": [h for h in HYPOTHESES if p_values.get(h) is None]}


def evaluate_flags(evidence: Mapping[str, Mapping[str, object]],
                   holm: Mapping[str, object]) -> Dict[str, Dict[str, object]]:
    """Each flag independently; every condition of a flag must hold."""
    significant = dict(holm["significant"])
    unevaluable = set(holm["unevaluable"])
    out: Dict[str, Dict[str, object]] = {}
    for name in HYPOTHESES:
        conditions = dict(evidence.get(name, {}).get("effect_gates", {}))
        if name in unevaluable:
            out[name] = {"flag": False, "evaluable": False,
                         "status": UNEVALUABLE, "effect_gates": conditions,
                         "p_holm_4family": holm["p_holm_4family"][name]}
            continue
        gates_ok = bool(conditions) and all(bool(v) for v in conditions.values())
        out[name] = {
            "flag": bool(gates_ok and significant[name]),
            "evaluable": True, "status": "EVALUATED",
            "effect_gates": conditions,
            "holm_significant": bool(significant[name]),
            "p_holm_4family": holm["p_holm_4family"][name]}
    return out


def decide(qa_ok: bool, m4_status: str,
           flags: Mapping[str, Mapping[str, object]],
           qa_first_failure: Optional[str] = None) -> Dict[str, object]:
    """The registered decision tree, evaluated in order; exactly one branch."""
    if not qa_ok:
        return {"decision": DECISION_MISMATCH,
                "first_stopping_reason": qa_first_failure or "qa_targets",
                "fired": []}
    if m4_status != M4_OK:
        fired = [HYPOTHESIS_FLAG[h] for h in ("H1", "H4")
                 if flags.get(h, {}).get("flag")]
        return {"decision": DECISION_UNRESOLVED,
                "first_stopping_reason": m4_status,
                "partial_flags": fired,
                "note": ("M0-M3 are diagnostic partial results; H1/H4 are not "
                         "promoted to a terminal mechanism verdict"),
                "fired": []}
    fired = [HYPOTHESIS_FLAG[h] for h in HYPOTHESES
             if flags.get(h, {}).get("flag")]
    if len(fired) >= 2:
        return {"decision": DECISION_MULTI, "first_stopping_reason": None,
                "fired": fired}
    if len(fired) == 1:
        return {"decision": fired[0], "first_stopping_reason": None,
                "fired": fired}
    return {"decision": DECISION_NONE, "first_stopping_reason": None,
            "fired": []}


# ─────────────────────────────────────────────────────────────────────────────
# Result assembly and bundle writing
# ─────────────────────────────────────────────────────────────────────────────
def build_config(mode: str, timestamp: str,
                 execution_approved: bool = False) -> Dict[str, object]:
    return {
        "experiment_id": EXPERIMENT_ID, "substage": SUBSTAGE,
        "run_slug": RUN_SLUG, "module_version": MODULE_VERSION,
        "mode": resolve_mode(mode), "timestamp": timestamp,
        "spec": SPEC_PATH,
        "master_seed": MASTER_SEED, "n_null_replicates": N_NULL_REPLICATES,
        "window_half_width": M1_WINDOW_HALF_WIDTH,
        "adjacency_primary": ADJ_PRIMARY,
        "adjacency_secondary_non_decisional": ADJ_SECONDARY,
        "h4_decisional_side": H4_DECISIONAL_SIDE,
        "execution_on_registered_data_approved": bool(execution_approved),
        "approval_note": APPROVAL_NOTE,
    }


def build_manifest(inputs: Mapping[str, object], timestamp: str
                   ) -> Dict[str, object]:
    return {
        "experiment_id": EXPERIMENT_ID, "substage": SUBSTAGE,
        "timestamp": timestamp,
        "module_sha256": sha256_file(os.path.abspath(__file__)),
        "frozen_module_sha256": sha256_file(os.path.abspath(BJ.__file__)),
        "source_bundle": {
            "run": SOURCE_BUNDLE_RUN, "folder_id": SOURCE_BUNDLE_FOLDER_ID,
            "producing_code_sha256": PRODUCING_CODE_SHA256,
            "rule_fingerprint": REGISTERED_RULE_FINGERPRINT},
        "inputs": dict(inputs),
        "m4_input_contract": {k: dict(v) for k, v in M4_INPUT_CONTRACT.items()},
        "registered_runtime": dict(M4_REGISTERED_RUNTIME),
    }


def build_result(qa: Mapping[str, object], m0: Mapping[str, object],
                 m1: Mapping[str, object], m2: Mapping[str, object],
                 m3: Mapping[str, object], m4: Mapping[str, object],
                 nulls: Mapping[str, object], tests: Mapping[str, object],
                 decision: Mapping[str, object],
                 source_files: Sequence[Mapping[str, object]] = ()
                 ) -> Dict[str, object]:
    """Assemble `q5e_result.json` in exactly the registered schema."""
    return {
        "experiment_id": EXPERIMENT_ID, "substage": SUBSTAGE,
        "analysis_only": True, "training_performed": False,
        "model_scored": False, "v10_probability_opened": False,
        "ds2_labels_opened": False, "association_performed": False,
        "detector_replay_performed": str(m4.get("status")) == M4_OK,
        "source_bundle": {
            "run": SOURCE_BUNDLE_RUN, "folder_id": SOURCE_BUNDLE_FOLDER_ID,
            "producing_code_sha256": PRODUCING_CODE_SHA256,
            "rule_fingerprint": REGISTERED_RULE_FINGERPRINT,
            "files": list(source_files)},
        "qa": dict(qa),
        "m0": dict(m0),
        "m1": dict(m1),
        "m2": dict(m2),
        "m3": {"by_group": m3.get("by_group", {}),
               "partition_ok": m3.get("partition_ok"),
               "h4_decisional_side": H4_DECISIONAL_SIDE,
               "non_decisional_sides": [s for s in SIDES
                                        if s != H4_DECISIONAL_SIDE]},
        "h4_decisional_side": H4_DECISIONAL_SIDE,
        "m4": dict(m4),
        "m5": {"strata_present": ["class", "reason", "record", "count_stratum",
                                  "record_116", "record_208", "pooled"]},
        "null": {"replicates": N_NULL_REPLICATES, "master_seed": MASTER_SEED,
                 "controls": dict(nulls)},
        "tests": dict(tests),
        "decision": decision.get("decision"),
        "first_stopping_reason": decision.get("first_stopping_reason"),
        "language_boundary": LANGUAGE_BOUNDARY,
    }


def write_csv(path: str, fields: Sequence[str],
              rows: Iterable[Mapping[str, object]]) -> str:
    import csv
    with open(path, "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fields),
                                extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({f: row.get(f) for f in fields})
    return path


CSV_SCHEMAS: Dict[str, Tuple[str, ...]] = {
    "m0_class_by_reason.csv": ("side", "class", "reason", "count",
                               "denominator", "rate"),
    "m0_record_class.csv": ("record", "stratum", "class", "side",
                            "denominator", "failures", "rate"),
    "m0_runs.csv": ("record", "adjacency_definition", "run_start",
                    "run_length", "classes", "reasons", "decisional"),
    "m1_distance.csv": ("record", "cache_record_row", "processed_class",
                        "reason", "d_inf", "bin", "censored",
                        "cache_endpoint_zero", "included_in_distance_gate"),
    "m3_graph.csv": ("record", "side", "row", "group", "decisional",
                     "candidate_degree", "usable_edges", "has_forced_rank",
                     "rr_pair_multiplicity", "local_rr_sd"),
    "m4_anchors.csv": ("record", "anchor_ordinal", "anchor_sample",
                       "anchor_kind", "adjacency_definition", "offset",
                       "mapped_mamba_record_row", "failed", "decisional"),
}


def write_bundle(directory: str, result: Mapping[str, object],
                 config: Mapping[str, object], manifest: Mapping[str, object],
                 tables: Mapping[str, Sequence[Mapping[str, object]]],
                 nulls: Mapping[str, object], log_lines: Sequence[str],
                 summary: str) -> Dict[str, object]:
    """Write one new bundle directory.  Nothing existing is touched.

    A stopped run still writes its bundle, so a STOP is as inspectable as a
    PASS.
    """
    if os.path.exists(directory) and os.listdir(directory):
        raise Q5EError(
            f"refusing to write into a non-empty directory {directory!r}: "
            f"a run bundle is new, never an overwrite")
    os.makedirs(directory, exist_ok=True)
    written: List[str] = []
    for name, payload in (("q5e_result.json", result), ("config.json", config),
                          ("manifest.json", manifest),
                          ("null_summary.json", nulls)):
        with open(os.path.join(directory, name), "w", encoding="utf-8") as fh:
            json.dump(payload, fh, indent=1, sort_keys=True)
        written.append(name)
    for name, fields in CSV_SCHEMAS.items():
        rows = tables.get(name)
        if rows is None:
            continue                       # m4_anchors.csv is absent on a STOP
        write_csv(os.path.join(directory, name), fields, rows)
        written.append(name)
    with open(os.path.join(directory, "log.txt"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(str(line) for line in log_lines) + "\n")
    with open(os.path.join(directory, "summary.md"), "w",
              encoding="utf-8") as fh:
        fh.write(summary)
    written.extend(["log.txt", "summary.md"])
    return {"directory": directory, "written": sorted(written)}


def summary_markdown(result: Mapping[str, object]) -> str:
    """Human-readable summary.  ASCII only, and no causal language."""
    m4 = result.get("m4", {})
    lines = [
        f"# {EXPERIMENT_ID} / Q5-E - Leg 2 failure mechanism audit",
        "",
        f"- decision: `{result.get('decision')}`",
        f"- first stopping reason: `{result.get('first_stopping_reason')}`",
        f"- M4 status: `{m4.get('status')}`",
        f"- language boundary: {LANGUAGE_BOUNDARY}",
        "",
        "This diagnostic reports association only.  No causal claim is made,",
        "and a PASS here licenses no change to the frozen Q5-D join rule.",
    ]
    return "\n".join(lines) + "\n"


# ─────────────────────────────────────────────────────────────────────────────
# Figures.  All titles, axis labels, tick labels and legends are ASCII.
# ─────────────────────────────────────────────────────────────────────────────
def figure_specs(m4_ok: bool) -> List[Dict[str, object]]:
    """The seven registered figures and their ASCII labels.

    Returned as data so a test can assert the label set without importing
    matplotlib or rendering anything.
    """
    specs = [
        {"file": FIGURES[0], "title": "Class by failure reason",
         "xlabel": "class", "ylabel": "count", "kind": "stacked_bar"},
        {"file": FIGURES[1], "title": "Per-record class failure rate",
         "xlabel": "class", "ylabel": "record", "kind": "heatmap"},
        {"file": FIGURES[2], "title": "Record 208 failure raster",
         "xlabel": "mamba_record_row", "ylabel": "class", "kind": "raster"},
        {"file": FIGURES[3], "title": "Run length distribution",
         "xlabel": "run length bucket", "ylabel": "count", "kind": "hist"},
        {"file": FIGURES[4], "title": "Nearest distance histogram",
         "xlabel": "d_inf bin (samples)", "ylabel": "count", "kind": "hist"},
        {"file": FIGURES[5], "title": "Candidate degree by group",
         "xlabel": "group", "ylabel": "candidate degree", "kind": "violin_ecdf"},
    ]
    if m4_ok:
        specs.append({"file": FIGURE_M4_ONLY,
                      "title": "Anchor aligned failure probability",
                      "xlabel": "beat offset from anchor",
                      "ylabel": "failure share", "kind": "curve"})
    return specs


def assert_ascii_labels(specs: Sequence[Mapping[str, object]]) -> None:
    for spec in specs:
        for key in ("title", "xlabel", "ylabel"):
            value = str(spec.get(key, ""))
            if not value.isascii():
                raise Q5EError(
                    f"figure {spec.get('file')!r} has non-ASCII {key}: {value!r}")


# ─────────────────────────────────────────────────────────────────────────────
# Production entry point
# ─────────────────────────────────────────────────────────────────────────────
def run_audit(bundle_dir: str, mamba_path: str, cache_dir: str,
              mitdb_dir: str, out_dir: str,
              approval: Optional[str] = None,
              open_registered_data: bool = OPEN_REGISTERED_DATA,
              emit=print) -> Dict[str, object]:
    """The single production route to a Q5-E decision.

    Refuses immediately without a separate execution approval.  Permission is
    checked before capability, so an unauthorised call is refused as
    unauthorised whatever the environment happens to have installed.
    """
    if not open_registered_data:
        raise ExecutionNotApprovedError(
            "OPEN_REGISTERED_DATA is False.  This is the default: a stray "
            "import or notebook run cannot reach registered data.  "
            f"{APPROVAL_NOTE}")
    require_execution_approval(approval, f"Q5-E audit over {bundle_dir!r}")
    assert_runtime_ready(MODE_AUDIT)
    canonical = verify_bundle_is_canonical(bundle_dir, approval)
    if not canonical["ok"]:
        raise DiagnosticInputMismatch(
            f"{DECISION_MISMATCH}: {canonical['problems']}")
    emit("Q5-E: canonical bundle verified; measurement may begin.")
    raise Q5EError(
        "run_audit is implemented but has never been executed: the separate "
        "user approval for running M0-M4 on the registered artifacts does not "
        "exist yet.  This line is the deliberate terminal guard for the "
        "implementation-only PR and is removed by the execution-approval "
        "change, not by an implementer in a hurry.")


def design_card() -> str:
    """A constants card that opens nothing.  Safe to print anywhere."""
    lines = [
        f"{EXPERIMENT_ID} / {SUBSTAGE} - implementation, not a result",
        f"  spec                 : {SPEC_PATH}",
        f"  module version       : {MODULE_VERSION}",
        f"  primary adjacency    : {ADJ_PRIMARY} (decisional)",
        f"  secondary adjacency  : {ADJ_SECONDARY} (non-decisional audit)",
        f"  M1 window half width : {M1_WINDOW_HALF_WIDTH}",
        f"  null replicates      : {N_NULL_REPLICATES} x {len(CONTROL_FAMILIES)}",
        f"  master seed          : {MASTER_SEED}",
        f"  Holm family size     : {HOLM_FAMILY_SIZE}",
        f"  H4 decisional side   : {H4_DECISIONAL_SIDE}",
        f"  execution approved   : {execution_is_approved(None)}",
        f"  {APPROVAL_NOTE}",
    ]
    return "\n".join(lines)


def main(argv: Optional[Sequence[str]] = None) -> int:   # pragma: no cover
    import argparse
    parser = argparse.ArgumentParser(description=f"{EXPERIMENT_ID} Q5-E audit")
    parser.add_argument("--mode", default=MODE_DESIGN, choices=list(MODES))
    parser.add_argument(EXECUTION_APPROVAL_FLAG, action="store_true",
                        dest="approved")
    args = parser.parse_args(argv)
    print(design_card())
    if resolve_mode(args.mode) in MODES_NEEDING_EXECUTION_APPROVAL and \
            not args.approved:
        print(f"\nSKIP {args.mode}: {APPROVAL_NOTE}")
        return 2
    if resolve_mode(args.mode) == MODE_DESIGN:
        assert_implementation_only()
        print("\nassert_implementation_only: OK")
    return 0


if __name__ == "__main__":                              # pragma: no cover
    raise SystemExit(main())
