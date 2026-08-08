#!/usr/bin/env python3
"""Tests for EXP-2026-002 / Q4-P — best_epoch=0 cause-separation diagnostic.

Spec: ``experiments/specs/EXP-2026-002-q4p-best-epoch-zero-diagnostic.md``

Coverage required by the spec (unit + CPU synthetic smoke only — the full GPU
experiment is NOT run here):
   1. epoch -1 output == morphology offset; alpha == 0; optimizer steps == 0
   2. epoch 0 has optimizer steps > 0
   3. every selector includes epoch -1 as a candidate
   4. selectors read dev information only (test values never change the choice)
   5. best checkpoint == argmin/argmax of the selector's definition, earliest on tie
   6. S2's alpha LR and CNN/head LRs are exactly as pre-registered
   7. paired initialisation and minibatch order across schedules
   8. Arm D's shuffle never crosses record boundaries
   9. outer-test labels cannot touch selection
  10. fixed trajectories: patience never stops the optimizer
  11. reporting leaves measured artifacts byte-identical
  12. no training_history.json is invented for runs that lack one
  13. synthetic trajectory fixtures separate overshoot / overfit / selector mismatch
  14. CPU smoke run end to end (bundle schema, figures, decision matrix)

Run:  python mit-bih/test_q4p_best_epoch_zero_diagnostic.py
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
    """Same CP949 guard as the Q4-O runner: garbled beats dead."""
    for name in ("stdout", "stderr"):
        stream = getattr(sys, name, None)
        if stream is None:
            continue
        enc = getattr(stream, "encoding", None) or "utf-8"
        try:
            "—─".encode(enc)
            continue
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

import q4o_leakage_free_residual as Q4O  # noqa: E402
import q4p_best_epoch_zero_diagnostic as QP  # noqa: E402

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


def _have_torch() -> bool:
    try:
        import torch  # noqa: F401
        return True
    except Exception:
        return False


def _fold_setup(seed: int = 17):
    """One synthetic outer fold with fit/dev/test indices and a zero offset."""
    cohort = Q4O.synthetic_cohort(n_record=8, n_beat=110, seed=seed)
    rec_ok = Q4O.scorable_records(cohort)
    burden = Q4O.record_burden(cohort, rec_ok)
    fold_map = Q4O.make_fold_map(rec_ok, burden)
    records = sorted(fold_map)
    te_recs = [r for r in records if fold_map[r] == 0]
    tr_recs = [r for r in records if fold_map[r] != 0]
    fit_recs, dv_recs = Q4O.dev_records(tr_recs, burden)
    return (cohort,
            Q4O.samples_of(cohort, fit_recs),
            Q4O.samples_of(cohort, dv_recs),
            Q4O.samples_of(cohort, te_recs))


def _run_traj(schedule: str, seed: int = 101, epochs: int = 2,
              flip_test_labels: bool = False):
    cohort, fit_idx, dev_idx, te_idx = _fold_setup()
    X = Q4O.current_beat_input(cohort)
    offset = np.zeros(cohort.n, dtype=float)
    y = np.array(cohort.y, copy=True)
    if flip_test_labels:
        y[te_idx] = ~y[te_idx]
    Q4O.set_determinism(seed)
    net = Q4O.build_residual_net(X.shape[1], init="normal")
    res = QP.diagnostic_train_one_fold(
        net, X, offset, y, cohort.rid, fit_idx, dev_idx, te_idx,
        seed, "cpu", schedule, epochs=epochs, batch=256)
    return res, net, fit_idx


# ─────────────────────────────────────────────────────────────────────────────
def test_pretrain_checkpoint_semantics() -> None:
    section("1. epoch -1 — 0 steps, alpha 0, output == offset; epoch 0 is post-step")
    if not _have_torch():
        ok(False, "torch unavailable")
        return
    res, _net, fit_idx = _run_traj("S0_original", epochs=2)
    cps = {c["epoch"]: c for c in res["checkpoints"]}
    pre = cps[QP.PRETRAIN_EPOCH]
    ok(pre["optimizer_steps"] == 0, "epoch -1 records exactly 0 optimizer steps")
    ok(pre["alpha"] == 0.0, "epoch -1 alpha is exactly 0")
    ok(pre["eff_residual_mean_abs"] == 0.0,
       "epoch -1 effective residual (alpha x residual) is exactly 0 on dev")
    # The in-loop assertion already compared logits to the offset; re-derive here:
    # with alpha == 0 the dev pooled BCE must equal the BCE of the offset itself.
    cohort, fit2, dev2, te2 = _fold_setup()
    off_bce = QP.pooled_bce(np.zeros(len(dev2)), cohort.y[dev2])
    ok(abs(pre["dev_pooled_bce"] - off_bce) < 1e-9,
       "epoch -1 dev BCE equals the raw offset's BCE — the output IS the offset")

    n_minibatch = int(np.ceil(len(fit_idx) / 256))
    e0 = cps[0]
    ok(e0["optimizer_steps"] == n_minibatch and e0["optimizer_steps"] > 0,
       f"epoch 0 sits after {e0['optimizer_steps']} optimizer steps (> 0)")
    ok(cps[1]["optimizer_steps"] == 2 * n_minibatch,
       "epoch 1 accumulates a second full epoch of steps")


def test_fixed_trajectory_no_early_stop() -> None:
    section("2. fixed trajectories — patience never stops the optimizer")
    if not _have_torch():
        ok(False, "torch unavailable")
        return
    epochs = 4
    res, _n, _f = _run_traj("S0_original", epochs=epochs)
    ok(len(res["checkpoints"]) == epochs + 1,
       f"all {epochs} epochs ran plus epoch -1 ({len(res['checkpoints'])} "
       f"checkpoints) — nothing stopped the loop early")
    eps = [c["epoch"] for c in res["checkpoints"]]
    ok(eps == list(range(-1, epochs)),
       f"checkpoints are exactly epochs -1..{epochs - 1} in order")


def test_selectors_include_pretrain_and_tie_break() -> None:
    section("3. selectors — epoch -1 candidacy, argmin/argmax, earliest-on-tie")
    base = {"dev_pooled_bce": 0.5, "dev_record_bce": 0.5, "dev_record_ksweep": 0.4}

    # epoch -1 strictly best -> every selector must pick it.
    cps = [dict(base, epoch=-1, dev_pooled_bce=0.30, dev_record_bce=0.30,
                dev_record_ksweep=0.60),
           dict(base, epoch=0), dict(base, epoch=1)]
    got = {s: QP.select_checkpoint(cps, s) for s in QP.SELECTORS}
    ok(all(v == -1 for v in got.values()),
       f"when the pre-training checkpoint is best, every selector returns -1 ({got})")

    # exact tie everywhere -> earliest wins, and the earliest is -1.
    cps = [dict(base, epoch=-1), dict(base, epoch=0), dict(base, epoch=1)]
    got = {s: QP.select_checkpoint(cps, s) for s in QP.SELECTORS}
    ok(all(v == -1 for v in got.values()),
       f"a full tie selects the EARLIEST checkpoint, which is epoch -1 ({got})")

    # sub-tolerance improvement does not displace the earlier checkpoint.
    cps = [dict(base, epoch=-1),
           dict(base, epoch=0, dev_pooled_bce=0.5 - 0.5 * QP.TIE_TOL_BCE)]
    ok(QP.select_checkpoint(cps, QP.SEL0) == -1,
       "an improvement smaller than the pre-registered tolerance is a tie")

    # each selector follows its own field and direction.
    cps = [dict(base, epoch=-1),
           dict(base, epoch=0, dev_pooled_bce=0.20, dev_record_bce=0.55),
           dict(base, epoch=1, dev_record_bce=0.20, dev_record_ksweep=0.70)]
    ok(QP.select_checkpoint(cps, QP.SEL0) == 0,
       "SEL0 minimises pooled dev BCE")
    ok(QP.select_checkpoint(cps, QP.SEL1) == 1,
       "SEL1 minimises record-balanced dev BCE (primary)")
    ok(QP.select_checkpoint(cps, QP.SEL2) == 1,
       "SEL2 maximises dev record k-sweep (sensitivity only)")

    # a trajectory without epoch -1 is rejected outright.
    try:
        QP.select_checkpoint([dict(base, epoch=0)], QP.SEL0)
        ok(False, "a trajectory missing epoch -1 must be rejected")
    except QP.Q4PError:
        ok(True, "a trajectory missing epoch -1 is rejected loudly")


def test_selectors_are_dev_only() -> None:
    section("4. selectors — test values cannot change the choice")
    base = {"dev_pooled_bce": 0.5, "dev_record_bce": 0.5, "dev_record_ksweep": 0.4}
    cps = [dict(base, epoch=-1),
           dict(base, epoch=0, dev_pooled_bce=0.3, dev_record_bce=0.3,
                dev_record_ksweep=0.6)]
    before = {s: QP.select_checkpoint(cps, s) for s in QP.SELECTORS}
    # Splice in wildly different test-side numbers — selection must not move.
    for c in cps:
        c["test_pooled_bce"] = 0.0 if c["epoch"] == -1 else 99.0
        c["test_record_ksweep"] = 1.0 if c["epoch"] == -1 else 0.0
    after = {s: QP.select_checkpoint(cps, s) for s in QP.SELECTORS}
    ok(before == after,
       "adding adversarial test-side fields changes no selector's choice")
    used = set(QP.SELECTOR_FIELD.values())
    ok(all(f.startswith("dev_") for f in used),
       f"every selector field is a dev_ quantity ({sorted(used)})")


def test_schedule_lrs_and_pairing() -> None:
    section("5. schedules — exact LRs, paired init, identical minibatch order")
    if not _have_torch():
        ok(False, "torch unavailable")
        return
    import torch

    # 5a. exact pre-registered learning rates in the optimizer's param groups.
    Q4O.set_determinism(7)
    net = Q4O.build_residual_net(2, init="normal")
    for sch, want in (("S0_original", (1e-3, 1e-3, 1e-3)),
                      ("S1_global_low", (3e-4, 3e-4, 3e-4)),
                      ("S2_alpha_low", (1e-3, 1e-3, 1e-4))):
        opt = QP.build_optimizer(net, sch)
        got = {g["name"]: g["lr"] for g in opt.param_groups}
        ok((got["trunk"], got["head"], got["alpha"]) == want,
           f"{sch}: trunk/head/alpha LRs are exactly {want}")
        ok(all(g["weight_decay"] == Q4O.DL_WD for g in opt.param_groups),
           f"{sch}: weight decay stays at Q4-O's {Q4O.DL_WD} for every group")
    alpha_group = [g for g in QP.build_optimizer(net, "S2_alpha_low").param_groups
                   if g["name"] == "alpha"][0]
    ok(len(alpha_group["params"]) == 1
       and alpha_group["params"][0] is net.alpha,
       "S2's low-LR group contains exactly the alpha parameter")

    # 5b. paired initialisation + identical minibatch order across schedules.
    res0, _n0, _f0 = _run_traj("S0_original", seed=555, epochs=1)
    res2, _n2, _f2 = _run_traj("S2_alpha_low", seed=555, epochs=1)
    pre0 = next(c for c in res0["checkpoints"] if c["epoch"] == -1)
    pre2 = next(c for c in res2["checkpoints"] if c["epoch"] == -1)
    ok(abs(pre0["dev_pooled_bce"] - pre2["dev_pooled_bce"]) < 1e-12,
       "identical pre-training dev BCE — the two schedules start from the same "
       "initial parameters")
    g0, g2 = res0["grad_log"][0], res2["grad_log"][0]
    same_grads = all(abs(g0[f"grad_{p}"] - g2[f"grad_{p}"]) < 1e-9
                     for p in ("alpha", "head", "trunk"))
    ok(same_grads,
       "step-0 gradient norms are identical across schedules — same init AND the "
       "same first minibatch (paired minibatch order)")
    ok(g0["upd_alpha"] > 0 and g2["upd_alpha"] > 0
       and g2["upd_alpha"] < g0["upd_alpha"],
       f"but S2's alpha UPDATE is smaller ({g2['upd_alpha']:.2e} < "
       f"{g0['upd_alpha']:.2e}) — the low alpha LR acts where it should")


def test_shuffle_respects_record_boundaries() -> None:
    section("6. Arm D — the within-record shuffle never crosses records")
    cohort = Q4O.synthetic_cohort(n_record=6, n_beat=90, seed=5)
    shuffled, rule = Q4O.shuffle_waveforms_within_record(cohort)
    crossed = False
    moved = 0
    for r in cohort.records:
        ii = cohort.idx_of[int(r)]
        orig = np.sort(cohort.beat[ii].reshape(len(ii), -1), axis=0)
        perm = np.sort(shuffled[ii].reshape(len(ii), -1), axis=0)
        if not np.array_equal(orig, perm):
            crossed = True
        moved += int((shuffled[ii] != cohort.beat[ii]).any(axis=(1, 2)).sum())
    ok(not crossed,
       "each record's multiset of waveforms is preserved exactly — nothing "
       "crossed a record boundary")
    ok(moved / cohort.n > 0.5 and rule["moved_fraction"] > 0.5,
       f"and the permutation is far from identity ({rule['moved_fraction']:.2f} "
       f"of beats moved)")


def test_outer_test_labels_cannot_touch_selection() -> None:
    section("7. outer-test labels — flipping them changes nothing before scoring")
    if not _have_torch():
        ok(False, "torch unavailable")
        return
    res_a, _na, _fa = _run_traj("S0_original", seed=321, epochs=2,
                                flip_test_labels=False)
    res_b, _nb, _fb = _run_traj("S0_original", seed=321, epochs=2,
                                flip_test_labels=True)
    ok(res_a["selected"] == res_b["selected"],
       "flipping every outer-test label leaves all three selections unchanged")
    dev_a = [c["dev_pooled_bce"] for c in res_a["checkpoints"]]
    dev_b = [c["dev_pooled_bce"] for c in res_b["checkpoints"]]
    ok(np.allclose(dev_a, dev_b, atol=1e-12),
       "and every dev metric on the trajectory is bit-for-bit unaffected")
    same_test_logits = all(
        np.allclose(res_a["test_logits_by_epoch"][e],
                    res_b["test_logits_by_epoch"][e], atol=1e-12)
        for e in res_a["test_logits_by_epoch"])
    ok(same_test_logits,
       "test logits are identical too — labels were never read during training")


def test_decision_tree_separates_causes() -> None:
    section("8. decision tree — synthetic fixtures hit the intended branches")

    def summary_base():
        boot = {"mean": 0.0, "ci_low": -0.001, "ci_high": 0.001}
        contrasts = {sch: {sel: {"C_minus_D": {"record_bootstrap": dict(boot)},
                                 "C_minus_A": {"record_bootstrap": dict(boot)},
                                 "p10": {"A": 0.5, "C": 0.5, "D": 0.5}}
                          for sel in QP.SELECTORS}
                     for sch in QP.SCHEDULE_NAMES}
        return {
            "best_epoch_dist": {
                arm: {sch: {sel: {"p_pretrain": 0.0, "p_epoch0": 1.0,
                                  "p_later": 0.0, "epochs": [0] * 10, "n": 10}
                            for sel in QP.SELECTORS}
                      for sch in QP.SCHEDULE_NAMES}
                for arm in QP.QP_ARMS},
            "contrasts": contrasts,
            "trajectory_flags": {QP.ARM_C: {sch: {
                "frac_epoch0_better_than_pretrain": 0.0,
                "frac_train_loss_decreasing": 0.0,
                "frac_dev_record_bce_worsens_later": 0.0}
                for sch in QP.SCHEDULE_NAMES}},
            "best_epoch_shift": {QP.ARM_C: {sch: {sel: {"moved_later": False}
                                                  for sel in QP.SELECTORS}
                                            for sch in QP.SCHEDULE_NAMES}},
            "schedule_dev_gain": {QP.ARM_C: {sch: {sel: 0.0
                                                   for sel in QP.SELECTORS}
                                             for sch in QP.SCHEDULE_NAMES}},
            "selector_comparison": {QP.ARM_C: {
                "sel1_beats_sel0_dev": False, "sel1_beats_sel0_test": False}},
            "schedule_symmetry": {"gains_similar_c_and_d": False,
                                  "c_minus_d_vanishes": False},
            "c_over_d_consistency": {"ci_low_gt_0": False,
                                     "seed_direction_stable": False,
                                     "lower_tail_improves": False},
        }

    # B1: pre-training best almost everywhere, C-D <= 0.
    s = summary_base()
    d = s["best_epoch_dist"][QP.ARM_C]["S0_original"][QP.PRIMARY_SELECTOR]
    d.update(p_pretrain=0.9, p_epoch0=0.1, epochs=[-1] * 9 + [0])
    s["contrasts"]["S0_original"][QP.PRIMARY_SELECTOR]["C_minus_D"][
        "record_bootstrap"]["mean"] = -0.0005
    dec = QP.evaluate_decision_tree(s)
    ok(dec["firing"] == ["B1_immediately_harmful_or_no_signal"],
       f"pre-training-dominant fixture fires B1 only ({dec['verdict']})")

    # B2: epoch 0 beats -1, train falls, record-balanced dev worsens later.
    s = summary_base()
    s["trajectory_flags"][QP.ARM_C]["S0_original"] = {
        "frac_epoch0_better_than_pretrain": 1.0,
        "frac_train_loss_decreasing": 1.0,
        "frac_dev_record_bce_worsens_later": 1.0}
    dec = QP.evaluate_decision_tree(s)
    ok(dec["firing"] == ["B2_first_epoch_then_overfit"],
       f"first-epoch-overfit fixture fires B2 only ({dec['verdict']})")

    # B3: S1 moves the best epoch later with dev + C-D gains over S0.
    s = summary_base()
    s["best_epoch_shift"][QP.ARM_C]["S1_global_low"][QP.PRIMARY_SELECTOR][
        "moved_later"] = True
    s["schedule_dev_gain"][QP.ARM_C]["S1_global_low"][QP.PRIMARY_SELECTOR] = 0.02
    s["contrasts"]["S1_global_low"][QP.PRIMARY_SELECTOR]["C_minus_D"][
        "record_bootstrap"]["mean"] = 0.004
    dec = QP.evaluate_decision_tree(s)
    ok(dec["firing"] == ["B3_lr_or_alpha_overshoot"],
       f"overshoot fixture fires B3 only ({dec['verdict']})")

    # B4: SEL1 beats SEL0 on dev AND paired test.
    s = summary_base()
    s["selector_comparison"][QP.ARM_C] = {"sel1_beats_sel0_dev": True,
                                          "sel1_beats_sel0_test": True}
    dec = QP.evaluate_decision_tree(s)
    ok(dec["firing"] == ["B4_selector_mismatch"],
       f"selector-mismatch fixture fires B4 only ({dec['verdict']})")

    # B5 and B6 fire from their summary blocks.
    s = summary_base()
    s["schedule_symmetry"] = {"gains_similar_c_and_d": True,
                              "c_minus_d_vanishes": True}
    dec = QP.evaluate_decision_tree(s)
    ok(dec["firing"] == ["B5_schedule_artifact_not_waveform_specific"],
       "schedule-artifact fixture fires B5 only")
    s = summary_base()
    s["c_over_d_consistency"] = {"ci_low_gt_0": True,
                                 "seed_direction_stable": True,
                                 "lower_tail_improves": True}
    dec = QP.evaluate_decision_tree(s)
    ok(dec["firing"] == ["B6_real_waveform_residual_candidate"],
       "real-residual fixture fires B6 only")

    # Mixed evidence is reported as multiple causes, never forced to one.
    s = summary_base()
    s["trajectory_flags"][QP.ARM_C]["S0_original"] = {
        "frac_epoch0_better_than_pretrain": 1.0,
        "frac_train_loss_decreasing": 1.0,
        "frac_dev_record_bce_worsens_later": 1.0}
    s["selector_comparison"][QP.ARM_C] = {"sel1_beats_sel0_dev": True,
                                          "sel1_beats_sel0_test": True}
    dec = QP.evaluate_decision_tree(s)
    ok(dec["verdict"].startswith("MULTIPLE_CAUSES")
       and set(dec["firing"]) == {"B2_first_epoch_then_overfit",
                                  "B4_selector_mismatch"},
       f"mixed fixture reports MULTIPLE_CAUSES ({dec['verdict']})")

    # No evidence at all -> UNDECIDED.
    dec = QP.evaluate_decision_tree(summary_base())
    ok(dec["verdict"] == "UNDECIDED",
       "an all-quiet summary is UNDECIDED, not forced into a branch")


_SMOKE_CACHE: dict = {}


def _smoke_bundle(tmp: str) -> str:
    if "dir" not in _SMOKE_CACHE:
        cohort = Q4O.synthetic_cohort(n_record=8, n_beat=110, seed=17,
                                      n_unscorable=2)
        prov = {"abs_path": "<synthetic>", "file_name": "<synthetic>",
                "sha256": "<synthetic>", "synthetic": True}
        QP.run_diagnostic(cohort, prov, tmp, seeds=Q4O.TRAIN_SEEDS[:2],
                          epochs=2, batch=256, n_boot=60, device="cpu",
                          smoke=True, log=Q4O.RunLog(echo=False))
        _SMOKE_CACHE["dir"] = tmp
    return _SMOKE_CACHE["dir"]


def test_smoke_run_end_to_end() -> None:
    section("9. CPU smoke run — bundle schema, figures, decision matrix")
    if not _have_torch():
        ok(False, "torch unavailable")
        return
    tmp = tempfile.mkdtemp(prefix="q4p_smoke_")
    run_dir = _smoke_bundle(tmp)

    for name in QP.REQUIRED_BUNDLE_FILES:
        ok(os.path.exists(os.path.join(run_dir, name)),
           f"bundle carries {name}")
    for name in QP.FIGURE_FILES + ("report_summary.md",):
        ok(os.path.exists(os.path.join(run_dir, "figures", name)),
           f"figures/{name} exists")

    res = json.load(open(os.path.join(run_dir, "result.json"), encoding="utf-8"))
    ok(res["smoke"] is True and "SYNTHETIC" in res["note"],
       "the smoke result is marked as carrying no scientific meaning")
    ok(res["primary_selector"] == QP.SEL1,
       "the primary diagnostic selector is SEL1_record_bce, as pre-registered")
    ok(res["decision_tree"]["verdict"] is not None,
       f"a decision-tree verdict is computed ({res['decision_tree']['verdict']})")

    hist = json.load(open(os.path.join(run_dir, "training_history.json"),
                          encoding="utf-8"))
    n_expected = (len(QP.QP_ARMS) * len(QP.SCHEDULE_NAMES) * 2
                  * Q4O.N_OUTER_FOLDS)
    ok(len(hist) == n_expected,
       f"history holds all {n_expected} (arm, schedule, seed, fold) trajectories")
    all_have_pre = all(any(c["epoch"] == -1 and c["optimizer_steps"] == 0
                           and c["alpha"] == 0.0 for c in h["checkpoints"])
                       for h in hist)
    ok(all_have_pre, "every stored trajectory includes the epoch -1 checkpoint "
                     "with 0 steps and alpha == 0")
    all_full = all(len(h["checkpoints"]) == 2 + 1 for h in hist)
    ok(all_full, "every trajectory ran the full fixed epoch budget")
    sel_match = all(
        h["selected"][sel] == QP.select_checkpoint(h["checkpoints"], sel)
        for h in hist for sel in QP.SELECTORS)
    ok(sel_match, "stored selections replay exactly from the stored trajectories")

    with np.load(os.path.join(run_dir, "predictions.npz")) as npz:
        keys = set(npz.files)
        want = {f"logit_{arm}__{sch}__{sel}" for arm in QP.QP_ARMS
                for sch in QP.SCHEDULE_NAMES for sel in QP.SELECTORS}
        ok(want <= keys,
           f"predictions.npz stores all {len(want)} arm x schedule x selector "
           f"score stacks")
        mask = npz["scored_mask"].astype(bool)
        one = npz[f"logit_{QP.ARM_C}__S0_original__{QP.SEL1}"]
        ok(one.shape[0] == 2 and np.all(np.isfinite(one[:, mask])),
           "selected-checkpoint test logits are finite on every scored beat")
        ok(np.all(np.isnan(one[:, ~mask])),
           "unscored beats stay NaN — nothing fabricated")

    n_probs = 0
    for root, _d, files in os.walk(os.path.join(run_dir, "arms")):
        n_probs += sum(1 for f in files if f == "probs.npy")
    ok(n_probs == len(QP.QP_ARMS) * len(QP.SCHEDULE_NAMES) * len(QP.SELECTORS),
       f"arms/<arm>/<schedule>/<selector>/probs.npy exists for all {n_probs} cells")
    # NOTE: run dir is kept for tests 10-11 and removed there.


def test_reporting_immutability() -> None:
    section("10. reporting — measured artifacts are byte-identical before/after")
    if not _have_torch():
        ok(False, "torch unavailable")
        return
    run_dir = _SMOKE_CACHE.get("dir")
    if not run_dir or not os.path.isdir(run_dir):
        ok(False, "smoke bundle unavailable (test 9 must run first)")
        return
    before = QP.bundle_fingerprint(run_dir)
    ok(len(before) > 0, f"fingerprinted {len(before)} measured artifacts")
    ok("training_history.json" in before,
       "training_history.json is part of the fingerprint for runs that have one")
    res = json.load(open(os.path.join(run_dir, "result.json"), encoding="utf-8"))
    hist = json.load(open(os.path.join(run_dir, "training_history.json"),
                          encoding="utf-8"))
    cohort = Q4O.synthetic_cohort(n_record=8, n_beat=110, seed=17, n_unscorable=2)
    fold_map = {int(k): int(v) for k, v in json.load(
        open(os.path.join(run_dir, "fold_map.json")))["record_to_fold"].items()}
    records = sorted(fold_map)
    QP._write_figures_and_report(run_dir, res, hist, cohort, records,
                                 [int(s) for s in Q4O.TRAIN_SEEDS[:2]],
                                 Q4O.RunLog(echo=False))
    after = QP.bundle_fingerprint(run_dir)
    ok(before == after,
       "re-running the full reporting pass leaves every measured artifact "
       "byte-identical (the writer itself raises if not)")


def test_no_history_invention() -> None:
    section("11. absent history — never invented for a run that lacks one")
    if not _have_torch():
        ok(False, "torch unavailable")
        return
    run_dir = _SMOKE_CACHE.get("dir")
    if not run_dir or not os.path.isdir(run_dir):
        ok(False, "smoke bundle unavailable (test 9 must run first)")
        return
    try:
        tmp = tempfile.mkdtemp(prefix="q4p_nohist_")
        clone = os.path.join(tmp, "bundle")
        shutil.copytree(run_dir, clone)
        os.remove(os.path.join(clone, "training_history.json"))
        fp = QP.bundle_fingerprint(clone)
        ok("training_history.json" not in fp,
           "a bundle without a history is fingerprinted without one")
        ok(not os.path.exists(os.path.join(clone, "training_history.json")),
           "fingerprinting did not create the file")
        try:
            QP.verify_bundle(clone)
            ok(False, "verify_bundle must flag the missing history for Q4-P runs")
        except QP.Q4PError:
            ok(True, "verify_bundle reports the missing history instead of "
                     "writing one (Q4-P runs are contracted to record it)")
        ok(not os.path.exists(os.path.join(clone, "training_history.json")),
           "and still no file was invented afterwards")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
        shutil.rmtree(os.path.dirname(run_dir), ignore_errors=True)
        _SMOKE_CACHE.clear()


def test_qo_reuse_not_copies() -> None:
    section("12. reuse — Q4-P imports Q4-O's frozen machinery, no local copies")
    src = open(os.path.abspath(QP.__file__), encoding="utf-8").read()
    ok("import q4o_leakage_free_residual" in src,
       "Q4-P imports the Q4-O module")
    for name in ("def build_features", "def make_fold_map",
                 "def cross_fitted_offsets", "def build_residual_net",
                 "def shuffle_waveforms_within_record",
                 "def paired_record_bootstrap", "def achievement_at"):
        ok(name not in src,
           f"'{name}' is not redefined in Q4-P — the Q4-O definition is the one "
           f"that runs")
    ok(QP.build_residual_net is Q4O.build_residual_net,
       "the model builder is literally Q4-O's object")
    ok(QP.SCHEDULES["S0_original"]["lr_trunk"] == Q4O.DL_LR,
       "S0_original reproduces Q4-O's LR exactly")


def main() -> int:
    print("=" * 78)
    print(f"EXP-2026-002 / Q4-P — best_epoch=0 diagnostic ({QP.STATUS})")
    print("=" * 78)
    for fn in (test_pretrain_checkpoint_semantics,
               test_fixed_trajectory_no_early_stop,
               test_selectors_include_pretrain_and_tie_break,
               test_selectors_are_dev_only,
               test_schedule_lrs_and_pairing,
               test_shuffle_respects_record_boundaries,
               test_outer_test_labels_cannot_touch_selection,
               test_decision_tree_separates_causes,
               test_smoke_run_end_to_end,
               test_reporting_immutability,
               test_no_history_invention,
               test_qo_reuse_not_copies):
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
