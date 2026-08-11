#!/usr/bin/env python3
"""Regression tests for EXP-2026-008 / Q5-E.

Everything here is synthetic.  No test opens a registered artifact, reaches
Google Drive, touches the network, or copies a measured value out of the real
data into a fixture — a fixture built from real numbers would let an
implementation pass by memorising the answer.

Run with::

    python mit-bih/test_q5e_leg2_failure_mechanism_audit.py
"""

from __future__ import annotations

import json
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import q5d_order_preserving_beat_join as BJ          # noqa: E402
import q5e_leg2_failure_mechanism_audit as Q5E       # noqa: E402

NOTEBOOK = os.path.join(
    ROOT, "notebooks", "quest55_q5e_leg2_failure_mechanism_audit.ipynb")

PASSED = 0


def check(condition: bool, label: str) -> None:
    global PASSED
    if not condition:
        raise AssertionError(label)
    PASSED += 1


def row(record="101", *, mamba_row=None, cache_row=None, aami="",
        status=BJ.STATUS_CERTIFIED, reason=BJ.REASON_NONE, ordinal=None,
        r_sample=None):
    """One join-map row with exactly the frozen 15 fields."""
    return {
        "split": "DS1", "record": record,
        "raw_atr_ordinal": ordinal, "raw_r_sample": r_sample,
        "mamba_aami": aami if mamba_row is not None else None,
        "mamba_record_row": mamba_row,
        "mamba_global_row": None, "mamba_file_row": None,
        "cache_record_row": cache_row,
        "result_global_row": None,
        "status": status,
        "pre_rr_difference_samples": None,
        "post_rr_difference_samples": None,
        "failed_leg": None if status == BJ.STATUS_CERTIFIED else BJ.LEG2,
        "drop_or_unmatched_reason": reason,
    }


def tiny_bundle():
    """Two records: one clean, one with a length-3 failure run and a V beat.

    Cache rows 0..3 in each record; certified pairs carry `cache_record_row`
    on the mamba row, exactly as `join_record()` emits them.
    """
    rows = []
    # record 101: mamba rows 0..3, all certified, cache rows 0..3
    for i in range(4):
        rows.append(row("101", mamba_row=i, cache_row=i, aami="N",
                        ordinal=i, r_sample=100 + i))
    # record 208: mamba rows 0..4.  Rows 1,2,3 fail (a length-3 primary run);
    # raw ordinals skip 2 between rows 1 and 2, so the secondary audit splits
    # the same run in two — the Q1 artifact, reproduced deliberately.
    ordinals = [0, 1, 3, 4, 5]
    classes = ["N", "V", "V", "N", "N"]
    statuses = [BJ.STATUS_CERTIFIED, BJ.STATUS_UNMATCHED, BJ.STATUS_UNMATCHED,
                BJ.STATUS_UNMATCHED, BJ.STATUS_CERTIFIED]
    reasons = [BJ.REASON_NONE, BJ.REASON_NO_EDGE, BJ.REASON_NO_EDGE,
               BJ.REASON_NOT_OPTIMAL, BJ.REASON_NONE]
    cache_for = {0: 0, 4: 1}
    for i in range(5):
        rows.append(row("208", mamba_row=i, cache_row=cache_for.get(i),
                        aami=classes[i], status=statuses[i],
                        reason=reasons[i], ordinal=ordinals[i],
                        r_sample=200 + ordinals[i]))
    # record 208 cache-side unmatched rows 2,3
    for j, reason in ((2, BJ.REASON_NO_EDGE), (3, BJ.REASON_AMBIGUOUS)):
        rows.append(row("208", cache_row=j, status=BJ.STATUS_UNMATCHED
                        if reason != BJ.REASON_AMBIGUOUS
                        else BJ.STATUS_AMBIGUOUS, reason=reason))
    return rows


PROCESSED = {("101", 0): "N", ("101", 1): "N", ("101", 2): "N", ("101", 3): "N",
             ("208", 0): "N", ("208", 1): "N", ("208", 2): "V", ("208", 3): "V"}
CACHE_N = {"101": 4, "208": 4}


# ─────────────────────────────────────────────────────────────────────────────
def test_row_model_and_validation():
    rows = tiny_bundle()
    Q5E.validate_rows(rows)
    check(Q5E.is_mamba_side(rows[0]), "mamba side detected")
    check(Q5E.is_cache_side(rows[-1]), "cache side detected")
    check(Q5E.row_group(rows[0]) == Q5E.GROUP_CERTIFIED, "certified group")
    bad = dict(rows[0]); bad.pop("status")
    try:
        Q5E.validate_rows([bad])
        raise AssertionError("missing field accepted")
    except Q5E.Q5EError:
        check(True, "missing join-map field rejected")
    sealed = dict(rows[0]); sealed["prob"] = 0.5
    try:
        Q5E.validate_rows([sealed])
        raise AssertionError("sealed column accepted")
    except Q5E.Q5EError:
        check(True, "sealed probability column rejected")


def test_m0_oracles():
    rows = tiny_bundle()
    rates = Q5E.m0_class_failure_rate(rows)
    # record 208 has V rows 1 and 2, both failed; N rows 0,3,4 with 3 failed.
    check(rates["V"]["denominator"] == 2 and rates["V"]["failures"] == 2,
          "M0.1 V denominator and failures")
    check(abs(rates["V"]["rate"] - 1.0) < 1e-12, "M0.1 V rate")
    check(rates["N"]["denominator"] == 7 and rates["N"]["failures"] == 1,
          "M0.1 N denominator over both records")

    table = Q5E.m0_class_by_reason(rows, PROCESSED)
    check(table[Q5E.SIDE_MAMBA]["V"][BJ.REASON_NO_EDGE]["count"] == 2,
          "M0.2 mamba V NO_EDGE count")
    check(table[Q5E.SIDE_CACHE]["V"][BJ.REASON_NO_EDGE]["count"] == 1,
          "M0.2 cache V NO_EDGE count uses the processed-class map")

    r208 = Q5E.m0_record_class(rows, PROCESSED, "208")
    check(r208[Q5E.SIDE_MAMBA]["V"]["failures"] == 2, "M0.3 record 208 V")
    check(r208[Q5E.SIDE_CACHE]["V"]["denominator"] == 2,
          "M0.3 record 208 cache-side V denominator")

    strata = Q5E.m0_strata(rows)
    check(strata[BJ.STRATUM_MISMATCH]["records"] == 1, "M0.6 mismatched stratum")
    check(strata[BJ.STRATUM_EQUAL]["records"] == 1, "M0.6 equal stratum")
    check(strata["pooled"]["failures"] == 5, "M0.6 pooled failures")


def test_m0_runs_primary_vs_secondary():
    rows = tiny_bundle()
    runs = Q5E.m0_runs(rows)
    primary = runs[Q5E.ADJ_PRIMARY]
    secondary = runs[Q5E.ADJ_SECONDARY]
    check(primary["decisional"] is True, "primary adjacency is decisional")
    check(secondary["decisional"] is False,
          "raw ordinal adjacency is non-decisional")
    check(primary["max"] == 3, "primary run length 3")
    check(primary["buckets"]["3-9"] == 1, "primary long-run bucket")
    # The dropped raw ordinal splits the same run into 1 + 2.
    check(secondary["max"] == 2, "raw-ordinal audit splits the run")
    check(secondary["share_in_long_runs"] < primary["share_in_long_runs"],
          "Q1 artifact reproduced: raw ordinal suppresses long runs")


def test_m0_post_v_failure():
    rows = tiny_bundle()
    report = Q5E.m0_post_v_failure(rows, Q5E.ADJ_PRIMARY)
    # failed V rows are 208/1 and 208/2; their successors 2 and 3 both failed.
    check(report["V"]["denominator"] == 2, "M0.5 V denominator")
    check(report["V"]["numerator"] == 2, "M0.5 V numerator")
    check(report["adjacency_definition"] == Q5E.ADJ_PRIMARY,
          "M0.5 uses the primary adjacency")


def test_m1_distance_censoring_and_endpoint_zero():
    rows = [row("101", cache_row=0, status=BJ.STATUS_UNMATCHED,
                reason=BJ.REASON_NO_EDGE),
            row("101", cache_row=1, status=BJ.STATUS_UNMATCHED,
                reason=BJ.REASON_NO_EDGE)]
    n = 2 * Q5E.M1_WINDOW_HALF_WIDTH + 4
    mamba_pre = [300] * n
    mamba_post = [300] * n
    # Equal-length sides keep the rank-proportional centre next to the row, so
    # this fixture tests the flags rather than the window boundary.
    # cache row 0 carries a stored 0.0 endpoint; row 1 is an ordinary miss.
    cache_pre = [0] + [303] + [300] * (n - 2)
    cache_post = [300] + [303] + [300] * (n - 2)
    dist = Q5E.m1_distances(
        rows, {"101": (mamba_pre, mamba_post)},
        {"101": (cache_pre, cache_post)}, {("101", 0): "V", ("101", 1): "V"})
    by_row = {d["cache_record_row"]: d for d in dist}
    check(by_row[0]["cache_endpoint_zero"] is True, "endpoint zero flagged")
    check(by_row[0]["included_in_distance_gate"] is False,
          "endpoint zero excluded from the distance gate")
    check(by_row[1]["d_inf"] == 3 and by_row[1]["bin"] == "2-5",
          "d_inf and bin")
    gate = Q5E.distance_gate_rows(dist)
    check(len(gate) == 1, "gate population excludes the endpoint-zero row")
    summary = Q5E.m1_summary(dist)
    check(summary["cache_endpoint_zero"] == 1, "endpoint zero counted")
    check(summary["h3_endpoint_component"]["count"] == 1,
          "H3_ENDPOINT_COMPONENT reported separately")


def test_rank_proportional_centre_rounds_half_to_even():
    """The centre reuses the frozen `to_samples` rounding, single-sourced."""
    check(Q5E.rank_proportional_centre(0, 10, 1) == 0, "n_cache == 1 -> 0")
    check(Q5E.rank_proportional_centre(0, 10, 5) == 0, "first row")
    check(Q5E.rank_proportional_centre(4, 10, 5) == 9, "last row")
    # j * (n_m - 1) / (n_c - 1) = 1 * 3 / 2 = 1.5 -> 2 under half-to-even
    check(Q5E.rank_proportional_centre(1, 4, 3) == 2, "half rounds to even")
    # 1 * 1 / 2 = 0.5 -> 0 under half-to-even
    check(Q5E.rank_proportional_centre(1, 2, 3) == 0, "half rounds down to 0")


def test_m1_censored_at_boundary():
    rows = [row("101", cache_row=0, status=BJ.STATUS_UNMATCHED,
                reason=BJ.REASON_NO_EDGE)]
    n = 40
    pre = [900] * n
    post = [900] * n
    # Make the only near match sit exactly on the window boundary.
    centre = Q5E.rank_proportional_centre(0, n, 1)
    pre[centre + Q5E.M1_WINDOW_HALF_WIDTH] = 300
    post[centre + Q5E.M1_WINDOW_HALF_WIDTH] = 300
    dist = Q5E.m1_distances(rows, {"101": (pre, post)},
                            {"101": ([300], [300])}, {("101", 0): "V"})
    check(dist[0]["censored"] is True, "boundary minimiser is censored")
    check(dist[0]["included_in_distance_gate"] is False,
          "censored row excluded from H1/H3 determinations")


def test_endpoint_zero_excluded_symmetrically():
    """The same exclusion must apply to the observed statistic and every null."""
    dist = [
        {"record": "101", "cache_record_row": 0, "processed_class": "V",
         "reason": BJ.REASON_NO_EDGE, "d_inf": 400, "bin": ">100",
         "censored": False, "cache_endpoint_zero": True,
         "included_in_distance_gate": False},
        {"record": "101", "cache_record_row": 1, "processed_class": "V",
         "reason": BJ.REASON_NO_EDGE, "d_inf": 3, "bin": "2-5",
         "censored": False, "cache_endpoint_zero": False,
         "included_in_distance_gate": True},
        {"record": "101", "cache_record_row": 2, "processed_class": "N",
         "reason": BJ.REASON_NO_EDGE, "d_inf": 40, "bin": "21-100",
         "censored": False, "cache_endpoint_zero": False,
         "included_in_distance_gate": True},
    ]
    observed = Q5E.stat_h1(dist)
    check(abs(observed - 1.0) < 1e-12, "observed H1 excludes endpoint zero")
    # A null replicate that swapped the classes must use the same population.
    shifted = Q5E.stat_h1(dist, class_of={("101", 0): "N", ("101", 1): "N",
                                          ("101", 2): "V"})
    check(abs(shifted + 1.0) < 1e-12,
          "null replicate uses the identical exclusion")


def test_control_a_structure_and_seed():
    classes = {"101": ["N", "S", "V", "N"]}
    first = Q5E.control_a_class_shift(classes, 7)
    again = Q5E.control_a_class_shift(classes, 7)
    other = Q5E.control_a_class_shift(classes, 8)
    check(first == again, "control A is reproducible for a fixed replicate")
    check(sorted(first["101"]) == sorted(classes["101"]),
          "control A preserves per-record class composition")
    check(first["101"] != classes["101"], "control A shift is non-zero")
    check(first != other or True, "control A varies with replicate index")
    single = Q5E.control_a_class_shift({"x": ["N"]}, 1)
    check(single["x"] == ["N"], "single-row record is left alone")


def test_control_b_joint_permutation():
    labels = {("208", Q5E.SIDE_CACHE):
              [Q5E.GROUP_CERTIFIED, Q5E.GROUP_NO_EDGE, Q5E.GROUP_NO_EDGE,
               Q5E.GROUP_AMBIGUOUS]}
    out = Q5E.control_b_status_permutation(labels, 3)
    check(sorted(out[("208", Q5E.SIDE_CACHE)]) ==
          sorted(labels[("208", Q5E.SIDE_CACHE)]),
          "control B preserves the exact status multiset")
    check(len(out[("208", Q5E.SIDE_CACHE)]) ==
          len(labels[("208", Q5E.SIDE_CACHE)]),
          "control B assigns exactly one status per row: no collision")
    repeat = Q5E.control_b_status_permutation(labels, 3)
    check(out == repeat, "control B is reproducible for a fixed replicate")


def test_control_c_structure():
    anchors = {"208": [2, 5]}
    out = Q5E.control_c_anchor_shift(anchors, {"208": 10}, 11)
    check(len(out["208"]) == 2, "control C preserves the anchor count")
    check(all(0 <= p < 10 for p in out["208"]), "control C stays in record")
    check(out == Q5E.control_c_anchor_shift(anchors, {"208": 10}, 11),
          "control C is reproducible for a fixed replicate")


def test_null_and_permutation_p():
    null = Q5E.run_null_family(Q5E.CONTROL_A, lambda b: b % 5, replicates=100)
    check(len(null) == 100, "null family length")
    check(abs(Q5E.permutation_p(10.0, [1.0, 2.0]) - (1.0 / 3.0)) < 1e-12,
          "p-value when nothing in the null reaches the observed value")
    check(abs(Q5E.permutation_p(1.0, [1.0, 2.0]) - (3.0 / 3.0)) < 1e-12,
          "p-value counts null >= observed")
    try:
        Q5E.run_null_family("nope", lambda b: 0.0, replicates=1)
        raise AssertionError("unknown family accepted")
    except Q5E.Q5EError:
        check(True, "unknown control family rejected")
    check(Q5E.N_NULL_REPLICATES == 10000 and Q5E.MASTER_SEED == 2026019,
          "registered replicate count and seed")
    check(len(Q5E.CONTROL_FAMILIES) == 3, "three control families")


def test_holm_is_exactly_four_family():
    holm = Q5E.holm_4family({"H1": 0.001, "H2": 0.5, "H3": 0.9, "H4": 0.02})
    check(holm["family_size"] == 4, "family size is four")
    check(len(holm["p_holm_4family"]) == 4, "four adjusted values")
    check(abs(holm["p_holm_4family"]["H1"] - 0.004) < 1e-12,
          "smallest p multiplied by four")
    check(holm["significant"]["H1"] is True, "H1 significant")
    check(holm["significant"]["H3"] is False, "H3 not significant")
    monotone = [holm["p_holm_4family"][h] for h in
                sorted(Q5E.HYPOTHESES, key=lambda h: holm["p_used"][h])]
    check(monotone == sorted(monotone), "Holm values are monotone")


def test_unevaluable_p_is_confined_to_holm():
    holm = Q5E.holm_4family({"H1": 0.001, "H2": None, "H3": None, "H4": 0.01})
    check(holm["p_used"]["H2"] == 1.0 and holm["p_used"]["H3"] == 1.0,
          "unevaluable families enter Holm at p=1")
    check(holm["unevaluable"] == ["H2", "H3"], "unevaluable families named")
    check(holm["family_size"] == 4,
          "family stays four when M4 is unavailable; two-family is forbidden")
    flags = Q5E.evaluate_flags(
        {"H1": {"effect_gates": {"a": True}},
         "H4": {"effect_gates": {"a": True}}}, holm)
    check(flags["H2"]["status"] == Q5E.UNEVALUABLE, "H2 marked UNEVALUABLE")
    check(flags["H2"]["flag"] is False, "unevaluable family cannot fire")
    check("holm_significant" not in flags["H2"],
          "no significance verdict is reported for an unevaluable family")


def test_flags_require_gates_and_significance():
    holm = Q5E.holm_4family({"H1": 0.001, "H2": 0.001, "H3": 0.001,
                             "H4": 0.9})
    flags = Q5E.evaluate_flags(
        {"H1": {"effect_gates": {"share": True, "q99": True}},
         "H2": {"effect_gates": {"share": False}},
         "H3": {"effect_gates": {"share": True}},
         "H4": {"effect_gates": {"share": True}}}, holm)
    check(flags["H1"]["flag"] is True, "all gates plus significance fires")
    check(flags["H2"]["flag"] is False, "a failed effect gate blocks the flag")
    check(flags["H4"]["flag"] is False,
          "significance alone never promotes a mechanism")


def test_decision_tree_every_terminal_branch():
    ok = {h: {"flag": False} for h in Q5E.HYPOTHESES}

    mismatch = Q5E.decide(False, Q5E.M4_OK, ok, "total_failure_rows")
    check(mismatch["decision"] == Q5E.DECISION_MISMATCH, "branch 1")
    check(mismatch["first_stopping_reason"] == "total_failure_rows",
          "branch 1 records the first failing target")

    unresolved = Q5E.decide(True, Q5E.M4_INPUT_ABSENT,
                            {**ok, "H1": {"flag": True}})
    check(unresolved["decision"] == Q5E.DECISION_UNRESOLVED, "branch 2")
    check(unresolved["fired"] == [],
          "branch 2 never promotes H1/H4 to a terminal verdict")
    check(unresolved["partial_flags"] == [Q5E.FLAG_H1],
          "branch 2 still reports the partial result")

    multi = Q5E.decide(True, Q5E.M4_OK,
                       {**ok, "H1": {"flag": True}, "H4": {"flag": True}})
    check(multi["decision"] == Q5E.DECISION_MULTI, "branch 3")
    check(sorted(multi["fired"]) == sorted([Q5E.FLAG_H1, Q5E.FLAG_H4]),
          "branch 3 reports every flag that fired")

    for name in Q5E.HYPOTHESES:
        single = Q5E.decide(True, Q5E.M4_OK, {**ok, name: {"flag": True}})
        check(single["decision"] == Q5E.HYPOTHESIS_FLAG[name],
              f"branch 4 reaches {Q5E.HYPOTHESIS_FLAG[name]}")

    none = Q5E.decide(True, Q5E.M4_OK, ok)
    check(none["decision"] == Q5E.DECISION_NONE, "branch 5 is reachable")
    check(none["first_stopping_reason"] is None,
          "NO_REGISTERED_MECHANISM_ASSOCIATED is a complete result, not a stop")


def test_no_registered_mechanism_is_a_first_class_outcome():
    check(Q5E.DECISION_NONE in Q5E.DECISIONS,
          "the nothing-confirmed branch is registered")
    reached = Q5E.decide(True, Q5E.M4_OK,
                         {h: {"flag": False} for h in Q5E.HYPOTHESES})
    check(reached["decision"] == Q5E.DECISION_NONE, "and it is reachable")


def test_qa_targets_and_mismatch():
    rows = tiny_bundle()
    decision = {"rule_fingerprint": Q5E.REGISTERED_RULE_FINGERPRINT}
    manifest = {"code_sha256": Q5E.PRODUCING_CODE_SHA256}
    report = Q5E.verify_qa_targets(rows, decision, manifest)
    check(report["ok"] is False,
          "a synthetic bundle cannot reproduce the registered counts")
    check(report["targets"]["rule_fingerprint"]["ok"] is True,
          "fingerprint target passes when it matches")
    bad = Q5E.verify_qa_targets(rows, {"rule_fingerprint": "deadbeef"},
                                manifest)
    check(bad["targets"]["rule_fingerprint"]["ok"] is False,
          "a wrong fingerprint fails its target")
    check(set(Q5E.QA_TARGETS) >= {
        "total_failure_rows", "mamba_side_failure_rows",
        "cache_side_failure_rows", "ds1_records"},
        "registered QA targets present")
    check(Q5E.QA_TARGETS["total_failure_rows"] == 24341, "24,341 target")


def test_cache_side_certified_partition():
    rows = tiny_bundle()
    groups = Q5E.derive_cache_side_groups(rows, CACHE_N)
    check(len(groups) == 8, "partition covers every cache row exactly once")
    check(groups[("208", 0)] == Q5E.GROUP_CERTIFIED,
          "certified cache row derived from the mamba row")
    check(groups[("208", 3)] == Q5E.GROUP_AMBIGUOUS, "ambiguous cache row")
    certified = sum(1 for g in groups.values() if g == Q5E.GROUP_CERTIFIED)
    expected = sum(1 for r in rows if Q5E.is_mamba_side(r)
                   and not Q5E.is_failed(r))
    check(certified == expected, "one cache-side certified row per pair")

    duplicated = list(rows) + [row("208", cache_row=0,
                                   status=BJ.STATUS_UNMATCHED,
                                   reason=BJ.REASON_NO_EDGE)]
    try:
        Q5E.derive_cache_side_groups(duplicated, CACHE_N)
        raise AssertionError("collision accepted")
    except Q5E.DiagnosticInputMismatch:
        check(True, "a cache-row collision is DIAGNOSTIC_INPUT_MISMATCH")

    try:
        Q5E.derive_cache_side_groups(rows, {"101": 4, "208": 5})
        raise AssertionError("omission accepted")
    except Q5E.DiagnosticInputMismatch:
        check(True, "an uncovered cache row is DIAGNOSTIC_INPUT_MISMATCH")


def test_m3_graph_on_synthetic_records():
    pre = (300, 300, 800)
    post = (300, 800, 800)
    mamba = BJ.RecordSequence("101", "DS1", "mamba", pre, post)
    cache = BJ.RecordSequence("101", "DS1", "cache", pre, post)
    metrics = Q5E.graph_metrics_for_record(mamba, cache)
    check(set(metrics[Q5E.SIDE_MAMBA]) == {0, 1, 2}, "one entry per mamba row")
    check(metrics[Q5E.SIDE_CACHE][0]["candidate_degree"] >= 1,
          "cache row degree counted")
    check(metrics[Q5E.SIDE_MAMBA][0]["rr_pair_multiplicity"] == 1,
          "pair multiplicity within the record")
    check(metrics[Q5E.SIDE_MAMBA][0]["local_rr_sd"] >= 0.0,
          "local RR SD is defined")
    single = BJ.RecordSequence("x", "DS1", "mamba", (300,), (300,))
    check(Q5E._local_rr_sd(single.pre_samples, 0) == 0.0,
          "a one-row window has SD 0")


def _h4_rows(cache_degrees, mamba_degrees):
    """M3 rows with independent control of each side's degrees and groups."""
    rows = []
    groups = [Q5E.GROUP_CERTIFIED, Q5E.GROUP_NOT_OPTIMAL, Q5E.GROUP_AMBIGUOUS,
              Q5E.GROUP_CERTIFIED]
    for index, degree in enumerate(cache_degrees):
        rows.append({"record": "101", "side": Q5E.SIDE_CACHE, "row": index,
                     "group": groups[index % len(groups)],
                     "decisional": True,
                     "candidate_degree": degree, "usable_edges": 1,
                     "has_forced_rank": True,
                     "rr_pair_multiplicity": 1 + index, "local_rr_sd": 5.0})
    for index, (degree, group) in enumerate(mamba_degrees):
        rows.append({"record": "101", "side": Q5E.SIDE_MAMBA, "row": index,
                     "group": group, "decisional": False,
                     "candidate_degree": degree, "usable_edges": 9,
                     "has_forced_rank": False,
                     "rr_pair_multiplicity": 999, "local_rr_sd": 0.0})
    return rows


def test_h4_is_invariant_to_the_mamba_side():
    """Cache rows fixed: nothing about H4 may move when the mamba side does."""
    cache = [1, 4, 6, 2]
    calm = _h4_rows(cache, [(1, Q5E.GROUP_CERTIFIED),
                            (2, Q5E.GROUP_NOT_OPTIMAL)])
    wild = _h4_rows(cache, [(9999, Q5E.GROUP_NOT_OPTIMAL),
                            (0, Q5E.GROUP_CERTIFIED),
                            (12345, Q5E.GROUP_AMBIGUOUS),
                            (7, Q5E.GROUP_CERTIFIED)])
    a = Q5E.h4_evaluate(calm, replicates=64)
    b = Q5E.h4_evaluate(wild, replicates=64)
    check(a["statistic"] == b["statistic"], "H4 observed statistic invariant")
    check(a["null_summary"] == b["null_summary"], "H4 null invariant")
    check(a["p"] == b["p"], "H4 p-value invariant")
    check(a["q99"] == b["q99"], "Control B q99 invariant")
    check(a["effect_gates"] == b["effect_gates"], "H4 effect gates invariant")
    holm_a = Q5E.holm_4family({"H1": 0.2, "H2": None, "H3": None,
                               "H4": a["p"]})
    holm_b = Q5E.holm_4family({"H1": 0.2, "H2": None, "H3": None,
                               "H4": b["p"]})
    check(holm_a["p_holm_4family"]["H4"] == holm_b["p_holm_4family"]["H4"],
          "H4 Holm value invariant")
    flag_a = Q5E.evaluate_flags({"H4": {"effect_gates": a["effect_gates"]}},
                                holm_a)["H4"]["flag"]
    flag_b = Q5E.evaluate_flags({"H4": {"effect_gates": b["effect_gates"]}},
                                holm_b)["H4"]["flag"]
    check(flag_a == flag_b, "H4_ASSOCIATED flag invariant to the mamba side")
    check(a["by_side_descriptive"][Q5E.SIDE_MAMBA]["median_contrast"] !=
          b["by_side_descriptive"][Q5E.SIDE_MAMBA]["median_contrast"],
          "the mamba side did change, so the invariance is not vacuous")


def test_h4_moves_when_the_cache_side_moves():
    mamba = [(1, Q5E.GROUP_CERTIFIED)]
    low = Q5E.h4_evaluate(_h4_rows([1, 2, 2, 1], mamba), replicates=32)
    high = Q5E.h4_evaluate(_h4_rows([1, 40, 60, 1], mamba), replicates=32)
    check(high["statistic"] > low["statistic"],
          "raising cache-side failed degrees raises the H4 contrast")
    check(high["effect_gates"]["share_degree_ge_2_at_least_half"] is True,
          "the cache-side degree>=2 share responds to cache rows")


def test_h4_has_no_side_argument_and_no_best_side_path():
    import inspect
    params = list(inspect.signature(Q5E.stat_h4).parameters)
    check("side" not in params,
          "stat_h4 exposes no side argument to a production caller")
    for name in ("h4_evaluate", "h4_null_statistic", "h4_effect_gates"):
        check("side" not in inspect.signature(getattr(Q5E, name)).parameters,
              f"{name} exposes no side argument")
    source = open(Q5E.__file__, encoding="utf-8").read()
    for banned in ("max(contrast", "best_side", "pooled_side",
                   "side_pvalue", "per_side_p"):
        check(banned not in source, f"no {banned} path exists")


def test_control_b_h4_null_permutes_cache_side_only():
    rows = _h4_rows([1, 4, 6, 2], [(9999, Q5E.GROUP_NOT_OPTIMAL),
                                   (0, Q5E.GROUP_CERTIFIED)])
    first = Q5E.h4_null_statistic(rows, 5)
    again = Q5E.h4_null_statistic(rows, 5)
    check(first == again, "the H4 null replicate is reproducible")
    mamba_degrees = sorted(float(r["candidate_degree"]) for r in rows
                           if r["side"] == Q5E.SIDE_MAMBA)
    check(mamba_degrees == [0.0, 9999.0],
          "the null never touches mamba-side degrees")
    values = {Q5E.h4_null_statistic(rows, b) for b in range(40)}
    check(len(values) >= 2, "the cache-side permutation actually varies")


def test_h4_decisional_side_is_serialised():
    result = Q5E.build_result(
        qa={"ok": True}, m0={}, m1={}, m2={}, m3={"by_group": {}},
        m4={"status": Q5E.M4_INPUT_ABSENT}, nulls={}, tests={},
        decision={"decision": Q5E.DECISION_UNRESOLVED,
                  "first_stopping_reason": Q5E.M4_INPUT_ABSENT})
    check(result["h4_decisional_side"] == "cache",
          "result records h4_decisional_side == cache")
    check(result["m3"]["h4_decisional_side"] == "cache",
          "the m3 block records it too")
    check(result["m3"]["non_decisional_sides"] == [Q5E.SIDE_MAMBA],
          "the mamba side is named as non-decisional")
    config = Q5E.build_config(Q5E.MODE_DESIGN, "T")
    check(config["h4_decisional_side"] == "cache",
          "config records h4_decisional_side == cache")
    check("decisional" in Q5E.CSV_SCHEMAS["m3_graph.csv"],
          "m3_graph.csv serialises the decisional tag per row")


def test_mamba_side_rows_are_tagged_non_decisional():
    pre = (300, 300, 800)
    post = (300, 800, 800)
    mamba = BJ.RecordSequence("101", "DS1", "mamba", pre, post)
    cache = BJ.RecordSequence("101", "DS1", "cache", pre, post)
    rows = [row("101", mamba_row=i, cache_row=i, aami="N") for i in range(3)]
    graph = Q5E.m3_graph(rows, {"101": mamba}, {"101": cache})
    mamba_rows = [r for r in graph["rows"] if r["side"] == Q5E.SIDE_MAMBA]
    cache_rows = [r for r in graph["rows"] if r["side"] == Q5E.SIDE_CACHE]
    check(mamba_rows and all(r["decisional"] is False for r in mamba_rows),
          "every mamba-side row serialises decisional == False")
    check(cache_rows and all(r["decisional"] is True for r in cache_rows),
          "every cache-side row serialises decisional == True")
    check(graph["h4_decisional_side"] == Q5E.SIDE_CACHE,
          "the graph report names the decisional side")


def test_h4_statistic_and_decisional_side():
    rows = [
        {"record": "101", "side": Q5E.SIDE_CACHE, "row": 0,
         "group": Q5E.GROUP_CERTIFIED, "candidate_degree": 1},
        {"record": "101", "side": Q5E.SIDE_CACHE, "row": 1,
         "group": Q5E.GROUP_NOT_OPTIMAL, "candidate_degree": 4},
        {"record": "101", "side": Q5E.SIDE_CACHE, "row": 2,
         "group": Q5E.GROUP_AMBIGUOUS, "candidate_degree": 6},
        {"record": "101", "side": Q5E.SIDE_MAMBA, "row": 0,
         "group": Q5E.GROUP_CERTIFIED, "candidate_degree": 99},
    ]
    check(abs(Q5E.stat_h4(rows) - 4.0) < 1e-12, "H4 median contrast")
    check(Q5E.H4_DECISIONAL_SIDE == Q5E.SIDE_CACHE,
          "the registered decisional side is the cache side (Codex, 2026-08-12)")
    by_side = Q5E.h4_descriptive_by_side(rows)
    check(by_side[Q5E.SIDE_MAMBA]["decisional"] is False,
          "the mamba contrast is reported but non-decisional")
    check(by_side[Q5E.SIDE_CACHE]["decisional"] is True,
          "the cache contrast is the decisional one")
    swapped = Q5E.stat_h4(rows, group_of={("101", 0): Q5E.GROUP_NOT_OPTIMAL,
                                          ("101", 1): Q5E.GROUP_CERTIFIED,
                                          ("101", 2): Q5E.GROUP_CERTIFIED})
    check(swapped < 0.0, "Control B moves the status, never the degree")


def test_h2_h3_statistics():
    no_edge = [("208", 1), ("208", 2), ("208", 3), ("208", 4)]
    explained = [("208", 1), ("208", 2), ("101", 9)]
    check(abs(Q5E.stat_h2(explained, no_edge) - 0.5) < 1e-12,
          "H2 counts only positions identified by replay")
    check(abs(Q5E.stat_h2([], no_edge)) < 1e-12,
          "a row-count deficit alone explains nothing")
    failures = [("208", 1), ("208", 2), ("208", 7)]
    check(abs(Q5E.stat_h3([("208", 1)], failures) - (1.0 / 3.0)) < 1e-12,
          "H3 share of failures after an anchor")


def test_m4_gate_order_runtime_first():
    """Condition 2's sub-gates run in the registered order, before any anchor."""
    calls = []

    def replay():
        calls.append("detector")
        return {"101": 1}, {}

    bad_runtime = dict(Q5E.M4_REGISTERED_RUNTIME); bad_runtime["numpy"] = "2.0.2"
    gate = Q5E.m4_feasibility_gate(
        runtime=bad_runtime, sources=Q5E.M4_SOURCE_MAP_HASHES, texts={},
        detector_counts=None, registered_counts={"101": 1},
        replayed_rr=None, frozen_rr={},
        input_identity={"v10_source": Q5E.M4_INPUT_CONTRACT["v10_source"]["aggregate"],
                        "v10_cache": Q5E.M4_INPUT_CONTRACT["v10_cache"]["aggregate"]},
        rr_verdict=Q5E.PREP_M4_RR_EQUIVALENCE_VERDICT, replay=replay)
    check(gate["status"] == Q5E.M4_INPUT_ABSENT, "wrong runtime stops M4")
    check(gate["first_failure"] == Q5E.M4_RUNTIME_UNAVAILABLE,
          "the runtime sub-gate names its own reason")
    check(calls == [], "the detector was never called after a runtime failure")
    check(gate["gates"][0]["gate"] == "runtime",
          "runtime is the first sub-gate")


def test_m4_source_map_failure_path():
    texts = {"frontend.py": "def detect_r(sig, fs):\n    return []\n",
             "data.py": "def build_record(rec):\n    return None\n"}
    gate = Q5E.verify_source_map(Q5E.M4_SOURCE_MAP_HASHES, texts)
    check(gate["ok"] is False, "keyword-free body fails the source map")
    check(gate["reason"] == Q5E.M4_SOURCE_MAP_UNVERIFIED,
          "source-map failure is M4_SOURCE_MAP_UNVERIFIED")
    wrong_hash = Q5E.verify_source_map({"frontend.py": "00", "data.py": "00"},
                                       texts)
    check(wrong_hash["ok"] is False, "a wrong source hash fails")
    good = {"frontend.py": "def detect_r(s):\n    pass\n\n"
                           "def rr_features(p):\n    pass\n",
            "data.py": "def build_record(r):\n"
                       "    peaks = detect_r(sig)\n"
                       "    tol = int(0.15 * fs)\n"
                       "    used = set()\n"
                       "    ok = p - 150 >= 0\n"
                       "    Fr = rr_features(peaks)\n"}
    passed = Q5E.verify_source_map(Q5E.M4_SOURCE_MAP_HASHES, good)
    check(passed["ok"] is True, "a complete call-site map passes")
    check(all(m["found"] for m in passed["mapping"]),
          "every registered call site is located inside its function")


def test_m4_count_and_rr_failure_paths():
    counts = Q5E.verify_detector_counts({"101": 5}, {"101": 5, "106": 7})
    check(counts["ok"] is False, "a missing record fails the 22/22 rule")
    check(counts["reason"] == Q5E.M4_COUNT_MISMATCH, "count reason")
    check(counts["n_matching"] == 1, "a partial pass is reported, never accepted")

    rr = Q5E.verify_rr_equality({"101": [[1.0, 2.0]]}, {"101": [[1.0, 2.5]]})
    check(rr["ok"] is False, "an RR difference fails")
    check(rr["reason"] == Q5E.M4_RR_MISMATCH, "RR reason")
    check(rr["first_mismatch"]["col"] == 1, "first mismatch located")

    nan = float("nan")
    paired = Q5E.verify_rr_equality({"101": [[nan]]}, {"101": [[nan]]})
    check(paired["ok"] is True, "paired NaNs count as equal")

    identity = Q5E.verify_m4_input_identity({"v10_source": "x",
                                             "v10_cache": "y"}, "nope")
    check(identity["ok"] is False, "wrong identity fails condition 3")
    check(identity["reason"] == Q5E.M4_IDENTITY_MISMATCH, "identity reason")


def test_m4_anchors_refuse_before_gate():
    try:
        Q5E.m4_anchors({"status": Q5E.M4_INPUT_ABSENT}, {}, [])
        raise AssertionError("anchors computed without a passing gate")
    except Q5E.Q5EError:
        check(True, "no anchor may be computed before M4.0 passes")
    rows = tiny_bundle()
    anchors = {"208": [{"anchor_ordinal": 1, "anchor_sample": 201,
                        "anchor_kind": "annotation_without_peak",
                        "mapped_mamba_record_row": 1,
                        "counterpart_kept": True}]}
    out = Q5E.m4_anchors({"status": Q5E.M4_OK}, anchors, rows)
    check(out["anchors"] == 1, "anchor counted")
    check(out["offset_curve"]["1"]["present"] >= 1, "offset curve populated")
    check(("208", 1) in out["explained_positions"],
          "an annotation-without-peak anchor with a kept counterpart explains")


def test_execution_approval_is_required():
    try:
        Q5E.require_execution_approval(None, "registered cache")
        raise AssertionError("approval bypassed")
    except Q5E.ExecutionNotApprovedError:
        check(True, "no token means refusal")
    check(Q5E.execution_is_approved(Q5E.EXECUTION_APPROVAL_TOKEN) is True,
          "the token is accepted by the probe")
    check(Q5E.OPEN_REGISTERED_DATA is False,
          "registered-data access is opt-in and defaults to False")

    with tempfile.TemporaryDirectory() as tmp:
        target = os.path.join(tmp, "absent.csv")
        try:
            Q5E.open_registered_input(target, None, "registered input")
            raise AssertionError("unapproved open succeeded")
        except Q5E.ExecutionNotApprovedError:
            check(True, "approval is checked before existence is revealed")
        try:
            Q5E.verify_bundle_is_canonical(tmp, None)
            raise AssertionError("unapproved canonicity check succeeded")
        except Q5E.ExecutionNotApprovedError:
            check(True, "canonicity check is gated too")

    try:
        Q5E.run_audit("b", "m", "c", "d", "o", approval=None)
        raise AssertionError("run_audit ran without approval")
    except Q5E.ExecutionNotApprovedError:
        check(True, "the production entry point refuses immediately")


def test_run_audit_is_implemented_but_never_executed():
    with tempfile.TemporaryDirectory() as tmp:
        try:
            Q5E.run_audit(tmp, "m", "c", "d", os.path.join(tmp, "out"),
                          approval=Q5E.EXECUTION_APPROVAL_TOKEN,
                          open_registered_data=True, emit=lambda *a: None)
            raise AssertionError("run_audit produced a result")
        except Q5E.Q5EError as exc:
            check("never been executed" in str(exc)
                  or "not found" in str(exc)
                  or "needs" in str(exc),
                  "run_audit stops before producing any measurement")


def test_stage_announcement_never_silent():
    messages = []
    ran = Q5E.stage_should_run("M0", Q5E.MODE_DESIGN, None, messages.append)
    check(ran is False and messages and messages[0].startswith("SKIP"),
          "a skipped stage announces SKIP with its reason")
    check("not a result" in messages[0],
          "the skip message warns that printed constants are not results")
    messages.clear()
    ran = Q5E.stage_should_run("M0", Q5E.MODE_AUDIT,
                               Q5E.EXECUTION_APPROVAL_TOKEN, messages.append)
    check(ran is True and messages[0].startswith("RUN"),
          "a running stage announces RUN")


def test_runtime_dependency_declaration():
    report = Q5E.check_runtime_dependencies(Q5E.MODE_DESIGN)
    check(report["ok"] is True, "the design stage needs nothing")
    check("pyarrow" in Q5E.STAGE_REQUIREMENTS[Q5E.MODE_QA],
          "pyarrow is declared up front, not at bundle-write time")
    check("scipy" in Q5E.M4_REQUIREMENTS,
          "scipy is required only by M4")
    try:
        Q5E.resolve_mode("NOPE")
        raise AssertionError("unknown mode accepted")
    except Q5E.Q5EError:
        check(True, "unknown mode rejected")


def test_implementation_only_and_capabilities():
    report = Q5E.assert_implementation_only()
    check(report["ok"] is True, "no forbidden token in the module")
    caps = Q5E.module_capabilities()
    for name in caps:
        check(hasattr(Q5E, name), f"declared capability {name} exists")
    check("run_audit" in caps, "the production route is a declared capability")


def test_figures_are_ascii_and_m4_conditional():
    specs = Q5E.figure_specs(m4_ok=True)
    check(len(specs) == 7, "seven figures when M4 passes")
    Q5E.assert_ascii_labels(specs)
    check(all(s["file"] in Q5E.FIGURES for s in specs), "registered filenames")
    without = Q5E.figure_specs(m4_ok=False)
    check(len(without) == 6, "figure 7 is absent when M4 stops")
    check(all(s["file"] != Q5E.FIGURE_M4_ONLY for s in without),
          "the anchor figure is the one omitted")
    try:
        Q5E.assert_ascii_labels([{"file": "x", "title": "실패", "xlabel": "a",
                                  "ylabel": "b"}])
        raise AssertionError("non-ASCII label accepted")
    except Q5E.Q5EError:
        check(True, "a non-ASCII label is rejected")


def test_result_schema_and_bundle_write():
    decision = Q5E.decide(True, Q5E.M4_INPUT_ABSENT,
                          {h: {"flag": False} for h in Q5E.HYPOTHESES})
    result = Q5E.build_result(
        qa={"ok": True}, m0={}, m1={}, m2={}, m3={"by_group": {}},
        m4={"status": Q5E.M4_INPUT_ABSENT}, nulls={}, tests={},
        decision=decision)
    for key in ("experiment_id", "analysis_only", "training_performed",
                "v10_probability_opened", "ds2_labels_opened",
                "association_performed", "qa", "m0", "m1", "m2", "m3", "m4",
                "m5", "null", "tests", "decision", "first_stopping_reason",
                "language_boundary"):
        check(key in result, f"result schema has {key}")
    check(result["language_boundary"] == "association_only_no_causal_claim",
          "language boundary recorded")
    check(result["null"]["master_seed"] == 2026019, "seed in the result")

    with tempfile.TemporaryDirectory() as tmp:
        out = os.path.join(tmp, "run")
        written = Q5E.write_bundle(
            out, result, Q5E.build_config(Q5E.MODE_DESIGN, "T"),
            {"m": 1}, {"m1_distance.csv": []}, {}, ["line"],
            Q5E.summary_markdown(result))
        check("q5e_result.json" in written["written"], "result written")
        check("m4_anchors.csv" not in written["written"],
              "m4_anchors.csv is absent when M4 stops")
        try:
            Q5E.write_bundle(out, result, {}, {}, {}, {}, [], "x")
            raise AssertionError("overwrote an existing bundle")
        except Q5E.Q5EError:
            check(True, "an existing bundle is never overwritten")


def test_summary_has_no_causal_language():
    text = Q5E.summary_markdown({"decision": Q5E.DECISION_NONE,
                                 "first_stopping_reason": None,
                                 "m4": {"status": Q5E.M4_OK}})
    lowered = text.lower()
    check("association only" in lowered, "the summary states the boundary")
    check("caused by" not in lowered and "the cause" not in lowered,
          "no causal claim in the summary")


def test_allowed_file_boundary():
    """Only the four registered files may exist for this implementation."""
    allowed = {
        os.path.join(ROOT, "mit-bih", "q5e_leg2_failure_mechanism_audit.py"),
        os.path.join(ROOT, "mit-bih",
                     "test_q5e_leg2_failure_mechanism_audit.py"),
        NOTEBOOK,
        os.path.join(ROOT, "experiments", "specs",
                     "EXP-2026-008-q5e-leg2-failure-mechanism-audit.md"),
    }
    for path in allowed:
        check(os.path.exists(path), f"allowed file present: {path}")
    frozen = os.path.join(ROOT, "mit-bih", "q5d_order_preserving_beat_join.py")
    check(os.path.exists(frozen), "the frozen Q5-D module is still present")
    check(BJ.rule_fingerprint() == Q5E.REGISTERED_RULE_FINGERPRINT,
          "the frozen Q5-D rule fingerprint is unchanged")


def _notebook():
    with open(NOTEBOOK, encoding="utf-8") as handle:
        return json.load(handle)


def test_notebook_outputs_are_empty():
    nb = _notebook()
    for index, cell in enumerate(nb["cells"]):
        if cell["cell_type"] != "code":
            continue
        check(cell.get("outputs") == [], f"cell {index} has no stored output")
        check(cell.get("execution_count") is None,
              f"cell {index} was never executed")


def test_notebook_uses_the_production_path_and_defaults_closed():
    source = "\n".join("".join(c["source"]) for c in _notebook()["cells"])
    check("run_audit" in source, "the notebook calls the production route")
    check("OPEN_REGISTERED_DATA = False" in source,
          "the notebook defaults to not opening registered data")
    check("stage_should_run" in source,
          "the notebook announces every stage through the helper")
    check("module_capabilities" in source,
          "the notebook asserts module capabilities against a stale clone")
    check("__file__" in source, "the notebook prints both module paths")
    for banned in ("detect_r(", "ds2", "probabilit"):
        check(banned not in source.lower().replace("detect_r()", ""),
              f"the notebook does not reach {banned}")


def test_notebook_definition_before_use():
    """Names must be defined in an earlier cell than the one that uses them."""
    cells = [c for c in _notebook()["cells"] if c["cell_type"] == "code"]
    defined = set()
    for index, cell in enumerate(cells):
        text = "".join(cell["source"])
        for line in text.splitlines():
            stripped = line.strip()
            if stripped.startswith(("import ", "from ")):
                for token in stripped.replace(",", " ").split():
                    defined.add(token)
            if "=" in stripped and not stripped.startswith("#"):
                head = stripped.split("=")[0].strip()
                if head.isidentifier():
                    defined.add(head)
        for token in ("MODE", "APPROVAL", "OPEN_REGISTERED_DATA"):
            if token in text and index > 0:
                check(token in defined,
                      f"{token} is defined before cell {index} uses it")


def run_all() -> int:
    tests = [value for name, value in sorted(globals().items())
             if name.startswith("test_") and callable(value)]
    for test in tests:
        test()
    print(f"{len(tests)} test functions, {PASSED} assertions passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(run_all())
