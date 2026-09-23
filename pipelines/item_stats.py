"""item_stats.py — 내 풀이 기록으로 문항 난이도·판단 단계·평가 목표를 **묶음 단위로** 보정한다(결정론, 읽기 전용).

2026-09-23 사용자 채택 — 「데이터가 쌓이면 선지와 난이도를 보정한다」.

학습자는 한 명이고 한 문항은 대개 한 번 푼다. 그래서 **문항 하나의 정답률·변별도는 계산하지 않는다**(한 번의 맞고
틀림은 통계가 아니다). 대신
  1. 묶음 정답률 — 첫 풀이만(변형·다시 풀기 제외) 난이도 라벨·판단 단계(design.steps)·평가 목표·시험별로 센다.
     라벨이 실제 정답률을 가르는지(난이도가 높을수록 정답률이 낮은지) 묶음이 충분히 클 때만(MIN_GROUP) 판정한다.
  2. 약한 곳 — 정답률이 낮은 평가 목표·판단 단계. 문항 생성 루틴이 그날 세트의 비중을 정할 때 참고한다
     (구성 목표 question_design.mix_report 는 그대로 지킨다).
  3. 선지 보정 — 내가 고른 오답 보기에 문항의 distractors 설명이 없는 것(concept_queue [dist] 와 같은 기준)과,
     「해설이 이해되지 않았다」 표시가 붙은 문항(해설 손질 대상).
  4. 찍어서 맞힘 — 「찍었다」 표시가 붙은 정답(정답률을 부풀린다 — 따로 센다).
출력은 사람이 읽는 표와 --json. 아무것도 쓰지 않는다(상태는 기록에서 늘 다시 계산).

  python pipelines/item_stats.py              # 표
  python pipelines/item_stats.py --brief      # 루틴용 세 줄 요약
  python pipelines/item_stats.py --json
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import learning_log as ll
from concepts import load_questions

MIN_GROUP = 20        # 이보다 적은 묶음은 정답률을 보여 주되 판정하지 않는다
GAP = 0.10            # 인접 난이도 묶음의 정답률이 이만큼 뒤집히면 「라벨이 가르지 못한다」


def first_attempts(events: list[dict]) -> dict[str, dict]:
    """{문항id: 첫 풀이 사건} — 변형(mode variant)은 빼고 덱에서 처음 푼 것만."""
    out: dict[str, dict] = {}
    for e in sorted(events, key=lambda e: (str(e.get("t", "")), e.get("eid", ""))):
        if e.get("kind") == "answer" and e.get("mode") != "variant" and e.get("qid") and e["qid"] not in out:
            out[e["qid"]] = e
    return out


def _group(rows: list[tuple[str, bool]]) -> dict[str, dict]:
    g: dict[str, dict] = {}
    for k, ok in rows:
        r = g.setdefault(k, {"n": 0, "ok": 0})
        r["n"] += 1
        r["ok"] += int(ok)
    for r in g.values():
        r["acc"] = round(r["ok"] / r["n"], 3) if r["n"] else None
    return g


def inversions(g: dict[str, dict], order: list[str]) -> list[str]:
    """order 순서(쉬움 → 어려움)로 인접 묶음이 둘 다 MIN_GROUP 이상인데 어려운 쪽 정답률이 GAP 이상 높으면."""
    out = []
    keys = [k for k in order if k in g and g[k]["n"] >= MIN_GROUP]
    for a, b in zip(keys, keys[1:]):
        if g[b]["acc"] - g[a]["acc"] >= GAP:
            out.append(f"{b} 의 정답률({g[b]['acc']:.0%}, n={g[b]['n']})이 {a}({g[a]['acc']:.0%}, n={g[a]['n']})보다 높다")
    return out


def build(events: list[dict], questions: dict[str, dict]) -> dict:
    first = first_attempts(events)
    rows = {"difficulty": [], "steps": [], "target": [], "exam": []}
    guessed_ok = 0
    flags: dict[str, set[str]] = {}
    for e in events:
        if e.get("kind") == "flag" and e.get("on") and e.get("qid"):
            flags.setdefault(str(e.get("flag")), set()).add(e["qid"])
    for qid, e in first.items():
        q = questions.get(qid) or {}
        d = q.get("design") if isinstance(q.get("design"), dict) else {}
        ok = bool(e.get("ok"))
        rows["difficulty"].append((f"난이도 {q.get('difficulty', '?')}", ok))
        rows["steps"].append((f"{d['steps']}단계" if d.get("steps") else "단계 없음", ok))
        rows["target"].append((str(d.get("target") or "목표 없음"), ok))
        rows["exam"].append((str(e.get("exam") or q.get("type") or "?"), ok))
        if ok and qid in flags.get("guessed", set()):
            guessed_ok += 1
    groups = {k: _group(v) for k, v in rows.items()}
    inv = (inversions(groups["difficulty"], [f"난이도 {i}" for i in range(1, 6)])
           + inversions(groups["steps"], [f"{i}단계" for i in range(1, 5)]))
    weak = sorted(((k, r) for k, r in groups["target"].items() if r["n"] >= 5 and k != "목표 없음"),
                  key=lambda x: x[1]["acc"])[:3]
    n = len(first)
    return {
        "first_attempts": n,
        "accuracy": round(sum(int(bool(e.get("ok"))) for e in first.values()) / n, 3) if n else None,
        "groups": groups,
        "label_inversions": inv,
        "weak_targets": [{"target": k, **r} for k, r in weak],
        "guessed_correct": guessed_ok,
        "not_understood": sorted(flags.get("not_understood", set())),
        "min_group": MIN_GROUP,
    }


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--events", help="학습 기록 파일(기본 state/learning_sync/events.json)")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--brief", action="store_true", help="루틴용 요약 세 줄")
    a = ap.parse_args(argv)
    events = ll.read_events(Path(a.events) if a.events else ll.SYNC_FILE)
    r = build(events, load_questions())
    if a.json:
        print(json.dumps(r, ensure_ascii=False, indent=1))
        return 0
    n = r["first_attempts"]
    acc = f"{r['accuracy']:.0%}" if r["accuracy"] is not None else "-"
    if a.brief:
        weak = ", ".join(f"{w['target']} {w['acc']:.0%}(n={w['n']})" for w in r["weak_targets"]) or "판단할 만큼 쌓이지 않음"
        print(f"첫 풀이 {n}문항 · 정답률 {acc} · 찍어서 맞힘 {r['guessed_correct']}")
        print(f"약한 평가 목표: {weak}")
        print("난이도 라벨: " + ("; ".join(r["label_inversions"]) if r["label_inversions"]
                              else f"뒤집힘 없음(묶음 {MIN_GROUP}문항 이상만 판정)"))
        return 0
    print(f"첫 풀이 {n}문항 · 정답률 {acc} · 「찍었다」 표시한 정답 {r['guessed_correct']}")
    print(f"(학습자 1명 — 문항 하나의 정답률·변별도는 계산하지 않는다. 묶음 {MIN_GROUP}문항 이상에서만 판정)")
    for name, g in r["groups"].items():
        print(f"\n[{name}]")
        for k, v in sorted(g.items()):
            mark = "" if v["n"] >= MIN_GROUP else "  (판정 보류)"
            print(f"  {k:<12} n={v['n']:>4}  정답률 {v['acc']:.0%}{mark}")
    print("\n난이도 라벨 점검: " + ("; ".join(r["label_inversions"]) if r["label_inversions"] else "뒤집힘 없음(또는 판정할 만큼 쌓이지 않음)"))
    if r["not_understood"]:
        print(f"해설이 이해되지 않았다 표시 {len(r['not_understood'])}문항: {', '.join(r['not_understood'][:10])}")
    print("고른 오답 보기의 설명 누락은 concept_queue.py 의 [dist] 를 본다.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
