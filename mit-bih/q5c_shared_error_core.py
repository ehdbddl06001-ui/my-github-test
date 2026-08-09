"""EXP-2026-006 / Q5-C — the shared error core (ANALYSIS ONLY / NO TRAINING).

Why this exists
---------------
Q5-A ended at ``UNRESOLVED`` (D5) and left one fact uninterpreted: V10 and
V9_BASE — two different lineages — are wrong on **710 of 1,628 S beats
(43.6%)** at the same time, while their worst *patients* barely overlap
(minimum pairwise overlap 0.333). Failure that does not persist per patient
but does persist per beat is a different object from the one the patient
blocks were built to describe, and nobody has looked at it.

Two corrections are built into this experiment before it starts.

1. **43.6% is not the number to explain.** It is threshold-based — the very
   definition Q5-A demoted after measuring that a prevalence-matched cut makes
   two thirds of S beats "errors" by construction. If each model is wrong on
   ~53% and ~55% of S beats independently, 29.1% would co-fail by arithmetic
   alone. The quantity worth a name is the EXCESS over that.
2. **Comparing beats across records re-imports the patient effect** that Q5-A
   already found to be the leading block. So hardness is defined *within a
   record, among that record's own S beats*, which fixes the chance baseline
   at 0.5^4 = 6.25% for four models and makes the excess patient-free by
   construction.

What it does
------------
Ranks each record's S beats by within-record badness under each frozen model,
calls a beat *hard* for that model when it lands in the worse half, and asks
what the beats that are hard under **all four** models have in common — using
only the feature blocks Q5-A pre-registered, so nothing is fished for. The
pre-registered tree can end at "the shared core is real but nothing we measure
explains it", and that verdict is a result, not a failure.

Trains nothing, regenerates no probabilities, and proposes no model.
"""

from __future__ import annotations

import json
import os
import sys
import time
from dataclasses import dataclass
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import q5a_patient_failure_atlas as QA          # noqa: E402
import q4o_leakage_free_residual as Q4O         # noqa: E402

EXPERIMENT_ID = "EXP-2026-006"
ARM_ID = "Q5-C"
RUN_SLUG = "q5c_shared_error_core"
MODULE_VERSION = 3
MODULE_BUILD = "2026-08-09"

MODES = ("DESIGN", "ANALYZE", "REPORT")
STATUS = "DESIGN / RESULT NOT RUN"

RunLog = QA.RunLog
S_INDEX = QA.S_INDEX

# ── pre-registered definitions (fixed before any number is looked at) ────────
#
# "hard for this model" = in the worse half of THIS RECORD's S beats, ranked by
# the within-record badness Q5-A settled on as its primary outcome. Half by
# construction, so the chance rate of being hard under all K models is 0.5**K
# and the excess needs no modelling assumption.
HARD_FRACTION = 0.50
#: A record needs enough S beats for "worse half" to mean anything.
CORE_MIN_S_PER_RECORD = 8
#: Blocks are Q5-A's, unchanged. B_SUBTYPE is permanently closed (EXP-2026-005)
#: and B_PATIENT is deliberately excluded: hardness is already defined within a
#: record, so a patient-identity feature would be explaining a variable it has
#: been conditioned out of.
CORE_BLOCKS = ("B_ATRIAL", "B_RR", "B_QUALITY")

# ── pre-registered decision thresholds ──────────────────────────────────────
#: The shared core must be more than two mediocre models overlapping.
EXCESS_MIN = 1.25
#: Out-of-patient discrimination that counts as "the measured features explain
#: membership". 0.55 is deliberately modest — the point is whether anything is
#: there at all, not how good a classifier could be.
AUROC_MIN = 0.55
#: A structured finding must collapse when membership is shuffled inside the
#: record it came from.
SHUFFLE_MAX_RETAINED = 0.25
SHUFFLE_REPEATS = 5
NB_BOOT = QA.NB_BOOT

BRANCH_STRUCTURED = "SHARED_CORE_STRUCTURED"
BRANCH_UNSTRUCTURED = "SHARED_CORE_UNSTRUCTURED"
BRANCH_NO_EXCESS = "NO_SHARED_CORE"
BRANCH_INSUFFICIENT = "INSUFFICIENT_ARTIFACTS"
BRANCHES = (BRANCH_STRUCTURED, BRANCH_UNSTRUCTURED, BRANCH_NO_EXCESS,
            BRANCH_INSUFFICIENT)

STATUS_MEASURED = QA.STATUS_MEASURED
STATUS_NOT_RUN = QA.STATUS_NOT_RUN

BUNDLE_FILES = ("config.json", "manifest.json", "result.json", "log.txt",
                "core_membership.csv", "co_error_matrix.csv",
                "feature_contrast.csv", "decision.json", "summary.md")
FIGURES = ("co_error_excess.png", "core_concentration.png",
           "feature_contrast.png", "core_decision.png")


class Q5CError(RuntimeError):
    """Stop condition. Q5-C never invents a feature to explain a core."""


def run_dir_name(timestamp: str) -> str:
    return f"{timestamp}_{EXPERIMENT_ID}_{RUN_SLUG}"


def resolve_mode(mode: str) -> str:
    m = str(mode).strip().upper()
    if m not in MODES:
        raise Q5CError(f"mode must be exactly one of {MODES}, got {mode!r}")
    return m


def assert_analysis_only() -> Dict[str, object]:
    return {"q5c": QA.assert_analysis_only(os.path.abspath(__file__)),
            "q5a": QA.assert_analysis_only()}


# ─────────────────────────────────────────────────────────────────────────────
# Hardness, defined inside a record
# ─────────────────────────────────────────────────────────────────────────────
@dataclass
class CoreMembership:
    """Per S beat: which models found it hard, and the record it belongs to."""

    record: np.ndarray            # (n_s,) int
    hard: np.ndarray              # (n_s, n_model) bool
    badness: np.ndarray           # (n_s, n_model) float — within-record rank
    labels: Tuple[str, ...]
    rows: np.ndarray              # cohort row index of each S beat

    @property
    def n(self) -> int:
        return int(len(self.record))

    @property
    def n_hard_models(self) -> np.ndarray:
        return self.hard.sum(axis=1)

    @property
    def shared_hard(self) -> np.ndarray:
        return self.hard.all(axis=1)

    @property
    def shared_easy(self) -> np.ndarray:
        return ~self.hard.any(axis=1)


def build_membership(cohort: QA.AtlasCohort, models: Dict[str, object],
                     rows: np.ndarray,
                     log: Optional[RunLog] = None) -> CoreMembership:
    """Rank each record's S beats per model and split them at the median.

    The split is per record and per model, so "hard" carries no information
    about which record a beat is in or how good the model is overall — only
    about where the beat sits among its own record's S beats under that model.
    """
    log = log or RunLog()
    labels = tuple(sorted(models))
    s_mask = np.asarray(cohort.y_s[rows], bool)
    if not s_mask.any():
        raise Q5CError("no S beats in the analysis rows")
    rec_all = cohort.record[rows]
    s_rows = rows[s_mask]
    rec = rec_all[s_mask]

    badness = np.full((int(s_mask.sum()), len(labels)), np.nan)
    for j, lab in enumerate(labels):
        score = np.asarray(models[lab].score, float)
        if len(score) != len(rows):
            raise Q5CError(f"{lab}: score length {len(score)} != {len(rows)} "
                           "analysis rows — align before calling Q5-C")
        y = QA.within_record_rank_outcome(cohort, rows, score, s_mask)["y"]
        badness[:, j] = y

    hard = np.zeros_like(badness, bool)
    kept_records: List[int] = []
    for r in np.unique(rec):
        sel = np.where(rec == r)[0]
        if len(sel) < CORE_MIN_S_PER_RECORD:
            continue
        kept_records.append(int(r))
        for j in range(len(labels)):
            v = badness[sel, j]
            # worse half of THIS record's S beats under THIS model; ties are
            # broken by a stable order so the split is exactly reproducible.
            order = np.argsort(np.argsort(-v, kind="stable"), kind="stable")
            hard[sel[order < int(np.ceil(HARD_FRACTION * len(sel)))], j] = True

    if not kept_records:
        raise Q5CError(
            f"no record has {CORE_MIN_S_PER_RECORD} or more S beats, so "
            "'the worse half of this record's S beats' is undefined "
            "everywhere — this cohort cannot answer the question. Report it "
            "as INSUFFICIENT_ARTIFACTS rather than splitting 3 beats in two")
    keep = np.isin(rec, kept_records)
    m = CoreMembership(record=rec[keep], hard=hard[keep], badness=badness[keep],
                       labels=labels, rows=s_rows[keep])
    log(f"membership: {m.n} S beats over {len(kept_records)} record(s) with "
        f">= {CORE_MIN_S_PER_RECORD} S beats; shared-hard "
        f"{int(m.shared_hard.sum())} ({m.shared_hard.mean():.1%}), chance "
        f"{0.5 ** len(labels):.1%}")
    return m


def co_error_excess(m: CoreMembership, n_boot: int = NB_BOOT,
                    seed: int = Q4O.SEED0) -> Dict[str, object]:
    """Observed co-hardness against the chance rate, with a patient bootstrap.

    Because hardness is a within-record median split, each model is hard on
    exactly half of a record's S beats, so independence gives 0.5**K with no
    fitting. The bootstrap resamples RECORDS, not beats — the unit that
    generalises.
    """
    k = len(m.labels)
    chance = 0.5 ** k
    records = np.unique(m.record)
    # The reported estimate and its interval must be the SAME estimator. The
    # bootstrap resamples records, so the point estimate is the mean over
    # records of each record's shared-hard share — not the beat-pooled mean,
    # which would put a large record's rate where a patient-level interval
    # cannot follow it. Under independence both have expectation 0.5**k, so
    # the chance baseline is unchanged either way; the pooled value is
    # reported beside it rather than silently swapped in.
    per_record = np.array([m.shared_hard[m.record == r].mean()
                           for r in records], float)
    obs = float(per_record.mean())
    obs_micro = float(m.shared_hard.mean())
    rng = np.random.default_rng(seed)
    boot = []
    for _ in range(int(n_boot)):
        pick = rng.choice(len(records), size=len(records), replace=True)
        boot.append(float(per_record[pick].mean()))
    lo, hi = np.percentile(boot, [2.5, 97.5])
    pairs = {}
    for i in range(k):
        for j in range(i + 1, k):
            both = float((m.hard[:, i] & m.hard[:, j]).mean())
            pairs[f"{m.labels[i]}|{m.labels[j]}"] = {
                "both_hard": both, "chance": 0.25,
                "excess": both / 0.25 if both else 0.0}
    return {"n_model": k, "chance": chance, "observed": obs,
            "estimator": "record_macro",
            "observed_micro": obs_micro,
            "excess": obs / chance if chance else None,
            "excess_micro": obs_micro / chance if chance else None,
            "ci_low": float(lo / chance), "ci_high": float(hi / chance),
            "observed_ci": [float(lo), float(hi)],
            "by_pair": pairs, "n_beat": m.n,
            "n_record": int(len(records)),
            "definition": ("hard = worse half of this record's S beats under "
                           "this model; chance = 0.5**n_model by construction; "
                           "the reported rate is the mean over records, the "
                           "unit the bootstrap resamples")}


def core_concentration(m: CoreMembership) -> Dict[str, object]:
    """Is the shared core a few records, or is it everywhere?

    Two different questions live here and the first version of this function
    only answered one of them.

    * **Count** concentration — how many records hold most of the core beats.
      This tracks where the S beats are, not where the phenomenon is: if one
      record carries most of a cohort's S beats it will carry most of anything
      defined on S beats, core or not.
    * **Rate** uniformity — whether each record's own share of core beats is
      similar. This is the one that says whether the phenomenon is general.

    Reading the count alone can call a perfectly uniform effect a "record
    story". Both are reported, and the note says which to read.
    """
    core = m.shared_hard
    chance = 0.5 ** len(m.labels)
    per = []
    for r in np.unique(m.record):
        sel = m.record == r
        per.append({"record": int(r), "n_s": int(sel.sum()),
                    "n_core": int((sel & core).sum()),
                    "core_fraction": float(core[sel].mean()),
                    "excess_vs_chance": float(core[sel].mean() / chance)})
    per.sort(key=lambda d: -d["n_core"])
    total = max(1, int(core.sum()))
    cum = np.cumsum([p["n_core"] for p in per]) / total
    n50 = int(np.searchsorted(cum, 0.50) + 1)
    n80 = int(np.searchsorted(cum, 0.80) + 1)
    rates = np.array([p["core_fraction"] for p in per], float)
    if not len(rates):
        return {"per_record": [], "n_core": 0, "records_for_50pct": 0,
                "records_for_80pct": 0, "n_record": 0,
                "count_concentration": "n/a", "rate_min": None,
                "rate_max": None, "rate_median": None, "excess_min": None,
                "excess_max": None, "records_above_chance": 0,
                "rate_uniform": False, "share_of_s_in_largest": None,
                "note": "no record qualified — nothing to concentrate"}
    above = int((rates > chance).sum())
    return {"per_record": per, "n_core": int(core.sum()),
            "records_for_50pct": n50, "records_for_80pct": n80,
            "n_record": len(per),
            "count_concentration": ("concentrated"
                                    if n50 <= max(1, len(per) // 5)
                                    else "spread"),
            "rate_min": float(rates.min()), "rate_max": float(rates.max()),
            "rate_median": float(np.median(rates)),
            "excess_min": float(rates.min() / chance),
            "excess_max": float(rates.max() / chance),
            "records_above_chance": above,
            "rate_uniform": bool(rates.min() >= EXCESS_MIN * chance),
            "share_of_s_in_largest": float(max(p["n_s"] for p in per)
                                           / max(1, m.n)),
            "note": ("read the RATE row, not the count row: one record holding "
                     "most of the core usually just means it holds most of the "
                     "S beats. A record story is one where the rate itself is "
                     "confined to a record or two")}


# ─────────────────────────────────────────────────────────────────────────────
# Can anything we already measure explain membership?
# ─────────────────────────────────────────────────────────────────────────────
def core_blocks(cohort: QA.AtlasCohort, rows: np.ndarray,
                m: CoreMembership) -> Dict[str, Dict[str, np.ndarray]]:
    """Q5-A's blocks, restricted to the S beats that carry a membership label.

    No new feature is invented here. If Q5-A's registered features cannot see
    the core, that is the finding.
    """
    s_mask = np.asarray(cohort.y_s[rows], bool)
    keep = np.isin(rows[s_mask], m.rows)
    rr = QA.rr_features(cohort, rows)
    atrial = QA.atrial_proxies(cohort, rows)
    quality = QA.quality_proxies(cohort, rows)
    out: Dict[str, Dict[str, np.ndarray]] = {}
    src = {"B_ATRIAL": {k: v for k, v in atrial.items()
                        if k != "qrs_leakage_estimate"},
           "B_RR": rr, "B_QUALITY": quality}
    for name in CORE_BLOCKS:
        blk = {k: np.asarray(v)[s_mask][keep] for k, v in src[name].items()}
        if blk:
            out[name] = blk
    return out


def explain_membership(blocks: Dict[str, Dict[str, np.ndarray]],
                       m: CoreMembership, n_boot: int = NB_BOOT,
                       log: Optional[RunLog] = None) -> Dict[str, object]:
    """Out-of-patient discrimination of shared-hard vs shared-easy.

    Uses Q5-A's own grouped-holdout machinery so the comparison is scored the
    same way the atlas scored its blocks: fit on some patients, score on the
    held-out ones, never on the beats used to fit.
    """
    log = log or RunLog()
    core = m.shared_hard
    easy = m.shared_easy
    sel = core | easy
    y = core[sel].astype(int)
    groups = m.record[sel]
    out: Dict[str, object] = {
        "n_core": int(core.sum()), "n_easy": int(easy.sum()),
        "n_used": int(sel.sum()), "n_patient": int(len(np.unique(groups))),
        "contrast": "shared-hard vs shared-easy (the mixed beats are excluded "
                    "so the comparison is between the two extremes)"}
    if int(y.sum()) < QA.BLOCK_MIN_EVENTS or int((1 - y).sum()) < QA.BLOCK_MIN_EVENTS:
        out.update({"underpowered": True, "blocks": {},
                    "reason": (f"only {int(y.sum())} shared-hard / "
                               f"{int((1 - y).sum())} shared-easy beats "
                               f"(< {QA.BLOCK_MIN_EVENTS})")})
        return out
    out["underpowered"] = False
    blocks_sel = {name: {k: np.asarray(v)[sel] for k, v in blk.items()}
                  for name, blk in blocks.items()}
    ev = QA.evaluate_blocks(blocks_sel, y, groups, n_boot=n_boot, log=log,
                            outcome=QA.OUTCOME_FN)
    out["blocks"] = ev.get("blocks", {})
    joint = {f"{name}__{k}": v for name, blk in blocks_sel.items()
             for k, v in blk.items()}
    if joint:
        out["joint"] = QA.block_incremental_value({}, joint, y, groups,
                                                  n_boot=n_boot,
                                                  mode="classification")
        # A held-out AUROC needs its own null. Without one, 0.73 and 0.53 read
        # the same on the page. Labels are shuffled INSIDE each record, so the
        # null keeps every record's core rate intact.
        rng = np.random.default_rng(0)
        nulls = []
        for _ in range(SHUFFLE_REPEATS):
            sh = y.copy()
            for r in np.unique(groups):
                g = groups == r
                sh[g] = rng.permutation(sh[g])
            nulls.append(float(QA.block_incremental_value(
                {}, joint, sh, groups, n_boot=50,
                mode="classification").get("auroc_aug") or 0.5))
        out["auroc_null"] = {"mean": float(np.mean(nulls)),
                             "values": nulls, "repeats": SHUFFLE_REPEATS,
                             "note": ("labels shuffled within record, so each "
                                      "record keeps its own core rate")}
    return out


def shuffle_control(blocks: Dict[str, Dict[str, np.ndarray]],
                    m: CoreMembership, repeats: int = SHUFFLE_REPEATS,
                    seed: int = 0, n_boot: int = 200) -> Dict[str, object]:
    """Shuffle membership inside each record; the explanation must collapse."""
    core = m.shared_hard
    easy = m.shared_easy
    sel = core | easy
    y = core[sel].astype(int)
    groups = m.record[sel]
    joint = {f"{name}__{k}": np.asarray(v)[sel] for name, blk in blocks.items()
             for k, v in blk.items()}
    if not joint or int(y.sum()) < QA.BLOCK_MIN_EVENTS:
        return {"available": False, "reason": "underpowered or no features"}
    real = QA.block_incremental_value({}, joint, y, groups, n_boot=n_boot,
                                      mode="classification")
    rng = np.random.default_rng(seed)
    deltas = []
    for _ in range(int(repeats)):
        sh = y.copy()
        for r in np.unique(groups):
            g = groups == r
            sh[g] = rng.permutation(sh[g])
        deltas.append(float(QA.block_incremental_value(
            {}, joint, sh, groups, n_boot=n_boot,
            mode="classification")["delta_logloss"]))
    real_delta = float(real["delta_logloss"])
    mean_sh = float(np.mean(deltas))
    if real_delta <= 0:
        return {"available": True, "applicable": False,
                "real_delta": real_delta, "shuffled_mean": mean_sh,
                "retained_fraction": None, "pass": True,
                "verdict": "nothing to destroy — the features explain nothing"}
    retained = mean_sh / real_delta
    return {"available": True, "applicable": True, "real_delta": real_delta,
            "shuffled_mean": mean_sh, "shuffled_deltas": deltas,
            "retained_fraction": retained,
            "max_allowed": SHUFFLE_MAX_RETAINED,
            "pass": bool(retained <= SHUFFLE_MAX_RETAINED)}


def feature_contrast(blocks: Dict[str, Dict[str, np.ndarray]],
                     m: CoreMembership) -> List[Dict[str, object]]:
    """Descriptive, within-record standardised difference per feature.

    Reported for reading, never for deciding: the branch rule reads the
    held-out discrimination, not these.
    """
    core = m.shared_hard
    easy = m.shared_easy
    rows_out = []
    for name, blk in blocks.items():
        for feat, v in blk.items():
            v = np.asarray(v, float)
            diffs = []
            for r in np.unique(m.record):
                g = m.record == r
                a, b = v[g & core], v[g & easy]
                a, b = a[np.isfinite(a)], b[np.isfinite(b)]
                if len(a) >= 3 and len(b) >= 3:
                    sd = np.std(np.concatenate([a, b]))
                    if sd > 0:
                        diffs.append(float((np.mean(a) - np.mean(b)) / sd))
            rows_out.append({
                "block": name, "feature": feat, "n_record": len(diffs),
                "within_record_std_diff": (float(np.median(diffs)) if diffs
                                           else None),
                "records_positive": (float(np.mean(np.array(diffs) > 0))
                                     if diffs else None)})
    rows_out.sort(key=lambda d: -abs(d["within_record_std_diff"] or 0))
    return rows_out


# ─────────────────────────────────────────────────────────────────────────────
# Pre-registered decision
# ─────────────────────────────────────────────────────────────────────────────
def evaluate_core_decision(excess: Dict[str, object],
                           explain: Dict[str, object],
                           shuffle: Dict[str, object],
                           concentration: Dict[str, object]
                           ) -> Dict[str, object]:
    """D-A / D-B / D-C, applied verbatim."""
    trace: List[str] = []
    ex = float(excess.get("excess") or 0.0)
    ci_low = float(excess.get("ci_low") or 0.0)
    trace.append(f"co-hardness excess {ex:.2f}x chance "
                 f"[{ci_low:.2f}, {float(excess.get('ci_high') or 0):.2f}]")
    if not (ex >= EXCESS_MIN and ci_low > 1.0):
        return {"branch": BRANCH_NO_EXCESS, "rule": "D-C",
                "reason": ("co-hardness is at or near the chance rate — the "
                           "'shared error core' is two models overlapping by "
                           "arithmetic, not a shared object"),
                "next_step": ("retire the shared-core framing; nothing here "
                              "names an intervention"),
                "trace": trace,
                "evidence": {"excess": excess, "concentration": concentration}}

    if explain.get("underpowered"):
        trace.append("explanation underpowered")
        return {"branch": BRANCH_UNSTRUCTURED, "rule": "D-B",
                "reason": explain.get("reason", "too few beats to explain"),
                "next_step": ("the core is real but unexplained here; the "
                              "cheapest next step is a measurement that sees "
                              "the waveform, not another model"),
                "trace": trace,
                "evidence": {"excess": excess, "explain": explain}}

    joint = explain.get("joint") or {}
    auroc = float(joint.get("auroc_aug") or 0.0)
    delta = float(joint.get("delta_logloss") or 0.0)
    d_low = float(joint.get("ci_low") or 0.0)
    trace.append(f"held-out joint AUROC {auroc:.3f}, delta logloss "
                 f"{delta:+.5f} [CI low {d_low:+.5f}]")
    structured = auroc >= AUROC_MIN and d_low > 0 and bool(shuffle.get("pass"))
    trace.append(f"shuffle control pass: {shuffle.get('pass')} "
                 f"(retained {shuffle.get('retained_fraction')})")
    if not structured:
        why = []
        if auroc < AUROC_MIN:
            why.append(f"held-out AUROC {auroc:.3f} < {AUROC_MIN}")
        else:
            why.append(f"held-out AUROC is {auroc:.3f}, but ")
        if d_low <= 0:
            why.append(f"the held-out loss does not improve "
                       f"(delta {delta:+.4f}, CI low {d_low:+.4f})")
        if not shuffle.get("pass"):
            why.append("the shuffle control did not pass")
        return {"branch": BRANCH_UNSTRUCTURED, "rule": "D-B",
                "reason": ("the shared core is real (excess over chance) but "
                           "the pre-registered rule needs BOTH discrimination "
                           "and a held-out loss improvement: "
                           + "; ".join(why)),
                "next_step": ("do NOT invent a feature to fit it. The core is "
                              "invisible to everything measured so far, so the "
                              "next step is a new measurement — not a new "
                              "model, and not a wider feature search on the "
                              "same beats"),
                "trace": trace,
                "evidence": {"excess": excess, "explain": explain,
                             "shuffle": shuffle,
                             "concentration": concentration}}

    ranked = sorted(explain.get("blocks", {}).items(),
                    key=lambda kv: -kv[1]["delta_logloss"])
    winner = ranked[0][0] if ranked else None
    trace.append(f"blocks ranked: {[(k, round(v['delta_logloss'], 5)) for k, v in ranked]}")
    return {"branch": BRANCH_STRUCTURED, "rule": "D-A",
            "reason": (f"the shared core is {ex:.2f}x chance and Q5-A's "
                       f"features discriminate it out of patient (AUROC "
                       f"{auroc:.3f}); leading block {winner}"),
            "next_step": ("this NAMES a candidate factor for a later "
                          "intervention — it does not authorise one. Q5-B "
                          "still needs its own approved spec, one variable, "
                          "and negative controls"),
            "leading_block": winner, "trace": trace,
            "evidence": {"excess": excess, "explain": explain,
                         "shuffle": shuffle, "concentration": concentration}}


# ─────────────────────────────────────────────────────────────────────────────
# Driver and bundle
# ─────────────────────────────────────────────────────────────────────────────
def _dump_json(path: str, obj) -> None:
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(QA._json_safe(obj), fh, ensure_ascii=False, indent=1)


def run_core_analysis(cohort: QA.AtlasCohort, models: Dict[str, object],
                      rows: np.ndarray, out_dir: str,
                      provenance: Optional[Dict[str, object]] = None,
                      n_boot: int = NB_BOOT,
                      log: Optional[RunLog] = None) -> Dict[str, object]:
    """ANALYZE: membership -> excess -> explanation -> pre-registered branch."""
    log = log or RunLog()
    assert_analysis_only()
    os.makedirs(out_dir, exist_ok=True)
    t0 = time.time()

    m = build_membership(cohort, models, rows, log=log)
    excess = co_error_excess(m, n_boot=n_boot)
    log(f"co-hardness: record-macro {excess['observed']:.4f} "
        f"(beat-pooled {excess['observed_micro']:.4f}) vs chance "
        f"{excess['chance']:.4f} -> {excess['excess']:.2f}x "
        f"[{excess['ci_low']:.2f}, {excess['ci_high']:.2f}]")
    conc = core_concentration(m)
    log(f"concentration: counts — {conc['records_for_50pct']} record(s) hold "
        f"half the core ({conc['count_concentration']}; the largest record "
        f"holds {conc['share_of_s_in_largest']:.1%} of the S beats). "
        f"RATE — {conc['records_above_chance']}/{conc['n_record']} records "
        f"above chance, per-record excess "
        f"{conc['excess_min']:.2f}x–{conc['excess_max']:.2f}x "
        f"(uniform: {conc['rate_uniform']})")

    blocks = core_blocks(cohort, rows, m)
    explain = explain_membership(blocks, m, n_boot=n_boot, log=log)
    shuffle = (shuffle_control(blocks, m) if not explain.get("underpowered")
               else {"available": False, "reason": "underpowered"})
    contrast = feature_contrast(blocks, m)
    decision = evaluate_core_decision(excess, explain, shuffle, conc)
    log(f"branch: {decision['branch']} ({decision['rule']})")

    result = {
        "experiment_id": EXPERIMENT_ID, "arm_id": ARM_ID, "mode": "ANALYZE",
        "status": STATUS_MEASURED, "training_performed": False,
        "module_version": MODULE_VERSION, "module_build": MODULE_BUILD,
        "models": list(m.labels), "n_s_beat": m.n,
        "n_record": excess["n_record"],
        "hard_fraction": HARD_FRACTION,
        "min_s_per_record": CORE_MIN_S_PER_RECORD,
        "co_error": excess, "concentration": {k: v for k, v in conc.items()
                                              if k != "per_record"},
        "concentration_per_record": conc["per_record"],
        "explain": explain, "shuffle_control": shuffle,
        "decision": decision, "blocks_used": list(CORE_BLOCKS),
        "elapsed_s": round(time.time() - t0, 2),
    }
    prov = dict(provenance or {})
    prov.update({"experiment": f"{EXPERIMENT_ID} / {ARM_ID}",
                 "analysis_only": True, "training_performed": False,
                 "module_version": MODULE_VERSION})
    _write_bundle(out_dir, result, m, conc, contrast, excess, decision, prov,
                  log)
    return result


def _write_bundle(out_dir, result, m, conc, contrast, excess, decision, prov,
                  log) -> None:
    _dump_json(os.path.join(out_dir, "config.json"),
               {"experiment_id": EXPERIMENT_ID, "arm_id": ARM_ID,
                "mode": "ANALYZE", "analysis_only": True,
                "hard_fraction": HARD_FRACTION,
                "min_s_per_record": CORE_MIN_S_PER_RECORD,
                "blocks": list(CORE_BLOCKS), "branches": list(BRANCHES),
                "thresholds": {"excess_min": EXCESS_MIN,
                               "auroc_min": AUROC_MIN,
                               "shuffle_max_retained": SHUFFLE_MAX_RETAINED}})
    _dump_json(os.path.join(out_dir, "manifest.json"), prov)
    _dump_json(os.path.join(out_dir, "result.json"), result)
    _dump_json(os.path.join(out_dir, "decision.json"), decision)
    QA._dump_csv(os.path.join(out_dir, "core_membership.csv"),
                 conc["per_record"] or [{"record": ""}])
    QA._dump_csv(os.path.join(out_dir, "co_error_matrix.csv"),
                 [{"pair": k, **v} for k, v in excess["by_pair"].items()]
                 or [{"pair": ""}])
    QA._dump_csv(os.path.join(out_dir, "feature_contrast.csv"),
                 contrast or [{"feature": ""}])
    with open(os.path.join(out_dir, "log.txt"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(log.lines))
    _write_summary(out_dir, result, contrast)
    _write_figures(out_dir, result, conc, contrast)
    missing = [f for f in BUNDLE_FILES
               if not os.path.exists(os.path.join(out_dir, f))]
    if missing:
        raise Q5CError(f"bundle incomplete: {missing}")


def _write_summary(out_dir: str, result: Dict[str, object],
                   contrast: Sequence[Dict[str, object]]) -> None:
    ex = result["co_error"]
    d = result["decision"]
    ex_p = result.get("explain") or {}
    joint = ex_p.get("joint") or {}
    lines = [
        f"# {EXPERIMENT_ID} / {ARM_ID} — 공유 실패 핵심",
        "",
        f"- status: **{result['status']}** (ANALYSIS ONLY / NO TRAINING)",
        f"- 정의: **record 안에서** 그 record S beat를 모델별로 나쁜 절반/좋은 "
        f"절반으로 가른다 → 우연히 {len(result['models'])}개 모델 모두에서 나쁜 "
        f"절반에 들 확률 = {ex['chance']:.4f}",
        f"- 실측 공유율(record 평균) **{ex['observed']:.4f}** → 우연 대비 "
        f"**{ex['excess']:.2f}배** [{ex['ci_low']:.2f}, {ex['ci_high']:.2f}] "
        f"(환자 bootstrap) · beat 통합값 {ex['observed_micro']:.4f} "
        f"({ex['excess_micro']:.2f}배)",
        f"- 대상: S beat {result['n_s_beat']}박 · record {result['n_record']}개 "
        f"(S가 {result['min_s_per_record']}박 미만인 record는 제외)",
        f"- 집중도(**개수**): 핵심의 절반을 "
        f"{result['concentration']['records_for_50pct']}개 record가 차지 "
        f"({result['concentration']['count_concentration']}) — 가장 큰 record가 "
        f"S beat의 {result['concentration']['share_of_s_in_largest']:.1%}를 갖고 "
        "있으므로 이 줄만 읽으면 오독한다",
        f"- 집중도(**비율 — 이쪽을 읽는다**): "
        f"{result['concentration']['records_above_chance']}/"
        f"{result['concentration']['n_record']} record가 우연 초과, record별 "
        f"{result['concentration']['excess_min']:.2f}배–"
        f"{result['concentration']['excess_max']:.2f}배 "
        f"(균일: {result['concentration']['rate_uniform']})",
        f"- Q5-A 등록 특징으로 환자 밖 판별: AUROC "
        f"{joint.get('auroc_aug', 'n/a')} · Δ {joint.get('delta_logloss', 'n/a')}",
        f"- 셔플 대조군: {result['shuffle_control'].get('pass')} "
        f"(잔존 {result['shuffle_control'].get('retained_fraction')})",
        "",
        f"## 판정: **{d['branch']}** ({d['rule']})",
        "",
        f"- 근거: {d['reason']}",
        f"- 다음: {d['next_step']}",
        "",
        "## 상위 특징 대비 (서술용 — 판정은 이 표를 읽지 않는다)",
        "",
    ]
    for row in list(contrast)[:6]:
        lines.append(f"- `{row['feature']}` ({row['block']}): record 내 표준화 "
                     f"차이 {row['within_record_std_diff']} · 양수 record 비율 "
                     f"{row['records_positive']}")
    lines += [
        "",
        "- 이 결과는 `원인`이 아니라 **실패 연관 요인** 분석이다.",
        "- 43.6%(임계값 기반)는 이 실험의 대상이 아니다 — 그 정의는 Q5-A가 이미",
        "  구조적으로 강제된다고 판정했다. 여기서 세는 것은 **우연 초과분**이다.",
        "- residual CNN 경로는 closed이며 INCART rescue run도 하지 않는다.",
        "- **어떤 개입도 여기서 구현하지 않는다.**",
    ]
    with open(os.path.join(out_dir, "summary.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")


def _write_figures(out_dir: str, result: Dict[str, object],
                   conc: Dict[str, object],
                   contrast: Sequence[Dict[str, object]]) -> None:
    plt = QA._plt()
    if plt is None:                                      # pragma: no cover
        return
    figdir = QA._figdir(out_dir)
    ex = result["co_error"]

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(["chance", "observed"], [ex["chance"], ex["observed"]],
           color=["#999999", "#3b6ea5"])
    lo = max(0.0, ex["observed"] - ex["observed_ci"][0])
    hi = max(0.0, ex["observed_ci"][1] - ex["observed"])
    ax.errorbar([1], [ex["observed"]], yerr=[[lo], [hi]], fmt="none",
                ecolor="black", capsize=4)
    ax.set_ylabel(f"fraction hard in all {ex['n_model']} models")
    ax.set_title(f"shared error core: {ex['excess']:.2f}x chance")
    QA._caption(ax, f"within-record median split · {ex['n_beat']} S beats · "
                    f"{ex['n_record']} records · record-macro rate with a "
                    f"patient bootstrap (beat-pooled {ex['observed_micro']:.4f})")
    fig.tight_layout()
    fig.savefig(os.path.join(figdir, "co_error_excess.png"), dpi=110)
    plt.close(fig)

    per = conc["per_record"]
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar([str(p["record"]) for p in per], [p["core_fraction"] for p in per],
           color="#5a7d5a")
    ax.axhline(ex["chance"], color="crimson", ls="--",
               label=f"chance {ex['chance']:.3f}")
    ax.set_ylabel("share of the record's S beats in the core")
    ax.set_title("where the shared core lives")
    ax.tick_params(axis="x", labelrotation=90, labelsize=7)
    ax.legend(fontsize=7)
    QA._caption(ax, f"{conc['records_for_50pct']} record(s) hold half the core")
    fig.tight_layout()
    fig.savefig(os.path.join(figdir, "core_concentration.png"), dpi=110)
    plt.close(fig)

    top = [r for r in contrast if r["within_record_std_diff"] is not None][:12]
    fig, ax = plt.subplots(figsize=(7, max(3, 0.35 * len(top) + 1)))
    if top:
        ax.barh([r["feature"] for r in top][::-1],
                [r["within_record_std_diff"] for r in top][::-1],
                color="#8a6fa8")
    ax.axvline(0, color="black", lw=0.8)
    ax.set_xlabel("within-record standardised difference (core − easy)")
    ax.set_title("descriptive contrast — the branch does not read this")
    fig.tight_layout()
    fig.savefig(os.path.join(figdir, "feature_contrast.png"), dpi=110)
    plt.close(fig)

    d = result["decision"]
    QA._table_fig(os.path.join(figdir, "core_decision.png"),
                  f"{EXPERIMENT_ID}/{ARM_ID} — {d['branch']} ({d['rule']})",
                  [[t] for t in d["trace"]], ["pre-registered trace"],
                  caption=d["next_step"][:150])


def report_bundle(run_dir: str) -> Dict[str, object]:
    """REPORT: read a stored bundle back, recomputing nothing."""
    if not os.path.isdir(run_dir):
        return {"status": STATUS_NOT_RUN, "reason": f"no run at {run_dir}"}
    out: Dict[str, object] = {"run_dir": run_dir, "recomputed": False}
    for name in ("result.json", "decision.json", "config.json"):
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


def self_check(min_version: int = MODULE_VERSION) -> Dict[str, object]:
    if MODULE_VERSION < min_version:
        raise Q5CError(f"stale module {MODULE_VERSION} < {min_version}")
    return {"experiment_id": EXPERIMENT_ID, "arm_id": ARM_ID,
            "module_version": MODULE_VERSION, "module_build": MODULE_BUILD,
            "modes": list(MODES), "status": STATUS,
            "branches": list(BRANCHES), "blocks": list(CORE_BLOCKS),
            "analysis_only": assert_analysis_only()["q5c"],
            "q5a_module_version": QA.MODULE_VERSION,
            "thresholds": {"hard_fraction": HARD_FRACTION,
                           "excess_min": EXCESS_MIN, "auroc_min": AUROC_MIN,
                           "shuffle_max_retained": SHUFFLE_MAX_RETAINED}}


def main(argv: Optional[Sequence[str]] = None) -> int:
    import argparse
    ap = argparse.ArgumentParser(description=f"{EXPERIMENT_ID} / {ARM_ID}")
    ap.add_argument("--mode", default="DESIGN")
    ap.add_argument("--run", help="stored run dir (REPORT)")
    args = ap.parse_args(argv)
    mode = resolve_mode(args.mode)
    if mode == "DESIGN":
        print(json.dumps(self_check(), ensure_ascii=False, indent=1))
        return 0
    if mode == "REPORT":
        print(json.dumps(report_bundle(args.run or ""), ensure_ascii=False,
                         indent=1, default=str))
        return 0
    raise SystemExit("ANALYZE runs from the notebook: it needs the frozen "
                     "baselines from the Q5-A inventory")


if __name__ == "__main__":                               # pragma: no cover
    raise SystemExit(main())
