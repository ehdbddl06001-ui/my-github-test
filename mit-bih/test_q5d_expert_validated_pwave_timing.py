#!/usr/bin/env python3
"""CPU test contract for EXP-2026-007 / Q5-D PREP_DATA-A (ACQUIRE ONLY).

No network, no Drive, no GPU, no wfdb install: a synthetic publisher serves
bytes from a dict and a fake ``wfdb`` module opens them.  The fixtures that
matter are the ones where the honest answer is "stop": a hash that does not
match, a file that is not there, an asset that already exists with different
content.  An acquisition harness that can only ever succeed is not a gate.

    python3 mit-bih/test_q5d_expert_validated_pwave_timing.py
"""
from __future__ import annotations

import hashlib
import io
import json
import os
import re
import shutil
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

_MODULES_BEFORE = set(sys.modules)

import q5d_expert_validated_pwave_timing as QD   # noqa: E402

_MODULES_AFTER = set(sys.modules)

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NOTEBOOK = os.path.join(REPO, "notebooks",
                        "quest47_q5d_expert_validated_pwave_timing.ipynb")
SPEC = os.path.join(REPO, "experiments", "specs",
                    "EXP-2026-007-q5d-expert-validated-pwave-timing-audit.md")
UNTOUCHABLE = (os.path.join(REPO, "research", "ASSETS.md"),
               os.path.join(REPO, "research", "PROJECT_STATE.md"))

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
# Synthetic publisher
# ─────────────────────────────────────────────────────────────────────────────
def _payload(db: str, rel: str) -> bytes:
    """Deterministic per-file bytes — small, but distinct for every path."""
    return (f"{db}/{rel}\n".encode() * 4)


class Publisher:
    """A stand-in PhysioNet tree: URL -> bytes, plus its own SHA256SUMS.txt."""

    def __init__(self, mit_records=None, pw_records=None, corrupt=(),
                 omit=(), sums_extra="", dup_differs=False,
                 drop_sums_entry=()):
        self.blobs = {}
        self.calls = []
        self.mit_records = list(mit_records if mit_records is not None
                                else QD.MITDB_RECORDS_EXPECTED)
        self.pw_records = list(pw_records if pw_records is not None
                               else QD.PWAVE_RECORDS_EXPECTED)
        self.corrupt = set(corrupt)
        self.omit = set(omit)
        self.drop_sums_entry = set(drop_sums_entry)
        for src, records in ((QD.SOURCE_MITDB, self.mit_records),
                             (QD.SOURCE_PWAVE, self.pw_records)):
            table = {}
            for rec in records:
                for ext in src.extensions:
                    rel = f"{rec}{ext}"
                    body = _payload(src.db, rel)
                    if src.db == "pwave" and ext in QD.DUPLICATE_EXTENSIONS:
                        # the shared raw waveform: identical bytes unless the
                        # fixture is deliberately asked for a divergent copy
                        body = _payload("mitdb", rel) if not dup_differs \
                            else _payload("pwave-divergent", rel)
                    table[rel] = body
            table["RECORDS"] = ("\n".join(records) + "\n").encode()
            table["ANNOTATORS"] = b"atr\tAnnotations\n"
            sums_lines = [f"{hashlib.sha256(v).hexdigest()}  {k}"
                          for k, v in sorted(table.items())
                          if (src.db, k) not in self.drop_sums_entry]
            if sums_extra:
                sums_lines.append(sums_extra)
            table["SHA256SUMS.txt"] = ("\n".join(sums_lines) + "\n").encode()
            for rel, body in table.items():
                if (src.db, rel) in self.omit:
                    continue
                served = (body + b"tampered" if (src.db, rel) in self.corrupt
                          else body)
                self.blobs[src.url_for(rel)] = served

    def opener(self, url: str) -> QD.FetchedStream:
        self.calls.append(url)
        if url not in self.blobs:
            raise QD.HttpStatusError(404, url)
        body = self.blobs[url]
        return QD.FetchedStream(final_url=url, reader=io.BytesIO(body),
                                headers={"Content-Length": str(len(body))})


class FakeWfdb:
    """Minimal wfdb surface: rdheader / rdrecord / rdann over the fixture tree."""

    def __init__(self, fs=360.0, sig_len=6000, n_sig=2, ann_n=50,
                 bad_header=(), ann_out_of_range=(), empty_ann=(),
                 unreadable_dat=()):
        self.fs, self.sig_len, self.n_sig, self.ann_n = fs, sig_len, n_sig, ann_n
        self.bad_header = set(bad_header)
        self.ann_out_of_range = set(ann_out_of_range)
        self.empty_ann = set(empty_ann)
        self.unreadable_dat = set(unreadable_dat)

    @staticmethod
    def _rec(base):
        return os.path.basename(base)

    def _require(self, base, ext):
        if not os.path.exists(base + ext):
            raise FileNotFoundError(base + ext)

    def rdheader(self, base):
        self._require(base, ".hea")
        rec = self._rec(base)
        fs = 250.0 if rec in self.bad_header else self.fs
        return type("H", (), {"fs": fs, "n_sig": self.n_sig,
                              "sig_len": self.sig_len,
                              "sig_name": ["MLII", "V5"]})()

    def rdrecord(self, base, sampfrom=0, sampto=None, channels=None):
        self._require(base, ".dat")
        if self._rec(base) in self.unreadable_dat:
            raise ValueError("corrupt signal block")
        n = int(sampto or self.sig_len)
        return type("R", (), {"p_signal": [[0.0]] * n})()

    def rdann(self, base, ext):
        self._require(base, "." + ext)
        rec = self._rec(base)
        if rec in self.empty_ann:
            return type("A", (), {"sample": []})()
        step = max(1, self.sig_len // max(1, self.ann_n))
        samples = list(range(0, self.sig_len, step))[: self.ann_n]
        if rec in self.ann_out_of_range:
            samples[-1] = self.sig_len + 999
        return type("A", (), {"sample": samples})()


class _AmbiguousArray(list):
    """A sequence that raises on truthiness — exactly what numpy arrays do.

    Measured on Colab 2026-08-09: ``wfdb.rdann(...).sample`` is a numpy array,
    so ``arr or []`` raised "truth value of an array ... is ambiguous" inside
    the try/except and every one of the 60 records was misreported as
    OPEN_FAILED while its bytes were perfectly fine.
    """

    def __bool__(self):
        raise ValueError("The truth value of an array with more than one "
                         "element is ambiguous. Use a.any() or a.all()")


class ArrayWfdb(FakeWfdb):
    """FakeWfdb that returns array-like objects instead of plain lists."""

    def rdheader(self, base):
        hdr = super().rdheader(base)
        hdr.sig_name = _AmbiguousArray(hdr.sig_name)
        return hdr

    def rdann(self, base, ext):
        ann = super().rdann(base, ext)
        ann.sample = _AmbiguousArray(ann.sample)
        return ann


def _numpy_wfdb(**kw):
    """The same fixture backed by real numpy arrays, when numpy is available."""
    try:
        import numpy as np
    except ImportError:
        return None

    class NumpyWfdb(FakeWfdb):
        def rdheader(self, base):
            hdr = super().rdheader(base)
            hdr.sig_name = np.array(hdr.sig_name)
            return hdr

        def rdrecord(self, base, sampfrom=0, sampto=None, channels=None):
            rec = super().rdrecord(base, sampfrom, sampto, channels)
            rec.p_signal = np.asarray(rec.p_signal)
            return rec

        def rdann(self, base, ext):
            ann = super().rdann(base, ext)
            ann.sample = np.asarray(ann.sample, dtype=int)
            return ann

    return NumpyWfdb(**kw)


def _run(tmp, publisher=None, wfdb=None, timestamp="20260809T2000", **kw):
    pub = publisher or Publisher()
    return QD.run_prep_data_acquire(
        tmp, timestamp, opener=pub.opener, wfdb_module=wfdb or FakeWfdb(),
        log=QD.RunLog(echo=False), sleeper=lambda s: None, **kw)


# ─────────────────────────────────────────────────────────────────────────────
def test_import_is_inert():
    print("import performs no download, no mount, no write")
    new = {m.split(".")[0] for m in (_MODULES_AFTER - _MODULES_BEFORE)}
    check(not ({"torch", "tensorflow", "keras"} & new),
          "no training framework imported")
    check("google" not in new, "no google.colab / Drive mount at import")
    check(not os.path.exists(QD.DRIVE_ASSET_REL),
          "importing the module created no asset directory")
    info = QD.assert_acquire_only()
    check(info["acquire_only"] and not info["training_performed"]
          and not info["delineation_performed"]
          and not info["analysis_performed"],
          "the module contains no training / delineation / analysis call")
    check(QD.EXPERIMENT_ID == "EXP-2026-007" and QD.ARM_ID == "Q5-D"
          and QD.SUBSTAGE == "PREP_DATA-A ACQUIRE_ONLY",
          "identity is EXP-2026-007 / Q5-D / PREP_DATA-A ACQUIRE_ONLY")
    check(QD.STATUS == "PREP_DATA DESIGN / RESULT NOT RUN",
          "the default status says the result has not been run")


def test_modes():
    print("modes: only the three authorised ones exist")
    check(QD.MODES == ("DESIGN", "PREP_DATA_ACQUIRE", "PREP_DATA_REPORT"),
          "MODES is exactly DESIGN / PREP_DATA_ACQUIRE / PREP_DATA_REPORT")
    check(QD.resolve_mode("design") == "DESIGN", "mode resolution is case-free")
    for bad in QD.FORBIDDEN_MODES:
        expect_raise(lambda b=bad: QD.resolve_mode(b),
                     f"mode {bad} is refused as an unauthorised stage",
                     QD.Q5DError)
    expect_raise(lambda: QD.resolve_mode("PREP_DATA"), "unknown mode refused",
                 QD.Q5DError)


def test_versioned_urls_only():
    print("only pinned versioned PhysioNet URLs are accepted")
    ok = "https://physionet.org/files/mitdb/1.0.0/100.dat"
    check(QD.assert_versioned_url(ok) == ok, "a pinned versioned URL passes")
    for bad in ("https://physionet.org/files/mitdb/latest/100.dat",
                "https://physionet.org/files/latest/1.0.0/100.dat",
                "https://physionet.org/content/mitdb/1.0.0/100.dat",
                "http://physionet.org/files/mitdb/1.0.0/100.dat",
                "https://example.com/files/mitdb/1.0.0/100.dat",
                "https://physionet.org/files/mitdb/1.0.0/../../etc/passwd"):
        expect_raise(lambda b=bad: QD.assert_versioned_url(b),
                     f"refused: {bad}", QD.Q5DError)
    check(QD.SOURCE_MITDB.files_url.endswith("/mitdb/1.0.0/")
          and QD.SOURCE_MITDB.doi == "10.13026/C2F305",
          "mitdb is pinned to 1.0.0 with DOI 10.13026/C2F305")
    check(QD.SOURCE_PWAVE.files_url.endswith("/pwave/1.0.0/")
          and QD.SOURCE_PWAVE.doi == "10.13026/C2108F",
          "pwave is pinned to 1.0.0 with DOI 10.13026/C2108F")
    expect_raise(lambda: QD.download_file(
        "https://physionet.org/files/mitdb/latest/100.dat", "/tmp/x"),
        "download_file itself refuses a moving alias", QD.Q5DError)


def test_sha_parser_and_path_normalisation():
    print("publisher SHA parser and relative-path normalisation")
    text = ("\n".join([
        "# comment line",
        "aa" * 32 + "  100.dat",
        "bb" * 32 + " *./101.dat",
        "cc" * 32 + "  mitdb/1.0.0/102.dat",
        "dd" * 32 + "  sub/100.dat",
    ]) + "\n")
    sums = QD.parse_sha256sums(text, "mitdb", "1.0.0")
    check(sums["100.dat"] == "aa" * 32, "'hash  path' form parses")
    check(sums["101.dat"] == "bb" * 32, "'hash *./path' form normalises")
    check(sums["102.dat"] == "cc" * 32, "the db/version prefix is stripped")
    check("sub/100.dat" in sums and sums["sub/100.dat"] == "dd" * 32
          and sums["100.dat"] != sums["sub/100.dat"],
          "same basename in another directory stays a separate entry")
    check(QD.expected_sha_for(sums, "100.dat") == "aa" * 32,
          "lookup is by exact relative path")
    check(QD.expected_sha_for(sums, "999.dat") is None,
          "an unlisted path has no hash (never a basename fallback)")
    expect_raise(lambda: QD.parse_sha256sums("garbage line\n"),
                 "an unparsable checksum line is a hard error", QD.Q5DError)
    expect_raise(lambda: QD.parse_sha256sums(""),
                 "an empty checksum table is a hard error", QD.Q5DError)
    expect_raise(lambda: QD.parse_sha256sums(
        "aa" * 32 + "  100.dat\n" + "bb" * 32 + "  100.dat\n"),
        "the same path with two different hashes is a hard error", QD.Q5DError)
    check(QD.normalize_rel_path("./x/y.dat") == "x/y.dat",
          "leading ./ is stripped without collapsing directories")
    expect_raise(lambda: QD.normalize_rel_path("../secrets"),
                 "a path-escaping checksum entry is refused", QD.Q5DError)
    recs = QD.parse_records("100\n101\n\n# note\n102.hea\n100\n")
    check(recs == ["100", "101", "102"],
          "RECORDS parsing keeps order, drops blanks/comments/duplicates")


def test_required_file_table():
    print("required-file table covers every record and extension")
    reqs = QD.required_files(QD.SOURCE_MITDB, QD.MITDB_RECORDS_EXPECTED)
    recs = {r.record for r in reqs if r.kind == "record"}
    check(len(QD.MITDB_RECORDS_EXPECTED) == 48, "48 MIT-BIH records expected")
    check(len(QD.PWAVE_RECORDS_EXPECTED) == 12, "12 P-wave records expected")
    check(recs == set(QD.MITDB_RECORDS_EXPECTED),
          "every declared MIT record is required")
    check(len([r for r in reqs if r.kind == "record"]) == 48 * 3,
          "48 records x .dat/.hea/.atr = 144 required record files")
    check(QD.SOURCE_PWAVE.extensions == (".dat", ".hea", ".pwave"),
          "the pwave source requires .dat/.hea/.pwave")
    check(all(r.url.startswith(QD.SOURCE_MITDB.files_url) for r in reqs),
          "every URL is built from the pinned versioned base")


def test_happy_path_verified():
    print("complete, hash-clean acquisition -> PREP_DATA_ACQUIRED_VERIFIED")
    tmp = tempfile.mkdtemp()
    try:
        out = _run(tmp)
        dec = out["decision"]
        check(dec["decision"] == QD.DECISION_VERIFIED,
              "decision is PREP_DATA_ACQUIRED_VERIFIED")
        check(all(g["pass"] for g in dec["gates"]), "every gate passed")
        check(dec["first_stopping_reason"] is None, "no stopping reason")
        inv = {i["database"]: i for i in out["inventories"]}
        check(inv["mitdb"]["n_records_declared"] == 48
              and inv["mitdb"]["records_match"],
              "official RECORDS shows 48/48 MIT-BIH records")
        check(inv["pwave"]["n_records_declared"] == 12
              and inv["pwave"]["records_match"],
              "official RECORDS shows 12/12 P-wave records")
        check(inv["mitdb"]["counts"][QD.FILE_VERIFIED] == 144 + 3,
              "144 record files + 3 metadata files verified for mitdb")
        check(inv["pwave"]["counts"][QD.FILE_VERIFIED] == 36 + 3,
              "36 record files + 3 metadata files verified for pwave")
        check(out["result"]["wfdb_records_ok"] == 60
              and out["result"]["wfdb_records_checked"] == 60,
              "all 48 + 12 records open under WFDB (no record skipped)")
        check(dec["training_performed"] is False
              and dec["delineation_performed"] is False
              and dec["analysis_performed"] is False,
              "the decision records that nothing scientific was run")
        check(dec["decision_is_scientific_result"] is False,
              "an acquisition decision is not a scientific result")
        audit = out["audit_dir"]
        missing = [f for f in QD.AUDIT_FILES
                   if not os.path.exists(os.path.join(audit, f))]
        check(not missing, f"the audit bundle is complete ({len(QD.AUDIT_FILES)} files)")
        check(not any(p.endswith(QD.PARTIAL_SUFFIX)
                      for _, _, fs in os.walk(tmp) for p in fs),
              "no .partial file survives a clean run")
        dup = out["duplicates"]
        check(len(dup) == 12 * 2
              and all(d["status"] == "IDENTICAL" for d in dup),
              "the 12 duplicated waveforms are compared, not substituted")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_hash_mismatch_stops():
    print("a publisher hash mismatch stops the run and names the file")
    tmp = tempfile.mkdtemp()
    try:
        out = _run(tmp, Publisher(corrupt={("mitdb", "119.dat")}))
        dec = out["decision"]
        check(dec["decision"] == QD.DECISION_MISMATCH,
              "decision is INPUT_ABSENT_OR_MISMATCH")
        rows = [f for i in out["inventories"] for f in i["files"]
                if f["rel_path"] == "119.dat" and f["database"] == "mitdb"]
        check(rows and rows[0]["status"] == QD.FILE_HASH_MISMATCH,
              "119.dat is reported HASH_MISMATCH")
        check(rows[0]["publisher_sha256"] and rows[0]["observed_sha256"]
              and rows[0]["publisher_sha256"] != rows[0]["observed_sha256"],
              "both the expected and the observed hash are reported")
        final = os.path.join(tmp, QD.SOURCE_SUBDIR,
                             QD.SOURCE_MITDB.dir_name, "119.dat")
        check(not os.path.exists(final),
              "a mismatching download is never promoted to its real name")
        check(os.path.exists(final + QD.PARTIAL_SUFFIX),
              "the partial file is kept for inspection, not deleted")
        fr = dec["first_stopping_reason"]
        check(fr and fr["gate"] == "mitdb_checksums",
              "the first stopping reason is the mitdb checksum gate")
        check(any(e.get("rel_path") == "119.dat" for e in fr["evidence"]),
              "the stopping evidence names the exact file")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_missing_required_extension_stops():
    print("a missing required extension stops the run")
    tmp = tempfile.mkdtemp()
    try:
        out = _run(tmp, Publisher(omit={("pwave", "231.pwave")}))
        dec = out["decision"]
        check(dec["decision"] == QD.DECISION_MISMATCH,
              "decision is INPUT_ABSENT_OR_MISMATCH")
        rows = [f for i in out["inventories"] for f in i["files"]
                if f["rel_path"] == "231.pwave"]
        check(rows and rows[0]["status"] == QD.FILE_MISSING,
              "231.pwave is reported MISSING (HTTP 404, not retried away)")
        recs = QD.record_inventory(out["inventories"], out["wfdb"],
                                   out["duplicates"])
        row = [r for r in recs if r["database"] == "pwave"
               and r["record"] == "231"][0]
        check(not row["all_extensions_verified"],
              "the per-record table shows record 231 incomplete")
        ok_rows = [r for r in recs if r["database"] == "pwave"
                   and r["record"] in ("100", "101")]
        check(all(r["all_extensions_verified"] for r in ok_rows),
              "records 100/101 still pass — and do NOT make the run pass")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_missing_publisher_hash_is_not_verified():
    print("a file the publisher does not checksum is never called verified")
    tmp = tempfile.mkdtemp()
    try:
        out = _run(tmp, Publisher(drop_sums_entry={("mitdb", "100.atr")}))
        rows = [f for i in out["inventories"] for f in i["files"]
                if f["rel_path"] == "100.atr" and f["database"] == "mitdb"]
        check(rows and rows[0]["status"] == QD.FILE_HASH_MISMATCH,
              "an unlisted path cannot reach VERIFIED")
        check("no publisher" in str(rows[0]["detail"]).lower(),
              "the reason given is the missing publisher entry")
        final = os.path.join(tmp, QD.SOURCE_SUBDIR,
                             QD.SOURCE_MITDB.dir_name, "100.atr")
        check(not os.path.exists(final) and
              os.path.exists(final + QD.PARTIAL_SUFFIX),
              "an unverifiable download stays a partial file")
        check(out["decision"]["decision"] == QD.DECISION_MISMATCH,
              "decision is INPUT_ABSENT_OR_MISMATCH")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_existing_verified_asset_is_reused_not_rewritten():
    print("an existing verified asset is read-verified, never rewritten")
    tmp = tempfile.mkdtemp()
    try:
        first = _run(tmp)
        check(first["decision"]["decision"] == QD.DECISION_VERIFIED,
              "first acquisition verifies")
        target = os.path.join(tmp, QD.SOURCE_SUBDIR,
                              QD.SOURCE_MITDB.dir_name, "100.dat")
        before = (os.path.getmtime(target), QD.sha256_file(target))
        second = _run(tmp, timestamp="20260809T2100")
        after = (os.path.getmtime(target), QD.sha256_file(target))
        check(before == after, "the existing file was not rewritten")
        rows = [f for i in second["inventories"] for f in i["files"]
                if f["rel_path"] == "100.dat" and f["database"] == "mitdb"]
        check(rows and rows[0]["action"] == "reused_existing"
              and rows[0]["status"] == QD.FILE_VERIFIED,
              "it is reported as reused_existing / VERIFIED")
        check(second["decision"]["decision"] == QD.DECISION_VERIFIED,
              "a re-run over a complete verified asset still verifies")
        check(second["staging_root"] is None
              or not os.path.isdir(str(second["staging_root"]))
              or not os.listdir(str(second["staging_root"])),
              "nothing needed staging when the asset was already complete")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_existing_conflicting_asset_stops():
    print("an existing path with different content is a hard stop")
    tmp = tempfile.mkdtemp()
    try:
        _run(tmp)
        target = os.path.join(tmp, QD.SOURCE_SUBDIR,
                              QD.SOURCE_MITDB.dir_name, "103.hea")
        with open(target, "wb") as fh:
            fh.write(b"somebody else's bytes\n")
        conflicting = QD.sha256_file(target)
        out = _run(tmp, timestamp="20260809T2200")
        check(out["decision"]["decision"] == QD.DECISION_MISMATCH,
              "decision is INPUT_ABSENT_OR_MISMATCH")
        rows = [f for i in out["inventories"] for f in i["files"]
                if f["rel_path"] == "103.hea" and f["database"] == "mitdb"]
        check(rows and rows[0]["action"] == QD.CONFLICT_CODE,
              "the row is flagged EXISTING_ASSET_CONFLICT")
        check(QD.sha256_file(target) == conflicting,
              "the conflicting file was NOT overwritten or deleted")
        gates = {g["gate"]: g for g in out["decision"]["gates"]}
        check(not gates["mitdb_no_conflict"]["pass"],
              "the no-conflict gate fails")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_partial_existing_asset_goes_to_staging():
    print("a pre-existing incomplete asset is staged, never topped up in place")
    tmp = tempfile.mkdtemp()
    try:
        _run(tmp)
        src_dir = os.path.join(tmp, QD.SOURCE_SUBDIR,
                               QD.SOURCE_PWAVE.dir_name)
        os.remove(os.path.join(src_dir, "222.pwave"))
        out = _run(tmp, timestamp="20260809T2300")
        inv = {i["database"]: i for i in out["inventories"]}
        check(inv["pwave"]["preexisting_asset"],
              "the pwave asset directory is recognised as pre-existing")
        check(inv["pwave"]["existing_asset_partial"],
              "its partial state is recorded in the inventory")
        staged = os.path.join(str(out["staging_root"]), QD.SOURCE_SUBDIR,
                              QD.SOURCE_PWAVE.dir_name, "222.pwave")
        check(os.path.exists(staged),
              "the missing file was fetched into a timestamped staging path")
        check(not os.path.exists(os.path.join(src_dir, "222.pwave")),
              "the immutable asset directory was not silently completed")
        check(out["decision"]["decision"] == QD.DECISION_MISMATCH,
              "a partial asset stops for review rather than passing")
        gates = {g["gate"]: g for g in out["decision"]["gates"]}
        check(not gates["pwave_asset_complete"]["pass"],
              "the asset-complete gate names the partial state")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_record_list_mismatch_stops():
    print("a record list that is not the official one stops the run")
    tmp = tempfile.mkdtemp()
    try:
        short = list(QD.MITDB_RECORDS_EXPECTED)[:40]
        out = _run(tmp, Publisher(mit_records=short))
        gates = {g["gate"]: g for g in out["decision"]["gates"]}
        check(not gates["mitdb_record_list"]["pass"],
              "40 declared records fails the 48-record gate")
        check(out["decision"]["decision"] == QD.DECISION_MISMATCH,
              "decision is INPUT_ABSENT_OR_MISMATCH")
        check(gates["mitdb_record_list"]["evidence"],
              "the missing record ids are listed as evidence")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    tmp = tempfile.mkdtemp()
    try:
        out = _run(tmp, Publisher(pw_records=["100", "101", "103"]))
        gates = {g["gate"]: g for g in out["decision"]["gates"]}
        check(not gates["pwave_record_list"]["pass"],
              "3 declared P-wave records fails the 12-record gate")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_wfdb_open_failures():
    print("WFDB open failures are verdicts, not warnings")
    tmp = tempfile.mkdtemp()
    try:
        out = _run(tmp, wfdb=FakeWfdb(bad_header={"212"}))
        rows = [r for r in out["wfdb"] if r["record"] == "212"
                and r["database"] == "mitdb"]
        check(rows and rows[0]["status"] == QD.FILE_OPEN_FAILED
              and not rows[0]["fs_ok"],
              "a 250 Hz header fails the 360 Hz check")
        check(out["decision"]["decision"] == QD.DECISION_MISMATCH,
              "one bad record fails the whole WFDB gate")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    tmp = tempfile.mkdtemp()
    try:
        out = _run(tmp, wfdb=FakeWfdb(unreadable_dat={"207"}))
        rows = [r for r in out["wfdb"] if r["record"] == "207"
                and r["database"] == "mitdb"]
        check(rows and rows[0]["status"] == QD.FILE_OPEN_FAILED
              and rows[0]["rdheader_ok"] and not rows[0]["dat_read_ok"],
              "a header that parses but a .dat that will not read is OPEN_FAILED")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    tmp = tempfile.mkdtemp()
    try:
        out = _run(tmp, wfdb=FakeWfdb(empty_ann={"233"}))
        rows = [r for r in out["wfdb"] if r["record"] == "233"
                and r["database"] == "mitdb"]
        check(rows and rows[0]["status"] == QD.FILE_OPEN_FAILED
              and rows[0]["ann_count"] == 0,
              "an empty .atr annotation set fails (count must exceed zero)")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_wfdb_array_returns():
    print("array-typed wfdb returns are read, not misreported as OPEN_FAILED")
    tmp = tempfile.mkdtemp()
    try:
        out = _run(tmp, wfdb=ArrayWfdb())
        check(out["result"]["wfdb_records_ok"] == 60,
              "60/60 records open when sample/sig_name raise on truthiness")
        check(out["decision"]["decision"] == QD.DECISION_VERIFIED,
              "decision is PREP_DATA_ACQUIRED_VERIFIED")
        row = [r for r in out["wfdb"] if r["record"] == "100"
               and r["database"] == "mitdb"][0]
        check(row["ann_count"] > 0 and row["ann_in_range"],
              "the annotation count and range come through as numbers")
        check(row["sig_names"] and "|" in row["sig_names"],
              "lead names survive the array round trip")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    npw = _numpy_wfdb()
    if npw is None:
        print("  (numpy unavailable — array-like fixture already covered it)")
        return
    tmp = tempfile.mkdtemp()
    try:
        out = _run(tmp, wfdb=npw)
        check(out["result"]["wfdb_records_ok"] == 60,
              "60/60 records open against real numpy arrays too")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    check(QD._as_list(None) == [] and QD._as_list((1, 2)) == [1, 2]
          and QD._as_list(_AmbiguousArray([3])) == [3],
          "_as_list converts without ever testing truthiness")


def test_failed_run_is_archived():
    print("every acquisition keeps an immutable copy, including a stopped one")
    tmp = tempfile.mkdtemp()
    try:
        # The real recovery path: downloads all verified, the WFDB check stopped
        # the run, and the fixed re-run reuses the complete asset from disk.
        bad = _run(tmp, wfdb=FakeWfdb(bad_header={"212"}),
                   timestamp="20260809T2000")
        check(bad["decision"]["decision"] == QD.DECISION_MISMATCH,
              "the first run stops with INPUT_ABSENT_OR_MISMATCH")
        first = str(bad["run_dir"])
        check(os.path.isdir(first),
              "its bundle is archived under audit/runs/<timestamp>/")
        with open(os.path.join(first, "decision.json"), encoding="utf-8") as fh:
            archived = json.load(fh)
        good = _run(tmp, timestamp="20260809T2100")
        check(good["decision"]["decision"] == QD.DECISION_VERIFIED,
              "the fixed re-run verifies without re-downloading anything")
        check(all(f["action"].startswith("reused_existing")
                  for i in good["inventories"] for f in i["files"]),
              "every file of the re-run came from the existing asset")
        with open(os.path.join(first, "decision.json"), encoding="utf-8") as fh:
            still = json.load(fh)
        check(still == archived and still["decision"] == QD.DECISION_MISMATCH,
              "the stopped run's evidence survives the successful re-run")
        rep = QD.report_bundle(tmp)
        check(rep["archived_runs"] == ["20260809T2000", "20260809T2100"],
              "the report lists both archived runs")
        check(rep["decision"] == QD.DECISION_VERIFIED,
              "audit/ itself holds the latest bundle")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_pwave_annotation_range():
    print("P-wave annotation samples must fall inside the record")
    tmp = tempfile.mkdtemp()
    try:
        out = _run(tmp, wfdb=FakeWfdb(ann_out_of_range={"214"}))
        rows = [r for r in out["wfdb"] if r["record"] == "214"]
        pw = [r for r in rows if r["database"] == "pwave"]
        check(pw and pw[0]["status"] == QD.FILE_OPEN_FAILED
              and not pw[0]["ann_in_range"],
              "an out-of-range pwave sample is OPEN_FAILED")
        check(pw and pw[0]["ann_ext"] == "pwave",
              "the pwave source is checked with the pwave annotator")
        mit = [r for r in out["wfdb"] if r["database"] == "mitdb"]
        check(all(r["ann_ext"] == "atr" for r in mit),
              "the mitdb source is checked with the atr annotator")
        check(out["decision"]["decision"] == QD.DECISION_MISMATCH,
              "decision is INPUT_ABSENT_OR_MISMATCH")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_duplicate_waveform_reported_not_substituted():
    print("duplicated raw waveforms are compared and reported, never swapped")
    tmp = tempfile.mkdtemp()
    try:
        out = _run(tmp, Publisher(dup_differs=True))
        dup = [d for d in out["duplicates"] if d["extension"] == ".dat"]
        check(dup and all(d["status"] == "DIFFERENT" for d in dup),
              "differing copies are reported as DIFFERENT")
        check(all(d["mitdb_sha256"] and d["pwave_sha256"]
                  and d["mitdb_sha256"] != d["pwave_sha256"] for d in dup),
              "both hashes are recorded side by side")
        mit = os.path.join(tmp, QD.SOURCE_SUBDIR, QD.SOURCE_MITDB.dir_name,
                           "100.dat")
        pw = os.path.join(tmp, QD.SOURCE_SUBDIR, QD.SOURCE_PWAVE.dir_name,
                          "100.dat")
        check(QD.sha256_file(mit) != QD.sha256_file(pw),
              "neither tree was rewritten to match the other")
        n_dup = 12 * len(QD.DUPLICATE_EXTENSIONS)
        check(out["decision"]["duplicate_waveform_summary"]["different"]
              == n_dup,
              f"the decision counts all {n_dup} differing waveform files")
        check(out["decision"]["decision"] == QD.DECISION_VERIFIED,
              "a difference is reported for review; the publisher hashes "
              "themselves still gate the decision")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_retry_budget():
    print("network retries stop at three attempts; 404/403 do not retry")
    calls = []

    def flaky(url):
        calls.append(url)
        raise QD.NetworkError("connection reset")

    tmp = tempfile.mkdtemp()
    try:
        expect_raise(lambda: QD.download_file(
            QD.SOURCE_MITDB.url_for("100.dat"),
            os.path.join(tmp, "100.dat"), expected_sha="ab" * 32,
            opener=flaky, sleeper=lambda s: None),
            "a persistent network error raises after the retry budget",
            QD.Q5DError)
        check(len(calls) == QD.MAX_RETRIES == 3,
              f"exactly {QD.MAX_RETRIES} attempts were made ({len(calls)})")

        hard = []

        def not_found(url):
            hard.append(url)
            raise QD.HttpStatusError(404, url)

        expect_raise(lambda: QD.download_file(
            QD.SOURCE_MITDB.url_for("100.dat"),
            os.path.join(tmp, "100.dat"), expected_sha="ab" * 32,
            opener=not_found, sleeper=lambda s: None),
            "a 404 stops immediately", QD.Q5DError)
        check(len(hard) == 1, "a 404 is not retried")
        check(QD.is_retryable(QD.HttpStatusError(503, "u"))
              and not QD.is_retryable(QD.HttpStatusError(403, "u")),
              "5xx is retryable, 403 is not")
        check(not os.path.exists(os.path.join(tmp, "100.dat"))
              and not os.path.exists(os.path.join(tmp,
                                                  "100.dat" + QD.PARTIAL_SUFFIX)),
              "a failed download leaves no promoted file behind")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_not_run_vs_verified():
    print("PREP_DATA_RESULT_NOT_RUN is distinct from an executed acquisition")
    tmp = tempfile.mkdtemp()
    try:
        rep = QD.report_bundle(tmp)
        check(rep["decision"] == QD.DECISION_NOT_RUN,
              "an empty asset root reports PREP_DATA_RESULT_NOT_RUN")
        out = _run(tmp)
        rep = QD.report_bundle(tmp)
        check(rep["decision"] == QD.DECISION_VERIFIED and not rep["recomputed"],
              "after a run the stored bundle reports VERIFIED without recomputing")
        check(rep["summary"].strip().startswith("# EXP-2026-007"),
              "the stored summary is replayed as saved")
        os.remove(os.path.join(out["audit_dir"], "decision.json"))
        rep = QD.report_bundle(tmp)
        check(rep["decision"] == QD.DECISION_NOT_RUN and rep["missing_audit_files"],
              "an incomplete bundle is NOT_RUN, not a silent pass")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_bundle_schema():
    print("decision bundle and manifest carry the required fields")
    tmp = tempfile.mkdtemp()
    try:
        out = _run(tmp)
        audit = out["audit_dir"]
        with open(os.path.join(audit, "decision.json"), encoding="utf-8") as fh:
            dec = json.load(fh)
        for key in ("experiment_id", "arm_id", "substage", "decision", "gates",
                    "first_stopping_reason", "permitted_next_step",
                    "training_performed", "delineation_performed",
                    "analysis_performed"):
            check(key in dec, f"decision.json has '{key}'")
        check(dec["decision"] in QD.DECISIONS,
              "the decision code is one of the three declared codes")
        with open(os.path.join(audit, "asset_manifest.json"),
                  encoding="utf-8") as fh:
            man = json.load(fh)
        for key in ("experiment_id", "timestamp", "asset_root", "environment",
                    "sources", "file_hashes", "duplicate_waveform_comparison"):
            check(key in man, f"asset_manifest.json has '{key}'")
        src = {s["database"]: s for s in man["sources"]}
        for db in ("mitdb", "pwave"):
            s = src[db]
            check(all(s.get(k) for k in ("version", "doi", "license_name",
                                         "files_url", "sha256sums_sha256")),
                  f"{db}: version, DOI, license, URL and table hash are stored")
        check(all(h["observed_sha256"] for h in man["file_hashes"]),
              "every acquired file carries an observed SHA-256")
        check(len(man["file_hashes"]) == 147 + 39,
              "the manifest hashes every required file of both sources")
        with open(os.path.join(audit, "config.json"), encoding="utf-8") as fh:
            cfg = json.load(fh)
        check(set(cfg["not_performed"]) >= {"p_wave_delineation", "s_pr_auc",
                                            "sham_permutation",
                                            "model_training"},
              "config.json states what this stage does not do")
        with open(os.path.join(audit, "checksum_report.csv"),
                  encoding="utf-8") as fh:
            head = fh.readline()
        for col in ("database", "record", "extension", "source_url",
                    "final_url", "observed_bytes", "publisher_sha256",
                    "observed_sha256", "status"):
            check(col in head, f"checksum_report.csv has column '{col}'")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_writes_stay_inside_the_asset_root():
    print("nothing is ever written outside the asset root")
    tmp = tempfile.mkdtemp()
    try:
        expect_raise(lambda: QD.safe_join(tmp, "../escape.txt"),
                     "a path escaping the root is refused", QD.Q5DError)
        expect_raise(lambda: QD.safe_join(tmp, "a/../../escape.txt"),
                     "a nested escape is refused", QD.Q5DError)
        check(QD.safe_join(tmp, "source/mitdb-1.0.0/100.dat").startswith(tmp),
              "a normal relative path stays inside the root")
        before = sorted(os.listdir(os.path.dirname(tmp)))
        _run(tmp)
        after = sorted(os.listdir(os.path.dirname(tmp)))
        check(before == after, "the run created nothing beside the asset root")
        tops = sorted(os.listdir(tmp))
        check(set(tops) <= {QD.SOURCE_SUBDIR, QD.AUDIT_SUBDIR}
              or all(t.startswith(QD.STAGING_PREFIX) or
                     t in (QD.SOURCE_SUBDIR, QD.AUDIT_SUBDIR) for t in tops),
              f"the asset root holds only source/ audit/ (and staging): {tops}")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_no_model_or_result_bundle_is_read():
    print("no probability, checkpoint or earlier Q5 bundle is touched")
    with open(QD.__file__, encoding="utf-8") as fh:
        # The forbidden-token table itself spells these names in split form; it
        # is the guard, not a use, so those lines are excluded from the scan.
        lines = [ln.lower() for ln in fh if '" + "' not in ln]
    src = "".join(lines)
    for token in ("v10pkg", "mamba_data", "core_membership", "state_dict",
                  "baseline_freeze", "probs.npy", "ens.npz"):
        check(token not in src, f"the module never references {token}")
    check("import numpy" not in src, "numpy is not imported at module scope")
    check("\nimport wfdb" not in src,
          "wfdb is imported lazily inside the check, not at module scope")
    tmp = tempfile.mkdtemp()
    try:
        opened = []
        real_open = io.open

        def watched(path, *a, **kw):
            opened.append(str(path))
            return real_open(path, *a, **kw)

        io.open = watched
        try:
            _run(tmp)
        finally:
            io.open = real_open
        bad = [p for p in opened
               if any(t in p.lower() for t in ("v10", "mamba", "runs/",
                                               "baseline_pkgs", ".npz"))]
        check(not bad, f"no run bundle or model file was opened ({bad[:3]})")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_untouchable_repo_files():
    print("research/ASSETS.md and research/PROJECT_STATE.md are untouched")
    before = {p: QD.sha256_file(p) for p in UNTOUCHABLE if os.path.exists(p)}
    check(len(before) == 2, "both intake documents exist to be protected")
    tmp = tempfile.mkdtemp()
    try:
        _run(tmp)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    after = {p: QD.sha256_file(p) for p in before}
    check(before == after, "an acquisition run does not modify either file")
    with open(QD.__file__, encoding="utf-8") as fh:
        src = fh.read()
    check("ASSETS.md" not in src and "PROJECT_STATE.md" not in src,
          "the module does not even name the intake documents as write targets")


def test_notebook_contract():
    print("notebook: default mode DESIGN and no later-stage execution path")
    check(os.path.exists(NOTEBOOK), f"notebook exists: {os.path.basename(NOTEBOOK)}")
    if not os.path.exists(NOTEBOOK):
        return
    with open(NOTEBOOK, encoding="utf-8") as fh:
        nb = json.load(fh)
    code = ["".join(c["source"]) for c in nb["cells"]
            if c["cell_type"] == "code"]
    joined = "\n".join(code)
    check('MODE = "DESIGN"' in joined, "the default mode assignment is DESIGN")
    check('VALID_MODES = ("DESIGN", "PREP_DATA_ACQUIRE", "PREP_DATA_REPORT")'
          in joined, "the notebook allows only the three authorised modes")
    guarded = re.findall(r'MODE\s*==\s*"([A-Z_]+)"', joined)
    check(guarded and all(m in QD.MODES for m in guarded),
          f"every cell guard names an authorised mode ({sorted(set(guarded))})")
    # The mandated banner is the one place a forbidden word may appear as text.
    body = joined.replace(QD.NO_SCIENCE_BANNER, "")
    for banned in ("QUALIFY", "ANALYZE", "TRAIN", "MEASURE"):
        check(banned not in body,
              f"no code cell mentions a {banned} execution path")
    check(QD.NO_SCIENCE_BANNER in joined,
          "the notebook prints the NO TRAINING / NO SCIENTIFIC ANALYSIS banner")
    for banned in ("delineate", "prauc", "pr_auc", "permutation", "torch",
                   "v10pkg", "mamba_data"):
        check(banned not in joined.lower(),
              f"no code cell performs '{banned}'")
    check(all(len(c.get("outputs", [])) == 0 for c in nb["cells"]
              if c["cell_type"] == "code"),
          "the committed notebook carries no outputs (nothing has been run)")
    first_md = "".join(nb["cells"][0]["source"])
    for token in ("PREP_DATA-A", "NO TRAINING", "RESULT NOT RUN"):
        check(token in first_md, f"the first screen states '{token}'")


def test_spec_present_and_approved():
    print("the spec is present, approved, and owned by this implementation")
    check(os.path.exists(SPEC), "EXP-2026-007 spec exists at the fixed path")
    if not os.path.exists(SPEC):
        return
    with open(SPEC, encoding="utf-8") as fh:
        text = fh.read()
    for line in ("experiment_id: EXP-2026-007",
                 "status: approved_for_implementation",
                 "design_owner: codex", "implementation_owner: claude",
                 "dataset: MIT-BIH", "split: DS1_to_DS2_inter_patient",
                 "primary_metric: S_PR_AUC"):
        check(line in text, f"frontmatter: {line}")
    for token in ("P_ALIGNMENT", "INPUT_ABSENT_OR_MISMATCH",
                  "MEASUREMENT_UNQUALIFIED", "INSUFFICIENT_PATIENT_SUPPORT",
                  "GENERIC_RR_OR_RECORD_EFFECT",
                  "NO_DETECTABLE_P_TIMING_ASSOCIATION",
                  "P_TIMING_FAILURE_ASSOCIATION",
                  "failure-associated P-wave timing", "maxT",
                  "PREP_DATA-A", "ACQUIRE_ONLY", "아무것도 없다"):
        check(token in text, f"the spec keeps '{token}'")
    check("10.13026/C2108F" in text, "the spec pins the pwave DOI")


def main() -> int:
    print(f"{QD.EXPERIMENT_ID} / {QD.SUBSTAGE} — CPU test contract")
    print("=" * 72)
    for fn in (test_import_is_inert, test_modes, test_versioned_urls_only,
               test_sha_parser_and_path_normalisation,
               test_required_file_table, test_happy_path_verified,
               test_hash_mismatch_stops, test_missing_required_extension_stops,
               test_missing_publisher_hash_is_not_verified,
               test_existing_verified_asset_is_reused_not_rewritten,
               test_existing_conflicting_asset_stops,
               test_partial_existing_asset_goes_to_staging,
               test_record_list_mismatch_stops, test_wfdb_open_failures,
               test_wfdb_array_returns, test_failed_run_is_archived,
               test_pwave_annotation_range,
               test_duplicate_waveform_reported_not_substituted,
               test_retry_budget, test_not_run_vs_verified, test_bundle_schema,
               test_writes_stay_inside_the_asset_root,
               test_no_model_or_result_bundle_is_read,
               test_untouchable_repo_files, test_notebook_contract,
               test_spec_present_and_approved):
        fn()
    print("=" * 72)
    print(f"passed {PASSED} · failed {FAILED}")
    return 1 if FAILED else 0


if __name__ == "__main__":
    raise SystemExit(main())
