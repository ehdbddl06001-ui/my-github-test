"""
branch_tree.py — 신경·동맥의 **분지 계보(트리) 구조도**를 SVG로 찍어낸다.

왜 생성기인가: 회차마다 신경 트리·동맥 트리가 필요한데(1·2·3·6회차만 해도 8장),
손으로 그리면 스타일이 갈리고 가지 하나 추가할 때마다 좌표를 다시 잡아야 한다.
`branch_specs.py` 의 중첩 dict 하나만 고치면 라벨판·퀴즈판이 같이 갱신되도록 한다.
(CLAUDE.md: 결정론은 pipelines 가 맡는다 — LLM 이 좌표를 손으로 세지 않는다.)

구도: 뿌리가 왼쪽, 가지가 오른쪽으로 뻗는 가로 트리. 잎을 세로로 쌓고 부모는
자식들의 세로 중앙에 놓는다(겹침이 원리적으로 생기지 않는 배치).

사용:
  python pipelines/branch_tree.py --all          # 전 스펙 → docs/assets/anatomy/
  python pipelines/branch_tree.py --key s06-nerve --out /tmp/a.svg
  python pipelines/branch_tree.py --selftest
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "docs" / "assets" / "anatomy"

BG = "#0e1826"
INK = "#e6edf3"
MUTED = "#93a4b7"
DIM = "#6f8299"
LINE = "#2b3a4d"

# 종류별 색 — 도해 lane 전체가 쓰는 규약(신경 파랑 / 동맥 빨강 / 정맥 보라)과 같다.
PALETTE = {
    "nerve":  {"fg": "#9cc3ff", "fill": "#1d3552", "edge": "#4a6483", "sub": "#7f9cc4"},
    "artery": {"fg": "#e0645f", "fill": "#40201f", "edge": "#7a3a38", "sub": "#c98a86"},
    "vein":   {"fg": "#b49ae0", "fill": "#2c2542", "edge": "#584a76", "sub": "#8f79b8"},
    "mixed":  {"fg": "#7fd4a8", "fill": "#24402f", "edge": "#3f7a5e", "sub": "#5fae87"},
}
STAR = "#eab308"

COLW = [206, 200, 196, 186]      # 깊이별 열 너비
GAP_Y = 9                        # 형제 사이 세로 여백
PAD_X = 26
HEAD_H = 92                      # 제목 영역
FOOT_PAD = 16
FS = {"kr": 12.0, "en": 9.0, "note": 9.0}   # 줄 종류별 글자 크기


def _cw(ch: str, size: float) -> float:
    """글자 하나의 폭 근사. 한글·CJK는 전각(1.0em), ASCII 는 0.52em.

    한 줄에 한글과 영문이 섞이므로 '글자 수' 로 세면 한글 줄이 상자 밖으로 넘친다
    (실측: note 줄이 통째로 삐져나옴) → 글자별로 더한다.
    """
    o = ord(ch)
    wide = (0x1100 <= o <= 0x11FF or 0x2E80 <= o <= 0xA4CF or 0xAC00 <= o <= 0xD7A3
            or 0xF900 <= o <= 0xFAFF or 0xFF00 <= o <= 0xFF60)
    return size * (1.0 if wide else 0.52)


def _textw(s: str, size: float) -> float:
    return sum(_cw(c, size) for c in s)


def _wrap(text: str, width_px: float, size: str = "kr") -> list[str]:
    """폭(px)에 맞춰 줄바꿈. 한글은 공백이 드물어 글자 단위로도 쪼갠다."""
    if not text:
        return []
    fs = FS.get(size, 9.0)
    out, cur = [], ""
    # 폭 계산에는 강조 마커를 빼고 센다(찍히지 않는 문자)
    _w = lambda t: _textw(t.replace("**", ""), fs)
    for tok in text.split(" "):
        cand = (cur + " " + tok).strip()
        if _w(cand) <= width_px:
            cur = cand
            continue
        if cur:
            out.append(cur); cur = ""
        while _w(tok) > width_px:              # 긴 한글 토큰은 글자 단위로
            cut = ""
            for ch in tok:
                if _w(cut + ch) > width_px:
                    break
                cut += ch
            out.append(cut); tok = tok[len(cut):]
        cur = tok
    if cur:
        out.append(cur)
    return out


def _node_lines(node: dict, w: float) -> tuple[list[str], list[str], list[str]]:
    inner = w - 20
    kr = _wrap(node.get("kr", ""), inner, "kr")
    en = _wrap(node.get("en", ""), inner, "en")
    note = _wrap(node.get("note", ""), inner, "note")
    return kr, en, note


def _node_h(node: dict, w: float) -> float:
    kr, en, note = _node_lines(node, w)
    h = 10 + 15 * len(kr) + 11 * len(en) + 11 * len(note) + 8
    return max(38.0, h)


def layout(node: dict, depth: int, y: float, acc: list) -> float:
    """자식을 먼저 쌓고 부모를 그 중앙에 놓는다. 반환값은 이 서브트리의 아래끝 y."""
    w = COLW[min(depth, len(COLW) - 1)] - 26
    h = _node_h(node, w)
    kids = node.get("children") or []
    if not kids:
        acc.append({"node": node, "depth": depth, "x": _col_x(depth), "y": y, "w": w, "h": h})
        return y + h
    cy = y
    centers = []
    for k in kids:
        end = layout(k, depth + 1, cy, acc)
        centers.append((cy + end - GAP_Y) / 2 if end > cy else cy)
        cy = end + GAP_Y
    cy -= GAP_Y
    mid = (centers[0] + centers[-1]) / 2
    top = max(y, mid - h / 2)
    acc.append({"node": node, "depth": depth, "x": _col_x(depth), "y": top, "w": w, "h": h})
    return max(cy, top + h)


def _col_x(depth: int) -> float:
    return PAD_X + sum(COLW[min(d, len(COLW) - 1)] for d in range(depth))


def _esc(s: str) -> str:
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def _rich(text: str, base: str) -> str:
    """`**강조**` 를 밝은 tspan 으로 바꾼다 — 안 하면 별표가 글자로 찍힌다."""
    out, bold = [], False
    for part in text.split("**"):
        if part:
            out.append(f'<tspan fill="{INK}" font-weight="700">{_esc(part)}</tspan>'
                       if bold else _esc(part))
        bold = not bold
    return "".join(out)


def _pal(node: dict, default: str) -> dict:
    """노드가 kind 를 따로 가지면 그 색을 쓴다 — 한 장에 동맥·정맥·신경을 섞기 위함."""
    return PALETTE.get(node.get("kind", default), PALETTE["nerve"])


def answer_key(spec: dict) -> list[str]:
    """퀴즈판 번호핀 1..N 에 대응하는 이름 목록. render(quiz=True) 와 **같은 순서**다.

    번호는 `sorted(boxes, key=(depth, y))` 로 결정되므로 사람이 세면 안 되고
    여기서 받아 써야 한다(문항 생성기가 이 함수를 쓴다).
    """
    return [f"{i}. {n}" for i, n in enumerate(_key_names(spec), 1)]


def _key_names(spec: dict) -> list[str]:
    acc: list[dict] = []
    layout(spec["root"], 0, HEAD_H, acc)
    return [b["node"].get("kr", "") for b in sorted(acc, key=lambda b: (b["depth"], b["y"]))]


def render(spec: dict, quiz: bool = False) -> str:
    kind = spec.get("kind", "nerve")
    pal = PALETTE.get(kind, PALETTE["nerve"])
    boxes: list = []
    bottom = layout(spec["root"], 0, HEAD_H, boxes)
    # 부모→자식 연결선을 위해 좌표 색인
    pos = {id(b["node"]): b for b in boxes}
    width = PAD_X * 2 + sum(COLW[min(d, len(COLW) - 1)]
                            for d in range(_max_depth(spec["root"]) + 1))
    foot = spec.get("footer", [])
    height = bottom + FOOT_PAD + 18 * len(foot) + 22

    o: list[str] = []
    o.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {int(width)} {int(height)}" '
             f'font-family="\'Apple SD Gothic Neo\',\'Noto Sans KR\',sans-serif" role="img" '
             f'aria-label="{_esc(spec["title"])} — 분지 계보 구조도{" 퀴즈판" if quiz else ""}">')
    o.append(f"  <!-- 자동 생성: pipelines/branch_tree.py (스펙: branch_specs.py). 손으로 고치지 말 것.\n"
             f"       근거: {_esc(spec.get('source', ''))} -->")
    o.append('  <style>text{paint-order:stroke;stroke:#0e1826;stroke-width:3px;'
             'stroke-linejoin:round}.kr{font-weight:700}.pin{stroke:none}</style>')
    o.append(f'  <rect width="{int(width)}" height="{int(height)}" fill="{BG}"/>')
    t2 = " — 분지 퀴즈판" if quiz else ""
    o.append(f'  <text x="{PAD_X}" y="30" fill="{INK}" font-size="17" font-weight="700">'
             f'{_esc(spec["title"])}{t2}'
             f'<tspan fill="{MUTED}" font-size="11.5" font-weight="400"> {_esc(spec.get("en", ""))}</tspan></text>')
    o.append(f'  <text x="{PAD_X}" y="50" fill="{MUTED}" font-size="10.5">{_esc(spec.get("subtitle", ""))}</text>')
    if spec.get("legend_kinds"):
        parts = []
        for kk, lab in (("artery", "동맥"), ("vein", "정맥"), ("nerve", "신경")):
            if kk in spec["legend_kinds"]:
                parts.append(f'<tspan fill="{PALETTE[kk]["fg"]}">■ {lab}</tspan>')
        tail = ("번호를 보고 이름을 답하시오" if quiz
                else "★ = tagging 최다 빈출 · 굵은 테두리 = 종말가지")
        o.append(f'  <text x="{PAD_X}" y="68" fill="{DIM}" font-size="10">'
                 + "  ".join(parts) + f'  · {tail}</text>')
    else:
        legend = ("번호를 보고 이름을 답하시오 · 정답은 대응 문항 카드 frontmatter"
                  if quiz else "★ = tagging 최다 빈출 · 굵은 테두리 = 종말가지")
        o.append(f'  <text x="{PAD_X}" y="68" fill="{DIM}" font-size="10">{_esc(legend)}</text>')

    # 연결선(부모 오른쪽 → 자식 왼쪽, 엘보)
    for b in boxes:
        for k in (b["node"].get("children") or []):
            c = pos[id(k)]
            x1, y1 = b["x"] + b["w"], b["y"] + b["h"] / 2
            x2, y2 = c["x"], c["y"] + c["h"] / 2
            mx = (x1 + x2) / 2
            o.append(f'  <path d="M {x1:.0f},{y1:.0f} H {mx:.0f} V {y2:.0f} H {x2:.0f}" '
                     f'fill="none" stroke="{_pal(k, kind)["edge"]}" stroke-width="1.6"/>')

    n = 0
    answers: list[str] = []
    for b in sorted(boxes, key=lambda b: (b["depth"], b["y"])):
        node, x, y, w, h = b["node"], b["x"], b["y"], b["w"], b["h"]
        term = bool(node.get("terminal"))
        np_ = _pal(node, kind)
        sw = 2.2 if term else 1.3
        o.append(f'  <rect x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" height="{h:.0f}" rx="7" '
                 f'fill="{np_["fill"]}" stroke="{np_["fg"] if term or b["depth"]==0 else np_["edge"]}" '
                 f'stroke-width="{sw}"/>')
        if quiz:
            n += 1
            answers.append(f'{n}. {node.get("kr","")}')
            cx, cy = x + w / 2, y + h / 2
            o.append(f'  <circle cx="{cx:.0f}" cy="{cy:.0f}" r="14" fill="{STAR}" '
                     f'stroke="{BG}" stroke-width="2"/>')
            o.append(f'  <text x="{cx:.0f}" y="{cy+5:.0f}" fill="#241a05" font-size="15" '
                     f'font-weight="700" text-anchor="middle" class="pin">{n}</text>')
            continue
        kr, en, note = _node_lines(node, w)
        ty = y + 20
        star = " ★" if node.get("star") else ""
        for i, ln in enumerate(kr):
            o.append(f'  <text x="{x+10:.0f}" y="{ty:.0f}" fill="{np_["fg"]}" font-size="12" '
                     f'class="kr">{_rich(ln, np_["fg"])}{star if i == len(kr)-1 else ""}</text>')
            ty += 15
        for ln in en:
            o.append(f'  <text x="{x+10:.0f}" y="{ty:.0f}" fill="{np_["sub"]}" font-size="9">{_rich(ln, np_["sub"])}</text>')
            ty += 11
        for ln in note:
            o.append(f'  <text x="{x+10:.0f}" y="{ty:.0f}" fill="{DIM}" font-size="9">{_rich(ln, DIM)}</text>')
            ty += 11

    fy = bottom + FOOT_PAD + 6
    if foot:
        o.append(f'  <line x1="{PAD_X}" y1="{fy-12:.0f}" x2="{width-PAD_X:.0f}" y2="{fy-12:.0f}" '
                 f'stroke="{LINE}" stroke-width="1"/>')
    for ln in foot:
        o.append(f'  <text x="{PAD_X}" y="{fy:.0f}" fill="{MUTED}" font-size="10.5">{_rich(ln, MUTED)}</text>')
        fy += 18
    o.append("</svg>")
    return "\n".join(o) + "\n"


def _max_depth(node: dict, d: int = 0) -> int:
    kids = node.get("children") or []
    return d if not kids else max(_max_depth(k, d + 1) for k in kids)


def build(key: str, spec: dict, out_dir: Path = OUT_DIR) -> list[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    made = []
    for quiz in (False, True):
        p = out_dir / f"tree-{key}-{'quiz' if quiz else 'labeled'}.svg"
        p.write_text(render(spec, quiz=quiz), encoding="utf-8")
        made.append(p)
    return made


def _mix_root() -> dict:
    return {"kr": "통로", "children": [
        {"kr": "동맥", "kind": "artery"}, {"kr": "정맥", "kind": "vein"},
        {"kr": "신경", "kind": "nerve"}]}


def selftest() -> int:
    spec = {
        "title": "테스트 트리", "en": "test", "subtitle": "sub", "kind": "artery",
        "source": "selftest",
        "footer": ["한 줄 정리"],
        "root": {"kr": "뿌리동맥", "en": "root a.", "children": [
            {"kr": "가지1", "en": "br 1", "note": "메모가 길어서 줄바꿈이 필요한 경우를 확인한다", "star": True},
            {"kr": "가지2", "en": "br 2", "children": [
                {"kr": "손자1", "terminal": True}, {"kr": "손자2", "terminal": True}]},
        ]},
    }
    svg = render(spec)
    assert svg.startswith("<svg") and svg.rstrip().endswith("</svg>")
    boxes: list = []
    layout(spec["root"], 0, HEAD_H, boxes)
    assert len(boxes) == 5, f"노드 수 {len(boxes)}"
    # 같은 열 안에서 상자가 겹치면 안 된다(배치 원리 회귀)
    for d in {b["depth"] for b in boxes}:
        col = sorted([b for b in boxes if b["depth"] == d], key=lambda b: b["y"])
        for a, b in zip(col, col[1:]):
            assert a["y"] + a["h"] <= b["y"] + 0.01, f"깊이 {d} 상자 겹침"
    # 부모는 자식들의 세로 범위 안에 있어야 한다
    root = [b for b in boxes if b["depth"] == 0][0]
    kids = [b for b in boxes if b["depth"] == 1]
    assert min(k["y"] for k in kids) - 1 <= root["y"] + root["h"] / 2 <= max(k["y"] + k["h"] for k in kids) + 1
    mixed = {"title": "혼합", "kind": "artery", "legend_kinds": ["artery", "vein", "nerve"],
             "root": _mix_root()}
    ms = render(mixed)
    for kk in ("artery", "vein", "nerve"):
        assert PALETTE[kk]["fill"] in ms, f"{kk} 색이 안 쓰임 — 노드별 kind 미적용"
    b2 = render({"title": "강조", "kind": "nerve",
                 "root": {"kr": "가", "note": "여기가 **핵심** 이다"}})
    assert "**" not in b2, "강조 마커가 글자로 찍힘"
    assert 'font-weight="700"' in b2
    q = render(spec, quiz=True)
    assert 'class="pin"' in q and "뿌리동맥" not in q, "퀴즈판에 정답이 남음"
    print("[ OK ] branch_tree selftest")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--key"); ap.add_argument("--out")
    ap.add_argument("--answers", help="퀴즈판 번호→이름 정답표를 출력할 스펙 키")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if a.answers:
        from branch_specs import SPECS as _S
        for ln in answer_key(_S[a.answers]):
            print(ln)
        return 0
    from branch_specs import SPECS
    if a.all:
        made = set()
        for k, s in SPECS.items():
            for p in build(k, s):
                made.add(p.name)
                print(f"생성: {p.relative_to(ROOT)}")
        # 스펙 키를 바꾸면(예: s01-artery → s01-vessel) 예전 파일이 남아 갤러리에
        # 유령 항목으로 뜬다(실측 2026-08-16) → 생성물이 아닌 tree-*.svg 는 지운다.
        for old in sorted(OUT_DIR.glob("tree-*.svg")):
            if old.name not in made:
                old.unlink()
                print(f"삭제(스펙 없음): {old.relative_to(ROOT)}")
        return 0
    if not a.key:
        print("--all 또는 --key 필요"); return 2
    spec = SPECS[a.key]
    if a.out:
        Path(a.out).write_text(render(spec), encoding="utf-8"); print(f"생성: {a.out}")
    else:
        for p in build(a.key, spec):
            print(f"생성: {p.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).parent))
    sys.exit(main())
