"""Tests for the Q5-D measurement qualification module.

Everything runs on synthetic fixtures — no Drive, no network, no real
waveform.  The fixtures are built so the *shape* of each failure the spec
cares about can be forced on demand: a record that misses P waves, a
delineator that fires everywhere, a join that crosses a beat, and a detector
that is no better than chance.

Run: ``python3 mit-bih/test_q5d_qualify_pwave_delineator.py``
"""

from __future__ import annotations

import hashlib
import json
import math
import os
import shutil
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import q5d_qualify_pwave_delineator as QQ                # noqa: E402

PASSED = 0
FAILED = 0
NOTEBOOK = os.path.join(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))), "notebooks",
    "quest53_q5d_qualify_pwave_delineator.ipynb")
SPEC = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    "experiments", "specs",
                    "EXP-2026-007-q5d-expert-validated-pwave-timing-audit.md")


def check(cond: bool, msg: str) -> bool:
    global PASSED, FAILED
    if cond:
        PASSED += 1
        print(f"  PASS  {msg}")
    else:
        FAILED += 1
        print(f"  FAIL  {msg}")
    return bool(cond)


# ─────────────────────────────────────────────────────────────────────────────
# Fixtures
# ─────────────────────────────────────────────────────────────────────────────
FS = 360.0
RR = 300              # samples between beats (~0.83 s)
N_BEATS = 40
PR_SAMPLES = 60       # 166.7 ms — inside the 40..300 ms window


def _r_samples(n=N_BEATS, rr=RR, start=500):
    return [start + i * rr for i in range(n)]


class FakeAnn:
    def __init__(self, sample, symbol=None):
        self.sample = list(sample)
        self.symbol = list(symbol) if symbol is not None else \
            ["N"] * len(self.sample)


class FakeHeader:
    def __init__(self, fs=FS):
        self.fs = fs
        self.n_sig = 2
        self.sig_name = ["MLII", "V1"]


class FakeRecord:
    def __init__(self, n):
        self.p_signal = [[0.0, 0.0] for _ in range(n)]


class FakeWfdb:
    """A record set with configurable beats, symbols and expert annotations."""

    def __init__(self, r_map=None, sym_map=None, expert_map=None, fs=FS,
                 sig_len=None):
        self.r_map = r_map or {}
        self.sym_map = sym_map or {}
        self.expert_map = expert_map or {}
        self.fs = fs
        self.sig_len = sig_len or (_r_samples()[-1] + RR)
        self.atr_reads = []
        self.pwave_reads = []

    def _rec(self, base):
        return os.path.basename(base)

    def rdheader(self, base):
        return FakeHeader(self.fs)

    def rdrecord(self, base, channels=None):
        return FakeRecord(self.sig_len)

    def rdann(self, base, ext):
        rec = self._rec(base)
        if ext == QQ.PWAVE_EXT:
            self.pwave_reads.append(rec)
            return FakeAnn(self.expert_map.get(rec, []),
                           ["p"] * len(self.expert_map.get(rec, [])))
        self.atr_reads.append(rec)
        rs = self.r_map.get(rec, _r_samples())
        syms = self.sym_map.get(rec, ["N"] * len(rs))
        return FakeAnn(rs, syms)


class FakeNk:
    """A delineator whose P peaks are a controllable function of the R peaks."""

    def __init__(self, offset=PR_SAMPLES, miss_every=0, extra=0, jitter=0):
        self.offset = offset
        self.miss_every = miss_every
        self.extra = extra
        self.jitter = jitter
        self.calls = 0

    def ecg_delineate(self, signal, rpeaks=None, sampling_rate=None,
                      method=None):
        self.calls += 1
        assert method == QQ.DELINEATOR_METHOD, method
        peaks = []
        for i, r in enumerate(sorted(rpeaks)):
            if self.miss_every and (i % self.miss_every == 0):
                continue
            j = (i * 7 % (2 * self.jitter + 1)) - self.jitter if self.jitter else 0
            peaks.append(int(r) - self.offset + j)
        for k in range(self.extra):
            peaks.append(int(sorted(rpeaks)[0]) - self.offset - 1000 * (k + 1))
        return None, {"ECG_P_Peaks": peaks}


def _default_maps(records, expert_offset=PR_SAMPLES, n_expert=None):
    r_map, sym_map, expert_map = {}, {}, {}
    for rec in records:
        rs = _r_samples()
        r_map[rec] = rs
        sym_map[rec] = ["N"] * len(rs)
        picks = rs if n_expert is None else rs[:n_expert]
        expert_map[rec] = [r - expert_offset for r in picks]
    return r_map, sym_map, expert_map


def _env_pin():
    return {"substage": "QUALIFY-0 ENV_PIN", "waveform_read": False,
            "packages": {"neurokit2": {"version": "0.2.13",
                                       "source_sha256": "a" * 64},
                         "wfdb": {"version": "4.3.1",
                                  "source_sha256": "b" * 64}}}


def _quiet_log():
    return QQ.RunLog(echo=False)


# ─────────────────────────────────────────────────────────────────────────────
# Guards and constants
# ─────────────────────────────────────────────────────────────────────────────
def test_guard_and_split():
    print("the module forbids outcome access and pins the record split")
    g = QQ.assert_qualify_only()
    check(g["qualify_only"] and not g["training_performed"],
          "assert_qualify_only passes on its own source")
    check(not g["ds2_outcome_opened"] and not g["model_scored"],
          "the guard states no outcome was opened and no model was scored")
    check(QQ.DS1_EXPERT_RECORDS == ("101", "106", "119", "122", "207", "223"),
          "DS1 expert records are the six pwave records inside DS1")
    check(QQ.DS2_EXPERT_RECORDS == ("100", "103", "117", "214", "222", "231"),
          "DS2 expert records are the six pwave records inside DS2")
    check(len(QQ.DS1_EXPERT_RECORDS) == 6 and len(QQ.DS2_EXPERT_RECORDS) == 6,
          "the 12 annotated records split exactly 6/6 as the spec states")
    check(not set(QQ.DS1_RECORDS) & set(QQ.DS2_RECORDS),
          "DS1 and DS2 are disjoint")
    check(set(QQ.PWAVE_RECORDS) <= set(QQ.DS1_RECORDS) | set(QQ.DS2_RECORDS),
          "every annotated record belongs to one of the two splits")
    for bad in ("ASSOCIATION", "TRAIN", "JOIN"):
        try:
            QQ.resolve_mode(bad)
            check(False, f"mode {bad} is refused")
        except QQ.Q5DQualifyError as exc:
            check("NOT authorised" in str(exc), f"mode {bad} is refused by name")
    check(QQ.resolve_mode("design") == "DESIGN", "mode names are normalised")


def test_frozen_thresholds_match_spec():
    print("the frozen numbers are the spec's numbers")
    check(QQ.MATCH_TOLERANCE_MS == 50.0, "P match tolerance is +-50 ms")
    check((QQ.P_SEARCH_MIN_MS, QQ.P_SEARCH_MAX_MS) == (40.0, 300.0),
          "P search interval is 40..300 ms")
    check(QQ.SENS_MACRO_MIN == 0.80 and QQ.PPV_MACRO_MIN == 0.80,
          "macro sensitivity and PPV floors are 0.80")
    check(QQ.PER_RECORD_MIN == 0.70 and QQ.PER_RECORD_MIN_COUNT == 5,
          "at least 5 of 6 records must reach 0.70")
    check(QQ.CHANCE_RATIO_MIN == 4.0 and QQ.CHANCE_CI_LOWER_MIN == 1.0,
          "chance ratio floor 4x with CI lower bound above 1x")
    check(QQ.PERMUTATION_SEED == 2026007 and QQ.BOOTSTRAP_SEED == 2026008,
          "the seed masters are the pre-registered ones")
    check(QQ.AAMI_N_SYMBOLS == frozenset("NLRej"),
          "AAMI N class is N/L/R/e/j")


# ─────────────────────────────────────────────────────────────────────────────
# Numeric helpers
# ─────────────────────────────────────────────────────────────────────────────
def test_numeric_helpers():
    print("percentile, MAD and the array-safe converter")
    check(abs(QQ.percentile([1, 2, 3, 4], 75) - 3.25) < 1e-9,
          "percentile matches numpy's linear interpolation")
    check(QQ.percentile([], 50) != QQ.percentile([], 50) or True,
          "an empty percentile returns nan rather than raising")
    check(math.isnan(QQ.percentile([], 50)), "empty percentile is nan")
    check(QQ.mad([1, 1, 1]) == 0.0, "MAD of a constant series is 0")
    check(QQ.mad([1, 2, 3, 4, 100]) == 1.0, "MAD ignores an outlier")

    class Ambiguous(list):
        def __bool__(self):
            raise ValueError("truth value of an array ... is ambiguous")

    check(QQ._as_list(Ambiguous([1, 2])) == [1, 2],
          "_as_list converts an array-like without testing truthiness")
    check(QQ._as_list(None) == [], "_as_list maps None to an empty list")
    try:
        import numpy as np
        check(QQ._as_list(np.array([3, 4])) == [3, 4],
              "_as_list handles a real numpy array")
    except ImportError:
        print("  (numpy unavailable — array-like fixture already covered it)")

    r1 = QQ._Rng(7)
    r2 = QQ._Rng(7)
    check([r1.next_int(1000) for _ in range(5)] ==
          [r2.next_int(1000) for _ in range(5)],
          "the seeded RNG is reproducible")


def test_percentile_matches_numpy():
    print("percentile agrees with numpy where numpy is available")
    try:
        import numpy as np
    except ImportError:
        print("  (numpy unavailable — skipped)")
        return
    vals = [0.5, 1.5, 2.25, 3.0, 7.5, 9.25, 11.0]
    for p in (0, 25, 50, 75, 90, 100):
        check(abs(QQ.percentile(vals, p) - float(np.percentile(vals, p))) < 1e-9,
              f"percentile p{p} matches numpy")


# ─────────────────────────────────────────────────────────────────────────────
# Delineation and assignment
# ─────────────────────────────────────────────────────────────────────────────
def test_p_assignment_window():
    print("a P belongs to the R it precedes inside 40..300 ms")
    rs = _r_samples(5)
    lo = int(QQ.P_SEARCH_MIN_MS * FS / 1000)     # 14 samples
    hi = int(QQ.P_SEARCH_MAX_MS * FS / 1000)     # 108 samples
    good = [r - 60 for r in rs]
    a = QQ.assign_p_to_r(good, rs, FS)
    check(len(a) == len(rs), "one P assigned per R when all are in window")
    too_close = [rs[0] - (lo - 5)]
    check(QQ.assign_p_to_r(too_close, rs, FS) == {},
          "a P closer than 40 ms to R is not assigned")
    too_far = [rs[2] - (hi + 20)]
    got = QQ.assign_p_to_r(too_far, rs, FS)
    check(rs[2] not in got, "a P farther than 300 ms from its R is not assigned")
    two = [rs[1] - 100, rs[1] - 30]
    got2 = QQ.assign_p_to_r(two, rs, FS)
    check(got2.get(rs[1]) == rs[1] - 30,
          "when two Ps fall in one window the nearest to R wins")
    check(len(got2) == 1, "the loser is not silently reassigned to another beat")


def test_pr_table_and_discordance():
    print("PR_ms and PR_discordance are label-free and record-local")
    rs = _r_samples(20)
    nk = FakeNk()
    sig = [0.0] * (rs[-1] + RR)
    t = QQ.record_pr_table("101", sig, rs, FS, nk_module=nk)
    check(t["n_valid"] == 20, "every beat gets a P from the clean fixture")
    check(abs(t["median_pr_ms"] - PR_SAMPLES * 1000.0 / FS) < 1e-6,
          "median PR is the injected offset in milliseconds")
    check(t["mad_degenerate"] and all(math.isnan(r["pr_discordance"])
                                      for r in t["rows"]),
          "a zero-MAD record yields nan discordance rather than a divide by 0")

    nk2 = FakeNk(jitter=6)
    t2 = QQ.record_pr_table("106", sig, rs, FS, nk_module=nk2)
    check(t2["mad_pr_ms"] > 0, "a jittered record has non-zero MAD")
    vals = [r["pr_discordance"] for r in t2["rows"] if r["valid"]]
    check(all(v >= 0 for v in vals), "discordance is a non-negative distance")
    check(abs(QQ.median([r["pr_ms"] for r in t2["rows"] if r["valid"]])
              - t2["median_pr_ms"]) < 1e-9,
          "the stored median is the median of the valid beats only")


def test_coupling_ratio_and_n_beats():
    print("coupling_ratio comes from .atr alone and N beats gate the RR band")
    rs = _r_samples(30)
    ratios = QQ.coupling_ratios(rs, FS)
    finite = [r for r in ratios if not math.isnan(r)]
    check(len(finite) == 29, "the first beat has no pre-RR and is dropped")
    check(all(abs(r - 1.0) < 1e-9 for r in finite),
          "a perfectly regular rhythm has coupling ratio 1.0")
    syms = ["N"] * 30
    syms[3] = "A"      # supraventricular — not AAMI N
    syms[4] = "V"
    only_n = QQ.ds1_normal_coupling(rs, syms, FS)
    check(len(only_n) == 27, "A and V beats are excluded from the RR band")
    try:
        QQ.ds1_normal_coupling(rs, [], FS)
        check(False, "N-beat selection without symbols is refused")
    except QQ.Q5DQualifyError:
        check(True, "N-beat selection without symbols is refused")


# ─────────────────────────────────────────────────────────────────────────────
# Matching, chance and bootstrap
# ─────────────────────────────────────────────────────────────────────────────
def test_match_is_one_to_one():
    print("matching is injective and respects the tolerance")
    tol = QQ.MATCH_TOLERANCE_MS * FS / 1000.0   # 18 samples
    m = QQ.match_one_to_one([100, 200, 300], [102, 205, 500], tol)
    check(m["n_matched"] == 2, "only the pairs inside +-50 ms match")
    check(sorted(m["ref_index"].keys()) == [0, 1],
          "the far reference stays unmatched")
    crowd = QQ.match_one_to_one([100, 105, 110], [104], tol)
    check(crowd["n_matched"] == 1,
          "three detections near one annotation still produce one match")
    check(crowd["matched"][0][0] == 105,
          "the nearest detection wins the single annotation")
    check(len(set(i for _d, _r, _x in [] )) == 0, "trivially injective on empty")
    big = QQ.match_one_to_one(list(range(0, 1000, 100)),
                              list(range(5, 1000, 100)), tol)
    check(big["n_matched"] == 10 and
          len(set(big["det_index"].values())) == big["n_matched"],
          "a full 1:1 match uses each annotation exactly once")


def test_cross_beat_detection():
    print("a join that crosses a beat boundary is counted, not hidden")
    rs = _r_samples(5)
    assigned = {r: r - 60 for r in rs}
    tol = QQ.MATCH_TOLERANCE_MS * FS / 1000.0
    clean = QQ.match_one_to_one(sorted(assigned.values()),
                                [r - 60 for r in rs], tol)
    check(QQ.cross_beat_violations(clean, rs, assigned) == 0,
          "an aligned join has zero cross-beat violations")
    # An expert annotation that sits just after the previous R: the detection
    # belongs to beat i, the annotation's own beat is i-1.
    shifted_ref = [rs[2] - 60, rs[1] + 5]
    bad = QQ.match_one_to_one([rs[2] - 60, rs[1] + 12], shifted_ref, tol)
    check(QQ.cross_beat_violations(bad, rs, assigned) >= 1,
          "a pair whose detection and annotation sit on different beats is flagged")


def test_chance_and_bootstrap():
    print("chance rate comes from circular shifts under the same rule")
    rs = _r_samples(30)
    det = [r - 60 for r in rs]
    ref = list(det)
    tol = QQ.MATCH_TOLERANCE_MS * FS / 1000.0
    sig_len = rs[-1] + RR
    ch = QQ.circular_shift_chance(det, ref, sig_len, tol, seed=1, n_shift=50)
    check(0.0 <= ch["chance_rate"] < 0.5,
          f"shifted detections match well below 1.0 ({ch['chance_rate']:.3f})")
    check(ch["n_shift"] == 50, "every requested shift was evaluated")
    same = QQ.circular_shift_chance(det, ref, sig_len, tol, seed=1, n_shift=50)
    check(abs(same["chance_rate"] - ch["chance_rate"]) < 1e-12,
          "the chance rate is reproducible for a fixed seed")

    rows = [{"true_rate": 0.9, "chance_rate": 0.1} for _ in range(6)]
    boot = QQ.bootstrap_ratio_ci(rows, seed=QQ.BOOTSTRAP_SEED, n_boot=500)
    check(abs(boot["ratio"] - 9.0) < 1e-9, "the point ratio is macro/macro")
    check(boot["ci_low"] > 1.0, "a strong signal keeps the CI lower bound above 1x")
    weak = QQ.bootstrap_ratio_ci(
        [{"true_rate": 0.11, "chance_rate": 0.10} for _ in range(6)],
        seed=QQ.BOOTSTRAP_SEED, n_boot=500)
    check(weak["ratio"] < QQ.CHANCE_RATIO_MIN,
          "a near-chance detector does not reach 4x")


# ─────────────────────────────────────────────────────────────────────────────
# Stage A — freeze
# ─────────────────────────────────────────────────────────────────────────────
def test_ds1_freeze_produces_constants():
    print("DS1 freeze derives the constants from 22 records and locks them")
    recs = QQ.DS1_RECORDS
    r_map, sym_map, expert_map = _default_maps(recs)
    for rec in recs:                       # give the RR band something to bite
        rs = _r_samples()
        rs = [s + (i % 3) * 12 for i, s in enumerate(rs)]
        r_map[rec] = rs
        sym_map[rec] = ["N" if i % 5 else "V" for i in range(len(rs))]
        expert_map[rec] = [r - PR_SAMPLES for r in rs]
    wf = FakeWfdb(r_map, sym_map, expert_map)
    out = QQ.run_ds1_freeze("/tmp/x", "20260810T0100", _env_pin(),
                            wfdb_module=wf, nk_module=FakeNk(jitter=5),
                            log=_quiet_log())
    fz = out["frozen"]
    check(len(out["per_record"]) == 22, "all 22 DS1 records were processed")
    check(fz["constants_scope"]["n_records"] == 22,
          "the frozen file records that the scope was 22 DS1 records")
    lo, hi = fz["rr_normal_band"]
    check(lo < hi and lo > 0, f"the RR band is a real interval ({lo:.3f},{hi:.3f})")
    check(fz["rr_band_n_normal_beats"] > 0 and fz["discordance_n_valid_beats"] > 0,
          "the constants are backed by a non-zero beat count")
    check(fz["discordance_threshold"] > 0,
          "the discordance threshold is a positive distance")
    check(fz["ds2_opened"] is False, "the freeze states DS2 was not opened")
    check(not any(r in wf.atr_reads for r in QQ.DS2_RECORDS),
          "no DS2 record was read during the freeze")
    dry = [r for r in out["per_record"] if r["expert_annotated"]]
    check(len(dry) == 6, "exactly the six DS1 expert records get a dry report")
    check(all(r["sensitivity"] > 0 for r in dry),
          "the dry report carries a sensitivity per expert record")
    QQ.verify_frozen(fz)
    check(True, "the frozen hash verifies right after the freeze")
    fz["discordance_threshold"] = 0.001
    try:
        QQ.verify_frozen(fz)
        check(False, "an edited constant is rejected")
    except QQ.Q5DQualifyError as exc:
        check("edited after the freeze" in str(exc),
              "an edited constant is rejected by hash")


def test_freeze_requires_env_pin():
    print("the freeze refuses to start without a complete environment pin")
    r_map, sym_map, expert_map = _default_maps(QQ.DS1_RECORDS)
    wf = FakeWfdb(r_map, sym_map, expert_map)
    bad = {"packages": {"neurokit2": {"version": "0.2.13"}}}
    try:
        QQ.run_ds1_freeze("/tmp/x", "20260810T0100", bad, wfdb_module=wf,
                          nk_module=FakeNk(), log=_quiet_log())
        check(False, "a pin without a neurokit source hash is refused")
    except QQ.Q5DQualifyError as exc:
        check("environment pin incomplete" in str(exc),
              "a pin without a neurokit source hash is refused")
    check(wf.atr_reads == [],
          "no waveform was read before the pin check failed")
    ok, missing = QQ.env_pin_is_complete(_env_pin())
    check(ok and not missing, "a complete pin passes the check")


def test_missing_pin_says_why():
    print("an uninstalled delineator explains itself instead of naming itself")
    # Exactly the Colab failure: neither package is installed yet, so
    # build_env_pin records the ImportError and the hash is None.
    bare = {"packages": {
        "neurokit2": {"version": None, "source_sha256": None,
                      "error": "ModuleNotFoundError: No module named "
                               "'neurokit2'"},
        "wfdb": {"version": None, "source_sha256": None,
                 "error": "ModuleNotFoundError: No module named 'wfdb'"}}}
    ok, missing = QQ.env_pin_is_complete(bare)
    check(not ok, "an uninstalled environment is refused")
    check(all("ModuleNotFoundError" in m for m in missing),
          "each missing entry carries the import error, not just the name")
    check(any(m.startswith("neurokit2:") for m in missing),
          "the entry is prefixed with the package it is about")
    silent = {"packages": {"neurokit2": {}, "wfdb": {}}}
    _, why = QQ.env_pin_is_complete(silent)
    check(all("not recorded in this pin" in m for m in why),
          "a pin that simply omits a package says so")
    real = QQ.build_env_pin("t", packages=("neurokit2",))
    entry = real["packages"]["neurokit2"]
    check("source_sha256" in entry,
          "build_env_pin always emits the key, installed or not")


def _pin_of(**pkgs):
    return {"timestamp": "20260810T0000", "packages": {
        n: {"version": v, "source_sha256": h, "py_files": f,
            "hash_algo_version": QQ.HASH_ALGO_VERSION}
        for n, (v, h, f) in pkgs.items()}}


def test_pin_drift_blocks_only_the_frozen_rule():
    print("drift stops on the delineator, is only noted for numpy/scipy")
    base = _pin_of(neurokit2=("0.2.13", "a" * 64, 313),
                   wfdb=("4.3.1", "b" * 64, 28),
                   numpy=("2.0.2", "c" * 64, 400))
    check(QQ.env_pin_drift(base, base) == [], "a pin never drifts from itself")
    moved = json.loads(json.dumps(base))
    moved["packages"]["numpy"]["source_sha256"] = "9" * 64
    d = QQ.env_pin_drift(moved, base)
    check(len(d) == 1 and d[0]["package"] == "numpy", "a numpy bump is detected")
    check(d[0]["blocking"] is False and QQ.blocking_drift(moved, base) == [],
          "a numpy bump is reported but does not stop the run")
    moved2 = json.loads(json.dumps(base))
    moved2["packages"]["neurokit2"]["source_sha256"] = "9" * 64
    check(len(QQ.blocking_drift(moved2, base)) == 1,
          "a neurokit2 source change is blocking")
    check(QQ.STRICT_PIN_PACKAGES == ("neurokit2", "wfdb"),
          "only the two version-pinned packages are strict")
    check(QQ.PIP_INSTALL_SPEC == ("neurokit2==0.2.13", "wfdb==4.3.1"),
          "the install spec pins the exact versions that were measured")
    absent = {"packages": {"neurokit2": {"source_sha256": None}}}
    check(QQ.env_pin_drift(absent, base) == [],
          "a missing hash is an incompleteness problem, not a drift problem")


def test_incomparable_hash_versions_are_refused():
    print("a baseline from another hash algorithm is refused, not called drift")
    base = _pin_of(wfdb=("4.3.1", "b" * 64, 28))
    base["packages"]["wfdb"]["hash_algo_version"] = 0     # the old walk order
    now = _pin_of(wfdb=("4.3.1", "z" * 64, 28))
    try:
        QQ.env_pin_drift(now, base)
        check(False, "an incomparable baseline raises instead of reporting drift")
    except QQ.Q5DQualifyError as exc:
        check("not comparable" in str(exc),
              "an incomparable baseline raises instead of reporting drift")
        check("Re-establish the baseline" in str(exc),
              "the error says what to do about it")


def test_hash_is_traversal_order_independent():
    print("the source hash is pinned to relative-path order, not walk order")
    tmp = tempfile.mkdtemp()
    try:
        root = os.path.join(tmp, "pkg")
        # A root-level .py that sorts *after* a subdirectory is exactly the
        # shape that made walk-order and path-order disagree.
        os.makedirs(os.path.join(root, "aaa"))
        for rel, body in (("__init__.py", "x = 1\n"),
                          ("zzz.py", "y = 2\n"),
                          ("aaa/mod.py", "z = 3\n")):
            with open(os.path.join(root, rel), "w", encoding="utf-8") as fh:
                fh.write(body)
        os.makedirs(os.path.join(root, "__pycache__"))
        with open(os.path.join(root, "__pycache__", "junk.py"), "w") as fh:
            fh.write("ignored = True\n")

        got = QQ.hash_source_tree(root)
        check(got["py_files"] == 3, "__pycache__ is excluded from the count")
        check(got["hash_algo_version"] == QQ.HASH_ALGO_VERSION,
              "the digest carries the algorithm version that made it")
        # Golden value: if this changes, HASH_ALGO_VERSION must change with it.
        expect = hashlib.sha256()
        for rel in ("__init__.py", "aaa/mod.py", "zzz.py"):
            expect.update(rel.encode())
            expect.update(open(os.path.join(root, rel), "rb").read())
        check(got["source_sha256"] == expect.hexdigest(),
              "the digest is exactly relative-path order over the .py files")

        walk = hashlib.sha256()
        for dp, dn, fn in os.walk(root):
            dn[:] = sorted(d for d in dn if d != "__pycache__")
            for f in sorted(fn):
                if f.endswith(".py"):
                    p = os.path.join(dp, f)
                    walk.update(os.path.relpath(p, root)
                                .replace(os.sep, "/").encode())
                    walk.update(open(p, "rb").read())
        check(walk.hexdigest() != got["source_sha256"],
              "walk order really does give a different digest for the same files")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_baseline_round_trip():
    print("the first run writes the baseline, later runs compare to it")
    tmp = tempfile.mkdtemp()
    try:
        pin = _pin_of(neurokit2=("0.2.13", "a" * 64, 313),
                      wfdb=("4.3.1", "b" * 64, 28))
        first = QQ.establish_or_check_baseline(tmp, pin)
        check(first["created"] and os.path.exists(first["path"]),
              "the first run creates env_pin_baseline.json")
        check(first["drift"] == [] and first["blocking"] == [],
              "a freshly created baseline reports no drift")
        again = QQ.establish_or_check_baseline(tmp, pin)
        check(not again["created"] and again["drift"] == [],
              "an unchanged environment shows no drift on the second run")
        bumped = json.loads(json.dumps(pin))
        bumped["packages"]["wfdb"]["source_sha256"] = "9" * 64
        third = QQ.establish_or_check_baseline(tmp, bumped)
        check(len(third["blocking"]) == 1
              and third["blocking"][0]["package"] == "wfdb",
              "a changed wfdb source is blocking on a later run")
        with open(first["path"], encoding="utf-8") as fh:
            stored = json.load(fh)
        check(stored["packages"]["wfdb"]["source_sha256"] == "b" * 64,
              "the baseline file is not rewritten by a drifting run")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


# ─────────────────────────────────────────────────────────────────────────────
# Stage B — the gate
# ─────────────────────────────────────────────────────────────────────────────
def _frozen_for_gate():
    fz = {"experiment_id": QQ.EXPERIMENT_ID, "substage": "QUALIFY-A DS1 FREEZE",
          "match_tolerance_ms": QQ.MATCH_TOLERANCE_MS,
          "rr_normal_band": [0.9, 1.1], "discordance_threshold": 1.5,
          "env_pin": _env_pin(), "ds2_opened": False}
    fz["frozen_sha256"] = QQ.frozen_hash(fz)
    return fz


def _gate(nk, expert_offset=PR_SAMPLES, n_expert=None, n_shift=30, n_boot=200):
    recs = QQ.DS2_EXPERT_RECORDS
    r_map, sym_map, expert_map = _default_maps(recs, expert_offset, n_expert)
    wf = FakeWfdb(r_map, sym_map, expert_map)
    out = QQ.run_ds2_gate("/tmp/x", "20260810T0200", _frozen_for_gate(),
                          wfdb_module=wf, nk_module=nk, n_shift=n_shift,
                          n_boot=n_boot, log=_quiet_log())
    out["wfdb"] = wf
    return out


def test_gate_passes_on_a_good_delineator():
    print("a delineator that finds the expert P waves qualifies")
    out = _gate(FakeNk())
    d = out["decision"]
    check(d["decision"] == QQ.DECISION_QUALIFIED,
          f"decision is MEASUREMENT_QUALIFIED ({d['n_gate_pass']}/"
          f"{d['n_gate_total']})")
    check(d["first_stopping_reason"] is None, "there is no stopping reason")
    check(abs(d["macro_sensitivity"] - 1.0) < 1e-9 and
          abs(d["macro_ppv"] - 1.0) < 1e-9,
          "a perfect fixture reaches sensitivity and PPV 1.0")
    check(d["chance_ratio"] >= QQ.CHANCE_RATIO_MIN,
          f"the detector beats chance by {d['chance_ratio']:.1f}x")
    check(all(r["cross_beat_joins"] == 0 for r in out["rows"]),
          "no record produced a cross-beat join")
    check(not d["training_performed"] and not d["ds2_outcome_opened"]
          and not d["association_performed"],
          "the decision states no training, no outcome, no association")
    check("not guarantee that every P wave is labelled" in d["limitation"],
          "the published-annotation limitation is reported")


def test_gate_never_reads_ds2_beat_classes():
    print("the DS2 gate never keeps a beat class")
    recs = QQ.DS2_EXPERT_RECORDS
    r_map, sym_map, expert_map = _default_maps(recs)
    for rec in recs:                       # plant classes that must not escape
        sym_map[rec] = ["S" if i % 4 == 0 else "N"
                        for i in range(len(r_map[rec]))]
    wf = FakeWfdb(r_map, sym_map, expert_map)
    out = QQ.run_ds2_gate("/tmp/x", "20260810T0200", _frozen_for_gate(),
                          wfdb_module=wf, nk_module=FakeNk(), n_shift=20,
                          n_boot=100, log=_quiet_log())
    blob = json.dumps({"rows": out["rows"], "decision": out["decision"]},
                      default=str)
    check("'S'" not in blob and '"S"' not in blob,
          "no DS2 beat class symbol appears anywhere in the output")
    ref = QQ.read_reference("/tmp/x", "100", keep_symbols=False, wfdb_module=wf)
    check(ref["symbols"] == [] and ref["symbols_kept"] is False,
          "read_reference drops the symbol column for a sealed record")
    check(len(ref["r_samples"]) == len(r_map["100"]),
          "dropping the class still keeps every beat's R position")
    kept = QQ.read_reference("/tmp/x", "101", keep_symbols=True, wfdb_module=wf)
    check(kept["symbols"] and kept["symbols_kept"],
          "DS1 keeps its symbols, because the RR band needs N beats")


def test_gate_fails_on_low_sensitivity():
    print("a delineator that misses P waves is refused")
    out = _gate(FakeNk(miss_every=2))
    d = out["decision"]
    check(d["decision"] == QQ.DECISION_UNQUALIFIED,
          "half the P waves missing gives MEASUREMENT_UNQUALIFIED")
    check(d["first_stopping_reason"] == "ds2_macro_sensitivity",
          "the first stopping reason names the sensitivity gate")
    check(d["macro_sensitivity"] < QQ.SENS_MACRO_MIN,
          f"macro sensitivity {d['macro_sensitivity']:.3f} is below 0.80")
    check("Do not widen the window" in d["permitted_next_step"],
          "the refusal spells out that the rule may not be relaxed")


def test_gate_fails_on_low_ppv():
    print("a delineator that fires everywhere is refused")
    out = _gate(FakeNk(extra=0), n_expert=8)
    d = out["decision"]
    check(d["decision"] == QQ.DECISION_UNQUALIFIED,
          "40 detections against 8 annotations gives UNQUALIFIED")
    check(d["macro_ppv"] < QQ.PPV_MACRO_MIN,
          f"macro PPV {d['macro_ppv']:.3f} is below 0.80")
    check(d["macro_sensitivity"] >= QQ.SENS_MACRO_MIN,
          "sensitivity alone would have passed — PPV is what fails")


def test_ppv_ceiling_is_reported_but_changes_no_gate():
    print("the structural PPV ceiling is recorded, and the gate ignores it")
    check(abs(QQ.ppv_ceiling(1500, 2022) - 0.7418) < 1e-3,
          "a sparsely annotated record has a PPV ceiling below 0.80")
    check(QQ.ppv_ceiling(2000, 1900) == 1.0,
          "more annotations than detections cannot push the ceiling above 1")
    check(math.isnan(QQ.ppv_ceiling(10, 0)), "no detections gives nan, not 0")

    # 40 detections against 8 annotations: a perfect delineator still gets 0.2.
    out = _gate(FakeNk(), n_expert=8, n_shift=20, n_boot=100)
    row = out["rows"][0]
    check(abs(row["ppv_ceiling"] - 0.2) < 1e-9,
          "the ceiling is n_expert/n_detected")
    check(abs(row["ppv_vs_ceiling"] - 1.0) < 1e-9,
          "the delineator reached 100% of the reachable PPV")
    d = out["decision"]
    check(d["decision"] == QQ.DECISION_UNQUALIFIED,
          "and the gate still fails, because the gate uses measured PPV")
    check(abs(d["macro_ppv_ceiling"] - 0.2) < 1e-9,
          "the decision records the macro ceiling as a diagnostic")
    ppv_gate = [g for g in d["gates"] if g["gate"] == "ds2_macro_ppv"][0]
    check(f"{QQ.PPV_MACRO_MIN}" in ppv_gate["detail"]
          and "ceiling" not in ppv_gate["detail"],
          "the PPV gate is still judged against the frozen 0.80, not the ceiling")
    check("ppv_ceiling" in d["limitation"]
          and "gate is evaluated on the measured PPV" in d["limitation"],
          "the limitation explains the ceiling without excusing the failure")
    check("ppv_ceiling" in QQ.DS2_COLUMNS and "ppv_ceiling" in QQ.DS1_COLUMNS,
          "both tables carry the ceiling column")


def test_gate_fails_when_only_chance():
    print("a detector no better than chance is refused")
    rows = [{"record": r, "sensitivity": 0.95, "ppv": 0.95,
             "cross_beat_joins": 0, "many_to_one_joins": 0,
             "true_rate": 0.95, "chance_rate": 0.90}
            for r in QQ.DS2_EXPERT_RECORDS]
    boot = QQ.bootstrap_ratio_ci(rows, seed=QQ.BOOTSTRAP_SEED, n_boot=300)
    d = QQ.evaluate_gate(rows, boot)
    check(d["decision"] == QQ.DECISION_UNQUALIFIED,
          "high sensitivity at chance level still fails")
    check(d["first_stopping_reason"] == "ds2_above_chance",
          "the chance gate is the one that stops it")
    check(d["chance_ratio"] < QQ.CHANCE_RATIO_MIN,
          f"the ratio {d['chance_ratio']:.2f}x is under 4x")


def test_gate_fails_on_join_integrity():
    print("a cross-beat join fails the gate on its own")
    rows = [{"record": r, "sensitivity": 0.95, "ppv": 0.95,
             "cross_beat_joins": (1 if r == "117" else 0),
             "many_to_one_joins": 0, "true_rate": 0.95, "chance_rate": 0.05}
            for r in QQ.DS2_EXPERT_RECORDS]
    boot = QQ.bootstrap_ratio_ci(rows, seed=QQ.BOOTSTRAP_SEED, n_boot=300)
    d = QQ.evaluate_gate(rows, boot)
    check(d["decision"] == QQ.DECISION_UNQUALIFIED,
          "one cross-beat join in one record fails everything")
    check(d["first_stopping_reason"] == "ds2_join_integrity",
          "the join-integrity gate names itself")


def test_gate_fails_on_per_record_floor():
    print("two weak records break the 5-of-6 floor even with a good macro")
    rows = []
    for i, r in enumerate(QQ.DS2_EXPERT_RECORDS):
        weak = i < 2
        rows.append({"record": r, "sensitivity": 0.60 if weak else 0.99,
                     "ppv": 0.60 if weak else 0.99, "cross_beat_joins": 0,
                     "many_to_one_joins": 0,
                     "true_rate": 0.60 if weak else 0.99, "chance_rate": 0.05})
    boot = QQ.bootstrap_ratio_ci(rows, seed=QQ.BOOTSTRAP_SEED, n_boot=300)
    d = QQ.evaluate_gate(rows, boot)
    check(d["decision"] == QQ.DECISION_UNQUALIFIED,
          "4 of 6 records above the floor is not enough")
    floor = [g for g in d["gates"] if g["gate"] == "ds2_per_record_floor"][0]
    check("4/6" in floor["detail"], "the gate detail states the real count")


def test_gate_requires_the_freeze():
    print("the gate refuses an edited frozen file")
    fz = _frozen_for_gate()
    fz["match_tolerance_ms"] = 120.0        # a quiet widening
    r_map, sym_map, expert_map = _default_maps(QQ.DS2_EXPERT_RECORDS)
    wf = FakeWfdb(r_map, sym_map, expert_map)
    try:
        QQ.run_ds2_gate("/tmp/x", "20260810T0200", fz, wfdb_module=wf,
                        nk_module=FakeNk(), n_shift=10, n_boot=50,
                        log=_quiet_log())
        check(False, "widening the tolerance after the freeze is refused")
    except QQ.Q5DQualifyError as exc:
        check("edited after the freeze" in str(exc),
              "widening the tolerance after the freeze is refused")
    check(wf.atr_reads == [], "no DS2 record was read before the hash check")


def test_gate_refuses_a_non_ds2_record():
    print("the gate refuses to score a record that is not in DS2")
    r_map, sym_map, expert_map = _default_maps(("101",))
    wf = FakeWfdb(r_map, sym_map, expert_map)
    try:
        QQ.run_ds2_gate("/tmp/x", "20260810T0200", _frozen_for_gate(),
                        wfdb_module=wf, nk_module=FakeNk(), records=("101",),
                        n_shift=5, n_boot=20, log=_quiet_log())
        check(False, "a DS1 record cannot be used for the DS2 gate")
    except QQ.Q5DQualifyError as exc:
        check("not a DS2 record" in str(exc),
              "a DS1 record cannot be used for the DS2 gate")


# ─────────────────────────────────────────────────────────────────────────────
# Bundle
# ─────────────────────────────────────────────────────────────────────────────
def test_bundle_round_trip():
    print("the bundle is written, archived immutably and replayed as saved")
    tmp = tempfile.mkdtemp()
    try:
        recs = QQ.DS1_RECORDS
        r_map, sym_map, expert_map = _default_maps(recs)
        for rec in recs:
            rs = [s + (i % 3) * 12 for i, s in enumerate(_r_samples())]
            r_map[rec] = rs
            sym_map[rec] = ["N"] * len(rs)
            expert_map[rec] = [r - PR_SAMPLES for r in rs]
        wf1 = FakeWfdb(r_map, sym_map, expert_map)
        log = _quiet_log()
        ds1 = QQ.run_ds1_freeze(tmp, "20260810T0100", _env_pin(),
                                wfdb_module=wf1, nk_module=FakeNk(jitter=5),
                                log=log)
        QQ.write_bundle(tmp, "20260810T0100", "QUALIFY_DS1_FREEZE",
                        ds1["frozen"], ds1, None, log)
        mid = QQ.report_bundle(tmp)
        check(mid["decision"] == QQ.DECISION_NOT_RUN,
              "after the freeze alone the bundle still reports NOT_RUN")

        out = _gate(FakeNk(), n_shift=20, n_boot=100)
        QQ.write_bundle(tmp, "20260810T0200", "QUALIFY_DS2_GATE",
                        _frozen_for_gate(), None, out, out["log"])
        rep = QQ.report_bundle(tmp)
        check(rep["decision"] == QQ.DECISION_QUALIFIED and not rep["recomputed"],
              "the stored decision replays without recomputing")
        check(rep["missing_files"] == [],
              f"the bundle is complete ({len(QQ.BUNDLE_FILES)} files)")
        check(rep["archived_runs"] == ["20260810T0100", "20260810T0200"],
              "both runs are archived under runs/<timestamp>/")
        first = os.path.join(QQ.qualify_dir(tmp), "runs", "20260810T0100",
                             "decision.json")
        with open(first, encoding="utf-8") as fh:
            archived = json.load(fh)
        check(archived["decision"] == QQ.DECISION_NOT_RUN,
              "the earlier archived run keeps its own decision, not the later one")
        check(rep["summary"].lstrip().startswith("# EXP-2026-007"),
              "the summary is replayed as saved")
        check("MEASURED" not in rep["summary"],
              "the summary never claims a scientific MEASURED verdict")
        csv = os.path.join(QQ.qualify_dir(tmp), "pwave_qualification.csv")
        with open(csv, encoding="utf-8") as fh:
            lines = fh.read().strip().split("\n")
        check(len(lines) == 7, "the qualification table has one row per DS2 record")
        check(lines[0].split(",") == list(QQ.DS2_COLUMNS),
              "the qualification table header is the declared schema")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_cards_do_not_overclaim():
    print("the printed cards state the boundary")
    card = QQ.design_card("/drive/x", "DESIGN")
    for token in ("NO TRAINING", "sealed", "NOT performed",
                  "MEASUREMENT_UNQUALIFIED"):
        check(token in card, f"the design card states '{token}'")
    check("MEASURED" not in card.replace("MEASUREMENT", ""),
          "the design card never promises a MEASURED verdict")
    out = _gate(FakeNk(), n_shift=10, n_boot=50)
    gate_card = QQ.render_gate_card(out["decision"], out["rows"])
    check("DECISION: MEASUREMENT_QUALIFIED" in gate_card,
          "the gate card leads with the decision")
    check(gate_card.count("[PASS]") == 5, "all five gates are printed")
    replay = QQ.render_gate_card(out["decision"])
    check("0/0" not in replay and "저장된 판정만" in replay,
          "a replayed card never invents a count it did not measure")


# ─────────────────────────────────────────────────────────────────────────────
# Repo contract
# ─────────────────────────────────────────────────────────────────────────────
def test_notebook_contract():
    print("notebook: default DESIGN, no later-stage path, honest outputs")
    if not check(os.path.exists(NOTEBOOK), "the qualify notebook exists"):
        return
    with open(NOTEBOOK, encoding="utf-8") as fh:
        nb = json.load(fh)
    code = ["".join(c["source"]) for c in nb["cells"]
            if c["cell_type"] == "code"]
    joined = "\n".join(code)
    check('MODE = "DESIGN"' in joined, "the default mode assignment is DESIGN")
    # The first run of this notebook died here: nothing installed the
    # delineator, so the environment pin had no hash to record.
    for spec in QQ.PIP_INSTALL_SPEC:
        check(spec in joined, f"the notebook installs the pinned '{spec}'")
    install_at = min((i for i, c in enumerate(nb["cells"])
                      if c["cell_type"] == "code"
                      and QQ.PIP_INSTALL_SPEC[0] in "".join(c["source"])),
                     default=10**6)
    pin_at = min((i for i, c in enumerate(nb["cells"])
                  if c["cell_type"] == "code"
                  and "build_env_pin" in "".join(c["source"])), default=-1)
    check(install_at < pin_at,
          f"the install cell ({install_at}) runs before the pin cell ({pin_at})")
    check("establish_or_check_baseline" in joined,
          "the notebook compares the pin against the Drive baseline")
    check('VALID_MODES = ("DESIGN", "QUALIFY_DS1_FREEZE", '
          '"QUALIFY_DS2_GATE", "QUALIFY_REPORT")' in joined,
          "the notebook allows only the four authorised modes")
    guarded = set()
    for tok in QQ.MODES:
        if f'MODE == "{tok}"' in joined:
            guarded.add(tok)
    check(guarded <= set(QQ.MODES) and guarded,
          f"every cell guard names an authorised mode ({sorted(guarded)})")
    body = joined.replace(QQ.NO_SCIENCE_BANNER, "")
    for banned in ("ASSOCIATION", "TRAIN"):
        check(banned not in body, f"no code cell mentions a {banned} path")
    for banned in QQ.FORBIDDEN_TOKENS:
        check(banned.lower() not in joined.lower(),
              f"no code cell reaches '{banned}'")
    outs = "\n".join("".join(o.get("text", []))
                     for c in nb["cells"] if c["cell_type"] == "code"
                     for o in c.get("outputs", []))
    if outs.strip():
        check("MEASURED" not in outs.replace("MEASUREMENT", ""),
              "executed outputs never claim a scientific MEASURED verdict")
    else:
        print("  (no outputs — the notebook has not been executed yet)")
    first_md = "".join(nb["cells"][0]["source"])
    for token in ("QUALIFY", "NO TRAINING", "RESULT NOT RUN",
                  "MEASUREMENT_UNQUALIFIED"):
        check(token in first_md, f"the first screen states '{token}'")


def test_spec_allows_these_files():
    print("the spec's allowed-file list covers the three qualify files")
    if not check(os.path.exists(SPEC), "the EXP-2026-007 spec exists"):
        return
    with open(SPEC, encoding="utf-8") as fh:
        spec = fh.read()
    for name in ("mit-bih/q5d_qualify_pwave_delineator.py",
                 "mit-bih/test_q5d_qualify_pwave_delineator.py",
                 "notebooks/quest53_q5d_qualify_pwave_delineator.ipynb"):
        check(name in spec, f"the spec lists '{name}' as changeable")
    check("status: approved_for_implementation" in spec,
          "the spec status is still approved_for_implementation, not MEASURED")
    for token in ("MEASUREMENT_UNQUALIFIED", "+-50 ms", "40..300 ms"):
        check(token in spec, f"the spec still pins '{token}'")


def main() -> int:
    tests = [test_guard_and_split, test_frozen_thresholds_match_spec,
             test_numeric_helpers, test_percentile_matches_numpy,
             test_p_assignment_window, test_pr_table_and_discordance,
             test_coupling_ratio_and_n_beats, test_match_is_one_to_one,
             test_cross_beat_detection, test_chance_and_bootstrap,
             test_ds1_freeze_produces_constants, test_freeze_requires_env_pin,
             test_missing_pin_says_why, test_pin_drift_blocks_only_the_frozen_rule,
             test_incomparable_hash_versions_are_refused,
             test_hash_is_traversal_order_independent, test_baseline_round_trip,
             test_gate_passes_on_a_good_delineator,
             test_gate_never_reads_ds2_beat_classes,
             test_gate_fails_on_low_sensitivity, test_gate_fails_on_low_ppv,
             test_ppv_ceiling_is_reported_but_changes_no_gate,
             test_gate_fails_when_only_chance, test_gate_fails_on_join_integrity,
             test_gate_fails_on_per_record_floor, test_gate_requires_the_freeze,
             test_gate_refuses_a_non_ds2_record, test_bundle_round_trip,
             test_cards_do_not_overclaim, test_notebook_contract,
             test_spec_allows_these_files]
    print("=" * 72)
    print(QQ.NO_SCIENCE_BANNER)
    print("=" * 72)
    for t in tests:
        t()
    print("=" * 72)
    print(f"passed {PASSED} · failed {FAILED}")
    return 1 if FAILED else 0


if __name__ == "__main__":
    raise SystemExit(main())
