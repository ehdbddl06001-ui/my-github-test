"""
check_week.py — AI랩 '완료 게이트'. 이번 주 실습이 기준을 넘었는지 판정하고,
통과하면 자동으로 다음 주차 과제를 제시한다.

판정은 결정론(코드)이 한다: 커리큘럼(datasets.py)의 metric·target과, 학습 노트북이
남긴 결과(results.json 또는 직접 입력한 값)를 비교한다. LLM이 '학습됐다'를 지어내지
않는다. 애매한 경우(질적 통과)는 --pass 로 사람이/멘토가 넘긴다.

우리 지표는 모두 '높을수록 좋음'(macro_f1·auroc·dice·qwk·downstream_gain).

사용:
  python pipelines/check_week.py --value 0.83          # 이번 주 지표값 제출 → 판정
  python pipelines/check_week.py --results results.json # 노트북 산출 파일에서 읽어 판정
  python pipelines/check_week.py --status               # 이번 주 기준만 확인(판정 안 함)
  python pipelines/check_week.py --pass                 # 질적 통과(멘토 승인) → 다음 주차로

results.json 예: {"week": 1, "metric": "macro_f1", "value": 0.83, "notes": "..."}
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

try:
    from datasets import current_topic, topic_for_week, TOTAL_WEEKS
    from state import advance_ailab_week, ailab_week
except ImportError:  # from pipelines.* 로 import 되는 경우
    from pipelines.datasets import current_topic, topic_for_week, TOTAL_WEEKS
    from pipelines.state import advance_ailab_week, ailab_week


def _print_topic(t: dict, header: str) -> None:
    print(f"── {header}: {t['week']}주차 / 총 {t['total']}주 ──")
    print(f"  🎯 {t['goal']}  ({t['arch']})")
    print(f"  📦 {t['dataset_name']}  🔗 {t['dataset_url']}")
    if t.get("metric"):
        print(f"  ✅ 통과 기준: {t['metric']} ≥ {t['target']}")
    if t.get("deliverable"):
        print(f"  📝 산출물: {t['deliverable']}")


def read_value(args) -> tuple[float | None, str | None]:
    """--value 또는 --results 에서 (값, 지표명)을 얻는다."""
    if args.value is not None:
        return float(args.value), None
    if args.results:
        data = json.loads(Path(args.results).read_text(encoding="utf-8"))
        v = data.get("value")
        return (None if v is None else float(v)), data.get("metric")
    return None, None


def main() -> int:
    ap = argparse.ArgumentParser(description="AI랩 주차 완료 게이트")
    ap.add_argument("--value", type=float, help="이번 주 지표 달성값")
    ap.add_argument("--results", help="결과 JSON 경로({'metric','value'})")
    ap.add_argument("--status", action="store_true", help="기준만 확인(판정 안 함)")
    ap.add_argument("--pass", dest="force_pass", action="store_true",
                    help="질적 통과(멘토 승인) — 값 검사 없이 다음 주차로")
    args = ap.parse_args()

    cur = current_topic()

    if args.status:
        _print_topic(cur, "이번 주")
        return 0

    target = cur.get("target")
    value, got_metric = read_value(args)

    # 질적 통과(멘토 승인)
    if args.force_pass:
        nxt = advance_ailab_week(TOTAL_WEEKS, cur.get("metric"), value)
        print(f"🟢 질적 통과 처리(멘토 승인). {cur['week']}주차 완료 → {nxt}주차로.")
        _print_topic(topic_for_week(nxt), "다음 과제")
        return 0

    if value is None:
        print("판정할 값이 없습니다. --value 0.83 또는 --results results.json 을 주세요.")
        _print_topic(cur, "이번 주")
        return 2

    if got_metric and cur.get("metric") and got_metric != cur["metric"]:
        print(f"⚠️  결과의 metric('{got_metric}')이 기준('{cur['metric']}')과 다릅니다. "
              f"값만으로 판정합니다.")

    if target is None or value >= float(target):
        nxt = advance_ailab_week(TOTAL_WEEKS, cur.get("metric"), value)
        print(f"🟢 통과! {cur['metric']}={value:.4f} ≥ {target}. "
              f"{cur['week']}주차 완료 → {nxt}주차로 넘어갑니다.")
        if nxt == cur["week"]:
            print("🎉 마지막 주차까지 완료했습니다. 커리큘럼 한 바퀴 끝!")
        else:
            _print_topic(topic_for_week(nxt), "다음 과제")
        return 0

    gap = float(target) - value
    print(f"🟡 아직 기준 미달: {cur['metric']}={value:.4f} < {target} (부족 {gap:.4f}). "
          f"다음 주차로 넘기지 않습니다.")
    print("   힌트: 데이터 증강·클래스가중치·에폭/학습률 조정·전처리 점검을 먼저 보세요.")
    print("   개념·코드가 막히면 /ai-mentor 로 질적 리뷰를 요청하세요(막판엔 --pass 로 승인 가능).")
    return 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except BrokenPipeError:
        pass
