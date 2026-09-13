"""
import_wrong_sync.py — 웹/PWA 가 동기화한 오답(state/wrong_sync/<exam>.json)을 사람이 읽는
오답노트 .md 로 만든다.

흐름: 핸드폰·PC 의 퀴즈 → Cloudflare Pages Function(/api/wrong) → GitHub 커밋
      `state/wrong_sync/{kmle,usmle,imaging}.json` → (이 스크립트, GitHub Actions
      wrong-sync.yml 이 자동 실행) → 아래 파일을 다시 쓴다.

  kmle    → kmle/오답노트/웹동기화.md
  usmle   → usmle/오답노트/웹동기화.md
  imaging → kmle/오답노트/웹동기화_영상.md      (국시형·USMLE형이 섞인 영상 덱)

표 형식은 `kmle/오답노트/_양식.md` 를 따른다. JSON 이 Source of Truth 이고 .md 는 파생물이므로
파일 전체를 매번 다시 쓴다(손으로 고치지 말 것 — 「틀린 이유」 같은 자기 메모는 웹의 오답노트
화면에서 쓰면 JSON 에 같이 실린다).

사용: python pipelines/import_wrong_sync.py            # 전부 재생성
      python pipelines/import_wrong_sync.py --selftest
"""
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SYNC_DIR = ROOT / "state" / "wrong_sync"
TARGETS = {
    "kmle": ROOT / "kmle" / "오답노트" / "웹동기화.md",
    "usmle": ROOT / "usmle" / "오답노트" / "웹동기화.md",
    "imaging": ROOT / "kmle" / "오답노트" / "웹동기화_영상.md",
}
TITLE = {"kmle": "KMLE", "usmle": "USMLE", "imaging": "오픈데이터 영상(국시형·USMLE형)"}
CIRCLED = "①②③④⑤"
ALPHA = "ABCDE"


def label(idx, exam: str, style: str = "") -> str:
    try:
        i = int(idx)
    except (TypeError, ValueError):
        return "?"
    use_alpha = exam == "usmle" or (exam == "imaging" and style == "usmle_style")
    table = ALPHA if use_alpha else CIRCLED
    return table[i] if 0 <= i < len(table) else str(i + 1)


def _cell(v) -> str:
    return str(v if v is not None else "").replace("|", "\\|").replace("\n", " ").strip()


def render(exam: str, data: dict) -> str:
    items = list((data.get("items") or {}).values())
    items.sort(key=lambda w: (str(w.get("date", "")), str(w.get("id", ""))), reverse=True)
    out = [f"# {TITLE.get(exam, exam)} 오답노트 — 웹 동기화 (자동 생성)", "",
           f"원본: `state/wrong_sync/{exam}.json` · 총 {len(items)}개 · 갱신 {data.get('updated', '')[:19]}",
           "", "> 이 파일은 파이프라인이 다시 쓰는 파생물이다. 메모는 웹 오답노트 화면에서 남긴다.", ""]
    by_sub: dict[str, list] = {}
    for w in items:
        by_sub.setdefault(str(w.get("subject") or "기타"), []).append(w)
    for sub, rows in by_sub.items():
        out.append(f"## {sub} ({len(rows)})")
        out.append("")
        for n, w in enumerate(rows, 1):
            style = str(w.get("style") or "")
            head = f"### [오답 #{n}] #{w.get('id', '')}"
            if w.get("step"):
                head += f" · {w['step']}"
            if w.get("type"):
                head += f" · {w['type']}"
            out += [head, "", "| 항목 | 내용 |", "|------|------|",
                    f"| 기록일 | {_cell(w.get('date'))} |",
                    f"| 과목 | {_cell(sub)} |",
                    f"| 문항 | {_cell(w.get('question'))} |",
                    f"| 내가 고른 답 | {label(w.get('chosen'), exam, style)} {_cell(w.get('chosenText'))} |",
                    f"| 정답 | {label(w.get('answer'), exam, style)} {_cell(w.get('answerText'))} |"]
            if w.get("coreNote"):
                out.append(f"| 핵심 정리 | {_cell(w['coreNote'])} |")
            if w.get("note"):
                out.append(f"| 틀린 이유(내 메모) | {_cell(w['note'])} |")
            if w.get("device"):
                out.append(f"| 기기 | {_cell(w['device'])} |")
            out.append(f"| 출처 | {_cell(w.get('source'))} |")
            out.append("")
    return "\n".join(out).rstrip() + "\n"


def run(sync_dir: Path = SYNC_DIR, targets: dict[str, Path] | None = None) -> list[Path]:
    targets = targets or TARGETS
    written: list[Path] = []
    for exam, target in targets.items():
        src = sync_dir / f"{exam}.json"
        if not src.exists():
            continue
        try:
            data = json.loads(src.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            print(f"[SKIP] {src.name}: JSON 오류 {e}")
            continue
        text = render(exam, data)
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists() and target.read_text(encoding="utf-8") == text:
            continue
        target.write_text(text, encoding="utf-8")
        written.append(target)
        try:
            shown = target.relative_to(ROOT)
        except ValueError:
            shown = target
        print(f"생성: {shown} ({len(data.get('items') or {})}개)")
    if not written:
        print("변경 없음")
    return written


def selftest() -> int:
    with tempfile.TemporaryDirectory() as td:
        sd = Path(td) / "sync"
        sd.mkdir()
        (sd / "imaging.json").write_text(json.dumps({
            "exam": "imaging", "updated": "2026-09-13T01:02:03Z",
            "items": {"img-2026-0001": {"id": "img-2026-0001", "subject": "순환기", "style": "kmle_style",
                                        "question": "심전도 소견은?", "chosen": 1, "chosenText": "고칼륨혈증",
                                        "answer": 2, "answerText": "QT 연장", "date": "2026-09-13", "note": "QT 안 잼"},
                      "img-2026-0002": {"id": "img-2026-0002", "subject": "피부", "style": "usmle_style",
                                        "question": "Dx?", "chosen": 0, "chosenText": "Nevus",
                                        "answer": 3, "answerText": "Melanoma", "date": "2026-09-12"}},
            "removed": {},
        }, ensure_ascii=False), encoding="utf-8")
        tgt = {"imaging": Path(td) / "out" / "x.md"}
        written = run(sd, tgt)
        assert written == [tgt["imaging"]], written
        md = tgt["imaging"].read_text(encoding="utf-8")
        assert "| 내가 고른 답 | ② 고칼륨혈증 |" in md, md      # 국시형 → ①②
        assert "| 정답 | D Melanoma |" in md, md              # USMLE형 → A~E
        assert "틀린 이유(내 메모) | QT 안 잼" in md
        assert run(sd, tgt) == [], "내용이 같으면 다시 쓰지 않아야 한다"
    print("[ OK ] import_wrong_sync selftest")
    return 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        raise SystemExit(selftest())
    run()
    raise SystemExit(0)
