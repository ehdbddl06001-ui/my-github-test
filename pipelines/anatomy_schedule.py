"""
anatomy_schedule.py — 2026-2학기 임상해부학술기 일정의 **단일 기준**.

사용자가 제공한 「2026학년도 2학기 수업시간표(의학과 2학년)」에서 확인된 일정만 담는다.
Drive의 `해부 수업계획서.xlsx`·파일명 날짜는 **과거 학기**이므로 절대 이 표를 덮어쓰지
못한다(테스트 고정: test_anatomy.py). spec: experiments/specs/anatomy-3q-2026.md §3.

phase 로직(결정론):
  ~09-09        t1-prep       Tagging 1 범위 우선
  09-10         t1-day        가벼운 rapid review (Tagging 1 당일)
  09-11~10-12   t2-new        Tagging 2 신규 범위 + T1 누적 취약점 소량
  10-13~10-18   t2-mock       신규 비중 축소, 혼합 mock tagging·분지/주행/층 연결
  10-19         final-review  최종 rapid review만
  10-20~        completed     새 생성·커밋 금지(no-op)
"""
from __future__ import annotations

from datetime import date, datetime, timedelta, timezone

KST = timezone(timedelta(hours=9))

# 자동 생성 종료: 2026-10-19 23:59:59 KST (Tagging 2 종료일)
END_DATE = date(2026, 10, 19)
START_DATE = date(2026, 8, 13)   # 루틴 시작일
TAGGING_1 = date(2026, 9, 10)
TAGGING_2 = date(2026, 10, 19)

# 2026 수업/시험 일정 — 단일 기준(사용자 제공 시간표). 순서 보존.
SCHEDULE_2026: list[dict] = [
    {"date": date(2026, 8, 18), "topics": ["orientation", "위령전례", "등·다리 피부벗기기"],
     "regions": ["back", "lower-limb"]},
    {"date": date(2026, 8, 20), "topics": ["등 얕은층·중간층·깊은층 근육", "볼기부위·넓적다리 뒤부분"],
     "regions": ["back", "lower-limb"]},
    {"date": date(2026, 8, 24), "topics": ["뒤통수밑삼각", "어깨뼈부위", "다리오금·종아리 뒤부위"],
     "regions": ["back", "lower-limb"]},
    {"date": date(2026, 8, 27), "topics": ["큰가슴근부위", "가슴벽",
     "얼굴·표정근육·귀밑샘·얼굴 신경/혈관·씹기근육·입술·바깥코·바깥귀"],
     "regions": ["thorax", "head"]},
    {"date": date(2026, 8, 31), "topics": ["가슴벽·가슴안·가슴막·위세로칸·심장막·심장", "관자부위·관자아래부위"],
     "regions": ["thorax", "head"]},
    {"date": date(2026, 9, 3), "topics": ["목의 삼각·목의 내장", "다리 얕은층·넓적다리 앞/안쪽칸·종아리 앞·발등"],
     "regions": ["neck", "lower-limb"]},
    {"date": date(2026, 9, 7), "topics": ["목의 뿌리·인두", "종아리 가쪽·발목 안쪽면·발바닥"],
     "regions": ["neck", "lower-limb"]},
    {"date": date(2026, 9, 10), "topics": ["Tagging 1"], "regions": [], "exam": "tagging-1"},
    {"date": date(2026, 9, 14), "topics": ["피드백", "팔 얕은근막·겨드랑", "기관·기관지·허파·뒤세로칸"],
     "regions": ["upper-limb", "thorax"]},
    {"date": date(2026, 9, 17), "topics": ["위팔 앞칸·팔오금·아래팔 앞칸·손바닥",
     "배벽·얕은근막·배근육·고샅관·정삭·음낭·고환"],
     "regions": ["upper-limb", "abdomen"]},
    {"date": date(2026, 9, 21), "topics": ["위팔 뒤칸·아래팔 뒤칸·손등",
     "복막·위·지라·간·작은창자·큰창자·샘창자·이자"],
     "regions": ["upper-limb", "abdomen"]},
    {"date": date(2026, 9, 28), "topics": ["척주·척수막", "샅·항문삼각·비뇨생식삼각·남녀 바깥생식기관"],
     "regions": ["back", "pelvis-perineum"]},
    {"date": date(2026, 10, 1), "topics": ["머리덮개·머리뼈 속구조·뇌 적출·눈확",
     "부신·콩팥·배대동맥·복막·가로막·뒤배벽"],
     "regions": ["head", "abdomen"]},
    {"date": date(2026, 10, 6), "topics": ["팔의 관절", "골반 복막·골반 절단·남녀 내부생식기관·골반가로막"],
     "regions": ["upper-limb", "pelvis-perineum"]},
    {"date": date(2026, 10, 8), "topics": ["머리 시상절단·입안·후두", "인두·후두", "다리의 관절"],
     "regions": ["head", "neck", "lower-limb"]},
    {"date": date(2026, 10, 19), "topics": ["Tagging 2"], "regions": [], "exam": "tagging-2"},
]


def kst_today() -> date:
    """KST 기준 오늘(루틴 컨테이너는 UTC이므로 반드시 이 함수로 판단)."""
    return datetime.now(tz=KST).date()


def phase_for(d: date) -> str:
    if d > END_DATE:
        return "completed"
    if d == TAGGING_2:
        return "final-review"
    if d > date(2026, 10, 12):
        return "t2-mock"
    if d > TAGGING_1:
        return "t2-new"
    if d == TAGGING_1:
        return "t1-day"
    return "t1-prep"


def exam_phase_for(d: date) -> str:
    """이 날짜의 학습이 겨냥하는 시험 구간."""
    return "tagging-1" if d <= TAGGING_1 else "tagging-2"


def next_session(d: date) -> dict | None:
    """d 이후(당일 포함) 첫 수업/시험. 없으면 None."""
    for s in SCHEDULE_2026:
        if s["date"] >= d:
            return s
    return None


def prev_session(d: date) -> dict | None:
    """d 이전(당일 제외) 마지막 수업/시험."""
    out = None
    for s in SCHEDULE_2026:
        if s["date"] < d:
            out = s
    return out


def days_until(d: date, target: date) -> int:
    return (target - d).days


def is_class_day(d: date) -> bool:
    return any(s["date"] == d for s in SCHEDULE_2026)


def summary(d: date) -> dict:
    """루틴 보고용 요약(결정론)."""
    nxt = next_session(d)
    return {
        "date": d.isoformat(),
        "phase": phase_for(d),
        "exam_phase": exam_phase_for(d),
        "is_class_day": is_class_day(d),
        "next_session": None if not nxt else {
            "date": nxt["date"].isoformat(), "topics": nxt["topics"],
            "exam": nxt.get("exam"),
        },
        "days_to_tagging1": days_until(d, TAGGING_1),
        "days_to_tagging2": days_until(d, TAGGING_2),
    }


if __name__ == "__main__":
    import json
    import sys
    d = date.fromisoformat(sys.argv[1]) if len(sys.argv) > 1 else kst_today()
    print(json.dumps(summary(d), ensure_ascii=False, indent=2))
