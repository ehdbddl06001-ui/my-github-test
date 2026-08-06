#!/usr/bin/env python3
"""EXP-2026-001 / Q4-O — leakage-free morphology baseline + current-beat raw-CNN residual.

Spec: ``experiments/specs/EXP-2026-001-q4o-leakage-free-residual-cnn.md``

What this module is for
-----------------------
Q4-N (branch ``claude/ai-model-ecg-diagnosis-6v8hof-5v35t1``, commit ``acbafb5``)
built the residual CNN's offset with::

    def cpu_fold(X):
        sc = np.full(len(K), np.nan)
        for f in range(DL_FOLDS):
            ...
            sc[tr] = lr.decision_function((X[tr] - mu) / sd)   # in-sample, overwrites
            sc[te] = lr.decision_function((X[te] - mu) / sd)
        return sc

Both train and test positions of one shared array are written, and the five folds run
in sequence, so after the last fold roughly 80% of ``sc`` holds in-sample predictions.
``cpu_comb = 0.8445``, ``boost_fix = 0.8631``, and ``boost_rank = 0.8492`` are scored
on (or trained against) that array and are therefore **not** baselines. They are kept
here only as ``REF_Q4N`` contaminated reference values for the Arm E diagnostic.

This module keeps the morphology feature definition frozen verbatim from Q4-N and
re-asks the complementarity question with a genuinely cross-fitted offset.

Arms
----
A ``morph_baseline``           frozen Q4-N morphology logistic, outer-train fit only
B ``raw_current_cnn``          current beat, two leads, nothing else
C ``morph_plus_raw_residual``  ``logit = morph_offset + alpha * cnn_residual``  (primary)
D ``shuffled_waveform_control``  Arm C with within-record waveform permutation
E ``corrected_q4n_diagnostic`` Q4-N ``boost_fix`` structure, offset de-contaminated

Nothing in this file declares an experiment successful. Gate evaluation is computed
from measured arrays only, and every reported number comes out of an executed run.

Commands
--------
    python mit-bih/test_q4o_leakage_free_residual.py
    python mit-bih/q4o_leakage_free_residual.py --smoke --out /tmp/q4o_smoke
    python mit-bih/q4o_leakage_free_residual.py --data <svdb_data5.npz> --out <run_dir>
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import subprocess
import sys
import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np

# ─────────────────────────────────────────────────────────────────────────────
# Frozen constants — copied verbatim from Q4-N. Do not retune inside this run.
# ─────────────────────────────────────────────────────────────────────────────
EXPERIMENT_ID = "EXP-2026-001"
ARM_ID = "Q4-O"
RUN_SLUG = "q4o_leakage_free_residual_cnn"

# Bumped whenever a fix changes runtime behaviour. Colab keeps an imported module in
# sys.modules across cell re-runs, so `git pull` alone does NOT update the code the
# kernel executes — and running the test script as a subprocess passes against the new
# file while the kernel still runs the old one. The notebook asserts this value and
# calls self_check() in-process so a stale import fails at cell 1, loudly.
MODULE_VERSION = 3
MODULE_BUILD = ("2026-08-06 q4o.3 — reporting layer (presentation only) "
                "+ training history; q4o.2 scoped the OOF audit to the scorable cohort")

SEED0 = 20260806
IDX_S = 1                       # y3 == 1 is the S (SVEB) class
FS = 360.0
R_IDX = 100

RHY_K = (5, 10, 20, 32)         # local RR baseline windows
MIN_S, MIN_N = 25, 25           # a record is scorable only with >=25 S and >=25 non-S
DEV_EVERY = 4                   # early-stopping dev records: every 4th of outer-train

K_SWEEP = (50, 100, 200, 300)   # primary metric = mean achievement over these k
K_OP = (30, 50)                 # secondary operating points
MAIN_K = 300

W_P_S = (20, 88)
W_T_S = (135, 265)
W_Q_S = (72, 148)
FRAC_QRS, FRAC_P, FRAC_T = 0.10, 0.25, 0.25
LAG = 30
P_CORR_MIN = 0.35
P_GAP = 4
P_NULL_Q = 0.95
TMPL_LO, TMPL_HI, TMPL_MIN = 0.92, 1.08, 30
PT_LO_F, PT_HI_F, PT_NRS = 0.35, 0.95, 32
AXIS_DEG = 30.0

# ── Q4-O protocol knobs (pre-registered in the spec) ─────────────────────────
N_OUTER_FOLDS = 5
N_INNER_FOLDS = 5
TRAIN_SEEDS = (20260806, 20260807, 20260808, 20260809, 20260810)
PERM_SEED = 20261797            # Arm D waveform permutation; never a model seed

DL_BATCH = 1024
DL_EMB = 16
DL_WD = 1e-4
DL_EPOCH = 12
DL_LR = 1e-3
DL_PATIENCE = 3                 # early stopping on outer-train dev records only
DL_MIN_EPOCH = 4                # early stopping cannot fire before this epoch.
                                # alpha starts at exactly 0, so epoch 0's dev loss is
                                # the baseline's. Without a warmup the patience counter
                                # can end training before alpha has left zero, which
                                # would make the arm untestable rather than merely
                                # unhelpful. Decided a priori, not from any result.
NB_BOOT = 2000

# ── Acceptance gates (pre-registered; never changed after seeing results) ────
GATE_MIN_GAIN = 0.015
GATE_MIN_SEED_AGREE = 4
GATE_LOWER_TAIL_MAX_DROP = 0.01
MORPH_PORT_TOL = 0.005          # |Arm A LORO ksw - 0.8361| tolerance for port check

ARM_A, ARM_B = "morph_baseline", "raw_current_cnn"
ARM_C, ARM_D = "morph_plus_raw_residual", "shuffled_waveform_control"
ARM_E = "corrected_q4n_diagnostic"
ARMS = (ARM_A, ARM_B, ARM_C, ARM_D, ARM_E)

REQUIRED_NPZ_KEYS = ("pid", "y3", "pre_rr", "post_rr", "beat", "sym")

# Q4-N reported values. CONTAMINATED — see the module docstring and the spec's
# Decision log. Present only for the Arm E diagnostic contrast.
REF_Q4N = {
    "morph_ksw_loro": 0.8361,       # from the unaffected loro() path
    "contaminated": {
        "cpu_comb": 0.8445,
        "boost_fix": 0.8631,
        "boost_rank": 0.8492,
    },
    "note": (
        "cpu_comb/boost_fix/boost_rank were computed with an offset array that is "
        "~80% in-sample (cpu_fold overwrote sc[tr] each fold). They are not baselines."
    ),
}

REQUIRED_BUNDLE_FILES = (
    "config.json", "manifest.json", "result.json", "log.txt",
    "fold_map.json", "predictions.npz",
)


class Q4OError(RuntimeError):
    """Raised when an input, an assertion, or an artifact contract is violated."""


# ─────────────────────────────────────────────────────────────────────────────
# Logging
# ─────────────────────────────────────────────────────────────────────────────
class RunLog:
    """Collects log lines and mirrors them to stdout."""

    def __init__(self, echo: bool = True) -> None:
        self.lines: List[str] = []
        self.echo = echo
        self.t0 = time.time()

    def __call__(self, msg: str = "") -> None:
        line = f"[{time.time() - self.t0:7.1f}s] {msg}" if msg else ""
        self.lines.append(line)
        if self.echo:
            print(line, flush=True)

    def text(self) -> str:
        return "\n".join(self.lines) + "\n"


# ─────────────────────────────────────────────────────────────────────────────
# Data loading and provenance
# ─────────────────────────────────────────────────────────────────────────────
def sha256_file(path: str, chunk: int = 1 << 20) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        while True:
            b = fh.read(chunk)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def git_commit_sha(repo_root: Optional[str] = None) -> str:
    root = repo_root or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    try:
        out = subprocess.run(["git", "-C", root, "rev-parse", "HEAD"],
                             capture_output=True, text=True, timeout=20)
        return out.stdout.strip() if out.returncode == 0 else "unavailable"
    except Exception as exc:                                  # pragma: no cover
        return f"unavailable ({exc})"


def package_versions() -> Dict[str, str]:
    vers = {"python": sys.version.split()[0], "platform": platform.platform()}
    for name in ("numpy", "scipy", "sklearn", "pandas", "torch", "matplotlib"):
        try:
            mod = __import__(name)
            vers[name] = str(getattr(mod, "__version__", "unknown"))
        except Exception:
            vers[name] = "not installed"
    return vers


def gpu_info() -> Dict[str, object]:
    info: Dict[str, object] = {"cuda_available": False, "device_name": None,
                              "cuda_version": None, "device_count": 0}
    try:
        import torch
        info["cuda_available"] = bool(torch.cuda.is_available())
        info["cuda_version"] = getattr(torch.version, "cuda", None)
        if torch.cuda.is_available():
            info["device_count"] = int(torch.cuda.device_count())
            info["device_name"] = torch.cuda.get_device_name(0)
    except Exception as exc:
        info["error"] = str(exc)
    return info


@dataclass
class Cohort:
    """Beat-level cohort. Arrays are aligned; index 0..n-1 is the sample order."""

    beat: np.ndarray            # (n, n_lead, width) float32
    y: np.ndarray               # (n,) bool — True == S class
    y3: np.ndarray              # (n,) int   — original 3-class label
    pre: np.ndarray             # (n,) float — previous RR, seconds
    post: np.ndarray            # (n,) float — next RR, seconds
    rid: np.ndarray             # (n,) int   — record / patient id
    sym: np.ndarray             # (n,) <U2   — annotation symbol; diagnostics only
    sample_id: np.ndarray       # (n,) int   — row index into the source npz
    records: np.ndarray         # (n_rec,) sorted unique record ids
    idx_of: Dict[int, np.ndarray]

    @property
    def n(self) -> int:
        return int(len(self.y))

    @property
    def n_lead(self) -> int:
        return int(self.beat.shape[1])

    @property
    def width(self) -> int:
        return int(self.beat.shape[2])


def load_cohort(npz_path: str) -> Tuple[Cohort, Dict[str, object]]:
    """Load ``svdb_data5.npz``. Refuses any file missing the Q4-N keys.

    ``svdb_data.npz`` is a different, older file (no ``y3``, no ``sym``) and must not
    be substituted for it — the key check below is what enforces that.
    """
    if not os.path.exists(npz_path):
        raise Q4OError(f"data file not found: {npz_path}")
    data = np.load(npz_path, allow_pickle=True)
    missing = [k for k in REQUIRED_NPZ_KEYS if k not in data.files]
    if missing:
        raise Q4OError(
            f"{os.path.basename(npz_path)} is missing required key(s) {missing}. "
            f"Q4-O requires svdb_data5.npz (keys {list(REQUIRED_NPZ_KEYS)}); "
            f"svdb_data.npz is a different file and must not be substituted."
        )

    pid = np.asarray(data["pid"]).astype(int)
    y3 = np.asarray(data["y3"]).astype(int)
    keep = np.where(y3 >= 0)[0]

    beat = np.asarray(np.asarray(data["beat"])[keep], dtype="float32")
    cohort = Cohort(
        beat=beat,
        y=(y3[keep] == IDX_S),
        y3=y3[keep],
        pre=np.asarray(data["pre_rr"], float)[keep],
        post=np.asarray(data["post_rr"], float)[keep],
        rid=pid[keep],
        sym=np.asarray(data["sym"]).astype("<U2")[keep],
        sample_id=keep.astype(np.int64),
        records=np.array(sorted(set(pid[keep].tolist())), dtype=int),
        idx_of={},
    )
    cohort.idx_of = {int(r): np.where(cohort.rid == r)[0] for r in cohort.records}

    if cohort.width <= W_T_S[1]:
        raise Q4OError(f"beat width {cohort.width} is shorter than the T window {W_T_S}")

    provenance = {
        "abs_path": os.path.abspath(npz_path),
        "file_name": os.path.basename(npz_path),
        "sha256": sha256_file(npz_path),
        "size_bytes": int(os.path.getsize(npz_path)),
        "arrays": {k: {"shape": list(np.asarray(data[k]).shape),
                       "dtype": str(np.asarray(data[k]).dtype)} for k in REQUIRED_NPZ_KEYS},
        "n_sample_total": int(len(y3)),
        "n_sample_labelled": cohort.n,
        "n_class": int(len(np.unique(cohort.y3))),
        "class_counts": {int(c): int((cohort.y3 == c).sum())
                         for c in np.unique(cohort.y3)},
        "n_record": int(len(cohort.records)),
        "n_patient": int(len(cohort.records)),
        "record_equals_patient": True,
        "n_lead": cohort.n_lead,
        "beat_width": cohort.width,
        "beat_dtype": str(cohort.beat.dtype),
    }
    return cohort, provenance


# ─────────────────────────────────────────────────────────────────────────────
# Feature pipeline — FROZEN. Ported verbatim from Q4-N; do not redefine here.
# ─────────────────────────────────────────────────────────────────────────────
def corr_to(x: np.ndarray, t: np.ndarray) -> np.ndarray:
    xc = x - x.mean(-1, keepdims=True)
    tc = t - t.mean(-1, keepdims=True)
    return (xc * tc).sum(-1) / (np.sqrt((xc ** 2).sum(-1) * (tc ** 2).sum(-1)) + 1e-9)


def peak_of(x: np.ndarray, lo: int, hi: int, base: float) -> Tuple[int, float]:
    seg = np.abs(x[lo:hi] - base)
    k = int(np.argmax(seg))
    return lo + k, float(seg[k])


def cross_span(x: np.ndarray, lo: int, hi: int, frac: float, base: float):
    """First-to-last threshold crossing. Correct for multiphasic QRS."""
    seg = np.abs(x[lo:hi] - base)
    amp = float(seg.max())
    if amp <= 1e-9:
        return lo, hi - 1, amp
    w = np.where(seg > frac * amp)[0]
    return lo + int(w[0]), lo + int(w[-1]), amp


def peak_span(x: np.ndarray, lo: int, hi: int, frac: float, base: float):
    """Contiguous growth outward from the peak. Correct for monophasic P and T."""
    seg = np.abs(x[lo:hi] - base)
    k = int(np.argmax(seg))
    amp = float(seg[k])
    if amp <= 1e-9:
        return lo, hi - 1, amp
    m = seg > frac * amp
    i = k
    while i > 0 and m[i - 1]:
        i -= 1
    j = k
    while j < len(m) - 1 and m[j + 1]:
        j += 1
    return lo + i, lo + j, amp


def cross_span_batch(B: np.ndarray, lo: int, hi: int, frac: float, base: np.ndarray):
    seg = np.abs(B[:, :, lo:hi] - base[:, :, None])
    amp = seg.max(-1)
    m = seg > frac * amp[..., None]
    first = m.argmax(-1)
    last = m.shape[-1] - 1 - m[:, :, ::-1].argmax(-1)
    w = np.where(m.any(-1), last - first + 1, 0)
    return w.astype(float), amp, first + lo, last + lo


def peak_span_batch(B: np.ndarray, lo: int, hi: int, frac: float, base: np.ndarray):
    seg = np.abs(B[:, :, lo:hi] - base[:, :, None])
    amp = seg.max(-1)
    pk = seg.argmax(-1)
    m = seg > frac * amp[..., None]
    _, _, width = m.shape
    ar = np.arange(width)[None, None, :]
    below = ~m
    left = np.where(below & (ar < pk[..., None]), ar, -1).max(-1) + 1
    right = np.where(below & (ar > pk[..., None]), ar, width).min(-1) - 1
    w = np.clip(right - left + 1, 0, width)
    return w.astype(float), amp, left + lo, right + lo


def local_base(pre: np.ndarray, idx_of: Dict[int, np.ndarray], k: int) -> np.ndarray:
    """Within-record shift(1).rolling(k, min_periods=1).median() of ``pre``.

    Q4-N computed this via ``groupby.apply`` + ``np.asarray``, which lines up with the
    original row order only when the record groups are contiguous and ascending. The
    explicit positional loop below is order-exact by construction; the arithmetic is
    the same (see the spec's Decision log).
    """
    out = np.array(pre, dtype=float, copy=True)
    for ii in idx_of.values():
        vals = pre[ii].astype(float)
        rolled = np.empty(len(vals), float)
        for j in range(len(vals)):
            if j == 0:
                rolled[j] = np.nan                       # shift(1) has no history yet
            else:
                lo = max(0, j - k)
                rolled[j] = np.median(vals[lo:j])
        out[ii] = np.where(np.isfinite(rolled), rolled, vals)
    return out


def build_base_features(cohort: Cohort) -> np.ndarray:
    """``F_BASE`` — the 9 RR-derived columns, frozen from Q4-N."""
    pre, post, idx_of = cohort.pre, cohort.post, cohort.idx_of
    med = np.empty_like(pre, dtype=float)
    std = np.empty_like(pre, dtype=float)
    mean = np.empty_like(pre, dtype=float)
    for ii in idx_of.values():
        med[ii] = float(np.median(pre[ii]))
        std[ii] = float(np.std(pre[ii], ddof=1)) if len(ii) > 1 else 0.0
        mean[ii] = float(np.mean(pre[ii]))
    cols = [med - pre]
    cols.append(np.column_stack([1.0 - pre / (local_base(pre, idx_of, k) + 1e-9)
                                 for k in RHY_K]))
    cols.append(post - pre)
    cols.append(std / (mean + 1e-9))
    cols.append(np.log1p(np.clip(pre, 0, None)))
    cols.append(np.log1p(np.clip(post, 0, None)))
    f_base = np.column_stack([c if c.ndim == 2 else c[:, None] for c in cols])
    return np.nan_to_num(f_base, nan=0.0, posinf=0.0, neginf=0.0)


def build_templates(cohort: Cohort, rel: np.ndarray) -> Tuple[Dict[int, np.ndarray],
                                                              Dict[int, dict]]:
    """Per-record median template plus the delineation Q4-N derived from it."""
    tmpl: Dict[int, np.ndarray] = {}
    delin: Dict[int, dict] = {}
    for r in cohort.records:
        ii = cohort.idx_of[int(r)]
        okm = (rel[ii] >= TMPL_LO) & (rel[ii] <= TMPL_HI)
        if int(okm.sum()) < TMPL_MIN:
            okm = np.ones(len(ii), bool)
        T = np.median(cohort.beat[ii][okm], axis=0).astype(float)
        iso = np.median(T[:, W_P_S[0]:W_P_S[0] + 8], axis=-1)
        # QRS lead first, then clamp the P window ahead of q_on so the P peak search
        # cannot land on the QRS upstroke (Q4-M's first run died exactly there).
        lq = int(np.argmax([peak_of(T[l], W_Q_S[0], W_Q_S[1], iso[l])[1]
                            for l in range(cohort.n_lead)]))
        q_on, q_off, q_amp = cross_span(T[lq], W_Q_S[0], W_Q_S[1], FRAC_QRS, iso[lq])
        p_hi = int(max(W_P_S[0] + 14, min(W_P_S[1], q_on - P_GAP)))
        lp = int(np.argmax([peak_of(T[l], W_P_S[0], p_hi, iso[l])[1]
                            for l in range(cohort.n_lead)]))
        p_on, p_off, p_amp = peak_span(T[lp], W_P_S[0], p_hi, FRAC_P, iso[lp])
        t_on, t_off, _ = peak_span(T[lq], W_T_S[0], W_T_S[1], FRAC_T, iso[lq])
        p_pk = peak_of(T[lp], W_P_S[0], p_hi, iso[lp])[0]
        tmpl[int(r)] = T
        delin[int(r)] = dict(
            lq=lq, lp=lp, iso=iso, p_hi=p_hi, q=(q_on, q_off), p=(p_on, p_off, p_pk),
            t=(t_on, t_off), p_amp=p_amp, q_amp=q_amp,
            qrs_ms=(q_off - q_on + 1) / FS * 1000.0,
            pw_ms=(p_off - p_on + 1) / FS * 1000.0,
            pr_ms=(q_on - p_on) / FS * 1000.0,
        )
    return tmpl, delin


def morph_feats(cohort: Cohort, tmpl: Dict[int, np.ndarray]) -> np.ndarray:
    """``MORPH`` — the 8 morphology columns. FROZEN: windows are Q4-N's, verbatim."""
    out = np.zeros((cohort.n, 8), float)
    WQ, WF, WS, WP, WW = (85, 125), (60, 220), (130, 260), (25, 75), (80, 130)
    for r in cohort.records:
        ii = cohort.idx_of[int(r)]
        B = cohort.beat[ii].astype(float)
        T = tmpl[int(r)]
        cq = corr_to(B[:, :, WQ[0]:WQ[1]], T[:, WQ[0]:WQ[1]])
        cf = corr_to(B[:, :, WF[0]:WF[1]], T[:, WF[0]:WF[1]])
        cs = corr_to(B[:, :, WS[0]:WS[1]], T[:, WS[0]:WS[1]])
        seg = B[:, :, WW[0]:WW[1]]
        med = np.median(seg, axis=-1, keepdims=True)
        amp = np.abs(seg - med).max(-1, keepdims=True) + 1e-9
        wid = (np.abs(seg - med) > 0.5 * amp).mean(-1)
        q = B[:, :, WQ[0]:WQ[1]]
        ptp = q.max(-1) - q.min(-1)
        tq = T[:, WQ[0]:WQ[1]]
        tptp = float(np.mean(tq.max(-1) - tq.min(-1))) + 1e-9
        area = np.abs(q - np.median(q, axis=-1, keepdims=True)).sum(-1)
        tarea = float(np.mean(np.abs(tq - np.median(tq, axis=-1, keepdims=True)).sum(-1))) + 1e-9
        p = B[:, :, WP[0]:WP[1]]
        pe = np.sqrt(((p - p.mean(-1, keepdims=True)) ** 2).mean(-1))
        tp_ = T[:, WP[0]:WP[1]]
        tpe = float(np.mean(np.sqrt(((tp_ - tp_.mean(-1, keepdims=True)) ** 2).mean(-1)))) + 1e-9
        out[ii, 0] = cq.min(1)
        out[ii, 1] = cq.mean(1)
        out[ii, 2] = cf.min(1)
        out[ii, 3] = cs.min(1)
        out[ii, 4] = wid.mean(1)
        out[ii, 5] = ptp.mean(1) / tptp
        out[ii, 6] = area.mean(1) / tarea
        out[ii, 7] = pe.mean(1) / tpe
    return np.nan_to_num(out, nan=0.0, posinf=0.0, neginf=0.0)


def interval_feats(cohort: Cohort, tmpl: Dict[int, np.ndarray],
                   delin: Dict[int, dict]) -> np.ndarray:
    """``INTV`` — 12 interval columns. Needed only to build Arm E's ``comb`` offset."""
    out = np.zeros((cohort.n, 12), float)
    for r in cohort.records:
        ri = int(r)
        ii = cohort.idx_of[ri]
        d = delin[ri]
        T = tmpl[ri]
        lp, lq = d["lp"], d["lq"]
        p_on, p_off, _ = d["p"]
        _, t_off = d["t"]
        p_hi = d["p_hi"]
        B = cohort.beat[ii].astype(float)
        pw0 = max(3, p_off - p_on + 1)
        seg_t = T[lp, p_on:p_on + pw0][None, :]
        best_a = np.full(len(ii), -1.0)
        best_s = np.ones(len(ii))
        best_l = np.zeros(len(ii), int)
        for lag in range(-LAG, LAG + 1):
            a, b = p_on + lag, p_on + lag + pw0
            if a < 0 or b > p_hi:
                continue
            c = corr_to(B[:, lp, a:b], seg_t)
            ac = np.abs(c)                       # |corr| so inverted P still registers
            upd = ac > best_a
            best_a[upd] = ac[upd]
            best_s[upd] = np.sign(c[upd])
            best_l[upd] = lag
        # Record-level zero calibration: the max over 61 lags clears 0.5 on noise by
        # selection alone, so the threshold comes from a sample-permuted template.
        seg_r = seg_t[:, np.random.RandomState(SEED0 + ri).permutation(pw0)]
        nul_a = np.full(len(ii), -1.0)
        for lag in range(-LAG, LAG + 1):
            a, b = p_on + lag, p_on + lag + pw0
            if a < 0 or b > p_hi:
                continue
            nul_a = np.maximum(nul_a, np.abs(corr_to(B[:, lp, a:b], seg_r)))
        thr_r = max(P_CORR_MIN, float(np.quantile(nul_a, P_NULL_Q)))
        p_found = (best_a >= thr_r).astype(float)

        base_b = np.median(B[:, :, W_P_S[0]:W_P_S[0] + 8], axis=-1)
        pw, pa, _, _ = peak_span_batch(B, max(0, p_on - LAG),
                                       min(p_hi, p_off + LAG + 1), FRAC_P, base_b)
        qw, _, q_first, _ = cross_span_batch(B, W_Q_S[0], W_Q_S[1], FRAC_QRS, base_b)
        tw, _, _, t_last = peak_span_batch(B, W_T_S[0], W_T_S[1], FRAC_T, base_b)
        pw = pw[:, lp]
        pa = pa[:, lp]
        qw = qw[:, lq]
        tw = tw[:, lq]
        p_on_b = (p_on + best_l).astype(float)
        q_on_b = q_first[:, lq].astype(float)
        pr_ms = (q_on_b - p_on_b) / FS * 1000.0
        ok_ = p_found > 0
        med_pr = float(np.median(pr_ms[ok_])) if ok_.any() else float(np.median(pr_ms))
        dpr = np.r_[0.0, np.diff(pr_ms)]
        rr_s = cohort.pre[ii] * FS
        t_last_prev = np.r_[float(t_off), t_last[:-1, lq].astype(float)]
        tp = rr_s + p_on_b - t_last_prev
        A = np.c_[np.ones(len(ii)), rr_s]
        coef, *_ = np.linalg.lstsq(A, tp, rcond=None)
        tp_res = tp - A @ coef
        med_pw = float(np.median(pw)) + 1e-9
        med_pa = float(np.median(pa)) + 1e-9
        out[ii, 0] = pr_ms / (med_pr + 1e-9)
        out[ii, 1] = dpr
        out[ii, 2] = pr_ms - med_pr
        out[ii, 3] = 1.0 - (dpr / 1000.0 * FS) / (rr_s + 1e-9)
        out[ii, 4] = pw / (qw + 1e-9)
        out[ii, 5] = pw / (tw + 1e-9)
        out[ii, 6] = tp_res / (float(np.std(tp_res)) + 1e-9)
        out[ii, 7] = pw / med_pw
        out[ii, 8] = best_a
        out[ii, 9] = best_s
        out[ii, 10] = pa / med_pa
        out[ii, 11] = p_found
    return np.nan_to_num(out, nan=0.0, posinf=0.0, neginf=0.0)


def _ang_dev(vx, vy, tx, ty):
    n1 = np.sqrt(vx ** 2 + vy ** 2) + 1e-12
    n2 = float(np.sqrt(tx ** 2 + ty ** 2)) + 1e-12
    c = np.clip((vx * tx + vy * ty) / (n1 * n2), -1.0, 1.0)
    return np.degrees(np.arccos(c))


def vec_feats(cohort: Cohort, tmpl: Dict[int, np.ndarray],
              delin: Dict[int, dict]) -> np.ndarray:
    """``VEC`` — 6 two-lead P/QRS axis columns. Arm E's ``comb`` offset only."""
    out = np.zeros((cohort.n, 6), float)
    if cohort.n_lead < 2:
        return out
    for r in cohort.records:
        ri = int(r)
        ii = cohort.idx_of[ri]
        B = cohort.beat[ii].astype(float)
        T = tmpl[ri]
        d = delin[ri]
        lp, lq, iso = d["lp"], d["lq"], d["iso"]
        p_on, p_off, p_pk = d["p"]
        pv = B[:, :, p_pk] - iso[None, :]
        tv = T[:, p_pk] - iso
        out[ii, 0] = _ang_dev(pv[:, 0], pv[:, 1], float(tv[0]), float(tv[1]))
        out[ii, 1] = (out[ii, 0] >= AXIS_DEG).astype(float)
        out[ii, 2] = (np.sign(pv[:, :2]) != np.sign(tv[:2])[None, :]).sum(1).astype(float)
        tmag = float(np.sqrt(float(tv[0]) ** 2 + float(tv[1]) ** 2)) + 1e-9
        out[ii, 3] = np.sqrt(pv[:, 0] ** 2 + pv[:, 1] ** 2) / tmag
        lo_ = 1 - lp if cohort.n_lead >= 2 else lp
        pw0 = max(3, p_off - p_on + 1)
        out[ii, 4] = np.abs(corr_to(B[:, lo_, p_on:p_on + pw0],
                                    T[lo_, p_on:p_on + pw0][None, :]))
        q_pk = peak_of(T[lq], W_Q_S[0], W_Q_S[1], iso[lq])[0]
        qv = B[:, :, q_pk] - iso[None, :]
        tq = T[:, q_pk] - iso
        out[ii, 5] = _ang_dev(qv[:, 0], qv[:, 1], float(tq[0]), float(tq[1]))
    return np.nan_to_num(out, nan=0.0, posinf=0.0, neginf=0.0)


def pont2_feats(cohort: Cohort, tmpl: Dict[int, np.ndarray],
                delin: Dict[int, dict]) -> np.ndarray:
    """``PONT2`` — 5 RR-normalised P-on-T columns. Arm E's ``comb`` offset only."""
    from scipy.stats import rankdata

    out = np.zeros((cohort.n, 5), float)
    grid = np.linspace(0.0, 1.0, PT_NRS)
    width = cohort.width
    for r in cohort.records:
        ri = int(r)
        ii = cohort.idx_of[ri]
        T = tmpl[ri]
        lq = delin[ri]["lq"]
        rr_s = np.clip(cohort.pre[ii] * FS, 60.0, 3.0 * FS)
        a_f = np.minimum(R_IDX + PT_LO_F * rr_s, float(width - 24))
        b_f = np.clip(R_IDX + PT_HI_F * rr_s, a_f + 4.0, float(width - 1))
        pos = a_f[:, None] + (b_f - a_f)[:, None] * grid[None, :]
        i0 = np.clip(np.floor(pos).astype(int), 0, width - 2)
        w1 = pos - i0
        prv = np.r_[ii[0], ii[:-1]]                       # the *previous* beat
        W = cohort.beat[prv][:, lq, :].astype(float)
        rows = np.arange(len(ii))[:, None]
        seg = W[rows, i0] * (1 - w1) + W[rows, i0 + 1] * w1
        tw = T[lq]
        tseg = tw[i0] * (1 - w1) + tw[i0 + 1] * w1
        c = corr_to(seg, tseg)
        e = np.sqrt(((seg - seg.mean(-1, keepdims=True)) ** 2).mean(-1))
        te = np.sqrt(((tseg - tseg.mean(-1, keepdims=True)) ** 2).mean(-1)) + 1e-9
        res = np.abs(seg - tseg)
        amp = np.ptp(tseg, axis=-1) + 1e-9
        half = PT_NRS // 2
        el = np.sqrt(((seg[:, half:] - seg[:, half:].mean(-1, keepdims=True)) ** 2).mean(-1))
        tel = np.sqrt(((tseg[:, half:] - tseg[:, half:].mean(-1, keepdims=True)) ** 2)
                      .mean(-1)) + 1e-9
        col = np.c_[c, e / te, res.max(-1) / amp,
                    res.argmax(-1) / float(PT_NRS - 1), el / tel]
        # Residualise against RR inside the record (label-free).
        z = (rr_s - rr_s.mean()) / (rr_s.std() + 1e-9)
        rk = rankdata(rr_s) / float(len(ii))
        A = np.c_[np.ones(len(ii)), z, z ** 2, z ** 3, rk, rk ** 2]
        coef, *_ = np.linalg.lstsq(A, col, rcond=None)
        out[ii] = col - A @ coef
    return np.nan_to_num(out, nan=0.0, posinf=0.0, neginf=0.0)


@dataclass
class FeatureSet:
    morph: np.ndarray           # F_BASE (9) + MORPH (8) = 17 — Arm A / C / D offset
    comb: np.ndarray            # + VEC (6) + PONT2 (5) = 27 — Arm E offset
    base: np.ndarray            # F_BASE alone (9), diagnostics only
    dims: Dict[str, int] = field(default_factory=dict)


def build_features(cohort: Cohort, with_comb: bool = True) -> FeatureSet:
    f_base = build_base_features(cohort)
    base12 = local_base(cohort.pre, cohort.idx_of, 12)
    rel = cohort.pre / (base12 + 1e-9)
    tmpl, delin = build_templates(cohort, rel)
    morph = morph_feats(cohort, tmpl)
    fm = np.c_[f_base, morph]
    if with_comb:
        comb = np.c_[fm, vec_feats(cohort, tmpl, delin), pont2_feats(cohort, tmpl, delin)]
    else:
        comb = fm
    fs = FeatureSet(morph=fm, comb=comb, base=f_base)
    fs.dims = {"base": f_base.shape[1], "morph": fm.shape[1], "comb": comb.shape[1]}
    return fs


# ─────────────────────────────────────────────────────────────────────────────
# Cohort filtering and the shared fold map
# ─────────────────────────────────────────────────────────────────────────────
def scorable_records(cohort: Cohort, min_s: int = MIN_S, min_n: int = MIN_N) -> List[int]:
    out = []
    for r in cohort.records:
        ii = cohort.idx_of[int(r)]
        if int(cohort.y[ii].sum()) >= min_s and int((~cohort.y[ii]).sum()) >= min_n:
            out.append(int(r))
    return out


def record_burden(cohort: Cohort, records: Sequence[int]) -> Dict[int, float]:
    return {int(r): float(cohort.y[cohort.idx_of[int(r)]].mean()) for r in records}


def make_fold_map(records: Sequence[int], burden: Dict[int, float],
                  n_folds: int = N_OUTER_FOLDS) -> Dict[int, int]:
    """Q4-N's record-burden stratification, unchanged: sort by (burden, id), i % n.

    Deterministic — no RNG is involved, so the same cohort always yields the same map.
    """
    if n_folds < 2:
        raise Q4OError("n_folds must be >= 2")
    if len(records) < n_folds:
        raise Q4OError(f"{len(records)} records cannot fill {n_folds} folds")
    order = sorted((int(r) for r in records), key=lambda r: (burden[r], r))
    return {r: i % n_folds for i, r in enumerate(order)}


def dev_records(train_records: Sequence[int], burden: Dict[int, float],
                every: int = DEV_EVERY) -> Tuple[List[int], List[int]]:
    """Split outer-train into (fit, dev). Dev is used for early stopping only."""
    rest = sorted((int(r) for r in train_records), key=lambda r: (burden[r], r))
    dev = [r for i, r in enumerate(rest) if i % every == 0]
    if len(dev) == len(rest):                                  # degenerate tiny cohorts
        dev = rest[:1]
    fit = [r for r in rest if r not in set(dev)]
    if not fit:
        raise Q4OError("outer-train has no records left after carving out dev")
    return fit, dev


def samples_of(cohort: Cohort, records: Sequence[int]) -> np.ndarray:
    if not len(records):
        return np.zeros(0, int)
    return np.concatenate([cohort.idx_of[int(r)] for r in records])


# ─────────────────────────────────────────────────────────────────────────────
# Leakage assertions
# ─────────────────────────────────────────────────────────────────────────────
def assert_disjoint(a: Sequence[int], b: Sequence[int], what: str) -> None:
    inter = sorted(set(int(x) for x in a) & set(int(x) for x in b))
    if inter:
        raise Q4OError(f"record leakage in {what}: shared records {inter}")


def assert_finite(arr: np.ndarray, what: str) -> None:
    a = np.asarray(arr, float)
    if not np.all(np.isfinite(a)):
        n_nan = int(np.isnan(a).sum())
        n_inf = int(np.isinf(a).sum())
        raise Q4OError(f"{what} contains {n_nan} NaN and {n_inf} Inf values")


def assert_full_coverage(scores: np.ndarray, n_expected: int, what: str) -> None:
    if scores.shape[-1] != n_expected:
        raise Q4OError(f"{what}: got {scores.shape[-1]} predictions for "
                       f"{n_expected} samples")
    assert_finite(scores, what)


def assert_fold_map_partition(fold_map: Dict[int, int], records: Sequence[int],
                              n_folds: int) -> None:
    recs = set(int(r) for r in records)
    if set(fold_map) != recs:
        raise Q4OError("fold map does not cover exactly the scorable records")
    for f in range(n_folds):
        te = [r for r, g in fold_map.items() if g == f]
        tr = [r for r, g in fold_map.items() if g != f]
        if not te:
            raise Q4OError(f"outer fold {f} has no test record")
        assert_disjoint(tr, te, f"outer fold {f} (train vs test)")


# ─────────────────────────────────────────────────────────────────────────────
# Leakage-free stacking — the whole point of Q4-O
# ─────────────────────────────────────────────────────────────────────────────
def _fit_logit(X: np.ndarray, y: np.ndarray):
    """Standardise on the given rows only, then fit. Returns a scoring closure."""
    from sklearn.linear_model import LogisticRegression

    mu = X.mean(0)
    sd = X.std(0) + 1e-9
    lr = LogisticRegression(max_iter=3000, C=1.0).fit((X - mu) / sd, y.astype(int))
    return lambda Z: lr.decision_function((Z - mu) / sd)


def cross_fitted_offsets(X: np.ndarray, cohort: Cohort, fold_map: Dict[int, int],
                         n_inner: int = N_INNER_FOLDS,
                         n_outer: int = N_OUTER_FOLDS,
                         burden: Optional[Dict[int, float]] = None,
                         log: Optional[RunLog] = None) -> Dict[int, np.ndarray]:
    """Return ``{outer_fold: offset_array}``, each of length ``cohort.n``.

    Within one outer fold ``f``:
      * outer-test records are removed entirely;
      * outer-train samples get an inner cross-fitted score — from an inner model that
        did **not** train on them — exactly once;
      * outer-test samples get a score from a single model fit on all of outer-train.

    This is the fix for the Q4-N bug. Q4-N wrote ``sc[tr]`` in-sample and let later
    folds overwrite earlier ones, leaving ~80% of the offset array in-sample.
    """
    records = sorted(fold_map)
    burden = burden or record_burden(cohort, records)
    offsets: Dict[int, np.ndarray] = {}

    # The cohort carries every beat, but only records that clear MIN_S/MIN_N are in the
    # fold map and therefore scored. Beats outside it are legitimately left as NaN with
    # an assignment count of 0, so the OOF audit runs over the scored subset.
    scored = samples_of(cohort, records)
    unscored = np.setdiff1d(np.arange(cohort.n), scored, assume_unique=False)

    for f in range(n_outer):
        te_recs = [r for r in records if fold_map[r] == f]
        tr_recs = [r for r in records if fold_map[r] != f]
        assert_disjoint(tr_recs, te_recs, f"outer fold {f}")

        off = np.full(cohort.n, np.nan)
        assign = np.zeros(cohort.n, int)

        inner_map = make_fold_map(tr_recs, burden, n_folds=min(n_inner, len(tr_recs)))
        n_inner_eff = max(inner_map.values()) + 1
        for g in range(n_inner_eff):
            iv_recs = [r for r in tr_recs if inner_map[r] == g]
            it_recs = [r for r in tr_recs if inner_map[r] != g]
            if not iv_recs or not it_recs:
                raise Q4OError(f"outer fold {f} inner fold {g} is degenerate")
            assert_disjoint(it_recs, iv_recs, f"outer {f} / inner {g}")
            it = samples_of(cohort, it_recs)
            iv = samples_of(cohort, iv_recs)
            score = _fit_logit(X[it], cohort.y[it])
            off[iv] = score(X[iv])
            assign[iv] += 1

        tr = samples_of(cohort, tr_recs)
        te = samples_of(cohort, te_recs)
        full = _fit_logit(X[tr], cohort.y[tr])
        off[te] = full(X[te])
        assign[te] += 1

        if not np.all(assign[scored] == 1):
            n_multi = int((assign[scored] > 1).sum())
            n_zero = int((assign[scored] == 0).sum())
            raise Q4OError(
                f"outer fold {f}: OOF assignment count != 1 for "
                f"{n_multi + n_zero} of {len(scored)} scored samples "
                f"({n_multi} scored more than once, {n_zero} never scored; "
                f"max {int(assign[scored].max())}). Scoring a sample more than once is "
                f"the Q4-N cpu_fold overwrite failure mode."
            )
        if unscored.size and np.any(assign[unscored] != 0):
            raise Q4OError(
                f"outer fold {f}: {int((assign[unscored] != 0).sum())} beats outside "
                f"the scorable cohort received an offset")
        assert_finite(off[scored], f"cross-fitted offset for outer fold {f}")
        offsets[f] = off
        if log:
            log(f"    fold {f}: offset cross-fitted over {len(tr_recs)} train records "
                f"({n_inner_eff} inner folds), {len(te_recs)} test records")
    return offsets


def leaky_overwrite_offsets(X: np.ndarray, cohort: Cohort,
                            fold_map: Dict[int, int],
                            n_outer: int = N_OUTER_FOLDS) -> Tuple[np.ndarray, np.ndarray]:
    """Reproduce Q4-N's ``cpu_fold`` verbatim, for the regression test only.

    Returns ``(scores, assignment_counts)``. The counts are what a correct OOF audit
    would check; here they come out far above 1, which is how the test detects the bug.
    NEVER use the returned scores for anything but demonstrating the failure.
    """
    records = sorted(fold_map)
    sc = np.full(cohort.n, np.nan)
    assign = np.zeros(cohort.n, int)
    for f in range(n_outer):
        te_recs = [r for r in records if fold_map[r] == f]
        tr_recs = [r for r in records if fold_map[r] != f]
        tr = samples_of(cohort, tr_recs)
        te = samples_of(cohort, te_recs)
        score = _fit_logit(X[tr], cohort.y[tr])
        sc[tr] = score(X[tr])        # <-- in-sample; later folds overwrite this
        assign[tr] += 1
        sc[te] = score(X[te])
        assign[te] += 1
    return sc, assign


# ─────────────────────────────────────────────────────────────────────────────
# Torch models
# ─────────────────────────────────────────────────────────────────────────────
def _require_torch():
    try:
        import torch
        return torch
    except Exception as exc:                                   # pragma: no cover
        raise Q4OError(f"torch is required for arms B/C/D/E: {exc}")


def set_determinism(seed: int) -> List[str]:
    """Enable determinism as far as the ops allow.

    Returns the notes for any op that refused to run deterministically; those go into
    ``manifest.json`` under ``nondeterministic_ops`` rather than being swallowed.
    """
    torch = _require_torch()
    notes: List[str] = []
    os.environ.setdefault("CUBLAS_WORKSPACE_CONFIG", ":4096:8")
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
    try:
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False
    except Exception as exc:
        notes.append(f"cudnn determinism unavailable: {exc}")
    try:
        torch.use_deterministic_algorithms(True, warn_only=True)
    except Exception as exc:
        notes.append(f"torch.use_deterministic_algorithms failed: {exc}")
    return notes


def build_residual_net(n_channel: int, init: str = "normal"):
    """``logit = offset + alpha * head(embed(conv(x)))``.

    ``alpha`` starts at exactly 0 so the model begins at the offset (lower bound
    guaranteed). The head is xavier-initialised: zero-initialising both ``alpha`` and
    the head is the Q4-N gradient deadlock — ``dL/dalpha ∝ head(z) = 0`` and
    ``dL/dhead_w ∝ alpha = 0`` trap each other at zero.
    """
    torch = _require_torch()
    import torch.nn as nn

    class ResidualBoost(nn.Module):
        def __init__(self) -> None:
            super().__init__()
            self.c = nn.Sequential(
                nn.Conv1d(n_channel, 24, 7, 2, 3), nn.GroupNorm(4, 24), nn.ReLU(),
                nn.Conv1d(24, 32, 5, 2, 2), nn.GroupNorm(4, 32), nn.ReLU(),
                nn.Conv1d(32, 32, 3, 2, 1), nn.GroupNorm(4, 32), nn.ReLU(),
                nn.AdaptiveAvgPool1d(1))
            self.e = nn.Linear(32, DL_EMB)
            self.h = nn.Linear(DL_EMB, 1)
            self.alpha = nn.Parameter(torch.zeros(1))
            if init == "zeros":          # deadlock reproduction — tests only
                nn.init.zeros_(self.h.weight)
                nn.init.zeros_(self.h.bias)
            else:
                nn.init.xavier_uniform_(self.h.weight)
                nn.init.zeros_(self.h.bias)

        def residual(self, x):
            z = torch.relu(self.e(self.c(x).squeeze(-1)))
            return self.h(z).squeeze(-1)

        def forward(self, x, off):
            return off + self.alpha * self.residual(x)

    return ResidualBoost()


def build_plain_cnn(n_channel: int):
    """Arm B: the same trunk, but a plain logit — no offset, no ``alpha``."""
    torch = _require_torch()
    import torch.nn as nn

    class PlainCNN(nn.Module):
        def __init__(self) -> None:
            super().__init__()
            self.c = nn.Sequential(
                nn.Conv1d(n_channel, 24, 7, 2, 3), nn.GroupNorm(4, 24), nn.ReLU(),
                nn.Conv1d(24, 32, 5, 2, 2), nn.GroupNorm(4, 32), nn.ReLU(),
                nn.Conv1d(32, 32, 3, 2, 1), nn.GroupNorm(4, 32), nn.ReLU(),
                nn.AdaptiveAvgPool1d(1))
            self.e = nn.Linear(32, DL_EMB)
            self.h = nn.Linear(DL_EMB, 1)
            nn.init.xavier_uniform_(self.h.weight)
            nn.init.zeros_(self.h.bias)

        def forward(self, x, off=None):
            z = torch.relu(self.e(self.c(x).squeeze(-1)))
            return self.h(z).squeeze(-1)

    return PlainCNN()


def residual_grad_is_alive(n_channel: int = 2, init: str = "normal",
                           width: int = 64, seed: int = SEED0,
                           warmup_steps: int = 0) -> Dict[str, float]:
    """Measure the residual branch's gradient after ``warmup_steps`` optimiser steps.

    The gradient structure of ``logit = off + alpha * h(z)`` is::

        dL/dalpha = dL/dlogit * h(z)
        dL/dh_w   = dL/dlogit * alpha * z

    Because Q4-O deliberately starts at ``alpha = 0`` (lower bound guaranteed), the
    head's gradient is zero at step 0 *by construction* — that alone is not the bug.
    The Q4-N bug is that zeroing the head too makes ``dL/dalpha`` zero as well, so
    neither can ever move. With a xavier head, ``dL/dalpha != 0`` at step 0, ``alpha``
    leaves zero, and the head starts receiving gradient from the next step onward.
    """
    torch = _require_torch()
    import torch.nn as nn

    torch.manual_seed(seed)
    net = build_residual_net(n_channel, init=init)
    x = torch.randn(32, n_channel, width)
    off = torch.randn(32) * 0.5
    y = (torch.rand(32) > 0.5).float()
    bce = nn.BCEWithLogitsLoss()

    if warmup_steps:
        opt = torch.optim.Adam(net.parameters(), DL_LR)
        for _ in range(warmup_steps):
            opt.zero_grad()
            bce(net(x, off), y).backward()
            opt.step()
    net.zero_grad(set_to_none=False)
    bce(net(x, off), y).backward()
    return {
        "alpha": float(net.alpha.detach().abs().sum()),
        "alpha_grad": float(net.alpha.grad.abs().sum()),
        "head_weight_grad": float(net.h.weight.grad.abs().sum()),
        "embed_weight_grad": float(net.e.weight.grad.abs().sum()),
        "warmup_steps": int(warmup_steps),
    }


# ─────────────────────────────────────────────────────────────────────────────
# Arm inputs
# ─────────────────────────────────────────────────────────────────────────────
def current_beat_input(cohort: Cohort, beat: Optional[np.ndarray] = None) -> np.ndarray:
    """Arms B/C/D: the current beat's lead waveforms and nothing else.

    No previous/next beat, no RR channel, no morphology, no P-vector.
    """
    B = cohort.beat if beat is None else beat
    return np.ascontiguousarray(B, dtype="float32")


def three_beat_input(cohort: Cohort) -> np.ndarray:
    """Arm E only: Q4-N's ``make_x`` — prev/cur/next waveforms plus two RR channels."""
    n, n_lead, width = cohort.beat.shape
    prev = np.zeros(n, int)
    nxt = np.zeros(n, int)
    for ii in cohort.idx_of.values():
        prev[ii] = np.r_[ii[0], ii[:-1]]
        nxt[ii] = np.r_[ii[1:], ii[-1]]
    base12 = local_base(cohort.pre, cohort.idx_of, 12)
    relp = np.clip(cohort.pre / (base12 + 1e-9), 0.3, 2.0)
    reln = np.clip(cohort.post / (base12 + 1e-9), 0.3, 2.0)
    wav = np.concatenate([cohort.beat[prev], cohort.beat, cohort.beat[nxt]], axis=1)
    rr = np.stack([np.repeat(relp[:, None], width, 1),
                   np.repeat(reln[:, None], width, 1)], axis=1)
    return np.ascontiguousarray(np.concatenate([wav, rr], axis=1), dtype="float32")


def shuffle_waveforms_within_record(cohort: Cohort,
                                    perm_seed: int = PERM_SEED) -> Tuple[np.ndarray, dict]:
    """Arm D: permute beat waveforms **within each record**.

    The record's set of waveforms is preserved exactly (it is a permutation of the same
    rows), so the record-level signal distribution is untouched. What is destroyed is
    the beat-level correspondence between a waveform and its own label, RR, and offset.
    """
    shuffled = np.array(cohort.beat, copy=True)
    moved_total = 0
    for r in cohort.records:
        ii = cohort.idx_of[int(r)]
        rng = np.random.RandomState(perm_seed + int(r))
        perm = rng.permutation(len(ii))
        shuffled[ii] = cohort.beat[ii][perm]
        moved_total += int((perm != np.arange(len(ii))).sum())
    rule = {
        "seed": int(perm_seed),
        "per_record_seed": "np.random.RandomState(PERM_SEED + record_id)",
        "rule": "beat[idx_of_record] = beat[idx_of_record][rng.permutation(n_record)]",
        "preserved": ["record signal distribution", "labels", "RR", "record ids",
                      "morphology offset"],
        "destroyed": ["beat-level waveform-to-label correspondence"],
        "moved_fraction": float(moved_total / max(1, cohort.n)),
    }
    if rule["moved_fraction"] < 0.5:
        raise Q4OError(f"waveform permutation is near-identity "
                       f"(moved {rule['moved_fraction']:.3f})")
    return shuffled, rule


# ─────────────────────────────────────────────────────────────────────────────
# Training loop shared by arms B/C/D/E
# ─────────────────────────────────────────────────────────────────────────────
def _chunked_mean_std(X: np.ndarray, idx: np.ndarray,
                      chunk: int = 8192) -> Tuple[float, float]:
    """Scalar mean/std over ``X[idx]`` without materialising the whole slice."""
    total = 0.0
    total_sq = 0.0
    count = 0
    for b0 in range(0, len(idx), chunk):
        block = X[idx[b0:b0 + chunk]].astype(np.float64, copy=False)
        total += float(block.sum())
        total_sq += float((block ** 2).sum())
        count += block.size
    if count == 0:
        raise Q4OError("cannot normalise on an empty fit split")
    mean = total / count
    var = max(total_sq / count - mean * mean, 0.0)
    return float(mean), float(np.sqrt(var)) + 1e-9


def _train_one_fold(net, X: np.ndarray, offset: Optional[np.ndarray],
                    y: np.ndarray, fit_idx: np.ndarray, dev_idx: np.ndarray,
                    test_idx: np.ndarray, seed: int, device: str,
                    epochs: int, batch: int, log: Optional[RunLog] = None):
    """Fit on ``fit_idx``, early-stop on ``dev_idx``, score ``test_idx``.

    ``dev_idx`` comes from outer-train records only. No test label, no test statistic,
    and no test-derived scaler is touched anywhere in this function.
    """
    torch = _require_torch()
    import torch.nn as nn

    net = net.to(device)
    opt = torch.optim.Adam(net.parameters(), DL_LR, weight_decay=DL_WD)
    bce = nn.BCEWithLogitsLoss()

    # Waveform normalisation is fit on the fit split only. Computed in chunks: on the
    # real cohort a plain X[fit_idx].mean() materialises a ~1.4 GB temporary for Arm E's
    # 8-channel input, and again for the std.
    wmu, wsd = _chunked_mean_std(X, fit_idx)

    def batch_tensors(idx):
        x = torch.tensor((X[idx] - wmu) / wsd, device=device)
        o = (torch.tensor(offset[idx].astype("float32"), device=device)
             if offset is not None else torch.zeros(len(idx), device=device))
        return x, o

    best_state = {k: v.detach().clone() for k, v in net.state_dict().items()}
    best_loss, bad, best_epoch = float("inf"), 0, -1
    rng = np.random.RandomState(seed)
    history: List[dict] = []

    for ep in range(epochs):
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
            opt.step()
            # Recorded from the loss that was already computed for the backward pass.
            train_tot += float(loss.detach()) * len(bi)
            train_cnt += len(bi)

        net.eval()
        with torch.no_grad():
            tot, cnt = 0.0, 0
            dev_logits = np.empty(len(dev_idx), dtype=float)
            for b0 in range(0, len(dev_idx), 4096):
                sl = slice(b0, b0 + 4096)
                bi = dev_idx[sl]
                x, o = batch_tensors(bi)
                yy = torch.tensor(y[bi].astype("float32"), device=device)
                out = net(x, o)
                tot += float(bce(out, yy)) * len(bi)
                cnt += len(bi)
                dev_logits[sl] = out.detach().cpu().numpy()
            dev_loss = tot / max(1, cnt)

        # Diagnostics only. dev PR-AUC is recorded for the learning curves and is
        # NEVER used to select the checkpoint — selection stays on dev BCE loss below,
        # exactly as before history recording existed.
        dev_prauc = None
        try:
            from sklearn.metrics import average_precision_score
            y_dev = y[dev_idx].astype(int)
            if 0 < int(y_dev.sum()) < len(y_dev):
                dev_prauc = float(average_precision_score(y_dev, dev_logits))
        except Exception:
            dev_prauc = None
        history.append({
            "epoch": int(ep),
            "train_loss": float(train_tot / max(1, train_cnt)),
            "dev_loss": float(dev_loss),
            "dev_prauc": dev_prauc,
            "alpha": (float(net.alpha.detach().cpu().numpy()[0])
                      if hasattr(net, "alpha") else None),
        })

        if dev_loss < best_loss - 1e-6:
            best_loss, best_epoch, bad = dev_loss, ep, 0
            best_state = {k: v.detach().clone() for k, v in net.state_dict().items()}
        else:
            bad += 1
            if bad >= DL_PATIENCE and ep + 1 >= min(DL_MIN_EPOCH, epochs):
                break

    net.load_state_dict(best_state)
    net.eval()
    scores = np.full(len(test_idx), np.nan, dtype=float)
    with torch.no_grad():
        for b0 in range(0, len(test_idx), 4096):
            sl = slice(b0, b0 + 4096)
            bi = test_idx[sl]
            x, o = batch_tensors(bi)
            scores[sl] = net(x, o).detach().cpu().numpy()
    alpha = float(net.alpha.detach().cpu().numpy()[0]) if hasattr(net, "alpha") else float("nan")
    return scores, alpha, best_epoch, float(best_loss), history


def run_logistic_arm(X: np.ndarray, cohort: Cohort, fold_map: Dict[int, int],
                     n_outer: int = N_OUTER_FOLDS) -> np.ndarray:
    """Arm A. One model per outer fold, fit on outer-train only, scores outer-test."""
    records = sorted(fold_map)
    out = np.full(cohort.n, np.nan)
    for f in range(n_outer):
        te_recs = [r for r in records if fold_map[r] == f]
        tr_recs = [r for r in records if fold_map[r] != f]
        assert_disjoint(tr_recs, te_recs, f"Arm A outer fold {f}")
        tr = samples_of(cohort, tr_recs)
        te = samples_of(cohort, te_recs)
        out[te] = _fit_logit(X[tr], cohort.y[tr])(X[te])
    scored = samples_of(cohort, records)
    assert_finite(out[scored], "Arm A scores")
    return out


def loro_scores(X: np.ndarray, cohort: Cohort, records: Sequence[int],
                burden: Dict[int, float], every: int = DEV_EVERY) -> np.ndarray:
    """Q4-N's leave-one-record-out path, reproduced for the porting-fidelity check.

    Held-out record -> the rest is split into (train, dev) by burden order, the model
    is fit on train, and a Platt calibration fit on dev is applied to the held-out
    scores. This is Q4-N's ``loro()`` / ``fit_fold()``, which the ``cpu_fold`` bug did
    not touch. Used only to compare Arm A's ported features against Q4-N's reported
    ``morph`` k-sweep of 0.8361 — it is not part of the hypothesis test.
    """
    from sklearn.linear_model import LogisticRegression

    out = np.full(cohort.n, np.nan)
    for held in records:
        rest = sorted((int(r) for r in records if int(r) != int(held)),
                      key=lambda r: (burden[r], r))
        dv_r = [r for i, r in enumerate(rest) if i % every == 0]
        tr_r = [r for r in rest if r not in set(dv_r)]
        assert_disjoint(tr_r + dv_r, [int(held)], "LORO held-out record")
        tr = samples_of(cohort, tr_r)
        dv = samples_of(cohort, dv_r)
        te = cohort.idx_of[int(held)]
        score = _fit_logit(X[tr], cohort.y[tr])
        cal = LogisticRegression(max_iter=3000, C=1e6).fit(
            score(X[dv]).reshape(-1, 1), cohort.y[dv].astype(int))
        a, b = float(cal.coef_[0, 0]), float(cal.intercept_[0])
        out[te] = a * score(X[te]) + b
    assert_finite(out[samples_of(cohort, records)], "LORO scores")
    return out


def morph_port_check(feats: "FeatureSet", cohort: Cohort, records: Sequence[int],
                     burden: Dict[int, float]) -> Dict[str, object]:
    """Compare the ported morphology features against Q4-N's reported LORO k-sweep."""
    sc = loro_scores(feats.morph, cohort, records, burden)
    ksw = summarise(per_record_metrics(sc, cohort, records)["ksw"])
    delta = ksw["mean"] - REF_Q4N["morph_ksw_loro"]
    return {
        "reference_q4n_morph_ksw_loro": REF_Q4N["morph_ksw_loro"],
        "measured_loro_ksw": ksw["mean"],
        "delta": float(delta),
        "tolerance": MORPH_PORT_TOL,
        "within_tolerance": bool(abs(delta) <= MORPH_PORT_TOL),
        "note": ("Diagnostic on the feature port, not on the hypothesis. A large "
                 "delta means the ported morphology code diverged from Q4-N."),
    }


def run_nn_arm(arm: str, X: np.ndarray, offsets: Optional[Dict[int, np.ndarray]],
               cohort: Cohort, fold_map: Dict[int, int], seed: int,
               burden: Dict[int, float], device: str, epochs: int, batch: int,
               n_outer: int = N_OUTER_FOLDS, log: Optional[RunLog] = None):
    """Arms B/C/D/E for one seed. Returns (scores, per-fold diagnostics)."""
    records = sorted(fold_map)
    out = np.full(cohort.n, np.nan)
    diags = []
    for f in range(n_outer):
        te_recs = [r for r in records if fold_map[r] == f]
        tr_recs = [r for r in records if fold_map[r] != f]
        assert_disjoint(tr_recs, te_recs, f"{arm} outer fold {f}")
        fit_recs, dv_recs = dev_records(tr_recs, burden)
        assert_disjoint(fit_recs, dv_recs, f"{arm} outer fold {f} (fit vs dev)")
        assert_disjoint(fit_recs + dv_recs, te_recs, f"{arm} outer fold {f} (train vs test)")

        fit_idx = samples_of(cohort, fit_recs)
        dev_idx = samples_of(cohort, dv_recs)
        te_idx = samples_of(cohort, te_recs)
        off = offsets[f] if offsets is not None else None

        set_determinism(seed + 1009 * f)
        net = (build_plain_cnn(X.shape[1]) if offsets is None
               else build_residual_net(X.shape[1], init="normal"))
        scores, alpha, best_ep, dev_loss, hist = _train_one_fold(
            net, X, off, cohort.y, fit_idx, dev_idx, te_idx,
            seed + 1009 * f, device, epochs, batch, log)
        out[te_idx] = scores
        diags.append({"fold": f, "alpha": alpha, "best_epoch": best_ep,
                      "dev_loss": dev_loss, "n_fit": int(len(fit_idx)),
                      "n_dev": int(len(dev_idx)), "n_test": int(len(te_idx)),
                      "history": hist})
        if log:
            log(f"    {arm} seed {seed} fold {f}: alpha {alpha:+.4f} · "
                f"best epoch {best_ep} · dev loss {dev_loss:.4f}")
    scored = samples_of(cohort, records)
    assert_finite(out[scored], f"{arm} scores")
    return out, diags


# ─────────────────────────────────────────────────────────────────────────────
# Metrics — protocol preserved from Q4-N
# ─────────────────────────────────────────────────────────────────────────────
def achievement_at(scores: np.ndarray, idx: np.ndarray, y: np.ndarray, k: int) -> float:
    """``TP@k / min(S_record, k)`` — Q4-N's identity, unchanged."""
    sc = scores[idx]
    yy = y[idx]
    n_s = int(yy.sum())
    kk = int(min(max(1, k), len(idx)))
    flag = sc >= np.partition(sc, -kk)[-kk]
    tp = int((flag & yy).sum())
    return tp / max(1, min(n_s, int(k)))


def per_record_metrics(scores: np.ndarray, cohort: Cohort,
                       records: Sequence[int]) -> Dict[str, Dict[int, float]]:
    from sklearn.metrics import average_precision_score, roc_auc_score

    out: Dict[str, Dict[int, float]] = {"ksw": {}, "auroc": {}, "prauc": {}}
    for k in tuple(K_OP) + tuple(K_SWEEP):
        out[f"ach@{k}"] = {}
    for r in records:
        ri = int(r)
        ii = cohort.idx_of[ri]
        yy = cohort.y[ii].astype(int)
        out["ksw"][ri] = float(np.mean([achievement_at(scores, ii, cohort.y, k)
                                        for k in K_SWEEP]))
        for k in tuple(K_OP) + tuple(K_SWEEP):
            out[f"ach@{k}"][ri] = float(achievement_at(scores, ii, cohort.y, k))
        out["auroc"][ri] = float(roc_auc_score(yy, scores[ii]))
        out["prauc"][ri] = float(average_precision_score(yy, scores[ii]))
    return out


def summarise(per_record: Dict[int, float]) -> Dict[str, float]:
    vals = np.array([per_record[r] for r in sorted(per_record)], float)
    worst_rec = int(min(per_record, key=lambda r: per_record[r]))
    return {
        "mean": float(vals.mean()),
        "std": float(vals.std(ddof=1)) if len(vals) > 1 else 0.0,
        "p10": float(np.percentile(vals, 10)),
        "median": float(np.median(vals)),
        "worst": float(vals.min()),
        "worst_record": worst_rec,
        "n_record": int(len(vals)),
    }


# ─────────────────────────────────────────────────────────────────────────────
# Statistics
# ─────────────────────────────────────────────────────────────────────────────
def paired_record_bootstrap(diff_by_record: Dict[int, float], n_boot: int = NB_BOOT,
                            seed: int = SEED0, alpha: float = 5.0) -> Dict[str, float]:
    """Record-level paired bootstrap of a per-record difference."""
    recs = sorted(diff_by_record)
    d = np.array([diff_by_record[r] for r in recs], float)
    rng = np.random.RandomState(seed)
    n = len(d)
    if n == 0:
        raise Q4OError("paired bootstrap needs at least one record")
    draws = np.array([d[rng.randint(0, n, n)].mean() for _ in range(n_boot)])
    return {
        "mean": float(d.mean()),
        "ci_low": float(np.percentile(draws, alpha / 2)),
        "ci_high": float(np.percentile(draws, 100 - alpha / 2)),
        "n_record": int(n),
        "n_boot": int(n_boot),
    }


def hierarchical_bootstrap(diff_by_record_seed: Dict[int, Dict[int, float]],
                           n_boot: int = NB_BOOT, seed: int = SEED0,
                           alpha: float = 5.0) -> Dict[str, float]:
    """Resample records **and**, within each drawn record, seeds.

    ``diff_by_record_seed[record][seed] = paired difference``.
    """
    recs = sorted(diff_by_record_seed)
    if not recs:
        raise Q4OError("hierarchical bootstrap needs at least one record")
    seeds = sorted(diff_by_record_seed[recs[0]])
    mat = np.array([[diff_by_record_seed[r][s] for s in seeds] for r in recs], float)
    rng = np.random.RandomState(seed + 1)
    n_rec, n_seed = mat.shape
    draws = np.empty(n_boot)
    for b in range(n_boot):
        ri = rng.randint(0, n_rec, n_rec)
        si = rng.randint(0, n_seed, (n_rec, n_seed))
        draws[b] = mat[ri[:, None], si].mean()
    return {
        "mean": float(mat.mean()),
        "ci_low": float(np.percentile(draws, alpha / 2)),
        "ci_high": float(np.percentile(draws, 100 - alpha / 2)),
        "n_record": int(n_rec),
        "n_seed": int(n_seed),
        "n_boot": int(n_boot),
    }


# ─────────────────────────────────────────────────────────────────────────────
# Pre-registered gates
# ─────────────────────────────────────────────────────────────────────────────
def evaluate_gates(c_minus_a: Dict[str, float], c_minus_d: Dict[str, float],
                   seed_direction: List[float], p10_a: float, p10_c: float,
                   leakage_ok: bool) -> Dict[str, object]:
    """Apply the spec's six PASS criteria to measured numbers. No value is invented."""
    positive_seeds = int(sum(1 for v in seed_direction if v > 0))
    checks = {
        "1_mean_gain_ge_0.015": bool(c_minus_a["mean"] >= GATE_MIN_GAIN),
        "2_ci_lower_gt_0": bool(c_minus_a["ci_low"] > 0.0),
        "3_beats_shuffle_control": bool(c_minus_d["mean"] > 0.0
                                        and c_minus_d["ci_low"] > 0.0),
        "4_seed_direction_stable": bool(positive_seeds >= GATE_MIN_SEED_AGREE),
        "5_lower_tail_not_worse": bool(p10_c >= p10_a - GATE_LOWER_TAIL_MAX_DROP),
        "6_leakage_and_reproducibility": bool(leakage_ok),
    }
    verdict = "PASS" if all(checks.values()) else "NO-GO"
    return {
        "checks": checks,
        "verdict": verdict,
        "positive_seed_count": positive_seeds,
        "n_seed": len(seed_direction),
        "thresholds": {
            "min_gain": GATE_MIN_GAIN,
            "min_seed_agreement": GATE_MIN_SEED_AGREE,
            "lower_tail_max_drop": GATE_LOWER_TAIL_MAX_DROP,
        },
        "next_step": ("Port the same minimal residual structure to MIT-BIH DS1->DS2 "
                      "under the primary S PR-AUC protocol. Do NOT go to a Transformer."
                      if verdict == "PASS" else
                      "Keep the morphology baseline. Return to failure-record and "
                      "lower-tail analysis. Do NOT build a Transformer or a larger "
                      "fusion model."),
    }


# ─────────────────────────────────────────────────────────────────────────────
# Artifacts
# ─────────────────────────────────────────────────────────────────────────────
def run_dir_name(timestamp: str) -> str:
    return f"{timestamp}_{EXPERIMENT_ID}_{RUN_SLUG}"


def _json_safe(obj):
    if isinstance(obj, dict):
        return {str(k): _json_safe(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_json_safe(v) for v in obj]
    if isinstance(obj, (np.integer,)):
        return int(obj)
    if isinstance(obj, (np.floating,)):
        return float(obj)
    if isinstance(obj, (np.bool_,)):
        return bool(obj)
    if isinstance(obj, np.ndarray):
        return _json_safe(obj.tolist())
    return obj


def write_bundle(out_dir: str, config: dict, manifest: dict, result: dict,
                 fold_map: Dict[int, int], arm_probs: Dict[str, np.ndarray],
                 predictions: dict, log_text: str,
                 figures: Optional[Dict[str, object]] = None,
                 training_history: Optional[list] = None) -> str:
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(os.path.join(out_dir, "figures"), exist_ok=True)
    for name, payload in (("config.json", config), ("manifest.json", manifest),
                          ("result.json", result)):
        with open(os.path.join(out_dir, name), "w", encoding="utf-8") as fh:
            json.dump(_json_safe(payload), fh, ensure_ascii=False, indent=2)
    with open(os.path.join(out_dir, "fold_map.json"), "w", encoding="utf-8") as fh:
        json.dump({"n_folds": N_OUTER_FOLDS,
                   "record_to_fold": {str(k): int(v) for k, v in sorted(fold_map.items())},
                   "fold_to_records": {str(f): sorted(r for r, g in fold_map.items()
                                                      if g == f)
                                       for f in sorted(set(fold_map.values()))}},
                  fh, ensure_ascii=False, indent=2)
    for arm, probs in arm_probs.items():
        arm_dir = os.path.join(out_dir, "arms", arm)
        os.makedirs(arm_dir, exist_ok=True)
        np.save(os.path.join(arm_dir, "probs.npy"), probs)
    np.savez_compressed(os.path.join(out_dir, "predictions.npz"), **predictions)
    if training_history:
        with open(os.path.join(out_dir, "training_history.json"), "w",
                  encoding="utf-8") as fh:
            json.dump(_json_safe(training_history), fh, ensure_ascii=False, indent=1)
    with open(os.path.join(out_dir, "log.txt"), "w", encoding="utf-8") as fh:
        fh.write(log_text)
    if figures:
        _write_figures(os.path.join(out_dir, "figures"), figures)
    verify_bundle(out_dir, tuple(arm_probs))
    return out_dir


def _write_figures(fig_dir: str, payload: Dict[str, object]) -> None:
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except Exception:
        with open(os.path.join(fig_dir, "FIGURES_SKIPPED.txt"), "w") as fh:
            fh.write("matplotlib unavailable; figures not rendered\n")
        return
    arm_means = payload.get("arm_means", {})
    if arm_means:
        fig, ax = plt.subplots(figsize=(7, 3.2))
        names = list(arm_means)
        ax.bar(np.arange(len(names)), [arm_means[a] for a in names], color="tab:blue")
        ax.set_xticks(np.arange(len(names)))
        ax.set_xticklabels(names, rotation=20, ha="right", fontsize=7)
        ax.set_ylabel("k-sweep achievement mean")
        ax.set_title(f"{EXPERIMENT_ID} / {ARM_ID} — arms", fontsize=9)
        ax.grid(alpha=0.3, axis="y")
        fig.tight_layout()
        fig.savefig(os.path.join(fig_dir, "arms_ksweep.png"), dpi=120)
        plt.close(fig)
    contrasts = payload.get("contrasts", {})
    if contrasts:
        # Primary and reference contrasts go on SEPARATE axes. B - A is orders of
        # magnitude larger than C - A; sharing one axis flattens every contrast the
        # decision actually rests on into a single indistinguishable dot at zero.
        groups = [("contrasts_primary.png", PRIMARY_CONTRASTS,
                   "Primary contrasts (decision-relevant)"),
                  ("contrasts_reference.png", REFERENCE_CONTRASTS,
                   "Reference gaps (separate scale)")]
        for fname, wanted, title in groups:
            names = [n for n in wanted if n in contrasts]
            if not names:
                continue
            fig, ax = plt.subplots(figsize=(8, 0.85 * len(names) + 2.0))
            means = [contrasts[c]["mean"] for c in names]
            lo = [contrasts[c]["mean"] - contrasts[c]["ci_low"] for c in names]
            hi = [contrasts[c]["ci_high"] - contrasts[c]["mean"] for c in names]
            ax.errorbar(means, np.arange(len(names)), xerr=[lo, hi], fmt="o",
                        capsize=5, lw=2)
            for i, c in enumerate(names):
                ax.annotate(f"  {contrasts[c]['mean']:+.4f}",
                            xy=(contrasts[c]["ci_high"], i), xytext=(5, 0),
                            textcoords="offset points", va="center", fontsize=8)
            ax.axvline(0.0, color="k", lw=1.0)
            ax.axvline(GATE_MIN_GAIN, color="tab:red", lw=1.0, ls="--",
                       label=f"gate +{GATE_MIN_GAIN}")
            ax.set_yticks(np.arange(len(names)))
            ax.set_yticklabels([n.replace("_minus_", " - ") for n in names], fontsize=8)
            ax.set_ylim(-0.7, len(names) - 0.3)
            ax.set_xlabel("paired difference (k-sweep achievement, 95% CI)")
            ax.set_title(title, fontsize=10)
            ax.legend(fontsize=7)
            ax.grid(alpha=0.3, axis="x")
            fig.tight_layout()
            fig.savefig(os.path.join(fig_dir, fname), dpi=120)
            plt.close(fig)


def verify_bundle(out_dir: str, arms: Sequence[str] = ARMS) -> None:
    """Artifact schema gate — raises if the run bundle is incomplete."""
    for name in REQUIRED_BUNDLE_FILES:
        p = os.path.join(out_dir, name)
        if not os.path.exists(p):
            raise Q4OError(f"run bundle is missing {name}")
    if not os.path.isdir(os.path.join(out_dir, "figures")):
        raise Q4OError("run bundle is missing figures/")
    for arm in arms:
        p = os.path.join(out_dir, "arms", arm, "probs.npy")
        if not os.path.exists(p):
            raise Q4OError(f"run bundle is missing arms/{arm}/probs.npy")
    pred = np.load(os.path.join(out_dir, "predictions.npz"))
    for key in ("sample_id", "record_id", "y_true", "fold", "seeds"):
        if key not in pred.files:
            raise Q4OError(f"predictions.npz is missing '{key}'")
    n = len(pred["sample_id"])
    mask = pred["scored_mask"].astype(bool) if "scored_mask" in pred.files else None
    for arm in arms:
        probs = np.load(os.path.join(out_dir, "arms", arm, "probs.npy"))
        if probs.ndim != 2 or probs.shape[1] != n:
            raise Q4OError(f"arms/{arm}/probs.npy has shape {probs.shape}; "
                           f"expected (n_seed, {n})")
        # Beats in records that fail MIN_S/MIN_N are never scored and stay NaN by
        # design. Every beat the run *claims* to have scored must be finite.
        if mask is not None and not np.all(np.isfinite(probs[:, mask])):
            bad = int((~np.isfinite(probs[:, mask])).sum())
            raise Q4OError(f"arms/{arm}/probs.npy has {bad} non-finite values among "
                           f"the scored beats")


def append_registry(registry_path: str, record: dict) -> None:
    """Append one measured run summary. Only ever called with executed results."""
    required = ("run_id", "experiment_id", "primary_value", "verdict", "conclusion",
                "run_folder")
    missing = [k for k in required if k not in record]
    if missing:
        raise Q4OError(f"registry record is missing {missing}")
    os.makedirs(os.path.dirname(os.path.abspath(registry_path)) or ".", exist_ok=True)
    with open(registry_path, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(_json_safe(record), ensure_ascii=False) + "\n")


# ─────────────────────────────────────────────────────────────────────────────
# Reporting — PRESENTATION ONLY
#
# Everything in this section reads a finished run bundle and renders it. It never
# trains, never changes an arm/fold/seed/metric/bootstrap/gate, and never writes to
# config.json, manifest.json, result.json, fold_map.json, predictions.npz, or
# arms/*/probs.npy. Measured quantities are read from result.json rather than
# recomputed. Per-record values, which result.json stores only as summaries, are
# recomputed from the stored logits using the same achievement_at() the run used —
# and reconcile_report() checks that recomputation against result.json's summaries.
#
# Figure text is English on purpose: Colab has no CJK font by default, so Korean
# axis labels render as tofu boxes. The prose report is Korean.
# ─────────────────────────────────────────────────────────────────────────────
IMMUTABLE_BUNDLE_FILES = ("config.json", "manifest.json", "result.json",
                          "fold_map.json", "predictions.npz")

PRIMARY_CONTRASTS = ("C_minus_A", "C_minus_D", "E_minus_combBaseline")
REFERENCE_CONTRASTS = ("B_minus_A", "D_minus_A", "E_minus_A")
COMB_BASELINE = "comb_baseline_diagnostic"

ARM_SHORT = {ARM_A: "A", ARM_B: "B", ARM_C: "C", ARM_D: "D", ARM_E: "E",
             COMB_BASELINE: "cleanComb"}
ARM_KO = {
    ARM_A: "A · morphology baseline (동결된 Q4-N 형태 특징, 로지스틱)",
    ARM_B: "B · 현재 박동 raw CNN (2리드 파형만)",
    ARM_C: "C · morphology + raw residual (주 비교군)",
    ARM_D: "D · 파형 셔플 대조군 (음성 대조)",
    ARM_E: "E · Q4-N boost_fix 구조 진단용 (누수 제거)",
    COMB_BASELINE: "cleanComb · comb 로지스틱 (Q4-N cpu_comb 의 깨끗한 대응물)",
}


@dataclass
class RunBundle:
    """A read-only view of a finished run bundle."""

    run_dir: str
    config: dict
    manifest: dict
    result: dict
    fold_map: Dict[int, int]
    predictions: Dict[str, np.ndarray]
    training_history: Optional[list]
    seeds: List[int]
    records: List[int]
    idx_of: Dict[int, np.ndarray]
    y: np.ndarray

    @property
    def figures_dir(self) -> str:
        return os.path.join(self.run_dir, "figures")

    def arm_names(self) -> List[str]:
        known = [a for a in ARMS if a in self.result.get("arms", {})]
        if COMB_BASELINE in self.result.get("arms", {}):
            known.append(COMB_BASELINE)
        return known

    def logits(self, arm: str) -> np.ndarray:
        """Stored logits as ``(n_seed, n_sample)``; 1-D entries are broadcast."""
        key = f"logit_{arm}"
        if key not in self.predictions:
            raise Q4OError(f"predictions.npz has no '{key}'")
        arr = np.asarray(self.predictions[key])
        if arr.ndim == 1:                       # deterministic diagnostic arm
            arr = np.repeat(arr[None, :], len(self.seeds), axis=0)
        return arr


def bundle_fingerprint(run_dir: str) -> Dict[str, str]:
    """SHA256 of every file a report must never touch."""
    out: Dict[str, str] = {}
    for name in IMMUTABLE_BUNDLE_FILES:
        p = os.path.join(run_dir, name)
        if os.path.exists(p):
            out[name] = sha256_file(p)
    arms_dir = os.path.join(run_dir, "arms")
    if os.path.isdir(arms_dir):
        for arm in sorted(os.listdir(arms_dir)):
            p = os.path.join(arms_dir, arm, "probs.npy")
            if os.path.exists(p):
                out[f"arms/{arm}/probs.npy"] = sha256_file(p)
    return out


def load_run_bundle(run_dir: str) -> RunBundle:
    """Read a finished run bundle. Read-only — opens nothing for writing."""
    if not os.path.isdir(run_dir):
        raise Q4OError(f"run directory not found: {run_dir}")
    for name in ("result.json", "manifest.json", "config.json", "predictions.npz"):
        if not os.path.exists(os.path.join(run_dir, name)):
            raise Q4OError(f"{run_dir} is not a complete run bundle — missing {name}")

    def _json(name):
        with open(os.path.join(run_dir, name), encoding="utf-8") as fh:
            return json.load(fh)

    result, manifest, config = _json("result.json"), _json("manifest.json"), _json("config.json")
    fold_raw = (_json("fold_map.json")["record_to_fold"]
                if os.path.exists(os.path.join(run_dir, "fold_map.json")) else {})
    fold_map = {int(k): int(v) for k, v in fold_raw.items()}

    with np.load(os.path.join(run_dir, "predictions.npz")) as npz:
        predictions = {k: npz[k] for k in npz.files}

    history_path = os.path.join(run_dir, "training_history.json")
    training_history = None
    if os.path.exists(history_path):
        training_history = _json("training_history.json")

    seeds = [int(s) for s in predictions["seeds"]]
    rid = np.asarray(predictions["record_id"]).astype(int)
    y = np.asarray(predictions["y_true"]).astype(bool)
    records = sorted(fold_map) if fold_map else sorted(set(rid.tolist()))
    idx_of = {int(r): np.where(rid == r)[0] for r in records}

    return RunBundle(run_dir=run_dir, config=config, manifest=manifest, result=result,
                     fold_map=fold_map, predictions=predictions,
                     training_history=training_history, seeds=seeds,
                     records=[int(r) for r in records], idx_of=idx_of, y=y)


def per_record_ksw(bundle: RunBundle, arm: str) -> np.ndarray:
    """``(n_seed, n_record)`` k-sweep achievement, recomputed from stored logits.

    Uses the same ``achievement_at`` the run used, so it reproduces result.json's
    summaries exactly rather than approximating them.
    """
    scores = bundle.logits(arm)
    out = np.empty((scores.shape[0], len(bundle.records)), float)
    for si in range(scores.shape[0]):
        row = scores[si]
        for ri, r in enumerate(bundle.records):
            idx = bundle.idx_of[int(r)]
            out[si, ri] = float(np.mean([achievement_at(row, idx, bundle.y, k)
                                         for k in K_SWEEP]))
    return out


def reconcile_report(bundle: RunBundle, tol: float = 1e-9) -> Dict[str, object]:
    """Check that the report's recomputation agrees with result.json.

    If this disagrees, the report is not describing the run and must not be trusted.
    """
    rows = []
    worst = 0.0
    for arm in bundle.arm_names():
        measured = bundle.result["arms"][arm]
        recomputed = per_record_ksw(bundle, arm)
        for si, per_seed in enumerate(measured["per_seed"]):
            got = float(recomputed[si].mean())
            want = float(per_seed["ksw"]["mean"])
            worst = max(worst, abs(got - want))
            rows.append({"arm": arm, "seed": int(per_seed["seed"]),
                         "result_json": want, "recomputed": got,
                         "abs_diff": abs(got - want)})
    return {"max_abs_diff": worst, "within_tolerance": bool(worst <= tol),
            "tolerance": tol, "n_checked": len(rows), "rows": rows}


def _contrast(bundle: RunBundle, name: str) -> Optional[dict]:
    return bundle.result.get("contrasts", {}).get(name)


def _arm_summary(bundle: RunBundle, arm: str) -> dict:
    """Seed-averaged headline numbers for one arm, read from result.json."""
    m = bundle.result["arms"][arm]
    per_seed = m["per_seed"]

    def seed_mean(key: str) -> float:
        return float(np.mean([s[key]["mean"] for s in per_seed]))

    sa = m["seed_averaged_ksw"]
    return {
        "arm": arm,
        "short": ARM_SHORT.get(arm, arm),
        "ksw_mean": float(sa["mean"]),
        "prauc": seed_mean("prauc"),
        "auroc": seed_mean("auroc"),
        "p10": float(sa["p10"]),
        "worst": float(sa["worst"]),
        "worst_record": int(sa["worst_record"]),
        "seed_sd": float(m.get("ksw_seed_std", 0.0)),
        "ach_by_k": {k: seed_mean(f"ach@{k}") for k in (30, 50, 100, 200, 300)
                     if f"ach@{k}" in per_seed[0]},
    }


def arm_metrics_rows(bundle: RunBundle) -> List[dict]:
    """One row per arm for arm_metrics.csv / arm_summary_table.png."""
    contrast_for = {ARM_B: "B_minus_A", ARM_C: "C_minus_A",
                    ARM_D: "D_minus_A", ARM_E: "E_minus_A"}
    a_mean = _arm_summary(bundle, ARM_A)["ksw_mean"]
    rows = []
    for arm in bundle.arm_names():
        s = _arm_summary(bundle, arm)
        if arm == ARM_A:
            s["delta_vs_A"], s["delta_source"] = 0.0, "baseline"
        else:
            c = _contrast(bundle, contrast_for.get(arm, ""))
            if c is not None:
                s["delta_vs_A"] = float(c["record_bootstrap"]["mean"])
                s["delta_source"] = "paired_contrast"
            else:
                # No paired contrast was measured for this arm. Report the plain
                # difference of means and say so, rather than passing it off as one.
                s["delta_vs_A"] = s["ksw_mean"] - a_mean
                s["delta_source"] = "mean_difference"
        rows.append(s)
    return rows


def _fold_diag_matrix(bundle: RunBundle, arm: str,
                      field: str) -> Tuple[np.ndarray, List[int], List[int]]:
    """``(seed x fold)`` matrix of a per-fold training diagnostic from manifest.json."""
    entries = (bundle.manifest.get("arm_alpha") or {}).get(arm)
    if not entries:
        return np.zeros((0, 0)), [], []
    seeds = [int(e["seed"]) for e in entries]
    folds = sorted({int(f["fold"]) for e in entries for f in e["folds"]})
    mat = np.full((len(seeds), len(folds)), np.nan)
    for si, e in enumerate(entries):
        for f in e["folds"]:
            mat[si, folds.index(int(f["fold"]))] = float(f.get(field, np.nan))
    return mat, seeds, folds


def training_stalled(bundle: RunBundle, arm: str = ARM_C) -> Dict[str, object]:
    """Did early stopping keep epoch 0 everywhere? A real limit on what a NO-GO proves."""
    mat, seeds, folds = _fold_diag_matrix(bundle, arm, "best_epoch")
    if mat.size == 0:
        return {"available": False}
    total = int(np.isfinite(mat).sum())
    zero = int((mat == 0).sum())
    return {"available": True, "arm": arm, "n_total": total, "n_best_epoch_zero": zero,
            "all_zero": bool(zero == total and total > 0),
            "fraction": float(zero / max(1, total))}


# ─────────────────────────────────────────────────────────────────────────────
# Reporting — Korean executive summary
# ─────────────────────────────────────────────────────────────────────────────
def _fmt_ci(c: Optional[dict], digits: int = 4) -> str:
    if c is None:
        return "해당 대비 없음"
    b = c["record_bootstrap"]
    return (f"{b['mean']:+.{digits}f} "
            f"[95% CI {b['ci_low']:+.{digits}f}, {b['ci_high']:+.{digits}f}]")


def executive_summary_ko(bundle: RunBundle) -> str:
    """The first thing a human should read. Every number comes from result.json."""
    res = bundle.result
    gates = res["gates"]
    verdict = gates["verdict"]
    a = _arm_summary(bundle, ARM_A)
    c = _arm_summary(bundle, ARM_C)
    ca, cd = _contrast(bundle, "C_minus_A"), _contrast(bundle, "C_minus_D")
    ec = _contrast(bundle, "E_minus_combBaseline")
    passed = [k for k, v in gates["checks"].items() if v]
    failed = [k for k, v in gates["checks"].items() if not v]
    stalled = training_stalled(bundle, ARM_C)
    n_seed = len(bundle.seeds)

    L: List[str] = []
    L.append("=" * 78)
    L.append(f"  {res['experiment_id']} / {res['arm_id']} — Executive Summary")
    L.append(f"  run: {os.path.basename(bundle.run_dir)}")
    L.append("=" * 78)
    L.append("")
    L.append(f"■ 최종 판정: {verdict}")
    L.append(f"   사전 등록된 6개 gate 중 {len(passed)}개 통과 / {len(failed)}개 실패."
             f"  (판정 기준은 실행 전에 고정되었고, 결과를 보고 바꾸지 않았다.)")
    L.append("")
    L.append("■ morphology baseline (Arm A) — 이번 실험이 지켜낸 기준선")
    L.append(f"   k-sweep 달성률 평균  {a['ksw_mean']:.4f}   "
             f"(record 매크로 PR-AUC {a['prauc']:.4f} · AUROC {a['auroc']:.4f})")
    L.append(f"   하위꼬리 p10 {a['p10']:.4f} · 최악 레코드 {a['worst_record']} "
             f"({a['worst']:.4f})")
    L.append(f"   ※ 이 값은 누수 없는 5-fold record-grouped CV 에서 측정됐다. "
             f"Q4-N 의 0.8445/0.8631/0.8492 와 같은 자리에 두고 비교하면 안 된다.")
    L.append("")
    L.append("■ 주 비교 — C(형태+원파형 잔차) − A(형태 단독)")
    L.append(f"   {_fmt_ci(ca)}")
    if ca is not None:
        L.append(f"   seed {ca['positive_seed_count']}/{n_seed} 개에서 양(+) 방향 · "
                 f"통과 기준은 평균 ≥ +{GATE_MIN_GAIN} 이고 CI 하한 > 0")
    L.append("")
    L.append("■ 음성 대조 — C − D(파형을 레코드 안에서 셔플한 동일 구조)")
    L.append(f"   {_fmt_ci(cd)}")
    L.append("   이 대비가 0 이면, C 가 얻은 것은 '박동 단위 파형 정보'가 아니다.")
    L.append("")
    if ec is not None:
        L.append("■ 진단 — E − cleanComb (Q4-N boost_fix 구조에서 잔차만의 효과)")
        L.append(f"   {_fmt_ci(ec)}")
        L.append("")
    L.append("■ 통과한 gate")
    for k in passed:
        L.append(f"   ✅ {k}")
    L.append("■ 실패한 gate")
    for k in failed:
        L.append(f"   ❌ {k}")
    L.append("")

    L.append("■ 이 결과가 의미하는 것")
    if verdict == "NO-GO":
        L.append("   · 누수를 제거한 조건에서, 현재 박동의 원파형 잔차는 형태 baseline 위에")
        L.append("     사전 등록한 크기(+0.015)의 이득을 주지 못했다.")
        if cd is not None and abs(cd["record_bootstrap"]["mean"]) < GATE_MIN_GAIN:
            L.append("   · C 가 파형 셔플 대조군 D 를 유의하게 이기지 못했다. 즉 C 의 점수는")
            L.append("     박동 단위 파형 정보에서 온 것이라고 말할 근거가 없다.")
        L.append("   · morphology baseline 은 유지된다. 이것이 현재까지 확립된 유일한 축이다.")
        L.append("   · Q4-N 의 boost_fix=0.8631 이 '개선'이 아니었다는 것과 정합적이다 —")
        L.append("     그 값은 80% 가 in-sample 인 offset 위에서 계산된 값이었다.")
    else:
        L.append("   · 사전 등록한 6개 기준을 모두 만족했다. 다만 이는 SVDB 한 데이터셋,")
        L.append("     한 프로토콜에서의 결과다.")
    L.append("")

    L.append("■ 이 결과가 증명하지 않는 것")
    L.append("   · '원파형에 S 판별 정보가 없다'는 것을 증명하지 않는다. 증명한 것은")
    L.append("     '이 구조·이 학습 스케줄·이 offset 에서 추가 이득이 없었다'는 것뿐이다.")
    if stalled.get("available") and stalled.get("all_zero"):
        L.append(f"   · ★ 중요 — Arm C 는 {stalled['n_total']}개 (seed × fold) 전부에서")
        L.append("     best_epoch = 0 이었다. 즉 dev BCE 손실 기준으로 1 epoch 이후 어떤")
        L.append("     지점도 epoch 0 보다 낫지 않았고, 잔차 분기는 사실상 학습되기 전의")
        L.append("     체크포인트로 되돌아갔다. 따라서 이 NO-GO 는 '잔차가 쓸모없다'가")
        L.append("     아니라 '이 스케줄에서는 잔차가 켜지지 않았다'에 더 가깝다.")
        L.append("     학습률·epoch 수·early stopping 기준은 다음 실험의 1순위 점검 대상이다.")
    L.append("   · Transformer 나 더 큰 fusion 모델이 실패한다는 것을 증명하지 않는다.")
    L.append("     동시에, 그것을 시도할 근거가 생겼다는 뜻도 전혀 아니다.")
    L.append("   · MIT-BIH DS1→DS2 에서의 결과를 예측하지 않는다. 이 실험은 SVDB 다.")
    L.append("")

    L.append("■ 권장 다음 행동")
    if verdict == "NO-GO":
        L.append("   1. Transformer·대형 fusion 모델로 가지 않는다 (사전 등록된 중단 규칙).")
        L.append("   2. morphology baseline 을 확정 기준선으로 고정하고 기록한다.")
        if stalled.get("available") and stalled.get("all_zero"):
            L.append("   3. 그 전에, 잔차 분기가 학습조차 안 된 것이 스케줄 문제인지 확인한다")
            L.append("      (learning rate / epoch 수 / early stopping 기준). 이는 새 가설이")
            L.append("      아니라 이번 실행의 타당성 점검이므로, 별도 spec 으로 사전 등록한다.")
            L.append("   4. 그다음 실패 레코드·하위꼬리 분석으로 돌아간다"
                     " (patient_delta_waterfall.png 참조).")
        else:
            L.append("   3. 실패 레코드·하위꼬리 분석으로 돌아간다"
                     " (patient_delta_waterfall.png 참조).")
    else:
        L.append("   1. Transformer 로 가지 않는다. 같은 최소 잔차 구조를 MIT-BIH")
        L.append("      DS1→DS2 · S PR-AUC 프로토콜로 이식한다.")
    L.append("")
    L.append(f"■ 재현 정보 — data sha256 "
             f"{str(bundle.manifest.get('data', {}).get('sha256', 'n/a'))[:16]}… · "
             f"git {str(bundle.manifest.get('git_commit_sha', 'n/a'))[:10]} · "
             f"seeds {bundle.seeds}")
    L.append("=" * 78)
    return "\n".join(L)


# ─────────────────────────────────────────────────────────────────────────────
# Reporting — figures. All axis text is English (Colab has no CJK font by default).
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


def fig_arm_summary_table(bundle: RunBundle) -> List[str]:
    """arm_summary_table.png + arm_metrics.csv"""
    import csv
    plt = _plt()
    rows = arm_metrics_rows(bundle)
    fig_dir = bundle.figures_dir
    csv_path = os.path.join(fig_dir, "arm_metrics.csv")
    cols = ["arm", "short", "ksw_mean", "delta_vs_A", "delta_source", "prauc",
            "auroc", "p10", "worst", "worst_record", "seed_sd"]
    with open(csv_path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow(r)

    header = ["arm", "k-sweep", "Δ vs A", "PR-AUC", "AUROC", "p10", "worst (rec)", "seed SD"]
    body = []
    for r in rows:
        delta = "—" if r["delta_source"] == "baseline" else f"{r['delta_vs_A']:+.4f}"
        if r["delta_source"] == "mean_difference":
            delta += "*"
        body.append([r["short"], f"{r['ksw_mean']:.4f}", delta, f"{r['prauc']:.4f}",
                     f"{r['auroc']:.4f}", f"{r['p10']:.4f}",
                     f"{r['worst']:.3f} (#{r['worst_record']})", f"{r['seed_sd']:.4f}"])

    fig, ax = plt.subplots(figsize=(11, 0.55 * len(body) + 1.9))
    ax.axis("off")
    tbl = ax.table(cellText=body, colLabels=header, loc="center", cellLoc="center")
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(9)
    tbl.scale(1, 1.5)
    for j in range(len(header)):
        tbl[0, j].set_facecolor("#dfe6ee")
        tbl[0, j].set_text_props(weight="bold")
    for i, r in enumerate(rows, start=1):
        if r["arm"] == ARM_C:
            for j in range(len(header)):
                tbl[i, j].set_facecolor("#fff3cd")
        elif r["arm"] == ARM_A:
            for j in range(len(header)):
                tbl[i, j].set_facecolor("#e8f4ea")
    ax.set_title(f"{EXPERIMENT_ID} / {ARM_ID} — arm summary "
                 f"(seed-averaged over {len(bundle.seeds)} seeds)\n"
                 f"A = morphology baseline (green), C = primary arm (yellow); "
                 f"* = mean difference, not a paired contrast",
                 fontsize=10, pad=14)
    return [_save(fig, os.path.join(fig_dir, "arm_summary_table.png")), csv_path]


def fig_primary_contrasts_zoom(bundle: RunBundle) -> List[str]:
    """primary_contrasts_zoom.png — only the small, decision-relevant contrasts."""
    plt = _plt()
    gates = bundle.result["gates"]["checks"]
    spec = [("C_minus_A", "C - A  (primary)",
             bool(gates.get("1_mean_gain_ge_0.015") and gates.get("2_ci_lower_gt_0"))),
            ("C_minus_D", "C - D  (negative control)",
             bool(gates.get("3_beats_shuffle_control"))),
            ("E_minus_combBaseline", "E - cleanComb  (diagnostic)", None)]
    items = [(name, label, ok) for name, label, ok in spec
             if _contrast(bundle, name) is not None]

    fig, ax = plt.subplots(figsize=(10, 1.15 * len(items) + 2.4))
    ys = np.arange(len(items))
    for i, (name, label, gate_ok) in enumerate(items):
        b = _contrast(bundle, name)["record_bootstrap"]
        colour = "tab:gray" if gate_ok is None else ("tab:green" if gate_ok else "tab:red")
        ax.errorbar(b["mean"], i,
                    xerr=[[b["mean"] - b["ci_low"]], [b["ci_high"] - b["mean"]]],
                    fmt="o", capsize=6, color=colour, markersize=9, lw=2)
        tag = "DIAGNOSTIC" if gate_ok is None else ("PASS" if gate_ok else "FAIL")
        ax.annotate(f"  {b['mean']:+.4f} [{b['ci_low']:+.4f}, {b['ci_high']:+.4f}]   {tag}",
                    xy=(b["ci_high"], i), xytext=(6, 0), textcoords="offset points",
                    va="center", fontsize=9,
                    color=colour, fontweight="bold")
    ax.axvline(0.0, color="k", lw=1.2, label="zero (no effect)")
    ax.axvline(GATE_MIN_GAIN, color="tab:blue", ls="--", lw=1.2,
               label=f"gate +{GATE_MIN_GAIN}")
    ax.set_yticks(ys)
    ax.set_yticklabels([label for _, label, _ in items], fontsize=9)
    ax.set_ylim(-0.7, len(items) - 0.3)
    ax.set_xlabel("paired difference in record-level k-sweep achievement "
                  "(95% CI, record bootstrap)")
    ax.set_title("Primary contrasts only — plotted on their own scale.\n"
                 "Large reference gaps (e.g. B - A) are in reference_gap_separate.png "
                 "so they cannot flatten this axis.", fontsize=10)
    ax.legend(fontsize=8, loc="lower right")
    ax.grid(alpha=0.3, axis="x")
    lo = min(_contrast(bundle, n)["record_bootstrap"]["ci_low"] for n, _, _ in items)
    hi = max(_contrast(bundle, n)["record_bootstrap"]["ci_high"] for n, _, _ in items)
    pad = max((hi - lo) * 0.55, 0.01)
    ax.set_xlim(min(lo, -0.005) - pad * 0.2, max(hi, GATE_MIN_GAIN) + pad)
    return [_save(fig, os.path.join(bundle.figures_dir, "primary_contrasts_zoom.png"))]


def fig_reference_gap_separate(bundle: RunBundle) -> List[str]:
    """reference_gap_separate.png — the large gaps, on their own axis."""
    plt = _plt()
    items = [(n, n.replace("_minus_", " - ")) for n in REFERENCE_CONTRASTS
             if _contrast(bundle, n) is not None]
    if not items:
        return []
    fig, ax = plt.subplots(figsize=(10, 1.0 * len(items) + 2.2))
    for i, (name, label) in enumerate(items):
        b = _contrast(bundle, name)["record_bootstrap"]
        ax.errorbar(b["mean"], i,
                    xerr=[[b["mean"] - b["ci_low"]], [b["ci_high"] - b["mean"]]],
                    fmt="s", capsize=6, color="tab:purple", markersize=8, lw=2)
        ax.annotate(f"  {b['mean']:+.4f} [{b['ci_low']:+.4f}, {b['ci_high']:+.4f}]",
                    xy=(b["mean"], i), xytext=(8, 10), textcoords="offset points",
                    fontsize=9)
    ax.axvline(0.0, color="k", lw=1.2)
    ax.axvline(GATE_MIN_GAIN, color="tab:blue", ls="--", lw=1.0,
               label=f"gate +{GATE_MIN_GAIN} (for scale)")
    ax.set_yticks(np.arange(len(items)))
    ax.set_yticklabels([lab for _, lab in items], fontsize=9)
    ax.set_ylim(-0.7, len(items) - 0.3)
    ax.set_xlabel("paired difference in record-level k-sweep achievement (95% CI)")
    ax.set_title("Reference gaps — separate axis.\n"
                 "B - A is orders of magnitude larger than the primary contrasts; "
                 "sharing an axis would render those invisible.", fontsize=10)
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3, axis="x")
    return [_save(fig, os.path.join(bundle.figures_dir, "reference_gap_separate.png"))]


def fig_achievement_by_k(bundle: RunBundle) -> List[str]:
    """achievement_by_k.png — achievement@k per arm, plus a zoomed C - A panel."""
    plt = _plt()
    arms = [a for a in (ARM_A, ARM_C, ARM_D, ARM_E) if a in bundle.result["arms"]]
    summaries = {a: _arm_summary(bundle, a) for a in arms}
    ks = sorted(summaries[arms[0]]["ach_by_k"])
    if not ks:
        return []
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.4))
    colours = {ARM_A: "tab:green", ARM_C: "tab:orange",
               ARM_D: "tab:gray", ARM_E: "tab:blue"}
    for a in arms:
        axes[0].plot(ks, [summaries[a]["ach_by_k"][k] for k in ks], "o-",
                     label=ARM_SHORT.get(a, a), color=colours.get(a), lw=2)
    axes[0].set_xscale("log")
    axes[0].set_xticks(ks)
    axes[0].set_xticklabels([str(k) for k in ks])
    axes[0].set_xlabel("k (top-k beats reviewed per record)")
    axes[0].set_ylabel("achievement @ k")
    axes[0].set_title("Achievement vs k — all arms", fontsize=10)
    axes[0].legend(fontsize=8)
    axes[0].grid(alpha=0.3)

    if ARM_C in summaries:
        d = [summaries[ARM_C]["ach_by_k"][k] - summaries[ARM_A]["ach_by_k"][k] for k in ks]
        axes[1].axhline(0.0, color="k", lw=1.2)
        axes[1].axhline(GATE_MIN_GAIN, color="tab:blue", ls="--", lw=1.0,
                        label=f"gate +{GATE_MIN_GAIN}")
        axes[1].plot(ks, d, "o-", color="tab:orange", lw=2, label="C - A")
        axes[1].set_xscale("log")
        axes[1].set_xticks(ks)
        axes[1].set_xticklabels([str(k) for k in ks])
        axes[1].set_xlabel("k")
        axes[1].set_ylabel("C - A (achievement @ k)")
        axes[1].set_title("Zoom: C - A at each k\n"
                          "(difference of seed-averaged means, not a paired CI)",
                          fontsize=10)
        axes[1].legend(fontsize=8)
        axes[1].grid(alpha=0.3)
    return [_save(fig, os.path.join(bundle.figures_dir, "achievement_by_k.png"))]


def fig_seed_effects(bundle: RunBundle) -> List[str]:
    """seed_effects.png — per-seed C - A and C - D."""
    plt = _plt()
    ca, cd = _contrast(bundle, "C_minus_A"), _contrast(bundle, "C_minus_D")
    if ca is None:
        return []
    seeds = bundle.seeds
    x = np.arange(len(seeds))
    fig, ax = plt.subplots(figsize=(10, 4.2))
    w = 0.36
    ax.bar(x - w / 2, ca["by_seed"], w, label="C - A",
           color=["tab:green" if v > 0 else "tab:red" for v in ca["by_seed"]])
    if cd is not None:
        ax.bar(x + w / 2, cd["by_seed"], w, label="C - D",
               color=["#7fb98a" if v > 0 else "#d99a9a" for v in cd["by_seed"]])
    ax.axhline(0.0, color="k", lw=1.2)
    ax.axhline(GATE_MIN_GAIN, color="tab:blue", ls="--", lw=1.2,
               label=f"gate +{GATE_MIN_GAIN}")
    ax.set_xticks(x)
    ax.set_xticklabels([str(s) for s in seeds], fontsize=8)
    ax.set_xlabel("training seed")
    ax.set_ylabel("paired difference (k-sweep)")
    pos = ca["positive_seed_count"]
    ax.set_title(f"Per-seed direction — {pos} of {len(seeds)} seeds positive for C - A "
                 f"(gate needs >= {GATE_MIN_SEED_AGREE})", fontsize=10)
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3, axis="y")
    return [_save(fig, os.path.join(bundle.figures_dir, "seed_effects.png"))]


def fig_fold_training_diagnostics(bundle: RunBundle) -> List[str]:
    """fold_training_diagnostics.png — seed x fold heatmaps of alpha/best_epoch/dev_loss."""
    plt = _plt()
    arms = [a for a in (ARM_C, ARM_D, ARM_E)
            if (bundle.manifest.get("arm_alpha") or {}).get(a)]
    if not arms:
        return []
    fields = [("alpha", "alpha (learned residual scale)", "viridis"),
              ("best_epoch", "best_epoch (early-stopping pick)", "magma"),
              ("dev_loss", "dev BCE loss at the chosen epoch", "cividis")]
    fig, axes = plt.subplots(len(arms), len(fields),
                             figsize=(4.3 * len(fields), 2.9 * len(arms)),
                             squeeze=False)
    for i, arm in enumerate(arms):
        for j, (field, title, cmap) in enumerate(fields):
            mat, seeds, folds = _fold_diag_matrix(bundle, arm, field)
            ax = axes[i][j]
            if mat.size == 0:
                ax.axis("off")
                continue
            im = ax.imshow(mat, cmap=cmap, aspect="auto")
            for r in range(mat.shape[0]):
                for c in range(mat.shape[1]):
                    v = mat[r, c]
                    txt = "n/a" if not np.isfinite(v) else (
                        f"{int(v)}" if field == "best_epoch" else f"{v:.3f}")
                    ax.text(c, r, txt, ha="center", va="center", fontsize=7,
                            color="w" if field != "alpha" else "k")
            ax.set_xticks(np.arange(len(folds)))
            ax.set_xticklabels([f"f{f}" for f in folds], fontsize=7)
            ax.set_yticks(np.arange(len(seeds)))
            ax.set_yticklabels([str(s)[-2:] for s in seeds], fontsize=7)
            if j == 0:
                ax.set_ylabel(f"{ARM_SHORT.get(arm, arm)}\nseed", fontsize=9)
            if i == 0:
                ax.set_title(title, fontsize=9)
            fig.colorbar(im, ax=ax, fraction=0.046)

    stalled = training_stalled(bundle, ARM_C)
    if stalled.get("available") and stalled.get("all_zero"):
        fig.suptitle(
            f"WARNING — Arm C selected best_epoch = 0 in "
            f"{stalled['n_best_epoch_zero']}/{stalled['n_total']} (seed x fold). "
            f"No epoch after the first beat epoch 0 on dev BCE loss, so the residual "
            f"branch reverted to its near-initial state.\n"
            f"The NO-GO therefore reflects 'the residual never switched on under this "
            f"schedule', not 'the raw waveform carries nothing'.",
            fontsize=10, color="tab:red", y=1.02)
    return [_save(fig, os.path.join(bundle.figures_dir,
                                    "fold_training_diagnostics.png"))]


def fig_patient_delta_waterfall(bundle: RunBundle) -> Tuple[List[str], List[dict]]:
    """patient_delta_waterfall.png + patient_delta.csv — mean over ALL seeds."""
    import csv
    plt = _plt()
    ksw_a = per_record_ksw(bundle, ARM_A)
    ksw_c = per_record_ksw(bundle, ARM_C)
    # Mean across every seed, not a single seed.
    delta = (ksw_c - ksw_a).mean(axis=0)
    a_mean, c_mean = ksw_a.mean(axis=0), ksw_c.mean(axis=0)
    burden = bundle.manifest.get("record_burden", {})

    rows = []
    for ri, r in enumerate(bundle.records):
        idx = bundle.idx_of[int(r)]
        rows.append({
            "record": int(r),
            "fold": int(bundle.fold_map.get(int(r), -1)),
            "n_beat": int(len(idx)),
            "n_s": int(bundle.y[idx].sum()),
            "s_burden": float(burden.get(str(int(r)), float(bundle.y[idx].mean()))),
            "ksw_A": float(a_mean[ri]),
            "ksw_C": float(c_mean[ri]),
            "delta_C_minus_A": float(delta[ri]),
            "n_seed_averaged": int(ksw_a.shape[0]),
        })
    rows.sort(key=lambda d: d["delta_C_minus_A"])
    csv_path = os.path.join(bundle.figures_dir, "patient_delta.csv")
    with open(csv_path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

    d = np.array([r["delta_C_minus_A"] for r in rows])
    fig, ax = plt.subplots(figsize=(max(10, 0.20 * len(rows)), 4.4))
    ax.bar(np.arange(len(rows)), d,
           color=["tab:red" if v < 0 else "tab:blue" for v in d])
    ax.axhline(0.0, color="k", lw=1.0)
    ax.axhline(GATE_MIN_GAIN, color="tab:green", ls="--", lw=1.0,
               label=f"gate +{GATE_MIN_GAIN}")
    ax.set_xticks(np.arange(len(rows)))
    ax.set_xticklabels([str(r["record"]) for r in rows], rotation=90, fontsize=6)
    ax.set_xlabel("record (sorted by delta)")
    ax.set_ylabel("C - A (k-sweep)")
    n_pos = int((d > 0).sum())
    ax.set_title(f"Per-record C - A, averaged over all {ksw_a.shape[0]} seeds — "
                 f"{n_pos}/{len(rows)} records improve", fontsize=10)
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3, axis="y")
    return [_save(fig, os.path.join(bundle.figures_dir,
                                    "patient_delta_waterfall.png")), csv_path], rows


def fig_metric_distribution(bundle: RunBundle) -> List[str]:
    """metric_distribution.png — per-record k-sweep distribution for A / C / D."""
    plt = _plt()
    arms = [a for a in (ARM_A, ARM_C, ARM_D) if a in bundle.result["arms"]]
    data = {a: per_record_ksw(bundle, a).mean(axis=0) for a in arms}

    fig, ax = plt.subplots(figsize=(9, 5))
    pos = np.arange(len(arms)) + 1
    parts = ax.violinplot([data[a] for a in arms], positions=pos, showextrema=False,
                          widths=0.75)
    for pc in parts["bodies"]:
        pc.set_facecolor("#b9cfe3")
        pc.set_alpha(0.55)
    ax.boxplot([data[a] for a in arms], positions=pos, widths=0.22, showfliers=False)
    rng = np.random.RandomState(0)
    for i, a in enumerate(arms):
        v = data[a]
        ax.scatter(pos[i] + rng.uniform(-0.13, 0.13, len(v)), v, s=13, alpha=0.65,
                   color="tab:blue", zorder=3)
        p10, med = float(np.percentile(v, 10)), float(np.median(v))
        ax.hlines(p10, pos[i] - 0.4, pos[i] + 0.4, color="tab:red", lw=1.8,
                  label="p10 (lower tail)" if i == 0 else None)
        ax.hlines(med, pos[i] - 0.4, pos[i] + 0.4, color="tab:green", lw=1.8,
                  label="median" if i == 0 else None)
        ax.annotate(f"p10 {p10:.3f}\nmed {med:.3f}", xy=(pos[i] + 0.42, p10),
                    fontsize=8, va="center")
    ax.set_xticks(pos)
    ax.set_xticklabels([ARM_SHORT.get(a, a) for a in arms])
    ax.set_ylabel("per-record k-sweep achievement (seed-averaged)")
    ax.set_title(f"Per-record distribution over {len(bundle.records)} records — "
                 f"the mean hides the tail", fontsize=10)
    ax.legend(fontsize=8, loc="lower left")
    ax.grid(alpha=0.3, axis="y")
    return [_save(fig, os.path.join(bundle.figures_dir, "metric_distribution.png"))]


def fig_learning_curves(bundle: RunBundle) -> List[str]:
    """learning_curves.png — only when the run actually recorded a training history.

    Runs produced before history recording existed have none. Nothing is fabricated;
    the report states the absence instead.
    """
    if not bundle.training_history:
        return []
    plt = _plt()
    hist = bundle.training_history
    arms = sorted({h["arm"] for h in hist})
    fields = [("train_loss", "train BCE loss"), ("dev_loss", "dev BCE loss"),
              ("dev_prauc", "dev PR-AUC"), ("alpha", "alpha")]
    fig, axes = plt.subplots(len(arms), len(fields),
                             figsize=(3.6 * len(fields), 2.7 * len(arms)), squeeze=False)
    for i, arm in enumerate(arms):
        for j, (field, title) in enumerate(fields):
            ax = axes[i][j]
            plotted = False
            for h in hist:
                if h["arm"] != arm:
                    continue
                ep = [e["epoch"] for e in h["epochs"]]
                vals = [e.get(field) for e in h["epochs"]]
                if any(v is None for v in vals):
                    continue
                ax.plot(ep, vals, lw=1.0, alpha=0.7)
                plotted = True
            if not plotted:
                ax.text(0.5, 0.5, "not recorded", ha="center", va="center",
                        fontsize=8, transform=ax.transAxes)
            ax.set_xlabel("epoch", fontsize=8)
            if j == 0:
                ax.set_ylabel(f"{ARM_SHORT.get(arm, arm)}", fontsize=9)
            if i == 0:
                ax.set_title(title, fontsize=9)
            ax.grid(alpha=0.3)
    fig.suptitle("Learning curves — one line per (seed, fold). "
                 "Checkpoint selection uses dev BCE loss only.", fontsize=10, y=1.01)
    return [_save(fig, os.path.join(bundle.figures_dir, "learning_curves.png"))]


# ─────────────────────────────────────────────────────────────────────────────
# Reporting — orchestration
# ─────────────────────────────────────────────────────────────────────────────
def _report_markdown(bundle: RunBundle, figures: List[str], patient_rows: List[dict],
                     recon: Dict[str, object]) -> str:
    res = bundle.result
    gates = res["gates"]
    a = _arm_summary(bundle, ARM_A)
    ca, cd = _contrast(bundle, "C_minus_A"), _contrast(bundle, "C_minus_D")
    ec = _contrast(bundle, "E_minus_combBaseline")
    stalled = training_stalled(bundle, ARM_C)
    rows = arm_metrics_rows(bundle)

    L: List[str] = []
    L.append(f"# {res['experiment_id']} / {res['arm_id']} — 결과 보고서")
    L.append("")
    L.append(f"- run: `{os.path.basename(bundle.run_dir)}`")
    L.append(f"- 최종 판정: **{gates['verdict']}**")
    L.append(f"- 주 지표: record 단위 k-sweep 달성률 평균 "
             f"(k = {bundle.config.get('k_sweep')})")
    L.append(f"- seed {len(bundle.seeds)}개 · record {len(bundle.records)}개 "
             f"· fold {bundle.config.get('n_outer_folds')}개")
    L.append(f"- data sha256 `{bundle.manifest.get('data', {}).get('sha256', 'n/a')}`")
    L.append(f"- git commit `{bundle.manifest.get('git_commit_sha', 'n/a')}`")
    L.append("")
    L.append("> 이 문서는 **표현(presentation) 전용**이다. 측정값은 `result.json` 에서")
    L.append("> 그대로 읽었고, arm·fold·seed·지표·bootstrap·gate 는 전혀 바꾸지 않았다.")
    L.append("")

    L.append("## 1. Executive Summary")
    L.append("")
    L.append("```text")
    L.append(executive_summary_ko(bundle))
    L.append("```")
    L.append("")

    L.append("## 2. baseline 정의")
    L.append("")
    L.append(f"**Arm A = morphology baseline** — Q4-N 의 `morph` arm 을 그대로 동결한 것"
             f"(`F_BASE` RR 9열 ⊕ `MORPH` 형태 8열 = 17열), 로지스틱 회귀.")
    L.append(f"모든 scaler 와 model 은 outer-train 에서만 적합하고, outer-test 예측은")
    L.append(f"해당 test record 를 한 번도 보지 않은 모델이 만든다.")
    L.append("")
    L.append(f"- k-sweep 달성률 평균 **{a['ksw_mean']:.4f}**")
    L.append(f"- record 매크로 PR-AUC {a['prauc']:.4f} · AUROC {a['auroc']:.4f}")
    L.append(f"- 하위꼬리 p10 {a['p10']:.4f} · 최악 레코드 #{a['worst_record']} "
             f"({a['worst']:.4f})")
    port = bundle.manifest.get("morph_port_check", {})
    if port.get("measured_loro_ksw") is not None:
        L.append("")
        L.append(f"이식 충실도 확인: 같은 특징을 Q4-N 의 LORO 프로토콜로 다시 채점하면 "
                 f"**{port['measured_loro_ksw']:.4f}** 로, Q4-N 이 보고한 "
                 f"`morph` {port['reference_q4n_morph_ksw_loro']:.4f} 와 "
                 f"delta {port.get('delta', float('nan')):+.4f} 이다 "
                 f"(허용치 {port.get('tolerance')}). 형태 특징 이식은 검증됐다.")
    L.append("")

    L.append("## 3. Q4-N 의 0.8631 을 baseline 에서 제외한 이유")
    L.append("")
    L.append("Q4-N 의 `cpu_fold()` 는 하나의 배열에 train 위치와 test 위치를 **둘 다** 썼고,")
    L.append("5개 fold 가 순차 실행되므로 뒤 fold 가 앞 fold 의 값을 덮어썼다.")
    L.append("")
    L.append("```python")
    L.append("sc[tr] = lr.decision_function((X[tr] - mu) / sd)   # in-sample, 덮어써짐")
    L.append("sc[te] = lr.decision_function((X[te] - mu) / sd)")
    L.append("```")
    L.append("")
    L.append("마지막 fold 이후 배열의 약 **80%** 가 in-sample 예측이다. 따라서")
    L.append("`cpu_comb=0.8445`, `boost_fix=0.8631`, `boost_rank=0.8492` 는 baseline 도")
    L.append("개선도 아니다. 잔차 CNN 은 학습 시 이미 그 박동들을 외운 offset 을 받았고,")
    L.append("테스트 시에는 깨끗한 offset 을 받았다 — offset 의 통계적 성격이 train 과")
    L.append("test 에서 서로 달랐다는 뜻이다. 이 값들은 Arm E 진단용 **오염된 참고값**")
    L.append("으로만 남긴다.")
    L.append("")
    L.append("반대로 Q4-N 의 **CPU arm** (`morph − base = +0.1570` 등) 은 별도의 `loro()`")
    L.append("경로를 썼고 이 버그의 영향을 받지 않는다.")
    L.append("")

    L.append("## 4. 구조 설명")
    L.append("")
    for arm in bundle.arm_names():
        L.append(f"- **{ARM_KO.get(arm, arm)}**")
    L.append("")
    L.append("`final_logit = morph_offset + alpha * cnn_residual` 이며 `alpha` 는 정확히 0")
    L.append("에서 출발한다(초기 상태가 baseline 과 동일 → 하한 보장). 잔차 head 는 xavier")
    L.append("초기화한다 — `alpha` 와 head 를 동시에 0 으로 두면 서로의 기울기를 0 에 가두는")
    L.append("Q4-N 의 초기화 데드락이 재현된다.")
    L.append("")
    L.append("offset 은 각 outer fold 안에서 **inner cross-fitting** 으로 만든다:")
    L.append("outer-train 의 각 샘플은 자신을 학습에 쓰지 않은 inner 모델의 예측을 정확히")
    L.append("한 번 받고, outer-test offset 은 outer-train 전체로 적합한 모델이 만든다.")
    L.append("")

    L.append("## 5. arm 요약")
    L.append("")
    L.append("| arm | k-sweep | Δ vs A | PR-AUC | AUROC | p10 | worst (record) | seed SD |")
    L.append("|---|---|---|---|---|---|---|---|")
    for r in rows:
        delta = "—" if r["delta_source"] == "baseline" else f"{r['delta_vs_A']:+.4f}"
        if r["delta_source"] == "mean_difference":
            delta += " \\*"
        L.append(f"| {r['short']} | {r['ksw_mean']:.4f} | {delta} | {r['prauc']:.4f} | "
                 f"{r['auroc']:.4f} | {r['p10']:.4f} | {r['worst']:.3f} "
                 f"(#{r['worst_record']}) | {r['seed_sd']:.4f} |")
    L.append("")
    L.append("\\* 짝지은 대비가 측정되지 않은 arm 은 평균의 차이로 표기했다.")
    L.append("")

    L.append("## 6. PASS / FAIL 근거")
    L.append("")
    L.append("| gate | 결과 | 측정값 |")
    L.append("|---|---|---|")
    ev = {
        "1_mean_gain_ge_0.015": (f"mean(C−A) = {ca['record_bootstrap']['mean']:+.4f}"
                                 f" vs 기준 +{GATE_MIN_GAIN}") if ca else "n/a",
        "2_ci_lower_gt_0": (f"CI 하한 = {ca['record_bootstrap']['ci_low']:+.4f}"
                            ) if ca else "n/a",
        "3_beats_shuffle_control": (
            f"mean(C−D) = {cd['record_bootstrap']['mean']:+.4f}, "
            f"CI 하한 {cd['record_bootstrap']['ci_low']:+.4f}") if cd else "n/a",
        "4_seed_direction_stable": (
            f"{ca['positive_seed_count']}/{len(bundle.seeds)} seed 양수, "
            f"기준 ≥ {GATE_MIN_SEED_AGREE}") if ca else "n/a",
        "5_lower_tail_not_worse": (
            f"p10 A {a['p10']:.4f} → C "
            f"{_arm_summary(bundle, ARM_C)['p10']:.4f}, 허용 하락 "
            f"{GATE_LOWER_TAIL_MAX_DROP}"),
        "6_leakage_and_reproducibility": "모든 누수 assertion 통과 (실패 시 실행 자체가 중단)",
    }
    for k, v in gates["checks"].items():
        L.append(f"| `{k}` | {'✅ PASS' if v else '❌ FAIL'} | {ev.get(k, '')} |")
    L.append("")
    L.append(f"**판정: {gates['verdict']}** — {gates['next_step']}")
    L.append("")

    L.append("## 7. 환자(레코드) 단위 결과")
    L.append("")
    improve = sorted(patient_rows, key=lambda d: -d["delta_C_minus_A"])[:10]
    worsen = sorted(patient_rows, key=lambda d: d["delta_C_minus_A"])[:10]
    for title, subset in (("개선 상위 10", improve), ("악화 상위 10", worsen)):
        L.append(f"### {title}")
        L.append("")
        L.append("| record | S burden | n_S | A | C | Δ(C−A) |")
        L.append("|---|---|---|---|---|---|")
        for r in subset:
            L.append(f"| {r['record']} | {r['s_burden']:.4f} | {r['n_s']} | "
                     f"{r['ksw_A']:.4f} | {r['ksw_C']:.4f} | "
                     f"{r['delta_C_minus_A']:+.4f} |")
        L.append("")
    L.append(f"전체 표: [`figures/patient_delta.csv`](figures/patient_delta.csv) "
             f"(모든 값은 seed {len(bundle.seeds)}개 평균)")
    L.append("")

    L.append("## 8. 학습 진단")
    L.append("")
    if stalled.get("available"):
        L.append(f"Arm C 의 early stopping 이 고른 epoch: "
                 f"{stalled['n_best_epoch_zero']}/{stalled['n_total']} "
                 f"(seed × fold) 에서 `best_epoch = 0`.")
        if stalled.get("all_zero"):
            L.append("")
            L.append("> ⚠️ **전부 epoch 0 이다.** dev BCE 손실 기준으로 첫 epoch 이후 어떤")
            L.append("> 지점도 epoch 0 보다 낫지 않았다는 뜻이고, 잔차 분기는 사실상 학습되기")
            L.append("> 전 상태의 체크포인트로 되돌아갔다. 이 사실은 NO-GO 의 해석 범위를")
            L.append("> 좁힌다 — 이번 결과는 '원파형에 정보가 없다'가 아니라 '이 학습")
            L.append("> 스케줄에서 잔차가 켜지지 않았다'에 가깝다.")
    else:
        L.append("이 run 의 manifest 에 per-fold 학습 진단이 없다.")
    L.append("")
    if bundle.training_history:
        L.append("epoch 단위 학습 곡선: `figures/learning_curves.png`")
    else:
        L.append("**이 run 에는 epoch 단위 training history 가 없다.** history 기록 기능은")
        L.append("이번 개정에서 추가됐으므로 *이후* 실행부터 `training_history.json` 이")
        L.append("생성된다. 없는 데이터를 만들어내지 않았고, 학습 곡선도 그리지 않았다.")
    L.append("")

    L.append("## 9. 한계와 다음 결정")
    L.append("")
    L.append("- 이 결과는 **SVDB · record-grouped 5-fold** 한 프로토콜의 결과다. "
             "MIT-BIH DS1→DS2 를 예측하지 않는다.")
    L.append("- 절대값은 Q4-N 의 LORO 수치와 직접 비교할 수 없다(분할이 다르다). "
             "해석 대상은 Q4-O 내부의 짝지은 대비뿐이다.")
    L.append("- NO-GO 는 Transformer 나 더 큰 fusion 모델을 시도할 근거가 아니다. "
             "사전 등록된 중단 규칙이 이를 금지한다.")
    if stalled.get("all_zero"):
        L.append("- 다음 결정의 1순위는 **학습 스케줄 타당성 점검**이다"
                 "(learning rate · epoch 수 · early stopping 기준). "
                 "이는 새 과학적 가설이 아니라 이번 실행의 타당성 확인이므로, "
                 "별도 spec 으로 사전 등록한 뒤 진행한다.")
    L.append("- 그다음은 실패 레코드·하위꼬리 분석이다.")
    L.append("")

    L.append("## 10. 생성한 그림")
    L.append("")
    for p in figures:
        rel = os.path.relpath(p, bundle.run_dir)
        L.append(f"- [`{rel}`]({rel})")
    L.append("")

    L.append("## 11. 재현 확인")
    L.append("")
    L.append(f"보고서가 저장된 logit 에서 다시 계산한 arm별·seed별 k-sweep 평균과 "
             f"`result.json` 의 값의 최대 절대 오차: "
             f"**{recon['max_abs_diff']:.3e}** "
             f"({recon['n_checked']}개 비교, 허용치 {recon['tolerance']:.0e}) → "
             f"{'일치' if recon['within_tolerance'] else '불일치 — 보고서를 신뢰하지 말 것'}")
    L.append("")
    return "\n".join(L)


def generate_report(run_dir: str, log: Optional[RunLog] = None) -> Dict[str, object]:
    """Render a finished run bundle into figures, CSVs, and report_summary.md.

    Read-only with respect to the run's measured artifacts: it verifies that
    config/manifest/result/fold_map/predictions/probs are byte-identical before and
    after, and raises if anything moved.
    """
    log = log or RunLog()
    bundle = load_run_bundle(run_dir)
    before = bundle_fingerprint(run_dir)
    os.makedirs(bundle.figures_dir, exist_ok=True)

    log(f"reporting on {os.path.basename(run_dir)} — verdict "
        f"{bundle.result['gates']['verdict']}, {len(bundle.seeds)} seeds, "
        f"{len(bundle.records)} records")

    recon = reconcile_report(bundle)
    if not recon["within_tolerance"]:
        raise Q4OError(
            f"report recomputation disagrees with result.json by "
            f"{recon['max_abs_diff']:.3e} — the report would not be describing this run")
    log(f"reconciled against result.json — max abs diff {recon['max_abs_diff']:.3e}")

    figures: List[str] = []
    figures += fig_arm_summary_table(bundle)
    figures += fig_primary_contrasts_zoom(bundle)
    figures += fig_reference_gap_separate(bundle)
    figures += fig_achievement_by_k(bundle)
    figures += fig_seed_effects(bundle)
    figures += fig_fold_training_diagnostics(bundle)
    waterfall, patient_rows = fig_patient_delta_waterfall(bundle)
    figures += waterfall
    figures += fig_metric_distribution(bundle)
    curves = fig_learning_curves(bundle)
    figures += curves
    if not curves:
        log("no training_history.json in this run — learning curves skipped, "
            "nothing fabricated")

    md_path = os.path.join(bundle.figures_dir, "report_summary.md")
    with open(md_path, "w", encoding="utf-8") as fh:
        fh.write(_report_markdown(bundle, figures, patient_rows, recon))
    figures.append(md_path)
    log(f"wrote {len(figures)} report artifacts to {bundle.figures_dir}")

    after = bundle_fingerprint(run_dir)
    changed = [k for k in before if before[k] != after.get(k)]
    if changed:
        raise Q4OError(f"reporting modified measured artifacts: {changed}")
    log("verified — no measured artifact was modified by reporting")

    return {
        "run_dir": run_dir,
        "verdict": bundle.result["gates"]["verdict"],
        "executive_summary_ko": executive_summary_ko(bundle),
        "figures": figures,
        "report_markdown": md_path,
        "patient_rows": patient_rows,
        "reconciliation": {k: v for k, v in recon.items() if k != "rows"},
        "training_history_present": bool(bundle.training_history),
        "fingerprint_stable": True,
        "n_seed": len(bundle.seeds),
        "n_record": len(bundle.records),
    }


# ─────────────────────────────────────────────────────────────────────────────
# Synthetic fixture (CPU smoke only — never a substitute for the real data)
# ─────────────────────────────────────────────────────────────────────────────
def synthetic_cohort(n_record: int = 12, n_beat: int = 140, width: int = 300,
                     n_lead: int = 2, seed: int = 7,
                     signal: float = 1.0, n_unscorable: int = 0) -> Cohort:
    """Grouped synthetic beats with a record-varying S burden.

    Enough structure for leakage/shape/order tests and a CPU smoke run. It is not a
    physiological simulator and no result from it means anything scientifically.

    ``n_unscorable`` appends records that carry too few S beats to clear ``MIN_S``.
    Real SVDB has 22 such records out of 78, so their beats sit in the cohort while
    being absent from the fold map — set it to exercise that path.
    """
    rng = np.random.RandomState(seed)
    beats, ys, pres, posts, rids = [], [], [], [], []
    t = np.arange(width)
    for r in range(n_record + n_unscorable):
        scorable = r < n_record
        if scorable:
            burden = 0.10 + 0.30 * (r / max(1, n_record - 1))
            y = rng.rand(n_beat) < burden
            while int(y.sum()) < MIN_S or int((~y).sum()) < MIN_N:
                y = rng.rand(n_beat) < max(0.25, burden)
        else:
            # too few S beats to be scorable — mirrors SVDB's low-burden records
            y = np.zeros(n_beat, bool)
            y[rng.choice(n_beat, max(1, MIN_S // 5), replace=False)] = True
        qrs = np.exp(-0.5 * ((t - R_IDX) / 6.0) ** 2)
        pwave = np.exp(-0.5 * ((t - (R_IDX - 55)) / 9.0) ** 2)
        twave = np.exp(-0.5 * ((t - (R_IDX + 90)) / 18.0) ** 2)
        b = np.zeros((n_beat, n_lead, width), float)
        for l in range(n_lead):
            amp = 1.0 + 0.2 * l
            base = amp * qrs + 0.25 * twave
            b[:, l, :] = base[None, :]
            # S beats: attenuated / inverted P, otherwise identical morphology.
            # The margins are deliberately small and the noise large, so the metrics
            # do not saturate at 1.0 and the statistics code gets a real workout.
            p_amp = np.where(y, 0.04 * signal, 0.16 * signal)
            b[:, l, :] += p_amp[:, None] * pwave[None, :]
            b[:, l, :] += 0.12 * rng.randn(n_beat, width)
        pre = np.where(y, 0.68, 0.85) + 0.16 * rng.randn(n_beat)
        post = np.where(y, 0.98, 0.85) + 0.16 * rng.randn(n_beat)
        beats.append(b.astype("float32"))
        ys.append(y)
        pres.append(np.clip(pre, 0.25, 2.0))
        posts.append(np.clip(post, 0.25, 2.0))
        rids.append(np.full(n_beat, r, int))
    beat = np.concatenate(beats, 0)
    y = np.concatenate(ys, 0)
    rid = np.concatenate(rids, 0)
    n = len(y)
    cohort = Cohort(
        beat=beat, y=y, y3=np.where(y, IDX_S, 0), pre=np.concatenate(pres, 0),
        post=np.concatenate(posts, 0), rid=rid,
        sym=np.where(y, "A", "N").astype("<U2"),
        sample_id=np.arange(n, dtype=np.int64),
        records=np.array(sorted(set(rid.tolist())), dtype=int), idx_of={},
    )
    cohort.idx_of = {int(r): np.where(rid == r)[0] for r in cohort.records}
    return cohort


# ─────────────────────────────────────────────────────────────────────────────
# Orchestration
# ─────────────────────────────────────────────────────────────────────────────
def self_check(min_version: int = MODULE_VERSION) -> Dict[str, object]:
    """Prove **in-process** that the loaded module is the fixed one. Fast (~1s).

    Why this exists: in Colab, `import q4o_leakage_free_residual` is a no-op once the
    module is in ``sys.modules``. A ``git pull`` updates the file on disk but not the
    code the kernel is executing, and running the test script as a subprocess passes
    against the new file while the kernel still runs the old one — so the stale import
    stays invisible until the run dies minutes later.

    This runs the exact path that used to fail (a cohort containing records below
    MIN_S/MIN_N) inside the caller's interpreter, so a stale import raises here.
    """
    if MODULE_VERSION < min_version:
        raise Q4OError(
            f"loaded module is version {MODULE_VERSION} ({MODULE_BUILD}), but "
            f"version {min_version} is required. The kernel is running stale code — "
            f"re-import with importlib.reload(), or restart the runtime.")

    cohort = synthetic_cohort(n_record=6, n_beat=120, seed=1, n_unscorable=2)
    rec_ok = scorable_records(cohort)
    if len(rec_ok) >= len(cohort.records):
        raise Q4OError("self_check fixture produced no unscorable records")

    burden = record_burden(cohort, rec_ok)
    fold_map = make_fold_map(rec_ok, burden, n_folds=3)
    X = build_base_features(cohort)
    scored = samples_of(cohort, rec_ok)
    unscored = np.setdiff1d(np.arange(cohort.n), scored)

    # The old code raised here; completing at all is the proof.
    offsets = cross_fitted_offsets(X, cohort, fold_map, n_inner=3, n_outer=3,
                                   burden=burden)
    for f, off in offsets.items():
        if not np.all(np.isfinite(off[scored])):
            raise Q4OError(f"self_check: fold {f} offset is not finite on scored beats")
        if not np.all(np.isnan(off[unscored])):
            raise Q4OError(f"self_check: fold {f} scored a beat outside the cohort")

    a = run_logistic_arm(X, cohort, fold_map, n_outer=3)
    if not (np.all(np.isfinite(a[scored])) and np.all(np.isnan(a[unscored]))):
        raise Q4OError("self_check: Arm A coverage is wrong")

    return {
        "module_version": MODULE_VERSION,
        "module_build": MODULE_BUILD,
        "module_file": os.path.abspath(__file__),
        "n_record": int(len(cohort.records)),
        "n_scorable": int(len(rec_ok)),
        "n_scored_beats": int(len(scored)),
        "n_unscored_beats": int(len(unscored)),
        "ok": True,
    }


def run_experiment(cohort: Cohort, provenance: Dict[str, object], out_dir: str,
                   seeds: Sequence[int] = TRAIN_SEEDS, epochs: int = DL_EPOCH,
                   batch: int = DL_BATCH, n_boot: int = NB_BOOT,
                   device: Optional[str] = None, smoke: bool = False,
                   port_check: bool = False,
                   log: Optional[RunLog] = None) -> dict:
    """Run every arm, score, apply the gates, and write the run bundle."""
    log = log or RunLog()
    torch = _require_torch()
    device = device or ("cuda" if torch.cuda.is_available() else "cpu")
    det_notes = set_determinism(int(seeds[0]))

    log(f"{EXPERIMENT_ID} / {ARM_ID} — {RUN_SLUG}")
    log(f"device {device} · smoke={smoke} · seeds {list(seeds)} · epochs {epochs}")
    log("Q4-N cpu_comb/boost_fix/boost_rank are CONTAMINATED reference values, "
        "not baselines. See the spec Decision log.")

    # ── cohort and folds
    rec_ok = scorable_records(cohort)
    if len(rec_ok) < N_OUTER_FOLDS:
        raise Q4OError(f"only {len(rec_ok)} scorable records; need >= {N_OUTER_FOLDS}")
    burden = record_burden(cohort, rec_ok)
    fold_map = make_fold_map(rec_ok, burden)
    assert_fold_map_partition(fold_map, rec_ok, N_OUTER_FOLDS)
    scored_idx = samples_of(cohort, rec_ok)
    log(f"records {len(cohort.records)} · scorable {len(rec_ok)} · "
        f"scored beats {len(scored_idx)} of {cohort.n}")

    # ── features (frozen)
    t0 = time.time()
    feats = build_features(cohort, with_comb=True)
    log(f"features built in {time.time() - t0:.1f}s — dims {feats.dims}")

    if port_check:
        log("porting-fidelity check — re-scoring Arm A features under Q4-N's LORO")
        port_check_result = morph_port_check(feats, cohort, rec_ok, burden)
        # The Q4-N reference is an SVDB number. On fixture data the comparison is
        # meaningless, so say so instead of reporting a spurious failure.
        port_check_result["applicable"] = not smoke
        if smoke:
            port_check_result["within_tolerance"] = None
            port_check_result["note"] = (
                "Not applicable: this was a smoke run on synthetic fixture data. The "
                "0.8361 reference is an SVDB LORO value.")
        log(f"  measured LORO k-sweep {port_check_result['measured_loro_ksw']:.4f} vs "
            f"Q4-N {REF_Q4N['morph_ksw_loro']:.4f} "
            f"(delta {port_check_result['delta']:+.4f}, "
            f"within tolerance: {port_check_result['within_tolerance']})")
    else:
        port_check_result = {
            "reference_q4n_morph_ksw_loro": REF_Q4N["morph_ksw_loro"],
            "tolerance": MORPH_PORT_TOL,
            "status": "not_run (opt in with --port-check)",
        }

    # ── leakage-free offsets
    log("cross-fitting the morphology offset (Arm C/D)")
    off_morph = cross_fitted_offsets(feats.morph, cohort, fold_map, burden=burden, log=log)
    log("cross-fitting the comb offset (Arm E)")
    off_comb = cross_fitted_offsets(feats.comb, cohort, fold_map, burden=burden, log=log)

    # ── arm inputs
    x_current = current_beat_input(cohort)
    shuffled_beat, perm_rule = shuffle_waveforms_within_record(cohort)
    x_shuffled = current_beat_input(cohort, shuffled_beat)
    x_three = three_beat_input(cohort)
    log(f"Arm D permutation moved {perm_rule['moved_fraction']:.1%} of beats")

    # ── arms
    arm_scores: Dict[str, np.ndarray] = {}
    arm_diag: Dict[str, object] = {}

    log("Arm A — morph_baseline (logistic, outer-train fit only)")
    a_scores = run_logistic_arm(feats.morph, cohort, fold_map)
    arm_scores[ARM_A] = np.repeat(a_scores[None, :], len(seeds), axis=0)

    # Arm E's offset is the 28-column `comb` set, not Arm A's 17-column `morph` set, so
    # E - A would conflate the feature change with the residual. Score the comb
    # logistic on its own so Arm E's residual effect can be isolated. Diagnostic only;
    # it is not one of the five arms and never enters a gate.
    log("diagnostic — comb logistic baseline (isolates Arm E's residual effect)")
    comb_scores = run_logistic_arm(feats.comb, cohort, fold_map)

    # Invariant: Arm A's test scores are exactly the outer-test offsets used by C/D.
    for f, off in off_morph.items():
        te = samples_of(cohort, [r for r in fold_map if fold_map[r] == f])
        if not np.allclose(off[te], a_scores[te], atol=1e-8):
            raise Q4OError(f"Arm A test scores diverge from the fold {f} test offset")
    log("  invariant ok — Arm A test scores == Arm C/D outer-test offsets")

    nn_specs = [
        (ARM_B, x_current, None),
        (ARM_C, x_current, off_morph),
        (ARM_D, x_shuffled, off_morph),
        (ARM_E, x_three, off_comb),
    ]
    for arm, X, offs in nn_specs:
        log(f"Arm — {arm} ({X.shape[1]} channels)")
        rows, diags = [], []
        for s in seeds:
            sc, d = run_nn_arm(arm, X, offs, cohort, fold_map, int(s), burden,
                               device, epochs, batch, log=log)
            rows.append(sc)
            diags.append({"seed": int(s), "folds": d})
        arm_scores[arm] = np.vstack(rows)
        arm_diag[arm] = diags

    # ── metrics
    log("scoring")
    metrics: Dict[str, object] = {}
    per_seed_ksw: Dict[str, Dict[int, Dict[int, float]]] = {}
    scored_for_metrics = dict(arm_scores)
    scored_for_metrics["comb_baseline_diagnostic"] = np.repeat(
        comb_scores[None, :], len(seeds), axis=0)
    for arm in scored_for_metrics:
        rows = scored_for_metrics[arm]
        per_seed_ksw[arm] = {}
        seed_summaries = []
        for si, s in enumerate(seeds):
            pr = per_record_metrics(rows[si], cohort, rec_ok)
            per_seed_ksw[arm][int(s)] = pr["ksw"]
            seed_summaries.append({
                "seed": int(s),
                **{key: summarise(pr[key]) for key in pr},
            })
        # seed-averaged per-record primary metric
        avg = {r: float(np.mean([per_seed_ksw[arm][int(s)][r] for s in seeds]))
               for r in rec_ok}
        metrics[arm] = {
            "per_seed": seed_summaries,
            "seed_averaged_ksw": summarise(avg),
            "ksw_mean_by_seed": [sd["ksw"]["mean"] for sd in seed_summaries],
            "ksw_seed_std": float(np.std([sd["ksw"]["mean"] for sd in seed_summaries],
                                         ddof=1)) if len(seeds) > 1 else 0.0,
        }

    def paired(arm_x: str, arm_y: str) -> Dict[str, object]:
        """arm_x - arm_y, paired on the same record and the same seed."""
        by_rec_seed = {r: {int(s): per_seed_ksw[arm_x][int(s)][r]
                              - per_seed_ksw[arm_y][int(s)][r] for s in seeds}
                       for r in rec_ok}
        by_rec = {r: float(np.mean(list(by_rec_seed[r].values()))) for r in rec_ok}
        by_seed = [float(np.mean([by_rec_seed[r][int(s)] for r in rec_ok])) for s in seeds]
        boot = paired_record_bootstrap(by_rec, n_boot=n_boot)
        hier = hierarchical_bootstrap(by_rec_seed, n_boot=n_boot)
        return {"record_bootstrap": boot, "hierarchical_bootstrap": hier,
                "by_seed": by_seed,
                "positive_seed_count": int(sum(1 for v in by_seed if v > 0))}

    contrasts = {
        "C_minus_A": paired(ARM_C, ARM_A),
        "C_minus_D": paired(ARM_C, ARM_D),
        "B_minus_A": paired(ARM_B, ARM_A),
        "E_minus_A": paired(ARM_E, ARM_A),
        "D_minus_A": paired(ARM_D, ARM_A),
        # Arm E's residual effect, isolated from its larger offset feature set.
        "E_minus_combBaseline": paired(ARM_E, "comb_baseline_diagnostic"),
    }
    log("contrasts:")
    for name, c in contrasts.items():
        b = c["record_bootstrap"]
        log(f"  {name:<12} {b['mean']:+.4f} [{b['ci_low']:+.4f}, {b['ci_high']:+.4f}] "
            f"· seeds positive {c['positive_seed_count']}/{len(seeds)}")

    gates = evaluate_gates(
        contrasts["C_minus_A"]["record_bootstrap"],
        contrasts["C_minus_D"]["record_bootstrap"],
        contrasts["C_minus_A"]["by_seed"],
        p10_a=metrics[ARM_A]["seed_averaged_ksw"]["p10"],
        p10_c=metrics[ARM_C]["seed_averaged_ksw"]["p10"],
        leakage_ok=True,     # every assertion above raises rather than returning False
    )
    log(f"verdict {gates['verdict']} — {gates['checks']}")

    e_diag = {
        "arm_E_seed_averaged_ksw": metrics[ARM_E]["seed_averaged_ksw"]["mean"],
        "arm_A_seed_averaged_ksw": metrics[ARM_A]["seed_averaged_ksw"]["mean"],
        "comb_baseline_seed_averaged_ksw":
            metrics["comb_baseline_diagnostic"]["seed_averaged_ksw"]["mean"],
        "q4n_contaminated_reference": REF_Q4N["contaminated"],
        "residual_effect_isolated": contrasts["E_minus_combBaseline"]["record_bootstrap"],
        "interpretation": (
            "Diagnostic only. Q4-N's boost_fix=0.8631 was trained against an offset "
            "array that was ~80% in-sample and scored against cpu_comb=0.8445 computed "
            "on the same contaminated array. Arm E re-runs that structure with a "
            "cross-fitted offset. Compare Arm E against comb_baseline_diagnostic (the "
            "clean analogue of Q4-N's cpu_comb), not against Arm A — Arm E's offset is "
            "the 28-column comb set while Arm A's is the 17-column morph set, so E - A "
            "mixes the feature change with the residual. Arm E is NOT the primary "
            "result and NOT a baseline."
        ),
        "protocol_note": (
            "Q4-N's numbers came from a different split (LORO for the CPU arms, and a "
            "contaminated offset for the boost arms), so the absolute values are not "
            "directly comparable. Read the direction and the de-contamination gap, not "
            "the difference of the two numbers."
        ),
    }

    # ── artifacts
    timestamp = time.strftime("%Y%m%dT%H%M", time.gmtime())
    config = {
        "experiment_id": EXPERIMENT_ID, "arm_id": ARM_ID, "run_slug": RUN_SLUG,
        "smoke": bool(smoke),
        "split": "frozen record-grouped 5-fold CV",
        "n_outer_folds": N_OUTER_FOLDS, "n_inner_folds": N_INNER_FOLDS,
        "training_seeds": [int(s) for s in seeds],
        "waveform_permutation": perm_rule,
        "k_sweep": list(K_SWEEP), "k_operating_points": list(K_OP), "main_k": MAIN_K,
        "min_s": MIN_S, "min_n": MIN_N, "dev_every": DEV_EVERY,
        "epochs": epochs, "batch": batch, "lr": DL_LR, "weight_decay": DL_WD,
        "embed": DL_EMB, "patience": DL_PATIENCE, "n_boot": n_boot,
        "feature_dims": feats.dims,
        "frozen_from_q4n": {
            "windows": {"W_P_S": list(W_P_S), "W_T_S": list(W_T_S), "W_Q_S": list(W_Q_S)},
            "fracs": [FRAC_QRS, FRAC_P, FRAC_T],
            "template": {"lo": TMPL_LO, "hi": TMPL_HI, "min": TMPL_MIN},
            "rhy_k": list(RHY_K), "fs": FS, "r_idx": R_IDX,
        },
        "gate_thresholds": {"min_gain": GATE_MIN_GAIN,
                            "min_seed_agreement": GATE_MIN_SEED_AGREE,
                            "lower_tail_max_drop": GATE_LOWER_TAIL_MAX_DROP},
    }
    manifest = {
        "data": provenance,
        "git_commit_sha": git_commit_sha(),
        "packages": package_versions(),
        "gpu": gpu_info(),
        "device": device,
        "determinism_notes": det_notes,
        "nondeterministic_ops": det_notes,
        "record_equals_patient": True,
        "n_record_total": int(len(cohort.records)),
        "n_record_scorable": int(len(rec_ok)),
        "scorable_records": [int(r) for r in rec_ok],
        "record_burden": {str(int(r)): burden[int(r)] for r in rec_ok},
        "fold_records": {str(f): sorted(int(r) for r in rec_ok if fold_map[int(r)] == f)
                         for f in range(N_OUTER_FOLDS)},
        "arm_alpha": {arm: arm_diag.get(arm) for arm in (ARM_C, ARM_D, ARM_E)},
        "morph_port_check": port_check_result,
    }
    result = {
        "experiment_id": EXPERIMENT_ID, "arm_id": ARM_ID,
        "timestamp_utc": timestamp,
        "smoke": bool(smoke),
        "primary_metric": "record_level_k_sweep_achievement_mean",
        "primary_comparison": "C_minus_A",
        "negative_control": "C_minus_D",
        "arms": metrics,
        "contrasts": contrasts,
        "gates": gates,
        "arm_E_diagnostic": e_diag,
        "note": ("Smoke runs use synthetic fixture data and carry no scientific "
                 "meaning." if smoke else
                 "Values are measured from this run only."),
    }

    predictions = {
        "sample_id": cohort.sample_id,
        "record_id": cohort.rid,
        "y_true": cohort.y.astype(np.int8),
        "fold": np.array([fold_map.get(int(r), -1) for r in cohort.rid], np.int16),
        "seeds": np.array([int(s) for s in seeds], np.int64),
        "scored_mask": np.isin(cohort.rid, np.array(rec_ok)),
    }
    arm_probs = {}
    for arm in ARMS:
        logits = arm_scores[arm]
        probs = 1.0 / (1.0 + np.exp(-np.clip(logits, -60, 60)))
        arm_probs[arm] = probs.astype("float32")
        predictions[f"logit_{arm}"] = logits.astype("float32")
    predictions["logit_comb_baseline_diagnostic"] = comb_scores.astype("float32")

    figures = {
        "arm_means": {a: metrics[a]["seed_averaged_ksw"]["mean"]
                      for a in list(ARMS) + ["comb_baseline_diagnostic"]},
        "contrasts": {k: v["record_bootstrap"] for k, v in contrasts.items()},
    }
    # Per-epoch training history, for learning curves in later reports. Recording it
    # changes neither the training computation nor the checkpoint selection — the
    # selection below is still argmin of dev BCE loss.
    training_history = []
    for arm, seed_runs in arm_diag.items():
        for entry in seed_runs or []:
            for fold_diag in entry["folds"]:
                training_history.append({
                    "arm": arm, "seed": int(entry["seed"]),
                    "fold": int(fold_diag["fold"]),
                    "best_epoch": int(fold_diag["best_epoch"]),
                    "epochs": fold_diag.get("history") or [],
                })

    write_bundle(out_dir, config, manifest, result, fold_map, arm_probs,
                 predictions, log.text(), figures,
                 training_history=training_history)
    log(f"bundle written to {out_dir}")
    return result


def main(argv: Optional[Sequence[str]] = None) -> int:
    ap = argparse.ArgumentParser(description=f"{EXPERIMENT_ID} / {ARM_ID} runner")
    ap.add_argument("--data", default=None,
                    help="path to svdb_data5.npz (required unless --smoke)")
    ap.add_argument("--out", required=True, help="run bundle output directory")
    ap.add_argument("--smoke", action="store_true",
                    help="CPU smoke run on synthetic fixture data")
    ap.add_argument("--epochs", type=int, default=None)
    ap.add_argument("--seeds", type=int, nargs="*", default=None)
    ap.add_argument("--boot", type=int, default=None)
    ap.add_argument("--device", default=None)
    ap.add_argument("--port-check", action="store_true",
                    help="re-score Arm A under Q4-N's LORO and compare against 0.8361")
    args = ap.parse_args(argv)

    log = RunLog()
    if args.smoke:
        log("SMOKE MODE — synthetic fixture data, no scientific meaning")
        cohort = synthetic_cohort()
        provenance = {"abs_path": "<synthetic>", "file_name": "<synthetic>",
                      "sha256": "<synthetic>", "synthetic": True,
                      "n_sample_labelled": cohort.n,
                      "n_record": int(len(cohort.records)),
                      "n_patient": int(len(cohort.records)),
                      "record_equals_patient": True,
                      "n_class": 2, "n_lead": cohort.n_lead,
                      "beat_width": cohort.width,
                      "beat_dtype": str(cohort.beat.dtype)}
        epochs = args.epochs if args.epochs is not None else 2
        seeds = args.seeds or list(TRAIN_SEEDS[:2])
        boot = args.boot if args.boot is not None else 200
    else:
        if not args.data:
            ap.error("--data is required unless --smoke is given")
        cohort, provenance = load_cohort(args.data)
        log(f"loaded {provenance['file_name']} sha256 {provenance['sha256'][:16]}… "
            f"· {provenance['n_sample_labelled']} beats · "
            f"{provenance['n_record']} records")
        epochs = args.epochs if args.epochs is not None else DL_EPOCH
        seeds = args.seeds or list(TRAIN_SEEDS)
        boot = args.boot if args.boot is not None else NB_BOOT

    result = run_experiment(cohort, provenance, args.out, seeds=seeds, epochs=epochs,
                            n_boot=boot, device=args.device, smoke=args.smoke,
                            port_check=args.port_check, log=log)
    print(json.dumps({"verdict": result["gates"]["verdict"],
                      "smoke": result["smoke"],
                      "out_dir": args.out}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
