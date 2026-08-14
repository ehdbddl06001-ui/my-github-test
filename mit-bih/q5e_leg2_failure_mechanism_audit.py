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
#:
#: **Registered 2026-08-14** by the P1/P2 registration PR, after the
#: `20260814T104835` PREP run returned `PREP_P1_P2_PASS` and Codex accepted it
#: (`PREP_P1_P2_RESULT_ACCEPTED`, `CORRECTIVE_PROMOTION_APPROVED`).  This names
#: the **corrective packaging-derived canonical Q5-E input** built by
#: EXP-2026-009 on 2026-08-13 — see :data:`SOURCE_BUNDLE_PROVENANCE` for what
#: that does and does not mean.  It is *not* the folder EXP-2026-007 published,
#: and no EXP-2026-007 execution ever produced a twelve-file bundle.
#: The accepted registration, as **one record**.  Every public constant below
#: is derived from it rather than restated beside it.
#:
#: Restating them was a real defect and not a hypothetical one: the first
#: version of this registration checked the folder id and run only for being
#: *different from* the pre-registration values, so `"wrong-folder"` and
#: `"wrong-run"` passed as a complete, atomic, well-formed registration.  A
#: check that accepts any value except one is not an identity check.  The
#: accepted states are now exactly two — this record, or the historical
#: unregistered one — and everything else stops.
#:
#: This record is not self-certifying, and nothing in a repository can be: an
#: edit here moves the target it is compared against.  What backs it is
#: outside the module — `research/ASSETS.md`, the execution contract's D9-D12,
#: and a regression test that pins all four values as literals.
APPROVED_INPUT_IDENTITY: Dict[str, object] = {
    "mitdb_tree_aggregate":
        "0b46a411c1882fc5e09e2e60c2613ca441574c78a62f84272ad3ff4a2179ade8",
    "source_bundle_folder_id": "1JzRW_Xdes4Ywp4-VYVvksFFih_RQVbhH",
    "source_bundle_run": ("20260813T000000_EXP-2026-009_q5d_null_artifact_"
                          "repair_corrective"),
    "source_bundle_file_sha256": {
        "decision.json":
            "d464a4059e6cad39de1018b3eaecb0b7713c9fd0839fbed94ffa4be2b2d7e8e5",
        "join_map.parquet":
            "dad93d340f2ca0db30b4c8c77e13f847e612b342b1e31c47a1b411fa8fd62971",
        "manifest.json":
            "4bd7b4d8bb2ce9a3461b85ecdf65761ce1ad625bd6c6adc1d39c6c12029fbb4c",
        "record_class_coverage.csv":
            "e786c203ffe23c67ba7d412c64703813b5cb22ecbe7d17f53679ee94d982ccec",
        "unmatched_and_ambiguous.csv":
            "b6134468493b32fa5b56cfff9c35aee4d4059d6d8f321c6678a06acdf250459f",
    },
}

SOURCE_BUNDLE_RUN = str(APPROVED_INPUT_IDENTITY["source_bundle_run"])
SOURCE_BUNDLE_FOLDER_ID = str(APPROVED_INPUT_IDENTITY["source_bundle_folder_id"])

#: The EXP-2026-007 run whose eleven files the corrective bundle copies
#: byte-identically, and the folder the 2026-08-12 PREP run read and stopped on
#: with `missing: ['negative_control_null.npz']`.  Kept — not deleted by the
#: registration — because it is the lineage of eleven of the twelve files and
#: the reason the twelfth had to be rebuilt.  It is **not** a fallback input:
#: nothing below reads it, and a bundle matching it would fail the registered
#: digests.
ORIGINAL_PRODUCER_RUN = "20260811T035108_EXP-2026-007_q5d_beat_join_DS1_GATE"
ORIGINAL_PRODUCER_FOLDER_ID = "1JjwBhU8BXf8lRrYPcM2UjFNdIKxE9Ghd"

#: The **only** other accepted state: this module before the 2026-08-14
#: registration.  Kept so that "unregistered" is an exact match against a
#: recorded state rather than "does not happen to equal the approved one",
#: which is how an arbitrary value slipped through the first version.
UNREGISTERED_INPUT_IDENTITY: Dict[str, object] = {
    "mitdb_tree_aggregate": None,
    "source_bundle_folder_id": ORIGINAL_PRODUCER_FOLDER_ID,
    "source_bundle_run": ORIGINAL_PRODUCER_RUN,
    "source_bundle_file_sha256": {},
}

#: Where the registered bundle came from, in the terms the acceptance fixed.
#: This is a provenance record, not a gate: nothing here is compared against an
#: observation, and no value in it enters a p-value, a threshold or a decision.
#:
#: The distinction it exists to keep is the one a reader gets wrong most
#: easily.  Eleven of the twelve files are byte-identical copies of the
#: EXP-2026-007 outputs.  The twelfth, `negative_control_null.npz`, is **not** a
#: file the original producer ever wrote: no EXP-2026-007 execution produced it,
#: and it was reconstructed a day later by a separate EXP-2026-009
#: packaging-repair module from the 100 preregistered null shards, through the
#: frozen `finalize_null_shards()` path.  Writing "the original EXP-2026-007 run
#: produced a twelve-file bundle" would therefore be false.
#:
#: What the repair did **not** change: no scientific rule, no null value, no
#: seed, no replicate count, no family.  Replicate coverage was 10000/10000 with
#: zero gaps and zero overlaps, and the reconstructed `j_null_max` is
#: element-wise identical to the vector the original `null_summary.json`
#: already carried — two independent code paths in the original run agreeing.
SOURCE_BUNDLE_PROVENANCE: Dict[str, object] = {
    "kind": "corrective packaging-derived canonical Q5-E input",
    "registered_on": "2026-08-14",
    "registered_by": "EXP-2026-008 Q5-E PREP P1/P2 registration PR",
    "verdict": "PREP_P1_P2_RESULT_ACCEPTED / CORRECTIVE_PROMOTION_APPROVED",
    "prep_run": "20260814T104835_EXP-2026-008_q5e_prep_p1_p2_asset_identity",
    "repair_spec": ("experiments/specs/"
                    "EXP-2026-009-q5d-null-artifact-repair.md"),
    "files_copied_byte_identical": 11,
    "files_reconstructed": 1,
    "reconstructed_file": "negative_control_null.npz",
    "reconstructed_by": "EXP-2026-009 packaging repair, 2026-08-13",
    "reconstructed_from": "100 preregistered null shards",
    "reconstruction_path": "frozen finalize_null_shards()",
    "replicate_coverage": "10000/10000, 0 gaps, 0 overlaps",
    "j_null_max_matches_null_summary": "element-wise identical",
    "original_producer_run": ORIGINAL_PRODUCER_RUN,
    "original_producer_folder_id": ORIGINAL_PRODUCER_FOLDER_ID,
    "original_producer_file_count": 11,
    "original_run_produced_twelve_files": False,
    "science_changed": False,
    "note": ("a deterministic packaging recovery of a missing output, not a "
             "re-run and not a change to any scientific rule, null value, "
             "seed or replicate count"),
}

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
#: Written into a synthetic bundle so an ingester can refuse it without
#: parsing prose.  Its presence is the machine-readable "do not ingest".
SYNTHETIC_MARKER = "SYNTHETIC_FIXTURE.json"
SYNTHETIC_NOTE = ("Produced against injected fixture QA targets by the "
                  "synthetic self-test. Not a Q5-E result and not an ingest "
                  "candidate.")

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
#: The registered V10 source expected set (spec §"Frozen M4 identity
#: constants").  Verification fails on either a missing or an extra file, so
#: this is a fixed set and never a glob over whatever the folder holds.
M4_V10_SOURCE_FILES: Tuple[str, ...] = (
    "__init__.py", "data.py", "evaluate.py", "frontend.py", "model.py",
    "pwave.py", "train.py")
#: The V9 corroborating set.  Recorded so a V9 folder cannot be mistaken for
#: the V10 one by file count alone; V9 is never an M4 input.
M4_V9_SOURCE_FILES: Tuple[str, ...] = (
    "__init__.py", "data.py", "evaluate.py", "frontend.py", "model.py",
    "train.py", "v15b_local.py")
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
#: One kind per registered figure.  Distinct by construction: two figures
#: sharing a kind is what let the run-length figure silently render the
#: distance series.
FIG_CLASS_REASON = "m0_class_reason_stacked_with_side_panels"
FIG_RECORD_CLASS_HEATMAP = "m0_record_class_heatmap"
FIG_RECORD_208_RASTER = "m0_record_208_raster_with_raw_ordinal_sensitivity"
FIG_RUN_LENGTH_HIST = "m0_run_length_histogram_with_summary"
FIG_DISTANCE_HIST = "m1_fixed_bin_distance_histogram_with_exclusions"
FIG_DEGREE_VIOLIN_ECDF = "m3_candidate_degree_violin_and_ecdf_by_side"
FIG_ANCHOR_CURVE = "m4_anchor_curve_with_control_c_band"
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
    "runtime", "source_map", "input_identity", "source_match_equivalence",
    "detector_replay", "record_counts", "rr_equality")
#: The sub-gates that must all pass **before** the detector may be called.
#: `source_match_equivalence` sits last among them: the annotation-matching
#: adapter is the thing the replay's counts are produced *through*, so running
#: the detector before that adapter has been shown equivalent to the
#: registered source would produce numbers no one can interpret.
M4_GATES_BEFORE_REPLAY: Tuple[str, ...] = (
    "runtime", "source_map", "input_identity", "source_match_equivalence")

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


class ReplayContractError(DiagnosticInputMismatch):
    """The detector replay returned something outside its registered contract.

    Narrow on purpose.  This is the *only* exception `m4_feasibility_gate`
    converts into a registered `M4` failure, so a shape violation becomes
    `DIAGNOSTIC_INPUT_ABSENT` — the branch the spec already defines — instead
    of killing the run and losing the M0-M3 partial results with it.  A
    programmer error must keep propagating, so nothing broader is caught.
    """


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


def frozen_module_approval(approval: Optional[str], what: str) -> str:
    """Translate a Q5-E execution approval into the frozen module's token.

    The two modules use different approval tokens, so handing Q5-E's token to
    a `BJ.*` reader is refused by the frozen module — every registered read on
    the production path would have failed at execution time, and only then.
    The translation is deliberate and narrow: Q5-E's own approval is required
    **first**, and only then is Q5-D's token produced, for the same registered
    assets Q5-D already reads.  It grants nothing Q5-E was not approved for,
    and an unapproved caller gets Q5-E's own refusal rather than Q5-D's.
    """
    require_execution_approval(approval, what)
    return BJ.EXECUTION_APPROVAL_TOKEN


def _bj(approval: Optional[str]) -> str:
    """Short alias for :func:`frozen_module_approval` at call sites."""
    return frozen_module_approval(approval, "a frozen Q5-D reader")


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
            "reverify_registered_inputs", "verify_mitdb_identity",
            "verify_bundle_directory_contract", "subset_file_fold",
            "registered_bundle_digests_complete", "prep_payload_fold",
            "input_identity_registration", "assert_registration_is_atomic",
            "detector_replay_performed",
            "verify_bundle_content_identity", "resolve_identical_candidates",
            "source_match_equivalence_status",
            "verify_source_match_equivalence", "build_detector_replay",
            "match_peaks_to_annotations", "load_frozen_rr", "build_m4_anchors",
            "hypothesis_strata", "stratified_statistic",
            "has_stratified_evidence", "figure_data",
            "assert_bundle_inputs_complete",
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
    # Read from the producer's schema, not a flat key no producer writes.  The
    # same defect that broke `verify_bundle_directory_contract` lived here too:
    # against a real manifest `manifest['code_sha256']` resolves to `""`, so
    # this QA target failed on every canonical bundle for a reason that had
    # nothing to do with the bundle.  One reader, one spelling.
    code_block = manifest.get("code")
    code = (str(code_block.get("sha256") or "")
            if isinstance(code_block, Mapping) else "")
    targets["producing_code_sha256"] = {
        "expected": expected_code, "observed": code,
        "read_from": MANIFEST_IDENTITY_SOURCES["code_sha256"],
        "ok": code == expected_code}
    ok = all(entry["ok"] for entry in targets.values())
    return {"targets": targets, "ok": ok, "target_set": target_set,
            "first_failure": None if ok else
            sorted(k for k, v in targets.items() if not v["ok"])[0]}


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


def stratum_levels(items: Sequence[Mapping[str, object]], stratum: str
                   ) -> Dict[str, List[Mapping[str, object]]]:
    """Split ``items`` into the levels of one registered stratum.

    Each item states its own `record`, and optionally `class` and `reason`.
    A stratum an item cannot answer for simply has no level for it — this
    never invents a class or a reason to keep a cell populated.
    """
    levels: Dict[str, List[Mapping[str, object]]] = {}
    for item in items:
        record = str(item.get("record") or "")
        if stratum == POOLED:
            keys: List[str] = [POOLED]
        elif stratum == "class":
            value = str(item.get("class") or "")
            keys = [value] if value in AAMI_CLASSES else []
        elif stratum == "reason":
            value = str(item.get("reason") or "")
            keys = [value] if value in REASON_TO_GROUP else []
        elif stratum == "record":
            keys = [record] if record else []
        elif stratum == "count_stratum":
            keys = [record_stratum(record)] if record else []
        elif stratum in ("record_116", "record_208"):
            keys = [record] if record == stratum.split("_")[1] else []
        else:                                            # pragma: no cover
            raise Q5EError(f"unknown stratum {stratum!r}")
        for key in keys:
            levels.setdefault(key, []).append(item)
    return levels


def stratified_statistic(items: Sequence[Mapping[str, object]],
                         statistic, minimum: int = 1
                         ) -> Dict[str, Dict[str, object]]:
    """Evaluate one hypothesis statistic inside every registered stratum.

    A level with fewer than ``minimum`` items, or whose statistic is not
    computable, is recorded as `NOT_APPLICABLE`.  A stratum counts as
    *materialised* only when at least one of its levels produced a real
    number — which is the whole point: a stratum name in the result JSON is
    not stratified evidence, and this is what makes the difference checkable.
    """
    out: Dict[str, Dict[str, object]] = {}
    for stratum in M5_STRATA:
        levels = stratum_levels(items, stratum)
        entries: Dict[str, object] = {}
        materialised = False
        for level, subset in sorted(levels.items()):
            if len(subset) < minimum:
                entries[level] = {"n": len(subset), "statistic": None,
                                  "status": NOT_APPLICABLE}
                continue
            try:
                value = statistic(subset)
            except (ZeroDivisionError, ValueError, statistics.StatisticsError):
                value = None
            if value is None:
                entries[level] = {"n": len(subset), "statistic": None,
                                  "status": NOT_APPLICABLE}
                continue
            entries[level] = {"n": len(subset), "statistic": float(value),
                              "status": "OK"}
            materialised = True
        out[stratum] = {"levels": entries, "materialised": bool(materialised),
                        "status": "OK" if materialised else NOT_APPLICABLE}
    return out


def materialised_strata(report: Mapping[str, Mapping[str, object]]
                        ) -> List[str]:
    """The strata of one hypothesis that actually carry a number."""
    return [name for name in M5_STRATA
            if dict(report.get(name, {})).get("materialised")]


def has_stratified_evidence(report: Mapping[str, Mapping[str, object]]
                            ) -> bool:
    """True only when some **non-pooled** stratum carries a real number.

    `A mechanism is never declared from the pooled value alone.`  Enforcing
    that on the presence of stratum *names* was the defect: names are always
    present.  This asks whether a stratified statistic was actually computed.
    """
    return bool([name for name in materialised_strata(report)
                 if name != POOLED])


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
                        replay: Optional[object] = None,
                        source_match_oracle: Optional[Mapping[str, object]]
                        = None) -> Dict[str, object]:
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

    # The annotation-matching adapter is what the replay's counts are produced
    # *through*, so it must be shown equivalent to the registered source
    # before the detector runs at all — otherwise the counts depend on an
    # unverified reimplementation and mean nothing.  This is a terminal stop,
    # not a warning attached to the result afterwards.
    step = verify_source_match_equivalence(source_match_oracle)
    gates.append(step)
    if not step["ok"]:
        return _m4_absent(gates, identity, step["reason"])

    # Only now may the detector run.  Every sub-gate in
    # `M4_GATES_BEFORE_REPLAY` has passed and is already recorded, in the
    # registered order.  `replay` is injected so the gate is testable without
    # ever calling `detect_r()`.
    assert [g["gate"] for g in gates] == list(M4_GATES_BEFORE_REPLAY)
    if detector_counts is None and replay is not None:
        try:
            detector_counts, replayed_rr = replay()
        except ReplayContractError as error:
            # The detector *did* run; its output violated the registered
            # replay contract.  That is a registered M4 outcome, so it becomes
            # DIAGNOSTIC_INPUT_ABSENT and the M0-M3 partial results survive,
            # rather than an exception that destroys the whole run.  Only this
            # typed error is converted: a programmer error still propagates.
            gates.append({"gate": "detector_replay", "ok": True,
                          "reason": None,
                          "note": "the detector ran; its output was rejected"})
            gates.append({"gate": "rr_equality", "ok": False,
                          "reason": M4_RR_MISMATCH,
                          "problems": [str(error)]})
            return _m4_absent(gates, identity, M4_RR_MISMATCH)
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
        # Stratified evidence means a stratified *statistic*, not a stratum
        # name.  `strata` carries the per-level numbers this hypothesis
        # actually produced; a hypothesis that only has a pooled number cannot
        # fire however significant it is.
        strata = dict(evidence.get(name, {}).get("strata", {}))
        reported = (materialised_strata(strata) if strata
                    else list(evidence.get(name, {}).get("strata_reported", ())))
        stratified = (has_stratified_evidence(strata) if strata
                      else bool([x for x in reported if x != POOLED]))
        out[name] = {
            "flag": bool(gates_ok and significant[name] and stratified),
            "evaluable": True, "status": "EVALUATED",
            "effect_gates": conditions,
            "strata_reported": reported,
            "stratified_evidence": bool(stratified),
            "pooled_only_blocked": not bool(stratified),
            "holm_significant": bool(significant[name]),
            "p_holm_4family": holm["p_holm_4family"][name]}
    return out


def decide(qa_ok: bool, m4_status: str,
           flags: Mapping[str, Mapping[str, object]],
           qa_first_failure: Optional[str] = None,
           m4_first_failure: Optional[str] = None) -> Dict[str, object]:
    """The registered decision tree, evaluated in order; exactly one branch.

    ``m4_first_failure`` carries M4's own first failing sub-gate into the
    result.  The terminal decision and the multiplicity family are unchanged;
    what changes is that a reader of `q5e_result.json` can tell
    `SOURCE_MATCH_EQUIVALENCE_REQUIRED` from `M4_COUNT_MISMATCH` from
    `M4_FROZEN_RR_MISMATCH`, instead of seeing only the umbrella status they
    all collapse into.
    """
    if not qa_ok:
        return {"decision": DECISION_MISMATCH,
                "first_stopping_reason": qa_first_failure or "qa_targets",
                "fired": []}
    if m4_status != M4_OK:
        fired = [HYPOTHESIS_FLAG[h] for h in ("H1", "H4")
                 if flags.get(h, {}).get("flag")]
        return {"decision": DECISION_UNRESOLVED,
                "first_stopping_reason": m4_first_failure or m4_status,
                "m4_status": m4_status,
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
                 execution_approved: bool = False,
                 qa_target_set: str = QA_TARGETS_REGISTERED
                 ) -> Dict[str, object]:
    synthetic = qa_target_set != QA_TARGETS_REGISTERED
    return {
        "experiment_id": EXPERIMENT_ID, "substage": SUBSTAGE,
        "run_slug": RUN_SLUG, "module_version": MODULE_VERSION,
        "mode": resolve_mode(mode), "timestamp": timestamp,
        "spec": SPEC_PATH,
        "qa_target_set": qa_target_set,
        "synthetic_fixture": synthetic,
        "ingestable": not synthetic,
        "master_seed": MASTER_SEED, "n_null_replicates": N_NULL_REPLICATES,
        "window_half_width": M1_WINDOW_HALF_WIDTH,
        "adjacency_primary": ADJ_PRIMARY,
        "adjacency_secondary_non_decisional": ADJ_SECONDARY,
        "h4_decisional_side": H4_DECISIONAL_SIDE,
        "execution_on_registered_data_approved": bool(execution_approved),
        "approval_note": APPROVAL_NOTE,
    }


def build_manifest(inputs: Mapping[str, object], timestamp: str,
                   qa_target_set: str = QA_TARGETS_REGISTERED
                   ) -> Dict[str, object]:
    synthetic = qa_target_set != QA_TARGETS_REGISTERED
    return {
        "experiment_id": EXPERIMENT_ID, "substage": SUBSTAGE,
        "timestamp": timestamp,
        "qa_target_set": qa_target_set,
        "synthetic_fixture": synthetic,
        "ingestable": not synthetic,
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


def detector_replay_performed(m4: Mapping[str, object]) -> bool:
    """Did the registered detector actually run?

    Not the same question as "did M4 pass".  A replay that ran and then failed
    the record-count or RR sub-gate *did* execute the detector, and a seal that
    reported `false` there would be untrue.  Conversely a run stopped at the
    source-equivalence sub-gate never reached the detector at all.  So this
    reads the gate list rather than the overall status.
    """
    for gate in m4.get("gates", ()) or ():
        if str(gate.get("gate")) == "detector_replay":
            return bool(gate.get("ok"))
    return False


def build_result(qa: Mapping[str, object], m0: Mapping[str, object],
                 m1: Mapping[str, object], m2: Mapping[str, object],
                 m3: Mapping[str, object], m4: Mapping[str, object],
                 nulls: Mapping[str, object], tests: Mapping[str, object],
                 decision: Mapping[str, object],
                 source_files: Sequence[Mapping[str, object]] = (),
                 identity_audit: Optional[Mapping[str, object]] = None
                 ) -> Dict[str, object]:
    """Assemble `q5e_result.json` in exactly the registered schema."""
    target_set = str(qa.get("target_set") or QA_TARGETS_REGISTERED)
    return {
        "experiment_id": EXPERIMENT_ID, "substage": SUBSTAGE,
        # Every identity check and its problem list, kept in the result so a
        # reader can see what was verified rather than trusting that it was.
        "identity_audit": dict(identity_audit or {}),
        "qa_target_set": target_set,
        "synthetic_fixture": target_set != QA_TARGETS_REGISTERED,
        "analysis_only": True, "training_performed": False,
        "model_scored": False, "v10_probability_opened": False,
        "ds2_labels_opened": False, "association_performed": False,
        # Whether the detector actually ran, which is not the same question as
        # whether M4 passed: a replay that ran and then failed the count or RR
        # sub-gate did happen, and the seal must say so.
        "detector_replay_performed": detector_replay_performed(m4),
        "m4_status": str(m4.get("status") or ""),
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
                   m4_ok: bool, backend=None,
                   nulls: Optional[Mapping[str, object]] = None) -> List[str]:
    """Render the registered figures as real PNG files.

    Each figure gets its own data through :func:`figure_data`; two figures
    never share a series because their `kind` happens to be similar.  That was
    a real defect: the run-length figure and the distance figure both rendered
    the distance bins, so one of them was silently a duplicate of the other.

    ``backend`` is injectable so a synthetic end-to-end test can exercise the
    complete bundle contract without depending on a plotting library.  The
    default backend is matplotlib with the non-interactive Agg canvas.  All
    titles, axis labels, tick labels and legends are ASCII.
    """
    specs = figure_specs(m4_ok)
    assert_ascii_labels(specs)
    writer = backend or _matplotlib_backend
    written: List[str] = []
    seen: Dict[str, str] = {}
    for spec in specs:
        path = os.path.join(directory, str(spec["file"]))
        if os.path.exists(path):
            raise Q5EError(f"refusing to overwrite an existing figure {path!r}")
        data = figure_data(str(spec["kind"]), tables, nulls)
        fingerprint = _canonical_json(data)
        clash = seen.get(fingerprint)
        if clash is not None:
            raise Q5EError(
                f"figures {clash!r} and {spec['file']!r} would render exactly "
                f"the same data.  Each registered figure shows a different "
                f"measurement; a duplicate is a rendering bug, not a figure.")
        seen[fingerprint] = str(spec["file"])
        writer(path, spec, tables, data)
        written.append(str(spec["file"]))
    return sorted(written)


def figure_data(kind: str,
                tables: Mapping[str, Sequence[Mapping[str, object]]],
                nulls: Optional[Mapping[str, object]] = None
                ) -> Dict[str, object]:
    """The panels of one registered figure, built from the written tables.

    Returned as data so a test can assert what each figure *shows* without
    importing matplotlib or reading pixels.
    """
    if kind == FIG_CLASS_REASON:
        # Stacked bar of reason within class, one panel per side.
        panels: Dict[str, object] = {}
        for side in SIDES:
            stacks: Dict[str, Dict[str, float]] = {}
            for row in tables.get("m0_class_by_reason.csv", []):
                if str(row.get("side")) != side:
                    continue
                stacks.setdefault(str(row.get("class")), {})[
                    str(row.get("reason"))] = float(row.get("count") or 0)
            panels[side] = {"categories": sorted(stacks),
                            "stacks": {k: stacks[k] for k in sorted(stacks)}}
        return {"kind": kind, "panels": panels}

    if kind == FIG_RECORD_CLASS_HEATMAP:
        # records x the three AAMI classes, as a real matrix of rates.
        rows = tables.get("m0_record_class.csv", [])
        records = sorted({str(r.get("record")) for r in rows})
        cells: Dict[str, Dict[str, object]] = {}
        for record in records:
            per_class: Dict[str, object] = {}
            for cls in AAMI_CLASSES:
                selected = [r for r in rows if str(r.get("record")) == record
                            and str(r.get("class")) == cls]
                denominator = sum(int(r.get("denominator") or 0)
                                  for r in selected)
                failures = sum(int(r.get("failures") or 0) for r in selected)
                per_class[cls] = (_ratio(failures, denominator)
                                  if denominator else None)
            cells[record] = per_class
        return {"kind": kind, "rows": records, "columns": list(AAMI_CLASSES),
                "cells": cells, "shape": [len(records), len(AAMI_CLASSES)]}

    if kind == FIG_RECORD_208_RASTER:
        # Beat-level state for record 208, plus the raw-ordinal sensitivity
        # that shows the same failures split into different runs.
        graph = [r for r in tables.get("m3_graph.csv", [])
                 if str(r.get("record")) == "208"
                 and str(r.get("side")) == SIDE_MAMBA]
        raster = [{"row": int(r.get("row") or 0),
                   "group": str(r.get("group")),
                   "failed": str(r.get("group")) != GROUP_CERTIFIED}
                  for r in sorted(graph, key=lambda r: int(r.get("row") or 0))]
        sensitivity: Dict[str, Dict[str, float]] = {}
        for row in tables.get("m0_runs.csv", []):
            if str(row.get("record")) != "208":
                continue
            adjacency = str(row.get("adjacency_definition"))
            sensitivity.setdefault(adjacency, {})[str(row.get("run_start"))] = \
                float(row.get("run_length") or 0)
        return {"kind": kind, "raster": raster,
                "raw_ordinal_sensitivity": sensitivity,
                "decisional_adjacency": ADJ_PRIMARY}

    if kind == FIG_RUN_LENGTH_HIST:
        # Run lengths, decisional adjacency only, plus summary statistics.
        buckets: Dict[str, float] = {}
        values: List[float] = []
        for row in tables.get("m0_runs.csv", []):
            if str(row.get("adjacency_definition")) != ADJ_PRIMARY:
                continue
            bucket = str(row.get("run_start"))
            count = float(row.get("run_length") or 0)
            buckets[bucket] = buckets.get(bucket, 0.0) + count
            values.append(count)
        summary = {"n_buckets": len(buckets), "total": sum(values),
                   "median": median(values) if values else None,
                   "max": max(values) if values else None}
        return {"kind": kind, "buckets": {k: buckets[k] for k in sorted(buckets)},
                "summary": summary, "adjacency": ADJ_PRIMARY}

    if kind == FIG_DISTANCE_HIST:
        # The registered fixed bins, in registered order, plus the two
        # descriptive exclusion counts beside them.
        rows = tables.get("m1_distance.csv", [])
        order = [name for name, _lo, _hi in M1_BINS]
        counts = {name: 0 for name in order}
        for row in rows:
            key = str(row.get("bin"))
            if key in counts:
                counts[key] += 1
        descriptive = {
            CENSORED_FLAG: sum(
                1 for r in rows if r.get("censored")),
            ENDPOINT_ZERO_FLAG: sum(
                1 for r in rows if r.get("cache_endpoint_zero"))}
        return {"kind": kind, "bins": order, "counts": counts,
                "descriptive_exclusions": descriptive}

    if kind == FIG_DEGREE_VIOLIN_ECDF:
        # Candidate degree per side, with each side labelled decisional or not.
        rows = tables.get("m3_graph.csv", [])
        panels = {}
        for side in SIDES:
            by_group: Dict[str, List[float]] = {}
            for row in rows:
                if str(row.get("side")) != side:
                    continue
                by_group.setdefault(str(row.get("group")), []).append(
                    float(row.get("candidate_degree") or 0))
            panels[side] = {
                "decisional": side == H4_DECISIONAL_SIDE,
                "label": ("H4 decisional" if side == H4_DECISIONAL_SIDE
                          else "descriptive, non-decisional"),
                "violin": {k: sorted(by_group[k]) for k in sorted(by_group)},
                "ecdf": {k: ecdf(by_group[k]) for k in sorted(by_group)}}
        return {"kind": kind, "panels": panels}

    if kind == FIG_ANCHOR_CURVE:
        rows = tables.get("m4_anchors.csv", [])
        by_offset: Dict[int, List[float]] = {}
        for row in rows:
            by_offset.setdefault(int(row.get("offset") or 0), []).append(
                1.0 if row.get("failed") else 0.0)
        offsets = sorted(by_offset)
        curve = [_ratio(sum(by_offset[k]), len(by_offset[k])) for k in offsets]
        control = dict((nulls or {}).get(CONTROL_C) or {})
        band = {}
        for name in ("H2", "H3"):
            entry = dict(control.get(name) or {})
            if entry:
                band[name] = {"q99": entry.get("q99"),
                              "mean": entry.get("mean"),
                              "min": entry.get("min"), "max": entry.get("max")}
        return {"kind": kind, "offsets": offsets, "curve": curve,
                "control_c_band": band}

    raise Q5EError(f"unknown figure kind {kind!r}")   # pragma: no cover


def _matplotlib_backend(path: str, spec: Mapping[str, object],
                        tables: Mapping[str, Sequence[Mapping[str, object]]],
                        data: Mapping[str, object]
                        ) -> None:                          # pragma: no cover
    """Default renderer.  ASCII labels only; no glyph can go missing.

    One branch per registered figure: the panel layout follows the figure's
    own meaning rather than a shared fallback.
    """
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    kind = str(spec.get("kind"))
    panels = list(spec.get("panels") or ("main",))
    figure, axes = plt.subplots(1, len(panels),
                                figsize=(4.2 * len(panels), 4.0),
                                squeeze=False)
    row = axes[0]

    if kind == FIG_CLASS_REASON:
        for index, side in enumerate(SIDES):
            panel = dict(dict(data["panels"])[side])
            categories = list(panel["categories"])
            bottom = [0.0] * len(categories)
            stacks = dict(panel["stacks"])
            reasons = sorted({r for v in stacks.values() for r in v})
            for reason in reasons:
                heights = [float(dict(stacks[c]).get(reason, 0.0))
                           for c in categories]
                row[index].bar(range(len(categories)), heights, bottom=bottom,
                               label=reason)
                bottom = [b + h for b, h in zip(bottom, heights)]
            row[index].set_xticks(range(len(categories)))
            row[index].set_xticklabels(categories)
            row[index].set_title(f"{side} side")
            if reasons:
                row[index].legend(fontsize=6)
    elif kind == FIG_RECORD_CLASS_HEATMAP:
        records = list(data["rows"])
        columns = list(data["columns"])
        cells = dict(data["cells"])
        matrix = [[(dict(cells[r]).get(c) or 0.0) for c in columns]
                  for r in records]
        if matrix:
            image = row[0].imshow(matrix, aspect="auto", cmap="viridis")
            figure.colorbar(image, ax=row[0], label="failure rate")
        row[0].set_yticks(range(len(records)))
        row[0].set_yticklabels(records, fontsize=6)
        row[0].set_xticks(range(len(columns)))
        row[0].set_xticklabels(columns)
    elif kind == FIG_RECORD_208_RASTER:
        raster = list(data["raster"])
        row[0].bar([int(e["row"]) for e in raster],
                   [1.0 if e["failed"] else 0.0 for e in raster], width=1.0)
        row[0].set_title("record 208, decisional adjacency")
        sensitivity = dict(data["raw_ordinal_sensitivity"])
        for adjacency in sorted(sensitivity):
            entry = dict(sensitivity[adjacency])
            keys = sorted(entry)
            row[1].plot(range(len(keys)), [entry[k] for k in keys],
                        marker="o", label=adjacency)
            row[1].set_xticks(range(len(keys)))
            row[1].set_xticklabels(keys, rotation=45, ha="right", fontsize=6)
        row[1].set_title("raw-ordinal sensitivity (non-decisional)")
        if sensitivity:
            row[1].legend(fontsize=6)
    elif kind == FIG_RUN_LENGTH_HIST:
        buckets = dict(data["buckets"])
        keys = list(buckets)
        row[0].bar(range(len(keys)), [buckets[k] for k in keys])
        row[0].set_xticks(range(len(keys)))
        row[0].set_xticklabels(keys, rotation=45, ha="right", fontsize=7)
        summary = dict(data["summary"])
        row[1].axis("off")
        row[1].text(0.02, 0.95, "\n".join(
            f"{k}: {v}" for k, v in sorted(summary.items())),
            va="top", family="monospace", fontsize=8)
        row[1].set_title("summary")
    elif kind == FIG_DISTANCE_HIST:
        bins = list(data["bins"])
        counts = dict(data["counts"])
        row[0].bar(range(len(bins)), [counts[b] for b in bins])
        row[0].set_xticks(range(len(bins)))
        row[0].set_xticklabels(bins, rotation=45, ha="right", fontsize=7)
        descriptive = dict(data["descriptive_exclusions"])
        keys = sorted(descriptive)
        row[1].bar(range(len(keys)), [descriptive[k] for k in keys])
        row[1].set_xticks(range(len(keys)))
        row[1].set_xticklabels(keys, rotation=45, ha="right", fontsize=6)
        row[1].set_title("descriptive exclusions")
    elif kind == FIG_DEGREE_VIOLIN_ECDF:
        panel_data = dict(data["panels"])
        for index, side in enumerate(SIDES):
            panel = dict(panel_data[side])
            violin = dict(panel["violin"])
            groups = list(violin)
            series = [list(violin[g]) or [0.0] for g in groups]
            if series:
                row[0].violinplot(series, positions=range(len(series)),
                                  showmedians=True)
            for group in groups:
                points = list(dict(panel["ecdf"])[group])
                row[1].plot([p[0] for p in points], [p[1] for p in points],
                            label=f"{side}/{group}")
            row[0].set_title(f"{SIDES[0]} vs {SIDES[1]} degree")
            row[1].set_title("ECDF")
            del index
        labels = [f"{s}: {dict(panel_data[s])['label']}" for s in SIDES]
        row[0].set_xlabel(" | ".join(labels), fontsize=6)
        row[1].legend(fontsize=5)
    elif kind == FIG_ANCHOR_CURVE:
        offsets = list(data["offsets"])
        row[0].plot(offsets, list(data["curve"]), marker="o")
        row[0].set_title("failure share by offset")
        band = dict(data["control_c_band"])
        names = sorted(band)
        row[1].bar(range(len(names)),
                   [float(dict(band[n]).get("q99") or 0.0) for n in names])
        row[1].set_xticks(range(len(names)))
        row[1].set_xticklabels(names)
        row[1].set_title("Control C q99 band")

    row[0].set_xlabel(str(spec["xlabel"]))
    row[0].set_ylabel(str(spec["ylabel"]))
    figure.suptitle(str(spec["title"]))
    figure.tight_layout()
    figure.savefig(path, dpi=110)
    plt.close(figure)


def assert_bundle_inputs_complete(result: Mapping[str, object],
                                  tables: Mapping[str, Sequence[Mapping[
                                      str, object]]]) -> List[str]:
    """Check the bundle can be completed **before** anything is created.

    Discovering a missing table after `os.makedirs` has already run leaves a
    half-written directory behind that reads like a run.  So the required
    output list and the tables backing it are validated first, and the
    filesystem is not touched until they agree.
    """
    m4_ok = str((result.get("m4") or {}).get("status")) == M4_OK
    needed = required_outputs(str(result.get("decision") or ""), m4_ok)
    missing = [name for name in needed
               if name in CSV_SCHEMAS and tables.get(name) is None]
    if missing:
        raise Q5EError(
            f"refusing to start a bundle: {missing} are required for decision "
            f"{result.get('decision')!r} (M4 ok={m4_ok}) but no table was "
            f"produced for them.  Nothing has been created on disk.")
    unexpected = [name for name in tables
                  if name in CSV_SCHEMAS and name not in needed]
    if unexpected:
        raise Q5EError(
            f"refusing to start a bundle: {unexpected} were produced but are "
            f"not registered outputs for this branch.  Nothing has been "
            f"created on disk.")
    return needed


def write_bundle(directory: str, result: Mapping[str, object],
                 config: Mapping[str, object], manifest: Mapping[str, object],
                 tables: Mapping[str, Sequence[Mapping[str, object]]],
                 nulls: Mapping[str, object], log_lines: Sequence[str],
                 summary: str, figures: Optional[bool] = None,
                 figure_backend=None,
                 require_complete: bool = False) -> Dict[str, object]:
    """Write one new bundle **atomically**.  Nothing existing is touched.

    Everything is written and verified inside a sibling staging directory and
    only then renamed into place, so the final path either does not exist or
    holds a complete bundle.  A partially written run is the one artifact that
    could be mistaken for a finished one, and this makes that state
    unreachable.  A stopped run still publishes its bundle, so a STOP is as
    inspectable as a PASS.
    """
    if os.path.exists(directory) and os.listdir(directory):
        raise Q5EError(
            f"refusing to write into a non-empty directory {directory!r}: "
            f"a run bundle is new, never an overwrite")
    needed = assert_bundle_inputs_complete(result, tables)
    m4_ok = str((result.get("m4") or {}).get("status")) == M4_OK

    parent = os.path.dirname(os.path.abspath(directory)) or "."
    os.makedirs(parent, exist_ok=True)
    staging = os.path.join(
        parent, f".{os.path.basename(os.path.abspath(directory))}.staging")
    if os.path.exists(staging):
        import shutil                                    # noqa: PLC0415
        shutil.rmtree(staging)
    os.makedirs(staging)
    try:
        written = _write_bundle_files(staging, result, config, manifest,
                                      tables, nulls, log_lines, summary,
                                      figures, figure_backend, m4_ok)
        if require_complete:
            missing = [name for name in needed
                       if not os.path.exists(os.path.join(staging, name))]
            if missing:
                raise Q5EError(
                    f"incomplete bundle: {missing} were required for decision "
                    f"{result.get('decision')!r} (M4 ok={m4_ok}) but were not "
                    f"written.  A bundle is complete or it is not published "
                    f"at all; the only registered absences are the M4-only "
                    f"artefacts when M4 stops.")
        if os.path.isdir(directory):
            os.rmdir(directory)            # empty by the check above
        os.rename(staging, directory)      # the publish step, atomic
    except BaseException:
        import shutil                                    # noqa: PLC0415
        shutil.rmtree(staging, ignore_errors=True)
        raise
    return {"directory": directory, "written": sorted(set(written)),
            "required": needed, "published": True}


def _write_bundle_files(directory: str, result, config, manifest, tables,
                        nulls, log_lines, summary, figures, figure_backend,
                        m4_ok: bool) -> List[str]:
    """Write every bundle file into ``directory``.  Used only for staging."""
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
    if result.get("synthetic_fixture"):
        # Machine-readable, in the bundle itself: an ingester never has to
        # parse prose to know this is not a registered result.
        with open(os.path.join(directory, SYNTHETIC_MARKER), "w",
                  encoding="utf-8") as fh:
            json.dump({"synthetic_fixture": True, "ingestable": False,
                       "qa_target_set": result.get("qa_target_set"),
                       "reason": SYNTHETIC_NOTE}, fh, indent=1, sort_keys=True)
        written.append(SYNTHETIC_MARKER)
    if figures is not None:
        written.extend(render_figures(directory, tables, m4_ok,
                                      backend=figure_backend, nulls=nulls))
    return written


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
         "xlabel": "class", "ylabel": "count",
         "kind": FIG_CLASS_REASON, "panels": ("mamba", "cache")},
        {"file": FIGURES[1], "title": "Per-record class failure rate",
         "xlabel": "class", "ylabel": "record",
         "kind": FIG_RECORD_CLASS_HEATMAP, "panels": ("heatmap",)},
        {"file": FIGURES[2], "title": "Record 208 failure raster",
         "xlabel": "mamba_record_row", "ylabel": "row state",
         "kind": FIG_RECORD_208_RASTER,
         "panels": ("raster", "raw_ordinal_sensitivity")},
        {"file": FIGURES[3], "title": "Run length distribution",
         "xlabel": "run length bucket", "ylabel": "count",
         "kind": FIG_RUN_LENGTH_HIST, "panels": ("histogram", "summary")},
        {"file": FIGURES[4], "title": "Nearest distance histogram",
         "xlabel": "d_inf bin (samples)", "ylabel": "count",
         "kind": FIG_DISTANCE_HIST,
         "panels": ("fixed_bin_histogram", "censor_and_endpoint")},
        {"file": FIGURES[5], "title": "Candidate degree by group and side",
         "xlabel": "group", "ylabel": "candidate degree",
         "kind": FIG_DEGREE_VIOLIN_ECDF, "panels": ("violin", "ecdf")},
    ]
    if m4_ok:
        specs.append({"file": FIGURE_M4_ONLY,
                      "title": "Anchor aligned failure probability",
                      "xlabel": "beat offset from anchor",
                      "ylabel": "failure share",
                      "kind": FIG_ANCHOR_CURVE,
                      "panels": ("curve", "control_c_band")})
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
                 "m4_anchors", "m4_source_match_oracle", "source_files")

    def __init__(self, rows, decision, manifest, processed_classes,
                 mamba_by_record, cache_by_record, cache_n,
                 m4_runtime=None, m4_sources=None, m4_texts=None,
                 m4_identity=None, m4_registered_counts=None,
                 m4_frozen_rr=None, m4_replay=None, m4_anchors=None,
                 m4_source_match_oracle=None, source_files=()):
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
        # The differential-PREP record.  Production leaves it None, so the
        # equivalence sub-gate stops M4 before the detector runs.
        self.m4_source_match_oracle = m4_source_match_oracle
        # Either a mapping or a zero-argument builder.  Production passes a
        # builder, because the anchors do not exist until the replay has run.
        self.m4_anchors = (m4_anchors if callable(m4_anchors)
                           else dict(m4_anchors or {}))
        self.source_files = list(source_files)

    def resolve_anchors(self) -> Dict[str, List[Dict[str, object]]]:
        """The anchors, built now if they are still a builder.

        Called only after M4.0 has passed, so a builder that refuses until the
        replay ran is exactly the intended behaviour.
        """
        value = self.m4_anchors
        return dict(value() if callable(value) else value)


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
    return BJ.load_cache_classes(cache_dir, SPLIT, approval=frozen_module_approval(
        approval, "canonical DS1 processed-class map"))


def load_sequences(mamba_path: str, cache_dir: str, approval: Optional[str],
                   mitdb_dir: str = "") -> Tuple[Dict[str, object],
                                                 Dict[str, object]]:
    """The frozen mamba and cache sequences for DS1.

    When ``mitdb_dir`` is given, the frozen Leg 1 replay is attached to the
    mamba rows so each carries its raw `.atr` ordinal and R sample.  M4.1
    places anchors against those samples, so without the attach the anchors
    would have nothing to be placed on — and inferring a position from a row
    count is exactly what the spec forbids.
    """
    require_execution_approval(approval, "frozen mamba and cache sequences")
    bj = frozen_module_approval(approval, "frozen mamba and cache sequences")
    mamba = BJ.load_mamba_sequences(mamba_path, approval=bj)
    cache = BJ.load_cache_sequences(cache_dir, approval=bj)
    ds1 = [row.record for row in BJ.build_ledger()[SPLIT]]
    mamba_by_record = {r: mamba["sequences"][r] for r in ds1}
    if mitdb_dir:
        leg1 = BJ.replay_leg1_split(mitdb_dir, SPLIT, approval=bj)
        mamba_by_record = {r: BJ.attach_leg1_identity(mamba_by_record[r],
                                                      leg1[r])
                           for r in ds1}
    return mamba_by_record, {r: cache["sequences"][r] for r in ds1}


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
DISCOVERED_PATH_KEYS: Tuple[str, ...] = (
    "bundle_dir", "mamba_path", "cache_dir", "v10_source_dir", "mitdb_dir")

#: The MIT-BIH publisher tree aggregate, as a **full** 64-hex digest.
#:
#: The spec recorded it only truncated (`0b46a411…`), and a truncated digest is
#: not an execution contract: it cannot be recomputed from, and must not be
#: guessed at or reconstructed.  The full value below was **measured** by the
#: separately approved read-only PREP P1 leg — 147/147 against the publisher
#: list plus the separately registered digest of the list itself — observed
#: identically by the `20260812T123035` and `20260814T104835` runs, and
#: registered here on 2026-08-14 together with the spec.
#: Derived from :data:`APPROVED_INPUT_IDENTITY`, never restated beside it.
MITDB_TREE_AGGREGATE: Optional[str] = (
    APPROVED_INPUT_IDENTITY["mitdb_tree_aggregate"])
INPUT_IDENTITY_REGISTRATION_REQUIRED = "INPUT_IDENTITY_REGISTRATION_REQUIRED"
#: `SHA256SUMS.txt` cannot appear in its own list, so the frozen verifier skips
#: it and covers the other 146 files.  Its own digest is registered separately
#: (`research/ASSETS.md :: data-mitdb-raw-100`), and the two together — 146
#: publisher-listed plus the list itself — are what "147/147" means.
MITDB_CHECKSUM_FILE_SHA256 = (
    "b61158a96d5f2ca80edfb354a9a66a6324836c390a84e1966dcee2b907d6be43")
MITDB_PUBLISHER_LISTED_FILES = 146

#: Per-file SHA-256 of the five canonical Q5-D bundle files Q5-E actually
#: reads.  Verifying only that the files exist and that `manifest.json` names
#: the right producing code leaves the contents unpinned: a bundle whose CSVs
#: were edited but whose `code_sha256` string was preserved would still be
#: accepted as canonical.
#:
#: **Registered 2026-08-14.**  Measured by the P2 leg of the
#: `20260814T104835` PREP run against Drive folder id
#: :data:`SOURCE_BUNDLE_FOLDER_ID`, read by folder id rather than by name, with
#: every ambiguity category zero and provider SHA-256 agreeing on all twelve
#: children.  These five files — not the other seven — are the scientific input
#: identity of Q5-E, and the fold over exactly these five is what
#: :func:`subset_file_fold` recomputes at run time.
#: Derived from :data:`APPROVED_INPUT_IDENTITY`, never restated beside it.
SOURCE_BUNDLE_FILE_SHA256: Dict[str, str] = dict(
    APPROVED_INPUT_IDENTITY["source_bundle_file_sha256"])
SOURCE_BUNDLE_DIGEST_FREEZE_REQUIRED = "SOURCE_BUNDLE_DIGEST_FREEZE_REQUIRED"

# ─────────────────────────────────────────────────────────────────────────────
# The registration is atomic across four categories.
#
# A bundle identified by one run's folder id and another run's digests is
# identified by neither, and a MIT-BIH aggregate registered beside an
# unregistered bundle would let half a preflight open the audit.  So the four
# values move together or not at all, and the check below is what makes that a
# property of the code rather than of whoever wrote the PR.
#
# It is deliberately not a *science* gate: it compares registration state
# against registration state, never an observation against a threshold.  The
# audit/lineage digests the same acceptance produced — the five-file subset
# fold, the twelve-file full fold, the PREP payload fold and the PREP manifest
# freeze — are recorded in `research/ASSETS.md` and the execution contract's
# Decision log, and deliberately do **not** appear here: none of them is a
# Q5-E runtime constant and none may become one.
# ─────────────────────────────────────────────────────────────────────────────
INPUT_IDENTITY_REGISTRATION_PARTIAL = "INPUT_IDENTITY_REGISTRATION_PARTIAL"
#: A value that is neither the approved one nor the recorded historical one.
#: Distinct from `PARTIAL` on purpose: a mixture of two known states and a
#: value nobody ever approved are different failures and want different words.
INPUT_IDENTITY_UNAPPROVED_VALUE = "INPUT_IDENTITY_UNAPPROVED_VALUE"
#: The four things the registration PR moves, in the order the contract lists
#: them.  Naming them makes "all four or none" checkable instead of asserted.
REGISTRATION_CATEGORIES: Tuple[str, ...] = (
    "mitdb_tree_aggregate", "source_bundle_folder_id", "source_bundle_run",
    "source_bundle_file_sha256")


def current_input_identity() -> Dict[str, object]:
    """The four registration constants as they stand right now."""
    return {
        "mitdb_tree_aggregate": MITDB_TREE_AGGREGATE,
        "source_bundle_folder_id": SOURCE_BUNDLE_FOLDER_ID,
        "source_bundle_run": SOURCE_BUNDLE_RUN,
        "source_bundle_file_sha256": dict(SOURCE_BUNDLE_FILE_SHA256),
    }


def input_identity_registration() -> Dict[str, object]:
    """Is the input identity **exactly** one of the two states that exist?

    Exactly two states are accepted, and each by exact match against a recorded
    record: :data:`APPROVED_INPUT_IDENTITY` — what Codex accepted on
    2026-08-14 — and :data:`UNREGISTERED_INPUT_IDENTITY`, this module before
    that PR.  Anything else stops.

    The first version of this function asked a weaker question: it treated a
    category as registered when it merely *differed* from the pre-registration
    value, with well-formedness reduced to a non-empty string.  Under that rule
    `SOURCE_BUNDLE_FOLDER_ID = "wrong-folder"` and an arbitrary but
    syntactically valid 64-hex aggregate were reported as a complete, atomic,
    well-formed registration.  A check that accepts every value except one is
    not an identity check, and the tests missed it because they only ever
    reverted values to the historical ones.

    Three summary facts come back: `registered` (all four match the approved
    record), `unregistered` (all four match the historical one) and `atomic`
    (one of those two holds).  A mixture of the two known states is
    `INPUT_IDENTITY_REGISTRATION_PARTIAL`; a value belonging to neither is
    `INPUT_IDENTITY_UNAPPROVED_VALUE`, which takes precedence because it is the
    more specific failure.
    """
    current = current_input_identity()
    categories: Dict[str, Dict[str, object]] = {}
    for name in REGISTRATION_CATEGORIES:
        value = current[name]
        matches_approved = value == APPROVED_INPUT_IDENTITY[name]
        matches_historical = value == UNREGISTERED_INPUT_IDENTITY[name]
        categories[name] = {
            "registered": matches_approved,
            "unregistered": matches_historical,
            "known": matches_approved or matches_historical,
            "value": sorted(value) if isinstance(value, dict) else value,
        }
    approved = sorted(n for n in REGISTRATION_CATEGORIES
                      if categories[n]["registered"])
    historical = sorted(n for n in REGISTRATION_CATEGORIES
                        if categories[n]["unregistered"])
    unknown = sorted(n for n in REGISTRATION_CATEGORIES
                     if not categories[n]["known"])

    problems: List[str] = []
    reason: Optional[str] = None
    if unknown:
        reason = INPUT_IDENTITY_UNAPPROVED_VALUE
        problems.append(
            f"{INPUT_IDENTITY_UNAPPROVED_VALUE}: {unknown} hold values that "
            f"are neither the approved registration nor the recorded "
            f"pre-registration state.  An input identity is not 'anything but "
            f"the old value'; it is the value the acceptance names, and "
            f"nothing else is registered by being different.")
    elif approved and historical:
        reason = INPUT_IDENTITY_REGISTRATION_PARTIAL
        problems.append(
            f"{INPUT_IDENTITY_REGISTRATION_PARTIAL}: registered {approved} but "
            f"not {historical}.  A bundle identified by one run's folder id "
            f"and another run's digests is identified by neither, so the four "
            f"categories move together or not at all.")
    # Reported for diagnostics; the exact-match comparison above is what
    # decides, so a well-formed-but-wrong map can no longer pass here.
    digests = registered_bundle_digests_complete()
    return {"categories": categories,
            "categories_order": list(REGISTRATION_CATEGORIES),
            "registered": not historical and not unknown,
            "unregistered": not approved and not unknown,
            "atomic": not problems,
            "registered_categories": approved,
            "unregistered_categories": historical,
            "unapproved_categories": unknown,
            "digest_registration": digests,
            "ok": not problems,
            "reason": reason,
            "problems": problems}


def assert_registration_is_atomic() -> Dict[str, object]:
    """Stop on a half-moved or unapproved registration.

    Callers invoke this **before** reading anything: a static registration
    error is decidable from the module alone, so hashing a registered artifact
    first would be work done in support of a conclusion that cannot be reached,
    and would open assets on behalf of a registration nobody approved.
    """
    state = input_identity_registration()
    if not state["ok"]:
        raise DiagnosticInputMismatch(
            f"{state['reason']}: {'; '.join(str(p) for p in state['problems'])}")
    return state


def _candidate_dirs(root: str, max_depth: int = DISCOVERY_MAX_DEPTH):
    """Directories under ``root``, breadth-limited so a mount cannot hang it."""
    root = os.path.abspath(root)
    base = root.rstrip(os.sep).count(os.sep)
    for current, subdirs, _files in os.walk(root):
        if current.rstrip(os.sep).count(os.sep) - base >= max_depth:
            subdirs[:] = []
        subdirs[:] = [d for d in sorted(subdirs) if not d.startswith(".")]
        yield current



def subset_file_fold(directory: str, names: Sequence[str],
                     approval: Optional[str]) -> Dict[str, object]:
    """Fold a **subset** of a directory without calling the rest unexpected.

    `BJ.hash_file_set` answers "is this directory exactly this file set?", and
    that is the right question for the bundle *as a whole*.  It is the wrong
    question for the five files Q5-E reads: a real Q5-D run bundle carries all
    twelve registered files, so asking for the five reports the other seven as
    unexpected and rejects a perfectly canonical bundle.

    So the two contracts are separated.  This computes the identity of just
    the named files, using the same `(name, bytes, sha256)` canonical-JSON
    fold as `hash_file_set` — the convention is reused, not reinvented — and
    nothing is copied, moved or excluded from the directory to do it.
    """
    require_execution_approval(approval, f"file subset in {directory!r}")
    files: List[Dict[str, object]] = []
    missing: List[str] = []
    for name in sorted(set(names)):
        path = os.path.join(directory, name)
        if not os.path.isfile(path):
            missing.append(name)
            continue
        files.append({"name": name, "bytes": os.path.getsize(path),
                      "sha256": sha256_file(path)})
    aggregate = hashlib.sha256(_canonical_json(
        [[f["name"], f["bytes"], f["sha256"]] for f in files]
    ).encode("utf-8")).hexdigest()
    return {"directory": directory, "files": files, "missing": missing,
            "aggregate": aggregate, "n_files": len(files),
            "ok": not missing,
            "problems": ([] if not missing
                         else [f"{directory}: missing {missing}"])}


#: Where each producing-identity field actually lives in a manifest the frozen
#: Q5-D module wrote.  Recorded rather than inferred, and reported beside the
#: values, so a reader can see which field a digest came from.
MANIFEST_IDENTITY_SOURCES: Dict[str, str] = {
    "code_sha256": "manifest['code']['sha256'] (nested, from "
                   "assert_implementation_only())",
    "rule_fingerprint": "manifest['rule_fingerprint'] (top level)",
}
MANIFEST_SCHEMA_MISMATCH = "MANIFEST_SCHEMA_MISMATCH"


def manifest_producing_identity(manifest: Mapping[str, object]
                                ) -> Tuple[Dict[str, object], List[str]]:
    """Read the producing identity from where the producer actually writes it.

    `BJ.build_manifest()` records the module digest **nested**, at
    ``manifest['code']['sha256']`` — `code` is the mapping
    `assert_implementation_only()` returns — and the rule fingerprint at the
    top level.  This gate previously read a flat ``manifest['code_sha256']``,
    which no producer has ever written: against a real bundle it resolved to
    `""` and the directory contract failed for a reason that had nothing to do
    with the bundle.  The registration would then have been recorded as
    complete while every canonical bundle was rejected at discovery.

    The same defect was found and fixed in the PREP module on 2026-08-14 (D7);
    it survived here because this suite's fixture was a hand-written flat dict,
    authored from the same belief as the code, so the tests could confirm the
    belief and never test it.  The fixture is now built by `BJ.build_manifest()`
    itself.

    Both fields are matched **exactly**.  There is no flat-field fallback and
    no raw/LF alternative: accepting a second spelling would let the schema
    this function exists to pin drift again, and returning one digest while the
    artifact carries another would hand the caller an identity it does not
    have.

    Malformed, missing, null and wrongly typed fields come back as `problems`
    and are never raised.  Nothing here calls into the frozen module, so there
    is no exception to catch and no way for an unrelated `RuntimeError` to be
    relabelled as a manifest defect.
    """
    problems: List[str] = []
    observed: Dict[str, object] = {
        "code_sha256": "", "rule_fingerprint": "",
        "read_from": dict(MANIFEST_IDENTITY_SOURCES),
    }

    code = manifest.get("code")
    if not isinstance(code, Mapping):
        problems.append(
            f"manifest code: {type(code).__name__}, not the mapping the "
            f"producer writes under manifest['code'].  The module digest lives "
            f"at manifest['code']['sha256']; a flat manifest['code_sha256'] is "
            f"not this schema and is not accepted as one.")
    else:
        code_sha = code.get("sha256")
        if not isinstance(code_sha, str) or not _is_sha256(code_sha):
            problems.append(
                f"manifest code.sha256: {code_sha!r} is not a lowercase "
                f"64-hex string")
        else:
            observed["code_sha256"] = code_sha
            if code_sha != PRODUCING_CODE_SHA256:
                problems.append(
                    f"manifest code.sha256 {code_sha!r} != "
                    f"{PRODUCING_CODE_SHA256!r}")

    fingerprint = manifest.get("rule_fingerprint")
    if not isinstance(fingerprint, str) or not _is_sha256(fingerprint):
        problems.append(
            f"manifest rule_fingerprint: {fingerprint!r} is not a lowercase "
            f"64-hex string at the manifest's top level")
    else:
        observed["rule_fingerprint"] = fingerprint
        if fingerprint != REGISTERED_RULE_FINGERPRINT:
            problems.append(
                f"manifest rule_fingerprint {fingerprint!r} != "
                f"{REGISTERED_RULE_FINGERPRINT!r}")
    return observed, problems


def verify_bundle_directory_contract(directory: str, approval: Optional[str]
                                     ) -> Dict[str, object]:
    """The **whole** Q5-D run bundle is complete and unmodified in shape.

    All twelve registered files present, nothing unexpected beside them, no
    `SUPERSEDED.json`, and `manifest.json` naming both the registered
    producing code and the registered rule fingerprint.  This is the directory
    contract; the scientific input identity of the five files Q5-E reads is a
    separate check (:func:`verify_bundle_content_identity`).
    """
    require_execution_approval(approval, f"bundle directory {directory!r}")
    problems: List[str] = []
    if os.path.exists(os.path.join(directory, SUPERSEDED_MARKER)):
        problems.append(
            f"{SUPERSEDED_MARKER} present: this is a superseded bundle")
    full = BJ.hash_file_set(directory, BJ.BUNDLE_FILES, approval=_bj(approval))
    problems.extend(full.get("problems", ()))
    identity: Dict[str, object] = {"code_sha256": "", "rule_fingerprint": "",
                                   "read_from": dict(MANIFEST_IDENTITY_SOURCES)}
    manifest_path = os.path.join(directory, "manifest.json")
    if not os.path.exists(manifest_path):
        problems.append("manifest.json is absent")
    else:
        try:
            with open(manifest_path, encoding="utf-8") as handle:
                manifest = json.load(handle)
        except (OSError, ValueError) as error:
            problems.append(f"manifest.json is unreadable: {error}")
        else:
            if not isinstance(manifest, Mapping):
                problems.append(
                    f"manifest.json holds a {type(manifest).__name__}, not an "
                    f"object")
            else:
                identity, manifest_problems = manifest_producing_identity(
                    manifest)
                problems.extend(manifest_problems)
    return {"gate": "bundle_directory", "ok": not problems,
            "reason": None if not problems else DECISION_MISMATCH,
            "directory": directory, "n_files": full.get("n_files"),
            "missing": list(full.get("missing", ())),
            "unexpected": list(full.get("extra", ())),
            "full_aggregate": full.get("aggregate"),
            "code_sha256": identity["code_sha256"],
            "rule_fingerprint": identity["rule_fingerprint"],
            "manifest_identity": identity,
            "problems": problems}


#: How to describe several accepted copies, per asset.  The distinction is not
#: cosmetic: `byte_identical_duplicates` is only true when the digest that
#: matched covers *every* byte compared.  For the Q5-D bundle the digest is the
#: five-file subset fold, so two copies can share it while differing in, say,
#: `log.txt` — calling those byte-identical would be a false audit record.
DUPLICATE_LABEL_FULL_BYTES = "byte_identical_duplicates"
DUPLICATE_LABEL_INPUT_SUBSET = "q5e_input_identical_copies"


#: The PREP bundle file that *records* the payload fold.  It is excluded from
#: the fold it records, because a manifest containing its own digest is a
#: circular contract that can never be satisfied.
PREP_MANIFEST_FILE = "manifest.json"
#: Files folded into `prep_payload_sha256`, by name.  Fixed rather than
#: globbed so "what was hashed" is answerable without the directory.
PREP_PAYLOAD_FILES: Tuple[str, ...] = (
    "config.json", "source_inventory.json", "oracle_harness_identity.json",
    "fixture_results.json", "decision.json", "log.txt", "summary.md")


def prep_payload_fold(files: Sequence[Mapping[str, object]]) -> Dict[str, object]:
    """Fold a PREP bundle's payload, excluding the manifest that records it.

    The self-reference this removes is real: if `manifest.json` carried a
    digest computed over a set that included `manifest.json`, writing the
    digest would change the file and invalidate the digest.  So the payload
    fold covers :data:`PREP_PAYLOAD_FILES` only, the manifest records it, and
    the manifest's *own* SHA-256 is frozen outside the bundle — in the
    Decision log and the registration record — where nothing it contains can
    change it.

    ``files`` is `(name, bytes, sha256)` triples; the same input always yields
    the same digest, using the same canonical convention as everywhere else.
    """
    payload = sorted(
        (dict(f) for f in files if str(f.get("name")) in PREP_PAYLOAD_FILES),
        key=lambda f: str(f["name"]))
    excluded = sorted({str(f.get("name")) for f in files}
                      - {str(f["name"]) for f in payload})
    if PREP_MANIFEST_FILE in {str(f["name"]) for f in payload}:
        raise Q5EError(
            f"{PREP_MANIFEST_FILE} cannot be part of the payload fold it "
            f"records; that contract is circular by construction")
    missing = [n for n in PREP_PAYLOAD_FILES
               if n not in {str(f["name"]) for f in payload}]
    digest = hashlib.sha256(_canonical_json(
        [[f["name"], f["bytes"], f["sha256"]] for f in payload]
    ).encode("utf-8")).hexdigest()
    return {"prep_payload_sha256": digest,
            "included": [str(f["name"]) for f in payload],
            "excluded": excluded, "missing": missing,
            "manifest_file": PREP_MANIFEST_FILE,
            "manifest_digest_frozen_externally": True,
            "complete": not missing}


def registered_bundle_digests_complete() -> Dict[str, object]:
    """Is `SOURCE_BUNDLE_FILE_SHA256` a complete, well-formed registration?

    A half-filled map is not a registration: it would silently verify some
    inputs and skip others.  The key set must be exactly the five files Q5-E
    reads — no missing key, no extra key — and every value a lowercase 64-hex
    digest.
    """
    registered = dict(SOURCE_BUNDLE_FILE_SHA256)
    if not registered:
        return {"registered": False, "complete": False,
                "reason": SOURCE_BUNDLE_DIGEST_FREEZE_REQUIRED, "problems": []}
    problems: List[str] = []
    expected = set(BUNDLE_INPUT_FILES)
    observed = set(registered)
    if observed - expected:
        problems.append(f"unregistered keys: {sorted(observed - expected)}")
    if expected - observed:
        problems.append(f"missing keys: {sorted(expected - observed)}")
    for name, value in sorted(registered.items()):
        if not _is_sha256(value):
            problems.append(f"{name}: not a lowercase 64-hex SHA-256")
    return {"registered": True, "complete": not problems,
            "reason": None if not problems
            else SOURCE_BUNDLE_DIGEST_FREEZE_REQUIRED,
            "problems": problems}


def resolve_identical_candidates(matches: Sequence[Mapping[str, object]],
                                 what: str, root: str,
                                 duplicate_label: str =
                                 DUPLICATE_LABEL_FULL_BYTES
                                 ) -> Dict[str, object]:
    """Choose one of several **byte-identical** copies, deterministically.

    Byte-identical duplicates are not a scientific ambiguity — being identical
    to the canonical asset is what verification means, and Drive already holds
    duplicates of `mamba_data.npz`.  Demanding they be deleted would both stall
    discovery and conflict with the standing rule that no Drive file is moved
    or removed.  So: zero matches fail; several copies of the *same* digest
    resolve to the lexicographically first path and record the rest; and
    candidates whose digests *differ* are never merged into one identity.

    This mirrors `BJ.resolve_canonical_mamba`, which settled the same question
    for Q5-D.
    """
    if not matches:
        raise DiagnosticInputMismatch(
            f"{DECISION_MISMATCH}: no {what} with the registered identity was "
            f"found under {root!r}.  The audit does not fall back to a "
            f"path-named guess: mount the registered artifact and re-run.")
    digests = {str(m["digest"]) for m in matches}
    if len(digests) > 1:
        raise DiagnosticInputMismatch(
            f"{DECISION_MISMATCH}: {len(digests)} different digests under "
            f"{root!r} were each accepted as the {what} "
            f"({sorted(d[:12] for d in digests)}).  Copies whose compared "
            f"digests differ are not one identity and are never merged.")
    ordered = sorted(matches, key=lambda m: str(m["path"]))
    chosen = ordered[0]
    others = [str(m["path"]) for m in ordered[1:]]
    out: Dict[str, object] = {
        "path": str(chosen["path"]),
        "digest": str(chosen["digest"]),
        "duplicate_label": duplicate_label,
        duplicate_label: others,
        "n_candidates": len(ordered),
        "candidates": [dict(m) for m in ordered],
    }
    if duplicate_label != DUPLICATE_LABEL_FULL_BYTES:
        out["note"] = (
            "these copies share the compared digest, which covers only part "
            "of the directory; they are NOT asserted to be byte-identical "
            "overall")
    return out


def verify_mitdb_identity(directory: str, approval: Optional[str]
                          ) -> Dict[str, object]:
    """MIT-BIH identity: publisher checksums **and** the registered aggregate.

    The publisher list proves the bytes are the published bytes; the registered
    aggregate proves this is the tree the experiment froze.  They answer
    different questions, so both are required — and while the full aggregate is
    unregistered this reports the open item rather than passing on the
    checksums alone.
    """
    require_execution_approval(approval, f"MIT-BIH tree at {directory!r}")
    # Registration state is decided from the module alone, so it is checked
    # here — after approval, before a single file is hashed.  Reading 147 files
    # to then report a static registration error would open registered assets
    # on behalf of a registration nobody approved.
    registration = input_identity_registration()
    if not registration["ok"]:
        return {"gate": "mitdb_identity", "ok": False,
                "reason": registration["reason"],
                "observed_aggregate": None,
                "registered_aggregate": MITDB_TREE_AGGREGATE,
                "registration": registration,
                "publisher_checksums": {}, "integrity": {},
                "files_read": 0,
                "problems": list(registration["problems"])}
    # `mitdb_expected_files()` already contains SHA256SUMS.txt, so it is passed
    # exactly as-is.  Appending the checksum file again would be a false
    # statement of the contract even where set semantics hide the effect.
    names = BJ.mitdb_expected_files()
    file_set = BJ.hash_file_set(directory, names, approval=_bj(approval))
    published = BJ.verify_against_publisher_checksums(file_set, directory)
    problems = list(file_set.get("problems", ()))
    problems.extend(published.get("problems", ()))
    if not published.get("available"):
        problems.append(
            f"{BJ.MITDB_CHECKSUM_FILE} is absent: the publisher list is the "
            f"independent check and its absence is not a pass")

    # Published-tree integrity has two parts, because a checksum file cannot
    # verify itself and the frozen verifier explicitly skips it:
    #   1. the files the publisher list covers, and
    #   2. the digest of SHA256SUMS.txt itself, registered separately.
    # Together they are 147/147.  Neither alone is.
    checksum_digest = ""
    checksum_path = os.path.join(directory, BJ.MITDB_CHECKSUM_FILE)
    if os.path.isfile(checksum_path):
        checksum_digest = sha256_file(checksum_path)
    checksum_ok = checksum_digest == MITDB_CHECKSUM_FILE_SHA256
    if not checksum_ok:
        problems.append(
            f"{BJ.MITDB_CHECKSUM_FILE} sha256 {checksum_digest!r} != "
            f"registered {MITDB_CHECKSUM_FILE_SHA256!r}; the publisher list "
            f"itself is not the registered one, so nothing it verifies counts")
    listed = {"checked": published.get("checked"),
              "matched": published.get("matched"),
              "expected_checked": MITDB_PUBLISHER_LISTED_FILES}
    if published.get("available") and \
            published.get("checked") != MITDB_PUBLISHER_LISTED_FILES:
        problems.append(
            f"the publisher list covered {published.get('checked')} files, "
            f"registered {MITDB_PUBLISHER_LISTED_FILES} "
            f"({BJ.MITDB_CHECKSUM_FILE} cannot verify itself)")
    integrity = {
        "publisher_listed": listed,
        "checksum_file": {"observed": checksum_digest,
                          "registered": MITDB_CHECKSUM_FILE_SHA256,
                          "ok": checksum_ok},
        "n_expected_files": len(names),
        "published_tree_integrity_ok": bool(
            checksum_ok and published.get("available")
            and not published.get("problems")
            and published.get("checked") == MITDB_PUBLISHER_LISTED_FILES),
    }

    observed = str(file_set.get("aggregate") or "")
    base = {"gate": "mitdb_identity", "observed_aggregate": observed,
            "publisher_checksums": published, "integrity": integrity,
            "registration": registration, "files_read": len(names)}
    if MITDB_TREE_AGGREGATE is None:
        return {**base, "ok": False,
                "reason": INPUT_IDENTITY_REGISTRATION_REQUIRED,
                "registered_aggregate": None,
                "problems": problems + [
                    "the MIT-BIH tree aggregate is registered only in "
                    "truncated form; a truncated digest is not an execution "
                    "contract and this implementation does not reconstruct or "
                    "guess the full value"]}
    if observed != MITDB_TREE_AGGREGATE:
        problems.append(
            f"aggregate {observed!r} != registered {MITDB_TREE_AGGREGATE!r}")
    return {**base, "ok": not problems,
            "reason": None if not problems else DECISION_MISMATCH,
            "registered_aggregate": MITDB_TREE_AGGREGATE,
            "problems": problems}


def verify_bundle_content_identity(directory: str, approval: Optional[str]
                                   ) -> Dict[str, object]:
    """Per-file content identity of the five files Q5-E reads.

    The companion check, :func:`verify_bundle_directory_contract`, establishes
    that the whole twelve-file run bundle is present and that `manifest.json`
    names the registered producing code and rule fingerprint.  Neither of
    those pins the *contents* of the inputs: editing `join_map.parquet` while
    leaving the `code_sha256` string alone would still satisfy the directory
    contract, and "the QA counts match" is not an identity check either.  This
    is the one authoritative check of those five files' bytes, and it stops
    when their digests have never been frozen.
    """
    require_execution_approval(approval, f"bundle contents at {directory!r}")
    # Before the fold, for the same reason as in `verify_mitdb_identity`: a
    # static registration error needs no bytes to decide, and folding the five
    # files first would open them for a registration that is not accepted.
    registration = input_identity_registration()
    if not registration["ok"]:
        return {"gate": "bundle_content_identity", "ok": False,
                "reason": registration["reason"],
                "observed": {}, "registered": dict(SOURCE_BUNDLE_FILE_SHA256),
                "subset_fold": None, "registration": registration,
                "problems": list(registration["problems"])}
    subset = subset_file_fold(directory, BUNDLE_INPUT_FILES, approval)
    observed = {f["name"]: f["sha256"] for f in subset["files"]}
    if not SOURCE_BUNDLE_FILE_SHA256:
        return {"gate": "bundle_content_identity", "ok": False,
                "reason": SOURCE_BUNDLE_DIGEST_FREEZE_REQUIRED,
                "observed": observed, "registered": {},
                "subset_fold": subset["aggregate"],
                "problems": [
                    "no per-file SHA-256 is registered for the canonical "
                    "Q5-D bundle, so its contents cannot be verified.  The "
                    "digests must be frozen by a separately approved "
                    "read-only PREP and recorded in the spec and here "
                    "together; they are not invented, and matching QA counts "
                    "is not a substitute."]}
    problems = []
    for name in BUNDLE_INPUT_FILES:
        want = SOURCE_BUNDLE_FILE_SHA256.get(name)
        got = observed.get(name)
        if want is None:
            problems.append(f"{name}: no registered digest")
        elif got is None:
            problems.append(f"{name}: absent")
        elif got != want:
            problems.append(f"{name}: sha256 {got!r} != registered {want!r}")
    return {"gate": "bundle_content_identity", "ok": not problems,
            "reason": None if not problems else DECISION_MISMATCH,
            "observed": observed,
            "registered": dict(SOURCE_BUNDLE_FILE_SHA256),
            "subset_fold": subset["aggregate"],
            "problems": problems}


def discover_registered_inputs(search_root: str, approval: Optional[str]
                               ) -> Dict[str, object]:
    """Locate every registered input under one mount, **by digest**.

    Nothing is matched on a folder name, so a renamed copy is still found and
    a look-alike is still refused; the V9 cache can never stand in for the V10
    one because only the registered V10 aggregate matches.  Several
    byte-identical copies of the same asset are resolved deterministically and
    audited rather than treated as an ambiguity — Drive already holds
    duplicates, and no Drive file is deleted or moved to satisfy this.

    The returned mapping carries the observed digests, but it is a *record*,
    not a credential: :func:`run_audit` re-verifies every input from bytes
    before it runs.
    """
    require_execution_approval(approval, f"input discovery under {search_root!r}")
    # Before the walk: an unapproved or half-moved registration is decidable
    # without touching the mount, and discovery is the widest reader here.
    assert_registration_is_atomic()
    found: Dict[str, object] = {}
    audit: Dict[str, object] = {}

    bundles: List[Dict[str, object]] = []
    for directory in _candidate_dirs(search_root):
        # A candidate must look like a whole Q5-D run bundle, so the presence
        # test is over the frozen twelve-file contract — not over the five
        # files Q5-E happens to read.
        if not all(os.path.exists(os.path.join(directory, name))
                   for name in BJ.BUNDLE_FILES):
            continue
        contract = verify_bundle_directory_contract(directory, approval)
        if not contract["ok"]:
            continue
        # Identity is the fold over the five files Q5-E reads, computed as a
        # subset so the other seven registered files are not "unexpected".
        subset = subset_file_fold(directory, BUNDLE_INPUT_FILES, approval)
        if not subset["ok"]:
            continue
        registration = registered_bundle_digests_complete()
        if registration["registered"]:
            if not registration["complete"]:
                raise DiagnosticInputMismatch(
                    f"{SOURCE_BUNDLE_DIGEST_FREEZE_REQUIRED}: the registered "
                    f"bundle digests are incomplete or malformed "
                    f"({registration['problems']}).  A partial registration "
                    f"would verify some inputs and silently skip others.")
            observed = {f["name"]: f["sha256"] for f in subset["files"]}
            if any(observed.get(name) != want for name, want
                   in SOURCE_BUNDLE_FILE_SHA256.items()):
                continue          # P2 registered: contents must match exactly
        bundles.append({
            "path": directory,
            # The identity used for matching is the five-file subset fold.
            "digest": str(subset.get("aggregate") or ""),
            "subset_fold": str(subset.get("aggregate") or ""),
            # Recorded beside it so a reader can see that two accepted copies
            # may still differ in the seven files Q5-E does not read.
            "full_aggregate": str(contract.get("full_aggregate") or "")})
    resolved = resolve_identical_candidates(
        bundles, "canonical bundle", search_root,
        duplicate_label=DUPLICATE_LABEL_INPUT_SUBSET)
    resolved["canonical_provenance"] = {
        "registered_run": SOURCE_BUNDLE_RUN,
        "registered_folder_id": SOURCE_BUNDLE_FOLDER_ID,
        # P2 read that folder id directly on 2026-08-14 and the five per-file
        # digests below came from it, so the bridge between "this folder id"
        # and "these bytes" is established rather than pending.
        "folder_id_bridge": "P2_SOURCE_BUNDLE_IDENTITY_PASS",
        "folder_id_bridge_run":
            "20260814T104835_EXP-2026-008_q5e_prep_p1_p2_asset_identity",
        "provenance": dict(SOURCE_BUNDLE_PROVENANCE),
        "note": ("the registered run and folder id are the canonical "
                 "provenance; the path below is the mounted copy that was "
                 "selected, and the link between them is the registered "
                 "per-file digests, which P2 measured at that folder id"),
        "selected_mount_path": resolved["path"]}
    found["bundle_dir"] = resolved["path"]
    audit["bundle_dir"] = resolved

    mamba: List[Dict[str, object]] = []
    for directory in _candidate_dirs(search_root):
        path = os.path.join(directory, "mamba_data.npz")
        if os.path.isfile(path) and sha256_file(path) == BJ.MAMBA_SHA256:
            mamba.append({"path": path, "digest": BJ.MAMBA_SHA256})
    resolved = resolve_identical_candidates(mamba, "mamba_data.npz",
                                            search_root)
    found["mamba_path"] = resolved["path"]
    audit["mamba_path"] = resolved

    cache_names = BJ.cache_expected_files()
    cache_want = str(M4_INPUT_CONTRACT["v10_cache"]["aggregate"])
    caches: List[Dict[str, object]] = []
    for directory in _candidate_dirs(search_root):
        if not os.path.isfile(os.path.join(directory, cache_names[0])):
            continue
        digest = BJ.hash_file_set(directory, cache_names, approval=_bj(approval))
        # `ok` as well as the aggregate: a directory can fold to the registered
        # aggregate over the expected set and still carry an unexpected file,
        # which is a contract problem rather than a match.
        if digest.get("ok") and digest.get("aggregate") == cache_want:
            caches.append({"path": directory, "digest": cache_want})
    resolved = resolve_identical_candidates(caches, "V10 preprocessing cache",
                                            search_root)
    found["cache_dir"] = resolved["path"]
    audit["cache_dir"] = resolved

    # The full registered expected set and aggregate, not just the two
    # decisive files: `frontend.py` is byte-identical in V9 and V10, so
    # matching on it alone would accept the V9 source folder.
    source_want = str(M4_INPUT_CONTRACT["v10_source"]["aggregate"])
    sources: List[Dict[str, object]] = []
    for directory in _candidate_dirs(search_root):
        if not os.path.isfile(os.path.join(directory, "frontend.py")):
            continue
        digest = BJ.hash_file_set(directory, M4_V10_SOURCE_FILES,
                                  approval=_bj(approval))
        if digest.get("ok") and digest.get("aggregate") == source_want:
            sources.append({"path": directory, "digest": source_want})
    resolved = resolve_identical_candidates(sources, "V10 source package",
                                            search_root)
    found["v10_source_dir"] = resolved["path"]
    audit["v10_source_dir"] = resolved

    # The MIT-BIH tree is a real M4 input: the detector replay reads its
    # signals and its `.atr` annotations.
    trees: List[Dict[str, object]] = []
    for directory in _candidate_dirs(search_root):
        names = BJ.mitdb_expected_files()
        if not all(os.path.isfile(os.path.join(directory, name))
                   for name in names):
            continue
        checked = verify_mitdb_identity(directory, approval)
        if checked["ok"]:
            trees.append({"path": directory,
                          "digest": str(checked["observed_aggregate"])})
        elif checked["reason"] == INPUT_IDENTITY_REGISTRATION_REQUIRED:
            raise DiagnosticInputMismatch(
                f"{INPUT_IDENTITY_REGISTRATION_REQUIRED}: a MIT-BIH tree was "
                f"found at {directory!r} and its publisher checksums were "
                f"read, but the registered tree aggregate exists only in "
                f"truncated form.  Register the full 64-hex digest through a "
                f"separately approved read-only PREP before running.")
    resolved = resolve_identical_candidates(
        trees, "MIT-BIH publisher tree verified against its own "
        f"{BJ.MITDB_CHECKSUM_FILE}", search_root)
    found["mitdb_dir"] = resolved["path"]
    audit["mitdb_dir"] = resolved

    found["discovery_audit"] = audit
    return found


def reverify_registered_inputs(paths: Mapping[str, object],
                               approval: Optional[str]) -> Dict[str, object]:
    """Re-verify every input **from its bytes**, immediately before the run.

    A stamp saying "these were verified" proves nothing: any caller can write
    the same string next to five paths of their choosing.  Provenance — which
    function produced the mapping — is not evidence either, because a mapping
    is just a dict.  So nothing is trusted here except digests recomputed now:

    * the canonical bundle: expected files present, no `SUPERSEDED.json`,
      `manifest.json` naming the registered producing code, **and** each of the
      five files matching its registered per-file digest;
    * `mamba_data.npz` against `BJ.MAMBA_SHA256`;
    * the V10 cache and V10 source against their registered aggregates, with
      `hash_file_set` problems treated as failures rather than ignored;
    * the MIT-BIH tree against the publisher checksum list and the registered
      tree aggregate.

    Any failure raises; there is no partial pass and no "verified earlier".
    """
    missing = [key for key in DISCOVERED_PATH_KEYS if not paths.get(key)]
    if missing:
        raise DiagnosticInputMismatch(
            f"{DECISION_MISMATCH}: the input set is missing {missing}")
    resolved = {key: str(paths[key]) for key in DISCOVERED_PATH_KEYS}
    require_execution_approval(
        approval, f"re-verification of {resolved['bundle_dir']!r}")
    assert_registration_is_atomic()

    checks: List[Dict[str, object]] = []

    # Exactly two authoritative bundle checks: the whole twelve-file directory
    # contract, then the five-file scientific input identity.  There is no
    # third, weaker "is it canonical" path — a second source of truth for the
    # same question is a place for the two answers to drift apart.
    checks.append(verify_bundle_directory_contract(resolved["bundle_dir"],
                                                   approval))
    content = verify_bundle_content_identity(resolved["bundle_dir"], approval)
    checks.append(content)

    observed_mamba = (sha256_file(resolved["mamba_path"])
                      if os.path.isfile(resolved["mamba_path"]) else "")
    checks.append({
        "gate": "mamba_identity",
        "ok": observed_mamba == BJ.MAMBA_SHA256,
        "observed": observed_mamba, "registered": BJ.MAMBA_SHA256,
        "problems": ([] if observed_mamba == BJ.MAMBA_SHA256 else
                     [f"{resolved['mamba_path']}: sha256 "
                      f"{observed_mamba!r} != registered"])})

    for key, names, want, label in (
            ("cache_dir", BJ.cache_expected_files(),
             str(M4_INPUT_CONTRACT["v10_cache"]["aggregate"]), "V10 cache"),
            ("v10_source_dir", M4_V10_SOURCE_FILES,
             str(M4_INPUT_CONTRACT["v10_source"]["aggregate"]),
             "V10 source")):
        digest = BJ.hash_file_set(resolved[key], names, approval=_bj(approval))
        problems = list(digest.get("problems", ()))
        if digest.get("aggregate") != want:
            problems.append(
                f"{label}: aggregate {digest.get('aggregate')!r} != "
                f"registered {want!r}")
        checks.append({"gate": f"{key}_identity", "ok": not problems,
                       "observed": digest.get("aggregate"),
                       "registered": want,
                       "missing": list(digest.get("missing", ())),
                       "unexpected": list(digest.get("extra", ())),
                       "problems": problems})

    checks.append(verify_mitdb_identity(resolved["mitdb_dir"], approval))

    failed = [c for c in checks if not c.get("ok")]
    if failed:
        reasons = [str(c.get("reason") or DECISION_MISMATCH) for c in failed]
        raise DiagnosticInputMismatch(
            f"{reasons[0]}: input re-verification failed immediately before "
            f"the run.  "
            + "; ".join(f"{c['gate']}: {list(c.get('problems') or [])[:2]}"
                        for c in failed))
    return {"paths": resolved, "checks": checks,
            # The provenance record is the five files that were actually
            # verified, taken from the content-identity check itself.
            "source_files": [dict(f) for f in
                             subset_file_fold(resolved["bundle_dir"],
                                              BUNDLE_INPUT_FILES,
                                              approval)["files"]],
            "bundle_subset_fold": content.get("subset_fold")}


# ─────────────────────────────────────────────────────────────────────────────
# Production M4.
#
# M4.0 condition 2 is not a version probe: it requires the registered runtime
# to stand, `detect_r()` to be re-run on all 22 DS1 records, every registered
# per-record cache count to be reproduced 22/22, and the frozen V10 `rr`
# arrays to be reproduced exactly.  M4.1 then needs the source's *own*
# annotation matching to place discordance anchors.  All of that is built here,
# so the execution-approval change has only to remove the terminal guard.
#
# Nothing in this section runs at import time, and every entry point is behind
# the approval check.  The replay is returned as a *callback* so
# `m4_feasibility_gate()` keeps its registered order: the detector cannot be
# called until runtime, source map and input identity have each passed.
# ─────────────────────────────────────────────────────────────────────────────
def load_frozen_rr(cache_by_record: Mapping[str, "BJ.RecordSequence"]
                   ) -> Dict[str, List[List[int]]]:
    """The frozen V10 RR arrays, in integer samples, per DS1 record.

    Taken from the already-loaded registered V10 cache rather than re-read, so
    the arrays compared in the `rr_equality` sub-gate are the same bytes the
    join consumed.  `[pre, post]` in `mamba_record_row`-independent cache row
    order, which is what `verify_rr_equality` compares element by element.
    """
    return {record: [list(seq.pre_samples), list(seq.post_samples)]
            for record, seq in sorted(cache_by_record.items())}


def load_v10_producer(v10_source_dir: str, approval: Optional[str]):
    """Import the registered V10 `frontend.py` as the detector producer.

    The digest of this exact file is verified by the `source_map` sub-gate
    *before* the replay callback is ever invoked, so this loads the file whose
    identity M4.0 condition 1 has already established — never an arbitrary
    `frontend.py` found on `sys.path`.
    """
    require_execution_approval(approval, f"V10 producer in {v10_source_dir!r}")
    import importlib.util                                # noqa: PLC0415
    path = os.path.join(v10_source_dir, "frontend.py")
    observed = sha256_file(path)
    want = M4_SOURCE_MAP_HASHES["frontend.py"]
    if observed != want:
        raise DiagnosticInputMismatch(
            f"{M4_SOURCE_MAP_UNVERIFIED}: frontend.py at {path!r} has sha256 "
            f"{observed!r}, registered {want!r}.  The producer is identified "
            f"by digest, never by path.")
    spec = importlib.util.spec_from_file_location(
        "q5e_frozen_v10_frontend", path)
    if spec is None or spec.loader is None:              # pragma: no cover
        raise Q5EError(f"cannot load the registered producer at {path!r}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    for name in ("detect_r", "rr_features"):
        if not hasattr(module, name):
            raise DiagnosticInputMismatch(
                f"{M4_SOURCE_MAP_UNVERIFIED}: the registered producer has no "
                f"{name}(); the static source map and the loaded module "
                f"disagree.")
    return module


#: The control-flow decisions this **candidate** adapter makes.  Each is a
#: place where a different reading of the prose "greedy nearest with a used
#: set" would produce a different answer, so they are named here as a
#: text-derived candidate contract: a reviewer compares decisions rather than
#: paragraphs, and the adapter fingerprint changes if any of them is edited.
#: None of this is evidence that the registered `data.py` makes the same
#: choices — that is what P3 exists to establish.
SOURCE_MATCH_CONTRACT: Dict[str, str] = {
    "traversal": "peaks in detector order; annotations in ascending sample "
                 "order, ties broken by their `.atr` ordinal",
    "distance_tie": "the smaller annotation sample wins; if two candidates "
                    "share a sample, the smaller `.atr` ordinal wins",
    "nearest_already_used": "the peak takes the next-nearest unused candidate "
                            "inside the tolerance; it is NOT dropped merely "
                            "because its nearest neighbour is taken",
    "used_added": "when the match is accepted, before the next peak is "
                  "considered",
    "used_vs_aami": "`used` is consumed during matching, BEFORE AAMI "
                    "selection; a non-AAMI annotation still consumes its match "
                    "and its peak is then dropped, not rematched",
    "used_vs_boundary": "`used` is consumed during matching, BEFORE the "
                        "boundary cut; a peak cut by `p-150`/`p+150` does not "
                        "release its annotation",
}
#: The registered file this candidate adapter is written *against*.  Pinned so
#: a reviewer can tell which bytes the contract above was read from.
SOURCE_MATCH_REGISTERED_FILE = "data.py"
SOURCE_MATCH_REGISTERED_FUNCTION = "build_record"
SOURCE_MATCH_EQUIVALENCE_REQUIRED = "SOURCE_MATCH_EQUIVALENCE_REQUIRED"
SOURCE_MATCH_ORACLE_PASS = "SOURCE_MATCH_EQUIVALENT_TO_REGISTERED_SOURCE"
#: Every field a differential PREP must record before the adapter may be used.
#: A bare verdict string is not enough: a PASS has to say *what* was compared,
#: so that changing either side invalidates it automatically.
SOURCE_MATCH_ORACLE_FIELDS: Tuple[str, ...] = (
    "verdict", "registered_file_sha256", "adapter_fingerprint",
    "prep_bundle_sha256", "oracle_harness_sha256", "fixtures",
    "fixtures_passed")
#: Fields of the record that must each be a lowercase 64-hex SHA-256.  A
#: non-empty string is not an identity; `"x"` must not open this gate.
SOURCE_MATCH_ORACLE_DIGEST_FIELDS: Tuple[str, ...] = (
    "registered_file_sha256", "adapter_fingerprint", "prep_bundle_sha256",
    "oracle_harness_sha256")
#: Every counterexample the differential PREP must cover, by the exact name
#: the corresponding regression test uses.  A PASS that omits one of these has
#: not tested the decision that fixture exists to pin, so it is not a PASS.
SOURCE_MATCH_REQUIRED_FIXTURES: Tuple[str, ...] = (
    "test_source_match_nearest_already_used_falls_through",
    "test_source_match_distance_tie_goes_to_the_earlier_annotation",
    "test_source_match_non_aami_symbol_consumes_its_match",
    "test_source_match_boundary_cut_consumes_its_match",
    "test_source_match_annotation_order_differing_from_sample_order",
    "test_source_match_peak_order_change_is_visible",
)


def _is_sha256(value: object) -> bool:
    """Exactly 64 lowercase hex characters.  Nothing else is a digest."""
    text = value if isinstance(value, str) else ""
    return (len(text) == 64
            and all(c in "0123456789abcdef" for c in text))
#: Filled only by a separately approved read-only PREP (P3).  While it is
#: `None` the equivalence sub-gate stops M4 **before the detector runs**.
SOURCE_MATCH_ORACLE_RECORD: Optional[Dict[str, object]] = None


def source_match_adapter_fingerprint() -> str:
    """Digest of this adapter's source plus its declared candidate contract.

    Editing the matching loop or any decision in `SOURCE_MATCH_CONTRACT`
    changes this value, so a differential PASS recorded against an older
    adapter cannot silently be reused for a newer one.
    """
    import inspect                                        # noqa: PLC0415
    body = inspect.getsource(match_peaks_to_annotations)
    payload = _canonical_json({"source": body,
                               "contract": SOURCE_MATCH_CONTRACT,
                               "tolerance": M4_PEAK_MATCH_TOLERANCE_SAMPLES,
                               "win_before": BJ.WIN_BEFORE,
                               "win_after": BJ.WIN_AFTER})
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def verify_source_match_equivalence(
        oracle: Optional[Mapping[str, object]] = None) -> Dict[str, object]:
    """M4.0 sub-gate: has this adapter been compared against the source?

    The annotation matching is the thing the replay's counts are produced
    *through*.  Running the detector before the adapter has been shown
    equivalent to the registered `data.py` yields numbers whose meaning
    depends on an unverified reimplementation, so this stops M4 **before**
    the detector callback is reached.

    A PASS is not a string.  It must name the registered `data.py` digest it
    was established against, the adapter fingerprint it tested, the PREP
    bundle that produced it, and the fixtures it compared — so that editing
    the adapter, or the registered file moving, invalidates it automatically
    rather than leaving a stale approval in place.
    """
    record = dict(oracle if oracle is not None
                  else (SOURCE_MATCH_ORACLE_RECORD or {}))
    fingerprint = source_match_adapter_fingerprint()
    registered = M4_SOURCE_MAP_HASHES[SOURCE_MATCH_REGISTERED_FILE]
    base = {"gate": "source_match_equivalence",
            "adapter_fingerprint": fingerprint,
            "registered_file": SOURCE_MATCH_REGISTERED_FILE,
            "registered_file_sha256": registered,
            "registered_function": SOURCE_MATCH_REGISTERED_FUNCTION,
            "contract": dict(SOURCE_MATCH_CONTRACT),
            "oracle": record}
    if not record:
        return {**base, "ok": False,
                "reason": SOURCE_MATCH_EQUIVALENCE_REQUIRED,
                "problems": [
                    "no differential comparison against the registered "
                    "`data.py` has been recorded.  The adapter is a "
                    "text-derived candidate and is unverified against the "
                    "registered source; reproducing the registered per-record "
                    "counts is a necessary condition, not a proof, and may "
                    "not be used to choose between candidate implementations."]}
    problems: List[str] = []
    missing = [f for f in SOURCE_MATCH_ORACLE_FIELDS if f not in record]
    if missing:
        problems.append(f"the oracle record is missing {missing}")
    if str(record.get("verdict") or "") != SOURCE_MATCH_ORACLE_PASS:
        problems.append(
            f"verdict {record.get('verdict')!r} is not "
            f"{SOURCE_MATCH_ORACLE_PASS!r}")
    # Every identity field must be a real digest.  A non-empty placeholder is
    # not an identity, and neither is an uppercase or truncated one.
    for field in SOURCE_MATCH_ORACLE_DIGEST_FIELDS:
        if not _is_sha256(record.get(field)):
            problems.append(
                f"{field} is not a lowercase 64-hex SHA-256: "
                f"{record.get(field)!r}")
    if str(record.get("registered_file_sha256") or "") != registered:
        problems.append(
            "the PREP was run against a different `data.py`; a PASS is not "
            "reused across a change of the registered source")
    if str(record.get("adapter_fingerprint") or "") != fingerprint:
        problems.append(
            "the adapter has changed since the PREP; the differential must be "
            "re-run against the current fingerprint")

    # Fixture results, not a list of names: each must say what the source
    # produced, what the adapter produced, and that the two agreed.
    entries = list(record.get("fixtures") or ())
    names: List[str] = []
    equal_count = 0
    for index, entry in enumerate(entries):
        if not isinstance(entry, Mapping):
            problems.append(f"fixture {index} is not a result record")
            continue
        name = str(entry.get("name") or "")
        if not name:
            problems.append(f"fixture {index} has no name")
            continue
        names.append(name)
        source_digest = entry.get("source_result_sha256")
        adapter_digest = entry.get("adapter_result_sha256")
        for field, value in (("source_result_sha256", source_digest),
                             ("adapter_result_sha256", adapter_digest)):
            if not _is_sha256(value):
                problems.append(
                    f"fixture {name!r}: {field} is not a 64-hex SHA-256")
        if entry.get("equal") is not True:
            problems.append(f"fixture {name!r} did not compare equal")
            continue
        if source_digest != adapter_digest:
            problems.append(
                f"fixture {name!r} is marked equal but the source and adapter "
                f"result digests differ")
            continue
        equal_count += 1
    duplicates = sorted({n for n in names if names.count(n) > 1})
    if duplicates:
        problems.append(f"duplicate fixture names: {duplicates}")
    absent = [n for n in SOURCE_MATCH_REQUIRED_FIXTURES if n not in names]
    if absent:
        problems.append(
            f"the differential omits required counterexamples: {absent}")
    try:
        passed = int(record.get("fixtures_passed"))
    except (TypeError, ValueError):
        passed = -1
    if not entries:
        problems.append("no oracle fixtures are listed")
    else:
        if passed != equal_count:
            problems.append(
                f"fixtures_passed is {passed} but {equal_count} fixtures "
                f"actually compared equal")
        if passed != len(entries):
            problems.append(
                f"{passed} of {len(entries)} oracle fixtures passed; a partial "
                f"differential is not a PASS")
    return {**base, "ok": not problems,
            "reason": None if not problems
            else SOURCE_MATCH_EQUIVALENCE_REQUIRED,
            "fixtures": names, "fixtures_passed": passed,
            "fixtures_equal": equal_count,
            "required_fixtures": list(SOURCE_MATCH_REQUIRED_FIXTURES),
            "problems": problems}


def source_match_equivalence_status(
        oracle: Optional[Mapping[str, object]] = None) -> Dict[str, object]:
    """Reporting view of the equivalence sub-gate, for the result bundle."""
    gate = verify_source_match_equivalence(oracle)
    return {
        "status": (SOURCE_MATCH_ORACLE_PASS if gate["ok"]
                   else SOURCE_MATCH_EQUIVALENCE_REQUIRED),
        "adapter_fingerprint": gate["adapter_fingerprint"],
        "registered_file": gate["registered_file"],
        "registered_file_sha256": gate["registered_file_sha256"],
        "registered_function": gate["registered_function"],
        "contract": gate["contract"],
        "problems": list(gate.get("problems", ())),
        "note": ("This adapter is a text-derived candidate and is unverified "
                 "against the registered `data.py` until a differential PREP "
                 "records a PASS.  Reproducing the registered per-record "
                 "counts is a necessary condition only."),
    }


def match_peaks_to_annotations(peaks: Sequence[int],
                               annotations: Sequence[Tuple[int, str]],
                               signal_length: int,
                               tolerance: int = M4_PEAK_MATCH_TOLERANCE_SAMPLES
                               ) -> Dict[str, object]:
    """**Candidate** source-matching adapter for `data.py :: build_record`.

    This is a *text-derived candidate contract*, **unverified against the
    registered `data.py`**.  EXP-2026-008 requires M4.1 to reproduce the
    source's own rule; this function does not yet establish that it does, and
    nothing here may be read as evidence that it does.  The equivalence
    sub-gate stops M4 before the detector runs until a differential PREP (P3)
    records a PASS.

    Every control-flow decision is fixed in :data:`SOURCE_MATCH_CONTRACT` and
    summarised here, because "greedy nearest with a `used` set" is prose that
    admits several inequivalent implementations:

    * peaks are traversed in detector order; annotations in ascending sample
      order, ties broken by `.atr` ordinal;
    * the nearest **unused** candidate within the tolerance wins, so a peak
      whose nearest annotation is already taken falls through to the
      next-nearest rather than being dropped;
    * distance ties go to the smaller sample, then the smaller ordinal;
    * `used` is updated at the moment a match is accepted, and therefore
      **before** both AAMI selection and the boundary cut — a peak later
      dropped by either does not release its annotation back into the pool.

    The tolerance, the greediness, the `used` set and the cut are all read
    from the registered source map rather than chosen here: no detector,
    second tolerance or manual anchor is introduced.  Whether these decisions
    match the registered implementation is exactly what remains unverified.
    Returns the kept cache rows in detector order plus the two discordance
    anchor kinds M4.1 defines.
    """
    order = sorted(range(len(annotations)),
                   key=lambda k: (int(annotations[k][0]), k))
    positions = [int(annotations[k][0]) for k in order]
    used: set = set()
    matched_annotation: Dict[int, int] = {}      # peak index -> annotation idx
    for index, peak in enumerate(peaks):
        peak = int(peak)
        best = None
        best_distance = tolerance + 1
        # Nearest *unused* candidate.  `rank` ascends with sample then ordinal,
        # and the comparison is strict, so a tie keeps the earlier one.
        for rank, pos in enumerate(positions):
            if rank in used:
                continue
            distance = abs(pos - peak)
            if distance < best_distance:
                best, best_distance = rank, distance
        if best is not None and best_distance <= tolerance:
            used.add(best)                 # consumed here: before AAMI and cut
            matched_annotation[index] = order[best]

    kept_rows: List[Dict[str, object]] = []
    peaks_without_annotation: List[Dict[str, object]] = []
    for index, peak in enumerate(peaks):
        peak = int(peak)
        annotation_index = matched_annotation.get(index)
        if annotation_index is None:
            peaks_without_annotation.append(
                {"anchor_kind": "peak_without_annotation",
                 "anchor_ordinal": index, "anchor_sample": peak})
            continue
        symbol = str(annotations[annotation_index][1])
        aami = BJ.AAMI_SYMBOL_MAP.get(symbol, "")
        if not aami:
            continue          # AAMI selection; the annotation stays consumed
        if not (peak - BJ.WIN_BEFORE >= 0 and
                peak + BJ.WIN_AFTER <= int(signal_length)):
            continue          # boundary cut; the annotation stays consumed
        kept_rows.append({"peak_index": index, "r_sample": peak,
                          "raw_atr_ordinal": annotation_index,
                          "symbol": symbol, "aami": aami})

    unmatched = set(range(len(annotations))) - {
        order[rank] for rank in used}
    annotations_without_peak = [
        {"anchor_kind": "annotation_without_peak",
         "anchor_ordinal": index,
         "anchor_sample": int(annotations[index][0])}
        for index in sorted(unmatched)]
    return {"kept_rows": kept_rows,
            "annotations_without_peak": annotations_without_peak,
            "peaks_without_annotation": peaks_without_annotation,
            "tolerance": int(tolerance)}


class DetectorReplay(object):
    """M4.0 condition 2 as a callback, plus the detail M4.1 needs afterwards.

    Two things come out of one detector pass — the counts/RR the feasibility
    gate compares, and the per-record annotation matching the anchors are
    placed from.  Keeping them on one object makes the dependency explicit:
    the anchors cannot be built before the replay has actually run, and
    :meth:`anchors_by_record` says so rather than silently returning nothing.
    """

    __slots__ = ("v10_source_dir", "mitdb_dir", "records", "approval",
                 "producer", "atr_reader", "signal_reader", "detail", "ran")

    def __init__(self, v10_source_dir: str, mitdb_dir: str,
                 records: Sequence[str], approval: Optional[str],
                 producer=None, atr_reader=None, signal_reader=None) -> None:
        self.v10_source_dir = v10_source_dir
        self.mitdb_dir = mitdb_dir
        self.records = sorted(records)
        self.approval = approval
        self.producer = producer
        self.atr_reader = atr_reader
        self.signal_reader = signal_reader
        self.detail: Dict[str, Dict[str, object]] = {}
        self.ran = False

    def _raw(self, record: str) -> Dict[str, object]:
        if self.atr_reader:
            return self.atr_reader(record)
        return BJ.load_atr_record(self.mitdb_dir, record,
                                  _bj(self.approval))

    def __call__(self) -> Tuple[Dict[str, int], Dict[str, List[List[int]]]]:
        """Re-run the registered detector on all 22 DS1 records."""
        module = self.producer or load_v10_producer(self.v10_source_dir,
                                                    self.approval)
        counts: Dict[str, int] = {}
        replayed: Dict[str, List[List[int]]] = {}
        for record in self.records:
            raw = self._raw(record)
            signal = (self.signal_reader(record) if self.signal_reader
                      else _read_signal(self.mitdb_dir, record, self.approval))
            peaks = [int(p) for p in module.detect_r(signal)]
            match = match_peaks_to_annotations(
                peaks, raw["annotations"], int(raw["signal_length"]))
            self.detail[record] = match
            kept = match["kept_rows"]
            counts[record] = len(kept)
            features = module.rr_features([row["r_sample"] for row in kept])
            pre, post = _rr_columns(features, expected_rows=len(kept))
            replayed[record] = [
                list(BJ.rr_to_samples(pre, BJ.CACHE_RR_UNIT)),
                list(BJ.rr_to_samples(post, BJ.CACHE_RR_UNIT))]
        self.ran = True
        return counts, replayed

    def anchors_by_record(self, mamba_by_record: Mapping[str, object]
                          ) -> Dict[str, List[Dict[str, object]]]:
        """M4.1 anchors from the matching this replay actually produced."""
        if not self.ran:
            raise Q5EError(
                "M4.1 anchors were requested before the M4.0 detector replay "
                "ran; no anchor may be computed before the gate passes")
        return build_m4_anchors(self.mitdb_dir, self.records, mamba_by_record,
                                self.approval, replay_detail=self.detail)


def build_detector_replay(v10_source_dir: str, mitdb_dir: str,
                          records: Sequence[str], approval: Optional[str],
                          producer=None, atr_reader=None, signal_reader=None
                          ) -> "DetectorReplay":
    """The M4.0 condition 2 replay callback.

    ``producer``, ``atr_reader`` and ``signal_reader`` are injection points for
    the synthetic tests.  Production passes none of them and therefore loads
    the digest-verified registered producer and reads the registered tree.
    """
    require_execution_approval(approval, f"detector replay over {mitdb_dir!r}")
    return DetectorReplay(v10_source_dir, mitdb_dir, records, approval,
                          producer=producer, atr_reader=atr_reader,
                          signal_reader=signal_reader)


def _read_signal(mitdb_dir: str, record: str, approval: Optional[str]):
    """One record's signal, for the detector.  No label is read."""
    require_execution_approval(approval, f"signal for record {record!r}")
    import wfdb                                          # noqa: PLC0415
    signal, _fields = wfdb.rdsamp(os.path.join(mitdb_dir, str(record)))
    return signal


def _rr_columns(features, expected_rows: Optional[int] = None
                ) -> Tuple[List[float], List[float]]:
    """`pre`/`post` from a replayed `rr_features()` of **exactly** `(n, 7)`.

    The registered cache stores `(n, 7)` with `pre` at column 0 and `post` at
    column 1.  Anything else is a contract failure and is refused: no reshape,
    no pad, no truncation, no column guessing.  Checking only the first row's
    width was not enough — a ragged result would pass that and then either
    raise `IndexError` deep in the caller or silently select a wrong column.
    """
    if isinstance(features, (str, bytes)):
        raise ReplayContractError(
            f"{M4_RR_MISMATCH}: rr_features() returned {type(features).__name__}, "
            f"not a two-dimensional array of rows")
    try:
        rows = [list(row) for row in features]
    except TypeError:
        raise ReplayContractError(
            f"{M4_RR_MISMATCH}: rr_features() did not return an iterable of "
            f"rows; the replay is not reshaped to fit")
    for index, row in enumerate(rows):
        if isinstance(row, (str, bytes)) or not hasattr(row, "__len__"):
            raise ReplayContractError(
                f"{M4_RR_MISMATCH}: rr_features() row {index} is not a "
                f"sequence; the result is not two-dimensional")
    widths = {len(row) for row in rows}
    if len(widths) > 1:
        raise ReplayContractError(
            f"{M4_RR_MISMATCH}: rr_features() returned ragged rows with widths "
            f"{sorted(widths)}; registered width is {BJ.CACHE_RR_DIM} for every "
            f"row.  The audit does not pad or truncate a replay to fit.")
    if widths and widths != {BJ.CACHE_RR_DIM}:
        raise ReplayContractError(
            f"{M4_RR_MISMATCH}: the replayed rr_features() produced width "
            f"{widths.pop()}, registered {BJ.CACHE_RR_DIM}.  The audit does "
            f"not reshape, pad or select columns to make a replay fit.")
    if expected_rows is not None and len(rows) != int(expected_rows):
        raise ReplayContractError(
            f"{M4_RR_MISMATCH}: rr_features() returned {len(rows)} rows for "
            f"{expected_rows} kept peaks.  A row-count mismatch is a failed "
            f"replay, not something to align.")
    return ([float(row[BJ.CACHE_PRE_COLUMN]) for row in rows],
            [float(row[BJ.CACHE_POST_COLUMN]) for row in rows])


def build_m4_anchors(mitdb_dir: str, records: Sequence[str],
                     mamba_by_record: Mapping[str, "BJ.RecordSequence"],
                     approval: Optional[str], replay_detail=None,
                     atr_reader=None) -> Dict[str, List[Dict[str, object]]]:
    """M4.1 anchors, placed at their unique sample-ordered boundary.

    An exact kept annotation is offset 0.  Otherwise the anchor sits between
    kept rows and is placed at the first kept row strictly after it; an anchor
    with no unique placement is reported with `mapped_mamba_record_row = None`
    and is excluded from the numerator rather than imputed.
    """
    require_execution_approval(approval, f"M4.1 anchors over {mitdb_dir!r}")
    detail = dict(replay_detail or {})
    out: Dict[str, List[Dict[str, object]]] = {}
    for record in sorted(records):
        mamba = mamba_by_record[record]
        kept_samples = [int(row.get("raw_r_sample"))
                        for row in mamba.rows
                        if row.get("raw_r_sample") is not None]
        if len(kept_samples) != len(mamba):
            raise DiagnosticInputMismatch(
                f"{DECISION_MISMATCH}: record {record} carries "
                f"{len(kept_samples)} raw R samples for {len(mamba)} kept "
                f"mamba rows.  Anchor placement needs the Leg 1 identity on "
                f"every row; it is never inferred from a row count.")
        exact = {sample: index for index, sample in enumerate(kept_samples)}
        match = detail.get(record)
        if match is None:
            raise Q5EError(
                f"no detector-replay detail for record {record}; M4.1 anchors "
                f"are placed from the replay's own matching and are never "
                f"recomputed under a second rule")
        anchors: List[Dict[str, object]] = []
        for anchor in (list(match.get("annotations_without_peak", ())) +
                       list(match.get("peaks_without_annotation", ()))):
            sample = int(anchor["anchor_sample"])
            placement: Optional[int] = exact.get(sample)
            counterpart_kept = placement is not None
            if placement is None:
                after = [i for i, s in enumerate(kept_samples) if s > sample]
                placement = after[0] if after else None
            anchors.append({**anchor,
                            "record": record,
                            "mapped_mamba_record_row": placement,
                            "counterpart_kept": bool(counterpart_kept)})
        out[record] = anchors
    return out


def observed_m4_identity(v10_source_dir: str, cache_dir: str,
                         approval: Optional[str]) -> Dict[str, str]:
    """Aggregate digests of what is **actually mounted**, freshly computed.

    `verify_m4_input_identity` compares these against the registered
    constants.  Substituting the constants here — which an earlier revision
    did — turns that comparison into a tautology, so the aggregates are
    recomputed from the bytes on disk every time and never carried over.
    """
    require_execution_approval(approval, "M4 input identity")
    source_names = tuple(sorted(M4_V10_SOURCE_FILES))
    source = BJ.hash_file_set(v10_source_dir, source_names,
                              approval=_bj(approval))
    cache = BJ.hash_file_set(cache_dir, BJ.cache_expected_files(),
                             approval=_bj(approval))
    return {"v10_source": str(source.get("aggregate") or ""),
            "v10_cache": str(cache.get("aggregate") or ""),
            "v10_source_problems": list(source.get("problems", ())),
            "v10_cache_problems": list(cache.get("problems", ()))}


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
    mamba, cache = load_sequences(mamba_path, cache_dir, approval,
                                  mitdb_dir=mitdb_dir)
    hashes, texts = load_m4_source_map(v10_source_dir, approval)
    records = sorted(mamba)
    # M4.0 condition 2 is fully constructed here.  `replay` is a callback, so
    # the detector still cannot run before the gate's three pre-replay
    # sub-gates pass; `m4_anchors` is the same object's anchor builder, so
    # M4.1 can only draw on a replay that actually happened.
    replay = build_detector_replay(v10_source_dir, mitdb_dir, records,
                                   approval)
    return ProductionInputs(
        rows=rows, decision=decision, manifest=manifest,
        processed_classes=processed, mamba_by_record=mamba,
        cache_by_record=cache, cache_n={r: len(cache[r]) for r in records},
        m4_runtime=observed_runtime(), m4_sources=hashes, m4_texts=texts,
        # Observed, not registered.  Passing the registered constant here
        # would make the identity sub-gate compare it against itself and pass
        # unconditionally, which is the opposite of verifying identity.
        m4_identity=observed_m4_identity(v10_source_dir, cache_dir, approval),
        m4_registered_counts={r: BJ.ledger_record(SPLIT, r).cache_n
                              for r in records},
        m4_frozen_rr=load_frozen_rr(cache),
        m4_replay=replay,
        m4_anchors=lambda: replay.anchors_by_record(mamba),
        # Explicitly the module-level record: production never injects a PASS.
        m4_source_match_oracle=SOURCE_MATCH_ORACLE_RECORD,
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
        rr_verdict=PREP_M4_RR_EQUIVALENCE_VERDICT, replay=inputs.m4_replay,
        source_match_oracle=inputs.m4_source_match_oracle)
    m4_ok = str(m4["status"]) == M4_OK
    anchors_by_record = inputs.resolve_anchors() if m4_ok else {}
    anchors = (m4_anchors(m4, anchors_by_record, rows) if m4_ok else None)

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
                            for r, v in anchors_by_record.items()}

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
    long_run_share = m0["runs_primary_mamba_row"]["share_in_long_runs"]
    gate_bins = m1["bins_in_distance_gate"]
    # M5 applied to the hypothesis statistics themselves, not only to the M0
    # failure counts.  Each hypothesis reports the strata *it* materialised.
    strata = hypothesis_strata(distances=distances, gate_rows=gate_rows,
                               m3_rows=m3["rows"], partition=partition,
                               anchors=anchors, rows=rows, m4_ok=m4_ok)
    evidence = {
        "H1": {"strata": strata["H1"],
               "strata_reported": materialised_strata(strata["H1"]),
               "effect_gates": {
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
        "H4": {"strata": strata["H4"],
               "strata_reported": materialised_strata(strata["H4"]),
               "effect_gates": h4["effect_gates"]},
    }
    if m4_ok:
        evidence["H2"] = {
            "strata": strata["H2"],
            "strata_reported": materialised_strata(strata["H2"]),
            "effect_gates": {
                "explains_at_least_half": bool(
                    h2["statistic"] >= EFFECT_SHARE_MIN),
                "exceeds_control_c_q99": bool(
                    h2["statistic"] > h2["null_summary"]["q99"])}}
        evidence["H3"] = {
            "strata": strata["H3"],
            "strata_reported": materialised_strata(strata["H3"]),
            "effect_gates": {
                "exceeds_control_c_q99": bool(
                    h3["statistic"] > h3["null_summary"]["q99"]),
                "half_in_long_runs": bool(long_run_share >= EFFECT_SHARE_MIN),
                "distance_mass_far": bool(
                    sum(gate_bins[b] for b in M1_H3_FAR_BINS)
                    > gate_bins[M1_GATE_BIN])}}

    flags = evaluate_flags(evidence, holm)
    decision = decide(qa["ok"], str(m4["status"]), flags,
                      qa.get("first_failure"),
                      m4_first_failure=m4.get("first_failure"))
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


def hypothesis_strata(distances: Sequence[Mapping[str, object]],
                      gate_rows: Sequence[Mapping[str, object]],
                      m3_rows: Sequence[Mapping[str, object]],
                      partition: Sequence[Mapping[str, object]],
                      anchors: Optional[Mapping[str, object]],
                      rows: Sequence[Mapping[str, object]],
                      m4_ok: bool) -> Dict[str, Dict[str, object]]:
    """M5 applied to H1-H4, each with the population that hypothesis measures.

    The registered strata are the same for all four, but the *unit* differs —
    H1 strata over distance rows, H4 over cache-side graph rows, H2/H3 over
    mamba failure positions — so each is stratified over its own items rather
    than over one shared table that would not answer for any of them.
    """
    out: Dict[str, Dict[str, object]] = {}

    # H1 — distance concentration, over the rows inside the distance gate.
    h1_items = [{"record": e["record"], "class": e["processed_class"],
                 "reason": e["reason"], "bin": e["bin"]} for e in gate_rows]
    out["H1"] = stratified_statistic(
        h1_items,
        lambda subset: _ratio(sum(1 for e in subset
                                  if str(e["bin"]) == M1_GATE_BIN),
                              len(subset)))

    # H4 — the cache-side degree contrast, over the decisional graph rows.
    class_of = {(str(e["record"]), int(e["cache_record_row"])): str(e["class"])
                for e in partition}
    h4_items = [{"record": str(r["record"]),
                 "class": class_of.get((str(r["record"]), int(r["row"])), ""),
                 "reason": {v: k for k, v in REASON_TO_GROUP.items()}.get(
                     str(r["group"]), ""),
                 "group": str(r["group"]),
                 "candidate_degree": float(r["candidate_degree"])}
                for r in m3_rows if str(r["side"]) == H4_DECISIONAL_SIDE]
    out["H4"] = stratified_statistic(
        h4_items,
        lambda subset: _degree_median_contrast(
            [{"record": e["record"], "side": H4_DECISIONAL_SIDE,
              "group": e["group"], "candidate_degree": e["candidate_degree"]}
             for e in subset], H4_DECISIONAL_SIDE),
        minimum=2)

    # H2 / H3 — only when M4.0 passed; otherwise the family is UNEVALUABLE and
    # a stratified table for it would be an invitation to read it anyway.
    if m4_ok and anchors is not None:
        explained = {tuple(x) for x in anchors["explained_positions"]}
        after: set = set()
        for entry in anchors["rows"]:
            base = int(entry["mapped_mamba_record_row"])
            for offset in range(1, M4_ANCHOR_HALF_WINDOW + 1):
                after.add((str(entry["record"]), base + offset))
        failures = [{"record": str(r["record"]),
                     "class": str(r.get("mamba_aami") or ""),
                     "reason": str(r["drop_or_unmatched_reason"]),
                     "position": int(r["mamba_record_row"])}
                    for r in rows if is_mamba_side(r) and is_failed(r)]
        no_edge = [e for e in failures
                   if e["reason"] == BJ.REASON_NO_EDGE]
        out["H2"] = stratified_statistic(
            no_edge,
            lambda subset: _ratio(
                sum(1 for e in subset
                    if (e["record"], e["position"]) in explained),
                len(subset)))
        out["H3"] = stratified_statistic(
            failures,
            lambda subset: _ratio(
                sum(1 for e in subset
                    if (e["record"], e["position"]) in after),
                len(subset)))
    else:
        absent = {name: {"levels": {}, "materialised": False,
                         "status": NOT_APPLICABLE}
                  for name in M5_STRATA}
        out["H2"] = dict(absent)
        out["H3"] = dict(absent)
    return out


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
    return run_audit(paths, out_dir, approval=approval,
                     open_registered_data=open_registered_data, emit=emit)


def run_audit(verified_inputs: Mapping[str, object], out_dir: str,
              approval: Optional[str] = None,
              open_registered_data: bool = OPEN_REGISTERED_DATA,
              emit=print) -> Dict[str, object]:
    """The single production route to a Q5-E decision.

    Every input is re-verified **from its bytes** here, immediately before the
    run.  Nothing is taken on the word of an earlier step: not a stamp, not
    which function produced the mapping, not a check performed a moment ago.
    Refuses immediately without a separate execution approval; permission is
    checked before capability, so an unauthorised call is refused as
    unauthorised whatever the environment happens to have installed.
    """
    if not open_registered_data:
        raise ExecutionNotApprovedError(
            "OPEN_REGISTERED_DATA is False.  This is the default: a stray "
            "import or notebook run cannot reach registered data.  "
            f"{APPROVAL_NOTE}")
    bundle_dir = str(verified_inputs.get("bundle_dir") or "")
    require_execution_approval(approval, f"Q5-E audit over {bundle_dir!r}")
    assert_runtime_ready(MODE_AUDIT)
    verified = reverify_registered_inputs(verified_inputs, approval)
    paths = verified["paths"]
    bundle_dir = paths["bundle_dir"]
    emit("Q5-E: every registered input re-verified from its bytes.")

    _terminal_execution_guard()

    # ---- Everything below is the complete, already-implemented audit. ------
    # Removing the guard above is the *only* change the execution-approval PR
    # makes here: it must expose a finished route, never introduce scientific
    # analysis for the first time.
    inputs = load_all_inputs(bundle_dir, paths["mamba_path"],
                             paths["cache_dir"], paths["mitdb_dir"],
                             paths["v10_source_dir"], approval)
    outcome = run_pipeline(inputs, emit=emit)
    qa_target_set = str(outcome["qa"].get("target_set")
                        or QA_TARGETS_REGISTERED)
    if qa_target_set != QA_TARGETS_REGISTERED:
        # Unreachable from here — production passes no fixture — and checked
        # anyway, because the one thing a fixture must never do is leave a
        # bundle in the production output directory.
        raise Q5EError(
            f"refusing to publish: the production route produced a "
            f"{qa_target_set} QA verdict.  A run measured against anything "
            f"other than the registered targets is not a Q5-E result and is "
            f"not written to {out_dir!r}.")
    timestamp = run_timestamp()
    result = build_result(
        qa=outcome["qa"], m0=outcome["m0"], m1=outcome["m1"],
        m2=outcome["m2"], m3=outcome["m3"], m4=outcome["m4"],
        nulls=outcome["nulls"], tests=outcome["tests"],
        decision=outcome["decision"],
        source_files=verified["source_files"],
        identity_audit={"checks": verified["checks"],
                        "discovery": verified_inputs.get("discovery_audit"),
                        "source_match": source_match_equivalence_status()})
    directory = os.path.join(out_dir, f"{timestamp}_{RUN_SLUG}")
    write_bundle(directory, result,
                 build_config(MODE_AUDIT, timestamp, execution_approved=True,
                              qa_target_set=qa_target_set),
                 build_manifest({key: paths[key] for key in
                                 DISCOVERED_PATH_KEYS}, timestamp,
                                qa_target_set=qa_target_set),
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
        "",
        "  Registered input identity (P1/P2, registered 2026-08-14):",
        f"    MIT-BIH tree aggregate     : "
        f"{MITDB_TREE_AGGREGATE or INPUT_IDENTITY_REGISTRATION_REQUIRED}",
        f"    canonical bundle run       : {SOURCE_BUNDLE_RUN}",
        f"    canonical bundle folder id : {SOURCE_BUNDLE_FOLDER_ID}",
        f"    canonical bundle digests   : "
        f"{sorted(SOURCE_BUNDLE_FILE_SHA256) or SOURCE_BUNDLE_DIGEST_FREEZE_REQUIRED}",
        f"    all four moved together    : "
        f"{input_identity_registration()['registered']}",
        f"    bundle kind                : {SOURCE_BUNDLE_PROVENANCE['kind']}",
        "",
        "  Open registration items - each is a terminal stop, not a warning:",
        f"    source-matching adapter (P3): "
        f"{source_match_equivalence_status()['status']}",
        "  The adapter is a text-derived candidate, unverified against the",
        "  registered data.py; M4 stops before the detector until a",
        "  differential PREP records a PASS.  P3 is the only remaining stop,",
        "  and it still needs its own design, implementation, execution and",
        "  result acceptance.",
        "",
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
