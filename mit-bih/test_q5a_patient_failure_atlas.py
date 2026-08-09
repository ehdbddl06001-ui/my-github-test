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
             skill_control: float = 2.0, skill_primary: float = 4.0,
             with_v9: bool = True):
    """Cohort + the four frozen baselines: V10 `pwave` / `base` and
    V9 `kink_noctx` / `v8base`, each with its own paired control."""
    cohort = QA.synthetic_atlas(n_per_record=n_per, seed=seed)
    ctrl = QA.synthetic_model(cohort, "V10_BASE", skill=skill_control, seed=3)
    prim = QA.synthetic_model(cohort, "V10", skill=skill_primary, seed=4)
    runs = os.path.join(tmp, "runs")
    QA.write_synthetic_run(os.path.join(runs, "20260102T0000_base"),
                           "base", cohort, ctrl, s_prauc=0.573)
    QA.write_synthetic_run(os.path.join(runs, "20260102T0100_pwave"),
                           "pwave", cohort, prim, s_prauc=0.660)
    if with_v9:
        v9 = QA.synthetic_model(cohort, "V9", skill=1.0, seed=6)
        v9b = QA.synthetic_model(cohort, "V9_BASE", skill=0.8, seed=7)
        QA.write_synthetic_run(os.path.join(runs, "20260101T0000_kink_noctx"),
                               "kink_noctx", cohort, v9, s_prauc=0.597)
        QA.write_synthetic_run(os.path.join(runs, "20260101T0100_v8base"),
                               "v8base", cohort, v9b, s_prauc=0.576)
    inv = QA.scan_inventory([runs], log=Q4O.RunLog(echo=False))
    freeze = QA.freeze_baseline(inv)
    models = {lab: QA.load_model_predictions(sel["run_dir"], lab,
                                             log=Q4O.RunLog(echo=False))
              for lab, sel in freeze["selected"].items()}
    return cohort, inv, freeze, models, runs


def _write_legacy_run(dir_path: str, cohort, model, rows: np.ndarray) -> str:
    """The 2026-07/08 ablation layout: <run>/<tag>/ens.npz with prob/y/pid
    and NO annotation index."""
    os.makedirs(dir_path, exist_ok=True)
    prob = np.zeros((len(rows), 3), float)
    prob[:, QA.S_COLUMN] = model.score[rows]
    prob[:, 0] = 1.0 - model.score[rows]
    np.savez_compressed(os.path.join(dir_path, "ens.npz"), prob=prob,
                        y=cohort.y5[rows].astype(int),
                        pid=cohort.record[rows].astype(int))
    return dir_path


def _write_frozen_source(path: str, cohort) -> str:
    """A mamba_data-like frozen source: beat/y/pid plus the `t` sample index."""
    samples = np.array([int(str(k).split("|")[2]) for k in cohort.key])
    np.savez_compressed(path, beat=cohort.beat, y=cohort.y5.astype(int),
                        pid=cohort.record.astype(int), t=samples,
                        sym=cohort.sym.astype(str), db=cohort.db.astype(str))
    return path


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
        check(inv["n_candidates"] == 4, "all fixture runs inventoried")
        check(all(e["beat_level_ready"] for e in inv["entries"]),
              "prediction probe finds scores + y_true + a stable key")
        check(freeze["status"] == "FROZEN", "clean fixture freezes cleanly")
        check(set(freeze["beat_level_models"])
              == {"V9", "V9_BASE", "V10", "V10_BASE"},
              "both primaries and both paired controls enter")
        check(freeze["selected"]["V10"]["role"] == QA.ROLE_PRIMARY
              and freeze["selected"]["V10_BASE"]["role"] == QA.ROLE_CONTROL,
              "roles are recorded on the frozen selection")
        check(freeze["selected"]["V10_BASE"]["model_name"] == "base",
              "the 'base' control is not confused with 'v8base'")

        # selection must not depend on the recorded performance number
        swapped = json.loads(json.dumps(inv))
        vals = [e.get("recorded_s_prauc") for e in swapped["entries"]]
        for e, v in zip(swapped["entries"], reversed(vals)):
            e["recorded_s_prauc"] = v
        f2 = QA.freeze_baseline(swapped)
        check({k: v["run_id"] for k, v in f2["selected"].items()}
              == {k: v["run_id"] for k, v in freeze["selected"].items()},
              "swapping the recorded S PR-AUC does not change the selection")

        def _entry(d, name):
            return next(e for e in d["entries"] if e["model_name"] == name)

        # a genuinely different run that carries the same model name, kept in
        # its own root so it cannot leak into the later checks
        amb = os.path.join(tmp, "amb")
        other = QA.synthetic_model(_c, "V10b", skill=3.3, seed=99)
        QA.write_synthetic_run(os.path.join(amb, "20260103T0000_pwave_rerun"),
                               "pwave", _c, other, s_prauc=0.61)
        dup = QA.scan_inventory([runs, amb], log=Q4O.RunLog(echo=False))
        fa = QA.freeze_baseline(dup)
        check(fa["status"] == "AMBIGUOUS_BASELINE",
              "two runs with the same model name -> AMBIGUOUS_BASELINE (STOP)")
        check("pwave" in " ".join(fa["reasons"]),
              "the ambiguous target is named in the reason")
        near = json.loads(json.dumps(inv))
        variant = json.loads(json.dumps(_entry(near, "pwave")))
        variant["run_id"] = "20260103T0000_v10_pwave_v2"
        variant["model_name"] = "pwave_noc"
        near["entries"].append(variant)
        fn_ = QA.freeze_baseline(near)
        check(fn_["selected"]["V10"]["model_name"] == "pwave",
              "an exact name beats a longer name containing the token "
              "(pwave vs pwave_noc)")

        # the same package reachable by two paths is ONE artifact, not two
        import shutil as _sh
        _sh.copytree(os.path.join(runs, "20260102T0100_pwave"),
                     os.path.join(tmp, "copy", "20260102T0100_pwave"))
        both = QA.scan_inventory([runs, os.path.join(tmp, "copy")],
                                 log=Q4O.RunLog(echo=False))
        fb = QA.freeze_baseline(both)
        check(fb["status"] == "FROZEN" and fb["collapsed_duplicates"],
              "a package unzipped twice collapses to one candidate, recorded")
        check(not any("duplicate" in r for r in fb["reasons"]),
              "the collapse note stays out of `reasons` so a STOP message "
              "shows only real blockers")
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


def test_absent_historical_baseline():
    print("a baseline recorded in prose but never saved is a RESULT")
    tmp = tempfile.mkdtemp(prefix="q5a_absent_")
    try:
        _c, inv, freeze, _m, _runs = _fixture(tmp, n_per=20, with_v9=False)
        check(freeze["status"] == "MISSING_BASELINE",
              "a missing PRIMARY baseline (V9) stops the analysis")
        check(not QA.evaluate_artifact_gates(inv, freeze, None)["pass"],
              "missing primary -> D0 gate STOP")

        # a purely historical target that is absent must NOT block
        tgt = {k: dict(v) for k, v in QA.BASELINE_TARGETS.items()}
        tgt["GHOST"] = {"name_tokens": ("never_saved",),
                        "role": QA.ROLE_HISTORICAL, "recorded_s_prauc": 0.5,
                        "note": "fixture"}
        full = _fixture(tmp + "2", n_per=20)[1]
        fz = QA.freeze_baseline(full, targets=tgt)
        check(fz["status"] == "FROZEN_WITH_ABSENT_BASELINE",
              "an absent historical baseline is recorded, not a stop")
        absent = {a["label"]: a for a in fz["absent_baselines"]}
        check(absent["GHOST"]["status"] == "ARTIFACT_ABSENT"
              and "UNVERIFIED" in absent["GHOST"]["consequence"],
              "its claim is carried and marked unverified")
        check("does not retrain" in absent["GHOST"]["consequence"],
              "absence never triggers retraining")
        check(QA.evaluate_artifact_gates(full, fz, None)["pass"],
              "the analysis proceeds on the artifacts that DO exist")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_legacy_adapter():
    print("legacy ablation artifacts (prob/y/pid, no annotation index)")
    tmp = tempfile.mkdtemp(prefix="q5a_legacy_")
    try:
        cohort = QA.synthetic_atlas(n_per_record=30)
        src = _write_frozen_source(os.path.join(tmp, "mamba_like.npz"), cohort)
        split = QA.cohort_split(cohort)
        ds2_rows = np.sort(cohort.rows_of(split["ds2"]))
        prim = QA.synthetic_model(cohort, "V10", skill=4.0, seed=4)
        ctrl = QA.synthetic_model(cohort, "V10_BASE", skill=2.0, seed=3)
        runs = os.path.join(tmp, "runs")
        step9d = os.path.join(runs, "ablation_step9d")
        _write_legacy_run(os.path.join(step9d, "pwave"), cohort, prim, ds2_rows)
        _write_legacy_run(os.path.join(step9d, "base"), cohort, ctrl, ds2_rows)
        # a same-named control in an UNRELATED run must not be able to collide
        # (different content, so it is a real rival — not a duplicate path)
        other = QA.synthetic_model(cohort, "OTHER", skill=1.1, seed=21)
        _write_legacy_run(os.path.join(runs, "ablation_step11", "base"),
                          cohort, other, ds2_rows)

        inv = QA.scan_inventory([runs], log=Q4O.RunLog(echo=False))
        names = sorted(e["model_name"] for e in inv["entries"])
        check("pwave" in names and names.count("base") == 2,
              "tag folders become their own inventory rows (ens.npz found "
              "by KEY, not by file name)")
        tag_row = next(e for e in inv["entries"] if e["model_name"] == "pwave")
        check(tag_row["beat_key_mode" if False else "beat_key_modes"]
              == [QA.KEY_MODE_SOURCE_VERIFIED],
              "legacy rows are flagged as needing source verification")
        check(tag_row["beat_level_ready"] and tag_row["needs_source_verification"],
              "legacy rows count as beat-level ONLY through verification")

        only_v10 = {k: v for k, v in QA.BASELINE_TARGETS.items()
                    if k in ("V10", "V10_BASE")}
        freeze = QA.freeze_baseline(inv, targets=only_v10)
        check(freeze["status"] == "FROZEN",
              "two same-named `base` runs do not make the freeze ambiguous")
        check(os.path.basename(os.path.dirname(
            freeze["selected"]["V10_BASE"]["run_dir"])) == "ablation_step9d",
            "the paired control is scoped to the primary's own run")

        src_index = QA.load_frozen_source_index(src, log=Q4O.RunLog(echo=False))
        expect_raise(lambda: QA.load_model_predictions(
            freeze["selected"]["V10"]["run_dir"], "V10"),
            "no annotation index and no frozen source -> STOP (row order is "
            "never a fallback)", QA.Q5AError)
        m = QA.load_model_predictions(freeze["selected"]["V10"]["run_dir"],
                                      "V10", source_index=src_index,
                                      log=Q4O.RunLog(echo=False))
        check(m.key_mode == QA.KEY_MODE_SOURCE_VERIFIED
              and m.verification["verified"] and m.verification["subset"] == "ds2",
              "row correspondence verified element-wise against the source")
        check(len(m.score) == len(ds2_rows)
              and np.allclose(m.score, prim.score[ds2_rows]),
              "the S column of the stored class matrix is read, not a guess")
        audit = QA.match_beat_keys(cohort, m, strict=False)
        check(audit["pass"] and audit["matched"] == len(ds2_rows),
              "verified keys join back to the atlas cohort exactly")

        # corruption must be caught, not absorbed
        bad_dir = os.path.join(tmp, "bad", "pwave")
        os.makedirs(bad_dir, exist_ok=True)
        with np.load(os.path.join(step9d, "pwave", "ens.npz")) as z:
            pid = np.asarray(z["pid"]).copy()
            pid[5] = 999
            np.savez_compressed(os.path.join(bad_dir, "ens.npz"),
                                prob=z["prob"], y=z["y"], pid=pid)
        bad = QA.load_model_predictions(bad_dir, "V10",
                                        source_index=src_index,
                                        log=Q4O.RunLog(echo=False))
        ex = bad.verification["excluded_records"]
        bad_recs = {e["record"] for e in ex}
        check(bad.verification["subset"] == "per_record"
              and bad_recs == {100, 999},
              "an altered record id excludes only the record it damaged (and "
              "the phantom it invented); per-record verification keeps the rest")
        check(len(bad.score) < len(ds2_rows) and ex[0]["reason"],
              "the excluded record is dropped from the model and given a reason")

        worse = os.path.join(tmp, "worse", "pwave")
        os.makedirs(worse, exist_ok=True)
        with np.load(os.path.join(step9d, "pwave", "ens.npz")) as z:
            np.savez_compressed(os.path.join(worse, "ens.npz"),
                                prob=z["prob"], y=1 - np.asarray(z["y"]),
                                pid=z["pid"])
        expect_raise(lambda: QA.load_model_predictions(
            worse, "V10", source_index=src_index),
            "if no record verifies, the artifact is rejected outright",
            QA.Q5AError)

        layout = QA.detect_score_layout(np.zeros((10, 3)), 10)
        check(layout["kind"] == "class_matrix" and layout["s_column"] == 1,
              "(n,3) is read as a class matrix with S at column 1")
        check(QA.detect_score_layout(np.zeros((5, 10)), 10)["kind"] == "per_seed",
              "(n_seed,n) is read as a per-seed stack")
        expect_raise(lambda: QA.detect_score_layout(np.zeros((7, 7)), 10),
                     "an uninterpretable shape is an error, not a guess",
                     QA.Q5AError)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def _float_time_cohort(unit: str, n_per: int = 30):
    """A cohort whose source time column is FLOAT — measured 2026-08-09:
    mamba_data.npz stores `t` as floating point, so `0.0` (not `0`)."""
    c = QA.synthetic_atlas(n_per_record=n_per)
    samples = QA.key_sample_values(c.key)
    t = samples if unit == "samples" else samples / c.fs
    c.key = QA.format_beat_keys(c.db, c.record, t.astype("float64"), c.sym)
    c.pre_rr = np.full(c.n, np.nan)
    c.post_rr = np.full(c.n, np.nan)
    return c


def test_float_time_column():
    print("float time column: the unit is verified, never assumed")
    for unit in ("samples", "seconds"):
        c = _float_time_cohort(unit)
        check("|0.0|" in "|".join(c.key[:1]) or ".0" in str(c.key[0]),
              f"[{unit}] the key really carries a float sample field")
        got = QA.infer_time_unit(c.key, c.record, c.fs)
        check(got["unit"] == unit,
              f"[{unit}] unit recovered from the data ("
              f"median RR {got['median_rr_seconds']:.3f}s)")
        idx, _u = QA.annotation_sample_index(c)
        check(idx.dtype.kind == "i" and idx.min() >= 0,
              f"[{unit}] an integer annotation sample index is derived")
        rep = QA.rr_from_samples(c)
        check(rep["derived"] and 0.25 <= rep["median_pre_rr_s"] <= 2.5,
              f"[{unit}] RR comes out physiological ("
              f"{rep['median_pre_rr_s']:.3f}s)")

    # an unusable column must stop, not pick the least-bad reading
    c = QA.synthetic_atlas(n_per_record=30)
    weird = np.arange(c.n, dtype="float64") * 1e6
    c.key = QA.format_beat_keys(c.db, c.record, weird, c.sym)
    expect_raise(lambda: QA.infer_time_unit(c.key, c.record, c.fs),
                 "an implausible interval stops instead of guessing a unit",
                 QA.Q5AError)

    # the float key must survive the legacy adapter round trip unchanged
    tmp = tempfile.mkdtemp(prefix="q5a_float_")
    try:
        c = _float_time_cohort("seconds")
        t = QA.key_sample_values(c.key)
        src = os.path.join(tmp, "src.npz")
        np.savez_compressed(src, beat=c.beat, y=c.y5.astype(int),
                            pid=c.record.astype(int), t=t.astype("float64"),
                            sym=c.sym.astype(str), db=c.db.astype(str))
        split = QA.cohort_split(c)
        rows = np.sort(c.rows_of(split["ds2"]))
        m = QA.synthetic_model(c, "V10", skill=4.0, seed=4)
        d = os.path.join(tmp, "runs", "ablation_step9d", "pwave")
        _write_legacy_run(d, c, m, rows)
        si = QA.load_frozen_source_index(src, log=Q4O.RunLog(echo=False))
        mp = QA.load_model_predictions(d, "V10", source_index=si,
                                       log=Q4O.RunLog(echo=False))
        check(list(mp.key) == list(c.key[rows]),
              "float `t` formats identically on both sides of the join "
              "(no 0.0 -> 0 cast)")
        audit = QA.match_beat_keys(c, mp, strict=False)
        check(audit["pass"] and audit["matched"] == len(rows),
              "the adapted legacy artifact matches the cohort exactly")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_patient_persistence_uses_every_pair():
    print("D4's persistence check is the MINIMUM over all model pairs")
    def mk(per_record):
        return {"per_record_s_prauc": {str(k): v for k, v in per_record.items()}}
    # A and B are near-twins (same worst quartile); C fails on other patients.
    a = mk({1: 0.1, 2: 0.2, 3: 0.8, 4: 0.9, 5: 0.95, 6: 0.99, 7: 0.5, 8: 0.6})
    b = mk({1: 0.12, 2: 0.22, 3: 0.82, 4: 0.9, 5: 0.95, 6: 0.99, 7: 0.5, 8: 0.6})
    c = mk({1: 0.9, 2: 0.95, 3: 0.1, 4: 0.15, 5: 0.5, 6: 0.6, 7: 0.8, 8: 0.99})
    twins = QA.patient_heterogeneity({"A": a, "B": b})
    check(twins["failure_persists_across_models"],
          "two near-twins do agree on their worst patients")
    trio = QA.patient_heterogeneity({"A": a, "B": b, "C": c})
    check(not trio["failure_persists_across_models"],
          "adding a model that fails on OTHER patients breaks persistence — "
          "the twin pair can no longer carry the claim alone")
    check(len(trio["worst_quartile_overlap_by_pair"]) == 3
          and trio["worst_quartile_overlap"]
          == min(trio["worst_quartile_overlap_by_pair"].values()),
          "every pair is reported and the minimum is the one that counts")
    gates = {"pass": True, "stops": [], "branch": None}
    blocks = {"blocks": {"B_RR": _ev(0.01, -0.02, 0.04, direction=0.4)}}
    d = QA.evaluate_branch_decision(gates, blocks, ATRIAL_WEAK, trio)
    check(d["branch"] == QA.BRANCH_UNRESOLVED,
          "without persistence across every pair, D4 does not fire")


def test_provenance_narrows_a_true_name_clash():
    print("a real name clash is settled by the RECORDED seed plan, not by score")
    tmp = tempfile.mkdtemp(prefix="q5a_clash_")
    try:
        cohort = QA.synthetic_atlas(n_per_record=20)
        split = QA.cohort_split(cohort)
        rows = np.sort(cohort.rows_of(split["ds2"]))
        root = os.path.join(tmp, "runs")
        pkg = os.path.join(root, "v10pkg_results")
        os.makedirs(pkg)
        for seed in range(1000, 1005):
            m = QA.synthetic_model(cohort, "V10", skill=4.0, seed=seed)
            prob = np.zeros((len(rows), 3))
            prob[:, QA.S_COLUMN] = m.score[rows]
            prob[:, 0] = 1.0 - m.score[rows]
            np.savez_compressed(os.path.join(pkg, f"pwave_s{seed}.npz"),
                                prob=prob, y=cohort.y5[rows].astype(int),
                                pid=cohort.record[rows].astype(int))
        # an unrelated run that happens to use the very same tag name
        rival = QA.synthetic_model(cohort, "RIVAL", skill=1.0, seed=77)
        _write_legacy_run(os.path.join(root, "ablation_step9d", "pwave"),
                          cohort, rival, rows)
        inv = QA.scan_inventory([root], log=Q4O.RunLog(echo=False))
        names = [e["model_name"] for e in inv["entries"]]
        check(names.count("pwave") == 2,
              "both same-named candidates are inventoried")
        fz = QA.freeze_baseline(inv)
        check(fz["selected"]["V10"]["run_dir"] == pkg,
              "the run whose SAVED SEED PLAN matches the record is chosen")
        check(any("seed plan matches the record" in r for r in fz["reasons"]),
              "the provenance rule that settled it is recorded")

        # remove the recorded seed plan -> the clash is unresolved again
        loose = {k: dict(v) for k, v in QA.BASELINE_TARGETS.items()}
        for v in loose.values():
            v.pop("require", None)
        fl = QA.freeze_baseline(inv, targets=loose)
        check(fl["status"] == "AMBIGUOUS_BASELINE",
              "without the provenance requirement the clash still STOPs — the "
              "narrowing is a recorded fact, not a preference")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_seed_family():
    print("per-seed families (<arm>_s<seed>.npz) — one model, N seeds")
    fams = QA.group_seed_families(["pwave_s1000.npz", "pwave_s1001.npz",
                                   "base_s1000.npz", "base_s1001.npz",
                                   "ens.npz", "notes.txt"])
    check(set(fams) == {"pwave", "base"} and len(fams["pwave"]) == 2,
          "files are grouped into one entry per arm")
    check(QA.group_seed_families(["only_s1000.npz"]) == {},
          f"a lone seed file is not a family (min {QA.SEED_FAMILY_MIN})")

    tmp = tempfile.mkdtemp(prefix="q5a_fam_")
    try:
        cohort = QA.synthetic_atlas(n_per_record=40)
        src = _write_frozen_source(os.path.join(tmp, "src.npz"), cohort)
        split = QA.cohort_split(cohort)
        rows = np.sort(cohort.rows_of(split["ds2"]))
        run = os.path.join(tmp, "v10pkg_results")
        os.makedirs(run)
        per_seed = []
        for i, seed in enumerate(range(1000, 1005)):
            m = QA.synthetic_model(cohort, "V10", skill=3.0 + 0.2 * i,
                                   seed=seed)
            prob = np.zeros((len(rows), 3))
            prob[:, QA.S_COLUMN] = m.score[rows]
            prob[:, 0] = 1.0 - m.score[rows]
            per_seed.append(m.score[rows])
            np.savez_compressed(os.path.join(run, f"pwave_s{seed}.npz"),
                                prob=prob, y=cohort.y5[rows].astype(int),
                                pid=cohort.record[rows].astype(int))
        paths, seeds = QA.find_prediction_file(run, arm="pwave")
        check(len(paths) == 5 and seeds == [1000, 1001, 1002, 1003, 1004],
              "the family is found with its seeds, not rejected as ambiguous")

        inv = QA.scan_inventory([tmp], log=Q4O.RunLog(echo=False))
        row = next((e for e in inv["entries"] if e["model_name"] == "pwave"),
                   None)
        check(row is not None and row["seed_family"]["n_seed"] == 5,
              "inventory carries one row per arm with its seed count")

        si = QA.load_frozen_source_index(src, log=Q4O.RunLog(echo=False))
        m = QA.load_model_predictions(run, "V10", source_index=si,
                                      arm="pwave", log=Q4O.RunLog(echo=False))
        check(m.per_seed is not None and m.per_seed.shape[0] == 5
              and m.seeds == [1000, 1001, 1002, 1003, 1004],
              "all five seeds are stacked")
        check(np.allclose(m.score, np.mean(per_seed, axis=0)),
              "the point score is the seed mean of the S column")
        metrics = QA.model_metrics(m, cohort, split, rows, n_boot=100,
                                   ds1_prevalence=0.02)
        expect = float(np.mean([QA.beat_micro_prauc(cohort.y_s[rows], p)
                                for p in per_seed]))
        check(abs(metrics["per_seed_mean_s_prauc"] - expect) < 1e-9,
              "per_seed_mean_s_prauc is the MEAN OF PER-SEED PR-AUC "
              "(the historical 0.660 / 0.597 contract)")
        check(metrics["per_seed_mean_s_prauc"]
              != metrics["beat_micro_s_prauc"],
              "it is NOT the PR-AUC of the averaged probability")
        check(metrics["seed_variability"]["n_seed"] == 5
              and metrics["seed_variability"]["seeds"] == m.seeds,
              "seed variability is recoverable again")

        claim = QA.baseline_claim_check(
            {"V10": metrics},
            {"selected": {"V10": {"recorded_s_prauc_claim":
                                  round(metrics["per_seed_mean_s_prauc"], 3),
                                  "role": "primary"}}})
        check(claim[0]["closest_unit"] == "per_seed_mean_beat_micro"
              and "consistent" in claim[0]["verdict"],
              "a claim recorded in the per-seed-mean unit is recognised as such")

        odd = os.path.join(tmp, "odd")
        os.makedirs(odd)
        with np.load(os.path.join(run, "pwave_s1000.npz")) as z:
            np.savez_compressed(os.path.join(odd, "pwave_s1000.npz"),
                                prob=z["prob"], y=z["y"], pid=z["pid"])
            np.savez_compressed(os.path.join(odd, "pwave_s1001.npz"),
                                prob=z["prob"], y=1 - np.asarray(z["y"]),
                                pid=z["pid"])
        expect_raise(lambda: QA.load_model_predictions(
            odd, "V10", source_index=si, arm="pwave"),
            "a seed file that disagrees on the cohort is a STOP",
            QA.Q5AError)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_rr_and_symbol_recovery():
    print("RR from the annotation index; symbols only when they really join")
    cohort = QA.synthetic_atlas(n_per_record=30)
    cohort.pre_rr = np.full(cohort.n, np.nan)
    cohort.post_rr = np.full(cohort.n, np.nan)
    QA.rr_from_samples(cohort)
    check(np.isfinite(cohort.pre_rr).sum() >= cohort.n - len(cohort.records),
          "pre-RR is derived from the annotation sample index")
    r = cohort.idx_of[int(cohort.records[0])]
    check(np.isnan(cohort.pre_rr[r][0]) and np.isnan(cohort.post_rr[r][-1]),
          "the first/last beat of a record keep an undefined RR")

    tmpd = tempfile.mkdtemp(prefix="q5a_ann_")
    try:
        rep = QA.attach_symbols_from_annotations(cohort, tmpd,
                                                 log=Q4O.RunLog(echo=False))
        check(rep["usable"] is False,
              "an empty annotation dir leaves symbols unusable (no guessing)")
        check(QA.find_annotation_dir(tmpd) is None,
              "the .atr locator reports absence instead of inventing a path")
        d = os.path.join(tmpd, "raw_ann", "mitdb")
        os.makedirs(d)
        open(os.path.join(d, "100.atr"), "wb").close()
        check(QA.find_annotation_dir(tmpd) == d,
              "the locator finds the measured raw_ann/mitdb layout")
    finally:
        shutil.rmtree(tmpd, ignore_errors=True)


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

    # continuous (rank) outcome — the amended primary
    yc = 0.7 * signal + 0.3 * rng.randn(len(groups))
    good_r = QA.block_incremental_value({}, {"signal": signal}, yc, groups,
                                        n_boot=200, mode="regression")
    bad_r = QA.block_incremental_value({}, {"noise": noise}, yc, groups,
                                       n_boot=200, mode="regression")
    check(good_r["delta_logloss"] > bad_r["delta_logloss"]
          and good_r["ci_low"] > 0,
          "regression mode: an informative block beats noise with CI > 0")
    check(good_r["mode"] == "regression"
          and set(map(int, good_r["per_patient_delta"])) == set(range(12)),
          "regression CI is still a patient bootstrap over per-patient loss")
    thin = QA.evaluate_blocks({"B_RR": {"x": signal[:20]}}, yc[:20],
                              groups[:20], n_boot=50, log=Q4O.RunLog(echo=False),
                              outcome=QA.OUTCOME_RANK)
    check(thin["underpowered"] and thin["mode"] == "regression",
          f"fewer than {QA.BLOCK_MIN_OBS} S beats -> rank outcome underpowered")


def test_rank_outcome_is_threshold_free():
    print("within-record rank outcome (amended primary)")
    check(QA.PRIMARY_OUTCOME == QA.OUTCOME_RANK
          and QA.OUTCOME_MODES[QA.OUTCOME_RANK] == "regression",
          "the primary outcome is the threshold-free within-record rank")
    cohort = QA.synthetic_atlas(n_per_record=40)
    rows = np.arange(cohort.n)
    model = QA.synthetic_model(cohort, "V10", skill=4.0, seed=11)
    s_mask = cohort.y_s[rows]
    out = QA.within_record_rank_outcome(cohort, rows, model.score, s_mask)
    y = out["y"]
    check(len(y) == int(s_mask.sum()) and np.isfinite(y).all(),
          "one finite rank per S beat")
    check(y.min() >= 0.0 and y.max() <= 1.0, "the rank lives in [0, 1]")

    # a beat that is the worst-scoring in its record must sit at the top
    rec = cohort.record[rows]
    score = model.score.copy()
    victim = np.where(s_mask)[0][0]
    score[victim] = score[rec == rec[victim]].min() - 1.0
    y2 = QA.within_record_rank_outcome(cohort, rows, score, s_mask)["y"]
    pos = int(np.sum(s_mask[:victim]))
    check(y2[pos] == y2.max() and y2[pos] >= 0.99,
          "the record's worst-ranked beat gets the maximum badness")

    # scaling every score in a record must not move a within-record rank
    score3 = model.score.copy()
    r0 = rec == cohort.records[0]
    score3[r0] = score3[r0] * 0.1
    y3 = QA.within_record_rank_outcome(cohort, rows, score3, s_mask)["y"]
    check(np.allclose(y, y3),
          "a per-record monotone rescale leaves the outcome unchanged — no "
          "global operating point can manufacture it")


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
        cohort, inv, freeze, models, runs = _fixture(tmp, n_per=120)
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
        check(res["primary_outcome"]["name"] == QA.OUTCOME_RANK,
              "the bundle records the amended primary outcome")
        be = res["block_evidence"]
        check(be["outcome"] == QA.OUTCOME_RANK and be["mode"] == "regression",
              "block evidence is computed on the rank outcome")
        sec = res["block_evidence_secondary_fn_outcome"]
        check(sec["outcome"] == QA.OUTCOME_FN,
              "the v1 binary outcome is still reported as secondary")
        mech = open(os.path.join(out, "mechanism_evidence.csv"),
                    encoding="utf-8").read()
        check("outcome" in mech.splitlines()[0] and QA.OUTCOME_RANK in mech
              and QA.OUTCOME_FN in mech,
              "mechanism_evidence.csv carries both outcomes, primary flagged")
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
    first_md = "".join(cells[0]["source"])
    status_line = first_md.splitlines()[2] if len(first_md.splitlines()) > 2 \
        else ""
    measured = "MEASURED" in status_line
    has_out = any(c.get("outputs") for c in cells if c["cell_type"] == "code")
    if measured:
        # executed notebook: the stored outputs ARE the evidence, and the front
        # page must carry the measured verdict instead of a stale NOT RUN.
        check(has_out, "measured notebook keeps its stored outputs")
        check("RESULT NOT RUN" not in status_line,
              "front page status line no longer claims RESULT NOT RUN")
        check("runs/" in first_md and "UNRESOLVED" in first_md,
              "front page cites the run bundle and its verdict")
        check("0.6603" in first_md and "0.5969" in first_md
              and "재현" in first_md,
              "front page reports what the recorded claims recomputed to")
        check("시드별 PR-AUC의 평균" in first_md and "0.7717" in first_md,
              "front page pins the unit of 0.660 next to the ensemble value")
        check("철회" in first_md,
              "front page carries the retractions instead of the stale text")
        check(any(f'MODE = "{m}"' in cfg for m in QA.MODES),
              "executed notebook still pins exactly one valid mode")
    else:
        check("RESULT NOT RUN" in first_md,
              "front page declares RESULT NOT RUN before any analysis")
        check(not has_out, "design notebook committed without stored outputs")
        check('MODE = "DESIGN"' in cfg, "un-executed notebook defaults to DESIGN")
    check("EXP-2026-004" in first_md and "Q5-A" in first_md,
          "front page identifies the experiment")
    check("ANALYSIS ONLY" in first_md and "NO TRAINING" in first_md,
          "front page declares analysis-only / no training")
    check("실패 연관 요인" in first_md and "원인" in first_md,
          "front page states association, not cause")
    check("residual CNN" in first_md and "INCART" in first_md,
          "front page repeats the closed directions")
    check(all(m in all_src for m in QA.MODES), "all four modes wired")
    check("1p3HvC_bnbiQlEanFOVIvVdejy60W0tho" in all_src
          and "1aSj_1jvS_W2iruVnORIG6DTVuHobzNzq" in all_src
          and "1ZCAYZCl4T4eoZzdFfV_IzkB0Mgbcqlw4" in all_src,
          "Drive file/folder ids for the declared inputs are shown")
    check("sys.modules.pop" in all_src and "NEED_Q5A" in all_src
          and "Restart runtime" in all_src,
          "stale-import guard after git pull")
    need = next((int(l.split("=")[1].split("#")[0])
                 for l in all_src.splitlines() if l.startswith("NEED_Q5A =")), 0)
    check(need == QA.MODULE_VERSION,
          f"notebook pins the current module version (NEED_Q5A={need} vs "
          f"MODULE_VERSION={QA.MODULE_VERSION}) — a stale checkout fails in "
          "cell 2, not halfway through the run")
    check("BRANCH" in all_src and "checkout" in all_src,
          "cell 2 checks out an explicit branch instead of assuming main")
    check('"/content/my-github-test"' in all_src
          and 'os.chdir("/content")' in all_src,
          "repo bootstrap anchors an absolute clone path")
    check("test_q4o" in all_src and "test_q4p" in all_src
          and "test_q4q" in all_src and "test_q5a" in all_src,
          "regression suites (Q4-O/Q4-P/Q4-Q) plus Q5-A run in the notebook")
    check("wfdb" in all_src, "cell 2 makes wfdb available (subtype recovery)")


def test_spec_and_docs():
    print("spec contract")
    root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
    spec = os.path.join(root, "experiments", "specs",
                        "EXP-2026-004-q5a-patient-failure-atlas.md")
    if not os.path.exists(spec):
        check(False, "Q5-A spec missing")
        return
    text = open(spec, encoding="utf-8").read()
    measured = "result_status: MEASURED" in text
    check(measured or "result_status: RESULT_NOT_RUN" in text,
          "spec frontmatter carries a legal result_status")
    if measured:
        # a measured spec must name the run it is measured from and the
        # pre-registered verdict; a verdict without a run id is a claim
        # without evidence.
        check("run_id: 20260809T1033" in text and "measured: 2026-08-09" in text,
              "measured spec names the run bundle and the date")
        for b in ("verdict: UNRESOLVED", "qualified (CI>0, adjusted CI>0, "
                  "direction>=0.6, stable): `[]`"):
            check(b in text, f"measured spec records the verdict verbatim: {b}")
        check("Q5-B design brief" in text,
              "measured spec carries the separate Q5-B design brief")
        check("`ablation_step9d/pwave`" in text or "철회" in text,
              "measured spec keeps the retractions visible")
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
    # the brief is a design brief, not an implementation: no Q5-B spec, module
    # or training notebook may exist before the user approves the branch.
    stray = [os.path.join(d, f)
             for sub in ("experiments/specs", "mit-bih", "notebooks")
             for d, _, fs in os.walk(os.path.join(root, sub)) for f in fs
             if "q5b" in f.lower() or "q5-b" in f.lower()]
    check(not stray, f"no Q5-B implementation file exists yet: {stray}")


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
               test_absent_historical_baseline, test_legacy_adapter,
               test_float_time_column, test_seed_family,
               test_provenance_narrows_a_true_name_clash,
               test_patient_persistence_uses_every_pair,
               test_rr_and_symbol_recovery,
               test_metrics_recomputation, test_subtype_and_audit_records,
               test_block_evidence, test_rank_outcome_is_threshold_free,
               test_decision_tree_all_branches,
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
