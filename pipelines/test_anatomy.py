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
