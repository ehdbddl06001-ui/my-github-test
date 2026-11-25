"""kr_guidelines.py — 국내 가이드라인 레지스트리(kr_guidelines.json)와 해리슨 22판 대조표 검증·배치 도구.

사용:
  python pipelines/kr_guidelines.py --check                   # 레지스트리 + 대조표 YAML 전체 검증
  python pipelines/kr_guidelines.py --summary                 # Tier·과별 현황 요약
  python pipelines/kr_guidelines.py --batch 내분비내과         # 해당 과의 Drive 체크리스트 + H22 문서 ID + Opus 5.5 프롬프트
  python pipelines/kr_guidelines.py --batch tier1             # Tier 1 전체 Drive 체크리스트
  python pipelines/kr_guidelines.py --scan-existing 내분비내과 # 기존 KMLE 문항·정리본 중 관련 후보 스캔
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "pipelines"))
import outline as ol  # noqa: E402

REGISTRY = ROOT / "content" / "outline" / "kr_guidelines.json"
DIFF_DIR = ROOT / "content" / "outline" / "kr_vs_harrison"
H22_PATH = ROOT / "content" / "outline" / "harrison22.json"
KMLE_DIR = ROOT / "content" / "kmle"
CONCEPT_DIR = ROOT / "content" / "concepts"

VALID_STATUS = {"pending_pdf", "ready", "compared"}
VALID_ACCESS = {"public_pdf", "society_check"}
VALID_DIFF_TYPES = {"threshold", "algorithm", "first_line", "screening", "terminology", "legal", "same"}
VALID_VERIFIED = {"text", "pending"}
PAGE_RE = re.compile(r"(?:p\.?\s*\d+|\d+\s*쪽)", re.I)


def load_registry() -> dict:
    return json.loads(REGISTRY.read_text(encoding="utf-8"))


def diff_items() -> list[dict]:
    """국내 vs 해리슨 대조 항목 전부(content/outline/kr_vs_harrison/*.yaml — `_` 로 시작하는 틀 제외)."""
    out: list[dict] = []
    for f in sorted(DIFF_DIR.glob("*.yaml")):
        if f.name.startswith("_"):
            continue
        doc = yaml.safe_load(f.read_text(encoding="utf-8")) or {}
        for it in doc.get("items") or []:
            out.append(dict(it, subject_slug=doc.get("subject_slug", f.stem)))
    return out


def track_slots(reg: dict) -> dict[str, set[str]]:
    """트랙 id → 그 지침이 닿는 기본틀 슬롯(레지스트리 slots)."""
    return {g["id"]: set(g.get("slots") or []) for g in reg.get("guidelines", [])}


def items_for_slot(slot: str, items: list[dict], tslots: dict[str, set[str]], include_same: bool = False) -> list[dict]:
    """정리본 기본틀 슬롯에 닿는 대조 항목 — 항목 slot 이 같거나, 항목 지침 트랙의 slots 에 그 슬롯이 있다.

    `same`(국내 = 해리슨)은 정리본에 차이로 넣을 것이 없어 기본으로 뺀다.
    """
    if not slot:
        return []
    return [it for it in items
            if (include_same or it.get("diff_type") != "same")
            and (it.get("slot") == slot or slot in tslots.get(str(it.get("kr_guideline_id", "")), set()))]


def load_h22() -> dict:
    return json.loads(H22_PATH.read_text(encoding="utf-8"))


def load_slots() -> dict[str, ol.Slot]:
    books, _ = ol.load()
    return ol.index(books)


def check_all() -> list[str]:
    errs: list[str] = []
    if not REGISTRY.is_file():
        return [f"레지스트리가 없다: {REGISTRY.relative_to(ROOT)}"]

    reg = load_registry()
    h22 = load_h22()
    h22_chs = h22.get("chapters", {})
    slots = load_slots()

    seen_ids: set[str] = set()
    guidelines = reg.get("guidelines") or []
    for idx, g in enumerate(guidelines, 1):
        gid = str(g.get("id", "")).strip()
        if not gid:
            errs.append(f"guidelines[{idx}]: id 가 비어 있다")
            continue
        if gid in seen_ids:
            errs.append(f"{gid}: 중복된 id")
        seen_ids.add(gid)

        if g.get("tier") not in (1, 2, 3):
            errs.append(f"{gid}: tier 는 1/2/3 이어야 한다 ({g.get('tier')})")
        if g.get("status") not in VALID_STATUS:
            errs.append(f"{gid}: status 오류 ({g.get('status')})")
        if g.get("access") not in VALID_ACCESS:
            errs.append(f"{gid}: access 오류 ({g.get('access')})")

        for s in g.get("slots") or []:
            if s not in slots:
                errs.append(f"{gid}: 슬롯 '{s}' 가 subjects.yaml 에 없다")
        for ch in g.get("h22_chapters") or []:
            if str(ch) not in h22_chs:
                errs.append(f"{gid}: 해리슨 22판 {ch}장이 harrison22.json 에 없다")
        if g.get("status") in ("ready", "compared") and not str(g.get("drive_doc_id", "")).strip():
            errs.append(f"{gid}: status={g.get('status')} 인데 drive_doc_id 가 비어 있다")

    if DIFF_DIR.is_dir():
        seen_diff_ids: set[str] = set()
        for yf in sorted(DIFF_DIR.glob("*.yaml")):
            if yf.name.startswith("_"):
                continue
            data = yaml.safe_load(yf.read_text(encoding="utf-8")) or {}
            for item in data.get("items") or []:
                did = str(item.get("id", "")).strip()
                loc = f"{yf.name}:{did or '?'}"
                if not did:
                    errs.append(f"{loc}: id 누락")
                elif did in seen_diff_ids:
                    errs.append(f"{loc}: 중복된 diff id")
                else:
                    seen_diff_ids.add(did)

                slot = item.get("slot")
                if slot not in slots:
                    errs.append(f"{loc}: 슬롯 '{slot}' 가 subjects.yaml 에 없다")
                kr_id = item.get("kr_guideline_id")
                if kr_id not in seen_ids:
                    errs.append(f"{loc}: kr_guideline_id '{kr_id}' 가 kr_guidelines.json 에 없다")
                ch = item.get("h22_chapter")
                if ch is not None and str(ch) not in h22_chs:
                    errs.append(f"{loc}: h22_chapter '{ch}' 가 harrison22.json 에 없다")
                if item.get("diff_type") not in VALID_DIFF_TYPES:
                    errs.append(f"{loc}: diff_type 오류 ({item.get('diff_type')})")
                ver = item.get("verified")
                if ver not in VALID_VERIFIED:
                    errs.append(f"{loc}: verified 오류 ({ver})")
                if ver == "text":
                    kr_cite = str(item.get("kr_cite", "")).strip()
                    if not kr_cite:
                        errs.append(f"{loc}: verified=text 인데 kr_cite 가 비어 있다")
                    if ch is not None:
                        h22_cite = str(item.get("h22_cite", "")).strip()
                        if not h22_cite or not PAGE_RE.search(h22_cite):
                            errs.append(f"{loc}: verified=text 인데 h22_cite 에 쪽 번호가 없다")
    # 정리본이 반영했다고 적은 대조 항목(kr_diffs · kr_diffs_skip)은 실제로 있어야 한다 — 큐 [krdiff] 가 이 표시로 끝난 것을 가린다
    if CONCEPT_DIR.is_dir():
        for cf in sorted(CONCEPT_DIR.rglob("*.md")):
            fm, _ = _read_fm(cf)
            for key in ("kr_diffs", "kr_diffs_skip"):
                for did in fm.get(key) or []:
                    if str(did) not in seen_diff_ids:
                        errs.append(f"{cf.relative_to(ROOT).as_posix()}: {key} 의 '{did}' 가 kr_vs_harrison 에 없다")
    return errs


def filter_guidelines(guidelines: list[dict], target: str) -> list[dict]:
    t = target.strip().lower()
    if t in ("all", "전체"):
        return guidelines
    m = re.fullmatch(r"(?:tier)?([123])", t)
    if m:
        tier = int(m.group(1))
        return [g for g in guidelines if g.get("tier") == tier]
    return [
        g for g in guidelines
        if t in (g.get("subject", "").lower(), g.get("subject_slug", "").lower(), g.get("id", "").lower())
        or t in g.get("subject", "").lower()
    ]


def cmd_summary(reg: dict) -> int:
    gs = reg.get("guidelines") or []
    print(f"총 {len(gs)}개 국내 가이드라인 트랙 (저장 폴더: {reg.get('folder')})\n")
    print("| Tier | 트랙 수 | 공개PDF | 학회확인 | Drive등록(ready) | 대조완료(compared) |")
    print("|---|---|---|---|---|---|")
    for tier in (1, 2, 3):
        sub = [g for g in gs if g.get("tier") == tier]
        pub = sum(1 for g in sub if g.get("access") == "public_pdf")
        soc = sum(1 for g in sub if g.get("access") == "society_check")
        rdy = sum(1 for g in sub if g.get("status") == "ready")
        cmp = sum(1 for g in sub if g.get("status") == "compared")
        print(f"| Tier {tier} | {len(sub)} | {pub} | {soc} | {rdy} | {cmp} |")

    print("\n| 과목 | 슬러그 | 트랙 수 | Tier 1 | 공개PDF | 대조완료 |")
    print("|---|---|---|---|---|---|")
    by_sub: dict[str, list[dict]] = {}
    for g in gs:
        by_sub.setdefault(g["subject"], []).append(g)
    for sub, items in by_sub.items():
        slug = items[0]["subject_slug"]
        t1 = sum(1 for g in items if g.get("tier") == 1)
        pub = sum(1 for g in items if g.get("access") == "public_pdf")
        cmp = sum(1 for g in items if g.get("status") == "compared")
        print(f"| {sub} | `{slug}` | {len(items)} | {t1} | {pub} | {cmp} |")
    return 0


def cmd_batch(reg: dict, h22: dict, target: str) -> int:
    items = filter_guidelines(reg.get("guidelines") or [], target)
    if not items:
        print(f"대상을 찾지 못했다: {target}")
        return 1

    chs = h22.get("chapters", {})
    print(f"=== 배치 대상: {target} ({len(items)}개 트랙) ===\n")
    print("[1] Google Drive PDF 준비 체크리스트")
    for g in items:
        acc = "공개PDF" if g["access"] == "public_pdf" else "학회확인"
        doc_tag = g["drive_doc_id"] or "미등록"
        print(f"  - [{g['status']:11}] Tier {g['tier']} | {g['topic_ko']} ({g['year']}) [{acc}]")
        print(f"      출처: {g['source_portal']}" + (f" · DOI {g['doi']}" if g.get("doi") else ""))
        print(f"      Drive: {reg['folder']}/{g['drive_path']} (doc_id: {doc_tag})")

    print("\n[2] 해리슨 22판 대응 Drive 문서 ID (Harrison_22e_장별)")
    seen_ch: set[int] = set()
    for g in items:
        for ch in g.get("h22_chapters") or []:
            if ch in seen_ch:
                continue
            seen_ch.add(ch)
            info = chs.get(str(ch), {})
            print(f"  - H22_{ch:03d} ({info.get('title', '')}) | p.{info.get('page')}~{info.get('page_end')} | doc_id: {info.get('doc', '')}")

    print("\n[3] Opus 5.5 세션용 배치 프롬프트")
    print("-" * 72)
    subjects = sorted({g["subject"] for g in items})
    slugs = sorted({g["subject_slug"] for g in items})
    print(f"# 작업: MedKOS 국내 가이드라인 vs 해리슨 22판 원문 대조 — {' · '.join(subjects)}")
    print("\n## 필수 규칙")
    print("1. CLAUDE.md와 schemas/frontmatter.md를 먼저 읽는다.")
    print("2. 원문 확인 없는 기억 기반 서술 금지. 아래 H22 문서 ID와 Drive 국내 가이드라인 PDF를 모두 직접 읽고 인쇄쪽(p.N)을 기록한다.")
    print("3. 대조 결과는 content/outline/kr_vs_harrison/<subject_slug>.yaml 에 저장하고 `python pipelines/kr_guidelines.py --check` 로 오류 0을 확인한다.")
    print("\n## 대조 대상")
    for g in items:
        ch_str = ", ".join(f"H22_{c:03d}(doc:{chs[str(c)]['doc']})" for c in g.get("h22_chapters") or [] if str(c) in chs) or "비해리슨"
        print(f"- {g['id']} ({g['topic_ko']}): slots={g['slots']} | {ch_str} | KR={g['drive_path']}")
        for cp in g.get("check_points") or []:
            print(f"    · 체크: {cp}")
    print(f"\n## 출력 파일: {', '.join(f'content/outline/kr_vs_harrison/{s}.yaml' for s in slugs)}")
    print("-" * 72)
    return 0


def _read_fm(path: Path) -> tuple[dict, str]:
    txt = path.read_text(encoding="utf-8", errors="ignore")
    if not txt.startswith("---"):
        return {}, txt
    parts = txt.split("---", 2)
    if len(parts) < 3:
        return {}, txt
    try:
        meta = yaml.safe_load(parts[1]) or {}
    except Exception:
        meta = {}
    return meta, parts[2]


def cmd_scan(reg: dict, target: str) -> int:
    items = filter_guidelines(reg.get("guidelines") or [], target)
    if not items:
        print(f"대상을 찾지 못했다: {target}")
        return 1

    # Load all concepts once
    concepts: list[tuple[Path, dict]] = []
    if CONCEPT_DIR.is_dir():
        for p in sorted(CONCEPT_DIR.rglob("*.md")):
            m, _ = _read_fm(p)
            concepts.append((p, m))

    # Load all KMLE questions once
    kmles: list[tuple[Path, dict, str]] = []
    if KMLE_DIR.is_dir():
        for p in sorted(KMLE_DIR.rglob("*.md")):
            m, body = _read_fm(p)
            hay = " ".join([
                str(m.get("topic", "")),
                str(m.get("subtopic", "")),
                " ".join(str(t) for t in (m.get("tags") or [])),
                str(m.get("stem", "")),
                str(m.get("explanation", "")),
            ]).lower()
            kmles.append((p, m, hay))

    print(f"=== 기존 MedKOS 카드 대조 후보 스캔: {target} ({len(items)}개 트랙) ===\n")
    print("| 트랙 | 슬롯 | 기존 정리본(슬롯 일치) | 기존 KMLE 문항(키워드 후보) |")
    print("|---|---|---|---|")
    total_c = 0
    total_q = 0
    details: list[tuple[str, list[str], list[str]]] = []
    for g in items:
        slot_set = set(g.get("slots") or [])
        kws = [k.lower() for k in (g.get("keywords") or []) if len(k) >= 2]
        c_hits = [str(m.get("id") or p.stem) for p, m in concepts if str(m.get("outline", "")) in slot_set]
        q_hits = [
            str(m.get("id") or p.stem)
            for p, m, hay in kmles
            if any(kw in hay for kw in kws)
        ]
        total_c += len(c_hits)
        total_q += len(q_hits)
        details.append((g["topic_ko"], c_hits, q_hits))
        print(f"| {g['topic_ko']} | `{', '.join(g['slots'])}` | {len(c_hits)} | {len(q_hits)} |")

    print(f"\n합계(트랙 간 중복 포함): 정리본 {total_c}건 · KMLE 후보 {total_q}건")
    for name, c_hits, q_hits in details:
        if c_hits or q_hits:
            sample_q = ", ".join(q_hits[:8]) + (f" … (+{len(q_hits) - 8})" if len(q_hits) > 8 else "")
            print(f"\n- {name}")
            if c_hits:
                print(f"    정리본: {', '.join(c_hits)}")
            if q_hits:
                print(f"    KMLE 후보({len(q_hits)}): {sample_q}")
    return 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--check", action="store_true", help="레지스트리와 대조표 YAML 검증")
    ap.add_argument("--summary", action="store_true", help="Tier·과별 현황 요약")
    ap.add_argument("--batch", help="과목명·슬러그·tier1/2/3 배치 체크리스트 및 Opus 프롬프트 출력")
    ap.add_argument("--scan-existing", help="기존 KMLE·정리본 중 관련 후보 스캔")
    a = ap.parse_args(argv)

    if a.check or not any((a.summary, a.batch, a.scan_existing)):
        errs = check_all()
        if errs:
            for e in errs:
                print("  ✗", e)
            return 1
        reg = load_registry()
        print(f"kr_guidelines --check 통과: {len(reg.get('guidelines') or [])}개 트랙 · 슬롯/H22 대응 이상 없음")
        if not any((a.summary, a.batch, a.scan_existing)):
            return 0

    reg = load_registry()
    if a.summary:
        return cmd_summary(reg)
    if a.batch:
        return cmd_batch(reg, load_h22(), a.batch)
    if a.scan_existing:
        return cmd_scan(reg, a.scan_existing)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
