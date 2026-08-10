"""EXP-2026-007 / Q5-D — deletion-aware order-preserving beat identity join.

IMPLEMENTATION ONLY.  NO TRAINING / NO ASSOCIATION / NOT RUN ON REGISTERED DATA.

This module implements the frozen join specified in
``experiments/specs/EXP-2026-007-q5d-order-preserving-beat-join-gate.md``.
Writing the code and running it on the registered data are **two separate
approvals**.  The user approved the first one.  The second one has not been
given, so every entry point that would open a registered artifact refuses to
run unless an explicit execution-approval token is handed to it, and the
token is not used anywhere in this repository yet.

The question
------------
Does one fixed, deletion-aware, order-preserving alignment of raw MIT-BIH
``.atr`` R-beat order to the registered processed-beat row order recover a
unique, one-to-one, class-balanced beat identity map?  This is an
*identifiability* question.  It is not the parent association question, and a
successful join does not authorise opening a V10 probability.

Two legs, two kinds of evidence
-------------------------------
``Leg 1`` — ``.atr`` -> mamba rows.  Deterministic **source replay**.  The
three frozen mamba rules (registered N/S/V symbol map, the 150-sample boundary
test on annotation position ``pos``, and the fewer-than-five-valid-beats
record rule) are recomputed from the raw annotations alone; no detector is
involved.  Post-filter RR is recomputed exactly as the source does, with the
first pre-RR duplicating the first interval and the last post-RR duplicating
the last interval — so first and last beats are **eligible**, not excluded.
Any deviation from the committed lineage ledger is ``JOIN_RULE_FALSIFIED``
with ``failed_leg = LEG1_SOURCE_REPLAY``.  A missing or hash-inconsistent
input is instead ``JOIN_INPUT_ABSENT``.

``Leg 2`` — mamba rows -> V9/V10 positional rows.  Detector-dependent, so it
is **not** reconstructed from ``.atr``.  It consumes the registered cache rows
in their materialised ``detect_r()`` order.  Facts this module encodes
structurally rather than in prose:

- V9/V10 row order is detection order, **not** ``.atr`` ordinal order.
- The result NPZ stores only ``prob``, ``y`` and ``pid``; row identity is
  positional and nothing else.
- ``t`` is never a join key.  :func:`reject_t_as_join_key` refuses any input
  that offers one.
- Global alignment is forbidden.  Matching happens strictly inside one record
  slice cut arithmetically from the 44-record ledger.
- The 36 equal-count and 8 mismatched-count records are *preregistered audit
  strata*.  Both strata run the same matcher; equal count is never treated as
  positional identity, and ``V9/V10 subset-of mamba`` is never an axiom.
  Mamba cuts at annotation position ``pos`` while V9/V10 cuts at detector
  position ``p``, so a drop-one/add-one cancellation is possible.
- Gaps are permitted on both sequences; no row is ever imputed.
- Every certified mapping is record-local, one-to-one and strictly monotone.

The matcher
-----------
One fixed rule and nothing else.  A candidate edge exists iff both integer
360 Hz sample differences are within one sample::

    abs(mamba_pre_samples[i]  - cache_pre_samples[j])  <= 1
    abs(mamba_post_samples[i] - cache_post_samples[j]) <= 1

Among candidate edges the matcher takes a strictly monotone one-to-one
matching of maximum cardinality.  There is no secondary score, distance
preference, label preference or record-specific penalty.  An edge is
``CERTIFIED`` only when it appears in **every** maximum-cardinality monotone
matching; edges that vary across equally optimal paths are ``AMBIGUOUS`` and
stay unmatched.  Forced edges are found with prefix/suffix dynamic
programming (:func:`match_record`) — optimal matchings are never enumerated
and one arbitrary optimal path is never promoted.

Stages
------
``DESIGN``              — print the frozen rule; read nothing.
``SYNTHETIC_FIXTURES``  — run the fixture battery; synthetic data only.
``LEG1_REPLAY_AUDIT``   — replay ``.atr`` and compare to the mamba ledger.
``LEG2_RECORD_JOIN``    — record-wise matching against the registered caches.
``DS1_GATE``            — the DS1 audit, null and bootstrap.
``DS2_GATE``            — the frozen support gates, once, after DS1 freezes.
``JOIN_REPORT``         — replay a saved bundle; recompute nothing.

``DESIGN``, ``SYNTHETIC_FIXTURES`` and ``JOIN_REPORT`` never open a registered
artifact.  The other four do, and therefore refuse to start without the
separate execution approval.

Decisions: ``JOIN_INPUT_ABSENT`` | ``JOIN_RULE_FALSIFIED`` |
``JOIN_SELECTION_BIASED`` | ``JOIN_UNRESOLVED`` | ``JOIN_IDENTIFIABLE``, plus
``JOIN_RESULT_NOT_RUN`` for the state this repository is actually in.
First-failure-wins picks the single primary decision; every gate's number and
pass/fail is still recorded separately.

Run the tests: ``python3 mit-bih/test_q5d_order_preserving_beat_join.py``
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import random
import sys
from typing import (Dict, Iterable, List, Mapping, Optional, Sequence, Tuple)

EXPERIMENT_ID = "EXP-2026-007"
ARM_ID = "Q5-D"
SUBSTAGE = "Q5D_BEAT_JOIN_IDENTIFIABILITY_GATE"
RUN_SLUG = "q5d_beat_join"
#: Bump whenever the *input contract* changes in a way a notebook must not
#: silently run against.  The notebook asserts a minimum, so a stale clone
#: fails loudly instead of producing a confusing STOP.
#:   1 — first implementation
#:   2 — MIT-BIH expected set = the published 48-record tree (147 files) and
#:       publisher-checksum cross-check; preflight freeze gained
#:       `cache_ledger_contract`; result contract is DS2-only and exhaustive.
#:   3 — publisher checksums are matched on the listed path, not a collapsed
#:       basename (a nested `x_mitdb/RECORDS` was answering for `RECORDS`);
#:       mismatch diagnostics; `checked`/`matched` reported separately.
MODULE_VERSION = 3
MODULE_BUILD = "2026-08-10"

NO_EXECUTION_BANNER = (
    "EXP-2026-007 / Q5-D BEAT JOIN — JOIN ONLY, NO OUTCOME, NO TRAINING")

#: Exactly which approvals exist, spelled out so no reader has to infer them.
#:
#: Both join approvals are now in hand: the design (spec «Status boundary»
#: step 2) and the execution on registered data (step 4).  What is still
#: sealed is everything downstream of the join — the V10 probability values
#: and the association analysis — which need their own further approval, and
#: the DS2 per-beat class labels, which open only after the DS1 rule, hashes,
#: tests, environment, thresholds and DS1 report have frozen.
APPROVAL_NOTE = (
    "Approved: writing this implementation (2026-08-10) AND executing the "
    "join on the registered MIT-BIH / mamba / V9 / V10 artifacts "
    "(2026-08-10).  Still sealed and NOT approved: V10 probability values, "
    "the association analysis, S PR-AUC, and any model training.  DS2 "
    "per-beat class labels open only under the separate post-freeze support "
    "gate.  Execution stays an explicit opt-in so no stray run touches the "
    "registered data by accident, and it must clear the hash preflight first.")

# ─────────────────────────────────────────────────────────────────────────────
# Modes
# ─────────────────────────────────────────────────────────────────────────────
MODE_DESIGN = "DESIGN"
MODE_FIXTURES = "SYNTHETIC_FIXTURES"
MODE_PREFLIGHT = "HASH_PREFLIGHT"
MODE_LEG1 = "LEG1_REPLAY_AUDIT"
MODE_LEG2 = "LEG2_RECORD_JOIN"
MODE_DS1 = "DS1_GATE"
MODE_DS2 = "DS2_GATE"
MODE_REPORT = "JOIN_REPORT"

MODES: Tuple[str, ...] = (MODE_DESIGN, MODE_FIXTURES, MODE_PREFLIGHT,
                          MODE_LEG1, MODE_LEG2, MODE_DS1, MODE_DS2,
                          MODE_REPORT)
#: Modes that reach a registered artifact.  Each needs the execution approval.
#: ``HASH_PREFLIGHT`` is one of them: it opens the artifacts to hash them, and
#: it is the STOP/PASS gate every later stage must clear first.
MODES_NEEDING_EXECUTION_APPROVAL: Tuple[str, ...] = (
    MODE_PREFLIGHT, MODE_LEG1, MODE_LEG2, MODE_DS1, MODE_DS2)
#: Modes that are safe without it, because they only touch synthetic data or
#: an already-produced bundle.
OFFLINE_MODES: Tuple[str, ...] = (MODE_DESIGN, MODE_FIXTURES, MODE_REPORT)
#: Stage names that belong to a substage nobody has authorised.
FORBIDDEN_MODES: Tuple[str, ...] = (
    "ASSOCIATION", "ANALYZE", "TRAIN", "RETRAIN", "CALIBRATE", "SHAM")

# ─────────────────────────────────────────────────────────────────────────────
# Decisions
# ─────────────────────────────────────────────────────────────────────────────
DECISION_INPUT_ABSENT = "JOIN_INPUT_ABSENT"
DECISION_RULE_FALSIFIED = "JOIN_RULE_FALSIFIED"
DECISION_SELECTION_BIASED = "JOIN_SELECTION_BIASED"
DECISION_UNRESOLVED = "JOIN_UNRESOLVED"
DECISION_IDENTIFIABLE = "JOIN_IDENTIFIABLE"
DECISION_NOT_RUN = "JOIN_RESULT_NOT_RUN"
DECISIONS: Tuple[str, ...] = (
    DECISION_INPUT_ABSENT, DECISION_RULE_FALSIFIED, DECISION_SELECTION_BIASED,
    DECISION_UNRESOLVED, DECISION_IDENTIFIABLE, DECISION_NOT_RUN)

LEG1 = "LEG1_SOURCE_REPLAY"
LEG2 = "LEG2_POSITIONAL_JOIN"
LEGS: Tuple[str, ...] = (LEG1, LEG2)

STATUS_CERTIFIED = "CERTIFIED"
STATUS_AMBIGUOUS = "AMBIGUOUS"
STATUS_UNMATCHED = "UNMATCHED"
STATUSES: Tuple[str, ...] = (STATUS_CERTIFIED, STATUS_AMBIGUOUS,
                             STATUS_UNMATCHED)

# Why a row is not certified.  These are audit categories, never inputs.
REASON_NONE = ""
REASON_SYMBOL = "LEG1_SYMBOL_NOT_IN_AAMI"
REASON_BOUNDARY = "LEG1_BOUNDARY_150_SAMPLES"
REASON_TOO_FEW = "LEG1_RECORD_UNDER_FIVE_VALID_BEATS"
REASON_NO_EDGE = "LEG2_NO_CANDIDATE_EDGE"
REASON_NOT_OPTIMAL = "LEG2_EDGE_IN_NO_MAXIMUM_MATCHING"
REASON_AMBIGUOUS = "LEG2_AMBIGUOUS_RANK_CLASS"
REASONS: Tuple[str, ...] = (REASON_NONE, REASON_SYMBOL, REASON_BOUNDARY,
                            REASON_TOO_FEW, REASON_NO_EDGE,
                            REASON_NOT_OPTIMAL, REASON_AMBIGUOUS)

# ─────────────────────────────────────────────────────────────────────────────
# Frozen rule constants.  None of these may move after DS1 or DS2 is seen.
# ─────────────────────────────────────────────────────────────────────────────
FS = 360.0
#: mamba boundary rule (`mit-bih/lineage/v15b_local.py`: WIN_BEFORE/WIN_AFTER).
WIN_BEFORE = 150
WIN_AFTER = 150
#: mamba record rule: a record with fewer than this many valid beats is dropped.
MIN_VALID_BEATS = 5
#: The registered mamba symbol map.  `F` and `Q` are absent on purpose — that
#: single omission is the whole of the 818-beat Q5-B-0 drop map.
AAMI_SYMBOL_MAP: Dict[str, str] = {
    "N": "N", "L": "N", "R": "N", "e": "N", "j": "N",
    "A": "S", "a": "S", "J": "S", "S": "S",
    "V": "V", "E": "V",
}
AAMI_CLASSES: Tuple[str, ...] = ("N", "S", "V")

#: The one fixed candidate-edge tolerance, in integer 360 Hz samples.
RR_TOLERANCE_SAMPLES = 1

UNIT_SECONDS = "seconds"
UNIT_SAMPLES = "samples"
DECLARED_UNITS: Tuple[str, ...] = (UNIT_SECONDS, UNIT_SAMPLES)

#: Fields that may never appear in an input offered as a join key.
BANNED_JOIN_KEYS: Tuple[str, ...] = ("t", "time", "t_seconds", "cumsum_pre")

#: The registered `arm × seed` grid of each results package.  The file set is
#: **preregistered by name**, never discovered with a glob: a glob would let a
#: missing or renamed file pass silently, and "whatever happens to be in the
#: folder" is not a contract.
V10_RESULT_ARMS: Tuple[str, ...] = ("base", "full", "pwave", "pwave_noc",
                                    "v8base")
V9_RESULT_ARMS: Tuple[str, ...] = ("kink", "kink_noctx", "kink_noproto",
                                   "v8_noc", "v8base")
RESULT_SEEDS: Tuple[int, ...] = (1000, 1001, 1002, 1003, 1004)


def result_expected_files(arms: Sequence[str] = V10_RESULT_ARMS
                          ) -> Tuple[str, ...]:
    """`{arm}_s{seed}.npz` for the whole registered grid, in a fixed order."""
    return tuple(f"{arm}_s{seed}.npz"
                 for arm in sorted(arms) for seed in sorted(RESULT_SEEDS))


#: Keys this module is allowed to pull out of a result NPZ.  The probability
#: array is not one of them, in any stage.
RESULT_NPZ_READABLE: Tuple[str, ...] = ("pid",)
RESULT_NPZ_DS1_AUDIT_KEYS: Tuple[str, ...] = ("pid", "y")
RESULT_NPZ_SEALED: Tuple[str, ...] = ("prob",)

# ─────────────────────────────────────────────────────────────────────────────
# Registered artifact contract.  Every constant below is quoted from a source
# file, not inferred from how well the join then works.  The spec requires both
# RR semantics to be frozen from source and manifest *before* any match.
# ─────────────────────────────────────────────────────────────────────────────
#: `mamba_data.npz`, ASSETS.md row `data-mit-mamba`.
MAMBA_SHA256 = ("b1c16106216522cb21291f990e7ab0e7f8dfd8135406db322f41cda3687"
                "f6c05")
MAMBA_BYTES = 204504913
#: The registered copy's Drive id and path.  Two byte-identical duplicates
#: exist (created 2026-08-10); when several copies verify, the registered one
#: is preferred and the others are recorded as duplicates, not treated as an
#: ambiguity.
MAMBA_REGISTERED_DRIVE_ID = "1p3HvC_bnbiQlEanFOVIvVdejy60W0tho"
MAMBA_REGISTERED_PATH = "mitbih/mamba_data.npz"
MAMBA_TOTAL_ROWS = 99871
MAMBA_KEYS: Tuple[str, ...] = ("beat", "ref", "feats", "y", "pid", "t")
#: `Z(26D) = psa_rel(4) + rr(7) + pw(3) + rhy(5) + ptf2_rel(7)`
#: (`mit-bih/lineage/build_penult.py :: FEATS`).  The `rr` block therefore
#: starts at column 4, and `RR_PRE_COL = 0` inside that block.
MAMBA_FEATS_DIM = 26
MAMBA_RR_BLOCK_START = 4
MAMBA_PRE_COLUMN = MAMBA_RR_BLOCK_START + 0
MAMBA_POST_COLUMN = MAMBA_RR_BLOCK_START + 1
#: `rr_all = np.diff(rpks) / FS` — seconds (`v15b_local.py:107`).
MAMBA_RR_UNIT = UNIT_SECONDS
#: mamba duplicates its endpoints: first pre-RR and last post-RR repeat their
#: neighbour interval, so first and last beats are eligible.
MAMBA_ENDPOINT_SEMANTIC = "duplicated"
#: mamba computes RR **after** the symbol and boundary filters, on annotation
#: positions (`v15b_local.py:101-109`).
MAMBA_RR_STAGE = "after_symbol_and_boundary_filter"

#: V9/V10 preprocessing cache, `kinkmap/data.py :: build_record` return dict.
CACHE_KEYS: Tuple[str, ...] = ("beat", "ref", "rr", "sim", "pw", "ctx", "y")
#: `N_RR = 7`; `rr_features` stacks
#: `[pre, post, pre/local, post/local, pre/avg, post-pre, lvar]`
#: (`kinkmap/frontend.py :: rr_features`).
CACHE_RR_DIM = 7
CACHE_PRE_COLUMN = 0
CACHE_POST_COLUMN = 1
#: `rr = np.diff(peaks) / fs` — seconds (`frontend.py :: rr_features`).
CACHE_RR_UNIT = UNIT_SECONDS
#: **This is where the two lineages genuinely differ.**  `rr_features` sets the
#: first pre-RR and the last post-RR to `np.nan` and then `nan_to_num`s them to
#: `0.0`.  It does *not* duplicate them the way mamba does.  A stored `0.0` is
#: therefore a real value meaning "no neighbour", not a missing entry, and it
#: will simply fail to form a candidate edge against mamba's duplicated
#: endpoint.  That row stays UNMATCHED and counts against coverage — which is
#: the honest outcome, not something to patch.
CACHE_ENDPOINT_SEMANTIC = "nan_to_zero"
#: V9/V10 computes `Fr = rr_features(peaks)` on the **full** matched-peak array
#: and only then selects `Fr[idx]` with the boundary-valid rows, so a cache row
#: can carry an RR whose neighbour was boundary-cut (`data.py :: build_record`).
CACHE_RR_STAGE = "before_boundary_filter"
#: V9/V10 drops a record below this many peaks; mamba's rule is five valid
#: beats.  The two record rules are different and both are quoted, not merged.
CACHE_MIN_PEAKS = 2
#: The detector-to-annotation matching tolerance, `tol = int(0.15 * fs)`.
CACHE_MATCH_TOL_SAMPLES = 54

#: Why one sample of tolerance is the right size, and what it is absorbing.
#:
#: A cache RR is a difference of **detector** positions and a mamba RR is a
#: difference of **annotation** positions.  Writing the detector position as
#: `p_j = pos_j + e_j`, the two RRs differ by `e_j - e_{j-1}` — the *change* in
#: detector offset between neighbouring beats, not the offset itself.  A stable
#: detector has a nearly constant per-record offset, so that difference is
#: small.  The frozen tolerance is one 360 Hz sample and is never widened; if
#: the offsets turn out to move faster than that, coverage falls and the
#: registered answer is `JOIN_UNRESOLVED`.
RR_TOLERANCE_RATIONALE = "difference of detector offsets between neighbours"

# ─── Negative controls, null and bootstrap ──────────────────────────────────
CONTROL_WRONG_RECORD = "wrong_record"
CONTROL_ORDER_SHUFFLE = "order_shuffle"
CONTROL_CIRCULAR_SHIFT = "circular_shift"
CONTROL_FAMILIES: Tuple[str, ...] = (CONTROL_WRONG_RECORD,
                                     CONTROL_ORDER_SHUFFLE,
                                     CONTROL_CIRCULAR_SHIFT)
MASTER_SEED = 2026017
BOOTSTRAP_SEED = 2026018
N_NULL_REPLICATES = 10000
N_BOOTSTRAP_REPLICATES = 2000
WRONG_RECORD_QUINTILES = 5

# ─── Acceptance gates (spec «Fixed acceptance and stopping gates») ──────────
GATE_COVERAGE_MIN = 0.95
GATE_S_COVERAGE_MIN = 0.95
GATE_PER_CLASS_COVERAGE_MIN = 0.90
GATE_CLASS_BALANCE_MIN = 0.80
GATE_RECORD_COVERAGE_MIN = 0.80
GATE_RECORD_BALANCE_MIN = 0.80
GATE_AGREEMENT_OVERALL_MIN = 0.995
GATE_AGREEMENT_PER_CLASS_MIN = 0.98
GATE_SIGNAL_TO_NULL_MIN = 5.0
GATE_S_SHARE_INFLATION_MAX = 1.25

#: Source-cohort facts about record 232, kept next to the gate that uses them.
#: This concentration exists **before** the join and cannot be repaired by
#: choosing a favourable join subset.  Gate 12 is source-relative: it asks
#: whether certification *inflated* the share.  It neither replaces nor relaxes
#: the parent spec's absolute 50% ceiling, so a clean join can still leave the
#: parent association blocked by the parent's own preregistered gate.
DS2_S_BEATS_TOTAL = 1837
RECORD_232_S_BEATS = 1382
RECORD_232_S_SHARE = RECORD_232_S_BEATS / DS2_S_BEATS_TOTAL      # 0.7523...
PARENT_ABSOLUTE_RECORD_S_SHARE_CEILING = 0.50

# ─────────────────────────────────────────────────────────────────────────────
# The 44-record ledger.  Registered, never recomputed from join performance.
# ─────────────────────────────────────────────────────────────────────────────
#: ``(record, cache_n)`` in V9/V10 array order, per split.  Source:
#: `research/HANDOFF_2026-08-10_Q5D_preflight_result_to_codex.md` §3, which is
#: the common value of the V9 and V10 cache ``meta.json`` ledgers.
CACHE_LEDGER: Dict[str, Tuple[Tuple[str, int], ...]] = {
    "DS1": (("101", 1862), ("106", 2027), ("108", 1759), ("109", 2528),
            ("112", 2537), ("114", 1875), ("115", 1952), ("116", 2397),
            ("118", 2277), ("119", 1987), ("122", 2474), ("124", 1613),
            ("201", 1961), ("203", 2972), ("205", 2644), ("207", 1859),
            ("208", 2572), ("209", 3004), ("215", 3360), ("220", 2046),
            ("223", 2590), ("230", 2255)),
    "DS2": (("100", 2271), ("103", 2083), ("105", 2566), ("111", 2123),
            ("113", 1794), ("117", 1534), ("121", 1862), ("123", 1517),
            ("200", 2598), ("202", 2134), ("210", 2638), ("212", 2747),
            ("213", 2887), ("214", 2257), ("219", 2153), ("221", 2427),
            ("222", 2477), ("228", 2053), ("231", 1570), ("232", 1780),
            ("233", 3066), ("234", 2752)),
}
SPLITS: Tuple[str, ...] = ("DS1", "DS2")

#: Registered cache start rows, kept separately so :func:`verify_ledger` can
#: check the arithmetic instead of trusting it.
REGISTERED_CACHE_STARTS: Dict[str, Tuple[int, ...]] = {
    "DS1": (0, 1862, 3889, 5648, 8176, 10713, 12588, 14540, 16937, 19214,
            21201, 23675, 25288, 27249, 30221, 32865, 34724, 37296, 40300,
            43660, 45706, 48296),
    "DS2": (0, 2271, 4354, 6920, 9043, 10837, 12371, 14233, 15750, 18348,
            20482, 23120, 25867, 28754, 31011, 33164, 35591, 38068, 40121,
            41691, 43471, 46537),
}

#: ``cache_n - mamba_n`` for the eight preregistered mismatched records.
#: Every other record is an equal-count record.  Registered, not discovered.
MAMBA_COUNT_DELTA: Dict[str, int] = {
    "108": -1, "116": -14, "203": -2, "208": -7, "223": -1,     # DS1, sum -25
    "105": -1, "111": -1, "222": -4,                            # DS2, sum  -6
}
REGISTERED_CACHE_TOTALS: Dict[str, int] = {"DS1": 50551, "DS2": 49289}
REGISTERED_MAMBA_TOTALS: Dict[str, int] = {"DS1": 50576, "DS2": 49295}
REGISTERED_COUNT_DIFFERENCE: Dict[str, int] = {"DS1": -25, "DS2": -6}
REGISTERED_EQUAL_COUNT_RECORDS = 36
REGISTERED_MISMATCHED_RECORDS = 8
REGISTERED_TOTAL_RECORDS = 44

STRATUM_EQUAL = "equal_count"
STRATUM_MISMATCH = "mismatched_count"
STRATA: Tuple[str, ...] = (STRATUM_EQUAL, STRATUM_MISMATCH)

# ─────────────────────────────────────────────────────────────────────────────
# Run-bundle contract
# ─────────────────────────────────────────────────────────────────────────────
DRIVE_RUN_REL = "MedKOS/ecg-model/runs"
RUN_DIR_SUFFIX = "EXP-2026-007_q5d_beat_join"

BUNDLE_FILES: Tuple[str, ...] = (
    "config.json", "manifest.json", "decision.json",
    "synthetic_fixture_results.csv", "join_map.parquet",
    "unmatched_and_ambiguous.csv", "record_class_coverage.csv",
    "negative_control_null.npz", "null_summary.json", "bootstrap.json",
    "log.txt", "summary.md",
)

#: Minimum audit fields of ``join_map``.  A probability column is not here and
#: :func:`validate_join_map_row` rejects one if it ever appears.
JOIN_MAP_FIELDS: Tuple[str, ...] = (
    "split", "record", "raw_atr_ordinal", "raw_r_sample", "mamba_record_row",
    "mamba_global_row", "mamba_file_row", "cache_record_row",
    "result_global_row", "status",
    "pre_rr_difference_samples", "post_rr_difference_samples", "failed_leg",
    "drop_or_unmatched_reason",
)
#: Column names that must never reach a join map, whatever the caller says.
JOIN_MAP_BANNED_FIELDS: Tuple[str, ...] = (
    "prob", "probability", "p_hat", "score", "logit", "v10_prob", "y_prob",
)

#: Textual evidence that this file cannot reach an outcome.  Tokens are split
#: so the table itself does not match.  Checked by
#: :func:`assert_implementation_only`, the cheapest artifact a reviewer can
#: re-run.
FORBIDDEN_TOKENS: Tuple[str, ...] = (
    '["pro' + 'b"]', "['pro" + "b']", ".f" + "it(", ".back" + "ward(",
    "average_" + "precision", "precision_recall_" + "curve",
    "roc_auc_" + "score", "pr_" + "auc(", "torch." + "optim",
    "state_" + "dict", "model." + "predict(", "keras." + "Model",
)


# ─────────────────────────────────────────────────────────────────────────────
# Runtime dependencies.  Checked per stage *before* the work, never discovered
# in the middle of it.
# ─────────────────────────────────────────────────────────────────────────────
#: Install these in the run environment.  `wfdb` is pinned to the version in
#: the registered runtime (`research/ASSETS.md :: env-v9v10-runtime`), which is
#: also what the qualification stage pinned.
PIP_INSTALL_SPEC: Tuple[str, ...] = ("wfdb==4.3.1",)

#: `module -> (what it is for, version in the registered runtime or "")`.
RUNTIME_DEPENDENCIES: Dict[str, Tuple[str, str]] = {
    "numpy": ("reading the registered arrays and caches", "2.5.1"),
    "wfdb": ("reading raw `.atr` annotations and headers (Leg 1)", "4.3.1"),
    "pyarrow": ("writing `join_map.parquet` into the run bundle", ""),
}

#: What each stage actually needs.  `pyarrow` is listed for the join stages
#: because the bundle is written at the *end* of a long run — discovering it
#: is missing there would waste the whole run.
STAGE_REQUIREMENTS: Dict[str, Tuple[str, ...]] = {
    MODE_DESIGN: (),
    MODE_FIXTURES: (),          # synthetic only — pure stdlib
    MODE_REPORT: (),            # reads an existing bundle
    MODE_PREFLIGHT: ("numpy",),
    MODE_LEG1: ("numpy", "wfdb"),
    MODE_LEG2: ("numpy", "wfdb", "pyarrow"),
    MODE_DS1: ("numpy", "wfdb", "pyarrow"),
    MODE_DS2: ("numpy", "wfdb", "pyarrow"),
}


class Q5DJoinError(RuntimeError):
    """Anything that must stop the substage rather than be worked around."""


class ExecutionNotApprovedError(Q5DJoinError):
    """Raised before a registered artifact is opened without approval."""


class NullReuseError(Q5DJoinError):
    """Raised when a stored null is offered to a rule it was not built for."""


# ─────────────────────────────────────────────────────────────────────────────
# Approval barrier
# ─────────────────────────────────────────────────────────────────────────────
#: The exact token a caller must pass to reach registered data.  It is long and
#: unpleasant on purpose: nobody types it by accident, and grepping the repo
#: for it shows immediately that nothing here uses it.
EXECUTION_APPROVAL_TOKEN = (
    "USER-APPROVED-EXP-2026-007-Q5D-BEAT-JOIN-EXECUTION-ON-REGISTERED-DATA")
EXECUTION_APPROVAL_FLAG = "--i-have-separate-execution-approval"

#: The extra token for the one stage that is allowed to see DS2 class labels,
#: and only after the DS1 rule, hashes, tests and thresholds have frozen.
DS2_LABEL_RELEASE_TOKEN = (
    "USER-APPROVED-EXP-2026-007-Q5D-DS2-SUPPORT-GATE-AFTER-DS1-FREEZE")
DS2_LABEL_RELEASE_FLAG = "--ds2-support-gate-released"


def require_execution_approval(approval: Optional[str], what: str) -> None:
    """Gate every path that would open a registered artifact.

    Called *before* the file is opened, not after, so a refusal leaves no
    trace of having touched the data.
    """
    if approval != EXECUTION_APPROVAL_TOKEN:
        raise ExecutionNotApprovedError(
            f"refusing to open {what}: reaching a registered artifact is an "
            f"explicit opt-in, so that no stray call touches the data.\n"
            f"{APPROVAL_NOTE}\n"
            f"Pass {EXECUTION_APPROVAL_FLAG} (CLI) or the execution-approval "
            f"token (API), and clear the hash preflight first.")


def require_ds2_label_release(release: Optional[str], what: str) -> None:
    """DS2 class labels stay sealed until the DS1 rule has frozen."""
    if release != DS2_LABEL_RELEASE_TOKEN:
        raise ExecutionNotApprovedError(
            f"refusing to read {what}: DS2 per-beat class labels are sealed "
            f"until the DS1 rule, source hash, tests, environment, thresholds "
            f"and DS1 report are frozen and the DS2 support gate is released. "
            f"They may never be used to select the join rule.")


def execution_is_approved(approval: Optional[str]) -> bool:
    """Non-raising probe, for cards and notebooks that report their own state."""
    return approval == EXECUTION_APPROVAL_TOKEN


def open_registered_input(path: str, approval: Optional[str], what: str):
    """The single door to a registered file.  Checks approval, then existence.

    Order matters: without approval this never calls :func:`open`, so an
    unapproved run cannot even learn whether the artifact is present.
    """
    require_execution_approval(approval, what)
    if not os.path.exists(path):
        raise Q5DJoinError(
            f"{DECISION_INPUT_ABSENT}: {what} not found at {path!r}")
    return open(path, "rb")


def read_result_npz(path: str, split: str, keys: Sequence[str],
                    approval: Optional[str] = None,
                    ds2_label_release: Optional[str] = None
                    ) -> Dict[str, object]:
    """Read the *positional* fields of a result NPZ.  Never the probability.

    ``pid`` proves the contiguous per-record block; ``y`` is the processed
    class, allowed on DS1 for audit and on DS2 only under the released support
    gate.  The sealed keys are refused whatever the caller asks for, so there
    is no argument that reaches a probability value.
    """
    split = _check_split(split)
    asked = tuple(str(k) for k in keys)
    for key in asked:
        if key in RESULT_NPZ_SEALED:
            raise Q5DJoinError(
                f"refusing to read {key!r} from a result NPZ: V10 probability "
                f"values stay sealed for the whole of this substage, pass or "
                f"fail.  Readable keys: {RESULT_NPZ_DS1_AUDIT_KEYS}")
        if key not in RESULT_NPZ_DS1_AUDIT_KEYS:
            raise Q5DJoinError(
                f"unknown result-NPZ key {key!r}; this join reads only "
                f"{RESULT_NPZ_DS1_AUDIT_KEYS}")
        if key == "y" and split == "DS2":
            require_ds2_label_release(ds2_label_release,
                                      f"DS2 result-NPZ key {key!r}")
    require_execution_approval(approval, f"result NPZ for {split} at {path!r}")
    import numpy                                        # noqa: PLC0415
    out: Dict[str, object] = {}
    with numpy.load(path) as bundle:                    # pragma: no cover
        present = tuple(bundle.files)
        missing = [k for k in asked if k not in present]
        if missing:
            raise Q5DJoinError(
                f"{DECISION_INPUT_ABSENT}: result NPZ {path!r} is missing "
                f"{missing}; its positional contract cannot be proven")
        for key in asked:
            out[key] = bundle[key]
    return out


# ─────────────────────────────────────────────────────────────────────────────
# Hash preflight — the material-input contract, checked before any matching
# ─────────────────────────────────────────────────────────────────────────────
def resolve_canonical_mamba(candidates: Sequence[str],
                            approval: Optional[str] = None,
                            registered_path: Optional[str] = None
                            ) -> Dict[str, object]:
    """Pick the canonical `mamba_data.npz` among same-size Drive copies.

    Three same-size copies exist and two were created after the lineage was
    registered, so size proves nothing — only bytes do.

    The rule, corrected after Codex review:

    - **zero** candidates matching :data:`MAMBA_SHA256` -> `JOIN_INPUT_ABSENT`;
    - **one or more** matches -> they are byte-identical to the registered
      asset by definition, which is *not* an identity ambiguity.  Prefer the
      copy at the registered path (Drive id :data:`MAMBA_REGISTERED_DRIVE_ID`)
      when it is among them; otherwise take the first match in the given order
      and record that the registered copy was absent, so the manifest says
      which physical file was used;
    - a same-size candidate whose hash differs is excluded and recorded.

    An earlier version stopped when two candidates matched.  That was wrong:
    two verified byte-identical copies carry the same content, and refusing
    them would have blocked a run for a non-problem.
    """
    require_execution_approval(approval, "mamba_data.npz candidates")
    registered = registered_path or MAMBA_REGISTERED_PATH
    checked: List[Dict[str, object]] = []
    matches: List[str] = []
    for path in candidates:
        row: Dict[str, object] = {"path": path, "exists": os.path.exists(path)}
        if row["exists"]:
            row["bytes"] = os.path.getsize(path)
            row["sha256"] = sha256_file(path)
            row["matches_registered"] = row["sha256"] == MAMBA_SHA256
            row["same_size_different_hash"] = (
                not row["matches_registered"] and row["bytes"] == MAMBA_BYTES)
            if row["matches_registered"]:
                matches.append(path)
        checked.append(row)
    if not matches:
        raise Q5DJoinError(
            f"{DECISION_INPUT_ABSENT}: no candidate matches the registered "
            f"mamba SHA-256 {MAMBA_SHA256[:16]}….  Checked: {checked}.  A copy "
            f"that cannot be linked byte-for-byte to the canonical asset is "
            f"not a substitute.")
    preferred = [p for p in matches if os.path.normpath(p).endswith(
        os.path.normpath(registered).lstrip(os.sep))] if registered else []
    canonical = preferred[0] if preferred else matches[0]
    for row in checked:
        if row.get("matches_registered"):
            row["role"] = ("canonical" if row["path"] == canonical
                           else "byte_identical_duplicate")
        elif row.get("exists"):
            row["role"] = ("excluded_same_size_different_hash"
                           if row.get("same_size_different_hash")
                           else "excluded_hash_mismatch")
        else:
            row["role"] = "absent"
    return {
        "canonical": canonical,
        "canonical_sha256": MAMBA_SHA256,
        "registered_copy_present": bool(preferred),
        "registered_path": registered,
        "byte_identical_duplicates": [p for p in matches if p != canonical],
        "candidates": checked,
    }


def hash_file_set(directory: str, expected_names: Sequence[str],
                  approval: Optional[str] = None) -> Dict[str, object]:
    """SHA-256 every file in a registered directory, then aggregate them.

    Hashing a directory *listing* proves nothing about content, so this hashes
    each file's bytes and folds `(name, size, sha256)` for the sorted expected
    set into one aggregate digest.  Extra and missing entries are reported
    separately — an unexpected file in a registered directory is a contract
    problem even when every expected file verifies.
    """
    require_execution_approval(approval, f"file set at {directory!r}")
    if not os.path.isdir(directory):
        return {"ok": False, "directory": directory, "files": [],
                "missing": list(expected_names), "extra": [],
                "aggregate": None, "problems": [f"not a directory: {directory}"]}
    present = sorted(name for name in os.listdir(directory)
                     if os.path.isfile(os.path.join(directory, name)))
    expected = sorted(set(expected_names))
    missing = [name for name in expected if name not in present]
    extra = [name for name in present if name not in expected]
    files: List[Dict[str, object]] = []
    for name in expected:
        if name in missing:
            continue
        path = os.path.join(directory, name)
        files.append({"name": name, "bytes": os.path.getsize(path),
                      "sha256": sha256_file(path)})
    aggregate = hashlib.sha256(_canonical_json(
        [[f["name"], f["bytes"], f["sha256"]] for f in files]
    ).encode("utf-8")).hexdigest()
    problems: List[str] = []
    if missing:
        problems.append(f"{directory}: missing {missing}")
    if extra:
        problems.append(f"{directory}: unexpected {extra}")
    return {"ok": not problems, "directory": directory, "files": files,
            "missing": missing, "extra": extra, "aggregate": aggregate,
            "problems": problems, "n_files": len(files)}


def cache_expected_files() -> Tuple[str, ...]:
    """`meta.json` plus one npz per registered record — the whole cache."""
    records = [row.record for split in SPLITS for row in build_ledger()[split]]
    return ("meta.json",) + tuple(f"{r}.npz" for r in sorted(records))


#: The four paced records.  MIT-BIH publishes 48 records; the de Chazal
#: inter-patient split uses 44 and excludes these, so the join never reads
#: them — but they are part of the **published tree**, and an integrity
#: contract over that tree must expect them.  Treating them as "unexpected"
#: was an error: it made a correct, immutable publisher directory fail.
MITDB_PACED_RECORDS: Tuple[str, ...] = ("102", "104", "107", "217")
#: Publisher metadata shipped alongside the waveforms.
MITDB_METADATA_FILES: Tuple[str, ...] = ("ANNOTATORS", "RECORDS",
                                         "SHA256SUMS.txt")
MITDB_CHECKSUM_FILE = "SHA256SUMS.txt"
#: `research/ASSETS.md :: data-mitdb-raw-100` — 48 records x 3 + 3 metadata.
MITDB_REGISTERED_FILE_COUNT = 48 * 3 + 3


def mitdb_all_records() -> Tuple[str, ...]:
    """All 48 published records: the 44 the join uses, plus the 4 paced."""
    used = {row.record for split in SPLITS for row in build_ledger()[split]}
    return tuple(sorted(used | set(MITDB_PACED_RECORDS)))


def mitdb_expected_files() -> Tuple[str, ...]:
    """The published MIT-BIH tree: 48 records x `.dat/.hea/.atr`, plus metadata.

    This is the *integrity* contract over an immutable publisher directory,
    not the list of files the join opens.  Which records the join reads is
    decided by the 44-record ledger and by nothing else; expecting the whole
    published tree here only means a missing or added file is noticed.
    """
    names: List[str] = []
    for record in mitdb_all_records():
        names.extend([f"{record}.atr", f"{record}.dat", f"{record}.hea"])
    return tuple(sorted(names) + sorted(MITDB_METADATA_FILES))


def parse_sha256sums(path: str) -> Dict[str, str]:
    """Parse a publisher `SHA256SUMS.txt` into `{relative path: sha256}`.

    The key is the path **exactly as listed**.  Collapsing it to a basename
    looks harmless and is not: the MIT-BIH list covers a wider tree than the
    directory we verify, and it contains both

        fcdca7ea…  RECORDS
        215c6f70…  x_mitdb/RECORDS

    Under basename collapsing the second entry overwrites the first, so the
    top-level `RECORDS` gets compared against a *different file's* digest and
    a pristine tree fails.  `ANNOTATORS` has the same shape but identical
    digests, so it passed silently — the bug only showed where the two files
    genuinely differ.  Keep the paths.
    """
    out: Dict[str, str] = {}
    with open(path, encoding="utf-8", errors="replace") as handle:
        for line in handle:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split(None, 1)
            if len(parts) != 2:
                continue
            digest, name = parts[0].strip(), parts[1].strip()
            name = name.lstrip("*")
            if name.startswith("./"):
                name = name[2:]
            if len(digest) == 64:
                out[name] = digest.lower()
    return out


def verify_against_publisher_checksums(file_set: Mapping[str, object],
                                       directory: str) -> Dict[str, object]:
    """Compare an already-hashed file set against the publisher's own list.

    Stronger than an aggregate over "whatever was there": it says the bytes
    are the *published* bytes.  Re-uses the digests computed by
    :func:`hash_file_set`, so this costs no extra I/O.  If the tree ships no
    checksum file the result is reported as unavailable rather than passed.
    """
    checksum_path = os.path.join(directory, MITDB_CHECKSUM_FILE)
    if not os.path.exists(checksum_path):
        return {"available": False, "ok": True, "problems": [],
                "note": f"{MITDB_CHECKSUM_FILE} not present in {directory}"}
    published = parse_sha256sums(checksum_path)
    problems: List[str] = []
    checked = matched = 0
    mismatched: List[Dict[str, object]] = []
    unlisted: List[str] = []
    for entry in file_set.get("files", ()):                 # type: ignore[union-attr]
        name = str(entry["name"])
        if name == MITDB_CHECKSUM_FILE:
            continue                    # a checksum file cannot list itself
        # Exact top-level key only.  The files we hash are the top level of
        # this directory, so a nested entry like `x_mitdb/RECORDS` must never
        # answer for `RECORDS`.
        want = published.get(name)
        if want is None:
            unlisted.append(name)       # publisher does not list it here
            continue
        checked += 1
        observed = str(entry["sha256"]).lower()
        if observed == want:
            matched += 1
        else:
            problems.append(f"{name}: sha256 differs from the publisher list")
            mismatched.append(describe_checksum_mismatch(
                directory, name, published=want, observed=observed,
                size=entry.get("bytes")))
    # If the publisher lists everything under a prefix we do not use, nothing
    # would be checked and the result would read as a pass.  Silence is not
    # verification, so say so.
    considered = sum(1 for e in file_set.get("files", ())      # type: ignore[union-attr]
                     if str(e["name"]) != MITDB_CHECKSUM_FILE)
    if considered and not checked:
        problems.append(
            f"the publisher list has {len(published)} entries but none of the "
            f"{considered} files in {directory} matched a top-level name; "
            f"nothing was actually verified")
    return {"available": True, "ok": not problems, "problems": problems,
            # `checked` is how many had a published entry; `matched` is how
            # many agreed.  An earlier version reported only the former under
            # the name "verified", which read as though everything passed.
            "checked": checked, "matched": matched, "considered": considered,
            "mismatched": mismatched, "unlisted": sorted(unlisted),
            "published_entries": len(published),
            "read_by_the_join": sorted(
                n for n in (m["name"] for m in mismatched)
                if _is_read_by_the_join(n))}


#: Extensions the join actually opens.  `wfdb` reads `{record}.hea` and
#: `{record}.atr` for each ledger record; nothing else in the tree is touched.
JOIN_READ_EXTENSIONS: Tuple[str, ...] = (".hea", ".atr")


def _is_read_by_the_join(name: str) -> bool:
    """Does the join ever open this file?  Publisher indexes: no."""
    stem, ext = os.path.splitext(name)
    if ext.lower() not in JOIN_READ_EXTENSIONS:
        return False
    return stem in {row.record for split in SPLITS
                    for row in build_ledger()[split]}


def describe_checksum_mismatch(directory: str, name: str, published: str,
                               observed: str,
                               size: Optional[object] = None
                               ) -> Dict[str, object]:
    """Enough detail to tell a benign rewrite from a real corruption.

    A hash mismatch on its own says "different bytes" and nothing more.  For a
    small publisher index file the difference is usually visible immediately —
    a changed line ending, a stripped trailing newline, a BOM, or a genuinely
    different record list.  This reports those without changing any gate.
    """
    path = os.path.join(directory, name)
    out: Dict[str, object] = {
        "name": name, "published_sha256": published,
        "observed_sha256": observed, "bytes": size,
        "read_by_the_join": _is_read_by_the_join(name),
    }
    try:
        with open(path, "rb") as handle:
            blob = handle.read(65536)
    except OSError as exc:                              # pragma: no cover
        out["error"] = str(exc)
        return out
    out["bytes_read"] = len(blob)
    out["starts_with_bom"] = blob.startswith(b"\xef\xbb\xbf")
    out["has_crlf"] = b"\r\n" in blob
    out["ends_with_newline"] = blob.endswith(b"\n")
    if len(blob) <= 8192:
        try:
            text = blob.decode("utf-8")
        except UnicodeDecodeError:                      # pragma: no cover
            out["binary"] = True
            return out
        lines = [ln for ln in text.splitlines() if ln.strip()]
        out["non_empty_lines"] = len(lines)
        out["first_lines"] = lines[:5]
        out["last_lines"] = lines[-5:]
        # The two cheapest benign explanations, checked explicitly.
        stripped = text.rstrip("\n")
        out["sha256_without_trailing_newlines"] = hashlib.sha256(
            stripped.encode("utf-8")).hexdigest()
        out["sha256_with_single_trailing_newline"] = hashlib.sha256(
            (stripped + "\n").encode("utf-8")).hexdigest()
        out["sha256_lf_normalised"] = hashlib.sha256(
            text.replace("\r\n", "\n").encode("utf-8")).hexdigest()
        for label in ("sha256_without_trailing_newlines",
                      "sha256_with_single_trailing_newline",
                      "sha256_lf_normalised"):
            if out[label] == published:
                out["benign_explanation"] = label
                break
    return out


def hash_preflight(assets: Mapping[str, str],
                   approval: Optional[str] = None,
                   expected: Optional[Mapping[str, str]] = None
                   ) -> Dict[str, object]:
    """Hash every registered input and decide STOP / PASS before matching.

    ``assets`` maps a label to a path.  ``expected`` gives the registered
    SHA-256 for whichever labels have one; a label without a registered hash is
    hashed and **recorded** so the run bundle pins it, but its absence is not
    by itself a failure — the spec's `JOIN_INPUT_ABSENT` covers missing or
    mismatched artifacts, not artifacts that were never hashed before.

    Returns a report whose ``ok`` decides whether Leg 1 may start.  This is the
    STOP/PASS gate the notebook runs first.
    """
    require_execution_approval(approval, "registered asset hash preflight")
    expected = dict(expected or {})
    rows: List[Dict[str, object]] = []
    problems: List[str] = []
    for label, path in sorted(assets.items()):
        row: Dict[str, object] = {"asset": label, "path": path}
        if not os.path.exists(path):
            row["status"] = "MISSING"
            problems.append(f"{label}: not found at {path}")
            rows.append(row)
            continue
        if os.path.isdir(path):
            names = sorted(os.listdir(path))
            row["status"] = "DIRECTORY"
            row["entries"] = len(names)
            row["sha256"] = hashlib.sha256(
                "\n".join(names).encode("utf-8")).hexdigest()
            row["listing_hash_only"] = True
        else:
            row["bytes"] = os.path.getsize(path)
            row["sha256"] = sha256_file(path)
            want = expected.get(label)
            if want is None:
                row["status"] = "RECORDED_NO_REGISTERED_HASH"
            elif row["sha256"] == want:
                row["status"] = "VERIFIED"
            else:
                row["status"] = "HASH_MISMATCH"
                problems.append(
                    f"{label}: sha256 {row['sha256'][:16]}… != registered "
                    f"{want[:16]}…")
        rows.append(row)
    return {
        "ok": not problems,
        "decision": None if not problems else DECISION_INPUT_ABSENT,
        "problems": problems,
        "assets": rows,
        "rule_fingerprint": rule_fingerprint(),
        "verified": sum(1 for r in rows if r.get("status") == "VERIFIED"),
        "recorded": sum(1 for r in rows
                        if r.get("status") == "RECORDED_NO_REGISTERED_HASH"),
        "total": len(rows),
    }


def assert_preflight_passed(report: Mapping[str, object]) -> None:
    """Leg 1 may not start on a failed preflight.  This is the hard stop."""
    if not report.get("ok"):
        raise Q5DJoinError(
            f"{DECISION_INPUT_ABSENT}: the material-input contract is not "
            f"closed, so no matching may start.\n  "
            + "\n  ".join(str(p) for p in report.get("problems", ())))


#: Every field a preflight freeze must carry before any matching starts.
PREFLIGHT_FREEZE_FIELDS: Tuple[str, ...] = (
    "ok", "rule_fingerprint", "canonical_mamba", "cache_aggregate",
    "mitdb_aggregate", "cache_ledger_contract", "result_contract",
)

#: The split whose rows a result NPZ actually holds.  V9/V10 result packages
#: are DS2 prediction outputs, so a DS1 row contract must never be demanded of
#: them — one `pid` array cannot satisfy both the DS1 50,551-row ledger and
#: the DS2 49,289-row ledger, and asking it to would STOP a perfectly good
#: asset.  DS1 is verified from the cache/ledger side instead.
RESULT_NPZ_SPLIT = "DS2"


def verify_cache_ledger_contract(cache_dir: str,
                                 approval: Optional[str] = None
                                 ) -> Dict[str, object]:
    """DS1 and DS2 record boundaries, proven from the cache `meta.json`.

    This is the DS1 side of the positional contract.  DS1 never gets a result
    NPZ check because the result packages hold DS2 rows; its row order and
    boundaries come from the cache, which is what the ledger registers.
    """
    require_execution_approval(approval, f"cache ledger at {cache_dir!r}")
    meta_path = os.path.join(cache_dir, "meta.json")
    if not os.path.exists(meta_path):
        return {"ok": False, "problems": [f"cache meta.json missing at "
                                          f"{meta_path}"], "observed": {}}
    with open(meta_path, encoding="utf-8") as handle:
        meta = json.load(handle)
    observed: Dict[str, Dict[str, int]] = {"DS1": {}, "DS2": {}}
    for record, entry in meta.items():
        split = str(entry.get("split", "")).upper()
        if split in observed:
            observed[split][str(record)] = int(entry.get("n", -1))
    boundary = verify_record_boundaries(observed)
    return {"ok": boundary["ok"], "problems": list(boundary["problems"]),
            "observed": {s: len(observed[s]) for s in SPLITS},
            "meta_sha256": sha256_file(meta_path)}


def _pid_digest(pid: Sequence[object]) -> str:
    """Hash the `pid` *content*, independent of the stored dtype.

    Two files holding the same row assignment must produce the same digest
    even if one saved `int32` and the other `int64`, so the raw buffer is not
    hashed.
    """
    return hashlib.sha256(
        ",".join(str(int(v)) for v in pid).encode("utf-8")).hexdigest()


def verify_result_set_positional_contract(
        results_dir: str, arms: Sequence[str] = V10_RESULT_ARMS,
        approval: Optional[str] = None,
        split: str = RESULT_NPZ_SPLIT) -> Dict[str, object]:
    """Check the `pid` contract of **every** file in the registered grid.

    One representative file only shows that the producer was *written* to
    store the same `pid`; it cannot detect a file that was mis-copied, mixed
    in from another run, or truncated.  Reading `pid` opens no outcome, so
    checking all 25 is cheap and is the right scope.

    Every file must independently satisfy the registered ledger — total rows,
    the 22 records in registered order, contiguous per-record blocks, and each
    record's registered `n` and start — and all files' `pid` digests must be
    identical.  A missing file, or any file that disagrees, is
    `JOIN_INPUT_ABSENT` for the **whole set**: dropping the failures and
    proceeding with the rest is explicitly forbidden, because that would be
    selecting inputs on the basis of which ones happened to pass.
    """
    split = _check_split(split)
    expected = result_expected_files(arms)
    require_execution_approval(approval, f"result set at {results_dir!r}")

    files: List[Dict[str, object]] = []
    problems: List[str] = []
    digests: Dict[str, List[str]] = {}
    for name in expected:
        path = os.path.join(results_dir, name)
        row: Dict[str, object] = {"name": name, "path": path}
        if not os.path.exists(path):
            row["status"] = "MISSING"
            problems.append(f"{name}: missing from {results_dir}")
            files.append(row)
            continue
        # Read `pid` once per file.  Over a Drive mount the second read is
        # not free, and 25 files is 25 reads, not 50.
        arrays = read_result_npz(path, split, ("pid",), approval)
        labels = [str(int(v)) for v in list(arrays["pid"])]
        report = check_pid_blocks(labels, split)
        digest = _pid_digest(list(arrays["pid"]))
        row.update({"status": "VERIFIED" if report["ok"] else "CONTRACT_FAIL",
                    "rows": sum(b["n"] for b in report["blocks"]),
                    "blocks": len(report["blocks"]),
                    "pid_sha256": digest})
        digests.setdefault(digest, []).append(name)
        if not report["ok"]:
            problems.extend(f"{name}: {p}" for p in report["problems"])
        files.append(row)

    if len(digests) > 1:
        groups = {d[:16]: sorted(names) for d, names in digests.items()}
        problems.append(
            f"the {len(expected)} result files do not share one `pid` "
            f"assignment; digest groups: {groups}")

    return {
        "ok": not problems,
        "decision": None if not problems else DECISION_INPUT_ABSENT,
        "split": split,
        "directory": results_dir,
        "arms": sorted(arms),
        "seeds": list(RESULT_SEEDS),
        "expected_files": list(expected),
        "n_expected": len(expected),
        "n_verified": sum(1 for f in files if f.get("status") == "VERIFIED"),
        "files": files,
        "pid_digest": next(iter(digests)) if len(digests) == 1 else None,
        "problems": problems,
    }


def build_preflight(mamba_candidates: Sequence[str], cache_dir: str,
                    mitdb_dir: str, results_dir: str,
                    approval: Optional[str] = None,
                    result_arms: Sequence[str] = V10_RESULT_ARMS
                    ) -> Dict[str, object]:
    """Close the whole material-input contract, once, before any matching.

    Produces the freeze that :func:`run_join` requires.  It covers everything
    `JOIN_INPUT_ABSENT` is defined over:

    - the canonical mamba asset, resolved by bytes among the Drive copies;
    - the V9/V10 cache as a per-file aggregate (content, not a listing);
    - the raw MIT-BIH source aggregate;
    - **DS1**: record boundaries from the cache `meta.json` against the ledger;
    - **DS2**: the `pid` positional contract of **all** registered result
      files, plus the requirement that they share one `pid` assignment.

    The two splits are checked differently on purpose.  The result packages
    hold DS2 rows, so demanding a DS1 row contract from them would STOP a
    correct asset; DS1's row order lives in the cache, which is what the
    ledger registers.
    """
    require_execution_approval(approval, "material-input preflight")
    assert_runtime_ready(MODE_PREFLIGHT)
    problems: List[str] = []

    mamba = resolve_canonical_mamba(mamba_candidates, approval)
    cache = hash_file_set(cache_dir, cache_expected_files(), approval)
    problems.extend(cache["problems"])
    mitdb = hash_file_set(mitdb_dir, mitdb_expected_files(), approval)
    problems.extend(mitdb["problems"])
    publisher = verify_against_publisher_checksums(mitdb, mitdb_dir)
    problems.extend(publisher["problems"])

    ledger_contract = verify_cache_ledger_contract(cache_dir, approval)
    problems.extend(ledger_contract["problems"])

    results = verify_result_set_positional_contract(results_dir, result_arms,
                                                    approval)
    problems.extend(results["problems"])

    return {
        "ok": not problems,
        "problems": problems,
        "decision": None if not problems else DECISION_INPUT_ABSENT,
        "rule_fingerprint": rule_fingerprint(),
        "canonical_mamba": {"path": mamba["canonical"],
                            "sha256": mamba["canonical_sha256"],
                            "registered_copy_present":
                                mamba["registered_copy_present"],
                            "byte_identical_duplicates":
                                mamba["byte_identical_duplicates"],
                            "candidates": mamba["candidates"]},
        "cache_aggregate": {"directory": cache["directory"],
                            "aggregate": cache["aggregate"],
                            "n_files": cache["n_files"],
                            "missing": cache["missing"], "extra": cache["extra"]},
        "mitdb_aggregate": {"directory": mitdb["directory"],
                            "aggregate": mitdb["aggregate"],
                            "n_files": mitdb["n_files"],
                            "missing": mitdb["missing"], "extra": mitdb["extra"],
                            "publisher_checksums": publisher},
        "cache_ledger_contract": ledger_contract,
        "result_contract": results,
    }


def verify_preflight_freeze(freeze: Mapping[str, object], mamba_path: str,
                            cache_dir: str, mitdb_dir: str,
                            approval: Optional[str] = None,
                            reverify: bool = True) -> Dict[str, object]:
    """Re-check that the files on disk *now* are the ones the freeze pinned.

    A freeze that merely travelled alongside the run proves nothing; this
    recomputes the canonical mamba digest and the two aggregates and compares
    them.  It also refuses a freeze made under a different rule fingerprint,
    so a relaxed rule cannot inherit a preflight the way it cannot inherit a
    null.
    """
    missing = [f for f in PREFLIGHT_FREEZE_FIELDS if f not in freeze]
    if missing:
        raise Q5DJoinError(
            f"{DECISION_INPUT_ABSENT}: preflight freeze is missing {missing}; "
            f"matching may not start without the complete input contract")
    assert_preflight_passed(freeze)
    if freeze.get("rule_fingerprint") != rule_fingerprint():
        raise Q5DJoinError(
            f"the preflight was frozen under rule "
            f"{freeze.get('rule_fingerprint')!r} but the current rule is "
            f"{rule_fingerprint()!r}; re-run the preflight under the rule you "
            f"intend to execute")

    ledger_contract = dict(freeze.get("cache_ledger_contract") or {})
    if not ledger_contract.get("ok"):
        raise Q5DJoinError(
            f"{DECISION_INPUT_ABSENT}: the DS1/DS2 cache record boundaries are "
            f"not proven in this freeze: {ledger_contract.get('problems')}")

    contract = dict(freeze.get("result_contract") or {})
    if not contract.get("ok"):
        raise Q5DJoinError(
            f"{DECISION_INPUT_ABSENT}: the DS2 result positional contract is "
            f"not proven in this freeze: {contract.get('problems')}")
    if contract.get("n_verified") != contract.get("n_expected") or \
            not contract.get("n_expected"):
        raise Q5DJoinError(
            f"{DECISION_INPUT_ABSENT}: the result contract verified "
            f"{contract.get('n_verified')} of {contract.get('n_expected')} "
            f"registered files.  Every file in the `arm x seed` grid must "
            f"pass; using only the ones that happened to pass is forbidden.")
    if not contract.get("pid_digest"):
        raise Q5DJoinError(
            f"{DECISION_INPUT_ABSENT}: the registered result files do not "
            f"share one `pid` assignment, so their row identity is not a "
            f"single contract")

    checks: Dict[str, object] = {"reverified": bool(reverify)}
    if not reverify:
        return checks
    require_execution_approval(approval, "preflight re-verification")
    frozen_mamba = dict(freeze["canonical_mamba"])
    now = sha256_file(mamba_path)
    if now != frozen_mamba.get("sha256"):
        raise Q5DJoinError(
            f"{DECISION_INPUT_ABSENT}: mamba at {mamba_path!r} now hashes to "
            f"{now[:16]}… but the preflight froze "
            f"{str(frozen_mamba.get('sha256'))[:16]}…")
    checks["mamba_sha256"] = now
    for label, directory, names, frozen in (
            ("cache", cache_dir, cache_expected_files(),
             freeze["cache_aggregate"]),
            ("mitdb", mitdb_dir, mitdb_expected_files(),
             freeze["mitdb_aggregate"])):
        recomputed = hash_file_set(directory, names, approval)
        want = dict(frozen).get("aggregate")
        if not recomputed["ok"] or recomputed["aggregate"] != want:
            raise Q5DJoinError(
                f"{DECISION_INPUT_ABSENT}: {label} aggregate changed since the "
                f"preflight ({str(recomputed['aggregate'])[:16]}… != "
                f"{str(want)[:16]}…) or the file set moved: "
                f"{recomputed['problems']}")
        checks[f"{label}_aggregate"] = recomputed["aggregate"]
    return checks


def release_ds2_support_gate(ds1_bundle_dir: str,
                             freeze: Mapping[str, object],
                             approval: Optional[str] = None) -> str:
    """Mint the DS2 label release only from a verified frozen DS1 bundle.

    The spec allows DS2 support gates exactly once, *after* the DS1 rule,
    hashes, tests, environment, thresholds and DS1 report have frozen.  This
    refuses to hand out the release unless a real DS1 bundle exists and agrees
    with the run about to happen: same rule fingerprint, same input hashes,
    and a DS1 decision that actually carries its null under the registered
    seed.  Without this, DS2 could be run standalone, which is precisely the
    "DS2 selected the rule" failure the design forbids.
    """
    require_execution_approval(approval, "DS2 support-gate release")
    decision_path = os.path.join(ds1_bundle_dir, "decision.json")
    manifest_path = os.path.join(ds1_bundle_dir, "manifest.json")
    null_path = os.path.join(ds1_bundle_dir, "null_summary.json")
    for path in (decision_path, manifest_path, null_path):
        if not os.path.exists(path):
            raise Q5DJoinError(
                f"DS2 release refused: the frozen DS1 bundle is incomplete — "
                f"{os.path.basename(path)} is missing from {ds1_bundle_dir!r}")
    with open(decision_path, encoding="utf-8") as handle:
        decision = json.load(handle)
    with open(manifest_path, encoding="utf-8") as handle:
        manifest = json.load(handle)
    with open(null_path, encoding="utf-8") as handle:
        null = json.load(handle)

    problems: List[str] = []
    current = rule_fingerprint()
    for label, value in (("decision", decision.get("rule_fingerprint")),
                         ("manifest", manifest.get("rule_fingerprint")),
                         ("null", null.get("rule_fingerprint")),
                         ("freeze", freeze.get("rule_fingerprint"))):
        if value != current:
            problems.append(f"{label} rule_fingerprint {value!r} != {current!r}")
    frozen_inputs = dict(manifest.get("preflight") or {})
    for key in ("canonical_mamba", "cache_aggregate", "mitdb_aggregate"):
        want = frozen_inputs.get(key)
        got = freeze.get(key)
        if want is None:
            problems.append(f"DS1 manifest did not freeze {key}")
        elif _canonical_json(want) != _canonical_json(got):
            problems.append(f"{key} differs between the DS1 freeze and this run")
    if null.get("master_seed") != MASTER_SEED:
        problems.append(f"DS1 null seed {null.get('master_seed')!r} != "
                        f"{MASTER_SEED}")
    if not null.get("j_null_max"):
        problems.append("DS1 null carries no replicates")
    if decision.get("decision") not in (DECISION_IDENTIFIABLE,):
        problems.append(
            f"DS1 decision is {decision.get('decision')!r}; the DS2 support "
            f"gate runs only after DS1 qualifies")
    if not manifest.get("code", {}).get("sha256"):
        problems.append("DS1 manifest did not record the code hash")
    if problems:
        raise Q5DJoinError(
            "DS2 release refused — the DS1 freeze does not authorise it:\n  "
            + "\n  ".join(problems))
    return DS2_LABEL_RELEASE_TOKEN


# ─────────────────────────────────────────────────────────────────────────────
# Loaders for the registered artifacts
# ─────────────────────────────────────────────────────────────────────────────
def _contiguous_blocks(values: Sequence[object]) -> List[Tuple[str, int, int]]:
    """``[(label, start, length)]`` for a run-length-contiguous id array.

    A record whose rows are *not* contiguous is a boundary violation, not
    something to sort around, so the caller checks for repeats.
    """
    blocks: List[Tuple[str, int, int]] = []
    start = 0
    for index in range(1, len(values) + 1):
        if index == len(values) or values[index] != values[start]:
            blocks.append((str(values[start]), start, index - start))
            start = index
    return blocks


def load_mamba_sequences(path: str, approval: Optional[str] = None
                         ) -> Dict[str, object]:
    """Read `mamba_data.npz` into one :class:`RecordSequence` per record.

    Row order inside a record is `.atr` ordinal order, which is the source's
    own construction (`v15b_local.py:101-102` appends in `wfdb.rdann` order and
    nothing re-sorts afterwards).

    Record *slices* are measured from the stored `pid` array rather than
    assumed.  That matters: `build_penult.py` enumerates
    `sorted(glob(cache/*.npz))` over **all 44 records at once**, so the global
    row order is `100, 101, 103, 105, …` with DS1 and DS2 interleaved — not
    DS1-block-then-DS2-block.  The spec's ledger builds `mamba_start` by
    cumulative addition *within the frozen split order*, which is a different
    enumeration.  Both are reported: `mamba_record_row` and the observed file
    offset are facts about the artifact, and the ledger start is kept for the
    registered audit.  Only the per-record **counts** are used as a gate, and
    those the ledger does fix.
    """
    require_execution_approval(approval, f"mamba array at {path!r}")
    import numpy                                        # noqa: PLC0415
    with numpy.load(path, allow_pickle=False) as bundle:
        present = tuple(bundle.files)
        for key in ("feats", "pid"):
            if key not in present:
                raise Q5DJoinError(
                    f"{DECISION_INPUT_ABSENT}: mamba array {path!r} has no "
                    f"{key!r}; keys are {present}")
        feats = numpy.asarray(bundle["feats"])
        pid = numpy.asarray(bundle["pid"])
    if feats.ndim != 2 or feats.shape[1] != MAMBA_FEATS_DIM:
        raise Q5DJoinError(
            f"{DECISION_INPUT_ABSENT}: mamba feats shape {feats.shape} is not "
            f"(N, {MAMBA_FEATS_DIM}); the 26-D Z layout is what fixes the RR "
            f"columns, so a different width invalidates the unit contract")
    if feats.shape[0] != MAMBA_TOTAL_ROWS:
        raise Q5DJoinError(
            f"{DECISION_INPUT_ABSENT}: mamba array has {feats.shape[0]} rows, "
            f"registered lineage has {MAMBA_TOTAL_ROWS}")

    labels = [str(int(v)) for v in pid.tolist()]
    blocks = _contiguous_blocks(labels)
    seen = [b[0] for b in blocks]
    if len(seen) != len(set(seen)):
        raise Q5DJoinError(
            f"{DECISION_INPUT_ABSENT}: mamba `pid` is not contiguous per "
            f"record; a record's rows appear in more than one block, so the "
            f"record boundary is not well defined")

    ledger = build_ledger()
    expected = {row.record: row for split in SPLITS for row in ledger[split]}
    sequences: Dict[str, RecordSequence] = {}
    observed: List[Dict[str, object]] = []
    for record, start, length in blocks:
        led = expected.get(record)
        if led is None:
            raise Q5DJoinError(
                f"{DECISION_INPUT_ABSENT}: mamba record {record!r} is not in "
                f"the registered 44-record ledger")
        pre = feats[start:start + length, MAMBA_PRE_COLUMN].tolist()
        post = feats[start:start + length, MAMBA_POST_COLUMN].tolist()
        check_declared_unit(MAMBA_RR_UNIT, pre)
        sequences[record] = RecordSequence(
            record, led.split, "mamba",
            rr_to_samples(pre, MAMBA_RR_UNIT),
            rr_to_samples(post, MAMBA_RR_UNIT),
            [{"mamba_record_row": k, "mamba_file_row": start + k}
             for k in range(length)])
        observed.append({"record": record, "split": led.split,
                         "file_start": start, "n": length,
                         "ledger_n": led.mamba_n,
                         "ledger_split_start": led.mamba_start,
                         "ok": length == led.mamba_n})
    bad = [o for o in observed if not o["ok"]]
    return {"sequences": sequences, "blocks": observed,
            "count_mismatches": bad, "ok": not bad,
            "rows": int(feats.shape[0])}


def load_cache_sequences(cache_dir: str, approval: Optional[str] = None
                         ) -> Dict[str, object]:
    """Read the registered V9/V10 preprocessing cache, record by record.

    The cache preserves the materialised `detect_r()` row order, which is the
    future result-NPZ position.  Its `meta.json` gives `{record: {split, n}}`
    and is checked against the frozen ledger before anything is matched.
    """
    require_execution_approval(approval, f"V9/V10 cache at {cache_dir!r}")
    import numpy                                        # noqa: PLC0415
    meta_path = os.path.join(cache_dir, "meta.json")
    if not os.path.exists(meta_path):
        raise Q5DJoinError(
            f"{DECISION_INPUT_ABSENT}: cache meta.json missing at {meta_path!r}")
    with open(meta_path, encoding="utf-8") as handle:
        meta = json.load(handle)

    observed: Dict[str, Dict[str, int]] = {"DS1": {}, "DS2": {}}
    for record, entry in meta.items():
        split = str(entry.get("split", "")).upper()
        if split in observed:
            observed[split][str(record)] = int(entry.get("n", -1))
    boundary = verify_record_boundaries(observed)
    if not boundary["ok"]:
        raise Q5DJoinError(
            f"{DECISION_INPUT_ABSENT}: cache meta.json does not match the "
            f"registered 44-record ledger: {boundary['problems'][:6]}")

    sequences: Dict[str, RecordSequence] = {}
    for split in SPLITS:
        for led in build_ledger()[split]:
            path = os.path.join(cache_dir, f"{led.record}.npz")
            if not os.path.exists(path):
                raise Q5DJoinError(
                    f"{DECISION_INPUT_ABSENT}: cache record npz missing at "
                    f"{path!r}")
            with numpy.load(path, allow_pickle=False) as bundle:
                if "rr" not in bundle.files:
                    raise Q5DJoinError(
                        f"{DECISION_INPUT_ABSENT}: cache {led.record} has no "
                        f"'rr'; keys are {tuple(bundle.files)}")
                rr = numpy.asarray(bundle["rr"])
            if rr.ndim != 2 or rr.shape[1] != CACHE_RR_DIM:
                raise Q5DJoinError(
                    f"{DECISION_INPUT_ABSENT}: cache {led.record} rr shape "
                    f"{rr.shape} is not (n, {CACHE_RR_DIM})")
            if rr.shape[0] != led.cache_n:
                raise Q5DJoinError(
                    f"{DECISION_INPUT_ABSENT}: cache {led.record} has "
                    f"{rr.shape[0]} rows, ledger says {led.cache_n}")
            pre = rr[:, CACHE_PRE_COLUMN].tolist()
            post = rr[:, CACHE_POST_COLUMN].tolist()
            # `rr_features` writes 0.0 where a neighbour does not exist, so the
            # unit check runs on the non-zero mass; a genuine 0.0 endpoint is
            # data, not a missing value, and is carried through unchanged.
            check_declared_unit(CACHE_RR_UNIT, [v for v in pre if v != 0.0])
            sequences[led.record] = RecordSequence(
                led.record, split, "cache",
                rr_to_samples(pre, CACHE_RR_UNIT),
                rr_to_samples(post, CACHE_RR_UNIT),
                [{"cache_record_row": k,
                  "result_global_row": led.cache_start + k}
                 for k in range(led.cache_n)])
    return {"sequences": sequences, "meta": meta, "boundary": boundary}


def load_cache_classes(cache_dir: str, split: str,
                       approval: Optional[str] = None,
                       ds2_label_release: Optional[str] = None
                       ) -> Dict[Tuple[str, int], str]:
    """``(record, cache_record_row) -> AAMI class`` from the cache's own `y`.

    This is the *processed* class — the V9/V10 positional row's label, which
    is the coverage denominator.  DS1 labels are allowed for audit; DS2 labels
    are sealed until the post-freeze support gate releases them, and they may
    never be used to select the join rule.
    """
    split = _check_split(split)
    if split == "DS2":
        require_ds2_label_release(ds2_label_release, "DS2 cache class labels")
    require_execution_approval(approval, f"{split} cache classes")
    import numpy                                        # noqa: PLC0415
    out: Dict[Tuple[str, int], str] = {}
    for led in build_ledger()[split]:
        path = os.path.join(cache_dir, f"{led.record}.npz")
        with numpy.load(path, allow_pickle=False) as bundle:
            labels = numpy.asarray(bundle["y"]).ravel().tolist()
        if len(labels) != led.cache_n:
            raise Q5DJoinError(
                f"{DECISION_INPUT_ABSENT}: cache {led.record} y has "
                f"{len(labels)} rows, ledger says {led.cache_n}")
        for row, value in enumerate(labels):
            index = int(value)
            if 0 <= index < len(AAMI_CLASSES):
                out[(led.record, row)] = AAMI_CLASSES[index]
    return out


def run_join(mitdb_dir: str, mamba_path: str, cache_dir: str, split: str,
             preflight: Mapping[str, object],
             approval: Optional[str] = None,
             ds2_label_release: Optional[str] = None,
             null_replicates: int = N_NULL_REPLICATES,
             bootstrap_replicates: int = N_BOOTSTRAP_REPLICATES,
             reverify: bool = True) -> Dict[str, object]:
    """The whole frozen pipeline for one split, in the registered order.

    ``preflight`` is **required**, not advisory: a PASSing freeze from
    :func:`build_preflight` covering the canonical mamba hash, the V9/V10
    cache aggregate, the raw MIT-BIH aggregate and the result positional
    contract, produced under this same rule fingerprint.  It is re-verified
    against the files on disk before anything is read, so passing the approval
    token alone cannot get a run past the material-input contract.

    Leg 1 must then pass its exact replay gate before Leg 2 starts; the
    negative controls rerun the *complete* Leg 2 for every replicate.  Nothing
    here chooses among rules, and no probability is opened at any point.
    """
    split = _check_split(split)
    require_execution_approval(approval, f"{split} join pipeline")
    # Order matters.  Authorisation and contract come first, so a call that
    # was never allowed is refused as unauthorised whatever the environment
    # happens to have installed.  Then the runtime check — including the
    # pyarrow used only at the very end to write the bundle, because finding
    # that missing after a completed join would throw the run away.  Only
    # then the expensive re-hashing.
    if split == "DS2" and ds2_label_release != DS2_LABEL_RELEASE_TOKEN:
        raise ExecutionNotApprovedError(
            "the DS2 support gate needs a release minted by "
            "release_ds2_support_gate() from a verified frozen DS1 bundle; "
            "DS2 may not be run standalone")
    verify_preflight_freeze(preflight, mamba_path, cache_dir, mitdb_dir,
                            approval, reverify=False)
    assert_runtime_ready(MODE_DS1 if split == "DS1" else MODE_DS2)
    verified = verify_preflight_freeze(preflight, mamba_path, cache_dir,
                                       mitdb_dir, approval, reverify)

    leg1 = replay_leg1_split(mitdb_dir, split, approval)
    mamba_loaded = load_mamba_sequences(mamba_path, approval)
    mamba_all = mamba_loaded["sequences"]
    stored_rr = {r: {"pre": list(s.pre_samples), "post": list(s.post_samples)}
                 for r, s in mamba_all.items() if s.split == split}
    leg1_report = audit_leg1_against_ledger(leg1, split, stored_rr,
                                            UNIT_SAMPLES)

    cache_loaded = load_cache_sequences(cache_dir, approval)
    cache_all = cache_loaded["sequences"]
    records = [row.record for row in build_ledger()[split]]
    mamba = {r: attach_leg1_identity(mamba_all[r], leg1[r]) for r in records} \
        if leg1_report["ok"] else {}
    cache = {r: cache_all[r] for r in records}

    if not leg1_report["ok"]:
        ledger = DecisionLedger()
        ledger.record("2a_leg1_source_replay", False, leg1_report["problems"],
                      True, DECISION_RULE_FALSIFIED, LEG1)
        return {"split": split, "leg1": leg1_report,
                "decision": ledger.decide(), "rows": [], "results": [],
                "preflight_verified": verified}

    joined = join_split(mamba, cache, split)
    rows, results = joined["rows"], joined["results"]

    processed = load_cache_classes(cache_dir, split, approval,
                                   ds2_label_release)
    mamba_classes = {
        (r, int(e["mamba_record_row"])): str(e["aami"])
        for r in records for e in leg1[r].kept}
    coverage = coverage_report(rows, processed, mamba_classes)
    inflation = s_share_inflation(rows, processed)
    j_true = j_min(rows, processed, mamba_classes)

    null = bootstrap = None
    if split == "DS1" and null_replicates:
        families: Dict[str, List[float]] = {f: [] for f in CONTROL_FAMILIES}
        for family in CONTROL_FAMILIES:
            for replicate in range(int(null_replicates)):
                shuffled = apply_control(family, mamba, replicate)
                control_rows = join_split(shuffled, cache, split)["rows"]
                families[family].append(
                    j_min(control_rows, processed, mamba_classes))
        null = null_summary(families[CONTROL_WRONG_RECORD],
                            families[CONTROL_ORDER_SHUFFLE],
                            families[CONTROL_CIRCULAR_SHIFT], j_true,
                            coverage["overall_total"])
        per_record = {}
        for record in records:
            hits = sum(1 for row in rows
                       if row["record"] == record
                       and row["status"] == STATUS_CERTIFIED)
            per_record[record] = (hits, ledger_record(split, record).cache_n)
        bootstrap = record_cluster_bootstrap(per_record, j_true, null["q95"],
                                             bootstrap_replicates)

    ambiguous = sum(1 for row in rows if row["status"] == STATUS_AMBIGUOUS)
    ledger = evaluate_gates(
        coverage, inflation, null, bootstrap,
        fixtures_ok=fixtures_passed(run_synthetic_fixtures()),
        leg1_ok=True,
        leg2_boundaries_ok=cache_loaded["boundary"]["ok"],
        ambiguous_fraction=_ratio(ambiguous, max(len(rows), 1)))
    decision = ledger.decide()
    decision["strata"] = stratum_report(results)
    decision["j_min_true"] = j_true
    return {"split": split, "leg1": leg1_report, "rows": rows,
            "results": results, "coverage": coverage,
            "s_share_inflation": inflation, "null": null,
            "bootstrap": bootstrap, "decision": decision,
            "mamba_blocks": mamba_loaded["blocks"],
            "preflight_verified": verified}


def replay_leg1_split(mitdb_dir: str, split: str,
                      approval: Optional[str] = None
                      ) -> Dict[str, Leg1Record]:
    """Replay Leg 1 for every record of one split, from raw `.atr`."""
    split = _check_split(split)
    # Permission before capability: an unapproved call is refused as
    # unapproved whatever the environment has installed.
    require_execution_approval(approval, f"{split} raw `.atr` replay")
    assert_runtime_ready(MODE_LEG1)
    out: Dict[str, Leg1Record] = {}
    for led in build_ledger()[split]:
        raw = load_atr_record(mitdb_dir, led.record, approval)
        out[led.record] = replay_leg1_record(led.record, split,
                                             raw["annotations"],
                                             raw["signal_length"])
    return out


def attach_leg1_identity(mamba: RecordSequence, leg1: Leg1Record
                         ) -> RecordSequence:
    """Carry the Leg 1 raw identity onto the mamba rows it produced.

    Leg 1 and the stored mamba slice must already agree on length — that is
    the Leg 1 gate — so this is a positional attach inside one record, which
    is exactly the relationship Leg 1 proved.  It carries the raw `.atr`
    ordinal, R sample and AAMI class used later for the audit; none of them
    enters candidate construction.
    """
    if leg1.n != len(mamba):
        raise Q5DJoinError(
            f"record {mamba.record}: Leg 1 replayed {leg1.n} beats but the "
            f"stored mamba slice has {len(mamba)}; Leg 1 must pass before "
            f"Leg 2 starts")
    rows = []
    for index, entry in enumerate(leg1.kept):
        merged = dict(mamba.rows[index]) if mamba.rows else {}
        merged.update({"raw_atr_ordinal": entry["raw_atr_ordinal"],
                       "raw_r_sample": entry["raw_r_sample"],
                       "symbol": entry["symbol"], "aami": entry["aami"]})
        rows.append(merged)
    return RecordSequence(mamba.record, mamba.split, mamba.side,
                          mamba.pre_samples, mamba.post_samples, rows)


def load_atr_record(mitdb_dir: str, record: str,
                    approval: Optional[str] = None) -> Dict[str, object]:
    """Read one record's raw `.atr` annotations and its signal length.

    Both are needed for Leg 1: the annotation `(pos, symbol)` stream in `.atr`
    sample order, and `len(signal)` for the 150-sample boundary test.  Only
    channel-independent header metadata is used for the length.
    """
    require_execution_approval(approval, f"raw .atr for record {record!r}")
    import wfdb                                         # noqa: PLC0415
    stem = os.path.join(mitdb_dir, str(record))
    header = wfdb.rdheader(stem)
    annotation = wfdb.rdann(stem, "atr")
    return {
        "record": str(record),
        "signal_length": int(header.sig_len),
        "fs": float(header.fs),
        "annotations": list(zip([int(s) for s in annotation.sample],
                                [str(s) for s in annotation.symbol])),
    }


def verify_result_positional_contract(result_npz: str, split: str,
                                      approval: Optional[str] = None
                                      ) -> Dict[str, object]:
    """Prove cache row -> result row without reading a probability.

    The result NPZ must be exactly as long as the split's registered cache
    total, and its `pid` must form contiguous per-record blocks whose lengths
    equal the registered `cache_n`, in the frozen order.  That is the whole
    positional contract, and it is checkable from `pid` alone.
    """
    split = _check_split(split)
    arrays = read_result_npz(result_npz, split, ("pid",), approval)
    labels = [str(int(v)) for v in list(arrays["pid"])]
    return check_pid_blocks(labels, split)


def check_pid_blocks(labels: Sequence[str], split: str) -> Dict[str, object]:
    """The positional contract, on an already-read `pid` array.

    Split out from :func:`verify_result_positional_contract` so a caller that
    has the array in hand does not read the file a second time.
    """
    split = _check_split(split)
    blocks = _contiguous_blocks(labels)
    rows = build_ledger()[split]
    problems: List[str] = []
    if len(labels) != REGISTERED_CACHE_TOTALS[split]:
        problems.append(f"{split}: result NPZ has {len(labels)} rows, "
                        f"registered {REGISTERED_CACHE_TOTALS[split]}")
    if len(blocks) != len(rows):
        problems.append(f"{split}: {len(blocks)} pid blocks, expected "
                        f"{len(rows)}")
    for led, block in zip(rows, blocks):
        record, start, length = block
        if record != led.record:
            problems.append(f"{split}: block {start} is record {record}, "
                            f"ledger order expects {led.record}")
        if start != led.cache_start or length != led.cache_n:
            problems.append(
                f"{split} {record}: observed {length}@{start}, registered "
                f"{led.cache_n}@{led.cache_start}")
    return {"ok": not problems, "problems": problems, "split": split,
            "blocks": [{"record": r, "start": s, "n": n}
                       for r, s, n in blocks],
            "decision": None if not problems else DECISION_INPUT_ABSENT}


# ─────────────────────────────────────────────────────────────────────────────
# Small guards
# ─────────────────────────────────────────────────────────────────────────────
def resolve_mode(mode: str) -> str:
    """Exactly one of :data:`MODES`; a later stage names itself when refused."""
    m = str(mode).strip().upper()
    if m in FORBIDDEN_MODES:
        raise Q5DJoinError(
            f"mode {m!r} belongs to a stage that is NOT authorised: the "
            f"approved substage is {SUBSTAGE}.  The association analysis and "
            f"any model training need their own approval.")
    if m not in MODES:
        raise Q5DJoinError(f"mode must be one of {MODES}, got {mode!r}")
    return m


def _check_split(split: str) -> str:
    s = str(split).strip().upper()
    if s not in SPLITS:
        raise Q5DJoinError(f"split must be one of {SPLITS}, got {split!r}")
    return s


def reject_t_as_join_key(payload: Mapping[str, object]) -> None:
    """``t`` is not a join key and offering one is an error, not a warning.

    ``t = np.cumsum(pre) - pre[0]`` restarts at zero per record and accumulates
    *filtered* RR, so it carries no identity.  Q5-A measured the consequence:
    a 1.9% join, chance level.  Anything that hands this module a ``t`` has
    misunderstood the input contract, so it stops rather than quietly ignoring
    the field.
    """
    if not isinstance(payload, Mapping):
        raise Q5DJoinError("join-key payload must be a mapping")
    declared = payload.get("join_key")
    offered = [k for k in payload if str(k).lower() in BANNED_JOIN_KEYS]
    if declared is not None and str(declared).lower() in BANNED_JOIN_KEYS:
        offered.append(str(declared))
    if offered:
        raise Q5DJoinError(
            f"{sorted(set(offered))} offered as a join key: `t` and its "
            f"aliases are explicitly ineligible.  It restarts at zero per "
            f"record and accumulates filtered RR, so it is not a sample "
            f"index and holds no beat identity.  Row identity here is "
            f"positional, inside a record slice, and nothing else.")


def assert_implementation_only(path: Optional[str] = None
                               ) -> Dict[str, object]:
    """Evidence that this file trains nothing and opens no probability."""
    path = path or os.path.abspath(__file__)
    with open(path, encoding="utf-8") as fh:
        lines = fh.readlines()
    body = "\n".join(ln for ln in lines if not ln.strip().startswith("#"))
    hits = sorted({tok for tok in FORBIDDEN_TOKENS if tok in body})
    if hits:
        raise Q5DJoinError(
            f"forbidden tokens present in {os.path.basename(path)}: {hits}")
    return {"file": os.path.basename(path), "lines": len(lines),
            "forbidden_tokens_checked": len(FORBIDDEN_TOKENS),
            "sha256": sha256_file(path), "clean": True}


def check_runtime_dependencies(mode: str = MODE_DESIGN
                               ) -> Dict[str, object]:
    """Which imports this stage needs, and whether they are importable now.

    Reports rather than raises, so a caller can print the whole picture.  The
    version actually loaded is recorded next to the registered one; a
    difference is a *fact for the manifest*, not a new stopping rule — this
    stage may not invent stops the spec did not register.
    """
    mode = resolve_mode(mode)
    needed = STAGE_REQUIREMENTS.get(mode, ())
    rows: List[Dict[str, object]] = []
    missing: List[str] = []
    for name in needed:
        purpose, registered = RUNTIME_DEPENDENCIES.get(name, ("", ""))
        row: Dict[str, object] = {"module": name, "purpose": purpose,
                                  "registered_version": registered or None}
        try:
            module = __import__(name)
            row["available"] = True
            row["version"] = getattr(module, "__version__", "unknown")
            if registered:
                row["matches_registered_runtime"] = (
                    str(row["version"]) == registered)
        except ImportError as exc:
            row["available"] = False
            row["error"] = str(exc)
            missing.append(name)
        rows.append(row)
    return {"mode": mode, "ok": not missing, "missing": missing,
            "dependencies": rows,
            "pip_install": list(PIP_INSTALL_SPEC),
            "python": sys.version.split()[0]}


def assert_runtime_ready(mode: str = MODE_DESIGN) -> Dict[str, object]:
    """Stop *before* the stage runs when something it needs is absent.

    `wfdb` was missing on the first Leg 1 attempt and surfaced only when the
    replay reached its first `.atr`; `pyarrow` would have surfaced worse, at
    the end of a completed join while writing the bundle.  A stage now refuses
    to start instead.
    """
    report = check_runtime_dependencies(mode)
    if not report["ok"]:
        wanted = " ".join(PIP_INSTALL_SPEC)
        raise Q5DJoinError(
            f"stage {report['mode']} needs {report['missing']}, which "
            f"cannot be imported.  Install the pinned runtime first:\n"
            f"    pip install -q {wanted} pyarrow\n"
            f"Stopping before the stage starts, so nothing is read and no "
            f"partial run is produced.")
    return report


def build_env_pin() -> Dict[str, object]:
    """The versions actually loaded, for the run manifest."""
    out: Dict[str, object] = {"python": sys.version.split()[0],
                              "pip_install_spec": list(PIP_INSTALL_SPEC)}
    for name, (_purpose, registered) in sorted(RUNTIME_DEPENDENCIES.items()):
        try:
            module = __import__(name)
            version = getattr(module, "__version__", "unknown")
        except ImportError:
            version = None
        out[name] = {"version": version, "registered_runtime": registered or None}
    return out


def sha256_file(path: str) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 16), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _canonical_json(obj: object) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False)


def rule_fingerprint() -> str:
    """A hash of every constant that defines the frozen rule.

    A null distribution generated under one fingerprint may not be reused
    under another.  That is the whole point: relaxing the tolerance, changing
    the ledger or touching a gate must invalidate the null rather than inherit
    its cutoff.
    """
    payload = {
        "module_version": MODULE_VERSION,
        "fs": FS,
        "win_before": WIN_BEFORE,
        "win_after": WIN_AFTER,
        "min_valid_beats": MIN_VALID_BEATS,
        "aami_symbol_map": AAMI_SYMBOL_MAP,
        "rr_tolerance_samples": RR_TOLERANCE_SAMPLES,
        "matcher": "maximum_cardinality_monotone_forced_edges_only",
        "secondary_score": None,
        "cache_ledger": {s: list(CACHE_LEDGER[s]) for s in SPLITS},
        "mamba_count_delta": MAMBA_COUNT_DELTA,
        "controls": list(CONTROL_FAMILIES),
        "master_seed": MASTER_SEED,
        "bootstrap_seed": BOOTSTRAP_SEED,
        "gates": {
            "coverage_min": GATE_COVERAGE_MIN,
            "s_coverage_min": GATE_S_COVERAGE_MIN,
            "per_class_coverage_min": GATE_PER_CLASS_COVERAGE_MIN,
            "class_balance_min": GATE_CLASS_BALANCE_MIN,
            "record_coverage_min": GATE_RECORD_COVERAGE_MIN,
            "record_balance_min": GATE_RECORD_BALANCE_MIN,
            "agreement_overall_min": GATE_AGREEMENT_OVERALL_MIN,
            "agreement_per_class_min": GATE_AGREEMENT_PER_CLASS_MIN,
            "signal_to_null_min": GATE_SIGNAL_TO_NULL_MIN,
            "s_share_inflation_max": GATE_S_SHARE_INFLATION_MAX,
        },
    }
    return hashlib.sha256(_canonical_json(payload).encode("utf-8")).hexdigest()


# ─────────────────────────────────────────────────────────────────────────────
# Ledger
# ─────────────────────────────────────────────────────────────────────────────
class LedgerRecord(object):
    """One record's frozen slice in both lineages.

    ``cache_start`` is the registered start row of the record inside the
    split's cache/result array, and it *is* the physical offset there because
    ``data.py::load_split`` sorts within a split.

    ``mamba_start`` is the **logical** split-local coordinate
    (``mamba_split_start``), also a cumulative sum in the frozen split order.
    It is deliberately *not* the physical offset inside ``mamba_data.npz``:
    ``build_penult.py`` enumerates all 44 records at once, so the file
    interleaves DS1 and DS2.  The physical offset is measured from ``pid`` by
    :func:`load_mamba_sequences` and reported as ``mamba_file_row``.

    Both are arithmetic or measured consequences — never boundaries inferred
    from labels or from how well the join went.  The matcher uses neither; it
    works on record-local rows.
    """

    __slots__ = ("split", "record", "index", "cache_n", "cache_start",
                 "mamba_n", "mamba_start", "delta", "stratum")

    def __init__(self, split: str, record: str, index: int, cache_n: int,
                 cache_start: int, mamba_n: int, mamba_start: int) -> None:
        self.split = split
        self.record = record
        self.index = index
        self.cache_n = cache_n
        self.cache_start = cache_start
        self.mamba_n = mamba_n
        self.mamba_start = mamba_start
        self.delta = cache_n - mamba_n
        self.stratum = STRATUM_EQUAL if self.delta == 0 else STRATUM_MISMATCH

    @property
    def mamba_split_start(self) -> int:
        """The registered logical split-local coordinate (see the docstring)."""
        return self.mamba_start

    def as_dict(self) -> Dict[str, object]:
        return {"split": self.split, "record": self.record,
                "array_index": self.index, "cache_n": self.cache_n,
                "cache_start": self.cache_start, "mamba_n": self.mamba_n,
                "mamba_split_start": self.mamba_start,
                "count_difference": self.delta, "stratum": self.stratum}

    def __repr__(self) -> str:                          # pragma: no cover
        return (f"LedgerRecord({self.split} {self.record} "
                f"cache {self.cache_n}@{self.cache_start} "
                f"mamba {self.mamba_n}@{self.mamba_start} d={self.delta})")


def build_ledger() -> Dict[str, Tuple[LedgerRecord, ...]]:
    """Materialise the 44-record ledger from the registered constants."""
    out: Dict[str, Tuple[LedgerRecord, ...]] = {}
    for split in SPLITS:
        rows: List[LedgerRecord] = []
        cache_start = 0
        mamba_start = 0
        for index, (record, cache_n) in enumerate(CACHE_LEDGER[split]):
            mamba_n = cache_n - MAMBA_COUNT_DELTA.get(record, 0)
            rows.append(LedgerRecord(split, record, index, cache_n,
                                     cache_start, mamba_n, mamba_start))
            cache_start += cache_n
            mamba_start += mamba_n
        out[split] = tuple(rows)
    return out


def ledger_record(split: str, record: str) -> LedgerRecord:
    split = _check_split(split)
    for row in build_ledger()[split]:
        if row.record == str(record):
            return row
    raise Q5DJoinError(f"record {record!r} is not in the {split} ledger")


def verify_ledger() -> Dict[str, object]:
    """Check the ledger against every registered total before matching.

    A failure here is :data:`DECISION_INPUT_ABSENT`: the registered inputs do
    not support the specified mapping.  It is never a performance result.
    """
    ledger = build_ledger()
    problems: List[str] = []
    equal = mismatch = 0
    for split in SPLITS:
        rows = ledger[split]
        if len(rows) != len(REGISTERED_CACHE_STARTS[split]):
            problems.append(f"{split}: record count {len(rows)}")
        for row, registered in zip(rows, REGISTERED_CACHE_STARTS[split]):
            if row.cache_start != registered:
                problems.append(
                    f"{split} {row.record}: cache start {row.cache_start} != "
                    f"registered {registered}")
        cache_total = sum(r.cache_n for r in rows)
        mamba_total = sum(r.mamba_n for r in rows)
        if cache_total != REGISTERED_CACHE_TOTALS[split]:
            problems.append(f"{split}: cache total {cache_total} != "
                            f"{REGISTERED_CACHE_TOTALS[split]}")
        if mamba_total != REGISTERED_MAMBA_TOTALS[split]:
            problems.append(f"{split}: mamba total {mamba_total} != "
                            f"{REGISTERED_MAMBA_TOTALS[split]}")
        if cache_total - mamba_total != REGISTERED_COUNT_DIFFERENCE[split]:
            problems.append(f"{split}: difference {cache_total - mamba_total} "
                            f"!= {REGISTERED_COUNT_DIFFERENCE[split]}")
        equal += sum(1 for r in rows if r.stratum == STRATUM_EQUAL)
        mismatch += sum(1 for r in rows if r.stratum == STRATUM_MISMATCH)
    if equal != REGISTERED_EQUAL_COUNT_RECORDS:
        problems.append(f"equal-count records {equal} != "
                        f"{REGISTERED_EQUAL_COUNT_RECORDS}")
    if mismatch != REGISTERED_MISMATCHED_RECORDS:
        problems.append(f"mismatched records {mismatch} != "
                        f"{REGISTERED_MISMATCHED_RECORDS}")
    known = set(MAMBA_COUNT_DELTA)
    listed = {r.record for split in SPLITS for r in ledger[split]
              if r.stratum == STRATUM_MISMATCH}
    if known != listed:
        problems.append(f"mismatch set {sorted(listed)} != "
                        f"registered {sorted(known)}")
    return {
        "ok": not problems, "problems": problems,
        "records": equal + mismatch,
        "equal_count_records": equal, "mismatched_records": mismatch,
        "cache_total": sum(REGISTERED_CACHE_TOTALS.values()),
        "mamba_total": sum(REGISTERED_MAMBA_TOTALS.values()),
        "total_difference": sum(REGISTERED_COUNT_DIFFERENCE.values()),
        "rule_fingerprint": rule_fingerprint(),
    }


def verify_record_boundaries(observed: Mapping[str, Mapping[str, int]]
                             ) -> Dict[str, object]:
    """Compare observed cache/result boundaries against the frozen ledger.

    ``observed`` maps ``split -> {record: n}``.  This is how a real run proves
    the 44 cache and result-position record boundaries without inspecting a
    probability: the contiguous ``pid`` block length must equal the registered
    ``cache_n``.
    """
    ledger = build_ledger()
    problems: List[str] = []
    for split in SPLITS:
        rows = ledger[split]
        seen = observed.get(split, {})
        for row in rows:
            got = seen.get(row.record)
            if got is None:
                problems.append(f"{split} {row.record}: boundary not observed")
            elif int(got) != row.cache_n:
                problems.append(f"{split} {row.record}: observed {got} != "
                                f"registered {row.cache_n}")
        extra = sorted(set(seen) - {r.record for r in rows})
        if extra:
            problems.append(f"{split}: unregistered records {extra}")
    return {"ok": not problems, "problems": problems}


# ─────────────────────────────────────────────────────────────────────────────
# Units
# ─────────────────────────────────────────────────────────────────────────────
def to_samples(value: float, unit: str) -> int:
    """Convert one declared RR value to integer 360 Hz samples.

    Round-half-to-even, which is what Python's :func:`round` already does for
    floats.  The unit comes from the artifact's declaration and nowhere else:
    there is no fitted scale, no record-specific scale search, and no
    "try both and keep the one with more matches".
    """
    u = str(unit).strip().lower()
    if u == UNIT_SAMPLES:
        scaled = float(value)
    elif u == UNIT_SECONDS:
        scaled = float(value) * FS
    else:
        raise Q5DJoinError(
            f"undeclared or unknown RR unit {unit!r}; declare one of "
            f"{DECLARED_UNITS}.  A unit scale is never estimated by picking "
            f"the value that creates the most matches.")
    return int(round(scaled))


def rr_to_samples(values: Sequence[float], unit: str) -> Tuple[int, ...]:
    return tuple(to_samples(v, unit) for v in values)


def check_declared_unit(unit: str, values: Sequence[float]) -> str:
    """Accept the declaration; refuse a declaration that cannot be true.

    This is deliberately *not* unit inference.  It only catches an
    unambiguously wrong declaration — RR in seconds is physiological around
    0.2-3.0 s, so a "seconds" array whose median is in the hundreds is a
    mislabelled samples array.  The response is to stop, never to rescale.
    """
    u = str(unit).strip().lower()
    if u not in DECLARED_UNITS:
        raise Q5DJoinError(
            f"undeclared or unknown RR unit {unit!r}; declare one of "
            f"{DECLARED_UNITS}")
    if not values:
        return u
    ordered = sorted(float(v) for v in values)
    median = ordered[len(ordered) // 2]
    if u == UNIT_SECONDS and not (0.05 <= median <= 10.0):
        raise Q5DJoinError(
            f"RR declared in {UNIT_SECONDS!r} but the median is {median:g}: "
            f"the declaration contradicts the artifact.  Stopping — a scale "
            f"is never fitted to make the join work.")
    if u == UNIT_SAMPLES and median < 18.0:
        raise Q5DJoinError(
            f"RR declared in {UNIT_SAMPLES!r} but the median is {median:g} "
            f"(< 0.05 s at {FS:g} Hz): the declaration contradicts the "
            f"artifact.  Stopping — a scale is never fitted.")
    return u


# ─────────────────────────────────────────────────────────────────────────────
# Leg 1 — deterministic `.atr` -> mamba source replay
# ─────────────────────────────────────────────────────────────────────────────
class Leg1Record(object):
    """The replayed mamba slice for one record, plus its full drop audit."""

    __slots__ = ("record", "split", "kept", "dropped", "record_dropped",
                 "pre_seconds", "post_seconds", "pre_samples", "post_samples")

    def __init__(self, record: str, split: str) -> None:
        self.record = record
        self.split = split
        self.kept: List[Dict[str, object]] = []
        self.dropped: List[Dict[str, object]] = []
        self.record_dropped = False
        self.pre_seconds: Tuple[float, ...] = ()
        self.post_seconds: Tuple[float, ...] = ()
        self.pre_samples: Tuple[int, ...] = ()
        self.post_samples: Tuple[int, ...] = ()

    @property
    def n(self) -> int:
        return len(self.kept)

    def as_dict(self) -> Dict[str, object]:
        return {"record": self.record, "split": self.split, "n": self.n,
                "record_dropped": self.record_dropped,
                "dropped_beats": len(self.dropped)}


def replay_leg1_record(record: str, split: str,
                       annotations: Sequence[Tuple[int, str]],
                       signal_length: int) -> Leg1Record:
    """Replay the three frozen mamba rules from raw ``.atr`` annotations.

    ``annotations`` is ``(pos, symbol)`` in ``.atr`` sample order; ``.atr``
    order is preserved and nothing is re-sorted, re-ranked or permuted.

    The rules, in the source's own order
    (`mit-bih/lineage/v15b_local.py` :101-109):

    1. keep only symbols in the registered N/S/V map — ``F`` and ``Q`` are not
       in it, which is the entire 818-beat Q5-B-0 drop map;
    2. keep only ``WIN_BEFORE <= pos < signal_length - WIN_AFTER``, the
       150-sample boundary test **on annotation position** ``pos``;
    3. drop the whole record if fewer than :data:`MIN_VALID_BEATS` survive.

    RR is then recomputed *after* filtering, in seconds, with the endpoints
    duplicated::

        d    = diff(kept_r_samples) / FS
        pre  = [d[0]] + d              # pre[0] duplicates the first interval
        post = pre[1:] + [pre[-1]]     # post[-1] duplicates the last interval

    So the first and last beats have RR on both sides and are **eligible**.
    An earlier draft assumed they were ineligible; the source says otherwise.
    """
    split = _check_split(split)
    out = Leg1Record(str(record), split)
    positions: List[int] = []
    last_pos: Optional[int] = None
    for ordinal, (pos, symbol) in enumerate(annotations):
        pos = int(pos)
        if last_pos is not None and pos < last_pos:
            raise Q5DJoinError(
                f"record {record}: annotation {ordinal} at sample {pos} is "
                f"before annotation {ordinal - 1} at {last_pos}; `.atr` "
                f"sample order must be preserved, not re-sorted")
        last_pos = pos
        entry = {"raw_atr_ordinal": ordinal, "raw_r_sample": pos,
                 "symbol": str(symbol),
                 "aami": AAMI_SYMBOL_MAP.get(str(symbol), "")}
        if str(symbol) not in AAMI_SYMBOL_MAP:
            entry["reason"] = REASON_SYMBOL
            out.dropped.append(entry)
            continue
        if not (WIN_BEFORE <= pos < int(signal_length) - WIN_AFTER):
            entry["reason"] = REASON_BOUNDARY
            out.dropped.append(entry)
            continue
        entry["reason"] = REASON_NONE
        out.kept.append(entry)
        positions.append(pos)

    if len(out.kept) < MIN_VALID_BEATS:
        for entry in out.kept:
            entry["reason"] = REASON_TOO_FEW
        out.dropped.extend(out.kept)
        out.kept = []
        out.record_dropped = True
        return out

    diffs = [(positions[i + 1] - positions[i]) / FS
             for i in range(len(positions) - 1)]
    pre = [diffs[0]] + diffs                      # length n
    post = pre[1:] + [pre[-1]]                    # length n
    out.pre_seconds = tuple(pre)
    out.post_seconds = tuple(post)
    out.pre_samples = rr_to_samples(pre, UNIT_SECONDS)
    out.post_samples = rr_to_samples(post, UNIT_SECONDS)
    for row, (entry, pre_s, post_s) in enumerate(
            zip(out.kept, out.pre_samples, out.post_samples)):
        entry["mamba_record_row"] = row
        entry["pre_samples"] = pre_s
        entry["post_samples"] = post_s
    return out


def audit_leg1_against_ledger(replayed: Mapping[str, Leg1Record],
                              split: str,
                              stored_rr: Optional[Mapping[str, Mapping[
                                  str, Sequence[float]]]] = None,
                              rr_unit: str = UNIT_SECONDS,
                              rr_atol_samples: int = 0) -> Dict[str, object]:
    """Compare a Leg 1 replay against the committed mamba ledger.

    Checks per-record count, split total, ordinal order and — when the stored
    RR is supplied — every stored RR value within the declared serialization
    tolerance.  Any mismatch is :data:`DECISION_RULE_FALSIFIED` with
    ``failed_leg = LEG1_SOURCE_REPLAY``, and Leg 2 must not start.
    """
    split = _check_split(split)
    rows = build_ledger()[split]
    problems: List[str] = []
    per_record: List[Dict[str, object]] = []
    total = 0
    for row in rows:
        got = replayed.get(row.record)
        if got is None:
            problems.append(f"{split} {row.record}: not replayed")
            per_record.append({"record": row.record, "expected": row.mamba_n,
                               "observed": None, "ok": False})
            continue
        total += got.n
        ok = got.n == row.mamba_n
        if not ok:
            problems.append(f"{split} {row.record}: replayed {got.n} beats != "
                            f"ledger {row.mamba_n}")
        ordinals = [int(e["raw_atr_ordinal"]) for e in got.kept]
        if ordinals != sorted(ordinals):
            ok = False
            problems.append(f"{split} {row.record}: `.atr` ordinal order lost")
        samples = [int(e["raw_r_sample"]) for e in got.kept]
        if any(b <= a for a, b in zip(samples, samples[1:])):
            ok = False
            problems.append(f"{split} {row.record}: R samples not strictly "
                            f"increasing after filtering")
        rr_problems = 0
        if stored_rr is not None and row.record in stored_rr:
            stored = stored_rr[row.record]
            check_declared_unit(rr_unit, list(stored.get("pre", ())))
            for name, replayed_samples in (("pre", got.pre_samples),
                                           ("post", got.post_samples)):
                values = stored.get(name)
                if values is None:
                    problems.append(f"{split} {row.record}: stored {name}-RR "
                                    f"absent")
                    ok = False
                    continue
                stored_samples = rr_to_samples(values, rr_unit)
                if len(stored_samples) != len(replayed_samples):
                    problems.append(
                        f"{split} {row.record}: stored {name}-RR length "
                        f"{len(stored_samples)} != replayed "
                        f"{len(replayed_samples)}")
                    ok = False
                    continue
                bad = sum(1 for a, b in zip(stored_samples, replayed_samples)
                          if abs(a - b) > rr_atol_samples)
                rr_problems += bad
                if bad:
                    ok = False
                    problems.append(f"{split} {row.record}: {bad} {name}-RR "
                                    f"values outside the declared tolerance")
        per_record.append({"record": row.record, "expected": row.mamba_n,
                           "observed": got.n, "dropped": len(got.dropped),
                           "record_dropped": got.record_dropped,
                           "rr_mismatches": rr_problems, "ok": ok})
    if total != REGISTERED_MAMBA_TOTALS[split]:
        problems.append(f"{split}: replayed total {total} != ledger "
                        f"{REGISTERED_MAMBA_TOTALS[split]}")
    return {"ok": not problems, "split": split, "problems": problems,
            "per_record": per_record, "replayed_total": total,
            "expected_total": REGISTERED_MAMBA_TOTALS[split],
            "failed_leg": None if not problems else LEG1,
            "decision": None if not problems else DECISION_RULE_FALSIFIED}


# ─────────────────────────────────────────────────────────────────────────────
# Leg 2 — record-wise maximum-cardinality monotone matching
# ─────────────────────────────────────────────────────────────────────────────
class RecordSequence(object):
    """One record's RR pairs, already in integer samples, in row order.

    ``rows`` carries whatever audit payload the caller wants to keep beside
    each row (raw ordinal, symbol, class).  The matcher never looks at it —
    beat symbols and labels do not enter candidate construction.
    """

    __slots__ = ("record", "split", "side", "pre_samples", "post_samples",
                 "rows")

    def __init__(self, record: str, split: str, side: str,
                 pre_samples: Sequence[int], post_samples: Sequence[int],
                 rows: Optional[Sequence[Mapping[str, object]]] = None) -> None:
        if len(pre_samples) != len(post_samples):
            raise Q5DJoinError(
                f"{side} {record}: pre/post length mismatch "
                f"{len(pre_samples)} vs {len(post_samples)}")
        self.record = str(record)
        self.split = _check_split(split)
        self.side = str(side)
        self.pre_samples = tuple(int(v) for v in pre_samples)
        self.post_samples = tuple(int(v) for v in post_samples)
        self.rows = tuple(dict(r) for r in (rows or ()))
        if self.rows and len(self.rows) != len(self.pre_samples):
            raise Q5DJoinError(
                f"{side} {record}: {len(self.rows)} audit rows for "
                f"{len(self.pre_samples)} beats")

    def __len__(self) -> int:
        return len(self.pre_samples)


class _PrefixMax(object):
    """Fenwick tree over 1..size holding a prefix maximum.

    This is the machinery behind the forced-edge test: it turns the
    prefix/suffix chain-length DP into O(E log E) instead of enumerating
    optimal matchings, which the spec forbids and which is exponential anyway.
    """

    __slots__ = ("size", "tree")

    def __init__(self, size: int) -> None:
        self.size = size
        self.tree = [0] * (size + 1)

    def update(self, index: int, value: int) -> None:
        i = index
        while i <= self.size:
            if self.tree[i] < value:
                self.tree[i] = value
            i += i & (-i)

    def query(self, index: int) -> int:
        best = 0
        i = index
        while i > 0:
            if self.tree[i] > best:
                best = self.tree[i]
            i -= i & (-i)
        return best


def candidate_edges(mamba: RecordSequence, cache: RecordSequence
                    ) -> Tuple[Tuple[int, int], ...]:
    """Every ``(i, j)`` satisfying the one fixed candidate rule.

    Both differences must be within :data:`RR_TOLERANCE_SAMPLES` integer 360 Hz
    samples.  One sample is the tolerance because both artifacts ultimately
    refer to the same discrete signal; it is not widened when RR patterns
    repeat, and there is no local-margin rule.
    """
    if mamba.record != cache.record or mamba.split != cache.split:
        raise Q5DJoinError(
            f"cross-record matching is not permitted: mamba "
            f"{mamba.split}/{mamba.record} vs cache "
            f"{cache.split}/{cache.record}.  Every mapping is record-local.")
    tol = RR_TOLERANCE_SAMPLES
    index: Dict[Tuple[int, int], List[int]] = {}
    for j, (pre, post) in enumerate(zip(cache.pre_samples,
                                        cache.post_samples)):
        index.setdefault((pre, post), []).append(j)
    edges: List[Tuple[int, int]] = []
    for i, (pre, post) in enumerate(zip(mamba.pre_samples,
                                        mamba.post_samples)):
        found: List[int] = []
        for dp in range(-tol, tol + 1):
            for dq in range(-tol, tol + 1):
                found.extend(index.get((pre + dp, post + dq), ()))
        for j in sorted(set(found)):
            edges.append((i, j))
    edges.sort()
    return tuple(edges)


class MatchResult(object):
    """The outcome of one record's matcher run."""

    __slots__ = ("record", "split", "n_mamba", "n_cache", "max_cardinality",
                 "certified", "ambiguous", "edges", "rank_class_sizes")

    def __init__(self, record: str, split: str, n_mamba: int, n_cache: int,
                 max_cardinality: int,
                 certified: Sequence[Tuple[int, int]],
                 ambiguous: Sequence[Tuple[int, int]],
                 edges: Sequence[Tuple[int, int]],
                 rank_class_sizes: Mapping[int, int]) -> None:
        self.record = record
        self.split = split
        self.n_mamba = n_mamba
        self.n_cache = n_cache
        self.max_cardinality = max_cardinality
        self.certified = tuple(certified)
        self.ambiguous = tuple(ambiguous)
        self.edges = tuple(edges)
        self.rank_class_sizes = dict(rank_class_sizes)

    @property
    def certified_count(self) -> int:
        return len(self.certified)

    def as_dict(self) -> Dict[str, object]:
        return {"record": self.record, "split": self.split,
                "n_mamba": self.n_mamba, "n_cache": self.n_cache,
                "candidate_edges": len(self.edges),
                "max_cardinality": self.max_cardinality,
                "certified": self.certified_count,
                "ambiguous": len(self.ambiguous)}


def match_record(mamba: RecordSequence, cache: RecordSequence) -> MatchResult:
    """Certify only the edges common to *every* maximum monotone matching.

    How the forced-edge test works, without enumerating anything:

    ``L(e)`` is the longest strictly-increasing chain of candidate edges
    ending at ``e``; ``R(e)`` is the longest chain starting at ``e``.  The
    maximum cardinality is ``M = max L``.  An edge lies in **some** maximum
    matching iff ``L(e) + R(e) - 1 == M``.

    For such an edge, its position inside any maximum matching containing it
    is forced to be ``L(e)``: a maximum matching through ``e`` at position
    ``k`` has ``k - 1 <= L(e) - 1`` edges before it and ``M - k <= R(e) - 1``
    after it, and those two inequalities sum to ``M - 1 <= M - 1``, so both
    are tight.  Every maximum matching therefore holds exactly one edge of
    each rank ``1..M``.

    Hence ``e`` is in **every** maximum matching iff no other usable edge
    shares its rank.  Singleton rank class -> ``CERTIFIED``; a rank class with
    two or more members -> all of them ``AMBIGUOUS``, and they stay unmatched.
    No arbitrary optimal path is ever promoted, and there is no secondary
    score, distance preference, label preference or record-specific penalty to
    break the tie with.
    """
    edges = candidate_edges(mamba, cache)
    n_mamba, n_cache = len(mamba), len(cache)
    if not edges:
        return MatchResult(mamba.record, mamba.split, n_mamba, n_cache,
                           0, (), (), (), {})

    # L(e): longest chain ending at e.  Process i ascending; the tree holds
    # only edges with a strictly smaller i, so monotonicity is enforced on
    # both coordinates at once.
    forward = _PrefixMax(n_cache + 1)
    chain_end: Dict[Tuple[int, int], int] = {}
    pos = 0
    while pos < len(edges):
        row = edges[pos][0]
        group = []
        while pos < len(edges) and edges[pos][0] == row:
            group.append(edges[pos])
            pos += 1
        for edge in group:
            chain_end[edge] = forward.query(edge[1]) + 1
        for edge in group:
            forward.update(edge[1] + 1, chain_end[edge])

    # R(e): longest chain starting at e.  Same walk, mirrored.
    backward = _PrefixMax(n_cache + 1)
    chain_start: Dict[Tuple[int, int], int] = {}
    pos = len(edges) - 1
    while pos >= 0:
        row = edges[pos][0]
        group = []
        while pos >= 0 and edges[pos][0] == row:
            group.append(edges[pos])
            pos -= 1
        for edge in group:
            mirrored = n_cache - edge[1]          # 1..n_cache, order reversed
            chain_start[edge] = backward.query(mirrored - 1) + 1
        for edge in group:
            backward.update(n_cache - edge[1], chain_start[edge])

    max_cardinality = max(chain_end.values())
    by_rank: Dict[int, List[Tuple[int, int]]] = {}
    for edge in edges:
        if chain_end[edge] + chain_start[edge] - 1 != max_cardinality:
            continue                                # in no maximum matching
        by_rank.setdefault(chain_end[edge], []).append(edge)

    certified: List[Tuple[int, int]] = []
    ambiguous: List[Tuple[int, int]] = []
    for rank in sorted(by_rank):
        members = by_rank[rank]
        if len(members) == 1:
            certified.append(members[0])
        else:
            ambiguous.extend(members)
    certified.sort()
    ambiguous.sort()
    _assert_monotone_one_to_one(certified, mamba.record)
    return MatchResult(mamba.record, mamba.split, n_mamba, n_cache,
                       max_cardinality, certified, ambiguous, edges,
                       {r: len(v) for r, v in by_rank.items()})


def _assert_monotone_one_to_one(edges: Sequence[Tuple[int, int]],
                                record: str) -> None:
    """Certified maps are strictly monotone and one-to-one, or nothing ships."""
    for (i0, j0), (i1, j1) in zip(edges, edges[1:]):
        if not (i1 > i0 and j1 > j0):
            raise Q5DJoinError(
                f"record {record}: certified edges ({i0},{j0}) and ({i1},{j1}) "
                f"are not strictly monotone in both sequences")
    if len({i for i, _ in edges}) != len(edges) or \
            len({j for _, j in edges}) != len(edges):
        raise Q5DJoinError(f"record {record}: certified map is not one-to-one")


def join_record(mamba: RecordSequence, cache: RecordSequence,
                ledger: Optional[LedgerRecord] = None
                ) -> Tuple[MatchResult, List[Dict[str, object]]]:
    """Match one record and emit its join-map rows.

    Every row of both sequences appears exactly once in the output: certified
    pairs, ambiguous rows, and unmatched rows with the reason they are
    unmatched.  Nothing is imputed — an unmatched V9/V10 row stays unmapped
    and counts against coverage, and an unmatched mamba row is reported with
    its Leg 1 identity.
    """
    result = match_record(mamba, cache)
    led = ledger or ledger_record(mamba.split, mamba.record)
    certified_by_i = {i: j for i, j in result.certified}
    certified_by_j = {j: i for i, j in result.certified}
    ambiguous_i = {i for i, _ in result.ambiguous}
    ambiguous_j = {j for _, j in result.ambiguous}
    with_edge_i = {i for i, _ in result.edges}
    with_edge_j = {j for _, j in result.edges}

    rows: List[Dict[str, object]] = []
    for i in range(len(mamba)):
        audit = dict(mamba.rows[i]) if mamba.rows else {}
        j = certified_by_i.get(i)
        if j is not None:
            status, reason = STATUS_CERTIFIED, REASON_NONE
        elif i in ambiguous_i:
            status, reason = STATUS_AMBIGUOUS, REASON_AMBIGUOUS
        elif i in with_edge_i:
            status, reason = STATUS_UNMATCHED, REASON_NOT_OPTIMAL
        else:
            status, reason = STATUS_UNMATCHED, REASON_NO_EDGE
        rows.append({
            "split": mamba.split,
            "record": mamba.record,
            "raw_atr_ordinal": audit.get("raw_atr_ordinal"),
            "raw_r_sample": audit.get("raw_r_sample"),
            "mamba_record_row": i,
            # Two enumerations of the same row, kept apart on purpose:
            # the ledger's logical split-local coordinate, and the physical
            # offset measured from the stored `pid` array.
            "mamba_global_row": led.mamba_start + i,
            "mamba_file_row": audit.get("mamba_file_row"),
            "cache_record_row": j,
            "result_global_row": None if j is None else led.cache_start + j,
            "status": status,
            "pre_rr_difference_samples": (
                None if j is None
                else mamba.pre_samples[i] - cache.pre_samples[j]),
            "post_rr_difference_samples": (
                None if j is None
                else mamba.post_samples[i] - cache.post_samples[j]),
            "failed_leg": None if status == STATUS_CERTIFIED else LEG2,
            "drop_or_unmatched_reason": reason,
        })
    # V9/V10 rows with no certified partner.  These are the coverage
    # denominator's misses, so they are reported, never imputed.
    for j in range(len(cache)):
        if j in certified_by_j:
            continue
        if j in ambiguous_j:
            status, reason = STATUS_AMBIGUOUS, REASON_AMBIGUOUS
        elif j in with_edge_j:
            status, reason = STATUS_UNMATCHED, REASON_NOT_OPTIMAL
        else:
            status, reason = STATUS_UNMATCHED, REASON_NO_EDGE
        rows.append({
            "split": cache.split, "record": cache.record,
            "raw_atr_ordinal": None, "raw_r_sample": None,
            "mamba_record_row": None, "mamba_global_row": None,
            "mamba_file_row": None, "cache_record_row": j,
            "result_global_row": led.cache_start + j,
            "status": status,
            "pre_rr_difference_samples": None,
            "post_rr_difference_samples": None,
            "failed_leg": LEG2, "drop_or_unmatched_reason": reason,
        })
    for row in rows:
        validate_join_map_row(row)
    return result, rows


def join_split(mamba_by_record: Mapping[str, RecordSequence],
               cache_by_record: Mapping[str, RecordSequence],
               split: str) -> Dict[str, object]:
    """Run Leg 2 over one split, record by record.

    Global order-preserving alignment is forbidden and structurally impossible
    here: each record is cut from the ledger and matched on its own, so a
    deficit in 105, 111 or 222 cannot shift any later record.
    """
    split = _check_split(split)
    rows_out: List[Dict[str, object]] = []
    results: List[MatchResult] = []
    for led in build_ledger()[split]:
        mamba = mamba_by_record.get(led.record)
        cache = cache_by_record.get(led.record)
        if mamba is None or cache is None:
            raise Q5DJoinError(
                f"{DECISION_INPUT_ABSENT}: {split} {led.record} missing from "
                f"{'mamba' if mamba is None else 'cache'} input")
        if len(cache) != led.cache_n:
            raise Q5DJoinError(
                f"{split} {led.record}: cache slice {len(cache)} != registered "
                f"{led.cache_n}; record boundaries come from the ledger, not "
                f"from the data")
        if len(mamba) != led.mamba_n:
            raise Q5DJoinError(
                f"{split} {led.record}: mamba slice {len(mamba)} != registered "
                f"{led.mamba_n}")
        result, rows = join_record(mamba, cache, led)
        results.append(result)
        rows_out.extend(rows)
    return {"split": split, "results": results, "rows": rows_out,
            "certified": sum(r.certified_count for r in results),
            "cache_rows": sum(r.n_cache for r in results)}


def validate_join_map_row(row: Mapping[str, object]) -> None:
    """Schema check.  A probability column never reaches a join map."""
    missing = [f for f in JOIN_MAP_FIELDS if f not in row]
    if missing:
        raise Q5DJoinError(f"join-map row missing fields {missing}")
    banned = sorted({k for k in row
                     if str(k).lower() in JOIN_MAP_BANNED_FIELDS})
    if banned:
        raise Q5DJoinError(
            f"join-map row carries {banned}: the join map holds stable IDs "
            f"and audit fields only.  V10 probability values are sealed.")
    if row["status"] not in STATUSES:
        raise Q5DJoinError(f"unknown join status {row['status']!r}")
    if row["drop_or_unmatched_reason"] not in REASONS:
        raise Q5DJoinError(
            f"unknown reason {row['drop_or_unmatched_reason']!r}")
    if row["failed_leg"] not in (None,) + LEGS:
        raise Q5DJoinError(f"unknown failed_leg {row['failed_leg']!r}")


# ─────────────────────────────────────────────────────────────────────────────
# Coverage, agreement and the primary statistic
# ─────────────────────────────────────────────────────────────────────────────
def coverage_report(rows: Sequence[Mapping[str, object]],
                    processed_classes: Mapping[Tuple[str, int], str],
                    mamba_classes: Optional[Mapping[Tuple[str, int], str]] = None
                    ) -> Dict[str, object]:
    """Per-class and per-record certified coverage, plus class agreement.

    ``processed_classes`` maps ``(record, cache_record_row) -> class`` — the
    V9/V10 positional row's class, which is the denominator.  ``processed``
    here never means a mamba row.  ``mamba_classes`` maps
    ``(record, mamba_record_row) -> class`` and is used only to audit agreement
    among certified pairs; class agreement never enters the join.
    """
    per_class_total = {c: 0 for c in AAMI_CLASSES}
    per_class_certified = {c: 0 for c in AAMI_CLASSES}
    per_class_agree = {c: 0 for c in AAMI_CLASSES}
    per_record: Dict[str, Dict[str, int]] = {}

    for (record, _row), cls in processed_classes.items():
        if cls in per_class_total:
            per_class_total[cls] += 1
        bucket = per_record.setdefault(record, {"total": 0, "certified": 0})
        bucket["total"] += 1

    agree_total = agree_hits = 0
    for row in rows:
        if row["status"] != STATUS_CERTIFIED:
            continue
        record = str(row["record"])
        j = row["cache_record_row"]
        if j is None:
            continue
        cls = processed_classes.get((record, int(j)))
        if cls in per_class_certified:
            per_class_certified[cls] += 1
        bucket = per_record.setdefault(record, {"total": 0, "certified": 0})
        bucket["certified"] += 1
        if mamba_classes is not None and row["mamba_record_row"] is not None:
            raw = mamba_classes.get((record, int(row["mamba_record_row"])))
            if raw is not None and cls is not None:
                agree_total += 1
                if raw == cls:
                    agree_hits += 1
                    if cls in per_class_agree:
                        per_class_agree[cls] += 1

    overall_total = sum(per_class_total.values())
    overall_certified = sum(per_class_certified.values())
    class_coverage = {c: _ratio(per_class_certified[c], per_class_total[c])
                      for c in AAMI_CLASSES}
    overall_coverage = _ratio(overall_certified, overall_total)
    record_coverage = {r: _ratio(v["certified"], v["total"])
                       for r, v in per_record.items()}
    covered = [record_coverage[r] for r in sorted(record_coverage)
               if per_record[r]["total"] > 0]
    class_agreement = {
        c: _ratio(per_class_agree[c], per_class_certified[c])
        for c in AAMI_CLASSES}
    return {
        "class_total": per_class_total,
        "class_certified": per_class_certified,
        "class_coverage": class_coverage,
        "overall_total": overall_total,
        "overall_certified": overall_certified,
        "overall_coverage": overall_coverage,
        "class_coverage_balance": _ratio(min(class_coverage.values()),
                                         overall_coverage)
        if overall_coverage else 0.0,
        "record_coverage": record_coverage,
        "record_macro_coverage": _mean(covered),
        "record_p10_coverage": percentile(covered, 10.0),
        "record_coverage_balance": _ratio(percentile(covered, 10.0),
                                          _mean(covered)) if covered else 0.0,
        "agreement_overall": _ratio(agree_hits, agree_total),
        "agreement_by_class": class_agreement,
        "agreement_pairs": agree_total,
    }


def j_min(rows: Sequence[Mapping[str, object]],
          processed_classes: Mapping[Tuple[str, int], str],
          mamba_classes: Mapping[Tuple[str, int], str]) -> float:
    """``min`` over the three per-class correct recalls.

    ``correct_recall_c`` counts certified pairs whose carried Leg 1 class
    *agrees* with the processed class ``c``, over all processed beats of class
    ``c``.  The minimum is taken so a dominant N class cannot hide the loss of
    S or V beats — the Q5-B-0 lesson, kept.
    """
    totals = {c: 0 for c in AAMI_CLASSES}
    hits = {c: 0 for c in AAMI_CLASSES}
    for (_record, _row), cls in processed_classes.items():
        if cls in totals:
            totals[cls] += 1
    for row in rows:
        if row["status"] != STATUS_CERTIFIED:
            continue
        j, i = row["cache_record_row"], row["mamba_record_row"]
        if j is None or i is None:
            continue
        key_processed = (str(row["record"]), int(j))
        key_mamba = (str(row["record"]), int(i))
        cls = processed_classes.get(key_processed)
        raw = mamba_classes.get(key_mamba)
        if cls in hits and raw == cls:
            hits[cls] += 1
    return min(_ratio(hits[c], totals[c]) for c in AAMI_CLASSES)


def s_share_inflation(rows: Sequence[Mapping[str, object]],
                      processed_classes: Mapping[Tuple[str, int], str]
                      ) -> Dict[str, float]:
    """Gate 12, source-relative.

    ``(record share of certified S) / (record share of all processed S)``.
    It asks whether certification *concentrated* S beats further — not whether
    a patient genuinely has many of them.  Record 232 already supplies 75.2% of
    DS2 S beats before any join; that is source concentration, and this gate
    neither repairs it nor substitutes for the parent's absolute 50% ceiling.
    """
    source: Dict[str, int] = {}
    certified: Dict[str, int] = {}
    for (record, _row), cls in processed_classes.items():
        if cls == "S":
            source[record] = source.get(record, 0) + 1
    for row in rows:
        if row["status"] != STATUS_CERTIFIED or row["cache_record_row"] is None:
            continue
        record = str(row["record"])
        if processed_classes.get((record, int(row["cache_record_row"]))) == "S":
            certified[record] = certified.get(record, 0) + 1
    source_total = sum(source.values())
    certified_total = sum(certified.values())
    out: Dict[str, float] = {}
    for record, count in sorted(source.items()):
        source_share = _ratio(count, source_total)
        certified_share = _ratio(certified.get(record, 0), certified_total)
        out[record] = _ratio(certified_share, source_share)
    return out


def _ratio(numerator: float, denominator: float) -> float:
    return float(numerator) / float(denominator) if denominator else 0.0


def _mean(values: Sequence[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def percentile(values: Sequence[float], pct: float) -> float:
    """Linear-interpolation percentile, matching ``numpy.percentile`` default.

    Written out so the statistic does not depend on numpy being importable in
    whatever environment reads a bundle.
    """
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


# ─────────────────────────────────────────────────────────────────────────────
# Negative controls and the empirical null
# ─────────────────────────────────────────────────────────────────────────────
def _rng(family: str, replicate: int) -> random.Random:
    """Deterministic per-replicate stream, seeded from a stable string.

    :meth:`random.Random.seed` hashes a string with SHA-512, so this is stable
    across processes and unaffected by ``PYTHONHASHSEED`` — which matters when
    the null has to be reproducible from a seed written into a manifest.
    """
    return random.Random(f"{MASTER_SEED}|{family}|{int(replicate)}")


def length_quintiles(records: Sequence[Tuple[str, int]]
                     ) -> List[List[str]]:
    """Frozen record-length bins for the wrong-record control.

    Bins are coarsened deterministically until every bin can be deranged; a
    bin with fewer than two records is merged with its neighbour rather than
    dropped.  Records are never dropped to make a control work.
    """
    ordered = sorted(records, key=lambda rc: (rc[1], rc[0]))
    if not ordered:
        return []
    bins = max(1, min(WRONG_RECORD_QUINTILES, len(ordered)))
    while bins > 1:
        grouped: List[List[str]] = [[] for _ in range(bins)]
        for position, (record, _n) in enumerate(ordered):
            grouped[min(position * bins // len(ordered), bins - 1)].append(
                record)
        grouped = [g for g in grouped if g]
        if all(len(g) >= 2 for g in grouped):
            return grouped
        bins -= 1
    return [[r for r, _n in ordered]]


def derange_within_bins(bins: Sequence[Sequence[str]], replicate: int
                        ) -> Dict[str, str]:
    """Wrong-record control: no record keeps its own partner.

    Falsifies the possibility that a common RR distribution alone makes the
    join look successful.

    A record in a bin of fewer than two records is **omitted** from the
    mapping, not mapped to itself.  `length_quintiles` coarsens the binning
    first, so this only happens when a whole split has one record — and there
    the spec says the control is *skipped*.  Mapping such a record to itself
    would quietly feed a copy of TRUE into the null, which is exactly the kind
    of contaminated control this design exists to prevent.  Use
    :func:`wrong_record_skipped` to report what was left out.
    """
    rng = _rng(CONTROL_WRONG_RECORD, replicate)
    mapping: Dict[str, str] = {}
    for group in bins:
        members = list(group)
        if len(members) < 2:
            continue
        shuffled = list(members)
        for _attempt in range(64):
            rng.shuffle(shuffled)
            if all(a != b for a, b in zip(members, shuffled)):
                break
        else:                                          # pragma: no cover
            shuffled = members[1:] + members[:1]
        mapping.update(dict(zip(members, shuffled)))
    return mapping


def wrong_record_skipped(bins: Sequence[Sequence[str]]) -> List[str]:
    """Records the wrong-record control cannot cover, reported not hidden."""
    return sorted(r for group in bins if len(group) < 2 for r in group)


def shuffle_within_record(sequence: RecordSequence, replicate: int
                          ) -> RecordSequence:
    """Order-shuffle control: permute complete RR *pairs* inside the record.

    The pair travels with its audit payload, so the multiset of RR pairs is
    preserved exactly and only chronology is destroyed.  Falsifies a join that
    the multiset alone could explain.
    """
    rng = _rng(CONTROL_ORDER_SHUFFLE, replicate)
    order = list(range(len(sequence)))
    rng.shuffle(order)
    return _reindex(sequence, order)


def circular_shift_within_record(sequence: RecordSequence, replicate: int
                                 ) -> RecordSequence:
    """Circular-shift control: a non-zero within-record rotation.

    Offsets are drawn uniformly from ``1..n-1``, so the shift is never the
    identity.  This preserves local autocorrelation far better than a full
    shuffle and falsifies a join driven by repetitive rhythm rather than by
    exact beat position.
    """
    n = len(sequence)
    if n < 2:
        return _reindex(sequence, list(range(n)))
    rng = _rng(CONTROL_CIRCULAR_SHIFT, replicate)
    offset = rng.randrange(1, n)
    order = [(k + offset) % n for k in range(n)]
    return _reindex(sequence, order)


def _reindex(sequence: RecordSequence, order: Sequence[int]) -> RecordSequence:
    return RecordSequence(
        sequence.record, sequence.split, sequence.side,
        [sequence.pre_samples[k] for k in order],
        [sequence.post_samples[k] for k in order],
        [sequence.rows[k] for k in order] if sequence.rows else None)


def apply_control(family: str, mamba_by_record: Mapping[str, RecordSequence],
                  replicate: int) -> Dict[str, RecordSequence]:
    """Transform the raw side only.  Leg 1 stays fixed and already passed.

    Nothing but ``SEQUENCE_RELATIONSHIP`` changes: each control then reruns the
    *complete* Leg 2 candidate construction, matching, certification and audit
    statistics.  There is no shortcut that reuses the true matching.
    """
    if family not in CONTROL_FAMILIES:
        raise Q5DJoinError(f"unknown control family {family!r}; registered "
                           f"families are {CONTROL_FAMILIES}")
    if family == CONTROL_ORDER_SHUFFLE:
        return {r: shuffle_within_record(s, replicate)
                for r, s in mamba_by_record.items()}
    if family == CONTROL_CIRCULAR_SHIFT:
        return {r: circular_shift_within_record(s, replicate)
                for r, s in mamba_by_record.items()}
    bins = length_quintiles([(r, len(s)) for r, s in mamba_by_record.items()])
    mapping = derange_within_bins(bins, replicate)
    skipped = wrong_record_skipped(bins)
    if skipped and len(skipped) == len(mamba_by_record):
        raise Q5DJoinError(
            f"the wrong-record control cannot be built: every record "
            f"({skipped}) sits alone in its length bin, so no derangement "
            f"exists.  The control is skipped and reported — it is never run "
            f"as an identity mapping, which would put a copy of TRUE into "
            f"the null.")
    out: Dict[str, RecordSequence] = {}
    for record, target in mapping.items():
        donor = mamba_by_record[target]
        out[record] = RecordSequence(record, donor.split, donor.side,
                                     donor.pre_samples, donor.post_samples,
                                     donor.rows)
    return out


def null_summary(j_wrong: Sequence[float], j_shuffle: Sequence[float],
                 j_shift: Sequence[float], j_true: float,
                 n_processed: int) -> Dict[str, object]:
    """The family-wise max-null and the signal ratio.

    ``J_null_max[b] = max(J_wrong[b], J_shuffle[b], J_shift[b])`` — one max
    per replicate across all three families, so passing means beating the best
    of them, not the average.  The ``1 / n_processed`` floor stops a zero null
    from manufacturing an infinite ratio.
    """
    lengths = {len(j_wrong), len(j_shuffle), len(j_shift)}
    if len(lengths) != 1:
        raise Q5DJoinError(
            f"the three control families must have equal replicate counts, "
            f"got {sorted(lengths)}")
    maxima = [max(a, b, c) for a, b, c in zip(j_wrong, j_shuffle, j_shift)]
    floor = 1.0 / float(n_processed) if n_processed else 1.0
    q95 = percentile(maxima, 95.0)
    q99 = percentile(maxima, 99.0)
    return {
        "replicates": len(maxima),
        "families": list(CONTROL_FAMILIES),
        "master_seed": MASTER_SEED,
        "rule_fingerprint": rule_fingerprint(),
        "j_true": float(j_true),
        "median": percentile(maxima, 50.0),
        "q95": q95, "q99": q99,
        "max": max(maxima) if maxima else 0.0,
        "finite_sample_floor": floor,
        "signal_to_null": _ratio(j_true, max(q95, floor)),
        "j_null_max": list(maxima),
    }


def assert_null_matches_rule(summary: Mapping[str, object]) -> None:
    """A null may not be inherited by a relaxed rule.

    If the tolerance, ledger, matcher or any gate constant moves, the
    fingerprint moves with it and the stored null becomes unusable.  That is
    the structural reason a relaxation cannot quietly borrow the primary
    rule's cutoff.
    """
    stored = summary.get("rule_fingerprint")
    current = rule_fingerprint()
    if stored != current:
        raise NullReuseError(
            f"this null was generated under rule {stored!r} but the current "
            f"rule is {current!r}.  A relaxed or altered rule must regenerate "
            f"all three control families; it may not inherit the primary "
            f"rule's cutoff.")


def record_cluster_bootstrap(per_record: Mapping[str, Tuple[int, int]],
                             j_true: float, null_q95: float,
                             replicates: int = N_BOOTSTRAP_REPLICATES
                             ) -> Dict[str, object]:
    """Record-cluster bootstrap of ``J_min_TRUE - q95(J_null_max)``.

    All beats of a sampled record travel together, because records are the
    unit of dependence here.  The null is generated once under the frozen
    rule; this interval quantifies the true record sample and is not a licence
    to retune anything.
    """
    records = sorted(per_record)
    if not records:
        return {"replicates": 0, "ci_low": 0.0, "ci_high": 0.0,
                "point": j_true - null_q95, "seed": BOOTSTRAP_SEED}
    rng = random.Random(f"{BOOTSTRAP_SEED}|record_cluster")
    deltas: List[float] = []
    for _b in range(int(replicates)):
        hits = total = 0
        for _k in range(len(records)):
            record = records[rng.randrange(len(records))]
            certified, denominator = per_record[record]
            hits += certified
            total += denominator
        deltas.append(_ratio(hits, total) - null_q95)
    return {
        "replicates": int(replicates), "seed": BOOTSTRAP_SEED,
        "point": float(j_true) - float(null_q95),
        "ci_low": percentile(deltas, 2.5), "ci_high": percentile(deltas, 97.5),
        "rule_fingerprint": rule_fingerprint(),
    }


# ─────────────────────────────────────────────────────────────────────────────
# Gates and the decision
# ─────────────────────────────────────────────────────────────────────────────
class DecisionLedger(object):
    """First-failure-wins for the primary decision; every gate still recorded.

    The spec allows exactly one primary stopping reason, but a reviewer needs
    the whole gate table — including the gates that passed after the first
    failure — so both are kept and neither is derived from the other.
    """

    __slots__ = ("gates", "_primary", "_primary_leg", "_primary_gate")

    def __init__(self) -> None:
        self.gates: List[Dict[str, object]] = []
        self._primary: Optional[str] = None
        self._primary_leg: Optional[str] = None
        self._primary_gate: Optional[str] = None

    def record(self, name: str, passed: bool, value: object = None,
               threshold: object = None, decision: Optional[str] = None,
               failed_leg: Optional[str] = None,
               detail: str = "") -> bool:
        if decision is not None and decision not in DECISIONS:
            raise Q5DJoinError(f"unknown decision {decision!r}")
        if failed_leg is not None and failed_leg not in LEGS:
            raise Q5DJoinError(f"unknown leg {failed_leg!r}")
        self.gates.append({"gate": name, "passed": bool(passed),
                           "value": value, "threshold": threshold,
                           "decision_if_failed": decision,
                           "failed_leg": failed_leg, "detail": detail})
        if not passed and self._primary is None:
            self._primary = decision or DECISION_RULE_FALSIFIED
            self._primary_leg = failed_leg
            self._primary_gate = name
        return bool(passed)

    @property
    def primary_decision(self) -> Optional[str]:
        return self._primary

    def decide(self, all_inputs_present: bool = True) -> Dict[str, object]:
        if not all_inputs_present and self._primary is None:
            self._primary = DECISION_INPUT_ABSENT
        decision = self._primary or DECISION_IDENTIFIABLE
        return {
            "decision": decision,
            "first_stopping_reason": self._primary_gate,
            "failed_leg": self._primary_leg,
            "gates": list(self.gates),
            "gates_passed": sum(1 for g in self.gates if g["passed"]),
            "gates_total": len(self.gates),
            "rule_fingerprint": rule_fingerprint(),
            "training_performed": False,
            "model_scored": False,
            "v10_probability_opened": False,
            "association_performed": False,
        }


def evaluate_gates(coverage: Mapping[str, object],
                   inflation: Mapping[str, float],
                   null: Optional[Mapping[str, object]] = None,
                   bootstrap: Optional[Mapping[str, object]] = None,
                   fixtures_ok: bool = True,
                   leg1_ok: bool = True,
                   leg2_boundaries_ok: bool = True,
                   ambiguous_fraction: float = 0.0) -> DecisionLedger:
    """The twelve frozen DS1 gates, in the spec's order.

    Nothing here is recomputed from results: the thresholds are module
    constants and the ledger only compares against them.
    """
    led = DecisionLedger()
    led.record("1_synthetic_fixtures", fixtures_ok, fixtures_ok, True,
               DECISION_RULE_FALSIFIED, LEG2,
               "zero false pairs and every non-identifiable segment AMBIGUOUS")
    led.record("2a_leg1_source_replay", leg1_ok, leg1_ok, True,
               DECISION_RULE_FALSIFIED, LEG1,
               "count, order and RR ledger reproduced exactly")
    led.record("2b_leg2_record_boundaries", leg2_boundaries_ok,
               leg2_boundaries_ok, True, DECISION_INPUT_ABSENT, LEG2,
               "all 44 cache and result-position boundaries verified")

    overall = float(coverage.get("overall_coverage", 0.0))
    class_cov = dict(coverage.get("class_coverage", {}))
    led.record("3_overall_coverage", overall >= GATE_COVERAGE_MIN, overall,
               GATE_COVERAGE_MIN, DECISION_UNRESOLVED, LEG2)
    s_cov = float(class_cov.get("S", 0.0))
    led.record("4_s_coverage", s_cov >= GATE_S_COVERAGE_MIN, s_cov,
               GATE_S_COVERAGE_MIN, DECISION_SELECTION_BIASED, LEG2)
    worst_class = min(class_cov.values()) if class_cov else 0.0
    led.record("5_per_class_coverage",
               worst_class >= GATE_PER_CLASS_COVERAGE_MIN, worst_class,
               GATE_PER_CLASS_COVERAGE_MIN, DECISION_SELECTION_BIASED, LEG2)
    balance = float(coverage.get("class_coverage_balance", 0.0))
    led.record("6_class_coverage_balance", balance >= GATE_CLASS_BALANCE_MIN,
               balance, GATE_CLASS_BALANCE_MIN, DECISION_SELECTION_BIASED, LEG2)

    record_cov = dict(coverage.get("record_coverage", {}))
    worst_record = min(record_cov.values()) if record_cov else 0.0
    record_balance = float(coverage.get("record_coverage_balance", 0.0))
    led.record("7_record_coverage",
               worst_record >= GATE_RECORD_COVERAGE_MIN
               and record_balance >= GATE_RECORD_BALANCE_MIN,
               {"worst_record": worst_record, "balance": record_balance},
               {"min": GATE_RECORD_COVERAGE_MIN,
                "balance_min": GATE_RECORD_BALANCE_MIN},
               DECISION_SELECTION_BIASED, LEG2)

    agree = float(coverage.get("agreement_overall", 0.0))
    by_class = dict(coverage.get("agreement_by_class", {}))
    worst_agree = min(by_class.values()) if by_class else 0.0
    led.record("8_class_agreement",
               agree >= GATE_AGREEMENT_OVERALL_MIN
               and worst_agree >= GATE_AGREEMENT_PER_CLASS_MIN,
               {"overall": agree, "worst_class": worst_agree},
               {"overall_min": GATE_AGREEMENT_OVERALL_MIN,
                "class_min": GATE_AGREEMENT_PER_CLASS_MIN},
               DECISION_SELECTION_BIASED, LEG2)

    if null is not None:
        assert_null_matches_rule(null)
        j_true = float(null.get("j_true", 0.0))
        led.record("9_true_exceeds_q99", j_true > float(null.get("q99", 1.0)),
                   {"j_true": j_true, "q99": null.get("q99")}, "j_true > q99",
                   DECISION_RULE_FALSIFIED, LEG2)
        ratio = float(null.get("signal_to_null", 0.0))
        led.record("10_signal_to_null", ratio >= GATE_SIGNAL_TO_NULL_MIN,
                   ratio, GATE_SIGNAL_TO_NULL_MIN, DECISION_RULE_FALSIFIED,
                   LEG2)
    if bootstrap is not None:
        low = float(bootstrap.get("ci_low", 0.0))
        led.record("11_bootstrap_ci_lower", low > 0.0, low, "> 0",
                   DECISION_RULE_FALSIFIED, LEG2)

    worst_inflation = max(inflation.values()) if inflation else 0.0
    offenders = sorted(r for r, v in inflation.items()
                       if v > GATE_S_SHARE_INFLATION_MAX)
    led.record("12_s_share_inflation",
               worst_inflation <= GATE_S_SHARE_INFLATION_MAX, worst_inflation,
               GATE_S_SHARE_INFLATION_MAX, DECISION_SELECTION_BIASED, LEG2,
               f"records over the ceiling: {offenders}" if offenders else
               "source-relative; the parent's absolute 50% S ceiling is "
               "separate and unchanged")

    if led.primary_decision is None and ambiguous_fraction > 0.0:
        led.record("13_ambiguity_reported", True, ambiguous_fraction, None,
                   DECISION_UNRESOLVED, LEG2,
                   "ambiguous pairs remain unmatched by construction")
    return led


def stratum_report(results: Sequence[MatchResult]) -> Dict[str, object]:
    """Split the same numbers by the two preregistered count strata.

    Diagnostic only: neither stratum may be excluded, given a different
    matcher, or used to rescue a failed primary gate.
    """
    out: Dict[str, Dict[str, int]] = {
        s: {"records": 0, "cache_rows": 0, "certified": 0, "ambiguous": 0}
        for s in STRATA}
    for result in results:
        led = ledger_record(result.split, result.record)
        bucket = out[led.stratum]
        bucket["records"] += 1
        bucket["cache_rows"] += result.n_cache
        bucket["certified"] += result.certified_count
        bucket["ambiguous"] += len(result.ambiguous)
    for bucket in out.values():
        bucket["coverage"] = _ratio(bucket["certified"], bucket["cache_rows"])
    return out


# ─────────────────────────────────────────────────────────────────────────────
# Synthetic fixtures
# ─────────────────────────────────────────────────────────────────────────────
def _seq(record: str, side: str, pre: Sequence[int], post: Sequence[int],
         split: str = "DS1",
         rows: Optional[Sequence[Mapping[str, object]]] = None
         ) -> RecordSequence:
    return RecordSequence(record, split, side, pre, post, rows)


def _rr_from_samples(samples: Sequence[int]) -> Tuple[List[int], List[int]]:
    """Mirror the frozen RR semantic on a synthetic R-sample sequence."""
    diffs = [samples[i + 1] - samples[i] for i in range(len(samples) - 1)]
    pre = [diffs[0]] + diffs
    post = pre[1:] + [pre[-1]]
    return pre, post


class FixtureOutcome(object):
    __slots__ = ("name", "passed", "false_certified", "detail")

    def __init__(self, name: str, passed: bool, false_certified: int,
                 detail: str) -> None:
        self.name = name
        self.passed = passed
        self.false_certified = false_certified
        self.detail = detail

    def as_dict(self) -> Dict[str, object]:
        return {"fixture": self.name, "passed": self.passed,
                "false_certified_pairs": self.false_certified,
                "detail": self.detail}


def _check_against_truth(name: str, mamba: RecordSequence,
                         cache: RecordSequence,
                         truth: Mapping[int, int],
                         must_be_ambiguous: Iterable[int] = ()
                         ) -> FixtureOutcome:
    """Certified pairs must be a subset of the known truth, with no exceptions.

    A fixture passes only when every certified pair is true (``false_certified
    == 0``) and every deliberately non-identifiable row is *not* certified.
    """
    result = match_record(mamba, cache)
    certified = dict(result.certified)
    false_pairs = sum(1 for i, j in certified.items() if truth.get(i) != j)
    ambiguous_ok = all(i not in certified for i in must_be_ambiguous)
    recovered = sum(1 for i, j in truth.items() if certified.get(i) == j)
    detail = (f"certified {len(certified)} · true {len(truth)} · "
              f"recovered {recovered} · ambiguous {len(result.ambiguous)}")
    return FixtureOutcome(name, false_pairs == 0 and ambiguous_ok,
                          false_pairs, detail)


def fixture_leg1_identity() -> FixtureOutcome:
    """Leg 1 with no drops: duplicated endpoint RR, first/last beat eligible."""
    samples = [200 + 300 * k for k in range(8)]
    annotations = [(p, "N") for p in samples]
    replayed = replay_leg1_record("901", "DS1", annotations, samples[-1] + 400)
    ok = (replayed.n == len(samples)
          and not replayed.record_dropped
          and replayed.pre_samples[0] == replayed.pre_samples[1]
          and replayed.post_samples[-1] == replayed.post_samples[-2]
          and replayed.pre_samples[0] > 0
          and replayed.post_samples[-1] > 0)
    return FixtureOutcome("leg1_identity_endpoint_duplication", ok, 0,
                          f"n={replayed.n} pre0={replayed.pre_samples[0]} "
                          f"postN={replayed.post_samples[-1]}")


def fixture_leg1_isolated_drop() -> FixtureOutcome:
    """One isolated deterministic drop, plus the 150-sample boundary rule.

    The dropped beat's neighbours must inherit a *recomputed* RR — the source
    computes RR after filtering, so the survivors either side of a gap carry a
    wider interval than the raw ``.atr`` would give.
    """
    samples = [50] + [200 + 300 * k for k in range(8)]
    symbols = ["N", "N", "N", "F", "N", "N", "N", "N", "N"]
    annotations = list(zip(samples, symbols))
    replayed = replay_leg1_record("902", "DS1", annotations, samples[-1] + 400)
    reasons = [d["reason"] for d in replayed.dropped]
    kept_samples = [e["raw_r_sample"] for e in replayed.kept]
    # The gap sits between the two survivors that flanked the dropped F beat.
    spans_gap = 600 in [b - a for a, b in zip(kept_samples, kept_samples[1:])]
    ok = (replayed.n == 7
          and reasons.count(REASON_BOUNDARY) == 1
          and reasons.count(REASON_SYMBOL) == 1
          and 50 not in kept_samples
          and spans_gap
          and to_samples(0.0 + max(replayed.pre_seconds), UNIT_SECONDS) == 600)
    return FixtureOutcome("leg1_isolated_deterministic_drop", ok, 0,
                          f"kept {replayed.n} · dropped {len(replayed.dropped)}"
                          f" · rr recomputed across the gap={spans_gap}")


def fixture_leg1_consecutive_drops() -> FixtureOutcome:
    """Two adjacent deterministic drops collapse into one wider interval."""
    samples = [200 + 300 * k for k in range(9)]
    symbols = ["N", "N", "N", "Q", "F", "N", "N", "N", "N"]
    annotations = list(zip(samples, symbols))
    replayed = replay_leg1_record("903", "DS1", annotations, samples[-1] + 400)
    kept_samples = [e["raw_r_sample"] for e in replayed.kept]
    gaps = [b - a for a, b in zip(kept_samples, kept_samples[1:])]
    ok = (replayed.n == 7
          and len(replayed.dropped) == 2
          and all(d["reason"] == REASON_SYMBOL for d in replayed.dropped)
          and 900 in gaps)
    return FixtureOutcome("leg1_consecutive_deterministic_drops", ok, 0,
                          f"kept {replayed.n} · gaps {sorted(set(gaps))}")


def fixture_leg1_fq_deletion_concentration() -> FixtureOutcome:
    """The Q5-B-0 drop shape: F/Q only, concentrated in two records.

    Q5-B-0 measured 818 absent beats — N 1, S 0, V 0, F 802, Q 15 — with 92%
    in records 208 and 213.  The fixture reproduces that *shape*: the class
    profile of a Leg 1 drop is F/Q-dominated, and no S beat is ever dropped by
    the symbol rule, because ``A a J S`` are all in the registered map.
    """
    dropped_by_record: Dict[str, List[str]] = {}
    kept_total = 0
    for record, f_count in (("208", 12), ("213", 10), ("101", 1)):
        symbols = ["N"] * 8 + ["F"] * f_count + ["Q"] + ["A", "a", "J", "S",
                                                         "V", "E"]
        samples = [200 + 300 * k for k in range(len(symbols))]
        replayed = replay_leg1_record(record, "DS1", list(zip(samples,
                                                              symbols)),
                                      samples[-1] + 400)
        kept_total += replayed.n
        dropped_by_record[record] = [str(d["symbol"]) for d in replayed.dropped]
    every_drop = [s for v in dropped_by_record.values() for s in v]
    concentrated = (len(dropped_by_record["208"])
                    + len(dropped_by_record["213"])) / len(every_drop)
    ok = (all(s in ("F", "Q") for s in every_drop)
          and concentrated > 0.9
          and kept_total == 3 * (8 + 6))
    return FixtureOutcome("leg1_fq_deletion_concentration", ok, 0,
                          f"dropped symbols {sorted(set(every_drop))} · "
                          f"two-record concentration {concentrated:.3f}")


def fixture_leg1_record_too_few() -> FixtureOutcome:
    """The fewer-than-five-valid-beats record rule drops the whole record."""
    annotations = [(200 + 300 * k, "N") for k in range(3)]
    replayed = replay_leg1_record("905", "DS1", annotations, 2000)
    ok = (replayed.record_dropped and replayed.n == 0
          and all(d["reason"] == REASON_TOO_FEW for d in replayed.dropped))
    return FixtureOutcome("leg1_record_under_five_valid_beats", ok, 0,
                          f"record_dropped={replayed.record_dropped}")


def fixture_leg2_identity() -> FixtureOutcome:
    """Leg 2 with identical sequences: every row certified, none ambiguous."""
    samples = [200 + k for k in _walk((300, 310, 295, 320, 288, 305, 299))]
    pre, post = _rr_from_samples(samples)
    mamba = _seq("904", "mamba", pre, post)
    cache = _seq("904", "cache", pre, post)
    truth = {i: i for i in range(len(pre))}
    return _check_against_truth("leg2_identity", mamba, cache, truth)


def fixture_leg2_cache_only_row() -> FixtureOutcome:
    """One cache row has no mamba partner; nothing is imputed for it."""
    samples = [200 + k for k in _walk((300, 311, 294, 322, 287, 306, 298, 315))]
    pre, post = _rr_from_samples(samples)
    keep = [0, 1, 2, 4, 5, 6, 7, 8]                 # mamba is missing row 3
    mamba = _seq("906", "mamba", [pre[k] for k in keep],
                 [post[k] for k in keep])
    cache = _seq("906", "cache", pre, post)
    truth = {i: k for i, k in enumerate(keep)}
    return _check_against_truth("leg2_cache_only_row_gap", mamba, cache, truth)


def fixture_leg2_mamba_only_row() -> FixtureOutcome:
    """One mamba row has no cache partner; it stays unmatched, not guessed."""
    samples = [200 + k for k in _walk((301, 312, 293, 324, 286, 307, 297, 316))]
    pre, post = _rr_from_samples(samples)
    keep = [0, 1, 3, 4, 5, 6, 7, 8]                 # cache is missing row 2
    mamba = _seq("907", "mamba", pre, post)
    cache = _seq("907", "cache", [pre[k] for k in keep],
                 [post[k] for k in keep])
    truth = {k: i for i, k in enumerate(keep)}
    return _check_against_truth("leg2_mamba_only_row_gap", mamba, cache, truth)


def fixture_leg2_consecutive_gaps() -> FixtureOutcome:
    """Consecutive gaps on both sides at once."""
    samples = [200 + k for k in _walk(
        (300, 313, 292, 325, 285, 308, 296, 317, 331, 279))]
    pre, post = _rr_from_samples(samples)
    mamba_keep = [0, 1, 2, 5, 6, 7, 8, 9, 10]       # dropped 3, 4
    cache_keep = [0, 1, 2, 3, 4, 5, 8, 9, 10]       # dropped 6, 7
    mamba = _seq("907", "mamba", [pre[k] for k in mamba_keep],
                 [post[k] for k in mamba_keep])
    cache = _seq("907", "cache", [pre[k] for k in cache_keep],
                 [post[k] for k in cache_keep])
    shared = [k for k in mamba_keep if k in cache_keep]
    truth = {mamba_keep.index(k): cache_keep.index(k) for k in shared}
    return _check_against_truth("leg2_consecutive_gaps", mamba, cache, truth)


def fixture_equal_count_cancellation() -> FixtureOutcome:
    """A drop-one/add-one cancellation must not be positionally zipped.

    Both sides hold the same number of rows, but they are not the same rows —
    exactly the ``pos`` versus ``p`` boundary difference the spec warns about.
    Certifying by position here would be a silent false map, so the fixture
    demands that every certified pair still be *true*, not merely aligned.
    """
    samples = [200 + k for k in _walk(
        (300, 314, 291, 326, 284, 309, 295, 318, 330))]
    pre, post = _rr_from_samples(samples)
    mamba_keep = [0, 1, 2, 3, 4, 5, 6, 7, 8]        # drops row 9
    cache_keep = [1, 2, 3, 4, 5, 6, 7, 8, 9]        # drops row 0
    mamba = _seq("908", "mamba", [pre[k] for k in mamba_keep],
                 [post[k] for k in mamba_keep])
    cache = _seq("908", "cache", [pre[k] for k in cache_keep],
                 [post[k] for k in cache_keep])
    shared = [k for k in mamba_keep if k in cache_keep]
    truth = {mamba_keep.index(k): cache_keep.index(k) for k in shared}
    outcome = _check_against_truth("leg2_equal_count_cancellation", mamba,
                                   cache, truth)
    # The zip hypothesis would map row 0 to row 0; that pair is false.
    result = match_record(mamba, cache)
    zipped = dict(result.certified).get(0) == 0
    if zipped:
        return FixtureOutcome(outcome.name, False, outcome.false_certified + 1,
                              "equal counts were zipped by position")
    return outcome


def fixture_repeated_rr_unique_context() -> FixtureOutcome:
    """A repeated coupling interval that one unique flank still resolves."""
    intervals = (300, 300, 300, 341, 300, 300, 300)
    samples = [200 + k for k in _walk(intervals)]
    pre, post = _rr_from_samples(samples)
    mamba = _seq("909", "mamba", pre, post)
    cache = _seq("909", "cache", pre, post)
    result = match_record(mamba, cache)
    certified = dict(result.certified)
    anchored = [i for i, (a, b) in enumerate(zip(pre, post))
                if 341 in (a, b)]
    ok = all(certified.get(i) == i for i in anchored) and \
        all(certified.get(i, i) == i for i in certified)
    return FixtureOutcome("leg2_repeated_rr_unique_flank", ok, 0,
                          f"certified {len(certified)} of {len(pre)} · "
                          f"anchored rows {anchored}")


def fixture_perfect_repeat_is_ambiguous() -> FixtureOutcome:
    """A perfectly repeated segment has two equally optimal alignments.

    Certifying either one would be promoting an arbitrary optimal path, so
    every interior row of the repeat must come back ``AMBIGUOUS`` and stay
    unmatched.  This is the ``JOIN_UNRESOLVED`` shape in miniature.
    """
    pre = [300] * 6
    post = [300] * 6
    mamba = _seq("910", "mamba", pre, post)
    cache = _seq("910", "cache", pre[:-1], post[:-1])   # one row shorter
    result = match_record(mamba, cache)
    ok = (not result.certified
          and result.max_cardinality == 5
          and len(result.ambiguous) > 0)
    return FixtureOutcome("leg2_perfect_repeat_stays_ambiguous", ok,
                          len(result.certified),
                          f"certified {len(result.certified)} · ambiguous "
                          f"{len(result.ambiguous)} · M={result.max_cardinality}")


def fixture_quantization_one_sample() -> FixtureOutcome:
    """A +/-1 sample wobble on either RR component still matches."""
    samples = [200 + k for k in _walk((300, 316, 289, 327, 283, 311, 294))]
    pre, post = _rr_from_samples(samples)
    jitter_pre = [v + (1 if k % 2 == 0 else -1) for k, v in enumerate(pre)]
    jitter_post = [v + (-1 if k % 3 == 0 else 1) for k, v in enumerate(post)]
    mamba = _seq("911", "mamba", pre, post)
    cache = _seq("911", "cache", jitter_pre, jitter_post)
    truth = {i: i for i in range(len(pre))}
    return _check_against_truth("leg2_plus_minus_one_sample", mamba, cache,
                                truth)


def fixture_two_sample_rejected() -> FixtureOutcome:
    """A 2-sample offset is outside the fixed tolerance and is not matched.

    The tolerance is never widened because a record's RR pattern repeats.
    """
    samples = [200 + k for k in _walk((300, 318, 288, 329, 282, 313, 292))]
    pre, post = _rr_from_samples(samples)
    shifted_pre = [v + 2 for v in pre]
    shifted_post = [v + 2 for v in post]
    mamba = _seq("912", "mamba", pre, post)
    cache = _seq("912", "cache", shifted_pre, shifted_post)
    result = match_record(mamba, cache)
    ok = not result.certified and not result.edges
    return FixtureOutcome("leg2_two_sample_offset_rejected", ok,
                          len(result.certified),
                          f"candidate edges {len(result.edges)}")


def fixture_seconds_conversion() -> FixtureOutcome:
    """A declared seconds artifact converts to the same integer samples."""
    samples = [200 + k for k in _walk((300, 315, 290, 324, 285, 312, 297))]
    pre, post = _rr_from_samples(samples)
    seconds_pre = [v / FS for v in pre]
    seconds_post = [v / FS for v in post]
    check_declared_unit(UNIT_SECONDS, seconds_pre)
    converted_pre = rr_to_samples(seconds_pre, UNIT_SECONDS)
    converted_post = rr_to_samples(seconds_post, UNIT_SECONDS)
    ok = (list(converted_pre) == pre and list(converted_post) == post)
    return FixtureOutcome("units_seconds_to_samples", ok, 0,
                          f"round-half-to-even at {FS:g} Hz")


def fixture_wrong_unit_stops() -> FixtureOutcome:
    """A wrong unit declaration stops the run instead of fitting a scale."""
    in_samples = [300, 305, 298, 311, 296]
    stopped_wrong = stopped_unknown = False
    try:
        check_declared_unit(UNIT_SECONDS, in_samples)
    except Q5DJoinError:
        stopped_wrong = True
    try:
        to_samples(0.83, "milliseconds")
    except Q5DJoinError:
        stopped_unknown = True
    return FixtureOutcome("units_wrong_declaration_stops",
                          stopped_wrong and stopped_unknown, 0,
                          f"wrong-scale stop={stopped_wrong} · "
                          f"unknown-unit stop={stopped_unknown}")


def fixture_record_boundary_corruption() -> FixtureOutcome:
    """A corrupted record boundary fails; it never becomes a cross-record map."""
    observed = {"DS1": {r: n for r, n in CACHE_LEDGER["DS1"]},
                "DS2": {r: n for r, n in CACHE_LEDGER["DS2"]}}
    clean = verify_record_boundaries(observed)
    observed["DS1"]["108"] = observed["DS1"]["108"] + 1
    corrupted = verify_record_boundaries(observed)
    return FixtureOutcome("ledger_record_boundary_corruption",
                          bool(clean["ok"]) and not corrupted["ok"], 0,
                          f"clean={clean['ok']} corrupted={corrupted['ok']}")


def fixture_row_order_corruption() -> FixtureOutcome:
    """Within-record row-order corruption must not certify a false pair."""
    samples = [200 + k for k in _walk((300, 317, 287, 328, 281, 314, 293))]
    pre, post = _rr_from_samples(samples)
    order = [0, 1, 2, 3, 4, 5, 6]
    corrupted = [0, 1, 4, 3, 2, 5, 6]               # rows 2 and 4 swapped
    mamba = _seq("914", "mamba", pre, post)
    cache = _seq("914", "cache", [pre[k] for k in corrupted],
                 [post[k] for k in corrupted])
    result = match_record(mamba, cache)
    truth = {i: corrupted.index(i) for i in order}
    false_pairs = sum(1 for i, j in result.certified if truth.get(i) != j)
    # The swapped rows cannot be recovered monotonically, and must not be
    # replaced by a plausible-looking wrong pair: they simply drop out.
    swapped_certified = [i for i, _j in result.certified if i in (2, 4)]
    ok = (false_pairs == 0 and not swapped_certified
          and len(result.certified) < len(order))
    return FixtureOutcome("leg2_row_order_corruption", ok, false_pairs,
                          f"certified {len(result.certified)}/{len(order)} · "
                          f"false {false_pairs} · swapped rows certified "
                          f"{swapped_certified}")


def fixture_cross_record_refused() -> FixtureOutcome:
    """A mapping may never cross a record boundary, in either direction."""
    pre, post = [300] * 5, [300] * 5
    left = _seq("914", "mamba", pre, post)
    right = _seq("915", "cache", pre, post)
    refused = False
    try:
        match_record(left, right)
    except Q5DJoinError:
        refused = True
    split_refused = False
    try:
        match_record(left, _seq("914", "cache", pre, post, split="DS2"))
    except Q5DJoinError:
        split_refused = True
    return FixtureOutcome("leg2_cross_record_refused",
                          refused and split_refused, 0,
                          f"record={refused} split={split_refused}")


def fixture_t_is_rejected() -> FixtureOutcome:
    """Offering ``t`` as a join key is an error, not a silently ignored field."""
    stopped_field = stopped_declared = False
    try:
        reject_t_as_join_key({"record": "100", "t": [0.0, 0.8, 1.6]})
    except Q5DJoinError:
        stopped_field = True
    try:
        reject_t_as_join_key({"record": "100", "join_key": "t"})
    except Q5DJoinError:
        stopped_declared = True
    reject_t_as_join_key({"record": "100", "join_key": "positional"})
    return FixtureOutcome("input_t_rejected_as_join_key",
                          stopped_field and stopped_declared, 0,
                          f"field={stopped_field} declared={stopped_declared}")


def fixture_no_arbitrary_optimal_path() -> FixtureOutcome:
    """Two optimal alignments coexist; only the invariant part is certified.

    A short repeat sits between two unique anchors and one of the repeated
    mamba rows has no cache partner.  Two maximum matchings therefore exist —
    the surviving cache row can pair with either repeated mamba row — so those
    two edges must come back ``AMBIGUOUS`` while the anchors, which every
    maximum matching contains, are ``CERTIFIED``.

    This is the fixture that would catch a matcher which walks one optimal
    path and certifies whatever it happened to touch.
    """
    mamba_pre = [250, 300, 300, 300, 400]
    mamba_post = [300, 300, 300, 400, 320]
    cache_keep = [0, 1, 3, 4]                       # one repeat row is missing
    cache_pre = [mamba_pre[k] for k in cache_keep]
    cache_post = [mamba_post[k] for k in cache_keep]
    mamba = _seq("915", "mamba", mamba_pre, mamba_post)
    cache = _seq("915", "cache", cache_pre, cache_post)
    result = match_record(mamba, cache)
    certified = dict(result.certified)
    ambiguous = set(result.ambiguous)
    anchors_certified = (certified.get(0) == 0 and certified.get(3) == 2
                         and certified.get(4) == 3)
    # Rows 1 and 2 are interchangeable, so neither may be certified.
    repeat_left_open = (1 not in certified and 2 not in certified
                        and {(1, 1), (2, 1)} <= ambiguous)
    false_pairs = sum(1 for i, j in certified.items()
                      if (i, j) not in ((0, 0), (3, 2), (4, 3)))
    ok = (anchors_certified and repeat_left_open and false_pairs == 0
          and result.max_cardinality == 4)
    return FixtureOutcome("leg2_no_arbitrary_optimal_path", ok, false_pairs,
                          f"M={result.max_cardinality} · certified "
                          f"{sorted(certified.items())} · ambiguous "
                          f"{sorted(ambiguous)}")


def _walk(intervals: Sequence[int]) -> List[int]:
    """Cumulative R positions from a list of RR intervals."""
    out = [0]
    for step in intervals:
        out.append(out[-1] + int(step))
    return out


FIXTURES: Tuple = (
    fixture_leg1_identity,
    fixture_leg1_isolated_drop,
    fixture_leg1_consecutive_drops,
    fixture_leg1_fq_deletion_concentration,
    fixture_leg1_record_too_few,
    fixture_leg2_identity,
    fixture_leg2_cache_only_row,
    fixture_leg2_mamba_only_row,
    fixture_leg2_consecutive_gaps,
    fixture_equal_count_cancellation,
    fixture_repeated_rr_unique_context,
    fixture_perfect_repeat_is_ambiguous,
    fixture_quantization_one_sample,
    fixture_two_sample_rejected,
    fixture_seconds_conversion,
    fixture_wrong_unit_stops,
    fixture_record_boundary_corruption,
    fixture_row_order_corruption,
    fixture_cross_record_refused,
    fixture_t_is_rejected,
    fixture_no_arbitrary_optimal_path,
)


def run_synthetic_fixtures() -> List[FixtureOutcome]:
    """Run every fixture.  Synthetic data only — nothing registered is opened."""
    return [fixture() for fixture in FIXTURES]


def fixtures_passed(outcomes: Sequence[FixtureOutcome]) -> bool:
    """Zero false certified pairs, and every fixture green."""
    return all(o.passed for o in outcomes) and \
        sum(o.false_certified for o in outcomes) == 0


# ─────────────────────────────────────────────────────────────────────────────
# Serialisers.  Schema now; the bundle itself only on an approved run.
# ─────────────────────────────────────────────────────────────────────────────
def write_csv(path: str, fields: Sequence[str],
              rows: Iterable[Mapping[str, object]]) -> str:
    import csv                                          # noqa: PLC0415
    with open(path, "w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(fields),
                                extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({k: ("" if row.get(k) is None else row.get(k))
                             for k in fields})
    return path


def write_synthetic_fixture_results(outcomes: Sequence[FixtureOutcome],
                                    path: str) -> str:
    return write_csv(path,
                     ("fixture", "passed", "false_certified_pairs", "detail"),
                     [o.as_dict() for o in outcomes])


def write_join_map(rows: Sequence[Mapping[str, object]], path: str) -> str:
    """Parquet when pyarrow is present; the schema is validated either way.

    No probability column can reach this file: every row goes through
    :func:`validate_join_map_row` first, and the banned-field list is checked
    against the frozen schema, not against whatever the caller passed.
    """
    for row in rows:
        validate_join_map_row(row)
    if path.endswith(".csv"):
        return write_csv(path, JOIN_MAP_FIELDS, rows)
    try:
        import pyarrow                                  # noqa: PLC0415
        import pyarrow.parquet as pq                    # noqa: PLC0415
    except ImportError as exc:                          # pragma: no cover
        raise Q5DJoinError(
            f"join_map.parquet needs pyarrow ({exc}); install it in the run "
            f"environment or write the .csv shadow instead") from exc
    columns = {f: [row.get(f) for row in rows] for f in JOIN_MAP_FIELDS}
    pq.write_table(pyarrow.table(columns), path)        # pragma: no cover
    return path


def write_unmatched_and_ambiguous(rows: Sequence[Mapping[str, object]],
                                  path: str) -> str:
    subset = [r for r in rows if r["status"] != STATUS_CERTIFIED]
    return write_csv(path, JOIN_MAP_FIELDS, subset)


def write_record_class_coverage(coverage: Mapping[str, object], path: str
                                ) -> str:
    record_coverage = dict(coverage.get("record_coverage", {}))
    rows = [{"record": record, "certified_coverage": value}
            for record, value in sorted(record_coverage.items())]
    for cls in AAMI_CLASSES:
        rows.append({"record": f"__class_{cls}",
                     "certified_coverage":
                         dict(coverage.get("class_coverage", {})).get(cls, 0.0)})
    return write_csv(path, ("record", "certified_coverage"), rows)


def build_config(mode: str, timestamp: str,
                 execution_approved: bool = False) -> Dict[str, object]:
    return {
        "experiment_id": EXPERIMENT_ID, "arm": ARM_ID, "substage": SUBSTAGE,
        "run_slug": RUN_SLUG, "module_version": MODULE_VERSION,
        "module_build": MODULE_BUILD, "mode": resolve_mode(mode),
        "timestamp": timestamp,
        "rule_fingerprint": rule_fingerprint(),
        "rr_tolerance_samples": RR_TOLERANCE_SAMPLES,
        "fs": FS, "master_seed": MASTER_SEED,
        "bootstrap_seed": BOOTSTRAP_SEED,
        "n_null_replicates": N_NULL_REPLICATES,
        "n_bootstrap_replicates": N_BOOTSTRAP_REPLICATES,
        "execution_on_registered_data_approved": bool(execution_approved),
        "approval_note": APPROVAL_NOTE,
    }


def build_manifest(inputs: Mapping[str, str], timestamp: str,
                   preflight: Optional[Mapping[str, object]] = None
                   ) -> Dict[str, object]:
    """Code, input, unit and environment hashes for the run bundle.

    The preflight freeze is embedded, not merely referenced: a later DS2
    support gate reads it back out of the DS1 manifest and refuses to release
    the labels unless this run's inputs are the same ones.
    """
    return {
        "timestamp": timestamp,
        "code": assert_implementation_only(),
        "rule_fingerprint": rule_fingerprint(),
        "ledger": verify_ledger(),
        "preflight": {k: preflight.get(k) for k in PREFLIGHT_FREEZE_FIELDS}
        if preflight else None,
        "declared_units": list(DECLARED_UNITS),
        "env_pin": build_env_pin(),
        "inputs": {name: {"path": path,
                          "sha256": sha256_file(path)
                          if os.path.exists(path) else None}
                   for name, path in sorted(inputs.items())},
        "python": sys.version.split()[0],
        "bundle_files": list(BUNDLE_FILES),
    }


def bundle_is_complete(directory: str) -> Tuple[bool, List[str]]:
    missing = [name for name in BUNDLE_FILES
               if not os.path.exists(os.path.join(directory, name))]
    return (not missing), missing


# ─────────────────────────────────────────────────────────────────────────────
# Cards
# ─────────────────────────────────────────────────────────────────────────────
def design_card(mode: str = MODE_DESIGN,
                execution_approved: bool = False) -> str:
    """The frozen rule in one screen.  Reads nothing."""
    ledger = verify_ledger()
    lines = [
        "=" * 74,
        NO_EXECUTION_BANNER,
        "=" * 74,
        f"experiment      : {EXPERIMENT_ID} / {ARM_ID}",
        f"substage        : {SUBSTAGE}",
        f"mode            : {resolve_mode(mode)}",
        f"rule fingerprint: {ledger['rule_fingerprint'][:16]}…",
        "",
        "APPROVAL",
        "  implementation                : approved",
        "  execution on registered data  : approved",
        "  V10 probability / association : SEALED — needs a further approval",
        "  DS2 per-beat class labels     : sealed until the DS1 freeze",
        f"  this run opted in to opening data : "
        f"{'yes' if execution_approved else 'no — it cannot open one'}",
        f"  {APPROVAL_NOTE}",
        "",
        "LEG 1 — `.atr` -> mamba (deterministic source replay)",
        f"  symbol map      : {sorted(set(AAMI_SYMBOL_MAP))} -> N/S/V "
        f"(F and Q are not mapped)",
        f"  boundary rule   : {WIN_BEFORE} <= pos < len(signal) - {WIN_AFTER}",
        f"  record rule     : drop the record below {MIN_VALID_BEATS} valid "
        f"beats",
        "  RR              : recomputed after filtering; first pre-RR and last",
        "                    post-RR duplicate their neighbour interval, so",
        "                    the first and last beats are ELIGIBLE",
        f"  failure         : {DECISION_RULE_FALSIFIED} / {LEG1}",
        "",
        "LEG 2 — mamba -> V9/V10 positional rows (detector-dependent)",
        "  row order       : detect_r() detection order, NOT `.atr` ordinal",
        "  identity        : positional only (result NPZ stores prob, y, pid)",
        "  `t`             : refused as a join key",
        "  scope           : record-local; global alignment is forbidden",
        f"  candidate edge  : |dpre| <= {RR_TOLERANCE_SAMPLES} and "
        f"|dpost| <= {RR_TOLERANCE_SAMPLES} integer samples at {FS:g} Hz",
        "  matcher         : maximum-cardinality monotone one-to-one;",
        "                    CERTIFIED = in every maximum matching;",
        "                    otherwise AMBIGUOUS and left unmatched",
        "",
        "44-RECORD LEDGER",
        f"  records         : {ledger['records']} "
        f"({ledger['equal_count_records']} equal-count, "
        f"{ledger['mismatched_records']} mismatched)",
        f"  cache / mamba   : {ledger['cache_total']} / {ledger['mamba_total']}"
        f"  (difference {ledger['total_difference']})",
        f"  verified        : {ledger['ok']}",
        "  equal count is a reporting stratum, NOT positional identity;",
        "  `V9/V10 subset-of mamba` is not an axiom (pos vs p boundary rules",
        "  allow a drop-one/add-one cancellation)",
        "",
        "CONTROLS / NULL",
        f"  families        : {list(CONTROL_FAMILIES)}",
        f"  master seed     : {MASTER_SEED} · bootstrap seed {BOOTSTRAP_SEED}",
        f"  replicates      : null {N_NULL_REPLICATES} · bootstrap "
        f"{N_BOOTSTRAP_REPLICATES}",
        "  J_null_max[b]   = max(J_wrong[b], J_shuffle[b], J_shift[b])",
        "",
        "RECORD 232 (source concentration, carried not repaired)",
        f"  record 232 supplies {RECORD_232_S_BEATS}/{DS2_S_BEATS_TOTAL} "
        f"DS2 S beats ({RECORD_232_S_SHARE * 100:.1f}%) BEFORE any join.",
        f"  gate 12 tests share INFLATION (<= {GATE_S_SHARE_INFLATION_MAX}); it",
        f"  does not relax the parent's absolute "
        f"{PARENT_ABSOLUTE_RECORD_S_SHARE_CEILING:.0%} ceiling.  A successful",
        "  join can still leave the parent association blocked.",
        "",
        f"DECISIONS        : {list(DECISIONS)}",
        "=" * 74,
    ]
    return "\n".join(lines)


def ledger_table() -> str:
    """The 44-record ledger as a readable table."""
    lines = [f"{'split':<5} {'rec':>4} {'cache_n':>8} {'cache@':>8} "
             f"{'mamba_n':>8} {'mamba@':>8} {'diff':>5}  stratum"]
    for split in SPLITS:
        for row in build_ledger()[split]:
            lines.append(
                f"{split:<5} {row.record:>4} {row.cache_n:>8} "
                f"{row.cache_start:>8} {row.mamba_n:>8} {row.mamba_start:>8} "
                f"{row.delta:>5}  {row.stratum}")
    return "\n".join(lines)


def fixture_card(outcomes: Sequence[FixtureOutcome]) -> str:
    lines = ["synthetic fixtures (no registered artifact opened)", "-" * 74]
    for outcome in outcomes:
        flag = "PASS" if outcome.passed else "FAIL"
        lines.append(f"  {flag}  {outcome.name:<44} {outcome.detail}")
    false_pairs = sum(o.false_certified for o in outcomes)
    lines.append("-" * 74)
    lines.append(f"  fixtures {sum(1 for o in outcomes if o.passed)}/"
                 f"{len(outcomes)} · false certified pairs {false_pairs} "
                 f"(must be 0)")
    return "\n".join(lines)


def not_run_decision(reason: str = "implementation only") -> Dict[str, object]:
    """The decision this repository is honestly in: implemented, not run."""
    return {
        "decision": DECISION_NOT_RUN,
        "reason": reason,
        "first_stopping_reason": None,
        "failed_leg": None,
        "rule_fingerprint": rule_fingerprint(),
        "execution_on_registered_data_approved": False,
        "training_performed": False,
        "model_scored": False,
        "ds2_outcome_opened": False,
        "v10_probability_opened": False,
        "association_performed": False,
        "drive_mutated": False,
    }


# ─────────────────────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────────────────────
def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=NO_EXECUTION_BANNER)
    parser.add_argument("--mode", default=MODE_DESIGN,
                        help=f"one of {MODES} (default {MODE_DESIGN})")
    parser.add_argument("--out-dir", default="",
                        help="where SYNTHETIC_FIXTURES writes its CSV")
    parser.add_argument("--bundle-dir", default="",
                        help="an existing run bundle for JOIN_REPORT")
    parser.add_argument("--asset-map", default="",
                        help="JSON {label: path} for HASH_PREFLIGHT")
    parser.add_argument(EXECUTION_APPROVAL_FLAG, dest="execution_approval",
                        action="store_true",
                        help="assert the SEPARATE user approval to run on "
                             "registered data; unused in this repository")
    parser.add_argument(DS2_LABEL_RELEASE_FLAG, dest="ds2_released",
                        action="store_true",
                        help="release the DS2 support gate, only after the "
                             "DS1 rule has frozen")
    parser.add_argument("--self-check", action="store_true",
                        help="verify the ledger and the no-outcome guard")
    args = parser.parse_args(argv)

    mode = resolve_mode(args.mode)
    approved = bool(args.execution_approval)

    if args.self_check:
        print(json.dumps({"guard": assert_implementation_only(),
                          "ledger": verify_ledger()},
                         indent=2, ensure_ascii=False))
        return 0

    if mode in MODES_NEEDING_EXECUTION_APPROVAL and not approved:
        # The barrier, exercised: this is where an unapproved run stops, and
        # it stops before any registered path is opened.
        print(design_card(mode, execution_approved=False))
        print()
        print(f"STOP — mode {mode} opens registered artifacts and this run did "
              f"not opt in.")
        print(APPROVAL_NOTE)
        print(f"Nothing was read.  Re-run with {EXECUTION_APPROVAL_FLAG}.")
        print(json.dumps(not_run_decision(f"{mode} was not opted into with "
                                          f"{EXECUTION_APPROVAL_FLAG}"),
                         indent=2, ensure_ascii=False))
        return 2

    if mode == MODE_DESIGN:
        print(design_card(mode, execution_approved=approved))
        print()
        print(ledger_table())
        return 0

    if mode == MODE_FIXTURES:
        outcomes = run_synthetic_fixtures()
        print(fixture_card(outcomes))
        if args.out_dir:
            os.makedirs(args.out_dir, exist_ok=True)
            path = write_synthetic_fixture_results(
                outcomes, os.path.join(args.out_dir,
                                       "synthetic_fixture_results.csv"))
            print(f"  wrote {path}")
        return 0 if fixtures_passed(outcomes) else 1

    if mode == MODE_PREFLIGHT:
        if not args.asset_map:
            print("HASH_PREFLIGHT needs --asset-map <json>: {label: path}.")
            print("Registered hash for mamba_data.npz:", MAMBA_SHA256)
            return 2
        with open(args.asset_map, encoding="utf-8") as handle:
            assets = json.load(handle)
        report = hash_preflight(assets, EXECUTION_APPROVAL_TOKEN,
                                {"mamba": MAMBA_SHA256})
        print(json.dumps(report, indent=2, ensure_ascii=False))
        print("\nPREFLIGHT", "PASS" if report["ok"] else "STOP")
        return 0 if report["ok"] else 1

    if mode == MODE_REPORT:
        if not args.bundle_dir:
            print("JOIN_REPORT replays a saved bundle; pass --bundle-dir")
            return 2
        complete, missing = bundle_is_complete(args.bundle_dir)
        print(json.dumps({"bundle": args.bundle_dir, "complete": complete,
                          "missing": missing}, indent=2, ensure_ascii=False))
        return 0 if complete else 1

    # Reachable only with the execution approval, which nothing here grants.
    print(design_card(mode, execution_approved=True))
    print(f"\n{mode}: execution approval asserted.  This stage reads the "
          f"registered artifacts through open_registered_input() and "
          f"read_result_npz(); wire the asset paths in the notebook.")
    return 0


if __name__ == "__main__":                              # pragma: no cover
    raise SystemExit(main())
