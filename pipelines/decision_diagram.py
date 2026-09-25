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
# 2026-09-25 다시 짬(사용자: 「선이 겹치고 너무 길어져 보기 불편하다」). 옛 배치는 두 층 이상 건너뛰는 선을
# 오른쪽 바깥 통로로 돌리고, 같은 틈의 가로선을 같은 높이에 두어 선이 겹쳤다(77개 도식에 겹침 45·교차 276).
# 라벨은 도착 노드 위에 두 줄로 엇갈려 쌓느라 층 사이가 길어졌다. 지금은 층 배치(Sugiyama) 순서를 따른다:
#   ① 층 = 가장 긴 경로  ② 긴 선은 층마다 보이지 않는 경유점(더미)으로 나눠 노드 사이를 곧게 지난다
#   ③ 층 안 순서는 무게중심 쓸기로 교차를 줄이고(가장 적은 배치를 고름)  ④ 가로 위치는 선이 나가는 포트
#   바로 아래에 자식이 오도록 최소제곱(간격 제약)으로 맞춘다  ⑤ 틈마다 가로선이 겹치지 않게 트랙을 나눈다
#   ⑥ 조건 라벨은 판단 노드 바로 아래(갈래가 시작하는 곳)에 둔다 — 「질문 → 답」이 붙어 읽힌다.
# geometry 형식(nodes/edges/points/label)은 그대로라 웹(learn.js)은 고칠 것이 없다.
TRACK = 9              # 한 틈 안 가로선 트랙 간격
DUMMY_GAP = 16         # 긴 선 경유점과 이웃 사이 최소 간격
LABEL_H = 13


def _crossings(upper: list[str], lower: list[str], links: list[tuple[str, str]]) -> int:
    pu = {n: i for i, n in enumerate(upper)}
    pl = {n: i for i, n in enumerate(lower)}
    es = sorted((pu[a], pl[b]) for a, b in links if a in pu and b in pl)
    return sum(1 for i in range(len(es)) for j in range(i + 1, len(es))
               if (es[i][0] - es[j][0]) * (es[i][1] - es[j][1]) < 0)


def _isotonic(target: list[float], weight: list[float]) -> list[float]:
    """y 가 오름차순이어야 할 때 Σw(y−target)² 최소(인접 위반 합치기)."""
    blocks: list[list[float]] = []            # [Σw·t, Σw, 개수]
    for t, w in zip(target, weight):
        blocks.append([t * w, w, 1])
        while len(blocks) > 1 and blocks[-2][0] / blocks[-2][1] > blocks[-1][0] / blocks[-1][1]:
            s2, w2, n2 = blocks.pop()
            blocks[-1][0] += s2; blocks[-1][1] += w2; blocks[-1][2] += n2
    out: list[float] = []
    for s_, w_, n_ in blocks:
        out += [s_ / w_] * int(n_)
    return out


def _span(pc: dict) -> tuple[float, float]:
    return min(pc["x0"], pc["x1"]), max(pc["x0"], pc["x1"])


def _overlap(p: dict, q: dict) -> bool:
    a0, a1 = _span(p); b0, b1 = _span(q)
    return min(a1, b1) - max(a0, b0) > -6


def _cross_cost(p: dict, q: dict) -> int:
    """p 가 q 보다 위 트랙일 때 두 선의 교차 수."""
    c = 0
    q0, q1 = _span(q); p0, p1 = _span(p)
    if q0 < p["x1"] < q1:          # 위 선의 아래쪽 세로선이 아래 선의 가로선을 지난다
        c += 1
    if p0 < q["x0"] < p1:          # 아래 선의 위쪽 세로선이 위 선의 가로선을 지난다
        c += 1
    return c


def _assign_tracks(pieces: list[dict]) -> int:
    """한 틈 안 가로 구간에 트랙 번호(0=맨 위)를 준다. 겹치면 다른 트랙, 위·아래 순서는 교차가 적은 쪽. 트랙 수를 돌려준다."""
    hs = [pc for pc in pieces if abs(pc["x0"] - pc["x1"]) > 1.5]
    for pc in pieces:
        pc["track"] = -1
    above: dict[int, set[int]] = {i: set() for i in range(len(hs))}
    for i in range(len(hs)):
        for j in range(i + 1, len(hs)):
            if _overlap(hs[i], hs[j]):
                if _cross_cost(hs[i], hs[j]) <= _cross_cost(hs[j], hs[i]):
                    above[j].add(i)
                else:
                    above[i].add(j)
    done: dict[int, int] = {}
    left = set(range(len(hs)))
    while left:
        ready = [i for i in left if not (above[i] - set(done))] or sorted(left)[:1]
        i = min(ready, key=lambda i: _span(hs[i])[0])
        left.discard(i)
        t = max([done[a] + 1 for a in above[i] if a in done] or [0])
        while any(done[o] == t and _overlap(hs[i], hs[o]) for o in done):
            t += 1
        done[i] = t
        hs[i]["track"] = t
    return max(done.values()) + 1 if done else 0


def layout(spec: dict, node_w: int = NODE_W, rank_gap: int | str = "auto", col_gap: int = COL_GAP) -> dict:
    """노드 좌표·선 경로·라벨 위치. 웹은 기본 폭(좁은 세로 화면), PDF 는 넓은 노드로 높이를 줄여 같은 그래프를 그린다.
    층 사이 높이는 그 틈에 실제로 필요한 만큼(라벨 + 가로선 트랙)만 둔다. rank_gap 에 수를 주면 그 절반이 최소 높이다."""
    errs = validate(spec)
    if errs:
        raise DiagramError("; ".join(errs))
    nodes = {str(n["id"]): n for n in spec["nodes"]}
    ids = list(nodes)
    edges = list(spec.get("edges", []))
    out: dict[str, list[dict]] = {i: [] for i in ids}
    inc: dict[str, list[dict]] = {i: [] for i in ids}
    for e in edges:
        out[e["from"]].append(e); inc[e["to"]].append(e)
    order = _topo(ids, out)
    rank = {i: 0 for i in ids}
    for n in order:                                # 가장 긴 경로 = 층
        for e in out[n]:
            rank[e["to"]] = max(rank[e["to"]], rank[n] + 1)
    for n in reversed(order):                      # 나가는 선이 더 많은 노드는 자식 바로 위로 내려 긴 선을 줄인다
        if out[n] and len(out[n]) > len(inc[n]) and nodes[n].get("kind") != "start":
            rank[n] = max(rank[n], min(rank[e["to"]] for e in out[n]) - 1)
    nr = max(rank.values()) + 1

    max_em = (node_w - 2 * PAD_X) / FONT
    geo_nodes: dict[str, dict] = {}
    for n in ids:
        lines = wrap(nodes[n]["text"], max_em)
        geo_nodes[n] = dict(id=n, kind=nodes[n]["kind"], kindLabel=KINDS[nodes[n]["kind"]], lines=lines,
                            w=node_w, h=8 + TOP_LINE + LINE_H * len(lines) + 6)

    # 긴 선 → 층마다 경유점(더미). chains[k] = k 번째 선이 지나는 항목(출발 노드·더미…·도착 노드)
    width = {n: float(node_w) for n in ids}
    item_rank = dict(rank)
    chains: list[list[str]] = []
    links: list[tuple[str, str]] = []
    for k, e in enumerate(edges):
        ch = [e["from"]]
        for r in range(rank[e["from"]] + 1, rank[e["to"]]):
            d = f"\u0000{k}:{r}"
            width[d] = 0.0; item_rank[d] = r; ch.append(d)
        ch.append(e["to"])
        chains.append(ch)
        links += list(zip(ch, ch[1:]))
    up: dict[str, list[str]] = {i: [] for i in item_rank}
    down: dict[str, list[str]] = {i: [] for i in item_rank}
    for a, b in links:
        down[a].append(b); up[b].append(a)

    # 층 안 순서: 등장 순(DFS) → 무게중심 위·아래 쓸기, 교차가 가장 적은 배치를 남긴다
    dfs: list[str] = []
    seen: set[str] = set()
    stack = [next(i for i in ids if nodes[i].get("kind") == "start")]
    while stack:
        n = stack.pop()
        if n in seen:
            continue
        seen.add(n); dfs.append(n)
        stack += list(reversed(down[n]))
    dfs += [i for i in item_rank if i not in seen]
    layers = [[i for i in dfs if item_rank[i] == r] for r in range(nr)]

    def total_cross(ls: list[list[str]]) -> int:
        return sum(_crossings(ls[r], ls[r + 1], links) for r in range(nr - 1))
    best, best_c = [list(L) for L in layers], total_cross(layers)
    for it in range(12):
        downward = it % 2 == 0
        for r in (range(1, nr) if downward else range(nr - 2, -1, -1)):
            ref = layers[r - 1] if downward else layers[r + 1]
            nb = up if downward else down
            pos = {n: k for k, n in enumerate(ref)}
            cur = {n: k for k, n in enumerate(layers[r])}

            def bary(n: str) -> float:
                ps = [pos[m] for m in nb[n] if m in pos]
                return sum(ps) / len(ps) if ps else cur[n]
            layers[r].sort(key=lambda n: (bary(n), cur[n]))
        c = total_cross(layers)
        if c < best_c:
            best, best_c = [list(L) for L in layers], c
    layers = best
    pos_in_layer = {n: k for L in layers for k, n in enumerate(L)}

    # 포트: 나가는 선은 아래 변, 들어오는 선은 위 변에 상대 순서대로 고르게(포트에서 선이 엇갈리지 않게)
    def port_off(n: str, other: str, downward: bool) -> float:
        if width[n] == 0:
            return 0.0
        nbrs = sorted(down[n] if downward else up[n], key=lambda m: pos_in_layer[m])
        k = nbrs.index(other)
        return width[n] * ((k + 1) / (len(nbrs) + 1) - 0.5)

    def sep(a: str, b: str) -> float:
        g = col_gap if width[a] and width[b] else DUMMY_GAP
        return (width[a] + width[b]) / 2 + g

    # 가로 위치: 이웃의 포트 바로 위·아래에 오도록 최소제곱(간격 제약). 긴 선(더미)은 무게를 크게 둬 곧게 편다
    x: dict[str, float] = {}
    for L in layers:
        cx = 0.0
        for k, n in enumerate(L):
            cx = cx + (sep(L[k - 1], n) if k else width[n] / 2)
            x[n] = cx
    for it in range(16):
        if it >= 8:
            rows, use_up, use_dn = list(range(nr)), True, True
        elif it % 2 == 0:
            rows, use_up, use_dn = list(range(1, nr)), True, False
        else:
            rows, use_up, use_dn = list(range(nr - 2, -1, -1)), False, True
        for r in rows:
            L = layers[r]
            tgt, wts = [], []
            for n in L:
                want, ws = [], []
                for m in (up[n] if use_up else []):
                    want.append(x[m] + port_off(m, n, True) - port_off(n, m, False))
                    ws.append(4.0 if width[m] == 0 or width[n] == 0 else 1.0)
                for m in (down[n] if use_dn else []):
                    want.append(x[m] + port_off(m, n, False) - port_off(n, m, True))
                    ws.append(4.0 if width[m] == 0 or width[n] == 0 else 1.0)
                if want:
                    tgt.append(sum(a * b for a, b in zip(want, ws)) / sum(ws)); wts.append(sum(ws))
                else:
                    tgt.append(x[n]); wts.append(0.25)
            off = [0.0]
            for k in range(1, len(L)):
                off.append(off[-1] + sep(L[k - 1], L[k]))
            ys = _isotonic([t - o for t, o in zip(tgt, off)], wts)
            for k, n in enumerate(L):
                x[n] = ys[k] + off[k]
    left = min(x[n] - width[n] / 2 for n in x)
    for n in x:
        x[n] += MARGIN - left
    right = max(x[n] + width[n] / 2 for n in x)

    # 선 조각: 층 r → r+1 마다 (출발 x, 도착 x)
    metas = []
    for e, ch in zip(edges, chains):
        pieces = [dict(r=item_rank[a], x0=x[a] + port_off(a, b, True), x1=x[b] + port_off(b, a, False))
                  for a, b in zip(ch, ch[1:])]
        metas.append(dict(e=e, chain=ch, pieces=pieces))

    # 라벨: 판단 노드 바로 아래, 갈래가 시작하는 선 위. 옆 라벨과 겹치면 한 칸 아래로 엇갈린다
    labels: dict[int, dict] = {}
    for n in ids:
        ports = sorted(m["pieces"][0]["x0"] for m in metas if m["e"]["from"] == n)
        outs = [k for k, m in enumerate(metas) if m["e"]["from"] == n and str(m["e"].get("label", "") or "").strip()]
        outs.sort(key=lambda k: metas[k]["pieces"][0]["x0"])
        n_left, n_right = x[n] - node_w / 2 + 2, x[n] + node_w / 2 - 2
        mine: list[tuple[int, dict]] = []
        for k in outs:
            text = str(metas[k]["e"]["label"]).strip()
            cx = metas[k]["pieces"][0]["x0"]
            i = ports.index(cx)
            # 라벨은 제 선 위에, 옆 갈래 선을 덮지 않는 칸(이웃 포트 사이) 안에 둔다
            lo = ports[i - 1] + 5 if i > 0 else n_left
            hi = ports[i + 1] - 5 if i + 1 < len(ports) else n_right
            room = max(min(cx - lo, hi - cx) * 2, 40.0) if 0 < i < len(ports) - 1 else max(hi - lo, 40.0)
            llines = wrap(text, max(4.0, (room - 8) / LABEL_FONT))
            if len(llines) > 3:                               # 칸이 너무 좁으면 넓히고 엇갈려 놓는다(글은 자르지 않는다)
                w_ = room
                while len(llines) > 2 and w_ < node_w:
                    w_ += 12
                    llines = wrap(text, max(4.0, (w_ - 8) / LABEL_FONT))
            lw = max(sum(_cw(c) for c in ln) for ln in llines) * LABEL_FONT + 8
            lx = min(max(cx - lw / 2, lo), hi - lw) if lw <= hi - lo else cx - lw / 2
            lx = min(max(lx, cx - lw + 6), cx - 6)            # 제 선은 반드시 라벨 안을 지난다
            mine.append((k, dict(lines=llines, w=round(lw, 1), h=len(llines) * LABEL_H + 4, x=lx, row=0)))
        pitch = max([lab["h"] for _, lab in mine] or [0]) + 3      # 엇갈림 한 칸 = 이 노드의 가장 높은 라벨
        placed: list[dict] = []
        for k, lab in mine:
            while any(p["row"] == lab["row"] and p["x"] < lab["x"] + lab["w"] + 3 and lab["x"] < p["x"] + p["w"] + 3 for p in placed):
                lab["row"] += 1
            lab["dy"] = 4 + lab["row"] * pitch
            placed.append(lab)
            labels[k] = lab
    label_drop = {k: lab["dy"] + lab["h"] for k, lab in labels.items()}   # 노드 아래변 → 라벨 아래

    gap_pieces: dict[int, list[dict]] = {r: [] for r in range(nr)}
    for m in metas:
        for pc in m["pieces"]:
            gap_pieces[pc["r"]].append(pc)
    ntracks = {r: _assign_tracks(ps) for r, ps in gap_pieces.items()}

    # 세로 위치: 틈 = 라벨 영역 + 트랙 + 화살표 자리
    row_top: list[float] = []
    row_h: list[float] = []
    lab_zone: dict[int, float] = {}
    y = float(MARGIN)
    min_gap = 22.0 if rank_gap == "auto" else float(rank_gap) / 2
    for r, L in enumerate(layers):
        real = [n for n in L if n in geo_nodes]
        h = max([geo_nodes[n]["h"] for n in real] or [0])
        if r:
            z = 0.0
            for k, d in label_drop.items():
                src = metas[k]["e"]["from"]
                if rank[src] == r - 1:
                    z = max(z, geo_nodes[src]["h"] + d - row_h[r - 1])
            lab_zone[r - 1] = z
            need = z + 8 + (ntracks[r - 1] - 1) * TRACK + 14 if ntracks[r - 1] else z + 14   # 곧은 선만 있으면 트랙 자리를 두지 않는다
            y += max(need, min_gap)
        row_top.append(y); row_h.append(h)
        for n in real:
            geo_nodes[n]["x"], geo_nodes[n]["y"] = round(x[n] - node_w / 2, 1), round(y, 1)
        y += h
    height = y + MARGIN

    geo_edges = []
    for k, m in enumerate(metas):
        e, ch = m["e"], m["chain"]
        s = geo_nodes[e["from"]]
        pts = [(m["pieces"][0]["x0"], s["y"] + s["h"])]
        for pc, nxt in zip(m["pieces"], ch[1:]):
            r = pc["r"]
            if pc["track"] >= 0:
                ty = row_top[r] + row_h[r] + lab_zone.get(r, 0.0) + 8 + pc["track"] * TRACK
                pts += [(pc["x0"], ty), (pc["x1"], ty)]
            if nxt in geo_nodes:
                pts.append((pc["x1"], geo_nodes[nxt]["y"]))
        clean = [pts[0]]
        for p in pts[1:]:
            if abs(p[0] - clean[-1][0]) < 0.05 and abs(p[1] - clean[-1][1]) < 0.05:
                continue
            if len(clean) >= 2 and ((abs(clean[-2][0] - clean[-1][0]) < 0.05 and abs(clean[-1][0] - p[0]) < 0.05)
                                    or (abs(clean[-2][1] - clean[-1][1]) < 0.05 and abs(clean[-1][1] - p[1]) < 0.05)):
                clean[-1] = p                      # 같은 방향으로 이어지는 꺾임점은 합친다
                continue
            clean.append(p)
        lab = None
        if k in labels:
            L_ = labels[k]
            lab = dict(lines=L_["lines"], w=L_["w"], h=L_["h"], x=round(L_["x"], 1),
                       y=round(s["y"] + s["h"] + L_["dy"], 1))
        geo_edges.append(dict(**{"from": e["from"], "to": e["to"]},
                              points=[[round(a, 1), round(b, 1)] for a, b in clean], label=lab))
    # 라벨이 도식 밖으로 나가지 않게
    lab_l = min([g["label"]["x"] for g in geo_edges if g["label"]] or [float(MARGIN)])
    lab_r = max([g["label"]["x"] + g["label"]["w"] for g in geo_edges if g["label"]] or [0.0])
    shift = max(0.0, MARGIN - lab_l)
    if shift:
        for g in geo_nodes.values():
            g["x"] = round(g["x"] + shift, 1)
        for g in geo_edges:
            g["points"] = [[round(a + shift, 1), b] for a, b in g["points"]]
            if g["label"]:
                g["label"]["x"] = round(g["label"]["x"] + shift, 1)
    total_w = max(right, lab_r) + shift + MARGIN
    return dict(title=str(spec.get("title", "")), w=round(total_w, 1), h=round(height, 1),
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
