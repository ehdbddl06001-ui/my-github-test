#!/usr/bin/env python3
"""CPU test contract for EXP-2026-004 / Q5-A (spec section 14).

No GPU, no training, no Drive. Everything here runs on synthetic fixtures; a
synthetic smoke bundle is never labelled as a measured result.
"""
from __future__ import annotations

import json
import os
import shutil
import sys
import tempfile

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

_MODULES_BEFORE = set(sys.modules)

import q4o_leakage_free_residual as Q4O  # noqa: E402
import q4q_transportability_replication as QQ  # noqa: E402
import q5a_patient_failure_atlas as QA  # noqa: E402

_MODULES_AFTER = set(sys.modules)

PASSED = 0
FAILED = 0


def check(cond: bool, label: str) -> None:
    global PASSED, FAILED
    if cond:
        PASSED += 1
        print(f"  PASS  {label}")
    else:
        FAILED += 1
        print(f"  FAIL  {label}")


def expect_raise(fn, label: str, exc=Exception) -> None:
    try:
        fn()
    except exc:
        check(True, label)
    else:
        check(False, label + " (no exception raised)")


def _fixture(tmp: str, n_per: int = 60, seed: int = 5,
             skill9: float = 2.0, skill10: float = 4.0):
    """Cohort + two discoverable fixture runs (V9-like and V10-like)."""
    cohort = QA.synthetic_atlas(n_per_record=n_per, seed=seed)
    m9 = QA.synthetic_model(cohort, "V9", skill=skill9, seed=3)
    m10 = QA.synthetic_model(cohort, "V10", skill=skill10, seed=4)
    runs = os.path.join(tmp, "runs")
    QA.write_synthetic_run(os.path.join(runs, "20260101T0000_v9_kink_noctx"),
                           "kink_noctx", cohort, m9, s_prauc=0.597)
    QA.write_synthetic_run(os.path.join(runs, "20260102T0000_v10_pwave"),
                           "pwave", cohort, m10, s_prauc=0.660)
    inv = QA.scan_inventory([runs], log=Q4O.RunLog(echo=False))
    freeze = QA.freeze_baseline(inv)
    models = {lab: QA.load_model_predictions(sel["run_dir"], lab,
                                             log=Q4O.RunLog(echo=False))
              for lab, sel in freeze["selected"].items()}
    return cohort, inv, freeze, models, runs


def _dir_fingerprint(root: str) -> dict:
    out = {}
    for dirpath, _d, files in os.walk(root):
        for f in sorted(files):
            p = os.path.join(dirpath, f)
            out[os.path.relpath(p, root)] = Q4O.sha256_file(p)
    return out


# ─────────────────────────────────────────────────────────────────────────────
def test_import_is_inert():
    print("import has no training and no Drive side effect")
    new = _MODULES_AFTER - _MODULES_BEFORE
    check("torch" not in sys.modules, "torch is not imported by Q5-A")
    check(not any(m.startswith("google.colab") for m in new),
          "no Colab/Drive import at module load")
    info = QA.assert_analysis_only()
    check(info["analysis_only"] is True,
          "assert_analysis_only finds no training call in the module")
    check(QA.self_check()["analysis_only"] is True,
          "self_check re-runs the analysis-only proof")
    check(QA.self_check()["default_mode"] == "DESIGN",
          "default mode is DESIGN")
    src = open(QA.__file__, encoding="utf-8").read()
    check("drive.mount" not in src, "module never mounts Drive itself")


def test_modes():
    print("mode resolution — exactly one")
    for m in QA.MODES:
        check(QA.resolve_mode(m.lower()) == m, f"mode {m} resolves")
    expect_raise(lambda: QA.resolve_mode("FULL"), "unknown mode rejected")
    expect_raise(lambda: QA.resolve_mode(""), "empty mode rejected")
    check(QA.MODES == ("DESIGN", "INVENTORY", "ANALYZE", "REPORT"),
          "the four pre-registered modes, in order")


def test_beat_keys_and_positional_ban():
    print("stable beat keys; positional matching is forbidden")
    cohort = QA.synthetic_atlas(n_per_record=30)
    check(cohort.key_mode == QA.KEY_MODE_ANNOTATION,
          "annotation key wins when a sample index exists")
    check(len(set(cohort.key.tolist())) == cohort.n, "keys are unique")
    expect_raise(lambda: QA.assert_not_positional(np.arange(10)),
                 "0..n-1 row index rejected as positional matching",
                 QA.Q5AError)
    QA.assert_not_positional(np.array(["mitdb|100|7|A"]))
    check(True, "structured keys accepted")
    # no sample field and no waveform -> aggregate only, never row order
    expect_raise(lambda: QA.build_beat_keys({"pid": np.arange(4)}, beat=None),
                 "no sample index and no waveform -> aggregate-only STOP",
                 QA.Q5AError)
    keys, mode, _p = QA.build_beat_keys(
        {"pid": np.array([100, 100, 101])},
        beat=np.array([[[0.0, 1.0]], [[0.5, 2.0]], [[0.1, 0.2]]]))
    check(mode == QA.KEY_MODE_FINGERPRINT,
          "waveform fingerprint is the documented fallback")
    check(len(set(keys.tolist())) == 3, "fingerprint keys unique")
    dup_beat = np.array([[[0.0, 1.0]], [[0.0, 1.0]]])
    expect_raise(lambda: QA.build_beat_keys({"pid": np.array([100, 100])},
                                            beat=dup_beat),
                 "non-unique fingerprints STOP instead of guessing",
                 QA.Q5AError)
    fp1 = QA.waveform_fingerprint(dup_beat)
    fp2 = QA.waveform_fingerprint(dup_beat)
    check(list(fp1) == list(fp2), "fingerprint is deterministic")


def test_matching_hard_stops():
    print("matching audit hard stops")
    cohort = QA.synthetic_atlas(n_per_record=30)
    model = QA.synthetic_model(cohort, "M", seed=1)
    audit = QA.match_beat_keys(cohort, model)
    check(audit["pass"] and audit["matched"] == cohort.n,
          "clean fixture matches every beat on the stable key")
    check(audit["s_mismatch"] == 0, "S mismatch is 0 on the clean fixture")
    check(audit["positional_matching_used"] is False,
          "audit records that row order was never used")

    conflict = QA.ModelPredictions(
        label="conflict", key=cohort.key.copy(), score=model.score.copy(),
        y_true=~cohort.y_s, record=cohort.record.copy())
    expect_raise(lambda: QA.match_beat_keys(cohort, conflict),
                 "label conflict on an identical key is a HARD STOP",
                 QA.Q5AError)

    dup_key = cohort.key.copy()
    dup_key[1] = dup_key[0]
    dup = QA.ModelPredictions(label="dup", key=dup_key,
                              score=model.score.copy(),
                              y_true=cohort.y_s.copy(),
                              record=cohort.record.copy())
    a = QA.match_beat_keys(cohort, dup, strict=False)
    check(not a["pass"] and a["n_duplicate_keys_model"] >= 1,
          "duplicate keys fail the gate instead of being resolved silently")

    s_rows = np.where(cohort.y_s)[0]
    keep = np.ones(cohort.n, bool)
    keep[s_rows[:3]] = False
    missing = QA.ModelPredictions(
        label="missing_s", key=cohort.key[keep], score=model.score[keep],
        y_true=cohort.y_s[keep], record=cohort.record[keep])
    a = QA.match_beat_keys(cohort, missing, strict=False)
    check(not a["pass"] and a["s_mismatch"] == 3,
          "unexplained S-beat mismatch fails the gate")

    alien = QA.ModelPredictions(
        label="alien", key=np.array([f"otherdb|9|{i}|N" for i in range(5)]),
        score=np.zeros(5), y_true=np.zeros(5, bool),
        record=np.full(5, 999))
    a = QA.match_beat_keys(cohort, alien, strict=False)
    check(not a["pass"], "a model that shares no key fails loudly")


def test_split_and_inclusion():
    print("DS1/DS2 split, S-free records, bootstrap unit")
    cohort = QA.synthetic_atlas(n_per_record=30)
    split = QA.cohort_split(cohort)
    check(not (set(split["ds1"]) & set(split["ds2"])),
          "DS1/DS2 patient overlap is 0")
    check(sorted(split["ds1"]) == sorted(QA.DS1_RECORDS)
          and sorted(split["ds2"]) == sorted(QA.DS2_RECORDS),
          "canonical de Chazal split reused from Q4-Q, not redefined")
    check("descriptive" in split["note"] and "untouched" in split["note"],
          "DS2 is labelled a descriptive audit, not an untouched test set")

    y = np.array([1, 0, 0, 0, 0, 0], bool)
    rec = np.array([1, 1, 1, 2, 2, 2])
    score = np.array([0.9, 0.1, 0.2, 0.5, 0.4, 0.3])
    pr = QA.per_record_prauc(y, score, rec, [1, 2])
    check(set(pr) == {1}, "a record without S is excluded from S PR-AUC")
    rep = QA.record_inclusion_report(y, rec, [1, 2])
    check(rep["n_records_total"] == 2 and rep["n_records_with_s"] == 1
          and rep["excluded_records"][0]["record"] == 2,
          "excluded records are reported separately with the reason")

    ci = QA.boot_ci({1: 0.5, 2: 0.7, 3: 0.9}, n_boot=200)
    check(ci["n_record"] == 3, "bootstrap resamples RECORDS, not beats")
    check(abs(ci["mean"] - 0.7) < 1e-9, "bootstrap mean is the record mean")


def test_no_ds2_feedback():
    print("DS2 labels never move a threshold, a bin edge or a proxy")
    cohort = QA.synthetic_atlas(n_per_record=40)
    split = QA.cohort_split(cohort)
    model = QA.synthetic_model(cohort, "M", seed=2)
    t1 = QA.ds1_locked_threshold(model, split)
    flipped = QA.ModelPredictions(
        label="M", key=model.key, score=model.score,
        y_true=np.where(np.isin(model.record, split["ds2"]),
                        ~model.y_true, model.y_true),
        record=model.record)
    t2 = QA.ds1_locked_threshold(flipped, split)
    check(t1["threshold"] == t2["threshold"] and t1["source"] == t2["source"],
          "DS1-locked threshold is identical after flipping every DS2 label")
    check(t1["uses_ds2_labels"] is False, "threshold declares no DS2 label use")

    ds1_rows = np.sort(cohort.rows_of(split["ds1"]))
    rr = QA.rr_features(cohort, ds1_rows)
    edges1 = QA.ds1_quantile_bins(rr["coupling_ratio"])
    cohort2 = QA.synthetic_atlas(n_per_record=40)
    ds2_rows = np.isin(cohort2.record, split["ds2"])
    cohort2.y_s[ds2_rows] = ~cohort2.y_s[ds2_rows]
    edges2 = QA.ds1_quantile_bins(
        QA.rr_features(cohort2, np.sort(cohort2.rows_of(split["ds1"])))
        ["coupling_ratio"])
    check(edges1 == edges2, "bin edges come from DS1 only")

    rows = np.sort(cohort.rows_of(split["ds2"]))
    a1 = QA.atrial_proxies(cohort, rows)
    a2 = QA.atrial_proxies(cohort2, rows)
    same = all(np.allclose(a1[k], a2[k], equal_nan=True) for k in a1)
    check(same, "atrial proxies are label-free (identical after a DS2 flip)")
    check(QA.BLOCK_MARGIN == 1.25 and QA.BLOCK_MIN_PATIENT_DIRECTION == 0.60,
          "branch-rule constants are pre-registered module constants")


def test_inventory_and_freeze():
    print("inventory + baseline freeze (provenance only)")
    tmp = tempfile.mkdtemp(prefix="q5a_inv_")
    try:
        _c, inv, freeze, _m, runs = _fixture(tmp, n_per=20)
        check(inv["n_candidates"] == 2, "both fixture runs inventoried")
        check(all(e["beat_level_ready"] for e in inv["entries"]),
              "prediction probe finds scores + y_true + a stable key")
        check(freeze["status"] == "FROZEN", "clean fixture freezes cleanly")
        check(set(freeze["beat_level_models"]) == {"V9", "V10"},
              "both baselines enter the beat-level comparison")

        # selection must not depend on the recorded performance number
        swapped = json.loads(json.dumps(inv))
        vals = [e.get("recorded_s_prauc") for e in swapped["entries"]]
        for e, v in zip(swapped["entries"], reversed(vals)):
            e["recorded_s_prauc"] = v
        f2 = QA.freeze_baseline(swapped)
        check({k: v["run_id"] for k, v in f2["selected"].items()}
              == {k: v["run_id"] for k, v in freeze["selected"].items()},
              "swapping the recorded S PR-AUC does not change the selection")

        dup = json.loads(json.dumps(inv))
        clone = json.loads(json.dumps(dup["entries"][1]))
        clone["run_id"] = "20260103T0000_v10_pwave_rerun"
        dup["entries"].append(clone)          # same model name, second run
        fa = QA.freeze_baseline(dup)
        check(fa["status"] == "AMBIGUOUS_BASELINE",
              "two runs with the same model name -> AMBIGUOUS_BASELINE (STOP)")
        near = json.loads(json.dumps(inv))
        variant = json.loads(json.dumps(near["entries"][1]))
        variant["run_id"] = "20260103T0000_v10_pwave_v2"
        variant["model_name"] = "pwave_v2"
        near["entries"].append(variant)
        fn_ = QA.freeze_baseline(near)
        check(fn_["selected"]["V10"]["model_name"] == "pwave",
              "an exact historical name beats a near-miss variant")
        g = QA.evaluate_artifact_gates(dup, fa, None)
        check(not g["pass"] and g["branch"] == QA.BRANCH_INSUFFICIENT,
              "ambiguous baseline blocks the analysis at D0")

        inc = json.loads(json.dumps(inv))
        inc["entries"][0]["metric_definition"] = "beat_micro_s_prauc"
        inc["entries"][1]["metric_definition"] = "record_macro_s_prauc"
        fi = QA.freeze_baseline(inc)
        check(fi["status"] == "INCOMPATIBLE_BASELINES",
              "different metric definitions -> INCOMPATIBLE_BASELINES")

        agg = json.loads(json.dumps(inv))
        for e in agg["entries"]:
            e["beat_level_ready"] = False
        fg = QA.freeze_baseline(agg)
        check(fg["aggregate_only_models"] and not fg["beat_level_models"],
              "artifacts without stable keys stay aggregate-only")
        g2 = QA.evaluate_artifact_gates(agg, fg, None)
        check(not g2["pass"], "no beat-level artifact -> gate STOP (no retrain)")
        check("retraining" in fg and "forbidden" in fg["retraining"],
              "freeze states that retraining a missing model is forbidden")

        empty = QA.scan_inventory([os.path.join(tmp, "nope")],
                                  log=Q4O.RunLog(echo=False))
        check(empty["n_candidates"] == 0, "a missing root is recorded, not fatal")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_metrics_recomputation():
    print("metric re-computation fixture")
    y = np.array([1, 0, 1, 0, 0, 0], bool)
    perfect = np.array([0.9, 0.1, 0.8, 0.2, 0.05, 0.0])
    check(abs(QA.beat_micro_prauc(y, perfect) - 1.0) < 1e-9,
          "perfect ranking gives beat-micro PR-AUC 1.0")
    expect_raise(lambda: QA.beat_micro_prauc(np.zeros(4, bool), perfect[:4]),
                 "single-class PR-AUC refuses to return a number", QA.Q5AError)
    tm = QA.threshold_metrics(y, perfect, 0.5)
    check(tm["s_recall"] == 1.0 and tm["s_precision"] == 1.0,
          "threshold metrics agree with the hand-computed fixture")
    cal = QA.brier_and_calibration(np.array([1, 0], bool), np.array([1.0, 0.0]))
    check(cal["brier"] == 0.0 and cal["ece"] == 0.0,
          "perfect probabilities give Brier 0 / ECE 0")
    ps = QA.patient_summary({1: 0.1, 2: 0.5, 3: 0.9, 4: 0.7, 5: 0.3, 6: 0.2})
    check(ps["worst5"][0]["record"] == 1 and len(ps["worst5"]) == 5,
          "worst-5 patients are the five lowest records")
    check(abs(ps["median"] - 0.4) < 1e-9, "patient median as expected")

    freeze = {"selected": {"V10": {"recorded_s_prauc_claim": 0.660}}}
    rows = QA.baseline_claim_check(
        {"V10": {"beat_micro_s_prauc": 0.661, "record_macro_s_prauc": 0.40}},
        freeze)
    check("consistent" in rows[0]["verdict"] and
          rows[0]["closest_unit"] == "beat_micro",
          "a claim reproduced under one metric unit is reported as such")
    rows = QA.baseline_claim_check(
        {"V10": {"beat_micro_s_prauc": 0.20, "record_macro_s_prauc": 0.25}},
        freeze)
    check("NOT reproduced" in rows[0]["verdict"],
          "an unreproduced claim stays explicitly unverified")
    rows = QA.baseline_claim_check({}, freeze)
    check("NOT_RECOMPUTED" in rows[0]["verdict"],
          "a baseline without beat-level artifacts is not silently dropped")


def test_subtype_and_audit_records():
    print("S subtype mapping and the 208/213 audit")
    sym = np.array(["A", "a", "J", "S", "N", "V"])
    sub = QA.subtype_of(sym)
    check(list(sub[:4]) == ["A", "a", "J", "S"],
          "the four AAMI-S source symbols keep their identity")
    check(list(sub[4:]) == ["other", "other"], "non-S symbols map to other")
    check(QA.S_SUBTYPES == ("A", "a", "J", "S"), "subtype set is frozen")

    cohort = QA.synthetic_atlas(n_per_record=40)
    model = QA.synthetic_model(cohort, "V10", seed=9)
    rows = np.arange(cohort.n)
    tab = QA.subtype_metrics(cohort, rows, {"V10": model}, "V10", 0.5)
    small = [r for r in tab if r["n"] < QA.SUBTYPE_MIN_N]
    check(all(r["descriptive_only"] for r in small),
          "small subtypes are flagged descriptive_only")
    check(all("fn_rate" in r for r in tab if r["n"]),
          "each non-empty subtype reports an FN rate")

    audit = QA.record_audit_208_213(cohort, {"V10": QA.match_beat_keys(
        cohort, model, strict=False)})
    check([a["record"] for a in audit] == [208, 213],
          "208 and 213 get their own audit rows")
    check(all(a["present_in_atlas"] for a in audit)
          and all("class_counts_atlas" in a for a in audit),
          "the audit reports per-record class composition")
    check(all("12.7" in a["known_deficit"] for a in audit),
          "the measured Q4-Q beat deficit is carried into the audit")


def test_block_evidence():
    print("feature-block incremental value (patient-held-out)")
    rng = np.random.RandomState(0)
    groups = np.repeat(np.arange(12), 40)
    signal = rng.randn(len(groups))
    noise = rng.randn(len(groups))
    y = (signal + 0.3 * rng.randn(len(groups)) > 0.4).astype(int)
    good = QA.block_incremental_value({}, {"signal": signal}, y, groups,
                                      n_boot=200)
    bad = QA.block_incremental_value({}, {"noise": noise}, y, groups,
                                     n_boot=200)
    check(good["delta_logloss"] > bad["delta_logloss"],
          "an informative block beats a pure-noise block")
    check(good["ci_low"] > 0, "informative block CI excludes 0")
    check(good["n_patient"] == 12 and set(map(int, good["per_patient_delta"]))
          == set(range(12)),
          "held-out evaluation is per patient, and the CI is a patient bootstrap")
    check("stable_after_record_drop" in good
          and len(good["top_influence_records"])
          == QA.DROP_RECORDS_FOR_STABILITY,
          "record-drop stability is computed for every block")

    few = QA.evaluate_blocks({"B_RR": {"x": signal[:50]}},
                             np.zeros(50, int), groups[:50], n_boot=50,
                             log=Q4O.RunLog(echo=False))
    check(few["underpowered"] and not few["blocks"],
          f"fewer than {QA.BLOCK_MIN_EVENTS} error events -> underpowered")


def _ev(mean, lo, hi, direction=0.8, stable=True, adj_lo=None):
    return {"delta_logloss": mean, "ci_low": lo, "ci_high": hi,
            "patient_direction_frac": direction,
            "stable_after_record_drop": stable,
            "adjusted_delta_logloss": mean,
            "adjusted_ci_low": lo if adj_lo is None else adj_lo,
            "adjusted_ci_high": hi}


ATRIAL_OK = {"concordant_enough": True, "has_independent_support": True,
             "n_concordant": 3}
ATRIAL_WEAK = {"concordant_enough": False, "has_independent_support": False,
               "n_concordant": 1}
PATIENT_DIFFUSE = {"available": True, "heterogeneity_large": True,
                   "failure_persists_across_models": True}
PATIENT_TIGHT = {"available": True, "heterogeneity_large": False,
                 "failure_persists_across_models": False}
GATE_OK = {"pass": True, "stops": [], "branch": None}


def test_decision_tree_all_branches():
    print("pre-registered decision tree — every branch")
    d0 = QA.evaluate_branch_decision(
        {"pass": False, "stops": ["baseline provenance unclear"],
         "branch": QA.BRANCH_INSUFFICIENT}, {"blocks": {}}, None,
        {"available": False})
    check(d0["branch"] == QA.BRANCH_INSUFFICIENT and d0["rule"] == "D0",
          "D0 INSUFFICIENT_ARTIFACTS fires first")
    d0b = QA.evaluate_branch_decision(
        {"pass": False, "stops": ["S mismatch unexplained"],
         "branch": QA.BRANCH_DATA_BLOCKED}, {"blocks": {}}, None,
        {"available": False})
    check(d0b["branch"] == QA.BRANCH_DATA_BLOCKED,
          "D0 DATA_INTEGRITY_BLOCKED on a matching failure")
    check("not a modelling experiment" in d0b["next_step"],
          "D0 next step is artifact recovery, not a model experiment")

    d1 = QA.evaluate_branch_decision(
        GATE_OK, {"blocks": {"B_QUALITY": _ev(0.05, 0.02, 0.08),
                             "B_RR": _ev(0.01, -0.01, 0.03),
                             "B_ATRIAL": _ev(0.005, -0.02, 0.03)}},
        ATRIAL_WEAK, PATIENT_TIGHT)
    check(d1["branch"] == QA.BRANCH_QUALITY and d1["rule"] == "D1",
          "D1 quality/preprocessing branch")
    check("classifier" in d1["next_step"] or "quality gate" in d1["next_step"],
          "D1 next step intervenes on quality, not on architecture")

    d2 = QA.evaluate_branch_decision(
        GATE_OK, {"blocks": {"B_ATRIAL": _ev(0.06, 0.03, 0.09),
                             "B_RR": _ev(0.02, -0.01, 0.05),
                             "B_QUALITY": _ev(0.01, -0.02, 0.04)}},
        ATRIAL_OK, PATIENT_TIGHT)
    check(d2["branch"] == QA.BRANCH_ATRIAL and d2["rule"] == "D2",
          "D2 atrial-evidence branch when the proxies concur")
    check("residual CNN" in d2["next_step"],
          "D2 explicitly rules out the closed residual CNN direction")
    d2_weak = QA.evaluate_branch_decision(
        GATE_OK, {"blocks": {"B_ATRIAL": _ev(0.06, 0.03, 0.09),
                             "B_RR": _ev(0.02, -0.01, 0.05)}},
        ATRIAL_WEAK, PATIENT_TIGHT)
    check(d2_weak["branch"] == QA.BRANCH_UNRESOLVED,
          "a leading atrial block without proxy concordance -> UNRESOLVED")

    d3 = QA.evaluate_branch_decision(
        GATE_OK, {"blocks": {"B_RR": _ev(0.07, 0.04, 0.10),
                             "B_ATRIAL": _ev(0.02, -0.01, 0.05),
                             "B_QUALITY": _ev(0.01, -0.01, 0.03)}},
        ATRIAL_OK, PATIENT_TIGHT)
    check(d3["branch"] == QA.BRANCH_RR and d3["rule"] == "D3",
          "D3 RR/timing branch")

    d4 = QA.evaluate_branch_decision(
        GATE_OK, {"blocks": {"B_RR": _ev(0.01, -0.02, 0.04, direction=0.4),
                             "B_ATRIAL": _ev(0.01, -0.03, 0.05,
                                             direction=0.45)}},
        ATRIAL_WEAK, PATIENT_DIFFUSE)
    check(d4["branch"] == QA.BRANCH_PATIENT and d4["rule"] == "D4",
          "D4 diffuse patient shift when no block qualifies but failure persists")
    check("GroupDRO is NOT pre-selected" in d4["next_step"],
          "D4 proposes an ERM vs CVaR/GroupDRO pilot, not GroupDRO by decree")

    d5 = QA.evaluate_branch_decision(
        GATE_OK, {"blocks": {"B_RR": _ev(0.01, -0.02, 0.04, direction=0.4),
                             "B_ATRIAL": _ev(0.01, -0.03, 0.05,
                                             direction=0.45)}},
        ATRIAL_WEAK, PATIENT_TIGHT)
    check(d5["branch"] == QA.BRANCH_UNRESOLVED and d5["rule"] == "D5",
          "D5 UNRESOLVED is a permitted verdict")
    check(set(QA.BRANCHES) >= {d0["branch"], d1["branch"], d2["branch"],
                               d3["branch"], d4["branch"], d5["branch"]},
          "every produced branch is a pre-registered label")


def test_branch_not_by_largest_mean():
    print("branch selection is never 'largest mean'")
    big_but_unstable = {"blocks": {
        "B_RR": _ev(0.20, -0.05, 0.45, direction=0.55, stable=False),
        "B_QUALITY": _ev(0.04, 0.02, 0.06)}}
    d = QA.evaluate_branch_decision(GATE_OK, big_but_unstable, ATRIAL_WEAK,
                                    PATIENT_TIGHT)
    check(d["branch"] == QA.BRANCH_QUALITY,
          "the largest mean loses to a smaller stable effect with a CI > 0")

    tied = {"blocks": {"B_RR": _ev(0.050, 0.02, 0.08),
                       "B_QUALITY": _ev(0.048, 0.02, 0.08)}}
    d = QA.evaluate_branch_decision(GATE_OK, tied, ATRIAL_WEAK, PATIENT_TIGHT)
    check(d["branch"] == QA.BRANCH_UNRESOLVED,
          f"a tie inside the {QA.BLOCK_MARGIN}x margin -> UNRESOLVED")

    record_dependent = {"blocks": {
        "B_QUALITY": _ev(0.09, 0.03, 0.15, stable=False)}}
    d = QA.evaluate_branch_decision(GATE_OK, record_dependent, ATRIAL_WEAK,
                                    PATIENT_TIGHT)
    check(d["branch"] == QA.BRANCH_UNRESOLVED,
          "an effect that dies when the top records are dropped is not a branch")

    adjusted_away = {"blocks": {
        "B_QUALITY": _ev(0.09, 0.03, 0.15, adj_lo=-0.01)}}
    d = QA.evaluate_branch_decision(GATE_OK, adjusted_away, ATRIAL_WEAK,
                                    PATIENT_TIGHT)
    check(d["branch"] == QA.BRANCH_UNRESOLVED,
          "a block that vanishes once the other blocks are adjusted for fails")


def test_language_boundary():
    print("language boundary — association, never cause")
    src = open(QA.__file__, encoding="utf-8").read()
    check("P-wave presence truth" not in src
          and "P_wave_ground_truth" not in src,
          "no proxy is ever named P-wave ground truth")
    meta = QA.ATRIAL_PROXY_META
    check(all("independence" in v and "expected_direction" in v
              for v in meta.values()),
          "every atrial proxy declares direction and independence")
    check(any("OVERLAPS V10" in v["independence"] for v in meta.values()),
          "proxies overlapping V10's own features are marked, not hidden")
    check(meta["qrs_leakage_estimate"]["independence"].startswith("confounder"),
          "QRS leakage is declared a confounder, not evidence")
    sup = {"caveat": QA.atrial_support({}, np.zeros(0, bool),
                                       np.zeros(0, int))["caveat"]}
    check("ground truth" in sup["caveat"] and "proxies" in sup["caveat"],
          "the atrial support table carries the no-ground-truth caveat")
    check("residual CNN" in QA.CLOSED_DIRECTIONS
          and "INCART rescue" in QA.CLOSED_DIRECTIONS,
          "closed directions are declared in the module")
    brief = QA.q5b_design_brief(
        {"branch": QA.BRANCH_ATRIAL, "rule": "D2", "reason": "x",
         "competing_branches": [], "trace": []}, {"blocks": {}}, {})
    check(brief["negative_controls"] and brief["single_intervention_variable"],
          "the Q5-B brief names one variable and its negative controls")
    check("NOT created" in brief["not_implemented"],
          "the brief states that Q5-B is not implemented")


def test_calibration_vs_ranking():
    print("calibration vs ranking split")
    cohort = QA.synthetic_atlas(n_per_record=30)
    model = QA.synthetic_model(cohort, "V10", skill=4.0, seed=11)
    rows = np.arange(cohort.n)
    out = QA.calibration_vs_ranking(cohort, rows, model, 0.99)
    check(out["n_fn"] > 0 and out["fn_that_are_threshold_only"] >= 0,
          "FNs are split into threshold-only and ranking failures")
    check(out["fn_that_are_threshold_only"] + out["fn_that_are_ranking_failures"]
          <= out["n_fn"], "the split never exceeds the FN count")
    check("closed direction" in out["note"],
          "the alarm-rate dial is explicitly not reopened")


def test_analyze_bundle_and_immutability():
    print("ANALYZE bundle schema, source immutability, REPORT")
    tmp = tempfile.mkdtemp(prefix="q5a_run_")
    try:
        cohort, inv, freeze, models, runs = _fixture(tmp, n_per=40)
        before = _dir_fingerprint(runs)
        out = os.path.join(tmp, "out")
        res = QA.run_atlas(cohort, models, inv, freeze,
                           QA.provenance_for(None), out, n_boot=150,
                           smoke=True, log=Q4O.RunLog(echo=False))
        after = _dir_fingerprint(runs)
        check(before == after, "source run bundles are byte-identical after Q5-A")
        check(res["source_immutable"] is True,
              "the result records the immutability check")
        check(res["status"] == QA.STATUS_SMOKE and res["status"] != "MEASURED",
              "a synthetic smoke bundle is never labelled MEASURED")
        check(res["training_performed"] is False and res["analysis_only"],
              "the result declares that no training happened")
        QA.verify_bundle(out)
        check(True, "full bundle schema + all 13 figures present")
        check(len(QA.FIGURES) == 13, "13 required visualisations")
        for name in ("patient_metrics.csv", "mechanism_evidence.csv",
                     "matching_audit.csv", "decision.json", "summary.md"):
            check(os.path.exists(os.path.join(out, name)),
                  f"{name} written")
        summary = open(os.path.join(out, "summary.md"), encoding="utf-8").read()
        check("실패 연관 요인" in summary and "원인" in summary,
              "the Korean summary states association, not cause")
        check("Q5-B" in summary and "실행하지 않았" in summary,
              "the summary says the next experiment has not been run")
        mech = open(os.path.join(out, "mechanism_evidence.csv"),
                    encoding="utf-8").read()
        check("failure-ASSOCIATED, not causal" in mech,
              "the evidence CSV carries the interpretation boundary")
        check(res["split"]["ds1"] and res["split"]["ds2"]
              and not set(res["split"]["ds1"]) & set(res["split"]["ds2"]),
              "the bundle records a DS1/DS2 split with 0 overlap")

        # REPORT re-displays without recomputing or writing
        fp_before = _dir_fingerprint(out)
        rep = QA.report_bundle(out)
        fp_after = _dir_fingerprint(out)
        check(fp_before == fp_after, "REPORT does not write into the bundle")
        check(rep["recomputed"] is False and rep["status"] == res["status"],
              "REPORT reports the stored status and recomputes nothing")
        check(len(rep["figures"]) == len(QA.FIGURES) and rep["summary_md"],
              "REPORT finds every stored figure and the summary")
        missing = QA.report_bundle(os.path.join(tmp, "nothing"))
        check(missing["status"] == QA.STATUS_NOT_RUN,
              "REPORT on an empty path says RESULT NOT RUN")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_blocked_bundle():
    print("BLOCKED_MEASURED bundle schema")
    tmp = tempfile.mkdtemp(prefix="q5a_blocked_")
    try:
        cohort, inv, freeze, models, runs = _fixture(tmp, n_per=20)
        broken = dict(models)
        lab = sorted(broken)[0]
        m = broken[lab]
        keys = m.key.copy()
        keys[:] = np.array([f"otherdb|1|{i}|N" for i in range(len(keys))])
        broken[lab] = QA.ModelPredictions(
            label=lab, key=keys, score=m.score, y_true=m.y_true,
            record=m.record, source_dir=m.source_dir)
        out = os.path.join(tmp, "blocked")
        res = QA.run_atlas(cohort, broken, inv, freeze,
                           QA.provenance_for(None), out, n_boot=100,
                           log=Q4O.RunLog(echo=False))
        check(res["status"] == QA.STATUS_BLOCKED,
              "a failed matching gate produces BLOCKED_MEASURED, not a crash")
        check(res["decision"]["branch"] == QA.BRANCH_DATA_BLOCKED,
              "the blocked bundle carries the D0 DATA_INTEGRITY_BLOCKED branch")
        QA.verify_bundle(out, blocked=True)
        check(True, "blocked bundle schema complete")
        check("BLOCKED_MEASURED" in json.load(
            open(os.path.join(out, "result.json"), encoding="utf-8"))["note"],
            "the blocked bundle states that this is a valid measured outcome")
        check(os.path.exists(os.path.join(out, "figures",
                                          "inventory_gate_dashboard.png")),
              "the gate dashboard is still drawn when the gate fails")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_notebook_static():
    print("notebook static validation")
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                     "notebooks", "quest50_q5a_patient_failure_atlas.ipynb")
    if not os.path.exists(p):
        check(False, "quest50 notebook missing")
        return
    nb = json.load(open(p, encoding="utf-8"))
    cells = nb["cells"]
    src = ["".join(c["source"]) for c in cells]
    all_src = "\n".join(src)
    cfg = next((s for s in src if "MODE = " in s), "")
    check("assert MODE in VALID_MODES" in cfg,
          "exactly-one-mode assertion present")
    check('MODE = "DESIGN"' in cfg, "default mode is DESIGN")
    first_md = "".join(cells[0]["source"])
    check("RESULT NOT RUN" in first_md,
          "front page declares RESULT NOT RUN before any analysis")
    check("EXP-2026-004" in first_md and "Q5-A" in first_md,
          "front page identifies the experiment")
    check("ANALYSIS ONLY" in first_md and "NO TRAINING" in first_md,
          "front page declares analysis-only / no training")
    check("실패 연관 요인" in first_md and "원인" in first_md,
          "front page states association, not cause")
    check("residual CNN" in first_md and "INCART" in first_md,
          "front page repeats the closed directions")
    check(all(m in all_src for m in QA.MODES), "all four modes wired")
    check(not any(c.get("outputs") for c in cells if c["cell_type"] == "code"),
          "design notebook committed without stored outputs")
    check("1p3HvC_bnbiQlEanFOVIvVdejy60W0tho" in all_src
          and "1aSj_1jvS_W2iruVnORIG6DTVuHobzNzq" in all_src
          and "1ZCAYZCl4T4eoZzdFfV_IzkB0Mgbcqlw4" in all_src,
          "Drive file/folder ids for the declared inputs are shown")
    check("sys.modules.pop" in all_src and "NEED_Q5A" in all_src
          and "Restart runtime" in all_src,
          "stale-import guard after git pull")
    check('"/content/my-github-test"' in all_src
          and 'os.chdir("/content")' in all_src,
          "repo bootstrap anchors an absolute clone path")
    check("test_q4o" in all_src and "test_q4p" in all_src
          and "test_q4q" in all_src and "test_q5a" in all_src,
          "regression suites (Q4-O/Q4-P/Q4-Q) plus Q5-A run in the notebook")
    stale = ("branch selected:" in all_src.lower()
             or "MEASURED —" in all_src)
    check(not stale, "no stale measured-result claims")


def test_spec_and_docs():
    print("spec contract")
    root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
    spec = os.path.join(root, "experiments", "specs",
                        "EXP-2026-004-q5a-patient-failure-atlas.md")
    if not os.path.exists(spec):
        check(False, "Q5-A spec missing")
        return
    text = open(spec, encoding="utf-8").read()
    check("result_status: RESULT_NOT_RUN" in text,
          "spec frontmatter says RESULT_NOT_RUN")
    check("kind: preregistered_analysis_only" in text,
          "spec declares the analysis-only kind")
    for f in ("experiments/specs/EXP-2026-004-q5a-patient-failure-atlas.md",
              "mit-bih/q5a_patient_failure_atlas.py",
              "mit-bih/test_q5a_patient_failure_atlas.py",
              "notebooks/quest50_q5a_patient_failure_atlas.ipynb",
              "research/ASSETS.md", "research/PROJECT_STATE.md"):
        check(f in text, f"spec lists the allowed file {f}")
    for b in QA.BRANCHES:
        check(b in text, f"spec documents branch {b}")
    check("Q5-B" in text and ("구현하지 않는다" in text or "만들지 않는다" in text),
          "spec states Q5-B is not implemented in this PR")


def test_regression_suites_importable():
    print("Q4-O / Q4-P / Q4-Q remain intact")
    check(Q4O.MODULE_VERSION >= 4, "Q4-O module present")
    check(QQ.MODULE_VERSION >= 6, "Q4-Q module present")
    check(QA.DS1_RECORDS is QQ.DS1_RECORDS and QA.DS2_RECORDS is QQ.DS2_RECORDS,
          "Q5-A reuses Q4-Q's canonical split objects (no drift)")
    check(QA.S_INDEX == QQ.MIT_S_INDEX, "S class index reused, not redefined")


def main() -> int:
    print("=" * 78)
    print(f"EXP-2026-004 / Q5-A test contract ({QA.STATUS})")
    print("=" * 78)
    for fn in (test_import_is_inert, test_modes, test_beat_keys_and_positional_ban,
               test_matching_hard_stops, test_split_and_inclusion,
               test_no_ds2_feedback, test_inventory_and_freeze,
               test_metrics_recomputation, test_subtype_and_audit_records,
               test_block_evidence, test_decision_tree_all_branches,
               test_branch_not_by_largest_mean, test_language_boundary,
               test_calibration_vs_ranking, test_analyze_bundle_and_immutability,
               test_blocked_bundle, test_notebook_static, test_spec_and_docs,
               test_regression_suites_importable):
        fn()
    print("=" * 78)
    print(f"passed {PASSED} - failed {FAILED}")
    print("=" * 78)
    return 1 if FAILED else 0


if __name__ == "__main__":
    sys.exit(main())
