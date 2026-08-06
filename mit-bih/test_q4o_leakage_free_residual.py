"""Tests for the Q4-O reporting layer.

The contract under test is narrow and strict: the reporting layer must
**reproduce** the run's measured numbers and must **not** invent any.

1. the arm table and contrast tables reproduce ``result.json``;
2. C−A / C−D point estimates and 95% CIs match the source byte-for-byte in value;
3. per-record views average all seeds, never one;
4. no training history is fabricated when the run has none;
5. ``result.json`` (and every other measured artifact) has the same checksum
   before and after the report runs.

Most tests run against a synthetic bundle built here, so they are hermetic. Set
``MEDKOS_Q4O_RUN_DIR`` to the real Drive run to additionally check the actual
artifact::

    MEDKOS_Q4O_RUN_DIR=/content/drive/MyDrive/MedKOS/ecg-model/runs/\
20260806T0923_EXP-2026-001_q4o_leakage_free_residual_cnn \
        python -m pytest mit-bih/test_q4o_leakage_free_residual.py -v

Run: ``python -m pytest mit-bih/test_q4o_leakage_free_residual.py``
"""

from __future__ import annotations

import json
import os
import re
import sys

import numpy as np
import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import q4o_leakage_free_residual as q4o  # noqa: E402


# --------------------------------------------------------------------------
# Synthetic run bundle — internally consistent by construction
# --------------------------------------------------------------------------

SEEDS = [20260806, 20260807, 20260808, 20260809, 20260810]
K_SWEEP = [50, 100, 200, 300]
KS_ALL = list(q4o.K_OPERATING_AND_SWEEP)
N_BOOT = 400
MIN_GAIN = 0.015


def _auroc(y: np.ndarray, p: np.ndarray) -> float:
    pos, neg = p[y], p[~y]
    if pos.size == 0 or neg.size == 0:
        return float("nan")
    ranks = np.argsort(np.argsort(p, kind="stable"), kind="stable") + 1.0
    r_pos = ranks[y].sum()
    return float((r_pos - pos.size * (pos.size + 1) / 2.0) / (pos.size * neg.size))


def _average_precision(y: np.ndarray, p: np.ndarray) -> float:
    order = np.argsort(-p, kind="stable")
    ys = y[order].astype(np.float64)
    tp = np.cumsum(ys)
    precision = tp / np.arange(1, ys.size + 1)
    n_pos = ys.sum()
    return float((precision * ys).sum() / n_pos) if n_pos else float("nan")


def _stats(vals: np.ndarray, record_ids) -> dict:
    v = np.asarray(vals, dtype=np.float64)
    worst_i = int(np.nanargmin(v))
    return {
        "mean": float(np.nanmean(v)),
        "std": float(np.nanstd(v)),
        "p10": float(np.nanpercentile(v, 10)),
        "median": float(np.nanmedian(v)),
        "worst": float(v[worst_i]),
        "worst_record": int(record_ids[worst_i]),
        "n_record": int(np.sum(np.isfinite(v))),
    }


def _ach_local(prob: np.ndarray, is_s: np.ndarray, rec: np.ndarray,
               record_ids, ks) -> np.ndarray:
    """Independent achievement implementation, written plainly on purpose.

    The fixture's ``result.json`` is generated with *this* function while the
    module under test uses its own, so "the report reproduces result.json" is a
    real check rather than a tautology.
    """
    buckets = {rid: ([], []) for rid in record_ids}
    for j in range(prob.size):
        bucket = buckets.get(int(rec[j]))
        if bucket is None or not np.isfinite(prob[j]):
            continue
        bucket[0].append(float(prob[j]))
        bucket[1].append(bool(is_s[j]))

    out = np.full((len(record_ids), len(ks)), np.nan)
    for i, rid in enumerate(record_ids):
        p, y = buckets[rid]
        if not p:
            continue
        n_s = sum(y)
        if n_s == 0:
            continue
        ranked = [yy for _, yy in sorted(zip(p, y), key=lambda t: -t[0])]
        for jj, k in enumerate(ks):
            hits = sum(ranked[: int(k)])
            out[i, jj] = hits / min(int(k), n_s)
    return out


def _bootstrap_ci(delta: np.ndarray, rng: np.random.Generator) -> dict:
    n = delta.size
    draws = np.empty(N_BOOT)
    for b in range(N_BOOT):
        draws[b] = np.mean(delta[rng.integers(0, n, n)])
    return {
        "mean": float(np.mean(delta)),
        "ci_low": float(np.percentile(draws, 2.5)),
        "ci_high": float(np.percentile(draws, 97.5)),
        "n_record": int(n),
        "n_boot": N_BOOT,
    }


def build_fixture_run(out_dir: str) -> dict:
    """Write a small but structurally faithful run bundle."""
    rng = np.random.default_rng(20260806)
    n_record_total = 16
    n_scorable = 12
    per_record = 420

    rec = np.repeat(np.arange(n_record_total), per_record)
    n_beat = rec.size
    scorable = list(range(n_scorable))

    # y3 in {0: N, 1: S, 2: V}; scorable records carry enough S beats.
    y3 = np.zeros(n_beat, dtype=np.int64)
    for r in range(n_record_total):
        idx = np.flatnonzero(rec == r)
        n_s = rng.integers(40, 120) if r in scorable else rng.integers(0, 8)
        n_v = rng.integers(5, 40)
        picked = rng.choice(idx, size=int(n_s + n_v), replace=False)
        y3[picked[: int(n_s)]] = 1
        y3[picked[int(n_s):]] = 2
    is_s = y3 == 1

    scored = np.isin(rec, scorable)

    def make_probs(signal: float, seed_noise: float, base_rng: np.random.Generator) -> np.ndarray:
        """(n_seed, n_beat) S-probabilities; NaN outside the scorable records."""
        shared = base_rng.normal(0, 1, n_beat) + signal * is_s
        out = np.full((len(SEEDS), n_beat), np.nan, dtype=np.float32)
        for s in range(len(SEEDS)):
            z = shared + seed_noise * base_rng.normal(0, 1, n_beat)
            out[s][scored] = (1.0 / (1.0 + np.exp(-z)))[scored].astype(np.float32)
        return out

    base_rng = np.random.default_rng(7)
    a_single = make_probs(2.4, 0.0, base_rng)[0]
    probs = {
        # A is deterministic: identical across seeds, exactly like the real run.
        "A": np.repeat(a_single[None, :], len(SEEDS), axis=0),
        "B": make_probs(0.25, 0.30, base_rng),
        "C": make_probs(2.4, 0.05, np.random.default_rng(11)),
        "D": make_probs(2.4, 0.05, np.random.default_rng(12)),
        "E": make_probs(2.45, 0.05, np.random.default_rng(13)),
        "F": np.repeat(make_probs(2.35, 0.0, np.random.default_rng(14))[0][None, :],
                       len(SEEDS), axis=0),
    }

    # ---- per-record achievement, from the independent implementation above ----
    ach = {}
    for code, p in probs.items():
        arr = np.full((len(SEEDS), len(scorable), len(KS_ALL)), np.nan)
        for s in range(len(SEEDS)):
            arr[s] = _ach_local(p[s].astype(np.float64), is_s, rec, scorable, KS_ALL)
        ach[code] = arr

    sweep_idx = [KS_ALL.index(k) for k in K_SWEEP]
    ksw = {code: np.nanmean(a[:, :, sweep_idx], axis=2) for code, a in ach.items()}

    arms_json = {}
    for spec in q4o.ARMS:
        code = spec.code
        per_seed = []
        for s, seed in enumerate(SEEDS):
            entry = {"seed": int(seed), "ksw": _stats(ksw[code][s], scorable)}
            au, pr = [], []
            for rid in scorable:
                idx = np.flatnonzero(rec == rid)
                p = probs[code][s][idx]
                keep = np.isfinite(p)
                au.append(_auroc(is_s[idx][keep], p[keep].astype(np.float64)))
                pr.append(_average_precision(is_s[idx][keep], p[keep].astype(np.float64)))
            entry["auroc"] = _stats(np.array(au), scorable)
            entry["prauc"] = _stats(np.array(pr), scorable)
            for j, k in enumerate(KS_ALL):
                entry[f"ach@{k}"] = _stats(ach[code][s][:, j], scorable)
            per_seed.append(entry)
        by_seed = [ps["ksw"]["mean"] for ps in per_seed]
        arms_json[spec.key] = {
            "per_seed": per_seed,
            "seed_averaged_ksw": _stats(np.nanmean(ksw[code], axis=0), scorable),
            "ksw_mean_by_seed": by_seed,
            "ksw_seed_std": float(np.std(by_seed)),
        }

    # ---- contrasts, from the seed-averaged per-record vectors ----
    boot_rng = np.random.default_rng(99)
    pairs = [
        ("C_minus_A", "C", "A"), ("C_minus_D", "C", "D"), ("B_minus_A", "B", "A"),
        ("E_minus_A", "E", "A"), ("D_minus_A", "D", "A"), ("E_minus_combBaseline", "E", "F"),
    ]
    contrasts = {}
    for name, lhs, rhs in pairs:
        delta = np.nanmean(ksw[lhs], axis=0) - np.nanmean(ksw[rhs], axis=0)
        by_seed = [float(np.nanmean(ksw[lhs][s]) - np.nanmean(ksw[rhs][s]))
                   for s in range(len(SEEDS))]
        rb = _bootstrap_ci(delta, boot_rng)
        hb = dict(rb)
        hb["n_seed"] = len(SEEDS)
        contrasts[name] = {
            "record_bootstrap": rb,
            "hierarchical_bootstrap": hb,
            "by_seed": by_seed,
            "positive_seed_count": int(sum(v > 0 for v in by_seed)),
        }

    ca = contrasts["C_minus_A"]
    cd = contrasts["C_minus_D"]
    p10_a = arms_json["morph_baseline"]["seed_averaged_ksw"]["p10"]
    p10_c = arms_json["morph_plus_raw_residual"]["seed_averaged_ksw"]["p10"]
    checks = {
        "1_mean_gain_ge_0.015": bool(ca["record_bootstrap"]["mean"] >= MIN_GAIN),
        "2_ci_lower_gt_0": bool(ca["record_bootstrap"]["ci_low"] > 0),
        "3_beats_shuffle_control": bool(cd["record_bootstrap"]["ci_low"] > 0),
        "4_seed_direction_stable": bool(ca["positive_seed_count"] >= 4),
        "5_lower_tail_not_worse": bool(p10_c >= p10_a - 0.01),
        "6_leakage_and_reproducibility": True,
    }
    result = {
        "experiment_id": "EXP-2026-001",
        "arm_id": "Q4-O",
        "timestamp_utc": "20260806T0933",
        "smoke": False,
        "primary_metric": "record_level_k_sweep_achievement_mean",
        "primary_comparison": "C_minus_A",
        "negative_control": "C_minus_D",
        "arms": arms_json,
        "contrasts": contrasts,
        "gates": {
            "checks": checks,
            "verdict": "NO-GO" if not all(checks.values()) else "GO",
            "positive_seed_count": ca["positive_seed_count"],
            "n_seed": len(SEEDS),
            "thresholds": {"min_gain": MIN_GAIN, "min_seed_agreement": 4,
                           "lower_tail_max_drop": 0.01},
            "next_step": "Keep the morphology baseline.",
        },
        "arm_E_diagnostic": {
            "arm_E_seed_averaged_ksw": arms_json["corrected_q4n_diagnostic"]["seed_averaged_ksw"]["mean"],
            "arm_A_seed_averaged_ksw": arms_json["morph_baseline"]["seed_averaged_ksw"]["mean"],
            "comb_baseline_seed_averaged_ksw": arms_json["comb_baseline_diagnostic"]["seed_averaged_ksw"]["mean"],
            "q4n_contaminated_reference": {"cpu_comb": 0.8445, "boost_fix": 0.8631, "boost_rank": 0.8492},
            "residual_effect_isolated": contrasts["E_minus_combBaseline"]["record_bootstrap"],
            "interpretation": "Diagnostic only.",
            "protocol_note": "Different split; read direction, not the difference.",
        },
        "note": "Values are measured from this run only.",
    }

    folds = {str(f): [r for r in scorable if r % 5 == f] for f in range(5)}
    arm_alpha = {}
    alpha_rng = np.random.default_rng(5)
    for key, all_zero in (("morph_plus_raw_residual", True),
                          ("shuffled_waveform_control", False),
                          ("corrected_q4n_diagnostic", False)):
        entries = []
        for seed in SEEDS:
            fold_rows = []
            for f in range(5):
                fold_rows.append({
                    "fold": f,
                    "alpha": float(alpha_rng.normal(0, 0.09)),
                    "best_epoch": 0 if all_zero else int(alpha_rng.integers(0, 3)),
                    "dev_loss": float(abs(alpha_rng.normal(0.3, 0.05))),
                    "n_fit": 1000, "n_dev": 300, "n_test": 200,
                })
            entries.append({"seed": int(seed), "folds": fold_rows})
        arm_alpha[key] = entries

    manifest = {
        "data": {"file_name": "fixture.npz", "sha256": "0" * 64},
        "git_commit_sha": "0" * 40,
        "packages": {"python": "3.12", "numpy": np.__version__},
        "record_equals_patient": True,
        "n_record_total": n_record_total,
        "n_record_scorable": n_scorable,
        "scorable_records": scorable,
        "record_burden": {str(r): float(np.mean(is_s[rec == r])) for r in range(n_record_total)},
        "fold_records": folds,
        "arm_alpha": arm_alpha,
        "morph_port_check": {
            "reference_q4n_morph_ksw_loro": 0.8361,
            "measured_loro_ksw": 0.83608,
            "delta": -1.8e-05, "tolerance": 0.005,
            "within_tolerance": True, "applicable": True,
        },
    }

    config = {
        "experiment_id": "EXP-2026-001", "arm_id": "Q4-O",
        "run_slug": "q4o_leakage_free_residual_cnn", "smoke": False,
        "split": "frozen record-grouped 5-fold CV",
        "n_outer_folds": 5, "n_inner_folds": 5,
        "training_seeds": SEEDS,
        "waveform_permutation": {"seed": 20261797, "moved_fraction": 0.9996},
        "k_sweep": K_SWEEP, "k_operating_points": [30, 50], "main_k": 300,
        "min_s": 25, "min_n": 25, "dev_every": 4, "epochs": 12, "n_boot": N_BOOT,
        "feature_dims": {"base": 9, "morph": 17, "comb": 28},
        "gate_thresholds": {"min_gain": MIN_GAIN, "min_seed_agreement": 4,
                            "lower_tail_max_drop": 0.01},
    }
    fold_map = {
        "n_folds": 5,
        "record_to_fold": {str(r): r % 5 for r in scorable},
        "fold_to_records": folds,
    }

    os.makedirs(out_dir, exist_ok=True)
    for name, payload in (("result.json", result), ("manifest.json", manifest),
                          ("config.json", config), ("fold_map.json", fold_map)):
        with open(os.path.join(out_dir, name), "w", encoding="utf-8") as fh:
            json.dump(payload, fh, indent=2)
    np.savez_compressed(os.path.join(out_dir, "predictions.npz"),
                        y3=y3, rec=rec, scored=scored)
    for spec in q4o.ARMS:
        d = os.path.join(out_dir, "arms", spec.key)
        os.makedirs(d, exist_ok=True)
        np.save(os.path.join(d, "probs.npy"), probs[spec.code])
    os.makedirs(os.path.join(out_dir, "figures"), exist_ok=True)

    return {"result": result, "ksw": ksw, "record_ids": scorable}


# --------------------------------------------------------------------------
# Fixtures
# --------------------------------------------------------------------------

@pytest.fixture(scope="module")
def fixture_run(tmp_path_factory):
    out_dir = str(tmp_path_factory.mktemp("q4o_run"))
    truth = build_fixture_run(out_dir)
    return out_dir, truth


@pytest.fixture(scope="module")
def analysis(fixture_run):
    out_dir, truth = fixture_run
    res = q4o.analyze_existing_run(out_dir, verbose=False)
    return out_dir, truth, res


@pytest.fixture(scope="module")
def real_run_dir():
    path = os.environ.get("MEDKOS_Q4O_RUN_DIR")
    if not path or not os.path.isdir(path):
        pytest.skip("MEDKOS_Q4O_RUN_DIR not set to an existing run directory")
    return path


# --------------------------------------------------------------------------
# 1. the report reproduces result.json
# --------------------------------------------------------------------------

def test_arm_table_reproduces_result_json(analysis):
    _, truth, res = analysis
    bundle = res["bundle"]
    rows = {r["arm"]: r for r in q4o.arm_metrics_rows(bundle)}
    src = truth["result"]["arms"]
    base = src["morph_baseline"]["seed_averaged_ksw"]["mean"]

    assert set(rows) == {s.code for s in q4o.ARMS}
    for spec in q4o.ARMS:
        row = rows[spec.code]
        arm = src[spec.key]
        assert row["ksweep_mean"] == arm["seed_averaged_ksw"]["mean"]
        assert row["p10"] == arm["seed_averaged_ksw"]["p10"]
        assert row["worst"] == arm["seed_averaged_ksw"]["worst"]
        assert row["worst_record"] == arm["seed_averaged_ksw"]["worst_record"]
        assert row["seed_sd"] == arm["ksw_seed_std"]
        assert row["delta_vs_A"] == pytest.approx(arm["seed_averaged_ksw"]["mean"] - base, abs=0)
        # PR-AUC / AUROC are the seed averages of the stored per-seed means.
        assert row["pr_auc"] == pytest.approx(
            float(np.mean([ps["prauc"]["mean"] for ps in arm["per_seed"]])), rel=0, abs=1e-15)
        assert row["auroc"] == pytest.approx(
            float(np.mean([ps["auroc"]["mean"] for ps in arm["per_seed"]])), rel=0, abs=1e-15)


def test_arm_metrics_csv_matches_result_json(analysis):
    import csv as _csv
    out_dir, truth, res = analysis
    path = res["figures"]["arm_metrics.csv"]
    assert path and os.path.isfile(path)
    with open(path, encoding="utf-8") as fh:
        rows = {r["arm"]: r for r in _csv.DictReader(fh)}
    for spec in q4o.ARMS:
        stored = truth["result"]["arms"][spec.key]["seed_averaged_ksw"]["mean"]
        assert float(rows[spec.code]["ksweep_mean"]) == pytest.approx(stored, abs=1e-15)


def test_gate_verdict_is_read_not_recomputed(analysis):
    _, truth, res = analysis
    bundle = res["bundle"]
    assert bundle.verdict == truth["result"]["gates"]["verdict"]
    assert bundle.result["gates"]["checks"] == truth["result"]["gates"]["checks"]


# --------------------------------------------------------------------------
# 2. C−A / C−D values and CIs match the original
# --------------------------------------------------------------------------

@pytest.mark.parametrize("name", ["C_minus_A", "C_minus_D"])
def test_primary_contrast_values_and_ci_match_source(analysis, name):
    _, truth, res = analysis
    bundle = res["bundle"]
    row = next(r for r in q4o.contrast_rows(bundle, q4o.PRIMARY_CONTRASTS + q4o.REFERENCE_CONTRASTS)
               if r["contrast"] == name)
    src = truth["result"]["contrasts"][name]["record_bootstrap"]
    hier = truth["result"]["contrasts"][name]["hierarchical_bootstrap"]

    assert row["mean"] == src["mean"]
    assert row["ci_low"] == src["ci_low"]
    assert row["ci_high"] == src["ci_high"]
    assert row["hier_ci_low"] == hier["ci_low"]
    assert row["hier_ci_high"] == hier["ci_high"]
    assert row["by_seed"] == [pytest.approx(v, abs=0) for v in
                              truth["result"]["contrasts"][name]["by_seed"]]
    assert row["positive_seed_count"] == truth["result"]["contrasts"][name]["positive_seed_count"]


@pytest.mark.parametrize("name", ["C_minus_A", "C_minus_D"])
def test_report_summary_prints_the_source_numbers(analysis, name):
    _, truth, res = analysis
    text = open(res["report_summary"], encoding="utf-8").read()
    src = truth["result"]["contrasts"][name]["record_bootstrap"]
    assert f"{src['mean']:+.4f}" in text
    assert f"[{src['ci_low']:+.4f}, {src['ci_high']:+.4f}]" in text


def test_executive_summary_is_korean_and_states_the_verdict(analysis):
    _, truth, res = analysis
    text = q4o.executive_summary_ko(res["bundle"])
    assert "최종 판정" in text
    assert truth["result"]["gates"]["verdict"] in text
    for heading in ("morphology baseline", "C − A", "C − D",
                    "이 결과가 의미하는 것", "이 결과가 증명하지 않는 것", "권장 다음 행동"):
        assert heading in text
    assert "통과한 gate" in text and "실패한 gate" in text


def test_primary_and_reference_contrasts_never_share_an_axis():
    """The contrasts.png defect: B−A must not sit on the primary axis."""
    primary = {k for k, _ in q4o.PRIMARY_CONTRASTS}
    reference = {k for k, _ in q4o.REFERENCE_CONTRASTS}
    assert "B_minus_A" in reference
    assert "B_minus_A" not in primary
    assert primary.isdisjoint(reference)
    assert primary == {"C_minus_A", "C_minus_D", "E_minus_combBaseline"}


def test_both_split_contrast_figures_exist(analysis):
    _, _, res = analysis
    for name in ("primary_contrasts_zoom.png", "reference_gap_separate.png"):
        assert res["figures"][name] and os.path.isfile(res["figures"][name])


# --------------------------------------------------------------------------
# 3. per-record views use every seed
# --------------------------------------------------------------------------

def test_per_record_uses_all_five_seeds(analysis):
    _, truth, res = analysis
    per_rec = res["per_record"]
    assert per_rec is not None, "per-record recomputation should verify on the fixture"
    for code in ("A", "C", "D"):
        assert per_rec.ksw[code].shape[0] == len(SEEDS) == 5
    # seed_mean really is the mean over all 5 seed rows, not row 0
    got = per_rec.seed_mean("C")
    assert np.allclose(got, np.nanmean(per_rec.ksw["C"], axis=0), atol=0, rtol=0)
    assert not np.allclose(got, per_rec.ksw["C"][0]), "seed-averaging collapsed to one seed"


def test_patient_delta_is_the_five_seed_mean(analysis):
    """The waterfall's record mean must equal the run's C−A point estimate."""
    _, truth, res = analysis
    per_rec = res["per_record"]
    delta = per_rec.seed_mean("C") - per_rec.seed_mean("A")
    expected = truth["result"]["contrasts"]["C_minus_A"]["record_bootstrap"]["mean"]
    assert float(np.mean(delta)) == pytest.approx(expected, abs=1e-12)


def test_patient_delta_csv_shape_and_columns(analysis):
    import csv as _csv
    _, truth, res = analysis
    path = res["figures"]["patient_delta.csv"]
    assert path and os.path.isfile(path)
    with open(path, encoding="utf-8") as fh:
        rows = list(_csv.DictReader(fh))
    assert len(rows) == len(truth["record_ids"])
    for col in ("record", "delta_C_minus_A", "ksw_A", "ksw_C", "s_burden", "n_seed_averaged"):
        assert col in rows[0]
    assert {int(r["n_seed_averaged"]) for r in rows} == {5}
    deltas = [float(r["delta_C_minus_A"]) for r in rows]
    assert deltas == sorted(deltas), "waterfall CSV must be sorted by delta"


def test_per_record_recomputation_reproduces_result_json(analysis):
    _, truth, res = analysis
    per_rec = res["per_record"]
    for code in ("A", "C", "D"):
        stored = truth["result"]["arms"][q4o.ARM_BY_CODE[code].key]["per_seed"]
        for s, ps in enumerate(stored):
            assert float(np.nanmean(per_rec.ksw[code][s])) == pytest.approx(
                ps["ksw"]["mean"], abs=1e-9)
    assert max(per_rec.verification["per_arm_max_abs_diff"].values()) <= 1e-9


def test_per_record_views_are_skipped_when_unverifiable(tmp_path, fixture_run):
    """Corrupt the probabilities: the report must skip, not guess."""
    import shutil
    src, _ = fixture_run
    dst = str(tmp_path / "tampered")
    shutil.copytree(src, dst)
    probs_path = os.path.join(dst, "arms", "morph_baseline", "probs.npy")
    p = np.load(probs_path)
    np.save(probs_path, p[:, ::-1].copy())

    bundle = q4o.load_run(dst)
    definition, diag = q4o.resolve_achievement_definition(bundle)
    assert definition is None
    assert "reason" in diag
    assert q4o.per_record_ksw(bundle) is None


# --------------------------------------------------------------------------
# 4. no fabricated training history
# --------------------------------------------------------------------------

def test_training_history_absent_is_reported_not_invented(analysis):
    out_dir, _, res = analysis
    status = res["history"]
    assert status["present"] is False
    assert status["files"] == []
    for name in q4o.TRAINING_HISTORY_FILES:
        assert not os.path.exists(os.path.join(out_dir, name)), \
            "reporting must never create a training history file"
    assert res["figures"]["learning_curves.png"] is None
    assert not os.path.exists(os.path.join(out_dir, "figures", "learning_curves.png"))


def test_report_says_history_is_missing(analysis):
    _, _, res = analysis
    text = open(res["report_summary"], encoding="utf-8").read()
    assert "epoch별 학습 이력이 없습니다" in text
    assert "생성하지 않았습니다" in text


def test_learning_curves_returns_none_without_history(analysis):
    out_dir, _, _ = analysis
    assert q4o.fig_learning_curves(out_dir, os.path.join(out_dir, "unused.png")) is None
    assert not os.path.exists(os.path.join(out_dir, "unused.png"))


def test_recorder_writes_nothing_when_nothing_logged(tmp_path):
    rec = q4o.TrainingHistoryRecorder(str(tmp_path))
    assert rec.write() is None
    assert not os.path.exists(os.path.join(str(tmp_path), "training_history.json"))


def test_recorder_is_observational_only(tmp_path):
    """log_epoch returns nothing and keeps no state a training loop could read."""
    rec = q4o.TrainingHistoryRecorder(str(tmp_path))
    assert rec.log_epoch(arm="morph_plus_raw_residual", seed=1, fold=0, epoch=0,
                         train_loss=0.5, dev_loss=0.4, dev_prauc=0.6, alpha=0.09) is None
    rec.log_epoch(arm="morph_plus_raw_residual", seed=1, fold=0, epoch=1, train_loss=0.4)
    path = rec.write()
    payload = json.load(open(path, encoding="utf-8"))
    assert payload["rows"][1]["dev_loss"] is None, \
        "an epoch without a dev evaluation must record None, not a carried value"
    assert len(payload["rows"]) == 2


def test_learning_curves_drawn_when_history_exists(tmp_path, fixture_run):
    import shutil
    src, _ = fixture_run
    dst = str(tmp_path / "with_history")
    shutil.copytree(src, dst)
    rec = q4o.TrainingHistoryRecorder(dst)
    for epoch in range(4):
        rec.log_epoch(arm="morph_plus_raw_residual", seed=SEEDS[0], fold=0, epoch=epoch,
                      train_loss=0.5 - 0.02 * epoch,
                      dev_loss=0.4 if epoch % 2 == 0 else None,
                      dev_prauc=0.6 if epoch % 2 == 0 else None,
                      alpha=0.09)
    rec.write()
    assert q4o.training_history_status(dst)["present"] is True
    out = q4o.fig_learning_curves(dst, os.path.join(dst, "figures", "learning_curves.png"))
    assert out and os.path.isfile(out)


# --------------------------------------------------------------------------
# 5. the measured artifacts are untouched
# --------------------------------------------------------------------------

def test_result_json_checksum_unchanged(analysis):
    _, _, res = analysis
    before, after = res["checksums_before"], res["checksums_after"]
    assert "result.json" in before
    assert before["result.json"] == after["result.json"]


def test_every_measured_artifact_checksum_unchanged(analysis):
    _, _, res = analysis
    assert res["checksums_before"] == res["checksums_after"]
    assert res["checksums_unchanged"] is True
    keys = set(res["checksums_after"])
    assert {"result.json", "manifest.json", "config.json", "fold_map.json",
            "predictions.npz"} <= keys
    assert any(k.startswith("arms/") for k in keys)


def test_report_dir_option_leaves_bundle_byte_identical(tmp_path, fixture_run):
    """With --report-dir the run directory itself gains no new file at all."""
    import shutil
    src, _ = fixture_run
    dst = str(tmp_path / "pristine")
    shutil.copytree(src, dst)
    before_tree = sorted(
        os.path.relpath(os.path.join(r, f), dst)
        for r, _, fs in os.walk(dst) for f in fs
    )
    before_sums = q4o.bundle_checksums(dst)

    out = str(tmp_path / "report_out")
    res = q4o.analyze_existing_run(dst, report_dir=out, verbose=False)

    after_tree = sorted(
        os.path.relpath(os.path.join(r, f), dst)
        for r, _, fs in os.walk(dst) for f in fs
    )
    assert before_tree == after_tree
    assert before_sums == q4o.bundle_checksums(dst)
    assert res["checksums_unchanged"] is True
    assert os.path.isfile(os.path.join(out, "report_summary.md"))


def test_load_run_does_not_mutate(fixture_run):
    out_dir, _ = fixture_run
    before = q4o.bundle_checksums(out_dir)
    q4o.load_run(out_dir)
    assert before == q4o.bundle_checksums(out_dir)


# --------------------------------------------------------------------------
# figure inventory
# --------------------------------------------------------------------------

REQUIRED_ARTIFACTS = [
    "arm_summary_table.png", "arm_metrics.csv", "primary_contrasts_zoom.png",
    "reference_gap_separate.png", "achievement_by_k.png", "seed_effects.png",
    "fold_training_diagnostics.png", "patient_delta_waterfall.png",
    "patient_delta.csv", "metric_distribution.png",
]


@pytest.mark.parametrize("name", REQUIRED_ARTIFACTS)
def test_required_artifact_is_produced(analysis, name):
    _, _, res = analysis
    path = res["figures"].get(name)
    assert path, f"{name} was not produced"
    assert os.path.isfile(path) and os.path.getsize(path) > 0


def test_report_summary_covers_every_required_section(analysis):
    _, _, res = analysis
    text = open(res["report_summary"], encoding="utf-8").read()
    for section in ("Executive Summary", "baseline 정의", "Arm 요약",
                    "PASS/FAIL 근거", "구조 설명", "Q4-N 0.8631",
                    "한계와 다음 결정", "생성한 그림", "checksum"):
        assert section in text, f"report_summary.md is missing: {section}"


# --------------------------------------------------------------------------
# the notebook
# --------------------------------------------------------------------------

NOTEBOOK = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "notebooks", "quest47_q4o_leakage_free_residual_cnn.ipynb",
)


@pytest.fixture(scope="module")
def notebook():
    if not os.path.isfile(NOTEBOOK):
        pytest.skip(f"notebook not found: {NOTEBOOK}")
    with open(NOTEBOOK, encoding="utf-8") as fh:
        return json.load(fh)


def test_notebook_cells_compile(notebook):
    for i, cell in enumerate(notebook["cells"]):
        if cell["cell_type"] != "code":
            continue
        compile("".join(cell["source"]), f"cell{i}", "exec")


def test_notebook_declares_analyze_existing_run_mode(notebook):
    src = "".join("".join(c["source"]) for c in notebook["cells"])
    assert "ANALYZE_EXISTING_RUN = True" in src
    assert "OUT_DIR" in src
    assert "20260806T0923_EXP-2026-001_q4o_leakage_free_residual_cnn" in src
    # It must display everything at the end and prove it changed nothing.
    assert "report_summary.md" in src
    assert "bundle_checksums" in src
    assert "interpretation_ko" in src


def test_notebook_has_no_training_code(notebook):
    """A presentation-only revision must not contain a training path."""
    src = "".join("".join(c["source"]) for c in notebook["cells"] if c["cell_type"] == "code")
    for banned in ("torch", ".backward(", "optimizer", "fit(", "train_one_epoch"):
        assert banned not in src, f"notebook must not train: found {banned!r}"


def test_notebook_runs_end_to_end(tmp_path, fixture_run):
    """Execute every code cell against the fixture bundle."""
    import contextlib
    import io
    import shutil

    src_dir, _ = fixture_run
    run_dir = str(tmp_path / "nb_run")
    shutil.copytree(src_dir, run_dir)

    with open(NOTEBOOK, encoding="utf-8") as fh:
        nb = json.load(fh)

    ns = {"__name__": "__main__"}
    buf = io.StringIO()
    for i, cell in enumerate(nb["cells"]):
        if cell["cell_type"] != "code":
            continue
        code = "".join(cell["source"])
        if "ANALYZE_EXISTING_RUN = True" in code:
            code = (
                f'ANALYZE_EXISTING_RUN = True\nOUT_DIR = {run_dir!r}\n'
                f'REPORT_DIR = None\nREPO_DIR = {os.path.dirname(os.path.dirname(NOTEBOOK))!r}\n'
                'MOUNT_DRIVE = False\n'
            )
        with contextlib.redirect_stdout(buf):
            exec(compile(code, f"cell{i}", "exec"), ns)

    assert ns["result"]["checksums_unchanged"] is True
    assert ns["bundle"].verdict == "NO-GO"
    assert ns["HISTORY"]["present"] is False
    out = buf.getvalue()
    assert "최종 판정" in out
    assert "checksum이 실행 전후 동일합니다" in out


def test_notebook_refuses_to_run_with_flag_off(tmp_path, fixture_run):
    """With the flag off the notebook stops loudly instead of half-running."""
    src_dir, _ = fixture_run
    with open(NOTEBOOK, encoding="utf-8") as fh:
        nb = json.load(fh)
    guard = next(
        "".join(c["source"]) for c in nb["cells"]
        if c["cell_type"] == "code" and "if not ANALYZE_EXISTING_RUN" in "".join(c["source"])
    )
    ns = {"ANALYZE_EXISTING_RUN": False, "OUT_DIR": src_dir, "q4o": q4o, "os": os}
    with pytest.raises(SystemExit) as excinfo:
        exec(compile(guard, "guard", "exec"), ns)
    assert "presentation" in str(excinfo.value)


# --------------------------------------------------------------------------
# interpretations must be computed, not hardcoded
# --------------------------------------------------------------------------

INTERPRETED = [
    "arm_summary_table.png", "primary_contrasts_zoom.png", "reference_gap_separate.png",
    "achievement_by_k.png", "seed_effects.png", "fold_training_diagnostics.png",
    "patient_delta_waterfall.png", "metric_distribution.png", "learning_curves.png",
]


@pytest.mark.parametrize("name", INTERPRETED)
def test_interpretation_is_korean_and_non_empty(analysis, name):
    _, _, res = analysis
    text = q4o.interpretation_ko(res["bundle"], name, res["per_record"])
    assert text, f"no interpretation for {name}"
    assert any("가" <= ch <= "힣" for ch in text), "interpretation must be Korean"
    # Count sentence-ending periods only — decimals are full of dots.
    sentences = len(re.findall(r"\.(?:\s|$)", text))
    assert 2 <= sentences <= 4, f"aim for two or three sentences, got {sentences}"


def test_interpretation_tracks_the_data(analysis, tmp_path):
    """Change the source numbers and the sentence must change with them."""
    _, _, res = analysis
    bundle = res["bundle"]
    before = q4o.interpretation_ko(bundle, "primary_contrasts_zoom.png")
    assert f"{bundle.contrast('C_minus_A')['record_bootstrap']['mean']:+.4f}" in before

    import copy
    tampered = copy.deepcopy(bundle)
    tampered.result["contrasts"]["C_minus_A"]["record_bootstrap"]["mean"] = 0.0777
    after = q4o.interpretation_ko(tampered, "primary_contrasts_zoom.png")
    assert "+0.0777" in after and after != before


# --------------------------------------------------------------------------
# optional: the real Drive run
# --------------------------------------------------------------------------

def test_real_run_reproduces_its_own_result_json(real_run_dir):
    bundle = q4o.load_run(real_run_dir)
    rows = {r["arm"]: r for r in q4o.arm_metrics_rows(bundle)}
    for spec in q4o.ARMS:
        if not bundle.has_arm(spec.code):
            continue
        stored = bundle.result["arms"][spec.key]["seed_averaged_ksw"]["mean"]
        assert rows[spec.code]["ksweep_mean"] == stored
    assert bundle.n_seed == 5
    assert bundle.verdict == "NO-GO"


def test_real_run_primary_contrasts_match(real_run_dir):
    bundle = q4o.load_run(real_run_dir)
    rows = {r["contrast"]: r for r in q4o.contrast_rows(bundle, q4o.PRIMARY_CONTRASTS)}
    for name in ("C_minus_A", "C_minus_D"):
        src = bundle.result["contrasts"][name]["record_bootstrap"]
        assert rows[name]["mean"] == src["mean"]
        assert rows[name]["ci_low"] == src["ci_low"]
        assert rows[name]["ci_high"] == src["ci_high"]
        assert len(rows[name]["by_seed"]) == 5


def test_real_run_report_leaves_artifacts_untouched(real_run_dir, tmp_path):
    before = q4o.bundle_checksums(real_run_dir)
    res = q4o.analyze_existing_run(real_run_dir, report_dir=str(tmp_path / "out"), verbose=False)
    assert before == q4o.bundle_checksums(real_run_dir)
    assert res["checksums_unchanged"] is True


def test_real_run_has_no_training_history(real_run_dir):
    status = q4o.training_history_status(real_run_dir)
    assert status["present"] is False
    assert "not synthesised" in status["note"] or "no history" in status["note"].lower()
