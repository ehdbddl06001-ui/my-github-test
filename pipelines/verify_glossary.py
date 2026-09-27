"""content/glossary/drugs_ko_en.yaml 의 영어 이름을 NLM 에서 확인해 verified.json 을 다시 만든다(2026-09-27).

약 = RxNorm 정확 일치(RxNav `rxcui.json?search=0`), 약군 = MeSH 표목 정확 일치(`check` 값).
확인되지 않은 항목은 verified.json 에 넣지 않는다 — 학습서는 확인된 영어만 쓴다(영어 이름을 지어내지 않는다).

  python pipelines/verify_glossary.py
"""
from __future__ import annotations

import json
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

import yaml

DIR = Path(__file__).resolve().parent.parent / "content" / "glossary"
UA = {"User-Agent": "medkos-glossary/1.0", "Accept": "application/json"}


def get(url: str):
    err: Exception | None = None
    for _ in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=20) as r:
                return json.loads(r.read().decode())
        except Exception as e:  # noqa: BLE001 — 잠깐의 연결 끊김은 다시 시도
            err = e
            time.sleep(1)
    raise err  # type: ignore[misc]


def main() -> int:
    g = yaml.safe_load((DIR / "drugs_ko_en.yaml").read_text(encoding="utf-8"))
    out: dict = {"drugs": {}, "classes": {}, "failed": []}
    rx: dict[str, list] = {}
    for ko, en in (g.get("drugs") or {}).items():
        if en not in rx:
            j = get("https://rxnav.nlm.nih.gov/REST/rxcui.json?" + urllib.parse.urlencode({"name": en, "search": 0}))
            rx[en] = (j.get("idGroup") or {}).get("rxnormId") or []
        if rx[en]:
            out["drugs"][ko] = {"en": en, "rxcui": rx[en][0]}
        else:
            out["failed"].append(f"drug {ko} → {en}")
    for ko, v in (g.get("classes") or {}).items():
        j = get("https://id.nlm.nih.gov/mesh/lookup/descriptor?"
                + urllib.parse.urlencode({"label": v["check"], "match": "exact", "limit": 1}))
        if j:
            out["classes"][ko] = {"en": v["en"], "mesh": j[0]["resource"].rsplit("/", 1)[-1], "mesh_label": j[0]["label"]}
        else:
            out["failed"].append(f"class {ko} → {v['check']}")
    (DIR / "verified.json").write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")
    print(f"약 {len(out['drugs'])} · 약군 {len(out['classes'])} 확인, 실패 {out['failed']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
