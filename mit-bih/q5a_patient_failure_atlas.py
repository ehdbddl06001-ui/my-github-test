#!/usr/bin/env python3
"""EXP-2026-004 / Q5-A — patient-level S-beat failure atlas and causal-branch selection.

Spec: ``experiments/specs/EXP-2026-004-q5a-patient-failure-atlas.md``
Status: DESIGN / RESULT NOT RUN — nothing in this file is a result.

What this is
------------
An **analysis-only** experiment. It never trains, never regenerates stored
probabilities and never touches a source run bundle. It reads what previous
runs already saved (predictions/logits plus the processed beat arrays) and
answers one question:

    In which patients, beats and situations does S-beat classification fail,
    and which single failure-associated factor is worth *intervening on* in a
    later experiment (Q5-B)?

Language boundary (enforced in code, figures and the summary): Q5-A is
observational. It may report **failure-associated factors** and **candidate
intervention hypotheses**. It may not promote an association to a cause; only
Q5-B, which changes one factor and carries a negative control, can test that.
``UNRESOLVED`` / ``INSUFFICIENT_ARTIFACTS`` / ``DATA_INTEGRITY_BLOCKED`` are
first-class verdicts — a branch is never forced.

Closed directions honoured here (project state, 2026-08-08): the raw-waveform
residual CNN path is CLOSED (Q4-O NO-GO, Q4-Q mechanism+utility fail) and the
INCART stage is not reopened as a rescue. Q5-A neither resumes nor proposes a
variant of either.

What this module reuses (imported, never copied)
------------------------------------------------
Q4-O: ``RunLog``, patient/record bootstraps, provenance helpers, ``sha256_file``,
``_json_safe``. Q4-Q: the canonical de Chazal DS1/DS2 record sets and the
S class index, so cohort definitions cannot drift between experiments.

Commands
--------
    python mit-bih/test_q5a_patient_failure_atlas.py
    python mit-bih/q5a_patient_failure_atlas.py --mode DESIGN
    python mit-bih/q5a_patient_failure_atlas.py --mode INVENTORY \
        --roots <drive runs dir> [--registry <registry.jsonl>] --out <dir>
    python mit-bih/q5a_patient_failure_atlas.py --mode ANALYZE \
        --data <ecg_multi.npz or mamba_data.npz> --inventory <inventory dir> \
        --out <run dir>
    python mit-bih/q5a_patient_failure_atlas.py --mode REPORT --run <run dir>
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import sys
import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import q4o_leakage_free_residual as Q4O  # noqa: E402
import q4q_transportability_replication as QQ  # noqa: E402
from q4o_leakage_free_residual import (  # noqa: E402
    RunLog, SEED0,
    assert_disjoint, git_commit_sha, gpu_info, package_versions,
    paired_record_bootstrap, sha256_file, _json_safe,
)

# ─────────────────────────────────────────────────────────────────────────────
# Identity and pre-registered constants — frozen before any analysis.
# ─────────────────────────────────────────────────────────────────────────────
EXPERIMENT_ID = "EXP-2026-004"
ARM_ID = "Q5-A"
RUN_SLUG = "q5a_patient_failure_atlas"
STATUS = "PREREGISTERED ANALYSIS ONLY / RESULT NOT RUN"

MODULE_VERSION = 2
MODULE_BUILD = ("2026-08-09 q5a.2 — legacy ablation adapter: prediction files "
                "detected by KEY (ens.npz), tag folders are their own runs, "
                "row correspondence VERIFIED against the frozen source before "
                "any key is derived, paired control scoped to the primary's "
                "run, absent historical baseline recorded as a result, "
                "annotation symbols joined from raw_ann/mitdb; still "
                "analysis-only and no run has been executed")

MODES = ("DESIGN", "INVENTORY", "ANALYZE", "REPORT")
DEFAULT_MODE = "DESIGN"

#: Q5-A performs no optimisation of any kind. The test contract greps this
#: file for the tokens below, so they are assembled from fragments — writing
#: them out literally here would make the guard flag its own definition.
FORBIDDEN_TRAINING_TOKENS = ("torch." + "optim", "." + "backward(",
                             "build_" + "residual_net",
                             "diagnostic_" + "train_one_fold",
                             "fit_" + "one_fold")
#: Directions that are closed and must not be reopened by this experiment.
CLOSED_DIRECTIONS = ("residual CNN", "INCART rescue")

# The one fixed problem (spec §1). The method is deliberately NOT fixed.
FIXED_PROBLEM = ("improve the per-patient lower tail and the failure patients "
                 "of S-beat performance on new patients")

# Baselines to freeze from stored artifacts (spec §5, Decision log 2026-08-09).
# The recorded numbers are *claims to check*, never selection criteria.
#
# ``role`` drives what a missing candidate means:
#   primary          — no artifact => MISSING_BASELINE, analysis stops;
#   paired_control   — must come from the SAME parent run as the primary, so a
#                      name that repeats across unrelated runs cannot collide;
#   historical_unverified — recorded in prose only; absence is a RESULT, not a
#                      stop, and never a reason to retrain.
BASELINE_TARGETS: Dict[str, Dict[str, object]] = {
    "V10": {"name_tokens": ("pwave",), "role": "primary",
            "recorded_s_prauc": 0.660,
            "recorded_in": "research/PROJECT_STATE.md (needs artifact check)",
            "source_script": "mit-bih/colab_step9d_final.py :: run_final('pwave')"},
    "BASE26": {"name_tokens": ("base26",), "role": "paired_control",
               "same_parent_as": "V10", "recorded_s_prauc": None,
               "source_script": "mit-bih/colab_step9d_final.py :: run_final('base26')",
               "note": ("the paired control of V10: same script, same seeds, "
                        "same weighing — only the P-wave feature block differs "
                        "(use_pw = tag == 'pwave')")},
    "V9": {"name_tokens": ("kink_noctx", "kink-noctx"),
           "role": "historical_unverified", "recorded_s_prauc": 0.597,
           "recorded_in": "research/PROJECT_STATE.md (needs artifact check)",
           "note": ("measured 2026-08-09: no run folder, no tag folder and no "
                    "Drive file carries this name. Recorded as ARTIFACT_ABSENT "
                    "— the 0.597 claim stays unverified and is NOT retrained.")},
}
#: Optional third comparison arm: the Q4-Q morphology baseline (Arm A).
Q4Q_BASELINE_KEY = "Q4Q_ARM_A"
ROLE_PRIMARY = "primary"
ROLE_CONTROL = "paired_control"
ROLE_HISTORICAL = "historical_unverified"

# Cohort definitions are imported, not redefined, so they cannot drift.
DS1_RECORDS = QQ.DS1_RECORDS
DS2_RECORDS = QQ.DS2_RECORDS
MIT_ALL_RECORDS = QQ.MIT_ALL_RECORDS
S_INDEX = QQ.MIT_S_INDEX
CLASS_NAMES = QQ.CLASS_NAMES
AUDIT_RECORDS: Tuple[int, ...] = (208, 213)   # measured beat deficits, Q4-Q

# Beat-key extraction (spec §6). Priority 1 is the original annotation key.
BEAT_KEY_RECORD_FIELDS = ("pid", "record", "record_id", "rid")
BEAT_KEY_SAMPLE_FIELDS = ("sample", "ann_sample", "samp", "t", "time", "index")
BEAT_KEY_SYMBOL_FIELDS = ("sym", "symbol", "ann_sym")
BEAT_KEY_DB_FIELDS = ("db", "database", "source_db")
KEY_MODE_ANNOTATION = "annotation"
KEY_MODE_FINGERPRINT = "waveform_fingerprint"
KEY_MODE_SOURCE_VERIFIED = "source_row_verified"
KEY_MODE_NONE = "unavailable"
FINGERPRINT_DECIMALS = 4

# Legacy artifacts (the 2026-07/08 ablation series) store `prob`/`y`/`pid` and
# no annotation index. Their rows come from one frozen source file, so the row
# correspondence can be VERIFIED element-wise (pid and label must match on every
# row) instead of assumed — that verification, not row order, is what earns a
# stable key. A single mismatching row is a STOP.
LEGACY_SCORE_FIELDS = ("prob", "probs", "p", "score", "scores", "logit",
                       "logits", "ens")
LEGACY_LABEL_FIELDS = ("y_true", "y", "y2", "label")
#: Column of the S class in a stored multi-class probability matrix. The
#: legacy 3-class head is ordered (N, S, V) — same S index as everywhere else.
S_COLUMN = S_INDEX
LEGACY_CLASS_WIDTHS = (2, 3, 5)
#: MIT-BIH annotation cache. Measured 2026-08-09: it lives under
#: ``mitbih/raw_ann/mitdb`` (folder id 151DJAcjCbDXCoy9ZIPudbtSuVziG1fnj), not
#: under ``mitbih/mitdb`` as research/ASSETS.md used to say.
ANN_DIR_CANDIDATES = ("raw_ann/mitdb", "mitdb", "raw_ann/mitdbdb")
ANN_SYMBOL_MIN_MATCH = 0.95      # below this the symbols are declared unusable

# S subtypes inside AAMI S (spec §8.3).
S_SUBTYPES: Tuple[str, ...] = ("A", "a", "J", "S")
SUBTYPE_MIN_N = 20                 # below this a subtype row is descriptive only

# Feature blocks (spec §9) — fixed before looking at any result.
BLOCKS: Tuple[str, ...] = ("B_ATRIAL", "B_RR", "B_QUALITY", "B_SUBTYPE",
                           "B_PATIENT")

# Pre-registered branch labels (spec §10).
BRANCH_INSUFFICIENT = "INSUFFICIENT_ARTIFACTS"
BRANCH_DATA_BLOCKED = "DATA_INTEGRITY_BLOCKED"
BRANCH_QUALITY = "Q5B_QUALITY_GATE_OR_PREPROCESSING"
BRANCH_ATRIAL = "Q5B_ATRIAL_EVIDENCE_BOTTLENECK"
BRANCH_RR = "Q5B_HIERARCHICAL_RR_ATRIAL_MODEL"
BRANCH_PATIENT = "Q5B_PATIENT_ROBUST_OBJECTIVE_PILOT"
BRANCH_UNRESOLVED = "UNRESOLVED"
BRANCHES = (BRANCH_INSUFFICIENT, BRANCH_DATA_BLOCKED, BRANCH_QUALITY,
            BRANCH_ATRIAL, BRANCH_RR, BRANCH_PATIENT, BRANCH_UNRESOLVED)
BLOCK_TO_BRANCH = {"B_QUALITY": BRANCH_QUALITY, "B_ATRIAL": BRANCH_ATRIAL,
                   "B_RR": BRANCH_RR}

# Branch-selection thresholds — pre-registered, never tuned on the result.
BLOCK_MIN_PATIENT_DIRECTION = 0.60   # fraction of patients moving the same way
BLOCK_MARGIN = 1.25                  # winner must lead the runner-up by 25%
BLOCK_MIN_EVENTS = 30                # errors needed before a block is scored
DROP_RECORDS_FOR_STABILITY = 2       # effect must survive dropping the top 2
PATIENT_HETEROGENEITY_MIN = 0.15     # p90-p10 spread of patient S PR-AUC
PATIENT_PERSISTENCE_MIN = 0.50       # V9/V10 worst-quartile overlap fraction

NB_BOOT = 2000
CALIBRATION_BINS = 10
GALLERY_TOP_N = 4                    # per category, sort keys fixed in code

# Result statuses (spec §12).
STATUS_MEASURED = "MEASURED"
STATUS_BLOCKED = "BLOCKED_MEASURED"
STATUS_NOT_RUN = "RESULT_NOT_RUN"
STATUS_SMOKE = "SMOKE_NOT_A_RESULT"

BUNDLE_FILES = ("config.json", "manifest.json", "result.json", "log.txt",
                "source_inventory.json", "source_inventory.csv",
                "baseline_freeze.json", "matching_audit.csv",
                "patient_metrics.csv", "subtype_metrics.csv",
                "rr_timing_metrics.csv", "atrial_proxy_metrics.csv",
                "quality_metrics.csv", "model_disagreement.csv",
                "mechanism_evidence.csv", "decision.json", "summary.md")
BLOCKED_BUNDLE_FILES = ("config.json", "manifest.json", "result.json",
                        "log.txt", "source_inventory.json",
                        "source_inventory.csv", "baseline_freeze.json",
                        "decision.json", "summary.md")

FIGURES = ("inventory_gate_dashboard.png", "baseline_comparison_table.png",
           "patient_waterfall_paired_delta.png", "patient_lower_tail_table.png",
           "subtype_prauc_fn.png", "rr_coupling_error_heatmap.png",
           "atrial_proxy_vs_error.png", "quality_and_208_213_audit.png",
           "calibration_pr_curves.png", "model_disagreement_matrix.png",
           "block_evidence_forest.png", "branch_decision_matrix.png",
           "error_gallery.png")
BLOCKED_FIGURES = ("inventory_gate_dashboard.png",)


class Q5AError(RuntimeError):
    """Loud failure with the cause and the fix — no silent fallback (spec §4)."""


def run_dir_name(timestamp: str) -> str:
    return f"{timestamp}_{EXPERIMENT_ID}_{RUN_SLUG}"


def resolve_mode(mode: str) -> str:
    """Exactly one of MODES; anything else is a hard error (spec §4)."""
    m = str(mode).strip().upper()
    if m not in MODES:
        raise Q5AError(f"mode must be exactly one of {MODES}, got {mode!r}")
    return m


def assert_analysis_only(path: Optional[str] = None) -> Dict[str, object]:
    """Evidence that Q5-A cannot train: this file contains no training call.

    The check is textual on purpose — it is the cheapest artifact a reviewer
    can re-run. ``FORBIDDEN_TRAINING_TOKENS`` itself is skipped.
    """
    path = path or os.path.abspath(__file__)
    with open(path, "r", encoding="utf-8") as fh:
        lines = fh.readlines()
    hits = []
    for i, line in enumerate(lines, 1):
        if line.lstrip().startswith("#"):
            continue
        for tok in FORBIDDEN_TRAINING_TOKENS:
            if tok in line and "assert_analysis_only" not in line:
                hits.append({"line": i, "token": tok})
    if hits:
        raise Q5AError(f"training call found in an analysis-only module: {hits}")
    return {"analysis_only": True, "checked_file": path,
            "tokens": list(FORBIDDEN_TRAINING_TOKENS),
            "torch_imported": "torch" in sys.modules}


# ─────────────────────────────────────────────────────────────────────────────
# Cohort: the beat-level source the atlas describes.
# ─────────────────────────────────────────────────────────────────────────────
@dataclass
class AtlasCohort:
    """Beat-level arrays for one database. Every array is aligned by row."""

    key: np.ndarray                 # (n,) <U — stable beat key
    key_mode: str                   # annotation | waveform_fingerprint
    db: np.ndarray                  # (n,) <U
    record: np.ndarray              # (n,) int
    y5: np.ndarray                  # (n,) int — AAMI 5-class
    y_s: np.ndarray                 # (n,) bool — True == S
    sym: np.ndarray                 # (n,) <U2 — original annotation symbol
    pre_rr: np.ndarray              # (n,) float, seconds (nan allowed)
    post_rr: np.ndarray             # (n,) float, seconds (nan allowed)
    beat: Optional[np.ndarray]      # (n, lead, width) float32 or None
    fs: float
    records: np.ndarray
    idx_of: Dict[int, np.ndarray] = field(default_factory=dict)

    @property
    def n(self) -> int:
        return int(len(self.y_s))

    def rows_of(self, records: Sequence[int]) -> np.ndarray:
        if not len(records):
            return np.zeros(0, int)
        return np.concatenate([self.idx_of[int(r)] for r in records])


def _first_key(files: Sequence[str], candidates: Sequence[str]) -> Optional[str]:
    lower = {f.lower(): f for f in files}
    for c in candidates:
        if c in lower:
            return lower[c]
    return None


def waveform_fingerprint(beat: np.ndarray,
                         decimals: int = FINGERPRINT_DECIMALS) -> np.ndarray:
    """Deterministic per-beat fingerprint (spec §6 priority 2).

    Quantised waveform digest; identical inputs always give identical strings.
    Never a substitute for the annotation key when that key exists, and only
    usable after the uniqueness check in :func:`build_beat_keys`.
    """
    import hashlib
    b = np.asarray(beat, float)
    if b.ndim == 2:
        b = b[:, None, :]
    q = np.round(b, decimals)
    out = np.empty(len(q), dtype="<U32")
    for i in range(len(q)):
        out[i] = hashlib.sha1(q[i].tobytes()).hexdigest()[:32]
    return out


def assert_not_positional(keys: np.ndarray) -> None:
    """Refuse keys that are row order in disguise (spec §6: no positional match)."""
    k = np.asarray(keys)
    try:
        as_int = k.astype(np.int64)
    except (ValueError, TypeError):
        return
    if np.array_equal(as_int, np.arange(len(as_int))):
        raise Q5AError(
            "beat keys are a plain 0..n-1 row index — that is positional "
            "matching, which is forbidden. Provide (db, record, "
            "annotation sample, symbol) or a verified waveform fingerprint.")


def build_beat_keys(fields: Dict[str, np.ndarray],
                    beat: Optional[np.ndarray] = None,
                    allow_fingerprint: bool = True
                    ) -> Tuple[np.ndarray, str, Dict[str, object]]:
    """Build stable beat keys from whatever the artifact actually carries.

    Priority 1 ``(db, record, annotation sample, symbol)``; priority 2 a
    deterministic waveform fingerprint (only when unique within its record).
    Row position is never used.
    """
    names = list(fields)
    rec_f = _first_key(names, BEAT_KEY_RECORD_FIELDS)
    samp_f = _first_key(names, BEAT_KEY_SAMPLE_FIELDS)
    sym_f = _first_key(names, BEAT_KEY_SYMBOL_FIELDS)
    db_f = _first_key(names, BEAT_KEY_DB_FIELDS)
    if rec_f is None:
        raise Q5AError(
            f"no record field among {BEAT_KEY_RECORD_FIELDS} — a beat key "
            "without a record cannot be matched; aggregate-only at best")
    rec = np.asarray(fields[rec_f]).astype(int)
    db = (np.asarray(fields[db_f]).astype(str) if db_f
          else np.full(len(rec), "mitdb", dtype="<U8"))
    prov: Dict[str, object] = {"record_field": rec_f, "db_field": db_f,
                               "sample_field": samp_f, "symbol_field": sym_f}
    if samp_f is not None:
        samp = np.asarray(fields[samp_f])
        sym = (np.asarray(fields[sym_f]).astype(str) if sym_f
               else np.full(len(rec), "?", dtype="<U2"))
        keys = np.array([f"{d}|{r}|{s}|{y}" for d, r, s, y
                         in zip(db, rec, samp, sym)], dtype=object).astype(str)
        assert_not_positional(np.asarray(fields[samp_f]))
        prov["mode"] = KEY_MODE_ANNOTATION
        return keys, KEY_MODE_ANNOTATION, prov
    if beat is not None and allow_fingerprint:
        fp = waveform_fingerprint(beat)
        keys = np.array([f"{d}|{r}|fp:{f}" for d, r, f in zip(db, rec, fp)])
        dup = _duplicate_keys(keys)
        if dup:
            raise Q5AError(
                f"waveform fingerprints are not unique ({len(dup)} duplicate "
                "keys, e.g. " + str(dup[:3]) + ") — matching would be "
                "ambiguous. STOP and recover the annotation sample index.")
        prov["mode"] = KEY_MODE_FINGERPRINT
        prov["decimals"] = FINGERPRINT_DECIMALS
        return keys, KEY_MODE_FINGERPRINT, prov
    raise Q5AError(
        "no annotation sample field and no waveform available — this artifact "
        "supports aggregate metrics only, never beat-level comparison "
        "(spec §5). Do not fall back to row order.")


def _duplicate_keys(keys: np.ndarray) -> List[str]:
    uniq, counts = np.unique(np.asarray(keys), return_counts=True)
    return [str(u) for u in uniq[counts > 1]]


def load_atlas_source(npz_path: str, db: str = "mitdb",
                      records: Optional[Sequence[int]] = None,
                      fs: float = 360.0,
                      log: Optional[RunLog] = None
                      ) -> Tuple[AtlasCohort, Dict[str, object]]:
    """Load the beat-level source (``ecg_multi.npz`` MIT subset preferred).

    Refuses to guess: missing labels, out-of-range class codes or a record set
    that is not the canonical 44 non-paced records are STOP conditions.
    """
    log = log or RunLog()
    if not os.path.exists(npz_path):
        raise Q5AError(f"atlas source not found: {npz_path}")
    data = np.load(npz_path, allow_pickle=True)
    files = list(data.files)
    fields: Dict[str, np.ndarray] = {}
    rec_f = _first_key(files, BEAT_KEY_RECORD_FIELDS)
    if rec_f is None:
        raise Q5AError(f"{os.path.basename(npz_path)} has no record field "
                       f"(looked for {BEAT_KEY_RECORD_FIELDS} in {files})")
    y_f = _first_key(files, ("y5", "y", "y3", "label"))
    if y_f is None:
        raise Q5AError(f"{os.path.basename(npz_path)} has no label key "
                       f"(y5/y/y3) — cannot build an S-beat atlas")
    rec_all = np.asarray(data[rec_f]).astype(int)
    y_all = np.asarray(data[y_f]).astype(int)
    db_f = _first_key(files, BEAT_KEY_DB_FIELDS)
    db_all = (np.asarray(data[db_f]).astype(str) if db_f
              else np.full(len(rec_all), db, dtype="<U8"))
    mask = np.isin(db_all, (db, "mit", "mit-bih", "mitdb")) if db_f \
        else np.ones(len(rec_all), bool)
    if not mask.any():
        raise Q5AError(f"no {db} rows in {os.path.basename(npz_path)}")
    if y_all.min() < 0 or y_all.max() > 4:
        raise Q5AError(f"labels in {y_f} are not AAMI 5-class coded "
                       f"(range [{y_all.min()},{y_all.max()}]) — STOP")

    keep_records = tuple(sorted(set(rec_all[mask].tolist())))
    wanted = tuple(records) if records is not None else MIT_ALL_RECORDS
    if set(wanted) - set(keep_records):
        raise Q5AError(
            f"source is missing records {sorted(set(wanted) - set(keep_records))[:8]}"
            " from the canonical DS1/DS2 set — cannot build the atlas without "
            "guessing; check the file, do not substitute another one")
    mask &= np.isin(rec_all, wanted)

    def take(name: str, default=None, dtype=None):
        f = _first_key(files, (name,) if isinstance(name, str) else name)
        if f is None:
            return default
        arr = np.asarray(data[f])[mask]
        return arr.astype(dtype) if dtype else arr

    beat = take("beat")
    if beat is not None:
        beat = np.asarray(beat, dtype="float32")
        if beat.ndim == 2:
            beat = beat[:, None, :]
    fields[rec_f] = rec_all[mask]
    if db_f:
        fields[db_f] = db_all[mask]
    for cand in BEAT_KEY_SAMPLE_FIELDS + BEAT_KEY_SYMBOL_FIELDS:
        f = _first_key(files, (cand,))
        if f is not None:
            fields[f] = np.asarray(data[f])[mask]
    keys, key_mode, key_prov = build_beat_keys(fields, beat=beat)
    dup = _duplicate_keys(keys)
    if dup:
        raise Q5AError(f"{len(dup)} duplicate beat keys in the atlas source "
                       f"(e.g. {dup[:3]}) — STOP (spec §6)")

    rec = rec_all[mask]
    y5 = y_all[mask]
    sym_f = _first_key(files, BEAT_KEY_SYMBOL_FIELDS)
    sym = (np.asarray(data[sym_f]).astype(str)[mask] if sym_f
           else np.full(len(rec), "?", dtype="<U2"))
    pre = take(("pre_rr", "prerr"), np.full(len(rec), np.nan))
    post = take(("post_rr", "postrr"), np.full(len(rec), np.nan))
    recs = np.array(sorted(set(rec.tolist())), int)
    cohort = AtlasCohort(
        key=keys, key_mode=key_mode, db=db_all[mask] if db_f else
        np.full(len(rec), db, dtype="<U8"),
        record=rec, y5=y5, y_s=(y5 == S_INDEX), sym=sym.astype("<U2"),
        pre_rr=np.asarray(pre, float), post_rr=np.asarray(post, float),
        beat=beat, fs=float(fs), records=recs,
        idx_of={int(r): np.where(rec == r)[0] for r in recs})
    audit = {
        "file": os.path.basename(npz_path),
        "sha256": sha256_file(npz_path),
        "keys_present": sorted(files),
        "label_key": y_f, "db_filter": db,
        "beat_key_mode": key_mode, "beat_key_provenance": key_prov,
        "n_beat": cohort.n, "n_record": len(recs),
        "n_s": int(cohort.y_s.sum()),
        "class_counts": {CLASS_NAMES[c]: int((y5 == c).sum()) for c in range(5)},
        "has_waveform": beat is not None,
        "has_rr": bool(np.isfinite(cohort.pre_rr).any()),
        "records": [int(r) for r in recs],
    }
    log(f"atlas source: {cohort.n} beats, {len(recs)} records, "
        f"S={audit['n_s']}, key mode {key_mode}")
    return cohort, audit


def find_annotation_dir(drive_root: str) -> Optional[str]:
    """Locate the MIT-BIH ``.atr`` cache. Measured 2026-08-09: it is under
    ``mitbih/raw_ann/mitdb``, not ``mitbih/mitdb``."""
    for rel in ANN_DIR_CANDIDATES:
        d = os.path.join(drive_root, rel)
        if os.path.isdir(d) and any(f.endswith(".atr") for f in os.listdir(d)):
            return d
    return None


def attach_symbols_from_annotations(cohort: AtlasCohort, ann_dir: str,
                                    log: Optional[RunLog] = None
                                    ) -> Dict[str, object]:
    """Recover the ORIGINAL annotation symbols (A/a/J/S/N/V…) for the cohort.

    The cohort's beat key already carries the annotation sample index, so the
    join is exact: (record, sample) -> symbol. When ``wfdb`` is unavailable, or
    when fewer than :data:`ANN_SYMBOL_MIN_MATCH` of the beats join, the symbols
    are declared UNUSABLE and the subtype block is reported as unavailable —
    never approximated.
    """
    log = log or RunLog()
    report: Dict[str, object] = {"ann_dir": ann_dir, "usable": False}
    try:
        import wfdb                                    # noqa: F401
    except Exception as exc:
        report["reason"] = f"wfdb not installed ({exc})"
        return report
    import wfdb
    samples = np.array([int(str(k).split("|")[2]) for k in cohort.key])
    matched = 0
    sym = np.full(cohort.n, "?", dtype="<U2")
    per_record = {}
    for r in cohort.records:
        base = os.path.join(ann_dir, str(int(r)))
        if not os.path.exists(base + ".atr"):
            per_record[str(int(r))] = "missing .atr"
            continue
        try:
            ann = wfdb.rdann(base, "atr")
        except Exception as exc:                        # pragma: no cover
            per_record[str(int(r))] = f"unreadable ({exc})"
            continue
        table = dict(zip(np.asarray(ann.sample).astype(np.int64),
                         np.asarray(ann.symbol).astype(str)))
        idx = cohort.idx_of[int(r)]
        hit = 0
        for i in idx:
            s = table.get(int(samples[i]))
            if s is not None:
                sym[i] = s
                hit += 1
        matched += hit
        per_record[str(int(r))] = {"n": int(len(idx)), "matched": int(hit)}
    frac = float(matched) / max(1, cohort.n)
    report.update({"matched_fraction": frac, "n_matched": int(matched),
                   "per_record": per_record,
                   "threshold": ANN_SYMBOL_MIN_MATCH})
    if frac >= ANN_SYMBOL_MIN_MATCH:
        cohort.sym = sym
        report["usable"] = True
        log(f"annotation symbols joined on {frac:.1%} of beats — subtype "
            "analysis available")
    else:
        report["reason"] = (f"only {frac:.1%} of beats joined to an annotation "
                            "sample; symbols are NOT approximated")
        log(f"annotation join too weak ({frac:.1%}) — subtype block unavailable")
    return report


def rr_from_samples(cohort: AtlasCohort) -> None:
    """Fill pre/post RR from the annotation sample index when the source
    file does not store them. Deterministic, per record, seconds."""
    if np.isfinite(cohort.pre_rr).any():
        return
    samples = np.array([float(str(k).split("|")[2]) for k in cohort.key])
    pre = np.full(cohort.n, np.nan)
    post = np.full(cohort.n, np.nan)
    for r in cohort.records:
        idx = cohort.idx_of[int(r)]
        order = idx[np.argsort(samples[idx])]
        t = samples[order] / cohort.fs
        d = np.diff(t)
        pre[order[1:]] = d
        post[order[:-1]] = d
    cohort.pre_rr = pre
    cohort.post_rr = post


def cohort_split(cohort: AtlasCohort) -> Dict[str, List[int]]:
    """DS1/DS2 patient split with an explicit overlap-0 assertion (spec §7)."""
    recs = set(int(r) for r in cohort.records)
    ds1 = [r for r in DS1_RECORDS if r in recs]
    ds2 = [r for r in DS2_RECORDS if r in recs]
    assert_disjoint(ds1, ds2, "DS1 vs DS2 (Q5-A atlas)")
    return {"ds1": ds1, "ds2": ds2,
            "note": ("DS2 has been used repeatedly in this project; this is a "
                     "descriptive failure audit, NOT an untouched external "
                     "test")}


# ─────────────────────────────────────────────────────────────────────────────
# Inventory: find candidate runs and their stored predictions (spec §5).
# ─────────────────────────────────────────────────────────────────────────────
SCORE_KEY_HINTS = ("prob", "probs", "probability", "score", "scores",
                   "logit", "logits", "y_score")
PRED_FILE_HINTS = ("predictions.npz", "probs.npz", "preds.npz", "probs.npy")
#: Directories that hold raw data or per-window features, never model
#: predictions. Skipped so a Drive-wide scan stays minutes, not hours.
SKIP_DIR_NAMES = ("raw_ann", "incart_raw", "incart", "mitdb", "incartdb",
                  "atrial_parts", "figs", "figures", "svdb_feats",
                  "synergy_feats", "__pycache__", ".ipynb_checkpoints")


def _read_json(path: str) -> Optional[dict]:
    if not os.path.exists(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except Exception as exc:                                # pragma: no cover
        return {"_unreadable": str(exc)}


def probe_prediction_file(path: str) -> Dict[str, object]:
    """Describe one prediction file without interpreting it.

    Reports which of (scores, y_true, record id, beat key) exist, so the gate
    can tell beat-level-ready artifacts from aggregate-only ones.
    """
    info: Dict[str, object] = {"file": os.path.basename(path), "path": path,
                               "readable": False}
    try:
        if path.endswith(".npy"):
            arr = np.load(path, allow_pickle=False, mmap_mode="r")
            info.update({"readable": True, "fields": ["<array>"],
                         "n_rows": int(arr.shape[0]),
                         "score_fields": ["<array>"], "has_y_true": False,
                         "has_record": False, "beat_key_mode": KEY_MODE_NONE})
            return info
        with np.load(path, allow_pickle=True) as npz:
            files = list(npz.files)
            # Detection is by KEY, not by file name: the legacy ablation runs
            # store their probabilities in `ens.npz`, `perseed.npz`, `b.npz`…
            score_fields = [f for f in files
                            if f.lower() in LEGACY_SCORE_FIELDS
                            or any(h in f.lower() for h in SCORE_KEY_HINTS)]
            y_field = _first_key(files, LEGACY_LABEL_FIELDS + ("y_s",))
            rec_field = _first_key(files, BEAT_KEY_RECORD_FIELDS)
            samp_field = _first_key(files, BEAT_KEY_SAMPLE_FIELDS)
            sym_field = _first_key(files, BEAT_KEY_SYMBOL_FIELDS)
            n_rows = None
            if y_field:
                n_rows = int(np.asarray(npz[y_field]).shape[0])
            elif rec_field:
                n_rows = int(np.asarray(npz[rec_field]).shape[0])
            if rec_field and samp_field:
                key_mode = KEY_MODE_ANNOTATION
            elif rec_field and y_field and score_fields:
                # Recoverable, but only after the row correspondence with the
                # frozen source file has been verified element-wise.
                key_mode = KEY_MODE_SOURCE_VERIFIED
            else:
                key_mode = KEY_MODE_NONE
            layout = None
            if score_fields and n_rows:
                try:
                    layout = detect_score_layout(
                        np.asarray(npz[score_fields[0]]), n_rows)
                except Q5AError as exc:
                    layout = {"kind": "unusable", "reason": str(exc)}
            info.update({
                "readable": True, "fields": sorted(files),
                "score_fields": sorted(score_fields),
                "has_y_true": bool(y_field), "y_field": y_field,
                "has_record": bool(rec_field), "record_field": rec_field,
                "sample_field": samp_field, "symbol_field": sym_field,
                "beat_key_mode": key_mode, "n_rows": n_rows,
                "score_layout": layout,
                "has_seed_axis": bool(layout and layout["kind"] == "per_seed"),
            })
    except Exception as exc:
        info["error"] = str(exc)
    return info


def detect_score_layout(arr: np.ndarray, n_rows: int) -> Dict[str, object]:
    """Say what a stored score array actually is — never guess silently.

    ``(n,)`` per-beat score; ``(n, n_class)`` class probabilities (S column
    fixed at :data:`S_COLUMN`); ``(n_seed, n)`` a per-seed stack. Anything
    else is an error, because picking the wrong axis silently would corrupt
    every number downstream.
    """
    a = np.asarray(arr)
    if a.ndim == 1 and a.shape[0] == n_rows:
        return {"kind": "per_beat", "shape": list(a.shape)}
    if a.ndim == 2 and a.shape[0] == n_rows and a.shape[1] in LEGACY_CLASS_WIDTHS:
        return {"kind": "class_matrix", "shape": list(a.shape),
                "s_column": int(S_COLUMN), "n_class": int(a.shape[1])}
    if a.ndim == 2 and a.shape[1] == n_rows:
        return {"kind": "per_seed", "shape": list(a.shape),
                "n_seed": int(a.shape[0])}
    raise Q5AError(
        f"score array of shape {a.shape} cannot be interpreted against "
        f"{n_rows} rows — refusing to guess the axis; fix the adapter")


def _score_vector(arr: np.ndarray, layout: Dict[str, object]
                  ) -> Tuple[np.ndarray, Optional[np.ndarray]]:
    """(per-beat S score, optional per-seed matrix) from a stored array."""
    a = np.asarray(arr, float)
    if layout["kind"] == "per_beat":
        return a, None
    if layout["kind"] == "class_matrix":
        return a[:, int(layout["s_column"])], None
    return np.nanmean(a, axis=0), a


def load_frozen_source_index(source_path: str,
                             log: Optional[RunLog] = None
                             ) -> Dict[str, np.ndarray]:
    """Read the frozen source npz that the legacy runs consumed.

    Returns the arrays needed to verify a row correspondence: record id, label
    and the annotation sample index (``t``). Nothing else is touched.
    """
    log = log or RunLog()
    if not os.path.exists(source_path):
        raise Q5AError(f"frozen source not found: {source_path}")
    with np.load(source_path, allow_pickle=True) as z:
        files = list(z.files)
        rec_f = _first_key(files, BEAT_KEY_RECORD_FIELDS)
        y_f = _first_key(files, ("y5", "y", "y3", "label"))
        t_f = _first_key(files, BEAT_KEY_SAMPLE_FIELDS)
        if rec_f is None or y_f is None:
            raise Q5AError(f"{os.path.basename(source_path)} lacks record/label "
                           f"keys (has {files}) — cannot verify any adapter")
        sym_f = _first_key(files, BEAT_KEY_SYMBOL_FIELDS)
        db_f = _first_key(files, BEAT_KEY_DB_FIELDS)
        out = {"record": np.asarray(z[rec_f]).astype(int),
               "y": np.asarray(z[y_f]).astype(int)}
        out["sample"] = (np.asarray(z[t_f]).astype(np.int64) if t_f is not None
                         else None)
        # Carried so the derived key matches the atlas cohort's key exactly —
        # the cohort builds its key from the same fields of the same file.
        out["sym"] = (np.asarray(z[sym_f]).astype(str) if sym_f is not None
                      else None)
        out["db"] = (np.asarray(z[db_f]).astype(str) if db_f is not None
                     else None)
    out["sha256"] = sha256_file(source_path)          # type: ignore[assignment]
    out["path"] = source_path                          # type: ignore[assignment]
    log(f"frozen source {os.path.basename(source_path)}: "
        f"{len(out['record'])} rows, sample index "
        f"{'present' if out['sample'] is not None else 'ABSENT'}")
    return out


def verify_row_correspondence(pred_record: np.ndarray, pred_y: np.ndarray,
                              source: Dict[str, np.ndarray],
                              subsets: Optional[Dict[str, np.ndarray]] = None
                              ) -> Dict[str, object]:
    """Find WHICH rows of the frozen source a legacy artifact corresponds to.

    A candidate subset is accepted only when the record ids and the labels
    match on **every single row**. That is a verification, not the positional
    matching the spec forbids: row order alone never establishes anything
    here, and a single mismatch rejects the candidate.
    """
    rec_src, y_src = source["record"], source["y"]
    cands = subsets or {
        "ds2": np.where(np.isin(rec_src, list(DS2_RECORDS)))[0],
        "ds1": np.where(np.isin(rec_src, list(DS1_RECORDS)))[0],
        "all": np.arange(len(rec_src)),
    }
    tried = []
    for name, rows in cands.items():
        if len(rows) != len(pred_record):
            tried.append({"subset": name, "n_source": int(len(rows)),
                          "n_pred": int(len(pred_record)),
                          "verdict": "length mismatch"})
            continue
        rec_ok = bool(np.array_equal(rec_src[rows],
                                     np.asarray(pred_record).astype(int)))
        y_ok = bool(np.array_equal(y_src[rows], np.asarray(pred_y).astype(int)))
        tried.append({"subset": name, "n_source": int(len(rows)),
                      "n_pred": int(len(pred_record)),
                      "record_match": rec_ok, "label_match": y_ok,
                      "verdict": "VERIFIED" if (rec_ok and y_ok)
                      else "row values differ"})
        if rec_ok and y_ok:
            return {"verified": True, "subset": name, "rows": rows,
                    "n": int(len(rows)), "attempts": tried,
                    "rule": ("every record id and every label matches the "
                             "frozen source on this subset — row order alone "
                             "was never sufficient")}
    return {"verified": False, "subset": None, "rows": None, "attempts": tried,
            "rule": "no subset of the frozen source matches element-wise"}


def _model_name_from(cfg: Optional[dict], res: Optional[dict],
                     run_dir: str) -> str:
    for src in (cfg or {}, res or {}):
        for k in ("model", "model_name", "config_name", "variant", "arm",
                  "experiment", "name"):
            v = src.get(k)
            if isinstance(v, str) and v:
                return v
    return os.path.basename(run_dir)


def scan_inventory(roots: Sequence[str],
                   registry_path: Optional[str] = None,
                   log: Optional[RunLog] = None) -> Dict[str, object]:
    """Enumerate every candidate run under ``roots`` — read-only.

    One row per run: provenance, split, metric definition, prediction files.
    Nothing is selected here; :func:`freeze_baseline` does that, and it never
    looks at a performance number.
    """
    log = log or RunLog()
    entries: List[Dict[str, object]] = []
    seen: set = set()
    for root in roots:
        if not os.path.isdir(root):
            log(f"  root missing (recorded, not fatal): {root}")
            continue
        for name in sorted(os.listdir(root)):
            run_dir = os.path.join(root, name)
            if not os.path.isdir(run_dir) or run_dir in seen:
                continue
            seen.add(run_dir)
            cfg = _read_json(os.path.join(run_dir, "config.json"))
            res = _read_json(os.path.join(run_dir, "result.json"))
            man = _read_json(os.path.join(run_dir, "manifest.json"))
            if name in SKIP_DIR_NAMES:
                continue
            preds, tag_dirs = [], {}
            for dirpath, dirnames, filenames in os.walk(run_dir):
                dirnames[:] = [d for d in dirnames if d not in SKIP_DIR_NAMES]
                for f in sorted(filenames):
                    if not f.endswith(".npz"):
                        continue
                    p = probe_prediction_file(os.path.join(dirpath, f))
                    if not (p.get("score_fields") and p.get("has_y_true")):
                        continue
                    preds.append(p)
                    if os.path.abspath(dirpath) != os.path.abspath(run_dir):
                        tag_dirs.setdefault(dirpath, []).append(p)
            # Legacy ablation layout: <run>/<tag>/ens.npz — the TAG is the
            # model identity (`run_final("pwave")`), so it gets its own row.
            for tdir, tpreds in sorted(tag_dirs.items()):
                tag = os.path.basename(tdir)
                entries.append(_inventory_row(
                    run_id=f"{name}/{tag}", run_dir=tdir, model_name=tag,
                    cfg=cfg, res=res, man=man, preds=tpreds,
                    parent_run_dir=run_dir))
            entries.append(_inventory_row(
                run_id=name, run_dir=run_dir,
                model_name=_model_name_from(cfg, res, run_dir),
                cfg=cfg, res=res, man=man, preds=preds, parent_run_dir=None))
    registry = None
    if registry_path and os.path.exists(registry_path):
        registry = _read_registry(registry_path)
    inv = {
        "experiment_id": EXPERIMENT_ID, "arm_id": ARM_ID,
        "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "roots": list(roots), "n_candidates": len(entries),
        "entries": entries, "registry": registry,
        "note": ("Inventory is descriptive. Selection happens in "
                 "baseline_freeze and never uses a performance number."),
    }
    log(f"inventory: {len(entries)} candidate run(s), "
        f"{sum(1 for e in entries if e['beat_level_ready'])} beat-level ready")
    return inv


def _inventory_row(run_id: str, run_dir: str, model_name: str,
                   cfg: Optional[dict], res: Optional[dict],
                   man: Optional[dict], preds: List[Dict[str, object]],
                   parent_run_dir: Optional[str]) -> Dict[str, object]:
    """One descriptive inventory row. No selection, no performance judgement."""
    beat_ready = [p for p in preds
                  if p.get("beat_key_mode") in (KEY_MODE_ANNOTATION,
                                                KEY_MODE_SOURCE_VERIFIED)]
    data = (man or {}).get("data")
    return {
        "run_id": run_id, "run_dir": run_dir, "model_name": model_name,
        "parent_run_dir": parent_run_dir,
        "experiment_id": (res or {}).get("experiment_id")
        or (cfg or {}).get("experiment_id"),
        "git_sha": (man or {}).get("git_commit_sha"),
        "data_sha": data.get("sha256") if isinstance(data, dict) else None,
        "data_file": data.get("file_name") if isinstance(data, dict) else None,
        "split": (res or {}).get("split") or (cfg or {}).get("split"),
        "metric_definition": (res or {}).get("primary_metric")
        or (cfg or {}).get("primary_metric"),
        "s_index": (cfg or {}).get("s_index", S_INDEX),
        "seeds": (cfg or {}).get("seeds") or (res or {}).get("seeds"),
        "folds": (cfg or {}).get("folds"),
        "run_timestamp": (res or {}).get("timestamp_utc"),
        "recorded_s_prauc": _recorded_s_prauc(res),
        "prediction_files": preds,
        "beat_level_ready": bool(beat_ready),
        "beat_key_modes": sorted({str(p.get("beat_key_mode")) for p in preds}),
        "needs_source_verification": bool(
            beat_ready and all(p.get("beat_key_mode") == KEY_MODE_SOURCE_VERIFIED
                               for p in beat_ready)),
        "has_config": cfg is not None, "has_result": res is not None,
        "has_manifest": man is not None,
    }


def _recorded_s_prauc(res: Optional[dict]) -> Optional[float]:
    if not res:
        return None
    for k in ("s_prauc", "S_PRAUC", "record_macro_s_prauc", "primary_value",
              "value"):
        v = res.get(k)
        if isinstance(v, (int, float)):
            return float(v)
    return None


def _read_registry(path: str) -> Dict[str, object]:
    rows, bad = [], 0
    with open(path, "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except Exception:
                bad += 1
    ids = [r.get("run_id") for r in rows if isinstance(r, dict)]
    dup = sorted({i for i in ids if ids.count(i) > 1 and i})
    return {"path": path, "n_rows": len(rows), "n_unparsable": bad,
            "duplicate_run_ids": dup,
            "append_only_ok": bool(not dup and not bad)}


def freeze_baseline(inventory: Dict[str, object],
                    targets: Optional[Dict[str, Dict[str, object]]] = None
                    ) -> Dict[str, object]:
    """Pick the V9/V10 runs by provenance only (spec §5).

    Hard rules, all pre-registered:
    * a candidate matches a target only through its recorded model name;
    * two indistinguishable candidates -> ``AMBIGUOUS_BASELINE`` (STOP);
    * differing split / metric definition / S index -> ``INCOMPATIBLE_BASELINES``;
    * a performance number is NEVER a tie-breaker — the recorded S PR-AUC is
      carried along only so the analysis can *check* it later.
    """
    targets = targets or BASELINE_TARGETS
    entries = list(inventory.get("entries", []))
    selected: Dict[str, object] = {}
    reasons: List[str] = []
    absent: List[Dict[str, object]] = []
    # primary first, so a paired control can be scoped to the primary's run
    order = sorted(targets, key=lambda k: (targets[k].get("role") != ROLE_PRIMARY,
                                           k))
    for label in order:
        tgt = targets[label]
        role = str(tgt.get("role", ROLE_PRIMARY))
        toks = tuple(t.lower() for t in tgt["name_tokens"])
        cands = [e for e in entries
                 if any(t in str(e.get("model_name", "")).lower() for t in toks)
                 or any(t in str(e.get("run_id", "")).lower() for t in toks)]
        if role == ROLE_CONTROL and tgt.get("same_parent_as") in selected:
            # A control name like "base26" repeats across unrelated ablation
            # runs. Scope it to the primary's own run — a provenance rule, not
            # a performance one.
            prim = selected[str(tgt["same_parent_as"])]
            parent = prim.get("parent_run_dir") or os.path.dirname(
                str(prim.get("run_dir", "")))
            same = [c for c in cands
                    if (c.get("parent_run_dir") or os.path.dirname(
                        str(c.get("run_dir", "")))) == parent]
            if same:
                cands = same
                reasons.append(
                    f"{label}: scoped to the parent run of "
                    f"{tgt['same_parent_as']} ({os.path.basename(str(parent))})"
                    " — same script and seeds, so the pair is comparable")
        if not cands:
            note = str(tgt.get("note", ""))
            absent.append({"label": label, "role": role,
                           "name_tokens": list(tgt["name_tokens"]),
                           "recorded_s_prauc_claim": tgt.get("recorded_s_prauc"),
                           "recorded_in": tgt.get("recorded_in"),
                           "status": "ARTIFACT_ABSENT",
                           "consequence": (
                               "the recorded claim stays UNVERIFIED; Q5-A does "
                               "not retrain a model to fill the gap"),
                           "note": note})
            reasons.append(f"{label} ({role}): no candidate run matches "
                           f"{tgt['name_tokens']} — ARTIFACT_ABSENT")
            continue
        if len(cands) > 1:
            # Provenance-only disambiguation: prefer an exact model-name match.
            exact = [c for c in cands
                     if str(c.get("model_name", "")).lower() in toks]
            if len(exact) == 1:
                cands = exact
            else:
                reasons.append(
                    f"{label}: {len(cands)} indistinguishable candidates "
                    f"{[c['run_id'] for c in cands]} — AMBIGUOUS_BASELINE "
                    "(selection by performance is forbidden)")
                continue
        c = cands[0]
        selected[label] = {
            "run_id": c["run_id"], "run_dir": c["run_dir"],
            "model_name": c["model_name"], "git_sha": c.get("git_sha"),
            "data_sha": c.get("data_sha"), "split": c.get("split"),
            "metric_definition": c.get("metric_definition"),
            "s_index": c.get("s_index"), "seeds": c.get("seeds"),
            "beat_level_ready": bool(c.get("beat_level_ready")),
            "recorded_s_prauc_claim": tgt.get("recorded_s_prauc"),
            "run_recorded_s_prauc": c.get("recorded_s_prauc"),
            "role": role, "parent_run_dir": c.get("parent_run_dir"),
            "needs_source_verification": bool(c.get("needs_source_verification")),
            "source_script": tgt.get("source_script"),
            "comparison_role": ("beat_level" if c.get("beat_level_ready")
                                else "aggregate_only"),
        }
    status = "FROZEN"
    missing_primary = [a for a in absent if a["role"] == ROLE_PRIMARY]
    if any("AMBIGUOUS_BASELINE" in r for r in reasons):
        status = "AMBIGUOUS_BASELINE"
    elif missing_primary:
        status = "MISSING_BASELINE"
    elif absent:
        # A historical baseline recorded in prose but never saved is a RESULT,
        # not a blocker: the claim is reported as unverified and the analysis
        # continues with the artifacts that do exist (spec Decision log
        # 2026-08-09). Retraining to fill the gap stays forbidden.
        status = "FROZEN_WITH_ABSENT_BASELINE"
    if len(selected) >= 2:
        keys = ("split", "metric_definition", "s_index")
        base = None
        for label, s in selected.items():
            sig = tuple(json.dumps(s.get(k), sort_keys=True, default=str)
                        for k in keys)
            if base is None:
                base = (label, sig)
            elif sig != base[1]:
                status = "INCOMPATIBLE_BASELINES"
                reasons.append(
                    f"{label} and {base[0]} differ in {keys}: direct "
                    "comparison would not be like-for-like (spec §5)")
    freeze = {
        "status": status, "selected": selected, "reasons": reasons,
        "absent_baselines": absent,
        "beat_level_models": sorted(k for k, v in selected.items()
                                    if v["comparison_role"] == "beat_level"),
        "aggregate_only_models": sorted(k for k, v in selected.items()
                                        if v["comparison_role"] != "beat_level"),
        "selection_rule": ("provenance only — model name, git SHA, data SHA, "
                           "split and metric definition. DS2 performance is "
                           "never used to choose between candidates."),
        "retraining": "forbidden — a model without artifacts stays out",
    }
    return freeze


def evaluate_artifact_gates(inventory: Dict[str, object],
                            freeze: Dict[str, object],
                            matching: Optional[Dict[str, object]] = None
                            ) -> Dict[str, object]:
    """D0 of the decision tree: can the atlas be computed at all? (spec §10)."""
    stops: List[str] = []
    branch: Optional[str] = None
    if freeze["status"] not in ("FROZEN", "FROZEN_WITH_ABSENT_BASELINE"):
        stops.append(f"baseline freeze status = {freeze['status']}: "
                     + "; ".join(freeze["reasons"]) or freeze["status"])
        branch = BRANCH_INSUFFICIENT
    if not freeze.get("beat_level_models"):
        stops.append("no baseline exposes beat-level predictions with a stable "
                     "key — beat-level failure mapping is impossible")
        branch = branch or BRANCH_INSUFFICIENT
    if matching is not None and not matching.get("pass", False):
        stops.extend(matching.get("fail_reasons", ["matching gate failed"]))
        branch = BRANCH_DATA_BLOCKED
    return {"pass": not stops, "stops": stops, "branch": branch,
            "checked": {"freeze_status": freeze["status"],
                        "n_candidates": inventory.get("n_candidates"),
                        "matching_pass": None if matching is None
                        else bool(matching.get("pass"))}}


# ─────────────────────────────────────────────────────────────────────────────
# Beat matching and the integrity audit (spec §6).
# ─────────────────────────────────────────────────────────────────────────────
@dataclass
class ModelPredictions:
    """Stored scores for one model, already keyed by a stable beat key."""

    label: str
    key: np.ndarray
    score: np.ndarray              # (n,) probability in [0,1]
    y_true: np.ndarray             # (n,) bool
    record: np.ndarray             # (n,) int
    score_kind: str = "probability"
    per_seed: Optional[np.ndarray] = None    # (n_seed, n) probabilities
    source_dir: Optional[str] = None
    fingerprint: Dict[str, str] = field(default_factory=dict)
    key_mode: str = KEY_MODE_ANNOTATION
    verification: Dict[str, object] = field(default_factory=dict)


def _sigmoid(x: np.ndarray) -> np.ndarray:
    x = np.asarray(x, float)
    return 1.0 / (1.0 + np.exp(-np.clip(x, -60, 60)))


def find_prediction_file(run_dir: str) -> Optional[str]:
    """The one prediction file in a run dir, found by CONTENT, not by name."""
    for cand in PRED_FILE_HINTS:
        p = os.path.join(run_dir, cand)
        if os.path.exists(p):
            return p
    hits = []
    for f in sorted(os.listdir(run_dir)) if os.path.isdir(run_dir) else []:
        p = os.path.join(run_dir, f)
        if os.path.isfile(p) and f.endswith(".npz"):
            probe = probe_prediction_file(p)
            if probe.get("score_fields") and probe.get("has_y_true"):
                hits.append(p)
    if len(hits) > 1:
        raise Q5AError(f"{run_dir} holds {len(hits)} prediction files "
                       f"{[os.path.basename(h) for h in hits]} — ambiguous, "
                       "name the one to use explicitly")
    return hits[0] if hits else None


def load_model_predictions(run_dir: str, label: str,
                           score_field: Optional[str] = None,
                           source_index: Optional[Dict[str, np.ndarray]] = None,
                           log: Optional[RunLog] = None) -> ModelPredictions:
    """Read one stored prediction bundle read-only, with a stable key.

    Two artifact layouts are supported:

    * modern bundles that carry their own annotation index -> key straight away;
    * legacy ablation bundles (``prob``/``y``/``pid``, no index) -> the row
      correspondence with the frozen source file is VERIFIED element-wise
      (``source_index``), and only then does the source's annotation sample
      index become the key. A single mismatching row is a STOP.

    Nothing is recomputed and nothing is written.
    """
    log = log or RunLog()
    pred_path = find_prediction_file(run_dir)
    if pred_path is None:
        raise Q5AError(f"no prediction file in {run_dir} — aggregate-only "
                       "artifact; retraining is forbidden")
    probe = probe_prediction_file(pred_path)
    with np.load(pred_path, allow_pickle=True) as npz:
        files = list(npz.files)
        sf = score_field or (probe.get("score_fields") or [None])[0]
        if sf is None or sf not in files:
            raise Q5AError(f"{pred_path} has no score field among {files}")
        raw = np.asarray(npz[sf], float)
        y_field = probe.get("y_field")
        if not y_field:
            raise Q5AError(f"{pred_path} has no y_true — cannot audit failures")
        y_raw = np.asarray(npz[y_field]).astype(int)
        rec_f = _first_key(files, BEAT_KEY_RECORD_FIELDS)
        if rec_f is None:
            raise Q5AError(f"{pred_path} has no record field — beat-level "
                           "comparison is impossible (aggregate only)")
        rec = np.asarray(npz[rec_f]).astype(int)
        layout = detect_score_layout(raw, len(y_raw))
        score, per_seed = _score_vector(raw, layout)
        has_index = probe.get("beat_key_mode") == KEY_MODE_ANNOTATION
        if has_index:
            fields = {f: np.asarray(npz[f]) for f in files
                      if f.lower() in set(BEAT_KEY_RECORD_FIELDS
                                          + BEAT_KEY_SAMPLE_FIELDS
                                          + BEAT_KEY_SYMBOL_FIELDS
                                          + BEAT_KEY_DB_FIELDS)}
            keys, key_mode, _prov = build_beat_keys(fields, beat=None,
                                                    allow_fingerprint=False)
            verification = {"needed": False}
        else:
            if source_index is None:
                raise Q5AError(
                    f"{os.path.basename(pred_path)} carries no annotation index "
                    "and no frozen source was supplied — beat-level matching "
                    "would have to fall back to row order, which is forbidden. "
                    "Pass the frozen source npz (--source) so the "
                    "correspondence can be verified.")
            verification = verify_row_correspondence(rec, y_raw, source_index)
            if not verification["verified"]:
                raise Q5AError(
                    f"{label}: no subset of "
                    f"{os.path.basename(str(source_index.get('path')))} matches "
                    f"this artifact element-wise: {verification['attempts']} — "
                    "STOP (the rows cannot be identified without guessing)")
            if source_index.get("sample") is None:
                raise Q5AError(
                    "the frozen source has no annotation sample index (`t`), "
                    "so no stable beat key can be derived — aggregate only")
            rows = verification["rows"]
            samples = np.asarray(source_index["sample"])[rows]
            syms = (np.asarray(source_index["sym"])[rows]
                    if source_index.get("sym") is not None
                    else np.full(len(rows), "?"))
            dbs = (np.asarray(source_index["db"])[rows]
                   if source_index.get("db") is not None
                   else np.full(len(rows), "mitdb"))
            keys = np.array([f"{d}|{r}|{s}|{y}" for d, r, s, y
                             in zip(dbs, rec, samples, syms)])
            key_mode = KEY_MODE_SOURCE_VERIFIED
            log(f"{label}: row correspondence VERIFIED against the frozen "
                f"source ({verification['subset']}, {verification['n']} rows, "
                "record ids and labels equal on every row)")
    y = y_raw == S_INDEX if y_raw.max() > 1 else y_raw.astype(bool)
    kind = "probability"
    if "logit" in sf.lower():
        kind = "logit->probability"
        score = _sigmoid(score)
        if per_seed is not None:
            per_seed = _sigmoid(per_seed)
    elif np.nanmin(score) < 0.0 or np.nanmax(score) > 1.0:
        raise Q5AError(
            f"{sf} is named like a probability but ranges "
            f"[{np.nanmin(score):.3f},{np.nanmax(score):.3f}] — refuse to "
            "guess the scale; fix the artifact adapter")
    log(f"{label}: {len(score)} scores from {os.path.basename(pred_path)} "
        f"({kind}, layout {layout['kind']}, key mode {key_mode})")
    return ModelPredictions(
        label=label, key=keys, score=score, y_true=y, record=rec,
        score_kind=kind, per_seed=per_seed, source_dir=run_dir,
        fingerprint={os.path.basename(pred_path): sha256_file(pred_path)},
        key_mode=key_mode,
        verification={k: v for k, v in verification.items() if k != "rows"})


def match_beat_keys(cohort: AtlasCohort, model: ModelPredictions,
                    strict: bool = True) -> Dict[str, object]:
    """Match a model's beats to the atlas cohort on the stable key only.

    Hard stops (spec §6): any label conflict on a shared key, unexplained
    duplicate keys, unexplained S-beat mismatch. Row order is never used.
    """
    assert_not_positional(model.key)
    left = {str(k): i for i, k in enumerate(cohort.key)}
    dup_right = _duplicate_keys(model.key)
    matched_left, matched_right = [], []
    for j, k in enumerate(model.key):
        i = left.get(str(k))
        if i is not None:
            matched_left.append(i)
            matched_right.append(j)
    ml = np.asarray(matched_left, int)
    mr = np.asarray(matched_right, int)
    conflicts = []
    if len(ml):
        bad = np.where(cohort.y_s[ml] != model.y_true[mr])[0]
        for b in bad[:50]:
            conflicts.append({"key": str(cohort.key[ml[b]]),
                              "record": int(cohort.record[ml[b]]),
                              "atlas_y_s": bool(cohort.y_s[ml[b]]),
                              "model_y_true": bool(model.y_true[mr[b]])})
    unmatched_left = int(cohort.n - len(ml))
    unmatched_right = int(len(model.key) - len(mr))
    s_left = int(cohort.y_s.sum())
    s_right = int(np.asarray(model.y_true).sum())
    s_matched = int(cohort.y_s[ml].sum()) if len(ml) else 0
    # A model may legitimately cover only part of the cohort — the legacy
    # ablation artifacts score DS2 only. Mismatch is judged INSIDE the model's
    # own record scope; records it never claims are reported as not covered,
    # not as missing beats.
    scope = set(int(r) for r in np.unique(model.record)) if len(model.record) \
        else set()
    per_record = []
    for r in cohort.records:
        idx = cohort.idx_of[int(r)]
        in_match = np.isin(idx, ml)
        rows_r = mr[np.isin(ml, idx)] if len(ml) else np.zeros(0, int)
        per_record.append({
            "record": int(r), "in_model_scope": bool(int(r) in scope),
            "n_atlas": int(len(idx)),
            "n_matched": int(in_match.sum()),
            "n_unmatched_atlas": int((~in_match).sum()),
            "s_atlas": int(cohort.y_s[idx].sum()),
            "s_matched": int(cohort.y_s[idx][in_match].sum()),
            "s_model": int(model.y_true[rows_r].sum()) if len(rows_r) else 0,
            "class_counts_atlas": [int((cohort.y5[idx] == c).sum())
                                   for c in range(5)],
        })
    in_scope = [p for p in per_record if p["in_model_scope"]]
    s_mismatch = sum(abs(p["s_atlas"] - p["s_matched"]) for p in in_scope)
    unmatched_left = int(sum(p["n_unmatched_atlas"] for p in in_scope))
    fail_reasons: List[str] = []
    if conflicts:
        fail_reasons.append(
            f"{len(conflicts)} label conflict(s) on identical keys "
            f"(e.g. {conflicts[0]}) — HARD STOP (spec §6)")
    if dup_right:
        fail_reasons.append(
            f"{len(dup_right)} duplicate key(s) in {model.label} "
            f"(e.g. {dup_right[:3]}) — must be explained, not silently resolved")
    if s_mismatch:
        fail_reasons.append(
            f"{s_mismatch} S beat(s) inside {model.label}'s own record scope "
            "have no counterpart — unexplained S mismatch, HARD STOP")
    if not len(ml):
        fail_reasons.append(f"{model.label} shares no beat key with the atlas "
                            "source — different preprocessing or key scheme")
    audit = {
        "model": model.label, "key_mode": cohort.key_mode,
        "model_key_mode": model.key_mode,
        "source_row_verification": model.verification or {"needed": False},
        "matched": int(len(ml)),
        "model_record_scope": sorted(scope),
        "records_not_covered": [int(r) for r in cohort.records
                                if int(r) not in scope],
        "unmatched_atlas_in_scope": unmatched_left,
        "unmatched_atlas": unmatched_left, "unmatched_model": unmatched_right,
        "duplicate_keys_model": dup_right[:20],
        "n_duplicate_keys_model": len(dup_right),
        "label_conflicts": conflicts, "n_label_conflicts": len(conflicts),
        "s_atlas": s_left, "s_model": s_right, "s_matched": s_matched,
        "s_mismatch": int(s_mismatch),
        "per_record": per_record,
        "audit_records": {str(r): next(p for p in per_record
                                       if p["record"] == r)
                          for r in AUDIT_RECORDS
                          if any(p["record"] == r for p in per_record)},
        "fail_reasons": fail_reasons,
        "pass": not fail_reasons,
        "positional_matching_used": False,
    }
    if fail_reasons and strict:
        raise Q5AError("beat matching gate FAILED for "
                       f"{model.label}: " + " | ".join(fail_reasons))
    return audit


def record_audit_208_213(cohort: AtlasCohort,
                         matches: Dict[str, Dict[str, object]]
                         ) -> List[Dict[str, object]]:
    """Dedicated audit table for the two records with measured beat deficits."""
    rows = []
    for r in AUDIT_RECORDS:
        if int(r) not in cohort.idx_of:
            rows.append({"record": int(r), "present_in_atlas": False})
            continue
        idx = cohort.idx_of[int(r)]
        row: Dict[str, object] = {
            "record": int(r), "present_in_atlas": True,
            "n_atlas": int(len(idx)), "s_atlas": int(cohort.y_s[idx].sum()),
            "class_counts_atlas": {CLASS_NAMES[c]: int((cohort.y5[idx] == c).sum())
                                   for c in range(5)},
            "symbols_atlas": {str(s): int((cohort.sym[idx] == s).sum())
                              for s in sorted(set(cohort.sym[idx].tolist()))},
            "known_deficit": ("Q4-Q PREP_DATA measured mamba preprocessing "
                              "removing ~12.7% (208) / ~11.1% (213) more beats "
                              "than ecg_multi on these two noisy records"),
        }
        for label, m in matches.items():
            per = {p["record"]: p for p in m["per_record"]}
            if int(r) in per:
                p = per[int(r)]
                row[f"{label}_matched"] = p["n_matched"]
                row[f"{label}_unmatched_atlas"] = p["n_unmatched_atlas"]
                row[f"{label}_s_matched"] = p["s_matched"]
                row[f"{label}_removed_frac"] = (
                    float(p["n_unmatched_atlas"]) / max(1, p["n_atlas"]))
        rows.append(row)
    return rows


# ─────────────────────────────────────────────────────────────────────────────
# Metrics. All CIs are patient(record)-level; beat bootstrap is never used to
# hide a small patient count (spec §7).
# ─────────────────────────────────────────────────────────────────────────────
def beat_micro_prauc(y: np.ndarray, score: np.ndarray) -> float:
    from sklearn.metrics import average_precision_score
    y = np.asarray(y, bool)
    if y.sum() == 0 or y.sum() == len(y):
        raise Q5AError("beat-micro PR-AUC undefined: one class only")
    return float(average_precision_score(y, np.asarray(score, float)))


def per_record_prauc(y: np.ndarray, score: np.ndarray, record: np.ndarray,
                     records: Sequence[int]) -> Dict[int, float]:
    """Per-record S PR-AUC. Records without S are EXCLUDED and reported."""
    from sklearn.metrics import average_precision_score
    out: Dict[int, float] = {}
    for r in records:
        idx = np.where(record == int(r))[0]
        yy = np.asarray(y[idx], bool)
        if 0 < int(yy.sum()) < len(yy):
            out[int(r)] = float(average_precision_score(yy, score[idx]))
    return out


def record_inclusion_report(y: np.ndarray, record: np.ndarray,
                            records: Sequence[int]) -> Dict[str, object]:
    excluded = []
    for r in records:
        idx = np.where(record == int(r))[0]
        n_s = int(np.asarray(y[idx], bool).sum())
        if n_s == 0:
            excluded.append({"record": int(r), "reason": "no S beat",
                             "n_beat": int(len(idx))})
        elif n_s == len(idx):
            excluded.append({"record": int(r), "reason": "S only",
                             "n_beat": int(len(idx))})
    return {"n_records_total": len(list(records)),
            "n_records_with_s": len(list(records)) - len(excluded),
            "excluded_records": excluded}


def boot_ci(by_record: Dict[int, float], n_boot: int = NB_BOOT,
            seed: int = SEED0) -> Dict[str, float]:
    """Patient(record)-level bootstrap of a mean — Q4-O's implementation."""
    return paired_record_bootstrap({int(k): float(v)
                                    for k, v in by_record.items()},
                                   n_boot=n_boot, seed=seed)


def patient_summary(by_record: Dict[int, float]) -> Dict[str, object]:
    vals = np.array([by_record[r] for r in sorted(by_record)], float)
    order = sorted(by_record, key=lambda r: by_record[r])
    return {"n_record": int(len(vals)), "mean": float(vals.mean()),
            "median": float(np.median(vals)),
            "p10": float(np.percentile(vals, 10)),
            "p25": float(np.percentile(vals, 25)),
            "worst5": [{"record": int(r), "value": float(by_record[r])}
                       for r in order[:5]]}


def brier_and_calibration(y: np.ndarray, prob: np.ndarray,
                          n_bins: int = CALIBRATION_BINS) -> Dict[str, object]:
    y = np.asarray(y, bool).astype(float)
    p = np.clip(np.asarray(prob, float), 0.0, 1.0)
    brier = float(np.mean((p - y) ** 2))
    edges = np.linspace(0.0, 1.0, n_bins + 1)
    idx = np.clip(np.digitize(p, edges[1:-1]), 0, n_bins - 1)
    ece, bins = 0.0, []
    for b in range(n_bins):
        m = idx == b
        if not m.any():
            continue
        conf, acc = float(p[m].mean()), float(y[m].mean())
        w = float(m.mean())
        ece += w * abs(conf - acc)
        bins.append({"bin": b, "n": int(m.sum()), "mean_prob": conf,
                     "observed_rate": acc})
    return {"brier": brier, "ece": float(ece), "bins": bins}


def ds1_locked_threshold(model: ModelPredictions, split: Dict[str, List[int]],
                         stored_threshold: Optional[float] = None,
                         ds1_prevalence: Optional[float] = None
                         ) -> Dict[str, object]:
    """A threshold that never sees a DS2 label (spec §7).

    1. a stored pre-specified threshold wins;
    2. else, if the artifact carries DS1 rows, maximise F1 on DS1 only;
    3. else, take the DS1 S prevalence and read the matching quantile off the
       DS2 *score* distribution — DS2 labels are still untouched.
    """
    if stored_threshold is not None:
        return {"threshold": float(stored_threshold),
                "source": "stored_prespecified", "uses_ds2_labels": False}
    in_ds1 = np.isin(model.record, list(split["ds1"]))
    if in_ds1.any() and np.asarray(model.y_true)[in_ds1].sum() > 0:
        s, y = model.score[in_ds1], np.asarray(model.y_true)[in_ds1]
        cand = np.unique(np.round(s, 4))
        if len(cand) > 512:
            cand = np.quantile(s, np.linspace(0, 1, 512))
        best, best_f1 = float(cand[0]), -1.0
        for t in cand:
            pred = s >= t
            tp = float((pred & y).sum())
            if tp == 0:
                continue
            prec, rec = tp / max(1.0, pred.sum()), tp / max(1.0, y.sum())
            f1 = 2 * prec * rec / max(1e-12, prec + rec)
            if f1 > best_f1:
                best, best_f1 = float(t), f1
        return {"threshold": best, "source": "ds1_labels_f1",
                "ds1_f1": float(best_f1), "uses_ds2_labels": False}
    if ds1_prevalence is not None:
        prev = float(ds1_prevalence)          # from DS1 annotations only
    elif in_ds1.any():
        prev = float(np.asarray(model.y_true)[in_ds1].mean())
    else:
        raise Q5AError(
            "no DS1 rows in this artifact and no DS1 prevalence supplied — "
            "deriving a threshold from DS2 labels is forbidden (spec §7)")
    ds2 = np.isin(model.record, list(split["ds2"]))
    pool = model.score[ds2] if ds2.any() else model.score
    thr = float(np.quantile(pool, 1.0 - min(max(prev, 1e-4), 0.5)))
    return {"threshold": thr, "source": "ds1_prevalence_quantile",
            "ds1_prevalence": prev, "uses_ds2_labels": False,
            "note": ("fallback: the quantile is read off the DS2 SCORE "
                     "distribution; no DS2 label is consulted")}


def threshold_metrics(y: np.ndarray, score: np.ndarray,
                      threshold: float) -> Dict[str, float]:
    y = np.asarray(y, bool)
    pred = np.asarray(score, float) >= float(threshold)
    tp = float((pred & y).sum())
    fp = float((pred & ~y).sum())
    fn = float((~pred & y).sum())
    prec = tp / (tp + fp) if tp + fp else 0.0
    rec = tp / (tp + fn) if tp + fn else 0.0
    return {"tp": tp, "fp": fp, "fn": fn,
            "s_recall": rec, "s_precision": prec,
            "s_f1": (2 * prec * rec / (prec + rec)) if prec + rec else 0.0}


def model_metrics(model: ModelPredictions, cohort: AtlasCohort,
                  split: Dict[str, List[int]], rows: np.ndarray,
                  n_boot: int = NB_BOOT,
                  ds1_prevalence: Optional[float] = None) -> Dict[str, object]:
    """Recompute every headline number for one model with identical code."""
    y = cohort.y_s[rows]
    score = model.score
    rec = cohort.record[rows]
    ds2 = [r for r in split["ds2"] if r in set(rec.tolist())]
    per_rec = per_record_prauc(y, score, rec, ds2)
    if not per_rec:
        raise Q5AError(f"{model.label}: no DS2 record has both classes")
    thr = ds1_locked_threshold(model, split, ds1_prevalence=ds1_prevalence)
    tm = threshold_metrics(y, score, thr["threshold"])
    cal = brier_and_calibration(y, score)
    seed_var = None
    if model.per_seed is not None and len(model.per_seed) > 1:
        seed_vals = []
        for s_i in range(len(model.per_seed)):
            pr = per_record_prauc(y, model.per_seed[s_i], rec, ds2)
            seed_vals.append(float(np.mean(list(pr.values()))))
        seed_var = {"by_seed": seed_vals, "std": float(np.std(seed_vals)),
                    "n_seed": int(len(seed_vals))}
    return {
        "model": model.label,
        "beat_micro_s_prauc": beat_micro_prauc(y, score),
        "record_macro_s_prauc": float(np.mean(list(per_rec.values()))),
        "record_macro_ci": boot_ci(per_rec, n_boot=n_boot),
        "per_record_s_prauc": {str(k): v for k, v in per_rec.items()},
        "patient_summary": patient_summary(per_rec),
        "threshold": thr, "threshold_metrics": tm,
        "calibration": {k: v for k, v in cal.items() if k != "bins"},
        "calibration_bins": cal["bins"],
        "seed_variability": seed_var,
        "inclusion": record_inclusion_report(y, rec, ds2),
        "score_kind": model.score_kind,
        "source_dir": model.source_dir,
    }


def baseline_claim_check(metrics: Dict[str, Dict[str, object]],
                         freeze: Dict[str, object]) -> List[Dict[str, object]]:
    """Compare the recorded 0.597 / 0.660 claims with the recomputed numbers."""
    rows = []
    for label, sel in freeze.get("selected", {}).items():
        m = metrics.get(label)
        claim = sel.get("recorded_s_prauc_claim")
        if claim is None:
            rows.append({"model": label, "recorded_claim": None,
                         "recomputed_beat_micro": (m or {}).get(
                             "beat_micro_s_prauc"),
                         "recomputed_record_macro": (m or {}).get(
                             "record_macro_s_prauc"),
                         "closest_unit": None, "abs_gap": None,
                         "verdict": ("no recorded claim to check — reported "
                                     f"as measured ({sel.get('role')})")})
            continue
        if m is None:
            rows.append({"model": label, "recorded_claim": claim,
                         "recomputed_beat_micro": None,
                         "recomputed_record_macro": None,
                         "verdict": "NOT_RECOMPUTED (no beat-level artifact)"})
            continue
        micro = m["beat_micro_s_prauc"]
        macro = m["record_macro_s_prauc"]
        best, unit = min(((abs(micro - claim), "beat_micro"),
                          (abs(macro - claim), "record_macro")))\
            if claim is not None else (None, None)
        rows.append({
            "model": label, "recorded_claim": claim,
            "recomputed_beat_micro": micro, "recomputed_record_macro": macro,
            "closest_unit": unit, "abs_gap": best,
            "verdict": ("consistent with the recorded claim under the "
                        f"{unit} definition" if best is not None and best <= 0.02
                        else "NOT reproduced by either metric unit — the "
                             "recorded value stays unverified"),
        })
    return rows


# ─────────────────────────────────────────────────────────────────────────────
# Failure maps: subtype, RR/timing, atrial proxies, quality (spec §8).
# ─────────────────────────────────────────────────────────────────────────────
def rank_fraction(score: np.ndarray, values: np.ndarray,
                  inclusive: bool = False) -> np.ndarray:
    """Fraction of ``score`` below (or at most) each of ``values``.

    Vectorised equivalent of ``[(score < v).mean() for v in values]`` — the
    loop form is O(n_S x n) and costs minutes on a full DS2 cohort.
    """
    s = np.sort(np.asarray(score, float), kind="mergesort")
    side = "right" if inclusive else "left"
    return np.searchsorted(s, np.asarray(values, float),
                           side=side) / max(1, len(s))


def subtype_of(sym: np.ndarray) -> np.ndarray:
    out = np.full(len(sym), "other", dtype="<U6")
    for s in S_SUBTYPES:
        out[np.asarray(sym) == s] = s
    return out


def subtype_metrics(cohort: AtlasCohort, rows: np.ndarray,
                    models: Dict[str, ModelPredictions],
                    ref_label: str, threshold: float) -> List[Dict[str, object]]:
    sub = subtype_of(cohort.sym[rows])
    y = cohort.y_s[rows]
    score = models[ref_label].score
    out = []
    for name in S_SUBTYPES + ("other",):
        m = (sub == name) & y
        n = int(m.sum())
        row = {"subtype": name, "n": n,
               "descriptive_only": bool(n < SUBTYPE_MIN_N)}
        if n:
            row.update({
                "mean_score": float(np.mean(score[m])),
                "median_score": float(np.median(score[m])),
                "fn_rate": float(np.mean(score[m] < threshold)),
                "mean_rank_pct": float(np.mean(
                    rank_fraction(score, score[m], inclusive=True))),
            })
        out.append(row)
    return out


def rr_features(cohort: AtlasCohort, rows: np.ndarray,
                window: int = 21) -> Dict[str, np.ndarray]:
    """pre/post RR, a local median RR, coupling ratio and pause proxies."""
    pre = cohort.pre_rr[rows]
    post = cohort.post_rr[rows]
    rec = cohort.record[rows]
    local = np.full(len(rows), np.nan)
    for r in np.unique(rec):
        idx = np.where(rec == r)[0]
        vals = pre[idx]
        half = max(1, window // 2)
        for j in range(len(idx)):
            lo, hi = max(0, j - half), min(len(idx), j + half + 1)
            w = vals[lo:hi]
            w = w[np.isfinite(w)]
            if len(w):
                local[idx[j]] = float(np.median(w))
    with np.errstate(invalid="ignore", divide="ignore"):
        coupling = pre / local
        pause = post / local
    edge = ~np.isfinite(pre) | ~np.isfinite(post)
    transition = np.abs(np.nan_to_num(coupling, nan=1.0) - 1.0) > 0.20
    return {"pre_rr": pre, "post_rr": post, "local_median_rr": local,
            "coupling_ratio": coupling, "compensatory_pause_ratio": pause,
            "rr_edge_flag": edge.astype(float),
            "rhythm_transition_flag": transition.astype(float)}


def ds1_quantile_bins(values_ds1: np.ndarray, n_bins: int = 4) -> List[float]:
    """Bin edges from DS1 only; applied unchanged to DS2 (spec §7)."""
    v = np.asarray(values_ds1, float)
    v = v[np.isfinite(v)]
    if len(v) < n_bins:
        raise Q5AError("not enough finite DS1 values to define bins")
    qs = np.linspace(0, 100, n_bins + 1)
    edges = [float(x) for x in np.percentile(v, qs)]
    edges[0], edges[-1] = -np.inf, np.inf
    return edges


def apply_bins(values: np.ndarray, edges: Sequence[float]) -> np.ndarray:
    return np.digitize(np.nan_to_num(np.asarray(values, float), nan=-np.inf),
                       np.asarray(edges[1:-1], float))


def binned_failure_table(name: str, values: np.ndarray, edges: Sequence[float],
                         y: np.ndarray, score: np.ndarray, record: np.ndarray,
                         threshold: float) -> List[Dict[str, object]]:
    """Per-bin S PR-AUC / FN rate with the patient composition of each bin."""
    b = apply_bins(values, edges)
    out = []
    for k in range(len(edges) - 1):
        m = b == k
        s_mask = m & np.asarray(y, bool)
        recs = sorted(set(record[m].tolist()))
        row = {"feature": name, "bin": k,
               "edge_low": float(edges[k]), "edge_high": float(edges[k + 1]),
               "n_beat": int(m.sum()), "n_s": int(s_mask.sum()),
               "n_record": len(recs),
               "records": ",".join(str(r) for r in recs[:12])}
        if s_mask.sum():
            row["fn_rate"] = float(np.mean(score[s_mask] < threshold))
            row["mean_s_score"] = float(np.mean(score[s_mask]))
        if m.sum() and 0 < int(np.asarray(y, bool)[m].sum()) < int(m.sum()):
            row["s_prauc_in_bin"] = beat_micro_prauc(np.asarray(y, bool)[m],
                                                     score[m])
        out.append(row)
    return out


#: Atrial proxies. ``independence`` is declared, never assumed: a proxy that
#: overlaps V10's own P-wave features cannot count as independent evidence.
ATRIAL_PROXY_META: Dict[str, Dict[str, str]] = {
    "atrial_window_energy_ratio": {
        "expected_direction": "lower ratio -> more failure",
        "independence": "independent of V10 features (energy only)"},
    "p_template_correlation": {
        "expected_direction": "lower correlation -> more failure",
        "independence": "OVERLAPS V10 P-wave morphology features"},
    "pre_qrs_peak_prominence": {
        "expected_direction": "lower prominence -> more failure",
        "independence": "partially overlaps V10 (morphology-derived)"},
    "p_window_morph_distance": {
        "expected_direction": "larger distance -> more failure",
        "independence": "OVERLAPS V10 P-wave morphology features"},
    "lead_atrial_concordance": {
        "expected_direction": "lower concordance -> more failure",
        "independence": "independent (two-lead agreement)"},
    "qrs_leakage_estimate": {
        "expected_direction": "confounder — higher leakage inflates the others",
        "independence": "confounder flag, not evidence"},
}


def atrial_proxies(cohort: AtlasCohort, rows: np.ndarray) -> Dict[str, np.ndarray]:
    """Several independent-ish pre-QRS proxies — never a P-wave ground truth.

    No detector output is called "P-wave presence": there is no P-wave
    annotation in this cohort, so every quantity here is a proxy whose
    agreement (and disagreement) is reported.
    """
    if cohort.beat is None:
        return {}
    beat = cohort.beat[rows]
    n, n_lead, width = beat.shape
    fs = cohort.fs
    center = width // 2
    def w(ms_lo: float, ms_hi: float) -> slice:
        lo = int(round(center + ms_lo * fs / 1000.0))
        hi = int(round(center + ms_hi * fs / 1000.0))
        return slice(max(0, min(lo, width - 2)), max(1, min(hi, width - 1)))
    p_win, iso_win, qrs_win = w(-250, -60), w(-400, -300), w(-60, 60)
    lead0 = beat[:, 0, :]
    eps = 1e-9

    def rms(a: np.ndarray) -> np.ndarray:
        return np.sqrt(np.mean(np.square(a), axis=-1) + eps)

    p_seg = lead0[:, p_win]
    iso_seg = lead0[:, iso_win]
    qrs_seg = lead0[:, qrs_win]
    energy_ratio = rms(p_seg) / (rms(iso_seg) + eps)
    prominence = (p_seg.max(axis=1) - p_seg.min(axis=1)) / \
        (qrs_seg.max(axis=1) - qrs_seg.min(axis=1) + eps)
    leakage = rms(p_seg[:, -max(1, p_seg.shape[1] // 4):]) / (rms(p_seg) + eps)

    rec = cohort.record[rows]
    corr = np.full(n, np.nan)
    dist = np.full(n, np.nan)
    for r in np.unique(rec):
        idx = np.where(rec == r)[0]
        # Label-free template: the record's median pre-QRS segment. Ectopic
        # beats are a small minority, so the median stands in for the normal
        # template WITHOUT reading a single DS2 label (spec §7).
        normal = idx
        if len(normal) < 5:
            continue
        tmpl = np.median(p_seg[normal], axis=0)
        tz = tmpl - tmpl.mean()
        denom = np.sqrt(np.sum(tz ** 2)) + eps
        seg = p_seg[idx] - p_seg[idx].mean(axis=1, keepdims=True)
        corr[idx] = (seg @ tz) / (np.sqrt(np.sum(seg ** 2, axis=1)) * denom + eps)
        scale = np.std(p_seg[normal]) + eps
        dist[idx] = np.sqrt(np.mean((p_seg[idx] - tmpl) ** 2, axis=1)) / scale
    if n_lead > 1:
        a = lead0[:, p_win] - lead0[:, p_win].mean(axis=1, keepdims=True)
        b = beat[:, 1, p_win] - beat[:, 1, p_win].mean(axis=1, keepdims=True)
        conc = np.sum(a * b, axis=1) / (np.sqrt(np.sum(a ** 2, axis=1))
                                        * np.sqrt(np.sum(b ** 2, axis=1)) + eps)
    else:
        conc = np.full(n, np.nan)
    return {"atrial_window_energy_ratio": energy_ratio,
            "p_template_correlation": corr,
            "pre_qrs_peak_prominence": prominence,
            "p_window_morph_distance": dist,
            "lead_atrial_concordance": conc,
            "qrs_leakage_estimate": leakage}


def quality_proxies(cohort: AtlasCohort, rows: np.ndarray
                    ) -> Dict[str, np.ndarray]:
    """Signal-quality / lead / alignment proxies (spec §8.6)."""
    if cohort.beat is None:
        return {}
    beat = cohort.beat[rows]
    n, n_lead, width = beat.shape
    lead0 = beat[:, 0, :]
    d = np.diff(lead0, axis=1)
    rng = lead0.max(axis=1) - lead0.min(axis=1) + 1e-9
    k = max(3, width // 16)
    kernel = np.ones(k) / k
    smooth = np.apply_along_axis(lambda v: np.convolve(v, kernel, mode="same"),
                                 1, lead0)
    return {
        "baseline_wander": (smooth.max(axis=1) - smooth.min(axis=1)) / rng,
        "hf_noise_rms": np.sqrt(np.mean(d ** 2, axis=1)) / rng,
        "flatline_frac": np.mean(np.abs(d) < 1e-6, axis=1),
        "saturation_frac": np.mean(
            np.abs(lead0 - lead0.mean(axis=1, keepdims=True))
            >= 0.999 * (rng[:, None] / 2), axis=1),
        "qrs_align_offset": (np.argmax(np.abs(lead0), axis=1)
                             - width // 2).astype(float) / width,
        "edge_clip": np.maximum(np.abs(lead0[:, 0]), np.abs(lead0[:, -1])) / rng,
        "n_lead": np.full(n, float(n_lead)),
    }


def calibration_vs_ranking(cohort: AtlasCohort, rows: np.ndarray,
                           model: ModelPredictions,
                           threshold: float) -> Dict[str, object]:
    """Split S errors into ranking failure vs threshold/calibration failure."""
    y = cohort.y_s[rows]
    score = model.score
    y5 = cohort.y5[rows]
    s_idx = np.where(y)[0]
    if not len(s_idx):
        raise Q5AError("no S beats — calibration/ranking split is undefined")
    ranks = rank_fraction(score, score[s_idx])
    fn = score[s_idx] < threshold
    high_rank_fn = fn & (ranks >= 0.90)      # ranked well, lost by the cut
    low_rank = ranks < 0.50
    fp_idx = np.where((~y) & (score >= threshold))[0]
    conf = {CLASS_NAMES[c]: int((y5[fp_idx] == c).sum()) for c in range(5)}
    return {
        "n_s": int(len(s_idx)), "n_fn": int(fn.sum()),
        "fn_rate": float(fn.mean()),
        "fn_that_are_threshold_only": int(high_rank_fn.sum()),
        "fn_that_are_ranking_failures": int((fn & low_rank).sum()),
        "median_rank_pct_of_s": float(np.median(ranks)),
        "false_positive_class_mix": conf,
        "note": ("A threshold move does not fix a ranking failure. The "
                 "alarm-rate dial is a closed direction and is not reopened."),
    }


def model_disagreement(cohort: AtlasCohort, rows: np.ndarray,
                       a: ModelPredictions, b: ModelPredictions,
                       thr_a: float, thr_b: float) -> Dict[str, object]:
    y = cohort.y_s[rows]
    ok_a = (a.score >= thr_a) == y
    ok_b = (b.score >= thr_b) == y
    s = np.asarray(y, bool)
    cells = {
        "both_correct": int((ok_a & ok_b & s).sum()),
        "a_only_correct": int((ok_a & ~ok_b & s).sum()),
        "b_only_correct": int((~ok_a & ok_b & s).sum()),
        "both_wrong": int((~ok_a & ~ok_b & s).sum()),
    }
    return {"model_a": a.label, "model_b": b.label, "s_beats": int(s.sum()),
            "cells": cells}


# ─────────────────────────────────────────────────────────────────────────────
# Feature blocks and incremental value (spec §9).
# ─────────────────────────────────────────────────────────────────────────────
def build_blocks(cohort: AtlasCohort, rows: np.ndarray,
                 rr: Dict[str, np.ndarray], atrial: Dict[str, np.ndarray],
                 quality: Dict[str, np.ndarray],
                 s_mask: np.ndarray) -> Dict[str, Dict[str, np.ndarray]]:
    """Assemble the five pre-registered blocks restricted to S beats."""
    sub = subtype_of(cohort.sym[rows])
    burden = {}
    for r in np.unique(cohort.record[rows]):
        idx = np.where(cohort.record[rows] == r)[0]
        burden[int(r)] = float(cohort.y_s[rows][idx].mean())
    blocks: Dict[str, Dict[str, np.ndarray]] = {
        "B_ATRIAL": {k: v[s_mask] for k, v in atrial.items()
                     if k != "qrs_leakage_estimate"},
        "B_RR": {k: v[s_mask] for k, v in rr.items()},
        "B_QUALITY": {k: v[s_mask] for k, v in quality.items()},
        "B_SUBTYPE": {f"subtype_{t}": (sub == t).astype(float)[s_mask]
                      for t in S_SUBTYPES},
        "B_PATIENT": {"patient_s_burden": np.array(
            [burden[int(r)] for r in cohort.record[rows]], float)[s_mask]},
    }
    if not (sub[s_mask] != "other").any():
        # No original annotation symbols were recovered — the subtype block is
        # dropped rather than filled with zeros pretending to be evidence.
        blocks.pop("B_SUBTYPE", None)
    return {k: v for k, v in blocks.items() if v}


def _design(block_dict: Dict[str, np.ndarray]) -> Tuple[np.ndarray, List[str]]:
    names = sorted(block_dict)
    if not names:
        return np.zeros((0, 0)), []
    cols = []
    for nm in names:
        v = np.asarray(block_dict[nm], float)
        med = np.nanmedian(v) if np.isfinite(v).any() else 0.0
        cols.append(np.where(np.isfinite(v), v, med))
    X = np.column_stack(cols)
    return X, names


def _standardize(X: np.ndarray) -> np.ndarray:
    if X.size == 0:
        return X
    mu = X.mean(axis=0)
    sd = X.std(axis=0)
    sd[sd < 1e-9] = 1.0
    return (X - mu) / sd


def grouped_holdout_logloss(X: np.ndarray, y: np.ndarray, groups: np.ndarray,
                            seed: int = SEED0) -> Dict[str, object]:
    """Leave-one-patient-out (or patient-grouped 5-fold) held-out log loss.

    Returns the per-patient held-out log loss so the CI can be a patient
    bootstrap — never a beat bootstrap.
    """
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import log_loss, roc_auc_score
    y = np.asarray(y, int)
    groups = np.asarray(groups)
    uniq = np.unique(groups)
    if len(uniq) < 3:
        raise Q5AError("patient-held-out evaluation needs >= 3 patients")
    folds = [[g] for g in uniq] if len(uniq) <= 25 else \
        [uniq[i::5] for i in range(5)]
    pred = np.full(len(y), np.nan)
    for hold in folds:
        te = np.isin(groups, hold)
        tr = ~te
        if y[tr].sum() in (0, int(tr.sum())) or not te.any():
            pred[te] = float(y[tr].mean()) if tr.any() else 0.5
            continue
        Xtr = X[tr] if X.size else np.zeros((int(tr.sum()), 1))
        Xte = X[te] if X.size else np.zeros((int(te.sum()), 1))
        clf = LogisticRegression(max_iter=2000, C=1.0, solver="lbfgs",
                                 random_state=seed)
        clf.fit(Xtr, y[tr])
        pred[te] = clf.predict_proba(Xte)[:, 1]
    pred = np.clip(np.nan_to_num(pred, nan=0.5), 1e-6, 1 - 1e-6)
    per_patient = {}
    for g in uniq:
        m = groups == g
        per_patient[int(g)] = float(-np.mean(
            y[m] * np.log(pred[m]) + (1 - y[m]) * np.log(1 - pred[m])))
    auroc = None
    if 0 < y.sum() < len(y):
        auroc = float(roc_auc_score(y, pred))
    return {"logloss": float(log_loss(y, pred, labels=[0, 1])),
            "auroc": auroc, "per_patient_logloss": per_patient,
            "n_patient": int(len(uniq)), "n_obs": int(len(y))}


def block_incremental_value(base: Dict[str, np.ndarray],
                            block: Dict[str, np.ndarray],
                            y: np.ndarray, groups: np.ndarray,
                            n_boot: int = NB_BOOT,
                            seed: int = SEED0) -> Dict[str, object]:
    """Held-out log-loss improvement from adding one block on top of ``base``.

    Positive delta = the block explains error the base did not. The CI is a
    patient bootstrap over per-patient held-out log-loss differences.
    """
    Xb, base_names = _design(base)
    Xk, block_names = _design(block)
    Xb = _standardize(Xb) if Xb.size else np.zeros((len(y), 0))
    Xk = _standardize(Xk) if Xk.size else np.zeros((len(y), 0))
    base_fit = grouped_holdout_logloss(Xb, y, groups, seed=seed)
    aug = np.column_stack([Xb, Xk]) if Xb.size else Xk
    aug_fit = grouped_holdout_logloss(aug, y, groups, seed=seed)
    per_patient_delta = {g: base_fit["per_patient_logloss"][g]
                         - aug_fit["per_patient_logloss"][g]
                         for g in base_fit["per_patient_logloss"]}
    ci = boot_ci(per_patient_delta, n_boot=n_boot, seed=seed)
    direction = float(np.mean([v > 0 for v in per_patient_delta.values()]))
    influence = sorted(per_patient_delta, key=lambda g: -per_patient_delta[g])
    dropped = {g: v for g, v in per_patient_delta.items()
               if g not in influence[:DROP_RECORDS_FOR_STABILITY]}
    stable = bool(dropped and np.mean(list(dropped.values())) > 0)
    return {
        "features": block_names, "base_features": base_names,
        "base_logloss": base_fit["logloss"], "aug_logloss": aug_fit["logloss"],
        "delta_logloss": float(ci["mean"]),
        "ci_low": float(ci["ci_low"]), "ci_high": float(ci["ci_high"]),
        "auroc_base": base_fit["auroc"], "auroc_aug": aug_fit["auroc"],
        "patient_direction_frac": direction,
        "per_patient_delta": {str(k): float(v)
                              for k, v in per_patient_delta.items()},
        "top_influence_records": [int(g) for g in
                                  influence[:DROP_RECORDS_FOR_STABILITY]],
        "delta_after_dropping_top": float(np.mean(list(dropped.values())))
        if dropped else float("nan"),
        "stable_after_record_drop": stable,
        "n_patient": base_fit["n_patient"], "n_obs": base_fit["n_obs"],
    }


def univariate_associations(block: Dict[str, np.ndarray], y: np.ndarray
                            ) -> List[Dict[str, object]]:
    from sklearn.metrics import roc_auc_score
    out = []
    y = np.asarray(y, int)
    for name in sorted(block):
        v = np.asarray(block[name], float)
        m = np.isfinite(v)
        row: Dict[str, object] = {"feature": name, "n_finite": int(m.sum())}
        if m.sum() > 10 and 0 < y[m].sum() < int(m.sum()) and np.std(v[m]) > 0:
            row["auroc_error_vs_feature"] = float(roc_auc_score(y[m], v[m]))
            row["mean_error"] = float(np.mean(v[m][y[m] == 1]))
            row["mean_ok"] = float(np.mean(v[m][y[m] == 0]))
        out.append(row)
    return out


def evaluate_blocks(blocks: Dict[str, Dict[str, np.ndarray]], y: np.ndarray,
                    groups: np.ndarray, n_boot: int = NB_BOOT,
                    log: Optional[RunLog] = None) -> Dict[str, object]:
    """Every block once on a shared base, then once adjusted for the others."""
    log = log or RunLog()
    y = np.asarray(y, int)
    if int(y.sum()) < BLOCK_MIN_EVENTS:
        return {"underpowered": True, "n_events": int(y.sum()),
                "min_events": BLOCK_MIN_EVENTS, "blocks": {},
                "reason": (f"only {int(y.sum())} error events among S beats "
                           f"(< {BLOCK_MIN_EVENTS}) — block comparison is not "
                           "informative; recorded as underpowered")}
    base: Dict[str, np.ndarray] = {}
    out: Dict[str, object] = {"underpowered": False, "n_events": int(y.sum()),
                              "blocks": {}}
    for name, blk in blocks.items():
        ev = block_incremental_value(base, blk, y, groups, n_boot=n_boot)
        others = {f"{o}__{k}": v for o, ob in blocks.items() if o != name
                  for k, v in ob.items()}
        adj = block_incremental_value(others, blk, y, groups, n_boot=n_boot)
        ev["adjusted_delta_logloss"] = adj["delta_logloss"]
        ev["adjusted_ci_low"] = adj["ci_low"]
        ev["adjusted_ci_high"] = adj["ci_high"]
        ev["univariate"] = univariate_associations(blk, y)
        out["blocks"][name] = ev
        log(f"  {name}: delta logloss {ev['delta_logloss']:+.4f} "
            f"[{ev['ci_low']:+.4f}, {ev['ci_high']:+.4f}], "
            f"patient direction {ev['patient_direction_frac']:.2f}")
    return out


def atrial_support(atrial: Dict[str, np.ndarray], s_mask: np.ndarray,
                   error: np.ndarray) -> Dict[str, object]:
    """Do several atrial proxies point the same way, and is it leakage?"""
    from sklearn.metrics import roc_auc_score
    rows = []
    concordant = 0
    for name, meta in ATRIAL_PROXY_META.items():
        if name not in atrial:
            continue
        v = np.asarray(atrial[name], float)[s_mask]
        m = np.isfinite(v)
        row: Dict[str, object] = {"proxy": name, **meta,
                                  "n_finite": int(m.sum())}
        if m.sum() > 10 and 0 < error[m].sum() < int(m.sum()) and np.std(v[m]) > 0:
            auc = float(roc_auc_score(error[m], v[m]))
            row["auroc_error_vs_proxy"] = auc
            expected_lower = meta["expected_direction"].startswith("lower")
            agrees = (auc < 0.5) if expected_lower else (auc > 0.5)
            row["agrees_with_expected_direction"] = bool(agrees)
            if name != "qrs_leakage_estimate" and agrees:
                concordant += 1
        rows.append(row)
    independent = [r for r in rows
                   if r.get("agrees_with_expected_direction")
                   and str(r.get("independence", "")).startswith("independent")]
    return {"proxies": rows, "n_concordant": concordant,
            "n_concordant_independent": len(independent),
            "concordant_enough": bool(concordant >= 2),
            "has_independent_support": bool(len(independent) >= 1),
            "caveat": ("No P-wave annotation exists in this cohort. These are "
                       "proxies; none of them is P-wave presence ground truth."),
            }


def patient_heterogeneity(metrics: Dict[str, Dict[str, object]]
                          ) -> Dict[str, object]:
    """Is the failure a diffuse patient shift that survives model changes?"""
    labels = [k for k in metrics if "per_record_s_prauc" in metrics[k]]
    if not labels:
        return {"available": False}
    spreads, worst = {}, {}
    for lab in labels:
        pr = {int(k): float(v)
              for k, v in metrics[lab]["per_record_s_prauc"].items()}
        vals = np.array(list(pr.values()), float)
        spreads[lab] = float(np.percentile(vals, 90) - np.percentile(vals, 10))
        q = np.percentile(vals, 25)
        worst[lab] = {r for r, v in pr.items() if v <= q}
    overlap = None
    if len(labels) >= 2:
        a, b = worst[labels[0]], worst[labels[1]]
        overlap = float(len(a & b) / max(1, len(a | b)))
    return {"available": True, "p90_minus_p10": spreads,
            "worst_quartile_overlap": overlap,
            "heterogeneity_large": bool(max(spreads.values())
                                        >= PATIENT_HETEROGENEITY_MIN),
            "failure_persists_across_models": bool(
                overlap is not None and overlap >= PATIENT_PERSISTENCE_MIN)}


# ─────────────────────────────────────────────────────────────────────────────
# Pre-registered decision tree (spec §10). No branch is forced.
# ─────────────────────────────────────────────────────────────────────────────
def _qualified(ev: Dict[str, object]) -> bool:
    return bool(ev.get("ci_low", 0) > 0
                and ev.get("adjusted_ci_low", 0) > 0
                and ev.get("patient_direction_frac", 0)
                >= BLOCK_MIN_PATIENT_DIRECTION
                and ev.get("stable_after_record_drop", False))


def evaluate_branch_decision(gates: Dict[str, object],
                             block_evidence: Dict[str, object],
                             atrial: Optional[Dict[str, object]],
                             patient: Dict[str, object]) -> Dict[str, object]:
    """D0 -> D5, applied verbatim. ``largest mean`` alone never selects a branch."""
    trace: List[str] = []
    if not gates.get("pass", False):
        branch = gates.get("branch") or BRANCH_INSUFFICIENT
        return {"branch": branch, "rule": "D0",
                "reason": "; ".join(gates.get("stops", [])) or "artifact gate failed",
                "next_step": ("recover artifacts / fix the adapter — this is "
                              "not a modelling experiment"),
                "competing_branches": [], "trace": ["D0 artifact/data gate"],
                "evidence": {"gates": gates}}
    blocks = block_evidence.get("blocks", {})
    if block_evidence.get("underpowered") or not blocks:
        trace.append("blocks underpowered or absent")
        return {"branch": BRANCH_UNRESOLVED, "rule": "D5",
                "reason": block_evidence.get("reason",
                                             "no block evidence available"),
                "next_step": ("cheapest additional measurement: recover "
                              "beat-level artifacts / more S-bearing patients"),
                "competing_branches": [], "trace": trace,
                "evidence": {"block_evidence": block_evidence}}

    ranked = sorted(blocks.items(), key=lambda kv: -kv[1]["delta_logloss"])
    qualified = [(k, v) for k, v in ranked if _qualified(v)]
    trace.append(f"ranked by delta logloss: "
                 f"{[(k, round(v['delta_logloss'], 5)) for k, v in ranked]}")
    trace.append(f"qualified (CI>0, adjusted CI>0, direction>="
                 f"{BLOCK_MIN_PATIENT_DIRECTION}, stable): "
                 f"{[k for k, _ in qualified]}")
    competing = [k for k, _ in qualified]

    if not qualified:
        if patient.get("available") and patient.get("heterogeneity_large") \
                and patient.get("failure_persists_across_models"):
            trace.append("no block qualifies; patient heterogeneity is large "
                         "and worst patients persist across models -> D4")
            return {"branch": BRANCH_PATIENT, "rule": "D4",
                    "reason": ("no atrial/RR/quality block dominates, while "
                               "worst-patient failure persists across models "
                               "with large patient heterogeneity"),
                    "next_step": ("small DS1-only pilot comparing ERM vs "
                                  "patient-CVaR/GroupDRO — GroupDRO is NOT "
                                  "pre-selected"),
                    "competing_branches": competing, "trace": trace,
                    "evidence": {"patient": patient, "blocks": blocks}}
        trace.append("no block qualifies and the diffuse-shift conditions are "
                     "not met -> D5")
        return {"branch": BRANCH_UNRESOLVED, "rule": "D5",
                "reason": ("evidence is similar across blocks or the CIs are "
                           "wide with unstable direction"),
                "next_step": ("propose the cheapest additional measurement or "
                              "artifact recovery; do not combine two "
                              "hypotheses in one model"),
                "competing_branches": competing, "trace": trace,
                "evidence": {"blocks": blocks, "patient": patient}}

    winner, wev = qualified[0]
    others = qualified[1:]
    decisive = all(wev["delta_logloss"] >= BLOCK_MARGIN * o["delta_logloss"]
                   for _k, o in others)
    trace.append(f"winner {winner} decisive over {[k for k, _ in others]}: "
                 f"{decisive} (margin {BLOCK_MARGIN})")
    if not decisive:
        return {"branch": BRANCH_UNRESOLVED, "rule": "D5",
                "reason": (f"{winner} does not lead the other qualified "
                           f"block(s) {[k for k, _ in others]} by the "
                           f"pre-registered margin of {BLOCK_MARGIN}x"),
                "next_step": ("separate the tied factors with a cheaper "
                              "targeted measurement before intervening"),
                "competing_branches": competing, "trace": trace,
                "evidence": {"blocks": blocks}}
    if winner not in BLOCK_TO_BRANCH:
        trace.append(f"winning block {winner} has no intervention branch "
                     "(subtype/patient are descriptive) -> D4/D5")
        if winner == "B_PATIENT" and patient.get("failure_persists_across_models"):
            return {"branch": BRANCH_PATIENT, "rule": "D4",
                    "reason": "patient block dominates and failure persists",
                    "next_step": ("DS1-only ERM vs patient-CVaR/GroupDRO pilot"),
                    "competing_branches": competing, "trace": trace,
                    "evidence": {"blocks": blocks, "patient": patient}}
        return {"branch": BRANCH_UNRESOLVED, "rule": "D5",
                "reason": (f"{winner} is a descriptive block; it names no "
                           "single manipulable variable"),
                "next_step": "define a manipulable proxy before Q5-B",
                "competing_branches": competing, "trace": trace,
                "evidence": {"blocks": blocks}}
    if winner == "B_ATRIAL":
        ok = bool(atrial and atrial.get("concordant_enough")
                  and atrial.get("has_independent_support"))
        trace.append(f"atrial concordance gate: {ok}")
        if not ok:
            return {"branch": BRANCH_UNRESOLVED, "rule": "D5",
                    "reason": ("the atrial block leads but the proxies do not "
                               "agree, or the only agreeing proxies overlap "
                               "V10's own P-wave features / QRS leakage"),
                    "next_step": ("add an independent atrial measurement "
                                  "before any intervention"),
                    "competing_branches": competing, "trace": trace,
                    "evidence": {"atrial": atrial, "blocks": blocks}}
    branch = BLOCK_TO_BRANCH[winner]
    rule = {"B_QUALITY": "D1", "B_ATRIAL": "D2", "B_RR": "D3"}[winner]
    next_step = {
        BRANCH_QUALITY: ("freeze the classifier; intervene deterministically on "
                         "quality gate / lead choice / alignment-filtering, "
                         "with a label-free selection rule"),
        BRANCH_ATRIAL: ("freeze the V10 baseline; add ONE independent atrial "
                        "evidence feature, with within-record atrial shuffle "
                        "and temporal-window shift as negative controls "
                        "(no residual CNN)"),
        BRANCH_RR: ("intervene on the RR/timing block only, with an "
                    "equal-width irrelevant timing control; atrial features "
                    "stay fixed"),
    }[branch]
    return {"branch": branch, "rule": rule,
            "reason": (f"{winner} carries the largest STABLE incremental value "
                       f"(delta logloss {wev['delta_logloss']:+.5f}, CI "
                       f"[{wev['ci_low']:+.5f}, {wev['ci_high']:+.5f}], patient "
                       f"direction {wev['patient_direction_frac']:.2f}, stable "
                       "after dropping the most influential records)"),
            "next_step": next_step, "competing_branches": competing,
            "trace": trace,
            "evidence": {"winner": winner, "block": wev, "atrial": atrial,
                         "patient": patient}}


def q5b_design_brief(decision: Dict[str, object],
                     block_evidence: Dict[str, object],
                     metrics: Dict[str, Dict[str, object]]) -> Dict[str, object]:
    """Draft material for the NEXT experiment — never a Q5-B implementation."""
    branch = decision["branch"]
    controls = {
        BRANCH_ATRIAL: ["within-record shuffle of the atrial feature",
                        "temporal-window shift of the atrial window"],
        BRANCH_RR: ["irrelevant timing feature of equal width",
                    "within-record shuffle of the RR feature"],
        BRANCH_QUALITY: ["random equal-rate exclusion rule",
                         "quality rule applied to a shuffled quality score"],
        BRANCH_PATIENT: ["ERM with identical budget and regularisation",
                         "random patient grouping instead of true patients"],
    }.get(branch, [])
    one_variable = {
        BRANCH_ATRIAL: "one independent atrial-evidence feature/gate",
        BRANCH_RR: "the RR/coupling representation only",
        BRANCH_QUALITY: "the deterministic quality/lead/alignment rule only",
        BRANCH_PATIENT: "the training objective only (ERM vs CVaR/GroupDRO)",
    }.get(branch)
    return {
        "selected_branch": branch, "rule": decision["rule"],
        "competing_branches": decision.get("competing_branches", []),
        "supporting_evidence": decision.get("reason"),
        "disconfirming_evidence": [
            v for k, v in (("underpowered", block_evidence.get("reason")),)
            if v] + [t for t in decision.get("trace", []) if "not" in t],
        "required_inputs": ["beat-level stored probabilities with stable keys",
                            "DS1-only design decisions",
                            "patient-grouped nested CV on DS1"],
        "single_intervention_variable": one_variable,
        "negative_controls": controls,
        "expected_risks": [
            "small patient count keeps CIs wide",
            "proxy features may overlap the frozen baseline's own features",
            "DS2 must not be consulted while the design is fixed"],
        "go_no_go_proposal": {
            "primary": "patient-macro S PR-AUC improvement",
            "uncertainty": "patient bootstrap CI excluding 0",
            "lower_tail": "p10 / worst-quartile improved or non-inferior",
            "seed": "consistent direction across seeds",
            "control": "intervention minus negative control > 0",
            "scope": "design frozen on DS1 before DS2/INCART is touched"},
        "not_implemented": ("Q5-B spec, code and training notebook are NOT "
                            "created in this PR. They wait for a MEASURED "
                            "Q5-A and explicit user approval."),
        "baseline_reference": {k: {"record_macro_s_prauc":
                                   v.get("record_macro_s_prauc"),
                                   "p10": v.get("patient_summary", {}).get("p10")}
                               for k, v in metrics.items()},
    }


# ─────────────────────────────────────────────────────────────────────────────
# Bundle writing (spec §12).
# ─────────────────────────────────────────────────────────────────────────────
def _dump_json(path: str, obj) -> None:
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(_json_safe(obj), fh, ensure_ascii=False, indent=1)


def _dump_csv(path: str, rows: Sequence[Dict[str, object]],
              columns: Optional[Sequence[str]] = None) -> None:
    rows = list(rows)
    cols = list(columns) if columns else sorted({k for r in rows for k in r})
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(cols)
        for r in rows:
            w.writerow([_scalar(r.get(c, "")) for c in cols])


def _scalar(v):
    if isinstance(v, (dict, list, tuple)):
        return json.dumps(_json_safe(v), ensure_ascii=False)
    if isinstance(v, (np.integer, np.floating, np.bool_)):
        return v.item()
    return v


def bundle_fingerprint(run_dir: str, files: Sequence[str]) -> Dict[str, str]:
    out = {}
    for f in files:
        p = os.path.join(run_dir, f)
        if os.path.exists(p):
            out[f] = sha256_file(p)
    return out


def source_fingerprints(sources: Dict[str, str]) -> Dict[str, Dict[str, str]]:
    """SHA256 of every source bundle Q5-A reads (before/after comparison)."""
    out: Dict[str, Dict[str, str]] = {}
    for label, run_dir in sources.items():
        if not run_dir or not os.path.isdir(run_dir):
            out[label] = {}
            continue
        fps = {}
        for name in sorted(os.listdir(run_dir)):
            p = os.path.join(run_dir, name)
            if os.path.isfile(p):
                fps[name] = sha256_file(p)
        out[label] = fps
    return out


def verify_bundle(out_dir: str, blocked: bool = False) -> None:
    files = BLOCKED_BUNDLE_FILES if blocked else BUNDLE_FILES
    figs = BLOCKED_FIGURES if blocked else FIGURES
    missing = [f for f in files if not os.path.exists(os.path.join(out_dir, f))]
    if missing:
        raise Q5AError(f"bundle incomplete, missing {missing}")
    figdir = os.path.join(out_dir, "figures")
    missing_fig = [f for f in figs
                   if not os.path.exists(os.path.join(figdir, f))]
    if missing_fig:
        raise Q5AError(f"figures incomplete, missing {missing_fig}")


def write_blocked_bundle(out_dir: str, inventory: Dict[str, object],
                         freeze: Dict[str, object], gates: Dict[str, object],
                         provenance: Dict[str, object],
                         log: Optional[RunLog] = None) -> Dict[str, object]:
    """A failed artifact/data gate is a REAL result — never hidden (spec §12)."""
    log = log or RunLog()
    os.makedirs(out_dir, exist_ok=True)
    decision = evaluate_branch_decision(gates, {"blocks": {}}, None,
                                        {"available": False})
    result = {
        "experiment_id": EXPERIMENT_ID, "arm_id": ARM_ID,
        "status": STATUS_BLOCKED,
        "analysis_only": True, "training_performed": False,
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "gates": gates, "baseline_freeze": freeze,
        "decision": decision,
        "q5b_design_brief": q5b_design_brief(decision, {"blocks": {}}, {}),
        "note": ("BLOCKED_MEASURED: the atlas could not be computed from the "
                 "stored artifacts. This is a valid measured outcome; the next "
                 "step is artifact recovery, not a model experiment."),
    }
    _dump_json(os.path.join(out_dir, "config.json"),
               {"experiment_id": EXPERIMENT_ID, "mode": "ANALYZE",
                "blocks": list(BLOCKS), "branches": list(BRANCHES),
                "n_boot": NB_BOOT, "analysis_only": True})
    _dump_json(os.path.join(out_dir, "manifest.json"), provenance)
    _dump_json(os.path.join(out_dir, "result.json"), result)
    _dump_json(os.path.join(out_dir, "source_inventory.json"), inventory)
    _dump_csv(os.path.join(out_dir, "source_inventory.csv"),
              [{k: v for k, v in e.items() if k != "prediction_files"}
               for e in inventory.get("entries", [])] or [{"run_id": ""}])
    _dump_json(os.path.join(out_dir, "baseline_freeze.json"), freeze)
    _dump_json(os.path.join(out_dir, "decision.json"), decision)
    with open(os.path.join(out_dir, "log.txt"), "w", encoding="utf-8") as fh:
        fh.write(log.text())
    _write_summary(out_dir, result, {}, decision)
    _figure_gate_dashboard(out_dir, inventory, freeze, gates)
    verify_bundle(out_dir, blocked=True)
    log(f"BLOCKED_MEASURED bundle written: {out_dir}")
    return result


# ─────────────────────────────────────────────────────────────────────────────
# Figures (spec §13).
# ─────────────────────────────────────────────────────────────────────────────
def _plt():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    return plt


def _figdir(out_dir: str) -> str:
    d = os.path.join(out_dir, "figures")
    os.makedirs(d, exist_ok=True)
    return d


def _caption(ax, text: str) -> None:
    ax.set_xlabel(text, fontsize=7)


def _table_fig(path: str, title: str, rows: Sequence[Sequence[str]],
               header: Sequence[str], caption: str) -> None:
    plt = _plt()
    h = max(2.0, 0.32 * (len(rows) + 2))
    fig, ax = plt.subplots(figsize=(11, h))
    ax.axis("off")
    ax.set_title(title, fontsize=10)
    tbl = ax.table(cellText=[[str(c) for c in r] for r in rows] or [["(none)"]
                                                                   ] * 1,
                   colLabels=list(header), loc="center")
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(7)
    fig.text(0.01, 0.01, caption, fontsize=7)
    fig.tight_layout()
    fig.savefig(path, dpi=110)
    plt.close(fig)


def _figure_gate_dashboard(out_dir: str, inventory: Dict[str, object],
                           freeze: Dict[str, object],
                           gates: Dict[str, object]) -> None:
    rows = [[e.get("run_id", "")[:38], str(e.get("model_name"))[:22],
             "yes" if e.get("beat_level_ready") else "no",
             str(e.get("metric_definition"))[:18],
             str(e.get("git_sha"))[:8], str(e.get("run_timestamp"))[:16]]
            for e in inventory.get("entries", [])]
    rows.append(["FREEZE", freeze.get("status", "?"), "", "", "", ""])
    rows.append(["GATE", "PASS" if gates.get("pass") else "STOP",
                 "; ".join(gates.get("stops", []))[:60], "", "", ""])
    _table_fig(os.path.join(_figdir(out_dir), "inventory_gate_dashboard.png"),
               f"{EXPERIMENT_ID}/{ARM_ID} source inventory & gate dashboard",
               rows, ["run", "model", "beat-level", "metric", "git", "when"],
               "ANALYSIS ONLY / NO TRAINING · failure-associated factors, not "
               "causes · cohort MIT-BIH DS1/DS2 (descriptive audit)")


def _write_figures(out_dir: str, result: Dict[str, object],
                   cohort: AtlasCohort, rows: np.ndarray,
                   models: Dict[str, ModelPredictions],
                   inventory: Dict[str, object], freeze: Dict[str, object],
                   gates: Dict[str, object], tables: Dict[str, object],
                   log: RunLog) -> None:
    plt = _plt()
    figdir = _figdir(out_dir)
    metrics = result["model_metrics"]
    n_pat = len(result["split"]["ds2"])
    sub = (f"MIT-BIH DS2 descriptive audit · n_patient={n_pat} · "
           f"n_beat={int(len(rows))} · patient bootstrap CI · "
           "failure-ASSOCIATED factors (not causes)")

    _figure_gate_dashboard(out_dir, inventory, freeze, gates)

    _table_fig(os.path.join(figdir, "baseline_comparison_table.png"),
               "recomputed baselines vs the recorded claims",
               [[r["model"], r["recorded_claim"],
                 None if r["recomputed_beat_micro"] is None
                 else round(r["recomputed_beat_micro"], 4),
                 None if r["recomputed_record_macro"] is None
                 else round(r["recomputed_record_macro"], 4),
                 r["closest_unit"], str(r["verdict"])[:44]]
                for r in result["baseline_claim_check"]],
               ["model", "recorded", "beat-micro", "record-macro", "unit",
                "verdict"], sub)

    # patient waterfall + paired delta
    labels = sorted(metrics)
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    for lab in labels:
        pr = {int(k): v for k, v in metrics[lab]["per_record_s_prauc"].items()}
        vals = [pr[r] for r in sorted(pr, key=lambda r: pr[r])]
        axes[0].plot(range(len(vals)), vals, marker="o", ms=3, label=lab)
    axes[0].set_title(f"patient waterfall — S PR-AUC per record\n{sub}",
                      fontsize=8)
    axes[0].legend(fontsize=7)
    if len(labels) >= 2:
        a, b = labels[0], labels[1]
        pa = {int(k): v for k, v in metrics[a]["per_record_s_prauc"].items()}
        pb = {int(k): v for k, v in metrics[b]["per_record_s_prauc"].items()}
        common = sorted(set(pa) & set(pb))
        d = [pb[r] - pa[r] for r in common]
        axes[1].bar(range(len(d)), sorted(d), width=0.9)
        axes[1].axhline(0, color="k", lw=0.6)
        axes[1].set_title(f"paired delta {b} - {a} (per patient)", fontsize=8)
    fig.tight_layout()
    fig.savefig(os.path.join(figdir, "patient_waterfall_paired_delta.png"),
                dpi=110)
    plt.close(fig)

    _table_fig(os.path.join(figdir, "patient_lower_tail_table.png"),
               "patient lower tail (median / p10 / worst-5)",
               [[lab, round(metrics[lab]["patient_summary"]["median"], 4),
                 round(metrics[lab]["patient_summary"]["p10"], 4),
                 ", ".join(f"{w['record']}:{w['value']:.3f}"
                           for w in metrics[lab]["patient_summary"]["worst5"])]
                for lab in labels],
               ["model", "median", "p10", "worst-5 (record:value)"], sub)

    st = tables["subtype"]
    fig, ax = plt.subplots(figsize=(8, 4))
    names = [r["subtype"] for r in st]
    fn = [r.get("fn_rate", np.nan) for r in st]
    ax.bar(names, fn)
    for i, r in enumerate(st):
        ax.text(i, 0.02, f"n={r['n']}" + ("*" if r["descriptive_only"] else ""),
                ha="center", fontsize=7)
    ax.set_title(f"S subtype FN rate (* = n<{SUBTYPE_MIN_N}, descriptive only)"
                 f"\n{sub}", fontsize=8)
    fig.tight_layout()
    fig.savefig(os.path.join(figdir, "subtype_prauc_fn.png"), dpi=110)
    plt.close(fig)

    rr = tables["rr"]
    fig, ax = plt.subplots(figsize=(9, 4))
    feats = sorted({r["feature"] for r in rr})
    mat = np.full((len(feats), max(1, max(r["bin"] for r in rr) + 1)), np.nan)
    for r in rr:
        if "fn_rate" in r:
            mat[feats.index(r["feature"]), r["bin"]] = r["fn_rate"]
    im = ax.imshow(mat, aspect="auto", cmap="viridis")
    ax.set_yticks(range(len(feats)), feats, fontsize=7)
    ax.set_xlabel("DS1-defined bin (edges frozen on DS1, applied to DS2)",
                  fontsize=7)
    ax.set_title(f"RR/coupling vs FN rate\n{sub}", fontsize=8)
    fig.colorbar(im, ax=ax, label="FN rate")
    fig.tight_layout()
    fig.savefig(os.path.join(figdir, "rr_coupling_error_heatmap.png"), dpi=110)
    plt.close(fig)

    ap = (result.get("atrial_support") or {}).get("proxies", [])
    fig, ax = plt.subplots(figsize=(9, 4))
    nm = [r["proxy"] for r in ap] or ["(no waveform — proxies unavailable)"]
    auc = [r.get("auroc_error_vs_proxy", np.nan) for r in ap] or [np.nan]
    ax.barh(nm, auc)
    ax.axvline(0.5, color="k", lw=0.6)
    ax.set_title("atrial PROXY vs S-beat error (AUROC) — proxies, NOT P-wave "
                 f"ground truth\n{sub}", fontsize=8)
    fig.tight_layout()
    fig.savefig(os.path.join(figdir, "atrial_proxy_vs_error.png"), dpi=110)
    plt.close(fig)

    q = tables["quality"]
    aud = tables["audit_208_213"]
    _table_fig(os.path.join(figdir, "quality_and_208_213_audit.png"),
               "quality proxies (top) and the record 208/213 audit (bottom)",
               [[r["feature"], r.get("bin", ""), r.get("n_beat", ""),
                 r.get("n_s", ""), round(r.get("fn_rate", float("nan")), 4)]
                for r in q]
               + [["--- 208/213 audit ---", "", "", "", ""]]
               + [[f"record {a['record']}", a.get("n_atlas", ""),
                   a.get("s_atlas", ""),
                   json.dumps(a.get("class_counts_atlas", {})),
                   str(a.get("known_deficit", ""))[:40]] for a in aud],
               ["feature/record", "bin/n", "n_beat/s", "n_s/classes", "fn/note"],
               sub)

    fig, axes = plt.subplots(1, 2, figsize=(11, 4))
    from sklearn.metrics import precision_recall_curve
    y = cohort.y_s[rows]
    for lab in labels:
        p, r_, _t = precision_recall_curve(y, models[lab].score)
        axes[0].plot(r_, p, label=lab)
        bins = metrics[lab]["calibration_bins"]
        axes[1].plot([b["mean_prob"] for b in bins],
                     [b["observed_rate"] for b in bins], marker="o", ms=3,
                     label=f"{lab} (ECE {metrics[lab]['calibration']['ece']:.3f})")
    axes[0].set_title(f"S PR curves\n{sub}", fontsize=8)
    axes[0].legend(fontsize=7)
    axes[1].plot([0, 1], [0, 1], "k--", lw=0.6)
    axes[1].set_title("calibration (reliability)", fontsize=8)
    axes[1].legend(fontsize=7)
    fig.tight_layout()
    fig.savefig(os.path.join(figdir, "calibration_pr_curves.png"), dpi=110)
    plt.close(fig)

    dis = result.get("model_disagreement")
    fig, ax = plt.subplots(figsize=(6, 4))
    if dis:
        cells = dis["cells"]
        mat = np.array([[cells["both_correct"], cells["a_only_correct"]],
                        [cells["b_only_correct"], cells["both_wrong"]]], float)
        ax.imshow(mat, cmap="magma")
        for i in range(2):
            for j in range(2):
                ax.text(j, i, int(mat[i, j]), ha="center", va="center",
                        color="w")
        ax.set_xticks([0, 1], ["both/A-only", "B-only/both-wrong"], fontsize=7)
        ax.set_yticks([0, 1], ["row1", "row2"], fontsize=7)
        ax.set_title(f"S-beat model disagreement ({dis['model_a']} vs "
                     f"{dis['model_b']})\n{sub}", fontsize=8)
    else:
        ax.axis("off")
        ax.set_title("model disagreement unavailable (single beat-level model)")
    fig.tight_layout()
    fig.savefig(os.path.join(figdir, "model_disagreement_matrix.png"), dpi=110)
    plt.close(fig)

    blocks = result["block_evidence"].get("blocks", {})
    fig, ax = plt.subplots(figsize=(8, 4))
    names = list(blocks)
    for i, b in enumerate(names):
        ev = blocks[b]
        ax.errorbar(ev["delta_logloss"], i,
                    xerr=[[max(0.0, ev["delta_logloss"] - ev["ci_low"])],
                          [max(0.0, ev["ci_high"] - ev["delta_logloss"])]],
                    fmt="o", capsize=4)
    ax.axvline(0, color="k", lw=0.6)
    ax.set_yticks(range(len(names)), names, fontsize=8)
    ax.set_title("feature-block incremental value (held-out log loss, "
                 f"patient bootstrap)\n{sub}", fontsize=8)
    fig.tight_layout()
    fig.savefig(os.path.join(figdir, "block_evidence_forest.png"), dpi=110)
    plt.close(fig)

    dec = result["decision"]
    _table_fig(os.path.join(figdir, "branch_decision_matrix.png"),
               f"pre-registered branch decision — {dec['branch']} ({dec['rule']})",
               [[b, "SELECTED" if b == dec["branch"] else
                 ("competing" if b in dec.get("competing_branches", []) else "")]
                for b in BRANCHES]
               + [["reason", str(dec["reason"])[:80]],
                  ["next step", str(dec["next_step"])[:80]]],
               ["branch", "status"], sub)

    _write_gallery(figdir, cohort, rows, models, result, sub)
    log("figures written")


GALLERY_CATEGORIES = (
    ("confident_false_negative", "S beats sorted by ASCENDING score"),
    ("confident_false_positive", "non-S beats sorted by DESCENDING score"),
    ("v9_fail_to_v10_correct", "S beats sorted by DESCENDING score gain"),
    ("v9_correct_to_v10_fail", "S beats sorted by DESCENDING score loss"),
    ("both_models_fail", "S beats sorted by ASCENDING mean score"),
    ("unmatched_or_filtered_208_213", "beats of 208/213 in record order"),
)


def _write_gallery(figdir: str, cohort: AtlasCohort, rows: np.ndarray,
                   models: Dict[str, ModelPredictions],
                   result: Dict[str, object], sub: str) -> None:
    """Error gallery with pre-fixed sort keys and top-N (no cherry-picking)."""
    plt = _plt()
    labels = sorted(models)
    ref = labels[-1]
    y = cohort.y_s[rows]
    score = models[ref].score
    thr = result["model_metrics"][ref]["threshold"]["threshold"]
    other = models[labels[0]].score if len(labels) > 1 else score
    thr_o = result["model_metrics"][labels[0]]["threshold"]["threshold"]
    picks: Dict[str, np.ndarray] = {}
    s_idx = np.where(y)[0]
    n_idx = np.where(~y)[0]
    picks["confident_false_negative"] = s_idx[np.argsort(score[s_idx])][:GALLERY_TOP_N]
    picks["confident_false_positive"] = n_idx[np.argsort(-score[n_idx])][:GALLERY_TOP_N]
    gain = score[s_idx] - other[s_idx]
    picks["v9_fail_to_v10_correct"] = s_idx[np.argsort(-gain)][:GALLERY_TOP_N]
    picks["v9_correct_to_v10_fail"] = s_idx[np.argsort(gain)][:GALLERY_TOP_N]
    both = ((score[s_idx] < thr) & (other[s_idx] < thr_o))
    picks["both_models_fail"] = s_idx[both][:GALLERY_TOP_N]
    aud = np.where(np.isin(cohort.record[rows], AUDIT_RECORDS))[0][:GALLERY_TOP_N]
    picks["unmatched_or_filtered_208_213"] = aud

    cats = [c for c, _ in GALLERY_CATEGORIES]
    fig, axes = plt.subplots(len(cats), GALLERY_TOP_N,
                             figsize=(3.0 * GALLERY_TOP_N, 2.0 * len(cats)),
                             squeeze=False)
    for i, cat in enumerate(cats):
        for j in range(GALLERY_TOP_N):
            ax = axes[i][j]
            ax.set_xticks([])
            ax.set_yticks([])
            sel = picks.get(cat, np.zeros(0, int))
            if j >= len(sel):
                ax.axis("off")
                continue
            k = int(sel[j])
            if cohort.beat is not None:
                ax.plot(cohort.beat[rows][k, 0, :], lw=0.8)
            r = int(cohort.record[rows][k])
            ax.set_title(f"{cat}\nrec {r} · sym {cohort.sym[rows][k]} · "
                         f"{ref} {score[k]:.3f}", fontsize=6)
    fig.suptitle("error gallery — public MIT-BIH record ids · sort keys fixed "
                 f"in code · top {GALLERY_TOP_N} each\n{sub}", fontsize=8)
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    fig.savefig(os.path.join(figdir, "error_gallery.png"), dpi=110)
    plt.close(fig)


def _write_summary(out_dir: str, result: Dict[str, object],
                   metrics: Dict[str, Dict[str, object]],
                   decision: Dict[str, object]) -> None:
    """Korean summary shown at the end of the notebook (spec §13)."""
    lines = [f"# {EXPERIMENT_ID} / {ARM_ID} — 요약",
             "",
             f"- status: **{result['status']}** (ANALYSIS ONLY / NO TRAINING)",
             f"- 확인된 것: {len(metrics)}개 모델의 지표를 동일 코드로 재계산",
             ]
    for lab, m in metrics.items():
        ps = m.get("patient_summary", {})
        lines.append(
            f"  - {lab}: beat-micro {m.get('beat_micro_s_prauc'):.4f} · "
            f"record-macro {m.get('record_macro_s_prauc'):.4f} · "
            f"p10 {ps.get('p10', float('nan')):.4f}")
    lines += [
        "- 확인되지 않은 것: P-wave ground truth(없음), 인과관계, DS2 밖의 일반화",
        "- 이 결과는 **원인이 아니라 '실패 연관 요인'** 이다. 관찰적 사후 분석이며,",
        "  실제 원인 여부는 Q5-B에서 그 요인 하나만 바꾸는 개입과 음성대조군으로 검증한다.",
        f"- 선택된 분기: **{decision['branch']}** ({decision['rule']})",
        f"  - 근거: {decision['reason']}",
        "  - 다음 실험에서 조작할 단 하나의 변수: "
        + (result.get("q5b_design_brief", {}).get("single_intervention_variable")
           or "없음 — 분기가 확정되지 않았으므로 개입 변수를 정하지 않는다"),
        f"  - 다음 단계 제안: {decision['next_step']}",
        "- **다음 실험(Q5-B)은 아직 실행하지 않았고, 구현하지도 않았다.**",
        "- residual CNN 경로는 closed 상태이며 이 분석에서 재개하지 않는다. "
        "INCART rescue run도 하지 않는다.",
    ]
    with open(os.path.join(out_dir, "summary.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")


# ─────────────────────────────────────────────────────────────────────────────
# The analysis itself.
# ─────────────────────────────────────────────────────────────────────────────
def run_atlas(cohort: AtlasCohort, models: Dict[str, ModelPredictions],
              inventory: Dict[str, object], freeze: Dict[str, object],
              provenance: Dict[str, object], out_dir: str,
              n_boot: int = NB_BOOT, smoke: bool = False,
              log: Optional[RunLog] = None) -> Dict[str, object]:
    """Compute the whole failure atlas from stored artifacts. Never trains."""
    log = log or RunLog()
    assert_analysis_only()
    os.makedirs(out_dir, exist_ok=True)
    t0 = time.time()
    split = cohort_split(cohort)

    sources = {lab: m.source_dir for lab, m in models.items() if m.source_dir}
    fp_before = source_fingerprints(sources)

    # ── matching gate ───────────────────────────────────────────────────────
    matches: Dict[str, Dict[str, object]] = {}
    aligned: Dict[str, ModelPredictions] = {}
    key_index = {str(k): i for i, k in enumerate(cohort.key)}
    for lab, m in models.items():
        audit = match_beat_keys(cohort, m, strict=False)
        matches[lab] = audit
        if audit["pass"]:
            # Scatter onto the cohort's own row order. A model that covers
            # only part of the cohort (the legacy artifacts score DS2 only)
            # leaves NaN elsewhere — never a silently shifted array.
            pos = np.array([key_index[str(k)] for k in m.key], int)
            score_full = np.full(cohort.n, np.nan)
            score_full[pos] = m.score
            per_seed_full = None
            if m.per_seed is not None:
                per_seed_full = np.full((len(m.per_seed), cohort.n), np.nan)
                per_seed_full[:, pos] = m.per_seed
            aligned[lab] = ModelPredictions(
                label=lab, key=cohort.key.copy(), score=score_full,
                y_true=cohort.y_s.copy(), record=cohort.record.copy(),
                score_kind=m.score_kind, per_seed=per_seed_full,
                source_dir=m.source_dir, fingerprint=m.fingerprint,
                key_mode=m.key_mode, verification=m.verification)
    matching = {"pass": all(a["pass"] for a in matches.values()) and bool(matches),
                "fail_reasons": [r for a in matches.values()
                                 for r in a["fail_reasons"]],
                "per_model": matches}
    gates = evaluate_artifact_gates(inventory, freeze, matching)
    if not gates["pass"]:
        log("artifact/data gate FAILED -> BLOCKED_MEASURED (a real result)")
        return write_blocked_bundle(out_dir, inventory, freeze, gates,
                                    provenance, log=log)

    # Analysis cohort: the DS2 records EVERY frozen model actually scores.
    # Excluding a record here is reported, never silent.
    ds2 = split["ds2"]
    covered = set(ds2)
    for lab, a in matches.items():
        covered &= set(int(r) for r in a["model_record_scope"])
    excluded_records = sorted(set(ds2) - covered)
    if not covered:
        raise Q5AError("the frozen models share no DS2 record — nothing to "
                       "compare; check the artifact scopes in matching_audit")
    if excluded_records:
        log(f"analysis restricted to {len(covered)} DS2 record(s) common to "
            f"every model; not covered by all: {excluded_records}")
    ds2 = sorted(covered)
    rows = np.sort(cohort.rows_of(ds2))
    split = dict(split, ds2_analysis=ds2, ds2_excluded=excluded_records)
    for lab in list(aligned):
        m = aligned[lab]
        sel = np.isin(np.arange(cohort.n), rows)
        aligned[lab] = ModelPredictions(
            label=lab, key=m.key[sel], score=m.score[sel],
            y_true=m.y_true[sel], record=m.record[sel],
            score_kind=m.score_kind,
            per_seed=None if m.per_seed is None else m.per_seed[:, sel],
            source_dir=m.source_dir, fingerprint=m.fingerprint,
            key_mode=m.key_mode, verification=m.verification)

    ds1_rows_all = cohort.rows_of(split["ds1"])
    ds1_prev = (float(cohort.y_s[ds1_rows_all].mean()) if len(ds1_rows_all)
                else None)
    metrics = {lab: model_metrics(m, cohort, split, rows, n_boot=n_boot,
                                  ds1_prevalence=ds1_prev)
               for lab, m in aligned.items()}
    labels = sorted(aligned)
    ref = labels[-1]
    thr = metrics[ref]["threshold"]["threshold"]

    # ── failure maps ────────────────────────────────────────────────────────
    y = cohort.y_s[rows]
    rec = cohort.record[rows]
    s_mask = np.asarray(y, bool)
    error = (aligned[ref].score[s_mask] < thr).astype(int)

    rr = rr_features(cohort, rows)
    atrial = atrial_proxies(cohort, rows)
    quality = quality_proxies(cohort, rows)

    ds1_rows = np.sort(cohort.rows_of(split["ds1"]))
    rr_ds1 = rr_features(cohort, ds1_rows)
    rr_tables: List[Dict[str, object]] = []
    for name in ("coupling_ratio", "compensatory_pause_ratio", "pre_rr",
                 "post_rr"):
        try:
            edges = ds1_quantile_bins(rr_ds1[name])
        except Q5AError:
            continue
        rr_tables += binned_failure_table(name, rr[name], edges, y,
                                          aligned[ref].score, rec, thr)
    atrial_tables: List[Dict[str, object]] = []
    quality_tables: List[Dict[str, object]] = []
    if atrial:
        at_ds1 = atrial_proxies(cohort, ds1_rows)
        for name in sorted(atrial):
            try:
                edges = ds1_quantile_bins(at_ds1[name])
            except Q5AError:
                continue
            atrial_tables += binned_failure_table(name, atrial[name], edges, y,
                                                 aligned[ref].score, rec, thr)
    if quality:
        q_ds1 = quality_proxies(cohort, ds1_rows)
        for name in sorted(quality):
            try:
                edges = ds1_quantile_bins(q_ds1[name])
            except Q5AError:
                continue
            quality_tables += binned_failure_table(name, quality[name], edges, y,
                                                   aligned[ref].score, rec, thr)

    sub_tab = subtype_metrics(cohort, rows, aligned, ref, thr)
    audit_rows = record_audit_208_213(cohort, matches)
    cal_rank = calibration_vs_ranking(cohort, rows, aligned[ref], thr)
    disagree = None
    if len(labels) >= 2:
        disagree = model_disagreement(
            cohort, rows, aligned[labels[0]], aligned[ref],
            metrics[labels[0]]["threshold"]["threshold"], thr)

    blocks = build_blocks(cohort, rows, rr, atrial, quality, s_mask)
    block_ev = evaluate_blocks(blocks, error, rec[s_mask], n_boot=n_boot,
                               log=log)
    at_support = atrial_support(atrial, s_mask, error) if atrial else None
    pat = patient_heterogeneity(metrics)
    decision = evaluate_branch_decision(gates, block_ev, at_support, pat)
    brief = q5b_design_brief(decision, block_ev, metrics)
    log(f"branch: {decision['branch']} ({decision['rule']})")

    fp_after = source_fingerprints(sources)
    if fp_after != fp_before:
        raise Q5AError("a source run bundle changed during Q5-A — "
                       "IMMUTABILITY VIOLATION, discard this output")

    result = {
        "experiment_id": EXPERIMENT_ID, "arm_id": ARM_ID,
        "status": STATUS_SMOKE if smoke else STATUS_MEASURED,
        "smoke": bool(smoke),
        "analysis_only": True, "training_performed": False,
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "cohort": {"db": str(cohort.db[0]) if cohort.n else "?",
                   "n_beat": cohort.n, "key_mode": cohort.key_mode,
                   "fs": cohort.fs},
        "split": {"ds1": [int(r) for r in split["ds1"]],
                  "ds2": [int(r) for r in split["ds2"]],
                  "overlap": [], "note": split["note"]},
        "baseline_freeze": freeze, "gates": gates,
        "matching": {lab: {k: v for k, v in a.items() if k != "per_record"}
                     for lab, a in matches.items()},
        "model_metrics": metrics,
        "baseline_claim_check": baseline_claim_check(metrics, freeze),
        "subtype_metrics": sub_tab,
        "calibration_vs_ranking": cal_rank,
        "model_disagreement": disagree,
        "record_audit_208_213": audit_rows,
        "atrial_support": at_support,
        "patient_heterogeneity": pat,
        "block_evidence": block_ev,
        "decision": decision,
        "q5b_design_brief": brief,
        "source_fingerprint_before": fp_before,
        "source_fingerprint_after": fp_after,
        "source_immutable": True,
        "language_boundary": (
            "Observational post-hoc analysis. Everything reported here is a "
            "failure-ASSOCIATED factor or a candidate intervention hypothesis. "
            "No causal claim is made; Q5-B tests causality with one "
            "intervention and a negative control."),
        "closed_directions": list(CLOSED_DIRECTIONS),
        "wall_time_s": float(time.time() - t0),
    }
    tables = {"subtype": sub_tab, "rr": rr_tables, "atrial": atrial_tables,
              "quality": quality_tables, "audit_208_213": audit_rows}
    _write_atlas_bundle(out_dir, result, inventory, freeze, matches, tables,
                        provenance, decision, metrics, log)
    _write_figures(out_dir, result, cohort, rows, aligned, inventory, freeze,
                   gates, tables, log)
    verify_bundle(out_dir)
    log(f"bundle complete: {out_dir}")
    return result


def _write_atlas_bundle(out_dir, result, inventory, freeze, matches, tables,
                        provenance, decision, metrics, log) -> None:
    _dump_json(os.path.join(out_dir, "config.json"),
               {"experiment_id": EXPERIMENT_ID, "arm_id": ARM_ID,
                "mode": "ANALYZE", "analysis_only": True,
                "blocks": list(BLOCKS), "branches": list(BRANCHES),
                "n_boot": NB_BOOT, "subtypes": list(S_SUBTYPES),
                "gallery_top_n": GALLERY_TOP_N,
                "block_rules": {"min_patient_direction":
                                BLOCK_MIN_PATIENT_DIRECTION,
                                "margin": BLOCK_MARGIN,
                                "min_events": BLOCK_MIN_EVENTS,
                                "drop_records_for_stability":
                                DROP_RECORDS_FOR_STABILITY}})
    man = dict(provenance)
    man["source_fingerprint_before"] = result["source_fingerprint_before"]
    _dump_json(os.path.join(out_dir, "manifest.json"), man)
    _dump_json(os.path.join(out_dir, "result.json"), result)
    _dump_json(os.path.join(out_dir, "source_inventory.json"), inventory)
    _dump_csv(os.path.join(out_dir, "source_inventory.csv"),
              [{k: v for k, v in e.items() if k != "prediction_files"}
               for e in inventory.get("entries", [])] or [{"run_id": ""}])
    _dump_json(os.path.join(out_dir, "baseline_freeze.json"), freeze)
    _dump_csv(os.path.join(out_dir, "matching_audit.csv"),
              [{"model": lab, **p} for lab, a in matches.items()
               for p in a["per_record"]])
    _dump_csv(os.path.join(out_dir, "patient_metrics.csv"),
              [{"model": lab, "record": int(r), "s_prauc": v,
                "is_worst5": any(w["record"] == int(r) for w in
                                 metrics[lab]["patient_summary"]["worst5"])}
               for lab, m in metrics.items()
               for r, v in m["per_record_s_prauc"].items()])
    _dump_csv(os.path.join(out_dir, "subtype_metrics.csv"), tables["subtype"])
    _dump_csv(os.path.join(out_dir, "rr_timing_metrics.csv"), tables["rr"]
              or [{"feature": "none"}])
    _dump_csv(os.path.join(out_dir, "atrial_proxy_metrics.csv"),
              tables["atrial"] or [{"feature": "none"}])
    _dump_csv(os.path.join(out_dir, "quality_metrics.csv"), tables["quality"]
              or [{"feature": "none"}])
    _dump_csv(os.path.join(out_dir, "model_disagreement.csv"),
              [result["model_disagreement"]] if result["model_disagreement"]
              else [{"note": "single beat-level model"}])
    _dump_csv(os.path.join(out_dir, "mechanism_evidence.csv"),
              [{"block": b, "delta_logloss": ev["delta_logloss"],
                "ci_low": ev["ci_low"], "ci_high": ev["ci_high"],
                "adjusted_delta_logloss": ev["adjusted_delta_logloss"],
                "adjusted_ci_low": ev["adjusted_ci_low"],
                "patient_direction_frac": ev["patient_direction_frac"],
                "stable_after_record_drop": ev["stable_after_record_drop"],
                "top_influence_records": ev["top_influence_records"],
                "n_patient": ev["n_patient"], "n_obs": ev["n_obs"],
                "interpretation": "failure-ASSOCIATED, not causal"}
               for b, ev in result["block_evidence"].get("blocks", {}).items()]
              or [{"block": "none", "interpretation": "underpowered"}])
    _dump_json(os.path.join(out_dir, "decision.json"), decision)
    with open(os.path.join(out_dir, "log.txt"), "w", encoding="utf-8") as fh:
        fh.write(log.text())
    _write_summary(out_dir, result, metrics, decision)


def report_bundle(run_dir: str) -> Dict[str, object]:
    """REPORT mode: read a stored bundle. Nothing is recomputed or written."""
    res_path = os.path.join(run_dir, "result.json")
    if not os.path.exists(res_path):
        return {"status": STATUS_NOT_RUN, "run_dir": run_dir,
                "message": "RESULT NOT RUN — no stored Q5-A bundle here"}
    result = _read_json(res_path) or {}
    payload = {
        "status": result.get("status", STATUS_NOT_RUN),
        "run_dir": run_dir,
        "decision": _read_json(os.path.join(run_dir, "decision.json")),
        "baseline_freeze": _read_json(os.path.join(run_dir,
                                                   "baseline_freeze.json")),
        "summary_md": _read_text(os.path.join(run_dir, "summary.md")),
        "figures": [f for f in FIGURES
                    if os.path.exists(os.path.join(run_dir, "figures", f))],
        "csv_tables": [f for f in BUNDLE_FILES if f.endswith(".csv")
                       and os.path.exists(os.path.join(run_dir, f))],
        "model_metrics": result.get("model_metrics", {}),
        "q5b_design_brief": result.get("q5b_design_brief"),
        "recomputed": False,
    }
    return payload


def _read_text(path: str) -> Optional[str]:
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


# ─────────────────────────────────────────────────────────────────────────────
# Synthetic fixtures for the CPU test contract. NEVER a result (spec §14).
# ─────────────────────────────────────────────────────────────────────────────
def synthetic_atlas(n_per_record: int = 120, width: int = 128,
                    seed: int = 5, records: Sequence[int] = MIT_ALL_RECORDS,
                    fs: float = 360.0) -> AtlasCohort:
    """A synthetic MIT-shaped cohort. Scientifically meaningless by design."""
    rng = np.random.RandomState(seed)
    recs = [int(r) for r in records]
    n = len(recs) * n_per_record
    rec = np.repeat(recs, n_per_record)
    samp = np.concatenate([np.arange(n_per_record) * 300 + 7 for _ in recs])
    y5 = np.zeros(n, int)
    for i, r in enumerate(recs):
        sl = slice(i * n_per_record, (i + 1) * n_per_record)
        marks = rng.choice(n_per_record, size=max(6, n_per_record // 12),
                           replace=False)
        y5[sl][marks[: len(marks) // 2]] = S_INDEX
        blk = y5[sl]
        blk[marks[: len(marks) // 2]] = S_INDEX
        blk[marks[len(marks) // 2:]] = 2
        y5[sl] = blk
    sym = np.where(y5 == S_INDEX,
                   rng.choice(list(S_SUBTYPES), size=n), "N").astype("<U2")
    sym[y5 == 2] = "V"
    t = np.linspace(-0.5, 0.5, width)
    qrs = np.exp(-((t / 0.03) ** 2))
    p_wave = np.exp(-(((t + 0.22) / 0.04) ** 2))
    beat = np.zeros((n, 2, width), "float32")
    p_amp = np.where(y5 == S_INDEX, 0.05, 0.20) + 0.02 * rng.randn(n)
    for lead in range(2):
        beat[:, lead, :] = (qrs[None, :] + p_amp[:, None] * p_wave[None, :]
                            + 0.01 * rng.randn(n, width)).astype("float32")
    pre = 0.8 + 0.05 * rng.randn(n)
    pre[y5 == S_INDEX] *= 0.6
    post = 0.8 + 0.05 * rng.randn(n)
    post[y5 == S_INDEX] *= 1.3
    recs_arr = np.array(sorted(set(rec.tolist())), int)
    keys = np.array([f"mitdb|{r}|{s}|{y}" for r, s, y in zip(rec, samp, sym)])
    return AtlasCohort(
        key=keys, key_mode=KEY_MODE_ANNOTATION,
        db=np.full(n, "mitdb", dtype="<U8"), record=rec, y5=y5,
        y_s=(y5 == S_INDEX), sym=sym, pre_rr=pre, post_rr=post, beat=beat,
        fs=fs, records=recs_arr,
        idx_of={int(r): np.where(rec == r)[0] for r in recs_arr})


def synthetic_model(cohort: AtlasCohort, label: str, skill: float = 3.0,
                    seed: int = 7) -> ModelPredictions:
    """Scores driven by the synthetic P-wave amplitude — fixture only."""
    rng = np.random.RandomState(seed)
    width = cohort.beat.shape[-1]
    p_idx = slice(int(0.20 * width), int(0.36 * width))
    p_energy = cohort.beat[:, 0, p_idx].max(axis=1)
    z = skill * (0.15 - p_energy) + 0.5 * rng.randn(cohort.n)
    return ModelPredictions(label=label, key=cohort.key.copy(),
                            score=_sigmoid(z), y_true=cohort.y_s.copy(),
                            record=cohort.record.copy(),
                            score_kind="probability", source_dir=None)


def write_synthetic_run(dir_path: str, model_name: str,
                        cohort: AtlasCohort, model: ModelPredictions,
                        s_prauc: float = 0.6) -> str:
    """Write a fixture run bundle that INVENTORY can discover."""
    os.makedirs(dir_path, exist_ok=True)
    _dump_json(os.path.join(dir_path, "config.json"),
               {"model_name": model_name, "primary_metric": "record_macro_s_prauc",
                "s_index": S_INDEX, "seeds": [1, 2], "split": "de_chazal_ds1_ds2"})
    _dump_json(os.path.join(dir_path, "result.json"),
               {"experiment_id": "fixture", "primary_metric":
                "record_macro_s_prauc", "s_prauc": s_prauc,
                "timestamp_utc": "2026-01-01T00:00:00Z",
                "split": "de_chazal_ds1_ds2"})
    _dump_json(os.path.join(dir_path, "manifest.json"),
               {"git_commit_sha": "fixture", "data": {"sha256": "fixture",
                                                      "file_name": "fixture.npz"}})
    parts = [k.split("|") for k in cohort.key]
    np.savez_compressed(
        os.path.join(dir_path, "predictions.npz"),
        prob=model.score, y_true=model.y_true, pid=model.record,
        sample=np.array([int(p[2]) for p in parts]),
        sym=np.array([p[3] for p in parts]),
        db=np.array([p[0] for p in parts]))
    return dir_path


# ─────────────────────────────────────────────────────────────────────────────
# Self-check and CLI.
# ─────────────────────────────────────────────────────────────────────────────
def self_check(min_version: int = MODULE_VERSION) -> Dict[str, object]:
    if MODULE_VERSION < min_version:
        raise Q5AError(f"stale module {MODULE_VERSION} < {min_version}")
    info = assert_analysis_only()
    if set(BLOCK_TO_BRANCH) - set(BLOCKS):
        raise Q5AError("branch map references an unknown block")
    return {"module_file": os.path.abspath(__file__),
            "module_version": MODULE_VERSION, "module_build": MODULE_BUILD,
            "modes": list(MODES), "default_mode": DEFAULT_MODE,
            "blocks": list(BLOCKS), "branches": list(BRANCHES),
            "status": STATUS, "analysis_only": info["analysis_only"],
            "closed_directions": list(CLOSED_DIRECTIONS),
            "fixed_problem": FIXED_PROBLEM}


def provenance_for(data_path: Optional[str] = None) -> Dict[str, object]:
    prov: Dict[str, object] = {"git_commit_sha": git_commit_sha(),
                               "packages": package_versions(), "gpu": gpu_info(),
                               "analysis_only": True,
                               "training_performed": False}
    if data_path and os.path.exists(data_path):
        prov["data"] = {"abs_path": os.path.abspath(data_path),
                        "file_name": os.path.basename(data_path),
                        "sha256": sha256_file(data_path),
                        "size_bytes": os.path.getsize(data_path)}
    return prov


def main(argv: Optional[Sequence[str]] = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--mode", default=DEFAULT_MODE,
                    help=f"exactly one of {MODES} (default {DEFAULT_MODE})")
    ap.add_argument("--data", help="beat-level atlas source npz")
    ap.add_argument("--source", help="frozen source npz the legacy runs "
                                     "consumed (defaults to --data); used to "
                                     "VERIFY row correspondence")
    ap.add_argument("--ann-dir", help="MIT-BIH .atr directory (symbol/subtype "
                                      "recovery); measured location is "
                                      "mitbih/raw_ann/mitdb")
    ap.add_argument("--roots", nargs="*", default=[],
                    help="run directories to inventory")
    ap.add_argument("--registry", help="registry.jsonl (append-only check)")
    ap.add_argument("--inventory", help="directory holding source_inventory.json")
    ap.add_argument("--run", help="stored Q5-A run dir (REPORT)")
    ap.add_argument("--out", help="output directory")
    ap.add_argument("--n-boot", type=int, default=NB_BOOT)
    args = ap.parse_args(argv)
    mode = resolve_mode(args.mode)
    log = RunLog()

    if mode == "DESIGN":
        log(f"{EXPERIMENT_ID}/{ARM_ID} DESIGN — {STATUS}")
        log("ANALYSIS ONLY / NO TRAINING. Failure-associated factors, not causes.")
        log(json.dumps(self_check(), ensure_ascii=False, indent=1))
        return 0

    if mode == "INVENTORY":
        if not args.roots or not args.out:
            raise Q5AError("INVENTORY needs --roots and --out")
        os.makedirs(args.out, exist_ok=True)
        inv = scan_inventory(args.roots, args.registry, log=log)
        freeze = freeze_baseline(inv)
        gates = evaluate_artifact_gates(inv, freeze, None)
        _dump_json(os.path.join(args.out, "source_inventory.json"), inv)
        _dump_csv(os.path.join(args.out, "source_inventory.csv"),
                  [{k: v for k, v in e.items() if k != "prediction_files"}
                   for e in inv["entries"]] or [{"run_id": ""}])
        _dump_json(os.path.join(args.out, "baseline_freeze.json"), freeze)
        _figure_gate_dashboard(args.out, inv, freeze, gates)
        log(f"freeze status: {freeze['status']}; gate pass: {gates['pass']}")
        for s in gates["stops"]:
            log(f"  STOP: {s}")
        return 0

    if mode == "ANALYZE":
        if not args.data or not args.inventory or not args.out:
            raise Q5AError("ANALYZE needs --data, --inventory and --out")
        inv = _read_json(os.path.join(args.inventory, "source_inventory.json"))
        if inv is None:
            raise Q5AError(f"no source_inventory.json in {args.inventory} — "
                           "run INVENTORY first")
        freeze = _read_json(os.path.join(args.inventory,
                                         "baseline_freeze.json")) \
            or freeze_baseline(inv)
        cohort, source_audit = load_atlas_source(args.data, log=log)
        rr_from_samples(cohort)
        ann_report = {"usable": False, "reason": "no --ann-dir given"}
        if args.ann_dir:
            ann_report = attach_symbols_from_annotations(cohort, args.ann_dir,
                                                         log=log)
        source_audit["annotation_symbols"] = ann_report
        source_index = load_frozen_source_index(args.source or args.data,
                                                log=log)
        models: Dict[str, ModelPredictions] = {}
        for label, sel in freeze.get("selected", {}).items():
            if not sel.get("beat_level_ready"):
                log(f"{label}: aggregate-only artifact, excluded from "
                    "beat-level comparison (spec §5)")
                continue
            models[label] = load_model_predictions(
                sel["run_dir"], label, source_index=source_index, log=log)
        if not models:
            gates = evaluate_artifact_gates(inv, freeze, None)
            gates["pass"] = False
            gates["stops"] = gates["stops"] or [
                "no beat-level prediction artifact could be loaded"]
            gates["branch"] = gates["branch"] or BRANCH_INSUFFICIENT
            write_blocked_bundle(args.out, inv, freeze, gates,
                                 provenance_for(args.data), log=log)
            return 0
        prov = provenance_for(args.data)
        prov["atlas_source_audit"] = source_audit
        run_atlas(cohort, models, inv, freeze, prov, args.out,
                  n_boot=args.n_boot, log=log)
        return 0

    if mode == "REPORT":
        if not args.run:
            raise Q5AError("REPORT needs --run")
        payload = report_bundle(args.run)
        compact = {k: v for k, v in payload.items()
                   if k not in ("summary_md", "model_metrics", "decision")}
        dec = payload.get("decision") or {}
        compact["decision"] = {k: dec.get(k) for k in
                               ("branch", "rule", "reason", "next_step",
                                "competing_branches")}
        log(json.dumps(compact, ensure_ascii=False, indent=1))
        for lab, m in (payload.get("model_metrics") or {}).items():
            ps = m.get("patient_summary", {})
            log(f"  {lab}: beat-micro {m.get('beat_micro_s_prauc'):.4f} · "
                f"record-macro {m.get('record_macro_s_prauc'):.4f} · "
                f"p10 {ps.get('p10', float('nan')):.4f}")
        if payload.get("summary_md"):
            log(payload["summary_md"])
        return 0
    raise Q5AError(f"unhandled mode {mode}")                # pragma: no cover


if __name__ == "__main__":
    sys.exit(main())
