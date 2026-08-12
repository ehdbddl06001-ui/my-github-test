"""
anatomy_ingest.py — 원본 PDF(binary lane)·텍스트 스냅샷(text lane)의 증분 인제스트.

binary lane (사용자가 `.private/anatomy/originals/<source-id>.pdf` 로 제공):
  - SHA-256이 source_doc 카드와 다르면 새 revision으로 페이지 분해(원본 불변).
  - 페이지 PNG + 페이지수는 `.private/anatomy/pages/<source-id>/rev-<n>/` 에 저장.
  - source_doc 카드의 sha256/pages/status(`ingested`)를 갱신.

text lane (Drive MCP 텍스트 추출 — 페이지 번호가 없다):
  - `--text-snapshot <txt> --source-id <sid>` 로 스냅샷을 등록(사본을 private에 보관).
  - 카드 status는 `text_ingested`. 페이지 번호를 지어내지 않는다(spec D1).

안전:
  - 원본을 절대 덮어쓰거나 지우지 않는다.
  - 실패 파일은 조용히 넘기지 않고 error manifest(`.private/anatomy/errors.json`)와
    종료 코드 1로 알린다.
  - 인증/네트워크 없음 → 아무것도 지우지 않고 현재 상태만 보고.

사용:
  python pipelines/anatomy_ingest.py [--dry-run] [--source-id a2-s14]
      [--private-assets-dir .private/anatomy]
  python pipelines/anatomy_ingest.py --text-snapshot state/.a2-s14.txt --source-id a2-s14
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
from datetime import date
from pathlib import Path

try:
    from frontmatter import split_frontmatter
except ModuleNotFoundError:
    from pipelines.frontmatter import split_frontmatter

import yaml

ROOT = Path(__file__).resolve().parent.parent
SOURCES_DIR = ROOT / "content" / "anatomy" / "sources"
DEFAULT_PRIVATE = ROOT / ".private" / "anatomy"


def sha256_of(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return "sha256:" + h.hexdigest()


def _cards() -> dict[str, tuple[Path, dict, str]]:
    """{source_id: (path, meta, body)}"""
    out = {}
    if SOURCES_DIR.exists():
        for p in sorted(SOURCES_DIR.glob("*.md")):
            meta, body = split_frontmatter(p.read_text(encoding="utf-8"))
            if meta.get("kind") == "source_doc" and meta.get("source_id"):
                out[str(meta["source_id"])] = (p, meta, body)
    return out


def _save_card(p: Path, meta: dict, body: str, dry: bool) -> None:
    if dry:
        return
    text = "---\n" + yaml.safe_dump(
        meta, allow_unicode=True, sort_keys=False, default_flow_style=None, width=100
    ) + "---\n\n" + body
    p.write_text(text, encoding="utf-8")


def split_pdf(pdf: Path, out_dir: Path, dry: bool) -> int:
    """PDF → 페이지 PNG(원본 불변). 이미 있으면 건너뜀(idempotent). 페이지수 반환."""
    import fitz  # PyMuPDF

    doc = fitz.open(pdf)
    n = doc.page_count
    if not dry:
        out_dir.mkdir(parents=True, exist_ok=True)
        for i in range(n):
            png = out_dir / f"page-{i + 1:04d}.png"
            if png.exists():
                continue
            pix = doc[i].get_pixmap(dpi=150)
            pix.save(png)
    doc.close()
    return n


def ingest_binaries(private: Path, only: str | None, dry: bool) -> tuple[int, list[dict]]:
    originals = private / "originals"
    errors: list[dict] = []
    n_done = 0
    cards = _cards()
    if not originals.exists():
        print(f"[INFO] {originals} 없음 — binary lane 건너뜀(기존 자료는 유지)")
        return 0, errors
    for pdf in sorted(originals.glob("*.pdf")):
        sid = pdf.stem
        if only and sid != only:
            continue
        if sid not in cards:
            errors.append({"source_id": sid, "error": "source_doc 카드 없음 — inventory 먼저"})
            continue
        p, meta, body = cards[sid]
        try:
            digest = sha256_of(pdf)
            rev = int(meta.get("revision", 1))
            if meta.get("sha256") == digest and meta.get("status") == "ingested":
                print(f"[SAME] {sid} (rev {rev}) — 해시 동일, 건너뜀")
                continue
            if meta.get("sha256") and meta.get("sha256") != digest:
                rev += 1  # 같은 file ID라도 내용이 바뀌면 새 revision
            pages_dir = private / "pages" / sid / f"rev-{rev}"
            n = split_pdf(pdf, pages_dir, dry)
            meta.update({
                "sha256": digest, "pages": n, "revision": rev,
                "status": "ingested", "updated": date.today().isoformat(),
                "asset_ref": str(pages_dir.relative_to(ROOT)),
            })
            _save_card(p, meta, body, dry)
            n_done += 1
            print(f"[ OK ] {sid}: {n}페이지 → {pages_dir.relative_to(ROOT)}"
                  f"{' (dry-run)' if dry else ''}")
        except Exception as e:  # 실패를 조용히 넘기지 않는다
            errors.append({"source_id": sid, "error": str(e)})
    return n_done, errors


def ingest_text(snapshot: Path, sid: str, private: Path, dry: bool) -> tuple[int, list[dict]]:
    cards = _cards()
    if sid not in cards:
        return 0, [{"source_id": sid, "error": "source_doc 카드 없음 — inventory 먼저"}]
    if not snapshot.exists():
        return 0, [{"source_id": sid, "error": f"스냅샷 없음: {snapshot}"}]
    p, meta, body = cards[sid]
    digest = sha256_of(snapshot)
    dst = private / "text" / f"{sid}.txt"
    if not dry:
        dst.parent.mkdir(parents=True, exist_ok=True)
        if snapshot.resolve() != dst.resolve():
            shutil.copyfile(snapshot, dst)
    if meta.get("text_sha256") == digest and meta.get("status", "").startswith("text"):
        print(f"[SAME] {sid} 텍스트 스냅샷 동일 — 건너뜀")
        return 0, []
    meta.update({
        "text_sha256": digest,
        "status": "text_ingested" if meta.get("status") != "ingested" else "ingested",
        "extraction": "drive-mcp-text",
        "updated": date.today().isoformat(),
    })
    _save_card(p, meta, body, dry)
    print(f"[ OK ] {sid}: 텍스트 스냅샷 등록 ({digest[:18]}…){' (dry-run)' if dry else ''}")
    return 1, []


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--source-id")
    ap.add_argument("--private-assets-dir", default=str(DEFAULT_PRIVATE))
    ap.add_argument("--text-snapshot", help="text lane: MCP 추출 텍스트 파일")
    a = ap.parse_args()
    private = Path(a.private_assets_dir)
    if not private.is_absolute():
        private = ROOT / private

    if a.text_snapshot:
        if not a.source_id:
            print("--text-snapshot 은 --source-id 가 필요합니다")
            return 2
        n, errors = ingest_text(Path(a.text_snapshot), a.source_id, private, a.dry_run)
    else:
        n, errors = ingest_binaries(private, a.source_id, a.dry_run)

    if errors:
        err_path = private / "errors.json"
        if not a.dry_run:
            err_path.parent.mkdir(parents=True, exist_ok=True)
            err_path.write_text(json.dumps(errors, ensure_ascii=False, indent=2),
                                encoding="utf-8")
        for e in errors:
            print(f"[FAIL] {e['source_id']}: {e['error']}")
        return 1
    print(f"ingest 완료: {n}건 처리")
    return 0


if __name__ == "__main__":
    sys.exit(main())
