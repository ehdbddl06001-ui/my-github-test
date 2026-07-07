"""
render_signal_svg.py — '실제 심전도 신호(mV 시계열) → SVG' 렌더러.

gen_ecg_svg.py(수식 합성)와 짝을 이루는 '실데이터' 경로. 오픈 신호 DB(PhysioNet
PTB-XL·MIT-BIH 등)의 진짜 파형을 렌더한다. 단, **런타임에 DB를 받지 않는다** —
데이터 있는 환경에서 pipelines/ingest_ecg.py 로 한 번 잘라 assets/ecg/*.json 으로
커밋해 두고, export 는 그 JSON만 읽어(네트워크·wfdb 불필요) 결정론적으로 그린다.

이 방식의 이유:
  - 루틴 컨테이너는 외부 DB 접근이 정책상 막힐 수 있고 wfdb도 없다 → 오프라인 렌더.
  - 진짜 모양 + 오픈 라이선스 + 재현성. (모양·ST가 본질인 브루가다·STEMI도 '합성'이
    아니라 '실데이터 렌더'로는 안전하게 다룰 수 있다 — 12유도 확장은 후속.)
"""
from __future__ import annotations

import json
from pathlib import Path

PX_PER_MM = 6.0
PX_PER_S = PX_PER_MM * 25.0     # 25 mm/s
PX_PER_MV = PX_PER_MM * 10.0    # 10 mm/mV


def _grid(w_px: int, h_px: int) -> str:
    minor, major = PX_PER_MM, PX_PER_MM * 5
    out = []
    x = 0.0
    while x <= w_px:
        out.append(f'<line x1="{x:.0f}" y1="0" x2="{x:.0f}" y2="{h_px}" '
                   f'class="{"gmaj" if abs(x % major) < 0.5 else "gmin"}"/>')
        x += minor
    y = 0.0
    while y <= h_px:
        out.append(f'<line x1="0" y1="{y:.0f}" x2="{w_px}" y2="{y:.0f}" '
                   f'class="{"gmaj" if abs(y % major) < 0.5 else "gmin"}"/>')
        y += minor
    return "".join(out)


def signal_svg(samples: list[float], fs: float, seconds: float | None = None,
               label: str = "", height_mv: float = 3.0) -> str:
    """mV 시계열 → SVG 스트립. baseline은 중앙값으로 0에 맞춘다."""
    if seconds:
        samples = samples[: int(seconds * fs)]
    if not samples:
        return ""
    med = sorted(samples)[len(samples) // 2]
    w_px = int((len(samples) / fs) * PX_PER_S)
    h_px = int(height_mv * PX_PER_MV)
    mid = h_px / 2
    pts = " ".join(
        f"{(i / fs) * PX_PER_S:.1f},{mid - (v - med) * PX_PER_MV:.1f}"
        for i, v in enumerate(samples)
    )
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w_px} {h_px + 18}" '
        f'width="{w_px}" height="{h_px + 18}" role="img" aria-label="ECG {label}">'
        '<style>.bg{fill:#fff}.gmin{stroke:#f4c9c9;stroke-width:0.5}'
        '.gmaj{stroke:#e59a9a;stroke-width:1}'
        '.trace{fill:none;stroke:#111;stroke-width:1.4;stroke-linejoin:round}'
        '.cap{font:11px -apple-system,Segoe UI,sans-serif;fill:#555}</style>'
        f'<rect class="bg" x="0" y="0" width="{w_px}" height="{h_px}"/>'
        + _grid(w_px, h_px)
        + f'<polyline class="trace" points="{pts}"/>'
        + f'<text class="cap" x="4" y="{h_px + 13}">{label}</text></svg>'
    )


def svg_from_asset(asset_path: str | Path, lead: str | None = None,
                   seconds: float | None = None, label: str | None = None) -> str:
    """assets/ecg/*.json (ingest_ecg.py 산출물)를 읽어 SVG로 렌더한다."""
    data = json.loads(Path(asset_path).read_text(encoding="utf-8"))
    leads = data.get("leads", {})
    if not leads:
        return ""
    name = lead if lead in leads else next(iter(leads))
    cap = label or f'{data.get("record","")} · {name} · {data.get("fs")}Hz · 실데이터'
    return signal_svg(leads[name], float(data.get("fs", 250)),
                      seconds or data.get("seconds"), cap)
