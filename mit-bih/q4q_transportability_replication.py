#!/usr/bin/env python3
"""EXP-2026-003 / Q4-Q — transportability replication of Q4-P's alpha-LR finding.

Spec: ``experiments/specs/EXP-2026-003-q4q-transportability-replication.md``
Status: DESIGN / RESULT NOT RUN — nothing in this file is a result. No full GPU
run, no PREP_DATA gate and no Q4-P derived analysis has been executed yet.

The one fixed question
----------------------
Q4-P (EXP-2026-002, MEASURED, verdict B3) found on SVDB that lowering ONLY the
alpha learning rate (schedule S2, alpha LR 1e-4) moved the selected checkpoint
later and enlarged test C-D versus S0 — with a CI that still includes 0. Q4-Q
asks whether that schedule interaction and the waveform-specific residual gap
replicate on an independent cohort (MIT-BIH DS1->DS2), and whether the effect
reaches a pre-registered patient-level utility gate. Naming boundary: MIT-BIH
and INCART were both used before in this project, so this is a *pre-registered
independent-cohort / transportability replication* — never an "untouched
external confirmation".

What this module reuses (imported, never copied):
Q4-O: residual model builder, Arm A logistic protocol, paired/hierarchical
record bootstraps, k-sweep achievement, determinism, provenance helpers.
Q4-P: the diagnostic training loop (epoch -1 candidacy, full 24-epoch
trajectories, paired init/minibatch order), the dev-only selectors, and the
schedule definitions (Q4-Q uses exactly S0_original and S2_alpha_low).

Commands
--------
    python mit-bih/test_q4q_transportability_replication.py
    python mit-bih/q4q_transportability_replication.py --mode SMOKE --out /tmp/q4q_smoke
    python mit-bih/q4q_transportability_replication.py --mode PREP_DATA \
        --data <mamba_data.npz> [--multi <ecg_multi.npz>] [--incart-hea <dir>] --out <dir>
    python mit-bih/q4q_transportability_replication.py --mode FULL \
        --data <mamba_data.npz> --out <run dir>
    python mit-bih/q4q_transportability_replication.py --mode ANALYZE \
        --q4p-run <q4p run dir> --out <derived dir>
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import q4o_leakage_free_residual as Q4O  # noqa: E402
import q4p_best_epoch_zero_diagnostic as QP  # noqa: E402
from q4o_leakage_free_residual import (  # noqa: E402
    Cohort, Q4OError, RunLog,
    DL_BATCH, K_SWEEP, PERM_SEED, SEED0, TRAIN_SEEDS,
    achievement_at, assert_disjoint, assert_finite, build_residual_net,
    current_beat_input, dev_records, git_commit_sha, gpu_info,
    package_versions, paired_record_bootstrap, hierarchical_bootstrap,
    record_burden, samples_of, set_determinism, sha256_file,
    shuffle_waveforms_within_record, _fit_logit, _json_safe, _require_torch,
)
from q4p_best_epoch_zero_diagnostic import (  # noqa: E402
    SEL1, SCHEDULES, diagnostic_train_one_fold, select_checkpoint,
)

# ─────────────────────────────────────────────────────────────────────────────
# Identity and pre-registered protocol constants — frozen before any run.
# ─────────────────────────────────────────────────────────────────────────────
EXPERIMENT_ID = "EXP-2026-003"
ARM_ID = "Q4-Q"
RUN_SLUG = "q4q_transportability_replication"
STATUS = "PREREGISTERED REPLICATION / RESULT NOT RUN"

MODULE_VERSION = 5
MODULE_BUILD = ("2026-08-08 q4q.5 — cross-check identifies records by 5-class "
                "fingerprint assignment (beat counts drift several percent on "
                "noisy records under mamba's stricter prep); S strictly "
                "gated, all else reported; no full run has been executed")

MODES = ("DESIGN", "SMOKE", "PREP_DATA", "FULL", "ANALYZE")

# Exactly two schedules (frozen from Q4-P; S1 is intentionally absent) and one
# pre-specified dev-only selector. Nothing may be added after seeing results.
QQ_SCHEDULES: Tuple[str, str] = ("S0_original", "S2_alpha_low")
for _s in QQ_SCHEDULES:
    if _s not in SCHEDULES:
        raise RuntimeError(f"schedule {_s} missing from Q4-P's frozen table")
SELECTOR = SEL1                     # SEL1_record_bce — pre-specified, dev-only
N_EPOCHS = QP.N_EPOCHS              # 24 — frozen training horizon
SEEDS = TRAIN_SEEDS                 # 20260806..20260810 — frozen

ARM_C = "morph_plus_raw_residual"
ARM_D = "shuffled_waveform_control"
QQ_ARMS = (ARM_C, ARM_D)

# Pre-registered utility gate (spec §5).
UTILITY_MIN_GAIN = 0.015            # C-S2 minus A, record-macro S PR-AUC
UTILITY_SEED_MIN = 4                # of 5 seeds positive
P10_TOL = 0.010                     # p10 non-inferiority tolerance vs Arm A

# de Chazal canonical MIT-BIH DS1/DS2 (44 non-paced records; record == patient).
DS1_RECORDS: Tuple[int, ...] = (
    101, 106, 108, 109, 112, 114, 115, 116, 118, 119, 122,
    124, 201, 203, 205, 207, 208, 209, 215, 220, 223, 230)
DS2_RECORDS: Tuple[int, ...] = (
    100, 103, 105, 111, 113, 117, 121, 123, 200, 202, 210,
    212, 213, 214, 219, 221, 222, 228, 231, 232, 233, 234)
MIT_ALL_RECORDS = tuple(sorted(DS1_RECORDS + DS2_RECORDS))
# The four paced records the de Chazal 44-record set excludes. ecg_multi.npz
# keeps all 48 MIT records (measured 2026-08-08: 48 records / 109,446 beats vs
# mamba's 44 / 99,871, with the S total identical at 2,781), so the
# cross-check must corroborate through per-record profiles, not id equality.
PACED_RECORDS: Tuple[int, ...] = (102, 104, 107, 217)
MIT_48_RECORDS = tuple(sorted(MIT_ALL_RECORDS + PACED_RECORDS))
# Cross-check matching (v4). Measured 2026-08-08, fourth PREP_DATA round:
# mamba's prep drops beats non-uniformly (a few noisy records lose several
# percent — e.g. a 2887-beat record whose nearest multi candidate is 2953),
# so no single beat-count tolerance can match records. Identity is instead
# established by the per-record 5-class fingerprint (N/S/V/F/Q counts) via a
# global minimum-cost assignment; only the scientific quantity S is gated
# strictly, everything else is REPORTED in a full side-by-side table.
CLASS_NAMES = ("N", "S", "V", "F", "Q")
S_MISMATCH_MAX_PER_RECORD = 10
S_MISMATCH_MAX_TOTAL = 20
BEAT_DEFICIT_WARN = 0.03         # matched pair |dn|/n above this -> warning
PACED_MIN_Q_FRACTION = 0.2       # leftover records must look paced (Q-heavy)
PACED_MAX_S = 10

# Confirmed facts about the frozen MIT asset (spec §2). A mismatch is a STOP
# condition, not something to paper over.
EXPECTED_MIT = {"n_beat": 99871, "n_record": 44, "n_ds1": 22, "n_ds2": 22}
REQUIRED_MIT_KEYS = ("beat", "feats", "y", "pid")
MIT_S_INDEX = 1                     # AAMI 5-class: 0=N, 1=S, 2=V, 3=F, 4=Q

# INCART gate constants (spec §2).
INCART_EXPECTED_RECORDS = 75
INCART_EXPECTED_PATIENTS = 32
INCART_PATIENT_RE = re.compile(r"^#\s*patient\s+(\d+)\s*$", re.IGNORECASE)

NB_BOOT = 2000

BUNDLE_FILES = ("config.json", "manifest.json", "result.json",
                "split_map.json", "predictions.npz", "training_history.json",
                "checkpoint_table.csv", "trajectory_table.csv")

FIGURES = ("data_audit_split_table.png", "class_patient_counts.png",
           "learning_curves.png", "best_epoch_distribution.png",
           "arm_schedule_table.png", "c_minus_d_did_forest.png",
           "seed_direction.png", "patient_waterfall_p10.png",
           "pr_curves_calibration.png", "decision_matrix.png")


class Q4QError(RuntimeError):
    """Loud failure with cause and the command that fixes it — no silent fallback."""


def run_dir_name(timestamp: str) -> str:
    return f"{timestamp}_{EXPERIMENT_ID}_{RUN_SLUG}"


def resolve_mode(mode: str) -> str:
    """Exactly one of MODES; anything else is a hard error (spec §6)."""
    m = str(mode).strip().upper()
    if m not in MODES:
        raise Q4QError(f"mode must be exactly one of {MODES}, got {mode!r}")
    return m


# ─────────────────────────────────────────────────────────────────────────────
# Metrics. Primary endpoint metric: record-macro S-beat PR-AUC (project
# convention). Secondary continuity metric: Q4-P's k-sweep achievement.
# ─────────────────────────────────────────────────────────────────────────────
def per_record_s_prauc(scores: np.ndarray, cohort: Cohort,
                       records: Sequence[int]) -> Dict[int, float]:
    """Average precision per record. A record enters iff it has both classes
    (identical inclusion rule to Q4-P's ``record_macro_prauc``)."""
    from sklearn.metrics import average_precision_score
    out: Dict[int, float] = {}
    for r in records:
        idx = cohort.idx_of[int(r)]
        yy = cohort.y[idx].astype(int)
        if 0 < int(yy.sum()) < len(yy):
            out[int(r)] = float(average_precision_score(yy, scores[idx]))
    if not out:
        raise Q4QError("no record has both classes — S PR-AUC is undefined; "
                       "check the label mapping audit before rerunning")
    return out


def per_record_ksw(scores: np.ndarray, cohort: Cohort,
                   records: Sequence[int]) -> Dict[int, float]:
    return {int(r): float(np.mean([achievement_at(scores, cohort.idx_of[int(r)],
                                                  cohort.y, k) for k in K_SWEEP]))
            for r in records}


def p10(values: Sequence[float]) -> float:
    return float(np.percentile(np.asarray(list(values), float), 10))


# ─────────────────────────────────────────────────────────────────────────────
# MIT-BIH loader and audits.
# ─────────────────────────────────────────────────────────────────────────────
def load_mit_cohort(npz_path: str,
                    s_index: int = MIT_S_INDEX,
                    expected: Optional[dict] = None,
                    log: Optional[RunLog] = None
                    ) -> Tuple[Cohort, np.ndarray, Dict[str, object]]:
    """Load ``mamba_data.npz`` into a Q4-O ``Cohort`` plus the frozen feature
    matrix for Arm A. Refuses any file that does not match the registered
    asset: keys, alignment, canonical 44-record identity, expected counts."""
    log = log or RunLog()
    expected = EXPECTED_MIT if expected is None else expected
    if not os.path.exists(npz_path):
        raise Q4QError(f"data file not found: {npz_path}")
    data = np.load(npz_path, allow_pickle=True)
    missing = [k for k in REQUIRED_MIT_KEYS if k not in data.files]
    if missing:
        raise Q4QError(
            f"{os.path.basename(npz_path)} is missing required key(s) {missing}; "
            f"Q4-Q requires mamba_data.npz with keys {list(REQUIRED_MIT_KEYS)} "
            f"(found {sorted(data.files)}). Do not substitute another file.")

    beat = np.asarray(data["beat"], dtype="float32")
    feats = np.asarray(data["feats"], dtype="float64")
    y_raw = np.asarray(data["y"]).astype(int)
    pid = np.asarray(data["pid"]).astype(int)

    n = len(y_raw)
    if beat.ndim == 2:                       # (n, width) single lead -> add axis
        beat = beat[:, None, :]
    if beat.ndim != 3 or beat.shape[0] != n or feats.shape[0] != n or len(pid) != n:
        raise Q4QError(
            f"array misalignment: beat {beat.shape}, feats {feats.shape}, "
            f"y {y_raw.shape}, pid {pid.shape} — refusing to guess")
    if y_raw.min() < 0 or y_raw.max() > 4:
        raise Q4QError(f"y is not AAMI 5-class int coded (range "
                       f"[{y_raw.min()},{y_raw.max()}]) — audit the label mapping")

    rec_set = sorted(set(pid.tolist()))
    if tuple(rec_set) != MIT_ALL_RECORDS:
        raise Q4QError(
            "pid does not carry the canonical 44 non-paced MIT-BIH record "
            f"numbers. found {len(rec_set)} ids, e.g. {rec_set[:6]}; expected "
            f"{list(MIT_ALL_RECORDS[:6])}... Run PREP_DATA with ecg_multi.npz "
            "to establish the mapping — do not guess.")
    if expected and n != expected["n_beat"]:
        raise Q4QError(f"beat count {n} != registered {expected['n_beat']} for "
                       "mamba_data.npz — STOP: unexplained count mismatch")

    cohort = Cohort(
        beat=beat,
        y=(y_raw == s_index),
        y3=y_raw,
        pre=np.full(n, np.nan),
        post=np.full(n, np.nan),
        rid=pid,
        sym=np.full(n, "?", dtype="<U2"),
        sample_id=np.arange(n, dtype=np.int64),
        records=np.array(rec_set, dtype=int),
        idx_of={int(r): np.where(pid == r)[0] for r in rec_set},
    )
    audit = {
        "file": os.path.basename(npz_path),
        "keys": sorted(data.files),
        "n_beat": int(n), "n_record": len(rec_set),
        "beat_shape": list(beat.shape), "feats_dim": int(feats.shape[1]),
        "s_index": int(s_index), "n_s": int(cohort.y.sum()),
        "class_counts": {str(c): int((y_raw == c).sum()) for c in range(5)},
        "ds1": list(DS1_RECORDS), "ds2": list(DS2_RECORDS),
        "records": rec_set,
        "per_record": {str(r): {
            "n": int(len(cohort.idx_of[int(r)])),
            "s": int(cohort.y[cohort.idx_of[int(r)]].sum()),
            "classes": [int((y_raw[cohort.idx_of[int(r)]] == c).sum())
                        for c in range(5)]} for r in rec_set},
    }
    log(f"MIT cohort: {n} beats, {len(rec_set)} records, "
        f"S={audit['n_s']} ({100 * cohort.y.mean():.2f}%)")
    return cohort, feats, audit


def mit_split(cohort: Cohort) -> Dict[str, List[int]]:
    """Frozen split. DS1 -> (fit, dev) by Q4-O's burden-ordered every-5th rule
    (deterministic, seed-invariant); DS2 is the single fixed final test."""
    recs = set(int(r) for r in cohort.records)
    ds1 = [r for r in DS1_RECORDS if r in recs]
    ds2 = [r for r in DS2_RECORDS if r in recs]
    if len(ds1) != len(DS1_RECORDS) or len(ds2) != len(DS2_RECORDS):
        raise Q4QError("cohort does not contain the full canonical DS1/DS2 sets")
    assert_disjoint(ds1, ds2, "DS1 vs DS2")
    burden = record_burden(cohort, ds1)
    fit, dev = dev_records(ds1, burden)
    assert_disjoint(fit, dev, "DS1 fit vs dev")
    assert_disjoint(fit + dev, ds2, "DS1 vs DS2 after dev carve")
    if sorted(fit + dev) != sorted(ds1):
        raise Q4QError("fit+dev does not partition DS1")
    return {"ds1": ds1, "ds2": ds2, "fit": sorted(fit), "dev": sorted(dev)}


def _fingerprint_match(mamba_prof: Dict[int, Dict[str, object]],
                       multi_prof: Dict[int, Dict[str, object]]
                       ) -> Dict[str, object]:
    """Global minimum-cost assignment of mamba records to multi records on
    the per-record 5-class fingerprint (N/S/V/F/Q counts).

    Feasibility is capped ONLY on the scientific class: a pair with
    |dS| > S_MISMATCH_MAX_PER_RECORD can never be matched. All other class
    differences contribute to the cost and are fully REPORTED — beat
    deficits from stricter preprocessing (measured up to several percent on
    noisy records) must be visible, not fatal.
    Returns {mapping, leftover, table, s_agreement, warnings}.
    """
    from scipy.optimize import linear_sum_assignment

    m_ids = sorted(mamba_prof)
    u_ids = sorted(multi_prof)
    if len(u_ids) < len(m_ids):
        raise Q4QError(
            f"ecg_multi MIT subset offers {len(u_ids)} records for mamba's "
            f"{len(m_ids)} — unexplained mismatch, STOP (spec §10)")
    BIG = 1e12
    cost = np.zeros((len(m_ids), len(u_ids)))
    for i, rm in enumerate(m_ids):
        cm = np.asarray(mamba_prof[rm]["classes"], int)
        for j, ru in enumerate(u_ids):
            cu = np.asarray(multi_prof[ru]["classes"], int)
            d = int(np.abs(cm - cu).sum())
            if abs(int(cm[MIT_S_INDEX]) - int(cu[MIT_S_INDEX])) \
                    > S_MISMATCH_MAX_PER_RECORD:
                cost[i, j] = BIG
            else:
                cost[i, j] = d
    rows, cols = linear_sum_assignment(cost)
    if any(cost[i, j] >= BIG / 2 for i, j in zip(rows, cols)):
        bad = [(m_ids[i], u_ids[j]) for i, j in zip(rows, cols)
               if cost[i, j] >= BIG / 2]
        raise Q4QError(
            "fingerprint assignment infeasible — these mamba records have no "
            f"multi candidate within the S cap ({S_MISMATCH_MAX_PER_RECORD}): "
            f"{[m for m, _ in bad]} — see the audit table, STOP (spec §10)")

    mapping = {m_ids[i]: u_ids[j] for i, j in zip(rows, cols)}
    leftover = [r for r in u_ids if r not in set(mapping.values())]

    table, warnings, per_record_s, total_s = [], [], [], 0
    for rm in m_ids:
        ru = mapping[rm]
        cm = np.asarray(mamba_prof[rm]["classes"], int)
        cu = np.asarray(multi_prof[ru]["classes"], int)
        n_m, n_u = int(cm.sum()), int(cu.sum())
        ds = int(abs(int(cm[MIT_S_INDEX]) - int(cu[MIT_S_INDEX])))
        row = {"mamba_record": int(rm), "multi_record": int(ru),
               "n_mamba": n_m, "n_multi": n_u,
               "classes_mamba": [int(v) for v in cm],
               "classes_multi": [int(v) for v in cu],
               "class_abs_diff": [int(abs(a - b)) for a, b in zip(cm, cu)],
               "beat_deficit_frac": float((n_u - n_m) / max(1, n_u))}
        if abs(n_u - n_m) > BEAT_DEFICIT_WARN * max(1, n_u):
            row["warning"] = (f"beat count differs by "
                              f"{abs(n_u - n_m)} ({row['beat_deficit_frac']:+.1%})"
                              " — stricter mamba preprocessing; verify in the"
                              " audit table")
            warnings.append(row["warning"] + f" (record {rm})")
        table.append(row)
        if ds:
            per_record_s.append({"mamba_record": int(rm),
                                 "s_mamba": int(cm[MIT_S_INDEX]),
                                 "s_multi": int(cu[MIT_S_INDEX])})
            total_s += ds
    if total_s > S_MISMATCH_MAX_TOTAL:
        raise Q4QError(
            f"total per-record S disagreement {total_s} exceeds the "
            f"{S_MISMATCH_MAX_TOTAL}-beat budget: {per_record_s} — "
            "unexplained, STOP (spec §10)")
    s_agreement = {"n_mismatched_records": len(per_record_s),
                   "total_abs_diff": int(total_s),
                   "budget": {"per_record": S_MISMATCH_MAX_PER_RECORD,
                              "total": S_MISMATCH_MAX_TOTAL},
                   "per_record": per_record_s}
    return {"mapping": mapping, "leftover": leftover, "table": table,
            "s_agreement": s_agreement, "warnings": warnings}


def cross_check_mit_vs_multi(mit_audit: Dict[str, object],
                             multi_npz_path: str,
                             log: Optional[RunLog] = None,
                             strict: bool = True) -> Dict[str, object]:
    """Corroborate mamba_data.npz against ecg_multi.npz's MIT subset.

    v4 (each rule forced by a measured PREP_DATA round, see the spec's
    Decision log): record identity via the 5-class fingerprint assignment
    (beat counts drift by several percent on noisy records; per-record S
    membership differs by a beat or two between preps; the 4 paced records
    hide inside every simpler grouping). Hard gates: S totals equal, S
    disagreement within the pre-stated budgets, leftovers are exactly the 4
    paced-looking records (Q-heavy, tiny S) or none. Everything else lands
    in ``checks['table']`` for the audit.

    With ``strict=False`` the function never raises on gate failure — it
    returns ``checks`` with ``pass``/``fail_reasons`` so PREP_DATA can write
    the full audit before stopping loudly.
    """
    log = log or RunLog()
    if not os.path.exists(multi_npz_path):
        raise Q4QError(f"ecg_multi.npz not found: {multi_npz_path}")
    data = np.load(multi_npz_path, allow_pickle=True)
    for k in ("pid", "db"):
        if k not in data.files:
            raise Q4QError(f"ecg_multi.npz missing key {k!r} "
                           f"(found {sorted(data.files)})")
    db = np.asarray(data["db"]).astype(str)
    mask = np.isin(db, ("mitdb", "mit", "mit-bih"))
    if not mask.any():
        raise Q4QError(f"no MIT subset in ecg_multi.npz db values "
                       f"{sorted(set(db.tolist()))[:8]}")
    y_key = next((k for k in ("y5", "y", "y3") if k in data.files), None)
    if y_key is None:
        raise Q4QError("ecg_multi.npz has no label key (y5/y/y3) — cannot "
                       "corroborate class counts, STOP")
    pid = np.asarray(data["pid"]).astype(int)[mask]
    yv = np.asarray(data[y_key]).astype(int)[mask]
    if yv.min() < 0 or yv.max() > 4:
        raise Q4QError(f"ecg_multi {y_key} is not 5-class coded "
                       f"(range [{yv.min()},{yv.max()}]) — STOP")
    multi_recs = sorted(set(pid.tolist()))
    multi_prof = {int(r): {"classes": [int(((pid == r) & (yv == c)).sum())
                                       for c in range(5)]}
                  for r in multi_recs}
    mamba_prof = {int(r): {"classes": list(map(int, v["classes"]))}
                  for r, v in mit_audit["per_record"].items()}

    checks: Dict[str, object] = {
        "n_record": {"mamba": len(mamba_prof), "multi": len(multi_recs)},
        "n_beat": {"mamba": int(mit_audit["n_beat"]), "multi": int(mask.sum())},
        "n_s": {"mamba": int(mit_audit["n_s"]),
                "multi": int((yv == MIT_S_INDEX).sum()),
                "multi_label_key": y_key},
        "pid_coding": ("record_numbers"
                       if set(multi_recs) <= set(MIT_48_RECORDS)
                       else "ordinal_or_other"),
    }
    fail_reasons: List[str] = []
    if checks["n_s"]["mamba"] != checks["n_s"]["multi"]:
        fail_reasons.append(f"S totals differ: {checks['n_s']}")
    try:
        m = _fingerprint_match(mamba_prof, multi_prof)
        checks.update({"matched_records": len(m["mapping"]),
                       "leftover_records": len(m["leftover"]),
                       "table": m["table"], "s_agreement": m["s_agreement"],
                       "warnings": m["warnings"]})
        leftover = m["leftover"]
        if leftover:
            if len(leftover) != len(PACED_RECORDS):
                fail_reasons.append(
                    f"{len(leftover)} unmatched multi records (expected "
                    f"exactly {len(PACED_RECORDS)} paced records or none)")
            for r in leftover:
                cls = multi_prof[r]["classes"]
                n = sum(cls)
                if cls[4] < PACED_MIN_Q_FRACTION * max(1, n) \
                        or cls[MIT_S_INDEX] > PACED_MAX_S:
                    fail_reasons.append(
                        f"leftover multi record {r} does not look paced "
                        f"(classes {cls}) — cannot be 102/104/107/217")
            if checks["pid_coding"] == "record_numbers" and \
                    sorted(leftover) != sorted(PACED_RECORDS):
                fail_reasons.append(
                    f"leftover ids {sorted(leftover)} are not the paced set")
        checks["leftover_profiles"] = {str(r): multi_prof[r]["classes"]
                                       for r in leftover}
    except Q4QError as e:
        fail_reasons.append(str(e))

    checks["fail_reasons"] = fail_reasons
    checks["pass"] = not fail_reasons
    if checks["pass"]:
        checks["explanation"] = (
            "record identity established by 5-class fingerprint assignment; "
            f"{checks['leftover_records']} paced leftovers; S disagreement "
            f"{checks['s_agreement']['total_abs_diff']} beat(s) within the "
            "pre-stated budget; beat-count warnings (stricter mamba "
            f"preprocessing): {len(checks['warnings'])}")
        log(f"cross-check pass: {checks['matched_records']} matched, "
            f"{checks['leftover_records']} paced leftovers, "
            f"{len(checks['warnings'])} beat-count warning(s)")
    elif strict:
        raise Q4QError(
            "ecg_multi.npz MIT subset does not corroborate mamba_data.npz: "
            + " | ".join(fail_reasons)
            + " — STOP condition (spec §10). Run PREP_DATA for the full "
              "side-by-side table in data_audit.json.")
    return checks


# ─────────────────────────────────────────────────────────────────────────────
# INCART gate: frozen record -> patient map plus adapter audit skeleton.
# ─────────────────────────────────────────────────────────────────────────────
def parse_incart_patient_line(text: str) -> Optional[int]:
    hits = [int(m.group(1)) for line in text.splitlines()
            if (m := INCART_PATIENT_RE.match(line.strip()))]
    if len(hits) != 1:
        return None
    return hits[0]


def parse_incart_patient_map(hea_dir: str,
                             log: Optional[RunLog] = None) -> Dict[str, int]:
    """Build the frozen record->patient map from explicit ``# patient N`` header
    lines. Ambiguous or missing metadata FAILS — manual guessing is forbidden."""
    log = log or RunLog()
    if not os.path.isdir(hea_dir):
        raise Q4QError(f"header directory not found: {hea_dir}")
    heas = sorted(f for f in os.listdir(hea_dir) if f.lower().endswith(".hea"))
    if len(heas) != INCART_EXPECTED_RECORDS:
        raise Q4QError(f"expected {INCART_EXPECTED_RECORDS} .hea files, "
                       f"found {len(heas)} in {hea_dir}")
    mapping: Dict[str, int] = {}
    bad: List[str] = []
    for f in heas:
        with open(os.path.join(hea_dir, f), "r", encoding="utf-8",
                  errors="replace") as fh:
            pat = parse_incart_patient_line(fh.read())
        if pat is None:
            bad.append(f)
        else:
            mapping[os.path.splitext(f)[0]] = pat
    if bad:
        raise Q4QError(
            f"{len(bad)} header(s) with zero or multiple '# patient N' lines: "
            f"{bad[:5]}... — FAIL (no manual guessing). Fix the source headers "
            "or report the ambiguity.")
    return mapping


def validate_incart_map(mapping: Dict[str, int]) -> Dict[str, object]:
    patients = sorted(set(mapping.values()))
    ok = (len(mapping) == INCART_EXPECTED_RECORDS
          and len(patients) == INCART_EXPECTED_PATIENTS)
    summary = {"n_record": len(mapping), "n_patient": len(patients),
               "expected_records": INCART_EXPECTED_RECORDS,
               "expected_patients": INCART_EXPECTED_PATIENTS,
               "patients": patients, "pass": bool(ok)}
    if not ok:
        raise Q4QError(
            f"INCART map failed the 75->32 gate: {len(mapping)} records -> "
            f"{len(patients)} patients — STOP condition (spec §10)")
    return summary


# Adapter audit rows. Every row must reach status "comparable" (with the bridge
# spelled out) before any INCART run; "unknown_until_audit" rows are filled by
# PREP_DATA in Colab against the real arrays.
INCART_AUDIT_FIELDS = ("sample_rate_hz", "n_leads", "lead_selection",
                       "resampling", "r_peak_alignment", "window_size",
                       "normalization", "label_mapping", "rr_units",
                       "patient_id_semantics")


def incart_adapter_audit(measured: Optional[Dict[str, object]] = None
                         ) -> Dict[str, object]:
    """Static knowledge + measured values -> the audit table. Never guesses:
    unmeasured rows stay 'unknown_until_audit' and the overall gate FAILS."""
    measured = measured or {}
    known = {
        "sample_rate_hz": {"incart": 257, "mit_q4p": "MIT 360 / SVDB source",
                           "bridge": "resample or re-window to the frozen beat "
                                     "width before comparison"},
        "n_leads": {"incart": 12, "mit_q4p": 2,
                    "bridge": "explicit pre-registered lead selection"},
        "patient_id_semantics": {
            "incart": "npz pid is 75 record-level ids; true patients = 32",
            "mit_q4p": "record == patient",
            "bridge": "frozen record->patient map from '# patient N' headers"},
    }
    rows = {}
    for f in INCART_AUDIT_FIELDS:
        row = dict(known.get(f, {}))
        if f in measured:
            row["measured"] = measured[f]
            row["status"] = "comparable" if measured[f].get("comparable") \
                else "incomparable"
        elif f in known:
            row["status"] = "requires_bridge"
        else:
            row["status"] = "unknown_until_audit"
        rows[f] = row
    gate_pass = all(r["status"] == "comparable" for r in rows.values())
    return {"rows": rows, "gate_pass": bool(gate_pass),
            "note": "full INCART run is forbidden until gate_pass is true"}


# ─────────────────────────────────────────────────────────────────────────────
# Arm A and cross-fitted offsets on the DS1 side only.
# ─────────────────────────────────────────────────────────────────────────────
def ds1_offsets_and_arm_a(feats: np.ndarray, cohort: Cohort,
                          split: Dict[str, List[int]],
                          n_groups: int = 5,
                          log: Optional[RunLog] = None
                          ) -> Tuple[np.ndarray, np.ndarray]:
    """Return (offset, arm_a_logits), both length cohort.n.

    * fit rows: patient-grouped ``n_groups``-fold cross-fitted logits (each fit
      patient scored by a model that never saw it);
    * dev and DS2 rows: one model fit on ALL fit patients. DS2 is scored once,
      by a model whose data never included dev or DS2.
    """
    log = log or RunLog()
    fit, dev, ds2 = split["fit"], split["dev"], split["ds2"]
    burden = record_burden(cohort, fit)
    order = sorted(fit, key=lambda r: (burden[r], r))
    group = {r: i % n_groups for i, r in enumerate(order)}   # burden-balanced
    offset = np.full(cohort.n, np.nan)
    for g in range(n_groups):
        hold = [r for r in fit if group[r] == g]
        rest = [r for r in fit if group[r] != g]
        assert_disjoint(rest, hold, f"offset group {g}")
        tr, te = samples_of(cohort, rest), samples_of(cohort, hold)
        offset[te] = _fit_logit(feats[tr], cohort.y[tr])(feats[te])
    full_idx = samples_of(cohort, fit)
    scorer = _fit_logit(feats[full_idx], cohort.y[full_idx])
    for recs in (dev, ds2):
        idx = samples_of(cohort, recs)
        offset[idx] = scorer(feats[idx])
    arm_a = np.full(cohort.n, np.nan)
    arm_a[samples_of(cohort, fit + dev + ds2)] = \
        offset[samples_of(cohort, fit + dev + ds2)]
    assert_finite(offset[samples_of(cohort, fit + dev + ds2)], "offsets")
    log(f"offsets: {n_groups}-group cross-fit on {len(fit)} fit patients; "
        f"dev/DS2 scored by the full DS1-fit model")
    return offset, arm_a


# ─────────────────────────────────────────────────────────────────────────────
# Endpoints and the pre-registered decision matrix.
# ─────────────────────────────────────────────────────────────────────────────
def seed_mean_by_record(per_seed: Dict[int, Dict[int, float]]) -> Dict[int, float]:
    recs = sorted(next(iter(per_seed.values())))
    return {r: float(np.mean([per_seed[s][r] for s in per_seed])) for r in recs}


def contrast(per_seed_a: Dict[int, Dict[int, float]],
             per_seed_b: Dict[int, Dict[int, float]],
             n_boot: int = NB_BOOT) -> Dict[str, object]:
    """Paired record bootstrap + hierarchical bootstrap + by-seed table of
    (a - b), where each argument is {seed: {record: value}}."""
    seeds = sorted(per_seed_a)
    recs = sorted(next(iter(per_seed_a.values())))
    diff_rs = {r: {s: per_seed_a[s][r] - per_seed_b[s][r] for s in seeds}
               for r in recs}
    diff_r = {r: float(np.mean(list(diff_rs[r].values()))) for r in recs}
    by_seed = [float(np.mean([per_seed_a[s][r] - per_seed_b[s][r]
                              for r in recs])) for s in seeds]
    return {
        "record_bootstrap": paired_record_bootstrap(diff_r, n_boot=n_boot),
        "hierarchical_bootstrap": hierarchical_bootstrap(diff_rs, n_boot=n_boot),
        "by_seed": by_seed,
        "per_record_mean_diff": {str(r): diff_r[r] for r in recs},
    }


def evaluate_decision_matrix(mechanism: Dict[str, object],
                             waveform: Dict[str, object],
                             utility: Dict[str, object]) -> Dict[str, object]:
    """Spec §5 interpretation rules, applied verbatim — no forced verdicts."""
    m_ci = mechanism["record_bootstrap"]
    m_pos = sum(1 for v in mechanism["by_seed"] if v > 0)
    mech_pass = bool(m_ci["ci_low"] > 0)
    mech_underpowered = bool(not mech_pass and m_ci["mean"] > 0
                             and m_pos >= UTILITY_SEED_MIN)
    mech_fail = bool(not mech_pass and not mech_underpowered)

    w_ci = waveform["record_bootstrap"]
    wf_confirmatory = bool(w_ci["ci_low"] > 0)

    util_pass = bool(utility["pass"])
    if mech_pass and util_pass:
        action = ("MIT transport replication PASS -> proceed to the frozen "
                  "INCART 32-patient stage (still not a pristine external "
                  "confirmation)")
    elif mech_pass and not util_pass:
        action = ("mechanism replicates but raw-residual utility is absent -> "
                  "stop expanding the residual CNN")
    elif mech_fail and not util_pass:
        action = "mechanism and utility both fail -> stop the residual CNN path"
    else:
        action = ("underpowered: positive mean with a CI spanning 0 — record "
                  "as underpowered; do NOT add seeds as a substitute for "
                  "patients")
    return {
        "mechanism": {"pass": mech_pass, "underpowered": mech_underpowered,
                      "fail": mech_fail, "ci": m_ci,
                      "seeds_positive": int(m_pos)},
        "waveform_specific": {"confirmatory": wf_confirmatory, "ci": w_ci},
        "utility": utility,
        "action": action,
    }


def evaluate_utility_gate(c_s2: Dict[int, Dict[int, float]],
                          arm_a: Dict[int, float],
                          n_boot: int = NB_BOOT) -> Dict[str, object]:
    """Pre-registered gate: mean gain >= +0.015, CI low > 0, seeds >= 4/5
    positive, and p10 non-inferiority within P10_TOL — all simultaneously."""
    seeds = sorted(c_s2)
    per_seed_a = {s: dict(arm_a) for s in seeds}     # A is seed-invariant
    con = contrast(c_s2, per_seed_a, n_boot=n_boot)
    ci = con["record_bootstrap"]
    seeds_pos = sum(1 for v in con["by_seed"] if v > 0)
    c_mean = seed_mean_by_record(c_s2)
    p10_c = p10(list(c_mean.values()))
    p10_a = p10(list(arm_a.values()))
    checks = {
        "mean_gain_ge_threshold": bool(ci["mean"] >= UTILITY_MIN_GAIN),
        "ci_low_gt_0": bool(ci["ci_low"] > 0),
        "seed_direction_ok": bool(seeds_pos >= UTILITY_SEED_MIN),
        "p10_non_inferior": bool(p10_c >= p10_a - P10_TOL),
    }
    return {"contrast_c_minus_a": con, "p10_c": p10_c, "p10_a": p10_a,
            "checks": checks, "seeds_positive": int(seeds_pos),
            "threshold": UTILITY_MIN_GAIN,
            "pass": bool(all(checks.values()))}


# ─────────────────────────────────────────────────────────────────────────────
# The replication run (Arms C/D under S0 and S2, SEL1, DS1->DS2).
# ─────────────────────────────────────────────────────────────────────────────
def run_replication(cohort: Cohort, feats: np.ndarray,
                    provenance: Dict[str, object], out_dir: str,
                    seeds: Sequence[int] = SEEDS, epochs: int = N_EPOCHS,
                    batch: int = DL_BATCH, n_boot: int = NB_BOOT,
                    device: Optional[str] = None, smoke: bool = False,
                    log: Optional[RunLog] = None) -> Dict[str, object]:
    """Everything pre-registered is fixed here: split, seeds, 24-epoch
    trajectories, two schedules, SEL1 only, epoch -1 candidacy. DS2 labels are
    never read before checkpoints are fixed by dev."""
    torch = _require_torch()
    log = log or RunLog()
    if device is None:
        device = "cuda" if torch.cuda.is_available() else "cpu"
    os.makedirs(out_dir, exist_ok=True)
    t_start = time.time()

    split = mit_split(cohort)
    fit_idx = samples_of(cohort, split["fit"])
    dev_idx = samples_of(cohort, split["dev"])
    ds2_idx = samples_of(cohort, split["ds2"])
    log(f"{EXPERIMENT_ID}/{ARM_ID} — device {device}, {len(seeds)} seeds, "
        f"{epochs} epochs, smoke={smoke}; fit {len(split['fit'])}p / dev "
        f"{len(split['dev'])}p / DS2 {len(split['ds2'])}p")

    offset, arm_a_logits = ds1_offsets_and_arm_a(feats, cohort, split, log=log)

    X_c = current_beat_input(cohort)
    shuffled, perm_rule = shuffle_waveforms_within_record(cohort)
    X_d = current_beat_input(cohort, beat=shuffled)

    history: List[dict] = []
    store: Dict[str, Dict[str, Dict[int, np.ndarray]]] = \
        {a: {s: {} for s in QQ_SCHEDULES} for a in QQ_ARMS}
    results_raw: Dict[str, Dict[str, Dict[int, dict]]] = \
        {a: {s: {} for s in QQ_SCHEDULES} for a in QQ_ARMS}

    for arm, X in ((ARM_C, X_c), (ARM_D, X_d)):
        for seed in seeds:
            for sch in QQ_SCHEDULES:
                set_determinism(int(seed))          # paired init across schedules
                net = build_residual_net(X.shape[1], init="normal")
                res = diagnostic_train_one_fold(
                    net, X, offset, cohort.y.astype("float32"), cohort.rid,
                    fit_idx, dev_idx, ds2_idx, int(seed), device, sch,
                    epochs=epochs, batch=batch, log=log)
                ep = res["selected"][SELECTOR]
                logits = np.full(cohort.n, np.nan)
                logits[ds2_idx] = res["test_logits_by_epoch"][ep]
                store[arm][sch][int(seed)] = logits
                results_raw[arm][sch][int(seed)] = res
                for cp in res["checkpoints"]:
                    history.append({"arm": arm, "schedule": sch,
                                    "seed": int(seed), **cp})
                log(f"  {arm}/{sch}/seed {seed}: selected epoch {ep}")

    # ── endpoints (primary: record-macro S PR-AUC; secondary: k-sweep) ──────
    ds2 = split["ds2"]
    a_prauc = per_record_s_prauc(arm_a_logits, cohort, ds2)
    a_ksw = per_record_ksw(arm_a_logits, cohort, ds2)
    endpoint_records = sorted(a_prauc)

    def prauc_by_seed(arm: str, sch: str) -> Dict[int, Dict[int, float]]:
        return {s: per_record_s_prauc(store[arm][sch][s], cohort,
                                      endpoint_records) for s in map(int, seeds)}

    pr = {arm: {sch: prauc_by_seed(arm, sch) for sch in QQ_SCHEDULES}
          for arm in QQ_ARMS}
    a_per_seed = {int(s): dict(a_prauc) for s in seeds}

    cd = {sch: contrast(pr[ARM_C][sch], pr[ARM_D][sch], n_boot)
          for sch in QQ_SCHEDULES}
    ca = {sch: contrast(pr[ARM_C][sch], a_per_seed, n_boot)
          for sch in QQ_SCHEDULES}
    da = {sch: contrast(pr[ARM_D][sch], a_per_seed, n_boot)
          for sch in QQ_SCHEDULES}

    def did(pair_hi, pair_lo):
        seeds_i = sorted(pair_hi)
        recs = sorted(next(iter(pair_hi.values())))
        return contrast(
            {s: {r: pair_hi[s][r] for r in recs} for s in seeds_i},
            {s: {r: pair_lo[s][r] for r in recs} for s in seeds_i}, n_boot)

    cd_s2 = {s: {r: pr[ARM_C]["S2_alpha_low"][s][r]
                 - pr[ARM_D]["S2_alpha_low"][s][r] for r in endpoint_records}
             for s in map(int, seeds)}
    cd_s0 = {s: {r: pr[ARM_C]["S0_original"][s][r]
                 - pr[ARM_D]["S0_original"][s][r] for r in endpoint_records}
             for s in map(int, seeds)}
    mechanism = did(cd_s2, cd_s0)
    waveform = cd["S2_alpha_low"]
    utility = evaluate_utility_gate(pr[ARM_C]["S2_alpha_low"], a_prauc, n_boot)
    decision = evaluate_decision_matrix(mechanism, waveform, utility)
    log(f"decision: {decision['action']}")

    best_epochs = {arm: {sch: [int(results_raw[arm][sch][int(s)]["selected"][SELECTOR])
                               for s in seeds] for sch in QQ_SCHEDULES}
                   for arm in QQ_ARMS}

    selected_rows = [
        {"arm": arm, "schedule": sch, "seed": int(s),
         "selected_epoch": int(results_raw[arm][sch][int(s)]["selected"][SELECTOR])}
        for arm in QQ_ARMS for sch in QQ_SCHEDULES for s in seeds]

    result = {
        "experiment_id": EXPERIMENT_ID, "arm_id": ARM_ID,
        "status": STATUS if smoke else "MEASURED",
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "smoke": bool(smoke), "selector": SELECTOR,
        "n_epochs": int(epochs), "schedules": {s: SCHEDULES[s]
                                               for s in QQ_SCHEDULES},
        "split": {k: list(map(int, v)) for k, v in split.items()},
        "primary_metric": "record_macro_s_prauc",
        "endpoint_records": list(map(int, endpoint_records)),
        "arm_a": {"prauc_by_record": {str(r): a_prauc[r] for r in a_prauc},
                  "ksw_by_record": {str(r): a_ksw[r] for r in a_ksw}},
        "best_epochs": best_epochs,
        "contrasts": {"c_minus_d": cd, "c_minus_a": ca, "d_minus_a": da},
        "mechanism_did_cd_s2_minus_s0": mechanism,
        "waveform_specific_c_minus_d_s2": waveform,
        "utility_gate": utility,
        "decision_matrix": decision,
        "perm_rule": perm_rule,
        "note": ("Pre-registered transportability replication. DS2 was "
                 "evaluated exactly once with dev-frozen checkpoints; nothing "
                 "was tuned on DS2."),
    }

    _write_bundle(out_dir, cohort, split, seeds, provenance, result, history,
                  store, arm_a_logits, selected_rows, t_start, log)
    _write_figures_and_report(out_dir, result, history, log)
    verify_bundle(out_dir)
    log(f"bundle complete: {out_dir}")
    return result


def _write_bundle(out_dir, cohort, split, seeds, provenance, result, history,
                  store, arm_a_logits, selected_rows, t_start, log) -> None:
    import csv
    manifest = dict(provenance)
    manifest["wall_time_s"] = float(time.time() - t_start)
    npz_payload = {
        "seeds": np.array([int(s) for s in seeds]),
        "record_id": cohort.rid, "sample_id": cohort.sample_id,
        "y_true": cohort.y,
        "split_ds2_mask": np.isin(cohort.rid, split["ds2"]),
        "logit_morph_baseline": arm_a_logits,
    }
    for arm in QQ_ARMS:
        for sch in QQ_SCHEDULES:
            npz_payload[f"logit_{arm}__{sch}__{SELECTOR}"] = np.stack(
                [store[arm][sch][int(s)] for s in seeds])
    np.savez_compressed(os.path.join(out_dir, "predictions.npz"), **npz_payload)

    with open(os.path.join(out_dir, "split_map.json"), "w", encoding="utf-8") as fh:
        json.dump({k: list(map(int, v)) for k, v in split.items()}, fh, indent=1)
    config = {"experiment_id": EXPERIMENT_ID, "schedules": list(QQ_SCHEDULES),
              "selector": SELECTOR, "seeds": [int(s) for s in seeds],
              "n_epochs": int(result["n_epochs"]),
              "utility_gate": {"min_gain": UTILITY_MIN_GAIN,
                               "seed_min": UTILITY_SEED_MIN,
                               "p10_tol": P10_TOL}}
    for name, obj in (("config.json", config), ("manifest.json", manifest),
                      ("result.json", result)):
        with open(os.path.join(out_dir, name), "w", encoding="utf-8") as fh:
            json.dump(_json_safe(obj), fh, ensure_ascii=False, indent=1)
    with open(os.path.join(out_dir, "training_history.json"), "w",
              encoding="utf-8") as fh:
        json.dump(_json_safe([{k: v for k, v in h.items()
                               if not isinstance(v, np.ndarray)}
                              for h in history]), fh, indent=1)

    cols = ["arm", "schedule", "seed", "epoch", "optimizer_steps",
            "train_pooled_bce", "dev_pooled_bce", "dev_record_bce", "alpha"]
    with open(os.path.join(out_dir, "trajectory_table.csv"), "w", newline="",
              encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(cols)
        for h in history:
            w.writerow([h.get(c, "") for c in cols])
    with open(os.path.join(out_dir, "checkpoint_table.csv"), "w", newline="",
              encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["arm", "schedule", "seed", "selected_epoch", "selector"])
        for row in selected_rows:
            w.writerow([row["arm"], row["schedule"], row["seed"],
                        row["selected_epoch"], SELECTOR])
    log("bundle files written")


def bundle_fingerprint(run_dir: str, files: Sequence[str]) -> Dict[str, str]:
    out = {}
    for f in files:
        p = os.path.join(run_dir, f)
        if os.path.exists(p):
            out[f] = sha256_file(p)
    return out


def verify_bundle(out_dir: str) -> None:
    missing = [f for f in BUNDLE_FILES if not os.path.exists(
        os.path.join(out_dir, f))]
    if missing:
        raise Q4QError(f"bundle incomplete, missing {missing}")
    figdir = os.path.join(out_dir, "figures")
    missing_fig = [f for f in FIGURES if not os.path.exists(
        os.path.join(figdir, f))]
    if missing_fig:
        raise Q4QError(f"figures incomplete, missing {missing_fig}")


# ─────────────────────────────────────────────────────────────────────────────
# Q4-P no-retrain derived analysis (spec §3). Reads the Q4-P bundle read-only.
# ─────────────────────────────────────────────────────────────────────────────
Q4P_SOURCE_FILES = ("predictions.npz", "result.json", "manifest.json")


def q4p_derived_analysis(q4p_run_dir: str, out_dir: str,
                         n_boot: int = NB_BOOT,
                         log: Optional[RunLog] = None) -> Dict[str, object]:
    """Post-hoc mechanism statistics from Q4-P's stored predictions ONLY.

    * metric: Q4-P's k-sweep achievement (original contract comparability);
    * outputs go to a NEW versioned directory — never into the source bundle;
    * the source bundle is fingerprinted before and after (immutability);
    * these numbers are post-hoc mechanism analysis and do NOT change Q4-P's
      pre-registered verdict (B3).
    """
    log = log or RunLog()
    q4p_run_dir = os.path.abspath(q4p_run_dir)
    out_dir = os.path.abspath(out_dir)
    if out_dir == q4p_run_dir or out_dir.startswith(q4p_run_dir + os.sep):
        raise Q4QError("derived output must be a NEW path outside the Q4-P "
                       "bundle (spec §3)")
    pred_path = os.path.join(q4p_run_dir, "predictions.npz")
    if not os.path.exists(pred_path):
        raise Q4QError(f"predictions.npz not found in {q4p_run_dir}")
    fp_before = bundle_fingerprint(q4p_run_dir, Q4P_SOURCE_FILES)
    os.makedirs(out_dir, exist_ok=True)

    with np.load(pred_path) as npz:
        seeds = [int(s) for s in npz["seeds"]]
        rid = np.asarray(npz["record_id"]).astype(int)
        y = np.asarray(npz["y_true"]).astype(bool)
        scored = np.asarray(npz["scored_mask"]).astype(bool)
        arm_a = np.asarray(npz["logit_morph_baseline"], float)

        def ksw_by_record(scores: np.ndarray) -> Dict[int, float]:
            recs = sorted(set(rid[scored].tolist()))
            out = {}
            for r in recs:
                idx = np.where((rid == r) & scored)[0]
                out[int(r)] = float(np.mean(
                    [achievement_at(scores, idx, y, k) for k in K_SWEEP]))
            return out

        def per_seed(arm: str, sch: str) -> Dict[int, Dict[int, float]]:
            key = f"logit_{arm}__{sch}__{SEL1}"
            if key not in npz:
                raise Q4QError(f"Q4-P predictions.npz missing {key}")
            mat = np.asarray(npz[key], float)
            return {seeds[i]: ksw_by_record(mat[i]) for i in range(len(seeds))}

        c_s0 = per_seed("morph_plus_raw_residual", "S0_original")
        c_s2 = per_seed("morph_plus_raw_residual", "S2_alpha_low")
        d_s0 = per_seed("shuffled_waveform_control", "S0_original")
        d_s2 = per_seed("shuffled_waveform_control", "S2_alpha_low")
        a_rec = ksw_by_record(arm_a)

    recs = sorted(a_rec)
    a_ps = {s: dict(a_rec) for s in seeds}

    def minus(x, ref):
        return {s: {r: x[s][r] - ref[s][r] for r in recs} for s in seeds}

    did_cd = contrast(minus(c_s2, d_s2), minus(c_s0, d_s0), n_boot)
    did_ca = contrast(minus(c_s2, a_ps), minus(c_s0, a_ps), n_boot)
    ca_s2 = contrast(c_s2, a_ps, n_boot)
    da_s2 = contrast(d_s2, a_ps, n_boot)
    cd_s2 = contrast(c_s2, d_s2, n_boot)

    waterfall = {str(r): float(np.mean([c_s2[s][r] - d_s2[s][r]
                                        for s in seeds])) for r in recs}
    derived = {
        "kind": "q4p_post_hoc_mechanism_analysis",
        "source_run": os.path.basename(q4p_run_dir),
        "source_fingerprint": fp_before,
        "metric": "q4p_ksweep_achievement",
        "n_boot": int(n_boot), "seeds": seeds,
        "did_cd_s2_minus_s0": did_cd,
        "did_ca_s2_minus_s0": did_ca,
        "decomposition_s2": {"c_minus_a": ca_s2, "d_minus_a": da_s2,
                             "c_minus_d": cd_s2},
        "patient_waterfall_c_minus_d_s2": waterfall,
        "note": ("POST-HOC mechanism analysis of stored Q4-P predictions. "
                 "It does not change Q4-P's pre-registered verdict (B3) and "
                 "must not be quoted as a confirmatory result."),
    }
    with open(os.path.join(out_dir, "derived_analysis.json"), "w",
              encoding="utf-8") as fh:
        json.dump(_json_safe(derived), fh, ensure_ascii=False, indent=1)
    _write_derived_csv(out_dir, derived, recs)
    _write_derived_figures(out_dir, derived)

    fp_after = bundle_fingerprint(q4p_run_dir, Q4P_SOURCE_FILES)
    if fp_after != fp_before:
        raise Q4QError("Q4-P source bundle changed during derived analysis — "
                       "IMMUTABILITY VIOLATION, investigate before trusting "
                       "any output")
    derived["source_immutable"] = True
    log(f"derived analysis written to {out_dir} (source bundle unchanged)")
    return derived


def _write_derived_csv(out_dir: str, derived: dict, recs: Sequence[int]) -> None:
    import csv
    with open(os.path.join(out_dir, "derived_tables.csv"), "w", newline="",
              encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["table", "key", "mean", "ci_low", "ci_high"])
        for name in ("did_cd_s2_minus_s0", "did_ca_s2_minus_s0"):
            rb = derived[name]["record_bootstrap"]
            w.writerow([name, "record_bootstrap", rb["mean"], rb["ci_low"],
                        rb["ci_high"]])
        for k, v in derived["decomposition_s2"].items():
            rb = v["record_bootstrap"]
            w.writerow(["decomposition_s2", k, rb["mean"], rb["ci_low"],
                        rb["ci_high"]])
        w.writerow([])
        w.writerow(["waterfall_record", "c_minus_d_s2_mean"])
        for r in recs:
            w.writerow([r, derived["patient_waterfall_c_minus_d_s2"][str(r)]])


def _plt():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    return plt


def _write_derived_figures(out_dir: str, derived: dict) -> None:
    plt = _plt()
    fig, axes = plt.subplots(1, 2, figsize=(11, 4))
    names = ["(C-D): S2-S0", "(C-A): S2-S0", "C-A S2", "D-A S2", "C-D S2"]
    cis = [derived["did_cd_s2_minus_s0"], derived["did_ca_s2_minus_s0"],
           derived["decomposition_s2"]["c_minus_a"],
           derived["decomposition_s2"]["d_minus_a"],
           derived["decomposition_s2"]["c_minus_d"]]
    for i, (nm, c) in enumerate(zip(names, cis)):
        rb = c["record_bootstrap"]
        axes[0].errorbar(rb["mean"], i, xerr=[[rb["mean"] - rb["ci_low"]],
                                              [rb["ci_high"] - rb["mean"]]],
                         fmt="o", capsize=4)
    axes[0].axvline(0, color="k", lw=0.6)
    axes[0].set_yticks(range(len(names)), names)
    axes[0].set_title("Q4-P post-hoc DiD & decomposition\n"
                      "(SVDB, k-sweep, 56 records, 5 seeds, 95% record-"
                      "bootstrap CI) — POST-HOC, not confirmatory")
    wf = sorted(derived["patient_waterfall_c_minus_d_s2"].values())
    axes[1].bar(range(len(wf)), wf, width=0.9)
    axes[1].axhline(0, color="k", lw=0.6)
    axes[1].set_title("patient waterfall: mean (C-D) under S2")
    fig.tight_layout()
    fig.savefig(os.path.join(out_dir, "derived_forest_waterfall.png"), dpi=110)
    plt.close(fig)


# ─────────────────────────────────────────────────────────────────────────────
# Figures for the replication bundle.
# ─────────────────────────────────────────────────────────────────────────────
def _write_figures_and_report(out_dir: str, result: dict, history: List[dict],
                              log) -> None:
    plt = _plt()
    figdir = os.path.join(out_dir, "figures")
    os.makedirs(figdir, exist_ok=True)
    sub = (f"MIT-BIH DS1->DS2 · arms A/C/D · {'/'.join(QQ_SCHEDULES)} · "
           f"{len(result['split']['ds2'])} DS2 patients · "
           f"{len(SEEDS)} seeds · 95% record-bootstrap CI · S PR-AUC")

    def table_fig(name, rows, title):
        fig, ax = plt.subplots(figsize=(9, 0.5 + 0.35 * len(rows)))
        ax.axis("off")
        ax.table(cellText=[[str(c) for c in r] for r in rows],
                 loc="center", cellLoc="left")
        ax.set_title(f"{title}\n{sub}", fontsize=9)
        fig.savefig(os.path.join(figdir, name), dpi=110,
                    bbox_inches="tight")
        plt.close(fig)

    split = result["split"]
    table_fig("data_audit_split_table.png",
              [["set", "n_patients", "records"],
               ["DS1-fit", len(split["fit"]), split["fit"]],
               ["DS1-dev", len(split["dev"]), split["dev"]],
               ["DS2", len(split["ds2"]), split["ds2"]]],
              "frozen split")
    table_fig("class_patient_counts.png",
              [["endpoint records (both classes)",
                len(result["endpoint_records"])],
               ["records", result["endpoint_records"]]],
              "class/patient counts")
    rows = [["arm", "schedule", "C-D mean", "ci_low", "ci_high"]]
    for sch in QQ_SCHEDULES:
        rb = result["contrasts"]["c_minus_d"][sch]["record_bootstrap"]
        rows.append(["C-D", sch, f"{rb['mean']:+.6f}", f"{rb['ci_low']:+.6f}",
                     f"{rb['ci_high']:+.6f}"])
        rb = result["contrasts"]["c_minus_a"][sch]["record_bootstrap"]
        rows.append(["C-A", sch, f"{rb['mean']:+.6f}", f"{rb['ci_low']:+.6f}",
                     f"{rb['ci_high']:+.6f}"])
    table_fig("arm_schedule_table.png", rows, "arm x schedule PR-AUC contrasts")

    fig, ax = plt.subplots(figsize=(8, 4))
    for sch in QQ_SCHEDULES:
        hs = [h for h in history if h["schedule"] == sch
              and h["arm"] == ARM_C and h.get("epoch", -2) >= 0]
        if hs:
            eps = sorted(set(h["epoch"] for h in hs))
            dv = [np.mean([h["dev_record_bce"] for h in hs
                           if h["epoch"] == e]) for e in eps]
            tr = [np.mean([h["train_pooled_bce"] for h in hs
                           if h["epoch"] == e]) for e in eps]
            ax.plot(eps, dv, label=f"dev {sch}")
            ax.plot(eps, tr, "--", label=f"train {sch}")
    ax.legend(fontsize=7)
    ax.set_title(f"learning curves (Arm C)\n{sub}", fontsize=9)
    fig.savefig(os.path.join(figdir, "learning_curves.png"), dpi=110)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(7, 4))
    width = 0.35
    for i, sch in enumerate(QQ_SCHEDULES):
        eps = result["best_epochs"][ARM_C][sch]
        vals, cnts = np.unique(eps, return_counts=True)
        ax.bar(vals + i * width, cnts, width=width, label=sch)
    ax.axvline(-0.5, color="r", lw=0.8)
    ax.set_xlabel("selected epoch (-1 = pre-training)")
    ax.legend(fontsize=8)
    ax.set_title(f"best-epoch distribution (Arm C, SEL1)\n{sub}", fontsize=9)
    fig.savefig(os.path.join(figdir, "best_epoch_distribution.png"), dpi=110)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(7, 4))
    items = [("DiD (C-D) S2-S0", result["mechanism_did_cd_s2_minus_s0"]),
             ("C-D S2", result["waveform_specific_c_minus_d_s2"]),
             ("C-D S0", result["contrasts"]["c_minus_d"]["S0_original"])]
    for i, (nm, c) in enumerate(items):
        rb = c["record_bootstrap"]
        ax.errorbar(rb["mean"], i, xerr=[[rb["mean"] - rb["ci_low"]],
                                         [rb["ci_high"] - rb["mean"]]],
                    fmt="o", capsize=4)
    ax.axvline(0, color="k", lw=0.6)
    ax.set_yticks(range(len(items)), [n for n, _ in items])
    ax.set_title(f"forest: mechanism DiD and C-D\n{sub}", fontsize=9)
    fig.savefig(os.path.join(figdir, "c_minus_d_did_forest.png"), dpi=110)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(6, 4))
    for i, (nm, c) in enumerate([("DiD", result["mechanism_did_cd_s2_minus_s0"]),
                                 ("C-A S2", result["contrasts"]["c_minus_a"]
                                  ["S2_alpha_low"])]):
        ax.scatter([i] * len(c["by_seed"]), c["by_seed"], s=30)
    ax.axhline(0, color="k", lw=0.6)
    ax.set_xticks([0, 1], ["DiD (C-D) S2-S0", "C-A S2"])
    ax.set_title(f"per-seed direction\n{sub}", fontsize=9)
    fig.savefig(os.path.join(figdir, "seed_direction.png"), dpi=110)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(8, 4))
    wf = result["utility_gate"]
    a_map = result["arm_a"]["prauc_by_record"]
    diffs = sorted(float(v) for v in result["waveform_specific_c_minus_d_s2"]
                   ["per_record_mean_diff"].values())
    ax.bar(range(len(diffs)), diffs, width=0.9)
    ax.axhline(0, color="k", lw=0.6)
    ax.set_title(f"patient waterfall C-D S2 · p10: C {wf['p10_c']:.3f} vs "
                 f"A {wf['p10_a']:.3f} (tol {P10_TOL})\n{sub}", fontsize=9)
    fig.savefig(os.path.join(figdir, "patient_waterfall_p10.png"), dpi=110)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(6, 4))
    vals = sorted(float(v) for v in a_map.values())
    ax.plot(vals, np.linspace(0, 1, len(vals)), label="Arm A per-record PR-AUC")
    ax.legend(fontsize=8)
    ax.set_title(f"PR/calibration summary view\n{sub}", fontsize=9)
    fig.savefig(os.path.join(figdir, "pr_curves_calibration.png"), dpi=110)
    plt.close(fig)

    dm = result["decision_matrix"]
    table_fig("decision_matrix.png",
              [["gate", "value"],
               ["mechanism pass", dm["mechanism"]["pass"]],
               ["mechanism underpowered", dm["mechanism"]["underpowered"]],
               ["waveform-specific confirmatory",
                dm["waveform_specific"]["confirmatory"]],
               ["utility pass", dm["utility"]["pass"]],
               ["action", dm["action"]]],
              "pre-registered decision matrix (auto)")

    with open(os.path.join(figdir, "report_summary.md"), "w",
              encoding="utf-8") as fh:
        fh.write(f"# {EXPERIMENT_ID} / {ARM_ID} report\n\n"
                 f"status: {result['status']} (smoke={result['smoke']})\n\n"
                 f"decision: {dm['action']}\n")
    log("figures written")


# ─────────────────────────────────────────────────────────────────────────────
# Synthetic cohort for CPU smoke (no scientific meaning).
# ─────────────────────────────────────────────────────────────────────────────
def synthetic_mit(n_beat_per_record: int = 80, width: int = 64,
                  seed: int = 11) -> Tuple[Cohort, np.ndarray]:
    """A 44-record synthetic cohort whose rid values are the canonical MIT
    record numbers, so the frozen split logic runs unchanged.

    ``n_beat_per_record`` must stay >= 80: Q4-O's ``synthetic_cohort`` redraws
    labels until each record clears MIN_S/MIN_N (25/25), which cannot terminate
    for small records."""
    if n_beat_per_record < 80:
        raise Q4QError("synthetic_mit needs n_beat_per_record >= 80 "
                       "(Q4-O synthetic_cohort redraws until >=25 S and >=25 "
                       "non-S per record)")
    base = Q4O.synthetic_cohort(n_record=44, n_beat=n_beat_per_record,
                                width=width, seed=seed)
    rid = np.array([MIT_ALL_RECORDS[int(r)] for r in base.rid], int)
    cohort = Cohort(
        beat=base.beat, y=base.y, y3=base.y3, pre=base.pre, post=base.post,
        rid=rid, sym=base.sym, sample_id=base.sample_id,
        records=np.array(sorted(set(rid.tolist())), int),
        idx_of={int(r): np.where(rid == r)[0]
                for r in sorted(set(rid.tolist()))},
    )
    rng = np.random.RandomState(seed + 1)
    feats = np.c_[cohort.beat.mean(axis=(1, 2)), cohort.beat.std(axis=(1, 2)),
                  rng.normal(size=(cohort.n, 3))]
    feats[:, 0] += 0.8 * cohort.y            # informative morphology proxy
    return cohort, feats


# ─────────────────────────────────────────────────────────────────────────────
# Self-check and CLI.
# ─────────────────────────────────────────────────────────────────────────────
def self_check(min_version: int = MODULE_VERSION) -> Dict[str, object]:
    if MODULE_VERSION < min_version:
        raise Q4QError(f"stale module {MODULE_VERSION} < {min_version}")
    for s in QQ_SCHEDULES:
        if s not in SCHEDULES:
            raise Q4QError(f"schedule {s} missing from Q4-P")
    ok_map = {f"I{i:02d}": (i - 1) // 3 + 1 for i in range(1, 76)}
    if len(set(ok_map.values())) != 25:      # sanity of the fixture only
        raise Q4QError("self-check fixture broken")
    return {"module_file": os.path.abspath(__file__),
            "module_version": MODULE_VERSION, "module_build": MODULE_BUILD,
            "modes": list(MODES), "schedules": list(QQ_SCHEDULES),
            "selector": SELECTOR, "status": STATUS}


def provenance_for(data_path: str) -> Dict[str, object]:
    return {"data": {"abs_path": os.path.abspath(data_path),
                     "file_name": os.path.basename(data_path),
                     "sha256": sha256_file(data_path),
                     "size_bytes": os.path.getsize(data_path)},
            "git_commit_sha": git_commit_sha(),
            "packages": package_versions(), "gpu": gpu_info()}


def main(argv: Optional[Sequence[str]] = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--mode", required=True,
                    help=f"exactly one of {MODES}; default workflow starts "
                         "with DESIGN")
    ap.add_argument("--data", help="mamba_data.npz path")
    ap.add_argument("--multi", help="ecg_multi.npz path (PREP_DATA cross-check)")
    ap.add_argument("--incart-hea", help="INCART .hea directory (PREP_DATA)")
    ap.add_argument("--q4p-run", help="Q4-P run dir (ANALYZE)")
    ap.add_argument("--out", help="output directory")
    ap.add_argument("--epochs", type=int, default=None)
    ap.add_argument("--n-boot", type=int, default=NB_BOOT)
    args = ap.parse_args(argv)
    mode = resolve_mode(args.mode)
    log = RunLog()

    if mode == "DESIGN":
        info = self_check()
        log(f"{EXPERIMENT_ID}/{ARM_ID} DESIGN — {STATUS}")
        log(json.dumps(info, indent=1))
        return 0

    if mode == "SMOKE":
        if not args.out:
            raise Q4QError("SMOKE needs --out")
        cohort, feats = synthetic_mit()
        prov = {"data": {"synthetic": True}, "git_commit_sha": git_commit_sha(),
                "packages": package_versions(), "gpu": gpu_info()}
        run_replication(cohort, feats, prov, args.out,
                        seeds=SEEDS[:2], epochs=args.epochs or 2,
                        n_boot=200, smoke=True, log=log)
        return 0

    if mode == "PREP_DATA":
        if not args.data or not args.out:
            raise Q4QError("PREP_DATA needs --data and --out")
        os.makedirs(args.out, exist_ok=True)
        cohort, feats, audit = load_mit_cohort(args.data, log=log)
        split = mit_split(cohort)
        audit["split"] = {k: list(map(int, v)) for k, v in split.items()}
        if args.multi:
            # strict=False: write the FULL audit (incl. the side-by-side
            # fingerprint table) before stopping, so a failed gate always
            # leaves complete diagnostics behind.
            audit["cross_check"] = cross_check_mit_vs_multi(
                audit, args.multi, log=log, strict=False)
        else:
            audit["cross_check"] = {"pass": False,
                                    "note": "NOT RUN — provide --multi"}
        if args.incart_hea:
            mapping = parse_incart_patient_map(args.incart_hea, log=log)
            audit["incart_map"] = validate_incart_map(mapping)
            with open(os.path.join(args.out, "incart_patient_map.json"), "w",
                      encoding="utf-8") as fh:
                json.dump(mapping, fh, indent=1, sort_keys=True)
        audit["incart_adapter_audit"] = incart_adapter_audit()
        with open(os.path.join(args.out, "data_audit.json"), "w",
                  encoding="utf-8") as fh:
            json.dump(_json_safe(audit), fh, ensure_ascii=False, indent=1)
        log(f"PREP_DATA audit written to {args.out}")
        cc = audit["cross_check"]
        for row in cc.get("table", []):
            mark = " <-- " + row["warning"] if "warning" in row else ""
            log(f"  {row['mamba_record']:>3} -> multi {row['multi_record']:>3}"
                f"  n {row['n_mamba']:>5}/{row['n_multi']:>5}"
                f"  cls diff {row['class_abs_diff']}{mark}")
        for r, cls in cc.get("leftover_profiles", {}).items():
            log(f"  leftover multi {r}: classes {cls}")
        if args.multi and not cc["pass"]:
            raise Q4QError(
                "PREP_DATA gate FAILED: " + " | ".join(cc["fail_reasons"])
                + f" — full table in {args.out}/data_audit.json")
        return 0

    if mode == "FULL":
        if not args.data or not args.out:
            raise Q4QError("FULL needs --data and --out")
        cohort, feats, _ = load_mit_cohort(args.data, log=log)
        run_replication(cohort, feats, provenance_for(args.data), args.out,
                        epochs=args.epochs or N_EPOCHS, n_boot=args.n_boot,
                        smoke=False, log=log)
        return 0

    if mode == "ANALYZE":
        if not args.q4p_run or not args.out:
            raise Q4QError("ANALYZE needs --q4p-run and --out")
        q4p_derived_analysis(args.q4p_run, args.out, n_boot=args.n_boot,
                             log=log)
        return 0
    raise Q4QError(f"unhandled mode {mode}")     # pragma: no cover


if __name__ == "__main__":
    sys.exit(main())
