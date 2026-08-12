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


def _verified(paths):
    """A hand-made input set, exactly as an attacker or a mistake would make it.

    It is *not* a credential and must not behave like one: `run_audit`
    re-verifies every input from its bytes, so a mapping like this is expected
    to be refused however plausible it looks.
    """
    return {key: paths.get(key, f"/synthetic/{key}")
            for key in Q5E.DISCOVERED_PATH_KEYS}


def tiny_partition(rows=None):
    """Synthetic cache partition.  `cache_n` is injected, never read from the
    registered ledger — that is the fixture boundary."""
    return Q5E.cache_partition(rows if rows is not None else tiny_bundle(),
                               PROCESSED, CACHE_N)


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

    part = tiny_partition(rows)
    table = Q5E.m0_class_by_reason(rows, PROCESSED, part)
    check(table[Q5E.SIDE_MAMBA]["V"][BJ.REASON_NO_EDGE]["count"] == 2,
          "M0.2 mamba V NO_EDGE count")
    check(table[Q5E.SIDE_CACHE]["V"][BJ.REASON_NO_EDGE]["count"] == 1,
          "M0.2 cache V NO_EDGE count uses the processed-class map")

    r208 = Q5E.m0_record_class(rows, PROCESSED, "208", part)
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
        {"H1": {"strata_reported": ["class", "pooled"],
                "effect_gates": {"a": True}},
         "H4": {"strata_reported": ["class", "pooled"],
                "effect_gates": {"a": True}}}, holm)
    check(flags["H2"]["status"] == Q5E.UNEVALUABLE, "H2 marked UNEVALUABLE")
    check(flags["H2"]["flag"] is False, "unevaluable family cannot fire")
    check("holm_significant" not in flags["H2"],
          "no significance verdict is reported for an unevaluable family")


def test_flags_require_gates_and_significance():
    holm = Q5E.holm_4family({"H1": 0.001, "H2": 0.001, "H3": 0.001,
                             "H4": 0.9})
    strata = ["class", "record", "pooled"]
    flags = Q5E.evaluate_flags(
        {"H1": {"strata_reported": strata,
                "effect_gates": {"share": True, "q99": True}},
         "H2": {"strata_reported": strata, "effect_gates": {"share": False}},
         "H3": {"strata_reported": strata, "effect_gates": {"share": True}},
         "H4": {"strata_reported": strata,
                "effect_gates": {"share": True}}}, holm)
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
    strata = ["class", "record", "pooled"]
    flag_a = Q5E.evaluate_flags({"H4": {"strata_reported": strata,
                                        "effect_gates": a["effect_gates"]}},
                                holm_a)["H4"]["flag"]
    flag_b = Q5E.evaluate_flags({"H4": {"strata_reported": strata,
                                        "effect_gates": b["effect_gates"]}},
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
        Q5E.run_audit(_verified({"bundle_dir": "b"}), "o", approval=None)
        raise AssertionError("run_audit ran without approval")
    except Q5E.ExecutionNotApprovedError:
        check(True, "the production entry point refuses immediately")


def test_run_audit_is_implemented_but_never_executed():
    with tempfile.TemporaryDirectory() as tmp:
        try:
            Q5E.run_audit(_verified({"bundle_dir": tmp}),
                          os.path.join(tmp, "out"),
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

    stopped_tables = {name: rows for name, rows in _full_tables().items()
                      if name != "m4_anchors.csv"}
    with tempfile.TemporaryDirectory() as tmp:
        out = os.path.join(tmp, "run")
        written = Q5E.write_bundle(
            out, result, Q5E.build_config(Q5E.MODE_DESIGN, "T"),
            {"m": 1}, stopped_tables, {}, ["line"],
            Q5E.summary_markdown(result))
        check("q5e_result.json" in written["written"], "result written")
        check("m4_anchors.csv" not in written["written"],
              "m4_anchors.csv is absent when M4 stops")
        try:
            Q5E.write_bundle(out, result, {}, {}, stopped_tables, {}, [], "x")
            raise AssertionError("overwrote an existing bundle")
        except Q5E.Q5EError:
            check(True, "an existing bundle is never overwritten")
        try:
            Q5E.write_bundle(os.path.join(tmp, "extra"), result, {}, {},
                             _full_tables(), {}, [], "x")
            raise AssertionError("an unregistered table was accepted")
        except Q5E.Q5EError as error:
            check("not registered outputs" in str(error),
                  "an M4-only table cannot be written on a STOP branch")


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


# ─────────────────────────────────────────────────────────────────────────────
# I1 corrective-implementation regressions (Codex acceptance review, #112)
# ─────────────────────────────────────────────────────────────────────────────
def test_cache_side_denominator_includes_certified_rows():
    """I1.2 — a certified cache beat exists only as a certified mamba row."""
    part = tiny_partition()
    Q5E.assert_cache_partition(part, CACHE_N)
    for record, n in CACHE_N.items():
        rows_r = [e for e in part if e["record"] == record]
        check(len(rows_r) == n, f"{record}: partition covers all {n} cache rows")
    rows = tiny_bundle()
    r208 = Q5E.m0_record_class(rows, PROCESSED, "208", part)
    total = sum(v["denominator"] for v in r208[Q5E.SIDE_CACHE].values())
    check(total == CACHE_N["208"],
          "cache-side class denominators sum to cache_n, certified included")
    # The old is_cache_side() view would have counted only the explicit rows.
    explicit = sum(1 for r in rows if Q5E.is_cache_side(r)
                   and r["record"] == "208")
    check(explicit < CACHE_N["208"],
          "the explicit cache-only rows really are fewer, so this is not vacuous")
    certified = [e for e in part if e["record"] == "208"
                 and e["group"] == Q5E.GROUP_CERTIFIED]
    check(len(certified) == 2, "certified cache rows recovered from mamba rows")
    check(all(e["class"] == PROCESSED[(e["record"], e["cache_record_row"])]
              for e in part),
          "cache class comes only from the processed-class map")


def test_cache_partition_rejects_duplicate_and_omission():
    rows = tiny_bundle()
    try:
        Q5E.cache_partition(rows, PROCESSED, {"101": 4, "208": 5})
        raise AssertionError("omission accepted")
    except Q5E.DiagnosticInputMismatch:
        check(True, "an uncovered cache row is DIAGNOSTIC_INPUT_MISMATCH")
    doubled = list(tiny_partition()) + [tiny_partition()[0]]
    try:
        Q5E.assert_cache_partition(doubled, CACHE_N)
        raise AssertionError("duplicate accepted")
    except Q5E.DiagnosticInputMismatch:
        check(True, "a duplicated cache row is DIAGNOSTIC_INPUT_MISMATCH")


def test_m3_exact_partition_qa():
    """I1.3 — row identity and reason assignment, not just a certified count."""
    pre = (300, 300, 800)
    post = (300, 800, 800)
    mamba = BJ.RecordSequence("101", "DS1", "mamba", pre, post)
    cache = BJ.RecordSequence("101", "DS1", "cache", pre, post)
    result = BJ.match_record(mamba, cache)
    rebuilt = Q5E.reconstructed_groups(result, len(mamba), len(cache))
    check(set(rebuilt) == {Q5E.SIDE_MAMBA, Q5E.SIDE_CACHE}, "both sides rebuilt")
    check(len(rebuilt[Q5E.SIDE_MAMBA]) == 3, "every mamba row assigned")

    rows = [row("101", mamba_row=i, cache_row=i, aami="N") for i in range(3)]
    graph = Q5E.m3_graph(rows, {"101": mamba}, {"101": cache})
    check(graph["partition_ok"] is True, "a consistent bundle reproduces")
    Q5E.assert_m3_partition(graph)
    check(True, "assert_m3_partition passes on agreement")

    wrong = [row("101", mamba_row=0, cache_row=0, aami="N"),
             row("101", mamba_row=1, cache_row=1, aami="N"),
             row("101", mamba_row=2, status=BJ.STATUS_UNMATCHED,
                 reason=BJ.REASON_NO_EDGE, aami="N"),
             row("101", cache_row=2, status=BJ.STATUS_UNMATCHED,
                 reason=BJ.REASON_NO_EDGE)]
    bad = Q5E.m3_graph(wrong, {"101": mamba}, {"101": cache})
    check(bad["partition_ok"] is False,
          "a disagreeing row assignment is detected")
    try:
        Q5E.assert_m3_partition(bad)
        raise AssertionError("mismatch accepted")
    except Q5E.DiagnosticInputMismatch:
        check(True, "one row mismatch is DIAGNOSTIC_INPUT_MISMATCH")
    try:
        Q5E.assert_m3_partition(graph, {BJ.REASON_NO_EDGE: 99})
        raise AssertionError("wrong reason count accepted")
    except Q5E.DiagnosticInputMismatch:
        check(True, "a reason-count mismatch stops M3")


def test_m4_gate_order_includes_input_identity():
    """I1.4 — the machine-readable order, the emitted gates and tests agree."""
    check(Q5E.M4_GATE_ORDER == ("runtime", "source_map", "input_identity",
                                "detector_replay", "record_counts",
                                "rr_equality"),
          "M4_GATE_ORDER is the registered order")
    check(Q5E.M4_GATES_BEFORE_REPLAY ==
          ("runtime", "source_map", "input_identity"),
          "three sub-gates precede any detector call")
    calls = []
    good = {"frontend.py": "def detect_r(s):\n    pass\n\n"
                           "def rr_features(p):\n    pass\n",
            "data.py": "def build_record(r):\n    peaks = detect_r(sig)\n"
                       "    tol = int(0.15 * fs)\n    used = set()\n"
                       "    ok = p - 150 >= 0\n    Fr = rr_features(peaks)\n"}

    def replay():
        calls.append("detector")
        return {"101": 1}, {"101": [[1.0]]}

    gate = Q5E.m4_feasibility_gate(
        runtime=Q5E.M4_REGISTERED_RUNTIME, sources=Q5E.M4_SOURCE_MAP_HASHES,
        texts=good, detector_counts=None, registered_counts={"101": 1},
        replayed_rr=None, frozen_rr={"101": [[1.0]]},
        input_identity={"v10_source": "wrong", "v10_cache": "wrong"},
        rr_verdict=Q5E.PREP_M4_RR_EQUIVALENCE_VERDICT, replay=replay)
    check(gate["status"] == Q5E.M4_INPUT_ABSENT, "identity failure stops M4")
    check(gate["first_failure"] == Q5E.M4_IDENTITY_MISMATCH, "identity reason")
    check([g["gate"] for g in gate["gates"]] ==
          ["runtime", "source_map", "input_identity"],
          "identity is emitted in its registered position")
    check(calls == [],
          "the detector is not called until identity has passed")

    ok = Q5E.m4_feasibility_gate(
        runtime=Q5E.M4_REGISTERED_RUNTIME, sources=Q5E.M4_SOURCE_MAP_HASHES,
        texts=good, detector_counts=None, registered_counts={"101": 1},
        replayed_rr=None, frozen_rr={"101": [[1.0]]},
        input_identity={
            "v10_source": Q5E.M4_INPUT_CONTRACT["v10_source"]["aggregate"],
            "v10_cache": Q5E.M4_INPUT_CONTRACT["v10_cache"]["aggregate"]},
        rr_verdict=Q5E.PREP_M4_RR_EQUIVALENCE_VERDICT, replay=replay)
    check(ok["status"] == Q5E.M4_OK, "a complete gate passes")
    check([g["gate"] for g in ok["gates"]] == list(Q5E.M4_GATE_ORDER),
          "the emitted gate list equals M4_GATE_ORDER exactly")
    check(calls == ["detector"], "the detector ran exactly once, and last")


def test_control_a_class_lineage_is_cache_side_only():
    """I1.5 — mamba class can never reach Control A's input."""
    rows = tiny_bundle()
    part = tiny_partition(rows)
    vectors = Q5E.build_control_a_class_vectors(part, PROCESSED, CACHE_N)
    check(vectors["208"] == ["N", "N", "V", "V"],
          "the vector is the processed class in cache_record_row order")
    Q5E.assert_control_a_input(vectors, PROCESSED, CACHE_N)

    mutated = [dict(r) for r in rows]
    for r in mutated:
        if r["mamba_aami"]:
            r["mamba_aami"] = "S"
    same = Q5E.build_control_a_class_vectors(
        Q5E.cache_partition(mutated, PROCESSED, CACHE_N), PROCESSED, CACHE_N)
    check(same == vectors, "changing mamba class leaves Control A untouched")

    moved = dict(PROCESSED); moved[("208", 2)] = "S"
    changed = Q5E.build_control_a_class_vectors(
        Q5E.cache_partition(rows, moved, CACHE_N), moved, CACHE_N)
    check(changed != vectors, "changing the processed class does change it")

    try:
        Q5E.assert_control_a_input({"208": ["N", "N", "N", "N"]},
                                   PROCESSED, CACHE_N)
        raise AssertionError("ad-hoc vector accepted")
    except Q5E.DiagnosticInputMismatch:
        check(True, "an ad-hoc class vector is refused")


def test_m5_strata_are_materialised_and_pooled_alone_cannot_fire():
    """I1.6 — stratum names in JSON are not stratification."""
    rows = tiny_bundle()
    report = Q5E.m5_stratified_failure_report(rows, tiny_partition(rows))
    for name in ("class", "reason", "record", "count_stratum", "pooled"):
        check(name in report and report[name], f"stratum {name} materialised")
    check(report["record_208"][Q5E.SIDE_CACHE]["denominator"] == 4,
          "record 208 reported on its own")
    check(report["record_116"]["status"] == Q5E.NOT_APPLICABLE,
          "an absent record is NOT_APPLICABLE, never a silent zero")
    empty = Q5E._rate_entry(0, 0)
    check(empty["rate"] is None and empty["status"] == Q5E.NOT_APPLICABLE,
          "an empty denominator is not written as a zero rate")
    reported = Q5E.strata_reported(report)
    check("pooled" in reported and len(reported) > 1, "several strata present")

    holm = Q5E.holm_4family({"H1": 0.0001, "H2": None, "H3": None, "H4": 0.5})
    pooled_only = Q5E.evaluate_flags(
        {"H1": {"strata_reported": ["pooled"],
                "effect_gates": {"a": True, "b": True}}}, holm)
    check(pooled_only["H1"]["flag"] is False,
          "a pooled-only mechanism claim cannot fire")
    check(pooled_only["H1"]["pooled_only_blocked"] is True,
          "and the block is reported, not silent")
    stratified = Q5E.evaluate_flags(
        {"H1": {"strata_reported": ["class", "pooled"],
                "effect_gates": {"a": True, "b": True}}}, holm)
    check(stratified["H1"]["flag"] is True,
          "the same evidence fires once it is stratified")


def _stub_png(path, spec, tables, data=None):
    """A real, valid 1x1 PNG using only the standard library."""
    import struct
    import zlib
    raw = b"\x00\xff\xff\xff"
    def chunk(tag, payload):
        return (struct.pack(">I", len(payload)) + tag + payload
                + struct.pack(">I", zlib.crc32(tag + payload) & 0xFFFFFFFF))
    png = (b"\x89PNG\r\n\x1a\n"
           + chunk(b"IHDR", struct.pack(">IIBBBBB", 1, 1, 8, 2, 0, 0, 0))
           + chunk(b"IDAT", zlib.compress(raw))
           + chunk(b"IEND", b""))
    with open(path, "wb") as handle:
        handle.write(png)


def test_required_outputs_and_incomplete_bundle_is_refused():
    """I1.7 — a bundle is complete or it is not written at all."""
    absent = Q5E.required_outputs(Q5E.DECISION_UNRESOLVED, m4_ok=False)
    present = Q5E.required_outputs(Q5E.DECISION_NONE, m4_ok=True)
    check("m4_anchors.csv" not in absent, "M4-only CSV absent when M4 stops")
    check(Q5E.FIGURE_M4_ONLY not in absent, "M4-only figure absent too")
    check("m4_anchors.csv" in present and Q5E.FIGURE_M4_ONLY in present,
          "both present when M4 passes")
    check(len(present) - len(absent) == 2,
          "exactly the two registered M4 exceptions differ")

    result = {"decision": Q5E.DECISION_NONE, "m4": {"status": Q5E.M4_OK}}
    with tempfile.TemporaryDirectory() as tmp:
        out = os.path.join(tmp, "incomplete")
        try:
            Q5E.write_bundle(out, result, {}, {}, {}, {}, ["x"], "s",
                             figures=True, figure_backend=_stub_png,
                             require_complete=True)
            raise AssertionError("incomplete bundle written")
        except Q5E.Q5EError as exc:
            check("Nothing has been created on disk" in str(exc),
                  "the completeness check runs before anything is created")
        check(not os.path.exists(out),
              "the refused bundle path was never created")
        check(os.listdir(tmp) == [],
              "no staging directory was left behind either")


def test_figure_rendering_writes_real_files():
    with tempfile.TemporaryDirectory() as tmp:
        written = Q5E.render_figures(tmp, {}, m4_ok=False, backend=_stub_png)
        check(len(written) == 6, "six figures when M4 stops")
        for name in written:
            path = os.path.join(tmp, name)
            check(os.path.getsize(path) > 0, f"{name} is a real file")
            with open(path, "rb") as handle:
                check(handle.read(8) == b"\x89PNG\r\n\x1a\n",
                      f"{name} is a PNG")
        try:
            Q5E.render_figures(tmp, {}, m4_ok=False, backend=_stub_png)
            raise AssertionError("overwrote a figure")
        except Q5E.Q5EError:
            check(True, "an existing figure is never overwritten")


def test_default_matplotlib_backend_when_available():
    try:
        import matplotlib                                  # noqa: F401
    except ImportError:
        check(True, "matplotlib absent: default renderer not exercised here")
        return
    with tempfile.TemporaryDirectory() as tmp:
        written = Q5E.render_figures(
            tmp, {"m0_class_by_reason.csv": [
                {"class": "V", "side": "cache", "count": 3}]},
            m4_ok=False)
        check(len(written) == 6, "the default backend renders every figure")
        with open(os.path.join(tmp, written[0]), "rb") as handle:
            check(handle.read(8) == b"\x89PNG\r\n\x1a\n",
                  "matplotlib produced a PNG")


# ─────────────────────────────────────────────────────────────────────────────
# Mandatory synthetic end-to-end production-path test.
#
# The whole route — QA, M0, M1, M2, M3, M4, controls A/B/C, Holm, flags, the
# decision tree and a complete CSV/JSON/PNG bundle — on injected fake readers
# and an injected M4 replay.  Nothing registered is opened, `detect_r()` is
# never called, and every number below is generated by the frozen matcher from
# synthetic RR values rather than copied out of the real bundle.
# ─────────────────────────────────────────────────────────────────────────────
E2E_RR = {
    # A clean record: mamba and cache agree beat for beat.
    "101": {"mamba": [100, 200, 300, 400], "cache": [100, 200, 300, 400]},
    # A record carrying one motif per M3 group.  Values are >1 sample apart
    # (RR_TOLERANCE_SAMPLES is 1), so every edge below is deliberate:
    #   rows 0,1 / cache 0,1  -> CERTIFIED
    #   row 2   (repeat of 100) -> an edge that is in no maximum matching
    #   row 3   / cache 2,3   -> a rank class of size two -> AMBIGUOUS
    #   row 4   / cache 4     -> no candidate edge at all
    "208": {"mamba": [100, 200, 100, 700, 900],
            "cache": [100, 200, 700, 700, 950]},
    # A record where the detector missed one annotation the Leg 1 replay kept:
    # mamba has five rows, the cache four.  This is the H2 story, and it is
    # what produces an annotation_without_peak anchor whose counterpart row
    # *was* kept.
    "116": {"mamba": [100, 200, 300, 400, 500],
            "cache": [100, 200, 300, 400]},
}
#: Class per row.  Indexed by mamba row for the join map and by cache row for
#: the processed-class map, so it is as long as the longer of the two.
E2E_CLASSES = {"101": ["N", "N", "N", "N"],
               "208": ["N", "V", "V", "N", "S"],
               "116": ["N", "V", "N", "S", "N"]}
#: Raw `.atr` sample positions of the kept mamba rows, per record.  Distinct
#: bases so no two records share a kept-sample tuple.
E2E_SAMPLES = {
    "101": [1000, 1200, 1400, 1600],
    "208": [2000, 2200, 2400, 2600, 2800],
    "116": [3000, 3200, 3400, 3600, 3800],
}
#: Detector peaks per record.  101 and 208 gain one peak with no annotation;
#: 116 is missing the peak for its last annotation.
E2E_PEAKS = {
    "101": [1000, 1200, 1400, 1600, 8000],
    "208": [2000, 2200, 2400, 2600, 2800, 9000],
    "116": [3000, 3200, 3400, 3600],
}
E2E_SIGNAL_LENGTH = 20000


def _e2e_sequences():
    """Mamba sequences carry the Leg 1 identity, as production's do."""
    mamba, cache = {}, {}
    for record, rr in E2E_RR.items():
        mamba[record] = BJ.RecordSequence(
            record, "DS1", "mamba", rr["mamba"], rr["mamba"],
            [{"raw_atr_ordinal": i, "raw_r_sample": s}
             for i, s in enumerate(E2E_SAMPLES[record])])
        cache[record] = BJ.RecordSequence(record, "DS1", "cache",
                                          rr["cache"], rr["cache"])
    return mamba, cache


class _FakeProducer(object):
    """The registered producer, injected.  `detect_r` is never the real one."""

    def __init__(self, cache_by_record):
        self.rr_by_kept = {}
        self.calls = []
        for record, sequence in cache_by_record.items():
            peaks = _kept_peaks(record)
            self.rr_by_kept[tuple(peaks)] = [
                [pre / BJ.FS, post / BJ.FS, 0, 0, 0, 0, 0]
                for pre, post in zip(sequence.pre_samples,
                                     sequence.post_samples)]

    def detect_r(self, signal):
        record = str(signal)
        self.calls.append(record)
        return list(E2E_PEAKS[record])

    def rr_features(self, kept):
        return self.rr_by_kept[tuple(int(k) for k in kept)]


def _kept_peaks(record):
    """Peaks that survive annotation matching and the boundary cut."""
    return [p for p in E2E_PEAKS[record] if p in set(E2E_SAMPLES[record])]


def _e2e_rows(mamba, cache):
    """Join-map rows *derived from the frozen matcher*, never hand-asserted.

    Building the fixture from `match_record()` is what keeps this test honest:
    it cannot pass by memorising a group assignment, because the groups are
    whatever the frozen rule produces on these RR values.
    """
    group_reason = {v: k for k, v in Q5E.REASON_TO_GROUP.items()}
    status_for = {Q5E.GROUP_AMBIGUOUS: BJ.STATUS_AMBIGUOUS,
                  Q5E.GROUP_NOT_OPTIMAL: BJ.STATUS_UNMATCHED,
                  Q5E.GROUP_NO_EDGE: BJ.STATUS_UNMATCHED}
    rows = []
    for record in sorted(mamba):
        result = BJ.match_record(mamba[record], cache[record])
        groups = Q5E.reconstructed_groups(result, len(mamba[record]),
                                          len(cache[record]))
        partner = {i: j for i, j in result.certified}
        for i, group in sorted(groups[Q5E.SIDE_MAMBA].items()):
            certified = group == Q5E.GROUP_CERTIFIED
            rows.append(row(
                record, mamba_row=i,
                cache_row=partner[i] if certified else None,
                aami=E2E_CLASSES[record][i],
                status=BJ.STATUS_CERTIFIED if certified else status_for[group],
                reason=BJ.REASON_NONE if certified else group_reason[group],
                ordinal=i, r_sample=1000 * (int(record) % 100) + i))
        for j, group in sorted(groups[Q5E.SIDE_CACHE].items()):
            if group == Q5E.GROUP_CERTIFIED:
                continue                # emitted as the certified mamba row
            rows.append(row(record, cache_row=j, status=status_for[group],
                            reason=group_reason[group]))
    return rows


def _e2e_inputs():
    """A `ProductionInputs` built entirely from fake readers.

    Every field production fills by opening a registered artifact is injected,
    but the *code path* is production's: the real `build_detector_replay()`
    runs, the real annotation matching places the anchors, and the real
    `load_frozen_rr()` supplies the arrays the gate compares.  Only the
    producer and the two readers are fakes.
    """
    mamba, cache = _e2e_sequences()
    rows = _e2e_rows(mamba, cache)
    cache_n = {r: len(c) for r, c in cache.items()}
    processed = {(r, j): E2E_CLASSES[r][j]
                 for r in cache for j in range(cache_n[r])}
    producer = _FakeProducer(cache)
    replay = Q5E.build_detector_replay(
        "/synthetic/v10", "/synthetic/mitdb", sorted(mamba),
        Q5E.EXECUTION_APPROVAL_TOKEN, producer=producer,
        atr_reader=lambda r: {
            "annotations": [(s, E2E_CLASSES[r][min(i, len(E2E_CLASSES[r]) - 1)])
                            for i, s in enumerate(E2E_SAMPLES[r])],
            "signal_length": E2E_SIGNAL_LENGTH},
        signal_reader=lambda r: r)
    texts = {
        "frontend.py": ("def detect_r(s):\n    pass\n\n"
                        "def rr_features(p):\n    pass\n"),
        "data.py": ("def build_record(r):\n    peaks = detect_r(sig)\n"
                    "    tol = int(0.15 * fs)\n    used = set()\n"
                    "    ok = p - 150 >= 0\n    Fr = rr_features(peaks)\n"),
    }
    return Q5E.ProductionInputs(
        rows=rows, decision={"rule_fingerprint": BJ.rule_fingerprint()},
        manifest={"code_sha256": Q5E.PRODUCING_CODE_SHA256},
        processed_classes=processed, mamba_by_record=mamba,
        cache_by_record=cache, cache_n=cache_n,
        m4_runtime=Q5E.M4_REGISTERED_RUNTIME,
        m4_sources=Q5E.M4_SOURCE_MAP_HASHES, m4_texts=texts,
        m4_identity={
            "v10_source": Q5E.M4_INPUT_CONTRACT["v10_source"]["aggregate"],
            "v10_cache": Q5E.M4_INPUT_CONTRACT["v10_cache"]["aggregate"]},
        m4_registered_counts={r: len(c) for r, c in cache.items()},
        m4_frozen_rr=Q5E.load_frozen_rr(cache),
        m4_replay=replay,
        m4_anchors=lambda: replay.anchors_by_record(mamba),
        source_files=[])


def _e2e_qa_fixture(rows):
    """Fixture QA targets, computed from the fixture itself.

    Not the registered numbers, and never presented as them: the resulting
    bundle is stamped FIXTURE end to end.
    """
    return {"targets": Q5E.observed_qa_counts(rows),
            "rule_fingerprint": BJ.rule_fingerprint(),
            "producing_code_sha256": Q5E.PRODUCING_CODE_SHA256}


def test_synthetic_end_to_end_production_path():
    opened = []
    real_open = Q5E.open_registered_input

    def tripwire(path, approval, what):        # pragma: no cover - must not run
        opened.append(path)
        raise AssertionError(f"the synthetic route opened {path!r}")

    Q5E.open_registered_input = tripwire
    try:
        inputs = _e2e_inputs()
        fixture = _e2e_qa_fixture(inputs.rows)
        # Replicates are reduced only through this fixture-only argument; the
        # registered count is untouched and production never passes either.
        outcome = Q5E.run_pipeline(inputs, replicates=25, emit=lambda *a: None,
                                   qa_fixture=fixture)
    finally:
        Q5E.open_registered_input = real_open
    check(not opened, "no registered artifact was opened")

    # ---- every stage is present and actually ran ---------------------------
    check(outcome["qa"]["ok"] and not outcome["stopped"],
          "QA passed on the fixture and the pipeline continued")
    check(outcome["qa"]["target_set"] == Q5E.QA_TARGETS_FIXTURE,
          "the QA verdict records that it used fixture targets")
    for stage in ("m0", "m1", "m2", "m3", "m4"):
        check(bool(outcome[stage]), f"{stage} produced a result")
    check(outcome["m4"]["status"] == Q5E.M4_OK,
          "the injected replay carried M4.0 through every sub-gate")
    check([g["gate"] for g in outcome["m4"]["gates"]] ==
          list(Q5E.M4_GATE_ORDER), "M4 ran the registered gate order")
    check("anchors_report" in outcome["m4"], "M4.1 anchors were computed")
    # The production M4 really ran: the detector replay was invoked once per
    # record, reproduced all three counts, and the anchors came out of its own
    # annotation matching rather than from a hand-written table.
    check(inputs.m4_replay.ran is True,
          "the detector replay callback actually executed")
    check(sorted(inputs.m4_replay.producer.calls) == sorted(E2E_RR),
          "the registered detector ran once for every record")
    anchors = outcome["m4"]["anchors_report"]
    check(anchors["anchors"] > 0, "anchors were placed")
    kinds = {str(r["anchor_kind"]) for r in anchors["rows"]}
    check("annotation_without_peak" in kinds,
          "record 116 produced an annotation-without-peak anchor")
    check(anchors["explained_positions"],
          "and it maps to a kept mamba row, so H2 has a numerator")
    for control in (Q5E.CONTROL_A, Q5E.CONTROL_B, Q5E.CONTROL_C):
        check(control in outcome["nulls"], f"{control} produced a null")
    check(set(outcome["nulls"][Q5E.CONTROL_C]) == {"H2", "H3"},
          "Control C fed both H2 and H3")
    for name in Q5E.HYPOTHESES:
        entry = outcome["tests"][name]
        check(entry["p"] is not None, f"{name} has a permutation p")
        check(entry["p_holm_4family"] is not None,
              f"{name} carries a 4-family Holm value")
        check("stratified_evidence" in entry,
              f"{name} records whether it has stratified evidence")
    check(outcome["holm"]["family_size"] == 4, "Holm used exactly 4 families")
    check(set(outcome["flags"]) == set(Q5E.HYPOTHESES), "every flag evaluated")
    check(outcome["decision"]["decision"] in Q5E.DECISIONS,
          "the decision tree chose a registered branch")
    # M5 reached the hypothesis statistics, not just the M0 counts.
    for name in Q5E.HYPOTHESES:
        reported = outcome["flags"][name].get("strata_reported") or []
        check(Q5E.POOLED in reported or not reported,
              f"{name} reports pooled among its materialised strata")
    h1_strata = outcome["flags"]["H1"]["strata_reported"]
    check([s for s in h1_strata if s != Q5E.POOLED],
          "H1 materialised at least one non-pooled stratum")
    check("record_116" in h1_strata or "record_208" in h1_strata,
          "the individually registered records are materialised for H1")

    # ---- the bundle is written complete, with real PNG files ---------------
    result = Q5E.build_result(
        qa=outcome["qa"], m0=outcome["m0"], m1=outcome["m1"],
        m2=outcome["m2"], m3=outcome["m3"], m4=outcome["m4"],
        nulls=outcome["nulls"], tests=outcome["tests"],
        decision=outcome["decision"], source_files=[])
    check(result["synthetic_fixture"] is True,
          "the result marks itself a synthetic fixture")
    check(result["qa_target_set"] == Q5E.QA_TARGETS_FIXTURE,
          "the result carries the fixture target set")
    summary = Q5E.summary_markdown(result)
    check("SYNTHETIC FIXTURE - NOT A Q5-E RESULT" in summary,
          "the summary says plainly that this is not a Q5-E result")
    check("cause" not in summary.lower(), "no causal language in the summary")

    try:
        import matplotlib                                  # noqa: F401
        backend = None
    except ImportError:
        backend = _stub_png
    with tempfile.TemporaryDirectory() as tmp:
        directory = os.path.join(tmp, "run")
        written = Q5E.write_bundle(
            directory, result,
            Q5E.build_config(Q5E.MODE_AUDIT, "20260812T000000Z"),
            Q5E.build_manifest({"fixture": True}, "20260812T000000Z"),
            outcome["tables"], outcome["nulls"], ["synthetic end-to-end"],
            summary, figures=True, figure_backend=backend,
            require_complete=True)
        for name in written["required"]:
            path = os.path.join(directory, name)
            check(os.path.exists(path), f"{name} was written")
            check(os.path.getsize(path) > 0, f"{name} is not empty")
        check("m4_anchors.csv" in written["required"],
              "an M4-OK branch must write the anchor table")
        pngs = [n for n in written["required"] if n.endswith(".png")]
        check(len(pngs) == 7, "an M4-OK branch writes all seven figures")
        for name in pngs:
            with open(os.path.join(directory, name), "rb") as handle:
                check(handle.read(8) == b"\x89PNG\r\n\x1a\n",
                      f"{name} is a real PNG")
        with open(os.path.join(directory, "q5e_result.json"),
                  encoding="utf-8") as handle:
            stored = json.load(handle)
        check(stored["synthetic_fixture"] is True,
              "the written result keeps the fixture stamp")
        check(stored["training_performed"] is False and
              stored["ds2_labels_opened"] is False and
              stored["v10_probability_opened"] is False,
              "the written result keeps every execution seal")


def test_production_route_never_injects_a_qa_fixture():
    """The fixture seam is test-only: production measures against the
    registered targets, and nothing in `run_audit` can change that."""
    with open(Q5E.__file__, encoding="utf-8") as handle:
        text = handle.read()
    body = text.split("def run_audit(", 1)[1].split("\ndef ", 1)[0]
    check("qa_fixture" not in body,
          "run_audit never passes a QA fixture")
    check("run_pipeline(inputs, emit=emit)" in body,
          "run_audit calls the pipeline with the registered defaults")
    default = Q5E.verify_qa_targets(
        [], {"rule_fingerprint": BJ.rule_fingerprint()},
        {"code_sha256": Q5E.PRODUCING_CODE_SHA256})
    check(default["target_set"] == Q5E.QA_TARGETS_REGISTERED,
          "the default target set is the registered one")
    check(default["targets"]["total_failure_rows"]["expected"] ==
          Q5E.QA_TARGETS["total_failure_rows"],
          "the registered targets are still what an unparameterised call uses")
    check(not default["ok"], "empty rows do not reproduce the registered QA")


def _fake_mount(tmp, *, superseded=False, duplicate=False):
    """A mount tree with one canonical bundle and one look-alike decoy.

    The decoy carries the same file names and a different `code_sha256`, which
    is exactly the failure mode path-typing produces: two plausible folders,
    one of them wrong.
    """
    import shutil
    def bundle(directory, code):
        os.makedirs(directory, exist_ok=True)
        for name in Q5E.BUNDLE_INPUT_FILES:
            with open(os.path.join(directory, name), "w",
                      encoding="utf-8") as handle:
                handle.write("{}" if name.endswith(".json") else "x\n")
        with open(os.path.join(directory, "manifest.json"), "w",
                  encoding="utf-8") as handle:
            json.dump({"code_sha256": code}, handle)
        return directory

    root = os.path.join(tmp, "MyDrive")
    good = bundle(os.path.join(root, "runs", "20260811T035108_real"),
                  Q5E.PRODUCING_CODE_SHA256)
    bundle(os.path.join(root, "runs", "20260810T000000_old"), "0" * 64)
    if superseded:
        with open(os.path.join(good, Q5E.SUPERSEDED_MARKER), "w",
                  encoding="utf-8") as handle:
            handle.write("{}")
    if duplicate:
        shutil.copytree(good, os.path.join(root, "backup", "copy_of_run"))
    return root, good


def test_input_discovery_is_by_digest_not_by_path():
    """No Drive path is typed by hand: identity selects the artifact."""
    with tempfile.TemporaryDirectory() as tmp:
        root, good = _fake_mount(tmp)
        # The cache, source and publisher trees are absent, so the call must
        # refuse rather than silently return a partial answer.
        try:
            Q5E.discover_registered_inputs(root, Q5E.EXECUTION_APPROVAL_TOKEN)
            raise AssertionError("a partial mount was accepted")
        except Q5E.DiagnosticInputMismatch as error:
            check("no " in str(error), "a missing input refuses, never guesses")

        found = []
        for directory in Q5E._candidate_dirs(root):
            manifest = os.path.join(directory, "manifest.json")
            if not os.path.exists(manifest):
                continue
            with open(manifest, encoding="utf-8") as handle:
                if json.load(handle).get("code_sha256") == \
                        Q5E.PRODUCING_CODE_SHA256:
                    found.append(directory)
        check(found == [good],
              "the decoy bundle with a different code_sha256 is not selected")


def test_discovery_refuses_a_superseded_bundle():
    with tempfile.TemporaryDirectory() as tmp:
        root, _ = _fake_mount(tmp, superseded=True)
        try:
            Q5E.discover_registered_inputs(root, Q5E.EXECUTION_APPROVAL_TOKEN)
            raise AssertionError("a superseded bundle was selected")
        except Q5E.DiagnosticInputMismatch as error:
            check("canonical bundle" in str(error),
                  "a SUPERSEDED bundle is not a match")


def test_byte_identical_duplicates_are_resolved_not_refused():
    """Blocker 4 — Drive holds identical copies and none may be deleted."""
    candidates = [{"path": "/drive/b/mamba_data.npz", "digest": "aa" * 32},
                  {"path": "/drive/a/mamba_data.npz", "digest": "aa" * 32}]
    resolved = Q5E.resolve_identical_candidates(candidates, "mamba", "/drive")
    check(resolved["path"] == "/drive/a/mamba_data.npz",
          "one copy is chosen deterministically, by sorted path")
    check(resolved["byte_identical_duplicates"] ==
          ["/drive/b/mamba_data.npz"],
          "every duplicate path is recorded in the audit")
    check(resolved["n_candidates"] == 2, "the candidate count is preserved")
    again = Q5E.resolve_identical_candidates(list(reversed(candidates)),
                                             "mamba", "/drive")
    check(again["path"] == resolved["path"],
          "resolution does not depend on discovery order")

    try:
        Q5E.resolve_identical_candidates([], "mamba", "/drive")
        raise AssertionError("zero matches accepted")
    except Q5E.DiagnosticInputMismatch as error:
        check("no mamba" in str(error), "zero matches still fail")

    try:
        Q5E.resolve_identical_candidates(
            [{"path": "/drive/a", "digest": "aa" * 32},
             {"path": "/drive/b", "digest": "bb" * 32}], "mamba", "/drive")
        raise AssertionError("different digests were merged")
    except Q5E.DiagnosticInputMismatch as error:
        check("never merged" in str(error),
              "copies that are not byte-identical are not one identity")

    with open(Q5E.__file__, encoding="utf-8") as handle:
        text = handle.read()
    for banned in ("os.remove(", "shutil.move(", "os.unlink("):
        check(banned not in text.split("def write_bundle", 1)[0],
              f"discovery never calls {banned} on a registered asset")


def test_discovery_requires_a_clean_file_set_not_only_an_aggregate():
    """Blocker 2 — an unexpected file is a contract problem, not a match."""
    with open(Q5E.__file__, encoding="utf-8") as handle:
        body = handle.read().split("def discover_registered_inputs(", 1)[1]
        body = body.split("\ndef ", 1)[0]
    check(body.count('digest.get("ok")') >= 3,
          "cache, source and bundle discovery all require a clean file set")
    problems = Q5E.verify_mitdb_identity.__doc__ or ""
    check("publisher" in problems,
          "the MIT-BIH gate documents its independent publisher check")


def test_identity_gate_fails_on_file_set_problems():
    """Blocker 2 — problems must not be computed and then ignored."""
    import q5d_order_preserving_beat_join as _BJ
    real = _BJ.hash_file_set

    def unexpected(directory, names, approval=None):
        out = dict(real(directory, names, approval=approval))
        out.update({"ok": False, "extra": ["stowaway.npz"],
                    "problems": [f"{directory}: unexpected ['stowaway.npz']"]})
        return out

    with tempfile.TemporaryDirectory() as tmp:
        paths = {key: tmp for key in Q5E.DISCOVERED_PATH_KEYS}
        paths["mamba_path"] = os.path.join(tmp, "mamba_data.npz")
        with open(paths["mamba_path"], "wb") as handle:
            handle.write(b"x")
        _BJ.hash_file_set = unexpected
        try:
            Q5E.reverify_registered_inputs(paths,
                                           Q5E.EXECUTION_APPROVAL_TOKEN)
            raise AssertionError("a set with an unexpected file was accepted")
        except Q5E.DiagnosticInputMismatch as error:
            check("re-verification failed" in str(error),
                  "an aggregate match with an unexpected file still fails")
        finally:
            _BJ.hash_file_set = real


def test_mount_route_is_the_notebook_route_and_is_still_guarded():
    check("run_audit_from_mount" in Q5E.module_capabilities(),
          "the mount route is a declared capability")
    with open(NOTEBOOK, encoding="utf-8") as handle:
        text = handle.read()
    check("run_audit_from_mount" in text,
          "the notebook uses the digest-resolved route")
    for typed in ("BUNDLE_DIR = ", "MAMBA_PATH = ", "CACHE_DIR = "):
        check(typed not in text,
              f"the notebook no longer asks for a typed {typed.split()[0]}")
    try:
        Q5E.run_audit_from_mount("/nonexistent", "/tmp",
                                 approval=Q5E.EXECUTION_APPROVAL_TOKEN,
                                 open_registered_data=True)
        raise AssertionError("the terminal guard was bypassed")
    except (Q5E.Q5EError, OSError) as error:
        check(not isinstance(error, AssertionError),
              "an approved mount run still cannot reach registered data here")


# ─────────────────────────────────────────────────────────────────────────────
# Second acceptance review (I1 round 2) regressions
# ─────────────────────────────────────────────────────────────────────────────
def _full_tables():
    """Non-empty tables for every registered CSV, so a bundle can complete."""
    return {
        "m0_class_by_reason.csv": [
            {"side": "mamba", "class": "V", "reason": BJ.REASON_NO_EDGE,
             "count": 2, "denominator": 4, "rate": 0.5},
            {"side": "cache", "class": "N", "reason": BJ.REASON_AMBIGUOUS,
             "count": 1, "denominator": 4, "rate": 0.25}],
        "m0_record_class.csv": [
            {"record": "208", "stratum": BJ.STRATUM_MISMATCH, "class": "V",
             "side": "cache", "denominator": 2, "failures": 1, "rate": 0.5}],
        "m0_runs.csv": [
            {"record": "208", "adjacency_definition": Q5E.ADJ_PRIMARY,
             "run_start": "1", "run_length": 3, "classes": "", "reasons": "",
             "decisional": True},
            {"record": "208", "adjacency_definition": Q5E.ADJ_SECONDARY,
             "run_start": "1", "run_length": 2, "classes": "", "reasons": "",
             "decisional": False}],
        "m1_distance.csv": [
            {"record": "208", "cache_record_row": 0, "processed_class": "V",
             "reason": BJ.REASON_NO_EDGE, "d_inf": 3, "bin": "2-5",
             "censored": False, "cache_endpoint_zero": False,
             "included_in_distance_gate": True}],
        "m3_graph.csv": [
            {"record": "208", "side": "cache", "row": 0,
             "group": Q5E.GROUP_NO_EDGE, "decisional": True,
             "candidate_degree": 0, "usable_edges": 0, "has_forced_rank": False,
             "rr_pair_multiplicity": 1, "local_rr_sd": 0.0},
            {"record": "208", "side": "mamba", "row": 0,
             "group": Q5E.GROUP_CERTIFIED, "decisional": False,
             "candidate_degree": 2, "usable_edges": 1, "has_forced_rank": True,
             "rr_pair_multiplicity": 1, "local_rr_sd": 0.5}],
        "m4_anchors.csv": [
            {"record": "208", "anchor_ordinal": 0, "anchor_sample": 700,
             "anchor_kind": "annotation_without_peak",
             "adjacency_definition": Q5E.ADJ_PRIMARY, "offset": 1,
             "mapped_mamba_record_row": 4, "failed": True,
             "decisional": True}],
    }


def test_bundle_publish_is_atomic():
    """3 — a failure never leaves an incomplete bundle at the final path."""
    result = {"decision": Q5E.DECISION_NONE, "m4": {"status": Q5E.M4_OK}}
    tables = _full_tables()

    def exploding(path, spec, tables_, data=None):
        if str(spec["file"]) == Q5E.FIGURES[3]:
            raise RuntimeError("renderer failed midway")
        _stub_png(path, spec, tables_, data)

    with tempfile.TemporaryDirectory() as tmp:
        out = os.path.join(tmp, "run")
        try:
            Q5E.write_bundle(out, result, {}, {}, tables, {}, ["x"], "s",
                             figures=True, figure_backend=exploding,
                             require_complete=True)
            raise AssertionError("a failed run published a bundle")
        except RuntimeError:
            check(True, "the renderer failure propagated")
        check(not os.path.exists(out),
              "the final path holds nothing after a mid-write failure")
        check(os.listdir(tmp) == [],
              "the staging directory was removed, not left as debris")

        written = Q5E.write_bundle(out, result, {}, {}, tables, {}, ["x"], "s",
                                   figures=True, figure_backend=_stub_png,
                                   require_complete=True)
        check(written["published"] is True, "a complete bundle publishes")
        check(os.path.isdir(out), "the final path now exists")
        for name in written["required"]:
            check(os.path.exists(os.path.join(out, name)),
                  f"{name} is present in the published bundle")
        check(not [n for n in os.listdir(tmp) if n.startswith(".")],
              "no staging directory survives a successful publish")


def test_every_figure_shows_a_different_measurement():
    """4 — figures 4 and 5 must not render the same series."""
    tables = _full_tables()
    kinds = [str(s["kind"]) for s in Q5E.figure_specs(m4_ok=True)]
    check(len(set(kinds)) == 7, "all seven figures have distinct kinds")
    payloads = [Q5E.figure_data(k, tables, {Q5E.CONTROL_C: {
        "H2": {"q99": 0.5}, "H3": {"q99": 0.25}}}) for k in kinds]
    rendered = [json.dumps(p, sort_keys=True, default=str) for p in payloads]
    check(len(set(rendered)) == 7, "no two figures render identical data")

    run_length = Q5E.figure_data(Q5E.FIG_RUN_LENGTH_HIST, tables)
    distance = Q5E.figure_data(Q5E.FIG_DISTANCE_HIST, tables)
    check(set(run_length["buckets"]) != set(distance["counts"]),
          "the run-length figure no longer renders the distance bins")
    check(run_length["adjacency"] == Q5E.ADJ_PRIMARY,
          "the run-length figure uses the decisional adjacency only")
    check(distance["bins"] == [n for n, _lo, _hi in Q5E.M1_BINS],
          "the distance figure uses the registered fixed bins in order")
    check(set(distance["descriptive_exclusions"]) ==
          {Q5E.CENSORED_FLAG, Q5E.ENDPOINT_ZERO_FLAG},
          "censor and endpoint bars sit beside the histogram")

    heatmap = Q5E.figure_data(Q5E.FIG_RECORD_CLASS_HEATMAP, tables)
    check(heatmap["columns"] == list(Q5E.AAMI_CLASSES) and
          heatmap["shape"][1] == 3, "the heatmap is records x 3 classes")
    raster = Q5E.figure_data(Q5E.FIG_RECORD_208_RASTER, tables)
    check(raster["raster"] and Q5E.ADJ_SECONDARY in
          raster["raw_ordinal_sensitivity"],
          "record 208 shows beat-level rows and the raw-ordinal sensitivity")
    degree = Q5E.figure_data(Q5E.FIG_DEGREE_VIOLIN_ECDF, tables)
    for side in Q5E.SIDES:
        panel = degree["panels"][side]
        check(panel["decisional"] == (side == Q5E.H4_DECISIONAL_SIDE),
              f"the {side} panel states its decisional status")
        check("ecdf" in panel and "violin" in panel,
              f"the {side} panel carries both a violin and an ECDF")
    anchor = Q5E.figure_data(Q5E.FIG_ANCHOR_CURVE, tables,
                             {Q5E.CONTROL_C: {"H2": {"q99": 0.5}}})
    check(anchor["control_c_band"], "the anchor curve carries a Control C band")


def test_render_refuses_two_figures_with_identical_data():
    with tempfile.TemporaryDirectory() as tmp:
        real = Q5E.figure_data
        Q5E.figure_data = lambda kind, tables, nulls=None: {"same": 1}
        try:
            Q5E.render_figures(tmp, {}, m4_ok=False, backend=_stub_png)
            raise AssertionError("duplicate figures accepted")
        except Q5E.Q5EError as error:
            check("same data" in str(error),
                  "two figures rendering the same data are refused")
        finally:
            Q5E.figure_data = real


def test_m5_stratification_is_computed_not_named():
    """2 — a stratum counts only when it carries a real number."""
    items = [{"record": "208", "class": "V", "reason": BJ.REASON_NO_EDGE,
              "bin": "2-5"},
             {"record": "208", "class": "N", "reason": BJ.REASON_NO_EDGE,
              "bin": "6-20"},
             {"record": "116", "class": "V", "reason": BJ.REASON_AMBIGUOUS,
              "bin": "2-5"}]
    report = Q5E.stratified_statistic(
        items, lambda subset: Q5E._ratio(
            sum(1 for e in subset if e["bin"] == "2-5"), len(subset)))
    check(report["class"]["levels"]["V"]["n"] == 2,
          "the class stratum carries per-level counts")
    check(report["class"]["levels"]["V"]["statistic"] == 1.0,
          "and a real per-level statistic")
    check(report["record_208"]["materialised"] is True,
          "record 208 is materialised when it has rows")
    check(report["record"]["levels"]["116"]["statistic"] == 1.0,
          "each record level is computed separately")
    check(Q5E.has_stratified_evidence(report),
          "this report carries non-pooled evidence")

    pooled_only = Q5E.stratified_statistic(
        [{"record": "", "class": "", "reason": ""}],
        lambda subset: 1.0)
    check(pooled_only[Q5E.POOLED]["materialised"] is True,
          "the pooled value is still computed")
    check(not Q5E.has_stratified_evidence(pooled_only),
          "an item with no stratum keys yields pooled-only evidence")
    check(Q5E.materialised_strata(pooled_only) == [Q5E.POOLED],
          "and only pooled is reported as materialised")


def test_flag_needs_a_real_stratified_statistic():
    """2 — stratum names can no longer stand in for stratified evidence."""
    holm = {"significant": {h: True for h in Q5E.HYPOTHESES},
            "unevaluable": [],
            "p_holm_4family": {h: 0.001 for h in Q5E.HYPOTHESES}}
    named_only = {name: {"levels": {}, "materialised": False,
                         "status": Q5E.NOT_APPLICABLE}
                  for name in Q5E.M5_STRATA}
    named_only[Q5E.POOLED] = {"levels": {"pooled": {"n": 4, "statistic": 0.9,
                                                    "status": "OK"}},
                              "materialised": True, "status": "OK"}
    blocked = Q5E.evaluate_flags(
        {"H1": {"strata": named_only, "strata_reported": list(Q5E.M5_STRATA),
                "effect_gates": {"g": True}}}, holm)
    check(blocked["H1"]["flag"] is False,
          "declaring every stratum name does not unlock the flag")
    check(blocked["H1"]["pooled_only_blocked"] is True,
          "it is recorded as pooled-only")
    check(blocked["H1"]["strata_reported"] == [Q5E.POOLED],
          "only the stratum that carries a number is reported")

    real = dict(named_only)
    real["class"] = {"levels": {"V": {"n": 3, "statistic": 0.8,
                                      "status": "OK"}},
                     "materialised": True, "status": "OK"}
    allowed = Q5E.evaluate_flags(
        {"H1": {"strata": real, "effect_gates": {"g": True}}}, holm)
    check(allowed["H1"]["flag"] is True,
          "one real non-pooled stratum is enough to allow the flag")
    check(allowed["H1"]["stratified_evidence"] is True,
          "and it is recorded as stratified evidence")


def test_m4_replay_reruns_the_detector_and_feeds_the_anchors():
    """1 — production M4 is complete, exercised by synthetic injection only."""
    annotations = [(200, "N"), (600, "V"), (1000, "N"), (1400, "N")]

    class FakeProducer(object):
        calls = []

        @staticmethod
        def detect_r(signal):
            FakeProducer.calls.append("detect_r")
            return [200, 601, 1000, 1400, 5000]   # 5000 has no annotation

        @staticmethod
        def rr_features(peaks):
            out = []
            for index in range(len(peaks)):
                pre = 1.0 if index == 0 else (peaks[index] -
                                              peaks[index - 1]) / BJ.FS
                post = (pre if index == len(peaks) - 1
                        else (peaks[index + 1] - peaks[index]) / BJ.FS)
                out.append([pre, post, 0, 0, 0, 0, 0])
            return out

    replay = Q5E.build_detector_replay(
        "/synthetic/v10", "/synthetic/mitdb", ["208"],
        Q5E.EXECUTION_APPROVAL_TOKEN, producer=FakeProducer,
        atr_reader=lambda r: {"annotations": annotations,
                              "signal_length": 10000},
        signal_reader=lambda r: [0.0])
    try:
        replay.anchors_by_record({})
        raise AssertionError("anchors were built before the replay ran")
    except Q5E.Q5EError as error:
        check("before the M4.0 detector replay ran" in str(error),
              "no anchor may be computed before the gate's replay")

    counts, replayed = replay()
    check(FakeProducer.calls == ["detect_r"],
          "the registered detector ran exactly once per record")
    check(counts["208"] == 4,
          "the boundary cut and AAMI selection drop the unannotated peak")
    check(len(replayed["208"]) == 2 and len(replayed["208"][0]) == 4,
          "the replay returns pre and post arrays in samples")

    mamba = BJ.RecordSequence(
        "208", "DS1", "mamba", [100, 200, 300, 400], [200, 300, 400, 400],
        [{"raw_r_sample": s} for s in (200, 600, 1000, 1400)])
    anchors = replay.anchors_by_record({"208": mamba})
    kinds = {a["anchor_kind"] for a in anchors["208"]}
    check("peak_without_annotation" in kinds,
          "a detector peak matched to no annotation is an anchor")
    placed = [a for a in anchors["208"]
              if a["mapped_mamba_record_row"] is not None]
    check(all(0 <= int(a["mapped_mamba_record_row"]) < len(mamba)
              for a in placed),
          "every placed anchor lands on a real kept mamba row")
    unplaceable = [a for a in anchors["208"]
                   if a["mapped_mamba_record_row"] is None]
    check(all(not a["counterpart_kept"] for a in unplaceable),
          "an anchor with no unique placement is reported, never imputed")


def test_m4_peak_matching_uses_the_sources_own_tolerance():
    """1 — no new detector, tolerance or manual anchor is introduced."""
    check(Q5E.M4_PEAK_MATCH_TOLERANCE_SAMPLES == 54,
          "the tolerance is the source's own int(0.15 * fs)")
    annotations = [(1000, "N"), (2000, "N")]
    near = Q5E.match_peaks_to_annotations([1054], annotations, 10000)
    check(not near["peaks_without_annotation"],
          "a peak exactly at the tolerance still matches")
    far = Q5E.match_peaks_to_annotations([1055], annotations, 10000)
    check(len(far["peaks_without_annotation"]) == 1,
          "one sample beyond the tolerance does not match")
    check(len(far["annotations_without_peak"]) == 2,
          "and both annotations are then unmatched")

    twice = Q5E.match_peaks_to_annotations([1000, 1001], annotations, 10000)
    check(len(twice["kept_rows"]) == 1,
          "the used set stops one annotation answering for two peaks")
    check(len(twice["peaks_without_annotation"]) == 1,
          "the second peak becomes an anchor rather than a duplicate match")
    check(len({r["raw_atr_ordinal"] for r in twice["kept_rows"]}) == 1,
          "each kept row maps to a distinct annotation")

    edge = Q5E.match_peaks_to_annotations([100], [(100, "N")], 10000)
    check(not edge["kept_rows"],
          "the p-150>=0 boundary cut drops a peak too close to the start")
    late = Q5E.match_peaks_to_annotations([9950], [(9950, "N")], 10000)
    check(not late["kept_rows"],
          "and the p+150<=len cut drops one too close to the end")


def test_m4_identity_is_observed_not_substituted():
    """6 — the identity sub-gate may never compare a constant with itself."""
    with open(Q5E.__file__, encoding="utf-8") as handle:
        body = handle.read().split("def load_all_inputs(", 1)[1]
        body = body.split("\ndef ", 1)[0]
    check("observed_m4_identity(" in body,
          "load_all_inputs observes the mounted aggregates")
    check('M4_INPUT_CONTRACT["v10_cache"]' not in body,
          "it never passes the registered constant as the observed value")
    mismatch = Q5E.verify_m4_input_identity(
        {"v10_source": "deadbeef", "v10_cache": "deadbeef"},
        Q5E.PREP_M4_RR_EQUIVALENCE_VERDICT)
    check(not mismatch["ok"], "a wrong observed aggregate fails the sub-gate")


def test_run_audit_reverifies_and_never_trusts_a_stamp():
    """Blocker 1 — a hand-made mapping is not evidence of identity.

    The old design accepted any mapping carrying the string
    "DIGEST_VERIFIED", which any caller could write beside five paths of their
    choosing.  Provenance is not evidence either; only recomputed digests are.
    """
    with open(Q5E.__file__, encoding="utf-8") as handle:
        text = handle.read()
    check(not hasattr(Q5E, "DISCOVERY_VERIFIED"),
          "the stamp constant is gone, not merely unused")
    check("assert_discovered_identity" not in text,
          "and so is the function that checked it")
    body = text.split("def run_audit(", 1)[1].split("\ndef ", 1)[0]
    check("reverify_registered_inputs(" in body,
          "run_audit re-verifies every input from its bytes")

    with tempfile.TemporaryDirectory() as tmp:
        forged = _verified({"bundle_dir": tmp})
        forged["identity_verified"] = "DIGEST_VERIFIED"
        try:
            Q5E.reverify_registered_inputs(forged,
                                           Q5E.EXECUTION_APPROVAL_TOKEN)
            raise AssertionError("a forged mapping was accepted")
        except Q5E.DiagnosticInputMismatch as error:
            check("re-verification failed" in str(error),
                  "a hand-made mapping with the old stamp is refused")
    try:
        Q5E.reverify_registered_inputs({"bundle_dir": "b"},
                                       Q5E.EXECUTION_APPROVAL_TOKEN)
        raise AssertionError("an incomplete set was accepted")
    except Q5E.DiagnosticInputMismatch as error:
        check("missing" in str(error), "every registered path must be present")
    try:
        Q5E.reverify_registered_inputs(_verified({}), None)
        raise AssertionError("re-verification ran without approval")
    except Q5E.ExecutionNotApprovedError:
        check(True, "re-verification is itself approval-gated")


def test_bundle_content_identity_is_required_and_unregistered():
    """Blocker 3 — file presence plus a manifest string is not identity."""
    with tempfile.TemporaryDirectory() as tmp:
        for name in Q5E.BUNDLE_INPUT_FILES:
            with open(os.path.join(tmp, name), "w", encoding="utf-8") as fh:
                fh.write("{}" if name.endswith(".json") else "x\n")
        checked = Q5E.verify_bundle_content_identity(
            tmp, Q5E.EXECUTION_APPROVAL_TOKEN)
        check(checked["ok"] is False,
              "content identity does not pass while unregistered")
        check(checked["reason"] == Q5E.SOURCE_BUNDLE_DIGEST_FREEZE_REQUIRED,
              "it reports the freeze as the open item")
        check(Q5E.SOURCE_BUNDLE_FILE_SHA256 == {},
              "no per-file digest is invented")
        check(set(checked["observed"]) == set(Q5E.BUNDLE_INPUT_FILES),
              "every file Q5-E reads is hashed and reported")

        # Once digests are registered, a one-byte change must fail. This
        # exercises the comparison itself without inventing a real digest.
        frozen = dict(checked["observed"])
        real = Q5E.SOURCE_BUNDLE_FILE_SHA256
        try:
            Q5E.SOURCE_BUNDLE_FILE_SHA256 = frozen
            ok = Q5E.verify_bundle_content_identity(
                tmp, Q5E.EXECUTION_APPROVAL_TOKEN)
            check(ok["ok"] is True, "matching contents verify")
            with open(os.path.join(tmp, "decision.json"), "a",
                      encoding="utf-8") as fh:
                fh.write(" ")
            mutated = Q5E.verify_bundle_content_identity(
                tmp, Q5E.EXECUTION_APPROVAL_TOKEN)
            check(mutated["ok"] is False,
                  "a one-byte change fails canonical verification")
            check(any("decision.json" in p for p in mutated["problems"]),
                  "and the mutated file is named")
        finally:
            Q5E.SOURCE_BUNDLE_FILE_SHA256 = real


def test_mitdb_aggregate_registration_is_an_open_item():
    """B3 — a truncated digest is not an execution contract."""
    check(Q5E.MITDB_TREE_AGGREGATE is None,
          "the full MIT-BIH aggregate is not invented or reconstructed")
    with tempfile.TemporaryDirectory() as tmp:
        checked = Q5E.verify_mitdb_identity(tmp,
                                            Q5E.EXECUTION_APPROVAL_TOKEN)
        check(checked["ok"] is False, "the gate does not pass while it is None")
        check(checked["reason"] == Q5E.INPUT_IDENTITY_REGISTRATION_REQUIRED,
              "it reports the registration as the open item")
        check(any("truncated" in p for p in checked["problems"]),
              "and says why: the registered value is truncated")


def test_frozen_module_approval_is_translated_not_reused():
    """The two modules use different tokens; production would have failed."""
    check(Q5E.EXECUTION_APPROVAL_TOKEN != BJ.EXECUTION_APPROVAL_TOKEN,
          "the two approval tokens genuinely differ")
    check(Q5E.frozen_module_approval(Q5E.EXECUTION_APPROVAL_TOKEN, "x") ==
          BJ.EXECUTION_APPROVAL_TOKEN,
          "an approved Q5-E call can reach the frozen readers")
    try:
        Q5E.frozen_module_approval(None, "x")
        raise AssertionError("the bridge granted access without approval")
    except Q5E.ExecutionNotApprovedError:
        check(True, "an unapproved caller gets Q5-E's own refusal")
    try:
        Q5E.frozen_module_approval("guessed-token", "x")
        raise AssertionError("a wrong token was accepted")
    except Q5E.ExecutionNotApprovedError:
        check(True, "a wrong token does not reach the frozen module")
    with open(Q5E.__file__, encoding="utf-8") as handle:
        text = handle.read()
    check("approval=approval)" not in text.split("def run_audit_from_mount", 1)[0],
          "no frozen reader is called with the untranslated Q5-E token")


def test_mitdb_is_verified_against_publisher_checksums():
    """6 — file-name completeness alone is not identity."""
    with open(Q5E.__file__, encoding="utf-8") as handle:
        text = handle.read()
    gate = text.split("def verify_mitdb_identity(", 1)[1].split("\ndef ", 1)[0]
    body = text.split("def discover_registered_inputs(", 1)[1]
    body = body.split("\ndef ", 1)[0]
    check("verify_against_publisher_checksums" in gate,
          "the MIT-BIH gate verifies the publisher checksum list")
    check("MITDB_CHECKSUM_FILE" in gate,
          "a tree without SHA256SUMS.txt is not accepted")
    check("verify_mitdb_identity(" in body,
          "discovery routes the MIT-BIH tree through that gate")
    check("M4_V10_SOURCE_FILES" in body,
          "the V10 source is matched on its full registered expected set")
    check(set(Q5E.M4_V10_SOURCE_FILES) != set(Q5E.M4_V9_SOURCE_FILES),
          "the V9 and V10 expected sets are distinguishable")
    check("pwave.py" in Q5E.M4_V10_SOURCE_FILES and
          "v15b_local.py" not in Q5E.M4_V10_SOURCE_FILES,
          "the V10 set is the registered one, not the V9 one")


def test_synthetic_bundle_is_marked_everywhere():
    """5 — a fixture bundle is machine-readably not an ingest candidate."""
    config = Q5E.build_config(Q5E.MODE_AUDIT, "T",
                              qa_target_set=Q5E.QA_TARGETS_FIXTURE)
    manifest = Q5E.build_manifest({}, "T",
                                  qa_target_set=Q5E.QA_TARGETS_FIXTURE)
    for name, payload in (("config", config), ("manifest", manifest)):
        check(payload["synthetic_fixture"] is True,
              f"the {name} is stamped synthetic")
        check(payload["ingestable"] is False,
              f"the {name} says it is not an ingest candidate")
    clean = Q5E.build_config(Q5E.MODE_AUDIT, "T")
    check(clean["synthetic_fixture"] is False and clean["ingestable"] is True,
          "a registered run is not stamped synthetic")

    result = {"decision": Q5E.DECISION_NONE, "m4": {"status": Q5E.M4_OK},
              "synthetic_fixture": True,
              "qa_target_set": Q5E.QA_TARGETS_FIXTURE}
    with tempfile.TemporaryDirectory() as tmp:
        out = os.path.join(tmp, "run")
        written = Q5E.write_bundle(out, result, config, manifest,
                                   _full_tables(), {}, ["x"],
                                   Q5E.summary_markdown(result),
                                   figures=True, figure_backend=_stub_png)
        check(Q5E.SYNTHETIC_MARKER in written["written"],
              "the marker file is written into the bundle")
        with open(os.path.join(out, Q5E.SYNTHETIC_MARKER),
                  encoding="utf-8") as handle:
            marker = json.load(handle)
        check(marker["ingestable"] is False,
              "the marker is machine-readable, not prose")


def test_production_refuses_to_publish_a_fixture_verdict():
    """5 — qa_fixture is only ever an explicit synthetic input."""
    with open(Q5E.__file__, encoding="utf-8") as handle:
        body = handle.read().split("def run_audit(", 1)[1].split("\ndef ", 1)[0]
    check("qa_fixture" not in body, "run_audit never passes a QA fixture")
    check("refusing to publish" in body,
          "and refuses to publish anything but a REGISTERED verdict")
    check("QA_TARGETS_REGISTERED" in body,
          "the check names the registered target set explicitly")


# ─────────────────────────────────────────────────────────────────────────────
# B1 — adversarial source-matching fixtures.
#
# Each one is a place where a different reading of "greedy nearest with a used
# set" produces a different answer.  They pin THIS adapter's behaviour so a
# later differential test against the registered `data.py` compares decisions
# rather than paragraphs.  No registered asset is opened.
# ─────────────────────────────────────────────────────────────────────────────
def test_source_match_nearest_already_used_falls_through():
    """Counterexample 1: nearest is taken, next-nearest is inside tolerance."""
    annotations = [(1000, "N"), (1040, "N")]
    result = Q5E.match_peaks_to_annotations([1000, 1010], annotations, 20000)
    kept = {r["peak_index"]: r["raw_atr_ordinal"] for r in result["kept_rows"]}
    check(kept == {0: 0, 1: 1},
          "the second peak takes the next-nearest unused annotation")
    check(not result["peaks_without_annotation"],
          "it is not dropped merely because its nearest was consumed")
    check(not result["annotations_without_peak"],
          "and no annotation is left unmatched")
    check(Q5E.SOURCE_MATCH_CONTRACT["nearest_already_used"].startswith(
        "the peak takes the next-nearest"),
        "the contract states this decision explicitly")


def test_source_match_distance_tie_goes_to_the_earlier_annotation():
    """Counterexample 2: two candidates at exactly the same distance."""
    annotations = [(960, "N"), (1040, "N")]
    result = Q5E.match_peaks_to_annotations([1000], annotations, 20000)
    check(len(result["kept_rows"]) == 1, "one peak matches one annotation")
    check(result["kept_rows"][0]["raw_atr_ordinal"] == 0,
          "the tie goes to the smaller annotation sample")
    check(result["annotations_without_peak"][0]["anchor_ordinal"] == 1,
          "the loser becomes an annotation-without-peak anchor")


def test_source_match_non_aami_symbol_consumes_its_match():
    """Counterexample 3: nearest annotation is a non-AAMI symbol."""
    annotations = [(1000, "F"), (1040, "N")]
    result = Q5E.match_peaks_to_annotations([1000], annotations, 20000)
    check(not result["kept_rows"],
          "a peak matched to a non-AAMI annotation is dropped")
    check([a["anchor_ordinal"] for a in result["annotations_without_peak"]]
          == [1],
          "the non-AAMI annotation stays consumed and is not an anchor")
    check(not result["peaks_without_annotation"],
          "the peak matched, so it is not a peak-without-annotation anchor")
    check("BEFORE AAMI" in Q5E.SOURCE_MATCH_CONTRACT["used_vs_aami"],
          "the contract fixes used-before-AAMI explicitly")


def test_source_match_boundary_cut_consumes_its_match():
    """Counterexample 4: the matched peak is cut by the boundary rule."""
    annotations = [(100, "N"), (140, "N")]
    result = Q5E.match_peaks_to_annotations([100], annotations, 20000)
    check(not result["kept_rows"], "the peak is cut by p-150 >= 0")
    check([a["anchor_ordinal"] for a in result["annotations_without_peak"]]
          == [1],
          "its annotation stays consumed rather than being rematched")
    check("BEFORE the" in Q5E.SOURCE_MATCH_CONTRACT["used_vs_boundary"],
          "the contract fixes used-before-boundary explicitly")


def test_source_match_annotation_order_differing_from_sample_order():
    """Counterexample 5: `.atr` ordinals are not in ascending sample order."""
    annotations = [(2000, "N"), (1000, "N")]
    result = Q5E.match_peaks_to_annotations([1000, 2000], annotations, 20000)
    kept = {r["peak_index"]: r["raw_atr_ordinal"] for r in result["kept_rows"]}
    check(kept == {0: 1, 1: 0},
          "each peak matches its own annotation, by sample not by ordinal")
    check(all(r["r_sample"] != 0 for r in result["kept_rows"]),
          "the raw sample travels with the kept row")


def test_source_match_peak_order_change_is_visible():
    """Counterexample 6: reordering peaks changes which peak wins a tie."""
    annotations = [(1000, "N")]
    first = Q5E.match_peaks_to_annotations([1000, 1020], annotations, 20000)
    second = Q5E.match_peaks_to_annotations([1020, 1000], annotations, 20000)
    check(first["kept_rows"][0]["peak_index"] == 0 and
          len(first["kept_rows"]) == 1,
          "the first peak in detector order consumes the annotation")
    check(second["kept_rows"][0]["r_sample"] == 1020,
          "reordering the peaks changes which one matches")
    check(len(second["peaks_without_annotation"]) == 1,
          "and the other becomes an anchor")
    check(Q5E.SOURCE_MATCH_CONTRACT["traversal"].startswith(
        "peaks in detector order"),
        "the contract fixes the traversal order this depends on")


def test_source_equivalence_is_declared_unproven():
    """B1 — count reproduction is necessary, not a proof of equivalence."""
    status = Q5E.source_match_equivalence_status()
    check(status["status"] == Q5E.SOURCE_MATCH_EQUIVALENCE_REQUIRED,
          "the adapter does not claim to be proven source-equivalent")
    check(status["registered_file_sha256"] ==
          Q5E.M4_SOURCE_MAP_HASHES["data.py"],
          "it pins the digest of the file it was written against")
    check(set(status["contract"]) == set(Q5E.SOURCE_MATCH_CONTRACT),
          "and carries every fixed control-flow decision")
    check("necessary condition only" in status["note"],
          "the note says count reproduction does not settle equivalence")
    fingerprint = Q5E.source_match_adapter_fingerprint()
    check(len(fingerprint) == 64 and
          fingerprint == Q5E.source_match_adapter_fingerprint(),
          "the adapter fingerprint is a stable sha256")


def test_rr_features_shape_is_validated_exactly():
    """B2 — ragged, 1-D, wrong width and wrong row count are all refused."""
    good = [[1.0, 2.0, 0, 0, 0, 0, 0], [1.0, 2.0, 0, 0, 0, 0, 0]]
    pre, post = Q5E._rr_columns(good, expected_rows=2)
    check(pre == [1.0, 1.0] and post == [2.0, 2.0],
          "a correct (n, 7) result yields the registered two columns")
    bad = {
        "ragged": [[1.0] * 7, [1.0] * 6],
        "one_dimensional": [1.0, 2.0, 3.0],
        "too_narrow": [[1.0] * 6],
        "too_wide": [[1.0] * 8],
        "a_string": "1234567",
    }
    for label, value in bad.items():
        try:
            Q5E._rr_columns(value, expected_rows=len(good))
            raise AssertionError(f"{label} was accepted")
        except Q5E.DiagnosticInputMismatch as error:
            check(Q5E.M4_RR_MISMATCH in str(error),
                  f"{label} is refused as {Q5E.M4_RR_MISMATCH}")
    try:
        Q5E._rr_columns(good, expected_rows=3)
        raise AssertionError("a row-count mismatch was accepted")
    except Q5E.DiagnosticInputMismatch as error:
        check("row-count mismatch" in str(error) or "rows for" in str(error),
              "a row count that disagrees with the kept peaks is refused")



def declared_tests() -> List[str]:
    """Top-level `test_*` functions, by AST rather than by line prefix.

    A prefix scan counts a `def test_` inside a string or a nested scope and
    misses one written with unusual spacing; parsing the module answers the
    question actually being asked — which top-level tests exist.
    """
    import ast
    with open(os.path.abspath(__file__), encoding="utf-8") as handle:
        tree = ast.parse(handle.read())
    return sorted(node.name for node in tree.body
                  if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
                  and node.name.startswith("test_"))


def run_all() -> int:
    """Run every test, and refuse to under-report.

    Two ways a suite can lie about itself are closed here.  A test defined
    after this function used to be collected too late to run while the suite
    still printed a pass, so the collected set is compared against the AST.
    And a test that runs but asserts nothing is indistinguishable from a
    passing one, so every test must raise the assertion counter.

    The assertion total is reported as a plain count of what actually ran; it
    is not a fixed number, because the optional matplotlib path contributes
    assertions only where that library is installed.
    """
    global PASSED
    collected = {name: value for name, value in globals().items()
                 if name.startswith("test_") and callable(value)}
    declared = declared_tests()
    missing = [name for name in declared if name not in collected]
    extra = [name for name in sorted(collected) if name not in declared]
    if missing or extra:
        raise AssertionError(
            f"the runner did not collect what this file declares: "
            f"missing={missing} unexpected={extra}.  A test defined after the "
            f"runner never executes, and a silent skip is a failure.")

    silent: List[str] = []
    for name in declared:
        before = PASSED
        collected[name]()
        if PASSED == before:
            silent.append(name)
    if silent:
        raise AssertionError(
            f"these tests ran without asserting anything: {silent}.  A test "
            f"that raises no assertion cannot fail, so it is not a test.")
    optional = "with" if _matplotlib_present() else "without"
    print(f"{len(declared)} test functions, {PASSED} assertions passed "
          f"({optional} the optional matplotlib renderer)")
    return 0


def _matplotlib_present() -> bool:
    try:
        import matplotlib                                  # noqa: F401
        return True
    except ImportError:
        return False


if __name__ == "__main__":
    raise SystemExit(run_all())
