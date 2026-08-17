#!/usr/bin/env python3
"""gen_tree_questions.py — 분지 계보 트리 **퀴즈판**을 그대로 문항으로 만든다(결정론).

왜: 홈페이지 '회차별 학습'의 문항 대부분이 실사(restored-scan)라 **웹에서는 그림이
안 뜬다**(카데바 파생물은 publishable:false). 그래서 화면에는 '번호핀 ①이 가리키는…'
같은 지문만 남아 그림 없이 읽히고, 정작 볼 수 있는 도해는 문항으로 연결돼 있지 않았다.

트리 퀴즈판은 우리가 직접 그린 SVG라 **공개 가능**하고, 번호핀 1..N 이 결정론이다
(`branch_tree.answer_key()` — 사람이 번호를 세지 않는다). 그 정답표를 그대로 답으로
쓰면 회차마다 '그림이 있는 문항'이 생긴다.

사용:
  python pipelines/gen_tree_questions.py --dry-run
  python pipelines/gen_tree_questions.py
  python pipelines/gen_tree_questions.py --selftest
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import anatomy_schedule as sched  # noqa: E402
import state  # noqa: E402
from branch_specs import SPECS  # noqa: E402
from branch_tree import answer_groups, answer_key  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
QDIR = ROOT / "content/anatomy/questions/tagging-1"
ASSETS = ROOT / "docs/assets/anatomy"

KIND_LABEL = {"nerve": "신경 계보", "vessel": "혈관 계보(동맥+정맥)",
              "bundle": "함께 지나는 것(신경혈관다발)"}
KIND_CLASSES = {"nerve": ["nerve"], "vessel": ["artery", "vein"],
                "bundle": ["artery", "vein", "nerve"]}


def targets() -> list[tuple[str, int, str]]:
    """(스펙키, 회차, 종류) — 퀴즈판 SVG가 실제로 있는 것만."""
    out = []
    for key in sorted(SPECS):
        m = re.fullmatch(r"s(\d\d)-(nerve|vessel|bundle)", key)
        if not m:
            continue
        if not (ASSETS / f"tree-{key}-quiz.svg").exists():
            continue
        out.append((key, int(m.group(1)), m.group(2)))
    return out


MIN_PINS = 3          # 핀 2개짜리 가지는 따로 묻기엔 너무 얕다 → '나머지'로 합친다


def groups_for(key: str) -> list[tuple[str, list[tuple[int, str]]]]:
    """이 트리에서 만들 (문항 제목, 핀 목록) 목록 — 가지별 + 자잘한 것 묶음."""
    big, small = [], []
    for name, pins in answer_groups(SPECS[key]):
        (big if len(pins) >= MIN_PINS else small).append((name, pins))
    if small:
        merged = sorted({p for _, ps in small for p in ps})
        big.append((" · ".join(n for n, _ in small), merged))
    return big


def card(key: str, no: int, kind: str, qid: str,
         group: tuple[str, list[tuple[int, str]]] | None = None) -> str:
    spec = SPECS[key]
    keys = ([f"{i}. {n}" for i, n in group[1]] if group else answer_key(spec))
    day = sched.SCHEDULE_2026[no - 1]["date"].isoformat()
    foot = " ".join(spec.get("footer", []))
    title = spec["title"]
    ans = " / ".join(keys)
    if group:
        nums = ", ".join(str(i) for i, _ in group[1])
        stem = (f"계보 구조도 퀴즈판({title})에서 **{group[0]}** 계통에 해당하는 "
                f"번호핀 {nums} 번이 가리키는 구조의 이름을 번호 순서대로 답하시오.")
    else:
        stem = (f"계보 구조도 퀴즈판({title})에서 번호핀 1~{len(keys)}가 가리키는 "
                f"구조의 이름을 번호 순서대로 답하시오. 위에서 아래로, 왼쪽에서 "
                f"오른쪽 순으로 매겨져 있다.")
    exp = (f"{spec.get('subtitle', '')} {foot} "
           "라벨판(tree-…-labeled.svg)과 짝이므로 퀴즈판을 먼저 풀고 라벨판으로 채점한다. "
           "이 도해는 직접 그린 것이라 웹에 공개된다 — 실사 태깅 문항과 달리 "
           "화면에서 바로 풀 수 있다.")
    return f"""---
id: {qid}
type: anatomy
kind: question
topic: Anatomy
subtopic: {title} — 계보 퀴즈판 ({no}회차 {KIND_LABEL[kind]}{f" · {group[0]}" if group else " · 종합"})
date: 2026-08-17
confidence: high
source: "{spec.get('source', '')} — 자체 제작 계보 트리(branch_specs.py)"
region: multi
subregion: {key}
structure_classes: {KIND_CLASSES[kind]}
question_style: spotter
exam_phase: {'tagging-1' if no <= 8 else 'tagging-2'}
scheduled_dates: [{day}]
priority: high
publishable: true
asset_origin: claude-drawn-svg
web_asset: assets/anatomy/tree-{key}-quiz.svg
needs_review: false
answer_separated: true
difficulty: {2 if group else 3}
gen_key: "tree:{key}:{group[0] if group else '__all__'}"
stem: "{stem}"
answer: "{ans}"
explanation: "{exp}"
source_refs:
  - {{source_file_id: "branch-specs-{key}", source_file_name: "pipelines/branch_specs.py — {key}", page: null, section: "{title}", note: "번호핀 순서는 branch_tree.answer_key() 결정론(상자를 depth·y 순으로 정렬). 사람이 번호를 세지 않는다."}}
tags: [계보, 도해, {no}회차, {KIND_LABEL[kind]}, 예습시험, 태깅]
---

## 문제

계보 구조도 퀴즈판 — 그림은 `docs/assets/anatomy/tree-{key}-quiz.svg`(공개 자산).

## 정답 및 해설

> 정답·해설은 frontmatter. 채점은 라벨판 `tree-{key}-labeled.svg` 로.
"""


def run(dry: bool) -> int:
    QDIR.mkdir(parents=True, exist_ok=True)
    made = 0
    existing = [p.read_text(encoding="utf-8") for p in QDIR.glob("*.md")]
    for key, no, kind in targets():
        wants: list = [None] + groups_for(key)   # None = 전체 종합판
        for g in wants:
            gk = f"tree:{key}:{g[0] if g else '__all__'}"
            # gen_key 로 재실행 안전. 옛 전체판 카드는 gen_key 가 없으므로
            # 그 트리의 퀴즈판을 쓰면서 'gen_key' 가 없는 카드도 전체판으로 친다.
            done = any(gk in t or (g is None and f"tree-{key}-quiz.svg" in t
                                   and "gen_key:" not in t) for t in existing)
            if done:
                continue
            qid = state.next_id("anatomy")
            n = len(g[1]) if g else len(answer_key(SPECS[key]))
            print(f"  {'DRY ' if dry else 'NEW '} {qid}  {no}회차 {KIND_LABEL[kind]}  "
                  f"{g[0] if g else '종합'} (핀 {n})")
            if not dry:
                (QDIR / f"{qid}.md").write_text(card(key, no, kind, qid, g),
                                                encoding="utf-8")
            made += 1
    print(f"{made}문항 {'예정' if dry else '생성'}")
    return 0


def selftest() -> int:
    ts = targets()
    assert ts, "트리 퀴즈판이 하나도 없다"
    key, no, kind = ts[0]
    txt = card(key, no, kind, "anatomy-2026-9999")
    assert "publishable: true" in txt and "claude-drawn-svg" in txt
    assert f"assets/anatomy/tree-{key}-quiz.svg" in txt
    # 정답 개수 = 퀴즈판 핀 개수(결정론) — 사람이 세지 않는다
    import branch_tree
    svg = branch_tree.render(SPECS[key], quiz=True)
    assert svg.count('class="pin"') == len(answer_key(SPECS[key]))
    # 정답이 지문에 새지 않는다
    stem = re.search(r'^stem: "(.+)"$', txt, re.M).group(1)
    first = answer_key(SPECS[key])[0].split(". ", 1)[1]
    assert first not in stem, "정답이 지문에 노출됨"
    # 가지별 분할: 모든 핀이 정확히 한 번씩 덮이고, 번호는 전체 기준을 유지한다
    gs = groups_for(key)
    pins = [i for _, ps in gs for i, _ in ps]
    assert len(pins) == len(set(pins)), f"{key}: 핀이 두 문항에 중복"
    assert set(pins) <= set(range(1, len(answer_key(SPECS[key])) + 1))
    assert all(len(ps) >= MIN_PINS or len(gs) == 1 for _, ps in gs), "너무 얕은 가지 문항"
    print("[ OK ] gen_tree_questions selftest")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    return selftest() if a.selftest else run(a.dry_run)


if __name__ == "__main__":
    sys.exit(main())
