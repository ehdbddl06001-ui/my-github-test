#!/usr/bin/env python3
"""Tests for EXP-2026-001 / Q4-O — leakage-free residual CNN.

Spec: ``experiments/specs/EXP-2026-001-q4o-leakage-free-residual-cnn.md``

Coverage required by the spec:
  1. true OOF assignment on synthetic grouped data
  2. the Q4-N overwrite pattern is *detected* by the audit
  3. zero record leakage across folds
  4. every arm's output shape and sample order
  5. the shuffled control actually destroys waveform-label correspondence
  6. the residual branch's gradient is non-zero
  7. artifact schema and required files
  8. a small synthetic CPU smoke run end to end

Run:  python mit-bih/test_q4o_leakage_free_residual.py
"""
from __future__ import annotations

import io
import json
import os
import shutil
import sys
import tempfile

import numpy as np


def _harden_stdout() -> None:
    """Keep the runner alive on consoles that cannot encode non-ASCII output.

    Windows CP949 (and other legacy codepages) raise UnicodeEncodeError on the em
    dashes and box-drawing rules this runner prints. Printing a garbled character is
    acceptable; dying before the first test is not.
    """
    for name in ("stdout", "stderr"):
        stream = getattr(sys, name, None)
        if stream is None:
            continue
        enc = getattr(stream, "encoding", None) or "utf-8"
        try:
            "—─".encode(enc)
            continue                       # this console can print everything we emit
        except (UnicodeEncodeError, LookupError):
            pass
        try:
            stream.reconfigure(errors="replace")
        except (AttributeError, ValueError):
            buf = getattr(stream, "buffer", None)
            if buf is not None:
                setattr(sys, name, io.TextIOWrapper(
                    buf, encoding=enc, errors="replace", line_buffering=True))


_harden_stdout()

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import q4o_leakage_free_residual as Q  # noqa: E402

PASS: list = []
FAIL: list = []


def ok(cond: bool, msg: str) -> bool:
    (PASS if cond else FAIL).append(msg)
    print(("  PASS  " if cond else "  FAIL  ") + msg)
    return bool(cond)


def section(title: str) -> None:
    print("\n" + "-" * 78)
    print(title)
    print("-" * 78)


def _fixture(n_record: int = 10, n_beat: int = 120, seed: int = 3) -> Q.Cohort:
    return Q.synthetic_cohort(n_record=n_record, n_beat=n_beat, seed=seed)


def _folds(cohort: Q.Cohort):
    rec_ok = Q.scorable_records(cohort)
    burden = Q.record_burden(cohort, rec_ok)
    fold_map = Q.make_fold_map(rec_ok, burden)
    return rec_ok, burden, fold_map


# ─────────────────────────────────────────────────────────────────────────────
def test_fold_map_and_record_leakage() -> None:
    section("1. fold map — record-grouped, no leakage between folds")
    cohort = _fixture()
    rec_ok, burden, fold_map = _folds(cohort)

    ok(len(rec_ok) >= Q.N_OUTER_FOLDS,
       f"fixture yields {len(rec_ok)} scorable records (>= {Q.N_OUTER_FOLDS})")
    ok(set(fold_map) == set(rec_ok), "the fold map covers exactly the scorable records")

    leaked = 0
    for f in range(Q.N_OUTER_FOLDS):
        te = {r for r, g in fold_map.items() if g == f}
        tr = {r for r, g in fold_map.items() if g != f}
        leaked += len(te & tr)
    ok(leaked == 0, "record leakage across outer folds == 0")

    # beat-level: no sample appears in both a fold's train and test index sets
    beat_leak = 0
    for f in range(Q.N_OUTER_FOLDS):
        te = set(Q.samples_of(cohort, [r for r, g in fold_map.items() if g == f]).tolist())
        tr = set(Q.samples_of(cohort, [r for r, g in fold_map.items() if g != f]).tolist())
        beat_leak += len(te & tr)
    ok(beat_leak == 0, "beat-level leakage across outer folds == 0")

    counts = [sum(1 for g in fold_map.values() if g == f) for f in range(Q.N_OUTER_FOLDS)]
    ok(min(counts) >= 1, f"every outer fold holds at least one record {counts}")

    # determinism: the same cohort always yields the same map (no RNG involved)
    again = Q.make_fold_map(rec_ok, burden)
    ok(again == fold_map, "the fold map is deterministic across calls")

    # every scorable record appears in exactly one fold's test set
    seen = [sum(1 for r2, g in fold_map.items() if g == fold_map[r] and r2 == r)
            for r in rec_ok]
    ok(all(s == 1 for s in seen), "each record is in exactly one fold's test set")

    # dev split never touches the held-out fold
    dev_leak = 0
    for f in range(Q.N_OUTER_FOLDS):
        tr_recs = [r for r, g in fold_map.items() if g != f]
        te_recs = [r for r, g in fold_map.items() if g == f]
        fit, dv = Q.dev_records(tr_recs, burden)
        dev_leak += len(set(fit) & set(te_recs)) + len(set(dv) & set(te_recs))
        dev_leak += len(set(fit) & set(dv))
    ok(dev_leak == 0,
       "early-stopping dev records come from outer-train only and are disjoint from fit")


def test_true_oof_assignment() -> None:
    section("2. cross-fitted offsets — every OOF sample assigned exactly once")
    cohort = _fixture()
    rec_ok, burden, fold_map = _folds(cohort)
    X = Q.build_base_features(cohort)

    offsets = Q.cross_fitted_offsets(X, cohort, fold_map, burden=burden)
    ok(set(offsets) == set(range(Q.N_OUTER_FOLDS)),
       f"one offset array per outer fold ({len(offsets)})")

    scored = Q.samples_of(cohort, rec_ok)
    all_finite = all(np.all(np.isfinite(offsets[f][scored])) for f in offsets)
    ok(all_finite, "no NaN and no Inf in any cross-fitted offset")

    ok(all(len(offsets[f]) == cohort.n for f in offsets),
       f"each offset array has one entry per sample ({cohort.n})")

    # The strong property: for a given outer fold, no sample was scored by a model
    # that trained on it. Verified by re-deriving the assignment count.
    counts_ok = True
    for f in range(Q.N_OUTER_FOLDS):
        tr_recs = [r for r, g in fold_map.items() if g != f]
        te_recs = [r for r, g in fold_map.items() if g == f]
        inner = Q.make_fold_map(tr_recs, burden, n_folds=min(Q.N_INNER_FOLDS, len(tr_recs)))
        assign = np.zeros(cohort.n, int)
        for g in sorted(set(inner.values())):
            iv = Q.samples_of(cohort, [r for r in tr_recs if inner[r] == g])
            assign[iv] += 1
        assign[Q.samples_of(cohort, te_recs)] += 1
        scored_f = Q.samples_of(cohort, rec_ok)
        counts_ok &= bool(np.all(assign[scored_f] == 1))
    ok(counts_ok, "per outer fold, every scored sample has an OOF assignment count == 1")

    # An inner-validation sample's offset must differ from an in-sample refit, or the
    # cross-fit did nothing.
    f = 0
    tr_recs = [r for r, g in fold_map.items() if g != f]
    inner = Q.make_fold_map(tr_recs, burden, n_folds=min(Q.N_INNER_FOLDS, len(tr_recs)))
    iv = Q.samples_of(cohort, [r for r in tr_recs if inner[r] == 0])
    tr_all = Q.samples_of(cohort, tr_recs)
    in_sample = Q._fit_logit(X[tr_all], cohort.y[tr_all])(X[iv])
    ok(not np.allclose(offsets[f][iv], in_sample, atol=1e-6),
       "cross-fitted offsets differ from an in-sample refit (the cross-fit is real)")


def test_unscorable_records_present() -> None:
    section("2b. cohorts that contain unscorable records (SVDB has 22 of 78)")
    # Regression: the OOF audit and the finiteness checks originally ran over the whole
    # cohort, so on real SVDB they fired on the 45,499 beats belonging to records that
    # fail MIN_S/MIN_N — beats that are legitimately never scored. The all-scorable
    # fixture could not catch it.
    cohort = Q.synthetic_cohort(n_record=10, n_beat=120, seed=3, n_unscorable=4)
    rec_ok = Q.scorable_records(cohort)
    ok(len(rec_ok) == 10 and len(cohort.records) == 14,
       f"fixture has {len(cohort.records)} records, {len(rec_ok)} scorable "
       f"— {len(cohort.records) - len(rec_ok)} fall below MIN_S/MIN_N")

    burden = Q.record_burden(cohort, rec_ok)
    fold_map = Q.make_fold_map(rec_ok, burden)
    scored = Q.samples_of(cohort, rec_ok)
    unscored = np.setdiff1d(np.arange(cohort.n), scored)
    ok(len(unscored) > 0 and len(scored) + len(unscored) == cohort.n,
       f"{len(scored)} scored beats and {len(unscored)} unscored beats "
       f"partition the cohort")
    ok(set(fold_map) == set(rec_ok),
       "the fold map covers the scorable records only — unscorable ones are absent")

    X = Q.build_base_features(cohort)

    offsets = Q.cross_fitted_offsets(X, cohort, fold_map, burden=burden)
    ok(all(np.all(np.isfinite(offsets[f][scored])) for f in offsets),
       "cross_fitted_offsets completes and is finite on every scored beat")
    ok(all(np.all(np.isnan(offsets[f][unscored])) for f in offsets),
       "unscored beats stay NaN — they are not silently given an offset")

    a = Q.run_logistic_arm(X, cohort, fold_map)
    ok(np.all(np.isfinite(a[scored])) and np.all(np.isnan(a[unscored])),
       "Arm A scores every scored beat and leaves the rest NaN")

    pr = Q.per_record_metrics(a, cohort, rec_ok)
    ok(len(pr["ksw"]) == len(rec_ok),
       f"metrics are computed over the {len(rec_ok)} scorable records only")

    # The audit must still reject a genuine double-assignment.
    raised = ""
    try:
        Q.cross_fitted_offsets(X, cohort, {**fold_map, rec_ok[0]: 0, rec_ok[1]: 0,
                                           rec_ok[2]: 0, rec_ok[3]: 0, rec_ok[4]: 0,
                                           rec_ok[5]: 0, rec_ok[6]: 0, rec_ok[7]: 0,
                                           rec_ok[8]: 0, rec_ok[9]: 0},
                               burden=burden)
    except Q.Q4OError as exc:
        raised = str(exc)
    ok(raised != "", f"a degenerate fold map is still rejected ({raised[:60]}…)")


def test_self_check_and_version() -> None:
    section("2c. module version stamp and in-process self-check")
    ok(isinstance(Q.MODULE_VERSION, int) and Q.MODULE_VERSION >= 3,
       f"the module carries a version stamp ({Q.MODULE_VERSION}: {Q.MODULE_BUILD})")

    res = Q.self_check()
    ok(res["ok"] is True and res["module_version"] == Q.MODULE_VERSION,
       "self_check() completes in-process and reports the loaded version")
    ok(res["n_scorable"] < res["n_record"] and res["n_unscored_beats"] > 0,
       f"self_check exercises the path that used to fail — {res['n_scorable']} of "
       f"{res['n_record']} records scorable, {res['n_unscored_beats']} beats unscored")
    ok(os.path.abspath(Q.__file__) == res["module_file"],
       "self_check reports the file the loaded module actually came from")

    raised = ""
    try:
        Q.self_check(min_version=Q.MODULE_VERSION + 1)
    except Q.Q4OError as exc:
        raised = str(exc)
    ok("stale" in raised.lower(),
       "a too-old module is rejected with a message naming the stale-import cause")


def test_detects_q4n_overwrite() -> None:
    section("3. regression — the Q4-N cpu_fold overwrite is detected")
    cohort = _fixture()
    rec_ok, burden, fold_map = _folds(cohort)
    X = Q.build_base_features(cohort)

    leaky, assign = Q.leaky_overwrite_offsets(X, cohort, fold_map)
    scored = Q.samples_of(cohort, rec_ok)

    ok(int(assign[scored].max()) > 1,
       f"the Q4-N pattern assigns some samples up to {int(assign[scored].max())} times "
       f"(a correct OOF audit requires exactly 1)")
    ok(not np.all(assign[scored] == 1),
       "the OOF assignment-count assertion REJECTS the Q4-N cpu_fold pattern")

    # Quantify the contamination: with 5 folds, the last fold's train records (~80% of
    # samples) end up holding in-sample predictions.
    last_f = Q.N_OUTER_FOLDS - 1
    tr_recs = [r for r, g in fold_map.items() if g != last_f]
    tr = Q.samples_of(cohort, tr_recs)
    in_sample = Q._fit_logit(X[tr], cohort.y[tr])(X[tr])
    frac_in_sample = float(np.mean(np.isclose(leaky[tr], in_sample, atol=1e-8)))
    ok(frac_in_sample > 0.99,
       f"after the last fold, {frac_in_sample:.1%} of the train positions hold "
       f"in-sample predictions")
    contaminated = len(tr) / len(scored)
    ok(contaminated > 0.5,
       f"that is {contaminated:.0%} of all scored samples — this is why cpu_comb=0.8445, "
       f"boost_fix=0.8631, and boost_rank=0.8492 are excluded from the baseline")

    # And the clean implementation does not exhibit it.
    clean = Q.cross_fitted_offsets(X, cohort, fold_map, burden=burden)
    frac_clean = float(np.mean(np.isclose(clean[last_f][tr], in_sample, atol=1e-8)))
    ok(frac_clean < 0.01,
       f"the Q4-O cross-fitted offset holds {frac_clean:.1%} in-sample predictions")

    # In-sample scores are optimistically biased — show it on the metric itself.
    ksw_leaky = Q.summarise(Q.per_record_metrics(leaky, cohort, rec_ok)["ksw"])["mean"]
    ksw_clean = Q.summarise(Q.per_record_metrics(clean[last_f], cohort, rec_ok)["ksw"])["mean"]
    ok(np.isfinite(ksw_leaky) and np.isfinite(ksw_clean),
       f"contaminated k-sweep {ksw_leaky:.4f} vs cross-fitted {ksw_clean:.4f} "
       f"(direction is data-dependent; the point is that they are different quantities)")


def test_scaler_and_label_scope() -> None:
    section("4. scalers and labels never cross into the test fold")
    cohort = _fixture()
    rec_ok, burden, fold_map = _folds(cohort)
    X = Q.build_base_features(cohort)

    # Corrupt ONE record inside fold 0's test set. The other records in that same fold
    # are scored by the fold-0 model, which is fit only on folds 1..4 — so if the
    # corrupted record had leaked into that fit or its scaler, their scores would move.
    # (Records in other folds legitimately change: fold 0's test records are training
    # data there, so they are excluded from this check by construction.)
    f = 0
    te_recs = sorted(r for r, g in fold_map.items() if g == f)
    ok(len(te_recs) >= 2, f"fold 0 holds {len(te_recs)} test records (need >= 2)")
    victim = te_recs[0]
    victim_idx = cohort.idx_of[int(victim)]
    siblings = Q.samples_of(cohort, te_recs[1:])

    base_scores = Q.run_logistic_arm(X, cohort, fold_map)
    Xp = X.copy()
    rng = np.random.RandomState(11)
    Xp[victim_idx] += 25.0 * rng.randn(len(victim_idx), X.shape[1])
    pert_scores = Q.run_logistic_arm(Xp, cohort, fold_map)

    ok(np.allclose(base_scores[siblings], pert_scores[siblings], atol=1e-8),
       f"corrupting record {victim} does not move the other fold-0 test records "
       f"(it never reached fold 0's scaler or fit)")
    ok(not np.allclose(base_scores[victim_idx], pert_scores[victim_idx], atol=1e-6),
       "the corrupted record's own scores do move (the perturbation was real)")

    # Same property for the cross-fitted offsets: fold 0's outer-test offsets come
    # from a model fit on folds 1..4 only.
    base_off = Q.cross_fitted_offsets(X, cohort, fold_map, burden=burden)
    pert_off = Q.cross_fitted_offsets(Xp, cohort, fold_map, burden=burden)
    ok(np.allclose(base_off[f][siblings], pert_off[f][siblings], atol=1e-8),
       "the same holds for the cross-fitted outer-test offsets")

    # Flipping fold 0's test labels must not change fold 0's predictions at all —
    # those labels never reach the fit, the scaler, or any threshold.
    te_all = Q.samples_of(cohort, te_recs)
    yflip = cohort.y.copy()
    yflip[te_all] = ~yflip[te_all]
    flipped = Q.Cohort(**{**cohort.__dict__, "y": yflip})
    flip_scores = Q.run_logistic_arm(X, flipped, fold_map)
    ok(np.allclose(base_scores[te_all], flip_scores[te_all], atol=1e-8),
       "flipping fold 0's test labels does not change fold 0's predictions "
       "(test labels never reach the fit)")
    ok(np.allclose(base_off[f][te_all],
                   Q.cross_fitted_offsets(X, flipped, fold_map,
                                          burden=burden)[f][te_all], atol=1e-8),
       "and it does not change fold 0's cross-fitted outer-test offsets either")

    # And the leakage assertions themselves fire.
    raised = False
    try:
        Q.assert_disjoint([1, 2, 3], [3, 4], "unit test")
    except Q.Q4OError:
        raised = True
    ok(raised, "assert_disjoint raises on an overlapping record set")

    raised = False
    try:
        Q.assert_finite(np.array([1.0, np.nan]), "unit test")
    except Q.Q4OError:
        raised = True
    ok(raised, "assert_finite raises on NaN")

    raised = False
    try:
        Q.assert_full_coverage(np.zeros((2, 5)), 7, "unit test")
    except Q.Q4OError:
        raised = True
    ok(raised, "assert_full_coverage raises when the prediction count is wrong")


def test_arm_inputs_and_shapes() -> None:
    section("5. arm inputs — shape, order, and what each arm is allowed to see")
    cohort = _fixture()

    xb = Q.current_beat_input(cohort)
    ok(xb.shape == (cohort.n, cohort.n_lead, cohort.width),
       f"Arms B/C/D input is the current beat only {xb.shape}")
    ok(xb.shape[1] == cohort.n_lead,
       f"Arms B/C/D see exactly {cohort.n_lead} channels — no RR, no prev/next beat, "
       f"no morphology, no P-vector")
    ok(np.array_equal(xb, cohort.beat.astype('float32')),
       "Arms B/C/D input preserves the sample order of the cohort")

    xe = Q.three_beat_input(cohort)
    ok(xe.shape == (cohort.n, 3 * cohort.n_lead + 2, cohort.width),
       f"Arm E keeps Q4-N's 3-beat + 2 RR channel layout {xe.shape}")
    ok(np.allclose(xe[:, cohort.n_lead:2 * cohort.n_lead, :], cohort.beat, atol=1e-6),
       "Arm E's middle channel block is the current beat, in order")

    # The prev/next index construction must not cross a record boundary.
    crossed = 0
    for r in cohort.records:
        ii = cohort.idx_of[int(r)]
        prev = np.r_[ii[0], ii[:-1]]
        nxt = np.r_[ii[1:], ii[-1]]
        crossed += int((cohort.rid[prev] != r).sum() + (cohort.rid[nxt] != r).sum())
    ok(crossed == 0, "Arm E's prev/next beats never cross a record boundary")

    feats = Q.build_features(cohort, with_comb=True)
    ok(feats.dims["base"] == 9, f"F_BASE has 9 RR columns (got {feats.dims['base']})")
    ok(feats.dims["morph"] == 17,
       f"Arm A features = F_BASE 9 + MORPH 8 = 17 (got {feats.dims['morph']})")
    ok(feats.dims["comb"] == 28,
       f"Arm E offset features = 17 + VEC 6 + PONT2 5 = 28 (got {feats.dims['comb']})")
    ok(feats.morph.shape[0] == cohort.n and feats.comb.shape[0] == cohort.n,
       "feature matrices have one row per sample, in cohort order")
    ok(np.all(np.isfinite(feats.morph)) and np.all(np.isfinite(feats.comb)),
       "no NaN and no Inf in the frozen feature matrices")


def test_shuffled_control() -> None:
    section("6. Arm D — the shuffle destroys waveform-label correspondence")
    cohort = _fixture()
    shuffled, rule = Q.shuffle_waveforms_within_record(cohort)

    ok(shuffled.shape == cohort.beat.shape, "the control keeps the waveform tensor shape")
    ok(rule["moved_fraction"] > 0.5,
       f"{rule['moved_fraction']:.1%} of beats moved (the control is not near-identity)")
    ok(rule["seed"] == Q.PERM_SEED and Q.PERM_SEED not in Q.TRAIN_SEEDS,
       f"the permutation seed {Q.PERM_SEED} is recorded and is not a model seed")

    # The record's signal distribution is preserved exactly: same multiset of rows.
    preserved = True
    for r in cohort.records:
        ii = cohort.idx_of[int(r)]
        a = np.sort(cohort.beat[ii].reshape(len(ii), -1).sum(1))
        b = np.sort(shuffled[ii].reshape(len(ii), -1).sum(1))
        preserved &= bool(np.allclose(a, b, atol=1e-4))
    ok(preserved, "every record's set of waveforms is preserved (it is a permutation)")

    # Beats never move between records.
    moved_record = 0
    for r in cohort.records:
        ii = cohort.idx_of[int(r)]
        rows = {tuple(np.round(v, 5)) for v in cohort.beat[ii].reshape(len(ii), -1)[:, :4]}
        for v in shuffled[ii].reshape(len(ii), -1)[:, :4]:
            if tuple(np.round(v, 5)) not in rows:
                moved_record += 1
    ok(moved_record == 0, "no beat crosses a record boundary")

    # The label-conditional waveform difference must collapse. In the fixture, S beats
    # carry an inverted P wave, so the original separation is large.
    def p_gap(B: np.ndarray) -> float:
        gaps = []
        for r in cohort.records:
            ii = cohort.idx_of[int(r)]
            y = cohort.y[ii]
            if y.sum() < 2 or (~y).sum() < 2:
                continue
            seg = B[ii][:, :, 30:70].mean(axis=(1, 2))
            gaps.append(abs(float(seg[y].mean() - seg[~y].mean())))
        return float(np.mean(gaps))

    g0, g1 = p_gap(cohort.beat), p_gap(shuffled)
    ok(g1 < 0.25 * g0,
       f"the label-conditional P-window gap collapses {g0:.4f} -> {g1:.4f} "
       f"({g1 / max(g0, 1e-12):.1%} of the original)")

    # Determinism.
    again, _ = Q.shuffle_waveforms_within_record(cohort)
    ok(np.array_equal(shuffled, again), "the permutation is reproducible from its seed")

    # A different seed gives a different permutation.
    other, _ = Q.shuffle_waveforms_within_record(cohort, perm_seed=Q.PERM_SEED + 1)
    ok(not np.array_equal(shuffled, other), "a different permutation seed changes it")


def test_residual_gradient_alive() -> None:
    section("7. residual branch — gradient is alive, and the deadlock reproduces")
    try:
        import torch  # noqa: F401
    except Exception as exc:
        ok(False, f"torch unavailable, cannot test the residual gradient: {exc}")
        return

    # Step 0: alpha starts at exactly 0, so dL/dh_w = dL/dlogit * alpha * z is zero by
    # construction. What must be non-zero is dL/dalpha = dL/dlogit * h(z) — that is the
    # gradient the Q4-N deadlock killed.
    good0 = Q.residual_grad_is_alive(n_channel=2, init="normal")
    ok(good0["alpha_grad"] > 0.0,
       f"alpha receives a non-zero gradient at step 0 ({good0['alpha_grad']:.3e}) — "
       f"the deadlock is broken")
    ok(good0["head_weight_grad"] == 0.0,
       "the head's step-0 gradient is 0 because alpha starts at 0 by design "
       "(initial output equality with the offset, not the bug)")

    # After alpha leaves zero, the residual branch itself starts learning.
    good = Q.residual_grad_is_alive(n_channel=2, init="normal", warmup_steps=3)
    ok(good["alpha"] > 0.0,
       f"alpha leaves zero within 3 steps (|alpha| = {good['alpha']:.4e})")
    ok(good["head_weight_grad"] > 0.0,
       f"the residual head then receives a non-zero gradient "
       f"({good['head_weight_grad']:.3e}) — the branch is genuinely training")
    ok(good["embed_weight_grad"] > 0.0,
       f"so does the embedding trunk ({good['embed_weight_grad']:.3e})")

    dead = Q.residual_grad_is_alive(n_channel=2, init="zeros")
    ok(dead["alpha_grad"] == 0.0 and dead["head_weight_grad"] == 0.0,
       "zero-initialising both alpha and the head reproduces the Q4-N deadlock "
       "(both gradients exactly 0) — which is why Q4-O never does that")
    dead_warm = Q.residual_grad_is_alive(n_channel=2, init="zeros", warmup_steps=25)
    ok(dead_warm["alpha"] == 0.0 and dead_warm["alpha_grad"] == 0.0,
       "and the deadlocked variant is still frozen at alpha = 0 after 25 steps")

    # alpha starts at exactly 0, so the model's INITIAL OUTPUT equals the offset.
    # (An initialisation property only — nothing about the trained model follows.)
    net = Q.build_residual_net(2, init="normal")
    ok(float(net.alpha.detach().abs().sum()) == 0.0,
       "alpha is initialised to exactly 0 (the arm starts at the morphology baseline)")

    import torch as _t
    x = _t.randn(8, 2, 64)
    off = _t.randn(8)
    with _t.no_grad():
        ok(bool(_t.allclose(net(x, off), off, atol=1e-6)),
           "at initialisation the arm's logit equals the offset exactly")

    # And a few optimiser steps actually move alpha off zero.
    import torch.nn as nn
    opt = _t.optim.Adam(net.parameters(), 1e-2)
    y = (_t.rand(8) > 0.5).float()
    for _ in range(20):
        opt.zero_grad()
        nn.BCEWithLogitsLoss()(net(x, off), y).backward()
        opt.step()
    ok(float(net.alpha.detach().abs().sum()) > 0.0,
       f"alpha moves off zero under training ({float(net.alpha.detach()):+.4f})")


def test_residual_learning_path() -> None:
    section("7b. residual arm end to end — it learns when there IS residual signal")
    try:
        import torch  # noqa: F401
    except Exception as exc:
        ok(False, f"torch unavailable: {exc}")
        return
    from sklearn.metrics import roc_auc_score

    # On the fixture the label information sits in features the morphology offset
    # already captures, so Arm C correctly reverts to the baseline (alpha ~ 0). That is
    # the right behaviour but it leaves the learning path itself unexercised. Here the
    # offset is deliberately uninformative (all zeros), so anything the arm achieves
    # has to come through alpha * residual.
    # A strong waveform signal, so the test measures whether the path *can* learn
    # rather than whether a tiny CNN can beat the noise on six training records.
    cohort = Q.synthetic_cohort(n_record=8, n_beat=150, seed=23, signal=6.0)
    rec_ok, burden, fold_map = _folds(cohort)
    X = Q.current_beat_input(cohort)
    offset = np.zeros(cohort.n, dtype=float)

    f = 0
    te_recs = [r for r, g in fold_map.items() if g == f]
    tr_recs = [r for r, g in fold_map.items() if g != f]
    fit_recs, dv_recs = Q.dev_records(tr_recs, burden)
    fit_idx = Q.samples_of(cohort, fit_recs)
    dev_idx = Q.samples_of(cohort, dv_recs)
    te_idx = Q.samples_of(cohort, te_recs)

    Q.set_determinism(Q.SEED0)
    net = Q.build_residual_net(X.shape[1], init="normal")
    scores, alpha, best_ep, dev_loss, hist = Q._train_one_fold(
        net, X, offset, cohort.y, fit_idx, dev_idx, te_idx,
        Q.SEED0, "cpu", epochs=14, batch=256)
    ok(len(hist) >= 1 and {"epoch", "train_loss", "dev_loss"} <= set(hist[0]),
       f"the fold returns a per-epoch training history ({len(hist)} epochs)")

    ok(abs(alpha) > 0.01,
       f"alpha grows away from 0 when the residual has something to add "
       f"(alpha = {alpha:+.4f})")
    auc = float(roc_auc_score(cohort.y[te_idx].astype(int), scores))
    ok(auc > 0.65,
       f"the trained residual arm separates held-out records (AUROC {auc:.3f}) "
       f"— offset + alpha*residual trains and predicts end to end")
    ok(np.all(np.isfinite(scores)) and len(scores) == len(te_idx),
       f"it returns one finite score per held-out sample ({len(scores)})")
    ok(best_ep >= 0 and dev_loss < float("inf"),
       f"early stopping selected epoch {best_ep} on outer-train dev records "
       f"(dev loss {dev_loss:.4f})")

    # The same run with a zero-initialised head must stay pinned at the offset.
    Q.set_determinism(Q.SEED0)
    dead_net = Q.build_residual_net(X.shape[1], init="zeros")
    dead_scores, dead_alpha, _, _, _ = Q._train_one_fold(
        dead_net, X, offset, cohort.y, fit_idx, dev_idx, te_idx,
        Q.SEED0, "cpu", epochs=14, batch=256)
    ok(dead_alpha == 0.0 and np.allclose(dead_scores, offset[te_idx]),
       "the Q4-N deadlocked initialisation stays pinned at the offset forever "
       "(alpha exactly 0, scores identical to the offset)")

    # The fit-split normalisation is computed in chunks so Arm E's 8-channel input does
    # not materialise a ~1.4 GB temporary on the real cohort. It must be exact.
    rng = np.random.RandomState(0)
    Xn = (rng.randn(3000, 8, 30) * 3 + 1.5).astype("float32")
    idx = rng.choice(3000, 2111, replace=False)
    m, s = Q._chunked_mean_std(Xn, idx, chunk=311)
    exact_m = float(Xn[idx].astype(np.float64).mean())
    exact_s = float(Xn[idx].astype(np.float64).std()) + 1e-9
    ok(abs(m - exact_m) < 1e-9 and abs(s - exact_s) < 1e-9,
       "chunked fit-split normalisation matches the exact float64 mean/std")
    m2, s2 = Q._chunked_mean_std(Xn, idx, chunk=100000)
    ok(abs(m2 - m) < 1e-12 and abs(s2 - s) < 1e-12,
       "and it does not depend on the chunk size")

    ok(Q.DL_MIN_EPOCH >= 1 and Q.DL_PATIENCE >= 1,
       f"early stopping has a warmup of {Q.DL_MIN_EPOCH} epochs before patience "
       f"{Q.DL_PATIENCE} can fire, so alpha gets room to leave zero")


def test_metrics_and_statistics() -> None:
    section("8. metrics and statistics")
    cohort = _fixture()
    rec_ok, _, _ = _folds(cohort)

    # Achievement identity, preserved from Q4-N.
    ii = cohort.idx_of[int(rec_ok[0])]
    y = cohort.y
    perfect = np.where(y, 10.0, -10.0)
    ok(abs(Q.achievement_at(perfect, ii, y, 300) - 1.0) < 1e-12,
       "a perfect ranking achieves 1.0")
    worst = -perfect
    ok(Q.achievement_at(worst, ii, y, 30) < 0.05,
       "an inverted ranking achieves ~0 at k=30")

    ok(Q.K_SWEEP == (50, 100, 200, 300),
       f"the primary k-sweep is unchanged from Q4-N {Q.K_SWEEP}")
    ok(Q.K_OP == (30, 50), f"secondary operating points are k=30 and k=50 {Q.K_OP}")

    pr = Q.per_record_metrics(perfect, cohort, rec_ok)
    ok(set(pr) >= {"ksw", "auroc", "prauc", "ach@30", "ach@50"},
       "per-record metrics include ksw, AUROC, PR-AUC, and both operating points")
    ok(len(pr["ksw"]) == len(rec_ok),
       f"one primary value per scorable record ({len(pr['ksw'])})")

    s = Q.summarise(pr["ksw"])
    ok({"mean", "std", "p10", "worst", "worst_record"} <= set(s),
       "the summary carries mean, std, lower-tail p10, worst value, and worst record")

    # Bootstrap behaviour.
    diff = {r: 0.02 for r in rec_ok}
    b = Q.paired_record_bootstrap(diff, n_boot=300)
    ok(abs(b["mean"] - 0.02) < 1e-9 and b["ci_low"] > 0,
       "a uniformly positive difference gives a CI strictly above 0")

    rng = np.random.RandomState(5)
    noise = {r: float(rng.randn() * 0.05) for r in rec_ok}
    bn = Q.paired_record_bootstrap(noise, n_boot=800)
    ok(bn["ci_low"] < bn["mean"] < bn["ci_high"], "the CI brackets the point estimate")

    hier = Q.hierarchical_bootstrap({r: {0: 0.02, 1: 0.02} for r in rec_ok}, n_boot=300)
    ok(abs(hier["mean"] - 0.02) < 1e-9 and hier["n_seed"] == 2,
       "the hierarchical bootstrap resamples records and seeds")


def test_gates() -> None:
    section("9. pre-registered gates")
    strong = {"mean": 0.02, "ci_low": 0.006, "ci_high": 0.034}
    ctrl = {"mean": 0.018, "ci_low": 0.004, "ci_high": 0.032}
    g = Q.evaluate_gates(strong, ctrl, [0.02, 0.03, 0.01, 0.02, -0.001], 0.51, 0.52, True)
    ok(g["verdict"] == "PASS", "all six criteria met -> PASS")
    ok(g["positive_seed_count"] == 4, "4 of 5 seeds positive is enough")

    g = Q.evaluate_gates({"mean": 0.010, "ci_low": 0.002, "ci_high": 0.02}, ctrl,
                         [0.01] * 5, 0.51, 0.52, True)
    ok(g["verdict"] == "NO-GO" and not g["checks"]["1_mean_gain_ge_0.015"],
       "a mean gain below +0.015 -> NO-GO")

    g = Q.evaluate_gates({"mean": 0.02, "ci_low": -0.001, "ci_high": 0.05}, ctrl,
                         [0.02] * 5, 0.51, 0.52, True)
    ok(g["verdict"] == "NO-GO" and not g["checks"]["2_ci_lower_gt_0"],
       "a CI containing 0 -> NO-GO")

    g = Q.evaluate_gates(strong, {"mean": 0.004, "ci_low": -0.01, "ci_high": 0.02},
                         [0.02] * 5, 0.51, 0.52, True)
    ok(g["verdict"] == "NO-GO" and not g["checks"]["3_beats_shuffle_control"],
       "failing to beat the waveform-shuffle control -> NO-GO")

    g = Q.evaluate_gates(strong, ctrl, [0.02, 0.03, -0.01, -0.02, 0.01], 0.51, 0.52, True)
    ok(g["verdict"] == "NO-GO" and not g["checks"]["4_seed_direction_stable"],
       "an unstable seed direction -> NO-GO")

    g = Q.evaluate_gates(strong, ctrl, [0.02] * 5, 0.51, 0.49, True)
    ok(g["verdict"] == "NO-GO" and not g["checks"]["5_lower_tail_not_worse"],
       "a lower tail worse by more than 0.01 -> NO-GO")

    g = Q.evaluate_gates(strong, ctrl, [0.02] * 5, 0.51, 0.52, False)
    ok(g["verdict"] == "NO-GO" and not g["checks"]["6_leakage_and_reproducibility"],
       "a failed leakage assertion -> NO-GO")

    ok("Transformer" in g["next_step"] and "NOT" in g["next_step"].upper(),
       "the NO-GO next step explicitly forbids a Transformer or a larger fusion model")


def test_data_guard() -> None:
    section("10. data guard — svdb_data.npz cannot stand in for svdb_data5.npz")
    tmp = tempfile.mkdtemp(prefix="q4o_data_")
    try:
        wrong = os.path.join(tmp, "svdb_data.npz")
        np.savez(wrong, beat=np.zeros((4, 2, 300), "float32"),
                 y=np.zeros(4, int), pid=np.zeros(4, int),
                 pre_rr=np.ones(4), post_rr=np.ones(4))
        raised = ""
        try:
            Q.load_cohort(wrong)
        except Q.Q4OError as exc:
            raised = str(exc)
        ok("y3" in raised and "svdb_data5" in raised,
           "a file without y3/sym is rejected with a message naming svdb_data5.npz")

        missing = ""
        try:
            Q.load_cohort(os.path.join(tmp, "nope.npz"))
        except Q.Q4OError as exc:
            missing = str(exc)
        ok("not found" in missing, "a missing data file is a hard error, not a fallback")

        probe = os.path.join(tmp, "probe.bin")
        with open(probe, "wb") as fh:
            fh.write(b"medkos")
        ok(len(Q.sha256_file(probe)) == 64, "sha256_file returns a 64-hex digest")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_artifact_schema() -> None:
    section("11. artifact schema — required files and probs alignment")
    tmp = tempfile.mkdtemp(prefix="q4o_bundle_")
    try:
        n, n_seed = 40, 3
        fold_map = {r: r % Q.N_OUTER_FOLDS for r in range(10)}
        arm_probs = {a: np.random.rand(n_seed, n).astype("float32") for a in Q.ARMS}
        preds = {
            "sample_id": np.arange(n, dtype=np.int64),
            "record_id": np.repeat(np.arange(10), 4).astype(np.int64),
            "y_true": (np.arange(n) % 3 == 0).astype(np.int8),
            "fold": np.repeat(np.arange(10) % Q.N_OUTER_FOLDS, 4).astype(np.int16),
            "seeds": np.array(Q.TRAIN_SEEDS[:n_seed], np.int64),
        }
        out = Q.write_bundle(tmp, {"c": 1}, {"m": 2}, {"r": 3}, fold_map,
                             arm_probs, preds, "log\n",
                             figures={"arm_means": {a: 0.5 for a in Q.ARMS},
                                      "contrasts": {"C_minus_A": {
                                          "mean": 0.02, "ci_low": 0.01,
                                          "ci_high": 0.03}}})
        for name in Q.REQUIRED_BUNDLE_FILES:
            ok(os.path.exists(os.path.join(out, name)), f"bundle contains {name}")
        ok(os.path.isdir(os.path.join(out, "figures")), "bundle contains figures/")
        for arm in Q.ARMS:
            ok(os.path.exists(os.path.join(out, "arms", arm, "probs.npy")),
               f"bundle contains arms/{arm}/probs.npy")

        fm = json.load(open(os.path.join(out, "fold_map.json")))
        ok("record_to_fold" in fm and "fold_to_records" in fm,
           "fold_map.json records both directions of the mapping")

        pred = np.load(os.path.join(out, "predictions.npz"))
        ok({"sample_id", "record_id", "y_true", "fold", "seeds"} <= set(pred.files),
           "predictions.npz carries sample_id, record_id, y_true, fold, and seeds")
        ok(all(np.load(os.path.join(out, "arms", a, "probs.npy")).shape
               == (n_seed, n) for a in Q.ARMS),
           f"every probs.npy is (n_seed, n_sample) = ({n_seed}, {n})")

        # verify_bundle must reject a broken bundle.
        np.save(os.path.join(out, "arms", Q.ARM_C, "probs.npy"),
                np.random.rand(n_seed, n + 1))
        raised = False
        try:
            Q.verify_bundle(out)
        except Q.Q4OError:
            raised = True
        ok(raised, "verify_bundle rejects a probs.npy whose length disagrees with "
                   "predictions.npz")

        os.remove(os.path.join(out, "result.json"))
        raised = False
        try:
            Q.verify_bundle(out)
        except Q.Q4OError:
            raised = True
        ok(raised, "verify_bundle rejects a bundle missing result.json")

        # registry append only accepts a complete measured record.
        reg = os.path.join(tmp, "registry.jsonl")
        raised = False
        try:
            Q.append_registry(reg, {"run_id": "x"})
        except Q.Q4OError:
            raised = True
        ok(raised, "append_registry refuses an incomplete record")
        Q.append_registry(reg, {"run_id": "x", "experiment_id": Q.EXPERIMENT_ID,
                                "primary_value": 0.5, "verdict": "NO-GO",
                                "conclusion": "measured", "run_folder": out})
        ok(len(open(reg).read().strip().splitlines()) == 1,
           "append_registry writes exactly one JSON line per measured run")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_cpu_smoke_run() -> None:
    section("12. CPU smoke run — end to end on synthetic fixture data")
    try:
        import torch  # noqa: F401
    except Exception as exc:
        ok(False, f"torch unavailable, cannot run the smoke test: {exc}")
        return

    tmp = tempfile.mkdtemp(prefix="q4o_smoke_")
    try:
        # Includes unscorable records, so the end-to-end path is exercised on the
        # same cohort shape as real SVDB (56 scorable of 78).
        cohort = Q.synthetic_cohort(n_record=8, n_beat=110, seed=17, n_unscorable=3)
        rec_ok = Q.scorable_records(cohort)
        prov = {"abs_path": "<synthetic>", "file_name": "<synthetic>",
                "sha256": "<synthetic>", "synthetic": True}
        log = Q.RunLog(echo=False)
        result = Q.run_experiment(cohort, prov, tmp, seeds=Q.TRAIN_SEEDS[:2],
                                  epochs=1, batch=256, n_boot=100, device="cpu",
                                  smoke=True, log=log)

        ok(result["gates"]["verdict"] in ("PASS", "NO-GO"),
           f"the smoke run produced a verdict ({result['gates']['verdict']}) "
           f"— on synthetic data it carries no scientific meaning")
        ok(set(Q.ARMS) <= set(result["arms"]), "all five arms were scored")
        ok("comb_baseline_diagnostic" in result["arms"],
           "the comb-logistic diagnostic that isolates Arm E's residual is also scored")
        ok("E_minus_combBaseline" in result["contrasts"],
           "Arm E's residual effect is reported isolated from its larger offset set")
        ok("C_minus_A" in result["contrasts"] and "C_minus_D" in result["contrasts"],
           "the primary comparison and the negative control are both reported")

        n = cohort.n
        pred = np.load(os.path.join(tmp, "predictions.npz"))
        mask = pred["scored_mask"].astype(bool)
        ok(int(mask.sum()) < n,
           f"the run scored {int(mask.sum())} of {n} beats — "
           f"{len(cohort.records) - len(rec_ok)} records were below MIN_S/MIN_N")
        for arm in Q.ARMS:
            p = np.load(os.path.join(tmp, "arms", arm, "probs.npy"))
            ok(p.shape == (2, n) and np.all(np.isfinite(p[:, mask])),
               f"{arm}: probs.npy is {p.shape} and finite on every scored beat")
            ok(np.all(np.isnan(p[:, ~mask])),
               f"{arm}: unscored beats are NaN, not a fabricated probability")
        ok(np.all(pred["fold"][~mask] == -1),
           "unscored beats carry fold = -1 so they cannot be mistaken for held-out data")
        ok(np.array_equal(pred["sample_id"], cohort.sample_id),
           "predictions.npz sample_id matches the cohort order exactly")
        ok(np.array_equal(pred["record_id"], cohort.rid),
           "predictions.npz record_id aligns with the probs rows")

        # Arm A is deterministic: its per-seed rows must be identical.
        pa = np.load(os.path.join(tmp, "arms", Q.ARM_A, "probs.npy"))
        ok(np.allclose(pa[0][mask], pa[1][mask]),
           "Arm A is deterministic across seeds")

        man = json.load(open(os.path.join(tmp, "manifest.json")))
        for key in ("data", "git_commit_sha", "packages", "gpu", "fold_records",
                    "record_burden", "n_record_scorable"):
            ok(key in man, f"manifest.json records '{key}'")
        ok("torch" in man["packages"] and "numpy" in man["packages"],
           "manifest.json records the core package versions")

        cfg = json.load(open(os.path.join(tmp, "config.json")))
        ok(cfg["k_sweep"] == list(Q.K_SWEEP) and cfg["split"].startswith("frozen"),
           "config.json records the frozen split and the primary k-sweep")
        ok(cfg["waveform_permutation"]["seed"] == Q.PERM_SEED,
           "config.json records the Arm D permutation seed and rule")

        res = json.load(open(os.path.join(tmp, "result.json")))
        ok(res["arm_E_diagnostic"]["q4n_contaminated_reference"]["boost_fix"] == 0.8631,
           "Arm E carries the Q4-N number as a contaminated reference, not a baseline")
        ok("NOT the primary result" in res["arm_E_diagnostic"]["interpretation"],
           "result.json states that Arm E is diagnostic only")
        ok(res["smoke"] is True and "synthetic" in res["note"],
           "the smoke result is explicitly marked as carrying no scientific meaning")

        ok(os.path.getsize(os.path.join(tmp, "log.txt")) > 0, "log.txt is non-empty")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


_BUNDLE_CACHE: dict = {}


def _built_bundle(tmp: str):
    """Build one real run bundle (via run_experiment) and reuse it across tests."""
    if "dir" not in _BUNDLE_CACHE:
        cohort = Q.synthetic_cohort(n_record=8, n_beat=110, seed=17, n_unscorable=3)
        prov = {"abs_path": "<synthetic>", "file_name": "<synthetic>",
                "sha256": "<synthetic>", "synthetic": True}
        Q.run_experiment(cohort, prov, tmp, seeds=Q.TRAIN_SEEDS[:3], epochs=2,
                         batch=256, n_boot=100, device="cpu", smoke=True,
                         log=Q.RunLog(echo=False))
        _BUNDLE_CACHE["dir"] = tmp
        _BUNDLE_CACHE["cohort"] = cohort
    return _BUNDLE_CACHE["dir"]


def test_training_history_recording() -> None:
    section("13. training history — recorded without changing checkpoint selection")
    try:
        import torch  # noqa: F401
    except Exception as exc:
        ok(False, f"torch unavailable: {exc}")
        return
    tmp = tempfile.mkdtemp(prefix="q4o_hist_")
    try:
        run_dir = _built_bundle(tmp)
        hist_path = os.path.join(run_dir, "training_history.json")
        ok(os.path.exists(hist_path), "a new run writes training_history.json")
        hist = json.load(open(hist_path, encoding="utf-8"))
        ok(len(hist) > 0, f"history has {len(hist)} (arm, seed, fold) entries")

        fields = set(hist[0]["epochs"][0])
        ok({"epoch", "train_loss", "dev_loss", "dev_prauc", "alpha"} <= fields,
           f"each epoch records train loss, dev loss, dev PR-AUC and alpha ({sorted(fields)})")

        # The decisive property: recording extra metrics must not have changed which
        # checkpoint was selected. Selection is argmin of dev BCE loss, nothing else.
        mismatches = []
        for h in hist:
            losses = [e["dev_loss"] for e in h["epochs"]]
            if not losses:
                continue
            # argmin with the same strict-improvement rule the trainer uses
            best, best_i = float("inf"), -1
            for i, v in enumerate(losses):
                if v < best - 1e-6:
                    best, best_i = v, i
            if best_i != h["best_epoch"]:
                mismatches.append((h["arm"], h["seed"], h["fold"], best_i, h["best_epoch"]))
        ok(not mismatches,
           f"best_epoch is exactly argmin of the recorded dev BCE loss in all "
           f"{len(hist)} entries — dev PR-AUC never influenced selection")

        arms_with_alpha = {h["arm"] for h in hist
                           if h["epochs"] and h["epochs"][0]["alpha"] is not None}
        ok(Q.ARM_C in arms_with_alpha and Q.ARM_B not in arms_with_alpha,
           "alpha is recorded for the residual arms and is null for the plain CNN")
    finally:
        pass  # bundle is reused by the reporting tests; cleaned up there


def test_reporting() -> None:
    section("14. reporting — presentation only, reproduces result.json")
    try:
        import torch  # noqa: F401
    except Exception as exc:
        ok(False, f"torch unavailable: {exc}")
        return
    tmp = _BUNDLE_CACHE.get("dir") or tempfile.mkdtemp(prefix="q4o_report_")
    try:
        run_dir = _built_bundle(tmp)

        # (5) checksum stability — capture BEFORE any reporting runs
        before = Q.bundle_fingerprint(run_dir)
        ok(len(before) >= 6,
           f"fingerprinted {len(before)} measured artifacts before reporting")

        bundle = Q.load_run_bundle(run_dir)
        report = Q.generate_report(run_dir, log=Q.RunLog(echo=False))
        after = Q.bundle_fingerprint(run_dir)

        ok(before == after,
           "result.json, manifest.json, config.json, fold_map.json, predictions.npz "
           "and every probs.npy are byte-identical before and after reporting")
        ok(before.get("result.json") == after.get("result.json"),
           f"result.json checksum unchanged ({str(before.get('result.json'))[:16]}…)")

        # (1) reproduces result.json
        recon = report["reconciliation"]
        ok(recon["within_tolerance"] and recon["max_abs_diff"] <= 1e-9,
           f"per-record recomputation matches result.json exactly "
           f"(max abs diff {recon['max_abs_diff']:.2e} over {recon['n_checked']} checks)")

        # (2) C-A / C-D values and CIs match the source
        summary = report["executive_summary_ko"]
        md = open(report["report_markdown"], encoding="utf-8").read()
        for name in ("C_minus_A", "C_minus_D"):
            b = bundle.result["contrasts"][name]["record_bootstrap"]
            triple = (f"{b['mean']:+.4f}", f"{b['ci_low']:+.4f}", f"{b['ci_high']:+.4f}")
            ok(all(t in summary for t in triple),
               f"{name} mean and 95% CI appear verbatim in the executive summary "
               f"{triple}")
            ok(all(t in md for t in triple[:1]),
               f"{name} mean appears in report_summary.md")

        ok(bundle.result["gates"]["verdict"] in summary
           and report["verdict"] == bundle.result["gates"]["verdict"],
           f"the verdict is taken from result.json, not recomputed "
           f"({report['verdict']})")

        rows = Q.arm_metrics_rows(bundle)
        by_arm = {r["arm"]: r for r in rows}
        ok(abs(by_arm[Q.ARM_C]["delta_vs_A"]
               - bundle.result["contrasts"]["C_minus_A"]["record_bootstrap"]["mean"]) < 1e-12,
           "the arm table's Δ vs A is the paired contrast from result.json, not a re-estimate")
        ok(by_arm[Q.COMB_BASELINE]["delta_source"] == "mean_difference",
           "an arm with no paired contrast is labelled 'mean_difference', "
           "not passed off as a paired result")

        # (3) all seeds, not one
        n_seed = len(bundle.seeds)
        ok(n_seed >= 3, f"the bundle carries {n_seed} seeds")
        ksw_b = Q.per_record_ksw(bundle, Q.ARM_B)
        ok(ksw_b.shape == (n_seed, len(bundle.records)),
           f"per_record_ksw returns every seed {ksw_b.shape}")
        ok(not np.allclose(ksw_b[0], ksw_b.mean(axis=0)),
           "the seed-averaged per-record values genuinely differ from seed 0 alone "
           "— the waterfall is not a single-seed plot")
        prow = report["patient_rows"]
        ok(all(r["n_seed_averaged"] == n_seed for r in prow),
           f"every patient_delta row is averaged over all {n_seed} seeds")
        ok(len(prow) == len(bundle.records),
           f"patient_delta covers all {len(bundle.records)} scorable records")
        csv_text = open(os.path.join(bundle.figures_dir, "patient_delta.csv"),
                        encoding="utf-8").read()
        ok(all(c in csv_text.splitlines()[0]
               for c in ("s_burden", "ksw_A", "ksw_C", "delta_C_minus_A")),
           "patient_delta.csv carries S burden, baseline performance and C performance")

        # required artifacts
        for name in ("arm_summary_table.png", "arm_metrics.csv",
                     "primary_contrasts_zoom.png", "reference_gap_separate.png",
                     "achievement_by_k.png", "seed_effects.png",
                     "fold_training_diagnostics.png", "patient_delta_waterfall.png",
                     "patient_delta.csv", "metric_distribution.png",
                     "report_summary.md"):
            ok(os.path.exists(os.path.join(bundle.figures_dir, name)),
               f"report produced figures/{name}")

        ok(not os.path.exists(os.path.join(bundle.figures_dir, "contrasts.png")),
           "the old mixed-axis contrasts.png is gone — primary and reference "
           "contrasts are on separate axes")
        for name in ("contrasts_primary.png", "contrasts_reference.png"):
            ok(os.path.exists(os.path.join(bundle.figures_dir, name)),
               f"the run itself writes the split {name}")

        for token in ("Executive Summary", "0.8631", "baseline", "NO-GO", "PASS"):
            ok(token in md, f"report_summary.md covers '{token}'")
    finally:
        pass


def test_report_does_not_invent_history() -> None:
    section("15. reporting — never fabricates a missing training history")
    try:
        import torch  # noqa: F401
    except Exception as exc:
        ok(False, f"torch unavailable: {exc}")
        return
    src = _BUNDLE_CACHE.get("dir")
    if not src:
        ok(False, "no bundle available")
        return
    tmp = tempfile.mkdtemp(prefix="q4o_nohist_")
    try:
        run_dir = os.path.join(tmp, "run")
        shutil.copytree(src, run_dir)
        # Simulate a run produced before history recording existed — exactly the case
        # of the 20260806T0923 bundle.
        os.remove(os.path.join(run_dir, "training_history.json"))
        for f in os.listdir(os.path.join(run_dir, "figures")):
            os.remove(os.path.join(run_dir, "figures", f))

        bundle = Q.load_run_bundle(run_dir)
        ok(bundle.training_history is None,
           "a bundle without training_history.json reports it as absent, not as empty data")

        report = Q.generate_report(run_dir, log=Q.RunLog(echo=False))
        ok(report["training_history_present"] is False,
           "the report states that no training history exists")
        ok(not os.path.exists(os.path.join(run_dir, "figures", "learning_curves.png")),
           "no learning_curves.png is drawn when there is no history to draw")
        ok(not os.path.exists(os.path.join(run_dir, "training_history.json")),
           "the report does not write a training_history.json of its own")

        md = open(report["report_markdown"], encoding="utf-8").read()
        ok("training history 가 없다" in md,
           "report_summary.md says plainly that this run has no epoch-level history")
        ok("만들어내지 않았고" in md,
           "and states that nothing was fabricated to fill the gap")

        # Everything else still works without a history.
        ok(report["reconciliation"]["within_tolerance"],
           "the rest of the report still reconciles against result.json")
        ok(os.path.exists(os.path.join(run_dir, "figures", "report_summary.md")),
           "the full report is still produced")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
        shutil.rmtree(_BUNDLE_CACHE.get("dir", ""), ignore_errors=True)
        _BUNDLE_CACHE.clear()


def test_epoch_zero_is_post_update() -> None:
    section("16. epoch 0 semantics — the first dev eval happens AFTER optimizer steps")
    try:
        import torch
    except Exception as exc:
        ok(False, f"torch unavailable: {exc}")
        return

    cohort = Q.synthetic_cohort(n_record=8, n_beat=110, seed=11)
    rec_ok, burden, fold_map = _folds(cohort)
    X = Q.current_beat_input(cohort)
    offset = np.zeros(cohort.n, dtype=float)
    te_recs = [r for r, g in fold_map.items() if g == 0]
    tr_recs = [r for r, g in fold_map.items() if g != 0]
    fit_recs, dv_recs = Q.dev_records(tr_recs, burden)
    fit_idx = Q.samples_of(cohort, fit_recs)
    dev_idx = Q.samples_of(cohort, dv_recs)
    te_idx = Q.samples_of(cohort, te_recs)

    Q.set_determinism(Q.SEED0)
    net = Q.build_residual_net(X.shape[1], init="normal")
    init_state = {k: v.detach().clone() for k, v in net.state_dict().items()}

    # Count optimizer steps without touching the training loop itself.
    calls = {"n": 0}
    orig_adam = torch.optim.Adam

    class CountingAdam(orig_adam):
        def step(self, *a, **k):
            calls["n"] += 1
            return super().step(*a, **k)

    torch.optim.Adam = CountingAdam
    try:
        batch = 256
        scores, alpha, best_ep, dev_loss, hist = Q._train_one_fold(
            net, X, offset, cohort.y, fit_idx, dev_idx, te_idx,
            Q.SEED0, "cpu", epochs=1, batch=batch)
    finally:
        torch.optim.Adam = orig_adam

    n_minibatch = int(np.ceil(len(fit_idx) / batch))
    ok(calls["n"] == n_minibatch and calls["n"] >= 1,
       f"one epoch ran {calls['n']} optimizer steps ({n_minibatch} minibatches) "
       f"BEFORE the first dev evaluation — epoch 0 is a post-update checkpoint")
    ok(best_ep == 0,
       "with a single epoch the selected checkpoint is epoch 0 (best_loss starts at "
       "inf, so the first evaluated epoch always replaces the initial best_state)")
    ok(min(e["epoch"] for e in hist) == 0,
       "the recorded history starts at epoch 0 — the pre-training state (epoch -1) "
       "is never evaluated as a dev candidate in Q4-O")

    # The selected checkpoint's weights differ from the initialisation, so
    # 'best_epoch = 0' cannot mean 'reverted to the untrained state'.
    moved = any(not torch.equal(init_state[k], v.detach().cpu())
                for k, v in net.state_dict().items())
    ok(moved, "the epoch-0 checkpoint's weights differ from the initialisation")

    # Phase A must not have changed the selection rule: still argmin of dev BCE with
    # the trainer's strict-improvement tie-break, over epochs >= 0 only.
    losses = [e["dev_loss"] for e in hist]
    best, best_i = float("inf"), -1
    for i, l in enumerate(losses):
        if l < best - 1e-6:
            best, best_i = l, i
    ok(best_i == best_ep,
       "checkpoint selection is unchanged — best_epoch is still argmin of the "
       "recorded dev BCE loss")


def test_no_pretraining_restore_claims() -> None:
    section("17. prose — no 'reverted to untrained' / 'guaranteed lower bound' claims")
    root = os.path.dirname(os.path.abspath(__file__))
    targets = {
        "module": os.path.join(root, "q4o_leakage_free_residual.py"),
        "spec": os.path.join(root, os.pardir, "experiments", "specs",
                             "EXP-2026-001-q4o-leakage-free-residual-cnn.md"),
        "notebook": os.path.join(root, os.pardir, "notebooks",
                                 "quest47_q4o_leakage_free_residual_cnn.ipynb"),
    }
    # Affirmative-form phrasings only. Corrected text may QUOTE the old claim in
    # negation ("this entry originally claimed ..."), so the patterns below are the
    # exact assertive forms the correction removed.
    forbidden = [
        "학습되기 전",                    # "the pre-training checkpoint" (assertive)
        "학습 전 상태로 되돌아갔다",       # "reverted to the untrained state"
        "되돌아갔다",
        "untrained state",
        "never switched on",
        "reverted to its near-initial",
        "reverted to a near-initial",
        "guaranteed lower bound at initialisation",
        "guaranteed lower bound still holds",
        "lower bound guaranteed",
        "하한 보장",
    ]
    for name, path in targets.items():
        if not os.path.exists(path):
            ok(False, f"{name} not found at {path}")
            continue
        text = open(path, encoding="utf-8").read()
        hits = [p for p in forbidden if p in text]
        ok(not hits, f"{name} carries no pre-training-restore claim "
                     f"({'clean' if not hits else 'found: ' + ', '.join(hits)})")


def test_fingerprint_covers_history_when_present() -> None:
    section("18. fingerprint — training_history.json included iff the run wrote one")
    tmp = tempfile.mkdtemp(prefix="q4o_fp_")
    try:
        for name in ("config.json", "manifest.json", "result.json",
                     "fold_map.json", "predictions.npz"):
            with open(os.path.join(tmp, name), "wb") as fh:
                fh.write(name.encode())
        hist_path = os.path.join(tmp, "training_history.json")

        fp = Q.bundle_fingerprint(tmp)
        ok("training_history.json" not in fp,
           "a run without training_history.json is fingerprinted without it")
        ok(not os.path.exists(hist_path),
           "fingerprinting a history-less run does not create the file")

        with open(hist_path, "w", encoding="utf-8") as fh:
            fh.write("[]")
        fp2 = Q.bundle_fingerprint(tmp)
        ok("training_history.json" in fp2,
           "a run that wrote training_history.json gets it fingerprinted — reporting "
           "can no longer alter it silently")
        ok(set(fp) <= set(fp2) and all(fp[k] == fp2[k] for k in fp),
           "adding the history changes nothing about the other artifacts' hashes")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_windows_console_survives() -> None:
    section("19. Windows CP949 console — the runner does not die on em dashes")
    # The guarded failure: a strict cp949 stream rejects an em dash.
    strict = io.TextIOWrapper(io.BytesIO(), encoding="cp949", errors="strict")
    try:
        strict.write("—")
        strict.flush()
        raised = False
    except UnicodeEncodeError:
        raised = True
    ok(raised, "a strict cp949 stream rejects an em dash (this is what is guarded)")

    # Swap stdout for a strict cp949 stream, harden, and print what the runner prints.
    old = sys.stdout
    raw = io.BytesIO()
    strict_out = io.TextIOWrapper(raw, encoding="cp949", errors="strict")
    sys.stdout = strict_out
    survived, captured = True, b""
    try:
        _harden_stdout()
        print("— ─ EXP-2026-001 / Q4-O — test banner")
        sys.stdout.flush()
        captured = raw.getvalue()      # read before any wrapper can be GC-closed
    except UnicodeEncodeError:
        survived = False
    finally:
        sys.stdout = old
    ok(survived,
       "after _harden_stdout() the banner prints on a cp949 console without raising")
    ok(b"EXP-2026-001" in captured,
       "the output still reaches the console (characters replaced, not dropped)")


def main() -> int:
    print("=" * 78)
    print("EXP-2026-001 / Q4-O — leakage-free residual CNN")
    print("=" * 78)
    for fn in (test_fold_map_and_record_leakage,
               test_true_oof_assignment,
               test_unscorable_records_present,
               test_self_check_and_version,
               test_detects_q4n_overwrite,
               test_scaler_and_label_scope,
               test_arm_inputs_and_shapes,
               test_shuffled_control,
               test_residual_gradient_alive,
               test_residual_learning_path,
               test_metrics_and_statistics,
               test_gates,
               test_data_guard,
               test_artifact_schema,
               test_cpu_smoke_run,
               test_training_history_recording,
               test_reporting,
               test_report_does_not_invent_history,
               test_epoch_zero_is_post_update,
               test_no_pretraining_restore_claims,
               test_fingerprint_covers_history_when_present,
               test_windows_console_survives):
        try:
            fn()
        except Exception as exc:                                # noqa: BLE001
            import traceback
            traceback.print_exc()
            ok(False, f"{fn.__name__} raised {type(exc).__name__}: {exc}")

    print("\n" + "=" * 78)
    print(f"passed {len(PASS)} · failed {len(FAIL)}")
    for f in FAIL:
        print("  x " + f)
    print("=" * 78)
    return 1 if FAIL else 0


if __name__ == "__main__":
    raise SystemExit(main())
