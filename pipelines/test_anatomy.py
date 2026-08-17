"""
test_anatomy.py — 해부학 파이프라인 회귀 테스트(pytest 없이 assert).

지키는 것:
  (1) 2026 일정이 단일 기준이고 과거 학기 날짜로 오염되지 않는다.
  (2) 종료일(10-19) 이후는 completed no-op.
  (3) anatomy frontmatter 계약(출처 강제·정답 분리·publishable 게이트).
  (4) inventory/answers 파싱의 결정론·idempotency.
  (5) 마스킹: label 100% 포함 검증, leak 검출, 원본 불변, no-OCR → review.
  (6) daily 선택: needs_review 제외, 문항 상한, 복습 슬롯.
  (7) export: 비공개 경로·금지 문자열이 번들에 없다.

실행: python pipelines/test_anatomy.py
"""
from __future__ import annotations

import json
import re
import sys
import tempfile
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import anatomy_answers  # noqa: E402
import anatomy_daily  # noqa: E402
import anatomy_inventory  # noqa: E402
import anatomy_mask  # noqa: E402
import anatomy_schedule as sched  # noqa: E402
from anatomy_extract import extract_terms  # noqa: E402
from frontmatter import validate  # noqa: E402


def test_schedule_is_2026_and_single_source() -> None:
    assert sched.TAGGING_1 == date(2026, 9, 10)
    assert sched.TAGGING_2 == date(2026, 10, 19)
    assert sched.END_DATE == date(2026, 10, 19)
    for s in sched.SCHEDULE_2026:
        assert s["date"].year == 2026, f"과거 학기 날짜 오염: {s['date']}"
        assert date(2026, 8, 18) <= s["date"] <= date(2026, 10, 19)
    # Drive 파일명 날짜(예: 0930=과거 학기)가 아니라 2026 표가 기준: 10-06에 팔의 관절
    d = [s for s in sched.SCHEDULE_2026 if s["date"] == date(2026, 10, 6)]
    assert d and "팔의 관절" in d[0]["topics"][0]


def test_phases_and_end_noop() -> None:
    assert sched.phase_for(date(2026, 8, 13)) == "t1-prep"
    assert sched.phase_for(date(2026, 9, 10)) == "t1-day"
    assert sched.phase_for(date(2026, 9, 11)) == "t2-new"
    assert sched.phase_for(date(2026, 10, 13)) == "t2-mock"
    assert sched.phase_for(date(2026, 10, 19)) == "final-review"
    assert sched.phase_for(date(2026, 10, 20)) == "completed"
    plan = anatomy_daily.build_plan(date(2026, 10, 20))
    assert plan["phase"] == "completed" and "no-op" in plan["action"]
    assert anatomy_daily.write_plan(plan, dry=True) is None  # 아무것도 쓰지 않음


def test_frontmatter_contract() -> None:
    base = {"id": "anatomy-2026-9999", "type": "anatomy", "topic": "Anatomy",
            "date": "2026-08-12", "confidence": "medium"}
    # question: source_refs·answer_separated·style 강제
    q = dict(base, kind="question", stem="문제", answer="정답구조물",
             question_style="relation",
             source_refs=[{"source_file_id": "x", "page": 3}],
             answer_separated=True)
    assert validate(q) == [], validate(q)
    assert any("source_refs" in e for e in validate(dict(q, source_refs=None)))
    assert any("answer_separated" in e for e in validate(dict(q, answer_separated=False)))
    assert any("question_style" in e for e in validate(dict(q, question_style="???")))
    # 단답형 정답이 stem에 노출되면 실패
    leak = dict(q, stem="이 구조물은 정답구조물이다. 이름은?")
    assert any("노출" in e for e in validate(leak))
    # source_page: 페이지 번호도 text-lane 마커도 없으면 실패
    sp = dict(base, kind="source_page", source_file_id="x")
    assert any("source_page" in e for e in validate(sp))
    ok_text = dict(sp, extraction="drive-mcp-text", section="어깨관절")
    assert validate(ok_text) == []
    ok_page = dict(sp, source_page=12)
    assert validate(ok_page) == []


def test_inventory_deterministic_and_idempotent() -> None:
    f = {"id": "F1", "title": "14차시(0930) 문용석pf.pdf", "fileSize": "100",
         "modifiedTime": "2026-08-04T05:18:00Z", "mimeType": "application/pdf",
         "folder": "해부2"}
    assert anatomy_inventory.source_id_for(f["title"], "해부2") == "a2-s14"
    assert anatomy_inventory.source_id_for("tagging 2차.pdf", "해부2") == "a2-tagging2"
    assert anatomy_inventory.source_id_for("해부 수업계획서.xlsx", "해부2") == "a2-plan"
    m1, ch1 = anatomy_inventory.build_card(f, None, "2026-08-12")
    assert ch1 and m1["revision"] == 1 and m1["status"] == "listed"
    assert m1["publishable"] is False
    # 같은 메타로 재실행 → 변경 없음(idempotent)
    m2, ch2 = anatomy_inventory.build_card(f, m1, "2026-08-13")
    assert not ch2
    # modifiedTime 변경 → revision 증가 + stale
    f2 = dict(f, modifiedTime="2026-09-01T00:00:00Z")
    m3, ch3 = anatomy_inventory.build_card(f2, m1, "2026-09-02")
    assert ch3 and m3["revision"] == 2 and m3["status"] == "stale"


def test_answers_parse_no_fabrication() -> None:
    text = """Upper Limb: Axilla
● 겨드랑정맥(axillary vein)
37. 앞위팔휘돌이동맥(anterior circumflex humeral artery)
[ 신경 Nerve ]
● 정중신경(median nerve)
"""
    items = anatomy_answers.parse_items(text)
    assert len(items) == 3
    numbered = [i for i in items if i["answer_only_candidate"]]
    assert len(numbered) == 1 and numbered[0]["no"] == 37
    assert numbered[0]["priority"] == "high"
    assert numbered[0]["region"] == "upper-limb"
    plain = [i for i in items if not i["answer_only_candidate"]]
    assert all(i["priority"] == "normal" for i in plain)
    # 질문 텍스트를 지어내는 필드가 없다
    assert all("stem" not in i and "question" not in i for i in items)


def test_terms_regex() -> None:
    t = extract_terms("돌림근띠 (rotator cuff)와 어깨밑근(subscapularis muscle)을 확인")
    assert {x["en"] for x in t} == {"rotator cuff", "subscapularis muscle"}


def _fake_extract(has_text=True):
    return {
        "source_id": "fx", "page": 1, "width": 300, "height": 200,
        "has_text_layer": has_text,
        "blocks": [
            {"text": "겨드랑동맥(axillary artery)", "bbox": [10, 10, 120, 22]},
            {"text": "쇄골 아래를 지나는 동맥이다", "bbox": [10, 40, 150, 52]},
        ],
        "terms": [{"ko": "겨드랑동맥", "en": "axillary artery", "bbox": [10, 10, 120, 22]}],
    }


def test_mask_build_verify_and_review_queue() -> None:
    rec = _fake_extract()
    m = anatomy_mask.build_masks(rec)
    assert m["status"] == "masked" and len(m["masks"]) == 1
    chk = anatomy_mask.verify_leakage(rec, m)
    assert chk["ok"], chk
    # 같은 정답 문자열이 마스크 밖에 또 있으면 leak
    rec2 = _fake_extract()
    rec2["blocks"].append({"text": "정답은 겨드랑동맥", "bbox": [10, 100, 150, 112]})
    chk2 = anatomy_mask.verify_leakage(rec2, anatomy_mask.build_masks(rec2))
    # build_masks는 terms 기반이라 새 블록은 마스크가 안 됨 → leak으로 잡혀야 한다
    assert not chk2["ok"] and chk2["leaks"]
    # 텍스트 레이어 없음(OCR 부재) → 마스크 없이 review로
    m3 = anatomy_mask.build_masks(_fake_extract(has_text=False))
    assert m3["status"] == "needs_review" and m3["masks"] == []


def test_mask_pipeline_on_synthetic_pdf() -> None:
    """합성 fixture PDF로 분해→추출→마스크→렌더→원본 불변까지 통합 검증."""
    import hashlib

    import fitz
    from anatomy_extract import extract_page
    from anatomy_ingest import split_pdf

    tmp = Path(tempfile.mkdtemp())
    pdf = tmp / "fixture.pdf"
    doc = fitz.open()
    page = doc.new_page(width=300, height=200)
    page.insert_text((20, 30), "겨드랑동맥(axillary artery)", fontname="helv", fontsize=11)
    page.insert_text((20, 60), "R", fontsize=9)  # 방향표시 — 마스크 금지
    doc.save(pdf)
    doc.close()
    orig_hash = hashlib.sha256(pdf.read_bytes()).hexdigest()

    n = split_pdf(pdf, tmp / "pages", dry=False)
    assert n == 1 and (tmp / "pages" / "page-0001.png").exists()

    d = fitz.open(pdf)
    rec = {"source_id": "fx", "page": 1, **extract_page(d[0])}
    d.close()
    # 한글 텍스트가 helv 폰트로 안 들어가는 환경이면 영문만으로도 페어가 안 잡힌다 —
    # 그 경우 이 통합 테스트는 단위 테스트(test_mask_build_verify)로 대체된다.
    if rec["terms"]:
        m = anatomy_mask.build_masks(rec)
        assert m["status"] == "masked"
        assert all(t["en"] != "R" for t in rec["terms"])  # 방향표시 미마스킹
        anatomy_mask.render_quiz(tmp / "pages" / "page-0001.png", m,
                                 (rec["width"], rec["height"]), tmp / "quiz.png")
        assert (tmp / "quiz.png").exists()
        assert anatomy_mask.verify_leakage(rec, m)["ok"]
    # 원본 PDF는 어떤 단계에서도 변경되지 않는다
    assert hashlib.sha256(pdf.read_bytes()).hexdigest() == orig_hash


def test_daily_selection_rules() -> None:
    plan = anatomy_daily.build_plan(date(2026, 8, 13))
    assert plan["phase"] == "t1-prep"
    assert len(plan["question_ids"]) <= 12
    assert plan["days_to_tagging1"] == 28
    # 시험 당일은 rapid review만(신규 개념 슬롯 0)
    t1 = anatomy_daily.build_plan(date(2026, 9, 10))
    assert t1["phase"] == "t1-day"
    assert sum(len(v) for v in t1["concepts"].values()) == 0
    # needs_review 카드는 덱에서 제외
    assert anatomy_daily._deck_eligible({"needs_review": True}) is False
    assert anatomy_daily._deck_eligible({}) is True


def test_export_bundle_has_no_private_material() -> None:
    out = Path(__file__).resolve().parent.parent / "docs" / "anatomy-data.js"
    if not out.exists():
        return  # 번들 미생성 환경(신규 clone)에서는 건너뜀
    blob = out.read_text(encoding="utf-8")
    for bad in (".private", "drive.google.com", "rclone", "token"):
        assert bad not in blob, f"금지 문자열 노출: {bad}"
    payload = json.loads(blob.split("window.MEDKOS_ANATOMY = ", 1)[1].rstrip().rstrip(";"))
    for q in payload["questions"]:
        assert q.get("refs"), f"출처 없는 문항 공개: {q['id']}"
    # Drive file ID(영숫자 28+자)가 웹 번들에 노출되지 않는지
    for q in payload["questions"] + payload["concepts"]:
        for r in q.get("refs", []):
            assert "source_file_id" not in r


def test_missing_dates_backlog() -> None:
    """이용 한도 초과로 밀린 날을 결정론적으로 찾는다: START~어제 중 daily 카드 없는 날."""
    today = date(2026, 8, 20)
    miss = anatomy_daily.missing_dates(today)
    assert all(m < today for m in miss)
    assert date(2026, 8, 13) not in miss  # 계획 카드가 이미 존재하는 날은 제외
    assert miss == sorted(miss)           # 오래된 순
    assert anatomy_daily.missing_dates(today, limit=2) == miss[:2]
    # completed 구간은 아예 대상이 아니다
    assert anatomy_daily.missing_dates(date(2026, 12, 1)) == \
        [m for m in anatomy_daily.missing_dates(date(2026, 12, 1))
         if sched.phase_for(m) != "completed"]


def test_mask_patch_pins_and_redraw_flag() -> None:
    """자연 패치 모드: 번호핀 결정론 배번 + 대면적 마스크는 재작화 권고."""
    rec = _fake_extract()
    rec["terms"].append({"ko": "노동맥", "en": "radial artery", "bbox": [30, 10, 120, 24]})
    m = anatomy_mask.build_masks(rec)
    pins = [x["pin"] for x in sorted(m["masks"], key=lambda x: x["pin"])]
    assert pins == list(range(1, len(m["masks"]) + 1))  # 1..N 빠짐없이
    # 위→아래 순서: y가 더 작은 라벨이 앞 번호
    top = min(m["masks"], key=lambda x: x["polygon"][0][1])
    assert top["pin"] == 1
    assert not m.get("redraw_recommended")
    # 페이지의 큰 면적을 가리면 재작화 권고
    big = _fake_extract()
    big["width"], big["height"] = 100, 100
    big["terms"] = [{"ko": "가", "en": "aa", "bbox": [5, 5, 95, 60]}]
    assert anatomy_mask.build_masks(big).get("redraw_recommended") is True
    # 배경 샘플링은 항상 불투명 RGB(정답이 비칠 수 없음), 띠가 없으면 NEUTRAL 폴백
    from PIL import Image
    img = Image.new("RGB", (50, 50), (200, 190, 180))
    c = anatomy_mask._sample_bg(img, [10, 10, 40, 40])
    assert c == (200, 190, 180)
    assert anatomy_mask._sample_bg(img, [0, 0, 50, 50]) == anatomy_mask.NEUTRAL


def test_preview_exam_signal() -> None:
    """예습시험 신호: 수업 D-2 prepare / D-1 finalize(전날 아침 마감) / 당일 class-day."""
    from datetime import date as _date
    assert anatomy_daily.preview_exams(_date(2026, 8, 17))[0]["phase"] == "finalize"
    both = anatomy_daily.preview_exams(_date(2026, 8, 18))
    assert [x["phase"] for x in both] == ["class-day", "prepare"]  # 당일 + 다음 회차 D-2
    assert both[1]["session_no"] == 2 and both[1]["due"] == "2026-08-19"
    # 시험일(Tagging)은 예습시험 대상이 아니다
    assert all(x["session_no"] != 8 for x in anatomy_daily.preview_exams(_date(2026, 9, 9)))
    # 월요일 수업(8/24) → 일요일(8/23) 아침 finalize (주말 루틴 필수 근거)
    sun = anatomy_daily.preview_exams(_date(2026, 8, 23))
    assert any(x["phase"] == "finalize" and x["class_date"] == "2026-08-24" for x in sun)


def test_session_details_match_confirmed_plan() -> None:
    """확정본(2026 수업계획서 실습계획표) 상세: 16회차 전부, 시험 회차 표시, 답안 규정."""
    from anatomy_schedule import ANSWER_RULES, SCHEDULE_2026, SESSION_DETAILS, session_detail
    assert set(SESSION_DETAILS) == set(range(1, len(SCHEDULE_2026) + 1))
    assert SESSION_DETAILS[8].get("exam") == "tagging-1"
    assert SESSION_DETAILS[16].get("exam") == "tagging-2"
    # 수업 회차는 e-Anatomy 구간·담당교수를 가진다(스캔 회차 매핑 근거)
    for no, d in SESSION_DETAILS.items():
        assert d.get("professor"), f"{no}회차 교수 누락"
        if not d.get("exam"):
            assert d.get("eanatomy"), f"{no}회차 e-Anatomy 구간 누락"
    assert "m." in ANSWER_RULES["abbreviations"]
    assert session_detail(99) == {}


def test_pdf_builder_selftest() -> None:
    """학습자료 PDF: 조판·frontmatter 파싱·.private 출력 가드 회귀 (anatomy_pdf --selftest)."""
    import subprocess
    r = subprocess.run([sys.executable, str(Path(__file__).parent / "anatomy_pdf.py"),
                        "--selftest"], capture_output=True, text=True)
    assert r.returncode == 0, f"anatomy_pdf selftest 실패: {r.stdout}{r.stderr}"


def test_unit_label_session_and_region() -> None:
    """날짜순 목록의 소속 배지('2회차 · 등') — 시간표가 유일 기준이고 부분일치를 안 만든다."""
    from anatomy_schedule import region_label, session_no_for_date, unit_label

    assert unit_label({"session_no": 2, "region": "back"}) == "2회차 · 등"
    # session_no 가 없으면 scheduled_dates 를 시간표에 대조해 회차를 구한다.
    assert unit_label({"scheduled_dates": ["2026-08-20"], "region": "lower-limb"}) == "2회차 · 다리"
    # 두 회차에 걸쳐 배우는 페이지 카드는 둘 다 적는다.
    assert unit_label({"scheduled_dates": ["2026-09-14", "2026-09-21"],
                       "region": "upper-limb"}) == "9·11회차 · 팔"
    # region 만 있는 인제스트 카드는 부위만.
    assert unit_label({"region": "abdomen"}) == "배"
    # multi 는 그 회차의 시간표 부위로 넓혀 적는다.
    assert unit_label({"session_no": 1, "region": "multi"}) == "1회차 · 등·다리"
    # daily plan 은 regions(복수) 를 쓴다.
    assert unit_label({"regions": ["back", "lower-limb"]}) == "등·다리"
    assert unit_label({}) == ""
    # 시험일(Tagging 1)은 부위가 없다 → 회차만.
    assert unit_label({"scheduled_dates": ["2026-09-10"]}) == "8회차"
    assert session_no_for_date(date(2026, 8, 18)) == 1
    assert session_no_for_date(date(2026, 8, 19)) is None      # 수업 없는 날
    assert region_label(["back", "back"]) == "등"              # 중복 제거
    # 배지 클릭은 정확일치여야 한다 — 접두어가 겹치면 1회차가 11회차를 끌고 온다.
    assert unit_label({"session_no": 11, "region": "back"}).split(" · ")[0] != "1회차"


def test_region_not_professor_decides_session() -> None:
    """과거 학기 자료의 회차 배정은 **부위** 기준이다 — 교수명·파일명 날짜가 아니라.

    사용자 지시(2026-08-15): "교수님 이름을 따라갈 필요 없이 부위별로 공부한다고 했던
    부분 기준으로 만들어라". 과거 학기 실습표의 담당교수·날짜는 지금과 다를 수 있다.
    """
    from anatomy_schedule import SCHEDULE_2026, session_for_region, session_no_for_date

    # 업로드된 과거 '실습6' 표: 담당교수 문용석 / 9월 1일 — 둘 다 2026 기준이 아니다.
    # 부위(목의 삼각·넓적다리 앞·안쪽·종아리 앞·발등)로 보면 2026-09-03 = 6회차.
    assert session_for_region("목의 삼각") == 6
    assert session_for_region("넓적다리 앞칸 넙다리네갈래근") == 6
    assert session_for_region("발등의 근육과 힘줄") == 6
    assert session_no_for_date(SCHEDULE_2026[5]["date"]) == 6

    # 같은 스캔에 섞여 있어도 발목 안쪽면·굽힘근지지띠는 2026에선 7회차다.
    assert session_for_region("발목 안쪽면") == 7
    assert session_for_region("굽힘근지지띠") == 7

    # 앞 회차 부위도 제자리를 찾아야 한다.
    assert session_for_region("뒤통수밑삼각") == 3
    assert session_for_region("볼기부위") == 2
    assert session_for_region("없는부위이름") is None


def test_branch_tree_selftest() -> None:
    """분지 계보 트리 생성기: 배치 겹침·노드별 색·강조 렌더 회귀."""
    import subprocess
    r = subprocess.run([sys.executable, str(Path(__file__).parent / "branch_tree.py"),
                        "--selftest"], capture_output=True, text=True)
    assert r.returncode == 0, f"branch_tree selftest 실패: {r.stdout}{r.stderr}"


def test_every_session_has_nerve_and_vessel_tree() -> None:
    """서브노트를 만든 회차는 신경·혈관·다발 트리를 모두 갖는다(사용자 지시 2026-08-16)."""
    sys.path.insert(0, str(Path(__file__).parent))
    from branch_specs import SPECS
    sessions = {k.split("-")[0] for k in SPECS}
    for s in sessions:
        for suffix in ("nerve", "vessel", "bundle"):
            assert f"{s}-{suffix}" in SPECS, f"{s}: {suffix} 트리 없음"


def test_diagram_manifest_covers_every_svg() -> None:
    """도해 갤러리 매니페스트: 자산 누락·유령 항목·날짜 없음 회귀(2026-08-16)."""
    import subprocess
    r = subprocess.run([sys.executable, str(Path(__file__).parent / "export_diagrams_web.py"),
                        "--selftest"], capture_output=True, text=True)
    assert r.returncode == 0, f"export_diagrams_web selftest 실패: {r.stdout}{r.stderr}"
    # 생성기가 만든 tree-*.svg 는 전부 현재 스펙에 대응해야 한다(이름 바꾼 옛 파일 잔존 금지)
    sys.path.insert(0, str(Path(__file__).parent))
    from branch_specs import SPECS
    root = Path(__file__).resolve().parents[1]
    for p in (root / "docs" / "assets" / "anatomy").glob("tree-*.svg"):
        key = p.stem.rsplit("-", 1)[0][len("tree-"):]
        assert key in SPECS, f"스펙 없는 유령 도해: {p.name}"


def test_every_question_has_a_session() -> None:
    """모든 문항에 `scheduled_dates` 가 있어야 회차 필터·일일 큐에 잡힌다(2026-08-17).

    초기 문항 39건이 이 값 없이 만들어져 웹 '오늘의 문항'에서 영영 안 뽑혔다.
    backfill_sessions.py 가 **부위 기준**으로 채웠고, 다시 새는 것을 여기서 막는다.
    """
    root = Path(__file__).resolve().parents[1]
    bad = []
    for p in (root / "content/anatomy/questions").rglob("*.md"):
        if not re.search(r"^scheduled_dates:", p.read_text(encoding="utf-8"), re.M):
            bad.append(p.name)
    assert not bad, f"scheduled_dates 없는 문항: {bad[:8]} (총 {len(bad)}건)"


def test_backfill_uses_region_not_professor() -> None:
    """회차 백필도 교수명·과거 학기 날짜가 아니라 부위로 정한다."""
    import subprocess
    r = subprocess.run([sys.executable, str(Path(__file__).parent / "backfill_sessions.py"),
                        "--selftest"], capture_output=True, text=True)
    assert r.returncode == 0, f"backfill_sessions selftest 실패: {r.stdout}{r.stderr}"


def test_subnotes_carry_memory_aids() -> None:
    """서브노트마다 암기 3종(두문자·빈칸·자가점검)의 재료가 있어야 한다(2026-08-17).

    빈칸·자가점검은 본문에서 자동 파생되므로 `==하이라이트==` 와 `### 소제목` 이,
    두문자 표는 `mnemonics:` 가 재료다. 하나라도 비면 그 회차만 암기 페이지가 사라진다.
    """
    sys.path.insert(0, str(Path(__file__).parent))
    import yaml
    from anatomy_subnote import cloze_items, self_check_items
    root = Path(__file__).resolve().parents[1]
    notes = sorted((root / "content/anatomy/notes").glob("*-subnote.md"))
    assert notes, "서브노트가 없다"
    for p in notes:
        raw = p.read_text(encoding="utf-8")
        _, fm, body = raw.split("---", 2)
        meta = yaml.safe_load(fm) or {}
        mn = meta.get("mnemonics") or []
        assert len(mn) >= 5, f"{p.name}: 두문자 {len(mn)}줄 (5줄 이상 필요)"
        assert all(m.get("key") and m.get("full") for m in mn), f"{p.name}: 빈 두문자 줄"
        assert len(cloze_items(body)) >= 10, f"{p.name}: 빈칸 재료(==하이라이트==) 부족"
        assert len(self_check_items(body)) >= 5, f"{p.name}: 자가점검 재료 부족"
def test_subnote_builder_selftest() -> None:
    """서브노트: 도해 레인·0절 제외·문항 합본·.private 가드 회귀 (anatomy_subnote --selftest)."""
    import subprocess
    r = subprocess.run([sys.executable, str(Path(__file__).parent / "anatomy_subnote.py"),
                        "--selftest"], capture_output=True, text=True)
    assert r.returncode == 0, f"anatomy_subnote selftest 실패: {r.stdout}{r.stderr}"


def test_publish_lane_guard() -> None:
    """publish.py: 콘텐츠만 main 자동 푸시, 코드 변경은 거부(2026-08-17).

    루틴이 매일 만드는 것(content/·docs/)은 사람 개입 없이 main 에 올라가야 하고,
    파이프라인·스킬·규칙 변경은 반드시 사람이 보게 막아야 한다.
    """
    import subprocess
    r = subprocess.run([sys.executable, str(Path(__file__).parent / "publish.py"),
                        "--selftest"], capture_output=True, text=True)
    assert r.returncode == 0, f"publish selftest 실패: {r.stdout}{r.stderr}"
    sys.path.insert(0, str(Path(__file__).parent))
    from publish import classify
    # 해부 루틴의 하루치 산출물은 전부 콘텐츠 레인이어야 한다
    daily = ["content/anatomy/daily/2026-08-20.md",
             "content/anatomy/questions/tagging-1/anatomy-2026-0200.md",
             "docs/anatomy-data.js", "docs/search-index.js"]
    assert classify(daily)[1] == [], "일일 산출물이 코드 레인으로 분류됨"
    # 파이프라인·스킬은 반드시 코드 레인
    assert classify(["pipelines/anatomy_daily.py"])[0] == []
    assert classify([".claude/skills/anatomy-daily/SKILL.md"])[0] == []


def test_legacy_professor_names_are_marked() -> None:
    """파일명에서 온 **과거 학기 교수명**이 2026 근거처럼 남아 있지 않아야 한다(2026-08-17).

    2026 확정본 담당은 문용석·김홍태 둘뿐인데, 업로드 스캔의 파일명은 과거 학기의
    회차·날짜·담당교수를 달고 있다. 그 이름이 카드 frontmatter 에 표시 없이 남으면
    '이 회차는 그 교수 자료' 로 잘못 읽힌다 — 실제로 그 교수가 올해 수업에 들어오지
    않는다는 사실이 확인됐다. 배정 기준은 부위지 교수가 아니다.
    """
    import subprocess
    r = subprocess.run([sys.executable, str(Path(__file__).parent / "legacy_sources.py"),
                        "--selftest"], capture_output=True, text=True)
    assert r.returncode == 0, f"legacy_sources selftest 실패: {r.stdout}{r.stderr}"
    sys.path.insert(0, str(Path(__file__).parent))
    from legacy_sources import current_professors, needs_mark
    cur = current_professors()
    assert cur == {"문용석", "김홍태"}, f"2026 담당 집합이 바뀌었다: {cur}"
    root = Path(__file__).resolve().parents[1]
    bad = []
    for p in (root / "content/anatomy").rglob("*.md"):
        names = needs_mark(p.read_text(encoding="utf-8"), cur)
        if names:
            bad.append((p.name, sorted(set(names))))
    assert not bad, f"표시 없는 과거 학기 교수명: {bad[:6]} (총 {len(bad)}건)"


TESTS = [v for k, v in sorted(globals().items()) if k.startswith("test_")]

if __name__ == "__main__":
    failed = 0
    for t in TESTS:
        try:
            t()
            print(f"[ OK ] {t.__name__}")
        except AssertionError as e:
            failed += 1
            print(f"[FAIL] {t.__name__}: {e}")
    print(f"\n{len(TESTS) - failed}/{len(TESTS)} 통과")
    sys.exit(1 if failed else 0)
