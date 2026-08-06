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

        if not np.all(assign == 1):
            bad = int((assign != 1).sum())
            raise Q4OError(
                f"outer fold {f}: {bad} samples have an OOF assignment count != 1 "
                f"(min {assign.min()}, max {assign.max()}). This is exactly the "
                f"Q4-N overwrite failure mode."
            )
        assert_finite(off, f"cross-fitted offset for outer fold {f}")
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

    # Waveform normalisation is fit on the fit split only.
    wmu = float(X[fit_idx].mean())
    wsd = float(X[fit_idx].std()) + 1e-9

    def batch_tensors(idx):
        x = torch.tensor((X[idx] - wmu) / wsd, device=device)
        o = (torch.tensor(offset[idx].astype("float32"), device=device)
             if offset is not None else torch.zeros(len(idx), device=device))
        return x, o

    best_state = {k: v.detach().clone() for k, v in net.state_dict().items()}
    best_loss, bad, best_epoch = float("inf"), 0, -1
    rng = np.random.RandomState(seed)

    for ep in range(epochs):
        net.train()
        perm = rng.permutation(len(fit_idx))
        for b0 in range(0, len(fit_idx), batch):
            bi = fit_idx[perm[b0:b0 + batch]]
            x, o = batch_tensors(bi)
            yy = torch.tensor(y[bi].astype("float32"), device=device)
            opt.zero_grad()
            bce(net(x, o), yy).backward()
            opt.step()

        net.eval()
        with torch.no_grad():
            tot, cnt = 0.0, 0
            for b0 in range(0, len(dev_idx), 4096):
                bi = dev_idx[b0:b0 + 4096]
                x, o = batch_tensors(bi)
                yy = torch.tensor(y[bi].astype("float32"), device=device)
                tot += float(bce(net(x, o), yy)) * len(bi)
                cnt += len(bi)
            dev_loss = tot / max(1, cnt)
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
    return scores, alpha, best_epoch, float(best_loss)


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
        scores, alpha, best_ep, dev_loss = _train_one_fold(
            net, X, off, cohort.y, fit_idx, dev_idx, te_idx,
            seed + 1009 * f, device, epochs, batch, log)
        out[te_idx] = scores
        diags.append({"fold": f, "alpha": alpha, "best_epoch": best_ep,
                      "dev_loss": dev_loss, "n_fit": int(len(fit_idx)),
                      "n_dev": int(len(dev_idx)), "n_test": int(len(te_idx))})
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
                 figures: Optional[Dict[str, object]] = None) -> str:
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
        fig, ax = plt.subplots(figsize=(7, 3.2))
        names = list(contrasts)
        means = [contrasts[c]["mean"] for c in names]
        lo = [contrasts[c]["mean"] - contrasts[c]["ci_low"] for c in names]
        hi = [contrasts[c]["ci_high"] - contrasts[c]["mean"] for c in names]
        ax.errorbar(means, np.arange(len(names)), xerr=[lo, hi], fmt="o", capsize=4)
        ax.axvline(0.0, color="k", lw=0.8)
        ax.axvline(GATE_MIN_GAIN, color="tab:red", lw=0.8, ls="--", label="gate +0.015")
        ax.set_yticks(np.arange(len(names)))
        ax.set_yticklabels(names, fontsize=7)
        ax.set_xlabel("paired difference (k-sweep achievement)")
        ax.legend(fontsize=7)
        ax.grid(alpha=0.3, axis="x")
        fig.tight_layout()
        fig.savefig(os.path.join(fig_dir, "contrasts.png"), dpi=120)
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
    for arm in arms:
        probs = np.load(os.path.join(out_dir, "arms", arm, "probs.npy"))
        if probs.ndim != 2 or probs.shape[1] != n:
            raise Q4OError(f"arms/{arm}/probs.npy has shape {probs.shape}; "
                           f"expected (n_seed, {n})")


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
# Synthetic fixture (CPU smoke only — never a substitute for the real data)
# ─────────────────────────────────────────────────────────────────────────────
def synthetic_cohort(n_record: int = 12, n_beat: int = 140, width: int = 300,
                     n_lead: int = 2, seed: int = 7,
                     signal: float = 1.0) -> Cohort:
    """Grouped synthetic beats with a record-varying S burden.

    Enough structure for leakage/shape/order tests and a CPU smoke run. It is not a
    physiological simulator and no result from it means anything scientifically.
    """
    rng = np.random.RandomState(seed)
    beats, ys, pres, posts, rids = [], [], [], [], []
    t = np.arange(width)
    for r in range(n_record):
        burden = 0.10 + 0.30 * (r / max(1, n_record - 1))
        y = rng.rand(n_beat) < burden
        while int(y.sum()) < MIN_S or int((~y).sum()) < MIN_N:
            y = rng.rand(n_beat) < max(0.25, burden)
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
    write_bundle(out_dir, config, manifest, result, fold_map, arm_probs,
                 predictions, log.text(), figures)
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
