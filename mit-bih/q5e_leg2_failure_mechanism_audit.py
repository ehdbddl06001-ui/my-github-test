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

#: Which target set a QA verdict was produced against.  A result is only a
#: Q5-E finding when this is `REGISTERED`; `FIXTURE` marks a synthetic
#: self-test bundle and is carried into the result JSON and the summary.
QA_TARGETS_REGISTERED = "REGISTERED"
QA_TARGETS_FIXTURE = "FIXTURE"

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
    "runtime", "source_map", "input_identity", "detector_replay",
    "record_counts", "rr_equality")
#: The sub-gates that must all pass **before** the detector may be called.
M4_GATES_BEFORE_REPLAY: Tuple[str, ...] = (
    "runtime", "source_map", "input_identity")

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
    return ("run_audit", "run_audit_from_mount", "discover_registered_inputs",
            "verify_qa_targets", "m0_report", "m1_distances",
            "m2_report", "m3_graph", "m4_feasibility_gate", "m4_anchors",
            "run_null_family", "h4_evaluate", "h4_descriptive_by_side",
            "holm_4family", "evaluate_flags", "decide", "run_pipeline",
            "load_all_inputs", "cache_partition", "build_control_a_class_vectors",
            "assert_m3_partition", "render_figures", "required_outputs",
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
# Cache-side partition (Q4).  A certified cache beat exists in the Q5-D join
# map only as a certified *mamba* row carrying `cache_record_row`, so
# `is_cache_side()` alone would silently drop every certified cache row from a
# cache-side denominator.  Every cache-side denominator, class lookup and
# Control A input is built from this one partition instead.
# ─────────────────────────────────────────────────────────────────────────────
def registered_cache_n(records: Iterable[str], split: str = SPLIT
                       ) -> Dict[str, int]:
    """Per-record cache row counts, from the frozen ledger and nowhere else."""
    return {str(r): BJ.ledger_record(split, str(r)).cache_n for r in records}


def cache_partition(rows: Sequence[Mapping[str, object]],
                    processed_classes: Mapping[Tuple[str, int], str],
                    cache_n: Optional[Mapping[str, int]] = None
                    ) -> List[Dict[str, object]]:
    """One entry per cache row: certified plus the three failure groups.

    The group assignment reuses :func:`derive_cache_side_groups`, so the
    disjoint/exhaustive contract and its `DIAGNOSTIC_INPUT_MISMATCH` failures
    are shared rather than re-implemented.  Class comes **only** from the
    canonical DS1 processed-class map; `mamba_aami` is never copied, filled or
    estimated into a cache row.
    """
    records = sorted({str(r["record"]) for r in rows})
    counts = dict(cache_n) if cache_n is not None else registered_cache_n(records)
    groups = derive_cache_side_groups(rows, counts)
    out: List[Dict[str, object]] = []
    for (record, index), group in sorted(groups.items()):
        out.append({
            "record": record, "cache_record_row": int(index), "group": group,
            "class": processed_classes.get((record, int(index)), ""),
            "reason": (BJ.REASON_NONE if group == GROUP_CERTIFIED
                       else {v: k for k, v in REASON_TO_GROUP.items()}[group]),
            "failed": group != GROUP_CERTIFIED,
            "stratum": record_stratum(record),
        })
    return out


def assert_cache_partition(partition: Sequence[Mapping[str, object]],
                           cache_n: Mapping[str, int]) -> None:
    """Disjoint, exhaustive, exactly `cache_n` rows per record."""
    seen: Dict[str, set] = {}
    for entry in partition:
        record = str(entry["record"])
        index = int(entry["cache_record_row"])
        bucket = seen.setdefault(record, set())
        if index in bucket:
            raise DiagnosticInputMismatch(
                f"{record}: cache row {index} appears twice in the partition")
        bucket.add(index)
    for record, n in cache_n.items():
        got = len(seen.get(record, ()))
        if got != int(n):
            raise DiagnosticInputMismatch(
                f"{record}: cache partition has {got} rows, ledger says {n}")


# ─────────────────────────────────────────────────────────────────────────────
# Control A input (I1.5).  The class vector Control A shifts is the cache-side
# processed-class sequence in `cache_record_row` order, over the *whole* cache
# population.  A production caller cannot supply `mamba_aami`, mamba ordering
# or an ad-hoc vector: this builder is the only accepted route and it asserts
# its own provenance.
# ─────────────────────────────────────────────────────────────────────────────
CONTROL_A_CLASS_SOURCE = "canonical_ds1_processed_class_map"


def build_control_a_class_vectors(partition: Sequence[Mapping[str, object]],
                                  processed_classes: Mapping[
                                      Tuple[str, int], str],
                                  cache_n: Mapping[str, int]
                                  ) -> Dict[str, List[str]]:
    """Per-record cache-side class vectors, ordered by `cache_record_row`."""
    assert_cache_partition(partition, cache_n)
    by_record: Dict[str, Dict[int, str]] = {}
    for entry in partition:
        by_record.setdefault(str(entry["record"]), {})[
            int(entry["cache_record_row"])] = str(entry["class"])
    out: Dict[str, List[str]] = {}
    for record, mapping in sorted(by_record.items()):
        n = int(cache_n[record])
        if sorted(mapping) != list(range(n)):
            raise DiagnosticInputMismatch(
                f"{record}: cache rows are not exactly 0..{n - 1}")
        vector = [mapping[i] for i in range(n)]
        for i, value in enumerate(vector):
            if value != processed_classes.get((record, i), ""):
                raise DiagnosticInputMismatch(
                    f"{record}: cache row {i} class does not come from the "
                    f"canonical DS1 processed-class map")
        out[record] = vector
    return out


def assert_control_a_input(vectors: Mapping[str, Sequence[str]],
                           processed_classes: Mapping[Tuple[str, int], str],
                           cache_n: Mapping[str, int]) -> Dict[str, object]:
    """Refuse any Control A input that did not come from the cache-side map."""
    for record, vector in vectors.items():
        n = int(cache_n.get(record, -1))
        if len(vector) != n:
            raise DiagnosticInputMismatch(
                f"{record}: Control A vector has {len(vector)} entries, "
                f"ledger says {n}")
        for i, value in enumerate(vector):
            if value != processed_classes.get((record, i), ""):
                raise DiagnosticInputMismatch(
                    f"{record}: Control A entry {i} is not the canonical "
                    f"processed class; `mamba_aami` may never be substituted")
    return {"source": CONTROL_A_CLASS_SOURCE, "records": len(vectors),
            "ok": True}


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
                      manifest: Mapping[str, object],
                      qa_fixture: Optional[Mapping[str, object]] = None
                      ) -> Dict[str, object]:
    """Reproduce every registered QA target.  One mismatch stops the audit.

    ``qa_fixture`` exists so a **synthetic** end-to-end test can traverse the
    whole route without a registered artifact.  It never relaxes anything: the
    registered targets are the default, production never passes it (see
    :func:`run_audit`), and every result derived from a fixture carries
    ``target_set = FIXTURE`` all the way into `q5e_result.json` and
    `summary.md`, so a synthetic bundle can never be read as a Q5-E finding.
    """
    validate_rows(rows)
    observed = observed_qa_counts(rows)
    fixture = dict(qa_fixture or {})
    target_set = QA_TARGETS_FIXTURE if fixture else QA_TARGETS_REGISTERED
    expected_counts = dict(fixture.get("targets") or QA_TARGETS)
    expected_fp = str(fixture.get("rule_fingerprint")
                      or REGISTERED_RULE_FINGERPRINT)
    expected_code = str(fixture.get("producing_code_sha256")
                        or PRODUCING_CODE_SHA256)
    targets: Dict[str, Dict[str, object]] = {}
    for name, expected in expected_counts.items():
        got = observed.get(name)
        targets[name] = {"expected": expected, "observed": got,
                         "ok": got == expected}
    fingerprint = str(decision.get("rule_fingerprint")
                      or manifest.get("rule_fingerprint") or "")
    targets["rule_fingerprint"] = {
        "expected": expected_fp, "observed": fingerprint,
        "ok": fingerprint == expected_fp}
    code = str(manifest.get("code_sha256") or "")
    targets["producing_code_sha256"] = {
        "expected": expected_code, "observed": code,
        "ok": code == expected_code}
    ok = all(entry["ok"] for entry in targets.values())
    return {"targets": targets, "ok": ok, "target_set": target_set,
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
                       processed_classes: Mapping[Tuple[str, int], str],
                       partition: Optional[Sequence[Mapping[str, object]]] = None
                       ) -> Dict[str, Dict[str, Dict[str, object]]]:
    """M0.2 — class x failure-reason contingency, per side, never summed.

    The cache side is taken from the disjoint, exhaustive
    :func:`cache_partition`, so its `_rows` denominator counts **every** cache
    row of that class — certified included — not only the explicit cache-only
    failure rows.
    """
    if partition is None:
        partition = cache_partition(rows, processed_classes)
    out: Dict[str, Dict[str, Dict[str, object]]] = {
        side: {cls: {} for cls in AAMI_CLASSES} for side in SIDES}
    for cls in AAMI_CLASSES:
        mamba_rows = [r for r in rows if is_mamba_side(r)
                      and str(r.get("mamba_aami") or "") == cls]
        cache_rows = [e for e in partition if str(e["class"]) == cls]
        for side, selected, failed in (
                (SIDE_MAMBA, mamba_rows,
                 [r for r in mamba_rows if is_failed(r)]),
                (SIDE_CACHE, cache_rows,
                 [e for e in cache_rows if e["failed"]])):
            denominator = len(failed)
            for reason in (BJ.REASON_NO_EDGE, BJ.REASON_NOT_OPTIMAL,
                           BJ.REASON_AMBIGUOUS):
                if side == SIDE_MAMBA:
                    count = sum(1 for r in failed
                                if str(r["drop_or_unmatched_reason"]) == reason)
                else:
                    count = sum(1 for e in failed if str(e["reason"]) == reason)
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
                    record: str,
                    partition: Optional[Sequence[Mapping[str, object]]] = None
                    ) -> Dict[str, Dict[str, Dict[str, float]]]:
    """M0.3 — one record, per class, on both sides.

    The cache-side denominator is the record's **whole** cache population from
    :func:`cache_partition`, so the per-class denominators sum to `cache_n`.
    """
    if partition is None:
        partition = cache_partition(rows, processed_classes)
    record = str(record)
    out: Dict[str, Dict[str, Dict[str, float]]] = {}
    subset = [r for r in rows if str(r["record"]) == record]
    cache_rows = [e for e in partition if str(e["record"]) == record]
    for cls in AAMI_CLASSES:
        mamba_sel = [r for r in subset if is_mamba_side(r)
                     and str(r.get("mamba_aami") or "") == cls]
        cache_sel = [e for e in cache_rows if str(e["class"]) == cls]
        out.setdefault(SIDE_MAMBA, {})[cls] = {
            "denominator": len(mamba_sel),
            "failures": sum(1 for r in mamba_sel if is_failed(r)),
            "rate": _ratio(sum(1 for r in mamba_sel if is_failed(r)),
                           len(mamba_sel))}
        out.setdefault(SIDE_CACHE, {})[cls] = {
            "denominator": len(cache_sel),
            "failures": sum(1 for e in cache_sel if e["failed"]),
            "rate": _ratio(sum(1 for e in cache_sel if e["failed"]),
                           len(cache_sel))}
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
              processed_classes: Mapping[Tuple[str, int], str],
              partition: Optional[Sequence[Mapping[str, object]]] = None
              ) -> Dict[str, object]:
    """The complete M0 block, in the registered schema field names."""
    if partition is None:
        partition = cache_partition(rows, processed_classes)
    runs = m0_runs(rows)
    return {
        "class_failure_rate": m0_class_failure_rate(rows),
        "class_by_reason": m0_class_by_reason(rows, processed_classes,
                                              partition),
        "record_208": m0_record_class(rows, processed_classes, "208",
                                      partition),
        "record_116": m0_record_class(rows, processed_classes, "116",
                                      partition),
        "runs_primary_mamba_row": runs[ADJ_PRIMARY],
        "runs_secondary_raw_ordinal": runs[ADJ_SECONDARY],
        "post_v_failure": {
            ADJ_PRIMARY: m0_post_v_failure(rows, ADJ_PRIMARY),
            ADJ_SECONDARY: m0_post_v_failure(rows, ADJ_SECONDARY)},
        "strata": m0_strata(rows),
        "m5": m5_stratified_failure_report(rows, partition),
    }


# ─────────────────────────────────────────────────────────────────────────────
# M5 — the registered strata, materialised.  Declaring stratum names in the
# result JSON is not stratification; every applicable result is reported across
# these strata simultaneously, and a combination that does not apply is marked
# `NOT_APPLICABLE` rather than silently written as zero.
# ─────────────────────────────────────────────────────────────────────────────
M5_STRATA: Tuple[str, ...] = ("class", "reason", "record", "count_stratum",
                              "record_116", "record_208", "pooled")
NOT_APPLICABLE = "NOT_APPLICABLE"
POOLED = "pooled"


def _rate_entry(failures: int, denominator: int) -> Dict[str, object]:
    if denominator == 0:
        return {"failures": failures, "denominator": 0, "rate": None,
                "status": NOT_APPLICABLE}
    return {"failures": failures, "denominator": denominator,
            "rate": _ratio(failures, denominator), "status": "OK"}


def m5_stratified_failure_report(rows: Sequence[Mapping[str, object]],
                                 partition: Sequence[Mapping[str, object]]
                                 ) -> Dict[str, object]:
    """Failure counts and rates across every registered stratum, both sides."""
    mamba = [r for r in rows if is_mamba_side(r)]
    out: Dict[str, object] = {"strata_materialised": list(M5_STRATA)}

    def side_pair(m_sel, c_sel):
        return {
            SIDE_MAMBA: _rate_entry(sum(1 for r in m_sel if is_failed(r)),
                                    len(m_sel)),
            SIDE_CACHE: _rate_entry(sum(1 for e in c_sel if e["failed"]),
                                    len(c_sel))}

    out["class"] = {
        cls: side_pair([r for r in mamba
                        if str(r.get("mamba_aami") or "") == cls],
                       [e for e in partition if str(e["class"]) == cls])
        for cls in AAMI_CLASSES}
    out["reason"] = {
        reason: {
            SIDE_MAMBA: {"count": sum(
                1 for r in mamba if is_failed(r)
                and str(r["drop_or_unmatched_reason"]) == reason)},
            SIDE_CACHE: {"count": sum(
                1 for e in partition if e["failed"]
                and str(e["reason"]) == reason)}}
        for reason in (BJ.REASON_NO_EDGE, BJ.REASON_NOT_OPTIMAL,
                       BJ.REASON_AMBIGUOUS)}
    records = sorted({str(r["record"]) for r in rows})
    out["record"] = {
        record: side_pair([r for r in mamba if str(r["record"]) == record],
                          [e for e in partition
                           if str(e["record"]) == record])
        for record in records}
    out["count_stratum"] = {
        stratum: side_pair(
            [r for r in mamba if record_stratum(str(r["record"])) == stratum],
            [e for e in partition if str(e["stratum"]) == stratum])
        for stratum in (BJ.STRATUM_EQUAL, BJ.STRATUM_MISMATCH)}
    for record in ("116", "208"):
        key = f"record_{record}"
        out[key] = (side_pair([r for r in mamba if str(r["record"]) == record],
                              [e for e in partition
                               if str(e["record"]) == record])
                    if record in records
                    else {"status": NOT_APPLICABLE,
                          "reason": f"record {record} not present in inputs"})
    out[POOLED] = side_pair(mamba, list(partition))
    return out


def strata_reported(report: Mapping[str, object]) -> List[str]:
    """Which registered strata this report actually materialised."""
    out = []
    for name in M5_STRATA:
        value = report.get(name)
        if not isinstance(value, dict) or not value:
            continue
        if value.get("status") == NOT_APPLICABLE:
            continue
        out.append(name)
    return out


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


def reconstructed_groups(result: "BJ.MatchResult", n_mamba: int, n_cache: int
                         ) -> Dict[str, Dict[int, str]]:
    """Group per row from the frozen matcher, assigned exactly as `join_record`.

    Certified, then ambiguous, then "had a candidate edge but is in no maximum
    matching", then "no candidate edge at all".  The matcher, tolerance,
    candidate-edge rule and certification definition are the frozen module's
    and are not touched here.
    """
    certified_i = {i for i, _ in result.certified}
    certified_j = {j for _, j in result.certified}
    ambiguous_i = {i for i, _ in result.ambiguous}
    ambiguous_j = {j for _, j in result.ambiguous}
    edge_i = {i for i, _ in result.edges}
    edge_j = {j for _, j in result.edges}

    def assign(index, cert, amb, edge):
        if index in cert:
            return GROUP_CERTIFIED
        if index in amb:
            return GROUP_AMBIGUOUS
        return GROUP_NOT_OPTIMAL if index in edge else GROUP_NO_EDGE

    return {
        SIDE_MAMBA: {i: assign(i, certified_i, ambiguous_i, edge_i)
                     for i in range(n_mamba)},
        SIDE_CACHE: {j: assign(j, certified_j, ambiguous_j, edge_j)
                     for j in range(n_cache)},
    }


def assert_m3_partition(graph: Mapping[str, object],
                        qa_reason_counts: Optional[Mapping[str, int]] = None
                        ) -> None:
    """One mismatch is `DIAGNOSTIC_INPUT_MISMATCH`; M3 may not be used after it."""
    if not graph.get("partition_ok"):
        raise DiagnosticInputMismatch(
            f"{DECISION_MISMATCH}: M3 does not reproduce the bundle partition: "
            f"{list(graph.get('problems', []))[:6]}")
    if qa_reason_counts:
        observed = dict(graph.get("reason_counts", {}))
        bad = {k: (observed.get(k), v) for k, v in qa_reason_counts.items()
               if observed.get(k) != v}
        if bad:
            raise DiagnosticInputMismatch(
                f"{DECISION_MISMATCH}: reconstructed reason counts differ "
                f"from the registered targets: {bad}")


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

    reason_counts = {BJ.REASON_NO_EDGE: 0, BJ.REASON_NOT_OPTIMAL: 0,
                     BJ.REASON_AMBIGUOUS: 0}
    for record in sorted(mamba_by_record):
        metrics = graph_metrics_for_record(
            mamba_by_record[record], cache_by_record[record])
        result = metrics["result"]
        rebuilt = reconstructed_groups(result, len(mamba_by_record[record]),
                                       len(cache_by_record[record]))
        # Row identity, not just counts: every mamba and cache row's group must
        # equal the bundle's, and the three reason counts must agree exactly.
        for side, expected in ((SIDE_MAMBA, mamba_groups),
                               (SIDE_CACHE, cache_groups)):
            for index, group in sorted(rebuilt[side].items()):
                bundle_group = expected.get((record, index))
                if bundle_group is None:
                    partition_ok = False
                    problems.append(
                        f"{record}/{side}/{index}: reconstructed {group} but "
                        f"the bundle has no such row")
                elif bundle_group != group:
                    partition_ok = False
                    problems.append(
                        f"{record}/{side}/{index}: reconstructed {group} != "
                        f"bundle {bundle_group}")
            for (rec, index) in expected:
                if rec == record and index not in rebuilt[side]:
                    partition_ok = False
                    problems.append(
                        f"{record}/{side}/{index}: in the bundle but not in "
                        f"the reconstructed graph")
            for group in rebuilt[side].values():
                if group != GROUP_CERTIFIED:
                    reason_counts[{v: k for k, v in
                                   REASON_TO_GROUP.items()}[group]] += 1
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
            "reason_counts": reason_counts,
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

    gates.append(identity)
    if not identity["ok"]:
        return _m4_absent(gates, identity, identity["reason"])

    # Only now may the detector run.  Every sub-gate in
    # `M4_GATES_BEFORE_REPLAY` has passed and is already recorded, in the
    # registered order.  `replay` is injected so the gate is testable without
    # ever calling `detect_r()`.
    assert [g["gate"] for g in gates] == list(M4_GATES_BEFORE_REPLAY)
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
    """Each flag independently; every condition of a flag must hold.

    A mechanism is never declared from the pooled value alone (M5), so
    evidence whose `strata_reported` contains nothing but `pooled` cannot fire
    a flag however significant it is.  That rule lives here, in the structure,
    rather than in a reviewer's attention.
    """
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
        reported = list(evidence.get(name, {}).get("strata_reported", ()))
        pooled_only = not [x for x in reported if x != POOLED]
        out[name] = {
            "flag": bool(gates_ok and significant[name] and not pooled_only),
            "evaluable": True, "status": "EVALUATED",
            "effect_gates": conditions,
            "strata_reported": reported,
            "pooled_only_blocked": bool(pooled_only),
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
    target_set = str(qa.get("target_set") or QA_TARGETS_REGISTERED)
    return {
        "experiment_id": EXPERIMENT_ID, "substage": SUBSTAGE,
        "qa_target_set": target_set,
        "synthetic_fixture": target_set != QA_TARGETS_REGISTERED,
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


def required_outputs(decision: str, m4_ok: bool) -> List[str]:
    """Every file this branch must produce.  Computed **before** writing.

    The only registered absences are the M4-only artefacts when M4 stops; a
    bundle missing anything else is refused rather than written incomplete.
    """
    names = [f for f in BUNDLE_FILES if f != "m4_anchors.csv"]
    figures = [spec["file"] for spec in figure_specs(m4_ok)]
    if m4_ok:
        names.append("m4_anchors.csv")
    return sorted(names + figures)


def render_figures(directory: str,
                   tables: Mapping[str, Sequence[Mapping[str, object]]],
                   m4_ok: bool, backend=None) -> List[str]:
    """Render the registered figures as real PNG files.

    ``backend`` is injectable so a synthetic end-to-end test can exercise the
    complete bundle contract without depending on a plotting library.  The
    default backend is matplotlib with the non-interactive Agg canvas.  All
    titles, axis labels, tick labels and legends are ASCII.
    """
    specs = figure_specs(m4_ok)
    assert_ascii_labels(specs)
    writer = backend or _matplotlib_backend
    written: List[str] = []
    for spec in specs:
        path = os.path.join(directory, str(spec["file"]))
        if os.path.exists(path):
            raise Q5EError(f"refusing to overwrite an existing figure {path!r}")
        writer(path, spec, tables)
        written.append(str(spec["file"]))
    return sorted(written)


def _matplotlib_backend(path: str, spec: Mapping[str, object],
                        tables: Mapping[str, Sequence[Mapping[str, object]]]
                        ) -> None:                          # pragma: no cover
    """Default renderer.  ASCII labels only; no glyph can go missing."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    figure, axes = plt.subplots(figsize=(7.0, 4.0))
    kind = str(spec.get("kind"))
    series = _figure_series(kind, tables)
    if series["x"]:
        if kind in ("stacked_bar", "hist", "raster"):
            axes.bar(range(len(series["x"])), series["y"])
        else:
            axes.plot(range(len(series["x"])), series["y"], marker="o")
        axes.set_xticks(range(len(series["x"])))
        axes.set_xticklabels([str(v) for v in series["x"]], rotation=45,
                             ha="right")
    axes.set_title(str(spec["title"]))
    axes.set_xlabel(str(spec["xlabel"]))
    axes.set_ylabel(str(spec["ylabel"]))
    figure.tight_layout()
    figure.savefig(path, dpi=110)
    plt.close(figure)


def _figure_series(kind: str,
                   tables: Mapping[str, Sequence[Mapping[str, object]]]
                   ) -> Dict[str, List[object]]:
    """Plain (x, y) series per registered figure, from the written tables."""
    rows: Sequence[Mapping[str, object]]
    if kind == "stacked_bar":
        rows = tables.get("m0_class_by_reason.csv", [])
        return {"x": [f"{r.get('class')}/{r.get('side')}" for r in rows],
                "y": [float(r.get("count") or 0) for r in rows]}
    if kind == "heatmap":
        rows = tables.get("m0_record_class.csv", [])
        return {"x": [f"{r.get('record')}/{r.get('class')}" for r in rows],
                "y": [float(r.get("rate") or 0.0) for r in rows]}
    if kind == "raster":
        rows = [r for r in tables.get("m0_runs.csv", [])
                if str(r.get("record")) == "208"]
        return {"x": [r.get("run_start") for r in rows],
                "y": [float(r.get("run_length") or 0) for r in rows]}
    if kind == "hist":
        rows = tables.get("m1_distance.csv", [])
        buckets: Dict[str, int] = {}
        for r in rows:
            buckets[str(r.get("bin"))] = buckets.get(str(r.get("bin")), 0) + 1
        if not buckets:
            rows = tables.get("m0_runs.csv", [])
            for r in rows:
                key = str(r.get("run_length"))
                buckets[key] = buckets.get(key, 0) + 1
        return {"x": sorted(buckets), "y": [buckets[k] for k in sorted(buckets)]}
    if kind == "violin_ecdf":
        rows = tables.get("m3_graph.csv", [])
        by_group: Dict[str, List[float]] = {}
        for r in rows:
            by_group.setdefault(str(r.get("group")), []).append(
                float(r.get("candidate_degree") or 0))
        return {"x": sorted(by_group),
                "y": [median(by_group[k]) for k in sorted(by_group)]}
    rows = tables.get("m4_anchors.csv", [])
    by_offset: Dict[int, List[float]] = {}
    for r in rows:
        by_offset.setdefault(int(r.get("offset") or 0), []).append(
            1.0 if r.get("failed") else 0.0)
    return {"x": sorted(by_offset),
            "y": [_ratio(sum(by_offset[k]), len(by_offset[k]))
                  for k in sorted(by_offset)]}


def write_bundle(directory: str, result: Mapping[str, object],
                 config: Mapping[str, object], manifest: Mapping[str, object],
                 tables: Mapping[str, Sequence[Mapping[str, object]]],
                 nulls: Mapping[str, object], log_lines: Sequence[str],
                 summary: str, figures: Optional[bool] = None,
                 figure_backend=None,
                 require_complete: bool = False) -> Dict[str, object]:
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

    m4_ok = str((result.get("m4") or {}).get("status")) == M4_OK
    if figures is not None:
        written.extend(render_figures(directory, tables, m4_ok,
                                      backend=figure_backend))
    if require_complete:
        needed = required_outputs(str(result.get("decision") or ""), m4_ok)
        missing = [name for name in needed
                   if not os.path.exists(os.path.join(directory, name))]
        if missing:
            raise Q5EError(
                f"incomplete bundle: {missing} were required for decision "
                f"{result.get('decision')!r} (M4 ok={m4_ok}) but were not "
                f"written.  A bundle is complete or it is not written at all; "
                f"the only registered absences are the M4-only artefacts when "
                f"M4 stops.")
    return {"directory": directory, "written": sorted(set(written)),
            "required": required_outputs(str(result.get("decision") or ""),
                                         m4_ok)}


def summary_markdown(result: Mapping[str, object]) -> str:
    """Human-readable summary.  ASCII only, and no causal language."""
    m4 = result.get("m4", {})
    lines = [
        f"# {EXPERIMENT_ID} / Q5-E - Leg 2 failure mechanism audit",
        "",
    ]
    if result.get("synthetic_fixture"):
        lines += [
            "> **SYNTHETIC FIXTURE - NOT A Q5-E RESULT.**  This bundle was",
            "> produced against injected fixture QA targets, not the",
            "> registered ones.  Nothing in it may be read, cited or",
            "> registered as a finding.",
            "",
        ]
    lines += [
        f"- QA target set: `{result.get('qa_target_set')}`",
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
class ProductionInputs(object):
    """Everything the pipeline needs, already loaded.

    Separating loading from computation is what makes the whole audit testable
    without a registered artifact: a synthetic test injects this object, and
    production fills it through :func:`load_all_inputs`.
    """

    __slots__ = ("rows", "decision", "manifest", "processed_classes",
                 "mamba_by_record", "cache_by_record", "cache_n",
                 "m4_runtime", "m4_sources", "m4_texts", "m4_identity",
                 "m4_registered_counts", "m4_frozen_rr", "m4_replay",
                 "m4_anchors", "source_files")

    def __init__(self, rows, decision, manifest, processed_classes,
                 mamba_by_record, cache_by_record, cache_n,
                 m4_runtime=None, m4_sources=None, m4_texts=None,
                 m4_identity=None, m4_registered_counts=None,
                 m4_frozen_rr=None, m4_replay=None, m4_anchors=None,
                 source_files=()):
        self.rows = list(rows)
        self.decision = dict(decision)
        self.manifest = dict(manifest)
        self.processed_classes = dict(processed_classes)
        self.mamba_by_record = dict(mamba_by_record)
        self.cache_by_record = dict(cache_by_record)
        self.cache_n = dict(cache_n)
        self.m4_runtime = dict(m4_runtime or {})
        self.m4_sources = dict(m4_sources or {})
        self.m4_texts = dict(m4_texts or {})
        self.m4_identity = dict(m4_identity or {})
        self.m4_registered_counts = dict(m4_registered_counts or {})
        self.m4_frozen_rr = dict(m4_frozen_rr or {})
        self.m4_replay = m4_replay
        self.m4_anchors = dict(m4_anchors or {})
        self.source_files = list(source_files)


def load_join_map(bundle_dir: str, approval: Optional[str]
                  ) -> List[Dict[str, object]]:
    """Read `join_map.parquet`.  Approval is checked before `open()`."""
    require_execution_approval(approval, f"join map in {bundle_dir!r}")
    import pyarrow.parquet as pq                          # noqa: PLC0415
    path = os.path.join(bundle_dir, "join_map.parquet")
    if not os.path.exists(path):
        raise Q5EError(f"{DECISION_MISMATCH}: join_map.parquet not found")
    table = pq.read_table(path, columns=list(BJ.JOIN_MAP_FIELDS))
    rows = table.to_pylist()
    validate_rows(rows)
    return [r for r in rows if str(r["split"]) == SPLIT]


def load_decision_and_manifest(bundle_dir: str, approval: Optional[str]
                               ) -> Tuple[Dict[str, object],
                                          Dict[str, object]]:
    out = []
    for name in ("decision.json", "manifest.json"):
        with open_registered_input(os.path.join(bundle_dir, name), approval,
                                   name) as handle:
            out.append(json.loads(handle.read().decode("utf-8")))
    return out[0], out[1]


def load_processed_classes(cache_dir: str, approval: Optional[str]
                           ) -> Dict[Tuple[str, int], str]:
    """Canonical DS1 processed-class map.  DS2 labels stay sealed."""
    require_execution_approval(approval, "canonical DS1 processed-class map")
    return BJ.load_cache_classes(cache_dir, SPLIT, approval=approval)


def load_sequences(mamba_path: str, cache_dir: str, approval: Optional[str]
                   ) -> Tuple[Dict[str, object], Dict[str, object]]:
    require_execution_approval(approval, "frozen mamba and cache sequences")
    mamba = BJ.load_mamba_sequences(mamba_path, approval=approval)
    cache = BJ.load_cache_sequences(cache_dir, approval=approval)
    ds1 = [row.record for row in BJ.build_ledger()[SPLIT]]
    return ({r: mamba["sequences"][r] for r in ds1},
            {r: cache["sequences"][r] for r in ds1})


def load_m4_source_map(source_dir: str, approval: Optional[str]
                       ) -> Tuple[Dict[str, str], Dict[str, str]]:
    """Digest and text of the two decisive V10 source-map files."""
    require_execution_approval(approval, f"V10 source map in {source_dir!r}")
    hashes, texts = {}, {}
    for name in M4_SOURCE_MAP_HASHES:
        path = os.path.join(source_dir, name)
        if not os.path.exists(path):
            raise Q5EError(f"{DECISION_MISMATCH}: V10 source {name} not found")
        hashes[name] = sha256_file(path)
        with open(path, encoding="utf-8", errors="replace") as handle:
            texts[name] = handle.read()
    return hashes, texts


# ─────────────────────────────────────────────────────────────────────────────
# Deterministic input resolution.
#
# The spec establishes identity **by digest, never by path**.  A notebook that
# asks a human to paste five Drive paths contradicts that: a typo silently
# selects the wrong artifact, and the V9 cache sits one directory away from the
# V10 one.  So the paths are not typed at all — every registered input is
# *found* by its registered digest under one mount root, and a search that does
# not find exactly one match refuses rather than guessing.
# ─────────────────────────────────────────────────────────────────────────────
DISCOVERY_MAX_DEPTH = 6


def _candidate_dirs(root: str, max_depth: int = DISCOVERY_MAX_DEPTH):
    """Directories under ``root``, breadth-limited so a mount cannot hang it."""
    root = os.path.abspath(root)
    base = root.rstrip(os.sep).count(os.sep)
    for current, subdirs, _files in os.walk(root):
        if current.rstrip(os.sep).count(os.sep) - base >= max_depth:
            subdirs[:] = []
        subdirs[:] = [d for d in sorted(subdirs) if not d.startswith(".")]
        yield current


def _only(matches: Sequence[str], what: str, root: str) -> str:
    if len(matches) == 1:
        return matches[0]
    if not matches:
        raise DiagnosticInputMismatch(
            f"{DECISION_MISMATCH}: no {what} with the registered identity was "
            f"found under {root!r}.  The audit does not fall back to a "
            f"path-named guess: mount the registered artifact and re-run.")
    raise DiagnosticInputMismatch(
        f"{DECISION_MISMATCH}: {len(matches)} directories under {root!r} match "
        f"the registered {what} ({matches[:4]}).  Identity must be unique; "
        f"remove the duplicate copy rather than choosing one here.")


def discover_registered_inputs(search_root: str, approval: Optional[str]
                               ) -> Dict[str, str]:
    """Locate every registered input under one mount, **by digest**.

    Returns the five paths :func:`run_audit` needs.  Nothing is matched on a
    folder name, so a renamed copy is still found and a look-alike is still
    refused.  In particular the V9 cache can never be selected in place of the
    V10 one: only the registered V10 aggregate matches.
    """
    require_execution_approval(approval, f"input discovery under {search_root!r}")
    found: Dict[str, str] = {}

    bundles: List[str] = []
    for directory in _candidate_dirs(search_root):
        if not all(os.path.exists(os.path.join(directory, name))
                   for name in BUNDLE_INPUT_FILES):
            continue
        if os.path.exists(os.path.join(directory, SUPERSEDED_MARKER)):
            continue                       # a superseded bundle is not a match
        try:
            with open(os.path.join(directory, "manifest.json"),
                      encoding="utf-8") as handle:
                code = str(json.load(handle).get("code_sha256") or "")
        except (OSError, ValueError):
            continue
        if code == PRODUCING_CODE_SHA256:
            bundles.append(directory)
    found["bundle_dir"] = _only(bundles, "canonical bundle", search_root)

    mamba: List[str] = []
    for directory in _candidate_dirs(search_root):
        path = os.path.join(directory, "mamba_data.npz")
        if os.path.isfile(path) and sha256_file(path) == BJ.MAMBA_SHA256:
            mamba.append(path)
    found["mamba_path"] = _only(mamba, "mamba_data.npz", search_root)

    cache_names = BJ.cache_expected_files()
    cache_want = str(M4_INPUT_CONTRACT["v10_cache"]["aggregate"])
    caches: List[str] = []
    for directory in _candidate_dirs(search_root):
        if not os.path.isfile(os.path.join(directory, cache_names[0])):
            continue
        digest = BJ.hash_file_set(directory, cache_names, approval=approval)
        if digest.get("aggregate") == cache_want:
            caches.append(directory)
    found["cache_dir"] = _only(caches, "V10 preprocessing cache", search_root)

    sources: List[str] = []
    for directory in _candidate_dirs(search_root):
        if all(os.path.isfile(os.path.join(directory, name))
               and sha256_file(os.path.join(directory, name)) == want
               for name, want in M4_SOURCE_MAP_HASHES.items()):
            sources.append(directory)
    found["v10_source_dir"] = _only(sources, "V10 source map", search_root)

    # The MIT-BIH publisher tree is recorded in the manifest for provenance;
    # Q5-E never opens it.  This spec pins its aggregate only in truncated
    # form, so it is matched on completeness of the registered file set rather
    # than on a digest that is not written down here in full.
    trees = [d for d in _candidate_dirs(search_root)
             if all(os.path.isfile(os.path.join(d, name))
                    for name in BJ.mitdb_expected_files())]
    found["mitdb_dir"] = _only(trees, "MIT-BIH publisher tree", search_root)
    return found


def observed_runtime() -> Dict[str, str]:
    """The runtime actually loaded.  Reported, never negotiated."""
    import platform                                       # noqa: PLC0415
    out = {"python": platform.python_version()}
    for name in ("numpy", "scipy", "wfdb"):
        try:
            out[name] = getattr(__import__(name), "__version__", "")
        except ImportError:
            out[name] = ""
    return out


def load_all_inputs(bundle_dir: str, mamba_path: str, cache_dir: str,
                    mitdb_dir: str, v10_source_dir: str,
                    approval: Optional[str]) -> ProductionInputs:
    """Every registered read, behind one approval-checked door."""
    rows = load_join_map(bundle_dir, approval)
    decision, manifest = load_decision_and_manifest(bundle_dir, approval)
    processed = load_processed_classes(cache_dir, approval)
    mamba, cache = load_sequences(mamba_path, cache_dir, approval)
    hashes, texts = load_m4_source_map(v10_source_dir, approval)
    records = sorted(mamba)
    return ProductionInputs(
        rows=rows, decision=decision, manifest=manifest,
        processed_classes=processed, mamba_by_record=mamba,
        cache_by_record=cache, cache_n={r: len(cache[r]) for r in records},
        m4_runtime=observed_runtime(), m4_sources=hashes, m4_texts=texts,
        m4_identity={"v10_source": str(M4_INPUT_CONTRACT["v10_source"]
                                       ["aggregate"]),
                     "v10_cache": str(M4_INPUT_CONTRACT["v10_cache"]
                                      ["aggregate"])},
        m4_registered_counts={r: BJ.ledger_record(SPLIT, r).cache_n
                              for r in records},
        m4_frozen_rr={}, m4_replay=None, m4_anchors={},
        source_files=[])


def run_pipeline(inputs: "ProductionInputs",
                 replicates: int = N_NULL_REPLICATES,
                 emit=print,
                 qa_fixture: Optional[Mapping[str, object]] = None
                 ) -> Dict[str, object]:
    """QA -> M0-M4 -> controls -> Holm -> flags -> decision, on loaded inputs.

    This is the complete audit.  It performs no I/O and opens nothing, so the
    execution-approval change has only to remove the terminal guard in
    :func:`run_audit` to reach an already finished route — it never introduces
    scientific logic for the first time.

    ``replicates`` and ``qa_fixture`` are the only fixture-facing arguments.
    Production passes neither, so the registered replicate count and the
    registered QA targets are what a real run is measured against.
    """
    rows = inputs.rows
    qa = verify_qa_targets(rows, inputs.decision, inputs.manifest, qa_fixture)
    partition = cache_partition(rows, inputs.processed_classes, inputs.cache_n)
    assert_cache_partition(partition, inputs.cache_n)

    if not qa["ok"]:
        decision = decide(False, M4_INPUT_ABSENT, {}, qa.get("first_failure"))
        return {"qa": qa, "decision": decision, "stopped": True,
                "m0": {}, "m1": {}, "m2": {}, "m3": {}, "m4": {},
                "nulls": {}, "tests": {}, "tables": {}}

    expected_counts = dict((qa_fixture or {}).get("targets") or QA_TARGETS)

    emit("QA targets reproduced; measurement may begin.")
    m0 = m0_report(rows, inputs.processed_classes, partition)
    mamba_rr = {r: (seq.pre_samples, seq.post_samples)
                for r, seq in inputs.mamba_by_record.items()}
    cache_rr = {r: (seq.pre_samples, seq.post_samples)
                for r, seq in inputs.cache_by_record.items()}
    distances = m1_distances(rows, mamba_rr, cache_rr,
                             inputs.processed_classes)
    m1 = m1_summary(distances)
    m2 = m2_report(rows)
    m3 = m3_graph(rows, inputs.mamba_by_record, inputs.cache_by_record)
    assert_m3_partition(m3, {k: expected_counts[k] for k in
                             (BJ.REASON_NO_EDGE, BJ.REASON_NOT_OPTIMAL,
                              BJ.REASON_AMBIGUOUS) if k in expected_counts})

    m4 = m4_feasibility_gate(
        runtime=inputs.m4_runtime, sources=inputs.m4_sources,
        texts=inputs.m4_texts, detector_counts=None,
        registered_counts=inputs.m4_registered_counts,
        replayed_rr=None, frozen_rr=inputs.m4_frozen_rr,
        input_identity=inputs.m4_identity,
        rr_verdict=PREP_M4_RR_EQUIVALENCE_VERDICT, replay=inputs.m4_replay)
    m4_ok = str(m4["status"]) == M4_OK
    anchors = (m4_anchors(m4, inputs.m4_anchors, rows) if m4_ok else None)

    # ---- controls, statistics, multiplicity -------------------------------
    class_vectors = build_control_a_class_vectors(
        partition, inputs.processed_classes, inputs.cache_n)
    assert_control_a_input(class_vectors, inputs.processed_classes,
                           inputs.cache_n)
    gate_rows = distance_gate_rows(distances)
    h1_observed = stat_h1(distances)

    def h1_replicate(b: int) -> float:
        shifted = control_a_class_shift(class_vectors, b)
        class_of = {(record, i): value
                    for record, vector in shifted.items()
                    for i, value in enumerate(vector)}
        return stat_h1(distances, class_of=class_of)

    null_a = run_null_family(CONTROL_A, h1_replicate, replicates=replicates)
    h1 = {"statistic": h1_observed, "p": permutation_p(h1_observed, null_a),
          "null_summary": null_summary(null_a)}
    h4 = h4_evaluate(m3["rows"], replicates=replicates)

    if m4_ok and anchors is not None:
        no_edge_positions = [(str(r["record"]), int(r["mamba_record_row"]))
                             for r in rows if is_mamba_side(r) and is_failed(r)
                             and str(r["drop_or_unmatched_reason"]) ==
                             BJ.REASON_NO_EDGE]
        all_failures = [(str(r["record"]), int(r["mamba_record_row"]))
                        for r in rows if is_mamba_side(r) and is_failed(r)]
        explained = [tuple(x) for x in anchors["explained_positions"]]
        h2_observed = stat_h2(explained, no_edge_positions)
        h3_observed = anchors["share_failures_within_10_after"]
        record_lengths = {r: len(seq) for r, seq in
                          inputs.mamba_by_record.items()}
        anchor_positions = {r: [int(a["mapped_mamba_record_row"])
                                for a in v
                                if a.get("mapped_mamba_record_row") is not None]
                            for r, v in inputs.m4_anchors.items()}

        def c_replicate(b: int, observed_kind: str) -> float:
            shifted = control_c_anchor_shift(anchor_positions, record_lengths, b)
            moved = {(r, p) for r, ps in shifted.items() for p in ps}
            if observed_kind == "H2":
                return stat_h2(sorted(moved), no_edge_positions)
            after = {(r, p + o) for r, p in moved
                     for o in range(1, M4_ANCHOR_HALF_WINDOW + 1)}
            return stat_h3(sorted(after), all_failures)

        null_c2 = run_null_family(CONTROL_C, lambda b: c_replicate(b, "H2"),
                                  replicates=replicates)
        null_c3 = run_null_family(CONTROL_C, lambda b: c_replicate(b, "H3"),
                                  replicates=replicates)
        h2 = {"statistic": h2_observed,
              "p": permutation_p(h2_observed, null_c2),
              "null_summary": null_summary(null_c2)}
        h3 = {"statistic": h3_observed,
              "p": permutation_p(h3_observed, null_c3),
              "null_summary": null_summary(null_c3)}
    else:
        h2 = {"statistic": None, "p": None, "status": UNEVALUABLE}
        h3 = {"statistic": None, "p": None, "status": UNEVALUABLE}

    holm = holm_4family({"H1": h1["p"], "H2": h2["p"], "H3": h3["p"],
                         "H4": h4["p"]})
    m5_report = m0.get("m5", {})
    reported = strata_reported(m5_report)
    long_run_share = m0["runs_primary_mamba_row"]["share_in_long_runs"]
    gate_bins = m1["bins_in_distance_gate"]
    evidence = {
        "H1": {"strata_reported": reported, "effect_gates": {
            "share_2_5_at_least_half": bool(
                _ratio(sum(1 for e in gate_rows
                           if str(e["reason"]) == BJ.REASON_NO_EDGE
                           and str(e["processed_class"]) == "V"
                           and str(e["bin"]) == M1_GATE_BIN),
                       sum(1 for e in gate_rows
                           if str(e["reason"]) == BJ.REASON_NO_EDGE
                           and str(e["processed_class"]) == "V"))
                >= EFFECT_SHARE_MIN),
            "exceeds_control_a_q99": bool(
                h1["statistic"] > h1["null_summary"]["q99"]),
            "run_mass_mostly_short": bool(long_run_share < EFFECT_SHARE_MIN),
            "m4_propagation_gate_not_met": not m4_ok}},
        "H4": {"strata_reported": reported,
               "effect_gates": h4["effect_gates"]},
    }
    if m4_ok:
        evidence["H2"] = {"strata_reported": reported, "effect_gates": {
            "explains_at_least_half": bool(
                h2["statistic"] >= EFFECT_SHARE_MIN),
            "exceeds_control_c_q99": bool(
                h2["statistic"] > h2["null_summary"]["q99"])}}
        evidence["H3"] = {"strata_reported": reported, "effect_gates": {
            "exceeds_control_c_q99": bool(
                h3["statistic"] > h3["null_summary"]["q99"]),
            "half_in_long_runs": bool(long_run_share >= EFFECT_SHARE_MIN),
            "distance_mass_far": bool(
                sum(gate_bins[b] for b in M1_H3_FAR_BINS)
                > gate_bins[M1_GATE_BIN])}}

    flags = evaluate_flags(evidence, holm)
    decision = decide(qa["ok"], str(m4["status"]), flags,
                      qa.get("first_failure"))
    tests = {name: {**{"statistic": value.get("statistic"),
                       "p": value.get("p"),
                       "p_holm_4family": holm["p_holm_4family"][name],
                       "q99": (value.get("null_summary") or {}).get("q99")},
                    **flags[name]}
             for name, value in (("H1", h1), ("H2", h2), ("H3", h3),
                                 ("H4", h4))}
    tables = build_tables(m0, distances, m3, anchors, partition)
    nulls = {CONTROL_A: h1.get("null_summary", {}),
             CONTROL_B: h4.get("null_summary", {}),
             CONTROL_C: ({"H2": h2.get("null_summary", {}),
                          "H3": h3.get("null_summary", {})} if m4_ok
                         else {"status": UNEVALUABLE,
                               "reason": "M4.0 did not pass"})}
    return {"qa": qa, "m0": m0, "m1": m1, "m2": m2, "m3": m3,
            "m4": {**m4, **({"anchors_report": anchors} if anchors else {})},
            "nulls": nulls, "tests": tests, "holm": holm, "flags": flags,
            "decision": decision, "tables": tables, "stopped": False}


def build_tables(m0: Mapping[str, object],
                 distances: Sequence[Mapping[str, object]],
                 m3: Mapping[str, object],
                 anchors: Optional[Mapping[str, object]],
                 partition: Sequence[Mapping[str, object]]
                 ) -> Dict[str, List[Dict[str, object]]]:
    """The registered CSV tables, in their registered column order."""
    class_rows: List[Dict[str, object]] = []
    for side, per_class in dict(m0.get("class_by_reason", {})).items():
        for cls, reasons in per_class.items():
            for reason, values in reasons.items():
                if reason.startswith("_"):
                    continue
                class_rows.append({"side": side, "class": cls,
                                   "reason": reason, **values,
                                   "rate": values.get("share")})
    record_rows = [
        {"record": entry["record"], "stratum": entry["stratum"],
         "class": entry["class"], "side": SIDE_CACHE,
         "denominator": 1, "failures": 1 if entry["failed"] else 0,
         "rate": 1.0 if entry["failed"] else 0.0}
        for entry in partition]
    run_rows: List[Dict[str, object]] = []
    for adjacency in ADJACENCIES:
        key = ("runs_primary_mamba_row" if adjacency == ADJ_PRIMARY
               else "runs_secondary_raw_ordinal")
        summary = dict(m0.get(key, {}))
        for record, value in dict(summary.get("per_record", {})).items():
            for bucket, count in dict(value.get("buckets", {})).items():
                run_rows.append({
                    "record": record, "adjacency_definition": adjacency,
                    "run_start": bucket, "run_length": count,
                    "classes": "", "reasons": "",
                    "decisional": adjacency == ADJ_PRIMARY})
    tables = {
        "m0_class_by_reason.csv": class_rows,
        "m0_record_class.csv": record_rows,
        "m0_runs.csv": run_rows,
        "m1_distance.csv": list(distances),
        "m3_graph.csv": list(m3.get("rows", [])),
    }
    if anchors is not None:
        tables["m4_anchors.csv"] = list(anchors.get("rows", []))
    return tables


def run_audit_from_mount(search_root: str, out_dir: str,
                         approval: Optional[str] = None,
                         open_registered_data: bool = OPEN_REGISTERED_DATA,
                         emit=print) -> Dict[str, object]:
    """:func:`run_audit` with every input path resolved by digest.

    This is the route the notebook uses, so no Drive path is ever typed by
    hand.  The approval and `open_registered_data` switches are checked here
    first, before discovery opens anything.
    """
    if not open_registered_data:
        raise ExecutionNotApprovedError(
            f"OPEN_REGISTERED_DATA is False.  {APPROVAL_NOTE}")
    require_execution_approval(approval, f"input discovery under {search_root!r}")
    paths = discover_registered_inputs(search_root, approval)
    emit(f"Q5-E: resolved every registered input by digest under "
         f"{search_root!r}.")
    return run_audit(paths["bundle_dir"], paths["mamba_path"],
                     paths["cache_dir"], paths["mitdb_dir"], out_dir,
                     v10_source_dir=paths["v10_source_dir"],
                     approval=approval,
                     open_registered_data=open_registered_data, emit=emit)


def run_audit(bundle_dir: str, mamba_path: str, cache_dir: str,
              mitdb_dir: str, out_dir: str,
              v10_source_dir: str = "",
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
    emit("Q5-E: canonical bundle verified.")

    _terminal_execution_guard()

    # ---- Everything below is the complete, already-implemented audit. ------
    # Removing the guard above is the *only* change the execution-approval PR
    # makes here: it must expose a finished route, never introduce scientific
    # analysis for the first time.
    inputs = load_all_inputs(bundle_dir, mamba_path, cache_dir, mitdb_dir,
                             v10_source_dir, approval)
    outcome = run_pipeline(inputs, emit=emit)
    timestamp = run_timestamp()
    result = build_result(
        qa=outcome["qa"], m0=outcome["m0"], m1=outcome["m1"],
        m2=outcome["m2"], m3=outcome["m3"], m4=outcome["m4"],
        nulls=outcome["nulls"], tests=outcome["tests"],
        decision=outcome["decision"], source_files=canonical["files"])
    directory = os.path.join(out_dir, f"{timestamp}_{RUN_SLUG}")
    write_bundle(directory, result,
                 build_config(MODE_AUDIT, timestamp, execution_approved=True),
                 build_manifest({"bundle": bundle_dir, "cache": cache_dir,
                                 "mamba": mamba_path, "mitdb": mitdb_dir},
                                timestamp),
                 outcome["tables"], outcome["nulls"],
                 [f"decision={result['decision']}"],
                 summary_markdown(result),
                 figures=True, require_complete=True)
    emit(f"Q5-E: decision {result['decision']}")
    return result


def _terminal_execution_guard() -> None:
    """The one line the execution-approval change removes.

    It sits *after* every check and *before* the first registered read, so an
    approved run reaches a complete pipeline and an unapproved one reaches
    nothing.
    """
    raise Q5EError(
        "run_audit is implemented but has never been executed: the separate "
        "user approval for running M0-M4 on the registered artifacts does not "
        "exist yet.  This is the deliberate terminal guard; the "
        "execution-approval change removes it and nothing else.")


def run_timestamp() -> str:
    """UTC stamp for a new bundle directory name."""
    import datetime                                       # noqa: PLC0415
    return datetime.datetime.now(datetime.timezone.utc).strftime(
        "%Y%m%dT%H%M%S")


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
