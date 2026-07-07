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
    """assets/ecg/*.json (ingest_ecg.py 산출물)를 읽어 단일 유도 SVG로 렌더한다."""
    data = json.loads(Path(asset_path).read_text(encoding="utf-8"))
    leads = data.get("leads", {})
    if not leads:
        return ""
    name = lead if lead in leads else next(iter(leads))
    cap = label or f'{data.get("record","")} · {name} · {data.get("fs")}Hz · 실데이터'
    return signal_svg(leads[name], float(data.get("fs", 250)),
                      seconds or data.get("seconds"), cap)


# 표준 12유도 배열: 4열(사지·증강·전흉부) × 3행 + 리듬 스트립(II)
LAYOUT_12 = [
    ["I", "AVR", "V1", "V4"],
    ["II", "AVL", "V2", "V5"],
    ["III", "AVF", "V3", "V6"],
]
_CLAMP = 1.6   # mV, 행 간 겹침 방지용 진폭 클램프


def _poly(samples, fs, x0, base_y, n=None):
    if n:
        samples = samples[:n]
    med = sorted(samples)[len(samples) // 2] if samples else 0
    pts = []
    for i, v in enumerate(samples):
        d = max(-_CLAMP, min(_CLAMP, v - med))
        pts.append(f"{x0 + (i / fs) * PX_PER_S:.1f},{base_y - d * PX_PER_MV:.1f}")
    return " ".join(pts)


def twelve_lead_svg(leads: dict, fs: float, sec_per_cell: float = 2.5,
                    label: str = "") -> str:
    """12유도를 표준 3×4 + 리듬 스트립(II)으로 렌더. 각 칸은 같은 시간창을 보여준다."""
    cell_n = int(sec_per_cell * fs)
    cell_w = sec_per_cell * PX_PER_S
    row_h = 108.0
    cols, rows = 4, 3
    pad_top = 8.0
    grid_h = pad_top + rows * row_h
    rhythm_h = row_h
    w_px = int(cols * cell_w)
    h_px = int(grid_h + rhythm_h)
    traces, labels = [], []
    for r, rowdef in enumerate(LAYOUT_12):
        for c, name in enumerate(rowdef):
            if name not in leads:
                continue
            base_y = pad_top + r * row_h + row_h / 2
            traces.append(f'<polyline class="trace" points="{_poly(leads[name], fs, c * cell_w, base_y, cell_n)}"/>')
            labels.append(f'<text class="lead" x="{c * cell_w + 4:.0f}" y="{base_y - row_h / 2 + 13:.0f}">{name}</text>')
    # 리듬 스트립: 유도 II 전체
    if "II" in leads:
        by = grid_h + rhythm_h / 2
        traces.append(f'<polyline class="trace" points="{_poly(leads["II"], fs, 0, by)}"/>')
        labels.append(f'<text class="lead" x="4" y="{grid_h + 14:.0f}">II (rhythm)</text>')
    # 방안지 격자
    minor, major = PX_PER_MM, PX_PER_MM * 5
    grid, x = [], 0.0
    while x <= w_px:
        grid.append(f'<line x1="{x:.0f}" y1="0" x2="{x:.0f}" y2="{h_px}" class="{"gmaj" if abs(x % major) < 0.5 else "gmin"}"/>')
        x += minor
    y = 0.0
    while y <= h_px:
        grid.append(f'<line x1="0" y1="{y:.0f}" x2="{w_px}" y2="{y:.0f}" class="{"gmaj" if abs(y % major) < 0.5 else "gmin"}"/>')
        y += minor
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w_px} {h_px + 16}" '
        f'width="{w_px}" height="{h_px + 16}" role="img" aria-label="12-lead ECG {label}">'
        '<style>.bg{fill:#fff}.gmin{stroke:#f4c9c9;stroke-width:0.5}'
        '.gmaj{stroke:#e59a9a;stroke-width:1}'
        '.trace{fill:none;stroke:#111;stroke-width:1.2;stroke-linejoin:round}'
        '.lead{font:bold 11px sans-serif;fill:#333}.cap{font:11px sans-serif;fill:#555}</style>'
        f'<rect class="bg" x="0" y="0" width="{w_px}" height="{h_px}"/>'
        + "".join(grid) + "".join(traces) + "".join(labels)
        + f'<text class="cap" x="4" y="{h_px + 12}">{label}</text></svg>'
    )


def svg12_from_asset(asset_path: str | Path, sec_per_cell: float = 2.5,
                     label: str | None = None) -> str:
    data = json.loads(Path(asset_path).read_text(encoding="utf-8"))
    leads = data.get("leads", {})
    if not leads:
        return ""
    cap = label or f'{data.get("record","")} · 12-lead · {data.get("fs")}Hz · 실데이터(오픈 DB)'
    return twelve_lead_svg(leads, float(data.get("fs", 100)), sec_per_cell, cap)
