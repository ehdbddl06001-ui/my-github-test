"""Tests for the Q5-D order-preserving beat identity join.

Everything runs on synthetic fixtures.  No Drive, no network, no registered
artifact, no MIT-BIH waveform, no mamba array, no V9/V10 cache, no result NPZ.
Where a real path would be needed the test asserts that the module *refuses*
to open it — the execution barrier is itself under test, because the user
approved writing this code and has not approved running it on the registered
data.

The load-bearing test is :func:`test_forced_edges_match_brute_force`: it
enumerates every maximum-cardinality monotone matching on small random
records and checks that the module's prefix/suffix DP certifies exactly the
edges common to all of them.  If that ever drifts, the join could promote an
arbitrary optimal path, which is the failure the spec is built to prevent.

Run: ``python3 mit-bih/test_q5d_order_preserving_beat_join.py``
"""

from __future__ import annotations

import json
import os
import random
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import q5d_order_preserving_beat_join as BJ              # noqa: E402

PASSED = 0
FAILED = 0
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NOTEBOOK = os.path.join(ROOT, "notebooks",
                        "quest54_q5d_order_preserving_beat_join.ipynb")
SPEC = os.path.join(ROOT, "experiments", "specs",
                    "EXP-2026-007-q5d-order-preserving-beat-join-gate.md")


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
# Helpers
# ─────────────────────────────────────────────────────────────────────────────
def seq(record, side, pre, post, split="DS1", rows=None):
    return BJ.RecordSequence(record, split, side, pre, post, rows)


def all_maximum_matchings(mamba, cache):
    """Brute force: every maximum-cardinality strictly monotone matching.

    Exponential on purpose — it is the independent oracle the fast path is
    checked against, and it only ever runs on tiny synthetic records.
    """
    edges = BJ.candidate_edges(mamba, cache)
    best_len = 0
    best: list = []

    def walk(start, last_i, last_j, chain):
        nonlocal best_len, best
        if len(chain) > best_len:
            best_len = len(chain)
            best = [tuple(chain)]
        elif len(chain) == best_len and chain:
            candidate = tuple(chain)
            if candidate not in best:
                best.append(candidate)
        for k in range(start, len(edges)):
            i, j = edges[k]
            if i > last_i and j > last_j:
                chain.append((i, j))
                walk(k + 1, i, j, chain)
                chain.pop()

    walk(0, -1, -1, [])
    if best_len == 0:
        return 0, []
    return best_len, [m for m in best if len(m) == best_len]


def random_record(rng, n, spread=3):
    """RR pairs drawn from a tiny alphabet, so ties and repeats are common."""
    pre = [300 + rng.randrange(spread) * 2 for _ in range(n)]
    post = [300 + rng.randrange(spread) * 2 for _ in range(n)]
    return pre, post


# ─────────────────────────────────────────────────────────────────────────────
# Ledger
# ─────────────────────────────────────────────────────────────────────────────
def test_ledger_matches_the_registered_numbers():
    print("44-record ledger: registered counts, starts, strata")
    report = BJ.verify_ledger()
    check(report["ok"], f"ledger verifies ({report['problems']})")
    check(report["records"] == 44, "44 records")
    check(report["equal_count_records"] == 36, "36 equal-count records")
    check(report["mismatched_records"] == 8, "8 mismatched-count records")
    check(report["total_difference"] == -31, "total difference -31")

    ledger = BJ.build_ledger()
    ds1 = {r.record: r for r in ledger["DS1"]}
    ds2 = {r.record: r for r in ledger["DS2"]}
    for record, delta in (("108", -1), ("116", -14), ("203", -2),
                          ("208", -7), ("223", -1)):
        check(ds1[record].delta == delta, f"DS1 {record} difference {delta}")
    for record, delta in (("105", -1), ("111", -1), ("222", -4)):
        check(ds2[record].delta == delta, f"DS2 {record} difference {delta}")
    check(sum(r.delta for r in ledger["DS1"].__iter__()) == -25,
          "DS1 difference sums to -25")
    check(sum(r.delta for r in ledger["DS2"]) == -6,
          "DS2 difference sums to -6")
    check(sum(r.cache_n for r in ledger["DS1"]) == 50551, "DS1 cache 50,551")
    check(sum(r.mamba_n for r in ledger["DS1"]) == 50576, "DS1 mamba 50,576")
    check(sum(r.cache_n for r in ledger["DS2"]) == 49289, "DS2 cache 49,289")
    check(sum(r.mamba_n for r in ledger["DS2"]) == 49295, "DS2 mamba 49,295")

    # Starts are cumulative sums in the frozen order, not free parameters.
    check(ds1["203"].cache_start == 27249, "DS1 203 starts at cache row 27,249")
    check(ds2["232"].cache_start == 41691, "DS2 232 starts at cache row 41,691")
    check(ds1["101"].mamba_start == 0 and ds1["106"].mamba_start == 1862,
          "mamba starts accumulate in the same frozen split order")
    check(ds1["109"].mamba_start == 1862 + 2027 + 1760,
          "a mamba start after a mismatched record uses the mamba count")
    check(ds1["108"].stratum == BJ.STRATUM_MISMATCH
          and ds1["101"].stratum == BJ.STRATUM_EQUAL,
          "strata are assigned from the registered difference")


def test_boundaries_must_come_from_the_ledger():
    print("record boundaries are arithmetic, and corruption is caught")
    observed = {s: {r: n for r, n in BJ.CACHE_LEDGER[s]} for s in BJ.SPLITS}
    check(BJ.verify_record_boundaries(observed)["ok"],
          "the registered boundaries verify")
    bad = {s: dict(observed[s]) for s in BJ.SPLITS}
    bad["DS2"]["222"] = 2478
    check(not BJ.verify_record_boundaries(bad)["ok"],
          "a single wrong boundary fails the check")
    missing = {s: dict(observed[s]) for s in BJ.SPLITS}
    missing["DS1"].pop("116")
    check(not BJ.verify_record_boundaries(missing)["ok"],
          "a missing record fails the check")
    extra = {s: dict(observed[s]) for s in BJ.SPLITS}
    extra["DS1"]["999"] = 10
    check(not BJ.verify_record_boundaries(extra)["ok"],
          "an unregistered record fails the check")


def test_rule_fingerprint_moves_with_the_rule():
    print("rule fingerprint: stable, and sensitive to every frozen constant")
    baseline = BJ.rule_fingerprint()
    check(baseline == BJ.rule_fingerprint(), "the fingerprint is stable")
    for attr, value in (("RR_TOLERANCE_SAMPLES", 2),
                        ("GATE_S_COVERAGE_MIN", 0.90),
                        ("MASTER_SEED", 1),
                        ("MIN_VALID_BEATS", 4)):
        original = getattr(BJ, attr)
        setattr(BJ, attr, value)
        moved = BJ.rule_fingerprint() != baseline
        setattr(BJ, attr, original)
        check(moved, f"changing {attr} changes the fingerprint")
    check(BJ.rule_fingerprint() == baseline, "restoring the constants restores it")


# ─────────────────────────────────────────────────────────────────────────────
# Leg 1
# ─────────────────────────────────────────────────────────────────────────────
def test_leg1_symbol_map_is_the_registered_one():
    print("Leg 1 symbol map: N/S/V only, F and Q excluded")
    for symbol in "NLRej":
        check(BJ.AAMI_SYMBOL_MAP.get(symbol) == "N", f"{symbol} maps to N")
    for symbol in "AaJS":
        check(BJ.AAMI_SYMBOL_MAP.get(symbol) == "S", f"{symbol} maps to S")
    for symbol in "VE":
        check(BJ.AAMI_SYMBOL_MAP.get(symbol) == "V", f"{symbol} maps to V")
    check("F" not in BJ.AAMI_SYMBOL_MAP and "Q" not in BJ.AAMI_SYMBOL_MAP,
          "F and Q are not in the map — the whole Q5-B-0 drop map")


def test_leg1_endpoints_are_eligible():
    print("Leg 1 RR: endpoints duplicate their neighbour and stay eligible")
    samples = [200, 500, 810, 1100, 1405, 1700]
    replayed = BJ.replay_leg1_record("101", "DS1",
                                     [(p, "N") for p in samples], 3000)
    diffs = [b - a for a, b in zip(samples, samples[1:])]
    check(replayed.n == len(samples), "every beat is kept")
    check(replayed.pre_samples[0] == diffs[0],
          "the first pre-RR duplicates the first interval")
    check(replayed.post_samples[-1] == diffs[-1],
          "the last post-RR duplicates the last interval")
    check(list(replayed.pre_samples[1:]) == diffs,
          "pre-RR is the interval that ends at the beat")
    check(list(replayed.post_samples[:-1]) == diffs,
          "post-RR is the interval that starts at the beat")
    check(all(v > 0 for v in replayed.pre_samples + replayed.post_samples),
          "no endpoint has an absent RR, so first and last beats are eligible")


def test_leg1_rules_are_deterministic():
    print("Leg 1: the three frozen rules and nothing else")
    symbols = ["N", "F", "A", "Q", "V", "N", "S", "N"]
    samples = [200 + 300 * k for k in range(len(symbols))]
    replayed = BJ.replay_leg1_record("102", "DS1", list(zip(samples, symbols)),
                                     samples[-1] + 400)
    check(replayed.n == 6, "F and Q are dropped, everything else kept")
    check([e["aami"] for e in replayed.kept] == ["N", "S", "V", "N", "S", "N"],
          "the kept classes follow the registered map")
    check(all(e["reason"] == BJ.REASON_SYMBOL for e in replayed.dropped),
          "each drop carries its exact reason")

    edge = BJ.replay_leg1_record("103", "DS1",
                                 [(149, "N")] + [(200 + 300 * k, "N")
                                                 for k in range(6)], 2200)
    kept = [e["raw_r_sample"] for e in edge.kept]
    check(149 not in kept, "a beat inside the leading 150-sample window is cut")
    check(all(BJ.WIN_BEFORE <= p < 2200 - BJ.WIN_AFTER for p in kept),
          "the boundary test uses annotation position `pos`")

    same = BJ.replay_leg1_record("102", "DS1", list(zip(samples, symbols)),
                                 samples[-1] + 400)
    check([e["raw_r_sample"] for e in same.kept] ==
          [e["raw_r_sample"] for e in replayed.kept],
          "the replay is deterministic")


def test_leg1_refuses_unsorted_annotations():
    print("Leg 1 preserves `.atr` sample order instead of re-sorting it")
    annotations = [(200, "N"), (900, "N"), (500, "N"), (1200, "N")]
    try:
        BJ.replay_leg1_record("104", "DS1", annotations, 3000)
        check(False, "out-of-order annotations must stop the replay")
    except BJ.Q5DJoinError as exc:
        check("order" in str(exc), f"refused: {str(exc)[:60]}…")


def test_leg1_audit_against_the_ledger():
    print("Leg 1 audit: exact counts pass, one beat off is JOIN_RULE_FALSIFIED")

    def build(counts):
        out = {}
        for record, n in counts.items():
            samples = [200 + 300 * k for k in range(n)]
            out[record] = BJ.replay_leg1_record(
                record, "DS1", [(p, "N") for p in samples], samples[-1] + 400)
        return out

    exact = {r.record: r.mamba_n for r in BJ.build_ledger()["DS1"]}
    report = BJ.audit_leg1_against_ledger(build(exact), "DS1")
    check(report["ok"], "an exact replay passes the ledger audit")
    check(report["replayed_total"] == 50576, "DS1 total 50,576 reproduced")
    check(report["decision"] is None, "a passing audit sets no decision")

    off = dict(exact)
    off["116"] -= 1
    bad = BJ.audit_leg1_against_ledger(build(off), "DS1")
    check(not bad["ok"], "one beat short fails")
    check(bad["decision"] == BJ.DECISION_RULE_FALSIFIED,
          "the failure is JOIN_RULE_FALSIFIED")
    check(bad["failed_leg"] == BJ.LEG1, "failed_leg is LEG1_SOURCE_REPLAY")

    absent = build(exact)
    absent.pop("203")
    missing = BJ.audit_leg1_against_ledger(absent, "DS1")
    check(not missing["ok"], "a record that was not replayed fails")


def test_leg1_audit_checks_stored_rr():
    print("Leg 1 audit compares stored RR within the declared tolerance")
    counts = {r.record: r.mamba_n for r in BJ.build_ledger()["DS1"]}
    replayed = {}
    stored = {}
    for record, n in counts.items():
        samples = [200 + 300 * k for k in range(n)]
        rec = BJ.replay_leg1_record(record, "DS1", [(p, "N") for p in samples],
                                    samples[-1] + 400)
        replayed[record] = rec
        stored[record] = {"pre": list(rec.pre_seconds),
                          "post": list(rec.post_seconds)}
    good = BJ.audit_leg1_against_ledger(replayed, "DS1", stored, BJ.UNIT_SECONDS)
    check(good["ok"], "matching stored RR passes")

    drifted = {r: {k: list(v) for k, v in stored[r].items()} for r in stored}
    drifted["205"]["pre"][7] += 5.0 / BJ.FS
    bad = BJ.audit_leg1_against_ledger(replayed, "DS1", drifted,
                                       BJ.UNIT_SECONDS)
    check(not bad["ok"] and bad["failed_leg"] == BJ.LEG1,
          "a 5-sample RR drift falsifies Leg 1")


# ─────────────────────────────────────────────────────────────────────────────
# Leg 2 — the matcher
# ─────────────────────────────────────────────────────────────────────────────
def test_candidate_edges_use_the_fixed_tolerance():
    print("candidate edges: |dpre| <= 1 and |dpost| <= 1, and nothing else")
    mamba = seq("201", "mamba", [300, 310], [320, 330])
    cache = seq("201", "cache", [301, 312], [321, 330])
    edges = BJ.candidate_edges(mamba, cache)
    check((0, 0) in edges, "a 1-sample offset on both components matches")
    check((1, 1) not in edges, "a 2-sample offset on pre-RR does not match")
    both = BJ.candidate_edges(seq("201", "mamba", [300], [320]),
                             seq("201", "cache", [301], [322]))
    check(not both, "one component inside and one outside is not a candidate")
    check(BJ.RR_TOLERANCE_SAMPLES == 1, "the tolerance is one sample, frozen")


def test_labels_never_enter_candidate_construction():
    print("beat symbols and classes do not affect the matcher")
    pre, post = [300, 311, 294], [311, 294, 294]
    rows_a = [{"aami": "N"}, {"aami": "S"}, {"aami": "V"}]
    rows_b = [{"aami": "V"}, {"aami": "N"}, {"aami": "S"}]
    left = BJ.match_record(seq("202", "mamba", pre, post, rows=rows_a),
                           seq("202", "cache", pre, post))
    right = BJ.match_record(seq("202", "mamba", pre, post, rows=rows_b),
                            seq("202", "cache", pre, post))
    check(left.certified == right.certified,
          "swapping every class label changes no certified edge")


def test_forced_edges_match_brute_force():
    print("certified == intersection of ALL maximum matchings (brute force)")
    rng = random.Random("q5d-forced-edge-oracle")
    mismatches = 0
    ambiguous_seen = 0
    partial_seen = 0
    cases = 0
    for trial in range(220):
        n = rng.randrange(2, 7)
        m = rng.randrange(2, 7)
        pre_a, post_a = random_record(rng, n)
        pre_b, post_b = random_record(rng, m)
        mamba = seq("203", "mamba", pre_a, post_a)
        cache = seq("203", "cache", pre_b, post_b)
        result = BJ.match_record(mamba, cache)
        size, matchings = all_maximum_matchings(mamba, cache)
        cases += 1
        if result.max_cardinality != size:
            mismatches += 1
            continue
        if not matchings:
            expected = set()
        else:
            expected = set(matchings[0])
            for other in matchings[1:]:
                expected &= set(other)
        if set(result.certified) != expected:
            mismatches += 1
        if result.ambiguous:
            ambiguous_seen += 1
        if len(matchings) > 1:
            partial_seen += 1
    check(mismatches == 0,
          f"{cases} random records agree with the oracle ({mismatches}差)"
          .replace("差", " mismatches"))
    check(ambiguous_seen > 0,
          f"the sample actually exercised ambiguity ({ambiguous_seen} records)")
    check(partial_seen > 0,
          f"the sample actually had multiple optima ({partial_seen} records)")


def test_certified_maps_are_monotone_and_one_to_one():
    print("certified maps are strictly monotone and one-to-one")
    rng = random.Random("q5d-monotone")
    ok = True
    for _trial in range(150):
        n, m = rng.randrange(2, 8), rng.randrange(2, 8)
        pre_a, post_a = random_record(rng, n)
        pre_b, post_b = random_record(rng, m)
        result = BJ.match_record(seq("204", "mamba", pre_a, post_a),
                                 seq("204", "cache", pre_b, post_b))
        rows = [i for i, _ in result.certified]
        cols = [j for _, j in result.certified]
        if rows != sorted(set(rows)) or cols != sorted(set(cols)):
            ok = False
        if any(i >= n or j >= m for i, j in result.certified):
            ok = False
    check(ok, "150 random records: strictly increasing, no row reused")


def test_ambiguous_stays_unmatched():
    print("AMBIGUOUS edges are reported and left unmatched")
    pre = [300] * 5
    post = [300] * 5
    result = BJ.match_record(seq("205", "mamba", pre, post),
                             seq("205", "cache", pre[:-1], post[:-1]))
    check(not result.certified, "a perfect repeat certifies nothing")
    check(result.ambiguous, "the alternatives are reported as AMBIGUOUS")
    check(result.max_cardinality == 4,
          "the maximum matching size is still reported honestly")
    _r, rows = BJ.join_record(seq("205", "mamba", pre, post),
                              seq("205", "cache", pre[:-1], post[:-1]),
                              BJ.ledger_record("DS1", "101"))
    statuses = {r["status"] for r in rows}
    check(BJ.STATUS_CERTIFIED not in statuses,
          "no ambiguous row leaks into the join map as CERTIFIED")
    check(all(r["cache_record_row"] is None or r["status"] != BJ.STATUS_CERTIFIED
              for r in rows), "ambiguous rows carry no mapping")


def test_equal_count_is_not_positional_identity():
    print("equal counts are a reporting stratum, not an identity axiom")
    samples = [200 + k for k in BJ._walk((300, 314, 291, 326, 284, 309, 295))]
    pre, post = BJ._rr_from_samples(samples)
    mamba_keep = list(range(len(pre) - 1))
    cache_keep = list(range(1, len(pre)))
    mamba = seq("206", "mamba", [pre[k] for k in mamba_keep],
                [post[k] for k in mamba_keep])
    cache = seq("206", "cache", [pre[k] for k in cache_keep],
                [post[k] for k in cache_keep])
    check(len(mamba) == len(cache), "the two sides have equal counts")
    result = BJ.match_record(mamba, cache)
    certified = dict(result.certified)
    check(certified.get(0) != 0,
          "the drop-one/add-one cancellation is not zipped by position")
    truth = {mamba_keep.index(k): cache_keep.index(k)
             for k in mamba_keep if k in cache_keep}
    check(all(truth.get(i) == j for i, j in certified.items()),
          "every certified pair is the true pair")


def test_cross_record_and_cross_split_are_refused():
    print("no mapping may cross a record or a split boundary")
    pre, post = [300] * 4, [300] * 4
    for label, other in (("record", seq("208", "cache", pre, post)),
                         ("split", seq("207", "cache", pre, post,
                                       split="DS2"))):
        try:
            BJ.match_record(seq("207", "mamba", pre, post), other)
            check(False, f"a cross-{label} match must be refused")
        except BJ.Q5DJoinError:
            check(True, f"a cross-{label} match is refused")


def test_t_is_never_a_join_key():
    print("`t` and its aliases are refused as a join key")
    for payload in ({"t": [0.0, 0.8]}, {"join_key": "t"},
                    {"join_key": "T"}, {"cumsum_pre": [0.0]},
                    {"time": [1.0]}):
        try:
            BJ.reject_t_as_join_key(payload)
            check(False, f"{sorted(payload)} must be refused")
        except BJ.Q5DJoinError:
            check(True, f"{sorted(payload)} is refused")
    BJ.reject_t_as_join_key({"join_key": "positional", "record": "100"})
    check(True, "a positional declaration is accepted")


def test_join_record_reports_every_row_once():
    print("join map: every row of both sides appears, nothing is imputed")
    samples = [200 + k for k in BJ._walk((300, 313, 292, 325, 285, 308))]
    pre, post = BJ._rr_from_samples(samples)
    keep = [0, 1, 3, 4, 5, 6]
    mamba = seq("209", "mamba", pre, post,
                rows=[{"raw_atr_ordinal": k, "raw_r_sample": samples[k]}
                      for k in range(len(pre))])
    cache = seq("209", "cache", [pre[k] for k in keep], [post[k] for k in keep])
    led = BJ.ledger_record("DS1", "101")
    result, rows = BJ.join_record(mamba, cache, led)
    certified = [r for r in rows if r["status"] == BJ.STATUS_CERTIFIED]
    check(len(rows) == len(mamba) + (len(cache) - len(certified)),
          "each mamba row once, plus every uncertified cache row")
    check(len(certified) == result.certified_count,
          "the join map's certified count equals the matcher's")
    check(all(r["raw_atr_ordinal"] is not None for r in certified),
          "certified rows carry their raw `.atr` ordinal")
    check(all(r["result_global_row"] ==
              led.cache_start + r["cache_record_row"] for r in certified),
          "the result row is the ledger start plus the record-local row")
    check(all(r["mamba_global_row"] == led.mamba_start + r["mamba_record_row"]
              for r in certified),
          "the mamba global row uses the mamba cumulative start")
    check(all(abs(r["pre_rr_difference_samples"]) <= 1
              and abs(r["post_rr_difference_samples"]) <= 1
              for r in certified),
          "certified rows record an RR difference inside the tolerance")
    unmatched = [r for r in rows if r["status"] == BJ.STATUS_UNMATCHED]
    check(all(r["drop_or_unmatched_reason"] in BJ.REASONS for r in unmatched),
          "every unmatched row carries a registered reason")
    check(all(r["failed_leg"] == BJ.LEG2 for r in unmatched),
          "unmatched rows are attributed to Leg 2")


def test_join_split_refuses_a_slice_that_is_not_the_ledger():
    print("Leg 2 cuts records from the ledger, never from the data")
    ledger = BJ.build_ledger()["DS1"]
    first = ledger[0]

    def sized(record, side, n):
        # Distinct RR values keep the candidate graph sparse; this test is
        # about the ledger check, which runs before any matching.
        return seq(record, side, [300 + (k % 97) for k in range(n)],
                   [310 + (k % 89) for k in range(n)])

    mamba = {r.record: sized(r.record, "mamba", r.mamba_n) for r in ledger}
    cache = {r.record: sized(r.record, "cache", r.cache_n) for r in ledger}

    short = dict(cache)
    short[first.record] = sized(first.record, "cache", 10)
    try:
        BJ.join_split(mamba, short, "DS1")
        check(False, "a cache slice that is not the registered n must stop")
    except BJ.Q5DJoinError as exc:
        check("ledger" in str(exc) or "registered" in str(exc),
              "the wrong-size slice is refused against the ledger")

    grown = dict(mamba)
    grown[first.record] = sized(first.record, "mamba", first.mamba_n + 1)
    try:
        BJ.join_split(grown, cache, "DS1")
        check(False, "a mamba slice that is not the registered n must stop")
    except BJ.Q5DJoinError as exc:
        check("registered" in str(exc),
              "the wrong-size mamba slice is refused too")

    absent = dict(cache)
    absent.pop(first.record)
    try:
        BJ.join_split(mamba, absent, "DS1")
        check(False, "a missing record must stop")
    except BJ.Q5DJoinError as exc:
        check(BJ.DECISION_INPUT_ABSENT in str(exc),
              "a missing record is JOIN_INPUT_ABSENT")


# ─────────────────────────────────────────────────────────────────────────────
# Units
# ─────────────────────────────────────────────────────────────────────────────
def test_unit_conversion_and_refusal():
    print("units: declared only, round-half-to-even, no fitted scale")
    check(BJ.to_samples(1.0, BJ.UNIT_SECONDS) == 360, "1 s is 360 samples")
    check(BJ.to_samples(300, BJ.UNIT_SAMPLES) == 300, "samples pass through")
    check(BJ.to_samples(0.5 / BJ.FS * 1, BJ.UNIT_SECONDS) == 0,
          "round-half-to-even sends 0.5 to 0")
    check(BJ.to_samples(1.5, BJ.UNIT_SAMPLES) == 2
          and BJ.to_samples(2.5, BJ.UNIT_SAMPLES) == 2,
          "round-half-to-even sends 1.5 to 2 and 2.5 to 2")
    for unit in ("", "ms", "milliseconds", "auto", None):
        try:
            BJ.to_samples(0.83, unit)
            check(False, f"unit {unit!r} must be refused")
        except BJ.Q5DJoinError:
            check(True, f"unit {unit!r} is refused")
    try:
        BJ.check_declared_unit(BJ.UNIT_SECONDS, [300, 310, 295])
        check(False, "a samples array declared as seconds must stop")
    except BJ.Q5DJoinError as exc:
        check("never fitted" in str(exc) or "contradicts" in str(exc),
              "the module stops instead of rescaling")
    try:
        BJ.check_declared_unit(BJ.UNIT_SAMPLES, [0.83, 0.80, 0.85])
        check(False, "a seconds array declared as samples must stop")
    except BJ.Q5DJoinError:
        check(True, "the mirror-image wrong declaration also stops")
    check(BJ.check_declared_unit(BJ.UNIT_SECONDS, [0.83, 0.80]) ==
          BJ.UNIT_SECONDS, "a correct declaration is accepted unchanged")


# ─────────────────────────────────────────────────────────────────────────────
# Negative controls, null, bootstrap
# ─────────────────────────────────────────────────────────────────────────────
def test_controls_are_registered_and_deterministic():
    print("negative controls: three registered families, reproducible")
    check(BJ.CONTROL_FAMILIES == ("wrong_record", "order_shuffle",
                                  "circular_shift"),
          "the three preregistered families")
    check(BJ.MASTER_SEED == 2026017, "master seed 2026017")
    check(BJ.BOOTSTRAP_SEED == 2026018, "bootstrap seed 2026018")
    check(BJ.N_NULL_REPLICATES == 10000 and BJ.N_BOOTSTRAP_REPLICATES == 2000,
          "10,000 null and 2,000 bootstrap replicates are registered")
    try:
        BJ.apply_control("best_of_three", {}, 0)
        check(False, "an unregistered control family must be refused")
    except BJ.Q5DJoinError:
        check(True, "an unregistered control family is refused")

    # Varied lengths, so the length bins hold more than two records each and
    # a derangement has genuine freedom.
    base = {str(100 + k): seq(str(100 + k), "mamba",
                              [300 + j for j in range(8 + k)],
                              [310 + j for j in range(8 + k)])
            for k in range(15)}
    for family in BJ.CONTROL_FAMILIES:
        first = BJ.apply_control(family, base, 3)
        second = BJ.apply_control(family, base, 3)
        same = all(first[r].pre_samples == second[r].pre_samples
                   for r in first)
        check(same, f"{family} replicate 3 is reproducible from the seed")
        varied = 0
        for replicate in range(4, 14):
            other = BJ.apply_control(family, base, replicate)
            if any(first[r].pre_samples != other[r].pre_samples
                   for r in first):
                varied += 1
        check(varied >= 8,
              f"{family} varies across replicates ({varied}/10 differ from #3)")


def test_wrong_record_control_deranges():
    print("wrong-record control: no record keeps its own partner")
    records = [(str(100 + k), 40 + k * 7) for k in range(12)]
    bins = BJ.length_quintiles(records)
    check(all(len(b) >= 2 for b in bins),
          f"bins are coarsened until derangement is possible ({[len(b) for b in bins]})")
    check(sorted(r for b in bins for r in b) == sorted(r for r, _ in records),
          "no record is dropped to make the control work")
    fixed_points = 0
    for replicate in range(40):
        mapping = BJ.derange_within_bins(bins, replicate)
        fixed_points += sum(1 for a, b in mapping.items() if a == b)
        if len(mapping) != len(records):
            fixed_points += 1000
    check(fixed_points == 0,
          "40 replicates produced no fixed point and covered every record")
    check(BJ.wrong_record_skipped(bins) == [],
          "nothing was skipped with these bins")

    # A singleton bin is skipped, never run as an identity mapping: feeding a
    # copy of TRUE into the null would contaminate the control.
    lone = [["101"]]
    check(BJ.derange_within_bins(lone, 0) == {},
          "a singleton bin contributes no mapping")
    check(BJ.wrong_record_skipped(lone) == ["101"],
          "the skipped record is reported rather than hidden")
    one_record = {"101": seq("101", "mamba", [300] * 5, [300] * 5)}
    try:
        BJ.apply_control(BJ.CONTROL_WRONG_RECORD, one_record, 0)
        check(False, "a split with one record cannot build this control")
    except BJ.Q5DJoinError as exc:
        check("identity" in str(exc),
              "the module refuses an identity 'control' explicitly")


def test_shuffle_and_shift_controls():
    print("order-shuffle keeps the multiset; circular shift is never identity")
    pre = [300, 311, 294, 322, 287, 306, 298]
    post = [311, 294, 322, 287, 306, 298, 298]
    rows = [{"aami": c} for c in "NSVNSVN"]
    original = seq("210", "mamba", pre, post, rows=rows)
    shuffled = BJ.shuffle_within_record(original, 7)
    check(sorted(zip(shuffled.pre_samples, shuffled.post_samples)) ==
          sorted(zip(pre, post)),
          "the shuffle permutes complete RR pairs, preserving the multiset")
    carried = {(r["aami"], p, q) for r, p, q in
               zip(shuffled.rows, shuffled.pre_samples, shuffled.post_samples)}
    expected = {(r["aami"], p, q) for r, p, q in zip(rows, pre, post)}
    check(carried == expected, "audit symbols travel with their RR pair")

    identity = 0
    for replicate in range(60):
        shifted = BJ.circular_shift_within_record(original, replicate)
        if shifted.pre_samples == original.pre_samples:
            identity += 1
        check_len = len(shifted) == len(original)
        if not check_len:
            break
    check(identity == 0, "60 circular shifts, none of them the identity")
    check(len(BJ.circular_shift_within_record(original, 1)) == len(original),
          "a circular shift preserves the record length")


def test_controls_rerun_the_whole_matcher():
    print("each control replicate reruns the complete Leg 2 matcher")
    # Several records, so the wrong-record control has partners to swap with.
    mamba = {}
    cache = {}
    for k, record in enumerate(("101", "106", "108", "109", "112", "114")):
        intervals = tuple(300 + ((j * 7 + k * 11) % 40) * 2
                          for j in range(9 + k))
        samples = [200 + s for s in BJ._walk(intervals)]
        pre, post = BJ._rr_from_samples(samples)
        mamba[record] = seq(record, "mamba", pre, post)
        cache[record] = seq(record, "cache", pre, post)

    true_total = sum(BJ.match_record(mamba[r], cache[r]).certified_count
                     for r in mamba)
    processed_total = sum(len(cache[r]) for r in cache)
    check(true_total == processed_total,
          "the TRUE alignment certifies every row")

    worst = 0
    for family in BJ.CONTROL_FAMILIES:
        for replicate in range(6):
            transformed = BJ.apply_control(family, mamba, replicate)
            total = sum(BJ.match_record(transformed[r], cache[r])
                        .certified_count for r in transformed)
            worst = max(worst, total)
            # Each replicate really did rebuild candidates and rematch.
            if total > processed_total:
                worst = 10 ** 6
    check(worst < true_total,
          f"every control replicate certifies fewer rows than TRUE "
          f"(best control {worst} < {true_total})")


def test_null_summary_and_reuse_guard():
    print("max-null, the finite-sample floor, and the rule-reuse guard")
    wrong = [0.10, 0.12, 0.08, 0.20]
    shuffle = [0.05, 0.30, 0.06, 0.04]
    shift = [0.40, 0.02, 0.07, 0.09]
    summary = BJ.null_summary(wrong, shuffle, shift, j_true=0.97,
                              n_processed=50551)
    check(summary["j_null_max"] == [0.40, 0.30, 0.08, 0.20],
          "J_null_max[b] is the per-replicate max over the three families")
    check(summary["replicates"] == 4, "the replicate count is reported")
    check(summary["signal_to_null"] > 0, "the signal ratio is computed")
    check(summary["rule_fingerprint"] == BJ.rule_fingerprint(),
          "the null records the rule it was generated under")
    try:
        BJ.null_summary([0.1, 0.2], [0.1], [0.1], 0.9, 100)
        check(False, "unequal family lengths must be refused")
    except BJ.Q5DJoinError:
        check(True, "unequal family lengths are refused")

    floored = BJ.null_summary([0.0] * 4, [0.0] * 4, [0.0] * 4, 0.9, 1000)
    check(abs(floored["signal_to_null"] - 0.9 * 1000) < 1e-6,
          "a zero null falls back to the 1/n floor, not to infinity")

    BJ.assert_null_matches_rule(summary)
    check(True, "a null generated under the current rule is accepted")
    relaxed = dict(summary)
    relaxed["rule_fingerprint"] = "0" * 64
    try:
        BJ.assert_null_matches_rule(relaxed)
        check(False, "a null from another rule must be refused")
    except BJ.NullReuseError as exc:
        check("regenerate" in str(exc),
              "a relaxed rule cannot inherit the primary rule's cutoff")

    original = BJ.RR_TOLERANCE_SAMPLES
    BJ.RR_TOLERANCE_SAMPLES = 2
    try:
        BJ.assert_null_matches_rule(summary)
        widened_refused = False
    except BJ.NullReuseError:
        widened_refused = True
    finally:
        BJ.RR_TOLERANCE_SAMPLES = original
    check(widened_refused,
          "widening the tolerance invalidates the stored null")


def test_bootstrap_is_reproducible():
    print("record-cluster bootstrap: records travel whole, seed reproduces")
    per_record = {str(100 + k): (90 - k, 100) for k in range(12)}
    # J_min_TRUE must be the statistic these clusters actually produce,
    # otherwise the interval is around a different quantity than the point.
    pooled = (sum(c for c, _t in per_record.values()) /
              sum(t for _c, t in per_record.values()))
    first = BJ.record_cluster_bootstrap(per_record, pooled, 0.2,
                                        replicates=200)
    second = BJ.record_cluster_bootstrap(per_record, pooled, 0.2,
                                         replicates=200)
    check(first["ci_low"] == second["ci_low"]
          and first["ci_high"] == second["ci_high"],
          "the same seed gives the same interval")
    check(first["ci_low"] <= first["point"] <= first["ci_high"],
          "the point estimate lies inside the interval")
    check(first["seed"] == BJ.BOOTSTRAP_SEED, "the registered seed is used")
    check(first["rule_fingerprint"] == BJ.rule_fingerprint(),
          "the bootstrap records its rule too")


def test_percentile_matches_numpy():
    print("the percentile helper matches numpy's default")
    try:
        import numpy
    except ImportError:                                 # pragma: no cover
        check(True, "numpy absent — the pure-python helper stands alone")
        return
    rng = random.Random("q5d-pct")
    ok = True
    for _trial in range(60):
        values = [rng.random() for _ in range(rng.randrange(1, 40))]
        for pct in (2.5, 10.0, 50.0, 95.0, 97.5, 99.0):
            if abs(BJ.percentile(values, pct) -
                   float(numpy.percentile(values, pct))) > 1e-9:
                ok = False
    check(ok, "60 random samples agree with numpy.percentile")


# ─────────────────────────────────────────────────────────────────────────────
# Coverage, gates, decision
# ─────────────────────────────────────────────────────────────────────────────
def _toy_join(certified_by_class, totals_by_class, records=("101", "106")):
    """Build join rows and class maps with a chosen coverage profile."""
    rows = []
    processed = {}
    mamba = {}
    j = 0
    for cls in BJ.AAMI_CLASSES:
        for k in range(totals_by_class[cls]):
            record = records[k % len(records)]
            local = j
            processed[(record, local)] = cls
            mamba[(record, local)] = cls
            status = (BJ.STATUS_CERTIFIED if k < certified_by_class[cls]
                      else BJ.STATUS_UNMATCHED)
            rows.append({
                "split": "DS1", "record": record,
                "raw_atr_ordinal": local, "raw_r_sample": 200 + local,
                "mamba_record_row": local, "mamba_global_row": local,
                "cache_record_row": local if status == BJ.STATUS_CERTIFIED
                else None,
                "result_global_row": local, "status": status,
                "pre_rr_difference_samples": 0,
                "post_rr_difference_samples": 0,
                "failed_leg": None if status == BJ.STATUS_CERTIFIED
                else BJ.LEG2,
                "drop_or_unmatched_reason":
                    BJ.REASON_NONE if status == BJ.STATUS_CERTIFIED
                    else BJ.REASON_NO_EDGE,
            })
            j += 1
    return rows, processed, mamba


def test_coverage_and_jmin():
    print("coverage, class balance and J_min")
    rows, processed, mamba = _toy_join({"N": 96, "S": 60, "V": 90},
                                       {"N": 100, "S": 100, "V": 100})
    report = BJ.coverage_report(rows, processed, mamba)
    check(abs(report["overall_coverage"] - 0.82) < 1e-9,
          "overall coverage is certified over processed rows")
    check(abs(report["class_coverage"]["S"] - 0.60) < 1e-9,
          "per-class coverage uses the processed class as denominator")
    check(abs(report["class_coverage_balance"] - 0.60 / 0.82) < 1e-9,
          "class_coverage_balance is min(class)/overall")
    check(abs(report["agreement_overall"] - 1.0) < 1e-9,
          "agreement is 1.0 when the carried class always agrees")
    value = BJ.j_min(rows, processed, mamba)
    check(abs(value - 0.60) < 1e-9,
          "J_min is the minimum per-class correct recall, so S cannot hide")

    # A dominant N class must not rescue a collapsed S class.
    rows2, processed2, mamba2 = _toy_join({"N": 1000, "S": 1, "V": 100},
                                          {"N": 1000, "S": 100, "V": 100})
    check(BJ.j_min(rows2, processed2, mamba2) < 0.02,
          "a perfect N class does not lift J_min when S collapses")


def test_s_share_inflation_is_source_relative():
    print("gate 12 measures inflation, not natural prevalence")
    processed = {}
    for k in range(80):
        processed[("232", k)] = "S"
    for k in range(20):
        processed[("231", k)] = "S"
    rows = []

    def add(record, local, status):
        rows.append({"split": "DS2", "record": record, "raw_atr_ordinal": local,
                     "raw_r_sample": 0, "mamba_record_row": local,
                     "mamba_global_row": local, "cache_record_row": local,
                     "result_global_row": local, "status": status,
                     "pre_rr_difference_samples": 0,
                     "post_rr_difference_samples": 0, "failed_leg": None,
                     "drop_or_unmatched_reason": BJ.REASON_NONE})

    for k in range(80):
        add("232", k, BJ.STATUS_CERTIFIED)
    for k in range(20):
        add("231", k, BJ.STATUS_CERTIFIED)
    proportional = BJ.s_share_inflation(rows, processed)
    check(abs(proportional["232"] - 1.0) < 1e-9,
          "a record keeping its exact source share has inflation 1.0 "
          "even at 80% of all S beats")

    rows = []
    for k in range(80):
        add("232", k, BJ.STATUS_CERTIFIED)
    for k in range(20):
        add("231", k, BJ.STATUS_UNMATCHED)
    concentrated = BJ.s_share_inflation(rows, processed)
    check(concentrated["232"] > 1.2,
          "dropping the other record's S beats inflates 232's share")


def test_record_232_constants_are_carried():
    print("record 232: source concentration and the parent-gate conflict")
    check(BJ.DS2_S_BEATS_TOTAL == 1837, "DS2 has 1,837 S beats")
    check(BJ.RECORD_232_S_BEATS == 1382, "record 232 supplies 1,382 of them")
    check(abs(BJ.RECORD_232_S_SHARE - 0.752) < 0.001,
          "that is 75.2%, before any join")
    check(BJ.RECORD_232_S_SHARE > BJ.PARENT_ABSOLUTE_RECORD_S_SHARE_CEILING,
          "the source share already exceeds the parent's absolute 50% ceiling")
    check(BJ.GATE_S_SHARE_INFLATION_MAX == 1.25,
          "gate 12 is a 1.25 inflation ceiling, a different quantity")
    card = BJ.design_card()
    check("does not relax" in card and "50%" in card,
          "the design card states that gate 12 does not relax the parent gate")


def test_gates_and_first_failure_wins():
    print("twelve gates, one primary decision, every number still recorded")
    good_coverage = {
        "overall_coverage": 0.97,
        "class_coverage": {"N": 0.97, "S": 0.96, "V": 0.95},
        "class_coverage_balance": 0.95,
        "record_coverage": {"101": 0.96, "106": 0.95},
        "record_coverage_balance": 0.98,
        "agreement_overall": 0.999,
        "agreement_by_class": {"N": 0.999, "S": 0.99, "V": 0.99},
    }
    null = dict(BJ.null_summary([0.05] * 10, [0.06] * 10, [0.04] * 10,
                                0.96, 50551))
    bootstrap = {"ci_low": 0.4, "ci_high": 0.6}
    led = BJ.evaluate_gates(good_coverage, {"232": 1.0}, null, bootstrap)
    decision = led.decide()
    check(decision["decision"] == BJ.DECISION_IDENTIFIABLE,
          "all gates passing gives JOIN_IDENTIFIABLE")
    check(decision["gates_passed"] == decision["gates_total"],
          f"{decision['gates_total']} gates, all passed")
    check(decision["v10_probability_opened"] is False
          and decision["training_performed"] is False,
          "the decision states that no probability was opened")

    biased = dict(good_coverage)
    biased["class_coverage"] = {"N": 0.99, "S": 0.70, "V": 0.95}
    led = BJ.evaluate_gates(biased, {"232": 1.0}, null, bootstrap)
    out = led.decide()
    check(out["decision"] == BJ.DECISION_SELECTION_BIASED,
          "a collapsed S coverage is JOIN_SELECTION_BIASED")
    check(out["first_stopping_reason"] == "4_s_coverage",
          "first-failure-wins names the S coverage gate")
    check(len(out["gates"]) == decision["gates_total"],
          "every gate is still evaluated and recorded after the first failure")
    check(any(g["passed"] for g in out["gates"]),
          "the gates that passed are recorded alongside the failure")

    low = dict(good_coverage)
    low["overall_coverage"] = 0.50
    low["class_coverage"] = {"N": 0.50, "S": 0.50, "V": 0.50}
    out = BJ.evaluate_gates(low, {"232": 1.0}, null, bootstrap).decide()
    check(out["decision"] == BJ.DECISION_UNRESOLVED,
          "too little coverage is JOIN_UNRESOLVED, a valid result")

    out = BJ.evaluate_gates(good_coverage, {"232": 1.0}, null, bootstrap,
                            leg1_ok=False).decide()
    check(out["decision"] == BJ.DECISION_RULE_FALSIFIED
          and out["failed_leg"] == BJ.LEG1,
          "a Leg 1 replay failure is JOIN_RULE_FALSIFIED / LEG1")

    out = BJ.evaluate_gates(good_coverage, {"232": 1.0}, null, bootstrap,
                            leg2_boundaries_ok=False).decide()
    check(out["decision"] == BJ.DECISION_INPUT_ABSENT,
          "an unverifiable record boundary is JOIN_INPUT_ABSENT")

    out = BJ.evaluate_gates(good_coverage, {"232": 1.40}, null,
                            bootstrap).decide()
    check(out["decision"] == BJ.DECISION_SELECTION_BIASED,
          "S-share inflation above 1.25 is JOIN_SELECTION_BIASED")

    weak = dict(null)
    weak["q99"] = 0.99
    out = BJ.evaluate_gates(good_coverage, {"232": 1.0}, weak,
                            bootstrap).decide()
    check(out["decision"] == BJ.DECISION_RULE_FALSIFIED,
          "failing to beat the max-null is JOIN_RULE_FALSIFIED")

    out = BJ.evaluate_gates(good_coverage, {"232": 1.0}, null,
                            {"ci_low": -0.01, "ci_high": 0.4}).decide()
    check(out["decision"] == BJ.DECISION_RULE_FALSIFIED,
          "a bootstrap CI touching zero is JOIN_RULE_FALSIFIED")

    out = BJ.evaluate_gates(good_coverage, {"232": 1.0}, null, bootstrap,
                            fixtures_ok=False).decide()
    check(out["decision"] == BJ.DECISION_RULE_FALSIFIED,
          "a synthetic false pair falsifies the rule before DS1 is inspected")


def test_gate_thresholds_match_the_spec():
    print("gate thresholds are the spec's, unchanged")
    for name, value in (("GATE_COVERAGE_MIN", 0.95),
                        ("GATE_S_COVERAGE_MIN", 0.95),
                        ("GATE_PER_CLASS_COVERAGE_MIN", 0.90),
                        ("GATE_CLASS_BALANCE_MIN", 0.80),
                        ("GATE_RECORD_COVERAGE_MIN", 0.80),
                        ("GATE_RECORD_BALANCE_MIN", 0.80),
                        ("GATE_AGREEMENT_OVERALL_MIN", 0.995),
                        ("GATE_AGREEMENT_PER_CLASS_MIN", 0.98),
                        ("GATE_SIGNAL_TO_NULL_MIN", 5.0),
                        ("GATE_S_SHARE_INFLATION_MAX", 1.25)):
        check(getattr(BJ, name) == value, f"{name} == {value}")


def test_all_decision_codes_exist():
    print("the five stopping codes plus the honest NOT RUN state")
    for code in ("JOIN_INPUT_ABSENT", "JOIN_RULE_FALSIFIED",
                 "JOIN_SELECTION_BIASED", "JOIN_UNRESOLVED",
                 "JOIN_IDENTIFIABLE"):
        check(code in BJ.DECISIONS, f"{code} is a registered decision")
    check(BJ.DECISION_NOT_RUN in BJ.DECISIONS,
          "JOIN_RESULT_NOT_RUN records the state this repository is in")
    ledger = BJ.DecisionLedger()
    try:
        ledger.record("x", False, decision="JOIN_LOOKS_GOOD")
        check(False, "an unregistered decision must be refused")
    except BJ.Q5DJoinError:
        check(True, "an unregistered decision is refused")


def test_stratum_report_covers_both_strata():
    print("both strata run the same matcher and are reported separately")
    results = []
    for record in ("101", "108", "116", "106"):
        led = BJ.ledger_record("DS1", record)
        results.append(BJ.MatchResult("101" if False else record, "DS1",
                                      led.mamba_n, led.cache_n, 0, (), (), (),
                                      {}))
    report = BJ.stratum_report(results)
    check(set(report) == set(BJ.STRATA), "both strata appear in the report")
    check(report[BJ.STRATUM_EQUAL]["records"] == 2,
          "101 and 106 land in the equal-count stratum")
    check(report[BJ.STRATUM_MISMATCH]["records"] == 2,
          "108 and 116 land in the mismatched stratum")


# ─────────────────────────────────────────────────────────────────────────────
# Output schema
# ─────────────────────────────────────────────────────────────────────────────
def test_join_map_schema_seals_the_probability():
    print("join map: required audit fields, and no probability column")
    for field in ("split", "record", "raw_atr_ordinal", "raw_r_sample",
                  "mamba_record_row", "mamba_global_row", "cache_record_row",
                  "result_global_row", "status", "pre_rr_difference_samples",
                  "post_rr_difference_samples", "failed_leg",
                  "drop_or_unmatched_reason"):
        check(field in BJ.JOIN_MAP_FIELDS, f"join_map carries '{field}'")
    good = {f: None for f in BJ.JOIN_MAP_FIELDS}
    good["status"] = BJ.STATUS_CERTIFIED
    good["drop_or_unmatched_reason"] = BJ.REASON_NONE
    BJ.validate_join_map_row(good)
    check(True, "a well-formed row validates")
    for banned in ("prob", "probability", "v10_prob", "score", "logit"):
        row = dict(good)
        row[banned] = 0.5
        try:
            BJ.validate_join_map_row(row)
            check(False, f"a '{banned}' column must be refused")
        except BJ.Q5DJoinError:
            check(True, f"a '{banned}' column is refused")
    short = dict(good)
    short.pop("raw_r_sample")
    try:
        BJ.validate_join_map_row(short)
        check(False, "a missing audit field must be refused")
    except BJ.Q5DJoinError:
        check(True, "a missing audit field is refused")
    bad = dict(good)
    bad["status"] = "PROBABLY_FINE"
    try:
        BJ.validate_join_map_row(bad)
        check(False, "an unknown status must be refused")
    except BJ.Q5DJoinError:
        check(True, "an unknown status is refused")


def test_bundle_contract_and_serialisers():
    print("run-bundle contract: twelve files, written from the real objects")
    for name in ("config.json", "manifest.json", "decision.json",
                 "synthetic_fixture_results.csv", "join_map.parquet",
                 "unmatched_and_ambiguous.csv", "record_class_coverage.csv",
                 "negative_control_null.npz", "null_summary.json",
                 "bootstrap.json", "log.txt", "summary.md"):
        check(name in BJ.BUNDLE_FILES, f"the bundle declares '{name}'")

    tmp = tempfile.mkdtemp(prefix="q5d-join-")
    try:
        complete, missing = BJ.bundle_is_complete(tmp)
        check(not complete and len(missing) == len(BJ.BUNDLE_FILES),
              "an empty directory is an incomplete bundle")

        outcomes = BJ.run_synthetic_fixtures()
        path = BJ.write_synthetic_fixture_results(
            outcomes, os.path.join(tmp, "synthetic_fixture_results.csv"))
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
        check("false_certified_pairs" in text,
              "the fixture CSV records false certified pairs per fixture")
        check(text.count("\n") == len(outcomes) + 1,
              f"one row per fixture ({len(outcomes)})")

        samples = [200 + k for k in BJ._walk((300, 313, 292, 325, 285))]
        pre, post = BJ._rr_from_samples(samples)
        mamba = seq("101", "mamba", pre, post,
                    rows=[{"raw_atr_ordinal": k, "raw_r_sample": samples[k]}
                          for k in range(len(pre))])
        cache = seq("101", "cache", pre[:-1], post[:-1])
        _result, rows = BJ.join_record(mamba, cache,
                                       BJ.ledger_record("DS1", "101"))
        shadow = BJ.write_join_map(rows, os.path.join(tmp, "join_map.csv"))
        with open(shadow, encoding="utf-8") as fh:
            header = fh.readline().strip()
        check(header == ",".join(BJ.JOIN_MAP_FIELDS),
              "the join map's columns are exactly the frozen schema")
        check("prob" not in header, "no probability column reaches the file")

        BJ.write_unmatched_and_ambiguous(
            rows, os.path.join(tmp, "unmatched_and_ambiguous.csv"))
        check(os.path.exists(os.path.join(tmp, "unmatched_and_ambiguous.csv")),
              "the unmatched/ambiguous CSV is written")

        config = BJ.build_config(BJ.MODE_DESIGN, "20260810T120000")
        check(config["execution_on_registered_data_approved"] is False,
              "config records that execution is NOT approved")
        check(config["rule_fingerprint"] == BJ.rule_fingerprint(),
              "config carries the rule fingerprint")
        manifest = BJ.build_manifest({}, "20260810T120000")
        check(manifest["ledger"]["ok"], "the manifest embeds a verified ledger")
        check(manifest["code"]["clean"],
              "the manifest embeds the no-outcome guard result")
        json.dumps(config)
        json.dumps(manifest)
        check(True, "config and manifest are JSON-serialisable")
    finally:
        import shutil
        shutil.rmtree(tmp, ignore_errors=True)


# ─────────────────────────────────────────────────────────────────────────────
# The approval barrier — the evidence that no registered data was opened
# ─────────────────────────────────────────────────────────────────────────────
def test_execution_barrier_blocks_registered_inputs():
    print("execution barrier: registered inputs stay shut without approval")
    check(not BJ.execution_is_approved(None), "no approval by default")
    check(not BJ.execution_is_approved("yes"),
          "a plausible-looking string is not the token")

    # A file that certainly exists: refusal must come from the barrier, not
    # from the file being missing.
    existing = os.path.abspath(__file__)
    try:
        BJ.open_registered_input(existing, None, "mamba_data")
        check(False, "an existing file must still be refused without approval")
    except BJ.ExecutionNotApprovedError as exc:
        check("separate user approval" in str(exc),
              "the refusal names the missing separate approval")

    try:
        BJ.open_registered_input(existing, "please", "mamba_data")
        check(False, "a wrong token must be refused")
    except BJ.ExecutionNotApprovedError:
        check(True, "a wrong token is refused")

    handle = BJ.open_registered_input(existing, BJ.EXECUTION_APPROVAL_TOKEN,
                                      "test file")
    handle.close()
    check(True, "the correct token opens the door (proved on this test file)")

    try:
        BJ.open_registered_input("/nonexistent/mamba_data.npz",
                                 BJ.EXECUTION_APPROVAL_TOKEN, "mamba")
        check(False, "a missing approved input must be JOIN_INPUT_ABSENT")
    except BJ.Q5DJoinError as exc:
        check(BJ.DECISION_INPUT_ABSENT in str(exc),
              "a missing input is JOIN_INPUT_ABSENT, not a low-coverage result")


def test_probability_is_sealed_in_every_stage():
    print("V10 probability values are sealed, with or without approval")
    sealed_key = BJ.RESULT_NPZ_SEALED[0]
    for approval in (None, BJ.EXECUTION_APPROVAL_TOKEN):
        for split in BJ.SPLITS:
            try:
                BJ.read_result_npz("/anything.npz", split, [sealed_key],
                                   approval, BJ.DS2_LABEL_RELEASE_TOKEN)
                check(False, "a probability read must be refused")
            except BJ.Q5DJoinError as exc:
                check("sealed" in str(exc),
                      f"{split} probability sealed (approval="
                      f"{'yes' if approval else 'no'})")
    check("prob" in BJ.RESULT_NPZ_SEALED,
          "'prob' is on the sealed list, not merely absent from the allowed one")
    check("prob" not in BJ.RESULT_NPZ_DS1_AUDIT_KEYS,
          "the readable-key list has no probability entry")


def test_ds2_labels_need_the_frozen_release():
    print("DS2 class labels stay sealed until the DS1 rule freezes")
    try:
        BJ.read_result_npz("/anything.npz", "DS2", ["y"],
                           BJ.EXECUTION_APPROVAL_TOKEN, None)
        check(False, "DS2 labels must need their own release")
    except BJ.ExecutionNotApprovedError as exc:
        check("sealed" in str(exc) and "select the join rule" in str(exc),
              "the refusal says DS2 labels may not select the rule")
    try:
        BJ.read_result_npz("/nonexistent.npz", "DS1", ["y"], None)
        check(False, "DS1 labels still need the execution approval")
    except BJ.ExecutionNotApprovedError:
        check(True, "DS1 labels need the execution approval too")


def test_modes_and_forbidden_stages():
    print("modes: offline ones are free, data ones need the approval")
    for mode in BJ.OFFLINE_MODES:
        check(mode not in BJ.MODES_NEEDING_EXECUTION_APPROVAL,
              f"{mode} opens no registered artifact")
    for mode in (BJ.MODE_LEG1, BJ.MODE_LEG2, BJ.MODE_DS1, BJ.MODE_DS2):
        check(mode in BJ.MODES_NEEDING_EXECUTION_APPROVAL,
              f"{mode} needs the separate execution approval")
    check(set(BJ.OFFLINE_MODES) | set(BJ.MODES_NEEDING_EXECUTION_APPROVAL) ==
          set(BJ.MODES), "every mode is classified exactly once")
    for stage in ("ASSOCIATION", "TRAIN", "SHAM"):
        try:
            BJ.resolve_mode(stage)
            check(False, f"{stage} must be refused")
        except BJ.Q5DJoinError as exc:
            check("NOT authorised" in str(exc), f"{stage} is refused by name")


def test_cli_refuses_data_modes_and_says_so():
    print("the CLI stops before opening anything, and reports NOT RUN")
    for mode in BJ.MODES_NEEDING_EXECUTION_APPROVAL:
        code = BJ.main(["--mode", mode])
        check(code == 2, f"--mode {mode} exits 2 without approval")
    check(BJ.main(["--mode", "DESIGN"]) == 0, "DESIGN runs freely")
    check(BJ.main(["--mode", "SYNTHETIC_FIXTURES"]) == 0,
          "SYNTHETIC_FIXTURES runs freely and passes")
    decision = BJ.not_run_decision()
    for flag in ("training_performed", "model_scored", "ds2_outcome_opened",
                 "v10_probability_opened", "association_performed",
                 "drive_mutated", "execution_on_registered_data_approved"):
        check(decision[flag] is False, f"not_run_decision records {flag}=False")
    check(decision["decision"] == BJ.DECISION_NOT_RUN,
          "the honest decision is JOIN_RESULT_NOT_RUN")


def test_module_reaches_no_outcome():
    print("textual guard: this module cannot reach a probability or a fit")
    report = BJ.assert_implementation_only()
    check(report["clean"], "no forbidden token in the join module")
    check(report["forbidden_tokens_checked"] >= 10,
          f"{report['forbidden_tokens_checked']} tokens checked")
    check(BJ.assert_implementation_only(os.path.abspath(__file__))["clean"],
          "the test file is clean too")


# ─────────────────────────────────────────────────────────────────────────────
# Fixtures, notebook and spec
# ─────────────────────────────────────────────────────────────────────────────
def test_every_fixture_passes_with_zero_false_pairs():
    print("the full synthetic fixture battery")
    outcomes = BJ.run_synthetic_fixtures()
    for outcome in outcomes:
        check(outcome.passed, f"fixture {outcome.name}: {outcome.detail}")
    total_false = sum(o.false_certified for o in outcomes)
    check(total_false == 0, f"false certified pairs across all fixtures: "
                            f"{total_false} (must be 0)")
    check(BJ.fixtures_passed(outcomes), "fixtures_passed() agrees")
    names = {o.name for o in outcomes}
    for required in ("leg1_identity_endpoint_duplication",
                     "leg1_isolated_deterministic_drop",
                     "leg1_consecutive_deterministic_drops",
                     "leg1_fq_deletion_concentration",
                     "leg1_record_under_five_valid_beats",
                     "leg2_identity", "leg2_cache_only_row_gap",
                     "leg2_mamba_only_row_gap", "leg2_consecutive_gaps",
                     "leg2_equal_count_cancellation",
                     "leg2_repeated_rr_unique_flank",
                     "leg2_perfect_repeat_stays_ambiguous",
                     "leg2_plus_minus_one_sample",
                     "leg2_two_sample_offset_rejected",
                     "units_seconds_to_samples",
                     "units_wrong_declaration_stops",
                     "ledger_record_boundary_corruption",
                     "leg2_row_order_corruption",
                     "leg2_cross_record_refused",
                     "input_t_rejected_as_join_key",
                     "leg2_no_arbitrary_optimal_path"):
        check(required in names, f"the spec's fixture '{required}' is present")


def test_notebook_contract():
    print("notebook: unexecuted, honest banner, results read from files")
    if not check(os.path.exists(NOTEBOOK), "the quest54 notebook exists"):
        return
    with open(NOTEBOOK, encoding="utf-8") as fh:
        nb = json.load(fh)
    check(nb.get("nbformat") == 4, "it is a valid nbformat 4 notebook")
    cells = nb["cells"]
    code = ["".join(c["source"]) for c in cells if c["cell_type"] == "code"]
    markdown = ["".join(c["source"]) for c in cells
                if c["cell_type"] == "markdown"]
    joined = "\n".join(code)

    outputs = sum(len(c.get("outputs", [])) for c in cells
                  if c["cell_type"] == "code")
    check(outputs == 0, "every code cell is unexecuted — no fabricated output")
    check(all(c.get("execution_count") is None for c in cells
              if c["cell_type"] == "code"),
          "no execution counts, so nothing pretends to have run")

    head = markdown[0] if markdown else ""
    check("IMPLEMENTED — FULL RESULT NOT RUN" in head,
          "the first screen says IMPLEMENTED — FULL RESULT NOT RUN")
    check("실제 실행 승인" in head or "execution approval" in head.lower(),
          "the first screen separates implementation from execution approval")
    check("결과가 없다" in head or "no actual result" in head.lower(),
          "the first screen says this notebook holds no result")

    check('MODE = "DESIGN"' in joined, "the default mode assignment is DESIGN")
    check("VALID_MODES" in joined, "the notebook restricts itself to the modes")
    for banned in ("ASSOCIATION", "TRAIN"):
        body = joined.replace(BJ.NO_EXECUTION_BANNER, "")
        check(banned not in body, f"no code cell names a {banned} path")
    for token in BJ.FORBIDDEN_TOKENS:
        check(token.lower() not in joined.lower(),
              f"no code cell reaches '{token}'")
    check(BJ.EXECUTION_APPROVAL_FLAG not in joined
          and BJ.EXECUTION_APPROVAL_TOKEN not in joined,
          "the notebook does not use the execution-approval token")

    sections = "\n".join(markdown)
    for heading in ("환경 및 승인 gate", "입력 asset/hash 확인",
                    "44-record ledger", "synthetic fixture",
                    "Leg 1 replay audit", "Leg 2 record-wise join",
                    "DS1 gate report", "DS2 frozen gate report",
                    "negative-control", "coverage", "ambiguous/unmatched",
                    "equal-count 36 vs mismatch 8", "105", "232",
                    "decision tree", "해석 요약", "Drive bundle"):
        check(heading in sections, f"the notebook has a '{heading}' section")

    # Result cells must read the bundle, not recompute numbers inline.
    check("decision.json" in joined and "null_summary.json" in joined,
          "result cells read decision.json and null_summary.json")
    check("json.load" in joined or "read_json" in joined,
          "the notebook loads its numbers from files")


def test_spec_contract():
    print("spec: approved for implementation, and its constants unchanged")
    if not check(os.path.exists(SPEC), "the join spec exists"):
        return
    with open(SPEC, encoding="utf-8") as fh:
        spec = fh.read()
    check("status: approved_for_implementation" in spec,
          "the spec status is approved_for_implementation")
    check("implementation_owner: claude" in spec,
          "the implementation owner is claude")
    for name in ("mit-bih/q5d_order_preserving_beat_join.py",
                 "mit-bih/test_q5d_order_preserving_beat_join.py",
                 "notebooks/quest54_q5d_order_preserving_beat_join.ipynb"):
        check(name in spec, f"the spec lists '{name}' as changeable")
    for token in ("JOIN_INPUT_ABSENT", "JOIN_RULE_FALSIFIED",
                  "JOIN_SELECTION_BIASED", "JOIN_UNRESOLVED",
                  "JOIN_IDENTIFIABLE", "LEG1_SOURCE_REPLAY",
                  "2026017", "2026018", "10,000", "2,000"):
        check(token in spec, f"the spec still pins '{token}'")
    for record, delta in (("108", "-1"), ("116", "-14"), ("203", "-2"),
                          ("208", "-7"), ("223", "-1"), ("105", "-1"),
                          ("111", "-1"), ("222", "-4")):
        check(f"{record} ({delta})" in spec or f"`{record}:" in spec,
              f"the spec registers record {record} ({delta})")
    check("second, explicit approval" in spec or "별도" in spec
          or "separate" in spec.lower(),
          "the spec keeps design approval and execution approval separate")
    # The spec's own file list must not have grown to cover qualification.
    check("mit-bih/q5d_qualify_*" in spec and "quest53_" in spec,
          "the qualification files are still marked do-not-touch")


def main() -> int:
    tests = [
        test_ledger_matches_the_registered_numbers,
        test_boundaries_must_come_from_the_ledger,
        test_rule_fingerprint_moves_with_the_rule,
        test_leg1_symbol_map_is_the_registered_one,
        test_leg1_endpoints_are_eligible,
        test_leg1_rules_are_deterministic,
        test_leg1_refuses_unsorted_annotations,
        test_leg1_audit_against_the_ledger,
        test_leg1_audit_checks_stored_rr,
        test_candidate_edges_use_the_fixed_tolerance,
        test_labels_never_enter_candidate_construction,
        test_forced_edges_match_brute_force,
        test_certified_maps_are_monotone_and_one_to_one,
        test_ambiguous_stays_unmatched,
        test_equal_count_is_not_positional_identity,
        test_cross_record_and_cross_split_are_refused,
        test_t_is_never_a_join_key,
        test_join_record_reports_every_row_once,
        test_join_split_refuses_a_slice_that_is_not_the_ledger,
        test_unit_conversion_and_refusal,
        test_controls_are_registered_and_deterministic,
        test_wrong_record_control_deranges,
        test_shuffle_and_shift_controls,
        test_controls_rerun_the_whole_matcher,
        test_null_summary_and_reuse_guard,
        test_bootstrap_is_reproducible,
        test_percentile_matches_numpy,
        test_coverage_and_jmin,
        test_s_share_inflation_is_source_relative,
        test_record_232_constants_are_carried,
        test_gates_and_first_failure_wins,
        test_gate_thresholds_match_the_spec,
        test_all_decision_codes_exist,
        test_stratum_report_covers_both_strata,
        test_join_map_schema_seals_the_probability,
        test_bundle_contract_and_serialisers,
        test_execution_barrier_blocks_registered_inputs,
        test_probability_is_sealed_in_every_stage,
        test_ds2_labels_need_the_frozen_release,
        test_modes_and_forbidden_stages,
        test_cli_refuses_data_modes_and_says_so,
        test_module_reaches_no_outcome,
        test_every_fixture_passes_with_zero_false_pairs,
        test_notebook_contract,
        test_spec_contract,
    ]
    print("=" * 72)
    print(BJ.NO_EXECUTION_BANNER)
    print(BJ.APPROVAL_NOTE)
    print("=" * 72)
    for test in tests:
        test()
    print("=" * 72)
    print(f"passed {PASSED} · failed {FAILED}")
    return 1 if FAILED else 0


if __name__ == "__main__":
    raise SystemExit(main())
