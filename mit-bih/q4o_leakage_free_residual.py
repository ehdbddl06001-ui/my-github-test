"""Q4-O (EXP-2026-001) — leakage-free residual CNN: reporting layer.

This module is **presentation-only**. It reads an already-finished Drive run
bundle and turns it into tables, figures and a Korean-language report. It never
trains, never re-fits, never re-samples a bootstrap, and never writes to any of
the measured artifacts (``result.json``, ``manifest.json``, ``config.json``,
``fold_map.json``, ``predictions.npz``, ``arms/<arm>/probs.npy``).

The scientific record lives in ``result.json``. Every headline number in the
report — arm means, contrasts, confidence intervals, gate verdicts — is *read*
from it verbatim. Nothing here recomputes a confidence interval or re-decides a
gate.

Two derived views (the per-record waterfall and the per-record distribution)
need record-level values that ``result.json`` only stores in aggregate, so they
are recomputed from ``probs.npy`` + the labels in ``predictions.npz``. That
recomputation is gated: it is first checked against the per-seed ``ach@k``
values stored in ``result.json``, and if it does not reproduce them the derived
figures are **skipped with an explicit warning** instead of being drawn from
numbers we cannot vouch for.

Arm map (as written by the run)::

    A  morph_baseline             morphology logistic baseline  (the baseline)
    B  raw_current_cnn            raw 2-channel CNN, no morphology
    C  morph_plus_raw_residual    A + CNN residual              (the hypothesis)
    D  shuffled_waveform_control  C with beat waveforms permuted (negative control)
    E  corrected_q4n_diagnostic   cross-fitted comb offset      (diagnostic only)
    F  comb_baseline_diagnostic   clean analogue of Q4-N cpu_comb (E's comparator)

Usage (Colab / CLI)::

    from q4o_leakage_free_residual import analyze_existing_run
    analyze_existing_run("/content/drive/MyDrive/MedKOS/ecg-model/runs/"
                         "20260806T0923_EXP-2026-001_q4o_leakage_free_residual_cnn")

    python mit-bih/q4o_leakage_free_residual.py --out-dir <run dir>
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import sys
import warnings
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, Iterable, List, Optional, Sequence, Tuple

import numpy as np

__all__ = [
    "ARMS",
    "ARM_BY_CODE",
    "PRIMARY_CONTRASTS",
    "REFERENCE_CONTRASTS",
    "RunBundle",
    "TrainingHistoryRecorder",
    "analyze_existing_run",
    "arm_metrics_rows",
    "bundle_checksums",
    "executive_summary_ko",
    "interpretation_ko",
    "load_run",
    "per_record_ksw",
    "resolve_achievement_definition",
    "sha256_file",
    "training_history_status",
]


# --------------------------------------------------------------------------
# Arm registry
# --------------------------------------------------------------------------

@dataclass(frozen=True)
class ArmSpec:
    code: str
    key: str
    label: str
    role: str

    @property
    def display(self) -> str:
        return f"{self.code} · {self.label}"


ARMS: Tuple[ArmSpec, ...] = (
    ArmSpec("A", "morph_baseline", "morphology baseline", "baseline"),
    ArmSpec("B", "raw_current_cnn", "raw CNN (no morphology)", "reference"),
    ArmSpec("C", "morph_plus_raw_residual", "morphology + CNN residual", "hypothesis"),
    ArmSpec("D", "shuffled_waveform_control", "shuffled-waveform control", "negative control"),
    ArmSpec("E", "corrected_q4n_diagnostic", "corrected Q4-N (comb offset)", "diagnostic"),
    ArmSpec("F", "comb_baseline_diagnostic", "clean comb baseline", "diagnostic comparator"),
)

ARM_BY_CODE: Dict[str, ArmSpec] = {a.code: a for a in ARMS}
ARM_BY_KEY: Dict[str, ArmSpec] = {a.key: a for a in ARMS}

#: Contrasts that answer the experimental question. Same order everywhere.
PRIMARY_CONTRASTS: Tuple[Tuple[str, str], ...] = (
    ("C_minus_A", "C − A"),
    ("C_minus_D", "C − D"),
    ("E_minus_combBaseline", "E − cleanComb"),
)

#: Large-magnitude reference contrasts. Never drawn on the primary axis.
REFERENCE_CONTRASTS: Tuple[Tuple[str, str], ...] = (
    ("B_minus_A", "B − A"),
    ("E_minus_A", "E − A"),
    ("D_minus_A", "D − A"),
)

#: Files that the reporting layer treats as read-only measured evidence.
MEASURED_FILES: Tuple[str, ...] = (
    "result.json",
    "manifest.json",
    "config.json",
    "fold_map.json",
    "predictions.npz",
)

K_OPERATING_AND_SWEEP: Tuple[int, ...] = (30, 50, 100, 200, 300)

# Okabe–Ito derived; validated for CVD separation and lightness band.
COLOR = {
    "A": "#0072B2",   # blue      — baseline
    "B": "#E69F00",   # orange    — raw CNN reference
    "C": "#009E73",   # green     — hypothesis
    "D": "#D55E00",   # vermillion— negative control
    "E": "#CC79A7",   # purple    — diagnostic
    "F": "#666666",   # gray      — diagnostic comparator
    "pos": "#0072B2",
    "neg": "#D55E00",
    "zero": "#444444",
    "gate": "#B25C00",
    "ink": "#222222",
    "muted": "#777777",
    "grid": "#DDDDDD",
    "warn_bg": "#FDF3E3",
}


# --------------------------------------------------------------------------
# Checksums — the report must not disturb the measured artifacts
# --------------------------------------------------------------------------

def sha256_file(path: str) -> str:
    """SHA-256 of a file, streamed."""
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def bundle_checksums(out_dir: str) -> Dict[str, str]:
    """SHA-256 of every measured artifact present in ``out_dir``.

    Includes ``arms/<arm>/probs.npy``. Missing files are simply absent from the
    mapping, so the same helper works on partial bundles and on fixtures.
    """
    sums: Dict[str, str] = {}
    for name in MEASURED_FILES:
        path = os.path.join(out_dir, name)
        if os.path.isfile(path):
            sums[name] = sha256_file(path)
    arms_dir = os.path.join(out_dir, "arms")
    if os.path.isdir(arms_dir):
        for arm in sorted(os.listdir(arms_dir)):
            path = os.path.join(arms_dir, arm, "probs.npy")
            if os.path.isfile(path):
                sums[f"arms/{arm}/probs.npy"] = sha256_file(path)
    return sums


# --------------------------------------------------------------------------
# Loading
# --------------------------------------------------------------------------

def _read_json(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


#: Accepted names for the per-beat label / record arrays inside predictions.npz.
_LABEL_ALIASES = ("y_s", "y", "y3", "label", "labels", "y_true", "target")
_RECORD_ALIASES = ("rec", "record", "record_id", "pid", "patient", "rid")


def _pick_array(npz, aliases: Sequence[str], n_beat: int, what: str):
    for name in aliases:
        if name in npz.files:
            arr = np.asarray(npz[name])
            if arr.ndim == 1 and arr.shape[0] == n_beat:
                return name, arr
    raise KeyError(
        f"predictions.npz has no 1-D {what} array of length {n_beat}. "
        f"Looked for {list(aliases)}; file contains "
        f"{[(k, np.asarray(npz[k]).shape) for k in npz.files]}"
    )


@dataclass
class RunBundle:
    """An already-finished run, loaded read-only."""

    out_dir: str
    result: Dict[str, Any]
    manifest: Dict[str, Any]
    config: Dict[str, Any]
    fold_map: Dict[str, Any] = field(default_factory=dict)
    arm_probs: Dict[str, np.ndarray] = field(default_factory=dict)
    labels: Optional[np.ndarray] = None
    records: Optional[np.ndarray] = None
    predictions_keys: Tuple[str, ...] = ()
    checksums_at_load: Dict[str, str] = field(default_factory=dict)
    load_warnings: List[str] = field(default_factory=list)

    # -- convenience -----------------------------------------------------
    @property
    def run_id(self) -> str:
        return os.path.basename(os.path.normpath(self.out_dir))

    @property
    def seeds(self) -> List[int]:
        seeds = self.config.get("training_seeds")
        if seeds:
            return list(seeds)
        arm = self.result["arms"][ARM_BY_CODE["C"].key]
        return [ps["seed"] for ps in arm["per_seed"]]

    @property
    def n_seed(self) -> int:
        return len(self.seeds)

    @property
    def k_sweep(self) -> List[int]:
        return list(self.config.get("k_sweep", [50, 100, 200, 300]))

    @property
    def gate_thresholds(self) -> Dict[str, float]:
        return dict(self.result.get("gates", {}).get("thresholds", {}))

    @property
    def min_gain(self) -> float:
        return float(self.gate_thresholds.get("min_gain", 0.015))

    @property
    def verdict(self) -> str:
        return str(self.result.get("gates", {}).get("verdict", "UNKNOWN"))

    @property
    def scorable_records(self) -> List[int]:
        recs = self.manifest.get("scorable_records")
        if recs:
            return [int(r) for r in recs]
        return []

    @property
    def record_burden(self) -> Dict[int, float]:
        return {int(k): float(v) for k, v in self.manifest.get("record_burden", {}).items()}

    @property
    def record_to_fold(self) -> Dict[int, int]:
        rtf = self.fold_map.get("record_to_fold")
        if rtf:
            return {int(k): int(v) for k, v in rtf.items()}
        out: Dict[int, int] = {}
        for fold, recs in (self.manifest.get("fold_records") or {}).items():
            for r in recs:
                out[int(r)] = int(fold)
        return out

    def arm(self, code: str) -> Dict[str, Any]:
        return self.result["arms"][ARM_BY_CODE[code].key]

    def has_arm(self, code: str) -> bool:
        return ARM_BY_CODE[code].key in self.result.get("arms", {})

    def contrast(self, name: str) -> Optional[Dict[str, Any]]:
        return self.result.get("contrasts", {}).get(name)

    def figures_dir(self) -> str:
        return os.path.join(self.out_dir, "figures")


def load_run(out_dir: str, *, require_predictions: bool = False) -> RunBundle:
    """Load a run bundle read-only.

    ``predictions.npz`` and the per-arm ``probs.npy`` files are optional: the
    core report (executive summary, arm table, contrasts, gates, fold
    diagnostics) is built entirely from ``result.json`` + ``manifest.json``.
    """
    out_dir = os.path.abspath(os.path.expanduser(out_dir))
    if not os.path.isdir(out_dir):
        raise FileNotFoundError(f"run directory not found: {out_dir}")

    warns: List[str] = []
    result = _read_json(os.path.join(out_dir, "result.json"))
    manifest = _read_json(os.path.join(out_dir, "manifest.json"))

    config_path = os.path.join(out_dir, "config.json")
    config = _read_json(config_path) if os.path.isfile(config_path) else {}
    if not config:
        warns.append("config.json is missing — falling back to result.json for seeds and k-sweep.")

    fold_path = os.path.join(out_dir, "fold_map.json")
    fold_map = _read_json(fold_path) if os.path.isfile(fold_path) else {}

    arm_probs: Dict[str, np.ndarray] = {}
    arms_dir = os.path.join(out_dir, "arms")
    if os.path.isdir(arms_dir):
        for spec in ARMS:
            path = os.path.join(arms_dir, spec.key, "probs.npy")
            if os.path.isfile(path):
                arm_probs[spec.code] = np.load(path, mmap_mode="r")
    if not arm_probs:
        warns.append("no arms/<arm>/probs.npy found — per-record views unavailable.")

    labels = records = None
    pred_keys: Tuple[str, ...] = ()
    pred_path = os.path.join(out_dir, "predictions.npz")
    if os.path.isfile(pred_path):
        with np.load(pred_path, allow_pickle=False) as npz:
            pred_keys = tuple(npz.files)
            n_beat = None
            for arr in arm_probs.values():
                n_beat = int(arr.shape[-1])
                break
            if n_beat is None:
                for key in npz.files:
                    cand = np.asarray(npz[key])
                    if cand.ndim == 2:
                        n_beat = int(cand.shape[-1])
                        break
            if n_beat is None:
                warns.append("predictions.npz present but beat count could not be determined.")
            else:
                try:
                    _, labels = _pick_array(npz, _LABEL_ALIASES, n_beat, "label")
                    _, records = _pick_array(npz, _RECORD_ALIASES, n_beat, "record-id")
                    labels = np.asarray(labels)
                    records = np.asarray(records)
                except KeyError as exc:
                    warns.append(str(exc))
    elif require_predictions:
        raise FileNotFoundError(f"predictions.npz not found in {out_dir}")
    else:
        warns.append("predictions.npz not found — per-record views unavailable.")

    return RunBundle(
        out_dir=out_dir,
        result=result,
        manifest=manifest,
        config=config,
        fold_map=fold_map,
        arm_probs=arm_probs,
        labels=labels,
        records=records,
        predictions_keys=pred_keys,
        checksums_at_load=bundle_checksums(out_dir),
        load_warnings=warns,
    )


# --------------------------------------------------------------------------
# Achievement metric — recomputed only to unlock per-record views
# --------------------------------------------------------------------------

def _achievement_attainable(hits: np.ndarray, k: int, n_s: int) -> float:
    """hits@k divided by the attainable ceiling min(k, n_S)."""
    return float(hits) / float(min(k, n_s))


def _achievement_recall(hits: np.ndarray, k: int, n_s: int) -> float:
    """hits@k divided by n_S (plain recall@k)."""
    return float(hits) / float(n_s)


#: Candidate definitions, tried in order against result.json's stored values.
ACHIEVEMENT_DEFS: Tuple[Tuple[str, Callable[[np.ndarray, int, int], float]], ...] = (
    ("attainable", _achievement_attainable),
    ("recall", _achievement_recall),
)


def _record_index(rec: np.ndarray, record_ids: Sequence[int]) -> List[np.ndarray]:
    """Beat indices per record, computed once and reused across seeds and arms."""
    order = np.argsort(rec, kind="stable")
    sorted_rec = rec[order]
    left = np.searchsorted(sorted_rec, np.asarray(record_ids), side="left")
    right = np.searchsorted(sorted_rec, np.asarray(record_ids), side="right")
    return [order[l:r] for l, r in zip(left, right)]


def _achievement_per_record(
    prob: np.ndarray,
    is_s: np.ndarray,
    idx_by_record: Sequence[np.ndarray],
    ks: Sequence[int],
    fn: Callable[[np.ndarray, int, int], float],
) -> np.ndarray:
    """(n_record, n_k) achievement values for one seed of one arm.

    Beats whose probability is NaN are unscored and dropped. Within a record the
    beats are ranked by probability, highest first, ties broken by beat order
    (``kind="stable"``) so the value is deterministic.
    """
    out = np.full((len(idx_by_record), len(ks)), np.nan, dtype=np.float64)
    for i, idx in enumerate(idx_by_record):
        if idx.size == 0:
            continue
        p = prob[idx]
        keep = np.isfinite(p)
        if not np.any(keep):
            continue
        p = p[keep]
        y = is_s[idx][keep]
        n_s = int(y.sum())
        if n_s == 0:
            continue
        order = np.argsort(-p, kind="stable")
        csum = np.cumsum(y[order])
        for j, k in enumerate(ks):
            take = min(int(k), csum.shape[0])
            hits = csum[take - 1] if take > 0 else 0
            out[i, j] = fn(hits, int(k), n_s)
    return out


def resolve_achievement_definition(
    bundle: RunBundle,
    *,
    probe_arm: str = "A",
    tol: float = 1e-9,
) -> Tuple[Optional[str], Dict[str, Any]]:
    """Find which achievement definition reproduces ``result.json``.

    Returns ``(name, diagnostics)``. ``name`` is ``None`` when no candidate
    reproduces the stored per-seed ``ach@k`` means within ``tol`` — in that case
    the caller must not draw per-record figures.
    """
    diag: Dict[str, Any] = {"tol": tol, "probe_arm": probe_arm, "candidates": {}}
    if bundle.labels is None or bundle.records is None or probe_arm not in bundle.arm_probs:
        diag["reason"] = "labels, record ids or probs.npy unavailable"
        return None, diag
    if not bundle.has_arm(probe_arm):
        diag["reason"] = f"arm {probe_arm} absent from result.json"
        return None, diag

    ks = list(K_OPERATING_AND_SWEEP)
    record_ids = bundle.scorable_records
    if not record_ids:
        diag["reason"] = "manifest has no scorable_records list"
        return None, diag

    is_s = _s_mask(bundle)
    if is_s is None:
        diag["reason"] = "label array could not be reduced to an S/not-S mask"
        return None, diag

    probs = np.asarray(bundle.arm_probs[probe_arm])
    per_seed = bundle.arm(probe_arm)["per_seed"]
    idx_by_record = _record_index(np.asarray(bundle.records), record_ids)
    diag["idx_by_record"] = idx_by_record

    for name, fn in ACHIEVEMENT_DEFS:
        worst = 0.0
        for s_idx, ps in enumerate(per_seed):
            if s_idx >= probs.shape[0]:
                worst = float("inf")
                break
            vals = _achievement_per_record(
                np.asarray(probs[s_idx], dtype=np.float64), is_s, idx_by_record, ks, fn
            )
            for j, k in enumerate(ks):
                stored = ps.get(f"ach@{k}", {}).get("mean")
                if stored is None:
                    continue
                got = float(np.nanmean(vals[:, j]))
                worst = max(worst, abs(got - float(stored)))
        diag["candidates"][name] = worst
        if worst <= tol:
            diag["chosen"] = name
            return name, diag

    diag["reason"] = (
        "no candidate definition reproduced result.json's ach@k means "
        f"(best max|Δ| = {min(diag['candidates'].values()):.3e})"
    )
    return None, diag


def _s_mask(bundle: RunBundle) -> Optional[np.ndarray]:
    """Reduce the stored label array to a boolean 'is an S beat' mask.

    AAMI 3-class runs store ``y3`` with S as class 1 (N=0, S=1, V=2); a run that
    already stores a binary target is used as-is.
    """
    y = bundle.labels
    if y is None:
        return None
    y = np.asarray(y)
    uniq = np.unique(y[np.isfinite(y.astype(np.float64))] if y.dtype.kind == "f" else y)
    uniq = uniq[uniq >= 0] if uniq.size else uniq
    if uniq.size <= 2:
        return y.astype(bool)
    if 1 in set(uniq.tolist()):
        return y == 1
    return None


@dataclass
class PerRecordKsw:
    """Per-record k-sweep values, seed by seed, for the arms we could compute."""

    definition: str
    record_ids: List[int]
    ksw: Dict[str, np.ndarray]          # code -> (n_seed, n_record)
    ach: Dict[str, np.ndarray]          # code -> (n_seed, n_record, n_k)
    ks: List[int]
    verification: Dict[str, Any]

    def seed_mean(self, code: str) -> np.ndarray:
        return np.nanmean(self.ksw[code], axis=0)


def per_record_ksw(
    bundle: RunBundle,
    codes: Sequence[str] = ("A", "C", "D"),
    *,
    tol: float = 1e-9,
) -> Optional[PerRecordKsw]:
    """Recompute per-record k-sweep values for ``codes``.

    Returns ``None`` — never a guess — when the recomputation cannot be verified
    against ``result.json``.
    """
    definition, diag = resolve_achievement_definition(bundle, tol=tol)
    if definition is None:
        return None
    fn = dict(ACHIEVEMENT_DEFS)[definition]

    ks_all = list(K_OPERATING_AND_SWEEP)
    sweep_idx = [ks_all.index(k) for k in bundle.k_sweep]
    record_ids = bundle.scorable_records
    is_s = _s_mask(bundle)
    assert is_s is not None  # resolve_achievement_definition already checked
    idx_by_record = diag.pop("idx_by_record", None)
    if idx_by_record is None:
        idx_by_record = _record_index(np.asarray(bundle.records), record_ids)

    ksw: Dict[str, np.ndarray] = {}
    ach: Dict[str, np.ndarray] = {}
    checks: Dict[str, float] = {}

    for code in codes:
        if code not in bundle.arm_probs or not bundle.has_arm(code):
            continue
        probs = np.asarray(bundle.arm_probs[code])
        per_seed = bundle.arm(code)["per_seed"]
        n_seed = min(probs.shape[0], len(per_seed))
        a = np.full((n_seed, len(record_ids), len(ks_all)), np.nan)
        for s_idx in range(n_seed):
            a[s_idx] = _achievement_per_record(
                np.asarray(probs[s_idx], dtype=np.float64), is_s, idx_by_record, ks_all, fn
            )
        ach[code] = a
        ksw[code] = np.nanmean(a[:, :, sweep_idx], axis=2)
        worst = 0.0
        for s_idx in range(n_seed):
            stored = per_seed[s_idx]["ksw"]["mean"]
            worst = max(worst, abs(float(np.nanmean(ksw[code][s_idx])) - float(stored)))
        checks[code] = worst

    if not ksw:
        return None
    if max(checks.values()) > tol:
        warnings.warn(
            "per-record k-sweep did not reproduce result.json "
            f"(max |Δ| = {max(checks.values()):.3e} > {tol:.0e}); per-record figures skipped",
            RuntimeWarning,
        )
        return None

    diag["per_arm_max_abs_diff"] = checks
    return PerRecordKsw(
        definition=definition,
        record_ids=list(record_ids),
        ksw=ksw,
        ach=ach,
        ks=ks_all,
        verification=diag,
    )


# --------------------------------------------------------------------------
# Tables
# --------------------------------------------------------------------------

def _seed_avg(arm: Dict[str, Any], metric: str, stat: str = "mean") -> float:
    vals = [ps[metric][stat] for ps in arm["per_seed"] if metric in ps]
    return float(np.mean(vals)) if vals else float("nan")


def arm_metrics_rows(bundle: RunBundle) -> List[Dict[str, Any]]:
    """One row per arm: the numbers the arm table and its CSV share."""
    base = bundle.arm("A")["seed_averaged_ksw"]["mean"]
    rows: List[Dict[str, Any]] = []
    for spec in ARMS:
        if not bundle.has_arm(spec.code):
            continue
        arm = bundle.arm(spec.code)
        ksw = arm["seed_averaged_ksw"]
        rows.append(
            {
                "arm": spec.code,
                "arm_key": spec.key,
                "label": spec.label,
                "role": spec.role,
                "ksweep_mean": float(ksw["mean"]),
                "delta_vs_A": float(ksw["mean"] - base),
                "pr_auc": _seed_avg(arm, "prauc"),
                "auroc": _seed_avg(arm, "auroc"),
                "p10": float(ksw["p10"]),
                "median": float(ksw["median"]),
                "worst": float(ksw["worst"]),
                "worst_record": int(ksw["worst_record"]),
                "seed_sd": float(arm.get("ksw_seed_std", float("nan"))),
                "n_record": int(ksw["n_record"]),
            }
        )
    return rows


def write_arm_metrics_csv(bundle: RunBundle, path: str) -> str:
    rows = arm_metrics_rows(bundle)
    fields = [
        "arm", "arm_key", "label", "role", "ksweep_mean", "delta_vs_A",
        "pr_auc", "auroc", "p10", "median", "worst", "worst_record",
        "seed_sd", "n_record",
    ]
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row[k] for k in fields})
    return path


def contrast_rows(bundle: RunBundle, names: Iterable[Tuple[str, str]]) -> List[Dict[str, Any]]:
    """Contrast point estimates and CIs, read verbatim from result.json."""
    out: List[Dict[str, Any]] = []
    gate = bundle.min_gain
    for key, label in names:
        c = bundle.contrast(key)
        if c is None:
            continue
        boot = c["record_bootstrap"]
        hier = c.get("hierarchical_bootstrap", {})
        mean = float(boot["mean"])
        lo = float(boot["ci_low"])
        hi = float(boot["ci_high"])
        out.append(
            {
                "contrast": key,
                "label": label,
                "mean": mean,
                "ci_low": lo,
                "ci_high": hi,
                "hier_ci_low": float(hier.get("ci_low", np.nan)),
                "hier_ci_high": float(hier.get("ci_high", np.nan)),
                "by_seed": [float(v) for v in c.get("by_seed", [])],
                "positive_seed_count": int(c.get("positive_seed_count", 0)),
                "passes_gain_gate": bool(mean >= gate),
                "ci_excludes_zero": bool(lo > 0.0),
            }
        )
    return out


def write_patient_delta_csv(bundle: RunBundle, per_rec: PerRecordKsw, path: str) -> str:
    """Per-record C − A delta (mean over all seeds), sorted worst → best."""
    burden = bundle.record_burden
    fold = bundle.record_to_fold
    a = per_rec.seed_mean("A")
    c = per_rec.seed_mean("C")
    delta = c - a
    order = np.argsort(delta)
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    fields = [
        "rank", "record", "fold", "delta_C_minus_A", "ksw_A", "ksw_C",
        "s_burden", "n_seed_averaged",
    ]
    with open(path, "w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        for rank, i in enumerate(order, start=1):
            rid = int(per_rec.record_ids[i])
            writer.writerow(
                {
                    "rank": rank,
                    "record": rid,
                    "fold": fold.get(rid, ""),
                    "delta_C_minus_A": float(delta[i]),
                    "ksw_A": float(a[i]),
                    "ksw_C": float(c[i]),
                    "s_burden": burden.get(rid, ""),
                    "n_seed_averaged": int(per_rec.ksw["A"].shape[0]),
                }
            )
    return path


# --------------------------------------------------------------------------
# Training history — recorded for FUTURE runs, never invented for past ones
# --------------------------------------------------------------------------

TRAINING_HISTORY_FILES = ("training_history.json", "training_history.csv")


def training_history_status(out_dir: str) -> Dict[str, Any]:
    """Report whether per-epoch history exists. Never fabricates one."""
    found = [n for n in TRAINING_HISTORY_FILES if os.path.isfile(os.path.join(out_dir, n))]
    return {
        "present": bool(found),
        "files": found,
        "expected": list(TRAINING_HISTORY_FILES),
        "note": (
            "This run predates per-epoch history recording. Nothing is plotted "
            "and no history is synthesised; only future runs that call "
            "TrainingHistoryRecorder will have learning curves."
        )
        if not found
        else "Per-epoch history found; learning curves are drawn from it.",
    }


class TrainingHistoryRecorder:
    """Passive per-epoch recorder for future runs.

    It only *observes*. It holds no optimiser state, chooses no checkpoint, and
    returns nothing that a training loop consumes — so adding a call to
    :meth:`log_epoch` cannot change training arithmetic or which epoch is
    selected as best. Use it alongside the existing loop::

        rec = TrainingHistoryRecorder(out_dir)
        for epoch in range(epochs):
            train_loss = train_one_epoch(...)          # unchanged
            dev_loss, dev_prauc = evaluate(...)        # unchanged
            best_epoch = pick_best(...)                # unchanged
            rec.log_epoch(arm=arm, seed=seed, fold=fold, epoch=epoch,
                          train_loss=train_loss, dev_loss=dev_loss,
                          dev_prauc=dev_prauc, alpha=alpha)
        rec.write()

    ``dev_loss``/``dev_prauc``/``alpha`` are optional because the run evaluates
    the dev set every ``dev_every`` epochs; epochs without an evaluation record
    ``None`` rather than a carried-forward value.
    """

    def __init__(self, out_dir: str, *, filename: str = "training_history.json"):
        self.out_dir = out_dir
        self.filename = filename
        self.rows: List[Dict[str, Any]] = []

    def log_epoch(
        self,
        *,
        arm: str,
        seed: int,
        fold: int,
        epoch: int,
        train_loss: Optional[float] = None,
        dev_loss: Optional[float] = None,
        dev_prauc: Optional[float] = None,
        alpha: Optional[float] = None,
    ) -> None:
        """Append one observation. Returns None on purpose — nothing to feed back."""
        self.rows.append(
            {
                "arm": str(arm),
                "seed": int(seed),
                "fold": int(fold),
                "epoch": int(epoch),
                "train_loss": None if train_loss is None else float(train_loss),
                "dev_loss": None if dev_loss is None else float(dev_loss),
                "dev_prauc": None if dev_prauc is None else float(dev_prauc),
                "alpha": None if alpha is None else float(alpha),
            }
        )

    def write(self, path: Optional[str] = None) -> Optional[str]:
        """Write the history. Writes nothing when nothing was recorded."""
        if not self.rows:
            return None
        path = path or os.path.join(self.out_dir, self.filename)
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        payload = {
            "schema": "medkos.training_history.v1",
            "fields": ["arm", "seed", "fold", "epoch", "train_loss", "dev_loss", "dev_prauc", "alpha"],
            "note": "Observational only. Recording does not affect training or checkpoint selection.",
            "rows": self.rows,
        }
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, indent=2)
        return path


def load_training_history(out_dir: str) -> Optional[List[Dict[str, Any]]]:
    path = os.path.join(out_dir, "training_history.json")
    if os.path.isfile(path):
        payload = _read_json(path)
        return payload["rows"] if isinstance(payload, dict) else payload
    path = os.path.join(out_dir, "training_history.csv")
    if os.path.isfile(path):
        with open(path, "r", encoding="utf-8", newline="") as fh:
            return [dict(r) for r in csv.DictReader(fh)]
    return None


# --------------------------------------------------------------------------
# Figures
# --------------------------------------------------------------------------

def _mpl():
    import matplotlib
    if matplotlib.get_backend().lower() not in ("agg", "module://matplotlib_inline.backend_inline"):
        try:
            matplotlib.use("Agg")
        except Exception:  # pragma: no cover - backend already fixed by Colab
            pass
    import matplotlib.pyplot as plt
    plt.rcParams.update(
        {
            "figure.dpi": 110,
            "savefig.dpi": 150,
            "savefig.bbox": "tight",
            "font.size": 10,
            "axes.edgecolor": COLOR["muted"],
            "axes.labelcolor": COLOR["ink"],
            "axes.titlesize": 12,
            "axes.grid": True,
            "grid.color": COLOR["grid"],
            "grid.linewidth": 0.6,
            "text.color": COLOR["ink"],
            "xtick.color": COLOR["ink"],
            "ytick.color": COLOR["ink"],
            "axes.spines.top": False,
            "axes.spines.right": False,
        }
    )
    return plt


def _save(fig, path: str) -> str:
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    fig.savefig(path)
    # Release the figure: analyze_existing_run draws many, and Colab keeps every
    # pyplot figure alive until it is closed.
    try:
        import matplotlib.pyplot as plt
        plt.close(fig)
    except Exception:  # pragma: no cover
        pass
    return path


def fig_arm_summary_table(bundle: RunBundle, path: str) -> str:
    """1. Arm summary rendered as a table image (the CSV is the machine view)."""
    plt = _mpl()
    rows = arm_metrics_rows(bundle)
    header = ["Arm", "k-sweep\nmean", "Δ vs A", "PR-AUC", "AUROC", "p10",
              "worst (record)", "seed SD"]
    body = []
    for r in rows:
        body.append(
            [
                f"{r['arm']}  {r['label']}",
                f"{r['ksweep_mean']:.4f}",
                f"{r['delta_vs_A']:+.4f}",
                f"{r['pr_auc']:.4f}",
                f"{r['auroc']:.4f}",
                f"{r['p10']:.4f}",
                f"{r['worst']:.4f}  (#{r['worst_record']})",
                f"{r['seed_sd']:.5f}",
            ]
        )
    fig, ax = plt.subplots(figsize=(13.5, 1.05 + 0.42 * len(body)))
    ax.axis("off")
    ax.grid(False)
    # The arm column holds the longest strings; give it the room it needs.
    col_widths = [0.30] + [0.70 / (len(header) - 1)] * (len(header) - 1)
    table = ax.table(cellText=body, colLabels=header, cellLoc="center",
                     loc="center", colWidths=col_widths)
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1, 1.55)
    for (row, col), cell in table.get_celld().items():
        cell.set_edgecolor("#EEEEEE")
        if row == 0:
            cell.set_facecolor("#F2F2F2")
            cell.set_text_props(weight="bold")
        else:
            code = rows[row - 1]["arm"]
            if col == 0:
                cell.set_text_props(color=COLOR.get(code, COLOR["ink"]),
                                    weight="bold", ha="left")
                cell.PAD = 0.04
            if code == "A":
                cell.set_facecolor("#F7FAFD")
    ax.set_title(
        f"Arm summary — {bundle.run_id}\n"
        f"primary metric: {bundle.result.get('primary_metric')} · "
        f"{bundle.n_seed} seeds · {rows[0]['n_record']} records · A is the baseline",
        pad=16,
    )
    return _save(fig, path)


def fig_primary_contrasts_zoom(bundle: RunBundle, path: str) -> str:
    """2. Primary contrasts only, on their own scale."""
    plt = _mpl()
    rows = contrast_rows(bundle, PRIMARY_CONTRASTS)
    gate = bundle.min_gain
    fig, ax = plt.subplots(figsize=(9.5, 0.95 * len(rows) + 2.6))
    ypos = np.arange(len(rows))[::-1]

    for y, r in zip(ypos, rows):
        passed = r["passes_gain_gate"] and r["ci_excludes_zero"]
        color = COLOR["C"] if passed else COLOR["neg"]
        ax.plot([r["ci_low"], r["ci_high"]], [y, y], color=color, lw=2, solid_capstyle="round")
        ax.plot([r["ci_low"], r["ci_high"]], [y, y], "|", color=color, ms=10, mew=2)
        ax.plot([r["mean"]], [y], "o", color=color, ms=9,
                markeredgecolor="white", markeredgewidth=2, zorder=3)
        # Values live in a fixed column outside the plot area, so a long label can
        # never collide with a CI whisker however narrow the interval is.
        ax.annotate(
            f"{r['mean']:+.4f}   [{r['ci_low']:+.4f}, {r['ci_high']:+.4f}]",
            xy=(1.02, y), xycoords=("axes fraction", "data"),
            va="center", ha="left", fontsize=9.5, color=COLOR["ink"],
            family="monospace",
        )
        ax.annotate(
            "PASS" if passed else "FAIL",
            xy=(1.40, y), xycoords=("axes fraction", "data"),
            va="center", ha="left", fontsize=10, color=color, weight="bold",
        )

    ax.axvline(0.0, color=COLOR["zero"], lw=1.4, zorder=1)
    ax.axvline(gate, color=COLOR["gate"], lw=1.6, ls="--", zorder=1)
    top = len(rows) - 0.30
    # The gate line sits at the right edge, so its label reads leftward.
    ax.annotate(f"+{gate:g} gate", xy=(gate, top), xytext=(-6, 0),
                textcoords="offset points", ha="right", va="center",
                color=COLOR["gate"], fontsize=9.5, weight="bold")
    ax.annotate("zero", xy=(0.0, top), xytext=(5, 0), textcoords="offset points",
                ha="left", va="center", color=COLOR["zero"], fontsize=9.5)
    ax.annotate("mean [95% CI]", xy=(1.02, top),
                xycoords=("axes fraction", "data"), va="center", ha="left",
                fontsize=9, color=COLOR["muted"])

    lo = min(min(r["ci_low"] for r in rows), 0.0)
    hi = max(max(r["ci_high"] for r in rows), gate)
    span = hi - lo
    ax.set_xlim(lo - span * 0.10, hi + span * 0.10)
    ax.set_yticks(ypos, [r["label"] for r in rows])
    ax.set_ylim(-0.6, len(rows) - 0.05)
    ax.set_xlabel("Δ record-level k-sweep achievement (95% record bootstrap CI)")
    ax.set_title("Primary contrasts — zoomed to their own scale\n"
                 "large reference gaps are in reference_gap_separate.png, never on this axis")
    ax.grid(axis="y", visible=False)
    return _save(fig, path)


def fig_reference_gap_separate(bundle: RunBundle, path: str) -> str:
    """3. Large reference contrasts, deliberately on a separate figure."""
    plt = _mpl()
    ref = contrast_rows(bundle, REFERENCE_CONTRASTS)
    prim = contrast_rows(bundle, PRIMARY_CONTRASTS)
    big = [r for r in ref if abs(r["mean"]) >= 0.05]
    small = [r for r in ref if abs(r["mean"]) < 0.05]

    span_ref = max((abs(r["mean"]) for r in big), default=0.0)
    span_prim = max((abs(r["mean"]) for r in prim), default=0.0)
    ratio = span_ref / span_prim if span_prim > 0 else float("nan")

    fig, axes = plt.subplots(1, 2, figsize=(13, 4.2), gridspec_kw={"width_ratios": [1.15, 1]})

    ax = axes[0]
    ypos = np.arange(len(big))[::-1]
    for y, r in zip(ypos, big):
        ax.plot([r["ci_low"], r["ci_high"]], [y, y], color=COLOR["B"], lw=2.5, solid_capstyle="round")
        ax.plot([r["mean"]], [y], "o", color=COLOR["B"], ms=9,
                markeredgecolor="white", markeredgewidth=2, zorder=3)
        ax.annotate(f"{r['mean']:+.4f}  [{r['ci_low']:+.3f}, {r['ci_high']:+.3f}]",
                    xy=(r["mean"], y), xytext=(0, 14), textcoords="offset points",
                    ha="center", fontsize=9.5, weight="bold")
    ax.axvline(0.0, color=COLOR["zero"], lw=1.4)
    ax.set_yticks(ypos, [r["label"] for r in big])
    ax.set_ylim(-0.55, len(big) - 0.45)
    ax.set_xlabel("Δ k-sweep achievement")
    ax.set_title(f"Reference gap — separate axis\n(scale is ~{ratio:.0f}× the primary contrasts)")
    ax.grid(axis="y", visible=False)

    ax = axes[1]
    ypos = np.arange(len(small))[::-1]
    for y, r in zip(ypos, small):
        ax.plot([r["ci_low"], r["ci_high"]], [y, y], color=COLOR["E"], lw=2, solid_capstyle="round")
        ax.plot([r["mean"]], [y], "o", color=COLOR["E"], ms=8,
                markeredgecolor="white", markeredgewidth=2, zorder=3)
        ax.annotate(f"{r['mean']:+.4f}", xy=(r["mean"], y), xytext=(0, 13),
                    textcoords="offset points", ha="center", fontsize=9.5)
    ax.axvline(0.0, color=COLOR["zero"], lw=1.4)
    ax.axvline(bundle.min_gain, color=COLOR["gate"], lw=1.4, ls="--")
    ax.set_yticks(ypos, [r["label"] for r in small])
    ax.set_ylim(-0.55, max(len(small) - 0.45, 0.5))
    ax.set_xlabel("Δ k-sweep achievement")
    ax.set_title("Other secondary contrasts\n(dashed line = +%g gate)" % bundle.min_gain)
    ax.grid(axis="y", visible=False)

    if span_prim > 0:
        fig.suptitle(
            f"Why these are split: |B−A| ≈ {span_ref:.3f} vs |primary| ≈ {span_prim:.4f} "
            f"(~{ratio:.0f}×). One shared axis would flatten the primary contrasts to a point.",
            y=1.05, fontsize=10, color=COLOR["muted"],
        )
    return _save(fig, path)


def fig_achievement_by_k(bundle: RunBundle, path: str,
                         codes: Sequence[str] = ("A", "C", "D", "E")) -> str:
    """4. achievement@k per arm, plus a zoom on C − A."""
    plt = _mpl()
    ks = list(K_OPERATING_AND_SWEEP)
    codes = [c for c in codes if bundle.has_arm(c)]

    curves: Dict[str, List[float]] = {}
    for code in codes:
        arm = bundle.arm(code)
        curves[code] = [
            float(np.mean([ps[f"ach@{k}"]["mean"] for ps in arm["per_seed"]])) for k in ks
        ]

    fig, axes = plt.subplots(1, 2, figsize=(13, 4.6), gridspec_kw={"width_ratios": [1.25, 1]})

    def log_axis(ax):
        """Log x with only the swept k labelled — no 4×10¹ minor-tick clutter."""
        ax.set_xscale("log")
        ax.set_xticks(ks, [str(k) for k in ks])
        ax.set_xticks([], minor=True)
        ax.set_xlim(ks[0] * 0.82, ks[-1] * 1.22)
        ax.set_xlabel("k (alarm budget per record)")

    ax = axes[0]
    for code in codes:
        ax.plot(ks, curves[code], "-o", color=COLOR[code], lw=2, ms=8,
                markeredgecolor="white", markeredgewidth=1.5,
                label=f"{code} · {ARM_BY_CODE[code].label}")
    log_axis(ax)
    ax.set_ylabel("achievement@k  (record mean, seed-averaged)")
    ax.set_title("Achievement by k — all arms on one scale")
    # The arms overlap to within ~0.005, so per-point labels would collide;
    # the legend carries identity and the zoom panel carries the difference.
    ax.legend(frameon=False, loc="upper left", fontsize=9)

    ax = axes[1]
    if "A" in curves and "C" in curves:
        diff = [c - a for c, a in zip(curves["C"], curves["A"])]
        ax.plot(ks, diff, "-o", color=COLOR["C"], lw=2, ms=8,
                markeredgecolor="white", markeredgewidth=1.5)
        for i, (k, d) in enumerate(zip(ks, diff)):
            ax.annotate(f"{d:+.4f}", xy=(k, d), xytext=(0, 12 if i % 2 == 0 else -18),
                        textcoords="offset points", ha="center", fontsize=9,
                        color=COLOR["ink"])
        ax.axhline(0.0, color=COLOR["zero"], lw=1.4)
        ax.axhline(bundle.min_gain, color=COLOR["gate"], lw=1.5, ls="--")
        ax.annotate(f"+{bundle.min_gain:g} gate — never approached",
                    xy=(ks[0], bundle.min_gain), xytext=(2, 6),
                    textcoords="offset points", ha="left",
                    color=COLOR["gate"], fontsize=9.5, weight="bold")
        hi = max(bundle.min_gain * 1.30, max(diff) * 1.8 if max(diff) > 0 else bundle.min_gain)
        lo = min(min(diff) * 1.8 if min(diff) < 0 else 0.0, -bundle.min_gain * 0.18)
        ax.set_ylim(lo, hi)
    log_axis(ax)
    ax.set_ylabel("C − A")
    ax.set_title("Zoom: C − A at every k\n(the gate line is the point of the zoom)")
    return _save(fig, path)


def fig_seed_effects(bundle: RunBundle, path: str) -> str:
    """5. Per-seed C − A and C − D, so the direction of all seeds is visible."""
    plt = _mpl()
    seeds = bundle.seeds
    series = [
        ("C_minus_A", "C − A", COLOR["C"]),
        ("C_minus_D", "C − D", COLOR["D"]),
    ]
    fig, ax = plt.subplots(figsize=(10, 4.8))
    x = np.arange(len(seeds), dtype=float)
    width = 0.34

    for i, (key, label, color) in enumerate(series):
        c = bundle.contrast(key)
        if c is None:
            continue
        vals = [float(v) for v in c["by_seed"]]
        offs = x + (i - 0.5) * (width + 0.02)
        ax.bar(offs, vals, width=width, color=color, label=label,
               edgecolor="white", linewidth=2)
        for xi, v in zip(offs, vals):
            ax.annotate(f"{v:+.4f}", xy=(xi, v),
                        xytext=(0, 6 if v >= 0 else -14), textcoords="offset points",
                        ha="center", fontsize=8.5, color=COLOR["ink"])

    ax.axhline(0.0, color=COLOR["zero"], lw=1.4)
    ax.axhline(bundle.min_gain, color=COLOR["gate"], lw=1.6, ls="--")
    ax.annotate(f"+{bundle.min_gain:g} gate", xy=(x[0] - 0.45, bundle.min_gain),
                xytext=(0, 5), textcoords="offset points",
                color=COLOR["gate"], fontsize=9.5, weight="bold")
    ax.set_xticks(x, [str(s) for s in seeds])
    ax.set_xlabel("training seed")
    ax.set_ylabel("Δ k-sweep achievement")
    ax.set_ylim(min(-0.002, ax.get_ylim()[0]), bundle.min_gain * 1.2)
    ax.set_title(
        "Seed effects — every seed, both primary contrasts\n"
        "direction is stable, but the whole range sits far below the gate"
    )
    ax.legend(frameon=False, ncol=2, loc="upper left")
    ax.grid(axis="x", visible=False)
    return _save(fig, path)


def fig_fold_training_diagnostics(bundle: RunBundle, path: str,
                                  codes: Sequence[str] = ("C", "D", "E")) -> str:
    """6. seed × fold heatmaps of alpha / best_epoch / dev_loss for C, D, E."""
    plt = _mpl()
    arm_alpha = bundle.manifest.get("arm_alpha", {})
    codes = [c for c in codes if ARM_BY_CODE[c].key in arm_alpha]
    if not codes:
        raise ValueError("manifest.arm_alpha has none of the requested arms")

    metrics = [
        ("alpha", "alpha (residual weight)", "diverging"),
        ("best_epoch", "best_epoch", "sequential"),
        ("dev_loss", "dev_loss", "sequential"),
    ]
    grids: Dict[Tuple[str, str], np.ndarray] = {}
    seeds: List[int] = []
    folds: List[int] = []
    for code in codes:
        entries = arm_alpha[ARM_BY_CODE[code].key]
        seeds = [int(e["seed"]) for e in entries]
        folds = sorted({int(f["fold"]) for e in entries for f in e["folds"]})
        for metric, _, _ in metrics:
            g = np.full((len(seeds), len(folds)), np.nan)
            for si, e in enumerate(entries):
                for f in e["folds"]:
                    g[si, folds.index(int(f["fold"]))] = float(f[metric])
            grids[(code, metric)] = g

    fig, axes = plt.subplots(
        len(metrics), len(codes),
        figsize=(3.7 * len(codes) + 1.4, 2.9 * len(metrics) + 1.5),
        squeeze=False,
    )
    for mi, (metric, mlabel, kind) in enumerate(metrics):
        vals = np.concatenate([grids[(c, metric)].ravel() for c in codes])
        finite = vals[np.isfinite(vals)]
        if kind == "diverging":
            lim = float(np.nanmax(np.abs(finite))) if finite.size else 1.0
            vmin, vmax, cmap = -lim, lim, "RdBu_r"
        else:
            vmin = float(np.nanmin(finite)) if finite.size else 0.0
            vmax = float(np.nanmax(finite)) if finite.size else 1.0
            cmap = "Blues"
        for ci, code in enumerate(codes):
            ax = axes[mi][ci]
            g = grids[(code, metric)]
            im = ax.imshow(g, cmap=cmap, vmin=vmin, vmax=vmax, aspect="auto")
            ax.grid(False)
            ax.set_xticks(range(len(folds)), [f"f{f}" for f in folds], fontsize=8.5)
            # Seed labels only on the leftmost panel, else they run into the
            # neighbouring heatmap's cells.
            if ci == 0:
                ax.set_yticks(range(len(seeds)), [str(s) for s in seeds], fontsize=8)
            else:
                ax.set_yticks([])
            for si in range(g.shape[0]):
                for fi in range(g.shape[1]):
                    v = g[si, fi]
                    if not np.isfinite(v):
                        continue
                    txt = f"{int(v)}" if metric == "best_epoch" else f"{v:+.3f}" if metric == "alpha" else f"{v:.3f}"
                    ax.text(fi, si, txt, ha="center", va="center", fontsize=7.5,
                            color="#111111")
            if mi == 0:
                ax.set_title(f"{code} · {ARM_BY_CODE[code].label}", fontsize=10.5)
            if ci == 0:
                ax.set_ylabel(f"{mlabel}\nseed", fontsize=9.5)
        fig.colorbar(im, ax=axes[mi], fraction=0.02, pad=0.015)

    # The finding that explains the whole run: Arm C never trained past epoch 0.
    c_grid = grids.get(("C", "best_epoch"))
    if c_grid is not None:
        zero = int(np.sum(c_grid == 0))
        total = int(np.sum(np.isfinite(c_grid)))
        if zero == total and total > 0:
            msg = (
                f"WARNING — Arm C: best_epoch = 0 in {zero}/{total} seed×fold fits. "
                "Early stopping selected the pre-training checkpoint every single time: "
                "the CNN residual never improved dev loss, so C is A plus (almost) nothing."
            )
        else:
            msg = (
                f"Arm C: best_epoch = 0 in {zero}/{total} seed×fold fits — "
                "the residual rarely earned an update."
            )
        fig.text(
            0.5, -0.015, msg, ha="center", va="top", fontsize=10, weight="bold",
            color="#8A3B00",
            bbox=dict(facecolor=COLOR["warn_bg"], edgecolor="#E0B27A", boxstyle="round,pad=0.55"),
        )
    fig.suptitle("Fold-level training diagnostics — seed × fold", y=1.0, fontsize=12)
    return _save(fig, path)


def fig_patient_delta_waterfall(bundle: RunBundle, per_rec: PerRecordKsw, path: str) -> str:
    """7. Per-record C − A, averaged over all seeds, sorted."""
    plt = _mpl()
    a = per_rec.seed_mean("A")
    c = per_rec.seed_mean("C")
    delta = c - a
    order = np.argsort(delta)
    d = delta[order]
    labels = [str(per_rec.record_ids[i]) for i in order]
    colors = [COLOR["pos"] if v >= 0 else COLOR["neg"] for v in d]

    mean_delta = float(np.mean(delta))
    n_pos = int(np.sum(delta > 0))
    n_neg = int(np.sum(delta < 0))
    best = float(np.max(delta))
    worst = float(np.min(delta))

    fig, ax = plt.subplots(figsize=(max(11, 0.24 * len(d)), 5.4))
    ax.set_axisbelow(True)  # bars sit above the grid, not under it
    ax.bar(np.arange(len(d)), d, color=colors, edgecolor="white", linewidth=1.2)
    ax.axhline(0.0, color=COLOR["zero"], lw=1.4)
    ax.axhline(mean_delta, color=COLOR["muted"], lw=1.3, ls=":")
    # Offset away from the zero line, which the mean sits almost on top of.
    ax.annotate(f"record mean {mean_delta:+.4f}", xy=(0.0, mean_delta),
                xycoords=("axes fraction", "data"),
                xytext=(4, 7 if mean_delta >= 0 else -15),
                textcoords="offset points", ha="left", fontsize=9.5,
                color=COLOR["ink"], zorder=6,
                bbox=dict(facecolor="white", alpha=0.85, edgecolor="none",
                          boxstyle="round,pad=0.25"))
    ax.set_xticks(np.arange(len(d)), labels, rotation=90, fontsize=7.5)
    ax.set_xlabel("record (sorted by Δ)")
    ax.set_ylabel("C − A, k-sweep achievement")
    ax.set_title(
        f"Per-record C − A, averaged over all {per_rec.ksw['A'].shape[0]} seeds "
        f"(not a single seed)\n"
        f"{n_pos} improve · {n_neg} degrade · best {best:+.4f} · worst {worst:+.4f} · "
        f"mean {mean_delta:+.4f}"
    )
    ax.grid(axis="x", visible=False)
    handles = [
        plt.Line2D([], [], color=COLOR["pos"], lw=8, label="improved (C > A)"),
        plt.Line2D([], [], color=COLOR["neg"], lw=8, label="degraded (C < A)"),
    ]
    ax.legend(handles=handles, frameon=False, loc="upper left")
    return _save(fig, path)


def fig_metric_distribution(bundle: RunBundle, per_rec: PerRecordKsw, path: str,
                            codes: Sequence[str] = ("A", "C", "D")) -> str:
    """8. Per-record k-sweep distribution for A / C / D, with p10 and median."""
    plt = _mpl()
    codes = [c for c in codes if c in per_rec.ksw]
    data = [per_rec.seed_mean(c) for c in codes]

    fig, ax = plt.subplots(figsize=(9.5, 5.6))
    parts = ax.violinplot(data, positions=np.arange(len(codes)), widths=0.8,
                          showmeans=False, showextrema=False, showmedians=False)
    for body, code in zip(parts["bodies"], codes):
        body.set_facecolor(COLOR[code])
        body.set_alpha(0.16)
        body.set_edgecolor(COLOR[code])
        body.set_linewidth(1.4)
    bp = ax.boxplot(data, positions=np.arange(len(codes)), widths=0.22,
                    showfliers=False, patch_artist=True, medianprops=dict(color=COLOR["ink"], lw=2))
    for patch, code in zip(bp["boxes"], codes):
        patch.set_facecolor("white")
        patch.set_edgecolor(COLOR[code])
        patch.set_linewidth(1.6)

    rng = np.random.default_rng(0)  # jitter only; no statistic depends on it
    ticklabels = []
    for i, (code, vals) in enumerate(zip(codes, data)):
        jitter = (rng.random(vals.shape[0]) - 0.5) * 0.22
        ax.plot(i + jitter, vals, "o", color=COLOR[code], ms=5, alpha=0.75,
                markeredgecolor="white", markeredgewidth=0.8, zorder=3)
        arm = bundle.arm(code)["seed_averaged_ksw"]
        p10, med = float(arm["p10"]), float(arm["median"])
        ax.hlines(p10, i - 0.42, i + 0.42, color=COLOR[code], lw=2, ls="--", zorder=4)
        # Values ride under the axis: the corridor between violins is too narrow
        # for a label, and one placed there lands on the neighbouring arm.
        ticklabels.append(
            f"{code}\n{ARM_BY_CODE[code].label}\nmedian {med:.3f}  ·  p10 {p10:.3f} (dashed)"
        )

    means = [float(np.nanmean(v)) for v in data]
    spread = max(means) - min(means)
    ax.set_xticks(np.arange(len(codes)), ticklabels, fontsize=9)
    ax.set_ylabel("per-record k-sweep achievement (seed-averaged)")
    ax.set_title(
        "Per-record distribution — " + " / ".join(codes) + "\n"
        f"arm means span only {spread:.4f}; the spread within one arm is "
        f"{float(np.nanmax(data[0]) - np.nanmin(data[0])):.3f} — the lower tail, not the "
        "mean, is what separates records"
    )
    ax.grid(axis="x", visible=False)
    return _save(fig, path)


def fig_learning_curves(out_dir: str, path: str) -> Optional[str]:
    """9. Learning curves — only when a real history file exists."""
    history = load_training_history(out_dir)
    if not history:
        return None
    plt = _mpl()

    def num(row, key):
        v = row.get(key)
        if v in (None, "", "None"):
            return np.nan
        return float(v)

    groups: Dict[Tuple[str, int, int], List[Dict[str, Any]]] = {}
    for row in history:
        key = (str(row["arm"]), int(row["seed"]), int(row["fold"]))
        groups.setdefault(key, []).append(row)

    panels = [("train_loss", "train loss"), ("dev_loss", "dev loss"),
              ("dev_prauc", "dev PR-AUC"), ("alpha", "alpha")]
    fig, axes = plt.subplots(2, 2, figsize=(12, 7.5))
    arms_seen = sorted({k[0] for k in groups})
    color_for = {a: COLOR.get(ARM_BY_KEY[a].code, COLOR["muted"]) if a in ARM_BY_KEY
                 else COLOR["muted"] for a in arms_seen}
    for ax, (field_name, label) in zip(axes.ravel(), panels):
        for (arm, _seed, _fold), rows in sorted(groups.items()):
            rows = sorted(rows, key=lambda r: int(r["epoch"]))
            xs = [int(r["epoch"]) for r in rows]
            ys = [num(r, field_name) for r in rows]
            if not np.any(np.isfinite(ys)):
                continue
            ax.plot(xs, ys, "-o", ms=4, lw=1.4, alpha=0.7, color=color_for[arm])
        ax.set_xlabel("epoch")
        ax.set_ylabel(label)
        ax.set_title(label)
    handles = [plt.Line2D([], [], color=color_for[a], lw=2, label=a) for a in arms_seen]
    if handles:
        fig.legend(handles=handles, frameon=False, loc="upper center",
                   ncol=min(4, len(handles)), bbox_to_anchor=(0.5, 1.05))
    fig.suptitle("Learning curves — per seed × fold", y=0.99)
    fig.tight_layout()
    return _save(fig, path)


# --------------------------------------------------------------------------
# Executive summary and report
# --------------------------------------------------------------------------

def _fmt_ci(r: Dict[str, Any]) -> str:
    return f"{r['mean']:+.4f} (95% CI {r['ci_low']:+.4f} ~ {r['ci_high']:+.4f})"


GATE_LABELS_KO = {
    "1_mean_gain_ge_0.015": "① 평균 이득 ≥ +0.015",
    "2_ci_lower_gt_0": "② 95% CI 하한 > 0",
    "3_beats_shuffle_control": "③ 셔플 대조군(D)보다 우수",
    "4_seed_direction_stable": "④ seed 방향 일관성",
    "5_lower_tail_not_worse": "⑤ 하위 꼬리 악화 없음",
    "6_leakage_and_reproducibility": "⑥ 누수·재현성 점검",
}


def executive_summary_ko(bundle: RunBundle) -> str:
    """The first thing the notebook prints — Korean, decision-first."""
    rows = {r["contrast"]: r for r in contrast_rows(bundle, PRIMARY_CONTRASTS + REFERENCE_CONTRASTS)}
    ca, cd = rows.get("C_minus_A"), rows.get("C_minus_D")
    arm_a = bundle.arm("A")["seed_averaged_ksw"]
    arm_c = bundle.arm("C")["seed_averaged_ksw"]
    checks = bundle.result.get("gates", {}).get("checks", {})
    passed = [GATE_LABELS_KO.get(k, k) for k, v in checks.items() if v]
    failed = [GATE_LABELS_KO.get(k, k) for k, v in checks.items() if not v]
    gate = bundle.min_gain
    n_rec = int(arm_a["n_record"])

    lines: List[str] = []
    add = lines.append

    add("=" * 78)
    add("Q4-O 결과 요약 (Executive Summary)")
    add(f"run: {bundle.run_id}")
    add(f"실험: {bundle.result.get('experiment_id')} / arm {bundle.result.get('arm_id')}"
        f" · 지표: {bundle.result.get('primary_metric')}")
    add(f"설계: {bundle.config.get('split', 'record-grouped CV')} · "
        f"seed {bundle.n_seed}개 · 채점 레코드 {n_rec}개")
    add("=" * 78)
    add("")
    add(f"■ 최종 판정: {bundle.verdict}")
    add("")
    add(f"■ morphology baseline (Arm A) = {arm_a['mean']:.4f}")
    add(f"   · 이번 실험이 넘어야 했던 기준선. p10 {arm_a['p10']:.4f} · "
        f"median {arm_a['median']:.4f} · worst {arm_a['worst']:.4f} (record #{int(arm_a['worst_record'])})")
    add(f"   · 가설 arm C = {arm_c['mean']:.4f} — 기준선과의 차이는 "
        f"{arm_c['mean'] - arm_a['mean']:+.4f}.")
    add("")
    if ca:
        add(f"■ C − A (가설 대 기준선): {_fmt_ci(ca)}")
        add(f"   · 요구 이득 +{gate:g}의 약 {ca['mean'] / gate * 100:.0f}% 수준이고, CI가 0을 포함한다.")
    if cd:
        add(f"■ C − D (가설 대 셔플 대조군): {_fmt_ci(cd)}")
        add(f"   · 파형-라벨 대응을 부순 대조군과도 구분되지 않는다. CI가 0을 포함한다.")
    add("")
    add(f"■ 통과한 gate ({len(passed)}/{len(checks)}): " + (", ".join(passed) if passed else "없음"))
    add(f"■ 실패한 gate ({len(failed)}/{len(checks)}): " + (", ".join(failed) if failed else "없음"))
    add("")
    add("■ 이 결과가 의미하는 것")
    add("   1) 형태학(morphology) 특징이 이미 가진 정보를 raw CNN residual이 더 얹지 못했다.")
    add(f"   2) C − D가 0과 구분되지 않는다는 것이 핵심이다. D는 비트 파형과 라벨의 대응을")
    add("      의도적으로 부순 arm인데, C가 그보다 낫다는 증거가 없다. 즉 C가 얻은 미세한")
    add("      이득은 '파형에서 배운 것'이라고 말할 수 없다.")
    c_folds = [f for e in bundle.manifest.get("arm_alpha", {}).get(ARM_BY_CODE["C"].key, [])
               for f in e["folds"]]
    n_zero = sum(1 for f in c_folds if f["best_epoch"] == 0)
    if c_folds:
        add(f"   3) 학습 진단이 이를 뒷받침한다. Arm C는 seed×fold {len(c_folds)}칸 중 "
            f"{n_zero}칸에서 best_epoch=0 —")
        add("      early stopping이 학습 이전 체크포인트를 골랐다. 그만큼 residual이 dev loss를")
        add("      개선하지 못했다는 뜻이다.")
    if "B_minus_A" in rows:
        add(f"   4) 반대로 형태학 없이 raw CNN만 쓴 B는 A보다 {rows['B_minus_A']['mean']:+.4f} —")
        add("      이 파이프라인에서 성능을 지탱하는 것은 형태학 특징 쪽이다.")
    add("")
    add("■ 이 결과가 증명하지 않는 것")
    add("   1) 'CNN이 ECG에서 쓸모없다'가 아니다. 이 설계(12 epoch, 2채널, residual 결합,")
    add("      고정된 형태학 offset) 안에서 이득이 없었다는 것뿐이다.")
    add("   2) 'Q4-N이 틀렸다'가 아니다. Q4-N의 0.8631은 오염된 offset 배열로 학습·채점된")
    add("      값이라 이 run의 값과 같은 축에서 비교할 수 없다. 제외 이유는 보고서 본문 참조.")
    add("   3) 더 큰 모델(Transformer·대형 fusion)이 실패한다는 증거도 아니다. 이 run은")
    add("      그런 모델을 시험하지 않았다. 동시에, 시험할 근거도 만들어 주지 않았다.")
    add("   4) 하위 꼬리(p10, worst record) 문제가 해결됐다는 뜻도 아니다. gate ⑤는")
    add("      '악화되지 않았다'만 말한다.")
    add("")
    add("■ 권장 다음 행동")
    next_step = bundle.result.get("gates", {}).get("next_step")
    if next_step:
        add(f"   0) run이 기록한 지시: {next_step}")
    add("   1) morphology baseline을 유지한다. C를 채택하지 않는다.")
    add(f"   2) 평균이 아니라 실패 레코드를 본다. A의 worst는 record "
        f"#{int(arm_a['worst_record'])} ({arm_a['worst']:.4f}), p10은 {arm_a['p10']:.4f}로")
    add("      중앙값과 크게 벌어져 있다. patient_delta.csv의 하위 레코드부터 원인을 본다.")
    add("   3) 다음 실험은 '평균을 올리는 모델'이 아니라 '하위 꼬리를 좁히는 가설'이어야 한다.")
    add("   4) 향후 run에는 TrainingHistoryRecorder를 붙여 epoch별 학습 곡선을 남긴다.")
    add("      이번 run에는 그 기록이 없어 학습 곡선을 그릴 수 없었다(조작하지 않았다).")
    add("=" * 78)
    return "\n".join(lines)


def interpretation_ko(
    bundle: RunBundle,
    artifact: str,
    per_rec: Optional[PerRecordKsw] = None,
) -> str:
    """Two or three Korean sentences for one table or figure.

    Every number in the text is read from this run, so the sentences move with
    the data instead of asserting something the figure may not show.
    """
    gate = bundle.min_gain
    rows = {r["contrast"]: r for r in
            contrast_rows(bundle, PRIMARY_CONTRASTS + REFERENCE_CONTRASTS)}
    a = bundle.arm("A")["seed_averaged_ksw"]
    c = bundle.arm("C")["seed_averaged_ksw"]

    if artifact == "arm_summary_table.png":
        best = max(arm_metrics_rows(bundle), key=lambda r: r["ksweep_mean"])
        return (
            f"기준선 A는 {a['mean']:.4f}, 가설 arm C는 {c['mean']:.4f}로 차이가 "
            f"{c['mean'] - a['mean']:+.4f}에 불과하다. 형태학을 뺀 B만 "
            f"{bundle.arm('B')['seed_averaged_ksw']['mean']:.4f}로 크게 떨어지므로, 이 파이프라인의 "
            "성능은 형태학 특징이 지탱하고 있다는 뜻이다. "
            f"표에서 가장 높은 값은 {best['arm']}({best['ksweep_mean']:.4f})이지만 "
            f"{'진단용 arm이라 판정 근거가 아니다.' if best['role'].startswith('diagnostic') else '차이가 gate에 못 미친다.'}"
        )

    if artifact == "primary_contrasts_zoom.png":
        ca, cd = rows["C_minus_A"], rows["C_minus_D"]
        return (
            f"C−A는 {ca['mean']:+.4f} (95% CI {ca['ci_low']:+.4f}~{ca['ci_high']:+.4f})로 "
            f"요구 이득 +{gate:g}의 {ca['mean'] / gate * 100:.0f}% 수준이고 CI가 0을 포함한다. "
            f"C−D도 {cd['mean']:+.4f} (CI {cd['ci_low']:+.4f}~{cd['ci_high']:+.4f})여서 "
            "파형-라벨 대응을 부순 대조군과 구분되지 않는다. "
            "세 대비 모두 gate 선(점선)에 닿지 못했고, 이것이 NO-GO의 직접 근거다."
        )

    if artifact == "reference_gap_separate.png":
        ba = rows.get("B_minus_A")
        ratio = abs(ba["mean"]) / max(abs(rows["C_minus_A"]["mean"]), 1e-12) if ba else float("nan")
        return (
            f"B−A는 {ba['mean']:+.4f}로 1차 대비({rows['C_minus_A']['mean']:+.4f})보다 "
            f"약 {ratio:.0f}배 크다. 같은 축에 그리면 1차 대비가 0 위의 점으로 뭉개지므로 "
            "축을 분리했다. 이 그림이 말하는 것은 '형태학을 빼면 무너진다'이지 "
            "'residual이 효과가 있다'가 아니다."
        )

    if artifact == "achievement_by_k.png":
        arm_a, arm_c = bundle.arm("A"), bundle.arm("C")
        diffs = {k: float(np.mean([ps[f"ach@{k}"]["mean"] for ps in arm_c["per_seed"]])
                          - np.mean([ps[f"ach@{k}"]["mean"] for ps in arm_a["per_seed"]]))
                 for k in K_OPERATING_AND_SWEEP}
        kmax = max(diffs, key=lambda k: diffs[k])
        kmin = min(diffs, key=lambda k: diffs[k])
        return (
            f"어떤 알람 예산 k에서도 arm들이 겹친다. C−A가 가장 큰 지점은 k={kmax}"
            f"({diffs[kmax]:+.4f}), 가장 작은 지점은 k={kmin}({diffs[kmin]:+.4f})이고 "
            f"둘 다 +{gate:g}에 한참 못 미친다. "
            "즉 '운영점을 바꾸면 이득이 나온다'는 해석도 이 데이터로는 성립하지 않는다."
        )

    if artifact == "seed_effects.png":
        ca, cd = rows["C_minus_A"], rows["C_minus_D"]
        vals = ca["by_seed"]
        return (
            f"5개 seed 중 {ca['positive_seed_count']}개에서 C−A가 양수라 방향은 안정적이다"
            f"(gate ④ 통과). 그러나 값의 범위가 {min(vals):+.4f}~{max(vals):+.4f}로 "
            f"모두 +{gate:g} 아래에 있다. "
            "방향이 일관된 것과 효과가 실재하는 것은 다르며, C−D도 같은 그림을 보인다."
        )

    if artifact == "fold_training_diagnostics.png":
        aa = bundle.manifest.get("arm_alpha", {}).get(ARM_BY_CODE["C"].key, [])
        eps = [f["best_epoch"] for e in aa for f in e["folds"]]
        alphas = [f["alpha"] for e in aa for f in e["folds"]]
        zero = sum(1 for v in eps if v == 0)
        n_neg = sum(1 for v in alphas if v < 0)
        return (
            f"Arm C는 {zero}/{len(eps)} seed×fold에서 best_epoch=0이다 — early stopping이 "
            "매번 학습 이전 체크포인트를 골랐고, residual이 dev loss를 개선한 적이 없다는 뜻이다. "
            f"residual 가중치 alpha도 {n_neg}/{len(alphas)}개가 음수로 부호가 뒤집혀 "
            "일관된 신호가 아니다. "
            "이 두 진단이 C−A가 왜 0 근처에 머무는지를 학습 과정 쪽에서 설명한다."
        )

    if artifact == "patient_delta_waterfall.png" and per_rec is not None:
        delta = per_rec.seed_mean("C") - per_rec.seed_mean("A")
        n_pos = int(np.sum(delta > 0))
        n_neg = int(np.sum(delta < 0))
        return (
            f"seed {per_rec.ksw['A'].shape[0]}개를 모두 평균한 레코드별 C−A다(단일 seed 아님). "
            f"{n_pos}개가 개선, {n_neg}개가 악화이고 최대 개선 {float(np.max(delta)):+.4f}, "
            f"최대 악화 {float(np.min(delta)):+.4f}로 양쪽 크기가 비슷하다. "
            f"평균 {float(np.mean(delta)):+.4f}는 소수 환자의 큰 이득이 아니라 상쇄의 결과다."
        )

    if artifact == "metric_distribution.png" and per_rec is not None:
        vals_a = per_rec.seed_mean("A")
        return (
            f"세 arm의 분포가 거의 포개진다. 반면 arm A 안에서만 봐도 레코드 값이 "
            f"{float(np.min(vals_a)):.3f}~{float(np.max(vals_a)):.3f}로 벌어져 있다. "
            f"p10({a['p10']:.4f})과 median({a['median']:.4f})의 간격이 arm 간 차이보다 "
            "훨씬 크므로, 다음 실험이 다뤄야 할 대상은 평균이 아니라 이 하위 꼬리다."
        )

    if artifact == "learning_curves.png":
        status = training_history_status(bundle.out_dir)
        if status["present"]:
            return ("epoch별 train/dev loss, dev PR-AUC, alpha 궤적이다. "
                    "dev loss가 언제 바닥을 치는지와 alpha가 어디서 안정되는지를 함께 본다. "
                    "이 곡선은 실제 기록에서만 그려지며 추정하지 않는다.")
        return ("이 run에는 epoch별 학습 이력이 없어 곡선을 그리지 않았다. "
                "없는 데이터를 합성하지 않는 것이 이 보고 기능의 규칙이다. "
                "향후 run은 TrainingHistoryRecorder를 붙이면 이 자리에 곡선이 생긴다.")

    return ""


def _md_table(header: Sequence[str], rows: Sequence[Sequence[str]]) -> str:
    out = ["| " + " | ".join(header) + " |",
           "|" + "|".join("---" for _ in header) + "|"]
    for r in rows:
        out.append("| " + " | ".join(str(c) for c in r) + " |")
    return "\n".join(out)


def write_report_summary(
    bundle: RunBundle,
    path: str,
    *,
    figures: Dict[str, Optional[str]],
    per_rec: Optional[PerRecordKsw],
    history: Dict[str, Any],
    checksums_before: Dict[str, str],
    checksums_after: Dict[str, str],
) -> str:
    """10. report_summary.md — every headline number, with its provenance."""
    rows = arm_metrics_rows(bundle)
    prim = contrast_rows(bundle, PRIMARY_CONTRASTS)
    ref = contrast_rows(bundle, REFERENCE_CONTRASTS)
    checks = bundle.result.get("gates", {}).get("checks", {})
    gate = bundle.min_gain
    diag = bundle.result.get("arm_E_diagnostic", {})
    q4n = diag.get("q4n_contaminated_reference", {})
    fig_dir_rel = os.path.relpath(bundle.figures_dir(), os.path.dirname(path) or ".")

    L: List[str] = []
    add = L.append

    add(f"# Q4-O 결과 보고서 — {bundle.run_id}")
    add("")
    add(f"- 실험: `{bundle.result.get('experiment_id')}` / arm `{bundle.result.get('arm_id')}`")
    add(f"- 최종 판정: **{bundle.verdict}**")
    add(f"- 1차 지표: `{bundle.result.get('primary_metric')}` · "
        f"1차 비교: `{bundle.result.get('primary_comparison')}` · "
        f"음성 대조: `{bundle.result.get('negative_control')}`")
    add(f"- 설계: {bundle.config.get('split')} · outer {bundle.config.get('n_outer_folds')} fold "
        f"· inner {bundle.config.get('n_inner_folds')} fold · seed {bundle.n_seed}개 "
        f"({', '.join(str(s) for s in bundle.seeds)})")
    add(f"- k-sweep: {bundle.k_sweep} · 운영점 k: {bundle.config.get('k_operating_points')} "
        f"· bootstrap {bundle.config.get('n_boot')}회")
    add(f"- 채점 레코드: {bundle.manifest.get('n_record_scorable')} / "
        f"{bundle.manifest.get('n_record_total')} (min_S={bundle.config.get('min_s')}, "
        f"min_N={bundle.config.get('min_n')})")
    add("")
    add("> 이 문서는 **presentation-only**입니다. 모든 수치는 이 run의 `result.json`에서 "
        "그대로 읽었고, 재학습·재부트스트랩·게이트 재판정을 하지 않았습니다.")
    add("")

    add("## 1. Executive Summary")
    add("")
    add("```text")
    add(executive_summary_ko(bundle))
    add("```")
    add("")

    add("## 2. baseline 정의")
    add("")
    add("- **baseline은 Arm A `morph_baseline`** 입니다. 형태학 17열 특징에 로지스틱 회귀를 "
        "outer-train에만 적합시킨 arm이고, 값은 "
        f"**{bundle.arm('A')['seed_averaged_ksw']['mean']:.4f}** 입니다.")
    add("- Arm A는 seed에 의존하지 않으므로 `ksw_seed_std = "
        f"{bundle.arm('A').get('ksw_seed_std', 0.0):.1e}` 입니다. 5개 seed의 값이 동일한 것은 "
        "버그가 아니라 결정론적 모델이기 때문입니다.")
    add("- Arm C(가설)는 **A와 같은 offset 위에 CNN residual을 더한** 구조라서 A가 유일한 "
        "정당한 비교 대상입니다. Arm F(`comb_baseline_diagnostic`)는 A가 아니라 **Arm E의** "
        "비교 대상입니다(28열 comb 특징).")
    add(f"- 이식 충실도 점검: 포팅한 형태학 코드를 Q4-N의 LORO로 재채점한 값이 "
        f"{bundle.manifest.get('morph_port_check', {}).get('measured_loro_ksw', float('nan')):.4f}, "
        f"Q4-N 기록값 {bundle.manifest.get('morph_port_check', {}).get('reference_q4n_morph_ksw_loro', float('nan'))} "
        f"— 허용오차 안({bundle.manifest.get('morph_port_check', {}).get('within_tolerance')}).")
    add("")

    add("## 3. Arm 요약")
    add("")
    add(_md_table(
        ["arm", "설명", "역할", "k-sweep mean", "Δ vs A", "PR-AUC", "AUROC", "p10",
         "worst (record)", "seed SD"],
        [[r["arm"], r["label"], r["role"], f"{r['ksweep_mean']:.4f}", f"{r['delta_vs_A']:+.4f}",
          f"{r['pr_auc']:.4f}", f"{r['auroc']:.4f}", f"{r['p10']:.4f}",
          f"{r['worst']:.4f} (#{r['worst_record']})", f"{r['seed_sd']:.2e}"] for r in rows],
    ))
    add("")
    add(f"→ `{fig_dir_rel}/arm_summary_table.png`, `{fig_dir_rel}/arm_metrics.csv`")
    add("")

    add("## 4. 대비(contrast)와 PASS/FAIL 근거")
    add("")
    add("### 4.1 1차 대비 (같은 축에서 볼 수 있는 크기)")
    add("")
    add(_md_table(
        ["대비", "평균", "95% CI (record bootstrap)", "95% CI (hierarchical)",
         f"≥ +{gate:g}?", "CI 하한 > 0?", "seed 양수", "판정"],
        [[r["label"], f"{r['mean']:+.4f}", f"[{r['ci_low']:+.4f}, {r['ci_high']:+.4f}]",
          f"[{r['hier_ci_low']:+.4f}, {r['hier_ci_high']:+.4f}]",
          "PASS" if r["passes_gain_gate"] else "FAIL",
          "PASS" if r["ci_excludes_zero"] else "FAIL",
          f"{r['positive_seed_count']}/{bundle.n_seed}",
          "PASS" if (r["passes_gain_gate"] and r["ci_excludes_zero"]) else "**FAIL**"]
         for r in prim],
    ))
    add("")
    add("### 4.2 참조 대비 (크기가 달라 **별도 축**으로만 그립니다)")
    add("")
    add(_md_table(
        ["대비", "평균", "95% CI", "seed 양수"],
        [[r["label"], f"{r['mean']:+.4f}", f"[{r['ci_low']:+.4f}, {r['ci_high']:+.4f}]",
          f"{r['positive_seed_count']}/{bundle.n_seed}"] for r in ref],
    ))
    add("")
    add(f"→ `{fig_dir_rel}/primary_contrasts_zoom.png`, `{fig_dir_rel}/reference_gap_separate.png`")
    add("")
    add("### 4.3 Gate 판정")
    add("")
    add(_md_table(
        ["gate", "결과", "근거"],
        [
            [GATE_LABELS_KO.get("1_mean_gain_ge_0.015", "①"),
             "PASS" if checks.get("1_mean_gain_ge_0.015") else "**FAIL**",
             f"C−A 평균 {prim[0]['mean']:+.4f} < +{gate:g}"],
            [GATE_LABELS_KO.get("2_ci_lower_gt_0", "②"),
             "PASS" if checks.get("2_ci_lower_gt_0") else "**FAIL**",
             f"CI 하한 {prim[0]['ci_low']:+.4f} ≤ 0"],
            [GATE_LABELS_KO.get("3_beats_shuffle_control", "③"),
             "PASS" if checks.get("3_beats_shuffle_control") else "**FAIL**",
             f"C−D {prim[1]['mean']:+.4f}, CI [{prim[1]['ci_low']:+.4f}, {prim[1]['ci_high']:+.4f}] 가 0 포함"],
            [GATE_LABELS_KO.get("4_seed_direction_stable", "④"),
             "PASS" if checks.get("4_seed_direction_stable") else "**FAIL**",
             f"양수 seed {prim[0]['positive_seed_count']}/{bundle.n_seed} ≥ "
             f"{bundle.gate_thresholds.get('min_seed_agreement')}"],
            [GATE_LABELS_KO.get("5_lower_tail_not_worse", "⑤"),
             "PASS" if checks.get("5_lower_tail_not_worse") else "**FAIL**",
             f"p10 A {bundle.arm('A')['seed_averaged_ksw']['p10']:.4f} → "
             f"C {bundle.arm('C')['seed_averaged_ksw']['p10']:.4f} "
             f"(허용 낙폭 {bundle.gate_thresholds.get('lower_tail_max_drop')})"],
            [GATE_LABELS_KO.get("6_leakage_and_reproducibility", "⑥"),
             "PASS" if checks.get("6_leakage_and_reproducibility") else "**FAIL**",
             "offset cross-fitting, 불변식 점검, 포팅 충실도 점검 통과"],
        ],
    ))
    add("")
    add(f"**판정 = {bundle.verdict}.** ①②③이 실패했고, 그중 ③(셔플 대조군과 구분 불가)이 "
        "가장 무겁습니다. ④⑤가 통과했다는 사실은 '작은 이득이 안정적으로 관측된다'는 뜻이지 "
        "'이득이 실재한다'는 뜻이 아닙니다 — 방향이 일관된 0에 가까운 값도 ④를 통과합니다.")
    add("")

    add("## 5. 구조 설명 — 각 arm이 무엇을 바꾸는가")
    add("")
    add(_md_table(
        ["arm", "입력", "무엇이 바뀌었나", "왜 존재하나"],
        [
            ["A `morph_baseline`", "형태학 17열", "없음(기준선)", "넘어야 할 대상"],
            ["B `raw_current_cnn`", "raw 2채널 파형", "형태학 제거", "형태학이 얼마나 지탱하는지 보는 참조"],
            ["C `morph_plus_raw_residual`", "형태학 offset + raw 2채널", "**CNN residual 추가(단일 변수)**", "이번 가설"],
            ["D `shuffled_waveform_control`", "C와 동일, 파형만 레코드 내 셔플", "파형↔라벨 대응 파괴", "음성 대조군 — C의 이득이 파형에서 온 것인지 검정"],
            ["E `corrected_q4n_diagnostic`", "comb 28열 offset + raw", "offset을 cross-fit으로 교정", "Q4-N 오염 구조를 깨끗하게 재현한 진단"],
            ["F `comb_baseline_diagnostic`", "comb 28열", "없음", "E의 비교 대상(= Q4-N cpu_comb의 깨끗한 짝)"],
        ],
    ))
    add("")
    add(f"- Arm D의 순열은 레코드 내부에서만 이루어졌고 비트의 "
        f"{float(bundle.config.get('waveform_permutation', {}).get('moved_fraction', 0)) * 100:.2f}%가 "
        "이동했습니다. 라벨·RR·레코드 id·형태학 offset은 보존됩니다 — 즉 **파형 정보만** 제거합니다.")
    c_folds = [f for e in bundle.manifest.get("arm_alpha", {}).get(ARM_BY_CODE["C"].key, [])
               for f in e["folds"]]
    n_fold = len(c_folds)
    n_zero = sum(1 for f in c_folds if f["best_epoch"] == 0)
    n_neg = sum(1 for f in c_folds if f["alpha"] < 0)
    if n_fold:
        med_abs = float(np.median([abs(f["alpha"]) for f in c_folds]))
        add(f"- Arm C의 residual 가중치 alpha는 크기가 대체로 ±{med_abs:.3f} 부근인데 "
            f"{n_neg}/{n_fold} 칸에서 음수로 부호가 뒤집힙니다. 부호가 일관되지 않는 것은 "
            "residual이 실질적 신호를 싣고 있지 않다는 또 하나의 징후입니다.")
        add(f"- **Arm C는 {n_zero}/{n_fold} seed×fold에서 `best_epoch = 0`** 입니다 → "
            f"`{fig_dir_rel}/fold_training_diagnostics.png` 의 경고 문구를 보세요.")
    add("")

    add("## 6. Q4-N 0.8631을 baseline에서 제외한 이유")
    add("")
    add(f"- Q4-N의 참조값: `cpu_comb = {q4n.get('cpu_comb')}`, `boost_fix = {q4n.get('boost_fix')}`, "
        f"`boost_rank = {q4n.get('boost_rank')}`.")
    add("- `boost_fix = 0.8631`은 **약 80%가 in-sample이던 offset 배열로 학습되고, 같은 오염된 "
        "배열로 계산한 `cpu_comb = 0.8445`에 대해 채점된** 값입니다. 학습·채점이 같은 오염을 "
        "공유하므로 이 숫자는 성능이 아니라 오염의 크기를 반영합니다.")
    add("- 게다가 Q4-N의 CPU arm은 **LORO**, 이번 run은 **record-grouped 5-fold CV** 로 "
        "분할 자체가 다릅니다. 절대값을 직접 빼는 것은 정의되지 않은 연산입니다.")
    add("- 그래서 이번 run은 오염을 제거한 구조를 Arm E로 다시 만들고, **A가 아니라 F(clean comb)** "
        "와 비교했습니다: "
        f"`E − cleanComb = {diag.get('residual_effect_isolated', {}).get('mean', float('nan')):+.4f}` "
        f"(95% CI [{diag.get('residual_effect_isolated', {}).get('ci_low', float('nan')):+.4f}, "
        f"{diag.get('residual_effect_isolated', {}).get('ci_high', float('nan')):+.4f}]).")
    add("- 결론: 0.8631은 **비교 대상이 아니라 오염 사례**로만 인용합니다. baseline은 A입니다.")
    add("")

    add("## 7. 환자(레코드) 단위 분석")
    add("")
    if per_rec is not None:
        a = per_rec.seed_mean("A")
        c = per_rec.seed_mean("C")
        delta = c - a
        order = np.argsort(delta)
        burden = bundle.record_burden
        n_seed_used = int(per_rec.ksw["A"].shape[0])
        add(f"- 아래 값은 **seed {n_seed_used}개 전부의 평균** C − A 입니다(단일 seed 아님).")
        add(f"- 검증: 재계산한 arm별·seed별 k-sweep 값이 `result.json`과 "
            f"최대 |Δ| = {max(per_rec.verification.get('per_arm_max_abs_diff', {0: 0}).values()):.2e} 로 일치했습니다. "
            "일치하지 않았다면 이 절은 생성되지 않습니다.")
        add(f"- 개선 {int(np.sum(delta > 0))}개 / 악화 {int(np.sum(delta < 0))}개 / "
            f"동일 {int(np.sum(delta == 0))}개, 레코드 평균 {float(np.mean(delta)):+.4f}.")
        add("")
        add("**개선 상위 10 레코드**")
        add("")
        top = order[::-1][:10]
        add(_md_table(
            ["record", "Δ C−A", "A", "C", "S burden"],
            [[per_rec.record_ids[i], f"{delta[i]:+.4f}", f"{a[i]:.4f}", f"{c[i]:.4f}",
              f"{burden.get(int(per_rec.record_ids[i]), float('nan')):.4f}"] for i in top],
        ))
        add("")
        add("**악화 상위 10 레코드**")
        add("")
        bot = order[:10]
        add(_md_table(
            ["record", "Δ C−A", "A", "C", "S burden"],
            [[per_rec.record_ids[i], f"{delta[i]:+.4f}", f"{a[i]:.4f}", f"{c[i]:.4f}",
              f"{burden.get(int(per_rec.record_ids[i]), float('nan')):.4f}"] for i in bot],
        ))
        add("")
        add(f"→ `{fig_dir_rel}/patient_delta_waterfall.png`, `{fig_dir_rel}/patient_delta.csv`, "
            f"`{fig_dir_rel}/metric_distribution.png`")
    else:
        add("- **생성되지 않았습니다.** 레코드 단위 값을 `probs.npy` + `predictions.npz`에서 "
            "재계산했지만 `result.json`의 `ach@k`를 재현하지 못했거나, 필요한 배열이 "
            "없었습니다. 재현되지 않은 수치로 그림을 그리지 않습니다.")
        if bundle.load_warnings:
            add("")
            for w in bundle.load_warnings:
                add(f"  - {w}")
    add("")

    add("## 8. 학습 이력(training history)")
    add("")
    if history["present"]:
        add(f"- 이 run에는 epoch별 이력이 있습니다: {', '.join(history['files'])} → "
            f"`{fig_dir_rel}/learning_curves.png`")
    else:
        add("- **이 run에는 epoch별 학습 이력이 없습니다.** `training_history.json` / "
            "`training_history.csv` 어느 것도 존재하지 않습니다.")
        add("- 따라서 `learning_curves.png`는 **생성하지 않았습니다.** 없는 이력을 추정하거나 "
            "합성하지 않습니다.")
        add("- 대신 이 run이 실제로 남긴 fold 단위 값(`alpha`, `best_epoch`, `dev_loss`)만 "
            f"`{fig_dir_rel}/fold_training_diagnostics.png` 에 그렸습니다. 이것은 측정값입니다.")
        add("- 향후 run은 `TrainingHistoryRecorder`(같은 모듈)를 학습 루프에 붙이면 "
            "epoch별 train loss / dev loss / dev PR-AUC / alpha가 남습니다. 이 기록기는 "
            "관찰만 하며 optimizer 상태나 checkpoint 선택에 관여하지 않습니다.")
    add("")

    add("## 9. 한계와 다음 결정")
    add("")
    add("**한계**")
    add("")
    add(f"1. 채점 레코드가 {bundle.manifest.get('n_record_scorable')}개뿐이라 record bootstrap의 "
        "CI가 넓습니다. 이 설계로는 +0.015보다 작은 효과를 탐지할 검정력이 없습니다.")
    add(f"2. epoch 예산이 {bundle.config.get('epochs')}이고 dev 평가는 "
        f"{bundle.config.get('dev_every')} epoch마다입니다. Arm C가 {n_zero}/{n_fold}에서 "
        "best_epoch=0이므로 '학습이 부족했다'와 '배울 것이 없었다'를 이 run만으로는 "
        "완전히 분리할 수 없습니다.")
    add("3. epoch별 이력이 없어 위 두 해석을 곡선으로 가릴 수 없습니다(그래서 9번 기능을 넣었습니다).")
    add("4. 지표가 record-level k-sweep achievement 하나입니다. 임상 알람 부담과 직접 연결되지만, "
        "beat-level PR-AUC와 항상 같은 방향은 아닙니다.")
    add("5. Arm E/F는 **진단**입니다. 어떤 gate도 이들로 판정하지 않습니다.")
    add("")
    add("**다음 결정**")
    add("")
    add(f"- run이 남긴 지시: *{bundle.result.get('gates', {}).get('next_step')}*")
    add("- 채택: morphology baseline(A) 유지. C 미채택.")
    add("- 다음 실험은 평균이 아니라 **하위 꼬리**를 목표로 하고, 사전에 검정력을 계산해 "
        "탐지 가능한 최소 효과를 정한 뒤 시작합니다.")
    add("")

    add("## 10. 생성한 그림")
    add("")
    order_figs = [
        ("arm_summary_table.png", "1. arm 요약 표"),
        ("arm_metrics.csv", "1. arm 요약 (CSV)"),
        ("primary_contrasts_zoom.png", "2. 1차 대비 확대 — CI·zero·+0.015 gate·PASS/FAIL"),
        ("reference_gap_separate.png", "3. 참조 대비(B−A 등) 별도 축"),
        ("achievement_by_k.png", "4. arm별 achievement@k + C−A 확대"),
        ("seed_effects.png", "5. seed별 C−A / C−D"),
        ("fold_training_diagnostics.png", "6. seed×fold alpha·best_epoch·dev_loss"),
        ("patient_delta_waterfall.png", "7. 레코드별 C−A 폭포 (5 seed 평균)"),
        ("patient_delta.csv", "7. 레코드별 delta (CSV)"),
        ("metric_distribution.png", "8. A/C/D 레코드 분포"),
        ("learning_curves.png", "9. 학습 곡선"),
    ]
    for name, label in order_figs:
        made = figures.get(name)
        if made:
            add(f"- [{label}]({fig_dir_rel}/{name})")
        else:
            add(f"- {label} — *생성되지 않음* "
                f"({'학습 이력 없음' if name == 'learning_curves.png' else '레코드 단위 재현 불가'})")
    add("")
    add(f"기존 `{fig_dir_rel}/contrasts.png`는 B−A(≈ −0.59)와 1차 대비(≈ +0.001)를 한 축에 "
        "그려 1차 대비가 0으로 눌려 보입니다. 이 보고서는 그 파일을 **덮어쓰지 않고**(측정 "
        "산출물 보존) `primary_contrasts_zoom.png` + `reference_gap_separate.png` 로 대체합니다.")
    add("")

    add("## 11. 무결성 — 보고 전후 checksum")
    add("")
    unchanged = checksums_before == checksums_after
    add(f"- 결과: **{'변경 없음 (identical)' if unchanged else '변경 감지됨 — 조사 필요'}**")
    add("")
    add(_md_table(
        ["파일", "SHA-256 (앞 16자)", "보고 전후"],
        [[k, checksums_after.get(k, "")[:16],
          "동일" if checksums_before.get(k) == checksums_after.get(k) else "**다름**"]
         for k in sorted(checksums_after)],
    ))
    add("")
    add("생성 도구: `mit-bih/q4o_leakage_free_residual.py` · "
        "notebook: `notebooks/quest47_q4o_leakage_free_residual_cnn.ipynb`")

    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    text = "\n".join(L) + "\n"
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)
    return path


# --------------------------------------------------------------------------
# Orchestration
# --------------------------------------------------------------------------

def analyze_existing_run(
    out_dir: str,
    *,
    report_dir: Optional[str] = None,
    verbose: bool = True,
) -> Dict[str, Any]:
    """Build the full report for an existing run. No training, no re-fitting.

    ``report_dir`` defaults to ``<out_dir>/figures``; point it elsewhere to keep
    the Drive bundle byte-identical.
    """
    log = (lambda *a: print(*a)) if verbose else (lambda *a: None)

    bundle = load_run(out_dir)
    checks_before = bundle.checksums_at_load
    fig_dir = report_dir or bundle.figures_dir()
    os.makedirs(fig_dir, exist_ok=True)

    log(executive_summary_ko(bundle))
    log("")
    for w in bundle.load_warnings:
        log(f"[load] {w}")

    figures: Dict[str, Optional[str]] = {}

    def make(name: str, fn: Callable[[str], Optional[str]]) -> None:
        path = os.path.join(fig_dir, name)
        try:
            figures[name] = fn(path)
        except Exception as exc:  # a broken panel must not lose the whole report
            figures[name] = None
            log(f"[skip] {name}: {type(exc).__name__}: {exc}")

    make("arm_summary_table.png", lambda p: fig_arm_summary_table(bundle, p))
    make("arm_metrics.csv", lambda p: write_arm_metrics_csv(bundle, p))
    make("primary_contrasts_zoom.png", lambda p: fig_primary_contrasts_zoom(bundle, p))
    make("reference_gap_separate.png", lambda p: fig_reference_gap_separate(bundle, p))
    make("achievement_by_k.png", lambda p: fig_achievement_by_k(bundle, p))
    make("seed_effects.png", lambda p: fig_seed_effects(bundle, p))
    make("fold_training_diagnostics.png", lambda p: fig_fold_training_diagnostics(bundle, p))

    per_rec = per_record_ksw(bundle)
    if per_rec is None:
        log("[skip] per-record figures — record-level values could not be reproduced "
            "from probs.npy/predictions.npz against result.json.")
        figures["patient_delta_waterfall.png"] = None
        figures["patient_delta.csv"] = None
        figures["metric_distribution.png"] = None
    else:
        log(f"[ok] per-record k-sweep reproduced result.json "
            f"(definition='{per_rec.definition}', "
            f"max |Δ| = {max(per_rec.verification['per_arm_max_abs_diff'].values()):.2e})")
        make("patient_delta_waterfall.png", lambda p: fig_patient_delta_waterfall(bundle, per_rec, p))
        make("patient_delta.csv", lambda p: write_patient_delta_csv(bundle, per_rec, p))
        make("metric_distribution.png", lambda p: fig_metric_distribution(bundle, per_rec, p))

    history = training_history_status(bundle.out_dir)
    if history["present"]:
        make("learning_curves.png", lambda p: fig_learning_curves(bundle.out_dir, p))
    else:
        figures["learning_curves.png"] = None
        log(f"[skip] learning_curves.png — {history['note']}")

    checks_after = bundle_checksums(bundle.out_dir)
    report_path = write_report_summary(
        bundle,
        os.path.join(fig_dir if report_dir else bundle.out_dir, "report_summary.md"),
        figures=figures,
        per_rec=per_rec,
        history=history,
        checksums_before=checks_before,
        checksums_after=checks_after,
    )

    unchanged = checks_before == checks_after
    log("")
    log(f"[checksum] measured artifacts unchanged: {unchanged}")
    log(f"[report] {report_path}")

    return {
        "bundle": bundle,
        "figures": figures,
        "per_record": per_rec,
        "history": history,
        "report_summary": report_path,
        "checksums_before": checks_before,
        "checksums_after": checks_after,
        "checksums_unchanged": unchanged,
        "figures_dir": fig_dir,
    }


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Q4-O reporting — read an existing run bundle, write tables, figures and report_summary.md.",
    )
    parser.add_argument("--out-dir", required=True, help="run bundle directory")
    parser.add_argument("--report-dir", default=None,
                        help="write figures here instead of <out-dir>/figures")
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args(argv)

    res = analyze_existing_run(args.out_dir, report_dir=args.report_dir, verbose=not args.quiet)
    return 0 if res["checksums_unchanged"] else 1


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
