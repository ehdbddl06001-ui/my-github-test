"""
export_imaging_web.py — content/imaging/**/*.md(오픈데이터 실제 영상 문항)를 웹 퀴즈 번들로 내보낸다.

배경: 의대_시험지_제작(medical_exam_builder_v6)의 아침 루틴이 PTB-XL·ISIC·HPA·TCIA·CTU 같은
오픈데이터 영상으로 국시형·USMLE형 문항 세트를 만든다. 그 세트를 `opendata medkos-export`
가 이 저장소의 `content/imaging/{연도}/imaging-YYYY-NNNN.md` 카드 + `docs/assets/imaging/*.png`
로 옮기고, 이 스크립트가 카드를 `docs/questions_imaging.js` 로 묶어 홈페이지·PWA 의
「🩻 영상」 덱에 띄운다. export_kmle_web.py / export_usmle_web.py 와 대칭이다.

산출물: window.IMAGING_QUESTIONS (docs/questions_imaging.js)
  각 레코드: id, exam="imaging", style(kmle_style|usmle_style), subject, subtopic, type,
             difficulty, created, vignette, question, options[], answer(1-based),
             explanationItems[], explanationText, source,
             figureImg{src, caption, alt}, attribution{dataset, license, license_url, url, asset_id},
             run_id, qid

사용: python pipelines/export_imaging_web.py
      python pipelines/export_imaging_web.py --selftest
"""
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

from frontmatter import load
from export_usmle_web import (
    LETTERS,
    clean_option,
    explanation_items,
    explanation_text,
    split_stem,
)

ROOT = Path(__file__).resolve().parent.parent
IMAGING_DIR = ROOT / "content" / "imaging"
OUT = ROOT / "docs" / "questions_imaging.js"

STYLE_LABEL = {"kmle_style": "국시형", "usmle_style": "USMLE형"}


def figure_record(fig: dict | None, fname: str = "") -> dict | None:
    """frontmatter `figure: {type: image, src, caption}` → 웹용 {src, caption, alt}.
    src 는 docs/ 기준 상대경로다(예: assets/imaging/imaging-2026-0001.png). 파일이 없으면
    문항은 살리되 경고를 남긴다(영상 없는 문항으로 뜬다)."""
    if not isinstance(fig, dict) or fig.get("type") != "image":
        return None
    src = str(fig.get("src", "")).strip()
    if not src:
        return None
    if not (ROOT / "docs" / src).exists():
        print(f"[figure] {fname}: 영상 파일 없음 — docs/{src}")
    return {
        "src": src,
        "caption": str(fig.get("caption", "") or ""),
        "alt": str(fig.get("alt", "") or "임상 영상"),
    }


def build_record(path: Path) -> dict | None:
    d = load(path)
    if d.errors:
        print(f"[SKIP] {path.name}: {d.errors}")
        return None
    m = d.meta
    vignette, question = split_stem(m.get("stem", ""))
    ans = str(m.get("answer", "")).strip().upper()
    style = str(m.get("style", "kmle_style"))
    attribution = m.get("attribution") or {}
    return {
        "id": d.id,
        "exam": "imaging",
        "style": style,
        "styleLabel": STYLE_LABEL.get(style, style),
        "subject": m.get("topic", ""),
        "subject_file": m.get("topic", ""),
        "subtopic": m.get("subtopic", ""),
        "type": m.get("subtopic", ""),
        "modality": m.get("modality", ""),
        "difficulty": m.get("difficulty"),
        "difficultyLabel": m.get("difficulty_label", ""),
        "created": str(m.get("date", "") or ""),
        "vignette": vignette,
        "question": question,
        "options": [clean_option(o) for o in m.get("choices", [])],
        "answer": LETTERS.get(ans, 0),
        "explanationText": explanation_text(d.body),
        "explanationItems": explanation_items(d.body),
        "source": m.get("source", ""),
        "vitals": m.get("vitals", []) or [],
        "labs": m.get("labs", []) or [],
        "appendix": m.get("appendix") or None,
        "figureImg": figure_record(m.get("figure"), path.name),
        "attribution": {
            "dataset": str(attribution.get("dataset", "") or ""),
            "license": str(attribution.get("license", "") or ""),
            "license_url": str(attribution.get("license_url", "") or ""),
            "url": str(attribution.get("url", "") or ""),
            "asset_id": str(attribution.get("asset_id", "") or ""),
            "text": str(attribution.get("text", "") or ""),
        },
        "run_id": str(m.get("run_id", "") or ""),
        "qid": str(m.get("qid", "") or ""),
    }


def load_records(base: Path = IMAGING_DIR) -> list[dict]:
    records = []
    if not base.exists():
        return records
    for p in sorted(base.rglob("*.md")):
        rec = build_record(p)
        if rec:
            records.append(rec)
    records.sort(key=lambda r: (r["created"], r["id"]), reverse=True)
    return records


def write_bundle(records: list[dict], out: Path = OUT) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(records, ensure_ascii=False, indent=1)
    out.write_text(
        "// 자동 생성 파일 — 수정하지 마세요.\n"
        "// 원본: content/imaging/**/*.md  →  `python pipelines/export_imaging_web.py`로 재생성\n"
        "window.IMAGING_QUESTIONS = " + payload + ";\n",
        encoding="utf-8",
    )


def main() -> int:
    records = load_records()
    write_bundle(records)
    by_style: dict[str, int] = {}
    with_img = 0
    for r in records:
        by_style[r["style"]] = by_style.get(r["style"], 0) + 1
        with_img += 1 if r["figureImg"] else 0
    print(f"생성: {OUT.relative_to(ROOT)} ({len(records)}문항, 영상 {with_img})  "
          + ", ".join(f"{k}:{v}" for k, v in sorted(by_style.items())))
    return 0


SAMPLE_CARD = """---
id: imaging-2026-0001
type: imaging
style: kmle_style
topic: "통합(순환기)"
subtopic: "심전도 판독"
modality: ECG
source: "의대_시험지_제작 daily / 2026-09-13"
confidence: high
date: 2026-09-13
tags: [ecg, qt]
stem: "79세 남자가 수술 전 심전도를 찍었다. 심전도는 그림과 같다. 소견은?"
choices: ["A. 좌심실비대", "B. 고칼륨혈증", "C. QT 간격 연장", "D. 완전방실차단", "E. 정상"]
answer: "C"
answer_separated: true
difficulty: 4
difficulty_label: 상
figure:
  type: image
  src: assets/imaging/imaging-2026-0001.png
  caption: "12유도 심전도 (PTB-XL, CC BY 4.0)"
attribution:
  dataset: "PTB-XL v1.0.3"
  license: "CC BY 4.0"
  url: "https://physionet.org/content/ptb-xl/1.0.3/"
  asset_id: PTBXL-00320
run_id: 20260913T053235Z_x
qid: Q0001
---

## 문제
79세 남자가 수술 전 심전도를 찍었다. 심전도는 그림과 같다. 소견은?

- A. 좌심실비대
- B. 고칼륨혈증
- C. QT 간격 연장
- D. 완전방실차단
- E. 정상

## 정답 및 해설
> 정답: C

- **정답 핵심**: QTc ≈ 0.50 s.
- **오답 이유**:
  - ① 전압 기준 미달
  - ② T파가 뾰족하지 않다
- **함정**: 서맥에서 눈대중이 틀어진다.
"""


def selftest() -> int:
    """카드 한 장을 임시 폴더에 두고 파싱 → 레코드 필드가 기대대로 나오는지 확인한다."""
    with tempfile.TemporaryDirectory() as td:
        base = Path(td) / "imaging" / "2026"
        base.mkdir(parents=True)
        (base / "imaging-2026-0001.md").write_text(SAMPLE_CARD, encoding="utf-8")
        recs = load_records(base)
        assert len(recs) == 1, recs
        r = recs[0]
        assert r["answer"] == 3 and r["options"][2] == "QT 간격 연장", r
        assert r["styleLabel"] == "국시형" and r["figureImg"]["src"].endswith("imaging-2026-0001.png"), r
        assert r["attribution"]["asset_id"] == "PTBXL-00320", r
        keys = [it["k"] for it in r["explanationItems"]]
        assert keys == ["정답 핵심", "오답 이유", "함정"], keys
        wrong = [it for it in r["explanationItems"] if it["k"] == "오답 이유"][0]["v"]
        assert "\n" in wrong and wrong.startswith("①"), repr(wrong)   # 보기별 줄 분리
        # style 누락은 frontmatter 검증에서 걸려야 한다
        bad = SAMPLE_CARD.replace("style: kmle_style\n", "")
        (base / "imaging-2026-0002.md").write_text(bad, encoding="utf-8")
        d = load(base / "imaging-2026-0002.md")
        assert any("style" in e for e in d.errors), d.errors
    print("[ OK ] export_imaging_web selftest")
    return 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        raise SystemExit(selftest())
    raise SystemExit(main())
