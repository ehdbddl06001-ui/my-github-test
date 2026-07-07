"""
gen_ecg_svg.py — 결정론적 ECG 리듬 스트립 SVG 생성기.

MedKOS '자료' 전략 中 B안: 파형은 AI 이미지가 아니라 **수식 기반으로 결정론 생성**한다.
라이선스 문제가 없고 리듬/심박수를 코드로 통제하므로 정답이 항상 파형과 일치한다.
X선·CT·조직 같은 photorealistic 영상, 그리고 '모양(ST/복합체)·12유도'로 정의되는
진단(브루가다·STEMI 등)은 범위 밖 — 이 생성기는 **리듬·간격·무질서**형만 다룬다.

모델: P파(심방)와 QRST(심실)를 **독립 이벤트**로 배치하고, 각 이벤트를 가우시안 합으로
합성한다. 여기에 리듬별 기저(심방세동 f파·조동 톱니·심실세동 무질서)를 더한다.
표준 스케일: 25 mm/s(가로), 10 mm/mV(세로), ECG 방안지(1 mm/5 mm 격자).

지원 rhythm:
  sinus(정상), brady(서맥), tachy(동성빈맥), afib(심방세동),
  flutter(심방조동), vtach(심실빈맥), vfib(심실세동), cavb(완전방실차단), asystole(무수축)

사용:
  python pipelines/gen_ecg_svg.py --rhythm vfib --out vfib.svg
  python pipelines/gen_ecg_svg.py --rhythm cavb --seconds 6 --out cavb.svg
"""
from __future__ import annotations

import argparse
import math
import random

# ── 스케일 ────────────────────────────────────────────────
PX_PER_MM = 6.0
MM_PER_S = 25.0
MM_PER_MV = 10.0
PX_PER_S = PX_PER_MM * MM_PER_S     # 150 px/s
PX_PER_MV = PX_PER_MM * MM_PER_MV   # 60 px/mV
DT = 0.004                          # 250 Hz 샘플

# ── 파형 형태: (진폭 mV, 이벤트 기준 오프셋 s, 폭 s) ─────────
P_MORPH = [(0.12, 0.0, 0.028)]
QRST_NARROW = [
    (-0.06, -0.028, 0.007), (1.05, 0.0, 0.011),
    (-0.18, 0.030, 0.011), (0.28, 0.30, 0.045),
]
# 심실 기원(넓은 QRS + 불일치 T) — VT·심실 escape 용
QRST_WIDE = [(1.00, 0.0, 0.040), (-0.45, 0.22, 0.070)]

DEFAULT_RATE = {
    "sinus": 75, "brady": 45, "tachy": 120, "afib": 110, "flutter": 150,
    "vtach": 160, "vfib": 0, "cavb": 40, "asystole": 0,
}

_PR = 0.16   # P→QRS 간격(초)


def _g(t: float, c: float, a: float, w: float) -> float:
    return a * math.exp(-((t - c) ** 2) / (2 * w * w))


def _sum_morph(t: float, event: float, morph) -> float:
    return sum(_g(t, event + off, amp, w) for amp, off, w in morph)


def _regular(period: float, seconds: float, start: float) -> list[float]:
    out, t = [], start
    while t < seconds:
        out.append(t)
        t += period
    return out


def _model(rhythm: str, rate: float, seconds: float, rng: random.Random):
    """(심방 이벤트, 심실 이벤트, 심실형태, 기저함수) 를 돌려준다."""
    atrial: list[float] = []
    vent: list[float] = []
    vmorph = QRST_NARROW
    baseline = None

    if rhythm in ("sinus", "brady", "tachy"):
        rr = 60.0 / rate
        atrial = _regular(rr, seconds, rr * 0.5)
        vent = [a + _PR for a in atrial]

    elif rhythm == "afib":
        # P 소실 + RR '불규칙하게 불규칙' + 잔물결(f파)
        rr = 60.0 / rate
        t = rr * 0.6
        while t < seconds:
            vent.append(t)
            t += rr * rng.uniform(0.6, 1.4)
        baseline = lambda tt: 0.03 * math.sin(2 * math.pi * 7.3 * tt) \
            + 0.02 * math.sin(2 * math.pi * 11.1 * tt + 1.3)

    elif rhythm == "flutter":
        # 톱니 F파(~300/분) + 규칙적 심실 전도
        vent = _regular(60.0 / rate, seconds, 0.4)
        ff = 5.0  # 300/min
        baseline = lambda tt: -0.16 * (2 * (ff * tt - math.floor(0.5 + ff * tt)))

    elif rhythm == "vtach":
        # 넓은 QRS, 규칙적, 빠름, P 없음
        vent = _regular(60.0 / rate, seconds, 0.3)
        vmorph = QRST_WIDE

    elif rhythm == "vfib":
        # 조직화 복합체 없음 — 무질서 기저
        comps = [(rng.uniform(4, 9), rng.uniform(0, 2 * math.pi), rng.uniform(0.15, 0.5))
                 for _ in range(5)]
        def _chaos(tt, comps=comps):
            v = sum(a * math.sin(2 * math.pi * f * tt + p) for f, p, a in comps)
            env = 0.7 + 0.3 * math.sin(2 * math.pi * 0.7 * tt + 1.0)  # 진폭 변조
            return v * env
        baseline = _chaos

    elif rhythm == "cavb":
        # 완전방실차단: P(심방 ~90/분)와 QRS(심실 escape)가 독립적으로 행진
        atrial = _regular(60.0 / 90.0, seconds, 0.25)
        vent = _regular(60.0 / (rate or 40), seconds, 0.55)
        vmorph = QRST_WIDE

    elif rhythm == "asystole":
        baseline = lambda tt: 0.012 * math.sin(2 * math.pi * 0.3 * tt)

    return atrial, vent, vmorph, baseline


def ecg_svg(rhythm: str = "sinus", rate: float | None = None,
            seconds: float = 6.0, label: str | None = None) -> str:
    if rate in (None, 0) and DEFAULT_RATE.get(rhythm):
        rate = DEFAULT_RATE[rhythm]
    rate = float(rate or 75)
    rng = random.Random(1234)   # 결정론(시드 고정)

    w_px = int(seconds * PX_PER_S)
    h_px = int(3.0 * PX_PER_MV)
    mid = h_px / 2
    atrial, vent, vmorph, baseline = _model(rhythm, rate, seconds, rng)

    pts = []
    n = int(seconds / DT)
    for i in range(n + 1):
        t = i * DT
        v = 0.0
        for ta in atrial:
            if abs(t - ta) < 0.20:
                v += _sum_morph(t, ta, P_MORPH)
        for tv in vent:
            if abs(t - tv) < 0.45:
                v += _sum_morph(t, tv, vmorph)
        if baseline:
            v += baseline(t)
        pts.append(f"{t * PX_PER_S:.1f},{mid - v * PX_PER_MV:.1f}")
    poly = " ".join(pts)

    minor, major = PX_PER_MM, PX_PER_MM * 5
    grid = []
    x = 0.0
    while x <= w_px:
        cls = "gmaj" if abs(x % major) < 0.5 else "gmin"
        grid.append(f'<line x1="{x:.0f}" y1="0" x2="{x:.0f}" y2="{h_px}" class="{cls}"/>')
        x += minor
    y = 0.0
    while y <= h_px:
        cls = "gmaj" if abs(y % major) < 0.5 else "gmin"
        grid.append(f'<line x1="0" y1="{y:.0f}" x2="{w_px}" y2="{y:.0f}" class="{cls}"/>')
        y += minor

    cap = label or f"{rhythm} · {int(rate)} bpm · 25 mm/s, 10 mm/mV"
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w_px} {h_px + 18}" '
        f'width="{w_px}" height="{h_px + 18}" role="img" aria-label="ECG {cap}">'
        '<style>.bg{fill:#fff}.gmin{stroke:#f4c9c9;stroke-width:0.5}'
        '.gmaj{stroke:#e59a9a;stroke-width:1}'
        '.trace{fill:none;stroke:#111;stroke-width:1.6;stroke-linejoin:round;stroke-linecap:round}'
        '.cap{font:11px -apple-system,Segoe UI,sans-serif;fill:#555}</style>'
        f'<rect class="bg" x="0" y="0" width="{w_px}" height="{h_px}"/>'
        + "".join(grid)
        + f'<polyline class="trace" points="{poly}"/>'
        + f'<text class="cap" x="4" y="{h_px + 13}">{cap}</text></svg>'
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rhythm", default="sinus", choices=list(DEFAULT_RATE.keys()))
    ap.add_argument("--rate", type=float, default=None)
    ap.add_argument("--seconds", type=float, default=6.0)
    ap.add_argument("--label", default=None)
    ap.add_argument("--out", default="ecg.svg")
    a = ap.parse_args()
    svg = ecg_svg(a.rhythm, a.rate, a.seconds, a.label)
    with open(a.out, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"생성: {a.out} ({len(svg)} bytes, rhythm={a.rhythm})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
