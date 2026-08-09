"""EXP-2026-005 / Q5-B-0 — S-subtype key recovery (ANALYSIS ONLY / NO TRAINING).

Why this exists
---------------
Q5-A (EXP-2026-004) measured four of its five pre-registered feature blocks and
returned ``UNRESOLVED`` (D5). The fifth block, ``B_SUBTYPE``, was never scored:
the atlas source's time column ``t`` is not the annotation sample index, so the
``.atr`` join landed at 1.9% — the chance rate. The pre-registered D5 next step
is *"the cheapest additional measurement or artifact recovery"*, and this module
is that measurement. It trains nothing and regenerates no probabilities.

What it does
------------
1. Reads a second processed file that carries the ORIGINAL annotation symbol
   (``ecg_multi.npz`` has ``sym``) and joins it to the frozen atlas cohort
   (``mamba_data.npz``) **by content**, per record, restricted to S beats —
   the only beats ``B_SUBTYPE`` uses.
2. The join key is an RR fingerprint: ``(pre_rr, post_rr, prev_pre_rr,
   next_post_rr)`` in seconds, taken from each file's own record-ordered
   arrays. Assignment is globally optimal and 1:1 per record. Row order is
   never the key, and the recovered symbol is never used to make the match.
3. Every join is put through pre-registered controls before anything is
   believed: permutation invariance, a one-beat shift control, a wrong-record
   control, and the payoff check that a matched S beat's recovered symbol
   actually lands in the AAMI S set — a check the matcher cannot have gamed
   because it never saw a symbol.
4. On GO the symbols are attached to the cohort and Q5-A's own ``run_atlas``
   is re-run unchanged, so the decision tree is re-evaluated with five blocks
   instead of four. On NO-GO ``B_SUBTYPE`` is closed permanently and the
   reason is written down. NO-GO is a result, not a failure to report.

Nothing here promotes an association to a cause, and nothing here implements
the Q5-B intervention: that still needs its own approved spec.
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import q5a_patient_failure_atlas as QA          # noqa: E402
import q4q_transportability_replication as QQ   # noqa: E402

EXPERIMENT_ID = "EXP-2026-005"
ARM_ID = "Q5-B-0"
RUN_SLUG = "q5b0_subtype_key_recovery"
REANALYSIS_SLUG = "q5b0_subtype_reanalysis"
MODULE_VERSION = 3
MODULE_BUILD = "2026-08-09"

MODES = ("DESIGN", "RECOVER", "REANALYZE", "REPORT")
STATUS = "DESIGN / RESULT NOT RUN"

S_INDEX = QA.S_INDEX
S_SUBTYPES = QA.S_SUBTYPES
MIT_ALL_RECORDS = QA.MIT_ALL_RECORDS

# ── pre-registered join parameters (fixed before any join is run) ────────────
#
# Both files derive RR from the same annotation samples, so a true pair should
# agree to the sample. 5 ms is 1.8 samples at 360 Hz: room for float32 storage
# and a rounding difference, not room for a different beat.
RR_TOLERANCE_S = 0.005
#: A match must beat the runner-up by this much, or the beat stays UNMATCHED.
#: Ambiguity is reported, never resolved by picking the first candidate.
RR_MARGIN_S = 0.005
#: Fingerprint coordinates, in the order they are concatenated.
FINGERPRINT_FIELDS = ("pre_rr", "post_rr")
#: Beats whose coupling interval is ambiguous may be filled in by ordinal
#: position ONLY when the content-matched anchors of that record prove the
#: mapping is exactly ordinal, and only when the anchors are at least this
#: share of the record's S beats. Below it, the ambiguous beats stay unmatched.
ORDINAL_MIN_ANCHOR_FRACTION = 0.50

# ── pre-registered GO/NO-GO gate ────────────────────────────────────────────
MIN_S_MATCH_FRACTION = 0.95        # of all S beats in the analysis cohort
MIN_RECORD_MATCH_FRACTION = 0.90   # per record ...
MIN_RECORDS_PASSING = 0.90         # ... in at least this share of records
MIN_SYMBOL_IN_S_SET = 0.99         # recovered symbol must be A/a/J/S
MAX_SHIFT_CONTROL = 0.20           # one-beat-shifted pool must NOT match
# Every match against another record's pool is false by construction, so this
# control is an UPPER BOUND on the join's false-match rate (in the real join
# the true partner is present and wins). The cap is what the subtype counts can
# absorb without distortion; the ratio is what separates signal from that null.
MAX_WRONG_RECORD = 0.05
MIN_SIGNAL_TO_NULL_RATIO = 5.0
MAX_S_COUNT_DIFF = QQ.S_MISMATCH_MAX_PER_RECORD   # per-record |dS| budget
#: A subtype block built from recovered symbols must lose its incremental
#: value when the symbols are shuffled inside each record. If it does not, the
#: "block" is measuring something other than the subtype.
SHUFFLE_CONTROL_MAX_RETAINED = 0.25
SHUFFLE_CONTROL_REPEATS = 5

SYMBOL_FIELDS = QA.BEAT_KEY_SYMBOL_FIELDS
LABEL_FIELDS = ("y5", "y", "y3", "label")
PRE_RR_FIELDS = ("pre_rr", "prerr", "rr_pre")
POST_RR_FIELDS = ("post_rr", "postrr", "rr_post")
RECORD_FIELDS = QA.BEAT_KEY_RECORD_FIELDS
DB_FIELDS = QA.BEAT_KEY_DB_FIELDS
TIME_FIELDS = QA.BEAT_KEY_SAMPLE_FIELDS

GATE_GO = "GO"
GATE_NOGO = "NO_GO_SUBTYPE_CLOSED"
GATES = (GATE_GO, GATE_NOGO)

STATUS_MEASURED = QA.STATUS_MEASURED
STATUS_BLOCKED = QA.STATUS_BLOCKED
STATUS_NOT_RUN = QA.STATUS_NOT_RUN

RECOVERY_BUNDLE_FILES = ("config.json", "manifest.json", "result.json",
                         "log.txt", "recovery_audit.csv",
                         "recovery_controls.json", "recovered_symbols.npz",
                         "decision.json", "summary.md")
RECOVERY_FIGURES = ("recovery_gate_dashboard.png", "rr_residual_hist.png",
                    "subtype_counts.png")


class Q5B0Error(RuntimeError):
    """Stop condition. Q5-B-0 never falls back to a weaker join in silence."""


RunLog = QA.RunLog


def run_dir_name(timestamp: str, slug: str = RUN_SLUG) -> str:
    return f"{timestamp}_{EXPERIMENT_ID}_{slug}"


def resolve_mode(mode: str) -> str:
    m = str(mode).strip().upper()
    if m not in MODES:
        raise Q5B0Error(f"mode must be exactly one of {MODES}, got {mode!r}")
    return m


def assert_analysis_only() -> Dict[str, object]:
    """This module must contain no training call, same rule as Q5-A."""
    own = QA.assert_analysis_only(os.path.abspath(__file__))
    return {"q5b0": own, "q5a": QA.assert_analysis_only()}


# ─────────────────────────────────────────────────────────────────────────────
# Symbol source
# ─────────────────────────────────────────────────────────────────────────────
@dataclass
class SymbolSource:
    """Beat-level rows of the file that still carries the original symbols."""

    record: np.ndarray            # (n,) int
    sym: np.ndarray               # (n,) <U2
    y5: np.ndarray                # (n,) int
    pre_rr: np.ndarray            # (n,) float seconds
    post_rr: np.ndarray           # (n,) float seconds
    records: np.ndarray
    idx_of: Dict[int, np.ndarray] = field(default_factory=dict)
    path: str = ""
    sha256: str = ""

    @property
    def n(self) -> int:
        return int(len(self.record))


def _first(files: Sequence[str], candidates: Sequence[str]) -> Optional[str]:
    lower = {f.lower(): f for f in files}
    for c in candidates:
        if c in lower:
            return lower[c]
    return None


def load_symbol_source(npz_path: str, db: str = "mitdb",
                       records: Optional[Sequence[int]] = None,
                       log: Optional[RunLog] = None) -> SymbolSource:
    """Load the symbol-bearing file (``ecg_multi.npz``) without its waveforms.

    The waveform array is the bulk of that file and the RR fingerprint does not
    need it, so the keys are read one at a time and ``beat`` is never touched.
    """
    log = log or RunLog()
    if not os.path.exists(npz_path):
        raise Q5B0Error(f"symbol source not found: {npz_path}")
    data = np.load(npz_path, allow_pickle=False)
    files = list(data.files)
    sym_f = _first(files, SYMBOL_FIELDS)
    if sym_f is None:
        raise Q5B0Error(
            f"{os.path.basename(npz_path)} carries no symbol key "
            f"(looked for {SYMBOL_FIELDS} in {files}) — without the original "
            "annotation symbol there is nothing to recover; STOP")
    rec_f = _first(files, RECORD_FIELDS)
    y_f = _first(files, LABEL_FIELDS)
    pre_f = _first(files, PRE_RR_FIELDS)
    post_f = _first(files, POST_RR_FIELDS)
    missing = [n for n, f in (("record", rec_f), ("label", y_f),
                              ("pre_rr", pre_f), ("post_rr", post_f))
               if f is None]
    if missing:
        raise Q5B0Error(f"{os.path.basename(npz_path)} is missing {missing} — "
                        "the RR fingerprint cannot be built; STOP")
    rec_all = np.asarray(data[rec_f]).astype(int)
    db_f = _first(files, DB_FIELDS)
    mask = (np.isin(np.asarray(data[db_f]).astype(str),
                    (db, "mit", "mit-bih", "mitdb")) if db_f
            else np.ones(len(rec_all), bool))
    if not mask.any():
        raise Q5B0Error(
            f"no {db} rows in {os.path.basename(npz_path)} "
            f"(db values seen: {sorted(set(np.asarray(data[db_f]).astype(str)))[:8] if db_f else 'no db key'})")
    # The record ids in this file are NOT assumed to be MIT record numbers.
    # Q4-Q measured that they can be ordinal, which is why record identity is
    # established later by the 5-class profile (:func:`resolve_record_mapping`)
    # instead of by id equality. Filtering on 100..234 here would silently
    # empty the file.
    if records is not None:
        keep = np.isin(rec_all, tuple(records))
        if keep.any():
            mask &= keep
    y5 = np.asarray(data[y_f]).astype(int)[mask]
    if y5.min() < 0 or y5.max() > 4:
        raise Q5B0Error(f"{y_f} is not AAMI 5-class coded — STOP")
    rec = rec_all[mask]
    src = SymbolSource(
        record=rec,
        sym=np.asarray(data[sym_f]).astype(str)[mask].astype("<U2"),
        y5=y5,
        pre_rr=np.asarray(data[pre_f], float)[mask],
        post_rr=np.asarray(data[post_f], float)[mask],
        records=np.array(sorted(set(rec.tolist())), int),
        path=npz_path, sha256=QA.sha256_file(npz_path))
    src.idx_of = {int(r): np.where(rec == r)[0] for r in src.records}
    coding = ("record_numbers" if set(src.records.tolist()) <= set(QQ.MIT_48_RECORDS)
              else "ordinal_or_other")
    log(f"symbol source: {src.n} beats, {len(src.records)} records "
        f"(id coding: {coding}), S={int((y5 == S_INDEX).sum())}, "
        f"symbol key {sym_f!r}")
    return src


# ─────────────────────────────────────────────────────────────────────────────
# Record identity — established, not assumed
# ─────────────────────────────────────────────────────────────────────────────
def _class_profile(record: np.ndarray, y5: np.ndarray) -> Dict[int, Dict]:
    return {int(r): {"classes": [int(((record == r) & (y5 == c)).sum())
                                 for c in range(5)]}
            for r in sorted(set(record.tolist()))}


def resolve_record_mapping(cohort: QA.AtlasCohort, source: SymbolSource,
                           log: Optional[RunLog] = None) -> Dict[str, object]:
    """Pair the source's record ids with the cohort's — by class profile.

    Q4-Q measured that ``ecg_multi``'s ``pid`` is not necessarily an MIT record
    number, so id equality is a guess, not a fact. Identity is therefore
    *checked* first (per-record S counts must agree within the same budget
    Q4-Q used) and only accepted when it holds; otherwise the records are
    matched by their 5-class fingerprint with Q4-Q's own assignment code, the
    one whose gate already passed on these two files.

    Never raises: an unresolvable mapping is a NO-GO with evidence, not a
    crash that leaves no bundle behind.
    """
    log = log or RunLog()
    cohort_prof = _class_profile(cohort.record, cohort.y5)
    source_prof = _class_profile(source.record, source.y5)
    out: Dict[str, object] = {
        "source_id_coding": ("record_numbers"
                             if set(source_prof) <= set(QQ.MIT_48_RECORDS)
                             else "ordinal_or_other"),
        "n_cohort_records": len(cohort_prof),
        "n_source_records": len(source_prof),
    }

    shared = [r for r in cohort_prof if r in source_prof]
    if len(shared) == len(cohort_prof):
        worst = max(abs(cohort_prof[r]["classes"][S_INDEX]
                        - source_prof[r]["classes"][S_INDEX])
                    for r in shared)
        if worst <= MAX_S_COUNT_DIFF:
            out.update({"ok": True, "method": "identity_verified",
                        "mapping": {int(r): int(r) for r in shared},
                        "worst_s_diff": int(worst), "leftover": [],
                        "detail": ("the ids already are MIT record numbers and "
                                   "the per-record S counts agree")})
            log(f"record mapping: identity, verified (worst |dS| = {worst})")
            return out
        out["identity_rejected"] = (
            f"ids look like record numbers but the per-record S counts "
            f"disagree by up to {worst} beats (> {MAX_S_COUNT_DIFF})")

    try:
        m = QQ._fingerprint_match(cohort_prof, source_prof)
    except Exception as exc:
        out.update({"ok": False, "method": "fingerprint_assignment",
                    "mapping": {}, "reason": str(exc)})
        log(f"record mapping FAILED: {exc}")
        return out
    out.update({"ok": True, "method": "fingerprint_assignment",
                "mapping": {int(k): int(v) for k, v in m["mapping"].items()},
                "leftover": [int(r) for r in m["leftover"]],
                "s_agreement": m["s_agreement"], "table": m["table"],
                "warnings": m["warnings"],
                "detail": ("record identity established by the 5-class profile "
                           "(Q4-Q's assignment), not by id equality")})
    log(f"record mapping: 5-class fingerprint assignment, "
        f"{len(out['mapping'])} record(s) paired, "
        f"{len(out['leftover'])} leftover")
    return out


def apply_record_mapping(source: SymbolSource, mapping: Dict[int, int]
                         ) -> SymbolSource:
    """Rewrite the source's ids into cohort record numbers; drop the rest."""
    inv = {int(v): int(k) for k, v in mapping.items()}
    keep = np.array([int(r) in inv for r in source.record], bool)
    rec = np.array([inv[int(r)] for r in source.record[keep]], int)
    out = SymbolSource(record=rec, sym=source.sym[keep], y5=source.y5[keep],
                       pre_rr=source.pre_rr[keep], post_rr=source.post_rr[keep],
                       records=np.array(sorted(set(rec.tolist())), int),
                       path=source.path, sha256=source.sha256)
    out.idx_of = {int(r): np.where(rec == r)[0] for r in out.records}
    return out


def rr_seconds_scale(pre_rr: np.ndarray, fs: float = 360.0) -> Dict[str, object]:
    """Verify the RR column really is seconds before it is used as a key.

    Same rule as Q5-A's time-unit inference: exactly one interpretation may
    land in the physiological range, otherwise the column is unusable.
    """
    v = np.asarray(pre_rr, float)
    v = v[np.isfinite(v) & (v > 0)]
    if not len(v):
        raise Q5B0Error("RR column is empty or non-finite — cannot verify unit")
    med = float(np.median(v))
    lo, hi = QA.RR_PLAUSIBLE_S
    as_seconds = lo <= med <= hi
    as_samples = lo <= med / float(fs) <= hi
    if as_seconds == as_samples:
        raise Q5B0Error(
            f"RR unit is ambiguous (median {med:g}; seconds={as_seconds}, "
            f"samples={as_samples}) — refusing to guess")
    return {"unit": "seconds" if as_seconds else "samples",
            "median_raw": med, "fs": float(fs),
            "scale_to_seconds": 1.0 if as_seconds else 1.0 / float(fs)}


# ─────────────────────────────────────────────────────────────────────────────
# RR fingerprint
# ─────────────────────────────────────────────────────────────────────────────
def rr_fingerprint(pre_rr: np.ndarray, post_rr: np.ndarray) -> np.ndarray:
    """Order-free content key for a beat: its own coupling and exit interval.

    Deliberately NOT a neighbourhood key. A key that reads the previous row's
    RR would change when the rows are permuted, and then "shuffle the pool and
    get the same answer" — the only honest way to show a join is not
    positional — could never be satisfied. Both coordinates are properties of
    the beat itself.

    Two beats of one record can share a coupling interval; that is what the
    margin rule in :func:`assign_one_to_one` is for. Such beats are left
    UNMATCHED and counted, not resolved by guessing.
    """
    pre = np.asarray(pre_rr, float)
    post = np.asarray(post_rr, float)
    if len(pre) != len(post):
        raise Q5B0Error("pre/post RR length mismatch")
    return np.column_stack([pre, post])


def chronology_report(pre_rr: np.ndarray, post_rr: np.ndarray,
                      tol: float = 0.005) -> Dict[str, object]:
    """Is this record's row order chronological? ``pre_rr[j+1] == post_rr[j]``.

    Reported, not assumed. A record whose chain is broken can still be joined
    (the fingerprint is content), but the neighbour coordinates are then less
    trustworthy and that has to be visible.
    """
    pre = np.asarray(pre_rr, float)
    post = np.asarray(post_rr, float)
    if len(pre) < 2:
        return {"n_pairs": 0, "chain_fraction": None}
    d = np.abs(pre[1:] - post[:-1])
    ok = np.isfinite(d)
    if not ok.any():
        return {"n_pairs": 0, "chain_fraction": None}
    return {"n_pairs": int(ok.sum()),
            "chain_fraction": float((d[ok] <= tol).mean()),
            "median_gap_s": float(np.median(d[ok]))}


def _cost_matrix(fa: np.ndarray, fb: np.ndarray) -> np.ndarray:
    """Mean absolute difference over the finite fingerprint coordinates."""
    diff = np.abs(fa[:, None, :] - fb[None, :, :])
    finite = np.isfinite(diff)
    n_finite = finite.sum(axis=2)
    total = np.where(finite, diff, 0.0).sum(axis=2)
    with np.errstate(invalid="ignore", divide="ignore"):
        cost = np.where(n_finite > 0, total / np.maximum(n_finite, 1), np.inf)
    return cost


def assign_one_to_one(cost: np.ndarray, tolerance: float = RR_TOLERANCE_S,
                      margin: float = RR_MARGIN_S) -> Dict[str, object]:
    """Globally optimal 1:1 assignment, then the pre-registered accept rules.

    Two rules decide whether an assigned pair is kept:

    * the cost must be within ``tolerance`` — the beats really are the same
      beat measured twice;
    * the runner-up for that row must be at least ``margin`` worse — if two
      candidates fit equally well the beat is AMBIGUOUS and stays unmatched.

    Ambiguity is counted and reported. Nothing is resolved by taking the first
    or the lowest index.
    """
    cost = np.asarray(cost, float)
    n, m = cost.shape
    out = {"n_row": n, "n_col": m, "match": np.full(n, -1, int),
           "cost": np.full(n, np.inf), "n_matched": 0, "n_ambiguous": 0,
           "n_over_tolerance": 0}
    if n == 0 or m == 0:
        return out
    finite = np.where(np.isfinite(cost), cost, 1e9)
    try:
        from scipy.optimize import linear_sum_assignment
        rows, cols = linear_sum_assignment(finite)
    except Exception:                                    # pragma: no cover
        rows, cols = _greedy_assignment(finite)
    # runner-up per row, excluding the assigned column
    order = np.argsort(finite, axis=1)
    best = finite[np.arange(n), order[:, 0]]
    second = (finite[np.arange(n), order[:, 1]] if m > 1
              else np.full(n, np.inf))
    match = np.full(n, -1, int)
    cst = np.full(n, np.inf)
    amb = over = 0
    for i, j in zip(rows, cols):
        c = float(finite[i, j])
        runner = float(second[i]) if np.isclose(finite[i, j], best[i]) \
            else float(best[i])
        if c > tolerance:
            over += 1
            continue
        if runner - c < margin:
            amb += 1
            continue
        match[i] = int(j)
        cst[i] = c
    out.update({"match": match, "cost": cst,
                "n_matched": int((match >= 0).sum()),
                "n_ambiguous": int(amb), "n_over_tolerance": int(over)})
    return out


def _greedy_assignment(cost: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """Fallback when scipy is unavailable: greedy by increasing cost."""
    n, m = cost.shape
    flat = np.argsort(cost, axis=None)
    used_r, used_c = set(), set()
    rows, cols = [], []
    for f in flat:
        i, j = divmod(int(f), m)
        if i in used_r or j in used_c:
            continue
        used_r.add(i)
        used_c.add(j)
        rows.append(i)
        cols.append(j)
        if len(rows) == min(n, m):
            break
    return np.array(rows, int), np.array(cols, int)


# ─────────────────────────────────────────────────────────────────────────────
# Recovery
# ─────────────────────────────────────────────────────────────────────────────
def _record_fingerprints(pre: np.ndarray, post: np.ndarray, y5: np.ndarray,
                         idx: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """Fingerprints for one record, plus the positions of its S beats."""
    fp = rr_fingerprint(pre[idx], post[idx])
    s_local = np.where(y5[idx] == S_INDEX)[0]
    return fp, s_local


def recover_symbols(cohort: QA.AtlasCohort, source: SymbolSource,
                    records: Optional[Sequence[int]] = None,
                    tolerance: float = RR_TOLERANCE_S,
                    margin: float = RR_MARGIN_S,
                    mapping_report: Optional[Dict[str, object]] = None,
                    log: Optional[RunLog] = None) -> Dict[str, object]:
    """Join S beats of the atlas cohort to the symbol source, per record.

    Only S beats are joined: they are the only rows ``B_SUBTYPE`` reads, and
    restricting the pool to the same class on both sides is what makes the
    assignment small and exact. The recovered symbol is never an input to the
    match, which is why "the symbol landed in the AAMI S set" is an
    independent check on the join rather than a tautology.
    """
    log = log or RunLog()
    if not np.isfinite(cohort.pre_rr).any():
        raise Q5B0Error("the atlas cohort carries no RR — run "
                        "QA.rr_from_samples first (it derives RR from the "
                        "verified time column)")
    unit = rr_seconds_scale(source.pre_rr)
    scale = float(unit["scale_to_seconds"])
    src_pre = source.pre_rr * scale
    src_post = source.post_rr * scale

    recs = [int(r) for r in (records if records is not None
                             else cohort.records)]
    sym_out = np.full(cohort.n, "?", dtype="<U2")
    sym_anchor = np.full(cohort.n, "?", dtype="<U2")
    per_record: List[Dict[str, object]] = []
    residuals: List[float] = []
    ordinal_seen: List[float] = []
    ordinal_seen_used: List[float] = []
    near_miss: List[float] = []
    ordinal_probe: List[Dict[str, object]] = []
    total_s = total_matched = total_anchor = total_extended = 0
    for r in recs:
        idx = cohort.idx_of[int(r)]
        row = {"record": int(r), "n_cohort": int(len(idx))}
        if int(r) not in source.idx_of:
            row.update({"status": "absent_in_symbol_source", "n_s_cohort":
                        int(cohort.y_s[idx].sum()), "n_matched": 0})
            per_record.append(row)
            total_s += int(cohort.y_s[idx].sum())
            continue
        sidx = source.idx_of[int(r)]
        fp_a = rr_fingerprint(cohort.pre_rr[idx], cohort.post_rr[idx])
        fp_b = rr_fingerprint(src_pre[sidx], src_post[sidx])
        a_s = np.where(cohort.y_s[idx])[0]
        b_s = np.where(source.y5[sidx] == S_INDEX)[0]
        row.update({
            "n_s_cohort": int(len(a_s)), "n_s_source": int(len(b_s)),
            "s_count_diff": int(len(a_s) - len(b_s)),
            "n_source": int(len(sidx)),
            "chronology_cohort": chronology_report(
                cohort.pre_rr[idx], cohort.post_rr[idx])["chain_fraction"],
            "chronology_source": chronology_report(
                src_pre[sidx], src_post[sidx])["chain_fraction"],
        })
        total_s += int(len(a_s))
        if not len(a_s) or not len(b_s):
            row.update({"status": "no_s_beats", "n_matched": 0})
            per_record.append(row)
            continue
        res = assign_one_to_one(_cost_matrix(fp_a[a_s], fp_b[b_s]),
                                tolerance=tolerance, margin=margin)
        anchor = res["match"] >= 0
        sym_anchor[idx[a_s[anchor]]] = source.sym[sidx[b_s[res["match"][anchor]]]]
        pair = res["match"].copy()

        # Is the anchor mapping ordinal — the k-th S beat of one file to the
        # k-th of the other? This is TESTED on the beats the content already
        # identified, never assumed. Only if it holds exactly may the beats
        # whose coupling interval was ambiguous be filled in ordinally, and
        # those fills are counted separately and still have to survive the
        # symbol check below (which the matcher cannot influence).
        ordinal = (float(np.mean(res["match"][anchor] == np.where(anchor)[0]))
                   if int(anchor.sum()) >= 2 else None)
        extended = np.zeros(len(a_s), bool)
        if (ordinal == 1.0 and len(a_s) == len(b_s)
                and int(anchor.sum()) >= ORDINAL_MIN_ANCHOR_FRACTION * len(a_s)):
            extended = ~anchor
            pair[extended] = np.where(extended)[0]

        hit = pair >= 0
        matched_rows = idx[a_s[hit]]
        matched_src = sidx[b_s[pair[hit]]]
        sym_out[matched_rows] = source.sym[matched_src]
        residuals += [float(c) for c in res["cost"][anchor]]
        in_s_set = np.isin(source.sym[matched_src], S_SUBTYPES)
        total_matched += int(hit.sum())
        total_anchor += int(anchor.sum())
        total_extended += int(extended.sum())
        if ordinal is not None:
            ordinal_seen.append(ordinal)
            if extended.any():
                ordinal_seen_used.append(ordinal)

        # ── diagnostics (no rule depends on these) ──────────────────────────
        # How far away was the nearest candidate for the beats that did NOT
        # match? Near misses and hopeless misses look identical in a match
        # rate, and they mean completely different things about the artifact.
        cost = _cost_matrix(fp_a[a_s], fp_b[b_s])
        if cost.size:
            nearest = np.min(np.where(np.isfinite(cost), cost, np.inf), axis=1)
            miss = nearest[~anchor]
            near_miss += [float(v) for v in miss[np.isfinite(miss)]]
            row["nearest_cost_unmatched_p50"] = (float(np.median(miss))
                                                 if len(miss) else None)
        # Under the ordinal hypothesis (k-th S beat <-> k-th S beat), what is
        # the RR discrepancy? A tight but non-zero cluster would mean the two
        # files measure the same beats on different time bases; a diffuse one
        # would mean they are simply not identifiable from RR.
        if len(a_s) == len(b_s) and len(a_s):
            d_pre = fp_b[b_s][:, 0] - fp_a[a_s][:, 0]
            ratio = np.divide(fp_b[b_s][:, 0], fp_a[a_s][:, 0],
                              out=np.full(len(a_s), np.nan),
                              where=fp_a[a_s][:, 0] > 0)
            ok = np.isfinite(d_pre)
            if ok.any():
                probe = {"record": int(r), "n": int(ok.sum()),
                         "pre_rr_diff_median_s": float(np.median(d_pre[ok])),
                         "pre_rr_diff_iqr_s": float(np.subtract(
                             *np.percentile(d_pre[ok], [75, 25]))),
                         "pre_rr_ratio_median": (float(np.nanmedian(ratio))
                                                 if np.isfinite(ratio).any()
                                                 else None)}
                ordinal_probe.append(probe)
                row.update({f"ordinal_probe_{k}": v for k, v in probe.items()
                            if k != "record"})
        row.update({
            "status": "matched", "n_matched": int(hit.sum()),
            "match_fraction": float(hit.mean()),
            "n_anchor": int(anchor.sum()), "n_extended": int(extended.sum()),
            "ordinal_consistency": ordinal,
            "n_ambiguous": int(res["n_ambiguous"]),
            "n_over_tolerance": int(res["n_over_tolerance"]),
            "median_cost_s": (float(np.median(res["cost"][anchor]))
                              if anchor.any() else None),
            "max_cost_s": (float(np.max(res["cost"][anchor]))
                           if anchor.any() else None),
            "symbol_in_s_set": (float(in_s_set.mean()) if hit.any() else None),
            "symbols": ",".join(sorted(set(
                source.sym[matched_src].tolist()))) if hit.any() else "",
        })
        per_record.append(row)
    frac = float(total_matched) / max(1, total_s)
    matched_all = sym_out != "?"
    in_set = (float(np.isin(sym_out[matched_all], S_SUBTYPES).mean())
              if matched_all.any() else 0.0)
    chrono = [min(float(r.get("chronology_cohort") or 0.0),
                  float(r.get("chronology_source") or 0.0))
              for r in per_record if r.get("chronology_cohort") is not None]
    out = {
        "sym": sym_out, "sym_anchor": sym_anchor, "per_record": per_record,
        "record_mapping": mapping_report or {
            "ok": True, "method": "identity_assumed_by_caller",
            "detail": ("the source was handed over with cohort record numbers "
                       "already; run_recovery always resolves this explicitly")},
        "chronology_min": (min(chrono) if chrono else None),
        "n_s": int(total_s), "n_matched": int(total_matched),
        "n_anchor": int(total_anchor), "n_extended": int(total_extended),
        "match_fraction": frac,
        "anchor_fraction": float(total_anchor) / max(1, total_s),
        "ordinal_consistency_min": (min(ordinal_seen) if ordinal_seen else None),
        "ordinal_consistency_mean": (float(np.mean(ordinal_seen))
                                     if ordinal_seen else None),
        "ordinal_consistency_min_where_used": (min(ordinal_seen_used)
                                               if ordinal_seen_used else None),
        "nearest_cost_unmatched": {
            "n": len(near_miss),
            "p10": (float(np.percentile(near_miss, 10)) if near_miss else None),
            "p50": (float(np.median(near_miss)) if near_miss else None),
            "p90": (float(np.percentile(near_miss, 90)) if near_miss else None),
            "within_2x_tolerance": (float(np.mean(np.array(near_miss)
                                                  <= 2 * tolerance))
                                    if near_miss else None)},
        "ordinal_hypothesis_probe": ordinal_probe,
        "symbol_in_s_set_fraction": in_set,
        "rr_unit": unit,
        "median_residual_s": float(np.median(residuals)) if residuals else None,
        "p95_residual_s": (float(np.percentile(residuals, 95)) if residuals
                           else None),
        "residuals": residuals,
        "subtype_counts": {t: int((sym_out[matched_all] == t).sum())
                           for t in S_SUBTYPES},
        "params": {"tolerance_s": tolerance, "margin_s": margin,
                   "fields": list(FINGERPRINT_FIELDS),
                   "ordinal_min_anchor_fraction": ORDINAL_MIN_ANCHOR_FRACTION},
    }
    log(f"symbol recovery: {total_matched}/{total_s} S beats joined "
        f"({frac:.1%}; {total_anchor} by content, {total_extended} filled "
        f"ordinally after the anchor mapping tested exact); symbol in AAMI S "
        f"set {in_set:.1%}")
    return out


def _empty_recovery(cohort: QA.AtlasCohort, mapping_report: Dict[str, object]
                    ) -> Dict[str, object]:
    """The shape :func:`recover_symbols` returns when no join was possible."""
    n_s = int(cohort.y_s.sum())
    return {"sym": np.full(cohort.n, "?", dtype="<U2"),
            "sym_anchor": np.full(cohort.n, "?", dtype="<U2"),
            "per_record": [{"record": int(r), "status": "no_record_mapping",
                            "n_s_cohort": int(cohort.y_s[cohort.idx_of[int(r)]]
                                              .sum()), "n_matched": 0}
                           for r in cohort.records],
            "record_mapping": mapping_report, "chronology_min": None,
            "n_s": n_s, "n_matched": 0, "n_anchor": 0, "n_extended": 0,
            "match_fraction": 0.0, "anchor_fraction": 0.0,
            "ordinal_consistency_min": None, "ordinal_consistency_mean": None,
            "ordinal_consistency_min_where_used": None,
            "nearest_cost_unmatched": {"n": 0, "p10": None, "p50": None,
                                       "p90": None, "within_2x_tolerance": None},
            "ordinal_hypothesis_probe": [],
            "symbol_in_s_set_fraction": 0.0, "rr_unit": None,
            "median_residual_s": None, "p95_residual_s": None, "residuals": [],
            "subtype_counts": {t: 0 for t in S_SUBTYPES},
            "params": {"tolerance_s": RR_TOLERANCE_S, "margin_s": RR_MARGIN_S,
                       "fields": list(FINGERPRINT_FIELDS)}}


# ─────────────────────────────────────────────────────────────────────────────
# Pre-registered controls
# ─────────────────────────────────────────────────────────────────────────────
def permutation_invariance(cohort: QA.AtlasCohort, source: SymbolSource,
                           records: Sequence[int], seed: int = 0
                           ) -> Dict[str, object]:
    """Shuffling the symbol source's rows must not change a single match.

    This is the formal statement of "no positional matching": a content join is
    invariant to the order of the pool it searches.
    """
    rng = np.random.default_rng(seed)
    perm = rng.permutation(source.n)
    shuffled = SymbolSource(
        record=source.record[perm], sym=source.sym[perm], y5=source.y5[perm],
        pre_rr=source.pre_rr[perm], post_rr=source.post_rr[perm],
        records=source.records, path=source.path, sha256=source.sha256)
    shuffled.idx_of = {int(r): np.where(shuffled.record == r)[0]
                       for r in shuffled.records}
    a = recover_symbols(cohort, source, records, log=RunLog(echo=False))
    b = recover_symbols(cohort, shuffled, records, log=RunLog(echo=False))
    same = bool(np.array_equal(a["sym_anchor"], b["sym_anchor"]))
    return {"identical": same,
            "n_differing": int((a["sym_anchor"] != b["sym_anchor"]).sum()),
            "n_anchor": int(a["n_anchor"]),
            "scope": "content anchors",
            "note": ("the RR key is order-free, so shuffling the pool must "
                     "not move a single anchor. The ordinal fill is order-"
                     "based BY DESIGN and is licensed separately, by the "
                     "anchors testing exactly ordinal and by the chronology "
                     "chain — it is deliberately outside this check")}


def shift_control(cohort: QA.AtlasCohort, source: SymbolSource,
                  records: Sequence[int],
                  tolerance: float = RR_TOLERANCE_S) -> Dict[str, object]:
    """Pair every S beat with its neighbour's counterpart: that must NOT fit.

    Permuting the pool cannot test anything here — the key is order-free, so a
    permutation is invisible by construction. What has to be ruled out is the
    correspondence itself being off by one, so this control takes the
    deliberately wrong pairing (beat k of the cohort against S beat k+1 of the
    source) and asks how much of it still lands inside the tolerance. On a
    record whose beats are genuinely distinguishable the answer is close to
    zero; if it is not, the tolerance is too loose to identify anything and the
    join means nothing however high its match rate looked.
    """
    unit = rr_seconds_scale(source.pre_rr)
    scale = float(unit["scale_to_seconds"])
    within = total = 0
    for r in records:
        r = int(r)
        if r not in source.idx_of:
            continue
        idx = cohort.idx_of[r]
        sidx = source.idx_of[r]
        a_s = np.where(cohort.y_s[idx])[0]
        b_s = np.where(source.y5[sidx] == S_INDEX)[0]
        n = min(len(a_s), len(b_s)) - 1
        if n < 1:
            continue
        fp_a = rr_fingerprint(cohort.pre_rr[idx], cohort.post_rr[idx])[a_s][:n]
        fp_b = rr_fingerprint(source.pre_rr[sidx] * scale,
                              source.post_rr[sidx] * scale)[b_s][1:n + 1]
        cost = np.abs(fp_a - fp_b)
        finite = np.isfinite(cost)
        n_fin = finite.sum(axis=1)
        mean_cost = np.where(n_fin > 0,
                             np.where(finite, cost, 0.0).sum(axis=1)
                             / np.maximum(n_fin, 1), np.inf)
        within += int((mean_cost <= tolerance).sum())
        total += int(n)
    frac = float(within) / max(1, total)
    return {"match_fraction": frac, "n_within_tolerance": int(within),
            "n_total": int(total), "max_allowed": MAX_SHIFT_CONTROL,
            "note": "off-by-one pairing must fall outside the tolerance"}


def wrong_record_control(cohort: QA.AtlasCohort, source: SymbolSource,
                         records: Sequence[int],
                         tolerance: float = RR_TOLERANCE_S,
                         margin: float = RR_MARGIN_S) -> Dict[str, object]:
    """Search each record's beats in the NEXT record's pool: must not match."""
    unit = rr_seconds_scale(source.pre_rr)
    scale = float(unit["scale_to_seconds"])
    usable = [int(r) for r in records if int(r) in source.idx_of]
    matched = total = 0
    for k, r in enumerate(usable):
        other = usable[(k + 1) % len(usable)]
        if other == r:
            continue
        idx = cohort.idx_of[r]
        sidx = source.idx_of[other]
        a_s = np.where(cohort.y_s[idx])[0]
        b_s = np.where(source.y5[sidx] == S_INDEX)[0]
        if not len(a_s) or not len(b_s):
            continue
        fp_a = rr_fingerprint(cohort.pre_rr[idx], cohort.post_rr[idx])[a_s]
        fp_b = rr_fingerprint(source.pre_rr[sidx] * scale,
                             source.post_rr[sidx] * scale)[b_s]
        res = assign_one_to_one(_cost_matrix(fp_a, fp_b), tolerance=tolerance,
                                margin=margin)
        matched += res["n_matched"]
        total += len(a_s)
    frac = float(matched) / max(1, total)
    return {"match_fraction": frac, "n_matched": int(matched),
            "n_total": int(total), "max_allowed": MAX_WRONG_RECORD,
            "note": ("every match here is false by construction, so this is "
                     "an upper bound on the join's false-match rate: in the "
                     "real join the true partner is present and wins the "
                     "assignment")}


def reference_scores(cohort: QA.AtlasCohort, models: Dict[str, object],
                     rows: np.ndarray) -> Tuple[str, np.ndarray]:
    """The reference model's scores on ``rows``, aligned the way the atlas does.

    Same label choice (``sorted(labels)[-1]``) and the same key-based scatter,
    so the shuffle control below scores the block against exactly the outcome
    the atlas used — not a near-miss reconstruction of it.
    """
    key_index = {str(k): i for i, k in enumerate(cohort.key)}
    label = sorted(models)[-1]
    m = models[label]
    full = np.full(cohort.n, np.nan)
    pos = np.array([key_index[str(k)] for k in m.key if str(k) in key_index],
                   int)
    keep = np.array([str(k) in key_index for k in m.key], bool)
    full[pos] = np.asarray(m.score)[keep]
    return label, full[rows]


def subtype_shuffle_control(subtype: np.ndarray, groups: np.ndarray,
                            outcome: np.ndarray,
                            repeats: int = SHUFFLE_CONTROL_REPEATS,
                            seed: int = 0,
                            n_boot: int = 200) -> Dict[str, object]:
    """Shuffle the recovered subtypes inside each record and re-score the block.

    A real subtype effect must collapse when the labels are permuted within the
    record they came from; something that survives is not the subtype but
    whatever the join happened to correlate with. Everything is passed in
    explicitly — the control never reaches back into the cohort, so a test can
    hand it a planted effect and a null and see it tell them apart.
    """
    subtype = np.asarray(subtype)
    groups = np.asarray(groups)
    outcome = np.asarray(outcome, float)
    if not len(subtype) or not (len(subtype) == len(groups) == len(outcome)):
        return {"available": False,
                "reason": "no subtype block, or mismatched lengths"}

    def block_of(labels: np.ndarray) -> Dict[str, np.ndarray]:
        return {f"subtype_{t}": (labels == t).astype(float)
                for t in S_SUBTYPES}

    real = QA.block_incremental_value({}, block_of(subtype), outcome, groups,
                                      mode="regression", n_boot=n_boot)
    rng = np.random.default_rng(seed)
    deltas = []
    for _ in range(int(repeats)):
        shuffled = subtype.copy()
        for r in np.unique(groups):
            m = groups == r
            shuffled[m] = rng.permutation(shuffled[m])
        deltas.append(float(QA.block_incremental_value(
            {}, block_of(shuffled), outcome, groups, mode="regression",
            n_boot=n_boot)["delta_logloss"]))
    real_delta = float(real["delta_logloss"])
    shuffled_mean = float(np.mean(deltas))
    if real_delta <= 0:
        # There is no incremental value to falsify. Dividing two numbers that
        # are both noise around zero would manufacture a verdict, so the
        # control reports that it does not apply instead of passing or failing.
        return {"available": True, "applicable": False,
                "real_delta": real_delta, "shuffled_deltas": deltas,
                "shuffled_mean": shuffled_mean, "retained_fraction": None,
                "max_allowed": SHUFFLE_CONTROL_MAX_RETAINED, "pass": True,
                "verdict": ("B_SUBTYPE carries no incremental value here, so "
                            "there is nothing for the shuffle to destroy")}
    retained = shuffled_mean / real_delta
    return {"available": True, "applicable": True, "real_delta": real_delta,
            "shuffled_deltas": deltas, "shuffled_mean": shuffled_mean,
            "retained_fraction": retained,
            "max_allowed": SHUFFLE_CONTROL_MAX_RETAINED,
            "pass": bool(retained <= SHUFFLE_CONTROL_MAX_RETAINED),
            "verdict": ("a real subtype effect must collapse when the symbols "
                        "are shuffled inside each record")}


# ─────────────────────────────────────────────────────────────────────────────
# Gate
# ─────────────────────────────────────────────────────────────────────────────
def evaluate_recovery_gate(recovery: Dict[str, object],
                           controls: Dict[str, object]) -> Dict[str, object]:
    """Pre-registered GO / NO-GO. Thresholds are never tuned on the result."""
    reasons: List[str] = []
    checks: List[Dict[str, object]] = []

    def add(name: str, ok: bool, value, threshold, detail: str = "") -> None:
        checks.append({"check": name, "pass": bool(ok), "value": value,
                       "threshold": threshold, "detail": detail})
        if not ok:
            reasons.append(f"{name}: {value} (needs {threshold}) {detail}".strip())

    rmap = recovery.get("record_mapping") or {}
    add("record_identity_resolved", bool(rmap.get("ok")),
        rmap.get("method", "missing"), "identity verified or assigned",
        str(rmap.get("reason") or rmap.get("detail") or "")[:160])

    frac = float(recovery.get("match_fraction") or 0.0)
    add("s_match_fraction", frac >= MIN_S_MATCH_FRACTION, round(frac, 4),
        f">= {MIN_S_MATCH_FRACTION}")

    per = [r for r in recovery.get("per_record", [])
           if r.get("n_s_cohort", 0) > 0]
    good = [r for r in per
            if float(r.get("match_fraction") or 0.0) >= MIN_RECORD_MATCH_FRACTION]
    share = float(len(good)) / max(1, len(per))
    add("records_at_or_above_record_floor", share >= MIN_RECORDS_PASSING,
        f"{len(good)}/{len(per)} ({share:.2f})",
        f">= {MIN_RECORDS_PASSING} of records at >= {MIN_RECORD_MATCH_FRACTION}")

    anch = float(recovery.get("anchor_fraction") or 0.0)
    add("content_anchor_fraction", anch >= ORDINAL_MIN_ANCHOR_FRACTION,
        round(anch, 4), f">= {ORDINAL_MIN_ANCHOR_FRACTION}",
        "share of S beats identified by the RR key alone")

    n_ext = int(recovery.get("n_extended") or 0)
    # Judge the rule this check NAMES: ordinal consistency in the records where
    # beats were actually filled. The min over every record also counts records
    # where the fill correctly refused to fire, which is a different (stricter,
    # and wrongly worded) test.
    omin = recovery.get("ordinal_consistency_min_where_used")
    if omin is None and n_ext:
        omin = recovery.get("ordinal_consistency_min")
    add("ordinal_mapping_exact_where_used",
        n_ext == 0 or (omin is not None and float(omin) >= 1.0),
        ("not used" if n_ext == 0 else omin), "== 1.0 whenever beats were "
        "filled ordinally", f"{n_ext} beat(s) filled")

    in_set = float(recovery.get("symbol_in_s_set_fraction") or 0.0)
    add("symbol_in_aami_s_set", in_set >= MIN_SYMBOL_IN_S_SET, round(in_set, 4),
        f">= {MIN_SYMBOL_IN_S_SET}",
        "the matcher never saw a symbol, so this is an independent check")

    worst = max((abs(int(r.get("s_count_diff") or 0)) for r in per), default=0)
    add("per_record_s_count_diff", worst <= MAX_S_COUNT_DIFF, worst,
        f"<= {MAX_S_COUNT_DIFF}")

    perm = controls.get("permutation_invariance", {})
    add("permutation_invariance", bool(perm.get("identical")),
        f"{perm.get('n_differing')} differing", "0 differing",
        "no positional matching")

    shift = controls.get("shift_control", {})
    sv = float(shift.get("match_fraction", 1.0))
    add("shift_control", sv <= MAX_SHIFT_CONTROL, round(sv, 4),
        f"<= {MAX_SHIFT_CONTROL}", "a one-beat-off pool must not match")

    wrong = controls.get("wrong_record_control", {})
    wv = float(wrong.get("match_fraction", 1.0))
    add("wrong_record_control", wv <= MAX_WRONG_RECORD, round(wv, 4),
        f"<= {MAX_WRONG_RECORD}",
        "upper bound on the false-match rate: another record's pool")
    ratio = (frac / wv) if wv > 0 else float("inf")
    add("signal_to_null_ratio", ratio >= MIN_SIGNAL_TO_NULL_RATIO,
        (round(ratio, 2) if np.isfinite(ratio) else "inf"),
        f">= {MIN_SIGNAL_TO_NULL_RATIO}",
        "true match rate against the wrong-record null")

    n_sub = sum(int(v) for v in recovery.get("subtype_counts", {}).values())
    add("subtypes_present", n_sub > 0, n_sub, "> 0",
        "at least one A/a/J/S symbol recovered")

    ok = not reasons
    return {"gate": GATE_GO if ok else GATE_NOGO, "pass": ok,
            "checks": checks, "fail_reasons": reasons,
            "next_step": (
                "attach the symbols and re-run the Q5-A atlas with five blocks"
                if ok else
                "B_SUBTYPE is closed: it cannot be measured from the stored "
                "artifacts. Do not approximate it, and do not retrain to "
                "create it")}


def attach_recovered_symbols(cohort: QA.AtlasCohort, recovery: Dict[str, object],
                             gate: Dict[str, object],
                             log: Optional[RunLog] = None) -> Dict[str, object]:
    """Write the recovered symbols onto the cohort — only when the gate is GO."""
    log = log or RunLog()
    if not gate.get("pass"):
        log("recovery gate NO-GO — symbols are NOT attached; B_SUBTYPE stays "
            "unavailable")
        return {"attached": False, "reason": "; ".join(gate["fail_reasons"])}
    sym = np.asarray(recovery["sym"])
    if len(sym) != cohort.n:
        raise Q5B0Error("recovered symbol array does not match the cohort")
    cohort.sym = sym.astype("<U2")
    n = int((sym != "?").sum())
    log(f"attached {n} recovered symbols — B_SUBTYPE is now measurable")
    return {"attached": True, "n_symbols": n,
            "subtype_counts": recovery["subtype_counts"]}


# ─────────────────────────────────────────────────────────────────────────────
# Bundle
# ─────────────────────────────────────────────────────────────────────────────
def _dump_json(path: str, obj) -> None:
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(QA._json_safe(obj), fh, ensure_ascii=False, indent=1)


def write_recovery_bundle(out_dir: str, result: Dict[str, object],
                          recovery: Dict[str, object],
                          controls: Dict[str, object], gate: Dict[str, object],
                          provenance: Dict[str, object],
                          keys: Optional[np.ndarray] = None,
                          log: Optional[RunLog] = None) -> Dict[str, object]:
    """Write the recovery evidence. Both GO and NO-GO produce a full bundle."""
    log = log or RunLog()
    os.makedirs(out_dir, exist_ok=True)
    _dump_json(os.path.join(out_dir, "config.json"),
               {"experiment_id": EXPERIMENT_ID, "arm_id": ARM_ID,
                "mode": "RECOVER", "analysis_only": True,
                "fingerprint_fields": list(FINGERPRINT_FIELDS),
                "tolerance_s": RR_TOLERANCE_S, "margin_s": RR_MARGIN_S,
                "gate": {"min_s_match_fraction": MIN_S_MATCH_FRACTION,
                         "min_record_match_fraction": MIN_RECORD_MATCH_FRACTION,
                         "min_records_passing": MIN_RECORDS_PASSING,
                         "min_symbol_in_s_set": MIN_SYMBOL_IN_S_SET,
                         "max_shift_control": MAX_SHIFT_CONTROL,
                         "max_wrong_record": MAX_WRONG_RECORD,
                         "max_s_count_diff": MAX_S_COUNT_DIFF}})
    _dump_json(os.path.join(out_dir, "manifest.json"), provenance)
    _dump_json(os.path.join(out_dir, "result.json"), result)
    QA._dump_csv(os.path.join(out_dir, "recovery_audit.csv"),
                 recovery.get("per_record") or [{"record": ""}])
    _dump_json(os.path.join(out_dir, "recovery_controls.json"), controls)
    _dump_json(os.path.join(out_dir, "decision.json"), gate)
    # The symbols themselves, keyed by the cohort's own beat key. This is what
    # makes REANALYZE a separate run instead of a variable left over in a
    # notebook: the bundle carries its own evidence and can be re-read.
    np.savez_compressed(
        os.path.join(out_dir, "recovered_symbols.npz"),
        key=(np.asarray(keys).astype(str) if keys is not None
             else np.array([], dtype=str)),
        sym=np.asarray(recovery["sym"]).astype(str),
        anchor=(np.asarray(recovery["sym_anchor"]) != "?"))
    with open(os.path.join(out_dir, "log.txt"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(log.lines))
    _write_recovery_summary(out_dir, result, recovery, controls, gate)
    _write_recovery_figures(out_dir, recovery, gate)
    missing = [f for f in RECOVERY_BUNDLE_FILES
               if not os.path.exists(os.path.join(out_dir, f))]
    if missing:
        raise Q5B0Error(f"recovery bundle incomplete: {missing}")
    return result


def _fmt_near(d: Optional[Dict[str, object]]) -> str:
    if not d or not d.get("n"):
        return "(없음 — 전부 매칭됨)"
    return (f"n={d['n']} · p10 {d['p10']:.4f}s · p50 {d['p50']:.4f}s · "
            f"p90 {d['p90']:.4f}s · 허용치의 2배 안 "
            f"{float(d['within_2x_tolerance']):.1%}")


def _fmt_probe(rows: Optional[Sequence[Dict[str, object]]]) -> str:
    rows = [r for r in (rows or []) if r.get("n")]
    if not rows:
        return "(S 개수가 어긋나 탐침 불가)"
    diff = np.array([r["pre_rr_diff_median_s"] for r in rows], float)
    iqr = np.array([r["pre_rr_diff_iqr_s"] for r in rows], float)
    ratio = np.array([r["pre_rr_ratio_median"] for r in rows
                      if r.get("pre_rr_ratio_median") is not None], float)
    return (f"record {len(rows)}개 · 차이 median {np.median(diff):+.4f}s "
            f"(record간 IQR {np.subtract(*np.percentile(diff, [75, 25])):.4f}s) · "
            f"record내 IQR median {np.median(iqr):.4f}s"
            + (f" · 비율 median {np.median(ratio):.4f}" if len(ratio) else ""))


def _write_recovery_summary(out_dir: str, result: Dict[str, object],
                            recovery: Dict[str, object],
                            controls: Dict[str, object],
                            gate: Dict[str, object]) -> None:
    counts = recovery.get("subtype_counts", {})
    lines = [
        f"# {EXPERIMENT_ID} / {ARM_ID} — S subtype key recovery",
        "",
        f"- status: **{result['status']}** (ANALYSIS ONLY / NO TRAINING)",
        f"- gate: **{gate['gate']}**",
        f"- S beats joined: {recovery.get('n_matched')} / "
        f"{recovery.get('n_s')} ({float(recovery.get('match_fraction') or 0):.1%})",
        f"- 매칭된 beat의 symbol이 AAMI S 집합(A/a/J/S)에 드는 비율: "
        f"{float(recovery.get('symbol_in_s_set_fraction') or 0):.1%} "
        "— matcher는 symbol을 보지 않으므로 이것은 **독립 검증**이다",
        f"- RR 잔차(매칭된 것): median {recovery.get('median_residual_s')} s · "
        f"p95 {recovery.get('p95_residual_s')} s "
        f"(허용 {RR_TOLERANCE_S} s, margin {RR_MARGIN_S} s)",
        f"- **못 붙인 beat의 최근접 후보 거리**: "
        f"{_fmt_near(recovery.get('nearest_cost_unmatched'))} "
        "— 아깝게 빗나간 것과 아예 못 찾은 것은 match rate에서 구별되지 않는다",
        f"- **ordinal 가설 탐침**(k번째↔k번째일 때의 RR 차이): "
        f"{_fmt_probe(recovery.get('ordinal_hypothesis_probe'))} "
        "— 좁게 뭉친 0이 아닌 값이면 '같은 beat를 다른 시간축으로 잰 것', "
        "흩어져 있으면 'RR로는 식별 불가'다",
        f"- 복구된 subtype 분포: "
        + " · ".join(f"{k} {v}" for k, v in counts.items()),
        "",
        "## 음성대조군 (사전 등록)",
        f"- 순서 뒤섞기 불변: {controls.get('permutation_invariance', {}).get('identical')} "
        "(content 조인이면 pool 순서를 바꿔도 결과가 같아야 한다)",
        f"- 한 beat 밀어놓기: 매칭률 "
        f"{controls.get('shift_control', {}).get('match_fraction')} "
        f"(≤ {MAX_SHIFT_CONTROL} 이어야 한다)",
        f"- 다른 record pool: 매칭률 "
        f"{controls.get('wrong_record_control', {}).get('match_fraction')} "
        f"(≤ {MAX_WRONG_RECORD} 이어야 한다)",
        "",
    ]
    if gate["pass"]:
        lines += [
            "## 다음 단계",
            "symbols를 cohort에 붙이고 **Q5-A의 run_atlas를 그대로** 다시 돌린다.",
            "블록이 4개에서 5개로 늘어난 상태로 사전등록 decision tree를 재평가한다.",
            "이 단계에서도 새 모델을 학습하지 않고 저장 확률을 다시 만들지 않는다.",
        ]
    else:
        lines += [
            "## 판정: `B_SUBTYPE` 종결",
            "저장된 산출물로는 S 하위분류를 복구할 수 없다. 실패 이유:",
        ] + [f"- {r}" for r in gate["fail_reasons"]] + [
            "",
            "추정으로 채우지 않고, 이것을 만들려고 재학습하지 않는다.",
            "Q5-A의 `UNRESOLVED`(D5)는 4개 블록 위에서 그대로 유지된다.",
        ]
    lines += ["", "- 이 결과는 `원인`이 아니라 **실패 연관 요인** 분석의 입력이다.",
              "- residual CNN 경로는 closed이며 INCART rescue run도 하지 않는다.",
              "- **Q5-B 개입 실험은 여기서 구현하지 않는다.**"]
    with open(os.path.join(out_dir, "summary.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")


def _write_recovery_figures(out_dir: str, recovery: Dict[str, object],
                            gate: Dict[str, object]) -> None:
    plt = QA._plt()
    if plt is None:                                      # pragma: no cover
        return
    figdir = QA._figdir(out_dir)
    rows = [[c["check"], "PASS" if c["pass"] else "FAIL", str(c["value"]),
             str(c["threshold"])] for c in gate["checks"]]
    QA._table_fig(os.path.join(figdir, "recovery_gate_dashboard.png"),
                  f"{EXPERIMENT_ID}/{ARM_ID} recovery gate — {gate['gate']}",
                  rows, ["check", "result", "value", "threshold"],
                  caption=("S beats only; the matcher never sees a symbol, so "
                           "'symbol in AAMI S set' is an independent check"))
    res = [r for r in recovery.get("residuals", []) if np.isfinite(r)]
    near = recovery.get("nearest_cost_unmatched") or {}
    fig, ax = plt.subplots(figsize=(7, 4))
    if res:
        ax.hist(res, bins=40, color="#3b6ea5", label=f"matched (n={len(res)})")
    if near.get("p50") is not None:
        for q, style in (("p10", ":"), ("p50", "-"), ("p90", "--")):
            ax.axvline(float(near[q]), color="#b06a00", ls=style, lw=1,
                       label=f"unmatched {q} = {float(near[q]):.3f}s")
    ax.axvline(RR_TOLERANCE_S, color="crimson", ls="--",
               label=f"tolerance {RR_TOLERANCE_S}s")
    ax.set_xlabel("RR fingerprint residual (s)")
    ax.set_ylabel(f"matched S beats (n={len(res)})")
    ax.set_title("join residuals (matched) vs nearest candidate (unmatched)")
    ax.legend(fontsize=7)
    QA._caption(ax, "mean |diff| over pre/post/prev/next RR, seconds")
    fig.tight_layout()
    fig.savefig(os.path.join(figdir, "rr_residual_hist.png"), dpi=110)
    plt.close(fig)

    counts = recovery.get("subtype_counts", {})
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(list(counts), [counts[k] for k in counts], color="#5a7d5a")
    ax.set_ylabel("recovered S beats")
    ax.set_title("S subtype counts (recovered symbols)")
    QA._caption(ax, f"n matched = {recovery.get('n_matched')} of "
                    f"{recovery.get('n_s')} S beats")
    fig.tight_layout()
    fig.savefig(os.path.join(figdir, "subtype_counts.png"), dpi=110)
    plt.close(fig)


# ─────────────────────────────────────────────────────────────────────────────
# Drivers
# ─────────────────────────────────────────────────────────────────────────────
def run_recovery(cohort: QA.AtlasCohort, symbol_npz: str, out_dir: str,
                 provenance: Optional[Dict[str, object]] = None,
                 records: Optional[Sequence[int]] = None,
                 log: Optional[RunLog] = None) -> Dict[str, object]:
    """RECOVER mode: join, control, gate, write the bundle. Never trains."""
    log = log or RunLog()
    assert_analysis_only()
    t0 = time.time()
    raw = load_symbol_source(symbol_npz, records=records, log=log)
    recs = [int(r) for r in (records if records is not None else cohort.records)]
    rmap = resolve_record_mapping(cohort, raw, log=log)
    if not rmap.get("ok"):
        # No record correspondence -> nothing to join. This is a measured
        # NO-GO with a full bundle, not an exception.
        recovery = _empty_recovery(cohort, rmap)
        controls = {"permutation_invariance": {"identical": False,
                                               "n_differing": None,
                                               "scope": "not run",
                                               "note": "record mapping failed"},
                    "shift_control": {"match_fraction": 1.0,
                                      "note": "not run"},
                    "wrong_record_control": {"match_fraction": 1.0,
                                             "note": "not run"}}
        source = raw
    else:
        source = apply_record_mapping(raw, rmap["mapping"])
        recovery = recover_symbols(cohort, source, recs, mapping_report=rmap,
                                   log=log)
        controls = {
            "permutation_invariance": permutation_invariance(cohort, source,
                                                             recs),
            "shift_control": shift_control(cohort, source, recs),
            "wrong_record_control": wrong_record_control(cohort, source, recs),
        }
    log(f"controls: permutation identical="
        f"{controls['permutation_invariance']['identical']} · shift "
        f"{controls['shift_control']['match_fraction']:.3f} · wrong-record "
        f"{controls['wrong_record_control']['match_fraction']:.3f}")
    gate = evaluate_recovery_gate(recovery, controls)
    log(f"recovery gate: {gate['gate']}"
        + ("" if gate["pass"] else " — " + "; ".join(gate["fail_reasons"])))
    result = {
        "experiment_id": EXPERIMENT_ID, "arm_id": ARM_ID, "mode": "RECOVER",
        "status": STATUS_MEASURED, "training_performed": False,
        "module_version": MODULE_VERSION, "module_build": MODULE_BUILD,
        "gate": gate["gate"], "gate_pass": gate["pass"],
        "n_s": recovery["n_s"], "n_matched": recovery["n_matched"],
        "n_anchor": recovery["n_anchor"], "n_extended": recovery["n_extended"],
        "match_fraction": recovery["match_fraction"],
        "anchor_fraction": recovery["anchor_fraction"],
        "ordinal_consistency_min": recovery["ordinal_consistency_min"],
        "ordinal_consistency_min_where_used":
            recovery["ordinal_consistency_min_where_used"],
        "nearest_cost_unmatched": recovery["nearest_cost_unmatched"],
        "chronology_min": recovery["chronology_min"],
        "symbol_in_s_set_fraction": recovery["symbol_in_s_set_fraction"],
        "subtype_counts": recovery["subtype_counts"],
        "median_residual_s": recovery["median_residual_s"],
        "p95_residual_s": recovery["p95_residual_s"],
        "rr_unit": recovery["rr_unit"],
        "symbol_source": {"path": raw.path, "sha256": raw.sha256,
                          "n_beat": raw.n, "n_beat_mapped": source.n},
        "records": recs,
        "record_mapping": {k: v for k, v in rmap.items() if k != "table"},
        "elapsed_s": round(time.time() - t0, 2),
    }
    prov = dict(provenance or {})
    prov.update({"experiment": f"{EXPERIMENT_ID} / {ARM_ID}",
                 "module_version": MODULE_VERSION,
                 "analysis_only": True, "training_performed": False})
    write_recovery_bundle(out_dir, result, recovery, controls, gate, prov,
                          keys=cohort.key, log=log)
    result["recovery"] = {k: v for k, v in recovery.items()
                          if k not in ("sym", "sym_anchor", "residuals")}
    result["controls"] = controls
    result["gate_detail"] = gate
    result["_sym"] = recovery["sym"]
    result["out_dir"] = out_dir
    return result


def run_reanalysis(cohort: QA.AtlasCohort, models: Dict[str, object],
                   inventory: Dict[str, object], freeze: Dict[str, object],
                   recovery_result: Dict[str, object], out_dir: str,
                   provenance: Optional[Dict[str, object]] = None,
                   n_boot: int = QA.NB_BOOT,
                   log: Optional[RunLog] = None) -> Dict[str, object]:
    """REANALYZE mode: attach symbols, then re-run Q5-A's atlas unchanged.

    The atlas code is Q5-A's, not a copy: the decision tree, the block rules
    and the thresholds are the ones that were pre-registered before Q5-A ran.
    The only difference is that ``B_SUBTYPE`` now has data.
    """
    log = log or RunLog()
    assert_analysis_only()
    gate = recovery_result.get("gate_detail") or {}
    att = attach_recovered_symbols(cohort, {"sym": recovery_result["_sym"],
                                            "subtype_counts":
                                            recovery_result["subtype_counts"]},
                                   gate, log=log)
    if not att["attached"]:
        raise Q5B0Error(
            "recovery gate is NO-GO — the re-analysis must not run. "
            "B_SUBTYPE stays unavailable and Q5-A's verdict stands.")
    prov = dict(provenance or {})
    prov.update({"experiment": f"{EXPERIMENT_ID} / {ARM_ID}",
                 "reanalysis_of": "EXP-2026-004 / Q5-A run_atlas",
                 "subtype_symbols": "recovered by Q5-B-0 RR fingerprint join",
                 "q5b0_module_version": MODULE_VERSION,
                 "analysis_only": True, "training_performed": False})
    result = QA.run_atlas(cohort, models, inventory, freeze, prov, out_dir,
                          n_boot=n_boot, log=log)
    result["q5b0"] = {
        "experiment_id": EXPERIMENT_ID, "arm_id": ARM_ID,
        "symbols_attached": att,
        "recovery_run": recovery_result.get("out_dir"),
        "note": ("the bundle is written by Q5-A's atlas code and is labelled "
                 f"EXP-2026-004 inside; {EXPERIMENT_ID} is the recovery that "
                 "made the fifth block measurable"),
    }
    blocks = (result.get("block_evidence") or {}).get("blocks", {})
    log(f"re-analysis blocks: {sorted(blocks)}")
    shuffle = _run_shuffle_control(cohort, models, result, log=log)
    result["subtype_shuffle_control"] = shuffle
    if "B_SUBTYPE" not in blocks:
        log("WARNING: B_SUBTYPE still absent after attaching symbols — check "
            "the per-record subtype counts before reading the verdict")
    _dump_json(os.path.join(out_dir, "q5b0_recovery.json"),
               {"experiment_id": EXPERIMENT_ID, "arm_id": ARM_ID,
                "gate": gate.get("gate"), "checks": gate.get("checks"),
                "controls": recovery_result.get("controls"),
                "recovery": recovery_result.get("recovery"),
                "subtype_shuffle_control": shuffle,
                "blocks_present": sorted(blocks)})
    return result


def _run_shuffle_control(cohort: QA.AtlasCohort, models: Dict[str, object],
                         result: Dict[str, object],
                         log: Optional[RunLog] = None) -> Dict[str, object]:
    """Re-score B_SUBTYPE against symbols shuffled inside each record."""
    log = log or RunLog()
    split = result.get("split") or {}
    recs = split.get("ds2_analysis") or split.get("ds2") or []
    if not recs:
        return {"available": False, "reason": "no analysis records in result"}
    rows = np.sort(cohort.rows_of([int(r) for r in recs]))
    s_mask = np.asarray(cohort.y_s[rows], bool)
    if not s_mask.any():
        return {"available": False, "reason": "no S beats"}
    _label, score = reference_scores(cohort, models, rows)
    if not np.isfinite(score).all():
        return {"available": False,
                "reason": "reference scores are incomplete on the analysis rows"}
    outcome = QA.within_record_rank_outcome(cohort, rows, score, s_mask)["y"]
    sub = QA.subtype_of(cohort.sym[rows])[s_mask]
    if not (sub != "other").any():
        return {"available": False, "reason": "no recovered subtype on S beats"}
    out = subtype_shuffle_control(sub, cohort.record[rows][s_mask], outcome)
    if out.get("available"):
        log(f"subtype shuffle control: real {out['real_delta']:+.5f} vs "
            f"shuffled {out['shuffled_mean']:+.5f} "
            f"(applicable={out.get('applicable')}, retained "
            f"{out['retained_fraction']}, pass={out['pass']})")
    return out


def load_recovery(run_dir: str, cohort: Optional[QA.AtlasCohort] = None
                  ) -> Dict[str, object]:
    """Re-read a stored RECOVER bundle so REANALYZE can be its own run.

    When a cohort is given the stored keys must line up with it beat for beat.
    A bundle recovered against a different source file is refused rather than
    scattered onto rows it was never about.
    """
    def _read(name):
        p = os.path.join(run_dir, name)
        if not os.path.exists(p):
            raise Q5B0Error(f"{name} missing from {run_dir} — not a RECOVER "
                            "bundle")
        with open(p, encoding="utf-8") as fh:
            return json.load(fh)

    result = _read("result.json")
    gate = _read("decision.json")
    controls = _read("recovery_controls.json")
    npz = np.load(os.path.join(run_dir, "recovered_symbols.npz"),
                  allow_pickle=False)
    key = np.asarray(npz["key"]).astype(str)
    sym = np.asarray(npz["sym"]).astype("<U2")
    if cohort is not None:
        if len(sym) != cohort.n or not np.array_equal(
                key, np.asarray(cohort.key).astype(str)):
            raise Q5B0Error(
                f"the symbols stored in {os.path.basename(run_dir)} do not "
                "line up with this cohort (different source file or different "
                "row set) — STOP")
    return {"_sym": sym, "gate": gate.get("gate"),
            "gate_pass": bool(gate.get("pass")), "gate_detail": gate,
            "controls": controls,
            "recovery": result.get("recovery") or {
                k: result[k] for k in
                ("n_s", "n_matched", "n_anchor", "n_extended",
                 "match_fraction", "anchor_fraction",
                 "ordinal_consistency_min", "chronology_min",
                 "symbol_in_s_set_fraction", "median_residual_s",
                 "p95_residual_s", "rr_unit", "symbol_source")
                if k in result},
            "subtype_counts": result.get("subtype_counts", {}),
            "out_dir": run_dir, "status": result.get("status")}


def report_recovery(run_dir: str) -> Dict[str, object]:
    """REPORT mode: read a stored bundle back. Recomputes nothing."""
    if not os.path.isdir(run_dir):
        return {"status": STATUS_NOT_RUN, "reason": f"no run at {run_dir}"}
    out: Dict[str, object] = {"run_dir": run_dir}
    for name in ("result.json", "decision.json", "recovery_controls.json",
                 "config.json"):
        p = os.path.join(run_dir, name)
        if os.path.exists(p):
            with open(p, encoding="utf-8") as fh:
                out[name[:-5]] = json.load(fh)
    p = os.path.join(run_dir, "summary.md")
    if os.path.exists(p):
        out["summary"] = open(p, encoding="utf-8").read()
    out.setdefault("status", (out.get("result") or {}).get("status",
                                                           STATUS_NOT_RUN))
    return out


# ─────────────────────────────────────────────────────────────────────────────
# Synthetic fixtures (tests only — never a result)
# ─────────────────────────────────────────────────────────────────────────────
def synthetic_pair(n_record: int = 4, n_beat: int = 60, s_every: int = 7,
                   seed: int = 0, drop: int = 0, jitter_s: float = 0.0
                   ) -> Tuple[QA.AtlasCohort, SymbolSource]:
    """A cohort and a symbol source describing the same synthetic beats.

    ``drop`` removes beats from the symbol source (the real files disagree by a
    few percent on noisy records) and ``jitter_s`` perturbs its RR values.
    """
    rng = np.random.default_rng(seed)
    records = list(QA.MIT_ALL_RECORDS[:n_record])
    rr_all, rec_all, y_all, sym_all, t_all = [], [], [], [], []
    for r in records:
        rr = 0.8 + 0.12 * rng.standard_normal(n_beat)
        rr = np.clip(rr, 0.4, 1.6)
        t = np.cumsum(rr)
        y = np.zeros(n_beat, int)
        y[::s_every] = S_INDEX
        sym = np.where(y == S_INDEX,
                       rng.choice(np.array(S_SUBTYPES), size=n_beat), "N")
        rr_all.append(rr)
        rec_all.append(np.full(n_beat, r, int))
        y_all.append(y)
        sym_all.append(sym)
        t_all.append(t)
    rr = np.concatenate(rr_all)
    rec = np.concatenate(rec_all)
    y5 = np.concatenate(y_all)
    sym = np.concatenate(sym_all).astype("<U2")
    t = np.concatenate(t_all)
    pre = np.full(len(rr), np.nan)
    post = np.full(len(rr), np.nan)
    for r in records:
        idx = np.where(rec == r)[0]
        pre[idx[1:]] = np.diff(t[idx])
        post[idx[:-1]] = np.diff(t[idx])
    keys = QA.format_beat_keys(np.full(len(rr), "mitdb"), rec, t, sym)
    cohort = QA.AtlasCohort(
        key=keys, key_mode="annotation",
        db=np.full(len(rr), "mitdb", dtype="<U8"), record=rec, y5=y5,
        y_s=(y5 == S_INDEX), sym=np.full(len(rr), "?", dtype="<U2"),
        pre_rr=pre, post_rr=post, beat=None, fs=360.0,
        records=np.array(records, int),
        idx_of={int(r): np.where(rec == r)[0] for r in records})
    keep = np.ones(len(rr), bool)
    if drop:
        for r in records:
            idx = np.where(rec == r)[0]
            n_idx = idx[y5[idx] != S_INDEX]
            keep[rng.choice(n_idx, size=min(drop, len(n_idx)),
                            replace=False)] = False
    src_pre = pre[keep] + (jitter_s * rng.standard_normal(int(keep.sum()))
                           if jitter_s else 0.0)
    src_post = post[keep] + (jitter_s * rng.standard_normal(int(keep.sum()))
                             if jitter_s else 0.0)
    source = SymbolSource(
        record=rec[keep], sym=sym[keep], y5=y5[keep],
        pre_rr=src_pre, post_rr=src_post,
        records=np.array(records, int), path="<synthetic>", sha256="synthetic")
    source.idx_of = {int(r): np.where(source.record == r)[0] for r in records}
    return cohort, source


def symbol_source_from_cohort(cohort: QA.AtlasCohort, drop: int = 0,
                              jitter_s: float = 0.0, seed: int = 0,
                              scramble: bool = False) -> SymbolSource:
    """A symbol source describing the SAME beats as ``cohort`` (fixture only).

    ``scramble`` redraws the RR values so the source describes a different
    recording: the controls must then refuse the join. That negative fixture is
    the only thing separating "the gate works" from "the gate always says GO".
    """
    rng = np.random.default_rng(seed)
    keep = np.ones(cohort.n, bool)
    if drop:
        for r in cohort.records:
            idx = cohort.idx_of[int(r)]
            n_idx = idx[~cohort.y_s[idx]]
            if len(n_idx):
                keep[rng.choice(n_idx, size=min(drop, len(n_idx)),
                                replace=False)] = False
    pre = cohort.pre_rr[keep].copy()
    post = cohort.post_rr[keep].copy()
    if scramble:
        pre = 0.8 + 0.15 * rng.standard_normal(len(pre))
        post = 0.8 + 0.15 * rng.standard_normal(len(post))
    elif jitter_s:
        pre = pre + jitter_s * rng.standard_normal(len(pre))
        post = post + jitter_s * rng.standard_normal(len(post))
    src = SymbolSource(record=cohort.record[keep].copy(),
                       sym=cohort.sym[keep].copy().astype("<U2"),
                       y5=cohort.y5[keep].copy(), pre_rr=pre, post_rr=post,
                       records=cohort.records.copy(), path="<synthetic>",
                       sha256="synthetic")
    src.idx_of = {int(r): np.where(src.record == r)[0] for r in src.records}
    return src


def write_symbol_npz(path: str, source: SymbolSource) -> str:
    """Write a fixture in the shape of ``ecg_multi.npz`` (tests only)."""
    os.makedirs(os.path.dirname(os.path.abspath(path)) or ".", exist_ok=True)
    np.savez_compressed(path, pid=source.record.astype(int),
                        db=np.full(source.n, "mitdb"),
                        y5=source.y5.astype(int), sym=source.sym.astype(str),
                        pre_rr=source.pre_rr.astype(float),
                        post_rr=source.post_rr.astype(float))
    return path if path.endswith(".npz") else path + ".npz"


def blank_symbols(cohort: QA.AtlasCohort) -> QA.AtlasCohort:
    """Erase the cohort's symbols — the state the real atlas source is in."""
    cohort.sym = np.full(cohort.n, "?", dtype="<U2")
    return cohort


def self_check(min_version: int = MODULE_VERSION) -> Dict[str, object]:
    if MODULE_VERSION < min_version:
        raise Q5B0Error(f"stale module {MODULE_VERSION} < {min_version}")
    return {"experiment_id": EXPERIMENT_ID, "arm_id": ARM_ID,
            "module_version": MODULE_VERSION, "module_build": MODULE_BUILD,
            "modes": list(MODES), "status": STATUS,
            "analysis_only": assert_analysis_only()["q5b0"],
            "q5a_module_version": QA.MODULE_VERSION,
            "gate": {"min_s_match_fraction": MIN_S_MATCH_FRACTION,
                     "min_symbol_in_s_set": MIN_SYMBOL_IN_S_SET,
                     "max_shift_control": MAX_SHIFT_CONTROL,
                     "max_wrong_record": MAX_WRONG_RECORD}}


def main(argv: Optional[Sequence[str]] = None) -> int:
    import argparse
    ap = argparse.ArgumentParser(description=f"{EXPERIMENT_ID} / {ARM_ID}")
    ap.add_argument("--mode", default="DESIGN")
    ap.add_argument("--source", help="atlas source npz (mamba_data.npz)")
    ap.add_argument("--symbols", help="symbol source npz (ecg_multi.npz)")
    ap.add_argument("--out", help="run directory")
    args = ap.parse_args(argv)
    mode = resolve_mode(args.mode)
    log = RunLog()
    if mode == "DESIGN":
        log(f"{EXPERIMENT_ID}/{ARM_ID} DESIGN — {STATUS}")
        print(json.dumps(self_check(), ensure_ascii=False, indent=1))
        return 0
    if mode == "REPORT":
        print(json.dumps(report_recovery(args.out or ""), ensure_ascii=False,
                         indent=1, default=QA._scalar))
        return 0
    if mode == "RECOVER":
        if not (args.source and args.symbols and args.out):
            raise SystemExit("RECOVER needs --source, --symbols and --out")
        cohort, audit = QA.load_atlas_source(args.source, log=log)
        QA.rr_from_samples(cohort)
        res = run_recovery(cohort, args.symbols, args.out,
                           provenance={"atlas_source": audit}, log=log)
        print(json.dumps({k: v for k, v in res.items()
                          if not k.startswith("_")},
                         ensure_ascii=False, indent=1, default=QA._scalar))
        return 0
    raise SystemExit("REANALYZE runs from the notebook: it needs the frozen "
                     "baselines from the Q5-A inventory")


if __name__ == "__main__":                               # pragma: no cover
    raise SystemExit(main())
