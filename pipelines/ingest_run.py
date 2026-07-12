"""
ingest_run.py — '내가 실제로 돌린 실행'의 결과를 repo에 실행 로그 카드(kind: log)로 박는다.

왜 필요한가: 클로드가 낡은 repo 노트북을 보고 "네가 한 것"을 **예측**하면 틀린다(실제로
1주차 심화 카드가 그렇게 절반이 어긋났다). 그래서 실제 코드·수치의 Source of Truth를
repo에 둔다. 노트북이 Drive에 남기는 `result.json`(또는 아래 플래그)에서 **결정론적으로**
로그 카드를 만든다 — 수치를 LLM이 지어내지 않는다(MedKOS 원칙: 결정론은 파이프라인).

result.json 예(노트북 CELL 8이 저장하는 형태):
  {"week":1, "task":"ECG 1D-CNN (MIT-BIH AAMI 5-class)", "split":"intra",
   "macro_f1":0.8273, "passed":true, "date":"2026-07-12"}

사용:
  # (1) 노트북이 남긴 result.json에서 바로
  python pipelines/ingest_run.py --results result.json \
      --notebook notebooks/week01_ecg_1dcnn.ipynb \
      --checkpoint drive:MedKOS/ailab/week01/week01_best.keras

  # (2) 값만 직접(파일 없이)
  python pipelines/ingest_run.py --week 1 --split intra --metric macro_f1 \
      --value 0.8273 --passed --notebook notebooks/week01_ecg_1dcnn.ipynb

멱등성: 같은 (week, split)의 로그가 이미 있으면 새 id를 낭비하지 않고 그 카드를
**갱신**한다(--force-new로 새로 만들 수 있음).
"""
from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path

try:
    from state import next_id, record_topic
    from frontmatter import load
    from datasets import topic_for_week
except ImportError:  # from pipelines.* 로 import 되는 경우
    from pipelines.state import next_id, record_topic
    from pipelines.frontmatter import load
    from pipelines.datasets import topic_for_week

ROOT = Path(__file__).resolve().parent.parent
LOGS_DIR = ROOT / "content" / "ailab" / "logs"

# result.json 안에서 지표로 쓸 수 있는 키(값이 '높을수록 좋음'인 우리 지표들).
KNOWN_METRICS = ("macro_f1", "macro_auroc", "auroc", "dice", "qwk", "f1", "accuracy")


def _metric_value_from_results(data: dict) -> tuple[str | None, float | None]:
    """result.json에서 (지표명, 값)을 뽑는다. {'metric','value'} 우선, 없으면 알려진 키."""
    if data.get("metric") and data.get("value") is not None:
        return str(data["metric"]), float(data["value"])
    for k in KNOWN_METRICS:
        if k in data and data[k] is not None:
            return k, float(data[k])
    return None, None


def find_existing(week: int, split: str, step: str = "") -> Path | None:
    """같은 (week, split, step)의 기존 로그 카드 경로. 없으면 None(멱등 갱신용).

    step은 퀘스트 실험 구분자(같은 week·split이라도 실험이 다르면 다른 로그로 쌓인다).
    """
    if not LOGS_DIR.exists():
        return None
    for p in sorted(LOGS_DIR.glob("*.md")):
        d = load(p)
        if d.errors:
            continue
        m = d.meta
        if m.get("kind") == "log" and str(m.get("week")) == str(week) \
                and str(m.get("split", "")) == str(split) \
                and str(m.get("step", "")) == str(step):
            return p
    return None


def render_card(meta: dict) -> str:
    """로그 카드 Markdown 문자열. 본문은 사람이 읽는 짧은 요약 + 다음 액션."""
    t = topic_for_week(int(meta["week"]))
    gate = ""
    if t.get("target") is not None:
        gate = f" (게이트 {t['metric']} ≥ {t['target']})"
    passed = "✅ 통과" if meta.get("passed") else "❌ 미달"
    split = meta.get("split", "")
    split_note = {
        "intra": "무작위 분할(같은 환자가 train/test에 섞임) — 파이프라인 통과용, 낙관적",
        "inter": "DS1/DS2 환자 단위 분리 — 실전 벤치마크(보통 더 낮게 나옴)",
    }.get(split, "")

    step = meta.get("step", "")
    quest = meta.get("quest", "")
    label = (f"{quest} 실험" if quest else f"{meta['week']}주차 실행")
    sub = f"{label} 로그 — {meta.get('task','')}"
    sub += f" · {step}" if step else ""
    sub += f" [{split}]"

    fm = [
        "---",
        f"id: {meta['id']}",
        "type: ailab",
        f"topic: {meta['topic']}",
        f"subtopic: {sub}",
        "kind: log",
        f"week: {meta['week']}",
        f"split: {split}",
        f"metric: {meta['metric']}",
        f"value: {meta['value']}",
        f"passed: {str(bool(meta.get('passed'))).lower()}",
        f"modality: {t.get('modality','')}",
        f"dataset: {t.get('dataset_key','')}",
        f"notebook: {meta.get('notebook','')}",
    ]
    if quest:
        fm.append(f"quest: {quest}")           # 이 실행이 어느 퀘스트에 귀속되나
    if step:
        fm.append(f"step: {step}")             # 퀘스트 실험 구분자(예: RR-hybrid)
    if meta.get("checkpoint"):
        fm.append(f"checkpoint: {meta['checkpoint']}")
    fm += [
        "source: \"MedKOS AI랩 실행 로그(ingest_run.py) · 실제 노트북 실행 결과\"",
        "confidence: high",
        f"date: {meta['date']}",
        f"tags: [ailab, run-log, week{meta['week']}, {split}, {meta['metric']}]",
    ]
    if meta.get("related"):
        fm.append(f"related: [{', '.join(meta['related'])}]")
    fm.append("---")

    body = [
        "",
        "## Overview",
        f"**{meta['week']}주차 실습을 실제로 돌린 결과 기록.** 이 카드는 결정론적으로",
        "`pipelines/ingest_run.py`가 노트북 결과에서 생성했다(수치는 실측 — 예측 아님).",
        "",
        f"- 🎯 과제: {meta.get('task','') or t['goal']}",
        f"- 📓 노트북: `{meta.get('notebook','(미기재)')}`",
        f"- 🔀 분할: **{split}** — {split_note}",
        f"- 🏁 결과: **{meta['metric']} = {meta['value']}** → {passed}{gate}",
    ]
    if meta.get("checkpoint"):
        body.append(f"- 💾 체크포인트: `{meta['checkpoint']}` (Drive는 파생물)")
    if quest:
        body.append(f"- 🎯 퀘스트: `{quest}`" + (f" · 실험 **{step}**" if step else ""))
    if meta.get("note"):
        body.append(f"- 📝 관찰: {meta['note']}")
    body += [
        "",
        "## Next",
    ]
    if quest:
        body += [
            f"- 이 결과는 퀘스트 `{quest}`에 쌓인다. 다음 목표는 퀘스트 카드의 `next_goal`을 갱신해 정한다",
            "  (홈페이지 🎯 심화 퀘스트에 '결과 + 다음 목표'가 함께 뜬다).",
        ]
    else:
        body += [
            "- 이 실행을 되돌아보는 심화는 `/deepen-week`가 이 로그의 `notebook`을 **직접 읽어** 쓴다",
            "  (glob 추정 대신 실제 코드 기준). 예측이 끼어들지 않는다.",
            "- `split: intra`로 통과했다면, `SPLIT=\"inter\"`로 한 번 더 돌려 실전 난이도를 로그로 남겨라.",
        ]
    body += [
        "",
        "## My notes",
        "<!-- 이 실행에서 관찰한 것을 한 줄로. 다음 /deepen-week·/ai-mentor가 이어받는다. -->",
        "",
    ]
    return "\n".join(fm + body)


def ingest(meta: dict, force_new: bool = False) -> Path:
    """로그 카드를 쓰고 경로를 반환. 같은 (week,split) 카드가 있으면 갱신(멱등)."""
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    existing = None if force_new else find_existing(
        meta["week"], meta.get("split", ""), meta.get("step", ""))
    if existing is not None:
        meta["id"] = load(existing).meta.get("id")  # id 유지(낭비·역행 방지)
        path = existing
    else:
        meta["id"] = next_id("ailab")
        path = LOGS_DIR / f"{meta['id']}.md"
    path.write_text(render_card(meta), encoding="utf-8")
    tag = meta.get("quest") or f"week{meta['week']}"
    record_topic("ailab", f"{tag} run {meta.get('step','') or meta.get('split','')}")
    return path


def build_meta(args) -> dict:
    data: dict = {}
    if args.results:
        data = json.loads(Path(args.results).read_text(encoding="utf-8"))

    week = args.week if args.week is not None else data.get("week")
    if week is None:
        raise SystemExit("week를 알 수 없습니다. --week N 또는 result.json에 week를 넣으세요.")

    metric, value = (args.metric, args.value)
    if metric is None or value is None:
        m2, v2 = _metric_value_from_results(data)
        metric = metric or m2
        value = value if value is not None else v2
    if metric is None or value is None:
        raise SystemExit("지표/값을 알 수 없습니다. --metric/--value 또는 result.json을 확인하세요.")

    passed = args.passed if args.passed is not None else bool(data.get("passed", False))
    t = topic_for_week(int(week))
    return {
        "week": int(week),
        "split": args.split or data.get("split", "intra"),
        "metric": metric,
        "value": float(value),
        "passed": passed,
        "task": args.task or data.get("task", "") or t["goal"],
        "notebook": args.notebook or data.get("notebook", ""),
        "checkpoint": args.checkpoint or data.get("checkpoint", ""),
        "topic": "Medical AI Lab",   # 실행 로그의 대주제(검색·연결 기준)
        "date": args.date or data.get("date") or date.today().isoformat(),
        "related": [r for r in (args.related or "").split(",") if r.strip()],
        # 퀘스트 실험이면 그 퀘스트에 귀속(홈페이지가 결과를 퀘스트 아래로 모은다).
        "quest": args.quest or data.get("quest", ""),
        "step": args.step or data.get("step", ""),
        "note": args.note or data.get("note", ""),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="실제 실행 결과 → 실행 로그 카드(kind: log)")
    ap.add_argument("--results", help="노트북이 남긴 result.json 경로")
    ap.add_argument("--week", type=int, help="주차(없으면 result.json에서)")
    ap.add_argument("--split", help="intra|inter (없으면 result.json 또는 intra)")
    ap.add_argument("--metric", help="지표명(없으면 result.json에서 추론)")
    ap.add_argument("--value", type=float, help="지표 실측값")
    ap.add_argument("--passed", dest="passed", action="store_true", default=None,
                    help="게이트 통과로 표시(생략 시 result.json의 passed)")
    ap.add_argument("--task", help="과제 설명(선택)")
    ap.add_argument("--notebook", help="실제로 돌린 repo 노트북 경로(예측 방지의 핵심)")
    ap.add_argument("--checkpoint", help="베스트 가중치 위치(예: drive:MedKOS/...)")
    ap.add_argument("--related", help="쉼표로 구분한 관련 카드 id")
    ap.add_argument("--date", help="실행일(ISO, 없으면 오늘)")
    ap.add_argument("--quest", help="이 실행이 귀속될 퀘스트 카드 id(예: ailab-2026-0011)")
    ap.add_argument("--step", help="퀘스트 실험 이름(예: 'RR-hybrid') — 같은 퀘스트의 실험 구분자")
    ap.add_argument("--note", help="한 줄 관찰(예: 'inter S-F1 0.18→0.46')")
    ap.add_argument("--force-new", action="store_true",
                    help="같은 (week,split,step) 로그가 있어도 새 카드로 발급")
    args = ap.parse_args()

    meta = build_meta(args)
    path = ingest(meta, force_new=args.force_new)
    print(f"실행 로그 기록: {path.relative_to(ROOT)}  "
          f"({meta['week']}주 · {meta['split']} · {meta['metric']}={meta['value']} · "
          f"{'통과' if meta['passed'] else '미달'})")
    if not meta["notebook"]:
        print("  ⚠️ notebook 경로가 비었습니다 — 실제 노트북을 repo에 커밋하고 --notebook로 지정하면"
              " /deepen-week가 예측 없이 실제 코드를 읽습니다.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
