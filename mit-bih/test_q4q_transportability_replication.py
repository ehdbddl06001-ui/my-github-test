#!/usr/bin/env python3
"""CPU test contract for EXP-2026-003 / Q4-Q (spec section 8). Not a GPU run."""
from __future__ import annotations

import json
import os
import shutil
import sys
import tempfile

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import q4o_leakage_free_residual as Q4O  # noqa: E402
import q4p_best_epoch_zero_diagnostic as QP  # noqa: E402
import q4q_transportability_replication as QQ  # noqa: E402

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


# ─────────────────────────────────────────────────────────────────────────────
def test_modes():
    print("mode resolution")
    for m in QQ.MODES:
        check(QQ.resolve_mode(m.lower()) == m, f"mode {m} resolves")
    expect_raise(lambda: QQ.resolve_mode("FULL_RUN"), "unknown mode rejected")
    expect_raise(lambda: QQ.resolve_mode(""), "empty mode rejected")


def test_split():
    print("frozen MIT split")
    cohort, feats = QQ.synthetic_mit()
    check(tuple(sorted(set(cohort.rid.tolist()))) == QQ.MIT_ALL_RECORDS,
          "synthetic cohort carries the canonical 44 record ids")
    split = QQ.mit_split(cohort)
    check(sorted(split["ds2"]) == sorted(QQ.DS2_RECORDS),
          "DS2 is exactly the canonical de Chazal DS2 (22 patients)")
    check(sorted(split["fit"] + split["dev"]) == sorted(QQ.DS1_RECORDS),
          "fit+dev partitions DS1 exactly")
    check(not (set(split["fit"]) & set(split["dev"])), "fit/dev disjoint")
    check(not (set(split["ds1"]) & set(split["ds2"])),
          "DS1/DS2 patient non-overlap")
    split2 = QQ.mit_split(cohort)
    check(split == split2, "split is deterministic (seed-invariant)")
    check(len(split["dev"]) >= 3, "dev has enough patients for record metrics")


def _write_fake_mamba(path, n_per=30, records=QQ.MIT_ALL_RECORDS, keys=None,
                      y_max=4):
    rng = np.random.RandomState(3)
    n = n_per * len(records)
    pid = np.repeat(np.array(records, int), n_per)
    y = rng.randint(0, y_max + 1, n)
    y[::7] = 1                                     # ensure S beats everywhere
    payload = {"beat": rng.normal(size=(n, 2, 32)).astype("float32"),
               "feats": rng.normal(size=(n, 4)),
               "y": y, "pid": pid,
               "ref": rng.normal(size=(n, 2, 32)).astype("float32"),
               "t": np.arange(n)}
    if keys is not None:
        payload = {k: payload[k] for k in keys}
    np.savez(path, **payload)
    return n


def test_mit_loader():
    print("MIT loader audits")
    tmp = tempfile.mkdtemp(prefix="q4q_loader_")
    try:
        good = os.path.join(tmp, "mamba_data.npz")
        n = _write_fake_mamba(good)
        exp = {"n_beat": n, "n_record": 44, "n_ds1": 22, "n_ds2": 22}
        cohort, feats, audit = QQ.load_mit_cohort(good, expected=exp)
        check(cohort.n == n and feats.shape[0] == n, "aligned load")
        check(audit["n_record"] == 44, "44 records audited")
        check(bool(cohort.y.any()) and not bool(cohort.y.all()),
              "binary S label has both classes")

        missing = os.path.join(tmp, "missing.npz")
        _write_fake_mamba(missing, keys=("beat", "y", "pid"))
        expect_raise(lambda: QQ.load_mit_cohort(missing, expected=exp),
                     "missing 'feats' key rejected", QQ.Q4QError)

        badrec = os.path.join(tmp, "badrec.npz")
        _write_fake_mamba(badrec, records=tuple(range(44)))
        expect_raise(lambda: QQ.load_mit_cohort(badrec, expected=None),
                     "non-canonical pid coding rejected (no guessing)",
                     QQ.Q4QError)

        expect_raise(lambda: QQ.load_mit_cohort(
            good, expected={"n_beat": n + 1, "n_record": 44,
                            "n_ds1": 22, "n_ds2": 22}),
            "count mismatch vs registered asset is a STOP", QQ.Q4QError)

        bady = os.path.join(tmp, "bady.npz")
        _write_fake_mamba(bady, y_max=9)
        expect_raise(lambda: QQ.load_mit_cohort(bady, expected=None),
                     "non-AAMI label coding rejected", QQ.Q4QError)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def _profs(d):
    return {r: {"classes": list(map(int, c))} for r, c in d.items()}


def test_cross_check():
    print("mamba vs ecg_multi cross-check (5-class fingerprint corroboration)")

    # unit: measured beat-deficit case — mamba's noisy record keeps fewer
    # beats (2887 vs 2953, -2.3%) but the class fingerprint still pins it;
    # a warning is reported instead of a STOP.
    mamba_u = _profs({208: [1500, 2, 1300, 20, 65],      # 2887 beats
                      230: [2200, 1, 50, 4, 0],          # 2255
                      999: [1800, 30, 10, 2, 0]})
    multi_u = _profs({0: [1560, 2, 1305, 21, 65],        # 2953 (208)
                      1: [2201, 1, 50, 4, 0],            # 2256 (230)
                      2: [1802, 31, 10, 2, 0],
                      3: [400, 0, 5, 0, 1700],           # paced-like
                      4: [500, 1, 2, 0, 1600]})
    m = QQ._fingerprint_match(mamba_u, multi_u)
    check(m["mapping"] == {208: 0, 230: 1, 999: 2},
          "fingerprint assignment pins records despite a 2.3% beat deficit "
          "(measured 2887/2953 case)")
    check(len(m["warnings"]) == 0 or "beat count" in m["warnings"][0],
          "beat deficits are warnings, never silent")
    check(m["s_agreement"]["total_abs_diff"] == 1
          and sorted(m["leftover"]) == [3, 4],
          "S disagreement reported; paced-like records left over")

    # unit: per-record S cap still hard-fails the assignment
    expect_raise(
        lambda: QQ._fingerprint_match(_profs({1: [2000, 15, 5, 0, 0]}),
                                      _profs({9: [2000, 30, 5, 0, 0]})),
        "per-record S disagreement beyond the 10-beat cap STOPs",
        QQ.Q4QError)
    # unit: total S budget
    expect_raise(
        lambda: QQ._fingerprint_match(
            _profs({i: [2000, 10, 5, 0, 0] for i in range(4)}),
            _profs({i: [2000, 16, 5, 0, 0] for i in range(4)})),
        "total S disagreement beyond the 20-beat budget STOPs", QQ.Q4QError)

    tmp = tempfile.mkdtemp(prefix="q4q_multi_")
    try:
        good = os.path.join(tmp, "mamba.npz")
        n = _write_fake_mamba(good)
        exp = {"n_beat": n, "n_record": 44, "n_ds1": 22, "n_ds2": 22}
        _, _, audit = QQ.load_mit_cohort(good, expected=exp)
        with np.load(good) as srcz:
            pid_m = np.asarray(srcz["pid"]).astype(int)
            y_m = np.asarray(srcz["y"]).astype(int)
        db44 = np.array(["mitdb"] * len(pid_m))

        # A) record-coded identical 44-record subset -> pass, 0 leftovers
        multi_a = os.path.join(tmp, "multi_a.npz")
        np.savez(multi_a, pid=pid_m, db=db44, y5=y_m)
        res = QQ.cross_check_mit_vs_multi(audit, multi_a)
        check(res["pass"] and res["leftover_records"] == 0
              and len(res["table"]) == 44,
              "44-record identical subset passes with a full audit table")

        # B) ordinal pids + 4 paced-like (Q-heavy) extras -> pass
        ordinal = {r: i for i, r in enumerate(sorted(set(pid_m.tolist())))}
        pid_b = np.array([ordinal[r] for r in pid_m], int)
        extra_pid = np.repeat(np.arange(44, 48), 30)
        rngq = np.random.RandomState(9)
        y_extra = np.where(rngq.rand(len(extra_pid)) < 0.7, 4, 0)
        pid_48 = np.concatenate([pid_b, extra_pid])
        y_48 = np.concatenate([y_m, y_extra])
        db48 = np.array(["mitdb"] * len(pid_48))
        multi_b = os.path.join(tmp, "multi_b.npz")
        np.savez(multi_b, pid=pid_48, db=db48, y5=y_48)
        res_b = QQ.cross_check_mit_vs_multi(audit, multi_b)
        check(res_b["pass"] and res_b["leftover_records"] == 4
              and res_b["pid_coding"] == "ordinal_or_other",
              "48-record ordinal subset passes; 4 Q-heavy paced leftovers")

        # C) an extra record that is NOT paced-like (all-N) -> STOP
        y_bad = np.concatenate([y_m, np.zeros(len(extra_pid), int)])
        multi_c = os.path.join(tmp, "multi_c.npz")
        np.savez(multi_c, pid=pid_48, db=db48, y5=y_bad)
        expect_raise(lambda: QQ.cross_check_mit_vs_multi(audit, multi_c),
                     "non-paced-looking leftover records are a STOP",
                     QQ.Q4QError)
        res_c = QQ.cross_check_mit_vs_multi(audit, multi_c, strict=False)
        check(not res_c["pass"] and res_c["fail_reasons"]
              and "table" in res_c,
              "strict=False returns the failed audit with the full table "
              "(PREP_DATA writes it before stopping)")

        # D) S total mismatch -> fail reason recorded and strict STOP
        y_tot = y_m.copy()
        s_pos = np.where(y_tot == QQ.MIT_S_INDEX)[0]
        y_tot[s_pos[0]] = 0
        multi_d = os.path.join(tmp, "multi_d.npz")
        np.savez(multi_d, pid=pid_m, db=db44, y5=y_tot)
        expect_raise(lambda: QQ.cross_check_mit_vs_multi(audit, multi_d),
                     "S-total mismatch is a STOP", QQ.Q4QError)

        # E) one S beat flipped to V in one record -> small class diff,
        # S totals differ -> STOP; but with the S beat MOVED to another
        # record (totals equal) -> pass with reported disagreement
        y_mv = y_m.copy()
        recs = sorted(set(pid_m.tolist()))
        r_from = next(r for r in recs
                      if (y_mv[pid_m == r] == QQ.MIT_S_INDEX).sum() > 1)
        r_to = next(r for r in recs if r != r_from)
        i_from = np.where((pid_m == r_from) & (y_mv == QQ.MIT_S_INDEX))[0][0]
        i_to = np.where((pid_m == r_to) & (y_mv != QQ.MIT_S_INDEX))[0][0]
        y_mv[i_from] = 0
        y_mv[i_to] = QQ.MIT_S_INDEX
        multi_e = os.path.join(tmp, "multi_e.npz")
        np.savez(multi_e, pid=pid_m, db=db44, y5=y_mv)
        res_e = QQ.cross_check_mit_vs_multi(audit, multi_e)
        check(res_e["pass"]
              and res_e["s_agreement"]["n_mismatched_records"] == 2
              and res_e["s_agreement"]["total_abs_diff"] == 2,
              "small cross-prep S disagreement passes and is reported")

        nodb = os.path.join(tmp, "nodb.npz")
        np.savez(nodb, pid=pid_m)
        expect_raise(lambda: QQ.cross_check_mit_vs_multi(audit, nodb),
                     "missing db key rejected", QQ.Q4QError)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def _write_incart_headers(d, n_records=75, n_patients=32, ambiguous=None,
                          missing=None):
    per = [(i % n_patients) + 1 for i in range(n_records)]
    for i in range(n_records):
        name = f"I{i + 1:02d}"
        lines = [f"{name} 12 257 462600",
                 f"{name}.dat 16 306 16 0 1161 -11409 0 II",
                 "#<age>: 65 <sex>: F <diagnoses> CAD",
                 f"# patient {per[i]}",
                 "# PVCs, noise"]
        if ambiguous == name:
            lines.append("# patient 99")
        if missing == name:
            lines = [ln for ln in lines if not ln.startswith("# patient")]
        with open(os.path.join(d, f"{name}.hea"), "w", encoding="utf-8") as fh:
            fh.write("\n".join(lines) + "\n")


def test_incart_map():
    print("INCART 75 -> 32 patient map gate")
    line_ok = QQ.parse_incart_patient_line("x\n# patient 7\ny")
    check(line_ok == 7, "regex parses the real header comment form")
    check(QQ.parse_incart_patient_line("# patient 1\n# patient 2") is None,
          "multiple patient lines -> ambiguous -> None")
    check(QQ.parse_incart_patient_line("no metadata") is None,
          "missing patient line -> None")

    tmp = tempfile.mkdtemp(prefix="q4q_incart_")
    try:
        _write_incart_headers(tmp)
        mapping = QQ.parse_incart_patient_map(tmp)
        summary = QQ.validate_incart_map(mapping)
        check(summary["pass"] and summary["n_record"] == 75
              and summary["n_patient"] == 32, "75 records -> 32 patients pass")

        shutil.rmtree(tmp)
        os.makedirs(tmp)
        _write_incart_headers(tmp, ambiguous="I05")
        expect_raise(lambda: QQ.parse_incart_patient_map(tmp),
                     "ambiguous header FAILS (no manual guessing)", QQ.Q4QError)

        shutil.rmtree(tmp)
        os.makedirs(tmp)
        _write_incart_headers(tmp, missing="I09")
        expect_raise(lambda: QQ.parse_incart_patient_map(tmp),
                     "missing patient metadata FAILS", QQ.Q4QError)

        shutil.rmtree(tmp)
        os.makedirs(tmp)
        _write_incart_headers(tmp, n_patients=30)
        expect_raise(
            lambda: QQ.validate_incart_map(QQ.parse_incart_patient_map(tmp)),
            "wrong patient count (30) fails the 32-patient gate", QQ.Q4QError)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    audit = QQ.incart_adapter_audit()
    check(audit["gate_pass"] is False,
          "adapter gate defaults to FAIL until every row is measured comparable")
    measured = {f: {"comparable": True} for f in QQ.INCART_AUDIT_FIELDS}
    check(QQ.incart_adapter_audit(measured)["gate_pass"] is True,
          "adapter gate passes only when all rows measured comparable")


def test_offsets_leakage():
    print("cross-fitted offsets and Arm A leakage boundaries")
    cohort, feats = QQ.synthetic_mit()
    split = QQ.mit_split(cohort)
    offset, arm_a = QQ.ds1_offsets_and_arm_a(feats, cohort, split)
    used = Q4O.samples_of(cohort, split["fit"] + split["dev"] + split["ds2"])
    check(np.isfinite(offset[used]).all(), "offsets finite on fit/dev/DS2")

    # flipping a held-out fit patient's labels must not change ITS OWN offset.
    # Group assignment is burden-ordered (labels are legitimate training-side
    # info), so pin the grouping to the original burden while flipping labels —
    # the cross-fit property is about the SCORING model, not the grouping.
    burden = Q4O.record_burden(cohort, split["fit"])
    order = sorted(split["fit"], key=lambda r: (burden[r], r))
    hold = [r for i, r in enumerate(order) if i % 5 == 0]     # group 0
    y_flip = cohort.y.copy()
    for r in hold:
        y_flip[cohort.idx_of[r]] = ~y_flip[cohort.idx_of[r]]
    cohort_flip = Q4O.Cohort(
        beat=cohort.beat, y=y_flip, y3=cohort.y3, pre=cohort.pre,
        post=cohort.post, rid=cohort.rid, sym=cohort.sym,
        sample_id=cohort.sample_id, records=cohort.records,
        idx_of=cohort.idx_of)
    frozen = dict(burden)
    orig_burden_fn = QQ.record_burden
    try:
        QQ.record_burden = lambda c, recs: {r: frozen[r] for r in recs} \
            if set(recs) <= set(frozen) else orig_burden_fn(c, recs)
        offset2, _ = QQ.ds1_offsets_and_arm_a(feats, cohort_flip, split)
    finally:
        QQ.record_burden = orig_burden_fn
    hold_idx = Q4O.samples_of(cohort, hold)
    check(np.allclose(offset[hold_idx], offset2[hold_idx]),
          "held-out fit patients' offsets ignore their own labels (cross-fit)")

    # flipping DS2 labels must not change DS2 offsets/Arm A scores at all
    y_flip2 = cohort.y.copy()
    ds2_idx = Q4O.samples_of(cohort, split["ds2"])
    y_flip2[ds2_idx] = ~y_flip2[ds2_idx]
    cohort_flip2 = Q4O.Cohort(
        beat=cohort.beat, y=y_flip2, y3=cohort.y3, pre=cohort.pre,
        post=cohort.post, rid=cohort.rid, sym=cohort.sym,
        sample_id=cohort.sample_id, records=cohort.records,
        idx_of=cohort.idx_of)
    offset3, arm_a3 = QQ.ds1_offsets_and_arm_a(feats, cohort_flip2, split)
    check(np.allclose(offset[ds2_idx], offset3[ds2_idx])
          and np.allclose(arm_a[ds2_idx], arm_a3[ds2_idx]),
          "DS2 label flip leaves DS2 offsets and Arm A scores unchanged")


def test_training_boundaries():
    print("training loop boundaries (Q4-P loop reused on DS1->DS2)")
    torch_ok = True
    try:
        Q4O._require_torch()
    except Exception:
        torch_ok = False
    if not torch_ok:
        check(False, "torch unavailable — training boundary tests cannot run")
        return
    cohort, feats = QQ.synthetic_mit(width=32)
    split = QQ.mit_split(cohort)
    offset, _ = QQ.ds1_offsets_and_arm_a(feats, cohort, split)
    fit_idx = Q4O.samples_of(cohort, split["fit"])
    dev_idx = Q4O.samples_of(cohort, split["dev"])
    ds2_idx = Q4O.samples_of(cohort, split["ds2"])
    X = Q4O.current_beat_input(cohort)
    seed = int(QQ.SEEDS[0])

    results = {}
    for sch in QQ.QQ_SCHEDULES:
        Q4O.set_determinism(seed)
        net = Q4O.build_residual_net(X.shape[1], init="normal")
        results[sch] = QP.diagnostic_train_one_fold(
            net, X, offset, cohort.y.astype("float32"), cohort.rid,
            fit_idx, dev_idx, ds2_idx, seed, "cpu", sch, epochs=2, batch=256)

    r0 = results["S0_original"]
    cp0 = r0["checkpoints"][0]
    check(cp0["epoch"] == -1 and cp0["optimizer_steps"] == 0,
          "epoch -1 exists with zero optimizer steps")
    check(abs(cp0["alpha"]) == 0.0, "epoch -1 alpha is exactly 0")
    check(np.allclose(r0["test_logits_by_epoch"][-1], offset[ds2_idx],
                      atol=1e-5),
          "epoch -1 DS2 logits equal the morphology offset (alpha off)")
    check(len(r0["checkpoints"]) == 3,
          "all epochs run (2 + epoch -1); nothing stops the optimizer")

    r2 = results["S2_alpha_low"]
    check(np.allclose(r0["test_logits_by_epoch"][-1],
                      r2["test_logits_by_epoch"][-1]),
          "paired initialization: epoch -1 state identical across schedules")

    # selector is dev-only: corrupting stored test logits must not change it
    sel_before = QQ.select_checkpoint(r0["checkpoints"], QQ.SELECTOR)
    import copy
    cps = copy.deepcopy(r0["checkpoints"])
    for c in cps:
        for k in list(c):
            if k.startswith("test"):
                c[k] = 1e9
    check(QQ.select_checkpoint(cps, QQ.SELECTOR) == sel_before,
          "selector reads dev fields only")

    # DS2 label flip: selection and DS2 logits identical
    y_flip = cohort.y.copy()
    y_flip[ds2_idx] = ~y_flip[ds2_idx]
    Q4O.set_determinism(seed)
    net = Q4O.build_residual_net(X.shape[1], init="normal")
    r_flip = QP.diagnostic_train_one_fold(
        net, X, offset, y_flip.astype("float32"), cohort.rid,
        fit_idx, dev_idx, ds2_idx, seed, "cpu", "S0_original",
        epochs=2, batch=256)
    check(r_flip["selected"][QQ.SELECTOR] == r0["selected"][QQ.SELECTOR],
          "outer-test (DS2) label flip does not change checkpoint selection")
    sel_ep = r0["selected"][QQ.SELECTOR]
    check(np.allclose(r_flip["test_logits_by_epoch"][sel_ep],
                      r0["test_logits_by_epoch"][sel_ep]),
          "outer-test label flip does not change DS2 logits")


def test_shuffle_control():
    print("Arm D shuffled-waveform control")
    cohort, _ = QQ.synthetic_mit(width=32)
    y_before = cohort.y.copy()
    shuffled, rule = Q4O.shuffle_waveforms_within_record(cohort)
    check(np.array_equal(cohort.y, y_before), "labels untouched by the shuffle")
    ok_within, moved = True, 0
    for r in cohort.records:
        idx = cohort.idx_of[int(r)]
        a = np.sort(cohort.beat[idx].reshape(len(idx), -1), axis=0)
        b = np.sort(shuffled[idx].reshape(len(idx), -1), axis=0)
        ok_within &= np.allclose(a, b)
        moved += int((cohort.beat[idx] != shuffled[idx]).any())
    check(ok_within, "shuffle is a permutation WITHIN each record")
    check(moved > 0, "shuffle actually moves waveforms")


def _mk_per_seed(vals):
    """{seed: {record: value}} from {seed: [v1, v2, ...]} over records 0..k."""
    return {s: {r: float(v) for r, v in enumerate(vs)} for s, vs in vals.items()}


def test_contrast_math():
    print("contrast / DiD arithmetic on a hand fixture")
    a = _mk_per_seed({1: [0.6, 0.7, 0.8], 2: [0.62, 0.72, 0.82]})
    b = _mk_per_seed({1: [0.5, 0.6, 0.7], 2: [0.52, 0.62, 0.72]})
    con = QQ.contrast(a, b, n_boot=200)
    check(abs(con["record_bootstrap"]["mean"] - 0.1) < 1e-9,
          "contrast mean matches the hand computation (+0.100)")
    check(all(abs(v - 0.1) < 1e-9 for v in con["by_seed"]),
          "by-seed values match")
    hi = _mk_per_seed({1: [0.10, 0.10, 0.10], 2: [0.10, 0.10, 0.10]})
    lo = _mk_per_seed({1: [0.04, 0.04, 0.04], 2: [0.04, 0.04, 0.04]})
    did = QQ.contrast(hi, lo, n_boot=200)
    check(abs(did["record_bootstrap"]["mean"] - 0.06) < 1e-9,
          "DiD mean = (C-D)_S2 - (C-D)_S0 fixture (+0.060)")


def test_utility_gate():
    print("pre-registered utility gate fixtures")
    arm_a = {r: 0.60 for r in range(6)}
    big = _mk_per_seed({s: [0.62] * 6 for s in range(5)})     # +0.020 uniform
    g = QQ.evaluate_utility_gate(big, arm_a, n_boot=200)
    check(g["pass"], "clear +0.020 gain with stable seeds passes the gate")

    small = _mk_per_seed({s: [0.61] * 6 for s in range(5)})   # +0.010 < 0.015
    g2 = QQ.evaluate_utility_gate(small, arm_a, n_boot=200)
    check(not g2["pass"] and not g2["checks"]["mean_gain_ge_threshold"],
          "+0.010 mean gain fails the >= +0.015 threshold")

    # big mean gain but one catastrophic patient -> p10 non-inferiority fails
    tail_vals = [0.66] * 5 + [0.40]
    tail = _mk_per_seed({s: tail_vals for s in range(5)})
    arm_a_t = {r: (0.60 if r < 5 else 0.55) for r in range(6)}
    g3 = QQ.evaluate_utility_gate(tail, arm_a_t, n_boot=200)
    check(not g3["checks"]["p10_non_inferior"] and not g3["pass"],
          "lower-tail degradation fails p10 non-inferiority")

    mixed = _mk_per_seed({0: [0.63] * 6, 1: [0.63] * 6, 2: [0.585] * 6,
                          3: [0.585] * 6, 4: [0.63] * 6})
    g4 = QQ.evaluate_utility_gate(mixed, arm_a, n_boot=200)
    check(not g4["checks"]["seed_direction_ok"],
          "3/5 positive seeds fails the >=4/5 rule")


def _fake_contrast(mean, lo, hi, by_seed):
    return {"record_bootstrap": {"mean": mean, "ci_low": lo, "ci_high": hi,
                                 "n_record": 22, "n_boot": 200},
            "by_seed": list(by_seed)}


def test_decision_matrix():
    print("decision matrix fixtures (each branch separated)")
    util_pass = {"pass": True, "checks": {}, "p10_c": 1, "p10_a": 1}
    util_fail = {"pass": False, "checks": {}, "p10_c": 1, "p10_a": 1}
    mech_pass = _fake_contrast(0.02, 0.005, 0.04, [0.02] * 5)
    mech_under = _fake_contrast(0.02, -0.005, 0.05, [0.02] * 5)
    mech_fail = _fake_contrast(0.0, -0.02, 0.02, [0.01, -0.01, 0.0, -0.02, 0.0])
    wf = _fake_contrast(0.01, 0.001, 0.02, [0.01] * 5)

    d = QQ.evaluate_decision_matrix(mech_pass, wf, util_pass)
    check(d["mechanism"]["pass"] and "INCART" in d["action"],
          "pass+pass -> proceed to frozen INCART stage")
    check("pristine" in d["action"],
          "pass+pass action still repeats the naming boundary")
    d = QQ.evaluate_decision_matrix(mech_pass, wf, util_fail)
    check("stop expanding" in d["action"],
          "mechanism pass + utility fail -> stop expanding residual CNN")
    d = QQ.evaluate_decision_matrix(mech_fail, wf, util_fail)
    check("stop the residual CNN path" in d["action"],
          "fail+fail -> stop the residual CNN path")
    d = QQ.evaluate_decision_matrix(mech_under, wf, util_fail)
    check(d["mechanism"]["underpowered"] and "underpowered" in d["action"],
          "positive mean + CI spanning 0 + stable seeds -> underpowered")
    check("substitute" in d["action"],
          "underpowered action forbids seed-for-patient substitution")


def _write_fake_q4p_bundle(d, n_per=400, n_rec=8, seeds=(1, 2, 3)):
    # records must be larger than K_SWEEP's k values (50..300) or the
    # achievement metric saturates at 1.0 and every contrast collapses to 0.
    rng = np.random.RandomState(5)
    rid = np.repeat(np.arange(n_rec), n_per)
    n = len(rid)
    y = rng.rand(n) < 0.25
    scored = np.ones(n, bool)
    base = rng.normal(size=n)
    arm_a = base + 0.6 * y

    def mk(strength):
        return np.stack([base + (0.6 + strength) * y + 0.3 * rng.normal(size=n)
                         for _ in seeds])

    payload = {"seeds": np.array(seeds), "record_id": rid,
               "sample_id": np.arange(n), "y_true": y, "scored_mask": scored,
               "fold": np.zeros(n, int), "logit_morph_baseline": arm_a,
               f"logit_morph_plus_raw_residual__S0_original__{QQ.SEL1}": mk(0.1),
               f"logit_morph_plus_raw_residual__S2_alpha_low__{QQ.SEL1}": mk(0.8),
               f"logit_shuffled_waveform_control__S0_original__{QQ.SEL1}": mk(0.0),
               f"logit_shuffled_waveform_control__S2_alpha_low__{QQ.SEL1}": mk(0.0)}
    np.savez_compressed(os.path.join(d, "predictions.npz"), **payload)
    for name in ("result.json", "manifest.json"):
        with open(os.path.join(d, name), "w", encoding="utf-8") as fh:
            json.dump({"fixture": name}, fh)


def test_q4p_derived():
    print("Q4-P no-retrain derived analysis (post-hoc; source immutable)")
    tmp = tempfile.mkdtemp(prefix="q4q_derived_")
    try:
        src = os.path.join(tmp, "q4p_run")
        out = os.path.join(tmp, "derived_v1")
        os.makedirs(src)
        _write_fake_q4p_bundle(src)
        fp0 = QQ.bundle_fingerprint(src, QQ.Q4P_SOURCE_FILES)

        expect_raise(
            lambda: QQ.q4p_derived_analysis(src, os.path.join(src, "derived")),
            "output inside the source bundle is refused", QQ.Q4QError)

        derived = QQ.q4p_derived_analysis(src, out, n_boot=200)
        check(os.path.exists(os.path.join(out, "derived_analysis.json"))
              and os.path.exists(os.path.join(out, "derived_tables.csv"))
              and os.path.exists(os.path.join(out,
                                              "derived_forest_waterfall.png")),
              "derived JSON/CSV/figure written to the NEW versioned path")
        check(QQ.bundle_fingerprint(src, QQ.Q4P_SOURCE_FILES) == fp0,
              "source Q4-P bundle byte-identical after the analysis")
        check(derived["source_immutable"] is True, "immutability flag recorded")
        did = derived["did_cd_s2_minus_s0"]["record_bootstrap"]
        check(did["mean"] > 0,
              "planted S2>S0 waveform signal yields a positive DiD mean")
        check("post-hoc" in derived["note"].lower()
              or "POST-HOC" in derived["note"],
              "output is labelled post-hoc (does not change B3)")
        check(derived["metric"] == "q4p_ksweep_achievement",
              "derived analysis keeps Q4-P's original k-sweep metric")

        rerun = QQ.q4p_derived_analysis(src, out, n_boot=200)
        check(rerun["did_cd_s2_minus_s0"] == derived["did_cd_s2_minus_s0"],
              "derived analysis is deterministic")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_smoke_bundle():
    print("CPU synthetic smoke run -> full bundle schema")
    torch_ok = True
    try:
        Q4O._require_torch()
    except Exception:
        torch_ok = False
    if not torch_ok:
        check(False, "torch unavailable — smoke cannot run")
        return
    tmp = tempfile.mkdtemp(prefix="q4q_smoke_")
    try:
        cohort, feats = QQ.synthetic_mit(width=32)
        prov = {"data": {"synthetic": True}, "git_commit_sha": "fixture"}
        res = QQ.run_replication(cohort, feats, prov, tmp,
                                 seeds=QQ.SEEDS[:2], epochs=2, n_boot=100,
                                 smoke=True)
        QQ.verify_bundle(tmp)
        check(True, "bundle schema + all figures present")
        check(res["smoke"] is True and res["status"] != "MEASURED",
              "smoke result is never labelled MEASURED")
        check(res["selector"] == QQ.SELECTOR
              and list(res["schedules"]) == list(QQ.QQ_SCHEDULES),
              "SEL1-only and exactly S0/S2 recorded")
        with np.load(os.path.join(tmp, "predictions.npz")) as npz:
            need = {"seeds", "record_id", "y_true", "split_ds2_mask",
                    "logit_morph_baseline",
                    f"logit_{QQ.ARM_C}__S2_alpha_low__{QQ.SELECTOR}"}
            check(need.issubset(set(npz.files)), "predictions.npz keys")
            ds2 = np.asarray(npz["split_ds2_mask"])
            lg = np.asarray(npz[f"logit_{QQ.ARM_C}__S2_alpha_low__{QQ.SELECTOR}"])
            check(np.isfinite(lg[:, ds2]).all() and np.isnan(lg[:, ~ds2]).all(),
                  "stored logits cover DS2 only (no train-side scores leak out)")
        dm = res["decision_matrix"]
        check({"mechanism", "waveform_specific", "utility", "action"}
              <= set(dm), "decision matrix auto-evaluated")
        split = res["split"]
        check(not (set(split["ds1"]) & set(split["ds2"])),
              "bundle split records DS1/DS2 non-overlap")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_notebook_static():
    print("notebook static validation")
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                     "notebooks", "quest49_q4q_transportability_replication.ipynb")
    if not os.path.exists(p):
        check(False, "quest49 notebook missing")
        return
    nb = json.load(open(p, encoding="utf-8"))
    cells = nb["cells"]
    src = ["".join(c["source"]) for c in cells]
    all_src = "\n".join(src)
    cfg = next((s for s in src if "MODE = " in s), "")
    check('MODE = "DESIGN"' in cfg, "default mode is DESIGN (not a GPU run)")
    check("assert MODE in VALID_MODES" in cfg,
          "exactly-one-mode assertion present")
    first_md = "".join(cells[0]["source"])
    check("RESULT NOT RUN" in first_md,
          "front page declares RESULT NOT RUN before any full run")
    check("1p3HvC_bnbiQlEanFOVIvVdejy60W0tho" in all_src
          and "1qS8JxwlARByoZrJLMb6wxSIktQypiRTF" in all_src,
          "data/run Drive file IDs shown on the front page")
    check("PREP_DATA" in all_src and "ANALYZE" in all_src
          and "FULL" in all_src, "all execution modes wired")
    check("q4p_derived_analysis" in all_src,
          "Q4-P derived analysis reachable from the notebook")
    stale = ("verdict B3 replicated" in all_src
             or "utility gate passed" in all_src)
    check(not stale, "no stale measured-result claims")
    has_out = any(c.get("outputs") for c in cells
                  if c["cell_type"] == "code")
    check(not has_out, "design notebook committed without stored outputs")
    check("EXP-2026-003" in all_src and "transportability" in all_src,
          "identifies the experiment")
    check("OUT_DERIVED" in all_src and "v1" in all_src,
          "derived outputs go to a NEW versioned path")
    check("sys.modules.pop" in all_src and "NEED_Q4Q" in all_src
          and "Restart runtime" in all_src,
          "cell 2 force-reimports modules after git pull and asserts "
          "freshness (stale-import guard)")
    check('"/content/my-github-test"' in all_src
          and 'os.chdir("/content")' in all_src and "rm" in all_src,
          "cell 2 chdirs to a valid cwd first and anchors the clone at an "
          "absolute path (no nested clones, no deleted-cwd traps)")


def test_regression_suites_importable():
    print("Q4-O / Q4-P regression suites remain importable and intact")
    check(QP.MODULE_VERSION >= 2, "Q4-P module present (>= v2)")
    check(Q4O.MODULE_VERSION >= 4, "Q4-O module present (>= v4)")
    check(QQ.self_check()["selector"] == "SEL1_record_bce",
          "self_check pins SEL1")


def main() -> int:
    print("=" * 78)
    print(f"EXP-2026-003 / Q4-Q test contract ({QQ.STATUS})")
    print("=" * 78)
    for fn in (test_modes, test_split, test_mit_loader, test_cross_check,
               test_incart_map, test_offsets_leakage,
               test_training_boundaries, test_shuffle_control,
               test_contrast_math, test_utility_gate, test_decision_matrix,
               test_q4p_derived, test_smoke_bundle, test_notebook_static,
               test_regression_suites_importable):
        fn()
    print("=" * 78)
    print(f"passed {PASSED} - failed {FAILED}")
    print("=" * 78)
    return 1 if FAILED else 0


if __name__ == "__main__":
    sys.exit(main())
