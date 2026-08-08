#!/usr/bin/env python3
"""EXP-2026-002 / Q4-P — why did Q4-O's Arm C select best_epoch = 0?

Spec: ``experiments/specs/EXP-2026-002-q4p-best-epoch-zero-diagnostic.md``
Status: EXPLORATORY DIAGNOSTIC / RESULT NOT RUN — nothing in this file is a result.

The one fixed question
----------------------
In Q4-O, every Arm C (seed x fold) selected the checkpoint after the FIRST completed
training epoch (best_epoch = 0). Q4-O never evaluated the pre-training state as a dev
candidate, so it cannot say which of these produced that pattern:

  H1  immediately-harmful / no-signal residual   (epoch -1 would have been best)
  H2  overfitting after the first epoch          (epoch 0 > -1 on dev, then decay)
  H3  learning-rate / alpha-gate overshoot       (lower LRs move the best epoch later)
  H4  selector mismatch                          (pooled-BCE checkpoint selection vs
                                                  patient-level evaluation)

Q4-P re-trains Arms C and D only, under three pre-registered schedules, evaluates the
true pre-training checkpoint (epoch -1) as a first-class candidate, runs a fixed
24-epoch trajectory (patience never stops the optimizer), and computes three
dev-only selectors on the same trajectory. Architecture and inputs are frozen at
Q4-O's; nothing here upgrades the model.

What this module reuses from Q4-O (imported, never copied):
data loading, features, fold map, dev split, leakage assertions, the residual model
builder, arm inputs (current beat / within-record shuffle), Arm A, cross-fitted
offsets, metrics, and the paired bootstraps. The *diagnostic training loop* is new
and lives here — Q4-O's loop and its past results are not touched.

Commands
--------
    python mit-bih/test_q4p_best_epoch_zero_diagnostic.py
    python mit-bih/q4p_best_epoch_zero_diagnostic.py --smoke --out /tmp/q4p_smoke
    python mit-bih/q4p_best_epoch_zero_diagnostic.py --data <svdb_data5.npz> --out <dir>
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import q4o_leakage_free_residual as Q4O  # noqa: E402
from q4o_leakage_free_residual import (  # noqa: E402
    ARM_A, ARM_C, ARM_D,
    Cohort, Q4OError, RunLog,
    DL_BATCH, DL_WD, K_SWEEP, PERM_SEED, SEED0, TRAIN_SEEDS,
    N_OUTER_FOLDS,
    assert_disjoint, assert_finite, assert_fold_map_partition,
    achievement_at, build_features, build_residual_net, cross_fitted_offsets,
    current_beat_input, dev_records, git_commit_sha, gpu_info, load_cohort,
    make_fold_map, package_versions, paired_record_bootstrap,
    hierarchical_bootstrap, record_burden, run_logistic_arm, samples_of,
    scorable_records, set_determinism, sha256_file,
    shuffle_waveforms_within_record, synthetic_cohort, _chunked_mean_std,
    _json_safe, _require_torch,
)

# ─────────────────────────────────────────────────────────────────────────────
# Identity and pre-registered protocol constants — frozen before any run.
# ─────────────────────────────────────────────────────────────────────────────
EXPERIMENT_ID = "EXP-2026-002"
ARM_ID = "Q4-P"
RUN_SLUG = "q4p_best_epoch_zero_diagnostic"
STATUS = "EXPLORATORY DIAGNOSTIC / RESULT NOT RUN"

MODULE_VERSION = 1
MODULE_BUILD = "2026-08-08 q4p.1 — design; no full run has been executed"

N_EPOCHS = 24                   # every schedule runs ALL 24 epochs; patience never
                                # interrupts the optimizer (trajectories must be
                                # complete so early stopping cannot mask the cause)
GRAD_LOG_STEPS = 100            # per-step gradient/update norms for the first N steps

# Checkpoint indexing. epoch -1 is the true pre-training state: 0 optimizer steps,
# alpha exactly 0, output identical to the morphology offset. Q4-O never evaluated
# it; Q4-P stores and selects over it like any other checkpoint.
PRETRAIN_EPOCH = -1

# The three pre-registered schedules. Nothing may be added after seeing results.
SCHEDULES: Dict[str, Dict[str, float]] = {
    "S0_original":  {"lr_trunk": 1e-3, "lr_head": 1e-3, "lr_alpha": 1e-3},
    "S1_global_low": {"lr_trunk": 3e-4, "lr_head": 3e-4, "lr_alpha": 3e-4},
    "S2_alpha_low": {"lr_trunk": 1e-3, "lr_head": 1e-3, "lr_alpha": 1e-4},
}
SCHEDULE_NAMES = tuple(SCHEDULES)

# The three dev-only selectors, all computed on the SAME stored trajectory.
SEL0 = "SEL0_pooled_bce"        # min pooled dev beat BCE (Q4-O's rule + epoch -1)
SEL1 = "SEL1_record_bce"        # min mean-over-dev-records per-record BCE — PRIMARY
SEL2 = "SEL2_record_ksweep"     # max dev record-level k-sweep — sensitivity only
SELECTORS = (SEL0, SEL1, SEL2)
PRIMARY_SELECTOR = SEL1

# Pre-registered tie tolerances. A candidate must beat the incumbent by MORE than
# the tolerance to replace it; scanning runs from epoch -1 upward, so ties keep the
# EARLIEST checkpoint (including -1).
TIE_TOL_BCE = 1e-6
TIE_TOL_KSW = 1e-6

QP_ARMS = (ARM_C, ARM_D)        # Arm A is scored once as the paired reference

REQUIRED_BUNDLE_FILES = (
    "config.json", "manifest.json", "result.json", "log.txt",
    "fold_map.json", "predictions.npz", "training_history.json",
    "checkpoint_table.csv", "trajectory_table.csv",
)
IMMUTABLE_BUNDLE_FILES = ("config.json", "manifest.json", "result.json",
                          "fold_map.json", "predictions.npz",
                          "training_history.json",
                          "checkpoint_table.csv", "trajectory_table.csv")

FIGURE_FILES = (
    "learning_curves_by_schedule.png",
    "pretrain_vs_epoch0.png",
    "best_epoch_distribution.png",
    "alpha_and_effective_residual.png",
    "gradient_update_diagnostics.png",
    "selector_disagreement.png",
    "c_vs_d_by_schedule.png",
    "patient_delta_waterfall.png",
    "decision_matrix.png",
)

# Colour convention used by every figure: epoch -1 is always drawn distinctly.
PRETRAIN_COLOR = "#c0392b"      # red — pre-training checkpoint
EPOCH0_COLOR = "#e67e22"        # orange — first completed epoch
LATER_COLOR = "#2c7fb8"         # blue — epoch >= 1


class Q4PError(RuntimeError):
    """Raised when an input, an assertion, or an artifact contract is violated."""


def run_dir_name(timestamp: str) -> str:
    return f"{timestamp}_{EXPERIMENT_ID}_{RUN_SLUG}"


# ─────────────────────────────────────────────────────────────────────────────
# Dev-side record metrics (selectors) — dev arrays only ever enter here.
# ─────────────────────────────────────────────────────────────────────────────
def _sigmoid(z: np.ndarray) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-np.clip(z, -30.0, 30.0)))


def pooled_bce(logits: np.ndarray, y: np.ndarray) -> float:
    """Mean beat-level BCE over a pooled index set."""
    p = _sigmoid(np.asarray(logits, float))
    yy = np.asarray(y, float)
    eps = 1e-12
    return float(-np.mean(yy * np.log(p + eps) + (1 - yy) * np.log(1 - p + eps)))


def record_balanced_bce(logits: np.ndarray, y: np.ndarray,
                        rid: np.ndarray) -> float:
    """Per-record BCE first, then a simple mean across records.

    This is the patient-level analogue of pooled BCE: a 33k-beat record and a
    2k-beat record contribute equally, exactly as they do in the k-sweep metric.
    """
    recs = sorted(set(int(r) for r in rid))
    vals = []
    for r in recs:
        m = rid == r
        vals.append(pooled_bce(logits[m], y[m]))
    if not vals:
        raise Q4PError("record_balanced_bce needs at least one record")
    return float(np.mean(vals))


def record_ksweep(logits: np.ndarray, y: np.ndarray, rid: np.ndarray) -> float:
    """Mean over records of the Q4-O k-sweep achievement, on the given subset."""
    recs = sorted(set(int(r) for r in rid))
    vals = []
    for r in recs:
        idx = np.where(rid == r)[0]
        vals.append(float(np.mean([achievement_at(logits, idx, y.astype(bool), k)
                                   for k in K_SWEEP])))
    if not vals:
        raise Q4PError("record_ksweep needs at least one record")
    return float(np.mean(vals))


def record_macro_prauc(logits: np.ndarray, y: np.ndarray,
                       rid: np.ndarray) -> Optional[float]:
    from sklearn.metrics import average_precision_score
    recs = sorted(set(int(r) for r in rid))
    vals = []
    for r in recs:
        m = rid == r
        yy = y[m].astype(int)
        if 0 < int(yy.sum()) < len(yy):
            vals.append(float(average_precision_score(yy, logits[m])))
    return float(np.mean(vals)) if vals else None


# ─────────────────────────────────────────────────────────────────────────────
# Checkpoint selection — dev-only by construction.
# ─────────────────────────────────────────────────────────────────────────────
SELECTOR_FIELD = {SEL0: "dev_pooled_bce", SEL1: "dev_record_bce",
                  SEL2: "dev_record_ksweep"}
SELECTOR_MODE = {SEL0: "min", SEL1: "min", SEL2: "max"}
SELECTOR_TOL = {SEL0: TIE_TOL_BCE, SEL1: TIE_TOL_BCE, SEL2: TIE_TOL_KSW}


def select_checkpoint(checkpoints: List[dict], selector: str) -> int:
    """Return the selected ``epoch`` (may be -1) for one trajectory.

    ``checkpoints`` must be ordered by epoch ascending and include epoch -1.
    The scan starts at the earliest checkpoint and a later one wins only by
    improving on the incumbent by more than the pre-registered tolerance, so a
    tie keeps the earliest checkpoint — including the pre-training one.

    Only ``dev_*`` fields are read. Test fields never enter this function's
    decision; a unit test mutates them and asserts the choice is unchanged.
    """
    if selector not in SELECTORS:
        raise Q4PError(f"unknown selector {selector}")
    fld, mode, tol = SELECTOR_FIELD[selector], SELECTOR_MODE[selector], SELECTOR_TOL[selector]
    epochs = [int(c["epoch"]) for c in checkpoints]
    if epochs != sorted(epochs):
        raise Q4PError("checkpoints must be ordered by epoch ascending")
    if PRETRAIN_EPOCH not in epochs:
        raise Q4PError("the pre-training checkpoint (epoch -1) is a mandatory "
                       "candidate for every selector")
    best_epoch, best_val = None, None
    for c in checkpoints:
        v = float(c[fld])
        if not np.isfinite(v):
            raise Q4PError(f"{fld} is not finite at epoch {c['epoch']}")
        if best_val is None:
            best_epoch, best_val = int(c["epoch"]), v
        elif mode == "min" and v < best_val - tol:
            best_epoch, best_val = int(c["epoch"]), v
        elif mode == "max" and v > best_val + tol:
            best_epoch, best_val = int(c["epoch"]), v
    return int(best_epoch)


# ─────────────────────────────────────────────────────────────────────────────
# The diagnostic training loop (new — Q4-O's loop is not modified or reused).
# ─────────────────────────────────────────────────────────────────────────────
def build_optimizer(net, schedule: str):
    """Three param groups (trunk+embed / head / alpha) with per-group LRs.

    For ``S0_original`` all groups carry Q4-O's 1e-3, which is mathematically
    identical to Q4-O's single-group Adam because Adam's update is per-parameter.
    Weight decay is Q4-O's ``DL_WD = 1e-4`` for every group and schedule.
    """
    torch = _require_torch()
    if schedule not in SCHEDULES:
        raise Q4PError(f"unknown schedule {schedule}")
    s = SCHEDULES[schedule]
    trunk_params = list(net.c.parameters()) + list(net.e.parameters())
    head_params = list(net.h.parameters())
    groups = [
        {"params": trunk_params, "lr": s["lr_trunk"], "name": "trunk"},
        {"params": head_params, "lr": s["lr_head"], "name": "head"},
        {"params": [net.alpha], "lr": s["lr_alpha"], "name": "alpha"},
    ]
    return torch.optim.Adam(groups, lr=s["lr_trunk"], weight_decay=DL_WD)


def _grad_norm(params) -> float:
    tot = 0.0
    for p in params:
        if p.grad is not None:
            tot += float(p.grad.detach().pow(2).sum())
    return float(np.sqrt(tot))


def _param_vec(params):
    torch = _require_torch()
    return torch.cat([p.detach().reshape(-1).clone() for p in params])


def diagnostic_train_one_fold(net, X: np.ndarray, offset: np.ndarray,
                              y: np.ndarray, rid: np.ndarray,
                              fit_idx: np.ndarray, dev_idx: np.ndarray,
                              test_idx: np.ndarray, seed: int, device: str,
                              schedule: str, epochs: int = N_EPOCHS,
                              batch: int = DL_BATCH,
                              log: Optional[RunLog] = None) -> Dict[str, object]:
    """Train one (arm, schedule, seed, fold) trajectory and record EVERY checkpoint.

    Guarantees enforced here (and unit-tested):
      * epoch -1 is evaluated BEFORE any optimizer step: alpha == 0 exactly, its
        output equals the offset, and its optimizer_steps field is 0;
      * all ``epochs`` epochs run — nothing stops the optimizer early;
      * minibatch order depends only on ``seed`` (identical across schedules);
      * dev metrics never see a test label; test logits are recorded per checkpoint
        for the exploratory trajectory but are never read by any selector.
    """
    torch = _require_torch()
    import torch.nn as nn

    net = net.to(device)
    opt = build_optimizer(net, schedule)
    bce = nn.BCEWithLogitsLoss()
    wmu, wsd = _chunked_mean_std(X, fit_idx)

    def batch_tensors(idx):
        x = torch.tensor((X[idx] - wmu) / wsd, device=device)
        o = torch.tensor(offset[idx].astype("float32"), device=device)
        return x, o

    def eval_split(idx) -> Tuple[np.ndarray, np.ndarray]:
        """(logits, alpha*residual) over ``idx`` in eval mode, batched."""
        net.eval()
        logits = np.empty(len(idx), float)
        eff = np.empty(len(idx), float)
        a = float(net.alpha.detach().cpu().numpy()[0])
        with torch.no_grad():
            for b0 in range(0, len(idx), 4096):
                sl = slice(b0, b0 + 4096)
                bi = idx[sl]
                x, o = batch_tensors(bi)
                r = net.residual(x)
                logits[sl] = (o + net.alpha * r).detach().cpu().numpy()
                eff[sl] = (a * r.detach().cpu().numpy())
        return logits, eff

    def checkpoint_record(epoch: int, n_steps: int, train_loss: Optional[float],
                          wall_s: float) -> dict:
        dev_logits, dev_eff = eval_split(dev_idx)
        te_logits, _ = eval_split(test_idx)
        a = float(net.alpha.detach().cpu().numpy()[0])
        off_dev = offset[dev_idx].astype(float)
        if np.std(dev_eff) > 0 and np.std(off_dev) > 0:
            corr = float(np.corrcoef(off_dev, dev_eff)[0, 1])
        else:
            corr = 0.0
        rec = {
            "epoch": int(epoch),
            "optimizer_steps": int(n_steps),
            "train_pooled_bce": (None if train_loss is None else float(train_loss)),
            "dev_pooled_bce": pooled_bce(dev_logits, y[dev_idx]),
            "dev_record_bce": record_balanced_bce(dev_logits, y[dev_idx], rid[dev_idx]),
            "dev_record_ksweep": record_ksweep(dev_logits, y[dev_idx], rid[dev_idx]),
            "dev_record_prauc": record_macro_prauc(dev_logits, y[dev_idx], rid[dev_idx]),
            "alpha": a,
            "abs_alpha": abs(a),
            "eff_residual_mean": float(np.mean(dev_eff)),
            "eff_residual_sd": float(np.std(dev_eff)),
            "eff_residual_mean_abs": float(np.mean(np.abs(dev_eff))),
            "eff_residual_p95_abs": float(np.percentile(np.abs(dev_eff), 95)),
            "corr_offset_eff_residual": corr,
            "wall_s": float(wall_s),
        }
        return rec, te_logits

    # ── epoch -1: the true pre-training checkpoint ──────────────────────────
    a0 = float(net.alpha.detach().cpu().numpy()[0])
    if a0 != 0.0:
        raise Q4PError(f"pre-training alpha must be exactly 0, got {a0!r}")
    t0 = time.time()
    net.eval()
    with torch.no_grad():                        # pre-training train BCE: eval pass
        tot, cnt = 0.0, 0
        for b0 in range(0, len(fit_idx), 4096):
            bi = fit_idx[b0:b0 + 4096]
            x, o = batch_tensors(bi)
            yy = torch.tensor(y[bi].astype("float32"), device=device)
            tot += float(bce(net(x, o), yy)) * len(bi)
            cnt += len(bi)
    rec, te_logits = checkpoint_record(PRETRAIN_EPOCH, 0, tot / max(1, cnt),
                                       time.time() - t0)
    pre_dev_logits, _ = eval_split(dev_idx)
    if not np.allclose(pre_dev_logits, offset[dev_idx], atol=1e-5):
        raise Q4PError("epoch -1 output does not equal the morphology offset — "
                       "the pre-training checkpoint is not what it claims to be")
    checkpoints = [rec]
    test_logits_by_epoch = {PRETRAIN_EPOCH: te_logits}

    # ── the fixed 24-epoch trajectory ───────────────────────────────────────
    # Minibatch order comes from a RandomState seeded by `seed` only, so two
    # schedules trained with the same seed see identical minibatch sequences.
    rng = np.random.RandomState(seed)
    grad_log: List[dict] = []
    n_steps = 0
    trunk_params = list(net.c.parameters()) + list(net.e.parameters())
    head_params = list(net.h.parameters())

    for ep in range(epochs):
        t0 = time.time()
        net.train()
        perm = rng.permutation(len(fit_idx))
        train_tot, train_cnt = 0.0, 0
        for b0 in range(0, len(fit_idx), batch):
            bi = fit_idx[perm[b0:b0 + batch]]
            x, o = batch_tensors(bi)
            yy = torch.tensor(y[bi].astype("float32"), device=device)
            opt.zero_grad()
            loss = bce(net(x, o), yy)
            loss.backward()
            if n_steps < GRAD_LOG_STEPS:
                pre_alpha = _param_vec([net.alpha])
                pre_head = _param_vec(head_params)
                pre_trunk = _param_vec(trunk_params)
                g = {"step": int(n_steps),
                     "grad_alpha": _grad_norm([net.alpha]),
                     "grad_head": _grad_norm(head_params),
                     "grad_trunk": _grad_norm(trunk_params)}
            opt.step()
            if n_steps < GRAD_LOG_STEPS:
                g["upd_alpha"] = float((_param_vec([net.alpha]) - pre_alpha).norm())
                g["upd_head"] = float((_param_vec(head_params) - pre_head).norm())
                g["upd_trunk"] = float((_param_vec(trunk_params) - pre_trunk).norm())
                grad_log.append(g)
            n_steps += 1
            train_tot += float(loss.detach()) * len(bi)
            train_cnt += len(bi)
        rec, te_logits = checkpoint_record(ep, n_steps,
                                           train_tot / max(1, train_cnt),
                                           time.time() - t0)
        checkpoints.append(rec)
        test_logits_by_epoch[ep] = te_logits

    if len(checkpoints) != epochs + 1:
        raise Q4PError(f"expected {epochs + 1} checkpoints (incl. epoch -1), "
                       f"got {len(checkpoints)} — did something stop the loop?")

    selected = {sel: select_checkpoint(checkpoints, sel) for sel in SELECTORS}
    fit_prev = float(np.mean(y[fit_idx]))
    dev_prev = float(np.mean(y[dev_idx]))
    return {
        "schedule": schedule,
        "seed": int(seed),
        "checkpoints": checkpoints,
        "grad_log": grad_log,
        "selected": selected,
        "test_logits_by_epoch": test_logits_by_epoch,
        "n_fit": int(len(fit_idx)), "n_dev": int(len(dev_idx)),
        "n_test": int(len(test_idx)),
        "fit_prevalence": fit_prev, "dev_prevalence": dev_prev,
        "n_fit_record": int(len(set(rid[fit_idx].tolist()))),
        "n_dev_record": int(len(set(rid[dev_idx].tolist()))),
    }


# ─────────────────────────────────────────────────────────────────────────────
# Pre-registered decision tree.
# ─────────────────────────────────────────────────────────────────────────────
DECISION_BRANCHES = (
    "B1_immediately_harmful_or_no_signal",
    "B2_first_epoch_then_overfit",
    "B3_lr_or_alpha_overshoot",
    "B4_selector_mismatch",
    "B5_schedule_artifact_not_waveform_specific",
    "B6_real_waveform_residual_candidate",
)


def evaluate_decision_tree(summary: Dict[str, object]) -> Dict[str, object]:
    """Apply the six pre-registered branches to a measured summary.

    ``summary`` is produced by ``run_diagnostic`` (or a test fixture) and holds
    only measured quantities. Multiple branches may fire; none may be forced.
    Nothing here invents a value — if a needed field is missing the branch is
    marked ``not evaluable`` instead of guessed.
    """
    fired: Dict[str, dict] = {}

    def get(path, default=None):
        node = summary
        for k in path:
            if not isinstance(node, dict) or k not in node:
                return default
            node = node[k]
        return node

    # B1 — epoch -1 best for most of Arm C, and C-D shows no improvement.
    p_pre = get(("best_epoch_dist", ARM_C, "S0_original", PRIMARY_SELECTOR,
                 "p_pretrain"))
    cd_mean = get(("contrasts", "S0_original", PRIMARY_SELECTOR, "C_minus_D",
                   "record_bootstrap", "mean"))
    if p_pre is None or cd_mean is None:
        fired["B1_immediately_harmful_or_no_signal"] = {"evaluable": False}
    else:
        fired["B1_immediately_harmful_or_no_signal"] = {
            "evaluable": True, "fires": bool(p_pre >= 0.5 and cd_mean <= 0.0),
            "p_pretrain": p_pre, "c_minus_d_mean": cd_mean}

    # B2 — epoch 0 beats -1 on dev, train loss keeps falling, record-balanced dev
    # worsens afterwards (majority of C trajectories under S0).
    b2 = get(("trajectory_flags", ARM_C, "S0_original"))
    if b2 is None:
        fired["B2_first_epoch_then_overfit"] = {"evaluable": False}
    else:
        fired["B2_first_epoch_then_overfit"] = {
            "evaluable": True,
            "fires": bool(b2.get("frac_epoch0_better_than_pretrain", 0) >= 0.5
                          and b2.get("frac_train_loss_decreasing", 0) >= 0.5
                          and b2.get("frac_dev_record_bce_worsens_later", 0) >= 0.5),
            **b2}

    # B3 — under S1 or S2 the best epoch moves later AND dev+test C-D improve vs S0.
    b3_detail = {}
    b3_fires = False
    for sch in ("S1_global_low", "S2_alpha_low"):
        later = get(("best_epoch_shift", ARM_C, sch, PRIMARY_SELECTOR, "moved_later"))
        dev_gain = get(("schedule_dev_gain", ARM_C, sch, PRIMARY_SELECTOR))
        cd_s = get(("contrasts", sch, PRIMARY_SELECTOR, "C_minus_D",
                    "record_bootstrap", "mean"))
        cd_0 = get(("contrasts", "S0_original", PRIMARY_SELECTOR, "C_minus_D",
                    "record_bootstrap", "mean"))
        if None in (later, dev_gain, cd_s, cd_0):
            b3_detail[sch] = {"evaluable": False}
            continue
        f = bool(later and dev_gain > 0 and cd_s > cd_0)
        b3_detail[sch] = {"evaluable": True, "fires": f, "moved_later": later,
                          "dev_gain": dev_gain, "cd_schedule": cd_s, "cd_s0": cd_0}
        b3_fires = b3_fires or f
    fired["B3_lr_or_alpha_overshoot"] = {
        "evaluable": any(v.get("evaluable") for v in b3_detail.values()),
        "fires": b3_fires, "by_schedule": b3_detail}

    # B4 — SEL1 consistently beats SEL0 on patient-level dev AND paired outer-test.
    b4 = get(("selector_comparison", ARM_C))
    if b4 is None:
        fired["B4_selector_mismatch"] = {"evaluable": False}
    else:
        fired["B4_selector_mismatch"] = {
            "evaluable": True,
            "fires": bool(b4.get("sel1_beats_sel0_dev", False)
                          and b4.get("sel1_beats_sel0_test", False)),
            **b4}

    # B5 — schedule improvements appear equally in C and D and C-D vanishes.
    b5 = get(("schedule_symmetry",))
    if b5 is None:
        fired["B5_schedule_artifact_not_waveform_specific"] = {"evaluable": False}
    else:
        fired["B5_schedule_artifact_not_waveform_specific"] = {
            "evaluable": True,
            "fires": bool(b5.get("gains_similar_c_and_d", False)
                          and b5.get("c_minus_d_vanishes", False)),
            **b5}

    # B6 — C consistently beats D with CI, seed direction, and lower tail improving.
    b6 = get(("c_over_d_consistency",))
    if b6 is None:
        fired["B6_real_waveform_residual_candidate"] = {"evaluable": False}
    else:
        fired["B6_real_waveform_residual_candidate"] = {
            "evaluable": True,
            "fires": bool(b6.get("ci_low_gt_0", False)
                          and b6.get("seed_direction_stable", False)
                          and b6.get("lower_tail_improves", False)),
            **b6}

    firing = [b for b in DECISION_BRANCHES
              if fired.get(b, {}).get("fires") is True]
    if len(firing) == 1:
        verdict = firing[0]
    elif len(firing) > 1:
        verdict = "MULTIPLE_CAUSES: " + " + ".join(firing)
    else:
        verdict = "UNDECIDED"
    return {"branches": fired, "firing": firing, "verdict": verdict,
            "note": ("Pre-registered tree. Mixed evidence is reported as "
                     "MULTIPLE_CAUSES or UNDECIDED — never forced into one branch.")}


# ─────────────────────────────────────────────────────────────────────────────
# Aggregation helpers (measured arrays in, summaries out — nothing invented).
# ─────────────────────────────────────────────────────────────────────────────
def per_record_ksw_scores(scores: np.ndarray, cohort: Cohort,
                          records: Sequence[int]) -> Dict[int, float]:
    return {int(r): float(np.mean([achievement_at(scores, cohort.idx_of[int(r)],
                                                  cohort.y, k) for k in K_SWEEP]))
            for r in records}


def assemble_test_scores(fold_results: Dict[int, dict], cohort: Cohort,
                         fold_map: Dict[int, int], selector: str) -> np.ndarray:
    """Stitch each outer fold's SELECTED-checkpoint test logits into one array."""
    out = np.full(cohort.n, np.nan)
    records = sorted(fold_map)
    for f, res in fold_results.items():
        te_recs = [r for r in records if fold_map[r] == f]
        te_idx = samples_of(cohort, te_recs)
        ep = res["selected"][selector]
        out[te_idx] = res["test_logits_by_epoch"][ep]
    scored = samples_of(cohort, records)
    assert_finite(out[scored], f"assembled test scores ({selector})")
    return out


def _traj_flags(fold_results_by_seed: Dict[int, Dict[int, dict]]) -> dict:
    """Trajectory-shape fractions used by decision branch B2."""
    n = 0
    e0_better = 0
    train_dec = 0
    dev_worse_later = 0
    for seed_res in fold_results_by_seed.values():
        for res in seed_res.values():
            cps = {c["epoch"]: c for c in res["checkpoints"]}
            n += 1
            if cps[0]["dev_pooled_bce"] < cps[PRETRAIN_EPOCH]["dev_pooled_bce"]:
                e0_better += 1
            tl = [c["train_pooled_bce"] for c in res["checkpoints"]
                  if c["epoch"] >= 0]
            if len(tl) >= 2 and tl[-1] < tl[0]:
                train_dec += 1
            rb = [c["dev_record_bce"] for c in res["checkpoints"] if c["epoch"] >= 0]
            if len(rb) >= 2 and min(rb[1:]) > rb[0]:
                dev_worse_later += 1
    if n == 0:
        raise Q4PError("no trajectories to summarise")
    return {"n": n,
            "frac_epoch0_better_than_pretrain": e0_better / n,
            "frac_train_loss_decreasing": train_dec / n,
            "frac_dev_record_bce_worsens_later": dev_worse_later / n}


def _best_epoch_dist(fold_results_by_seed: Dict[int, Dict[int, dict]],
                     selector: str) -> dict:
    eps = [res["selected"][selector]
           for seed_res in fold_results_by_seed.values()
           for res in seed_res.values()]
    n = len(eps)
    return {"n": n,
            "p_pretrain": sum(1 for e in eps if e == PRETRAIN_EPOCH) / n,
            "p_epoch0": sum(1 for e in eps if e == 0) / n,
            "p_later": sum(1 for e in eps if e > 0) / n,
            "epochs": sorted(eps)}


# ─────────────────────────────────────────────────────────────────────────────
# The full diagnostic run (CPU smoke or the future GPU run — NOT executed as part
# of the design task).
# ─────────────────────────────────────────────────────────────────────────────
def run_diagnostic(cohort: Cohort, provenance: Dict[str, object], out_dir: str,
                   seeds: Sequence[int] = TRAIN_SEEDS, epochs: int = N_EPOCHS,
                   batch: int = DL_BATCH, n_boot: int = 2000,
                   device: Optional[str] = None, smoke: bool = False,
                   log: Optional[RunLog] = None) -> Dict[str, object]:
    """Run Arms C and D under all schedules, all selectors, and write the bundle.

    Everything pre-registered in the spec is fixed here: fold map (Q4-O's,
    recomputed by the same deterministic function on the same cohort), seeds,
    24-epoch trajectories, three schedules, three selectors, epoch -1 candidacy.
    Outer-test labels are never read before checkpoints are fixed by dev.
    """
    torch = _require_torch()
    log = log or RunLog()
    if device is None:
        device = "cuda" if torch.cuda.is_available() else "cpu"
    os.makedirs(out_dir, exist_ok=True)
    t_start = time.time()

    log(f"{EXPERIMENT_ID} / {ARM_ID} diagnostic — device {device}, "
        f"{len(seeds)} seeds, {epochs} epochs/trajectory, smoke={smoke}")

    rec_ok = scorable_records(cohort)
    burden = record_burden(cohort, rec_ok)
    fold_map = make_fold_map(rec_ok, burden)
    assert_fold_map_partition(fold_map, rec_ok, N_OUTER_FOLDS)
    records = sorted(fold_map)

    feats = build_features(cohort, with_comb=False)
    offsets = cross_fitted_offsets(feats.morph, cohort, fold_map, burden=burden,
                                   log=log)
    arm_a_scores = run_logistic_arm(feats.morph, cohort, fold_map)
    ksw_a = per_record_ksw_scores(arm_a_scores, cohort, records)

    X_c = current_beat_input(cohort)
    shuffled, perm_rule = shuffle_waveforms_within_record(cohort)
    X_d = current_beat_input(cohort, beat=shuffled)
    arm_inputs = {ARM_C: X_c, ARM_D: X_d}

    # arm -> schedule -> seed -> fold -> trajectory result
    all_results: Dict[str, Dict[str, Dict[int, Dict[int, dict]]]] = {
        arm: {sch: {} for sch in SCHEDULE_NAMES} for arm in QP_ARMS}
    history_out: List[dict] = []

    n_jobs = len(QP_ARMS) * len(SCHEDULE_NAMES) * len(seeds) * N_OUTER_FOLDS
    done = 0
    for arm in QP_ARMS:
        X = arm_inputs[arm]
        for seed in seeds:
            for f in range(N_OUTER_FOLDS):
                te_recs = [r for r in records if fold_map[r] == f]
                tr_recs = [r for r in records if fold_map[r] != f]
                assert_disjoint(tr_recs, te_recs, f"{arm} outer fold {f}")
                fit_recs, dv_recs = dev_records(tr_recs, burden)
                assert_disjoint(fit_recs, dv_recs, f"{arm} fold {f} fit/dev")
                assert_disjoint(fit_recs + dv_recs, te_recs,
                                f"{arm} fold {f} train/test")
                fit_idx = samples_of(cohort, fit_recs)
                dev_idx = samples_of(cohort, dv_recs)
                te_idx = samples_of(cohort, te_recs)
                for sch in SCHEDULE_NAMES:
                    # Paired initialisation: the SAME (seed, fold) determinism call
                    # precedes net construction for every schedule, so initial
                    # parameters are identical across schedules; and the loop draws
                    # minibatch order from `seed + 1009*f` only.
                    set_determinism(seed + 1009 * f)
                    net = build_residual_net(X.shape[1], init="normal")
                    res = diagnostic_train_one_fold(
                        net, X, offsets[f], cohort.y, cohort.rid,
                        fit_idx, dev_idx, te_idx, seed + 1009 * f, device,
                        sch, epochs=epochs, batch=batch, log=log)
                    res["fold"] = f
                    all_results[arm][sch].setdefault(seed, {})[f] = res
                    history_out.append({
                        "arm": arm, "schedule": sch, "seed": int(seed), "fold": f,
                        "selected": res["selected"],
                        "checkpoints": res["checkpoints"],
                        "grad_log_first_steps": res["grad_log"],
                        "n_fit": res["n_fit"], "n_dev": res["n_dev"],
                        "n_test": res["n_test"],
                        "fit_prevalence": res["fit_prevalence"],
                        "dev_prevalence": res["dev_prevalence"],
                    })
                    done += 1
                    sel = res["selected"]
                    log(f"  [{done}/{n_jobs}] {arm} {sch} seed {seed} fold {f}: "
                        f"SEL0 ep {sel[SEL0]} · SEL1 ep {sel[SEL1]} · "
                        f"SEL2 ep {sel[SEL2]}")

    # ── dev-only selection is now frozen; outer-test evaluation begins ───────
    log("all trajectories complete — assembling selected-checkpoint test scores")
    contrasts: Dict[str, dict] = {}
    arm_scores_store: Dict[str, Dict[str, Dict[str, np.ndarray]]] = {}
    best_epoch_dist: Dict[str, dict] = {arm: {} for arm in QP_ARMS}
    for arm in QP_ARMS:
        arm_scores_store[arm] = {}
        for sch in SCHEDULE_NAMES:
            arm_scores_store[arm][sch] = {}
            best_epoch_dist[arm][sch] = {
                sel: _best_epoch_dist(all_results[arm][sch], sel)
                for sel in SELECTORS}
            for sel in SELECTORS:
                per_seed = {}
                for seed in seeds:
                    sc = assemble_test_scores(all_results[arm][sch][seed],
                                              cohort, fold_map, sel)
                    per_seed[seed] = sc
                arm_scores_store[arm][sch][sel] = per_seed

    def ksw_by_seed(arm, sch, sel):
        return {seed: per_record_ksw_scores(arm_scores_store[arm][sch][sel][seed],
                                            cohort, records)
                for seed in seeds}

    for sch in SCHEDULE_NAMES:
        contrasts[sch] = {}
        for sel in SELECTORS:
            kc = ksw_by_seed(ARM_C, sch, sel)
            kd = ksw_by_seed(ARM_D, sch, sel)
            k_mean = lambda kk: {r: float(np.mean([kk[s][r] for s in seeds]))
                                 for r in records}
            kcm, kdm = k_mean(kc), k_mean(kd)
            def boot(x, yref):
                diff = {r: x[r] - yref[r] for r in records}
                return paired_record_bootstrap(diff, n_boot=n_boot)
            def hier(kk, yref_by_seed):
                d = {r: {s: kk[s][r] - yref_by_seed(s)[r] for s in seeds}
                     for r in records}
                return hierarchical_bootstrap(d, n_boot=n_boot)
            by_seed_ca = [float(np.mean([kc[s][r] - ksw_a[r] for r in records]))
                          for s in seeds]
            by_seed_cd = [float(np.mean([kc[s][r] - kd[s][r] for r in records]))
                          for s in seeds]
            contrasts[sch][sel] = {
                "C_minus_A": {"record_bootstrap": boot(kcm, ksw_a),
                              "hierarchical_bootstrap": hier(kc, lambda s: ksw_a),
                              "by_seed": by_seed_ca},
                "D_minus_A": {"record_bootstrap": boot(kdm, ksw_a),
                              "by_seed": [float(np.mean([kd[s][r] - ksw_a[r]
                                                         for r in records]))
                                          for s in seeds]},
                "C_minus_D": {"record_bootstrap": boot(kcm, kdm),
                              "hierarchical_bootstrap": hier(kc, lambda s: kd[s]),
                              "by_seed": by_seed_cd},
                "ksw_mean": {"A": float(np.mean(list(ksw_a.values()))),
                             "C": float(np.mean(list(kcm.values()))),
                             "D": float(np.mean(list(kdm.values())))},
                "p10": {"A": float(np.percentile(list(ksw_a.values()), 10)),
                        "C": float(np.percentile(list(kcm.values()), 10)),
                        "D": float(np.percentile(list(kdm.values()), 10))},
            }

    # Derived summaries for the decision tree.
    def _sched_shift(arm, sch, sel):
        e0 = best_epoch_dist[arm]["S0_original"][sel]
        es = best_epoch_dist[arm][sch][sel]
        return {"moved_later": bool(np.mean(es["epochs"]) > np.mean(e0["epochs"])),
                "mean_epoch_s0": float(np.mean(e0["epochs"])),
                "mean_epoch": float(np.mean(es["epochs"]))}

    def _sched_dev_gain(arm, sch, sel):
        """Mean selected-checkpoint dev metric improvement vs S0 (dev only)."""
        fld = SELECTOR_FIELD[sel]
        sign = -1.0 if SELECTOR_MODE[sel] == "min" else 1.0
        def mean_sel_dev(schedule):
            vals = []
            for seed_res in all_results[arm][schedule].values():
                for res in seed_res.values():
                    ep = res["selected"][sel]
                    c = next(c for c in res["checkpoints"] if c["epoch"] == ep)
                    vals.append(c[fld])
            return float(np.mean(vals))
        return float(sign * (mean_sel_dev(sch) - mean_sel_dev("S0_original")))

    selector_comparison = {}
    for arm in (ARM_C,):
        def mean_sel_dev_metric(sel):
            vals = []
            for sch in ("S0_original",):
                for seed_res in all_results[arm][sch].values():
                    for res in seed_res.values():
                        ep = res["selected"][sel]
                        c = next(c for c in res["checkpoints"]
                                 if c["epoch"] == ep)
                        vals.append(c["dev_record_bce"])
            return float(np.mean(vals))
        t_sel1 = contrasts["S0_original"][SEL1]["C_minus_A"]["record_bootstrap"]["mean"]
        t_sel0 = contrasts["S0_original"][SEL0]["C_minus_A"]["record_bootstrap"]["mean"]
        selector_comparison[arm] = {
            "dev_record_bce_sel0": mean_sel_dev_metric(SEL0),
            "dev_record_bce_sel1": mean_sel_dev_metric(SEL1),
            "sel1_beats_sel0_dev": bool(mean_sel_dev_metric(SEL1)
                                        < mean_sel_dev_metric(SEL0)),
            "test_c_minus_a_sel0": t_sel0,
            "test_c_minus_a_sel1": t_sel1,
            "sel1_beats_sel0_test": bool(t_sel1 > t_sel0),
        }

    cd0 = contrasts["S0_original"][PRIMARY_SELECTOR]["C_minus_D"]
    c_over_d = {
        "ci_low_gt_0": bool(cd0["record_bootstrap"]["ci_low"] > 0),
        "seed_direction_stable": bool(sum(1 for v in cd0["by_seed"] if v > 0)
                                      >= max(1, len(seeds) - 1)),
        "lower_tail_improves": bool(
            contrasts["S0_original"][PRIMARY_SELECTOR]["p10"]["C"]
            >= contrasts["S0_original"][PRIMARY_SELECTOR]["p10"]["D"]),
        "c_minus_d": cd0["record_bootstrap"],
    }

    gains_c = [_sched_dev_gain(ARM_C, sch, PRIMARY_SELECTOR)
               for sch in ("S1_global_low", "S2_alpha_low")]
    gains_d = [_sched_dev_gain(ARM_D, sch, PRIMARY_SELECTOR)
               for sch in ("S1_global_low", "S2_alpha_low")]
    best_cd = max(contrasts[sch][PRIMARY_SELECTOR]["C_minus_D"]
                  ["record_bootstrap"]["mean"] for sch in SCHEDULE_NAMES)
    schedule_symmetry = {
        "dev_gains_c": gains_c, "dev_gains_d": gains_d,
        "gains_similar_c_and_d": bool(
            all(abs(gc - gd) <= max(1e-4, 0.5 * max(abs(gc), abs(gd), 1e-12))
                for gc, gd in zip(gains_c, gains_d))
            and any(g > 0 for g in gains_c + gains_d)),
        "c_minus_d_vanishes": bool(abs(best_cd) < 1e-3),
        "best_c_minus_d_over_schedules": best_cd,
    }

    summary = {
        "best_epoch_dist": best_epoch_dist,
        "contrasts": contrasts,
        "trajectory_flags": {ARM_C: {sch: _traj_flags(all_results[ARM_C][sch])
                                     for sch in SCHEDULE_NAMES}},
        "best_epoch_shift": {ARM_C: {sch: {sel: _sched_shift(ARM_C, sch, sel)
                                           for sel in SELECTORS}
                                     for sch in SCHEDULE_NAMES}},
        "schedule_dev_gain": {ARM_C: {sch: {sel: _sched_dev_gain(ARM_C, sch, sel)
                                            for sel in SELECTORS}
                                      for sch in SCHEDULE_NAMES}},
        "selector_comparison": selector_comparison,
        "schedule_symmetry": schedule_symmetry,
        "c_over_d_consistency": c_over_d,
    }
    decision = evaluate_decision_tree(summary)
    log(f"decision tree verdict: {decision['verdict']}")

    result = {
        "experiment_id": EXPERIMENT_ID,
        "arm_id": ARM_ID,
        "status": STATUS if smoke else "MEASURED",
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "smoke": bool(smoke),
        "primary_selector": PRIMARY_SELECTOR,
        "n_epochs": int(epochs),
        "schedules": SCHEDULES,
        "selectors": list(SELECTORS),
        "tie_tolerances": {"bce": TIE_TOL_BCE, "ksweep": TIE_TOL_KSW},
        "summary": summary,
        "decision_tree": decision,
        "note": ("Exploratory diagnostic of Q4-O's best_epoch=0. The exploratory "
                 "test trajectories are recorded but never used for selection or "
                 "baseline promotion. No headline is picked as max-over-schedules."
                 + (" SYNTHETIC smoke run — no scientific meaning." if smoke else "")),
    }
    config = {
        "experiment_id": EXPERIMENT_ID, "arm_id": ARM_ID, "run_slug": RUN_SLUG,
        "n_outer_folds": N_OUTER_FOLDS, "seeds": [int(s) for s in seeds],
        "epochs": int(epochs), "batch": int(batch), "weight_decay": DL_WD,
        "schedules": SCHEDULES, "selectors": list(SELECTORS),
        "tie_tolerances": {"bce": TIE_TOL_BCE, "ksweep": TIE_TOL_KSW},
        "pretrain_epoch": PRETRAIN_EPOCH, "grad_log_steps": GRAD_LOG_STEPS,
        "k_sweep": list(K_SWEEP),
        "waveform_permutation": perm_rule,
        "split": "frozen Q4-O record-burden stratification (same function, same cohort)",
        "arms": list(QP_ARMS) + [ARM_A + " (paired reference, logistic)"],
    }
    manifest = {
        "data": provenance,
        "git_commit_sha": git_commit_sha(),
        "packages": package_versions(),
        "gpu": gpu_info(),
        "device": device,
        "n_record_scorable": len(records),
        "scorable_records": records,
        "record_burden": {int(r): burden[r] for r in records},
        "fold_records": {f: sorted(r for r in records if fold_map[r] == f)
                         for f in range(N_OUTER_FOLDS)},
        "wall_time_s": None,   # filled below, before writing
    }

    _write_bundle(out_dir, cohort, fold_map, records, seeds, config, manifest,
                  result, history_out, arm_scores_store, arm_a_scores, log,
                  t_start)
    _write_figures_and_report(out_dir, result, history_out, cohort, records,
                              seeds, log)
    verify_bundle(out_dir)
    log(f"bundle complete: {out_dir}")
    return result


def _write_bundle(out_dir, cohort, fold_map, records, seeds, config, manifest,
                  result, history_out, arm_scores_store, arm_a_scores, log,
                  t_start) -> None:
    import csv
    manifest["wall_time_s"] = float(time.time() - t_start)
    scored = samples_of(cohort, records)
    mask = np.zeros(cohort.n, bool)
    mask[scored] = True
    fold_arr = np.full(cohort.n, -1, int)
    for r, f in fold_map.items():
        fold_arr[cohort.idx_of[int(r)]] = f

    npz_payload = {
        "seeds": np.array([int(s) for s in seeds]),
        "record_id": cohort.rid,
        "sample_id": cohort.sample_id,
        "y_true": cohort.y,
        "fold": fold_arr,
        "scored_mask": mask,
        "logit_morph_baseline": arm_a_scores,
    }
    for arm in QP_ARMS:
        for sch in SCHEDULE_NAMES:
            for sel in SELECTORS:
                per_seed = arm_scores_store[arm][sch][sel]
                npz_payload[f"logit_{arm}__{sch}__{sel}"] = np.stack(
                    [per_seed[s] for s in seeds])
    np.savez_compressed(os.path.join(out_dir, "predictions.npz"), **npz_payload)

    for arm in QP_ARMS:
        for sch in SCHEDULE_NAMES:
            for sel in SELECTORS:
                d = os.path.join(out_dir, "arms", arm, sch, sel)
                os.makedirs(d, exist_ok=True)
                per_seed = arm_scores_store[arm][sch][sel]
                probs = _sigmoid(np.stack([per_seed[s] for s in seeds]))
                np.save(os.path.join(d, "probs.npy"), probs)

    with open(os.path.join(out_dir, "fold_map.json"), "w", encoding="utf-8") as fh:
        json.dump({"record_to_fold": {str(r): int(f) for r, f in fold_map.items()}},
                  fh, indent=1)
    for name, obj in (("config.json", config), ("manifest.json", manifest),
                      ("result.json", result)):
        with open(os.path.join(out_dir, name), "w", encoding="utf-8") as fh:
            json.dump(_json_safe(obj), fh, ensure_ascii=False, indent=1)
    with open(os.path.join(out_dir, "training_history.json"), "w",
              encoding="utf-8") as fh:
        json.dump(_json_safe(history_out), fh, ensure_ascii=False, indent=1)

    cp_cols = ["arm", "schedule", "seed", "fold", "epoch", "optimizer_steps",
               "train_pooled_bce", "dev_pooled_bce", "dev_record_bce",
               "dev_record_ksweep", "dev_record_prauc", "alpha", "abs_alpha",
               "eff_residual_mean", "eff_residual_sd", "eff_residual_mean_abs",
               "eff_residual_p95_abs", "corr_offset_eff_residual", "wall_s"]
    with open(os.path.join(out_dir, "trajectory_table.csv"), "w", newline="",
              encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(cp_cols)
        for h in history_out:
            for c in h["checkpoints"]:
                w.writerow([h["arm"], h["schedule"], h["seed"], h["fold"]]
                           + [c.get(k) for k in cp_cols[4:]])
    with open(os.path.join(out_dir, "checkpoint_table.csv"), "w", newline="",
              encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["arm", "schedule", "seed", "fold", "selector",
                    "selected_epoch"])
        for h in history_out:
            for sel, ep in h["selected"].items():
                w.writerow([h["arm"], h["schedule"], h["seed"], h["fold"],
                            sel, ep])
    with open(os.path.join(out_dir, "log.txt"), "w", encoding="utf-8") as fh:
        fh.write(log.text())


def bundle_fingerprint(run_dir: str) -> Dict[str, str]:
    """SHA256 of every measured file reporting must never touch."""
    out: Dict[str, str] = {}
    for name in IMMUTABLE_BUNDLE_FILES:
        p = os.path.join(run_dir, name)
        if os.path.exists(p):
            out[name] = sha256_file(p)
    arms_dir = os.path.join(run_dir, "arms")
    if os.path.isdir(arms_dir):
        for root, _dirs, files in os.walk(arms_dir):
            for f in sorted(files):
                p = os.path.join(root, f)
                out[os.path.relpath(p, run_dir)] = sha256_file(p)
    return out


def verify_bundle(out_dir: str) -> None:
    missing = [f for f in REQUIRED_BUNDLE_FILES
               if not os.path.exists(os.path.join(out_dir, f))]
    if missing:
        raise Q4PError(f"incomplete bundle — missing {missing}")
    with np.load(os.path.join(out_dir, "predictions.npz")) as npz:
        keys = set(npz.files)
        need = {"seeds", "record_id", "sample_id", "y_true", "fold",
                "scored_mask", "logit_morph_baseline"}
        if not need <= keys:
            raise Q4PError(f"predictions.npz missing {sorted(need - keys)}")
        for arm in QP_ARMS:
            for sch in SCHEDULE_NAMES:
                for sel in SELECTORS:
                    k = f"logit_{arm}__{sch}__{sel}"
                    if k not in keys:
                        raise Q4PError(f"predictions.npz missing {k}")
    hist = json.load(open(os.path.join(out_dir, "training_history.json"),
                          encoding="utf-8"))
    for h in hist:
        eps = [c["epoch"] for c in h["checkpoints"]]
        if PRETRAIN_EPOCH not in eps:
            raise Q4PError("a trajectory is missing the epoch -1 checkpoint")
        pre = next(c for c in h["checkpoints"] if c["epoch"] == PRETRAIN_EPOCH)
        if pre["optimizer_steps"] != 0 or pre["alpha"] != 0.0:
            raise Q4PError("epoch -1 must have 0 optimizer steps and alpha == 0")


# ─────────────────────────────────────────────────────────────────────────────
# Figures + report. Presentation only — fingerprinted before and after.
# ─────────────────────────────────────────────────────────────────────────────
def _plt():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    return plt


def _save(fig, path: str) -> str:
    fig.tight_layout()
    fig.savefig(path, dpi=130, bbox_inches="tight")
    _plt().close(fig)
    return path


def _hist_by(history: List[dict], **want) -> List[dict]:
    return [h for h in history
            if all(h.get(k) == v for k, v in want.items())]


def _epoch_axis_note(ax) -> None:
    ax.axvline(-1, color=PRETRAIN_COLOR, lw=1.0, ls="--", alpha=0.8)
    ax.axvline(0, color=EPOCH0_COLOR, lw=1.0, ls="--", alpha=0.8)


def _write_figures_and_report(out_dir: str, result: dict, history: List[dict],
                              cohort: Cohort, records: List[int],
                              seeds: Sequence[int], log: RunLog) -> None:
    before = bundle_fingerprint(out_dir)
    fig_dir = os.path.join(out_dir, "figures")
    os.makedirs(fig_dir, exist_ok=True)
    plt = _plt()
    summary = result["summary"]

    # 1. learning_curves_by_schedule.png — every seed/fold trajectory, no mean-only.
    fields = [("dev_pooled_bce", "dev pooled BCE"),
              ("dev_record_bce", "dev record-balanced BCE"),
              ("dev_record_ksweep", "dev record k-sweep"),
              ("train_pooled_bce", "train pooled BCE")]
    fig, axes = plt.subplots(len(SCHEDULE_NAMES), len(fields),
                             figsize=(4.0 * len(fields), 2.8 * len(SCHEDULE_NAMES)),
                             squeeze=False)
    for i, sch in enumerate(SCHEDULE_NAMES):
        for j, (fld, title) in enumerate(fields):
            ax = axes[i][j]
            for arm, color in ((ARM_C, LATER_COLOR), (ARM_D, "#999999")):
                for h in _hist_by(history, arm=arm, schedule=sch):
                    eps = [c["epoch"] for c in h["checkpoints"]]
                    vals = [c[fld] for c in h["checkpoints"]]
                    if any(v is None for v in vals):
                        continue
                    ax.plot(eps, vals, lw=0.7, alpha=0.45, color=color)
            _epoch_axis_note(ax)
            if i == 0:
                ax.set_title(title, fontsize=9)
            if j == 0:
                ax.set_ylabel(sch, fontsize=8)
            ax.grid(alpha=0.3)
            ax.set_xlabel("epoch (-1 = pre-training)", fontsize=7)
    fig.suptitle("One line per (arm, seed, fold): C blue, D grey. "
                 "Red dashes: epoch -1 (pre-training). Orange: epoch 0.",
                 fontsize=10, y=1.01)
    _save(fig, os.path.join(fig_dir, "learning_curves_by_schedule.png"))

    # 2. pretrain_vs_epoch0.png — the comparison Q4-O could not make.
    fig, axes = plt.subplots(1, len(SCHEDULE_NAMES),
                             figsize=(4.0 * len(SCHEDULE_NAMES), 3.4),
                             squeeze=False)
    for i, sch in enumerate(SCHEDULE_NAMES):
        ax = axes[0][i]
        for arm, marker in ((ARM_C, "o"), (ARM_D, "x")):
            xs, ys = [], []
            for h in _hist_by(history, arm=arm, schedule=sch):
                cps = {c["epoch"]: c for c in h["checkpoints"]}
                xs.append(cps[PRETRAIN_EPOCH]["dev_record_bce"])
                ys.append(cps[0]["dev_record_bce"])
            ax.scatter(xs, ys, marker=marker, alpha=0.7,
                       label=f"{arm}", s=22,
                       color=LATER_COLOR if arm == ARM_C else "#999999")
        lims = ax.get_xlim() + ax.get_ylim()
        lo, hi = min(lims), max(lims)
        ax.plot([lo, hi], [lo, hi], color=PRETRAIN_COLOR, lw=1, ls="--")
        ax.set_xlabel("epoch -1 dev record BCE (pre-training)", fontsize=8)
        ax.set_ylabel("epoch 0 dev record BCE", fontsize=8)
        ax.set_title(sch, fontsize=9)
        ax.legend(fontsize=7)
        ax.grid(alpha=0.3)
    fig.suptitle("Below the diagonal: the first trained epoch IMPROVED on the "
                 "pre-training checkpoint.", fontsize=10, y=1.03)
    _save(fig, os.path.join(fig_dir, "pretrain_vs_epoch0.png"))

    # 3. best_epoch_distribution.png
    fig, axes = plt.subplots(len(QP_ARMS), len(SELECTORS),
                             figsize=(4.0 * len(SELECTORS), 2.8 * len(QP_ARMS)),
                             squeeze=False)
    for i, arm in enumerate(QP_ARMS):
        for j, sel in enumerate(SELECTORS):
            ax = axes[i][j]
            for sch, off in zip(SCHEDULE_NAMES, (-0.25, 0.0, 0.25)):
                eps = summary["best_epoch_dist"][arm][sch][sel]["epochs"]
                vals, counts = np.unique(eps, return_counts=True)
                colors = [PRETRAIN_COLOR if v == PRETRAIN_EPOCH else
                          (EPOCH0_COLOR if v == 0 else LATER_COLOR) for v in vals]
                ax.bar(vals + off, counts, width=0.24, alpha=0.75,
                       color=colors, label=sch)
            _epoch_axis_note(ax)
            if i == 0:
                ax.set_title(sel, fontsize=9)
            if j == 0:
                ax.set_ylabel(arm, fontsize=8)
            ax.set_xlabel("selected epoch", fontsize=7)
            ax.grid(alpha=0.3, axis="y")
    _save(fig, os.path.join(fig_dir, "best_epoch_distribution.png"))

    # 4. alpha_and_effective_residual.png
    fig, axes = plt.subplots(len(SCHEDULE_NAMES), 3,
                             figsize=(12, 2.8 * len(SCHEDULE_NAMES)),
                             squeeze=False)
    for i, sch in enumerate(SCHEDULE_NAMES):
        for j, (fld, title) in enumerate((("alpha", "alpha (sign can flip with head)"),
                                          ("eff_residual_mean_abs",
                                           "mean |alpha x residual| (dev)"),
                                          ("eff_residual_p95_abs",
                                           "p95 |alpha x residual| (dev)"))):
            ax = axes[i][j]
            for h in _hist_by(history, arm=ARM_C, schedule=sch):
                eps = [c["epoch"] for c in h["checkpoints"]]
                ax.plot(eps, [c[fld] for c in h["checkpoints"]],
                        lw=0.7, alpha=0.5, color=LATER_COLOR)
            _epoch_axis_note(ax)
            if i == 0:
                ax.set_title(title, fontsize=9)
            if j == 0:
                ax.set_ylabel(sch, fontsize=8)
            ax.grid(alpha=0.3)
    fig.suptitle("Interpretation target is alpha x residual, not alpha's sign.",
                 fontsize=10, y=1.01)
    _save(fig, os.path.join(fig_dir, "alpha_and_effective_residual.png"))

    # 5. gradient_update_diagnostics.png — first GRAD_LOG_STEPS steps.
    fig, axes = plt.subplots(len(SCHEDULE_NAMES), 2,
                             figsize=(10, 2.8 * len(SCHEDULE_NAMES)),
                             squeeze=False)
    for i, sch in enumerate(SCHEDULE_NAMES):
        for j, kind in enumerate(("grad", "upd")):
            ax = axes[i][j]
            for h in _hist_by(history, arm=ARM_C, schedule=sch):
                gl = h.get("grad_log_first_steps") or []
                if not gl:
                    continue
                steps = [g["step"] for g in gl]
                for part, color in (("alpha", PRETRAIN_COLOR),
                                    ("head", EPOCH0_COLOR),
                                    ("trunk", LATER_COLOR)):
                    ax.plot(steps, [g[f"{kind}_{part}"] for g in gl],
                            lw=0.5, alpha=0.35, color=color)
            ax.set_yscale("log")
            if i == 0:
                ax.set_title(f"{kind} norm, first {GRAD_LOG_STEPS} steps "
                             "(red alpha / orange head / blue trunk)", fontsize=9)
            if j == 0:
                ax.set_ylabel(sch, fontsize=8)
            ax.grid(alpha=0.3)
            ax.set_xlabel("optimizer step", fontsize=7)
    _save(fig, os.path.join(fig_dir, "gradient_update_diagnostics.png"))

    # 6. selector_disagreement.png
    fig, ax = plt.subplots(figsize=(8, 4))
    labels, s0e, s1e, s2e = [], [], [], []
    for sch in SCHEDULE_NAMES:
        for h in _hist_by(history, arm=ARM_C, schedule=sch):
            labels.append(f"{sch[:2]}·s{str(h['seed'])[-2:]}·f{h['fold']}")
            s0e.append(h["selected"][SEL0])
            s1e.append(h["selected"][SEL1])
            s2e.append(h["selected"][SEL2])
    xs = np.arange(len(labels))
    ax.scatter(xs, s0e, s=14, label=SEL0, color=LATER_COLOR)
    ax.scatter(xs, s1e, s=14, label=SEL1, color=EPOCH0_COLOR, marker="s")
    ax.scatter(xs, s2e, s=14, label=SEL2, color="#6a51a3", marker="^")
    ax.axhline(-1, color=PRETRAIN_COLOR, lw=0.8, ls="--")
    ax.axhline(0, color=EPOCH0_COLOR, lw=0.8, ls="--")
    ax.set_ylabel("selected epoch")
    ax.set_title("Arm C: where the three dev-only selectors disagree", fontsize=10)
    ax.legend(fontsize=7)
    ax.grid(alpha=0.3, axis="y")
    ax.set_xticks([])
    _save(fig, os.path.join(fig_dir, "selector_disagreement.png"))

    # 7. c_vs_d_by_schedule.png
    fig, ax = plt.subplots(figsize=(8, 4))
    xpos = 0
    ticks, ticklabels = [], []
    for sch in SCHEDULE_NAMES:
        for sel in SELECTORS:
            c = summary["contrasts"][sch][sel]["C_minus_D"]["record_bootstrap"]
            ax.errorbar(xpos, c["mean"],
                        yerr=[[c["mean"] - c["ci_low"]], [c["ci_high"] - c["mean"]]],
                        fmt="o", color=LATER_COLOR if sel == PRIMARY_SELECTOR
                        else "#999999", capsize=3)
            ticks.append(xpos)
            ticklabels.append(f"{sch[:2]}\n{sel[3:6]}")
            xpos += 1
        xpos += 1
    ax.axhline(0, color="k", lw=0.8)
    ax.set_xticks(ticks)
    ax.set_xticklabels(ticklabels, fontsize=7)
    ax.set_ylabel("C - D (record k-sweep, paired)")
    ax.set_title("C - D per schedule x selector. Blue = primary selector. "
                 "No max-over-schedules headline.", fontsize=10)
    ax.grid(alpha=0.3, axis="y")
    _save(fig, os.path.join(fig_dir, "c_vs_d_by_schedule.png"))

    # 8. patient_delta_waterfall.png — primary selector, S0, mean over seeds.
    with np.load(os.path.join(out_dir, "predictions.npz")) as npz:
        key = f"logit_{ARM_C}__S0_original__{PRIMARY_SELECTOR}"
        c_scores = npz[key]
        a_scores = npz["logit_morph_baseline"]
    ksw_a = per_record_ksw_scores(a_scores, cohort, records)
    deltas = []
    for r in records:
        vals = []
        for si in range(c_scores.shape[0]):
            k_c = float(np.mean([achievement_at(c_scores[si],
                                                cohort.idx_of[int(r)],
                                                cohort.y, k) for k in K_SWEEP]))
            vals.append(k_c - ksw_a[r])
        deltas.append((int(r), float(np.mean(vals))))
    deltas.sort(key=lambda t: t[1])
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.bar(range(len(deltas)), [d for _, d in deltas],
           color=[PRETRAIN_COLOR if d < 0 else LATER_COLOR for _, d in deltas])
    ax.axhline(0, color="k", lw=0.8)
    ax.set_xticks(range(len(deltas)))
    ax.set_xticklabels([str(r) for r, _ in deltas], fontsize=5, rotation=90)
    ax.set_ylabel(f"C - A per record ({len(seeds)}-seed mean)")
    ax.set_title(f"Per-record delta, Arm C S0_original {PRIMARY_SELECTOR} "
                 "(all seeds averaged)", fontsize=10)
    _save(fig, os.path.join(fig_dir, "patient_delta_waterfall.png"))

    # 9. decision_matrix.png
    dec = result["decision_tree"]
    fig, ax = plt.subplots(figsize=(10, 3.2))
    ax.axis("off")
    rows = []
    for b in DECISION_BRANCHES:
        info = dec["branches"].get(b, {})
        state = ("NOT EVALUABLE" if not info.get("evaluable")
                 else ("FIRES" if info.get("fires") else "does not fire"))
        rows.append([b, state])
    tbl = ax.table(cellText=rows, colLabels=["pre-registered branch", "state"],
                   loc="center", cellLoc="left")
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(8)
    tbl.scale(1, 1.4)
    for (r, c), cell in tbl.get_celld().items():
        if r > 0 and c == 1:
            txt = cell.get_text().get_text()
            if txt == "FIRES":
                cell.get_text().set_color(PRETRAIN_COLOR)
    ax.set_title(f"Decision matrix — verdict: {dec['verdict']}", fontsize=11)
    _save(fig, os.path.join(fig_dir, "decision_matrix.png"))

    # report_summary.md
    md = _report_markdown(result)
    with open(os.path.join(fig_dir, "report_summary.md"), "w",
              encoding="utf-8") as fh:
        fh.write(md)

    after = bundle_fingerprint(out_dir)
    changed = [k for k in before if before[k] != after.get(k)]
    if changed:
        raise Q4PError(f"reporting modified measured artifacts: {changed}")
    log(f"figures + report written; measured artifacts unchanged "
        f"({len(before)} fingerprints)")


def _report_markdown(result: dict) -> str:
    s = result["summary"]
    dec = result["decision_tree"]
    L = [f"# {EXPERIMENT_ID} / {ARM_ID} — best_epoch=0 원인 분리 진단",
         "",
         f"- 상태: **{result['status']}**",
         f"- 주 selector: `{result['primary_selector']}`",
         f"- 판정: **{dec['verdict']}**",
         ""]
    if result.get("smoke"):
        L += ["> ⚠️ **SYNTHETIC smoke run.** 과학적 의미 없음 — 배관 검증 전용.", ""]
    L += ["## best epoch 분포 (P(-1) / P(0) / P(>0))", ""]
    for arm in QP_ARMS:
        for sch in SCHEDULE_NAMES:
            d = s["best_epoch_dist"][arm][sch][result["primary_selector"]]
            L.append(f"- {arm} · {sch}: P(-1)={d['p_pretrain']:.2f} "
                     f"P(0)={d['p_epoch0']:.2f} P(>0)={d['p_later']:.2f}")
    L += ["", "## C-D (주 selector, schedule별)", ""]
    for sch in SCHEDULE_NAMES:
        c = s["contrasts"][sch][result["primary_selector"]]["C_minus_D"][
            "record_bootstrap"]
        L.append(f"- {sch}: {c['mean']:+.4f} [{c['ci_low']:+.4f}, "
                 f"{c['ci_high']:+.4f}]")
    L += ["", "## 사전등록 decision tree", ""]
    for b in DECISION_BRANCHES:
        info = dec["branches"].get(b, {})
        state = ("평가불가" if not info.get("evaluable")
                 else ("발화" if info.get("fires") else "미발화"))
        L.append(f"- `{b}`: {state}")
    L += ["", f"**최종 판정: {dec['verdict']}**", "",
          "epoch -1(학습 전)과 epoch 0(첫 학습 epoch 완료)은 모든 표·그림에서 "
          "빨강/주황으로 구분 표기된다. test trajectory 전체는 exploratory이며 "
          "schedule 선택이나 baseline 승격에 사용되지 않았다.", ""]
    return "\n".join(L)


# ─────────────────────────────────────────────────────────────────────────────
# Self-check (stale-import guard, mirrors Q4-O's convention)
# ─────────────────────────────────────────────────────────────────────────────
def self_check(min_version: int = MODULE_VERSION) -> Dict[str, object]:
    if MODULE_VERSION < min_version:
        raise Q4PError(f"stale module: version {MODULE_VERSION} < {min_version}")
    # Selector sanity on a tiny synthetic trajectory, incl. the -1 candidate.
    cps = [{"epoch": -1, "dev_pooled_bce": 0.5, "dev_record_bce": 0.5,
            "dev_record_ksweep": 0.4},
           {"epoch": 0, "dev_pooled_bce": 0.4, "dev_record_bce": 0.6,
            "dev_record_ksweep": 0.4},
           {"epoch": 1, "dev_pooled_bce": 0.4, "dev_record_bce": 0.45,
            "dev_record_ksweep": 0.5}]
    got = {sel: select_checkpoint(cps, sel) for sel in SELECTORS}
    want = {SEL0: 0, SEL1: 1, SEL2: 1}
    if got != want:
        raise Q4PError(f"selector self-check failed: {got} != {want}")
    return {"module_file": os.path.abspath(__file__),
            "module_version": MODULE_VERSION, "module_build": MODULE_BUILD,
            "selectors_ok": True, "status": STATUS}


# ─────────────────────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────────────────────
def main(argv: Optional[Sequence[str]] = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--data", help="svdb_data5.npz path (full run)")
    ap.add_argument("--out", required=True, help="output run directory")
    ap.add_argument("--smoke", action="store_true",
                    help="CPU synthetic smoke run (no scientific meaning)")
    ap.add_argument("--seeds", type=int, nargs="*", default=None)
    ap.add_argument("--epochs", type=int, default=None)
    ap.add_argument("--n-boot", type=int, default=2000)
    args = ap.parse_args(argv)

    log = RunLog()
    if args.smoke:
        cohort = synthetic_cohort(n_record=8, n_beat=110, seed=17, n_unscorable=2)
        provenance = {"abs_path": "<synthetic>", "file_name": "<synthetic>",
                      "sha256": "<synthetic>", "synthetic": True}
        seeds = args.seeds or list(TRAIN_SEEDS[:2])
        epochs = args.epochs or 3
    else:
        if not args.data:
            ap.error("--data is required unless --smoke")
        cohort, provenance = load_cohort(args.data)
        seeds = args.seeds or list(TRAIN_SEEDS)
        epochs = args.epochs or N_EPOCHS
    result = run_diagnostic(cohort, provenance, args.out, seeds=seeds,
                            epochs=epochs, n_boot=args.n_boot,
                            device="cpu" if args.smoke else None,
                            smoke=args.smoke, log=log)
    log(f"verdict: {result['decision_tree']['verdict']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
