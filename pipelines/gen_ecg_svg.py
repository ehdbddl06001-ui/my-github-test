"""
gen_ecg_svg.py — 결정론적 ECG 리듬 스트립 SVG 생성기 (PoC).

MedKOS '자료' 전략 中 B안: 파형/도표는 AI 이미지가 아니라 **수식 기반으로 결정론적
생성**한다. 라이선스 문제가 없고 정답(간격·리듬)을 우리가 통제하므로 의학적으로 안전.
X선·CT·조직 같은 photorealistic 영상은 범위 밖(여전히 텍스트 소견으로 대체).

파형 모델: 각 심박을 P·Q·R·S·T의 가우시안 합으로 합성(McSharry 단순화).
표준 스케일: 25 mm/s(가로), 10 mm/mV(세로), ECG 방안지(1 mm/5 mm 격자).

사용:
  python pipelines/gen_ecg_svg.py --rhythm sinus --rate 75 --seconds 6 --out ecg.svg
  python pipelines/gen_ecg_svg.py --rhythm afib  --rate 110 --out afib.svg
지원 rhythm: sinus(정상동율동), brady(서맥), tachy(빈맥), afib(심방세동: P소실+불규칙 RR)
"""
from __future__ import annotations

import argparse
import math
import random

# ── 스케일 ────────────────────────────────────────────────
PX_PER_MM = 6.0                 # 1 mm = 6 px (화면 가독성)
MM_PER_S = 25.0                 # 표준 종이 속도
MM_PER_MV = 10.0                # 표준 진폭
PX_PER_S = PX_PER_MM * MM_PER_S     # 150 px/s
PX_PER_MV = PX_PER_MM * MM_PER_MV   # 60 px/mV
DT = 0.004                      # 샘플 간격(s) → 250 Hz

# 한 심박의 P Q R S T (진폭 mV, 중심 오프셋 s, 폭 s)
WAVES = [
    ("P", 0.12, -0.20, 0.028),
    ("Q", -0.06, -0.028, 0.007),
    ("R", 1.05, 0.0, 0.011),
    ("S", -0.18, 0.030, 0.011),
    ("T", 0.28, 0.30, 0.045),
]


def _beat_value(t: float, tb: float, include_p: bool = True) -> float:
    v = 0.0
    for name, amp, off, w in WAVES:
        if name == "P" and not include_p:
            continue
        v += amp * math.exp(-((t - (tb + off)) ** 2) / (2 * w * w))
    return v


def _beat_times(rhythm: str, rate: float, seconds: float) -> tuple[list[float], bool]:
    """심박 중심 시각 리스트와 P파 포함 여부를 반환."""
    rng = random.Random(42)     # 결정론적(시드 고정)
    rr = 60.0 / rate
    include_p = True
    times: list[float] = []
    t = rr * 0.6
    if rhythm == "afib":
        include_p = False       # 심방세동: P파 소실
        while t < seconds:
            times.append(t)
            t += rr * rng.uniform(0.6, 1.4)   # 불규칙 RR
    else:
        while t < seconds:
            times.append(t)
            t += rr
    return times, include_p


def _fibrillatory(t: float) -> float:
    """심방세동 기저의 잔물결(f파) — 작은 불규칙 진동."""
    return (0.03 * math.sin(2 * math.pi * 7.3 * t)
            + 0.02 * math.sin(2 * math.pi * 11.1 * t + 1.3))


def ecg_svg(rhythm: str = "sinus", rate: float = 75.0, seconds: float = 6.0,
            label: str | None = None) -> str:
    w_px = int(seconds * PX_PER_S)
    h_px = int(3.0 * PX_PER_MV)          # 세로 3 mV 창
    mid = h_px / 2
    beats, include_p = _beat_times(rhythm, rate, seconds)

    # 파형 좌표
    pts = []
    t = 0.0
    n = int(seconds / DT)
    for i in range(n + 1):
        t = i * DT
        v = 0.0
        for tb in beats:
            if abs(t - tb) < 0.45:
                v += _beat_value(t, tb, include_p)
        if rhythm == "afib":
            v += _fibrillatory(t)
        x = t * PX_PER_S
        y = mid - v * PX_PER_MV
        pts.append(f"{x:.1f},{y:.1f}")
    poly = " ".join(pts)

    # ECG 방안지 격자(소 1 mm, 대 5 mm)
    minor = PX_PER_MM
    major = PX_PER_MM * 5
    grid = []
    x = 0.0
    while x <= w_px:
        strong = abs(x % major) < 0.5
        grid.append(f'<line x1="{x:.0f}" y1="0" x2="{x:.0f}" y2="{h_px}" '
                    f'class="{"gmaj" if strong else "gmin"}"/>')
        x += minor
    y = 0.0
    while y <= h_px:
        strong = abs(y % major) < 0.5
        grid.append(f'<line x1="0" y1="{y:.0f}" x2="{w_px}" y2="{y:.0f}" '
                    f'class="{"gmaj" if strong else "gmin"}"/>')
        y += minor

    cap = label or f"{rhythm} · {int(rate)} bpm · 25 mm/s · 10 mm/mV"
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w_px} {h_px + 18}" '
        f'width="{w_px}" height="{h_px + 18}" role="img" aria-label="ECG {cap}">'
        '<style>'
        '.bg{fill:#fff}.gmin{stroke:#f4c9c9;stroke-width:0.5}.gmaj{stroke:#e59a9a;stroke-width:1}'
        '.trace{fill:none;stroke:#111;stroke-width:1.6;stroke-linejoin:round;stroke-linecap:round}'
        '.cap{font:11px -apple-system,Segoe UI,sans-serif;fill:#555}'
        '</style>'
        f'<rect class="bg" x="0" y="0" width="{w_px}" height="{h_px}"/>'
        + "".join(grid)
        + f'<polyline class="trace" points="{poly}"/>'
        + f'<text class="cap" x="4" y="{h_px + 13}">{cap}</text>'
        '</svg>'
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rhythm", default="sinus",
                    choices=["sinus", "brady", "tachy", "afib"])
    ap.add_argument("--rate", type=float, default=75.0)
    ap.add_argument("--seconds", type=float, default=6.0)
    ap.add_argument("--label", default=None)
    ap.add_argument("--out", default="ecg.svg")
    a = ap.parse_args()
    svg = ecg_svg(a.rhythm, a.rate, a.seconds, a.label)
    with open(a.out, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"생성: {a.out} ({len(svg)} bytes, rhythm={a.rhythm}, rate={a.rate})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
