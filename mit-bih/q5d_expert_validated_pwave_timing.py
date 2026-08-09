"""EXP-2026-007 / Q5-D — PREP_DATA-A: acquire the public inputs, then stop.

ACQUIRE ONLY.  NO DELINEATION.  NO SCIENTIFIC ANALYSIS.  NO TRAINING.

What this module is
-------------------
The spec (`experiments/specs/EXP-2026-007-q5d-expert-validated-pwave-timing-audit.md`)
asks whether independently validated P-to-R timing is associated with the frozen
V10 failure pattern.  That question cannot be asked yet: the two public inputs it
needs — the versioned PhysioNet P-wave expert annotations and the raw MIT-BIH
waveforms — are not registered in Drive.  The user has authorised exactly one
substage, **PREP_DATA-A ACQUIRE_ONLY**, and this module implements that substage
and nothing after it.

So the only things in this file are: download from pinned versioned URLs, verify
every required file against the publisher's own `SHA256SUMS.txt`, prove each
record can actually be opened by WFDB, write an immutable audit bundle, and emit
one of three decision codes.  There is no delineator here, no P-to-R scalar, no
RR rule, no S PR-AUC, no permutation, and nothing that reads a model probability,
a checkpoint, or an earlier Q5 result bundle.  ``assert_acquire_only()`` checks
that textually so a reviewer can re-run the claim instead of trusting it.

Three decision codes, and only these
------------------------------------
``PREP_DATA_ACQUIRED_VERIFIED``
    Every required file of both sources exists, matches the publisher hash, and
    opens under WFDB; the record lists match; nothing pre-existing was touched.
``INPUT_ABSENT_OR_MISMATCH``
    Anything above failed.  The bundle names the exact files, the expected hash
    and the observed hash.  A stop is a complete result — **지금은 답할 수 없다**.
``PREP_DATA_RESULT_NOT_RUN``
    The code exists but nobody has executed the acquisition yet.  An unexecuted
    notebook is never reported as verified.

Design rules that are deliberately awkward
------------------------------------------
- A file is promoted from ``*.partial`` to its final name **only after** its hash
  matches.  A hash mismatch keeps the partial file and stops; it never triggers a
  louder re-download or a delete.
- If the destination asset directory already exists, its files are read and
  verified, never rewritten.  Different content at the same path is
  ``EXISTING_ASSET_CONFLICT`` and stops.  Missing files are fetched into a
  separate timestamped staging directory and the state is reported as partial —
  quietly topping up somebody else's immutable asset is exactly the failure mode
  this gate exists to prevent.
- Publisher checksum paths are normalised as *paths*, never collapsed to
  basenames: two different files may legitimately share a basename.
- Records 100/101 opening cleanly says nothing about record 231.  Every record is
  checked and every record appears in the report.
"""

from __future__ import annotations

import csv
import hashlib
import json
import os
import platform
import posixpath
import re
import shutil
import sys
import time
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional, Sequence, Tuple

EXPERIMENT_ID = "EXP-2026-007"
ARM_ID = "Q5-D"
SUBSTAGE = "PREP_DATA-A ACQUIRE_ONLY"
RUN_SLUG = "q5d_prep_data"
MODULE_VERSION = 2
MODULE_BUILD = "2026-08-09"

#: The banner every entry point prints.  It stays this way until a real
#: acquisition writes a decision bundle.
STATUS = "PREP_DATA DESIGN / RESULT NOT RUN"
HEADLINE = f"{EXPERIMENT_ID} / {SUBSTAGE}"
NO_SCIENCE_BANNER = "NO TRAINING / NO SCIENTIFIC ANALYSIS"

MODES: Tuple[str, ...] = ("DESIGN", "PREP_DATA_ACQUIRE", "PREP_DATA_REPORT")
#: Named so that asking for them fails loudly instead of silently doing nothing.
#: These stages exist in the spec but are NOT authorised in this substage.
FORBIDDEN_MODES: Tuple[str, ...] = ("QUALIFY", "ANALYZE", "MEASURE", "TRAIN")

# ── decision codes (spec §PREP_DATA acquisition gate) ───────────────────────
DECISION_VERIFIED = "PREP_DATA_ACQUIRED_VERIFIED"
DECISION_MISMATCH = "INPUT_ABSENT_OR_MISMATCH"
DECISION_NOT_RUN = "PREP_DATA_RESULT_NOT_RUN"
DECISIONS: Tuple[str, ...] = (DECISION_VERIFIED, DECISION_MISMATCH,
                              DECISION_NOT_RUN)

# ── per-file status vocabulary ──────────────────────────────────────────────
FILE_VERIFIED = "VERIFIED"
FILE_MISSING = "MISSING"
FILE_HASH_MISMATCH = "HASH_MISMATCH"
FILE_OPEN_FAILED = "OPEN_FAILED"
FILE_STATUSES: Tuple[str, ...] = (FILE_VERIFIED, FILE_MISSING,
                                  FILE_HASH_MISMATCH, FILE_OPEN_FAILED)

#: Not a file status — a stop reason for the whole run.
CONFLICT_CODE = "EXISTING_ASSET_CONFLICT"
PARTIAL_CODE = "EXISTING_ASSET_PARTIAL"

PARTIAL_SUFFIX = ".partial"
MAX_RETRIES = 3                      # network errors only, exponential backoff
RETRY_BACKOFF_S: Tuple[float, ...] = (2.0, 4.0, 8.0)
HTTP_TIMEOUT_S = 60
CHUNK_BYTES = 1 << 20
USER_AGENT = f"MedKOS-{EXPERIMENT_ID}-prep-data/{MODULE_VERSION}"

#: WFDB expectations for MIT-BIH.  360 Hz is a gate; lead names are recorded.
EXPECTED_FS = 360.0
EXPECTED_MIN_SIG = 2
#: How much of each ``.dat`` is actually decoded.  The point is to prove the
#: signal file is readable, not to load 104 MB of waveform into a prep run.
SAMPLE_WINDOW = 3600                 # 10 s at 360 Hz

REQUIRED_METADATA: Tuple[str, ...] = ("SHA256SUMS.txt", "RECORDS", "ANNOTATORS")
OPTIONAL_METADATA: Tuple[str, ...] = ("LICENSE.txt",)
#: The publisher's own checksum file is the root of trust, so it is the one file
#: with no expected hash.  Its observed hash is recorded in the manifest.
TRUST_ROOT = "SHA256SUMS.txt"


class Q5DError(RuntimeError):
    """Stop condition.  Every message names the file and the fix."""


class NetworkError(Q5DError):
    """Transport failure.  Retryable up to ``MAX_RETRIES`` and no further."""


class HttpStatusError(Q5DError):
    """Non-2xx response.  4xx (404/403) is fatal; 5xx/429 is retryable."""

    def __init__(self, code: int, url: str, reason: str = "") -> None:
        super().__init__(f"HTTP {code} for {url}"
                         + (f" ({reason})" if reason else ""))
        self.code = int(code)
        self.url = url


def is_retryable(exc: BaseException) -> bool:
    """Only transport hiccups are retried.  404/403 means *stop and report*."""
    if isinstance(exc, HttpStatusError):
        return exc.code >= 500 or exc.code == 429
    return isinstance(exc, NetworkError)


# ─────────────────────────────────────────────────────────────────────────────
# Pinned sources.  Versioned URLs only — `latest` is rejected by construction.
# ─────────────────────────────────────────────────────────────────────────────
MITDB_RECORDS_EXPECTED: Tuple[str, ...] = (
    "100", "101", "102", "103", "104", "105", "106", "107", "108", "109",
    "111", "112", "113", "114", "115", "116", "117", "118", "119",
    "121", "122", "123", "124",
    "200", "201", "202", "203", "205", "207", "208", "209", "210",
    "212", "213", "214", "215", "217", "219", "220", "221", "222", "223",
    "228", "230", "231", "232", "233", "234",
)
#: The 12 records with expert P-wave annotations (spec "Why now").  Six are DS1
#: (101, 106, 119, 122, 207, 223) and six are DS2 (100, 103, 117, 214, 222, 231);
#: that split matters to a later substage, not to this one.
PWAVE_RECORDS_EXPECTED: Tuple[str, ...] = (
    "100", "101", "103", "106", "117", "119", "122",
    "207", "214", "222", "223", "231",
)


@dataclass(frozen=True)
class Source:
    """One pinned PhysioNet database version and what must be fetched from it."""

    db: str
    version: str
    doi: str
    files_url: str                       # https://physionet.org/files/<db>/<v>/
    landing_url: str                     # https://physionet.org/content/<db>/<v>/
    license_name: str
    license_url: str
    extensions: Tuple[str, ...]
    records_expected: Tuple[str, ...]
    approx_uncompressed_mb: float

    @property
    def dir_name(self) -> str:
        return f"{self.db}-{self.version}"

    def url_for(self, rel_path: str) -> str:
        return assert_versioned_url(
            posixpath.join(self.files_url.rstrip("/"), rel_path.lstrip("/")))


SOURCE_MITDB = Source(
    db="mitdb",
    version="1.0.0",
    doi="10.13026/C2F305",
    files_url="https://physionet.org/files/mitdb/1.0.0/",
    landing_url="https://physionet.org/content/mitdb/1.0.0/",
    # Declared by the publisher on the landing page; the fetched LICENSE.txt (when
    # the tree publishes one) is stored beside it so intake can reconcile them.
    license_name="Open Data Commons Attribution License v1.0",
    license_url="https://physionet.org/content/mitdb/view-license/1.0.0/",
    extensions=(".dat", ".hea", ".atr"),
    records_expected=MITDB_RECORDS_EXPECTED,
    approx_uncompressed_mb=104.3,
)

SOURCE_PWAVE = Source(
    db="pwave",
    version="1.0.0",
    doi="10.13026/C2108F",
    files_url="https://physionet.org/files/pwave/1.0.0/",
    landing_url="https://physionet.org/content/pwave/1.0.0/",
    license_name="Open Data Commons Attribution License v1.0",
    license_url="https://physionet.org/content/pwave/view-license/1.0.0/",
    extensions=(".dat", ".hea", ".pwave"),
    records_expected=PWAVE_RECORDS_EXPECTED,
    approx_uncompressed_mb=22.4,
)

SOURCES: Tuple[Source, ...] = (SOURCE_MITDB, SOURCE_PWAVE)
SOURCE_BY_DB: Dict[str, Source] = {s.db: s for s in SOURCES}

#: Records whose raw waveform is published in BOTH trees.  They are compared,
#: never substituted for one another.
DUPLICATED_RECORDS: Tuple[str, ...] = PWAVE_RECORDS_EXPECTED
DUPLICATE_EXTENSIONS: Tuple[str, ...] = (".dat", ".hea")

# ── Drive contract (§3 of the task) ─────────────────────────────────────────
DRIVE_ASSET_REL = "MedKOS/ecg-model/assets/EXP-2026-007_prep_data"
SOURCE_SUBDIR = "source"
AUDIT_SUBDIR = "audit"
#: One immutable copy of every acquisition lives in ``audit/runs/<timestamp>/``.
RUNS_SUBDIR = "runs"
STAGING_PREFIX = "staging_"

AUDIT_FILES: Tuple[str, ...] = (
    "config.json", "asset_manifest.json", "source_inventory.csv",
    "checksum_report.csv", "record_inventory.csv", "wfdb_open_report.csv",
    "decision.json", "log.txt", "summary.md",
)

#: Textual proof that this module cannot do the forbidden things.  Tokens are
#: split so the list itself does not match.  Checked by ``assert_acquire_only``.
FORBIDDEN_TOKENS: Tuple[str, ...] = (
    "torch." + "optim", "." + "backward(", ".f" + "it(",
    "ecg_" + "delineate", "neuro" + "kit",
    "average_" + "precision", "precision_recall_" + "curve",
    "roc_auc_" + "score", "pr_" + "auc(",
    "mamba_" + "data", "v10" + "pkg", "core_" + "membership",
    "probs" + ".npy", "state_" + "dict",
)


# ─────────────────────────────────────────────────────────────────────────────
# Guards
# ─────────────────────────────────────────────────────────────────────────────
def resolve_mode(mode: str) -> str:
    """Exactly one of ``MODES``.  A later-stage mode names itself when refused."""
    m = str(mode).strip().upper()
    if m in FORBIDDEN_MODES:
        raise Q5DError(
            f"mode {m!r} belongs to a stage that is NOT authorised: the approved "
            f"substage is {SUBSTAGE}. Qualification and association analysis "
            f"start only after the acquisition bundle is reviewed.")
    if m not in MODES:
        raise Q5DError(f"mode must be exactly one of {MODES}, got {mode!r}")
    return m


def assert_acquire_only(path: Optional[str] = None) -> Dict[str, object]:
    """Evidence that this file trains nothing and analyses nothing.

    Textual on purpose: it is the cheapest artifact a reviewer can re-run.  Lines
    that are comments, and the token table itself, are skipped.
    """
    path = path or os.path.abspath(__file__)
    with open(path, "r", encoding="utf-8") as fh:
        lines = fh.readlines()
    hits: List[Dict[str, object]] = []
    for i, line in enumerate(lines, 1):
        stripped = line.lstrip()
        if stripped.startswith("#") or '" + "' in line:
            continue
        low = line.lower()
        for tok in FORBIDDEN_TOKENS:
            if tok.lower() in low and "assert_acquire_only" not in line:
                hits.append({"line": i, "token": tok})
    if hits:
        raise Q5DError(f"forbidden call found in an acquire-only module: {hits}")
    return {"acquire_only": True, "checked_file": path,
            "tokens": list(FORBIDDEN_TOKENS),
            "training_performed": False,
            "delineation_performed": False,
            "analysis_performed": False}


def assert_versioned_url(url: str) -> str:
    """Only pinned ``/files/<db>/<version>/`` URLs.  ``latest`` is refused.

    PhysioNet serves a moving ``latest`` alias.  Acquiring an immutable asset
    from a moving alias would make every hash in the manifest meaningless.
    """
    u = str(url).strip()
    if not u.startswith("https://"):
        raise Q5DError(f"refusing a non-HTTPS source URL: {url!r}")
    m = re.match(r"^https://physionet\.org/files/([A-Za-z0-9_.-]+)/"
                 r"(\d+\.\d+\.\d+)/(.*)$", u)
    if not m:
        raise Q5DError(
            f"refusing {url!r}: this stage downloads only from a pinned "
            f"https://physionet.org/files/<db>/<major.minor.patch>/ URL")
    if "latest" in (m.group(1).lower(), m.group(2).lower()):
        raise Q5DError(f"refusing the moving alias in {url!r}")
    tail = m.group(3)
    if ".." in tail.split("/"):
        raise Q5DError(f"refusing a path-escaping URL: {url!r}")
    return u


def safe_join(root: str, rel_path: str) -> str:
    """Join inside ``root`` or raise.  Nothing is ever written outside the root."""
    rel = str(rel_path).replace("\\", "/").lstrip("/")
    if not rel:
        raise Q5DError("empty relative path")
    full = os.path.normpath(os.path.join(root, *rel.split("/")))
    root_abs = os.path.normpath(root)
    if full != root_abs and not full.startswith(root_abs + os.sep):
        raise Q5DError(f"refusing to write outside {root_abs}: {rel_path!r}")
    return full


# ─────────────────────────────────────────────────────────────────────────────
# Publisher metadata parsing
# ─────────────────────────────────────────────────────────────────────────────
_SHA_RE = re.compile(r"^([0-9a-fA-F]{64})\s+[*]?(.+)$")


def normalize_rel_path(path: str, db: Optional[str] = None,
                       version: Optional[str] = None) -> str:
    """Normalise a publisher path to the tree-relative path used on disk.

    Keeps directories.  Two files that merely share a basename stay two files —
    collapsing them is how a checksum table quietly starts verifying the wrong
    bytes.
    """
    p = str(path).strip().replace("\\", "/")
    while p.startswith("./"):
        p = p[2:]
    p = p.lstrip("/")
    for prefix in ([f"{db}/{version}/", f"{db}/"] if db else []):
        if version and p.startswith(prefix):
            p = p[len(prefix):]
        elif not version and p.startswith(prefix):
            p = p[len(prefix):]
    parts = [seg for seg in p.split("/") if seg not in ("", ".")]
    if any(seg == ".." for seg in parts):
        raise Q5DError(f"refusing a path-escaping checksum entry: {path!r}")
    return "/".join(parts)


def parse_sha256sums(text: str, db: Optional[str] = None,
                     version: Optional[str] = None) -> Dict[str, str]:
    """Parse ``SHA256SUMS.txt`` into ``{relative path: sha256}``.

    Accepts both ``hash  path`` and ``hash *path``.  A repeated path with two
    different hashes is a hard error: the publisher table must be unambiguous
    before a single byte is verified against it.
    """
    out: Dict[str, str] = {}
    for lineno, raw in enumerate(str(text).splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        m = _SHA_RE.match(line)
        if not m:
            raise Q5DError(f"unparsable SHA256SUMS.txt line {lineno}: {raw!r}")
        sha = m.group(1).lower()
        rel = normalize_rel_path(m.group(2), db, version)
        if rel in out and out[rel] != sha:
            raise Q5DError(
                f"SHA256SUMS.txt lists {rel!r} twice with different hashes "
                f"({out[rel]} vs {sha}); refusing to guess which is canonical")
        out[rel] = sha
    if not out:
        raise Q5DError("SHA256SUMS.txt contained no usable entries")
    return out


def parse_records(text: str) -> List[str]:
    """Parse a PhysioNet ``RECORDS`` file, preserving publication order."""
    seen: List[str] = []
    for raw in str(text).splitlines():
        rec = raw.strip()
        if not rec or rec.startswith("#"):
            continue
        rec = rec.split("/")[-1]
        if rec.endswith(".hea"):
            rec = rec[:-4]
        if rec not in seen:
            seen.append(rec)
    return seen


def expected_sha_for(sums: Dict[str, str], rel_path: str,
                     source: Optional[Source] = None) -> Optional[str]:
    """Exact path lookup, with the publisher's optional ``<db>/<version>/`` prefix.

    Never falls back to a basename search.
    """
    rel = normalize_rel_path(rel_path)
    if rel in sums:
        return sums[rel]
    if source is not None:
        for prefix in (f"{source.db}/{source.version}/", f"{source.db}/"):
            if prefix + rel in sums:
                return sums[prefix + rel]
    return None


# ─────────────────────────────────────────────────────────────────────────────
# Required-file table
# ─────────────────────────────────────────────────────────────────────────────
@dataclass
class RequiredFile:
    db: str
    version: str
    record: str                  # "" for metadata files
    extension: str               # "" for metadata files
    rel_path: str
    url: str
    kind: str                    # "record" | "metadata"


def required_files(source: Source, records: Sequence[str],
                   include_metadata: bool = True) -> List[RequiredFile]:
    """Every file this stage must obtain from ``source``, in a fixed order."""
    out: List[RequiredFile] = []
    if include_metadata:
        for name in REQUIRED_METADATA:
            out.append(RequiredFile(source.db, source.version, "", "", name,
                                    source.url_for(name), "metadata"))
    for rec in records:
        for ext in source.extensions:
            rel = f"{rec}{ext}"
            out.append(RequiredFile(source.db, source.version, rec, ext, rel,
                                    source.url_for(rel), "record"))
    return out


# ─────────────────────────────────────────────────────────────────────────────
# Hashing and existing-asset inspection
# ─────────────────────────────────────────────────────────────────────────────
def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: str, chunk: int = CHUNK_BYTES) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        while True:
            block = fh.read(chunk)
            if not block:
                break
            h.update(block)
    return h.hexdigest()


EXISTING_ABSENT = "ABSENT"
EXISTING_VERIFIED = "VERIFIED_EXISTING"
EXISTING_CONFLICT = "CONFLICT"
EXISTING_UNVERIFIABLE = "UNVERIFIABLE"


def inspect_existing(path: str, expected_sha: Optional[str]) -> Dict[str, object]:
    """Read-only look at an already-present file.  Never writes, never deletes."""
    if not os.path.exists(path):
        return {"state": EXISTING_ABSENT, "path": path}
    observed = sha256_file(path)
    size = os.path.getsize(path)
    if expected_sha is None:
        return {"state": EXISTING_UNVERIFIABLE, "path": path,
                "observed_sha256": observed, "observed_bytes": size,
                "detail": "no publisher hash for this path"}
    if observed == expected_sha.lower():
        return {"state": EXISTING_VERIFIED, "path": path,
                "observed_sha256": observed, "observed_bytes": size}
    return {"state": EXISTING_CONFLICT, "path": path,
            "observed_sha256": observed, "expected_sha256": expected_sha,
            "observed_bytes": size,
            "detail": "same path, different content — not overwritten"}


def choose_write_root(final_root: str, staging_root: str) -> Dict[str, object]:
    """Where new downloads may land.

    A pre-existing asset directory is immutable: anything still missing goes to a
    timestamped staging directory and the run reports a partial state for a human
    to resolve.  Nothing tops up somebody else's frozen asset in place.
    """
    preexisting = os.path.isdir(final_root) and bool(os.listdir(final_root))
    return {"read_root": final_root,
            "write_root": staging_root if preexisting else final_root,
            "preexisting": preexisting}


# ─────────────────────────────────────────────────────────────────────────────
# HTTP
# ─────────────────────────────────────────────────────────────────────────────
@dataclass
class FetchedStream:
    """What an opener returns: a final URL plus something with ``.read(n)``."""

    final_url: str
    reader: object
    headers: Dict[str, str] = field(default_factory=dict)
    status: int = 200

    def close(self) -> None:
        closer = getattr(self.reader, "close", None)
        if callable(closer):
            closer()


def urllib_opener(url: str, timeout: int = HTTP_TIMEOUT_S) -> FetchedStream:
    """Default opener.  Streams over HTTPS from a pinned versioned URL."""
    assert_versioned_url(url)
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        resp = urllib.request.urlopen(req, timeout=timeout)   # noqa: S310
    except urllib.error.HTTPError as exc:                     # 4xx / 5xx
        raise HttpStatusError(exc.code, url, getattr(exc, "reason", "")) from exc
    except urllib.error.URLError as exc:
        raise NetworkError(f"network failure for {url}: {exc.reason}") from exc
    except (TimeoutError, OSError) as exc:
        raise NetworkError(f"network failure for {url}: {exc}") from exc
    code = int(getattr(resp, "status", 200) or 200)
    if code >= 400:
        raise HttpStatusError(code, url)
    final = resp.geturl() if hasattr(resp, "geturl") else url
    headers = dict(getattr(resp, "headers", {}) or {})
    return FetchedStream(final_url=final, reader=resp, headers=headers,
                         status=code)


Opener = Callable[[str], FetchedStream]
Progress = Callable[[Dict[str, object]], None]


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


def download_file(url: str, dest: str, expected_sha: Optional[str] = None,
                  opener: Optional[Opener] = None,
                  max_retries: int = MAX_RETRIES,
                  chunk: int = CHUNK_BYTES,
                  sleeper: Callable[[float], None] = time.sleep,
                  progress: Optional[Progress] = None,
                  log: Optional[RunLog] = None,
                  trust_root: bool = False) -> Dict[str, object]:
    """Stream one file to ``dest`` via ``dest + '.partial'``.

    The partial name is the whole point: a file only takes its real name after
    its hash matches the publisher's.  On mismatch the partial is *kept* (so the
    bytes can be inspected) and the caller stops — no delete, no forced retry.
    A file with no publisher hash is never promoted either; the single exception
    is ``trust_root=True``, which is the publisher's own checksum table and by
    definition cannot be verified against itself.

    Retries cover transport failures only, at most ``max_retries`` attempts with
    2s/4s/8s backoff.  A 404 or 403 stops immediately.
    """
    opener = opener or urllib_opener
    assert_versioned_url(url)
    os.makedirs(os.path.dirname(dest) or ".", exist_ok=True)
    partial = dest + PARTIAL_SUFFIX

    attempts = 0
    last_exc: Optional[BaseException] = None
    t0 = time.time()
    while attempts < max(1, int(max_retries)):
        attempts += 1
        try:
            stream = opener(url)
            try:
                total = _content_length(stream.headers)
                done = 0
                h = hashlib.sha256()
                with open(partial, "wb") as fh:
                    while True:
                        block = stream.reader.read(chunk)
                        if not block:
                            break
                        fh.write(block)
                        h.update(block)
                        done += len(block)
                        if progress is not None:
                            progress({"url": url, "bytes": done,
                                      "total": total, "dest": dest,
                                      "elapsed_s": time.time() - t0})
            finally:
                stream.close()
            observed = h.hexdigest()
            elapsed = round(time.time() - t0, 3)
            row: Dict[str, object] = {
                "url": url, "final_url": stream.final_url, "dest": dest,
                "observed_bytes": done, "observed_sha256": observed,
                "expected_sha256": expected_sha, "attempts": attempts,
                "elapsed_s": elapsed,
                "redirected": stream.final_url != url,
                "offversion_redirect": _is_offversion(stream.final_url),
            }
            if expected_sha is not None and observed != str(expected_sha).lower():
                row.update({"status": FILE_HASH_MISMATCH,
                            "partial_path": partial, "promoted": False,
                            "detail": ("publisher hash and observed hash differ; "
                                       "the partial file was kept for inspection "
                                       "and NOT promoted")})
                if log:
                    log(f"  HASH_MISMATCH {os.path.basename(dest)} "
                        f"expected {expected_sha} observed {observed}")
                return row
            if expected_sha is None and not trust_root:
                row.update({"status": FILE_HASH_MISMATCH,
                            "partial_path": partial, "promoted": False,
                            "detail": ("no publisher SHA-256 entry for this "
                                       "path; the download stays a partial file "
                                       "and is NOT promoted")})
                return row
            os.replace(partial, dest)
            row.update({"status": FILE_VERIFIED, "promoted": True,
                        "verified_against_publisher": expected_sha is not None,
                        "detail": ("" if expected_sha is not None else
                                   "publisher trust root — no expected hash "
                                   "exists; its own sha256 is recorded")})
            return row
        except BaseException as exc:                       # noqa: BLE001
            last_exc = exc
            _remove_partial(partial)
            if not is_retryable(exc) or attempts >= max(1, int(max_retries)):
                break
            wait = RETRY_BACKOFF_S[min(attempts - 1, len(RETRY_BACKOFF_S) - 1)]
            if log:
                log(f"  retry {attempts}/{max_retries} in {wait:.0f}s — {exc}")
            sleeper(wait)
    raise Q5DError(
        f"download failed after {attempts} attempt(s): {url} -> {last_exc}")


def _remove_partial(partial: str) -> None:
    """Remove only our own ``*.partial`` scratch file, never a real asset."""
    if partial.endswith(PARTIAL_SUFFIX) and os.path.exists(partial):
        try:
            os.remove(partial)
        except OSError:
            pass


def _content_length(headers: Dict[str, str]) -> Optional[int]:
    for key in ("Content-Length", "content-length"):
        if key in (headers or {}):
            try:
                return int(headers[key])
            except (TypeError, ValueError):
                return None
    return None


def _is_offversion(url: str) -> bool:
    try:
        assert_versioned_url(url)
    except Q5DError:
        return True
    return False


def fetch_text(url: str, dest: str, expected_sha: Optional[str] = None,
               opener: Optional[Opener] = None, log: Optional[RunLog] = None,
               sleeper: Callable[[float], None] = time.sleep,
               max_retries: int = MAX_RETRIES,
               trust_root: bool = False) -> Tuple[str, Dict[str, object]]:
    """Download a small metadata file and return ``(text, row)``."""
    row = download_file(url, dest, expected_sha=expected_sha, opener=opener,
                        log=log, sleeper=sleeper, max_retries=max_retries,
                        trust_root=trust_root)
    path = dest if row.get("promoted") else str(row.get("partial_path") or dest)
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        return fh.read(), row


# ─────────────────────────────────────────────────────────────────────────────
# Acquisition
# ─────────────────────────────────────────────────────────────────────────────
def acquire_source(source: Source, final_root: str, staging_root: str,
                   opener: Optional[Opener] = None,
                   log: Optional[RunLog] = None,
                   max_retries: int = MAX_RETRIES,
                   progress: Optional[Progress] = None,
                   sleeper: Callable[[float], None] = time.sleep,
                   ) -> Dict[str, object]:
    """Acquire and verify one pinned source tree.

    Order matters: the publisher's checksum table and record list come first, so
    every subsequent byte is checked against the publisher rather than against
    an assumption of what the database should contain.
    """
    log = log or RunLog()
    assert_acquire_only()
    src_final = os.path.join(final_root, SOURCE_SUBDIR, source.dir_name)
    src_staging = os.path.join(staging_root, SOURCE_SUBDIR, source.dir_name)
    plan = choose_write_root(src_final, src_staging)
    write_root, read_root = str(plan["write_root"]), str(plan["read_root"])
    log(f"{source.db} {source.version} — read {read_root}"
        f"{' (pre-existing, immutable)' if plan['preexisting'] else ''}")
    if plan["preexisting"]:
        log(f"  new files (if any) go to staging: {write_root}")

    rows: List[Dict[str, object]] = []
    notes: List[str] = []

    # 1. publisher checksum table (trust root, no expected hash of its own)
    sums_rel = TRUST_ROOT
    sums_text, sums_row = _obtain(source, sums_rel, None, read_root, write_root,
                                  opener, log, max_retries, sleeper, text=True,
                                  trust_root=True)
    rows.append(_row(source, "", "", sums_rel, sums_row, "metadata"))
    if sums_row.get("status") != FILE_VERIFIED:
        return _source_result(source, rows, [], plan, notes + [
            f"{sums_rel} could not be obtained — nothing can be verified"],
            sums_sha=None)
    sums = parse_sha256sums(sums_text, source.db, source.version)
    sums_sha = str(sums_row.get("observed_sha256"))
    log(f"  {sums_rel}: {len(sums)} publisher entries (sha256 {sums_sha[:16]}…)")

    # 2. RECORDS and ANNOTATORS, verified against the table
    records_declared: List[str] = []
    for name in ("RECORDS", "ANNOTATORS"):
        exp = expected_sha_for(sums, name, source)
        text, row = _obtain(source, name, exp, read_root, write_root, opener,
                            log, max_retries, sleeper, text=True)
        rows.append(_row(source, "", "", name, row, "metadata"))
        if row.get("status") != FILE_VERIFIED:
            notes.append(f"required metadata {name} is {row.get('status')}")
            continue
        if name == "RECORDS":
            records_declared = parse_records(text)

    if not records_declared:
        return _source_result(source, rows, [], plan,
                              notes + ["RECORDS is unusable — the record list "
                                       "cannot be confirmed"], sums_sha)
    log(f"  RECORDS declares {len(records_declared)} record(s); expected "
        f"{len(source.records_expected)}")

    # 3. optional metadata — recorded, never a gate
    for name in OPTIONAL_METADATA:
        exp = expected_sha_for(sums, name, source)
        if exp is None:
            continue
        try:
            _, row = _obtain(source, name, exp, read_root, write_root, opener,
                             log, max_retries, sleeper, text=True)
            rows.append(_row(source, "", "", name, row, "optional"))
        except Q5DError as exc:
            notes.append(f"optional metadata {name} unavailable: {exc}")

    # 4. every required record file
    reqs = required_files(source, records_declared, include_metadata=False)
    log(f"  {len(reqs)} required record file(s) "
        f"({len(records_declared)} records x {len(source.extensions)} ext)")
    for i, req in enumerate(reqs, 1):
        exp = expected_sha_for(sums, req.rel_path, source)
        _, row = _obtain(source, req.rel_path, exp, read_root, write_root,
                         opener, log, max_retries, sleeper, text=False,
                         progress=progress)
        rows.append(_row(source, req.record, req.extension, req.rel_path, row,
                         "record"))
        if progress is not None:
            progress({"scope": "file", "db": source.db, "index": i,
                      "total": len(reqs), "record": req.record,
                      "extension": req.extension,
                      "status": row.get("status")})
    return _source_result(source, rows, records_declared, plan, notes, sums_sha)


def _obtain(source: Source, rel_path: str, expected_sha: Optional[str],
            read_root: str, write_root: str, opener: Optional[Opener],
            log: Optional[RunLog], max_retries: int,
            sleeper: Callable[[float], None], text: bool,
            progress: Optional[Progress] = None,
            trust_root: bool = False) -> Tuple[str, Dict[str, object]]:
    """Reuse a verified existing file, or download it — never overwrite one."""
    existing_path = safe_join(read_root, rel_path)
    expected = expected_sha.lower() if expected_sha else None
    state = inspect_existing(existing_path, expected)
    if state["state"] == EXISTING_UNVERIFIABLE and trust_root:
        # The publisher's checksum table has no expected hash by construction.
        # Reuse the copy already in the immutable asset and record its own hash
        # so two runs of this stage can be compared against each other.
        content = ""
        if text:
            with open(existing_path, "r", encoding="utf-8",
                      errors="replace") as fh:
                content = fh.read()
        return content, {
            "url": source.url_for(rel_path), "final_url": "",
            "dest": existing_path, "status": FILE_VERIFIED,
            "action": "reused_existing_trust_root", "promoted": True,
            "observed_bytes": state.get("observed_bytes"),
            "observed_sha256": state.get("observed_sha256"),
            "expected_sha256": None, "attempts": 0, "elapsed_s": 0.0,
            "detail": ("publisher trust root reused from the existing asset; "
                       "its own sha256 is recorded for comparison")}
    if state["state"] == EXISTING_VERIFIED:
        row = {"url": source.url_for(rel_path), "final_url": "",
               "dest": existing_path, "status": FILE_VERIFIED,
               "action": "reused_existing", "promoted": True,
               "observed_bytes": state["observed_bytes"],
               "observed_sha256": state["observed_sha256"],
               "expected_sha256": expected, "attempts": 0, "elapsed_s": 0.0,
               "detail": "already present and hash-identical; not rewritten"}
        content = ""
        if text:
            with open(existing_path, "r", encoding="utf-8",
                      errors="replace") as fh:
                content = fh.read()
        return content, row
    if state["state"] == EXISTING_CONFLICT:
        if log:
            log(f"  {CONFLICT_CODE}: {rel_path} exists with different content")
        return "", {"url": source.url_for(rel_path), "final_url": "",
                    "dest": existing_path, "status": FILE_HASH_MISMATCH,
                    "action": CONFLICT_CODE, "promoted": False,
                    "observed_bytes": state.get("observed_bytes"),
                    "observed_sha256": state.get("observed_sha256"),
                    "expected_sha256": expected, "attempts": 0,
                    "elapsed_s": 0.0, "detail": str(state.get("detail"))}
    if state["state"] == EXISTING_UNVERIFIABLE:
        return "", {"url": source.url_for(rel_path), "final_url": "",
                    "dest": existing_path, "status": FILE_HASH_MISMATCH,
                    "action": "existing_without_publisher_hash",
                    "promoted": False,
                    "observed_bytes": state.get("observed_bytes"),
                    "observed_sha256": state.get("observed_sha256"),
                    "expected_sha256": None, "attempts": 0, "elapsed_s": 0.0,
                    "detail": str(state.get("detail"))}

    dest = safe_join(write_root, rel_path)
    url = source.url_for(rel_path)
    try:
        if text:
            content, row = fetch_text(url, dest, expected_sha=expected,
                                      opener=opener, log=log, sleeper=sleeper,
                                      max_retries=max_retries,
                                      trust_root=trust_root)
        else:
            row = download_file(url, dest, expected_sha=expected,
                                opener=opener, log=log, sleeper=sleeper,
                                max_retries=max_retries, progress=progress,
                                trust_root=trust_root)
            content = ""
    except Q5DError as exc:
        return "", {"url": url, "final_url": "", "dest": dest,
                    "status": FILE_MISSING, "action": "download_failed",
                    "promoted": False, "observed_bytes": 0,
                    "observed_sha256": "", "expected_sha256": expected,
                    "attempts": max_retries, "elapsed_s": 0.0,
                    "detail": str(exc)}
    row.setdefault("action", "downloaded")
    return content, row


def _row(source: Source, record: str, ext: str, rel_path: str,
         raw: Dict[str, object], kind: str) -> Dict[str, object]:
    return {"database": source.db, "version": source.version,
            "record": record, "extension": ext, "rel_path": rel_path,
            "kind": kind, "source_url": raw.get("url"),
            "final_url": raw.get("final_url") or raw.get("url"),
            "expected_bytes": raw.get("expected_bytes", ""),
            "observed_bytes": raw.get("observed_bytes", 0),
            "publisher_sha256": raw.get("expected_sha256") or "",
            "observed_sha256": raw.get("observed_sha256") or "",
            "status": raw.get("status", FILE_MISSING),
            "action": raw.get("action", ""),
            "attempts": raw.get("attempts", 0),
            "redirected": bool(raw.get("redirected", False)),
            "offversion_redirect": bool(raw.get("offversion_redirect", False)),
            "path": raw.get("dest", ""),
            "detail": raw.get("detail", "")}


def _source_result(source: Source, rows: List[Dict[str, object]],
                   records_declared: Sequence[str], plan: Dict[str, object],
                   notes: Sequence[str], sums_sha: Optional[str],
                   ) -> Dict[str, object]:
    by_status: Dict[str, int] = {s: 0 for s in FILE_STATUSES}
    for r in rows:
        by_status[str(r["status"])] = by_status.get(str(r["status"]), 0) + 1
    conflicts = [r for r in rows if r.get("action") == CONFLICT_CODE]
    # "Partial" is about the immutable asset, not about the run: if the asset
    # directory already existed and this run still had to fetch something, that
    # directory was incomplete.  Whether the fetch succeeded into staging is
    # irrelevant — a human decides what goes into a frozen asset.
    fetched = [r for r in rows
               if str(r.get("action", "")).startswith("download")]
    partial = bool(plan.get("preexisting")) and bool(fetched)
    return {
        "database": source.db, "version": source.version, "doi": source.doi,
        "files_url": source.files_url, "landing_url": source.landing_url,
        "license_name": source.license_name, "license_url": source.license_url,
        "extensions": list(source.extensions),
        "records_declared": list(records_declared),
        "records_expected": list(source.records_expected),
        "records_match": list(records_declared) == list(source.records_expected),
        "n_records_declared": len(records_declared),
        "n_records_expected": len(source.records_expected),
        "sha256sums_sha256": sums_sha,
        "files": rows, "counts": by_status,
        "n_files": len(rows),
        "observed_total_bytes": int(sum(int(r.get("observed_bytes") or 0)
                                        for r in rows)),
        "approx_expected_mb": source.approx_uncompressed_mb,
        "checksum_pass_fraction": (round(by_status.get(FILE_VERIFIED, 0)
                                         / len(rows), 6) if rows else 0.0),
        "conflicts": conflicts, "n_conflict": len(conflicts),
        "existing_asset_partial": partial, "n_fetched": len(fetched),
        "write_root": plan.get("write_root"),
        "read_root": plan.get("read_root"),
        "preexisting_asset": bool(plan.get("preexisting")),
        "notes": list(notes),
    }


# ─────────────────────────────────────────────────────────────────────────────
# WFDB verification
# ─────────────────────────────────────────────────────────────────────────────
def _import_wfdb():
    try:
        import wfdb                                   # noqa: PLC0415
    except Exception as exc:                          # pragma: no cover
        raise Q5DError(
            "wfdb is required for the open/annotation check: pip install wfdb "
            f"({exc})") from exc
    return wfdb


def _as_list(value) -> List:
    """Sequence -> list without ever asking a sequence whether it is truthy.

    ``wfdb`` hands back numpy arrays.  ``arr or []`` raises "truth value of an
    array ... is ambiguous", and inside a try/except that misreports a perfectly
    good annotation file as an unreadable one.  Convert, never test.
    """
    if value is None:
        return []
    try:
        return list(value)
    except TypeError:
        return []


def check_record(root: str, source: Source, record: str, wfdb_module=None,
                 sample_window: int = SAMPLE_WINDOW) -> Dict[str, object]:
    """Open one record: header, sampling frequency, a real ``.dat`` read, annotations.

    Nothing here interprets the signal.  It answers one question — can a later
    stage actually open this file — and answers it per record, because 100 and
    101 opening cleanly says nothing about 231.
    """
    wfdb = wfdb_module or _import_wfdb()
    base = safe_join(root, record)
    ann_ext = "pwave" if source.db == "pwave" else "atr"
    out: Dict[str, object] = {
        "database": source.db, "version": source.version, "record": record,
        "rdheader_ok": False, "fs": None, "fs_ok": False, "n_sig": None,
        "sig_names": "", "sig_len": None, "dat_read_ok": False,
        "n_samples_read": 0, "ann_ext": ann_ext, "ann_ok": False,
        "ann_count": 0, "ann_min_sample": None, "ann_max_sample": None,
        "ann_in_range": False, "status": FILE_OPEN_FAILED, "detail": "",
    }
    try:
        hdr = wfdb.rdheader(base)
    except Exception as exc:                          # noqa: BLE001
        out["detail"] = f"rdheader failed: {exc}"
        return out
    out["rdheader_ok"] = True
    fs = float(getattr(hdr, "fs", 0) or 0)
    n_sig = int(getattr(hdr, "n_sig", 0) or 0)
    sig_len = int(getattr(hdr, "sig_len", 0) or 0)
    names = _as_list(getattr(hdr, "sig_name", None))
    out.update({"fs": fs, "fs_ok": fs == EXPECTED_FS, "n_sig": n_sig,
                "sig_names": "|".join(str(n) for n in names),
                "sig_len": sig_len})
    if fs != EXPECTED_FS:
        out["detail"] = f"sampling frequency {fs} != {EXPECTED_FS}"
        return out
    if n_sig < EXPECTED_MIN_SIG:
        out["detail"] = f"signal count {n_sig} < {EXPECTED_MIN_SIG}"
        return out

    want = max(1, min(int(sample_window), sig_len or int(sample_window)))
    try:
        rec = wfdb.rdrecord(base, sampfrom=0, sampto=want, channels=[0])
        signal = getattr(rec, "p_signal", None)
        if signal is None:
            signal = getattr(rec, "d_signal", None)
        n_read = int(len(signal)) if signal is not None else 0
        out["dat_read_ok"] = n_read > 0
        out["n_samples_read"] = n_read
    except Exception as exc:                          # noqa: BLE001
        out["detail"] = f"rdrecord failed: {exc}"
        return out
    if not out["dat_read_ok"]:
        out["detail"] = "rdrecord returned no samples"
        return out

    try:
        ann = wfdb.rdann(base, ann_ext)
        samples = _as_list(getattr(ann, "sample", None))
    except Exception as exc:                          # noqa: BLE001
        out["detail"] = f"rdann({ann_ext!r}) failed: {exc}"
        return out
    out["ann_count"] = len(samples)
    out["ann_ok"] = len(samples) > 0
    if not samples:
        out["detail"] = f"{ann_ext} annotation file is empty"
        return out
    lo, hi = int(min(samples)), int(max(samples))
    out["ann_min_sample"], out["ann_max_sample"] = lo, hi
    out["ann_in_range"] = bool(lo >= 0 and (sig_len == 0 or hi < sig_len))
    if not out["ann_in_range"]:
        out["detail"] = (f"{ann_ext} annotation samples [{lo}, {hi}] fall "
                         f"outside the record range [0, {sig_len})")
        return out
    out["status"] = FILE_VERIFIED
    return out


def wfdb_open_report(root: str, source: Source, records: Sequence[str],
                     wfdb_module=None, sample_window: int = SAMPLE_WINDOW,
                     log: Optional[RunLog] = None,
                     progress: Optional[Progress] = None,
                     ) -> List[Dict[str, object]]:
    """Run ``check_record`` over every record — no sampling, no early exit."""
    src_root = os.path.join(root, SOURCE_SUBDIR, source.dir_name)
    rows: List[Dict[str, object]] = []
    for i, rec in enumerate(records, 1):
        row = check_record(src_root, source, rec, wfdb_module=wfdb_module,
                           sample_window=sample_window)
        rows.append(row)
        if log and row["status"] != FILE_VERIFIED:
            log(f"  OPEN_FAILED {source.db} {rec}: {row['detail']}")
        if progress is not None:
            progress({"scope": "wfdb", "db": source.db, "index": i,
                      "total": len(records), "record": rec,
                      "status": row["status"]})
    return rows


def compare_duplicate_waveforms(root: str,
                                records: Sequence[str] = DUPLICATED_RECORDS,
                                extensions: Sequence[str] = DUPLICATE_EXTENSIONS,
                                ) -> List[Dict[str, object]]:
    """Compare the raw waveforms published in both trees.  Report, never swap.

    The 12 P-wave records ship their own copy of the MIT-BIH signal.  If the two
    copies differ, that is a fact for the reviewer — silently preferring one of
    them would decide a provenance question this stage has no authority over.
    """
    out: List[Dict[str, object]] = []
    mit_root = os.path.join(root, SOURCE_SUBDIR, SOURCE_MITDB.dir_name)
    pw_root = os.path.join(root, SOURCE_SUBDIR, SOURCE_PWAVE.dir_name)
    for rec in records:
        for ext in extensions:
            a = os.path.join(mit_root, f"{rec}{ext}")
            b = os.path.join(pw_root, f"{rec}{ext}")
            row: Dict[str, object] = {"record": rec, "extension": ext,
                                      "mitdb_path": a, "pwave_path": b,
                                      "mitdb_sha256": "", "pwave_sha256": "",
                                      "status": "INCOMPLETE",
                                      "detail": "one or both copies absent"}
            if os.path.exists(a) and os.path.exists(b):
                sa, sb = sha256_file(a), sha256_file(b)
                row.update({"mitdb_sha256": sa, "pwave_sha256": sb,
                            "status": "IDENTICAL" if sa == sb else "DIFFERENT",
                            "detail": "" if sa == sb else
                                      "the two published copies differ; both are "
                                      "kept as published, neither is substituted"})
            out.append(row)
    return out


# ─────────────────────────────────────────────────────────────────────────────
# Decision
# ─────────────────────────────────────────────────────────────────────────────
def evaluate_prep_decision(inventories: Sequence[Dict[str, object]],
                           wfdb_rows: Sequence[Dict[str, object]],
                           duplicates: Sequence[Dict[str, object]] = (),
                           ) -> Dict[str, object]:
    """The pre-registered acquisition gate.  Exactly one decision code.

    Every gate is evaluated (so the report is complete) but the FIRST failure is
    named as the stopping reason, and any failure at all means
    ``INPUT_ABSENT_OR_MISMATCH``.
    """
    inv = {str(s["database"]): s for s in inventories}
    gates: List[Dict[str, object]] = []

    def gate(key: str, passed: bool, detail: str, evidence=None) -> None:
        gates.append({"gate": key, "pass": bool(passed), "detail": detail,
                      "evidence": evidence if evidence is not None else []})

    for src in SOURCES:
        s = inv.get(src.db)
        if s is None:
            gate(f"{src.db}_acquired", False,
                 f"{src.db} {src.version} was never acquired")
            continue
        n_exp = len(src.records_expected)
        gate(f"{src.db}_record_list", bool(s.get("records_match")),
             (f"official RECORDS lists {s.get('n_records_declared')} record(s); "
              f"expected {n_exp}"),
             sorted(set(s.get("records_expected", []))
                    ^ set(s.get("records_declared", []))))
        files = list(s.get("files", []))
        bad = [f for f in files if f.get("status") != FILE_VERIFIED]
        gate(f"{src.db}_checksums", not bad,
             (f"{len(files) - len(bad)}/{len(files)} required file(s) match the "
              f"publisher SHA-256"),
             [_fail_row(f) for f in bad[:50]])
        gate(f"{src.db}_no_conflict", not s.get("conflicts"),
             (f"{len(s.get('conflicts', []))} path(s) already existed with "
              f"different content"),
             [_fail_row(f) for f in list(s.get("conflicts", []))[:50]])
        gate(f"{src.db}_asset_complete", not s.get("existing_asset_partial"),
             ("a pre-existing asset directory was incomplete; the missing files "
              "were staged for review instead of being written into it"
              if s.get("existing_asset_partial") else
              "no pre-existing asset was modified"))
        gate(f"{src.db}_provenance", _provenance_complete(s),
             "source, version, DOI, license, URL and the checksum-table hash "
             "are all recorded")

        recs = [r for r in wfdb_rows if r.get("database") == src.db]
        seen = {str(r.get("record")) for r in recs}
        declared = [str(r) for r in s.get("records_declared", [])]
        bad_open = [r for r in recs if r.get("status") != FILE_VERIFIED]
        covered = bool(declared) and seen == set(declared)
        gate(f"{src.db}_wfdb_open",
             covered and not bad_open and len(recs) == len(declared),
             (f"{len(recs) - len(bad_open)}/{len(declared) or '?'} record(s) "
              f"open under WFDB with fs {EXPECTED_FS:g} Hz and a non-empty "
              f"{'pwave' if src.db == 'pwave' else 'atr'} annotation set"),
             [{"record": r.get("record"), "detail": r.get("detail")}
              for r in bad_open[:50]]
             + ([{"detail": "not every declared record was checked"}]
                if not covered else []))

    failed = [g for g in gates if not g["pass"]]
    decision = DECISION_VERIFIED if not failed else DECISION_MISMATCH
    dup_diff = [d for d in duplicates if d.get("status") == "DIFFERENT"]
    return {
        "experiment_id": EXPERIMENT_ID, "arm_id": ARM_ID, "substage": SUBSTAGE,
        "decision": decision,
        "decision_is_scientific_result": False,
        "training_performed": False,
        "delineation_performed": False,
        "analysis_performed": False,
        "gates": gates,
        "n_gate_pass": len(gates) - len(failed), "n_gate_total": len(gates),
        "first_stopping_reason": (
            None if not failed else
            {"gate": failed[0]["gate"], "detail": failed[0]["detail"],
             "evidence": failed[0]["evidence"]}),
        "duplicate_waveform_summary": {
            "compared": len(duplicates),
            "identical": len([d for d in duplicates
                              if d.get("status") == "IDENTICAL"]),
            "different": len(dup_diff),
            "incomplete": len([d for d in duplicates
                               if d.get("status") == "INCOMPLETE"]),
            "note": ("copies that differ are reported and both kept as "
                     "published; neither tree is substituted for the other"),
        },
        "permitted_next_step": (
            "report this acquisition bundle to the user and STOP. Delineation "
            "qualification, the beat join, and any DS2 outcome analysis need a "
            "separate approval — nothing after PREP_DATA-A runs automatically."),
    }


def _fail_row(f: Dict[str, object]) -> Dict[str, object]:
    return {"rel_path": f.get("rel_path"), "database": f.get("database"),
            "record": f.get("record"), "extension": f.get("extension"),
            "status": f.get("status"), "action": f.get("action"),
            "expected_sha256": f.get("publisher_sha256"),
            "observed_sha256": f.get("observed_sha256"),
            "observed_bytes": f.get("observed_bytes"),
            "detail": f.get("detail")}


def _provenance_complete(s: Dict[str, object]) -> bool:
    required = ("database", "version", "doi", "license_name", "files_url",
                "sha256sums_sha256")
    if any(not s.get(k) for k in required):
        return False
    files = list(s.get("files", []))
    if not files:
        return False
    return all(f.get("observed_sha256") for f in files
               if f.get("status") == FILE_VERIFIED)


# ─────────────────────────────────────────────────────────────────────────────
# Bundle
# ─────────────────────────────────────────────────────────────────────────────
def _json_safe(obj):
    if isinstance(obj, dict):
        return {str(k): _json_safe(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_json_safe(v) for v in obj]
    if isinstance(obj, (bytes, bytearray)):
        return obj.decode("utf-8", "replace")
    return obj


def _dump_json(path: str, obj) -> None:
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(_json_safe(obj), fh, ensure_ascii=False, indent=1,
                  default=str)


def _dump_csv(path: str, rows: Sequence[Dict[str, object]],
              columns: Optional[Sequence[str]] = None) -> None:
    rows = list(rows)
    cols = list(columns) if columns else sorted({k for r in rows for k in r})
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(cols or ["(empty)"])
        for r in rows:
            w.writerow([_scalar(r.get(c, "")) for c in cols])


def _scalar(v):
    if isinstance(v, (dict, list, tuple)):
        return json.dumps(_json_safe(v), ensure_ascii=False, default=str)
    return v


def environment_manifest() -> Dict[str, object]:
    return {"python": sys.version.split()[0], "platform": platform.platform(),
            "module_version": MODULE_VERSION, "module_build": MODULE_BUILD,
            "wfdb_version": _optional_version("wfdb"),
            "numpy_version": _optional_version("numpy")}


def _optional_version(name: str) -> Optional[str]:
    mod = sys.modules.get(name)
    if mod is None:
        try:
            mod = __import__(name)
        except Exception:                             # noqa: BLE001
            return None
    return str(getattr(mod, "__version__", "unknown"))


def build_config() -> Dict[str, object]:
    """Everything fixed before execution, written out so a reviewer can diff it."""
    return {
        "experiment_id": EXPERIMENT_ID, "arm_id": ARM_ID, "substage": SUBSTAGE,
        "mode": "PREP_DATA_ACQUIRE", "status_banner": NO_SCIENCE_BANNER,
        "module_version": MODULE_VERSION, "module_build": MODULE_BUILD,
        "modes": list(MODES), "forbidden_modes": list(FORBIDDEN_MODES),
        "decisions": list(DECISIONS), "file_statuses": list(FILE_STATUSES),
        "drive_asset_rel": DRIVE_ASSET_REL,
        "audit_files": list(AUDIT_FILES),
        "max_retries": MAX_RETRIES, "retry_backoff_s": list(RETRY_BACKOFF_S),
        "expected_fs_hz": EXPECTED_FS, "sample_window": SAMPLE_WINDOW,
        "required_metadata": list(REQUIRED_METADATA),
        "sources": [{"database": s.db, "version": s.version, "doi": s.doi,
                     "files_url": s.files_url, "landing_url": s.landing_url,
                     "license_name": s.license_name,
                     "license_url": s.license_url,
                     "extensions": list(s.extensions),
                     "n_records_expected": len(s.records_expected),
                     "records_expected": list(s.records_expected),
                     "approx_uncompressed_mb": s.approx_uncompressed_mb}
                    for s in SOURCES],
        "duplicated_records": list(DUPLICATED_RECORDS),
        "not_performed": ["p_wave_delineation", "p_to_r_measurement",
                          "rr_or_coupling_ratio", "ds2_outcome_analysis",
                          "s_pr_auc", "sham_permutation", "model_training"],
    }


def run_prep_data_acquire(asset_root: str, timestamp: str,
                          opener: Optional[Opener] = None,
                          wfdb_module=None,
                          log: Optional[RunLog] = None,
                          max_retries: int = MAX_RETRIES,
                          sample_window: int = SAMPLE_WINDOW,
                          progress: Optional[Progress] = None,
                          sleeper: Callable[[float], None] = time.sleep,
                          sources: Sequence[Source] = SOURCES,
                          ) -> Dict[str, object]:
    """PREP_DATA_ACQUIRE: download, verify, open, report — and stop there.

    ``timestamp`` is supplied by the caller (the notebook) so the staging path and
    the manifest are reproducible rather than wall-clock dependent.
    """
    log = log or RunLog()
    assert_acquire_only()
    log(f"{HEADLINE} — {NO_SCIENCE_BANNER}")
    asset_root = os.path.abspath(asset_root)
    staging_root = os.path.join(asset_root, f"{STAGING_PREFIX}{timestamp}")
    audit_dir = os.path.join(asset_root, AUDIT_SUBDIR)
    os.makedirs(audit_dir, exist_ok=True)
    t0 = time.time()

    inventories: List[Dict[str, object]] = []
    for src in sources:
        inventories.append(acquire_source(
            src, asset_root, staging_root, opener=opener, log=log,
            max_retries=max_retries, progress=progress, sleeper=sleeper))
        inv = inventories[-1]
        log(f"  {src.db}: {inv['counts'].get(FILE_VERIFIED, 0)}/"
            f"{inv['n_files']} verified · "
            f"{inv['observed_total_bytes'] / 1e6:.1f} MB observed "
            f"(publisher tree ~{src.approx_uncompressed_mb:.1f} MB)")

    wfdb_rows: List[Dict[str, object]] = []
    for src, inv in zip(sources, inventories):
        recs = [str(r) for r in inv.get("records_declared", [])]
        if not recs:
            log(f"  {src.db}: no declared records — skipping the WFDB check")
            continue
        # The asset root always holds whatever was already there; when a staging
        # root was used, the freshly fetched files live there instead, so the
        # check falls back to staging for records the asset root cannot open.
        rows = wfdb_open_report(asset_root, src, recs, wfdb_module=wfdb_module,
                                sample_window=sample_window, log=log,
                                progress=progress)
        if inv.get("preexisting_asset"):
            staged = wfdb_open_report(staging_root, src, recs,
                                      wfdb_module=wfdb_module,
                                      sample_window=sample_window)
            rows = [b if a["status"] != FILE_VERIFIED
                    and b["status"] == FILE_VERIFIED else a
                    for a, b in zip(rows, staged)]
        ok = len([r for r in rows if r["status"] == FILE_VERIFIED])
        log(f"  {src.db}: WFDB open {ok}/{len(rows)} record(s)")
        wfdb_rows.extend(rows)

    duplicates = compare_duplicate_waveforms(asset_root)
    decision = evaluate_prep_decision(inventories, wfdb_rows, duplicates)
    log(f"decision: {decision['decision']} "
        f"({decision['n_gate_pass']}/{decision['n_gate_total']} gates)")
    if decision["first_stopping_reason"]:
        log(f"  first stopping reason: "
            f"{decision['first_stopping_reason']['gate']} — "
            f"{decision['first_stopping_reason']['detail']}")

    manifest = {
        "experiment_id": EXPERIMENT_ID, "arm_id": ARM_ID, "substage": SUBSTAGE,
        "timestamp": timestamp, "asset_root": asset_root,
        "staging_root": staging_root if os.path.isdir(staging_root) else None,
        "audit_dir": audit_dir,
        "environment": environment_manifest(),
        "sources": [{k: v for k, v in inv.items() if k != "files"}
                    for inv in inventories],
        "file_hashes": [{"database": f["database"], "rel_path": f["rel_path"],
                         "publisher_sha256": f["publisher_sha256"],
                         "observed_sha256": f["observed_sha256"],
                         "observed_bytes": f["observed_bytes"],
                         "status": f["status"], "final_url": f["final_url"]}
                        for inv in inventories for f in inv["files"]],
        "duplicate_waveform_comparison": duplicates,
        "training_performed": False, "delineation_performed": False,
        "analysis_performed": False,
        "elapsed_s": round(time.time() - t0, 2),
    }
    result = {
        "experiment_id": EXPERIMENT_ID, "arm_id": ARM_ID, "substage": SUBSTAGE,
        "mode": "PREP_DATA_ACQUIRE", "decision": decision["decision"],
        "n_files_required": sum(int(i["n_files"]) for i in inventories),
        "n_files_verified": sum(int(i["counts"].get(FILE_VERIFIED, 0))
                                for i in inventories),
        "observed_total_bytes": sum(int(i["observed_total_bytes"])
                                    for i in inventories),
        "wfdb_records_checked": len(wfdb_rows),
        "wfdb_records_ok": len([r for r in wfdb_rows
                                if r["status"] == FILE_VERIFIED]),
        "elapsed_s": manifest["elapsed_s"],
    }
    _write_audit(audit_dir, inventories, wfdb_rows, duplicates, decision,
                 manifest, result, log, timestamp)
    return {"decision": decision, "manifest": manifest, "result": result,
            "inventories": inventories, "wfdb": wfdb_rows,
            "duplicates": duplicates, "audit_dir": audit_dir,
            "run_dir": os.path.join(audit_dir, RUNS_SUBDIR, timestamp),
            "staging_root": manifest["staging_root"]}


def _write_audit(audit_dir: str, inventories, wfdb_rows, duplicates, decision,
                 manifest, result, log: RunLog,
                 timestamp: str = "") -> None:
    _dump_json(os.path.join(audit_dir, "config.json"), build_config())
    _dump_json(os.path.join(audit_dir, "asset_manifest.json"), manifest)
    _dump_json(os.path.join(audit_dir, "decision.json"), decision)
    _dump_csv(os.path.join(audit_dir, "source_inventory.csv"),
              [{k: v for k, v in inv.items()
                if k not in ("files", "conflicts", "records_declared",
                             "records_expected", "notes", "extensions")}
               | {"records_declared": ",".join(inv.get("records_declared", [])),
                  "notes": " | ".join(inv.get("notes", []))}
               for inv in inventories])
    _dump_csv(os.path.join(audit_dir, "checksum_report.csv"),
              [f for inv in inventories for f in inv["files"]])
    _dump_csv(os.path.join(audit_dir, "record_inventory.csv"),
              record_inventory(inventories, wfdb_rows, duplicates))
    _dump_csv(os.path.join(audit_dir, "wfdb_open_report.csv"), wfdb_rows)
    with open(os.path.join(audit_dir, "log.txt"), "w", encoding="utf-8") as fh:
        fh.write(log.text())
    _write_summary(audit_dir, inventories, wfdb_rows, decision, result)
    missing = [f for f in AUDIT_FILES
               if not os.path.exists(os.path.join(audit_dir, f))]
    if missing:
        raise Q5DError(f"audit bundle incomplete: {missing}")
    _archive_run(audit_dir, timestamp)


def _archive_run(audit_dir: str, timestamp: str) -> Optional[str]:
    """Keep one immutable copy of every acquisition under ``audit/runs/<ts>/``.

    ``audit/`` is the latest bundle, which a re-run replaces.  A stopped run is
    evidence — the file list and hashes that produced `INPUT_ABSENT_OR_MISMATCH`
    have to survive the next attempt, or the record of why it stopped is gone.
    """
    if not timestamp:
        return None
    run_dir = os.path.join(audit_dir, RUNS_SUBDIR, str(timestamp))
    if os.path.isdir(run_dir):        # never overwrite an archived run
        return run_dir
    os.makedirs(run_dir, exist_ok=True)
    for name in AUDIT_FILES:
        src = os.path.join(audit_dir, name)
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(run_dir, name))
    return run_dir


def record_inventory(inventories: Sequence[Dict[str, object]],
                     wfdb_rows: Sequence[Dict[str, object]],
                     duplicates: Sequence[Dict[str, object]] = (),
                     ) -> List[Dict[str, object]]:
    """One row per (database, record): the per-record table §4.10 asks for."""
    dup_by: Dict[str, List[str]] = {}
    for d in duplicates:
        dup_by.setdefault(str(d["record"]), []).append(
            f"{d['extension']}:{d['status']}")
    open_by = {(str(r.get("database")), str(r.get("record"))): r
               for r in wfdb_rows}
    rows: List[Dict[str, object]] = []
    for inv in inventories:
        db = str(inv["database"])
        src = SOURCE_BY_DB[db]
        by_rec: Dict[str, List[Dict[str, object]]] = {}
        for f in inv["files"]:
            if f.get("kind") == "record":
                by_rec.setdefault(str(f["record"]), []).append(f)
        for rec in [str(r) for r in inv.get("records_declared", [])]:
            files = by_rec.get(rec, [])
            present = [str(f["extension"]) for f in files
                       if f["status"] == FILE_VERIFIED]
            opened = open_by.get((db, rec))
            all_ext = sorted(set(src.extensions)) == sorted(set(present))
            rows.append({
                "database": db, "version": inv["version"], "record": rec,
                "extensions_required": "|".join(src.extensions),
                "extensions_verified": "|".join(sorted(present)),
                "all_extensions_verified": all_ext,
                "observed_bytes": sum(int(f.get("observed_bytes") or 0)
                                      for f in files),
                "wfdb_status": (opened or {}).get("status", "NOT_CHECKED"),
                "fs": (opened or {}).get("fs", ""),
                "n_sig": (opened or {}).get("n_sig", ""),
                "sig_names": (opened or {}).get("sig_names", ""),
                "ann_ext": (opened or {}).get("ann_ext", ""),
                "ann_count": (opened or {}).get("ann_count", ""),
                "ann_in_range": (opened or {}).get("ann_in_range", ""),
                "duplicate_waveform": ",".join(dup_by.get(rec, [])),
                "status": (FILE_VERIFIED
                           if all_ext and (opened or {}).get("status")
                           == FILE_VERIFIED else FILE_MISSING
                           if not all_ext else FILE_OPEN_FAILED),
                "detail": (opened or {}).get("detail", ""),
            })
    return rows


def _write_summary(audit_dir: str, inventories, wfdb_rows, decision,
                   result) -> None:
    d = decision["decision"]
    lines = [
        f"# {EXPERIMENT_ID} / {SUBSTAGE}",
        "",
        f"- **{NO_SCIENCE_BANNER}**",
        f"- 판정: **{d}**  ({decision['n_gate_pass']}/"
        f"{decision['n_gate_total']} gate pass)",
        "- 이 판정은 **데이터 준비 결과**이고 EXP-2026-007의 과학적 판정이 아니다.",
        "",
        "## 소스",
        "",
    ]
    for inv in inventories:
        lines.append(
            f"- `{inv['database']} {inv['version']}` DOI `{inv['doi']}` · "
            f"{inv['files_url']} · license {inv['license_name']}")
        lines.append(
            f"  - RECORDS {inv['n_records_declared']}개 (기대 "
            f"{inv['n_records_expected']}개, 일치 {inv['records_match']}) · "
            f"checksum pass {inv['checksum_pass_fraction']:.3f} "
            f"({inv['counts'].get(FILE_VERIFIED, 0)}/{inv['n_files']}) · "
            f"관측 {inv['observed_total_bytes'] / 1e6:.1f} MB "
            f"(공개 트리 참고치 ~{inv['approx_expected_mb']:.1f} MB)")
        lines.append(f"  - SHA256SUMS.txt sha256 `{inv['sha256sums_sha256']}`")
    ok = len([r for r in wfdb_rows if r["status"] == FILE_VERIFIED])
    lines += [
        "",
        "## WFDB open",
        "",
        f"- {ok}/{len(wfdb_rows)} record 통과 (record 100·101만 보고 전체를 "
        "통과로 표시하지 않는다 — 표는 record 단위로 전부 있다)",
        "",
        "## Gate",
        "",
    ]
    for g in decision["gates"]:
        lines.append(f"- {'PASS' if g['pass'] else 'FAIL'} `{g['gate']}` — "
                     f"{g['detail']}")
    if decision["first_stopping_reason"]:
        fr = decision["first_stopping_reason"]
        lines += ["", f"**첫 중단 사유**: `{fr['gate']}` — {fr['detail']}"]
    lines += [
        "",
        "## 다음 단계",
        "",
        f"- {decision['permitted_next_step']}",
        "- P-wave delineation · P-to-R 계산 · DS2 outcome · S PR-AUC · SHAM "
        "permutation · 모델 학습은 이 단계에서 **하지 않았다**.",
        "",
    ]
    with open(os.path.join(audit_dir, "summary.md"), "w",
              encoding="utf-8") as fh:
        fh.write("\n".join(lines))


def report_bundle(asset_root: str) -> Dict[str, object]:
    """PREP_DATA_REPORT: read a stored bundle back.  Recomputes nothing."""
    audit_dir = os.path.join(asset_root, AUDIT_SUBDIR)
    out: Dict[str, object] = {"asset_root": asset_root, "audit_dir": audit_dir,
                              "recomputed": False}
    if not os.path.isdir(audit_dir):
        out.update({"decision": DECISION_NOT_RUN,
                    "reason": f"no acquisition bundle at {audit_dir}"})
        return out
    for name in ("decision.json", "asset_manifest.json", "config.json"):
        p = os.path.join(audit_dir, name)
        if os.path.exists(p):
            with open(p, encoding="utf-8") as fh:
                out[name[:-5]] = json.load(fh)
    p = os.path.join(audit_dir, "summary.md")
    if os.path.exists(p):
        with open(p, encoding="utf-8") as fh:
            out["summary"] = fh.read()
    dec = (out.get("decision") or {})
    out["decision"] = (dec.get("decision", DECISION_NOT_RUN)
                       if isinstance(dec, dict) else DECISION_NOT_RUN)
    out["decision_detail"] = dec if isinstance(dec, dict) else {}
    missing = [f for f in AUDIT_FILES
               if not os.path.exists(os.path.join(audit_dir, f))]
    out["missing_audit_files"] = missing
    runs_dir = os.path.join(audit_dir, RUNS_SUBDIR)
    out["archived_runs"] = (sorted(os.listdir(runs_dir))
                            if os.path.isdir(runs_dir) else [])
    if missing:
        out["decision"] = DECISION_NOT_RUN
        out["reason"] = f"incomplete bundle, missing {missing}"
    return out


# ─────────────────────────────────────────────────────────────────────────────
# Notebook-facing display
# ─────────────────────────────────────────────────────────────────────────────
def design_card(asset_root: str = "", mode: str = "DESIGN") -> str:
    """The first screen: what will happen, where, and what will not happen."""
    lines = [
        "=" * 72,
        f"  {HEADLINE}",
        f"  {NO_SCIENCE_BANNER}",
        "=" * 72,
        f"  mode           : {mode}",
        f"  status         : {STATUS}",
        f"  drive target   : {asset_root or DRIVE_ASSET_REL}",
    ]
    for s in SOURCES:
        lines.append(f"  source         : {s.db} {s.version} · DOI {s.doi} · "
                     f"{len(s.records_expected)} records · "
                     f"~{s.approx_uncompressed_mb:.1f} MB · {s.files_url}")
    lines += [
        f"  extensions     : mitdb {'/'.join(SOURCE_MITDB.extensions)} · "
        f"pwave {'/'.join(SOURCE_PWAVE.extensions)}",
        "  immutability   : 기존 파일·폴더를 덮어쓰거나 삭제하지 않는다. 같은 "
        "경로에 내용이 다르면 EXISTING_ASSET_CONFLICT로 중단한다.",
        "  NOT performed  : delineation · P-to-R · RR/coupling · DS2 outcome · "
        "S PR-AUC · SHAM permutation · training",
        f"  decision codes : {' | '.join(DECISIONS)}",
        "-" * 72,
        "  Colab 실행 순서",
        "   1) repo 준비 + commit SHA 확인",
        "   2) Google Drive mount",
        "   3) mode DESIGN 실행",
        "   4) 예상 경로·용량 확인",
        "   5) mode PREP_DATA_ACQUIRE 로 바꿔 전체 실행",
        "   6) 판정과 checksum gate 확인",
        "   7) mode PREP_DATA_REPORT 로 저장 bundle 재표시",
        "   8) 출력 포함 notebook 저장",
        "   9) 여기서 중단하고 결과 보고",
        "=" * 72,
    ]
    return "\n".join(lines)


def render_gate_card(decision: Dict[str, object],
                     inventories: Sequence[Dict[str, object]] = (),
                     wfdb_rows: Sequence[Dict[str, object]] = ()) -> str:
    """The one-screen result card the notebook prints after an acquisition."""
    d = str(decision.get("decision", DECISION_NOT_RUN))
    lines = ["=" * 72, f"  {HEADLINE}", f"  DECISION: {d}", "=" * 72]
    for inv in inventories:
        db = inv["database"]
        exp = len(SOURCE_BY_DB[db].records_expected)
        lines.append(
            f"  {db:<6} records {inv['n_records_declared']}/{exp} "
            f"{'OK ' if inv['records_match'] else 'MISMATCH'} · "
            f"files {inv['counts'].get(FILE_VERIFIED, 0)}/{inv['n_files']} "
            f"verified · missing {inv['counts'].get(FILE_MISSING, 0)} · "
            f"hash-mismatch {inv['counts'].get(FILE_HASH_MISMATCH, 0)} · "
            f"{inv['observed_total_bytes'] / 1e6:.1f} MB")
    for src in SOURCES:
        rows = [r for r in wfdb_rows if r.get("database") == src.db]
        ok = len([r for r in rows if r["status"] == FILE_VERIFIED])
        lines.append(f"  {src.db:<6} WFDB open {ok}/{len(rows)}")
    lines.append("-" * 72)
    for g in decision.get("gates", []):
        lines.append(f"  [{'PASS' if g['pass'] else 'FAIL'}] {g['gate']}: "
                     f"{g['detail']}")
    fr = decision.get("first_stopping_reason")
    if fr:
        lines += ["-" * 72, f"  FIRST STOPPING REASON: {fr['gate']}",
                  f"  {fr['detail']}"]
        for ev in list(fr.get("evidence") or [])[:10]:
            lines.append(f"    - {ev}")
    lines += ["-" * 72,
              "  다음 단계는 자동 실행되지 않는다 — qualification·DS2 분석·학습은",
              "  이 bundle을 사람이 검토한 뒤 별도 승인으로만 시작한다.",
              "=" * 72]
    return "\n".join(lines)


def progress_printer(every: int = 12) -> Progress:
    """A quiet-by-default progress callback for the notebook."""
    state = {"last": 0.0}

    def _p(ev: Dict[str, object]) -> None:
        if ev.get("scope") in ("file", "wfdb"):
            i, n = int(ev.get("index", 0)), int(ev.get("total", 0)) or 1
            if i == n or i % max(1, every) == 0 or ev.get("status") not in (
                    FILE_VERIFIED, None):
                bar_n = int(24 * i / n)
                print(f"  [{'#' * bar_n}{'.' * (24 - bar_n)}] "
                      f"{ev.get('scope')} {ev.get('db')} {i}/{n} "
                      f"{ev.get('record', '')}{ev.get('extension', '')} "
                      f"{ev.get('status', '')}", flush=True)
            return
        now = time.time()
        if now - state["last"] > 2.0:
            state["last"] = now
            total = ev.get("total")
            mb = float(ev.get("bytes", 0)) / 1e6
            tot = f"/{float(total) / 1e6:.1f}" if total else ""
            print(f"    {os.path.basename(str(ev.get('dest')))}: "
                  f"{mb:.1f}{tot} MB in {float(ev.get('elapsed_s', 0)):.1f}s",
                  flush=True)
    return _p


def self_check(min_version: int = MODULE_VERSION) -> Dict[str, object]:
    if MODULE_VERSION < min_version:
        raise Q5DError(f"stale module {MODULE_VERSION} < {min_version}")
    return {
        "experiment_id": EXPERIMENT_ID, "arm_id": ARM_ID, "substage": SUBSTAGE,
        "module_version": MODULE_VERSION, "module_build": MODULE_BUILD,
        "status": STATUS, "modes": list(MODES),
        "forbidden_modes": list(FORBIDDEN_MODES),
        "decisions": list(DECISIONS),
        "sources": [{"database": s.db, "version": s.version, "doi": s.doi,
                     "files_url": s.files_url,
                     "n_records_expected": len(s.records_expected),
                     "extensions": list(s.extensions),
                     "approx_uncompressed_mb": s.approx_uncompressed_mb}
                    for s in SOURCES],
        "drive_asset_rel": DRIVE_ASSET_REL,
        "audit_files": list(AUDIT_FILES),
        "acquire_only": assert_acquire_only(),
    }


def main(argv: Optional[Sequence[str]] = None) -> int:
    import argparse
    ap = argparse.ArgumentParser(description=f"{EXPERIMENT_ID} / {SUBSTAGE}")
    ap.add_argument("--mode", default="DESIGN")
    ap.add_argument("--asset-root", default="",
                    help="Drive asset root (PREP_DATA_REPORT)")
    args = ap.parse_args(argv)
    mode = resolve_mode(args.mode)
    if mode == "DESIGN":
        print(design_card(args.asset_root, mode))
        print(json.dumps(self_check(), ensure_ascii=False, indent=1,
                         default=str))
        return 0
    if mode == "PREP_DATA_REPORT":
        print(json.dumps(report_bundle(args.asset_root), ensure_ascii=False,
                         indent=1, default=str))
        return 0
    raise SystemExit(
        "PREP_DATA_ACQUIRE runs from the notebook: it needs the mounted Drive "
        "asset path and a user-supplied timestamp.")


if __name__ == "__main__":                            # pragma: no cover
    raise SystemExit(main())
