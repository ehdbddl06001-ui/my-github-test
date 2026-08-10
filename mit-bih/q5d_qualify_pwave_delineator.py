"""EXP-2026-007 / Q5-D — QUALIFY: frozen P-wave delineator qualification.

NO TRAINING / NO SCIENTIFIC ANALYSIS.  This module answers exactly one
question: *does one frozen delineation rule find expert-annotated P waves well
enough to be used as a measuring instrument?*  It never scores a model, never
opens a DS2 class label as a class, and never computes an outcome metric.

What it reads
-------------
- MIT-BIH raw waveforms ``.dat``/``.hea`` (channel 0 only), from the immutable
  asset acquired by PREP_DATA-A (canonical run ``20260809T153151``).
- ``.atr`` **R sample positions**.  Reference R locations are used as given;
  R peaks are never re-detected.
- ``pwave 1.0.0`` expert P annotations for the 12 annotated records.

What stays sealed
-----------------
DS2 beat class labels, the V10 probability package, and the processed beat
arrays.  Those are outcome; this substage must finish without them.

One honest caveat about ``.atr`` on DS2: picking R locations out of an
annotation file requires knowing which annotations are *beats*, which means
touching the symbol column.  So the symbol is reduced to a boolean
``is_beat`` the moment it is read (:func:`_beat_samples`) and the class itself
is dropped — never stored, never returned, never written to an output file for
a DS2 record.  DS1 keeps its symbols because DS1 labels are not sealed and the
frozen RR band is defined on DS1 N beats.

Stages
------
``DESIGN``              — print the plan, read nothing.
``QUALIFY_DS1_FREEZE``  — DS1 dry report + derive and freeze the constants.
``QUALIFY_DS2_GATE``    — run once on the six DS2 expert records, decide.
``QUALIFY_REPORT``      — replay a saved bundle, recompute nothing.

The freeze is the boundary: ``QUALIFY_DS2_GATE`` refuses to start until
``frozen_constants.json`` exists, and it re-checks that file's hash so a
constant cannot be edited after DS2 has been seen.

Decisions: ``MEASUREMENT_QUALIFIED`` | ``MEASUREMENT_UNQUALIFIED`` |
``QUALIFY_RESULT_NOT_RUN``.  A failure is a complete, valid result — the spec
forbids widening the window, swapping the lead, changing the delineator, or
excluding records by hand to rescue it.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib
import json
import os
import platform
import statistics
import sys
import time
from typing import Dict, List, Optional, Sequence, Tuple

EXPERIMENT_ID = "EXP-2026-007"
ARM_ID = "Q5-D"
SUBSTAGE = "QUALIFY measurement qualification"
RUN_SLUG = "q5d_qualify"
MODULE_VERSION = 1
MODULE_BUILD = "2026-08-10"

NO_SCIENCE_BANNER = (
    "EXP-2026-007 / Q5-D QUALIFY — NO TRAINING / NO SCIENTIFIC ANALYSIS")

MODES: Tuple[str, ...] = (
    "DESIGN", "QUALIFY_DS1_FREEZE", "QUALIFY_DS2_GATE", "QUALIFY_REPORT")
FORBIDDEN_MODES: Tuple[str, ...] = (
    "ASSOCIATION", "ANALYZE", "MEASURE", "TRAIN", "JOIN")

DECISION_QUALIFIED = "MEASUREMENT_QUALIFIED"
DECISION_UNQUALIFIED = "MEASUREMENT_UNQUALIFIED"
DECISION_NOT_RUN = "QUALIFY_RESULT_NOT_RUN"
DECISIONS: Tuple[str, ...] = (
    DECISION_QUALIFIED, DECISION_UNQUALIFIED, DECISION_NOT_RUN)

# ─── de Chazal inter-patient split, as used everywhere in this repo ──────────
# (mit-bih/colab_crossdb.py:24-25 — copied, not re-derived)
DS1_RECORDS: Tuple[str, ...] = tuple(str(r) for r in (
    101, 106, 108, 109, 112, 114, 115, 116, 118, 119, 122, 124,
    201, 203, 205, 207, 208, 209, 215, 220, 223, 230))
DS2_RECORDS: Tuple[str, ...] = tuple(str(r) for r in (
    100, 103, 105, 111, 113, 117, 121, 123, 200, 202, 210, 212,
    213, 214, 219, 221, 222, 228, 231, 232, 233, 234))
#: The 12 records carrying published expert P-wave annotations.
PWAVE_RECORDS: Tuple[str, ...] = tuple(str(r) for r in (
    100, 101, 103, 106, 117, 119, 122, 207, 214, 222, 223, 231))

DS1_EXPERT_RECORDS: Tuple[str, ...] = tuple(
    r for r in PWAVE_RECORDS if r in DS1_RECORDS)
DS2_EXPERT_RECORDS: Tuple[str, ...] = tuple(
    r for r in PWAVE_RECORDS if r in DS2_RECORDS)

#: AAMI N class (mit-bih/svdb_labels.py:62).  DS1 only.
AAMI_N_SYMBOLS = frozenset("NLRej")
#: Every symbol that marks a beat, as opposed to a rhythm/quality annotation
#: (mit-bih/svdb_labels.py:75).
BEAT_SYMBOLS = frozenset("NLRBAaJSVrFejnE/fQ?")

EXPECTED_FS = 360.0
DELINEATOR_METHOD = "dwt"
DELINEATOR_CHANNEL = 0

# ─── Frozen rule parameters (spec «Measurement qualification gate» item 2) ───
MATCH_TOLERANCE_MS = 50.0
P_SEARCH_MIN_MS = 40.0
P_SEARCH_MAX_MS = 300.0
RR_WINDOW_BEATS = 21          # q5a_patient_failure_atlas.py :: rr_features
RR_BAND_LOW_PCTL = 25.0
RR_BAND_HIGH_PCTL = 75.0
DISCORDANCE_PCTL = 75.0

# ─── Gate thresholds (spec item 4).  Never relax these after seeing DS2. ─────
SENS_MACRO_MIN = 0.80
PPV_MACRO_MIN = 0.80
PER_RECORD_MIN = 0.70
PER_RECORD_MIN_COUNT = 5
CHANCE_RATIO_MIN = 4.0
CHANCE_CI_LOWER_MIN = 1.0

N_CIRCULAR_SHIFT = 200
N_BOOTSTRAP = 2000
PERMUTATION_SEED = 2026007
BOOTSTRAP_SEED = 2026008

PINNED_PACKAGES: Tuple[str, ...] = ("neurokit2", "wfdb", "numpy", "scipy",
                                    "pandas")
#: Exact versions to install in Colab.  Pinned so a re-run reproduces the pin
#: instead of silently picking up whatever the index serves that day.
PIP_INSTALL_SPEC: Tuple[str, ...] = ("neurokit2==0.2.13", "wfdb==4.3.1")
#: The packages that *are* the frozen rule.  Drift in these stops the run.
STRICT_PIN_PACKAGES: Tuple[str, ...] = ("neurokit2", "wfdb")
#: The pin baseline lives next to the run, in Drive — not hard-coded here.
#:
#: An earlier version of this module carried literal hashes measured in Colab
#: on 2026-08-10.  They were produced by a *different* traversal order than
#: :func:`hash_source_tree` uses, so every later run reported drift on wfdb,
#: numpy and scipy while the environment had not moved at all.  Hard-coding a
#: hash means hard-coding the algorithm that made it; the first run now writes
#: the baseline and later runs compare against that file.
BASELINE_FILE = "env_pin_baseline.json"

DRIVE_ASSET_REL = "MedKOS/ecg-model/assets/EXP-2026-007_prep_data"
SOURCE_SUBDIR = "source"
QUALIFY_SUBDIR = "qualify"
RUNS_SUBDIR = "runs"
MITDB_DIR = "mitdb-1.0.0"
PWAVE_DIR = "pwave-1.0.0"
PWAVE_EXT = "pwave"
ATR_EXT = "atr"

FROZEN_FILE = "frozen_constants.json"
BUNDLE_FILES: Tuple[str, ...] = (
    "config.json", "env_pin.json", FROZEN_FILE, "ds1_dry_report.csv",
    "ds1_pr_distribution.csv", "pwave_qualification.csv", "chance_null.csv",
    "decision.json", "log.txt", "summary.md",
)

#: Textual proof that this file cannot reach an outcome.  Tokens are split so
#: the table itself does not match.  Checked by :func:`assert_qualify_only`.
FORBIDDEN_TOKENS: Tuple[str, ...] = (
    "torch." + "optim", "." + "backward(", ".f" + "it(",
    "average_" + "precision", "precision_recall_" + "curve",
    "roc_auc_" + "score", "pr_" + "auc(",
    "mamba_" + "data", "v10" + "pkg", "ecg_" + "multi",
    "core_" + "membership", "probs" + ".npy", "state_" + "dict",
    "ablation_" + "step",
)


class Q5DQualifyError(RuntimeError):
    """Anything that must stop the substage rather than be worked around."""


# ─────────────────────────────────────────────────────────────────────────────
# Guards
# ─────────────────────────────────────────────────────────────────────────────
def resolve_mode(mode: str) -> str:
    """Exactly one of :data:`MODES`; a later stage names itself when refused."""
    m = str(mode).strip().upper()
    if m in FORBIDDEN_MODES:
        raise Q5DQualifyError(
            f"mode {m!r} belongs to a stage that is NOT authorised: the "
            f"approved substage is {SUBSTAGE}. The beat join and the "
            f"association analysis need their own approval.")
    if m not in MODES:
        raise Q5DQualifyError(f"mode must be one of {MODES}, got {mode!r}")
    return m


def assert_qualify_only(path: Optional[str] = None) -> Dict[str, object]:
    """Evidence that this file trains nothing and scores no model.

    Textual on purpose: the cheapest artifact a reviewer can re-run.  Comment
    lines and the token table itself are skipped.
    """
    path = path or os.path.abspath(__file__)
    with open(path, "r", encoding="utf-8") as fh:
        lines = fh.readlines()
    hits: List[Dict[str, object]] = []
    for i, line in enumerate(lines, 1):
        stripped = line.lstrip()
        if stripped.startswith("#") or '" + "' in line:
            continue
        low = line.lower()
        for tok in FORBIDDEN_TOKENS:
            if tok.lower() in low and "assert_qualify_only" not in line:
                hits.append({"line": i, "token": tok})
    if hits:
        raise Q5DQualifyError(f"forbidden call in a qualify-only module: {hits}")
    return {"qualify_only": True, "checked_file": path,
            "tokens": list(FORBIDDEN_TOKENS), "training_performed": False,
            "model_scored": False, "ds2_outcome_opened": False}


# ─────────────────────────────────────────────────────────────────────────────
# Small numeric helpers (no numpy dependency, so the tests run anywhere)
# ─────────────────────────────────────────────────────────────────────────────
def _as_list(value) -> List:
    """Sequence -> list without ever asking a sequence whether it is truthy.

    Same lesson as the acquisition module: ``arr or []`` on a numpy array
    raises "truth value of an array ... is ambiguous", and inside a try/except
    that turns a good record into a fake failure.  Convert, never test.
    """
    if value is None:
        return []
    try:
        return list(value)
    except TypeError:
        return []


def percentile(values: Sequence[float], pct: float) -> float:
    """Linear-interpolation percentile; matches ``numpy.percentile`` default."""
    vals = sorted(float(v) for v in values if _finite(v))
    if not vals:
        return float("nan")
    if len(vals) == 1:
        return vals[0]
    pos = (len(vals) - 1) * (float(pct) / 100.0)
    lo = int(pos)
    hi = min(lo + 1, len(vals) - 1)
    frac = pos - lo
    return vals[lo] * (1.0 - frac) + vals[hi] * frac


def _finite(v) -> bool:
    try:
        f = float(v)
    except (TypeError, ValueError):
        return False
    return f == f and f not in (float("inf"), float("-inf"))


def median(values: Sequence[float]) -> float:
    vals = [float(v) for v in values if _finite(v)]
    return float(statistics.median(vals)) if vals else float("nan")


def mad(values: Sequence[float]) -> float:
    """Median absolute deviation.  Raw, not scaled to a normal sigma."""
    vals = [float(v) for v in values if _finite(v)]
    if not vals:
        return float("nan")
    med = statistics.median(vals)
    return float(statistics.median([abs(v - med) for v in vals]))


class _Rng:
    """A tiny deterministic PRNG so results do not depend on numpy's version."""

    def __init__(self, seed: int):
        self.state = (int(seed) ^ 0x5DEECE66D) & ((1 << 48) - 1)

    def next_int(self, bound: int) -> int:
        self.state = (self.state * 0x5DEECE66D + 0xB) & ((1 << 48) - 1)
        return (self.state >> 16) % max(1, int(bound))


# ─────────────────────────────────────────────────────────────────────────────
# Environment pin — recorded before any waveform is read
# ─────────────────────────────────────────────────────────────────────────────
#: Bump when :func:`hash_source_tree` changes.  A hash is only comparable to
#: another hash made by the same algorithm, so the pin carries its version and
#: a comparison across versions is refused rather than reported as drift.
HASH_ALGO_VERSION = 1


def hash_source_tree(root: str) -> Dict[str, object]:
    """SHA-256 over every ``.py`` under ``root``, in relative-path order.

    Order matters and is fixed here on purpose: hashing in ``os.walk`` order
    instead gives a different digest for the very same files, which is exactly
    how the first baseline ended up incomparable with later runs.
    """
    paths: List[str] = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if d != "__pycache__")
        for fn in sorted(filenames):
            if fn.endswith(".py"):
                paths.append(os.path.join(dirpath, fn))
    rels = sorted(os.path.relpath(p, root).replace(os.sep, "/") for p in paths)
    digest = hashlib.sha256()
    for rel in rels:
        digest.update(rel.encode("utf-8"))
        with open(os.path.join(root, rel), "rb") as fh:
            digest.update(fh.read())
    return {"source_sha256": digest.hexdigest(), "py_files": len(rels),
            "hash_algo_version": HASH_ALGO_VERSION}


def package_pin(name: str) -> Dict[str, object]:
    """Version plus a deterministic SHA-256 over the package's ``.py`` tree."""
    mod = importlib.import_module(name)
    root = os.path.dirname(os.path.abspath(mod.__file__))
    out: Dict[str, object] = {"version": str(getattr(mod, "__version__", "?"))}
    out.update(hash_source_tree(root))
    return out


def build_env_pin(timestamp: str,
                  packages: Sequence[str] = PINNED_PACKAGES) -> Dict[str, object]:
    pins: Dict[str, object] = {}
    for name in packages:
        try:
            pins[name] = package_pin(name)
        except Exception as exc:                       # noqa: BLE001
            pins[name] = {"version": None, "source_sha256": None,
                          "error": f"{type(exc).__name__}: {exc}"}
    return {"experiment_id": EXPERIMENT_ID, "arm_id": ARM_ID,
            "substage": "QUALIFY-0 ENV_PIN", "timestamp": str(timestamp),
            "waveform_read": False, "python": sys.version,
            "platform": platform.platform(), "packages": pins}


def env_pin_is_complete(pin: Dict[str, object]) -> Tuple[bool, List[str]]:
    """The delineator's own version and hash must be present, or we stop.

    Each missing entry carries *why* it is missing.  The first version of this
    returned bare names, and a plain ``['neurokit2', 'wfdb']`` reads like a
    module bug when the real cause is simply that Colab has not installed them
    yet — the reason is already in the pin, so hand it back.
    """
    pkgs = dict(pin.get("packages") or {})
    missing: List[str] = []
    for name in ("neurokit2", "wfdb"):
        entry = dict(pkgs.get(name) or {})
        if entry.get("source_sha256"):
            continue
        why = entry.get("error") or "not recorded in this pin"
        missing.append(f"{name}: {why}")
    return (not missing), missing


def env_pin_drift(pin: Dict[str, object],
                  baseline: Dict[str, object]) -> List[Dict[str, object]]:
    """Packages whose source hash differs from the baseline pin.

    Reported, never auto-corrected.  Only :data:`STRICT_PIN_PACKAGES` are
    ``blocking``: those two are version-pinned by us and they *are* the frozen
    rule, so a change there means the rule is not the one that was pinned.
    numpy and scipy ride along with whatever Colab ships; a bump there is worth
    recording, not worth refusing to start over.

    A pin made by a different :data:`HASH_ALGO_VERSION` is not comparable, and
    saying "drift" about it would be a lie about the environment.
    """
    now = dict(pin.get("packages") or {})
    was = dict(baseline.get("packages") or {})
    drift: List[Dict[str, object]] = []
    for name, old in was.items():
        old = dict(old or {})
        new = dict(now.get(name) or {})
        want, got = old.get("source_sha256"), new.get("source_sha256")
        if not want or not got or str(want) == str(got):
            continue
        if int(old.get("hash_algo_version") or 0) != \
                int(new.get("hash_algo_version") or 0):
            raise Q5DQualifyError(
                f"baseline for {name} was hashed by algorithm version "
                f"{old.get('hash_algo_version')} but this run uses "
                f"{new.get('hash_algo_version')} — the two digests are not "
                f"comparable. Re-establish the baseline instead of reading "
                f"this as environment drift.")
        drift.append({"package": name, "expected": want, "observed": got,
                      "version": new.get("version"),
                      "baseline_version": old.get("version"),
                      "py_files": new.get("py_files"),
                      "baseline_py_files": old.get("py_files"),
                      "blocking": name in STRICT_PIN_PACKAGES})
    return drift


def blocking_drift(pin: Dict[str, object],
                   baseline: Dict[str, object]) -> List[Dict[str, object]]:
    return [d for d in env_pin_drift(pin, baseline) if d["blocking"]]


def baseline_path(asset_root: str) -> str:
    return os.path.join(qualify_dir(asset_root), BASELINE_FILE)


def establish_or_check_baseline(asset_root: str, pin: Dict[str, object]
                                ) -> Dict[str, object]:
    """First run writes the baseline; later runs are compared against it."""
    path = baseline_path(asset_root)
    if not os.path.exists(path):
        _dump_json(path, pin)
        return {"created": True, "path": path, "drift": [], "blocking": []}
    with open(path, encoding="utf-8") as fh:
        base = json.load(fh)
    drift = env_pin_drift(pin, base)
    return {"created": False, "path": path, "drift": drift,
            "baseline_timestamp": base.get("timestamp"),
            "blocking": [d for d in drift if d["blocking"]]}


# ─────────────────────────────────────────────────────────────────────────────
# Reading records
# ─────────────────────────────────────────────────────────────────────────────
def _import_wfdb():
    try:
        import wfdb                                    # noqa: PLC0415
    except ImportError as exc:                         # pragma: no cover
        raise Q5DQualifyError(
            "wfdb is required. In Colab: pip install wfdb") from exc
    return wfdb


def _import_nk():
    try:
        import neurokit2                               # noqa: PLC0415
    except ImportError as exc:                         # pragma: no cover
        raise Q5DQualifyError(
            "neurokit2 is required. In Colab: pip install neurokit2") from exc
    return neurokit2


def record_base(asset_root: str, record: str, source: str = "mitdb") -> str:
    sub = MITDB_DIR if source == "mitdb" else PWAVE_DIR
    return os.path.join(asset_root, SOURCE_SUBDIR, sub, str(record))


def _beat_samples(ann, keep_symbols: bool) -> Tuple[List[int], List[str]]:
    """Beat R samples, and the symbols **only when the caller may keep them**.

    For a sealed record the symbol column is collapsed to "is this a beat" and
    the class is dropped right here, so no DS2 beat class can leave this call.
    """
    samples = _as_list(getattr(ann, "sample", None))
    symbols = _as_list(getattr(ann, "symbol", None))
    if len(symbols) != len(samples):
        raise Q5DQualifyError(
            f"annotation sample/symbol length mismatch: "
            f"{len(samples)} vs {len(symbols)}")
    out_s: List[int] = []
    out_y: List[str] = []
    for smp, sym in zip(samples, symbols):
        if str(sym) in BEAT_SYMBOLS:
            out_s.append(int(smp))
            if keep_symbols:
                out_y.append(str(sym))
    return out_s, out_y


def read_reference(asset_root: str, record: str, keep_symbols: bool,
                   wfdb_module=None) -> Dict[str, object]:
    """Channel-0 signal plus reference R samples.  R peaks are never redetected.

    ``keep_symbols`` must be False for every sealed (DS2) record.
    """
    wfdb = wfdb_module or _import_wfdb()
    base = record_base(asset_root, record, "mitdb")
    hdr = wfdb.rdheader(base)
    fs = float(getattr(hdr, "fs", 0) or 0)
    if fs != EXPECTED_FS:
        raise Q5DQualifyError(f"record {record}: fs {fs} != {EXPECTED_FS}")
    rec = wfdb.rdrecord(base, channels=[DELINEATOR_CHANNEL])
    signal = [float(row[0]) for row in _as_list(getattr(rec, "p_signal", None))]
    if not signal:
        raise Q5DQualifyError(f"record {record}: empty channel-0 signal")
    ann = wfdb.rdann(base, ATR_EXT)
    r_samples, symbols = _beat_samples(ann, keep_symbols)
    if not r_samples:
        raise Q5DQualifyError(f"record {record}: no beat annotations")
    return {"record": str(record), "fs": fs, "signal": signal,
            "r_samples": r_samples, "symbols": symbols,
            "sig_len": len(signal), "symbols_kept": bool(keep_symbols)}


def read_expert_p(asset_root: str, record: str, wfdb_module=None) -> List[int]:
    """Published expert P annotations.  This is not a DS2 outcome."""
    wfdb = wfdb_module or _import_wfdb()
    base = record_base(asset_root, record, "pwave")
    ann = wfdb.rdann(base, PWAVE_EXT)
    return sorted(int(s) for s in _as_list(getattr(ann, "sample", None)))


# ─────────────────────────────────────────────────────────────────────────────
# Delineation — one frozen rule, no sweep
# ─────────────────────────────────────────────────────────────────────────────
def delineate_p_peaks(signal: Sequence[float], r_samples: Sequence[int],
                      fs: float, nk_module=None) -> List[int]:
    """NeuroKit2 ``ecg_delineate(method="dwt")`` on channel 0, R given.

    Returns the raw P-peak sample positions.  Defaults are fixed; there is no
    parameter to tune here on purpose.
    """
    nk = nk_module or _import_nk()
    _, info = nk.ecg_delineate(list(signal), rpeaks=list(r_samples),
                               sampling_rate=float(fs),
                               method=DELINEATOR_METHOD)
    raw = _as_list((info or {}).get("ECG_P_Peaks"))
    return sorted(int(v) for v in raw if _finite(v) and int(v) >= 0)


def assign_p_to_r(p_peaks: Sequence[int], r_samples: Sequence[int], fs: float,
                  lo_ms: float = P_SEARCH_MIN_MS,
                  hi_ms: float = P_SEARCH_MAX_MS) -> Dict[int, int]:
    """One P per R inside the physiological pre-R window, nearest R wins.

    Deliberately independent of however the delineator orders or pads its
    output: a P belongs to the R it precedes by ``lo_ms..hi_ms``, and if two Ps
    land in the same window the one closest to R is kept.  Ambiguity is
    resolved, not silently dropped, so the counts stay auditable.
    """
    lo = lo_ms * fs / 1000.0
    hi = hi_ms * fs / 1000.0
    rs = sorted(int(r) for r in r_samples)
    chosen: Dict[int, int] = {}
    for p in sorted(int(v) for v in p_peaks):
        best_r = None
        best_d = None
        # rs ascends, so d = r - p ascends too: skip up to the window, stop
        # once past it.  The first R inside the window is the nearest one.
        for r in rs:
            d = r - p
            if d < lo:
                continue
            if d > hi:
                break
            best_r, best_d = r, d
            break
        if best_r is None:
            continue
        prev = chosen.get(best_r)
        if prev is None or (best_r - p) < (best_r - prev):
            chosen[best_r] = p
    return chosen


def record_pr_table(record: str, signal: Sequence[float],
                    r_samples: Sequence[int], fs: float,
                    nk_module=None) -> Dict[str, object]:
    """``PR_ms`` and ``PR_discordance`` for one record.  Label-free throughout."""
    p_peaks = delineate_p_peaks(signal, r_samples, fs, nk_module=nk_module)
    assigned = assign_p_to_r(p_peaks, r_samples, fs)
    rows: List[Dict[str, object]] = []
    pr_values: List[float] = []
    for r in sorted(int(x) for x in r_samples):
        p = assigned.get(r)
        pr_ms = (r - p) * 1000.0 / fs if p is not None else float("nan")
        if p is not None:
            pr_values.append(pr_ms)
        rows.append({"record": str(record), "r_sample": r,
                     "p_sample": (int(p) if p is not None else None),
                     "pr_ms": pr_ms, "valid": p is not None})
    med = median(pr_values)
    dev = mad(pr_values)
    for row in rows:
        if row["valid"] and _finite(med) and _finite(dev) and dev > 0:
            row["pr_discordance"] = abs(float(row["pr_ms"]) - med) / dev
        else:
            row["pr_discordance"] = float("nan")
    return {"record": str(record), "rows": rows,
            "p_peaks": p_peaks, "assigned": assigned,
            "n_beats": len(rows), "n_valid": len(pr_values),
            "median_pr_ms": med, "mad_pr_ms": dev,
            "mad_degenerate": not (_finite(dev) and dev > 0)}


# ─────────────────────────────────────────────────────────────────────────────
# RR features — from .atr R samples alone (spec: DS1 N beats only)
# ─────────────────────────────────────────────────────────────────────────────
def coupling_ratios(r_samples: Sequence[int], fs: float,
                    window: int = RR_WINDOW_BEATS) -> List[float]:
    """``pre_rr / local_median_rr`` per beat (q5a ``rr_features``, window 21)."""
    rs = sorted(int(r) for r in r_samples)
    pre = [float("nan")] + [(rs[i] - rs[i - 1]) / fs for i in range(1, len(rs))]
    half = max(1, int(window) // 2)
    out: List[float] = []
    for j in range(len(rs)):
        lo, hi = max(0, j - half), min(len(rs), j + half + 1)
        win = [v for v in pre[lo:hi] if _finite(v)]
        local = median(win) if win else float("nan")
        if _finite(pre[j]) and _finite(local) and local > 0:
            out.append(pre[j] / local)
        else:
            out.append(float("nan"))
    return out


def ds1_normal_coupling(r_samples: Sequence[int], symbols: Sequence[str],
                        fs: float) -> List[float]:
    """Coupling ratios restricted to AAMI N beats.  DS1 only, by construction."""
    if len(symbols) != len(r_samples):
        raise Q5DQualifyError("N-beat selection needs DS1 symbols")
    ratios = coupling_ratios(r_samples, fs)
    order = sorted(range(len(r_samples)), key=lambda i: int(r_samples[i]))
    return [ratios[k] for k, i in enumerate(order)
            if str(symbols[i]) in AAMI_N_SYMBOLS and _finite(ratios[k])]


# ─────────────────────────────────────────────────────────────────────────────
# Matching detections to expert annotations
# ─────────────────────────────────────────────────────────────────────────────
def match_one_to_one(detected: Sequence[int], reference: Sequence[int],
                     tol_samples: float) -> Dict[str, object]:
    """Greedy nearest 1:1 match inside ``tol_samples``.

    Greedy-by-distance with mutual exclusion is deterministic and never lets a
    detection serve two annotations, so the produced join is injective by
    construction — asserted below rather than assumed.
    """
    det = sorted(int(v) for v in detected)
    ref = sorted(int(v) for v in reference)
    pairs: List[Tuple[float, int, int]] = []
    for i, d in enumerate(det):
        for j, r in enumerate(ref):
            dist = abs(d - r)
            if dist <= tol_samples:
                pairs.append((dist, i, j))
    pairs.sort()
    used_d: Dict[int, int] = {}
    used_r: Dict[int, int] = {}
    matched: List[Tuple[int, int, float]] = []
    for dist, i, j in pairs:
        if i in used_d or j in used_r:
            continue
        used_d[i] = j
        used_r[j] = i
        matched.append((det[i], ref[j], float(dist)))
    if len(used_d) != len(used_r) or len(matched) != len(used_d):
        raise Q5DQualifyError("matcher produced a non-injective join")
    return {"matched": matched, "n_matched": len(matched),
            "n_detected": len(det), "n_reference": len(ref),
            "det_index": used_d, "ref_index": used_r,
            "detected": det, "reference": ref}


def cross_beat_violations(match: Dict[str, object], r_samples: Sequence[int],
                          assigned: Dict[int, int]) -> int:
    """Matched pairs whose detection and annotation belong to different beats.

    The detection's beat is the R it was assigned to; the annotation's beat is
    the first R at or after it.  Different R -> the join crossed a beat.
    """
    rs = sorted(int(r) for r in r_samples)
    p_to_r = {int(p): int(r) for r, p in assigned.items()}
    bad = 0
    for det, ref, _dist in match["matched"]:
        r_det = p_to_r.get(int(det))
        r_ref = None
        for r in rs:
            if r >= int(ref):
                r_ref = r
                break
        if r_det is None or r_ref is None or r_det != r_ref:
            bad += 1
    return bad


def circular_shift_chance(detected: Sequence[int], reference: Sequence[int],
                          sig_len: int, tol_samples: float, seed: int,
                          n_shift: int = N_CIRCULAR_SHIFT) -> Dict[str, object]:
    """Chance match rate from within-record circular shifts of the detections.

    Recomputed under the exact rule being evaluated, as the spec's chance-
    baseline section requires — same tolerance, same matcher.
    """
    ref = sorted(int(v) for v in reference)
    det = sorted(int(v) for v in detected)
    if not ref or not det or sig_len <= 0:
        return {"chance_rate": float("nan"), "n_shift": 0, "rates": []}
    rng = _Rng(seed)
    rates: List[float] = []
    for _ in range(int(n_shift)):
        off = rng.next_int(sig_len)
        shifted = sorted((d + off) % sig_len for d in det)
        m = match_one_to_one(shifted, ref, tol_samples)
        rates.append(m["n_matched"] / len(ref))
    return {"chance_rate": sum(rates) / len(rates), "n_shift": len(rates),
            "rates": rates}


def bootstrap_ratio_ci(per_record: Sequence[Dict[str, float]], seed: int,
                       n_boot: int = N_BOOTSTRAP) -> Dict[str, object]:
    """Record-cluster bootstrap CI for macro(true) / macro(chance).

    Records are the sampling unit — a record is drawn whole, with its true and
    chance rates together.
    """
    rows = [r for r in per_record
            if _finite(r.get("true_rate")) and _finite(r.get("chance_rate"))]
    if len(rows) < 2:
        return {"ratio": float("nan"), "ci_low": float("nan"),
                "ci_high": float("nan"), "n_boot": 0,
                "note": "fewer than 2 usable records"}
    rng = _Rng(seed)
    ratios: List[float] = []
    for _ in range(int(n_boot)):
        pick = [rows[rng.next_int(len(rows))] for _ in range(len(rows))]
        t = sum(p["true_rate"] for p in pick) / len(pick)
        c = sum(p["chance_rate"] for p in pick) / len(pick)
        ratios.append(t / c if c > 0 else float("inf"))
    finite = sorted(r for r in ratios if _finite(r))
    t0 = sum(r["true_rate"] for r in rows) / len(rows)
    c0 = sum(r["chance_rate"] for r in rows) / len(rows)
    return {"ratio": (t0 / c0 if c0 > 0 else float("inf")),
            "macro_true": t0, "macro_chance": c0,
            "ci_low": percentile(finite, 2.5) if finite else float("nan"),
            "ci_high": percentile(finite, 97.5) if finite else float("nan"),
            "n_boot": len(ratios), "n_records": len(rows),
            "n_infinite": len(ratios) - len(finite)}


# ─────────────────────────────────────────────────────────────────────────────
# Stage A — DS1 dry report and the freeze
# ─────────────────────────────────────────────────────────────────────────────
class RunLog:
    """Timestamped lines, printed and kept for ``log.txt``."""

    def __init__(self, echo: bool = True):
        self.t0 = time.time()
        self.lines: List[str] = []
        self.echo = echo

    def __call__(self, msg: str) -> None:
        line = f"[{time.time() - self.t0:7.1f}s] {msg}"
        self.lines.append(line)
        if self.echo:
            print(line, flush=True)

    def text(self) -> str:
        return "\n".join(self.lines) + "\n"


def run_ds1_freeze(asset_root: str, timestamp: str, env_pin: Dict[str, object],
                   wfdb_module=None, nk_module=None,
                   ds1_records: Sequence[str] = DS1_RECORDS,
                   expert_records: Sequence[str] = DS1_EXPERT_RECORDS,
                   log: Optional[RunLog] = None) -> Dict[str, object]:
    """DS1 dry report + the frozen constants.  Reads no DS2 record at all."""
    log = log or RunLog()
    log(NO_SCIENCE_BANNER)
    ok, missing = env_pin_is_complete(env_pin)
    if not ok:
        raise Q5DQualifyError(
            f"environment pin incomplete ({missing}); QUALIFY-0 must run and "
            f"be saved before any waveform is read")
    for rec in expert_records:
        if rec not in ds1_records:
            raise Q5DQualifyError(f"expert record {rec} is not in DS1")

    pr_rows: List[Dict[str, object]] = []
    coupling_all: List[float] = []
    per_record: List[Dict[str, object]] = []
    tol = MATCH_TOLERANCE_MS * EXPECTED_FS / 1000.0

    for k, rec in enumerate(ds1_records, 1):
        ref = read_reference(asset_root, rec, keep_symbols=True,
                             wfdb_module=wfdb_module)
        table = record_pr_table(rec, ref["signal"], ref["r_samples"],
                                ref["fs"], nk_module=nk_module)
        pr_rows.extend(table["rows"])
        coupling_all.extend(
            ds1_normal_coupling(ref["r_samples"], ref["symbols"], ref["fs"]))
        entry = {"record": rec, "n_beats": table["n_beats"],
                 "n_valid": table["n_valid"],
                 "valid_fraction": (table["n_valid"] / table["n_beats"]
                                    if table["n_beats"] else float("nan")),
                 "median_pr_ms": table["median_pr_ms"],
                 "mad_pr_ms": table["mad_pr_ms"],
                 "mad_degenerate": table["mad_degenerate"],
                 "expert_annotated": rec in expert_records,
                 "sensitivity": float("nan"), "ppv": float("nan"),
                 "ppv_ceiling": float("nan"),
                 "n_expert": 0, "n_matched": 0}
        if rec in expert_records:
            expert = read_expert_p(asset_root, rec, wfdb_module=wfdb_module)
            detected = sorted(table["assigned"].values())
            m = match_one_to_one(detected, expert, tol)
            entry.update({
                "n_expert": m["n_reference"], "n_matched": m["n_matched"],
                "n_detected": m["n_detected"],
                "sensitivity": (m["n_matched"] / m["n_reference"]
                                if m["n_reference"] else float("nan")),
                "ppv": (m["n_matched"] / m["n_detected"]
                        if m["n_detected"] else float("nan")),
                "ppv_ceiling": ppv_ceiling(m["n_reference"],
                                           m["n_detected"])})
        per_record.append(entry)
        log(f"  DS1 {rec:>4} {k:2d}/{len(ds1_records)} "
            f"beats {entry['n_beats']} · valid {entry['n_valid']}"
            + (f" · dry sens {entry['sensitivity']:.3f} "
               f"ppv {entry['ppv']:.3f}" if entry["expert_annotated"] else ""))

    discordances = [float(r["pr_discordance"]) for r in pr_rows
                    if r["valid"] and _finite(r["pr_discordance"])]
    frozen = {
        "experiment_id": EXPERIMENT_ID, "arm_id": ARM_ID,
        "substage": "QUALIFY-A DS1 FREEZE", "frozen_at": str(timestamp),
        "module_version": MODULE_VERSION, "module_build": MODULE_BUILD,
        "delineator": {"library": "neurokit2", "function": "ecg_delineate",
                       "method": DELINEATOR_METHOD,
                       "channel": DELINEATOR_CHANNEL,
                       "r_peaks": "reference .atr, never redetected"},
        "match_tolerance_ms": MATCH_TOLERANCE_MS,
        "p_search_window_ms": [P_SEARCH_MIN_MS, P_SEARCH_MAX_MS],
        "expected_fs_hz": EXPECTED_FS,
        "constants_scope": {"records": list(ds1_records),
                            "n_records": len(ds1_records),
                            "note": "DS1 22 records (user decision 2026-08-10)"},
        "rr_normal_band": [percentile(coupling_all, RR_BAND_LOW_PCTL),
                           percentile(coupling_all, RR_BAND_HIGH_PCTL)],
        "rr_band_pctl": [RR_BAND_LOW_PCTL, RR_BAND_HIGH_PCTL],
        "rr_window_beats": RR_WINDOW_BEATS,
        "rr_band_n_normal_beats": len(coupling_all),
        "discordance_threshold": percentile(discordances, DISCORDANCE_PCTL),
        "discordance_pctl": DISCORDANCE_PCTL,
        "discordance_n_valid_beats": len(discordances),
        "seeds": {"permutation_master": PERMUTATION_SEED,
                  "bootstrap_master": BOOTSTRAP_SEED},
        "gate_thresholds": {
            "macro_sensitivity_min": SENS_MACRO_MIN,
            "macro_ppv_min": PPV_MACRO_MIN,
            "per_record_min": PER_RECORD_MIN,
            "per_record_min_count": PER_RECORD_MIN_COUNT,
            "chance_ratio_min": CHANCE_RATIO_MIN,
            "chance_ci_lower_min": CHANCE_CI_LOWER_MIN},
        "env_pin": env_pin,
        "ds2_opened": False,
    }
    frozen["frozen_sha256"] = frozen_hash(frozen)
    log(f"  RR normal band {frozen['rr_normal_band']} "
        f"from {len(coupling_all)} DS1 N beats")
    log(f"  discordance threshold {frozen['discordance_threshold']:.4f} "
        f"(p{DISCORDANCE_PCTL:g} of {len(discordances)} valid DS1 beats)")
    log("  FREEZE — no constant may change after this point")
    return {"frozen": frozen, "per_record": per_record, "pr_rows": pr_rows,
            "coupling_n": len(coupling_all), "log": log}


def frozen_hash(frozen: Dict[str, object]) -> str:
    """Hash of everything except the hash field itself."""
    payload = {k: v for k, v in frozen.items() if k != "frozen_sha256"}
    blob = json.dumps(payload, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


def verify_frozen(frozen: Dict[str, object]) -> None:
    stored = str(frozen.get("frozen_sha256") or "")
    actual = frozen_hash(frozen)
    if stored != actual:
        raise Q5DQualifyError(
            "frozen_constants.json was edited after the freeze "
            f"(stored {stored[:16]}… != actual {actual[:16]}…)")


# ─────────────────────────────────────────────────────────────────────────────
# Stage B — the DS2 gate, run exactly once
# ─────────────────────────────────────────────────────────────────────────────
def run_ds2_gate(asset_root: str, timestamp: str, frozen: Dict[str, object],
                 wfdb_module=None, nk_module=None,
                 records: Sequence[str] = DS2_EXPERT_RECORDS,
                 n_shift: int = N_CIRCULAR_SHIFT, n_boot: int = N_BOOTSTRAP,
                 log: Optional[RunLog] = None) -> Dict[str, object]:
    """Qualify or refuse.  DS2 class labels are never kept (see module docstring)."""
    log = log or RunLog()
    log(NO_SCIENCE_BANNER)
    verify_frozen(frozen)
    tol_ms = float(frozen["match_tolerance_ms"])
    tol = tol_ms * EXPECTED_FS / 1000.0

    rows: List[Dict[str, object]] = []
    chance_rows: List[Dict[str, object]] = []
    for k, rec in enumerate(records, 1):
        if rec not in DS2_RECORDS:
            raise Q5DQualifyError(f"record {rec} is not a DS2 record")
        ref = read_reference(asset_root, rec, keep_symbols=False,
                             wfdb_module=wfdb_module)
        if ref["symbols"]:
            raise Q5DQualifyError(f"DS2 record {rec} leaked beat symbols")
        table = record_pr_table(rec, ref["signal"], ref["r_samples"],
                                ref["fs"], nk_module=nk_module)
        expert = read_expert_p(asset_root, rec, wfdb_module=wfdb_module)
        detected = sorted(table["assigned"].values())
        m = match_one_to_one(detected, expert, tol)
        cross = cross_beat_violations(m, ref["r_samples"], table["assigned"])
        sens = m["n_matched"] / m["n_reference"] if m["n_reference"] else float("nan")
        ppv = m["n_matched"] / m["n_detected"] if m["n_detected"] else float("nan")
        chance = circular_shift_chance(
            detected, expert, ref["sig_len"], tol,
            seed=PERMUTATION_SEED + int(rec), n_shift=n_shift)
        rows.append({"record": rec, "n_beats": table["n_beats"],
                     "n_valid_pr": table["n_valid"],
                     "n_detected": m["n_detected"],
                     "n_expert": m["n_reference"],
                     "n_matched": m["n_matched"],
                     "sensitivity": sens, "ppv": ppv,
                     "ppv_ceiling": ppv_ceiling(m["n_reference"],
                                                m["n_detected"]),
                     "ppv_vs_ceiling": (
                         ppv / ppv_ceiling(m["n_reference"], m["n_detected"])
                         if ppv_ceiling(m["n_reference"], m["n_detected"])
                         else float("nan")),
                     "cross_beat_joins": cross,
                     "many_to_one_joins": 0,
                     "chance_rate": chance["chance_rate"],
                     "true_rate": sens})
        chance_rows.append({"record": rec, "n_shift": chance["n_shift"],
                            "chance_rate": chance["chance_rate"],
                            "true_rate": sens})
        log(f"  DS2 {rec:>4} {k}/{len(records)} sens {sens:.3f} · "
            f"ppv {ppv:.3f} · cross-beat {cross} · "
            f"chance {chance['chance_rate']:.4f}")

    boot = bootstrap_ratio_ci(
        [{"true_rate": r["true_rate"], "chance_rate": r["chance_rate"]}
         for r in rows], seed=BOOTSTRAP_SEED, n_boot=n_boot)
    decision = evaluate_gate(rows, boot)
    log(f"decision: {decision['decision']} "
        f"({decision['n_gate_pass']}/{decision['n_gate_total']} gates)")
    return {"decision": decision, "rows": rows, "chance_rows": chance_rows,
            "bootstrap": boot, "log": log, "timestamp": str(timestamp)}


def ppv_ceiling(n_expert: int, n_detected: int) -> float:
    """The largest PPV a perfect delineator could reach on this record.

    A one-to-one match cannot produce more true positives than there are
    expert annotations, so ``PPV <= n_expert / n_detected``.  The published
    resource does not label every P wave, so on a record with more beats than
    annotations this ceiling sits well below 1.0 and a detection on an
    unlabelled beat is scored as a false positive no matter how correct it is.

    Descriptive only — the gate is evaluated on the measured PPV, unchanged.
    """
    if not n_detected:
        return float("nan")
    return min(1.0, float(n_expert) / float(n_detected))


def _macro(rows: Sequence[Dict[str, object]], key: str) -> float:
    vals = [float(r[key]) for r in rows if _finite(r.get(key))]
    return sum(vals) / len(vals) if vals else float("nan")


def evaluate_gate(rows: Sequence[Dict[str, object]],
                  boot: Dict[str, object]) -> Dict[str, object]:
    """The five spec conditions.  All true, or ``MEASUREMENT_UNQUALIFIED``."""
    macro_sens = _macro(rows, "sensitivity")
    macro_ppv = _macro(rows, "ppv")
    n_ok = len([r for r in rows
                if _finite(r.get("sensitivity")) and _finite(r.get("ppv"))
                and float(r["sensitivity"]) >= PER_RECORD_MIN
                and float(r["ppv"]) >= PER_RECORD_MIN])
    n_cross = sum(int(r.get("cross_beat_joins", 0)) for r in rows)
    n_multi = sum(int(r.get("many_to_one_joins", 0)) for r in rows)
    ratio = float(boot.get("ratio", float("nan")))
    ci_low = float(boot.get("ci_low", float("nan")))

    gates = [
        {"gate": "ds2_macro_sensitivity",
         "pass": _finite(macro_sens) and macro_sens >= SENS_MACRO_MIN,
         "detail": f"record-macro P-peak sensitivity {macro_sens:.4f} "
                   f"(>= {SENS_MACRO_MIN})"},
        {"gate": "ds2_macro_ppv",
         "pass": _finite(macro_ppv) and macro_ppv >= PPV_MACRO_MIN,
         "detail": f"record-macro PPV {macro_ppv:.4f} (>= {PPV_MACRO_MIN})"},
        {"gate": "ds2_per_record_floor",
         "pass": n_ok >= PER_RECORD_MIN_COUNT,
         "detail": f"{n_ok}/{len(rows)} record(s) with sensitivity and PPV "
                   f">= {PER_RECORD_MIN} (need {PER_RECORD_MIN_COUNT})"},
        {"gate": "ds2_join_integrity",
         "pass": n_cross == 0 and n_multi == 0,
         "detail": f"{n_multi} many-to-one and {n_cross} cross-beat join(s); "
                   f"both must be 0"},
        {"gate": "ds2_above_chance",
         "pass": (_finite(ratio) and ratio >= CHANCE_RATIO_MIN
                  and _finite(ci_low) and ci_low > CHANCE_CI_LOWER_MIN),
         "detail": f"true/chance match rate {ratio:.3f}x "
                   f"(>= {CHANCE_RATIO_MIN}x), record-bootstrap 95% CI lower "
                   f"bound {ci_low:.3f}x (> {CHANCE_CI_LOWER_MIN}x)"},
    ]
    failed = [g for g in gates if not g["pass"]]
    qualified = not failed
    return {
        "experiment_id": EXPERIMENT_ID, "arm_id": ARM_ID, "substage": SUBSTAGE,
        "decision": DECISION_QUALIFIED if qualified else DECISION_UNQUALIFIED,
        "decision_is_scientific_result": False,
        "training_performed": False,
        "model_scored": False,
        "ds2_outcome_opened": False,
        "association_performed": False,
        "gates": gates,
        "n_gate_pass": len(gates) - len(failed), "n_gate_total": len(gates),
        "first_stopping_reason": (failed[0]["gate"] if failed else None),
        "macro_sensitivity": macro_sens, "macro_ppv": macro_ppv,
        "macro_ppv_ceiling": _macro(rows, "ppv_ceiling"),
        "macro_ppv_vs_ceiling": _macro(rows, "ppv_vs_ceiling"),
        "chance_ratio": ratio, "chance_ci_low": ci_low,
        "chance_ci_high": float(boot.get("ci_high", float("nan"))),
        "n_records": len(rows),
        "limitation": (
            "The published resource does not guarantee that every P wave is "
            "labelled, so a missed match may be an unlabelled beat rather "
            "than a delineator failure. Where a record carries fewer "
            "annotations than detections, PPV is capped at "
            "n_expert/n_detected ('ppv_ceiling') however correct the "
            "detections are; 'ppv_vs_ceiling' says how much of the reachable "
            "PPV was actually reached. Reported, not corrected for: the gate "
            "is evaluated on the measured PPV against the frozen 0.80 "
            "threshold, which was set with this caveat already on record "
            "(spec, qualification gate item 5)."),
        "permitted_next_step": (
            "report this qualification bundle and STOP. The beat join and the "
            "association analysis need a separate approval — nothing after "
            "QUALIFY runs automatically."
            if qualified else
            "MEASUREMENT_UNQUALIFIED is a complete result. Do not widen the "
            "window, change the delineator, pick another lead, or exclude "
            "records by hand inside this experiment."),
    }


# ─────────────────────────────────────────────────────────────────────────────
# Bundle
# ─────────────────────────────────────────────────────────────────────────────
def qualify_dir(asset_root: str) -> str:
    return os.path.join(asset_root, QUALIFY_SUBDIR)


def _dump_json(path: str, payload) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2, ensure_ascii=False, default=str)


def _dump_csv(path: str, rows: Sequence[Dict[str, object]],
              columns: Sequence[str]) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(",".join(columns) + "\n")
        for row in rows:
            vals = []
            for c in columns:
                v = row.get(c, "")
                vals.append("" if v is None else str(v))
            fh.write(",".join(vals) + "\n")


def build_config(mode: str) -> Dict[str, object]:
    return {"experiment_id": EXPERIMENT_ID, "arm_id": ARM_ID,
            "substage": SUBSTAGE, "mode": mode,
            "module_version": MODULE_VERSION, "module_build": MODULE_BUILD,
            "banner": NO_SCIENCE_BANNER,
            "ds1_records": list(DS1_RECORDS),
            "ds1_expert_records": list(DS1_EXPERT_RECORDS),
            "ds2_expert_records": list(DS2_EXPERT_RECORDS),
            "delineator_method": DELINEATOR_METHOD,
            "delineator_channel": DELINEATOR_CHANNEL,
            "match_tolerance_ms": MATCH_TOLERANCE_MS,
            "p_search_window_ms": [P_SEARCH_MIN_MS, P_SEARCH_MAX_MS],
            "bundle_files": list(BUNDLE_FILES),
            "guard": assert_qualify_only()}


DS1_COLUMNS = ("record", "n_beats", "n_valid", "valid_fraction",
               "median_pr_ms", "mad_pr_ms", "mad_degenerate",
               "expert_annotated", "n_expert", "n_detected", "n_matched",
               "sensitivity", "ppv", "ppv_ceiling")
PR_COLUMNS = ("record", "r_sample", "p_sample", "pr_ms", "valid",
              "pr_discordance")
DS2_COLUMNS = ("record", "n_beats", "n_valid_pr", "n_detected", "n_expert",
               "n_matched", "sensitivity", "ppv", "ppv_ceiling",
               "ppv_vs_ceiling", "many_to_one_joins", "cross_beat_joins",
               "true_rate", "chance_rate")
CHANCE_COLUMNS = ("record", "n_shift", "true_rate", "chance_rate")


def write_bundle(asset_root: str, timestamp: str, mode: str,
                 frozen: Dict[str, object],
                 ds1: Optional[Dict[str, object]],
                 ds2: Optional[Dict[str, object]],
                 log: RunLog) -> Dict[str, object]:
    """Write ``qualify/`` and archive an immutable copy under ``runs/<ts>/``."""
    root = qualify_dir(asset_root)
    _dump_json(os.path.join(root, "config.json"), build_config(mode))
    _dump_json(os.path.join(root, "env_pin.json"), frozen.get("env_pin", {}))
    _dump_json(os.path.join(root, FROZEN_FILE), frozen)
    if ds1 is not None:
        _dump_csv(os.path.join(root, "ds1_dry_report.csv"),
                  ds1["per_record"], DS1_COLUMNS)
        _dump_csv(os.path.join(root, "ds1_pr_distribution.csv"),
                  ds1["pr_rows"], PR_COLUMNS)
    if ds2 is not None:
        _dump_csv(os.path.join(root, "pwave_qualification.csv"),
                  ds2["rows"], DS2_COLUMNS)
        _dump_csv(os.path.join(root, "chance_null.csv"),
                  ds2["chance_rows"], CHANCE_COLUMNS)
        _dump_json(os.path.join(root, "decision.json"), ds2["decision"])
        summary = render_summary(ds2["decision"], ds2["rows"], frozen)
    else:
        _dump_json(os.path.join(root, "decision.json"),
                   {"decision": DECISION_NOT_RUN,
                    "detail": "DS1 constants frozen; the DS2 gate has not run"})
        summary = ("# EXP-2026-007 / Q5-D QUALIFY\n\n"
                   f"- {DECISION_NOT_RUN} — DS1 constants are frozen, the DS2 "
                   "gate has not run yet.\n")
    with open(os.path.join(root, "summary.md"), "w", encoding="utf-8") as fh:
        fh.write(summary)
    with open(os.path.join(root, "log.txt"), "w", encoding="utf-8") as fh:
        fh.write(log.text())
    run_dir = _archive_run(root, timestamp)
    return {"qualify_dir": root, "run_dir": run_dir}


def _archive_run(root: str, timestamp: str) -> Optional[str]:
    """One immutable copy per run.  An archived run is never overwritten."""
    if not timestamp:
        return None
    run_dir = os.path.join(root, RUNS_SUBDIR, str(timestamp))
    if os.path.isdir(run_dir):
        return run_dir
    os.makedirs(run_dir, exist_ok=True)
    import shutil                                       # noqa: PLC0415
    for name in BUNDLE_FILES:
        src = os.path.join(root, name)
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(run_dir, name))
    return run_dir


def report_bundle(asset_root: str) -> Dict[str, object]:
    """Replay what was saved.  Nothing is recomputed here."""
    root = qualify_dir(asset_root)
    out: Dict[str, object] = {"qualify_dir": root, "recomputed": False}
    missing = [f for f in BUNDLE_FILES
               if not os.path.exists(os.path.join(root, f))]
    out["missing_files"] = missing
    runs = os.path.join(root, RUNS_SUBDIR)
    out["archived_runs"] = sorted(os.listdir(runs)) if os.path.isdir(runs) else []
    dec_path = os.path.join(root, "decision.json")
    if not os.path.exists(dec_path):
        out["decision"] = DECISION_NOT_RUN
        out["reason"] = "no decision.json"
        return out
    with open(dec_path, encoding="utf-8") as fh:
        decision = json.load(fh)
    out["decision"] = decision.get("decision", DECISION_NOT_RUN)
    out["decision_detail"] = decision
    sm = os.path.join(root, "summary.md")
    if os.path.exists(sm):
        with open(sm, encoding="utf-8") as fh:
            out["summary"] = fh.read()
    return out


# ─────────────────────────────────────────────────────────────────────────────
# Cards
# ─────────────────────────────────────────────────────────────────────────────
def design_card(asset_root: str, mode: str) -> str:
    w = 72
    L = ["=" * w, f"  {EXPERIMENT_ID} / {ARM_ID} — {SUBSTAGE}",
         "  NO TRAINING / NO SCIENTIFIC ANALYSIS", "=" * w,
         f"  mode           : {mode}",
         f"  asset root     : {asset_root}",
         f"  delineator     : neurokit2 ecg_delineate(method="
         f"{DELINEATOR_METHOD!r}) · channel {DELINEATOR_CHANNEL} · "
         f"R from .atr (never redetected)",
         f"  P search window: {P_SEARCH_MIN_MS:g}–{P_SEARCH_MAX_MS:g} ms before R",
         f"  match tolerance: ±{MATCH_TOLERANCE_MS:g} ms, one-to-one",
         f"  DS1 constants  : {len(DS1_RECORDS)} records "
         f"(RR band p{RR_BAND_LOW_PCTL:g}–p{RR_BAND_HIGH_PCTL:g} of N-beat "
         f"coupling · discordance p{DISCORDANCE_PCTL:g})",
         f"  DS1 expert     : {' '.join(DS1_EXPERT_RECORDS)}",
         f"  DS2 expert     : {' '.join(DS2_EXPERT_RECORDS)}  (gate, once)",
         "  sealed         : DS2 class labels · V10 probabilities · processed "
         "beat arrays",
         "  NOT performed  : beat join · P-to-R association · S PR-AUC · "
         "SHAM · training",
         f"  decisions      : {' | '.join(DECISIONS)}",
         "-" * w,
         "  gate (all five, or MEASUREMENT_UNQUALIFIED)",
         f"   1) DS2 record-macro sensitivity >= {SENS_MACRO_MIN}",
         f"   2) DS2 record-macro PPV >= {PPV_MACRO_MIN}",
         f"   3) >= {PER_RECORD_MIN_COUNT}/6 records with both >= {PER_RECORD_MIN}",
         "   4) no many-to-one and no cross-beat join",
         f"   5) >= {CHANCE_RATIO_MIN:g}x chance, bootstrap CI lower bound "
         f"> {CHANCE_CI_LOWER_MIN:g}x",
         "=" * w]
    return "\n".join(L)


def render_gate_card(decision: Dict[str, object],
                     rows: Optional[Sequence[Dict[str, object]]] = None) -> str:
    w = 72
    L = ["=" * w, f"  {EXPERIMENT_ID} / {ARM_ID} — {SUBSTAGE}",
         f"  DECISION: {decision.get('decision', DECISION_NOT_RUN)}", "=" * w]
    for r in (rows or []):
        L.append(f"  {str(r['record']):>4}  sens {float(r['sensitivity']):.3f} · "
                 f"ppv {float(r['ppv']):.3f} · matched {r['n_matched']}"
                 f"/{r['n_expert']} · cross-beat {r['cross_beat_joins']}")
    if not rows:
        L.append("  (저장된 판정만 읽었다 — 집계는 아래 gate 표가 원본이다)")
    L.append("-" * w)
    for g in decision.get("gates", []):
        L.append(f"  [{'PASS' if g['pass'] else 'FAIL'}] {g['gate']}: "
                 f"{g['detail']}")
    L.append("-" * w)
    if decision.get("first_stopping_reason"):
        L.append(f"  first stopping reason: {decision['first_stopping_reason']}")
    L.append("  " + str(decision.get("permitted_next_step", "")))
    L.append("=" * w)
    return "\n".join(L)


def render_summary(decision: Dict[str, object],
                   rows: Sequence[Dict[str, object]],
                   frozen: Dict[str, object]) -> str:
    L = [f"# {EXPERIMENT_ID} / {ARM_ID} — QUALIFY", "",
         "- **NO TRAINING / NO SCIENTIFIC ANALYSIS**",
         f"- 판정: **{decision['decision']}** "
         f"({decision['n_gate_pass']}/{decision['n_gate_total']} gate pass)",
         "- 이 판정은 **측정도구 자격검증 결과**이고 "
         f"{EXPERIMENT_ID}의 과학적 판정이 아니다.", "",
         "## Frozen rule", "",
         f"- neurokit2 `ecg_delineate(method=\"{DELINEATOR_METHOD}\")` · "
         f"channel {DELINEATOR_CHANNEL} · R from `.atr`",
         f"- P search {P_SEARCH_MIN_MS:g}–{P_SEARCH_MAX_MS:g} ms · "
         f"match ±{MATCH_TOLERANCE_MS:g} ms one-to-one",
         f"- RR normal band `{frozen.get('rr_normal_band')}` · "
         f"discordance threshold `{frozen.get('discordance_threshold')}`",
         f"- frozen sha256 `{frozen.get('frozen_sha256')}`", "",
         "## DS2 per record", ""]
    for r in rows:
        L.append(f"- `{r['record']}` sensitivity {float(r['sensitivity']):.4f} · "
                 f"PPV {float(r['ppv']):.4f} · matched {r['n_matched']}"
                 f"/{r['n_expert']} · cross-beat {r['cross_beat_joins']} · "
                 f"chance {float(r['chance_rate']):.4f}")
    L += ["", "## Gate", ""]
    for g in decision.get("gates", []):
        L.append(f"- {'PASS' if g['pass'] else 'FAIL'} `{g['gate']}` — "
                 f"{g['detail']}")
    L += ["", "## 한계", "", f"- {decision.get('limitation', '')}",
          "", "## 다음 단계", "", f"- {decision.get('permitted_next_step', '')}",
          "- beat join · P-to-R · S PR-AUC · SHAM · 학습은 이 단계에서 "
          "**하지 않았다**.", ""]
    return "\n".join(L)


# ─────────────────────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────────────────────
def main(argv: Optional[Sequence[str]] = None) -> int:
    ap = argparse.ArgumentParser(description=NO_SCIENCE_BANNER)
    ap.add_argument("--mode", default="DESIGN")
    ap.add_argument("--asset-root", default="")
    ap.add_argument("--self-check", action="store_true")
    args = ap.parse_args(list(argv) if argv is not None else None)

    if args.self_check:
        print(json.dumps(assert_qualify_only(), indent=2, ensure_ascii=False))
        print(f"DS1 expert {DS1_EXPERT_RECORDS} · DS2 expert {DS2_EXPERT_RECORDS}")
        return 0
    mode = resolve_mode(args.mode)
    if mode == "DESIGN":
        print(design_card(args.asset_root or "<asset root>", mode))
        return 0
    if not args.asset_root:
        raise SystemExit("--asset-root is required outside DESIGN")
    if mode == "QUALIFY_REPORT":
        print(json.dumps(report_bundle(args.asset_root), indent=2,
                         ensure_ascii=False, default=str))
        return 0
    raise SystemExit(
        f"mode {mode} runs in Colab against Drive; the CLI covers DESIGN, "
        f"QUALIFY_REPORT and --self-check only")


if __name__ == "__main__":                              # pragma: no cover
    raise SystemExit(main())
