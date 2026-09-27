"""concept_figures.py — 개념 정리본에 싣는 그림(심전도·조직·영상 사진)의 후보 찾기·붙이기·점검(결정론).

2026-09-27 사용자 요청: 오답 정리본에 ECG·병리 소견 같은 그림을 넣는다. 조건(사용자 지시)
  1. **확실한 라벨만** — 전문가가 판정한 데이터셋 라벨(데이터 논문이 있고 여러 연구에 쓰인 것)이거나,
     동료 심사 논문의 그림 설명에 그 소견이라고 적힌 그림. 모델(Claude)이 그림을 보고 붙인 판독은 라벨로 쓰지 않는다.
  2. 그림은 **이미 모아 둔 풀**(exam-builder open_assets — 틀린 영상 문항의 그림이 여기서 왔다)에서 고른다.
     풀에 없으면 `figures_wanted` 로 요청을 남기고, exam-builder 의 아침 수확(`opendata demand`)이 조금씩 받아 온다.

역할 나눔 — 무엇을 보여 줄지(shows)·어디서 보라(look_for)·어느 절에 둘지(at)는 정리본을 쓰는 모델이 정한다.
**라벨·라벨 근거·데이터 논문·출처 표기·라이선스·파일은 이 스크립트가 풀 기록에서 그대로 옮긴다**(모델이 지어낼 수 없게).

  python pipelines/concept_figures.py find 심방조동 AFLT          # 쓸 수 있는 후보(기준을 통과한 것만)
  python pipelines/concept_figures.py find --all LIDC              # 기준 밖 후보도 이유와 함께
  python pipelines/concept_figures.py add <정리본 id> <자산 id> --at "<절 제목>" --shows "…" --look "…" --look "…"
  python pipelines/concept_figures.py want <정리본 id> --source PTBXL --codes AFLT --shows "…" [--at …]
  python pipelines/concept_figures.py want <정리본 id> --source PMC_OA --query "<Europe PMC 검색식>" --caption-terms "peaked,T wave" --modality ECG --shows "…"
  python pipelines/concept_figures.py add <정리본 id> <PMC 자산> --privacy-checked "얼굴·문신·이름 없음 확인" [--crop x0,y0,x1,y1] …
  python pipelines/concept_figures.py reject <정리본 id> <자산 id> "<붙이지 않는 이유>"   # 수확이 다음 후보를 받는다
  python pipelines/concept_figures.py none <정리본 id> "<그림이 필요 없는 이유>"
  python pipelines/concept_figures.py check                         # 모든 정리본의 그림 계약 점검
  python pipelines/concept_figures.py status                        # 붙임·요청·불필요·미판단 집계

풀 위치: 환경변수 MEDKOS_BUILDER → ../exam-builder → ~/exam-builder (루틴 컨테이너는 두 저장소를 나란히 받는다).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
FIG_DIR = ROOT / "docs" / "assets" / "figures"
CONCEPT_DIR = ROOT / "content" / "concepts"
MAX_FIGURES = 3                 # 한 정리본에 싣는 그림 상한(학습서 배치 — 그림이 본문을 밀어내지 않게)
MAX_PX = 1600                   # 저장소·PDF 에 넣는 긴 변 상한(원본은 풀에 남는다)

# ── 라벨 근거를 인정하는 출처(데이터 논문은 2026-09-27 Crossref 로 서지·피인용 수 확인) ─────────────
# basis: dataset_expert = 전문가 판정 라벨(인스턴스 단위) · published_figure = 동료 심사 논문의 그림 설명
FIGURE_SOURCES: dict[str, dict[str, Any]] = {
    "PTBXL": {
        "kind": "ecg", "basis": "dataset_expert",
        "reference": "심장내과 전문의의 SCP-ECG 판독을 두 번째 전문의가 검증 — 해당 진술의 가능도 100 인 기록만",
        "paper": "Wagner P 외. PTB-XL, a large publicly available electrocardiography dataset. Sci Data 2020;7:154",
        "doi": "10.1038/s41597-020-0495-6", "cited_by": 1213},
    "CHAPMAN_NINGBO": {
        "kind": "ecg", "basis": "dataset_expert",
        "reference": "의사 1명이 리듬·심장 상태를 판정하고 다른 의사가 검증",
        "paper": "Zheng J 외. A 12-lead electrocardiogram database for arrhythmia research covering more than 10,000 patients. Sci Data 2020;7:48",
        "doi": "10.1038/s41597-020-0386-x", "cited_by": 437},
    "ISIC": {
        "kind": "dermoscopy", "basis": "dataset_expert",
        "reference": "이미지마다 조직병리 검사로 확진(ISIC 기록 diagnosis_confirm_type = histopathology)",
        "paper": "Codella NCF 외. Skin lesion analysis toward melanoma detection: a challenge at ISBI 2017. ISBI 2018:168-172",
        "doi": "10.1109/ISBI.2018.8363547", "cited_by": 1935},
    "IDRID": {
        "kind": "fundus", "basis": "dataset_expert",
        "reference": "안과 전문의의 ICDR 당뇨망막병증 중증도 판정",
        "paper": "Porwal P 외. Indian Diabetic Retinopathy Image Dataset (IDRiD). Data 2018;3(3):25",
        "doi": "10.3390/data3030025", "cited_by": 849},
    "FRACATLAS": {
        "kind": "radiograph", "basis": "dataset_expert",
        "reference": "영상의학과 전문의와 의사가 골절 유무와 위치(상자)를 표시",
        "paper": "Abedeen I 외. FracAtlas: a dataset for fracture classification, localization and segmentation. Sci Data 2023;10:521",
        "doi": "10.1038/s41597-023-02432-4", "cited_by": 114},
    "GRAZPEDWRI_DX": {
        "kind": "radiograph", "basis": "dataset_expert",
        "reference": "소아 손목 X선의 골절·골막반응 등을 전문가가 상자로 주석",
        "paper": "Nagy E 외. A pediatric wrist trauma X-ray dataset (GRAZPEDWRI-DX) for machine learning. Sci Data 2022;9:222",
        "doi": "10.1038/s41597-022-01328-z", "cited_by": 101},
    "TCIA_AML_CYTOMORPHOLOGY": {
        "kind": "smear", "basis": "dataset_expert",
        "reference": "숙련 검사자의 단일세포 형태 판정(일부는 재판정으로 일치도 측정)",
        "paper": "Matek C 외. Human-level recognition of blast cells in acute myeloid leukaemia with convolutional neural networks. Nat Mach Intell 2019;1:538-544",
        "doi": "10.1038/s42256-019-0101-9", "cited_by": 256},
    "FETAL_PLANES_ZENODO": {
        "kind": "ultrasound", "basis": "dataset_expert",
        "reference": "산과 전문가의 표준 단면 분류(질병 라벨 없음 — 정상 해부 단면으로만 쓴다)",
        "paper": "Burgos-Artizzu XP 외. Evaluation of deep convolutional neural networks for automatic classification of common maternal fetal ultrasound planes. Sci Rep 2020;10:10200",
        "doi": "10.1038/s41598-020-67076-5", "cited_by": 209},
    "HPA": {
        "kind": "histology", "basis": "dataset_expert",
        "reference": "조직 종류·표본 진단 = 표본 기록(병리의사 SNOMED 주석), 세포별 염색 강도 = HPA 병리의사 주석(이 항체·조직의 요약 — 사진 한 장 단위가 아님)",
        "paper": "Uhlén M 외. Tissue-based map of the human proteome. Science 2015;347:1260419",
        "doi": "10.1126/science.1260419", "cited_by": 14435},
    # 판독의 윤곽(LIDC XML)으로 고른 슬라이스만(exam-builder `opendata fetch-nodules`, 2026-09-27). 위치로 고른 옛 슬라이스는 제외 그대로.
    "TCIA_LIDC_IDRI": {
        "kind": "ct", "basis": "dataset_expert",
        "reference": "흉부영상의학과 판독의 4명 중 3명 이상이 바로 이 슬라이스에 결절 윤곽을 그렸다(LIDC XML 합의)",
        "paper": "Armato SG 3rd 외. The Lung Image Database Consortium (LIDC) and Image Database Resource Initiative (IDRI): a completed reference database of lung nodules on CT scans. Med Phys 2011;38(2):915-931",
        "doi": "10.1118/1.3528204", "cited_by": 2481},
    "PMC_OA": {
        "kind": None, "basis": "published_figure",
        "reference": "동료 심사 논문의 그림 설명(저자가 그 소견이라고 쓴 그림)",
        "paper": "", "doi": "", "cited_by": None},
}
# 풀에 있지만 라벨이 인스턴스 단위가 아니거나(환자·시리즈 단위) 작성자 판독인 출처 — 정리본 그림으로 쓰지 않는다
EXCLUDED_SOURCES = {
    "TCIA_LIDC_IDRI": "슬라이스 소견은 작성자 판독(시리즈 단위 라벨, Grade B)",
    "TCIA_PANCREAS_CT": "슬라이스 소견은 작성자 판독(Grade B)",
    "TCIA_COVID19_AR": "영상 소견 라벨이 없다(임상 진단만, Grade B)",
    "TCIA_UPENN_GBM": "환자 단위 진단 — 이 슬라이스의 병변은 작성자 판독(Grade B). 분할 마스크로 고른 슬라이스만 후보가 된다(미구현)",
    "TCIA_TCGA_UCEC": "환자 단위 진단 — 슬라이스 소견은 작성자 판독(Grade B)",
    "TCIA_CPTAC_UCEC": "환자 단위 진단 — 슬라이스 소견은 작성자 판독(Grade B)",
    "PHYSIONET_CTU_UHB": "태아심박동 소견은 작성자 판독 — 데이터셋 라벨은 분만 결과(pH·Apgar)뿐",
}
REDISTRIBUTABLE = re.compile(r"(CC0|CC-0|Creative Commons Zero|Public Domain|CC BY|CC-BY|Creative Commons Attribution(?! Non)|"
                             r"Open Data Commons Attribution|ODC-BY)", re.I)
NONCOMMERCIAL = re.compile(r"(NC\b|NonCommercial|Non-Commercial)", re.I)
KINDS = ("ecg", "ctg", "dermoscopy", "fundus", "radiograph", "ct", "mri", "ultrasound", "histology", "smear", "photo", "gross")
_PMC_KIND = {"ULTRASOUND": "ultrasound", "CT": "ct", "MR": "mri", "HISTOLOGY": "histology", "HISTOLOGY_HE": "histology",
             "HISTOLOGY_IHC": "histology", "GROSS_PHOTO": "gross", "CTG": "ctg", "CLINICAL_PHOTO": "photo", "ECG": "ecg", "DX": "radiograph",
             "CR": "radiograph", "XR_MSK": "radiograph", "DERMOSCOPY": "dermoscopy", "FUNDUS": "fundus", "BLOOD_SMEAR": "smear"}


# ── 풀 ─────────────────────────────────────────────────────────────────────
def builder_root() -> Path | None:
    for p in (os.environ.get("MEDKOS_BUILDER"), ROOT.parent / "exam-builder", Path.home() / "exam-builder"):
        if p and (Path(p) / "open_assets" / "pool_manifest.jsonl").exists():
            return Path(p)
    return None


def load_pool(builder: Path | None = None) -> dict[str, dict]:
    b = builder or builder_root()
    if not b:
        return {}
    out: dict[str, dict] = {}
    for line in (b / "open_assets" / "pool_manifest.jsonl").read_text(encoding="utf-8").splitlines():
        if line.strip():
            r = json.loads(line)
            out[str(r.get("asset_id"))] = r          # 같은 id 가 다시 나오면 나중 기록(갱신)이 이긴다
    return out


def _gate(r: dict, name: str) -> str:
    return str(((r.get("gates") or {}).get(name) or {}).get("status") or "")


def eligibility(r: dict) -> list[str]:
    """정리본 그림으로 쓸 수 없는 이유 목록(빈 목록 = 통과)."""
    why: list[str] = []
    src = str(r.get("source_id") or "")
    L = r.get("label") or {}
    if r.get("status") == "REJECTED":
        why.append("풀에서 폐기된 자산")
    ann = L.get("annotation") if isinstance(L.get("annotation"), dict) else {}
    contour_ok = src == "TCIA_LIDC_IDRI" and ann.get("source") == "LIDC XML" and int(ann.get("readers_on_slice") or 0) >= 3
    if src in EXCLUDED_SOURCES and not contour_ok:
        why.append(EXCLUDED_SOURCES[src] + (" — 판독의 윤곽으로 고른 슬라이스(fetch-nodules)만 쓸 수 있다" if src == "TCIA_LIDC_IDRI" else ""))
    elif src not in FIGURE_SOURCES:
        why.append(f"라벨 근거를 확인하지 않은 출처({src})")
    lic = str(r.get("license_name") or "")
    if not REDISTRIBUTABLE.search(lic) or NONCOMMERCIAL.search(lic):
        why.append(f"공개 저장소에 다시 싣기 어려운 라이선스({lic or '없음'})")
    for g in ("rights", "privacy"):
        st = _gate(r, g)
        if st and st != "PASS":
            why.append(f"{g} 게이트 {st}" + (" — 그림을 보고 얼굴·문신·이름이 없으면 add --privacy-checked" if g == "privacy" else ""))
    if src in FIGURE_SOURCES and FIGURE_SOURCES[src]["basis"] == "dataset_expert":
        if str(L.get("grade") or "") != "A":
            why.append(f"라벨 등급 {L.get('grade') or '없음'}(A 만)")
        if not str(L.get("primary") or "").strip():
            why.append("데이터셋 라벨(primary)이 없다")
        if src == "ISIC" and str(L.get("confirm_type") or "").lower() != "histopathology":
            why.append("ISIC 조직병리 확진이 아니다")
        if src == "PTBXL":
            code = L.get("primary_code")
            if code and float((L.get("scp_codes") or {}).get(code, 0) or 0) < 100:
                why.append(f"PTB-XL {code} 가능도 100 미만")
    if src == "PMC_OA" and not str(L.get("caption_full") or "").strip():
        why.append("논문 그림 설명이 없다")
    if not r.get("file"):
        why.append("파일 없음")
    return why


def dataset_label(r: dict) -> str:
    """그림 아래 「데이터 라벨」로 싣는 글 — 풀 기록에서 그대로(번역·요약하지 않는다)."""
    src = str(r.get("source_id") or "")
    L = r.get("label") or {}
    if src == "PTBXL":
        return f"{L.get('primary')} (SCP {L.get('primary_code')}, 가능도 {int(float((L.get('scp_codes') or {}).get(L.get('primary_code'), 0) or 0))})"
    if src == "ISIC":
        return f"{L.get('primary')} — 조직병리 확진"
    if src == "HPA":
        cells = "; ".join(f"{c.get('cell_type')}: {c.get('level')}" for c in L.get("cell_annotations") or [] if isinstance(c, dict))
        gene = L.get("gene") or ""
        dx = str(L.get("diagnosis") or "").split(" (")[0]
        return (f"{L.get('primary')}" + (f"(표본 진단 {dx})" if dx else "") + f", {gene} 면역조직화학"
                + (f" — 병리의사 주석(항체·조직 요약) {cells}" if cells else ""))
    if src == "IDRID":
        return f"{L.get('primary')} (ICDR {L.get('primary_code')})"
    if src in ("FRACATLAS", "GRAZPEDWRI_DX"):
        n = len([o for o in L.get("objects") or [] if isinstance(o, dict) and "fract" in str(o.get("name", ""))])
        ao = f" · AO/OTA 소아 분류 {L['ao_classification']}" if L.get("ao_classification") else ""
        return f"{L.get('primary')}{ao}" + (f" — 골절 주석 상자 {n}개" if n else "")
    if src == "TCIA_LIDC_IDRI":
        a = L.get("annotation") or {}
        ch = a.get("characteristics_mean") or {}
        d = f", 윤곽 긴 지름 약 {a['diameter_mm_est']} mm" if a.get("diameter_mm_est") else ""
        m = f" · 판독의 악성 의심 점수 평균 {ch['malignancy']}/5(주관 평가 — 병리 확진 아님)" if ch.get("malignancy") else ""
        return f"{L.get('primary')} — 판독의 {a.get('readers_on_slice')}/4 명이 이 슬라이스에 윤곽{d}{m}"
    if src == "PMC_OA":
        return f"「{str(L.get('caption_full') or '').strip()}」 — {L.get('article_title') or ''}"
    return str(L.get("primary") or "")


def kind_of(r: dict) -> str:
    src = str(r.get("source_id") or "")
    k = (FIGURE_SOURCES.get(src) or {}).get("kind")
    return k or _PMC_KIND.get(str(r.get("modality") or "").upper(), "photo")


def reference_of(r: dict) -> dict:
    src = str(r.get("source_id") or "")
    S = FIGURE_SOURCES[src]
    L = r.get("label") or {}
    if src == "PMC_OA":
        return {"basis": "published_figure", "reference": S["reference"],
                "paper": f"{L.get('article_title') or ''}. {L.get('journal') or ''}".strip(" ."),
                "doi": re.sub(r"^https?://(dx\.)?doi\.org/", "", str(r.get("doi") or L.get("doi") or "")), "cited_by": None}
    return {"basis": S["basis"], "reference": S["reference"], "paper": S["paper"], "doi": S["doi"], "cited_by": S["cited_by"]}


def search_text(r: dict) -> str:
    L = r.get("label") or {}
    return " ".join(str(x) for x in (r.get("asset_id"), r.get("source_id"), r.get("modality"), L.get("primary"), L.get("primary_code"),
                                     L.get("gene"), L.get("caption_full"), L.get("article_title"),
                                     " ".join((L.get("scp_codes") or {}).keys()),
                                     " ".join(str(v) for v in (L.get("diagnosis_chain") or {}).values()))).lower()


def find(terms: list[str], pool: dict[str, dict], show_all: bool = False) -> list[tuple[dict, list[str]]]:
    out = []
    for r in pool.values():
        t = search_text(r)
        if terms and not all(x.lower() in t for x in terms):
            continue
        why = eligibility(r)
        if why and not show_all:
            continue
        out.append((r, why))
    return sorted(out, key=lambda x: (bool(x[1]), str(x[0].get("source_id")), str(x[0].get("asset_id"))))


# ── 정리본 파일 다루기(frontmatter 만 고친다 — 본문은 그대로) ────────────────
def concept_path(cid: str) -> Path:
    hits = list(CONCEPT_DIR.rglob(f"{cid}.md"))
    if not hits:
        raise SystemExit(f"정리본 {cid} 이 없다")
    return hits[0]


def split_fm(text: str) -> tuple[dict, str, str]:
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        raise SystemExit("frontmatter 가 없다")
    return yaml.safe_load(m.group(1)) or {}, m.group(1), text[m.end():]


def _dump_block(key: str, value: Any) -> str:
    return yaml.safe_dump({key: value}, allow_unicode=True, sort_keys=False, width=1000).rstrip("\n")


def set_fm_key(path: Path, key: str, value: Any, bump: bool = True) -> None:
    """frontmatter 의 한 키만 바꾼다(없으면 끝에 더한다). 다른 키의 모양(주석·따옴표)은 건드리지 않는다."""
    text = path.read_text(encoding="utf-8")
    meta, raw, body = split_fm(text)
    lines = raw.split("\n")
    start = next((i for i, l in enumerate(lines) if re.match(rf"^{re.escape(key)}:", l)), None)
    new = _dump_block(key, value).split("\n") if value is not None else []
    if start is None:
        lines += new
    else:
        end = start + 1
        while end < len(lines) and (lines[end].startswith((" ", "-")) or not lines[end].strip()):
            end += 1
        lines[start:end] = new
    raw2 = "\n".join(lines)
    if bump:
        v = int(meta.get("version") or 1) + 1
        raw2 = re.sub(r"^version:.*$", f"version: {v}", raw2, count=1, flags=re.M)
        from datetime import datetime, timedelta, timezone
        today = (datetime.now(timezone.utc) + timedelta(hours=9)).strftime("%Y-%m-%d")
        raw2 = re.sub(r"^updated:.*$", f"updated: {today}", raw2, count=1, flags=re.M)
    path.write_text(f"---\n{raw2}\n---\n{body}", encoding="utf-8", newline="\n")


def section_titles(path: Path) -> list[str]:
    _, _, body = split_fm(path.read_text(encoding="utf-8"))
    return [re.sub(r"^\(심화\)\s*", "", t).strip() for t in re.findall(r"^##\s+(.+?)\s*$", body, re.M)]


# ── 파일 옮기기 ──────────────────────────────────────────────────────────────
def copy_image(r: dict, builder: Path, crop: str = "", mark: bool = False) -> str:
    """풀 파일을 docs/assets/figures/ 로(긴 변 MAX_PX 로 줄여). 반환 = 저장소 상대경로(docs/ 기준 아님)."""
    from PIL import Image
    src = builder / "open_assets" / str(r["file"])
    if not src.exists():
        raise SystemExit(f"풀 파일이 없다: {src}")
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    stem = re.sub(r"[^a-z0-9._-]+", "-", str(r["asset_id"]).lower()).strip("-")
    im = Image.open(src)
    if mark:                                        # 데이터셋 주석 위치(상자)를 노란 테두리로 — 자르기 전 원본 좌표
        from PIL import ImageDraw
        im = im.convert("RGB")
        d = ImageDraw.Draw(im)
        wpx = max(2, round(max(im.size) / 300))
        for o in (r.get("label") or {}).get("objects") or []:
            if isinstance(o, dict) and o.get("name") != "text":
                pad = max(4, round(max(im.size) / 90))
                d.rectangle([o["xmin"] - pad, o["ymin"] - pad, o["xmax"] + pad, o["ymax"] + pad], outline=(255, 200, 0), width=wpx)
        stem += "-mark"
    if crop:                                        # 여러 패널 그림에서 한 패널만(원본 픽셀) — 자르기만, 늘이기·보정 없음
        x0, y0, x1, y1 = (int(v) for v in crop.split(","))
        im = im.crop((x0, y0, x1, y1))
        if min(im.size) < 250:
            raise SystemExit(f"잘라 낸 패널이 {im.size[0]}×{im.size[1]} 픽셀 — 250 픽셀 미만은 인쇄에서 소견이 안 보인다")
        stem += "-" + "-".join(crop.split(","))
    im.thumbnail((MAX_PX, MAX_PX))
    if kind_of(r) in ("ecg", "ctg"):                # 선 그림(심전도·태아심박동)은 PNG 로 — JPEG 는 격자선이 뭉개진다
        out = FIG_DIR / f"{stem}.png"
        im.convert("RGB").save(out, optimize=True)
    else:
        out = FIG_DIR / f"{stem}.jpg"
        im.convert("RGB").save(out, quality=86, optimize=True, progressive=True)
    return str(out.relative_to(ROOT)).replace("\\", "/")


def figure_record(r: dict, file: str, at: str, shows: str, look: list[str], from_q: str = "", privacy: str = "", crop: str = "",
                  mark: bool = False) -> dict:
    ref = reference_of(r)
    rec = {
        "id": "", "file": file, "kind": kind_of(r), "at": at, "shows": shows, "look_for": look,
        "label": dataset_label(r), "label_basis": ref["basis"], "reference": ref["reference"],
        "paper": ref["paper"], "doi": ref["doi"],
        "credit": str(r.get("attribution_text") or r.get("dataset") or ""),
        "license": str(r.get("license_name") or ""), "url": str(r.get("item_url") or r.get("canonical_url") or ""),
        "asset": str(r["asset_id"]),
    }
    if ref.get("cited_by"):
        rec["paper_cited_by"] = ref["cited_by"]
    if from_q:
        rec["from_question"] = from_q
    if privacy:
        rec["privacy_check"] = privacy
    if crop:
        rec["crop"] = crop
    if mark:
        rec["marked"] = "노란 테두리 = 데이터셋 주석 위치(판독의·전문가가 표시한 곳)"
    return rec


# ── 점검 ────────────────────────────────────────────────────────────────────
FIG_KEYS = ("file", "kind", "shows", "look_for", "label", "label_basis", "reference", "credit", "license", "asset")


def validate_figures(meta: dict, section_names: list[str] | None = None, root: Path = ROOT) -> list[str]:
    """정리본 frontmatter 의 figures · figures_wanted · figures_none 계약. [WARN] 접두는 경고."""
    errs: list[str] = []
    figs = meta.get("figures")
    if figs is not None and not isinstance(figs, list):
        return ["figures 는 목록"]
    figs = figs or []
    if len(figs) > MAX_FIGURES:
        errs.append(f"그림은 정리본마다 {MAX_FIGURES}개까지(지금 {len(figs)}개) — 학습서에서 본문을 밀어낸다")
    ids = set()
    for i, f in enumerate(figs, 1):
        if not isinstance(f, dict):
            errs.append(f"figures[{i}] 는 사전"); continue
        for k in FIG_KEYS:
            if f.get(k) in (None, "", []):
                errs.append(f"figures[{i}] 필수 필드 누락: {k} — `concept_figures.py add` 로 붙이면 채워진다")
        fid = str(f.get("id") or "")
        if not re.fullmatch(r"f\d+", fid):
            errs.append(f"figures[{i}].id 는 f1·f2 …")
        if fid in ids:
            errs.append(f"figures id 중복: {fid}")
        ids.add(fid)
        file = str(f.get("file") or "")
        if file and (not file.startswith("docs/assets/figures/") or ".." in file or not (root / file).exists()):
            errs.append(f"figures[{i}].file '{file}' 이 docs/assets/figures/ 안에 없다")
        if f.get("kind") and f["kind"] not in KINDS:
            errs.append(f"figures[{i}].kind 는 {'/'.join(KINDS)} 중 하나")
        if f.get("label_basis") not in ("dataset_expert", "published_figure"):
            errs.append(f"figures[{i}].label_basis 는 dataset_expert · published_figure 만 — 모델 판독은 라벨이 아니다")
        if f.get("label_basis") == "dataset_expert" and not (f.get("paper") and f.get("doi")):
            errs.append(f"figures[{i}] 데이터셋 라벨은 데이터 논문(paper·doi)이 필요하다")
        lic = str(f.get("license") or "")
        if lic and (not REDISTRIBUTABLE.search(lic) or NONCOMMERCIAL.search(lic)):
            errs.append(f"figures[{i}] 라이선스 '{lic}' 는 공개 저장소에 다시 싣기 어렵다")
        look = f.get("look_for") or []
        if not isinstance(look, list) or not 1 <= len(look) <= 3:
            errs.append(f"figures[{i}].look_for 는 1~3개(보는 곳)")
        if len(str(f.get("shows") or "")) > 90:
            errs.append(f"[WARN] figures[{i}].shows 가 길다 — 그림이 보여 주는 소견 한 줄")
        at = str(f.get("at") or "")
        if section_names is not None and at and at not in section_names:
            errs.append(f"figures[{i}].at '{at}' 인 절이 본문에 없다(있는 절: {', '.join(section_names[:6])} …)")
    wanted = meta.get("figures_wanted")
    if wanted is not None:
        if not isinstance(wanted, list):
            errs.append("figures_wanted 는 목록")
        else:
            for i, w in enumerate(wanted, 1):
                if not isinstance(w, dict) or not w.get("source") or not w.get("shows"):
                    errs.append(f"figures_wanted[{i}] 는 {{source, shows, codes|diagnoses|genes|tissues|query|note}}")
                elif w.get("source") == "PMC_OA" and not (w.get("query") and w.get("caption_terms") and w.get("modality")):
                    errs.append(f"figures_wanted[{i}] PMC_OA 요청은 query · caption_terms · modality 가 필요하다")
                elif w.get("source") not in FIGURE_SOURCES and not w.get("note"):
                    errs.append(f"figures_wanted[{i}] 출처 {w.get('source')} 는 라벨 근거를 확인하지 않았다 — 무엇이 필요한지 note 로 적는다")
    none = meta.get("figures_none")
    if none is not None and (not isinstance(none, str) or len(none.strip()) < 6):
        errs.append("figures_none 은 그림이 필요 없는 이유 한 문장")
    if none and figs:
        errs.append("figures_none 과 figures 가 함께 있다 — 하나만")
    return errs


def status(concepts: dict[str, dict]) -> dict[str, list[str]]:
    out: dict[str, list[str]] = {"붙임": [], "요청": [], "불필요": [], "미판단": []}
    for cid, c in sorted(concepts.items()):
        if c.get("figures"):
            out["붙임"].append(cid)
        elif c.get("figures_wanted"):
            out["요청"].append(cid)
        elif c.get("figures_none"):
            out["불필요"].append(cid)
        else:
            out["미판단"].append(cid)
    return out


def request_key(concept: str, w: dict) -> str:
    """exam-builder opendata/demand.py 의 request_key 와 같아야 한다(PMC 그림이 어느 요청의 답인지 잇는 열쇠)."""
    parts = [concept, str(w.get("source"))] + [f"{k}={','.join(map(str, w.get(k) or []))}" for k in ("codes", "diagnoses", "genes", "tissues")]
    parts.append(str(w.get("query") or ""))
    return hashlib.sha1("|".join(parts).encode("utf-8")).hexdigest()[:12]


def _privacy_only(why: list[str]) -> bool:
    return bool(why) and all(w.startswith("privacy 게이트") for w in why)


def wanted_fulfilled(w: dict, pool: dict[str, dict], concept: str = "", rejected: set[str] | None = None) -> list[str]:
    """요청 하나를 채우는 풀 자산(기준 통과 — PMC 는 개인정보 육안 확인만 남은 것도 후보)."""
    src = str(w.get("source") or "")
    rejected = rejected or set()
    if src == "PMC_OA":
        key = request_key(concept, w)
        return sorted(str(r["asset_id"]) for r in pool.values()
                      if str(r.get("source_id")) == "PMC_OA" and str(r["asset_id"]) not in rejected
                      and ((r.get("label") or {}).get("demand") or {}).get("key") == key
                      and (not eligibility(r) or _privacy_only(eligibility(r))))
    keys = [str(x).lower() for x in (w.get("codes") or []) + (w.get("diagnoses") or []) + (w.get("genes") or [])]
    tissues = [str(x).lower() for x in w.get("tissues") or []]
    hits = []
    for r in pool.values():
        if str(r.get("source_id")) != src or eligibility(r) or str(r.get("asset_id")) in rejected:
            continue
        L = r.get("label") or {}
        codes = {str(k).lower() for k in (L.get("scp_codes") or {}) if float((L.get("scp_codes") or {}).get(k) or 0) >= 100}
        codes |= {str(L.get("primary_code") or "").lower(), str(L.get("primary") or "").lower(), str(L.get("gene") or "").lower()}
        codes |= {str(v).lower() for v in (L.get("diagnosis_chain") or {}).values()}
        if keys and not any(k in codes for k in keys):
            continue
        if tissues and str(L.get("primary") or "").lower() not in tissues:
            continue
        if not keys and not tissues:
            continue
        hits.append(str(r["asset_id"]))
    return sorted(hits)


# ── CLI ─────────────────────────────────────────────────────────────────────
def _load_concepts() -> dict[str, dict]:
    from concepts import load_concepts
    return load_concepts()[0]


def main(argv: list[str]) -> int:
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("find"); p.add_argument("terms", nargs="*"); p.add_argument("--all", action="store_true")
    p = sub.add_parser("add")
    p.add_argument("concept"); p.add_argument("asset")
    p.add_argument("--at", required=True); p.add_argument("--shows", required=True)
    p.add_argument("--look", action="append", required=True); p.add_argument("--from-question", default="")
    p.add_argument("--privacy-checked", default="", help="그림을 직접 보고 확인한 것(얼굴·문신·이름·병원 표지 없음) — 개인정보 게이트가 검토 전인 PMC 그림에 필요")
    p.add_argument("--crop", default="", help="한 패널만 x0,y0,x1,y1(원본 픽셀)")
    p.add_argument("--mark", action="store_true", help="데이터셋 주석 상자(결절·골절 위치)를 노란 테두리로 표시")
    p = sub.add_parser("want")
    p.add_argument("concept"); p.add_argument("--source", required=True); p.add_argument("--shows", required=True)
    for k in ("codes", "diagnoses", "genes", "tissues"):
        p.add_argument(f"--{k}", default="")
    p.add_argument("--at", default=""); p.add_argument("--note", default="")
    p.add_argument("--query", default="", help="PMC_OA: Europe PMC 검색식(영어)")
    p.add_argument("--caption-terms", default="", help="PMC_OA: 그림 설명에 모두 들어 있어야 하는 단어, 쉼표 구분")
    p.add_argument("--modality", default="", help="PMC_OA: ECG · CT · MR · ULTRASOUND · HISTOLOGY_HE · CLINICAL_PHOTO …")
    p = sub.add_parser("reject"); p.add_argument("concept"); p.add_argument("asset"); p.add_argument("reason")
    p = sub.add_parser("none"); p.add_argument("concept"); p.add_argument("reason")
    sub.add_parser("check")
    sub.add_parser("status")
    a = ap.parse_args(argv)

    if a.cmd == "find":
        pool = load_pool()
        if not pool:
            print("풀을 찾지 못했다 — MEDKOS_BUILDER 또는 ../exam-builder"); return 1
        rows = find(a.terms, pool, a.all)
        for r, why in rows:
            mark = "✔" if not why else "✗"
            print(f"{mark} {r['asset_id']:<42} {kind_of(r):<10} {dataset_label(r)[:90]}" + (f"\n     └ 쓸 수 없음: {'; '.join(why)}" if why else ""))
        print(f"— {len(rows)}건" + ("" if a.all else " (기준 통과만 — --all 로 전부)"))
        return 0

    if a.cmd == "add":
        builder = builder_root()
        pool = load_pool(builder)
        r = pool.get(a.asset)
        if not r:
            raise SystemExit(f"풀에 {a.asset} 이 없다")
        why = eligibility(r)
        if why and not (_privacy_only(why) and a.privacy_checked.strip()):
            raise SystemExit("이 자산은 정리본 그림 기준을 통과하지 못한다: " + "; ".join(why))
        path = concept_path(a.concept)
        secs = section_titles(path)
        if a.at not in secs:
            raise SystemExit(f"--at '{a.at}' 인 절이 없다. 있는 절: {secs}")
        meta, _, _ = split_fm(path.read_text(encoding="utf-8"))
        figs = list(meta.get("figures") or [])
        if any(f.get("asset") == a.asset for f in figs):
            print("이미 붙어 있다"); return 0
        if len(figs) >= MAX_FIGURES:
            raise SystemExit(f"그림은 {MAX_FIGURES}개까지")
        if a.mark and not any(isinstance(o, dict) and o.get("name") != "text" for o in (r.get("label") or {}).get("objects") or []):
            raise SystemExit("--mark: 이 자산에는 데이터셋 주석 상자가 없다")
        rec = figure_record(r, copy_image(r, builder, a.crop, a.mark), a.at, a.shows.strip(), [x.strip() for x in a.look], a.from_question,
                            a.privacy_checked.strip() if _privacy_only(why) else "", a.crop, a.mark)
        rec["id"] = f"f{max([int(str(f.get('id', 'f0'))[1:] or 0) for f in figs] + [0]) + 1}"
        figs.append(rec)
        set_fm_key(path, "figures", figs)
        if meta.get("figures_none"):
            set_fm_key(path, "figures_none", None, bump=False)
        rest = [w for w in meta.get("figures_wanted") or [] if a.asset not in wanted_fulfilled(w, {a.asset: r}, a.concept)]
        if len(rest) != len(meta.get("figures_wanted") or []):
            set_fm_key(path, "figures_wanted", rest or None, bump=False)
        print(f"{a.concept} ← {rec['id']} {a.asset} ({rec['file']})")
        return 0

    if a.cmd == "want":
        path = concept_path(a.concept)
        meta, _, _ = split_fm(path.read_text(encoding="utf-8"))
        w = {"source": a.source, "shows": a.shows}
        for k in ("codes", "diagnoses", "genes", "tissues"):
            v = [x.strip() for x in getattr(a, k).split(",") if x.strip()]
            if v:
                w[k] = v
        if a.at:
            w["at"] = a.at
        if a.note:
            w["note"] = a.note
        if a.source == "PMC_OA":
            if not (a.query and a.caption_terms and a.modality):
                raise SystemExit("PMC_OA 요청은 --query · --caption-terms · --modality 가 필요하다")
            w.update(query=a.query, caption_terms=[x.strip() for x in a.caption_terms.split(",") if x.strip()], modality=a.modality)
        cur = list(meta.get("figures_wanted") or [])
        if w in cur:
            print("이미 요청했다"); return 0
        set_fm_key(path, "figures_wanted", cur + [w], bump=False)
        if meta.get("figures_none"):
            set_fm_key(path, "figures_none", None, bump=False)
        print(f"{a.concept} — 그림 요청 {w}")
        return 0

    if a.cmd == "reject":
        path = concept_path(a.concept)
        meta, _, _ = split_fm(path.read_text(encoding="utf-8"))
        cur = list(meta.get("figures_rejected") or [])
        if not any(x.get("asset") == a.asset for x in cur if isinstance(x, dict)):
            set_fm_key(path, "figures_rejected", cur + [{"asset": a.asset, "reason": a.reason.strip()}], bump=False)
        print(f"{a.concept} — {a.asset} 거절: {a.reason} (아침 수확이 다음 후보를 받는다)")
        return 0

    if a.cmd == "none":
        path = concept_path(a.concept)
        set_fm_key(path, "figures_none", a.reason.strip(), bump=False)
        print(f"{a.concept} — 그림 불필요: {a.reason}")
        return 0

    concepts = _load_concepts()
    if a.cmd == "status":
        st = status(concepts)
        for k, v in st.items():
            print(f"{k} {len(v)}")
        pool = load_pool()
        for cid in st["요청"]:
            for w in concepts[cid].get("figures_wanted") or []:
                rej = {str(x.get("asset")) for x in concepts[cid].get("figures_rejected") or [] if isinstance(x, dict)}
                hit = wanted_fulfilled(w, pool, cid, rej) if pool else []
                print(f"  요청 {cid}: {w.get('source')} {w.get('codes') or w.get('diagnoses') or w.get('genes') or w.get('tissues') or w.get('query') or w.get('note', '')}"
                      + (f"  → 풀에 들어옴: {', '.join(hit[:3])}" if hit else ""))
        return 0
    bad = 0
    for cid, c in sorted(concepts.items()):
        for e in validate_figures(c, [s["title"] for s in c.get("sections") or []]):
            print(f"  {'⚠' if e.startswith('[WARN]') else '✗'} {cid}: {e}")
            bad += 0 if e.startswith("[WARN]") else 1
    print(f"그림 계약 오류 {bad}건")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    sys.exit(main(sys.argv[1:]))
