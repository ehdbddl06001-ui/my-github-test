#!/usr/bin/env python3
"""restore_store.py — 실사 복원 **설정을 커밋 대상으로** 보관하고 재현한다.

왜 필요한가(2026-08-18 실측): 실사 블랭크 문항이 쪽지시험의 실제 형태라 가장 중요한데,
복원 설정(`.private/anatomy/cfg/*.json`)과 결과 PNG 가 **둘 다 gitignore 된 `.private/`**
에만 있었다. 컨테이너가 바뀌면 통째로 사라져, main 에 문항 카드는 있는데 그 이미지를
다시 만들 방법이 없어진다 — 오늘 아침 루틴이 만든 5회차 8문항이 정확히 그렇게 됐다
(서브노트 PDF 31쪽에 실사 이미지가 0장).

설정 JSON 은 **좌표와 플래그뿐이라 카데바 픽셀이 없다** → 공개 repo 에 커밋해도 된다.
원본 스캔 PDF 만 다시 있으면 어느 컨테이너에서든 같은 결과를 재현한다.

저장 형식: `content/anatomy/restore/<render_dir>/<page>.json`
    {"page": "A044", "session": 5, "render_dir": "uploads-s05",
     "source": {"pages": 50, "page_no": 44, "hint": "5회차 스캔 A(1-50)"},
     "render_width": 1650, "cfg": { ...restore_scan 설정... }}

사용:
  python pipelines/restore_store.py --import        # .private/cfg → 커밋 저장소로 이관
  python pipelines/restore_store.py --rebuild       # 저장된 설정으로 PNG 재생성
  python pipelines/restore_store.py --audit         # 문항이 참조하는 이미지/설정 점검
  python pipelines/restore_store.py --selftest
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STORE = ROOT / "content/anatomy/restore"
PRIV = ROOT / ".private/anatomy"
UPLOADS = Path(os.environ.get("CLAUDE_UPLOADS", "/root/.claude/uploads"))

ASSET_RE = re.compile(r"^asset_ref:\s*(\.private/anatomy/render/([\w.-]+)/([\w.-]+)_quiz\.png)\s*$",
                      re.M)


def question_assets() -> list[tuple[Path, str, str]]:
    """(카드, render_dir, page) — 실사 이미지를 참조하는 문항 전부."""
    out = []
    for p in sorted((ROOT / "content/anatomy/questions").rglob("*.md")):
        m = ASSET_RE.search(p.read_text(encoding="utf-8"))
        if m:
            out.append((p, m.group(2), m.group(3)))
    return out


def store_path(render_dir: str, page: str) -> Path:
    return STORE / render_dir / f"{page}.json"


def configs() -> list[Path]:
    """커밋된 복원 설정들. `_` 로 시작하는 파일은 설정이 아니다 —
    `_rejected.json`(사람이 못 쓴다고 판정한 페이지 목록)이 여기 섞여 있다."""
    return sorted(p for p in STORE.rglob("*.json") if not p.name.startswith("_"))


def audit() -> dict:
    """문항이 참조하는 실사 이미지에 대해 (PNG 있음 / 설정 있음) 을 센다."""
    rows = []
    for card, rd, page in question_assets():
        png = PRIV / "render" / rd / f"{page}_quiz.png"
        rows.append({"card": card.name, "dir": rd, "page": page,
                     "png": png.exists(), "cfg": store_path(rd, page).exists()})
    return {"rows": rows,
            "no_png": [r for r in rows if not r["png"]],
            "no_cfg": [r for r in rows if not r["cfg"]]}


def _find_cfg(page: str) -> Path | None:
    """`.private/anatomy/cfg/` 에서 이 페이지의 설정 파일을 찾는다.

    옛 파일명 규칙이 제각각이라(`pf1_p44_supcluneal.json`, `s06_A010_cervbranch.json`)
    카드가 아는 **페이지 토큰**으로 되짚는 편이 확실하다.
    """
    src = PRIV / "cfg"
    if not src.exists():
        return None
    for cand in sorted(src.glob("*.json")):
        stem = cand.stem
        if stem.startswith(page + "_") or f"_{page}_" in stem or stem.endswith("_" + page):
            return cand
    return None


def import_legacy(dry: bool) -> int:
    """문항이 참조하는 실사마다 설정을 찾아 커밋 저장소로 옮긴다.

    카드가 (render_dir, page) 를 알고 있으므로 그것을 기준으로 되짚는다 —
    cfg 파일명 규칙에 기대지 않는다.
    """
    n = miss = 0
    for card, rd, page in question_assets():
        out = store_path(rd, page)
        if out.exists():
            continue
        cfg = _find_cfg(page)
        if cfg is None:
            miss += 1
            print(f"  설정 못 찾음: {rd}/{page}  ({card.name})")
            continue
        sess = re.match(r"uploads-s(\d\d)", rd)
        rec = {"page": page, "render_dir": rd,
               "session": int(sess.group(1)) if sess else None,
               "render_width": 1650,
               "source": {"hint": f"{rd} 업로드 스캔", "page_no": None, "pages": None},
               "cfg": json.loads(cfg.read_text(encoding="utf-8"))}
        print(f"  {'DRY ' if dry else 'SAVE'} {out.relative_to(ROOT)}  ← {cfg.name}")
        if not dry:
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
        n += 1
    print(f"{n}건 이관 · {miss}건 설정 없음{' (dry-run)' if dry else ''}")
    return 0


def rebuild(only: str | None, dry: bool) -> int:
    """저장된 설정 + 원본 렌더(src/*.png)로 clean/quiz PNG 를 다시 만든다."""
    todo = configs()
    if only:
        todo = [p for p in todo if only in str(p)]
    ok = fail = skip = 0
    for p in todo:
        rec = json.loads(p.read_text(encoding="utf-8"))
        rd, page = rec["render_dir"], rec["page"]
        src = PRIV / "render" / rd / "src" / f"{page}.png"
        if not src.exists():
            print(f"  SKIP {rd}/{page} — 원본 렌더 없음({src.relative_to(ROOT)}). "
                  f"스캔 PDF 를 다시 올려 렌더하면 재현된다")
            skip += 1
            continue
        tmp = PRIV / "cfg" / f"{rd}_{page}.json"
        tmp.parent.mkdir(parents=True, exist_ok=True)
        tmp.write_text(json.dumps(rec["cfg"], ensure_ascii=False), encoding="utf-8")
        if dry:
            print(f"  [dry] {rd}/{page}")
            ok += 1
            continue
        r = subprocess.run(
            [sys.executable, "pipelines/restore_scan.py", "--image", str(src),
             "--config", str(tmp),
             "--out-clean", str(PRIV / "render" / rd / f"{page}_clean.png"),
             "--out-quiz", str(PRIV / "render" / rd / f"{page}_quiz.png")],
            cwd=ROOT, capture_output=True, text=True)
        if r.returncode:
            print(f"  FAIL {rd}/{page}: {r.stderr.strip()[-160:]}")
            fail += 1
        else:
            ok += 1
    print(f"재생성 {ok} · 실패 {fail} · 원본없음 {skip}")
    return 1 if fail else 0


DATES_RE = re.compile(r"^scheduled_dates:\s*\[([^\]]*)\]", re.M)
BLOCK_RE = re.compile(r"^scan_questions:\n(?:[ \t]+- \{.*\n)+", re.M)


def _dates(text: str) -> set[str]:
    m = DATES_RE.search(text)
    return {s.strip().strip('"\'') for s in m.group(1).split(",") if s.strip()} if m else set()


def sync_subnote(card: Path, dry: bool) -> int:
    """서브노트 카드의 `scan_questions:` 를 **문항에서 다시 만든다**(결정론).

    이 목록을 손으로 유지하면 실사 문항을 늘려도 서브노트 PDF 에 안 실린다 —
    4회차를 15장에서 27장으로 늘렸을 때 실제로 15장까지만 나왔다(2026-08-18).
    같은 `scheduled_dates` 를 가진 실사 문항 전부를 페이지 순서로 싣는다.
    """
    text = card.read_text(encoding="utf-8")
    want = _dates(text)
    if not want:
        print(f"{card.name}: scheduled_dates 가 없다")
        return 2
    rows = []
    for qc, rd, page in question_assets():
        if not (_dates(qc.read_text(encoding="utf-8")) & want):
            continue
        rows.append((rd, page, qc.relative_to(ROOT).as_posix()))
    rows.sort(key=lambda r: (r[0], r[1]))
    if not rows:
        print(f"{card.name}: 붙일 실사 문항이 없다")
        return 0
    block = "scan_questions:\n" + "".join(
        f'  - {{card: "{c}", quiz_image: ".private/anatomy/render/{rd}/{p}_quiz.png",'
        f' clean_image: ".private/anatomy/render/{rd}/{p}_clean.png"}}\n'
        for rd, p, c in rows)
    new = BLOCK_RE.sub(lambda _m: block, text, count=1) if BLOCK_RE.search(text) else text
    old_n = len(BLOCK_RE.search(text).group(0).splitlines()) - 1 if BLOCK_RE.search(text) else 0
    print(f"{card.name}: 실사 문항 {old_n} → {len(rows)}{' (dry-run)' if dry else ''}")
    if not dry and new != text:
        card.write_text(new, encoding="utf-8")
    return 0


def selftest() -> int:
    a = audit()
    assert isinstance(a["rows"], list)
    # 저장 경로 규칙
    assert store_path("uploads-s05", "A044").name == "A044.json"
    assert store_path("uploads-s05", "A044").parent.name == "uploads-s05"
    # 설정에는 카데바 픽셀이 없다 — 좌표·플래그뿐이라 커밋해도 안전하다
    for p in configs()[:20]:
        rec = json.loads(p.read_text(encoding="utf-8"))
        assert set(rec) >= {"page", "render_dir", "cfg"}, p
        assert "base64" not in p.read_text(encoding="utf-8"), f"{p}: 이미지가 섞여 있다"
    print("[ OK ] restore_store selftest")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--import", dest="do_import", action="store_true")
    ap.add_argument("--rebuild", action="store_true")
    ap.add_argument("--only")
    ap.add_argument("--audit", action="store_true")
    ap.add_argument("--sync-subnote", dest="sync", help="서브노트 카드 경로")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if a.do_import:
        return import_legacy(a.dry_run)
    if a.rebuild:
        return rebuild(a.only, a.dry_run)
    if a.sync:
        return sync_subnote(ROOT / a.sync, a.dry_run)
    if a.audit:
        r = audit()
        print(f"실사 참조 문항 {len(r['rows'])}건 — PNG 없음 {len(r['no_png'])} · 설정 없음 {len(r['no_cfg'])}")
        for x in r["no_cfg"][:12]:
            print(f"  설정 없음: {x['dir']}/{x['page']}  ({x['card']})")
        return 0
    print("--import / --rebuild / --audit / --sync-subnote / --selftest 중 하나가 필요하다")
    return 2


if __name__ == "__main__":
    sys.exit(main())
