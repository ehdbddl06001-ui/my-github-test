"""
ingest_ecg.py — 오픈 ECG 신호(WFDB)를 잘라 assets/ecg/<name>.json 으로 커밋한다.

**데이터 접근이 되는 환경에서 사람이 1회 실행**하는 오프라인 도구다(루틴이 매번
돌리지 않는다). 산출 JSON은 작고 오프라인이며, export 가 이걸 읽어 SVG를 렌더한다
(pipelines/render_signal_svg.py). 진짜 파형 + 오픈 라이선스 + 재현성.

주의(라이선스): 재배포 가능한 오픈 라이선스(예: MIT-BIH=ODC-BY, PTB-XL=CC-BY)만
담고, `source`·`license` 를 반드시 기록·표기한다. PhysioNet 직접 접근이 막힌
환경이면 AWS/GCS 미러나 GitHub 샘플에서 .hea/.dat 를 받아 로컬 경로로 넘긴다.

사용:
  pip install wfdb
  python pipelines/ingest_ecg.py --record /path/to/100 --name mitdb-100 \
      --start 0 --seconds 6 --source "MIT-BIH Arrhythmia DB" --license "ODC-BY 1.0"
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "assets" / "ecg"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--record", required=True, help="WFDB 레코드 경로(확장자 제외)")
    ap.add_argument("--name", required=True, help="에셋 이름 → assets/ecg/<name>.json")
    ap.add_argument("--start", type=float, default=0.0, help="시작 시각(초)")
    ap.add_argument("--seconds", type=float, default=6.0)
    ap.add_argument("--leads", default="", help="쉼표구분 유도명(빈값=전체)")
    ap.add_argument("--source", default="")
    ap.add_argument("--license", default="")
    ap.add_argument("--round", type=int, default=4)
    a = ap.parse_args()

    import wfdb  # 데이터 있는 환경에서만 필요
    rec = wfdb.rdrecord(a.record)
    fs = float(rec.fs)
    i0 = int(a.start * fs)
    i1 = i0 + int(a.seconds * fs)
    want = [s.strip() for s in a.leads.split(",") if s.strip()] or list(rec.sig_name)

    leads = {}
    for name in want:
        j = rec.sig_name.index(name)
        leads[name] = [round(float(v), a.round) for v in rec.p_signal[i0:i1, j]]

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUT_DIR / f"{a.name}.json"
    out.write_text(json.dumps({
        "record": a.name,
        "source": a.source,
        "license": a.license,
        "fs": fs,
        "unit": "mV",
        "start_s": a.start,
        "seconds": a.seconds,
        "leads": leads,
    }, ensure_ascii=False), encoding="utf-8")
    print(f"생성: {out.relative_to(ROOT)} (leads={list(leads)}, {len(next(iter(leads.values())))} samples/lead)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
