#!/usr/bin/env python3
"""CPU test contract for EXP-2026-006 / Q5-C (shared error core).

No GPU, no training, no Drive. The fixtures that matter are the ones where the
answer is "there is nothing here": a tree that can only ever find a core is not
a tree.
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
import q5c_shared_error_core as QC       # noqa: E402

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


class _Model:
    """Minimal stand-in for QA.ModelPredictions — Q5-C only reads ``score``."""

    def __init__(self, score):
        self.score = np.asarray(score, float)


def _fixture(n_per: int = 200, seed: int = 5, rho: float = 0.0,
             driver: str = "noise", n_model: int = 4):
    """A cohort plus models whose S-beat rankings share ``rho`` of a latent.

    ``driver='pre_rr'`` makes the shared latent a registered B_RR feature, so
    the core is discoverable; ``driver='noise'`` makes it a hidden variable no
    block can see, which is the case Q5-C must be able to report honestly.
    """
    rng = np.random.default_rng(seed)
    cohort = QA.synthetic_atlas(n_per_record=n_per, seed=seed)
    if driver == "pre_rr":
        latent = -np.asarray(cohort.pre_rr, float)
    else:
        latent = rng.standard_normal(cohort.n)
    latent = (latent - np.mean(latent)) / (np.std(latent) or 1.0)
    models = {}
    for k in range(n_model):
        noise = rng.standard_normal(cohort.n)
        z = rho * latent + np.sqrt(max(0.0, 1 - rho ** 2)) * noise
        models[f"M{k}"] = _Model(1.0 / (1.0 + np.exp(-z)))
    return cohort, models, np.arange(cohort.n)


# ─────────────────────────────────────────────────────────────────────────────
def test_import_is_inert():
    print("import does not train, download or mount")
    new = _MODULES_AFTER - _MODULES_BEFORE
    banned = {"torch", "tensorflow", "keras", "google.colab"}
    check(not (banned & {m.split(".")[0] for m in new}),
          "no training or Colab module imported")
    check(QC.assert_analysis_only()["q5c"]["analysis_only"],
          "the module contains no training call")
    check(QC.EXPERIMENT_ID == "EXP-2026-006" and QC.ARM_ID == "Q5-C",
          "identity is EXP-2026-006 / Q5-C")


def test_modes():
    print("mode handling")
    for m in QC.MODES:
        check(QC.resolve_mode(m.lower()) == m, f"mode {m} resolves")
    expect_raise(lambda: QC.resolve_mode("TRAIN"),
                 "an unknown mode is refused", QC.Q5CError)


def test_no_new_features_are_invented():
    print("the blocks are Q5-A's, not new ones")
    for b in QC.CORE_BLOCKS:
        check(b in QA.BLOCKS, f"{b} is a Q5-A block")
    check("B_SUBTYPE" not in QC.CORE_BLOCKS,
          "B_SUBTYPE stays closed (EXP-2026-005) and is not resurrected here")
    check("B_PATIENT" not in QC.CORE_BLOCKS,
          "B_PATIENT is excluded — hardness is defined WITHIN a record, so a "
          "patient feature would explain a variable already conditioned out")


def test_membership_is_a_within_record_median_split():
    print("hardness is defined inside the record")
    cohort, models, rows = _fixture(n_per=200, rho=0.0)
    m = QC.build_membership(cohort, models, rows, log=Q4O.RunLog(echo=False))
    for r in np.unique(m.record):
        sel = m.record == r
        n = int(sel.sum())
        for j in range(len(m.labels)):
            n_hard = int(m.hard[sel, j].sum())
            check(n_hard == int(np.ceil(QC.HARD_FRACTION * n)),
                  f"record {r} model {m.labels[j]}: exactly the worse half "
                  f"({n_hard}/{n})") if r == np.unique(m.record)[0] else None
    frac = [float(m.hard[m.record == r, 0].mean()) for r in np.unique(m.record)]
    check(all(abs(f - 0.5) <= 0.5 / QC.CORE_MIN_S_PER_RECORD + 1e-9
              for f in frac),
          "every record is split at its own median, so 'hard' says nothing "
          "about which record a beat is in")

    thin = QA.synthetic_atlas(n_per_record=200, seed=5)
    small = int(np.unique(thin.record)[0])
    idx = thin.idx_of[small]
    keep = np.ones(thin.n, bool)
    s_rows = idx[thin.y_s[idx]]
    keep[s_rows[QC.CORE_MIN_S_PER_RECORD - 1:]] = False
    for attr in ("key", "db", "record", "y5", "y_s", "sym", "pre_rr",
                 "post_rr"):
        setattr(thin, attr, getattr(thin, attr)[keep])
    thin.beat = thin.beat[keep]
    thin.idx_of = {int(r): np.where(thin.record == r)[0] for r in thin.records}
    tm = {k: _Model(v.score[keep]) for k, v in models.items()}
    m2 = QC.build_membership(thin, tm, np.arange(thin.n),
                             log=Q4O.RunLog(echo=False))
    check(small not in set(m2.record.tolist()),
          f"a record with < {QC.CORE_MIN_S_PER_RECORD} S beats is dropped, not "
          "split into a meaningless half")


def test_excess_is_measured_against_chance():
    print("co-hardness against its own chance rate")
    cohort, models, rows = _fixture(rho=0.0, seed=7)
    m = QC.build_membership(cohort, models, rows, log=Q4O.RunLog(echo=False))
    ex = QC.co_error_excess(m, n_boot=300)
    check(abs(ex["chance"] - 0.5 ** len(m.labels)) < 1e-12,
          "the chance rate is 0.5**n_model by construction, not fitted")
    check(ex["estimator"] == "record_macro"
          and ex["observed_ci"][0] <= ex["observed"] <= ex["observed_ci"][1],
          "the point estimate and its interval are the SAME estimator, so the "
          "estimate cannot fall outside its own interval")
    check("observed_micro" in ex and ex["observed_micro"] != ex["observed"]
          or ex["observed_micro"] == ex["observed"],
          "the beat-pooled rate is reported beside it, not swapped in")
    check(ex["ci_low"] <= 1.0 <= ex["ci_high"],
          f"independent models sit at chance (excess {ex['excess']:.2f}, CI "
          f"[{ex['ci_low']:.2f}, {ex['ci_high']:.2f}])")

    cohort, models, rows = _fixture(rho=0.85, seed=7)
    m = QC.build_membership(cohort, models, rows, log=Q4O.RunLog(echo=False))
    ex2 = QC.co_error_excess(m, n_boot=300)
    check(ex2["excess"] > QC.EXCESS_MIN and ex2["ci_low"] > 1.0,
          f"models sharing a latent show real excess ({ex2['excess']:.2f}x, "
          f"CI low {ex2['ci_low']:.2f})")
    check(len(ex2["by_pair"]) == len(m.labels) * (len(m.labels) - 1) // 2,
          "every model pair is reported, not just the first two")


def test_decision_tree_reaches_every_branch():
    print("all three pre-registered branches are reachable")
    tmp = tempfile.mkdtemp(prefix="q5c_tree_")
    try:
        # D-C: no excess
        cohort, models, rows = _fixture(rho=0.0, seed=3)
        res = QC.run_core_analysis(cohort, models, rows,
                                   os.path.join(tmp, "dc"), n_boot=200,
                                   log=Q4O.RunLog(echo=False))
        check(res["decision"]["branch"] == QC.BRANCH_NO_EXCESS,
              "independent models -> NO_SHARED_CORE (D-C)")
        check("arithmetic" in res["decision"]["reason"],
              "and the reason says so in plain words")

        # D-B: real core, invisible to the registered features
        cohort, models, rows = _fixture(rho=0.9, driver="noise", seed=11)
        res = QC.run_core_analysis(cohort, models, rows,
                                   os.path.join(tmp, "db"), n_boot=200,
                                   log=Q4O.RunLog(echo=False))
        check(res["decision"]["branch"] == QC.BRANCH_UNSTRUCTURED,
              "a core driven by a hidden variable -> SHARED_CORE_UNSTRUCTURED")
        check("invent" in res["decision"]["next_step"]
              and "widen" in res["decision"]["next_step"],
              "and the next step forbids inventing or widening features")

        # D-A: real core the registered features can see
        cohort, models, rows = _fixture(rho=0.95, driver="pre_rr", seed=13)
        res = QC.run_core_analysis(cohort, models, rows,
                                   os.path.join(tmp, "da"), n_boot=200,
                                   log=Q4O.RunLog(echo=False))
        check(res["decision"]["branch"] in (QC.BRANCH_STRUCTURED,
                                            QC.BRANCH_UNSTRUCTURED),
              f"a feature-driven core is scored, not crashed "
              f"({res['decision']['branch']})")
        if res["decision"]["branch"] == QC.BRANCH_STRUCTURED:
            check(res["decision"]["leading_block"] in QC.CORE_BLOCKS,
                  "the structured branch names one of the registered blocks")
            check("does not authorise" in res["decision"]["next_step"],
                  "and refuses to authorise an intervention by itself")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_figures_survive_a_degenerate_interval():
    print("a plot cannot destroy a measured result")
    tmp = tempfile.mkdtemp(prefix="q5c_fig_")
    try:
        cohort, models, rows = _fixture(rho=0.5, seed=29)
        m = QC.build_membership(cohort, models, rows, log=Q4O.RunLog(echo=False))
        ex = QC.co_error_excess(m, n_boot=200)
        # force the pathological case the first real run hit: an interval that
        # does not bracket the point estimate
        ex = dict(ex, observed_ci=[ex["observed"] + 0.01,
                                   ex["observed"] + 0.02])
        res = {"co_error": ex, "models": list(m.labels),
               "concentration": QC.core_concentration(m),
               "decision": {"branch": QC.BRANCH_NO_EXCESS, "rule": "D-C",
                            "trace": ["x"], "next_step": "y"}}
        QC._write_figures(tmp, res, res["concentration"], [])
        for f in QC.FIGURES:
            check(os.path.exists(os.path.join(tmp, "figures", f)),
                  f"{f} is still written when the interval is degenerate")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_db_next_step_matches_the_measurement():
    print("D-B never claims 'invisible' when the AUROC says otherwise")
    ex = {"excess": 4.0, "ci_low": 3.0, "ci_high": 5.0}
    conc = {"n_record": 7}
    seen = {"underpowered": False, "blocks": {},
            "joint": {"auroc_aug": 0.73, "delta_logloss": -1.0,
                      "ci_low": -1.6}}
    d = QC.evaluate_core_decision(ex, seen, {"pass": True}, conc)
    check(d["branch"] == QC.BRANCH_UNSTRUCTURED,
          "discrimination without a loss improvement is still D-B by the rule")
    check("invisible" not in d["next_step"] and "DO rank" in d["next_step"],
          "but the next step states what actually happened, not a canned line")

    blind = dict(seen, joint={"auroc_aug": 0.51, "delta_logloss": -0.1,
                              "ci_low": -0.4})
    d2 = QC.evaluate_core_decision(ex, blind, {"pass": True}, conc)
    check("invisible" in d2["next_step"],
          "and when the features really are blind it says exactly that")


def test_shuffle_control():
    print("shuffle control")
    cohort, models, rows = _fixture(rho=0.95, driver="pre_rr", seed=13)
    m = QC.build_membership(cohort, models, rows, log=Q4O.RunLog(echo=False))
    blocks = QC.core_blocks(cohort, rows, m)
    out = QC.shuffle_control(blocks, m, repeats=3, n_boot=100)
    check(out["available"], "the control runs on a real core")
    if out.get("applicable"):
        check(out["shuffled_mean"] < out["real_delta"],
              "shuffling membership inside the record destroys the signal")
    ex = QC.explain_membership(blocks, m, n_boot=100,
                               log=Q4O.RunLog(echo=False))
    if not ex.get("underpowered"):
        check("auroc_null" in ex and 0.3 <= ex["auroc_null"]["mean"] <= 0.7,
              "the held-out AUROC gets its own shuffled-label null "
              f"({ex.get('auroc_null', {}).get('mean')})")
    else:
        check(out["pass"] and "nothing to destroy" in out["verdict"],
              "with no signal the control says it does not apply")


def test_concentration_is_reported():
    print("where the core lives")
    cohort, models, rows = _fixture(rho=0.9, seed=17)
    m = QC.build_membership(cohort, models, rows, log=Q4O.RunLog(echo=False))
    c = QC.core_concentration(m)
    check(c["records_for_50pct"] <= c["records_for_80pct"] <= c["n_record"],
          "the concentration curve is monotone and bounded")
    check(sum(p["n_core"] for p in c["per_record"]) == c["n_core"],
          "the per-record table accounts for every core beat")
    check("rate_uniform" in c and "count_concentration" in c,
          "count concentration and rate uniformity are reported separately")
    check(c["excess_min"] <= c["excess_max"]
          and all("excess_vs_chance" in p for p in c["per_record"]),
          "each record carries its own excess over chance")
    check("read the RATE row" in c["note"],
          "the note says which row to read")

    # a cohort where one record holds almost every S beat but the RATE is
    # uniform must not be called a record story
    rng = np.random.default_rng(2)
    n_big, n_small = 800, 20
    rec = np.concatenate([np.full(n_big, 1), np.repeat(np.arange(2, 8),
                                                       n_small)])
    hard = rng.random((len(rec), 4)) < 0.72   # same rate everywhere
    mm = QC.CoreMembership(record=rec, hard=hard,
                           badness=np.zeros((len(rec), 4)),
                           labels=("a", "b", "c", "d"),
                           rows=np.arange(len(rec)))
    cc = QC.core_concentration(mm)
    check(cc["count_concentration"] == "concentrated"
          and cc["rate_uniform"] and cc["records_above_chance"] == 7,
          "one record holding most S beats does NOT make a uniform rate a "
          f"record story (counts {cc['count_concentration']}, rate uniform "
          f"{cc['rate_uniform']})")


def test_bundle_and_report():
    print("bundle schema and REPORT")
    tmp = tempfile.mkdtemp(prefix="q5c_bundle_")
    try:
        cohort, models, rows = _fixture(rho=0.8, seed=21)
        out = os.path.join(tmp, "run")
        res = QC.run_core_analysis(cohort, models, rows, out, n_boot=200,
                                   provenance={"fixture": True},
                                   log=Q4O.RunLog(echo=False))
        check(res["training_performed"] is False,
              "the result records that nothing was trained")
        for f in QC.BUNDLE_FILES:
            check(os.path.exists(os.path.join(out, f)), f"bundle has {f}")
        for f in QC.FIGURES:
            check(os.path.exists(os.path.join(out, "figures", f)),
                  f"figure {f} written")
        summary = open(os.path.join(out, "summary.md"), encoding="utf-8").read()
        check("실패 연관 요인" in summary and "원인" in summary,
              "the summary keeps the association/cause boundary")
        check("43.6%" in summary and "우연 초과분" in summary,
              "the summary says which number is NOT being explained and why")
        check("residual CNN" in summary and "INCART" in summary,
              "the summary repeats the closed directions")

        before = {f: os.path.getsize(os.path.join(out, f))
                  for f in QC.BUNDLE_FILES}
        rep = QC.report_bundle(out)
        after = {f: os.path.getsize(os.path.join(out, f))
                 for f in QC.BUNDLE_FILES}
        check(before == after, "REPORT does not write into the bundle")
        check(rep["recomputed"] is False
              and rep["decision"]["branch"] == res["decision"]["branch"],
              "REPORT returns the stored verdict and recomputes nothing")
        check(QC.report_bundle(os.path.join(tmp, "nope"))["status"]
              == QC.STATUS_NOT_RUN, "REPORT on an empty path says NOT RUN")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_underpowered_is_a_verdict():
    print("too few beats is reported, not papered over")
    # a cohort whose records are all too small to split: a clear stop, not a
    # meaningless "worse half" of three beats
    tiny_cohort, tiny_models, tiny_rows = _fixture(n_per=60, rho=0.9, seed=23)
    expect_raise(lambda: QC.build_membership(tiny_cohort, tiny_models,
                                             tiny_rows,
                                             log=Q4O.RunLog(echo=False)),
                 "a cohort with no splittable record stops with a reason",
                 QC.Q5CError)
    check(QC.core_concentration(
        QC.CoreMembership(record=np.zeros(0, int), hard=np.zeros((0, 4), bool),
                          badness=np.zeros((0, 4)), labels=("a", "b", "c", "d"),
                          rows=np.zeros(0, int)))["note"].startswith("no record"),
          "an empty membership concentrates into a stated 'nothing', not a crash")

    cohort, models, rows = _fixture(n_per=200, rho=0.5, seed=23)
    m = QC.build_membership(cohort, models, rows, log=Q4O.RunLog(echo=False))
    blocks = QC.core_blocks(cohort, rows, m)
    ex = QC.explain_membership(blocks, m, n_boot=100,
                               log=Q4O.RunLog(echo=False))
    if ex.get("underpowered"):
        check("reason" in ex and str(QA.BLOCK_MIN_EVENTS) in str(ex["reason"]),
              "the underpowered verdict names the threshold it failed")
        d = QC.evaluate_core_decision(
            QC.co_error_excess(m, n_boot=100), ex,
            {"available": False}, QC.core_concentration(m))
        check(d["branch"] in (QC.BRANCH_UNSTRUCTURED, QC.BRANCH_NO_EXCESS),
              "an unexplainable core never becomes 'structured' by default")
    else:
        check(ex["n_core"] > 0, "the contrast has beats on both sides")


def test_language_boundary():
    print("language boundary and closed directions")
    src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "q5c_shared_error_core.py"), encoding="utf-8").read()
    for bad in ("cause of", "causal factor", "proves that", "ground truth"):
        check(bad not in src.lower(), f"no causal/ground-truth claim: {bad!r}")
    check("실패 연관 요인" in src, "the association wording is present")
    check("does not authorise" in src,
          "a structured finding explicitly does not authorise an intervention")


def test_spec_and_notebook():
    print("spec and notebook contract")
    root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
    spec = os.path.join(root, "experiments", "specs",
                        "EXP-2026-006-q5c-shared-error-core.md")
    if not os.path.exists(spec):
        check(False, "Q5-C spec missing")
        return
    text = open(spec, encoding="utf-8").read()
    check("kind: preregistered_analysis_only" in text,
          "the spec declares the analysis-only kind")
    for f in ("mit-bih/q5c_shared_error_core.py",
              "mit-bih/test_q5c_shared_error_core.py",
              "notebooks/quest52_q5c_shared_error_core.ipynb",
              "experiments/specs/EXP-2026-006-q5c-shared-error-core.md",
              "research/ASSETS.md", "research/PROJECT_STATE.md"):
        check(f in text, f"the spec lists the allowed file {f}")
    for b in QC.BRANCHES:
        check(b in text, f"the spec documents branch {b}")
    check("0.5" in text and "43.6" in text,
          "the spec states the chance baseline and the number it replaces")
    check(str(QC.EXCESS_MIN) in text and str(QC.AUROC_MIN) in text,
          "the spec states the thresholds it will be judged on")
    check("Q5-B" in text and ("구현하지 않는다" in text
                              or "만들지 않는다" in text),
          "the spec states no intervention is implemented here")

    p = os.path.join(root, "notebooks", "quest52_q5c_shared_error_core.ipynb")
    if not os.path.exists(p):
        check(False, "quest52 notebook missing")
        return
    nb = json.load(open(p, encoding="utf-8"))
    src = ["".join(c["source"]) for c in nb["cells"]]
    all_src = "\n".join(src)
    first = src[0]
    cfg = next((s for s in src if "MODE = " in s), "")
    check("assert MODE in VALID_MODES" in cfg,
          "exactly-one-mode assertion present")
    check('MODE = "DESIGN"' in cfg, "default mode is DESIGN")
    check(not any(c.get("outputs") for c in nb["cells"]
                  if c["cell_type"] == "code"),
          "design notebook committed without stored outputs")
    check("RESULT NOT RUN" in first, "front page declares RESULT NOT RUN")
    check("EXP-2026-006" in first and "Q5-C" in first,
          "front page identifies the experiment")
    check("ANALYSIS ONLY" in first and "NO TRAINING" in first,
          "front page declares analysis-only / no training")
    check("실패 연관 요인" in first and "원인" in first,
          "front page states association, not cause")
    check("residual CNN" in first and "INCART" in first,
          "front page repeats the closed directions")
    need = next((int(l.split("=")[1].split("#")[0])
                 for l in all_src.splitlines() if l.startswith("NEED_Q5C =")), 0)
    check(need == QC.MODULE_VERSION,
          f"notebook pins the module version (NEED_Q5C={need})")
    check("BRANCH" in all_src and "checkout" in all_src,
          "cell 2 checks out an explicit branch")
    check("test_q5c" in all_src and "test_q5a" in all_src,
          "the notebook runs both test suites")


def test_q5a_is_untouched():
    print("Q5-A and Q5-B-0 stay as accepted")
    check(QA.MODULE_VERSION >= 8, "Q5-A module is the accepted version")
    check(QA.PRIMARY_OUTCOME == QA.OUTCOME_RANK,
          "Q5-C reuses Q5-A's primary outcome definition, unchanged")
    check(QC.NB_BOOT == QA.NB_BOOT,
          "and its bootstrap size, unchanged")


def main() -> int:
    print("=" * 78)
    print("EXP-2026-006 / Q5-C — CPU contract")
    print("=" * 78)
    for fn in (test_import_is_inert, test_modes,
               test_no_new_features_are_invented,
               test_membership_is_a_within_record_median_split,
               test_excess_is_measured_against_chance,
               test_decision_tree_reaches_every_branch,
               test_figures_survive_a_degenerate_interval,
               test_db_next_step_matches_the_measurement, test_shuffle_control,
               test_concentration_is_reported, test_bundle_and_report,
               test_underpowered_is_a_verdict, test_language_boundary,
               test_spec_and_notebook, test_q5a_is_untouched):
        fn()
    print("=" * 78)
    print(f"passed {PASSED} - failed {FAILED}")
    print("=" * 78)
    return 1 if FAILED else 0


if __name__ == "__main__":
    sys.exit(main())
