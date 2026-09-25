"""check_sources.py — 정리본이 인용한 출처의 개정·정정 여부를 주기적으로 확인한다(결정론).

2026-09-18 사용자 지시: 출처가 바뀌면 영향받는 단원·표·도식을 표시하고, 확인에 실패하면 내용을 지우지 말고
「업데이트 확인 필요」로 남긴다. 기준·지침의 내용을 코드가 판정하지는 않는다 — **바뀌었다는 신호**만 만든다.

확인 방법(출처마다 할 수 있는 만큼만 — 할 수 없는 것을 했다고 쓰지 않는다)
  pmid       PubMed efetch 의 CommentsCorrections 에서 UpdateIn·ErratumIn·RetractionIn·RepublishedIn·
             ExpressionOfConcernIn 목록을 지문으로 둔다. 새 항목이 생기면 changed.
  doi 만     PubMed esearch 로 그 DOI 의 PMID 를 한 번 찾아(state 에 기억) pmid 와 같이 본다. PubMed 에 없으면
             doi.org 핸들 API 로 DOI 가 살아 있는지만 본다(method: doi — 개정은 알 수 없음). 2026-09-25 추가 —
             루틴이 쓴 정리본 16개 출처가 DOI 만 있어 전부 「확인 실패」가 되어 책마다 경고가 찍힐 뻔했다.
  watch.pattern  (url) 쪽 글에서 정규식이 잡은 문자열(예: 「updated July 2022」)을 지문으로 둔다. 달라지면 changed.
  그 밖(url 만)  도달 여부만 본다 — 개정은 알 수 없음(method: reachability).
결과: state/source_checks.json  {출처 키: {status, method, fingerprint, baseline, checked_at, changed_at, note, concepts}}
  status ∈ ok · changed · failed · unchecked(일시 오류로 못 봄 — 배너를 찍지 않는다). build_books.py 가 changed·failed 인 출처를 인용한 단원에 배너를 단다.
사람이 출처를 다시 대조하고 정리본의 해당 출처 `checked_at` 을 changed_at 이후 날짜로 고치면 새 지문을 기준으로 삼는다.

사용: python pipelines/check_sources.py [--offline]
"""
from __future__ import annotations

import json
import re
import sys
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from pathlib import Path

from concepts import load_concepts, safe_url

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "state" / "source_checks.json"
KST = timezone(timedelta(hours=9))
EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&retmode=xml&id="
ESEARCH = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&retmode=xml&term="
DOI_HANDLE = "https://doi.org/api/handles/"
WATCH_REFS = {"UpdateIn", "ErratumIn", "RetractionIn", "RepublishedIn", "ExpressionOfConcernIn"}
UA = {"User-Agent": "MedKOS-source-check/1 (study notes; contact via GitHub repo)"}


def source_key(s: dict) -> str:
    return str(s.get("doi") or s.get("pmid") or s.get("url") or s.get("id"))


_LAST_NCBI = [0.0]
NCBI_GAP = 0.4          # NCBI E-utilities 는 키 없이 초당 3건 — 2026-09-25 첫 전수 확인에서 20건이 429 로 「확인 못 함」


def fetch(url: str, timeout: int = 20) -> str:
    if "eutils.ncbi.nlm.nih.gov" in url:
        import time
        wait = _LAST_NCBI[0] + NCBI_GAP - time.monotonic()
        if wait > 0:
            time.sleep(wait)
        _LAST_NCBI[0] = time.monotonic()
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


def pmid_for_doi(doi: str, getter=fetch) -> str:
    """DOI → PMID(PubMed 에 딱 하나 있을 때만). 없으면 빈 글."""
    root = ET.fromstring(getter(ESEARCH + urllib.parse.quote(f'"{doi}"[doi]')))
    ids = [(i.text or "").strip() for i in root.iter("Id")]
    return ids[0] if len(ids) == 1 and ids[0].isdigit() else ""


def doi_alive(doi: str, getter=fetch) -> bool:
    """doi.org 핸들 API — 출판사 사이트(봇 차단이 잦다)를 거치지 않고 DOI 등록만 본다."""
    body = json.loads(getter(DOI_HANDLE + urllib.parse.quote(doi, safe="/")))
    return body.get("responseCode") == 1


def check_one(s: dict, getter=fetch, doi_pmid: str | None = None) -> tuple[str, str]:
    """(method, fingerprint). 실패하면 예외. doi_pmid = DOI 에서 이미 찾아 둔 PMID(없으면 None → 찾아 본다)."""
    if s.get("pmid"):
        return "pubmed", json.dumps(pubmed_fingerprint(str(s["pmid"]), getter), ensure_ascii=False)
    if s.get("doi"):                                   # url 이 같이 있어도 DOI 로 본다 — 출판사 사이트는 봇을 403 으로 막는다
        doi = str(s["doi"]).strip()
        pm = doi_pmid if doi_pmid is not None else pmid_for_doi(doi, getter)
        if pm:
            return "pubmed", json.dumps(pubmed_fingerprint(pm, getter), ensure_ascii=False)
        if not doi_alive(doi, getter):
            raise ValueError(f"DOI {doi} 가 doi.org 에 없다")
        return "doi", "registered"
    url = safe_url(s.get("url"))
    if not url and s.get("kind") == "textbook":
        return "manual", "교과서 — 판이 바뀌면 사람이 정리본의 citation·checked_at 을 고친다(자동 확인 대상 아님)"
    if not url:
        raise ValueError("확인할 https url·pmid 가 없다")
    text = getter(url)
    pat = (s.get("watch") or {}).get("pattern")
    if pat:
        m = re.search(pat, text, re.IGNORECASE)
        return "pattern", (re.sub(r"\s+", " ", m.group(1 if m.groups() else 0)).strip() if m else "(패턴 없음)")
    return "reachability", "reachable"


# 403 = 출판사·기관 사이트의 봇 차단, 302 = 쿠키 리디렉션 루프(urllib 가 멈춘다) — 출처가 바뀌었다는 신호가 아니다
# (2026-09-25 첫 전수 확인에서 37개가 403 으로 「업데이트 확인 필요」가 될 뻔했다). 사라진 쪽은 404·410 으로 남는다.
def baseline_shape_ok(method: str, base: str) -> bool:
    """기준 지문이 지금 확인 방법으로 만든 것인가. 방법이 바뀌면(예: 출판사 url 도달 → DOI 로 찾은 PubMed) 옛 기준과 비교하면
    내용이 그대로여도 「지문 변경」이 된다(2026-09-25 — reachable → [] 3건이 개정으로 찍혔다)."""
    if method == "pubmed":
        return base.startswith("[")
    if method == "reachability":
        return base == "reachable"
    if method == "doi":
        return base == "registered"
    return True


TRANSIENT_CODES = {302, 403, 408, 425, 429, 500, 502, 503, 504}


def transient(ex: Exception) -> bool:
    """출처가 바뀐 게 아니라 이번 요청만 실패한 경우 — 요청 제한·일시 장애·연결 문제."""
    import socket
    from urllib.error import HTTPError, URLError
    if isinstance(ex, HTTPError):
        return ex.code in TRANSIENT_CODES
    return isinstance(ex, (URLError, TimeoutError, socket.timeout, ConnectionError))


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
            src = e["source"]
            doi_pmid = p.get("doi_pmid") if (src.get("doi") and not src.get("pmid") and "doi_pmid" in p) else None
            if src.get("doi") and not src.get("pmid") and doi_pmid is None:
                doi_pmid = pmid_for_doi(str(src["doi"]).strip(), getter)
                rec["doi_pmid"] = doi_pmid                    # 한 번 찾으면 기억(빈 글 = PubMed 에 없음)
            method, fp = check_one(src, getter, doi_pmid)
            rec.update(method=method, fingerprint=fp, checked_at=today)
            base = p.get("baseline")
            if base is not None and not baseline_shape_ok(method, str(base)):
                rec.update(baseline=fp, status="ok", note=f"확인 방법이 바뀌어({p.get('baseline_method') or '이전 방법'} → {method}) 새 기준 지문 기록",
                           baseline_method=method)
                rec.pop("changed_at", None)
            elif base is None:
                rec.update(baseline=fp, status="ok", note="기준 지문 기록" + (" — 개정 여부는 알 수 없음(도달만 확인)" if method in ("reachability", "doi") else ""))
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
                # 지문이 그대로다 — 옛 메모(지난번 일시 오류 문구 등)를 물려받지 않는다
                rec.update(status="ok", note="기준 지문과 같음")
        except Exception as ex:                       # 내용은 그대로 두고 표시만
            if transient(ex):
                # 우리 쪽 사정(PubMed 요청 제한·일시 장애)이다. 출처가 개정됐다는 뜻이 아니므로
                # 학습서에 「출처 개정 확인 필요」를 찍지 않는다(2026-09-21 — 429 가 책에 경고로 찍혔다).
                keep = p.get("status") if p.get("status") in ("ok", "changed") else "unchecked"
                before = str(p.get("note", "") or "")
                if before.startswith("확인 실패") or "일시 오류" in before:
                    before = ""                        # 옛 실패 문구를 물려받지 않는다
                rec.update(status=keep, last_error=f"{type(ex).__name__}: {str(ex)[:80]}",
                           note=(before + " · " if before else "") + f"{today} 확인 못 함(일시 오류, 다음 실행에 다시 본다)")
            else:
                rec.update(status="failed", checked_at=today,
                           note=f"확인 실패({type(ex).__name__}: {str(ex)[:120]}) — 업데이트 확인 필요")
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
