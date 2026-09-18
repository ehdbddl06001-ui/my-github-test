"""check_sources.py — 정리본이 인용한 출처의 개정·정정 여부를 주기적으로 확인한다(결정론).

2026-09-18 사용자 지시: 출처가 바뀌면 영향받는 단원·표·도식을 표시하고, 확인에 실패하면 내용을 지우지 말고
「업데이트 확인 필요」로 남긴다. 기준·지침의 내용을 코드가 판정하지는 않는다 — **바뀌었다는 신호**만 만든다.

확인 방법(출처마다 할 수 있는 만큼만 — 할 수 없는 것을 했다고 쓰지 않는다)
  pmid       PubMed efetch 의 CommentsCorrections 에서 UpdateIn·ErratumIn·RetractionIn·RepublishedIn·
             ExpressionOfConcernIn 목록을 지문으로 둔다. 새 항목이 생기면 changed.
  watch.pattern  (url) 쪽 글에서 정규식이 잡은 문자열(예: 「updated July 2022」)을 지문으로 둔다. 달라지면 changed.
  그 밖(url 만)  도달 여부만 본다 — 개정은 알 수 없음(method: reachability).
결과: state/source_checks.json  {출처 키: {status, method, fingerprint, baseline, checked_at, changed_at, note, concepts}}
  status ∈ ok · changed · failed. build_books.py 가 changed·failed 인 출처를 인용한 단원에 배너를 단다.
사람이 출처를 다시 대조하고 정리본의 해당 출처 `checked_at` 을 changed_at 이후 날짜로 고치면 새 지문을 기준으로 삼는다.

사용: python pipelines/check_sources.py [--offline]
"""
from __future__ import annotations

import json
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from pathlib import Path

from concepts import load_concepts, safe_url

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "state" / "source_checks.json"
KST = timezone(timedelta(hours=9))
EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&retmode=xml&id="
WATCH_REFS = {"UpdateIn", "ErratumIn", "RetractionIn", "RepublishedIn", "ExpressionOfConcernIn"}
UA = {"User-Agent": "MedKOS-source-check/1 (study notes; contact via GitHub repo)"}


def source_key(s: dict) -> str:
    return str(s.get("doi") or s.get("pmid") or s.get("url") or s.get("id"))


def fetch(url: str, timeout: int = 20) -> str:
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", "replace")


def pubmed_fingerprint(pmid: str, getter=fetch) -> list[str]:
    root = ET.fromstring(getter(EUTILS + pmid))
    out = []
    for cc in root.iter("CommentsCorrections"):
        rt = cc.get("RefType")
        if rt in WATCH_REFS:
            ref = (cc.findtext("RefSource") or "").strip()
            pm = (cc.findtext("PMID") or "").strip()
            out.append(f"{rt}:{pm or ref}")
    return sorted(out)


def check_one(s: dict, getter=fetch) -> tuple[str, str]:
    """(method, fingerprint). 실패하면 예외."""
    if s.get("pmid"):
        return "pubmed", json.dumps(pubmed_fingerprint(str(s["pmid"]), getter), ensure_ascii=False)
    url = safe_url(s.get("url"))
    if not url:
        raise ValueError("확인할 https url·pmid 가 없다")
    text = getter(url)
    pat = (s.get("watch") or {}).get("pattern")
    if pat:
        m = re.search(pat, text, re.IGNORECASE)
        return "pattern", (re.sub(r"\s+", " ", m.group(1 if m.groups() else 0)).strip() if m else "(패턴 없음)")
    return "reachability", "reachable"


def run(offline: bool = False, getter=fetch, out: Path = OUT, today: str | None = None) -> dict:
    today = today or datetime.now(KST).strftime("%Y-%m-%d")
    prev = json.loads(out.read_text(encoding="utf-8")) if out.exists() else {}
    concepts, _ = load_concepts()
    srcs: dict[str, dict] = {}
    for cid, c in concepts.items():
        for s in c.get("sources") or []:
            k = source_key(s)
            e = srcs.setdefault(k, {"source": s, "concepts": [], "checked_at": str(s.get("checked_at", ""))})
            e["concepts"].append(cid)
            e["checked_at"] = min(e["checked_at"], str(s.get("checked_at", ""))) or e["checked_at"]
    res: dict = {}
    for k, e in sorted(srcs.items()):
        p = dict(prev.get(k) or {})
        rec = {**p, "concepts": sorted(set(e["concepts"])), "title": str(e["source"].get("title", ""))}
        if offline:
            res[k] = rec or {"status": "unchecked"}
            continue
        try:
            method, fp = check_one(e["source"], getter)
            rec.update(method=method, fingerprint=fp, checked_at=today)
            base = p.get("baseline")
            if base is None:
                rec.update(baseline=fp, status="ok", note="기준 지문 기록" + (" — 개정 여부는 알 수 없음(도달만 확인)" if method == "reachability" else ""))
                if method == "pubmed" and "RetractionIn" in fp:
                    rec.update(status="changed", changed_at=today, note="철회(Retraction) 기록이 있다")
            elif fp != base:
                # 사람이 다시 대조했으면(정리본 checked_at ≥ changed_at) 새 지문을 기준으로 삼는다
                if p.get("changed_at") and e["checked_at"] >= p["changed_at"]:
                    rec.update(baseline=fp, status="ok", note=f"{e['checked_at']} 사람 재대조 후 새 기준")
                else:
                    rec.update(status="changed", changed_at=p.get("changed_at") or today,
                               note=f"지문 변경: {base[:80]} → {fp[:80]}")
            else:
                rec.update(status="ok", note=p.get("note", ""))
        except Exception as ex:                       # 내용은 그대로 두고 표시만
            rec.update(status="failed", checked_at=today, note=f"확인 실패({type(ex).__name__}: {str(ex)[:120]}) — 업데이트 확인 필요")
        res[k] = rec
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
    return res


def main(argv: list[str]) -> int:
    res = run(offline="--offline" in argv)
    for k, r in res.items():
        print(f"  {r.get('status', '?'):8} {r.get('method', ''):12} {k}  {r.get('note', '')}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
