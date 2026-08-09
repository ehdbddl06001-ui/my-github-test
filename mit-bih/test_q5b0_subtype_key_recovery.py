#!/usr/bin/env python3
"""CPU test contract for EXP-2026-005 / Q5-B-0 (S subtype key recovery).

No GPU, no training, no Drive. Every fixture is synthetic, and the negative
fixtures matter more than the positive ones: a gate that only ever says GO is
not a gate.
"""
from __future__ import annotations

import json
import os
import shutil
import sys
import tempfile

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

_MODULES_BEFORE = set(sys.modules)

import q4o_leakage_free_residual as Q4O  # noqa: E402
import q5a_patient_failure_atlas as QA   # noqa: E402
import q5b0_subtype_key_recovery as QB   # noqa: E402

_MODULES_AFTER = set(sys.modules)

PASSED = 0
FAILED = 0


def check(cond: bool, label: str) -> None:
    global PASSED, FAILED
    if cond:
        PASSED += 1
        print(f"  PASS  {label}")
    else:
        FAILED += 1
        print(f"  FAIL  {label}")


def expect_raise(fn, label: str, exc=Exception) -> None:
    try:
        fn()
    except exc:
        check(True, label)
    else:
        check(False, label + " (no exception raised)")


def _pair(n_per: int = 60, seed: int = 5, drop: int = 0, jitter_s: float = 0.0,
          scramble: bool = False):
    """A blanked cohort plus the symbol source that describes the same beats."""
    cohort = QA.synthetic_atlas(n_per_record=n_per, seed=seed)
    source = QB.symbol_source_from_cohort(cohort, drop=drop, jitter_s=jitter_s,
                                          seed=seed + 1, scramble=scramble)
    QB.blank_symbols(cohort)
    return cohort, source, [int(r) for r in cohort.records]


def _controls(cohort, source, recs):
    return {"permutation_invariance":
            QB.permutation_invariance(cohort, source, recs),
            "shift_control": QB.shift_control(cohort, source, recs),
            "wrong_record_control":
            QB.wrong_record_control(cohort, source, recs)}


def _atlas_fixture(tmp: str, n_per: int = 120, seed: int = 5):
    """Cohort + the four frozen baselines, as Q5-A freezes them."""
    cohort = QA.synthetic_atlas(n_per_record=n_per, seed=seed)
    runs = os.path.join(tmp, "runs")
    specs = (("20260102T0000_base", "base", "V10_BASE", 2.0, 3, 0.573),
             ("20260102T0100_pwave", "pwave", "V10", 4.0, 4, 0.660),
             ("20260101T0000_kink_noctx", "kink_noctx", "V9", 1.0, 6, 0.597),
             ("20260101T0100_v8base", "v8base", "V9_BASE", 0.8, 7, 0.576))
    for dirname, arm, label, skill, mseed, prauc in specs:
        model = QA.synthetic_model(cohort, label, skill=skill, seed=mseed)
        QA.write_synthetic_run(os.path.join(runs, dirname), arm, cohort, model,
                               s_prauc=prauc)
    inv = QA.scan_inventory([runs], log=Q4O.RunLog(echo=False))
    freeze = QA.freeze_baseline(inv)
    models = {lab: QA.load_model_predictions(sel["run_dir"], lab,
                                             log=Q4O.RunLog(echo=False))
              for lab, sel in freeze["selected"].items()}
    return cohort, inv, freeze, models


def _dir_fingerprint(path: str) -> dict:
    out = {}
    for root, _d, files in os.walk(path):
        for f in sorted(files):
            p = os.path.join(root, f)
            out[os.path.relpath(p, path)] = (os.path.getsize(p),
                                             QA.sha256_file(p))
    return out


# ─────────────────────────────────────────────────────────────────────────────
def test_import_is_inert():
    print("import does not train, download or mount")
    new = _MODULES_AFTER - _MODULES_BEFORE
    banned = {"torch", "tensorflow", "keras", "google.colab"}
    check(not (banned & {m.split(".")[0] for m in new}),
          "no training or Colab module imported")
    check(QB.assert_analysis_only()["q5b0"]["analysis_only"],
          "the module contains no training call")
    check(QB.EXPERIMENT_ID == "EXP-2026-005" and QB.ARM_ID == "Q5-B-0",
          "identity is EXP-2026-005 / Q5-B-0")
    check(QB.self_check()["q5a_module_version"] >= 8,
          "runs against the accepted Q5-A module (v8+)")


def test_modes():
    print("mode handling")
    for m in QB.MODES:
        check(QB.resolve_mode(m.lower()) == m, f"mode {m} resolves")
    expect_raise(lambda: QB.resolve_mode("TRAIN"),
                 "an unknown mode is refused", QB.Q5B0Error)
    check(QB.run_dir_name("20260810T0000").startswith(
        "20260810T0000_EXP-2026-005_"), "run dir carries the experiment id")


def test_symbol_source_loader():
    print("symbol source loader")
    tmp = tempfile.mkdtemp(prefix="q5b0_src_")
    try:
        cohort, source, _ = _pair(n_per=40)
        good = QB.write_symbol_npz(os.path.join(tmp, "multi.npz"), source)
        loaded = QB.load_symbol_source(good, log=Q4O.RunLog(echo=False))
        check(loaded.n == source.n and set(loaded.records.tolist())
              == set(source.records.tolist()),
              "the MIT subset loads with its records intact")
        check(loaded.sha256 and loaded.sha256 != "synthetic",
              "the loaded source is fingerprinted")

        nosym = os.path.join(tmp, "nosym.npz")
        np.savez_compressed(nosym, pid=source.record, y5=source.y5,
                            pre_rr=source.pre_rr, post_rr=source.post_rr)
        expect_raise(lambda: QB.load_symbol_source(nosym,
                                                   log=Q4O.RunLog(echo=False)),
                     "a file without a symbol key is refused", QB.Q5B0Error)

        norr = os.path.join(tmp, "norr.npz")
        np.savez_compressed(norr, pid=source.record, y5=source.y5,
                            sym=source.sym)
        expect_raise(lambda: QB.load_symbol_source(norr,
                                                   log=Q4O.RunLog(echo=False)),
                     "a file without RR is refused", QB.Q5B0Error)

        badlab = os.path.join(tmp, "badlab.npz")
        np.savez_compressed(badlab, pid=source.record,
                            y5=np.full(source.n, 9), sym=source.sym,
                            pre_rr=source.pre_rr, post_rr=source.post_rr)
        expect_raise(lambda: QB.load_symbol_source(badlab,
                                                   log=Q4O.RunLog(echo=False)),
                     "labels outside the AAMI 5-class range are refused",
                     QB.Q5B0Error)
        expect_raise(lambda: QB.load_symbol_source(os.path.join(tmp, "no.npz")),
                     "a missing file is refused", QB.Q5B0Error)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_rr_unit_is_verified():
    print("RR unit verification")
    sec = QB.rr_seconds_scale(np.full(50, 0.8))
    check(sec["unit"] == "seconds" and sec["scale_to_seconds"] == 1.0,
          "a seconds column is recognised")
    smp = QB.rr_seconds_scale(np.full(50, 288.0))
    check(smp["unit"] == "samples"
          and abs(smp["scale_to_seconds"] - 1 / 360.0) < 1e-9,
          "a samples column is recognised and rescaled")
    expect_raise(lambda: QB.rr_seconds_scale(np.full(50, 1e6)),
                 "a column that fits neither unit is refused", QB.Q5B0Error)
    expect_raise(lambda: QB.rr_seconds_scale(np.zeros(0)),
                 "an empty RR column is refused", QB.Q5B0Error)


def test_fingerprint_is_order_free():
    print("the join key is a property of the beat, not of the row")
    pre = np.array([0.4, 0.9, 0.6, 1.1])
    post = np.array([1.2, 0.8, 1.0, 0.7])
    fp = QB.rr_fingerprint(pre, post)
    perm = np.array([2, 0, 3, 1])
    fp_perm = QB.rr_fingerprint(pre[perm], post[perm])
    check(np.array_equal(fp[perm], fp_perm),
          "permuting the rows permutes the key and nothing else")
    check(fp.shape[1] == len(QB.FINGERPRINT_FIELDS) == 2,
          "the key has exactly the declared coordinates")
    check("prev" not in "".join(QB.FINGERPRINT_FIELDS)
          and "next" not in "".join(QB.FINGERPRINT_FIELDS),
          "no neighbour coordinate sneaks row order into the key")


def test_assignment_rules():
    print("assignment: tolerance, margin, one-to-one")
    cost = np.array([[0.001, 0.500], [0.400, 0.002]])
    res = QB.assign_one_to_one(cost, tolerance=0.005, margin=0.005)
    check(res["n_matched"] == 2 and list(res["match"]) == [0, 1],
          "two clean pairs match")

    far = np.array([[0.100, 0.200], [0.300, 0.400]])
    res = QB.assign_one_to_one(far, tolerance=0.005, margin=0.005)
    check(res["n_matched"] == 0 and res["n_over_tolerance"] == 2,
          "pairs outside the tolerance are refused, not stretched")

    tie = np.array([[0.001, 0.002], [0.400, 0.500]])
    res = QB.assign_one_to_one(tie, tolerance=0.005, margin=0.005)
    check(res["match"][0] == -1 and res["n_ambiguous"] >= 1,
          "a beat with two equally good candidates stays UNMATCHED")

    both = np.array([[0.001, 0.400], [0.002, 0.500]])
    res = QB.assign_one_to_one(both, tolerance=0.005, margin=0.005)
    check(len(set(int(j) for j in res["match"] if j >= 0))
          == int((res["match"] >= 0).sum()),
          "no source beat is handed to two cohort beats")


def test_recovery_on_a_faithful_source():
    print("recovery on a source describing the same beats")
    cohort, source, recs = _pair(n_per=60, drop=2)
    rec = QB.recover_symbols(cohort, source, recs, log=Q4O.RunLog(echo=False))
    check(rec["match_fraction"] >= QB.MIN_S_MATCH_FRACTION,
          f"S beats join ({rec['match_fraction']:.1%})")
    check(rec["symbol_in_s_set_fraction"] >= QB.MIN_SYMBOL_IN_S_SET,
          "recovered symbols land in the AAMI S set")
    check(sum(rec["subtype_counts"].values()) == rec["n_matched"],
          "every matched beat is counted in exactly one subtype")
    gate = QB.evaluate_recovery_gate(rec, _controls(cohort, source, recs))
    check(gate["gate"] == QB.GATE_GO, f"gate GO ({gate['fail_reasons']})")


def test_gate_refuses_an_unrelated_source():
    print("negative fixture: a source describing a different recording")
    cohort, source, recs = _pair(n_per=60, scramble=True)
    rec = QB.recover_symbols(cohort, source, recs, log=Q4O.RunLog(echo=False))
    gate = QB.evaluate_recovery_gate(rec, _controls(cohort, source, recs))
    check(gate["gate"] == QB.GATE_NOGO, "gate NO-GO on an unrelated source")
    check(any("match_fraction" in r for r in gate["fail_reasons"]),
          "the failure names the match rate")
    check("closed" in gate["next_step"] and "retrain" in gate["next_step"],
          "NO-GO says B_SUBTYPE closes and retraining is not the answer")


def test_symbols_never_drive_the_match():
    print("the matcher never sees a symbol")
    cohort, source, recs = _pair(n_per=60)
    a = QB.recover_symbols(cohort, source, recs, log=Q4O.RunLog(echo=False))
    relabelled = QB.SymbolSource(
        record=source.record, sym=np.full(source.n, "A", dtype="<U2"),
        y5=source.y5, pre_rr=source.pre_rr, post_rr=source.post_rr,
        records=source.records)
    relabelled.idx_of = dict(source.idx_of)
    b = QB.recover_symbols(cohort, relabelled, recs, log=Q4O.RunLog(echo=False))
    check(np.array_equal(a["sym"] != "?", b["sym"] != "?"),
          "rewriting every symbol changes nothing about WHICH rows matched")
    check(a["n_matched"] == b["n_matched"],
          "the match count is identical under relabelling")


def test_controls_can_fail():
    print("controls are falsifiable")
    cohort, source, recs = _pair(n_per=60)
    perm = QB.permutation_invariance(cohort, source, recs)
    check(perm["identical"] and perm["n_differing"] == 0,
          "content anchors survive a shuffled pool untouched")
    check(perm["scope"] == "content anchors" and "ordinal" in perm["note"],
          "the invariance claim is scoped to the anchors, not to the fill")

    shift = QB.shift_control(cohort, source, recs)
    check(shift["match_fraction"] <= QB.MAX_SHIFT_CONTROL,
          "an off-by-one pairing does not fit the tolerance")
    wrong = QB.wrong_record_control(cohort, source, recs)
    check(wrong["match_fraction"] <= QB.MAX_WRONG_RECORD,
          "another record's pool does not match")

    # A source whose beats are indistinguishable: every RR identical. The join
    # must not celebrate; the shift control is what catches it.
    flat = QB.SymbolSource(
        record=source.record, sym=source.sym, y5=source.y5,
        pre_rr=np.full(source.n, 0.8), post_rr=np.full(source.n, 0.8),
        records=source.records)
    flat.idx_of = dict(source.idx_of)
    flat_cohort = QA.synthetic_atlas(n_per_record=60, seed=5)
    flat_cohort.pre_rr = np.full(flat_cohort.n, 0.8)
    flat_cohort.post_rr = np.full(flat_cohort.n, 0.8)
    QB.blank_symbols(flat_cohort)
    sh = QB.shift_control(flat_cohort, flat, recs)
    check(sh["match_fraction"] > QB.MAX_SHIFT_CONTROL,
          "indistinguishable beats FAIL the shift control")
    rec = QB.recover_symbols(flat_cohort, flat, recs,
                             log=Q4O.RunLog(echo=False))
    gate = QB.evaluate_recovery_gate(
        rec, {"permutation_invariance":
              QB.permutation_invariance(flat_cohort, flat, recs),
              "shift_control": sh,
              "wrong_record_control":
              QB.wrong_record_control(flat_cohort, flat, recs)})
    check(gate["gate"] == QB.GATE_NOGO,
          "a non-identifying key cannot reach GO however it was assigned")


def test_ordinal_fill_needs_its_licence():
    print("ordinal fill is licensed by the anchors, never assumed")
    cohort, source, recs = _pair(n_per=60)
    rec = QB.recover_symbols(cohort, source, recs, log=Q4O.RunLog(echo=False))
    check(rec["n_anchor"] + rec["n_extended"] == rec["n_matched"],
          "every match is either a content anchor or a licensed fill")
    if rec["n_extended"]:
        check(rec["ordinal_consistency_min"] == 1.0,
              "beats are only filled where the anchors mapped exactly ordinally")

    # Reversing one record's source rows breaks the ordinal hypothesis: the
    # anchors still match (the key is order-free) but the fill must not happen.
    rev = QB.SymbolSource(record=source.record.copy(), sym=source.sym.copy(),
                          y5=source.y5.copy(), pre_rr=source.pre_rr.copy(),
                          post_rr=source.post_rr.copy(),
                          records=source.records.copy())
    idx = source.idx_of[int(recs[0])]
    for arr in ("sym", "y5", "pre_rr", "post_rr"):
        getattr(rev, arr)[idx] = getattr(rev, arr)[idx][::-1]
    rev.idx_of = {int(r): np.where(rev.record == r)[0] for r in rev.records}
    out = QB.recover_symbols(cohort, rev, [recs[0]], log=Q4O.RunLog(echo=False))
    row = out["per_record"][0]
    check(row["n_extended"] == 0 or row["ordinal_consistency"] == 1.0,
          "a record whose mapping is not ordinal gets no ordinal fill")
    check(out["symbol_in_s_set_fraction"] >= QB.MIN_SYMBOL_IN_S_SET,
          "the content anchors still recover real S symbols after reversal")


def test_record_identity_is_established_not_assumed():
    print("record identity: ids may not be MIT record numbers")
    tmp = tempfile.mkdtemp(prefix="q5b0_ids_")
    try:
        cohort, source, recs = _pair(n_per=60, drop=1)
        ident = QB.resolve_record_mapping(cohort, source,
                                          log=Q4O.RunLog(echo=False))
        check(ident["ok"] and ident["method"] == "identity_verified",
              "record numbers are accepted only after the S counts agree")

        # the shape the real ecg_multi.npz is in: ordinal ids, no relation to
        # MIT record numbers. Filtering on 100..234 would empty the file.
        order = {int(r): i for i, r in enumerate(sorted(set(
            source.record.tolist())))}
        ordinal = QB.SymbolSource(
            record=np.array([order[int(r)] for r in source.record], int),
            sym=source.sym, y5=source.y5, pre_rr=source.pre_rr,
            post_rr=source.post_rr,
            records=np.array(sorted(order.values()), int))
        ordinal.idx_of = {int(r): np.where(ordinal.record == r)[0]
                          for r in ordinal.records}
        rmap = QB.resolve_record_mapping(cohort, ordinal,
                                         log=Q4O.RunLog(echo=False))
        check(rmap["ok"] and rmap["method"] == "fingerprint_assignment",
              "ordinal ids are paired by the 5-class profile instead")
        check(rmap["source_id_coding"] == "ordinal_or_other",
              "the id coding is reported, not silently assumed")
        check(rmap["mapping"] == {int(r): order[int(r)] for r in order},
              "the assignment recovers the true pairing")

        npz = QB.write_symbol_npz(os.path.join(tmp, "ordinal.npz"), ordinal)
        res = QB.run_recovery(cohort, npz, os.path.join(tmp, "run"),
                              log=Q4O.RunLog(echo=False))
        check(res["gate"] == QB.GATE_GO,
              f"a file with ordinal ids still joins ({res['match_fraction']:.1%})")
        check(res["record_mapping"]["method"] == "fingerprint_assignment",
              "the result records how identity was established")

        # a source that shares no record profile at all: NO-GO with a bundle,
        # never a crash that leaves nothing behind
        alien = QB.SymbolSource(
            record=np.zeros(50, int), sym=np.full(50, "A", dtype="<U2"),
            y5=np.zeros(50, int), pre_rr=np.full(50, 0.8),
            post_rr=np.full(50, 0.8), records=np.array([0]))
        alien.idx_of = {0: np.arange(50)}
        bad = QB.resolve_record_mapping(cohort, alien,
                                        log=Q4O.RunLog(echo=False))
        check(bad["ok"] is False and bad.get("reason"),
              "an unresolvable mapping is reported, not raised")
        anpz = QB.write_symbol_npz(os.path.join(tmp, "alien.npz"), alien)
        ares = QB.run_recovery(cohort, anpz, os.path.join(tmp, "alien"),
                               log=Q4O.RunLog(echo=False))
        check(ares["gate"] == QB.GATE_NOGO
              and ares["status"] == QB.STATUS_MEASURED,
              "no record correspondence -> measured NO-GO")
        for f in QB.RECOVERY_BUNDLE_FILES:
            check(os.path.exists(os.path.join(tmp, "alien", f)),
                  f"the NO-GO-by-mapping bundle still has {f}")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_gate_blocks_attachment_and_reanalysis():
    print("NO-GO stops everything downstream")
    cohort, source, recs = _pair(n_per=60, scramble=True)
    rec = QB.recover_symbols(cohort, source, recs, log=Q4O.RunLog(echo=False))
    gate = QB.evaluate_recovery_gate(rec, _controls(cohort, source, recs))
    att = QB.attach_recovered_symbols(cohort, rec, gate,
                                      log=Q4O.RunLog(echo=False))
    check(att["attached"] is False, "symbols are not attached on NO-GO")
    check(set(np.unique(cohort.sym).tolist()) == {"?"},
          "the cohort keeps its blank symbols")
    expect_raise(lambda: QB.run_reanalysis(
        cohort, {}, {}, {}, {"_sym": rec["sym"], "subtype_counts":
                             rec["subtype_counts"], "gate_detail": gate},
        tempfile.mkdtemp(prefix="q5b0_never_")),
        "the re-analysis refuses to run on a NO-GO recovery", QB.Q5B0Error)
    check(QA.BLOCK_TO_BRANCH.get("B_SUBTYPE") is None,
          "B_SUBTYPE still names no intervention branch — recovering it cannot "
          "auto-start a model experiment")


def test_recovery_bundle_and_report():
    print("recovery bundle schema and REPORT")
    tmp = tempfile.mkdtemp(prefix="q5b0_bundle_")
    try:
        cohort, source, recs = _pair(n_per=60, drop=2)
        npz = QB.write_symbol_npz(os.path.join(tmp, "multi.npz"), source)
        out = os.path.join(tmp, "run")
        res = QB.run_recovery(cohort, npz, out, provenance={"fixture": True},
                              log=Q4O.RunLog(echo=False))
        check(res["training_performed"] is False,
              "the result records that nothing was trained")
        for f in QB.RECOVERY_BUNDLE_FILES:
            check(os.path.exists(os.path.join(out, f)), f"bundle has {f}")
        for f in QB.RECOVERY_FIGURES:
            check(os.path.exists(os.path.join(out, "figures", f)),
                  f"figure {f} written")
        summary = open(os.path.join(out, "summary.md"), encoding="utf-8").read()
        check("실패 연관 요인" in summary and "원인" in summary,
              "the summary keeps the association/cause boundary")
        check("residual CNN" in summary and "INCART" in summary,
              "the summary repeats the closed directions")
        check("Q5-B" in summary and "구현하지 않는다" in summary,
              "the summary states the intervention is not implemented here")
        before = _dir_fingerprint(out)
        rep = QB.report_recovery(out)
        check(_dir_fingerprint(out) == before,
              "REPORT does not write into the bundle")
        check(rep["result"]["gate"] == res["gate"] and rep["summary"],
              "REPORT returns the stored gate and summary")
        check(QB.report_recovery(os.path.join(tmp, "nothing"))["status"]
              == QB.STATUS_NOT_RUN, "REPORT on an empty path says NOT RUN")

        # the bundle must be re-readable: REANALYZE is its own run, not a
        # variable left over in a notebook
        back = QB.load_recovery(out, cohort)
        check(np.array_equal(back["_sym"], res["_sym"])
              and back["gate_pass"] == res["gate_pass"],
              "the stored symbols round-trip out of the bundle")
        check(back["recovery"] and back["controls"],
              "the reloaded recovery carries its summary and its controls")
        other = QA.synthetic_atlas(n_per_record=40, seed=11)
        expect_raise(lambda: QB.load_recovery(out, other),
                     "symbols recovered against another source are refused",
                     QB.Q5B0Error)

        # a NO-GO run still writes the full evidence bundle
        bad_cohort, bad_source, _ = _pair(n_per=60, scramble=True)
        bad_npz = QB.write_symbol_npz(os.path.join(tmp, "bad.npz"), bad_source)
        bad_out = os.path.join(tmp, "nogo")
        bad = QB.run_recovery(bad_cohort, bad_npz, bad_out,
                              log=Q4O.RunLog(echo=False))
        check(bad["gate"] == QB.GATE_NOGO and bad["status"]
              == QB.STATUS_MEASURED,
              "NO-GO is a measured result, not a crash")
        for f in QB.RECOVERY_BUNDLE_FILES:
            check(os.path.exists(os.path.join(bad_out, f)),
                  f"NO-GO bundle has {f}")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_reanalysis_adds_the_fifth_block():
    print("re-analysis runs Q5-A's atlas with five blocks")
    tmp = tempfile.mkdtemp(prefix="q5b0_re_")
    try:
        cohort, inv, freeze, models = _atlas_fixture(tmp, n_per=120)
        source = QB.symbol_source_from_cohort(cohort, drop=1, seed=9)
        QB.blank_symbols(cohort)
        npz = QB.write_symbol_npz(os.path.join(tmp, "multi.npz"), source)
        rec = QB.run_recovery(cohort, npz, os.path.join(tmp, "rec"),
                              log=Q4O.RunLog(echo=False))
        check(rec["gate"] == QB.GATE_GO, "the fixture recovery passes the gate")
        runs_before = _dir_fingerprint(os.path.join(tmp, "runs"))
        out = os.path.join(tmp, "atlas")
        res = QB.run_reanalysis(cohort, models, inv, freeze, rec, out,
                                n_boot=200, log=Q4O.RunLog(echo=False))
        check(_dir_fingerprint(os.path.join(tmp, "runs")) == runs_before,
              "the frozen baseline runs are untouched")
        blocks = res["block_evidence"]["blocks"]
        check("B_SUBTYPE" in blocks,
              "B_SUBTYPE is scored now that symbols exist")
        check(len(blocks) == len(QA.BLOCKS),
              f"all {len(QA.BLOCKS)} pre-registered blocks are scored")
        check(res["decision"]["branch"] in QA.BRANCHES,
              "the verdict is one of Q5-A's pre-registered branches")
        check(res["training_performed"] is False,
              "the re-analysis trains nothing")
        check(os.path.exists(os.path.join(out, "q5b0_recovery.json")),
              "the atlas bundle carries the recovery evidence beside it")
        note = json.load(open(os.path.join(out, "q5b0_recovery.json"),
                              encoding="utf-8"))
        check(note["experiment_id"] == QB.EXPERIMENT_ID
              and note["blocks_present"],
              "the addendum names EXP-2026-005 and the blocks it enabled")
        sc = res["subtype_shuffle_control"]
        check(sc["available"] and "pass" in sc,
              "the subtype shuffle control ran on the re-analysis")
        for f in QA.BUNDLE_FILES:
            check(os.path.exists(os.path.join(out, f)),
                  f"the re-analysis keeps Q5-A's bundle contract: {f}")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_shuffle_control_semantics():
    print("subtype shuffle control")
    rng = np.random.default_rng(3)
    n = 600
    rec = rng.integers(0, 12, n)
    sub = rng.choice(np.array(QA.S_SUBTYPES), size=n)
    # a planted effect: subtype 'a' really is ranked worse
    outcome = 0.5 + 0.35 * (sub == "a") + 0.02 * rng.standard_normal(n)
    out = QB.subtype_shuffle_control(sub, rec, outcome, repeats=3, n_boot=50)
    check(out["available"] and out["applicable"],
          "a real subtype effect makes the control applicable")
    check(out["shuffled_mean"] < out["real_delta"],
          "shuffling the symbols inside each record destroys the effect")
    check(out["pass"], "a genuine effect passes its own falsification test")

    flat_outcome = 0.5 + 0.02 * rng.standard_normal(n)
    null = QB.subtype_shuffle_control(sub, rec, flat_outcome, repeats=3,
                                      n_boot=50)
    check(null["applicable"] is False and null["retained_fraction"] is None,
          "with no effect to destroy the control reports 'not applicable'")
    check(null["pass"] is True and "nothing" in null["verdict"],
          "it does not manufacture a verdict out of two noise numbers")
    check(QB.subtype_shuffle_control(sub[:5], rec, outcome)["available"]
          is False,
          "mismatched inputs mean no control, stated plainly")


def test_language_boundary():
    print("language boundary and closed directions")
    src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "q5b0_subtype_key_recovery.py"),
               encoding="utf-8").read()
    check("residual CNN" not in src.replace(
        "residual CNN 경로는 closed", "").replace(
        "no residual CNN", "") or "closed" in src,
        "residual CNN is only ever mentioned as a closed direction")
    check("ground truth" not in src.lower().replace(
        "p-wave ground truth", ""), "no proxy is called ground truth")
    for bad in ("cause of the failure", "causal factor", "proves that"):
        check(bad not in src.lower(), f"no causal claim: {bad!r}")
    check("failure-associated" in src or "실패 연관 요인" in src,
          "the association wording is present")


def test_spec_and_docs():
    print("spec contract")
    root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
    spec = os.path.join(root, "experiments", "specs",
                        "EXP-2026-005-q5b0-subtype-key-recovery.md")
    if not os.path.exists(spec):
        check(False, "Q5-B-0 spec missing")
        return
    text = open(spec, encoding="utf-8").read()
    check("kind: preregistered_analysis_only" in text,
          "the spec declares the analysis-only kind")
    check("result_status: RESULT_NOT_RUN" in text
          or "result_status: MEASURED" in text,
          "the spec carries a legal result_status")
    for f in ("mit-bih/q5b0_subtype_key_recovery.py",
              "mit-bih/test_q5b0_subtype_key_recovery.py",
              "notebooks/quest51_q5b0_subtype_key_recovery.ipynb",
              "experiments/specs/EXP-2026-005-q5b0-subtype-key-recovery.md",
              "research/ASSETS.md", "research/PROJECT_STATE.md"):
        check(f in text, f"the spec lists the allowed file {f}")
    for g in (QB.GATE_GO, QB.GATE_NOGO):
        check(g in text, f"the spec documents the gate outcome {g}")
    for name in ("permutation", "shift", "wrong-record", "shuffle"):
        check(name in text.lower(), f"the spec pre-registers the {name} control")
    check(str(QB.MIN_S_MATCH_FRACTION) in text
          and str(QB.MIN_SYMBOL_IN_S_SET) in text,
          "the spec states the gate thresholds it will be judged on")
    check("Q5-B-1" in text and ("구현하지 않는다" in text
                                or "만들지 않는다" in text),
          "the spec states the intervention pilot is not implemented")
    # the design brief must not have become an implementation
    stray = [os.path.join(d, f)
             for sub in ("mit-bih", "notebooks", "experiments/specs")
             for d, _x, fs in os.walk(os.path.join(root, sub)) for f in fs
             if "q5b1" in f.lower() or "cvar" in f.lower()]
    check(not stray, f"no Q5-B-1 intervention file exists yet: {stray}")


def test_notebook_static():
    print("notebook static validation")
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                     "notebooks", "quest51_q5b0_subtype_key_recovery.ipynb")
    if not os.path.exists(p):
        check(False, "quest51 notebook missing")
        return
    nb = json.load(open(p, encoding="utf-8"))
    cells = nb["cells"]
    src = ["".join(c["source"]) for c in cells]
    all_src = "\n".join(src)
    first = src[0]
    cfg = next((s for s in src if "MODE = " in s), "")
    has_out = any(c.get("outputs") for c in cells if c["cell_type"] == "code")
    if "MEASURED" in first.splitlines()[2]:
        check(has_out, "a measured notebook keeps its stored outputs")
        check("RESULT NOT RUN" not in first.splitlines()[2],
              "the front page no longer claims RESULT NOT RUN")
    else:
        check("RESULT NOT RUN" in first, "front page declares RESULT NOT RUN")
        check(not has_out, "design notebook committed without stored outputs")
        check('MODE = "DESIGN"' in cfg, "default mode is DESIGN")
    check("assert MODE in VALID_MODES" in cfg,
          "exactly-one-mode assertion present")
    check(all(m in all_src for m in QB.MODES), "all four modes wired")
    check("EXP-2026-005" in first and "Q5-B-0" in first,
          "front page identifies the experiment")
    check("ANALYSIS ONLY" in first and "NO TRAINING" in first,
          "front page declares analysis-only / no training")
    check("실패 연관 요인" in first and "원인" in first,
          "front page states association, not cause")
    check("residual CNN" in first and "INCART" in first,
          "front page repeats the closed directions")
    need = next((int(l.split("=")[1].split("#")[0])
                 for l in all_src.splitlines() if l.startswith("NEED_Q5B0 =")),
                0)
    check(need == QB.MODULE_VERSION,
          f"notebook pins the module version (NEED_Q5B0={need} vs "
          f"MODULE_VERSION={QB.MODULE_VERSION})")
    check("BRANCH" in all_src and "checkout" in all_src,
          "cell 2 checks out an explicit branch")
    check("1aSj_1jvS_W2iruVnORIG6DTVuHobzNzq" in all_src
          and "1p3HvC_bnbiQlEanFOVIvVdejy60W0tho" in all_src,
          "the Drive ids of both inputs are shown")
    check("test_q5a" in all_src and "test_q5b0" in all_src,
          "the notebook runs both test suites")
    check("NO_GO" in all_src or "NO-GO" in all_src,
          "the notebook shows what happens on NO-GO")


def test_q5a_is_untouched():
    print("Q5-A stays exactly as it was accepted")
    check(QA.MODULE_VERSION >= 8, "Q5-A module is the accepted version")
    check(QA.PRIMARY_OUTCOME == QA.OUTCOME_RANK,
          "the primary outcome is still the within-record rank")
    check(QA.BLOCK_MARGIN == 1.25
          and QA.BLOCK_MIN_PATIENT_DIRECTION == 0.60,
          "the branch thresholds are unchanged")
    check(QB.S_SUBTYPES is QA.S_SUBTYPES and QB.S_INDEX == QA.S_INDEX,
          "Q5-B-0 reuses Q5-A's subtype set and S index, never redefines them")
    check("B_SUBTYPE" in QA.BLOCKS,
          "B_SUBTYPE was pre-registered in Q5-A, not invented here")


def main() -> int:
    print("=" * 78)
    print("EXP-2026-005 / Q5-B-0 — CPU contract")
    print("=" * 78)
    for fn in (test_import_is_inert, test_modes, test_symbol_source_loader,
               test_rr_unit_is_verified, test_fingerprint_is_order_free,
               test_assignment_rules, test_recovery_on_a_faithful_source,
               test_gate_refuses_an_unrelated_source,
               test_symbols_never_drive_the_match, test_controls_can_fail,
               test_ordinal_fill_needs_its_licence,
               test_record_identity_is_established_not_assumed,
               test_gate_blocks_attachment_and_reanalysis,
               test_recovery_bundle_and_report,
               test_reanalysis_adds_the_fifth_block,
               test_shuffle_control_semantics, test_language_boundary,
               test_spec_and_docs, test_notebook_static, test_q5a_is_untouched):
        fn()
    print("=" * 78)
    print(f"passed {PASSED} - failed {FAILED}")
    print("=" * 78)
    return 1 if FAILED else 0


if __name__ == "__main__":
    sys.exit(main())
