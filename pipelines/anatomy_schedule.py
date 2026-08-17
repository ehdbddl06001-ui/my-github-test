"""
anatomy_schedule.py — 2026-2학기 임상해부학술기 일정의 **단일 기준**.

사용자가 제공한 「2026학년도 2학기 수업시간표(의학과 2학년)」에서 확인된 일정만 담는다.
Drive의 `해부 수업계획서.xlsx`·파일명 날짜는 **과거 학기**이므로 절대 이 표를 덮어쓰지
못한다(테스트 고정: test_anatomy.py). spec: experiments/specs/anatomy-3q-2026.md §3.

2026-08-12: 사용자 업로드 **과정 확정본**(2026학년도 2학기 수업계획서 xlsx, 실습계획표
시트)과 전 회차 대조 완료 — 날짜·주제 16개 항목 모두 일치. 확정본에서 추가로 확인된
회차별 상세(담당교수·실습지침 페이지·e-Anatomy 영상 구간·응용과제)는 SESSION_DETAILS,
답안 표기 규정은 ANSWER_RULES 로 인코딩한다.

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

# 회차별 상세 — 2026 과정 확정본(실습계획표 시트) 실측. key = 회차(1-based).
# eanatomy: (부위 비디오, 구간) — 업로드 스캔(영상 캡처)의 회차 매핑·donor 탐색 기준.
SESSION_DETAILS: dict[int, dict] = {
    1: {"professor": "문용석", "guide_pages": "11-13p / 307p·311p",
        "eanatomy": [("Back — Superficial layer", "0:00~11:08"),
                     ("Lower limb — Superficial layer", "02:44~03:39 / 12:02~13:34")],
        "tasks": ["허리천자 방법·원칙", "꼬리마취 목적·방법", "척수신경 앞가지·뒤가지 차이"]},
    2: {"professor": "김홍태", "guide_pages": "12-19p / 307-312p",
        "eanatomy": [("Back — Superficial layer", "07:06~11:08"),
                     ("Back — Muscles of back", "00:00~23:53"),
                     ("Lower limb — Superficial layer", "02:41~03:40 / 12:00~13:00"),
                     ("Lower limb — Gluteal region & posterior thigh", "00:00~18:00")],
        "tasks": ["청진삼각·허리삼각 경계와 임상", "중간·작은볼기근과 직립보행", "볼기주사 회피 부위"]},
    3: {"professor": "김홍태", "guide_pages": "19-22p / 34-37p / 312-319p",
        "eanatomy": [("Back — Superficial layer", "10:25~10:40"),
                     ("Back — Muscles of back", "23:40~28:55"),
                     ("Upper limb — Scapular region", "00:00~18:08"),
                     ("Lower limb — Gluteal region & posterior thigh", "17:35~23:05"),
                     ("Lower limb — Leg", "0:00~13:20")],
        "tasks": ["어깨관절 근육 작용 시연", "겨드랑신경 손상 상황·결과", "어깨 동맥그물 임상"]},
    4: {"professor": "문용석", "guide_pages": "151-162p / 27-32p / 83-85p",
        "eanatomy": [("Head — Superficial layer of face", "0:00~46:38"),
                     ("Upper limb — Pectoral region", "0:00~13:55"),
                     ("Thorax — Thoracic wall", "00:00~06:58")],
        "tasks": ["삼차신경 가지·분포", "귀밑샘-얼굴신경 관계", "젖꼭지 표지점", "가슴천자"]},
    5: {"professor": "김홍태", "guide_pages": "184-191p / 86-104p",
        "eanatomy": [("Head — Superficial layer of face", "38:00~46:35"),
                     ("Head — Deep layer of face", "00:00~28:14"),
                     ("Thorax — Thoracic cavity and pleura", "00:00~12:48"),
                     ("Thorax — Superior mediastinum", "00:00~13:58"),
                     ("Thorax — Pericardium and heart", "00:00~41:29")],
        "tasks": ["아래이틀신경차단", "심장음 청진위치 vs 제자리 심장", "심장동맥 분포"]},
    6: {"professor": "문용석", "guide_pages": "117-130p / 293-307p·319-329p",
        "eanatomy": [("Neck — Triangle of neck (superficial)", "00:00~19:59"),
                     ("Neck — Triangle of neck (deep)", "00:00~26:45"),
                     ("Lower limb — Superficial layer", "00:00~13:34"),
                     ("Lower limb — Anterior & medial thigh", "00:00~31:31"),
                     ("Lower limb — Leg", "13:20~29:38"),
                     ("Lower limb — Foot", "0:00~5:42")],
        "tasks": ["목삼각 그림", "온목동맥 박동 촉진", "넙다리동맥 채혈·더듬자 삽입 이유"]},
    7: {"professor": "문용석", "guide_pages": "131-141p / 323-327p·330-334p",
        "eanatomy": [("Neck — Internal organ of neck", "00:00~06:48"),
                     ("Neck — Root of neck", "0:00~17:08"),
                     ("Neck — Pharynx", "0:00~07:37"),
                     ("Lower limb — Leg", "21:28~29:38"),
                     ("Lower limb — Foot", "05:43~17:17")],
        "tasks": ["기관절개 시연", "위가슴문 통과 구조물", "온종아리신경 손상", "발바닥활 보강 구조"],
        "note": "빗장뼈 절단 한쪽만; 발바닥은 한쪽 둘째층/다른쪽 넷째층"},
    8: {"professor": "김홍태·문용석", "exam": "tagging-1"},
    9: {"professor": "김홍태", "guide_pages": "105-115p / 38-47p",
        "eanatomy": [("Thorax — Trachea, Bronchus, Lung", "00:00~11:14"),
                     ("Thorax — Posterior mediastinum", "00:00~14:36"),
                     ("Upper limb — Superficial fascia", "00:00~06:49"),
                     ("Upper limb — Axilla", "00:00~30:33")],
        "tasks": ["주기관지 구조 차이와 이물질", "기관지허파구역", "팔신경얼기 부위별 손상"]},
    10: {"professor": "김홍태", "guide_pages": "48-51p·55-61p·69-75p / 215-230p",
         "eanatomy": [("Upper limb — Arm", "0:00~15:20"),
                      ("Upper limb — Forearm", "0:00~35:20"),
                      ("Upper limb — Hand", "1:30~26:20"),
                      ("Abdomen — Abdominal wall", "00:00~44:47")],
         "tasks": ["노동맥 채혈·더듬자 이유", "고샅탈장 구조적 이유"]},
    11: {"professor": "문용석", "guide_pages": "52-54p·62-69p / 231-248p",
         "eanatomy": [("Upper limb — Arm", "15:19~21:18"),
                      ("Upper limb — Forearm", "23:01~41:51"),
                      ("Upper limb — Hand", "0:00~01:17"),
                      ("Abdomen — Abdominal cavity", "0:00~59:00")],
         "tasks": ["노신경 손상 증상", "막창자꼬리 위치변이", "간문맥-대정맥연결"]},
    12: {"professor": "김홍태", "guide_pages": "23-26p / 261-274p",
         "eanatomy": [("Back — Spinal cord and meninges", "00:00~11:54"),
                      ("Perineum & Pelvis — Perineum", "00:00~31:22")],
         "tasks": ["척주관·척수 길이차와 허리천자", "골반바닥손상·episiotomy"]},
    13: {"professor": "문용석", "guide_pages": "163-183p / 248-260p",
         "eanatomy": [("Head — Scalp and cranium", "0:00~28:45"),
                      ("Head — Orbit", "00:00~36:11"),
                      ("Abdomen — Abdominal cavity", "59:14~1:16:47"),
                      ("Abdomen — Diaphragm & posterior wall", "00:00~11:06")],
         "tasks": ["섬모체신경절 부교감 작용", "위 내시경 비교", "ERCP 쓸개이자관", "팽대부 종양 황달"]},
    14: {"professor": "문용석", "guide_pages": "76-82p / 275-291p",
         "eanatomy": [("Upper limb — Joints of upper limb", "0:00~12:50"),
                      ("Perineum & Pelvis — Pelvis", "0:00~38:37")],
         "tasks": ["어깨관절 안정화 구조", "골반장기-복막 관계", "배뇨·배변 기전"],
         "note": "골반분리/내부생식기관 적출은 조별로 다르게"},
    15: {"professor": "김홍태", "guide_pages": "197-214p / 142-149p / 335-345p",
         "eanatomy": [("Head — Sagittal section of head", "00:00~12:14"),
                      ("Head — Oral cavity and tongue", "00:00~11:08"),
                      ("Head — Middle ear", "00:00~06:19"),
                      ("Neck — Pharynx", "00:00~10:58"),
                      ("Neck — Larynx", "00:00~13:17"),
                      ("Lower limb — Joints of the lower limb", "00:00~29:58")],
         "tasks": ["뇌하수체 접근법", "후두경 영상 비교", "십자인대 손상 확인법"]},
    16: {"professor": "김홍태·문용석", "exam": "tagging-2"},
}

# 예습시험·Tagging 답안 작성원칙 — 확정본 학습평가 시트 실측. 문항 카드의 answer 표기 기준.
ANSWER_RULES = {
    "terminology": "공인 한글용어 또는 원어용어 중 하나 (인정 교재: e-Anatomy, "
                   "사람해부실습지침 7판, Gray's Atlas 3rd, 국소해부학 5판, 무어 핵심임상해부학 5판)",
    "abbreviations": ["a.", "v.", "n.", "m.", "lig.", "sup.", "inf.", "ant.", "post.", "med.", "lat."],
    "abbreviation_note": "허용 약자만 인정, 마침표 필수",
    "muscle_naming": "한글용어는 ~근, 원어용어는 ~ muscle (또는 m.)",
    "preview_exam": "실습 전 예습시험(형성평가), 실습 전 수업에서 정답 확인",
    "grading_note": "총괄평가: 실습시험(Tagging 1·2) 중심 65%, 예습시험은 기타 평가에 포함",
}


def session_detail(no: int) -> dict:
    """회차 상세(확정본). 없으면 빈 dict."""
    return SESSION_DETAILS.get(no, {})


# 과거 학기 자료를 2026 회차에 배정할 때 쓰는 부위 키워드 사전.
# 값은 그 부위가 다뤄지는 SCHEDULE_2026 인덱스(=회차-1)가 아니라, 회차 번호다.
# 키는 영상 타이틀·실습주제에 실제로 쓰이는 말 그대로 적는다.
REGION_KEYWORDS: dict[str, int] = {
    # 1~3회차 — 등·볼기·넓적다리 뒤·뒤통수밑·어깨뼈·다리오금
    "피부벗기기": 1, "얕은근막": 1, "피부신경": 1, "볼기피부신경": 1, "장딴지신경": 1,
    "등 얕은층": 2, "등세모근": 2, "넓은등근": 2, "마름근": 2, "척주세움근": 2,
    "볼기부위": 2, "궁둥신경": 2, "넓적다리 뒤": 2, "햄스트링": 2,
    "뒤통수밑삼각": 3, "어깨뼈부위": 3, "네모공간": 3, "다리오금": 3, "종아리 뒤": 3,
    # 4~5회차 — 가슴·얼굴·관자
    "큰가슴근": 4, "작은가슴근": 4, "젖샘": 4, "가슴벽": 4, "갈비사이": 4,
    "얼굴": 4, "표정근육": 4, "귀밑샘": 4, "씹기근육": 4, "삼차신경": 4,
    "입술": 4, "바깥코": 4, "바깥귀": 4,
    "가슴안": 5, "가슴막": 5, "세로칸": 5, "심장막": 5, "심장": 5, "관자부위": 5,
    # 6회차 — 목의 삼각 / 다리 얕은층·넓적다리 앞·안쪽칸·종아리 앞·발등
    "목의 삼각": 6, "목삼각": 6, "앞목삼각": 6, "뒤목삼각": 6, "턱밑삼각": 6,
    "턱끝밑삼각": 6, "근육삼각": 6, "목동맥삼각": 6, "목신경얼기": 6, "넓은목근": 6,
    "목빗근": 6, "목의 내장": 6,
    "얕은정맥": 6, "큰두렁정맥": 6, "작은두렁정맥": 6,
    "넙다리삼각": 6, "넙다리동맥": 6, "넙다리신경": 6, "넓적다리 앞칸": 6,
    "넙다리네갈래근": 6, "넙다리빗근": 6, "모음근굴": 6, "넓적다리 안쪽칸": 6,
    "두덩정강근": 6, "종아리 앞칸": 6, "폄근지지띠": 6, "발등": 6,
    # 7회차 — 목의 뿌리·인두 / 종아리 가쪽·발목 안쪽면·발바닥
    "목의 뿌리": 7, "인두": 7, "종아리 가쪽": 7,
    "발목 안쪽면": 7, "굽힘근지지띠": 7, "발바닥": 7,
    # 카드의 `subregion` 슬러그(영문)도 같은 사전으로 본다 — 부위 기준 배정의
    # 입력이 한글 실습주제일 때도, 영문 슬러그일 때도 결정론이 하나로 유지된다.
    "superficial-back": 2, "deep-back": 2, "gluteal": 2, "posterior-thigh": 2,
    "suboccipital": 3, "scapular-region": 3, "popliteal-fossa": 3, "posterior-leg": 3,
    "pectoral": 4, "thoracic-wall": 4, "face": 4, "parotid": 4, "infratemporal": 4,
    "anterior-neck": 6, "femoral-triangle": 6,
    "anal-canal": 12, "perineum": 12,
    "pelvic-cavity": 14, "pelvic-diaphragm": 14, "urinary-bladder": 14,
    "male-internal-genitalia": 14, "female-internal-genitalia": 14,
    # 9~15회차
    "겨드랑": 9, "허파": 9, "기관지": 9, "뒤세로칸": 9,
    "위팔 앞칸": 10, "팔오금": 10, "아래팔 앞칸": 10, "손바닥": 10,
    "배벽": 10, "고샅관": 10, "정삭": 10, "음낭": 10, "고환": 10,
    "위팔 뒤칸": 11, "아래팔 뒤칸": 11, "손등": 11, "복막": 11, "작은창자": 11, "큰창자": 11,
    "척주": 12, "척수막": 12, "샅": 12, "항문삼각": 12, "비뇨생식삼각": 12,
    "머리덮개": 13, "눈확": 13, "콩팥": 13, "배대동맥": 13, "가로막": 13, "뒤배벽": 13,
    "팔의 관절": 14, "골반가로막": 14, "내부생식기관": 14,
    "입안": 15, "후두": 15, "다리의 관절": 15,
}


def session_for_region(text: str) -> int | None:
    """부위 이름(영상 타이틀·실습주제)으로 2026 회차 번호를 찾는다 — **부위 기준 배정**.

    과거 학기 스캔·영상은 담당교수가 지금과 다를 수 있고 파일명 날짜도 과거 학기다.
    그래서 **교수명·파일명으로 회차를 정하면 안 되고**, 그 자료가 다루는 부위를
    2026 시간표(SCHEDULE_2026)의 실습주제에 맞춰야 한다. 이 함수가 그 결정론이다.

    여러 키워드가 걸리면 가장 긴(구체적인) 키워드를 이긴 것으로 본다.
    못 찾으면 None — 사람이 판단하고 카드에 근거를 남긴다(추측 금지).
    """
    hits = [(len(k), no) for k, no in REGION_KEYWORDS.items() if k in text]
    return max(hits)[1] if hits else None


def session_no_for_date(d: date) -> int | None:
    """SCHEDULE_2026 상의 회차 번호(1-base). 시험일 포함."""
    for i, s in enumerate(SCHEDULE_2026, 1):
        if s["date"] == d:
            return i
    return None


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
