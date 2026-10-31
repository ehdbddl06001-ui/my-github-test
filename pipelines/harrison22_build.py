"""harrison22_build.py — 해리슨 22판 장별 DB(사용자 드라이브)의 목차·문서 ID 를 `content/outline/harrison22.json` 으로 굳힌다.

2026-10-31 사용자 지시: 해리슨 대조를 22판 DB 로 본다. 사용자가 드라이브 `내 드라이브/교과서/Harrison_22e_장별/` 에
장마다 Google 문서 `H22_<장 3자리>`(쪽마다 `===== [H22 p.<인쇄쪽>] =====`)와 `Harrison_22e_목차.csv` 를 만들어 두었다.

기본틀 슬롯 id(`h<21판 장>`)와 순서는 **바꾸지 않는다** — 정리본 `outline:` 과 학습서 순서가 그것을 가리킨다.
대신 21판 장 → 22판 장 대응표(`from21`)를 둔다. 제목이 같으면 자동으로, 바뀐 장은 아래 `OVERRIDES` 에 손으로 적었다
(이웃 장 사이에서 제목으로 확인한 것). 22판에 대응 장이 없으면 빈 목록 — `outline.py --harrison` 이 21판 문서로 돌아간다.

입력(드라이브 커넥터로 받은 것):
  --toc  Harrison_22e_목차.csv (chapter,title,part,section,print_start,print_end,…)
  --ids  {"H22_044": "<문서 ID>", …}  (폴더 안 Google 문서 목록)
사용:
  python pipelines/harrison22_build.py --toc 목차.csv --ids ids.json
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOC21 = ROOT / "content" / "outline" / "harrison_toc.json"
OUT = ROOT / "content" / "outline" / "harrison22.json"
FOLDER = "내 드라이브/교과서/Harrison_22e_장별"
FOLDER_ID = "1pdmFCyAAGPVel6V_YkkTuLWP1PvMGbVI"

# 21판 장 → 22판 장(제목이 바뀌었거나 나뉜/없어진 장). 이웃 장 사이에서 제목으로 확인했다(2026-10-31).
OVERRIDES: dict[int, list[int]] = {
    7: [],              # Global Diversity of Health System Financing and Delivery — 22판에 없음
    17: [18, 19],       # Back and Neck Pain → Low Back Pain · Neck Pain
    81: [86],           # Lower Gastrointestinal Cancers → Colorectal Cancer
    97: [102],          # Iron Deficiency and Other Hypoproliferative Anemias
    135: [140],         # Urinary Tract Infections
    176: [181],         # Whipple Disease
    185: [190],         # Relapsing Fever
    196: [201],         # Poxvirus Infections
    199: [204, 205],    # Common Viral Respiratory Infections · SARS-CoV-2 and COVID-19
    210: [216],         # Filovirids (Ebola·Marburg)
    219: [225, 226],    # Superficial · Uncommon Disseminated Fungal Infections
    246: [253],         # Approach to Supraventricular Arrhythmias
    247: [254],         # Physiologic and Nonphysiologic Sinus Rhythm
    259: [266, 267, 268, 269, 270],  # Cardiomyopathy and Myocarditis → 다섯 장으로 나뉨
    313: [325],         # Kidney Transplantation
    317: [329],         # Thrombotic Renovascular Disorders
    343: [354],         # MASLD and Steatohepatitis
    361: [373],         # Sjögren's Disease
    400: [412],         # LGBTQIA+ Health
    417: [],            # Disorders of Purine and Pyrimidine Metabolism — 22판에 없음
    428: [439],         # Intracerebral Hemorrhage
    455: [466],         # Cannabis and Cannabis Use Disorder
    467: [480],         # The Integration of Inherited Genetics into Clinical Practice
    471: [484],         # The Human Microbiome in Health and Disease
    473: [486],         # Emerging and Re-Emerging Infectious Diseases
    480: [492],         # Medical Evaluation of the Patient Undergoing Noncardiac Surgery
    481: [494],         # Behavioral Economics
    484: [],            # Applications of Stem Cell Biology — 22판에 없음
    486: [499],         # Network Medicine and Multiomic Approaches
}


def norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", s.lower().replace("’", "'")).strip()


def build(toc_rows: list[dict], ids: dict[str, str], toc21: list[dict]) -> tuple[dict, list[str]]:
    errs: list[str] = []
    chapters: dict[str, dict] = {}
    for r in toc_rows:
        r = {k.replace("\\_", "_").strip(): (v or "").replace("\\_", "_").strip() for k, v in r.items() if k}
        n = int(r["chapter"])
        doc = ids.get(f"H22_{n:03d}")
        if not doc:
            errs.append(f"22판 {n}장 문서 ID 가 없다")
        chapters[str(n)] = {"title": r["title"], "part": r.get("part", ""),
                            "section": "" if r.get("section") in ("", "-") else r["section"],
                            "page": int(r["print_start"]), "page_end": int(r["print_end"]), "doc": doc or ""}
    by_title = {norm(c["title"]): int(n) for n, c in chapters.items()}
    from21: dict[str, list[int]] = {}
    for c in toc21:
        n = c["n"]
        if n in OVERRIDES:
            from21[str(n)] = OVERRIDES[n]
        elif norm(c["title"]) in by_title:
            from21[str(n)] = [by_title[norm(c["title"])]]
        else:
            errs.append(f"21판 {n}장 {c['title']!r} 의 22판 장을 못 찾았다 — OVERRIDES 에 적는다")
    for n, js in from21.items():
        for j in js:
            if str(j) not in chapters:
                errs.append(f"21판 {n}장 → 22판 {j}장이 목차에 없다")
    data = {"edition": 22, "folder": FOLDER, "folder_id": FOLDER_ID,
            "note": "해리슨 22판 장별 텍스트(사용자 드라이브의 Google 문서 H22_<장>, 비공개). 루틴은 Google Drive 커넥터 "
                    "read_file_content 로 그 장만 읽는다. `===== [H22 p.N] =====` 뒤가 인쇄쪽 N 의 본문이다. "
                    "from21 = 기본틀 슬롯(21판 장 번호) → 22판 장(빈 목록 = 22판에 없음).",
            "chapters": chapters, "from21": from21}
    return data, errs


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--toc", required=True)
    ap.add_argument("--ids", required=True)
    a = ap.parse_args(argv)
    rows = list(csv.DictReader(open(a.toc, encoding="utf-8-sig")))
    ids = json.loads(Path(a.ids).read_text(encoding="utf-8"))
    toc21 = json.loads(TOC21.read_text(encoding="utf-8"))["chapters"]
    data, errs = build(rows, ids, toc21)
    for e in errs:
        print("  ✗", e)
    if errs:
        return 1
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    gone = [n for n, js in data["from21"].items() if not js]
    print(f"{OUT.relative_to(ROOT)}: 22판 {len(data['chapters'])}장 · 21판 대응 {len(data['from21'])}장(22판에 없음 {gone})")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
