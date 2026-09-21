"""harrison_split.py — 해리슨 21판을 **장별 텍스트 문서**로 나눠 사용자 드라이브에 두고, 장 → 파일 ID 표를 만든다.

왜(2026-09-22 사용자 지시 「해리슨을 기본으로 대조」): 클라우드 루틴 컨테이너에는 PC 의 G: 드라이브가 없고
4,132쪽 원본은 한 번에 읽을 수도 없다. 장별로 나눠 두면 루틴이 Google Drive 커넥터
(`read_file_content`)로 **그 장 하나만** 텍스트로 읽어 대조할 수 있다(57장 9쪽 ≈ 59 KB 텍스트 실측).

- 파일은 사용자 드라이브 `내 드라이브/교과서/Harrison_21e_장별/H21_<장>`(Google 문서, 원본 옆, 비공개 그대로). 원본은 건드리지 않는다.
- PDF 로 나누면 434 MB 원본만큼 드라이브를 더 쓰고, 새 PDF 는 드라이브가 색인할 때까지 빈 글로 읽힌다(2026-09-22 실측).
  루틴은 어차피 텍스트만 읽으므로 **쪽마다 `===== [H21 p.<인쇄쪽>] =====` 을 박은 텍스트**를 Google 문서로 올린다.
  그림·표 배치가 필요하면 PC 에서 원본 PDF 를 `harrison_read.py` 로 본다.
- 저장소에는 **파일 ID 표**(`content/outline/harrison_drive.json`)만 둔다. 교과서 본문은 저장소에 넣지 않는다.
- 이미 올라간 장은 다시 올리지 않는다(rclone copy 가 크기·시각으로 건너뜀). `--force` 는 다시 만든다.

사용(PC 에서, 한 번):
  python pipelines/harrison_split.py                 # 나누기 → 올리기 → ID 표
  python pipelines/harrison_split.py --only 57,255   # 일부 장만
  python pipelines/harrison_split.py --needed        # 정리본이 자리 잡은 장 중 아직 없는 것만(필요할 때만 올리기)
  python pipelines/harrison_split.py --ids-only      # 드라이브 목록만 다시 읽어 ID 표 갱신
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "pipelines"))
import harrison_toc as ht                                        # noqa: E402

OUT = ROOT / "content" / "outline" / "harrison_drive.json"
TEXTBOOK_FOLDER = "13w6B2aVzC2reEIUr9ScqdYunb_aCjdIn"             # 내 드라이브 › 교과서 (2026-09-22 확인)
SUBFOLDER = "Harrison_21e_장별"
RCLONE = os.environ.get("RCLONE") or str(Path.home() / "Downloads" / "rclone-v1.74.3-windows-amd64"
                                         / "rclone-v1.74.3-windows-amd64" / "rclone.exe")
REMOTE = "gdrive"


def name(n: int) -> str:
    return f"H21_{n:03d}.txt"


def rclone(*args: str, timeout: int = 3600) -> str:
    # 구글 문서를 .txt 로 보고 다루게 한다(가져오기·내보내기 형식이 같아야 rclone 이 변환을 허락한다)
    cmd = [RCLONE, *args, "--drive-root-folder-id", TEXTBOOK_FOLDER, "--drive-export-formats", "txt"]
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", timeout=timeout)
    if r.returncode != 0:
        raise RuntimeError(f"rclone {' '.join(args[:2])} 실패: {r.stderr.strip()[:400]}")
    return r.stdout


def split(chapters: list[dict], offset: int, pdf: Path, out: Path, force: bool) -> int:
    import pymupdf

    src = pymupdf.open(pdf)
    made = 0
    for c in chapters:
        f = out / name(c["n"])
        if f.exists() and not force:
            continue
        parts = [f"해리슨 21판 {c['n']}장 — {c['title']} (인쇄쪽 {c['page']}~{c['pdf_end'] - offset})",
                 f"절: {c.get('section') or '-'}", ""]
        for i in range(c["pdf"], c["pdf_end"] + 1):
            parts.append(f"===== [H21 p.{i - offset}] =====")
            parts.append(src[i].get_text().strip())
            parts.append("")
        f.write_text(chr(10).join(parts), encoding="utf-8")
        made += 1
    return made


def list_ids() -> dict[int, str]:
    rows = json.loads(rclone("lsjson", f"{REMOTE}:{SUBFOLDER}", timeout=300) or "[]")
    out = {}
    for r in rows:
        n = r.get("Name", "")
        # 내보내기 형식을 txt 로 준 탓에 구글 문서도 text/plain · 크기 -1 로 보인다(크기 -1 = 구글 문서)
        if n.startswith("H21_") and n.endswith(".txt") and r.get("Size") == -1:
            out[int(n[4:7])] = r["ID"]
    return out


def existing_ids() -> dict[int, str]:
    if OUT.exists():
        return {int(k): v for k, v in json.loads(OUT.read_text(encoding="utf-8")).get("chapters", {}).items()}
    return {}


def needed_chapters() -> set[int]:
    """정리본이 자리 잡은 슬롯의 해리슨 장(= 대조에 실제로 쓰일 장)."""
    import outline as ol
    from concepts import load_concepts
    idx = ol.index(ol.load()[0])
    concepts, _ = load_concepts()
    return {n for c in concepts.values() for n in (idx.get(str(c.get("outline") or "")).chapters
                                                   if idx.get(str(c.get("outline") or "")) else [])}


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--pdf", default=str(ht.DEFAULT_PDF))
    ap.add_argument("--only", help="쉼표로 장 번호")
    ap.add_argument("--work", default=str(Path(tempfile.gettempdir()) / "harrison_ch"))
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--ids-only", action="store_true")
    ap.add_argument("--needed", action="store_true", help="정리본의 기본틀 슬롯이 가리키는 장 가운데 드라이브에 없는 것만")
    a = ap.parse_args(argv)

    toc = ht.load()
    chapters = toc["chapters"]
    if a.only:
        want = {int(x) for x in a.only.split(",") if x.strip()}
        chapters = [c for c in chapters if c["n"] in want]
    if a.needed:
        want = needed_chapters() - set(existing_ids())
        chapters = [c for c in chapters if c["n"] in want]
        print(f"필요한데 드라이브에 없는 장: {sorted(want) or '없음'}")
        if not chapters:
            return 0

    if not a.ids_only:
        work = Path(a.work)
        work.mkdir(parents=True, exist_ok=True)
        made = split(chapters, toc["offset"], Path(a.pdf), work, a.force)
        print(f"나눔 {made}개(이미 있던 것 제외) → {work}")
        rclone("mkdir", f"{REMOTE}:{SUBFOLDER}", timeout=120)
        files = [name(c["n"]) for c in chapters]
        lst = work / "_files.txt"
        lst.write_text("\n".join(files), encoding="utf-8")
        # .txt → Google 문서로 변환해 올린다(드라이브 용량을 거의 쓰지 않고, 올리자마자 커넥터로 읽힌다)
        rclone("copy", str(work), f"{REMOTE}:{SUBFOLDER}", "--files-from", str(lst),
               "--drive-import-formats", "txt", "--transfers", "4", "--checkers", "8", "--tpslimit", "8")
        print(f"올림: {SUBFOLDER} ({len(files)}개 대상)")

    ids = list_ids()
    missing = [c["n"] for c in toc["chapters"] if c["n"] not in ids]
    data = {"note": "해리슨 21판 장별 텍스트(사용자 드라이브의 Google 문서, 비공개). 루틴은 Google Drive 커넥터 "
                    "read_file_content 로 그 장만 읽는다. `===== [H21 p.N] =====` 뒤가 인쇄쪽 N 의 본문이다.",
            "folder": f"내 드라이브/교과서/{SUBFOLDER}", "parent_folder_id": TEXTBOOK_FOLDER,
            "chapters": {str(n): ids[n] for n in sorted(ids)}}
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
    print(f"ID 표 {len(ids)}개 — {OUT.relative_to(ROOT)}" + (f" · 아직 없는 장 {len(missing)}개" if missing else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
