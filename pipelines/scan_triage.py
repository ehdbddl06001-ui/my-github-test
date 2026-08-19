#!/usr/bin/env python3
"""scan_triage.py — 스캔 페이지를 **쪽지시험 형태(라벨 블랭크)** 로 자동 변환한다.

쪽지시험이 이 스캔의 라벨을 지운 형태라 실사 문항을 회차당 30~40장까지 늘려야 하는데,
페이지마다 사람이 좌표를 잡으면 그 규모가 안 나온다. 그래서 규칙을 코드로 박는다.

세 갈래로 나눈다 — **가리는 것 / 묻는 것 / 검사**:

1. **가린다(전부)**: 어두운 배경 위의 '가는 밝은 획' = 화면 글자. 손글씨 라벨·자막·
   타이틀·미리보기 썸네일이 모두 여기 걸린다. 답이 새는 곳은 전부 검은 박스로 덮는다.
   과하게 덮어도 답은 안 샌다 — 반대로 덜 덮으면 문항이 통째로 무의미해진다.
2. **묻는다(지시선/▲ 가 달린 것만)**: 라벨이 구조를 가리키는 방식은 둘뿐이다 —
   흰 **지시선**을 긋거나 빨간 **▲** 를 놓거나. 지시선은 글자를 지워도 그대로 남으므로
   그 자리에 번호핀만 얹으면 무엇을 묻는지가 살아난다. ▲ 는 색 마스크로 지워지므로
   핀에서 화살표 끝으로 잇는 선을 그린다. **자막에는 지시선이 없다** → 문항이 안 된다.
   (D015 실측: 자막 3줄·손글씨 2줄 중 지시선이 달린 것은 손글씨 2줄뿐)
3. **검사한다**: 만든 quiz PNG 를 같은 검출기로 다시 훑어 **글자가 남았으면 버린다**.
   5·7회차에서 세 번 연속 '자동 결과에 답이 남은' 사고가 났고, 그때마다 사람이 축소
   대지를 눈으로 봤다가 놓쳤다. 눈 대신 같은 검출기를 쓴다.

사용:
  python pipelines/scan_triage.py --dir uploads-s04                 # 후보 목록
  python pipelines/scan_triage.py --dir uploads-s04 --build --limit 12
  python pipelines/scan_triage.py --dir uploads-s04 --verify        # 결과 재검사
  python pipelines/scan_triage.py --selftest
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PRIV = ROOT / ".private/anatomy/render"

# 영상 프레임의 고정 좌표(폭 1650 렌더 기준)
CROP = [29, 89, 1621, 1085]
TITLE = [45, 150, 545, 275]
BAR_TOP = 960          # 이 아래는 진행바·컨트롤(답이 없다)
MAX_PINS = 6           # 한 장에 이보다 많으면 문항으로 쓰기 번잡하다


def _cv():
    import cv2
    import numpy as np
    return cv2, np


# ---------------------------------------------------------------- 글자 검출
def pen_mask(img, bar_top: int = BAR_TOP):
    """어두운 배경 위의 **가는 밝은 획**만 남긴다.

    표본(카데바)도 밝지만 '넓은 면'이라 15px top-hat 이 죽인다. 그래도 남는 밝은
    결은 `bi < 110`(그 자리의 배경이 어둡다)이 걸러 낸다 — 글자는 검은 여백 위에,
    표본 결은 밝은 조직 위에 있다.
    """
    cv2, np = _cv()
    g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    bg = cv2.medianBlur(g, 61)
    gi, bi = g.astype(np.int16), bg.astype(np.int16)
    th = cv2.morphologyEx(g, cv2.MORPH_TOPHAT,
                          cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15)))
    m = ((th > 28) & (gi - bi > 48) & (gi > 150) & (bi < 110)).astype(np.uint8)
    m[bar_top:, :] = 0
    return m


def caption_mask(img, bar_top: int = BAR_TOP):
    """**밝은 표본 위에 얹힌 인쇄 캡션**(흰 글자 + 어두운 테두리)만 남긴다.

    `pen_mask` 는 '배경이 어둡다'를 조건으로 써서 검은 여백 위의 손글씨는 잘 잡지만,
    조직 위에 그대로 얹힌 영상 캡션을 통째로 놓친다(D013 실측: '긴발가락굽힘근 힘줄
    (tendon of flexor digitorum longus muscle)' 이 답 그대로 남았다). 캡션은 손글씨보다
    훨씬 밝고(>195) 대비가 세서 배경 밝기와 무관하게 걸린다.
    """
    cv2, np = _cv()
    g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    bg = cv2.medianBlur(g, 61).astype(np.int16)
    th = cv2.morphologyEx(g, cv2.MORPH_TOPHAT,
                          cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (13, 13)))
    m = ((th > 45) & (g.astype(np.int16) - bg > 55) & (g > 195)).astype(np.uint8)
    m[bar_top:, :] = 0
    return cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((2, 2), np.uint8))


def dark_mask(img, bar_top: int = BAR_TOP):
    """표본 위의 **검은 펜 손글씨** — 밝은 조직 위에 얹힌 가는 어두운 획(black-hat)."""
    cv2, np = _cv()
    g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    bg = cv2.medianBlur(g, 61).astype(np.int16)
    bh = cv2.morphologyEx(g, cv2.MORPH_BLACKHAT,
                          cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11)))
    m = ((bh > 34) & (bg - g.astype(np.int16) > 28) & (bg > 110)).astype(np.uint8)
    m[bar_top:, :] = 0
    return cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((2, 2), np.uint8))


def dark_lines(img, bar_top: int = BAR_TOP) -> list[tuple[int, int, int, int]]:
    """손으로 쓴 검은 글씨 줄. **눈·입술 같은 어두운 해부 구조도 섞여** 정밀하지 않다 —
    '얼마나 많은가'를 재는 용도다(많으면 그 페이지는 자동으로 못 만든다)."""
    return _boxes(dark_mask(img, bar_top), 15, 55, 1.4, 500, 4)


def _boxes(mask, kern, wmin, ratio, amin, glyph_min, src=None):
    cv2, np = _cv()
    d = cv2.dilate(mask, np.ones((3, kern), np.uint8))
    d = cv2.dilate(d, np.ones((7, 3), np.uint8))
    n, _, st, _ = cv2.connectedComponentsWithStats(d * 255, 8)
    ref = mask if src is None else src
    out = []
    for i in range(1, n):
        x, y, w, h, a = (st[i, cv2.CC_STAT_LEFT], st[i, cv2.CC_STAT_TOP],
                         st[i, cv2.CC_STAT_WIDTH], st[i, cv2.CC_STAT_HEIGHT],
                         st[i, cv2.CC_STAT_AREA])
        if w < wmin or not (14 <= h <= 110) or w < h * ratio or a < amin:
            continue
        if glyph_min:
            n2, _, st2, _ = cv2.connectedComponentsWithStats(ref[y:y + h, x:x + w] * 255, 8)
            if sum(1 for j in range(1, n2) if st2[j, cv2.CC_STAT_AREA] >= 20) < glyph_min:
                continue
        out.append((int(x), int(y), int(w), int(h)))
    return out


def grow_line(img, box, bar_top: int = BAR_TOP) -> tuple[int, int, int, int]:
    """찾은 글자 줄을 **같은 줄의 흐린 글자까지** 좌우로 늘린다.

    캡션 한 줄이 표본 위로 지나가면 밝은 부분만 검출되고 흐린 꼬리가 남는다
    (F008 실측: '…lis muscle)' 이 그대로 읽혔다). 줄의 위아래 몇 픽셀 띠에서
    획(top-hat)이 이어지는 구간을 따라가면 그 줄 전체가 잡힌다 — 띠 안에서만
    보므로 표본을 통째로 먹지 않는다.
    """
    cv2, np = _cv()
    x, y, w, h = box
    g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    th = cv2.morphologyEx(g, cv2.MORPH_TOPHAT,
                          cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (13, 13)))
    y0, y1 = max(0, y - 4), min(min(bar_top, img.shape[0]), y + h + 4)
    if y1 - y0 < 8:
        return box
    col = (th[y0:y1] > 26).sum(axis=0) >= 4
    # 한쪽으로 200px 까지만 — 밝은 표본(2회차 등근육) 위에서는 조직 결이 이 검사에
    # 걸려 끝없이 이어져, 안 막으면 한 줄이 화면 폭 전체로 자란다(실측: 127 → 886px).
    reach = 200
    left, gap = x, 0
    for i in range(x - 1, max(-1, x - reach), -1):
        if col[i]:
            left, gap = i, 0
        else:
            gap += 1
            if gap > 45:
                break
    right, gap = x + w, 0
    for i in range(x + w, min(img.shape[1], x + w + reach)):
        if col[i]:
            right, gap = i + 1, 0
        else:
            gap += 1
            if gap > 45:
                break
    return (left, y, right - left, h)


def text_lines(img, bar_top: int = BAR_TOP, grow: bool = True) -> list[tuple[int, int, int, int]]:
    """글자 '줄' 단위 박스 — 손글씨(어두운 배경)와 인쇄 캡션(밝은 표본 위)의 합집합."""
    # 획이 3개 이상 모여야 글자다 — 검은 여백에 닿은 표본 가장자리 한 줄기가
    # '글자'로 잡혀 어깨·목이 통째로 검게 덮였다(2회차 A013 실측: 가짜 4줄).
    hand = _boxes(pen_mask(img, bar_top), 21, 45, 1.1, 600, 3)
    # 캡션은 짧은 한글 줄('큰마름근' 4자)도 있어 조건을 너무 죄면 통째로 놓친다
    # (A013 실측: 영문 줄만 잡혀 한글 줄이 그대로 읽혔다).
    cap = _boxes(caption_mask(img, bar_top), 17, 90, 1.8, 700, 3)
    # 두 검출기가 같은 줄을 잡으면 하나로 합친다 — 안 합치면 핀이 두 개 생긴다
    merged: list[list[int]] = []
    for x, y, w, h in sorted(hand + cap, key=lambda b: -b[2] * b[3]):
        for m in merged:
            if (_overlap(x, x + w, m[0], m[0] + m[2]) > 0.5 * min(w, m[2])
                    and _overlap(y, y + h, m[1], m[1] + m[3]) > 0.5 * min(h, m[3])):
                m[2] = max(m[0] + m[2], x + w) - min(m[0], x)
                m[3] = max(m[1] + m[3], y + h) - min(m[1], y)
                m[0], m[1] = min(m[0], x), min(m[1], y)
                break
        else:
            merged.append([x, y, w, h])
    out = [grow_line(img, tuple(m), bar_top) if grow else tuple(m) for m in merged]
    return sorted(out, key=lambda b: (b[1] // 60, b[0]))


def leaders(img, boxes, bar_top: int = BAR_TOP) -> list[tuple[int, int, int, int]]:
    """글자를 뺀 획 마스크에서 **길고 가는 것** = 지시선."""
    cv2, np = _cv()
    m = pen_mask(img, bar_top)
    for x, y, w, h in boxes:
        m[max(0, y - 8):y + h + 8, max(0, x - 8):x + w + 8] = 0
    m = cv2.dilate(m, np.ones((3, 3), np.uint8))
    n, _, st, _ = cv2.connectedComponentsWithStats(m * 255, 8)
    out = []
    for i in range(1, n):
        x, y, w, h, a = (st[i, cv2.CC_STAT_LEFT], st[i, cv2.CC_STAT_TOP],
                         st[i, cv2.CC_STAT_WIDTH], st[i, cv2.CC_STAT_HEIGHT],
                         st[i, cv2.CC_STAT_AREA])
        span = max(int(w), int(h))
        if span >= 70 and a >= 120 and a < span * 12:
            out.append((int(x), int(y), int(w), int(h)))
    return out


def title_band(img, lines) -> list[int]:
    """좌상단 캡션 띠 — 회차·부위 이름이 적혀 답이 새므로 통째로 덮는다.

    고정 `TITLE` 만으로는 긴 제목의 끝이 삐져나온다(D015 실측: 오른쪽으로 90px).
    검은 배경 위 밝은 픽셀의 실제 범위를 재서 그만큼 넓힌다.
    """
    # 캡션은 **항상 좌상단**이다. 오른쪽까지 열어 두면 표본의 밝은 결이 끌려 들어와
    # 화면 위쪽이 통째로 검게 덮인다(2회차 A013 실측: x 39~968 이 한 박스가 됐다).
    hits = [b for b in lines if b[1] < 290 and b[0] < 380]
    if not hits:
        return list(TITLE)
    # **밝은 픽셀 전체**로 재면 안 된다 — 표본이 화면을 가득 채우는 회차(2회차 등근육)
    # 에서는 그 덩어리째 검은 박스가 돼 화면 위쪽이 통째로 날아간다(실측).
    # 글자로 검출된 줄만 감싼다.
    return [min(TITLE[0], min(b[0] for b in hits) - 14),
            min(TITLE[1], min(b[1] for b in hits) - 12),
            max(TITLE[2], max(b[0] + b[2] for b in hits) + 16),
            max(TITLE[3], max(b[1] + b[3] for b in hits) + 14)]


def looks_like_text(img, box, bar_top: int = BAR_TOP) -> bool:
    """줄 박스 안에 **글자 낱낱**이 여러 개 있는가 — 표본의 밝은 결 하나와 구별한다."""
    cv2, np = _cv()
    x, y, w, h = box
    m = (pen_mask(img, bar_top) | caption_mask(img, bar_top))[y:y + h, x:x + w]
    n, _, st, _ = cv2.connectedComponentsWithStats(m * 255, 8)
    return sum(1 for i in range(1, n) if st[i, cv2.CC_STAT_AREA] >= 25) >= 3


def find_arrows(img) -> list[tuple[int, int, int, int]]:
    """빨간 ▲ 마커들. 진행바의 빨간 눈금은 제외한다."""
    cv2, np = _cv()
    b, g, r = cv2.split(img.astype(np.int16))
    m = (((r > 140) & (g < 95) & (b < 95)).astype(np.uint8)) * 255
    m[BAR_TOP:, :] = 0
    m[:, :60] = 0
    n, _, st, _ = cv2.connectedComponentsWithStats(m, 8)
    out = []
    for i in range(1, n):
        x, y, w, h, a = (st[i, cv2.CC_STAT_LEFT], st[i, cv2.CC_STAT_TOP],
                         st[i, cv2.CC_STAT_WIDTH], st[i, cv2.CC_STAT_HEIGHT],
                         st[i, cv2.CC_STAT_AREA])
        if a > 90 and 8 < w < 70 and 8 < h < 70:
            out.append((int(x), int(y), int(w), int(h)))
    return out


# ---------------------------------------------------------------- 묶기·잇기
_BANDS: dict[str, list[int] | None] = {}


def subtitle_band(render_dir: str, sample: int = 24) -> list[int] | None:
    """이 영상의 **자막 띠**(모든 페이지에서 같은 높이)를 여러 장에서 재서 정한다.

    자막은 답을 그대로 적어 놓아 반드시 가려야 하는데, 밝은 표본 위에 얹힌 페이지는
    대비가 낮아 글자 검출이 놓친다(D016 실측 — '뒤정강근 힘줄' 자막이 그대로 남았다).
    한 영상 안에서 자막 높이는 고정이므로, 검출이 잘 된 페이지들에서 띠를 재 두고
    **모든 페이지에 통째로** 덮으면 그 구멍이 막힌다.
    """
    if render_dir in _BANDS:
        return _BANDS[render_dir]
    cv2, np = _cv()
    hits = np.zeros(1200, np.int32)
    pages = 0
    for p in sorted((PRIV / render_dir / "src").glob("*.png"))[:sample]:
        img = cv2.imread(str(p))
        if img is None:
            continue
        pages += 1
        rows = np.zeros(1200, np.int32)
        for x, y, w, h in text_lines(img):
            # 오른쪽 끝의 미리보기 썸네일은 자막이 아니다 — 넣으면 띠가 진행바까지
            # 늘어나 표본 아랫부분을 통째로 덮는다(D015 실측).
            if w >= 150 and y > 500 and 250 <= x + w // 2 <= 1350:
                rows[y:y + h] = 1        # 페이지당 한 번만 센다
        hits += rows
    band = None
    if pages >= 4:
        # 자막은 **거의 모든 페이지에서 같은 줄**을 차지한다 — 그 줄만 띠로 잡는다.
        # 백분위로 잡으면 한 장짜리 손글씨까지 빨려 들어가 화면 1/3이 검게 덮인다(실측).
        on = np.where(hits >= max(3, int(pages * 0.45)))[0]
        if on.size:
            top, bot = int(on.min()) - 34, int(on.max()) + 22
            # 아래쪽 1/3 의 얄팍한 띠여야 자막이다. 라벨이 빽빽한 아틀라스형 페이지
            # 묶음(5회차 실측: 한 장에 19줄)은 화면 한복판을 띠로 잡아 표본을 덮는다.
            if top >= 640 and bot - top <= 170:
                band = [0, top, 1650, bot]
    _BANDS[render_dir] = band
    return band


def _overlap(a0, a1, b0, b1) -> int:
    return min(a1, b1) - max(a0, b0)


def group_lines(boxes) -> list[list[tuple[int, int, int, int]]]:
    """세로로 붙은 줄을 한 라벨로 묶는다(한글 줄 + 그 아래 영문 줄)."""
    groups: list[list] = []
    for b in boxes:
        x, y, w, h = b
        for g in groups:
            gx0 = min(p[0] for p in g)
            gx1 = max(p[0] + p[2] for p in g)
            gy1 = max(p[1] + p[3] for p in g)
            if 0 <= y - gy1 <= 26 and _overlap(x, x + w, gx0, gx1) > 0.3 * min(w, gx1 - gx0):
                g.append(b)
                break
        else:
            groups.append([b])
    return groups


def bbox(group) -> list[int]:
    return [min(p[0] for p in group), min(p[1] for p in group),
            max(p[0] + p[2] for p in group), max(p[1] + p[3] for p in group)]


TISSUE_BG = 96          # 이 밝기보다 밝으면 '표본 위'로 본다
MIN_RUN = 26            # 이보다 좁은 조각은 이웃에 합친다


def split_by_bg(img, box, bar_top: int = BAR_TOP) -> list[tuple[list[int], bool]]:
    """가림 박스를 **밑에 무엇이 있는지**로 잘라 (조각, 표본위냐) 로 돌려준다.

    라벨이 표본 위에 얹혀 있으면 검은 박스로 덮는 순간 **물어볼 구조까지 사라진다**
    (사용자 지적, 2026-08-19). 그런 자리는 주변 조직과 앞뒤 프레임을 보고 **복원**해야
    하고, 검은 여백 위의 글자만 검은 박스로 덮으면 된다. 한 라벨이 조직에서 시작해
    여백으로 넘어가는 일이 흔하므로 **박스를 세로로 쪼개** 구간별로 정한다.
    """
    cv2, np = _cv()
    x0, y0, x1, y1 = [int(v) for v in box]
    x0, y0 = max(0, x0), max(0, y0)
    x1, y1 = min(img.shape[1], x1), min(min(bar_top, img.shape[0]), y1)
    if x1 - x0 < 8 or y1 - y0 < 6:
        return [([x0, y0, x1, y1], False)]
    g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 글자 자체(밝은 획)에 휘둘리지 않게 큰 커널 중앙값으로 '바탕'만 본다
    bg = cv2.medianBlur(g, 61)[y0:y1, x0:x1]
    tissue = np.median(bg, axis=0) > TISSUE_BG
    runs: list[list] = []
    for i, t in enumerate(tissue):
        if runs and runs[-1][2] == bool(t):
            runs[-1][1] = i + 1
        else:
            runs.append([i, i + 1, bool(t)])
    # 자잘한 구간은 이웃에 흡수 — 조각이 잘게 나면 경계마다 이음매가 보인다
    merged: list[list] = []
    for r in runs:
        if merged and (r[1] - r[0] < MIN_RUN or merged[-1][2] == r[2]):
            merged[-1][1] = r[1]
        else:
            merged.append(r)
    return [([x0 + a, y0, x0 + b, y1], t) for a, b, t in merged]


def pick_donor(render_dir: str, page: str, span: int = 3) -> str | None:
    """앞뒤 페이지 중 **같은 장면**을 고른다 — 복원에 쓸 진짜 조직 질감의 출처.

    같은 영상의 이웃 캡처는 카메라 구도가 거의 같아, 지운 자리에 옆 프레임의 조직을
    그대로 옮겨 붙일 수 있다(확산 인페인팅보다 훨씬 자연스럽다). 장면이 바뀌면 오히려
    엉뚱한 걸 붙이므로 **전체 밝기 차이가 작은 것만** 쓴다.
    """
    cv2, np = _cv()
    src = PRIV / render_dir / "src"
    cur = cv2.imread(str(src / f"{page}.png"))
    if cur is None:
        return None
    pages = sorted(p.stem for p in src.glob("*.png"))
    if page not in pages:
        return None
    i = pages.index(page)
    small = cv2.resize(cv2.cvtColor(cur, cv2.COLOR_BGR2GRAY), (160, 110))
    best, score = None, 1e9
    for j in range(max(0, i - span), min(len(pages), i + span + 1)):
        if j == i:
            continue
        other = cv2.imread(str(src / f"{pages[j]}.png"))
        if other is None:
            continue
        d = float(np.abs(small.astype(np.int16)
                         - cv2.resize(cv2.cvtColor(other, cv2.COLOR_BGR2GRAY),
                                      (160, 110)).astype(np.int16)).mean())
        if d < score:
            best, score = pages[j], d
    # 12 이상이면 다른 장면이다(실측: 같은 shot 은 3~8)
    return str((src / f"{best}.png").relative_to(ROOT)) if best and score < 12 else None


def grow_block(img, box, bar_top: int = BAR_TOP) -> list[int]:
    """라벨 덩어리를 **위아래로** 늘려 못 찾은 이웃 줄까지 감싼다.

    캡션은 보통 한글 줄 + 영문 줄 두 줄인데, 표본 위에서는 한 줄만 잡히는 일이 잦다
    (A013 실측: 영문 줄만 잡혀 '큰마름근'이 그대로 읽혔다). 잡힌 줄과 **같은 가로
    범위**에서 획이 이어지는 행을 따라가면 놓친 줄이 딸려 온다.
    """
    cv2, np = _cv()
    x0, y0, x1, y1 = [int(v) for v in box]
    g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    th = cv2.morphologyEx(g, cv2.MORPH_TOPHAT,
                          cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (13, 13)))
    xa, xb = max(0, x0), min(img.shape[1], x1)
    if xb - xa < 30:
        return [x0, y0, x1, y1]
    rows = (th[:, xa:xb] > 26).sum(axis=1)
    need = max(8, int(0.06 * (xb - xa)))
    top, gap = y0, 0
    for i in range(y0 - 1, max(-1, y0 - 80), -1):
        if rows[i] >= need:
            top, gap = i, 0
        else:
            gap += 1
            if gap > 16:
                break
    bot, gap = y1, 0
    for i in range(y1, min(min(bar_top, img.shape[0]), y1 + 80)):
        if rows[i] >= need:
            bot, gap = i + 1, 0
        else:
            gap += 1
            if gap > 16:
                break
    return [x0, top - 6, x1, bot + 6]


def _far_end(box, lead) -> tuple[int, int]:
    """지시선의 **라벨에서 먼 쪽 끝** — 실제로 가리키는 자리."""
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    lx, ly, lw, lh = lead
    corners = [(lx, ly), (lx + lw, ly), (lx, ly + lh), (lx + lw, ly + lh)]
    return max(corners, key=lambda p: (p[0] - cx) ** 2 + (p[1] - cy) ** 2)


def _inside(pt, box, pad: int = 0) -> bool:
    return (box[0] - pad <= pt[0] <= box[2] + pad
            and box[1] - pad <= pt[1] <= box[3] + pad)


def _near(box, other, pad: int) -> bool:
    x0, y0, x1, y1 = box
    ox, oy, ow, oh = other
    return (_overlap(x0 - pad, x1 + pad, ox, ox + ow) > 0
            and _overlap(y0 - pad, y1 + pad, oy, oy + oh) > 0)


def plan(path: Path, band: list[int] | None = None) -> dict:
    """페이지 하나의 가림 박스·핀을 정한다. ok=False 면 후보에서 뺀다."""
    cv2, _ = _cv()
    img = cv2.imread(str(path))
    if img is None:
        return {"page": path.stem, "ok": False, "why": "읽기 실패"}
    lines = text_lines(img)
    if not lines:
        return {"page": path.stem, "ok": False, "why": "화면 글자가 없다 — 라벨 페이지가 아니다"}
    # 표본 위에 손으로 답을 빼곡히 적어 둔 페이지(4회차 F009·F022 실측: 8~9줄)는
    # 다 지우려면 얼굴을 통째로 덮어야 한다 → 자동 대상에서 뺀다. 몇 줄뿐이면
    # 검은 박스가 아니라 **획만 지우는** stroke_boxes 로 넘겨 조직을 살린다.
    dark = dark_lines(img)
    # 눈·입술 같은 어두운 해부 구조도 이 검출기에 걸려 깨끗한 얼굴 페이지도 2줄쯤
    # 나온다(실측: F004·F007 = 2). 그래서 '기준선보다 확실히 많은' 쪽만 걷어낸다.
    if len(dark) > 3:
        return {"page": path.stem, "ok": False,
                "why": f"표본 위 손글씨가 {len(dark)}줄 — 지우면 표본이 남지 않는다"}
    leads = leaders(img, lines)
    arrows = find_arrows(img)
    groups = group_lines(lines)

    title = title_band(img, lines)
    masks, lead_pins, arrow_pins = [], [], []
    if band:
        masks.append(list(band))
    for g in groups:
        box = bbox(g)
        masks.append([box[0] - 10, box[1] - 8, box[2] + 12, box[3] + 10])
        if box[1] < title[3] and box[0] < title[2]:
            continue                                     # 좌상단 캡션 — title_box 담당
        if band and box[1] >= band[1] - 6 and box[3] <= band[3] + 6:
            continue                                     # 자막 띠 — 가리기만, 문항 아님
        lead = next((L for L in leads if _near(box, L, 26)), None)
        if lead is not None:
            # 지시선은 글자를 지워도 남는다 → 라벨 자리에 번호만 얹으면 된다
            lead_pins.append((box, {"x": min(1590, box[0] + 34),
                                    "y": (box[1] + box[3]) // 2},
                              _far_end(box, lead)))
            continue
        arw = next((a for a in arrows if _near(box, a, 90)), None)
        if arw is not None:
            ax, ay, aw, ah = arw                         # ▲ 는 지워지므로 선을 그어 준다
            tgt = (ax + aw // 2, ay + ah // 2)
            arrow_pins.append((box, {"x": max(80, box[0] - 120),
                                     "y": max(60, box[1] - 40), "to": list(tgt)}, tgt))

    # 지시선 라벨이 있으면 ▲ 는 그 라벨을 되짚는 자막 옆 표식일 뿐이다(D015 실측:
    # ▲ 옆 인쇄 자막이 손글씨 라벨과 같은 구조를 가리켜 핀이 두 배로 늘었다).
    pins = lead_pins or arrow_pins
    # **가리킨 자리가 검은 박스 안이면 문항이 안 된다.** 캡션이 구조 위에 바로 얹힌
    # 페이지(7회차 다수)는 답을 지우려면 그 구조까지 덮게 돼, 남는 건 검은 구멍을
    # 가리키는 핀뿐이다 — 그런 페이지는 자동 대상에서 뺀다.
    # ▲ 자리를 비우려고 **가림 박스를 잘라내면 그만큼 글자가 남는다**(A013 실측:
    # 캡션 왼쪽 277px 이 통째로 노출됐다). 이제 조직 위 조각은 검게 덮지 않고 복원하므로
    # 자를 필요가 없다 — 아래에서 **검게 남는 조각에만** 여유를 준다.
    # 가장자리에 딱 붙어도 핀 선이 검은 박스로 빨려 들어가 무엇을 묻는지 사라진다
    # (2회차 A044·A045·A046 실측) → 여유 30px 을 두고 본다.
    # 복원(label_boxes)될 자리는 조직이 남으므로 핀이 가리켜도 된다 — 검게 덮이는
    # 조각만 따진다. split_by_bg 로 나눈 결과는 아래에서 만들므로 여기서 미리 본다.
    dark_pieces = [pc for m in masks for pc, on_t in split_by_bg(img, m) if not on_t]
    for _b, _p, tgt in arrow_pins:          # 검은 조각만 ▲ 앞에서 끊는다
        for m in dark_pieces:
            if not _inside(tgt, m, 40):
                continue
            if tgt[0] - m[0] < m[2] - tgt[0]:
                m[0] = min(m[2] - 40, tgt[0] + 40)
            else:
                m[2] = max(m[0] + 40, tgt[0] - 40)
    buried = [p for p in pins if any(_inside(p[2], m, 30) for m in dark_pieces)]
    if buried:
        return {"page": path.stem, "ok": False,
                "why": f"가리킨 자리가 가림 박스 안이다({len(buried)}개) — 캡션이 구조 위에 얹혔다"}
    if not pins:
        return {"page": path.stem, "ok": False,
                "why": f"지시선·▲ 가 달린 라벨이 없다(글자 {len(lines)}줄은 자막·타이틀)"}
    if len(pins) > MAX_PINS:
        return {"page": path.stem, "ok": False, "why": f"라벨 {len(pins)}개 — 한 장에 너무 많다"}
    pins.sort(key=lambda t: (t[0][1] // 60, t[0][0]))
    for i, (_, p, _t) in enumerate(pins, 1):
        p["n"] = i
    # **밑에 표본이 있는 조각은 검게 덮지 않고 복원한다**(label_boxes). 검은 여백 위
    # 글자만 검은 박스로 남긴다 — 그래야 물어볼 구조가 화면에 남는다.
    paint = [pc for m in masks for pc, on_t in split_by_bg(img, m) if on_t]
    black = dark_pieces
    if band:                       # 자막 띠는 화면 UI 다 — 복원할 구조가 없다
        paint = [pc for pc in paint if not (pc[1] >= band[1] - 8 and pc[3] <= band[3] + 8)]
        black = [pc for pc in black if not (pc[1] >= band[1] - 8 and pc[3] <= band[3] + 8)]
        black.append(list(band))
    return {"page": path.stem, "ok": True, "masks": black, "paint": paint,
            "title": title,
            "strokes": [[x, y, x + w, y + h] for x, y, w, h in dark],
            "pins": [p for _, p, _t in pins], "lines": len(lines)}


def config_for(p: dict, donor: str | None = None) -> dict:
    cfg = {"crop": CROP, "title_box": p.get("title", list(TITLE)),
           "colors": {"red": True},
           "stroke_drop": 26, "stroke_pad": 3,
           "stroke_boxes": p.get("strokes", []),
           "black_boxes": p["masks"],
           # 표본 위 글자는 **검게 덮지 않고 지워서 되살린다** — donor(앞뒤 프레임) →
           # 점진 인페인팅 → 질감 매칭. 획만 지우는 방식도 해 봤지만 테두리를 두른
           # 인쇄 캡션은 글자가 그대로 읽혀(A013 '큰마름근' 실측) 답이 샜다.
           "label_boxes": p.get("paint", []),
           "pins": p["pins"]}
    if donor:
        cfg["donor"] = donor
        # donor 프레임에도 같은 자막이 떠 있으면 그 글자를 그대로 복사해 온다 →
        # donor 쪽 글자 자리는 쓰지 않는다.
        cfg["donor_bad_boxes"] = p.get("donor_bad", [])
    return cfg


# ---------------------------------------------------------------- 검사
def box_has_text(quiz_img, box, pad: int = 6) -> bool:
    """복원한 자리에 **글자가 남았는가** — 자르기 전 좌표 박스를 quiz 이미지에서 본다."""
    cv2, np = _cv()
    x0 = max(0, box[0] - CROP[0] - pad); y0 = max(0, box[1] - CROP[1] - pad)
    x1 = min(quiz_img.shape[1], box[2] - CROP[0] + pad)
    y1 = min(quiz_img.shape[0], box[3] - CROP[1] + pad)
    if x1 - x0 < 20 or y1 - y0 < 10:
        return False
    sub = quiz_img[y0:y1, x0:x1]
    bar = max(10, BAR_TOP - CROP[1] - y0)
    m = pen_mask(sub, bar) | caption_mask(sub, bar)
    n, _, st, _ = cv2.connectedComponentsWithStats(m * 255, 8)
    # 글자 크기 조각이 여러 개 모여 있으면 글자가 남은 것이다
    return sum(1 for i in range(1, n) if 18 <= st[i, cv2.CC_STAT_AREA] <= 900) >= 4


def verify(quiz: Path) -> list[tuple[int, int, int, int]]:
    """만들어진 quiz PNG 에 **글자가 남았는지** 같은 검출기로 다시 본다.

    quiz 는 이미 잘린 이미지라 좌표계가 다르다 — 진행바 경계도 그만큼 올린다.
    번호핀(노랑)은 우리가 그린 것이니 제외한다.
    """
    cv2, np = _cv()
    img = cv2.imread(str(quiz))
    if img is None:
        return [(0, 0, 0, 0)]
    bar = BAR_TOP - CROP[1]
    pin = (np.abs(img.astype(np.int16) - np.array([8, 179, 234])).sum(axis=2) < 90)
    pin = cv2.dilate(pin.astype(np.uint8), np.ones((41, 41), np.uint8))
    work = img.copy()
    work[pin > 0] = 0
    # 가릴 때는 넉넉히(과해도 답은 안 샌다), 검사할 때는 **글자다운 것만** 센다 —
    # 안 그러면 핀셋·표본의 밝은 반사 하나에도 멀쩡한 페이지가 탈락한다(실측).
    # 검사에서는 줄 늘리기를 끈다 — 늘린 박스는 표본의 결까지 '한 줄'처럼 만들어
    # 멀쩡한 페이지를 흠집낸다(P015 실측). 가릴 때만 넉넉히, 볼 때는 있는 그대로.
    return [b for b in text_lines(work, bar_top=bar, grow=False)
            if looks_like_text(work, b, bar)]


# ---------------------------------------------------------------- 실행
def rejects_path(render_dir: str) -> Path:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import restore_store
    return restore_store.STORE / render_dir / "_rejected.json"


def rejected(render_dir: str) -> dict:
    p = rejects_path(render_dir)
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}


def reject(render_dir: str, pages: list[str], why: str) -> int:
    """사람이 눈으로 보고 **못 쓴다고 판정한 페이지**를 기록하고 결과물을 지운다.

    기록해 두지 않으면 다음 `--build` 가 같은 페이지를 똑같이 다시 만든다.
    자동 검사가 못 잡는 것(표본 결에 섞인 흐린 캡션, 손글씨)이 여기 남는다.
    """
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import restore_store
    cur = rejected(render_dir)
    for page in pages:
        cur[page] = why
        for suf in ("_quiz.png", "_clean.png"):
            (PRIV / render_dir / f"{page}{suf}").unlink(missing_ok=True)
        restore_store.store_path(render_dir, page).unlink(missing_ok=True)
    out = rejects_path(render_dir)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(cur, ensure_ascii=False, indent=1, sort_keys=True),
                   encoding="utf-8")
    print(f"{len(pages)}장 제외 기록 · 누적 {len(cur)}장 — {out.relative_to(ROOT)}")
    return 0


def triage(render_dir: str) -> list[dict]:
    src = PRIV / render_dir / "src"
    if not src.exists():
        raise SystemExit(f"원본 렌더가 없다: {src}")
    done = {p.stem[:-5] for p in (PRIV / render_dir).glob("*_quiz.png")} | set(rejected(render_dir))
    band = subtitle_band(render_dir)
    rows = []
    for p in sorted(src.glob("*.png")):
        r = plan(p, band)
        r["done"] = r["page"] in done
        rows.append(r)
    return rows


def build(render_dir: str, limit: int, dry: bool) -> int:
    """자동가능 페이지를 복원하고, **검사를 통과한 것만** 남긴다."""
    import subprocess

    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import restore_store

    rows = [r for r in triage(render_dir) if r["ok"] and not r["done"]][:limit]
    made = dropped = 0
    for r in rows:
        page = r["page"]
        src = PRIV / render_dir / "src" / f"{page}.png"
        donor = pick_donor(render_dir, page)
        if donor:
            import cv2 as _cv2
            dimg = _cv2.imread(str(ROOT / donor))
            # donor 프레임에도 같은 자막이 떠 있다 — 그 글자 자리는 가져오지 않는다
            r["donor_bad"] = [[x - 14, y - 12, x + w + 14, y + h + 12]
                              for x, y, w, h in text_lines(dimg)] if dimg is not None else []
        cfg = config_for(r, donor)
        rec = {"page": page, "render_dir": render_dir, "render_width": 1650,
               "session": int(render_dir[-2:]) if render_dir[-2:].isdigit() else None,
               "source": {"hint": f"{render_dir} 업로드 스캔", "page_no": None, "pages": None},
               "cfg": cfg}
        if dry:
            print(f"  DRY  {page}  가림 {len(cfg['black_boxes'])} · 핀 {len(cfg['pins'])}")
            made += 1
            continue
        tmp = ROOT / ".private/anatomy/cfg" / f"{render_dir}_{page}.json"
        tmp.parent.mkdir(parents=True, exist_ok=True)
        quiz = PRIV / render_dir / f"{page}_quiz.png"
        clean = PRIV / render_dir / f"{page}_clean.png"
        # 검사에서 남은 글자는 **그대로 가림 목록에 더해 다시 만든다**. 핀셋의 금속
        # 반사처럼 글자가 아닌 것도 섞이지만, 작은 검은 박스라 표본을 해치지 않는다 —
        # 반대로 여기서 그냥 버리면 멀쩡한 페이지가 무더기로 날아간다(실측).
        left: list = []
        for _round in range(4):
            tmp.write_text(json.dumps(cfg, ensure_ascii=False), encoding="utf-8")
            rr = subprocess.run(
                [sys.executable, "pipelines/restore_scan.py", "--image", str(src),
                 "--config", str(tmp), "--out-clean", str(clean), "--out-quiz", str(quiz)],
                cwd=ROOT, capture_output=True, text=True)
            if rr.returncode:
                print(f"  FAIL {page}: {rr.stderr.strip()[-140:]}")
                left = [(0, 0, 0, 0)]
                break
            # 복원한 자리에 글자가 남으면(저대비 캡션) 그 조각만 검게 덮어 답을 막는다
            qimg = _cv()[0].imread(str(quiz))
            stuck = [b for b in cfg.get("label_boxes", [])
                     if qimg is not None and box_has_text(qimg, b)]
            if stuck and _round < 2:
                cfg["label_boxes"] = [b for b in cfg["label_boxes"] if b not in stuck]
                cfg["black_boxes"].extend(stuck)
                print(f"    {page}: 복원해도 글자가 남은 라벨 {len(stuck)}개 → 검은 박스")
                left = [(0, 0, 0, 0)]
                continue
            left = verify(quiz)
            if not left:
                break
            # 진짜 '샌 글자'는 이미 가린 캡션의 꼬리라 기존 박스 곁에 있다. 멀리
            # 떨어진 것은 표본의 결일 확률이 높아, 그것까지 덮으면 화면이 걸레가 된다
            # (2회차 A013 실측: 덧칠 6개가 전부 조직이었다) → 그런 페이지는 버린다.
            near = []
            for x, y, w, h in left:      # quiz 좌표 → 자르기 전 좌표
                box = [x + CROP[0] - 12, y + CROP[1] - 10,
                       x + w + CROP[0] + 12, y + h + CROP[1] + 10]
                if any(_overlap(box[0] - 130, box[2] + 130, m[0], m[2]) > 0
                       and _overlap(box[1] - 90, box[3] + 90, m[1], m[3]) > 0
                       for m in cfg["black_boxes"]):
                    near.append(box)
            if not near:
                break                    # 남은 게 조직뿐 → 아래에서 DROP 된다
            cfg["black_boxes"].extend(near)
        if left:
            print(f"  DROP {page}  가려도 글자가 계속 남는다({len(left)}줄) {left[:2]}")
            quiz.unlink(missing_ok=True)
            clean.unlink(missing_ok=True)
            dropped += 1
            continue
        rec["cfg"] = cfg
        out = restore_store.store_path(render_dir, page)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"  NEW  {page}  가림 {len(cfg['black_boxes'])} · 핀 {len(cfg['pins'])}")
        made += 1
    print(f"{made}장 {'예정' if dry else '복원'} · 검사탈락 {dropped}")
    return 0


def sheets(render_dir: str, prefix: str, per: int = 4, wide: int = 700) -> int:
    """QA 대지 — 만들어진 quiz 를 네 장씩 붙여 사람이 한눈에 본다.

    **줄여서 보면 놓친다**(7회차 실측: 위 520px 만 잘라 본 대지가 남은 필기를 감췄다).
    그래서 잘라내지 않고 페이지 **전체**를 줄여 붙인다.
    """
    cv2, np = _cv()
    ps = sorted((PRIV / render_dir).glob("*_quiz.png"))
    for i in range(0, len(ps), per):
        tiles = []
        for p in ps[i:i + per]:
            im = cv2.imread(str(p))
            im = cv2.resize(im, (wide, int(wide * im.shape[0] / im.shape[1])))
            cv2.putText(im, p.stem[:-5], (8, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0,
                        (0, 255, 255), 2)
            tiles.append(im)
        while len(tiles) < per:
            tiles.append(np.zeros_like(tiles[0]))
        grid = np.vstack([np.hstack(tiles[j:j + 2]) for j in range(0, per, 2)])
        out = f"{prefix}{i // per}.png"
        cv2.imwrite(out, grid)
        print(f"  {out}  ({', '.join(p.stem[:-5] for p in ps[i:i + per])})")
    print(f"{len(ps)}장 → 대지 {-(-len(ps) // per)}장")
    return 0


def verify_dir(render_dir: str) -> int:
    bad = 0
    for q in sorted((PRIV / render_dir).glob("*_quiz.png")):
        left = verify(q)
        if left:
            bad += 1
            print(f"  글자 남음 {q.stem[:-5]}: {len(left)}줄 {left[:3]}")
    print(f"{render_dir}: 검사 통과 {len(list((PRIV / render_dir).glob('*_quiz.png'))) - bad} · 실패 {bad}")
    return 1 if bad else 0


def selftest() -> int:
    cv2, np = _cv()
    img = np.zeros((1171, 1650, 3), np.uint8)
    cv2.circle(img, (700, 600), 240, (185, 180, 175), -1)         # 표본(넓은 밝은 면)
    # 지시선이 달린 라벨 → 문항이 된다
    cv2.putText(img, "posterior tibial artery", (1000, 430),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)
    cv2.line(img, (1030, 450), (930, 570), (255, 255, 255), 3)
    # 지시선이 없는 자막 → 가리기만
    cv2.putText(img, "tibial nerve runs behind", (600, 830),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)
    tmp = Path("/tmp/_triage.png")
    cv2.imwrite(str(tmp), img)
    p = plan(tmp)
    assert p["ok"], p
    assert len(p["pins"]) == 1, p          # 자막은 문항이 되지 않는다
    assert len(p["masks"]) >= 2, p         # 그래도 자막은 가린다
    # 표본만 있는 페이지는 후보가 아니다
    plain = np.zeros((1171, 1650, 3), np.uint8)
    cv2.circle(plain, (700, 600), 240, (185, 180, 175), -1)
    cv2.imwrite(str(tmp), plain)
    assert not plan(tmp)["ok"]
    # 검사기: 글자가 그대로면 잡아낸다
    assert verify(tmp) == []
    cv2.imwrite(str(tmp), img[CROP[1]:CROP[3], CROP[0]:CROP[2]])
    assert verify(tmp), "글자가 남았는데 통과시켰다"
    print("[ OK ] scan_triage selftest")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir")
    ap.add_argument("--json")
    ap.add_argument("--build", action="store_true")
    ap.add_argument("--verify", action="store_true")
    ap.add_argument("--reject", help="사람이 보고 뺀 페이지들, 쉼표로 구분")
    ap.add_argument("--why", default="사람 QA: 글자가 남거나 표본이 덮였다")
    ap.add_argument("--sheet", help="QA 대지(contact sheet) 저장 경로 prefix")
    ap.add_argument("--limit", type=int, default=100)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not a.dir:
        print("--dir uploads-sNN 이 필요하다")
        return 2
    if a.reject:
        return reject(a.dir, [s.strip() for s in a.reject.split(",") if s.strip()], a.why)
    if a.sheet:
        return sheets(a.dir, a.sheet)
    if a.verify:
        return verify_dir(a.dir)
    if a.build:
        return build(a.dir, a.limit, a.dry_run)
    rows = triage(a.dir)
    auto = [r for r in rows if r["ok"]]
    new = [r for r in auto if not r["done"]]
    for r in rows:
        tail = ("(복원됨)" if r["done"] else
                (f"핀 {len(r['pins'])} · 가림 {len(r['masks'])}" if r["ok"] else r["why"]))
        print(f"  {'AUTO' if r['ok'] else '  - '} {r['page']}  {tail}")
    print(f"\n{a.dir}: 전체 {len(rows)} · 자동가능 {len(auto)} · 아직 안 만든 것 {len(new)}")
    if a.json:
        Path(a.json).write_text(json.dumps(rows, ensure_ascii=False, indent=1),
                                encoding="utf-8")
        print(f"저장: {a.json}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
