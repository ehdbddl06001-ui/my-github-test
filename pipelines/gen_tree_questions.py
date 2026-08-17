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
from branch_tree import answer_key  # noqa: E402

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


def card(key: str, no: int, kind: str, qid: str) -> str:
    spec = SPECS[key]
    keys = answer_key(spec)
    day = sched.SCHEDULE_2026[no - 1]["date"].isoformat()
    foot = " ".join(spec.get("footer", []))
    title = spec["title"]
    ans = " / ".join(keys)
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
subtopic: {title} — 계보 퀴즈판 ({no}회차 {KIND_LABEL[kind]})
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
difficulty: 3
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
    for key, no, kind in targets():
        # 같은 트리로 이미 만든 문항이 있으면 건너뛴다(재실행 안전)
        if any(f"tree-{key}-quiz.svg" in p.read_text(encoding="utf-8")
               for p in QDIR.glob("*.md")):
            print(f"  SKIP {key} (이미 있음)")
            continue
        qid = state.next_id("anatomy")
        print(f"  {'DRY ' if dry else 'NEW '} {qid}  {no}회차 {KIND_LABEL[kind]}  "
              f"핀 {len(answer_key(SPECS[key]))}개")
        if not dry:
            (QDIR / f"{qid}.md").write_text(card(key, no, kind, qid), encoding="utf-8")
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
