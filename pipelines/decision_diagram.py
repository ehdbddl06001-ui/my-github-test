"""decision_diagram.py — 임상 판단 도식(세로형) 배치·SVG·글 대체본을 결정론으로 만든다.

2026-09-18 사용자 지시(오답 뒤 학습 흐름·과별 PDF 학습서):
- 세로 방향, 분기마다 조건 라벨, 억지 분기 없이. 안정화·선행 단계를 포함한다.
- 「미시행·정보 없음」과 「정상·음성」을 구분하고, 「추가 정보 필요」 경로를 둔다.
- 색만으로 구분하지 않는다 — 모든 노드 윗줄에 종류 글자(판단·처치·추가 정보 필요…)와 사례 표지
  (★ 이 사례 · ◆ 갈림 · ? 정보 없음 · ○ 미시행)를 글자로 적고, 경로 선은 굵기·점선으로도 다르게 그린다.
- 일반 구조 + 이 사례의 경로 + 선택한 오답과 갈리는 지점. 문항에 없는 정보를 채우지 않는다.
- 렌더링이 실패해도 학습이 끊기지 않도록 **같은 그래프에서** 글 대체본을 만든다(도식·글 불일치 방지).

한 번 계산한 배치(geometry)를 웹(app.js 가 createElementNS+textContent 로 그림 — innerHTML 없음)과
PDF(여기서 만든 SVG 문자열)가 함께 쓴다. 그래서 두 화면의 도식이 어긋나지 않는다.

도식 규격(개념 정리본 frontmatter `diagram`):
  title: str
  nodes: [{id, kind, text}]      kind ∈ KINDS
  edges: [{from, to, label}]     판단(decision) 노드에서 나가는 선은 라벨 필수
사례 경로(문항 frontmatter `case_path`):
  visit: [{node, state, note}]   state ∈ STATES — 순서대로 지난 노드
  (선택한 오답과 갈리는 지점은 문항 `distractors.<letter>.split` 이 노드 id 를 가리킨다)
"""
from __future__ import annotations

import html
from typing import Any

KINDS = {
    "start": "시작",
    "step": "평가·처치",
    "decision": "판단",
    "info": "추가 정보 필요",
    "alert": "위험·이 도식 범위 밖",
    "end": "결론",
}
STATES = {
    "path": "★ 이 사례",               # 사례가 지나간 노드(판단 결과는 note 로)
    "normal": "★ 정상·음성 확인",       # 확인했더니 정상/음성 — 「정보 없음」과 다르다
    "abnormal": "★ 이상 소견",
    "unknown": "? 문항에 정보 없음",     # 문항이 말하지 않았다 — 음성으로 채우지 않는다
    "not_done": "○ 미시행",             # 검사를 하지 않았다 — 정상이라는 뜻이 아니다
}
SPLIT_MARK = "◆"

NODE_W = 196
PAD_X = 10
TOP_LINE = 16          # 종류·사례 표지 줄
LINE_H = 17
FONT = 13
LABEL_FONT = 11
RANK_GAP = 66          # 층 사이(갈래 가로선 + 엇갈린 라벨 두 줄 자리)
COL_GAP = 30
LANE_GAP = 14
MARGIN = 16

LIGHT = dict(bg="#ffffff", fg="#1b2430", sub="#4a5566", line="#56657a", path="#0b57d0",
             node="#f5f7fa", decision="#fff6e0", info="#eef3ff", alert="#fdecec", end="#e9f7ef",
             split="#b3261e", label_bg="#ffffff")
DARK = dict(bg="#0e1826", fg="#e6edf5", sub="#a9b6c6", line="#7f8fa6", path="#7cb8ff",
            node="#16212f", decision="#2a2412", info="#141f36", alert="#321417", end="#11281c",
            split="#ff8a80", label_bg="#0e1826")


class DiagramError(ValueError):
    pass


# ── 검증 ───────────────────────────────────────────────────────────
def validate(spec: Any) -> list[str]:
    """도식 규격 오류 목록(빈 목록 = 통과)."""
    if not isinstance(spec, dict):
        return ["diagram 은 사전이어야 한다"]
    errs: list[str] = []
    nodes = spec.get("nodes") or []
    edges = spec.get("edges") or []
    if not isinstance(nodes, list) or not nodes:
        return ["diagram.nodes 가 비어 있다"]
    ids: list[str] = []
    for i, n in enumerate(nodes, 1):
        if not isinstance(n, dict) or not n.get("id") or not str(n.get("text", "")).strip():
            errs.append(f"diagram.nodes[{i}] 는 {{id, kind, text}}")
            continue
        if n.get("kind") not in KINDS:
            errs.append(f"diagram.nodes[{i}] kind '{n.get('kind')}' — {'/'.join(KINDS)} 중에서")
        if n["id"] in ids:
            errs.append(f"diagram 노드 id 중복: {n['id']}")
        ids.append(str(n["id"]))
    idset = set(ids)
    kind = {str(n.get("id")): n.get("kind") for n in nodes if isinstance(n, dict)}
    out: dict[str, list[dict]] = {i: [] for i in ids}
    for j, e in enumerate(edges if isinstance(edges, list) else [], 1):
        if not isinstance(e, dict) or e.get("from") not in idset or e.get("to") not in idset:
            errs.append(f"diagram.edges[{j}] 가 없는 노드를 가리킨다: {e}")
            continue
        out[e["from"]].append(e)
    for nid, es in out.items():
        if kind.get(nid) == "decision":
            if len(es) < 2:
                errs.append(f"판단 노드 '{nid}' 는 갈래가 2개 이상이어야 한다(갈래가 하나면 판단이 아니다)")
            if any(not str(e.get("label", "")).strip() for e in es):
                errs.append(f"판단 노드 '{nid}' 에서 나가는 선에 조건 라벨이 없다")
        if kind.get(nid) in ("end", "alert") and es:
            errs.append(f"'{nid}' ({KINDS[kind[nid]]}) 에서 선이 나간다 — 결론·범위 밖 노드는 끝이어야 한다")
    starts = [i for i in ids if kind.get(i) == "start"]
    if len(starts) != 1:
        errs.append(f"시작 노드(kind: start)는 정확히 1개 — 현재 {len(starts)}개")
    if not any(k == "info" for k in kind.values()):
        errs.append("「추가 정보 필요」 노드(kind: info)가 없다 — 정보가 모자랄 때의 경로를 둔다")
    if errs:
        return errs
    # 순환·도달성
    order = _topo(ids, out)
    if order is None:
        errs.append("diagram 에 순환이 있다 — 판단 도식은 위에서 아래로만 흐른다")
        return errs
    seen = {starts[0]}
    stack = [starts[0]]
    while stack:
        for e in out[stack.pop()]:
            if e["to"] not in seen:
                seen.add(e["to"]); stack.append(e["to"])
    lost = [i for i in ids if i not in seen]
    if lost:
        errs.append(f"시작에서 닿지 않는 노드: {', '.join(lost)}")
    return errs


def validate_case(spec: dict, case: Any, split_nodes: list[str] | None = None) -> list[str]:
    """문항의 사례 경로가 도식과 맞는지. 경로는 선을 따라 이어져야 한다(도식·글 정합성)."""
    errs: list[str] = []
    ids = {str(n["id"]) for n in spec.get("nodes", [])}
    for s in split_nodes or []:
        if s not in ids:
            errs.append(f"갈림 지점 '{s}' 이 도식에 없다")
    if case is None:
        return errs
    visit = (case or {}).get("visit") if isinstance(case, dict) else None
    if not isinstance(visit, list) or not visit:
        return errs + ["case_path.visit 이 비어 있다"]
    edges = {(e["from"], e["to"]) for e in spec.get("edges", [])}
    prev = None
    for i, v in enumerate(visit, 1):
        if not isinstance(v, dict) or v.get("node") not in ids:
            errs.append(f"case_path.visit[{i}] 노드가 도식에 없다: {v}")
            prev = None
            continue
        if v.get("state", "path") not in STATES:
            errs.append(f"case_path.visit[{i}] state '{v.get('state')}' — {'/'.join(STATES)} 중에서")
        if prev and (prev, v["node"]) not in edges:
            errs.append(f"case_path: '{prev}' → '{v['node']}' 로 가는 선이 도식에 없다")
        prev = v["node"]
    return errs


def _topo(ids: list[str], out: dict[str, list[dict]]) -> list[str] | None:
    indeg = {i: 0 for i in ids}
    for es in out.values():
        for e in es:
            indeg[e["to"]] += 1
    q = [i for i in ids if indeg[i] == 0]
    order = []
    while q:
        n = q.pop(0)
        order.append(n)
        for e in out[n]:
            indeg[e["to"]] -= 1
            if indeg[e["to"]] == 0:
                q.append(e["to"])
    return order if len(order) == len(ids) else None


# ── 글 줄바꿈(한글 폭 1, 라틴 0.56) ─────────────────────────────────
def _cw(ch: str) -> float:
    o = ord(ch)
    if o < 0x2E80:
        return 0.34 if ch == " " else 0.58
    return 1.0


def wrap(text: str, max_em: float) -> list[str]:
    out: list[str] = []
    for para in str(text).split("\n"):
        line, w = "", 0.0
        for tok in _tokens(para):
            tw = sum(_cw(c) for c in tok)
            if line and w + tw > max_em:
                out.append(line.rstrip()); line, w = tok.lstrip(), sum(_cw(c) for c in tok.lstrip())
                while w > max_em:                      # 한 토큰이 한 줄보다 길면 글자로 자른다
                    cut, cw = "", 0.0
                    for c in line:
                        if cw + _cw(c) > max_em:
                            break
                        cut += c; cw += _cw(c)
                    out.append(cut); line = line[len(cut):]; w = sum(_cw(c) for c in line)
            else:
                line += tok; w += tw
        out.append(line.rstrip())
    return [x for x in out if x != ""] or [""]


def _tokens(s: str) -> list[str]:
    toks, cur = [], ""
    for c in s:
        cur += c
        if c in " ·/,)":
            toks.append(cur); cur = ""
    if cur:
        toks.append(cur)
    return toks


# ── 배치 ───────────────────────────────────────────────────────────
def layout(spec: dict, node_w: int = NODE_W, rank_gap: int | str = RANK_GAP, col_gap: int = COL_GAP) -> dict:
    """노드 좌표·선 경로·라벨 위치. 웹은 기본 폭(좁은 세로 화면), PDF 는 넓은 노드로 높이를 줄여 같은 그래프를 그린다.
    rank_gap="auto" 이면 층 사이를 그 틈에 실제로 필요한 만큼만 둔다(갈래 가로선 + 엇갈린 라벨 줄 수)."""
    errs = validate(spec)
    if errs:
        raise DiagramError("; ".join(errs))
    nodes = {str(n["id"]): n for n in spec["nodes"]}
    ids = list(nodes)
    out: dict[str, list[dict]] = {i: [] for i in ids}
    inc: dict[str, list[dict]] = {i: [] for i in ids}
    for e in spec.get("edges", []):
        out[e["from"]].append(e); inc[e["to"]].append(e)
    order = _topo(ids, out)
    rank = {i: 0 for i in ids}
    for n in order:                                # 가장 긴 경로 = 층
        for e in out[n]:
            rank[e["to"]] = max(rank[e["to"]], rank[n] + 1)
    nr = max(rank.values()) + 1
    # 층 안 순서: 등장 순(DFS) → 부모 무게중심 두 번
    dfs, seen = [], set()

    def visit(n: str) -> None:
        if n in seen:
            return
        seen.add(n); dfs.append(n)
        for e in out[n]:
            visit(e["to"])
    visit(next(i for i in ids if nodes[i].get("kind") == "start"))
    layers = [[i for i in dfs if rank[i] == r] for r in range(nr)]
    for _ in range(2):
        pos = {n: k for L in layers for k, n in enumerate(L)}
        for r in range(1, nr):
            def bary(n: str) -> float:
                ps = [pos[e["from"]] for e in inc[n]]
                return sum(ps) / len(ps) if ps else pos[n]
            layers[r].sort(key=bary)
    max_em = (node_w - 2 * PAD_X) / FONT
    geo_nodes: dict[str, dict] = {}
    for n in ids:
        lines = wrap(nodes[n]["text"], max_em)
        geo_nodes[n] = dict(id=n, kind=nodes[n]["kind"], kindLabel=KINDS[nodes[n]["kind"]], lines=lines,
                            w=node_w, h=8 + TOP_LINE + LINE_H * len(lines) + 6)
    widest = max(len(L) for L in layers)
    inner_w = widest * node_w + (widest - 1) * col_gap

    def label_h(e: dict, t_w: float) -> int:
        lab = str(e.get("label", "") or "").strip()
        return (len(wrap(lab, max(4.0, t_w * 0.92 / LABEL_FONT))[:2]) * 13 + 4) if lab else 0
    zone: dict[int, int] = {}                     # 층 r 위쪽의 라벨 영역 높이
    gaps: dict[int, float] = {}
    for r in range(1, nr):
        z = 0
        for n in layers[r]:
            hs = [label_h(e, node_w) for e in inc[n] if str(e.get("label", "") or "").strip()]
            if hs:
                z = max(z, (min(2, len(hs))) * (max(hs) + 3) + 3)
        zone[r] = z
        top = max([10 + 6 * (len(out[n]) - 1) for n in layers[r - 1]] or [10])
        gaps[r] = max(top + 8 + z, 30) if rank_gap == "auto" else float(rank_gap)
    y = MARGIN
    for r, L in enumerate(layers):
        if r:
            y += gaps[r]
        row_h = max(geo_nodes[n]["h"] for n in L)
        lw = len(L) * node_w + (len(L) - 1) * col_gap
        x = MARGIN + (inner_w - lw) / 2
        for n in L:
            g = geo_nodes[n]
            g["x"], g["y"] = round(x, 1), round(y, 1)
            x += node_w + col_gap
        y += row_h
    height = y + MARGIN
    # 선: 나가는 포트는 아래 변에, 들어오는 포트는 위 변에 고르게. 두 층 이상 건너뛰면 오른쪽 통로로.
    lane_x = MARGIN + inner_w + LANE_GAP
    geo_edges = []
    for n in ids:
        outs = sorted(out[n], key=lambda e: geo_nodes[e["to"]]["x"])
        for k, e in enumerate(outs):
            s, t = geo_nodes[e["from"]], geo_nodes[e["to"]]
            ins = sorted(inc[e["to"]], key=lambda f: geo_nodes[f["from"]]["x"])
            ki = ins.index(e)
            px = s["x"] + s["w"] * (k + 1) / (len(outs) + 1)
            tx = t["x"] + t["w"] * (ki + 1) / (len(ins) + 1)
            ys, yt = s["y"] + s["h"], t["y"]
            y_out = ys + 10 + 6 * k                   # 같은 노드에서 나가는 갈래는 가로선 높이를 달리한다
            if rank[e["to"]] - rank[e["from"]] > 1:
                y_in = yt - (zone.get(rank[e["to"]], 0) + 6 if rank_gap == "auto" else 46)
                pts = [(px, ys), (px, y_out), (lane_x, y_out), (lane_x, y_in), (tx, y_in), (tx, yt)]
                lane_x += LANE_GAP
            else:
                pts = [(px, ys), (px, y_out), (tx, y_out), (tx, yt)]
            label = str(e.get("label", "") or "").strip()
            lab = None
            if label:
                slot = t["w"] * 0.92
                llines = wrap(label, max(4.0, slot / LABEL_FONT))[:2]
                lw = max(sum(_cw(c) for c in ln) for ln in llines) * LABEL_FONT + 8
                lh = len(llines) * 13 + 4
                # 한 노드로 들어오는 선이 여럿이면 라벨을 위아래로 엇갈려 겹치지 않게 한다
                ly = yt - 3 - lh - (ki % 2) * (lh + 3)
                lab = dict(lines=llines, w=round(lw, 1), h=lh, x=round(tx - lw / 2, 1), y=round(ly, 1))
            geo_edges.append(dict(**{"from": e["from"], "to": e["to"]},
                                  points=[[round(a, 1), round(b, 1)] for a, b in pts], label=lab))
    width = max(lane_x - LANE_GAP + MARGIN, MARGIN * 2 + inner_w)
    return dict(title=str(spec.get("title", "")), w=round(width, 1), h=round(height, 1),
                nodes=[geo_nodes[n] for n in ids], edges=geo_edges)


def overlay(case: dict | None, split: dict[str, list[str]] | None = None) -> dict:
    """사례 경로 표지. split = {노드 id: [보기 글머리…]} — 선택한 오답과 갈리는 지점."""
    visit = (case or {}).get("visit") or []
    states = {str(v["node"]): v.get("state", "path") for v in visit if isinstance(v, dict) and v.get("node")}
    seq = [str(v["node"]) for v in visit if isinstance(v, dict) and v.get("node")]
    return dict(states=states, pathEdges=[[a, b] for a, b in zip(seq, seq[1:])], split=split or {})


def top_line(node: dict, ov: dict | None) -> str:
    parts = [node["kindLabel"]]
    if ov:
        st = ov["states"].get(node["id"])
        if st:
            parts.append(STATES[st])
        if node["id"] in ov["split"]:
            parts.append(f"{SPLIT_MARK} {'·'.join(ov['split'][node['id']])} 보기와 갈림")
    return " · ".join(parts)


# ── SVG(PDF·검수용). 모든 글은 escape — 콘텐츠의 글자가 마크업이 되지 않는다 ──
def to_svg(geo: dict, ov: dict | None = None, theme: dict = LIGHT, title: str | None = None) -> str:
    esc = lambda s: html.escape(str(s), quote=True)
    T = theme
    path_edges = {tuple(p) for p in (ov or {}).get("pathEdges", [])}
    fill = {"decision": T["decision"], "info": T["info"], "alert": T["alert"], "end": T["end"]}
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {geo["w"]} {geo["h"]}" '
           f'width="{geo["w"]}" height="{geo["h"]}" role="img" aria-label="{esc(title or geo["title"])}" '
           f'font-family="NanumGothic, \'Noto Sans KR\', \'Apple SD Gothic Neo\', sans-serif">',
           f'<rect width="100%" height="100%" fill="{T["bg"]}"/>',
           f'<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
           f'<path d="M0,0 L10,5 L0,10 z" fill="{T["line"]}"/></marker>'
           f'<marker id="ahp" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
           f'<path d="M0,0 L10,5 L0,10 z" fill="{T["path"]}"/></marker></defs>']
    for e in geo["edges"]:
        on = (e["from"], e["to"]) in path_edges
        pts = " ".join(f"{x},{y}" for x, y in e["points"])
        style = (f'stroke="{T["path"]}" stroke-width="3.2"' if on
                 else f'stroke="{T["line"]}" stroke-width="1.4" stroke-dasharray="{"0" if not ov else "5 4"}"')
        out.append(f'<polyline points="{pts}" fill="none" {style} marker-end="url(#{"ahp" if on else "ah"})"/>')
    for n in geo["nodes"]:
        st = (ov or {}).get("states", {}).get(n["id"])
        split = n["id"] in (ov or {}).get("split", {})
        rx = 14 if n["kind"] in ("start", "end") else 4
        border = T["split"] if split else (T["path"] if st else T["line"])
        bw = 3 if (split or st) else 1.2
        dash = ' stroke-dasharray="6 3"' if st in ("unknown", "not_done") else ""
        out.append(f'<rect x="{n["x"]}" y="{n["y"]}" width="{n["w"]}" height="{n["h"]}" rx="{rx}" '
                   f'fill="{fill.get(n["kind"], T["node"])}" stroke="{border}" stroke-width="{bw}"{dash}/>')
        tl = top_line(n, ov)
        out.append(f'<text x="{n["x"] + PAD_X}" y="{n["y"] + 5 + 11}" font-size="10" fill="{T["sub"]}" '
                   f'font-weight="{700 if (split or st) else 400}">{esc(tl)}</text>')
        for k, ln in enumerate(n["lines"]):
            out.append(f'<text x="{n["x"] + PAD_X}" y="{n["y"] + 8 + TOP_LINE + LINE_H * k + 13}" font-size="{FONT}" '
                       f'fill="{T["fg"]}" font-weight="{700 if n["kind"] in ("decision", "end") else 400}">{esc(ln)}</text>')
    for e in geo["edges"]:
        lab = e.get("label")
        if not lab:
            continue
        out.append(f'<rect x="{lab["x"]}" y="{lab["y"]}" width="{lab["w"]}" height="{lab["h"]}" rx="3" '
                   f'fill="{T["label_bg"]}" stroke="{T["line"]}" stroke-width="0.6"/>')
        for k, ln in enumerate(lab["lines"]):
            out.append(f'<text x="{lab["x"] + lab["w"] / 2}" y="{lab["y"] + 13 + 13 * k}" font-size="{LABEL_FONT}" '
                       f'text-anchor="middle" fill="{T["fg"]}">{esc(ln)}</text>')
    out.append("</svg>")
    return "".join(out)


# ── 글 대체본(도식과 같은 그래프에서) ────────────────────────────────
def text_steps(spec: dict, case: dict | None = None, split: dict[str, list[str]] | None = None,
               labels: dict[str, str] | None = None) -> list[dict]:
    """[{id, marker, text, branches:[{label, to, toText}], note}] — 위에서 아래 순서."""
    nodes = {str(n["id"]): n for n in spec["nodes"]}
    out: dict[str, list[dict]] = {i: [] for i in nodes}
    for e in spec.get("edges", []):
        out[e["from"]].append(e)
    order = _topo(list(nodes), out) or list(nodes)
    num = {n: k + 1 for k, n in enumerate(order)}
    ov = overlay(case, split)
    notes = {str(v["node"]): str(v.get("note", "") or "") for v in (case or {}).get("visit", []) if isinstance(v, dict)}
    steps = []
    for n in order:
        nd = nodes[n]
        steps.append(dict(
            id=n, num=num[n], kind=KINDS[nd["kind"]], marker=top_line(dict(id=n, kindLabel=KINDS[nd["kind"]]), ov if case or split else None),
            text=str(nd["text"]), note=notes.get(n, ""),
            branches=[dict(label=str(e.get("label", "") or "다음"), to=num[e["to"]], toText=str(nodes[e["to"]]["text"]))
                      for e in out[n]],
        ))
    return steps


def text_alternative(spec: dict, case: dict | None = None, split: dict[str, list[str]] | None = None) -> str:
    """사람이 읽는 글 대체본(평문). PDF·웹 공통."""
    lines = [f"[도식] {spec.get('title', '')}"]
    for s in text_steps(spec, case, split):
        lines.append(f"{s['num']}. ({s['marker']}) {s['text']}" + (f" — 이 사례: {s['note']}" if s["note"] else ""))
        for b in s["branches"]:
            lines.append(f"   · {b['label']} → {b['to']}번")
    return "\n".join(lines)
