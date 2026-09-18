"""drive_books.py — 검증을 통과한 과별 학습서를 Google Drive 에 갱신한다(rclone).

지키는 것(2026-09-18 사용자 지시)
- **폴더 ID 로만** 가리킨다(`--drive-root-folder-id`). 그 폴더의 **우리가 만든 이름**(MedKOS_학습서_*.pdf, archive/)만 쓴다.
  관계없는 파일은 읽기만 하고 고치지 않는다. 아무것도 지우지 않는다.
- 최신본은 **같은 파일 ID** 로 갱신한다(rclone 은 같은 이름의 기존 객체를 update 한다 — 올린 뒤 ID 를 다시 읽어 확인한다).
- 날짜·버전이 붙은 사본은 archive/ 에 따로 남긴다(이미 있으면 건너뜀 — 중복 업로드 없음).
- **사용자 필기 보호**: 드라이브의 최신본 md5 가 우리가 마지막으로 올린 md5 와 다르면(아이패드에서 직접 필기·수정)
  덮어쓰지 않고 멈춘 뒤 보고한다. 관리 기록이 없는 같은 이름 파일도 덮어쓰지 않는다. 같은 이름이 둘 이상이어도 멈춘다.
- 인증 정보는 rclone 설정 파일(PC: %APPDATA%\\rclone\\rclone.conf, Actions: 시크릿 RCLONE_CONF_BASE64)에만 있다.
  여기서 읽거나 출력하지 않는다.
- 실제로 올리지 못했으면 「완료」라고 쓰지 않는다 — 결과는 항목별 상태(uploaded/unchanged/skipped/failed)로 남긴다.
"""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
from datetime import datetime, timedelta, timezone
from pathlib import Path

KST = timezone(timedelta(hours=9))


def rclone_bin() -> str | None:
    for c in (os.environ.get("RCLONE_BIN"), shutil.which("rclone"),
              str(Path.home() / "Downloads" / "rclone-v1.74.3-windows-amd64" / "rclone.exe")):
        if c and Path(c).exists():
            return c
    return None


def md5(p: Path) -> str:
    h = hashlib.md5()
    with p.open("rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


class Remote:
    def __init__(self, remote: str, folder_id: str, binary: str):
        self.base = [binary, "--drive-root-folder-id", folder_id]
        self.remote = remote.rstrip(":") + ":"

    def _run(self, args: list[str], timeout: int = 600) -> subprocess.CompletedProcess:
        return subprocess.run(self.base + args, capture_output=True, text=True, encoding="utf-8", timeout=timeout)

    def ls(self, sub: str = "") -> list[dict]:
        r = self._run(["lsjson", self.remote + sub, "--files-only", "--hash", "--hash-type", "md5", "--no-mimetype"])
        if r.returncode != 0:
            if "directory not found" in (r.stderr or ""):
                return []
            raise RuntimeError(f"rclone lsjson 실패: {(r.stderr or '').strip()[-300:]}")
        return json.loads(r.stdout or "[]")

    def put(self, local: Path, name: str) -> None:
        r = self._run(["copyto", str(local), self.remote + name, "--ignore-times"])
        if r.returncode != 0:
            raise RuntimeError(f"rclone copyto 실패: {(r.stderr or '').strip()[-300:]}")

    def get_dir(self, local: Path, include: str = "*.json") -> None:
        local.mkdir(parents=True, exist_ok=True)
        r = self._run(["copy", self.remote, str(local), "--include", include, "--max-depth", "1"])
        if r.returncode != 0:
            raise RuntimeError(f"rclone copy 실패: {(r.stderr or '').strip()[-300:]}")


def _entry(entries: list[dict], name: str) -> list[dict]:
    return [e for e in entries if e.get("Name") == name]


def upload(cfg: dict, state_dir: Path, out_dir: Path, run: dict) -> dict:
    drv = cfg.get("drive") or {}
    folder = os.environ.get("MEDKOS_BOOKS_FOLDER_ID") or drv.get("folder_id") or ""
    res: dict = {"result": "ok", "items": {}, "at": datetime.now(KST).isoformat(timespec="seconds")}
    manifest_path = state_dir / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8")) if manifest_path.exists() else {"books": {}}
    if not folder:
        res.update(result="not_configured",
                   note="books_config.yaml drive.folder_id(또는 환경변수 MEDKOS_BOOKS_FOLDER_ID)가 비어 있어 업로드하지 않았다.")
        return _finish(state_dir, run, res)
    binary = rclone_bin()
    if not binary:
        res.update(result="failed", note="rclone 실행 파일을 찾지 못했다(RCLONE_BIN 또는 PATH).")
        return _finish(state_dir, run, res)
    rem = Remote(drv.get("remote", "gdrive"), folder, binary)
    try:
        top = rem.ls()
        arch = rem.ls("archive") if drv.get("archive", True) else []
    except Exception as e:
        res.update(result="failed", note=str(e))
        return _finish(state_dir, run, res)

    targets = [(t, manifest["books"][t]) for t in run.get("built", []) if t in manifest["books"]]
    # 이전 실행에서 올리지 못한 책(업로드 기록이 최신 판보다 오래됨)도 다시 시도한다 — 멱등
    for t, m in manifest["books"].items():
        if t not in dict(targets) and (m.get("drive") or {}).get("version") != m.get("version") and (out_dir / m["file"]).exists():
            targets.append((t, m))
    if manifest.get("index") and (out_dir / manifest["index"]["file"]).exists():
        targets.append(("__index__", manifest["index"]))
    for title, m in targets:
        local = out_dir / m["file"]
        name = m["file"]
        item: dict = {"file": name}
        res["items"][title] = item
        try:
            if not local.exists():
                raise RuntimeError("로컬 PDF 가 없다")
            lmd5 = md5(local)
            same = _entry(top, name)
            prev = m.get("drive") or {}
            if len(same) > 1:
                item.update(status="skipped", reason=f"같은 이름 파일이 {len(same)}개 — 어느 것을 갱신할지 모호해 멈춤(사람 정리 필요)")
                continue
            if same:
                rmd5 = ((same[0].get("Hashes") or {}).get("md5") or "").lower()
                if not prev.get("md5"):
                    item.update(status="skipped", reason="관리 기록이 없는 같은 이름 파일 — 사용자 파일일 수 있어 덮어쓰지 않음")
                    continue
                if rmd5 and rmd5 != prev["md5"]:
                    item.update(status="skipped", reason="드라이브 최신본이 마지막 업로드 뒤 바뀌었다(필기·수정 추정) — 덮어쓰지 않음. "
                                                         "필기본 이름을 바꾸거나 옮기면 다음 실행에서 새로 올린다")
                    continue
                if rmd5 == lmd5:
                    item.update(status="unchanged", id=same[0].get("ID"))
                    m["drive"] = {**prev, "id": same[0].get("ID"), "md5": lmd5, "version": m.get("version")}
                    continue
            before_id = same[0].get("ID") if same else None
            rem.put(local, name)
            after = _entry(rem.ls(), name)
            if len(after) != 1:
                raise RuntimeError(f"올린 뒤 같은 이름이 {len(after)}개")
            aid, amd5 = after[0].get("ID"), ((after[0].get("Hashes") or {}).get("md5") or "").lower()
            if amd5 != lmd5:
                raise RuntimeError("올린 뒤 md5 가 로컬과 다르다")
            if before_id and aid != before_id:
                raise RuntimeError(f"파일 ID 가 바뀌었다({before_id} → {aid}) — 새 파일로 만들어졌다")
            item.update(status="uploaded", id=aid, kept_id=bool(before_id), md5=lmd5)
            m["drive"] = {"id": aid, "md5": lmd5, "version": m.get("version"), "uploaded": res["at"]}
            # 날짜·버전 사본(책만)
            if title != "__index__" and drv.get("archive", True):
                aname = f"{Path(name).stem}_v{m.get('version')}_{m.get('date')}.pdf"
                if _entry(arch, aname):
                    item["archive"] = "exists"
                else:
                    rem.put(local, "archive/" + aname)
                    m.setdefault("archive", []).append(aname)
                    item["archive"] = aname
        except Exception as e:
            item.update(status="failed", reason=str(e)[:300])
    st = [i.get("status") for i in res["items"].values()]
    if any(s == "failed" for s in st):
        res["result"] = "failed" if not any(s == "uploaded" for s in st) else "partial"
    elif any(s == "skipped" for s in st):
        res["result"] = "partial"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
    return _finish(state_dir, run, res)


def pull_inbox(cfg: dict, inbox: Path) -> dict:
    """앱에서 내보낸 학습 기록(.json)을 드라이브 수신함에서 **읽어 오기만** 한다(드라이브 쪽은 그대로)."""
    drv = cfg.get("drive") or {}
    fid = os.environ.get("MEDKOS_INBOX_FOLDER_ID") or drv.get("inbox_folder_id") or ""
    if not fid:
        return {"result": "not_configured"}
    binary = rclone_bin()
    if not binary:
        return {"result": "failed", "note": "rclone 없음"}
    try:
        Remote(drv.get("remote", "gdrive"), fid, binary).get_dir(inbox)
        return {"result": "ok", "files": sorted(p.name for p in inbox.glob("*.json"))}
    except Exception as e:
        return {"result": "failed", "note": str(e)[:300]}


def _finish(state_dir: Path, run: dict, res: dict) -> dict:
    run["upload"] = res
    p = state_dir / "last_run.json"
    state_dir.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(run, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
    return res
